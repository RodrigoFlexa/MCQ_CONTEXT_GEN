# Tipos de questão (23/10/2026)

Substituem os rótulos fácil, média e difícil. Os pilotos de dificuldade
(`relatorios/piloto_inventario_20261023T042252Z` e `relatorios/piloto_dificuldade_20261023T053615Z`)
mostraram que esses rótulos mediam habilidades diferentes (conceito, aplicação, diagnóstico) e não
previam o acerto dos modelos. A dificuldade, quando for necessária, será medida depois, por um painel
de modelos.

## Os seis tipos

O tipo é definido pelo que a pergunta pede e pela forma da resposta. Nos três tipos causais, o que os
distingue é a direção do raciocínio.

| Tipo | A pergunta pede | Forma da resposta | Regras em código (`tipos.py`) |
|---|---|---|---|
| `conceito` | o que é, para que serve, qual componente, parâmetro ou local | termo, função ou entidade única | sem cenário; até 35 palavras; sem "que aspectos/quais fatores/além de X" |
| `mecanismo` | dados causa e efeito, o elo entre eles | processo causal | regras gerais |
| `consequencia` | dada uma condição ou mudança, o efeito (causa → efeito) | efeito com direção ou variável afetada | regras gerais |
| `diagnostico` | dados os sinais, a causa (efeito → causa) | causa específica | exige cenário |
| `decisao` | dada a situação, a ação, prioridade ou critério | ação ou critério específico | exige cenário |
| `procedimento` | como executar, monitorar, testar ou verificar | método, etapa, ponto ou medida | regras gerais |

Regras gerais, para todos os tipos: pergunta aberta (sem sim/não, sem escolha entre opções dadas, sem
"conclusão correta sobre a decisão"); enunciado com observações, não interpretações; termo decisivo
fora do enunciado; enunciado até 90 palavras; resposta começando pelo elemento decisivo, até 30
palavras; nenhum caractere fora do português.

## Marcas

- `cenario`: o enunciado apresenta uma situação operacional (`true`) ou é pergunta direta (`false`).
- `composicao`: `simples` (uma relação, geração por janela) ou `composta` (duas ou três relações de
  blocos diferentes, geração a partir dos encadeamentos do inventário).

## Composição

- Por janela (prompt `prompt_janela_qa_15.md`): até 4 questões, 1 `conceito`, 1 `mecanismo` ou
  `consequencia`, 1 `diagnostico`, `decisao` ou `procedimento`, e 1 livre que não pode ser outro
  conceito. Duas ou três boas valem mais que quatro com uma fraca: se o bloco foco não sustentar um
  grupo, a janela sai `parcial`, com o motivo.
- Compostas: uma por encadeamento; qualquer tipo menos `conceito`.

## Método híbrido

| Parte | O que gera | Por quê |
|---|---|---|
| Janela (v15) | questões simples, até 4 por chamada | barata (0,25 chamada por questão) e de qualidade equivalente ao inventário nas questões de uma relação |
| Encadeamentos do inventário | questões compostas | a janela só vê 3 blocos vizinhos e quase não usa os de apoio; os encadeamentos ligam blocos distantes |

## Versão 15 (23/10/2026)

Mudanças depois do teste `relatorios/geracao_tipos_20261023T171137Z` (42% das questões de janela e 58%
das compostas aprovadas pelo auditor):

- **Sem datasets externos.** No lugar, um banco curado (`geracao_tipos/exemplos.json`) com uma questão
  aprovada por tipo (e três compostas), cada uma com o motivo de ser boa, e oito contraexemplos reais com
  o problema de cada um. A janela recebe exemplos de outro documento, para não induzir cópia.
- **Auditoria como filtro**: `aprovadas.jsonl` guarda só as questões com referência válida e sem atalho;
  quando o auditor discorda do tipo, vale o tipo dele (o declarado fica em `tipo_declarado`).
- **Regras mais duras por tipo**, no prompt e em código:
  - conceito com resposta única no domínio, sem "que tipo de" e sem perguntar o que é citado;
  - consequência que não saia da definição dos termos;
  - decisão com ação técnica específica, sem heurística e sem comparar dois itens pelos atributos para
    perguntar qual priorizar; quando o bloco não sustenta uma ação específica, preferir procedimento ou
    diagnóstico (decisão e diagnóstico saem melhor nas compostas);
  - procedimento específico do sistema, não recomendação genérica.
- **Vaga livre sem conceito** e incentivo explícito a `parcial` em blocos de gestão ou introdutórios.

## Versão 16 (23/10/2026): geração por meta

Resultado da v15 (`relatorios/geracao_tipos_20261023T183239Z`): 52% das questões de janela e 62% das
compostas aprovadas; decisão na janela ainda em 25% (nas compostas, 55%); o modelo nunca entrega
`parcial`, então a qualidade fica com o filtro da auditoria.

- **Decisão sai da janela.** Grupos da janela: 1 `conceito`; 1 `mecanismo` ou `consequencia`; 1
  `diagnostico` ou `procedimento`; 1 livre entre mecanismo, consequência, diagnóstico e procedimento.
  Decisão só nas compostas. Conceito também não pode pedir sigla nem elemento trivial de fórmula.
- **Meta por tópico** (`python -m pipeline.qa_research.geracao_tipos meta`, script
  `rodar_geracao_meta.sh`): para cada tópico, inventário (relações e encadeamentos), compostas, e
  rodadas de janela até atingir N questões aprovadas (padrão 100). A 1ª rodada passa por todas as
  janelas; as seguintes voltam às mais produtivas, com as questões já geradas ali em
  `<questoes_existentes>`, no máximo 3 vezes por janela e 4 rodadas. Quase duplicatas no tópico
  (Jaccard ≥ 0,6) não contam.
- **Banco dinâmico ("ad hoc").** Depois de cada auditoria, as aprovadas viram exemplos e as reprovadas
  viram contraexemplos (com a justificativa do auditor) para as chamadas seguintes, sempre de outros
  tópicos. Cada chamada recebe um exemplo por tipo, 5 contraexemplos do banco curado e 3 reprovações
  recentes. No fim, `exemplos_proposto.json` sugere a atualização do banco curado, para revisão.

## Versão 17 (24/10/2026): geração completa sem meta

- **Sem meta obrigatória**: cada tópico passa uma vez por todas as janelas e por todos os encadeamentos;
  gera o que o documento sustenta. A meta (`--meta N`) continua disponível como opção.
- **Ondas de 5 tópicos**: compostas, janelas e auditoria por onda; o banco dinâmico (aprovadas como
  exemplos, reprovadas como contraexemplos) é atualizado entre uma onda e outra, e começa com o banco
  herdado da v16.
- O sinal que descarta a alternativa não pode resolver a questão por exclusão (janela e compostas);
  encadeamentos limitados a 25 por documento; filtro de conteúdo do Azure vira insuficiente;
  deduplicação também por resposta curta; "citado/mencionado como" barrado.

## Versão 18 (24/10/2026): prompt, auditor e refinador mais rigorosos

Motivo: numa amostra de 30 aprovadas da v16, só ~27% eram boas e ~37% eram fracas (caso específico como
"no FPSO Frade", respostas vagas, listas genéricas, respostas que só resumem o enunciado). As 13 fracas
identificadas foram retiradas das aprovadas da v16 (`remocoes_manuais.json`) e viraram contraexemplos.

- **Prompt v18** (`prompt_janela_qa_18.md`) e compostas: seção "Defeitos que reprovam a questão" (caso
  específico, resposta vaga, lista genérica, reformula o enunciado, várias respostas, prudência genérica,
  trivial, sim ou não disfarçado) e autoverificação: um profissional que não leu o documento responderia
  com segurança e chegaria à mesma resposta? a resposta sai por bom senso? só repete o enunciado?
- **Código** (`tipos.py`): barra unidade, campo ou bacia com nome próprio ("FPSO Frade", "P-50",
  "Bacia de Campos") e respostas vagas ("tende a se alterar", "potencialmente", "depende de").
- **Auditor v2** (`prompts/auditoria_v2.md`): mais exigente ("na dúvida, reprove") e com motivo em
  categoria fixa; só `motivo = nenhum` é aprovado.
- **Refinador** (`prompts/refinador.md`, gpt-5-mini): reescreve uma vez as reprovadas por motivo
  recuperável (caso específico, resposta vaga, lista genérica, reformula o enunciado, várias respostas),
  usando o texto do bloco; a versão refinada passa pelo código e pelo auditor de novo.
- **Contraexemplos com "como poderia ser"**: o banco curado tem 4 contraexemplos com a versão corrigida
  (incluindo o do FPSO Frade), sempre presentes no prompt; no banco dinâmico, quando a versão refinada é
  aprovada, ela vira o "como poderia ser" da original.
- **Teste** (`rodar_teste_v18.sh`): reauditoria das aprovadas da v16 com o auditor v2 e geração completa
  em 2 documentos novos (05_01 e 06_01), esperando ~100 questões válidas.

## Versão 19 (24/10/2026): refinador com exemplos, auditor calibrado, deduplicação por sentido

Teste v18 (`relatorios/teste_v18_20261024T043655Z`): 142 válidas em 05_01 e 06_01; na revisão manual,
~33% boas, ~33% aceitáveis, ~33% fracas; o refinador recuperou 15 de 63 (24%), mas consertava um defeito
e criava outro (sobretudo "várias respostas") e chegou a inventar uma fórmula aprovada pelo auditor.

- **Refinador** (`prompts/refinador.md`): exemplos de antes e depois para cada motivo (caso específico,
  resposta vaga, reformula o enunciado, várias respostas, lista genérica), exemplos de descarte (fato
  inventado, caso sem princípio, mudança só cosmética) e autoverificação antes de responder.
- **Auditor v3** (`prompts/auditoria_v3.md`): calibração com questões reais aprovadas por engano e com
  exemplos de aprovação correta; nas refinadas recebe o texto-fonte e reprova com `fora_da_fonte` o que
  acrescentar fato, valor, fórmula ou mecanismo que o texto não sustente.
- **Deduplicação por sentido** (`prompts/dedup.md`): no fim de cada tópico, uma chamada ao modelo forte
  agrupa as aprovadas que avaliam o mesmo conhecimento e mantém a melhor.
- **Banco herdado limpo**: as 416 aprovadas da v16 reprovadas pelo auditor v2 viraram contraexemplos
  (`banco_dinamico_auditor_v2.json`); as 10 fracas da amostra do teste v18 foram retiradas
  (`remocoes_manuais.json`).
- **Piloto** (`rodar_teste_v19.sh`): reauditoria das aprovadas do teste v18 com o auditor v3 e geração
  completa em 2 documentos novos (07_03 manutenção, 03_03 tanques de carga e estabilidade).

## Versão 20 (24/10/2026): ajustes do piloto v19, pronta para a geração final

Piloto v19 (`relatorios/teste_v19_20261024T053346Z`): 104 válidas em 07_03 e 03_03. Na primeira auditoria,
40% das questões de janela foram aprovadas (88/220); a deduplicação por sentido retirou 50 aprovadas (os
grupos conferidos eram do mesmo conhecimento em cenários diferentes). O auditor v3 com o texto-fonte
funcionou: nenhuma refinada aprovada tem fato inventado (9 foram barradas por `fora_da_fonte`). Na revisão
manual (amostra de 30), ~27% boas, ~43% aceitáveis e ~30% fracas; os defeitos mudaram: quase não há caso
específico nem resposta vaga, e as fracas são enunciados que entregam a resposta ou a resolvem por eliminação
e, nas refinadas, artefatos do refinador. As 13 fracas identificadas foram retiradas
(`geracao/remocoes_manuais.json`, 92 válidas) e viraram contraexemplos.

- **Referência à fonte barrada em código** (`tipos.py`): "nos blocos", "no texto", "no documento", "segundo o
  texto" e "único sob essas condições" (o refinador chegou a escrever "técnica descrita nos blocos").
- **Refinador**: mudança só cosmética é recusada em código (pergunta com Jaccard ≥ 0,8 e resposta ≥ 0,6 em
  relação à original); o exemplo de "várias respostas" agora acrescenta um sinal positivo que separa a causa
  certa, e não uma lista de condições descartadas (o exemplo antigo ensinava a resolver por eliminação, no
  máximo uma ou duas condições de descarte); descarte quando a única saída é pôr a pista no enunciado.
- **Auditor v3**: `reformula_enunciado` também cobre a questão resolvida por eliminação; três novos exemplos
  de calibração (válvula que só abre ou fecha descrita no enunciado, lista de causas descartadas, referência
  aos blocos).
- **Herança**: inventário e banco dinâmico do piloto v19 entram em `REUSAR` e `BANCO_INICIAL`.

## Experimento de refino (24/10/2026): refinador forte x fraco

Pergunta: um refinador forte, com o motivo da reprovação, os blocos e exemplos aprovados, recupera reprovadas
suficientes para aumentar a taxa de válidas? O experimento (`refino_forte.py`, script `rodar_teste_refino.sh`)
parte do piloto v19, sem gerar nada novo: as 153 originais reprovadas pelo auditor (todos os motivos, não só os
recuperáveis) passam por dois braços com o mesmo prompt (`prompts/refinador_v3.md`):

- `mini`: gpt-5-mini-petrobras:medium; `forte`: gpt-5-4-petrobras:high.
- Prompt v3: exemplos de correção também para trivial, prudência genérica, sim ou não disfarçado,
  tecnicamente errada e fora da fonte; pode mudar o tipo; recebe dois exemplos aprovados do mesmo tipo (de outros
  tópicos) e, a partir da 2ª tentativa, o histórico das versões reprovadas.
- Cada versão passa pelo código e pelo auditor v3 com o texto-fonte; as reprovadas de novo têm mais uma tentativa.
- Ganho líquido: deduplicação por sentido contra as 92 aprovadas do piloto.

Referência: o refinador do piloto (mini, prompt v19, só motivos recuperáveis) recuperou 25 depois da revisão
manual. Se o braço forte tiver ganho líquido claramente maior e a revisão manual confirmar a qualidade, ele vira o
refinador padrão da geração final.

### Resultado da 1ª etapa (`relatorios/teste_refino_20261024T161142Z`)

| Braço | recuperadas (auditor) | conhecimento novo (ganho líquido) | repetem uma aprovada | fracas na amostra manual de 16 novas |
|---|---|---|---|---|
| mini | 85/153 | 40 | 45 | ~9 (longas, confusas, reformulam o enunciado) |
| forte | 122/153 | 24 | 98 | ~5 |

- O forte recupera mais e melhor (nenhuma versão barrada por `fora_da_fonte`, contra 35 no mini), mas dois
  terços das recuperadas repetem o conhecimento de uma questão já aprovada: as janelas se sobrepõem e a questão
  reprovada costuma ser "irmã" de uma aprovada. Recuperar a forma não cria conhecimento novo.
- O mini muda mais a pergunta (mais conhecimento novo), mas metade das novas é fraca; o auditor aprova
  refinadas longas e confusas com facilidade.
- Nenhum braço descartou nada, apesar do prompt.

**2ª etapa: braço `forte_cob`.** O refinador forte recebe em `<ja_cobertas>` as aprovadas que tocam os mesmos
blocos (média de 8 por questão) e deve avaliar conhecimento que nenhuma delas avalia, ou descartar. O ganho
líquido passou a contar só conhecimento novo (uma por grupo de recuperadas equivalentes).

### Resultado da 2ª etapa e versão 21

| Braço | recuperadas | conhecimento novo | repetem aprovada | revisão manual das novas |
|---|---|---|---|---|
| mini | 85/153 | 40 | 45 | ~56% fracas (16) |
| forte | 122/153 | 24 | 98 | ~31% fracas (16) |
| **forte_cob** | 96/153 | **54** (92 → 146) | 42 (33 entre recuperadas da mesma rodada) | ~36% boas, ~44% aceitáveis, ~20% fracas (25) |

Com as questões já cobertas, o refinador forte deixa de repetir as aprovadas (só 9 repetem uma aprovada da
origem) e as novas são melhores que as da geração (~30% fracas no piloto v19). **v21**: o refinador do pipeline
passa a ser o `forte_cob` (gpt-5-4 high, `refinador_v3`, todos os motivos, `<ja_cobertas>`, exemplos aprovados,
até 2 tentativas com histórico, tipo pode mudar). No piloto v19 isso leva de 46 para ~73 válidas por tópico.
