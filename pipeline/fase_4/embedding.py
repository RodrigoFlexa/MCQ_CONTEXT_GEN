"""Representa textos completos por janelas de tokens, sem alterar a fase 3."""
import hashlib
import json
from pathlib import Path

import numpy as np
from .domain import legacy
from .storage import atomic_json


class FullTextEmbedder(legacy.Embedder):
    def __init__(self, cfg, overlap=16):
        super().__init__(cfg)
        self.overlap = overlap
        self.window = int(self.model.max_seq_length) - self.model.tokenizer.num_special_tokens_to_add(False) - 8
        if self.window <= self.overlap:
            raise ValueError("Janela de embeddings deve exceder a sobreposição")
        config = self.model[0].auto_model.config
        import torch
        weights=hashlib.sha256()
        for name,tensor in sorted(self.model.state_dict().items()):
            weights.update(json.dumps([name,str(tensor.dtype),list(tensor.shape)]).encode())
            weights.update(tensor.detach().cpu().contiguous().reshape(-1).view(torch.uint8).numpy().tobytes())
        tokenizer_signature=hashlib.sha256(json.dumps(self.model.tokenizer.get_vocab(),sort_keys=True,
                                                      ensure_ascii=False).encode()).hexdigest()
        self.protocol = {"name":cfg.modelo_embedding, "revision":getattr(config, '_commit_hash', None),
            'weights_sha256':weights.hexdigest(),'tokenizer_vocab_sha256':tokenizer_signature,
            "max_tokens":int(self.model.max_seq_length), "window":self.window,
            "overlap":overlap, "aggregation":"mean_weighted_new_tokens_l2_v1"}
        manifest=Path(cfg.out_dir)/'embeddings/protocolo.json'
        if manifest.exists() and json.loads(manifest.read_text(encoding='utf-8')) != self.protocol:
            raise ValueError("Modelo ou representação de embeddings mudou; use outra saída")
        if self._cache and not manifest.exists():
            raise ValueError("Cache antigo sem protocolo; use outra saída")
        atomic_json(manifest,self.protocol)

    def windows(self, text):
        # Aqui somente contamos/dividimos tokens; o texto integral não vai ao modelo.
        ids=self.model.tokenizer.encode(text,add_special_tokens=False,truncation=False,verbose=False)
        if len(ids)<=self.window:
            return [text],[max(1,len(ids))]
        pieces, weights=[],[]
        step=self.window-self.overlap
        for start in range(0,len(ids),step):
            part=ids[start:start+self.window]
            pieces.append(self.model.tokenizer.decode(part,skip_special_tokens=True))
            weights.append(len(part) if start==0 else max(1,len(part)-self.overlap))
            if start+self.window>=len(ids):
                break
        return pieces,weights

    def encode(self,textos,batch_size=64,usar_cache=True,progresso=False):
        texts=list(textos)
        if not texts:
            return np.zeros((0,self.dim),dtype=np.float32)
        keys=[hashlib.sha256(t.encode()).hexdigest() for t in texts]
        missing=list(dict.fromkeys(k for k in keys if not usar_cache or k not in self._cache))
        lookup=dict(zip(keys,texts))
        pieces, groups=[],[]
        for key in missing:
            parts,weights=self.windows(lookup[key]);start=len(pieces);pieces.extend(parts)
            groups.append((key,start,len(parts),weights))
        if pieces:
            # encode de texto decodificado pode alterar a tokenização: nunca cortar silenciosamente.
            for part in pieces:
                if len(self.model.tokenizer.encode(part,add_special_tokens=True,truncation=False,verbose=False))>self.model.max_seq_length:
                    raise ValueError("Janela re-tokenizada excede o modelo; ajuste a estratégia")
            vectors=np.asarray(self.model.encode(pieces,batch_size=batch_size,
                normalize_embeddings=True,show_progress_bar=progresso),dtype=np.float32)
            for key,start,n,weights in groups:
                vec=np.average(vectors[start:start+n],axis=0,weights=weights)
                self._cache[key]=np.asarray(vec/max(float(np.linalg.norm(vec)),1e-12),dtype=np.float32)
        return np.stack([self._cache[k] for k in keys])

    def diagnostics(self,text):
        n=len(self.model.tokenizer.encode(text,add_special_tokens=False,truncation=False,verbose=False))
        return {'tokens':n,'windows':len(self.windows(text)[0]),'silently_truncated':False}
