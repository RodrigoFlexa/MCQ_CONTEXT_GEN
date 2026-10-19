# Próxima execução: fluxo documental v2

Use [DOCUMENTO_DISTRIBUIDO.md](DOCUMENTO_DISTRIBUIDO.md): o pacote de Produtos químicos
já vai preparado pelo Git. Esse fluxo dispensa corpus bruto, indexação e embeddings
no servidor e gera somente o documento. As instruções abaixo são do fluxo anterior.

# Fluxo anterior: documento de 2.2. Produtos químicos no servidor

Para poupar CPU e disco do servidor, prefira **preparar o pacote fora dele e
executar com `--pack`**. Veja o fluxo em [`PREPROCESSAMENTO.md`](PREPROCESSAMENTO.md),
incluindo a exportação de um índice existente sem reler o corpus bruto. Os comandos
abaixo com `--manifest` continuam válidos e preparam/verificam índices no servidor.

Use a raiz do checkout e o ambiente Azure que já funciona no servidor. Os comandos
abaixo usam o caminho registrado no projeto, `/home/gbs2/MCQ_CONTEXT_GEN`, e
`venv/bin/python`. Ajuste esses dois caminhos se a instalação for diferente.

## Atualizar e conferir as entradas

```bash
cd /home/gbs2/MCQ_CONTEXT_GEN
git fetch origin
git switch codex/qa-evidencias-verificadas
git pull --ff-only origin codex/qa-evidencias-verificadas

QA_PYTHON=venv/bin/python
"$QA_PYTHON" -m pip install -r pipeline/qa_research/requirements.txt

"$QA_PYTHON" -m pipeline.qa_research.run \
  --config pipeline/qa_research/configs/produtos_quimicos.json \
  --manifest dataset/domain_corpora/manifest.json \
  --stage pesquisa \
  --plan
```

`--plan` não faz chamadas de modelo. O manifesto deve ser o do corpus completo já
instalado. A execução verifica sua integridade antes das chamadas. Se o manifesto
estiver em outro lugar, substitua o caminho em ambos os comandos.

As credenciais são lidas pelo backend existente a partir do `.env` da raiz ou do
ambiente do processo. Elas não são fornecidas nem alteradas pelos comandos acima.
O deployment padrão é `gpt-5-4-petrobras:low`, conforme o ambiente utilizado nas
execuções anteriores. A configuração `models` permite alterá-lo por papel.

## Gerar somente o documento

```bash
nohup "$QA_PYTHON" -u -m pipeline.qa_research.run \
  --config pipeline/qa_research/configs/produtos_quimicos.json \
  --manifest dataset/domain_corpora/manifest.json \
  --stage pesquisa \
  > pipeline/qa_research/produtos_quimicos_hibrido_documento.log 2>&1 &

echo "PID: $!"
tail -F pipeline/qa_research/produtos_quimicos_hibrido_documento.log
```

`Ctrl+C` encerra o acompanhamento do log; a geração continua no processo iniciado
por `nohup`. Esta etapa faz planejamento, pesquisa, redação e auditoria. Não executa
extração de unidades nem geração/avaliação de QA.

O perfil usa o escopo completo fornecido para **2.2. Produtos químicos**, propõe
oito recortes iniciais e admite até dezesseis com as descobertas. Permite até quatro
rodadas de pesquisa por recorte, três pesquisadores simultâneos, uma revisão de
capítulo e 500 tentativas de API cumulativas. Não é o piloto reduzido de dois recortes.

## Conferir o resultado

Quando o processo terminar, o documento consolidado estará em:

```text
pipeline/qa_research/saida_produtos_quimicos_hibrido/documento_auditado.md
```

Para ler no terminal:

```bash
less pipeline/qa_research/saida_produtos_quimicos_hibrido/documento_auditado.md
```

A recuperação agora combina BM25, embeddings Azure e reranqueamento. A primeira
execução prepara o índice vetorial completo; as seguintes reutilizam o cache.
O deployment é `embedding-3-large-global` para `text-embedding-3-large`, em 3.072 dimensões.
O limite de evidências é de 64 por recorte. Detalhes em [`HIBRIDA.md`](HIBRIDA.md).

Os arquivos `relatorio.md` e `resumo.json` na mesma pasta mostram capítulos publicados,
falhas e interrupções. `cobertura.json` apresenta os recortes e lacunas; `recortes/`
guarda as versões e auditorias. Um documento pode ser parcial ou vazio quando as
fontes não sustentarem os blocos. A aprovação é automática, com revisão humana pendente.

Para retomar uma execução interrompida, repita o comando de geração com a mesma
configuração e saída. Não inicie duas execuções na mesma pasta. Para uma nova
investigação independente, acrescente `--output pipeline/qa_research/saida_produtos_quimicos_v2`.

Sem corpus completo instalado, pode-se retirar `--manifest` para pesquisar somente
os trechos originais das seleções salvas. Nesse caso, o resultado declara cobertura
parcial; não é uma pesquisa no corpus bruto completo.
