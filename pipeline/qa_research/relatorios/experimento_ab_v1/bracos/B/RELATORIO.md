# Geração completa (v19): uma passagem por janela e encadeamento, sem meta

Janela com o prompt v18 (sem decisão), compostas a partir dos encadeamentos, auditor v3 (com motivo, calibração e checagem contra o texto-fonte nas refinadas) como filtro, refinador com exemplos de reescrita, deduplicação por sentido no fim de cada tópico e banco dinâmico de exemplos e contraexemplos.

**Total: 342 questões válidas em 3 tópicos.**

| Tópico | Tema | blocos | encadeamentos | passagens de janela | rodadas | válidas | meta | janela aprov. | compostas aprov. | refinadas aprov. |
|---|---|---|---|---|---|---|---|---|---|---|
| 02_02 | Produtos químicos | 60 | 25 | 60 | 1 | **156** | - | 84/240 | 13/25 | 59/144 |
| 03_03 | Operação de tanques de carga, lastro, sistema | 29 | 23 | 29 | 1 | **86** | - | 42/116 | 5/23 | 39/107 |
| 07_01 | Instrumentação, Controle e Automação | 37 | 22 | 37 | 1 | **100** | - | 41/148 | 8/22 | 51/152 |

| Tipo | janela (aprov./geradas) | compostas (aprov./geradas) |
|---|---|---|
| conceito | 35/126 | 0/0 |
| mecanismo | 49/126 | 5/7 |
| consequencia | 14/65 | 4/25 |
| diagnostico | 41/83 | 13/22 |
| decisao | 0/0 | 4/16 |
| procedimento | 28/104 | 0/0 |

Por rodada (0 = compostas): r0: 47/122 (dup. 0, redund. 9); r1: 295/855 (dup. 10, redund. 147).
Motivos do auditor: {'janela': {'trivial': 70, 'nenhum': 248, 'reformula_enunciado': 47, 'lista_generica': 24, 'resposta_vaga': 20, 'prudencia_generica': 27, 'varias_respostas': 62, 'caso_especifico': 2, 'tecnicamente_errada': 4}, 'composta': {'nenhum': 34, 'varias_respostas': 14, 'reformula_enunciado': 10, 'tecnicamente_errada': 1, 'trivial': 4, 'resposta_vaga': 1, 'prudencia_generica': 5, 'lista_generica': 1}, 'refinada': {'nenhum': 226, 'varias_respostas': 47, 'reformula_enunciado': 49, 'trivial': 44, 'fora_da_fonte': 2, 'prudencia_generica': 14, 'resposta_vaga': 6, 'lista_generica': 14, 'caso_especifico': 1}}.
Refinador: {'tentadas': 408, 'reescritas': 403, 'descartadas': 5, 'aprovadas_apos_refino': 149, 'por_motivo': {'reformula_enunciado': 87, 'varias_respostas': 113, 'caso_especifico': 3, 'resposta_vaga': 23, 'prudencia_generica': 40, 'lista_generica': 34, 'trivial': 102, 'fora_da_fonte': 1, 'tecnicamente_errada': 5}, 'por_tentativa': {1: {'tentadas': 292, 'aprovadas': 110}, 2: {'tentadas': 116, 'aprovadas': 39}}, 'tipo_mudou': 221}.
Banco dinâmico: {'aprovadas': 352, 'reprovadas': 469, 'herdadas': {'aprovadas': 0, 'reprovadas': 0}}. Falhas pendentes: 0.

## Amostra de aprovadas por tópico

### 02_02

**[diagnostico · simples]** Em uma linha fria e pressurizada, a vazão prevista de injeção de MEG está mantida. Amostras representativas logo após o ponto de injeção mostram teor alto de MEG, mas, mais a jusante, coletas sucessivas da água livre alternam entre teor muito baixo e muito alto; os hidratos aparecem de forma intermitente. Qual causa técnica explica a perda de proteção?

- Resposta: Mistura insuficiente do MEG com a água livre, gerando distribuição não homogênea e bolsões localmente sem concentração suficiente para inibir hidratos.

**[conceito · simples]** Na desoxigenação mecânica da água de injeção, qual rota opera por redução de pressão, e não por gás em contracorrente?

- Resposta: Desaeração por torre a vácuo.

**[procedimento · simples]** Após mudança de salinidade ou teor de sólidos do fluido, como deve ser verificada a faixa útil de dosagem do antiespumante?

- Resposta: Com ensaio no fluido de produção, levantando novamente a resposta à dose nessa nova condição.

**[mecanismo · simples]** Na água de injeção, que aspecto da água de alimentação pode reduzir o biocida disponível a jusante mesmo sem mudar produto nem tempo de contato?

- Resposta: Demanda química maior da água, consumindo parte do ativo antes de ele alcançar a região contaminada.

### 03_03

**[conceito · simples]** Que sistema mantém a condição segura da atmosfera interna de um tanque de carga frente ao ingresso de oxigênio?

- Resposta: Sistema de gás inerte.

**[procedimento · simples]** Em perda total de energia durante uma condição degradada, como deve permanecer disponível a bordo o cálculo de estabilidade?

- Resposta: Por solução computacional de contingência ou método manual previsto, que a equipe marítima saiba executar e interpretar.

**[mecanismo · simples]** Em offloading normal entre FPSO e navio aliviador, a pressão e o O2 dos tanques estão conformes. Por que isso ainda não permite afirmar operação sem emissões atmosféricas?

- Resposta: Porque a arquitetura aprovada de ventilação pode prever descarga de vapores ou IG à atmosfera; inertização e pressão conforme não significam operação sem emissões.

**[diagnostico · simples]** Após manutenção com isolamento individual, um tanque inertizado retorna ao serviço. Sem movimentação de líquido, a pressão sobe quando o gás inerte é admitido; depois surgem deformações, e o alarme de pressão não atuou ou não foi atendido. Qual é a causa mais provável?

- Resposta: Blank remanescente bloqueando a rota normal de vent e alívio após o isolamento.

### 07_01

**[mecanismo · simples]** Por que certificado de fabricante, calibração de bancada e verificação em campo não se substituem na evidência metrológica de um analisador instalado?

- Resposta: Porque cada uma comprova aspecto distinto: documentação de origem, desempenho em ensaio controlado e desempenho no arranjo real de serviço.

**[mecanismo · composta]** Dois instrumentos do mesmo modelo saem da bancada com estabilidade metrológica equivalente. Após alguns meses, o instalado em um FPSO passou a exigir verificação mais frequente que o mantido em bancada. Que mecanismo técnico explica essa diferença?

- Resposta: Alteração da resposta no arranjo instalado: o instrumento deixa o ensaio controlado e passa a sofrer solicitações do processo e do ambiente, o que acelera degradação e deriva.

**[diagnostico · simples]** Durante um teste, o comando remoto abre a válvula, a vazão aumenta e o atuador se move no campo, mas a posição indicada no controlador permanece congelada. Que perda técnica esse quadro caracteriza?

- Resposta: Perda de medição; o comando atua e o processo reage, mas o retorno ao controlador não representa a condição real.

**[procedimento · simples]** Ao investigar um sintoma de automação com origem ainda indefinida, como a análise deve ser estruturada para reduzir o risco de atribuir a causa à camada errada?

- Resposta: Por diagnóstico por camadas, começando no nível em que o sintoma se manifesta e separando supervisão, controlador, rede, interfaces de E/S e campo.
