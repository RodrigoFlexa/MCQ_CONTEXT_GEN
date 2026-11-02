# Comparação do benchmark

Histórico: questões do método anterior com seus contextos originais. Novo: fluxo contínuo aplicado às versões antiga e refinada dos documentos.
Sem meta fixa de questões. As tabelas integrais e equilibradas preservam os tamanhos reais. Resultados ausentes são indicados por —.

## Documentos usados

| Documento | Versão | Capítulos | Blocos | Palavras |
|---|---|---|---|---|
| 02_02 | antigo | 11 | 57 | 8379 |
| 02_02 | refinado | 12 | 60 | 9645 |
| 03_03 | antigo | 5 | 25 | 4230 |
| 03_03 | refinado | 6 | 29 | 5735 |
| 07_01 | antigo | 5 | 34 | 5602 |
| 07_01 | refinado | 5 | 37 | 6561 |

Dimensões descrevem o contexto; maior comprimento não demonstra melhor qualidade. Os ajustes estão nos arquivos revisao.json.

## Produção e cobertura da execução

| Grupo | Questões disponíveis | Candidatas | Admissão (%) | Documentos encerrados |
|---|---|---|---|---|
| Histórico | 60 | — | — | Existente |
| Novo + contexto antigo | 0 | 0 | — | 0/3 |
| Novo + contexto refinado | 0 | — | — | 0/3 |

Encerramento significa baixa produtividade observada nos contextos, não cobertura completa de todo o conhecimento. Histórico é amostra do banco anterior.

## Métricas textuais — Amostra equilibrada por documento e classe

| Grupo | N | Overlap Q–C | Max ROUGE-L | Novel 2 (%) | Novel 3 (%) | Self-BLEU 4 | Duplicatas exatas |
|---|---|---|---|---|---|---|---|
| Histórico | 0 | — | — | — | — | — | 0 |
| Novo + contexto antigo | 0 | — | — | — | — | — | 0 |
| Novo + contexto refinado | 0 | — | — | — | — | — | 0 |

ROUGE sem stopwords; sem lematização. Novel e sobreposição não comprovam raciocínio ou sustentação. Denominadores válidos por métrica estão em metricas.json.

## Diversidade semântica — Amostra equilibrada por documento e classe

| Grupo | N | Cosseno médio | Distância média | Cosseno vizinho | Vendi | Vendi centrado |
|---|---|---|---|---|---|---|
| Histórico | 0 | — | — | — | — | — |
| Novo + contexto antigo | 0 | — | — | — | — | — |
| Novo + contexto refinado | 0 | — | — | — | — | — |

E5 local; Vendi centrado é análise de sensibilidade separada. Comparar Vendi/Self-BLEU com o mesmo N. — significa indisponível, não zero.

## Métricas textuais — Conjuntos integrais

| Grupo | N | Overlap Q–C | Max ROUGE-L | Novel 2 (%) | Novel 3 (%) | Self-BLEU 4 | Duplicatas exatas |
|---|---|---|---|---|---|---|---|
| Histórico | 60 | 0.552 | 0.269 | 59.0 | 75.6 | 0.127 | 0 |
| Novo + contexto antigo | 0 | — | — | — | — | — | 0 |
| Novo + contexto refinado | 0 | — | — | — | — | — | 0 |

ROUGE sem stopwords; sem lematização. Novel e sobreposição não comprovam raciocínio ou sustentação. Denominadores válidos por métrica estão em metricas.json.

## Diversidade semântica — Conjuntos integrais

| Grupo | N | Cosseno médio | Distância média | Cosseno vizinho | Vendi | Vendi centrado |
|---|---|---|---|---|---|---|
| Histórico | 60 | 0.873 | 0.127 | 0.919 | 2.313 | 40.082 |
| Novo + contexto antigo | 0 | — | — | — | — | — |
| Novo + contexto refinado | 0 | — | — | — | — | — |

E5 local; Vendi centrado é análise de sensibilidade separada. Comparar Vendi/Self-BLEU com o mesmo N. — significa indisponível, não zero.

## Distribuição de tipos

| Grupo | conceito | mecanismo | consequencia | diagnostico | decisao | procedimento | Compostas |
|---|---|---|---|---|---|---|---|
| Histórico | 12 | 10 | 8 | 9 | 10 | 11 | 11 |
| Novo + contexto antigo | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Novo + contexto refinado | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

Composição é outra dimensão: não se soma como sétima classe. Sua classificação é automática, sem teste de ablação nesta versão.

## Desempenho — amostra equilibrada

| Grupo | Respondente | Questões | Pares válidos | Sem par | Sem contexto (%) | Com contexto (%) | Gap (p.p.) | IC 95% gap |
|---|---|---|---|---|---|---|---|---|

Pares são a mesma pergunta com/sem contexto; grupos contêm perguntas diferentes. Parciais contam como erro na acurácia estrita; bloqueios/falhas não recebem zero. Avaliação pendente se tabela vazia.

## Desempenho — conjuntos integrais

| Grupo | Respondente | Questões | Pares válidos | Sem par | Sem contexto (%) | Com contexto (%) | Gap (p.p.) | IC 95% gap |
|---|---|---|---|---|---|---|---|---|

Pares são a mesma pergunta com/sem contexto; grupos contêm perguntas diferentes. Parciais contam como erro na acurácia estrita; bloqueios/falhas não recebem zero. Avaliação pendente se tabela vazia.

## Sustentação dos gabaritos — auditoria adicional

| Grupo | Total | Processadas | Com decisão | Sustentados | Insuficientes | Contradições | Sustentação (%) |
|---|---|---|---|---|---|---|---|

Auditoria adicional à admissão, automática e sujeita a erro. Inconclusivos/bloqueios ficam fora da taxa; estados completos estão em comparacao.json.

## Diferenças descritivas — amostra equilibrada

| Comparação | Métrica | N referência | N refinado | Diferença |
|---|---|---|---|---|
| Refinado − Histórico | overlap_q_c | 0 | 0 | — |
| Refinado − Histórico | max_rougeL_f1_sem_stop | 0 | 0 | — |
| Refinado − Histórico | novel_2gram_pct | 0 | 0 | — |
| Refinado − Histórico | novel_3gram_pct | 0 | 0 | — |
| Refinado − Novo + contexto antigo | overlap_q_c | 0 | 0 | — |
| Refinado − Novo + contexto antigo | max_rougeL_f1_sem_stop | 0 | 0 | — |
| Refinado − Novo + contexto antigo | novel_2gram_pct | 0 | 0 | — |
| Refinado − Novo + contexto antigo | novel_3gram_pct | 0 | 0 | — |

Diferenças não isolam efeitos causais do contexto/gerador, nem representam automaticamente melhoria. Os grupos novos partem do mesmo banco inicial e crescem separadamente.
