# PetroQuest: qualidade do dataset final

1076 questões em 40 tópicos. Por fonte: {'v23': 263, 'v22': 37, 'antigo': 776}. Por tipo: {'procedimento': 135, 'decisao': 172, 'mecanismo': 295, 'diagnostico': 237, 'consequencia': 65, 'conceito': 172}.

| Dimensão | Métrica | Melhor | Faixa de referência | Valor |
|---|---|---|---|---|
| Validade | Gabaritos totalmente sustentados pelo contexto | ↑ | > 90% | 84.4% |
| Validade | Afirmações do gabarito sustentadas | ↑ | > 95% | 89.9% |
| Dificuldade | GPT-4.1 Nano sem contexto | ↓ | 30–50% | 35.8% |
| Dificuldade | GPT-4.1 Mini sem contexto | ↓ | 45–70% | 58.4% |
| Dificuldade | GPT-4.1 sem contexto | ↓ | 50–75% | 72.6% |
| Dificuldade | GPT-4.1 sem contexto, parcial = 0,5 | ↓ | 60–80% | 81.2% |
| Dificuldade | GPT-5 nano sem contexto | ↓ | 30–60% | 65.2% |
| Dificuldade | GPT-5 mini sem contexto | ↓ | < 80% | 80.4% |
| Dificuldade | GPT-5 sem contexto (modelo forte independente) | ↓ | < 85% | 91.4% |
| Dificuldade | GPT-5.4 sem contexto (gerou as questões; só referência) | – | – | 91.6% |
| Dificuldade | Difícil para o GPT-5 (inclui muito difícil) | ↑ | > 15% | 8.6% |
| Dificuldade | Nenhum modelo independente acerta | ↑ (com questões boas) | 5–15% | 4.0% |
| Contexto | GPT-4.1 com contexto | ↑ | > 90% | 94.9% |
| Contexto | Gap do GPT-4.1 (com − sem contexto) | ↔ moderado | 5–20 pontos | 22.3 pontos |
| Não trivialidade | Max ROUGE-L pergunta ↔ frase do contexto | ↓ | 0,15–0,40 | 0.253 |
| Não trivialidade | Bigramas novos no gabarito | ↑ | > 30% | 51.6% |
| Não trivialidade | Trigramas novos no gabarito | ↑ | > 50% | 70.6% |
| Diversidade | Self-BLEU-4 entre perguntas do mesmo tópico | ↓ | < 0,25 | 0.129 |
| Diversidade | Vizinho mais próximo no tópico (cosseno centrado) | ↓ | < 0,50 | 0.463 |
| Forma | Palavras no gabarito | ↓ | 3–15 | 9.5 |
| Cobertura | Decisão + procedimento | ↑ | > 30% | 28.5% |

As faixas são referências de trabalho do projeto, não padrões da literatura. Acurácia baixa só é virtude quando a questão é válida: leia as linhas de dificuldade junto com a revisão manual.

Questões por tópico: {'01_01': 13, '02_01': 26, '02_02': 195, '02_03': 22, '02_04': 36, '02_05': 23, '02_06': 20, '02_07': 28, '02_08': 26, '02_09': 30, '02_10': 30, '02_11': 38, '02_12': 29, '03_01': 23, '03_02': 36, '03_03': 72, '04_01': 20, '04_02': 37, '05_01': 29, '05_02': 25, '06_01': 11, '06_02': 5, '06_03': 7, '06_04': 14, '06_05': 15, '06_06': 7, '06_07': 5, '07_01': 78, '07_02': 12, '07_03': 14, '07_04': 36, '07_05': 14, '08_01': 5, '08_02': 10, '08_03': 25, '08_04': 6, '08_05': 15, '09_01': 14, '09_02': 11, '10_01': 14}.
