"""Mantém o notebook como interface do mesmo motor usado pelo CLI."""
import json
from pathlib import Path


def markdown(source):
    return {"cell_type": "markdown", "metadata": {}, "source": source.splitlines(keepends=True)}


def code(source):
    return {"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [],
            "source": source.splitlines(keepends=True)}


cells = [
markdown("""# PetroQuest QA — fluxo completo da fase 4

**Domínio Petrolês → facetas → recuperação semântica/MMR → documento consolidado → geração QA → Scorer → Refiner → Judge → dataset.**

O alvo desta rodada é até 100 questões novas aceitas por tópico. Entropia, cosine, Jaccard e diversidade lexical são observados durante a geração. **Cosine e saturação não filtram nem encerram a rodada por padrão.** A aprovação técnica do Judge continua ativa. Não há distratores ou alternativas.

Execute este notebook no servidor com corpus, exemplos externos e configuração Azure. O notebook e a linha de comando chamam o mesmo motor. As saídas anteriores devem ser preservadas em sua própria pasta.
"""),
code("""from pathlib import Path
import sys
import json
from collections import Counter

cwd = Path.cwd().resolve()
ROOT = next(p for p in [cwd, *cwd.parents] if (p / 'pipeline/fase_4/run_qa.py').is_file())
sys.path.insert(0, str(ROOT))
from pipeline.fase_4.config import QAConfig
from pipeline.fase_4.engine import execute
from pipeline.fase_4.domain import TOPICOS
from pipeline.fase_4.examples import build_seed_bank

print(ROOT)
print(f'{len(TOPICOS)} tópicos; {sum(len(s) for s in TOPICOS.values())} subtópicos')
"""),
markdown("""## Configurar o experimento

O corpus deve ser o Petrolês disponível no servidor. A descoberta automática prefere `PetrolesCompleto` e usa `PetrolesHibrido` quando o completo não existe; o caminho e a assinatura ficam no manifesto. É possível escolher explicitamente pasta, arquivos TXT ou ZIP.

O `.env` deve conter endpoint, chave e versão da API Azure. Credenciais não entram em células, notebooks ou Git.
"""),
code("""cfg = QAConfig()
cfg.output = ROOT / 'pipeline/fase_4/saida_qa_v2'
# Ajuste se necessário:
# cfg.corpus_dir = Path('/caminho/no/servidor/PetrolesCompleto')
cfg.deployment = 'gpt-5-4-petrobras'
cfg.preparation_deployment = cfg.deployment
cfg.judge_deployment = cfg.deployment
cfg.effort = 'high'
cfg.limit_per_topic = 100
cfg.batch_size = 5
cfg.max_attempts_per_topic = 500
cfg.max_calls = 5000
cfg.enable_cosine_filter = False
cfg.enable_saturation_stop = False
cfg.similarity_threshold = 0.50  # Somente diagnóstico nesta rodada
cfg.resume = False  # True para continuar uma execução QA v2 existente
# cfg.topics = [next(iter(TOPICOS))]  # Opcional: restringir tópicos
cfg.validate()
print(json.dumps(cfg.serializable(), ensure_ascii=False, indent=2))
"""),
markdown("""## Baixar exemplos externos QA

O downloader busca Pirá, ARC Easy/Challenge, SQuAD 2.0, HotpotQA e BoolQ. No ARC, o texto da opção correta vira a resposta e todas as opções são removidas. Enunciados que dependem de alternativas ou passagem são filtrados. Os exemplos são referências de forma, nunca fontes factuais sobre FPSO. Licença e proveniência permanecem nos arquivos de auditoria.
"""),
code("""import subprocess
if not cfg.external_examples.exists():
    subprocess.run([sys.executable, str(ROOT / 'pipeline/qa_references/download_qa_examples.py'),
                    '--max-per-dataset', '1000'], cwd=ROOT, check=True)
else:
    print('Banco externo já disponível:', cfg.external_examples)
"""),
markdown("""## Verificar exemplos melhor avaliados

O banco preserva as vencedoras da avaliação humana da fase 2 e as aprovações sem ressalvas extraídas da revisão do especialista. A nota de preferência humana e a aprovação binária são identificadas separadamente; não são tratadas como a mesma escala do Judge. Durante a geração, questões novas com nota ≥0,85 também podem entrar no pool. Todo few-shot PetroQuest vem de outros tópicos.
"""),
code("""seeds = build_seed_bank(cfg)
print('Seeds elegíveis:', len(seeds))
print('Origens:', dict(Counter(q['origin'] for q in seeds)))
print('Tópicos:', dict(Counter(q['topic'] for q in seeds)))
print(seeds[0]['question'])
print(seeds[0]['answer'])
"""),
markdown("""## Rever o prompt

O núcleo do prompt usa apenas QA e contexto quando necessário. O conteúdo dinâmico inclui o escopo revisado, a faceta, o documento consolidado e os trechos originais com seus IDs. Cada resposta gerada precisa indicar evidência literal para auditoria. O Scorer verifica a forma e a rastreabilidade; o Refiner corrige problemas; o Judge avalia a versão final contra as fontes.
"""),
code("""subprocess.run([sys.executable, str(ROOT / 'pipeline/fase_4/run_qa.py'), '--print-prompt'],
               cwd=ROOT, check=True)
"""),
markdown("""## Executar o fluxo completo

A primeira execução extrai facetas, percorre o corpus, faz recuperação semântica com MMR e treina codebooks fixos sobre trechos do domínio. Em seguida gera e avalia QA. Índices, codebooks, estados e pedidos por papel são persistidos. A entropia principal mede a distribuição dos pares pergunta/resposta sobre esses clusters fixos, por tópico e subtópico.

Os limites de 100 aceitas, tentativas, chamadas e falhas técnicas são os únicos encerramentos ativos neste experimento. O sinal `configured_saturation_would_stop` fica disponível para estudo e não interrompe a rodada.
"""),
code("""run = execute(cfg)
print(run.meta['status'])
print('Questões aceitas:', len(run.accepted))
print('Pedidos por papel:', run.state['calls_by_role'])
"""),
markdown("""## Estudar curvas e regras simuladas

Cada candidata conserva versão original, refinamentos, diagnóstico do Scorer, veredito/nota/dificuldade do Judge, fontes, métricas e IDs dos exemplos. As decisões simuladas não são taxas de uma geração contrafactual completa: o conjunto é o produzido nesta execução observacional. Isso permite comparar cortes sem esconder o efeito de seleção.
"""),
code("""import pandas as pd
import matplotlib.pyplot as plt

rows_path = cfg.output / 'metricas_por_rodada.jsonl'
if rows_path.exists():
    rounds = pd.read_json(rows_path, lines=True)
    rounds['entropy_value'] = rounds['entropy'].map(lambda x: x['value'])
    fig, axes = plt.subplots(1, 2, figsize=(13, 4))
    for topic, group in rounds.groupby('topic', sort=False):
        axes[0].plot(group['round'], group['entropy_value'], label=topic)
        axes[1].plot(group['round'], group['mean_cosine'], label=topic)
    axes[0].set(title='Entropia sobre clusters fixos do domínio', xlabel='Rodada', ylabel='Entropia normalizada')
    axes[1].set(title='Cosine máximo médio por rodada', xlabel='Rodada', ylabel='Cosine')
    axes[0].legend(fontsize=6, loc='best')
    fig.tight_layout()
    fig.savefig(cfg.output / 'curvas_metricas.png', dpi=180)
    plt.show()
"""),
code("""candidate_path = cfg.output / 'candidatas_metricas.jsonl'
if candidate_path.exists():
    candidates = pd.read_json(candidate_path, lines=True)
    if 'counterfactual_decisions' in candidates:
        measured = candidates[candidates['counterfactual_decisions'].map(lambda x: isinstance(x, dict))]
        policies = pd.json_normalize(measured['counterfactual_decisions'])
        display(policies.mean().rename('fração que seria recusada').to_frame())
    display(candidates.reindex(columns=['topic', 'subtopic', 'question', 'answer', 'accepted', 'nota',
                                       'requested_difficulty', 'difficulty', 'rejection_reason']).head(20))
"""),
markdown("""## Levar os resultados para curadoria

`questoes_qa.jsonl` contém as aprovadas pelo fluxo técnico. `pares_qa.jsonl` contém somente pergunta/resposta. `seeds_especialista_e_geradas.jsonl` reúne candidatas aprovadas pelo especialista e novas questões para curadoria. Dados de auditoria, fontes e exemplos são preservados na pasta da execução. A revisão humana continua necessária para confirmar a qualidade das questões e calibrar as métricas.
"""),
code("""import zipfile
archive = ROOT / 'pipeline/fase_4/petroquest_qa_v2_resultados.zip'
with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED) as zipped:
    for path in cfg.output.rglob('*'):
        if path.is_file():
            zipped.write(path, path.relative_to(cfg.output.parent))
print('Pacote para trazer de volta:', archive)
"""),
]


def main():
    for number, cell in enumerate(cells):
        cell["id"] = f"qa-v2-{number:02d}"
    notebook = {"cells": cells, "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python"}}, "nbformat": 4, "nbformat_minor": 5}
    path = Path(__file__).with_name("petroquest_fase4_qa.ipynb")
    path.write_text(json.dumps(notebook, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
