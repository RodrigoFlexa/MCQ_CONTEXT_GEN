"""CLI do baseline sem documentos. --plano não faz chamadas nem cria uma saída."""
import argparse
from datetime import datetime, timezone
from pathlib import Path

from .core import METAS, ROOT, GeracaoSemConteudo


def main(argv=None):
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--saida',type=Path)
    ap.add_argument('--metas',type=Path,default=METAS)
    ap.add_argument('--itens',nargs='+',help='IDs, por exemplo 01_01 02_02; padrão: todos ou os da retomada')
    ap.add_argument('--lote',type=int,default=5)
    ap.add_argument('--memoria',type=int,default=20)
    ap.add_argument('--refinos',type=int,default=2,choices=(0,1,2))
    ap.add_argument('--workers',type=int,default=5)
    ap.add_argument('--max-lotes',type=int,default=100,help='limite cumulativo de lotes por tópico')
    ap.add_argument('--max-sem-progresso',type=int,default=10)
    ap.add_argument('--max-chamadas',type=int,default=30000,help='tentativas de API cumulativas; inclui reparos e refinos')
    ap.add_argument('--plano',action='store_true')
    ap.add_argument('--relatorio',action='store_true')
    a=ap.parse_args(argv)
    saida=a.saida or ROOT/'pipeline/qa_research/relatorios'/f'sem_conteudo_{datetime.now(timezone.utc):%Y%m%dT%H%M%SZ}'
    g=GeracaoSemConteudo(saida,metas=a.metas,itens=a.itens,lote=a.lote,memoria=a.memoria,
        refinos=a.refinos,workers=a.workers,max_lotes=a.max_lotes,
        max_sem_progresso=a.max_sem_progresso,max_chamadas=a.max_chamadas)
    print(f'Saída: {saida}',flush=True)
    print(f'Metas: {sum(i["meta"] for i in g.itens)} questões em {len(g.itens)} tópicos',flush=True)
    if a.plano:
        for item in g.itens:
            print(f'{item["id"]}: {item["meta"]} | {item["subtopico"]}')
        print('Plano somente: sem chamadas, documentos, exemplos ou leitura das questões de referência.')
        return 0
    if a.relatorio:
        from pipeline.inventario.locking import output_lock
        with output_lock(saida):
            g.relatorio()
        return 0
    return g.run()


if __name__=='__main__':
    raise SystemExit(main())
