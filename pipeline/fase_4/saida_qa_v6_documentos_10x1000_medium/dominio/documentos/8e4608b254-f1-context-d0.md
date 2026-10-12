# Testes de malha e funções instrumentadas

## 1. Contexto operacional e arquitetura relevante para teste
Em FPSOs e outras unidades offshore, o sistema de supervisão e controle pode apresentar variáveis analógicas em tempo real, tendências, alarmes, eventos, estados de equipamentos e comandos operacionais, além de manter histórico e relatórios. Entre as funções supervisionadas citadas nas fontes estão: anunciação de alarmes, reconhecimento pelo operador, mudança de cor de objetos de tela para indicar estados operacionais, registro de eventos, armazenamento/recuperação de dados de equipamentos, comandos de abertura/fechamento de válvulas on-off, modulação de válvulas de controle, alteração de modo manual/automático e mudança de parâmetros de controladores. Também aparecem como funções possíveis a colocação de equipamentos em estado de manutenção, bypass de entradas inicializadoras de ESD e override de saídas para atuadores, sempre em caráter excepcional.  

Para fins de teste e restabelecimento, um ponto central das fontes é a separação entre **supervisão** e **execução da lógica crítica no controlador**. Segundo o material citado, em plataformas de E&P os sistemas de controle, intertravamento e cálculos com restrição temporal devem ser executados diretamente no **CLP**, e não no sistema supervisório, por razões de velocidade, segurança e confiabilidade. Assim, a validação de uma malha ou função instrumentada não pode se limitar à IHM/SSC: ela deve alcançar o caminho completo entre entrada de campo, lógica no controlador e ação final.  

No caso dos sistemas instrumentados de segurança, as fontes descrevem o SIS/ESD como conjunto de **dispositivos de medição, dispositivos lógicos e atuadores** voltados à segurança operacional. A criticidade desses sistemas torna essencial verificar se a lógica implementada no CLP e sua integração com os dispositivos de campo atendem às especificações do sistema.  

_Fontes: `petroles-004c2afadba7ea17c7dd7908:pNone:2452720.0-2452749.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2452729.0-2452771.0`, `regis-2d3da060a3a288efef9b844c:pNone:496.0-718.0`_

## 2. Conceitos essenciais para avaliação de testes e retorno ao serviço
### 2.1 Alarme, evento e resposta operacional
As fontes definem **alarme** como aviso sonoro e/ou visual que indica condição anormal que requer resposta em tempo restrito. Já **evento** é mudança de estado que não requer ação do operador e, portanto, não deveria ser anunciado como alarme; seu uso principal é registro, análise de manutenção, incidentes e monitoração. A configuração inadequada de eventos como alarmes contribui para pseudoalarmes e sobrecarga operacional.

Essa distinção é decisiva em testes de malha, porque um teste bem-sucedido não é apenas aquele que “faz aparecer algo na tela”, mas aquele que confirma que a condição testada produz a **classe correta de resposta**:
- condição que exige ação do operador → alarme;
- simples mudança informativa de estado → evento.

### 2.2 Estados e atributos de alarme
As fontes citam, entre outros conceitos:
- **ativação** do alarme;
- **desativação** quando a condição deixa de existir;
- **desabilitação** da anunciação, mesmo existindo condição de ativação;
- **inibição** como desabilitação temporária e controlada por ação manual;
- **supressão** como impedimento automático da ativação em condição pré-estabelecida;
- **prioridade** do alarme;
- **grupo de alarmes**;
- **eclipse**, quando um nível superior substitui um nível inferior na mesma medição;
- **alarme de sistema**, gerado por falhas de hardware/software ou elementos de campo/comunicação;
- **reconhecimento**, pelo qual o operador confirma ciência da anormalidade;
- **tempo de resposta**, intervalo entre a anunciação e o início da ação corretiva.

Para manutenção, inspeção e restabelecimento, esses conceitos importam porque o teste deve verificar não só a atuação da lógica, mas também se o alarme foi configurado com os atributos esperados e se retorna ao estado normal corretamente após o fim da condição de teste.

### 2.3 Alarmes incômodos, pseudoalarmes e avalanche de alarmes
As fontes destacam que alarmes e eventos são frequentemente configurados de forma semelhante, gerando pseudoalarmes. Também definem **alarme incômodo** como aquele que anuncia excessivamente, desnecessariamente ou não retorna ao normal após a resposta correta. Já a **avalanche de alarmes** é a ocorrência de muitos alarmes em curto período, a ponto de o operador não conseguir gerenciá-los.

Na prática de testes e comissionamento/manutenção, isso significa que um sistema pode estar “funcionando” do ponto de vista lógico e, ainda assim, estar **mal configurado operacionalmente**. Uma restauração inadequada após teste pode produzir exatamente esse tipo de degradação: alarmes deixados desabilitados, prioridades indevidas, eventos anunciados como alarmes ou retorno incorreto ao normal.

_Fontes: `petroles-004c2afadba7ea17c7dd7908:pNone:2452729.0-2452771.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2452751.0-2452797.0`_

## 3. Documentos-base para teste, validação e rastreabilidade
### 3.1 Filosofia de alarmes
As fontes definem **filosofia de alarmes** como a documentação que estabelece definições básicas, princípios e procedimentos para projetar, implementar e manter o sistema de alarmes. A **racionalização** é a análise dos alarmes com base nessa filosofia para fundamentar sua concepção.

Para teste e restabelecimento, a filosofia de alarmes funciona como referência para confirmar pelo menos:
- o que deve ser alarme e o que deve ser evento;
- prioridade e agrupamento;
- forma de anunciação;
- comportamento em bypass/inibição/supressão;
- critérios de apresentação ao operador.

### 3.2 Matriz de Causa e Efeito (C&E)
No material da coleção REGIS, a **matriz de causa e efeito** é apresentada como documento que define a relação entre sinais de campo que indicam situações críticas e as ações de segurança correspondentes. O texto a trata como documento essencial para a **programação** e para a **validação** dos SIS.

Sob a ótica de manutenção e testes, isso é crucial: a validação de intertravamentos e funções instrumentadas deve confrontar o comportamento real do sistema com a relação causa→efeito formalmente especificada. Em termos práticos, a matriz C&E sustenta perguntas e avaliações como:
- qual variável/iniciador deve disparar a ação;
- qual ação de segurança deve ocorrer;
- quais efeitos são automáticos e quais dependem de intervenção manual;
- como tratar múltiplas causas concorrentes;
- quais saídas e permissivos devem mudar de estado.

O mesmo texto ressalta que erros de especificação podem causar sérios prejuízos e apresenta, em estudo citado, participação relevante de falhas de especificação e de alterações pós-comissionamento em acidentes relacionados a falhas de segurança. Para gestão de integridade, isso reforça a necessidade de manter documentação de teste e de mudança coerente com a lógica em serviço.

_Fontes: `petroles-004c2afadba7ea17c7dd7908:pNone:2452729.0-2452771.0`, `regis-2d3da060a3a288efef9b844c:pNone:496.0-718.0`_

## 4. O que deve ser efetivamente verificado em um teste de malha ou função instrumentada
Com base nas fontes, a avaliação técnica de uma malha, alarme, intertravamento ou função de segurança deve abranger pelo menos três planos: **campo**, **lógica** e **supervisão/registro**.

### 4.1 Plano de campo
No plano de campo, interessa verificar se o sinal ou estado originado pelo dispositivo de entrada representa corretamente a condição de processo ou condição simulada de teste. As fontes não detalham procedimento metrológico, mas deixam claro que sensores e variáveis medidas alimentam tanto o BPCS quanto o SIS para execução de lógicas e geração de alarmes.

### 4.2 Plano lógico no controlador
No plano lógico, interessa confirmar se a lógica no CLP executa corretamente a resposta prevista, especialmente em funções com restrição temporal e em intertravamentos de segurança. Como o material afirma que controle, intertravamento e cálculos temporicamente críticos devem ficar no controlador, a aprovação do teste precisa demonstrar coerência entre o comportamento observado e a lógica especificada, preferencialmente referenciada à matriz C&E quando se tratar de SIS/ESD.

### 4.3 Plano supervisório, de anunciação e de histórico
No plano supervisório, as fontes permitem verificar se:
- o alarme foi anunciado na IHM/SSC;
- a prioridade e a forma de apresentação estão corretas;
- o operador pode reconhecê-lo adequadamente;
- o evento/alarmística foi registrado em log/histórico;
- o estado do equipamento ou da variável é mostrado de forma coerente.

As fontes citam ainda geração de tendências, registro histórico de variáveis, registro de eventos, histórico de falha/manutenção e relatórios. Em contexto de pós-teste, esses registros servem como evidência objetiva de execução, resultado e retorno ao normal.

### 4.4 Testes que envolvem primeiro trip
As fontes descrevem a **lógica de primeiro trip** como método para identificar qual inicializador atuou primeiro em cenários com múltiplos alarmes/intertravamentos. Também descrevem uma estratégia em que o primeiro alarme é gravado em buffer e, após isso, os demais ficam impedidos de gravar o bit correspondente naquele buffer.

Isso é especialmente importante em testes e análises de falha porque, em sistemas com interações entre equipamentos, efeitos secundários podem mascarar a causa primária. O exemplo dado nas fontes é o de duas bombas em série/booster: a parada da primeira pode levar a segunda a parar por baixa sucção. Se a interação não for prevista, ambas podem parecer ter parado pela “mesma causa”, quando na verdade a causa primária foi a parada do equipamento anterior. Portanto, a validação deve confirmar que o sistema registra corretamente a **causa iniciadora** e não apenas as consequências em cascata.

_Fontes: `petroles-004c2afadba7ea17c7dd7908:pNone:2452720.0-2452749.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2452751.0-2452797.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2452994.0-2453045.0`, `regis-2d3da060a3a288efef9b844c:pNone:496.0-718.0`_

## 5. Bypass, override, inibição e controle de acesso durante testes
As fontes tratam o **bypass de pontos de entrada inicializadores de ESD** e o **override de pontos de saída** como operações excepcionais, sujeitas a procedimento específico, documentação e análise de risco. Também afirmam que tais operações não devem ficar disponíveis indistintamente a qualquer usuário: há categorias de acesso, e comandos mais críticos exigem autorização hierárquica superior.

Para avaliação profissional de testes e restabelecimento, isso implica que um teste em função instrumentada não é aceitável apenas por ter atingido o resultado lógico esperado; ele deve também ser analisado sob o ponto de vista de **governança operacional**:
- o bypass/override era realmente necessário?
- houve autorização compatível com a criticidade?
- a condição excepcional foi documentada?
- os riscos temporários foram avaliados?
- a condição excepcional foi removida ao final?

As fontes também definem **inibição** como desabilitação manual e temporária do alarme e **supressão** como bloqueio automático sob condição pré-estabelecida. Em teste, a distinção importa porque o tratamento de retorno ao serviço não é o mesmo:
- inibições e bypasses manuais exigem reversão explícita e confirmação;
- supressões automáticas dependem do retorno da condição de processo/lógica que as habilita.

_Fontes: `petroles-004c2afadba7ea17c7dd7908:pNone:2452720.0-2452749.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2452729.0-2452771.0`_

## 6. Restabelecimento após teste: itens críticos a confirmar
As fontes não fornecem um procedimento completo de restabelecimento, mas oferecem elementos suficientes para identificar o que tipicamente precisa ser conferido antes de considerar a malha/função restaurada.

### 6.1 Reversão de estados e parâmetros alterados durante o teste
Como o sistema supervisório/controlador pode permitir:
- alterar status de equipamento para **manutenção**;
- mudar válvulas de **manual para automático** e vice-versa;
- alterar **setpoint** e **ganhos** de controladores;
- modificar dados de referência de cálculos/totalizadores;
- aplicar **bypass** de entradas e **override** de saídas;

o restabelecimento deve incluir a reversão explícita dos itens que foram modificados para viabilizar o teste.

### 6.2 Reativação da proteção e da anunciação
Após o teste, deve-se confirmar que:
- alarmes desabilitados/inibidos voltaram ao regime normal previsto;
- pontos em bypass foram restituídos à condição de proteção ativa;
- overrides foram removidos, devolvendo a saída à lógica normal;
- a anunciação visual/sonora voltou a operar conforme prioridade e filosofia aplicáveis;
- o sistema voltou a registrar ocorrências em log/eventos.

### 6.3 Coerência entre estado real e representação na IHM
As fontes indicam mudança de cor de objetos para estados de equipamento e para ocorrências de alarme. Também mencionam que, quando um dispositivo indicativo de alarme estiver em bypass, a cor do objeto deve acompanhar o estado real da chave, sem indicação piscante, e o TAG deve ficar em laranja. Isso mostra que, no retorno ao serviço, não basta remover a condição de teste; é necessário confirmar que a representação gráfica e a condição lógica voltaram a ser coerentes entre si.

### 6.4 Reset de registros auxiliares de diagnóstico
Como a detecção de primeiro trip utiliza buffer/memória para armazenar a causa inicializadora, o pós-teste deve assegurar que a informação remanescente do teste não seja confundida com evento real futuro. Em termos de integridade operacional, isso significa limpar ou normalizar os mecanismos de diagnóstico usados apenas para identificar a sequência do teste.

_Fontes: `petroles-004c2afadba7ea17c7dd7908:pNone:2452720.0-2452749.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2452994.0-2453045.0`_

## 7. Anunciação, interface com operador e evidências do teste
As fontes trazem elementos úteis para avaliar se a resposta do sistema ao operador está adequada após manutenção ou teste:
- mensagens de alarme com diferenciação por prioridade por meio de cor;
- anunciação sonora diferenciada por prioridade;
- reconhecimento de alarme pelo operador;
- páginas/telas específicas associadas à anormalidade;
- logs de alarmes e eventos;
- tendências e históricos.

Do ponto de vista de integridade, isso permite tratar a IHM/SSC não só como interface de operação, mas também como parte da **evidência de validação**. Uma função pode atuar fisicamente, porém ainda assim estar inadequada se:
- a prioridade estiver incorreta;
- o texto/mensagem dificultar entendimento;
- o alarme não aparecer na tela apropriada;
- o som ou a cor não corresponderem à criticidade esperada;
- o registro histórico não ficar disponível para auditoria/análise posterior.

As fontes também ressaltam que um bom sistema de alarme auxilia a tomada de decisão do operador, reduz demanda de atuação do ESD e diminui perdas de produção, aumentando a segurança operacional. Em manutenção e restabelecimento, esse é um critério importante: restaurar a lógica sem restaurar a capacidade de percepção e resposta do operador é restauração incompleta.

_Fontes: `petroles-004c2afadba7ea17c7dd7908:pNone:2452751.0-2452797.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2452994.0-2453045.0`_

## 8. Integridade funcional, independência e confiabilidade do SIS
As fontes descrevem sistemas de segurança em plantas de processo como compostos por múltiplas **barreiras de proteção**. A escolha de quantas barreiras usar depende de análise de perigos, normas aplicáveis e engenharia de segurança. Para que uma barreira seja considerada independente, o material menciona que ela deve ser específica, independente, confiável e auditável, além de atingir a redução de risco pretendida.

Um ponto importante para avaliação de testes é que as fontes afirmam que a barreira formada por **controles básicos, alarmes de processo e supervisão do operador** não é, na prática, tratada como camada de proteção independente, devido a mudanças frequentes no processo ao longo da vida da planta sem validação de integridade funcional correspondente. Isso reforça a diferença entre:
- testar o desempenho do BPCS/alarmística; e
- testar uma função de segurança que de fato componha um SIS/IPL independente.

As fontes também associam o SIS ao conceito de **SIL** e mencionam uso de **CLPs com arquiteturas redundantes**, incluindo configuração dual-simplex/hot standby em plataformas Petrobras. Também indicam que a escolha de configuração deve considerar desempenho de segurança e custo do ciclo de vida, com prioridade para o desempenho de segurança.

Em contexto de manutenção e testes, isso se traduz em um princípio prático: intervenções em SIS não devem ser avaliadas apenas por facilidade operacional ou tempo de parada. Deve-se considerar o impacto temporário na disponibilidade da função de segurança e na manutenção da independência/auditabilidade da barreira.

_Fontes: `petroles-004c2afadba7ea17c7dd7908:pNone:2475571.0-2475607.60`, `petroles-004c2afadba7ea17c7dd7908:pNone:2475592.0-2475621.0`_

## 9. Síntese aplicada à manutenção e integridade
À luz das fontes, a avaliação de testes e do restabelecimento de malhas de controle, alarmes, intertravamentos e funções de segurança em FPSO deve considerar simultaneamente:
1. **correção funcional** da lógica no CLP;
2. **aderência documental** à filosofia de alarmes e à matriz C&E, quando aplicável;
3. **controle de exceções** como bypass, override, inibição e supressão;
4. **qualidade da interação com o operador**, evitando pseudoalarmes e avalanches;
5. **rastreabilidade** por meio de logs, históricos, registros de eventos e evidências de primeiro trip;
6. **restauração completa** dos estados, parâmetros e permissões alterados durante o teste;
7. **preservação da integridade funcional** e da independência das barreiras de segurança.

Em outras palavras, testar e restabelecer corretamente uma função instrumentada não é só comprovar que ela “atuou”; é comprovar que atuou pela causa certa, com a sequência certa, na camada certa, com a anunciação certa, com governança adequada das exceções e com retorno seguro ao regime normal de operação.

_Fontes: `petroles-004c2afadba7ea17c7dd7908:pNone:2452720.0-2452749.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2452729.0-2452771.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2452751.0-2452797.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2452994.0-2453045.0`, `regis-2d3da060a3a288efef9b844c:pNone:496.0-718.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2475571.0-2475607.60`, `petroles-004c2afadba7ea17c7dd7908:pNone:2475592.0-2475621.0`_