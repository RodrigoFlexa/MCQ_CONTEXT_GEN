# Preparar uma vez e executar no servidor

O servidor pode receber um diretório autossuficiente contendo **textos originais,
proveniência, BM25 e FAISS já construídos**. A execução com `--pack` não descobre
arquivos do corpus, não fragmenta textos, não treina FAISS e não calcula embeddings
dos documentos. Não precisa do corpus bruto nem do modelo local de triagem.

Ainda faz embeddings Azure das novas consultas e chamadas ao reranqueador,
pesquisadores, redator e auditor. Preparar o pacote não elimina essa latência.
Não há estimativa de aceleração sem medir a execução real no servidor.

## Caminho recomendado: conservar todo o acervo

Na máquina de preparação, com o manifesto completo dos cinco bancos e o ambiente
Azure que já funciona no projeto:

```powershell
python -m pip install -r pipeline/qa_research/requirements.txt

python -u -m pipeline.qa_research.prepare `
  --config pipeline/qa_research/configs/produtos_quimicos.json `
  --manifest dataset/domain_corpora/manifest.json `
  --destination pipeline/qa_research/.local/packs/acervo_completo
```

Sem `--profile`, **conserva todos os trechos** e o mesmo pacote pode servir a outros
tópicos. Esta é a opção que preserva a cobertura do acervo de entrada. O primeiro
preparo ainda tem custo de CPU, disco e API; os vetores são calculados em lotes,
guardados em cache por conteúdo e reutilizados nas próximas preparações. Alterar
o tópico não exige reembeddar o mesmo acervo com o mesmo protocolo.

Para incluir triagem semântica local, instale as dependências adicionais **somente
na máquina de preparação**:

```powershell
python -m pip install -r pipeline/qa_research/requirements-preparation.txt
```

## Opção: acervo menor para 2.2. Produtos químicos

```powershell
python -u -m pipeline.qa_research.prepare `
  --config pipeline/qa_research/configs/produtos_quimicos.json `
  --manifest dataset/domain_corpora/manifest.json `
  --profile pipeline/qa_research/configs/triagem_produtos_quimicos.json `
  --local-semantic `
  --destination pipeline/qa_research/.local/packs/produtos_quimicos
```

O perfil contém 40 consultas de exploração em português e inglês: processamento
do óleo, água produzida, água do mar, SRU, desaeração, tratamento do gás, MEG,
hidratos, incrustações, corrosão, emulsões, espuma, depósitos, microbiologia,
dosagem, monitoramento, armazenamento, manuseio e compatibilidade.

Para cada consulta, a triagem toma a **união** de até 40 resultados BM25 com até 40
resultados semânticos locais. Não exige concordância entre os canais. Depois,
preserva todos os trechos disponíveis no índice dos documentos que tenham
fronteiras conhecidas e algum trecho selecionado. Em TXT concatenado, conserva os trechos selecionados e não inventa
fronteiras ou vizinhanças de documento. A deduplicação já existente preserva todas
as referências de origem. Só então os trechos do subconjunto são enviados ao Azure
para preparar a busca híbrida usada pelos agentes.

`selection.json` informa consultas, contagens, fração retida, coleções e protocolo.
`selection.jsonl` registra **cada trecho de entrada**, com seleção/exclusão e seus
motivos. Exclusão significa que o trecho não entrou neste pacote; não é uma
afirmação de irrelevância científica. Não apaga originais nem rejeita uma fonte
por idioma, ser tese ou apresentar resultado divergente. O subconjunto sempre é
marcado como parcial, com `recall_validated=false`. Um documento amplo pode ficar
inteiro no pacote; não há porcentagem de redução garantida.

Esta triagem não valida fatos, doses ou respostas: isso continua sendo feito na
pesquisa e na auditoria. Antes de adotá-la em produção, revise consultas sem
resultados e meça a recuperação com evidências conhecidas e amostras dos excluídos.
O código não realiza essa validação científica automaticamente. Sem essa medição,
prefira o pacote completo para investigações em que a cobertura seja prioritária.

O modelo é [`intfloat/multilingual-e5-small`](https://huggingface.co/intfloat/multilingual-e5-small),
revisão `614241f622f53c4eeff9890bdc4f31cfecc418b3`, com 384 dimensões. O protocolo usa
os prefixos `query: ` e `passage: ` do autor, normaliza os vetores e divide trechos
longos em janelas de 400 tokens, com passo de 320; a melhor similaridade entre as
janelas representa o trecho para cada consulta. Não descarta a cauda do trecho.
Esse é um protocolo de triagem deste projeto, não uma avaliação publicada de E5
no domínio offshore. O cache SQLite é separado do Azure e a execução retoma
embeddings locais concluídos após interrupção.

Por padrão, exige o modelo no cache e não baixa pesos. Acrescente
`--allow-model-download` no primeiro uso se necessário. `--device cuda` usa GPU
disponível na máquina de preparação; o padrão é CPU. CPU também pode demorar.

## Se o corpus completo só existe no servidor

Há duas opções para trazer os textos e a proveniência para a máquina de preparação:

1. Copiar o corpus bruto e seu manifesto completo.
2. Exportar **o índice lexical que já foi construído**, evitando nova leitura e
   fragmentação dos originais.

Para a segunda opção, no servidor, encontre a pasta que contém `corpus.sqlite3` e
`indice.json` em `pipeline/qa_research/.local/index/<assinatura>/`. Use essa pasta:

```bash
venv/bin/python -m pipeline.qa_research.prepare \
  --config pipeline/qa_research/configs/produtos_quimicos.json \
  --snapshot pipeline/qa_research/.local/index/ASSINATURA_DO_INDICE \
  --lexical-only \
  --destination pipeline/qa_research/.local/packs/base_para_preparar
```

Isso só exporta o snapshot escolhido; não verifica se o corpus bruto mudou depois
de sua construção. Não usa APIs. Leve esse diretório para a máquina de preparação
e finalize lá:

```powershell
python -u -m pipeline.qa_research.prepare `
  --config pipeline/qa_research/configs/produtos_quimicos.json `
  --source-pack pipeline/qa_research/.local/packs/base_para_preparar `
  --profile pipeline/qa_research/configs/triagem_produtos_quimicos.json `
  --local-semantic `
  --destination pipeline/qa_research/.local/packs/produtos_quimicos
```

Retire `--profile` e `--local-semantic` para finalizar o acervo completo. Na
finalização, os embeddings dos documentos são calculados na máquina de preparação
por chamadas ao backend Azure; precisa haver acesso a esse backend nessa máquina.

Também é possível usar `--lexical-only` no preparo com originais e/ou triagem. Um
pacote assim contém textos/BM25 e serve de etapa intermediária: **a pesquisa híbrida
recusa um pacote sem vetores**, em vez de construí-los silenciosamente no servidor.

## Transferir o pacote final

Os índices e textos não são enviados pelo Git. O Git transporta o código; o pacote
é um artefato local de dados em `.local/`. Para arquivar no Windows:

```powershell
tar -czf pipeline/qa_research/.local/produtos_quimicos.tar.gz `
  -C pipeline/qa_research/.local/packs produtos_quimicos
```

Transfira o arquivo pelo meio habitual. No servidor, extraia e execute:

```bash
cd /home/gbs2/MCQ_CONTEXT_GEN
git fetch origin
git switch codex/qa-evidencias-verificadas
git pull --ff-only origin codex/qa-evidencias-verificadas
venv/bin/python -m pip install -r pipeline/qa_research/requirements.txt

mkdir -p pipeline/qa_research/.local/packs
tar -xzf /CAMINHO/DO/ARQUIVO/produtos_quimicos.tar.gz \
  -C pipeline/qa_research/.local/packs

nohup venv/bin/python -u -m pipeline.qa_research.run \
  --config pipeline/qa_research/configs/produtos_quimicos.json \
  --pack pipeline/qa_research/.local/packs/produtos_quimicos \
  --output pipeline/qa_research/saida_produtos_quimicos_pacote \
  --stage pesquisa \
  > pipeline/qa_research/produtos_quimicos_pacote.log 2>&1 &
```

O documento fica em
`pipeline/qa_research/saida_produtos_quimicos_pacote/documento_auditado.md`.
Não combine `--pack` com `--manifest`. No notebook, configure
`CONFIG.prepared_pack` ou use `load_config(CONFIG_PATH, pack='caminho/do/pacote')`.

## Integridade, compatibilidade e espaço

- `pack.json` identifica os arquivos, seus hashes, a cobertura, o protocolo de
  embeddings e a versão FAISS usada na preparação. Textos e proveniência ficam
  no SQLite; `index.faiss` contém o índice vetorial. Relatórios de triagem entram
  no pacote quando existem. Não inclui credenciais, pesos E5 ou o cache de vetores
  float32 usado na preparação.
- A primeira instalação verifica hashes, contagem, dimensões e correspondência
  exata dos IDs SQLite/FAISS. As seguintes usam um recibo local, invalidado por
  mudanças no manifesto ou atributos dos arquivos. Isso reduz leituras repetidas;
  não é proteção contra adulteração deliberada que também modifique recibos.
- O caminho Windows/Linux não entra na identidade do pacote. O servidor não
  recalcula a assinatura a partir dos caminhos antigos dos originais. Esses
  caminhos continuam registrados como proveniência, sem serem acessados.
- Para forçar nova verificação integral, execute `prepare --config ...
  --destination CAMINHO_DO_PACOTE --verify`. A leitura sequencial de hashes
  acontece uma vez por instalação, sem reindexação nem chamadas de modelo.
- Pacotes publicados são imutáveis; uma nova preparação exige outro destino.
  Cache de embeddings e BM25 pode ser compartilhado entre preparações. O cache
  permite retomar trabalho concluído; não se deve escrever simultaneamente no
  mesmo destino.
- Os vetores de consulta devem ter exatamente o protocolo Azure do pacote:
  deployment, modelo, versão declarada, dimensões, endpoint e tokenização. **Um
  vetor E5 não pode consultar o índice Azure.** O servidor usa E5 apenas se uma
  futura arquitetura optar explicitamente por esse modelo também na recuperação;
  esta implementação mantém Azure na recuperação final.
- A implementação carrega FAISS em RAM. Conserva Flat para até 20 mil trechos e
  usa IVF-PQ acima disso, conforme a configuração existente. Um vetor Flat de
  3.072 dimensões ocupa 12.288 bytes antes dos IDs/metadados: um milhão ocupa
  aproximadamente 12,3 GB decimais. O IVF-PQ atual usa códigos de 96 bytes por
  vetor, além de IDs, tabelas e textos; a busca é aproximada. O cache completo de
  float32 pode permanecer somente na máquina de preparação.
- Exportar um snapshot já vetorizado com o mesmo protocolo/cache também reutiliza
  FAISS existente. Incompatibilidade de arquivo/modelo falha explicitamente;
  `--pack` não reconstrói índices como alternativa automática.

## Disponibilidade local nesta alteração

O checkout local possui dois TXT brutos do Petrolês (cerca de 970 MB), trechos de
40 seleções salvas e manifestos de teste; não possui o manifesto completo dos
cinco bancos. Sem esse manifesto, a entrada padrão contém 5.576 trechos únicos
das seleções, com cobertura parcial. Os TXT isolados não substituem os cinco
bancos. As credenciais Azure também não estão disponíveis nesta sessão.

Portanto, um pacote local dessas seleções é uma demonstração parcial. Ele não é
o acervo completo de produção, e um pacote `--lexical-only` não é apresentado
como pronto para pesquisa híbrida. Para preparar toda a produção aqui, traga os
originais/manifesto ou o snapshot exportado e disponibilize o backend Azure no
ambiente de preparação.

Foi gerado o pacote intermediário `pipeline/qa_research/.local/packs/base_selecoes_local`
e seu arquivo `pipeline/qa_research/.local/base_selecoes_local.zip` (16.654.097 bytes).
Ele contém 5.576 trechos, proveniência e BM25; não contém vetores Azure. O carregamento
do E5 e o processamento de lotes reais foram verificados, mas a triagem semântica
integral não foi concluída nesta sessão. Os lotes calculados permanecem no cache;
nenhuma seleção semântica incompleta foi publicada como resultado final.
