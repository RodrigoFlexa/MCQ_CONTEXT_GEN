"""Inventário de conhecimento do PetroQuest.

Constrói, a partir das frases do especialista e dos corpora de domínio, um
inventário de unidades de conhecimento por assunto (fichas), para futura
geração de QA. Alternativas permanecem em standby.

Etapas: assuntos -> varredura lexical -> seleção densa (GPU) -> extração de
unidades (LLM) -> consolidação -> fichas e relatório de cobertura.
"""
VERSION = "inventario-v2-azure"
