# Documento técnico primeiro — fluxo v3

Entrada: tópico, subtópico e frase integral do especialista. O comando padrão
termina no documento para leitura. Questões exigem solicitação explícita e um
contexto completo, tecnicamente liberado e compatível com o critério atual.

**Planejar → buscar/selecionar → escrever → revisar → complementar/corrigir uma vez.**

## O que mudou após o segundo piloto

A qualidade das afirmações e a cobertura do escopo são avaliadas separadamente.
Uma seção correta pode ser publicada mesmo com cobertura parcial. Lacuna essencial
mantém a pendência do ponto e bloqueia QA; limite opcional não rejeita a seção.
Uma afirmação errada ou não sustentada continua exigindo correção.

Consultas PT/EN usam expressões técnicas curtas, de preferência 3–12 palavras e no
máximo 16 por idioma. A busca mantém BM25/RRF, com uma oportunidade inicial para
cada coleção. A seleção lê até 12 candidatas por seção, retorna somente as úteis,
e permite até duas passagens de apoio. Não preenche quantidade com material genérico.

A pesquisa inicial faz uma seleção, sem expandir a própria busca. Depois da revisão,
uma lacuna essencial com consultas úteis pode motivar uma única complementação.
Somente passagens inéditas são avaliadas. Se não houver evidência direta nova,
o conteúdo correto é preservado e não é reescrito. Erros/editorial são corrigidos
uma vez com as fontes existentes, mesmo quando a busca adicional não ajuda.

A verificação editorial permite o uso físico de “trecho” e detecta metalinguagem
como “a base disponível” e “o conjunto disponível sustenta”. A redação deve explicar
termos profissionais e evitar repetir os mesmos fundamentos em todas as seções.

## Preparar o servidor e complementar o corpus

Na raiz do repositório:

```bash
git pull --ff-only origin codex/qa-evidencias-verificadas
export DOCUMENT_PYTHON="$PWD/.venv-documento/bin/python"
"$DOCUMENT_PYTHON" -m pip install -r pipeline/qa_research/v3/requirements.txt

"$DOCUMENT_PYTHON" -m pipeline.qa_research.v2.install_corpora \
  --output dataset/professional_corpora_v2 \
  --sources dupont bakerhughes slb_chemicals \
  --max-documents 3 --max-pages 5 --depth 0
```

São cinco documentos/páginas profissionais selecionados para as lacunas de
SRU/membranas, corrosão em gás com MEG, desemulsificação e controle microbiológico.
O catálogo e os limites de aplicação estão em [FONTES_QUIMICA.md](FONTES_QUIMICA.md).
Outras coleções íntegras do manifesto são preservadas; downloads já verificados são
reutilizados. Nenhum dataset externo de questões é baixado ou alterado.

Confira `dataset/professional_corpora_v2/install_report.json`. Falhas de coleta
ficam registradas; a geração ainda pode retornar parcial se faltar evidência.
`--retry-failed` permite repetir as URLs que falharem. O reparo de feed IMCA do
piloto anterior não precisa ser repetido para instalar essas três coleções.

Use Python 3.10+ e as mesmas credenciais Azure/CA do projeto. Se o ambiente tiver
outro nome, ajuste somente `DOCUMENT_PYTHON`.

## Executar o novo piloto somente documental

Use uma saída nova, preservando os pilotos anteriores:

```bash
bash pipeline/qa_research/rodar_piloto_fluxo_v3.sh \
  --item 02_02 --manifest dataset/professional_corpora_v2/manifest.json \
  --output pipeline/qa_research/saida_fluxo_v3/02_02_documento_03 \
  --stage context --check

nohup bash pipeline/qa_research/rodar_piloto_fluxo_v3.sh \
  --item 02_02 --manifest dataset/professional_corpora_v2/manifest.json \
  --output pipeline/qa_research/saida_fluxo_v3/02_02_documento_03 \
  --stage context > piloto_documento_02_02_03.log 2>&1 &
tail -f piloto_documento_02_02_03.log
```

`--check` testa redação e revisão com duas chamadas curtas. `--plan` mostra somente
a configuração, sem API nem escrita. O notebook `piloto_fluxo_v3.ipynb` chama a CLI
com `--stage context`. Uma única execução pode escrever em cada saída.

Repita o mesmo comando para retomar. Chamadas compatíveis concluídas são reutilizadas;
o orçamento gasto não é zerado. Mudanças em prompts, modelos de conteúdo, critério
ou corpus criam uma nova versão documental; resultados antigos não viram novos.
Alterações em workers, timeout e progresso não repetem trabalho já concluído.

## Ler o resultado e coletar

- `RELATORIO.md`: estado, cobertura por ponto, motivo de parada e pendências essenciais.
- `preparacao_corpus.json`: coleções verificadas, hashes e diagnóstico da instalação,
  incluído na coleta sem passagens originais.
- `contexto/documento.md`: seções tecnicamente liberadas, inclusive quando o escopo
  global ainda é parcial. Lacunas e referências ficam nos auxiliares.
- `contexto/rascunho_para_revisao.md`: todos os últimos rascunhos, inclusive seções
  rejeitadas. Serve para análise; nunca alimenta automaticamente QA.
- `contexto/cobertura.json`: elegibilidade de QA, cobertura publicada e cobertura
  antes da exclusão das seções, limites opcionais e lacunas essenciais.
- `contexto/versoes/.../`: plano, buscas, seleção, rastreabilidade e rascunhos.
  `revisao_*_modelo.json` preserva o parecer antes da verificação editorial local.

As passagens originais e as respostas brutas ficam em `.local/` no servidor e são
excluídas da coleta. Coletas somente documentais não incluem questões antigas.
Ao terminar, aparece “O código acabou de rodar no terminal 🙂” com o estado real e
os comandos concretos de coleta/commit/push. Retorno 0 significa concluído; 2,
parcial ou interrompido. Exemplo de coleta, após o processo encerrar:

```bash
"$DOCUMENT_PYTHON" -m pipeline.qa_research.v3 \
  --output pipeline/qa_research/saida_fluxo_v3/02_02_documento_03 \
  --collect pipeline/qa_research/relatorios/piloto_documento_02_02_03
git add -- pipeline/qa_research/relatorios/piloto_documento_02_02_03
git commit -m "Resultados do piloto documental 03 - 02_02"
git push origin codex/qa-evidencias-verificadas
```

A coleta é imutável: use um destino ainda inexistente. O arquivo de rascunhos deve
ser lido junto ao relatório para distinguir texto publicado de conteúdo pendente.

## Critérios, limites e QA

Há no máximo uma complementação e uma correção por seção. Uma entrega pode ser
útil e parcial. Sem novas evidências, repetir redação não fecha lacunas essenciais.
Duas requisições simultâneas, prazo de 300 segundos por tentativa e no máximo duas
tentativas por chamada lógica. O SDK não adiciona outra camada de repetição.
Heartbeat mostra a fase atual a cada 30 segundos; `--verbose` exibe os detalhes
operacionais. O JSONL sempre registra tentativas e uso de tokens.

Parâmetros em `piloto.json`: 12 candidatas por seleção, até oito passagens úteis,
até duas de apoio, 700 palavras como referência por seção e orçamento cumulativo
de 120 tentativas. Uma complementação conserva as evidências anteriores e pode
acrescentar até oito passagens; o empacotamento mantém as passagens integrais e
registra qualquer exclusão por tamanho. A seleção usa o modelo de redação; a revisão
mantém seu próprio modelo. Não há novos agentes ou biblioteca de orquestração.

`--stage qa` confere integridade, versão, todas as seções liberadas, todos os pontos
atendidos e ausência de lacunas essenciais/omissões. `--stage all` também respeita
a barreira; o piloto recomendado continua somente documental. QA conserva as seis
classes e os lotes de até oito candidatas com resolução sem gabarito e revisão.
Exemplos curados existentes só são lidos quando QA é solicitada e o contexto é
elegível; permanecem separados do suporte factual e do resolvedor.

A fundamentação da pesquisa está em [METODO.md](METODO.md). Testes offline verificam
fluxo e contratos; a qualidade técnica/didática precisa ser avaliada no piloto real.

```bash
python -m unittest discover -s pipeline/qa_research/v3/tests -v
```
