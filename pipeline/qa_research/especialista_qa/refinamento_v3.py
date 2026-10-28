"""Conversão com parecer técnico, refatoração limitada e reaproveitamento verificável da v2."""
import copy
import re
import threading
from collections import Counter
from pathlib import Path

from pipeline.inventario.textutil import atomic_json, read_json
from . import core as C
from .extracao import jsonl
from .preparacao_v3 import ENTRADA, ANTERIOR, CONJUNTO, ROTULO, ler_nao_reprovadas
from .revisadas import ROTULOS


def validar_proposta(d, ids):
    fields = {'status', 'motivo', 'qa', 'alteracoes', 'uso_parecer', 'fonte_resposta'}
    if not isinstance(d, dict) or set(d) != fields:
        raise ValueError('Informe status, motivo, qa, alteracoes, uso_parecer e fonte_resposta')
    C.validar_conversao({k: d[k] for k in ('status', 'motivo', 'qa')}, ids)
    if (not isinstance(d['alteracoes'], list) or any(not isinstance(t, str) for t in d['alteracoes'])
            or not isinstance(d['uso_parecer'], str)
            or d['fonte_resposta'] not in ('gabarito_original', 'gabarito_e_parecer', 'correcao_do_especialista')):
        raise ValueError('Metadados de adaptação inválidos')


def original_com_parecer(row):
    return {k: row.get(k) for k in ('agrupamento_original', 'subtopico_original', 'enunciado',
        'gabarito', 'resposta_original', 'justificativa_original', 'notas_documento')} | {
        'alternativas': {k:v['texto'] for k,v in row['alternativas'].items()},
        'parecer_especialista': row['revisao_humana']['parecer_original']}


def apoio_numeros(row):
    adapted = copy.deepcopy(row)
    comment = row['revisao_humana']['parecer_original']
    letters = set(re.findall(r'\b[A-E]\b', comment)) if re.search(r'alternativa', comment, re.I) else set()
    cited = ' '.join(row['alternativas'][k]['texto'] for k in sorted(letters) if k in row['alternativas'])
    adapted['justificativa_original'] += '\n'+comment+'\n'+row.get('notas_documento', '')+'\n'+cited
    return adapted


class RefinarRevisadas(C.ConverterEspecialista):
    def __init__(self, saida, *, entrada=ENTRADA, anterior=ANTERIOR, base=C.BASE, sem_contexto=C.SEM_CONTEXTO,
                 workers=8, max_chamadas=20000, limite=None, max_ciclos=3, clientes=None, progress=print):
        self.saida, self.entrada, self.anterior = Path(saida), Path(entrada), Path(anterior)
        self.base, self.sem_contexto = Path(base), Path(sem_contexto)
        self.todas = ler_nao_reprovadas(self.entrada)
        if not self.todas or len({r['uid'] for r in self.todas}) != len(self.todas):
            raise ValueError('Entrada vazia ou IDs repetidos')
        if not 1 <= max_ciclos <= 5 or workers < 1 or max_chamadas < 1 or (limite is not None and limite < 1):
            raise ValueError('Ciclos entre 1 e 5; workers, orçamento e limite positivos')
        old = read_json(self.saida/'config.json') or {}
        byid = {r['uid']: r for r in self.todas}
        self.rows = [byid[u] for u in old['uids']] if limite is None and old.get('uids') else self.todas[:limite]
        self.workers, self.max_chamadas, self.max_ciclos = workers, max_chamadas, max_ciclos
        self.catalogo, self.ids = C.catalogo(), {r['item'] for r in C.catalogo()}
        self.prompts = {k: (C.HERE/'prompts'/f'{k}_v3.md').read_text(encoding='utf-8') for k in C.MODELOS}
        self.clientes, self.progress = dict(clientes or {}), progress
        self.lock, self.budget, self.interromper = threading.Lock(), None, threading.Event()
        self.rotulos = {**ROTULOS, CONJUNTO: ROTULO}
        self.previous = {r['uid']: r for r in C.ler_linhas(self.anterior/'decisoes.jsonl')}
        self.old_input = {r['uid']:r for r in C.ler_linhas(C.HERE/'entrada/revisadas/curadoria_todas.jsonl')}
        for row in self.rows:
            if row['status_extracao'] == 'ok':
                marked = row['alternativas'].get(row['gabarito'], {}).get('texto')
                if marked != row['resposta_original'] or {e['alternativa'] for e in row['evidencias_gabarito']} != {row['gabarito']}:
                    raise ValueError('Gabarito não corresponde à extração')
            if row['uid'] in self.previous:
                oldrow = self.old_input.get(row['uid'])
                if oldrow is None or any(row.get(k) != oldrow.get(k) for k in ('enunciado', 'alternativas', 'gabarito', 'resposta_original', 'revisao_humana')):
                    raise ValueError('Fonte mudou: não reutilizar a decisão anterior')

    def config(self):
        cfg = {'schema': 'especialista-revisadas-v3', 'entrada_sha256': C.sha(self.todas), 'uids': [r['uid'] for r in self.rows],
            'anterior_path': self.anterior.resolve().relative_to(C.ROOT).as_posix() if self.anterior.resolve().is_relative_to(C.ROOT) else str(self.anterior.resolve()),
            'catalogo': self.catalogo, 'modelos': C.MODELOS, 'max_ciclos': self.max_ciclos,
            'prompts_sha256': {k:C.sha(v) for k,v in self.prompts.items()},
            'codigo_sha256': C.sha(Path(__file__).read_text(encoding='utf-8')),
            'core_sha256': C.sha(Path(C.__file__).read_text(encoding='utf-8')),
            'curadoria_sha256': C.sha((C.HERE/'preparacao_v3.py').read_text(encoding='utf-8')),
            'regras_forma_sha256': C.sha((C.ROOT/'pipeline/qa_research/dificuldade.py').read_text(encoding='utf-8')),
            'normalizacao_sha256': C.sha((C.ROOT/'pipeline/inventario/textutil.py').read_text(encoding='utf-8')),
            'anterior_decisoes_sha256': C.sha(self.previous), 'fonte_original_sha256': C.sha(self.old_input),
            'base_sha256': C.sha(C.ler_linhas(self.base)), 'sem_contexto_sha256': C.sha(C.ler_linhas(self.sem_contexto)),
            'deduplicacao': False, 'parecer_usado_na_conversao': True}
        old = read_json(self.saida/'config.json')
        if old and old != cfg:
            raise ValueError('Protocolo v3 mudou; use outra --saida')
        atomic_json(self.saida/'config.json', cfg)
        atomic_json(self.saida/'limites_execucao.json', {'max_chamadas': self.max_chamadas})
        (self.saida/'tentativas').mkdir(parents=True, exist_ok=True)

    def processar(self, row):
        name = self.nome(row['uid'])
        final = self.saida/'processadas'/name
        if final.exists():
            return True
        if self.interromper.is_set():
            return False
        stage = 'converter'
        try:
            failure = read_json(self.saida/'falhas'/name)
            if failure and failure.get('erro') == 'ContentFiltered':
                return self.registrar_bloqueio(row, name, failure.get('etapa', stage), failure)
            if row['status_extracao'] != 'ok':
                atomic_json(final, {'uid': row['uid'], 'status': 'pendente_extracao', 'motivos': row['problemas_extracao']})
                return True
            prior = self.previous.get(row['uid'], {})
            if prior.get('status') == 'aprovada':
                qa = copy.deepcopy(prior['qa'])
                qa.update(faixa_parecer=row['faixa_parecer'], fluxo_conversao='reaproveitada_v2')
                atomic_json(final, {**prior, 'qa': qa, 'reaproveitada_v2': True, 'ciclos_v3': 0})
                return True
            previous_qa, critique = prior.get('qa'), prior.get('motivos', [])
            original = original_com_parecer(row)
            decision = None
            for cycle in range(1, self.max_ciclos+1):
                directory = self.saida/'tentativas'/name.removesuffix('.json')/f'{cycle:02d}'
                stage = 'converter'
                cpath, apath = directory/'conversao.json', directory/'validacao.json'
                conversion = read_json(cpath)
                if conversion is None:
                    conversion = self.chamar('converter', {'original': original, 'catalogo': self.catalogo,
                        'qa_anterior': previous_qa, 'critica_anterior': critique, 'ciclo': cycle}, row,
                        lambda d: validar_proposta(d, self.ids))
                    atomic_json(cpath, conversion)
                if conversion['status'] == 'descartar':
                    decision = {'uid': row['uid'], 'status': 'descartada_conversao', 'motivos': [conversion['motivo']],
                                'ciclos_v3': cycle, 'adaptacao': conversion}
                    break
                stage = 'validar'
                audit = read_json(apath)
                if audit is None:
                    audit = self.chamar('validar', {'original': original, 'catalogo': self.catalogo, 'qa': conversion['qa'],
                        'alteracoes': conversion['alteracoes'], 'uso_parecer': conversion['uso_parecer'],
                        'fonte_resposta': conversion['fonte_resposta']}, row, lambda d: C.validar_auditoria(d, self.ids))
                    atomic_json(apath, audit)
                qa = {**conversion['qa'], **{k:audit[k] for k in ('item', 'tipo', 'cenario', 'composicao')}}
                issues = C.problemas_codigo(qa, apoio_numeros(row))
                valid = audit['valida'] and not issues
                result = {**qa, 'uid': row['uid']+':qa', 'origem': 'especialista_convertida', 'fonte_uid': row['uid'],
                    'tipo_declarado': conversion['qa']['tipo'], 'conjunto_especialista': CONJUNTO, 'faixa_parecer': row['faixa_parecer'],
                    'politica_curadoria': row['politica_curadoria'], 'revisao_humana': row['revisao_humana'],
                    'agrupamento_id': row['agrupamento_id'], 'agrupamento_original': row['agrupamento_original'],
                    'subtopico_original': row.get('subtopico_original'), 'fluxo_conversao': 'refatorada_v3', 'aprovada': valid}
                decision = {'uid': row['uid'], 'status': 'aprovada' if valid else 'reprovada', 'qa': result,
                    'motivos': audit['motivos']+issues, 'validacao': audit, 'problemas_codigo': issues,
                    'ciclos_v3': cycle, 'adaptacao': {k:v for k,v in conversion.items() if k != 'qa'}}
                if valid:
                    break
                previous_qa, critique = qa, decision['motivos']
            atomic_json(final, decision)
            (self.saida/'falhas'/name).unlink(missing_ok=True)
            return True
        except Exception as exc:
            evidence = {'uid': row['uid'], 'erro': type(exc).__name__, 'mensagem': str(exc)[:1500], 'etapa': stage}
            if type(exc).__name__ == 'ContentFiltered':
                return self.registrar_bloqueio(row, name, stage, evidence)
            atomic_json(self.saida/'falhas'/name, evidence)
            if type(exc).__name__ == 'BudgetExceeded' or getattr(exc, 'kind', None) == 'fatal':
                self.interromper.set()
            return False

    def exportar(self):
        summary = super().exportar()
        ds = C.ler_linhas(self.saida/'decisoes.jsonl')
        summary['reaproveitadas_v2'] = sum(d.get('reaproveitada_v2') is True for d in ds)
        summary['novas_aprovadas_v3'] = summary['aprovadas']-summary['reaproveitadas_v2']
        summary['por_faixa_parecer'] = dict(Counter(q['faixa_parecer'] for q in C.ler_linhas(self.saida/'aprovadas.jsonl')))
        summary['por_conjunto_especialista'] = {CONJUNTO: {'rotulo': ROTULO, 'selecionadas': len(self.rows),
                'aprovadas_qa': summary['aprovadas'], 'status': summary['status']}}
        atomic_json(self.saida/'resultado.json', summary)
        report = self.saida/'RELATORIO.md'
        report.write_text(report.read_text(encoding='utf-8')+f"\nReaproveitadas da v2: {summary['reaproveitadas_v2']}. Novas aprovadas na v3: {summary['novas_aprovadas_v3']}.\n"
            'O parecer técnico foi enviado ao conversor e ao validador. Tentativas e correções ficam em tentativas/.\n', encoding='utf-8')
        return summary


def semear_avaliacao(saida, anterior=ANTERIOR, lote_juiz=8):
    """Copia somente respostas/julgamentos das QAs v2 preservadas integralmente."""
    from pipeline.inventario.locking import output_lock
    from .avaliacao import RESPONDENTES
    from pipeline.qa_research.geracao_tipos.avaliacao import JUIZ
    from pipeline.qa_research.geracao_tipos.core import prompt
    saida, anterior = Path(saida), Path(anterior)
    if not (saida/'conversao_concluida.json').exists():
        raise ValueError('Conclua a conversão antes de reaproveitar a avaliação')
    questions = C.ler_linhas(saida/'aprovadas.jsonl')
    selected = [q for q in questions if q.get('fluxo_conversao') == 'reaproveitada_v2']
    source_protocol = read_json(anterior/'avaliacao/protocolo_experimento.json')
    if selected:
        if (source_protocol['respondentes'] != RESPONDENTES or source_protocol['juiz'] != JUIZ
                or source_protocol['lote_juiz'] != lote_juiz
                or source_protocol['prompt_respondente_sha256'] != C.sha(prompt('respondente'))
                or source_protocol['prompt_juiz_sha256'] != C.sha(prompt('juiz_respostas'))):
            raise ValueError('Protocolo anterior não é compatível com a avaliação atual')
    oldquestions = {q['uid']:q for q in C.ler_linhas(anterior/'aprovadas.jsonl')}
    directory = saida/'avaliacao'
    with output_lock(directory):
        marker = directory/'reaproveitamento_v2.json'
        record = {'aprovadas_sha256': C.sha(questions), 'uids': [q['uid'] for q in selected],
                  'protocolo_origem_sha256': C.sha(source_protocol)}
        previous = read_json(marker)
        if previous:
            if previous != record:
                raise ValueError('A seleção para reaproveitamento da avaliação mudou')
            return len(selected)
        for model in RESPONDENTES:
            grades = {}
            for path in (anterior/'avaliacao/juiz'/model).glob('*.json'):
                for a in read_json(path)['avaliacoes']:
                    if a['uid'] in grades and grades[a['uid']] != a:
                        raise ValueError('Julgamentos anteriores conflitantes')
                    grades[a['uid']] = a
            for q in selected:
                old = oldquestions[q['uid']]
                if any(q[k] != old[k] for k in ('pergunta', 'resposta', 'item', 'tipo', 'composicao')):
                    raise ValueError('QA alterada não pode reutilizar uma avaliação')
                name = q['uid'].replace(':', '_')
                response = read_json(anterior/'avaliacao/respostas'/model/(name+'.json'))
                grade = grades[q['uid']]
                if not response or response['uid'] != q['uid'] or grade['veredito'] not in ('correta', 'parcial', 'incorreta'):
                    raise ValueError('Resposta/julgamento anterior incompleto')
                targets = [(directory/'respostas'/model/(name+'.json'), response),
                           (directory/'juiz'/model/(name+'__v2.json'), {'modelo': model, 'avaliacoes': [grade]})]
                for path, value in targets:
                    if path.exists() and read_json(path) != value:
                        raise ValueError('Não sobrescrever respostas ou julgamentos existentes')
                    atomic_json(path, value)
        atomic_json(marker, record)
    return len(selected)
