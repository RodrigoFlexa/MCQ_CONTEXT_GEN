"""Gráficos locais dos três bancos; nunca seleciona ou altera as questões de entrada."""
import hashlib
import json
import re
import unicodedata
from collections import Counter
from pathlib import Path

from .core import ROOT, HERE, ler_linhas, sha

MODEL = 'intfloat/multilingual-e5-small'
REVISION = '614241f622f53c4eeff9890bdc4f31cfecc418b3'
WORD = re.compile(r'[^\W\d_]+(?:[-’\'][^\W\d_]+)*', re.UNICODE)
LABELS = ('Enunciados', 'Respostas', 'Enunciados + respostas')
FIELDS = ('perguntas', 'respostas', 'perguntas_respostas')


def tokens(text):
    return WORD.findall(unicodedata.normalize('NFC', text).lower())


def mattr(words, window=100):
    if len(words) < window:
        return None
    counts = Counter(words[:window])
    total = len(counts)
    for i in range(window, len(words)):
        old = words[i-window]
        counts[old] -= 1
        if not counts[old]:
            del counts[old]
        counts[words[i]] += 1
        total += len(counts)
    return total/(len(words)-window+1)/window


def carregar_manifesto(path):
    m = json.loads(Path(path).read_text(encoding='utf-8'))
    if m.get('schema') != 'comparacao-tres-bancos-v1' or len(m['bancos']) != 3:
        raise ValueError('Manifesto dos três bancos inválido')
    out = []
    for spec in m['bancos']:
        p = Path(spec['path'])
        rows = ler_linhas(p if p.is_absolute() else ROOT/p)
        if len(rows) != spec['questoes'] or sha(rows) != spec['conteudo_sha256']:
            raise ValueError('Banco mudou após montar o manifesto: '+spec['id'])
        if len(rows) < 2 or len({q['uid'] for q in rows}) != len(rows):
            raise ValueError('Cada banco precisa de pelo menos duas questões e IDs únicos')
        out.append((spec, rows))
    return m, out


class E5Local:
    def __init__(self):
        import os
        os.environ['HF_HUB_OFFLINE'] = '1'
        os.environ['TRANSFORMERS_OFFLINE'] = '1'
        os.environ['TOKENIZERS_PARALLELISM'] = 'false'
        import torch
        from transformers import AutoModel, AutoTokenizer
        snapshot = Path.home()/'.cache/huggingface/hub'/('models--'+MODEL.replace('/', '--'))/'snapshots'/REVISION
        if not snapshot.is_dir():
            raise FileNotFoundError('O E5 precisa estar no cache local para os gráficos; não há download automático')
        torch.set_num_threads(4)
        self.tokenizer = AutoTokenizer.from_pretrained(str(snapshot), local_files_only=True)
        self.model = AutoModel.from_pretrained(str(snapshot), local_files_only=True).eval()

    def __call__(self, texts):
        import torch
        import numpy as np
        prepared = ['query: '+t for t in texts]
        lengths = [len(x) for x in self.tokenizer(prepared, truncation=False, verbose=False)['input_ids']]
        if max(lengths) > 512:
            raise ValueError('Há texto acima de 512 tokens: não será truncado silenciosamente')
        order = np.argsort(lengths)
        vectors = np.empty((len(texts), 384), dtype=np.float32)
        with torch.inference_mode():
            for start in range(0, len(texts), 32):
                ix = order[start:start+32]
                batch = self.tokenizer([prepared[i] for i in ix], padding=True, truncation=False, return_tensors='pt')
                hidden = self.model(**batch).last_hidden_state
                mask = batch['attention_mask'].unsqueeze(-1).bool()
                mean = hidden.masked_fill(~mask, 0.).sum(dim=1)/mask.sum(dim=1)
                vectors[ix] = torch.nn.functional.normalize(mean, p=2, dim=1).numpy()
                if start % 640 == 0:
                    print(f'Embeddings: {min(start+32,len(texts))}/{len(texts)}', flush=True)
        return vectors


def analisar(manifesto, output, *, encoder=None):
    import csv
    import numpy as np
    import sklearn
    from sklearn.feature_extraction.text import TfidfVectorizer
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    manifest, banks = carregar_manifesto(manifesto)
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    stop = (HERE/'stopwords_pt.txt').read_text(encoding='utf-8').splitlines()
    colors = ('#b45c26', '#117c83', '#7254a3')
    short = ('Sem contexto', 'Com contexto', 'Com contexto + especialista')
    metrics, texts, lexrows, simrows, arrays = {}, {}, [], [], {}
    for spec, rows in banks:
        name = spec['id']
        texts[name] = {'perguntas': [q['pergunta'] for q in rows], 'respostas': [q['resposta'] for q in rows],
                       'perguntas_respostas': [q['pergunta']+'\n'+q['resposta'] for q in rows]}
        metrics[name] = {'questoes': len(rows), 'lexico': {}, 'similaridade': {}}
        for field, ts in texts[name].items():
            words = [w for t in ts for w in tokens(t)]
            counts = Counter(words)
            m = {'tokens': len(words), 'types': len(counts), 'ttr': len(counts)/len(words) if words else None,
                 'mattr_50': mattr(words, 50), 'mattr_100': mattr(words, 100),
                 'palavras_por_questao': len(words)/len(rows)}
            metrics[name]['lexico'][field] = m
            lexrows.append({'banco': name, 'campo': field, 'questoes': len(rows), **m})
    model = encoder
    for field in ('perguntas', 'perguntas_respostas'):
        # O banco com especialista contém o banco base: este não deve pesar duas vezes no IDF.
        byuid = {}
        for spec, rows in banks:
            for q, t in zip(rows, texts[spec['id']][field]):
                if q['uid'] in byuid and byuid[q['uid']] != t:
                    raise ValueError('Mesmo UID com textos diferentes nos bancos')
                byuid[q['uid']] = t
        vectorizer = TfidfVectorizer(tokenizer=tokens, token_pattern=None, lowercase=False, stop_words=stop,
                                    ngram_range=(1, 2), sublinear_tf=True, norm='l2', dtype=np.float32)
        vectorizer.fit(list(byuid.values()))
        for spec, rows in banks:
            name = spec['id']
            ts = texts[name][field]
            dense = None
            digest = sha(ts)
            cache = output/f'embeddings_{digest[:20]}.npz'
            if cache.exists():
                with np.load(cache, allow_pickle=False) as z:
                    if str(z['digest']) == digest and str(z['revision']) == REVISION:
                        dense = z['vectors']
            if dense is None:
                if model is None:
                    model = E5Local()
                dense = model(ts)
                np.savez_compressed(cache, vectors=dense, digest=digest, revision=REVISION)
            if len(dense) != len(rows) or not np.isfinite(dense).all():
                raise ValueError('Embeddings inválidos')
            lexical = vectorizer.transform(ts)
            for method, vectors in [('tfidf', lexical), ('e5', dense)]:
                sim = vectors@vectors.T
                if hasattr(sim, 'toarray'):
                    sim = sim.toarray()
                sim = np.clip(sim, -1, 1)
                assert np.isfinite(sim).all() and np.allclose(np.diag(sim), 1, atol=1e-5)
                n = len(rows)
                # Evita dois vetores de índices int64 com dezenas de milhões de elementos.
                vals = np.concatenate([sim[i, i+1:] for i in range(n-1)])
                assert len(vals) == n*(n-1)//2
                np.fill_diagonal(sim, -np.inf)
                nearest = sim.max(axis=1)
                stats = {'pares': len(vals), 'media_pares': float(vals.mean()),
                         'mediana_pares': float(np.median(vals)), 'p95_pares': float(np.quantile(vals, .95)),
                         'mediana_vizinho': float(np.median(nearest)), 'p95_vizinho': float(np.quantile(nearest, .95)),
                         'pares_maior_igual_095': int((vals >= .95).sum()),
                         'questoes_com_vizinho_095': int((nearest >= .95).sum())}
                metrics[name]['similaridade'][method+'_'+field] = stats
                simrows.append({'banco': name, 'campo': field, 'metrica': method, **stats})
                arrays[(name, field, method)] = (vals, nearest)
            print(f'Analisado: {name}/{field}', flush=True)
    for filename, rows in [('vocabulario.csv', lexrows), ('similaridade.csv', simrows)]:
        with (output/filename).open('w', encoding='utf-8-sig', newline='') as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0]))
            w.writeheader()
            w.writerows(rows)
    (output/'metricas.json').write_text(json.dumps(metrics, ensure_ascii=False, indent=2), encoding='utf-8')
    (output/'protocolo.json').write_text(json.dumps({
        'manifesto': manifest, 'tokens': WORD.pattern, 'normalizacao': 'NFC, minúsculas, acentos preservados, sem lematização; números excluídos',
        'mattr': 'janelas contíguas na ordem dos arquivos, incluindo fronteiras entre questões',
        'tfidf': 'IDF comum ajustado em documentos com UID único na união dos três bancos; unigramas+bigramas, L2, TF sublinear',
        'stopwords_sha256': hashlib.sha256('\n'.join(stop).encode()).hexdigest(),
        'e5': {'model': MODEL, 'revision': REVISION, 'prefix': 'query: ', 'pooling': 'mean_with_attention_mask', 'norm': 'L2'},
        'sklearn': sklearn.__version__, 'numpy': np.__version__, 'bancos_alterados': False,
        'nota': 'Tamanhos diferentes afetam TTR. E5 não é porcentagem de igualdade; comparar também MATTR. Não há deduplicação.'
    }, ensure_ascii=False, indent=2), encoding='utf-8')
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 10,
                         'axes.spines.top': False, 'axes.spines.right': False})
    def save(fig, name):
        fig.savefig(output/(name+'.png'), dpi=180)
        fig.savefig(output/(name+'.svg'))
        plt.close(fig)
    for field in ('perguntas', 'perguntas_respostas'):
        fig, axs = plt.subplots(2, 2, figsize=(14, 9), constrained_layout=True)
        for col, method in enumerate(('tfidf', 'e5')):
            bins = np.linspace(0, 1, 81) if method == 'tfidf' else np.linspace(.7, 1, 76)
            for i, (spec, rows) in enumerate(banks):
                vals, near = arrays[(spec['id'], field, method)]
                label = f'{short[i]} (n={len(rows)})'
                axs[0, col].hist(vals, bins=bins, density=True, histtype='step', color=colors[i], linewidth=2, label=label)
                axs[1, col].hist(near, bins=bins, density=True, histtype='step', color=colors[i], linewidth=2,
                                 label=label+f' · mediana {np.median(near):.3f}')
            axs[0, col].set(title='TF-IDF comum' if col == 0 else 'Proximidade semântica E5',
                             xlabel='Cosseno de todos os pares', ylabel='Densidade')
            axs[1, col].set(title='Vizinho mais próximo de cada questão', xlabel='Cosseno do vizinho', ylabel='Densidade')
            if col == 0:
                axs[0, col].set_yscale('log')
            for ax in axs[:, col]:
                ax.legend(fontsize=8)
        fig.suptitle('Comparação dos três bancos · '+('enunciados' if field == 'perguntas' else 'enunciados e respostas'), fontsize=16)
        fig.supxlabel('Densidades normalizadas por banco. E5 não é porcentagem de igualdade.', fontsize=10)
        save(fig, 'similaridade_'+field)
    fig, axs = plt.subplots(2, 2, figsize=(14, 9), constrained_layout=True)
    x = np.arange(3)
    panels = [('ttr', 'TTR global · sensível ao tamanho', 100), ('mattr_100', 'MATTR de 100 palavras', 100),
              ('types', 'Formas distintas', 1), ('palavras_por_questao', 'Palavras por questão, média', 1)]
    for ax, (key, title, scale) in zip(axs.flat, panels):
        for i, (spec, rows) in enumerate(banks):
            vals = [metrics[spec['id']]['lexico'][f][key] for f in FIELDS]
            vals = [np.nan if v is None else v*scale for v in vals]
            bars = ax.bar(x+(i-1)*.25, vals, width=.25, color=colors[i], label=f'{short[i]} (n={len(rows)})')
            ax.bar_label(bars, fmt='%.2f' if scale == 100 else '%.0f', fontsize=8, padding=3)
        ax.set(title=title, xticks=x, xticklabels=LABELS)
        ax.legend(fontsize=8)
    fig.suptitle('Diversidade lexical dos três bancos', fontsize=16)
    fig.supxlabel('O banco com especialista é maior: o TTR bruto não deve ser comparado isoladamente.', fontsize=10)
    save(fig, 'vocabulario')
    text = ['# Análise dos três bancos', '', manifest['observacao'], '',
            '| Banco | Questões | Palavras nos enunciados | Formas distintas | TTR | MATTR-100 |',
            '|---|---:|---:|---:|---:|---:|']
    for spec, rows in banks:
        m = metrics[spec['id']]['lexico']['perguntas']
        fmt = lambda v: '-' if v is None else f'{v:.4f}'
        text.append(f"| {spec['rotulo']} | {len(rows)} | {m['tokens']} | {m['types']} | {fmt(m['ttr'])} | {fmt(m['mattr_100'])} |")
    text += ['', '![Vocabulário](vocabulario.png)', '', '![Similaridade](similaridade_perguntas.png)', '',
             'Os grupos diferem em volume, origem e filtros. As medidas não certificam correção técnica '
             'nem isolam o efeito causal de adicionar questões do especialista. Limiares E5 são '
             'descritivos; nenhuma questão foi removida para produzir estes resultados.', '']
    (output/'RELATORIO.md').write_text('\n'.join(text), encoding='utf-8')
    carregar_manifesto(manifesto)  # confirma que as três fontes continuam intactas
    return metrics
