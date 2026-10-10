# Fase 4 — PetroQuest QA

Esta fase gera somente pares pergunta/resposta, sem alternativas ou distratores. O limite de 100 é **por tópico**, distribuído em rodízio entre seus subtópicos. As dificuldades fácil, média e difícil são alternadas para equilibrar a saída.

## Métricas e critério desta rodada

- Similaridade semântica por cosine com `paraphrase-multilingual-MiniLM-L12-v2`; decisão ativa padrão: rejeitar a partir de 0,50. Cada candidata também registra decisões simuladas para 0,70 e 0,85.
- Comparadores adicionais: duplicata exata, Jaccard lexical e Jaccard de trigramas de caracteres.
- Diversidade: razão tipos/tokens, vocabulário novo e número de trigramas; entropia normalizada dos focos conceituais.
- Entropia, novidade e saturação são observacionais e **não interrompem** esta rodada. O tópico termina ao alcançar 100 aceitas ou ao atingir `--max-attempts-per-topic`/`--max-calls`.
- Cada candidata tem um registro em `candidatas_metricas.jsonl`, mesmo quando rejeitada. A lista aceita é `questoes_qa.jsonl`; resumo por tópico em `resumo_topicos.jsonl`.
- `--observe-only` registra o que os limites de cosine recusariam, sem usá-los como filtro (duplicatas exatas continuam rejeitadas). Use outra pasta de saída para essa comparação.

## Preparar os dados e iniciar

No servidor com acesso à internet:

```bash
python pipeline/qa_references/download_qa_examples.py --max-per-dataset 0
python pipeline/fase_4/run_qa.py --deployment gpt-5-4-petrobras --effort high --limit-per-topic 100 --similarity-threshold 0.50
```

O downloader preserva apenas pergunta e resposta. No ARC, resolve a `answerKey` para o texto da resposta e remove as alternativas; perguntas que pedem para selecionar opções são filtradas. Exemplos externos são apenas referência de formato. Seeds do especialista são sorteadas de outros tópicos para evitar uso de conteúdo como fato.

Para retomar uma execução interrompida, repetir o comando com `--resume`. Para comparar apenas as decisões semânticas em outra saída:

```bash
python pipeline/fase_4/run_qa.py --deployment gpt-5-4-petrobras --effort high --limit-per-topic 100 --observe-only --output pipeline/fase_4/saida_qa_observacao
```

Configure o `.env`/ambiente conforme [azure_openai_backend.py](../../azure_openai_backend.py). Não comite credenciais, dados baixados ou resultados brutos. O notebook [petroquest_fase4_qa.ipynb](petroquest_fase4_qa.ipynb) apresenta a revisão do prompt, execução e análise.
