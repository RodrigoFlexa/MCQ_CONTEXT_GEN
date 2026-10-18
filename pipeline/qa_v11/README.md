# QA v11 — piloto e experimentos no servidor

Branch: `codex/qa-evidencias-verificadas`.

Implementação da revisão de arquitetura em [estudo](../../docs/pesquisa_arquitetura_qa_2026_10_18/estudo.md)
e [contratos propostos](../../docs/pesquisa_arquitetura_qa_2026_10_18/prompts_propostos.md).
Código novo isolado do v10, que permanece disponível como referência histórica.
**Conforme solicitado, esta alteração foi preparada sem executar testes, plano ou geração local.**
Os comandos abaixo serão executados pelo usuário no servidor; ainda não há resultado real do v11.

## O que muda

- Reextrai afirmações dos trechos originais; não importa os fatos antigos como verdade.
- Conserva texto, hash, localização disponível e problemas de extração. Fronteiras desconhecidas e números mascarados não são reconstruídos.
- Verifica estatuto da afirmação, fidelidade, adequação técnica, condições e aplicabilidade antes da nota.
- Usa **SQLite FTS5/BM25** no acervo autorizado disponível, com verificação semântica pelo LLM. Não depende de GPU nem usa embeddings de teste.
- Com manifesto instalado, indexa também as janelas do corpus completo configurado. Sem ele, declara que a cobertura se limita a todos os índices/seleções salvos, não apenas aos candidatos do conceito.
- Recupera contexto vizinho como evidência separada, quando a fronteira documental é confiável. Não inventa seções, figuras, paginação ou independência entre publicações repetidas.
- Complementa lacunas verificando se o retorno resolve o problema. Pode promover propostas paramétricas da nota somente após sustentação verificável.
- Revisa blocos e objetivos individualmente, mantendo quarentena e preservando outros conteúdos válidos. Não bloqueia todo princípio por aparecer em incidente/tese.
- Seleciona exemplos próprios e externos por habilidade e pertinência. Conserva suporte anotado do HotpotQA para demonstrar raciocínio.
- Separa demonstrações, calibração e material reservado. Rótulos extraídos dos pareceres continuam identificados como triagem a conferir, não como verdade nova produzida pelo pipeline.
- Produz uma resolução com evidências **sem ver a resposta do autor**, antes do julgamento. Juiz técnico/pedagógico, respondente cego, adjudicador e verificador de novidade têm funções separadas.
- O refinador pode corrigir pergunta, resposta e rubrica; cada versão volta ao juiz e, se aprovada, ao teste cego.
- Falhas de API, apresentação, evidência e reprovação técnica têm estados distintos. Erros de juiz/cego/novidade nunca aprovam o item.
- A novidade compara competência, condições e rubrica com todos os itens já aprovados do mesmo subtópico, sem depender de um corte de similaridade.

Não há OCR novo nem coleta web arbitrária no loop. Se o texto extraído não sustenta uma proposição que depende de tabela/figura/valor ausente, o sistema deve manter a lacuna. A verificação automatizada não substitui validação técnica humana.

## Três configurações

| Configuração | Entrada do gerador | Complemento |
|---|---|---|
| `direta` | Afirmações verificadas, evidências, objetivo e exemplos | Não |
| `nota` | Mesma preparação mais a nota pedagógica revisada | Não |
| `nota_complemento` | Nota revisada e evidências, incluindo complementos aprovados | Sim, com limite |

Para controlar os objetivos, **todas preparam a nota e seus objetivos**. Em `direta`, a prosa da nota é omitida do gerador/juiz. Assim, `direta` versus `nota` mede o efeito da exibição da nota, não a remoção de todo o custo do redator. As chamadas idênticas de preparação podem ser reutilizadas pelo cache compartilhado. `nota_complemento` também muda a evidência disponível: não interpretar sua comparação como efeito isolado da redação.

O consumo observado depende da ordem e do aquecimento do cache. Não usá-lo como comparação de custo sem cache. `uso_cache.json` informa reutilização e etapas da última execução; `chamadas_llm.jsonl` e o resumo registram tentativas e tokens pagos acumulados naquela saída.

Modelos padrão mantidos: redator/gerador/refinador e juiz/adjudicador `gpt-5-4-petrobras:low`; respondente cego `gpt-5-2-petrobras:low`; novidade `gpt-5-4-nano-petrobras:low`. O recuperador desta experiência é BM25 com revisão semântica LLM, sem chamada de embeddings.

## Meta e limites

Subtópicos do piloto:

1. Operação de Separadores Trifásicos.
2. SGSO.
3. Operação de Tanques de Carga/Lastro, identificado pelo prefixo do nome do inventário.

Padrão: **10 aprovadas automaticamente por subtópico = meta de 30 por configuração**.
A bateria tem, portanto, meta de **90 aprovações automáticas**. Não são 90 questões necessariamente distintas entre experimentos; é desejável haver objetivos comparáveis.

Não há garantia de atingir a cota: usa até 20 unidades e 50 candidatas por subtópico, com teto global cumulativo de 900 tentativas de API **por configuração**. Tentativas de reparo também contam. Até duas revisões por questão; complemento de lacunas, propostas e uma recuperação motivada pelo juiz são limitados no código. Nenhum desses limites implica relaxar os critérios para fechar a cota. Código de saída 2 indica meta incompleta/orçamento; os resultados parciais permanecem disponíveis.

Na bateria, o teto máximo configurado é 2.700 tentativas de API; isso não é previsão de consumo. Há reutilização do cache, e a execução pode encerrar antes. Tokens e tentativas reais são informados por etapa. Para reduzir o teto, configure `QA_V11_MAX_CHAMADAS` antes de executar.

`QA_V11_MODO=fixo` muda o objetivo para **10 candidatas por subtópico**, independentemente de aprovação, útil para reduzir o efeito de cada método consumir objetivos diferentes. Pendências operacionais continuam pendentes. A comparação lista os objetivos presentes em todos os experimentos. Não promete pareamento perfeito com a variante que complementa evidências.

## Atualizar e executar no servidor

Na raiz do checkout, usando o ambiente que já tem o acesso Azure e `.env` configurados:

```bash
git fetch origin
git switch --track origin/codex/qa-evidencias-verificadas
git pull --ff-only origin codex/qa-evidencias-verificadas

python -m pip install -r pipeline/inventario/requirements_azure.txt

# Inspeciona fontes, configurações e metas sem APIs.
bash pipeline/qa_v11/run_qa_v11_azure.sh plan

# Roda todas as três configurações sequencialmente.
# O download dos exemplos externos ocorre automaticamente se o arquivo v11 não existir.
nohup bash pipeline/qa_v11/run_qa_v11_azure.sh experimentos \
  > pipeline/qa_v11/console_experimentos.log 2>&1 &

echo "PID: $!"
tail -F pipeline/qa_v11/console_experimentos.log
```

Se a branch já existir localmente, use `git switch codex/qa-evidencias-verificadas` no lugar de `git switch --track ...`.

O arquivo geral informa início/fim de cada configuração. O progresso detalhado estará em:

```bash
tail -F pipeline/qa_v11/saida_30/console_direta.log
tail -F pipeline/qa_v11/saida_30/console_nota.log
tail -F pipeline/qa_v11/saida_30/console_nota_complemento.log
```

Para rodar só o método completo, meta total de 30:

```bash
nohup bash pipeline/qa_v11/run_qa_v11_azure.sh piloto \
  > pipeline/qa_v11/console_piloto.log 2>&1 &
```

Para uma bateria com quantidade fixa de candidatos:

```bash
QA_V11_MODO=fixo QA_V11_SAIDA=pipeline/qa_v11/saida_fixa \
  nohup bash pipeline/qa_v11/run_qa_v11_azure.sh experimentos \
  > pipeline/qa_v11/console_fixa.log 2>&1 &
```

Não altere o modo dentro da mesma saída. A assinatura bloqueia mistura de código, exemplos, fontes ou modelos diferentes. Use outra pasta para outra condição.

## Retomada

Repita o mesmo comando e parâmetros. Os pacotes de evidências/notas e estados por tópico são persistidos; respostas de API idênticas são reutilizadas pelo cache. Perguntas aprovadas não são recontadas como novas. Pendências operacionais podem ser reprocessadas. O teto de API é cumulativo, mesmo após reiniciar; para aumentá-lo, use `QA_V11_MAX_CHAMADAS=1200`.

É possível ampliar os limites de unidades, candidatas ou meta sem mudar o restante da condição, mantendo o histórico. Alteração no código ou nos arquivos de entrada exige uma saída nova. Evite atualizar a branch enquanto a bateria está rodando.

## Arquivos para análise

Em cada configuração:

- `resumo.json`: contagens por subtópico, motivos de encerramento, modelos, cobertura do acervo e tokens/tentativas por etapa.
- `questoes.md`: leitura das aprovadas automaticamente.
- `questoes_aprovadas.jsonl` e `questoes_todas.jsonl`: itens com evidências, afirmações, revisões, teste cego e novidade.
- `unidades/*.json`: extração, verificações, complementos, propostas, rascunhos e quarentena.
- `artefatos_qa/*.json`: checkpoints, inclusive quando uma etapa de avaliação falha.
- `estados/*.json`: andamento, falhas e unidades sem objetivo.
- `revisao_humana.csv`: revisão de aprovadas e reprovadas, com identificação cega; campos humanos começam vazios.
- `evidencias_revisao.jsonl`: textos originais por identificação cega, permitindo conferir sustentação sem mostrar o parecer automático.
- `referencias_avaliacao/`: demonstrações, calibração e referências reservadas, com origem dos rótulos.

Na pasta `comparacao/`: `comparacao.md`, `comparacao.json`, `revisao_cega.csv` conjunta, `evidencias_revisao_cega.jsonl` e `mapa_revisao.json` separado. Não forneça o mapa ao revisor durante uma revisão cega. Preencha `sim`/`não` nas dimensões da revisão e repita:

```bash
bash pipeline/qa_v11/run_qa_v11_azure.sh comparar
```

A comparação calcula precisão nas aprovadas revisadas, falsas aprovações e falsas reprovações apenas quando todas as dimensões do item tiverem rótulo humano. Campos vazios não são aprovação. Inclui intervalo de Wilson para a precisão e preserva os rótulos preenchidos.

Para devolver os resultados por Git, depois de a execução terminar:

```bash
git add pipeline/qa_v11/saida_30
git commit -m "results: experimentos QA v11 nos três subtópicos"
git push origin codex/qa-evidencias-verificadas
```

O índice e o cache de chamadas ficam fora do Git. Os textos de evidência nos resultados pertencem ao mesmo acervo já autorizado no projeto. Use a pasta efetiva se tiver alterado `QA_V11_SAIDA`.
