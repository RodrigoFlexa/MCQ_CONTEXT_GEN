# Sem contexto com o mesmo tamanho do Full

O Full tem 4.111 QAs: Default (2.818) + Ampliado (670) + Especialista (623).
Esta execução preserva as 2.818 QAs do baseline bruto e gera **mais 1.293**.
As metas finais são idênticas às do Full em cada um dos 40 subtópicos.
Não usa o banco local das análises: as contagens e os escopos foram congelados
em metas_full_4111.json, versionado junto ao código.

## Rodar no servidor

```bash
git pull --ff-only origin codex/qa-evidencias-verificadas &&
bash pipeline/qa_research/rodar_sem_conteudo_full.sh
```

Esse comando completa a geração e avalia **todas as 4.111 QAs**, incluindo
as 2.818 anteriores, com GPT-5.4 Nano e GPT-5.4 em paralelo (esforço low).
O juiz é gpt-5-4-petrobras:medium, lote de 8, com os mesmos prompts usados
nas outras ablações. Os respondentes recebem somente a pergunta.
Não há avaliação antiga do baseline a reaproveitar nesta execução.

Saída padrão: pipeline/qa_research/relatorios/sem_conteudo_full_4111.
Repita o mesmo comando para retomar após interrupção. Respostas e julgamentos
já salvos não são refeitos. Há duas sondagens de disponibilidade por execução.
Falha de um modelo obrigatório impede conclusão; não é descartado silenciosamente.

```bash
# Conferir metas sem API e sem criar saída:
bash pipeline/qa_research/rodar_sem_conteudo_full.sh --plano

# Só terminar a avaliação após geração concluída:
bash pipeline/qa_research/rodar_sem_conteudo_full.sh --so-avaliacao
```

Outras opções: --workers 8, --lote 5, --memoria 20, --max-lotes 100,
--max-chamadas 30000, --lote-juiz 8, --sem-avaliacao e --saida.
Lote, memória e demais parâmetros experimentais devem ser mantidos na retomada;
os limites podem ser aumentados. --max-lotes conta também os lotes históricos
preservados; --max-chamadas limita tentativas da nova geração, incluindo reparos
estruturais. Avaliação tem seus próprios limites de cliente, herdados do avaliador.

## Condição experimental

- Gerador gpt-5-4-petrobras:high, mesmo prompt e regras do baseline bruto.
- Entradas: tópico, subtópico, frase do programa e últimas 20 QAs **do próprio
  baseline sem contexto**, incluindo as anteriores do mesmo subtópico.
- Nenhuma QA do Full, MCQ, parecer, documento técnico ou exemplo externo é
  enviado ao gerador. A preparação offline lê as fontes somente para contar.
- IDs, textos e classificações das 2.818 QAs antigas são preservados integralmente.
  Novos IDs continuam a numeração por subtópico; não sobrescreve a run anterior.
- Sem refinamento, auditoria de qualidade, deduplicação ou filtros de similaridade.
  Repetidas e questões fracas contam para a meta. Só se valida estrutura/quantidade.
- Seis tipos e composição simples/composta continuam declarados pelo gerador,
  sem cotas nem correção. **Igualamos tamanho e contagem por subtópico, não a
  distribuição por tipo.** Isso preserva a condição original de geração.

## Dificuldade e limites da comparação

A avaliação não aprova/reprova perguntas nem as remove: mede acertos, parciais,
erros e cobertura das respostas. Acurácia = corretas / respostas com nota;
a métrica alternativa atribui 0,5 a parciais. Bloqueio do respondente ou juiz é
terminal e fica sem nota, fora do denominador; o lote bloqueado não é dividido
ou reenviado. Falhas transitórias ficam pendentes para retomada.

O gabarito é produzido pelo gerador: o juiz de respostas não faz uma nova
validação documental da referência. Acurácia baixa pode refletir dificuldade,
ambiguidade ou erro residual. Mesmo tamanho e metas por subtópico não isolam
causalmente o efeito do contexto: os processos e os tipos das QAs diferem.

Arquivos principais:

- questoes.jsonl: todas as 4.111 QAs; nunca rotuladas como aprovadas.
- resultado.json, RELATORIO.md, config.json, metas.json e geracao_concluida.json.
- topicos/<id>/estado.json: geração retomável por subtópico.
- avaliacao/ACURACIA.md, acuracia.json, acuracia.csv, avaliacoes.jsonl.
- avaliacao/protocolo_experimento.json e avaliacao_concluida.json: fingerprints,
  modelos, prompts, cobertura e status final; respostas/ e juiz/ guardam evidência.

Ao concluir, o terminal imprime a mensagem de término e os comandos de coleta,
commit e push. Após coletar, comparar o baseline de 4.111 QAs com Default + A + E.
