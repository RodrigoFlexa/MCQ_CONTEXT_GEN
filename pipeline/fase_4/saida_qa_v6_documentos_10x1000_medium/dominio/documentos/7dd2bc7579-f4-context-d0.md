# Baixo desempenho e arraste em tratadores eletrostáticos

Este texto consolida os trechos fornecidos para fins de estudo e geração futura de perguntas e respostas. Ele **não substitui** dados de projeto, manuais do fabricante, procedimentos operacionais ou requisitos contratuais/regulatórios da instalação.

## 1. Papel do tratador eletrostático no trem de processamento de óleo

Nos sistemas de processamento primário, os separadores gravitacionais do primeiro estágio retiram principalmente **gás livre**, **água livre** e **óleo livre**. Mesmo assim, permanecem contaminações residuais dispersas: névoa líquida no gás, bolhas de gás no líquido, gotículas de óleo na água e, de forma especialmente crítica, **gotículas de água dispersas no óleo**. Entre essas contaminações, a dispersão de água em óleo tende a ser a mais difícil de remover, porque a diferença de densidade entre óleo e água é relativamente pequena e a viscosidade da fase contínua oleosa costuma ser maior. Além disso, emulsificantes naturais do petróleo aumentam a estabilidade da emulsão.

Por isso, após a separação primária, costuma-se empregar um **tratador eletrostático (TO)** para especificar o óleo quanto a **BS&W** e **salinidade**, promovendo a quebra da emulsão óleo/água por aplicação de campo elétrico em um vaso com tempo de residência elevado. Em literatura secundária baseada em referência PETROBRAS 2007, aparecem como metas típicas de tratamento **BS&W até 1% em volume** e **até 570 mg/L de sais no óleo**; esses valores devem ser confirmados para a unidade e para o requisito de exportação aplicável.

**Fontes da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:4420063.0-4420096.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2016418.0-2016453.0`, `regis-ef7d62eda3748119ba3e9e9e:pNone:1183.0-1355.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:1403297.0-1403342.0`

## 2. Fundamentos físico-químicos do baixo desempenho

### 2.1. Tamanho de gota, viscosidade e segregação gravitacional

A separação óleo-água melhora quando o diâmetro das gotículas de água aumenta, pois a **velocidade terminal de sedimentação** cresce com o tamanho da gota. De modo qualitativo, a separação gravitacional depende de três grupos principais de variáveis:

- **tamanho das gotas**;
- **diferença de densidade** entre fase dispersa e fase contínua;
- **viscosidade da fase contínua**.

Para o caso de água dispersa em óleo, as condições normalmente são desfavoráveis: pequena diferença de densidade e viscosidade relativamente alta do óleo. O aquecimento ajuda porque **reduz a viscosidade** e tende a facilitar a separação. Para gotículas muito pequenas, a separação pode se tornar muito difícil; a fonte menciona inclusive a importância do movimento Browniano nesse limite.

### 2.2. Como a emulsão se forma e por que pode persistir

Em geral, petróleo e água podem estar mais segregados no reservatório, mas durante o escoamento em tubulações de produção essas fases são submetidas a **agitação e cisalhamento**. Na presença de emulsificantes naturais do petróleo, como asfaltenos, resinas e ácidos naftênicos, formam-se emulsões do tipo **água em óleo (A/O)**: pequenas gotas de água revestidas por um filme interfacial que dificulta o contato entre gotas e, portanto, dificulta a coalescência.

O problema se agrava quando o fluido passa por:

- restrições;
- tubulações com elevada dissipação de energia;
- bombas;
- chokes;
- válvulas de controle de nível ou de pressão entre estágios.

Esses pontos de maior cisalhamento **quebram gotas maiores em gotas menores**, piorando o tratamento subsequente.

### 2.3. O que o campo elétrico faz no tratador

Quando um líquido pouco condutivo (óleo) contendo gotículas de uma fase condutiva (água salina) é submetido a um campo elétrico, a literatura citada descreve três efeitos principais:

1. **polarização e alinhamento** das gotículas de água, favorecendo colisões e coalescência;
2. **atração das gotículas pelo eletrodo**;
3. **enfraquecimento do filme de emulsificantes** na interface da gota, facilitando a coalescência quando ocorre colisão.

Na prática, o TO funciona melhor quando recebe uma alimentação em que a emulsão ainda possa ser desestabilizada por química, calor, campo elétrico e tempo de residência, e piora quando recebe emulsão excessivamente fina, muito viscosa, muito contaminada por sólidos ou fortemente estabilizada por surfactantes naturais.

**Fontes da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:4420063.0-4420096.0`, `regis-382370e69ec038894a313f3f:pNone:0.0-16.60`, `petroles-004c2afadba7ea17c7dd7908:pNone:1403297.0-1403342.0`

## 3. Principais causas de emulsões persistentes e respectivas correções

### 3.1. Cisalhamento excessivo a montante

**Mecanismo:** restrições, bombas, chokes e válvulas entre estágios quebram gotas e produzem dispersões mais finas. Quanto menores as gotas, mais lenta a sedimentação e maior a dependência de química, calor e campo elétrico.

**Sinais típicos:**

- piora do BS&W após mudanças de choke, recirculação ou aumento de vazão;
- piora do tratamento após grandes quedas de pressão entre estágios;
- necessidade crescente de química sem recuperação consistente da performance.

**Correções compatíveis com as fontes:**

- reduzir cisalhamento desnecessário a montante;
- revisar o arranjo de entrada e internos que limitem a região perturbada e controlem melhor a turbulência;
- preferir dispositivos de entrada de trajetória mais suave quando aplicável, pois foram descritos como alternativas projetadas para gerar menos espuma e cisalhamento;
- estabilizar golfadas antes de sobrecarregar o tratamento subsequente.

### 3.2. Temperatura baixa e óleo muito viscoso

**Mecanismo:** viscosidade elevada da fase contínua oleosa reduz a velocidade de segregação das gotas. Além disso, baixas temperaturas podem favorecer espuma e, quando houver risco parafínico, deposição de parafinas.

**Sinais típicos:**

- melhora do tratamento ao elevar temperatura;
- piora concomitante de espuma ou depósitos;
- maior sensibilidade do processo a pequenas mudanças de carga.

**Correções compatíveis com as fontes:**

- elevar a temperatura dentro da janela segura/permitida da planta;
- usar aquecimento como forma de reduzir viscosidade, desestabilizar emulsões e combater espuma;
- manter temperatura acima da TIAC quando houver deposição de parafinas associada.

### 3.3. Desemulsificante inadequado, mal dosado ou mal aplicado

**Mecanismo:** o desemulsificante precisa deslocar os emulsificantes naturais da superfície das gotas para permitir a coalescência. A literatura destaca que **cada petróleo requer formulação específica**, normalmente selecionada pelo fabricante em conjunto com a unidade de produção.

**Sinais típicos:**

- pouca resposta do TO mesmo com calor e tempo de residência adequados;
- forte dependência de pequenas variações de dosagem;
- mudança de comportamento após alteração de origem do fluido ou mistura de poços.

**Correções compatíveis com as fontes:**

- revisar formulação e dosagem com base no petróleo efetivamente processado;
- garantir ponto de injeção e tempo de contato adequados antes do TO;
- considerar que a unidade normalmente injeta também antiespumante, inibidores e outros químicos logo na chegada do fluido, pois essa química influencia tanto a eficiência do tratamento quanto a integridade do sistema.

### 3.4. Sólidos, areia, parafinas e contaminantes interfaciais

**Mecanismo:** sólidos podem estabilizar emulsões, causar erosão, obstruções e perda de volume útil; parafinas podem precipitar e se depositar quando a temperatura cai abaixo da faixa adequada. Ambos degradam hidráulica, controle e eficiência de separação.

**Sinais típicos:**

- aumento de perda de carga ou obstruções;
- drenos com baixa eficiência;
- necessidade frequente de limpeza;
- piora do controle de nível e da estabilidade operacional.

**Correções compatíveis com as fontes:**

- remover sólidos por drenos e sistemas de revolvimento/remoção quando existentes;
- atuar na causa da produção de areia sempre que possível;
- evitar operação abaixo da temperatura de aparecimento de cristais de parafina;
- inspecionar obstruções em internos e linhas de saída.

### 3.5. Sobrecarga hidráulica e tempo de residência insuficiente

**Mecanismo:** mesmo com química e aquecimento, o tratamento perde eficiência se o vaso opera acima da capacidade, com vazão elevada, grandes flutuações de carga ou subdimensionamento. A literatura de separadores destaca que alterações de ajuste e capacidade devem considerar a condição desejada de operação, e que sistemas subdimensionados elevam risco de arraste.

**Sinais típicos:**

- degradação da qualidade do óleo em picos de produção;
- sensibilidade a golfadas;
- arraste em outras correntes do trem de processo;
- melhora temporária ao reduzir carga.

**Correções compatíveis com as fontes:**

- reduzir carga quando possível;
- operar equipamentos em paralelo, se disponível;
- restabelecer remoção de água livre e estabilização de vazão a montante;
- verificar se o problema real é subdimensionamento ou perda de eficiência por internos danificados/obstruídos.

**Fontes da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:4420063.0-4420096.0`, `regis-382370e69ec038894a313f3f:pNone:0.0-16.60`, `regis-ef7d62eda3748119ba3e9e9e:pNone:1183.0-1355.0`, `regis-ef7d62eda3748119ba3e9e9e:pNone:1079.0-1270.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2016436.0-2016470.60`, `petroles-004c2afadba7ea17c7dd7908:pNone:1403297.0-1403342.0`

## 4. Arraste, carryover, carryunder e perda de eficiência no sistema de tratamento

As fontes fornecidas detalham causas de arraste principalmente em **separadores gravitacionais**. Esses mecanismos são úteis para diagnosticar o TO porque o tratador está inserido no mesmo trem hidráulico e depende fortemente da qualidade da alimentação e do controle de nível/interface.

### 4.1. Carryover de líquido para a corrente de gás a montante

A literatura cita como causas clássicas de arraste de óleo pelo gás:

- **nível de líquido muito alto**;
- **dano em componente interno**;
- **formação de espuma**;
- **saída de líquido obstruída**;
- **subdimensionamento do equipamento**.

Consequências: danos a compressores, perturbações no controle e alimentação instável do tratamento de óleo.

### 4.2. Arraste de gás pelo líquido

É citado como indicativo de:

- **nível de líquido muito baixo**; ou
- **falha no sistema de controle de nível**.

Em um trem de tratamento, isso desestabiliza a alimentação subsequente e dificulta manter regime hidráulico previsível no vaso de tratamento.

### 4.3. Espuma como multiplicador de problemas

A espuma reduz a área de escoamento do gás, aumenta arraste de líquido na saída de gás e pode levar instrumentos de nível, alarmes e até shut down a atuar indevidamente. Para mitigá-la, as fontes citam:

- aquecimento dos fluidos;
- uso de **antiespumantes**, preferencialmente à base de silicone.

### 4.4. Interface instável e descarga da fase errada

As fontes enfatizam que o bom desempenho dos vasos depende de controle adequado de **nível** e de uma hidráulica que evite recirculação, zonas mortas, vórtices e grande perturbação na interface. Em separadores, são citados dispositivos quebra-vórtice e tranquilizadores de fluxo; em termos de diagnóstico, a mesma lógica é útil para investigar o circuito do TO quando há:

- água saindo com o óleo tratado;
- óleo saindo com a água produzida;
- oscilação de interface;
- perda súbita de especificação após instabilidade de nível.

**Fontes da seção:** `regis-ef7d62eda3748119ba3e9e9e:pNone:1183.0-1355.0`, `regis-ef7d62eda3748119ba3e9e9e:pNone:1079.0-1270.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2016436.0-2016470.60`, `petroles-004c2afadba7ea17c7dd7908:pNone:215483.0-215532.0`

## 5. Variáveis operacionais que mais afetam o desempenho

### 5.1. Pressão

Nas fontes sobre separadores, reduzir a pressão aumenta o volume de gás liberado do óleo; com isso, a velocidade do gás cresce e aumenta a tendência de arraste de gotículas, reduzindo a capacidade do vaso para a mesma geometria. Ainda que esse comentário seja específico para separadores, ele é relevante para o TO porque uma alimentação mais carregada de gás e mais perturbada tende a degradar o tratamento subsequente.

### 5.2. Temperatura

Quanto maiores a viscosidade e a densidade do fluido, maior tende a ser a necessidade de temperatura de separação. O aumento de temperatura reduz a viscosidade, pode aumentar a diferença de densidade óleo/água e ajuda a minimizar espuma. Logo, temperatura insuficiente é uma causa operacional forte de perda de eficiência.

### 5.3. Nível e estabilidade de vazão

Se o equipamento recebe fluxo regular, é mais fácil manter nível estável e maximizar a eficiência de separação. Flutuações de carga, golfadas e mau ajuste dos instrumentos fazem o vaso operar fora da condição desejada, prejudicando a remoção de contaminantes.

### 5.4. Internos e acessórios

As fontes citam como relevantes para desempenho global do sistema:

- dispositivos de entrada para limitar turbulência;
- tranquilizadores de fluxo;
- extratores de névoa;
- pratos coalescedores;
- dispositivos quebra-vórtice;
- dispositivos/sistemas de remoção de areia.

Em diagnóstico de perda de eficiência, a inspeção desses internos é obrigatória quando há suspeita de dano, obstrução ou alteração do padrão de escoamento.

**Fontes da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:215483.0-215532.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2016436.0-2016470.60`, `petroles-004c2afadba7ea17c7dd7908:pNone:1403297.0-1403342.0`

## 6. Roteiro prático de troubleshooting para baixo desempenho do TO

Uma sequência coerente, consistente com os mecanismos das fontes, é:

1. **Confirmar o sintoma dominante**  
   - BS&W alto?  
   - salinidade alta?  
   - óleo na água produzida?  
   - instabilidade de nível/interface?  
   - espuma, alarmes frequentes ou shut down?

2. **Verificar a alimentação a montante**  
   Procurar mudanças recentes de choke, pressão entre estágios, vazão, bombas, golfadas e qualquer condição que aumente cisalhamento ou liberação de gás.

3. **Checar química**  
   Confirmar formulação, dosagem e ponto de injeção do desemulsificante; revisar também necessidade de antiespumante quando houver espuma.

4. **Checar temperatura**  
   Avaliar se a temperatura está suficiente para reduzir viscosidade, desestabilizar a emulsão e evitar deposição de parafina.

5. **Checar nível, interface e saídas**  
   Obstruções em saídas, controle de nível deficiente, níveis altos/baixos e vórtices podem explicar arraste e perda de especificação.

6. **Inspecionar internos e acúmulo de sólidos**  
   Procurar dano ou obstrução em dispositivos de entrada, internos coalescedores, drenos, quebra-vórtices, extratores de névoa e pontos de acúmulo de areia/parafina.

7. **Avaliar capacidade real versus carga aplicada**  
   Se a performance só é aceitável com carga reduzida, o problema pode ser tempo de residência insuficiente, subdimensionamento ou perda de volume/eficiência por sólidos e danos internos.

Esse roteiro ajuda a separar quatro famílias de causa-raiz: **química inadequada**, **hidráulica ruim**, **térmica insuficiente** e **integridade/obstrução de internos**.

**Fontes da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:4420063.0-4420096.0`, `regis-ef7d62eda3748119ba3e9e9e:pNone:1183.0-1355.0`, `regis-ef7d62eda3748119ba3e9e9e:pNone:1079.0-1270.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:215483.0-215532.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2016436.0-2016470.60`

## 7. Síntese operacional

Em termos práticos, o tratador eletrostático perde eficiência quando recebe uma emulsão **muito fina, muito viscosa, muito estável ou muito carregada de sólidos/espuma**, especialmente sob **sobrecarga hidráulica** e com **controle deficiente de nível/interface**. As ações mais efetivas, segundo os mecanismos descritos nas fontes, são:

- reduzir cisalhamento a montante;
- garantir química adequada ao petróleo processado;
- fornecer temperatura suficiente;
- recuperar tempo de residência e estabilidade de vazão;
- eliminar espuma, obstruções, parafinas e sólidos;
- inspecionar internos e controle de nível quando houver arraste ou perda persistente de especificação.

**Fontes da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:4420063.0-4420096.0`, `regis-382370e69ec038894a313f3f:pNone:0.0-16.60`, `regis-ef7d62eda3748119ba3e9e9e:pNone:1183.0-1355.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:215483.0-215532.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:1403297.0-1403342.0`