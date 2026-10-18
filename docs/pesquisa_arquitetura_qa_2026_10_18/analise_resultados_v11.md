# Análise dos resultados recebidos da v11

Análise documental em 18/10/2026 do snapshot recebido no commit `ff9a389`, cuja implementação é `72188ba`. Não foram executados testes, geração ou chamadas a modelos. As contagens vêm dos arquivos salvos no servidor, sem reexecutar validadores. O arquivo `metricas_resultados_v11.json` registra as contagens por configuração e etapa.

## Resultado efetivamente disponível

| Configuração | Situação do snapshot | Candidatas | Aprovadas | Rejeitadas tecnicamente | Pendentes por falha operacional |
| --- | --- | ---: | ---: | ---: | ---: |
| direta | Resumo final disponível | 29 | 0 | 0 | 29 |
| nota | Parcial, sem resumo final | 20 | 0 | 0 | 20 |
| nota_complemento | Não recebida | — | — | — | — |

Na direta: SGSO teve 8 candidatas, separadores 12 e tanques 9. Na nota parcial: 8, 6 e 6, respectivamente. Não há evidência de execução do refinador, respondente cego, adjudicador ou avaliador de novidade nos logs recebidos. Não se pode avaliar a eficácia dessas etapas com este snapshot. A ausência de aprovação não significa que 49 questões foram examinadas e reprovadas tecnicamente: nenhuma dessas candidatas completou o julgamento válido.

## 1. Bloqueio operacional comprovado: contrato do juiz

`contracts.validate_judgment` exige exatamente nove chaves em `dimensoes`: `sustentacao`, `correcao_tecnica`, `autonomia`, `competencia`, `condicoes`, `sem_pista`, `escopo`, `jurisdicao` e `integracao`.

O prompt `JUIZ` fornece apenas uma chave no exemplo JSON, seguida de reticências. A explicação usa nomes humanos diferentes das chaves e reúne escopo/jurisdição. As tentativas de reparo recebem a mensagem genérica “inclua todas as dimensões pedidas, sem nota global”, sem as chaves exigidas, recebidas ou ausentes.

Todas as 84 tentativas do juiz na direta falharam nessa checagem. Na nota parcial, foram 57 tentativas com o mesmo erro. São 28 candidatas da direta e 19 da nota; as duas candidatas restantes pararam na resolução independente por referências de suporte inválidas. Os registros não preservam a resposta inválida completa; não é possível afirmar quais chaves específicas cada resposta trouxe.

É um defeito da implementação publicada, que precisa ser corrigido antes de outra execução. A correção não deve relaxar sustentação ou aprovar automaticamente dimensões ausentes. O contrato de saída deve declarar todas as chaves e tipos; o reparo deve informar precisamente o desvio. Uma falha de contrato recorrente deve interromper a execução e a bateria, preservando os artefatos já produzidos.

## 2. Outros desperdícios anteriores ao juiz

Na direta houve 465 tentativas de API: 159 respostas aceitas pelos validadores, 304 falhas de validação e 2 timeouts. Os logs registram 6.601.551 tokens de entrada e saída. Na nota parcial houve 166 tentativas: 52 respostas aceitas e 114 falhas de validação, com 2.553.686 tokens. Total recebido: 631 tentativas e 9.155.237 tokens. Uma resposta estruturalmente aceita não é uma aprovação técnica da questão.

Exemplos de falhas da direta, contando tentativas e incluindo reparos:

- 65 extrações com citação não contígua no original;
- 49 respostas do redator da nota com referências de bloco inválidas ou suporte obrigatório ausente;
- 45 verificações com objeto de suporte contendo citação vazia;
- 17 notas com `condicoes_enunciado` fora do tipo lista;
- 17 verificações com decisão avaliável incompatível com os demais campos;
- 12 verificações com referências de premissas inválidas.

Essas mensagens não permitem concluir que o validador esteja sempre errado ou sempre certo: as respostas inválidas não foram preservadas para auditoria. Precisamos de contratos completos, exemplos válidos para os caminhos sem suporte e erros com campo e IDs permitidos. Não se deve aceitar citação inventada ou remover as condições para reduzir a taxa de falha.

O resultado `fila_esgotada` oculta a causa predominante: na direta, 46 preparações de unidade terminaram em falha operacional. Isso não demonstra esgotamento do conhecimento do corpus. O resumo informa índice com 2.972.589 trechos e cobertura do manifesto e índices configurados; ausência de corpus não explica o bloqueio observado. Essa cobertura também não prova relevância dos trechos recuperados.

## 3. Problema de conteúdo comprovado antes da geração

Na unidade `567fdce5c3:a03:k1`, o foco original era distribuição de carga, priorização e transferência entre tanques, incluindo condicionantes do arranjo e do momento operacional. A evidência principal veio das páginas 62–63 do relatório de investigação do FPSO Cidade de São Mateus.

As afirmações preservam corretamente que se trata daquele arranjo, não de uma regra universal. Porém, o verificador marca as afirmações como avaliáveis por tratarem de um FPSO. A nota então propõe objetivos sobre o roteamento daquele navio e a diferença entre seus tanques 2C a 6C e slops. A revisão aprova esses objetivos. Uma justificativa chega a afirmar que o objetivo exige conhecimento específico do caso e, ainda assim, o considera adequado.

A cadeia demonstra uma confusão entre três decisões distintas:

1. O trecho realmente diz isso?
2. Isso é tecnicamente plausível e se aplica ao sistema em questão?
3. Esse conteúdo permite avaliar conhecimento profissional sem conhecer aquela publicação ou instalação?

A decisão favorável nas duas primeiras não resolve a terceira. A nota também se afasta do foco de distribuição e controle da carga para uma descrição do inventário funcional de um caso. O problema nasce na seleção do conhecimento avaliável e na revisão dos objetivos, antes do gerador de perguntas.

## 4. Exemplos reais das consequências

### Dependência de caso

Na configuração nota, `567fdce5c3:a03:k1:O2:Q` pergunta:

> No arranjo operacional documentado para o FPSO Cidade de São Mateus, qual é a diferença funcional entre os tanques 2C a 6C e os tanques de slop no sistema de movimentação de carga?

O respondente não recebe o arranjo. A pergunta exige conhecer um caso documental particular. Não basta trocar o nome do navio por “um FPSO”: as características locais continuam ocultas.

### Resposta entregue pelo enunciado

Na direta, o mesmo objetivo informa que cinco tanques armazenam produto pronto para exportação e dois slops armazenam água suja antes de tratamento; em seguida pergunta a diferença funcional entre os dois grupos. O núcleo da resposta já está nas premissas. O gerador contornou a dependência do documento fornecendo também a conclusão que deveria avaliar.

### Generalidade e repetição das premissas

Na direta, `d99fb5d8d3:a02:k1:O1:Q` descreve enfraquecimento das responsabilidades, comunicação e recursos e pergunta por que isso compromete o SGSO. O gabarito repete esses efeitos e acrescenta que a prática é estruturante. Há relação com o tema, mas pouca exigência discriminante de conhecimento técnico.

### Condição decisiva pouco clara

Na direta, `4e96c8ab4a:a02:k1:O1:Q` apresenta uma corrente com gás, óleo e água e pede justificar a adequação da separação trifásica. A pergunta já encaminha a decisão e agrega mecanismos e uma etapa adicional. A presença de três fases, por si só, não explicita o objetivo funcional que se deseja para aquele vaso no arranjo de processo. A arquitetura precisa exigir que a escolha esteja sustentada por um critério exposto, sem tratar a conclusão do autor como premissa. Isso é uma crítica ao desenho da questão, não um parecer de especialista sobre todos os detalhes do gabarito.

Esses exemplos demonstram problemas; não constituem uma rotulagem humana integral das 49 candidatas.

## 5. Correções necessárias, em ordem

1. **Contrato e controle de execução.** Declarar campos, tipos e enums completos; tornar reparos acionáveis; preservar saídas inválidas para diagnóstico; parar falhas estruturais recorrentes e propagar a interrupção para as próximas configurações. Não reapresentar falha operacional como rejeição técnica ou escassez de conteúdo.
2. **Conhecimento avaliável.** Distinguir princípio ou relação técnica transferível, fato particular do caso, opinião e obrigação com jurisdição e vigência. Um fato de uma instalação pode ser contexto de cenário; não deve virar gabarito de conhecimento geral apenas por receber `aplicabilidade=fpso`.
3. **Objetivo antes da pergunta.** Exigir demonstração do conhecimento técnico necessário, relação com o foco pretendido, condições decisivas e independência da fonte. Rejeitar objetivos cuja resposta dependa de nomes, listas ou arranjos locais não fornecidos. Verificar se fornecer esses dados acaba entregando a própria resposta.
4. **Liberdade de redação com verificação.** A nota pode organizar, explicar e propor relações com conhecimento paramétrico. Relações técnicas novas que sustentem o gabarito precisam seguir para verificação e, quando necessário, recuperação complementar. Não resolver falta de suporte com mais prosa nem com universalização do caso.
5. **Avaliação pedagógica com evidência.** O revisor deve explicitar o que o profissional precisa saber além do enunciado, qual detalhe local seria necessário e por que o item continua exigindo conhecimento. Isso pode admitir formatos variados de questão, sem um molde rígido de redação. Dimensões preenchidas corretamente não garantem julgamento competente.
6. **Retomada controlada.** Preservar as evidências, unidades e candidatas existentes. Mudanças de código hoje alteram a assinatura da execução e exigem outra pasta; é necessário um caminho explícito e auditável de reaproveitamento antes de indicar comandos para retomar. Não copiar checkpoints antigos indiscriminadamente nem manter decisões antigas após alterar seu critério de validade.

O corpus recuperou material potencialmente útil e o gerador produziu candidatas, mas o pipeline não chegou ao fim e já aprovou objetivos inadequados ao propósito do benchmark. Corrigir somente as nove chaves libera uma etapa quebrada; não demonstra resolução dos problemas de generalidade, dependência de caso ou qualidade da avaliação. O snapshot parcial e os contratos compartilhados também impedem concluir qual das três configurações é superior ou atribuir a falha à capacidade de um modelo específico.
