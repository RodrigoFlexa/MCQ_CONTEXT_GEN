# Geração completa (v19): uma passagem por janela e encadeamento, sem meta

Janela com o prompt v18 (sem decisão), compostas a partir dos encadeamentos, auditor v3 (com motivo, calibração e checagem contra o texto-fonte nas refinadas) como filtro, refinador com exemplos de reescrita, deduplicação por sentido no fim de cada tópico e banco dinâmico de exemplos e contraexemplos.

**Total: 92 questões válidas em 2 tópicos.**

| Tópico | Tema | blocos | encadeamentos | passagens de janela | rodadas | válidas | meta | janela aprov. | compostas aprov. | refinadas aprov. |
|---|---|---|---|---|---|---|---|---|---|---|
| 03_03 | Operação de tanques de carga, lastro, sistema | 25 | 25 | 25 | 1 | **46** | - | 25/100 | 9/25 | 12/37 |
| 07_03 | Manutenção e Plano de Manutenção | 30 | 23 | 30 | 1 | **46** | - | 27/120 | 6/23 | 13/61 |

| Tipo | janela (aprov./geradas) | compostas (aprov./geradas) |
|---|---|---|
| conceito | 14/55 | 0/0 |
| mecanismo | 13/54 | 0/0 |
| consequencia | 1/27 | 4/20 |
| diagnostico | 17/37 | 3/9 |
| decisao | 0/0 | 8/19 |
| procedimento | 7/47 | 0/0 |

Por rodada (0 = compostas): r0: 19/65 (dup. 0, redund. 11); r1: 73/301 (dup. 1, redund. 39).
Motivos do auditor: {'janela': {'nenhum': 88, 'trivial': 39, 'resposta_vaga': 10, 'reformula_enunciado': 13, 'lista_generica': 5, 'caso_especifico': 9, 'varias_respostas': 44, 'prudencia_generica': 12}, 'composta': {'nenhum': 27, 'reformula_enunciado': 3, 'varias_respostas': 14, 'trivial': 2, 'tecnicamente_errada': 2}, 'refinada': {'nenhum': 41, 'trivial': 13, 'varias_respostas': 14, 'fora_da_fonte': 9, 'caso_especifico': 5, 'tecnicamente_errada': 1, 'resposta_vaga': 2, 'reformula_enunciado': 7, 'prudencia_generica': 2, 'lista_generica': 3, 'sim_nao_disfarcado': 1}}.
Refinador: {'tentadas': 98, 'reescritas': 98, 'descartadas': 0, 'aprovadas_apos_refino': 25, 'por_motivo': {'varias_respostas': 58, 'resposta_vaga': 10, 'caso_especifico': 9, 'reformula_enunciado': 16, 'lista_generica': 5}}.
Banco dinâmico: {'aprovadas': 998, 'reprovadas': 2408, 'herdadas': {'aprovadas': 906, 'reprovadas': 2185}}. Falhas pendentes: 0.

## Amostra de aprovadas por tópico

### 03_03

**[diagnostico · composta]** Em um FPSO com integração parcial entre vent e rede de gás inerte, um tanque de carga foi isolado individualmente para gas freeing. Após retorno, sem carga nem descarga, sem variação de temperatura e sem transferência ou operação de bombas, o gás inerte foi restabelecido e a pressão do tanque subiu continuamente. Que causa técnica explica melhor esse comportamento?

- Resposta: Blank mantido no trajeto de vent/alívio após o isolamento, bloqueando a rota de descarga e permitindo que o gás inerte sobrepressurize o tanque.

**[procedimento · simples]** Como deve ser verificada a aceitabilidade de manter a bomba de stripping com a descarga muito restringida?

- Resposta: Confrontando a condição com a curva da bomba e com os limites do sistema: tempo, recirculação mínima, proteções e resistência mecânica.

**[conceito · simples]** Qual é a função primária do sistema de ventilação dos tanques em um FPSO?

- Resposta: Permitir enchimento e esvaziamento sem sobrepressão nem vácuo excessivos.

**[decisao · composta]** Num FPSO, um tanque de serviço de óleo recebeu água produzida por várias semanas. Na inspeção seguinte, apareceram desplacamento de revestimento e perda localizada de espessura em costado e anteparas, e o desvio de armazenamento já foi reconhecido pela operação. Qual ação técnica prioritária deve ser adotada?

- Resposta: Interromper a exposição incompatível e reavaliar a aptidão do tanque, porque o serviço real com água produzida pode exceder a proteção concebida para óleo.

### 07_03

**[diagnostico · simples]** Uma unidade marítima afastada da costa adotou a mesma distribuição de tarefas usada em instalação costeira equivalente. Em operação, atividades presenciais acumulam postergações recorrentes; a mobilização de apoio em terra leva dias, e o efetivo embarcado não absorve a carga prevista. Já atividades com acompanhamento remoto seguem executáveis. Qual causa explica a inadequação do plano?

- Resposta: Estratégia de manutenção transposta de contexto costeiro sem incorporar as restrições logísticas e de suporte técnico da unidade marítima.

**[mecanismo · simples]** Por que organizar a programação em horizontes sucessivos de detalhamento ajuda a transformar demanda técnica em trabalho executável?

- Resposta: Porque o plano é refinado conforme surgem informações mais concretas sobre recursos, interferências e sequência das atividades.

**[mecanismo · simples]** Por que tratar todos os elementos igualmente em um indicador agregado pode mascarar a indisponibilidade de itens funcionalmente mais relevantes?

- Resposta: Porque a agregação sem pesos dilui a indisponibilidade dos itens críticos no índice global, misturando seu impacto ao dos elementos menos importantes.

**[conceito · simples]** Que abordagem define os requisitos de manutenção de ativos físicos segundo a função atualmente exigida do ativo?

- Resposta: Manutenção Centrada na Confiabilidade, RCM.
