"""Versão final dos 40 contextos para a geração de questões (relatorios/contextos_finais_v1).

Parte da coleta do refino e aplica correções de forma, sem mudar conteúdo técnico:

1. Restaura o texto do editor final nos blocos em que a inserção automática de siglas corrompeu a expansão
   (ex.: "(Multiphase Flow Meter, Multiphase Flow Meter (MPFM))"). O texto do editor está em polimento.json.
2. Siglas sem expansão na primeira ocorrência do documento recebem a expansão do glossário, no formato
   "SIGLA (expansão)", que preserva a concordância do artigo ("do FPSO (...)").
3. Expansões repetidas depois da primeira ocorrência voltam a ser só a sigla (glossário e 1ª ocorrência bastam).
4. Correções manuais pontuais (dados/correcoes_finais.json): troca exata, que precisa ocorrer uma vez.
5. Checagens finais: siglas, metatexto, travessões, termos do especialista, parênteses quebrados, concordância
   "do/no/o unidade" e afins. O relatório lista o que mudou por documento.

    python -m pipeline.qa_research.refino.finalizar \\
        --coleta pipeline/qa_research/relatorios/refino_contextos_20261121T183818 \\
        --saida pipeline/qa_research/relatorios/contextos_finais_v1
"""
import argparse
import json
import re
import shutil
from collections import Counter
from pathlib import Path

from pipeline.domain_corpora.io_utils import file_hash
from pipeline.inventario.textutil import atomic_json

from . import textos as T

DADOS = Path(__file__).resolve().parent / 'dados' / 'correcoes_finais.json'
QUEBRADO = [
    ('parenteses_duplos', re.compile(r'\)\s*\([A-Z][A-Za-z0-9&/-]+\)\)')),
    ('aninhado', re.compile(r'\([^()]{0,160}\([A-Z][A-Za-z0-9&/-]+\)[^()]{0,40}\)')),
    ('repetido', re.compile(r'\b([A-Z][\w-]+(?: [\w-]+){0,4}) \([A-Z][A-Z0-9-]+\) \1\b')),
]
CONCORDANCIA = re.compile(r'\b(?:do|no|ao|pelo|o|um|deste|desse|neste|nesse|daquele)\s+unidade\b', re.I)


def ler(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def problemas(texto):
    out = [nome for nome, p in QUEBRADO if p.search(texto)]
    if CONCORDANCIA.search(texto):
        out.append('concordancia')
    if T.TRAVESSAO.search(texto):
        out.append('travessao')
    return out


def restaurar(doc, detalhado, polimento, log):
    """Blocos corrompidos voltam ao texto que o editor final entregou (antes da inserção automática)."""
    depois = {a['bloco']: T.TRAVESSAO.sub(', ', a['depois']) for a in polimento.get('alteracoes', [])}
    for c, cd in zip(doc['capitulos'], detalhado['capitulos']):
        for b, bd in zip(c['blocos'], cd['blocos']):
            achados = [p for p in problemas(b['texto']) if p != 'travessao']
            novo = depois.get(bd.get('id'))
            if achados and novo and novo != b['texto'] and not [p for p in problemas(novo) if p != 'travessao']:
                log.append(dict(bloco=bd['id'], tipo='restaurado', motivo=achados))
                b['texto'] = novo


def expandir_pendentes(doc, glossario, log):
    pend, _ = T.acronyms(doc)
    ids = {bid: (ci, bi) for ci, c in enumerate(doc['capitulos']) for bi, _ in enumerate(c['blocos'])
           for bid in [f'C{ci + 1:02d}B{bi + 1:02d}']}
    for bid, siglas in pend.items():
        ci, bi = ids[bid]
        b = doc['capitulos'][ci]['blocos'][bi]
        for s in siglas:
            if s in glossario:
                b['texto'] = re.sub(r'\b' + re.escape(s) + r'\b', f'{s} ({glossario[s]})', b['texto'], count=1)
                log.append(dict(bloco=bid, tipo='sigla_expandida', sigla=s))


def tirar_reexpansoes(doc, glossario, log):
    """Depois da primeira "expansão (SIGLA)", as seguintes viram só a sigla (só quando a expansão é a do glossário)."""
    vistos = set()
    for ci, c in enumerate(doc['capitulos'], 1):
        for bi, b in enumerate(c['blocos'], 1):
            texto = b['texto']
            for s, e in glossario.items():
                padrao = re.compile(r'(?<![\w(])' + re.escape(e[0]) + '(?i:' + re.escape(e[1:]) + r') \(' + re.escape(s) + r'\)')
                partes, pos, novo = [], 0, []
                for m in padrao.finditer(texto):
                    if s in vistos:
                        novo.append(texto[pos:m.start()] + s)
                        pos = m.end()
                        log.append(dict(bloco=f'C{ci:02d}B{bi:02d}', tipo='reexpansao_removida', sigla=s))
                    vistos.add(s)
                if novo:
                    texto = ''.join(novo) + texto[pos:]
                if re.search(r'\b' + re.escape(s) + r'\b', texto):
                    vistos.add(s)
            b['texto'] = texto


def corrigir_manual(doc, item, correcoes, log):
    for c in correcoes.get(item, []):
        alvo = [b for cap in doc['capitulos'] for b in cap['blocos'] if c['antes'] in b['texto']]
        total = sum(b['texto'].count(c['antes']) for b in alvo)
        if total != 1:
            raise ValueError(f"{item}: correção manual precisa ocorrer uma vez ({total}x): {c['antes'][:80]}")
        alvo[0]['texto'] = alvo[0]['texto'].replace(c['antes'], c['depois'])
        log.append(dict(tipo='manual', antes=c['antes'], depois=c['depois'], motivo=c.get('motivo')))


def glossario_final(doc, glossario):
    texto = ' '.join(s + ' ' + t for _, s, t in T.blocks_of(doc))
    return {s: e for s, e in sorted(glossario.items()) if re.search(r'\b' + re.escape(s) + r's?\b', texto)}


def blocos_questoes(item, doc, detalhado, antigos, glossario):
    por_id = {r['bloco']: r for r in antigos}
    out = []
    for c, cd in zip(doc['capitulos'], detalhado['capitulos']):
        for b, bd in zip(c['blocos'], cd['blocos']):
            velho = por_id.get(bd.get('id'), {})
            achadas = {T._base_sigla(m.group(0)) for m in T.SIGLA.finditer(b['subtitulo'] + ' ' + b['texto'])}
            out.append(dict(velho, documento=item, titulo_documento=doc['titulo'], capitulo=c['titulo'], bloco=bd.get('id'),
                            subtitulo=b['subtitulo'], texto=b['texto'],
                            siglas={s: glossario[s] for s in sorted(achadas) if s in glossario},
                            testabilidade=T.testability(dict(capitulos=[dict(blocos=[b])]))))
    return out


def finalizar(coleta, saida, correcoes=None):
    coleta, saida = Path(coleta), Path(saida)
    correcoes = correcoes or {}
    saida.mkdir(parents=True, exist_ok=True)
    resumo = {}
    for pasta in sorted(p for p in coleta.iterdir() if (p / 'documento.json').exists()):
        item, log = pasta.name, []
        doc, det = ler(pasta / 'documento.json'), ler(pasta / 'documento_detalhado.json')
        pol = ler(pasta / 'polimento.json') if (pasta / 'polimento.json').exists() else {}
        glos = ler(pasta / 'glossario.json') if (pasta / 'glossario.json').exists() else {}
        antes = T.style_report(doc)
        restaurar(doc, det, pol, log)
        expandir_pendentes(doc, glos, log)
        tirar_reexpansoes(doc, glos, log)
        corrigir_manual(doc, item, correcoes, log)
        for c in doc['capitulos']:
            for b in c['blocos']:
                b['texto'] = T.TRAVESSAO.sub(', ', b['texto'])
        restantes = [dict(bloco=bid, problemas=p) for bid, s, t in T.blocks_of(doc) for p in [problemas(s + ' ' + t)] if p]
        lint = [dict(bloco=bid, alertas=a) for bid, s, t in T.blocks_of(doc) for a in [T.lint(s + ' ' + t)] if a]
        gl = glossario_final(doc, glos)
        destino = saida / item
        destino.mkdir(parents=True, exist_ok=True)
        atomic_json(destino / 'documento.json', T.clean(doc))
        (destino / 'documento.md').write_text(T.markdown(T.clean(doc)), encoding='utf-8')
        atomic_json(destino / 'glossario.json', gl)
        antigos = [json.loads(l) for l in (pasta / 'blocos_questoes.jsonl').read_text(encoding='utf-8').splitlines()
                   if l.strip()] if (pasta / 'blocos_questoes.jsonl').exists() else []
        linhas = blocos_questoes(item, doc, det, antigos, gl)
        (destino / 'blocos_questoes.jsonl').write_text(
            ''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in linhas), encoding='utf-8')
        for nome in ('metricas.json', 'RELATORIO.md'):
            if (pasta / nome).exists():
                shutil.copy2(pasta / nome, destino / ('refino_' + nome))
        atomic_json(destino / 'revisao_final.json', dict(alteracoes=log, problemas_restantes=restantes, lint=lint))
        resumo[item] = dict(titulo=doc['titulo'], palavras=len(T.words(' '.join(t for _, _, t in T.blocks_of(doc)))),
                            blocos=len(T.blocks_of(doc)), alteracoes=dict(Counter(x['tipo'] for x in log)),
                            estilo_antes=antes, estilo_depois=T.style_report(doc),
                            problemas_restantes=len(restantes), alertas_lint=len(lint), siglas_glossario=len(gl))
    atomic_json(saida / 'resumo.json', dict(origem=str(coleta), documentos=resumo))
    atomic_json(saida / 'manifest.json', dict(
        files={p.relative_to(saida).as_posix(): file_hash(p) for p in sorted(saida.rglob('*')) if p.is_file()
               and p.name != 'manifest.json'}))
    (saida / 'REVISAO.md').write_text(relatorio(resumo), encoding='utf-8')
    return resumo


def relatorio(resumo):
    tot = Counter()
    for r in resumo.values():
        tot.update(r['alteracoes'])
    linhas = ['# Contextos finais v1: revisão de forma', '',
              f"{len(resumo)} documentos, {sum(r['palavras'] for r in resumo.values())} palavras, "
              f"{sum(r['blocos'] for r in resumo.values())} blocos.", '',
              'Alterações: ' + ', '.join(f'{k} {v}' for k, v in sorted(tot.items())) + '.', '',
              '| Documento | Palavras | Blocos | Alterações | Siglas sem expansão (antes → depois) | Problemas restantes |',
              '|---|---|---|---|---|---|']
    for item, r in resumo.items():
        linhas.append(f"| {item} | {r['palavras']} | {r['blocos']} | {sum(r['alteracoes'].values())} | "
                      f"{r['estilo_antes']['siglas_sem_expansao']} → {r['estilo_depois']['siglas_sem_expansao']} | "
                      f"{r['problemas_restantes'] + r['alertas_lint']} |")
    return '\n'.join(linhas) + '\n'


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--coleta', type=Path, required=True)
    parser.add_argument('--saida', type=Path, required=True)
    parser.add_argument('--correcoes', type=Path, default=DADOS)
    args = parser.parse_args(argv)
    correcoes = ler(args.correcoes) if args.correcoes.exists() else {}
    resumo = finalizar(args.coleta, args.saida, correcoes)
    for item, r in resumo.items():
        print(item, r['palavras'], r['alteracoes'], 'restantes', r['problemas_restantes'], 'lint', r['alertas_lint'])


if __name__ == '__main__':
    main()
