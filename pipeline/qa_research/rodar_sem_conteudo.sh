#!/usr/bin/env bash
# Geração sem documentos, seguida da mesma avaliação dos seis modelos da run final.
# Repetir --saida retoma. --plano não chama modelos. --sem-avaliacao gera somente.
set -euo pipefail
export PYTHONUTF8=1
qa_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd)"
cd -- "$qa_root"
qa_python="${DOCUMENT_PYTHON:-$qa_root/.venv-documento/bin/python}"
if [[ ! -x "$qa_python" ]]; then
    if [[ -n "${DOCUMENT_PYTHON:-}" ]]; then
        echo "DOCUMENT_PYTHON não é executável: $qa_python"; exit 1
    fi
    qa_python="$qa_root/venv/bin/python"
    if [[ ! -x "$qa_python" ]]; then qa_python="$(command -v python3)"; fi
fi
saida="pipeline/qa_research/relatorios/sem_conteudo_$(date -u +%Y%m%dT%H%M%SZ)"
avaliar=1
so_avaliacao=0
plano=0
lote_juiz=8
args=()
while [[ $# -gt 0 ]]; do
    case "$1" in
        --saida) saida="${2:?Informe a pasta de saída}"; shift 2 ;;
        --sem-avaliacao) avaliar=0; shift ;;
        --so-avaliacao) so_avaliacao=1; shift ;;
        --lote-juiz) lote_juiz="${2:?Informe o tamanho do lote}"; shift 2 ;;
        --plano) plano=1; args+=("$1"); shift ;;
        *) args+=("$1"); shift ;;
    esac
done
if [[ $so_avaliacao -eq 1 && ( $avaliar -eq 0 || $plano -eq 1 ) ]]; then
    echo "--so-avaliacao não pode ser combinado com --sem-avaliacao ou --plano."; exit 1
fi
echo "Saída: $saida"
status=0
if [[ $so_avaliacao -eq 0 ]]; then
    "$qa_python" -u -m pipeline.qa_research.sem_conteudo --saida "$saida" "${args[@]}" || status=$?
fi
if [[ $plano -eq 1 ]]; then exit "$status"; fi
if [[ $status -eq 0 && $avaliar -eq 1 ]]; then
    if [[ ! -f "$saida/geracao_concluida.json" ]]; then
        echo "A avaliação requer geração concluída com todas as metas atingidas."; exit 2
    fi
    "$qa_python" -u -m pipeline.qa_research.geracao_tipos avaliar --saida "$saida" --lote-juiz "$lote_juiz" || status=$?
fi
echo
if [[ $status -eq 0 ]]; then
    echo "O código acabou de rodar no terminal :)"
else
    echo "Execução incompleta. Veja $saida/RELATORIO.md. Retome com a mesma saída:"
    printf '  bash pipeline/qa_research/rodar_sem_conteudo.sh --saida %q\n' "$saida"
    echo "Se um limite foi atingido, aumente --max-lotes, --max-sem-progresso ou --max-chamadas."
fi
echo
echo "Coleta no servidor (resumo e questões):"
printf '  cat %q %q\n' "$saida/RELATORIO.md" "$saida/resultado.json"
echo "Commit e push dos resultados no servidor:"
printf '  git add -- %q\n' "$saida"
printf '  git commit -m %q\n' "Resultados: $(basename "$saida")"
echo "  git push origin codex/qa-evidencias-verificadas"
echo "Coleta na máquina local:"
echo "  git pull --ff-only origin codex/qa-evidencias-verificadas"
exit "$status"
