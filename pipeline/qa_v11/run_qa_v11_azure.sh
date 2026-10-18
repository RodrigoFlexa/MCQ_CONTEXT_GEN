#!/usr/bin/env bash
# Piloto de 30 questões ou bateria de três configurações. Execução no servidor.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"
if [[ -n "${QA_PYTHON:-}" ]]; then PY="$QA_PYTHON"
elif [[ -x "$ROOT/venv/bin/python" ]]; then PY="$ROOT/venv/bin/python"
else PY=python3; fi
MODE="${1:-piloto}"
case "$MODE" in plan|piloto|experimentos|comparar|referencias) ;;
  *) echo "Modo: plan, piloto, experimentos, comparar ou referencias" >&2; exit 2 ;;
esac
BASE="${QA_V11_SAIDA:-pipeline/qa_v11/saida_30}"
CACHE="${QA_V11_CACHE:-pipeline/qa_v11/cache_compartilhado}"
EXAMPLES="${QA_V11_EXEMPLOS:-pipeline/qa_references/data/qa_examples_v11.jsonl}"
CONFIG="${QA_V11_CONFIG:-nota_complemento}"
METHODS=(direta nota nota_complemento)
SUBS="${QA_V11_SUBTOPICOS:-Operação de Separadores Trifásicos|SGSO|Operação de Tanques de Carga}"
IFS='|' read -r -a FILTERS <<< "$SUBS"
COMMON=(--cache-dir "$CACHE" --exemplos-externos "$EXAMPLES" --provider azure
        --subtopicos "${FILTERS[@]}" --por-topico "${QA_V11_POR_TOPICO:-10}"
        --modo "${QA_V11_MODO:-cota}" --workers "${QA_WORKERS:-3}"
        --max-unidades "${QA_V11_MAX_UNIDADES:-20}" --max-candidatas "${QA_V11_MAX_CANDIDATAS:-50}"
        --max-chamadas "${QA_V11_MAX_CHAMADAS:-900}"
        --redator "${QA_GERADOR:-gpt-5-4-petrobras:low}" --juiz "${QA_JUIZ:-gpt-5-4-petrobras:low}"
        --respondente "${QA_RESPONDENTE:-gpt-5-2-petrobras:low}"
        --novidade "${QA_NOVIDADE:-gpt-5-4-nano-petrobras:low}" --seed "${QA_V11_SEED:-42}")
MANIFEST="${QA_V11_MANIFEST:-dataset/domain_corpora/manifest.json}"
if [[ -f "$MANIFEST" ]]; then COMMON+=(--manifest "$MANIFEST")
elif [[ -n "${QA_V11_MANIFEST:-}" ]]; then
  echo "Manifesto informado não existe: $MANIFEST" >&2; exit 2
else
  echo "Sem corpus bruto local: a recuperação usará todos os índices e seleções salvos."
fi
prepare_examples() {
  if [[ ! -s "$EXAMPLES" || "$MODE" == referencias ]]; then
    "$PY" -u pipeline/qa_references/download_qa_examples.py \
      --only pira_ptbr arc_easy arc_challenge hotpotqa --max-per-dataset 500 \
      --preserve-reasoning-context --out "$EXAMPLES"
  fi
}
compare() {
  local outputs=()
  for config in "${METHODS[@]}"; do outputs+=("$BASE/$config"); done
  "$PY" -u -m pipeline.qa_v11.comparar --experimentos "${outputs[@]}" --saida "$BASE/comparacao"
}
if [[ "$MODE" == plan ]]; then
  "$PY" -u -m pipeline.qa_v11.run "${COMMON[@]}" --configuracao "$CONFIG" --saida "$BASE/$CONFIG" --plan
  exit 0
fi
if [[ "$MODE" == comparar ]]; then compare; exit 0; fi
prepare_examples
if [[ "$MODE" == referencias ]]; then exit 0; fi
if [[ "$MODE" == piloto ]]; then
  "$PY" -u -m pipeline.qa_v11.run "${COMMON[@]}" --configuracao "$CONFIG" --saida "$BASE/$CONFIG"
else
  mkdir -p "$BASE"
  failed=0
  # Uma configuração incompleta não impede coletar resultados das demais.
  for config in "${METHODS[@]}"; do
    echo "=== Configuração: $config ==="
    if "$PY" -u -m pipeline.qa_v11.run "${COMMON[@]}" --configuracao "$config" --saida "$BASE/$config" \
      > "$BASE/console_${config}.log" 2>&1; then
      echo "$config: meta atingida"
    else
      code=$?
      echo "$config: execução retornou $code; consulte $BASE/console_${config}.log" >&2
      failed=1
    fi
  done
  compare
  if [[ "$failed" -ne 0 ]]; then
    echo "Uma ou mais configurações ficaram incompletas. A comparação preserva esse estado." >&2
    exit 2
  fi
fi
echo "Resultados: $BASE"
