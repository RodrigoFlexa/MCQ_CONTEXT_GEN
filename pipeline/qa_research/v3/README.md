# Contexto e questões por seções e lotes — v3

Entrada: tópico, subtópico e frase integral do especialista. O fluxo novo gera seções
diretamente das passagens recuperadas, revisa o conjunto e corrige uma vez. QA usa
lotes de até oito candidatas: autoria → resolução sem gabarito → revisão. Refino é
seletivo, uma vez, com nova resolução/revisão das modificadas. Não utiliza o Runner
documental anterior. Busca e utilidades de idioma reaproveitam componentes sem geração.

## Instalar e conferir no servidor

Na raiz do checkout, após encerrar uma execução anterior que não deseja continuar:

```bash
git pull --ff-only origin codex/qa-evidencias-verificadas
export DOCUMENT_PYTHON="$PWD/.venv-documento/bin/python"
"$DOCUMENT_PYTHON" -m pip install -r pipeline/qa_research/v3/requirements.txt

bash pipeline/qa_research/rodar_piloto_fluxo_v3.sh \
  --item 02_02 --manifest dataset/professional_corpora_v2/manifest.json \
  --output pipeline/qa_research/saida_fluxo_v3/02_02_piloto_01 --check
```

Se o ambiente tiver outro nome, ajuste somente `DOCUMENT_PYTHON`. Requer Python
3.10+ e as mesmas credenciais Azure/CA do projeto. Não muda endpoint nem certificado.
`--check` verifica o manifesto e testa os deployments/esforços de autoria, revisão
e resolução: são até três chamadas lógicas, com retentativas limitadas, registradas
no mesmo orçamento. Não gera contexto nem questões. `--plan` mostra somente a
entrada/configuração, sem criar saídas ou acessar a API.

O corpus já instalado é reutilizado. Não há download ou alteração de datasets de QA.
O instalador de documentos profissionais existente permanece separado e pode ser
usado para reparar um manifesto bloqueado antes de iniciar a geração.

## Rodar o piloto

```bash
bash pipeline/qa_research/rodar_piloto_fluxo_v3.sh \
  --item 02_02 --manifest dataset/professional_corpora_v2/manifest.json \
  --output pipeline/qa_research/saida_fluxo_v3/02_02_piloto_01
```

Em segundo plano, sem perder a execução ao desconectar do SSH:

```bash
nohup bash pipeline/qa_research/rodar_piloto_fluxo_v3.sh \
  --item 02_02 --manifest dataset/professional_corpora_v2/manifest.json \
  --output pipeline/qa_research/saida_fluxo_v3/02_02_piloto_01 \
  > piloto_fluxo_v3_02_02.log 2>&1 &
tail -f piloto_fluxo_v3_02_02.log
```

Use uma única execução por saída. Repita o mesmo comando para retomar. Chamadas
validadas e lotes concluídos são reutilizados; tentativas gastas não são zeradas.
Uma pendência de QA interrompe o lote e preserva os anteriores; na retomada, as
respostas intermediárias validadas também são reutilizadas. Se precisar ampliar o
orçamento cumulativo, acrescente `--max-calls 160` explicitamente.

`--stage context` executa só contexto. `--stage qa` utiliza o documento desta saída,
conferindo seu conteúdo com o que foi revisado e com a rastreabilidade. Uma alteração
manual do documento exige nova geração/revisão. Mudanças de conteúdo, modelos ou
prompts criam versões por etapa e preservam o histórico; escopo/schema diferentes
exigem outra saída. Alterações em concorrência, timeout e progresso não invalidam
as respostas concluídas. Mudança no corpus refaz sua verificação antes da API.

## Limites e decisões

- Duas requisições simultâneas; atualização a cada 30 segundos com a etapa e tempo
  de espera atual. O terminal explica o motivo de cada repetição real. `--verbose`
  mostra também números de tentativas e limites de tokens; o JSONL registra sempre
  os detalhes, mesmo no modo normal.
- Prazo de 300 segundos por tentativa de requisição, incluindo cancelamento via
  cliente assíncrono. Espera por vaga é contabilizada separadamente.
- No máximo duas tentativas por chamada lógica. Orçamento inicial: 16.000 tokens;
  truncagem usa 32.000 na tentativa restante. SDK sem retentativas adicionais.
- Revisão documental conjunta: técnica, suporte, cobertura e PT-BR. Se a entrada
  ultrapassar o teto configurado, divide por seções completas e faz coerência final.
- Na redação, pacotes grandes recebem sumário/metadados compactos e seleção por
  tamanho serializado. Passagens são mantidas inteiras ou excluídas com motivo;
  o texto original e a frase do especialista não são cortados. O ajuste fica em
  `contexto/versoes/.../entradas/`, incluído na coleta. Os pacotes que já cabem
  permanecem iguais para reutilizar chamadas compatíveis em uma retomada.
- Uma rodada de correção documental; partes problemáticas ficam fora do contexto
  de QA. As demais podem alimentar uma entrega parcial explicitamente registrada.
- Meta inicial de 40 questões, cobertura dos pontos prioritários liberados, até
  12 lotes/96 candidatas novas e 120 tentativas externas incluindo falhas/preflight.
- Saturação: dois lotes sem novas admitidas, após dar oportunidade a todas as seções.
- As seis classes e a composição simples/composta são preservadas. Duplicatas são
  verificadas dentro/entre lotes na revisão. Não há seis questões obrigatórias por ponto.
- Lacunas encontradas na QA são registradas para a próxima versão documental.

Configuração em `piloto.json`. Os limites são hipóteses do piloto, sem garantia de
quantidade, duração ou validação científica. `concluido` exige a meta configurada;
`parcial` e `interrompido` não são apresentados como sucesso. Aprovação por modelo
continua sujeita à avaliação pelo especialista.

Exemplos curados existentes de outros subtópicos são lidos por padrão. Arquivos
adicionais podem ser indicados com `--examples /caminho/existente.jsonl`; a opção
substitui a lista padrão. Somente pergunta/resposta/tipo e origem são utilizados.
Os exemplos ficam separados do corpus factual e nunca são enviados ao resolvedor.

## Resultados e coleta

Leia `RELATORIO.md` e `resumo.json`. O contexto está em `contexto/documento.md` e
`documento.json`; fontes/pareceres/cobertura ficam nos auxiliares. As questões estão
em `questoes/qa.csv`, `admitidas.json` e `decisoes.json`. As versões mantêm seu histórico.
As respostas brutas e as evidências originais ficam somente em `.local/` no servidor.

Ao terminar aparece `O código acabou de rodar no terminal 🙂`, o estado real e os
comandos de coleta/commit/push com um destino novo. Retorno 0 indica conclusão; 2,
parcial/interrupção. Também pode coletar manualmente após a execução encerrar:

```bash
"$DOCUMENT_PYTHON" -m pipeline.qa_research.v3 \
  --output pipeline/qa_research/saida_fluxo_v3/02_02_piloto_01 \
  --collect pipeline/qa_research/relatorios/piloto_fluxo_v3_02_02_01
git add -- pipeline/qa_research/relatorios/piloto_fluxo_v3_02_02_01
git commit -m "Resultados do piloto fluxo v3 - 02_02"
git push origin codex/qa-evidencias-verificadas
```

A coleta é imutável e verifica hashes. Exclui credenciais, cache, respostas brutas e
passagens originais do corpus. O notebook `piloto_fluxo_v3.ipynb` apenas chama a CLI.

## Testes offline

```bash
python -m unittest discover -s pipeline/qa_research/v3/tests -v
```

Testes simulados verificam contratos, fluxo, retomada, parcial, bloqueio técnico,
refino, duplicatas, erro 500, truncagem e cancelamento por prazo. Não medem a qualidade
do conteúdo produzido pelo deployment real; essa medição pertence ao piloto.
