#!/usr/bin/env bash
# Experimento de modos: planejamento e redação no mesmo prompt (junto) x em chamadas separadas
# (separado). Condição C (3 exemplos do especialista), 4 questões por janela, pelo menos 1 média e 1 difícil,
# nas mesmas 40 janelas do experimento de exemplos. Somente geração.
# Uso: bash pipeline/qa_research/rodar_experimento_modos.sh [opções]
#   ex.: --limite 2            (teste rápido: 2 focos por item em cada modo, 12 chamadas)
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

saida=""
args=("$@")
for ((i = 0; i < ${#args[@]}; i++)); do
    if [[ "${args[$i]}" == "--saida" ]]; then saida="${args[$((i + 1))]}"; fi
done
if [[ -z "$saida" ]]; then
    saida="pipeline/qa_research/relatorios/experimento_modos_$(date -u +%Y%m%dT%H%M%SZ)"
    args+=("--saida" "$saida")
fi

"$qa_python" -u -m pipeline.qa_research.piloto_janela modos "${args[@]}"
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
    echo "  bash pipeline/qa_research/rodar_experimento_modos.sh --saida $saida"
fi
exit $status
