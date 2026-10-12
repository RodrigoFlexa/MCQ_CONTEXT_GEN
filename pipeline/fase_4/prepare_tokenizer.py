"""Instala o vocabulário público cl100k_base com hash, proxy e CA corporativa."""
import argparse
import hashlib
import os
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
from pipeline.domain_corpora.io_utils import HTTP, file_hash

URL='https://openaipublic.blob.core.windows.net/encodings/cl100k_base.tiktoken'
SHA256='223921b76ee99bde995b7ff738513eef100fb51d18c93597a113bcffe865b2a7'


def ensure_tokenizer(ca_file=None):
    cache=Path(os.environ.get('TIKTOKEN_CACHE_DIR',ROOT/'dataset/tokenizer_cache')).resolve()
    cache.mkdir(parents=True,exist_ok=True)
    target=cache/hashlib.sha1(URL.encode()).hexdigest()
    if not target.is_file() or file_hash(target)!=SHA256:
        if ca_file is None:
            from azure_openai_backend import AzureSettings
            ca_file=AzureSettings.load().ca_bundle
        HTTP(ca_file=ca_file).download(URL,target,'sha256:'+SHA256)
    os.environ['TIKTOKEN_CACHE_DIR']=str(cache)
    import tiktoken
    return tiktoken.get_encoding('cl100k_base')


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--ca-file')
    args=parser.parse_args();tokenizer=ensure_tokenizer(args.ca_file)
    print('Tokenizer OK:',tokenizer.name,'; chamadas Azure=0')


if __name__=='__main__':main()
