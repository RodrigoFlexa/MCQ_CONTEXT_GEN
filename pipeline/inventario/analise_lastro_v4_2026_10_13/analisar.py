"""Revisão numérica e exemplos do Lastro v4 já recebido. Sem API ou alteração do inventário."""
import collections
import csv
import json
import statistics
from pathlib import Path

from pipeline.inventario.textutil import quote_supported

OUT=Path(__file__).resolve().parent
RUN=OUT.parent/'saida_sistemas_de_lastro_v4_notas'


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def rows(path):
    return [json.loads(line) for line in path.read_text(encoding='utf-8').splitlines() if line.strip()]


def main():
    notes=rows(RUN/'notas_aprovadas.jsonl')
    combos=rows(RUN/'combinacoes.jsonl')
    questions=rows(RUN/'teste_dificeis/questoes.jsonl')
    summary=read(RUN/'resumo.json')
    facts,discarded,chunks=[],[],{}
    programs=[]
    for d in sorted((RUN/'subtopicos').iterdir()):
        facts+=rows(d/'fatos.jsonl')
        discarded+=rows(d/'fatos_descartados.jsonl')
        programs.append(read(d/'assuntos.json'))
        for selection in read(d/'selecao.json')['assuntos'].values():
            chunks.update({c['chunk_id']:c for c in selection['trechos']})
    numeric_notes=[n for n in notes if any('numeros_sem_fonte' in a for a in n['alertas'])]
    local_facts={(f['sub_key'],f['fid']):f for f in facts}
    grouped=collections.defaultdict(list)
    for f in facts:
        grouped[f['fid']].append(f)
    trace=[]
    for n in notes:
        different=[]
        for fid,source in n['fontes'].items():
            original=local_facts.get((n['sub_key'],fid))
            if source['tipo']=='fato' and original and source['afirmacao']!=original['afirmacao']:
                different.append({'fid':fid,'na_nota':source,'na_extracao_do_subtopico':original})
        if different:
            trace.append({'nid':n['nid'],'titulo':n['titulo'],'subtopico':n['subtopico'],'divergencias':different})
    by_topic=[]
    for sk in sorted({n['sub_key'] for n in notes}):
        mine=[n for n in notes if n['sub_key']==sk]
        by_topic.append({'subtopico':mine[0]['subtopico'],'notas':len(mine),
                         'palavras_notas_unicas':sum(n['metricas']['palavras'] for n in mine)})
    m={'status_execucao':summary['status'],'tempo_min':round(summary['tempo_total_s']/60,1),
       'notas_aprovadas':len(notes),'subtopicos':len(by_topic),
       'assuntos_com_contexto':summary['assuntos']['com_contexto'],
       'palavras_notas_unicas':sum(n['metricas']['palavras'] for n in notes),
       'palavras_somadas_por_assunto_no_resumo':summary['palavras_aprovadas'],
       'palavras_nota':{'min':min(n['metricas']['palavras'] for n in notes),
                       'mediana':statistics.median(n['metricas']['palavras'] for n in notes),
                       'max':max(n['metricas']['palavras'] for n in notes)},
       'fatos_retidos':len(facts),'fatos_descartados':len(discarded),
       'citacoes_retidas_rechecadas':sum(quote_supported(f['citacao'],chunks[f['fonte']['chunk_id']]['texto']) for f in facts),
       'motivos_descarte':dict(collections.Counter(r for f in discarded for r in f['descartado_por'])),
       'decisoes_revisor_nas_notas_aprovadas':dict(collections.Counter(n['revisao']['decisao'] for n in notes)),
       'problemas_apontados_pelo_revisor':dict(collections.Counter(p.get('tipo') for n in notes for p in n['revisao']['problemas'])),
       'distribuicao_notas_do_revisor':{k:dict(collections.Counter(n['avaliacao'][k] for n in notes)) for k in notes[0]['avaliacao']},
       'notas_com_alerta_numerico_residual':[n['nid'] for n in numeric_notes],
       'participacao_colecoes_em_notas':dict(collections.Counter(c for n in notes for c in n['colecoes'])),
       'mediana_referencias_por_nota':statistics.median(len(n['fontes']) for n in notes),
       'notas_sem_alvo_dificil':sum(not any(a['nivel']=='dificil' for a in n['alvos']) for n in notes),
       'combinacoes':len(combos),'combinacoes_multi_assunto':sum(c['multi_assunto'] for c in combos),
       'questoes_teste':len(questions),'teste_dificuldade':read(RUN/'teste_dificeis/resumo.json'),
       'ocorrencias':rows(RUN/'ocorrencias.jsonl'),'subtopicos_resumo':by_topic}
    m.update(fids_repetidos_entre_subtopicos=sum(len(x)>1 for x in grouped.values()),
             notas_com_rastreio_divergente=len(trace),
             referencias_com_afirmacao_diferente_da_extracao_local=sum(len(x['divergencias']) for x in trace))
    (OUT/'rastreio_para_curadoria.json').write_text(json.dumps(trace,ensure_ascii=False,indent=2),encoding='utf-8')
    (OUT/'resumo_numerico.json').write_text(json.dumps(m,ensure_ascii=False,indent=2),encoding='utf-8')
    (OUT/'alertas_numericos.json').write_text(json.dumps(numeric_notes,ensure_ascii=False,indent=2),encoding='utf-8')
    selected_ids=['62e43c1988:a25:k3','01c1c3db6e:a11:k5','567fdce5c3:a02:k5']
    examples=[n for nid in selected_ids for n in notes if n['nid']==nid]
    docs=['# Exemplos reais do Lastro v4','',
          'Notas produzidas no servidor antes dos ajustes de autonomia dos prompts. Textos preservados, sem reescrita nesta análise.','']
    for n in examples:
        docs.extend([f"## {n['titulo']}",'',f"ID: `{n['nid']}`; subtópico: {n['subtopico']}; coleções: {', '.join(n['colecoes'])}",'',n['resumo'],''])
        for s in n['secoes']:
            docs.extend([f"### {s['titulo']}",'',s['texto'],'',
                         'Base: conhecimento geral marcado.' if s['conhecimento_geral'] else 'Fatos/trechos: '+', '.join(s['fatos']), ''])
        docs.extend(['### Alvos avaliáveis','']+[f"- {a['nivel']}: {a['descricao']}" for a in n['alvos']]+[''])
    docs.extend(['## Perguntas reais do experimento',''])
    for qid in ['q002','q003','q021']:
        q=next(q for q in questions if q['id']==qid)
        docs.extend([f"### {qid} · pedido {q['tipo']} · medido {q['avaliacao']['difficulty']}",'',
                     '**Pergunta:** '+q['pergunta'],'','**Resposta:** '+q['resposta'],''])
        if qid=='q003':
            docs.extend(['**Observação da análise:** depende do episódio do tanque 6C sem fornecer suas condições. O rótulo de dificuldade não detectou esse problema de autonomia. Não usar a QA como está.',''])
    (OUT/'exemplos.md').write_text('\n'.join(docs),encoding='utf-8')
    text=['# Lastro v4 — revisão do código e dos resultados','',
          'Resultados recebidos no commit `aeecfa7`, analisados em 13/10/2026. A conversa anexada é contexto; os números abaixo foram recontados nos arquivos.','',
          '## Resultado','',
          f"Execução: {m['status_execucao']}; {m['tempo_min']} minutos; {len(notes)} notas aprovadas em {len(by_topic)} subtópicos e 68 assuntos com contexto.",
          f"Fatos: {len(facts)} retidos, {len(discarded)} descartados; {m['citacoes_retidas_rechecadas']} citações retidas correspondem ao trecho de origem segundo o verificador.",
          f"Notas: mediana {m['palavras_nota']['mediana']} palavras; {m['palavras_nota']['min']} a {m['palavras_nota']['max']} palavras. {m['palavras_notas_unicas']} palavras nas notas únicas; o resumo por assunto soma {m['palavras_somadas_por_assunto_no_resumo']} porque uma nota pode atender a mais de um assunto.",
          'O inventário de Lastro já pode contar como o primeiro tópico. Sua utilização em QA requer enunciados autossuficientes e preservação das condições das fontes.','',
          '| Subtópico | Notas aprovadas únicas | Palavras nas notas |','|---|---:|---:|']
    for r in by_topic:
        text.append(f"| {r['subtopico']} | {r['notas']} | {r['palavras_notas_unicas']} |")
    text.extend(['','## O que mudou no código e funcionou na execução','',
                 '- Fatos são evidência; o produto final é uma nota por conceito, com mecanismos, variáveis, problemas, decisões e alvos por dificuldade.',
                 '- A revisão recebe a nota, os fatos e até oito trechos completos; pode corrigir o texto inteiro. Referências são registradas por seção, não uma verificação automática de cada frase.',
                 '- O filtro de conteúdo da Azure ocorreu de fato em uma nota do redator. O item foi registrado e a execução continuou.',
                 '- A seleção bilíngue e as cotas por coleção mudaram o material: todas as cinco coleções aparecem nas notas aprovadas. Isso não prova isoladamente qual mudança causou cada ganho.',
                 '- Retentativas informam o erro de validação; truncamento aumenta o orçamento de resposta; falhas de itens têm diagnóstico e não encerram automaticamente todos os assuntos.','',
                 '## Pontos que ainda exigem cuidado','',
                 '1. Autonomia: q003 pergunta por que os slops e o tanque 6C não esvaziaram, sem trazer o caso ao respondente. O teste mediu dificuldade, não corretude nem autonomia. Os prompts novos foram ajustados para avaliar relações técnicas e fornecer condições suficientes.',
                 '2. Avaliação pelo mesmo modelo: 256 das 311 notas finais receberam corrigir, 55 aprovar. O revisor apontou 577 problemas de suporte nos rascunhos; isso é uma contagem de apontamentos, não prova de 577 afirmações removidas nem de corretude total da versão final. As avaliações se concentram em 5 e não servem como ranking externo de qualidade.',
                 '3. Alertas numéricos: quatro notas finais têm cinco alertas. Em duas delas, 10 e 100 estão escritos como dez e cem no trecho Petrolês: o alerta é um falso positivo. Os demais valores exigem conferir seus próprios trechos; não classificar todo alerta como alucinação. A rotina também ignora inteiros menores que 10 e não valida automaticamente unidades, versões de normas ou condições.',
                 '4. Fontes: várias referências podem vir do mesmo documento. A mediana de nove referências por nota não equivale a nove documentos independentes.',
                 '5. Cobertura: 68 assuntos têm notas utilizáveis, mas um conceito foi filtrado. Na próxima saída, processamento_completo distingue material presente de processamento sem itens pulados. Lastro continua preservado.',
                 '6. Deduplicação: compara título e resumo por cosseno; conteúdo complementar, condições e contradições ainda dependem de revisão. Não é auditoria factual independente.','',
                 '7. Defeito de isolamento de evidências encontrado no código: stage_notas construía um mapa global por fid, mas o identificador não inclui o subtópico. Há 157 IDs repetidos entre extrações de subtópicos diferentes. Em 81 notas, 188 referências guardadas têm afirmação diferente da extração local. Como o redator e o revisor também receberam trechos e os registros preservam a evidência efetivamente usada, isso não prova erro técnico em todas essas notas; exige conferência das ligações conceito/fato. O código foi corrigido para consultar um mapa por subtópico, com teste de regressão. A lista de notas está em rastreio_para_curadoria.json. Não foram reescritos os resultados de Lastro.', '',
                 '## Experimento de dificuldade','',
                 '| Pedido | Resultado medido |','|---|---|',
                 '| Fácil (4) | 2 fáceis, 2 médias |','| Média (4) | 1 média, 3 difíceis |',
                 '| Difícil A (8) | 6 difíceis, 2 médias |','| Difícil B (8) | 7 difíceis, 1 média |','',
                 'A amostra tem só 24 questões. Sugere revisar a calibração das fáceis e médias, mas não estabelece desempenho geral. O nível pedido deve ser preservado como metadado; a dificuldade inferida deve passar pela validação da geração final.',
                 '', '## Próxima rodada','',
                 'Lastro é o tópico já construído. Os quatro escolhidos são Produção e Processo, Operações submarinas, Utilidades e Segurança Operacional: 23 subtópicos no novo script run_mais_4_topicos_azure.sh. Uma execução fará uma varredura lexical para o conjunto. Os resultados de Produção v3 continuam sendo uma execução antiga parcial, e não o primeiro tópico concluído desta rodada v4.',
                 'Os ajustes novos de prompt ainda precisam de avaliação com a Azure. A análise atual não faz chamadas ao modelo nem altera os arquivos gerados.',
                 '', '[Exemplos completos de notas e QA](exemplos.md). Comandos: [RODADA_5_TOPICOS.md](../RODADA_5_TOPICOS.md).',''])
    (OUT/'relatorio.md').write_text('\n'.join(text),encoding='utf-8')
    print(json.dumps({k:m[k] for k in ['status_execucao','tempo_min','notas_aprovadas','subtopicos','fatos_retidos','fatos_descartados','citacoes_retidas_rechecadas','combinacoes','questoes_teste']},ensure_ascii=False))


if __name__=='__main__':
    main()
