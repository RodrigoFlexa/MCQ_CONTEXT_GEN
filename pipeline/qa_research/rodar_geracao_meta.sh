#!/usr/bin/env bash
# Geração completa, v21 (pipeline/qa_research/TIPOS_QUESTAO.md): gera o que cada documento sustenta, sem meta.
#   1. inventário: relações por bloco e até 25 encadeamentos por documento (reaproveitados quando já existem)
#   2. em ondas de 5 tópicos: compostas (uma por encadeamento), janelas (uma passagem por janela, prompt v18) e
#      auditor v3; depois, refinador forte (gpt-5-4 high, prompt refinador_v3) em todas as reprovadas, com as
#      questões já aprovadas sobre os mesmos blocos, em até 2 tentativas, cada uma seguida de nova auditoria;
#      entre ondas, as aprovadas viram exemplos e as reprovadas contraexemplos (banco herdado da v16, v18 e v19)
#   3. deduplicação por sentido em cada tópico, RELATORIO.md, aprovadas.jsonl e exemplos_proposto.json
# Uso: bash pipeline/qa_research/rodar_geracao_meta.sh [opções]
#   padrão: um tópico por área (01_01 02_03 03_01 04_02 05_02 06_05 07_04 08_03 09_02 10_01)
#   ex.: --itens todos                                       (os 40 tópicos)
#        --itens 08_02 --saida <pasta de teste>              (teste barato)
#        --meta 100                                          (opcional: rodadas extras até 100 válidas por tópico)
#        --saida <pasta>                                     (retoma uma execução interrompida)
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

saida=""
args=("$@")
for ((i = 0; i < ${#args[@]}; i++)); do
    if [[ "${args[$i]}" == "--saida" ]]; then saida="${args[$((i + 1))]}"; fi
done
if [[ -z "$saida" ]]; then
    saida="pipeline/qa_research/relatorios/geracao_meta_$(date -u +%Y%m%dT%H%M%SZ)"
    args+=("--saida" "$saida")
fi

"$qa_python" -u -m pipeline.qa_research.geracao_tipos meta "${args[@]}"
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
    echo "  bash pipeline/qa_research/rodar_geracao_meta.sh --saida $saida"
fi
exit $status
