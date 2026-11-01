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

## Procedimento

1. Planejar seções e pontos ancorados na frase integral. Gerar consultas PT/EN
   específicas sobre mecanismos, condições e decisões, sem inventar subtópicos.
2. Recuperar candidatas nas coleções, excluir navegação/extrações anormais e ler
   a pertinência das passagens integrais. Distinguir evidência direta, apoio
   conceitual e coincidência de termos; registrar aplicabilidade e limites.
3. Se houver lacuna e consulta útil, fazer uma busca complementar. Sem passagem
   nova, parar a pesquisa da seção. Se não houver evidência direta, registrar
   pendência e não escrever uma seção apenas com conhecimento genérico do modelo.
4. Escrever a seção com explicações causais, condições, critérios e consequências.
   Complementos conceituais e lacunas são auxiliares. Dados, limites, dosagens e
   obrigações normativas exigem suporte. Documento estrangeiro não cria obrigação
   brasileira; documento sobre um equipamento não sustenta outro por analogia.
5. Revisar o conjunto quanto a suporte, aplicabilidade, profundidade, cobertura,
   coerência e PT-BR. Mencionar um termo não equivale a ensinar o ponto solicitado.
6. Corrigir apenas seções com problemas, uma vez; pesquisar novamente somente se
   o parecer indicar consultas. Reavaliar. Preservar seções boas e registrar
   pendências, sem ciclo indefinido de pesquisa ou reescrita.

A correção pode acrescentar uma busca dirigida, além das duas buscas máximas da
pesquisa inicial. Seleção usa o modelo de redação; revisão mantém seu modelo
próprio. Não há novo catálogo de modelos ou nova biblioteca de orquestração.
Falhas de transporte continuam com até duas tentativas por chamada lógica e o
orçamento cumulativo já existente. Essas tentativas não são rodadas de pesquisa.

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
