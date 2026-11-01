"""Feeds são caminhos para documentos, nunca um documento técnico agregado."""
import re
from urllib.parse import urlsplit
from xml.etree import ElementTree as ET


def navigation_reason(row):
    path = urlsplit(row.get('url') or '').path.lower().rstrip('/')
    if re.search(r'/(?:rss(?:-feed)?|feed|atom)(?:\.xml)?$', path):
        return 'feed de descoberta, sem fronteira de documento individual'
    if len(row.get('title') or '') > 2000:
        return 'título anormal; conferir extração antes de usar como evidência'
    if row.get('document_type') in ('feed', 'catalogo'):
        return 'índice de navegação'
    return None


def feed_links(content):
    """None para HTML; lista (inclusive vazia) para RSS/Atom. Sem resolver entidades."""
    if not re.search(r'<(?:\w+:)?(?:rss|feed|RDF)\b', content[:4096], re.I):
        return None
    if re.search(r'<!DOCTYPE|<!ENTITY', content, re.I):
        raise ValueError('Feed com declaração de entidades não é aceito')
    root = ET.fromstring(content)
    local = lambda tag: tag.rsplit('}', 1)[-1].lower()
    links = []
    for entry in root.iter():
        if local(entry.tag) not in ('item', 'entry'):
            continue
        for node in entry:
            if local(node.tag) == 'link' and node.get('rel', 'alternate') == 'alternate':
                value = node.get('href') or (node.text or '').strip()
                if value and value not in links:
                    links.append(value)
    return links
