# Piloto de contexto e QA por cobertura

Fluxo novo e opt-in. A entrada é **tópico + subtópico + frase integral do especialista**,
lida diretamente de `pipeline/fase_3/topicos.py`. O piloto padrão é `02_02`, Produtos
químicos. Recortes são organização interna; não criam subtópicos nem reduzem o escopo.
As saídas anteriores não são usadas como checkpoints nem sobrescritas.

## Instalar no servidor

Na raiz do checkout, na branch de trabalho:

```bash
git pull --ff-only origin codex/qa-evidencias-verificadas
python3 -m venv .venv-documento  # apenas se esse ambiente ainda não existir
.venv-documento/bin/python -m pip install -r pipeline/qa_research/v2/requirements.txt
export DOCUMENT_PYTHON="$PWD/.venv-documento/bin/python"
```

As credenciais Azure continuam no ambiente ou `.env` da raiz. Nenhum comando abaixo
troca credenciais, endpoint, gateway ou certificado. Para a coleta HTTPS corporativa,
use `--ca-file /caminho/certificado.pem` ou `SSL_CERT_FILE`; não desative TLS.

## Instalar o corpus profissional

```bash
bash pipeline/qa_research/instalar_corpus_profissional_v2.sh \
  --output dataset/professional_corpora_v2 \
  --sources abb kimray emerson offshorenorge imca iogp \
  --max-documents 30 --max-pages 100 --depth 2
```

Coleta somente fontes oficiais delimitadas: ABB Production Handbook, treinamento
Kimray, Emerson/Fisher Control Valve Handbook, guias Offshore Norge, IMCA Safety
Flashes e IOGP Process Safety Fundamentals. Os limites são **por fonte**. Não é
espelhamento integral nem corpus exaustivo. `install_report.json` registra erros,
limites e páginas restantes; `manifest.json` distingue acervo utilizável com avisos
de instalação bloqueada.

Se um portal bloquear acesso, examine o relatório. Repita o comando para reutilizar
downloads verificados por hash. Para aceitar **explicitamente** um acervo com fonte
selecionada vazia, repita com `--allow-errors`: erros continuam registrados,
coleções vazias são omitidas e a cobertura continua parcial. Sem nenhuma coleção
utilizável, o manifesto mantém ready=false.
Não execute o instalador enquanto uma geração usa esse mesmo manifesto.

### Atualização de robustez: AES, retomada e estado do acervo

O ambiente agora instala **`pypdf[crypto]`**, incluindo suporte a AES. O instalador
verifica as dependências antes de alterar o manifesto e informa o Python que deve
receber a instalação. Isso corrige `cryptography>=3.1 is required for AES algorithm`.
PDF que realmente exige senha continua registrado como inacessível.

Na versão atual, falha isolada de um documento **não bloqueia** uma fonte que já
tem documentos íntegros. O manifesto pode indicar `ready=true` e
`status=ready_with_warnings`, mantendo erros, categorias e ações recomendadas no
relatório. Dependência ausente, corrupção ou fonte selecionada vazia bloqueiam.
`--strict` restaura o bloqueio por qualquer erro; `--allow-errors` permite aceitar
explicitamente fontes ausentes. Nenhuma dessas opções produz um acervo exaustivo.

Para reparar o download já feito no servidor, sem baixar novamente o acervo:

```bash
git pull --ff-only origin codex/qa-evidencias-verificadas
export DOCUMENT_PYTHON="$PWD/.venv-documento/bin/python"
"$DOCUMENT_PYTHON" -m pip install -r pipeline/qa_research/v2/requirements.txt
bash pipeline/qa_research/instalar_corpus_profissional_v2.sh \
  --output dataset/professional_corpora_v2 --retry-failed
```

Essa retomada usa `install_report.json`, tenta somente URLs antes reprovadas e
preserva as demais coleções verificadas por hash, mesmo se o manifesto anterior
estiver `ready=false`. Em recoleta normal, originais são reutilizados e novas
extrações também possuem cache por hash/revisão. Uma falha de rede não apaga os
documentos válidos anteriores. Não altere o diretório de origem do download.

Dados ficam em `dataset/` (fora do Git), preservando números, texto original,
fronteiras documentais e páginas conhecidas. HTML sem paginação tem page=null.
PDF sem texto suficiente é rejeitado; não há OCR automático. Figuras/tabelas que
perderem informação exigem revisão. Acesso público não implica licença aberta:
conserve atribuição e condições registradas e não publique os originais automaticamente.

Para reunir o corpus novo com o acervo antigo **já instalado no servidor**, acrescente:

```bash
  --base-manifest dataset/domain_corpora/manifest.json
```

Essa opção cria um manifesto combinado sem modificar a instalação antiga. O
carregador anterior continua exigindo suas cinco coleções no schema legado; o
schema profissional permite coleções adicionais e subconjuntos declarados.

FORCE é **corpus de documentos industriais**, não banco de questões. Sua instalação
é opcional porque acrescenta aproximadamente 6,1 GB em CSV, além do texto normalizado:

```bash
bash pipeline/qa_research/instalar_corpus_profissional_v2.sh \
  --output dataset/professional_corpora_force_v2 --sources abb kimray \
  --with-force
```

Importa o registro oficial <https://zenodo.org/records/10775273>, verifica checksums,
prefere texto anonimizado `content_scrubbed_light` e usa os indicadores de qualidade.
Preserva filename/page quando presentes; não inventa identidade de relatório quando
ausente. Falha explicitamente se o esquema CSV mudar. Reserve espaço para originais
e normalizados. Volve não é baixado automaticamente: exige acesso ao Marketplace e
seleção dos formatos úteis; não é prometido como corpus textual pronto.

Verificar recuperação antes de gastar chamadas Azure:

```bash
.venv-documento/bin/python -m pipeline.qa_research.v2.search \
  --manifest dataset/professional_corpora_v2/manifest.json \
  --query "dosagem química água produzida" \
  --query-en "chemical dosing produced water" --limit 5
```

O piloto usa **BM25/FTS5**, com índice persistente e fronteiras documentais; não
calcula embeddings nem afirma executar busca híbrida. O manifesto também pode
ser usado pelo `CorpusIndex` existente. A arquitetura permite acrescentar canais
semânticos depois de medir as lacunas do piloto; este teste controla a recuperação lexical.

### Recuperação bilíngue e escrita em português brasileiro

Cada rodada normaliza as consultas iniciais e as lacunas em pares explícitos
`pt`/`en`, validados antes da busca. O limite configura **pares**, não uma lista
que pode cortar todas as consultas inglesas. Ambos os idiomas são sempre
consultados; os rankings são combinados por RRF antes da seleção de passagens.
Os originais permanecem intactos. BM25 não traduz sozinho e ainda depende dos
termos/sinônimos gerados; não é busca semântica multilíngue.

Novas extrações registram idioma e confiança com detecção estatística determinística.
Fontes antigas com idioma desconhecido são identificadas durante a recuperação.
O idioma nunca é, isoladamente, um filtro de exclusão. Idiomas diferentes de PT/EN
podem estar no acervo, mas a consulta bilíngue não garante sua recuperação.
Cada rodada entrega `idiomas_busca.json` e consultas/resultados com idioma em
`recuperacoes.json`, para conferir a contribuição efetiva de materiais ingleses.

Redação e auditoria recebem orientação de português brasileiro e uso profissional
do Brasil. Há revisão linguística explícita por bloco e critérios obrigatórios
`pt_br` e `terminologia_br` na auditoria das questões. Regionalismos como caudal,
equipa e controlo geram revisão; termos consolidados como offloading, topside,
subsea e siglas podem permanecer. Não há substituição cega de palavras, alteração
das evidências literais nem conversão automática de requisitos estrangeiros.
A revisão de tradução técnica permanece no auditor que recebe as fontes originais.

Esta atualização altera prompts, papéis e identidade do experimento. Use uma
**saída nova para geração**; o corpus baixado pode ser reparado no mesmo lugar:

```bash
bash pipeline/qa_research/rodar_piloto_cobertura_v2.sh \
  --item 02_02 --manifest dataset/professional_corpora_v2/manifest.json \
  --output pipeline/qa_research/saida_cobertura_v2/02_02_ptbr
```

Consultas usam `gpt-5-4-petrobras:low`; revisão linguística usa
`gpt-5-4-petrobras:medium`. Parecer do modelo e detecção estatística não substituem
a revisão humana de terminologia pelo especialista.

## Planejar e executar o piloto

```bash
bash pipeline/qa_research/rodar_piloto_cobertura_v2.sh \
  --item 02_02 --manifest dataset/professional_corpora_v2/manifest.json --plan

bash pipeline/qa_research/rodar_piloto_cobertura_v2.sh \
  --item 02_02 --manifest dataset/professional_corpora_v2/manifest.json \
  --output pipeline/qa_research/saida_cobertura_v2/02_02
```

`--plan` lê somente a configuração e o escopo: não cria clientes, índices, saídas
ou chamadas. Para acompanhar pelo notebook, abra `piloto_cobertura_v2.ipynb`.

Execução após desconectar da sessão SSH:

```bash
nohup bash pipeline/qa_research/rodar_piloto_cobertura_v2.sh \
  --item 02_02 --manifest dataset/professional_corpora_v2/manifest.json \
  --output pipeline/qa_research/saida_cobertura_v2/02_02 \
  > piloto_cobertura_02_02.log 2>&1 &
tail -f piloto_cobertura_02_02.log
```

Repita o mesmo comando para retomar; orçamento e checkpoints são cumulativos.
`--max-calls 2400` pode ampliar o limite sem invalidar a identidade. Mudanças em
código, escopo, corpus, exemplos ou modelos exigem outra saída. Execução concorrente
na mesma saída é bloqueada. Respostas inválidas usam o reparo/retentativas do backend.
Falha fatal/orçamento interrompe preservando checkpoints; falha isolada de candidata
é registrada como pendência, sem aprovar itens para completar quantidade.

O resolvedor está configurado como `gpt-5-petrobras:high`; os demais papéis estão em
`piloto_02_02.json`. Nomes de deployment não confirmam disponibilidade na conta.
Se necessário, escolha explicitamente outro resolvedor **na primeira execução**:
`--solver-model gpt-5-4-petrobras:high`. Não há fallback automático. A troca reduz a
diversidade de modelos, e chamadas separadas não provam independência de erros.

## Mecanismo documental

1. Planejador extrai até 12 recortes com âncoras literais na frase do especialista.
2. Consultas PT/EN recuperam fontes do manifesto. Cada recorte conserva até 36
   passagens, com limite por documento; rodadas seguintes procuram material adicional.
3. Motor documental existente lê fontes, escreve, audita blocos, valida todos os
   complementos declarados, corrige reprovações e deduplica. O orçamento global é
   compartilhado entre os papéis; leitura usa low, escrita/auditoria usam high.
4. Revisor global verifica cobertura, coerência de sistemas e redundâncias. Suas
   consultas e correções voltam à rodada seguinte de pesquisa/redação.
5. Ganho é contado por relações novas identificadas nos blocos auditados, não por
   crescimento do texto. É julgamento automatizado e não enumeração perfeita do domínio.
6. Encerra por cobertura suficiente, duas rodadas sem ganho ou três rodadas totais.
   Limites/orçamento são preservados e resultado parcial é explícito. Blocos com
   conflitos globais conhecidos são excluídos e a versão restante é reavaliada.
   Conflito global restante bloqueia QA.

`contexto/documento.md` e `.json` são texto limpo. Fontes, complementos, auditorias,
consultas e lacunas ficam em auxiliares nas pastas das rodadas.

## Mecanismo das questões e quantidade

1. Extrai KUs com passagens literais e alvos de classe sustentados, audita-as e
   identifica duplicatas. Inventário rejeitado e motivos são conservados.
2. Planeja alvos por KU/classe e encadeamentos necessários entre 2–3 KUs.
   Mantém conceito, mecanismo, consequência, diagnóstico, decisão e procedimento;
   simples/composta são classificações separadas. Não força seis perguntas por KU.
3. Autor recebe alvo, KUs, contexto e exemplos curados de outros subtópicos.
   Pode ler arquivos adicionais via `--examples /caminho/existente.jsonl` (campos
   pergunta/resposta ou question/answer). **Nunca baixa ou altera datasets QA**.
   Exemplos não são evidência e não entram no corpus técnico.
4. Resolvedor recebe apenas pergunta e blocos, sem gabarito/plano/exemplos. Auditor
   recebe contexto em todas as candidatas e verifica suporte, autonomia, ambiguidade,
   pistas e preservação do alvo/classe/composição.
5. Refino tem até duas tentativas, mantém o alvo e é novamente resolvido e auditado.
   Mudança de alvo vai ao planejador; falta de suporte vira lacuna documental.
   Essas lacunas são entregues para nova execução documental, não preenchidas pelo
   refinador nem corrigidas automaticamente no corpus original.
6. Compara aprovadas por demanda/conhecimento, inclusive entre classes; similaridade
   é triagem, não um corte universal de cosine. Toda candidata aprovada é comparada
   com todas as já admitidas em lotes.

Para evitar poucas questões, o piloto permite **160 alvos, 24 por rodada e até oito
rodadas**. A meta mínima desejada é 40 aprovadas, sem garantia nem relaxamento dos
filtros. Parada por cobertura exige simultaneamente 90% das KUs, 85% das demandas
KU/classe e pelo menos 40 aprovadas; duas rodadas com menos de duas novas aprovadas
também encerram. Metas são hipóteses experimentais configuráveis, não limites
validados. Cobertura de KU sozinha não encerra o ciclo e não demonstra cobertura
integral da frase ou domínio. O relatório discrimina classes, composição, alvos
descobertos, recusas e encaminhamentos.

Só documento: acrescente `--stage context`. Só QA do documento deste piloto:

```bash
bash pipeline/qa_research/rodar_piloto_cobertura_v2.sh \
  --item 02_02 --manifest dataset/professional_corpora_v2/manifest.json \
  --output pipeline/qa_research/saida_cobertura_v2/02_02 --stage qa
```

Um documento externo limpo pode ser indicado por `--document CAMINHO`; use saída nova,
confira o título esperado em `--plan` e registre que sua auditoria prévia é externa.

## Ler, coletar e enviar resultados

Leia `saida_cobertura_v2/02_02/RELATORIO.md`, `resumo.json`, `contexto/cobertura.json`
e `questoes/cobertura.json`. Questões publicadas estão em `questoes/qa.csv` e
`aprovadas.jsonl`; rejeições/histórico e KUs ficam nos auxiliares.

Ao terminar, aparece **O código acabou de rodar no terminal 🙂**, o estado real e
os comandos concretos de coleta, commit, push e pull local. Código 0 indica cobertura
configurada atendida; 2 indica resultado parcial/interrupção. A frase de término
não transforma um resultado parcial em sucesso.

```bash
.venv-documento/bin/python -m pipeline.qa_research.v2 \
  --output pipeline/qa_research/saida_cobertura_v2/02_02 \
  --collect pipeline/qa_research/relatorios/piloto_cobertura_v2_02_02
git add -- pipeline/qa_research/relatorios/piloto_cobertura_v2_02_02
git commit -m "Resultados do piloto de cobertura v2 - Produtos quimicos"
git push origin codex/qa-evidencias-verificadas
```

A coleta é imutável e guarda hashes. Exclui `.local`, pacotes de fontes, chamadas
com fontes brutas e diretórios documentais internos. A auditoria completa permanece
na saída original do servidor; o snapshot Git é a entrega de textos, QA e relatórios
de cobertura/encaminhamento. Não inclui `.env`, credenciais nem originais de fabricantes.

Na máquina local: `git pull --ff-only origin codex/qa-evidencias-verificadas`.

## Verificação

```bash
python -m unittest discover -s pipeline/qa_research/v2/tests -v
```

Testes simulados verificam a cadeia completa, retomada sem novas chamadas,
isolamento do gabarito, contexto na auditoria original, ancoragem no escopo,
preservação das classes, reauditoria do refino, encaminhamento de lacunas,
integridade do manifesto e compatibilidade com a busca existente. Não medem
qualidade científica nem substituem o piloto Azure/revisão do especialista.
