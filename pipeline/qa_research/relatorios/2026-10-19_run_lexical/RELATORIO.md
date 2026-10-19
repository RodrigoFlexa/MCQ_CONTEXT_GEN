# Relatório parcial — run lexical (Produtos químicos, `qa_research`)

Instantâneo de 2026-10-19 ~14:57 (-03). A run **ainda está em andamento**; nada aqui é resultado final.
Tópico: *2.2. Produtos químicos — Produção e Processo*. Etapa: `--stage pesquisa` (gera o documento auditado; a QA vem depois).

## Configuração
- Código: commit `5111daa` (pré-híbrido), executado a partir de um worktree separado para preservar a identidade da run (hash da implementação `4afef632…`).
- Recuperação: **lexical SQLite FTS5/BM25** sobre o índice de 2.973.683 trechos (manifesto verificado, 29 GB, fora do git).
- Modelos: `gpt-5-4-petrobras:low` em todos os papéis. Orçamento: 500 chamadas; 3 workers; 4 rodadas de pesquisa; `max_evidence` 32.
- Linha do tempo: planejamento 02:06; primeira tentativa parou ~02:20 (sem erro no log); retomada às 11:48 reaproveitando a pasta de saída.

## Situação atual
| Item | Valor |
|---|---|
| Recortes planejados / descobertos | 8 → **16** (limite `max_facets`) |
| Concluídos e auditados pelo modelo (`auditado_modelo`) | **6** (R053dfaf, R2b2c088, R5e28ba6, R880d4df, R93b3ed1, Rd4bc78f) |
| Concluídos parciais (`parcial`) | 2 (R311ca65, R32a4d85) |
| Aguardando auditoria | 2 (R78dd379, Rac09fbe) |
| Pendentes de pesquisa (`pendente_execucao`) | 5, mais 1 em andamento sem evidência |
| Capítulos publicados no `resumo.json` | 0 (o resumo só é regravado ao final da run) |
| Chamadas usadas | ~100 de 500 |

Os recortes concluídos tratam, por exemplo, de: URS × risco de BaSO₄/CaCO₃; dessulfatação + desaeração reduzindo incrustação e processos aeróbios; desaeração por membranas × scavenger de O₂; dosagem de bissulfito × O₂ dissolvido, pH e corrosão; arranjo SRU → desaerador → dosagem pós-desaerador.

## Chamadas ao modelo (98 registradas)
| Papel | Chamadas | OK | Tokens entrada | Tokens saída | Tempo de modelo |
|---|---|---|---|---|---|
| planejador | 2 | 1 | 3,2 mil | 4,1 mil | 44 s |
| pesquisador | 58 | 23 | 2,02 mi | 215 mil | 2.395 s |
| redator | 12 | **12** | 292 mil | 26,5 mil | 368 s |
| auditor | 26 | 10 | 749 mil | 114 mil | 1.147 s |
| **Total** | 98 | 46 (47%) | 3,07 mi | 360 mil | 3.954 s (~66 min) |

## O que está dando certo
- **Redator: 12/12 chamadas válidas.** A redação a partir das evidências aprovadas não é o gargalo.
- **A pesquisa descobre recortes úteis:** o plano cresceu de 8 para 16 recortes com âncoras literais, e os recortes concluídos têm 24–32 evidências (alguns, 5).
- **O reparo funciona:** 45 chamadas foram retentativas com `reparo=true`; sem elas haveria muito mais recortes perdidos.
- **Retomada confiável:** a identidade (config + implementação + corpus) permitiu retomar a pasta antiga sem refazer o plano; o orçamento persistente contou as tentativas corretamente.
- **A integridade é preservada:** nenhum filtro foi afrouxado; recortes sem citação literal válida ficam `pendente_execucao` em vez de entrarem no documento.

## Problemas e insights
1. **Taxa de falha alta (52/98)**, concentrada em pesquisador (35/58) e auditor (16/26). Os 7 erros terminais em `eventos.jsonl` são validações de suporte: *"citação não é trecho contíguo original de E…"* (6) e *"evidência não citada pelo bloco"* (1). O modelo parafraseia em vez de copiar literalmente.
2. **O gargalo de tempo não é o modelo.** O modelo gastou ~66 min no total; o restante da retomada (~3 h) é busca BM25 no índice de 29 GB e I/O, com pausas de 10–20 min entre chamadas. Trocar por um modelo menor (nano) não resolve e provavelmente pioraria a citação literal.
3. **Contexto grande:** o pesquisador usa ~35 mil tokens de entrada por chamada e produz ~3,7 mil; cada falha desperdiça uma chamada cara.
4. **Consultas FTS5 com até 40 termos ligados por `OR`** retornam muitos candidatos a ordenar por BM25 — suspeita principal da lentidão; falta perfilar.
5. **A primeira tentativa parou sem erro no log** (~02:20); causa não determinada. A retomada só foi possível porque o código antigo foi preservado num worktree: o código novo invalidaria a identidade (`implementation`).
6. **Ao reutilizar a saída em outro worktree** é preciso fixar `origins` com caminhos absolutos e disponibilizar `.env`, o CA bundle `petrobras-ca-root.pem` e o índice via symlink.

## Possíveis ações
- Perfilar a busca FTS5 (limitar termos e candidatos) para reduzir as pausas.
- Reduzir `max_evidence`/contexto do pesquisador para diminuir citações erradas.
- Manter `gpt-5-4` em pesquisador, redator e auditor; usar nano só em papéis de baixo risco (ex.: `novidade`).
- Registrar o motivo de cada falha em `chamadas_llm.jsonl`; hoje só consta `ok=false`.

## Run híbrida em paralelo (fora deste resultado)
Geração de embeddings (text-embedding-3-large) dos 2,97 mi de trechos, com retomada por cache (`vectors.sqlite3`) e reinício automático. Progresso: ~12,7% às 14:52, ~31 trechos/s, ~23 h restantes. Uma paralelização com 24 workers foi revertida a pedido; o ritmo é limitado pela cota do Azure.
Mudança no config: `embedding_max_calls` 50.000 → 200.000 em `configs/produtos_quimicos.json` (não altera a identidade da run).

## Arquivos neste diretório
`plano.json`, `eventos.jsonl`, `chamadas_llm.jsonl`, `orcamento.json`, `execucao.json`, `config.json`, `recortes/` (estado de cada recorte), `console_*.log`.
O documento final (`documento_auditado.md`) ainda não existe; índices (29 GB) e vetores ficam fora do git.
