#!/usr/bin/env bash
# Execute a partir do checkout, com o ambiente Python/Azure já configurado.
set -euo pipefail
task_repo="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$task_repo"
qa_python="${PYTHON_BIN:-python}"
qa_manifest="${QA_CORPUS_MANIFEST:-dataset/domain_corpora/manifest.json}"
qa_output="${QA_OUTPUT:-pipeline/fase_4/saida_qa_v6_documentos_10x1000_medium}"

if [[ ! -f "$qa_manifest" ]]; then
  echo "Manifesto não encontrado: $qa_manifest"
  echo "Instale os corpora com pipeline/domain_corpora/install_corpora.py antes de gerar."
  exit 2
fi

"$qa_python" pipeline/fase_4/prepare_tokenizer.py
if [[ ! -f pipeline/qa_references/data/qa_examples.jsonl ]]; then
  "$qa_python" pipeline/qa_references/download_qa_examples.py --max-per-dataset 1000
fi

exec "$qa_python" -u pipeline/fase_4/run_qa.py \
  --corpus-manifest "$qa_manifest" \
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
  --output "$qa_output" \
  "$@"
