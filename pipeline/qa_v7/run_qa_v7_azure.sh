#!/usr/bin/env bash
# QA v7 na Azure a partir do inventário.
#   cota:     100 perguntas aprovadas por tópico (10 tópicos), distribuídas entre os subtópicos
#   profundo: TODOS os alvos de 3 subtópicos (Produtos químicos, Separadores Trifásicos, SGSO),
#             para estudar critérios de parada pela curva de novidade
# Uso: bash pipeline/qa_v7/run_qa_v7_azure.sh cota|profundo|ambos   (padrão: ambos, um depois do outro)
# Variáveis: QA_PYTHON, QA_WORKERS (8), QA_GERADOR (gpt-5-4-petrobras:low), QA_JUIZ (gpt-5-4-petrobras:low),
#            QA_POR_TOPICO (100), QA_SAIDA_COTA, QA_SAIDA_PROFUNDO, QA_PROFUNDOS (nomes separados por "|").
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"
if [[ -n "${QA_PYTHON:-}" ]]; then PY="$QA_PYTHON"
elif [[ -x "$ROOT/venv/bin/python" ]]; then PY="$ROOT/venv/bin/python"
else PY=python3; fi
ETAPA="${1:-ambos}"
I=pipeline/inventario
INV=("$I/saida_sistemas_de_lastro_v4_notas" "$I/saida_mais_4_topicos_v4_nano_low" "$I/saida_ultimos_5_topicos_v4_nano_low")
EXT=pipeline/qa_references/data/qa_examples_v7.jsonl
for d in "${INV[@]}"; do [[ -d "$d" ]] || { echo "Inventário ausente: $d" >&2; exit 2; }; done
if [[ ! -s "$EXT" ]]; then
  echo "[qa] baixando exemplos externos (Pirá, ARC, HotpotQA)"
  "$PY" pipeline/qa_references/download_qa_examples.py --out "$EXT" --max-per-dataset 300 \
    --only pira_ptbr arc_challenge arc_easy hotpotqa
fi
COMUM=(--inventarios "${INV[@]}" --exemplos-externos "$EXT" --llm-provider azure
       --gerador "${QA_GERADOR:-gpt-5-4-petrobras:low}" --juiz "${QA_JUIZ:-gpt-5-4-petrobras:low}"
       --workers "${QA_WORKERS:-8}")

if [[ "$ETAPA" == cota || "$ETAPA" == ambos ]]; then
  OUT="${QA_SAIDA_COTA:-pipeline/qa_v7/saida_cota_100_por_topico}"
  mkdir -p "$OUT"
  echo "[qa] cota: ${QA_POR_TOPICO:-100} por tópico -> $OUT"
  "$PY" -u pipeline/qa_v7/gerar_qa.py "${COMUM[@]}" --saida "$OUT" --modo cota --por-topico "${QA_POR_TOPICO:-100}"
fi

if [[ "$ETAPA" == profundo || "$ETAPA" == ambos ]]; then
  OUT="${QA_SAIDA_PROFUNDO:-pipeline/qa_v7/saida_profundo_3_subtopicos}"
  IFS='|' read -r -a SUBS <<< "${QA_PROFUNDOS:-Produtos químicos|Operação de Separadores Trifásicos|SGSO}"
  mkdir -p "$OUT"
  echo "[qa] profundo: ${SUBS[*]} -> $OUT"
  "$PY" -u pipeline/qa_v7/gerar_qa.py "${COMUM[@]}" --saida "$OUT" --modo profundo --subtopicos "${SUBS[@]}"
fi
echo "[qa] concluído"
