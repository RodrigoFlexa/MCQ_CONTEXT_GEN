# Fluxo contínuo de questões e comparação histórica

Esta implementação exige **nova pasta de saída** em relação ao piloto que falhou
em `continuo_v2`: código e prompts participam da identidade do experimento. O novo
padrão é `continuo_v3`; resultados anteriores permanecem intactos.

Entrada atual: `python -m pipeline.qa_research.piloto_qa.fluxo` ou
`bash pipeline/qa_research/rodar_piloto_qa.sh`. Sem teto de questões por documento.
O piloto fixo anterior permanece no módulo `piloto_qa`, documentado em
README_piloto_fixo.md. Usar uma saída nova para o fluxo contínuo.

## Funcionamento

1. Preparar versões antiga/refinada dos documentos 02_02, 03_03 e 07_01. Ajustes
   editoriais explícitos continuam em documents.py, com proteções do especialista.
   Snapshots históricos ficam intactos; pendências não são completadas pelo modelo.
2. Criar contextos de capítulos completos e conjuntos de capítulos do mesmo grupo
   editorial/sistema. Capítulos grandes são divididos entre blocos íntegros. Grupos
   grandes usam pares adjacentes que caibam completos; nunca truncar texto. Um bloco
   individual maior que o orçamento causa erro antes de qualquer chamada paga.
3. Percorrer os contextos em rodízio: capítulos, interfaces e novas passagens.
   Cada chamada cria até quatro candidatas, com alvos/evidências junto da redação,
   sem inventário prévio obrigatório. Pode retornar menos ou nenhuma candidata.
4. Priorizar classes com poucas questões novas aprovadas naquele documento,
   alternando empates: conceito, mecanismo, consequência, diagnóstico, decisão,
   procedimento. São prioridades, não cotas. Composição é simples/composta;
   diagnóstico e decisão exigem cenário. Dificuldade não é inventada pelo redator.
5. Mostrar até 30 enunciados aprovados, sem respostas, como memória: recentes
   daquele contexto e semanticamente relacionados. Exemplos de forma são seis
   questões próprias de outros assuntos, uma por classe. `--examples` permite
   leitura explícita de arquivos existentes. Não baixa nem altera datasets externos.
6. Depois de gerar, barrar duplicatas normalizadas e buscar cinco vizinhos
   semânticos por candidata em TODO o banco aprovado. E5 local só ranqueia: nenhum
   limiar fixo determina descarte. O auditor compara demanda, condições, conclusão
   e gabarito, também entre candidatas do lote. Mesmo assunto não basta para duplicação.
   Registrar vizinhos, escores e decisões.
7. Resolver sem gabarito e revisar com contexto desde a primeira chamada.
   Verificar suporte, correção, autonomia, determinação, pistas, novidade e composição.
   Gabarito mínimo até 60 palavras; critérios essenciais, equivalentes e erros
   materiais separados. Evidências devem ser literais nos blocos fornecidos.
8. Validar e salvar cada candidata independentemente na autoria, na resolução,
   no parecer e no refino. Uma linha inválida não invalida as irmãs. Reparar somente
   os IDs com erro; aprovações válidas já estão no disco antes das chamadas de reparo.
   Permitir um único refino de conteúdo, com nova resolução e revisão. Deduplicar
   novamente depois do refino. Incorporar aprovadas à memória e ao banco.
9. Três rodadas válidas sem ganho desativam aquele contexto; ganho reinicia seu
   contador. Encerrar quando todos estiverem sem ganho. Isso não certifica cobertura
   integral ou saturação conceitual.

Interfaces automáticas usam o campo grupo. Não há busca combinatória entre todos
os capítulos/documentos, inventário obrigatório de KUs, cota de compostas, teste de
ablação ou classificação formal de dificuldade. O julgamento semântico e técnico
continua sujeito a erro automático e exige análise do piloto.

## Retomada e limites

`--max-calls` é orçamento CUMULATIVO de tentativas por documento/grupo, não meta
de questões. Padrão 150; pode ser ampliado ao retomar. Prazo por chamada 300s,
até duas tentativas, com progresso a cada 30s. Falhas de serviço/formato e orçamento
suspendem a execução, preservam resultados e não contam como baixa produtividade.
O próximo documento/grupo só começa quando o atual termina, mantendo o banco
inicial reproduzível. Rodadas parcialmente revisadas têm checkpoint próprio por candidata. A retomada
não regenera candidatas já recebidas nem repete resoluções/pareceres válidos.
Erros individuais ficam em `erros_validacao`, com ID e caminho do campo, e no
resumo em `falhas_validacao`. `candidatas` inclui as inválidas; não mascara a autoria
como zero quando houve respostas rejeitadas.
Retorno 2 indica parcial; pode ser coletado. Orçamento maior não invalida resultados.
Documento, banco, código, prompts e configuração de conteúdo são congelados por hash;
mudanças exigem outra saída. `--memory-limit` e `--patience` configuram memória e parada.
Uma rodada inteiramente inválida não conta como rodada válida sem ganho.
Depois de `--max-invalid-rounds` falhas consecutivas (padrão 3), apenas aquele
contexto é suspenso; os outros continuam. Ao fim, `contextos_com_falhas` sinaliza
parcial, sem declarar saturação. Candidatas individuais que continuam inválidas
após o reparo recebem `invalida_contrato`; irmãs aprovadas permanecem no banco.

Somente JSON ilegível/envelope não recuperável ou falha de serviço usa repetição
da requisição inteira. Erros de linhas são separados após salvar o JSON e não
acionam a regeneração global do lote. Há no máximo um reparo de contrato por
candidata na autoria e uma repetição focalizada de resolução/parecer, além de um
refino de conteúdo. Pacotes grandes são divididos entre candidatas, sem truncar
seu contexto. Falhas de API e orçamento continuam suspendendo a rodada para
retomada e preservam todas as decisões já salvas.

Esse orçamento limita a geração. A avaliação paga é uma etapa adicional, com
volume proporcional ao número final de questões, descrito abaixo.

## Evidências e composição

O prompt contínuo define integralmente a autoria conjunta de alvos e questões,
sem herdar instruções de uma etapa com alvos previamente planejados. Questão
composta exige ao menos duas afirmações e ponte explícita da inferência necessária.
Uma ponte ausente gera erro individual; o Python nunca inventa a ligação para
aprovar a questão. O auditor ainda verifica se a composição é necessária.

Cada bloco fornecido possui `passagens` com IDs estáveis naquele documento e
intervalos exatos do texto original, por exemplo `B001_P001`. O modelo pode citar
`{"passagem":"B001_P001"}`. O Python expande o ID em bloco/trecho literais antes
da validação e do julgamento. ID desconhecido, bloco incompatível ou trecho que
contradiz a passagem são erros individuais. Não há correspondência aproximada,
paráfrase aceita como citação nem relaxamento de suporte factual.

O formato legado bloco/trecho continua aceito, com correspondência literal.
Evidências selecionadas não bastam para aprovação: resolução independente,
checagem dos critérios essenciais e parecer técnico continuam obrigatórios.

## Comparação e tabelas

Padrão `--arms both`:

| Grupo | Gerador | Contexto |
|---|---|---|
| Histórico | Questões existentes, 20 selecionadas por documento | Contextos originais |
| Novo + antigo | Fluxo contínuo | dez_areas_final_v2 |
| Novo + refinado | Mesmo fluxo contínuo | Documentos ajustados |

Os dois grupos novos partem do mesmo banco histórico para deduplicação e crescem
separadamente. Questões do grupo antigo não bloqueiam as do refinado. Dentro de
um grupo, aprovadas de cada documento entram no banco seguinte.
O histórico de comparação não é exemplo de autoria, mas pode aparecer na memória
de existentes porque participa da deduplicação. Relatar como geração incremental
contra banco conhecido; não como teste histórico reservado e cego.

Depois de gerar, calcular e imprimir tabelas, também em `TABELAS.html` (formatado),
`TABELAS.md` e CSVs em `tabelas/`. Saída parcial também tem tabelas parciais.
Campos ausentes não recebem zero. As tabelas incluem:

- Documentos: capítulos, blocos e palavras. Tamanho não é nota de qualidade textual.
- Volume, taxa de admissão, distribuição das seis classes e compostas.
- Overlap Q–C, Max ROUGE-L, Novel 2/3-gramas, Self-BLEU e duplicatas.
- Cosseno médio/vizinho, distância e Vendi E5; sensibilidade centrada separada.
- Acurácia estrita com/sem contexto, gap e IC 95%, por modelo e grupo.
- Sustentação dos gabaritos em auditoria adicional, insuficiências e contradições.
- Diferenças descritivas entre refinado, antigo e histórico.

Resultados integrais e amostras com mesmo N por documento/classe aparecem separados.
Não comparar Vendi/Self-BLEU com N diferente como equivalente. Sobreposição/novidade
não comprovam raciocínio. Grupos têm perguntas diferentes e diferenças não isolam
efeitos causais do contexto/gerador. Só a mesma pergunta com/sem contexto é pareada.

`--stage all` gera, mede e, quando a geração termina, avalia com os modelos pagos
e prompts históricos congelados. São seis respostas por questão (três modelos ×
com/sem contexto), mais julgamentos e auditoria por gabarito. O volume real aparece
antes da avaliação. Se a geração suspender, avaliação paga não começa automaticamente.

Modelos: autoria/refino GPT-5.4 medium; resolvedor GPT-5 medium; revisor GPT-5.4 high.
Avaliação: GPT-4.1 Nano/Mini/Full e juiz/auditor GPT-5.4 medium, mesmos aliases
existentes. `--mini-deployment` ajusta o alias do Mini. Autoria e revisão usam a
mesma família; isso não é auditoria entre famílias. Prompts: prompts_fluxo.py/prompts.py.

## Servidor

Na raiz do repositório, com o Python que já executa o pipeline:

```bash
git pull --ff-only origin codex/qa-evidencias-verificadas
export DOCUMENT_PYTHON="$PWD/.venv-documento/bin/python"
"$DOCUMENT_PYTHON" -m pip install -r pipeline/qa_research/piloto_qa/requirements-semantic.txt

# Apenas pesos do E5 em revisão fixada, reutilizando cache; não é dataset de questões.
"$DOCUMENT_PYTHON" -m pipeline.qa_research.piloto_qa.similarity

# Mostra contextos, sem API paga e sem escrever resultados.
bash pipeline/qa_research/rodar_piloto_qa.sh --plan

# Dois grupos novos + histórico, métricas, avaliação e tabelas.
nohup bash pipeline/qa_research/rodar_piloto_qa.sh --stage all --max-calls 300 \
  > piloto_qa_continuo_v3.log 2>&1 &
tail -F piloto_qa_continuo_v3.log
```

Saída: `pipeline/qa_research/saida_piloto_qa/continuo_v3`.
O comando permite até 300 tentativas por documento/grupo. Se preferir só gerar
e medir, usar `--stage generate`. Para só os refinados, usar `--arms refinado`
desde o começo em outra saída. Não mudar grupos/ordem de documentos na retomada.

Se aparecer suspenso_orcamento, aumentar o orçamento cumulativo e repetir:

```bash
nohup bash pipeline/qa_research/rodar_piloto_qa.sh --stage all --max-calls 600 \
  > piloto_qa_continuo_v3_retomada.log 2>&1 &
tail -F piloto_qa_continuo_v3_retomada.log
```

Recalcular tabelas sem API, ou executar somente avaliação:

```bash
bash pipeline/qa_research/rodar_piloto_qa.sh --stage metrics --embeddings
bash pipeline/qa_research/rodar_piloto_qa.sh --stage evaluate
```

Não ampliar o banco depois de começar a avaliação congelada. Se ampliar, usar
outra saída de experimento: o avaliador rejeita misturar questões, e as tabelas
omitem avaliações antigas incompatíveis com o banco atual.

## Coleta

Ao terminar aparece “O código acabou de rodar no terminal 🙂” e comandos concretos.
Depois das etapas desejadas, coletar para destino novo:

```bash
"$DOCUMENT_PYTHON" -m pipeline.qa_research.piloto_qa.fluxo \
  --collect pipeline/qa_research/relatorios/qa_continuo_v3
git add -- pipeline/qa_research/relatorios/qa_continuo_v3
git commit -m "Resultados QA continuo v2"
git push origin codex/qa-evidencias-verificadas
```

Inclui HTML, Markdown, CSV, decisões e hashes. Exclui cache privado, pesos e brutas.
Não altera datasets externos nem resultados históricos.

## Verificação

```bash
python -m unittest discover -s pipeline/qa_research/piloto_qa/tests -v
```

As regressões incluem lotes mistos com ponte vazia e evidência não literal,
falhas em resolução/parecer/refino, IDs ausentes/duplicados, reparo focalizado,
checkpoint antes do reparo, orçamento/interrupção e retomada, passagens exatas,
limite de falhas por contexto e divisão de payloads grandes. São testes offline.

Testes com modelos simulados: mais de 20 questões, memória limitada, tipos,
capítulos/interfaces, deduplicação posterior, retomada e isolamento dos grupos,
tabelas completas e avaliador histórico. E5 real também foi verificado localmente
sem API paga. Qualidade das questões novas depende do piloto e revisão humana.
