"""Busca semântica local; o escore seleciona vizinhos, não determina descarte."""
import numpy as np
from pathlib import Path
from pipeline.inventario.textutil import atomic_json,read_json
from pipeline.qa_research.v3.runtime import digest


class Similarity:
    def __init__(self,directory,encoder=None):
        if encoder is None:
            from pipeline.qa_research.selection import LocalE5
            encoder=LocalE5(Path(directory)/'.local',offline=True)
        self.encoder=encoder
        self.protocol=dict(encoder=encoder.protocol,agregacao='query windows 300 chars; media normalizada; sem truncar')
        self.path=Path(directory)/'.local'/('vetores_'+digest(self.protocol)+'.json')
        self.cache=read_json(self.path) or {}

    def vectors(self,texts):
        for i,text in enumerate(dict.fromkeys(texts),1):
            key=digest(text)
            if key in self.cache:continue
            parts=[];current=''
            for word in text.split():
                if len(word)>300:raise ValueError('Palavra excede janela semântica')
                if len(current)+len(word)+1>300:parts.append(current);current=''
                current=(current+' '+word).strip()
            if current:parts.append(current)
            if not parts:raise ValueError('Texto vazio para similaridade')
            v=np.asarray(self.encoder.queries(parts),dtype=float).mean(axis=0)
            norm=np.linalg.norm(v)
            if not np.isfinite(v).all() or norm<=0:raise ValueError('Embedding inválido')
            self.cache[key]=(v/norm).tolist()
            if i%200==0:print(f'[similaridade local] {i}/{len(texts)} enunciados preparados',flush=True)
        return np.asarray([self.cache[digest(t)] for t in texts])

    def nearest(self,text,bank,limit):
        if not bank or limit<=0:return []
        scores=self.vectors([q['pergunta'] for q in bank])@self.vectors([text])[0]
        order=sorted(range(len(bank)),key=lambda i:(-scores[i],bank[i]['id']))[:limit]
        return [dict(bank[i],similaridade=float(scores[i])) for i in order]

    def close(self):
        atomic_json(self.path,self.cache);self.encoder.close()


def prepare_model():
    from huggingface_hub import snapshot_download
    from pipeline.qa_research.selection import LOCAL_MODEL,LOCAL_REVISION
    snapshot_download(repo_id=LOCAL_MODEL,revision=LOCAL_REVISION)
    print('Modelo semântico preparado. Nenhum dataset de questões foi alterado.')


if __name__=='__main__':prepare_model()
