# Limite de palavras na resposta: 100 x 20

Amostra estratificada de 301 questões do dataset final, sem contexto. Por tipo: {'diagnostico': 67, 'mecanismo': 83, 'conceito': 47, 'procedimento': 38, 'consequencia': 18, 'decisao': 48}. Por estrato: {'facil': 79, 'media': 196, 'dificil': 26}.

| Modelo | Limite | Acurácia | Com parcial | Parciais | Palavras | Acima do limite | Revocação | F1 | EM | BLEU | ROUGE-L | AUC F1 x juiz |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| gpt-4-1-nano | 100 | 34.2% | 49.8% | 31.2% | 56 | 100.0% | 27.0 | 7.9 | 0.0 | 0.5 | 6.9 | 0.64 |
| gpt-4-1-nano | 20 | 31.9% | 47.3% | 30.9% | 12 | 0.0% | 14.0 | 12.8 | 0.3 | 1.4 | 11.8 | 0.63 |
| gpt-4-1-mini | 100 | 58.0% | 71.0% | 26.0% | 60 | 100.0% | 36.6 | 9.8 | 0.0 | 0.6 | 8.4 | 0.68 |
| gpt-4-1-mini | 20 | 51.5% | 64.0% | 24.9% | 14 | 0.3% | 23.3 | 17.1 | 0.3 | 1.7 | 16.2 | 0.66 |
| gpt-4-1 | 100 | 77.4% | 83.9% | 13.0% | 59 | 100.0% | 41.7 | 10.9 | 0.0 | 0.8 | 9.4 | 0.69 |
| gpt-4-1 | 20 | 65.8% | 76.4% | 21.3% | 13 | 0.3% | 27.0 | 22.4 | 1.7 | 3.0 | 21.0 | 0.66 |
| gpt-5-nano | 100 | 67.1% | 75.7% | 17.3% | 75 | 100.0% | 38.7 | 8.5 | 0.0 | 0.6 | 7.2 | 0.66 |
| gpt-5-nano | 20 | 52.2% | 62.6% | 20.9% | 12 | 0.0% | 22.8 | 19.0 | 1.0 | 2.6 | 18.0 | 0.77 |
| gpt-5-mini | 100 | 81.1% | 87.2% | 12.3% | 72 | 100.0% | 42.5 | 9.2 | 0.0 | 0.5 | 7.7 | 0.79 |
| gpt-5-mini | 20 | 69.8% | 77.2% | 15.0% | 13 | 0.0% | 29.4 | 21.5 | 0.7 | 2.6 | 19.8 | 0.73 |
| gpt-5 | 100 | 91.4% | 94.5% | 6.3% | 74 | 100.0% | 50.8 | 10.3 | 0.0 | 0.8 | 8.7 | 0.49 |
| gpt-5 | 20 | 83.4% | 89.0% | 11.3% | 13 | 0.0% | 35.6 | 26.6 | 1.3 | 4.3 | 24.3 | 0.72 |
| gpt-5-4 | 100 | 91.0% | 94.4% | 6.6% | 76 | 100.0% | 55.9 | 11.5 | 0.0 | 1.0 | 9.6 | 0.65 |
| gpt-5-4 | 20 | 89.4% | 92.9% | 7.0% | 14 | 4.3% | 40.1 | 31.1 | 3.3 | 4.7 | 29.1 | 0.65 |

## Diferença pareada da acurácia (limite curto − 100 palavras)

| Modelo | Pontos | IC 95% |
|---|---|---|
| gpt-4-1-nano | -2.3 | [-8.0; +3.3] |
| gpt-4-1-mini | -6.7 | [-12.0; -1.0] |
| gpt-4-1 | -11.6 | [-16.6; -6.6] |
| gpt-5-nano | -15.0 | [-20.3; -9.6] |
| gpt-5-mini | -11.3 | [-15.9; -6.6] |
| gpt-5 | -8.0 | [-12.0; -4.0] |
| gpt-5-4 | -1.7 | [-4.3; +1.3] |

AUC F1 x juiz: probabilidade de uma resposta julgada correta ter F1 maior que uma julgada incorreta (0,5 = métrica lexical não distingue; 1 = concorda sempre com o juiz). O GPT-5.4 gerou as questões e entra só como referência.
