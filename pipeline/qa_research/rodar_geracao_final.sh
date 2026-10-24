#!/usr/bin/env bash
# Geração final (v21) dos 40 tópicos com avaliação dos modelos em paralelo (pipeline/qa_research/TIPOS_QUESTAO.md).
#   1. geração (rodar_geracao_meta.sh): em ondas de 5 tópicos; ao fim de cada onda os tópicos ficam prontos
#      (topicos/<item>/aprovadas.jsonl e finalizado.json)
#   2. avaliação, em paralelo: a cada 2 minutos pega os tópicos prontos, responde sem contexto com
#      gpt-5-4-nano, gpt-5-4, gpt-5, gpt-5-nano (esforço low), gpt-4-1 e gpt-4-1-nano (sem esforço), julga em
#      lotes de 8 respostas (juiz gpt-5-4 medium) e regrava <saida>/avaliacao/ACURACIA.md
# Uso: bash pipeline/qa_research/rodar_geracao_final.sh [--saida <pasta>] [--itens todos] [--lote-juiz 8]
#   repetir com a mesma --saida retoma de onde parou (geração e avaliação)
# Tabela durante a execução, em outro terminal:
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
while [[ $# -gt 0 ]]; do
    case "$1" in
        --saida) saida="$2"; shift 2 ;;
        --lote-juiz) lote_juiz="$2"; shift 2 ;;
        --itens) shift; itens=(); while [[ $# -gt 0 && "$1" != --* ]]; do itens+=("$1"); shift; done ;;
        *) echo "Opção desconhecida: $1"; exit 1 ;;
    esac
done

mkdir -p "$saida/avaliacao"
rm -f "$saida/geracao_encerrada"
echo "Saída: $saida"
echo "Avaliação em paralelo; log em $saida/avaliacao/log.txt"
echo "Tabela de acurácia (outro terminal): python -m pipeline.qa_research.geracao_tipos acuracia $saida"
"$qa_python" -u -m pipeline.qa_research.geracao_tipos avaliar --saida "$saida" --esperar --lote-juiz "$lote_juiz" \
    > "$saida/avaliacao/log.txt" 2>&1 &
pid_avaliacao=$!

"$qa_python" -u -m pipeline.qa_research.geracao_tipos meta --itens "${itens[@]}" --saida "$saida"
s1=$?
touch "$saida/geracao_encerrada"
echo
echo "Geração terminou (código $s1). Aguardando a avaliação dos últimos tópicos..."
wait "$pid_avaliacao"
s2=$?
tail -n 3 "$saida/avaliacao/log.txt"

echo
if [[ $s1 -eq 0 && $s2 -eq 0 ]]; then
    echo "O código acabou de rodar no terminal :)"
else
    echo "Algumas unidades falharam (geração $s1, avaliação $s2). Para tentar só elas:"
    echo "  bash pipeline/qa_research/rodar_geracao_final.sh --saida $saida --itens ${itens[*]}"
fi
echo
echo "Para enviar os resultados (no servidor; pode ser feito também no meio da execução):"
echo "  bash pipeline/qa_research/enviar_resultados.sh $saida"
echo
echo "Na sua máquina:"
echo "  git pull"
echo "  e abra $saida/RELATORIO.md e $saida/avaliacao/ACURACIA.md"
