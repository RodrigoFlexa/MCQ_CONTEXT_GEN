# Repositório definitivo de questões

Questões validadas por especialista do domínio. Cada linha de `questoes.jsonl` é uma questão de
pergunta e resposta curta; `questoes.csv` traz os mesmos dados em tabela.

Lote atual: `especialista_2026-10-21`, 56 questões.

- `status = aprovada` — aprovada sem ressalvas; texto original preservado.
- `status = aprovada_com_ressalvas_editada` — texto editado conforme o parecer;
  `pergunta_original`, `resposta_original` e `justificativa_edicao` registram a mudança.

Questões reprovadas não entram aqui.

Campos principais: `id` (`PQ-<item>-<id da candidata>`), tópico e subtópico, `dificuldade`
(nível da geração, não reclassificado), `parecer_especialista`, `contexto` (documento da v1 usado na
geração e documento vigente na v2) e `origem` (lote, código do formulário e arquivos de auditoria).

Gerado por `pipeline/qa_research/revisao_especialista/aplicar_revisao.py`; não edite à mão.
