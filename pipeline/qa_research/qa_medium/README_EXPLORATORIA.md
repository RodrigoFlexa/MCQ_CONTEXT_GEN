# Rodada exploratória: extensão da resposta

Compara três instruções de extensão, nas mesmas 1.000 perguntas Sem contexto e
1.000 Default + Ampliado do manifesto `amostras_1000.json` (semente 20261028,
repetição 1). Não gera nem seleciona novas perguntas.

| Braço | Instrução | Respondentes | Juiz |
|---|---|---|---|
| p50 | Até 50 palavras | GPT-5.4 Nano e GPT-5.4, medium | GPT-5.4, medium |
| p100 | Até 100 palavras | Os mesmos, medium | O mesmo |
| concisa_livre | Sem limite numérico de palavras, resposta concisa e suficiente | Os mesmos, medium | O mesmo |

O texto dos prompts muda somente nas instruções de extensão. `p100` reproduz
exatamente o prompt da rodada concluída `qa_100_palavras_medium_1000`. O prompt do
juiz é idêntico nos três braços e verifica suficiência técnica, sem bonificar
extensão. O juiz recebe pergunta, referência e resposta candidata, com IDs locais:
não recebe identidade do respondente, braço nem origem da pergunta. Variantes da
mesma pergunta ficam em lotes distintos. Os lotes têm até 8 respostas do mesmo
respondente/braço, com trabalhadores de julgamento separados dos respondentes.

São 12.000 casos de resposta: 2.000 perguntas × 3 braços × 2 modelos. As **4.000
respostas e respectivas notas de p100 são reaproveitadas** da rodada concluída;
restam **8.000 respostas novas**, mais seus julgamentos e duas sondagens de
disponibilidade por execução. O reaproveitamento confere conteúdo e IDs, modelos,
esforço, ambos os prompts, lote do juiz, respostas, notas e conclusão. Se houver
divergência, interrompe antes de chamar modelos. Mantém os lotes e bloqueios
originais de p100. Não usa as respostas históricas de 50 palavras/low como p50.

## Executar no servidor

```bash
git pull --ff-only origin codex/qa-evidencias-verificadas &&
bash pipeline/qa_research/rodar_qa_exploratoria.sh
```

O comando retoma automaticamente os checkpoints da mesma saída. Há acurácia ao
vivo para cada combinação de conjunto, braço e modelo, desde os primeiros lotes;
p100 já aparece com seus resultados reaproveitados. As tarefas de 50 palavras e
concisa livre são intercaladas entre conjuntos e executadas em paralelo nos dois
respondentes. A acurácia parcial reflete apenas as respostas já julgadas.

```bash
# Verificar dados e reaproveitamento, sem API nem criação de saída:
bash pipeline/qa_research/rodar_qa_exploratoria.sh --plano

# Salvar também o terminal, preservando o código de erro:
set -o pipefail
bash pipeline/qa_research/rodar_qa_exploratoria.sh 2>&1 | tee qa_exploratoria.console.log
```

Opções: `--saida`, `--workers 8`, `--judge-workers 2`, `--manifesto` e
`--referencia-100`. A referência padrão já está versionada. Prompts, amostras,
modelos, esforço, braços e tamanho do lote são fixados no protocolo. Workers
podem variar na retomada. Mudança de protocolo exige outra pasta de saída.

## O que é medido

Acurácia principal = corretas / respostas com nota técnica. Parcial e incorreta
não contam como corretas. As três categorias e justificativas são preservadas;
o indicador histórico com meia pontuação para parcial também permanece na tabela
geral. Bloqueios ficam sem nota e com cobertura explícita; não são reenviados,
divididos em novos lotes nem tratados como erro técnico. Falhas transitórias
ficam pendentes para retomada com o mesmo comando.

Os limites de palavras são **instruções no prompt**. Respostas acima de 50 ou 100
não são cortadas, regeneradas nem excluídas. Registramos tamanho real e violações.
No braço livre não há teto numérico de palavras, mas continua existindo o mesmo
orçamento técnico por chamada: 8.000 tokens iniciais, com a política já existente
de repetição por limite de tokens até o teto de 16.000 (inclusive raciocínio e
saída). Portanto, não se trata de saída infinita. Logs preservam tokens, motivos
de término e tentativas; os limites são iguais em todos os braços.

Os respondentes recebem somente a pergunta. “Com contexto” descreve a origem da
geração do dataset. Não há material técnico, gabarito ou comentário de especialista
na entrada do respondente. Não há novos filtros, deduplicação, refinamento ou
remoção de questões nesta rodada. IDs de transporte recebem prefixo do braço;
`uid_original` e os textos originais são preservados para comparação pareada.

Esta ablação compara a instrução de extensão com esforço e juiz mantidos. O
reaproveitamento de p100 conserva a data e os lotes daquela avaliação; os braços
novos são executados depois. Deployments podem mudar e julgamentos podem variar.
Uma execução por item não elimina essas fontes de variação nem estabelece que
qualquer efeito seja causado exclusivamente por contagem de palavras. O teste
não isola o efeito de esforço low/medium da comparação histórica e não substitui
uma auditoria humana do juiz e dos gabaritos. Depois da rodada, convém examinar
discordâncias pareadas e erros por tamanho, além das médias globais.

## Resultados para coleta e gráficos

Pasta: `pipeline/qa_research/relatorios/qa_exploratoria_limites_medium_1000`.

- `config.json`, `amostras.json`, `questoes.jsonl`: protocolo e dados congelados.
- `avaliacao/ACURACIA.md`, `acuracia.json`, `acuracia_por_condicao.csv`: atualizados
  a cada lote, por conjunto/braço/modelo; cobertura e corretas/parciais/incorretas.
- `avaliacao/resumo_exploratorio.csv`: 12 combinações, acurácia, cobertura,
  média/máximo de palavras, violações do limite e quantidade reaproveitada.
- `avaliacao/comparacao_mesmas_questoes.csv`: acurácia dos três braços no mesmo
  subconjunto de perguntas com nota em todos eles, separadamente por conjunto/modelo.
  Serve para verificar sensibilidade a denominadores diferentes por bloqueios.
- `avaliacao/avaliacoes.jsonl`: questão, referência, respostas, notas, justificativas,
  status, contagem de palavras, braço, origem e sinalização de reaproveitamento.
- `avaliacao/reaproveitamento_p100.json`, `protocolo_experimento.json`, diretórios
  `respostas/` e `juiz/`: evidências e checkpoints. `avaliacao_concluida.json` só é
  escrito quando todos os casos têm resultado terminal, inclusive bloqueios.

O script imprime coleta, commit e push ao terminar. As avaliações históricas
ficam preservadas em suas pastas. O código e os testes locais não fazem chamadas
pagas; elas só começam ao executar o comando no servidor sem `--plano`.
