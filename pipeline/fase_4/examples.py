"""Pool de QA com avaliação humana e notas do Judge; few-shot de outros tópicos."""
import random
from collections import defaultdict

from pipeline.qa_references.download_qa_examples import CHOICE_REFERENCES, CONTEXT_REFERENCES
from .domain import human_seeds, legacy, TOPICOS
from .storage import read_jsonl, write_jsonl


def canonical_topic(name):
    norm = legacy.normalizar(name).split("(")[0].strip()
    if not norm:
        return ""
    for topic in TOPICOS:
        target = legacy.normalizar(topic).split("(")[0].strip()
        if norm == target or target.startswith(norm) or norm.startswith(target):
            return topic
    words = legacy.palavras_conteudo(name)
    scores = [(len(words & legacy.palavras_conteudo(t)) / max(1, len(words)), t) for t in TOPICOS]
    score, topic = max(scores, default=(0, ""))
    return topic if score >= 0.60 else ""


def standalone(question):
    return isinstance(question, str) and not CHOICE_REFERENCES.search(question) and not CONTEXT_REFERENCES.search(question)


def build_seed_bank(cfg):
    rows = []
    # Mantém o procedimento já existente de seleção por preferência humana.
    if cfg.human_ratings.is_dir():
        originals = human_seeds.construir_banco_seed(cfg.human_ratings, cfg.min_human_preference, verbose=False)
        for q in originals:
            topic = canonical_topic(q.get("topico", ""))
            if not topic or not standalone(q["stem"]):
                continue
            rows.append({"id": "fase2:" + q["id"], "question": q["stem"],
                         "answer": q["alternatives"][q["correct_answer_index"]],
                         "topic": topic, "subtopic": "", "origin": "human_preference_phase2",
                         "human_preference_score": q["nota"], "votes": q["votos"],
                         "pair_id": q["pair_id"], "selection_weight": 2 * (0.5 + q["nota"]),
                         "evaluation_type": "pairwise_human_preference"})
    for q in read_jsonl(cfg.reviewed_seeds):
        path = q.get("topic_path", "").split(" > ")
        topic = canonical_topic(path[0])
        if not topic or not standalone(q.get("question", "")):
            continue
        # Só o arquivo de candidatas conservadoras, não as aprovações com ressalvas.
        if q.get("review_comment", "").strip().casefold() != "aprovada" and not q.get("seed_note", "").startswith("aprovada sem ressalva"):
            continue
        rows.append({"id": f"especialista:{q['review_id']}", "question": q["question"],
                     "answer": q["answer"], "topic": topic, "subtopic": path[1] if len(path) > 1 else "",
                     "origin": "expert_approved", "human_approved": True,
                     "review_id": q["review_id"], "review_comment": q["review_comment"],
                     "selection_weight": 3.0, "evaluation_type": "binary_expert_approval"})
    unique = {}
    for q in rows:
        key = " ".join(legacy.tokenizar(legacy.normalizar(q["question"])))
        if key not in unique or q["selection_weight"] > unique[key]["selection_weight"]:
            unique[key] = q
    bank = list(unique.values())
    if not bank:
        raise ValueError("Nenhuma questão humana melhor avaliada disponível: não será usado few-shot arbitrário")
    return bank


class ExamplePool:
    def __init__(self, cfg, seeds, accepted):
        self.cfg, self.seeds, self.accepted = cfg, seeds, accepted

    def sample_quality(self, topic, round_number):
        rng = random.Random(f"{self.cfg.seed}:{topic}:{round_number}:quality")
        generated = [q for q in self.accepted if q.get("nota", 0) >= self.cfg.minimum_fewshot_quality]
        seed_weight = max(0.1, 1 - len(generated) / 40)
        pool = [(q, q["selection_weight"] * seed_weight) for q in self.seeds if q["topic"] != topic]
        pool += [(q, q["nota"]) for q in generated if q["topic"] != topic]
        if not pool:
            raise ValueError(f"Sem exemplos melhor avaliados de outros tópicos para {topic}")
        chosen = []
        for _ in range(min(self.cfg.cross_topic_examples, len(pool))):
            pos = rng.choices(range(len(pool)), weights=[weight for _, weight in pool], k=1)[0]
            chosen.append(pool.pop(pos)[0])
        return chosen


def load_external(path):
    values = read_jsonl(path)
    clean, seen = [], set()
    for q in values:
        question, answer = q.get("question"), q.get("answer")
        if not standalone(question) or not isinstance(answer, str) or not answer.strip():
            continue
        key = " ".join(question.casefold().split())
        if key not in seen:
            seen.add(key)
            clean.append(q)
    if not clean:
        raise ValueError("Sem exemplos externos QA. Execute o downloader antes da geração")
    return clean


def sample_external(rows, count, seed):
    rng = random.Random(str(seed))
    groups = defaultdict(list)
    for q in rows:
        groups[str(q.get("id", "unknown")).split(":")[0]].append(q)
    for group in groups.values():
        rng.shuffle(group)
    chosen = []
    for source in ("pira_ptbr", "arc_challenge", "arc_easy"):
        if groups[source] and len(chosen) < count:
            chosen.append(groups[source].pop())
    names = list(groups)
    rng.shuffle(names)
    while len(chosen) < count and any(groups[name] for name in names):
        for name in names:
            if groups[name] and len(chosen) < count:
                chosen.append(groups[name].pop())
    return chosen
