#!/usr/bin/env bash
# Experimento de refino (pipeline/qa_research/TIPOS_QUESTAO.md, v21): o refinador forte recupera mais reprovadas?
#   Parte do piloto v19 (07_03 e 03_03), sem gerar nada novo. As 153 originais reprovadas pelo auditor passam
#   por dois refinadores com o prompt refinador_v3 (todos os motivos, exemplos aprovados, histórico):
#     mini  = gpt-5-mini-petrobras:medium
#     forte = gpt-5-4-petrobras:high
#   Cada versão volta ao auditor v3 (com o texto-fonte); as reprovadas de novo têm mais uma tentativa.
#   No fim, deduplicação por sentido contra as 92 aprovadas do piloto, para medir o ganho líquido.
# Uso: bash pipeline/qa_research/rodar_teste_refino.sh [--saida <pasta>] [--bracos forte] [--rodadas 2]
set -uo pipefail
export PYTHONUTF8=1
qa_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd)"
cd -- "$qa_root"
qa_python="$qa_root/.venv-documento/bin/python"
if [[ -n "${DOCUMENT_PYTHON:-}" ]]; then
    qa_python="$DOCUMENT_PYTHON"
elif [[ ! -x "$qa_python" ]]; then
    qa_python="$qa_root/venv/bin/python"
    if [[ ! -x "$qa_python" ]]; then qa_python="$(command -v python3)"; fi
fi

saida="pipeline/qa_research/relatorios/teste_refino_$(date -u +%Y%m%dT%H%M%SZ)"
args=()
while [[ $# -gt 0 ]]; do
    case "$1" in
        --saida) saida="$2"; shift 2 ;;
        *) args+=("$1"); shift ;;
    esac
done

"$qa_python" -u -m pipeline.qa_research.geracao_tipos refino --saida "$saida" "${args[@]}"
s=$?

if [[ $s -eq 0 ]]; then
    echo
    echo "O código acabou de rodar no terminal :)"
    echo
    echo "Para enviar os resultados (no servidor):"
    echo "  bash pipeline/qa_research/enviar_resultados.sh $saida"
    echo
    echo "Na sua máquina:"
    echo "  git pull"
    echo "  e abra $saida/REFINO.md"
else
    echo
    echo "Algumas unidades falharam. Para tentar só elas:"
    echo "  bash pipeline/qa_research/rodar_teste_refino.sh --saida $saida ${args[*]}"
fi
