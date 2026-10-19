# Ajustes aplicados após a análise da execução lexical

O fluxo recomendado passou a ser a pesquisa documental distribuída v2, descrita
em [DOCUMENTO_DISTRIBUIDO.md](../../pipeline/qa_research/DOCUMENTO_DISTRIBUIDO.md).
O notebook [documento_produtos_quimicos.ipynb](../../pipeline/qa_research/documento_produtos_quimicos.ipynb)
inspeciona o pacote e os resultados. O fluxo anterior foi preservado para comparação
e desenvolvimento futuro da fase de QA; ele não é executado pela entrada documental v2.

| Problema observado | Correção implementada |
|---|---|
| Sete recortes originais pendentes, descobertas concentradas em água | 12 focos explícitos do escopo; primeira rodada para todos antes de aprofundar; descobertas não criam capítulos automaticamente |
| Erro de descoberta descartava a pesquisa principal | Classificação principal persistida; achados auxiliares validados individualmente; descoberta em chamada posterior opcional |
| Citações copiadas pelo modelo falhavam na correspondência | IDs de intervalos pré-calculados; texto da prova resolvido diretamente do original |
| Referência proposta pelo redator podia ser inadequada | Auditor vê os originais e pode selecionar outro trecho visível; suporte e contraevidência separados |
| Parecer antigo associado a novo texto | IDs com versão; revisão altera somente blocos reprovados; selo liga texto, parecer e hashes dos originais |
| Blocos finais com números apagados | Marcadores proibidos no corpo; números não são reconstruídos; guarda de valores/unidades e auditoria semântica |
| Lacunas antigas mantidas após serem atendidas | Reconciliação com blocos atuais e suas provas; abertas, parciais, resolvidas e não reavaliadas são estados distintos |
| Capítulos quase equivalentes | Comparação de possíveis duplicatas após aprovação; exige mesma relação e mesmas condições, sem reescrever o texto admitido |
| Muito processamento local no servidor | Leitura, triagem lexical, embeddings E5 de candidatos e fusão RRF nesta máquina; pacote de textos pronto no Git |
| Termos gerais recuperavam material sem relação com a aplicação | Contextos por recorte, exclusões explícitas para homônimos e filtro de catálogos/listas bibliográficas reconhecíveis |
| Lentidão entre fases de chamadas | Papéis concorrentes, com um teto global de chamadas Azure, sem multiplicar o limite nos auditores internos |
| Falha isolada interrompia a publicação útil | Checkpoints por etapa/bloco; exportação parcial de aprovados e estado explícito das pendências |
| Retorno dos resultados dependia de copiar arquivos manualmente | Coletor com lista de arquivos permitidos e manifesto de hashes; comandos de add/commit/push documentados |
| Dois relatórios com nomes incompatíveis no Windows | Relatório humano preservado como `relatorio_servidor.md`; relatório automático permanece `relatorio.md` |
| Hashes poderiam mudar entre Windows e Linux | Atributos Git preservam bytes dos pacotes e snapshots; assinatura de código normaliza as quebras de linha |

O perfil local evita calcular embeddings sobre todas as janelas: mantém até 64
candidatos lexicais por foco, usa o E5 na união desses candidatos e seleciona até
36 passagens por foco. O pesquisador pode ler novas passagens dentro do catálogo,
mas não faz busca no corpus integral do servidor. Pedidos fora do pacote voltam
em `pedidos_busca.json` para nova preparação aqui.

Essa opção reduz custo no servidor e torna a execução independente dos bancos
brutos. Também limita o alcance: fontes que a preparação não selecionou precisam
de outra rodada local. Não se demonstra exaustividade, recall completo ou superioridade
do E5 em relação aos embeddings Azure sem uma avaliação controlada.

Os fundamentos científicos e as adaptações de engenharia estão no
[plano metodológico, seção 9](../plano_qa_research.md#9-fundamentos-da-literatura-e-adaptações-nossas).
O encadeamento em pacote offline, a grade fixa e as regras de retomada são decisões
do projeto, motivadas pelos resultados e pela separação das duas máquinas.

A validação de software usa modelos simulados para conferir contratos, rejeições,
retomada, concorrência e publicação. A preparação temática usa o E5 real em cache,
sem chamadas Azure. A qualidade científica das novas sínteses precisará ser avaliada
com o documento que será gerado no servidor; os testes não substituem essa avaliação.

## Pacote preparado e verificado

O pacote entregue contém 352 passagens únicas e 1.399 intervalos de citação,
com cerca de 1,52 MB. Foram examinadas 596.301 janelas dos materiais locais;
710 candidatos passaram à etapa de embeddings após os filtros finais. Cada um
dos 12 recortes tem um catálogo de até 36 passagens; uma passagem pode pertencer
a mais de um catálogo. As contagens não representam estudos independentes.

Há 324 passagens Petroles, 27 REGIS e uma BSEE. Apenas nove preservam identificação
de fronteira documental segundo os metadados existentes; 313 têm números apagados
no texto. Esses limites reforçam a necessidade de manter as condições dos achados
e explicitar lacunas quantitativas. A seleção não representa os cinco bancos completos.

Foram aprovados 170 testes da pesquisa QA/documental e 107 do inventário, incluindo
a infraestrutura compartilhada. O notebook foi validado e todas as suas células
foram executadas localmente sem chamadas Azure. Os números e a assinatura do pacote
estão em [preparo_local_v2.json](preparo_local_v2.json).
