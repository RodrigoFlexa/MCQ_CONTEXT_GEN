"""Extrair DOCX localmente, converter/validar no servidor e avaliar as QAs aprovadas."""
import argparse
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from .core import ENTRADA, BASE, SEM_CONTEXTO, ROOT, ConverterEspecialista


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest='cmd', required=True)
    ex = sub.add_parser('extrair', help='extração local determinística, sem API')
    ex.add_argument('--docx', type=Path, required=True)
    ex.add_argument('--saida', type=Path, default=ENTRADA.parent)
    rev = sub.add_parser('extrair-revisadas', help='curadoria humana e extração do DOCX revisado, sem API')
    rev.add_argument('--docx', type=Path, required=True)
    rev.add_argument('--saida', type=Path, default=ENTRADA.parent/'revisadas')
    pv3 = sub.add_parser('preparar-revisadas-v3', help='seleciona todas as MCQs sem reprovação explícita, sem API')
    pv3.add_argument('--saida', type=Path)
    cv = sub.add_parser('converter')
    cv.add_argument('--saida', type=Path)
    cv.add_argument('--entrada', type=Path, default=ENTRADA)
    cv.add_argument('--base', type=Path, default=BASE)
    cv.add_argument('--sem-contexto', type=Path, default=SEM_CONTEXTO)
    cv.add_argument('--workers', type=int, default=8)
    cv.add_argument('--max-chamadas', type=int, default=20000)
    cv.add_argument('--limite', type=int, help='piloto com as primeiras N questões; retomada preserva seleção')
    cv.add_argument('--plano', action='store_true')
    v3 = sub.add_parser('refinar-revisadas', help='usa pareceres e até três ciclos para refatorar QAs, preservando as válidas v2')
    from .preparacao_v3 import ENTRADA as ENTRADA_V3, ANTERIOR
    v3.add_argument('--entrada', type=Path, default=ENTRADA_V3)
    v3.add_argument('--anterior', type=Path, default=ANTERIOR)
    v3.add_argument('--saida', type=Path, required=True)
    v3.add_argument('--base', type=Path, default=BASE)
    v3.add_argument('--sem-contexto', type=Path, default=SEM_CONTEXTO)
    v3.add_argument('--workers', type=int, default=8)
    v3.add_argument('--max-chamadas', type=int, default=20000)
    v3.add_argument('--max-ciclos', type=int, default=3)
    v3.add_argument('--limite', type=int)
    v3.add_argument('--plano', action='store_true')
    av = sub.add_parser('avaliar')
    av.add_argument('--saida', type=Path, required=True)
    av.add_argument('--workers', type=int, default=8)
    av.add_argument('--lote-juiz', type=int, default=8)
    an = sub.add_parser('graficos', help='análise local após coletar a run; requer bibliotecas de análise e modelo E5 local')
    an.add_argument('--saida', type=Path, required=True)
    an.add_argument('--output', type=Path)
    a = ap.parse_args(argv)
    if a.cmd == 'preparar-revisadas-v3':
        from .preparacao_v3 import preparar
        d = preparar(a.saida or ENTRADA_V3.parent)
        print(f"Candidatas: {d['candidatas']}; reprovações/descartes explícitos: {d['reprovadas_explicitas']}")
        return 0
    if a.cmd == 'refinar-revisadas':
        from .refinamento_v3 import RefinarRevisadas
        c = RefinarRevisadas(a.saida, entrada=a.entrada, anterior=a.anterior, base=a.base, sem_contexto=a.sem_contexto,
            workers=a.workers, max_chamadas=a.max_chamadas, max_ciclos=a.max_ciclos, limite=a.limite)
        reused = sum(c.previous.get(r['uid'], {}).get('status') == 'aprovada' for r in c.rows)
        print(f'Saída: {a.saida}\nCandidatas: {len(c.rows)}; QAs v2 preservadas: {reused}; para refatorar: {len(c.rows)-reused}', flush=True)
        if a.plano:
            print('Planejamento sem API ou criação da saída. Pareceres serão usados; máximo de ciclos por MCQ: '+str(a.max_ciclos))
            return 0
        return c.run()
    if a.cmd == 'extrair':
        from .extracao import extrair
        d = extrair(a.docx, a.saida)
        print(f"Extraídas: {d['questoes_extraidas']}; elegíveis: {d['elegiveis']}; pendentes: {d['pendentes']}")
        return 0
    if a.cmd == 'extrair-revisadas':
        from .revisadas import extrair_revisadas
        d = extrair_revisadas(a.docx, a.saida)
        print(f"MCQs: {d['total_mcq']}; selecionadas: {d['selecionadas']}; excluídas: {d['excluidas']}")
        return 0
    if a.cmd == 'avaliar':
        from .avaliacao import avaliar
        from pipeline.inventario.textutil import read_json
        cfg = read_json(a.saida/'config.json') or {}
        if cfg.get('schema') == 'especialista-revisadas-v3':
            from .refinamento_v3 import semear_avaliacao
            previous_path = Path(cfg['anterior_path'])
            semear_avaliacao(a.saida, previous_path if previous_path.is_absolute() else ROOT/previous_path, a.lote_juiz)
        return avaliar(a.saida, workers=a.workers, lote_juiz=a.lote_juiz)
    if a.cmd == 'graficos':
        from .analise import analisar
        analisar(a.saida/'bancos/manifesto.json', a.output or a.saida/'analise_tres_bancos')
        return 0
    saida = a.saida or ROOT/'pipeline/qa_research/relatorios'/f'especialista_qa_{datetime.now(timezone.utc):%Y%m%dT%H%M%SZ}'
    c = ConverterEspecialista(saida, entrada=a.entrada, base=a.base, sem_contexto=a.sem_contexto,
                            workers=a.workers, max_chamadas=a.max_chamadas, limite=a.limite)
    print(f'Saída: {saida}\nQuestões selecionadas: {len(c.rows)} de {len(c.todas)}', flush=True)
    print('Por conjunto: '+str(dict(Counter(r['conjunto_especialista'] for r in c.rows))), flush=True)
    if a.plano:
        print('Somente planejamento: sem API ou criação da saída; o servidor lê a entrada extraída, sem precisar do DOCX.')
        return 0
    return c.run()


if __name__ == '__main__':
    raise SystemExit(main())
