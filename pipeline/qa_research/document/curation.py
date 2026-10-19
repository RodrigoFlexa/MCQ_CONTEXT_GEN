"""Curadoria humana dos caminhos de busca; não gera perguntas nem chama modelos.

Cada linha: capítulo | âncoras PT/EN | consulta EN | decisões e relações a explicar.
O escopo integral de cada frase é preservado separadamente no perfil publicado.
"""
PLANS = {
"01.01": """
Indicadores e metas|indicador;desempenho;kpi;performance indicator|FPSO operational performance indicators targets measurement|Definição, denominadores, metas, qualidade de dados e interpretação dos indicadores de produção, segurança, ambiente e equipes.
Disponibilidade e confiabilidade|disponibilidade;confiabilidade;availability;reliability;mtbf;mttr|offshore production availability reliability maintenance losses|Disponibilidade, eficiência, confiabilidade, mantenabilidade e efeito da redundância sobre o desempenho dos sistemas.
Perdas e restrições de produção|perda de produ;deferment;production loss;gargalo;bottleneck|FPSO production deferment bottleneck loss accounting|Balanços, produção potencial, perdas planejadas e não planejadas, gargalos e atribuição de causas.
Planejamento, custos e riscos|custo operacional;gestão de risco;operating cost;asset management|FPSO asset management operational planning costs risk decisions|Planejamento operacional, custos do ciclo de vida, priorização por risco e consequências das decisões.
Equipes e melhoria contínua|melhoria contínua;continuous improvement;human factor;competência|offshore operational performance teams continuous improvement|Desempenho das equipes, acompanhamento de ações, análise de causa, aprendizagem e revisão das metas.
""",
"02.01": """
Arquitetura e seleção de medidores|medição fiscal;custody transfer;fiscal metering;flow meter|offshore oil gas fiscal metering custody transfer measurement systems|Seleção, instalação, condicionamento do escoamento, trechos retos e limites dos medidores de óleo e gás.
Volumes e propriedades|volume corrigido;compressibilidade;compressibility;density;bsw;densidade|petroleum gas standard volume correction density water sediment compressibility|Condições de referência, densidade, água e sedimentos, propriedades do gás, amostragem e cálculo de volumes.
Calibração e comprovação|calibra;prover;meter factor;rastreabilidade metrológica|oil gas meter proving calibration traceability meter factor|Calibração, verificação, provadores, fator do medidor, padrões e cadeia de rastreabilidade.
Incerteza e validação de dados|incerteza;uncertainty;measurement error;validação de dados|fiscal measurement uncertainty budget data validation reconciliation|Fontes e combinação de incerteza, erros, reconciliação, validação e tratamento de dados inválidos.
Custódia, falhas e registros|offloading;custódia;anp;metering audit|FPSO offloading custody transfer metering audit failure reporting|Fronteiras de custódia, balanços da transferência, registros, auditorias e comunicação de falhas; requisitos normativos só com suporte de edição e jurisdição.
""",
"02.03": """
Caracterização e separação gravitacional|água produzida;produced water;oil water separator;skimming|FPSO produced water gravity separation skimming vessel droplet size|Óleo disperso e dissolvido, sólidos, tamanho de gotas, residência, skimming e influência de temperatura e vazão.
Hidrociclones|hidrocicl;hydrocyclone|produced water deoiling hydrocyclone pressure drop split ratio|Separação centrífuga, diferencial de pressão, split, turndown, erosão e diagnóstico de perda de eficiência.
Flotação e produtos químicos|flota;flotation;coagulante;flocculant|produced water induced gas flotation coagulation chemical dosing|Adesão bolha-gota, flotação induzida, química, espuma e interação entre os estágios do tratamento.
Controle, desvios e correntes oleosas|água produzida;produced water;off specification|FPSO produced water off specification diversion recirculation slop control|Controle de processo, recirculação, desvio, slop, resíduos oleosos e resposta a variações e falhas.
TOG, amostragem e desempenho|óleos e graxas;oil in water;tog;sampling|produced water oil in water monitoring sampling online laboratory discharge|Amostragem representativa, métodos laboratoriais e instrumentos on-line, eficiência e controle do descarte; não extrapolar limites ambientais sem fonte normativa válida.
""",
"02.04": """
Captação e bombeamento|sea water intake;seawater lift;caixa de mar;bomba de injeção;water injection|FPSO seawater intake lift injection pumps pressure flow cavitation|Caixas de mar, captação, bombas, demanda de vazão e pressão, cavitação, redundância e desempenho.
Filtração e injetividade|filtra;filtration;injectivity;injetividade|seawater injection filtration backwash suspended solids reservoir injectivity|Filtros, retrolavagem, sólidos, tamanho de partículas e preservação da injetividade da formação.
Remoção de sulfato|sulfato;sulphate;sulfate;sru;nanofiltra|seawater sulfate removal unit nanofiltration membrane rejection fouling|SRU, rejeição de sulfato, membranas, pressões, limpeza, fouling e compatibilidade das águas.
Desaeração e oxigênio|desaera;deaerat;oxygen scaveng;oxigênio dissolvido|seawater injection vacuum deaeration dissolved oxygen scavenger corrosion|Transferência de massa, vácuo, sequestrantes de oxigênio, espuma e corrosão.
Microbiologia e compatibilidade|biocid;souring;microbiolog;scale inhibitor|seawater injection microbiological control souring scale reservoir compatibility|Biocidas, biofilmes, souring, incrustação, corrosão e incompatibilidade com água de formação e materiais.
Monitoramento e transientes|água de injeção;injection water;water quality|FPSO injection water quality monitoring startup shutdown troubleshooting|Controle de qualidade, alarmes, perda de utilidades, partidas, paradas e resposta à água fora de especificação.
""",
"02.05": """
Segregação e fontes de drenagem|open drain;closed drain;drenagem aberta;drenagem fechada|FPSO open closed drain segregation hazardous non hazardous sources|Classificação de fontes, drenagem pressurizada, atmosférica, perigosa e não perigosa e riscos de interligação.
Hidráulica e selos|drain;drenagem;water seal;liquid seal;funil de drenagem|offshore drain piping slope liquid seals gas migration hydraulic capacity|Declividades, dimensionamento, funis, caixas, selos e prevenção de migração de gás, refluxo e transbordamento.
Vasos, tanques e transferências|closed drain drum;open drain tank;slop;drain pump|FPSO closed drain drum open drain tank pumps slop recovery|Vasos, tanques, bombas, recuperação de hidrocarbonetos e interfaces com água oleosa, slop e flare.
Controle, inertização e transientes|drain;drenagem;blanketing;venting|offshore closed drain pressure control inerting alarms shutdown upset|Ventilação, inertização, pressão, níveis, alarmes e desempenho em operação normal, upset e emergência.
Comissionamento e integridade|drain;drenagem;flushing;leak test|FPSO drain system commissioning flushing leak testing corrosion blockage inspection|Testes, estanqueidade, flushing, limpeza, obstruções, corrosão, isolamento, manutenção e desativação segura.
""",
"02.06": """
Coordenação e balanço da produção|fpso;produção offshore;offshore production;production planning|FPSO integrated operations production planning bottlenecks performance|Planejamento, balanços de óleo, gás e água, restrições, perdas e decisões integradas de produção.
Partidas, paradas e alarmes|startup;shutdown;partida;parada;alarm management|FPSO startup shutdown transient alarm management abnormal operations|Sequências, permissivos, transientes, gestão de alarmes e estabilização após condições anormais.
Interfaces de processo e utilidades|fpso;utility;utilidades;process integration|FPSO process utilities power cooling fuel gas integration failures|Dependências entre processo, utilidades, energia e sistemas marítimos, eficiência energética e falhas comuns.
Interfaces marítimas e submarinas|fpso;offloading;subsea;lastro;mooring|FPSO marine cargo ballast stability mooring subsea operational interfaces|Lastro, estabilidade, armazenamento, transferência, ancoragem, poços e risers durante a operação integrada.
Disciplina operacional e mudanças|permit to work;management of change;simops;isolamento|FPSO operations maintenance handover permit isolation simultaneous operations|Passagem de turno, manutenção, permissões, isolamentos, SIMOPS, gestão de mudanças e competência.
Emergências e desempenho ambiental|fpso;emergency response;process safety;emiss|FPSO process safety emergency response environmental emissions waste operations|Escalonamento de emergências, barreiras, emissões, efluentes, resíduos e acompanhamento do desempenho.
""",
"02.07": """
Recebimento e separação em estágios|primary processing;primary separation;processamento primário;separação trifásica|FPSO primary oil processing multiphase staged separation inlet slugging|Recebimento de poços, manifolds e risers, separação multifásica, estágios e balanços de massa e energia.
Aquecimento, desidratação e dessalgação|desidrata;desalting;dehydration;electrostatic;dessalga|crude oil heating electrostatic dehydration desalting emulsion viscosity|Temperatura, viscosidade, água e sais, coalescência, tratamento eletrostático e qualidade do óleo.
Estabilização e especificação|crude stabilization;oil stabilization;estabiliza;vapor pressure|FPSO crude oil stabilization vapor pressure storage export specification|Pressão de vapor, gases liberados, BS&W, especificações de armazenamento e exportação.
Emulsões, espuma e depósitos|emuls;foam;espuma;paraffin;asphaltene;incrusta|crude oil processing emulsion foam scale wax asphaltene chemical treatment|Mecanismos, dosagem e compatibilidade química, sólidos, parafinas, incrustação e corrosão.
Controle e transientes|separator;separador;process control;controle de nível|FPSO oil processing pressure level flow control startup shutdown upset|Malhas, alarmes, intertravamentos, recirculações, partidas, paradas e resposta a alterações da produção.
Desempenho e integridade|fpso;oil processing;processamento de óleo;bottleneck|FPSO oil process equipment capacity heat exchanger pump vessel integrity|Gargalos, eficiência de trocadores, bombas e vasos, disponibilidade, inspeção e perdas de produção.
""",
"02.08": """
Cenários e cargas de alívio|overpressure;relief;psv;sobrepressão|FPSO overpressure relief scenarios blocked outlet fire thermal expansion sizing|Causas de sobrepressão, cenários simultâneos, seleção de PSV e definição de cargas de alívio.
Despressurização e blowdown|blowdown;depressuri;despressuri;bdv|FPSO emergency depressurization blowdown low temperature inventory|Inventário, BDV, tempo de despressurização, baixas temperaturas e efeitos sobre materiais e processo.
Headers e knock-out drums|flare header;knock out;knock-out;contrapressão;backpressure|flare network high low pressure headers knockout drum two phase backpressure|Segregação de headers, escoamento bifásico, contrapressão, arraste, slugging e coleta de líquidos.
Ignição, purga e prevenção de ar|flare;pilot;purge;liquid seal;water seal|offshore flare tip pilot ignition purge air ingress seal flashback|Pilotos, ignição, purga, selos, prevenção de entrada de ar e retorno de chama.
Radiação, dispersão e emissões|flare;radiation;radiação;flaring;dispersion|FPSO flare thermal radiation gas dispersion noise emission minimization|Radiação térmica, dispersão, ruído, emissões e minimização de queima sem comprometer as funções de proteção.
Operação e ciclo de vida|flare;relief system;sistema de alívio|FPSO flare relief commissioning inspection corrosion maintenance emergency shutdown|Interfaces com drenagem e ESD, partidas, upset, testes, inspeção, vibração, manutenção e descomissionamento.
""",
"02.09": """
Coalescência e campo elétrico|electrostatic;coalesc;eletrostát;eletrostat|crude oil electrostatic coalescence electric field electrodes water droplets|Polarização, colisão, crescimento e separação de gotas; campo, tensão e configuração de eletrodos.
Fluidos, emulsões e químicos|electrostatic;desalter;desidratador;emuls|electrostatic crude treater emulsion viscosity salinity demulsifier solids gas|Viscosidade, densidade, salinidade, água, emulsificantes, sólidos e gás livre no desempenho do tratador.
Controle de interface e qualidade|electrostatic;desalter;tratador|electrostatic treater oil water interface temperature residence time BSW salt|Interface, temperatura, pressão, vazão, residência, BS&W, sais, turndown e especificação do óleo.
Falhas elétricas e proteções|electrostatic;desalter;high voltage;alta tensão|electrostatic treater short circuit arcing voltage instability protective interlocks|Arcos, curtos, isoladores, transformadores, alarmes, intertravamentos e diagnóstico do campo instável.
Operação, inspeção e interfaces|electrostatic;desalter;tratador|FPSO electrostatic treater commissioning maintenance internal inspection process integration|Partida, comissionamento, carryover, carryunder, manutenção e interfaces com aquecedores e separadores.
""",
"02.10": """
Princípios e capacidade de separação|three phase;three-phase;trifásic;trifasic|three phase separator gas oil water residence time capacity turndown|Equilíbrio, densidade, viscosidade, residência, capacidade e eficiência da separação gás-óleo-água.
Internos e arraste entre fases|separator;separador;mist eliminator;demister|three phase separator inlet device coalescer demister carryover carryunder|Distribuição de entrada, defletores, coalescedores e eliminadores de névoa; carryover, carryunder e arraste cruzado.
Controle de pressão e interfaces|separator;separador;interface;level control|three phase separator pressure oil water interface level control instrumentation|Níveis, interface, pressão, instrumentos, válvulas de saída e interações entre malhas.
Emulsões, espuma e sólidos|separator;separador;slugging;emuls;foam|three phase separator slugging emulsion foam sand deposits troubleshooting|Slugging, areia, emulsões, espuma, depósitos e diagnóstico de baixa eficiência.
Transientes, proteção e integridade|separator;separador;shutdown;psv|FPSO three phase separator startup shutdown relief inspection integrity|Partidas, paradas, mudanças nos poços, alarmes, ESD, PSV, inspeção do vaso e interfaces com gás e água produzida.
""",
"02.11": """
Separação de líquidos e contaminantes|gas treatment;tratamento de gás;scrubber;coalescer|FPSO produced gas scrubber filter coalescer liquid solid removal|Scrubbers, filtros e coalescedores, arraste de líquidos e sólidos e proteção dos estágios seguintes.
Adoçamento e gases ácidos|sweetening;amine;amina;acid gas;h2s|natural gas sweetening amine hydrogen sulfide carbon dioxide removal|H₂S, CO₂, seleção de adoçamento, absorção, regeneração, corrosão e qualidade do gás.
Desidratação e ponto de orvalho|teg;glycol;glicol;dew point;desidratação de gás|natural gas dehydration TEG regeneration water dew point control|Absorção de água, circulação e regeneração de TEG, ponto de orvalho, perdas e contaminação.
Equilíbrio, hidratos e condensação|gas hydrate;hidrato;phase envelope;dew point|natural gas phase equilibrium hydrate prevention condensation corrosion|Pressão, temperatura, composição, hidratos, condensação de água e hidrocarbonetos e corrosão.
Controle, especificações e interfaces|gas treatment;tratamento de gás;fuel gas;export gas|FPSO gas treatment specification fuel export reinjection control troubleshooting|Destino combustível, exportação e reinjeção, malhas, transientes, energia, alarmes e manutenção.
""",
"02.12": """
Termodinâmica e estágios|compressor;compression;compressão;polytropic|gas compression stages pressure ratio polytropic efficiency intercooling|Razão de pressão, trabalho, eficiência, estágios, resfriamento e efeito da composição do gás.
Mapa e antissurge|surge;anti-surge;antissurge;compressor map|centrifugal gas compressor map surge choke recycle antisurge control|Surge, choke, mapa de desempenho, reciclo, controle e transientes de carga.
Auxiliares, selos e lubrificação|dry gas seal;seal gas;lubrication;compressor|offshore compressor dry gas seals seal gas lube oil bearings auxiliaries|Selagem, gás de selo, óleo lubrificante, mancais, condicionamento e proteção contra líquidos.
Acionamento e controle|compressor;gas turbine;variable speed;compression|FPSO gas compression driver speed capacity pressure load control|Acionadores, controle de capacidade e pressão, interação com geração e processo.
Partidas, proteção e confiabilidade|compressor;compression;compressão;vibration|FPSO compressor startup shutdown vibration trips condition monitoring maintenance|Permissivos, sequências, vibração, temperatura, trips, manutenção e diagnóstico de perda de desempenho.
""",
"03.01": """
Configuração e aproximação do aliviador|offloading;tandem;shuttle tanker;aliviador|FPSO tandem offloading shuttle tanker approach turret spread mooring weathervaning|Turret, spread mooring, weathervaning, setores de aproximação, DP e apoio de rebocadores.
Amarração, posição e ambiente|hawser;offloading;chafe chain;pick-up rope|tandem offloading hawser tension relative motion station keeping weather limits|Hawser, acessórios, movimentos relativos, tensões, posição, distância e envelopes ambientais.
Mangueiras e equipamentos de transferência|offloading hose;floating hose;mangueira de offloading|FPSO offloading hose connection testing pressure drain disconnection storage|Preparação, conexão, testes, pressurização, drenagem, desconexão, inspeção e armazenamento de mangueiras.
Transferência, lastro e comunicação|offloading;cargo transfer;transferência de carga|FPSO shuttle tanker cargo transfer ballast stability pressure flow communication|Bombas, válvulas, vazão, pressão, níveis, sequência de tanques, estabilidade e coordenação entre equipes.
Emergências e contingências|offloading;emergency release;hawser;ers|FPSO offloading emergency shutdown release collision hose rupture oil spill|ESD, liberação de emergência, ruptura de cabo ou mangueira, perda de posição, poluição e SIMOPS.
""",
"03.02": """
Configurações e dimensionamento|mooring;ancoragem;turret;station keeping|FPSO spread turret mooring coupled analysis environmental static dynamic loads|Seleção, profundidade, cargas, resposta acoplada casco-risers-ancoragem e limites de excursão.
Linhas, fundações e componentes|mooring;amarras;fairlead;chain stopper;suction pile|FPSO mooring chain wire polyester rope suction anchor connector fatigue|Amarras, cabos de aço e sintéticos, âncoras, estacas, conectores, fairleads e mecanismos de dano.
Instalação e distribuição de cargas|mooring;ancoragem;pretension;pré-tensão|FPSO mooring installation pretension load distribution intact damaged condition|Hook-up, pré-tensão, retensionamento, distribuição de cargas e comportamento intacto ou avariado.
Posição, tensão e alarmes|mooring;dgps;offset;heading;station keeping|FPSO mooring position heading offset line tension monitoring alarms|DGPS, sensores, heading, offsets, tensões, tendências e interfaces com risers, offloading e SIMOPS.
Inspeção, reparo e contingências|mooring;ancoragem;line break;anchor dragging|FPSO mooring inspection ROV corrosion fatigue line break repair replacement|Inspeção aérea e submarina, corrosão, desgaste, fadiga, substituição, ruptura, arraste de âncora e extremos ambientais.
""",
"03.03": """
Tanques, transferências e slop|cargo tank;tanque de carga;slop;cargo pump|FPSO cargo slop tank filling transfer overfill segregation oil water|Níveis, interfaces, bombas, válvulas, sequência de transferência, slop, contaminação cruzada e transbordamento.
Gás inerte e atmosferas|inert gas;gás inerte;gas freeing;inerting|FPSO cargo tank inert gas oxygen pressure purge gas freeing entry|Geração, distribuição, qualidade, oxigênio, pressão, purga, inertização, limpeza e entrada em tanques.
Ventilação e pressão dos tanques|tank vent;pressure vacuum;pv valve;mast riser|cargo tank vent pressure vacuum valve mast riser flame screen emissions|P/V, mast risers, telas, vapores, sobrepressão e vácuo durante enchimento e descarga.
Lastro e qualidade da água|ballast;lastro;deballast|FPSO ballast water pumps valves treatment contamination control|Lastro e deslastro, bombas, válvulas, tratamento, segregação e contaminação da água de lastro.
Estabilidade e esforços estruturais|stability;estabilidade;trim;free surface;bending moment|FPSO intact damage stability free surface trim shear force bending loading computer|Calado, banda, trim, deslocamento, centro de gravidade, superfície livre, avaria, esforços e loading computer.
Integridade e condições anormais|cargo tank;ballast tank;tanque de lastro;hull corrosion|FPSO tank hull corrosion inspection sediment leak emergency stability|Corrosão, sedimentos, inspeção estrutural, falhas de transferência e limites em produção, manutenção e emergência.
""",
"04.01": """
Geometria, cargas e envelopes|pull-in;pull in;riser;hang-off|FPSO riser pull in trajectory tension minimum bend radius environmental loads|Configuração, trajetória, raio mínimo, peso submerso, flutuabilidade, ondas, correntes e movimentos da unidade.
Equipamentos e preparação|pull-in;pull in;winch;sheave;pull head|riser pull in winch wire sheave guide pull head proof load inspection|Cabos, guinchos, sheaves, guias, pull-in heads, capacidade, inspeção, testes e proof load.
Execução, I-tubes e hang-off|i-tube;hang-off;bend stiffener;pull-in|FPSO riser I tube hang off bend stiffener load transfer connection|Controle de geometria e tração, conexão, bend stiffeners, transferência de cargas e verificação após instalação.
Embarcações, ROV e SIMOPS|pull-in;pull in;plsv;rsv|FPSO PLSV RSV ROV riser installation coordination weather window SIMOPS|Coordenação de FPSO, PLSV, RSV e ROV, comunicação, posicionamento, ancoragem e limites ambientais.
Falhas e preservação da integridade|pull-in;pull in;overbending;riser installation|riser pull in stuck overbending torsion wire failure contingency leak testing|Travamento, sobretração, flambagem, torção, cabo ou guincho avariado, abandono temporário e testes de estanqueidade.
""",
"04.02": """
Arquitetura submarina e interfaces|subsea;submarin;manifold;plem;plet|FPSO subsea production wet tree manifold PLEM PLET jumper flowline riser|ANM, manifolds, PLEM, PLET, flowlines, jumpers, risers, umbilicais e ligação ao FPSO; excluir operações de perfuração com sonda.
Poços, controle e retorno à produção|subsea;árvore de natal;wet tree;choke;gas lift|FPSO subsea well startup restart choke pressure flow gas lift injection|Partida, retorno após paradas, choke, vazão, pressão, gas lift, injeção e alinhamento de válvulas.
Controle subsea e diagnóstico|subsea control;umbilical;eletro-hidrául;electrohydraulic|subsea production hydraulic electrohydraulic control umbilical communication failure|Atuação hidráulica e elétrica, comunicação, sensores, válvulas, falhas e diagnóstico de vazamentos.
Garantia de escoamento e linhas|flow assurance;garantia de escoamento;hydrate;wax;asphaltene|subsea flow assurance hydrate wax asphaltene scale sand pigging flushing|Hidratos, parafinas, asfaltenos, incrustações, erosão, areia, pigging, flushing e preservação.
Isolamento, barreiras e contingências|subsea;well integrity;barrier;integridade de poço|FPSO subsea isolation depressurization well barriers leak loss of control contingency|Barreiras de poço e linhas, equalização, despressurização, perda de contenção e interfaces de emergência com topside.
Inspeção e intervenção com ROV|subsea;rov;rsv;subsea intervention|subsea ROV inspection intervention jumper replacement seabed fatigue corrosion|Inspeção, danos, fadiga, corrosão, leito marinho, troca de módulos e jumpers e SIMOPS com RSV; sem intervenção direta com sonda.
""",
"05.01": """
Ar de instrumento e de serviço|instrument air;ar de instrumento;compressed air;air dryer|FPSO instrument service air compressor dryer receiver pressure dew point|Compressores, filtros, secadores, vasos, ponto de orvalho, pressão, consumidores e perda de ar.
Nitrogênio e inertização|nitrogen;nitrogênio;psa;membrane nitrogen|FPSO nitrogen generation membrane PSA purity inerting purge blanketing|Geração por membranas ou PSA, pureza, capacidade, armazenamento, purga, inertização e preservação.
Água do mar e hipoclorito|hypochlorite;hipoclorito;electrochlorination;seawater cooling|FPSO seawater utilities electrochlorination hypochlorite biofouling control|Captação para serviços, cloração, concentração, dosagem, biofouling e corrosão.
Resfriamento e aquecimento|cooling medium;heating medium;água de resfriamento;heat exchanger|FPSO cooling heating medium closed open loop heat exchanger expansion vessel|Circuitos abertos e fechados, trocadores, expansão, controle térmico, capacidade e fouling.
Água doce, potável e de serviço|potable water;fresh water;água potável;reverse osmosis|FPSO fresh potable service water reverse osmosis evaporation disinfection storage|Geração, osmose, evaporação, desinfecção, pressurização, armazenamento e prevenção de contaminação.
Combustíveis, auxiliares e disponibilidade|diesel;lubricating oil;fuel system;utility failure|FPSO diesel lubrication utilities demand redundancy startup failure essential consumers|Diesel, lubrificantes, filtração, demanda, redundância, sequências, consumidores essenciais e falhas comuns; geração elétrica em documento próprio.
""",
"05.02": """
Geração, cargas e redundância|power generation;geração de energia;gas turbine;spinning reserve|FPSO electrical generation gas turbine diesel load balance spinning reserve redundancy|Geração principal e emergência, turbinas e diesel, capacidade, demanda, reserva girante e N+1.
Sincronismo e compartilhamento|synchronization;load sharing;reactive power;sincronismo|offshore generator synchronization frequency voltage active reactive power sharing|Frequência, tensão, potência ativa e reativa, fator de potência, sincronismo e compartilhamento de carga.
Distribuição e proteções|switchgear;bus tie;electrical protection;proteção elétrica|FPSO switchgear transformer motor control bus tie selectivity earth fault protection|Barramentos, bus ties, transformadores, motores, seletividade, aterramento e proteções elétricas.
PMS, transientes e blackout|load shedding;blackout;black start;power management|FPSO power management load shedding large motor starting blackout black start|PMS, rejeição de cargas, partida de grandes consumidores, perda de geração, blackout e recomposição.
UPS, baterias e sistemas essenciais|ups;battery;uninterruptible;emergency generator|FPSO emergency essential electrical loads UPS batteries DC safety systems|Cargas essenciais, emergência, UPS, corrente contínua, baterias e interfaces com SIS, ESD e F&G.
Qualidade, condição e manutenção|harmonic;power quality;insulation;electrical maintenance|FPSO power quality harmonics variable speed drive insulation monitoring maintenance Ex|Harmônicos, desequilíbrio, acionamentos, temperatura, isolamento, proteção Ex, manutenção e eficiência energética.
""",
"06.01": """
Filosofia e rede de incêndio|fire water;firewater;fire main;combate a incêndio|FPSO fire water main pumps jockey hydraulic demand redundancy coverage|Cenários, demanda simultânea, bombas, jockey, caixas de mar, rede, vazão, pressão e redundância.
Dilúvio, monitores e espuma|deluge;water spray;fire foam;espuma de combate|FPSO deluge water spray monitors foam helideck tank fire protection|Dilúvio, water spray, hidrantes, monitores, espuma e seleção de proteção por área e combustível.
Extinção fixa e portátil|fire extinguish;co2 suppression;clean agent;extintor|FPSO fixed portable fire suppression carbon dioxide clean agent powder safety|CO₂, agentes limpos, pó, extintores e proteção de pessoas na liberação de agentes.
Acionamento, testes e disponibilidade|fire pump;deluge;firewater;combate a incêndio|FPSO firefighting pump start deluge testing inspection impairment contingency|Partidas automáticas e manuais, testes, corrosão, obstrução, indisponibilidades e medidas compensatórias; detecção em documento próprio.
Resposta e interfaces de emergência|firefighting;combate a incêndio;fire response|FPSO firefighting response emergency organization cooling isolation maintenance|Resposta a incêndio, resfriamento, isolamento, equipes, comunicações, comissionamento e manutenção.
""",
"06.02": """
Estrutura e responsabilidades do SGSO|sgso;operational safety management;anp;process safety management|FPSO operational safety management system leadership accountability documentation|Política, responsabilidades, práticas de gestão, documentação e integração do SGSO à operação.
Riscos, barreiras e elementos críticos|barrier;barreira;critical safety element;sgso|FPSO safety critical elements performance standards barrier management risk|Identificação de perigos, barreiras, elementos críticos, padrões de desempenho, verificação e degradação.
Mudanças, procedimentos e competência|management of change;procedimento operacional;competence;sgso|FPSO safety management change operating procedures training contractor competence|Gestão de mudanças, procedimentos, qualificação, treinamento, contratadas e disciplina operacional.
Incidentes, auditorias e indicadores|incident investigation;safety audit;sgso;leading indicator|FPSO safety audit incident investigation action tracking performance indicators|Notificação, investigação, causas, auditorias, indicadores proativos e reativos e eficácia das ações.
Emergência e melhoria contínua|emergency preparedness;sgso;safety management|FPSO safety management emergency preparedness drills continuous improvement|Preparação, exercícios, gestão de crises, revisão gerencial e aprendizado; obrigações legais só com fonte válida.
""",
"06.03": """
Identificação de interferências|simops;simultaneous operations;operações simultâneas|FPSO simultaneous operations interface hazards compatibility matrix|Mapeamento de atividades, dependências, matrizes de compatibilidade, riscos cumulativos e responsabilidades.
Planejamento e autorização|simops;permit to work;work coordination|FPSO SIMOPS coordination planning permit work toolbox meeting isolation|Planejamento integrado, permissões, isolamentos, reuniões e comunicação entre operação, manutenção e contratadas.
Interfaces marítimas e submarinas|simops;offloading;plsv;subsea operation|FPSO SIMOPS offloading PLSV RSV ROV mooring marine interface|Offloading, içamentos, PLSV, RSV, ROV, ancoragem, risers, embarcações e zonas de exclusão.
Barreiras e contingências|simops;simultaneous;simultâneas|FPSO SIMOPS barrier impairment stop work emergency change weather contingency|Degradação de barreiras, critérios para suspender atividades, mudanças, ambiente e resposta a emergências.
""",
"06.04": """
Identificação de perigos e desvios|hazid;hazop;what if;hazard identification|FPSO HAZID HAZOP guidewords deviations causes consequences safeguards|HAZID, HAZOP, What-if, parâmetros, desvios, causas, consequências e recomendações.
Análise quantitativa e consequências|qra;quantitative risk;fire explosion;consequence analysis|FPSO quantitative risk assessment fire explosion dispersion frequency consequence|Frequências, inventários, vazamentos, incêndio, explosão, dispersão e incertezas das análises.
Camadas de proteção e segurança funcional|lopa;sil;safety integrity;protection layer|FPSO LOPA independent protection layers SIL safety instrumented function|LOPA, independência de camadas, alocação de SIL, funções instrumentadas e premissas de disponibilidade.
Barreiras, ALARP e decisões|bow tie;bow-tie;alarp;barrier analysis|FPSO bow tie barrier ALARP risk acceptance safety study actions|Bow-tie, critérios de tolerabilidade, ALARP, medidas de redução e acompanhamento de recomendações.
Atualização e aplicação dos estudos|safety study;hazop;risk assessment;estudo de segurança|FPSO safety studies lifecycle change revalidation evacuation layout escape|Aplicação ao arranjo, evacuação e operação, revisão por mudanças, revalidação e rastreabilidade das premissas.
""",
"06.05": """
Tecnologias e cobertura de detecção|gas detector;flame detector;fire gas;fogo e gás|FPSO fire gas flame smoke detection technology coverage placement|Gás inflamável e tóxico, chama, fumaça, tecnologias, cobertura, posicionamento e limitações ambientais.
Lógica, votação e causa e efeito|fire gas;f&g;voting;cause effect|FPSO fire gas voting logic cause effect alarm ESD HVAC isolation|Votação, alarmes, matriz causa e efeito, ESD, ventilação, isolamento e interfaces de combate.
Testes, inibições e diagnóstico|gas detector;fire gas;proof test;detector|FPSO fire gas calibration proof testing inhibit bypass fault spurious alarm|Calibração, testes, falsas atuações, falhas, inibições, medidas compensatórias e retorno ao serviço.
Disponibilidade e manutenção|fire gas;f&g;detector;fire detection|FPSO fire gas detector maintenance redundancy power communication availability|Redundância, alimentação, comunicação, manutenção, comissionamento e preservação da cobertura.
""",
"06.06": """
Abandono e meios coletivos|lifeboat;liferaft;salvatagem;abandon ship|FPSO lifeboat liferaft abandonment capacity location launch recovery|Baleeiras, balsas, capacidade, localização, lançamento, recuperação e limitações operacionais.
Proteção individual e resgate|life jacket;immersion suit;rescue boat;man overboard|FPSO lifesaving lifejackets immersion suits rescue boat man overboard|Coletes, roupas de imersão, resgate de pessoa ao mar e interação com embarcações de apoio.
Rotas, reunião e comunicação|muster;escape route;evacuation;abandonment|FPSO escape evacuation muster station POB communication emergency|Rotas de fuga, pontos de reunião, POB, comunicação, evacuação e critérios de abandono.
Inspeções, exercícios e prontidão|lifesaving;lifeboat;salvatagem;drill|FPSO lifesaving appliance inspection maintenance drill davit release mechanism|Guinchos, davits, liberação, testes, manutenção, exercícios e indisponibilidades dos meios de salvatagem.
""",
"06.07": """
Perigos, avaliação e hierarquia de controles|risk assessment;hazard;análise de risco;hierarchy control|FPSO operational risk hazard assessment hierarchy control residual risk|Identificação de perigos, severidade, probabilidade, risco residual e seleção de controles.
Permissões, isolamentos e tarefas críticas|permit to work;lockout;tagout;isolation;permissão de trabalho|FPSO permit work energy isolation confined space hot work lifting|Permissões, bloqueio de energias, teste de isolamento, espaços confinados, trabalho a quente e atividades críticas.
Barreiras e disciplina de campo|barrier;line of fire;stop work;barreira|FPSO barrier assurance line of fire field verification stop work authority|Verificação dos controles, integridade de barreiras, autoridade de parada e gestão de desvios.
Fatores humanos, contratadas e comunicação|human factor;fadiga;contractor;fatores humanos|FPSO human factors fatigue contractor safety communication handover|Fadiga, erros, carga de trabalho, supervisão, coordenação e competência de equipes e contratadas.
Incidentes, emergências e aprendizagem|incident investigation;near miss;emergency;quase acidente|FPSO incident near miss root cause emergency corrective action learning|Investigação, causas sistêmicas, tendências, recorrência, ações e preparação para emergências.
""",
"07.01": """
Instrumentos e metrologia|instrumentation;transmitter;calibra;instrumentação|FPSO transmitter sensor calibration drift hysteresis repeatability loop check|Sensores, transmissores e analisadores; erro, deriva, histerese, padrões, calibração e loop checks.
Válvulas e elementos finais|control valve;stiction;positioner;válvula de controle|offshore control valve stiction hunting positioner actuator seat leakage maintenance|Posicionadores, atuadores, solenoides, atrito, hunting, vazamento de sede e diagnóstico.
DCS, PLC, redes e diagnóstico|dcs;plc;industrial network;remote io|FPSO DCS PLC industrial network IO power supply communication fault diagnosis|Arquitetura, redes, cartões, fontes, comunicação, redundância e localização de falhas.
SIS, testes e indisponibilidades|sis;esd;proof test;functional safety|FPSO SIS ESD safety function proof test bypass override compensating measures|Testes funcionais, intertravamentos, permissivos, bypasses, overrides, compensações e retorno ao serviço.
Configurações, Ex e confiabilidade|instrumentation;automação;automation;configuration management|FPSO automation configuration change backups Ex maintenance obsolescence reliability|Setpoints, lógicas, backups, mudanças, proteção Ex, sobressalentes, obsolescência e manutenção de sistemas críticos.
""",
"07.02": """
Arquitetura e segmentação IT/OT|cybersecurity;cyber security;ot security;cibersegurança|FPSO OT IT cybersecurity network segmentation zones conduits DMZ firewall|Inventário, fronteiras IT/OT, zonas, conduítes, DMZ, firewalls e defesa em profundidade.
Acessos e cadeia de suprimentos|cybersecurity;remote access;least privilege;ot security|offshore OT identity privileged remote vendor access removable media supply chain|Identidades, menor privilégio, acesso remoto de fornecedores, mídias e riscos de terceiros.
Vulnerabilidades, patches e legados|ot security;patch management;hardening;cybersecurity|industrial control vulnerability patch hardening legacy obsolescence availability|Vulnerabilidades, patches, hardening, configurações, legados e avaliação de indisponibilidade.
Monitoramento e resposta a incidentes|cybersecurity;ransomware;intrusion;incident response|FPSO OT cybersecurity monitoring logs malware ransomware incident containment|Eventos, logs, anomalias, malware, contenção, erradicação, resposta e interface com emergência operacional.
Backups, integridade e recuperação|ot security;cybersecurity;backup;disaster recovery|FPSO OT backup restoration safety logic data integrity recovery continuity|Backups, restauração testada, lógicas de SIS, autenticidade de dados, continuidade e recuperação segura.
Novas tecnologias e competência|iiot;digital twin;cybersecurity;industrial internet|FPSO IIoT digital twins cloud cybersecurity risk training engineering social|Integração de nuvem, sensores, analytics e IA, treinamento, engenharia social e testes sem impacto na planta.
""",
"07.03": """
Criticidade e estratégia de manutenção|rcm;fmea;fmeca;maintenance strategy;criticidade|FPSO maintenance criticality RCM FMEA preventive predictive condition based|Consequências das falhas, elementos críticos e escolha entre corretiva, preventiva e baseada em condição.
Planos, tarefas e CMMS|maintenance plan;cmms;sap pm;plano de manutenção|FPSO maintenance planning tasks intervals CMMS SAP work orders|Tarefas, periodicidades, critérios, ordens, notas, histórico, documentação e revisão dos planos.
Programação, backlog e diferimentos|backlog;maintenance scheduling;deferred maintenance;manutenção diferida|FPSO maintenance backlog scheduling deferral risk shutdown campaign|Priorização, recursos, sobressalentes, paradas, campanhas, manutenção vencida e medidas compensatórias.
Condição, falhas e causa raiz|condition monitoring;vibration;root cause;bad actor|FPSO condition monitoring vibration oil temperature chronic failure root cause|Vibração, óleo, temperatura, espessura, degradação, bad actors e eliminação de defeitos.
Indicadores e confiabilidade|mtbf;mttr;maintenance performance;reliability|FPSO maintenance availability MTBF MTTR preventive compliance effectiveness|MTBF, MTTR, disponibilidade, eficácia das tarefas e otimização de periodicidades.
Execução, preservação e retorno|maintenance;manutenção;standby;post maintenance|FPSO maintenance isolation spares preservation standby post maintenance testing|Preparação, isolamentos, redundância, materiais, obsolescência, preservação e testes pós-manutenção.
""",
"07.04": """
Risco e planos de inspeção|rbi;risk based inspection;inspection plan;inspeção|FPSO risk based inspection damage mechanisms criticality corrosion circuits|RBI, criticidade, mecanismos, circuitos de corrosão, pontos e periodicidades de monitoramento.
Mecanismos de dano|corrosion;corrosão;fatigue;erosion;stress corrosion|FPSO corrosion erosion CUI fatigue cracking embrittlement degradation|Corrosão interna, externa e sob isolamento, erosão, fadiga, trincas e fragilização.
END e aptidão para serviço|ultrasonic;non destructive;fitness for service;ultrassom|FPSO NDT ultrasonic thickness remaining life fitness for service repair|Inspeção visual, ultrassom e END avançados, taxas, vida remanescente, aceitação e reparos.
Equipamentos estáticos e documentação|pressure vessel;nr-13;nr13;piping integrity|FPSO pressure vessel piping tank inspection documentation safety devices NR13|Vasos, tubulações, tanques, inspeções e dispositivos; requisitos da NR-13 apenas quando enquadramento e versão estiverem documentados.
Casco, estruturas e proteção|hull;structural integrity;coating;cathodic;casco|FPSO hull topside structure splash zone tank corrosion coating cathodic protection|Casco, módulos, flare, helideck, tanques, regiões submersas, ROV, revestimentos e proteção catódica.
Anomalias, barreiras e extensão de vida|integrity management;life extension;inspection;integridade|FPSO integrity anomaly deferral safety critical element ageing life extension|Classificação de anomalias, recomendações, diferimentos, barreiras, reforços, envelhecimento e rastreabilidade.
""",
"07.05": """
Laboratório e calibração|calibration laboratory;metrological;laboratório;calibração|FPSO instrument calibration laboratory reference standard certificate acceptance|Padrões, certificados, tolerâncias, rastreabilidade, testes e diagnóstico de instrumentos.
Oficinas mecânica e elétrica|workshop;oficina;mechanical repair;motor repair|FPSO mechanical electrical workshop pump valve seal bearing motor repair testing|Desmontagem, medição, reparo, montagem e teste de bombas, selos, válvulas, motores e componentes elétricos.
Pipe shop e qualidade de fabricação|pipe shop;spool;welding;welder qualification|FPSO pipe shop spool fabrication welding material traceability NDT contamination|Spools, corte, bisel, soldagem, qualificação, segregação de ligas, END e rastreabilidade dos materiais.
Almoxarifado, estoques e reparáveis|spare parts;inventory;warehouse;sobressalente;almoxarifado|FPSO critical spares warehouse inventory reorder lead time repairable preservation|Cadastros, acuracidade, níveis e ponto de reposição, lead time, criticidade, reparáveis e obsolescência.
Preservação, ferramentas e liberação|workshop;oficina;preservation;tool calibration|offshore workshop tool certification spares preservation safety post repair release|Preservação, validade, armazenamento, certificação de ferramentas, áreas Ex, resíduos, segurança e limites do reparo a bordo.
""",
"08.01": """
Exposições e higiene ocupacional|occupational health;industrial hygiene;saúde ocupacional;exposição|FPSO occupational exposure noise heat vibration benzene chemical biological agents|Reconhecimento, avaliação e controle de ruído, calor, vibração e agentes químicos e biológicos.
Vigilância e aptidão|occupational health;medical surveillance;pcmsо;pcmso|offshore occupational medical surveillance fitness work exposure health monitoring|Vigilância médica, aptidão, acompanhamento de exposições e prevenção de agravos; sem inventar limites ou condutas clínicas.
Ergonomia, fadiga e saúde mental|ergonom;fatigue;fadiga;mental health|FPSO offshore ergonomics shift work fatigue psychosocial mental health|Ergonomia, turnos, sono, fadiga, carga física e mental e fatores psicossociais.
Assistência, emergência e prevenção|offshore health;medical evacuation;medevac;saúde|FPSO health emergency medical response medevac hygiene prevention|Estrutura de atendimento, primeiros cuidados, evacuação, higiene e prevenção em ambiente offshore.
""",
"08.02": """
Permissões e controle de energias|permit to work;lockout;tagout;segurança ocupacional|FPSO occupational safety permit work hazardous energy isolation verification|Permissões, APR, bloqueio, etiquetagem, energia residual e verificação antes da intervenção.
Espaço confinado e trabalho a quente|confined space;hot work;espaço confinado;trabalho a quente|FPSO confined space atmosphere testing ventilation rescue hot work ignition|Atmosferas, ventilação, monitoramento, resgate, fontes de ignição e medidas de prevenção.
Altura, quedas e movimentação|work at height;fall protection;dropped object;trabalho em altura|FPSO working height fall protection lifting dropped objects line fire|Quedas de pessoas e objetos, acesso, içamentos, linha de fogo, esmagamento e zonas de exclusão.
Eletricidade, químicos e proteção|electrical safety;chemical handling;ppe;proteção individual|FPSO electrical safety chemical handling PPE machine guarding occupational|Risco elétrico, máquinas, produtos químicos, EPI, proteção coletiva e escolha de controles.
Organização, contratadas e aprendizagem|occupational safety;contractor;toolbox;safety culture|FPSO occupational safety contractor toolbox human factors incident prevention|Supervisão, contratadas, competência, comunicação, inspeções, incidentes e cultura de segurança.
""",
"08.03": """
Licenciamento e gestão ambiental|environmental management;licenciamento;ibama;environmental license|FPSO environmental management licensing impact monitoring compliance|Aspectos e impactos, licenciamento, condicionantes, monitoramento, registros e responsabilidades.
Efluentes e água de lastro|produced water;ballast water;sewage;efluente|FPSO produced water sewage ballast water effluent treatment discharge monitoring|Água produzida, efluentes sanitários, lastro, drenagem e monitoramento de descarte; limites só com base válida.
Emissões e eficiência energética|greenhouse;emission;flaring;methane;emissão|FPSO atmospheric emissions methane flaring greenhouse energy efficiency|Gases de efeito estufa, metano, flare, inventários, controle de emissões e eficiência energética.
Resíduos e materiais perigosos|waste management;hazardous waste;resíduo;norm|FPSO waste hazardous materials segregation storage reverse logistics NORM|Classificação, segregação, armazenamento, rastreabilidade, logística reversa e materiais contaminados.
Poluição, resposta e sustentabilidade|oil spill;spill response;biodiversity;sustainability|FPSO oil spill prevention response biodiversity environmental sustainability|Prevenção, contenção e resposta a derramamentos, ecossistemas, consumo de recursos e melhoria ambiental.
""",
"08.04": """
Competências e dimensionamento|competence;competência;manning;training matrix|FPSO workforce competence matrix minimum manning qualification staffing|Perfis, competências, experiência, composição mínima e lacunas das equipes.
Treinamento e avaliação|training;treinamento;simulation;competency assessment|FPSO training onboarding refresher simulation practical competence assessment|Integração, capacitação prática, reciclagens, simulações, avaliação e eficácia da aprendizagem.
Liderança, desempenho e comunicação|leadership;teamwork;handover;liderança|FPSO leadership team performance feedback communication shift handover|Metas, feedback, comunicação, passagem de turno, equipe, conflitos e tomada de decisão.
Fadiga, mobilização e mudanças|fatigue;human factor;crew change;fatores humanos|FPSO fatigue workload crew change minimum competence organizational change|Carga de trabalho, fadiga, escalas, mobilização, substituições e preservação de competências.
Aprendizagem e revisão dos programas|learning;training;incident investigation;lessons learned|FPSO organizational learning incident competence gap training program review|Lições de incidentes, mudanças de processo e legislação, auditorias e revisão dos programas.
""",
"08.05": """
Dados meteoceanográficos e incerteza|metocean;meteocean;weather forecast;oceanographic|FPSO metocean wind wave current tide seasonal extreme forecast uncertainty|Vento, ondas, correntes, marés, extremos, dados, previsões, tendências e incertezas.
Movimentos, ancoragem e estruturas|fpso;wave induced;vessel motion;environmental load|FPSO environment motions heading mooring riser fatigue hull wave loads|Movimentos, acelerações, estabilidade, ancoragem, risers, fadiga e carregamentos ambientais.
Janelas e limites das operações|weather window;operational limit;metocean;offloading|FPSO weather window offloading crane helicopter ROV transfer abort limits|Limites para offloading, guindastes, pessoal, helicópteros, ROV e atividades externas; início, suspensão e abortamento.
Atmosfera marinha e sistemas|marine corrosion;ambient temperature;salt spray;lightning|FPSO marine atmosphere corrosion salt spray temperature cooling lightning drainage|Corrosão, spray, chuva, drenagem, temperatura, resfriamento, ventilação e descargas atmosféricas.
Dispersão, contingências e desempenho|wind dispersion;metocean;weather contingency;fpso|FPSO wind gas smoke flare dispersion severe weather contingency production loss|Vento, gases, fumaça, flare, prontidão, SIMOPS, mudanças rápidas, perdas e extensão de vida.
""",
"09.01": """
Demanda, suprimento e estoques|offshore logistics;supply chain;logística offshore;spare parts|FPSO offshore supply demand critical spares inventory lead time procurement|Demanda, compras, prioridades, criticidade, estoques, lead time e continuidade da cadeia de suprimentos.
Embarcações e interfaces marítimas|supply vessel;psv;ahts;plsv;rsv|FPSO supply vessel AHTS PLSV RSV approach station keeping marine interface|Programação, aproximação, posicionamento, zonas de segurança, interface com ancoragem, risers e ROV.
Cargas, granéis e produtos perigosos|offshore logistics;bulk transfer;dangerous goods;cargo handling|FPSO cargo bulk diesel chemical transfer hose dangerous goods segregation|Carga e descarga, granéis, mangueiras, identificação, embalagem, segregação e prevenção de derrames.
Helicópteros, POB e pessoal|helicopter;helideck;pob;crew change|FPSO helicopter helideck passenger manifest POB crew change medevac|Voos, helideck, passageiros, manifestos, POB, escalas, competências e evacuação médica.
Logística reversa e rastreabilidade|reverse logistics;logística reversa;cargo manifest;container|FPSO reverse logistics waste repairable container certification traceability|Resíduos, reparáveis, retornos a terra, contêineres, documentação, certificados e rastreio.
Desempenho, SIMOPS e contingências|offshore logistics;simops;weather window;supply vessel|FPSO logistics performance vessel utilization weather disruption contingency SIMOPS|Indicadores, custos, utilização de meios, atrasos, clima, demandas emergenciais e atividades simultâneas.
""",
"09.02": """
Plano e capacidade do içamento|lifting plan;rigging;load chart;lifting operation|FPSO offshore lifting plan crane capacity radius centre gravity dynamic factor|Peso, centro de gravidade, trajetória, raio, carga admissível, tabelas, fatores dinâmicos e içamentos críticos.
Acessórios e distribuição de esforços|sling;shackle;padeye;spreader beam;linga|offshore lifting slings shackles padeyes beam sling angle load distribution|Lingas, cabos, manilhas, ganchos, vigas, padeyes, ângulos e distribuição das forças.
Equipamentos, condição e certificação|offshore crane;hoist;guindaste;lifting appliance|FPSO crane hoist winch brake wire inspection testing certification maintenance|Guindastes, monovias, talhas, guinchos, freios, cabos, limitadores, inspeção e retirada de serviço.
Equipe, exclusão e comunicação|lifting;rigging;line of fire;tag line|FPSO lifting operator rigger banksman communication exclusion zone tag line|Responsabilidades, sinaleiro, rádio, toolbox, zonas de exclusão, linhas de fogo e controle da carga.
Movimentos, ambiente e SIMOPS|offshore lifting;vessel motion;blind lift;guindaste|FPSO supply boat lifting relative motion weather blind lift SIMOPS contingency|Movimentos relativos, limites de vento e mar, visibilidade, blind lifts, obstáculos, SIMOPS, falhas e contingências.
""",
"10.01": """
Envelhecimento e extensão de vida|life extension;ageing;aging;remaining life|FPSO ageing asset integrity remaining life fitness service life extension|Degradação, fadiga, corrosão, obsolescência, vida remanescente, inspeção especial, reparos e mudanças para extensão de vida.
Planejamento e escolha de estratégia|decommission;descomission;dismantling|FPSO decommissioning strategy offshore yard dismantling risk cost schedule|Planejamento de ciclo de vida, alternativas em estaleiro ou offshore, riscos, custos, cronograma, recursos e contingências.
Parada, limpeza e descontaminação|decommission;descomission;decontamination;gas freeing|FPSO final shutdown isolation depressurization flushing cleaning decontamination gas freeing|Parada definitiva, inventários, isolamento, drenagem, flushing, purga, inertização, limpeza e contaminantes.
Interfaces submarinas e ancoragem|decommission;descomission;subsea removal;mooring removal|FPSO subsea decommissioning well barriers riser umbilical mooring disconnection recovery|Barreiras e interfaces com poços, ANM, manifolds, linhas, risers, umbilicais, recuperação e remoção da ancoragem.
Preparação para reboque e estaleiro|tow-out;tow out;decommission;descomission|FPSO decommissioning tow out hull stability ballast weather route shipyard|Casco, estanqueidade, estabilidade, lastro, sistemas temporários, certificação, rota, janela e recebimento em estaleiro.
Desmontagem offshore e sistemas essenciais|offshore dismantling;heavy lift;decommission;desmantela|FPSO offshore dismantling module removal heavy lift progressive stability essential systems|Sequência de módulos, içamentos pesados, distribuição de pesos, resistência, sistemas essenciais, SIMOPS e mudança de barreiras.
Resíduos, reúso e encerramento|ship recycling;decommission;descomission;circular economy|FPSO decommissioning hazardous waste recycling reuse traceability environmental closure|Inventários, resíduos perigosos, reúso, reciclagem, rastreabilidade, logística, documentação e encerramento das pendências.
""",
}

# Filtros de domínio amplos: termos específicos dos recortes continuam obrigatórios.
# Não exigir literalmente FPSO em todo parágrafo permite recuperar engenharia
# transferível, enquanto a redação e auditoria restringem sua aplicação ao FPSO.
DOMAIN = "fpso;offshore;petróleo;petroleo;petroleum;oil;gas;gás;subsea;marine;marítim;plataforma;production;produção"
SPECIAL_CONTEXT = {
    "01": "fpso;offshore;asset;production;produção;petróleo;oil;maintenance;manutenção",
    "07.02": "industrial;ot;ics;scada;plc;dcs;sis;offshore;fpso;process control",
    "08.01": "offshore;fpso;occupational;ocupacional;worker;trabalhador;industrial",
    "08.02": "offshore;fpso;occupational;ocupacional;industrial;workplace;work site",
    "08.04": "offshore;fpso;crew;tripula;competence;industrial;maintenance;process safety",
}

# Revisão das amostras recuperadas: restringir a decisão técnica, sem exigir
# literalmente FPSO nem refazer a varredura ampla. IDs Fxx seguem a ordem acima.
POST_CONTEXT = {
    "02.01": {"*": ["medição", "meter", "measurement", "custódia", "custody", "fiscal", "amostragem", "sampling", "prover"]},
    "02.08": {"F01": ["sobrepress", "overpressure", "relief", "alívio", "psv", "pressure safety"]},
    "02.11": {"F01": ["scrubber", "gas treatment", "tratamento de gás", "gás produzido", "produced gas", "gas conditioning", "gas liquid", "gas-liquid"]},
    "03.01": {"*": ["offloading", "aliviador", "shuttle tanker", "tandem", "hawser", "cargo transfer"]},
    "04.01": {"*": ["pull-in", "pull in", "pullin", "i-tube", "hang-off", "hang off"]},
    "06.04": {"F03": ["lopa", "sil", "safety integrity", "segurança funcional", "protection layer"]},
    "07.02": {"*": ["cyber", "ciber", "ot", "scada", "industrial control", "industrial network", "dcs", "plc"]},
    "09.01": {"*": ["offshore", "fpso", "supply vessel", "supply boat", "psv", "plsv", "rsv", "helideck", "ahts"]},
}


def facets_for(key, title):
    """Expansão determinística da curadoria escrita acima; sem inferência por LLM."""
    if key not in PLANS:
        raise ValueError("Falta curadoria manual para " + key)
    context = SPECIAL_CONTEXT.get(key, SPECIAL_CONTEXT.get(key[:2], DOMAIN)).split(";")
    facets = []
    for i, line in enumerate(PLANS[key].strip().splitlines(), 1):
        label, terms, english, focus = line.strip().split("|")
        facets.append({"id": "F" + str(i).zfill(2), "grupo": title, "titulo": label,
            "foco": focus, "termos": terms.split(";"),
            "consultas": [f"FPSO {title}: {label}. {focus}", english],
            "context_groups": [context], "exclude_context": []})
        rules = POST_CONTEXT.get(key, {})
        gate = rules.get(facets[-1]["id"], rules.get("*"))
        if gate:
            facets[-1]["post_context_groups"] = [gate]
    return facets
