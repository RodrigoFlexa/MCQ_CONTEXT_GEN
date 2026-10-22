#!/usr/bin/env bash
# Piloto de geração por janela (3 blocos, 1 foco). Somente geração, sem refinamento.
# Uso: bash pipeline/qa_research/rodar_piloto_janela.sh [opções do run]
#   ex.: --limite 3            (teste rápido: 3 blocos por item)
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
    saida="pipeline/qa_research/relatorios/piloto_janela_$(date -u +%Y%m%dT%H%M%SZ)"
    args+=("--saida" "$saida")
fi

"$qa_python" -u -m pipeline.qa_research.piloto_janela run "${args[@]}"
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
    echo "  e abra $saida/RESUMO.md e $saida/QUESTOES.md"
elif [[ $status -eq 2 ]]; then
    echo
    echo "Algumas janelas falharam. Para tentar só elas:"
    echo "  bash pipeline/qa_research/rodar_piloto_janela.sh --saida $saida"
fi
exit $status
