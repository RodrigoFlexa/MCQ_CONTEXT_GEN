# Operação de tanques de carga, lastro, sistema gás inerte, ventilação e estabilidade

Tópico: Sistemas de Lastro, Estabilidade, Ancoragem e Posicionamento, Offloading e Tanques de Carga

> Frase do especialista: As questões devem abordar os aspectos de projeto, comissionamento, operação, controle, monitoramento, inspeção, manutenção, integridade e resposta a condições anormais dos sistemas associados aos tanques de carga, slop tanks e tanques de lastro de FPSOs, incluindo planejamento e sequência das operações de enchimento, esvaziamento, transferência interna e offloading, distribuição de carga entre tanques, controle de níveis, pressões, temperaturas e interfaces óleo-água, segregação e gerenciamento de slops, drenagens, resíduos oleosos e água de lavagem, operação de bombas, válvulas, manifolds e redes de transferência, prevenção de overfilling, overflow, contaminação cruzada e entrada indevida de hidrocarbonetos em tanques de lastro, operação e monitoramento do sistema de gás inerte, incluindo geração ou suprimento, qualidade, teor de oxigênio, pressão, distribuição, purga, inertização e prevenção da formação de atmosferas inflamáveis, sistemas de ventilação e controle de pressão e vácuo dos tanques, incluindo P/V valves, mast risers, flame screens e dispositivos de proteção contra sobrepressão e vácuo, controle e destinação de vapores de hidrocarbonetos e prevenção de emissões indevidas, operações de limpeza, gas freeing, entrada em tanques e retorno ao serviço, monitoramento de atmosferas perigosas, corrosão, sedimentos e integridade estrutural dos tanques, operação dos sistemas de lastro e deslastro, tratamento e gerenciamento da água de lastro, controle de calado, trim, banda, deslocamento, esforços longitudinais, shear forces e bending moments, influência da movimentação de carga, lastro e consumíveis sobre o centro de gravidade, estabilidade intacta e condições de avaria, efeitos de superfície livre, uso e interpretação dos sistemas de loading computer e instrumentação associada, manutenção dos limites operacionais e estruturais durante produção, offloading, manutenção e condições de emergência, além da integração entre gerenciamento de carga, lastro, estabilidade, integridade do casco, segurança marítima, proteção ambiental e boas práticas de engenharia para assegurar a operação segura e eficiente do FPSO.

## a02 · planejamento e sequência das operações de enchimento, esvaziamento, transferência interna e offloading

_Sem material nos corpora que sustente uma nota técnica. Assunto marcado para geração **sem contexto**._

## a03 · distribuição de carga entre tanques

_Sem material nos corpora que sustente uma nota técnica. Assunto marcado para geração **sem contexto**._

## a04 · controle de níveis, pressões, temperaturas e interfaces óleo-água

### Medição e controle da interface óleo-água em vasos e separadores: criticidade, limitações de medição e efeito da manutenção na confiabilidade

_Controlar a interface óleo-água é essencial porque o separador precisa manter segregadas as correntes líquidas: se a interface subir ou descer indevidamente, pode haver óleo na linha de água ou água na linha de óleo. O problema é que, em serviço real, a interface frequentemente não é uma linha nítida, mas uma zona perturbada por emulsão, espuma, gás, sólidos, turbulência e variações de densidade associadas à temperatura. Isso reduz a confiabilidade da medição e, por consequência, do controle. Nos documentos recuperados, métodos dependentes de densidade ficam vulneráveis quando essa propriedade varia; medidores tipo empuxo em standpipe apresentaram histórico operacional ruim; e sistemas nucleônicos aparecem como capazes de localizar a interface a partir de um perfil de densidade. O material também mostra que manutenção inadequada e atraso na substituição de tecnologia problemática podem degradar a confiança no valor indicado ao operador e no desempenho do controle._

**O que é e para que serve.** A função da medição de interface não é apenas informar um nível dentro do vaso, mas sustentar a separação entre duas correntes líquidas que saem por linhas distintas. Nos documentos, a interface água-óleo deve ser controlada para evitar entrada de óleo na linha de água e entrada de água na linha de óleo. Portanto, o controle da interface atua diretamente sobre a qualidade da segregação entre as fases líquidas do separador. [1]

**Princípio de funcionamento e mecanismo.** A dificuldade prática surge porque, em separadores multifásicos, a interface muitas vezes deixa de ser uma fronteira nítida. O material relata que a presença simultânea de água, óleo, gás, sólidos, espuma e emulsão, sob turbulência, desafia a medição confiável de nível. Também registra que, com espuma e emulsão, a interface água-óleo não fica perfeitamente definida. Contribuição paramétrica: quando a transição entre fases vira uma faixa de mistura, o instrumento pode deixar de indicar uma posição geométrica única e passar a responder a uma zona de propriedades variáveis. Isso tende a introduzir oscilação, atraso ou ambiguidade no sinal usado para controle. [2][3]

**Variáveis e condições operacionais.** Os documentos destacam uma limitação clara dos métodos que dependem de densidade. A medição por diferencial de pressão é calculada a partir de densidade, gravidade e altura e funciona quando a densidade é conhecida com precisão e permanece geralmente constante. No caso citado, a temperatura do fluido varia continuamente e altera essa densidade, comprometendo a medição; seria necessário recalculá-la continuamente com base na temperatura. Contribuição paramétrica: em separadores de produção, a dificuldade pode aumentar porque a densidade aparente na região da interface também pode mudar com teor de água, gás disperso, emulsão e sólidos, não apenas com temperatura. [4][5]

**Divergências e limites das fontes.** Os materiais recuperados permitem comparar alguns princípios de medição aplicáveis à interface. O medidor tipo empuxo instalado em standpipe foi associado, em relatório citado pela ANP, a problemas sérios de histórico operacional: tendência à descalibração, erros de medição, retardo de resposta e alta frequência de manutenção. Por isso, relatórios internos recomendaram descontinuar seu uso para interface água/óleo e estudar soluções melhores para SGs e TOs. Em contraste, o sistema nucleônico descrito para o outlet vessel mede por atenuação de raios gama: sensores perfilados captam um sinal correspondente à densidade do meio, o sistema compara esse sinal com uma tabela previamente carregada, determina a posição da interface e converte a medição em 4 a 20 mA. Em outro caso recuperado, detectores nucleônico e indutivo ambos identificavam a presença de emulsões, mas apenas o nucleônico localizava a interface óleo-água e os sólidos no fundo do vaso. Contribuição paramétrica: isso sugere uma diferença operacional relevante entre detectar que existe uma zona emulsificada e localizar onde está a interface útil para controle. [6][7][8][9]

**Segurança e riscos.** A confiabilidade do controle depende da tecnologia e também da sua manutenção. Na P-53, houve causa sistêmica para a falta de manutenção dos medidores de interface dos separadores: após a redução do efetivo a bordo, algumas manutenções preventivas foram substituídas por verificações de rotina da Operação, sem plano de manutenção periódica associado. O mesmo relatório afirma que os prazos adotados foram incompatíveis com a urgência de substituir o tipo de medidor. Além disso, durante o acidente, o valor mostrado no painel indicava faixa operacional, mas a investigação verificou que o medidor de interface apresentou problemas operacionais e não refletia o valor real. Isso documenta um ponto crítico: sem manutenção adequada e sem substituição tempestiva de tecnologia já reconhecida como problemática, o sistema de controle pode aparentar normalidade ao operador enquanto a condição real do processo é outra. [6][10][11][1]

**Conhecimentos avaliáveis**

- (fácil) Explicar por que a interface água-óleo precisa ser controlada em um separador com saídas segregadas de óleo e água.
  Resposta essencial: A resposta deve afirmar que o objetivo do controle é evitar contaminação cruzada entre as correntes, impedindo que óleo siga para a linha de água e que água siga para a linha de óleo.
  Critérios: Menciona explicitamente as duas direções de contaminação cruzada ou equivalente semântico.; Relaciona a interface à função de segregação das correntes líquidas, e não apenas à indicação de nível.; Não introduz critérios não documentados, como limites de descarte ou especificações comerciais, sem apoio no material.
  Condições do enunciado: Informar que o vaso possui retirada segregada de óleo e água.; Contextualizar que se trata de separador em operação.; Separador com retirada segregada de água e óleo
- (média) Comparar por que a medição de interface fica mais difícil em serviço real do que em um tanque de líquido com condições estáveis.
  Resposta essencial: A resposta deve explicar que, em serviço real, há água, óleo, gás, sólidos, espuma, emulsão e turbulência, o que torna a interface menos definida e desafia a medição. Deve também indicar que métodos dependentes de densidade, como diferencial de pressão, perdem confiabilidade quando a densidade varia com a temperatura.
  Critérios: Distingue medição em condições ideais de líquido estável versus separador multifásico perturbado.; Cita espuma e emulsão como fatores que tornam a interface difusa ou mal definida.; Cita a dependência da densidade nos métodos hidrostáticos e a influência da temperatura.; Não afirma desempenho absoluto de tecnologias não documentadas.
  Condições do enunciado: Informar que o separador opera com mistura multifásica e turbulência.; Se mencionar DP, indicar que se trata de método baseado em densidade.; Escoamento multifásico; Turbulência; Presença de espuma e emulsão; Interior do tanque ou separador com espuma e emulsão; Método de diferencial de pressão; Densidade variável com a temperatura

**Relações, proveniência e limites**

- R1 (fonte; principio; avaliável: True): O controle da interface água-óleo em separadores é necessário para evitar contaminação cruzada entre as correntes, isto é, óleo na linha de água e água na linha de óleo. [1]
  Condições: Separador com retirada segregada de água e óleo
  Limites: O material não fornece tolerâncias de arraste, metas de qualidade das correntes nem setpoints operacionais.
- R2 (fonte; principio; avaliável: True): Em presença simultânea de água, óleo, gás, sólidos, espuma e emulsão sob turbulência, a medição confiável de nível/interface fica dificultada, e instrumentos eficazes em tanques de líquido podem não operar de forma confiável nessas condições. [2]
  Condições: Escoamento multifásico; Turbulência; Presença de espuma e emulsão
  Limites: O material não compara quantitativamente todas as tecnologias de mercado nessas mesmas condições.
- R3 (fonte; principio; avaliável: True): Quando há espuma e emulsão, a interface água-óleo deixa de estar perfeitamente definida, o que dificulta sua medição. [3]
  Condições: Interior do tanque ou separador com espuma e emulsão
  Limites: O material não apresenta método documental para determinar uma interface 'verdadeira' nessas condições.
- R4 (fonte; principio; avaliável: True): A medição de nível por diferencial de pressão depende de densidade conhecida e geralmente constante; quando a temperatura varia continuamente e altera a densidade do fluido, a confiabilidade do método fica comprometida, exigindo recálculo contínuo da densidade. [4][5]
  Condições: Método de diferencial de pressão; Densidade variável com a temperatura
  Limites: O material não fornece uma estratégia documental completa de compensação nem desempenho residual após compensação.
- R5 (fonte; estudo; avaliável: False): Medidores de interface tipo empuxo instalados em standpipe tiveram, no histórico citado pela ANP, alta tendência à descalibração, erros de medição, retardo de resposta e alta frequência de manutenção. [6]
  Condições: Medição de interface onshore e offshore; Instrumento tipo empuxo instalado em standpipe
  Limites: A evidência recuperada é específica para esse tipo e instalação; não permite rejeitar toda instrumentação por empuxo em qualquer configuração sem documentação adicional.
- R6 (fonte; estudo; avaliável: False): Relatórios internos citados no relatório da ANP recomendaram descontinuar e não utilizar medidor tipo empuxo para medição de interface água/óleo, além de estudar melhores soluções tecnológicas para SGs e TOs. [7]
  Condições: Medição de interface água/óleo em SGs e TOs
  Limites: O material recuperado não traz o conteúdo integral do estudo comparativo entre alternativas.
- R7 (fonte; procedimento_local; avaliável: False): No outlet vessel do SSAO, a medição nucleônica de interface usa atenuação de raios gama; sensores perfilados captam sinal correspondente à densidade do meio, o sistema o compara com uma tabela previamente carregada, determina a posição da interface e converte a medida para 4 a 20 mA. [8]
  Condições: SSAO; Outlet vessel
  Limites: O material descreve o princípio e a implementação local, mas não informa erro, resposta dinâmica, disponibilidade ou carga de manutenção dessa aplicação.
- R8 (fonte; estudo; avaliável: False): No sistema Troll Pilot, tanto o detector nucleônico quanto o indutivo detectavam emulsões, mas apenas o nucleônico localizava a interface óleo-água e os sólidos no fundo do vaso. [9]
  Condições: Sistema de separação submarina Troll Pilot
  Limites: Resultado reportado para o sistema descrito; não demonstra por si só a incapacidade geral de toda tecnologia indutiva em qualquer vaso de FPSO/FSO.
- R9 (deducao; incidente; avaliável: False): A confiabilidade do controle de interface pode ser degradada por manutenção inadequada e por atraso na substituição de tecnologia reconhecidamente problemática, como documentado na P-53. [6][10][11]
  Condições: FPU P-53; Redução de pessoal a bordo; Ausência de plano de manutenção periódica associado; Prazos incompatíveis com a urgência da substituição; Medição de interface onshore e offshore; Instrumento tipo empuxo instalado em standpipe
  Limites: A documentação recuperada não quantifica a degradação de confiabilidade nem define periodicidades corretas de manutenção para outras unidades.; A evidência recuperada é específica para esse tipo e instalação; não permite rejeitar toda instrumentação por empuxo em qualquer configuração sem documentação adicional.
- R10 (fonte; incidente; avaliável: False): Quando a medição de interface é afetada por problemas operacionais, o valor exibido ao operador pode permanecer aparentemente dentro da faixa enquanto não representa a condição real do processo. [1]
  Condições: P-53; Momento do acidente; Medidor de interface com problemas operacionais
  Limites: A evidência recuperada é de um caso de incidente e não define frequência, mecanismo detalhado de falha nem regra geral para todos os instrumentos.
- R11 (parametrico; principio; avaliável: False): Contribuição paramétrica: quanto menos nítida a transição entre água e óleo e quanto mais variável for a densidade aparente na zona de interface, mais difícil é converter o sinal do instrumento em uma posição única e estável de interface para controle. [2][5][3][8]
  Condições: Zona de interface com emulsão, espuma ou turbulência; Propriedades locais variáveis
  Limites: É uma explicação do modelo; não foi demonstrada quantitativamente nos trechos recuperados.

**Lacunas e restrições para a avaliação**

- Os materiais recuperados não trazem comparação documental aplicável a FPSO/FSO com outras tecnologias usuais de medição de interface, como radar guiado, capacitivas, ultrassônicas ou arranjos multivariáveis.
- Faltam dados quantitativos de desempenho em campo para cada princípio, como erro, tempo de resposta, disponibilidade, sensibilidade à emulsão e esforço de manutenção.
- Não há critérios documentais de setpoint, banda de controle, filosofia de fallback operacional ou estratégia de validação cruzada quando a interface fica indefinida.

**Correções de terminologia/conceito em relação às fontes**

-  → : 

**Fontes**

1. regis: 14919_PFC-20122-PriscilaLucasAntunes.pdf: "Outro fator importante a se calcular no separador é a interface água-óleo. Essa interface deve ter controlada para que não ocorra entrada de óleo na linha de água ou entrada de água na linha de óleo."
2. regis: 14919_PFC-20122-PriscilaLucasAntunes.pdf: "A presença de água, óleo, gás, sólidos, espuma e uma emulsão (água - óleo) sob turbulência desafia os melhores instrumentos de detecção de nível encontrados atualmente."
3. regis: 14919_PFC-20122-PriscilaLucasAntunes.pdf: "essa interface não se encontra perfeitamente definida. Dentro do tanque há a criação de espulma e emulsão que dificultam a medição desta interface."
4. regis: 14919_PFC-20122-PriscilaLucasAntunes.pdf: "Como exemplo, pensamos na medição de nível por diferencial de pressão, calculada através da densidade, gravidade e altura. Esse método funciona quando sabemos precisamente a densidade, em processos onde geralmente essa densidade é constante."
5. regis: 14919_PFC-20122-PriscilaLucasAntunes.pdf: "O problema está no fato de que a temperatura do fluído esta constantemente variando, variando assim a densidade. Para utilização de métodos que dependem da densidade, teriamos que calculá-la constantemente através dos dados de temperatura."
6. anp: Relatório de investigação do acidente de descarga de óleo ocorrida em P-53 em 24/3/2019 p.36 (BR): "problemas sérios no histórico deste tipo de instrumento instalado em standpipe, que foi considerado o pior medidor. Entre os problemas destacados naquele relatório estão: alta tendência a descalibração, erros de medição, retardo da resposta e alta frequência de manutenção."
7. anp: Relatório de investigação do acidente de descarga de óleo ocorrida em P-53 em 24/3/2019 p.36 (BR): "O relatório recomendou a descontinuação do uso deste tipo de instrumento para medição de interface. O Relatório do Grupo de Trabalho para Definição de Critérios para Utilização das Tecnologias de Medição de Nível de Interface 1, de 2011, também já recomendava “ não utilizar medidor tipo empuxo” para medição de interface água/óleo."
8. regis: BPP_2011_5_2_08_Sistema_piloto1.pdf: "O sinal captado pelos sensores perfilados corresponde à densidade do meio em que estão imersos. Este sinal, comparado com valores de uma tabela previamente carregada, indica a posição do nível de interface. Esta medida é transformada em sinal elétrico por meio de loop de corrente de 4 a 20mA"
9. regis: 9616_TCC_Priscilla_Reis_completo.pdf: "Os dois sistemas funcionam separadamente e são controlados por linhas independentes. Ambos captam a presença de emulsões, contudo só o detector de nível nucleônico pode localizar a interface óleo-água e os sólidos no fundo do vaso."
10. anp: Relatório de investigação do acidente de descarga de óleo ocorrida em P-53 em 24/3/2019 p.36 (BR): "Houve um plano de redução do quantitativo de pessoal a bordo em 2013. Como parte desse plano, algumas manutenções preventivas foram substituídas por verificações a serem realizadas pela equipe de Operação, como parte de rotina operacional , sem um plano de manutenção periódica associado."
11. anp: Relatório de investigação do acidente de descarga de óleo ocorrida em P-53 em 24/3/2019 p.36 (BR): "os prazos mostraram-se incompatíveis com a urgência da medida de substituição do tipo de medidor de interface para a FPU P-53."

<sub>Nota 567fdce5c3:a04:k1 · revisão: corrigir · correcao_tecnica=4, suporte=4, pertinencia=5, riqueza=4 · 719 palavras</sub>

## a05 · segregação e gerenciamento de slops, drenagens, resíduos oleosos e água de lavagem

_Sem material nos corpora que sustente uma nota técnica. Assunto marcado para geração **sem contexto**._

## a06 · operação de bombas, válvulas, manifolds e redes de transferência

### Alinhamento real de headers, slops e rotas temporárias: por que o fluido nem sempre segue o caminho pretendido

_Em operação de tanques de carga e slop de FPSO, a transferência real entre compartimentos depende da malha que está efetivamente comunicante naquele momento, e não apenas do alinhamento pretendido no procedimento. Os documentos mostram que headers de fundo, linhas de stripping, drenos, linha de secagem de gás inerte e conexões temporárias podem formar caminhos alternativos; ao mesmo tempo, válvulas sem estanqueidade, vazamento interno e comunicação entre tanques podem drenar, recircular ou migrar conteúdo para destinos não desejados. Esse redesenho do circuito pode viabilizar manutenção e contingência, mas também inviabilizar esgotamento, contaminar outros tanques ou gerar vazamento se o isolamento e a gestão de mudança forem insuficientes._

**O que é e para que serve.** O conceito aqui é distinguir rota nominal de rota real. A rota nominal é a que o arranjo ou a manobra pretendem usar. A rota real é o conjunto de caminhos pelos quais o fluido pode efetivamente escoar, considerando headers, válvulas, linhas auxiliares, drenos e quaisquer comunicações existentes. No material, o projeto do FPSO previa que os líquidos produzidos destinados ao armazenamento fossem inicialmente para os tanques 2C e 3C, sendo depois redistribuídos aos demais por meio dos headers no fundo dos tanques. Isso mostra que o roteamento entre tanques dependia estruturalmente desses coletores, e não apenas de uma conexão direta tanque-bomba-tanque. [1]

**Princípio de funcionamento e mecanismo.** O mecanismo principal documentado é simples: se existe comunicação indevida entre tanques ou perda de estanqueidade nas barreiras hidráulicas, a bomba passa a alimentar uma rede diferente daquela imaginada pela operação. No Cidade de São Mateus, as tentativas de esvaziar os slops e o tanque 6C com a bomba de stripping foram infrutíferas porque havia comunicação entre os tanques de slop e entre o slop de bombordo e o tanque 6C. Em 11/02, a dificuldade de bombeio foi atribuída provavelmente à falta de estanqueidade das válvulas ou a vazamento interno nas linhas. [2][3]

**Princípio de funcionamento e mecanismo** _(conhecimento técnico geral, não extraído das fontes)_: Contribuição paramétrica: em termos hidráulicos, a bomba impõe energia ao sistema, mas a vazão útil se distribui pelos caminhos disponíveis; se surgem caminhos parasitas, parte do fluido recircula, reequilibra nível entre compartimentos ou retorna por contrafluxo, reduzindo o esgotamento líquido do tanque-alvo.

**Variáveis e condições operacionais.** Os documentos destacam três grupos de variáveis que mudam o caminho real da transferência. Primeiro, a topologia ativa da rede: header central, header de boreste, headers de fundo, linha de stripping, linha de secagem de gás inerte, linha de COW e drenos. Segundo, a qualidade do isolamento: suspeita de passagem em válvulas, problemas em acoplamentos Dresser e vazamento interno nas linhas. Terceiro, os alinhamentos temporários criados para contingência ou manutenção. O material registra proposta de destinar produção ao tanque 6C usando linha de secagem de gás inerte fora de uso; desvio de drenos fechados para o tanque 4C via mangote flexível conectado à linha de COW; e retorno posterior dos drenos aberto e fechado ao slop bombordo quando seu isolamento foi liberado. Esses exemplos mostram que a malha operacional ativa podia diferir substancialmente da malha usual. [4][5][6][7]

**Princípio de funcionamento e mecanismo.** Há uma diferença importante entre rota segregada e rota improvisada por contingência. Para esvaziar o slop bombordo, o relatório em inglês registra alinhamento com a válvula OP-038 em linha separada dos headers que continham válvulas defeituosas. Também registra que, para transferir o slop bombordo ao tanque 6C, toda a transferência podia ser feita em linha, dentro do tanque e da casa de bombas, pelas válvulas OP-038, OP-071, OP-079 e OP-085, sem necessidade da linha de secagem de gás inerte. Em contraste, também existia uma linha temporária preparada no convés principal para mover produção diretamente ao 6C, usando trechos de tubulação, válvulas e isolamento mecânico; e, no dia 11/02, diante da dificuldade de bombeio, adotou-se outra estratégia usando o header de sucção de boreste e a linha de gás inerte para transferir o fluido do 6C para o 2C sem a devida MOC. [8][9][10][11]

**Decisões, ações e critérios.** O material mostra que o mesmo princípio pode ser usado de forma benéfica ou perigosa. De forma benéfica, a campanha de troca de seat rings iniciada pela casa de bombas permitiu criar rotas para o fluxo de condensado e isolar partes do sistema, viabilizando intervenções e manutenção. Também foi registrada substituição de seat rings por Viton para prevenir migração de condensado pelos headers de fundo. De forma perigosa, a alteração do circuito pode criar drenagem indevida ou vazamento. No Cidade de São Mateus, recomendou-se evitar o uso do header de fundo de bombordo para transferir carga enquanto o slop bombordo não estivesse consertado, porque a carga drenaria para esse tanque. Na P-48, uma manobra de alinhamento não usual, prevista apenas para parada prolongada dos vasos de slop, resultou em vazamento de fluido combustível. [12][13][14][15]

**Decisões, ações e critérios** _(conhecimento técnico geral, não extraído das fontes)_: Contribuição paramétrica: ao avaliar uma rota temporária ou alterada, não basta perguntar se existe um caminho possível para o fluido. Também importa identificar quais compartimentos ficam comunicantes, em que sentido o fluxo pode inverter e quais barreiras permanecem confiáveis.

**Segurança e riscos.** Quando se usa linha temporária ou linha originalmente fora de serviço para transferir líquido entre tanques, o problema não é só estabelecer passagem, mas evitar contrafluxo e contaminação de outros tanques. No caso documentado, foi instalada válvula de retenção na linha temporária, que era a linha de secagem de gás inerte, para impedir contrafluxo durante o uso da bomba de stripping e evitar que o conteúdo do slop bombordo seguisse para os tanques 2C a 5C. O trecho complementar do relatório também reforça que o isolamento na região da OP-084 era considerado necessário porque havia possibilidade de o condensado migrar para o slop bombordo pelos problemas das válvulas do sistema de armazenamento. [16]

**Segurança e riscos** _(conhecimento técnico geral, não extraído das fontes)_: Contribuição paramétrica: retenção local ajuda contra um sentido específico de refluxo, mas não elimina comunicação por outros ramais nem substitui a estanqueidade exigida nas válvulas restantes da rede.

**Problemas típicos, sintomas e causas.** Para diagnóstico operacional, a dificuldade de esgotamento não pode ser lida automaticamente como falha da bomba. Os documentos sustentam investigar também hipóteses de sistema hidraulicamente mal segregado quando existe histórico de comunicação entre tanques, passagem em válvulas e uso de rotas alteradas. Isso é coerente com as tentativas frustradas de esvaziar os slops e o 6C, com o registro de migração entre tanques 2C a 5C e com a atribuição provável da dificuldade de bombeio à falta de estanqueidade ou vazamento interno. Os trechos complementares ainda registram problema de passagem de gás entre os tanques 3C e 6C na entrada da linha de gás inerte e que o problema de comunicação entre os slops não foi adequadamente migrado em passagem de serviço. [2][4][3]

**Conhecimentos avaliáveis**

- (fácil) Explicar por que um tanque pode não esvaziar como esperado com a bomba de stripping em operação quando há comunicação entre tanques ou perda de estanqueidade em válvulas/linhas.
  Resposta essencial: Porque a bomba não define sozinha o destino do fluido. Se houver comunicação entre tanques, passagem em válvulas, vazamento interno em linhas ou conexões com fuga, o sistema deixa de estar segregado. Assim, parte do conteúdo pode migrar para outro compartimento, recircular ou retornar pela rede, reduzindo a vazão útil para o destino pretendido e tornando o esgotamento ineficiente mesmo com a bomba funcionando.
  Critérios: menciona comunicação entre tanques e/ou perda de estanqueidade em válvulas/linhas; relaciona essa condição à migração, recirculação, retorno ou reequilíbrio do fluido; explica que a baixa efetividade de esgotamento não prova, por si só, defeito da bomba
  Condições do enunciado: informar que a bomba de stripping está operando; indicar histórico ou suspeita de comunicação entre tanques e/ou passagem por válvulas/linhas; mostrar que o tanque não está esvaziando como esperado; tanques comunicantes por falha ou por arranjo indevido; tentativa de esvaziamento com bomba de stripping; tanques ligados à mesma rede de linhas ou headers; barreiras hidráulicas com perda de estanqueidade; bomba em operação com baixa efetividade de transferência; histórico de comunicação entre tanques ou passagem em válvulas/linhas

**Relações, proveniência e limites**

- R1 (fonte; principio; avaliável: False): No arranjo documentado, o roteamento entre tanques de carga dependia dos headers de fundo, porque a produção só podia ser encaminhada inicialmente aos tanques 2C e 3C e depois redistribuída aos demais por esses headers. [1]
  Condições: arranjo de projeto do FPSO Cidade de São Mateus para armazenamento em tanques de carga
  Limites: descreve o arranjo daquele FPSO; não define arquitetura universal de todos os FPSO/FSO
- R2 (fonte; principio; avaliável: True): Comunicação indevida entre tanques pode tornar infrutífero o esvaziamento por bomba de stripping, porque o conteúdo deixa de permanecer segregado no tanque que se quer esgotar. [2]
  Condições: tanques comunicantes por falha ou por arranjo indevido; tentativa de esvaziamento com bomba de stripping
  Limites: o caso documentado envolve especificamente os slops e o tanque 6C; o material não quantifica vazões nem grau de comunicação
- R3 (fonte; principio; avaliável: True): Passagem em válvulas, vazamento interno em linhas e problemas em acoplamentos podem criar migração de conteúdo entre tanques e alterar o trajeto real da transferência. [4][3]
  Condições: tanques ligados à mesma rede de linhas ou headers; barreiras hidráulicas com perda de estanqueidade
  Limites: os documentos registram suspeita ou probabilidade para alguns componentes; não identificam todos os pontos de passagem
- R4 (fonte; procedimento_local; avaliável: False): Linhas não dedicadas ou temporárias podem ser usadas para desviar produção ou transferir conteúdo entre tanques quando a rota normal está indisponível ou quando se busca viabilizar manutenção. [6][12][17][9]
  Condições: existência de contingência operacional ou manutenção; adaptação física com linha temporária ou linha fora de uso
  Limites: os exemplos são do Cidade de São Mateus; não constituem autorização geral para reutilizar qualquer linha de utilidade
- R5 (deducao; principio; avaliável: False): Ao criar rota temporária, pode ser necessário adicionar retenção e isolamento para evitar contrafluxo e migração do conteúdo para tanques não pretendidos. [16]
  Condições: uso de linha temporária para stripping ou transferência; risco de refluxo para outros tanques
  Limites: o suporte documental mostra medidas específicas no Cidade de São Mateus; não demonstra suficiência universal de uma válvula de retenção isoladamente
- R6 (fonte; procedimento_local; avaliável: False): Se um header permanecer comunicado com um compartimento defeituoso, usar esse header para transferir carga pode drenar a carga para o compartimento indesejado. [15]
  Condições: slop bombordo não consertado; uso do header de fundo de bombordo para transferir carga
  Limites: instrução local ao defeito e ao arranjo documentados no Cidade de São Mateus
- R7 (fonte; procedimento_local; avaliável: False): Desviar drenos para outro tanque por mangote flexível e linha de COW muda materialmente o destino dos fluidos e amplia a malha de comunicação entre sistemas. [18][7]
  Condições: indisponibilidade dos tanques de slop; instalação de mangote flexível conectado à linha de COW
  Limites: o material registra o desvio e o destino, mas não detalha todos os controles adicionais de integridade e monitoramento
- R8 (fonte; procedimento_local; avaliável: False): A condição de vedação das válvulas dos headers de fundo é determinante do roteamento real, a ponto de a troca de seat rings ter sido adotada para prevenir migração de condensado para os tanques. [13]
  Condições: migração de condensado pelos headers de fundo; campanha de troca de seat rings
  Limites: o trecho mostra a finalidade da ação corretiva, mas não fornece desempenho quantitativo antes/depois
- R9 (deducao; principio; avaliável: True): Em um sistema com histórico de comunicação entre tanques e perda de estanqueidade, dificuldade de bombeio deve ser investigada também como problema de caminho hidráulico não controlado, e não apenas como falha da bomba. [2][4][3]
  Condições: bomba em operação com baixa efetividade de transferência; histórico de comunicação entre tanques ou passagem em válvulas/linhas; tanques comunicantes por falha ou por arranjo indevido; tentativa de esvaziamento com bomba de stripping; tanques ligados à mesma rede de linhas ou headers; barreiras hidráulicas com perda de estanqueidade
  Limites: não autoriza diagnóstico único; bomba, alinhamento e demais componentes ainda precisam ser verificados no caso concreto; o caso documentado envolve especificamente os slops e o tanque 6C; o material não quantifica vazões nem grau de comunicação; os documentos registram suspeita ou probabilidade para alguns componentes; não identificam todos os pontos de passagem
- R10 (fonte; incidente; avaliável: False): Manobras de alinhamento não usuais, mesmo previstas apenas para condição excepcional, podem abrir caminhos de vazamento não presentes na operação rotineira. [14]
  Condições: alinhamento não usual; rota excepcional prevista somente para situação específica
  Limites: é uma lição de incidente da P-48; não define por si só procedimento geral nem identifica todos os mecanismos causais

**Lacunas e restrições para a avaliação**

- O material recuperado ainda não traz o P&ID completo no corpo desta consulta para mapear, com precisão visual, todos os caminhos simultâneos entre headers de fundo, slops, 6C, linha de gás inerte, COW e drenos.
- Não há no material recuperado critérios quantitativos de aceitação para estanqueidade interna, taxa admissível de passagem ou limites operacionais de pressão/vazão para essas manobras temporárias.

**Correções de terminologia/conceito em relação às fontes**

-  → : 
-  → : 

**Fontes**

1. anp: Relatório final da investigação do FPSO Cidade de São Mateus p.121 (BR): "De acordo com o projeto da plataforma, os produtos líquidos produzidos a ser em armazenados nos tanques de carga proveniente da produção só poderiam ser destinado s para os tanques 2C e 3C e, posteriormente, para os demais com o uso dos headers no fundo dos tanques"
2. anp: Resumo técnico executivo do Relatório de Investigação do incidente de explosão ocorrido no FPSO Cidade de São Mateus em 11/02/2015 p.21 (BR): "Tentativas anteriores de esvaziar os ta nques de slop de boreste e 6C (desde novembro de 2014) com o uso da bomba de stripping demonstraram-se infrutíferas devido à comunicação entre os tanques de slop e entre o tanque de slop de bombordo e o tanque 6C."
3. regis: 14661_merged.pdf: "Em função da dificuldade de bombeio, provavelmente devido à falta de estanqueidade das válvulas ou vazamento interno nas linhas"
4. anp: Relatório final da investigação do FPSO Cidade de São Mateus p.121 (BR): "os tanques 2C, 3C, 4C e 5C possuíam suspeita de problemas de passagem nas suas válvulas e nos seus acoplamentos Dresser – junta elástica que permite a união de tubos de ponta lisa, dispensando flange, solda ou rosca e absorve vibrações, pequenos movimentos axiais e ang ulares. Este problema levava à migração de conteúdo entre os tanques."
5. anp: Relatório final da investigação do FPSO Cidade de São Mateus p.138 (BR): "Em 04/08/2014, os drenos fechado e aberto que estavam alinhados para o tanque slop boreste, devido ao isolamento do tanque slop bombordo, puderam ser retornados ao alinhamento normal, ou seja, para o tanque slop bombordo."
6. anp: Relatório final da investigação do FPSO Cidade de São Mateus p.121 (BR): "Assim, essa solicitação era para que a produção pudesse ser destinada para o tanque 6C utilizando uma linha de secagem de gás inerte que estava fora de uso no deck principal da plataforma e outras adaptações."
7. anp: Relatório final da investigação do FPSO Cidade de São Mateus p.178 (BR): "The closed drains from process were diverted to 4C via flexible hose connected to the cow line."
8. regis: 14661_merged.pdf: "optou-se por uma nova estratégia que seria utilizar o header de sucção de boreste (empregado para offloading10 de condensado), transferindo o fluido do tanque 6C para o tanque 2C, via linha de gás inerte, com auxílio da bomba de stripping, operação a ser realizada sem a devida Gestão de Mudança (MOC)."
9. anp: ANP Final Report FPSO (english version) p.118 (BR): "If any d ifficulties were encountered during the service inside the tanks, there would be a line ready to move production directly to 6C tank with the aid of a temporary alignment."
10. anp: ANP Final Report FPSO (english version) p.118 (BR): "For emptying the port slop tank, would be used to pump stripping with alignment with OP -038, located in-line separate from the headers that contain faulty valves."
11. anp: ANP Final Report FPSO (english version) p.118 (BR): "Then, for emptying the slop tank port to the tank 6C, it was not necessary the use of inert gas drying line, for the entire transfer would be in line inside the tank and pump house using valves OP - 038, OP -071, OP -079 e OP -085."
12. anp: Relatório final da investigação do FPSO Cidade de São Mateus p.128 (BR): "Essa campanha foi iniciada pelo interior da casa de bombas, dando a possibilidade para o pessoal de bordo de criar rotas para o fluxo de condensado e isolar partes do sistema, sendo assim possível executar intervenções e outras atividades regulares de manutenção."
13. anp: Relatório final da investigação do FPSO Cidade de São Mateus p.128 (BR): "a fim de prevenir a migração de condensado para os tanques pelos coletores (headers) de fundo, foram trocados os selos de vedação ( seat rings) das seguintes válvulas por selos de material Viton"
14. anp: Relatório de Investigação do acidente de incêndio ocorrido na plataforma P-48 em 17/03/2016 p.10 (BR): "Ao fazer tal manobra, que não era usual e que estava prevista em procedimento apenas para situações de parada programada prolongada dos vasos de slop, ocorreu vazamento de fluido combustível pela linha 6”-P-B10H-0827 e sua migração pela lateral boreste da embarcação"
15. anp: Relatório final da investigação do FPSO Cidade de São Mateus p.178 (BR): "If the port slop tank is not fixed, avoid using the port side bottom header to transfer cargo as it will drain into the port slop tank. Use only if you have to strip any tank."
16. anp: ANP Final Report FPSO (english version) p.118 (BR): "In order to prevent a counter flow during the use of the stripping pump, or prevent the contents of the tank port slop tanks were to 2C to 5C 87, It was installed a check valve (check valve) in the temporary line (inert gas drying line)."
17. anp: Relatório final da investigação do FPSO Cidade de São Mateus p.138 (BR): "Em 15/06/2014 foi registrado o esvaziamento do tanque slop de bombordo para o tanque 6C, conforme planejado na gestão de mudança, ou seja, usando a bomba de stripping."
18. anp: Relatório final da investigação do FPSO Cidade de São Mateus p.178 (BR): "Em janeiro, houve tentativa de esvaziamento do tanque de slop de bombordo, juntamente com o slop de boreste e do tanque 6C, conforme registros de bandalho."

<sub>Nota 567fdce5c3:a06:k1 · revisão: corrigir · correcao_tecnica=4, suporte=4, pertinencia=5, riqueza=4 · 1055 palavras</sub>

## a07 · prevenção de overfilling, overflow, contaminação cruzada e entrada indevida de hidrocarbonetos em tanques de lastro

_Sem material nos corpora que sustente uma nota técnica. Assunto marcado para geração **sem contexto**._

## Combinações para questões difíceis (tipo B)

_Conceitos que interagem numa situação real; a pergunta exige integrá-los._

### Diagnóstico de água em corrente/tanque de óleo: diferenciar falha de segregação no separador de migração por caminho hidráulico indevido

**Notas:** Medição e controle da interface óleo-água em vasos e separadores: criticidade, limitações de medição e efeito da manutenção na confiabilidade; Alinhamento real de headers, slops e rotas temporárias: por que o fluido nem sempre segue o caminho pretendido  
**Ligação:** A presença anormal de água em uma corrente ou tanque de óleo pode nascer em dois mecanismos tecnicamente distintos que produzem sintomas parecidos: (i) controle/medição inadequados da interface água-óleo no separador, agravados por espuma, emulsão, turbulência ou erro por densidade variável; e (ii) migração entre tanques por válvulas/linhas com perda de estanqueidade ou alinhamento real diferente do pretendido. Um mecanismo pode mascarar o outro: mesmo que a interface no separador esteja mal controlada, a evidência observada em inventário ou qualidade de um tanque pode ser amplificada, redistribuída ou mantida por comunicação indevida entre tanques; inversamente, uma suspeita inicial sobre o separador pode ser falsa se o desvio ocorrer a jusante por caminho hidráulico não controlado.  
**Raciocínio exigido:** O respondente precisa integrar a física de separação e limitações de medição da interface com a hidráulica real das rotas de tanques e headers. Só com N1 ele explicaria contaminação cruzada na origem, mas não conseguiria avaliar por que a anomalia persiste ou aparece em tanques aparentemente fora da rota. Só com N2 ele explicaria migração entre tanques, mas não conseguiria discutir a geração inicial de água na corrente de óleo nem por que um sinal de interface pode ser enganoso. A boa resposta exige construir hipóteses concorrentes, relacionar sintomas comuns e propor uma lógica de diagnóstico que não confunda falha de bomba/transferência com problema de caminho hidráulico nem atribua automaticamente toda água observada a erro de separação.  
**Cenário:** Durante uma operação rotineira, surge indicação de água onde se esperava predominantemente óleo, e ao mesmo tempo uma manobra de esgotamento/stripping de um tanque não produz a redução esperada de conteúdo. Parte da equipe atribui o problema ao controle da interface no separador; outra parte suspeita de falha da bomba ou de erro de alinhamento. O histórico recente inclui condições com emulsão/espuma no processo e também dúvidas sobre estanqueidade de válvulas/linhas entre tanques.
