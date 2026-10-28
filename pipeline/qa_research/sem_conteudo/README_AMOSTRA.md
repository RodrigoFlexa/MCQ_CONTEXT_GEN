# Acurácia da amostra fixa de 1.000 questões sem contexto

Avalia exatamente o **primeiro sorteio sem contexto** já usado na análise de
amostras de 1.000 questões: semente 20261028, 1.000 IDs únicos, sem reposição,
da fonte sem_conteudo_bruto_v1 (2.818 QAs). IDs, ordem, hashes da fonte e da
seleção estão congelados em amostra_1000.json, versionado com o código.
O servidor não precisa dos arquivos locais dos gráficos nem de NumPy.

## Servidor

```bash
git pull --ff-only origin codex/qa-evidencias-verificadas &&
bash pipeline/qa_research/rodar_sem_conteudo_amostra.sh
```

O comando só copia a seleção congelada para uma nova saída e avalia as
1.000 perguntas com GPT-5.4 Nano e GPT-5.4 (esforço low), no mesmo grupo em
paralelo. Os respondentes recebem somente a pergunta, sem contexto, parecer,
resposta de referência ou alternativas. O juiz é gpt-5-4-petrobras:medium,
lotes de 8; prompts e regras de avaliação iguais aos do Full.

Não gera nem refina perguntas, não amplia o banco para 4.111 e não exige
concluir essa expansão. Nenhuma pergunta é excluída por repetição ou dificuldade.
Não rotula a amostra como aprovada. É possível executar esta avaliação
independentemente da geração Full, em pasta distinta.

Saída: pipeline/qa_research/relatorios/sem_conteudo_amostra_1000.
Serão **2.000 respostas**, mais julgamentos e duas sondagens de disponibilidade
por execução. Repita o mesmo comando para retomar; não refaz respostas/notas
salvas. Falhas transitórias deixam pendências. Ambos os modelos são obrigatórios.
Bloqueios do provedor são terminais, sem nota, com cobertura explícita; lotes
bloqueados não são divididos ou reenviados. Acurácia = corretas / respostas com
nota; a métrica alternativa conta parcial como 0,5. O gabarito original do
gerador é usado como referência; não há validação documental nova das QAs.

```bash
# Conferência sem API, sem criar saída:
bash pipeline/qa_research/rodar_sem_conteudo_amostra.sh --plano
```

Opções: --saida, --workers 8, --lote-juiz 8, --manifesto e --fonte.
Mudar fonte, seleção, textos, prompts ou protocolo bloqueia a retomada.
Workers podem variar; lote do juiz deve ser preservado. Não troque o manifesto
para tentar melhorar acurácia após conhecer os resultados.

Arquivos: questoes.jsonl (seleção intacta), amostra.json, config.json;
avaliacao/ACURACIA.md, acuracia.json, acuracia.csv, avaliacoes.jsonl,
protocolo_experimento.json, avaliacao_concluida.json, respostas/ e juiz/.

**Esta acurácia corresponde a um único sorteio fixo de 1.000 questões.**
Os gráficos anteriores mostram médias de 100 sorteios. Para comparação direta,
usar também o primeiro sorteio das demais condições, cujas respostas já existem;
não apresentar esta única avaliação como média dos 100 sorteios sem contexto.
Os IDs compartilhados entre sorteios não tornam a avaliação deste subconjunto
uma avaliação completa das 2.818 questões.

Ao finalizar, o script imprime a mensagem de término e os comandos para coleta,
commit e push dos resultados.
