"""Instalador de documentos profissionais, nunca de datasets de questões."""
import argparse
import csv
import hashlib
import json
import os
import re
from collections import deque
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit, urldefrag

from pipeline.domain_corpora.io_utils import HTTP, atomic_json, file_hash
from pipeline.domain_corpora.extract import pdf_pages, accepted_pages
from pipeline.domain_corpora.manifest import load_manifest
from pipeline.inventario.locking import output_lock

CATALOG = {
 'abb': {'seeds':['https://library.e.abb.com/public/34d5b70e18f7d6c8c1257be500438ac3/Oil%20and%20gas%20production%20handbook%20ed3x0_web.pdf'],
         'hosts':['new.abb.com','library.e.abb.com'], 'kind':'manual_industrial',
         'scope':['/oil-and-gas/production-book','/public/'], 'jurisdiction':'not_specified',
         'rights':'ABB: uso pessoal/não comercial e interno conforme prefácio; não redistribuir automaticamente'},
 'kimray': {'seeds':['https://kimray.com/kimray-training', 'https://kimray.com/training/oil-gas-production-follow-pipes'],
         'hosts':['kimray.com'], 'scope':['/training','/kimray-training','/sites/default/files/'],
         'kind':'treinamento_fabricante','jurisdiction':'US', 'rights':'acesso público; direitos reservados do fabricante'},
 'emerson': {'seeds':['https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d101881x012.pdf'],
         'hosts':['www.emerson.com'], 'scope':['/is/content/emerson/'],
         'kind':'manual_fabricante','jurisdiction':'not_specified','rights':'acesso público; verificar condições Emerson/Fisher'},
 'offshorenorge': {'seeds':['https://www.offshorenorge.no/en/subject-matter/guidelines/guidelines/environment/085--norwegian-oil-and-gas-recommended-guidelines-for-sampling-and-analysis-of-produced-water/',
                          'https://www.offshorenorge.no/en/subject-matter/guidelines/guidelines/'],
         'hosts':['www.offshorenorge.no'], 'scope':['/en/faginnhold/guidelines/','/en/subject-matter/guidelines/','/contentassets/'],
         'kind':'guia_offshore','jurisdiction':'NO','rights':'acesso público; verificar direitos de cada guia'},
 'imca': {'seeds':['https://www.imca-int.com/resources/safety/safety-flashes/'],
         'hosts':['www.imca-int.com'], 'scope':['/resources/safety/safety-flashes/','/media/'],
         'kind':'licao_aprendida','jurisdiction':'not_specified','rights':'IMCA Safety Flashes públicos; manter atribuição e condições'},
 'iogp': {'seeds':['https://www.iogp.org/workstreams/safety/safety/process-safety/fundamentals/'],
         'hosts':['www.iogp.org'], 'scope':['/workstreams/safety/safety/process-safety/','/bookstore/wp-content/uploads/'],
         'kind':'guia_profissional','jurisdiction':'not_specified','rights':'IOGP: atribuição e condições no documento'},
}


class HTML(HTMLParser):
    """Extrai corpo sem executar scripts; conserva links para descoberta delimitada."""
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links, self.body, self.main, self.title = [], [], [], []
        self.stack, self.skip, self.in_main, self.in_title = [], 0, 0, 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'a' and attrs.get('href'): self.links.append(attrs['href'])
        if tag in ('br','p','div','li','h1','h2','h3','tr'): self.handle_data('\n')
        if tag in ('meta','link','img','input','br','hr','source','wbr'): return
        skip = tag in ('script','style','nav','header','footer','form','noscript','svg')
        main = tag in ('main','article') or attrs.get('id') in ('content-core','main-content')
        self.stack.append((tag, skip, main))
        self.skip += skip
        self.in_main += main
        self.in_title += tag == 'title'

    def handle_endtag(self, tag):
        if not any(t[0] == tag for t in self.stack): return
        while self.stack:
            name, skip, main = self.stack.pop()
            self.skip -= skip
            self.in_main -= main
            self.in_title -= name == 'title'
            if name == tag: break

    def handle_data(self, data):
        if self.in_title: self.title.append(data)
        if not self.skip:
            self.body.append(data)
            if self.in_main: self.main.append(data)

    def text(self):
        return '\n'.join(' '.join(s.split()) for s in ''.join(self.main or self.body).splitlines() if s.strip())


def permitted(url, spec):
    p = urlsplit(url)
    return (p.scheme == 'https' and p.hostname in spec['hosts'] and not p.username
            and any(p.path.startswith(s) for s in spec['scope']))


def collect(source, root, http, limit=30, max_pages=100, depth=2):
    spec = CATALOG[source]
    queue, seen, records, errors = deque((u,0) for u in spec['seeds']), set(), [], []
    while queue and len(seen) < max_pages and len({r['document_id'] for r in records}) < limit:
        url, level = queue.popleft()
        url = urldefrag(url)[0]
        if url in seen or not permitted(url, spec): continue
        seen.add(url)
        uid = source + '-' + hashlib.sha256(url.encode()).hexdigest()[:24]
        raw = root/source/'raw'/uid
        try:
            print(f'[{source}] consultando {url}',flush=True)
            # HTTP.download mantém .part e verifica o cache por SHA-256.
            meta = http.download(url, raw)
            if not permitted(meta['final_url'], spec):
                raise ValueError('Redirecionamento saiu do catálogo permitido')
            with raw.open('rb') as stream: is_pdf=stream.read(5)==b'%PDF-'
            if is_pdf:
                pages = list(pdf_pages(raw))
                title = Path(urlsplit(url).path).name
            else:
                if raw.stat().st_size > 20*1024*1024: raise ValueError('HTML maior que 20 MiB')
                html = HTML(); html.feed(raw.read_text(encoding='utf-8', errors='replace'))
                title = ' '.join(html.title).strip() or url
                for link in html.links:
                    target = urldefrag(urljoin(url, link))[0]
                    pdf_link='.pdf' in urlsplit(target).path.lower()
                    if (level < depth or pdf_link) and permitted(target, spec) and not re.search(r'\.(jpg|png|svg|mp4|zip|xlsx?)($|\?)',target,re.I):
                        if pdf_link: queue.appendleft((target,level))
                        else: queue.append((target,level+1))
                pages = [{'page':None,'text':html.text()}]
                if source=='offshorenorge': continue  # catálogo/detalhe não substitui o PDF do guia
            pages, issues = accepted_pages(pages)
            # Índices de catálogo não contam como documentos técnicos.
            if ((url in spec['seeds'] and source in ('imca','offshorenorge')) or
                    url=='https://kimray.com/kimray-training'): continue
            base = dict(collection=source,document_id=uid,title=title,url=url,
                        source_sha256=meta['sha256'],source_kind='original',
                        source_boundary='known_document',language='not_verified',
                        jurisdiction=spec['jurisdiction'],document_type=spec['kind'],
                        license=spec['rights'],extraction_issues=issues)
            records.extend({**base,**p} for p in pages)
            print(f'[{source}] {len({r["document_id"] for r in records})}/{limit}: {title}',flush=True)
        except Exception as exc:
            errors.append({'source':source,'url':url,'error':str(exc)[:600]})
            print(f'[{source}] falha registrada: {type(exc).__name__}',flush=True)
    return records, errors, {'visited':len(seen),'remaining_urls':len(queue),'document_limit':limit}


def force(root, http, record_id='10775273'):
    """Importação CSV em fluxo; sem inventar páginas/identidade documental ausentes."""
    meta = json.loads(http.bytes('https://zenodo.org/api/records/'+record_id))
    atomic_json(root/'force'/'zenodo_record.json',meta)
    license_info = meta.get('metadata',{}).get('license',{})
    license_id = license_info.get('id','not_specified') if isinstance(license_info,dict) else str(license_info)
    csv.field_size_limit(100*1024*1024)
    dest=root/'force'/'pages.jsonl';dest.parent.mkdir(parents=True,exist_ok=True)
    documents=set();pages_written=0
    with dest.with_suffix('.tmp').open('w',encoding='utf-8') as out:
        for entry in meta['files']:
            if not entry['key'].lower().endswith('.csv'): continue
            url=entry['links'].get('self') or entry['links']['download']
            raw=root/'force'/'raw'/Path(entry['key']).name
            http.download(url,raw,entry['checksum'],entry['size'])
            with raw.open(encoding='utf-8-sig',newline='') as stream:
                reader=csv.DictReader(stream)
                columns={c.casefold().strip():c for c in reader.fieldnames or []}
                text_key=next((columns[k] for k in ('content_scrubbed_light','text','content','page_content','page_text','extracted_text') if k in columns),None)
                if text_key is None: raise ValueError('CSV FORCE sem coluna textual reconhecida: '+str(reader.fieldnames))
                for n,row in enumerate(reader):
                    text=row.get(text_key,'').strip()
                    if len(text.split())<20: continue
                    quality=row.get(text_key+'_could_be_natural_language',row.get('content_could_be_natural_language',''))
                    if str(quality).casefold() in ('false','0','no'): continue
                    filename=row.get('filename','').strip()
                    uid='force-'+hashlib.sha256((entry['key']+':'+(filename or str(n))).encode()).hexdigest()[:24]
                    page=row.get('page','')
                    page=int(page) if str(page).isdigit() and int(page)>0 else None
                    data=dict(collection='force',document_id=uid,title=filename or entry['key']+' linha '+str(n+2),
                        url='https://zenodo.org/records/'+record_id,language=row.get('langdetect','not_verified'),jurisdiction='not_specified',
                        document_type='relatorio_industrial',license=license_id,
                        source_boundary='known_document' if filename else 'unknown_csv_row',
                        document_boundaries_known=bool(filename),page=page,text=text,source_sha256=entry['checksum'],
                        upstream_metadata={k:row[k] for k in ('_id','filename','page','possible_language','langdetect') if k in row})
                    out.write(json.dumps(data,ensure_ascii=False)+'\n');documents.add(uid);pages_written+=1
    dest.with_suffix('.tmp').replace(dest)
    if not documents: raise ValueError('FORCE vazio')
    return {'id':'force','format':'pages_jsonl','path':'force/pages.jsonl','sha256':file_hash(dest),'documents':len(documents),'pages':pages_written}


def install(root, sources, http, limit=30, max_pages=100, depth=2, base=None, allow_errors=False, with_force=False):
    root=Path(root).resolve()
    with output_lock(root):
        collections,errors,discovery=[],[],{}
        # Invalida uma instalação anterior ANTES de alterar arquivos.
        atomic_json(root/'manifest.json',{'schema':'petroquest-professional-corpora-v1','ready':False})
        for source in sources:
            records,failures,trace=collect(source,root,http,limit,max_pages,depth)
            errors.extend(failures);discovery[source]=trace
            if not records:
                errors.append({'source':source,'error':'Nenhum documento utilizável'});continue
            path=root/source/'pages.jsonl';path.parent.mkdir(parents=True,exist_ok=True)
            path.write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in records),encoding='utf-8')
            collections.append({'id':source,'format':'pages_jsonl','path':path.relative_to(root).as_posix(),
                'sha256':file_hash(path),'documents':len({r['document_id'] for r in records})})
        if with_force: collections.append(force(root,http))
        if base:
            _,old=load_manifest(base)
            for c in old:
                c=dict(c)
                if c['id'] in {x['id'] for x in collections}: raise ValueError('Coleção duplicada: '+c['id'])
                if c['format']=='pages_jsonl': c['path']=os.path.relpath(c.pop('resolved_path'),root).replace(os.sep,'/')
                else:
                    c['files']=[{**{k:v for k,v in f.items() if k!='resolved_path'},
                        'path':os.path.relpath(f['resolved_path'],root).replace(os.sep,'/')} for f in c['files']]
                collections.append(c)
        result={'schema':'petroquest-professional-corpora-v1','ready':bool(collections) and (not errors or allow_errors),
            'partial':True,'sample':False,'coverage':'Acervo delimitado; limites de descoberta e erros no relatório',
            'collections':collections,'selected_sources':sources,'errors':errors,'discovery':discovery}
        atomic_json(root/'install_report.json',result);atomic_json(root/'manifest.json',result)
        return result


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path,default=Path('dataset/professional_corpora_v2'))
    p.add_argument('--sources',nargs='+',choices=sorted(CATALOG),default=['abb','kimray','emerson','offshorenorge','imca','iogp'])
    p.add_argument('--max-documents',type=int,default=30)
    p.add_argument('--max-pages',type=int,default=100)
    p.add_argument('--depth',type=int,default=2)
    p.add_argument('--base-manifest',type=Path)
    p.add_argument('--allow-errors',action='store_true')
    p.add_argument('--with-force',action='store_true',help='Download explícito adicional de aproximadamente 6,1 GB em CSV')
    p.add_argument('--ca-file')
    p.add_argument('--timeout',type=int,default=30)
    p.add_argument('--retries',type=int,default=2)
    p.add_argument('--plan',action='store_true')
    a=p.parse_args(argv)
    if min(a.max_documents,a.max_pages,a.timeout,a.retries)<1 or a.depth<0: p.error('Limites inválidos')
    if a.plan:
        print(json.dumps({s:CATALOG[s] for s in a.sources},ensure_ascii=False,indent=2));return 0
    result=install(a.output,a.sources,HTTP(ca_file=a.ca_file,timeout=a.timeout,retries=a.retries),a.max_documents,a.max_pages,a.depth,
                   a.base_manifest,a.allow_errors,a.with_force)
    print('Manifesto:',a.output/'manifest.json','| erros:',len(result['errors']))
    return 0 if result['ready'] else 2


if __name__=='__main__': raise SystemExit(main())
