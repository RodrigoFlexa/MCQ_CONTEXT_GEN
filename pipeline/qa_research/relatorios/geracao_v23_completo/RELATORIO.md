# Geração v22

Braço v23_completo: 2006 questões finais de 8324 propostas (86 recusadas pela régua, 2292/8238 aprovadas pelo auditor, 286 redundantes).

Chamadas do gerador: 4320, das quais 250 sem questões; questões por chamada: {0: 250, 1: 1668, 2: 970, 3: 1012, 4: 420}.
Falhas do auditor por verificação: {'atalho': 5211, 'varias_respostas': 1139, 'nao_unico': 65, 'fora_da_fonte': 230, 'depende_do_documento': 239, 'bloqueio': 1}.
Segunda chance: 838 revisitas de foco após visita sem ganho (321 conhecimentos novos); 502 segundas tentativas de composta (86 finais).
Conhecimentos novos por rodada: {1: 737, 2: 406, 3: 268, 4: 123, 5: 54}; focos por número de visitas: {1: 6, 2: 305, 3: 319, 4: 170, 5: 145}.
Tipos finais: {'diagnostico': 557, 'decisao': 772, 'mecanismo': 255, 'conceito': 121, 'consequencia': 73, 'procedimento': 228}.
Falhas pendentes: 0.

## Amostra de questões finais

**[04_02 · mecanismo · janela]** Em uma válvula subsea configurada como fail safe close, ocorre perda da pressão de controle e a válvula vai ao fechado sem novo comando de abertura ou fechamento. Qual elemento mecânico efetivamente produz esse movimento até o estado seguro?

- Resposta: Mola de retorno do atuador.
- Explicação: Nessa filosofia, a perda de pressão libera a atuação da mola, que leva a válvula ao fechado sem depender de novo acionamento hidráulico.

**[02_08 · diagnostico · janela]** Após trips reais de um mesmo segmento, os testes periódicos ainda mostram comando de ESD e curso da BDV normais. Sem programar novo ensaio, que registro operacional deve ser confrontado com a previsão para verificar se a despressurização real continua aderente ao esperado?

- Resposta: Curva pressão-tempo dos blowdowns reais do segmento.
- Explicação: A aderência da função aparece na queda real de pressão entre a condição inicial e a final; esse histórico incorpora atraso, perdas de carga, contrapressão e evolução do fluido.

**[02_09 · diagnostico · janela]** Em um mesmo período, o óleo tratado passa a sair com BSW e teor de sal acima do padrão recente. Qual fenômeno na corrente oleosa fica tecnicamente mais compatível com esse desvio conjunto?

- Resposta: Retenção de água salgada dispersa no óleo tratado.
- Explicação: Parte do sal acompanha a água arrastada com o óleo; quando BSW e sal sobem juntos, o sinal aponta para permanência de gotículas aquosas salinas na fase oleosa.

**[02_08 · decisao · janela]** Um vaso tem um cenário de sobrepressão com grande vazão e outro com vazão bem menor. A PSV única dimensionada pelo caso governante limita a pressão, mas no evento de menor carga não se comporta de forma estável. Que arranjo de proteção deve ser adotado para que só o primeiro dispositivo atue na menor vazão, sem perder cobertura do caso maior?

- Resposta: Duas PSVs com pressões de ajuste diferentes.
- Explicação: Quando a inadequação aparece no cenário de menor carga, uma solução contextual é escalonar os setpoints para que só a primeira válvula abra nesse evento, mantendo a proteção do caso governante.

**[04_01 · diagnostico · janela]** Depois do pull-in de um riser flexível, não há vazamento e a geometria final ficou aceitável, mas surge uma abertura axial entre a base do bend stiffener e o terminal de topo após os primeiros ciclos de movimento da unidade. Qual condição específica do conjunto deve ser verificada primeiro?

- Resposta: Fixação do bend stiffener.
- Explicação: Abertura axial na interface do acessório aponta para perda ou falha de fixação; esse item deve ser verificado junto com trincas, abrasão e deformações.

**[09_02 · decisao · janela]** Uma carga assimétrica, sem pega segura, precisa cruzar entre corrimão e estrutura secundária e tende a girar ao perder contato com o convés. Na reunião pré-tarefa, que meio de controle de orientação deve ficar definido para a execução?

- Resposta: Uso de tag lines.
- Explicação: O alinhamento pré-tarefa deve definir o uso esperado de tag lines. Em passagem estreita com tendência de giro, elas permitem controlar a orientação à distância.

**[03_02 · decisao · janela]** Na falta de histórico local, planeja-se aplicar em um FPSO o estimador de direção de mar por movimentos, calibrado em outra unidade de porte semelhante. Qual elemento técnico deve ser confirmado como compatível antes de aceitar essa transferência?

- Resposta: A resposta hidrodinâmica da própria unidade, expressa nos RAOs.
- Explicação: A inferência depende dos RAOs representados no modelo. Sem compatibilidade da resposta hidrodinâmica, semelhança de porte não garante a mesma recuperação direcional.

**[06_06 · consequencia · composta]** Durante o muster em um FPSO, todo o pessoal precisa passar por um único leitor instalado antes da área segura para validar presença, antes de prosseguir por qualquer acesso disponível. Na análise temporal da evacuação, qual elemento técnico esse arranjo reduz diretamente?

- Resposta: A margem entre o tempo de resistência e o tempo necessário de evacuação.
- Explicação: A validação obrigatória em ponto único restringe o movimento do pessoal e aumenta o tempo necessário de deslocamento e organização. Como a viabilidade depende da folga entre esse tempo e o tempo de resistência disponível, a margem diminui.

**[05_02 · decisao · janela]** Após substituição de relés em vários alimentadores, a equipe quer conferir se pickups e temporizações parametrizados no campo ainda correspondem à coordenação aprovada, sem reinterpretar curva por curva de cada função. Qual documento deve ser a referência central dessa conferência?

- Resposta: Planilha mestra de ajustes de proteção.
- Explicação: Ela consolida os valores de ajuste a implantar e comparar no campo; o estudo de seletividade sustenta a coordenação, mas não substitui essa referência operacional.

**[06_05 · diagnostico · janela]** Após um remanejamento de detectores, um detector de gás entra em alarme local, aparece com identificação correta no supervisório e, quando há confirmação por outro detector da mesma área, a resposta automática ocorre na área vizinha enquanto a zona esperada não fecha a votação. Qual falha de configuração explica melhor esse comportamento?

- Resposta: Associação do detector à zona de votação errada.
- Explicação: O ponto detecta e transmite corretamente, mas está contando para a lógica de outra zona; por isso a confirmação e a causa e efeito se materializam no arranjo vizinho.

**[05_01 · diagnostico · janela]** Em uma malha de aquecimento de óleo, após um aumento de carga, a temperatura medida fica inicialmente sem mudar e o operador tende a abrir mais a válvula antes de qualquer reação; depois a temperatura sobe e passa do alvo. Que elemento da malha concentra esse atraso inicial enganoso?

- Resposta: Medição de temperatura na saída do trocador.
- Explicação: O intervalo inicial sem reação caracteriza tempo morto; nos blocos, ele está associado à medição na saída do trocador. A inércia térmica explica lentidão depois que a resposta começa.

**[06_07 · procedimento · janela]** Uma intervenção longa usa duas válvulas em série como segregação, com possibilidade de pequena passagem interna ao longo das horas. Para acompanhar se a barreira continua eficaz durante a execução, em que ponto do arranjo a verificação deve permanecer disponível?

- Resposta: No ponto intermediário de alívio/verificação.
- Explicação: No bloqueio e sangria, a eficácia depende da estanqueidade das válvulas. O volume entre elas é o ponto que revela passagem antes que o inventário alcance a frente de trabalho.

**[02_11 · decisao · janela]** Em uma corrente de gás úmido que sofrerá estrangulamento e depois seguirá por um trecho mais frio, o circuito previsto é de dosagem com recirculação do glicol para evitar hidratos. Qual glicol deve ser selecionado?

- Resposta: MEG
- Explicação: O bloco foco associa o MEG à prevenção de hidratos em estrangulamentos e correntes que serão resfriadas depois, com recuperação posterior da água absorvida.

**[02_05 · decisao · janela]** Uma linha de drenagem ficará poucos dias fora de serviço após receber condensado, em material cuja corrosão por umidade não é o fator dominante nesse período. Depois de drenada, qual condicionamento adicional deve ser adotado para manter a condição segura durante a parada?

- Resposta: Inertização interna com gás inerte.
- Explicação: Com resíduo de condensado e parada curta, o risco decisivo é atmosfera inflamável remanescente. A condição segura na retirada de serviço depende do fluido residual, do material e do tempo de parada.

**[02_12 · consequencia · composta]** Em um compressor de duas seções, a sucção da segunda acompanha oscilações da descarga da primeira. Em rotação moderada, a válvula de reciclo dessa seção permanece muito aberta e a potência consumida sobe. Se, para reduzir essa perda, o ajuste de proteção da segunda seção for deslocado para diminuir a abertura do reciclo sem revalidar o envelope operacional, qual efeito final pode ser introduzido no trem?

- Resposta: Propagação de instabilidade entre as seções.
- Explicação: Como a sucção da segunda seção varia com a primeira, um ajuste nominal pode já estar deslocado. Reduzir reciclo movendo a proteção sem revalidar o envelope corta margem e pode acoplar a instabilidade às duas seções.
