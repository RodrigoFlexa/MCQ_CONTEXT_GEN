# Piloto: somente documentos de KPI

O inventário organiza a frase do especialista em assuntos, recupera trechos das cinco coleções,
extrai afirmações com citações, separa conflitos e escreve fichas e um documento técnico do tópico.
Esta execução **não gera perguntas**. O gerador antigo da fase_4 ainda não consome este inventário.

## Ambiente e credenciais

Na raiz do repositório, no servidor Linux, use o ambiente Python já configurado:

```bash
python3 -m pip install -r pipeline/inventario/requirements_azure.txt
```

As credenciais são as mesmas do backend corporativo existente (`azure_openai_backend.py`):
`.env` com `AZURE_OPENAI_ENDPOINT`, `AZURE_OPENAI_API_KEY`, `AZURE_OPENAI_API_VERSION`,
ou `AOAI_CONFIG_INI`, `AOAI_CONFIG_SECTION` e `AOAI_CA_BUNDLE`. Não copie credenciais para o Git.
O certificado é validado; endpoints de gateway são tratados como `base_url` quando necessário.

Padrões do piloto: `gpt-5-4-petrobras`, effort `medium`, embeddings exclusivamente
`embedding-3-large-global` (3072 dimensões), dois pedidos LLM simultâneos.
Sem reranker local: a ordenação usa cosseno dos embeddings Azure e MMR.
Isso não reproduz o cross-encoder BGE do Claude; o score de cosseno não é probabilidade de relevância.
Nenhum modelo local é executado em CPU. A varredura lexical e a escrita de arquivos usam CPU normalmente.

## Sequência no servidor

```bash
# 1. Confere as cinco coleções, hashes e o recorte; zero chamadas aos modelos.
bash pipeline/inventario/run_piloto_azure.sh --plan

# 2. Um pedido de JSON ao LLM e um lote de dois textos aos embeddings.
# Esse teste usa a API e tem custo. Não usa cache de resposta ou de embeddings.
bash pipeline/inventario/run_piloto_azure.sh --check-api

# 3. Piloto completo do tópico KPI, produzindo somente documentos e fichas.
bash pipeline/inventario/run_piloto_azure.sh
```

Se quiser inspecionar a seleção antes de extrair unidades:

```bash
bash pipeline/inventario/run_piloto_azure.sh --parar-apos selecao
# Após inspecionar selecao.json, execute novamente sem --parar-apos.
```

No Windows, os equivalentes são:

```powershell
python -m pip install -r pipeline/inventario/requirements_azure.txt
powershell -ExecutionPolicy Bypass -File pipeline/inventario/run_piloto_azure.ps1 -Plan
powershell -ExecutionPolicy Bypass -File pipeline/inventario/run_piloto_azure.ps1 -CheckApi
powershell -ExecutionPolicy Bypass -File pipeline/inventario/run_piloto_azure.ps1
```

## Saída e acompanhamento

Pasta padrão: `pipeline/inventario/saida_piloto_kpi_azure/`.

- `execucao.log`: etapas, contagens e tempos.
- `chamadas_llm.jsonl` e `chamadas_embeddings.jsonl`: pedidos e erros, sem chaves.
- `documentos_topicos.json`: caminho do documento técnico reunido em `topicos/`.
- `subtopicos/*/fichas/*.md` e `.json`: unidades por assunto e fontes.
- `subtopicos/*/selecao.json`: trechos originais e scores; indispensável para avaliar pertinência.
- `cobertura.md` e `cobertura.csv`: cobertura e assuntos sem evidência utilizável.
- `falhas_extracao.json`: falhas de execução; não são tratadas como falta de conhecimento nos corpora.
- `resumo.json`: resumo da última execução bem-sucedida.

```bash
tail -f pipeline/inventario/saida_piloto_kpi_azure/execucao.log
```

Repetir o comando retoma do cache. Alterações de modelo, esforço, trechos ou seleção exigem nova saída.
Pode mudar workers, limite de chamadas e etapa final mantendo os demais parâmetros.
O teto de 400 chamadas LLM vale por invocação, inclui tentativas e não inclui os pedidos de embeddings.
É uma proteção de custo, não um critério científico de parada. Duas execuções não podem usar a mesma saída.

## O que avaliar antes de ampliar

1. Os assuntos são literais e cobrem a frase do especialista?
2. Os trechos são pertinentes e os limites de aplicação estão preservados?
3. Fórmulas, números, unidades e condições conferem com as fontes? Citação literal não prova essa coerência.
4. Os conflitos mantêm as versões divergentes? Eles ficam fora das unidades utilizáveis para QA.
5. Os assuntos sem contexto são ausência real de evidência, não erro de API?

O documento é uma reunião das fichas, sem uma nova síntese do modelo. A afirmação canônica da consolidação
ainda é produzida pelo LLM e deve ser conferida com as unidades originais preservadas.
O modo `sem_contexto` é uma indicação para a futura geração, não uma geração já implementada neste inventário.

## Testes offline

```bash
python3 -m unittest discover -s pipeline/inventario/tests -v
```

Testam serviços simulados; o sucesso deles não certifica acesso à Azure nem qualidade factual dos documentos reais.
Integração Azure segundo a [documentação oficial do SDK](https://developers.openai.com/api/reference/python);
entradas, lotes e limites de embeddings conforme a [referência da API](https://developers.openai.com/api/reference/python/resources/embeddings/methods/create).
