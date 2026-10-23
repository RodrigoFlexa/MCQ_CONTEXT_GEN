#!/usr/bin/env bash
# Piloto: inventário leve (estilo qa_v7) x configuração EC, com avaliação cega.
#   1. relações por bloco (gpt-5-4-petrobras:low) nos documentos 01_01 e 02_02
#   2. combinações de relações por documento (gpt-5-4-petrobras:high)
#   3-4. 100 questões a partir do inventário (25% fáceis, 50% médias, 25% difíceis A e B)
#   5. 100 questões sorteadas da configuração EC, na mesma proporção
#   6. gpt-4-1-nano-petrobras responde sem contexto; gpt-5-4-petrobras:high julga contra a referência
#   7. RELATORIO.md com a acurácia por método e dificuldade
# Uso: bash pipeline/qa_research/rodar_piloto_inventario.sh [opções]
#   ex.: --limite-blocos 6 --total 8 --saida <pasta de teste>   (teste rápido e barato)
#        --saida <pasta>                                         (retoma uma execução interrompida)
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
    saida="pipeline/qa_research/relatorios/piloto_inventario_$(date -u +%Y%m%dT%H%M%SZ)"
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
    echo "  bash pipeline/qa_research/rodar_piloto_inventario.sh --saida $saida"
fi
exit $status
