"""Mesmo protocolo lexical do Default; grupos pareados por tamanho e estrato."""
import random
import re
import statistics
import unicodedata
from collections import defaultdict
from pathlib import Path
from pipeline.inventario.textutil import atomic_json
from pipeline.qa_research.v3.runtime import digest
from .generate import jsonl


def tokens(text):
    return re.findall(r'[^\W\d_]+(?:[-’\'][^\W\d_]+)*', unicodedata.normalize('NFC',text).lower(), re.UNICODE)


def grams(ts, n): return set(zip(*(ts[i:] for i in range(n))))


def lcs(a,b):
    masks={}
    for i,t in enumerate(a):masks[t]=masks.get(t,0)|(1<<i)
    state=0
    for t in b:
        x=masks.get(t,0)|state;state=x&~(x-((state<<1)|1))
    return state.bit_count()


def rouge(a,b): return 2*lcs(a,b)/(len(a)+len(b)) if a and b else 0.


def measure(q, stopwords):
    qt=tokens(q['pergunta']);at=tokens(q['resposta']);clean=[t for t in qt if t not in stopwords];qs=set(clean)
    bodies=[b['texto'] for b in q['blocos_contexto']]
    sentences=[s for body in bodies for s in re.split(r'(?<=[.!?;])\s+|\n+',body) if s.strip()]
    raw=[tokens(s) for s in sentences];content=[[t for t in s if t not in stopwords] for s in raw]
    ctx={t for body in bodies for t in tokens(body) if t not in stopwords}
    result=dict(uid=q['uid'],grupo=q['grupo'],item=q['item'],tipo=q['tipo'],
        overlap_q_c=len(qs&ctx)/len(qs) if qs else None,
        max_rougeL_f1_sem_stop=max((rouge(clean,s) for s in content),default=0),
        max_rougeL_f1_com_stop=max((rouge(qt,s) for s in raw),default=0),
        max_jaccard=max((len(qs&set(s))/len(qs|set(s)) if qs|set(s) else 0 for s in content),default=0),
        contexto_palavras=sum(len(b.split()) for b in bodies),resposta_palavras=len(q['resposta'].split()),
        resposta_substring_literal=any(q['resposta'].casefold() in b.casefold() for b in bodies))
    for n in (2,3):
        ag=grams(at,n);cg=set().union(*(grams(tokens(body),n) for body in bodies))
        result[f'novel_{n}gram_pct']=100*len(ag-cg)/len(ag) if ag else None
    return result


def self_bleu(texts):
    if len(texts)<2:return None
    from nltk.translate.bleu_score import sentence_bleu,SmoothingFunction
    ts=[tokens(t) for t in texts]
    return statistics.mean(sentence_bleu(ts[:i]+ts[i+1:],q,smoothing_function=SmoothingFunction().method1) for i,q in enumerate(ts))


def summary(rows):
    names=['overlap_q_c','max_rougeL_f1_sem_stop','max_rougeL_f1_com_stop','max_jaccard',
           'novel_2gram_pct','novel_3gram_pct','contexto_palavras','resposta_palavras']
    return {k:dict(n=len(v),media=statistics.mean(v) if v else None,mediana=statistics.median(v) if v else None)
            for k in names for v in [[r[k] for r in rows if r[k] is not None]]}


def matched(groups, seed):
    """Mesmo N por documento/classe; reduz todos ao estrato realmente disponível."""
    strata={name:defaultdict(list) for name in groups}
    for name,qs in groups.items():
        for q in qs:strata[name][q['item'],q['tipo']].append(q)
    selected={name:[] for name in groups};rng=random.Random(seed)
    keys=sorted(set().union(*(set(s) for s in strata.values())))
    for key in keys:
        n=min(len(s[key]) for s in strata.values())
        for name,s in strata.items():
            candidates=sorted(s[key],key=lambda q:q['uid']);rng.shuffle(candidates)
            selected[name]+=candidates[:n]
    return selected


def semantic(vectors):
    import numpy as np
    e=np.asarray(vectors,dtype=float)
    if len(e)<2:return dict(n=len(e),status='amostra_insuficiente')
    norms=np.linalg.norm(e,axis=1,keepdims=True)
    if not np.isfinite(e).all() or (norms==0).any():raise ValueError('Embeddings inválidos')
    e=e/norms;s=e@e.T;off=s[np.triu_indices(len(e),1)];np.fill_diagonal(s,-np.inf)
    def vendi(matrix):
        eig=np.clip(np.linalg.eigvalsh(matrix@matrix.T/len(matrix)),0,None);eig/=eig.sum()
        return float(np.exp(-sum(x*np.log(x) for x in eig if x>0)))
    centered=e-e.mean(axis=0);cn=np.linalg.norm(centered,axis=1,keepdims=True)
    return dict(n=len(e),cosseno_medio=float(off.mean()),distancia_media_cosseno=float(1-off.mean()),
        cosseno_vizinho=float(s.max(axis=1).mean()),vendi_cosseno=vendi(e),
        vendi_centrado_sensibilidade=vendi(centered/cn) if (cn>1e-12).all() else None)


def calculate(groups, output, seed=20261102, embeddings=False):
    from spacy.lang.pt.stop_words import STOP_WORDS
    output=Path(output);output.mkdir(parents=True,exist_ok=True)
    per=[measure(q,STOP_WORDS) for qs in groups.values() for q in qs]
    jsonl(output/'por_questao.jsonl',per)
    sub=matched(groups,seed);byuid={r['uid']:r for r in per};result={}
    encoder=None;cache={}
    if embeddings:
        from pipeline.qa_research.selection import LocalE5
        encoder=LocalE5(output/'.local',offline=True)
    try:
        for label,sets in [('integral',groups),('comparavel_mesmo_n_item_classe',sub)]:
            result[label]={}
            for name,qs in sets.items():
                rows=[byuid[q['uid']] for q in qs];texts=[q['pergunta'] for q in qs]
                r=dict(n=len(qs),uids=[q['uid'] for q in qs],metricas=summary(rows),self_bleu4=self_bleu(texts),
                    duplicatas_exatas=len(texts)-len({' '.join(tokens(t)) for t in texts}),
                    semantica=dict(status='nao_calculada',motivo='Executar metrics --embeddings com snapshot E5 local'))
                if encoder and texts:
                    for q in qs:
                        if q['uid'] not in cache:cache[q['uid']]=encoder.queries([q['pergunta']])[0]
                    r['semantica']=dict(semantic([cache[q['uid']] for q in qs]),protocolo=encoder.protocol)
                result[label][name]=r
    finally:
        if encoder:encoder.close()
    result['protocolo']=dict(seed=seed,lematizacao=False,stopwords='spaCy PT',
        tokenizacao='Unicode NFC, minúsculas, números excluídos; hífens e acentos preservados',
        rouge='LCS F1 máximo por frase; com/sem stopwords',novel='Conjuntos únicos por bloco; não cruza fronteiras de blocos',
        self_bleu='NLTK BLEU4, smoothing método 1; outras perguntas do próprio grupo como referências',
        interpretacao='Distância lexical não comprova raciocínio; Vendi depende do kernel e do N. Sem limiares de aprovação.',
        dados_sha256=digest(groups))
    atomic_json(output/'metricas.json',result)
    md=['# Métricas descritivas do piloto','',
        'A comparação principal usa o mesmo número de perguntas por documento e classe. Não comparar Self BLEU ou Vendi do piloto diretamente com os 2.818 itens globais.',
        '', '| Grupo | N comparável | Overlap Q C | Max ROUGE L | Novel bigramas | Novel trigramas | Self BLEU 4 |',
        '|---|---:|---:|---:|---:|---:|---:|']
    def fmt(value):return '—' if value is None else f'{value:.4f}'
    for name,r in result['comparavel_mesmo_n_item_classe'].items():
        m=r['metricas'];values=[m[k]['media'] for k in ['overlap_q_c','max_rougeL_f1_sem_stop','novel_2gram_pct','novel_3gram_pct']]
        md.append('| '+name+' | '+str(r['n'])+' | '+' | '.join(fmt(x) for x in values+[r['self_bleu4']])+' |')
    md+=['','Overlap é fração; Novel é percentual. Sem lematização. Os denominadores válidos de respostas curtas estão no JSON.',
         'Semântica, Vendi e sensibilidade centrada ficam no JSON quando --embeddings é informado. Métricas lexicais não comprovam raciocínio nem sustentação factual.']
    (output/'RESULTADOS.md').write_text('\n'.join(md)+'\n',encoding='utf-8')
    return result
