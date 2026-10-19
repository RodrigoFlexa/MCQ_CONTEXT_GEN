# Documento de Produtos químicos: preparação local e pesquisa no servidor

Este é o fluxo recomendado para a próxima execução. Gera **somente o documento**
do tópico 2.2. Produtos químicos, em Produção e Processo. Não gera QA, alternativas,
exemplos de questões nem usa perguntas de datasets como contexto.

As máquinas trocam arquivos pelo Git. Nenhuma conexão SSH entre elas é necessária.
O pacote preparado aqui já está em `pacotes/produtos_quimicos_v2/` e acompanha este
commit. **Não execute `prepare` no servidor.**

As decisões e sua relação com os problemas observados estão em
[AJUSTES_V2.md](../../docs/analise_run_lexical_2026_10_19/AJUSTES_V2.md).

## O que muda em relação à execução lexical anterior

1. A máquina local lê os originais em streaming e guarda uma fronteira lexical
   por recorte. Exige contexto técnico de aplicação, reduz homônimos fora do
   escopo e filtra catálogos/listas bibliográficas reconhecíveis. Calcula embeddings
   E5 somente desses candidatos, compara consultas
   PT/EN com janelas do texto e combina os rankings por RRF. Deduplica cópias muito
   semelhantes e limita a concentração em documentos com fronteira identificada.
   O servidor não lê os arquivos brutos, não constrói BM25/FAISS e não calcula
   embeddings. O E5 é um filtro de recuperação; não escreve conhecimento científico.
2. O perfil fixa 12 recortes para garantir cobertura: desemulsificantes, espuma,
   água produzida, SRU, oxigênio/desaeração, microbiologia, MEG/hidratos,
   corrosão no gás, depósitos, compatibilidade, armazenamento/manuseio e
   monitoramento/dosagem. Todos recebem a primeira rodada de leitura antes de
   aprofundarmos qualquer recorte. A cobertura é controlada pelo escopo, não pela
   quantidade de variantes que o modelo inventar para água de injeção.
3. No servidor, o pesquisador recebe seis passagens originais por rodada, com
   título/procedência disponível, alertas de qualidade e IDs de seus intervalos.
   Classifica pertinência e natureza da afirmação, extrai relações com condições
   e limites e escolhe próximas fontes dentro do catálogo do recorte. Até três
   rodadas leem até 18 das até 36 fontes pré-selecionadas por recorte. Sugestões de busca fora
   do pacote vão para `pedidos_busca.json`; não são executadas no corpus remoto.
4. O redator recebe até 12 fontes julgadas pertinentes e os achados. Escreve até
   oito blocos delimitados por recorte, com até 220 palavras cada. O auditor vê
   os originais em uma chamada separada por bloco, podendo corrigir a referência
   proposta pelo redator. Exige suporte, condições, escopo, natureza da afirmação
   e fundamentação completa. Somente os cinco critérios aprovados permitem publicar.
5. Uma revisão reescreve somente blocos reprovados. Os IDs incluem a versão;
   pareceres antigos nunca passam a valer para um texto novo. Trechos literais
   são resolvidos pelo código a partir dos intervalos originais, evitando pedir
   ao modelo que copie citações longas sem erro. Valores apagados não são recuperados.
6. Lacunas históricas são reavaliadas contra os blocos atuais. Resolução exige
   um bloco vigente e suporte original. Lacunas sem reavaliação ficam identificadas.
   Descobertas são uma chamada opcional separada; falhas nelas não invalidam a
   pesquisa principal. A consolidação compara possíveis duplicatas sem reescrever
   a prosa aprovada nem tratar fontes sobrepostas como equivalência automática.

Esses papéis podem usar o mesmo deployment em chamadas separadas. A auditoria é
automatizada; não demonstra independência entre os erros dos modelos e não substitui
revisão técnica. “Execução concluída” significa que o processamento terminou, não
que o corpus permita responder a todos os aspectos do tópico.

## Material disponível e limites

O pacote informa as entradas efetivamente utilizadas em `preparation.json`.
Nesta máquina há os dois TXT originais do Petroles, seleções originais já salvas
e passagens originais exportadas pela execução anterior. O manifesto completo
dos cinco bancos **não está instalado aqui**. Não tratamos essas seleções como
uma cópia integral de ANP, HSE, REGIS e demais bases.

Os TXT agregados nem sempre preservam título, página, fronteira documental ou
números. Essas ausências acompanham cada passagem. Não se inventam páginas nem
se contam passagens repetidas como estudos independentes. Uma relação qualitativa
pode ser aproveitada mesmo quando a dosagem foi apagada; o documento não publicará
`<NUMBER>` como se fosse um valor operacional.

A triagem lexical é ampla, mas limitada. O E5 reranqueia a união dos candidatos
dos recortes e pode promover material sem coincidência lexical naquele recorte.
Não é uma busca vetorial exaustiva sobre todos os documentos. A avaliação de
pertinência pelo pesquisador é uma segunda filtragem. A Azure não é usada para
embeddar todo o corpus nesta preparação. O modelo e a revisão do E5 são registrados.

## No servidor: instalar e executar

Na raiz do projeto, na branch `codex/qa-evidencias-verificadas`:

```bash
git pull --ff-only origin codex/qa-evidencias-verificadas
python3 -m venv .venv-documento
.venv-documento/bin/python -m pip install -r pipeline/qa_research/requirements-server.txt
.venv-documento/bin/python -m pipeline.qa_research.document check --packet pipeline/qa_research/pacotes/produtos_quimicos_v2
```

Use o `.env`/`.ini` e o certificado Azure que já funcionam no servidor.
O deployment padrão é `gpt-5-4-petrobras:low`. Não envie credenciais pelo Git.
O ambiente isolado acima evita instalar as dependências pesadas da preparação local.

Para executar em segundo plano:

```bash
nohup .venv-documento/bin/python -u -m pipeline.qa_research.document run \
  --packet pipeline/qa_research/pacotes/produtos_quimicos_v2 \
  --output pipeline/qa_research/saida_documento_produtos_quimicos_v2 \
  > documento_produtos_quimicos_v2.log 2>&1 &
```

```bash
tail -f documento_produtos_quimicos_v2.log
```

`Ctrl+C` encerra o acompanhamento do log. O processo iniciado com `nohup` continua.
O documento parcial é atualizado após cada lote de até três recortes. Leia:

```bash
cat pipeline/qa_research/saida_documento_produtos_quimicos_v2/resumo.json
cat pipeline/qa_research/saida_documento_produtos_quimicos_v2/progresso.json
```

O limite cumulativo é 500 tentativas, incluindo reparos e falhas, com até três
tentativas por pedido. Há no máximo três chamadas concorrentes. O código de saída
é 0 para processamento concluído e 2 para interrupção/pendências. Verifique o
`status` e os `recortes_pendentes` do resumo; conteúdo ausente não deve ser confundido
com erro de chamada. As durações por etapa são medidas, sem atribuir todo o tempo
fora da API ao índice.
Os tempos por etapa somam as durações dos pedidos; chamadas concorrentes podem
se sobrepor. `session_seconds` mede o tempo de parede da sessão de execução.

Para retomar, execute novamente o mesmo comando `run`, com a mesma saída. Pode
adicionar `--max-calls 700` ou `--workers 2`; o orçamento anterior não é zerado.
Pacote, modelo, parâmetros de conteúdo e código são vinculados por assinatura.
Se eles mudarem, use outra pasta. A saída lexical antiga não é reutilizada como
se tivesse sido gerada por este método. Falhas fatais de credenciais interrompem
a rodada; após corrigir a credencial no servidor, retome o comando.

## Quando terminar: devolver os resultados pelo Git

Espere o processo terminar. O coletor recusa copiar uma saída ainda em uso. Ele
inclui documento, cobertura, suporte original, versões, prompts, respostas, erros,
orçamento e manifesto com hashes. Exclui credenciais, bancos de cache e índices.

```bash
.venv-documento/bin/python -m pipeline.qa_research.document collect \
  --packet pipeline/qa_research/pacotes/produtos_quimicos_v2 \
  --output pipeline/qa_research/saida_documento_produtos_quimicos_v2 \
  --destination pipeline/qa_research/relatorios/produtos_quimicos_v2
git add -- pipeline/qa_research/relatorios/produtos_quimicos_v2
git commit -m "Resultados do documento Produtos quimicos v2"
git push origin codex/qa-evidencias-verificadas
```

O coletor também pode retornar resultados parciais após uma execução interrompida.
Para uma segunda coleta, use outro destino, preservando o primeiro snapshot.

**Aqui na máquina local**, na mesma branch:

```powershell
git pull --ff-only origin codex/qa-evidencias-verificadas
```

Abra `pipeline/qa_research/relatorios/produtos_quimicos_v2/documento_auditado.md`
ou o notebook `documento_produtos_quimicos.ipynb`. O manifesto permite conferir
se os arquivos devolvidos permanecem iguais aos coletados.

## Próxima rodada local, se faltarem fontes

A preparação usa pesos E5 em cache, revisão fixada; o modo offline não baixa
modelos silenciosamente. Na primeira preparação de outra máquina, instale as
dependências de `requirements-local.txt` e disponibilize os pesos com:

```powershell
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('intfloat/multilingual-e5-small', revision='614241f622f53c4eeff9890bdc4f31cfecc418b3')"
```

Depois, somente aqui:

```powershell
python -m pipeline.qa_research.document prepare --profile pipeline/qa_research/configs/documento_produtos_quimicos.json --feedback pipeline/qa_research/relatorios/produtos_quimicos_v2/pedidos_busca.json --destination pipeline/qa_research/pacotes/produtos_quimicos_v3
```

Hashes dos originais, fronteira lexical e embeddings de candidatos ficam em
`.local/document/`, reutilizados quando suas entradas não mudam. Pedidos novos
mudam a triagem e podem exigir uma nova leitura local. Adicionar os bancos ausentes
ao manifesto local melhora o alcance; o feedback sozinho não cria documentos que
não existem aqui. Envie o novo pacote pelo Git e use outra saída no servidor.

Os prompts completos estão em `document/prompts.py`; os de cada chamada ficam em
`chamadas/`. O plano anterior de QA permanece disponível para desenvolvimento
futuro, sem ser chamado pelo fluxo documental v2.
