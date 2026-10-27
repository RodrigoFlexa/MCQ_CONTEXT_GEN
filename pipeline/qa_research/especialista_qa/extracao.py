"""Extração OOXML offline; marcadores explícitos de gabarito, sem inferência por modelo."""
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from zipfile import ZipFile
import xml.etree.ElementTree as ET

from pipeline.inventario.textutil import atomic_json, write_jsonl

NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
W = '{' + NS['w'] + '}'
SECTION = re.compile(r'^(.+?)\s*[–—-]\s*(\d+)\s+[Qq]uest[õo]es\s*$', re.I)
NUMBER = re.compile(r'^\s*(\d{1,4})(?:[.)\-–]\s*|\s+)(?=\S)')
OPTION = re.compile(r'^\s*([A-Ea-e])\s*[).:\-–]\s*(.*)$')
KEY = re.compile(r'^[✅✔✓☑\s\-–]*(?:gabarito|resposta(?:\s+correta)?|alternativa\s+correta)\s*[:\-–]\s*\(?([A-E])\)?(?:[.)])?(?:\s|$)', re.I)
KEY_START = re.compile(r'^[✅✔✓☑\s\-–]*(?:gabarito|resposta(?:\s+correta)?|alternativa\s+correta)\s*[:\-–]', re.I)
JUST = re.compile(r'^\s*justificativa\s*[:\-–]\s*(.*)$', re.I)
CHECK = re.compile(r'[✅✔✓☑]')


def jsonl(path, rows):
    # O utilitário comum também repete bloqueios transitórios de troca no Windows/OneDrive.
    write_jsonl(path, rows)


def paragrafos(path):
    with ZipFile(path) as archive:
        raw = archive.read('word/document.xml')
        if len(raw) > 50_000_000:
            raise ValueError('DOCX excede o tamanho de XML previsto')
        root = ET.fromstring(raw)
    out = []
    for index, p in enumerate(root.findall('.//w:body//w:p', NS), 1):
        # Mantém quebras que separam enunciado, alternativas e gabarito.
        text = ''.join((n.text or '') if n.tag == W+'t' else '\n' if n.tag in (W+'br', W+'cr')
                       else '\t' if n.tag == W+'tab' else '' for n in p.iter())
        num = p.find('w:pPr/w:numPr/w:numId', NS)
        out.append({'indice': index, 'texto': text, 'lista_word': num is not None,
                    'num_id': num.get(W+'val') if num is not None else None})
    return out


def linhas(p):
    text = p['texto']
    # Alguns parágrafos contêm alternativas juntas em um único w:t.
    if len(text.splitlines()) == 1 and all(re.search(r'\b'+letter+r'\)', text) for letter in 'ABCD'):
        text = re.sub(r'(?<![A-Za-z])([A-E])\)', r'\n\1)', text)
        text = re.sub(r'(?=[✅✔✓☑]?\s*(?:Gabarito|Resposta correta|Resposta|Justificativa):)', '\n', text)
    return [t.strip() for t in text.splitlines() if t.strip()]


def extrair(path, saida):
    path, saida = Path(path), Path(saida)
    source_hash = hashlib.sha256(path.read_bytes()).hexdigest()
    paragraphs = paragrafos(path)
    rows, sections, leftovers = [], [], []
    current, section = None, None
    serial = Counter()

    def iniciar(stem, p, numero=None):
        nonlocal current
        serial[section['id']] += 1
        current = {'uid': f"especialista:{section['id']}:{serial[section['id']]:04d}",
                   'agrupamento_id': section['id'], 'agrupamento_original': section['titulo'],
                   'numero_original': numero, 'ordem_no_agrupamento': serial[section['id']],
                   'enunciado': stem, 'alternativas': {}, 'justificativa_original': '',
                   'evidencias_gabarito': [], 'problemas_extracao': [],
                   'fonte': {'arquivo': path.name, 'docx_sha256': source_hash,
                             'paragrafo_inicio': p['indice'], 'paragrafo_fim': p['indice']},
                   '_just': False, '_paragrafos': []}

    def fechar():
        nonlocal current
        if current is None:
            return
        letters = set(current['alternativas'])
        keys = {e['alternativa'] for e in current['evidencias_gabarito']}
        if letters not in (set('ABCD'), set('ABCDE')):
            current['problemas_extracao'].append('alternativas_incompletas_ou_repetidas')
        if any(not a['texto'].strip() for a in current['alternativas'].values()):
            current['problemas_extracao'].append('alternativa_vazia')
        if len(keys) != 1:
            current['problemas_extracao'].append('gabarito_ausente' if not keys else 'gabaritos_conflitantes')
        answer = next(iter(keys)) if len(keys) == 1 else None
        if answer and answer not in letters:
            current['problemas_extracao'].append('gabarito_sem_alternativa')
        current['gabarito'] = answer
        current['resposta_original'] = current['alternativas'].get(answer, {}).get('texto')
        current['texto_original'] = '\n'.join(current.pop('_paragrafos'))
        current.pop('_just')
        current['problemas_extracao'] = sorted(set(current['problemas_extracao']))
        current['status_extracao'] = 'pendente' if current['problemas_extracao'] else 'ok'
        rows.append(current)
        current = None

    for p in paragraphs:
        text = p['texto'].strip()
        if not text:
            continue
        header = SECTION.fullmatch(text)
        if header:
            fechar()
            section = {'id': f'g{len(sections)+1:02d}', 'titulo': header[1].strip(),
                       'quantidade_declarada': int(header[2]), 'paragrafo': p['indice']}
            sections.append(section)
            continue
        if section is None:
            continue  # título/autoria do documento não entram nos prompts
        ls = linhas(p)
        first = ls[0]
        number = NUMBER.match(first)
        inline = any(OPTION.match(t) for t in ls[1:])
        new = bool(number) or (inline and not OPTION.match(first))
        if new:
            fechar()
            iniciar(first[number.end():].strip() if number else first, p, int(number[1]) if number else None)
            ls = ls[1:]
        elif current is None:
            leftovers.append({'paragrafo': p['indice'], 'texto': text})
            continue
        current['fonte']['paragrafo_fim'] = p['indice']
        current['_paragrafos'].append(p['texto'])
        for line in ls:
            key = KEY.match(line)
            if key:
                current['evidencias_gabarito'].append({'alternativa': key[1].upper(),
                    'metodo': 'gabarito_explicito', 'paragrafo': p['indice'], 'texto': line})
                current['_just'] = False
                continue
            if KEY_START.match(line):
                current['problemas_extracao'].append('gabarito_incompleto')
                continue
            just = JUST.match(line)
            if just:
                current['justificativa_original'] += just[1]
                current['_just'] = True
                continue
            option = OPTION.match(line)
            if option:
                letter, content, method = option[1].upper(), option[2], 'rotulo_explicito'
                current['_just'] = False
            elif current['_just']:
                current['justificativa_original'] += ' '+line
                continue
            elif p['lista_word'] and len(current['alternativas']) < 4:
                letter, content, method = 'ABCD'[len(current['alternativas'])], line, 'ordem_lista_word'
            else:
                current['problemas_extracao'].append('linha_nao_associada')
                current.setdefault('linhas_nao_associadas', []).append({'paragrafo': p['indice'], 'texto': line})
                continue
            if letter in current['alternativas']:
                current['problemas_extracao'].append('alternativa_repetida')
            marked = CHECK.search(content) is not None
            current['alternativas'][letter] = {'texto': CHECK.sub('', content).strip(), 'metodo_rotulo': method}
            if marked:
                current['evidencias_gabarito'].append({'alternativa': letter, 'metodo': 'marca_na_alternativa',
                                                      'paragrafo': p['indice'], 'texto': line})
    fechar()
    for s in sections:
        rs = [r for r in rows if r['agrupamento_id'] == s['id']]
        s.update(extraidas=len(rs), elegiveis=sum(r['status_extracao']=='ok' for r in rs),
                 diferenca_contagem=len(rs)-s['quantidade_declarada'])
    summary = {'schema': 'extracao-especialista-v1', 'arquivo': path.name, 'docx_sha256': source_hash,
               'questoes_extraidas': len(rows), 'elegiveis': sum(r['status_extracao']=='ok' for r in rows),
               'pendentes': sum(r['status_extracao']!='ok' for r in rows), 'agrupamentos': sections,
               'paragrafos_sem_questao': leftovers,
               'motivos_pendencia': dict(Counter(m for r in rows for m in r['problemas_extracao']))}
    saida.mkdir(parents=True, exist_ok=True)
    jsonl(saida/'questoes_mcq.jsonl', rows)
    jsonl(saida/'pendencias.jsonl', [r for r in rows if r['status_extracao']!='ok'])
    atomic_json(saida/'extracao.json', summary)
    return summary
