# QA v7: perguntas a partir do inventário

A geração usa as notas técnicas aprovadas do inventário (`pipeline/inventario/saida_*`) como contexto.
Não há busca nos corpora nem composição de documentos: cada nota já traz seções revisadas, fatos `F#` com
citação literal e uma lista de alvos (fácil, média, difícil). As combinações de notas alimentam o difícil B.

```text
nota ou combinação ─► GERADOR (1 chamada por lote, 1 pergunta por alvo, cita os F# usados)
                   ─► verificação em código (autonomia, alternativas, tamanho, F# existentes)
                   ─► JUIZ (correção, suporte por afirmação, autonomia, escopo, jurisdição,
                      generalização, tipo) ─► no máximo 1 correção se for reparável ─► juiz de novo
                   ─► aprovada | reprovada (com motivos)
```

- O nível de cada questão é o **tipo pedido ao gerador** (`facil`, `media`, `dificil_A`, `dificil_B`).
  O avaliador de dificuldade da fase 4 ficou fora do loop.
- Exemplos no prompt: 3 aprovados pelo especialista (de outros tópicos) e 3 de benchmarks públicos
  escolhidos pelo tipo (ARC Easy/Challenge e Pirá filtrado para fácil e média; HotpotQA para difícil B).
- Modelos por papel: `--gerador deployment:effort` e `--juiz deployment:effort`. `o3-petrobras` e
  `o4-mini-petrobras` usam automaticamente a API version `2025-01-01-preview`.
- Robustez herdada do inventário: cache, filtro de conteúdo da Azure (o lote é pulado e registrado),
  reparo de JSON, saldo/cota esgotados encerram sem insistir. Um lote com falha não derruba os demais.

## Modos

- `--modo piloto`: 4 perguntas por subtópico (uma nota dá fácil + média, outra dá difícil A, uma combinação dá
  difícil B). Usado para comparar juízes.
- `--modo cota --por-topico 100`: 100 perguntas **aprovadas** por tópico. A cota de cada subtópico é proporcional
  ao número de notas aprovadas, com piso de 3. Reprovadas são repostas com os próximos alvos da fila (até 3 ondas).
- `--modo profundo --subtopicos ...`: consome **todos** os alvos dos subtópicos indicados (estudo de parada).

**Fila de alvos** (`plano.py`): cada nota traz de 4 a 8 alvos (conhecimentos avaliáveis com nível). A fila de um
subtópico reveza níveis (3 fácil : 4 média : 2 difícil A : 1 difícil B), assuntos e notas: uma nota só recebe a
segunda pergunta depois que todas as notas com alvo naquele nível receberam a primeira. Cada alvo vira no máximo
uma pergunta (aprovada ou não) e sai da fila; cada combinação de notas vira uma difícil B. A fila é determinística.

**Novidade** (`novidade.py`, observacional, não filtra): para cada aprovada, na ordem da fila, o cosseno do
embedding (`embedding-3-large-global`) com as aprovadas anteriores do subtópico; quando passa de 0,70, o
`gpt-5-4-nano-petrobras` diz se os pares são redundantes, sobrepostos ou distintos. `novidade.json` traz a curva
por subtópico e a fração de redundantes por janela de 20 aprovadas, base para escolher o critério de parada.

`comparar_juizes.py` testa juízes diferentes sobre **as mesmas** questões (a versão original do gerador) e
sobre versões com um defeito sutil plantado (`erro_tecnico`, `sem_suporte`, `dependencia_fonte`,
`caso_na_resposta`). `piloto_sol_2026_10_14/` guarda o primeiro piloto (gpt-6.1-sol).

### Histórico dos pilotos

- `saida_piloto_azure`: juiz GPT-5.2 aprovou 61%. Na comparação, GPT-5.2 aprovou só 34% das originais (rigor
  excessivo em suporte); o3 e GPT-5 deixaram passar 66% e 47% das perguntas dependentes de fonte.
- `saida_piloto_azure_v2`: regras novas de suporte, resposta enxuta e sem caso específico; aprovação 82%.
  GPT-5.4 low e medium equivalentes (aprovam 81-82%, pegam 88-85% dos defeitos sutis); GPT-5.2 aprova 68%.
  Escolhido GPT-5.4 low como juiz.

## No servidor

```bash
git pull --ff-only origin dev
nohup bash pipeline/qa_v7/run_qa_v7_azure.sh ambos > pipeline/qa_v7/console_qa_v7.log 2>&1 &
tail -F pipeline/qa_v7/console_qa_v7.log
```

`cota` ou `profundo` rodam só uma etapa. Variáveis: `QA_WORKERS` (8), `QA_GERADOR`, `QA_JUIZ`
(`gpt-5-4-petrobras:low`), `QA_POR_TOPICO` (100), `QA_PROFUNDOS` (nomes separados por `|`), `QA_SAIDA_COTA`,
`QA_SAIDA_PROFUNDO`, `QA_PYTHON`. Repetir o comando reaproveita o cache. O piloto de juízes continua em
`run_piloto_juizes_azure.sh`.

## Saída

```text
saida_cota_100_por_topico/  (e saida_profundo_3_subtopicos/)
  questoes.jsonl       todas as questões: ordem na fila, original do gerador, correções, juiz, fatos, novidade
  aprovadas.jsonl      só as aprovadas (pergunta, resposta, nível, notas de origem)
  relatorio.md         questões por tópico e subtópico, com status e motivos
  resumo.json          contagens, aprovadas por tópico, redundantes e tokens por papel
  novidade.json        curva de novidade por subtópico e janelas de 20
  cota.json            cota de cada subtópico (modo cota)
```

## Testes

```bash
python3 -m unittest discover -s pipeline/qa_v7/tests -t .
```
