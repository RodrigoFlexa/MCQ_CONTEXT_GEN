# Refatoração das questões revisadas com os comentários do especialista

A v3 usa todas as MCQs sem reprovação explícita do DOCX revisado. O parecer
técnico participa tanto da conversão quanto da auditoria; as QAs reprovadas
podem ser refatoradas em até três ciclos, sempre com validação independente.

## O que ocorreu na v2

Das 1.000 MCQs revisadas, 446 foram selecionadas por aprovação sem observações.
Dessas, 175 viraram QAs válidas (39,2%) e 271 foram reprovadas. O comentário
humano não era enviado ao modelo e existia apenas uma tentativa de adaptação.

| Critério reprovado entre as 271 | Questões |
|---|---:|
| Univocidade | 235 |
| Resposta sugerida pelo enunciado | 65 |
| Autonomia sem alternativas | 23 |
| Correção técnica | 21 |
| Escopo/catalogação | 19 |
| Forma aberta | 12 |
| Informação sem sustentação | 10 |
| Fidelidade ao gabarito | 1 |

Os critérios se sobrepõem. Não se deve somar essas linhas. Apenas uma
reprovação teve aprovação pelo auditor e falhou exclusivamente nas checagens
de código. A principal dificuldade foi transformar uma escolha entre opções
em uma pergunta aberta com alvo determinado. Muitas decisões descritas como
"melhor ação" admitiam alternativas igualmente defensáveis após retirar A/B/C/D.

O auditor também apontou erros de catalogação que podia corrigir diretamente.
A v3 deixa explícito que o escopo deve ser julgado após a correção do rótulo.
Isso não transforma erros técnicos ou ambiguidades reais em aprovações.

## Seleção ampliada

São **720 candidatas**, com esta distribuição:

- 446 com aprovação simples;
- 270 com aprovação e observações/ressalvas;
- 4 com parecer, mas sem aprovação explícita: entram como candidatas sinalizadas.

As outras 280 têm descarte/reprovação explícita. As questões 25, 86 e 165
contêm ordens de descarte no meio/fim do comentário; elas ficam fora mesmo
quando o parecer começa com "aprovada". As notas que explicam siglas após o
parecer da questão 384 são preservadas como conteúdo de apoio, sem adivinhar
um novo gabarito. Entrada e auditoria estão em entrada/revisadas_v3/.

## Executar no servidor

    git pull --ff-only origin codex/qa-evidencias-verificadas && \
    bash pipeline/qa_research/rodar_especialista_qa.sh \
      --revisadas-v3 \
      --saida pipeline/qa_research/relatorios/especialista_revisadas_v3

Use essa nova pasta para a v3. A v2 e o dataset consolidado anterior são
referências históricas. A retomada usa o mesmo comando e a mesma saída.
O servidor não precisa do DOCX: a seleção completa está versionada em JSONL.

O comando preserva as 175 QAs válidas, seus textos, classificações, respostas
e notas dos dois modelos, verificando a compatibilidade dos protocolos. Assim
há **545 candidatas para adaptar ou recuperar**: as 271 reprovadas da seleção
anterior mais 274 que passaram a ser consideradas. As 623 questões do
documento autoral não fazem parte desta execução.

Para conferir sem API:

    bash pipeline/qa_research/rodar_especialista_qa.sh \
      --revisadas-v3 --saida pipeline/qa_research/relatorios/especialista_revisadas_v3 --plano

## Conversão e refatoração

1. gpt-5-4-petrobras:high recebe original, alternativas, gabarito, parecer,
   notas e, quando existir, a QA anterior com os motivos de reprovação.
2. O modelo pode delimitar um componente da resposta ou aplicar uma correção
   técnica explícita do parecer, registrando alterações e a fonte da resposta.
   Um comentário sem correção suficiente não autoriza inventar um novo fato.
3. Outra chamada faz a auditoria com os mesmos critérios de qualidade. Frases
   tecnicamente equivalentes não são confundidas com respostas diferentes.
4. Se reprovada, a crítica volta ao refinador. O padrão é no máximo três
   candidatas por MCQ. Reprovação após o limite e descarte são decisões finais.

Números, normas, limites e premissas novos sem apoio continuam proibidos.
Comentários que corrigem ou combinam alternativas podem fundamentar uma
resposta revisada; o auditor verifica essa sustentação independentemente.
O conteúdo dos documentos é tratado como dado, nunca como comando do sistema.
Não há metas de aprovação, filtros de similaridade ou deduplicação adicional.
Bloqueios do provedor são terminais e não disparam ciclos de refatoração.

As tentativas ficam em tentativas/<uid>/<ciclo>/, separando conversão e
auditoria. Falha de API na auditoria não refaz uma conversão já salva.
Entrada, fontes, modelos, prompts, código e limite de ciclos entram no
protocolo; alterar esses parâmetros exige outra pasta. O orçamento padrão
é de 20.000 tentativas de API para converter/auditar, com oito trabalhadores.

## Avaliação e datasets

Ao concluir a conversão, o script reaproveita a avaliação compatível das 175
QAs preservadas. GPT-5.4 e Nano respondem somente às novas QAs válidas, em
paralelo. O juiz e os prompts de avaliação permanecem iguais. Respondentes
recebem apenas a pergunta, sem parecer, gabarito ou comentários.

Cada nova QA mantém conjunto_especialista=mcq_revisada_nao_reprovada,
faixa_parecer, revisao_humana, fonte_uid e fluxo_conversao. O rótulo de origem
das 175 preservadas continua o da v2. A avaliação exporta esses campos e
separa as faixas do parecer em acuracia.json. Não se atribui aprovação humana
à QA convertida: a aprovação humana se refere à MCQ e o QA passa pela auditoria.

aprovadas.jsonl conterá as 175 preservadas mais as novas aprovadas. O banco
principal ampliado em bancos/com_contexto_com_especialista.jsonl usa sempre
as 2.818 questões originais como base, evitando adicionar as 175 duas vezes.
A quantidade final e o ganho de aprovação só serão conhecidos após o servidor
rodar. As 720 são candidatas, não uma promessa de 720 QAs válidas.

Ao finalizar, o script mostra a mensagem de conclusão e os comandos de coleta,
commit e push. O histórico de decisões da v2 não é modificado.
