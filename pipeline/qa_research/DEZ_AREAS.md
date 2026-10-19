# Documentos das dez áreas do especialista

O programa contempla **10 áreas, 40 frases e 217 recortes de pesquisa**. Cada
frase origina um documento técnico independente; a coleta também reúne esses
documentos em dez volumes, um por área. Não gera perguntas nesta etapa.

As frases integrais vêm de `pipeline/fase_3/topicos.py`. A curadoria de capítulos,
âncoras e consultas PT/EN está escrita explicitamente em `document/curation.py`,
sem planejamento por LLM. Os perfis materializados estão em
`configs/dez_areas_v1/01_01.json` até `10_01.json`, acompanhados de `programa.json`.
Produtos químicos conserva seu perfil e pacote originais: 12 dos 217 recortes.

| Área | Frases | Organização |
| --- | ---: | --- |
| 01 | 1 | Desempenho empresarial e KPI |
| 02 | 12 | Produção e Processo |
| 03 | 3 | Lastro, estabilidade, ancoragem, offloading e tanques |
| 04 | 2 | Sistemas e operações submarinas |
| 05 | 2 | Utilidades e energia elétrica |
| 06 | 7 | Segurança operacional, SGSO e riscos |
| 07 | 5 | Manutenção, inspeção e integridade |
| 08 | 5 | Saúde, segurança ocupacional e ambiente |
| 09 | 2 | Logística, suprimentos e cargas |
| 10 | 1 | Descomissionamento e ciclo de vida |

## Preparar nesta máquina

Na raiz do projeto, em PowerShell:

```powershell
& ./pipeline/qa_research/preparar_documentos_10_areas.ps1 -Device cuda
```

O script usa `.venv-documento-gpu/Scripts/python.exe`, quando disponível. Pode
indicar outro Python com `-Python 'C:/caminho/python.exe'`. `-Device auto` escolhe
CUDA quando o Python permite, ou CPU; `-Device cuda` falha claramente se CUDA não
estiver disponível. O ambiente isolado desta máquina herda o PyTorch CUDA já
instalado em `agent_lab`. Pesos e ambientes não são enviados pelo Git.

Em outra máquina, instale `requirements-local.txt` em ambiente separado e prepare
o snapshot `intfloat/multilingual-e5-small`, revisão
`614241f622f53c4eeff9890bdc4f31cfecc418b3`, no cache Hugging Face antes de executar.
O PyTorch precisa ter suporte CUDA para usar a GPU. A preparação roda offline.

A leitura conjunta usa Aho-Corasick para localizar as âncoras dos 39 perfis novos
em uma única passagem pelos originais. Mantém até 64 candidatos por recorte,
descarta listas bibliográficas, de siglas e de traduções sem explicação e reutiliza a fronteira salva. Não
calcula embeddings do corpus inteiro. Um único modelo E5, carregado uma vez,
processa janelas de 400 tokens com sobreposição e cache persistente por conteúdo.
A ordenação semântica e lexical é combinada por RRF; a seleção final controla
repetição e concentração em documentos identificáveis. A GPU acelera embeddings;
leitura, filtros, deduplicação e empacotamento usam CPU/disco.

O pacote antigo de Produtos químicos é validado e reutilizado. Pacotes novos
ficam em `pacotes/dez_areas_v1/`, com `lote.json` publicado somente depois que os
40 pacotes estiverem íntegros. Repetir o comando verifica os pacotes prontos e
processa apenas os que faltarem. Não execute duas preparações simultâneas.
`pacotes/dez_areas_v1/PREPARACAO.md` apresenta os escopos, recortes, âncoras,
consultas e quantidades de fontes; seu JSON registra distribuição e uso da GPU.

**Cobertura local:** o manifesto dos cinco bancos não está instalado nesta
máquina. A preparação usa os dois TXT Petroles e passagens originais das seleções
anteriores, com proveniência. Isso constitui um subconjunto temático, sem garantia
de exaustividade. Documentos gerados, questões, respostas e datasets de QA não
entram como fontes. Valores removidos como `<NUMBER>` não são reconstruídos.

Para enviar preparação e perfis ao Git:

```powershell
git add -- pipeline/qa_research/configs/dez_areas_v1 pipeline/qa_research/pacotes/dez_areas_v1
git commit -m "Preparacao local das dez areas FPSO"
git push origin codex/qa-evidencias-verificadas
```

Se não houver alterações, o commit dirá que não há nada novo a registrar.
Não use `git add .`: há outros diretórios locais fora deste trabalho.

## Gerar os documentos no servidor

Na raiz do checkout do servidor:

```bash
git pull --ff-only origin codex/qa-evidencias-verificadas
bash pipeline/qa_research/rodar_documentos_10_areas.sh
```

O script reutiliza `.venv-documento`, depois `venv`, depois `python3`.
`DOCUMENT_PYTHON=/caminho/python` permite escolher explicitamente o ambiente.
Se precisar preparar o ambiente leve:

```bash
python3 -m venv .venv-documento
.venv-documento/bin/python -m pip install -r pipeline/qa_research/requirements-server.txt
```

As credenciais Azure seguem a configuração já usada em Produtos químicos.
O servidor verifica os hashes dos 40 pacotes antes da primeira chamada. Não lê
TXT bruto, não calcula índices, não importa PyTorch/E5 e não chama embeddings
Azure. A pesquisa explora as fontes selecionadas e registra buscas adicionais
para eventual rodada local; não faz uma nova busca no corpus bruto no servidor.

Os documentos são executados sequencialmente, com até **3 chamadas simultâneas**
no documento corrente. O deployment e o esforço continuam
`gpt-5-4-petrobras:low`. Os tetos de tentativas são por frase, cumulativos; não
representam garantia de cobertura. `--max-calls 400` altera o teto por frase;
`--total-max-calls 6000` limita o lote inteiro, contando as tentativas anteriores.
Pesquisa, escrita e auditoria compartilham o orçamento; reparos também contam.

Produtos químicos pode reaproveitar as leituras verificadas do relatório v3,
mantendo redação e auditoria novas. As outras frases começam a pesquisa sobre
seus pacotes. O estilo permanece técnico, didático, autônomo e sem referências
no documento. Complementos do modelo têm origem e auditoria registradas à parte.

É possível executar uma parte:

```bash
bash pipeline/qa_research/rodar_documentos_10_areas.sh --only 02
bash pipeline/qa_research/rodar_documentos_10_areas.sh --only 04_01 04_02
```

Para acompanhar pelo terminal sem depender da sessão SSH:

```bash
nohup bash pipeline/qa_research/rodar_documentos_10_areas.sh > documentos_10_areas.log 2>&1 &
tail -f documentos_10_areas.log
```

Repetir o mesmo comando retoma os checkpoints. Documentos concluídos não geram
novas chamadas. Documento parcial não é tratado como concluído. Erros de backend
ou cancelamento interrompem o lote; esgotar o teto de uma frase permite continuar
as demais. Código, pacotes ou parâmetros semânticos alterados exigem nova saída.
Código de saída 2 sinaliza interrupção ou pendências, inclusive se parte foi
publicada corretamente. O resumo distingue esses casos. Para uma execução
selecionada, as frases não selecionadas continuam pendentes no resumo global.

## Devolver os resultados

Ao terminar, o terminal mostra **“O código acabou de rodar no terminal 🙂”**, o
estado real da execução e os comandos concretos para coletar, registrar e enviar.
Os padrões são:

```bash
.venv-documento/bin/python -m pipeline.qa_research.document.batch collect
git add -- pipeline/qa_research/relatorios/dez_areas_v1
git commit -m "Resultados documentais das dez areas FPSO"
git push origin codex/qa-evidencias-verificadas
```

Se usa outro Python, substitua o primeiro comando pelo interpretador informado
no aviso final. A coleta valida os documentos, registra hashes e reúne dez
arquivos `.md` e `.json` em `relatorios/dez_areas_v1/areas/`. `INDICE.md` abre o
conjunto; `indice.json` e `resumo_lote.json` registram o que existe e suas pendências.
Os 40 documentos individuais e as auditorias permanecem nas pastas `01_01` etc.
Referências e rastreabilidade ficam fora dos documentos de conhecimento.

A coleta concluída é imutável e pode ser verificada/reutilizada. Depois de uma
nova rodada no servidor, escolha outro `--destination`, como
`pipeline/qa_research/relatorios/dez_areas_v1_retomada`, para recolher a versão nova.
O aviso final já sugere destino novo se o padrão existe.

Nesta máquina, para receber:

```powershell
git pull --ff-only origin codex/qa-evidencias-verificadas
```

Os pedidos de busca ficam em cada `pedidos_busca.json`. Para ampliar um recorte,
revise a curadoria com base nesses pedidos e publique uma nova versão dos perfis
e pacotes, preservando as execuções anteriores.
