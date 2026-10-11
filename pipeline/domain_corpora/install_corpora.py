"""Baixa ANP/HSE/BSEE/REGIS e registra Petrolês no mesmo manifesto.

Uso completo: python pipeline/domain_corpora/install_corpora.py --petroles-dir PATH
Amostra: acrescente --max-documents-per-source 2 --output dataset/corpora_smoke
Não usa Azure. TLS permanece verificado; suporta --ca-file para rede corporativa.
"""
import argparse
import hashlib
import json
import os
import sys
import zipfile
from collections import Counter, deque
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlsplit, urldefrag

ROOT=Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
from pipeline.domain_corpora.catalog import SOURCES, DIRECT, INDEXES, REGIS_RECORD
from pipeline.domain_corpora.io_utils import HTTP, RemoteZIP, atomic_json, file_hash
from pipeline.domain_corpora.extract import pdf_pages, regis_pages, accepted_pages, EXTRACTION_VERSION, ExtractionRejected

SCHEMA='petroquest-domain-corpora-v1'
PETROLES_FILES=('corpusPublico(sem IBICT)-SemProcessamento.txt','corpusPublicoIBICT-SemProcessamento.txt')


def identity(value):return hashlib.sha256(value.encode()).hexdigest()[:24]
def now():return datetime.now(timezone.utc).isoformat()
def relative(path,base):return Path(os.path.relpath(Path(path).resolve(),Path(base).resolve())).as_posix()


def canonical_document_url(source,url):
    # Migração confirmada no portal ANP: links antigos ainda constam do índice,
    # mas PDFs estão no diretório novo. A URL original permanece na proveniência.
    if source=='anp' and urlsplit(url).netloc=='www.gov.br' and urlsplit(url).path.startswith('/anp/'):
        return url.replace('/seguranca-operacional-e-meio-ambiente/','/seguranca-operacional/')
    return url


def html_links(content,url):
    from bs4 import BeautifulSoup
    soup=BeautifulSoup(content,'html.parser')
    main=soup.select_one('#content-core') or soup.select_one('main') or soup.select_one('#main-content')
    if main is None:raise ValueError('Página sem área de conteúdo reconhecida: '+url)
    for a in main.select('a[href]'):
        link=urldefrag(urljoin(url,a['href']))[0]
        if urlsplit(link).scheme=='https':yield link,a.get_text(' ',strip=True)


def in_scope(source,url):
    parts=urlsplit(url)
    if source=='anp':return parts.netloc=='www.gov.br' and parts.path.startswith('/anp/') and (
        'seguranca-operacional' in parts.path or 'relatorio' in parts.path)
    if source=='hse':return parts.netloc=='www.hse.gov.uk' and parts.path.startswith('/offshore/')
    if source=='bsee':return parts.netloc=='www.bsee.gov'
    return False


def discover(source,http,root,limit,warnings):
    """Navegação delimitada ao domínio e seção técnica; não coleta menus gerais."""
    pdfs={url:Path(urlsplit(url).path).name for url in DIRECT[source]}
    if limit and len(pdfs)>=limit:return list(pdfs.items())[:limit]
    queue=deque((u,0) for u in INDEXES[source]);seen=set()
    while queue:
        url,depth=queue.popleft()
        url=canonical_document_url(source,url)
        if url in seen:continue
        seen.add(url)
        if len(seen)>2000:
            raise RuntimeError('Descoberta excedeu 2.000 páginas; revise o catálogo antes de continuar')
        if len(seen)%25==0:print(f'[{source}] catálogo: {len(seen)} páginas, {len(pdfs)} PDFs',flush=True)
        cache=root/'catalog_cache'/f'{identity(url)}.html'
        try:
            if cache.exists():content=cache.read_bytes()
            else:
                content=http.bytes(url);cache.parent.mkdir(parents=True,exist_ok=True);cache.write_bytes(content)
            links=list(html_links(content,url))
        except Exception as error:
            warnings.append({'source':source,'url':url,'stage':'discovery','error':str(error)});continue
        if source=='bsee' and 'safety-alerts-program' in url:
            from bs4 import BeautifulSoup
            soup=BeautifulSoup(content,'html.parser')
            links=[(urljoin(url,a['href']),a.get_text(' ',strip=True))
                   for a in soup.select('table tbody a[href], .pager a[href], .js-pager__items a[href], .usa-pagination__list a[href]')]
        for link,title in links:
            if not in_scope(source,link):continue
            if '.pdf' in urlsplit(link).path.lower():pdfs.setdefault(link,title)
            elif Path(urlsplit(link).path).suffix.lower() in ('.xls','.xlsx','.doc','.docx','.zip','.csv','.jpg','.png'):
                warnings.append({'source':source,'url':link,'stage':'unsupported_format',
                                 'error':'Coleta atual é textual PDF/XML; anexo não incluído'})
            elif source=='bsee' and ('safety-alerts-program' in link or depth==0):
                # Paginação tem profundidade zero; detalhe de alerta tem um nível.
                queue.append((link,0 if 'safety-alerts-program' in link else 1))
            elif source in ('anp','hse') and depth<2:queue.append((link,depth+1))
            if limit and len(pdfs)>=limit:return list(pdfs.items())[:limit]
    return list(pdfs.items())


def write_document(root,source,document_id,title,pages,metadata,raw_path):
    dest=root/source/'extracted'/f'{document_id}.jsonl'
    kept,issues=accepted_pages(pages)
    tmp=dest.with_suffix('.tmp');dest.parent.mkdir(parents=True,exist_ok=True)
    base={**SOURCES[source],**metadata,'collection':source,'document_id':document_id,
          'title':title,'raw_path':relative(raw_path,root) if raw_path else None,
          'extraction_version':EXTRACTION_VERSION,'extraction_issues':issues}
    with tmp.open('w',encoding='utf-8') as stream:
        for page in kept:stream.write(json.dumps({**base,**page},ensure_ascii=False)+'\n')
    tmp.replace(dest)
    result={**base,'normalized_path':relative(dest,root),'pages_kept':len(kept),
            'pages_skipped':len(issues),'normalized_sha256':file_hash(dest),'status':'ready'}
    atomic_json(dest.with_suffix('.meta.json'),result)
    return result


def cached_document(root,source,document_id,raw_sha256):
    path=root/source/'extracted'/f'{document_id}.meta.json'
    if not path.exists():return None
    meta=json.loads(path.read_text(encoding='utf-8'));normalized=root/meta['normalized_path']
    if meta.get('extraction_version')!=EXTRACTION_VERSION or meta.get('raw_sha256')!=raw_sha256:return None
    if normalized.is_file() and file_hash(normalized)==meta['normalized_sha256']:return meta
    return None


def collect_pdfs(source,http,root,limit,errors,warnings,quarantined):
    urls=discover(source,http,root,limit,warnings);rows=[]
    atomic_json(root/source/'catalog.json',[{'url':u,'title':t} for u,t in urls])
    for index,(url,title) in enumerate(urls,1):
        listing_url=url;url=canonical_document_url(source,url)
        docid=source+'-'+identity(url);raw=root/source/'raw'/f'{docid}.pdf'
        try:
            download=http.download(url,raw)
            result=cached_document(root,source,docid,download['sha256'])
            if not result:
                language='en' if any(s in title.casefold() for s in ('english','inglês','ingles')) else SOURCES[source]['language']
                result=write_document(root,source,docid,title,list(pdf_pages(raw)),
                    {'url':url,'listing_url':listing_url,'final_url':download['final_url'],'raw_sha256':download['sha256'],
                     'language':language,'acquired_at':now()},raw)
            rows.append(result)
            print(f'[{source}] {index}/{len(urls)}: {result["pages_kept"]} páginas',flush=True)
        except ExtractionRejected as error:
            quarantined.append({'source':source,'url':url,'stage':'text_quality','error':str(error)})
        except Exception as error:
            errors.append({'source':source,'url':url,'stage':'download_or_extraction','error':str(error)})
            print(f'[{source}] falha registrada: {url}',flush=True)
    return rows,{'discovered':len(urls)}


def regis_members(archive):
    # Não extraímos arquivos usando caminhos do ZIP; o alvo é um ID calculado.
    return sorted((i for i in archive.infolist() if not i.is_dir() and
        '/documents/' in '/'+i.filename.replace('\\','/') and i.filename.lower().endswith('.xml')),
        key=lambda i:i.filename)


def collect_regis(http,root,limit,errors,quarantined,local=None,full_archive=False):
    record=json.loads(http.bytes(REGIS_RECORD))
    atomic_json(root/'regis'/'zenodo_record.json',record)
    bundles=[f for f in record['files'] if f['key'].lower().endswith('.zip')]
    if len(bundles)!=1:raise ValueError('Estrutura do registro REGIS mudou: revisar catálogo')
    bundle=bundles[0];url=bundle['links']['self'];raw=root/'regis'/'raw'/'regis.zip'
    remote=None
    if local:
        raw=Path(local)
        algorithm,wanted=bundle['checksum'].split(':',1)
        if file_hash(raw,algorithm)!=wanted:raise ValueError('Pacote REGIS local não confere com o checksum oficial')
    elif limit and not full_archive:
        remote=RemoteZIP(http,url,bundle['size'])
    else:
        print(f'[regis] pacote completo: {bundle["size"]/1e9:.2f} GB; download retomável',flush=True)
        http.download(url,raw,bundle['checksum'],bundle['size'])
    rows=[]
    with zipfile.ZipFile(remote or raw) as archive:
        members=regis_members(archive);total=len(members)
        if not members:raise ValueError('Nenhum documento XML no pacote REGIS')
        for index,member in enumerate(members[:limit] if limit else members,1):
            docid='regis-'+identity(member.filename)
            extracted_raw=root/'regis'/'raw'/'documents'/f'{docid}.xml'
            try:
                if member.file_size>64*1024*1024:raise ValueError('XML excede 64 MiB: revisão manual requerida')
                # CRC verificado por zipfile.read inclusive na amostra remota.
                raw_bytes=archive.read(member)
                digest=hashlib.sha256(raw_bytes).hexdigest()
                result=cached_document(root,'regis',docid,digest)
                if result and result.get('archive_checksum_verified')!=(remote is None):result=None
                if not result:
                    extracted_raw.parent.mkdir(parents=True,exist_ok=True);extracted_raw.write_bytes(raw_bytes)
                    title,original_id,pages=regis_pages(raw_bytes)
                    result=write_document(root,'regis',docid,title or Path(member.filename).stem,pages,
                        {'url':url,'archive_member':member.filename,'original_document_id':original_id,
                         'raw_sha256':digest,'archive_checksum':bundle['checksum'],
                         'archive_checksum_verified':remote is None,'acquired_at':now()},extracted_raw)
                rows.append(result)
                if index<=3 or index%500==0:print(f'[regis] {index}/{limit or total} documentos',flush=True)
            except ExtractionRejected as error:
                quarantined.append({'source':'regis','member':member.filename,'stage':'text_quality','error':str(error)})
            except Exception as error:
                errors.append({'source':'regis','member':member.filename,'stage':'extraction','error':str(error)})
    return rows,{'discovered':total,'archive_bytes':bundle['size'],
        'archive_checksum_verified':remote is None,'sample_transfer_bytes':remote.transferred if remote else None}


def include_petroles(directory,explicit,root):
    if explicit:files=[Path(p).resolve() for p in explicit]
    else:
        if directory is None:
            from pipeline.fase_4.config import default_corpus
            directory=default_corpus()
        files=[Path(directory).resolve()/name for name in PETROLES_FILES]
    if not files or any(not p.is_file() for p in files):
        raise FileNotFoundError('Informe --petroles-dir com os dois TXT reais, ou --petroles-txt com a lista explícita')
    if any('nilc' in p.name.casefold() for p in files):raise ValueError('NILC não integra os corpora factuais desta rodada')
    return {'id':'petroles','format':'petroles_txt','language':'pt','jurisdiction':'not_specified',
        'documents':len(files),'files':[{'path':relative(p,root),'bytes':p.stat().st_size,'sha256':file_hash(p)} for p in files]}


def install(args):
    root=args.output.resolve();root.mkdir(parents=True,exist_ok=True)
    # Valida Petrolês antes de iniciar os downloads, mas não modifica seus arquivos.
    petroles=include_petroles(args.petroles_dir,args.petroles_txt,root)
    http=HTTP(timeout=args.timeout,delay=args.delay,ca_file=args.ca_file)
    errors=[];warnings=[];quarantined=[];collections=[petroles]
    for source in SOURCES:
        print(f'Preparando {source.upper()}...',flush=True)
        try:
            if source=='regis':rows,details=collect_regis(http,root,args.max_documents_per_source,errors,quarantined,
                args.regis_local,args.full_regis_archive)
            else:rows,details=collect_pdfs(source,http,root,args.max_documents_per_source,errors,warnings,quarantined)
        except Exception as error:
            rows=[];details={};errors.append({'source':source,'stage':'collection','error':str(error)})
        target=root/source/'pages.jsonl';target.parent.mkdir(parents=True,exist_ok=True)
        tmp=target.with_suffix('.tmp');seen=set();duplicates=0
        with tmp.open('wb') as stream:
            for row in rows:
                # Remove PDFs/XML idênticos encontrados em mais de uma URL da coleção.
                if row['raw_sha256'] in seen:duplicates+=1;continue
                seen.add(row['raw_sha256'])
                with (root/row['normalized_path']).open('rb') as input_stream:
                    for block in iter(lambda:input_stream.read(1024*1024),b''):stream.write(block)
        tmp.replace(target)
        atomic_json(root/source/'documents.json',rows)
        collections.append({'id':source,'format':'pages_jsonl','path':relative(target,root),
            'sha256':file_hash(target),'documents':len(seen),'duplicate_files':duplicates,
            'pages':sum(r['pages_kept'] for r in rows),'pages_skipped':sum(r['pages_skipped'] for r in rows),
            'quarantined_documents':sum(q['source']==source for q in quarantined),
            'language':SOURCES[source]['language'],'jurisdiction':SOURCES[source]['jurisdiction'],**details})
    ready=all(c['documents']>0 for c in collections) and (not errors or args.allow_document_errors)
    report={'created_at':now(),'ready':ready,'partial':bool(errors),'sample':bool(args.max_documents_per_source),
            'collections':collections,'errors':errors,'discovery_warnings':warnings,'quarantined':quarantined}
    atomic_json(root/'install_report.json',report)
    atomic_json(root/'manifest.json',{'schema':SCHEMA,'extraction_version':EXTRACTION_VERSION,
        'ready':ready,'partial':bool(errors),'download_errors':len(errors),
        'sample':bool(args.max_documents_per_source),'collections':collections})
    print(json.dumps({'ready':ready,'documents':{c['id']:c['documents'] for c in collections},
                      'errors':len(errors),'warnings':len(warnings),'manifest':str(root/'manifest.json')},ensure_ascii=False),flush=True)
    return 0 if ready else 1


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=ROOT/'dataset/domain_corpora')
    petrol=parser.add_mutually_exclusive_group()
    petrol.add_argument('--petroles-dir',type=Path)
    petrol.add_argument('--petroles-txt',type=Path,nargs='+')
    parser.add_argument('--max-documents-per-source',type=int,default=0,
                        help='0=todos os documentos descobertos; positivo=amostra explícita')
    parser.add_argument('--regis-local',type=Path,help='ZIP original com checksum oficial')
    parser.add_argument('--full-regis-archive',action='store_true',help='Baixa o ZIP inteiro mesmo em teste de amostra')
    parser.add_argument('--allow-document-errors',action='store_true',
        help='Permite explicitamente instalação parcial registrada, desde que as cinco coleções tenham documentos')
    parser.add_argument('--timeout',type=float,default=90)
    parser.add_argument('--delay',type=float,default=.25)
    parser.add_argument('--ca-file',help='CA corporativa adicional, sem desabilitar TLS')
    args=parser.parse_args()
    if args.max_documents_per_source<0 or args.timeout<=0 or args.delay<0:parser.error('Limites inválidos')
    try:return install(args)
    except (ValueError,FileNotFoundError) as error:parser.exit(1,str(error)+'\n')


if __name__=='__main__':raise SystemExit(main())
