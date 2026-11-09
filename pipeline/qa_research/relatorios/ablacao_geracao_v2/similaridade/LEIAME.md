# Similaridade e diversidade das perguntas da ablação

Gerado por `python -m pipeline.qa_research.experimento_ab.similaridade_ablacao`.

Conjuntos: as 1000 perguntas geradas de cada braço (coluna `aceita` = passou no auditor, na resposta de até 20 palavras,
na sustentação e no dedup) e as 1000 do banco final nas mesmas vagas (`banco`). Só a pergunta entra nas similaridades.

Representações (cosseno): `tfidf` = TF-IDF de palavras, uni e bigramas, todas as palavras, ajustado em todos os
conjuntos juntos; `char` = TF-IDF de n-gramas de caracteres 3 a 5; `e5` = embedding `intfloat/multilingual-e5-base` (local, prefixo
"query: "; vetores em `embeddings_e5.npz`, float16). Os embeddings 3-large do dedup não estão no repositório.

## Arquivos

- `questoes.csv`: uma linha por pergunta.
  - `nn_<rep>_conjunto`: similaridade com a pergunta mais parecida do mesmo conjunto (qualquer tópico);
    `nn_<rep>_uid` diz qual é.
  - `nn_<rep>_topico` / `media_<rep>_topico`: a mais parecida e a média, só entre as do mesmo tópico.
    `nn_e5_topico_pergunta` traz o texto da mais parecida.
  - `dens10_<rep>_conjunto`: densidade local = média das 10 maiores similaridades no conjunto.
  - `nn_<rep>_banco`: a mais parecida entre as 1000 do banco (vazia para o próprio banco).
  - `self_bleu_topico`: BLEU-4 (suavizado) da pergunta contra as outras do mesmo conjunto e tópico.
- `pares_mesmo_topico.csv.gz`: todos os pares do mesmo tópico dentro de cada conjunto: cossenos nas três
  representações, Jaccard das palavras de conteúdo e BLEU-4 simétrico (média dos dois sentidos).
- `pares_amostra.csv.gz`: 5000 pares sorteados por conjunto, de qualquer tópico (`mesmo_topico` marca).
- `pares_distribuicao.csv`: TODOS os 499.500 pares de cada conjunto: média, desvio, quantis e histograma
  (bordas de -0,2 a 1,0 em passos de 0,01, em JSON).
- `entre_configuracoes.csv`: para cada pergunta do conjunto A, a similaridade com a mais parecida do conjunto B
  no mesmo tópico (`nn_<rep>_topico`) e em qualquer tópico (`nn_<rep>_geral`).
- `entre_configuracoes_resumo.csv`: por par (A, B) e representação: média e mediana do vizinho no tópico, média do
  vizinho geral, cosseno médio dos pares do mesmo tópico e cosseno entre os centroides.
- `diversidade.csv`: por conjunto, para as geradas e as aceitas: TTR, TTR rarefeito (mesmo número de tokens para
  todos: o menor conjunto), Guiraud, Herdan, MATTR (janelas 50 e 100), MTLD, HD-D, Yule K, entropia de unigramas,
  Distinct-1/2/3, vocabulário de conteúdo, taxa de compressão gzip, Self-BLEU (conjunto, até 300 perguntas
  sorteadas, e por tópico), cosseno médio e vizinho mais próximo médio (conjunto e tópico) e Vendi (E5).
- `diversidade_por_topico.csv`: as mesmas métricas por conjunto e tópico (geradas).
- `figuras/`: figS1 (vizinho mais próximo no tópico, E5 e TF-IDF), figS2 (pares do mesmo tópico, E5),
  figS3 (Self-BLEU), figS4 (matriz entre configurações, E5).

## Leitura

Similaridade maior = perguntas mais parecidas = menos diversidade. Self-BLEU, cosseno médio, vizinho mais próximo,
Yule K e compressão: menor = mais variado. TTR, MATTR, MTLD, HD-D, entropia, Distinct e Vendi: maior = mais variado.
TTR bruto depende do tamanho do texto: compare o rarefeito, MATTR, MTLD ou HD-D. Naive e regras têm poucas aceitas
(23 e 31): as métricas das aceitas desses braços são frágeis.
