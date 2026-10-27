"""Conversão e classificação por gpt-5-4, validação independente e junção rastreável."""
import csv
import hashlib
import json
import re
import threading
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

from pipeline.inventario.locking import output_lock
from pipeline.inventario.textutil import atomic_json, read_json, squash
from pipeline.qa_research.dificuldade import problemas_forma
from pipeline.qa_research.tipos import TIPOS
from .extracao import jsonl
from .revisadas import ler_entradas, ROTULOS

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
ENTRADA_AUTORAL = HERE/'entrada/questoes_mcq.jsonl'
ENTRADA = HERE/'entrada/fontes.json'
BASE = ROOT/'pipeline/qa_research/relatorios/geracao_final_20261024T204734Z/aprovadas.jsonl'
SEM_CONTEXTO = ROOT/'pipeline/qa_research/relatorios/sem_conteudo_bruto_v1/questoes.jsonl'
MODELOS = {'converter': 'gpt-5-4-petrobras:high', 'validar': 'gpt-5-4-petrobras:high'}
CAMPOS = {'item', 'tipo', 'cenario', 'composicao', 'pergunta', 'resposta'}
CRITERIOS = {'fiel_gabarito', 'autonoma', 'sem_resposta_no_enunciado', 'univoca',
             'correcao_tecnica', 'escopo_correto', 'pergunta_aberta', 'sem_informacao_inventada'}


def agora():
    return datetime.now(timezone.utc).isoformat()


def sha(data):
    return hashlib.sha256(json.dumps(data, ensure_ascii=False, sort_keys=True).encode()).hexdigest()


def ler_linhas(path):
    return [json.loads(line) for line in Path(path).read_text(encoding='utf-8-sig').splitlines() if line.strip()]


def catalogo():
    from pipeline.fase_3.topicos import TOPICOS
    return [{'item': f'{i:02d}_{j:02d}', 'topico': area, 'subtopico': sub}
            for i, (area, subs) in enumerate(TOPICOS.items(), 1) for j, sub in enumerate(subs, 1)]


def validar_rotulos(q, ids):
    if q.get('item') not in ids or q.get('tipo') not in TIPOS or type(q.get('cenario')) is not bool or q.get('composicao') not in ('simples', 'composta'):
        raise ValueError('Item, tipo, cenário ou composição inválidos')


def validar_conversao(d, ids):
    if not isinstance(d, dict) or set(d) != {'status', 'motivo', 'qa'} or d['status'] not in ('ok', 'descartar') or not isinstance(d['motivo'], str):
        raise ValueError('Use status, motivo e qa')
    if d['status'] == 'descartar':
        if d['qa'] is not None or not d['motivo'].strip():
            raise ValueError('Descarte exige qa null e motivo preenchido')
        return
    q = d['qa']
    if not isinstance(q, dict) or set(q) != CAMPOS:
        raise ValueError('QA deve ter item, tipo, cenario, composicao, pergunta e resposta')
    validar_rotulos(q, ids)
    if any(not isinstance(q[k], str) or not q[k].strip() for k in ('pergunta', 'resposta')):
        raise ValueError('Pergunta e resposta devem ser textos preenchidos')


def validar_auditoria(d, ids):
    fields = {'valida', 'item', 'tipo', 'cenario', 'composicao', 'criterios', 'motivos', 'justificativa'}
    if not isinstance(d, dict) or set(d) != fields or type(d['valida']) is not bool:
        raise ValueError('Campos de validação inválidos')
    validar_rotulos(d, ids)
    c = d['criterios']
    if not isinstance(c, dict) or set(c) != CRITERIOS or any(type(v) is not bool for v in c.values()):
        raise ValueError('Informe os oito critérios booleanos')
    if not isinstance(d['motivos'], list) or any(not isinstance(m, str) or not m.strip() for m in d['motivos']):
        raise ValueError('Motivos deve ser uma lista de textos')
    if not isinstance(d['justificativa'], str) or not d['justificativa'].strip():
        raise ValueError('Explique a validação')
    if d['valida'] != all(c.values()) or d['valida'] != (not d['motivos']):
        raise ValueError('Aprovação exige todos os critérios true e motivos vazio')


def problemas_codigo(q, original):
    p, r = q['pergunta'], q['resposta']
    issues = list(problemas_forma(p, r, teto_resposta=40))
    if not p.rstrip().endswith('?'):
        issues.append('pergunta_sem_interrogacao')
    if len(p.split()) > 90:
        issues.append('pergunta_longa')
    answer, question = squash(r), squash(p)
    if answer and f' {answer} ' in f' {question} ':
        issues.append('resposta_literal_no_enunciado')
    if re.search(r'\b(?:qual|quais)\b.{0,30}\balternativas?\b|\b(?:letra|opção|opcao)\s+[A-E]\b', p+' '+r, re.I) or len(re.findall(r'\b[A-E]\)', p+r)) >= 2 or re.fullmatch(r'(?:alternativa\s+)?[A-E][).]?', r.strip(), re.I):
        issues.append('referencia_a_alternativas')
    if re.search(r'\b(?:segundo o (?:texto|documento)|no (?:texto|documento)|gabarito)\b', p, re.I):
        issues.append('referencia_ao_documento')
    if q['tipo'] in ('diagnostico', 'decisao') and not q['cenario']:
        issues.append('tipo_exige_cenario')
    support = original['enunciado']+' '+original['resposta_original']+' '+original['justificativa_original']
    numbers = lambda t: {s.replace(',', '.') for s in re.findall(r'\d+(?:[.,]\d+)?', t)}
    if numbers(p+' '+r)-numbers(support):
        issues.append('numero_novo_sem_sustentacao')
    return issues


class ConverterEspecialista:
    def __init__(self, saida, *, entrada=ENTRADA, base=BASE, sem_contexto=SEM_CONTEXTO,
                 workers=8, max_chamadas=20000, limite=None, clientes=None, progress=print):
        self.saida, self.entrada = Path(saida), Path(entrada)
        self.base, self.sem_contexto = Path(base), Path(sem_contexto)
        self.todas = ler_entradas(self.entrada)
        if not self.todas or len({r['uid'] for r in self.todas}) != len(self.todas):
            raise ValueError('Entrada vazia ou com IDs repetidos')
        for r in self.todas:
            if r['status_extracao'] == 'ok':
                keys = {e['alternativa'] for e in r['evidencias_gabarito']}
                marked = r['alternativas'].get(r['gabarito'], {}).get('texto')
                if keys != {r['gabarito']} or not marked or marked != r['resposta_original']:
                    raise ValueError('Entrada inconsistente: gabarito não corresponde à marcação explícita')
        old = read_json(self.saida/'config.json') or {}
        if limite is not None and (type(limite) is not int or limite < 1):
            raise ValueError('Limite deve ser positivo')
        if limite is None and old.get('uids'):
            byid = {r['uid']: r for r in self.todas}
            self.rows = [byid[i] for i in old['uids']]
        else:
            self.rows = self.todas[:limite]
        if workers < 1 or max_chamadas < 1:
            raise ValueError('Workers e orçamento devem ser positivos')
        self.workers, self.max_chamadas = workers, max_chamadas
        self.catalogo = catalogo()
        self.ids = {r['item'] for r in self.catalogo}
        self.prompts = {k: (HERE/'prompts'/f'{k}.md').read_text(encoding='utf-8') for k in MODELOS}
        self.clientes, self.progress = dict(clientes or {}), progress
        self.lock, self.budget = threading.Lock(), None
        self.interromper = threading.Event()

    def config(self):
        cfg = {'schema': 'especialista-qa-v2', 'entrada_sha256': sha(self.todas),
               'uids': [r['uid'] for r in self.rows], 'catalogo': self.catalogo, 'modelos': MODELOS,
               'prompts_sha256': {k: sha(v) for k, v in self.prompts.items()},
               'codigo_sha256': sha(Path(__file__).read_text(encoding='utf-8')),
               'curadoria_sha256': sha((HERE/'revisadas.py').read_text(encoding='utf-8')),
               'regras_forma_sha256': sha((ROOT/'pipeline/qa_research/dificuldade.py').read_text(encoding='utf-8')),
               'normalizacao_sha256': sha((ROOT/'pipeline/inventario/textutil.py').read_text(encoding='utf-8')),
               'base_sha256': sha(ler_linhas(self.base)), 'sem_contexto_sha256': sha(ler_linhas(self.sem_contexto)),
               'deduplicacao': False, 'agrupamento_original_preservado': True}
        old = read_json(self.saida/'config.json')
        if old and {k: v for k, v in old.items() if k != 'criado_em'} != cfg:
            raise ValueError('Configuração, entrada ou bancos mudaram; use outra --saida')
        if not old:
            atomic_json(self.saida/'config.json', {**cfg, 'criado_em': agora()})
        atomic_json(self.saida/'limites_execucao.json', {'max_chamadas': self.max_chamadas})

    def cliente(self, role):
        with self.lock:
            if role not in self.clientes:
                from pipeline.inventario.llm import LLMClient, load_dotenv
                from pipeline.qa_research.runtime import PersistentBudget
                load_dotenv(ROOT)
                if self.budget is None:
                    self.budget = PersistentBudget(self.saida/'orcamento.json', self.max_chamadas)
                model, effort = MODELOS[role].rsplit(':', 1)
                self.clientes[role] = LLMClient(model, effort, self.saida/'.local'/f'{role}.sqlite3',
                    self.saida/'chamadas'/f'{role}.jsonl', provider='azure', budget=self.budget,
                    max_attempts=3, max_calls=self.max_chamadas, max_tokens_cap=16000, timeout=600,
                    response_dir=self.saida/'.local/respostas'/role)
            return self.clientes[role]

    def chamar(self, role, payload, row, validate):
        return self.cliente(role).json(self.prompts[role], json.dumps(payload, ensure_ascii=False, sort_keys=True),
            tag='especialista_'+role, max_tokens=8000, item=row['agrupamento_id'], validate=validate)

    @staticmethod
    def nome(uid):
        if not re.fullmatch(r'[a-zA-Z0-9:_-]+', uid):
            raise ValueError('UID contém caracteres inválidos')
        return uid.replace(':', '_')+'.json'

    def processar(self, row):
        name = self.nome(row['uid'])
        final = self.saida/'processadas'/name
        if final.exists():
            return True
        if self.interromper.is_set():
            return False
        try:
            if row['status_extracao'] != 'ok':
                atomic_json(final, {'uid': row['uid'], 'status': 'pendente_extracao',
                                   'motivos': row['problemas_extracao']})
                return True
            original = {'agrupamento_original': row['agrupamento_original'], 'enunciado': row['enunciado'],
                        'subtopico_original': row.get('subtopico_original'),
                        'alternativas': {k: v['texto'] for k, v in row['alternativas'].items()},
                        'gabarito': row['gabarito'], 'resposta_original': row['resposta_original'],
                        'justificativa_original': row['justificativa_original']}
            payload = {'original': original, 'catalogo': self.catalogo}
            cpath = self.saida/'conversoes'/name
            conversion = read_json(cpath)
            if conversion is None:
                conversion = self.chamar('converter', payload, row, lambda d: validar_conversao(d, self.ids))
                atomic_json(cpath, conversion)
            if conversion['status'] == 'descartar':
                decision = {'uid': row['uid'], 'status': 'descartada_conversao', 'motivos': [conversion['motivo']]}
            else:
                qa = conversion['qa']
                apath = self.saida/'validacoes'/name
                audit = read_json(apath)
                if audit is None:
                    audit = self.chamar('validar', {**payload, 'qa': qa}, row, lambda d: validar_auditoria(d, self.ids))
                    atomic_json(apath, audit)
                classified = {**qa, **{k: audit[k] for k in ('item', 'tipo', 'cenario', 'composicao')}}
                issues = problemas_codigo(classified, row)
                valid = audit['valida'] and not issues
                decision = {'uid': row['uid'], 'status': 'aprovada' if valid else 'reprovada',
                            'motivos': audit['motivos']+issues, 'validacao': audit, 'problemas_codigo': issues,
                            'qa': {**classified, 'uid': row['uid']+':qa', 'origem': 'especialista_convertida',
                                   'tipo_declarado': qa['tipo'], 'fonte_uid': row['uid'],
                                   'conjunto_especialista': row['conjunto_especialista'],
                                   'revisao_humana': row.get('revisao_humana'),
                                   'subtopico_original': row.get('subtopico_original'),
                                   'agrupamento_id': row['agrupamento_id'], 'agrupamento_original': row['agrupamento_original'],
                                   'aprovada': valid}}
            atomic_json(final, decision)
            (self.saida/'falhas'/name).unlink(missing_ok=True)
            return True
        except Exception as exc:
            atomic_json(self.saida/'falhas'/name, {'uid': row['uid'], 'erro': type(exc).__name__, 'mensagem': str(exc)[:1500]})
            if type(exc).__name__ == 'BudgetExceeded' or getattr(exc, 'kind', None) == 'fatal':
                with self.lock:
                    if not self.interromper.is_set():
                        self.interromper.set()
                        atomic_json(self.saida/'interrupcao.json', {'erro': type(exc).__name__, 'mensagem': str(exc)[:1500]})
            return False

    def exportar(self):
        approved, decisions, review = [], [], []
        for row in self.rows:
            name = self.nome(row['uid'])
            d = read_json(self.saida/'processadas'/name) or {'uid': row['uid'], 'status': 'falha',
                'motivos': [(read_json(self.saida/'falhas'/name) or {}).get('mensagem', 'Não processada')]}
            decisions.append({**d, 'fonte': row['fonte'], 'numero_original': row['numero_original'],
                              'conjunto_especialista': row['conjunto_especialista'],
                              'subtopico_original': row.get('subtopico_original'),
                              'revisao_humana': row.get('revisao_humana')})
            if d['status'] == 'aprovada':
                approved.append(d['qa'])
            q = d.get('qa') or {}
            review.append({'uid': row['uid'], 'agrupamento_original': row['agrupamento_original'],
                'subtopico_original': row.get('subtopico_original'), 'conjunto_especialista': row['conjunto_especialista'],
                'parecer_humano': (row.get('revisao_humana') or {}).get('parecer_original'),
                'numero_original': row['numero_original'], 'status': d['status'], 'enunciado_original': row['enunciado'],
                'resposta_original': row['resposta_original'], 'pergunta_qa': q.get('pergunta'),
                'resposta_qa': q.get('resposta'), 'item': q.get('item'), 'tipo': q.get('tipo'),
                'motivos': '; '.join(d.get('motivos', []))})
        jsonl(self.saida/'aprovadas.jsonl', approved)
        jsonl(self.saida/'decisoes.jsonl', decisions)
        jsonl(self.saida/'reprovadas.jsonl', [d for d in decisions if d['status'] != 'aprovada'])
        with (self.saida/'revisao_conversoes.csv').open('w', encoding='utf-8-sig', newline='') as f:
            w = csv.DictWriter(f, fieldnames=list(review[0]))
            w.writeheader()
            w.writerows(review)
        summary = {'selecionadas': len(self.rows), 'entrada_total': len(self.todas), 'aprovadas': len(approved),
                   'status': dict(Counter(d['status'] for d in decisions)),
                   'por_tipo': dict(Counter(q['tipo'] for q in approved)),
                   'por_subtopico': dict(Counter(q['item'] for q in approved))}
        summary['por_conjunto_especialista'] = {key: {
            'rotulo': ROTULOS[key], 'selecionadas': sum(r['conjunto_especialista'] == key for r in self.rows),
            'aprovadas_qa': sum(q['conjunto_especialista'] == key for q in approved),
            'status': dict(Counter(d['status'] for d in decisions if d['conjunto_especialista'] == key))}
            for key in dict.fromkeys(r['conjunto_especialista'] for r in self.rows)}
        atomic_json(self.saida/'resultado.json', summary)
        lines = ['# Conversão das questões do especialista', '',
            f"Questões selecionadas: {len(self.rows)} de {len(self.todas)}. Aprovadas automaticamente: **{len(approved)}**.", '',
            'O agrupamento original é preservado; o subtópico no catálogo de 40 itens é atribuído separadamente. '
            'A validação do QA usa o original e o conhecimento do modelo, sem comprovação documental. '
            'A aprovação humana da MCQ revisada é preservada separadamente e não equivale à aprovação do QA convertido. '
            'Pergunta e resposta aprovadas não são reescritas pelo auditor. Não há deduplicação de questões válidas.', '',
            '| Situação | Quantidade |', '|---|---:|']
        lines += [f'| {k} | {v} |' for k, v in summary['status'].items()]
        lines += ['', '| Conjunto | MCQs selecionadas | QAs aprovadas |', '|---|---:|---:|']
        lines += [f"| {d['rotulo']} | {d['selecionadas']} | {d['aprovadas_qa']} |"
                  for d in summary['por_conjunto_especialista'].values()]
        lines += ['', 'Consulte revisao_conversoes.csv e decisoes.jsonl para a rastreabilidade e os motivos de reprovação.', '']
        (self.saida/'RELATORIO.md').write_text('\n'.join(lines), encoding='utf-8')
        return summary

    def montar_bancos(self):
        base, raw = ler_linhas(self.base), ler_linhas(self.sem_contexto)
        cfg = read_json(self.saida/'config.json')
        if sha(base) != cfg['base_sha256'] or sha(raw) != cfg['sem_contexto_sha256']:
            raise ValueError('Um banco de referência mudou durante a execução; não misturar versões')
        expert = ler_linhas(self.saida/'aprovadas.jsonl')
        if any(q.get('aprovada') is not True for q in base+expert):
            raise ValueError('A junção aceita somente aprovadas do banco com contexto e do especialista')
        merged = base+expert
        if len({q['uid'] for q in merged}) != len(merged):
            raise ValueError('Colisão de IDs na junção')
        target = self.saida/'bancos/com_contexto_com_especialista.jsonl'
        jsonl(target, merged)
        specs = [('sem_contexto', 'Sem contexto', self.sem_contexto, raw),
                 ('com_contexto_sem_especialista', 'Com contexto sem questões do especialista', self.base, base),
                 ('com_contexto_com_especialista', 'Com contexto com questões do especialista', target, merged)]
        bancos = []
        for key, label, path, rows in specs:
            path = path.resolve()
            bancos.append({'id': key, 'rotulo': label,
                'path': path.relative_to(ROOT).as_posix() if path.is_relative_to(ROOT) else str(path),
                'questoes': len(rows), 'conteudo_sha256': sha(rows)})
        manifest = {'schema': 'comparacao-tres-bancos-v1', 'bancos': bancos, 'especialista_aprovadas': len(expert),
                    'especialista_por_conjunto': dict(Counter(q['conjunto_especialista'] for q in expert)),
                    'deduplicacao': False, 'observacao': 'Bancos têm tamanhos diferentes; comparar TTR com cautela e usar MATTR. '
                    'Origem, filtros e processo também diferem. Coincidências textuais não são removidas.'}
        atomic_json(self.saida/'bancos/manifesto.json', manifest)
        return manifest

    def run(self):
        with output_lock(self.saida):
            self.config()
            self.interromper.clear()
            (self.saida/'interrupcao.json').unlink(missing_ok=True)
            for directory in ('processadas', 'conversoes', 'validacoes', 'falhas', 'chamadas'):
                (self.saida/directory).mkdir(parents=True, exist_ok=True)
            marker = self.saida/'conversao_concluida.json'
            marker.unlink(missing_ok=True)
            failed = 0
            try:
                with ThreadPoolExecutor(max_workers=self.workers) as pool:
                    for i, ok in enumerate(pool.map(self.processar, self.rows), 1):
                        failed += not ok
                        if i % 25 == 0 or i == len(self.rows):
                            self.progress(f'Conversão/validação: {i}/{len(self.rows)} | falhas {failed}', flush=True)
                summary = self.exportar()
                if not failed:
                    manifest = self.montar_bancos()
                    atomic_json(marker, {'em': agora(), 'aprovadas': summary['aprovadas'],
                                         'bancos': {r['id']: r['questoes'] for r in manifest['bancos']}})
                return 2 if failed else 0
            finally:
                for c in self.clientes.values():
                    if hasattr(c, 'close'):
                        c.close()
