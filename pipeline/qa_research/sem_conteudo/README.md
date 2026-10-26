# Geração sem conteúdo externo

Baseline para comparar com `geracao_final_20261024T204734Z`. O objetivo é gerar
**2.818 questões aprovadas automaticamente nos mesmos 40 subtópicos**, com a mesma
quantidade final por subtópico: 62 em Gestão do Desempenho, 159 em Produtos químicos,
70 em Offloading etc. As refinadas da referência entram nas metas.

O servidor lê somente `metas_geracao_final_20261024.json`: rótulos do programa,
frases originais do especialista e contagens. Não precisa ler o banco de referência.
Documentos, blocos, inventários, encadeamentos, pesquisas, exemplos, contraexemplos
e bancos dinâmicos anteriores não são carregados. Não há datasets externos de QA.

## Executar no servidor

Na instalação já usada para a run final, com as mesmas credenciais Azure:

```bash
cd /home/gbs2/MCQ_CONTEXT_GEN
git pull --ff-only origin codex/qa-evidencias-verificadas
bash pipeline/qa_research/rodar_sem_conteudo.sh \
  --saida pipeline/qa_research/relatorios/sem_conteudo_v1
```

O script escolhe `.venv-documento/bin/python`, depois `venv/bin/python` e por último
`python3`. `DOCUMENT_PYTHON` pode indicar explicitamente outro Python. Não são
necessárias novas bibliotecas além de `requirements-server.txt`.

Esse comando faz a geração e, **somente se todas as metas forem alcançadas**, a
avaliação existente com os seis respondentes, em pares, e juiz em lotes. A tabela
fica em `<saida>/avaliacao/ACURACIA.md`. Para gerar sem essa avaliação, acrescente
`--sem-avaliacao`. Para retomar somente a avaliação, use a mesma saída com
`--so-avaliacao`.

Para executar em segundo plano e acompanhar:

```bash
nohup bash pipeline/qa_research/rodar_sem_conteudo.sh \
  --saida pipeline/qa_research/relatorios/sem_conteudo_v1 \
  > pipeline/qa_research/relatorios/sem_conteudo_v1.console.log 2>&1 &
tail -F pipeline/qa_research/relatorios/sem_conteudo_v1.console.log
```

Interromper o acompanhamento com Ctrl+C não encerra a execução iniciada por nohup.
Para uma run independente, use outra pasta de saída.

## Conferir sem consumir API

```bash
bash pipeline/qa_research/rodar_sem_conteudo.sh --plano
```

Esse comando lista as 40 metas, não carrega credenciais e não cria a saída.
Um piloto com a meta real de um único subtópico:

```bash
bash pipeline/qa_research/rodar_sem_conteudo.sh \
  --saida pipeline/qa_research/relatorios/sem_conteudo_piloto_kpi \
  --itens 01_01 --sem-avaliacao
```

## Método e limites

- Gerador, auditor, refinador e deduplicador: `gpt-5-4-petrobras:high`.
- Lotes de até 5 questões, com memória das últimas 20 versões geradas **na nova
  run e no mesmo subtópico**. Inclui versões reprovadas para desencorajar repetição;
  a memória não é apresentada como evidência nem exemplo de qualidade.
- A auditoria avalia escopo, plausibilidade, univocidade, tipo e defeitos de redação
  sem consultar fontes. Os filtros de formato do pipeline anterior são reutilizados.
- Até duas tentativas de refinamento por questão reprovada. O refinador vê o escopo,
  a questão, a crítica e a memória da run, sem documento e sem exemplos anteriores.
- Quase duplicatas lexicais de enunciados (Jaccard ≥ 0,6) não contam. Ao atingir a
  meta provisória, há deduplicação por sentido de todas as aprovadas do subtópico.
  As removidas são repostas, e a deduplicação é repetida antes da conclusão.
- O total final é exato quando concluído. Não há cotas por tipo ou composição.
  Esses campos são classificados pelo que a questão exige; a composição não tem
  proveniência documental nesta condição. A diferença de composição deve ser
  considerada na comparação com a run anterior.
- Limites padrão: 100 lotes cumulativos por subtópico, 10 lotes seguidos sem
  progresso e 30.000 tentativas de API cumulativas para geração/auditoria/refino/dedup.
  O orçamento inclui reparos e retentativas do cliente. A avaliação dos seis modelos
  é uma etapa separada com o orçamento do avaliador existente.
- Se uma meta ou chamada falhar, o comando retorna código 2, salva o progresso e
  **não inicia a avaliação**. Relatórios parciais não significam sucesso. Questões
  de tópicos incompletos ainda podem estar pendentes de deduplicação por sentido.
- Não há deduplicação global entre subtópicos: avalie a similaridade global ao final,
  usando o mesmo protocolo aplicado ao banco de referência.

As questões são aprovadas por revisão paramétrica do modelo, **não por comprovação
documental nem revisão humana**. A acurácia dos respondentes mede o desempenho
contra a resposta gerada, não estabelece verdade técnica. Correção técnica exige
avaliação independente dos dois bancos. Essa comparação envolve duas abordagens
com processos diferentes, não uma ablação que altera apenas o texto de contexto.

## Retomar

Repita o comando com a mesma `--saida`. Cada lote é uma transação: checkpoint
atômico depois da geração, auditoria e refino; o cache permite repetir um lote
interrompido. Tópicos concluídos não geram novas chamadas. Um bloqueio impede duas
execuções simultâneas na mesma saída.

Se o relatório apontar limite atingido, aumente apenas os limites necessários:

```bash
bash pipeline/qa_research/rodar_sem_conteudo.sh \
  --saida pipeline/qa_research/relatorios/sem_conteudo_v1 \
  --max-lotes 150 --max-sem-progresso 15 --max-chamadas 45000
```

Esses limites são cumulativos, não reiniciam contagens. Mudanças nas metas,
escopos, modelos, prompts, memória, lote, refinos ou código exigem outra saída.
Se a primeira execução usou `--itens`, a retomada sem `--itens` reutiliza a seleção.
Outras opções não padrão, como `--lote`, devem ser repetidas.

## Arquivos e coleta

- `aprovadas.jsonl`: banco final ou parcial; inclui as refinadas aprovadas.
- `questoes.jsonl`: todas as versões processadas, com auditoria e motivos de exclusão.
- `resultado.json` e `RELATORIO.md`: metas, quantidades, origem, tipo e falhas.
- `topicos/<id>/estado.json`: checkpoint com memória, versões e eventos de dedup.
- `topicos/<id>/finalizado.json`: só existe quando a meta foi deduplicada e atingida.
- `geracao_concluida.json`: só existe quando todos os tópicos selecionados terminaram.
- `config.json`, `metas.json`, `limites_execucao.json`, `orcamento.json`: protocolo,
  hashes e limites. `chamadas/` registra uso de API; `.local/` mantém cache e respostas
  brutas locais, ignorados pelo Git.

Ao terminar, o script mostra a mensagem de conclusão e os comandos concretos:

```bash
git add -- pipeline/qa_research/relatorios/sem_conteudo_v1
git commit -m "Resultados: sem_conteudo_v1"
git push origin codex/qa-evidencias-verificadas
```

Na máquina local: `git pull --ff-only origin codex/qa-evidencias-verificadas`.

O manifesto foi preparado uma vez por
`python -m pipeline.qa_research.sem_conteudo.preparar_metas`. Essa ferramenta de
preparação lê a referência apenas para contar e verificar IDs; a geração não a importa.
