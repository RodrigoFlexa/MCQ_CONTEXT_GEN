# PetroQuest QA v6 — documentos técnicos por faceta

## Configuração da próxima rodada

- Petrolês + ANP + HSE + BSEE + REGIS pelo manifesto já instalado.
- Até **10 trechos por faceta**, alvo de **1.000 palavras por trecho**. Não se inventa texto para completar quantidade ou tamanho.
- Janelas podem juntar páginas consecutivas do mesmo documento. Não atravessam documentos nem lacunas na paginação; Petrolês preserva seu limite conhecido de TXT concatenado. Página inicial/final e offsets ficam na proveniência.
- **Um documento técnico por faceta**, composto por GPT `gpt-5-4-petrobras`, effort `medium`. Explicação técnica organizada, sem meta obrigatória de palavras; orçamento da resposta de 32.000 tokens, incluindo raciocínio conforme o backend.
- Sem auditoria factual prévia bloqueante no modo padrão `composed`. O prompt pede corretude/plausibilidade, preservação de condições e registro de dúvidas. Metadados declaram `factually_audited=false`.
- Scorer/Refiner/Judge continuam avaliando as QA, com documento e trechos originais. Dificuldade independente. Nenhuma alternativa.
- Meta de **100 novas QA aprovadas por tópico**, dez tópicos; não 100 por faceta. Similaridade/redundância e parada científica permanecem observacionais.
- Embeddings exclusivos `embedding-3-large-global`; exemplos humanos melhor avaliados e exemplos externos QA continuam presentes.

O corpus, os PDFs/XML/TXT e os exemplos externos já baixados podem ser reutilizados. Índices e documentos de QA v4/v5 não são compatíveis: iniciar em saída nova QA v6.

## 1. Atualizar o servidor

Na raiz do repositório, usando o ambiente Python/Azure das rodadas anteriores:

```bash
git pull --ff-only origin dev
python -m pip install -r requirements.txt
```

Endpoint, chave, versão e certificado Azure permanecem na configuração local do servidor. O script utiliza o mesmo backend já configurado; não inclui credenciais.

## 2. Executar em segundo plano

```bash
mkdir -p pipeline/fase_4/saida_qa_v6_documentos_10x1000_medium

nohup bash pipeline/fase_4/run_qa_v6.sh \
  > pipeline/fase_4/saida_qa_v6_documentos_10x1000_medium/execucao.log \
  2>&1 < /dev/null &

echo $!
```

O script prepara o tokenizer e baixa exemplos externos **somente se ainda não houver o arquivo**. Confere a presença do manifesto; o motor valida seus arquivos/hashes antes das chamadas. O instalador de corpora não é executado novamente.

Ele roda o equivalente a:

```bash
python -u pipeline/fase_4/run_qa.py \
  --corpus-manifest dataset/domain_corpora/manifest.json \
  --deployment gpt-5-4-petrobras \
  --effort medium \
  --embedding-deployment embedding-3-large-global \
  --context-mode composed \
  --chunk-words 1000 \
  --chunks-per-facet 10 \
  --composition-max-tokens 32000 \
  --limit-per-topic 100 \
  --batch-size 2 \
  --observe-only \
  --max-calls 20000 \
  --output pipeline/fase_4/saida_qa_v6_documentos_10x1000_medium
```

Se quiser primeiro cinco perguntas de KPI, em saída separada:

```bash
QA_OUTPUT=pipeline/fase_4/saida_qa_v6_piloto_kpi \
  bash pipeline/fase_4/run_qa_v6.sh \
  --topics "Gestão do Desempenho Empresarial (KPI)" \
  --limit-per-topic 5 --batch-size 1
```

`PYTHON_BIN=python3`, `QA_CORPUS_MANIFEST=/caminho/manifest.json` e `QA_OUTPUT=/caminho/saida` permitem ajustar caminhos sem editar o script. Defaults correspondem à instalação já utilizada no servidor.

## 3. Acompanhar

```bash
tail -f pipeline/fase_4/saida_qa_v6_documentos_10x1000_medium/execucao.log
```

O log mostra a busca, `N/10` trechos por faceta, palavras recuperadas, palavras do documento, alvos, avisos e contagem de QA aprovadas. `Ctrl+C` sai do acompanhamento sem encerrar a geração.

```bash
python -m json.tool pipeline/fase_4/saida_qa_v6_documentos_10x1000_medium/preparacao_status.json
python -m json.tool pipeline/fase_4/saida_qa_v6_documentos_10x1000_medium/state.json
pgrep -af 'pipeline/fase_4/run_qa.py'
```

`preparacao_status.json` passa a existir na etapa de composição, após a varredura. A preparação ainda termina para os tópicos selecionados antes da primeira pergunta.

## 4. Retomar somente esta execução QA v6

Depois de conferir que o processo anterior terminou:

```bash
nohup bash pipeline/fase_4/run_qa_v6.sh --resume \
  >> pipeline/fase_4/saida_qa_v6_documentos_10x1000_medium/execucao.log \
  2>&1 < /dev/null &
```

A retomada reutiliza documentos e vetores compatíveis. Não muda tópicos, prompts, tamanho dos trechos ou modelo. Se atingir o teto de chamadas, pode aumentar somente o orçamento, por exemplo `--resume --max-calls 40000`. A meta e os limites operacionais ainda podem encerrar a execução; não há garantia de 100 aprovações quando o modelo não produz QA adequadas.

## 5. Arquivos para curadoria

- `dominio/documentos/*.md`: documentos técnicos completos por faceta.
- `dominio/composicoes/*.json`: fontes utilizadas, alvos, avisos e dimensões do material.
- `dominio/composicoes/*.respostas.jsonl`: respostas originais e erros de formato.
- `dominio/contextos_candidatos/*.json`: trechos originais entregues ao compositor.
- `composicoes_contexto.jsonl`, `cobertura_dominio.json`, `preparacao_status.json`: decisões e cobertura.
- `questoes_qa.jsonl`, `pares_qa.jsonl`: QA aprovadas.
- `candidatas_metricas.jsonl`, `metricas_por_rodada.jsonl`: candidatas, avaliações e métricas, incluindo rejeições.
- `state.json`, `run_config.json`, `chamadas_modelo.jsonl`, `chamadas_embeddings.jsonl`, `execucao.log`: rastreabilidade da execução.

Os resultados são ignorados pelo Git por padrão. Para trazê-los de volta pelo GitHub, selecione arquivos de texto/JSON/Markdown; mantenha vetores e corpora grandes fora do commit. A partir da raiz, no servidor:

```bash
git add -f -- \
  pipeline/fase_4/saida_qa_v6_documentos_10x1000_medium/questoes_qa.jsonl \
  pipeline/fase_4/saida_qa_v6_documentos_10x1000_medium/pares_qa.jsonl \
  pipeline/fase_4/saida_qa_v6_documentos_10x1000_medium/candidatas_metricas.jsonl \
  pipeline/fase_4/saida_qa_v6_documentos_10x1000_medium/metricas_por_rodada.jsonl \
  pipeline/fase_4/saida_qa_v6_documentos_10x1000_medium/composicoes_contexto.jsonl \
  pipeline/fase_4/saida_qa_v6_documentos_10x1000_medium/cobertura_dominio.json \
  pipeline/fase_4/saida_qa_v6_documentos_10x1000_medium/preparacao_status.json \
  pipeline/fase_4/saida_qa_v6_documentos_10x1000_medium/state.json \
  pipeline/fase_4/saida_qa_v6_documentos_10x1000_medium/run_config.json \
  pipeline/fase_4/saida_qa_v6_documentos_10x1000_medium/chamadas_modelo.jsonl \
  pipeline/fase_4/saida_qa_v6_documentos_10x1000_medium/chamadas_embeddings.jsonl \
  pipeline/fase_4/saida_qa_v6_documentos_10x1000_medium/execucao.log \
  pipeline/fase_4/saida_qa_v6_documentos_10x1000_medium/dominio/documentos \
  pipeline/fase_4/saida_qa_v6_documentos_10x1000_medium/dominio/composicoes \
  pipeline/fase_4/saida_qa_v6_documentos_10x1000_medium/dominio/contextos_candidatos

git commit -m "Add QA v6 generated questions and technical documents"
git push origin dev
```

Se a execução não chegou a produzir algum desses arquivos, selecione apenas os existentes. Se um arquivo exceder o limite do GitHub, particione o JSONL antes de adicionar. Localmente: `git pull --ff-only origin dev`.

## Prompts e validação

[Prompts efetivos QA v6](prompts_qa_v6.md). Histórico do diagnóstico: [QA v4/v5](diagnostico_qa_v4.md).

Foram executados 76 testes offline, incluindo composição/cache, janelas entre páginas com proveniência, ausência de auditoria no modo composto, fluxo até QA/Judge/dificuldade com modelos simulados e execução do launcher Bash com Python simulado. Não houve geração paga no Azure nesta implementação; a validação factual e de acesso ocorre no servidor.
