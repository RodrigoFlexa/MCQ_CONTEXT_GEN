# Rede de flare e segregação HP/LP

## 1. Finalidade do sistema e arquitetura básica da rede
O sistema de flare integra a filosofia de alívio, blowdown e disposição segura de hidrocarbonetos liberados por eventos de operação normal anormal ou de emergência. Em termos funcionais, ele deve:

- receber descargas de válvulas de alívio e sistemas de despressurização;
- transportar essas correntes sem comprometer a capacidade de proteção dos equipamentos a montante;
- separar líquidos antes do ponto de queima;
- evitar a formação de mistura inflamável dentro da própria rede;
- descarregar e queimar o gás com segurança aceitável para pessoas, equipamentos e estruturas.

Uma configuração típica inclui coletores (headers), vaso de separação/knock-out ou vaso de blowdown, selos, chaminé/flare stack, pilotos/ignição e utilidades associadas, como gás de purga, gás combustível e, em alguns casos, vapor para operação smokeless. O vaso de separação tem papel central para remover líquidos e evitar que cheguem ao queimador; os selos têm função de impedir infiltração de ar; e a torre/chaminé deve ser posicionada e dimensionada considerando efeitos de calor, vento e exposição da instalação. Em muitas plantas, inclusive unidades offshore e FPSOs, pode haver mais de um subsistema de flare, conforme a faixa de pressão, a natureza do fluido e o regime de descarga esperado.

**Rastreabilidade da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:4262419.0-4262463.0`, `petroles-4ee4bce16acf674505c8912d:pNone:1742905.0-1742941.0`, `hse-84ee4101a6ca194620d4089b:p41-44:25.0-15.0`

## 2. Lógica de segregação da rede: headers HP e LP
A segregação entre flare de alta pressão (HP) e baixa pressão (LP) é um arranjo recorrente porque as fontes de descarga, as vazões, os regimes hidráulicos e as consequências operacionais são diferentes.

### 2.1. Função típica do header LP
O sistema LP é usualmente associado a correntes de baixa pressão, próximas da atmosférica, oriundas de:

- vazamentos de válvulas;
- separadores de último estágio;
- tanques de armazenamento;
- hidrocarbonetos parcialmente evaporados (flash) de tanques e vasos;
- pequenas liberações rotineiras ou semi-rotineiras do processo.

Em geral, trata-se de uma rede voltada a baixas vazões e baixa capacidade de contrapressão admissível.

### 2.2. Função típica do header HP
O sistema HP é usualmente empregado para despressurização da planta em emergência e para eventos de maior severidade, lidando com altas vazões de descarga. Portanto, a rede HP tende a ser associada a cenários de blowdown/ESD e a correntes com maior energia de expansão.

### 2.3. Por que segregar HP e LP
A segregação HP/LP ajuda a:

- evitar que um cenário severo de blowdown imponha contrapressão excessiva sobre fontes de baixa pressão;
- dimensionar cada header e seus vasos para a faixa de vazão e pressão que realmente precisam atender;
- melhorar a estabilidade operacional da rede em partidas, paradas e upset;
- reduzir interação indesejada entre descargas contínuas/pequenas e descargas emergenciais/maciças;
- facilitar medição, monitoramento e análise de desempenho por faixa de serviço.

Além da segregação por pressão, o material disponível também indica a necessidade de separar correntes incompatíveis, por exemplo correntes frias/úmidas de correntes quentes/com condensado, e de projetar a tubulação para evitar acúmulo de slugs líquidos. Isso é relevante porque a mistura inadequada de serviços distintos pode aumentar condensação, arraste de líquido, vibração, golpes de pressão, corrosão e perda de capacidade hidráulica da rede.

### 2.4. Outras segregações possíveis
Os trechos também mencionam separação entre sistemas para gases corrosivos/ácidos e não corrosivos. Para gases ácidos com alto teor de H2S, descreve-se uma "tocha química" dedicada. Já para gases não corrosivos, descreve-se um coletor principal dividido em alta e baixa pressão. Isso indica que a arquitetura da rede pode exigir segregação simultânea por:

- pressão (HP/LP);
- corrosividade/composição (ácido vs. não ácido);
- compatibilidade térmica e de fase (quente/frio, seco/úmido).

Essa decisão não deve ser tratada como regra única para todas as instalações: ela depende do inventário, da composição do fluido, do perfil de cenários de alívio e da filosofia global de segurança de processo.

**Rastreabilidade da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:4262419.0-4262463.0`, `petroles-4ee4bce16acf674505c8912d:pNone:1742905.0-1742941.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:1903113.0-1903157.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:1903134.0-1903178.0`, `hse-84ee4101a6ca194620d4089b:p41-44:25.0-15.0`

## 3. Prevenção da entrada de ar na rede de flare
A prevenção da entrada de ar é um requisito de segurança central. O objetivo é impedir que, dentro dos headers, vaso(s), riser e base da chaminé, se forme mistura inflamável que possa ser acesa pelos próprios pilotos da tocha.

### 3.1. Mecanismo básico de proteção: purga contínua
O meio mais diretamente citado é a manutenção de fluxo contínuo de gás de purga, normalmente gás combustível ou nitrogênio, para assegurar vazão ascendente e pressão interna capaz de evitar penetração de ar na tocha e nos headers. O HSE ressalta que esse arranjo deve funcionar em todas as condições da instalação, especialmente em partida e parada, quando pode não haver gás combustível disponível.

### 3.2. Por que o risco existe mesmo sem grande vazão de flare
Um ponto importante do material é que a entrada de ar não ocorre apenas pela boca da chaminé. Em fluxos muito baixos, sem purga suficiente, pode haver pressão negativa na base da chaminé por efeito de empuxo/flutuabilidade do gás residual, sobretudo se esse gás for:

- de baixa densidade/baixo peso molecular; ou
- estiver a temperatura elevada.

Nessa condição, qualquer vazamento em flanges, tampas de inspeção ou conexões pode admitir ar para dentro da rede. Se os pilotos estiverem acesos, essa mistura pode inflamar. Por isso, a estanqueidade do sistema é requisito prático tão importante quanto a própria taxa de purga.

### 3.3. Selos como barreira contra ingresso de ar
Os trechos tratam dois tipos principais de selagem:

- **selo hidráulico/selo d’água/vaso de selagem**, que funciona de modo análogo a uma retenção hidráulica;
- **selo molecular**, destinado a reduzir o consumo de gás de selagem/purga e dificultar a infiltração de ar.

O selo molecular é descrito como baseado em diferença de peso molecular, com reposição contínua do gás de selagem e manutenção de pressão ligeiramente acima da atmosférica. O benefício principal é reduzir a vazão de purga necessária em comparação com uma chaminé sem esse recurso. Ainda assim, o próprio material alerta que a simples existência do selo não elimina a necessidade de filosofia operacional adequada, estanqueidade e controles compatíveis.

### 3.4. Pilotos e risco de ignição interna
O documento fonte é explícito: o perigo de explosão está associado à presença de ar/oxigênio na rede enquanto os pilotos permanecem acesos. Portanto:

- se o sistema precisar ser aberto para intervenção, os pilotos devem ser apagados antes do trabalho;
- eles não devem ser reacendidos antes de a rede ter sido completamente purgada.

Esse ponto liga diretamente projeto, operação e manutenção: a prevenção de entrada de ar não é apenas um detalhe do flare tip, mas uma disciplina de integridade operacional da rede inteira.

**Rastreabilidade da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:1903113.0-1903157.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:1903134.0-1903178.0`, `hse-84ee4101a6ca194620d4089b:p41-44:25.0-15.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:4262419.0-4262463.0`

## 4. Componentes da rede relevantes para a segregação e para a segurança do header

### 4.1. Vaso de separação / knock-out / blowdown drum
A função principal é separar e recuperar líquidos do fluxo enviado ao flare, evitando que eles atinjam o queimador. Isso é essencial para reduzir risco de arraste de líquido, instabilidade de chama, dano térmico e eventos mecânicos associados a escoamento bifásico.

O HSE acrescenta que o knock-out drum deve ser dimensionado para eventos previsíveis de alívio e que sua função não deve ser perdida por alto nível de líquido. Se o desempenho do vaso for degradado em alto nível, deve existir resposta operacional definida.

### 4.2. Header drains
Drenos de header, quando instalados, devem permanecer desobstruídos. Isso é relevante tanto para segregação correta de fases quanto para prevenção de bolsões de líquido e slugs, especialmente quando há mistura potencial entre correntes frias, úmidas e quentes.

### 4.3. Válvulas de isolamento a jusante de dispositivos de alívio/blowdown
Quando existirem válvulas de isolamento a jusante desses dispositivos, deve haver arranjo robusto para impedir fechamento inadvertido enquanto o dispositivo estiver em serviço, como intertravamento por chave ou disciplina formal de válvula travada aberta/fechada. Mudança de posição deve ser precedida de avaliação de risco.

### 4.4. Integração entre headers e blowdown
Se o sistema de blowdown não suportar fluxo simultâneo de todos os sistemas protegidos, a filosofia deve prever blowdown faseado ou escalonado, inclusive por configuração do ESD. Isso afeta diretamente a arquitetura HP/LP, porque a segregação física dos headers por si só não garante capacidade sistêmica adequada sem lógica de acionamento compatível.

**Rastreabilidade da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:1903113.0-1903157.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:1903134.0-1903178.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:4262419.0-4262463.0`, `hse-84ee4101a6ca194620d4089b:p41-44:25.0-15.0`

## 5. Comissionamento, partida e operação da rede com foco em ar ingress e segregação

### 5.1. Partida após montagem ou abertura do sistema
O material descreve uma condição crítica de partida: há risco severo de explosão se os pilotos forem acesos antes de o sistema ser totalmente purgado. A referência disponível cita purga prévia com gás incondensável em volume equivalente a **dez vezes o volume interno do sistema**, incluindo tubulações, coletor das válvulas de alívio alinhadas para flare e o riser até o ponto de queima.

Os gases de purga citados como apropriados são aqueles que não se condensam à temperatura ambiente, incluindo gás natural, propano, butano, nitrogênio, dióxido de carbono e outros gases inertes.

### 5.2. Operação rotineira
A operação deve prever, no mínimo:

- verificação rotineira de taxa de purga acima do mínimo seguro;
- confirmação de que drenos dos headers estão livres;
- monitoramento da condição dos selos;
- manutenção da alimentação constante dos pilotos durante o período em que a tocha estiver em operação normal;
- decisão documentada sobre quando continuar operando, quando parar e quando um shutdown sem blowdown pode ser mais seguro em caso de falha na própria rede de flare.

### 5.3. Testes funcionais
O HSE recomenda testes rotineiros do blowdown em condição controlada para verificar, por exemplo:

- tempo de despressurização;
- ocorrência de vibração excessiva;
- efetividade geral do sistema.

Isso é particularmente importante em FPSOs, nos quais mudanças de composição do fluido, regime de produção e modificações da planta podem alterar o comportamento hidráulico real dos headers.

**Rastreabilidade da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:1903134.0-1903178.0`, `hse-84ee4101a6ca194620d4089b:p41-44:25.0-15.0`

## 6. Critérios práticos para avaliar a configuração de uma rede de flare HP/LP
Ao avaliar se a configuração da rede está coerente com a função de segurança pretendida, alguns critérios extraídos do material são particularmente úteis:

1. **Os cenários de alívio e blowdown foram identificados e as combinações críveis foram consideradas?** A rede deve suportar combinações plausíveis sem comprometer a proteção contra sobrepressão.
2. **A segregação HP/LP evita interação hidráulica indevida?** Deve haver lógica clara para não transferir contrapressão de eventos severos do HP para fontes sensíveis do LP.
3. **Há segregação adicional para correntes incompatíveis?** Ex.: ácido vs. não ácido; quente/condensante vs. fria/úmida.
4. **Existe meio confiável de impedir entrada de ar em todas as condições operacionais?** Purga contínua, estanqueidade, selos e filosofia de partida/parada precisam ser coerentes entre si.
5. **Os drenos e vasos suportam o comportamento bifásico esperado?** A presença de líquidos não pode anular a função do sistema.
6. **O comissionamento prevê purga completa antes do acendimento de pilotos?** Esse é um ponto crítico de segurança.
7. **A rede foi reavaliada após modificações operacionais ou de composição de fluido?** Mudança de serviço pode invalidar a segregação ou a capacidade originalmente assumida.
8. **Os dispositivos de isolamento e manutenção preservam a disponibilidade da função de alívio?** Fechamentos inadvertidos a jusante de dispositivos de proteção devem ser prevenidos.

Em síntese, a segregação HP/LP não deve ser analisada apenas como arranjo de tubulação. Ela é parte de uma arquitetura de segurança que combina hidráulica da rede, compatibilidade de fluidos, separação de líquidos, purga/selagem, filosofia de partida e confiabilidade operacional.

**Rastreabilidade da seção:** `hse-84ee4101a6ca194620d4089b:p41-44:25.0-15.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:4262419.0-4262463.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:1903113.0-1903157.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:1903134.0-1903178.0`, `petroles-4ee4bce16acf674505c8912d:pNone:1742905.0-1742941.0`