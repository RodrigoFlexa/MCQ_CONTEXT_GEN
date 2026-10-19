# Análise da execução lexical de Produtos químicos

Base: resultados incorporados no commit `10812bf`, de 19/10/2026. Esta análise
examina o documento, os 16 estados de recorte, as evidências e os registros de
chamadas. Não faz chamadas a modelos, não repete buscas no servidor e não valida
os PDFs originais. Os resultados importados foram preservados.

## Parecer

O experimento produziu material técnico aproveitável sobre **água de injeção,
SRU e desaeração**, com referências internas verificáveis e preservação explícita
de várias condições e limitações. Entretanto, **não entregou cobertura equilibrada
de 2.2. Produtos químicos**. Os nove capítulos publicados pertencem a esse mesmo
nicho. Sete dos oito recortes iniciais ficaram pendentes, inclusive os que
abordavam óleo, água produzida, gás/MEG e armazenamento/manuseio.

Eu trataria o resultado como um piloto de pesquisa sobre água de injeção. Há
potencial para QA qualitativas selecionadas; não há evidência de que o sistema
já consiga gerar um conjunto equilibrado e confiável de QA para o tópico inteiro.
A etapa de QA não foi executada nesta run.

O primeiro problema a resolver não é aumentar o orçamento global: foram reservadas
105 de 500 tentativas. É necessário reduzir as falhas de contrato, recuperar a
cobertura inicial e melhorar a qualidade das fontes para alvos quantitativos.

## O que esta execução efetivamente testou

- Versão registrada: `qa-research-1.0`, implementação atribuída ao commit `5111daa`.
- Busca: SQLite FTS5/BM25 sobre 2.973.683 trechos, conforme o índice registrado.
- Entrada: manifesto dos cinco bancos, marcado como completo naquela instalação.
- Modelos: `gpt-5-4-petrobras:low` em todos os papéis configurados.
- Limites: 8 recortes iniciais, até 16 com descobertas, 32 evidências por recorte,
  três trabalhadores e até três tentativas por chamada lógica.
- Etapa: pesquisa, redação e auditoria de documento. Não houve extração de unidades
  nem geração/avaliação de QA.

**Não é uma avaliação do RAG híbrido, do reranqueamento, dos pacotes portáteis ou
da consulta FTS5 otimizada posteriormente.** Essas mudanças não participaram desta
execução. Também não houve comparação controlada entre modelos ou configurações.

## Resultado medido

| Indicador | Resultado |
|---|---:|
| Recortes iniciais publicados | 1 de 8 |
| Recortes descobertos publicados | 8 de 8 incorporados |
| Recortes totais | 16 |
| Capítulos publicados | 9: seis `auditado_modelo` e três `parcial` |
| Recortes pendentes | 7 |
| Descobertas adicionais não investigadas | 12 |
| Blocos publicados | 74 |
| Palavras dos blocos, sem títulos/lacunas/referências | 9.279 |
| Evidências únicas exportadas, incluindo recortes pendentes | 291 |
| Evidências distintas citadas no documento | 60 |
| Blocos com `<NUMBER>` | 19 de 74 — 25,7% |
| Ocorrências de `<NUMBER>` nos blocos | 61 |
| Evidências citadas contendo `<NUMBER>` | 49 de 60 — 81,7% |
| QA geradas | 0; etapa não executada |

Não interprete nove capítulos como nove assuntos independentes nem 9/16 como uma
porcentagem da cobertura do tópico. Há concentração temática e sobreposição.
O [inventário dos recortes](recortes.md) mostra todos os estados individualmente.

## 1. A cobertura se concentrou em uma única área

Os oito recortes iniciais distribuíam a investigação por diferentes serviços. O
único publicado foi o de condicionamento da água do mar com SRU/desaeração. Os
oito recortes incorporados por descoberta aprofundaram essa mesma área.

| Área inicialmente prevista | Resultado |
|---|---|
| Processamento do óleo: emulsões e espuma | Pendente na pesquisa |
| Água produzida para descarte: compatibilidade | Redação existente; auditoria não concluída |
| Água do mar para injeção: dosagem, SRU e desaeração | Publicado parcialmente |
| Compatibilidade específica de químicos no SRU | Pendente na pesquisa |
| Tratamento do gás: MEG, hidratos e corrosão | Pendente na pesquisa |
| Armazenamento e manuseio | Pendente na pesquisa |
| Monitoramento microbiológico em topside/subsea | Pendente na pesquisa |
| Integração óleo/água/gás e compatibilidade | Redação existente; auditoria não concluída |

Isso não demonstra falta de material sobre as áreas ausentes. O próprio estado do
recorte de óleo registra 11 fontes consideradas pertinentes na última análise
válida, com indícios sobre desemulsificante, antiespumante e monitoramento. O de
gás/MEG registra sete. São avaliações do modelo, não validações humanas, e o
pesquisador também apontou suporte incompleto para as relações mais específicas.
Ainda assim, a ausência desses capítulos não pode ser atribuída apenas ao corpus.

Há dois problemas combinados: pesquisa com suporte parcial para recortes amplos
e falhas que impedem concluir a execução. Não houve um estado final `sem_suporte`
para esses sete recortes; houve `pendente_execucao` por `CallFailed`.

**Recomendação:** garantir uma primeira passagem pelos serviços e decisões do
escopo antes de gastar a capacidade restante em aprofundamentos. A expansão deve
considerar a cobertura ainda ausente e a novidade da relação técnica, além da
existência de um novo título. Recortes iniciais que juntam vários fenômenos e
decisões podem ser decompostos em relações menores sem exigir que uma única fonte
responda a tudo simultaneamente.

## 2. A maior fragilidade operacional está nos contratos de saída

| Papel | Chamadas registradas | Saídas válidas | Saídas inválidas |
|---|---:|---:|---:|
| Planejador | 2 | 1 | 1 |
| Pesquisador | 59 | 24 | 35 |
| Redator | 14 | 14 | 0 |
| Auditor de documento | 28 | 12 | 16 |
| Total | 103 | 51 | 52 |

Todas as 52 falhas registradas são de validação; as 103 respostas terminaram com
`finish=stop`. Não há, nesses registros, evidência de que truncamento por limite
de saída ou falha HTTP tenha sido a causa predominante.

| Primeiro erro registrado na tentativa inválida | Ocorrências |
|---|---:|
| Citação não contígua no texto da evidência | 37 |
| Suporte da auditoria aponta fonte não citada no bloco | 9 |
| Âncora não literal no escopo | 3 |
| Outros erros de schema | 3 |

As tentativas consumiram 3.103.483 tokens de entrada e 374.032 de saída. As
respostas inválidas estão associadas a 1.869.146 tokens de entrada e 217.460 de
saída: aproximadamente 60% dos tokens registrados. Isso não é uma estimativa de
custo financeiro nem significa que toda tentativa de reparo foi inútil: 24 das
45 tentativas marcadas como reparo foram válidas.

### Descobertas opcionais estão bloqueando a tarefa principal

No contrato `research`, citações de suporte e âncoras de escopo são exigidas nas
propostas de **novos recortes**. Das 35 falhas do pesquisador, 31 tiveram como
primeiro erro uma citação não contígua e duas uma âncora não literal. Portanto,
33/35 primeiras falhas reportadas ocorreram em campos de descobertas, e a
validação do objeto inteiro foi rejeitada.

Isso não prova que todo o restante de cada resposta era válido: o validador para
no primeiro erro. Mas identifica um acoplamento desnecessário: uma proposta
opcional de expansão pode impedir a conclusão da pesquisa do recorte atual.
Os registros não incluem aqui as respostas brutas inválidas; não é possível
determinar se cada erro foi paráfrase, tradução, pontuação alterada ou ID incorreto.

**Recomendação prioritária:** validar a avaliação das fontes e a decisão de pesquisa
independentemente das descobertas. Validar/reparar as descobertas em uma etapa
própria, preservando o resultado principal aproveitável. Manter a validação literal.

Para reduzir a cópia defeituosa, o programa pode oferecer trechos contíguos
identificados por IDs e intervalos; o modelo escolhe os IDs, e o programa recupera
o texto exato do original. Isso resolve a integridade literal por construção,
mantendo a auditoria semântica: escolher um trecho existente ainda não prova que
ele sustenta a afirmação.

As nove falhas por fonte não citada no bloco também indicam uma necessidade de
alinhar o prompt do auditor ao contrato. Se houver contraevidência ou indicação
de fonte omitida, ela deve ter campo próprio, distinto do suporte de uma afirmação
aprovada. Não convém simplesmente aceitar qualquer fonte como suporte do bloco.

## 3. O documento contém dados numéricos inutilizáveis

O [capítulo de bissulfito](../../pipeline/qa_research/relatorios/2026-10-19_run_lexical/documento_auditado.md#L178)
preserva relações entre dosagem, oxigênio dissolvido, pH e corrosão. Entretanto,
razão estequiométrica, concentração de solução, dosagem, pressão, tempos e taxas
aparecem repetidamente como `<NUMBER>`.

Essas substituições já existem nos textos de entrada: por exemplo,
`Eade54c6582c8122a` e `Eb1a5ddb56052d6e5`, linhas 93–94 de
[`evidencias.jsonl`](../../pipeline/qa_research/relatorios/2026-10-19_run_lexical/evidencias.jsonl).
A perda não foi criada pela redação desses parágrafos. Com este pacote, não é
possível estabelecer em que etapa anterior os números foram substituídos.

O modelo acertou ao não inventar os números e ao declarar limitações. Contudo,
uma passagem fiel contendo uma dose apagada não é suficiente para uma QA sobre
essa dose. O rótulo `auditado_modelo` não significa prontidão quantitativa.

**Recomendação:** recuperar os originais com números e condições preservados,
incluindo tabelas, quando forem essenciais ao alvo. Registrar a versão original
como evidência própria. Não preencher valores por plausibilidade, estequiometria
de memória ou aproximação do modelo. Embeddings podem ajudar a localizar outra
passagem, mas não recuperam um número ausente do texto indexado.

Não é necessário descartar toda evidência que contenha `<NUMBER>`. Algumas relações
qualitativas permanecem sustentadas. A elegibilidade deve ser decidida por
proposição/alvo: um valor essencial ausente bloqueia aquela QA; um mecanismo
independente do valor pode continuar aproveitável.

## 4. Há redundância na expansão

Dois capítulos tratam praticamente da mesma relação:

- [Desaeração por membranas pode reduzir ou dispensar scavenger](../../pipeline/qa_research/relatorios/2026-10-19_run_lexical/documento_auditado.md#L128).
- [Desaeração por membranas pode reduzir ou eliminar sequestrante](../../pipeline/qa_research/relatorios/2026-10-19_run_lexical/documento_auditado.md#L231).

O primeiro cita cinco evidências; o segundo cita três, todas presentes no primeiro.
Os parágrafos iniciais defendem a mesma possibilidade condicionada a projeto
adequado. Isso não permite afirmar duplicação de cada frase, mas é evidência
suficiente para propor fusão dos capítulos ou diferenciação explícita de objetivos.

O identificador de recorte atual deriva de três campos textuais:
serviço, fenômeno/produto e decisão. Variações como `seleção` e `seleção e dosagem`
permitem novas chaves para relações semanticamente muito próximas.

**Recomendação:** consolidar por relação técnica, condições e evidências antes de
reservar um novo recorte. Novidade de redação ou título não equivale a novo
conhecimento. A mesma verificação continua necessária depois, nas unidades de QA.

## 5. A lista de lacunas mistura histórico e pendências atuais

No [capítulo sobre URS e CaCO3](../../pipeline/qa_research/relatorios/2026-10-19_run_lexical/documento_auditado.md#L396),
o texto relata o caso operacional de dosagem contínua de inibidor de CaCO3 com URS,
citando `E23ea2451eb21e9a4`. Na lista de lacunas do próprio capítulo, permanece
um pedido antigo de evidência literal dessa dosagem no cenário com URS.

Também permanece uma crítica ao bloco B003 da primeira versão, apesar de ter
havido reescrita e aprovação da versão seguinte. Como os IDs por posição são
reutilizados, essa crítica pode parecer referir-se ao bloco atual.

O código acumula lacunas das rodadas de pesquisa, dos pareceres e da redação,
sem uma etapa de resolução que feche as já atendidas. O resultado é uma lista
historicamente informativa, mas inconsistente como retrato das pendências finais.

**Recomendação:** cada lacuna deve ter ID, versão de origem e estado atual:
aberta, parcialmente resolvida, resolvida ou não investigada. O documento final
mostra as atuais; o histórico completo permanece no registro da execução.

## 6. A rastreabilidade computacional funcionou; a bibliográfica é limitada

As 291 evidências exportadas têm os hashes e IDs de texto coerentes. Os nove
capítulos publicados passaram novamente nas verificações estruturais atuais de
fonte, auditoria e correspondência com a versão publicada. Isso é um resultado
positivo do mecanismo de integridade.

Há também exemplos de auditoria útil: no capítulo de breakthrough, a última
auditoria reprovou dois blocos que ligavam o material a conclusões não plenamente
sustentadas pelas fontes citadas. Eles não entraram no capítulo publicado.

Isso não equivale à validação científica humana das 74 passagens. `14/14` saídas
válidas do redator significa conformidade estrutural, não 14 capítulos
semanticamente corretos sem necessidade de revisão.

Das 60 evidências citadas:

- 52 são do Petrolês, extraídas de dois TXT concatenados sem fronteiras conhecidas
  dos documentos originais;
- oito são de quatro documentos identificados da coleção REGIS;
- nenhuma tem página original identificada em `page_ini`;
- não há evidências ANP, HSE ou BSEE citadas nos blocos publicados.

Isso não torna uma fonte de outro banco automaticamente melhor. Também não prova
que os outros bancos tenham evidência pertinente para cada recorte. Mostra que
consultar um índice com cinco coleções não implica obter suporte final diverso.
As 60 evidências são trechos, não 60 estudos independentes. Para a maior parte,
o pacote não permite confirmar precisamente o tipo de documento original.

Há ainda um problema de metadados: `Ec72c582780cd2ad5` contém texto em inglês,
mas está marcado com `language=pt`. O rótulo foi herdado do TXT; não pode ser usado
sozinho para medir diversidade de idiomas ou aplicar filtros linguísticos.

**Recomendação:** reconstruir identidade do documento, título, data, tipo de fonte
e localização, sempre que possível. Preservar as limitações quando isso não for
possível. Para decisões de dose e compatibilidade, priorizar evidência com as
condições do ensaio/processo recuperáveis, independentemente de idioma ou de a
fonte ser tese, artigo ou documento técnico.

## 7. Tempo: há indícios de gargalo fora das chamadas, mas falta medir cada etapa

As 103 chamadas registram 4.130,65 segundos somados, cerca de 68,8 minutos.
Esse total não é tempo de parede, pois há trabalhadores concorrentes.

Na janela observável da retomada, entre o primeiro evento de modelo às 11:48:43
e a última resposta às 15:08:24, passaram-se aproximadamente 199,7 minutos. A
união aproximada dos intervalos de chamada cobre 60,6 minutos; aproximadamente
139,1 minutos não têm chamada registrada em execução. Há intervalos sem chamadas
de cerca de 21,5 e 19,3 minutos.

Esses números são reconstruídos pelo horário de log de conclusão menos `seconds`.
Não incluem necessariamente a inicialização antes do primeiro evento nem a
exportação final. Não são um perfil de CPU, disco ou SQLite.

O relatório humano atribui o restante a BM25/I/O. É uma hipótese consistente com
a consulta antiga e com os intervalos, mas os arquivos não registram a duração
de cada busca. Portanto, não permitem atribuir com precisão esses 139 minutos
ao SQLite, separar espera, disco, preparação e outras atividades, ou prever a
aceleração da próxima run.

**Recomendação:** registrar por consulta o tempo de BM25, embedding da consulta,
FAISS, reranqueamento, leituras de texto e total, além de candidatos e fontes
adicionadas. Medir a consulta otimizada no índice real. A preparação portátil
elimina reconstrução no servidor, mas não elimina a latência de pesquisa e auditoria.

## 8. A execução encerrou com pendências

`interrupcao=null` indica que não foi registrada uma interrupção global. Ao mesmo
tempo, `pendencias_execucao=true` e sete estados `pendente_execucao` indicam que a
pesquisa não foi concluída em todos os recortes. A CLI dessa versão retorna código
2 quando há pendências, embora o shell que a lançou não tenha registrado aqui
seu código de saída observado.

Durante uma passagem de `research()`, cada recorte é acrescentado ao conjunto de
processados mesmo quando retorna pendente. Ele não é automaticamente tentado outra
vez nessa mesma passagem. Uma retomada pode reaproveitar os resultados concluídos,
mas repetir o mesmo contrato defeituoso também pode repetir o problema.

O orçamento registra 105 reservas e o arquivo de chamadas contém 103 registros.
A diferença de duas reservas não tem explicação conclusiva nos artefatos. Pode
haver relação com a primeira tentativa interrompida, mas isso não está provado.

## Prioridades para a próxima execução

1. **Desacoplar descobertas opcionais da pesquisa principal.** Preservar as análises
   válidas e corrigir citações com seleção de trechos identificados, sem relaxar
   a exigência de suporte literal e semântico.
2. **Recuperar os sete recortes pendentes e proteger a cobertura por serviço.**
   Reaproveitar as 291 evidências e os estados existentes, em vez de reiniciar
   indiscriminadamente. Uma migração para código novo precisa respeitar a
   identidade de implementação/configuração da saída antiga.
3. **Consolidar capítulos próximos e reconciliar lacunas.** Separar histórico de
   pendência atual e impedir que assuntos semelhantes ocupem a expansão inteira.
4. **Recuperar fontes quantitativas utilizáveis.** Manter alvos qualitativos
   independentes dos números; bloquear alvos que dependam de valores apagados.
5. **Medir recuperação híbrida e desempenho.** Usar evidências de controle internas
   distribuídas pelos serviços, sem inserir datasets externos ou QA de exemplo
   nos prompts. Comparar cobertura, suporte recuperado e latência por etapa.
6. **Só então ampliar QA.** Um piloto qualitativo delimitado em água de injeção
   pode começar antes, após revisar as proposições e seus alvos. Ele não deve ser
   apresentado como cobertura integral de Produtos químicos.

## Observação sobre os arquivos no Windows

O Git armazena, na mesma pasta, `RELATORIO.md` e `relatorio.md`. Um é o relatório
humano; o outro, o resumo automático. No checkout Windows desta sessão, o conteúdo
local corresponde ao arquivo automático, e o relatório humano aparece como
modificado por essa colisão de nomes. Li o relatório humano diretamente do objeto
Git, sem sobrescrever os arquivos locais.

Uma próxima organização dos artefatos deve usar nomes distintos além da caixa,
por exemplo `relatorio_servidor.md` e `resumo_execucao.md`.

## Dados auxiliares

- [Métricas calculadas e método](metricas.json).
- [Todos os recortes, estados e contagens](recortes.md).
- [Resumo original da execução](../../pipeline/qa_research/relatorios/2026-10-19_run_lexical/resumo.json).
- [Documento gerado](../../pipeline/qa_research/relatorios/2026-10-19_run_lexical/documento_auditado.md).
