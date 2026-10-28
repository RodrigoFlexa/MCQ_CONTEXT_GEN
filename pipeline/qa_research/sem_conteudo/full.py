"""Completa o baseline bruto até o tamanho do Full e avalia sem filtrar questões."""
import argparse
import copy
import json
from collections import Counter
from pathlib import Path

from pipeline.inventario.locking import output_lock
from pipeline.inventario.textutil import atomic_json, read_json
from . import core as C

METAS_FULL = C.HERE/'metas_full_4111.json'
SEMENTE = C.ROOT/'pipeline/qa_research/relatorios/sem_conteudo_bruto_v1/questoes.jsonl'
SAIDA = C.ROOT/'pipeline/qa_research/relatorios/sem_conteudo_full_4111'


def linhas(path):
    return [json.loads(s) for s in Path(path).read_text(encoding='utf-8-sig').splitlines() if s.strip()]


def preparar_metas(saida=METAS_FULL):
    """Só a preparação offline lê as QAs Full; exporta apenas contagens e escopos."""
    root = C.ROOT/'pipeline/qa_research/relatorios'
    files = [root/'geracao_final_20261024T204734Z/aprovadas.jsonl',
             root/'especialista_revisadas_v3/aprovadas.jsonl', root/'especialista_qa_v2/aprovadas.jsonl']
    components = [linhas(p) for p in files]
    components[2] = [q for q in components[2] if q['conjunto_especialista'] == 'autoral_especialista']
    full = sum(components, [])
    seed = linhas(SEMENTE)
    if [len(qs) for qs in components] != [2818, 670, 623] or len(seed) != 2818:
        raise ValueError('Contagens das fontes mudaram; revise a definição de Full')
    if len({q['uid'] for q in full}) != 4111 or any(q.get('aprovada') is not True for q in full):
        raise ValueError('Full deve conter 4.111 IDs distintos e questões aprovadas')
    targets, existing = Counter(q['item'] for q in full), Counter(q['item'] for q in seed)
    data = copy.deepcopy(C.carregar_metas())
    if set(targets) != {i['id'] for i in data['itens']} or set(existing) != set(targets):
        raise ValueError('Tópicos incompatíveis')
    for i in data['itens']:
        if existing[i['id']] > targets[i['id']]:
            raise ValueError('A semente já ultrapassa a meta do tópico')
        i['meta'] = targets[i['id']]
    data.update(total=4111, run_referencia='Default+A+E',
                full_sha256=C.sha(full), semente_sha256=C.sha(seed),
                semente_total=len(seed), semente_por_item=dict(existing),
                componentes={'Default': 2818, 'A': 670, 'E': 623})
    data.pop('aprovadas_referencia_sha256', None)
    atomic_json(saida, data)
    return data


class GeracaoFull(C.GeracaoSemConteudo):
    def __init__(self, saida, *, metas=METAS_FULL, semente=SEMENTE, **kw):
        super().__init__(saida, metas=metas, **kw)
        self.semente_path = Path(semente)
        if self.semente_path.parent.resolve() == self.saida.resolve() or self.semente_path.parent.resolve() in self.saida.resolve().parents:
            raise ValueError('Use uma saída nova fora da run original')
        self.semente = linhas(semente)
        if C.sha(self.semente) != self.manifesto.get('semente_sha256') or len(self.semente) != self.manifesto.get('semente_total'):
            raise ValueError('Semente mudou em relação às metas congeladas')
        self.por_item = {i['id']: [q for q in self.semente if q['item'] == i['id']] for i in self.itens}
        if set(q['item'] for q in self.semente) != set(self.por_item) or len({q['uid'] for q in self.semente}) != len(self.semente):
            raise ValueError('Semente com IDs ou tópicos inválidos; todos os tópicos são obrigatórios')
        for item in self.itens:
            rows = self.por_item[item['id']]
            if len(rows) > item['meta'] or len(rows) != self.manifesto['semente_por_item'].get(item['id']):
                raise ValueError('Contagem da semente incompatível com as metas')
            for q in rows:
                C.validar_questao({k: q[k] for k in C.CAMPOS})
                if type(q.get('rodada')) is not int or q['rodada'] < 1 or not q['uid'].startswith(item['id']+':sc:'):
                    raise ValueError('Rodada ou UID da semente inválido')

    def config(self):
        cfg = dict(schema=C.SCHEMA, extensao_sem_contexto='full-v1',
                   itens=[i['id'] for i in self.itens], escopos_e_metas=self.itens,
                   manifesto_sha256=C.sha(self.manifesto), semente_sha256=C.sha(self.semente),
                   modelos=self.modelos, lote=self.lote, memoria=self.memoria,
                   prompt_sha256=C.sha(self.prompt), motor_sha256=C.sha(Path(C.__file__).read_text(encoding='utf-8')),
                   extensao_sha256=C.sha(Path(__file__).read_text(encoding='utf-8')),
                   criterio_parada='quantidade_gerada', conteudo_externo=False,
                   auditoria=False, refinamento=False, deduplicacao=False, filtro_qualidade=False)
        old = read_json(self.saida/'config.json')
        if old and {k: v for k, v in old.items() if k != 'criado_em'} != cfg:
            raise ValueError('Configuração mudou: use outra saída')
        # Confere todos os checkpoints antes de gravar qualquer semente.
        for item in self.itens:
            state = read_json(self.saida/'topicos'/item['id']/'estado.json')
            if state is not None:
                seed = self.por_item[item['id']]
                if state.get('questoes', [])[:len(seed)] != seed:
                    raise ValueError('Checkpoint perdeu ou alterou questões da semente')
        if not old:
            atomic_json(self.saida/'config.json', {**cfg, 'criado_em': C.agora()})
        atomic_json(self.saida/'metas.json', self.manifesto)
        atomic_json(self.saida/'limites_execucao.json', dict(max_lotes_por_topico=self.max_lotes, max_chamadas_cumulativas=self.max_chamadas))
        for item in self.itens:
            directory = self.saida/'topicos'/item['id']
            directory.mkdir(parents=True, exist_ok=True)
            path = directory/'estado.json'
            if not path.exists():
                seed = self.por_item[item['id']]
                atomic_json(path, dict(lotes=max((q['rodada'] for q in seed), default=0),
                    questoes=seed, recentes=[{k: q[k] for k in ('uid', 'pergunta', 'resposta')} for q in seed[-self.memoria:]], concluido=False))

    def relatorio(self):
        result = super().relatorio()
        rows = linhas(self.saida/'questoes.jsonl')
        byid = {q['uid']: q for q in rows}
        if len(byid) != len(rows) or any(byid.get(q['uid']) != q for q in self.semente):
            raise RuntimeError('Questões originais foram perdidas ou alteradas')
        result.update(preservadas=len(self.semente), novas=len(rows)-len(self.semente),
                      questoes_sha256=C.sha(rows), referencia_full_sha256=self.manifesto['full_sha256'])
        atomic_json(self.saida/'resultado.json', result)
        with (self.saida/'RELATORIO.md').open('a', encoding='utf-8') as f:
            f.write(f"\nPreservadas: {result['preservadas']}; novas: {result['novas']}. "
                    'Metas iguais ao Full por subtópico. Tipos sem cotas; não se iguala a composição por tipo.\n')
        return result


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--saida', type=Path, default=SAIDA)
    p.add_argument('--metas', type=Path, default=METAS_FULL)
    p.add_argument('--semente', type=Path, default=SEMENTE)
    p.add_argument('--workers', type=int, default=8)
    p.add_argument('--lote', type=int, default=5)
    p.add_argument('--memoria', type=int, default=20)
    p.add_argument('--max-lotes', type=int, default=100)
    p.add_argument('--max-chamadas', type=int, default=30000)
    p.add_argument('--lote-juiz', type=int, default=8)
    p.add_argument('--plano', action='store_true')
    p.add_argument('--so-avaliacao', action='store_true')
    p.add_argument('--sem-avaliacao', action='store_true')
    p.add_argument('--preparar-metas', action='store_true')
    a = p.parse_args(argv)
    if a.preparar_metas:
        preparar_metas(a.metas)
        return 0
    if a.so_avaliacao and a.sem_avaliacao:
        p.error('--so-avaliacao e --sem-avaliacao são incompatíveis')
    g = GeracaoFull(a.saida, metas=a.metas, semente=a.semente, workers=a.workers, lote=a.lote,
                   memoria=a.memoria, max_lotes=a.max_lotes, max_chamadas=a.max_chamadas)
    total = sum(i['meta'] for i in g.itens)
    print(f'Saída: {a.saida}\nPreservadas: {len(g.semente)}; novas: {total-len(g.semente)}; total: {total}', flush=True)
    if a.plano:
        for i in g.itens:
            print(f"{i['id']}: {len(g.por_item[i['id']])} → {i['meta']}")
        calls = sum((i['meta']-len(g.por_item[i['id']])+g.lote-1)//g.lote for i in g.itens)
        print(f'Plano sem API e sem criar saída. Geração: {calls} lotes; avaliação: {total*2} respostas + juiz.')
        return 0
    status = 0 if a.so_avaliacao else g.run()
    if status == 0 and not a.sem_avaliacao:
        from .avaliacao_full import avaliar
        status = avaliar(a.saida, workers=a.workers, lote_juiz=a.lote_juiz)
    return status


if __name__ == '__main__':
    raise SystemExit(main())
