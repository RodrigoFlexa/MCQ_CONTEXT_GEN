#!/usr/bin/env bash
# Experimento de exemplos de forma: condições A (sem), B (externos), C (especialista) e D (B + C),
# nas mesmas janelas (20 focos por item em 01_01 e 02_02). Somente geração.
# Uso: bash pipeline/qa_research/rodar_experimento_exemplos.sh [opções]
#   ex.: --limite 2            (teste rápido: 2 focos por item em cada condição)
#        --saida <pasta>       (retoma uma execução interrompida)
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

if [[ ! -s pipeline/qa_references/data/qa_examples.jsonl ]]; then
    echo "Exemplos externos ausentes. Baixe com:"
    echo "  $qa_python pipeline/qa_references/download_qa_examples.py --only pira_ptbr arc_challenge hotpotqa --max-per-dataset 1000"
    exit 1
fi

saida=""
args=("$@")
for ((i = 0; i < ${#args[@]}; i++)); do
    if [[ "${args[$i]}" == "--saida" ]]; then saida="${args[$((i + 1))]}"; fi
done
if [[ -z "$saida" ]]; then
    saida="pipeline/qa_research/relatorios/experimento_exemplos_$(date -u +%Y%m%dT%H%M%SZ)"
    args+=("--saida" "$saida")
fi

"$qa_python" -u -m pipeline.qa_research.piloto_janela experimento "${args[@]}"
status=$?

if [[ $status -eq 0 ]]; then
    echo
    echo "O código acabou de rodar no terminal :)"
    echo
    echo "Para enviar os resultados (no servidor):"
    echo "  bash pipeline/qa_research/enviar_resultados.sh $saida"
    echo
    echo "Na sua máquina:"
    echo "  git pull"
    echo "  e abra $saida/COMPARACAO.md"
elif [[ $status -eq 2 ]]; then
    echo
    echo "Algumas janelas falharam. Para tentar só elas:"
    echo "  bash pipeline/qa_research/rodar_experimento_exemplos.sh --saida $saida"
fi
exit $status
