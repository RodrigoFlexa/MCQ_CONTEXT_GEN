# Rubrica de dificuldade v2 (23/10/2026)

Vale para a geração por janela (`prompt_janela_qa_13.md`) e para o inventário
(`inventario_docs/prompts/questao.md`). As checagens de forma estão em `dificuldade.py`.

## Por que mudar

No piloto inventário x EC (`relatorios/piloto_inventario_20261023T042252Z`), o modelo pequeno sem
contexto (`gpt-4-1-nano-petrobras`) acertou tanto as difíceis quanto as fáceis (0,60 a 0,67 x 0,56 a
0,69). Lendo as 200 questões:

- As 19 questões com forma de sim ou não, de escolha entre duas opções dadas ou de "conclusão correta
  sobre a decisão" tiveram acurácia 0,89. A resposta era sempre "Não, considere o contexto".
- As difíceis que o modelo acertou traziam no enunciado a interpretação dos sinais ("as lições foram
  copiadas sem verificar", "houve espera logística"); a resposta só repetia essa interpretação, ou era
  um princípio de prudência válido em qualquer cenário.
- As difíceis que o modelo errou pediam um mecanismo, espécie ou ação específicos que não estavam no
  enunciado e que diferiam da resposta óbvia: barita (BaSO4) pela mistura de águas, BRS e H2S no
  volume estagnado, oxidante degradando o inibidor, limpeza mecânica em vez de mais biocida,
  anti-incrustante adsorvendo na rocha junto ao injetor.

## Definição

A dificuldade é o trabalho que o respondente precisa fazer e que o enunciado não faz por ele:

1. **inferências encadeadas**: quantos passos separam os dados do enunciado da resposta, com o passo
   intermediário ausente do enunciado (a "ponte" de MuSiQue e de Cheng et al., 2021);
2. **resposta atraente descartada**: existe uma resposta óbvia, a que um profissional generalista daria
   olhando só o sintoma principal, e uma observação do enunciado a torna errada.

Tamanho do enunciado, siglas, vocabulário raro e informação omitida não contam.

| Nível | Operação | Enunciado |
|---|---|---|
| fácil | recordar um conceito, função, parâmetro, causa ou efeito específico | até 35 palavras, sem cenário |
| média | aplicar uma relação a uma condição dada; responder com a consequência, variável, direção ou critério | até 60 palavras |
| difícil A (diagnóstico com resposta atraente) | observações de um único mecanismo; o sintoma principal sugere uma explicação ou ação comum que outra observação descarta; a resposta é outro mecanismo, causa, espécie ou ação | até 90 palavras |
| difícil B (encadeamento) | observação ou ação → relação 1 → estado intermediário não dito → relação 2 → resposta; inclui um efeito que mascara o sinal de outro | até 90 palavras |

## Regras de forma (todos os níveis)

1. Pergunta aberta, com resposta específica: a última frase usa qual, que, como, onde, quando, quanto,
   por que. Proibido: sim ou não ("basta?", "justifica?", "é adequado?"), escolha entre opções dadas
   ("entre manter e rever, qual decisão?") e "qual a conclusão correta sobre essa decisão?".
2. A resposta não pode ser prudência genérica que acertaria qualquer cenário ("considerar o contexto",
   "investigar antes de concluir", "não decidir só pelo indicador").
3. O enunciado descreve observações (medições, tendências, o que foi verificado e descartado), não a
   interpretação delas.
4. O termo decisivo da resposta, ou um sinônimo evidente, não aparece no enunciado.
5. Em comparações, os lados diferem só na condição que importa.
6. Resposta: começa pelo elemento decisivo; no máximo uma oração de justificativa; até 30 palavras.

## Campo `desenho` (obrigatório nas difíceis)

- `passo_oculto`: a inferência intermediária que o respondente precisa fazer e que o enunciado não diz;
- `resposta_atraente`: a resposta que um generalista daria olhando só a pista mais saliente;
- `sinal_que_descarta`: a observação do enunciado que torna a resposta atraente errada.

O campo não vai para o respondente nem para o juiz; serve para forçar o desenho e para auditoria.

## Medição

Dois respondentes sem contexto (`gpt-4-1-nano-petrobras` e `gpt-5-4-nano-petrobras:low`) e um juiz
forte (`gpt-5-4-petrobras:high`). O juiz marca, além do veredito, `referencia_valida` e
`atalho_generico` (uma resposta genérica de prudência seria aceita). O relatório também simula um
filtro adversarial ao estilo de Humanity's Last Exam: a acurácia do primeiro respondente nas questões
que o segundo errou.

Referências: Trivedi et al., MuSiQue (TACL 2022); Cheng et al., Guiding the Growth (ACL 2021);
Phan et al., Humanity's Last Exam (2025); Haladyna, Downing e Rodriguez, diretrizes de redação de
itens (pistas e "testwiseness").
