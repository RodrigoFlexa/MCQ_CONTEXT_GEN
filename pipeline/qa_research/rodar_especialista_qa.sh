#!/usr/bin/env bash
# Converte o MCQ, mantém somente QAs válidas e executa os dois respondentes em paralelo.
set -euo pipefail
export PYTHONUTF8=1
qa_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd)"
cd -- "$qa_root"
qa_python="${DOCUMENT_PYTHON:-$qa_root/.venv-documento/bin/python}"
if [[ ! -x "$qa_python" ]]; then
    if [[ -n "${DOCUMENT_PYTHON:-}" ]]; then echo "DOCUMENT_PYTHON não é executável: $qa_python"; exit 1; fi
    qa_python="$qa_root/venv/bin/python"
    if [[ ! -x "$qa_python" ]]; then qa_python="$(command -v python3)"; fi
fi
saida="pipeline/qa_research/relatorios/especialista_qa_$(date -u +%Y%m%dT%H%M%SZ)"
avaliar=1
so_avaliacao=0
plano=0
lote_juiz=8
conversao=converter
args=()
while [[ $# -gt 0 ]]; do
    case "$1" in
        --saida) saida="${2:?Informe a saída}"; shift 2 ;;
        --sem-avaliacao) avaliar=0; shift ;;
        --so-avaliacao) so_avaliacao=1; shift ;;
        --lote-juiz) lote_juiz="${2:?Informe o lote}"; shift 2 ;;
        --revisadas-v3) conversao=refinar-revisadas; shift ;;
        --plano) plano=1; args+=("$1"); shift ;;
        *) args+=("$1"); shift ;;
    esac
done
if [[ $so_avaliacao -eq 1 && ( $avaliar -eq 0 || $plano -eq 1 ) ]]; then
    echo "--so-avaliacao não pode ser combinado com --sem-avaliacao ou --plano."; exit 1
fi
status=0
if [[ $so_avaliacao -eq 0 ]]; then
    "$qa_python" -u -m pipeline.qa_research.especialista_qa "$conversao" --saida "$saida" "${args[@]}" || status=$?
fi
if [[ $plano -eq 1 ]]; then exit "$status"; fi
if [[ $status -eq 0 && $avaliar -eq 1 ]]; then
    "$qa_python" -u -m pipeline.qa_research.especialista_qa avaliar --saida "$saida" --lote-juiz "$lote_juiz" || status=$?
fi
echo
if [[ $status -eq 0 ]]; then
    echo "O código acabou de rodar no terminal :)"
else
    echo "Execução incompleta. Consulte $saida/RELATORIO.md e as pastas de falhas."
    if [[ "$conversao" == refinar-revisadas ]]; then
        printf 'Retomada: bash pipeline/qa_research/rodar_especialista_qa.sh --revisadas-v3 --saida %q\n' "$saida"
    else
        printf 'Retomada: bash pipeline/qa_research/rodar_especialista_qa.sh --saida %q\n' "$saida"
    fi
fi
echo "Coleta no servidor:"
printf '  cat %q %q\n' "$saida/RELATORIO.md" "$saida/resultado.json"
if [[ $avaliar -eq 1 ]]; then
    echo "Acurácia e cobertura por modelo (bloqueios aparecem separados):"
    printf '  cat %q\n' "$saida/avaliacao/ACURACIA.md"
fi
echo "Commit e push dos resultados:"
printf '  git add -- %q\n' "$saida"
printf '  git commit -m %q\n' "Resultados: $(basename "$saida")"
echo "  git push origin codex/qa-evidencias-verificadas"
echo "Na máquina local: git pull --ff-only origin codex/qa-evidencias-verificadas"
echo "Gráficos depois de coletar a run (Python de análise com E5 local):"
printf '  python -m pipeline.qa_research.especialista_qa graficos --saida %q\n' "$saida"
exit "$status"
