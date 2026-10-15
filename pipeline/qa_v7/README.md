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

## Piloto atual

Por subtópico (40 no total): uma nota gera fácil + média, outra nota gera difícil A e uma combinação gera
difícil B, totalizando 160 questões. O critério de parada definitivo ainda não foi escolhido; será estudado
num teste com 100 questões por subtópico.

`comparar_juizes.py` testa juízes diferentes sobre **as mesmas** questões (a versão original do gerador) e
sobre versões com defeito plantado (`erro_tecnico`, `sem_suporte`, `dependencia_fonte`), criadas por
modelo. Mede aprovação das originais, detecção de cada defeito, se o motivo da reprovação é o esperado,
concordância entre juízes (kappa) e tokens. As originais em que os juízes divergem ficam listadas para
o especialista decidir.

`piloto_sol_2026_10_14/` guarda o primeiro piloto (160 questões, gerador e juiz `gpt-6.1-sol`, com o
avaliador de dificuldade ainda ativo), para comparação.

## No servidor

```bash
git pull --ff-only origin dev
OUT=pipeline/qa_v7/saida_piloto_azure
mkdir -p "$OUT"
nohup bash pipeline/qa_v7/run_piloto_juizes_azure.sh > "$OUT/console.log" 2>&1 &
tail -F "$OUT/console.log"
```

`run_piloto_juizes_azure.sh geracao` ou `juizes` roda só uma das etapas. Variáveis: `QA_GERADOR`
(padrão `gpt-5-4-petrobras:low`), `QA_JUIZ` (padrão `gpt-5-2-petrobras:medium`), `QA_JUIZES` (padrão
`gpt-5-2-petrobras:medium o3-petrobras:medium gpt-5-4-petrobras:medium gpt-5-petrobras:medium`),
`QA_DEFEITOS` (32), `QA_WORKERS` (8), `QA_SOL=1` (também compara os juízes nas questões do piloto Sol),
`QA_OUTPUT`, `QA_PYTHON`. Repetir o comando reaproveita o cache.

## Saída

```text
saida_piloto_azure/
  questoes.jsonl       todas as questões: original do gerador, correções, pareceres do juiz, fatos e fontes
  aprovadas.jsonl      só as aprovadas (pergunta, resposta, nível, notas de origem)
  relatorio.md         questões por tópico e subtópico, com status e motivos
  resumo.json          contagens e tokens por papel
  juizes/relatorio_juizes.md, resumo_juizes.json, avaliacoes.jsonl, itens.jsonl
```

## Testes

```bash
python3 -m unittest discover -s pipeline/qa_v7/tests -t .
```
