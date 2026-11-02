"""Edição explícita e reproduzível para o piloto, sem tocar os snapshots anteriores."""
import copy
import json
from pathlib import Path
from pipeline.inventario.textutil import atomic_json
from pipeline.qa_research.v3.runtime import ROOT, digest
from pipeline.qa_research.polimento.documents import markdown

REPORTS = ROOT / 'pipeline/qa_research/relatorios'
LATEST = REPORTS / 'polimento_3_contextos_20261101T231615'
INTERMEDIATE = REPORTS / 'polimento_3_contextos_20261101T210304'
OLD = REPORTS / 'dez_areas_final_v2'
PENDING = {
    '02_02': ['Complementação específica de bombas dosadoras, LDHI e outros itens do parecer requer pesquisa separada.'],
    '03_03': ['Tratamento e gerenciamento da água de lastro continuam incompletos.'],
    '07_01': ['Backups, restauração, controle de acesso e sobressalentes permanecem sem desenvolvimento suficiente.'],
}


def load(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def flatten(document):
    return [dict(id=f'B{i:03}', capitulo=c['titulo'], subtitulo=b['subtitulo'], texto=b['texto'])
            for i, (c, b) in enumerate(((c, b) for c in document['capitulos'] for b in c['blocos']), 1)]


def close_pilot(item, source=LATEST, previous=INTERMEDIATE):
    original = load(Path(source) / item / 'documento_para_revisao.json')
    document, changes = copy.deepcopy(original), []

    def block(chapter, number):
        return document['capitulos'][chapter - 1]['blocos'][number - 1]

    def replace(b, old, new, why):
        if old not in b['texto']:
            raise ValueError('Base mudou; conferir ajuste explícito: ' + old[:80])
        before = b['texto']; b['texto'] = before.replace(old, new)
        changes.append(dict(subtitulo=b['subtitulo'], motivo=why, antes=before, depois=b['texto']))

    if item == '02_02':
        replace(block(4, 5), ', o que não elimina por si só o risco de bioincrustação a jusante', '', 'Retirar duplicação na mesma explicação')
        for ci, bi, a, b in [(4, 3, 'Os mecanismos descritos incluem', 'Os mecanismos de atuação incluem'),
                             (8, 5, 'Entre os indicadores citados para esse acompanhamento estão', 'Entre os indicadores empregados nesse acompanhamento estão'),
                             (11, 2, 'Em sistemas automatizados, foram sugeridos controles', 'Em sistemas automatizados, podem ser implementados controles')]:
            replace(block(ci, bi), a, b, 'Conhecimento autônomo, sem relato de leitura')
        b = block(11, 3); start = b['texto'].index('Em uma operação acompanhada,'); end = b['texto'].index('O efeito prático é', start)
        replace(b, b['texto'][start:end], '', 'Retirar caso circunstancial; preservar os mecanismos e conclusão já presentes')
        old = block(1, 3); fixed = load(Path(previous) / item / 'documento_para_revisao.json')['capitulos'][0]['blocos'][2]
        changes.append(dict(subtitulo=old['subtitulo'], motivo='Recuperar distinção de categorias aprovada na rodada intermediária', antes=old['texto'], depois=fixed['texto']))
        old.update(fixed)
        chapter = document['capitulos'][6]; definition = chapter['blocos'].pop(4); chapter['blocos'].insert(0, definition)
        changes.append(dict(motivo='Apresentar definição de MEG antes das aplicações', subtitulo=definition['subtitulo'], operacao='mover'))
    elif item == '03_03':
        prior = load(Path(previous) / item / 'documento_para_revisao.json')
        addition = next(b for c in prior['capitulos'] for b in c['blocos'] if b['subtitulo'].startswith('P/V valves, mast risers'))
        document['capitulos'][2]['blocos'].append(copy.deepcopy(addition))
        changes.append(dict(subtitulo=addition['subtitulo'], motivo='Recuperar inclusão aprovada da rodada intermediária', antes=None, depois=addition['texto']))
        replace(block(2, 4), 'Casos de investigação também mostram outro risco: ', '', 'Retirar relato mantendo a relação de risco já descrita')
        replace(block(2, 4), 'Um evento isolado não transforma essa prática em regra geral, mas evidencia que linhas', 'Linhas', 'Retirar comentário sobre evento isolado')
        b = block(3, 4); start = b['texto'].index('Há contextos em que vapores de tankage'); end = b['texto'].index('Como complemento conceitual, ', start)
        replace(b, b['texto'][start:end], '', 'Retirar composição de caso específico sem generalizá-la')
        replace(b, 'Como complemento conceitual, as emissões', 'As emissões', 'Retirar comentário de elaboração')
    elif item == '07_01':
        b = block(2, 5); start = b['texto'].index('Foi proposto um método'); end = b['texto'].index('Esse tipo de compensação', start)
        replace(b, b['texto'][start:end], '', 'Retirar resultado de método particular mantendo mecanismo e compromisso com desgaste')
        b = block(3, 1); start = b['texto'].index('Em um circuito de regeneração,'); end = b['texto'].index('O princípio técnico transferível é que ', start)
        replace(b, b['texto'][start:end], '', 'Concentrar o exemplo com N2 no bloco de comissionamento de segurança')
        replace(b, 'O princípio técnico transferível é que testes integrados', 'Testes integrados', 'Explicar diretamente a função dos testes')
        b = block(3, 7); start = b['texto'].index('Em um caso investigado em FPSO,'); end = b['texto'].index('Quando ações são concluídas', start)
        replace(b, b['texto'][start:end], '', 'Preservar rastreabilidade sem relato de caso')
        start = b['texto'].index(' Em tecnologias com poucas aplicações'); replace(b, b['texto'][start:], '', 'Retirar fechamento desconectado de intervenções lógicas temporárias')
    else:
        raise ValueError('Documento sem fechamento editorial explícito: ' + item)
    protections = load(Path(source) / item / 'base.json')['protecoes']
    body = '\n'.join(b['texto'] for c in document['capitulos'] for b in c['blocos'])
    if not all(p['requisito'] in body for p in protections):
        raise ValueError('Correção do especialista não foi conservada')
    return document, dict(item=item, origem=str(Path(source) / item), antes_sha256=digest(original),
        depois_sha256=digest(document), alteracoes=changes, protecoes_preservadas=True,
        pendencias=PENDING[item], status='piloto_com_escopo_delimitado',
        criterio='Revisão editorial explícita; não é certificação integral nem liberação ampla da coleção')


def prepare(destination, items):
    destination = Path(destination)
    identity = dict(versao='fechamento-piloto-1', items=items, fontes={}, documentos={})
    prepared = []
    for item in items:
        document, report = close_pilot(item)
        old = load(OLD / item / 'documento.json')
        identity['documentos'][item] = report
        identity['fontes'][item] = digest([old, document, report])
        prepared.append((item, old, document, report))
    saved = destination / 'manifesto.json'
    if saved.exists() and load(saved) != identity:
        raise ValueError('Preparação mudou; use nova saída')
    for item, old, document, report in prepared:
        for condition, doc in [('antigo', old), ('refinado', document)]:
            folder = destination / condition / item
            atomic_json(folder / 'documento.json', doc)
            # O exportador não exige IDs nos textos limpos.
            (folder / 'documento.md').write_text(markdown(doc), encoding='utf-8')
        atomic_json(destination / 'refinado' / item / 'revisao.json', report)
    atomic_json(saved, identity)
    return identity
