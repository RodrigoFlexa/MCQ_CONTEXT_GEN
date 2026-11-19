"""Contexto para qualquer recorte de um documento refinado (geração e resposta de questões).

O documento é escrito para ser recortado. Mesmo assim, um trecho solto perde o título do
documento, a seção e o significado de siglas apresentadas antes. `contexto` devolve um
cabeçalho curto com essas três coisas, montado a partir de `blocos_questoes.jsonl` e
`glossario.json` do documento (técnica de "contextual retrieval": o contexto vai à frente do
trecho, o texto do trecho não muda).

    from pipeline.qa_research.refino.para_questoes import carregar, contexto
    blocos, glossario = carregar('pipeline/qa_research/relatorios/<coleta>/02_06')
    cabecalho = contexto(trecho, blocos, glossario)
"""
import json
from pathlib import Path

from . import textos as T


def carregar(pasta):
    pasta = Path(pasta)
    blocos = [json.loads(l) for l in (pasta / 'blocos_questoes.jsonl').read_text(encoding='utf-8').splitlines() if l.strip()]
    glossario_path = pasta / 'glossario.json'
    glossario = json.loads(glossario_path.read_text(encoding='utf-8')) if glossario_path.is_file() else {}
    return blocos, glossario


def blocos_do_trecho(trecho, blocos):
    """Blocos de onde o trecho saiu: os que contêm alguma de suas sentenças (ou o trecho inteiro)."""
    alvo = T.norm(trecho)
    frases = [T.norm(s) for s in T.sentences(trecho)] or [alvo]
    achados = []
    for b in blocos:
        texto = T.norm(b['texto'])
        if alvo in texto or any(f in texto for f in frases):
            achados.append(b)
    return achados


def contexto(trecho, blocos, glossario, incluir_origem=False):
    origem = blocos_do_trecho(trecho, blocos)
    linhas = []
    if origem:
        linhas.append('Documento: ' + origem[0]['titulo_documento'])
        secoes = list(dict.fromkeys(f"{b['capitulo']} > {b['subtitulo']}" for b in origem))
        linhas.append('Seção: ' + ' | '.join(secoes))
    siglas = {T._base_sigla(m.group(0)) for m in T.SIGLA.finditer(trecho)}
    usadas = {s: glossario[s] for s in sorted(siglas) if s in glossario}
    if usadas:
        linhas.append('Siglas: ' + '; '.join(f'{s} = {e}' for s, e in usadas.items()))
    if incluir_origem and origem:
        sem = [b['bloco'] for b in origem if b.get('sem_evidencia')]
        linhas.append('Conteúdo sem evidência nos corpora: ' + (', '.join(sem) if sem else 'nenhum'))
    return '\n'.join(linhas)
