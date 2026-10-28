# QA: 100 palavras, esforço medium e acurácia ao vivo

Reavalia duas amostras fixas, sem gerar ou modificar perguntas:

- Sem contexto: primeiro sorteio de 1.000 QAs do baseline bruto (2.818).
- Default + Ampliado: primeiro sorteio de 1.000 QAs das 2.818 originais + 670 revisadas.

A seleção segue a resposta do usuário “Default + ampliado”. A amostra com contexto
não usa o Full nem as 623 QAs autorais. Os mesmos IDs usados nos gráficos estão
congelados em amostras_1000.json, semente 20261028, repetição 1. O servidor não
precisa dos arquivos locais de análise nem de NumPy.

## Executar no servidor

```bash
git pull --ff-only origin codex/qa-evidencias-verificadas &&
bash pipeline/qa_research/rodar_qa_medium.sh
```

São **4.000 respostas novas**, mais julgamentos: 2.000 perguntas × 2 respondentes.
GPT-5.4 Nano e GPT-5.4 usam os mesmos deployments Petrobras com esforço `medium`.
Ambos são obrigatórios. O juiz continua gpt-5-4-petrobras:medium, em lotes de 8.
Os respondentes recebem **somente a pergunta**, inclusive nas QAs geradas com
contexto. O conteúdo de geração e os gabaritos não são enviados aos respondentes.

Saída: pipeline/qa_research/relatorios/qa_100_palavras_medium_1000.
Repita o comando para retomar sem refazer respostas e notas salvas. Os resultados
anteriores de 50 palavras/low não são sobrescritos nem reutilizados como respostas
desta nova rodada. Há duas sondagens de disponibilidade por execução.

```bash
# Plano sem API, sem criação de saída:
bash pipeline/qa_research/rodar_qa_medium.sh --plano
```

Opções: --saida, --workers 8 (respondentes), --judge-workers 2, --lote-juiz 8,
--manifesto. Mudanças em IDs, conteúdo, modelos, prompts, código ou lote do juiz
impedem misturar protocolos. Workers podem variar na retomada.

## Terminal ao vivo

As duas condições são alternadas na fila de respostas. Respondentes trabalham em
paralelo; assim que um modelo acumula um lote pronto, trabalhadores separados
fazem o julgamento enquanto as outras respostas continuam. Não espera terminar
as 2.000 perguntas para mostrar acurácia.

Cada lote julgado atualiza e imprime as quatro combinações de condição/modelo:

```text
[AO VIVO | sem_contexto | gpt-5-4] respostas .../1000 | julgadas ... | C/P/I .../.../... | sem nota ... | acurácia ...%
[AO VIVO | default_ampliado | gpt-5-4-nano] respostas .../1000 | julgadas ... | C/P/I .../.../... | sem nota ... | acurácia ...%
```

Antes do primeiro julgamento, a acurácia aparece como “—”. A cada dez respostas
salvas há uma linha de progresso; se as chamadas demorarem, há aviso a cada
15 segundos de espera sem conclusão. Acurácia só muda após o julgamento.
São valores parciais do conjunto processado, não estimativas do resultado final.

Use o comando em primeiro plano para acompanhar. Se quiser também salvar o
console, o pipeline deve preservar o código de erro:

```bash
set -o pipefail
bash pipeline/qa_research/rodar_qa_medium.sh 2>&1 | tee qa_medium.console.log
```

## Prompts revisados

Os novos prompts estão em prompts/respondente.md e prompts/juiz.md. Não alteram
os arquivos nem fingerprints das avaliações históricas.

Respondedor: resposta direta em português, até 100 palavras, suficiente para
todas as partes essenciais; orientações específicas para procedimentos e
mecanismos; sem premissas ou números inventados; JSON com a resposta. O limite
é solicitado no prompt: respostas que o excederem são contadas e sinalizadas,
sem truncamento, regeneração ou exclusão de conteúdo.

Juiz: avalia significado e requisitos da pergunta, aceita paráfrases e equivalência
técnica, distingue componentes essenciais de detalhes opcionais do gabarito,
não favorece extensão e exige justificativa concreta para parcial/incorreta.
Se a pergunta pede etapas ou mecanismo, esse conteúdo deve estar presente; se
pede apenas o elemento decisivo, não exige repetir explicações complementares.
Problemas percebidos na referência devem ser registrados na justificativa.
Não há exemplos de QA nem outros datasets nos prompts.

As categorias continuam correta/parcial/incorreta. A rubrica é uma melhoria
proposta, ainda sujeita a revisão humana de concordância; testes offline não
demonstram que um juiz LLM ficou mais correto. A orientação segue as
[boas práticas oficiais de avaliação OpenAI](https://developers.openai.com/api/docs/guides/evaluation-best-practices),
que destacam rubricas claras, viés por extensão e validação contra julgamento humano.

## Interpretação e rastreabilidade

**Esta rodada muda simultaneamente o limite de palavras, o esforço do respondente
e os prompts de resposta/julgamento.** Diferenças de acurácia medem o conjunto
dessas mudanças, não o efeito isolado de medium ou de 100 palavras. Para isolar
efeitos seria preciso uma ablação adicional ou julgar respostas antigas com a
nova rubrica; isso não é executado por este comando.

Bloqueios do respondente ou juiz são terminais e sem nota, fora do denominador,
com cobertura explícita. Lotes bloqueados pelo juiz não são divididos ou reenviados.
Falhas transitórias deixam pendências para retomar. Não há filtros de qualidade,
deduplicação nem remoção de questões. Gabaritos não passam por validação documental
adicional; o juiz compara conteúdo técnico e não certifica uma verdade externa.

Arquivos principais: config.json, amostras.json, questoes.jsonl;
avaliacao/ACURACIA.md, acuracia.json, acuracia_por_condicao.csv, avaliacoes.jsonl,
protocolo_experimento.json e avaliacao_concluida.json; respostas/ e juiz/ mantêm
respostas/vereditos e justificativas por lote. As exportações incluem condição,
número de palavras e status por modelo. O script imprime coleta, commit e push
ao terminar. Nenhuma nova geração de questões é realizada.
