# Geração híbrida por tipo de questão

Tipos, marcas e composição: [`../TIPOS_QUESTAO.md`](../TIPOS_QUESTAO.md).

## Etapas

| Etapa | Modelo padrão | Saída |
|---|---|---|
| 1. janelas (prompt v15, exemplos e contraexemplos de `exemplos.json`): todas do 01_01 e 36 do 02_02, até 4 questões cada | `gpt-5-4-petrobras:high` | `janelas/<item>/<foco>.json` |
| 2. compostas: uma por encadeamento do piloto v2 (32 por documento) | `gpt-5-4-petrobras:high` | `compostas/` |
| 3. auditoria (filtro): tipo confere, referência válida, atalho | `gpt-5-4-petrobras:high` | `auditoria/` |
| 4. relatório e banco filtrado | código | `RELATORIO.md`, `resultado.json`, `questoes.jsonl`, `aprovadas.jsonl`, `questoes.csv` |
| (opcional) `--etapas reclassificar ...`: tipos das questões do piloto v2 x acurácia | `gpt-5-4-petrobras:high` | `reclassificacao/` |

Cerca de 60 chamadas de janela, 64 de compostas e ~30 de auditoria. Sem datasets externos.

## Rodar

```bash
bash pipeline/qa_research/rodar_geracao_tipos.sh                                   # completo
bash pipeline/qa_research/rodar_geracao_tipos.sh --ec-janelas 2 --limite-compostas 2 \
     --saida pipeline/qa_research/relatorios/teste_tipos
bash pipeline/qa_research/rodar_geracao_tipos.sh --saida <pasta>                    # retoma
python -m pipeline.qa_research.geracao_tipos relatorio <pasta>                        # refaz o relatório
```

## Como ler

- Janelas `parcial`: quais grupos o bloco não sustentou (esperado em blocos de gestão para `diagnostico`).
- `tipo confere`: se o auditor concorda com o tipo; divergências frequentes indicam tipos mal definidos.
- Referência inválida e atalho por tipo: onde a qualidade ainda falha.
- Reclassificação: acurácia de R1 e R2 por tipo nas questões antigas, e se respostas com dado específico
  (nome, local, parâmetro, prática) são mais erradas que as gerais.
