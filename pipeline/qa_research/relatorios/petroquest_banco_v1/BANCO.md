# Banco PetroQuest v1

3813 questões em 40 tópicos, selecionadas de 4369 questões do dataset final v2 (todas com gabarito totalmente sustentado pelo documento). Revisão de unicidade: 1312 questões revisadas, 84 com veredito corrigido, 0 pendentes. Das 113 que GPT-5 e GPT-5.4 erram mesmo com o documento, 56 ficaram (a pegadinha funcionou e o gabarito é único).

## Poda

| Regra | Motivo | Removidas |
|---|---|---|
| R1 | GPT-5 e GPT-5.4 erram com o documento e a revisão não foi concluída | 0 |
| R2 | o gabarito já está no enunciado (escolha entre opções dadas ou atalho) | 21 |
| R3 | forma "por que X não basta/garante" | 11 |
| R4 | mesmo conhecimento de outra questão do tópico | 7 |
| R5 | revisão: outra resposta também é correta | 400 |
| R6 | revisão: gabarito vago | 2 |
| R7 | revisão: depende do documento | 4 |
| R8 | tópico acima do teto: questão mais redundante do tópico | 111 |

## Composição

Por tipo: {'decisao': 1016, 'conceito': 818, 'diagnostico': 789, 'mecanismo': 561, 'procedimento': 467, 'consequencia': 162}.

Por área: {'Produção e Processo (Medição Fiscal e Sistema de Alívio)': 1444, 'Segurança Operacional, SGSO, Sistemas de Segurança e Gestão de Riscos': 524, 'Manutenção, Inspeção e Integridade de Ativos': 469, 'Segurança Ocupacional, Saúde e Meio Ambiente': 334, 'Sistemas de Lastro, Estabilidade, Ancoragem e Posicionamento, Offloading e Tanques de Carga': 327, 'Operações submarinas, poços, risers e equipamentos submarinos': 233, 'Utilidades, geração de energia e sistemas auxiliares': 207, 'Logística, Suprimentos e Movimentação de Cargas': 132, 'Gestão do Desempenho Empresarial (KPI)': 81, 'Descomissionamento e Gestão do Ciclo de Vida da Unidade': 62}.

Por fonte: {'v23c': 765, 'tipo_procedimento': 690, 'variada': 655, 'conceitos': 533, 'tipo_decisao': 445, 'tipo_diagnostico': 360, 'antigo': 285, 'v23': 69, 'v22': 11}.

Questões por tópico: de 33 a 150 (teto 150; redundância medida por embeddings (cosseno centrado)).

## Modelos (resposta de até 20 palavras)

| Modelo | Sem contexto | Com contexto | Ganho com contexto |
|---|---|---|---|
| GPT-4.1 Mini | 42.0% | 75.3% | 33.3 |
| GPT-4.1 | 53.7% | 83.7% | 30.0 |
| GPT-5 mini | 60.0% | 81.9% | 21.9 |
| GPT-5 | 78.5% | 94.1% | 15.6 |
| GPT-5.4 (referência) | 80.4% | 97.3% | 16.9 |

## Dificuldade e forma

| Métrica | Melhor | Referência | Valor |
|---|---|---|---|
| Difícil para o GPT-5 (inclui muito difícil) | ↑ | > 15% | 21.5% |
| Nenhum modelo independente acerta | ↑ (se forem boas) | 5–15% | 13.1% |
| Fácil (todos os independentes acertam) | ↓ | < 40% | 27.6% |
| Rubrica do especialista: fácil / média / difícil | - | - | 28.7% / 70.0% / 1.3% |
| Max ROUGE-L pergunta ↔ frase do documento | ↓ | 0,15–0,40 | 0.206 |
| Bigramas novos no gabarito | ↑ | > 30% | 48.3% |
| Self-BLEU-4 no tópico | ↓ | < 0,25 | 0.132 |
| Vizinho mais próximo no tópico (cosseno centrado) | ↓ | < 0,50 | 0.486 |
| Palavras no gabarito | ↓ | 3–15 | 6.2 |
| Palavras na pergunta | - | - | 31.0 |
| Perguntas que abrem com "Em um/Num" | ↓ | - | 11.4% |
| Perguntas com cenário | - | - | 70.3% |

Difícil para o GPT-5 por tipo: {'conceito': 17.4, 'consequencia': 18.5, 'decisao': 26.8, 'diagnostico': 19.1, 'mecanismo': 14.1, 'procedimento': 31.0}.

Por tópico: {'01_01': 81, '02_01': 114, '02_02': 150, '02_03': 95, '02_04': 146, '02_05': 129, '02_06': 89, '02_07': 118, '02_08': 103, '02_09': 112, '02_10': 140, '02_11': 148, '02_12': 100, '03_01': 103, '03_02': 129, '03_03': 95, '04_01': 83, '04_02': 150, '05_01': 108, '05_02': 99, '06_01': 70, '06_02': 66, '06_03': 53, '06_04': 130, '06_05': 62, '06_06': 58, '06_07': 85, '07_01': 120, '07_02': 65, '07_03': 94, '07_04': 127, '07_05': 63, '08_01': 42, '08_02': 42, '08_03': 99, '08_04': 33, '08_05': 118, '09_01': 65, '09_02': 67, '10_01': 62}.

Estratos com os 4 modelos independentes (GPT-4.1 Mini, GPT-4.1, GPT-5 mini, GPT-5); o GPT-5.4 gerou as questões e é só referência. As faixas são referências de trabalho do projeto.
