"""Extrair DOCX localmente, converter/validar no servidor e avaliar as QAs aprovadas."""
import argparse
from datetime import datetime, timezone
from pathlib import Path

from .core import ENTRADA, BASE, SEM_CONTEXTO, ROOT, ConverterEspecialista


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest='cmd', required=True)
    ex = sub.add_parser('extrair', help='extração local determinística, sem API')
    ex.add_argument('--docx', type=Path, required=True)
    ex.add_argument('--saida', type=Path, default=ENTRADA.parent)
    cv = sub.add_parser('converter')
    cv.add_argument('--saida', type=Path)
    cv.add_argument('--entrada', type=Path, default=ENTRADA)
    cv.add_argument('--base', type=Path, default=BASE)
    cv.add_argument('--sem-contexto', type=Path, default=SEM_CONTEXTO)
    cv.add_argument('--workers', type=int, default=8)
    cv.add_argument('--max-chamadas', type=int, default=20000)
    cv.add_argument('--limite', type=int, help='piloto com as primeiras N questões; retomada preserva seleção')
    cv.add_argument('--plano', action='store_true')
    av = sub.add_parser('avaliar')
    av.add_argument('--saida', type=Path, required=True)
    av.add_argument('--workers', type=int, default=8)
    av.add_argument('--lote-juiz', type=int, default=8)
    an = sub.add_parser('graficos', help='análise local após coletar a run; requer bibliotecas de análise e modelo E5 local')
    an.add_argument('--saida', type=Path, required=True)
    an.add_argument('--output', type=Path)
    a = ap.parse_args(argv)
    if a.cmd == 'extrair':
        from .extracao import extrair
        d = extrair(a.docx, a.saida)
        print(f"Extraídas: {d['questoes_extraidas']}; elegíveis: {d['elegiveis']}; pendentes: {d['pendentes']}")
        return 0
    if a.cmd == 'avaliar':
        from .avaliacao import avaliar
        return avaliar(a.saida, workers=a.workers, lote_juiz=a.lote_juiz)
    if a.cmd == 'graficos':
        from .analise import analisar
        analisar(a.saida/'bancos/manifesto.json', a.output or a.saida/'analise_tres_bancos')
        return 0
    saida = a.saida or ROOT/'pipeline/qa_research/relatorios'/f'especialista_qa_{datetime.now(timezone.utc):%Y%m%dT%H%M%SZ}'
    c = ConverterEspecialista(saida, entrada=a.entrada, base=a.base, sem_contexto=a.sem_contexto,
                            workers=a.workers, max_chamadas=a.max_chamadas, limite=a.limite)
    print(f'Saída: {saida}\nQuestões selecionadas: {len(c.rows)} de {len(c.todas)}', flush=True)
    if a.plano:
        print('Somente planejamento: sem API ou criação da saída; o servidor lê a entrada extraída, sem precisar do DOCX.')
        return 0
    return c.run()


if __name__ == '__main__':
    raise SystemExit(main())
