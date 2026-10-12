# Documentos revisados — Produção e Processo

O próximo tópico na ordem do projeto é **Produção e Processo (Medição Fiscal e Sistema de Alívio)**,
com 12 subtópicos. O launcher novo seleciona todos eles e produz somente documentos técnicos.
Use uma saída nova: o piloto KPI anterior permanece preservado.

## O ajuste

Cada unidade utilizável precisa declarar um **alvo de conhecimento profissional**. Cronologia de acidente,
identidade de pessoas, datas de embarque e número de viagens não bastam. O revisor registra
`carater_avaliativo` e `alvo_qa`: somente `conhecimento_profissional` pode ser aprovado ou refinado.
Uma lição de incidente precisa explicitar mecanismo, condição, consequência, critério ou decisão sustentada.
Os fatos históricos continuam nos trechos e pareceres como evidência, sem virar automaticamente perguntas.

O próprio redator/extrator agora também declara `carater_avaliativo` e `alvo_qa`. Antes da revisão,
a validação separa unidades sem alvo e memória do caso. O prompt orienta a omitir cronologia isolada
e a redigir lições técnicas apenas quando a relação estiver sustentada no trecho completo.
O revisor confere essa primeira proposta e registra qualquer alteração do alvo.

O redator também pode corrigir pequenas imprecisões conceituais e adaptar a redação já na extração.
Cada unidade declara `redacao.ajuste`: `nenhum`, `editorial` ou `tecnico`. Guarda a formulação e
as condições anteriores, motivo, base da intervenção, referências e se a citação sustenta o resultado.
O guia técnico local é fornecido ao redator e ao revisor. Conhecimento conceitual do modelo também
pode ser utilizado, com essa base explicitamente identificada. Não há pesquisa automática adicional.

Exemplo: a fonte chama F(t) de “taxa de falha acumulada”; o redator pode propor “probabilidade
acumulada de falha até t”, preservando a citação com o erro, indicando a referência e registrando
`suporte_citacao: false`. O revisor precisa conferir a proposta e declarar `refinar` para confirmá-la,
mesmo que mantenha sua formulação. Ele pode corrigi-la novamente, rejeitá-la ou deixá-la pendente.
Uma adaptação editorial que preserve o significado pode ser aprovada normalmente.

O documento e as fichas exibem separadamente **antes da redação**, **antes da revisão** e a formulação
final. A verificação de que a citação existe no trecho não significa que ela sustenta uma correção.
`resumo_redacao.json` e as linhas `[redação]` do log contam as intervenções propostas antes da revisão.

Fluxo: assuntos → recuperação → extração → **revisor/refinador** → consolidação → documentos.

O revisor usa GPT-5.4 Petrobras, effort medium, em pedidos próprios com acesso aos trechos originais.
Avalia todas as unidades extraídas, inclusive as inicialmente descartadas. Pode recuperar uma unidade
relevante, corrigir conceitos/terminologia, retirar números dispensáveis ausentes e preservar limites.
Uma imprecisão não significa automaticamente que o trecho é irrelevante.

Decisões:

| Decisão | Destino |
|---|---|
| aprovar | conteúdo utilizável, com formulação preservada |
| refinar | conteúdo utilizável, com original e correção registrados |
| fora_escopo | parecer e original preservados para inspeção |
| pendente | conteúdo potencialmente relevante que precisa de informação adicional |

F(t) e h(t), por exemplo, podem ser reconciliados com as definições técnicas fornecidas do NIST.
A citação da fonte continua literal, mesmo se contiver o erro. A correção recebe sua base explícita:
fonte original, referência técnica fornecida ou normalização conceitual do modelo.
Assim, não é apresentada como uma reprodução fiel de uma fonte que afirmava outra coisa.

Valores ausentes não são estimados. Procedimentos específicos e obrigações normativas não podem ser
inventados a partir de conhecimento do modelo. Princípios transferíveis precisam estar explicitados
na fonte; uma tabela de hospital não se transforma em conteúdo de FPSO por mudar o nome da instalação.

Após a revisão, a consolidação preserva o histórico das correções. A fusão recebe o rótulo `consolidada`:
ter dois arquivos não é prova de fontes independentes. O documento por tópico apresenta cada ID de
unidade canônica uma vez e registra todos os assuntos associados. As fichas individuais continuam disponíveis.

Esta etapa é revisão por modelo, não certificação factual externa. O agrupamento ainda pode deixar
equivalências ou conflitos entre grupos sem identificação. O gerador de QA ainda não consome este inventário.

## No servidor Linux

Na raiz do repositório, com o ambiente e as credenciais corporativas já usados no piloto:

```bash
git pull --ff-only origin dev
python3 -m pip install -r pipeline/inventario/requirements_azure.txt
bash pipeline/inventario/run_producao_azure.sh --plan
bash pipeline/inventario/run_producao_azure.sh --check-api
bash pipeline/inventario/run_producao_azure.sh
```

Para executar em segundo plano e manter o processo após fechar a sessão SSH, use esta alternativa
à última linha, depois de o plano e o teste de API concluírem com sucesso:

```bash
export INV_OUTPUT=pipeline/inventario/saida_producao_v3_correcao_azure
mkdir -p "$INV_OUTPUT"
nohup bash pipeline/inventario/run_producao_azure.sh > "$INV_OUTPUT/console.log" 2>&1 &
echo "PID: $!"
```

Para acompanhar, inclusive erros enviados ao terminal:

```bash
tail -F pipeline/inventario/saida_producao_v3_correcao_azure/console.log
```

`Ctrl+C` encerra somente o acompanhamento. O log interno também fica em `execucao.log`.

O plano deve listar **12 subtópicos, todos de Produção e Processo**. A varredura percorre os corpora
uma vez para o conjunto selecionado. O tópico tem um volume maior que KPI; não há previsão de tempo
baseada apenas na primeira rodada. O limite técnico padrão é 30.000 tentativas LLM por invocação,
incluindo extração, revisão e consolidação, sem contar embeddings. Pode ser configurado com `INV_MAX_CHAMADAS`.

Para começar apenas pelo primeiro subtópico, use outra saída:

```bash
INV_OUTPUT=pipeline/inventario/saida_medicao_v3_correcao_azure \
  bash pipeline/inventario/run_producao_azure.sh \
  --subtopicos 'Medição Fiscal de óleo, medição fiscal de gás e transferência de custódia em operações de offloading'
```

Também pode parar em `--parar-apos revisao` para inspecionar os pareceres antes dos documentos finais.
Retome com o mesmo recorte e saída; respostas já bem-sucedidas ficam em cache. Alterar filtros/modelos/parâmetros
de seleção exige saída nova.

## Windows

```powershell
powershell -ExecutionPolicy Bypass -File pipeline/inventario/run_producao_azure.ps1 -Plan
powershell -ExecutionPolicy Bypass -File pipeline/inventario/run_producao_azure.ps1 -CheckApi
powershell -ExecutionPolicy Bypass -File pipeline/inventario/run_producao_azure.ps1
```

## Arquivos para trazer pelo GitHub

Saída padrão: `pipeline/inventario/saida_producao_v3_correcao_azure/`.

- `subtopicos/*/pareceres_revisao.jsonl`: original, decisão, motivo e unidade revisada.
- `unidades_revisadas.jsonl`, `unidades_pendentes.jsonl`, `unidades_rejeitadas_revisao.jsonl` em cada subtópico.
- `subtopicos/*/resumo_revisao.json` e `resumo_revisao.json`: quantidades de cada decisão.
- `subtopicos/*/selecao.json`: trechos originais.
- `subtopicos/*/unidades_brutas.jsonl` e `unidades_descartadas.jsonl`: proposta e histórico do redator.
- `resumo_redacao.json`: ajustes editoriais e técnicos propostos por subtópico.
- `topicos/*/documento_tecnico.md`, fichas, cobertura e `cobertura_resumo.json`.
- `falha_revisao.json`: falhas de execução, separadas das pendências de conteúdo.

```bash
tail -f pipeline/inventario/saida_producao_v3_correcao_azure/execucao.log
```

## Referências usadas no guia de revisão

- [NIST: taxa instantânea de falha](https://www.itl.nist.gov/div898/handbook/apr/section1/apr123.htm).
- [NIST: sobrevivência e distribuição acumulada](https://www.itl.nist.gov/div898/handbook/apr/section1/apr122.htm).
- [NIST: ocorrência de falhas em sistemas reparáveis](https://www.itl.nist.gov/div898/handbook/apr/section1/apr125.htm).
- [HSE: passagem de serviço e conferência das informações](https://www.hse.gov.uk/humanfactors/topics/shift-handover.htm).
- [Documentação oficial: validação de saídas JSON](https://developers.openai.com/api/docs/guides/structured-outputs).

O guia técnico é local e explícito; o pipeline não pesquisa automaticamente fontes novas na internet.
