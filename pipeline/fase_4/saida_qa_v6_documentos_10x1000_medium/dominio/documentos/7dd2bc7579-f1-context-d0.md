# Controle operacional de tratadores eletrostáticos no processamento de óleo

## 1. Recorte técnico desta faceta
Com o material disponível, este documento trata principalmente do **controle operacional da interface óleo-água e das variáveis de processo que condicionam a estabilidade e a eficiência de separação** em sistemas de tratamento de óleo usados offshore, incluindo tratadores eletrostáticos no contexto do processamento primário. O foco está em como **temperatura, pressão, vazão, tempo de residência, estabilidade de emulsão, dosagem química e estratégia de controle de nível/interface** afetam a faixa operacional.

As fontes consultadas indicam que, no processamento primário offshore, o aumento de produção de água, a presença de óleos mais pesados e as restrições de peso e espaço levaram à adoção de equipamentos mais compactos e tecnologias de tratamento mais complexas, entre elas os **tratadores eletrostáticos**. Ao mesmo tempo, essa compacidade reduz a tolerância a oscilações de carga, tornando o controle de processo mais crítico. Também é importante distinguir que **desidratação** é tipicamente executada nas unidades de produção, enquanto a **dessalgação** é descrita nas fontes como etapa típica de refinaria. Assim, para esta faceta, o maior suporte documental está na desidratação e no controle da interface, não em uma discussão completa de dessalgadores eletrostáticos.  
**Fontes:** `regis-cbfdf414fa0dd7c3c5945bb5:pNone:0.0-27.0`, `regis-382370e69ec038894a313f3f:pNone:16.120-55.0`

## 2. Papel do tratador no trem de processo e relação com a separação primária
O tratamento de óleo em FPSO normalmente depende de uma cadeia em que a separação inicial gás-óleo-água reduz a carga sobre as etapas seguintes. As fontes sobre separadores trifásicos mostram que o vaso precisa simultaneamente:

- separar gás, óleo e água livre;
- absorver flutuações de carga e golfadas;
- manter inventário líquido adequado;
- limitar arraste de líquido no gás, água no óleo e óleo na água.

Em separadores gravitacionais trifásicos, as variáveis mais diretamente associadas ao inventário são:

- **nível de óleo** na câmara de óleo;
- **nível de água/interface** na câmara de separação;
- **pressão do gás** no vaso.

A lógica operacional é relevante para tratadores eletrostáticos porque estes, mesmo quando agregam mecanismos adicionais de coalescência, continuam dependendo de um regime hidráulico estável a montante e a jusante. Se a separação primária entrega ao tratador uma corrente com excesso de gás livre, espuma, sólidos ou emulsão muito estável, a operação do tratador tende a ficar mais instável e a janela operacional encolhe.

As fontes também descrevem a seção de acumulação de líquido como aquela em que o líquido permanece retido por um **tempo de retenção/residência**, citado em uma das fontes como tipicamente da ordem de **5 a 10 min** para boa eficiência em muitos casos; e outra fonte indica que, em ensaios e prática de projeto de separadores, costuma-se buscar condição de viscosidade do petróleo em torno de **10 a 25 cSt** para favorecer a separação. Esses números não devem ser tomados como universais para todo tratador eletrostático, mas são referências úteis para ajuste da janela térmica e hidráulica.  
**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:215418.0-215453.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:215508.0-215548.0`, `regis-382370e69ec038894a313f3f:pNone:16.120-55.0`

## 3. Variáveis operacionais que mais afetam a estabilidade do tratador

### 3.1 Temperatura: viscosidade, diferença de densidade e espuma
A temperatura de separação depende das características do óleo processado. As fontes indicam que, em geral:

- quanto **maiores a viscosidade e a densidade** do fluido, **maior tende a ser a temperatura requerida**;
- o aumento de temperatura costuma **reduzir a densidade do óleo** e **aumentar a diferença de densidade óleo-água**, favorecendo a separação gravitacional;
- o aumento de temperatura também pode **reduzir a viscosidade**, o que facilita a movimentação e a segregação das gotas de água;
- a temperatura elevada tende a **minimizar a formação de espuma** na separação gás-óleo.

Do ponto de vista de controle operacional, isso significa que a temperatura do tratador não deve ser ajustada apenas para “aquecer mais”, mas para colocar o óleo em uma faixa reológica que permita coalescência e separação dentro do tempo de residência disponível. Uma referência de laboratório/projeto descrita nas fontes é ajustar a faixa térmica para que a viscosidade cinemática do petróleo fique entre **10 cSt e 25 cSt**. Para isso, é citada a correlação ASTM D341:

**Log[Log(ν + 0,7)] = A + B·Log(T + 273)**

onde:
- **ν** = viscosidade cinemática, em cSt;
- **T** = temperatura, em °C;
- **A** e **B** = constantes ajustadas para cada petróleo.

Essa relação é útil para selecionar a temperatura de ensaio, de comissionamento ou de operação alvo a partir da reologia do óleo.

Há, porém, um contrapeso operacional importante: uma das fontes observa que elevar a temperatura pode produzir, sobre a vazão de gás, efeito semelhante ao de reduzir a pressão, pois favorece a liberação de gás da corrente. Logo, aquecer demais pode melhorar viscosidade e coalescência, mas também aumentar gasificação interna e perturbar a estabilidade hidráulica do vaso.  
**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:215508.0-215548.0`, `regis-382370e69ec038894a313f3f:pNone:16.120-55.0`

### 3.2 Pressão: liberação de gás e capacidade do vaso
As fontes afirmam que, quando a **pressão de separação é reduzida**, aumenta o volume de gás liberado pelo óleo. Como esse gás passa a ocupar maior volume no interior do vaso:

- cresce a fração volumétrica de gás no equipamento;
- aumenta a velocidade do gás;
- eleva-se o risco de **arraste de gotículas de óleo** na corrente gasosa;
- para evitar esse arraste, pode ser necessário **reduzir a vazão de entrada**;
- como consequência, **a capacidade do separador diminui**.

No sentido inverso, o aumento da pressão de separação pode permitir maior capacidade hidráulica, embora com menor liberação de gás do óleo.

Para um tratador eletrostático, a implicação operacional é clara: operar com pressão muito baixa pode até ajudar certa desgaseificação a montante, mas, dentro do vaso, pode piorar a estabilidade da separação e reduzir a faixa de throughput segura. Em termos de ajuste fino, pressão e temperatura devem ser avaliadas juntas, porque ambas afetam o equilíbrio entre separação líquida e liberação de gás.  
**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:215508.0-215548.0`

### 3.3 Vazão, tempo de residência e turndown operacional
As fontes são consistentes ao mostrar que a eficiência de separação depende de manter inventário e escoamento internos compatíveis com o tempo disponível para segregação das fases. Quando o vaso recebe um fluxo regular, é possível manter **estáveis o nível de óleo e a velocidade de circulação do gás**, obtendo maior eficiência.

Em sentido prático:

- aumento de vazão reduz o tempo de residência efetivo;
- oscilações de carga e golfadas tendem a deslocar interface e inventário;
- equipamentos compactos têm **menor capacidade de absorver perturbações**;
- excesso de emulsão, sólidos ou espuma ocupa volume útil e reduz ainda mais o tempo de residência real.

Portanto, a faixa operacional do tratador não depende apenas da vazão média, mas da combinação entre:

1. vazão média;
2. amplitude/frequência das oscilações;
3. viscosidade e estabilidade da emulsão;
4. volume útil realmente disponível, descontando espuma, emulsão acumulada e sedimentos.

Essa leitura é particularmente importante para FPSOs sujeitos a slugs. Uma vazão média aparentemente aceitável pode ser operacionalmente inviável se os transientes provocarem excursões frequentes de interface e perda de qualidade do óleo tratado.  
**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:215508.0-215548.0`, `regis-cbfdf414fa0dd7c3c5945bb5:pNone:0.0-27.0`

## 4. Emulsões, química e condicionamento da carga
As fontes destacam que a separação água-petróleo pode ser dificultada pela presença de **materiais insolúveis finamente divididos na interface**, que estabilizam emulsões. Para desestabilizar a emulsão e permitir a coalescência das gotas, o tratamento costuma combinar efeitos:

- adição de **desemulsificante** previamente selecionado;
- **aquecimento** da emulsão;
- estabelecimento de padrão de fluxo e condição operacional que permitam a segregação de fases.

O papel do desemulsificante, conforme descrito, é **competir e deslocar emulsificantes naturais presentes na interface**. Isso é operacionalmente relevante porque o ajuste de interface do vaso, por si só, não corrige uma emulsão estável demais: se a química estiver inadequada, a banda de emulsão cresce, consome volume do equipamento e deteriora a separação.

As fontes também mostram um método laboratorial para avaliar separação água-óleo em diferentes temperaturas e doses de desemulsificante. Embora esse procedimento não possa ser convertido diretamente em receita de campo, ele sustenta duas boas práticas:

1. selecionar a temperatura de operação com base na reologia do petróleo;  
2. avaliar o efeito do desemulsificante no desempenho de separação em condições representativas da salinidade e do teor de água da emulsão.

Em operação, isso se traduz em otimização conjunta de:

- temperatura do tratador;
- dose e ponto de injeção do desemulsificante;
- vazão alimentada;
- posição de interface e tempo de residência.

Se uma dessas variáveis for ajustada isoladamente, o ganho pode ser limitado ou até compensado por perda em outra.  
**Fontes:** `regis-382370e69ec038894a313f3f:pNone:16.120-55.0`

## 5. Controle da interface óleo-água

### 5.1 Por que o ajuste da interface é central
Nas fontes sobre separadores e sistemas compactos, a interface óleo-água aparece como variável crítica porque define quanto volume do equipamento fica efetivamente disponível para cada fase e quanto tempo cada corrente permanece no interior do vaso.

Se a interface se desloca de forma excessiva:

- pode haver piora da separação óleo-água;
- aumenta o risco de **carryover** de água para a corrente de óleo ou **carryunder** de óleo para a corrente aquosa;
- a banda de emulsão pode invadir regiões onde deveria haver separação mais limpa;
- o sistema passa a operar com menor robustez frente a perturbações.

Em um exemplo de sistema compacto, a fonte ressalta que a margem admissível de flutuação da interface era pequena porque a interface precisava ficar aproximadamente na região central de um separador tubular de 12 pol, sob pena de comprometer a eficiência de separação. Embora esse caso não descreva diretamente um tratador eletrostático de FPSO, ele evidencia o mesmo princípio: **quanto menor a folga geométrica e hidráulica, mais disciplinado deve ser o controle da interface**.  
**Fontes:** `regis-c09531a21d9ac256b681a236:pNone:276.60-312.0`

### 5.2 Medição da interface e diagnóstico do perfil interno
Uma das fontes descreve instrumentação capaz de inferir a posição da interface por comparação do sinal com uma tabela previamente carregada, além de traçar o **perfil de preenchimento do vaso**: gás, espuma, óleo, emulsão, água e areia.

Para operação e troubleshooting, essa capacidade é muito valiosa porque permite diferenciar situações que, à primeira vista, aparecem apenas como “nível ruim”:

- interface realmente deslocada;
- camada de espuma ocupando volume;
- crescimento da banda de emulsão;
- acúmulo de areia no fundo;
- discordância entre dois sensores instalados.

Em termos de controle operacional do tratador, isso ajuda a decidir se a ação correta é:

- alterar setpoint de interface;
- reduzir vazão;
- revisar dose química;
- aumentar temperatura;
- limpar fundo/internos;
- tratar falha de medição ou divergência entre instrumentos.  
**Fontes:** `regis-c09531a21d9ac256b681a236:pNone:276.60-312.0`

### 5.3 Estratégias de controle: PI, controle por bandas e dead band assimétrico
As fontes apresentam três ideias importantes para controle de interface em sistemas de separação:

1. **controle PI** como filosofia clássica de manutenção do nível/interface em um ponto definido;
2. **controle por bandas**, defendido em estudos de processamento offshore como alternativa para estabilizar as vazões de saída;
3. **dead band assimétrico**, no qual o sistema reage mais rapidamente à queda da interface, visando preservar a qualidade da corrente aquosa.

A contribuição prática dessas fontes é que o melhor controle nem sempre é o que “prende” a variável rigidamente ao setpoint. Em plantas sujeitas a oscilações de carga, foi proposto que a filosofia de ajuste do controlador de nível deveria ser a de **manter a vazão de descarte estável, deixando o nível flutuar o máximo possível dentro de limites seguros**. Essa mudança reduz a propagação de perturbações para jusante.

Aplicado ao contexto de tratadores eletrostáticos, o raciocínio é útil quando o objetivo é preservar simultaneamente:

- estabilidade hidráulica do vaso;
- qualidade do óleo tratado;
- estabilidade das correntes a jusante.

Entretanto, esse tipo de estratégia só é aceitável se os limites de excursão de interface forem conhecidos e compatíveis com:

- geometria interna do vaso;
- espessura admissível da banda de emulsão;
- risco de carryover/carryunder;
- tempo de resposta dos instrumentos e atuadores.  
**Fontes:** `regis-cbfdf414fa0dd7c3c5945bb5:pNone:0.0-27.0`, `regis-c09531a21d9ac256b681a236:pNone:276.60-312.0`

## 6. Problemas operacionais típicos que reduzem eficiência ou estreitam a faixa operacional

### 6.1 Espuma
A formação de espuma é associada, nas fontes, às características físico-químicas do óleo, impurezas presentes e à queda de pressão imposta à mistura gás-líquido. Quando presente, a espuma:

- dificulta o controle de nível;
- ocupa volume que deveria estar disponível para líquido separado;
- pode ser arrastada pela corrente de gás ou de óleo desgaseificado.

Para o operador, isso significa que um aparente problema de interface pode ser, na verdade, perda de volume útil por espuma. Nessa situação, ajustar a válvula de nível sem tratar a causa tende a ter efeito limitado.  
**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:215508.0-215548.0`

### 6.2 Emulsão persistente
As fontes indicam que emulsões formadas na interface óleo-água são problemáticas porque:

- atrapalham o controle de nível/interface;
- acumulam-se no vaso;
- reduzem o tempo de retenção efetivo;
- diminuem a eficiência global da separação.

As ações citadas para mitigar esse problema são **adição de calor** e **produtos químicos**, preferencialmente na etapa de tratamento do óleo. Em termos operacionais, uma banda de emulsão crescente é sinal de que pode haver desequilíbrio entre química, temperatura, regime de escoamento e carga processada.  
**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:215508.0-215548.0`, `regis-382370e69ec038894a313f3f:pNone:16.120-55.0`

### 6.3 Parafina, areia e sedimentos
As fontes apontam que:

- **parafinas** podem obstruir internos, especialmente placas coalescedoras e extratores de névoa;
- **areia e sedimentos** causam erosão em válvulas, obstrução de internos e redução do tempo de residência por acúmulo no fundo do vaso.

Na prática, esses fenômenos afetam diretamente a estabilidade operacional porque modificam a hidráulica interna e degradam a resposta do controle. Em tratadores, o diagnóstico deve considerar se a perda de desempenho decorre de variável de processo mal ajustada ou de perda física de volume/área útil por incrustação e sólidos.  
**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:215508.0-215548.0`

## 7. Comissionamento e qualificação do controle de interface
Uma das contribuições mais úteis das fontes é a filosofia de qualificação do sistema de controle antes da operação normal. No caso documentado, buscou-se assegurar que os tempos de ação e retardo da instrumentação, da malha e da comunicação fossem similares aos da operação real.

Os objetivos de qualificação incluíam verificar se:

- o sistema de controle e a instrumentação eram suficientes para manter o processo sob controle;
- a interface permanecia dentro da faixa requerida em condições normais e sob flutuações de vazão, pressão e composição;
- o sistema era capaz de lidar com transientes de partida, parada e flushing;
- a capacidade volumétrica do vaso era suficiente para o controle proposto;
- perturbações rápidas não induziam mistura excessiva nos equipamentos.

A matriz de testes citada é diretamente aproveitável como referência de comissionamento operacional:

- parada de alimentação;
- bloqueio de saídas de óleo e gás;
- variação de entrada em degrau;
- oscilação de entrada;
- aumento do atraso da malha de controle;
- aplicação de golfadas a montante.

Para tratadores em FPSO, essa abordagem ajuda a validar a faixa operacional real, não apenas a nominal. Um equipamento pode “fechar balanço” em regime permanente e ainda assim falhar em campo por atraso excessivo de malha, sintonia inadequada ou inventário insuficiente diante de slugs.  
**Fontes:** `regis-c09531a21d9ac256b681a236:pNone:276.60-312.0`

## 8. Lições de controle e confiabilidade extraídas dos testes
Os testes relatados também registraram falhas que são relevantes como lições de engenharia:

- rampa de variação de frequência do VSD maior que a esperada para o caso real;
- falha de associação de sensor de trip por nível baixo;
- implementação de dead band assimétrico sem anti-windup da ação integral na banda morta;
- bugs de lógica que atrasaram a campanha de testes;
- instabilidade de bomba operando perto da vazão máxima.

Esses pontos mostram que o controle estável da interface não depende só do algoritmo, mas do conjunto formado por:

- qualidade da medição;
- coerência da lógica de proteção;
- comportamento real dos atuadores;
- limites hidráulicos de bombas e válvulas;
- fidelidade entre ambiente de teste e caso de operação.

Em termos práticos, um mau desempenho do tratador pode ser erroneamente atribuído ao processo quando a causa primária está na instrumentação, na lógica de controle ou na limitação do elemento final de controle.  
**Fontes:** `regis-c09531a21d9ac256b681a236:pNone:276.60-312.0`

## 9. Critérios práticos de ajuste operacional
A partir das fontes, uma rotina técnica de ajuste do tratador pode ser estruturada assim:

1. **Verificar a estabilidade da alimentação.** Se houver golfadas ou oscilação acentuada, reconhecer que a eficiência cairá mesmo com setpoints “corretos”.  
2. **Ajustar temperatura pela reologia do óleo.** A meta é alcançar viscosidade compatível com boa separação, usando a faixa 10 a 25 cSt como referência preliminar onde aplicável.  
3. **Controlar pressão sem induzir gasificação excessiva no vaso.** Reduções de pressão podem exigir diminuição de carga para evitar arraste por aumento da velocidade do gás.  
4. **Manter interface dentro de uma banda operacional, não apenas em um número absoluto.** A banda precisa preservar volume útil, evitar carryover/carryunder e acomodar perturbações.  
5. **Monitorar crescimento de espuma e emulsão.** Esses fenômenos consomem inventário efetivo e podem explicar perda de capacidade sem alteração aparente de vazão média.  
6. **Revisar química quando a interface fica instável ou a banda de emulsão cresce.** O problema pode ser de estabilidade interfacial, não de controle de válvula.  
7. **Inspecionar obstrução por parafina e acúmulo de sólidos** quando houver perda progressiva de desempenho, resposta lenta ou necessidade crescente de intervenções.  
8. **Validar sintonia e atrasos da malha** com testes representativos das perturbações reais da unidade.

Esses critérios não substituem as especificações próprias de cada FPSO, mas sintetizam o núcleo operacional suportado pelas fontes: a boa performance depende da combinação entre **condicionamento térmico-químico**, **inventário/residência**, **pressão/vazão** e **controle robusto da interface**.  
**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:215508.0-215548.0`, `regis-382370e69ec038894a313f3f:pNone:16.120-55.0`, `regis-c09531a21d9ac256b681a236:pNone:276.60-312.0`, `regis-cbfdf414fa0dd7c3c5945bb5:pNone:0.0-27.0`

## 10. Síntese aplicada à faceta
Para a faceta **controle operacional** de tratadores eletrostáticos, o material sustenta a seguinte leitura profissional:

- a eficiência do tratamento de óleo depende fortemente da **condição da emulsão na entrada**;
- **temperatura** deve ser definida em função da reologia e não por critério único de maximização;
- **pressão** afeta diretamente a liberação de gás e, portanto, a capacidade efetiva do vaso;
- **interface óleo-água** deve ser controlada como variável de inventário crítica, preferencialmente com filosofia compatível com o regime de perturbações da unidade;
- **espuma, emulsão, parafina e sólidos** são causas recorrentes de perda de capacidade e instabilidade;
- a qualificação do controle deve reproduzir **atrasos, transientes e golfadas** reais de campo.

Em resumo, o ajuste da interface em um tratador não é uma ação isolada: ele só é tecnicamente consistente quando feito em conjunto com **temperatura, pressão, vazão, química e diagnóstico do perfil interno do vaso**.  
**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:215508.0-215548.0`, `regis-c09531a21d9ac256b681a236:pNone:276.60-312.0`, `regis-cbfdf414fa0dd7c3c5945bb5:pNone:0.0-27.0`, `regis-382370e69ec038894a313f3f:pNone:16.120-55.0`