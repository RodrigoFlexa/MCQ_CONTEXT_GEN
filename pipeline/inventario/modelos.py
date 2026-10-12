"""Embedding Azure Large e opções explícitas locais com GPU.

`hash` é um substituto apenas para testes. Sem cross-encoder, o segundo estágio
usa cosseno dos embeddings; não usa outro modelo de embedding implicitamente.
"""
import hashlib
import json
from pathlib import Path

import numpy as np

from .textutil import sha, tokens


class HashEmbedder:
    """Embedding determinístico por n-gramas de caracteres (testes)."""
    name = 'hash'

    def __init__(self, dim=512):
        self.dim = dim

    def encode(self, texts, batch_size=32, desc=None):
        out = np.zeros((len(texts), self.dim), dtype=np.float32)
        for i, t in enumerate(texts):
            s = ' '.join(tokens(t))
            for j in range(max(1, len(s) - 2)):
                h = int(hashlib.md5(s[j:j + 3].encode()).hexdigest()[:8], 16)
                out[i, h % self.dim] += 1.0
        n = np.linalg.norm(out, axis=1, keepdims=True)
        return out / np.maximum(n, 1e-9)


class HashReranker:
    name = 'hash'

    def __init__(self, emb=None):
        self.emb = emb or HashEmbedder()
        self.name = 'cosine' if getattr(self.emb, 'name', 'hash') != 'hash' else 'hash'

    def score(self, query, texts, batch_size=16):
        if not texts:
            return np.zeros(0, dtype=np.float32)
        q = self.emb.encode([query])[0]
        return (self.emb.encode(texts) @ q).astype(np.float32)


GPU_HELP = ("Rode o setup da GPU (PowerShell, na raiz do repositório):\n"
            "    powershell -ExecutionPolicy Bypass -File pipeline/inventario/setup_gpu.ps1\n"
            "e execute o inventário com o Python do ambiente criado (venv_gpu\\Scripts\\python.exe).")


def require_gpu():
    """Falha cedo se não houver CUDA utilizável. Não há fallback para CPU."""
    try:
        import torch
    except ImportError as exc:
        raise RuntimeError('PyTorch não está instalado neste Python.\n' + GPU_HELP) from exc
    if torch.version.cuda is None:
        raise RuntimeError(f'O PyTorch instalado ({torch.__version__}) é a versão só-CPU.\n' + GPU_HELP)
    if not torch.cuda.is_available():
        raise RuntimeError(f'PyTorch {torch.__version__} (CUDA {torch.version.cuda}) não encontrou a GPU: '
                           'verifique o driver NVIDIA (nvidia-smi).\n' + GPU_HELP)
    props = torch.cuda.get_device_properties(0)
    return f"cuda:0 ({props.name}, {props.total_memory / 2**30:.1f} GB, torch {torch.__version__}, CUDA {torch.version.cuda})"


def _device(requested):
    if requested in (None, '', 'auto', 'cuda'):
        require_gpu()
        return 'cuda'
    if requested.startswith('cuda'):
        require_gpu()
        if requested != 'cuda':
            import torch
            try:
                index = int(requested.split(':', 1)[1])
            except (ValueError, IndexError) as exc:
                raise ValueError('Device deve ser cuda ou cuda:N') from exc
            if not 0 <= index < torch.cuda.device_count():
                raise ValueError('Índice CUDA inexistente')
    else:
        raise ValueError('Modelos locais exigem cuda ou cuda:N; não há fallback CPU')
    return requested


class STEmbedder:
    def __init__(self, model_name, device='auto', max_len=1024):
        import torch
        from sentence_transformers import SentenceTransformer
        self.device = _device(device)
        kwargs = {}
        if self.device.startswith('cuda'):
            kwargs['model_kwargs'] = {'torch_dtype': torch.float16}
        self.model = SentenceTransformer(model_name, device=self.device, **kwargs)
        self.model.max_seq_length = max_len
        self.name = model_name

    def encode(self, texts, batch_size=32, desc=None):
        if not texts:
            return np.zeros((0, self.model.get_sentence_embedding_dimension()), dtype=np.float32)
        v = self.model.encode(list(texts), batch_size=batch_size, normalize_embeddings=True,
                              convert_to_numpy=True, show_progress_bar=bool(desc) and len(texts) > 500)
        return v.astype(np.float32)


class STReranker:
    def __init__(self, model_name, device='auto', max_len=768):
        import torch
        from sentence_transformers import CrossEncoder
        self.device = _device(device)
        kwargs = {}
        if self.device.startswith('cuda'):
            kwargs['model_kwargs'] = {'torch_dtype': torch.float16}
        try:
            self.model = CrossEncoder(model_name, device=self.device, max_length=max_len, **kwargs)
        except TypeError:  # versões antigas do sentence-transformers
            self.model = CrossEncoder(model_name, device=self.device, max_length=max_len)
        self.name = model_name

    def score(self, query, texts, batch_size=16):
        if not texts:
            return np.zeros(0, dtype=np.float32)
        s = self.model.predict([(query, t) for t in texts], batch_size=batch_size, show_progress_bar=False)
        s = np.asarray(s, dtype=np.float32).reshape(-1)
        if s.min() < 0 or s.max() > 1:  # logits -> probabilidade
            s = 1 / (1 + np.exp(-s))
        return s


class EmbeddingCache:
    """Cache em disco (npz) de vetores por hash de texto, para retomadas."""

    def __init__(self, path, model_name):
        self.path = Path(path)
        self.model_name = model_name
        self.vectors = {}
        if self.path.exists():
            data = np.load(self.path, allow_pickle=False)
            meta = json.loads(str(data['meta']))
            if meta.get('model') == model_name:
                for k, v in zip(meta['keys'], data['vectors']):
                    self.vectors[k] = v.astype(np.float32) / max(float(np.linalg.norm(v)), 1e-12)
        self.dirty = False

    def encode(self, embedder, texts, batch_size=32):
        keys = [sha(t, 24) for t in texts]
        missing = [i for i, k in enumerate(keys) if k not in self.vectors]
        if missing:
            uniq = {}
            for i in missing:
                uniq.setdefault(keys[i], texts[i])
            vecs = embedder.encode(list(uniq.values()), batch_size=batch_size, desc='emb')
            if len(vecs) != len(uniq) or not np.isfinite(vecs).all():
                raise ValueError('Resposta de embeddings incompleta ou inválida')
            for k, v in zip(uniq.keys(), vecs):
                self.vectors[k] = v
            self.dirty = True
        if not texts:
            return np.zeros((0, 1), dtype=np.float32)
        return np.stack([self.vectors[k] for k in keys]).astype(np.float32)

    def save(self):
        if not self.dirty or not self.vectors:
            return
        keys = list(self.vectors)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.path.with_name(self.path.stem + '.tmp.npz')
        np.savez(tmp, vectors=np.stack([self.vectors[k] for k in keys]).astype(np.float32),
                 meta=json.dumps({'model': self.model_name, 'keys': keys}))
        tmp.replace(self.path)
        self.dirty = False


class AzureEmbedder:
    """Adapta o backend integral e persistente já usado na fase_4."""
    name = 'embedding-3-large-global'
    device = 'azure'

    def __init__(self, output, backend=None, tokenizer=None):
        from pipeline.fase_4.config import QAConfig
        from pipeline.fase_4.azure_embeddings import AzureFullTextEmbedder
        cfg = QAConfig(output=Path(output))
        cfg.validate()
        self.impl = AzureFullTextEmbedder(cfg, backend=backend, tokenizer=tokenizer)

    def encode(self, texts, batch_size=32, desc=None):
        return self.impl.encode(texts, batch_size=batch_size)

    def close(self):
        self.impl.close()


def load_models(embedder_name, reranker_name, device='cuda', output=None):
    if embedder_name == 'hash':
        emb = HashEmbedder()
        return emb, HashReranker(emb)
    if embedder_name == 'embedding-3-large-global':
        if output is None:
            raise ValueError('Azure embeddings exige uma pasta de saída')
        emb = AzureEmbedder(output)
    else:
        emb = STEmbedder(embedder_name, device)
    try:
        rr = HashReranker(emb) if reranker_name in (None, '', 'none') else STReranker(reranker_name, device)
    except BaseException:
        if hasattr(emb, 'close'):
            emb.close()
        raise
    return emb, rr
