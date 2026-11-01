"""Leitura da edição existente, aplicação de patches e exportação compatível."""
import copy
import json
from pathlib import Path

from pipeline.domain_corpora.io_utils import file_hash
from pipeline.inventario.textutil import read_json
from pipeline.qa_research.v3.runtime import digest, topic
from . import contracts as C
from .editorial import block_issues


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
    C.normalize_operations(proposal)
    seen = set()
    for row in proposal['alteracoes']:
        C.require(isinstance(row, dict), 'Alteração deve ser objeto')
        operation, target = row.get('operacao'), row.get('alvo')
        C.require(operation in ('substituir', 'inserir', 'remover', 'novo_capitulo', 'mover', 'renomear_capitulo'), 'Operação inválida')
        C.require(target in intervention['alvos'], 'Alteração fora dos alvos autorizados: ' + str(target))
        C.require(C.text(row.get('motivo')) and C.text(row.get('preservacao')), 'Registre motivo e preservação do conhecimento')
        C.refs(row.get('achados'), findings, 'alteracao.achados', empty=True)
        C.strings(row.get('complementos'), 'alteracao.complementos')
        C.require(intervention['tipo'] != 'editorial' or (not row['achados'] and not row['complementos']),
                  'Edição editorial não acrescenta fatos, achados ou complementos')
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
            issues = block_issues(row)
            C.require(not issues, '; '.join(issues))


def apply_changes(base, proposals):
    document = copy.deepcopy(base)
    for proposal in proposals:
        # Propostas são commits sequenciais; só operações dentro do mesmo commit
        # disputam alvos. Um reparo posterior pode legitimamente tocar o mesmo bloco.
        occupied = set()
        for number, row in enumerate(proposal['alteracoes'], 1):
            number = int(row['op_id'].rsplit('_OP', 1)[1]) if row.get('op_id') else number
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
            C.require(block['id'] not in blocks or operation not in ('inserir', 'novo_capitulo'),
                      'ID de bloco novo já existe: ' + block['id'])
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


def build_review_payload(base_doc, interventions_batch, proposals, evidences, protections):
    """Diff sobre a base ANTERIOR ao lote, sem aplicar operações em avaliação."""
    document = base_doc.get('documento', base_doc)
    chapters, blocks = catalog(document)
    interventions = {i['id']: i for i in interventions_batch}
    structural = [dict(capitulo_id=c['id'], titulo=c['titulo'], blocos_existentes=[
        dict(bloco_id=b['id'], subtitulo=b['subtitulo'], resumo_primeiras_30_palavras=' '.join(b['texto'].split()[:30]))
        for b in c['blocos']]) for c in document['capitulos']]
    entries = []
    for proposal in proposals:
        C.normalize_operations(proposal)
        intervention = interventions[proposal['id']]
        research = evidences.get(proposal['id'], {}) if isinstance(evidences, dict) else {}
        findings = research.get('achados', [])
        supplied = [dict(f, fontes=[s for s in research.get('fontes', [])
                    if any(p['id'] in f['citacoes'] for p in s['paragrafos'])]) for f in findings]
        if isinstance(evidences, list):
            supplied = evidences
        operations = []
        for row in proposal['alteracoes']:
            target, operation = row['alvo'], row['operacao']
            creation = operation in ('inserir', 'novo_capitulo')
            before = None if creation else blocks.get(target) or chapters.get(target)
            chapter = chapters.get(target) or next((c for c in document['capitulos']
                if any(b['id'] == target for b in c['blocos'])), None)
            previous = dict(bloco_id=target, subtitulo=before.get('subtitulo', before.get('titulo', '')),
                            texto=before.get('texto', ''), **({'blocos': before['blocos']} if 'blocos' in before else {})) if before else None
            proposed = dict(subtitulo=row.get('subtitulo', before.get('subtitulo', '') if before else ''),
                texto=row.get('texto', before.get('texto', '') if before else ''), motivo=row['motivo'],
                preservacao=row['preservacao'], achados_citados=row['achados'], complementos=row['complementos'])
            for field in ('destino', 'capitulo', 'grupo', 'dependencias'):
                if field in row:
                    proposed[field] = row[field]
            operations.append(dict(op_id=row['op_id'], operacao=operation, alvo=target,
                status_existencia_alvo='CRIACAO_DE_BLOCO_OU_CAPITULO_NOVO_NESTA_PROPOSTA' if creation else 'ALVO_EXISTENTE_NO_DOCUMENTO_VIGENTE',
                estado_anterior_do_bloco=previous, estado_proposto_pela_operacao=proposed,
                contexto_blocos_vizinhos_no_capitulo=[dict(bloco_id=b['id'], subtitulo=b['subtitulo'], texto=b['texto'])
                    for b in (chapter or {}).get('blocos', []) if creation or b['id'] != target],
                alerta_reducao_tamanho=bool(before and operation == 'substituir' and len(row['texto'].split()) < len(before['texto'].split()) * .6)))
        entries.append(dict(intervencao_id=proposal['id'], tipo_intervencao=intervention['tipo'],
            modo_validacao_suporte='MODO_PRESERVACAO_EDITORIAL_SEM_FATOS_NOVOS' if intervention['tipo'] == 'editorial' else 'EXIGE_EVIDENCIA_NOVA_PARA_FATOS_NOVOS',
            objetivo=intervention['objetivo'], sub_objetivos_com_suporte=intervention.get('sub_objetivos_com_suporte', research.get('sub_objetivos_com_suporte', [])),
            evidencias_fornecidas=supplied, operacoes=operations))
    return copy.deepcopy(dict(frase_escopo_especialista=base_doc.get('entrada', {}).get('frase_especialista', base_doc.get('frase_escopo_especialista', base_doc.get('frase_especialista', ''))),
        protecoes_especialista=protections, mapa_estrutural_documento_vigente_ANTES_deste_lote=structural,
        intervencoes_e_operacoes_propostas=entries))


def diff(base, proposals):
    chapters, blocks = catalog(base)
    result = []
    for proposal in proposals:
        for row in proposal['alteracoes']:
            before = None if row['operacao'] in ('inserir', 'novo_capitulo') else blocks.get(row['alvo'])
            result.append(dict(intervencao=proposal['id'], **row, antes=before,
                capitulo_anterior=chapters[row['alvo']]['titulo'] if row['alvo'] in chapters else None,
                alerta_reducao=bool(before and row['operacao'] == 'substituir' and len(row['texto'].split()) < len(before['texto'].split()) * .6)))
    return result
