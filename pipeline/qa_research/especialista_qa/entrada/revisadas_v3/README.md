# Entrada ampliada das questões revisadas

nao_reprovadas_mcq.jsonl contém 720 candidatas: 446 aprovações simples,
270 aprovações com observações/ressalvas e 4 pareceres sem aprovação explícita.
São excluídas 280 reprovações/ordens de descarte, inclusive quando aparecem
ao fim do comentário após uma aprovação inicial (questões 25, 86 e 165).

O comentário humano, as alternativas, o gabarito original, as notas, os
parágrafos de origem e o hash do DOCX são preservados. Aprovação da MCQ e
aprovação automática do QA são decisões separadas. As quatro candidatas
sem aprovação explícita são identificadas por faixa_parecer.

curadoria_todas.jsonl e selecao.csv registram as 1.000 decisões de inclusão.
extracao.json contém critérios e contagens. diagnostico_v2.json resume os
motivos das 271 conversões reprovadas, com critérios sobrepostos.
O servidor lê os JSONLs diretamente; não precisa do Word ou do DOCX.

Para reproduzir a seleção offline:

    python -m pipeline.qa_research.especialista_qa preparar-revisadas-v3
