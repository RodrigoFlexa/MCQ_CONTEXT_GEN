# QA v7 (cota): perguntas a partir do inventário

Gerador gpt-5-4-petrobras:low, juiz gpt-5-4-petrobras:low. 139 questões geradas, 100 aprovadas (72%). Tempo 14.9 min. Chamadas 710, tokens de entrada 2,100,305, de saída 275,180.

O nível é o tipo pedido ao gerador (sem avaliador de dificuldade no loop).

| Tipo | geradas | aprovadas | corrigidas |
|---|---:|---:|---:|
| facil | 53 | 37 | 11 |
| media | 53 | 36 | 16 |
| dificil_A | 26 | 20 | 8 |
| dificil_B | 7 | 7 | 2 |

Motivos de reprovação: suporte (16), codigo:depende_do_material (11), autonomia (9), sem_pista (5), resposta_unica_cega (4), codigo:pergunta_composta (4), sem_generalizacao (3), tipo_ok (3), objetividade (2), resposta_unica (2), escopo (1), codigo:pergunta_aberta (1), jurisdicao (1)
Lotes com falha ou filtro de conteúdo: 0
Alvos descartados na triagem (genéricos): 3; recortados: 111

Respondente às cegas nas aprovadas (estimativa de dificuldade):

| Tipo | equivalente | parcial | incorreta |
|---|---:|---:|---:|
| facil | 21 | 6 | 9 |
| media | 15 | 13 | 8 |
| dificil_A | 11 | 5 | 4 |
| dificil_B | 2 | 4 | 1 |

## Por subtópico

| Tópico | Subtópico | cota | geradas | aprovadas | redundantes (novidade) |
|---|---|---:|---:|---:|---:|
| Sistemas de Lastro, Estabilidade, Ancora | Operação de Offloading | 3 | 5 | 3 | 0 |
| Sistemas de Lastro, Estabilidade, Ancora | Operação de tanques de carga, lastro, sistema gás  | 3 | 3 | 3 | 0 |
| Sistemas de Lastro, Estabilidade, Ancora | Sistema de ancoragem, manutenção e monitoramento d | 4 | 4 | 4 | 0 |
| Operações submarinas, poços, risers e eq | Operações submarinas, poços, manifolds, PLEM e PLE | 4 | 4 | 4 | 0 |
| Operações submarinas, poços, risers e eq | Sistema e operação de pull in de risers | 6 | 12 | 6 | 0 |
| Produção e Processo (Medição Fiscal e Si | Compressão de Gás | 1 | 1 | 1 | 0 |
| Produção e Processo (Medição Fiscal e Si | Operação de Separadores Trifásicos | 1 | 2 | 1 | 0 |
| Produção e Processo (Medição Fiscal e Si | Operação de Tratadores Eletrostáticos | 1 | 1 | 1 | 0 |
| Produção e Processo (Medição Fiscal e Si | Operação Geral FPSO | 2 | 2 | 2 | 0 |
| Produção e Processo (Medição Fiscal e Si | Produção, processo e processamento do óleo | 1 | 1 | 1 | 0 |
| Produção e Processo (Medição Fiscal e Si | Sistema de Alívio e Flare | 1 | 1 | 1 | 0 |
| Produção e Processo (Medição Fiscal e Si | Sistema de captação e tratamento de água do mar pa | 1 | 1 | 1 | 0 |
| Produção e Processo (Medição Fiscal e Si | Sistema de drenagem aberta e fechada | 1 | 4 | 1 | 0 |
| Produção e Processo (Medição Fiscal e Si | Tratamento do Gás produzido | 1 | 1 | 1 | 0 |
| Segurança Operacional, SGSO, Sistemas de | Estudos de Segurança | 1 | 1 | 1 | 0 |
| Segurança Operacional, SGSO, Sistemas de | Operações simultâneas – SIMOPS | 2 | 2 | 2 | 0 |
| Segurança Operacional, SGSO, Sistemas de | Segurança e Controle de Riscos | 2 | 2 | 2 | 0 |
| Segurança Operacional, SGSO, Sistemas de | SGSO | 2 | 3 | 2 | 0 |
| Segurança Operacional, SGSO, Sistemas de | Sistema de Combate a Incêndio | 1 | 1 | 1 | 0 |
| Segurança Operacional, SGSO, Sistemas de | Sistema de Fogo e Gás (F&G) | 1 | 2 | 1 | 0 |
| Segurança Operacional, SGSO, Sistemas de | Sistemas e equipamentos de salvatagem | 1 | 1 | 1 | 0 |
| Utilidades, geração de energia e sistema | Geração e distribuição de energia elétrica | 5 | 7 | 5 | 0 |
| Utilidades, geração de energia e sistema | Sistema de utilidades | 5 | 5 | 5 | 0 |
| Descomissionamento e Gestão do Ciclo de  | Geral | 10 | 16 | 10 | 0 |
| Gestão do Desempenho Empresarial (KPI) | Gestão do Desempenho Empresarial (KPI) | 10 | 12 | 10 | 0 |
| Logística, Suprimentos e Movimentação de | Logística e Suprimento Offshore | 5 | 8 | 5 | 0 |
| Logística, Suprimentos e Movimentação de | Movimentação de Cargas | 5 | 8 | 5 | 0 |
| Manutenção, Inspeção e Integridade de At | Apoio Técnico e Manutenção em um FPSO (Laboratório | 2 | 3 | 2 | 0 |
| Manutenção, Inspeção e Integridade de At | Cibersegurança e Integridade de Sistemas Digitais | 2 | 4 | 2 | 0 |
| Manutenção, Inspeção e Integridade de At | Inspeção e Integridade | 2 | 2 | 2 | 0 |
| Manutenção, Inspeção e Integridade de At | Instrumentação, Controle e Automação | 2 | 3 | 2 | 0 |
| Manutenção, Inspeção e Integridade de At | Manutenção e Plano de Manutenção | 2 | 3 | 2 | 0 |
| Segurança Ocupacional, Saúde e Meio Ambi | Condições Ambientais e Impactos Operacionais | 2 | 3 | 2 | 0 |
| Segurança Ocupacional, Saúde e Meio Ambi | Gestão de Pessoas e Treinamento | 2 | 4 | 2 | 0 |
| Segurança Ocupacional, Saúde e Meio Ambi | Meio Ambiente, Gestão Ambiental e Sustentabilidade | 2 | 2 | 2 | 0 |
| Segurança Ocupacional, Saúde e Meio Ambi | Saúde Ocupacional | 2 | 3 | 2 | 0 |
| Segurança Ocupacional, Saúde e Meio Ambi | Segurança Ocupacional | 2 | 2 | 2 | 0 |

## Curva de novidade (aprovadas na ordem da fila, janelas de 20)

### Operação de Offloading

| aprovadas | redundantes | fração |
|---|---:|---:|
| 1 a 3 | 0 | 0% |

### Operação de tanques de carga, lastro, sistema gás inerte, ventilação e estabilidade

| aprovadas | redundantes | fração |
|---|---:|---:|
| 1 a 3 | 0 | 0% |

### Sistema de ancoragem, manutenção e monitoramento da posição

| aprovadas | redundantes | fração |
|---|---:|---:|
| 1 a 4 | 0 | 0% |

### Operações submarinas, poços, manifolds, PLEM e PLET

| aprovadas | redundantes | fração |
|---|---:|---:|
| 1 a 4 | 0 | 0% |

### Sistema e operação de pull in de risers

| aprovadas | redundantes | fração |
|---|---:|---:|
| 1 a 6 | 0 | 0% |

### Compressão de Gás

| aprovadas | redundantes | fração |
|---|---:|---:|
| 1 a 1 | 0 | 0% |

### Operação de Separadores Trifásicos

| aprovadas | redundantes | fração |
|---|---:|---:|
| 1 a 1 | 0 | 0% |

### Operação de Tratadores Eletrostáticos

| aprovadas | redundantes | fração |
|---|---:|---:|
| 1 a 1 | 0 | 0% |

### Operação Geral FPSO

| aprovadas | redundantes | fração |
|---|---:|---:|
| 1 a 2 | 0 | 0% |

### Produção, processo e processamento do óleo

| aprovadas | redundantes | fração |
|---|---:|---:|
| 1 a 1 | 0 | 0% |

### Sistema de Alívio e Flare

| aprovadas | redundantes | fração |
|---|---:|---:|
| 1 a 1 | 0 | 0% |

### Sistema de captação e tratamento de água do mar para injeção no reservatório

| aprovadas | redundantes | fração |
|---|---:|---:|
| 1 a 1 | 0 | 0% |

### Sistema de drenagem aberta e fechada

| aprovadas | redundantes | fração |
|---|---:|---:|
| 1 a 1 | 0 | 0% |

### Tratamento do Gás produzido

| aprovadas | redundantes | fração |
|---|---:|---:|
| 1 a 1 | 0 | 0% |

### Estudos de Segurança

| aprovadas | redundantes | fração |
|---|---:|---:|
| 1 a 1 | 0 | 0% |

### Operações simultâneas – SIMOPS

| aprovadas | redundantes | fração |
|---|---:|---:|
| 1 a 2 | 0 | 0% |

### Segurança e Controle de Riscos

| aprovadas | redundantes | fração |
|---|---:|---:|
| 1 a 2 | 0 | 0% |

### SGSO

| aprovadas | redundantes | fração |
|---|---:|---:|
| 1 a 2 | 0 | 0% |

### Sistema de Combate a Incêndio

| aprovadas | redundantes | fração |
|---|---:|---:|
| 1 a 1 | 0 | 0% |

### Sistema de Fogo e Gás (F&G)

| aprovadas | redundantes | fração |
|---|---:|---:|
| 1 a 1 | 0 | 0% |

### Sistemas e equipamentos de salvatagem

| aprovadas | redundantes | fração |
|---|---:|---:|
| 1 a 1 | 0 | 0% |

### Geração e distribuição de energia elétrica

| aprovadas | redundantes | fração |
|---|---:|---:|
| 1 a 5 | 0 | 0% |

### Sistema de utilidades

| aprovadas | redundantes | fração |
|---|---:|---:|
| 1 a 5 | 0 | 0% |

### Geral

| aprovadas | redundantes | fração |
|---|---:|---:|
| 1 a 10 | 0 | 0% |

### Gestão do Desempenho Empresarial (KPI)

| aprovadas | redundantes | fração |
|---|---:|---:|
| 1 a 10 | 0 | 0% |

### Logística e Suprimento Offshore

| aprovadas | redundantes | fração |
|---|---:|---:|
| 1 a 5 | 0 | 0% |

### Movimentação de Cargas

| aprovadas | redundantes | fração |
|---|---:|---:|
| 1 a 5 | 0 | 0% |

### Apoio Técnico e Manutenção em um FPSO (Laboratório, Oficinas, Pipe Shop)

| aprovadas | redundantes | fração |
|---|---:|---:|
| 1 a 2 | 0 | 0% |

### Cibersegurança e Integridade de Sistemas Digitais

| aprovadas | redundantes | fração |
|---|---:|---:|
| 1 a 2 | 0 | 0% |

### Inspeção e Integridade

| aprovadas | redundantes | fração |
|---|---:|---:|
| 1 a 2 | 0 | 0% |

### Instrumentação, Controle e Automação

| aprovadas | redundantes | fração |
|---|---:|---:|
| 1 a 2 | 0 | 0% |

### Manutenção e Plano de Manutenção

| aprovadas | redundantes | fração |
|---|---:|---:|
| 1 a 2 | 0 | 0% |

### Condições Ambientais e Impactos Operacionais

| aprovadas | redundantes | fração |
|---|---:|---:|
| 1 a 2 | 0 | 0% |

### Gestão de Pessoas e Treinamento

| aprovadas | redundantes | fração |
|---|---:|---:|
| 1 a 2 | 0 | 0% |

### Meio Ambiente, Gestão Ambiental e Sustentabilidade

| aprovadas | redundantes | fração |
|---|---:|---:|
| 1 a 2 | 0 | 0% |

### Saúde Ocupacional

| aprovadas | redundantes | fração |
|---|---:|---:|
| 1 a 2 | 0 | 0% |

### Segurança Ocupacional

| aprovadas | redundantes | fração |
|---|---:|---:|
| 1 a 2 | 0 | 0% |

## Questões

### Sistemas de Lastro, Estabilidade, Ancoragem e Posicionamento, Offloading e Tanques de Carga

#### Operação de Offloading

**facil · APROVADA**  
_Nota(s): Segurança dos tanques de óleo cru durante offloading: inertização contínua e preparação segura para entrada_

**P:** Que condição de segurança a inertização deve manter nos tanques de óleo cru de FPSO/FSU durante armazenamento, carregamento e descarga?

**R:** Manter continuamente a atmosfera do tanque fora dos limites explosivos.

_Explicação:_ A inertização é o controle crítico para impedir que a atmosfera no espaço de vapor do tanque entre na faixa inflamável. Durante armazenamento, carregamento e descarga, esse estado deve ser mantido continuamente.

_Às cegas (equivalente):_ Manter atmosfera inerte com O2 abaixo do LOC (limite de concentração de oxigênio) para evitar combustão/explosão, tipicamente ≤8% v/v (ou conforme COF do óleo) e leve sobrepressão positiva no tanque.

**media · REPROVADA: autonomia, sem_generalizacao · corrigida**  
_Nota(s): Drive-off, perda de posição e colisão no offloading: cenários críticos de poluição_

**P:** Nas estações de offloading pela proa e pela popa, qual associação principal caracteriza os riscos classificados como “Not Tolerable” quanto ao evento iniciador e à consequência de poluição?

**R:** Drive-off associado a vazamento de óleo em grande escala a partir de tanque de carga do FPSO.

_Explicação:_ Segundo a conclusão da PRA para as estações de proa e popa, os riscos “Not Tolerable” estão principalmente ligados a drive-off, e a consequência de poluição correspondente é vazamento de óleo em grande escala a partir de tanque de carga do FPSO.

**dificil_A · APROVADA**  
_Nota(s): Conexão e desconexão de hawser, mangote e cabos mensageiros no offloading entre FPSO e aliviador_

**P:** Durante o offloading em tandem, ocorre uma falha de equipamento na etapa de desconexão do mangote. A investigação imediata confirma falha no cilindro do sistema. Qual ação operacional deve ser adotada?

**R:** Abortar o offloading, acionar a parada de emergência da transferência, desconectar e desamarrar, afastando o aliviador com o sistema DP.

_Explicação:_ Em falha de equipamento, a continuidade da transferência não é o critério correto; a operação deve ser abortada com execução da sequência de emergência. Quando a falha é especificamente no cilindro, o afastamento do aliviador deve ser feito com o sistema de posicionamento dinâmico.

_Às cegas (parcial):_ Parar imediatamente a transferência (ESD), manter posição/afastamento seguro, comunicar FPSO e aliviador e iniciar o procedimento de desconexão de emergência/contingência (isolando hidráulica e usando back‑up/manual). Falta confirmar se há ESD/EDS redundante ou liberação manual disponível.

**media · REPROVADA: autonomia**  
_Nota(s): Envelopes ambientais por fase e janela meteorológica no offloading em tandem FPSO–navio aliviador_

**P:** Em cenários de offloading na Bacia de Santos com FPSOs de aproamento fixo, qual foi a consequência prática sobre a programação dos navios aliviadores?

**R:** A programação dos NADPs ficou restrita a previsões de condições ambientais amenas.

_Explicação:_ Nesses cenários, a maior restrição operacional levou a limitar a programação dos navios aliviadores a janelas previstas com condições ambientais favoráveis, em vez de aceitar condições mais severas.

**facil · APROVADA**  
_Nota(s): Sequência hidráulica e ajuste de vazão no offloading após a conexão_

**P:** Após a conexão do sistema de offloading entre um FPSO e um navio aliviador, qual é a sequência operacional até o início da transferência principal de óleo?

**R:** Teste de vazamento na linha de mangueiras, bombeio de água para o slop tank do navio aliviador e depois bombeio de óleo para os tanques de carga.

_Explicação:_ A operação não começa diretamente com a carga principal de óleo. Primeiro confirma-se a estanqueidade da linha, depois faz-se o deslocamento inicial com água para o slop tank do navio aliviador e só então se inicia o envio de óleo aos tanques de carga.

_Às cegas (parcial):_ Após conectar: testes de comunicações/ESD e verificação de intertravamentos; alinhamento de válvulas/linhas e confirmação de contenção; pressurização e teste de estanqueidade; inertização/eliminação de ar se aplicável; abertura gradual e transferência de “line fill/recirculação”, estabilizando pressões/caudais; iniciar transferência principal.

#### Operação de tanques de carga, lastro, sistema gás inerte, ventilação e estabilidade

**facil · APROVADA**  
_Nota(s): Representação da massa de carga e do centro de gravidade em modelos hidrodinâmicos de FLNG_

**P:** Antes de deduzir a contribuição dos tanques de carga para representar o FLNG no WAMIT, em quais componentes do modelo global essa massa entra?

**R:** Na matriz global de massa e no centro de gravidade da unidade.

_Explicação:_ Na modelagem hidrodinâmica do FLNG, a carga armazenada nos tanques compõe inicialmente tanto a matriz global de massa quanto o centro de gravidade. Essa contribuição é depois deduzida para obter o modelo sem a carga dos tanques a ser representado no WAMIT.

_Às cegas (equivalente):_ Entra no modelo global como: (1) massa/deslocamento total (matriz de massa/inércia 6DOF do corpo), (2) posição do CG e momentos de inércia, e (3) hidrostática (calado/GM via distribuição de peso). Falta definir se o WAMIT usa corpo rígido ou multibody/tanques como corpos separados.

**dificil_A · APROVADA**  
_Nota(s): Lastro em emergência e compensação de avarias_

**P:** Após alagamento em uma coluna, a unidade aderna e perde flutuabilidade. A equipe planeja admitir água nos tanques de lastro do lado oposto para recuperar a condição segura. Se essa capacidade dedicada não bastar para manter a estabilidade, qual é a linha de ação correta nessa emergência?

**R:** Fazer contralastro nos tanques dedicados para reduzir a inclinação, monitorando o aumento de calado; recorrer a tanques de carga apenas se a capacidade de lastro dedicada for insuficiente.

_Explicação:_ Em emergência, o sistema de lastro é usado para levar a unidade a uma condição segura de trim e nivelamento e para compensar perda de flutuabilidade. O contralastro no lado oposto pode corrigir a banda, mas pode acelerar o aumento do calado. O uso de tanques de carga para manter a estabilidade é medida excepcional, associada à insuficiência da capacidade dedicada de lastro.

_Às cegas (incorreta):_ Não prosseguir com alagamento/contralastro além do previsto no manual de estabilidade avariada; isolar a entrada d’água, parar produção (ESD), acionar resposta a emergências, solicitar apoio externo e preparar evacuação/abandono se a estabilidade não puder ser restabelecida.

**media · APROVADA**  
_Nota(s): Avaliação e critérios de estabilidade intacta e em avaria_

**P:** Em três condições de carregamento com o mesmo calado, qual delas deve ser adotada como condição crítica na verificação de estabilidade intacta?

**R:** A condição de maior KG, porque com o mesmo calado a hidrostática não muda e o centro de gravidade mais alto torna a estabilidade menos favorável.

_Explicação:_ Com calado constante, as propriedades hidrostáticas permanecem iguais entre as condições comparadas. Assim, a condição com maior KG é a mais crítica, por reduzir a margem de estabilidade em relação às demais.

_Às cegas (incorreta):_ Adote como condição crítica a que resultar na menor margem de estabilidade (menor GM e/ou menores áreas/ângulos da curva GZ), normalmente a de maior KG e maior efeito de superfície livre. Falta saber quais são as três condições para apontar qual delas é essa.

#### Sistema de ancoragem, manutenção e monitoramento da posição

**facil · APROVADA**  
_Nota(s): Offset da unidade em sistemas de ancoragem: origem, cálculo, limites e evidências de conformidade_

**P:** O que é o offset, ou passeio, de uma unidade flutuante ancorada?

**R:** Deslocamento horizontal da unidade entre o equilíbrio neutro inicial e o equilíbrio final sob vento, corrente e ondas.

_Explicação:_ Offset, ou passeio, é o deslocamento horizontal imposto pelas cargas ambientais. Ele é medido da posição inicial de equilíbrio neutro até a posição final de equilíbrio sob a ação de vento, correnteza e ondas.

_Às cegas (parcial):_ Offset (passeio) é o deslocamento horizontal do FPSO/FSO em relação ao ponto de referência da amarração (centro do spread/turret/âncora), devido a vento, onda e corrente; mede-se como distância e direção no plano.

**media · APROVADA · corrigida**  
_Nota(s): Aproamento e alinhamento ambiental conforme a arquitetura de ancoragem_

**P:** Que sistema de ancoragem distribuída usa menor rigidez ou tensionamento nas linhas de popa que nas de proa, introduzindo complacência parcial da ordem de 20° no aproamento?

**R:** DICAS.

_Explicação:_ No DICAS, a assimetria entre as linhas de proa e de popa cria liberdade parcial de alinhamento da unidade, da ordem de 20°. Isso o distingue do spread mooring convencional, em que o aproamento fica praticamente fixo pela distribuição das linhas e pela locação.

_Às cegas (equivalente):_ Sistema de ancoragem distribuída do tipo DICAS (Differential Compliance Anchorage System): usa menor rigidez/tensionamento nas linhas de popa que nas de proa, permitindo complacência parcial ~20° no aproamento.

**dificil_A · APROVADA**  
_Nota(s): Zonas críticas de desgaste em amarras e limitações diagnósticas da inspeção submersa_

**P:** Em um FPSO com turret, a inspeção submersa em operação mostrou condição aceitável nas partes visíveis da linha, mas a região de entrada da amarra no spider passa por um trumpet submerso. O ROV só consegue observar parcialmente essa área, e a equipe precisa decidir se a avaliação visual basta para concluir a integridade. Em que condição essa conclusão não pode se apoiar apenas na inspeção submersa?

**R:** Quando há suspeita de desgaste na região interna e oculta do trumpet, que não é adequadamente acessível por inspeção visual ou por ROV.

_Explicação:_ As regiões internas do trumpet são de difícil acesso e a inspeção por ROV nessa área é apenas limitada. Nessa condição, a inspeção submersa em operação revela só parte da condição real, e a avaliação de integridade deve ser complementada por remoção da amarra ou por modelos de predição de desgaste.

_Às cegas (equivalente):_ Não pode se apoiar só na inspeção submersa quando a região crítica (entrada no spider/trumpet) não é totalmente acessível/visível ao ROV, pois pode haver desgaste/corrosão/fadiga não detectáveis; falta confirmar acesso 100% ou aplicar END/monitoramento/tensionamento para validar.

**media · APROVADA**  
_Nota(s): LBL como referência hidroacústica ao fundo para posição horizontal da embarcação_

**P:** Em um sistema LBL já implantado e calibrado, qual característica da rede de transponders explica a boa acurácia de posicionamento horizontal da embarcação?

**R:** Grandes distâncias entre os transponders, formando linhas de base longas.

_Explicação:_ No LBL, a boa acurácia é atribuída ao fato de as linhas de base serem longas, ou seja, de haver grandes distâncias entre os transponders da rede de fundo. A calibração pode ser trabalhosa, mas o ganho esperado do arranjo está nessa geometria.

_Às cegas (equivalente):_ A boa acurácia horizontal vem da geometria/“baseline” da rede: transponders bem espaçados e distribuídos ao redor (cobrindo 360°) geram boa diluição de precisão (HDOP baixo) e reduzem erros na triangulação.

### Operações submarinas, poços, risers e equipamentos submarinos

#### Operações submarinas, poços, manifolds, PLEM e PLET

**facil · APROVADA**  
_Nota(s): Monitoramento de vazamentos, restrições de fluxo e anomalias de integridade em linhas e equipamentos submarinos_

**P:** Qual é o motivo técnico para comparar um desvio de queda de pressão apenas com referência na mesma condição de vazão de líquido, GLR e water-cut?

**R:** Porque a queda de pressão é uma função não linear de vazão de líquido, GLR e water-cut, e mudanças de composição podem alterar Δp sem indicar dano mecânico.

_Explicação:_ A perda de carga na linha depende simultaneamente da vazão e da composição do fluido. Por isso, comparar Δp com uma referência de condição diferente pode confundir efeito normal de escoamento multifásico com anomalia de integridade.

_Às cegas (equivalente):_ Porque a queda de pressão depende diretamente de vazão de líquido, GLR e water-cut, que alteram regime de escoamento, holdup/densidade, viscosidade e atrito. Comparar sem igualar essas variáveis mistura efeito operacional com degradação/obstrução real.

**media · APROVADA**  
_Nota(s): Completação submarina, cabeça de poço, ANM e barreiras de controle do poço_

**P:** Na vida produtiva de um poço submarino, como se define tecnicamente a ANM quanto à sua função principal e às classificações por serviço e por configuração?

**R:** É o principal equipamento de controle do poço; por serviço, pode ser de produção ou injeção; por configuração, convencional, vertical ou horizontal.

_Explicação:_ Durante a vida produtiva, a ANM é o conjunto de válvulas usado para controlar o poço a partir da unidade de produção, inclusive em aplicações de produção ou de injeção. Sua classificação técnica separa a função de serviço da geometria/configuração do arranjo submarino.

_Às cegas (parcial):_ ANM (Árvore de Natal Molhada) é o conjunto de válvulas/conexões no cabeçote submarino para controlar, monitorar e isolar o poço e direcionar o escoamento. Classifica-se por serviço: produção ou injeção (água/gás). Por configuração: vertical ou horizontal.

**dificil_A · APROVADA**  
_Nota(s): Funções do manifold submarino e arranjo de válvulas para produção, teste e injeção_

**P:** Durante a preparação para testar um poço ligado a um manifold submarino, a equipe precisa desviar apenas esse escoamento para o circuito de teste, mantendo os demais poços em produção normal e sem usar a rota principal de produção desse poço. Que elemento do arranjo do manifold torna esse encaminhamento seletivo possível?

**R:** Válvulas dedicadas e segregadas para produção e teste, usando a linha específica de teste do manifold.

_Explicação:_ O encaminhamento seletivo depende de o manifold ter, para cada template de produção, pelo menos uma válvula para a linha de produção e outra para a linha de teste. Essa segregação permite desviar o poço para o circuito de teste, inclusive por um caminho próprio até o equipamento de teste, sem precisar usar a rota normal de produção.

_Às cegas (equivalente):_ Válvula/dúplo isolamento do ramal do poço (produção–teste) no manifold — o ‘test header’ com válvulas de seleção que comutam só esse poço para a linha de teste, mantendo os demais no header de produção. Falta saber se o manifold é com test header dedicado ou via MCS.

**media · APROVADA**  
_Nota(s): Estratégias de garantia de escoamento ao longo do ciclo de vida em sistemas submarinos_

**P:** Na seleção da estratégia de garantia de escoamento para um sistema submarino, qual critério técnico-econômico deve orientar a escolha, em vez de assumir uma medida única para todos os casos?

**R:** A alternativa deve combinar medidas conforme o comportamento do fluido e os mecanismos identificados, escolhendo a solução técnico-econômica mais adequada ao sistema.

_Explicação:_ Em garantia de escoamento, normalmente não existe solução única aplicável a todo projeto ou sistema em operação. A escolha deve ser baseada na avaliação do fluido, com identificação dos principais mecanismos, para então compor a alternativa mais viável técnica e economicamente.

_Às cegas (parcial):_ Escolher pela alternativa de menor Custo Total do Ciclo de Vida (CAPEX+OPEX+perdas por indisponibilidade/risco) que cumpra as margens de flow assurance (hidratos, parafina, erosão/corrosão) no envelope operacional e metocean previsto.

#### Sistema e operação de pull in de risers

**facil · REPROVADA: autonomia · corrigida**  
_Nota(s): Restrições geométricas e pontos de conexão no pull-in de risers integrados ao posicionamento do FPSO_

**P:** No planejamento descrito para viabilizar a configuração de um SLWR, qual parâmetro de projeto foi pré-fixado para atender à restrição geométrica de projeção horizontal?

**R:** A distância entre o PLET e o FPSO.

_Explicação:_ A restrição geométrica ligada à projeção horizontal foi tratada no planejamento por meio da definição prévia do afastamento entre o PLET e o FPSO. Esse parâmetro funcionou como condicionante para viabilizar a configuração do SLWR.

**media · REPROVADA: autonomia**  
_Nota(s): Definição geométrica e envelope de instalação do SLWR no pull-in_

**P:** Na seleção de configurações de riser durante o pull-in, qual medida geométrica foi usada para reduzir a probabilidade de interferência entre linhas?

**R:** O deslocamento transversal; preferem-se configurações com menor deslocamento para minimizar a interferência entre risers.

_Explicação:_ O critério de interferência foi baseado na medição do deslocamento transversal de cada configuração. As configurações com menor deslocamento foram selecionadas porque tendem a reduzir a interferência entre risers no arranjo.

**dificil_A · REPROVADA: suporte, objetividade**  
_Nota(s): Ventilação do anular e integridade do end fitting na terminação do riser conectada à unidade_

**P:** Na terminação de um riser flexível conectada à unidade, o sistema de ventilação do anular existe, mas as linhas foram montadas e operadas sem GRVs. Qual mecanismo de degradação essa condição introduz e que outro dano continua possível no anular, comprometendo a integridade do end fitting?

**R:** Entrada de oxigênio com corrosão interna, além de sobrepressão no anular; sem GRVs, o arranjo deixa de bloquear o retorno de ar previsto no projeto.

_Explicação:_ A ventilação do end fitting deve dissipar o gás permeado no anular para evitar sobrepressão. Quando as GRVs não estão instaladas, o sistema não atende ao projeto, permite retorno de ar atmosférico e introduz oxigênio no anular, favorecendo corrosão severa de componentes internos como a armadura de tração.

**media · APROVADA**  
_Nota(s): Preparação pré-operacional e prontidão dos sistemas de içamento e tração para pull-in de risers_

**P:** Na preparação para o pull-in de um riser, o sistema de içamento/tração tem indícios de manutenção inadequada e há desvio das instruções originais do fabricante para testes e inspeções. Qual deve ser a decisão de prontidão antes da manobra?

**R:** Não liberar o sistema; corrigir a divergência e submetê-lo à avaliação técnica aplicável antes do pull-in.

_Explicação:_ Manutenção inadequada e descumprimento das instruções do fabricante degradam a confiabilidade do sistema e podem manter falhas latentes até a aplicação de carga. Nessas condições, a prontidão declarada deve ser interrompida até restabelecer conformidade e confirmar a condição do equipamento.

_Às cegas (equivalente):_ Decisão: NÃO PRONTO (No-Go). Suspender o pull-in, bloquear o equipamento e executar inspeções/testes conforme OEM e requisitos legais, com manutenção corretiva e validação por pessoa competente antes de liberar. Falta: confirmação de que os testes/inspeções OEM foram realizados e aprovados.

**facil · REPROVADA: codigo:depende_do_material · corrigida**  
_Nota(s): Controle axial da geometria do riser no pull in: tração de topo, compressão e risco de flambagem_

**P:** Como a tração no topo do riser se decompõe quanto à origem física?

**R:** Em parcela estática, ligada a peso próprio, gravidade e empuxo, e parcela dinâmica, ligada aos deslocamentos, velocidades e acelerações impostos ao topo.

_Explicação:_ Segundo o material, a tração no topo do riser é dividida em duas parcelas conforme sua origem física: uma estática, devida ao peso próprio e ao balanço entre gravidade e empuxo, e outra dinâmica, causada pelos movimentos impostos ao topo pela unidade.

**dificil_B · APROVADA**  
_Nota(s): Limites estruturais de tração e compressão no pull-in e na instalação do riser; Monitoramento operacional das forças de pull-in e dos esforços transmitidos ao sistema riser-unidade; Travamentos, aumento anormal de esforços e falhas de guincho/cabo ou linhas auxiliares em manobras submarinas de pull in de risers_

**P:** Durante o pull-in de um riser vazio, a tensão registrada continuamente no sistema de tração sobe abruptamente, mas o conjunto praticamente não avança. Ao mesmo tempo, o stability programme não mostra mudança compatível nos esforços globais da unidade, e as tentativas de seguir puxando só repetem o pico de carga. Qual deve ser a decisão operacional diante desse padrão?

**R:** Tratar como provável travamento ou enroscamento e interromper a manobra para reavaliação, sem aumentar a tração.

_Explicação:_ A combinação de carga crescente sem deslocamento útil indica perda de correspondência entre comando, movimento e carga, padrão típico de travamento ou enroscamento. Como a tração deve ser monitorada continuamente e correlacionada com a resposta da unidade, a ausência de mudança global compatível reforça que seguir aumentando a puxada tende a transferir esforço indevido ao riser e a equipamentos submarinos, com risco de dano.

_Às cegas (incorreta):_ Suspender imediatamente o pull-in, manter tensão segura/zero e travar o sistema; padrão indica enroscamento/obstrução local ou falha de medição, não esforço global. Inspecionar e diagnosticar (ROV, alinhamento/guia, roletes, I-tube) antes de retomar.

**media · APROVADA**  
_Nota(s): Critérios de suspensão, abortamento e preparação para tempo severo em operações de pull in de risers_

**P:** Antes de uma operação de pull in sujeita a tempo extremo sazonal, quais barreiras organizacionais prévias devem estar estabelecidas para evitar atraso, conflito de comando e resposta inadequada quando a condição piorar?

**R:** Contingências documentadas nos Hurricane ou Extreme Weather Plans; precedência clara desses planos com os Bridging Documents; discussão com as equipes e correção de lacunas de treinamento.

_Explicação:_ A resposta a tempo extremo depende de contingências já registradas para cenários em que a unidade não consiga evadir ou evacuar. Também é necessário definir qual plano prevalece entre os documentos aplicáveis e verificar se a prática real foi discutida com o pessoal, corrigindo lacunas de treinamento antes da temporada crítica.

_Às cegas (parcial):_ Comando unificado (RACI) e autoridade de parada; janela/meteo criteria e gatilhos Go/No-Go; plano de contingência e abort/recovery; comunicação formal (briefings, handover, canais); coordenação com marine/DP/tug/shore; recursos críticos e sobressalentes; exercícios/simulados e Lições Aprendidas; MOC e aprovação HSE.

**dificil_A · APROVADA**  
_Nota(s): Critérios de controle de carga axial no topo do riser durante hang-off e transferência para a suportação definitiva_

**P:** Durante o hang-off de um riser, a verificação mostra fator de utilização das tensões abaixo do limite admissível, mas a transferência de carga para a suportação definitiva faria o esforço axial no topo cruzar para compressão. Essa transferência é aceitável?

**R:** Não. A transferência é rejeitável, porque o topo do riser deve permanecer em tração; compressão na junta de topo não é admitida para preservar o flexjoint.

_Explicação:_ Atender apenas ao fator de utilização das tensões não basta. O critério operacional e estrutural exige simultaneamente utilização inferior ao limite e esforço axial de topo sempre trativo, porque a compressão na junta de topo viola a preservação do flexjoint.

_Às cegas (incorreta):_ Em geral, não: cruzar para compressão no topo durante a transferência é inaceitável sem comprovar que o riser/hang-off e conectores são aptos a compressão e que flambagem (global/local) e estabilidade sob movimentos foram verificadas. Falta essa verificação/aprovação de projeto.

**facil · REPROVADA: suporte, autonomia**  
_Nota(s): Movimentos do casco e posição de conexão na viabilidade de risers em FPSOs_

**P:** Para FPSOs nas condições de Campos e Santos, qual configuração de riser rígido é inviável e qual ainda depende de estudo específico de viabilidade: catenária livre ou SLWR?

**R:** A catenária livre é inviável; a SLWR pode ser viável, mas requer estudo de viabilidade.

_Explicação:_ Nessas condições, a catenária livre não deve ser assumida como aplicável em FPSOs. A alternativa que ainda pode atender é a SLWR, desde que sua geometria e conexão ao casco sejam verificadas em estudo de viabilidade.

**media · APROVADA**  
_Nota(s): Teste hidrostático após instalação de risers flexíveis: finalidade, condicionantes e critérios de aceitação_

**P:** Após o pull in e a instalação de um riser flexível, a equipe avalia executar o teste hidrostático. Qual condição prévia define se esse ensaio pode ser realizado ou deve ser evitado?

**R:** Só deve ser realizado se relatório de instalação, inspeção visual e análise de vida de serviço não indicarem falha estrutural significativa.

_Explicação:_ O teste hidrostático pós-instalação serve para verificar integridade e estanqueidade, mas não deve ser usado quando já há evidência de dano estrutural relevante. Se essas três fontes indicarem falha significativa, a pressurização pode agravar o defeito e levar à falha durante o ensaio.

_Às cegas (incorreta):_ Só pode executar se o riser (tipo/ED) estiver qualificado e o fabricante/procedimento do projeto permitir teste hidrostático pós-instalação; caso contrário, deve ser evitado por risco ao liner/armaduras/anelar. Falta confirmar a exigência do fabricante/ITP.

**facil · REPROVADA: codigo:depende_do_material · corrigida**  
_Nota(s): Planejamento de SIMOPS e coordenação formal de interfaces no pull in de risers_

**P:** Antes e durante a mobilização para pull in de riser, quais duas etapas formais de planejamento e coordenação não devem ser omitidas para controlar interfaces e riscos subsea?

**R:** Reunião formal de SIMOPS e avaliação de riscos, incluindo hazard assessment.

_Explicação:_ No caso citado de operação offshore com embarcação de apoio e trabalho subsea, a omissão dessas duas etapas caracterizou planejamento e coordenação inadequados e contribuiu para o incidente durante mobilização e execução.

**media · APROVADA**  
_Nota(s): Influência da geometria de conexão e do casco na viabilidade do pull-in de risers em FPSOs_

**P:** Na comparação de configurações de riser para reduzir risco de interação entre linhas durante o pull-in e na geometria final conectada ao FPSO, qual medida é usada como critério de interferência e que decisão ela orienta?

**R:** Usa-se o deslocamento transversal; selecionam-se as configurações com menor deslocamento para minimizar a interferência entre risers.

_Explicação:_ O critério de interferência entre risers é baseado na medição do deslocamento transversal de cada configuração. Essa comparação orienta a escolha das alternativas com menor deslocamento, porque elas têm menor potencial de interferência entre linhas.

_Às cegas (incorreta):_ Usa-se a distância mínima/clearance (folga) entre as linhas (centro‑a‑centro ou casca‑a‑casca) como critério de interferência. Ela orienta a escolha da configuração/posição (slot/porch) e, se necessário, a sequência de pull‑in para manter a folga mínima requerida.

### Produção e Processo (Medição Fiscal e Sistema de Alívio)

#### Compressão de Gás

**facil · APROVADA**  
_Nota(s): Condicionamento do gás comprimido em FPSO: separação de condensado, desidratação por TEG e prevenção complementar de hidratos_

**P:** Qual é a função dos scrubbers instalados antes de cada estágio de compressão em um trem de gás multiestágio?

**R:** Remover condensado e líquido livre antes de cada estágio, reduzindo o arraste de líquidos no trem de compressão.

_Explicação:_ Nos arranjos multiestágio, o scrubber antecede cada compressor para retirar condensado do gás antes da compressão seguinte. Isso reduz a presença e o arraste de líquidos ao longo do trem de compressão.

_Às cegas (equivalente):_ Remover líquidos condensados (água/HC) e sólidos/aerossóis do gás antes de cada compressor, protegendo contra slugging, erosão, corrosão e danos mecânicos, além de melhorar eficiência e controlar o ponto de orvalho entre estágios.

#### Operação de Separadores Trifásicos

**facil · REPROVADA: escopo**  
_Nota(s): Dimensionamento de PSV, superdimensionamento e risco de chatter_

**P:** Que comportamento operacional caracteriza o chatter em uma PSV?

**R:** Abertura e fechamento rápidos e repetitivos da PSV.

_Explicação:_ Chatter é uma condição operacional anormal em que a PSV não permanece em alívio sustentado, mas cicla rapidamente entre abrir e fechar. Esse comportamento pode danificar a válvula e comprometer sua função de proteção.

**media · APROVADA**  
_Nota(s): Emulsões e dificuldades na separação óleo-água em separadores trifásicos_

**P:** Em um separador trifásico, o óleo chega com água dispersa em gotículas finas e presença de emulsificantes adsorvidos na interface. Qual efeito isso tende a produzir sobre a separação gravitacional óleo-água?

**R:** Forma gotas menores com filme interfacial estável, reduz a coalescência e dificulta que a água se torne fase livre para decantar.

_Explicação:_ Os emulsificantes adsorvidos na interface reduzem a tensão interfacial e favorecem a formação de gotículas menores. Ao mesmo tempo, o filme interfacial dificulta floculação e coalescência, então a água permanece emulsificada em vez de se segregar como fase livre no vaso.

_Às cegas (equivalente):_ Gotas de água muito finas e emulsificantes estabilizam a emulsão, reduzem a coalescência e a velocidade de sedimentação (Stokes), aumentando arraste e dificultando/retardando a separação gravitacional, exigindo mais tempo de residência e/ou demulsificante/aquecimento.

#### Operação de Tratadores Eletrostáticos

**facil · APROVADA**  
_Nota(s): Prevenção de arc flash em tratadores eletrostáticos durante operação, drenagem, limpeza e manutenção_

**P:** Qual efeito da queda do nível de fluido abaixo da seção de coalescência sobre os componentes elétricos do tratador eletrostático exige atuação automática do sistema de potência?

**R:** Ela expõe os componentes de alta tensão, que devem ser automaticamente desenergizados por intertravamento de nível baixo.

_Explicação:_ Quando o nível cai a ponto de expor os componentes elétricos, a condição elétrica prevista pelo processo deixa de existir e manter a energização se torna perigoso. Por isso, a barreira adequada é retirar energia automaticamente nessa condição.

_Às cegas (equivalente):_ Com o nível abaixo da seção de coalescência, os eletrodos ficam parcialmente “a seco”, reduzindo a condução e aumentando corona/arco elétrico, aquecimento e risco de perfuração de isoladores/transformador. Exige atuação automática para desenergizar/cortar a alta tensão.

#### Operação Geral FPSO

**facil · APROVADA**  
_Nota(s): Operação marítima de alívio/offloading em FPSO e interface com navios aliviadores_

**P:** Quais são as duas alternativas básicas para exportar o óleo armazenado em um FPSO durante a operação de offloading?

**R:** Via bóia CALM/monobóia ou diretamente do FPSO, em tandem offloading.

_Explicação:_ Na exportação por offloading, o óleo armazenado pode ser transferido ao navio aliviador por dois arranjos básicos: usando uma bóia CALM/monobóia ou por conexão direta com o FPSO no arranjo tandem.

_Às cegas (incorreta):_ As duas alternativas básicas são: exportação para navio aliviador via mangotes/flutuantes (tandem ou side-by-side) e exportação por duto submarino (pipeline) para terra ou outra unidade. Falta definir se a pergunta restringe “offloading” apenas a navio aliviador.

**media · APROVADA**  
_Nota(s): Controle operacional de partidas, paradas e retomada após intervenção em FPSOs_

**P:** Após manutenção ou período ocioso em um sistema de processo de FPSO, qual condição justifica tratar a reintrodução de fluidos como gestão de mudança?

**R:** A possibilidade de o sistema não estar mais na mesma condição operacional, exigindo reavaliação dos perigos e dos controles antes da reintrodução.

_Explicação:_ O retorno de fluidos após manutenção ou ociosidade não deve ser assumido como simples retomada do estado anterior, porque mudanças ocorridas no período podem tornar inadequados os perigos e controles previamente considerados. Por isso, a retomada deve ser tratada como caso específico de gestão de mudança antes do start-up.

_Às cegas (parcial):_ Qualquer alteração da condição de integridade/operacional do sistema (intervenção que abriu linha, substituição de materiais/valvulas/instrumentos, mudança de procedimento/limites) ou risco de incompatibilidade/contaminação ao reiniciar justifica MOC. Falta definir o escopo exato da manutenção/isolamentos executados.

#### Produção, processo e processamento do óleo

**facil · APROVADA**  
_Nota(s): Restrições de escoamento e compressão como fontes de perda de produção e consumo energético_

**P:** Quais condições determinam os vários estágios de compressão da corrente de gás ao longo do processo e após o processamento?

**R:** As perdas de pressão no processo e a pressão requerida no destino final do gás.

_Explicação:_ A recompressão é necessária porque a corrente perde pressão ao longo do processo. Além disso, a pressão final a ser atingida depende da finalidade do gás no seu destino, o que define os estágios de compressão requeridos.

_Às cegas (parcial):_ Definem os estágios: pressão/temperatura disponíveis na sucção; pressão requerida na descarga (exporto, reinjeção, fuel gas); vazão e composição (MW, CO2/H2S); limites de T de descarga/condensação; anti-surge/turn-down; eficiência/energia; inter-resfriamento; NPSH e controle. Falta especificar a pressão-alvo de cada serviço.

#### Sistema de Alívio e Flare

**facil · APROVADA**  
_Nota(s): Estanqueidade, vazamentos e tratamento de falhas em componentes do sistema de alívio e flare_

**P:** O que caracteriza perda de estanqueidade, para fins de integridade mecânica, em componentes de um sistema de alívio e flare?

**R:** Perda não intencional de contenção em componentes ou interfaces seladas, incluindo vazamento visível e emissão fugitiva.

_Explicação:_ Em integridade mecânica, o ponto central é a perda de contenção do fluido em elementos de vedação e interfaces mecânicas. Tanto vazamentos visíveis quanto emissões fugitivas representam o mesmo desvio fundamental de estanqueidade.

_Às cegas (equivalente):_ Perda de estanqueidade é qualquer vazamento não intencional de hidrocarbonetos/água/inerte para atmosfera, dreno/coletores indevidos ou entre seções (válvulas, flanges, selos, PSV, discos de ruptura, juntas, tampões) que comprometa a contenção, detectado por queda de pressão, LEL, ruído/bolhas ou inspeção.

#### Sistema de captação e tratamento de água do mar para injeção no reservatório

**facil · APROVADA**  
_Nota(s): Prevenção de incrustação na injeção de água e uso de métodos preditivos para selecionar anti-incrustantes_

**P:** Qual estratégia de controle de incrustação é indicada na injeção de água quando os depósitos formados tendem a ser duros e de baixa solubilidade?

**R:** Controle predominantemente preventivo com uso de anti-incrustantes, em vez de depender de remoção corretiva periódica.

_Explicação:_ Quando a incrustação já formada é dura e pouco solúvel, os processos de remoção são limitados e as intervenções corretivas consomem tempo e recursos. Por isso, a estratégia mais adequada é prevenir a formação do depósito com tratamento químico apropriado.

_Às cegas (equivalente):_ Usar inibidor de incrustação do tipo limiar (fosfonatos/polímeros) em injeção contínua, focando prevenção, pois depósitos duros/baixa solubilidade não respondem bem à dissolução. Falta definir a química da incrustação (carbonato, sulfato, sílica) para selecionar o produto/dosagem.

#### Sistema de drenagem aberta e fechada

**facil · REPROVADA: suporte**  
_Nota(s): Drenagem aberta/fechada: segregação, ventilação dos vasos e interface com flare KO drum em FPSO_

**P:** Qual é o mecanismo pelo qual seal pots, loop seals e lute seals mantêm a segregação entre sistemas de drenagem?

**R:** Eles formam uma vedação líquida que impede a migração de gás entre sistemas de dreno.

_Explicação:_ Esses dispositivos mantêm um selo hidráulico entre circuitos de dreno. Essa barreira líquida preserva a segregação ao evitar a passagem de gás de um sistema para outro.

**media · REPROVADA: suporte**  
_Nota(s): Isolamento e controle seguro de intervenções em sistemas de drenagem aberta e fechada_

**P:** Em uma intervenção em sistema de drenagem que exige bloqueio e etiquetagem e foi submetida a análise de riscos, qual é a diferença funcional entre o isolamento de processo e a Permissão para Trabalho?

**R:** O isolamento controla fisicamente a condição da planta; a PTW formaliza as salvaguardas, responsabilidades e restrições da execução.

_Explicação:_ O isolamento de processo atua sobre a condição física da instalação para evitar comunicação indevida e liberações perigosas durante mudanças temporárias do estado da planta. A PTW complementa essa barreira ao autorizar e disciplinar a execução, definindo controles administrativos para a atividade identificada na análise de riscos.

**media · REPROVADA: suporte**  
_Nota(s): Arranjo do sistema de drenagem aberta e fechada e gestão de integridade de linhas internas a tanques, headers e vasos de drenagem_

**P:** Em um arranjo de drenagem que depende de escoamento por gravidade, separação de fases e bombeamento, qual é o efeito hidráulico mais direto de corrosão interna, incrustação ou obstrução nas linhas?

**R:** Aumentam a resistência ao escoamento, alterando níveis e pressões e podendo inverter fluxos ou interligar volumes que deveriam permanecer isolados.

_Explicação:_ Esses sistemas dependem de rota hidráulica definida para conduzir correntes distintas até tanques, vaso de drenagem ou tubo de despejo. Quando a linha perde capacidade de escoamento, o balanço hidráulico local muda; isso afeta níveis e pressões e pode criar comunicação indevida entre volumes segregados.

**facil · APROVADA**  
_Nota(s): Segregação de correntes e capacidade de drenagem/tratamento em sistemas de drenagem aberta e fechada_

**P:** Quais dois desvios a segregação entre água pluvial limpa e correntes potencialmente contaminadas deve evitar no sistema de drenagem?

**R:** Lançamento de poluentes no sistema pluvial limpo e no corpo receptor, e sobrecarga da ETE por entrada indevida de água pluvial limpa.

_Explicação:_ A segregação deve manter separadas as correntes conforme sua qualidade. Assim, evita tanto a descarga inadequada de água contaminada para o pluvial limpo quanto a perda de capacidade da ETE por receber água limpa que não precisaria ser tratada.

_Às cegas (equivalente):_ Evitar: (1) desvio/mistura de água oleosa ou contaminada para o dreno mar (descarga indevida); (2) desvio de água pluvial limpa para o sistema oleoso (slop/OWS), sobrecarregando tratamento e aumentando volume de resíduos.

#### Tratamento do Gás produzido

**facil · APROVADA**  
_Nota(s): Equilíbrio de fases e formação incipiente de hidratos no gás produzido_

**P:** Na curva de hidrato de um diagrama de fases gás-água, o que significa estar sobre a curva, acima dela e abaixo dela?

**R:** Sobre a curva, há formação incipiente; acima dela, o hidrato já está formado; abaixo dela, o hidrato não se forma.

_Explicação:_ A curva de hidrato representa o limite termodinâmico de início da formação. Sobre a curva está a condição de equilíbrio de formação incipiente; acima dela o sistema está na região de hidratos; abaixo dela permanece fora dessa região.

_Às cegas (equivalente):_ Sobre a curva: condição de equilíbrio do hidrato (início/dissociação). Acima da curva: região estável, hidrato pode se formar/manter. Abaixo da curva: hidrato termodinamicamente instável, não se forma ou dissocia. Falta definir eixos (P×T) para “acima/abaixo”.

### Segurança Operacional, SGSO, Sistemas de Segurança e Gestão de Riscos

#### Estudos de Segurança

**facil · APROVADA**  
_Nota(s): Riscos de operações marítimas e subsea com DP: deriva, desconexão de emergência e tempo para encerrar a tarefa_

**P:** Que mecanismo leva ao acionamento do EDS quando uma embarcação em DP perde a capacidade de manter proa e posição sob agravamento ambiental rápido, próxima de infraestrutura submarina?

**R:** A perda de proa e posição provoca deriva não comandada em direção à infraestrutura submarina, e o EDS é acionado para evitar colisão ou dano subsea.

_Explicação:_ Sob agravamento ambiental rápido, o DP pode deixar de sustentar simultaneamente proa e posição. A embarcação então deriva e a desconexão de emergência atua como barreira final para impedir que a perda de controle de posição se converta em impacto ou dano à infraestrutura submarina.

_Às cegas (incorreta):_ O agravamento ambiental eleva o erro DP e a taxa de deriva; ao ultrapassar limites de posição/velocidade (watch circle) ou perder redundância/controle, o DP gera alarme crítico e aciona EDS automaticamente para evitar colisão/overload do riser umbilical.

#### Operações simultâneas – SIMOPS

**facil · APROVADA**  
_Nota(s): Gestão de atmosferas perigosas por detecção de gás, ventilação e prevenção de exposição em SIMOPS_

**P:** Que efeito de segurança a realimentação de ar exaurido contaminado para o interior do prédio pode provocar?

**R:** Pode levar gases e vapores inflamáveis a áreas internas antes não afetadas, formando atmosfera perigosa com risco de exposição e ignição.

_Explicação:_ Se o ar exaurido contaminado retorna ao prédio, o contaminante pode alcançar ambientes que deveriam permanecer seguros. Isso amplia a área exposta a atmosfera inflamável e aumenta o risco tanto para pessoas quanto para fontes de ignição nessas áreas.

_Às cegas (equivalente):_ Pode introduzir gases/vapores tóxicos ou inflamáveis no ambiente interno, causando asfixia/intoxicação, atmosferas explosivas, alarmes falsos e propagação de contaminantes; aumenta risco de ignição e compromete evacuação. Falta definir o tipo/nível de contaminante e a taxa de recirculação.

**media · APROVADA · corrigida**  
_Nota(s): SIMOPS: revisão de riscos, gestão de mudanças e controle de desvios antes da execução_

**P:** Em uma SIMOPS com teste em serviço proposto para uma linha de gás, qual é o critério para admitir esse teste?

**R:** Apenas sem alternativa, ou se desmontar juntas elevar o risco, e com revisão formal do desvio por pessoas apropriadas.

_Explicação:_ Em sistemas de hidrocarbonetos, especialmente de gás, o teste em serviço deve ser normalmente evitado. Só pode ser admitido nas exceções indicadas, e então exige revisão formal do desvio das exigências normais de teste por pessoas apropriadas.

_Às cegas (incorreta):_ Admite-se o teste em serviço somente se a Análise de Risco/SIMOPS demonstrar risco ALARP, com barreiras íntegras: isolamentos/duplo bloqueio e sangria, controle de fontes de ignição, detecção de gás ativa, ESD disponível, PTW/LOTO e plano de emergência.

#### Segurança e Controle de Riscos

**facil · APROVADA**  
_Nota(s): DDS/toolbox e ferramentas de avaliação operacional: comunicação, capacitação, aderência procedimental e efetivo como base da execução segura_

**P:** Qual é o papel do DDS/toolbox quando a tarefa já é controlada por um procedimento operacional crítico tratado como salvaguarda da análise de risco?

**R:** Apoiar a execução segura e reforçar a aderência ao procedimento; não substituir a salvaguarda, que é o procedimento operacional crítico.

_Explicação:_ O procedimento operacional crítico é a própria salvaguarda para cenários relevantes, enquanto o DDS/toolbox funciona como ferramenta pré-tarefa e de alinhamento para comunicar perigos, mitigadores e sustentar a aderência na execução sob supervisão. Portanto, seu papel é complementar a aplicação da salvaguarda, não substituí-la.

_Às cegas (equivalente):_ O DDS/toolbox complementa o procedimento crítico: confirma entendimento e aderência, revisa perigos e salvaguardas do dia (interfaces, mudanças, condições reais), define papéis e comunicação, e verifica prontidão para executar com segurança. Falta definir se há mudanças/MOC ou simultaneidades.

**media · APROVADA**  
_Nota(s): PTW em áreas classificadas e sistemas de hidrocarbonetos: reconhecimento de ignição, cenários de evento maior e gestão de salvaguardas afetadas_

**P:** Em uma PTW para área classificada, a resposta ao campo sobre risco de centelha, faíscas ou eletricidade estática foi “não”. Porém, a tarefa autorizada inclui corte com maçarico, solda ou preparação de superfície com lixadeira elétrica. O que essa inconsistência caracteriza?

**R:** Falha de identificação do perigo de ignição na emissão da PTW, e não mera falha documental.

_Explicação:_ Essas atividades reconhecidamente geram faíscas ou fagulhas. Se a PTW nega esse risco em área classificada, o desvio não é apenas de preenchimento: o perigo principal foi identificado de forma incorreta, comprometendo a seleção e o monitoramento dos controles.

_Às cegas (parcial):_ Caracteriza não conformidade grave/erro de avaliação de riscos na PTW (preenchimento incorreto), com autorização indevida de trabalho a quente em área classificada e falha de controle de ignição, tornando a permissão inválida até correção e revalidação.

#### SGSO

**facil · APROVADA**  
_Nota(s): Fatores de qualidade da manutenção que sustentam a integridade mecânica_

**P:** Qual é o requisito aplicável aos instrumentos e controles de vasos de pressão que interferem na segurança do equipamento?

**R:** Devem ser periodicamente calibrados e mantidos em boas condições operacionais.

_Explicação:_ Esses dispositivos integram a proteção do vaso de pressão e precisam responder corretamente nas condições reais de operação. Por isso, a integridade mecânica exige tanto calibração periódica quanto manutenção do seu bom estado operacional.

_Às cegas (equivalente):_ Instrumentos e controles de vasos de pressão que interferem na segurança devem ser dispositivos de segurança adequados ao serviço, com atuação confiável (preferencialmente fail-safe), independentes quando aplicável, mantidos operacionais, calibrados e testados/inspecionados periodicamente, sem bloqueio/by-pass não autorizado.

**media · REPROVADA: suporte**  
_Nota(s): Procedimentos operacionais para partida, transientes, condições degradadas e contingência operacional no SGSO_

**P:** Durante a partida de um FPSO, a estratégia de alarmes é ajustada para refletir a condição transitória da instalação. O que essa estratégia deve assegurar para a equipe de operação nessa fase?

**R:** Que a equipe de operação lide apenas com os alarmes aplicáveis à fase de partida.

_Explicação:_ Na partida, a instalação opera fora da condição estável, então a estratégia de alarmes deve ser compatível com essa fase. Isso evita que a equipe seja exposta a alarmes não pertinentes ao estado momentâneo da planta e foque nos sinais relevantes para a condução segura do start-up.

**dificil_A · APROVADA**  
_Nota(s): Evidências documentais, registros e rastreabilidade para demonstrar conformidade do SGSO_

**P:** Em uma verificação de mudança já implementada em uma unidade offshore, a modificação física está concluída, mas o procedimento disponível está fora do controle documental e sem atualização válida; não há evidência de treinamento aplicável nem registro de close out. Qual é o diagnóstico de conformidade do SGSO para essa mudança?

**R:** A mudança não pode ser considerada conforme nem com risco demonstradamente sob controle.

_Explicação:_ A verificação de uma mudança concluída exige evidência documental de atualização, treinamento aplicável e fechamento formal. Quando o documento está fora de controle e faltam registros confiáveis de treinamento e close out, o procedimento perde função como barreira e não há como demonstrar a implementação efetiva do tratamento do risco.

_Às cegas (parcial):_ Não conforme: a Mudança não atende ao SGSO/MoC. Embora a modificação física esteja concluída, há falha de controle documental (procedimento não controlado/atualizado), ausência de evidência de treinamento e inexistência de registro de close out; mudança não pode ser considerada encerrada.

#### Sistema de Combate a Incêndio

**facil · APROVADA**  
_Nota(s): Integração entre detecção de fogo e gás, SIS/ESD, supressão e HVAC nas ações automáticas de emergência_

**P:** Qual é a cadeia funcional básica de um sistema de fogo e gás integrado ao SIS/ESD?

**R:** Sensores de campo detectam o evento; a lógica de segurança no CLP/SIS processa o sinal; os atuadores finais executam a ação de segurança.

_Explicação:_ Em sistemas instrumentados de segurança, a função é organizada em três etapas: detecção por sensores, processamento da lógica de segurança e atuação física no campo. Essa estrutura é a base da integração entre fogo e gás, SIS/ESD e os elementos que realizam a resposta automática.

_Às cegas (equivalente):_ Detecção (sensores F&G) → F&G logic solver/PLC → votação/validação e alarmes → comando ao SIS/ESD → atuação: isolamentos (SDV/ESDV), parada de processo, depressurização/BDV, shutdown elétrico, liberação de combate (deluge/drencher), ventilação/fechamento de dampers.

#### Sistema de Fogo e Gás (F&G)

**facil · REPROVADA: autonomia, codigo:depende_do_material, resposta_unica_cega · corrigida**  
_Nota(s): Detecção e análise de H2S em líquidos e em áreas abertas: distinção entre métodos analíticos e detecção de campo_

**P:** Segundo o material apresentado, quais métodos são citados para detectar H2S em ambientes abertos em uma plataforma?

**R:** Papel embebido de acetato de chumbo e instrumentos portáteis de detecção de H2S.

_Explicação:_ A condição foi restringida ao que o material cita para ambientes abertos. Nesse contexto, os métodos mencionados são o papel embebido de acetato de chumbo e os instrumentos portáteis de detecção de H2S.

_Às cegas (alternativa_valida):_ Em áreas abertas usa-se monitoramento pessoal (detector portátil multigás) e fixo (detectores H2S pontuais eletroquímicos/IR, open-path/feixe IR/UV, cercas perimetrais/wind-sock com alarmes) integrados ao F&G e amostragem para tubos colorimétricos.

**media · APROVADA · corrigida**  
_Nota(s): Verificação de aderência, contingenciamento e atualização da estratégia de F&G por estudos de cobertura e mapeamento de detectores_

**P:** Em uma fire zone, compare três desvios de F&G: inibições sucessivas na mesma zona, quantidade de detectores abaixo do mínimo requerido e detectores indisponíveis sem contingenciamento associado. Qual é o efeito específico de cada desvio sobre a proteção esperada?

**R:** As inibições sucessivas reduzem a cobertura; o mínimo insuficiente impede a atuação automática prevista; a indisponibilidade sem contingenciamento deixa a barreira sem compensação.

_Explicação:_ Os três desvios degradam a proteção por mecanismos distintos. Inibições sucessivas diminuem a capacidade de detecção na área. Detectores abaixo do mínimo requerido impedem o cumprimento da matriz de causa e efeito. Já a indisponibilidade sem contingenciamento mantém a perda da barreira sem medida compensatória.

_Às cegas (parcial):_ Inibições sucessivas: reduz/zera detecção/ação automática enquanto durar, elevando risco de fogo/gás não mitigado. Abaixo do mínimo de detectores: baixa cobertura e confiabilidade, aumenta probabilidade de não detectar/atrasar alarme. Indisponíveis sem contingência: perda de camadas de proteção sem compensação, degradando SIL/LOPA e resposta.

#### Sistemas e equipamentos de salvatagem

**facil · APROVADA · corrigida**  
_Nota(s): Condições de acesso, descida ao mar e lançamento seguro de life rafts_

**P:** Para abandono por life raft, classifique os seguintes meios de descida ao nível do mar em controlados ou não controlados: donuts, escape chutes, escadas fixas, cordas com nós e redes de escalada.

**R:** Controlados: donuts, escape chutes e escadas fixas; não controlados: cordas com nós e redes de escalada.

_Explicação:_ Segundo o critério do material, meios controlados de descida não devem depender de força e destreza do usuário sob emergência. Por isso, donuts, escape chutes e escadas fixas são controlados, enquanto cordas com nós e redes de escalada não são.

_Às cegas (erro):_ 

### Utilidades, geração de energia e sistemas auxiliares

#### Geração e distribuição de energia elétrica

**facil · REPROVADA: codigo:depende_do_material · corrigida**  
_Nota(s): Redundância e reconfiguração da distribuição para sustentar consumidores essenciais e de controle_

**P:** Quais consumidores são alimentados pelos sistemas redundantes de 24 Vcc de serviços gerais descritos?

**R:** CLP e painéis de controle dos geradores principais e de emergência.

_Explicação:_ Os sistemas redundantes de 24 Vcc descritos alimentam o CLP e os painéis de controle dos geradores principais e de emergência.

**media · APROVADA**  
_Nota(s): Base de risco e enquadramento de equipamentos em áreas classificadas_

**P:** Na seleção de equipamentos elétricos para uma área com potencial presença de gás inflamável, quais variáveis do ambiente definem o enquadramento da área em zonas?

**R:** A frequência e a duração da presença da atmosfera explosiva de gás.

_Explicação:_ O enquadramento em zonas decorre de com que frequência a atmosfera explosiva pode ocorrer e por quanto tempo ela permanece presente. Essas variáveis são a base para classificar a área e, a partir disso, selecionar o equipamento adequado.

_Às cegas (equivalente):_ Zona é definida por: frequência/probabilidade de atmosfera explosiva, duração de sua presença e grau/efetividade da ventilação (natural ou forçada), considerando direção do vento e obstáculos/confinamento. Falta a classificação do grupo de gás e temperatura de ignição (T-class) para selecionar o equipamento.

**dificil_A · APROVADA**  
_Nota(s): Aterramento e bonding como barreiras de segurança elétrica na instalação offshore_

**P:** Em um skid com ASD em área classificada, uma falha de isolamento energiza a carcaça metálica do equipamento. As partes metálicas estão bonded e aterradas, e a proteção detecta a anormalidade. Qual é a função coordenada dessas duas barreiras nessa condição?

**R:** Bonding e aterramento limitam o potencial de toque, enquanto a detecção com seccionamento automático elimina a persistência da falta ao desenergizar o circuito.

_Explicação:_ O bonding interliga as partes metálicas e, com o aterramento, reduz diferenças de potencial e favorece potenciais de toque seguros durante falta à terra. Já a proteção com alarme e seccionamento automático trata a continuidade da condição anormal, retirando a energia do circuito afetado.

_Às cegas (equivalente):_ O bonding/aterramento mantém equipotencialidade e fornece caminho de baixa impedância para a corrente de falha, reduzindo tensão de toque e evitando centelha por diferenças de potencial. A proteção detecta a falha à terra e desarma/isolando a energia rapidamente.

**media · APROVADA**  
_Nota(s): Degradação de equipamentos elétricos e técnicas diagnósticas associadas_

**P:** Em um sistema elétrico offshore, quais verificações apoiam diretamente a confiabilidade e a operação segura de equipamentos com SF6 e de equipamentos com interruptores ou disjuntores a vácuo?

**R:** Verificar a pureza e o teor de umidade do SF6 e realizar testes de vazamento no sistema com SF6 e no invólucro de vácuo.

_Explicação:_ A confiabilidade e a operação segura desses equipamentos dependem da condição do meio isolante e da integridade de vedação. Por isso, é necessário confirmar a qualidade do SF6 por pureza e umidade e verificar vazamentos tanto no sistema com SF6 quanto no invólucro de vácuo.

_Às cegas (parcial):_ SF6: checar pressão/densidade e alarmes, taxa de fuga, ponto de orvalho/umidade, pureza e subprodutos, estanqueidade/vedações e intertravamentos. Vácuo: monitorar integridade da garrafa (vácuo/indicador), resistência de isolamento, desgaste/curso/temporização de contatos e condição do mecanismo/contagem de operações.

**facil · REPROVADA: autonomia, codigo:depende_do_material, codigo:pergunta_composta · corrigida**  
_Nota(s): Sistemas de partida de unidades geradoras acionadas por turbina: motor de partida lateral e bloco de partida axial_

**P:** Em uma unidade geradora acionada por turbina com dois arranjos de partida descritos no material, quais são esses arranjos e qual uso operacional cada um permite?

**R:** Motor de partida lateral: partida da unidade completa ou geração de potência ativa; bloco de partida axial: partida só do gerador como compensador síncrono ou da unidade completa para potência ativa.

_Explicação:_ No material, a partida podia ser feita por motor de partida lateral ou por bloco de partida axial. O motor lateral era usado para partir a unidade completa ou para geração de potência ativa. O bloco axial podia partir apenas o gerador para operação como compensador síncrono, ou a unidade completa quando fosse necessário gerar potência ativa.

**dificil_B · APROVADA**  
_Nota(s): Arquiteturas de barramento, bus ties e transferência de circuitos; Proteção de barramentos seccionados, zonas diferenciais e falha de disjuntores; Seletividade e coordenação entre proteção primária e retaguarda em esquemas de sobrecorrente/falta à terra e arranjos de barramento_

**P:** Após uma falta em uma linha ligada a barramento seccionado, a ocorrência registra abertura de dois disjuntores. Nessa configuração, a seção de barramento participa da linha e a proteção local de retaguarda não se aplica. Qual critério distingue comportamento esperado da filosofia de proteção de perda de seletividade?

**R:** A abertura de dois disjuntores pode ser normal nessa topologia; há perda de seletividade apenas se a proteção de retaguarda atuar sem falha da proteção primária em eliminar a falta.

_Explicação:_ Em barramentos seccionados em que a seção participa da linha, ou em arranjos equivalentes com duas zonas diferenciais, uma falta na linha pode comandar a abertura de dois disjuntores como resposta prevista da configuração. Isso só caracteriza má coordenação quando a retaguarda intervém indevidamente, isto é, sem falha da proteção primária responsável pela área faltosa.

_Às cegas (parcial):_ Critério: verificar se os dois disjuntores abertos pertencem à zona prevista (linha + seção de barramento associada) por proteção principal/diferencial ou falha de disjuntor, dentro dos tempos. Se abriu fora da zona/sem atuação BF/dif, é perda de seletividade. Falta identificar quais disjuntores/proteções atuaram.

**media · APROVADA**  
_Nota(s): Gestão de bypass do ESD e preservação das interfaces elétricas durante manutenção e introdução de equipamento temporário_

**P:** Na introdução de equipamento temporário em uma unidade offshore, que conjunto de interfaces e documentos deve ser coordenado e atualizado para manter a coerência das barreiras e a resposta real do ESD?

**R:** Devem ser atualizados a detecção e a alarmística associadas ao ESD, incluindo sua lógica, e a documentação de arranjo e segurança da instalação, como classificação de áreas, rotas de fuga e desenhos de engenharia.

_Explicação:_ A introdução de equipamento temporário pode alterar barreiras existentes e criar incompatibilidades entre o que está instalado e o que a planta aparenta proteger. Por isso, além de coordenar impactos nos sistemas de segurança, é necessário atualizar detectores de gás, diagramas de alarme, lógica de ESD e a documentação de engenharia ligada ao arranjo e à segurança da instalação.

_Às cegas (equivalente):_ Coordenar: HAZID/HAZOP, MOC, SRS/filosofia ESD/PSD/F&G, C&E, matriz causa‑efeito e setpoints, lista de I/O e lógicas, diagramas (P&ID/ESD/F&G), classificações de área, POB/ERP, PTW/SIMOPS. Falta definir o tipo de equipamento temporário.

#### Sistema de utilidades

**facil · APROVADA**  
_Nota(s): Interfaces térmicas das utilidades com os consumidores de processo_

**P:** Qual é o percurso típico da água em um sistema de água de resfriamento de processo em recirculação fechada?

**R:** O header distribui aos consumidores; o retorno segue ao vaso de expansão e ao filtro, volta às bombas e é resfriado no permutador com água do mar.

_Explicação:_ No arranjo típico, a água é enviada pelas bombas ao header de distribuição, atende os consumidores e retorna mais quente pelo header de retorno. Esse retorno se conecta ao vaso de expansão, passa por filtro e segue novamente às bombas e ao permutador, onde rejeita calor para a água do mar antes de fechar o ciclo.

_Às cegas (parcial):_ Tanque de expansão/compensação → bombas de água de resfriamento (recirculação) → consumidores/trocadores de calor do processo → coletor de retorno → resfriador (trocador com água do mar ou ar) → volta ao tanque/linha de sucção, com purga/maquiagem e tratamento.

**media · APROVADA**  
_Nota(s): Requisitos de pressão e capacidade na geração e distribuição de ar comprimido_

**P:** Na estimativa da potência e do consumo de combustível de um compressor em um sistema de ar comprimido modelado em regime permanente, quais informações do modelo sustentam esse cálculo?

**R:** Vazões, velocidades, volumes, perfis de pressão e temperatura e propriedades do gás especificadas no modelo.

_Explicação:_ O cálculo de potência estimada e de requisitos de combustível do compressor é suportado pelas variáveis de processo e pelas propriedades do gás inseridas no modelo. Esses dados representam o estado hidráulico e termodinâmico necessário para estimar o desempenho da compressão em regime permanente.

_Às cegas (parcial):_ Sustentam o cálculo: vazão mássica/volumétrica de ar, pressões de sucção e descarga, temperaturas (sucção/inter-resfriamento), número de estágios e perdas de carga, eficiência isentrópica/politrópica e mecânica, razão de compressão, propriedades do gás e perfil de carga/horas; consumo: potência/equilíbrio térmico + SFC do prime mover.

**dificil_A · APROVADA · corrigida**  
_Nota(s): Biofilmes, biofouling e biocorrosão em sistemas auxiliares: progressão do problema e controle combinado_

**P:** Em um circuito auxiliar de água de uma FPSO, a dosagem de biocida reduziu a contagem microbiológica no fluido, mas persistem corrosão interna, perda de troca térmica e depósitos aderidos na tubulação. Qual ação deve vir primeiro para controlar o problema?

**R:** Remoção física regular dos depósitos, como pigging ou raspagem.

_Explicação:_ A queda da contagem no fluido com persistência de corrosão, perda de desempenho e depósitos aderidos indica colonização superficial já estabelecida. Como muitos biocidas atuam melhor sobre microrganismos em suspensão do que sobre biofilmes aderidos, o biocida isolado tende a ser insuficiente; por isso, a prioridade é remover fisicamente o depósito e depois manter controle combinado.

_Às cegas (equivalente):_ Primeiro, remover o biofilme/depósitos: executar limpeza/desincrustação da linha e trocadores (flush/pigging/limpeza química) para expor a superfície e restabelecer a troca térmica; só depois ajustar biocida/inibidor. Falta definir a composição dos depósitos para escolher o método.

**media · APROVADA**  
_Nota(s): Faixa operacional, suprimento alternativo e modulação de utilidades no sistema de flare/vent_

**P:** Ao definir a localização dos pontos de purga em um header de flare/vent, em que extremidade eles devem ser instalados para evitar trechos sem varredura efetiva?

**R:** Na extremidade a montante, para que todo o header seja varrido e não permaneçam dead legs.

_Explicação:_ Os pontos de purga devem ficar na extremidade a montante para que o fluxo de purga percorra o header inteiro. Isso reduz a possibilidade de trechos sem escoamento efetivo, que poderiam permanecer como dead legs.

_Às cegas (incorreta):_ Instale os pontos de purga nas extremidades cegas (dead-ends) e nos pontos mais distantes do selo/KO drum, preferencialmente na extremidade oposta ao fluxo principal, para garantir varredura contínua e evitar bolsões sem purga.

**facil · APROVADA**  
_Nota(s): Purga de headers de flare e vent para evitar ingresso de ar e mistura inflamável_

**P:** Em que condição uma taxa mínima de purga dos headers de flare e vent pode ser aceitável?

**R:** Quando as descargas contínuas e incidentais do processo forem suficientes para complementar a purga e impedir o ingresso de ar.

_Explicação:_ A aceitabilidade de uma taxa mínima de purga depende do modo operacional. Se o próprio sistema receber descargas do processo em quantidade suficiente para renovar o gás no interior do header, essa contribuição complementa a purga dedicada e mantém a barreira contra entrada de ar.

_Às cegas (incorreta):_ Pode ser aceitável quando os headers ficam inertizados/pressurizados com gás combustível ou N₂, com monitoramento de O₂/hidrocarbonetos garantindo mistura abaixo do LEL e acima do LOC, sem entradas de ar e com válvulas/selos íntegros. Falta definir o método de inertização e limites LOC/LEL aplicáveis.

### Descomissionamento e Gestão do Ciclo de Vida da Unidade

#### Geral

**facil · APROVADA · corrigida**  
_Nota(s): Continuidade da gestão de riscos e da segurança operacional da fase de operação ao descomissionamento_

**P:** Qual é o motivo técnico central para manter o SGSO e a gestão de riscos ativos após a parada da produção, durante todo o descomissionamento?

**R:** Porque o descomissionamento ainda expõe a unidade a perigos relevantes e impactos ESHS, exigindo controle contínuo até a retirada final.

_Explicação:_ A parada da produção não elimina o potencial de acidentes, poluição e outros impactos ambientais, sociais e de saúde e segurança. Como o descomissionamento continua sendo atividade com riscos relevantes, o sistema de gestão e a gestão de riscos devem permanecer ativos até a retirada definitiva de serviço.

_Às cegas (equivalente):_ Porque, após a parada, permanecem inventários energizados e perigosos (hidrocarbonetos residuais, pressão, eletricidade, içamentos, trabalhos a quente, químicos) e novas atividades de alto risco; o SGSO garante controle contínuo, barreiras, MOC e resposta a emergências durante todo o descomissionamento.

**media · APROVADA · corrigida**  
_Nota(s): Baseline survey e inspeções especiais como base técnica para extensão de vida de FPSO/FSU_

**P:** Em um FPSO de casco simples que armazenou água produzida, além da integridade estrutural, qual conjunto mínimo adicional deve constar da avaliação e da documentação de inspeção dos tanques?

**R:** Funcionalidade da proteção catódica, condição do revestimento e maior rigor na qualidade dos relatórios de inspeção.

_Explicação:_ Para tanques de FPSO de casco simples que armazenaram água produzida, a avaliação deve incluir, além da integridade estrutural, a funcionalidade da proteção catódica e a condição do revestimento. As inspeções de tanques também exigem aumento do grau de exigência na qualidade das inspeções e dos respectivos relatórios, inclusive quando executadas por terceiros.

_Às cegas (parcial):_ Além da estrutura: condição do revestimento/lining; mapeamento de corrosão (pites/MIC) e medições de espessura; estado da proteção catódica/ânodos; histórico e evidências de limpeza, desgaseificação e testes de atmosfera/contaminação (óleo, H2S/radioatividade/NORM).

**dificil_A · REPROVADA: suporte, codigo:pergunta_composta**  
_Nota(s): Encerramento de pendências de integridade, inspeção, manutenção e governança operacional no fim de vida da unidade_

**P:** Na preparação para retirar uma FPSO de serviço, a equipe quer priorizar entre reparar, substituir, manter com monitoramento reforçado ou retirar equipamentos da operação. Há achados de classe disponíveis, mas também histórico disperso de inspeções, reparos, anomalias antigas, backlog e modificações. Qual base integrada deve orientar essa priorização, e qual é a limitação de usar apenas os requisitos de classificação?

**R:** O resumo anual de integridade; a classificação sozinha não abrange todos os elementos estruturais e equipamentos relevantes para a decisão.

_Explicação:_ A priorização no fim de vida deve partir de uma visão consolidada do estado atual de integridade, reunindo histórico de inspeções, reparos, anomalias pendentes, backlog, modificações e principais ameaças. A avaliação não deve ser feita por um item isolado, e os requisitos de classificação não abrangem necessariamente todos os elementos estruturais e equipamentos importantes para a decisão.

**media · APROVADA**  
_Nota(s): Critérios de decisão entre aceitar, monitorar, reparar, reforçar ou substituir em condições de degradação_

**P:** Ao avaliar uma indicação de degradação em um equipamento offshore, em que condição técnica é mais apropriado aceitar o defeito com monitoramento em vez de repará-lo?

**R:** Quando a indicação não compromete a integridade atual do equipamento e sua expansão e seus efeitos podem ser identificados e monitorados.

_Explicação:_ A decisão não deve ser automática só porque existe uma não conformidade. Se a condição observada for irrelevante para a integridade no estado atual e houver capacidade de acompanhar sua evolução e consequências, manter em serviço com monitoramento pode ser a alternativa tecnicamente mais segura.

_Às cegas (equivalente):_ Aceite com monitoramento quando a indicação for estável, de baixa severidade, sem impacto na integridade/segurança/produção, com vida remanescente comprovada por análise (FCA/FFS) e limites/critério de disparo definidos. Falta confirmar o resultado do FFS/vida remanescente.

**facil · APROVADA**  
_Nota(s): Avaliação contínua de estabilidade, distribuição de pesos e centro de gravidade com remoção progressiva de cargas_

**P:** Quais dois fatores tornam crítica a disposição de equipamentos na superestrutura de uma plataforma flutuante, inclusive em emergência?

**R:** A sensibilidade a cargas excêntricas e à posição vertical do centro de gravidade.

_Explicação:_ Em plataformas flutuantes, a distribuição dos equipamentos na superestrutura afeta diretamente a resposta da unidade porque ela é sensível tanto a assimetrias de carga quanto à elevação do centro de gravidade. Essa sensibilidade permanece relevante em condições normais e também em emergência.

_Às cegas (incorreta):_ Segurança de incêndio/explosão (segregação de áreas, afastamentos, ventilação e controle de fontes de ignição) e acessibilidade/evacuação (rotas de fuga, combate a incêndio e acesso para operação/manutenção, inclusive sob fumaça, calor e dano estrutural).

**dificil_B · APROVADA**  
_Nota(s): Estabilidade, lastro e monitoramento da condição da FPSO na preparação para reboque; Avaliação contínua de estabilidade, distribuição de pesos e centro de gravidade com remoção progressiva de cargas; Limpeza, isolamento e reconfiguração estrutural da unidade após parada e antes de navegação/reboque_

**P:** Após a parada, a planta e os tanques foram limpos e isolados para preparação ao reboque. Em seguida, houve remoção progressiva de equipamentos no convés e esvaziamento de inventário líquido. O programa de estabilidade ainda indica condição aceitável, mas a equipe identifica que parte das cargas removidas não foi atualizada e a unidade dispõe de capacidade de lastro muito limitada. Qual decisão deve vir primeiro antes de declarar a FPSO apta ao trânsito?

**R:** Reconstituir e atualizar o inventário real de pesos e líquidos no programa de estabilidade; se o lastro não bastar, recompor peso e distribuição com volume em tanques de carga.

_Explicação:_ Após limpeza, esvaziamento e remoções, a condição da unidade deixa de ser fixa e precisa ser reavaliada com base no arranjo real de pesos. Como cargas de convés dependem de lançamento manual, o programa pode não representar a condição verdadeira; e, se a capacidade de lastro for limitada, manter a estabilidade pode exigir uso operacional de volume em tanques de carga para recompor a distribuição e os esforços monitorados.

_Às cegas (parcial):_ Primeiro, suspender a declaração de “apta ao trânsito” e recalcular/verificar a estabilidade com o weight control atualizado (todas as remoções/inventários). Falta confirmar a margem de GM/trim/ângulo e a capacidade real de lastro para corrigir desvios.

**media · REPROVADA: suporte**  
_Nota(s): Planejamento antecipado do descomissionamento ao longo do ciclo de vida_

**P:** Na gestão do ciclo de vida de uma unidade offshore, quais dois elementos de governança precisam estar definidos antecipadamente para reduzir incerteza e passivos no descomissionamento e encerramento?

**R:** Garantias ou provisões financeiras para o descomissionamento e responsáveis claramente identificados desde cedo.

_Explicação:_ A ausência de reservas financeiras e de responsabilização clara amplia a incerteza e o potencial de passivos no encerramento. Tratar esses elementos antecipadamente reduz impactos e melhora a previsibilidade do descomissionamento.

**dificil_A · REPROVADA: sem_pista, tipo_ok · corrigida**  
_Nota(s): Governança, competências, recursos e coordenação organizacional no ciclo de vida e no descomissionamento de FPSOs_

**P:** Durante a reorganização da equipe de uma FPSO na preparação para o descomissionamento, uma área terá redução de efetivo, outra terá reforço de pessoal, parte da equipe acumulará funções e também haverá admissões e desligamentos. Em quais alterações de pessoal o gerenciamento de mudanças de pessoas deve ser formalmente aplicado?

**R:** Redução, aumento e acúmulo de funções, além de entrada e saída de pessoas.

_Explicação:_ O processo de gerenciamento de mudanças de pessoas deve ser aplicado formalmente a redução, aumento e acúmulo de funções, bem como à entrada e à saída de pessoas.

**facil · APROVADA**  
_Nota(s): Reavaliação de riscos e controle operacional em mudanças complexas e fases finais do ciclo de vida_

**P:** Em Operações Simultâneas, qual condição exige tratamento específico e a implementação de procedimentos próprios de gestão?

**R:** Interfaces operacionais consideráveis com perigos novos, logística especial não coberta ou impacto na disponibilidade/funcionalidade de ECSO exigem procedimentos específicos de SIMOPS.

_Explicação:_ Não basta haver atividades simultâneas. O tratamento específico é exigido quando a interface entre elas introduz perigos novos, requer logística ou procedimentos fora das práticas já previstas, ou compromete Elementos Críticos de Segurança Operacional, caso em que devem ser implementados procedimentos próprios de gerenciamento.

_Às cegas (parcial):_ Quando duas ou mais atividades ocorrem simultaneamente com potencial de interferência mútua, elevando o risco (uma pode afetar a integridade/segurança da outra), exige tratamento específico e procedimentos próprios de gestão. Falta definir quais operações estão combinadas no seu caso.

**media · APROVADA**  
_Nota(s): Planos e registros de integridade como base para decisões de fim de vida, refurbishment e destinação_

**P:** Na avaliação de fim de vida de um ativo offshore, um reparo antigo aparece no histórico, mas é preciso comprovar que aquela condição não corresponde ao projeto original. Quais registros de reparo devem existir para dar essa rastreabilidade técnica?

**R:** Relatório de inspeção extraordinária, procedimentos de reparo, serviços executados e identificação do pessoal qualificado envolvido.

_Explicação:_ Esses registros permitem vincular a condição encontrada à intervenção realizada, distinguindo uma condição modificada ou restaurada da condição original de projeto. Sem essa documentação, aumenta a incerteza sobre a extensão do dano, o método aplicado e a qualificação da execução.

_Às cegas (parcial):_ Devem existir: relatório de anomalia/inspeção e classificação; engenharia de reparo aprovada (desenhos/cálculos/aceite de classe); MOC; ITP/QCP; WPS/PQR e qualificação de soldadores; certificados de materiais/rastreabilidade; NDT/PMI/HT; as-built/redlines; relatório de conclusão e liberação operacional.

**facil · REPROVADA: codigo:pergunta_composta · corrigida**  
_Nota(s): Condição de limpeza, drenagem e isolamento da planta para transporte ou reboque_

**P:** Após a parada da produção e antes do transporte ou reboque, qual sequência de ações define a condição de limpeza da unidade, e qual medida evita a recontaminação dos trechos já tratados?

**R:** Drenagem, ventilação, purga e lavagem; isolamento dos sistemas para impedir contaminação.

_Explicação:_ A condição de limpeza após a parada é composta por drenagem, ventilação, purga e lavagem. Em seguida, os sistemas são isolados para evitar que trechos já limpos sejam novamente contaminados.

**media · REPROVADA: autonomia**  
_Nota(s): Limpeza, isolamento e controle de perda de contenção antes de corte, desmontagem e intervenção_

**P:** Antes do corte de risers em um caso de resposta à emergência, foi registrado TOG abaixo de 15 mg/L no fluido remanescente das linhas. Qual a interpretação operacional mais adequada desse registro para a decisão de corte?

**R:** Indica fluido remanescente com baixo teor de óleo antes do corte, como critério contextual complementar de liberação, não como limite universal.

_Explicação:_ Nesse caso, o registro de TOG abaixo de 15 mg/L caracterizou a condição do fluido nas linhas antes da operação, reduzindo o potencial de descarga oleosa. Porém, esse valor foi observado em um contexto específico e não substitui a verificação de drenagem, limpeza, isolamento e ausência de resíduo perigoso.

**dificil_A · REPROVADA: sem_generalizacao · corrigida**  
_Nota(s): Desconexão, pull out e retirada de risers, umbilicais e sistemas associados em unidades flutuantes_

**P:** Durante o descomissionamento de uma FPSO, a equipe pretende fazer pull out dos risers e deixá-los temporariamente no leito marinho para liberar a unidade antes da campanha posterior de recolhimento definitivo, enquanto a unidade sai da locação por reboque. Qual combinação de condição e de interface operacional torna essa estratégia admissível?

**R:** Autorização formal em caráter excepcional ou de urgência, com coordenação entre a desconexão das linhas submarinas e a liberação do sistema de ancoragem.

_Explicação:_ O material sustenta que o pull out com abandono temporário no leito marinho pode liberar a unidade antes do recolhimento definitivo quando houver autorização formal, em caráter excepcional ou de urgência. Como a retirada da unidade flutuante ocorre por reboque, a preparação segura exige coordenar a liberação das conexões submarinas com a desconexão do sistema de ancoragem.

**media · APROVADA**  
_Nota(s): Revalidação de premissas de projeto, histórico de carregamento e extensão de vida de FPSO/FSO_

**P:** Em uma estratégia madura de extensão de vida de um FPSO/FSO, quais dados de monitoramento em tempo real alimentam a estimativa de cargas de fadiga e as avaliações preditivas de vida remanescente?

**R:** Dados meteocean, movimentos da embarcação e monitoramento/resposta estrutural do casco em tempo real.

_Explicação:_ A estimativa preditiva de fadiga depende da combinação entre ambiente atuante, resposta dinâmica da unidade e medições físicas da estrutura. Esse conjunto permite calcular cargas de fadiga em tempo real e sustentar avaliações preditivas de vida remanescente.

_Às cegas (equivalente):_ Alimentam: metocean/onda/vento/corrente; movimentos do casco (MRU: heave/pitch/roll) e acelerações; tensões/deformações (strain gauges) e vibração; pressões/níveis/densidades de tanques (sloshing); cargas/offset/tração de amarras e risers; dados operacionais de calado/trim. Falta definir áreas/sistemas críticos monitorados.

**facil · APROVADA**  
_Nota(s): Disponibilidade de sobressalentes e estratégia de estoque para continuidade operacional_

**P:** Qual é o mecanismo pelo qual reduzir o estoque de sobressalentes de equipamentos críticos pode elevar o custo total da operação?

**R:** A falta da peça prolonga a indisponibilidade do equipamento, e a perda de produção pode superar a economia obtida com a redução do estoque.

_Explicação:_ Em equipamentos críticos, a ruptura de estoque faz o reparo depender do fornecimento do item, aumentando o tempo fora de serviço. Em ativos remotos ou com componentes específicos, esse atraso amplia a perda de produção e pode custar mais do que a redução do inventário economizou.

_Às cegas (equivalente):_ Reduzir sobressalentes críticos aumenta tempo de reparo (MTTR) por falta imediata de peças, elevando downtime, perdas de produção, custos de mobilização/urgência, fretes/expedites e risco de operar degradado, além de penalidades contratuais e maior exposição a falhas repetidas.

**dificil_B · APROVADA**  
_Nota(s): Decisão de fim de vida e extensão de vida útil da unidade; Sistema de gestão de integridade: dados, escopo, backlog e governança no ciclo de vida da unidade; Encerramento de pendências de integridade, inspeção, manutenção e governança operacional no fim de vida da unidade_

**P:** Uma FPSO em late life ainda tem campo economicamente atrativo para alguns anos, e a gerência propõe life extension. Porém, o histórico de reparos e modificações é fragmentado, não foi estabelecido baseline confiável da condição real, o backlog de inspeções críticas não é visível de forma consolidada, há anomalias antigas abertas e desenhos/listas de equipamentos relevantes estão desatualizados. Qual condição torna essa extensão tecnicamente indefensável neste momento?

**R:** A incapacidade de demonstrar a condição conhecida do ativo por falta de baseline confiável e de avaliação formal com backlog, anomalias e documentação rastreáveis.

_Explicação:_ A extensão de vida exige avaliação formal sustentada por baseline que represente a condição real da unidade e por histórico rastreável de reparos, anomalias e modificações. Quando backlog crítico, anomalias e documentação permanecem sem visibilidade consolidada e sem rastreabilidade confiável, o sistema deixa de representar o estado real do ativo e não há base técnica robusta para sustentar a continuidade segura além da vida de projeto.

_Às cegas (equivalente):_ A extensão é tecnicamente indefensável enquanto não se consegue demonstrar, com dados rastreáveis (as-built, histórico e inspeções), um baseline de integridade/fitness-for-service para itens críticos, com backlog e anomalias consolidados e tratados.

### Gestão do Desempenho Empresarial (KPI)

#### Gestão do Desempenho Empresarial (KPI)

**facil · REPROVADA: suporte**  
_Nota(s): KPIs de melhoria operacional para processo, logística offshore e perdas de produção_

**P:** Em uma área que já possui modelagem de processos e definição de indicadores, qual é o efeito da ausência de diagnóstico periódico sobre a melhoria dos processos?

**R:** Sem diagnóstico periódico, os indicadores não direcionam melhorias incrementais nos processos.

_Explicação:_ Ter modelagem de processos e indicadores, por si só, não basta para orientar a melhoria contínua. Sem diagnóstico periódico, a gestão perde a capacidade de usar os indicadores para identificar desvios recorrentes e direcionar melhorias incrementais.

**media · APROVADA**  
_Nota(s): KPIs de segurança de processo, integridade de ativos e barreiras críticas para decisão gerencial em FPSOs_

**P:** Em um FPSO, a gerência recebe como principal KPI apenas o número de inspeções concluídas no período e quer usá-lo para decidir continuidade operacional e priorização de manutenção. Por que esse indicador, isoladamente, é insuficiente?

**R:** Porque mede esforço executado, não se as barreiras e SCEs estão com condição, disponibilidade e confiabilidade adequadas nem se houve redução real do risco.

_Explicação:_ Indicadores de input, como quantidade de inspeções, mostram volume de atividade, mas não demonstram o impacto do trabalho sobre a integridade dos elementos críticos à segurança. Para decidir continuidade operacional e priorizar manutenção, a gestão precisa de evidência sobre condição, degradação, disponibilidade e efeito nas barreiras, idealmente complementada por resultados qualitativos e métricas de risco.

_Às cegas (equivalente):_ Porque mede volume, não qualidade nem risco: pode haver inspeções superficiais, atrasos em itens críticos e falhas não mitigadas. Não reflete condição/barreiras (SCE), criticidade, achados, backlog, integridade e MTBF. Falta ponderar por criticidade e resultados/fechamento.

**dificil_A · APROVADA**  
_Nota(s): OEE como KPI composto para localizar perdas e priorizar ativos com pior utilização_

**P:** Em uma unidade, três recursos tiveram os seguintes resultados: Separador A com OEE 0,81, disponibilidade 0,90, performance 0,90 e qualidade 1,00; Compressor B com OEE 0,64, disponibilidade 0,80, performance 0,80 e qualidade 1,00; Bomba C com OEE 0,72, disponibilidade 0,95, performance 0,80 e qualidade 0,95. Qual deve ser a prioridade inicial de diagnóstico?

**R:** Priorizar o Compressor B e analisar primeiro disponibilidade ou performance, que são os menores componentes nesse ativo.

_Explicação:_ A priorização deve recair sobre o recurso de menor OEE na unidade, porque ele representa a pior eficiência global entre os comparados. Depois disso, o diagnóstico deve começar pelo componente mais baixo desse recurso; no Compressor B, disponibilidade e performance estão empatadas como menores valores.

_Às cegas (equivalente):_ Prioridade inicial: Compressor B, por ter o menor OEE (0,64) e perdas relevantes em disponibilidade (0,80) e performance (0,80). Focar diagnóstico em falhas/paradas e restrições de capacidade/controle; qualidade não é o limitante (1,00).

**media · REPROVADA: codigo:depende_do_material · corrigida**  
_Nota(s): Alinhamento dos indicadores à estratégia e à criação de valor_

**P:** Em uma empresa que ampliou a capacidade da planta e passou a produzir novos itens, qual combinação de mudanças no negócio e perspectivas do sistema de desempenho concentra o efeito mais forte que indica revisar o mix de KPIs?

**R:** Ampliação de capacidade e introdução de novos produtos, com maior impacto em processos internos e clientes.

_Explicação:_ Segundo o material, o aumento de capacidade da planta e a introdução de novos produtos impactam os indicadores de todas as perspectivas, especialmente processos internos e clientes. Esse efeito pode tornar insuficiente o mix anterior de KPIs e justificar sua revisão.

**facil · APROVADA**  
_Nota(s): Sistema de KPIs para priorização de melhorias e criação de valor_

**P:** Em ambientes empresariais com mudanças frequentes, qual é a dupla função de um sistema de KPIs bem estruturado?

**R:** Apoiar a gestão estratégica e tornar compreensível o processo de criação de valor.

_Explicação:_ Nessas condições, o sistema de indicadores não serve apenas para exibir números. Ele apoia decisões de gestão e ajuda a entender como o desempenho do negócio é gerado.

_Às cegas (incorreta):_ Um sistema de KPIs bem estruturado tem dupla função: (1) monitorar desempenho e aderência a metas/segurança em tempo real; (2) orientar decisões e priorização de recursos, alinhando equipes e mantendo controle durante mudanças frequentes.

**dificil_B · APROVADA**  
_Nota(s): KPIs de integridade, manutenção e confiabilidade como tradutores de indisponibilidade, perdas de produção e custo; Trade-offs econômicos entre CAPEX, OPEX, risco operacional e perdas futuras de produção; Estratégias de manutenção para elevar confiabilidade e disponibilidade dos ativos_

**P:** Em um FPSO sob pressão de caixa por preço baixo do petróleo, a gerência quer cortar o OPEX do semestre adiando intervenções preventivas em equipamentos críticos. Ao mesmo tempo, o backlog de manutenção está alto e o trending indica ameaça futura com queda de vida residual. Esse adiamento é tecnicamente adequado como decisão de desempenho empresarial?

**R:** Não; a prioridade é revisar a priorização e manter ou reforçar a manutenção proativa baseada na condição.

_Explicação:_ Backlog alto sinaliza confiabilidade abaixo do requerido, e trending com ameaça futura e vida residual em queda indica necessidade de ação mitigatória oportuna, não de empurrar a intervenção. Adiar para reduzir OPEX imediato aumenta a exposição a falhas, indisponibilidade e reparos não programados, o que tende a piorar o resultado econômico total mesmo em cenário de preço baixo.

_Às cegas (parcial):_ Não. Adiar preventiva em equipamentos críticos, com backlog alto e trending de perda de vida residual, eleva risco HSE/produção e pode aumentar OPEX total (falhas, paradas, corretivas). Falta definir criticidade/limites operacionais e requisitos regulatórios/RBI.

**dificil_A · APROVADA · corrigida**  
_Nota(s): KPIs técnicos para gestão de metas operacionais e disponibilidade_

**P:** Em um ativo de produção, o OEE caiu nas últimas medições. A gerência quer distribuir recursos de melhoria simultaneamente entre manutenção, ritmo operacional e retrabalho. Pelo critério de uso do OEE, qual deve ser a prioridade inicial?

**R:** Priorizar o componente do OEE com perda dominante.

_Explicação:_ Como o OEE é o produto de disponibilidade, performance e qualidade, sua queda pode resultar de mecanismos distintos de perda. O uso correto do indicador para direcionar melhorias é identificar qual componente mais degrada o resultado e atacar esse componente primeiro, em vez de dispersar recursos.

_Às cegas (equivalente):_ A prioridade inicial é atacar a maior perda que mais derruba o OEE: o pilar com pior resultado (Disponibilidade/manutenção, Performance/ritmo ou Qualidade/retrabalho). Sem a decomposição do OEE por pilar e perdas, não dá para definir qual área lidera.

**facil · APROVADA**  
_Nota(s): Retroalimentação por falhas, risco e integridade para melhoria sustentada ao longo da vida útil da unidade_

**P:** Qual é o efeito da Análise de Falhas, quando identifica mecanismos e causas, sobre a reincidência e sobre o enfoque da manutenção e da inspeção?

**R:** Inibe reincidências e desloca a manutenção e a inspeção do modo reativo para o preventivo.

_Explicação:_ Quando a análise identifica mecanismo e causa da falha, ela permite corrigir a origem do problema e reduzir repetição. Com isso, manutenção e inspeção deixam de atuar principalmente após a falha e passam a prevenir novas ocorrências.

_Às cegas (equivalente):_ Ao identificar mecanismos e causas, reduz a reincidência ao eliminar a causa-raiz e direciona manutenção/inspeção de reativas/tempo para baseadas em condição e risco, focando modos críticos e pontos vulneráveis, ajustando planos, frequências, critérios e ações corretivas.

**media · APROVADA · corrigida**  
_Nota(s): KPI como elemento do ciclo de monitoramento, verificação e melhoria contínua na governança de FPSOs_

**P:** No sistema de gestão de um FPSO, em que etapa do PDCA os resultados de KPI, tratados junto com achados de auditoria e análise crítica gerencial, servem de base para ação corretiva ou aperfeiçoamento?

**R:** Na etapa Check, de verificação.

_Explicação:_ Pelo encadeamento de melhoria contínua, o KPI entra como dado de desempenho para a etapa de verificação do sistema de gestão. Nessa etapa, seus resultados são considerados com auditorias e análise crítica da administração para fundamentar ações corretivas ou oportunidades de melhoria.

_Às cegas (incorreta):_ Na etapa ACT (Agir/Melhorar): resultados de KPI, achados de auditoria e análise crítica gerencial fundamentam ações corretivas e de melhoria contínua no sistema de gestão.

**facil · APROVADA**  
_Nota(s): Eficiência e disponibilidade de subsistemas como restrições diretas à produção e à qualidade dos fluidos_

**P:** Qual mecanismo faz a indisponibilidade do tratamento de gás interromper a produção de óleo quando há limite de flaring?

**R:** Sem tratamento e destinação adequados do gás associado, a produção de óleo precisa ser interrompida para não exceder o limite de flaring.

_Explicação:_ Quando o sistema de tratamento de gás fica indisponível, o gás associado deixa de ter rota compatível com a restrição operacional. Nessa condição, a produção de óleo deve ser interrompida para evitar atingir o limite de queima.

_Às cegas (equivalente):_ A perda do tratamento reduz a capacidade de compressão/desidratação/remoção de CO₂; o gás associado não atende exportação/reinjeção e vai ao flare. Ao atingir o limite de flaring, o ESD/PSD comanda redução/fechamento dos poços (choke/SDV), cortando a produção de óleo.

**media · APROVADA**  
_Nota(s): Arquitetura de KPIs para desdobrar estratégia, planejamento e controle_

**P:** Em um sistema de medição de desempenho com múltiplas perspectivas, a empresa amplia a capacidade produtiva e altera o mix de produtos. Quais perspectivas tendem a ser especialmente mais impactadas por essas mudanças?

**R:** As perspectivas de processos internos e de clientes.

_Explicação:_ Mudanças de capacidade e de mix de produção afetam o sistema de indicadores como um todo, mas o efeito é particularmente forte nas perspectivas ligadas ao desempenho dos processos e à resposta percebida pelos clientes.

_Às cegas (incorreta):_ Principalmente Processos Internos (capacidade, gargalos, eficiência, qualidade) e Financeira (CAPEX/OPEX, custo unitário, margens). Também Clientes (nível de serviço, prazos, especificações) e, em menor grau, Aprendizado & Crescimento (competências/treinamentos).

**dificil_A · APROVADA**  
_Nota(s): Qualidade dos dados e trending como base de KPIs preditivos de confiabilidade dos ativos_

**P:** Um KPI de confiabilidade de uma bomba manteve tendência contínua e aparentemente estável, mas o campo relata troca recente do componente monitorado e o desempenho observado não combina com o histórico. Qual indício de rastreabilidade explica melhor essa incoerência?

**R:** O componente novo recebeu o mesmo tag do anterior, misturando os históricos e criando falsa continuidade da tendência.

_Explicação:_ Quando a identificação é feita pela localização funcional e não pelo item físico específico, a troca de componente pode manter o mesmo tag no sistema. Isso funde a história do equipamento antigo com a do novo, distorce o trending e faz o KPI parecer coerente no painel mesmo sem representar o mesmo fenômeno físico ao longo do tempo.

_Às cegas (equivalente):_ Indício: falha de rastreabilidade/CMMS—o tag/asset ID ou número de série do componente trocado não foi atualizado (ou o KPI continua vinculado ao equipamento antigo), mantendo o histórico. Falta confirmar o vínculo KPI↔tag/serial após a troca.

### Logística, Suprimentos e Movimentação de Cargas

#### Logística e Suprimento Offshore

**facil · APROVADA**  
_Nota(s): Logística de contingência e resposta a emergências offshore_

**P:** No planejamento da logística de contingência offshore, quais elementos precisam estar explicitados para ligar cada cenário acidental aos meios de resposta?

**R:** Fontes e evolução do evento, métodos de controle, dados organizados para resposta rápida e os recursos disponíveis para cada cenário.

_Explicação:_ A vinculação entre cenário e resposta exige que o planejamento descreva como o evento pode surgir e evoluir, quais métodos de controle serão usados e quais dados sustentam a resposta rápida. Além disso, os recursos precisam estar associados a cada cenário; sem isso, a cobertura da resposta fica incompleta.

_Às cegas (equivalente):_ Para cada cenário: tipificação e premissas (volume/taxa, duração, meteoceanografia), gatilhos/níveis de escalonamento, recursos requeridos e disponibilidade (embarcações, barreiras, dispersantes, recolhimento, EPI), tempos de mobilização/rotas, responsabilidades/contatos, comunicação e interface com autoridades, pontos de reunião/estocagem.

**media · APROVADA**  
_Nota(s): Configuração e integridade do sistema de transferência por mangotes em operações offshore_

**P:** No dimensionamento de um mangote de offloading para um FPSO, qual critério deve relacionar o diâmetro da linha com a vazão de projeto para manter a operação dentro do envelope aceitável do fabricante?

**R:** O diâmetro deve ser compatível com a vazão de projeto para não exceder a velocidade limite de fluido definida pelo fabricante.

_Explicação:_ O critério de dimensionamento não é apenas hidráulico por capacidade de vazão; ele deve garantir que a velocidade interna do fluido permaneça dentro do limite especificado pelo fabricante do mangote. Se esse limite for ultrapassado, a operação sai da condição prevista de serviço do componente.

_Às cegas (equivalente):_ Usar o critério de velocidade/queda de pressão do fabricante: dimensionar o diâmetro para que, na vazão de projeto, a velocidade no mangote (e ΔP associada) fique dentro dos limites do datasheet/OCIMF (Q = v·A). Falta o limite de v/ΔP do fabricante.

**dificil_A · REPROVADA: codigo:depende_do_material · corrigida**  
_Nota(s): Critérios de seleção da classe de ROV e do sistema de lançamento/recuperação em operações profundas_

**P:** Segundo a referência apresentada, na mobilização de um RSV para duas campanhas de ROV, uma a 1500 m e outra a 3200 m, qual combinação de classe de ROV e de requisitos de alimentação, transmissão e lançamento/recuperação é compatível com cada profundidade?

**R:** Para 1500 m: MSROV, média tensão AC ou DC, cobre ou fibra, com TMS; para 3200 m: WCROV, alta tensão AC, fibra, com A-frame hidráulico.

_Explicação:_ Segundo a referência, a profundidade funciona como filtro inicial da classe de ROV e do arranjo de lançamento/recuperação. Acima de 1000 m, a associação indicada é MSROV com média tensão, cobre ou fibra e TMS; acima de 3000 m, é WCROV com alta tensão AC, fibra e A-frame hidráulico.

**media · REPROVADA: suporte**  
_Nota(s): Manutenção simultânea com operação em SIMOPS: MOC, isolamento, salvaguardas e restauração de barreiras_

**P:** Durante a preparação para retorno à operação, uma mudança de projeto removeu um intertravamento de baixa pressão que atuava como salvaguarda, mas a análise de riscos do processo permaneceu na configuração anterior. Qual providência é necessária antes de operar nessa nova condição?

**R:** Reavaliar os riscos da nova configuração e atualizar o HAZOP antes do retorno à operação.

_Explicação:_ A remoção de uma salvaguarda altera a relação entre causas iniciadoras, barreiras e consequências, portanto a condição de risco deixa de ser a mesma da análise anterior. Operar sem atualizar o HAZOP mantém uma incoerência entre projeto modificado e análise de risco, o que pode contribuir para vazamentos e outros desvios críticos.

**facil · APROVADA**  
_Nota(s): Envelopes operacionais e barreiras automáticas no offloading tandem para prevenir perda de contenção_

**P:** Quais variáveis operacionais definem os estados de alerta no offloading tandem?

**R:** Distância relativa entre o navio aliviador e o FPSO/TO e a tração ou tensão no cabo hawser.

_Explicação:_ Os estados de alerta da operação são definidos pela combinação entre posição relativa e esforço no sistema de amarração. Essa combinação determina a escalada das ações, de preparação para parar até isolamento da linha e desconexão.

_Às cegas (incorreta):_ Estados de alerta no offloading tandem são definidos por: velocidade/direção do vento, altura/periodo/direção de ondas, correnteza, aproamento/heading e offset (distância/ângulo) navio–FPSO, velocidade de aproximação, tensão/ângulo do hawser, carga no mangote, taxa de transferência e limites de ESD/ERP.

**dificil_B · APROVADA · corrigida**  
_Nota(s): Programação e roteirização do suprimento offshore com PSVs e embarcações de apoio; Restrições operacionais e capacidades da embarcação que condicionam a programação offshore; Restrições logísticas e condicionantes operacionais para movimentação de cargas offshore_

**P:** Um PSV foi programado dentro do limite de três dias e com convés compatível com a carga. Antes da saída, conclui-se que a embarcação não consegue se posicionar com segurança junto à unidade. Já a unidade recebedora informa um desvio operacional que muda a sequência prevista de descarga. Que dois fatores passam a impedir a execução do plano original?

**R:** Inadequação da embarcação para a aproximação à unidade; necessidade de revisar e simular a nova descarga no programa de estabilidade antes de executar.

_Explicação:_ Pela programação offshore, não basta o PSV ter convés e duração de viagem compatíveis: ele também precisa ter capacidade de manobra para operar próximo à unidade. Se surgir um desvio operacional na instalação que altere a sequência de descarga, o plano original deixa de valer até que as exigências sejam revistas e simuladas no programa de estabilidade.

_Às cegas (parcial):_ (1) Falta de capacidade de posicionamento/DP e manutenção de estação do PSV para operar com segurança junto à unidade. (2) Mudança na janela/ordem de descarga por desvio operacional da unidade, tornando o sequenciamento/janela logística original inválido.

**media · REPROVADA: codigo:depende_do_material · corrigida**  
_Nota(s): Expedição, consolidação, transporte e rastreamento de cargas para unidades offshore_

**P:** Em um terminal offshore, foram ampliadas embarcações e informatização, mas o desempenho logístico não melhorou. Que condição torna esses investimentos isolados insuficientes?

**R:** A permanência de restrições nos demais modais e na infraestrutura de escoamento, sem interação harmônica entre os elos.

_Explicação:_ Segundo o material, o desempenho do terminal depende da integração entre diferentes modais e da infraestrutura de escoamento. Por isso, investir apenas em embarcações, equipamentos ou informatização não basta quando os outros elos continuam limitantes.

**dificil_A · APROVADA · corrigida**  
_Nota(s): Conteinerização e perfil das cargas no suprimento offshore_

**P:** Na programação de uma embarcação de apoio, parte dos suprimentos foi consolidada em contêineres antes do embarque. Entre a base e a instalação offshore, como essa carga deve ser classificada operacionalmente?

**R:** Como carga de convés; a conteinerização é apenas a consolidação física de produtos acabados.

_Explicação:_ Pelos fatos dados, a conteinerização prepara o fluxo de transporte ao consolidar produtos acabados em contêineres até a descarga final. No suprimento offshore por embarcação de apoio, cargas em contêineres transportadas no convés integram o grupo de deck cargo, junto com tubos e equipamentos.

_Às cegas (incorreta):_ Deve ser classificada operacionalmente como carga conteinerizada (unitizada). Falta confirmar se os contêineres são de carga geral/CCU ou de classe IMO (perigosa), pois isso altera a segregação, rotulagem e manuseio durante o transporte.

#### Movimentação de Cargas

**facil · REPROVADA: suporte**  
_Nota(s): Inspeção pré-uso e retirada de serviço de guindastes, acessórios e equipamentos de içamento_

**P:** Quais defeitos observáveis na inspeção pré-uso exigem rejeição imediata de uma linga de cabo de aço ou de um cabo de guincho no tambor?

**R:** Arames rompidos, amassamento ou kinking severo, e enrolamento no tambor com empilhamento ou kinking severo.

_Explicação:_ Na inspeção pré-uso, esses sinais já indicam degradação mecânica ou enrolamento inadequado capaz de comprometer o caminho de carga e o comportamento do içamento. Por isso, a linga ou o cabo não devem seguir para uso normal.

**media · REPROVADA: resposta_unica, tipo_ok, resposta_unica_cega · corrigida**  
_Nota(s): Controle de interação da carga com estruturas, obstáculos e pontos de enrosco_

**P:** Segundo a recomendação para içamentos próximos a equipamentos e estruturas da instalação, que medida específica deve ser adotada nos pontos potenciais de contato ou enrosco?

**R:** Identificar previamente os pontos potenciais de contato ou enrosco e posicionar spotters adicionais nesses pontos críticos.

_Explicação:_ A fonte recomenda, para içamentos próximos a equipamentos e estruturas, reconhecer antes do movimento os pontos onde a carga pode tocar ou enroscar e aplicar mitigação apropriada, incluindo spotters adicionais nesses locais.

_Às cegas (alternativa_valida):_ Adotar “tag lines” (cabos-guia) para controlar a orientação e o balanço da carga durante o deslocamento, mantendo afastamento de estruturas e evitando contato/enrosco.

**dificil_A · APROVADA · corrigida**  
_Nota(s): Segurança operacional na transferência de cargas entre embarcações_

**P:** Durante o backloading para um supply vessel, a carga toca aparentemente o convés e um trabalhador inicia o desengate do stinger. Uma ondulação súbita desloca a carga nesse momento, e ela desce novamente logo depois. Qual é o mecanismo de risco mais provável nessa situação?

**R:** O movimento relativo provocado pelo swell reativa o esforço no stinger, permitindo que a carga volte a erguer levemente e depois caia sobre o convés.

_Explicação:_ O pouso aparente no convés não garante que a carga esteja estabilizada. Com o movimento relativo entre embarcação, carga e arranjo de içamento, o swell pode fazer o stinger voltar a assumir esforço por instantes, retirando apoio parcial do deck e levando a novo movimento descendente da carga.

_Às cegas (parcial):_ Mecanismo mais provável: carga suspensa ainda energizada por heave/recuperação do peso, causando movimento inesperado e possível re-suspensão durante o desengate, gerando risco de esmagamento/impacto/arraste do trabalhador (zona de beliscamento) e falha de engate do stinger.

**media · REPROVADA: sem_pista · corrigida**  
_Nota(s): Comunicação, supervisão e disciplina de execução em lifts complexos e críticos_

**P:** Em um lift crítico, qual condição caracteriza perda de uma barreira essencial de controle operacional ligada à supervisão e à disponibilidade do plano no campo?

**R:** Prosseguimento do lift sem o supervisor responsável e sem cópia física do lift plan na frente de trabalho.

_Explicação:_ Pela nota, em lift crítico a supervisão compatível com a criticidade e a presença do lift plan na frente de trabalho são barreiras essenciais. Quando a operação continua sem essas duas condições, há ruptura do controle operacional.

**facil · APROVADA**  
_Nota(s): Prevenção de queda de objetos e proteção de estruturas/áreas críticas em movimentação de cargas offshore_

**P:** Quais áreas devem ser projetadas contra queda acidental de objetos em plataformas com facilidades de perfuração?

**R:** As áreas de pipe-rack e as cabeças de poço.

_Explicação:_ Essas áreas são explicitamente identificadas como expostas a um tipo de acidente frequente em estruturas offshore e, por isso, devem ser protegidas contra queda acidental de objetos.

_Às cegas (incorreta):_ Áreas abaixo/adjacentes à torre (derrick), subestrutura, monkey board, piso de sonda, BOP/wellhead, guinchos e rotas de içamento; áreas ocupadas (CCR, módulos elétricos, alojamento), helideck, escape/muster e passagens. Falta critério do padrão aplicável (DNV/ISO/API) para detalhar níveis.

**dificil_B · APROVADA · corrigida**  
_Nota(s): Integridade e limitações de FIBCs no içamento offshore; Distribuição de esforços entre alças e técnica de içamento em múltiplos pontos para FIBC; Inspeção das alças do FIBC e retirada de serviço antes do içamento_

**P:** Um FIBC está com o peso total dentro do limite nominal. Na inspeção prévia, há degradação visível em uma alça, e o arranjo de pega previsto não assegura distribuição igual de esforços entre as alças. O içamento pode ser liberado?

**R:** Não. Retire o FIBC de serviço antes do içamento.

_Explicação:_ Degradação visível em alça exige retirada de serviço antes do içamento. Além disso, um arranjo que não distribui igualmente os esforços aumenta o risco de sobrecarga localizada, de modo que o peso nominal, isoladamente, não autoriza a liberação.

_Às cegas (equivalente):_ Não. Qualquer degradação visível em alça e arranjo que não garanta carga igualmente distribuída entre alças torna o içamento inseguro, mesmo dentro do SWL. Falta definir se há método/acessório aprovado (spreader/4 pontos) para equalizar esforços e substituição do FIBC.

**media · APROVADA · corrigida**  
_Nota(s): Integridade mecânica e inspeção como condição para a validade da capacidade nominal de guindastes e sistemas de içamento_

**P:** Em um içamento, supondo que o load chart aplicável esteja correto e que as condições operacionais já estejam dentro dos limites previstos, que condição do próprio equipamento precisa estar confirmada para que esse chart seja válido na operação?

**R:** A inspeção deve confirmar integridade mecânica e funcional aceitável do equipamento.

_Explicação:_ O chart correto define apenas o limite teórico para a configuração prevista. Para que ele represente a capacidade real disponível, a inspeção precisa confirmar que componentes e funções críticas do equipamento permanecem em condição aceitável, como freios, cabo, guincho e conexões estruturais.

_Às cegas (alternativa_valida):_ Confirmar que as condições reais de operação estão dentro das premissas do load chart (principalmente adernamento/trim do FPSO/FSO e movimento/sea state/vento). Falta confirmar os limites admissíveis dessas condições conforme o próprio chart/manual.

_Às cegas (equivalente):_ Confirmar que o guindaste está certificado/inspecionado e configurado exatamente conforme o load chart (mesma configuração/reeving, contrapeso, lança/jib e dispositivos limitadores operacionais). Falta garantir que não houve alterações/danos que mudem a capacidade real.

**dificil_A · APROVADA**  
_Nota(s): Delimitação da área de movimentação e das zonas de exposição à queda de carga_

**P:** Antes de um içamento em plataforma, a equipe precisa marcar a zona de exclusão no convés. Se o critério for o cenário acidental de queda da carga, qual envoltória espacial deve ser usada para delimitar essa área?

**R:** A envoltória do raio de ação do guindaste ampliada pela dispersão cônica da queda a partir de qualquer ponto alcançável.

_Explicação:_ A zona de exclusão não deve considerar só a trajetória nominal da carga. No cenário acidental, deve-se assumir queda a partir de qualquer ponto alcançável pelo guindaste, com dispersão geométrica em cone, o que amplia a área potencialmente atingida.

_Às cegas (incorreta):_ Use a envoltória de “queda livre”: um cone/sector com ápice no ponto de suspensão (gancho/manilha) e base no convés, cobrindo toda a projeção vertical da carga e possíveis desvios (balanço/pendular). Falta definir a altura máxima do içamento para dimensionar o raio.

### Manutenção, Inspeção e Integridade de Ativos

#### Apoio Técnico e Manutenção em um FPSO (Laboratório, Oficinas, Pipe Shop)

**facil · REPROVADA: codigo:depende_do_material, resposta_unica_cega · corrigida**  
_Nota(s): Testes funcionais sob carga e verificação de proteções em geradores e unidades elétricas de FPSO/FSO_

**P:** Segundo o critério de aceitação para geradores de FPSO/FSO, inclusive o de emergência, o que o teste sob carga deve demonstrar e, quando houver operação em paralelo, quais verificações específicas devem ser evidenciadas?

**R:** Deve demonstrar operação sob carga; em paralelo, deve evidenciar partilha de carga satisfatória, operação dos disjuntores e desligamento por potência reversa.

_Explicação:_ A pergunta foi delimitada ao critério de aceitação descrito na referência. Pelo material, geradores, inclusive o de emergência, devem ser operados sob carga. Se operarem em paralelo, o aceite deve incluir evidência de partilha de carga satisfatória, operação dos disjuntores e demonstração do desligamento por potência reversa.

_Às cegas (alternativa_valida):_ Que o gerador sustenta tensão e frequência dentro de limites com carga real, aceitando degraus, sem instabilidade, sobreaquecimento ou atuação indevida de proteções; valida regulador/AVR, governador, capacidade/kW‑kVAr e seletividade. Falta definir o perfil de carga e critérios de aceitação.

**media · APROVADA**  
_Nota(s): Políticas de ressuprimento e parametrização de níveis de estoque para sobressalentes_

**P:** Na gestão de sobressalentes de um FPSO, como se distinguem reposição contínua, ponto de ressuprimento e reposição periódica quanto ao disparo do pedido, à quantidade reposta e à forma de controle do estoque?

**R:** Reposição contínua: ressuprimento automático contínuo; ponto de ressuprimento: pedido ao cair abaixo do gatilho, em lote econômico; reposição periódica: revisão em datas fixas e pedido igual a MAX menos saldo.

_Explicação:_ Na reposição contínua, o sistema trata o ressuprimento como processo automático. No ponto de ressuprimento, o pedido é disparado quando o estoque cai abaixo de um nível definido, normalmente em lote econômico. Na reposição periódica, a decisão ocorre apenas nas revisões em intervalos fixos, e a quantidade pedida recompõe o estoque até o nível máximo.

_Às cegas (parcial):_ Reposição contínua: pedido dispara a cada saída; repõe quantidade consumida; controle por registro/consumo (2-bin/Kanban). Ponto de ressuprimento: dispara ao atingir estoque mínimo; repõe até nível máximo/EOQ; controle por min–max. Periódica: dispara em datas fixas; repõe até nível alvo; controle por revisão periódica.

**dificil_A · APROVADA**  
_Nota(s): Estruturação de sobressalentes e definição de níveis de estoque no ERP_

**P:** Em um FPSO, um item já existe no ERP. Em alguns casos, a equipe não consegue sequer identificar com segurança qual número de material deve requisitar para um equipamento específico; em outros, o número de material está correto, mas o estoque zera repetidamente antes da reposição do fornecedor. Qual diagnóstico distingue essas duas origens da falta de material?

**R:** Indefinição do item por equipamento indica falha de especificação ligada à tag/BOM; ruptura com item já corretamente cadastrado indica níveis mínimo/máximo incompatíveis com lead time e demanda.

_Explicação:_ Quando tags, BOM e Spare Part List não estão robustamente estruturadas, aumentam os erros de especificação e a dificuldade de requisitar o material correto. Se o item já está tecnicamente correto no cadastro, mas falta durante o ciclo de reposição, a causa passa a ser a parametrização de estoque, que deve cobrir tempo de entrega e demanda sem excesso de inventário.

_Às cegas (equivalente):_ Se a falha é de identificação: divergência entre BOM/equipamento/tag e cadastro (descrição, fabricante, part number, aplicação), gerando requisições erradas/duplicadas. Se a falha é de reposição: material correto, porém parâmetros MRP/lead time/estoque de segurança e consumo x prazo (OTIF) insuficientes. Falta confirmar se há BOM/padronização por tag atualizada.

#### Cibersegurança e Integridade de Sistemas Digitais

**facil · REPROVADA: suporte, objetividade, codigo:pergunta_composta**  
_Nota(s): Controle de acesso remoto e de pontos de entrada para funções essenciais_

**P:** Que tipo de dispositivo pode acessar redes e sistemas que suportam função essencial, e qual exigência adicional se aplica ao acesso privilegiado?

**R:** Somente dispositivos corporativamente próprios e gerenciados; acesso privilegiado exige dispositivo corporativamente gerenciado dedicado à administração.

_Explicação:_ Para redes e sistemas de função essencial, o critério de base é restringir o acesso remoto a ativos sob governança corporativa. Quando a atividade é privilegiada, o rigor aumenta: a origem deve ser uma estação gerenciada e dedicada à administração, para reduzir exposição de sessões sensíveis.

**media · APROVADA**  
_Nota(s): Historização e cópias operacionais distribuídas como suporte à recuperação de sistemas digitais_

**P:** Em uma recuperação pós-falha, além das variáveis de campo historizadas, que aspecto adicional da reconstrução de estado é fornecido pelos dados de gerência do sistema de controle, de usuários e pelas variáveis de comportamento do processo?

**R:** O contexto de configuração e de uso em que o processo ocorreu.

_Explicação:_ As variáveis de campo mostram o que o processo fez, mas os dados de gerência do sistema de controle, de usuários e de comportamento do processo permitem reconstruir em que configuração e sob que uso isso aconteceu. Isso torna a reconstrução de estado mais robusta para diagnóstico e restauração.

_Às cegas (equivalente):_ Eles permitem reconstruir o “contexto operacional”: quem atuou (ações, permissões, logins), o que o sistema de controle fez (alarmes, eventos, mudanças de lógica/configuração) e como o processo reagiu dinamicamente. Falta definir qual plataforma/SCADA para detalhar itens.

**dificil_A · REPROVADA: suporte**  
_Nota(s): Arquitetura integrada de redes e acesso remoto em sistemas digitais de FPSO_

**P:** Uma plataforma já permite monitoramento e algumas operações a partir de terra com os mesmos recursos disponíveis a bordo. A equipe quer liberar mudança de lógica em CLPs sem deslocamento físico. Qual critério deve ser atendido para autorizar essa programação remota?

**R:** Liberar apenas com a barreira de rede operante e privilégios de acesso adequados; sem isso, a programação remota deve permanecer bloqueada.

_Explicação:_ O acesso remoto pode reproduzir em terra funções disponíveis a bordo, e a própria conectividade permite monitoramento e operação por usuários com software e privilégios. Por isso, ações de maior impacto, como reprogramar controladores, só devem ser liberadas quando houver barreira de rede efetiva e controle de privilégios compatível com o risco.

**media · APROVADA**  
_Nota(s): Atualização oportuna de defesas por assinatura e validação da efetividade da threat intelligence_

**P:** Uma unidade offshore recebe feeds de threat intelligence e os converte em regras, assinaturas e IoCs para monitoramento industrial. Qual critério deve ser usado para verificar se essa inteligência está trazendo valor real para a detecção?

**R:** Medir, por rastreamento de resultados, se ela aumentou a identificação de problemas de segurança.

_Explicação:_ O valor da threat intelligence não se comprova pela quantidade de feeds recebidos, mas pelo efeito operacional na capacidade de identificar problemas de segurança. Por isso, a verificação deve acompanhar resultados de detecção e confirmar se houve ganho efetivo nessa identificação.

_Às cegas (equivalente):_ Use o impacto na eficácia de detecção: aumento de verdadeiros positivos e redução de falsos positivos, medidos por taxa de detecção/alertas acionáveis e melhoria de MTTD/MTTR em casos confirmados. Falta definir baseline e período de comparação.

#### Inspeção e Integridade

**facil · APROVADA**  
_Nota(s): Monitoramento e planejamento de inspeção para corrosão e perda de espessura em dutos, tubulações e sistemas submarinos_

**P:** Qual é o efeito de empregar métodos e frequências de inspeção diferentes sobre a detecção e o dimensionamento de danos e sobre o risco de falha?

**R:** Eles têm capacidades diferentes de detectar e dimensionar danos, alterando de modo distinto o risco de falha.

_Explicação:_ Planos de inspeção não são equivalentes: a combinação de método e frequência muda a chance de encontrar descontinuidades e de estimar sua extensão. Por isso, cada plano produz um efeito próprio na avaliação do risco de falha.

_Às cegas (equivalente):_ Métodos e frequências diferentes mudam a POD e a precisão do dimensionamento: inspeções mais sensíveis e/ou mais frequentes detectam danos menores mais cedo, melhoram o sizing e reduzem o risco de falha; menos sensíveis/raras aumentam danos não detectados e o risco.

**media · APROVADA · corrigida**  
_Nota(s): RBI/IBR como base para priorização e otimização dinâmica dos planos de inspeção_

**P:** Na RBI, após novas inspeções e revisão dos registros do equipamento, qual relação de atualização do risco para o plano de inspeção deve ser identificada?

**R:** Mecanismos de dano e histórico operacional atualizam o risco e reordenam prioridades, frequência, métodos e escopo da inspeção.

_Explicação:_ Na RBI, a atualização do risco usa os mecanismos de dano atuantes e o histórico operacional do equipamento. Quando essa percepção de risco muda, o plano de inspeção é revisto, com possível reordenação de prioridades e ajuste de frequência, métodos e escopo.

_Às cegas (parcial):_ Identificar como as novas inspeções alteram PoF e/ou CoF (degradação/criticidade), atualizando a matriz/nível de risco e, consequentemente, escopo, método e intervalos do plano (reduzir/manter/aumentar frequência). Falta o critério de aceitação/limiar de risco aplicável.

#### Instrumentação, Controle e Automação

**facil · REPROVADA: suporte, sem_pista**  
_Nota(s): Critérios e limites para bypass temporário de dispositivos de segurança_

**P:** Qual mecanismo faz um único maintenance bypass em um transmissor de pressão desabilitar ao mesmo tempo as funções PSH e PSL?

**R:** Porque PSH e PSL usam o mesmo transmissor; ao bypassar esse ponto comum, a lógica retira ambas as proteções.

_Explicação:_ Quando duas funções de segurança compartilham o mesmo transmissor, o efeito do bypass depende da granularidade da lógica. Se o bypass atua sobre esse ponto comum, ele suprime simultaneamente as duas ações de proteção, não apenas a função que motivou a manobra.

**media · APROVADA**  
_Nota(s): Desempenho dinâmico de medição e controle sob ruído, variabilidade operacional e não linearidades_

**P:** Em uma planta offshore, o número de poços alinhados e as condições do processo mudam ao longo do tempo, mas os PIDs regulatórios permanecem com a mesma sintonia. Qual efeito isso tende a causar no desempenho da malha?

**R:** A sintonia fixa deixa de ser adequada entre as condições, e a malha passa a oscilar mais e a operar mais afastada do setpoint.

_Explicação:_ Quando o ponto de operação e a dinâmica da planta variam no tempo, um PID linear com a mesma sintonia não mantém desempenho equivalente em todas as condições. O resultado típico é degradação da malha, com maior faixa de oscilação das variáveis e operação mais distante do setpoint.

_Às cegas (equivalente):_ Tende a causar degradação da malha: variação de ganho/tempo morto/constantes do processo muda a dinâmica e a sintonia fixa fica inadequada, gerando maior oscilação, overshoot, erro estacionário e/ou resposta lenta (maior variabilidade e intervenções manuais).

**dificil_A · APROVADA · corrigida**  
_Nota(s): Diagnóstico estruturado em camadas no ambiente de automação_

**P:** Em um FPSO, PLC e supervisório já registram eventos de falha, e a revisão realizada não alterou a filosofia nem a racionalização de alarmes. O ganho veio da reorganização dos diagnósticos desses sistemas e de sua integração permanente aos processos internos da empresa, com base corporativa de conhecimento e melhoria contínua. Que mudança explica a priorização e o tratamento mais padronizados dos problemas?

**R:** A implantação de diagnóstico em camadas integrado ao macroprocesso DIA com base corporativa de conhecimento.

_Explicação:_ Pelos fatos do material, o ganho de eficácia não decorre de mais alarmes nem de sua racionalização, mas de estruturar os diagnósticos para automatizar entendimento, atendimento e tratamento dos problemas. Quando isso é integrado permanentemente aos processos internos pelo macroprocesso DIA, com base corporativa de conhecimento e melhoria contínua, o tratamento deixa de ser disperso e passa a ser padronizado.

_Às cegas (alternativa_valida):_ Implantação de gestão de alarmes com racionalização/filtragem e padronização (ISA‑18.2/EEMUA 191), incluindo prioridades, causas prováveis e ações/responsáveis no supervisório/CMMS. Melhora o encaminhamento e a resposta sem necessariamente aumentar a quantidade de alarmes.

_Às cegas (parcial):_ Mudança de gestão/processo: implantação de um programa corporativo integrado de gestão de falhas (FMS/RCA) com base de conhecimento, padronizando classificação/priorização e workflow de tratamento. Falta confirmar se houve formalização em CMMS/ERP (ordens de serviço/criticidade).

#### Manutenção e Plano de Manutenção

**facil · APROVADA**  
_Nota(s): Premissas da filosofia de manutenção: alinhamento ao negócio, criticidade e revisão ao longo do ciclo de vida_

**P:** Qual é a razão operacional para, em uma unidade offshore com poucos mantenedores a bordo, concentrar a manutenção nos equipamentos de maior criticidade?

**R:** Porque não é viável aplicar o mesmo esforço a todo o parque; os recursos devem ir para os ativos com maior impacto em produção, segurança e meio ambiente.

_Explicação:_ Com limitação de mão de obra a bordo, a filosofia de manutenção precisa otimizar o uso dos recursos disponíveis. Por isso, a priorização por criticidade direciona esforço aos equipamentos cuja falha traria consequências mais relevantes para produção, segurança da plataforma e meio ambiente.

_Às cegas (equivalente):_ Porque com equipe limitada o tempo, sobressalentes e janelas de parada são escassos; priorizar ativos críticos reduz o risco de perda de produção, falhas de segurança/ambientais e indisponibilidade do sistema, maximizando confiabilidade e continuidade operacional.

**media · REPROVADA: suporte, resposta_unica, sem_pista, tipo_ok, codigo:depende_do_material · corrigida**  
_Nota(s): Integração de informações e decisão sobre backlog e prioridades de manutenção_

**P:** Em uma instalação operando sob Operações Integradas, considerando os impactos da manutenção sobre obrigações da unidade, continuidade operacional dos equipamentos e despesas de manutenção, por que sua gestão recebe maior foco entre os processos-chave?

**R:** Porque é vital para cumprir requisitos legais, garantir a disponibilidade dos equipamentos e otimizar os custos de manutenção.

_Explicação:_ A nota técnica associa o maior foco dado à gestão da manutenção, nas Operações Integradas, aos seus efeitos diretos sobre conformidade legal, disponibilidade dos equipamentos e custos de manutenção. Ao explicitar esse recorte no enunciado, a resposta correta fica única.

**dificil_A · APROVADA**  
_Nota(s): Estruturação do cadastro de ativos e dos planos de manutenção no CMMS/SAP PM_

**P:** Em um FPSO, o CMMS está com cadastro, TAGs, listas de tarefas, planos preventivos e geração de ordens funcionando normalmente. Porém, na revisão da base, verifica-se que os equipamentos e sistemas críticos definidos nos estudos de segurança não foram inseridos no sistema. Qual é o efeito mais provável dessa omissão sobre a gestão da integridade?

**R:** Reduz a aderência do cadastro e da gestão informatizada às necessidades de integridade, por não incorporar a criticidade desses equipamentos e sistemas.

_Explicação:_ Mesmo com cadastro e planos funcionando, a gestão informatizada fica incompleta para integridade se não incorporar os equipamentos e sistemas críticos definidos em estudos de segurança. Sem essa informação, o sistema não reflete adequadamente a criticidade que deve orientar o controle do ativo.

_Às cegas (equivalente):_ A omissão impede priorização e rastreabilidade dos itens críticos (SECE/barreiras), levando a PMs/inspeções incompletas, risco de falhas não detectadas, não conformidade regulatória e decisões de integridade distorcidas. Falta saber se há controle paralelo (planilhas/sistema SIS).

### Segurança Ocupacional, Saúde e Meio Ambiente

#### Condições Ambientais e Impactos Operacionais

**facil · APROVADA · corrigida**  
_Nota(s): Alterações meteoceanográficas na extensão de vida útil: revalidação da base de segurança e integridade_

**P:** No contexto da ANP no Brasil, qual é a condição formal para manter a continuidade operacional de uma FPSO/FSO em extensão de vida útil?

**R:** Atender às avaliações de integridade e às condicionantes do estudo de EVU, inclusive o limite de data final de paralisação.

_Explicação:_ No contexto regulatório da ANP, a continuidade operacional em extensão de vida útil depende do atendimento às avaliações de integridade e às condicionantes impostas pelos estudos de EVU, inclusive o respeito ao limite definido para a data final de paralisação.

_Às cegas (pergunta_insuficiente):_ Manter a continuidade operacional exige aprovação formal da extensão de vida pela Autoridade Marítima e organismos de classe, baseada em avaliação de integridade (estrutural/sistemas), inspeções, análises de risco e plano de manutenção/monitoramento atualizado. Falta definir o regulador/jurisdição aplicável.

_Às cegas (incorreta):_ Manter a operação em extensão de vida útil exige Autorização da ANP para Continuidade Operacional (ATO/ACO), baseada em avaliação formal de integridade (estrutural/sistemas) e certificação de classe atualizadas. Falta definir a resolução ANP aplicável ao seu caso específico.

**media · REPROVADA: sem_pista, resposta_unica_cega · corrigida**  
_Nota(s): Condições ambientais, variação de calado e efeito no aproamento e na dinâmica da unidade_

**P:** Durante uma manobra de mudança de aproamento, considerando apenas a variação do ângulo de incidência de vento, corrente e ondas e o fato de os propulsores serem fixos ao casco, que mecanismo altera o controle de posição?

**R:** A mudança de aproamento altera as componentes das forças ambientais no casco e a direção dos eixos de atuação dos propulsores fixos.

_Explicação:_ Pela mudança de aproamento, vento, corrente e ondas passam a incidir com outro ângulo em relação ao casco, mudando as componentes vetoriais das forças ambientais. Como os propulsores são fixos ao casco, seus eixos de atuação também mudam de direção, o que altera o problema de controle de posição.

_Às cegas (alternativa_valida):_ Com o aproamento, muda o ângulo de incidência do escoamento no casco/coluna, alterando a distribuição hidrodinâmica e a “blindagem” dos propulsores; cai a eficiência (perda de empuxo, recirculação/cavitação/ventilação) e aumenta o esforço para manter posição.

**dificil_A · APROVADA**  
_Nota(s): Critérios de avaliação de fadiga e vibração para integridade estrutural_

**P:** Em uma derivação de tubulação offshore, a medição de vibração enquadrou a linha na região azul do critério velocidade RMS × frequência. Não há trinca visível, e a verificação estrutural feita até agora considerou apenas parâmetros elásticos do estado íntegro. Qual é a conduta técnica mais consistente?

**R:** Implementar controle adicional ou melhorar a operação, e refazer a análise considerando também os parâmetros elásticos após o dano por fadiga.

_Explicação:_ No critério vibratório, a região azul já indica potencial de falha por fadiga, portanto a linha não deve ficar apenas em observação passiva. Além disso, a avaliação estrutural é insuficiente se considerar somente o estado íntegro, porque o critério exige verificar também a condição após o dano por fadiga.

_Às cegas (parcial):_ Manter em operação com monitoramento/trending e inspeção periódica, e complementar a avaliação com análise de fadiga (S–N) e verificação de suportes/clamps/ressonância, não só elástica. Falta definir tempo de exposição/ciclos no envelope operacional para fechar a vida remanescente.

#### Gestão de Pessoas e Treinamento

**facil · REPROVADA: suporte, codigo:pergunta_aberta**  
_Nota(s): Treinamento, indução e desenvolvimento de competências para reduzir erro humano_

**P:** Quais fatores organizacionais estão associados à redução da frequência de erros humanos e da probabilidade de seus efeitos adversos nas instalações?

**R:** Seleção de pessoal, treinamento, supervisão, programas de controle de qualidade, cultura de segurança e ambiente de indução ao trabalho.

_Explicação:_ A redução do erro humano depende de um conjunto de barreiras organizacionais, não apenas de capacitação técnica isolada. Esses fatores atuam para diminuir tanto a ocorrência do erro quanto a chance de ele gerar efeitos adversos sobre a instalação.

**media · REPROVADA: jurisdicao, sem_generalizacao · corrigida**  
_Nota(s): Competência para funções críticas, emergência e operações especiais na matriz de competências_

**P:** Em uma atividade offshore, a avaliação de riscos identificou que o trabalho deve ser controlado por PTW. Antes do início da execução, qual requisito se aplica à emissão da permissão?

**R:** A PTW deve ser emitida por pessoa competente.

_Explicação:_ Segundo o critério aplicável ao PTW, depois que a avaliação de riscos identifica a necessidade desse sistema de controle, o trabalho não deve prosseguir sem permissão emitida por pessoa competente.

**dificil_A · APROVADA**  
_Nota(s): Simuladores imersivos e OTS para desenvolver decisão operacional sob falhas_

**P:** Uma unidade offshore vai revisar sua matriz de treinamento. Há tarefas rotineiras de baixa consequência, partidas e paradas raras, resposta a falhas de processo e ações de emergência com potencial impacto em segurança e meio ambiente. Como critério de priorização, quais tarefas devem ir primeiro para treinamento em simulador imersivo/OTS?

**R:** As tarefas críticas, raras ou perigosas, de alta consequência de erro e ligadas a condições anormais, falhas e emergência; as demais podem ficar com sala de aula, CBT ou OJT estruturado.

_Explicação:_ Simuladores e cenários de alta fidelidade são mais indicados quando a competência envolve situações que não podem ser treinadas com segurança ou frequência suficiente na planta real, especialmente falhas, modos raros e emergências. Métodos menos imersivos e treinamento estruturado em serviço continuam adequados para tarefas rotineiras de menor criticidade.

_Às cegas (equivalente):_ Priorize no OTS tarefas raras e de alta consequência: emergências (ESD, blowdown, incêndio/gás, perda de contenção), resposta a falhas críticas (trip de compressores/geração, perda de utilidades) e partidas/paradas complexas. Rotinas de baixa consequência ficam para treinamento no posto/procedimentos.

**media · APROVADA**  
_Nota(s): Planejamento do treinamento por tarefas críticas, competência e reciclagem_

**P:** Ao definir ou revisar a periodicidade de reciclagem de treinamento para procedimentos e tarefas críticas em uma unidade offshore, quais critérios técnicos devem orientar essa decisão e que tratamento deve ser dado aos procedimentos críticos?

**R:** Complexidade da tarefa, severidade dos cenários, frequência de execução e atualizações dos procedimentos; procedimentos críticos devem ter reciclagem diferenciada.

_Explicação:_ A periodicidade de reciclagem não deve seguir um intervalo uniforme para todos os casos. Ela precisa ser compatível com a complexidade e o potencial de consequência das tarefas, com a frequência de execução e com mudanças nos procedimentos, enquanto procedimentos críticos exigem frequência diferenciada dentro de um programa contínuo.

_Às cegas (parcial):_ Critérios: análise de risco (HAZID/HAZOP/JSA), criticidade/barreiras, histórico de incidentes e desvios, mudanças (MOC), desempenho/auditorias, complexidade, frequência de execução, turnover, requisitos legais/IMCA/ISO, lições aprendidas e exercícios. Procedimentos críticos: padronizados, controlados, treinados antes da tarefa e reciclados por competência, com simulado/avaliação, registros e revisão formal periódica.

#### Meio Ambiente, Gestão Ambiental e Sustentabilidade

**facil · APROVADA**  
_Nota(s): Uso eficiente de recursos e redução da pegada de carbono nas operações de FPSO/FSO_

**P:** Em cenário de escassez de recursos hídricos, qual medida de gestão ambiental é indicada para a água usada pela indústria?

**R:** Tratamento e reúso de efluentes para otimizar o uso de recursos hídricos.

_Explicação:_ Quando há escassez hídrica, a gestão ambiental da água industrial deve priorizar estratégias que reduzam a demanda por água nova e evitem descarte desnecessário. O tratamento seguido de reúso de efluentes atende a esse objetivo ao otimizar o uso dos recursos hídricos.

_Às cegas (equivalente):_ Indica-se implementar reúso/recirculação de água industrial (tratamento e reaproveitamento em circuito fechado), com metas de redução e monitoramento de consumo e perdas. Falta definir a qualidade requerida e a fonte atual (captação, dessalinização ou rede) para dimensionar o tratamento.

**media · APROVADA**  
_Nota(s): Bioincrustação por espécies exóticas em estruturas offshore no descomissionamento: risco de disseminação, controle e exigências operacionais_

**P:** Após a remoção de bioincrustação por espécie exótica invasora em uma estrutura offshore, que exigências mostram que o material removido deve ser tratado como parte do controle ambiental da espécie, e não apenas como resíduo operacional?

**R:** Destinação final do resíduo em conformidade com a legislação e eventual coleta de parte do material biológico, se houver solicitação justificada do IBAMA.

_Explicação:_ O material gerado na remoção não é tratado somente como descarte operacional porque precisa ter destinação final legal e, além disso, parte dele pode ser segregada e coletada para estudos ambientais quando houver solicitação justificada do IBAMA. Essas exigências inserem o material no controle ambiental da espécie exótica invasora.

_Às cegas (incorreta):_ Exigências: plano/programa de controle/erradicação aprovado pelo órgão ambiental; condicionantes de licença e procedimentos de biossegurança (contenção, segregação, rastreabilidade); transporte e destinação como material biológico de risco, com tratamento (inativação/esterilização) e comprovação. Falta indicar o órgão/condicionantes aplicáveis ao empreendimento.

#### Saúde Ocupacional

**facil · APROVADA**  
_Nota(s): Medidas de controle e proteção contra contaminantes químicos em operações offshore_

**P:** Em operações offshore, qual instrumento deve, antes da execução da atividade, identificar e gerenciar os riscos à saúde associados a substâncias perigosas?

**R:** O permit to work deve identificar e gerenciar esses riscos à saúde.

_Explicação:_ Esse controle precisa entrar no fluxo formal de liberação da atividade. O instrumento usado para identificar e gerenciar riscos à saúde ligados a substâncias perigosas antes da execução é o permit to work.

_Às cegas (incorreta):_ A Avaliação de Risco à Saúde (ARS/HRA), vinculada ao PGR/GRO, deve identificar e definir controles para riscos à saúde por substâncias perigosas antes da atividade. Falta definir a norma/sistema aplicável (ANP/NRs/ISO) para nome exato do documento.

**media · REPROVADA: autonomia, codigo:depende_do_material · corrigida**  
_Nota(s): Gestão de casos de doença, restrições e retorno seguro ao trabalho offshore_

**P:** No caso analisado de gestão de risco de COVID-19 offshore, sob regras de privacidade médica que limitavam a identificação direta de trabalhadores com maior risco de doença grave, qual mecanismo de identificação predominava?

**R:** Predominava a autodeclaração do empregado, em vez de triagem por terceiros.

_Explicação:_ No caso analisado, as regras de privacidade médica limitaram a identificação direta, de modo que a maior parte dos operadores dependia de que o próprio empregado se declarasse como integrante de grupo de alto risco para doença grave por COVID-19.

**dificil_A · APROVADA**  
_Nota(s): Análise Ergonômica do Trabalho como adaptação do trabalho ao homem e base para adequação ergonômica de postos, equipamentos e sistemas_

**P:** Em uma auditoria de uma unidade offshore, a instalação apresenta AET formalmente emitida, mas os relatórios tratam principalmente de mobiliário administrativo. Na planta e na sala de controle, operadores relatam compensações frequentes para executar tarefas rotineiras, sem evidências de acompanhamento das recomendações. Qual deve ser o foco prioritário das intervenções ergonômicas?

**R:** Priorizar as tarefas rotineiras reais da planta e da sala de controle em que há compensações do operador, e não avaliações apenas administrativas.

_Explicação:_ A priorização ergonômica deve recair sobre a atividade real, especialmente onde o operador precisa compensar a distância entre o trabalho prescrito e o trabalho executado. Relatórios centrados em "mesa-cadeira-computador" e sem implementação de recomendações não atendem ao objetivo da AET em instalações offshore.

_Às cegas (equivalente):_ Priorizar ergonomia operacional na planta e sala de controle: análise das tarefas reais, redução de compensações em rotinas (layout, acesso, ferramentas, interfaces), e implantação de plano de ação com responsáveis, prazos e verificação de eficácia. Falta definir escopo AET vs atividades críticas.

#### Segurança Ocupacional

**facil · APROVADA**  
_Nota(s): Planejamento do içamento e sistema formal de trabalho seguro_

**P:** Quais elementos administrativos compõem o sistema formal de trabalho seguro para lifting/handling antes da execução da manobra?

**R:** Permissões, procedimentos, procedimentos específicos da empresa, toolbox meeting e lifting plans.

_Explicação:_ O sistema formal de trabalho seguro para lifting/handling é estruturado por controles administrativos definidos antes da manobra. Esses elementos são complementares entre si e organizam o preparo e o controle da atividade antes do início do içamento.

_Às cegas (parcial):_ PTW/Permissão de Trabalho; JSA/AST; plano e procedimento de içamento/manuseio; checklist pré-uso de guindaste/talhas/acessórios certificados; matriz de responsabilidades/competências; autorização/validação do responsável; comunicação (toolbox talk) e plano de emergência/resgate.

**media · APROVADA**  
_Nota(s): Isolamento positivo, despressurização e verificação de ausência de gás antes de abrir sistemas_

**P:** Uma linha de processo que continha hidrocarbonetos foi apenas drenada por gravidade e aberta à atmosfera. Antes da abertura definitiva, não houve teste que comprovasse ausência de gás. Qual deve ser a premissa de segurança sobre o conteúdo remanescente?

**R:** Que a linha ainda pode conter líquidos ou vapores inflamáveis e não está comprovadamente segura para abertura ou corte.

_Explicação:_ Drenagem por gravidade e abertura à atmosfera podem deixar produto e vapores retidos. Sem verificação positiva da ausência de condição perigosa, a linha deve continuar sendo tratada como potencialmente inflamável.

_Às cegas (equivalente):_ Premissa: a linha ainda contém hidrocarbonetos e pode ter gás/vapores inflamáveis e atmosfera explosiva; tratar como energizada/perigosa até prova em contrário. Falta a condição: teste/medições de gás (LEL/VOC/O2) comprovando ausência de inflamáveis.
