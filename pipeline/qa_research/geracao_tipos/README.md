# Geração híbrida por tipo de questão

Tipos, marcas e composição: [`../TIPOS_QUESTAO.md`](../TIPOS_QUESTAO.md).

## Etapas

| Etapa | Modelo padrão | Saída |
|---|---|---|
| 0. reclassificar por tipo as 199 questões avaliadas no piloto v2 e cruzar com a acurácia | `gpt-5-4-petrobras:high` | `reclassificacao/` |
| 1. janelas (prompt v14, exemplos E+C): todas do 01_01 e 36 do 02_02, 4 questões cada | `gpt-5-4-petrobras:high` | `janelas/<item>/<foco>.json` |
| 2. compostas: uma por encadeamento do piloto v2 (32 por documento) | `gpt-5-4-petrobras:high` | `compostas/` |
| 3. auditoria: tipo confere, referência válida, atalho | `gpt-5-4-petrobras:high` | `auditoria/` |
| 4. relatório | código | `RELATORIO.md`, `resultado.json`, `questoes.jsonl`, `questoes.csv` |

Cerca de 60 chamadas de janela, 64 de compostas, ~30 de auditoria e ~20 de reclassificação.

## Rodar

```bash
bash pipeline/qa_research/rodar_geracao_tipos.sh                                   # completo
bash pipeline/qa_research/rodar_geracao_tipos.sh --ec-janelas 2 --limite-compostas 2 \
     --etapas janelas compostas auditoria relatorio --saida pipeline/qa_research/relatorios/teste_tipos
bash pipeline/qa_research/rodar_geracao_tipos.sh --saida <pasta>                    # retoma
python -m pipeline.qa_research.geracao_tipos relatorio <pasta>                        # refaz o relatório
```

## Como ler

- Janelas `parcial`: quais grupos o bloco não sustentou (esperado em blocos de gestão para `diagnostico`).
- `tipo confere`: se o auditor concorda com o tipo; divergências frequentes indicam tipos mal definidos.
- Referência inválida e atalho por tipo: onde a qualidade ainda falha.
- Reclassificação: acurácia de R1 e R2 por tipo nas questões antigas, e se respostas com dado específico
  (nome, local, parâmetro, prática) são mais erradas que as gerais.
