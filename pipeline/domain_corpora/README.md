# Corpora factuais para PetroQuest QA

## Próxima execução: QA v6

A instalação dos corpora permanece a mesma. A rodada atual compõe documentos técnicos por faceta usando 10 trechos de cerca de 1.000 palavras, sem auditoria factual prévia bloqueante. **[Comandos atuais QA v6](../fase_4/EXECUCAO_QA_V6.md)**. Use saída nova. Comandos QA v4 abaixo são históricos; não reutilize seus índices ou documentos.

**Petrolês continua na base**, junto com ANP, HSE, BSEE e REGIS. Estes materiais fornecem suporte factual; os datasets de QA externos continuam servindo como exemplos de formato.

## Instalar no servidor

Na raiz do checkout, com o ambiente Python utilizado pelo pipeline:

```bash
git pull --ff-only origin dev
python -m pip install -r requirements.txt

python -u pipeline/domain_corpora/install_corpora.py \
  --petroles-dir dataset/corpus-SemProcessamento-publico-PetrolesHibrido \
  --output dataset/domain_corpora

python pipeline/domain_corpora/verify_corpora.py \
  --manifest dataset/domain_corpora/manifest.json
```

Informe a pasta real do Petrolês. O instalador registra os **dois TXT de domínio** `corpusPublico(sem IBICT)-SemProcessamento.txt` e `corpusPublicoIBICT-SemProcessamento.txt`, sem modificá-los. Para outros nomes ou uma seleção diferente, use `--petroles-txt /arquivo1.txt /arquivo2.txt`. NILC não entra. Não é obrigatório que o diretório se chame Híbrido.

Instalar somente as dependências da coleta, sem os modelos do pipeline: `python -m pip install -r pipeline/domain_corpora/requirements.txt`. É necessário Python 3.10 ou superior.

Sem `--max-documents-per-source`, o instalador coleta **todos os documentos descobertos nas seções configuradas** e todos os XML do pacote REGIS. Não significa espelhar integralmente os portais das agências. REGIS fornece um ZIP oficial de aproximadamente **1,31 GB** com **21.444 XML de documentos**, além de metadados de avaliação. Os XML somam **4,15 GB** descomprimidos; reserve pelo menos **20 GB livres** para originais, cópias normalizadas, PDFs e índices. `queries.xml`, `qrels.txt`, README e licença do código não viram documentos factuais.

Downloads são retomáveis por `.part`, têm hash SHA-256 local e, no REGIS completo, verificação do MD5 publicado pelo Zenodo. Repita o mesmo comando para continuar ou reutilizar o cache. Arquivos alterados/corrompidos são detectados. `--regis-local /pacote/regis.zip` aceita o ZIP original já baixado, verificando o checksum oficial.

Para o certificado corporativo: acrescente `--ca-file /caminho/certificado.pem` ou configure `SSL_CERT_FILE`. Proxy usa as variáveis padrão `HTTPS_PROXY`/`HTTP_PROXY`. A verificação TLS permanece ativa.

## Fontes e escopo

| Coleção | Material coletado | Idioma / jurisdição |
|---|---|---|
| Petrolês | Os TXT existentes, lidos em fluxo | Português; jurisdição não inferida |
| [ANP](https://www.gov.br/anp/pt-br/assuntos/exploracao-e-producao-de-oleo-e-gas/seguranca-operacional) | Relatórios de incidentes e documentos da seção de segurança operacional | Principalmente português / Brasil |
| [HSE](https://www.hse.gov.uk/offshore/inspection.htm) | Guias de inspeção offshore, integridade, manutenção, controle de trabalho, segurança, operação marítima e documentos relacionados | Inglês / Reino Unido |
| [BSEE](https://www.bsee.gov/guidance-and-regulations/guidance/safety-alerts-program) | Alertas de segurança offshore, com paginação do catálogo e PDFs vinculados | Inglês / Estados Unidos |
| [REGIS](https://zenodo.org/records/4726013) | Texto dos documentos geocientíficos do pacote oficial, em XML Solr | Português; jurisdição não inferida |

O catálogo de URLs oficiais está em `catalog.py`. A descoberta segue apenas seções/domínios delimitados. HSE possui também PDFs oficiais enumerados no catálogo, úteis quando uma página HTML estiver indisponível. Erros de descoberta aparecem no relatório; a coleção instalada é um snapshot dos documentos efetivamente encontrados. Há links antigos no índice da ANP: a migração confirmada de `seguranca-operacional-e-meio-ambiente` para `seguranca-operacional` é tratada, preservando a URL do índice e a URL utilizada.

Licença/origem são registradas. A licença do código REGIS não é assumida como licença de cada publicação. O HSE indica OGL com exceções; materiais de terceiros precisam conservar suas condições. Os documentos ficam em `dataset/`, fora do Git.

## Teste rápido, sem Azure

```bash
python -m unittest discover -s pipeline/domain_corpora/tests -v

python pipeline/domain_corpora/install_corpora.py \
  --petroles-dir dataset/corpus-SemProcessamento-publico-PetrolesHibrido \
  --max-documents-per-source 2 --output dataset/corpora_smoke

python pipeline/domain_corpora/verify_corpora.py \
  --manifest dataset/corpora_smoke/manifest.json --allow-sample
```

O modo de amostra do REGIS usa HTTP Range para ler o índice do ZIP e os membros selecionados, verificando o CRC dos membros. **Não verifica o MD5 do pacote inteiro.** Se o servidor/proxy não permitir Range, use `--full-regis-archive` ou `--regis-local`. As amostras têm `sample=true` no manifesto e são bloqueadas pela geração por padrão. Instale a rodada principal em `dataset/domain_corpora`, **sem o limite de amostra**.

Testes cobrem cache, retomada e checksum, ZIP parcial, XML real do REGIS, paginação BSEE, migração ANP, páginas sem texto, proveniência, cotas lexicais por coleção, tradução em cache, janelas finais, integração com auditoria e alternância das cinco coleções. Não chamam Azure. A auditoria técnica do LLM será executada ao preparar a rodada, não durante os testes do instalador.

## Organização e controle de qualidade

```text
dataset/domain_corpora/
  manifest.json
  install_report.json
  anp|hse|bsee|regis/
    catalog.json / zenodo_record.json
    raw/                         PDFs ou XML originais
    extracted/                   texto e metadados por documento
    pages.jsonl                  coleção normalizada para recuperação
    documents.json               inventário de documentos
```

O manifesto também referencia os TXT originais do Petrolês com caminhos relativos. PDFs preservam página e fronteira de documento. REGIS não fornece paginação confiável; usa `page=null`. O Petrolês concatenado não oferece fronteiras confiáveis de documento nem página; esta limitação é informada ao auditor. Não inventamos essas fronteiras.

Páginas com menos de 20 palavras ou baixo conteúdo alfabético são excluídas e registradas. Documento sem nenhuma página aproveitável fica em `quarantined`; não vira material factual. **OCR não é automático nesta implementação.** Figuras, fórmulas e tabelas podem perder informação na extração; a auditoria deve rejeitar afirmações dependentes de elementos ausentes. Falha de download/estrutura aparece em `errors` e retorna código de saída 1. Uma coleção vazia ou erros pendentes tornam o manifesto não utilizável. Falhas de descoberta não são ocultadas: consulte `discovery_warnings` para conhecer a cobertura.

Se alguns PDFs públicos estiverem indisponíveis, consulte o relatório e repita a instalação para tentar novamente. Para utilizar explicitamente o conjunto parcial disponível, acrescente **`--allow-document-errors`**: o manifesto terá `partial=true`, preservará o número de falhas e o pipeline informará a condição. Uma das cinco coleções vazia continua bloqueando a instalação. Esta opção não substitui documentos ausentes nem desativa a auditoria.

## Executar a próxima geração

```bash
python pipeline/qa_references/download_qa_examples.py --max-per-dataset 1000
mkdir -p pipeline/fase_4/saida_qa_v4_azure_large_medium

nohup python -u pipeline/fase_4/run_qa.py \
  --corpus-manifest dataset/domain_corpora/manifest.json \
  --deployment gpt-5-4-petrobras --effort medium \
  --embedding-deployment embedding-3-large-global \
  --limit-per-topic 100 --batch-size 2 --observe-only --max-calls 10000 \
  --max-context-refinements 2 \
  --output pipeline/fase_4/saida_qa_v4_azure_large_medium \
  > pipeline/fase_4/saida_qa_v4_azure_large_medium/execucao.log 2>&1 < /dev/null &
```

Use uma **nova saída QA v4**, sem retomar a coleta anterior: facetas, seleção, embeddings e auditoria mudaram. Os corpora instalados permanecem válidos; a preparação e os vetores são recalculados. Para continuar uma interrupção desta mesma QA v4, repita os argumentos com `--resume`. `--prepare-only` permite revisar as auditorias antes de gerar QA; essa etapa **usa Azure**, inclusive embeddings. O teto de 10.000 pedidos lógicos inclui LLM e embeddings; não é uma previsão de consumo. Pode ser ampliado na retomada.

Antes de iniciar, teste o acesso ao deployment com um pedido curto de embeddings (não gera QA):

```bash
python pipeline/fase_4/prepare_tokenizer.py
python pipeline/fase_4/run_qa.py --check-embeddings \
  --embedding-deployment embedding-3-large-global --output dataset/embedding_smoke_servidor
```

O primeiro comando baixa o vocabulário público cl100k_base, verificando seu hash; aceita `--ca-file` e utiliza `AOAI_CA_BUNDLE` do backend quando configurado. O segundo usa o Azure e precisa retornar vetores `(2, 3072)`. Ambos preservam verificação TLS. Endpoint, credenciais, API version, gateway e certificado seguem a configuração existente do projeto. Não há chamada ao modelo de chat no teste de embeddings.

O manifesto substitui a seleção de arquivos na CLI: já contém Petrolês. Não combine `--corpus-manifest` com `--corpus-txt`, `--corpus-dir` ou `--corpus-zip`.

### Como as cinco fontes participam

1. O manifesto e os hashes são conferidos antes de preparar facetas.
2. As consultas/termos das facetas ganham versão em inglês, via modelo de preparação, com cache. Textos originais não são traduzidos em massa.
3. A busca guarda até **60 candidatos por `(faceta, coleção)`**, em vez de deixar todo o top-K ser ocupado pelo corpus maior. Janelas não atravessam documentos/páginas quando essas fronteiras existem.
4. Os candidatos de **todas as coleções formam um conjunto único por faceta**. Embeddings são exclusivamente Azure `embedding-3-large-global`, em 3.072 dimensões. O ranking combina similaridade à faceta (0,60), ao escopo FPSO/FSO (0,25) e relevância lexical (0,15), seguido de MMR. São parâmetros iniciais, ainda não calibrados com a nova coleta. Seleciona até 12 trechos, montando até dois documentos com no máximo seis trechos cada. **Um mesmo contexto pode combinar os cinco corpora**, sem função fixa por coleção. Conteúdo idêntico entre coleções é deduplicado; contextos de uma só coleção também são válidos.
5. Cada montagem passa pelo auditor de conteúdo, que recebe o conjunto e a proveniência de cada trecho. Ele verifica compatibilidade de condições, contradições e jurisdições, podendo excluir trechos ou bloquear a montagem. Um contexto bloqueado pode passar por **duas recomposições**: um refinador seleciona novos IDs entre até 24 candidatos reais, orientado pelo parecer; cada seleção recebe nova auditoria independente. Não altera texto original, não inventa fatos e não pode repetir um conjunto já reprovado. Se não houver suporte útil, mantém o bloqueio. Apenas trechos autorizados chegam ao Gerador/Refiner/Judge.
6. A exploração alterna facetas/documentos e considera uso das coleções. Não é obrigatório usar todas em cada tópico: a pertinência e a auditoria governam a cobertura.

QA continua em português, autossuficiente e sem alternativas. HSE/BSEE não viram automaticamente requisitos brasileiros. Auditoria e Judge fazem o controle factual. Cosine, redundância e saturação continuam **observacionais** nesta rodada.

Os resultados incluem `corpora_utilizados.json`, `dominio/indices/candidatos_multicorpus.meta.json`, cobertura por coleção, auditorias, escolhas de coleção em cada rodada e proveniência dos trechos por candidata. Isso permitirá analisar quais fontes contribuíram e onde foram bloqueadas.

`cobertura_dominio.json` também registra `documents_with_multiple_collections`. Um contexto com duas coleções conta em ambas em `documents_by_collection`; essa soma pode exceder o total de documentos. O journal de auditorias registra as coleções candidatas e as efetivamente autorizadas. A nova montagem muda a assinatura dos contextos: se já houve preparação na versão que separava por coleção, utilize a nova saída indicada acima. Os corpora instalados podem ser reutilizados.

QA v4 acrescenta `recuperacoes_contexto.jsonl`, `dominio/recuperacoes/`, `chamadas_embeddings.jsonl` e `dominio/embeddings/azure_cache.sqlite3`. O cache guarda vetores já normalizados por hash do texto e valida modelo, deployment, dimensões, tokenizer e API version. Textos maiores que 8.192 tokens são divididos em janelas sobrepostas e agregados sem truncamento. Lotes têm até 64 entradas e 100.000 tokens. O contrato segue a [API oficial de embeddings](https://developers.openai.com/api/reference/python/resources/embeddings/methods/create). Nenhum vetor MiniLM é utilizado nesta QA v4. A escala de cosine e os clusters mudam, exigindo nova análise; os filtros continuam observacionais.

`--reuse-preparation-from` é uma opção para futuras execuções com preparação compatível, verificando assinaturas e copiando somente facetas/índice lexical. Ela não importa vetores nem auditorias e rejeita as facetas da versão anterior. **Nesta nova rodada, não use essa opção**, para refazer a preparação que gerou os bloqueios relatados.
