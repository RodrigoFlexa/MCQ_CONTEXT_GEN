"""Validação mecânica. Correção técnica e ambiguidade exigem auditoria semântica."""
import re

IDS = list(range(1, 10))
CRITERIA = ("fundamento", "correcao_tecnica", "resposta_determinada", "autonomia",
            "sem_pistas", "dificuldade", "contexto_brasileiro", "foco", "aderencia_ao_plano")


def obj(value, keys):
    if not isinstance(value, dict) or set(value) != set(keys):
        raise ValueError("Objeto deve conter somente: " + ", ".join(keys))


def text(value, *, empty=False):
    if not isinstance(value, str) or (not empty and not value.strip()):
        raise ValueError("Texto não vazio esperado")


def texts(value, *, nonempty=False):
    if not isinstance(value, list) or (nonempty and not value):
        raise ValueError("Lista de textos esperada")
    for entry in value:
        text(entry)


def short(value):
    text(value)
    if len(value.split()) > 50:
        raise ValueError("Resposta excede o máximo de 50 palavras")


def norm(value):
    return " ".join(value.split())


def quotes(value, context, *, required=True, label="Fundamento"):
    texts(value, nonempty=required)
    for index, passage in enumerate(value, 1):
        if norm(passage) not in norm(context):
            raise ValueError(f"{label}[{index}]: passagem não literal do contexto: {passage[:180]!r}. "
                             "Copie um trecho contínuo exatamente como está no contexto, sem paráfrases ou reticências.")


def rows(value, ids=IDS):
    if not isinstance(value, list) or len(value) != len(ids):
        raise ValueError(f"Esperados exatamente {len(ids)} itens")
    if any(not isinstance(row, dict) or type(row.get("id")) is not int for row in value):
        raise ValueError("Cada item deve ter um ID inteiro")
    if [row["id"] for row in value] != list(ids):
        raise ValueError("IDs devem ser únicos, completos e ordenados: " + str(list(ids)))


def expected_difficulty(item_id):
    return "facil" if item_id <= 3 else "media" if item_id <= 6 else "dificil"


def difficulty(row):
    if row["dificuldade"] != expected_difficulty(row["id"]):
        raise ValueError("Dificuldade incompatível com o ID")


def envelope(data, field):
    obj(data, ("status", "motivo", field))
    text(data["motivo"], empty=True)
    if data["status"] == "insuficiente":
        text(data["motivo"])
        if data[field] != []:
            raise ValueError("Insuficiência deve retornar lista vazia")
        return False
    if data["status"] != "ok" or data["motivo"].strip():
        raise ValueError("Sucesso exige status ok e motivo vazio")
    return True


def plan(data, context):
    if not envelope(data, "itens"):
        return
    rows(data["itens"])
    targets = []
    for row in data["itens"]:
        obj(row, ("id", "dificuldade", "alvo", "resposta_esperada", "condicoes_necessarias",
                  "exigencia_cognitiva", "fundamentos"))
        difficulty(row)
        text(row["alvo"])
        short(row["resposta_esperada"])
        texts(row["condicoes_necessarias"])
        text(row["exigencia_cognitiva"])
        quotes(row["fundamentos"], context, label=f"Item {row['id']} fundamentos")
        targets.append(norm(row["alvo"]).casefold())
    if len(set(targets)) != 9:
        raise ValueError("Alvos idênticos no plano")


def questions(data, ids=IDS):
    if not envelope(data, "questoes"):
        return
    rows(data["questoes"], ids)
    seen = set()
    for row in data["questoes"]:
        obj(row, ("id", "dificuldade", "pergunta", "resposta"))
        difficulty(row)
        text(row["pergunta"])
        short(row["resposta"])
        key = re.sub(r"\W+", " ", row["pergunta"].casefold()).strip()
        if key in seen:
            raise ValueError("Perguntas idênticas no lote")
        seen.add(key)


def blind(data):
    obj(data, ("resolucoes",))
    rows(data["resolucoes"])
    for row in data["resolucoes"]:
        obj(row, ("id", "status", "resposta", "outras_respostas", "condicoes_faltantes"))
        if row["status"] not in {"respondida", "ambigua", "sem_suporte"}:
            raise ValueError("Estado de resolução inválido")
        text(row["resposta"], empty=row["status"] != "respondida")
        if row["resposta"]:
            short(row["resposta"])
        texts(row["outras_respostas"])
        texts(row["condicoes_faltantes"])
        if row["status"] == "respondida" and (row["outras_respostas"] or row["condicoes_faltantes"]):
            raise ValueError("Resolução determinada não pode declarar alternativas ou condições ausentes")


def review(data, context, question_rows):
    obj(data, ("itens", "diversidade"))
    rows(data["itens"])
    rows(question_rows)
    enunciados = {q["id"]: q["pergunta"] for q in question_rows}
    for row in data["itens"]:
        obj(row, ("id", "criterios", "motivo", "correcao_sugerida", "fundamentos",
                  "teste_de_unicidade", "dificuldade_observada"))
        obj(row["criterios"], CRITERIA)
        if any(type(v) is not bool for v in row["criterios"].values()):
            raise ValueError("Cada critério deve ser booleano")
        passed = all(row["criterios"].values())
        text(row["motivo"], empty=passed)
        text(row["correcao_sugerida"], empty=True)
        quotes(row["fundamentos"], context, required=row["criterios"]["fundamento"],
               label=f"Item {row['id']} fundamentos")
        check = row["teste_de_unicidade"]
        obj(check, ("outra_resposta_plausivel", "condicao_que_a_exclui"))
        for value in check.values():
            text(value, empty=True)
        condition = check["condicao_que_a_exclui"].strip()
        if condition:
            if not check["outra_resposta_plausivel"].strip():
                raise ValueError("Condição discriminante exige uma resposta concorrente")
            if norm(condition) not in norm(enunciados[row["id"]]):
                raise ValueError("Condição discriminante deve ser passagem literal da pergunta")
        if row["dificuldade_observada"] not in {"facil", "media", "dificil", "indeterminada"}:
            raise ValueError("Dificuldade observada inválida")
    diversity = data["diversidade"]
    obj(diversity, ("ok", "ids_conflitantes", "motivo"))
    if type(diversity["ok"]) is not bool:
        raise ValueError("diversidade.ok deve ser booleano")
    ids = diversity["ids_conflitantes"]
    if (not isinstance(ids, list) or any(type(i) is not int or i not in IDS for i in ids)
            or len(set(ids)) != len(ids)):
        raise ValueError("IDs conflitantes inválidos")
    if (diversity["ok"] and ids) or (not diversity["ok"] and len(ids) < 2):
        raise ValueError("Conflito de diversidade exige ao menos dois IDs")
    text(diversity["motivo"], empty=diversity["ok"])


def rejected(audit, resolution):
    bad = {r["id"] for r in audit["itens"] if not all(r["criterios"].values())}
    # A decisão também respeita os achados estruturados, mesmo se os booleanos
    # vierem complacentes ou em desacordo com o restante da própria auditoria.
    for row in audit["itens"]:
        check = row["teste_de_unicidade"]
        if (check["outra_resposta_plausivel"].strip()
                and not check["condicao_que_a_exclui"].strip()):
            bad.add(row["id"])
        if row["dificuldade_observada"] != expected_difficulty(row["id"]):
            bad.add(row["id"])
    bad.update(r["id"] for r in resolution["resolucoes"] if r["status"] != "respondida")
    bad.update(audit["diversidade"]["ids_conflitantes"])
    return sorted(bad)
