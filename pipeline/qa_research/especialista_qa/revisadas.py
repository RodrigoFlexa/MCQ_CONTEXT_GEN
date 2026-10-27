"""Curadoria offline das MCQs revisadas: aprovação humana explícita e gabarito em negrito."""
import hashlib
import csv
import re
from collections import Counter
from pathlib import Path
from zipfile import ZipFile
import xml.etree.ElementTree as ET

from pipeline.inventario.textutil import atomic_json
from .extracao import NS, W, jsonl

CONJUNTO_AUTORAL = 'autoral_especialista'
CONJUNTO_REVISADAS = 'mcq_revisada_aprovada'
ROTULOS = {CONJUNTO_AUTORAL: 'MCQs autorais do especialista',
           CONJUNTO_REVISADAS: 'MCQs revisadas e aprovadas pelo especialista'}
QUESTAO = re.compile(r'^\s*(\d+)\.\s+(.+)$', re.S)
ALTERNATIVA = re.compile(r'^\s*([A-E])\)\s*(.*)$', re.S)
# Grafias do rótulo presentes no documento. O teor do parecer nunca é corrigido.
COMENTARIO = re.compile(r'^\s*(?:Comentário|Cimentário|Comenário|Comentpario|Comnetário)\s*:\s*(.*)$', re.I | re.S)
REGRA_APROVACAO = r'(?:aprovad[ao]|aprovar)[\s.!]*'


def classificar_parecer(texto):
    """Não adivinha status em textos livres nem transforma ressalvas em aprovação simples."""
    texto = texto.strip()
    if not texto:
        return 'sem_parecer'
    if re.fullmatch(REGRA_APROVACAO, texto, re.I):
        return 'aprovada_sem_observacoes'
    if re.match(r'^(?:descart|desaprov|reprov|não\s+aprov)', texto, re.I):
        return 'descartada_ou_reprovada'
    if re.match(r'^(?:aprov|aprovar|arpov)', texto, re.I):
        return 'aprovacao_com_observacoes_ou_ressalvas'
    return 'parecer_indeterminado'


def texto_xml(element):
    return ''.join((n.text or '') if n.tag == W+'t' else '\n' if n.tag in (W+'br', W+'cr')
                   else '\t' if n.tag == W+'tab' else '' for n in element.iter())


def extrair_revisadas(path, saida):
    path, saida = Path(path), Path(saida)
    source_hash = hashlib.sha256(path.read_bytes()).hexdigest()
    with ZipFile(path) as z:
        raw = z.read('word/document.xml')
        if len(raw) > 50_000_000:
            raise ValueError('DOCX excede o tamanho de XML previsto')
        root = ET.fromstring(raw)
        styles = ET.fromstring(z.read('word/styles.xml')) if 'word/styles.xml' in z.namelist() else None
        style_names = {s.get(W+'styleId'): n.get(W+'val', '') for s in styles.findall('w:style', NS)
                       if (n := s.find('w:name', NS)) is not None} if styles is not None else {}
    if root.findall('.//w:tbl', NS):
        raise ValueError('Layout com tabelas exige revisão do extrator')
    rows, current = [], None
    topic, subtopic, group = '', '', 0
    serial = Counter()

    def fechar():
        nonlocal current
        if current is None:
            return
        r = current
        keys = {e['alternativa'] for e in r['evidencias_gabarito']}
        issues = r['problemas_extracao']
        if set(r['alternativas']) not in (set('ABCD'), set('ABCDE')):
            issues.append('alternativas_incompletas')
        if any(not a['texto'].strip() for a in r['alternativas'].values()):
            issues.append('alternativa_vazia')
        if len(keys) != 1:
            issues.append('gabarito_em_negrito_ausente_ou_ambiguo')
        if not r['agrupamento_original']:
            issues.append('topico_ausente')
        comments = r.pop('_comentarios')
        comment = '\n'.join(comments)
        if len(comments) > 1:
            issues.append('multiplos_pareceres')
        status = classificar_parecer(comment)
        r['revisao_humana'] = {'parecer_original': comment, 'status': status,
                              'aprovacao_simples': status == 'aprovada_sem_observacoes'}
        r['gabarito'] = next(iter(keys)) if len(keys) == 1 else None
        r['resposta_original'] = r['alternativas'].get(r['gabarito'], {}).get('texto', '')
        r['status_extracao'] = 'pendente' if issues else 'ok'
        r['selecionada_para_conversao'] = r['revisao_humana']['aprovacao_simples'] and not issues
        r['texto_original'] = '\n'.join(r.pop('_paragrafos'))
        rows.append(r)
        current = None

    for index, p in enumerate(root.findall('.//w:body/w:p', NS), 1):
        text = texto_xml(p).strip()
        if not text:
            continue
        style = p.find('w:pPr/w:pStyle', NS)
        style = style.get(W+'val', '') if style is not None else ''
        level = re.search(r'(?:Heading|T.tulo)\s*([12])$', style_names.get(style, style), re.I)
        if level:
            fechar()
            if level[1] == '1':
                topic, subtopic = text, ''
                # O sumário usa Heading1, mas não é uma área do banco.
                if text.casefold() != 'sumário':
                    group += 1
            else:
                subtopic = text
            continue
        m = QUESTAO.match(text)
        if m:
            fechar()
            number = int(m[1])
            serial[group] += 1
            current = {'uid': f'especialista_revisada:{number:04d}', 'conjunto_especialista': CONJUNTO_REVISADAS,
                       'agrupamento_id': f'r{group:02d}', 'agrupamento_original': topic,
                       'subtopico_original': subtopic or None, 'numero_original': number,
                       'ordem_no_agrupamento': serial[group], 'enunciado': m[2], 'alternativas': {},
                       'justificativa_original': '', 'evidencias_gabarito': [], 'problemas_extracao': [],
                       'fonte': {'arquivo': path.name, 'docx_sha256': source_hash,
                                 'paragrafo_inicio': index, 'paragrafo_fim': index},
                       '_comentarios': [], '_paragrafos': [text]}
            continue
        if current is None:
            continue
        current['_paragrafos'].append(text)
        current['fonte']['paragrafo_fim'] = index
        m = COMENTARIO.match(text)
        if m:
            current['_comentarios'].append(m[1])
            continue
        m = ALTERNATIVA.match(text)
        if m:
            letter, answer = m[1], m[2].strip()
            if letter in current['alternativas']:
                current['problemas_extracao'].append('rotulo_alternativa_repetido')
            current['alternativas'][letter] = {'texto': answer, 'metodo_rotulo': 'rotulo_explicito'}
            runs = [(texto_xml(r).strip(), r.find('w:rPr/w:b', NS)) for r in p.findall('w:r', NS)]
            bold_chars = sum(len(t) for t, b in runs if b is not None and b.get(W+'val', 'true') not in ('0', 'false', 'off'))
            # Negrito em uma palavra ou apenas na letra não prova que esta é a resposta.
            if bold_chars >= .8*len(text):
                current['evidencias_gabarito'].append({'alternativa': letter, 'metodo': 'alternativa_em_negrito',
                                                       'paragrafo': index, 'texto': text})
        else:
            current['problemas_extracao'].append('paragrafo_nao_interpretado')
    fechar()
    if len({r['uid'] for r in rows}) != len(rows):
        raise ValueError('Números originais repetidos; revisar IDs antes de exportar')
    selected = [r for r in rows if r['selecionada_para_conversao']]
    summary = {'schema': 'curadoria-mcq-revisada-v1', 'arquivo': path.name, 'docx_sha256': source_hash,
               'total_mcq': len(rows), 'pareceres': dict(Counter(r['revisao_humana']['status'] for r in rows)),
               'selecionadas': len(selected), 'excluidas': len(rows)-len(selected),
               'regra_aprovacao': REGRA_APROVACAO,
               'criterio': 'Apenas aprovação explícita sem texto adicional. Observações, ressalvas, grafias ambíguas e ausência de parecer ficam fora.',
               'pendencias_extracao': dict(Counter(x for r in rows for x in r['problemas_extracao'])),
               'por_agrupamento': [{'agrupamento': t, 'total': sum(r['agrupamento_original'] == t for r in rows),
                   'selecionadas': sum(r['agrupamento_original'] == t for r in selected)}
                   for t in dict.fromkeys(r['agrupamento_original'] for r in rows)]}
    jsonl(saida/'curadoria_todas.jsonl', rows)
    jsonl(saida/'aprovadas_mcq.jsonl', selected)
    atomic_json(saida/'extracao.json', summary)
    with (saida/'curadoria.csv').open('w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['uid', 'numero_original', 'agrupamento_original', 'subtopico_original',
                         'parecer_original', 'status_humano', 'selecionada_para_conversao', 'problemas_extracao'])
        for r in rows:
            writer.writerow([r['uid'], r['numero_original'], r['agrupamento_original'], r['subtopico_original'],
                             r['revisao_humana']['parecer_original'], r['revisao_humana']['status'],
                             r['selecionada_para_conversao'], '; '.join(r['problemas_extracao'])])
    return summary


def ler_entradas(path):
    """Manifesto pequeno referencia os dois JSONLs, sem duplicar a entrada autoral."""
    import json
    path = Path(path)
    if path.suffix == '.json':
        manifest = json.loads(path.read_text(encoding='utf-8-sig'))
        if manifest.get('schema') != 'fontes-especialista-v1':
            raise ValueError('Manifesto de entradas desconhecido')
        rows = []
        for source in manifest['fontes']:
            target = (path.parent/source['path']).resolve()
            if not target.is_relative_to(path.parent.resolve()):
                raise ValueError('Entrada deve permanecer dentro da pasta do manifesto')
            part = ler_entradas(target)
            if len(part) != source['questoes'] or any(r['conjunto_especialista'] != source['id'] for r in part):
                raise ValueError('Contagem ou identificação da fonte divergente do manifesto')
            rows.extend(part)
        return rows
    rows = [json.loads(line) for line in path.read_text(encoding='utf-8-sig').splitlines() if line.strip()]
    for r in rows:
        source = r.setdefault('conjunto_especialista', CONJUNTO_AUTORAL)
        if source not in ROTULOS:
            raise ValueError('Conjunto do especialista desconhecido')
        if source == CONJUNTO_REVISADAS:
            review = r.get('revisao_humana', {})
            if (classificar_parecer(review.get('parecer_original', '')) != 'aprovada_sem_observacoes'
                    or review.get('aprovacao_simples') is not True or review.get('status') != 'aprovada_sem_observacoes'
                    or r.get('selecionada_para_conversao') is not True):
                raise ValueError('MCQ revisada sem aprovação humana simples: não enviar ao modelo')
        elif r['uid'].startswith('especialista_revisada:') or 'revisao_humana' in r:
            raise ValueError('MCQ revisada com identificação de fonte incorreta')
    return rows
