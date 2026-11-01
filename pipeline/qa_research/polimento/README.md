# Polimento da edição existente dos 40 contextos

O programa usa `relatorios/dez_areas_final_v2` como base, preserva os recortes
curados e as correções registradas do especialista e produz alterações localizadas.
Não gera questões. Os documentos anteriores e os datasets externos de QA não são
modificados. O plano aprovado está em `../PLANO_POLIMENTO_40_CONTEXTOS.md`.

## Fluxo implementado

1. Conferir documento, recortes, evidências herdadas e correções do especialista.
2. Diagnosticar até seis intervenções: correção técnica, lacuna essencial,
   aprofundamento ou edição. Os pontos de cobertura mantêm os IDs curados.
3. Pesquisar cada necessidade nos índices das evidências originais e do corpus
   instalado. Reutilizar BM25, busca PT/EN e RRF. Ler até oito passagens por rodada,
   no máximo duas rodadas; a segunda exige consulta adicional e passagem inédita.
   Intervenção técnica exige consulta PT/EN; apenas edição pode dispensar pesquisa.
   Pesquisa não executada, falta de passagens, leitura malsucedida e falta de
   evidência pertinente são estados distintos. Achados contextuais não autorizam
   inclusão factual: somente relações diretamente pertinentes chegam à edição.
4. Extrair relações, condições, limites e estatuto das afirmações. O modelo cita IDs
   das passagens; o código recupera texto e intervalos, sem exigir cópia literal.
   Cada intervenção técnica tem de um a três subobjetivos verificáveis. Achados
   diretos precisam indicar quais deles sustentam. O Python recalcula a cobertura
   e restringe a segunda leitura aos subobjetivos faltantes, mesmo quando o modelo
   declara suficiência. Subobjetivos sem suporte viram pendências da edição.
5. Editar em lotes de duas intervenções. Somente os alvos autorizados podem ser
   substituídos, removidos ou receber inserções. Capítulo novo exige autorização
   no diagnóstico. Blocos intocados permanecem idênticos.
   Movimentos preservam integralmente os blocos; títulos de capítulos podem ser
   ajustados sem regenerar seus parágrafos.
   Cada lote recebe a edição corrente, incluindo as alterações já aprovadas.
6. Revisar cada operação pelo seu `op_id`, usando o mapa da base anterior ao lote,
   o bloco anterior e o estado proposto. Inserções nunca aparecem como já aplicadas
   nessa base. Aprovações independentes são comitadas antes do único reparo, que
   recebe apenas os `op_id` a corrigir e o documento já atualizado. Fusões dependentes
   são avaliadas como transações acopladas para evitar perda de conhecimento.
   Em edição editorial, suporte significa preservar fatos existentes sem inventar
   novos; não se exige pesquisa nova para afirmações já presentes no bloco original.
7. Fazer uma leitura editorial focada do documento inteiro, com o modelo de revisão:
   comparar capítulos, procurar repetição de ideias, relato de leitura e termos
   estrangeiros sem explicação. Verificações locais sinalizam expressões explícitas
   e parágrafos semelhantes; similaridade é pista, não autorização para apagar.
8. Agrupar os defeitos em micro-intervenções `E01`, `E02` etc., com no máximo três
   blocos por chamada editorial e mantendo juntos os pares com repetição. Cada lote
   tem revisão por operação, aplicação imediata e no máximo um reparo focalizado.
   Operações que continuarem reprovadas são descartadas individualmente. A leitura
   de conferência verifica o documento após os commits de acabamento.
9. Conferir coerência, proteções e cobertura final. O parecer geral não apaga falhas
   da leitura editorial ou das verificações locais. Relato de fonte, duplicação
   literal longa ou problema editorial confirmado impede publicar a edição e
   liberar QA. A versão para revisão permanece disponível.

`resumo.json`, `relatorio.md` (também disponível como `RELATORIO.md`) e a versão
para revisão são atualizados em cada etapa e commit. Interrupções preservam os
apontamentos da leitura editorial e as alterações técnicas e editoriais já
aprovadas. A consolidação recebe a cobertura inicial e a da base anterior; um ponto
atendido não regride sem remoção associada ou evidência explícita de regressão.

A lista de pendências reúne intervenções não aprovadas, cobertura parcial/ausente,
omissões de escopo e problemas de revisão. Aprovar uma inclusão útil não significa
que todos os objetivos da intervenção tenham sido atendidos.

O revisor de alterações confere os fatos novos e modificados. O texto herdado
preservado não é apresentado como se cada uma de suas afirmações tivesse passado
por nova pesquisa. Dados, números operacionais e normas exigem suporte; uma norma
sem edição/vigência conferida não autoriza declarar que a regra é atual.

## Piloto de três documentos

Configuração padrão:

| ID | Documento | Blocos na base | Correções do especialista herdadas |
|---|---|---:|---:|
| 02_02 | Produtos químicos | 57 | 2 |
| 03_03 | Tanques de carga, lastro, gás inerte, ventilação e estabilidade | 25 | 2 |
| 07_01 | Instrumentação, controle e automação | 34 | 0 |

Os documentos são processados sequencialmente; as pesquisas do documento corrente
compartilham duas vagas de API. Os modelos continuam nos deployments existentes:
diagnóstico `gpt-5-4-petrobras:medium`, pesquisa/edição `gpt-5-4-petrobras:medium`,
revisão `gpt-5-4-petrobras:high`. O orçamento padrão é de 60 tentativas por documento,
cumulativo, incluindo as repetições. São limites de proteção, sem meta de gastar
essas chamadas. O transporte reutilizado permite até duas tentativas por chamada,
prazo de 300 segundos e heartbeat a cada 30 segundos.
Sem defeitos editoriais, a leitura focada acrescenta uma chamada. Havendo defeitos,
cada micro-lote acrescenta escrita e revisão, com um único reparo opcional e uma
conferência global após o acabamento. Tudo usa o mesmo orçamento cumulativo e cache.
A segunda tentativa de transporte usa `retry_tokens` após truncamento, ou após
erro de formato/contrato com mais de 35.000 caracteres. O log e a exceção final
conservam o tipo de falha e o limite de tokens de cada tentativa.

Validação offline (inclui os 29 testes anteriores, as regressões da versão 2.1 e
o transporte compartilhado com v3):

```bash
python -m pytest pipeline/qa_research/polimento/tests tests/test_polimento_v21.py pipeline/qa_research/v3/tests -q
```

## Continuar a partir do piloto já aprovado parcialmente

Para preservar as inclusões do lote de 01/11, use-o explicitamente como base.
O diagnóstico procura as necessidades restantes e as verificações editoriais leem
o texto completo. Não é uma retomada do cache da implementação anterior: é uma
nova edição do resultado existente. A base anterior permanece intacta.

```bash
git pull --ff-only origin codex/qa-evidencias-verificadas
export DOCUMENT_PYTHON="$PWD/.venv-documento/bin/python"
nohup bash pipeline/qa_research/rodar_polimento_contextos.sh \
  --base pipeline/qa_research/relatorios/polimento_3_contextos_20261101T194650 \
  --items 02_02 03_03 07_01 \
  --manifest dataset/professional_corpora_v2/manifest.json \
  --output pipeline/qa_research/saida_polimento/piloto_3_documentos_02 \
  > polimento_3_documentos_02.log 2>&1 &
tail -F polimento_3_documentos_02.log
```

Na raiz do repositório, no servidor:

```bash
git pull --ff-only origin codex/qa-evidencias-verificadas
export DOCUMENT_PYTHON="$PWD/.venv-documento/bin/python"
"$DOCUMENT_PYTHON" -m pip install -r pipeline/qa_research/polimento/requirements.txt

bash pipeline/qa_research/rodar_polimento_contextos.sh \
  --items 02_02 03_03 07_01 \
  --manifest dataset/professional_corpora_v2/manifest.json \
  --output pipeline/qa_research/saida_polimento/piloto_3_documentos_01 --plan

nohup bash pipeline/qa_research/rodar_polimento_contextos.sh \
  --items 02_02 03_03 07_01 \
  --manifest dataset/professional_corpora_v2/manifest.json \
  --output pipeline/qa_research/saida_polimento/piloto_3_documentos_01 \
  > polimento_3_documentos_01.log 2>&1 &
tail -F polimento_3_documentos_01.log
```

`--plan` verifica a base e mostra a configuração sem escrever ou chamar modelos.
O `-F` aguarda o arquivo de log aparecer. Não iniciar duas execuções na mesma saída.
Para retomar, repetir o comando. Chamadas compatíveis são reutilizadas; mudar
workers, orçamento ou progresso não invalida resultados. Mudança de base, corpus,
prompts, configuração de conteúdo ou código produz nova versão. Se a origem da
coleção mudar, escolher outra saída.

O corpus profissional já instalado é reutilizado. As evidências antigas são lidas
de `relatorios/dez_areas_v1/<item>/evidencias_citadas.jsonl` e indexadas separadamente
em `.local/` da saída. A aplicação não presume que a seleção herdada seja um acervo
completo. Se esse arquivo não estiver disponível, o relatório registra a ausência;
recortes curados e documento de base são obrigatórios.

O notebook `piloto_polimento_3.ipynb` usa o Python do kernel ou `DOCUMENT_PYTHON` e
chama os mesmos comandos. Não precisa iniciar Jupyter no servidor para usar a CLI.

## Ler e coletar para análise

Começar por `RELATORIO.md` na raiz do lote e pelo relatório de cada item:

- `documento_anterior.md/json`: a base recebida pelo mecanismo.
- `documento_para_revisao.md/json`: a edição consolidada, sempre disponível após
  uma execução com relatório, mesmo quando precisa de revisão.
- `documento.md/json`: edição publicada somente quando há revisão final sem
  problemas críticos ou correções técnicas pendentes. Pode estar parcial em cobertura.
- `versoes/<versao>/comparacao.json`: antes/depois, motivos, evidências citadas,
  alertas de redução e blocos preservados literalmente. `alteracoes` compara a
  base com as edições técnicas; `acabamento` compara essa edição com os reparos
  editoriais subsequentes. As duas fases reconstituem a edição final.
- `diagnostico.json`, `pesquisas.json`, `decisoes.json` e `coerencia_final.json`:
  plano, relações pesquisadas, avaliações e cobertura estável.
- `leitura_editorial.json`, `acabamento_editorial.json`, `acabamento_parecer.json`,
  `acabamento_aprovado.json` e `leitura_editorial_conferencia.json`: defeitos
  localizados, reparos propostos/aprovados e conferência, quando aplicáveis.
- `base.json`: hashes, proteções e observações herdadas. `preparacao_corpus.json`
  na raiz registra coleções, hashes e diagnóstico da instalação.

A presença de `documento.md` não implica QA liberada. Conferir `qa_elegivel` no
resumo. Erro crítico retém a edição em revisão; lacuna essencial mantém QA bloqueada
sem descartar alterações adequadas. Limite opcional não rejeita automaticamente
o conteúdo. Nenhum consumidor de QA é redirecionado para a nova edição pelo script.

Ao terminar, o terminal mostra “O código acabou de rodar no terminal 🙂”, o estado
real e os comandos concretos de coleta, commit e push. Pode coletar manualmente:

```bash
"$DOCUMENT_PYTHON" -m pipeline.qa_research.polimento \
  --output pipeline/qa_research/saida_polimento/piloto_3_documentos_01 \
  --collect pipeline/qa_research/relatorios/polimento_3_contextos_01
git add -- pipeline/qa_research/relatorios/polimento_3_contextos_01
git commit -m "Resultados do piloto de polimento em três contextos"
git push origin codex/qa-evidencias-verificadas
```

A coleta exige destino inexistente e exclui `.local/`, chaves, cache, respostas
brutas e passagens originais dos corpus. Inclui textos gerados, comparação,
pesquisas sem texto original, metadados, estados e hashes de integridade.
Retorno 0 significa todos concluídos; retorno 2 sinaliza parcial/interrompido.
Não ampliar para `--items all` antes de avaliar os três pilotos.

## Testes offline

```bash
python -m unittest discover -s pipeline/qa_research/polimento/tests -v
```

Os testes usam modelos simulados. Verificam preservação, alvos, perdas detectadas
pela revisão, fundamentação, orçamento, retomada, cancelamento e exportação. Não
substituem a leitura técnica comparativa do piloto real.
