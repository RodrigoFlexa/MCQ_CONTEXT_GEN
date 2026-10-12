# Inventário de conhecimento do PetroQuest

## Piloto atual: Azure, somente documentos de KPI

Leia **[PILOTO_AZURE.md](PILOTO_AZURE.md)** para instalação, comandos Linux/Windows,
validação de conectividade e acompanhamento. O padrão atual usa `gpt-5-4-petrobras`
com effort medium e `embedding-3-large-global` (3072 dimensões).

```text
frase do especialista → assuntos literais → varredura lexical nos cinco corpora
→ embeddings Azure + cosseno + MMR → extração de unidades com citações
→ consolidação e conflitos → fichas por assunto → documento técnico por tópico
```

O inventário não gera perguntas. `assuntos_para_geracao.jsonl` é um contrato para
uma integração futura; o gerador da fase_4 ainda não o consome.

## Arquivos produzidos

- `topicos/*/documento_tecnico.md`: reúne as fichas, preservando condições e fontes.
- `documentos_topicos.json`: índice dos documentos.
- `subtopicos/*/assuntos.json`: programa de conteúdo e consultas em português/inglês.
- `subtopicos/*/selecao.json`: trechos originais, proveniência e scores.
- `subtopicos/*/fichas/*.md` e `.json`: conhecimento utilizável e conflitos separados.
- `unidades_brutas.jsonl`, `unidades_descartadas.jsonl`, `unidades_consolidadas.jsonl`:
  extração, descartes e consolidação auditáveis, dentro de cada subtópico.
- `cobertura.md`, `cobertura.csv`: assuntos com contexto, parcial ou sem contexto.
- `falhas_extracao.json`: erros de execução; não viram ausência de contexto.
- `execucao.log`, `resumo.json`, `chamadas_llm.jsonl`, `chamadas_embeddings.jsonl`: execução e uso.

## Retomada e validação

Hashes dos corpora são verificados antes das chamadas, inclusive na retomada.
Caches distinguem modelos, endpoint e orçamento de resposta. A configuração
experimental fica fixa por saída; workers, limite de chamadas e etapa final podem mudar.
Os registros de extração são ordenados e duas execuções não podem escrever na mesma saída.

Citações precisam ser contíguas, sem trocar números, operadores ou negações.
Elas toleram caixa, acentos e espaços. A presença da citação não comprova que toda
a afirmação é correta ou que o princípio é aplicável a um FPSO.

Conflitos preservam as afirmações originais e não contam como conhecimento
utilizável. Um assunto sem evidência permanece identificado para a futura geração
sem contexto; falhas de API interrompem o processo em vez de produzir esse status.

## Opção local com GPU

O caminho originalmente criado pelo Claude continua disponível mediante escolha
explícita de `--embedder BAAI/bge-m3 --reranker BAAI/bge-reranker-v2-m3`.
Esses modelos exigem CUDA e as dependências em `requirements.txt`;
`setup_gpu.ps1` prepara um ambiente Windows separado. Não há fallback CPU.
`--embedder hash` é somente um substituto determinístico para testes offline.
Nenhum deles é usado automaticamente no piloto Azure.

## Limitações a avaliar no piloto

- A triagem lexical pode perder material sem os termos pesquisados.
- Sem cross-encoder local, o score é cosseno; o limiar não é uma probabilidade calibrada.
- Trechos padrão: 350 palavras, stride 250, até 12 por assunto; isso difere da v6 (10×1000 por faceta).
- Petrolês substitui números por `<NUMBER>` e não identifica fronteiras confiáveis de documento.
- Extração e consolidação dependem do julgamento do LLM; citações não são uma auditoria factual independente.
- O agrupamento por similaridade pode deixar conflitos entre unidades de grupos diferentes sem detecção.
- Não há integração com geração/refino/julgamento de QA nesta etapa.

## Testes

```bash
python -m unittest discover -s pipeline/inventario/tests -v
```

Os testes não usam rede ou GPU; a conectividade real é verificada por `--check-api` no servidor.
