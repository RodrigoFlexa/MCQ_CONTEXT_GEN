# Lastro v4 — revisão do código e dos resultados

Resultados recebidos no commit `aeecfa7`, analisados em 13/10/2026. A conversa anexada é contexto; os números abaixo foram recontados nos arquivos.

## Resultado

Execução: concluido_com_ocorrencias; 109.1 minutos; 311 notas aprovadas em 3 subtópicos e 68 assuntos com contexto.
Fatos: 2488 retidos, 341 descartados; 2488 citações retidas correspondem ao trecho de origem segundo o verificador.
Notas: mediana 756 palavras; 319 a 1464 palavras. 234282 palavras nas notas únicas; o resumo por assunto soma 235171 porque uma nota pode atender a mais de um assunto.
O inventário de Lastro já pode contar como o primeiro tópico. Sua utilização em QA requer enunciados autossuficientes e preservação das condições das fontes.

| Subtópico | Notas aprovadas únicas | Palavras nas notas |
|---|---:|---:|
| Operação de Offloading | 107 | 81499 |
| Operação de tanques de carga, lastro, sistema gás inerte, ventilação e estabilidade | 88 | 64520 |
| Sistema de ancoragem, manutenção e monitoramento da posição | 116 | 88263 |

## O que mudou no código e funcionou na execução

- Fatos são evidência; o produto final é uma nota por conceito, com mecanismos, variáveis, problemas, decisões e alvos por dificuldade.
- A revisão recebe a nota, os fatos e até oito trechos completos; pode corrigir o texto inteiro. Referências são registradas por seção, não uma verificação automática de cada frase.
- O filtro de conteúdo da Azure ocorreu de fato em uma nota do redator. O item foi registrado e a execução continuou.
- A seleção bilíngue e as cotas por coleção mudaram o material: todas as cinco coleções aparecem nas notas aprovadas. Isso não prova isoladamente qual mudança causou cada ganho.
- Retentativas informam o erro de validação; truncamento aumenta o orçamento de resposta; falhas de itens têm diagnóstico e não encerram automaticamente todos os assuntos.

## Pontos que ainda exigem cuidado

1. Autonomia: q003 pergunta por que os slops e o tanque 6C não esvaziaram, sem trazer o caso ao respondente. O teste mediu dificuldade, não corretude nem autonomia. Os prompts novos foram ajustados para avaliar relações técnicas e fornecer condições suficientes.
2. Avaliação pelo mesmo modelo: 256 das 311 notas finais receberam corrigir, 55 aprovar. O revisor apontou 577 problemas de suporte nos rascunhos; isso é uma contagem de apontamentos, não prova de 577 afirmações removidas nem de corretude total da versão final. As avaliações se concentram em 5 e não servem como ranking externo de qualidade.
3. Alertas numéricos: quatro notas finais têm cinco alertas. Em duas delas, 10 e 100 estão escritos como dez e cem no trecho Petrolês: o alerta é um falso positivo. Os demais valores exigem conferir seus próprios trechos; não classificar todo alerta como alucinação. A rotina também ignora inteiros menores que 10 e não valida automaticamente unidades, versões de normas ou condições.
4. Fontes: várias referências podem vir do mesmo documento. A mediana de nove referências por nota não equivale a nove documentos independentes.
5. Cobertura: 68 assuntos têm notas utilizáveis, mas um conceito foi filtrado. Na próxima saída, processamento_completo distingue material presente de processamento sem itens pulados. Lastro continua preservado.
6. Deduplicação: compara título e resumo por cosseno; conteúdo complementar, condições e contradições ainda dependem de revisão. Não é auditoria factual independente.

7. Defeito de isolamento de evidências encontrado no código: stage_notas construía um mapa global por fid, mas o identificador não inclui o subtópico. Há 157 IDs repetidos entre extrações de subtópicos diferentes. Em 81 notas, 188 referências guardadas têm afirmação diferente da extração local. Como o redator e o revisor também receberam trechos e os registros preservam a evidência efetivamente usada, isso não prova erro técnico em todas essas notas; exige conferência das ligações conceito/fato. O código foi corrigido para consultar um mapa por subtópico, com teste de regressão. A lista de notas está em rastreio_para_curadoria.json. Não foram reescritos os resultados de Lastro.

## Experimento de dificuldade

| Pedido | Resultado medido |
|---|---|
| Fácil (4) | 2 fáceis, 2 médias |
| Média (4) | 1 média, 3 difíceis |
| Difícil A (8) | 6 difíceis, 2 médias |
| Difícil B (8) | 7 difíceis, 1 média |

A amostra tem só 24 questões. Sugere revisar a calibração das fáceis e médias, mas não estabelece desempenho geral. O nível pedido deve ser preservado como metadado; a dificuldade inferida deve passar pela validação da geração final.

## Próxima rodada

Lastro é o tópico já construído. Os quatro escolhidos são Produção e Processo, Operações submarinas, Utilidades e Segurança Operacional: 23 subtópicos no novo script run_mais_4_topicos_azure.sh. Uma execução fará uma varredura lexical para o conjunto. Os resultados de Produção v3 continuam sendo uma execução antiga parcial, e não o primeiro tópico concluído desta rodada v4.
Os ajustes novos de prompt ainda precisam de avaliação com a Azure. A análise atual não faz chamadas ao modelo nem altera os arquivos gerados.

[Exemplos completos de notas e QA](exemplos.md). Comandos: [RODADA_5_TOPICOS.md](../RODADA_5_TOPICOS.md).
