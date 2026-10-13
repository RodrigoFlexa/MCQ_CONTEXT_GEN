# Inventário v4: notas técnicas por conceito

A v3 guardava **frases soltas** (mediana de 30 palavras, 4,4 por trecho) e o "documento" era uma lista delas.
A v4 guarda **notas técnicas**: explicações de 250 a 750 palavras por conceito, com mecanismo, variáveis,
problemas e diagnóstico, decisões e valores, cada seção ligada aos fatos (com citação literal) que a sustentam,
mais os conhecimentos avaliáveis por nível de dificuldade. É o material de que o gerador de QA precisa.

## Fluxo

```text
frase do especialista ─► assuntos (texto literal)                                   1 chamada/subtópico
corpora (5 coleções)  ─► varredura lexical pt+en                                     CPU, reaproveitável
                      ─► seleção: consulta pt E en (vale a maior), piso de relevância,
                         cota mínima por coleção (HSE/BSEE/ANP entram), teto por documento, MMR
trechos               ─► FATOS: afirmação de 1-3 frases + condições + citação literal  1 chamada/trecho
fatos do assunto      ─► CONCEITOS: agrupa fatos de várias fontes, descarta o que não
                         pertence ao assunto                                         1 chamada/assunto
conceito              ─► REDATOR: nota técnica com seções fundamentadas (F#/T#) e, se
                         preciso, conhecimento de engenharia consagrado MARCADO        1 chamada/conceito
                      ─► REVISOR: aprovar | corrigir (devolve a nota final) | rejeitar,
                         com notas 1-5 de correção, suporte, pertinência e riqueza      1 chamada/conceito
notas aprovadas       ─► deduplicação
                      ─► COMBINAÇÕES: pares/trios de notas do subtópico cujos conceitos
                         interagem numa situação real (base das difíceis tipo B)      1 chamada/subtópico
                      ─► documento por subtópico e por tópico
```

Aceitação de uma nota: revisor não rejeitou; correção técnica ≥ 4; suporte, pertinência e riqueza ≥ 3;
pelo menos 2 seções fundamentadas em fatos; ≥ 120 palavras; conhecimento geral ≤ 50% do texto.
Seções que ficarem sem fato depois da revisão são removidas automaticamente.

## Níveis de dificuldade

- **fácil**: pergunta direta sobre conceito, função ou efeito de uma nota.
- **média**: aplicar causa e efeito, variável ou critério de uma nota a uma condição dada.
- **difícil A** (uma nota): cenário operacional; diagnosticar ou decidir dentro de um conceito.
- **difícil B** (combinação): cenário em que 2 ou 3 conceitos interagem; usa `combinacoes.jsonl`
  (notas, ligação, raciocínio exigido, esboço de cenário, o que cada nota contribui).

O nível medido vem do avaliador da fase 4 (`pipeline/fase_4/difficulty.py`, 4 dimensões de 1 a 3),
que não recebe o nível pedido. Para medir num inventário pronto:

```bash
python -u pipeline/inventario/teste_dificeis.py --inventario pipeline/inventario/saida_producao_v4_notas \
    --por-tipo 8 --controles 4
```

Saída em `<inventario>/teste_dificeis/`: `questoes.jsonl`, `relatorio.md`, `resumo.json`.

## Robustez

| Situação | Comportamento |
|---|---|
| Filtro de conteúdo da Azure (prompt ou resposta) | sem nova tentativa; item registrado em `ocorrencias.jsonl` (`filtro_conteudo`); **a execução continua** |
| JSON inválido ou fora do formato | nova tentativa devolvendo o erro ao modelo (reparo) |
| Resposta truncada | nova tentativa com 1,6× mais tokens (até 32 mil) |
| 429, 5xx, timeout, conexão | espera (respeita Retry-After) e repete |
| 400 comum (ex.: contexto longo) | registra e pula o item |
| Fato inválido dentro de uma resposta boa | só aquele fato é descartado (motivo em `fatos_descartados.jsonl`) |
| 401/403/404 (credencial, deployment) | interrompe: é configuração |
| 20 falhas seguidas (`--max-falhas-consecutivas`) | interrompe: serviço indisponível; `resumo.json` com status `interrompido` |

Toda tentativa fica em `chamadas_llm.jsonl` com a mensagem do erro. Repetir o mesmo comando reprocessa
apenas o que faltou: tudo o que já foi obtido vem do cache. Assuntos afetados por falha aparecem como
`incompleto` (modo `reprocessar`), nunca como "sem contexto".

## No servidor

```bash
git pull --ff-only origin dev
python3 -m pip install -r pipeline/inventario/requirements_azure.txt

bash pipeline/inventario/run_producao_azure.sh --plan        # lista 12 subtópicos, sem chamadas
bash pipeline/inventario/run_producao_azure.sh --check-api   # 1 pedido LLM + 1 de embeddings

mkdir -p pipeline/inventario/saida_producao_v4_notas
nohup bash pipeline/inventario/run_producao_azure.sh \
  > pipeline/inventario/saida_producao_v4_notas/console.log 2>&1 &
tail -F pipeline/inventario/saida_producao_v4_notas/console.log
```

O script reaproveita automaticamente, se existir, `saida_producao_v3_correcao_azure`: assuntos, índice lexical
e vetores de embeddings (a varredura de ~45 min e a vetorização não se repetem). Nada do LLM antigo é reutilizado.
Variáveis: `INV_OUTPUT`, `INV_REUSE`, `INV_WORKERS` (padrão 8), `INV_MAX_CHAMADAS`, `INV_PYTHON`, `INV_MANIFEST`.

Piloto curto antes da rodada inteira (2 assuntos por subtópico):

```bash
INV_OUTPUT=pipeline/inventario/saida_producao_v4_piloto \
  bash pipeline/inventario/run_producao_azure.sh --limite-assuntos 2
```

Estimativa para Produção e Processo (186 assuntos): ~2.100 chamadas de fatos, 186 de conceitos e ~1.500 de
notas (redator + revisor). Com 8 workers, algumas horas; o limite real é a cota de tokens por minuto do deployment.

Um tópico qualquer (o nome pode ser parcial; a saída padrão é `saida_<tópico>_v4_notas`):

```bash
bash pipeline/inventario/run_topico_azure.sh "Sistemas de Lastro" --plan
mkdir -p pipeline/inventario/saida_sistemas_de_lastro_v4_notas
nohup bash pipeline/inventario/run_topico_azure.sh "Sistemas de Lastro" \
  > pipeline/inventario/saida_sistemas_de_lastro_v4_notas/console.log 2>&1 &
```

Para um tópico novo a varredura lexical é refeita (os assuntos mudam); vetores já calculados vêm do cache.

## Saída

```text
saida_producao_v4_notas/
  resumo.json, execucao.log, ocorrencias.jsonl, chamadas_llm.jsonl
  cobertura.md / cobertura.csv            por assunto: com_contexto | sem_contexto | incompleto | generico
  notas_aprovadas.jsonl                   todas as notas aprovadas (entrada do gerador de QA)
  assuntos_para_geracao.jsonl             assunto -> modo_geracao e ids das notas
  combinacoes.jsonl                       todas as combinações (cid, notas, ligação, raciocínio, cenário)
  topicos/*/documento_tecnico.md          documento legível do tópico
  subtopicos/<subtópico>/
    documento.md, README.md
    assuntos.json, selecao.json
    fatos.jsonl, fatos_descartados.jsonl
    conceitos.json                        plano por assunto (fatos agrupados e descartados com motivo)
    combinacoes.json                      mapa de combinações do subtópico (e as descartadas, com motivo)
    notas.jsonl                           todas as notas: aprovadas, reprovadas (com motivos), insuficientes,
                                          duplicadas, falhas; inclui rascunho, revisão, alertas e fontes
```

Cada nota em `notas_aprovadas.jsonl` traz: `titulo`, `resumo`, `secoes` (tipo, texto, fatos,
conhecimento_geral), `alvos` (facil/media/dificil), `fontes` (citação literal e proveniência de cada fato),
`avaliacao` do revisor, `assuntos` e o texto do assunto do especialista.

## Validação feita

- 69 testes offline (combinações, filtro de conteúdo, reparo, truncamento, disjuntor, salvamento parcial, cotas por coleção,
  normalização numérica, notas, revisão, deduplicação, documentos, CLI completa e retomada).
- Execução real (gpt-6-luna) em trechos reais de Separadores Trifásicos e Flare: 15 notas aprovadas de 277 a
  728 palavras, sem falhas. Piso de cosseno calibrado com text-embedding-3-large: trechos relevantes 0,60-0,74,
  trechos de outro subtópico do mesmo domínio até ~0,69. Na Azure ainda falta medir com o gpt-5-4-petrobras.
