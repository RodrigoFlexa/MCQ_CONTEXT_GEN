"""Instalador de documentos profissionais, nunca de datasets de questões."""
import argparse
import csv
import hashlib
import json
import os
import re
import importlib.util
from collections import deque
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit, urldefrag

from pipeline.domain_corpora.io_utils import HTTP, atomic_json, file_hash
from pipeline.domain_corpora.extract import pdf_pages, accepted_pages
from pipeline.domain_corpora.manifest import load_manifest
from pipeline.inventario.locking import output_lock
from .language import detect_language

EXTRACTION_REVISION='professional-pages-v2.2-language'


def collection_files(collection):
    return collection.get('files',[]) if collection['format']=='petroles_txt' else [collection]


def same_content(a,b):
    return a['format']==b['format'] and sorted(f['sha256'] for f in collection_files(a))==sorted(f['sha256'] for f in collection_files(b))


def error_record(source,url,exc):
    message=str(exc)
    category='download_or_extraction'
    action='Repetir a coleta; verificar URL e conectividade.'
    if isinstance(exc,ImportError) or 'cryptography' in message or 'AES algorithm' in message:
        category='missing_dependency'
        action='Instalar requirements.txt do v2, que inclui pypdf[crypto], no mesmo Python da coleta.'
    elif 'protegido' in message.casefold() or 'password' in message.casefold():
        category='password_protected';action='Documento exige senha; não será desbloqueado pelo coletor.'
    elif isinstance(exc,TimeoutError) or 'timed out' in message:
        category='timeout';action='Repetir --retry-failed ou aumentar --timeout.'
    return dict(source=source,url=url,error=message[:600],category=category,action=action)


def existing_records(root,source):
    """Admite somente coleção cujo hash foi publicado no relatório anterior."""
    report=root/'install_report.json'
    if not report.exists(): return []
    data=json.loads(report.read_text(encoding='utf-8'))
    entry=next((c for c in data.get('collections',[]) if c['id']==source),None)
    if not entry:return []
    path=(root/entry['path']).resolve()
    if not path.is_relative_to(root) or not path.is_file() or file_hash(path)!=entry['sha256']:
        raise ValueError('Coleção anterior corrompida; não será reutilizada: '+source)
    rows=[json.loads(s) for s in path.read_text(encoding='utf-8').splitlines() if s.strip()]
    if any(r.get('collection')!=source for r in rows):raise ValueError('Proveniência anterior inválida')
    return rows

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


def collect(source, root, http, limit=30, max_pages=100, depth=2, retry_urls=None):
    spec = CATALOG[source]
    previous=existing_records(root,source)
    records=list(previous) if retry_urls is not None else []
    queue,seen,errors=deque((u,0) for u in (retry_urls if retry_urls is not None else spec['seeds'])),set(),[]
    reused=0
    while queue and len(seen)<max_pages and (retry_urls is not None or len({r['document_id'] for r in records})<limit):
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
            cache=root/source/'extracted'/(uid+'.json')
            if cache.exists():
                try:saved=json.loads(cache.read_text(encoding='utf-8'))
                except json.JSONDecodeError:saved={}  # reextrai do original íntegro
                if (saved.get('revision')==EXTRACTION_REVISION and saved.get('raw_sha256')==meta['sha256']
                        and saved.get('rows_sha256')==hashlib.sha256(json.dumps(saved.get('rows'),sort_keys=True,ensure_ascii=False).encode()).hexdigest()):
                    records=[r for r in records if r['document_id']!=uid]+saved['rows'];reused+=1
                    print(f'[{source}] documento normalizado reutilizado',flush=True);continue
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
                        source_boundary='known_document',language='und',
                        jurisdiction=spec['jurisdiction'],document_type=spec['kind'],
                        license=spec['rights'],extraction_issues=issues)
            normalized=[]
            for page in pages:
                signal=detect_language(page['text'])
                normalized.append({**base,**page,'language':signal['language'],'language_detection':signal})
            atomic_json(cache,dict(revision=EXTRACTION_REVISION,raw_sha256=meta['sha256'],rows=normalized,
                rows_sha256=hashlib.sha256(json.dumps(normalized,sort_keys=True,ensure_ascii=False).encode()).hexdigest()))
            records=[r for r in records if r['document_id']!=uid]+normalized
            print(f'[{source}] {len({r["document_id"] for r in records})}/{limit}: {title}',flush=True)
        except Exception as exc:
            errors.append(error_record(source,url,exc))
            print(f'[{source}] falha registrada: {type(exc).__name__}',flush=True)
    # Recoleta incompleta nunca apaga documentos anteriores íntegros.
    have={r['document_id'] for r in records}
    records.extend(r for r in previous if r['document_id'] not in have)
    return records, errors, {'visited':len(seen),'remaining_urls':len(queue),'document_limit':limit,
        'normalized_reused':reused,'previous_documents_preserved':len({r['document_id'] for r in previous}-have)}


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


def install(root, sources, http, limit=30, max_pages=100, depth=2, base=None, allow_errors=False, with_force=False,
            retry_failed=False,strict=False):
    root=Path(root).resolve()
    if base and Path(base).resolve().parent==root:raise ValueError('O manifesto base deve ficar separado da instalação de destino')
    with output_lock(root):
        prior=json.loads((root/'install_report.json').read_text(encoding='utf-8')) if (root/'install_report.json').exists() else {}
        if retry_failed and not prior:raise ValueError('--retry-failed exige install_report.json anterior')
        collections,errors,discovery=[],[],dict(prior.get('discovery',{}))
        for c in prior.get('collections',[]):
            if all((root/f['path']).is_file() and file_hash(root/f['path'])==f['sha256'] for f in collection_files(c)):collections.append(c)
            else:raise ValueError('Coleção anterior mudou; preserve o acervo e instale em outro destino: '+c['id'])
        processed=set(sources)
        errors.extend(e for e in prior.get('errors',[]) if e.get('source') not in processed)
        # Invalida uma instalação anterior ANTES de alterar arquivos.
        atomic_json(root/'manifest.json',{'schema':'petroquest-professional-corpora-v1','ready':False})
        for source in sources:
            urls=None
            if retry_failed:
                urls=[e['url'] for e in prior.get('errors',[]) if e.get('source')==source and e.get('url')]
                # Relatórios copiados de Markdown também podem ser diagnosticados sem visitar outro domínio.
                urls=[re.sub(r'^\[[^\]]*\]\((https://[^)]+)\)$',r'\1',u) for u in urls]
                if not urls:continue
                if any(not permitted(u,CATALOG[source]) for u in urls):raise ValueError('URL de retomada fora do catálogo')
            records,failures,trace=collect(source,root,http,limit,max_pages,depth,retry_urls=urls)
            errors.extend(failures);discovery[source]=trace
            if not records:
                errors.append({'source':source,'error':'Nenhum documento utilizável'});continue
            path=root/source/'pages.jsonl';path.parent.mkdir(parents=True,exist_ok=True)
            tmp=path.with_suffix('.tmp');tmp.write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in records),encoding='utf-8');tmp.replace(path)
            collections=[c for c in collections if c['id']!=source]
            collections.append({'id':source,'format':'pages_jsonl','path':path.relative_to(root).as_posix(),
                'sha256':file_hash(path),'documents':len({r['document_id'] for r in records})})
        if with_force:
            try:
                entry=force(root,http);collections=[c for c in collections if c['id']!='force']+[entry]
            except Exception as exc:errors.append(error_record('force','https://zenodo.org/records/10775273',exc))
        if base:
            _,old=load_manifest(base)
            for c in old:
                c=dict(c)
                if c['id'] in {x['id'] for x in collections}:
                    if same_content(c,next(x for x in collections if x['id']==c['id'])):continue
                    raise ValueError('Coleção duplicada diferente: '+c['id'])
                if c['format']=='pages_jsonl': c['path']=os.path.relpath(c.pop('resolved_path'),root).replace(os.sep,'/')
                else:
                    c['files']=[{**{k:v for k,v in f.items() if k!='resolved_path'},
                        'path':os.path.relpath(f['resolved_path'],root).replace(os.sep,'/')} for f in c['files']]
                collections.append(c)
        expected=set(prior.get('selected_sources',[]))|set(sources)
        if with_force:expected.add('force')
        missing=sorted(expected-{c['id'] for c in collections})
        blocking=[e for e in errors if e.get('category')=='missing_dependency']
        usable=bool(collections) and not blocking and (not missing or allow_errors) and (not strict or not errors)
        result={'schema':'petroquest-professional-corpora-v1','ready':usable,
            'partial':True,'sample':False,'coverage':'Acervo delimitado; limites de descoberta e erros no relatório',
            'collections':collections,'selected_sources':sorted(expected),'errors':errors,'discovery':discovery,
            'status':'ready_with_warnings' if usable and errors else ('ready' if usable else 'blocked'),
            'missing_sources':missing,'blocking_errors':blocking,
            'readiness_policy':'Uma falha documental não invalida coleções íntegras; dependências ausentes e fontes vazias bloqueiam. --strict bloqueia qualquer erro.'}
        atomic_json(root/'install_report.json',result);atomic_json(root/'manifest.json',result)
        return result


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path,default=Path('dataset/professional_corpora_v2'))
    p.add_argument('--sources',nargs='+',choices=sorted(CATALOG))
    p.add_argument('--max-documents',type=int,default=30)
    p.add_argument('--max-pages',type=int,default=100)
    p.add_argument('--depth',type=int,default=2)
    p.add_argument('--base-manifest',type=Path)
    p.add_argument('--allow-errors',action='store_true')
    p.add_argument('--retry-failed',action='store_true',help='Reprocessa somente URLs com falha e preserva as coleções já baixadas')
    p.add_argument('--strict',action='store_true',help='Bloqueia o manifesto se qualquer documento falhar')
    p.add_argument('--with-force',action='store_true',help='Download explícito adicional de aproximadamente 6,1 GB em CSV')
    p.add_argument('--ca-file')
    p.add_argument('--timeout',type=int,default=30)
    p.add_argument('--retries',type=int,default=2)
    p.add_argument('--plan',action='store_true')
    a=p.parse_args(argv)
    if a.sources is None:
        if a.retry_failed and (a.output/'install_report.json').is_file():
            previous=json.loads((a.output/'install_report.json').read_text(encoding='utf-8'))
            a.sources=[s for s in previous.get('selected_sources',[]) if s in CATALOG]
        else:a.sources=list(CATALOG)
    if min(a.max_documents,a.max_pages,a.timeout,a.retries)<1 or a.depth<0: p.error('Limites inválidos')
    if a.plan:
        print(json.dumps({s:CATALOG[s] for s in a.sources},ensure_ascii=False,indent=2));return 0
    missing=[name for name in ('pypdf','cryptography','langdetect') if importlib.util.find_spec(name) is None]
    if missing:
        import sys
        print('Dependências ausentes:',', '.join(missing))
        print('Use o mesmo Python: '+sys.executable+' -m pip install -r pipeline/qa_research/v2/requirements.txt')
        return 2
    result=install(a.output,a.sources,HTTP(ca_file=a.ca_file,timeout=a.timeout,retries=a.retries),a.max_documents,a.max_pages,a.depth,
                   a.base_manifest,a.allow_errors,a.with_force,a.retry_failed,a.strict)
    print('Manifesto:',a.output/'manifest.json','| erros:',len(result['errors']))
    return 0 if result['ready'] else 2


if __name__=='__main__': raise SystemExit(main())
