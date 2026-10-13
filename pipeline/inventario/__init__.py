"""Inventário de conhecimento do PetroQuest.

Constrói, a partir das frases do especialista e dos corpora de domínio, notas técnicas por
conceito para cada assunto, base da futura geração de QA. Alternativas permanecem em standby.

Etapas: assuntos -> varredura lexical -> seleção bilíngue -> fatos com citação -> conceitos ->
nota técnica (redator) + revisão -> documentos e índices.
"""
VERSION = "inventario-v4-notas"
