#!/usr/bin/env bash
# Pesquisa de um tópico, capítulos revisados e meta de 10 questões. Executar no servidor.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"
if [[ -n "${DOCS_PYTHON:-}" ]]; then PY="$DOCS_PYTHON"
elif [[ -n "${QA_PYTHON:-}" ]]; then PY="$QA_PYTHON"
elif [[ -x "$ROOT/venv/bin/python" ]]; then PY="$ROOT/venv/bin/python"
else PY=python3; fi
MODE="${1:-completo}"
case "$MODE" in plan|documentos|completo) ;;
  *) echo "Modo: plan, documentos ou completo" >&2; exit 2 ;;
esac
TOPIC="${DOCS_TOPICO:-Operação de Tanques de Carga}"
OUT="${DOCS_SAIDA:-pipeline/documentos_tecnicos/saida_tanques_10}"
ETAPA="$MODE"
if [[ "$MODE" == plan ]]; then ETAPA="${DOCS_ETAPA_PLANO:-completo}"; fi
COMMON=(--saida "$OUT" --topico "$TOPIC" --etapa "$ETAPA" --provider azure
        --documentos "${DOCS_QUANTIDADE:-10}" --questoes "${DOCS_QUESTOES:-10}"
        --max-candidatas "${DOCS_MAX_CANDIDATAS:-40}"
        --max-pesquisas "${DOCS_MAX_PESQUISAS:-4}" --max-fontes "${DOCS_MAX_FONTES:-32}"
        --trechos-por-busca "${DOCS_TRECHOS_POR_BUSCA:-5}"
        --max-refinamentos "${DOCS_MAX_REFINAMENTOS:-1}"
        --max-refinamentos-qa "${DOCS_MAX_REFINAMENTOS_QA:-1}"
        --max-chamadas "${DOCS_MAX_CHAMADAS:-400}"
        --max-chamadas-documento "${DOCS_MAX_CHAMADAS_DOCUMENTO:-24}"
        --max-chamadas-questao "${DOCS_MAX_CHAMADAS_QUESTAO:-20}"
        --cache-dir "${DOCS_CACHE:-pipeline/documentos_tecnicos/cache_compartilhado}"
        --indice-dir "${DOCS_INDICE:-pipeline/qa_v11/cache_compartilhado/indice}"
        --pesquisador "${DOCS_PESQUISADOR:-gpt-5-4-petrobras:low}"
        --revisor "${DOCS_REVISOR:-gpt-5-4-petrobras:low}"
        --refinador "${DOCS_REFINADOR:-gpt-5-4-petrobras:low}"
        --respondente "${DOCS_RESPONDENTE:-gpt-5-2-petrobras:low}"
        --novidade "${DOCS_NOVIDADE:-gpt-5-4-nano-petrobras:low}"
        --exemplos-externos "${DOCS_EXEMPLOS:-pipeline/qa_references/data/qa_examples_v11.jsonl}"
        --pareceres "${DOCS_PARECERES:-pipeline/qa_references/review/questoes_revisadas_classificadas.jsonl}")
MANIFEST="${DOCS_MANIFEST:-dataset/domain_corpora/manifest.json}"
if [[ -f "$MANIFEST" ]]; then COMMON+=(--manifest "$MANIFEST")
elif [[ -n "${DOCS_MANIFEST:-}" ]]; then
  echo "Manifesto informado não existe: $MANIFEST" >&2; exit 2
else
  echo "Sem corpus bruto instalado: cobertura limitada aos índices e seleções salvos."
fi
if [[ "${DOCS_REVISITAR_PENDENTES:-0}" == 1 ]]; then COMMON+=(--revisitar-pendentes); fi
if [[ "$MODE" == plan ]]; then
  "$PY" -u -m pipeline.documentos_tecnicos.run "${COMMON[@]}" --plan
  exit 0
fi
if [[ "$MODE" == completo ]]; then
  EXAMPLES="${DOCS_EXEMPLOS:-pipeline/qa_references/data/qa_examples_v11.jsonl}"
  if [[ ! -s "$EXAMPLES" ]]; then
    "$PY" -u pipeline/qa_references/download_qa_examples.py \
      --only pira_ptbr arc_easy arc_challenge hotpotqa --max-per-dataset 500 \
      --preserve-reasoning-context --out "$EXAMPLES"
  fi
fi
"$PY" -u -m pipeline.documentos_tecnicos.run "${COMMON[@]}"
