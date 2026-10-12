"""O redator precisa entregar conhecimento avaliável antes da revisão."""
import copy
import json
import tempfile
import unittest
from pathlib import Path

from pipeline.inventario import extracao as X, revisao as R, consolidacao as C, fichas as F
from pipeline.inventario.textutil import write_jsonl

HISTORY = 'O responsável havia realizado apenas duas viagens na unidade desde a data indicada no relatório de investigação.'
LESSON = 'No caso investigado, o treinamento inadequado e a passagem de serviço deficiente deixaram o responsável tomando decisões sem conhecer as condições dos sistemas.'
SUB = {'key':'s1','topico':'KPI','subtopico':'Desempenho das equipes'}
SUBJECTS = [{'id':'a01','texto':'desempenho das equipes','generico':False,
             'consulta_pt':'desempenho das equipes','consulta_en':'team performance'}]


def item(text=LESSON):
    return {'tipo':'licao_incidente','afirmacao':text,'condicoes':'Caso investigado, sem universalizar causalidade.',
            'entidades':[],'assuntos':['a01'],'aplicabilidade':'fpso_direta','valor_para_pergunta':'alto',
            'carater_avaliativo':'conhecimento_profissional',
            'alvo_qa':'Reconhecer a relação entre preparação para a função e conhecimento dos sistemas.',
            'citacao':text,
            'redacao':{'ajuste':'nenhum','afirmacao_original':text,
                       'condicoes_originais':'Caso investigado, sem universalizar causalidade.',
                       'base':'fonte_original','motivo':'','referencias':[],'suporte_citacao':True}}


def extract(value, source_text=None):
    class LLM:
        def json(self,*args,**kwargs):
            data={'unidades':[copy.deepcopy(value)]}
            kwargs['validate'](data)
            return data
    chunk={'chunk_id':'d','collection':'anp','document_id':'d','title':'Relatório',
           'texto':value['citacao'] if source_text is None else source_text}
    return X.extract_chunk(LLM(),SUB,chunk,SUBJECTS,{'a01'})


def corrected():
    old = 'A função F(t) representa a taxa de falha acumulada dos equipamentos ao longo do tempo.'
    u = item(old)
    u.update(tipo='definicao', afirmacao='F(t) representa a probabilidade acumulada de falha até t.',
             condicoes='Tempo até falha de uma população não reparável.',
             alvo_qa='Distinguir probabilidade acumulada de falha e taxa de falha.')
    u['redacao'].update(ajuste='tecnico', afirmacao_original=old,
                        condicoes_originais='', base='referencia_tecnica',
                        motivo='A fonte chamou uma probabilidade acumulada de taxa.',
                        referencias=['nist_sobrevivencia'], suporte_citacao=False)
    return u


def confirmation(u, decision='refinar'):
    return {'uid':u['uid'],'decisao':decision,'motivo':'Confere com a definição do guia técnico.',
            'base':'referencia_tecnica','referencias':['nist_sobrevivencia'],'suporte_citacao':False,
            'carater_avaliativo':u['carater_avaliativo'],'alvo_qa':u['alvo_qa'],
            'unidade':{k:copy.deepcopy(u[k]) for k in R.FIELDS}}


class RedacaoTests(unittest.TestCase):
    def test_extracao_exige_alvo_no_contrato(self):
        u=item();u.pop('alvo_qa')
        with self.assertRaises(ValueError):X._validate({'unidades':[u]})

    def test_cronologia_nao_e_aceita_mesmo_com_valor_alto(self):
        u=item(HISTORY);u['carater_avaliativo']='memoria_do_caso';u['alvo_qa']='Recordar quantas viagens foram realizadas.'
        kept,dropped=extract(u)
        self.assertEqual(kept,[])
        self.assertIn('sem_conhecimento_profissional',dropped[0]['descartada_por'])

    def test_sem_alvo_nao_passa(self):
        u=item();u['alvo_qa']=''
        kept,dropped=extract(u)
        self.assertEqual(kept,[])
        self.assertIn('sem_alvo_qa',dropped[0]['descartada_por'])

    def test_licao_com_relacao_tecnica_e_preservada(self):
        kept,dropped=extract(item())
        self.assertEqual(dropped,[])
        self.assertEqual(kept[0]['alvo_qa'],item()['alvo_qa'])
        self.assertEqual(kept[0]['carater_avaliativo'],'conhecimento_profissional')

    def test_revisor_nao_pode_reclassificar_silenciosamente(self):
        kept,_=extract(item());u=kept[0]
        row={'uid':u['uid'],'decisao':'aprovar','motivo':'adequada','base':'fonte_original',
             'referencias':[],'suporte_citacao':True,'carater_avaliativo':'conhecimento_profissional',
             'alvo_qa':'Um alvo diferente.', 'unidade':{k:u[k] for k in R.FIELDS}}
        with self.assertRaises(ValueError):
            R.validator([u],{'d':{'texto':LESSON}},SUBJECTS)({'pareceres':[row]})

    def test_historia_redacao_obrigatoria(self):
        u=item();u.pop('redacao')
        with self.assertRaisesRegex(ValueError,'Histórico'):extract(u)

    def test_corrige_conceito_e_preserva_citacao_errada(self):
        u=corrected();before=copy.deepcopy(u)
        kept,dropped=extract(u)
        self.assertEqual(dropped,[])
        result=kept[0]
        self.assertEqual(result['afirmacao'],u['afirmacao'])
        self.assertEqual(result['citacao'],u['citacao'])
        self.assertTrue(result['citacao_verificada'])
        self.assertFalse(result['redacao']['suporte_citacao'])
        self.assertEqual(result['redacao']['afirmacao_original'],u['citacao'])
        self.assertIn('nist.gov',result['redacao']['referencias_detalhadas'][0]['url'])
        self.assertEqual(u,before)

    def test_adaptacao_editorial_preserva_origem(self):
        u=item();u['afirmacao']='No caso investigado, falhas na preparação para a função prejudicaram decisões sobre os sistemas.'
        u['redacao'].update(ajuste='editorial',motivo='Explicitar a relação técnica já descrita na fonte.')
        kept,dropped=extract(u)
        self.assertEqual(dropped,[])
        self.assertEqual(kept[0]['redacao']['afirmacao_original'],LESSON)
        self.assertEqual(kept[0]['redacao']['base'],'fonte_original')

    def test_ajuste_nao_pode_ser_ocultado_como_nenhum(self):
        u=item();u['afirmacao']='Uma redação diferente.'
        with self.assertRaisesRegex(ValueError,'Mudança não declarada'):extract(u)

    def test_correcao_precisa_de_motivo_e_base(self):
        for field,value in (('motivo',''),('base','inventada'),('referencias',[]),
                            ('referencias',['referencia_inventada']),('suporte_citacao','false')):
            with self.subTest(field=field,value=value):
                u=corrected();u['redacao'][field]=value
                with self.assertRaises(ValueError):extract(u)

    def test_nao_atribui_correcao_sem_suporte_a_fonte(self):
        u=corrected();u['redacao']['base']='fonte_original'
        with self.assertRaisesRegex(ValueError,'sem base'):extract(u)

    def test_correcao_nao_permite_reescrever_citacao(self):
        u=corrected();source=u['citacao']
        u['citacao']='A função F(t) representa a probabilidade acumulada de falha dos equipamentos ao longo do tempo.'
        kept,dropped=extract(u,source)
        self.assertEqual(kept,[])
        self.assertIn('citacao_nao_encontrada',dropped[0]['descartada_por'])

    def test_normalizacao_do_modelo_e_explicitamente_identificada(self):
        u=corrected();u['redacao'].update(base='normalizacao_tecnica_modelo',referencias=[])
        kept,_=extract(u)
        self.assertEqual(kept[0]['redacao']['base'],'normalizacao_tecnica_modelo')

    def test_redator_nao_inventa_numero_ausente(self):
        u=corrected();u['afirmacao']='A probabilidade de falha é 57%.'
        with self.assertRaisesRegex(ValueError,'Número novo'):extract(u)

    def test_numero_explicitado_no_guia_tecnico_permitido(self):
        u=corrected();u['afirmacao']='A confiabilidade é R(t)=1-F(t).'
        kept,_=extract(u)
        self.assertEqual(kept[0]['afirmacao'],u['afirmacao'])

    def test_redator_nao_inventa_obrigacao_normativa(self):
        u=corrected();u.update(tipo='requisito_normativo',condicoes='Brasil, ANP.')
        with self.assertRaisesRegex(ValueError,'obrigação normativa'):extract(u)

    def test_revisor_nao_confirma_correcao_silenciosamente(self):
        kept,_=extract(corrected());u=kept[0]
        row=confirmation(u,'aprovar');row.update(base='fonte_original',referencias=[],suporte_citacao=True)
        with self.assertRaisesRegex(ValueError,'confirmação explícita'):
            R.validator([u],{'d':{'texto':u['citacao']}},SUBJECTS)({'pareceres':[row]})

    def test_fluxo_redator_revisor_documento_preserva_duas_intervencoes(self):
        raw,_=extract(corrected());u=raw[0]
        class LLM:
            def json(self,system,user,**kwargs):
                payload=json.loads(user)
                self.assertions=payload
                data={'pareceres':[confirmation(v) for v in payload['unidades']]}
                kwargs['validate'](data)
                return data
        llm=LLM()
        kept,*_=R.review_units(llm,SUB,raw,{'d':{'chunk_id':'d','texto':u['citacao']}},SUBJECTS)
        self.assertEqual(llm.assertions['unidades'][0]['redacao'],u['redacao'])
        self.assertEqual(kept[0]['revisao']['redacao_original'],u['redacao'])
        canonical=C._from_members(kept,'s1',1,'unica')
        self.assertEqual(canonical['fontes'][0]['redacao'],u['redacao'])
        md=F.render_ficha(SUB,SUBJECTS[0],[canonical],{})
        self.assertIn('Antes da redação: '+u['citacao'],md)
        self.assertIn('Antes da revisão: '+u['afirmacao'],md)
        self.assertIn('não sustenta a correção',md)
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            write_jsonl(root/'subtopicos'/'s1'/'unidades_consolidadas.jsonl',[canonical])
            rows=[{'topico':'KPI','subtopico':'Confiabilidade','sub_dir':'s1','assunto_id':'a01',
                   'assunto':'confiabilidade','status':'contexto_parcial','unidades':1,'pendentes':0,'generico':False}]
            F.write_topic_documents(root,rows)
            index=json.loads((root/'documentos_topicos.json').read_text(encoding='utf-8'))
            doc=(root/index[0]['arquivo']).read_text(encoding='utf-8')
            self.assertIn('Antes da redação: '+u['citacao'],doc)
            self.assertIn('Antes da revisão: '+u['afirmacao'],doc)

    def test_correcao_duvidosa_fica_pendente_com_historico(self):
        raw,_=extract(corrected());u=raw[0]
        class LLM:
            def json(self,*args,**kwargs):
                row=confirmation(u);row.update(decisao='pendente',unidade=None,
                                               motivo='A hipótese do modelo de confiabilidade não está clara.')
                return {'pareceres':[row]}
        kept,rejected,pending,*_=R.review_units(LLM(),SUB,raw,{'d':{'texto':u['citacao']}},SUBJECTS)
        self.assertEqual(kept+rejected,[])
        self.assertEqual(pending[0]['redacao'],u['redacao'])
        self.assertEqual(pending[0]['revisao']['redacao_original'],u['redacao'])

    def test_adaptacao_editorial_pode_ser_aprovada(self):
        proposed=item();proposed['afirmacao']='No caso investigado, preparação inadequada prejudicou decisões sobre os sistemas.'
        proposed['redacao'].update(ajuste='editorial',motivo='Explicitar a lição relatada.')
        raw,_=extract(proposed);u=raw[0]
        row=confirmation(u,'aprovar');row.update(base='fonte_original',referencias=[],suporte_citacao=True)
        self.assertTrue(R.validator(raw,{'d':{'texto':u['citacao']}},SUBJECTS)({'pareceres':[row]}))


if __name__=='__main__':unittest.main()
