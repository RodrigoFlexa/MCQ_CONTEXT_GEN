# Pesquisa e auditoria dos prompts de pesquisa e documentos

Data: 18/10/2026. Implementação examinada: `a6b7378`. Esta é uma análise de documentação, código e prompts públicos, sem testes, geração ou chamadas aos deployments do projeto. As propostas não substituem automaticamente os prompts publicados.

Atualização posterior à pesquisa: o usuário autorizou a aplicação e o push. A versão `pesquisa-documentos-2` incorpora os [prompts completos revisados](prompts_completos_revisados.md), contexto por papel e perfis uma vez por coleção. A análise abaixo documenta a versão anterior; o primeiro experimento com a revisão será executado pelo usuário no servidor.

## Conclusão

Os prompts atuais expressam preocupações válidas, mas precisam de melhor separação entre tarefa, contexto, critério de qualidade e contrato de saída. Há repetições, instruções que pertencem a outro papel e referências ao histórico do desenvolvimento. Não há evidência para chamá-los de melhores possíveis, nem para concluir, sem resultados, quanto cada defeito afeta o modelo.

“Conhecimento paramétrico” é uma expressão técnica compreensível, mas não define uma verificação observável. O revisor recebe texto e fontes; não recebe uma identificação confiável da origem interna de cada explicação. A tarefa útil é examinar a sustentação de todas as conclusões técnicas importantes, suas condições e a correspondência real das referências.

## O que as fontes primárias mostram

| Fonte examinada | Achado e aplicação |
| --- | --- |
| [OpenAI: prompt engineering](https://developers.openai.com/api/docs/guides/prompt-engineering) | Separar identidade, instruções, exemplos e contexto torna a tarefa mais explícita. Proposta: papel curto, tarefa específica e dados variáveis claramente identificados. |
| [OpenAI: reasoning best practices](https://developers.openai.com/api/docs/guides/reasoning-best-practices) | Recomenda instruções diretas, delimitadores e objetivo claro; pedir raciocínio passo a passo não é necessário para esses modelos. A orientação tem escopo de modelos específico, não é regra universal para todo deployment. |
| [OpenAI: GPT-5 prompting guide](https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_prompting_guide) | Ambiguidades e conflitos entre instruções podem prejudicar o comportamento. Melhorar a hierarquia e a decisão esperada é mais útil do que acrescentar frases enfáticas. |
| [Anthropic: context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) | Recomenda contexto relevante, instruções organizadas e detalhe suficiente sem codificar toda a lógica em regras frágeis. “Mínimo necessário” não significa simplesmente menor número de palavras. |
| [Anthropic: prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices) | Orientações positivas, exemplos pertinentes e separação entre instruções e documentos ajudam a comunicar o resultado esperado. Recomendações específicas para Claude precisam ser avaliadas antes da transferência para outro modelo. |
| [Anthropic: sistema de pesquisa](https://www.anthropic.com/engineering/multi-agent-research-system) | Define responsabilidades, fontes, ferramentas, limites e critérios para encerrar a pesquisa. Precisamos preservar essas decisões, em vez de transformar a pesquisa em uma redação com regras extras. |
| [Anthropic: prompt público do líder](https://github.com/anthropics/claude-cookbooks/blob/main/patterns/agents/prompts/research_lead_agent.md) | O exemplo é extenso e organizado por responsabilidades. Isso contraria a ideia de que um prompt profissional precisa sempre ser curto. Ele contém decisões específicas daquele ambiente e não deve ser copiado integralmente. |
| [LangChain Open Deep Research: prompts reais](https://github.com/langchain-ai/open_deep_research/blob/main/src/open_deep_research/prompts.py) | Separa formulação da investigação, supervisão, pesquisa, consolidação dos achados e relatório. O pesquisador recebe tarefa, ferramentas, orientação de busca e parada; a redação final recebe os achados e o objetivo. As cotas de fontes e instruções de raciocínio desse exemplo não são automaticamente adequadas ao nosso corpus ou modelo. |
| [GPT Researcher: prompts](https://github.com/assafelovic/gpt-researcher/blob/main/gpt_researcher/prompts.py) e [revisor](https://github.com/assafelovic/gpt-researcher/blob/main/multi_agents/agents/reviewer.py) | A pesquisa de consultas e a redação têm instruções próprias. O revisor usa critérios da tarefa e evita ciclos por correções não críticas. Há orientações de opinião e extensão na redação de relatórios que não correspondem ao nosso objetivo de texto didático técnico; não adotar literalmente. |
| [OpenAI: Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs) | JSON válido e aderência a um schema são problemas diferentes. Se o gateway/deployment suportar a funcionalidade, a estrutura pode ser reforçada na API. Isso não garante veracidade, referências corretas ou qualidade do texto. A compatibilidade com o gateway Petrobras não foi verificada nesta pesquisa. |

Esses materiais estabelecem práticas e exemplos, não um ranking universal de prompts. O prompt público de um produto também não é uma garantia de que o sistema em produção inteiro esteja representado ali. Não foram obtidos prompts privados de produtos comerciais.

## Problemas observáveis na implementação atual

| Onde | Problema | Mudança proposta |
| --- | --- | --- |
| `PESQUISAR = BASE + EDITORIAL + ...` | O pesquisador recebe regras sobre parágrafos, citações no capítulo e exclusão de gabaritos antes de decidir a pesquisa. | Manter para ele objetivo de investigação, decisões possíveis, informações faltantes e condição de parada. |
| `BASE` e `EDITORIAL` | Repetem orientações sobre opinião, caso, condições e conhecimento do modelo. | Uma política de evidência curta, com aplicação específica por papel. |
| `REVISAR` | “Especialmente explicações acrescentadas com conhecimento paramétrico” pressupõe uma origem que não é observável no material recebido. | Verificar as conclusões importantes e as condições necessárias, independentemente de como foram produzidas. |
| `REVISAR` | “Não existe nota global nem nove dimensões obrigatórias” carrega a história da v11. | Explicar somente a tarefa e o formato de saída vigente. |
| Blocos de proibições | Acumulam sintomas sem sempre indicar a alternativa desejada. | Descrever o produto esperado e manter proibições essenciais, com uma ação em caso de impedimento. |
| Revisão e refinamento | Falta uma distinção editorial suficientemente direta entre impedimento factual e preferência estilística. | Bloquear por erro/lacuna material; mudanças de estilo ficam como sugestões quando não afetam o objetivo. |
| `Engine.payload()` | Todos os papéis recebem praticamente o mesmo conjunto de contexto e histórico. | Preparar entrada própria para pesquisador, redator, revisor e refinador. Preservar histórico integral no disco. |
| `profiles.annotate()` | O perfil da coleção se repete em cada trecho. | Apresentar cada perfil uma vez e manter coleção/identidade no trecho. Isso requer ajuste da montagem de contexto. |
| `LLMClient.json()` | O modo atual pede `json_object`; aderência aos campos depende do prompt e validador. | Preservar contratos pequenos; considerar schema nativo somente após confirmar compatibilidade do gateway. |

Esses são achados de projeto. Não medem causalmente a influência de cada frase, nem demonstram que um modelo deixou de entender a palavra “paramétrico”.

## Desenho recomendado

1. Uma orientação comum curta: público, domínio e tratamento das fontes como material de consulta.
2. Um objetivo e um critério de conclusão por papel.
3. Instruções positivas e limites essenciais. Condições que o programa pode garantir permanecem no código.
4. Contexto variável separado das instruções: pauta, trechos identificados, pendência atual e espaço de pesquisa restante.
5. Contrato de saída completo e único por caminho, consistente com o validador.
6. Exemplos de decisão pertinentes, em separado, apenas quando ajudarem a distinguir uma falha real. Eles não devem impor o mesmo formato aos capítulos ou perguntas.
7. Revisão por defeitos materiais, com passagens e evidências concretas, sem demanda por exposição do raciocínio interno.

O pesquisador e o redator podem continuar usando o mesmo deployment, com prompts e entradas próprios. Essa separação não exige acrescentar agentes nem multiplicar o custo. O revisor deve poder pedir pesquisa, mas um parecer favorável continua sendo uma decisão automatizada.

## Como avaliar uma revisão futura

Os textos em `prompts_propostos.md` são candidatos de desenho, não versões comprovadamente superiores. Uma comparação posterior no servidor deve manter fontes, pauta e configuração do modelo comparáveis e examinar correção, sustentação, utilidade didática, dependência de caso e esforço gasto. Redução de palavras, fluência ou concordância entre revisores não bastam como medidas de qualidade.

Não foram executados testes ou experimentos, respeitando a orientação anterior do usuário. Após autorização, o código foi atualizado e as instruções agora usam uma nova pasta de saída para separar a revisão das execuções anteriores.
