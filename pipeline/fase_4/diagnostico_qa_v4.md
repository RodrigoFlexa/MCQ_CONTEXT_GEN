# Diagnóstico da execução QA v4 e correção QA v5

**Histórico:** a proposta QA v5 abaixo foi posteriormente substituída, por decisão do usuário, pela composição de documentos com 10 trechos de cerca de 1.000 palavras. [Executar QA v6](EXECUCAO_QA_V6.md).

## Resultado observado

Artefatos recebidos em `7afc49b`: log, estado, seis pareceres no journal, cinco eventos de recuperação, 239 facetas e suas traduções. A execução interrompeu a preparação no tópico KPI. **Não chegou ao gerador de QA.**

| Indicador | Observado |
|---|---:|
| Facetas planejadas para os 40 subtópicos | 239 |
| Candidatas retidas nas buscas | 45.681 |
| Pedidos lógicos de API | 110 |
| Preparação de facetas/traduções | 60 |
| Embeddings | 36 |
| Auditoria | 8 |
| Refinador de contexto | 6 |
| Pareceres completos registrados | 6 |
| Contextos aprovados nesses pareceres | 0 |
| QA geradas | 0 |
| Tokens de entrada dos papéis LLM | 267.916 |
| Tokens de saída dos papéis LLM | 286.835 |
| Tokens de entrada dos embeddings | 567.827 |

As 45.681 candidatas são entradas por faceta, não documentos distintos. Pedidos lógicos não equivalem necessariamente a tentativas HTTP. Os tokens de saída são os contabilizados pelo backend; não há estimativa de preço ou separação de raciocínio nos arquivos recebidos.

O motivo terminal foi `Auditor devolveu estrutura/evidência inválida duas vezes`. **Não foi entropia, cosine, saturação ou orçamento.** Esses dados ainda não permitem avaliar o comportamento das métricas sobre perguntas.

## Defeitos encontrados

### 1. Confusão entre pertinência e cobertura integral

No parecer `01e50e2f14-f0-context-d0`, o auditor autorizou um trecho, extraiu quatro afirmações e dois alvos, declarou consistência técnica e rejeitou porque o material não cobria a “faceta completa”. No contexto recuperado `01e50e2f14-f0-context-d1-r1`, autorizou dois trechos, duas afirmações e dois alvos, mas voltou a exigir cobertura do subtópico inteiro.

O refinador repetiu a exigência de integrar produção, manutenção, utilidades, offloading, subsea e desempenho empresarial. A faceta virou uma lista de condições que uma fonte deveria satisfazer, quando deveria ser uma orientação temática. Isso desperdiça recortes utilizáveis e incentiva montagens grandes.

**Correção:** a unidade de aprovação passa a ser um alvo profissional sustentado. Cobertura parcial é registrada como limitação. O gerador recebe o recorte aprovado. Não se aprova automaticamente nenhum parecer antigo: pertinência e suporte precisam ser reavaliados.

### 2. Recuperação lexical com pouca proteção contra ruído

Os pareceres descrevem listas de figuras, siglas, referências, glossários, históricos e estudos sem afirmações úteis. O código aceitava uma expressão forte OU duas palavras de apoio e colocava todas na mesma fila. Várias palavras genéricas podiam superar uma expressão distintiva. A etapa semântica só podia ordenar o que essa primeira etapa preservava.

As consultas também eram longas: de 23 a 107 palavras, ainda antes de acrescentar inglês. Elas enumeravam sistemas/interfaces e diluíam o recorte. A instrução herdada mandava produzir uma query “densa” e termos no singular, embora o casamento lexical seja literal.

**Correção:** prompt específico para um recorte estreito e consulta curta; variantes lexicais usuais; capacidade reservada para candidatas com termos distintivos, mantendo candidatas de apoio para recuperação. Exclusão conservadora de páginas estruturais evidentes antes dos embeddings. Não é um detector universal de texto ruim: o auditor continua obrigatório.

### 3. Diversidade aplicada dentro de um contexto sem coerência suficiente

A montagem anterior selecionava até 12 trechos por MMR e os dividia em dois grupos de seis. O MMR premia diversidade, mas não comprova que os trechos formam um núcleo utilizável. Os pareceres mostram montagens com documentos heterogêneos e pouca informação central.

O ranking também usava z-score por conjunto. Isso transforma diferenças relativas em pontuações altas mesmo quando todos os candidatos são fracos; não é uma medida de qualidade absoluta.

**Correção:** até três trechos por contexto. Começa-se pelo trecho mais pertinente e escolhem-se complementos pela relevância e proximidade ao núcleo. O ranking usa cossenos brutos: 85% recorte, 5% aplicação offshore e 10% sinal lexical. Esses pesos são escolhas iniciais, ainda não calibradas com julgamentos humanos. A auditoria decide se há evidência utilizável.

Um contexto continua podendo combinar Petrolês, ANP, HSE, BSEE e REGIS. Uma coleção isolada também é válida. Não há obrigação de mistura nem função fixa por coleção.

### 4. Falha de resposta derrubava toda a preparação

Após duas respostas inválidas, o auditor lançava uma exceção que interrompia todos os tópicos. A tentativa de correção recebia apenas nomes dos erros, sem a resposta anterior. O refinador tinha a mesma limitação de feedback.

**Correção:** resposta anterior e falhas concretas entram no pedido de correção. Duas respostas inválidas isolam aquele contexto como `invalid_response`, sem aprová-lo ou tratá-lo como evidência de falta de conteúdo. O fluxo continua para o próximo. Três falhas consecutivas do auditor ou do refinador interrompem com diagnóstico explícito, para evitar gastar indefinidamente em uma falha sistemática. Erros de API, credenciais e orçamento continuam propagando.

Uma rejeição por conteúdo continua bloqueando o material. Nenhuma barreira factual, de jurisdição ou de autonomia da QA foi removida.

### 5. Faltava informação para investigar a falha terminal

As duas respostas inválidas não estão nos oito arquivos recebidos. Não é possível afirmar qual campo ou citação provocou a interrupção. Um parecer completo registrado, de `f1-d0`, contém `nonliteral_claim_evidence`; isso não identifica a causa das duas respostas terminais.

Também não recebemos o índice completo de candidatas nem os vetores da execução. Portanto, não medimos recall da busca nem demonstramos quanto os novos embeddings melhoraram o ranking. Não há evidência para concluir que o corpus inteiro não tenha conteúdo adequado: a preparação parou no primeiro tópico.

O log também informa uma **instalação parcial dos corpora**. Sem o `install_report.json` do servidor, não sabemos quais downloads ficaram ausentes nem seu efeito sobre KPI. Conferir esse relatório faz parte do piloto; não assumir que todas as fontes descobertas foram instaladas.

**Correção:** salvar entradas originais, todas as respostas de auditoria/refinamento e os erros de validação. Persistir progresso e cobertura durante a preparação.

## Fluxo corrigido

```text
Recorte técnico estreito
  → busca conjunta nos cinco corpora
  → contexto pequeno com núcleo coerente
  → auditoria: quais alvos este material realmente sustenta?
  → se não houver alvo: substituir trechos e reauditar, até duas vezes
  → QA autossuficiente sobre um alvo aprovado
  → Scorer / Refiner / Judge / dificuldade / métricas
```

Mantidos: somente QA; exemplos humanos melhor avaliados; exemplos externos sem alternativas; GPT `gpt-5-4-petrobras`, effort `medium`; exclusivamente `embedding-3-large-global`; dificuldade independente. Cosine, redundância e parada científica continuam observacionais.

A preparação ainda faz a varredura conjunta e audita os tópicos selecionados antes das perguntas. Isso é uma limitação de latência, não corrigida com a troca de prompt. Por isso a primeira validação deve selecionar apenas KPI e cinco QA, em vez de pagar outra preparação completa antes de conferir a qualidade real.

## Validação local

**59 testes offline passaram**, além da compilação dos módulos. As regressões cobrem aprovação parcial com um alvo, preservação de rejeições, citações inválidas inclusive em parecer rejeitado, JSON inválido, confiança não finita, diagnóstico persistido, continuidade após falha isolada, interrupção após falhas consecutivas, capacidade lexical reservada, montagem com complementos coerentes e múltiplos corpora. Os testes anteriores de download/extração, proveniência, cache e embeddings continuam passando.

Clientes Azure e pareceres foram simulados nos testes. Eles demonstram o comportamento do código; **não demonstram melhora factual do GPT na nova seleção**. Isso exige o piloto no servidor. Não foram feitas chamadas pagas ao Azure nesta revisão.

## Próximo passo: piloto de cinco QA em KPI

Depois de publicar estas alterações no GitHub e atualizar o servidor, use os corpora já instalados. Saída nova; não retome QA v4 nem reutilize sua preparação.

```bash
python -u pipeline/fase_4/run_qa.py \
  --corpus-manifest dataset/domain_corpora/manifest.json \
  --deployment gpt-5-4-petrobras \
  --effort medium \
  --embedding-deployment embedding-3-large-global \
  --topics "Gestão do Desempenho Empresarial (KPI)" \
  --limit-per-topic 5 \
  --batch-size 1 \
  --observe-only \
  --max-calls 1000 \
  --output pipeline/fase_4/saida_qa_v5_piloto_kpi
```

Antes das 100 por tópico, conferir: algum contexto e alvo realmente aprovados; ausência de falha sistemática de formato; pertinência e evidências dos contextos aprovados; perguntas respondíveis por conhecimento profissional e respostas tecnicamente corretas. Se não surgir evidência, investigar candidatas e fontes reais; não diminuir os critérios para atingir a meta. Poucas perguntas não bastam para estudar saturação.

Depois do piloto, a coleta completa usa saída `saida_qa_v5_contextos_focados_medium`, `--limit-per-topic 100`, `--batch-size 2`, `--max-calls 10000`, e omite `--topics`. A preparação é refeita para todos os tópicos.

## Arquivos para acompanhar e investigar

- `preparacao_status.json`: estágio, aprovações, rejeições, respostas inválidas e último documento.
- `cobertura_dominio.json`: cobertura concluída por subtópico, atualizada durante a preparação.
- `dominio/contextos_candidatos/<doc_id>.json`: entrada original da auditoria.
- `dominio/auditorias_respostas/<doc_id>.jsonl`: todas as respostas e erros de validação.
- `dominio/auditorias/<doc_id>.json`: parecer final; status distingue rejeição de conteúdo de resposta inválida.
- `dominio/recuperacoes/<base_doc_id>/plano-rN.respostas.jsonl`: respostas do refinador.
- `auditorias_contexto.jsonl` e `recuperacoes_contexto.jsonl`: histórico das decisões.
- `questoes_qa.jsonl`: perguntas aprovadas quando a geração começar.

Prompts efetivos para revisão: [prompts_qa_v5.md](prompts_qa_v5.md). Os resultados e prompts QA v4 permanecem preservados.
