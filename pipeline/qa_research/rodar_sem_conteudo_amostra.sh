#!/usr/bin/env bash
# Apenas avaliação da amostra fixa; não gera questões e não amplia o baseline.
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
saida="pipeline/qa_research/relatorios/sem_conteudo_amostra_1000"
plano=0
args=()
while [[ $# -gt 0 ]]; do
    case "$1" in
        --saida) saida="${2:?Informe a saída}"; shift 2 ;;
        --plano) plano=1; args+=("$1"); shift ;;
        *) args+=("$1"); shift ;;
    esac
done
status=0
"$qa_python" -u -m pipeline.qa_research.sem_conteudo.amostra --saida "$saida" "${args[@]}" || status=$?
if [[ $plano -eq 1 ]]; then exit "$status"; fi
echo
if [[ $status -eq 0 ]]; then
    echo "O código acabou de rodar no terminal :)"
else
    echo "Avaliação incompleta; progresso salvo. Retome com os mesmos parâmetros:"
    printf '  bash pipeline/qa_research/rodar_sem_conteudo_amostra.sh --saida %q' "$saida"
    if [[ ${#args[@]} -gt 0 ]]; then printf ' %q' "${args[@]}"; fi
    echo
fi
echo "Coleta no servidor:"
printf '  cat %q\n' "$saida/avaliacao/ACURACIA.md"
echo "Commit e push dos resultados:"
printf '  git add -- %q\n' "$saida"
printf '  git commit -m %q\n' "Resultados: $(basename "$saida")"
echo "  git push origin codex/qa-evidencias-verificadas"
echo "Coleta local:"
echo "  git pull --ff-only origin codex/qa-evidencias-verificadas"
exit "$status"
