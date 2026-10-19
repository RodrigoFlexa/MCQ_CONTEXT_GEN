# Uma pauta do especialista, um documento e dois lotes de seis questões

O piloto padrão pesquisa **uma pauta**, escreve e revisa **um documento** e gera **dois lotes de até seis candidatas sobre esse mesmo documento**. Não são doze documentos nem uma meta de doze aprovações. Cada candidata passa por resolução independente, juiz, refino quando necessário, resposta cega, adjudicação e novidade. A aprovação continua automática e requer conferência de especialista.

Versão: `pesquisa-documentos-3-lotes`. Implementação preparada **sem testes, plano, geração ou chamadas a modelos localmente**, conforme a orientação do usuário. O primeiro experimento será feito no servidor.

## De onde vêm as pautas

O inventário `assuntos.json` conserva a frase original do especialista e os segmentos extraídos dela. O pipeline confere a correspondência dos textos com a frase e registra o programa completo em `programa_topico.json`, antes de pesquisar. O total de assuntos depende dessa segmentação, não da quantidade desejada de perguntas. Não fazemos nova segmentação paga a cada execução.

Para o subtópico de tanques, o inventário existente tem **21 segmentos: 19 pautas técnicas e dois segmentos classificados como genéricos**. Essa classificação é a do inventário, não uma certificação de que a divisão é a única possível.

O piloto seleciona apenas `a02`: **planejamento e sequência das operações de enchimento, esvaziamento, transferência interna e offloading**. É o primeiro assunto técnico na ordem do especialista. A frase completa é contexto de escopo; o documento deve desenvolver a pauta selecionada. Este experimento não cobre todo o subtópico. `DOCS_ASSUNTO_ID` permite selecionar outra pauta técnica por seu ID.

## Fluxo e lotes

1. Pesquisador escolhe o recorte e faz buscas adaptativas no acervo, com limites.
2. Redator desenvolve uma seção de livro técnico. Revisor confere as conclusões importantes contra as fontes originais; refinador corrige ou solicita pesquisa. Organização e extensão são livres.
3. Somente o documento aprovado alimenta o QA. O gerador propõe seis candidatas em uma chamada; o código atribui IDs e avalia cada candidata separadamente.
4. Depois da avaliação do primeiro lote, o gerador recebe o mesmo documento e as candidatas anteriores para propor outras seis. Trocar nomes ou cenários não estabelece novidade.
5. O verificador de novidade compara cada candidata com todas as anteriores aprovadas, inclusive as do outro lote. Não há reposição automática de reprovações.

Se o material não sustentar seis candidatas distintas, o lote pode retornar menos, inclusive zero, explicando a insuficiência. O piloto registra a saturação e continua para o outro lote dentro dos limites. Nenhum documento é criado de novo para preencher uma cota. Refinamentos e busca complementar de evidência por candidata continuam disponíveis.

As fontes são preservadas integralmente nos checkpoints. Cada chamada recebe contexto próprio do papel e as orientações de leitura uma vez por coleção (REGIS, Petrolês, ANP, HSE, BSEE). O redator pode usar seus conhecimentos para esclarecer conceitos e conectar ideias; as conclusões importantes precisam de fundamento. Opinião isolada, detalhes incidentais de instalação e generalidade vazia não devem sustentar o núcleo do documento ou do gabarito.

O índice BM25 com contexto vizinho, cliente Azure e banco de exemplos próprios/externos limpos são reaproveitados. Não há busca web automática nem novo framework. Sem o corpus completo no manifesto, a cobertura fica limitada ao índice e às seleções disponíveis; isso é registrado.

## Executar no servidor

Use o ambiente Azure que já funciona no projeto. Atualize depois de encerrar execuções antigas que usem o mesmo checkout ou índice.

```bash
cd /home/gbs2/MCQ_CONTEXT_GEN
git fetch origin
git switch codex/qa-evidencias-verificadas
git pull --ff-only origin codex/qa-evidencias-verificadas

export DOCS_TOPICO="Operação de tanques de carga e lastro"
export DOCS_ASSUNTO_ID=a02
export DOCS_QUANTIDADE=1
export DOCS_LOTES=2
export DOCS_QUESTOES_POR_LOTE=6
export DOCS_SAIDA="pipeline/documentos_tecnicos/saida_tanques_1doc_2x6"

nohup bash pipeline/documentos_tecnicos/run_azure.sh completo \
  > pipeline/documentos_tecnicos/console_tanques_1doc_2x6.log 2>&1 &

echo "PID: $!"
tail -F pipeline/documentos_tecnicos/console_tanques_1doc_2x6.log
```

Opcionalmente, antes de iniciar, `bash pipeline/documentos_tecnicos/run_azure.sh plan` mostra a frase, todas as pautas, a selecionada e o tamanho dos lotes, sem chamar APIs, baixar exemplos ou construir o índice. Não executamos esse comando localmente.

O script prefere `venv/bin/python`; configure `DOCS_PYTHON` se necessário. Não foram adicionadas dependências. Os exemplos externos são baixados e filtrados somente no modo completo, caso o arquivo ainda não exista. Para sair do acompanhamento sem encerrar a geração, use `Ctrl+C`.

A pasta é nova para separar as versões. Repita o mesmo comando para retomar checkpoints: o documento e os lotes gerados são reutilizados, e candidatas concluídas não são avaliadas novamente. Novos prompts, código, fontes, pauta, modelos ou desenho dos lotes exigem outra pasta. Metas e limites operacionais podem aumentar, mas número e tamanho dos lotes fazem parte da assinatura desta execução.

Para gerar somente o documento, use `documentos` e outra pasta de saída desde o início; o modo faz parte da assinatura. O modo antigo de uma questão por chamada e meta de aprovadas continua disponível com `DOCS_LOTES=0` e `DOCS_QUESTOES`, em outra saída. `DOCS_QUESTOES` e `DOCS_MAX_CANDIDATAS` não determinam o tamanho do piloto em lotes.

## Modelos e limites

| Papel | Deployment e esforço |
| --- | --- |
| Pesquisador/redator e gerador de lotes | `gpt-5-4-petrobras:low` |
| Revisor/juiz/adjudicador | `gpt-5-4-petrobras:low` |
| Refinador | `gpt-5-4-petrobras:low` |
| Respondente cego | `gpt-5-2-petrobras:low` |
| Novidade | `gpt-5-4-nano-petrobras:low` |

Tetos cumulativos: 400 tentativas de API globais, 24 por documento, quatro por geração de lote e 20 por candidata. Até quatro rodadas de busca por documento, três consultas por rodada, 32 trechos por unidade e um refinamento de documento/candidata. Cada chamada tem até duas tentativas; falha nas duas interrompe a execução para não multiplicar erros de contrato. Esses limites são proteções, não estimativas de consumo nem garantia de conclusão.

Código de saída `0`: documento aprovado, dois lotes completos gerados e todas as candidatas avaliadas sem interrupção. Isso **não exige doze aprovações**: rejeição, redundância, insuficiência ou decisão indeterminada de uma candidata são resultados registrados. Código `2`: piloto incompleto/erro, inclusive lote parcial por falta de conteúdo. Código `130`: interrupção pelo usuário. Consulte os estados e os motivos no resumo, não apenas o código de saída.

## Arquivos para analisar

Em `pipeline/documentos_tecnicos/saida_tanques_1doc_2x6/`:

- `programa_topico.json`: frase, segmentação completa, quantidades e origem; `pautas.json`: pauta selecionada e configuração dos lotes.
- `documentos.md` e `leitura/*.md`: documento técnico e referências; `documentos/*.json`: fontes, consultas, versões e revisões.
- `lotes/L01.json` e `lotes/L02.json`: candidatas originais dos lotes, exemplos usados e motivo de eventual insuficiência; `lotes.md`: candidatas e resultados por lote.
- `questoes.md` e `questoes_aprovadas.jsonl`: somente as aprovadas; `questoes_todas.jsonl` e `questoes/*.json`: todas as candidatas, incluindo reprovações, respostas cegas e histórico.
- `resumo.json`: solicitadas, geradas, avaliadas e estados por lote; contagem de aprovadas, cobertura, modelos e consumo.
- `revisao_humana.csv`: itens com identificação de lote, sem rótulo humano preenchido; não é uma revisão cega.
- `respostas_modelos/*.json`, `chamadas_llm.jsonl`, `uso_cache.json` e `run_config.json`: saídas brutas, inclusive inválidas, e diagnóstico, sem chaves de API.
- `referencias_avaliacao/`: partições de exemplos de apresentação, calibração e material reservado. Exemplos não são fontes factuais dos itens.

## Devolver os resultados

Quando terminar, mesmo se nenhuma candidata for aprovada:

```bash
git add pipeline/documentos_tecnicos/saida_tanques_1doc_2x6
git commit -m "results: um documento de tanques e dois lotes de seis"
git push origin codex/qa-evidencias-verificadas
```

Índice, caches e locks ficam fora do Git. As evidências e os históricos voltam para análise. O conjunto de prompts está documentado em `docs/pesquisa_prompts_2026_10_18/prompts_completos_revisados.md`; os textos executáveis são os módulos `prompts.py`, `qa_prompts.py` e `profiles.py`.
