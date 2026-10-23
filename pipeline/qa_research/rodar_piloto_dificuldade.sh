#!/usr/bin/env bash
# Piloto de dificuldade v2 (rubrica em pipeline/qa_research/DIFICULDADE_V2.md): inventário x EC v13.
#   1. relações por bloco: reaproveitadas da rodada piloto_inventario_20261023T042252Z
#   2. encadeamentos por documento (gpt-5-4-petrobras:high), base das difíceis B
#   3-4. inventário: 10 fáceis, 10 médias e uma difícil por janela EC por documento (metade A, metade B),
#        com reservas usadas só quando o gerador declara um alvo insuficiente
#   5. EC v13: janelas de 3 blocos (todas do 01_01 e 36 do 02_02), 1 fácil, 2 médias e 1 difícil por janela
#   6. gpt-4-1-nano-petrobras e gpt-5-4-nano-petrobras:low respondem sem contexto; gpt-5-4-petrobras:high julga
#   7. RELATORIO.md: acurácia por método e dificuldade, atalho genérico, filtro simulado e histórico da v1
# Uso: bash pipeline/qa_research/rodar_piloto_dificuldade.sh [opções]
#   ex.: --limite-blocos 6 --faceis 1 --medias 1 --dificeis 2 --ec-janelas 2 --saida <pasta de teste>
#        --saida <pasta>      (retoma uma execução interrompida, com a configuração gravada)
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

dados=pipeline/qa_references/data
if [[ ! -s $dados/qa_examples_revisados.jsonl && ! -s $dados/qa_examples_limpos.jsonl ]]; then
    echo "Exemplos externos ainda não preparados. Rode antes:"
    echo "  bash pipeline/qa_research/rodar_preparar_exemplos.sh"
    exit 1
fi

saida=""
args=("$@")
for ((i = 0; i < ${#args[@]}; i++)); do
    if [[ "${args[$i]}" == "--saida" ]]; then saida="${args[$((i + 1))]}"; fi
done
if [[ -z "$saida" ]]; then
    saida="pipeline/qa_research/relatorios/piloto_dificuldade_$(date -u +%Y%m%dT%H%M%SZ)"
    args+=("--saida" "$saida")
fi

"$qa_python" -u -m pipeline.qa_research.inventario_docs run "${args[@]}"
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
    echo "  bash pipeline/qa_research/rodar_piloto_dificuldade.sh --saida $saida"
fi
exit $status
