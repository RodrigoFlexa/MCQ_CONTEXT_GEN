# Piloto de dificuldade v2: inventário x EC v13

Rubrica e motivação: [`../DIFICULDADE_V2.md`](../DIFICULDADE_V2.md). Resumo: no piloto v1
(`relatorios/piloto_inventario_20261023T042252Z`) as difíceis não foram mais difíceis que as fáceis
para um modelo pequeno sem contexto, porque muitas eram de sim ou não, de escolha entre duas opções
ou de prudência genérica, e porque o enunciado trazia a interpretação dos sinais. A v2 define a
difícil pelo trabalho que o enunciado não faz: um passo intermediário oculto e uma resposta atraente
descartada por uma observação.

## O que muda em relação à v1

| | v1 | v2 |
|---|---|---|
| Difícil A | diagnóstico com explicação concorrente | diagnóstico com **resposta atraente** explícita e o sinal que a descarta no enunciado |
| Difícil B | combinação de relações que "interagem" | **encadeamento**: A → ponte oculta → resposta específica (ou mascaramento) |
| Forma | livre | pergunta aberta; sem sim/não, escolha binária ou "conclusão sobre a decisão" (checado em código) |
| Resposta | até 50 palavras | começa pelo elemento decisivo, até 30 palavras |
| Campo `desenho` | não | passo oculto, resposta atraente e sinal que descarta (obrigatório nas difíceis) |
| EC | prompt v12 | prompt v13 com a mesma rubrica |
| Amostra | 100 por método, 24 difíceis | por documento: 10 fáceis, 10 médias e uma difícil por janela EC (60 difíceis por método) |
| Respondentes | gpt-4-1-nano | gpt-4-1-nano e gpt-5-4-nano:low |
| Juiz | veredito e referência válida | + `atalho_generico` e veredito por candidato |

## Etapas

| Etapa | Modelo padrão | Saída |
|---|---|---|
| 1. relações por bloco (reaproveitadas da v1 com `--reusar`, o padrão) | `gpt-5-4-petrobras:low` | `relacoes/` |
| 2. encadeamentos (até 40 por documento) | `gpt-5-4-petrobras:high` | `combinacoes/` |
| 3. alvos com reservas (difícil A prefere relações de mecanismo e causa) | código | `alvos.json` |
| 4. uma questão por alvo; reservas só cobrem alvos insuficientes | `gpt-5-4-petrobras:high` | `questoes/` |
| 5. EC v13 por janela e amostra na mesma composição | `gpt-5-4-petrobras:high` | `ec/`, `amostra_ec.json` |
| 6. respostas sem contexto e juiz cego em lotes embaralhados | nano 4.1, nano 5.4 low; juiz 5.4 high | `avaliacao/` |
| 7. relatório | código | `RELATORIO.md`, `resultado.json`, `questoes_avaliadas.csv` |

## Rodar

```bash
bash pipeline/qa_research/rodar_piloto_dificuldade.sh                     # piloto completo
bash pipeline/qa_research/rodar_piloto_dificuldade.sh --limite-blocos 6 --faceis 1 --medias 1 \
     --dificeis 2 --ec-janelas 2 --saida pipeline/qa_research/relatorios/teste_dificuldade
bash pipeline/qa_research/rodar_piloto_dificuldade.sh --saida <pasta>     # retoma
python -m pipeline.qa_research.inventario_docs relatorio <pasta>           # refaz o relatório
```

## Como ler o resultado

- **Gradiente**: a acurácia de R1 deve cair de fácil para difícil. Na v1 ela ficou plana (0,56 a 0,69).
- **Atalho genérico**: deve ficar perto de zero nas difíceis.
- **Filtro simulado**: acurácia de R1 nas questões que R2 errou. Se for bem menor que a geral, vale filtrar
  as difíceis com um modelo pequeno diferente do avaliado (como em Humanity's Last Exam).
- **Insuficientes por tipo**: quantos alvos o gerador recusou; mostra se o documento sustenta a rubrica.
