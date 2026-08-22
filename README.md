# MCQ_CONTEXT_GEN

Geração e avaliação de questões de múltipla escolha (MCQ) em português, no domínio de óleo e gás (corpus Petrolês), comparando geração fundamentada em contexto (RAG) vs. instruction-only.

## Estrutura

- `pipeline/` — scripts do pipeline atual:
  - `geracao_mcq_petroles.py` — geração *context-grounded* (RAG sobre o corpus Petrolês).
  - `geracao_mcq_instrucao.py` — geração *instruction-only* (baseline), 5 assuntos.
  - `analise_selecao_mcq.py` — métricas comparativas e seleção estratificada de questões.
  - `pipeline/notebooks/geracao/` — notebooks de geração, pareados aos scripts via jupytext.
  - `pipeline/notebooks/avaliacao/` — notebooks de avaliação e análise de resultados.
  - `prompt_mcq_generation.py` — templates de prompt, importado pelos notebooks acima.
  - `gerar_pares_30_v2.py` — monta os pares para o formulário de avaliação comparativa.
  - `gerar_preview_mcq.py`, `progresso.py`, `reordenar_questionario.py`, `analisar_respostas.py` — utilitários de acompanhamento/pós-processamento.
  - `rodar_experimento.sh` — roda as duas condições de geração em sequência.
  - `corpus/` — os dois arquivos de corpus Petrolês usados na geração.
  - `mcq_output/` — todos os artefatos gerados (datasets, logs, pares de avaliação).
  - Todos os caminhos relativos nos scripts assumem execução a partir desta pasta.
- `reports/` — relatório comparativo (`analise_comparativa_mcq.html`) e respostas do formulário de avaliação (`.xlsx`).
- `archive/` — material superado ou histórico, mantido só por rastreabilidade:
  - `pipeline_superseded/` — protótipo de geração *instruction-only* de 1 assunto e a v1 do fluxo de pareamento/form (`gerar_pares_30.py` + `gerar_form_comparativo.py`), ambos substituídos por versões generalizadas/v2 ainda em uso em `pipeline/`.
  - `mcq_output_v1/` — saídas da v1 do fluxo de pareamento (mapa, form `.gs`, pares), substituídas pelas versões `_v2` em `pipeline/mcq_output/`.
  - `results_backup/`, `results_backup_2/` — backups antigos de execuções.
  - `teste.ipynb` — notebook de teste avulso.
- `data/` — corpus bruto grande não usado diretamente pelo pipeline atual (`NILC.txt`).
- `venv/` — ambiente virtual Python (não versionado).

## Uso

Os scripts em `pipeline/` esperam ser executados com `pipeline/` como diretório de trabalho (ex.: `cd pipeline && python gerar_pares_30_v2.py`), pois usam caminhos relativos como `mcq_output/` e `corpus/`, e importam `prompt_mcq_generation.py` do mesmo diretório.
