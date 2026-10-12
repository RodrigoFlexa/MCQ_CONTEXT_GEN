"""Valida a GPU com os modelos reais do inventário (bge-m3 e bge-reranker-v2-m3).

    venv_gpu\\Scripts\\python.exe pipeline/inventario/check_gpu.py
"""
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from pipeline.inventario.modelos import STEmbedder, STReranker, require_gpu  # noqa: E402


def main(embedder='BAAI/bge-m3', reranker='BAAI/bge-reranker-v2-m3'):
    try:
        print('[gpu]', require_gpu(), flush=True)
    except RuntimeError as exc:
        print('[gpu] ERRO:', exc)
        sys.exit(1)
    import torch
    q = 'gestão de backlog de manutenção em FPSO'
    docs = ['The maintenance backlog should be prioritised by safety criticality and its age monitored.',
            'O backlog de manutenção corresponde às ordens pendentes, priorizadas por criticidade.',
            'Na distribuição de gasolina, o preço inclui a margem de revenda do posto.']
    t = time.time()
    emb = STEmbedder(embedder, 'cuda')
    rr = STReranker(reranker, 'cuda')
    print(f'[modelos] carregados em {time.time() - t:.0f}s', flush=True)
    v = emb.encode([q] + docs)
    dense = v[1:] @ v[0]
    scores = rr.score(q, docs)
    print('[teste] denso  :', [round(float(x), 3) for x in dense])
    print('[teste] rerank :', [round(float(x), 3) for x in scores])
    t = time.time()
    emb.encode([docs[0] * 20] * 512, batch_size=64)
    torch.cuda.synchronize()
    print(f'[desempenho] 512 trechos longos vetorizados em {time.time() - t:.1f}s '
          f'(memória máx. {torch.cuda.max_memory_allocated() / 2**30:.1f} GB)')
    ok = scores[0] > 0.5 and scores[1] > 0.5 and scores[2] < 0.2
    print('[resultado]', 'OK' if ok else 'ATENÇÃO: scores inesperados')
    sys.exit(0 if ok else 2)


if __name__ == '__main__':
    main()
