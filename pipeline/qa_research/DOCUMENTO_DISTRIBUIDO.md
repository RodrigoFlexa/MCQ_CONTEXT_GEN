# Síntese técnica autônoma de Produtos químicos — v3

Este fluxo gera somente o documento de conhecimento do tópico 2.2. Produtos
químicos, em Produção e Processo. A futura geração de QA usará esse texto técnico.
Não são geradas questões, exemplos de QA nem alternativas nesta execução.

## Como deve ser o texto de contexto

O documento deve ensinar o domínio de forma independente: definir conceitos,
explicar mecanismos e relações de causa e efeito, organizar critérios de seleção,
aplicação, dosagem e monitoramento, discutir interações e consequências operacionais.
Cada seção tem subtítulo específico, sujeito claro e condições suficientes para
entender a relação técnica. Os princípios são situados em produção de óleo, água
e gás e em sistemas de FPSO quando essa aplicação for tecnicamente defensável.

As passagens recuperadas orientam a exploração do assunto. O autor pode usar seu
conhecimento técnico para desenvolver conceitos consolidados, conectar mecanismos
e preencher lacunas conceituais. Essa contribuição é identificada internamente;
não é atribuída ao corpus. Dados de campo, limites e resultados ausentes não são
preenchidos por suposição. Afirmações numéricas novas continuam exigindo suporte
nas passagens: complementar a explicação não recupera números apagados.

O produto apresenta diretamente o conhecimento. Referências, citações, autores/ano,
IDs, histórico de lacunas e comentários sobre fontes ficam em arquivos auxiliares.
O redator e o auditor devem evitar relato de leitura e ressalvas genéricas sobre
falta de fonte de FPSO, preservando as condições físicas e operacionais que de fato
restringem uma afirmação. Resultados de outros processos só contribuem com um
princípio transferível, sem transplantar cenários ou inventar validação offshore.

## O que mudou no código

1. O redator organiza uma síntese didática, com subtítulos e relações técnicas.
   Cada bloco declara internamente `base=corpus`, `conhecimento_tecnico` ou `mista`.
   Complementos do modelo são enumerados no campo interno `complementos`.
2. A auditoria confronta o conteúdo derivado do corpus com os originais e verifica
   cada complemento em uma chamada separada, com justificativa técnica. Um conceito
   consolidado não é reprovado só por não estar no corpus. Cada complemento precisa
   de avaliação explícita; o modelo não pode atribuí-lo a uma prova inexistente.
   Essa revisão é automatizada por modelo, não confirmação empírica independente.
3. Uma barreira editorial rejeita metadiscurso e citações no texto antes de publicar.
   A revisão reescreve somente relações reprovadas, preservando os blocos aprovados.
4. Duplicatas literais são removidas deterministicamente. A comparação semântica
   também considera pares dentro do mesmo capítulo, inclusive versões diferentes.
5. Lacunas permanecem internas. Explicações complementares aprovadas podem resolver
   lacunas conceituais; fatos de ativos e dados empíricos exigem evidência própria.
6. A execução termina com o aviso `O código acabou de rodar no terminal 🙂`, informa
   o estado real e imprime os comandos de coleta e de Git. Uma interrupção ou erro
   não é apresentado como sucesso.

## O que permanece pronto

O pacote `pacotes/produtos_quimicos_v2/` permanece byte a byte igual: 352 passagens,
12 recortes, citações por intervalos e os mesmos filtros lexicais, embeddings E5 e
fusão RRF já preparados aqui. **Não rode `prepare` no servidor.**

As bases disponíveis localmente não representam os cinco bancos completos.
A pesquisa no servidor explora o catálogo temático e registra pedidos adicionais
para futura preparação local. Nenhuma dessas mudanças exige recalcular embeddings.

A investigação já concluída em `relatorios/produtos_quimicos_v2/` também pode ser
reutilizada. São importadas apenas leituras, avaliações e achados após verificar
assinatura do pacote, arquivos e IDs. Redação, revisões e auditorias antigas não
são importadas. Os 259 achados da execução v2 são compatíveis com a nova redação.
O recibo fica em `pesquisa_reutilizada.json`; a retomada não reimporta nem sobrescreve
trabalho novo. Sem pesquisa anterior, o fluxo executa a investigação normalmente.

## Rodar no servidor

Na raiz do checkout, mantendo o ambiente e as credenciais Azure já usados:

```bash
git pull --ff-only origin codex/qa-evidencias-verificadas
bash pipeline/qa_research/rodar_documento_v3.sh
```

O script usa `.venv-documento/bin/python`, ou `venv/bin/python`, ou `python3`.
Para escolher explicitamente outro ambiente:

```bash
DOCUMENT_PYTHON=/caminho/do/ambiente/bin/python bash pipeline/qa_research/rodar_documento_v3.sh
```

A saída é `pipeline/qa_research/saida_documento_produtos_quimicos_v3/`. O documento
parcial é atualizado entre lotes de recortes. O script detecta o relatório v2 e
reutiliza sua investigação. Repita o mesmo comando para retomar uma interrupção.
Não use a pasta de saída v2 com código novo: as assinaturas protegem o histórico.

Em ambiente novo, as dependências do servidor continuam leves:

```bash
python3 -m venv .venv-documento
.venv-documento/bin/python -m pip install -r pipeline/qa_research/requirements-server.txt
```

Para manter a execução após desconectar do servidor:

```bash
nohup bash pipeline/qa_research/rodar_documento_v3.sh > documento_produtos_quimicos_v3.log 2>&1 &
tail -f documento_produtos_quimicos_v3.log
```

Nesse modo, o aviso aparece no log e no terminal que o acompanha. `Ctrl+C` encerra
apenas o acompanhamento. Para execução em primeiro plano, o primeiro comando
com `bash` já mostra o aviso diretamente e devolve o controle do terminal ao final.

O deployment continua `gpt-5-4-petrobras:low`, com no máximo três chamadas concorrentes
e orçamento cumulativo de 500 tentativas, incluindo reparos. O script aceita opções
extras de `run`, como `--max-calls 700` ou `--workers 2`, sem zerar o orçamento anterior.
Código de saída 0 indica processamento concluído; 2 indica interrupção/pendências.
Consulte também `resumo.json`: conclusão do processamento não significa cobertura
exaustiva ou confirmação científica independente.

## Arquivos entregues

| Arquivo | Uso |
|---|---|
| `documento.md` | Texto técnico para leitura e futura geração de QA |
| `documento_auditado.md` | Mesmo texto, mantido para compatibilidade com o nome anterior |
| `documento.json` | Somente título, capítulos, subtítulos e texto; sem referências/IDs/auditorias |
| `rastreabilidade.json` | Origem de cada bloco, complementos, suporte e decisões de auditoria |
| `cobertura.json`, `lacunas.json` | Cobertura e pendências internas |
| `suporte.jsonl`, `evidencias_citadas.jsonl` | Passagens originais e intervalos utilizados |
| `resumo.json`, `chamadas/`, `recortes/` | Estado da execução, prompts, versões e revisões |

Use `documento.md` ou `documento.json` como contexto da futura geração de QA.
A rastreabilidade é um recurso auxiliar de verificação e não integra o texto didático.

## Retornar os resultados pelo Git

Quando terminar, os comandos concretos serão impressos no terminal. Para a primeira
coleta da v3, equivalem a:

```bash
.venv-documento/bin/python -m pipeline.qa_research.document collect \
  --packet pipeline/qa_research/pacotes/produtos_quimicos_v2 \
  --output pipeline/qa_research/saida_documento_produtos_quimicos_v3 \
  --destination pipeline/qa_research/relatorios/produtos_quimicos_v3
git add -- pipeline/qa_research/relatorios/produtos_quimicos_v3
git commit -m "Resultados do documento Produtos quimicos - sintese v3"
git push origin codex/qa-evidencias-verificadas
```

O aviso usa o Python efetivamente executado. Se o destino de coleta já existir,
sugere outro nome com sufixo de retomada. O coletor recusa uma saída ainda em uso,
preserva hashes e exclui credenciais, índices e caches.

Aqui na máquina local:

```powershell
git pull --ff-only origin codex/qa-evidencias-verificadas
```

O notebook `documento_produtos_quimicos.ipynb` inspeciona o pacote e apresenta o
novo documento depois do retorno. A documentação da execução v2 e sua análise
continuam em `docs/analise_run_lexical_2026_10_19/` como histórico.
