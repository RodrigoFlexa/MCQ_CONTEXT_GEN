# Geração completa (v19): uma passagem por janela e encadeamento, sem meta

Janela com o prompt v18 (sem decisão), compostas a partir dos encadeamentos, auditor v3 (com motivo, calibração e checagem contra o texto-fonte nas refinadas) como filtro, refinador com exemplos de reescrita, deduplicação por sentido no fim de cada tópico e banco dinâmico de exemplos e contraexemplos.

**Total: 280 questões válidas em 3 tópicos.**

| Tópico | Tema | blocos | encadeamentos | passagens de janela | rodadas | válidas | meta | janela aprov. | compostas aprov. | refinadas aprov. |
|---|---|---|---|---|---|---|---|---|---|---|
| 02_02 | Produtos químicos | 57 | 24 | 57 | 1 | **121** | - | 62/228 | 10/24 | 49/180 |
| 03_03 | Operação de tanques de carga, lastro, sistema | 25 | 22 | 25 | 1 | **82** | - | 39/100 | 9/22 | 34/101 |
| 07_01 | Instrumentação, Controle e Automação | 34 | 20 | 34 | 1 | **77** | - | 37/136 | 6/20 | 34/149 |

| Tipo | janela (aprov./geradas) | compostas (aprov./geradas) |
|---|---|---|
| conceito | 33/116 | 0/0 |
| mecanismo | 48/117 | 2/4 |
| consequencia | 6/57 | 6/25 |
| diagnostico | 27/79 | 8/20 |
| decisao | 0/0 | 9/17 |
| procedimento | 24/95 | 0/0 |

Por rodada (0 = compostas): r0: 43/110 (dup. 1, redund. 15); r1: 237/850 (dup. 9, redund. 148).
Motivos do auditor: {'janela': {'nenhum': 203, 'varias_respostas': 76, 'trivial': 70, 'reformula_enunciado': 36, 'lista_generica': 25, 'prudencia_generica': 29, 'resposta_vaga': 9, 'tecnicamente_errada': 5, 'caso_especifico': 11}, 'composta': {'nenhum': 35, 'reformula_enunciado': 12, 'varias_respostas': 15, 'tecnicamente_errada': 1, 'trivial': 3}, 'refinada': {'nenhum': 215, 'varias_respostas': 64, 'reformula_enunciado': 61, 'trivial': 51, 'resposta_vaga': 7, 'sim_nao_disfarcado': 3, 'prudencia_generica': 16, 'lista_generica': 8, 'tecnicamente_errada': 2, 'caso_especifico': 2, 'fora_da_fonte': 1}}.
Refinador: {'tentadas': 430, 'reescritas': 430, 'descartadas': 0, 'aprovadas_apos_refino': 117, 'por_motivo': {'lista_generica': 29, 'varias_respostas': 135, 'reformula_enunciado': 81, 'trivial': 109, 'resposta_vaga': 14, 'prudencia_generica': 38, 'tecnicamente_errada': 8, 'sim_nao_disfarcado': 2, 'caso_especifico': 13, 'fora_da_fonte': 1}, 'por_tentativa': {1: {'tentadas': 292, 'aprovadas': 75}, 2: {'tentadas': 138, 'aprovadas': 42}}, 'tipo_mudou': 237}.
Banco dinâmico: {'aprovadas': 283, 'reprovadas': 507, 'herdadas': {'aprovadas': 0, 'reprovadas': 0}}. Falhas pendentes: 0.

## Amostra de aprovadas por tópico

### 02_02

**[mecanismo · simples]** Por que o teor de oxigênio residual obtido em um piloto de desaeração por membranas não deve ser assumido para qualquer água do mar, vazão ou arranjo offshore?

- Resposta: Dependência de projeto e operação: água, vazão e configuração alteram a transferência de massa e o residual de oxigênio atingível.

**[decisao · composta]** Em um FPSO, no separador de produção, após aumento do corte de água e mudança da salinidade com aparecimento de finos, a espuma passou a persistir, com arraste de líquido no gás. A dose do antiespumante em uso foi elevada em etapas, mas a resposta permaneceu irregular e não sustentada; internos e controle básico do vaso não mudaram. Que ação técnica específica deve ser tomada?

- Resposta: Revisar formulação e ponto de aplicação do antiespumante, porque a mudança do fluido tornou inconsistente a resposta ao simples aumento de dose.

**[conceito · simples]** Na desaeração por membranas com contatoores de fibras ocas, qual característica do contator favorece sistemas compactos e modulares?

- Resposta: Grande área interfacial por volume.

**[conceito · simples]** Que relação governa a necessidade de dosagem de bissulfito de sódio na água de injeção?

- Resposta: A estequiometria com o oxigênio dissolvido: a dosagem requerida acompanha a carga de O2 a remover.

### 03_03

**[mecanismo · composta]** Numa unidade em que o condensado normalmente segue ao processamento de óleo, a operação passou para modo sem produção de óleo. Sem mudança na composição do condensado, por que a destinação dessa corrente pode precisar mudar?

- Resposta: Porque o modo operacional muda o arranjo e a disponibilidade dos sistemas; nesse modo, o condensado pode exigir desidratação e seguir para exportação por gasoduto.

**[consequencia · composta]** Durante offloading com crude oil washing, um tanque de carga inertizado permanece em descarga com recirculação pelos bicos e vapores de hidrocarbonetos no espaço de vapor. Os jatos de lavagem seguem atuando, porém a pressão de gás inerte do tanque não se mantém no patamar esperado ao longo da operação. Nessa condição, que atmosfera específica pode surgir no tanque?

- Resposta: Mistura inflamável no espaço de vapor, porque o COW aumenta a dependência da inertização contínua e a queda de pressão do GI pode tirar o tanque da condição não inflamável.

**[mecanismo · simples]** Como trincas e tubulações corroídas podem degradar a condição segura mantida pelo sistema de gás inerte em tanques de carga?

- Resposta: Ao criarem caminhos de ingresso de oxigênio, desestabilizam o controle de atmosfera e degradam a inertização segura do tanque.

**[mecanismo · simples]** Após manutenção, um blank ficou na rota de vent/alívio de um tanque inertizado. O suprimento de gás inerte continua e a pressão sobe. Que falha adicional permite que o evento evolua até deformação estrutural do tanque?

- Resposta: Falha do alarme de pressão ou da resposta operacional a ele, permitindo que a sobrepressão prossiga até níveis estruturais.

### 07_01

**[mecanismo · simples]** No comissionamento de um circuito com intertravamentos, por que os testes da matriz de causa e efeito continuam decisivos mesmo quando painéis, comandos manuais e instrumentos parecem normais?

- Resposta: Porque verificam a cadeia causa-efeito integrada, confirmando que a condição de processo aciona a lógica, a comunicação e os elementos finais previstos da função de segurança.

**[mecanismo · simples]** Após comissionar o circuito de regeneração em malha fechada com N2, a equipe quer liberar a entrada de gás natural alegando que o desempenho já foi comprovado. Por que esse resultado, sozinho, não valida integralmente o comportamento do subsistema em serviço?

- Resposta: Representatividade parcial: o arranjo com N2 não reproduz todos os cenários de processo, combustão, composição do gás nem a resposta das barreiras ao inventário real.

**[conceito · simples]** Em uma medição com placa de orifício que usa três transmissores distintos para calcular a vazão, que grandezas cada um mede?

- Resposta: Pressão estática, pressão diferencial e temperatura.

**[procedimento · simples]** No retorno ao serviço de uma função de proteção, em que condição a liberação passa a exigir análise de engenharia e aprovação por profissional habilitado?

- Resposta: Quando a ação necessária estiver em desacordo com a documentação técnica existente ou fora de sua cobertura.
