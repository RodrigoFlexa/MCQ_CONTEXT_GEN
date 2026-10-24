#!/usr/bin/env bash
# Piloto v19 antes da geração final (pipeline/qa_research/TIPOS_QUESTAO.md):
#   1. reauditoria: as aprovadas do teste v18 passam pelo auditor v3 (calibrado); mede quantas continuam e se
#      as 10 removidas na revisão manual seriam reprovadas
#   2. geração completa (sem meta) em 2 documentos novos, em ondas de 1 tópico: prompt v18, auditor v3,
#      refinador com exemplos de reescrita (auditor confere as refinadas contra o texto-fonte), deduplicação
#      por sentido no fim de cada tópico e banco de exemplos limpo
# Uso: bash pipeline/qa_research/rodar_teste_v19.sh [--itens 07_03 03_03] [--saida <pasta>]
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

saida="pipeline/qa_research/relatorios/teste_v19_$(date -u +%Y%m%dT%H%M%SZ)"
itens=(07_03 03_03)
while [[ $# -gt 0 ]]; do
    case "$1" in
        --saida) saida="$2"; shift 2 ;;
        --itens) shift; itens=(); while [[ $# -gt 0 && "$1" != --* ]]; do itens+=("$1"); shift; done ;;
        *) echo "Opção desconhecida: $1"; exit 1 ;;
    esac
done

"$qa_python" -u -m pipeline.qa_research.geracao_tipos reauditar \
    --origem pipeline/qa_research/relatorios/teste_v18_20261024T043655Z/geracao --saida "$saida/reauditoria"
s1=$?
"$qa_python" -u -m pipeline.qa_research.geracao_tipos meta --itens "${itens[@]}" --onda 1 --saida "$saida/geracao"
s2=$?

if [[ $s1 -eq 0 && $s2 -eq 0 ]]; then
    echo
    echo "O código acabou de rodar no terminal :)"
    echo
    echo "Para enviar os resultados (no servidor):"
    echo "  bash pipeline/qa_research/enviar_resultados.sh $saida"
    echo
    echo "Na sua máquina:"
    echo "  git pull"
    echo "  e abra $saida/reauditoria/REAUDITORIA.md e $saida/geracao/RELATORIO.md"
else
    echo
    echo "Algumas unidades falharam. Para tentar só elas:"
    echo "  bash pipeline/qa_research/rodar_teste_v19.sh --itens ${itens[*]} --saida $saida"
fi
