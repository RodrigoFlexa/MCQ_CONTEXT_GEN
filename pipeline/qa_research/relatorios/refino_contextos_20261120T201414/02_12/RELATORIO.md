# Refino: 2.12. Compressão de Gás

**Estado:** parcial

| Medida | Base revisada | Nova versão |
|---|---|---|
| Palavras | 3903 | 9851 |
| Blocos | 22 | 34 |
| Sentenças com quase-duplicata | 4.5% | 0.6% |
| Repetição de 6-gramas | 1.0% | 0.2% |
| Lacunas do especialista | 0/7 atendidas, 5 parciais (0.0%) | 7/7 atendidas, 0 parciais (100.0%) |
| Sentenças com paráfrase em outro bloco (embeddings ≥ 0.85) | 4.5% | 1.8% |

Unidades de conteúdo: 58 ({'evidencia': 49, 'consenso_modelos': 6, 'base_revisada': 3}); 84.5% com evidência nos corpora.
Rascunhos: 487 afirmações fundidas em 58 unidades; descartes {'fora_escopo': 12, 'irrelevante': 2, 'casuistica': 2, 'duplicada': 3}.
Pesquisa: 22 rodadas, 217 passagens lidas, 104 citadas, por coleção {'evidencias_herdadas': 22, 'hse': 8, 'regis': 12, 'petroles': 14, 'bsee': 3, 'abb': 11, 'wikipedia_en': 5, 'offshorenorge': 12, 'anp': 3, 'anp_regulacao': 6, 'mte_nr': 5, 'emerson': 2, 'imca': 1}.
Revisão: 6 problemas, 6 blocos reparados; alertas locais finais: 0. Chamadas reservadas: 84.
Uso como fonte de questões: sentenças com relação verificável 39% → 51%; sentenças vagas 1% → 0%.
Polimento de estilo: 30 blocos ajustados, 0 removidos, 0 frases de enchimento cortadas; antes {'metatexto': 0, 'travessao': 0, 'siglas_sem_expansao': 4, 'aberturas_dependentes': 0}, depois {'metatexto': 0, 'travessao': 0, 'siglas_sem_expansao': 0, 'aberturas_dependentes': 0}.

## Falhas

- S02_rascunho_sms_integridade: CallFailure: S02_rascunho_sms_integridade: Falha após 1 tentativas: [T1: api_error (filtro de conteúdo) com 16000 tokens]

Arquivos: documento.md (nova versão), documento_base.md (base revisada), roteiro.json, rascunhos.json,
pesquisa.json, consolidacao_secoes.json, proveniencia.json, consolidacao_documento.json, revisao.json, metricas.json.
