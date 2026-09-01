AVISO: os trechos fornecidos não contêm informação específica sobre sequência de transferências nem sobre gestão de lastro e estabilidade hidrodinâmica do FPSO e do navio aliviador; o documento abaixo consolida apenas os aspectos disponíveis relativos a controle de fluxos, pressões e níveis durante transferência e à robustez do sistema de controle frente a perturbações (golfeadas, variações de vazão/composição, atrasos de malha).

Controle de nível e propriedades do vaso de acumulação
O controle do nível no outlet vessel e em vasos separadores é crítico para evitar arraste de líquido pela corrente gasosa e passagem de gás pela saída de líquido. O volume do vaso deve ser explorado de forma a atenuar perturbações de vazão de carga; vasos com capacidade volumétrica adequada evitam propagação imediata de flutuações para a saída. Existe trade-off entre permitir oscilações do nível (maior liberdade aumenta estabilidade da vazão de saída e capacidade de filtragem de carga) e respeitar limites que impeçam arraste ou perda de retenção de gás. Esses limites configuram a banda de atuação do controlador, definida em torno do setpoint e limitada por margem superior e inferior, conforme o conceito de controle por bandas.

Estratégias de controle e sintonia
A filosofia adotada para o sistema descrito é um controlador PI (proporcional-integral) com sintonia baseada na metodologia proposta por Skogestad. Em estudos complementares foi testado controlador com ações proporcional e derivativa; controladores com ação derivativa mal sintonizados podem reagir de forma brusca a golfeadas, imprimindo variações rápidas na válvula de controle de saída e provocando desgaste mecânico excessivo ao longo do tempo. Para preservar a qualidade do efluente e reduzir atuação excessiva na diminuição do nível de interface, foi testada a estratégia denominada Dead Band Assimétrico, na qual o sistema reage mais rapidamente a quedas de nível do que a elevações, visando proteger a qualidade da água de injeção.

Comportamento frente a golfeadas e variações
Golfeadas foram simuladas em ensaios utilizando-se tanque pressurizado para injetar gás no pipe separator; a duração e o volume das golfeadas eram controlados pelo tempo de injeção do gás. Os testes demonstraram que, sob as condições fornecidas nas bases de projeto, o sistema de controle de nível se mostrou adequadamente robusto e não apresentou variações significativas de nível de interface no outlet vessel. As perturbações aplicadas na matriz de testes incluíram parada da alimentação na entrada do pipe separator, bloqueio da saída de óleo e gás, variação em degrau de entrada água e gás, oscilação da entrada água e gás, aumento do atraso da malha de controle e golfeada a montante do pipe separator.

Requisitos de instrumentação e tempos de malha
Um objetivo central da qualificação foi assegurar que tempos de ação e retardo dos instrumentos, da malha de controle e dos meios de comunicação fossem similares aos esperados em operação real. A compatibilidade desses tempos é condição para que os algoritmos de controle e as dimensões do vaso cumpram sua função de atenuar transientes sem induzir mistura excessiva no pipe separator e no outlet vessel. Testes confirmaram que o sistema de controle associado à instrumentação é suficiente para manter o nível de interface dentro da faixa requerida tanto em condições normais quanto em flutuações de carga, vazão, pressão e composição, além de ser capaz de levar a interface ao nível requerido em transientes como partidas, paradas e flushing.

Controle por bandas aplicado a separadores bifásicos
No controle por bandas, define-se uma faixa de atuação permitida para o nível, centrada em um setpoint; o sistema permite oscilações contidas dentro dessa banda para suavizar vazões de saída, respeitando os limites que previnem arraste de líquido ou passagem de gás. A estratégia aproveita a propriedade física do vaso de armazenar carga momentaneamente, filtrando variações de entrada e evitando repassar perturbações diretamente à etapa subsequente (por exemplo, recompressão de gás).

Impactos operacionais e integridade de válvulas
Golfeadas e perturbações rápidas podem gerar comandos abruptos nas válvulas de controle, com consequente desgaste mecânico. Controladores que respondem sem amortecimento adequado (ou com ação derivativa mal calibrada) podem aumentar esse risco. Portanto, a sintonia deve equilibrar suavização das vazões de saída, limites de flutuação de nível e vida útil dos atuadores.

Dimensionamento do outlet vessel
A capacidade volumétrica do outlet vessel deve ser tal que variações rápidas e transientes nas condições de entrada não provoquem mistura excessiva nem comprometam a separação no pipe separator e no próprio outlet vessel. Os ensaios procuraram validar que as dimensões projetadas atendem à função de tamponamento requerida pelo sistema de controle.

Procedimentos de qualificação e critérios
A qualificação do sistema de controle incluiu matriz de testes representativa das perturbações previstas no projeto, verificação de resposta sob falhas e transientes e confirmação da capacidade do sistema em manter níveis de interface dentro das faixas operacionais. Critérios avaliados foram: manutenção do nível de interface na faixa requerida, capacidade de resposta em condições transientes, compatibilidade de tempos de instrumentação e controle com as condições reais e ausência de mistura excessiva que comprometa a separação.

Observações sobre bloqueios e manutenção
Ocorrência de bloqueio por acúmulo de sólidos (areia) em válvulas de rejeito foi identificada em imagens de operação e representa risco de perda de controle de vazão; tal condição exige monitoramento e procedimentos de manutenção específicos, pois pode alterar a capacidade de controle do nível e das vazões durante transferência.

Resumo técnico prático
- Dimensionar outlet vessel para oferecer tamponamento adequado a golfeadas e degraus de vazão sem induzir mistura excessiva.  
- Sintonia de controladores PI segundo metodologia de referência (ex.: Skogestad) e validação em testes que reproduzam tempos e atrasos reais de instrumentação.  
- Implementar Dead Band Assimétrico quando desejado priorizar resposta a baixa de nível para proteger qualidade do fluido e reduzir atuações desnecessárias.  
- Aplicar controle por bandas para permitir oscilações controladas do nível, aumentando estabilidade da vazão de saída dentro de limites que evitem arraste ou passagem de gás.  
- Monitorar desgaste de válvulas e impacto de golfeadas na atuação de controle; evitar derivações de sintonia que gerem comandos abruptos.  
- Incluir ensaios de bloqueio e falha na matriz de qualificação e prever rotinas de manutenção para obstruções (ex.: areia).