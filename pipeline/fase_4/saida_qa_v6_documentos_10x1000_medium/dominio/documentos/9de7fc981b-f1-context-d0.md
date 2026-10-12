# Controle metrológico da medição fiscal em operação de FPSO

## 1. Finalidade metrológica e contexto operacional no FPSO
**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:3299121.0-3299193.0`, `petroles-4ee4bce16acf674505c8912d:pNone:1658059.0-1658092.0`

Em um FPSO, a medição fiscal não é apenas uma variável de processo: ela sustenta transferência de custódia, apuração de produção, participações governamentais e rastreabilidade dos volumes produzidos. Por isso, o regulamento citado nos trechos da ANP/INMETRO enquadra **projeto, instalação, operação, teste e manutenção** dos sistemas de medição que realizam medições fiscais e medições operacionais de petróleo, gás natural e água.

Sob a ótica operacional, a **confiabilidade metrológica** de uma medição fiscal em serviço depende de a unidade manter, ao mesmo tempo:

- tecnologia de medição apropriada ao fluido e à faixa operacional;
- instalação compatível com o sistema de transferência;
- instrumentos auxiliares confiáveis para compensações e correções;
- calibração/proving rastreável e representativa das condições reais de operação;
- registros íntegros dos fatores de correção e dos cálculos que levam ao volume apurado.

Em termos práticos, um medidor fiscal em um FPSO pode estar “funcionando” do ponto de vista de automação, mas ainda assim **não ser metrologicamente confiável** se estiver fora do envelope de vazão, com histórico de fator do medidor instável, com compensação incorreta de temperatura/pressão, com passagem de gás pelo medidor de líquido, ou com amostragem de BS&W não representativa.

---

## 2. Conceitos operacionais e metrológicos relevantes
**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:3297971.0-3298040.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3299121.0-3299193.0`

Os trechos fornecem definições úteis para interpretar a medição fiscal em operação:

- **Medidor padrão:** medidor usado como padrão de comparação na calibração de outros medidores.
- **Provador em linha:** recipiente aberto ou fechado, de volume conhecido, usado como padrão volumétrico para calibrar medidores de petróleo.
- **Relatório de medição:** documento que informa valores medidos, fatores de correção e volume apurado em um período de medição.
- **Vazão usual de operação:** vazão média de operação avaliada desde a última calibração do sistema de medição ou desde o último teste aplicável, desconsiderando períodos sem produção.
- **Volume registrado:** variação do registro do totalizador entre o início e o fim da medição.
- **Volume efetivo:** produto do volume registrado pelo fator de calibração do medidor.
- **Volume efetivo em condições de referência:** volume efetivo corrigido para as condições de referência de pressão e temperatura.
- **Volume líquido:** volume de petróleo nas condições de referência, descontados água e sedimentos.

Essas definições mostram que a medição fiscal confiável é uma **cadeia de transformação metrológica**:

1. o medidor gera um volume registrado;
2. esse valor é ajustado pelo fator do medidor;
3. aplicam-se correções para referência de temperatura e pressão;
4. desconta-se o conteúdo de água e sedimentos;
5. documenta-se o volume líquido apurado.

Logo, a confiabilidade não está concentrada em um único equipamento; ela pertence ao **sistema de medição como um todo**.

---

## 3. Configuração mínima do sistema de medição fiscal de petróleo em linha
**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:3299370.0-3299441.0`

Para medição fiscal de petróleo em linha, o sistema deve incluir, no mínimo:

- medidor de fluido do tipo **deslocamento positivo**, **turbina** ou **mássico tipo Coriolis com indicação de volume**; outros tipos dependem de autorização prévia da ANP;
- **totalizador** sem retorno a zero, ou com proteção contra acesso não autorizado;
- **sistema de calibração** fixo ou móvel, aprovado para calibrar os medidores;
- **sistema de amostragem proporcional à vazão**, comandado por sinal de saída do medidor;
- instrumento ou sistema de **medição/compensação de temperatura**;
- instrumento ou sistema de **medição/compensação de pressão**.

Do ponto de vista de projeto e operação, o sistema deve ser concebido para:

- ser compatível com o sistema de transferência ao qual está conectado;
- impedir **refluxo** pelo medidor;
- proteger o medidor contra **transientes** e **choques de pressão**;
- impedir a passagem de **gases ou vapores** pelo medidor de líquido;
- não possuir **contorno (bypass)** do medidor fiscal.

### Consequência operacional
Esses requisitos existem porque a exatidão declarada do medidor só é válida se o escoamento e o arranjo hidráulico permanecerem dentro das hipóteses para as quais o equipamento foi projetado e calibrado. Em operação de FPSO, isso significa que alterações em bombas, válvulas de controle, backpressure, separação inadequada de gás, espuma, slugs ou mudanças de malha podem degradar a qualidade metrológica mesmo sem gerar falha evidente no sistema de supervisão.

---

## 4. Correções obrigatórias e formação do volume fiscal
**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:3299370.0-3299441.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3297971.0-3298040.0`

Os trechos indicam que as medições de petróleo em linha devem ser corrigidas, quando aplicável, por pelo menos três grupos de fatores:

1. **dilatação térmica** entre a temperatura de referência e a temperatura de medição;
2. **compressibilidade do líquido** entre a pressão de referência e a pressão de medição;
3. **conteúdo de sedimentos e água (BS&W)** no petróleo.

O cálculo do volume de líquidos medidos deve seguir norma de cálculo dinâmico de quantidades de petróleo, e os **relatórios de medição** devem conter:

- todos os valores medidos;
- todos os parâmetros e fatores usados;
- todos os cálculos realizados para chegar ao volume líquido corrigido.

### Leitura metrológica
A confiabilidade fiscal depende de duas perguntas operacionais:

- **A medição bruta foi obtida corretamente?**
- **As correções foram aplicadas com instrumentos, fatores e dados válidos?**

Um erro no termopoço, no transmissor de pressão, no densímetro auxiliar, no fator de encolhimento adotado, no teor de BS&W ou no algoritmo de compensação pode distorcer o resultado final mesmo que o medidor principal esteja bem calibrado.

### Efeito do BS&W
Como o volume líquido desconta água e sedimentos, qualquer problema de representatividade da amostragem ou do método analítico afeta diretamente a apuração do volume de petróleo. Para FPSO, isso é particularmente sensível quando há oscilação de emulsão, mudança de eficiência de separação ou alteração de origem dos poços ligados ao manifold de produção.

---

## 5. Calibração, proving e rastreabilidade em operação
**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:3299408.0-3299466.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3299370.0-3299441.0`, `regis-44b5e0f18c0eba454e5dfcf8:pNone:329.0-370.0`, `petroles-4ee4bce16acf674505c8912d:pNone:1658059.0-1658092.0`

Os trechos da ANP/INMETRO indicam que os medidores fiscais em linha devem ser calibrados em intervalos máximos definidos pelo regulamento, podendo haver ampliação mediante aprovação da ANP com base no **histórico de calibrações**. Embora os valores numéricos estejam suprimidos nos trechos, o princípio técnico é claro: a periodicidade não deve ser arbitrária; ela depende de evidência histórica de estabilidade.

### Sistemas aceitos para calibração/proving
Podem ser usados, quando aprovados:

- **provadores em linha**;
- **tanques de prova**;
- **medidores padrão (master meters)**;
- outros sistemas previamente autorizados.

### O que é o provador em linha
Um provador em linha de deslocamento mecânico consiste em um tubo calibrado de diâmetro interno conhecido, instalado em série com o medidor. Uma esfera ou êmbolo é deslocada pelo próprio fluido; ao passar por detectores, mede-se o volume deslocado entre dois pontos conhecidos. Se o medidor gera pulsos, o quociente entre a totalização de pulsos e o volume de referência define o **fator K** do medidor.

### Requisitos importantes para a validade da calibração em operação
Os trechos destacam que:

- o medidor padrão deve ser calibrado antes de ser usado para calibrar o medidor em operação;
- o fluido usado na calibração deve ter **massa específica, viscosidade e temperatura suficientemente próximas** das do fluido medido;
- a vazão de calibração deve ser igual ou muito próxima da **vazão usual de operação**;
- se um medidor padrão atender vários medidores com condições diferentes, podem ser necessárias múltiplas calibrações do padrão;
- a instalação do medidor padrão, quando usada para calibrar outro medidor, deve respeitar posição relativa a filtros, eliminadores de gás, válvulas de contrapressão e válvulas de retenção;
- provadores e tanques de calibração devem ser recalibrados periodicamente com **rastreabilidade ao INMETRO**.

### Interpretação para o FPSO
Para avaliar a confiabilidade metrológica do ponto fiscal em serviço, não basta verificar se “houve uma calibração”. É preciso verificar se a calibração foi:

- **rastreável**;
- **representativa** do fluido real;
- executada em **condições usuais de operação**;
- compatível com a faixa de vazão e com as propriedades do petróleo em produção;
- repetível, isto é, com variação aceitável do fator do medidor nos testes sucessivos.

Se uma alteração operacional muda viscosidade, temperatura, pressão, teor de gás arrastado ou regime de vazão a ponto de afetar o erro admissível, o regulamento exige nova calibração do medidor fiscal.

---

## 6. Como a incerteza entra na avaliação da confiabilidade metrológica
**Fontes:** `regis-44b5e0f18c0eba454e5dfcf8:pNone:329.0-370.0`

Os trechos técnicos do REGIS mostram que a confiabilidade metrológica pode ser analisada por meio da **incerteza combinada** do princípio de medição adotado.

### 6.1 Medidor de turbina e medidor de deslocamento positivo
Para ambos, o trecho apresenta a forma:

`Q = F / K`

onde:
- `Q` = vazão volumétrica;
- `F` = frequência/contagem de pulsos associada ao escoamento;
- `K` = fator do medidor.

A incerteza combinada depende principalmente de:

- incerteza da geração/contagem de pulsos `u(F)`;
- incerteza do fator do medidor `u(K)`.

Forma apresentada no trecho:

`u(Q) = sqrt[(1/K * u(F))² + (F/K² * u(K))²]`

#### Implicação prática
Se o fator K deriva de um proving instável, ou se há baixa geração de pulsos em determinada faixa de vazão, a incerteza cresce. Logo, confiabilidade metrológica em operação exige acompanhar a **estabilidade do K-factor** e a adequação da faixa de medição.

### 6.2 Medidor ultrassônico
O trecho apresenta, para medidor monofeixe, uma relação do tipo:

`Q = A . K . V`

com a velocidade inferida a partir dos tempos de trânsito ultrassônicos. A incerteza resulta da combinação de contribuições como:

- fator do medidor `K`;
- distância entre transdutores `d`;
- tempos de trânsito `tAB` e `tBA`;
- geometria/ângulo do feixe.

#### Implicação prática
Em medidores ultrassônicos, a confiabilidade não depende só da calibração global; depende também da integridade geométrica, da eletrônica de tempo de trânsito e da qualidade do perfil de escoamento.

### 6.3 Medidor Coriolis
O trecho relaciona a vazão volumétrica à vazão mássica e à densidade, isto é, conceitualmente:

`Qv = (dm/dt) / ρ`

e aponta que a incerteza combinada envolve variáveis internas do sensor, como frequência angular de oscilação, ângulo de torção, constante elástica, volume interno e massa do tubo sensor.

#### Implicação prática
No Coriolis, deriva mecânica do sensor, compensações eletrônicas e qualidade da densidade associada ao cálculo afetam a confiabilidade do volume indicado.

---

## 7. Instrumentos auxiliares também são parte da medição fiscal
**Fontes:** `regis-2957bf09b49f6e9e6c5ea146:pNone:7176.0-7457.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3299370.0-3299441.0`

A medição fiscal de petróleo em linha depende de instrumentos auxiliares, especialmente os usados em compensação de temperatura, pressão e, em certos arranjos, densidade.

O trecho do REGIS sobre densímetros vibracionais destaca pontos tecnicamente úteis:

- a recalibração deve ser feita, preferencialmente, nas **mesmas condições** da calibração anterior, para permitir comparação coerente dos resultados;
- é desejável usar fluidos de pureza certificada;
- quando o densímetro calcula densidade na temperatura de medição, mas não compensa adequadamente o efeito da **pressão**, pode ser necessário empregar constantes específicas fornecidas pelo fabricante ou desenvolver metodologia experimental para essa compensação;
- a rastreabilidade e a avaliação de incerteza devem seguir referências metrológicas reconhecidas, como VIM e GUM.

### Aplicação ao FPSO
Isso significa que a confiabilidade do medidor principal pode ser comprometida por um instrumento auxiliar aparentemente secundário. Por exemplo:

- transmissor de temperatura com deriva altera a correção térmica do volume;
- pressão mal medida compromete a correção de compressibilidade;
- densidade mal compensada pode degradar cálculos derivados ou verificações cruzadas.

Portanto, avaliação metrológica séria deve incluir **toda a cadeia de medição e compensação**.

---

## 8. Limitações operacionais e exemplos de degradação da confiabilidade
**Fontes:** `petroles-4ee4bce16acf674505c8912d:pNone:1658501.0-1658554.0`, `petroles-4ee4bce16acf674505c8912d:pNone:1658059.0-1658092.0`, `regis-44b5e0f18c0eba454e5dfcf8:pNone:329.0-370.0`

Os estudos fornecidos mostram exemplos de mecanismos de perda de confiabilidade metrológica.

### 8.1 Baixa vazão e provador tipo ball prover
Um estudo laboratorial com ball prover bidirecional concluiu que:

- os resultados foram satisfatórios em níveis de vazão intermediária e máxima;
- em vazão mínima, a incerteza do provador não atendeu ao recomendado;
- uma causa apontada foi a **perda do movimento contínuo da esfera**.

#### Leitura técnica
Em baixas vazões, o comportamento mecânico do elemento deslocador pode deixar de representar adequadamente o volume de referência, deteriorando repetibilidade e incerteza.

### 8.2 Pouca geração de pulsos e sensibilidade do fator K
O mesmo estudo indica que, em certas condições, a pequena quantidade de pulsos gerados pela turbina tende a piorar a confiabilidade da leitura, ampliando dispersão e erro relativo.

#### Leitura técnica
Mesmo quando a tecnologia é adequada, sua resolução efetiva pode se tornar limitada em determinadas faixas operacionais. Isso reforça a necessidade de manter o ponto fiscal na faixa para a qual o medidor foi comprovado.

### 8.3 BS&W e representatividade da amostra
O trecho do REGIS lembra que o BS&W instantâneo pode diferir do valor médio, e que a representatividade da amostragem é fundamental. Em FPSO, onde emulsão e regime de produção variam com o alinhamento de poços e separadores, esse aspecto é crítico para o volume líquido fiscal.

### Observação importante
Esses estudos ilustram mecanismos reais, mas não devem ser transformados automaticamente em regra universal para todo FPSO. Eles servem como **exemplos de falhas plausíveis** a serem investigadas quando houver desvio metrológico.

---

## 9. Critérios práticos para julgar a confiabilidade metrológica em operação
**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:3299370.0-3299441.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3299408.0-3299466.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3297971.0-3298040.0`, `regis-44b5e0f18c0eba454e5dfcf8:pNone:329.0-370.0`

Uma avaliação profissional da confiabilidade metrológica da medição fiscal em um FPSO deve verificar, no mínimo, os seguintes pontos:

### 9.1 Enquadramento metrológico do sistema
- O arranjo é compatível com o tipo de medição fiscal executada?
- O sistema contém medidor, totalização protegida, amostragem, pressão, temperatura e sistema de calibração apropriados?
- Não existe bypass indevido, refluxo ou possibilidade de passagem de gás/vapor pelo medidor de líquido?

### 9.2 Representatividade das condições de calibração
- O proving foi feito com o **mesmo fluido** ou com fluido suficientemente similar?
- Pressão, temperatura, viscosidade, massa específica e vazão estavam próximas das condições usuais de operação?
- O medidor padrão ou provador tinha calibração rastreável vigente?

### 9.3 Estabilidade do medidor
- O fator do medidor mostra histórico estável entre provas sucessivas?
- Houve mudança operacional capaz de alterar o erro além do admissível?
- O medidor continua operando dentro dos limites do fabricante?

### 9.4 Integridade das correções
- Temperatura e pressão usadas nas correções são medidas por instrumentos confiáveis?
- O conteúdo de água e sedimentos é determinado por amostragem representativa e método controlado?
- Os cálculos e fatores de correção estão devidamente registrados no relatório de medição?

### 9.5 Resposta a desvios
Se qualquer um desses elementos perder validade, a consequência operacional correta não é “aceitar o valor com ressalva” de forma informal. O adequado é tratar a condição como **redução de confiança metrológica**, avaliar necessidade de nova calibração, ajuste, inspeção do sistema de amostragem, revisão das condições de operação e eventual limitação do uso fiscal até restabelecimento da conformidade metrológica, conforme procedimentos da instalação e exigências regulatórias aplicáveis.

---

## 10. Complemento: confiabilidade metrológica na medição fiscal de gás
**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:3299568.0-3299633.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3299121.0-3299193.0`

Embora o foco principal desta faceta seja a medição fiscal em operação, os trechos também mostram princípios úteis para correntes gasosas do FPSO:

- medidores de gás devem ser calibrados segundo critérios normativos aplicáveis e com periodicidades máximas definidas pelo regulamento;
- instrumentos de **pressão** e **temperatura** usados para compensação devem manter exatidão compatível com a incerteza total requerida;
- em medições com **placa de orifício**, os instrumentos de pressão diferencial, pressão estática e temperatura devem ser calibrados e ajustados se ficarem fora dos limites;
- placas de orifício fiscais devem ser inspecionadas periodicamente quanto às tolerâncias dimensionais;
- trechos de medição também devem ser inspecionados para verificação de dimensões e rugosidade interna;
- nos pontos fiscais de produção de gás natural, devem ser coletadas amostras para análise de composição, massa específica, poder calorífico, inertes e contaminantes, podendo haver analisadores em linha calibrados por comparação com laboratório.

### Relevância para a confiabilidade
Em gás, a confiabilidade metrológica depende ainda mais da **qualidade das variáveis de compensação** e da **composição**. Um medidor de vazão bem calibrado pode produzir resultado fiscal ruim se a pressão, a temperatura ou a composição do gás estiverem mal determinadas.

---

## 11. Síntese operacional
**Fontes:** todas as acima

Em um FPSO, a medição fiscal confiável é o resultado da combinação de:

- medidor adequado à aplicação;
- instalação hidráulica correta;
- eliminação de gás/vapor e de refluxo;
- operação dentro da faixa comprovada;
- calibração/proving representativos da condição real;
- rastreabilidade metrológica dos padrões;
- correções corretas de temperatura, pressão/compressibilidade e BS&W;
- instrumentos auxiliares íntegros;
- documentação completa e auditável.

Assim, **avaliar a confiabilidade metrológica da medição fiscal em operação** significa verificar a robustez da cadeia inteira de medição, e não apenas confirmar que o indicador do medidor está variando ou que a última calibração existe em arquivo.