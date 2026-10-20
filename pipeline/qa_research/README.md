# Pesquisa no corpus → documento auditado → QA curta

**Para gerar um lote de 9 QA a partir de um documento pronto,
use [QA_LOTE_9.md](QA_LOTE_9.md).** Planejamento e geração usam
`gpt-5-4-petrobras:high`; verificação e refinamento usam
`gpt-5-4-petrobras:low`. Essa etapa é independente da pesquisa documental abaixo.

Os 40 contextos revisados estão na [versão final para QA](relatorios/dez_areas_final_v1/INDICE.md),
com [registro editorial separado](relatorios/dez_areas_final_v1/REVISAO.md).

**Para as dez áreas (40 frases), use [DEZ_AREAS.md](DEZ_AREAS.md).** Os perfis têm
217 recortes definidos manualmente; a preparação local compartilha uma única
varredura e um E5 com GPU. No servidor:
`bash pipeline/qa_research/rodar_documentos_10_areas.sh`.

**Para a próxima execução de Produtos químicos, use a [síntese técnica autônoma v3](DOCUMENTO_DISTRIBUIDO.md)**
e o notebook `documento_produtos_quimicos.ipynb`. O pacote já preparado localmente
acompanha o Git; no servidor rodam somente as chamadas Azure e a coordenação do
documento. Execute `bash pipeline/qa_research/rodar_documento_v3.sh` no servidor.
O pré-processamento e o pacote v2 são preservados. O produto passa a ensinar o
assunto com explicações técnicas complementares auditadas, sem referências nem
comentários sobre fontes no documento. As instruções abaixo descrevem o fluxo anterior, que também possui QA.

Implementação nova para geração de **pergunta e resposta**, sem alternativas de
múltipla escolha, datasets externos ou questões de exemplo nos prompts. A API e o
notebook usam o mesmo motor; o notebook é a entrada recomendada para acompanhar as etapas.

Abra `pesquisa_e_qa.ipynb`. O plano metodológico está em
[`docs/plano_qa_research.md`](../../docs/plano_qa_research.md).
Para gerar somente o documento de Produtos químicos no servidor, use
[`SERVIDOR.md`](SERVIDOR.md).

## Caminho implementado

1. Planejador extrai eixos de serviço, fenômeno/produto e decisão do tópico. Propõe
   recortes investigáveis com âncoras literais no escopo e consultas PT/EN.
2. Pesquisadores investigam recortes em paralelo, avaliam a pertinência e o estatuto
   dos textos, refinam consultas e propõem recortes novos com evidência literal.
   O coordenador admite descobertas até o limite e registra as restantes.
3. Redator escreve capítulos amplos, com blocos ligados às passagens originais.
   Auditor independente verifica suporte, condições, escopo, atribuições e tradução.
   Uma revisão pode pesquisar lacunas antes de reescrever. Só blocos aprovados são publicados.
4. Extrator decompõe o documento admitido em unidades de conhecimento e escolhe
   um alvo de resposta curta **antes** de formular uma pergunta. Outra auditoria
   filtra fidelidade, atomicidade, contexto e determinação do alvo.
5. Autor gera uma pergunta fechada por unidade elegível. Respondente recebe pergunta
   e evidências, sem gabarito/variantes/unidade-alvo. Uma busca adicional pode trazer
   contraevidência. Auditor adversarial verifica alternativas válidas e equivalência.
6. Exportação aceita somente a cadeia aprovada. Falhas, ambiguidades e falta de suporte
   ficam registradas; não se afrouxam filtros para cumprir a meta. Rodízio entre recortes
   e comparação de unidades reduzem concentração temática e repetição.

Papéis são chamadas separadas com contexto próprio; podem usar o mesmo deployment ou
deployments diferentes em `models`. Isso não demonstra independência estatística dos erros.

## Executar

Na raiz do repositório, com Python 3.10+ e as dependências existentes:

```powershell
python -m pipeline.qa_research.run --config pipeline/qa_research/configs/piloto_produtos_quimicos.json --plan
python -m pipeline.qa_research.run --config pipeline/qa_research/configs/piloto_produtos_quimicos.json --stage pesquisa
python -m pipeline.qa_research.run --config pipeline/qa_research/configs/piloto_produtos_quimicos.json --stage qa
```

`--plan` não cria clientes, não lê credenciais, não faz chamadas, não baixa documentos
e não indexa. Os recortes dependem do planejador e aparecem após executar pesquisa.
`--stage completo` executa as duas fases. O perfil maior é `configs/produtos_quimicos.json`.
O piloto limita a investigação a dois recortes: **não** pretende cobrir todo o tópico.
`--manifest caminho/manifest.json` seleciona o corpus completo já instalado sem editar
o JSON de configuração; o argumento tem prioridade sobre o campo `manifest` do arquivo.

As credenciais e o cliente JSON com cache/reparo vêm da infraestrutura Azure/OpenAI
já existente em `pipeline/inventario/llm.py`. Os defaults de deployment reaproveitam
nomes do projeto, não representam detecção de disponibilidade na conta. Altere `models`
se necessário, configurando todos os papéis de `config.ROLES` como `deployment:effort`.

## Corpus e limites da busca

Com `manifest`, o pipeline verifica hashes e utiliza o corpus completo declarado pelo
manifesto existente. Sem manifesto, indexa somente textos originais em `selecao.json`
nas `origins` e declara **cobertura parcial**. Não indexa notas, fatos extraídos,
documentos gerados ou perguntas como fontes primárias. O manifesto tem prioridade
sobre as seleções; versões antigas não se misturam à coleção verificada.

O padrão agora é **BM25 + embeddings Azure text-embedding-3-large + FAISS + fusão RRF
e reranqueamento por LLM**. O deployment de embeddings é `embedding-3-large-global`
com 3.072 dimensões, já utilizado no projeto. O perfil maior recupera até 80 candidatos
de cada canal, reranqueia 50 e entrega até oito principais por consulta. A preparação
vetorial é persistente e reutilizada. Consulte [`HIBRIDA.md`](HIBRIDA.md) para cache,
limites, orçamento e avaliação. O modo `bm25` fica disponível explicitamente como controle.
Vizinhos só são incorporados com limites documentais conhecidos. TXT concatenado não
recebe páginas ou fronteiras inventadas.

Teses, dissertações e documentos estrangeiros permanecem consultáveis. O filtro é
por afirmação: resultado experimental conserva condições; opinião/hipótese não vira
QA factual; norma sem edição/jurisdição documentadas não é elegível. O idioma pode
ser traduzido para compreensão, mas a evidência literal continua no original.

## Saídas e retomada

- `plano.json`: eixos, recortes, origem das descobertas e expansões não investigadas.
- `recortes/`: buscas, fontes, avaliações, versões de capítulo e auditorias.
- `documento_auditado.md` e `documento.json`: blocos admitidos, referências e lacunas.
- `evidencias.jsonl`: textos originais, hashes e metadados disponíveis.
- `unidades.jsonl`: proposições, condições, alvos e resultados da auditoria.
- `qa.csv`: apenas `pergunta,resposta` para itens aprovados pelo modelo.
- `qa_aprovadas.jsonl`: QA com cadeia de evidências e pareceres.
- `qa_nao_aprovadas.jsonl`: rejeições, redundância e pendências.
- `cobertura.json`, `resumo.json`, `relatorio.md`: alcance e limitações da execução.
- `chamadas/`: prompts, entradas e saídas por chamada; material para auditoria.
- `orcamento.json`: tentativas reservadas cumulativamente, inclusive reparos.
- `recuperacoes/`: canais lexical/vetorial, fusão e decisões do reranqueador.
- `chamadas_embeddings.jsonl` e `orcamento_embeddings.json`: uso e orçamento dos embeddings.

Repita o mesmo comando para retomar a mesma saída. Configuração, corpus e implementação
são vinculados por assinatura; mudança material exige uma nova pasta. Pode aumentar
`max_calls` ou mudar `workers` sem invalidar a identidade. Não execute simultaneamente
duas instâncias na mesma saída. Cada índice fixa seu snapshot de corpus.
O orçamento `embedding_max_calls` também pode aumentar na retomada. `--stage indice`
prepara apenas os índices; `--stage pesquisa` os prepara/reutiliza e gera o documento.

Interrupção por orçamento e pendência de execução retornam código 2. Não atingir a meta
por falta de unidades aprováveis é registrado no resumo, sem fabricar itens. Os estados
`auditado_modelo` e `aprovada_modelo` não significam validação humana.

## Preparação fora do servidor

Use `--pack` para reutilizar textos, proveniência, BM25 e FAISS sem repetir
fragmentação ou embeddings dos documentos no servidor. A preparação pode conservar
todo o acervo ou aplicar triagem opcional BM25 + E5 local antes do Azure.
Comandos e transferência: [`PREPROCESSAMENTO.md`](PREPROCESSAMENTO.md).
Os pacotes de dados ficam separados do Git. Um pacote só lexical exige finalização
explícita antes de uma pesquisa híbrida.

## Verificação

```powershell
python -m unittest discover -s pipeline/qa_research/tests -v
```

Os testes usam corpus temporário e clientes simulados. Verificam recuperação,
proveniência, contratos, isolamento do gabarito, bloqueio de itens reprovados, orçamento
e retomada. Não substituem um piloto com os modelos e revisão técnica humana.

O desenho adapta extração contextual de [Claimify](https://aclanthology.org/2025.acl-long.348/),
evidência científica de [SciFact](https://aclanthology.org/2020.emnlp-main.609/), extração
atômica de [AIM-SciQA](https://arxiv.org/html/2603.14257v1) e pesquisa com feedback de
[OpenScholar](https://www.nature.com/articles/s41586-025-10072-4). A composição e os
critérios de QA curta são decisões deste projeto, não uma reprodução desses métodos.
