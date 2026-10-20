# Falha e retomada de QA em 03_02

O snapshot `qa_lote_9_03_02_20261020T172806026463Z`, recebido no commit `e784853`,
registra interrupção da auditoria por validação de citações. O planejamento, a
geração e a resolução sem gabarito já haviam sido salvos. A auditoria falhou três
vezes: duas por passagens não literais do contexto e uma por condição não literal
da pergunta. O orçamento tinha sete tentativas reservadas, em 305,18 segundos.

O reparo substitui a recitação na auditoria por seleção de IDs de passagens do
contexto integral e de partes do próprio enunciado. O código recupera os textos
exatos, rejeita IDs inexistentes e continua verificando sustentação, unicidade e
dificuldade. O formato limpo das perguntas e respostas permanece o mesmo.

A retomada reconhece apenas o fingerprint da implementação anterior conhecida,
mantendo iguais tópico, contexto, modelos e tokens. O orçamento não reinicia.
Checkpoints antigos são conferidos e as etapas com a mesma chave são reutilizadas.
O reparo de auditoria exige uma chamada nova nessa etapa; eventual refinamento e
nova verificação continuam sujeitos aos critérios e ao limite já configurados.

O teste de regressão usa uma cópia do checkpoint real de `03_02`, com auditor
simulado. Ele confirma que somente a auditoria é solicitada, que as sete tentativas
anteriores são preservadas e que os três checkpoints originais não são alterados.
Isso verifica a retomada; não é aprovação técnica real dessas nove questões.

O teste de lote aprovado usa o snapshot real de `02_02` e confirma que seus arquivos
são preservados sem chamadas nem regravação. Alteração de gabarito, modelos ou
implementação desconhecida continua sendo rejeitada.

O novo comando `rodar_qa_todos.sh` isola falhas de resposta por item, mostra progresso
e ETA, interrompe para erros globais de credencial/configuração e permite coleta
única de todos os resultados. O pull desta análise trouxe o snapshot da falha em
`03_02`; os demais lotes existentes no servidor serão incluídos pela coleta global.

O pré-processamento documental e os documentos técnicos não foram alterados.
As chamadas reais de continuação precisam ocorrer no servidor, onde está o acesso
ao backend Azure.

Validação local: suíte completa com 253 testes executados, 252 aprovados e um
ignorado; 40 entradas documentais conferidas sem API; sintaxe Bash validada.
O hash de implementação do motor documental continua
`386b84f4c71aad15fc7957e93bb6b5b4b087be29957d05fc7936db0b00cadfe7`.

A distinção entre JSON válido, conformidade de formato e correção do conteúdo
também é descrita na [documentação oficial de saídas estruturadas](https://developers.openai.com/api/docs/guides/structured-outputs).
Este reparo mantém o cliente e o modo JSON existentes do gateway privado; não
pressupõe disponibilidade de outra opção de formato nesse deployment.
