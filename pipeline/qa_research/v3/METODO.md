# Pesquisa e escrita técnica: adaptação mínima de métodos estabelecidos

## Problema observado no piloto

O piloto coletado em `piloto_fluxo_v3_02_02_20261101T024133` liberou três de seis
seções. Um título de feed IMCA tinha 130.277 caracteres; repetido em passagens,
excedeu o limite de entrada. A revisão também identificou transferência indevida
de recomendações de abastecimento de aeronave para tanques de produtos químicos.
Havia texto útil, mas cobertura incompleta e narrativa sobre referências no corpo.
O erro de autoria de QA ocorreu depois; a prioridade desta revisão é o documento.

## O que aproveitamos da literatura

- **STORM (Shao et al., NAACL 2024):** pesquisa prévia orientada por perguntas e
  organização do conteúdo antes da escrita de textos extensos. Adotamos consultas
  técnicas específicas por seção, sempre subordinadas à frase do especialista.
  Não reproduzimos as conversas simuladas entre múltiplos personagens do sistema.
  [Artigo original](https://aclanthology.org/2024.naacl-long.347/).
- **Reciprocal Rank Fusion (Cormack, Clarke e Büttcher, SIGIR 2009):** combinação
  de listas ordenadas de recuperação. Reutilizamos a implementação já existente
  de BM25 e RRF com constante 60 nas consultas PT/EN. Uma oportunidade inicial
  para cada coleção amplia a lista de candidatas; pertinência decide a seleção
  final, sem cotas obrigatórias de fontes na redação.
  [Artigo original](https://cormack.uwaterloo.ca/cormacksigir09-rrf.pdf).
- **Corrective RAG (Yan et al., 2024):** avaliar a qualidade da recuperação e
  corrigir a busca quando necessário. Adotamos uma seleção de pertinência antes
  da escrita e uma única busca complementar dirigida às lacunas.
  Não reproduzimos seu avaliador treinado, seus experimentos ou busca web automática.
  [Artigo original](https://arxiv.org/abs/2401.15884).

É uma adaptação de princípios, não uma reprodução experimental desses trabalhos.
Os resultados publicados não demonstram a qualidade deste pipeline em óleo e gás.
A busca do pipeline continua nos corpus locais instalados; esta alteração não
instala um serviço de pesquisa na internet nem amplia silenciosamente o acervo.

## Aprendizado do segundo piloto

A coleta `piloto_fluxo_v3_02_02_20261101T041303` produziu seis rascunhos corrigidos,
mas a regra “qualquer lacuna rejeita a seção” descartou todos. O parecer indicava
conteúdo útil e dez pontos atendidos/dez parciais. A regra estava incorreta para
esse objetivo: qualidade do conteúdo e completude do escopo são decisões distintas.
Também houve falso positivo editorial no uso físico de “o trecho realmente protegido”.

## Procedimento atual

1. Planejar seções e pontos ancorados na frase integral. Gerar expressões técnicas
   PT/EN curtas (preferência 3–12, máximo 16 palavras), com uma necessidade por
   consulta. Descrições não ampliam o pedido com dados quantitativos universais.
2. Recuperar e selecionar até 12 candidatas por seção. A seleção retorna somente
   as úteis (até oito e até duas de apoio), com pontos sustentados e aplicabilidade.
   Não pede justificativa para cada rejeição nem propõe novas consultas.
3. Escrever a seção, explicando mecanismos, condições, critérios e consequências.
   As fontes devem sustentar diretamente parte do conteúdo. Complementos e limites
   ficam nos auxiliares. Sem evidência direta, registrar pendência.
4. Revisar o conjunto separando: (a) erros técnicos/editoriais que exigem reparo;
   (b) lacunas essenciais que tornam pontos parciais/ausentes; (c) limites opcionais
   que não rejeitam conteúdo correto. Uma seção liberada pode ter cobertura parcial.
5. Somente lacunas essenciais com consultas úteis motivam uma busca complementar.
   Avaliar apenas passagens inéditas. Sem suporte direto novo, manter o texto
   aprovado e registrar pendência; não repetir a escrita.
6. Corrigir erros/editorial uma vez; completar lacunas somente quando há evidência
   nova. Preservar as evidências anteriores e o texto correto. Se houver alteração,
   revisar o conjunto novamente. Uma correção técnica que falha não libera o erro;
   uma tentativa de ampliar cobertura que falha preserva a versão já aprovada.

Há uma pesquisa inicial e, no máximo, uma complementação por seção, após a revisão.
Não existe expansão adicional na seleção nem uma terceira pesquisa durante a
correção. Seleção usa o modelo de redação. Falhas de transporte continuam com até
duas tentativas por chamada lógica; isso não é rodada adicional de pesquisa.

O corpus recebeu fontes profissionais direcionadas, documentadas em
[FONTES_QUIMICA.md](FONTES_QUIMICA.md). São orientações de fabricante, manual e caso
operacional, com limites de aplicabilidade. Não são evidência universal para FPSOs,
nem fornecem normas brasileiras por inferência. A instalação é explícita e mantém
separados os corpus factuais e os datasets de questões.

## Parada e passagem para questões

A execução padrão é `--stage context`: termina no documento para avaliação.
Uma versão só se torna elegível a QA com todas as seções liberadas, todos os
pontos atendidos, nenhuma omissão de escopo e revisão sob o critério atual.
Revisões antigas não são promovidas automaticamente. Mesmo a opção explícita
`--stage all` respeita a barreira. `--stage qa` não reescreve o documento.

O corpus pode continuar insuficiente. Nesse caso o resultado correto é parcial,
com indicação do que falta pesquisar. A aprovação automática não substitui a
avaliação do especialista. O novo piloto deve comparar profundidade, cobertura,
aplicabilidade, autonomia do texto e tempo/custo com a versão anterior antes de
avaliar quantidade ou qualidade de questões.

Nesta alteração, o gerador de questões mantém seu algoritmo e suas seis classes.
O problema de rejeição de lote por fundamento literal não foi tratado aqui; a QA
fica para a etapa seguinte, depois de o documento ser considerado adequado.
Nenhum dataset externo de questões foi baixado ou alterado.
