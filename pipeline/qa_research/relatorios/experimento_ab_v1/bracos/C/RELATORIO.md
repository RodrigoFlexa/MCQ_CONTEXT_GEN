# Geração completa (v19): uma passagem por janela e encadeamento, sem meta

Janela com o prompt v18 (sem decisão), compostas a partir dos encadeamentos, auditor v3 (com motivo, calibração e checagem contra o texto-fonte nas refinadas) como filtro, refinador com exemplos de reescrita, deduplicação por sentido no fim de cada tópico e banco dinâmico de exemplos e contraexemplos.

**Total: 271 questões válidas em 3 tópicos.**

| Tópico | Tema | blocos | encadeamentos | passagens de janela | rodadas | válidas | meta | janela aprov. | compostas aprov. | refinadas aprov. |
|---|---|---|---|---|---|---|---|---|---|---|
| 02_02 | Produtos químicos | 57 | 24 | 57 | 1 | **131** | - | 65/228 | 11/24 | 55/181 |
| 03_03 | Operação de tanques de carga, lastro, sistema | 25 | 22 | 25 | 1 | **62** | - | 25/100 | 7/22 | 30/117 |
| 07_01 | Instrumentação, Controle e Automação | 34 | 20 | 34 | 1 | **78** | - | 41/136 | 6/20 | 31/128 |

| Tipo | janela (aprov./geradas) | compostas (aprov./geradas) |
|---|---|---|
| conceito | 28/116 | 0/0 |
| mecanismo | 44/116 | 1/3 |
| consequencia | 11/63 | 4/26 |
| diagnostico | 31/71 | 12/19 |
| decisao | 0/0 | 7/18 |
| procedimento | 17/98 | 0/0 |

Por rodada (0 = compostas): r0: 41/120 (dup. 2, redund. 13); r1: 230/836 (dup. 11, redund. 149).
Motivos do auditor: {'janela': {'nenhum': 205, 'lista_generica': 27, 'varias_respostas': 84, 'prudencia_generica': 22, 'reformula_enunciado': 36, 'trivial': 65, 'resposta_vaga': 13, 'sim_nao_disfarcado': 1, 'caso_especifico': 6, 'tecnicamente_errada': 5}, 'composta': {'nenhum': 32, 'varias_respostas': 17, 'reformula_enunciado': 13, 'trivial': 3, 'resposta_vaga': 1}, 'refinada': {'nenhum': 209, 'reformula_enunciado': 75, 'prudencia_generica': 17, 'fora_da_fonte': 3, 'trivial': 47, 'caso_especifico': 4, 'varias_respostas': 52, 'lista_generica': 11, 'resposta_vaga': 6, 'tecnicamente_errada': 2}}.
Refinador: {'tentadas': 427, 'reescritas': 426, 'descartadas': 1, 'aprovadas_apos_refino': 116, 'por_motivo': {'lista_generica': 34, 'varias_respostas': 132, 'reformula_enunciado': 95, 'prudencia_generica': 34, 'resposta_vaga': 15, 'trivial': 100, 'caso_especifico': 9, 'sim_nao_disfarcado': 1, 'tecnicamente_errada': 6, 'fora_da_fonte': 1}, 'por_tentativa': {1: {'tentadas': 293, 'aprovadas': 77}, 2: {'tentadas': 134, 'aprovadas': 39}}, 'tipo_mudou': 236}.
Banco dinâmico: {'aprovadas': 428, 'reprovadas': 510, 'herdadas': {'aprovadas': 0, 'reprovadas': 0}}. Falhas pendentes: 0.

## Amostra de aprovadas por tópico

### 02_02

**[decisao · composta]** Em um separador de produção de FPSO que já opera com antiespumante, o corte de água aumentou, a água produzida ficou mais salina e passaram a aparecer finos. A espuma no vaso ficou mais persistente, com episódios de arraste de líquido no gás. Reforços sucessivos da dose do mesmo produto deram resposta irregular, sem melhora progressiva. Qual ação técnica específica deve ser tomada no programa químico?

- Resposta: Revisar a formulação e o ponto de aplicação do antiespumante, porque a mudança de salinidade, finos e corte de água tornou insuficiente apenas elevar a dose.

**[conceito · composta]** Num sistema com URS, propõe-se usar a dosagem de anti-incrustante na água de injeção como única barreira para proteger também o poço produtor. Antes de aprovar essa estratégia, que limitação técnica do trajeto pelo reservatório precisa ser considerada?

- Resposta: Adsorção na rocha ao redor do poço injetor, que pode reter o inibidor e impedir que ele alcance o poço produtor.

**[mecanismo · simples]** Num bottle test, uma família de desemulsificante respondeu melhor em baixo pH. No FPSO, pH, salinidade e dosagem ficaram alinhados ao ensaio, mas uma mudança de arranjo aumentou a mistura em válvulas e bombas antes do tratador e o ganho desapareceu. Que mecanismo técnico explica a divergência?

- Resposta: Cisalhamento mais intenso, porque mantém a emulsão mais dispersa e dificulta a coalescência que o produto precisa promover.

**[procedimento · simples]** Após uma intervenção no poço, o fósforo residual na água produzida caiu até a MIC, com amostragem representativa e método analítico compatível. Antes de indicar novo squeeze, que critério de interpretação deve ser aplicado?

- Resposta: Interpretação conjunta com histórico do poço, produção de água, intervenções e mudanças de regime; o valor na MIC, isoladamente, não comprova esgotamento do squeeze.

### 03_03

**[mecanismo · simples]** Como a ausência, na interface do operador, de informações relevantes da bomba e da posição das válvulas torna parcial a supervisão da transferência?

- Resposta: Porque sem esses sinais o operador não confirma os trechos conectados nem a pressão efetivamente enxergada pelo circuito.

**[mecanismo · simples]** Como trincas estruturais e tubulações corroídas degradam a condição segura de atmosfera de um tanque de carga?

- Resposta: Ao abrir caminhos para ingresso de oxigênio, aumentam o O2 interno e comprometem a inertização.

**[diagnostico · composta]** Num FPSO, para contornar a indisponibilidade de uma linha de transferência, a equipe instalou sem MOC um spool temporário por um trecho associado ao gás inerte. Após o alinhamento, a vazão caiu, apareceu aumento de nível em um tanque fora da operação e surgiu pressão em um trecho que deveria permanecer isolado. Que mecanismo oculto esse arranjo provavelmente criou?

- Resposta: Caminho de retorno entre sistemas, porque a conexão temporária pode permitir pressurização inesperada ou enchimento indevido de trechos que deveriam ficar isolados.

**[conceito · simples]** Na lavagem interna do tanque com óleo cru durante o offloading, por onde o óleo retorna ao tanque?

- Resposta: Pelos bicos de aspersão.

### 07_01

**[conceito · simples]** No conjunto de atuação de uma válvula de controle, como se chama a oscilação apreciável que continua mesmo depois de cessar a perturbação externa?

- Resposta: Hunting.

**[conceito · simples]** Na medição de vazão com placa de orifício, quais sinais de processo os transmissores devem enviar ao computador de vazão para que ele calcule a vazão?

- Resposta: Pressão diferencial, pressão estática e temperatura, combinadas pelo computador de vazão conforme o procedimento configurado.

**[mecanismo · simples]** Em um FPSO, a equipe vai retirar do anúncio da sala de controle várias mudanças de estado que não exigem ação imediata, mas teme perder elementos para reconstruir uma perturbação depois. Por que essa reclassificação não prejudica a análise posterior?

- Resposta: Permanência como eventos registrados no histórico, úteis ao diagnóstico, sem disputar atenção com alarmes acionáveis.

**[mecanismo · simples]** Por que a falta de detecção da perda de redundância pode deixar o sistema operando em resiliência reduzida sem resposta tempestiva?

- Resposta: Porque a falha ou comutação de um canal passa despercebida, o reparo não é acionado a tempo e o serviço segue sem caminho alternativo efetivo.
