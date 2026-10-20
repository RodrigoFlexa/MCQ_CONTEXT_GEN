# Revisão manual do segundo piloto de QA — Produtos químicos

Data: 20/10/2026. Revisão do assistente nesta conversa, por leitura das nove questões, planejamento, duas auditorias e blocos técnicos de suporte. Sem nova chamada ao backend.

Snapshot: `relatorios/qa_lote_9_02_02_20261020T162624575988Z/`, importado no commit `ddcb871`. Motor: `qa-batch-v2`.

## Decisão para os 40 subtópicos

É razoável avançar com a geração inicial dos 40 subtópicos, mantendo os resultados como candidatos para revisão. O segundo piloto demonstra funcionamento do fluxo e uma correção de ambiguidade, mas não comprova que a classificação automática das três difíceis esteja correta.

O conjunto não deve ser tratado como banco final de nove questões já certificadas. Os ajustes restantes se concentram em delimitação da demanda, dificuldade e força das conclusões. A geração dos demais temas permitirá avaliar a recorrência desses problemas em domínios diferentes.

Esta análise não muda prompts, configuração, contexto ou implementação. Os checkpoints do segundo piloto podem ser retomados com a mesma versão. Os arquivos originais das duas execuções foram preservados.

## Verificações da execução

- Nove questões, com distribuição declarada de três por dificuldade.
- Respostas entre 17 e 30 palavras; todas abaixo do limite de 50.
- Duração registrada: **301,86 segundos**, aproximadamente **5 minutos e 2 segundos**.
- **Nove tentativas**, correspondentes a sete respostas de etapas aceitas e duas retentativas de validação de passagens literais.
- Uma rodada de refinamento, somente na questão 9.
- Os **22 arquivos** do manifesto têm os hashes esperados; o hash semântico do lote corresponde ao resumo.
- Contratos do plano, questões e duas auditorias validados com o código atual.
- Primeira auditoria rejeitou o ID 9; segunda auditoria não rejeitou itens.
- Mesmo contexto técnico do primeiro piloto: `bbc680adb05037e9c1c3b030844bca39b98a73e945d42262d4684ccfe59ab1af`.

A seleção dos alvos mudou entre os pilotos. Há melhorias pontuais observáveis, mas as execuções não constituem uma comparação controlada das mesmas nove perguntas nem permitem estimar uma taxa geral de melhora.

## Avaliação de cada questão

| ID | Assunto | Avaliação manual |
|---|---|---|
| 1 | Uso do bottle test | Conteúdo sustentado, mas a pergunta “Como é usado” convida a descrever método, finalidade e controles. Estreitar para a finalidade do teste deixa o item fácil mais objetivo. |
| 2 | Finalidade da URS | Aproveitável: demanda delimitada e gabarito coerente. A enumeração de sais/cátions não precisa ser obrigatória para aceitar uma resposta equivalente. |
| 3 | Mecanismo do MEG | Aproveitável como recordação de conceito. “Condições mais severas” pode ser explicado com maior precisão, mas o núcleo termodinâmico está correto no contexto. |
| 4 | Menor oxigênio residual e bissulfito | Bom item médio: explicita comparação equivalente e pede uma única direção de mudança. |
| 5 | Cisalhamento e antiespumante | Aproveitável como médio. A consequência é coerente com o mecanismo descrito; o gabarito usa “tende” e “pode”, sem impor uma resposta universal à aplicação. |
| 6 | Superdosagem antes da flotação | Ajustar o foco. “Qual consequência isso pode trazer?” admite vários efeitos diferentes e o gabarito enumera três mecanismos. Pedir o efeito sobre a eficiência de remoção delimita melhor a resposta. |
| 7 | Mudança do fluido e formulação do antiespumante | Mais delimitada que a questão de antiespumante do primeiro piloto. A revisão da formulação é uma conclusão operacional plausível; não equivale a comprovar inadequação do produto. Enunciado genérico e classificação difícil ainda merecem revisão. |
| 8 | MEG e precipitação na recuperação | Mecanismo sustentado, mas a dificuldade permanece limítrofe: concentração de glicol, remoção de água e precipitados já aproximam diretamente o candidato da resposta. O enunciado não demonstra que duas inferências sejam necessárias. |
| 9 | Contagens planctônicas e biofilme | O refinamento melhorou o suporte para discutir a superfície interna. Permanecem ressalvas sobre atividade microbiana, causalidade da corrosão, diagnóstico de limitação de contato e dificuldade. |

## Melhoria observada na questão 9

Na primeira versão, a pergunta apresentava baixa contagem planctônica, corrosão localizada, sulfeto e depósitos, sem confirmação de população aderida. A auditoria identificou uma conclusão concorrente: corrosão sob depósito sem demonstração suficiente de biofilme remanescente. O refinamento acrescentou confirmação de biofilme na superfície interna.

Esse é um avanço concreto na explicitação de condições. Contudo, confirmar a presença de biofilme não comprova, por si só, atividade microbiana após o tratamento nem que a corrosão seja microbiologicamente influenciada. O próprio documento estabelece que a presença de bactérias, isoladamente, não demonstra a causa de um ataque corrosivo.

O gabarito final é mais cuidadoso ao dizer que a queda planctônica não comprova controle na superfície. Essa é a parte mais sólida do item. A afirmação anterior de limitação de contato/penetração continua sendo uma explicação plausível, sem uma medida que a isole das demais limitações do tratamento.

Além disso, o enunciado já nomeia biofilme aderido sob depósito. Relacionar essa condição à proteção da população séssil pode exigir apenas uma inferência, contrariando a dificuldade declarada. Uma opção editorial é aproveitar o conteúdo como questão média sobre a diferença entre monitoramento da água e controle na superfície, sem afirmar uma causa única de corrosão.

## Limite da nova auditoria estruturada

O código confirma que a condição discriminante citada pertence à pergunta. A exclusão lógica da alternativa continua sendo uma avaliação do modelo.

Na questão 8, a auditoria final considerou a hipótese de deposição por sólidos ou hidrocarbonetos e citou como exclusão a maior concentração de glicol/remoção de água. Essa condição favorece o mecanismo salino proposto, mas não exclui logicamente o carregamento de outros materiais. Na questão 9, a presença de biofilme também não exclui corrosão não microbiológica coexistente.

Assim, um campo preenchido com uma passagem real não é prova suficiente de unicidade. Esse ponto deve continuar na revisão posterior dos lotes, especialmente dos difíceis.

## Ajustes editoriais simples para este lote

1. **Questão 1:** perguntar a finalidade do bottle test, com gabarito centrado na comparação de produtos e dosagens em condições controladas. A lista de variáveis não precisa integrar a resposta essencial.
2. **Questão 6:** perguntar especificamente a consequência sobre a eficiência de remoção por flotação. O gabarito pode se limitar a que a superdosagem pode reduzir essa eficiência; não exigir três mecanismos possíveis.
3. **Questão 7:** delimitar a demanda ao aspecto do programa químico a reavaliar e preservar a distinção entre investigar formulação e comprovar que ela seja a causa.
4. **Questões 8 e 9:** revisar a dificuldade antes de usá-las como itens difíceis finais. Não aumentar a extensão nem acrescentar pistas para aparentar maior exigência.

Não foi publicada uma versão substituta com esses ajustes. O snapshot permanece como registro fiel do que o pipeline gerou.

## Execução dos demais temas

Usar a versão atual com um lote por item do programa: 40 subtópicos, meta de 360 questões. A quantidade publicada pode ser menor se alguns lotes ficarem pendentes na verificação. A aprovação automática continua registrada como `aprovado_modelo`, com validação humana pendente.

O processamento usa os documentos finais existentes. Não precisa refazer indexação, embeddings ou pesquisa documental. Cada item mantém saída e checkpoints próprios em `saida_qa_lote_9_final_v2/ID/`.

As duas falhas de citação literal foram corrigidas pelas retentativas existentes. Este piloto não indica necessidade de relaxar a validação ou refazer o pré-processamento. A velocidade observada é uma referência de uma execução, não uma previsão garantida para os 40 temas.
