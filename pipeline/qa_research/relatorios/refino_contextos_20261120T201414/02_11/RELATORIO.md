# Refino: 2.11. Tratamento do Gás produzido

**Estado:** parcial

| Medida | Base revisada | Nova versão |
|---|---|---|
| Palavras | 5035 | 11076 |
| Blocos | 30 | 41 |
| Sentenças com quase-duplicata | 2.1% | 5.9% |
| Repetição de 6-gramas | 0.1% | 2.3% |
| Lacunas do especialista | 1/7 atendidas, 2 parciais (14.3%) | 7/7 atendidas, 0 parciais (100.0%) |
| Sentenças com paráfrase em outro bloco (embeddings ≥ 0.85) | 2.1% | 5.4% |

Unidades de conteúdo: 66 ({'evidencia': 61, 'consenso_modelos': 4, 'base_revisada': 1}); 92.4% com evidência nos corpora.
Rascunhos: 566 afirmações fundidas em 66 unidades; descartes {'fora_fpso': 2, 'fora_escopo': 5, 'duplicada': 1}.
Pesquisa: 22 rodadas, 242 passagens lidas, 134 citadas, por coleção {'anp_regulacao': 7, 'petroles': 19, 'evidencias_herdadas': 27, 'hse': 4, 'slb_chemicals': 5, 'abb': 13, 'regis': 17, 'anp': 6, 'offshorenorge': 11, 'emerson': 3, 'mte_nr': 3, 'wikipedia_en': 10, 'bakerhughes': 2, 'bsee': 4, 'kimray': 2, 'imca': 1}.
Revisão: 6 problemas, 6 blocos reparados; alertas locais finais: 0. Chamadas reservadas: 98.
Uso como fonte de questões: sentenças com relação verificável 52% → 52%; sentenças vagas 0% → 0%.
Polimento de estilo: 40 blocos ajustados, 0 removidos, 2 frases de enchimento cortadas; antes {'metatexto': 0, 'travessao': 0, 'siglas_sem_expansao': 3, 'aberturas_dependentes': 0}, depois {'metatexto': 0, 'travessao': 0, 'siglas_sem_expansao': 0, 'aberturas_dependentes': 0}.

## Falhas

- S03: CallFailure: S03_consolidacao: Falha após 2 tentativas: [T1: contract_error (U02: valor numérico sem achado nem bloco revisado; descreva qualitativamente) com 16000 tokens] -> [T2: contract_error (U02: valor numérico sem achado nem bloco revisado; descreva qualitativamente) com 16000 tokens]

Arquivos: documento.md (nova versão), documento_base.md (base revisada), roteiro.json, rascunhos.json,
pesquisa.json, consolidacao_secoes.json, proveniencia.json, consolidacao_documento.json, revisao.json, metricas.json.
