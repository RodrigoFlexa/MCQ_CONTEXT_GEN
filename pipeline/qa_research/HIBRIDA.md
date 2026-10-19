# Recuperação híbrida para o levantamento de contexto

Versão `qa-research-1.1-hybrid`. Os perfis de Produtos químicos agora habilitam a
recuperação híbrida e usam novas pastas de saída, sem misturar checkpoints da versão BM25.

## Caminho da consulta

1. BM25 recupera até 80 trechos por correspondência lexical.
2. A mesma consulta é representada por `text-embedding-3-large`, via deployment
   Azure `embedding-3-large-global`, em 3.072 dimensões. FAISS recupera até 80 candidatos
   por produto interno dos vetores normalizados.
3. Duplicatas são unidas pelo hash do conteúdo. Reciprocal Rank Fusion soma
   `1 / (60 + posição)` de cada canal. Pontuações BM25 e vetoriais não são somadas
   diretamente, pois têm escalas diferentes.
4. Os primeiros 50 candidatos da fusão são avaliados pelo papel `reranqueador`.
   Ele usa o deployment de linguagem configurado, por padrão `gpt-5-4-petrobras:low`.
   Este é **reranqueamento por LLM**, não um cross-encoder local nem o semantic ranker
   gerenciado do Azure AI Search. Não exige provisionar Azure AI Search.
5. O reranqueador recebe consulta, tópico/recorte, textos originais e metadados.
   Pontua todos: 0 irrelevante, 1 contexto útil, 2 parcial, 3 diretamente pertinente.
   Deve preservar contraevidências, exceções e material complementar. Empates usam
   a posição da fusão; score 0 não entra no contexto.
6. O perfil maior entrega até oito trechos principais por consulta, com até três
   do mesmo documento conhecido, e acrescenta vizinhos quando as fronteiras são
   conhecidas. TXT concatenado não é tratado como um único artigo para essa cota.
   O limite acumulado é 64 evidências por recorte, incluindo vizinhos.

O pesquisador continua examinando os resultados e refinando consultas em português
e inglês. O auditor continua verificando conteúdo. Recuperação/reranqueamento
medem pertinência: não certificam que uma afirmação é verdadeira ou aplicável ao FPSO.

## Preparação e cache

O corpo original é a entrada do embedding. Textos que excederem 8.191 tokens são
divididos em janelas com sobreposição; nenhuma cauda é truncada. Seus vetores são
agregados por média ponderada dos tokens novos e normalizados. Os lotes têm até 64
entradas e 60.000 tokens. O tokenizer público `cl100k_base` usa o preparador já
existente do projeto, com verificação de hash e suporte ao certificado corporativo.

O cache SQLite é separado por endpoint, versão da API, modelo, deployment, versão
declarada, dimensões e protocolo de tokenização/agregação. Dentro desse namespace,
o hash do texto permite reutilizar vetores entre tópicos e consultas repetidas.
Mudança de corpus recria o índice FAISS, mas textos já representados reutilizam vetores.
Uma alteração de modelo no mesmo deployment exige atualizar `embedding_model_version`.

Acervos com até 20 mil trechos usam FAISS Flat exato. Os maiores usam IVF-PQ
aproximado, treinado com amostra determinística de até 50 mil vetores. Utiliza 96
subquantizadores de oito bits; consulta com `nprobe=32`. A compressão reduz memória,
mas pode perder vizinhos relevantes. As métricas e a avaliação do corpus devem orientar
eventuais mudanças. Não se carrega a matriz inteira de embeddings na RAM.

O cache dos vetores originais continua ocupando disco: um milhão de vetores float32
de 3.072 dimensões tem cerca de 12,3 GB de dados, antes do overhead do banco. O índice
IVF-PQ é adicional e bem menor. A primeira preparação precisa representar todos os
trechos únicos e pode ser demorada; consultas futuras reutilizam o índice preparado.

Há orçamento separado de 50 mil tentativas HTTP de embeddings (`embedding_max_calls`).
Cada retentativa é contada; as reservas ficam em `orcamento_embeddings.json`.
`chamadas_embeddings.jsonl` registra deployment, contagem de tokens, uso informado
e erros, sem credenciais. As chamadas de reranqueamento usam o orçamento de linguagem
(`max_calls`), junto com pesquisa, redação e auditoria. Esgotar orçamento/falhar não
ativa silenciosamente um modo lexical: interrompe e preserva checkpoints/cache.

## Execução no servidor

Atualize a branch e instale `pipeline/qa_research/requirements.txt`. Os comandos de
[`SERVIDOR.md`](SERVIDOR.md) continuam usando o mesmo arquivo de configuração e agora
produzem `saida_produtos_quimicos_hibrido/documento_auditado.md`.

Opcionalmente, prepare o índice antes da pesquisa, sem chamadas a modelos de linguagem:

```bash
venv/bin/python -u -m pipeline.qa_research.run \
  --config pipeline/qa_research/configs/produtos_quimicos.json \
  --manifest dataset/domain_corpora/manifest.json \
  --stage indice
```

Depois use `--stage pesquisa` para produzir o documento. A preparação também acontece
automaticamente se a pesquisa for iniciada diretamente. `--plan` continua sem API.

## Avaliar ganho e possíveis perdas

Cada arquivo em `recuperacoes/` contém consulta/recorte, listas dos dois canais,
escores, fusão, textos enviados ao reranqueador, avaliações e seleção final.
É possível comparar BM25, fusão e reranqueamento sobre as mesmas consultas sem
adivinhar quais candidatos foram excluídos. O modo `bm25` permanece explícito em
`retrieval_mode` para controle, sempre com outra pasta de saída.

Os testes usam FAISS real, inclusive IVF-PQ, e embeddings/LLM simulados. Verificam
integração, cache, orçamento, ausência de fallback silencioso e proveniência; não
demonstram ganho de qualidade científica do modelo Azure. Para isso, a próxima
execução deve avaliar uma amostra das consultas e seus resultados: evidências úteis
recuperadas, cobertura entre documentos, exceções retidas, falsos positivos e custo.

Não adicionamos datasets externos nem pares QA de exemplo aos prompts.

Referências primárias: [OpenAI — embeddings](https://developers.openai.com/api/docs/guides/embeddings),
[OpenAI — text-embedding-3-large](https://developers.openai.com/api/docs/models/text-embedding-3-large),
[Microsoft — fusão RRF](https://learn.microsoft.com/en-us/azure/search/hybrid-search-ranking),
[FAISS — tipos de índice](https://github.com/facebookresearch/faiss/wiki/Faiss-indexes).
