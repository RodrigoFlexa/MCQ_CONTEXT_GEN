# PetroQuest: qualidade do dataset final v2

3813 questões em 40 tópicos, todas com gabarito totalmente sustentado pelo contexto (- de - candidatas). Por fonte: {'v23': 69, 'v23c': 765, 'v22': 11, 'antigo': 285, 'conceitos': 533, 'variada': 655, 'tipo_decisao': 445, 'tipo_diagnostico': 360, 'tipo_procedimento': 690}. Por tipo: {'decisao': 1016, 'diagnostico': 789, 'mecanismo': 561, 'consequencia': 162, 'procedimento': 467, 'conceito': 818}.

## Modelos (resposta de até 20 palavras)

| Modelo | Sem contexto ↓ | Com parcial ↓ | Com contexto ↑ | Gap | F1 | ROUGE-L | BLEU |
|---|---|---|---|---|---|---|---|
| llama-3-1-8b | 15.2% | 26.3% | 42.0% | 26.8 | 10.5 | 10.2 | 1.3 |
| llama-3-3-70b | 24.5% | 37.8% | 50.7% | 26.2 | 13.2 | 13.0 | 1.2 |

F1, ROUGE-L e BLEU (0 a 100) comparam a resposta sem contexto com o gabarito. O veredito do juiz é a métrica principal; as lexicais são complementares. O GPT-5.4 gerou, auditou e julga as questões: fica fora dos estratos e só serve de referência.

## Dataset

| Dimensão | Métrica | Melhor | Faixa de referência | Valor |
|---|---|---|---|---|
| Dificuldade | Difícil para o GPT-5 (inclui muito difícil) | ↑ | > 15% | 100.0% |
| Dificuldade | Nenhum modelo independente acerta | ↑ (com questões boas) | 5–15% | 68.5% |
| Dificuldade | Todos os modelos independentes acertam (fácil) | ↓ | < 40% | 0.0% |
| Não trivialidade | Max ROUGE-L pergunta ↔ frase do contexto | ↓ | 0,15–0,40 | 0.206 |
| Não trivialidade | Bigramas novos no gabarito | ↑ | > 30% | 48.3% |
| Diversidade | Self-BLEU-4 entre perguntas do mesmo tópico | ↓ | < 0,25 | 0.132 |
| Diversidade | Vizinho mais próximo no tópico (cosseno centrado) | ↓ | < 0,50 | 0.486 |
| Forma | Palavras no gabarito | ↓ | 3–15 | 6.2 |
| Cobertura | Decisão + procedimento | ↑ | > 30% | 38.9% |

Difícil para o GPT-5 por tipo: {'conceito': 100.0, 'consequencia': 100.0, 'decisao': 100.0, 'diagnostico': 100.0, 'mecanismo': 100.0, 'procedimento': 100.0}.

Questões por tópico: {'01_01': 81, '02_01': 114, '02_02': 150, '02_03': 95, '02_04': 146, '02_05': 129, '02_06': 89, '02_07': 118, '02_08': 103, '02_09': 112, '02_10': 140, '02_11': 148, '02_12': 100, '03_01': 103, '03_02': 129, '03_03': 95, '04_01': 83, '04_02': 150, '05_01': 108, '05_02': 99, '06_01': 70, '06_02': 66, '06_03': 53, '06_04': 130, '06_05': 62, '06_06': 58, '06_07': 85, '07_01': 120, '07_02': 65, '07_03': 94, '07_04': 127, '07_05': 63, '08_01': 42, '08_02': 42, '08_03': 99, '08_04': 33, '08_05': 118, '09_01': 65, '09_02': 67, '10_01': 62}.

As faixas são referências de trabalho do projeto, não padrões da literatura.
