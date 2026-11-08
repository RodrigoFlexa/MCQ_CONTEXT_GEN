# Divisão do banco PetroQuest v1

Treino, validação e teste em 70%, 10%, 20%, por grupo (1240 grupos: mesmo foco de janela ou questões parecidas no mesmo tópico, TF-IDF >= 0.45), estratificada por tópico, tipo, estrato de dificuldade e fonte. Semente 20261107.

| | treino | validacao | teste |
|---|---|---|---|
| Questões | 2664 (69.9%) | 384 (10.1%) | 765 (20.1%) |
| Tipo: conceito | 21.5% | 21.6% | 21.3% |
| Tipo: consequencia | 4.2% | 4.2% | 4.3% |
| Tipo: decisao | 26.7% | 26.6% | 26.7% |
| Tipo: diagnostico | 20.7% | 20.6% | 20.8% |
| Tipo: mecanismo | 14.8% | 14.6% | 14.6% |
| Tipo: procedimento | 12.2% | 12.5% | 12.3% |
| Estrato: dificil | 8.4% | 8.6% | 8.4% |
| Estrato: facil | 27.6% | 27.6% | 27.6% |
| Estrato: media | 51.1% | 50.5% | 50.8% |
| Estrato: muito_dificil | 13.0% | 13.3% | 13.2% |

Tópicos presentes em cada conjunto: treino 40, validacao 40, teste 40; mínimo de questões por tópico: treino 22, validacao 4, teste 7.
