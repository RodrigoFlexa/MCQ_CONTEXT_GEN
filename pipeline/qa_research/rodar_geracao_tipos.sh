#!/usr/bin/env bash
# Geração híbrida por tipo de questão, v15 (pipeline/qa_research/TIPOS_QUESTAO.md):
#   1. janelas com o prompt v15: até 4 questões por janela (1 conceito, 1 mecanismo ou consequência,
#      1 diagnóstico, decisão ou procedimento, 1 livre sem conceito), todas as janelas do 01_01 e 36 do 02_02,
#      com exemplos e contraexemplos curados (geracao_tipos/exemplos.json) e sem datasets externos
#   2. compostas: uma questão por encadeamento do inventário (piloto v2)
#   3. auditoria por gpt-5-4-petrobras:high como filtro: tipo, validade da referência e atalho
#   4. RELATORIO.md e aprovadas.jsonl (só as questões que passaram no filtro)
# Uso: bash pipeline/qa_research/rodar_geracao_tipos.sh [opções]
#   ex.: --ec-janelas 2 --limite-compostas 2 --saida <pasta de teste>
#        --saida <pasta>      (retoma uma execução interrompida)
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
    saida="pipeline/qa_research/relatorios/geracao_tipos_$(date -u +%Y%m%dT%H%M%SZ)"
    args+=("--saida" "$saida")
fi

"$qa_python" -u -m pipeline.qa_research.geracao_tipos run "${args[@]}"
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
    echo "  e abra $saida/RELATORIO.md"
elif [[ $status -eq 2 ]]; then
    echo
    echo "Algumas unidades falharam. Para tentar só elas:"
    echo "  bash pipeline/qa_research/rodar_geracao_tipos.sh --saida $saida"
fi
exit $status
