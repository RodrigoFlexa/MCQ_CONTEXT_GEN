#!/usr/bin/env bash
# Teste dos sistemas v18 antes da geração final (pipeline/qa_research/TIPOS_QUESTAO.md):
#   1. reauditoria: as 1.038 aprovadas da v16 passam pelo auditor v2 (com motivo); mede quantas continuam
#      aprovadas e se as 13 removidas na revisão manual seriam reprovadas
#   2. geração completa (sem meta) em 2 documentos novos, em ondas de 1 tópico, com prompt v18, auditor v2,
#      refinador (gpt-5-mini) e banco de exemplos/contraexemplos; espera-se ~100 questões válidas
# Uso: bash pipeline/qa_research/rodar_teste_v18.sh [--itens 05_01 06_01] [--saida <pasta>]
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

saida="pipeline/qa_research/relatorios/teste_v18_$(date -u +%Y%m%dT%H%M%SZ)"
itens=(05_01 06_01)
while [[ $# -gt 0 ]]; do
    case "$1" in
        --saida) saida="$2"; shift 2 ;;
        --itens) shift; itens=(); while [[ $# -gt 0 && "$1" != --* ]]; do itens+=("$1"); shift; done ;;
        *) echo "Opção desconhecida: $1"; exit 1 ;;
    esac
done

"$qa_python" -u -m pipeline.qa_research.geracao_tipos reauditar --saida "$saida/reauditoria"
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
    echo "  bash pipeline/qa_research/rodar_teste_v18.sh --itens ${itens[*]} --saida $saida"
fi
