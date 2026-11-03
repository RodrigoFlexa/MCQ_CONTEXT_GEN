# Calibração da deduplicação incremental

Pares rotulados: 150 (50 redundantes). Rótulo: humano onde preenchido; demais: gpt-5-4-petrobras:high.

| Embedding | AUC | limiar automático | limiar do juiz | recall na faixa do juiz | pares que iriam ao juiz |
|---|---|---|---|---|---|
| 3-small | 0.660 | 0.742 | 0.338 | 96% | 123 |
| 3-large | 0.743 | 0.709 | 0.406 | 96% | 106 |

| Juiz | concordância | recall dos redundantes | precisão dos redundantes | n |
|---|---|---|---|---|
| gpt-5-4-nano (gpt-5-4-nano-petrobras:low) | 87% | 96% | 74% | 150 |
| gpt-4-1-mini (gpt-4-1-mini-petrobras) | 85% | 90% | 73% | 150 |
| gpt-5-mini (gpt-5-mini-petrobras:low) | 85% | 98% | 70% | 150 |

**Escolhas:** embedding `3-large`, limiar automático 0.709, limiar do juiz 0.406, juiz `gpt-5-4-petrobras:high`.

Cosseno centrado: subtrai o vetor médio do banco antes do cosseno. A amostra é estratificada por faixa, então recall e AUC valem para a amostra, não para a população de pares.
Para revisar rótulos: preencha `rotulo_humano` (sim/nao) em `pares_rotulados.csv`, salve como `rotulos_humanos.csv` e rode a calibração com `--recalcular` (sem chamadas novas).
