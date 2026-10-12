"""Notebook de operação do mesmo motor QA v6 utilizado pelo CLI."""
import json
from pathlib import Path


def markdown(source):
    return {'cell_type':'markdown','metadata':{},'source':source.splitlines(keepends=True)}


def code(source):
    return {'cell_type':'code','metadata':{},'execution_count':None,'outputs':[],
            'source':source.splitlines(keepends=True)}


cells=[
markdown('''# PetroQuest QA v6 — documentos técnicos por faceta, 10 × 1.000 palavras

Petrolês + ANP + HSE + BSEE + REGIS → recuperação bilíngue → **contextos que podem combinar vários corpora, sem funções fixas por coleção** → 10 trechos maiores por faceta → composição de documento técnico por LLM (sem auditoria factual prévia bloqueante) → alternância de subtópicos, facetas, documentos e alvos → Gerador → Scorer/Refiner/Judge → dificuldade independente → avaliação de redundância → journal.

Próxima coleta: **100 novas QA aprovadas por tópico**, GPT‑5.4, effort `medium`. Somente pergunta/resposta. Os filtros de similaridade/redundância e a parada científica permanecem **desligados**; suas decisões são registradas. Scorer/Refiner/Judge continuam avaliando as QA. O documento composto é experimental e não certificado. A meta, orçamento e falhas técnicas podem encerrar a execução.
'''),
code('''from pathlib import Path
from dataclasses import replace
from collections import Counter
import sys, json, subprocess

cwd=Path.cwd().resolve()
ROOT=next(p for p in [cwd,*cwd.parents] if (p/'pipeline/fase_4/run_qa.py').is_file())
sys.path.insert(0,str(ROOT))
from pipeline.fase_4.config import QAConfig
from pipeline.fase_4.engine import execute
from pipeline.fase_4.domain import TOPICOS
from pipeline.fase_4.storage import read_jsonl
print(ROOT)
print('Tópicos:',len(TOPICOS))
'''),
markdown('''## Configuração

O manifesto une as quatro novas coleções aos dois TXT reais do Petrolês. Instale com `python pipeline/domain_corpora/install_corpora.py --petroles-dir /pasta/real` antes desta etapa. O README de `pipeline/domain_corpora` contém os comandos de instalação e teste. Endpoint/chave/versão Azure ficam no `.env`, fora do Git. Use uma saída nova: o corpus mudou e as curvas anteriores devem ser preservadas.
'''),
code('''cfg=QAConfig()
cfg.output=ROOT/'pipeline/fase_4/saida_qa_v6_documentos_10x1000_medium'
cfg.topics=None  # Todos os tópicos; pode selecionar uma lista para piloto
cfg.corpus_manifest=ROOT/'dataset/domain_corpora/manifest.json'
cfg.corpus_dir=None  # Petrolês já está no manifesto
# cfg.corpus_dir=Path('/caminho/real/do/PetrolesHibrido')
# Ou os dois arquivos, evitando a descoberta automática:
# cfg.corpus_dir=None
# cfg.corpus_txt=[Path('/caminho/arquivo1.txt'),Path('/caminho/arquivo2.txt')]
cfg.deployment=cfg.preparation_deployment=cfg.judge_deployment='gpt-5-4-petrobras'
cfg.effort='medium'
cfg.embedding_model='text-embedding-3-large'
cfg.embedding_deployment='embedding-3-large-global'
cfg.context_mode='composed'
cfg.chunk_words=1000
cfg.chunks_per_facet=10
cfg.composition_max_tokens=32000
cfg.limit_per_topic=100
cfg.batch_size=2
cfg.max_calls=20000  # Teto operacional de pedidos lógicos, não sinal de saturação
cfg.enable_cosine_filter=cfg.filter_redundancy=cfg.enable_saturation_stop=False
cfg.resume=False  # True apenas para continuar esta mesma execução v6
cfg.validate()
print(json.dumps(cfg.serializable(),ensure_ascii=False,indent=2))
'''),
markdown('''## Conferir a instalação dos cinco corpora — sem Azure

Confere hashes e proveniência. Um manifesto de amostra é bloqueado por padrão; a rodada principal deve usar a instalação sem `--max-documents-per-source`.
'''),
code('''subprocess.run([sys.executable,str(ROOT/'pipeline/domain_corpora/verify_corpora.py'),
                '--manifest',str(cfg.corpus_manifest)],cwd=ROOT,check=True)
'''),
markdown('''## Exemplos externos e humanos

ARC Easy/Challenge, Pirá, SQuAD 2.0, HotpotQA e BoolQ são normalizados para QA e amostrados a cada lote. No ARC, opções são removidas e o texto da opção correta vira resposta; comandos dependentes de alternativas são excluídos. Exemplos fornecem formato, nunca suporte factual para FPSO.

Seeds humanas mantêm proveniência; a preparação da geração remove redundância confirmada entre seeds. Novas QA de outros tópicos só entram nos exemplos se aprovadas e consideradas novidade útil.
'''),
code('''if not cfg.external_examples.exists():
    subprocess.run([sys.executable,str(ROOT/'pipeline/qa_references/download_qa_examples.py'),
                    '--max-per-dataset','1000'],cwd=ROOT,check=True)
else:
    print('Exemplos disponíveis:',cfg.external_examples)
'''),
markdown('''## Revisar os prompts antes de gastar chamadas

A rubrica de dificuldade foi recuperada do notebook antigo do backup e adaptada para QA. O avaliador recebe pergunta/resposta e tópico, **sem a dificuldade solicitada**. Dimensões: integração de conhecimento, cadeia de raciocínio, demanda cognitiva e especificidade técnica. Não há dimensão de distratores.
'''),
code('''for flag in ('--print-prompt','--print-composition-prompt','--print-judge-prompt','--print-difficulty-prompt'):
    print()
    print(flag)
    subprocess.run([sys.executable,str(ROOT/'pipeline/fase_4/run_qa.py'),flag],cwd=ROOT,check=True)
'''),
markdown('''## Recuperar trechos e compor documentos técnicos — usa Azure

Esta célula recupera até **10 trechos de cerca de 1.000 palavras por faceta** e compõe um documento técnico pelo modelo antes de gerar perguntas. O prompt pede corretude técnica, preservação de condições e registro de dúvidas. Não há auditoria factual prévia bloqueante no modo composed. A validação automática confere estrutura, IDs e alvos.

O compositor organiza conceitos, mecanismos, critérios de decisão e limitações em Markdown; os trechos originais também chegam ao gerador e ao Judge. Páginas consecutivas do mesmo documento podem compor um trecho, com páginas e offsets preservados. A quantidade pode ser menor em fontes curtas e fica registrada. Os embeddings usam exclusivamente Azure `embedding-3-large-global`, em 3.072 dimensões, com cobertura integral do texto. Vetores persistem em SQLite e os codebooks ficam fixos por execução.

O texto completo, os alvos, as fontes usadas, as dúvidas e todas as respostas do compositor ficam salvos. Uma falha de formato é corrigida uma vez e isolada; falhas consecutivas interrompem com diagnóstico. Use a saída QA v6 nova, sem retomar preparação de versões anteriores.
'''),
code('''prepared=execute(replace(cfg,prepare_only=True))
print('Estado:',prepared.meta['status'])
print('Chamadas por papel:',prepared.state['calls_by_role'])
compositions=read_jsonl(cfg.output/'composicoes_contexto.jsonl')
print('Composições:',dict(Counter(r['status'] for r in compositions)))
print(json.dumps(json.loads((cfg.output/'cobertura_dominio.json').read_text(encoding='utf-8')),
                 ensure_ascii=False,indent=2))
'''),
code('''# Ler um documento composto e sua proveniência.
if compositions:
    doc_id=compositions[0]['doc_id']
    document=cfg.output/'dominio/documentos'/f'{doc_id}.md'
    if document.exists():print(document.read_text(encoding='utf-8'))
    print(json.dumps(compositions[0],ensure_ascii=False,indent=2))
'''),
markdown('''## Gerar QA — usa Azure

O agendador alterna subtópicos, facetas/fontes e alvos de conhecimento, considerando cobertura e rendimento de novidade. A dificuldade solicitada é balanceada **dentro de cada subtópico**. A dificuldade inferida é registrada separadamente, sem forçar concordância com a solicitada.

Scorer e Judge podem acionar até dois refinamentos no total por candidata. O Judge recebe documento composto, trechos originais e metadados, sem presumir auditoria prévia. A dificuldade é inferida independentemente. Cosine ≥0,85 recupera vizinhos para avaliação de pares; nesta coleta não descarta candidatos.
'''),
code('''if prepared.meta['status']!='prepared':
    raise RuntimeError('Preparação incompleta; reveja orçamento/checkpoint antes de gerar')
cfg.resume=True
run=execute(cfg)
print('Estado:',run.meta['status'])
print('Aceitas:',len(run.accepted))
print('Novidade útil estimada:',sum(bool(r.get('useful_novel')) for r in run.accepted))
print('Chamadas:',run.state['calls_by_role'])
print('Tokens:',run.state.get('usage_by_role',{}))
'''),
markdown('''## Observar métricas e dificuldade

A entropia é diagnóstica. A parada requer cobertura mínima, duas janelas completas sem novidade suficiente e sem novos alvos, seguidas de recuperação com outras fontes. Falhas técnicas não entram nas janelas. Bloqueio de qualidade é separado de saturação. Com apenas 100 por tópico, alguns subtópicos poderão não acumular amostras suficientes para concluir saturação.
'''),
code('''import pandas as pd
import matplotlib.pyplot as plt
rounds=pd.DataFrame(read_jsonl(cfg.output/'metricas_por_rodada.jsonl'))
candidates=pd.DataFrame(read_jsonl(cfg.output/'candidatas_metricas.jsonl'))
if not rounds.empty:
    fig,axes=plt.subplots(1,3,figsize=(16,4))
    for topic,group in rounds.groupby('topic',sort=False):
        axes[0].plot(group['round'],group['entropy'].map(lambda x:x['value']),label=topic)
        axes[1].plot(group['round'],group['mean_cosine'])
        valid=group[group['generated']>0]
        axes[2].plot(valid['round'],valid['useful_novel_this_round']/valid['generated'])
    for ax,title in zip(axes,('Entropia das aprovadas','Cosine máximo médio','Rendimento de novidade útil')):
        ax.set(title=title,xlabel='Rodada')
    axes[0].legend(fontsize=6)
    fig.tight_layout()
    plt.show()
if not candidates.empty:
    approved=candidates[candidates['accepted'].eq(True)]
    display(pd.crosstab(approved['requested_difficulty'],approved['difficulty']))
    display(approved.groupby(['topic','subtopic','difficulty']).size().rename('quantidade').to_frame())
    display(candidates.reindex(columns=['topic','subtopic','question','answer','accepted','useful_novel',
                                       'requested_difficulty','difficulty','rejection_reason']).head(30))
'''),
markdown('''## Reavaliar os sinais e trazer pelo GitHub

`replay_stopping.py` reconstrói os sinais em diferentes janelas e coberturas, registrando novidades observadas depois deles. Isso é replay da trajetória observada, não uma nova geração contrafactual.

`questoes_qa.jsonl`, `candidatas_metricas.jsonl`, `composicoes_contexto.jsonl`, documentos e chamadas permitem curadoria junto com as fontes. Os comandos de execução e Git de transporte estão em `EXECUCAO_QA_V6.md`. Mantenha corpus, `.env` e caches binários fora do Git.
'''),
code('''subprocess.run([sys.executable,str(ROOT/'pipeline/fase_4/replay_stopping.py'),
                '--output',str(cfg.output)],cwd=ROOT,check=True)
print('Resultados:',cfg.output)
'''),
]


def main():
    for number,cell in enumerate(cells):cell['id']=f'qa-v6-{number:02d}'
    notebook={'cells':cells,'metadata':{'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},
                'language_info':{'name':'python'}},'nbformat':4,'nbformat_minor':5}
    Path(__file__).with_name('petroquest_fase4_qa.ipynb').write_text(
        json.dumps(notebook,ensure_ascii=False,indent=1)+'\n',encoding='utf-8')


if __name__=='__main__':main()
