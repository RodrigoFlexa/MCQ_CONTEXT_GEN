# Ambiente marinho e integridade de equipamentos

## 1. Visão técnica da faceta
A exposição ambiental em FPSOs e sistemas submarinos afeta a integridade principalmente por três vias recorrentes nos materiais fornecidos: **carregamentos cíclicos**, **vibrações induzidas pelo escoamento** e **condições térmicas do meio**, com reflexos sobre vida à fadiga, desempenho funcional, disponibilidade e necessidade de monitoramento.

Nos trechos analisados, o conteúdo é particularmente forte em **fadiga estrutural de risers, captadores de água do mar e tubulações**, com ênfase em ações de **vento, ondas e correntes**, inclusive sobre estruturas conectadas a unidades flutuantes. Há também indicações de que o **ambiente corrosivo offshore**, combinado com gradientes térmicos e esforços dinâmicos, agrava a durabilidade de tubulações, embora os mecanismos de corrosão não sejam detalhados nas fontes disponíveis.

**Fontes da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:4056207.0-4056247.0`, `petroles-4ee4bce16acf674505c8912d:pNone:1087226.0-1087259.0`, `petroles-4ee4bce16acf674505c8912d:pNone:1230533.0-1230579.0`

## 2. Caracterização ambiental relevante para integridade

### 2.1 Variáveis meteoceanográficas críticas
Os materiais apontam que a dinâmica de plataformas e risers está diretamente ligada a **vento, ondas e correntes**. No mar, o vento transfere energia para a superfície, gerando ondas em várias frequências e direções. Essas ondas podem ser tratadas como:
- **vagas (sea / wind-sea)**: ainda na zona de geração e recebendo energia do vento;
- **ondulação (swell)**: fora da zona de geração original ou já sem receber energia adicional do vento.

Para projeto e avaliação operacional, os parâmetros destacados são:
- **altura significativa de onda**;
- **período**;
- **direção**;
- **densidade espectral** e **espectro direcional**.

A relação entre estado de mar e movimento da estrutura é descrita pelas **curvas RAO (Response Amplitude Operator)**, que indicam quanto a resposta da unidade varia conforme altura, período e direção da onda. Isso é central para estimar movimentos do casco e os carregamentos transferidos a risers, captadores e outros equipamentos expostos.

Além das ondas, o **perfil de corrente ao longo da profundidade** é crítico. As fontes ressaltam que, em águas profundas, magnitude e direção da corrente podem variar significativamente com a profundidade, de modo que diferentes trechos de uma mesma linha podem ser excitados em modos vibratórios distintos.

**Fontes da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:4056207.0-4056247.0`, `petroles-4ee4bce16acf674505c8912d:pNone:1230533.0-1230579.0`, `regis-f71a954fc19e882ac51655f2:pNone:2611.0-2865.0`

### 2.2 Monitoramento para gestão de integridade
Os trechos citam instrumentação típica de monitoração meteoceanográfica e estrutural, incluindo:
- **ADCP** para perfil de correntes em diferentes profundidades;
- **anemômetros** para direção e velocidade do vento;
- **ondógrafos** para altura, período e direção de ondas.

Esse monitoramento é importante não só para prever movimentos da unidade, mas para sustentar análises de integridade de longo prazo, especialmente de fadiga. O conhecimento “de quanto” e “como” cada variável ambiental influencia os movimentos é tratado como fundamental para predizer a exposição de risers e plataformas.

**Fontes da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:4056207.0-4056247.0`

## 3. Mecanismos pelos quais o ambiente afeta a integridade

### 3.1 Fadiga por carregamentos cíclicos ambientais
Os materiais descrevem a fadiga como processo de **nucleação e propagação de trincas** sob cargas cíclicas, levando à ruptura em tensões inferiores àquelas de projeto. Em estruturas offshore, os carregamentos cíclicos relevantes incluem:
- ação de **ondas**;
- ação de **correntes marítimas**;
- **movimentos da unidade flutuante** transferidos ao topo do riser;
- variações cíclicas de **pressão** e **temperatura**;
- em algumas fases do ciclo de vida, também **transporte** e **instalação**.

Para risers conectados a FPSOs, as fontes destacam que a combinação de **correnteza + onda + vento atuando sobre a unidade flutuante** induz movimentos no casco, e esses movimentos chegam ao topo do riser como cargas estáticas e dinâmicas. Em SCRs, as regiões apontadas como mais críticas são a **conexão de topo** e o **TDP (touchdown point)**.

Os trechos também registram, com base em literatura técnica citada pelos próprios autores, que as principais causas de fadiga de risers incluem:
- **carregamento direto de onda**;
- **movimentos de 1ª e 2ª ordens da embarcação**;
- **vibrações induzidas por vórtices (VIV)**.

Para mar irregular, o dano por fadiga é tratado nas fontes como acumulativo por estado de mar, com somatório posterior pela **regra de Miner**.

**Fontes da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:223570.0-223619.0`, `petroles-4ee4bce16acf674505c8912d:pNone:1087226.0-1087259.0`, `petroles-4ee4bce16acf674505c8912d:pNone:1230533.0-1230579.0`

### 3.2 VIV: mecanismo crítico para risers, captadores e linhas com vãos livres
As fontes tratam a **VIV (Vortex Induced Vibration)** como um dos mecanismos mais danosos para linhas submarinas. O fenômeno decorre do **desprendimento alternado de vórtices** ao redor de corpos cilíndricos, gerando esforços oscilatórios, especialmente na direção transversal ao escoamento.

Consequências destacadas:
- redução da **vida útil à fadiga** do riser;
- aumento do dano em **SCRs** e em **risers tensionados no topo**;
- possibilidade de dano em **flowlines com vãos livres**;
- transferência indireta de vibração para outras estruturas, como **cabeça de poço**, **casing** e **conexões/soldas**;
- em sistemas com linhas próximas, contribuição para **colisão relativa** e efeitos de esteira.

Os materiais distinguem, para sistemas de risers:
- **vibração transversal (cross-flow)**, com amplitudes da ordem de um diâmetro;
- componente **in-line** induzida pela transversal, com amplitudes de 30 a 50% da transversal;
- **in-line pura**, com amplitudes menores.

Uma observação importante para tomada de decisão é que o VIV pode ser **mais sensível ao perfil de corrente** do que a outras variáveis citadas no estudo. Isso reforça a necessidade de dados verticais de corrente, e não apenas valores superficiais.

**Fontes da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:4056207.0-4056247.0`, `petroles-4ee4bce16acf674505c8912d:pNone:1087226.0-1087259.0`, `regis-f71a954fc19e882ac51655f2:pNone:2611.0-2865.0`, `regis-c7a0ad45c8b8fbff935529bf:pNone:215.0-477.0`, `petroles-4ee4bce16acf674505c8912d:pNone:1230533.0-1230579.0`

### 3.3 Influência das ondas e movimentos impostos pela plataforma
No caso de linhas conectadas a unidades flutuantes, os carregamentos ambientais não atuam apenas diretamente sobre a linha: eles também alteram a resposta da plataforma, que impõe movimentos à conexão de topo.

Os trechos citam a aplicação da **equação de Morison** para a força de onda em risers na direção **in-line**, composta por:
- um termo de **inércia**, relacionado à aceleração da partícula fluida;
- um termo de **arrasto**, relacionado à velocidade da partícula fluida e à resistência ao movimento no fluido.

Mesmo quando o projeto busca reduzir a ação direta de ondas, ainda pode permanecer a suscetibilidade a correntes e VIV. Exemplo disso é o **riser tower**, cuja configuração submersa reduz a fadiga associada às ondas de superfície, mas não elimina os problemas de **VIV no riser vertical** e **VIM no tanque de flutuação**.

**Fontes da seção:** `regis-c7a0ad45c8b8fbff935529bf:pNone:215.0-477.0`, `petroles-4ee4bce16acf674505c8912d:pNone:1230533.0-1230579.0`

### 3.4 Temperatura da água do mar e desempenho/arranjo de equipamentos
Um caso específico relevante é o do **captador profundo de água de resfriamento**. As fontes mostram que, quando a temperatura disponível na superfície não atende às especificações do sistema de resfriamento, pode ser necessário captar água em profundidade maior.

No exemplo citado, a solução foi um **tubo de aço** conectado ao pontoon, com extremidade inferior livre captando água a **351,4 m** de profundidade. A definição da posição considerou simultaneamente:
- evitar interferência futura com **risers flexíveis**;
- reduzir a ação de **ondas** sobre o captador;
- eliminar o risco de **impacto no flutuante**;
- permitir a ligação ao sistema de resfriamento da unidade.

Isso mostra que a variável ambiental **temperatura da água** afeta diretamente o **desempenho funcional** do sistema de resfriamento, enquanto ondas e correntes afetam a **integridade estrutural** e a **instalação** do equipamento.

**Fontes da seção:** `regis-a4e97e67b420ad75979d406a:pNone:0.0-40.0`

### 3.5 Ambiente corrosivo e efeitos combinados
Os materiais não trazem uma modelagem detalhada de corrosão, mas registram explicitamente que a exploração e condução de petróleo e gás offshore envolvem a combinação de:
- **carregamentos dinâmicos**;
- **gradientes de temperatura elevados**;
- **ambiente corrosivo**.

Do ponto de vista de integridade, isso é relevante porque a vida útil não depende apenas da amplitude dos ciclos, mas também da interação entre dano mecânico e degradação ambiental. Entretanto, os trechos fornecidos não detalham taxas de corrosão, critérios de allowance, revestimentos, proteção catódica ou efeitos específicos de salinidade/spray marinho.

**Fontes da seção:** `petroles-4ee4bce16acf674505c8912d:pNone:1087226.0-1087259.0`

## 4. Critérios de projeto e análise orientados pela exposição ambiental

### 4.1 Seleção de dados ambientais conforme a finalidade da análise
No caso do captador de água de resfriamento em Albacora, os dados ambientais foram usados com **períodos de recorrência diferentes conforme o objetivo**:
- **3 meses** para análises de **instalação**;
- **1 ano** para análise de **fadiga**;
- **100 anos** para análises de **tensões máximas** e **deslocamentos**.

Esse ponto é importante porque a exposição ambiental relevante para dano acumulado de fadiga não é necessariamente a mesma adotada para verificação de resposta extrema. Também foram utilizados **perfis de correntes anuais e centenários** e dados de ondas com **Hmax, Tmax e Hs**.

**Fontes da seção:** `regis-a4e97e67b420ad75979d406a:pNone:0.0-40.0`

### 4.2 Limitações de modelos de VIV e implicações para decisão
As fontes destacam que análises de fadiga por VIV podem ser feitas por software, inclusive com solução modal e cálculo de dano no domínio da frequência, mas também registram limitações importantes:
- **VIV in-line pode ser ignorado**, levando a estimativa **não conservativa** do dano;
- modelo estrutural linear pode ser **impreciso** em regiões como o contato com o solo no TDP de um SCR;
- a **tensão axial causada por VIV transversal** pode não ser incluída.

Também se menciona que CFD, em princípio, poderia superar algumas limitações, mas sua aplicação ainda seria limitada pelo custo computacional, devendo métodos numéricos ser validados ou calibrados com **dados de campo** ou **ensaios de laboratório**.

Em termos práticos, isso significa que a aceitação de resultados de fadiga por VIV deve considerar não só o valor calculado, mas a **abrangência física do modelo** adotado.

**Fontes da seção:** `regis-f71a954fc19e882ac51655f2:pNone:2611.0-2865.0`

## 5. Medidas de mitigação para preservar integridade e disponibilidade

### 5.1 Mitigação de VIV em risers e tubos expostos a corrente
As medidas de mitigação citadas incluem:
- **modificação das propriedades do riser**;
- introdução de mecanismos de **inibição de vórtices**;
- uso de **strakes helicoidais**;
- uso de superfícies protuberantes, mantas perfuradas ou estabilizadores.

Os **strakes helicoidais** são apresentados como solução comum para reduzir a formação de vórtices ao longo do riser, embora tragam contrapartidas: aumento de custo, maior complexidade de manuseio/instalação e aumento do **coeficiente de arraste in-line**. A eficácia do dispositivo deve ser qualificada, incluindo efeitos hidrodinâmicos, durabilidade, crescimento marinho e acabamento superficial.

As fontes também citam, de forma mais geral, o uso de **supressores de vórtices** acoplados ao tubo para reduzir vibração e, por consequência, a probabilidade de falhas por fadiga diretas e indiretas.

**Fontes da seção:** `regis-f71a954fc19e882ac51655f2:pNone:2611.0-2865.0`, `petroles-4ee4bce16acf674505c8912d:pNone:1087226.0-1087259.0`

### 5.2 Mitigação de vibração em tubulações de pequeno diâmetro e reflexos na disponibilidade
Nos sistemas de processo, falhas por vibração em **tubulações de pequeno diâmetro (TPD)** podem causar:
- **vazamentos**;
- potencial de **explosão**;
- **danos ambientais**;
- **danos materiais**;
- **perda de produção**;
- **baixa confiabilidade e disponibilidade**.

As boas práticas citadas nos materiais incluem:
- avaliar a real necessidade da TPD;
- mantê-la **curta** e adequadamente suportada;
- preferir conexões mais robustas;
- realocar derivações para regiões da linha principal com **pouco movimento**, próximas de suportes, quando os equipamentos adjacentes não forem fonte de vibração;
- adicionar **suportes de reforço**, preferencialmente em duas direções e afastados do ponto de conexão o suficiente para serem efetivos;
- evitar TPD longas e sem suportação solidária à linha principal.

Essas recomendações são úteis porque a exposição ambiental e operacional do FPSO pode aumentar a severidade de vibrações já presentes no processo, degradando a disponibilidade de instrumentos, drenos, vents e pequenos ramais.

**Fontes da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:466662.0-466730.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:466836.0-466877.0`

## 6. Exposição ambiental ao longo do ciclo de vida
A integridade pode ser afetada antes mesmo da operação contínua. As fontes registram **fadiga por transporte** em tubos e mencionam um caso em que, durante o transporte de uma plataforma, concluiu-se que o **vento poderia ter provocado vórtices**, levando o material à fadiga e a trincas.

Assim, para equipamentos e estruturas expostas, a gestão da integridade não deve se limitar ao período de produção: **transporte, instalação e operação** podem contribuir para o dano acumulado.

**Fontes da seção:** `petroles-4ee4bce16acf674505c8912d:pNone:1087226.0-1087259.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:849063.0-849118.0`

## 7. Síntese aplicada ao FPSO/FSO
Para FPSOs e sistemas subsea, os materiais permitem concluir, de forma técnica e não certificadora, que:
1. **A exposição meteoceanográfica deve ser traduzida em resposta estrutural**, e não tratada apenas como dado ambiental bruto.
2. **Perfis de corrente com profundidade** são decisivos para estimar VIV e vida à fadiga de risers e equipamentos alongados.
3. **Movimentos do casco** afetam diretamente a integridade de linhas conectadas, especialmente SCRs.
4. **Temperatura da água do mar** pode impor soluções de arranjo e instalação específicas para manter desempenho de sistemas de resfriamento.
5. **Mitigação de vibração** em risers e em tubulações de pequeno diâmetro é também uma medida de **disponibilidade operacional**, não apenas de integridade mecânica.
6. **Resultados de software** para VIV/fadiga devem ser aceitos com consciência de suas limitações, preferencialmente suportados por monitoramento, validação e critérios conservadores compatíveis com a aplicação.

**Fontes da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:4056207.0-4056247.0`, `regis-a4e97e67b420ad75979d406a:pNone:0.0-40.0`, `regis-f71a954fc19e882ac51655f2:pNone:2611.0-2865.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:466662.0-466730.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:466836.0-466877.0`, `petroles-4ee4bce16acf674505c8912d:pNone:1230533.0-1230579.0`