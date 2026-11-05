# PetroQuest: qualidade do dataset final v2

3457 questões em 40 tópicos, todas com gabarito totalmente sustentado pelo contexto (3457 de 4942 candidatas). Por fonte: {'v23': 175, 'v23c': 1211, 'v22': 23, 'antigo': 393, 'conceitos': 702, 'variada': 953}. Por tipo: {'procedimento': 306, 'decisao': 653, 'diagnostico': 454, 'mecanismo': 784, 'consequencia': 215, 'conceito': 1045}.

## Modelos (resposta de até 20 palavras)

| Modelo | Sem contexto ↓ | Com parcial ↓ | Com contexto ↑ | Gap | F1 | ROUGE-L | BLEU |
|---|---|---|---|---|---|---|---|
| GPT-4.1 Nano | 25.9% | 39.5% | 48.0% | 22.1 | 11.7 | 11.3 | 1.3 |
| GPT-4.1 Mini | 45.6% | 59.5% | 81.9% | 36.4 | 16.4 | 15.8 | 1.7 |
| GPT-4.1 | 56.4% | 68.6% | 88.6% | 32.2 | 21.9 | 21.2 | 2.7 |
| GPT-5 nano | 45.8% | 57.8% | 77.3% | 31.5 | 17.9 | 17.2 | 2.1 |
| GPT-5 mini | 63.2% | 73.2% | 86.3% | 23.1 | 21.6 | 20.7 | 2.7 |
| GPT-5 | 75.4% | 82.7% | 94.9% | 19.5 | 29.2 | 28.2 | 4.1 |
| GPT-5.4 (referência) | 81.5% | 87.3% | 97.5% | 16.1 | 31.2 | 30.1 | 4.2 |

F1, ROUGE-L e BLEU (0 a 100) comparam a resposta sem contexto com o gabarito. O veredito do juiz é a métrica principal; as lexicais são complementares. O GPT-5.4 gerou, auditou e julga as questões: fica fora dos estratos e só serve de referência.

## Dataset

| Dimensão | Métrica | Melhor | Faixa de referência | Valor |
|---|---|---|---|---|
| Dificuldade | Difícil para o GPT-5 (inclui muito difícil) | ↑ | > 15% | 24.6% |
| Dificuldade | Nenhum modelo independente acerta | ↑ (com questões boas) | 5–15% | 12.3% |
| Dificuldade | Todos os modelos independentes acertam (fácil) | ↓ | < 40% | 13.3% |
| Não trivialidade | Max ROUGE-L pergunta ↔ frase do contexto | ↓ | 0,15–0,40 | 0.232 |
| Não trivialidade | Bigramas novos no gabarito | ↑ | > 30% | 44.3% |
| Diversidade | Self-BLEU-4 entre perguntas do mesmo tópico | ↓ | < 0,25 | 0.142 |
| Diversidade | Vizinho mais próximo no tópico (cosseno centrado) | ↓ | < 0,50 | 0.494 |
| Forma | Palavras no gabarito | ↓ | 3–15 | 6.0 |
| Cobertura | Decisão + procedimento | ↑ | > 30% | 27.7% |

Difícil para o GPT-5 por tipo: {'conceito': 23.2, 'consequencia': 22.3, 'decisao': 30.0, 'diagnostico': 22.2, 'mecanismo': 20.8, 'procedimento': 32.7}.

Questões por tópico: {'01_01': 69, '02_01': 103, '02_02': 215, '02_03': 86, '02_04': 136, '02_05': 108, '02_06': 77, '02_07': 112, '02_08': 97, '02_09': 92, '02_10': 122, '02_11': 119, '02_12': 92, '03_01': 90, '03_02': 107, '03_03': 84, '04_01': 80, '04_02': 150, '05_01': 88, '05_02': 86, '06_01': 60, '06_02': 61, '06_03': 53, '06_04': 115, '06_05': 58, '06_06': 43, '06_07': 80, '07_01': 100, '07_02': 53, '07_03': 82, '07_04': 107, '07_05': 52, '08_01': 34, '08_02': 44, '08_03': 89, '08_04': 28, '08_05': 96, '09_01': 67, '09_02': 60, '10_01': 62}.

As faixas são referências de trabalho do projeto, não padrões da literatura.
