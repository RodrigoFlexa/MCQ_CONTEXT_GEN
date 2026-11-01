"""Leitura da edição existente, aplicação de patches e exportação compatível."""
import copy
import json
from pathlib import Path

from pipeline.domain_corpora.io_utils import file_hash
from pipeline.inventario.textutil import read_json
from pipeline.qa_research.v3.runtime import digest, topic
from pipeline.qa_research.v3.review import editor_issues
from . import contracts as C


def catalog(document):
    chapters = {c['id']: c for c in document['capitulos']}
    blocks = {b['id']: b for c in document['capitulos'] for b in c['blocos']}
    return chapters, blocks


def clean(document):
    return dict(titulo=document['titulo'], capitulos=[dict(titulo=c['titulo'], grupo=c['grupo'],
        blocos=[dict(subtitulo=b['subtitulo'], texto=b['texto']) for b in c['blocos']]) for c in document['capitulos']])


def markdown(document):
    lines = ['# ' + document['titulo']]
    previous = None
    for chapter in document['capitulos']:
        if chapter['grupo'] != previous:
            lines += ['', '## ' + chapter['grupo']]
            previous = chapter['grupo']
        lines += ['', '### ' + chapter['titulo']]
        for block in chapter['blocos']:
            lines += ['', '#### ' + block['subtitulo'], '', block['texto']]
    return '\n'.join(lines) + '\n'


def load_base(base, item, legacy_root, expert_file):
    C.require(item == topic(item)['id'], 'Item inválido')
    folder = Path(base).resolve() / item
    path = folder / 'documento.json'
    raw = read_json(path)
    C.require(isinstance(raw, dict) and C.text(raw.get('titulo')) and isinstance(raw.get('capitulos'), list),
              'Documento anterior ausente ou incompatível: ' + str(path))
    document = dict(titulo=raw['titulo'], capitulos=[])
    for ci, chapter in enumerate(raw['capitulos'], 1):
        C.require(C.text(chapter.get('titulo')) and C.text(chapter.get('grupo')) and chapter.get('blocos'), 'Capítulo anterior inválido')
        blocks = []
        for bi, block in enumerate(chapter['blocos'], 1):
            C.require(C.text(block.get('subtitulo')) and C.text(block.get('texto')), 'Bloco anterior inválido')
            blocks.append(dict(id=f'B{ci:02}_{bi:02}', subtitulo=block['subtitulo'], texto=block['texto']))
        document['capitulos'].append(dict(id=f'C{ci:02}', titulo=chapter['titulo'], grupo=chapter['grupo'], blocos=blocks))
    C.require(document['capitulos'], 'Documento anterior vazio')
    summary = read_json(folder / 'resumo.json') or {}
    legacy = Path(legacy_root).resolve() / item
    facets = read_json(legacy / 'pacote' / 'facets.json') or []
    C.require(isinstance(facets, list), 'Recortes anteriores inválidos')
    points = [dict(id=f['id'], titulo=f['titulo'], descricao=f.get('foco', f['titulo']),
                   grupo=f.get('grupo', '')) for f in facets]
    C.require(points, 'Recortes curados ausentes; não reconstruir o checklist a partir do conteúdo existente: ' + str(legacy))
    C.rows(points, 'recortes herdados')
    protected = []
    expert = read_json(expert_file) if expert_file and Path(expert_file).is_file() else None
    for row in (expert or {}).get('documentos', {}).get(item, []):
        ci, bi = row['capitulo'], row['bloco']
        C.require(0 <= ci < len(document['capitulos']) and 0 <= bi < len(document['capitulos'][ci]['blocos']), 'Correção do especialista fora do documento')
        block = document['capitulos'][ci]['blocos'][bi]
        # A edição de entrada deve realmente conter as correções que declara herdar.
        C.require(row['depois'] in block['texto'], 'Edição de entrada não contém a correção do especialista: ' + block['id'])
        protected.append(dict(bloco=block['id'], requisito=row['depois'], motivo=row['motivo']))
    evidence = legacy / 'evidencias_citadas.jsonl'
    fingerprints = dict(documento=file_hash(path), resumo=file_hash(folder / 'resumo.json') if (folder / 'resumo.json').exists() else None,
        recortes=file_hash(legacy / 'pacote' / 'facets.json') if (legacy / 'pacote' / 'facets.json').exists() else None,
        evidencias=file_hash(evidence) if evidence.exists() else None, especialista=digest(protected))
    return dict(item=item, entrada=topic(item), documento=document, pontos=points, protecoes=protected,
        resumo_anterior=summary, origem=str(path), evidencias=str(evidence), fingerprints=fingerprints)


def validate_changes(proposal, intervention, base, findings):
    """A operação só alcança alvos autorizados; conteúdo novo precisa de fundamento."""
    chapters, blocks = catalog(base)
    seen = set()
    for row in proposal['alteracoes']:
        C.require(isinstance(row, dict), 'Alteração deve ser objeto')
        operation, target = row.get('operacao'), row.get('alvo')
        C.require(operation in ('substituir', 'inserir', 'remover', 'novo_capitulo', 'mover', 'renomear_capitulo'), 'Operação inválida')
        C.require(target in intervention['alvos'], 'Alteração fora dos alvos autorizados: ' + str(target))
        C.require(C.text(row.get('motivo')) and C.text(row.get('preservacao')), 'Registre motivo e preservação do conhecimento')
        C.refs(row.get('achados'), findings, 'alteracao.achados', empty=True)
        C.strings(row.get('complementos'), 'alteracao.complementos')
        C.require(intervention['tipo'] == 'editorial' or row['achados'] or row['complementos'],
                  'Alteração factual exige achado ou complemento conceitual declarado')
        if operation in ('substituir', 'remover', 'mover'):
            C.require(target in blocks and target not in seen, 'Alvo deve ser bloco único')
            seen.add(target)
            if operation == 'mover':
                C.require(row.get('destino') in chapters and row['destino'] in intervention['alvos'], 'Destino do movimento não autorizado')
        elif operation == 'renomear_capitulo':
            C.require(target in chapters and target not in seen and C.text(row.get('capitulo')), 'Renomeação precisa de capítulo existente e título')
            seen.add(target)
        elif operation == 'inserir':
            C.require(target in chapters or target in blocks, 'Inserção precisa de capítulo/bloco existente')
        else:
            C.require(target == 'DOCUMENTO' and C.text(row.get('capitulo')) and C.text(row.get('grupo')), 'Capítulo novo precisa de título e grupo')
        if operation not in ('remover', 'mover', 'renomear_capitulo'):
            C.require(C.text(row.get('subtitulo')) and C.text(row.get('texto')), 'Bloco novo precisa de subtítulo e texto')
            issues = editor_issues(row)
            C.require(not issues, '; '.join(issues))


def apply_changes(base, proposals):
    document = copy.deepcopy(base)
    occupied = set()
    for proposal in proposals:
        for number, row in enumerate(proposal['alteracoes'], 1):
            operation, target = row['operacao'], row['alvo']
            chapters, blocks = catalog(document)
            if operation in ('substituir', 'remover', 'mover', 'renomear_capitulo'):
                C.require(target not in occupied and target in (chapters if operation == 'renomear_capitulo' else blocks), 'Conflito entre alterações: ' + target)
                occupied.add(target)
            if operation == 'renomear_capitulo':
                chapters[target]['titulo'] = row['capitulo']
                if row.get('grupo'):
                    chapters[target]['grupo'] = row['grupo']
                continue
            block = dict(id=f'N_{proposal["id"]}_{number}', subtitulo=row.get('subtitulo'), texto=row.get('texto'))
            if operation == 'novo_capitulo':
                document['capitulos'].append(dict(id=f'NC_{proposal["id"]}_{number}', titulo=row['capitulo'], grupo=row['grupo'], blocos=[block]))
                continue
            chapter = chapters.get(target) or next(c for c in document['capitulos'] if any(b['id'] == target for b in c['blocos']))
            if operation == 'inserir' and target in chapters:
                chapter['blocos'].append(block)
            else:
                index = next(i for i, b in enumerate(chapter['blocos']) if b['id'] == target)
                if operation == 'substituir':
                    chapter['blocos'][index] = dict(block, id=target)
                elif operation == 'remover':
                    chapter['blocos'].pop(index)
                elif operation == 'mover':
                    moved = chapter['blocos'].pop(index)
                    chapters[row['destino']]['blocos'].append(moved)
                else:
                    chapter['blocos'].insert(index + 1, block)
    document['capitulos'] = [c for c in document['capitulos'] if c['blocos']]
    C.require(document['capitulos'], 'Uma edição não pode apagar o documento inteiro')
    return document


def diff(base, proposals):
    chapters, blocks = catalog(base)
    result = []
    for proposal in proposals:
        for row in proposal['alteracoes']:
            before = blocks.get(row['alvo'])
            result.append(dict(intervencao=proposal['id'], **row, antes=before,
                capitulo_anterior=chapters[row['alvo']]['titulo'] if row['alvo'] in chapters else None,
                alerta_reducao=bool(before and row['operacao'] == 'substituir' and len(row['texto'].split()) < len(before['texto'].split()) * .6)))
    return result
