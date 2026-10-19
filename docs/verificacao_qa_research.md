# Verificação da implementação — 19/10/2026

O novo motor está em `pipeline/qa_research/`, com notebook `pesquisa_e_qa.ipynb`.
O plano metodológico está em `plano_qa_research.md` e o uso em
`../pipeline/qa_research/README.md`.

## Executado

- **88 testes offline passaram**, usando `python -m unittest discover -s pipeline/qa_research/tests -q`.
- Validação do formato do notebook com `nbformat.validate`, compilação de suas células
  Python e compilação do pacote foram concluídas.
- Inspeção `--plan` validou as três origens: 40 arquivos de seleção ao todo, sem API.
- Indexação das seleções existentes: **7.457 registros de fonte**, deduplicados em
  **5.576 trechos únicos**. Coleções representadas: ANP, REGIS, Petrolês, HSE e BSEE.
- O índice declara `saved_selections_partial`: esses trechos não são o corpus bruto completo.

## Recuperação real no acervo disponível

As consultas abaixo foram executadas por BM25. A tabela registra o primeiro resultado,
sem afirmar que os demais sejam todos pertinentes ou que o resultado esteja auditado
tecnicamente. As consultas são verificações da busca, não exemplos de QA enviados a modelos.

| Consulta | Primeiro documento recuperado | Identificador do trecho |
|---|---|---|
| desaeração física tratamento químico | `BTP_1985_28_4_11_Tratamento_de_agua.pdf` | `regis:regis-2abff12c300b2f0d5a6ea665:pNone:w0` |
| THPS bactérias sésseis planctônicas | `BTP_2001_44_1_4_05_Avaliacao_da_acao.pdf` | `regis:regis-3c6ec3e8d5ac43c6d5b8a0b0:pNone:w4500` |
| benzotriazol compatibilidade sequestrante | `15001_Monografia-Versao-final.pdf` | `regis:regis-67e1ec53f1c608635e279664:pNone:w1500` |
| MEG monoetilenoglicol hidratos | `corpusPublicoIBICT-SemProcessamento.txt` | `petroles:petroles-4ee4bce16acf674505c8912d:pNone:w19612750` |

## O que os testes verificam

Os testes incluem proveniência, deduplicação, citações alteradas, fronteiras de
documento, integridade do manifesto e isolamento dos snapshots de índice. Também
verificam o caminho completo com modelo simulado: pesquisa, expansão por descoberta,
pesquisa solicitada pela auditoria, redação, auditoria, extração, QA e exportação.

Foram testadas rejeições de blocos sem suporte, unidades ambíguas, opinião promovida
a QA factual, resposta cega ambígua, falha de chamada, orçamento esgotado e corrupção
da cadeia fonte→bloco→unidade→QA. O respondente recebe somente pergunta, passagens e
limite de palavras, sem gabarito ou alvo. Retomada não repete chamadas concluídas e
o orçamento permanece cumulativo.

## Piloto com os modelos

Foi tentada a execução do perfil de dois recortes, mas ela parou na configuração do
cliente: `AZURE_OPENAI_ENDPOINT`, `AZURE_OPENAI_API_KEY` e `AZURE_OPENAI_API_VERSION`
não estavam definidas para o backend existente. **Nenhuma tentativa de API foi
reservada e nenhum documento ou QA foi produzido por modelos nesse piloto.**

Os diagnósticos estão em `pipeline/qa_research/saida_diagnostico_sem_credenciais/`.
A pasta padrão do piloto fica livre para executar o notebook após configurar o
backend. Credenciais não foram impressas nem incorporadas aos artefatos.

Consequentemente, a verificação atual confirma a implementação, os filtros e a
recuperação local. Ainda falta avaliar a qualidade da pesquisa, redação e QA com
modelos reais e revisão técnica humana. A meta de duas QA do piloto e a de vinte
do perfil maior são metas de execução, não resultados já obtidos.
