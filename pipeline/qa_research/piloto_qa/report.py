"""Tabelas do experimento em Markdown, HTML e CSV, sem notas inventadas."""
import csv
import html
from pathlib import Path
from pipeline.inventario.textutil import read_json
from pipeline.qa_research.v3.runtime import digest
from .documents import load,flatten

LABELS={'historico':'Histórico','novo_antigo':'Novo + contexto antigo','novo_refinado':'Novo + contexto refinado'}


def write(output,groups):
    output=Path(output);protocol=load(output/'protocolo.json')
    metrics=read_json(output/'metricas/metricas.json') or {}
    if metrics.get('protocolo',{}).get('dados_sha256')!=digest(groups):metrics={}
    evaluation=read_json(output/'avaliacao_comparavel/comparacao.json') or {}
    evaluated=read_json(output/'avaliacao_comparavel/config.json')
    if evaluated and evaluated.get('dados_sha256')!=digest([q for qs in groups.values() for q in qs]):evaluation={}
    sections=[]
    def fmt(value,digits=3):return '—' if value is None else f'{value:.{digits}f}'
    def add(title,headers,rows,note=''):
        sections.append((title,headers,rows,note))
    docs=[]
    for item in protocol['items']:
        for version in ('antigo','refinado'):
            d=load(output/'contextos'/version/item/'documento.json');bs=flatten(d)
            docs.append([item,version,len(d['capitulos']),len(bs),sum(len(b['texto'].split()) for b in bs)])
    add('Documentos usados',['Documento','Versão','Capítulos','Blocos','Palavras'],docs,
        'Dimensões descrevem o contexto; maior comprimento não demonstra melhor qualidade. Os ajustes estão nos arquivos revisao.json.')
    volume=[]
    for group,qs in groups.items():
        reports=[read_json(output/'geracao'/group/item/'resumo.json') for item in protocol['items']]
        reports=[r for r in reports if r]
        candidates=sum(r['candidatas'] for r in reports) if reports else None
        done=sum(r['status']=='concluido' for r in reports)
        volume.append([LABELS[group],len(qs),'—' if candidates is None else candidates,
            fmt(100*len(qs)/candidates if candidates else None,1),
            'Existente' if group=='historico' else f'{done}/{len(protocol["items"])}'])
    add('Produção e cobertura da execução',['Grupo','Questões disponíveis','Candidatas','Admissão (%)','Documentos encerrados'],volume,
        'Encerramento significa baixa produtividade observada nos contextos, não cobertura completa de todo o conhecimento. Histórico é amostra do banco anterior.')
    for scope,label in [('comparavel_mesmo_n_item_classe','Amostra equilibrada por documento e classe'),('integral','Conjuntos integrais')]:
        rows=[];semantic=[]
        for group,r in metrics.get(scope,{}).items():
            m=r['metricas'];value=lambda k:m[k]['media']
            rows.append([LABELS[group],r['n'],fmt(value('overlap_q_c')),fmt(value('max_rougeL_f1_sem_stop')),
                fmt(value('novel_2gram_pct'),1),fmt(value('novel_3gram_pct'),1),fmt(r['self_bleu4']),r['duplicatas_exatas']])
            s=r['semantica']
            semantic.append([LABELS[group],r['n'],fmt(s.get('cosseno_medio')),fmt(s.get('distancia_media_cosseno')),
                fmt(s.get('cosseno_vizinho')),fmt(s.get('vendi_cosseno')),fmt(s.get('vendi_centrado_sensibilidade'))])
        add('Métricas textuais — '+label,['Grupo','N','Overlap Q–C','Max ROUGE-L','Novel 2 (%)','Novel 3 (%)','Self-BLEU 4','Duplicatas exatas'],rows,
            'ROUGE sem stopwords; sem lematização. Novel e sobreposição não comprovam raciocínio ou sustentação. Denominadores válidos por métrica estão em metricas.json.')
        add('Diversidade semântica — '+label,['Grupo','N','Cosseno médio','Distância média','Cosseno vizinho','Vendi','Vendi centrado'],semantic,
            'E5 local; Vendi centrado é análise de sensibilidade separada. Comparar Vendi/Self-BLEU com o mesmo N. — significa indisponível, não zero.')
    types=['conceito','mecanismo','consequencia','diagnostico','decisao','procedimento']
    add('Distribuição de tipos',['Grupo']+types+['Compostas'],[[LABELS[g]]+[sum(q['tipo']==t for q in qs) for t in types]+
        [sum(q.get('composicao')=='composta' for q in qs)] for g,qs in groups.items()],
        'Composição é outra dimensão: não se soma como sétima classe. Sua classificação é automática, sem teste de ablação nesta versão.')
    for scope,title in [('gap_mesmo_n_item_classe','Desempenho — amostra equilibrada'),('gap_por_grupo','Desempenho — conjuntos integrais')]:
        rows=[]
        for r in evaluation.get(scope,[]):
            ci=r['ic95_gap'];ci='—' if ci is None else ' a '.join(fmt(v,2) for v in ci)
            rows.append([LABELS[r['grupo']],r['modelo'],r['total'],r['pares_validos'],r['sem_par'],
                fmt(r['acuracia_sem_contexto'],2),fmt(r['acuracia_com_contexto'],2),fmt(r['gap_pp'],2),ci])
        add(title,['Grupo','Respondente','Questões','Pares válidos','Sem par','Sem contexto (%)','Com contexto (%)','Gap (p.p.)','IC 95% gap'],rows,
            'Pares são a mesma pergunta com/sem contexto; grupos contêm perguntas diferentes. Parciais contam como erro na acurácia estrita; bloqueios/falhas não recebem zero. Avaliação pendente se tabela vazia.')
    support=evaluation.get('sustentacao_por_grupo',{})
    add('Sustentação dos gabaritos — auditoria adicional',['Grupo','Total','Processadas','Com decisão','Sustentados','Insuficientes','Contradições','Sustentação (%)'],
        [[LABELS[g],s['total'],s['processadas'],s['com_decisao'],s['por_status'].get('totalmente_sustentado',0),
          s['por_status'].get('suporte_insuficiente',0),s['por_status'].get('contradicao',0),fmt(s['taxa_sustentacao'],2)] for g,s in support.items()],
        'Auditoria adicional à admissão, automática e sujeita a erro. Inconclusivos/bloqueios ficam fora da taxa; estados completos estão em comparacao.json.')
    balanced=metrics.get('comparavel_mesmo_n_item_classe',{});delta=[]
    for reference in ('historico','novo_antigo'):
        a=balanced.get(reference);b=balanced.get('novo_refinado')
        if not a or not b:continue
        for name in ('overlap_q_c','max_rougeL_f1_sem_stop','novel_2gram_pct','novel_3gram_pct'):
            av=a['metricas'][name]['media'];bv=b['metricas'][name]['media']
            delta.append(['Refinado − '+LABELS[reference],name,a['n'],b['n'],fmt(None if av is None or bv is None else bv-av)])
    add('Diferenças descritivas — amostra equilibrada',['Comparação','Métrica','N referência','N refinado','Diferença'],delta,
        'Diferenças não isolam efeitos causais do contexto/gerador, nem representam automaticamente melhoria. Os grupos novos partem do mesmo banco inicial e crescem separadamente.')
    md=['# Comparação do benchmark','',
        'Histórico: questões do método anterior com seus contextos originais. Novo: fluxo contínuo aplicado às versões antiga e refinada dos documentos.',
        'Sem meta fixa de questões. As tabelas integrais e equilibradas preservam os tamanhos reais. Resultados ausentes são indicados por —.','']
    web=['<!doctype html><html lang="pt-BR"><meta charset="utf-8"><title>Comparação do benchmark</title>',
        '<style>body{font:15px system-ui;color:#172b4d;background:#f4f7fb;margin:32px}main{max-width:1500px;margin:auto}section{background:white;padding:24px;margin:24px 0;border-radius:12px;overflow:auto}h1,h2{color:#123b65}table{border-collapse:collapse;width:100%;font-variant-numeric:tabular-nums}th{background:#173f68;color:white;text-align:left}th,td{padding:11px 13px;border-bottom:1px solid #dae2ed;white-space:nowrap}tbody tr:nth-child(even){background:#f1f5fa}p{line-height:1.6;color:#47566a}@media print{body{margin:0;background:white}section{break-inside:avoid}}</style><main><h1>Comparação do benchmark</h1>',
        '<p>Histórico, novo gerador com contexto antigo e novo gerador com contexto refinado. Tamanhos reais e amostras equilibradas. Campos ausentes não recebem zero.</p>']
    directory=output/'tabelas';directory.mkdir(exist_ok=True)
    for i,(title,headers,rows,note) in enumerate(sections,1):
        md+=['## '+title,'','| '+' | '.join(headers)+' |','|'+'|'.join(['---']*len(headers))+'|']
        md+=['| '+' | '.join(str(v).replace('|','/').replace('\n',' ') for v in row)+' |' for row in rows]
        md+=['',note,'']
        web+=['<section><h2>'+html.escape(title)+'</h2><table><thead><tr>'+''.join('<th>'+html.escape(h)+'</th>' for h in headers)+'</tr></thead><tbody>']
        web+=['<tr>'+''.join('<td>'+html.escape(str(v))+'</td>' for v in row)+'</tr>' for row in rows]
        web+=['</tbody></table><p>'+html.escape(note)+'</p></section>']
        with (directory/f'{i:02}.csv').open('w',encoding='utf-8-sig',newline='') as stream:
            writer=csv.writer(stream);writer.writerow(headers);writer.writerows(rows)
    (output/'TABELAS.md').write_text('\n'.join(md),encoding='utf-8')
    (output/'TABELAS.html').write_text('\n'.join(web)+ '</main></html>',encoding='utf-8')
    return output/'TABELAS.md'
