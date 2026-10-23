#!/usr/bin/env bash
# Experimento de exemplos externos, modo junto, composição exata (1 fácil, 2 médias, 1 difícil),
# nas mesmas 40 janelas dos experimentos anteriores:
#   E  = 6 exemplos externos limpos (2 Pirá, 2 MMMLU PT-BR, 1 ARC-Challenge, 1 QASC)
#   EC = E + 3 questões do especialista, apresentadas como questões já geradas, a não imitar
# Uso: bash pipeline/qa_research/rodar_experimento_externos.sh [opções]
#   ex.: --limite 2            (teste rápido: 2 focos por item em cada braço, 8 chamadas)
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

dados=pipeline/qa_references/data
if [[ ! -s $dados/qa_examples_revisados.jsonl && ! -s $dados/qa_examples_limpos.jsonl ]]; then
    echo "Exemplos externos ainda não preparados. Rode antes:"
    echo "  bash pipeline/qa_research/rodar_preparar_exemplos.sh"
    exit 1
fi
if [[ ! -s $dados/qa_examples_revisados.jsonl ]]; then
    echo "AVISO: usando os exemplos limpos só por regras (sem revisão por LLM)."
fi

saida=""
args=("$@")
for ((i = 0; i < ${#args[@]}; i++)); do
    if [[ "${args[$i]}" == "--saida" ]]; then saida="${args[$((i + 1))]}"; fi
done
if [[ -z "$saida" ]]; then
    saida="pipeline/qa_research/relatorios/experimento_externos_$(date -u +%Y%m%dT%H%M%SZ)"
    args+=("--saida" "$saida")
fi

"$qa_python" -u -m pipeline.qa_research.piloto_janela externos "${args[@]}"
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
    echo "  bash pipeline/qa_research/rodar_experimento_externos.sh --saida $saida"
fi
exit $status
