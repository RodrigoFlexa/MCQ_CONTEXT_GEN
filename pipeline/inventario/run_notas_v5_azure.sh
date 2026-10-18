#!/usr/bin/env bash
# Reconstrói notas v5 e gera QA v10 usando os artefatos existentes.
# Uso: bash pipeline/inventario/run_notas_v5_azure.sh plan|piloto|completo|qa
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"
if [[ -n "${QA_PYTHON:-}" ]]; then PY="$QA_PYTHON"
elif [[ -x "$ROOT/venv/bin/python" ]]; then PY="$ROOT/venv/bin/python"
else PY=python3; fi
MODE="${1:-piloto}"
case "$MODE" in plan|piloto|completo|qa) ;; *) echo "Modo: plan, piloto, completo ou qa" >&2; exit 2 ;; esac
I=pipeline/inventario
INV=("$I/saida_sistemas_de_lastro_v4_notas" "$I/saida_mais_4_topicos_v4_nano_low" "$I/saida_ultimos_5_topicos_v4_nano_low")
for d in "${INV[@]}"; do [[ -d "$d" ]] || { echo "Inventário ausente: $d" >&2; exit 2; }; done
if [[ "$MODE" == completo ]]; then
  DEFAULT_NOTAS="$I/saida_notas_v5_completo"
  DEFAULT_QA=pipeline/qa_v7/saida_v10_completo
  DEFAULT_COTA=100
else
  DEFAULT_NOTAS="$I/saida_notas_v5_piloto"
  DEFAULT_QA=pipeline/qa_v7/saida_v10_piloto
  DEFAULT_COTA=10
fi
NOTAS="${V5_SAIDA_NOTAS:-$DEFAULT_NOTAS}"
QA="${V5_SAIDA_QA:-$DEFAULT_QA}"
ARGS=(--origens "${INV[@]}" --saida "$NOTAS" --provider azure
      --modelo "${V5_MODELO_NOTAS:-gpt-5-4-petrobras}" --effort "${V5_EFFORT:-low}"
      --workers "${QA_WORKERS:-8}" --max-chamadas "${V5_MAX_CHAMADAS:-30000}")
if [[ "$MODE" != completo ]]; then
  SUBS="${V5_SUBTOPICOS:-Operação de Separadores Trifásicos|SGSO|Operação de Tanques de Carga}"
  IFS='|' read -r -a FILTERS <<< "$SUBS"
  ARGS+=(--subtopicos "${FILTERS[@]}" --limite-conceitos-por-subtopico "${V5_LIMITE_CONCEITOS:-6}")
fi
if [[ "$MODE" == plan ]]; then
  "$PY" -u pipeline/inventario/reconstruir_notas.py "${ARGS[@]}" --plan
  exit 0
fi
if [[ "$MODE" != qa ]]; then
  "$PY" -u pipeline/inventario/reconstruir_notas.py "${ARGS[@]}"
fi
[[ -s "$NOTAS/notas_aprovadas.jsonl" ]] || { echo "Nenhuma nota aprovada em $NOTAS; veja resumo.json e ocorrencias.jsonl" >&2; exit 3; }
"$PY" -u pipeline/qa_v7/gerar_qa.py --inventarios "$NOTAS" --saida "$QA" --modo cota \
  --por-topico "${QA_POR_TOPICO:-$DEFAULT_COTA}" --llm-provider azure --workers "${QA_WORKERS:-8}" \
  --gerador "${QA_GERADOR:-gpt-5-4-petrobras:low}" --juiz "${QA_JUIZ:-gpt-5-4-petrobras:low}" \
  --respondente "${QA_RESPONDENTE:-gpt-5-2-petrobras:low}" --escopo-novidade topico
echo "Notas: $NOTAS/resumo.json"
echo "Questões: $QA/resumo.json"
