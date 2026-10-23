# Piloto: inventário leve (estilo qa_v7) x configuração EC

Pergunta do piloto: gerar a partir de notas técnicas (relações e combinações de relações, como no `qa_v7`)
produz questões realmente mais difíceis do que a configuração atual (janela de 3 blocos, exemplos E+C,
composição 1 fácil, 2 médias, 1 difícil)? A medida é a acurácia de um modelo pequeno respondendo sem
contexto, julgada por um modelo forte. Se a dificuldade for real, a acurácia cai de fácil para difícil.

## Etapas

| Etapa | Modelo padrão | Saída |
|---|---|---|
| 1. relações por bloco (0 a 8, com trecho literal verificado em código) | `gpt-5-4-petrobras:low` | `relacoes/<item>/<bloco>.json` |
| 2. combinações de 2 ou 3 relações de blocos diferentes (até 15 por documento) | `gpt-5-4-petrobras:high` | `combinacoes/<item>.json` |
| 3. alvos: 25% fáceis, 50% médias, 12,5% difíceis A, 12,5% difíceis B, espalhados pelos blocos, sem repetir relação | (código) | `alvos.json` |
| 4. uma questão por alvo, com os exemplos EC no prompt | `gpt-5-4-petrobras:high` | `questoes/*.json` |
| 5. amostra de 100 questões EC na mesma proporção de níveis e documentos | (código) | `amostra_ec.json` |
| 6a. respondente sem contexto | `gpt-4-1-nano-petrobras` | `avaliacao/respostas/` |
| 6b. juiz contra a referência, em lotes embaralhados, sem ver método nem nível | `gpt-5-4-petrobras:high` | `avaliacao/juiz/` |
| 7. relatório | (código) | `RELATORIO.md`, `resultado.json`, `questoes_avaliadas.csv` |

Difícil A: diagnóstico ou decisão num único mecanismo, com explicação concorrente descartada por uma
condição do enunciado. Difícil B: duas ou três relações que interagem (a combinação).

O juiz também marca `referencia_valida = false` quando a pergunta é ambígua, entrega a resposta ou a
referência está errada; o relatório mostra a acurácia com e sem esses itens.

## Rodar

```bash
bash pipeline/qa_research/rodar_piloto_inventario.sh                                  # piloto completo
bash pipeline/qa_research/rodar_piloto_inventario.sh --limite-blocos 6 --total 8 \
     --saida pipeline/qa_research/relatorios/teste_inventario                         # teste barato
bash pipeline/qa_research/rodar_piloto_inventario.sh --saida <pasta>                  # retoma
python -m pipeline.qa_research.inventario_docs relatorio <pasta>                       # refaz o relatório
```

Opções úteis: `--modelo-respondente`, `--modelo-juiz` (e os demais papéis), `--sem-exemplos`,
`--combinacoes N`, `--ec <questoes.jsonl>` (padrão: o experimento_externos mais recente).
