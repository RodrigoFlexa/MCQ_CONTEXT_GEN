"""Extração textual: não usa OCR nem inventa texto a partir de figuras."""
import re
import xml.etree.ElementTree as ET
from pathlib import Path

EXTRACTION_VERSION='pages-v1'
class ExtractionRejected(ValueError):
    """Documento sem texto suficiente: quarentena, não uma falha de download."""


def clean_text(text):
    text=text.replace('\x00','').replace('\u00ad','')
    # Une palavra quebrada por hífen de fim de linha, preservando demais hífens.
    text=re.sub(r'(?<=[a-zá-ú])[-]\s*\n\s*(?=[a-zá-ú])','',text)
    return '\n'.join(' '.join(line.split()) for line in text.splitlines()).strip()


def pdf_pages(path):
    from pypdf import PdfReader
    with Path(path).open('rb') as stream:
        if stream.read(5)!=b'%PDF-':raise ValueError('URL não retornou PDF válido')
    reader=PdfReader(path,strict=False)
    if reader.is_encrypted and not reader.decrypt(''):raise ValueError('PDF protegido')
    for page_index,page in enumerate(reader.pages,1):
        yield {'page':page_index,'text':clean_text(page.extract_text() or '')}


def regis_pages(raw):
    """REGIS é XML por documento, não qrels/queries nem um pacote de PDFs."""
    if b'<!DOCTYPE' in raw.upper() or b'<!ENTITY' in raw.upper():raise ValueError('XML com DTD/entidades não permitido')
    root=ET.fromstring(raw)
    def local(element):return element.attrib.get('name',element.tag.rsplit('}',1)[-1]).lower()
    # O formato real tem TEXT/BODY; metadados não são suporte factual.
    body=[e for e in root.iter() if local(e) in ('text','body','fulltext','content')]
    if not body:raise ValueError('Documento REGIS sem campo de corpo textual reconhecido')
    text=clean_text('\n'.join(''.join(e.itertext()) for e in body))
    title=next((clean_text(' '.join(e.itertext())) for e in root.iter()
                if local(e) in ('title','titulo','filename')), '')
    docid=next((clean_text(' '.join(e.itertext())) for e in root.iter()
                if local(e) in ('docno','docid','id')), '')
    # XML original não informa paginação confiável: page=null, sem fabricar páginas.
    return title,docid,[{'page':None,'text':text}]


def accepted_pages(pages):
    kept=[];issues=[]
    for page in pages:
        text=page['text'];words=text.split()
        letters=sum(c.isalpha() for c in text)
        if len(words)<20 or letters/max(len(text),1)<.35:
            issues.append({'page':page['page'],'reason':'little_or_no_extractable_text','words':len(words)})
        else:kept.append(page)
    if not kept:raise ExtractionRejected('Sem texto extraível suficiente; requer OCR/revisão, não entra no corpus')
    return kept,issues
