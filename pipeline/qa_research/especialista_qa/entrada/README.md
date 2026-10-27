# Entradas estruturadas dos especialistas

fontes.json é a entrada padrão do pipeline: combina 2.546 MCQs autorais com
446 MCQs revisadas e aprovadas sem observações adicionais, totalizando 2.992.
Os JSONLs já estão no Git e podem ser lidos diretamente no servidor.
Não é preciso transferir os DOCXs.

- questoes_mcq.jsonl: documento autoral, preservado como extraído inicialmente.
- revisadas/aprovadas_mcq.jsonl: somente as 446 selecionadas do novo DOCX.
- revisadas/curadoria.csv: conferência dos pareceres e seleção das 1.000 MCQs.
- revisadas/curadoria_todas.jsonl: conteúdo completo e rastreabilidade das 1.000.
- revisadas/extracao.json: critérios, contagens e SHA-256 do segundo DOCX.

conjunto_especialista diferencia autoral_especialista de mcq_revisada_aprovada
na conversão, na junção e na avaliação. O parecer humano é preservado e não
substitui a validação automática da QA convertida.

## Documento autoral

Origem: DATASET MÚLTIPLA ESCOLHA NOVO AGRUPAMENTO 28 05 26.docx.
Extração determinística do OOXML, sem chamadas de modelo.

| Agrupamento original | Questões |
|---|---:|
| Gestão do Desempenho | 154 |
| Produção e Processo | 685 |
| Lastro estabilidade ancoragem offloading e tanques | 215 |
| Operações Submarinas Poços e Risers | 77 |
| Utilidades Energia e Sistemas Auxiliares | 212 |
| Segurança Operacional e Gestão de Riscos | 431 |
| Manutenção Inspeção e Integridade de Ativos | 286 |
| Segurança Ocupacional Saúde e Meio Ambiente | 347 |
| Logística Suprimentos e Movimentação de Cargas | 70 |
| Descomissionamento e Ciclo de Vida | 69 |
| Total | 2.546 |

As dez contagens conferem com o documento. Nenhuma pendência estrutural foi
encontrada nesta entrada; isso não constitui aprovação técnica das questões.

questoes_mcq.jsonl mantém enunciado, alternativas, gabarito e justificativa,
marcação que sustenta a resposta e intervalo de parágrafos. As letras de
alternativas de listas automáticas são atribuídas pela ordem documentada
dos itens da lista; o método é registrado em cada alternativa.

extracao.json registra contagens, método e hash SHA-256 do DOCX original.
O DOCX e a pasta Downloads não são necessários no servidor.
