# EERA, ESSA e abandono em FPSOs

> **Nota de escopo:** este texto consolida apenas os trechos fornecidos. Ele serve como base técnica para treinamento e avaliação profissional, **não** como interpretação normativa certificada nem como substituto de estudos formais da unidade.

## 1. Inserção de EERA/ETRERA e ESSA no conjunto de estudos de segurança

Nos trechos fornecidos, o *Safety Case* do FPSO Cidade de São Mateus foi descrito como o documento que demonstra: (i) identificação dos perigos, (ii) avaliação dos riscos, (iii) adoção de medidas de controle para reduzir os riscos a nível **ALARP**, e (iv) descrição do sistema de gestão que sustenta a aplicação consistente desses controles. Dentro desse conjunto, aparecem explicitamente:

- **ETRERA** (*Escape, Temporary Refuge, Evacuation and Rescue Analysis*), isto é, estudo de escape, refúgio temporário, evacuação e resgate;
- **ESSA** (*Emergency Systems Survivability Analysis*), isto é, análise de sobrevivência dos sistemas de emergência.

Os próprios trechos indicam que esses estudos compõem a base formal do *Safety Case* ao lado de HAZID, HAZOP, FEA e QRA. Também consta que o manual de implementação do *Safety Case* aplicava esse escopo a **novos projetos, conversões e modificações/aprimoramentos** em unidades existentes. Logo, EERA/ETRERA e ESSA não devem ser tratados como estudos “de projeto apenas”; eles precisam continuar úteis quando a configuração operacional, os meios de evacuação, o POB ou os recursos de resposta forem alterados.

Na faceta de abandono e sobrevivência de sistemas de emergência, a leitura integrada dos trechos mostra a seguinte lógica:

1. **EERA/ETRERA** dá suporte à definição e verificação de:
   - rotas de fuga;
   - refúgios temporários;
   - pontos de encontro;
   - meios de evacuação e abandono;
   - interface com resgate e apoio externo.
2. **ESSA** dá suporte à verificação de que funções e recursos de emergência continuam disponíveis tempo suficiente, mesmo após danos, perda de utilidades ou escalonamento do acidente.
3. Os resultados desses estudos precisam alimentar o **PRE**, a estratégia de resposta, os simulados, o controle de pessoas e as decisões operacionais sob emergência.

**Fontes da seção:** `anp-dabfb60617e4f0ede433578e:p69-72:23.0-19.0`, `anp-dabfb60617e4f0ede433578e:p9-12:0.0-11.0`

## 2. O que um EERA precisa demonstrar na prática

Pelos exemplos fornecidos, um estudo de escape, refúgio, evacuação e resgate só é operacionalmente útil se demonstrar, em termos práticos, que as pessoas conseguem:

- sair das áreas de risco inicial;
- atingir pontos de encontro compatíveis com o cenário acidental em curso;
- permanecer em refúgio temporário sem exposição indevida a explosão, fumaça, perda de integridade estrutural ou escalonamento;
- migrar para meios de evacuação/abandono quando houver ordem de abandono;
- ser contabilizadas e resgatadas mesmo com dano parcial de sistemas e desorganização inicial.

Os trechos do acidente mostram que o problema não é apenas “existir rota” ou “existir baleeira”, mas sim a **robustez do arranjo diante de degradação real**. Entre os aspectos que se revelam críticos:

### 2.1 Rotas principais e secundárias

A literatura técnica presente no material destaca que, já no desenvolvimento do *layout* do FPSO, as rotas de fuga entre áreas de processo, superestrutura e refúgios temporários têm grande importância. Também são citadas as rotas secundárias para uso quando as principais estiverem impedidas, além da possibilidade de túneis de escape protegidos em unidades mais congestionadas.

Isso é coerente com o acidente analisado: após a explosão, as pessoas foram deslocadas sucessivamente para diferentes áreas, com medo de novas explosões, fumaça, água de incêndio e danos estruturais. Portanto, a avaliação de escape não pode presumir caminho único nem manter válida, sem rechecagem, a rota pensada para operação normal.

### 2.2 Compatibilidade entre cenário e ponto de encontro

O caso mostra que pontos de encontro só são adequados se permanecerem seguros frente aos cenários acidentais relevantes. A ANP registrou que não foi evidenciada a existência de estudos que avaliassem a segurança dos pontos de encontro destinados às pessoas com função de resposta à emergência, nem pontos alternativos quando os originais fossem inseguros.

Assim, em termos profissionais, um EERA deve pelo menos sustentar respostas como:

- qual ponto de encontro é aceitável para o POB geral em cada macrocenário;
- qual ponto de encontro é aceitável para equipes de resposta;
- quando um ponto deixa de ser aceitável;
- para onde migrar, com que gatilho decisório e por qual rota;
- como evitar que a migração exponha pessoas a riscos não contemplados.

### 2.3 Interface com o layout da unidade

O material acadêmico incluído aponta que a disposição entre superestrutura, área de processo e meios de evacuação deve buscar redução da exposição do pessoal aos perigos previsíveis da armazenagem/processamento de óleo e gás. Também relaciona o tema à operacionalidade do heliponto e ao acesso livre às rotas de escape.

Ainda que esse trecho não seja normativo, ele reforça um princípio útil: **EERA começa no layout**. Se o arranjo físico induz atravessamento de áreas congestionadas, proximidade excessiva com fontes de hidrocarbonetos ou dependência de rotas facilmente bloqueáveis, a degradação operacional em acidente tende a ser rápida.

**Fontes da seção:** `anp-dabfb60617e4f0ede433578e:p237-242:20.0-15.0`, `anp-dabfb60617e4f0ede433578e:p49-52:12.0-0.0`, `regis-a50877419ec61449c9277f90:pNone:3661.0-3915.0`

## 3. Refúgio temporário e disciplina de permanência

Um dos pontos mais fortes dos trechos é que **o valor do refúgio temporário depende tanto de sua localização quanto da disciplina de ocupação/manutenção da condição de abrigo**.

No acidente do FPSO Cidade de São Mateus:

- a situação ainda era de emergência, com evidências de atmosfera explosiva;
- mesmo assim, houve desmobilização do ponto de encontro do refúgio temporário (refeitório) e desmobilização parcial de outros pontos;
- pessoas passaram a agir como se estivessem em condição normal, indo trocar roupa para almoço e usando elevador;
- quando a explosão ocorreu, várias estavam fora do abrigo previsto e foram feridas.

A investigação concluiu que essa desmobilização expôs pessoas a riscos **não contemplados pelo estudo usado para definição do refúgio temporário**. Em outras palavras: o estudo pode ter sido feito para determinada ocupação e determinado comportamento esperado; ao romper essa premissa durante a emergência, a proteção planejada foi perdida.

### Implicações técnicas

1. **Refúgio temporário não é apenas uma sala designada**; é uma condição operacional que exige permanência, controle e comando consistentes.
2. A ordem de desmobilização não pode ser baseada em percepção informal de controle se persistirem indícios objetivos de cenário perigoso.
3. Condutas típicas de rotina — como deslocar-se aos camarotes, preparar-se para refeição ou usar elevadores — podem se tornar incompatíveis com a fase de abrigo.
4. O EERA precisa dialogar com o PRE e com o sistema de comando a emergências, para que a decisão de manter ou dissolver pontos de encontro seja tecnicamente sustentada.

A própria ANP classificou essa falha como associada à exposição de pessoas e à falta de conscientização da força de trabalho. Portanto, a avaliação de refúgio não pode ser separada de treinamento, comando e disciplina operacional.

**Fontes da seção:** `anp-dabfb60617e4f0ede433578e:p236-239:13.0-17.0`, `anp-dabfb60617e4f0ede433578e:p237-242:20.0-15.0`

## 4. Pontos de encontro de equipes de resposta: exposição ocupacional diferenciada

Os trechos mostram distinção importante entre:

- pessoas que devem permanecer em refúgio temporário; e
- pessoas com função de resposta, que podem precisar posicionar-se fora do refúgio para atuar na mitigação.

Esse arranjo cria uma exigência adicional: **os pontos de encontro e posições de prontidão das equipes de resposta também precisam ser analisados contra os cenários acidentais plausíveis**.

Na investigação do acidente, a ANP apontou que não foi possível evidenciar estudos que avaliassem a segurança desses pontos para a brigada e demais funções de emergência, nem a definição de alternativas quando os locais designados se tornassem inseguros. O caso concreto mostrou consequências severas:

- ruptura de antepara entre casa de bombas e praça de máquinas;
- morte de operador em ponto de encontro dentro do ECR;
- ferimentos graves em pessoas próximas ao bote de resgate rápido, atingidas por sobrepressão.

### Consequência para EERA/ESSA

A análise não pode tratar a equipe de resposta como “recurso abstrato sempre disponível”. A própria brigada pode se tornar vítima do cenário, perdendo:

- capacidade de comando;
- capacidade de busca e salvamento;
- capacidade de atendimento inicial a feridos;
- capacidade de lançamento e guarnecimento de meios de abandono.

Por isso, a segurança dos locais de espera, apoio e aproximação das equipes de emergência é parte do problema de escape/evacuação/resgate e, ao mesmo tempo, parte da sobrevivência dos sistemas de emergência em sentido funcional.

**Fontes da seção:** `anp-dabfb60617e4f0ede433578e:p237-242:20.0-15.0`

## 5. Abandono real: o que o caso evidencia sobre baleeiras, contagem e comando

Os eventos posteriores à explosão no FPSO Cidade de São Mateus mostram vários modos de falha do abandono em condição degradada.

### 5.1 Perda de estrutura de comando e atendimento

A explosão causou morte de lideranças da brigada, ferimentos em socorristas e danos à enfermaria. Isso comprometeu simultaneamente:

- busca de desaparecidos;
- atendimento médico a bordo;
- organização do abandono;
- clareza de contagem de pessoas.

Ou seja, o abandono não falhou apenas por problema em embarcação salva-vidas, mas pela **quebra de várias funções de emergência em cascata**.

### 5.2 Contagem de pessoas e controle de POB

No ponto de abandono da baleeira de boreste, os cartões de identificação foram perdidos, e a lista de pessoas a bordo disponível estava desatualizada. A contagem passou a ser feita manualmente, por chamada, e só depois chegou um POB atualizado para recontagem.

Esse trecho mostra que o controle de pessoas é uma barreira crítica para abandono. Sem controle confiável de POB e meios associados de checagem, surgem atrasos, incerteza sobre desaparecidos e decisões equivocadas sobre busca versus abandono.

### 5.3 Guarnecimento e operação da baleeira

A tripulação mínima necessária para a navegação da baleeira estava incompleta devido aos ferimentos do pessoal treinado. Foi necessário acionar outra pessoa com algum conhecimento, mas o próprio relatório registra dificuldade de lançamento/liberação e insuficiência de conhecimento prático na condução da embarcação.

Logo, a prontidão de abandono depende de mais do que “equipamento instalado”:

- pessoal treinado precisa estar disponível mesmo após impacto inicial do acidente;
- substituições improvisadas tendem a reduzir a confiabilidade da manobra;
- a análise deve considerar indisponibilidade de operadores-chave por morte, lesão ou isolamento.

### 5.4 Evacuação aeromédica e condicionantes do heliponto

O material informa que o resgate dos feridos graves por helicóptero ocorreu **após confirmação de ausência de gás inflamável no heliponto**. Isso mostra a dependência entre estudos de dispersão/gás, decisão de uso do helideck e estratégia de evacuação médica.

Em termos de análise, o heliponto não é automaticamente disponível após explosão/incêndio; sua utilização pode depender de:

- atmosfera segura para pouso/decolagem;
- integridade estrutural e de acesso;
- comunicações e coordenação com apoio externo.

### 5.5 Sequenciamento e hesitação no abandono

O relato também mostra hesitação e divergência comportamental: algumas pessoas não queriam retornar para áreas próximas ao casario e à casa de bombas para usar baleeira, preferindo balsas infláveis em outra região. Isso indica que, em cenário real, a percepção de risco local influencia fortemente a aderência à estratégia formal de abandono.

Portanto, o EERA e o PRE precisam ser compreensíveis e treinados o suficiente para reduzir improviso e disputa entre rotas/meios concorrentes.

**Fontes da seção:** `anp-dabfb60617e4f0ede433578e:p49-52:12.0-0.0`

## 6. ESSA na prática: sobrevivência funcional dos sistemas de emergência

Os trechos fornecidos quase não detalham a metodologia de ESSA, mas o caso investigado permite inferir seu foco funcional: verificar se os **sistemas, recursos e funções de emergência** sobrevivem ao evento por tempo e em condições suficientes para sustentar abrigo, evacuação, abandono e resgate.

No material, aparecem exemplos claros de perda de sobrevivência funcional:

- **comunicações degradadas:** cerca de vinte minutos após a explosão, as comunicações entre a plataforma e escritórios da Petrobras foram perdidas em razão do término da carga da UPS, restando comunicação via rádio de emergência e intermediação por outra unidade;
- **função médica degradada:** a enfermaria foi destruída pela sobrepressão, prejudicando o atendimento aos feridos;
- **estrutura de resposta degradada:** morte/ferimento de lideranças e socorristas comprometeu busca e atendimento;
- **meios de abandono degradados funcionalmente:** perda de pessoal treinado, perda de cartões de identificação e dificuldade na liberação/navegação da baleeira;
- **uso condicionado do helideck:** necessidade de confirmar ausência de gás inflamável antes do resgate aeromédico.

### Leitura técnica útil

Assim, mesmo sem um método completo explícito nos trechos, a análise de sobrevivência deve considerar pelo menos a permanência das seguintes funções:

1. comando e comunicações de emergência;
2. detecção/avaliação da atmosfera para tomada de decisão;
3. atendimento inicial a feridos;
4. controle de POB e identificação de faltantes;
5. disponibilidade real dos meios de evacuação/abandono;
6. interface segura com resgate externo.

Se uma dessas funções colapsa cedo demais, a unidade pode até ter equipamentos instalados, mas não terá **capacidade efetiva** de executar o abandono com segurança.

**Fontes da seção:** `anp-dabfb60617e4f0ede433578e:p49-52:12.0-0.0`, `anp-dabfb60617e4f0ede433578e:p237-242:20.0-15.0`

## 7. Mudanças operacionais exigem revisão de EERA e PRE

O trecho sobre a P-62 é particularmente importante porque mostra uma falha de gestão: a unidade operava com duas baleeiras retiradas, mantendo operações com POB diurno da ordem de 500 pessoas, enquanto as duas baleeiras remanescentes totalizavam 160 vagas, e a estratégia de escape/abandono estava sendo feita com apoio de *gangway* ligada a unidade acoplada.

Segundo o material, foram identificados desvios críticos, entre eles:

- falta de previsão na gestão de mudanças para revisar o **EERA** e o **PRE** para a nova condição;
- falta de simulados para a nova condição operacional;
- falta de análise de risco sobre indisponibilidade da *gangway* em desconexões rotineiras e de emergência;
- falta de análise técnica da habitabilidade da acomodação temporária em caso de desconexão e indisponibilidade da *gangway*;
- falta de garantia das rotinas de manutenção e inspeção das baleeiras remanescentes.

### Lições objetivas

1. **Mudança temporária também é mudança relevante para EERA/abandono.**
2. Não basta introduzir um meio alternativo de escape; é preciso analisar sua indisponibilidade nos momentos mais críticos.
3. Capacidade nominal de meios de abandono deve ser confrontada com o POB real da condição operacional.
4. Habitabilidade e abrigo de acomodações temporárias entram no problema de refúgio/evacuação.
5. O PRE e os simulados precisam ser reconfigurados para o novo arranjo.

Esse trecho reforça diretamente a aplicabilidade do *Safety Case* e de seus estudos às **modificações e aprimoramentos** da unidade, e não apenas ao desenho original.

**Fontes da seção:** `anp-2d117d40b4b79e409c88509a:p48-51:21.0-6.0`, `anp-dabfb60617e4f0ede433578e:p69-72:23.0-19.0`

## 8. Cenários acidentais, simulados e recursos externos

A investigação do Cidade de São Mateus também apontou falha no planejamento de situações de emergência porque os cenários de **atmosfera explosiva (gás não ignitado)** ou **explosão** não figuravam entre os cenários previstos para simulação pela equipe de resposta. Além disso, não havia registros de simulados que demandassem acionamento de recursos externos indicados no PRE como níveis II e III.

Esse ponto é decisivo para EERA/abandono porque muitos arranjos parecem adequados em papel, mas colapsam quando o cenário envolve simultaneamente:

- gás inflamável ainda não ignitado;
- necessidade de manter pessoas em refúgio por período incerto;
- possibilidade de transição brusca para explosão;
- perda parcial de comunicações e lideranças;
- necessidade de resgate aeromédico e apoio de embarcações externas.

Em consequência, a utilidade dos estudos depende de sua tradução em:

- cenários de simulado coerentes com os perigos identificados;
- critérios claros para mobilização, manutenção ou desmobilização de pontos de encontro;
- acionamento tempestivo de apoio externo;
- treinamento sobre condutas proibidas ou incompatíveis com emergência em curso.

**Fontes da seção:** `anp-dabfb60617e4f0ede433578e:p236-239:13.0-17.0`, `anp-dabfb60617e4f0ede433578e:p9-12:0.0-11.0`

## 9. Critérios práticos de verificação derivados dos trechos

Sem introduzir critérios numéricos não presentes no material, os trechos permitem organizar um conjunto de verificações qualitativas e semiquantitativas para EERA/ESSA e abandono:

### 9.1 Para rotas de fuga e refúgio

- As rotas principais e secundárias permanecem transitáveis sob fumaça, danos e inundação parcial por água de incêndio?
- Há risco de a rota conduzir pessoas para zonas expostas a sobrepressão, explosão secundária ou gás inflamável?
- O refúgio temporário selecionado continua aceitável em cada cenário relevante?
- Existe regra clara para impedir desmobilização prematura do refúgio?
- Há proibição operacional efetiva de uso de elevadores e outras facilidades incompatíveis com emergência?

### 9.2 Para equipes de resposta

- Os pontos de prontidão da brigada e apoio foram avaliados contra os cenários acidentais plausíveis?
- Há locais alternativos para quando o ponto original se tornar inseguro?
- A estratégia reduz ou aumenta a exposição da própria equipe que deveria responder?

### 9.3 Para abandono

- Os meios de abandono disponíveis cobrem o POB real da condição operacional, e não apenas o POB de projeto?
- Há redundância de pessoal treinado para operação das baleeiras?
- Os mecanismos de contagem, T-cards e POB permanecem confiáveis após dano e desorganização inicial?
- O helideck é utilizável com base em critérios objetivos de atmosfera segura?
- A interface com embarcações e apoio aeromédico foi treinada e exercitada?

### 9.4 Para ESSA / sobrevivência funcional

- Quanto tempo as comunicações críticas sobrevivem após perda de energia principal?
- A função médica de emergência permanece disponível ou possui alternativa praticável?
- Os recursos externos são acionados cedo o suficiente?
- A perda de alguns respondedores-chave inviabiliza o abandono ou existe substituição treinada?

### 9.5 Para gestão de mudança

- Toda remoção temporária de baleeiras, uso de *gangway* como rota crítica, acomodação temporária ou alteração relevante de POB gera revisão do EERA e do PRE?
- A nova condição foi simulada?
- Foram avaliadas indisponibilidades transitórias do novo arranjo, como desconexão de *gangway*?

**Fontes da seção:** `anp-dabfb60617e4f0ede433578e:p236-239:13.0-17.0`, `anp-dabfb60617e4f0ede433578e:p237-242:20.0-15.0`, `anp-dabfb60617e4f0ede433578e:p49-52:12.0-0.0`, `anp-2d117d40b4b79e409c88509a:p48-51:21.0-6.0`, `regis-a50877419ec61449c9277f90:pNone:3661.0-3915.0`

## 10. Síntese técnica

Os trechos convergem para uma conclusão prática: em FPSOs, **escape, refúgio, evacuação, abandono, resgate e sobrevivência dos sistemas de emergência formam um único problema integrado**. Não basta haver estudo formal arquivado, nem equipamentos instalados. É necessário que:

- o estudo seja compatível com a configuração real da unidade;
- o PRE reflita os cenários efetivamente plausíveis;
- os pontos de encontro e refúgios sejam seguros para ocupantes e respondedores;
- o abandono permaneça executável mesmo com perda de pessoas-chave, de comunicações e de áreas críticas;
- modificações temporárias ou permanentes disparem revisão formal de EERA e PRE;
- simulados incluam cenários de alta severidade e acionamento de recursos externos.

Os casos fornecidos mostram que falhas nesses pontos tendem a converter um evento inicial em **exposição humana ampliada, perda de controle da resposta e abandono degradado**.

**Fontes da seção:** `anp-dabfb60617e4f0ede433578e:p69-72:23.0-19.0`, `anp-dabfb60617e4f0ede433578e:p236-239:13.0-17.0`, `anp-dabfb60617e4f0ede433578e:p237-242:20.0-15.0`, `anp-dabfb60617e4f0ede433578e:p49-52:12.0-0.0`, `anp-2d117d40b4b79e409c88509a:p48-51:21.0-6.0`