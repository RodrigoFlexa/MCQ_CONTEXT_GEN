# Lote de nove perguntas e respostas

A etapa gera um lote por execução. Não inicia pesquisa documental,
indexação, embeddings ou leitura do corpus bruto. A entrada é **um documento de
conhecimento técnico já produzido**, associado a uma frase do especialista.
Cada execução trata um único item do programa, por padrão `02_02`: Produtos
químicos, em Produção e Processo (Medição Fiscal e Sistema de Alívio).

## Etapas e modelos

| Etapa | Deployment Azure | Reasoning effort |
|---|---|---|
| Planejamento | `gpt-5-4-petrobras` | `high` |
| Geração | `gpt-5-4-petrobras` | `high` |
| Verificação | `gpt-5-4-petrobras` | `low` |
| Refinamento | `gpt-5-4-petrobras` | `low` |

A configuração fica em `configs/qa_lote_9.json`. O effort é enviado no parâmetro
`reasoning_effort` da API, pelo cliente Azure já usado no projeto. Não há troca
automática de deployment ou redução de effort em caso de falha.

1. **Planejamento:** recebe área, tema, escopo orientador e o documento integral.
   Seleciona nove alvos distintos, resposta esperada, condições, exigência
   cognitiva e fundamentos literais. O início da frase do especialista passa de
   “As questões devem abordar” para “As questões podem abordar”.
2. **Geração:** recebe o plano e o mesmo documento integral. Formula as perguntas
   e respostas, preservando alvos, IDs e dificuldades.
3. **Verificação:** primeiro resolve as nove perguntas sem receber o gabarito do
   autor, o plano ou suas respostas esperadas. Depois, outra chamada compara
   perguntas, respostas, plano, resolução e contexto. Avalia sustentação,
   correção, determinação da resposta, autonomia, pistas, dificuldade, contexto
   brasileiro, foco, aderência ao plano e diversidade do lote. Registra uma
   possível resposta concorrente e a condição literal da pergunta que a exclui,
   além da dificuldade observada sem presumir o nível solicitado.
4. **Refinamento, se necessário:** corrige somente os IDs reprovados, preservando
   os alvos e os demais itens. O lote inteiro passa novamente pelas duas chamadas
   de verificação. O padrão permite um refinamento. Se o problema exigir mudar
   o alvo ou o nível, encerra com insuficiência para replanejamento, em vez de
   retirar condições necessárias para tentar aprovar o item.

São quatro chamadas quando o lote passa de primeira; sete com um refinamento,
sem contar retentativas de API/JSON inválido. Insuficiência de fundamento encerra
a etapa sem inventar conteúdo nem completar o lote com itens inadequados.

## Critérios do lote

- **Fácil, IDs 1–3:** recordar fato ou conceito isolado, sem cenário.
- **Média, IDs 4–6:** uma condição permite inferência de um passo.
- **Difícil, IDs 7–9:** dois ou mais passos necessários dentro do mesmo conceito
  ou mecanismo; sinais discriminantes sem nomear a causa esperada.
- Respostas objetivas de no máximo 50 palavras, com uma demanda por pergunta.
- Português brasileiro e contexto técnico aplicável à indústria brasileira.
  Regras estrangeiras não são automaticamente transferidas para o Brasil.
- Sem múltipla escolha, datasets externos ou questões de exemplo nos prompts.

Os prompts aprovados estão em `prompt_planejamento_qa_9.md` e
`prompt_geracao_qa_9.md`. Na API, o corpo de instruções vai na mensagem de sistema
e as entradas vão como dados JSON em uma mensagem separada. Verificação e
refinamento estão em `qa_batch/prompts.py`.

As regras distinguem a relação técnica, fundamentada no contexto, das condições
de uma situação hipotética, que precisam aparecer na pergunta. O resolvedor e o
revisor não podem preencher condições ausentes usando o documento ou o plano.
Gabaritos respondem apenas à demanda, sem recomendações operacionais adicionais.

Na versão `qa-batch-v2`, uma resposta concorrente sem condição que a exclua, ou
uma dificuldade observada diferente da solicitada, bloqueia a publicação mesmo
se os booleanos da auditoria vierem todos positivos. A condição discriminante,
quando declarada, precisa ser uma passagem da própria pergunta. Essa conferência
não substitui a avaliação semântica de que a condição realmente exclui a alternativa.

A auditoria agora seleciona IDs de passagens e de partes do enunciado. O código
recupera os textos originais e mantém a validação literal nos arquivos auxiliares.
Assim, a API não precisa recitar passagens longas. IDs inexistentes ou pertencentes
a outra pergunta são rejeitados. Planejamento e geração mantêm os mesmos prompts.

## Retomar os 40 subtópicos

Na raiz do projeto, no servidor:

```bash
git pull --ff-only
bash pipeline/qa_research/rodar_qa_todos.sh
```

O comando confere os 40 documentos, preserva resultados finalizados e retoma
interrupções na saída existente `saida_qa_lote_9_final_v2/`. Mostra contadores de
aprovados, pendentes, falhas, preservados e ETA aproximada, calculada com as
latências registradas. Não refaz pesquisa documental, índices ou embeddings.

Falhas de validação, filtro de conteúdo, orçamento por item ou indisponibilidade
após as retentativas são registradas e a fila continua. Credenciais inválidas,
configuração incompatível ou corrupção de checkpoint interrompem para correção.
Pendências de qualidade continuam pendências; o lote não é aprovado para completar
a quantidade. O limite cumulativo de 40 tentativas de API por item é preservado.

Opcionalmente, para percorrer somente o trecho a partir de `03_02`:

```bash
bash pipeline/qa_research/rodar_qa_todos.sh --from-item 03_02
```

O reparo reconhece a implementação v2 que produziu os resultados existentes.
Tópico, contexto, modelos e tokens precisam continuar idênticos. Lotes finalizados
são preservados sem novas chamadas. Nas interrupções, a migração é registrada em
`migracoes/`; checkpoints com chave idêntica são revalidados e reutilizados.
Alterações desconhecidas de implementação continuam exigindo saída nova.

Para verificar as entradas sem chamadas de API:

```bash
python -m pipeline.qa_research.qa_all check
```

O andamento consolidado fica em `saida_qa_lote_9_final_v2/resumo_todos.json`.
O código de saída global é 0 para todos aprovados, 2 quando a fila termina com
pendências/falhas isoladas, 1 para interrupção por erro global e 130 por Ctrl+C.

Ao terminar, o terminal imprime a mensagem com 🙂 e um comando `qa_all collect`
para coletar **todos os lotes existentes**, inclusive os anteriores à interrupção.
O snapshot contém um índice, manifestos, resultados e auditorias, sem `.env`,
SQLite ou caches locais. Depois, execute os comandos `git add`, `git commit` e
`git push` mostrados. Na máquina local, use `git pull --ff-only`.

## Conferir sem chamar modelos

Na raiz do projeto, em Windows ou Linux, com o ambiente Python habitual:

```text
python -m pipeline.qa_research.qa_batch plan --item 02_02
python -m pipeline.qa_research.qa_batch check --item 02_02
```

`plan` mostra a configuração mesmo quando o documento futuro ainda não existe.
`check` valida o documento e seu manifesto, quando disponível, sem chamada de
API. Nenhum dos dois carrega modelos de embeddings ou precisa de credenciais.

A entrada padrão é
`pipeline/qa_research/relatorios/dez_areas_final_v1/02_02/documento.json`, da
versão editorial final dos 40 documentos. Os resultados originais da pesquisa
permanecem em `relatorios/dez_areas_v1/`. O registro da revisão e as referências
auxiliares ficam fora dos contextos, em `relatorios/dez_areas_final_v1/REVISAO.md`.
Para outro snapshot, use `--document CAMINHO`.
O arquivo precisa manter a estrutura limpa de `documento.json`, sem campos de
proveniência ou questões. O título é conferido contra o perfil do item.

Um documento com cobertura parcial pode ser aproveitado se sua consolidação
estiver finalizada e não houver interrupção nem etapa pendente. Somente seus
blocos de conhecimento publicados chegam aos prompts. As pendências ficam nos
metadados auxiliares; o planejamento decide se há suporte para nove alvos.

## Repetir o teste no servidor

Com o projeto atualizado e as mesmas credenciais Azure da geração documental,
o comando usa diretamente a versão final revisada de Produtos químicos:

```bash
git pull --ff-only
bash pipeline/qa_research/rodar_qa_lote_9.sh --item 02_02 \
  --output pipeline/qa_research/saida_qa_lote_9_final_v2/02_02
```

O script usa `.venv-documento/bin/python`, depois `venv/bin/python`, ou `python3`.
`DOCUMENT_PYTHON` permite escolher outro interpretador. Para usar a saída
documental finalizada diretamente, antes da coleta:

```bash
bash pipeline/qa_research/rodar_qa_lote_9.sh --item 02_02 \
  --document pipeline/qa_research/saida_documento_dez_areas_v1/02_02/documento.json
```

A saída padrão é `pipeline/qa_research/saida_qa_lote_9_final_v2/02_02/`. São gravados
checkpoints por chamada, orçamento cumulativo e os arquivos auxiliares de cada
etapa. Interrupções retomam pelo mesmo comando; o limite de 40 tentativas não
reinicia. Mudanças no contexto, prompts, código, modelos ou effort exigem uma
nova pasta `--output`, para preservar a identidade dos resultados anteriores,
exceto a migração compatível explicitamente descrita acima.

Este teste usa o mesmo tópico e o mesmo documento técnico do primeiro piloto,
com novo planejamento e geração de nove itens (3/3/3). O lote anterior permanece
em `relatorios/qa_lote_9_02_02_20261020T155946028788Z/`, e sua revisão manual está
em `relatorios/analise_qa_02_02_20261020/REVISAO.md`. A nova execução não usa essas
questões como exemplos e não refaz o pré-processamento. A comparação de qualidade
será feita após a geração; os testes de código não demonstram melhora das questões.

`qa.json`, `qa.csv` e `qa.md` só são publicados com nove itens aprovados pela
verificação automática. Referências, fundamentos, auditorias e plano ficam fora
desses arquivos. `resumo.json` informa `aprovado_modelo`, insuficiência,
`pendente_revisao` ou interrupção. Aprovação automática não substitui revisão
humana nem validação empírica da dificuldade. O código de saída é 0 para lote
aprovado, 2 para insuficiência/reprovação e 1 para falha de execução.

Ao terminar, o terminal mostra “O código acabou de rodar no terminal 🙂”, seguido
dos comandos concretos de coleta, `git add`, `git commit` e `git push`. A coleta
cria um snapshot novo em `relatorios/qa_lote_9_...`, com hashes; inclui somente
resultados e auditorias, sem credenciais, índices, SQLite ou caches.

Depois do push no servidor, na máquina local:

```bash
git pull
```

Abra `qa.md` no snapshot indicado pelo terminal. Se o lote tiver sido reprovado,
consulte `resumo.json`, `candidatas.json` e `revisoes/`; não haverá um lote
publicado como se tivesse sido aprovado.

## Base dos ajustes de prompt

As instruções separam objetivo, critérios de aceitação e formato de saída,
conforme a [orientação oficial para modelos de raciocínio](https://developers.openai.com/api/docs/guides/reasoning-best-practices).
Os critérios de unicidade, autonomia e dificuldade são decisões do projeto,
ajustadas pela revisão manual do piloto; não são garantias de qualidade do modelo.
