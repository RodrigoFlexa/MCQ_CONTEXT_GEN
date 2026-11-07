# PetroQuest: qualidade do dataset final v2

4369 questões em 40 tópicos, todas com gabarito totalmente sustentado pelo contexto (4369 de 7387 candidatas). Por fonte: {'v23': 119, 'v23c': 842, 'v22': 14, 'antigo': 315, 'conceitos': 571, 'variada': 766, 'tipo_decisao': 507, 'tipo_diagnostico': 432, 'tipo_procedimento': 803}. Por tipo: {'procedimento': 542, 'mecanismo': 646, 'decisao': 1166, 'diagnostico': 929, 'consequencia': 178, 'conceito': 908}.

## Modelos (resposta de até 20 palavras)

| Modelo | Sem contexto ↓ | Com parcial ↓ | Com contexto ↑ | Gap | F1 | ROUGE-L | BLEU |
|---|---|---|---|---|---|---|---|
| GPT-4.1 Mini | 40.0% | 54.1% | 73.8% | 33.8 | 14.9 | 14.4 | 1.6 |
| GPT-4.1 | 51.1% | 63.9% | 82.4% | 31.3 | 19.7 | 19.1 | 2.3 |
| GPT-5 mini | 56.9% | 66.9% | 79.5% | 22.6 | 19.2 | 18.4 | 2.4 |
| GPT-5 | 70.3% | 78.5% | 91.8% | 21.5 | 25.9 | 24.8 | 3.6 |
| GPT-5.4 (referência) | 77.1% | 84.1% | 95.6% | 18.5 | 28.4 | 27.2 | 4.1 |

F1, ROUGE-L e BLEU (0 a 100) comparam a resposta sem contexto com o gabarito. O veredito do juiz é a métrica principal; as lexicais são complementares. O GPT-5.4 gerou, auditou e julga as questões: fica fora dos estratos e só serve de referência.

## Dataset

| Dimensão | Métrica | Melhor | Faixa de referência | Valor |
|---|---|---|---|---|
| Dificuldade | Difícil para o GPT-5 (inclui muito difícil) | ↑ | > 15% | 29.7% |
| Dificuldade | Nenhum modelo independente acerta | ↑ (com questões boas) | 5–15% | 17.6% |
| Dificuldade | Todos os modelos independentes acertam (fácil) | ↓ | < 40% | 25.1% |
| Não trivialidade | Max ROUGE-L pergunta ↔ frase do contexto | ↓ | 0,15–0,40 | 0.207 |
| Não trivialidade | Bigramas novos no gabarito | ↑ | > 30% | 48.5% |
| Diversidade | Self-BLEU-4 entre perguntas do mesmo tópico | ↓ | < 0,25 | 0.143 |
| Diversidade | Vizinho mais próximo no tópico (cosseno centrado) | ↓ | < 0,50 | 0.494 |
| Forma | Palavras no gabarito | ↓ | 3–15 | 6.3 |
| Cobertura | Decisão + procedimento | ↑ | > 30% | 39.1% |

Difícil para o GPT-5 por tipo: {'conceito': 24.4, 'consequencia': 23.0, 'decisao': 35.0, 'diagnostico': 29.5, 'mecanismo': 21.1, 'procedimento': 39.7}.

Questões por tópico: {'01_01': 87, '02_01': 124, '02_02': 273, '02_03': 101, '02_04': 164, '02_05': 135, '02_06': 102, '02_07': 134, '02_08': 119, '02_09': 123, '02_10': 160, '02_11': 160, '02_12': 112, '03_01': 120, '03_02': 142, '03_03': 102, '04_01': 91, '04_02': 192, '05_01': 119, '05_02': 102, '06_01': 78, '06_02': 77, '06_03': 63, '06_04': 148, '06_05': 72, '06_06': 63, '06_07': 92, '07_01': 133, '07_02': 70, '07_03': 104, '07_04': 139, '07_05': 71, '08_01': 45, '08_02': 46, '08_03': 115, '08_04': 38, '08_05': 127, '09_01': 77, '09_02': 78, '10_01': 71}.

As faixas são referências de trabalho do projeto, não padrões da literatura.
