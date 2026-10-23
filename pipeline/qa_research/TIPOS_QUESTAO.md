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
