"""Amplia a curadoria sem modificar a seleção histórica: toda MCQ sem reprovação explícita."""
import copy
import csv
import re
from collections import Counter
from pathlib import Path

from pipeline.inventario.textutil import atomic_json
from .core import HERE, ROOT, ler_linhas, sha
from .extracao import jsonl

CONJUNTO = 'mcq_revisada_nao_reprovada'
ROTULO = 'MCQs revisadas sem reprovação explícita'
ENTRADA = HERE/'entrada/revisadas_v3/nao_reprovadas_mcq.jsonl'
ANTERIOR = ROOT/'pipeline/qa_research/relatorios/especialista_qa_v2'
REPROVACAO = re.compile(r'\b(?:descartar|descartad[ao]s?|desaprovad[ao]s?|reprovad[ao]s?|não\s+aprovad[ao]s?)\b', re.I)


def reprovacao_explicita(comment):
    # A sentença pode revogar uma aprovação no início. Não presumir aceitação nesses casos.
    for match in REPROVACAO.finditer(comment):
        if not match.group().lower().startswith('não ') and re.search(r'\bnão\s+$', comment[:match.start()], re.I):
            continue
        return True
    return False


def faixa(row):
    status = row['revisao_humana']['status']
    return ('aprovacao_simples' if status == 'aprovada_sem_observacoes' else
            'aprovacao_com_observacoes' if status == 'aprovacao_com_observacoes_ou_ressalvas' else 'parecer_sem_aprovacao_explicita')


def preparar(saida=ENTRADA.parent):
    source = HERE/'entrada/revisadas/curadoria_todas.jsonl'
    rows = ler_linhas(source)
    decisions, selected = [], []
    for original in rows:
        r = copy.deepcopy(original)
        comment = r['revisao_humana']['parecer_original']
        rejected = reprovacao_explicita(comment) or r['revisao_humana']['status'] == 'descartada_ou_reprovada'
        r['conjunto_especialista'] = CONJUNTO
        r['politica_curadoria'] = 'nao_reprovadas_v3'
        r['faixa_parecer'] = faixa(r)
        r['nao_reprovada_humano'] = not rejected
        # Preserva as explicações de siglas que seguem o comentário no DOCX (questão 384).
        lines = r['texto_original'].splitlines()
        ix = next((i for i,t in enumerate(lines) if re.match(r'^(?:Comentário|Cimentário|Comenário|Comentpario|Comnetário)\s*:', t, re.I)), len(lines))
        tail = lines[ix+1:]
        definitions = bool(tail) and all(re.match(r'^[A-Z][A-Z0-9]{1,12}\s*=', t) for t in tail)
        r['notas_documento'] = '\n'.join(tail) if definitions else ''
        r['problemas_extracao_originais'] = list(r['problemas_extracao'])
        if definitions and set(r['problemas_extracao']) == {'paragrafo_nao_interpretado'}:
            r['problemas_extracao'] = []
            r['status_extracao'] = 'ok'
        r['selecionada_para_conversao'] = not rejected
        decisions.append(r)
        if not rejected:
            selected.append(r)
    summary = {'schema': 'curadoria-revisadas-v3', 'total': len(rows), 'candidatas': len(selected),
               'reprovadas_explicitas': len(rows)-len(selected),
               'por_faixa_parecer': dict(Counter(r['faixa_parecer'] for r in selected)),
               'pendentes_extracao': sum(r['status_extracao'] != 'ok' for r in selected),
               'origem_sha256': sha(rows), 'origem_docx_sha256': rows[0]['fonte']['docx_sha256'],
               'criterio': 'Inclui pareceres sem reprovação explícita, inclusive ressalvas e comentários sem aprovação. Ordens de descarte em qualquer parte do comentário prevalecem.',
               'descartes_fora_prefixo': [r['numero_original'] for r in decisions if not r['nao_reprovada_humano']
                    and r['revisao_humana']['status'] != 'descartada_ou_reprovada']}
    saida = Path(saida)
    jsonl(saida/'nao_reprovadas_mcq.jsonl', selected)
    jsonl(saida/'curadoria_todas.jsonl', decisions)
    atomic_json(saida/'extracao.json', summary)
    previous = [r for r in ler_linhas(ANTERIOR/'decisoes.jsonl') if r.get('conjunto_especialista') == 'mcq_revisada_aprovada']
    rejected = [r for r in previous if r['status'] == 'reprovada']
    diagnosis = {'candidatas_v2': len(previous), 'aprovadas_v2': sum(r['status'] == 'aprovada' for r in previous),
        'reprovadas_v2': len(rejected),
        'criterios_reprovacao_sobrepostos': dict(Counter(k for r in rejected for k,v in r['validacao']['criterios'].items() if not v)),
        'problemas_codigo_sobrepostos': dict(Counter(k for r in rejected for k in r.get('problemas_codigo', []))),
        'somente_codigo': sum(r['validacao']['valida'] is True for r in rejected),
        'comentario_enviado_ao_modelo_v2': False, 'tentativas_qualidade_por_mcq_v2': 1}
    atomic_json(saida/'diagnostico_v2.json', diagnosis)
    with (saida/'selecao.csv').open('w', encoding='utf-8-sig', newline='') as f:
        w = csv.writer(f)
        w.writerow(['numero', 'uid', 'selecionada', 'faixa_parecer', 'parecer_original', 'status_extracao'])
        w.writerows([r['numero_original'], r['uid'], r['selecionada_para_conversao'], r['faixa_parecer'],
                     r['revisao_humana']['parecer_original'], r['status_extracao']] for r in decisions)
    return summary


def ler_nao_reprovadas(path):
    rows = ler_linhas(path)
    for r in rows:
        if (r.get('politica_curadoria') != 'nao_reprovadas_v3' or r.get('conjunto_especialista') != CONJUNTO
                or r.get('nao_reprovada_humano') is not True or r.get('selecionada_para_conversao') is not True
                or reprovacao_explicita(r['revisao_humana']['parecer_original'])
                or r['revisao_humana']['status'] == 'descartada_ou_reprovada'):
            raise ValueError('Entrada v3 contém MCQ reprovada ou com curadoria inconsistente')
    return rows
