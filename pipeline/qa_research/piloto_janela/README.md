# Piloto de geração por janela

Gera questões percorrendo cada bloco dos documentos de contexto (v2) como **foco**, com o bloco
anterior e o seguinte como apoio, num único prompt (`../prompt_janela_qa_10.md`) que junta
planejamento e redação. Somente geração: não há refinamento, auditoria nem descarte.

## O que o piloto faz

- Itens padrão: `01_01` (24 blocos) e `02_02` (57 blocos), ou seja, 81 janelas e 81 chamadas.
- Cada janela pede de 6 a 8 questões (`--min`, `--max`). O modelo pode entregar menos (`parcial`) ou
  nenhuma (`sem_questoes`), sempre com motivo.
- O código só confere o formato do JSON. Se estiver fora do formato, o cliente pede ao modelo a
  correção do formato, como no `qa_batch`. Nada é descartado por conteúdo.
- Métricas descritivas registradas por questão: se os fundamentos são cópias literais, se há âncora
  válida no bloco foco, se usa bloco de apoio e o tamanho da pergunta e da resposta.

## Rodar no servidor

```bash
# teste rápido: 3 janelas por item
bash pipeline/qa_research/rodar_piloto_janela.sh --limite 3

# piloto completo
bash pipeline/qa_research/rodar_piloto_janela.sh

# retomar uma execução interrompida (só gera as janelas que faltam)
bash pipeline/qa_research/rodar_piloto_janela.sh --saida pipeline/qa_research/relatorios/piloto_janela_<data>
```

Outras opções: `--modelo deployment:esforço` (padrão `gpt-5-4-petrobras:high`), `--workers` (padrão 4),
`--orientacao "Priorize média ou difícil, se o foco sustentar."`, `--anteriores <pasta>` (segunda rodada:
passa ao modelo as questões já geradas para cada foco) e `--dry-run` (grava os prompts sem chamar o modelo).

## Experimento de exemplos de forma (condições A, B, C e D)

Roda as quatro condições nas **mesmas janelas** (por padrão, 20 focos espaçados em cada item, 40 por
condição, 160 chamadas). Só muda o bloco `<exemplos_de_forma>` dos dados:

| Condição | Exemplos por chamada |
|---|---|
| A | nenhum |
| B | 3 externos, um por dificuldade, de fontes diferentes: Pirá (fácil), ARC-Challenge (média), HotpotQA (difícil) |
| C | 3 aprovadas sem ressalvas pelo especialista, uma por dificuldade, de áreas diferentes entre si e da área da janela |
| D | B + C (6 exemplos) |

A dificuldade dos exemplos não é informada ao modelo e a ordem é embaralhada. O sorteio é determinístico
por janela: B e D recebem os mesmos externos; C e D, as mesmas questões do especialista. Exige
`pipeline/qa_references/data/qa_examples.jsonl` no servidor (o script avisa como baixar, se faltar).

```bash
bash pipeline/qa_research/rodar_experimento_exemplos.sh --limite 2   # teste rápido: 16 chamadas
bash pipeline/qa_research/rodar_experimento_exemplos.sh              # experimento completo
```

Saída em `relatorios/experimento_exemplos_<data>/`: uma subpasta por condição (com `RESUMO.md` e
`QUESTOES.md`) e `COMPARACAO.md` lado a lado. A métrica nova é a semelhança lexical entre cada questão
gerada e os exemplos recebidos naquela chamada, para medir cópia.

## Experimento de modos: planejamento e redação juntos x separados

Usa a condição C (3 exemplos do especialista), 4 questões por janela com pelo menos 1 média e 1 difícil
(`--min-medias`, `--min-dificeis`), nas
mesmas 40 janelas do experimento de exemplos.

| Modo | Chamadas por janela | Prompts |
|---|---:|---|
| `junto` | 1 | `prompt_janela_qa_11.md` |
| `separado` | 2 | `prompt_janela_planejamento_qa_11.md` (escolhe alvos, sem exemplos) e `prompt_janela_redacao_qa_11.md` (redige a partir do plano, com os exemplos), como no lote 9 |

Os prompts v11 trazem a régua de dificuldade da `qa_v7`, com a resposta sempre curta (até 50 palavras):
fácil (pergunta direta, sem cenário, até 35 palavras), média (aplicar uma relação a uma condição dada,
até 60) e difícil (até 90), em duas formas: diagnóstico ou decisão num único mecanismo, ou integração de
duas relações que se explicam, mascaram ou limitam. Também proíbem perguntas que pedem listas ou o que
foi "citado".

```bash
bash pipeline/qa_research/rodar_experimento_modos.sh --limite 2   # teste rápido: 12 chamadas
bash pipeline/qa_research/rodar_experimento_modos.sh              # completo: 120 chamadas
```

A comparação (`COMPARACAO.md`) acrescenta: janelas com ao menos uma difícil, palavras da pergunta por
nível, porcentagem acima do tamanho pedido, janelas com média e com difícil e itens do plano descartados na redação.

## Levar os resultados do servidor para a sua máquina

```bash
# no servidor, ao terminar
bash pipeline/qa_research/enviar_resultados.sh pipeline/qa_research/relatorios/<pasta>
# na sua máquina
git pull
```

## Saídas (`relatorios/piloto_janela_<data>/`)

- `RESUMO.md` e `resumo.json` — métricas totais e por item: status das janelas, questões por janela,
  distribuição de dificuldade contra o alvo 50/30/20, tipos de demanda, fundamentos literais, uso dos
  apoios, quase duplicadas (Jaccard ≥ 0,6) e tokens.
- `QUESTOES.md` — leitura humana, por bloco foco.
- `questoes.jsonl` e `questoes.csv` — todas as questões com as métricas.
- `<item>/janelas/NNN.json` — registro de cada chamada. `<item>/falhas/` guarda as janelas que falharam;
  elas são tentadas de novo ao repetir a mesma `--saida`.
- `.local/` (fora do git) — cache das chamadas e respostas brutas.

Recalcular o resumo de uma pasta: `python -m pipeline.qa_research.piloto_janela resumo <pasta>`.

## Testes (offline)

```bash
python -m unittest pipeline.qa_research.tests.test_piloto_janela -v
```
