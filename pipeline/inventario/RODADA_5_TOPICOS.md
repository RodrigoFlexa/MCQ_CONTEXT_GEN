# Primeiros cinco tópicos — inventário v4

O inventário de **Sistemas de Lastro, Estabilidade, Ancoragem e Posicionamento, Offloading e Tanques
de Carga** já conta como o primeiro tópico. Seus arquivos permanecem na saída
`saida_sistemas_de_lastro_v4_notas` e podem alimentar a geração de QA, com curadoria dos casos
específicos e dos limites numéricos.

Os próximos quatro tópicos escolhidos são:

| Tópico | Subtópicos |
|---|---:|
| Produção e Processo (Medição Fiscal e Sistema de Alívio) | 12 |
| Operações submarinas, poços, risers e equipamentos submarinos | 2 |
| Utilidades, geração de energia e sistemas auxiliares | 2 |
| Segurança Operacional, SGSO, Sistemas de Segurança e Gestão de Riscos | 7 |
| **Total novo** | **23** |

O script `run_mais_4_topicos_azure.sh` seleciona somente esses quatro. A varredura lexical percorre
os corpora uma vez para o conjunto; não são quatro processos simultâneos. O padrão usa oito pedidos
LLM simultâneos, o perfil `petrobras-nano-low` e somente `embedding-3-large-global`.

## Modelos por etapa

| Etapa | Deployment Azure | Effort |
|---|---|---|
| Organizar assuntos e consultas (inclusive tentativa de reorganização) | `gpt-5-4-nano-petrobras` | low |
| Extrair fatos e citações | `gpt-5-4-nano-petrobras` | low |
| Agrupar fatos em conceitos | `gpt-5-4-petrobras` | low |
| Redigir notas técnicas | `gpt-5-4-petrobras` | low |
| Revisar notas | `gpt-5-4-petrobras` | low |
| Planejar combinações para questões difíceis | `gpt-5-4-petrobras` | low |

O roteamento vale também para reparos de JSON, respostas truncadas e retentativas: cada pedido
continua no modelo da sua etapa. Não há fallback para outro deployment. Um nome de etapa não
configurado causa erro antes da chamada. Os oito workers e o limite de chamadas são compartilhados
entre os dois modelos; retentativas também consomem o limite, respostas do cache não.

`run_config.json` registra o perfil efetivo. `chamadas_llm.jsonl` identifica etapa, modelo e effort
em cada tentativa; `resumo.json` traz o uso agregado, o uso por etapa e as tentativas consumidas.
Esses contadores representam a invocação atual; o log de chamadas é acumulado nas retomadas.
O cache diferencia deployment e effort. Alterar o perfil exige outra saída para não misturar notas
e fatos já gravados com um experimento diferente.

Para usar esse perfil diretamente com `run_inventario.py`, acrescente
`--perfil-modelos petrobras-nano-low` (effort low é automático), sem `--llm-model`.
Os comandos antigos continuam no perfil `unico`: `--llm-model` e `--effort` valem para todas as etapas,
com medium como padrão. O perfil misto exige Azure e recusa modelos ou efforts conflitantes.

## Conteúdo e ajustes

O fluxo continua: assuntos → trechos → fatos → conceitos → redator/revisor → combinações → documentos.
Os prompts do redator e do revisor agora cobram autonomia dos alvos: um caso pode ilustrar um mecanismo,
mas a pergunta futura não pode depender de memorizar uma investigação, um tanque identificado só na fonte
ou uma data. O prompt do experimento de QA também exige sintomas e condições suficientes para a resposta.
Não se generaliza arbitrariamente uma conclusão específica da fonte.
O mapa de fatos do redator foi isolado por subtópico: IDs de fatos extraídos do mesmo trecho
em contextos diferentes deixam de sobrescrever a evidência de outro plano de conceito.

Esses ajustes valem para as próximas chamadas. As 311 notas e as 24 questões do piloto de Lastro
continuam preservadas, produzidas pelos prompts anteriores. O teste de dificuldade mede dificuldade;
ele não é uma avaliação de corretude e autonomia da QA.

## No servidor

Na raiz do repositório, com o ambiente e as credenciais corporativas:

```bash
git pull --ff-only origin dev
python3 -m pip install -r pipeline/inventario/requirements_azure.txt
export INV_OUTPUT=pipeline/inventario/saida_mais_4_topicos_v4_nano_low

bash pipeline/inventario/run_mais_4_topicos_azure.sh --plan
bash pipeline/inventario/run_mais_4_topicos_azure.sh --check-api
```

O plano deve listar **23 subtópicos de quatro tópicos**, sem Lastro nem KPI, e mostrar os modelos
por etapa. `--check-api` faz um pedido JSON real e novo em **cada um dos dois deployments**, ambos
com effort low, e uma chamada de embeddings Azure para dois textos (3.072 dimensões). Não usa
respostas em cache nesse teste. Credenciais, API version, gateway e certificado vêm da configuração
Azure já utilizada no servidor; não é necessário cadastrar uma chave por modelo. Quando ambas as
verificações concluírem com sucesso:

```bash
mkdir -p "$INV_OUTPUT"
nohup bash pipeline/inventario/run_mais_4_topicos_azure.sh > "$INV_OUTPUT/console.log" 2>&1 &
echo "PID: $!"
tail -F "$INV_OUTPUT/console.log"
```

`Ctrl+C` encerra apenas o acompanhamento. O processo continua ao fechar a sessão SSH.
Para ver o modelo de cada pedido, em outra sessão:

```bash
tail -F "$INV_OUTPUT/chamadas_llm.jsonl"
```

Retome com o mesmo comando e saída caso haja interrupção; para preservar o log, use `>>` na retomada.
Não inicie uma segunda execução nessa mesma saída enquanto a primeira estiver ativa.

`INV_REUSE` aponta por padrão para o inventário de Lastro. Se os caches do servidor estiverem presentes,
o script reaproveita vetores de trechos já vistos. O índice lexical será recalculado porque os assuntos
são diferentes. Nenhuma resposta LLM ou nota de Lastro é copiada para os quatro tópicos novos.

Pode ajustar `INV_WORKERS` e `INV_MAX_CHAMADAS` (padrões: 8 e 30.000 tentativas por invocação).
O filtro de conteúdo pula o item e registra a ocorrência; orçamento, credenciais inválidas e falhas
sistêmicas interrompem a execução com diagnóstico. `concluido_com_ocorrencias` precisa ser lido
junto com cobertura e ocorrências; notas aprovadas não comprovam cobertura exaustiva.
Nas saídas novas, `processamento_completo` na cobertura e no índice de geração distingue
material utilizável de processamento sem itens pulados; um assunto pode ter notas boas e ainda ser parcial.

## Resultados e retorno pelo GitHub

Na saída nova:

- `notas_aprovadas.jsonl`: notas dos quatro tópicos, com origem e revisão.
- `topicos/*/documento_tecnico.md`: um documento por tópico.
- `subtopicos/*/documento.md`: os documentos dos subtópicos.
- `combinacoes.jsonl`, `cobertura.csv`, `resumo.json`, `ocorrencias.jsonl` e `console.log`.

Depois da execução no servidor:

```bash
git add pipeline/inventario/saida_mais_4_topicos_v4_nano_low/
git commit -m "results: inventarios v4 de quatro novos topicos"
git push origin dev
```

Aqui no computador:

```powershell
git pull --ff-only origin dev
```

Essa rodada produz documentos. Não dispara a geração completa de QA.
