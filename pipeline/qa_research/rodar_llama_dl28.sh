#!/usr/bin/env bash
# Respostas dos modelos Llama às questões do banco final (sem e com documento), com vLLM nas GPUs 6 e 7 da DL-28.
# O juiz roda depois no servidor (python -m pipeline.qa_research.experimento_ab avaliar-externos).
#
# Uso (na raiz do repositório MCQ_CONTEXT_GEN, na DL-28):
#   bash pipeline/qa_research/rodar_llama_dl28.sh                 # 8B e 70B
#   bash pipeline/qa_research/rodar_llama_dl28.sh llama-3-1-8b    # só um modelo
#   TESTE=20 bash pipeline/qa_research/rodar_llama_dl28.sh llama-3-1-8b   # teste rápido com 20 questões
# Variáveis: GPUS (padrão 6,7), PY (python do ambiente com vLLM), HF_TOKEN (modelos meta-llama exigem licença aceita).
# Repetir o comando continua de onde parou.
set -uo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.."
export CUDA_VISIBLE_DEVICES="${GPUS:-6,7}"
export PYTHONUTF8=1 VLLM_WORKER_MULTIPROC_METHOD=spawn
py="${PY:-python}"
if [[ $# -gt 0 ]]; then modelos=("$@"); else modelos=(llama-3-1-8b llama-3-3-70b); fi

echo "GPUs visíveis: $CUDA_VISIBLE_DEVICES"
nvidia-smi --query-gpu=index,name,memory.used,memory.total --format=csv -i "$CUDA_VISIBLE_DEVICES" || true
for m in "${modelos[@]}"; do
    echo "[$(date +%H:%M:%S)] $m"
    extra=()
    [[ -n "${TESTE:-}" ]] && extra+=(--limite "$TESTE")
    "$py" -u pipeline/qa_research/experimento_ab/responder_vllm.py "$m" ${extra[@]+"${extra[@]}"} || {
        echo "Falhou em $m. Repita o mesmo comando para continuar."; exit 2; }
done

echo
echo "O código acabou de rodar no terminal :)"
echo
echo "Resultados:"
for m in "${modelos[@]}"; do echo "  cat pipeline/qa_research/relatorios/respostas_externas/$m.meta.json"; done
echo "Enviar ao GitHub:"
echo "  git add pipeline/qa_research/relatorios/respostas_externas"
echo "  git commit -m \"Respostas dos modelos Llama (vLLM, DL-28)\""
echo "  git pull --rebase origin codex/qa-evidencias-verificadas && git push origin HEAD:codex/qa-evidencias-verificadas"
echo "Depois, no servidor Petrobras:"
echo "  git pull --ff-only origin codex/qa-evidencias-verificadas"
echo "  bash pipeline/qa_research/rodar_experimento_ab.sh externos"
