#!/usr/bin/env bash
# Geração final (v21) dos 40 tópicos e, depois dela, a avaliação dos modelos (pipeline/qa_research/TIPOS_QUESTAO.md).
#   1. geração (subcomando meta): ondas de 5 tópicos, refinador forte, deduplicação; cada tópico pronto grava
#      topicos/<item>/aprovadas.jsonl e finalizado.json
#   2. avaliação, só depois que a geração termina sem falhas: respostas sem contexto, em pares de modelos (os dois
#      do par ao mesmo tempo, um par depois do outro):
#        gpt-5-4-nano + gpt-5-4  ->  gpt-5 + gpt-5-nano  ->  gpt-4-1 + gpt-4-1-nano
#      esforço low (os gpt-4-1 não têm esforço); juiz gpt-5-4 medium em lotes de 8 respostas; a cada bloco de 80
#      questões a tabela <saida>/avaliacao/ACURACIA.md é regravada (geral, por tipo e por composição)
# Uso: bash pipeline/qa_research/rodar_geracao_final.sh [--saida <pasta>] [--itens todos] [--lote-juiz 8] [--so-avaliacao]
#   repetir com a mesma --saida retoma de onde parou (geração e avaliação)
# Tabela durante a avaliação, em outro terminal:
#   python -m pipeline.qa_research.geracao_tipos acuracia <saida>      (ou: cat <saida>/avaliacao/ACURACIA.md)
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

saida="pipeline/qa_research/relatorios/geracao_final_$(date -u +%Y%m%dT%H%M%SZ)"
itens=(todos)
lote_juiz=8
so_avaliacao=0
while [[ $# -gt 0 ]]; do
    case "$1" in
        --saida) saida="$2"; shift 2 ;;
        --lote-juiz) lote_juiz="$2"; shift 2 ;;
        --so-avaliacao) so_avaliacao=1; shift ;;
        --itens) shift; itens=(); while [[ $# -gt 0 && "$1" != --* ]]; do itens+=("$1"); shift; done ;;
        *) echo "Opção desconhecida: $1"; exit 1 ;;
    esac
done

echo "Saída: $saida"
s1=0
if [[ $so_avaliacao -eq 0 ]]; then
    "$qa_python" -u -m pipeline.qa_research.geracao_tipos meta --itens "${itens[@]}" --saida "$saida"
    s1=$?
fi
s2=0
if [[ $s1 -eq 0 ]]; then
    echo
    echo "== Avaliação dos modelos (tabela: python -m pipeline.qa_research.geracao_tipos acuracia $saida)"
    "$qa_python" -u -m pipeline.qa_research.geracao_tipos avaliar --saida "$saida" --lote-juiz "$lote_juiz"
    s2=$?
fi

echo
if [[ $s1 -eq 0 && $s2 -eq 0 ]]; then
    echo "O código acabou de rodar no terminal :)"
elif [[ $s1 -ne 0 ]]; then
    echo "A geração teve unidades com falha; a avaliação só começa quando ela terminar sem falhas. Para tentar só elas:"
    echo "  bash pipeline/qa_research/rodar_geracao_final.sh --saida $saida --itens ${itens[*]}"
else
    echo "A avaliação teve unidades com falha. Para tentar só elas:"
    echo "  bash pipeline/qa_research/rodar_geracao_final.sh --saida $saida --so-avaliacao"
fi
echo
echo "Para enviar os resultados (no servidor; pode ser feito também no meio da execução):"
echo "  bash pipeline/qa_research/enviar_resultados.sh $saida"
echo
echo "Na sua máquina:"
echo "  git pull"
echo "  e abra $saida/RELATORIO.md e $saida/avaliacao/ACURACIA.md"
