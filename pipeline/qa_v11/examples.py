"""Exemplos positivos selecionados por tarefa; pareceres separados para calibração/revisão."""
import re
from pathlib import Path

from pipeline.inventario.textutil import content_words, norm, read_jsonl, sha, write_jsonl
from pipeline.qa_references.download_qa_examples import CHOICE_REFERENCES, CONTEXT_REFERENCES


def cognitive_tags(question):
    q = norm(question)
    tags = set()
    for tag, pattern in {
        'comparacao': r'diferenc|compar|enquanto|ambos',
        'diagnostico': r'causa|sintoma|diagnos|observ|falha',
        'decisao': r'decis|mais adequad|prioriz|deve|escolh',
        'aplicacao': r'durante|considere|em um|em uma|se ',
        'integracao': r'combin|integr|simult|interdepend',
    }.items():
        if re.search(pattern, q):
            tags.add(tag)
    return tags or {'compreensao'}


class ExampleBank:
    def __init__(self, review_path, external_path, seed=42):
        self.seed = seed
        rows = read_jsonl(review_path)
        external = read_jsonl(external_path)
        if not rows or not external:
            raise ValueError('Exemplos próprios e externos são obrigatórios. Baixe os externos com o script indicado no README v11.')
        topics = sorted({r.get('topic_path', '').split(' > ')[0] for r in rows}, key=lambda t: sha(str(seed) + t, 40))
        held_topics = set(topics[:max(1, len(topics) // 5)])
        split = {}
        for r in rows:
            split[r['review_id']] = ('reservado' if r.get('topic_path', '').split(' > ')[0] in held_topics
                                     else 'calibracao' if int(sha(str(r['review_id']) + str(seed), 8), 16) % 5 == 0
                                     else 'demonstracao')
        # Conservador: resposta literalmente equivalente herda a partição mais reservada.
        family = {}
        priority = {'demonstracao': 0, 'calibracao': 1, 'reservado': 2}
        for r in rows:
            key = norm(re.sub(r'\W+', ' ', r.get('answer', ''))).strip()
            if key and priority[split[r['review_id']]] > priority.get(family.get(key, ''), -1):
                family[key] = split[r['review_id']]
        self.partitions = {k: [] for k in priority}
        for r in rows:
            key = norm(re.sub(r'\W+', ' ', r.get('answer', ''))).strip()
            part = family.get(key, split[r['review_id']])
            self.partitions[part].append({**r, 'particao': part,
                                         'rotulo_origem': 'parecer_especialista_classificado_por_regras',
                                         'rotulo_requer_conferencia': True})
        self.not_reserved = {r['review_id']: r for part in ('demonstracao', 'calibracao')
                             for r in self.partitions[part]}
        self.positive = [dict(id=f"especialista:{r['review_id']}", pergunta=r['question'], resposta=r['answer'],
                              topico=r.get('topic_path', ''), origem='questao_propria_revisada')
                         for r in self.partitions['demonstracao']
                         if r.get('seed_candidate') and r.get('review_status') == 'aprovada'
                         and not r.get('flags') and not CHOICE_REFERENCES.search(r['question'])
                         and not CONTEXT_REFERENCES.search(r['question'])]
        self.external = [dict(id=r['id'], pergunta=r['question'], resposta=r['answer'],
                              topico='', origem=r.get('source_dataset', ''),
                              demonstracao_evidencias=r.get('reasoning_context', [])) for r in external
                         if r.get('question') and r.get('answer')
                         and not CHOICE_REFERENCES.search(r['question'])
                         and not CONTEXT_REFERENCES.search(r['question'])]
        if not self.positive or not self.external:
            raise ValueError('Banco limpo de demonstrações ficou vazio; revise a curadoria')

    def export(self, directory):
        for part, rows in self.partitions.items():
            write_jsonl(Path(directory) / f'{part}.jsonl', rows)

    def choose(self, objective, topic):
        words = set(content_words(objective['descricao']))
        skill = objective['habilidade']
        def ranking(e):
            tokens = set(content_words(e['pergunta']))
            task = skill in cognitive_tags(e['pergunta'])
            relevance = len(words & tokens) / max(1, len(words | tokens))
            return (-int(task), -relevance, sha(f"{self.seed}:{e['id']}:{objective['descricao']}", 40))
        own = sorted(self.positive, key=ranking)[:2]
        external = sorted(self.external, key=ranking)
        chosen, sources = [], set()
        for e in external:
            source = e['id'].split(':', 1)[0]
            if source not in sources:
                chosen.append(e)
                sources.add(source)
            if len(chosen) == 2:
                break
        return {'proprios': own, 'externos': chosen}

    def anchors(self):
        negatives = [r for r in self.partitions['calibracao'] if r.get('flags') and r.get('review_comment')]
        positives = [r for r in self.partitions['calibracao'] if r.get('review_status') == 'aprovada'
                     and r.get('seed_candidate') and not r.get('flags')][:2]
        selected = [{'id': r['review_id'], 'pergunta': r['question'], 'resposta': r.get('answer'),
                     'parecer': r['review_comment'], 'sinais': [], 'comparadas': [],
                     'uso': 'exemplo positivo de calibração; não é fonte factual do item novo'} for r in positives]
        flags = set()
        negative_count = 0
        for r in negatives:
            new = set(r['flags']) - flags
            if new:
                pairs = []
                if 'repeticao_ou_semelhanca' in r['flags']:
                    cited = re.findall(r'(?:quest[aã]o|q\.?|n[ºo.]?)\s*(\d{1,4})', r['review_comment'], re.I)
                    pairs = [self.not_reserved[int(i)] for i in cited if int(i) in self.not_reserved
                             and int(i) != r['review_id']]
                    if not pairs:
                        # Uma alegação de repetição sem o outro item não é demonstração suficiente.
                        new.discard('repeticao_ou_semelhanca')
                        if not new:
                            continue
                selected.append({'id': r['review_id'], 'pergunta': r['question'], 'resposta': r.get('answer'),
                                 'parecer': r['review_comment'], 'sinais': r['flags'],
                                 'comparadas': [{'pergunta': p['question'], 'resposta': p.get('answer')} for p in pairs],
                                 'uso': 'calibração do tipo de defeito; não é fonte factual do item novo'})
                flags.update(new)
                negative_count += 1
            if negative_count >= 3:
                break
        return selected
