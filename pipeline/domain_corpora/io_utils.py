"""Download verificável e acesso parcial a ZIP para testes pequenos."""
import hashlib
import io
import json
import os
import ssl
import time
import urllib.error
import urllib.request
from pathlib import Path


def atomic_json(path, value):
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix+'.tmp')
    tmp.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    tmp.replace(path)


def file_hash(path, algorithm='sha256'):
    digest = hashlib.new(algorithm)
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1024*1024), b''): digest.update(block)
    return digest.hexdigest()


class HTTP:
    def __init__(self, timeout=90, retries=3, delay=.25, ca_file=None):
        self.timeout, self.retries, self.delay = timeout, retries, delay
        self.context = ssl.create_default_context()
        extra_ca=ca_file or os.getenv('SSL_CERT_FILE')
        if extra_ca:self.context.load_verify_locations(cafile=extra_ca)
        self.last_request = 0

    def open(self, url, headers=None):
        # Mantém verificação TLS. Nunca imprime tokens, ambiente ou cabeçalhos.
        for attempt in range(self.retries):
            time.sleep(max(0, self.delay-(time.monotonic()-self.last_request)))
            self.last_request = time.monotonic()
            try:
                return urllib.request.urlopen(urllib.request.Request(url, headers={
                    'User-Agent':'PetroQuestCorpus/1.0 (public research documents)',
                    **(headers or {})}), timeout=self.timeout, context=self.context)
            except urllib.error.HTTPError as error:
                if error.code not in (408,429,500,502,503,504) or attempt+1==self.retries: raise
            except (urllib.error.URLError, TimeoutError, OSError):
                if attempt+1==self.retries: raise
            time.sleep(min(2**attempt, 8))

    def bytes(self, url, max_bytes=20*1024*1024):
        with self.open(url) as response:
            content = response.read(max_bytes+1)
        if len(content)>max_bytes: raise ValueError('Resposta excedeu o limite de leitura: '+url)
        return content

    def download(self, url, target, checksum=None, expected_size=None):
        target=Path(target); target.parent.mkdir(parents=True,exist_ok=True)
        meta=target.with_suffix(target.suffix+'.json')
        if target.exists() and meta.exists():
            try:saved=json.loads(meta.read_text(encoding='utf-8'))
            except json.JSONDecodeError:saved={}
            if saved.get('url')==url and saved.get('sha256')==file_hash(target):
                if expected_size is not None and target.stat().st_size!=expected_size:
                    raise ValueError('Tamanho do arquivo em cache não confere')
                if checksum:
                    algorithm,wanted=checksum.split(':',1)
                    if file_hash(target,algorithm)!=wanted: raise ValueError('Checksum do cache não confere')
                return saved
        partial=target.with_suffix(target.suffix+'.part')
        offset=partial.stat().st_size if partial.exists() else 0
        if expected_size is not None and offset>expected_size:
            partial.unlink(); offset=0
        if expected_size is not None and offset==expected_size and checksum:
            algorithm,wanted=checksum.split(':',1)
            if file_hash(partial,algorithm)==wanted:
                partial.replace(target)
                saved={'url':url,'final_url':url,'bytes':expected_size,'sha256':file_hash(target),'upstream_checksum':checksum}
                atomic_json(meta,saved);return saved
            partial.unlink();offset=0
        headers={'Range':f'bytes={offset}-'} if offset else {}
        with self.open(url,headers) as response:
            append=offset>0 and response.status==206
            content_range=response.headers.get('Content-Range','')
            if append and not content_range.startswith(f'bytes {offset}-'):
                raise ValueError('Servidor respondeu um intervalo inesperado')
            total=expected_size
            if total is None:
                length=response.headers.get('Content-Length')
                if length: total=int(length)+(offset if append else 0)
            with partial.open('ab' if append else 'wb') as stream:
                for block in iter(lambda:response.read(1024*1024),b''):stream.write(block)
            if total is not None and partial.stat().st_size!=total:
                raise ValueError('Download incompleto; arquivo .part preservado para retomada')
            final_url=response.url
        if checksum:
            algorithm,wanted=checksum.split(':',1)
            if file_hash(partial,algorithm)!=wanted:
                partial.unlink(); raise ValueError('Checksum oficial não confere: '+url)
        partial.replace(target)
        saved={'url':url,'final_url':final_url,'bytes':target.stat().st_size,
               'sha256':file_hash(target),'upstream_checksum':checksum}
        atomic_json(meta,saved)
        return saved


class RemoteZIP(io.RawIOBase):
    """ZIP seekable via HTTP Range; só usado na amostra explícita, nunca no full.

    zipfile verifica CRC de cada membro. Amostra não valida MD5 do ZIP inteiro.
    """
    def __init__(self, http, url, size):
        self.http,self.url,self.size,self.position=http,url,size,0
        self.transferred=0
    def seekable(self): return True
    def readable(self): return True
    def tell(self): return self.position
    def seek(self, offset, whence=0):
        pos=offset if whence==0 else self.position+offset if whence==1 else self.size+offset
        if pos<0: raise ValueError('Seek negativo')
        self.position=pos; return pos
    def read(self, size=-1):
        size=min(self.size-self.position, size if size>=0 else self.size)
        if size<=0:return b''
        start=self.position;end=start+size-1
        with self.http.open(self.url,{'Range':f'bytes={start}-{end}'}) as response:
            if response.status!=206 or response.headers.get('Content-Range')!=f'bytes {start}-{end}/{self.size}':
                raise ValueError('Amostra REGIS requer HTTP Range. Use --full-regis-archive ou --regis-local.')
            result=response.read(size+1)
        if len(result)!=size:raise ValueError('Intervalo REGIS incompleto')
        self.position+=size; self.transferred+=size
        return result
