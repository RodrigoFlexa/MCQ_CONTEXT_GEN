# Queima, dispersão e impactos em sistemas de alívio e flare

## 1. Papel do flare como sistema de segurança
O sistema de flare/tocha em FPSOs é tratado no material como parte do sistema de segurança da instalação, destinado a permitir a liberação segura de gases de alívio e de despressurização quando a pressão de linhas e equipamentos pode exceder limites aceitáveis. O material também sustenta que a queima em tocha não é um recurso desejável do ponto de vista de aproveitamento energético e emissões, mas não pode ser eliminada completamente em instalações de produção porque permanece necessária para segurança de processo.

Um sistema completo de flare é descrito, de forma geral, como composto por:
- chaminé/lança;
- queimador ou flare tip;
- selo/vedações para impedir retorno de chama;
- tubulações que coletam os gases a serem queimados;
- recipiente na base para remoção e armazenamento de líquidos provenientes do fluxo de gás;
- chama piloto mantida continuamente acesa para ignição imediata quando houver descarte ou alívio.

O material também indica que uma mesma instalação pode possuir sistemas de alta pressão (HP) e baixa pressão (LP), para cobrir diferentes faixas de vazão e condições operacionais. De modo qualitativo, o LP atende correntes de baixa pressão, próximas da atmosférica, enquanto o HP é associado à despressurização de sistemas pressurizados e a eventos mais severos.

**Implicação para a faceta:** a confiabilidade da queima não é apenas um requisito operacional; ela é parte da função de segurança do sistema de alívio. Falha de ignição, instabilidade de chama ou dispersão inadequada de gases queimados/não queimados podem transferir o risco do equipamento protegido para a própria plataforma.

**Fontes:** `petroles-4ee4bce16acf674505c8912d:pNone:1742886.0-1742923.0`, `petroles-4ee4bce16acf674505c8912d:pNone:1742905.0-1742941.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:4261895.0-4261932.0`

## 2. Confiabilidade da queima: requisitos funcionais e mecanismos que a favorecem
O material distingue dois grandes modos de operação da tocha:
- **condições contínuas**: perda total ou parcial da capacidade de exportação de gás, mantendo-se a produção de óleo;
- **condições de emergência**: falha operacional, quebra de equipamento ou fogo na plataforma, exigindo a queima do gás proveniente da despressurização dos equipamentos de processo.

Para ambos os casos, a exigência fundamental é que a queima ocorra **de modo contínuo**, sem interrupção, inclusive sob condições atmosféricas adversas. A justificativa é direta: gás descarregado sem queima pode se espalhar pela plataforma e gerar consequências graves.

O material aponta alguns mecanismos físicos e construtivos que favorecem essa confiabilidade:
1. **Piloto permanentemente aceso**: garante ignição imediata dos gases aliviados.
2. **Baixa sensibilidade ao vento em tochas multiponto**: é citado que a descarga pode ocorrer em velocidade próxima de 0,9 Mach, da ordem de 330 m/s, muito acima de velocidades usuais de vento, o que ajuda a manter a continuidade da queima.
3. **Mistura rápida com ar**: a alta velocidade de saída torna a chama turbulenta; além disso, a subdivisão da vazão em vários pequenos fluxos favorece mistura rápida combustível-ar.
4. **Baixa perda de carga e ausência de obstruções**: o duto do flare deve funcionar como caminho de alívio confiável; obstáculos que prejudiquem essa função devem ser evitados.
5. **Remoção de líquidos e vedações contra retorno de chama**: a presença de dispositivo para retirada de líquidos na base e de vedações/selos reduz mecanismos de instabilidade e risco de retrocesso de chama.

Em termos de operação, o objetivo não é apenas manter a chama acesa, mas também buscar **queima completa**. No contexto do material, isso significa reduzir a liberação de hidrocarbonetos não queimados e minimizar a dispersão perigosa de gás inflamável ao redor da unidade.

**Fontes:** `regis-dce79d82a4a7f1760d88e146:pNone:15.60-32.0`, `petroles-4ee4bce16acf674505c8912d:pNone:1742905.0-1742941.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:4261895.0-4261932.0`

## 3. Implantação, ventos e dispersão de gases queimados ou não queimados
A definição da posição da tocha na unidade é apresentada como decisão de segurança com forte componente aerodinâmico e operacional. Os fatores explicitamente citados incluem:
- localização da planta e do sistema na planta;
- posição e área disponível para instalação;
- velocidade/direção predominante dos ventos;
- ruído;
- radiação térmica.

### 3.1 Posicionamento em relação aos ventos
O material enfatiza que a tocha não deve se tornar fonte de ignição para vazamentos na própria plataforma. Por isso, o posicionamento favorável em relação aos ventos predominantes é crítico. É citado, como prática da Petrobras, o arranjo em que os ventos predominantes passam perpendicularmente à lança, reduzindo:
- a chance de um vazamento de gás na planta ser inflamado pela tocha;
- a chance de gás eventualmente descarregado sem queima se espalhar sobre a plataforma.

### 3.2 Dispersão de gases queimados
Os gases queimados também podem gerar impactos operacionais e de segurança. O material indica que eles não devem atingir:
- áreas de trabalho, especialmente aquelas de evacuação difícil;
- tomadas de ar dos sistemas de ventilação;
- o heliponto, onde elevação súbita da temperatura do ar admitido nas turbinas do helicóptero pode reduzir potência disponível.

Em campos com presença de **H2S**, a dispersão torna-se ainda mais crítica pelo potencial letal desse contaminante. Assim, a análise de dispersão não deve ser tratada como mero tema ambiental: ela afeta ocupação segura, habitabilidade, continuidade operacional e resposta a emergências.

### 3.3 Consequência prática para projeto e modificações
Qualquer alteração de layout, novos módulos, mudanças de ventilação, novos equipamentos altos ou alterações na lança podem modificar padrões de escoamento e recirculação. Portanto, a avaliação de dispersão e de incidência sobre áreas sensíveis deve ser revista sempre que o arranjo da unidade for modificado.

**Fontes:** `regis-dce79d82a4a7f1760d88e146:pNone:15.60-32.0`, `petroles-4ee4bce16acf674505c8912d:pNone:1742905.0-1742941.0`

## 4. Radiação térmica: critérios, condicionantes e impacto estrutural
A radiação térmica da chama é apontada como um dos principais limitantes de projeto do flare offshore. O material relaciona melhor desempenho radiativo a chamas:
- curtas;
- de cor clara;
- pouco deformáveis pelo vento.

Para esse tipo de chama, o texto informa que a parcela do calor total de combustão liberada por radiação pode ficar em torno de **7 a 10%**. Essa característica é relevante porque a radiação incidente deve permanecer aceitável sobre pessoas, equipamentos e estrutura da plataforma.

### 4.1 Níveis de referência citados no material
O material atribui ao API RP 521 níveis recomendados de radiação incidente em áreas de trabalho de:
- **1 578 W/m² (500 BTU/h·ft²)** para condições contínuas;
- **4 737 W/m² (1 500 BTU/h·ft²)** para condições de emergência.

Esses valores são apresentados como referência para que a tocha possa queimar qualquer vazão de gás prevista no projeto, sob quaisquer condições ambientais consideradas.

### 4.2 Ferramentas de análise de radiação e temperatura estrutural
Um exemplo tecnológico citado é o uso, pela Petrobras, de simuladores computacionais de radiação térmica para tochas multiponto. Segundo o material, esses simuladores:
- representam as várias chamas da tocha com posições e geometria volumétrica definidas;
- calculam fatores de configuração entre as superfícies de chama e pontos de interesse na plataforma ou na estrutura da lança;
- avaliam campos triaxiais de temperatura nas paredes dos tubos estruturais da lança.

Esse tipo de análise permitiu, no caso citado, reduzir comprimento/peso de lanças, racionalizar heat shields e até empregar a própria estrutura como caminho para condução do gás. Como lição de engenharia, isso mostra que a avaliação de radiação não serve apenas para proteção de pessoal: ela também condiciona arquitetura estrutural, envelopes de operação e filosofia de proteção térmica.

**Fontes:** `regis-dce79d82a4a7f1760d88e146:pNone:15.60-32.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:832965.0-833015.0`

## 5. Ruído como critério de projeto e operação
O material informa que a queima em condição contínua deve ocorrer com **nível de ruído aceitável** na plataforma. Esse requisito atua como limitante de engenharia para:
- a velocidade de saída do gás no flare tip;
- a velocidade do gás nas tubulações do sistema.

Assim, o ruído não é consequência secundária: ele participa da definição do envelope operacional do sistema. Em termos práticos, aumentar velocidade para favorecer mistura e estabilidade de chama pode elevar ruído; portanto, o projeto precisa equilibrar continuidade da queima, mistura com ar, radiação e ruído.

**Fontes:** `regis-dce79d82a4a7f1760d88e146:pNone:15.60-32.0`, `petroles-4ee4bce16acf674505c8912d:pNone:1742905.0-1742941.0`

## 6. Emissões, venting versus flaring e minimização de impactos
O material associa a queima em tocha a emissões atmosféricas, principalmente pela formação de **CO2** e vapor d'água, além de calor e ruído. Também reconhece a relevância climática do tema: historicamente, o controle regulatório e o aproveitamento energético do gás contribuíram para reduzir volumes queimados, mas a eliminação total do flaring não é compatível com a função de segurança do sistema.

Há ainda uma distinção importante entre **venting** e **flaring**. O material sustenta que a queima do gás reduz o impacto ambiental relativo da emissão direta de gás natural rico em metano para a atmosfera. Em outras palavras:
- do ponto de vista de segurança, o flare permite descarte controlado e com ignição imediata;
- do ponto de vista ambiental, flaring pode ser preferível à liberação direta de gás inflamável e rico em metano;
- mesmo assim, flaring continua representando perda de recurso energético e emissão de gases de efeito estufa, devendo ser minimizado sempre que possível sem comprometer a segurança.

Portanto, a estratégia tecnicamente consistente não é "eliminar a tocha", mas sim:
1. preservar sua disponibilidade para cenários de alívio e despressurização;
2. reduzir flaring rotineiro por meio de melhor controle operacional e aproveitamento/exportação do gás quando viável;
3. assegurar que, quando a tocha for usada, a queima seja estável, completa e com impactos controlados de dispersão, radiação e ruído.

**Fontes:** `petroles-4ee4bce16acf674505c8912d:pNone:1742886.0-1742923.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:4261895.0-4261932.0`, `regis-dce79d82a4a7f1760d88e146:pNone:15.60-32.0`

## 7. Implicações para comissionamento, operação e manutenção
Mesmo com foco em queima, dispersão e impactos, o material permite extrair alguns pontos objetivos para ciclo de vida do sistema:

### 7.1 Comissionamento e partida
- verificar disponibilidade da chama piloto antes de admitir correntes de alívio;
- confirmar que a geometria/implantação do sistema atende aos critérios de vento, radiação e dispersão previstos em projeto;
- assegurar funcionalidade de selos/vedações e do sistema de remoção de líquidos na base;
- verificar que o caminho do flare esteja desobstruído e com baixa perda de carga compatível com a função de alívio.

### 7.2 Operação normal, upset e emergência
- diferenciar operação contínua e operação de emergência, pois duração, vazão e consequências são distintas;
- manter queima estável mesmo sob condições meteorológicas adversas;
- monitorar impactos sobre áreas ocupadas, HVAC e heliponto;
- tratar H2S como agravante importante na avaliação de dispersão.

### 7.3 Manutenção e modificações
- preservar integridade de piloto, linhas, vedações e recipiente de líquidos;
- evitar inserção de obstáculos ou alterações que prejudiquem a função de "grande válvula de alívio" do sistema de flare;
- reavaliar radiação, ruído e dispersão após modificações de layout, de ventilação ou da própria lança.

**Fontes:** `regis-dce79d82a4a7f1760d88e146:pNone:15.60-32.0`, `petroles-4ee4bce16acf674505c8912d:pNone:1742905.0-1742941.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:4261895.0-4261932.0`

## 8. Síntese técnica
Para a faceta **Queima, dispersão e impactos**, a mensagem central do material é que um flare confiável em FPSO depende da combinação de:
- ignição sempre disponível;
- geometria e velocidade de descarga que sustentem chama estável;
- implantação orientada por vento, ocupação humana e interfaces sensíveis;
- controle de radiação térmica e ruído;
- minimização de emissões e de flaring rotineiro sem perder a função de segurança.

Quando esses elementos são tratados de forma integrada, o sistema de flare deixa de ser apenas o "ponto de queima" e passa a ser entendido como um subsistema de segurança, habitabilidade e desempenho ambiental da unidade.