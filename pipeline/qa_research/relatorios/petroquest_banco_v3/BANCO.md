# Banco PetroQuest v3 (PROVISÓRIO)

4427 questões, uma por conhecimento, de 4841 grupos de válidas equivalentes da geração final v3 e dos loops (auditor v23, gabarito de até 20 palavras e totalmente sustentado, deduplicação única). Todas foram avaliadas pelos modelos e revisadas uma a uma; quando o representante de um grupo caiu, o próximo equivalente foi tentado (374 questões do banco são substitutas).

Grupos sem nenhum representante válido: 409. Pendências: 5 sem revisão, 0 reprovadas aguardando o substituto, 0 válidas sem deduplicação. Vereditos corrigidos pela revisão: 221.

## Poda

| Regra | Motivo | Questões |
|---|---|---|
| R2 | o gabarito já está no enunciado | 36 |
| R3 | forma "por que X não basta/garante" | 0 |
| R5 | revisão: outra resposta também é correta | 854 |
| R6 | revisão: gabarito vago | 5 |
| R7 | revisão: depende do documento | 0 |
| R9 | o enunciado precisa do documento | 56 |
| R10 | revisão: trivial (resposta no enunciado ou por bom senso) | 0 |

## Composição

Por tipo: {'procedimento': 1602, 'decisao': 1470, 'diagnostico': 604, 'mecanismo': 388, 'consequencia': 188, 'conceito': 175}.

Por origem: {'retro_sem_memoria': 3680, 'loop_reparo': 747}.

Simples e compostas: {'simples': 4427}. Consertadas (vindas de uma reprovada): 0.

Com evidência rotulada (blocos e trechos que sustentam o gabarito, gabarito de recuperação para avaliar RAG e memória): 4427; com evidência em 2 blocos ou mais: 947.

Por área: {'Produção e Processo (Medição Fiscal e Sistema de Alívio)': 1645, 'Segurança Operacional, SGSO, Sistemas de Segurança e Gestão de Riscos': 574, 'Manutenção, Inspeção e Integridade de Ativos': 475, 'Segurança Ocupacional, Saúde e Meio Ambiente': 449, 'Sistemas de Lastro, Estabilidade, Ancoragem e Posicionamento, Offloading e Tanques de Carga': 364, 'Utilidades, geração de energia e sistemas auxiliares': 333, 'Operações submarinas, poços, risers e equipamentos submarinos': 263, 'Logística, Suprimentos e Movimentação de Cargas': 170, 'Descomissionamento e Gestão do Ciclo de Vida da Unidade': 110, 'Gestão do Desempenho Empresarial (KPI)': 44}.

Por documento: {'01_01': 44, '02_01': 138, '02_02': 160, '02_03': 111, '02_04': 130, '02_05': 117, '02_06': 153, '02_07': 132, '02_08': 127, '02_09': 104, '02_10': 134, '02_11': 184, '02_12': 155, '03_01': 115, '03_02': 115, '03_03': 134, '04_01': 114, '04_02': 149, '05_01': 186, '05_02': 147, '06_01': 95, '06_02': 70, '06_03': 80, '06_04': 95, '06_05': 85, '06_06': 67, '06_07': 82, '07_01': 123, '07_02': 66, '07_03': 104, '07_04': 120, '07_05': 62, '08_01': 75, '08_02': 129, '08_03': 111, '08_04': 41, '08_05': 93, '09_01': 75, '09_02': 95, '10_01': 110}.

## Modelos (resposta de até 20 palavras)

| Modelo | Sem contexto | Com contexto | Ganho com contexto |
|---|---|---|---|
| GPT-4.1 Mini | 41.3% | 82.7% | 41.4 |
| GPT-4.1 | 58.7% | 90.5% | 31.8 |
| GPT-5 mini | 64.0% | 88.6% | 24.6 |
| GPT-5 | 80.1% | 97.7% | 17.6 |
| GPT-5.4 (referência) | 82.2% | 99.2% | 17.0 |

## Dificuldade e forma

Estratos (4 modelos independentes, sem contexto): fácil 29.7%, média 50.3%, difícil 9.1%, muito difícil 10.9%.

Difícil para o GPT-5 por tipo: {'conceito': 16.0, 'consequencia': 21.3, 'decisao': 18.3, 'diagnostico': 12.1, 'mecanismo': 13.9, 'procedimento': 26.2}.

Palavras na pergunta: 32.1; no gabarito: 4.7; perguntas que abrem com "Em um/Num": 4.0%.
