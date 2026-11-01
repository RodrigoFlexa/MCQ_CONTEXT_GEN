# Nova edição do contexto — polimento

**Estado:** interrompido

Base: /home/gbs2/MCQ_CONTEXT_GEN/pipeline/qa_research/relatorios/polimento_3_contextos_20261101T194650/07_01/documento.json

Intervenções aprovadas: 1 de 3.
Alterações aprovadas: 1.
Alterações de acabamento: 0.
Palavras: 6692 → 6677.
Tentativas externas cumulativas: 13.
Documento publicado: não; leia documento_para_revisao.md.
Elegível para QA: não.

A preservação de texto herdado não significa que todas as afirmações anteriores foram verificadas novamente.

| Ponto estável | Cobertura | Motivo |
|---|---|---|
| F01 | atendido | O capítulo cobre sensores, transmissores, analisadores, cadeia de medição, erro, deriva, histerese, repetibilidade, calibração, verificação, rastreabilidade e loop check. A necessidade restante é editorial, não de conteúdo essencial. |
| F02 | atendido | O documento cobre atuadores, posicionadores, suprimento pneumático, stiction, hunting, diagnóstico com posicionador inteligente, compensação temporária de atrito, distinção entre válvula modulante e ESDV, solenoides, chaves fim de curso, perda de curso, falha de atuação e vazamento pela sede. |
| F03 | parcial | Há boa cobertura de arquitetura, comunicação, redundância e diagnóstico por camadas, mas ainda falta ensinar de forma mais explícita a separação entre falha de cabo, fonte, cartão/canal de I/O, remota de I/O, servidor/estação e rede, com sintomas e limites de inferência. |
| F04 | atendido | O capítulo cobre com boa profundidade intertravamentos, permissivos, bypasses, overrides, compensações, retorno ao serviço, testes funcionais, proof tests, matriz de causa e efeito e interfaces com SIS, ESD e F&G, preservando limites de cobertura dos ensaios. |
| F05 | parcial | Há cobertura consistente de gestão de mudanças, configuração, alarmes, proteção Ex e confiabilidade, mas faltam explicitamente backups, restauração, controle de acesso, versionamento e o tratamento técnico de sobressalentes e obsolescência dos sistemas de automação. |

Interrupção: CallFailure: acabamento_editorial: resposta truncada após duas tentativas

Trabalho ainda pendente (intervenções, cobertura, escopo e revisão):

- I01 (lacuna_essencial): Acrescentar um bloco que ensine o diagnóstico por sintomas e por escopo de falha na arquitetura de automação, distinguindo perda de um canal de campo, falha de cabo ou alimentação, falha de canal ou cartão de I/O, falha de remota de I/O, perda de comunicação de rede, falha de controlador, indisponibilidade de servidor/estação e degradação de redundância.
- I02 (lacuna_essencial): Acrescentar um bloco sobre integridade de configuração ao longo do ciclo de vida, cobrindo controle de versões, backups, restauração, controle de acesso e alterações de setpoints, lógicas, alarmes e intertravamentos; no mesmo bloco, fechar a ligação com sobressalentes e obsolescência de PLCs, DCS, SIS, módulos e estações críticas.
- cobertura_F03 (lacuna_essencial): Há boa cobertura de arquitetura, comunicação, redundância e diagnóstico por camadas, mas ainda falta ensinar de forma mais explícita a separação entre falha de cabo, fonte, cartão/canal de I/O, remota de I/O, servidor/estação e rede, com sintomas e limites de inferência.
- cobertura_F05 (lacuna_essencial): Há cobertura consistente de gestão de mudanças, configuração, alarmes, proteção Ex e confiabilidade, mas faltam explicitamente backups, restauração, controle de acesso, versionamento e o tratamento técnico de sobressalentes e obsolescência dos sistemas de automação.
- escopo_1 (lacuna_essencial): A integração entre equipes de instrumentação, automação, elétrica, processo, operação e manutenção aparece na frase do especialista, mas não está explicitamente representada no mapa curado.
- escopo_2 (lacuna_essencial): A análise estruturada de falhas recorrentes e causa raiz aparece na frase do especialista, mas o mapa curado não a destaca como ponto próprio.

Pareceres, fontes, comparação antes/depois e decisões estão na pasta da versão: `versoes/bf8bea2f105a7110788d3fd8/`.
