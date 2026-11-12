#!/usr/bin/env bash
# Dificuldade cognitiva v3 no banco final (experimento_ab/dificuldade_v3.py, prompt prompts/dificuldade_v3.md).
# Quatro dimensões (conhecimento, inferência, sistemas, generalista; 0 a 2) e o nível de um profissional de FPSO,
# comparados com a rubrica antiga e com a dificuldade empírica do painel.
#
# Uso: bash pipeline/qa_research/rodar_dificuldade_v3.sh [--amostra N] [--workers N]
#   --amostra N   amostra estratificada por tipo (teste rápido); sem a opção, o banco inteiro (3.813 questões)
# Repetir o mesmo comando retoma de onde parou.
set -uo pipefail
export PYTHONUTF8=1
qa_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd)"
cd -- "$qa_root"
py="${DOCUMENT_PYTHON:-$qa_root/.venv-documento/bin/python}"
if [[ ! -x "$py" ]]; then
    py="$qa_root/venv/bin/python"
    if [[ ! -x "$py" ]]; then py="$(command -v python3)"; fi
fi

pasta="pipeline/qa_research/relatorios/petroquest_banco_v1/dificuldade_v3_1"
args=("$@")
for ((i = 0; i < ${#args[@]}; i++)); do
    if [[ "${args[$i]}" == "--amostra" && -n "${args[$((i + 1))]:-}" && "${args[$((i + 1))]}" != "0" ]]; then
        pasta="${pasta}_amostra${args[$((i + 1))]}"
    fi
done

st=0
for t in 1 2 3; do
    echo "[$(date +%H:%M:%S)] dificuldade v3 (tentativa $t)"
    "$py" -u -m pipeline.qa_research.experimento_ab.dificuldade_v3 "$@"
    st=$?
    [[ $st -eq 0 ]] && break
    [[ $st -eq 2 ]] || break
    sleep 20
done

echo
if [[ $st -eq 0 ]]; then
    echo "O código acabou de rodar no terminal 🙂"
else
    echo "A execução terminou com pendências (código $st). Repita o mesmo comando para continuar."
fi
echo "Relatório:"
echo "  cat $pasta/DIFICULDADE_V3.md"
echo "Enviar os resultados:"
echo "  bash pipeline/qa_research/enviar_resultados.sh $pasta \"Resultados: dificuldade cognitiva v3\""
echo "Na sua máquina:"
echo "  git pull --ff-only origin codex/qa-evidencias-verificadas"
exit $st
