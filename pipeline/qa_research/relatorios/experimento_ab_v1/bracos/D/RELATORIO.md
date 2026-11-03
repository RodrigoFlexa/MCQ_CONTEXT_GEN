# Geração completa (v19): uma passagem por janela e encadeamento, sem meta

Janela com o prompt v18 (sem decisão), compostas a partir dos encadeamentos, auditor v3 (com motivo, calibração e checagem contra o texto-fonte nas refinadas) como filtro, refinador com exemplos de reescrita, deduplicação por sentido no fim de cada tópico e banco dinâmico de exemplos e contraexemplos.

**Total: 290 questões válidas em 3 tópicos.**

| Tópico | Tema | blocos | encadeamentos | passagens de janela | rodadas | válidas | meta | janela aprov. | compostas aprov. | refinadas aprov. |
|---|---|---|---|---|---|---|---|---|---|---|
| 02_02 | Produtos químicos | 60 | 25 | 60 | 1 | **137** | - | 70/240 | 12/25 | 55/166 |
| 03_03 | Operação de tanques de carga, lastro, sistema | 29 | 23 | 29 | 1 | **74** | - | 39/116 | 5/23 | 30/106 |
| 07_01 | Instrumentação, Controle e Automação | 37 | 22 | 37 | 1 | **79** | - | 35/148 | 9/22 | 35/162 |

| Tipo | janela (aprov./geradas) | compostas (aprov./geradas) |
|---|---|---|
| conceito | 36/126 | 0/0 |
| mecanismo | 44/121 | 2/8 |
| consequencia | 9/66 | 7/27 |
| diagnostico | 37/86 | 10/21 |
| decisao | 0/0 | 7/14 |
| procedimento | 18/105 | 0/0 |

Por rodada (0 = compostas): r0: 41/112 (dup. 1, redund. 21); r1: 249/896 (dup. 18, redund. 170).
Motivos do auditor: {'janela': {'nenhum': 233, 'reformula_enunciado': 39, 'trivial': 80, 'prudencia_generica': 21, 'lista_generica': 22, 'resposta_vaga': 17, 'varias_respostas': 85, 'tecnicamente_errada': 5, 'caso_especifico': 2}, 'composta': {'nenhum': 39, 'varias_respostas': 12, 'reformula_enunciado': 11, 'trivial': 6, 'prudencia_generica': 1, 'resposta_vaga': 1}, 'refinada': {'trivial': 64, 'varias_respostas': 49, 'nenhum': 228, 'reformula_enunciado': 69, 'fora_da_fonte': 4, 'lista_generica': 7, 'prudencia_generica': 10, 'resposta_vaga': 2, 'tecnicamente_errada': 1}}.
Refinador: {'tentadas': 434, 'reescritas': 434, 'descartadas': 0, 'aprovadas_apos_refino': 120, 'por_motivo': {'prudencia_generica': 25, 'trivial': 135, 'reformula_enunciado': 86, 'varias_respostas': 133, 'lista_generica': 26, 'fora_da_fonte': 3, 'resposta_vaga': 19, 'tecnicamente_errada': 5, 'caso_especifico': 2}, 'por_tentativa': {1: {'tentadas': 302, 'aprovadas': 84}, 2: {'tentadas': 132, 'aprovadas': 36}}, 'tipo_mudou': 238}.
Banco dinâmico: {'aprovadas': 473, 'reprovadas': 508, 'herdadas': {'aprovadas': 0, 'reprovadas': 0}}. Falhas pendentes: 0.

## Amostra de aprovadas por tópico

### 02_02

**[diagnostico · composta]** Num FPSO, o sequestrante de oxigênio é dosado em água tratada e o controle automático usa um analisador on-line logo após a injeção. Após limpeza e checagem, esse analisador continua concordando com amostras do mesmo ponto e indica residual estável. Mesmo assim, cupons e amostras manuais mais a jusante passaram a mostrar maior corrosividade e oxidante residual, sem mudança na dosagem nominal. Que causa técnica explica melhor esse quadro?

- Resposta: Má mistura ou contato insuficiente do sequestrante, mascarados pela medição junto à injeção, que não representa a condição a jusante.

**[mecanismo · simples]** Como a redução da seção metálica efetiva do elemento sensor faz a sonda RE acusar maior perda de metal?

- Resposta: Porque a seção menor aumenta a resistência elétrica do sensor, e a sonda converte essa variação em perda metálica.

**[conceito · simples]** Qual método mecânico de limpeza interna pode ser muito eficaz para remover materiais aderidos da parede, mas pode ser inviável por geometrias não adequadas ou por exigir interrupção da produção?

- Resposta: Pigging, limitado por geometrias não adequadas e por eventual necessidade de interromper a produção.

**[conceito · simples]** Como se chamam os microrganismos dispersos na fase aquosa do sistema de água de injeção, em contraste com os aderidos às superfícies internas?

- Resposta: Células planctônicas.

### 03_03

**[conceito · simples]** Que grupo microbiológico, se mal controlado, pode elevar a geração de sulfeto de hidrogênio em áreas de produção e armazenamento?

- Resposta: Bactérias redutoras de sulfato.

**[consequencia · simples]** Mantidas as demais restrições da unidade, se o planejamento do lastro ignora a sequência das transferências, o que pode acontecer com o carregamento estrutural?

- Resposta: Pode ultrapassar os limites permissíveis de carregamento estrutural.

**[mecanismo · simples]** Por que alterar o trim para favorecer o bombeio de um tanque remanescente pode afetar a estabilidade e os esforços do casco?

- Resposta: Porque redistribui longitudinalmente o peso e modifica a resposta hidrostática da unidade.

**[consequencia · composta]** Após uma entrada para manutenção, um tanque de carga foi recomposto e recolocado em serviço inertizado. Um blank usado no isolamento permaneceu montado, o suprimento de gás inerte foi retomado e a indicação de pressão seguiu aumentando, sem atuação efetiva do alarme ou resposta da equipe. Nessa situação, que consequência pode atingir a integridade do tanque?

- Resposta: Deformação estrutural do tanque, porque a pressão pode continuar se elevando em tanque inertizado após recomposição incorreta sem barreira efetiva.

### 07_01

**[diagnostico · simples]** No comissionamento de uma válvula prevista para controlar nível, a saída do controlador varia continuamente e a posição indicada acompanha o movimento observado em campo. Mesmo assim, a haste sempre corre até 0% ou 100%, sem parar em posições intermediárias. Que incompatibilidade técnica isso evidencia?

- Resposta: Modo de atuação efetivo abre-fecha; a configuração de comando, lógica ou montagem não corresponde à função modulante prevista.

**[mecanismo · simples]** Durante a operação, por que um posicionador inteligente com diagnóstico fuzzy pode indicar sintomas como atrito ou vazamento sem abrir a válvula?

- Resposta: Conversão de variáveis medidas na própria válvula, como pressão do atuador e deslocamento do obturador, em inferências de estado e sintomas por regras fuzzy.

**[conceito · simples]** Na seleção de ação para função degradada, que característica da arquitetura de proteção ajuda a distinguir degradação parcial de indisponibilidade total?

- Resposta: Redundância independente entre os caminhos de proteção.

**[mecanismo · simples]** Em um FPSO, um intertravamento foi ensaiado até o logic solver, sem percorrer a interface com o ESD nem a atuação da válvula. Por que isso não demonstra a função completa?

- Resposta: Ficaram sem demonstração a interface SIS/ESD, o comando ao solenóide e a movimentação da válvula, que podem falhar mesmo com a lógica interna correta.
