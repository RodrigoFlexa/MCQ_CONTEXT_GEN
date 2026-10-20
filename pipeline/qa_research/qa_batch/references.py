"""Endereços verificáveis para a auditoria; o modelo seleciona IDs, sem recitar texto."""
import copy
import re

from . import contracts as C


def catalog(context, questions):
    # Não truncar nem resumir: todo o contexto continua disponível ao auditor.
    passages = {f"C{i:04d}": part for i, part in enumerate(
        (p.strip() for p in re.split(r"\n\s*\n", context) if p.strip()), 1)}
    conditions = {}
    for question in questions:
        parts = re.split(r"(?<=[.!?;])\s+", question["pergunta"])
        conditions.update({f"Q{question['id']}_S{i}": part
                           for i, part in enumerate(parts, 1) if part.strip()})
    return {"contexto": passages, "enunciados": conditions}


def decode_review(response, references):
    """Converte apenas IDs existentes em passagens exatas, sem aceitar paráfrases."""
    data = copy.deepcopy(response)
    C.obj(data, ("itens", "diversidade"))
    C.rows(data["itens"])
    for row in data["itens"]:
        ids = row.get("fundamentos")
        C.texts(ids)
        passages = []
        for identifier in ids:
            if identifier not in references["contexto"]:
                raise ValueError(f"Item {row['id']}: fundamento {identifier[:50]!r} não é ID do contexto")
            passages.append(references["contexto"][identifier])
        row["fundamentos"] = passages
        check = row.get("teste_de_unicidade")
        C.obj(check, ("outra_resposta_plausivel", "condicao_que_a_exclui"))
        identifiers = check["condicao_que_a_exclui"]
        C.texts(identifiers)
        own = [key for key in references["enunciados"] if key.startswith(f"Q{row['id']}_S")]
        if len(set(identifiers)) != len(identifiers) or any(key not in own for key in identifiers):
            raise ValueError(f"Item {row['id']}: condições devem usar IDs únicos do próprio enunciado")
        if identifiers:
            positions = [own.index(key) for key in identifiers]
            # Recupera um intervalo contínuo, inclusive quando duas condições
            # separadas são necessárias. Nenhuma palavra é criada pelo modelo.
            selected = own[min(positions):max(positions) + 1]
            check["condicao_que_a_exclui"] = " ".join(references["enunciados"][key] for key in selected)
        else:
            check["condicao_que_a_exclui"] = ""
    return data
