# Perguntas e respostas

## 1. Fácil

Quais condições elétricas são necessárias para sincronizar um gerador com um barramento energizado?

**Resposta:** Sequência de fases compatível, tensão próxima à do barramento, frequência muito próxima e ângulo de fase adequado no instante do fechamento do disjuntor.

## 2. Fácil

Qual arranjo de turbina a gás tende a oferecer melhor estabilidade transitória de frequência e menor risco de overspeed após perda de carga na geração elétrica?

**Resposta:** O arranjo de eixo único.

## 3. Fácil

Como varia a potência reativa de um cabo submarino em corrente alternada com o comprimento e a tensão operacional?

**Resposta:** Ela aumenta com o comprimento do cabo e com o quadrado da tensão operacional.

## 4. Média

Em uma partida direta de um motor de grande porte em barramento energizado, qual é o efeito imediato sobre corrente, tensão e demanda reativa do sistema?

**Resposta:** A corrente sobe fortemente, ocorre queda transitória de tensão e a demanda de potência reativa fica elevada durante a aceleração.

## 5. Média

Se um grande motor está próximo da velocidade nominal e a compensação temporária de reativos permanece conectada, qual consequência tende a ocorrer no barramento?

**Resposta:** A tendência é de sobretensão no barramento.

## 6. Média

Ao fechar o bus tie entre barramentos energizados, o que muda nas correntes de falta e na coordenação das proteções?

**Resposta:** Surgem caminhos adicionais de corrente de falta, mudam os níveis de curto-circuito e a coordenação das proteções precisa ser revista.

## 7. Difícil

Dois geradores principais estavam em operação estável, sem indício dominante de problema mecânico ou de combustível. Em seguida, ambos deixaram de permanecer conectados ao sistema ao mesmo tempo em que desapareceram indicações e comandos associados aos seus painéis, sem falta primária no barramento de potência que explicasse o evento. Que mecanismo explica essa perda de geração?

**Resposta:** Perda da alimentação de comando, supervisão ou atuação dos geradores, tipicamente na malha de 24 Vcc ou UPS, deixando-os incapazes de permanecer conectados ou controláveis.

## 8. Difícil

Após blackout total, o gerador de emergência parte e fica apto a assumir carga, mas toda tentativa de fechamento do seu disjuntor termina em trip imediato. O comportamento só aparece durante a reinicialização do sistema de controle, e a condição usual de reinício por bateria não está disponível. O que explica o fracasso repetido da recomposição?

**Resposta:** Uma lógica de controle mantém sinal de trip no disjuntor do gerador de emergência durante o reboot, impedindo o fechamento mesmo com a máquina disponível.

## 9. Difícil

Dois canais previstos como redundantes perdem função quando falha um único UPS ou barramento, embora cada fonte tenha capacidade nominal para suprir toda a carga e o projeto previsse segregação entre ramos independentes. O que isso revela sobre a arquitetura implantada?

**Resposta:** A implantação perdeu segregação entre ramos: canais redundantes foram concentrados no mesmo UPS ou barramento, criando ponto único de falha e redundância apenas nominal.
