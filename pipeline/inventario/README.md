# Inventário de conhecimento do PetroQuest

Transforma as frases do especialista e os cinco corpora (Petrolês, ANP, HSE, BSEE, REGIS) em **notas técnicas
por conceito**, base da geração de QA. Versão atual: **v4**. Leia **[PRODUCAO_V4.md](PRODUCAO_V4.md)** para o
fluxo, a política de erros, os comandos do servidor e o formato da saída.

```text
assuntos → varredura → seleção bilíngue → fatos com citação → conceitos → nota técnica + revisão → combinações → documentos
```

## Módulos

| Arquivo | Papel |
|---|---|
| `run_topico_azure.sh` | rodada de um tópico na Azure (`run_producao_azure.sh` é o atalho de Produção e Processo) |
| `run_inventario.py` | CLI e orquestração; execução por item, ocorrências, disjuntor, retomada |
| `llm.py` | cliente Azure/OpenAI: cache, reparo de validação, truncamento, filtro de conteúdo, diagnóstico |
| `assuntos.py` | frase do especialista → assuntos literais + consultas pt/en |
| `varredura.py` | passada lexical pelos corpora (candidatos por assunto e coleção) |
| `selecao.py` | escolha dos trechos: consulta pt/en, piso de relevância, cota por coleção, MMR |
| `extracao.py` | fatos técnicos com citação literal; descarte por fato, nunca da resposta inteira |
| `consolidacao.py` | plano de conceitos por assunto (agrupa fatos, descarta o que não pertence) |
| `notas.py` | redator de notas técnicas, validação, métricas e deduplicação |
| `revisao.py` | revisor de notas: aprovar, corrigir ou rejeitar, com notas de avaliação |
| `combinacoes.py` | mapa de combinações de notas por subtópico (difíceis tipo B) |
| `teste_dificeis.py` | experimento: gera fácil/média/difícil A/difícil B e mede com o avaliador da fase 4 |
| `fichas.py` | documentos Markdown, cobertura e índice para a geração |
| `modelos.py` | embeddings (Azure, bge-m3 local em GPU, hash para testes) e reranker opcional |

## Testes

```bash
python3 -m unittest discover -s pipeline/inventario/tests -v
```

Sem rede, sem chaves e sem GPU. Histórico das versões anteriores: `PILOTO_AZURE.md`, `PRODUCAO_V3.md`,
`REVISAO_2026_10_12.md` (descrevem a v3, baseada em unidades de uma frase, substituída pela v4).

Execução local com GPU (embeddings bge-m3): `setup_gpu.ps1`, `check_gpu.py` e `requirements.txt`.
