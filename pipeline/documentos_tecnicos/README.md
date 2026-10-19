# Pesquisa de documentos e QA de um tópico

Fluxo de pesquisa iterativa nos corpus autorizados: pesquisador/redator → revisão com fontes originais → pesquisa complementar quando necessária → refinamento → revisão final. A escrita é uma seção de livro técnico, com referências, sem extração/classificação obrigatória de cada afirmação.

Conforme a atualização do pedido, o modo `completo` produz documentos e tenta alcançar **10 questões aprovadas automaticamente sobre um tópico**. O padrão é **tanques de carga/lastro**, com dez pautas de documentos. Não há relação obrigatória de uma questão por documento: uma seção pode sustentar competências diferentes; a verificação de novidade compara todas as questões já aprovadas. Documentos pendentes não entram no QA. A quantidade aprovada não é garantida nem preenchida relaxando critérios. Revisão humana continua pendente.

Esta implementação foi preparada **sem executar testes, plano, geração ou chamadas a modelos localmente**, por orientação do usuário. Os comandos abaixo são para o servidor; ainda não há resultados deste fluxo.

A versão **`pesquisa-documentos-2`** incorpora os [prompts completos revisados](../../docs/pesquisa_prompts_2026_10_18/prompts_completos_revisados.md). Cada chamada recebe a tarefa e o contexto de seu papel, com os perfis de corpus apresentados uma vez por coleção. O revisor confere as conclusões importantes contra os trechos originais e distingue impedimentos materiais de preferências de estilo. O histórico completo permanece nos checkpoints. Essa revisão ainda precisa ser avaliada pelas saídas do servidor.

## O que foi simplificado

- Os agentes trabalham com trechos originais e prosa, sem grafo de afirmações, etiquetas por frase ou nove campos do juiz.
- Contratos pequenos: pesquisador devolve ação/orientação/consultas; redator e refinador devolvem título/texto/fontes; revisor e juiz devolvem decisão/parecer/consultas. Os formatos completos estão nos prompts.
- O pesquisador escolhe novas consultas a partir do que encontrou. Pedidos de evidência do revisor ou refinador retornam à pesquisa, dentro do orçamento. O refinador pode devolver um pedido curto de pesquisa em vez de inventar a correção. O redator pode usar seus conhecimentos para esclarecer conceitos e conectar ideias; as conclusões técnicas importantes precisam de fundamento e são examinadas pelo revisor.
- Chamadas com fontes recebem orientações de leitura por corpus (REGIS, Petrolês, ANP, HSE, BSEE), uma vez por coleção presente. O gênero e o conteúdo prevalecem sobre o nome da coleção. Fontes continuam podendo estar erradas.
- As pautas vêm de `assuntos.json`, com recorte escolhido pelo pesquisador. Não importamos as antigas notas/objetivos ou suas aprovações como verdade. As dez primeiras pautas não genéricas são usadas no piloto; amplie a quantidade para maior cobertura.
- A organização do capítulo é livre. Opinião isolada, detalhes incidentais de instalação e generalidade vazia não devem sustentar suas conclusões. Conhecimento condicional, fundamentos e exemplos didáticos são permitidos.
- A recuperação BM25, o índice com contexto vizinho, o cliente Azure e o banco curado de exemplos são reaproveitados. Não foi adicionado framework de agentes, OCR, GPU ou busca web automática.
- Os corpus completos precisam estar instalados no manifesto. Sem ele, a cobertura declarada é somente a dos índices/seleções disponíveis. Esse fallback não equivale a auditoria do acervo completo.

## Como as questões são avaliadas

Cada candidata usa um capítulo automaticamente aprovado e os trechos originais. O gerador vê exemplos próprios/externos limpos e a cobertura anterior. O juiz recebe uma resolução produzida antes de ver o gabarito do autor, revisa a sustentação e a adequação pedagógica e pode pedir refino ou uma busca complementar. Revisões voltam ao julgamento. O respondente cego recebe exclusivamente a pergunta; a adjudicação confronta as respostas com as fontes, sem exigir coincidência literal. O verificador de novidade examina todas as aprovadas anteriores. Concordância entre modelos não substitui evidência ou revisão humana.

Para esta execução não usamos os juízos v11 que falharam no contrato de nove dimensões. O v11 histórico permanece separado. A única extensão no cliente compartilhado é a gravação opcional das saídas dos modelos, inclusive inválidas, ativada somente neste fluxo.

## Modelos e limites padrão

| Papel | Deployment e esforço |
| --- | --- |
| Pesquisador/redator | `gpt-5-4-petrobras:low` |
| Revisor/juiz/adjudicador | `gpt-5-4-petrobras:low` |
| Refinador | `gpt-5-4-petrobras:low` |
| Respondente cego | `gpt-5-2-petrobras:low` |
| Novidade | `gpt-5-4-nano-petrobras:low` |

Uma execução sequencial evita problemas de coordenação e torna o consumo mais previsível. Limites: 400 tentativas de API no total, 24 por documento, 20 por candidata, 40 candidatas, até quatro rodadas de busca por documento, até três consultas por rodada e 32 trechos preservados por unidade. Contexto vizinho conta no limite de trechos. Um refinamento por documento e um por candidata, com nova revisão em ambos. O primeiro rascunho não conta como refinamento.

Cada chamada pode ter até duas tentativas. Se as duas falham, a execução inteira é interrompida com diagnóstico, preservando checkpoints; não percorre todas as pautas repetindo o mesmo erro de contrato. Filtro de conteúdo e limite por unidade ficam registrados, sem virar aprovação. Limites globais e por unidade são cumulativos após retomada. Cache válido não consome outra tentativa. O teto não é uma estimativa de consumo nem garantia de conclusão; tokens reais são registrados por etapa.

## Executar no servidor

Use o ambiente Azure já configurado no projeto. Atualize apenas depois de encerrar processos antigos que usam o mesmo checkout/índice.

```bash
cd /home/gbs2/MCQ_CONTEXT_GEN
git fetch origin
git switch codex/qa-evidencias-verificadas
git pull --ff-only origin codex/qa-evidencias-verificadas

# Um tópico, dez pautas de documentos e meta de dez questões aprovadas.
# A pasta nova separa esta versão dos experimentos anteriores.
export DOCS_TOPICO="Operação de tanques de carga e lastro"
export DOCS_QUANTIDADE=10
export DOCS_QUESTOES=10
export DOCS_SAIDA="pipeline/documentos_tecnicos/saida_tanques_10_prompts_v2"

# Só mostra as pautas e os limites; sem API, indexação ou download.
# Opcional; não inicia a geração.
bash pipeline/documentos_tecnicos/run_azure.sh plan

# Dez pautas de documentos de tanques e meta de dez questões aprovadas.
nohup bash pipeline/documentos_tecnicos/run_azure.sh completo \
  > pipeline/documentos_tecnicos/console_tanques_10_prompts_v2.log 2>&1 &

echo "PID: $!"
tail -F pipeline/documentos_tecnicos/console_tanques_10_prompts_v2.log
```

O script prefere `venv/bin/python`; configure `DOCS_PYTHON` se seu ambiente tiver outro caminho. Use as dependências e a configuração Azure que já funcionavam no servidor; não foram adicionadas dependências. Os exemplos externos são baixados e filtrados somente se o arquivo v11 ainda não existir, no modo completo. Não há download no modo `plan` ou `documentos`.

Para somente documentos, use **outra saída**:

```bash
DOCS_SAIDA=pipeline/documentos_tecnicos/saida_so_documentos \
  bash pipeline/documentos_tecnicos/run_azure.sh documentos
```

O modo faz parte da assinatura; não troque `documentos` por `completo` na mesma saída. Para ter capítulos e questões numa execução use `completo` desde o início.

Para outro tópico ou outro deployment, use outra saída:

```bash
DOCS_TOPICO="Operação de Separadores Trifásicos" \
DOCS_SAIDA=pipeline/documentos_tecnicos/saida_separadores_10 \
  bash pipeline/documentos_tecnicos/run_azure.sh completo
```

## Retomar e ajustar limites

Repita o mesmo comando. Documentos aprovados e questões concluídas são reutilizados; checkpoints interrompidos retomam a etapa salva. Código, prompts, modelos, entradas, exemplos, tamanho da busca ou modo diferentes exigem outra saída. A assinatura inclui as dependências compartilhadas utilizadas, e a cobertura do corpus é conferida pelo índice.

Metas e limites podem aumentar sem trocar a saída, e a configuração de cada retomada é registrada. Para reabrir documentos que encerraram com pendência substantiva, use `DOCS_REVISITAR_PENDENTES=1` junto aos limites ampliados. Aprovações não são alteradas automaticamente, nem rejeições técnicas de questões são convertidas em aprovações. Uma indisponibilidade não é contada como rejeição técnica.

```bash
DOCS_MAX_CHAMADAS=550 \
DOCS_MAX_CHAMADAS_DOCUMENTO=32 \
DOCS_MAX_PESQUISAS=5 \
DOCS_MAX_FONTES=40 \
DOCS_REVISITAR_PENDENTES=1 \
  bash pipeline/documentos_tecnicos/run_azure.sh completo
```

Se aumentar também `DOCS_QUANTIDADE`, novas pautas são acrescentadas na ordem do inventário. Cada checkpoint preserva sua pauta e fontes. A cota de questões é do tópico inteiro, independentemente da quantidade de capítulos. `DOCS_MAX_CANDIDATAS` permite examinar outras competências quando algumas candidatas forem rejeitadas; nunca é uma ordem para completar a cota a qualquer custo.

Código de saída `0`: ambas as metas atingidas sem interrupção; `2`: saída incompleta/erro, conferir resumo; `130`: interrupção pelo usuário. Não interprete `0` como validação de especialista.

## Arquivos de resultado

Em `pipeline/documentos_tecnicos/saida_tanques_10_prompts_v2/`:

- `documentos.md` e `leitura/*.md`: índice e capítulos para ler, com estado, referências e pendências.
- `documentos/*.json`: fontes originais, consultas, orientações do pesquisador, rascunhos, revisões e estado.
- `documentos_aprovados.jsonl`: apenas capítulos aprovados automaticamente.
- `questoes.md` e `questoes_aprovadas.jsonl`: questões automaticamente aprovadas com resposta, explicação e rubrica.
- `questoes/*.json` e `questoes_todas.jsonl`: inclusive rejeições, falhas e pendências; histórico de refino, julgamento, resposta cega, adjudicação e novidade.
- `resumo.json`: contagens, cobertura, deployments e tokens/tentativas por etapa.
- `revisao_humana.csv`: aprovadas e demais candidatas com texto, sem rótulos humanos preenchidos automaticamente. Não é uma revisão cega.
- `respostas_modelos/*.json`: saídas brutas dos modelos, incluindo saídas inválidas, sem headers/chaves de API.
- `chamadas_llm.jsonl`, `uso_cache.json`, `run_config.json`, `pautas.json`: diagnóstico, consumo, versões e parâmetros.

As referências externas são exemplos de formato, nunca fontes factuais das questões. As partições de demonstração, calibração e material reservado são preservadas em `referencias_avaliacao/`.

## Devolver os resultados

Quando terminar, inclusive se a saída estiver incompleta:

```bash
git add pipeline/documentos_tecnicos/saida_tanques_10_prompts_v2
git commit -m "results: pesquisa de documentos e QA de tanques"
git push origin codex/qa-evidencias-verificadas
```

O índice e os caches permanecem fora do Git; as evidências, versões e logs retornam para diagnóstico. Use a pasta correspondente se modificar `DOCS_SAIDA`.
