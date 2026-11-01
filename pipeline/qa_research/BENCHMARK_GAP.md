# Gap com/sem contexto e sustentação dos gabaritos — todas as QAs do Default

Executa nas **2.818 questões próprias do Default**, incluindo refinadas, de todos
os 40 subtópicos. Não é amostra. Exclui as conversões dos DOCX e o dataset gerado
sem conteúdo externo: o experimento compara entradas diferentes na MESMA questão.

```bash
git pull --ff-only origin codex/qa-evidencias-verificadas &&
bash pipeline/qa_research/rodar_benchmark_gap.sh
```

O servidor usa fontes já versionadas, sem os artefatos locais de análise em docs/:
`geracao_final_20261024T204734Z/aprovadas.jsonl` e os documentos
`relatorios/dez_areas_final_v2`. Reconstrói a janela de três blocos ou os blocos
do encadeamento. Refinadas mantêm os vínculos originais. Salva contextos e hashes
na saída; não modifica questões, gabaritos, documentos nem datasets externos.

## Protocolo controlado

- GPT-4.1 Nano, GPT-4.1 Mini e GPT-4.1, sem parâmetro effort. Deployments padrões:
  gpt-4-1-nano-petrobras, gpt-4-1-mini-petrobras e gpt-4-1-petrobras.
- Cada modelo responde às mesmas 2.818 perguntas em closed-book (`contexto=null`)
  e open-book (somente texto dos blocos de geração, sem metadados de auditoria,
  exemplos de QA, encadeamento/resposta esperada ou gabarito anexado).
- Mesmo prompt e instrução de até 100 palavras nos dois braços; respostas acima
  do limite são preservadas e contadas, sem truncamento ou regeneração por extensão.
- Orçamento inicial 8.000 tokens por resposta/julgamento; cliente existente pode
  repetir por truncamento até o teto de 16.000. Juiz GPT-5.4 medium, mesma rubrica
  nos dois braços. O juiz recebe Q, gabarito e candidato, sem modelo, braço ou contexto.
- Lotes de até oito; braços separados antes das chamadas. Não compara variantes
  da mesma pergunta no mesmo lote. Resposta e julgamento avançam em paralelo,
  com acurácia ao vivo por braço/modelo. Cada chamada é independente.

São **16.908 casos de resposta novos**, mais julgamentos. Regera closed-book:
não mistura o protocolo histórico de 50 palavras/juiz anterior com o novo braço
open-book. Nenhum novo resultado sobrescreve avaliações históricas.

Os três deployments são obrigatórios. A sondagem inicial não remove um modelo
indisponível nem o substitui. Se o nome do deployment Mini na sua conta for outro:

```bash
bash pipeline/qa_research/rodar_benchmark_gap.sh --mini-deployment NOME_DO_DEPLOYMENT_MINI
```

Use o nome real do GPT-4.1 Mini, sem sufixo de effort. Não muda de modelo.
Falha de disponibilidade encerra antes da rodada principal; veja falha_execucao.json.
Se já iniciou com um nome incorreto, forneça também `--saida` com uma pasta nova
ao corrigir o deployment: os modelos ficam congelados desde a criação da saída.
Prompts, dados, modelos e código ficam congelados no protocolo; retomadas com
mudanças recusam a mistura. Workers podem variar. Não há opção de limitar a amostra.

```bash
# Sem API, sem custos e sem criação de pasta:
bash pipeline/qa_research/rodar_benchmark_gap.sh --plano

# Retomar: repetir o comando com a mesma saída e deployment.
# Opcional: --workers 8 --judge-workers 2 --saida OUTRA_PASTA
```

## Faithfulness automática adicional

Após QA, executa **2.818 auditorias**, uma por gabarito/contexto. GPT-5.4 medium
decompõe A em afirmações, indica cobertura completa e classifica cada afirmação
como sustentada, contradita ou insuficiente. Sustentada/contradita exigem trechos
literais, validados por código contra os blocos. IDs/citações inválidos geram
falha de validação, não aceitação automática. Literalidade não prova entailment;
as justificativas e evidências ficam disponíveis para auditoria.

A decisão do gabarito é derivada das afirmações: totalmente sustentado, contradição,
suporte insuficiente ou inconclusivo (decomposição incompleta). Bloqueios são
terminais e separados. A taxa principal exclui bloqueios e inconclusivos, com
denominadores explícitos. Também são exportadas as contagens por afirmação.

É uma avaliação automática em nova chamada, com a mesma família do gerador,
sem acesso ao parecer anterior; não equivale a validação humana independente.
O CSV de revisão humana seleciona deterministicamente até 25 casos por resultado,
com os estratos registrados. Essa amostra estratificada não deve ser usada como
estimativa simples da taxa global sem ponderação. As notas das questões não são
alteradas por esse parecer; a análise posterior pode mostrar sensibilidade ao
subconjunto de gabaritos sustentados sem descartar silenciosamente o restante.

## Resultados e coleta

Saída padrão: `pipeline/qa_research/relatorios/benchmark_gap_full_v1`.

- `config.json`, `contextos.jsonl`, `questoes.jsonl`: dados e protocolo congelados.
- `avaliacao/ACURACIA.md`, `acuracia_por_condicao.csv`: acurácia estrita por braço
  e modelo, além de corretas/parciais/incorretas, cobertura e progresso ao vivo.
- `avaliacao/avaliacoes.jsonl`, `respostas/`, `juiz/`: textos, notas e checkpoints.
- `gap_pareado.csv`: open − closed em pontos percentuais, somente nas MESMAS
  perguntas com nota nos dois braços; ganhos, perdas e pares excluídos.
- `pares.csv`: uma linha por questão/modelo, permitindo McNemar e bootstrap locais.
- `faithfulness.jsonl`, `faithfulness/`: pareceres por afirmação com evidências.
- `faithfulness_resumo.json`, `amostra_revisao_humana.csv`: cobertura e revisão.
- `rodada_concluida.json`: todas as questões/modelos/braços e auditorias têm
  resultado terminal, inclusive bloqueios. Falhas transitórias deixam pendências
  e retorno 2; repetir o comando retoma somente o que falta. Bloqueios do provedor
  não são reenviados nem divididos em lotes para contornar filtros.

O script imprime os comandos de coleta, commit e push. Não versionar `.local`:
o .gitignore vigente já exclui cache e respostas brutas locais. Ao trazer a pasta
de resultados para cá, será possível calcular gap, intervalos pareados, transições,
sustentação e sensibilidade à qualidade dos gabaritos.

### Retomada da falha de exportação CSV (01/11/2026)

Se apareceu `need to escape, but no escapechar set`, atualize o código e repita
o mesmo comando. A correção preserva controles e aspas usando QUOTE_ALL e escape
explícito. Ao ler esses CSVs em Python, use `csv.DictReader(..., escapechar='\\')`;
os JSONL continuam sendo a fonte integral dos textos. A compatibilidade aceita
somente o hash conhecido da implementação anterior e exige dados, modelos,
prompts e demais parâmetros idênticos. O protocolo original fica preservado,
com registro em compatibilidade_retomada.json. Se respostas e notas já estiverem
completas, nenhuma sondagem ou resposta é refeita; a execução segue para a
auditoria de sustentação que ainda falta.

Lematização e análise sintática de repetitividade são etapas locais separadas;
este comando completa os dados que exigem chamadas aos modelos. Não recalcula
Vendi/Self-BLEU, já disponíveis. A avaliação humana continua pendente até preenchida.

Rubrica e desenho seguem [boas práticas de avaliação OpenAI](https://developers.openai.com/api/docs/guides/evaluation-best-practices):
condições controladas, critérios claros e conferência humana do juiz.
