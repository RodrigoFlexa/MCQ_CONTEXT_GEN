# Refino: 2.6. Operação Geral FPSO

**Estado:** parcial

| Medida | Base revisada | Nova versão |
|---|---|---|
| Palavras | 4481 | 6532 |
| Blocos | 30 | 22 |
| Sentenças com quase-duplicata | 0.0% | 0.0% |
| Repetição de 6-gramas | 0.0% | 0.7% |
| Lacunas do especialista | 1/11 atendidas, 8 parciais (9.1%) | 10/11 atendidas, 1 parciais (90.9%) |
| Sentenças com paráfrase em outro bloco (embeddings ≥ 0.85) | 1.1% | 1.5% |

Unidades de conteúdo: 40 ({'evidencia': 38, 'consenso_modelos': 1, 'base_revisada': 1}); 95.0% com evidência nos corpora.
Rascunhos: 328 afirmações fundidas em 40 unidades; descartes {'fora_escopo': 5}.
Pesquisa: 12 rodadas, 151 passagens lidas, 92 citadas, por coleção {'anp': 9, 'slb_chemicals': 1, 'evidencias_herdadas': 17, 'regis': 8, 'imca': 3, 'anp_regulacao': 9, 'hse': 8, 'mte_nr': 3, 'petroles': 9, 'conama': 2, 'bakerhughes': 1, 'abb': 8, 'bsee': 2, 'wikipedia_en': 2, 'kimray': 3, 'offshorenorge': 6, 'dupont': 1}.
Revisão: 5 problemas, 5 blocos reparados; alertas locais finais: 0. Chamadas reservadas: 72.
Uso como fonte de questões: sentenças com relação verificável 38% → 48%; sentenças vagas 0% → 0%.
Polimento de estilo: 21 blocos ajustados, 0 removidos; antes {'metatexto': 0, 'travessao': 0, 'siglas_sem_expansao': 2, 'aberturas_dependentes': 0}, depois {'metatexto': 0, 'travessao': 0, 'siglas_sem_expansao': 0, 'aberturas_dependentes': 0}.

## Falhas

- S02: CallFailure: S02_leitura_2: Falha após 2 tentativas: [T1: contract_error (novas_consultas: par repetido ou sem tradução) com 16000 tokens] -> [T2: contract_error (novas_consultas: consultas de até 16 palavras) com 16000 tokens]
- S07: CallFailure: S07_consolidacao: Falha após 2 tentativas: [T1: contract_error (U04: reescreva sem relato de fonte e com a terminologia de bordo: upset → distúrbio) com 16000 tokens] -> [T2: contract_error (U05: reescreva sem relato de fonte e com a terminologia de bordo: , interromper a fonte, isolar o trecho quando a filosofia do sistema) com 16000 tokens]

Arquivos: documento.md (nova versão), documento_base.md (base revisada), roteiro.json, rascunhos.json,
pesquisa.json, consolidacao_secoes.json, proveniencia.json, consolidacao_documento.json, revisao.json, metricas.json.
