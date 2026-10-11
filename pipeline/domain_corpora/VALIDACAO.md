# Validação — 11/10/2026

## Execuções realizadas

| Verificação | Resultado |
|---|---|
| Testes offline novos | **21 passaram** |
| Sintaxe dos módulos Python | Passou |
| Sintaxe das 19 células do notebook | Passou |
| Instalador com downloads reais | **32 documentos novos**, oito por coleção; sem erros na amostra final |
| Petrolês | Dois TXT mantidos e verificados por SHA-256, total de 969.999.194 bytes |
| Proveniência/integridade da amostra | Passou nas cinco coleções |
| Recuperação lexical com textos reais | Candidatos das cinco coleções, dez por coleção na cota do teste |
| Azure | **Nenhuma chamada** |

No teste de recuperação real, o Petrolês foi limitado explicitamente às primeiras 1.000 linhas de cada arquivo, em cópias temporárias; os originais não foram alterados. Foi um teste de integração lexical, sem gerar QA ou avaliar correção factual pelo modelo.

### Extração da amostra final

| Fonte | Documentos | Unidades textuais aproveitadas | Páginas excluídas por baixo conteúdo textual |
|---|---:|---:|---:|
| ANP | 8 | 311 páginas | 10 |
| HSE | 8 | 392 páginas | 12 |
| BSEE | 8 | 26 páginas | 1 |
| REGIS | 8 | 8 documentos sem paginação | 0 |

Relatórios locais, fora do Git: `dataset/corpora_validation/install_report.json`, `verification_report.json` e `retrieval_smoke_report.json`. A pasta de amostra tem `sample=true`; não deve ser confundida com a instalação completa do servidor.

## Descoberta completa dos catálogos

- ANP: **117 URLs PDF** nas seções configuradas. Cinco anexos ZIP/DOCX ficaram fora do coletor PDF/XML, com registro explícito.
- HSE: **101 URLs PDF**; anexos de outros formatos foram registrados. Não espelha o arquivo histórico do National Archives.
- BSEE: **608 URLs PDF**, percorrendo a paginação real do portal, sem falhas de descoberta nesta execução.
- REGIS: índice do ZIP oficial inspecionado; **21.444 XML de documentos**, total de **4.153.776.597 bytes descomprimidos**; ZIP com **1.311.890.042 bytes**.

As contagens de URLs não são contagens finais de documentos úteis: downloads podem falhar, PDFs podem ser idênticos, páginas podem não ter texto e a auditoria de conteúdo pode rejeitar material. O relatório da instalação completa dará as contagens efetivas.

## Correções encontradas durante os testes

1. REGIS usa XML Solr com `<field name="text">`, não PDFs nem uma tag `<text>` simples. Parser adaptado e testado com documentos reais.
2. Links antigos da ANP permanecem no índice. Os caminhos atuais foram verificados; origem e URL utilizada são preservadas.
3. A paginação BSEE usa `usa-pagination__list/js-pager__items`. O coletor foi adaptado ao HTML real para não ficar apenas na primeira página.
4. PDFs sem texto suficiente ficam em quarentena; falhas de download não são consideradas reprovação factual.
5. A assinatura dos corpora usa conteúdo/hash no modo manifesto: tocar ou reconstruir arquivos idênticos não invalida a retomada pela data de modificação.

## Limites do teste

O ZIP REGIS inteiro não foi baixado/descomprimido localmente; a amostra usou HTTP Range e CRC por membro. O modo completo com MD5 oficial usa o mesmo downloader, testado offline quanto a checksum, interrupção, retomada, cache e corrupção. Não houve execução de geração nem auditoria LLM: a integração com esses papéis foi verificada com respostas simuladas. Não houve validação técnica humana dos documentos ou QA nesta etapa. OCR não está implementado.

## Reproduzir

```bash
python -m unittest discover -s pipeline/domain_corpora/tests -v
python pipeline/domain_corpora/install_corpora.py \
  --petroles-dir dataset/corpus-SemProcessamento-publico-PetrolesHibrido \
  --max-documents-per-source 8 --output dataset/corpora_validation
python pipeline/domain_corpora/verify_corpora.py \
  --manifest dataset/corpora_validation/manifest.json --allow-sample
```

## Atualização: contextos com várias coleções

Na atualização de 11/10/2026, a montagem passou a usar o conjunto de candidatos de todas as coleções por faceta. O mesmo documento pode combinar origens; não há função fixa nem coleção obrigatória. Até dois contextos por faceta, com até seis trechos cada, passam por auditoria conjunta. A auditoria pode autorizar somente parte dos trechos, com as coleções efetivamente mantidas registradas separadamente.

**25 testes passaram**, incluindo montagem com as cinco coleções no mesmo documento, contexto com uma coleção, ausência de candidatos, deduplicação entre corpora, limites de montagem e exclusão de uma coleção pela auditoria. A integração usa embeddings e respostas do auditor simulados; não houve chamadas Azure nem validação factual pelo modelo nesta atualização. O notebook e os prompts foram atualizados e a sintaxe foi verificada. Os testes de downloads anteriores continuam válidos; não foi necessário baixar novamente os corpora.
