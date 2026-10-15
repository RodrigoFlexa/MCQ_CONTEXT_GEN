#!/usr/bin/env bash
# Piloto QA v7 na Azure: (1) gera 4 questões por subtópico a partir do inventário;
# (2) compara juízes sobre as mesmas questões e sobre versões com defeitos plantados.
# Uso: bash pipeline/qa_v7/run_piloto_juizes_azure.sh [geracao|juizes|tudo]   (padrão: tudo)
# Variáveis: QA_PYTHON, QA_OUTPUT, QA_GERADOR, QA_JUIZ, QA_JUIZES, QA_DEFEITOS, QA_WORKERS, QA_SOL (=1 também
#            compara os juízes nas 160 questões do piloto gerado com gpt-6.1-sol).
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"
if [[ -n "${QA_PYTHON:-}" ]]; then
  PY="$QA_PYTHON"
elif [[ -x "$ROOT/venv/bin/python" ]]; then
  PY="$ROOT/venv/bin/python"
else
  PY=python3
fi
ETAPA="${1:-tudo}"
OUT="${QA_OUTPUT:-pipeline/qa_v7/saida_piloto_azure_v2}"
I=pipeline/inventario
INV=("$I/saida_sistemas_de_lastro_v4_notas" "$I/saida_mais_4_topicos_v4_nano_low" "$I/saida_ultimos_5_topicos_v4_nano_low")
EXT=pipeline/qa_references/data/qa_examples_v7.jsonl
read -r -a JUIZES <<< "${QA_JUIZES:-gpt-5-4-petrobras:medium gpt-5-2-petrobras:medium gpt-5-4-petrobras:low}"
for d in "${INV[@]}"; do [[ -d "$d" ]] || { echo "Inventário ausente: $d" >&2; exit 2; }; done
mkdir -p "$OUT"

if [[ ! -s "$EXT" ]]; then
  echo "[piloto] baixando exemplos externos (Pirá, ARC, HotpotQA)"
  "$PY" pipeline/qa_references/download_qa_examples.py --out "$EXT" --max-per-dataset 300 \
    --only pira_ptbr arc_challenge arc_easy hotpotqa
fi

if [[ "$ETAPA" == geracao || "$ETAPA" == tudo ]]; then
  echo "[piloto] geração: gerador ${QA_GERADOR:-gpt-5-4-petrobras:low}, juiz ${QA_JUIZ:-gpt-5-4-petrobras:medium}"
  "$PY" -u pipeline/qa_v7/gerar_qa.py --inventarios "${INV[@]}" --saida "$OUT" --exemplos-externos "$EXT" \
    --llm-provider azure --gerador "${QA_GERADOR:-gpt-5-4-petrobras:low}" --juiz "${QA_JUIZ:-gpt-5-4-petrobras:medium}" \
    --workers "${QA_WORKERS:-8}"
fi

if [[ "$ETAPA" == juizes || "$ETAPA" == tudo ]]; then
  echo "[piloto] comparação de juízes: ${JUIZES[*]}"
  "$PY" -u pipeline/qa_v7/comparar_juizes.py --inventarios "${INV[@]}" --questoes "$OUT/questoes.jsonl" \
    --saida "$OUT/juizes" --juizes "${JUIZES[@]}" --gerador-defeitos "${QA_GERADOR:-gpt-5-4-petrobras:low}" \
    --defeitos "${QA_DEFEITOS:-32}" --llm-provider azure --workers "${QA_WORKERS:-8}"
  if [[ "${QA_SOL:-0}" == 1 ]]; then
    "$PY" -u pipeline/qa_v7/comparar_juizes.py --inventarios "${INV[@]}" \
      --questoes pipeline/qa_v7/piloto_sol_2026_10_14/questoes.jsonl --saida "$OUT/juizes_sobre_sol" \
      --juizes "${JUIZES[@]}" --gerador-defeitos "${QA_GERADOR:-gpt-5-4-petrobras:low}" \
      --defeitos "${QA_DEFEITOS:-32}" --llm-provider azure --workers "${QA_WORKERS:-8}"
  fi
fi
echo "[piloto] concluído: $OUT"
