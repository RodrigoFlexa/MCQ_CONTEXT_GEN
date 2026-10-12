# Controle da transferência de carga em operações de offloading

## 1. Escopo técnico desta faceta
Esta faceta trata do **controle operacional da transferência de petróleo** entre o FPSO e o navio aliviador, com ênfase em:
- alinhamento e comando do sistema de carga;
- sequência de preparação e bombeio;
- monitoramento de vazão, pressão, temperatura, nível e estado de equipamentos;
- coordenação entre FPSO e aliviador por telemetria e comunicação operacional;
- atuação humana, automação e resposta a anormalidades.

As fontes recebidas não trazem uma filosofia completa e padronizada de offloading para todos os arranjos de FPSO, mas permitem consolidar uma base técnica consistente para entender **como o sistema deve ser monitorado e controlado** durante a operação.

---

## 2. Arquitetura básica de controle da transferência

Em operação real de FPSO, o sistema de transferência de carga pode ser acompanhado por um **sistema supervisório com IHM**, instalado em uma sala de controle dedicada à marinha/carga. No caso descrito pela ANP, o monitoramento do sistema de transferência entre tanques era feito na **CCRM (sala de controle de marinha)**, e a operação era conduzida pelo **operador de marinha (cargo operator)**, sob supervisão do superintendente de marinha. A tela principal do sistema era baseada nos diagramas P&ID da malha de transferência, o que é tecnicamente coerente com a necessidade de o operador visualizar caminhos de fluxo, estado de válvulas e condição dos equipamentos antes e durante o bombeio.

Do ponto de vista funcional, um sistema de controle é estruturado para relacionar **causa e efeito** sobre variáveis do processo, por meio de medição, supervisão e comando. As fontes também destacam que um sistema desse tipo deve:
- permitir a operabilidade remota dos elementos controlados;
- fornecer dados suficientes para operação segura;
- responder adequadamente a condições que exijam parada;
- executar paradas de emergência de forma segura dentro do tempo requerido pelo projeto aplicável.

Embora essa formulação venha de contexto de controle subsea, ela é plenamente útil como **filosofia de controle** para offloading: a transferência só deve prosseguir quando o operador dispõe de informação confiável, capacidade de comando e meios de interrupção segura.

### 2.1 Comando remoto e comando local
Um ponto operacional importante é que **nem todas as válvulas necessariamente são comandadas apenas da sala de controle**. No caso documentado pela ANP, grande parte das válvulas era comandada pelo supervisório, mas algumas exigiam **acionamento local** no upper deck e no pump room top, por meio de alavancas ou chaves com posições aberta/fechada/neutra instaladas em *solenoid boxes*.

Isso tem implicações diretas para o controle da transferência:
- o alinhamento da linha de carga pode depender de uma combinação de válvulas remotas e locais;
- a confirmação de estado deve ser positiva, e não presumida;
- a sequência de bombeio deve considerar o tempo de resposta e a validação de campo das válvulas locais;
- falhas de comunicação entre sala de controle e campo podem gerar linha indevidamente bloqueada, pressurização incorreta ou rota de fluxo não pretendida.

### 2.2 Válvulas de isolamento e função na sequência
As fontes conceituais lembram que **válvulas de isolamento** são usadas para isolar linhas ou processos e podem compor manifolds. Aplicado ao offloading, isso significa que a preparação para transferência depende do correto estado de abertura/fechamento das válvulas que:
- separam tanques da linha de exportação;
- conectam bombas e manifolds ao circuito de carga;
- permitem isolar trechos para intervenção, teste ou contenção de anormalidades.

Em termos operacionais, o erro de line-up de válvulas compromete a sequência de bombeio, podendo resultar em:
- sobrepressão localizada;
- recirculação não desejada;
- transferência do tanque incorreto;
- perda de contenção durante mudança de rota.

**Fontes:** `anp-dabfb60617e4f0ede433578e:p89-95:25.0-13.0`, `regis-9d017883010dd907fdb51652:pNone:163.120-198.0`

---

## 3. Variáveis de processo críticas para o controle da transferência

O controle de uma transferência de petróleo entre FPSO e navio aliviador depende do acompanhamento contínuo de variáveis operacionais. As fontes permitem destacar, como mínimo conceitual, as seguintes grandezas:

- **pressão** na linha e no manifold;
- **vazão** no mangote/linha de transferência;
- **temperatura da carga**;
- **nível** nos tanques ou vasos envolvidos;
- **posição de válvulas**;
- **estado das bombas**;
- **detecção de vazamentos**;
- **tração no hawser**, que embora não seja variável de processo de fluido, afeta diretamente a segurança da transferência.

No material sobre sistemas de controle, aparecem como parâmetros monitoráveis pressão e temperatura de produção, pressão em choke, pressão e temperatura em manifold, detecção de vazamento e posição de válvulas. Já no material sobre offloading, o sistema de telemetria troca entre FPSO e navio aliviador dados como pressão no manifold de carga do aliviador, pressão no mangote, vazão, temperatura da carga e condição de bomba de carga.

### 3.1 Relação entre essas variáveis
Mesmo sem limites numéricos fornecidos nas fontes, a lógica operacional é clara:
- **pressão** excessiva indica risco de sobrecarga de mangote, manifold, bomba ou válvula;
- **vazão** abaixo do esperado pode indicar restrição, desalinhamento de válvulas, perda de eficiência de bomba ou comando inadequado;
- **nível** em tanques condiciona a continuidade da retirada ou recebimento de carga;
- **temperatura** afeta a condição do fluido e pode ser relevante para desempenho hidráulico e rastreabilidade da carga;
- **posição de válvulas** é essencial para confirmar que o caminho de escoamento corresponde ao planejado.

### 3.2 Controle por setpoint e ação sobre válvulas
Em sistemas de processo, pressão e nível são tipicamente mantidos por meio de controladores que atuam sobre válvulas. As fontes destacam que a operação normal de vasos ocorre por controles de pressão do gás e nível de líquido, e que falhas de válvula ou falhas operacionais podem produzir perdas e acidentes de grande proporção.

Aplicado ao offloading, o princípio é o mesmo: a estabilidade da transferência depende de uma ação coordenada sobre:
- válvulas de rota/alinhamento;
- válvulas de controle associadas à linha;
- bombas de exportação/transferência;
- permissivos de continuidade associados ao sistema supervisório e à telemetria.

Como o comportamento do sistema real pode ser não linear e sujeito a variações no tempo, a fonte ressalta que algoritmos padrão de controle têm limitações e podem exigir atuação do operador. Isso é particularmente relevante em offloading, onde a hidráulica da linha e as condições marítimas mudam ao longo da operação.

**Fontes:** `regis-0605ee69ad83c97b9a70cfd2:pNone:796.60-830.0`, `regis-9d017883010dd907fdb51652:pNone:163.120-198.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3025711.0-3025739.0`

---

## 4. Telemetria entre FPSO e navio aliviador

As operações de offloading descritas contam com um **OMTS (Offloading Monitoring Telemetry System)**, cuja função é integrar dados operacionais entre FPSO e navio aliviador durante a transferência de carga. Os sinais são transmitidos por rádio, com exigência de **alta confiabilidade e disponibilidade**, o que é coerente com a criticidade da operação.

Segundo a fonte, os sinais trocados incluem:
- **Green Line Status / condição de bombeio OK**;
- **condição de comunicação OK**;
- **pressão no manifold de carga do navio aliviador**;
- **tração no hawser na terminação do navio aliviador**;
- **vazão no mangote de transferência**;
- **temperatura da carga transferida**;
- **pressão no mangote de transferência**;
- **tração no hawser na terminação do FPSO**;
- **condição da bomba de carga ON/OFF**.

### 4.1 Função operacional dos sinais
Esses sinais suportam três camadas de controle:

1. **Permissivo de início da transferência**  
   A condição de bombeio (*Green Line Status*) indica que o navio aliviador está pronto para receber carga. Isso é essencial para evitar partida de bomba sem prontidão do recebedor.

2. **Continuidade segura da operação**  
   Vazão, pressão e temperatura permitem acompanhar a consistência hidráulica da transferência. Já as trações no hawser mostram se a condição relativa entre as embarcações está compatível com a permanência em tandem.

3. **Detecção rápida de degradação da situação**  
   Perda de comunicação, alteração abrupta de pressão, queda inesperada de vazão ou aumento de tração são indícios de anormalidade que podem exigir redução de taxa, interrupção do bombeio ou preparação para desconexão.

### 4.2 Green Line Status como síntese operacional
A fonte informa que o **Green Line Status** é projetado para excluir sinais espúrios e constitui, na prática, um resultado dos demais sinais monitorados. Isso caracteriza uma lógica de **estado composto**, mais robusta do que um único contato discreto. Em termos de operação, isso reduz a chance de se interpretar como “pronto para bombear” uma condição que ainda apresenta falha parcial de comunicação ou inconsistência de variáveis.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:3025711.0-3025739.0`

---

## 5. Sequência operacional da transferência e do bombeio

## 5.1 Preparação mecânica da conexão
Antes de qualquer bombeio, a operação tandem requer a formação do arranjo de amarração e a transferência do mangote. A fonte descreve um **BLS** com dois guinchos de capacidades distintas:
- um guincho de aproximadamente **5 toneladas-força**, mais veloz, para pagar e recolher os **cabos mensageiros** leves;
- um segundo guincho, de aproximadamente **50 toneladas-força**, mais lento, para recolher o conjunto de **hawser**, **chafing chain** e, posteriormente, o **mangote de transferência**.

A primeira passagem de cabo é normalmente feita com **pistola pneumática**, que lança um projétil com o primeiro cabo mensageiro. A partir desse vínculo inicial, transfere-se o hawser e depois o mangote. O sistema inclui ainda um **mordente hidráulico** que trava a chafing chain associada ao hawser.

Do ponto de vista de controle da transferência, essa etapa é relevante porque o bombeio só pode ser considerado quando houver:
- amarração estabelecida;
- mangote transferido e mecanicamente preparado;
- confirmação das condições de monitoramento e comunicação.

## 5.2 Preparação de line-up e prontidão para bombeio
Com a conexão física estabelecida, a preparação para bombeio requer, tecnicamente:
- confirmação do line-up das válvulas no FPSO e no navio aliviador;
- verificação de prontidão do navio recebedor por sinal de bombeio OK;
- confirmação do link de comunicação ativo;
- checagem do estado das bombas e do circuito de carga;
- verificação de que as variáveis medidas estão dentro da condição esperada de partida.

Como parte das válvulas pode ter comando local, a prontidão operacional não deve ser baseada somente na intenção de comando pela sala de controle, mas também na **confirmação do estado efetivo da rota hidráulica**.

## 5.3 Partida e rampa de transferência
As fontes não fornecem uma curva de partida quantitativa, mas a filosofia de controle indica que a partida segura depende de:
- abertura correta da rota de escoamento;
- ativação das bombas de forma compatível com a condição do sistema;
- observação da resposta de pressão, vazão e nível;
- confirmação de que a pressão no mangote e no manifold evolui sem comportamento anormal.

A sequência de bombeio deve ser tratada como uma operação integrada: aumentar vazão sem validação de pressão, estado de válvulas e condição do navio aliviador aumenta o risco de sobrepressão, golpe operacional, esforço excessivo no sistema ou interrupção abrupta.

## 5.4 Controle durante a transferência
Durante o bombeio, o operador deve acompanhar continuamente:
- vazão transferida;
- pressão da linha/mangote/manifold;
- temperatura da carga;
- estado ON/OFF das bombas;
- tração no hawser em ambas as terminações;
- condição da comunicação e do permissivo de bombeio.

Se a filosofia de controle da planta for considerada, pressão e nível são variáveis centrais; portanto, na prática, a taxa de transferência precisa ser compatibilizada com a capacidade hidráulica do sistema e com a condição de inventário nos tanques.

## 5.5 Encerramento e transição de estado
As fontes disponíveis não detalham a drenagem final, despressurização ou armazenamento do mangote. Ainda assim, o material mostra que o encerramento da operação deve ser entendido como **mudança controlada de estado**, com dependência de:
- parada do bombeio;
- retorno das válvulas ao estado seguro/alinhado para pós-operação;
- manutenção do monitoramento até cessarem as condições críticas da conexão em tandem.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:3025711.0-3025739.0`, `anp-dabfb60617e4f0ede433578e:p89-95:25.0-13.0`, `regis-0605ee69ad83c97b9a70cfd2:pNone:796.60-830.0`

---

## 6. Papel do operador, supervisão e fatores humanos

As fontes mostram que a operação de transferência de carga envolve forte componente humano. No caso investigado pela ANP, havia uma equipe de operadores de marinha, mas com diferença prática de experiência entre profissionais que ocupavam formalmente o mesmo cargo. Isso é relevante porque o controle da transferência não depende apenas do sistema, mas também de:
- interpretação correta da IHM;
- disciplina de line-up;
- comunicação entre sala de controle, convés e embarcação aliviadora;
- julgamento operacional para reagir a desvios.

Outra fonte destaca que plantas reais são complexas, não lineares, com variações temporais e múltiplos objetivos, e que algoritmos padrão de controle possuem limitações, exigindo intervenção humana em determinadas situações. Em offloading, essa limitação aparece quando a operação precisa conciliar simultaneamente:
- estabilidade hidráulica da transferência;
- integridade mecânica do mangote e da amarração;
- condição relativa entre duas embarcações de grande porte;
- eventual mudança do modo de posicionamento do navio aliviador.

Assim, um controle operacional robusto requer:
- definição clara de autoridade para iniciar, manter, reduzir ou interromper o bombeio;
- confirmação cruzada de comandos locais e remotos;
- procedimentos de handover e comunicação consistentes;
- treinamento específico para leitura dos sinais críticos da operação.

**Fontes:** `anp-dabfb60617e4f0ede433578e:p89-95:25.0-13.0`, `regis-0605ee69ad83c97b9a70cfd2:pNone:796.60-830.0`

---

## 7. Integração entre controle de transferência e posicionamento relativo

O material recebido sobre offloading ressalta que, em operações de alívio com navios dinamicamente posicionados, foram necessários **modos operacionais específicos do SPD**, pois duas embarcações de grande porte permanecem próximas por várias horas e a perda de controle pode resultar em colisão direta. A mesma fonte registra que também existem modos manuais ou não automáticos, inclusive para lidar com falhas em subsistemas do próprio SPD, propulsão, geração ou referências de posição.

Para o controle da transferência de carga, isso significa que a decisão de continuar bombeando não pode ser baseada só em variáveis de fluido. A permanência do bombeio também depende da manutenção do **posicionamento relativo seguro** entre FPSO e aliviador. Por isso, a inclusão da **tração no hawser** no sistema de telemetria é tecnicamente importante: ela conecta a condição de amarração ao estado do bombeio.

Em termos práticos, a filosofia correta é tratar a transferência como uma operação acoplada entre:
- sistema hidráulico de carga;
- sistema de amarração/mangote;
- sistema de posicionamento/navegação/comunicação.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:3025711.0-3025739.0`

---

## 8. Segurança de processo, áreas classificadas e proteção de equipamentos

A ANP registra que a casa de bombas é tipicamente classificada como **Zona 1**, e que bombas dessa área podem ter motor acionador localizado externamente. A classificação de áreas tem por objetivo selecionar, projetar e instalar equipamentos elétricos adequados a atmosferas potencialmente explosivas.

Para a operação de offloading, isso reforça que o controle da transferência não é apenas hidráulico: ele também deve ser compatível com os requisitos de segurança em áreas com risco de formação de atmosfera inflamável.

A mesma fonte apresenta um exemplo de **válvula de alívio de pressão** em bomba de stripping, cuja descarga retornava à sucção da bomba. Embora seja um caso específico, ele ilustra uma filosofia de proteção relevante: equipamentos de movimentação de carga podem necessitar de meios para evitar sobrepressão local em condição anormal.

Portanto, no contexto desta faceta, o controle seguro da transferência envolve pelo menos três níveis de proteção:
- **controle operacional** por IHM, válvulas e bombas;
- **monitoramento contínuo** por sensores e telemetria;
- **proteção de equipamento e instalação** por classificação de área e dispositivos de alívio/proteção adequados ao projeto.

**Fontes:** `anp-dabfb60617e4f0ede433578e:p89-95:25.0-13.0`

---

## 9. Síntese técnica

Com base nas fontes, o controle da transferência de petróleo em offloading pode ser resumido como uma operação em que:

1. a **conexão mecânica** (mensageiros, hawser, chafing chain e mangote) precisa estar estabelecida e confirmada;
2. o **line-up hidráulico** depende de válvulas remotas e, em alguns casos, válvulas de acionamento local;
3. o **bombeio** só deve ocorrer com prontidão confirmada do navio aliviador e comunicação ativa;
4. a **continuidade da operação** exige observação simultânea de pressão, vazão, temperatura, estado das bombas e tração no hawser;
5. o **operador** permanece parte central da barreira de segurança, porque o sistema real é dinâmico, não linear e sujeito a anormalidades que exigem julgamento operacional;
6. o controle efetivo da transferência é sempre uma integração entre **processo, amarração, posicionamento relativo e segurança de área classificada**.

Esse conjunto de pontos é suficiente para sustentar avaliação profissional sobre a lógica de controle da transferência de carga e da sequência de bombeio entre FPSO e navio aliviador.