# Água do mar para injeção

## 1. Objetivo do condicionamento químico
A água do mar destinada à injeção em reservatórios precisa ser condicionada para reduzir riscos de **tamponamento da formação**, **perda de injetividade**, **corrosão de equipamentos**, **incrustação** e **proliferação microbiológica**. As fontes destacam como causas relevantes de problemas na qualificação da água: matéria orgânica viva, proliferação bacteriológica e traços de petróleo. Também apontam critérios clássicos de aceitação, como: não ser corrosiva, não incrustar nas condições de operação, não carrear sólidos/óleo/emulsão em níveis que plugueiem rapidamente os poços, ter baixo teor de oxigênio dissolvido e ser compatível com a água da jazida. Em termos práticos, o tratamento deve ser pensado como compromisso técnico-econômico entre qualidade requerida, risco ao reservatório e custo operacional do sistema offshore.

**Fontes:** `regis-b478d29fcb19d1d6be3194bc:pNone:176.60-224.0`

## 2. Trem típico de tratamento em FPSO para água do mar de injeção
Um arranjo descrito para sistema de injeção de água em unidade offshore compreende, em sequência geral:

1. **Captação de água do mar** por bombas de elevação;
2. **Injeção de hipoclorito**, gerado em unidade de eletrocloração, para evitar desenvolvimento de microrganismos ainda no início do sistema;
3. **Filtração e tratamento químico**;
4. **Remoção de sulfato (SRU)** para reduzir potencial de incrustação em linhas de injeção e poços;
5. **Desaeração**, com remoção de oxigênio por arraste com gás combustível;
6. **Pós-tratamento químico da água desaerada**, com injeção de sequestrante de oxigênio, biodispersante e biocida;
7. **Bombas de injeção**, que enviam a água tratada aos poços.

Esse encadeamento mostra que o condicionamento químico não é uma ação isolada, mas parte de uma barreira em camadas: controle biológico inicial, remoção de sólidos/espécies causadoras de incrustação, remoção de oxigênio e tratamento químico final antes da injeção.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:388720.0-388754.0`

## 3. Seleção e função da SRU no condicionamento da água do mar
A função central da **Unidade de Remoção de Sulfato (SRU)** é reduzir o teor de sulfato da água do mar antes da injeção, mitigando o risco de incrustação quando essa água entra em contato, no reservatório ou em zonas próximas ao poço, com águas de formação ricas em cátions como **bário** e **estrôncio**. As fontes destacam que a incrustação decorre da precipitação de compostos inorgânicos quando o equilíbrio químico do sistema é perturbado, especialmente por:

- mudança de pressão e/ou temperatura;
- mudança na composição química da água;
- mistura de águas submetidas a condições diferentes.

No contexto offshore brasileiro, a incompatibilidade mais lembrada é a reação do sulfato da água do mar com bário e estrôncio da água conata, produzindo incrustações como sulfato de bário e sulfato de estrôncio. Por isso, a SRU atua como medida preventiva sistêmica: em vez de apenas tentar controlar o crescimento de cristais depois que o risco foi criado, reduz-se a chegada do ânion crítico ao sistema de injeção/reservatório.

As fontes também mostram que, em alguns campos, estudos de compatibilidade água do mar/água de formação indicaram potencial para precipitação de carbonato de cálcio, sulfato de bário, carbonato ferroso, hidróxido férrico, sulfato de estrôncio e sulfato de cálcio, o que levou à recomendação de uso de inibidor de incrustação no tratamento.

Logo, a decisão SRU versus dependência maior de inibidor químico deve considerar pelo menos:

- composição da água do mar captada;
- composição da água da formação/conata;
- tendência de mistura entre águas incompatíveis;
- sensibilidade da formação à perda de injetividade;
- restrições de espaço e arranjo da planta;
- estratégia de mitigação por barreiras múltiplas.

Quando não houver SRU, a literatura citada sugere que o uso de **inibidores de incrustação** ganha relevância, mas isso não elimina a necessidade de estudo de compatibilidade.

**Fontes:** `regis-9f1e60c0f9bdef2ea4d052ec:pNone:2110.0-2360.0`, `regis-b478d29fcb19d1d6be3194bc:pNone:176.60-224.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:844668.0-844719.0`

## 4. Desaeração: objetivo, seleção do método e condicionamento químico complementar
A desaeração é tratada nas fontes como etapa **obrigatória** do tratamento da água de injeção, com objetivo clássico de reduzir o oxigênio dissolvido a níveis muito baixos. Um valor histórico citado é **inferior a 0,05 ppm**. Em textos mais recentes ligados à prática Petrobras, aparecem metas em **ppb**, associadas à prevenção de corrosão e geração de partículas de ferro a jusante dos filtros.

### 4.1 Por que remover oxigênio?
O oxigênio dissolvido é indesejável porque:

- aumenta a corrosividade da água sobre linhas e equipamentos, especialmente em aço carbono;
- favorece geração de produtos de corrosão e partículas de ferro, que podem contaminar a água de injeção e danificar a formação;
- pode elevar custos de manutenção e reduzir disponibilidade do sistema.

### 4.2 Métodos de desaeração citados
As fontes mencionam dois métodos principais:

- **stripping com gás** em contracorrente, apontado como o sistema mecânico mais usado;
- **desaeração a vácuo**.

Critérios de escolha indicados no material:

- **stripping a gás** tende a ser preferido quando há disponibilidade de gás sem componentes ácidos e facilidade para queima/descarga segura, especialmente quando há preocupação com espaço;
- **vácuo** tende a ser preferido quando não há gás disponível e não existe limitação relevante de espaço;
- em certas condições, pode ser atrativa uma solução em dois estágios, com vácuo e auxílio de stripping no segundo estágio.

O material também chama atenção para aspecto operacional importante: em torres a vácuo podem ocorrer **entradas falsas de ar**, comprometendo o desempenho de remoção de oxigênio.

### 4.3 Sequestrante de oxigênio como complemento
A remoção mecânica é complementada por **sequestrante de oxigênio**. Uma das fontes cita o uso disseminado de **bissulfito de sódio (NaHSO3)**, destacando:

- seu emprego como prática comum na indústria de petróleo;
- a necessidade de dosagem em função do oxigênio dissolvido residual;
- vantagem operacional por ser normalmente fornecido em solução aquosa concentrada;
- limitação potencial: em forma diluída, o produto pode ser corrosivo para vários materiais por causa do baixo pH.

O material também relata que redução insuficiente da dosagem de bissulfito eleva o teor de oxigênio dissolvido e, com isso, a taxa de corrosão. Portanto, a dosagem não deve ser tratada como valor fixo: precisa ser ajustada com base em monitoramento do residual de oxigênio e no comportamento corrosivo do sistema.

### 4.4 Implicações de materiais
As fontes indicam que a região de entrada da torre de desaeração pode trabalhar com água ainda bastante aerada, exigindo metalurgia mais resistente à corrosão; já a jusante da desaeração, com baixos teores de oxigênio, torna-se viável o emprego de aço carbono em mais partes do sistema. Isso reforça que o desempenho químico da desaeração influencia diretamente a seleção de materiais.

**Fontes:** `regis-b478d29fcb19d1d6be3194bc:pNone:176.60-224.0`, `regis-2abff12c300b2f0d5a6ea665:pNone:58.60-100.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:4453849.0-4453883.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:388720.0-388754.0`

## 5. Controle microbiológico e interação com a desaeração
O condicionamento microbiológico da água do mar aparece em dois momentos distintos do processo:

### 5.1 Controle inicial na captação
A cloração/hipoclorito tem uso generalizado para controlar matéria orgânica microscópica e evitar desenvolvimento de microrganismos. Além disso, telas na captação retêm organismos macroscópicos.

### 5.2 Controle após desaeração
Há um ponto técnico importante nas fontes: ao eliminar oxigênio dissolvido, cria-se ambiente mais favorável à proliferação de bactérias anaeróbias, inclusive **bactérias sulfato-redutoras**, que podem causar corrosão e gerar sulfetos/particulados que também prejudicam o sistema e a formação. Por isso, o tratamento da água de injeção exige **esterilização química** ou uso de **biocidas**, mesmo quando a água já foi desaerada.

No arranjo de processo citado para FPSO, a água desaerada recebe **sequestrante de oxigênio, biodispersante e biocida** antes da injeção. O biodispersante ajuda a combater formação de limo/biofilme e a manter material biológico disperso, reduzindo incrustação orgânica e fouling microbiológico.

### 5.3 Interferência do cloro residual
Uma observação operacional valiosa é que o **cloro residual** na entrada da torre de desaeração deve ser acompanhado:

- se for insuficiente, o controle microbiológico fica deficiente;
- se for excessivo, ele pode **competir** com bissulfito ou sulfito na reação química de remoção de oxigênio, prejudicando a eficiência do sequestrante.

Isso mostra que a sequência de dosagem e o residual remanescente de oxidantes importam tanto quanto a escolha do produto.

**Fontes:** `regis-b478d29fcb19d1d6be3194bc:pNone:176.60-224.0`, `regis-2abff12c300b2f0d5a6ea665:pNone:58.60-100.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:388720.0-388754.0`

## 6. Dosagem, armazenamento e manuseio dos químicos
As fontes desta faceta trazem pouca dosagem numérica confiável, mas descrevem filosofia de sistema de injeção química relevante para FPSOs:

- **tanques dedicados por produto químico**;
- **bombas dedicadas** para cada produto;
- dispositivos de dosagem/controle, como coluna de calibração, amortecedor de pulsação, recirculação/alívio interno e ajuste de vazão;
- filosofia de estocagem que permita **manutenção sem interromper a operação**;
- em uma unidade descrita, parte dos produtos é transferida por **gravidade** de contêineres/tambores na estação de enchimento para os tanques de químicos.

Embora o exemplo detalhado de skid químico esteja inserido numa unidade mais ampla de injeção química de óleo e gás, essa filosofia é útil para o condicionamento da água do mar porque atende a três necessidades típicas do serviço offshore:

1. **segregação por produto**, reduzindo risco de contaminação cruzada;
2. **controle de vazão**, essencial para ajuste fino do tratamento;
3. **continuidade operacional**, crítica em sistemas de injeção que devem acompanhar a produção ao longo dos anos.

Para químicos da água de injeção, a definição de dose deve ser baseada em ensaios, residual medido e desempenho do sistema, e não em dose fixa transplantada entre ativos. Isso vale especialmente para hipoclorito, biocida, sequestrante de oxigênio e inibidor de incrustação.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:388755.0-388789.0`

## 7. Monitoramento de desempenho do tratamento
O desempenho do condicionamento químico e físico da água de injeção deve ser acompanhado por parâmetros de qualidade da água e por indicadores indiretos de dano ao sistema.

### 7.1 Parâmetros analíticos citados nas fontes
- **Oxigênio dissolvido (TOD)**: monitoramento contínuo com oxymeter de eletrodo de ouro; verificação periódica por método úmido com Rodazina D.
- **Turbidez**: monitoramento contínuo por método óptico.
- **Sólidos totais em suspensão (STS)**: filtração em membrana de 0,45 µm, periodicamente e sempre que houver suspeita de mudança na qualidade.
- **Ferro total**: algumas instalações controlam para avaliar contaminação por corrosão.
- **Razão de corrosão e pitting factor**: monitoramento contínuo por eletrodos energizados.
- **Cloro residual**: útil na entrada das torres de desaeração, pelo efeito sobre controle biológico e sobre o consumo do sequestrante.

### 7.2 Parâmetros de qualificação da água para injeção
Em exemplo de campo citado, o acompanhamento da qualidade da água incluiu:

- teor de sólidos em suspensão;
- fator de filtrabilidade;
- distribuição de partículas.

Outro trecho destaca especificações Petrobras por campo produtor para sólidos suspensos, número de partículas acima de certos diâmetros e teor de oxigênio dissolvido em ppb, associando diretamente esses parâmetros ao risco de entupimento e geração de partículas de ferro.

### 7.3 Lições operacionais
As fontes mostram um ponto frequentemente negligenciado: **a confiabilidade da instrumentação e do método analítico é parte do controle de desempenho**. Em um caso relatado, resultados de distribuição de partículas divergentes foram posteriormente desconsiderados porque o contador de partículas estava descalibrado.

**Fontes:** `regis-2abff12c300b2f0d5a6ea665:pNone:58.60-100.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:844668.0-844719.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:4453849.0-4453883.0`

## 8. Exemplo de evolução de sistema de tratamento
Um caso de campo descrito nas fontes ajuda a entender decisões de seleção de tratamento:

- **Sistema antecipado**: captação de água do mar, filtragem grosseira, dosagem de eliminador de oxigênio, inibidor de incrustação e biocida orgânico, filtragem fina por cartucho e bombeamento para injeção.
- **Sistema definitivo**: passou a incluir **filtros de areia** antes do filtro de cartucho e **torre de desaeração** para eliminar oxigênio dissolvido.

A mudança sugere amadurecimento do projeto em duas frentes:

1. reforço do controle de **sólidos**;
2. reforço do controle de **oxigênio dissolvido**.

No mesmo caso, foram feitos estudos de distribuição de partículas, compatibilidade entre água do mar e água de formação e sensibilidade da formação à água de injeção. Isso ilustra um princípio importante: a seleção de produtos químicos e equipamentos de tratamento deve ser sustentada por **testes específicos do ativo**, e não apenas por prática genérica de mercado.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:844668.0-844719.0`

## 9. Síntese técnica para tomada de decisão
Para esta faceta, o condicionamento químico da água do mar para injeção em FPSO pode ser resumido assim:

- **Hipoclorito/cloração**: controla biofouling na captação e no início do sistema.
- **SRU**: reduz risco de incrustação por sulfato em contato com águas de formação incompatíveis.
- **Desaeração**: reduz oxigênio dissolvido para limitar corrosão e formação de partículas de ferro.
- **Sequestrante de oxigênio**: completa a remoção de O2 residual após a etapa mecânica.
- **Biocida e biodispersante**: combatem o risco microbiológico remanescente, especialmente após criação de ambiente anaeróbio.
- **Monitoramento**: deve fechar o ciclo entre dosagem, residual, corrosão, sólidos, partículas e compatibilidade.

A seleção correta depende de compatibilidade água do mar/água da formação, sensibilidade do reservatório, disponibilidade de gás para stripping, restrições de espaço, metalurgia, confiabilidade analítica e estratégia de operação contínua da planta.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:388720.0-388754.0`, `regis-b478d29fcb19d1d6be3194bc:pNone:176.60-224.0`, `regis-2abff12c300b2f0d5a6ea665:pNone:58.60-100.0`, `regis-9f1e60c0f9bdef2ea4d052ec:pNone:2110.0-2360.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:4453849.0-4453883.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:844668.0-844719.0`