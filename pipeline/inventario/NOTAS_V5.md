# Notas v5 e QA v10

As notas passam a ensinar relações técnicas reutilizáveis com condições e limites.
O modelo pode contribuir com explicações paramétricas, sem apresentá-las como extrações.
O QA recebe as relações e a rubrica revisadas; não há número mínimo de alvos por nota
nem obrigação de produzir uma questão difícil.

## O que mudou

- `schema_conhecimento=nota-v5`; cada relação tem origem `fonte`, `deducao` ou `parametrico`,
  natureza, aplicabilidade, condições, limites, referências e premissas.
- `avaliavel` é calculado no código. Uma contribuição paramétrica continua auxiliar mesmo
  se citar um documento. Deduções exigem todas as premissas avaliáveis e herdam condições,
  limites e evidências. Estudo, incidente, checklist e procedimento local não viram
  automaticamente conhecimento geral para um gabarito. A avaliação semântica cabe ao revisor.
- O redator pode explicar livremente, comparar e conectar ideias. Não há cota de seções,
  frases, perguntas por nota ou níveis. A suficiência das notas novas depende de haver
  relações e alvos sustentados, não de um mínimo de palavras.
- Os alvos incluem habilidade, relações, condições para o enunciado, resposta, critérios e
  respostas aceitáveis. Alvos sem sustentação ficam em `alvos_bloqueados`. Relação e habilidade
  idênticas não criam outro alvo pela troca de cenário ou nível.
- Até duas lacunas com consultas pt/en acionam uma busca complementar lexical em candidatos
  já recuperados. São até quatro novas passagens e uma segunda redação por nota. O mecanismo
  não pesquisa a internet nem faz nova varredura de todos os corpora. Sem os índices antigos,
  utiliza os trechos das seleções salvas. A ausência de evidência continua limitando os alvos.
- O revisor recebe a proveniência e não pode retirar o schema ao corrigir. Markdown e JSON
  preservam relações, limites, lacunas e trilha de complemento.
- As combinações novas precisam mobilizar relações avaliáveis de cada nota, com resposta e
  rubrica. O juiz deve verificar se a integração é necessária.
- QA v10 conserva o contrato da nota; a triagem de alvos legados continua disponível.
  O gerador pode retornar `evidencia_insuficiente`. Comparações e decisões justificadas são
  permitidas como um objetivo coerente, sem impor resposta de uma palavra.
- O juiz precisa mapear afirmações em referências existentes. Passagens completas T# ficam
  disponíveis como evidência, além de fatos extraídos; condições e identificadores são exportados.
- Uma análise independente vê apenas a pergunta, responde e registra condições ausentes e
  alternativas. O comparador deve verificar ambas as respostas, incluindo a referência.
  Discordância sozinha não reprova. `referencia_invalida` reprova; erro de chamada deixa o
  item `pendente_validacao`, fora das aprovadas.
- O refinador tem uma tentativa no total e pode mudar pergunta/explicação, preservando
  resposta, rubrica e evidências. Mudança nesses campos é recusada.
- Novidade compara vizinhos mesmo abaixo do limiar de cosseno; no CLI, o escopo padrão é
  o tópico, alcançando questões de outros subtópicos. Similaridade continua sendo uma busca
  aproximada; não é garantia de eliminar toda repetição. Benchmarks externos ficam opcionais
  (`--com-exemplos-externos`); exemplos do especialista continuam no prompt.

## Rodar no servidor

Na raiz do repositório, com o ambiente Python e as credenciais Azure já usados nas rodadas anteriores:

```bash
git pull --ff-only origin dev
bash pipeline/inventario/run_notas_v5_azure.sh plan
nohup bash pipeline/inventario/run_notas_v5_azure.sh piloto > pipeline/inventario/console_notas_v5_piloto.log 2>&1 &
echo "PID: $!"
tail -F pipeline/inventario/console_notas_v5_piloto.log
```

`plan` não chama APIs. O piloto reconstrói até seis conceitos por subtópico em separadores
trifásicos, SGSO e tanques de carga/lastro. Reaproveita fatos, conceitos e passagens dos três
inventários existentes e pede até dez aprovadas por tópico. A fila pode terminar antes da cota
se não houver alvos sustentados suficientes; isso não deve ser compensado com questões inventadas.

O script faz a reconstrução e, em seguida, o QA. Resultados:

```bash
cat pipeline/inventario/saida_notas_v5_piloto/resumo.json
cat pipeline/qa_v7/saida_v10_piloto/resumo.json
```

Inspecione `subtopicos/*/documento.md`, `notas_aprovadas.jsonl`, `ocorrencias.jsonl` e
`pipeline/qa_v7/saida_v10_piloto/relatorio.md`. Há casos pendentes e evidência insuficiente
além de aprovações/reprovações. O rótulo fácil/média/difícil continua sendo o tipo solicitado,
não uma dificuldade humana medida. Revise uma amostra com o especialista.

Após avaliar o piloto, para reconstruir todas as notas e gerar a cota de 100 por tópico:

```bash
nohup bash pipeline/inventario/run_notas_v5_azure.sh completo > pipeline/inventario/console_notas_v5_completo.log 2>&1 &
echo "PID: $!"
```

As pastas completas são `pipeline/inventario/saida_notas_v5_completo` e
`pipeline/qa_v7/saida_v10_completo`. As saídas anteriores são preservadas. Repetir exatamente
o mesmo comando usa o cache; mudar configuração/fontes exige outra pasta. A reconstrução
não repete extração de fatos nem conceitos. O redator e o revisor novos fazem chamadas pagas,
assim como embeddings, combinações e QA; este código foi validado offline, não na Azure.

Variáveis opcionais: `QA_PYTHON`, `QA_WORKERS`, `V5_MODELO_NOTAS`, `V5_EFFORT`,
`V5_MAX_CHAMADAS`, `V5_SAIDA_NOTAS`, `V5_SAIDA_QA`, `QA_POR_TOPICO`, `QA_GERADOR`,
`QA_JUIZ`, `QA_RESPONDENTE`. No piloto: `V5_SUBTOPICOS` (separador `|`) e
`V5_LIMITE_CONCEITOS` (padrão 6). Para repetir só o QA do piloto, use modo `qa`.

Para um recorte diferente ou para desligar o complemento:

```bash
python3 -u pipeline/inventario/reconstruir_notas.py \
  --origens pipeline/inventario/saida_mais_4_topicos_v4_nano_low \
  --saida pipeline/inventario/saida_notas_v5_separadores \
  --subtopicos 'Operação de Separadores Trifásicos' \
  --limite-conceitos-por-subtopico 6 --sem-complemento-notas
```

## Verificação offline

```bash
python3 -m unittest discover -s pipeline/inventario/tests
python3 -m unittest discover -s pipeline/qa_v7/tests -t .
```

As regressões cobrem contribuições paramétricas com citações, dependências de deduções,
transferência de casos/checklists, contratos incompletos, duplicação de alvos, complemento,
reconstrução sem alterar origens, aprovação com erro cego, mudança de gabarito pelo refinador,
evidência insuficiente e repetição entre subtópicos. Modelos simulados validam o fluxo e
as invariantes; a qualidade técnica da geração real precisa ser medida no piloto.
