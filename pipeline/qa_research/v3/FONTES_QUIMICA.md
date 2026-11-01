# Complementação profissional para o piloto de produtos químicos

URLs verificadas e coleta/extração testadas em 01/11/2026. São cinco documentos
ou páginas em três coleções. O instalador mantém URL, hash do original, idioma,
fronteira documental e páginas quando fornecidas pelo PDF. Nenhum material de QA
faz parte desta lista. Direitos reservados dos respectivos fabricantes; originais
ficam no corpus local, fora das coletas de resultados para Git.

| Coleção | Documento | Utilidade pretendida | Limite |
|---|---|---|---|
| dupont | [Injection Water Treatment for Oil & Gas](https://www.dupont.com/content/dam/water/amer/us/en/water/public/documents/en/DWS-Oil-Gas-Injection-Water-Br-45-D03549-en.pdf) | Água de injeção e remoção de sulfato em aplicações offshore | Brochura de fabricante; separar mecanismo de alegação comercial |
| dupont | [FilmTec Reverse Osmosis / Nanofiltration Technical Manual](https://www.dupont.com/content/dam/water/amer/us/en/water/public/documents/en/RO-NF-FilmTec-Manual-45-D01504-en.pdf) | Pré-tratamento, compatibilidade, incrustação, limpeza, operação e monitoramento de membranas | Manual de famílias específicas; não aplicar parâmetros de um modelo a toda SRU |
| bakerhughes | [Corrosion inhibition used for a wet gas system treated with MEG](https://dam.bakerhughes.com/m/74838446cbc54945/original/Corrosion-inhibition-used-for-a-wet-gas-system-treated-with-meg-cs.pdf) | Seleção de inibidor compatível com MEG/regeneração e acompanhamento do desempenho | Caso australiano de fabricante; resultados e frequência de aplicação pertencem ao caso |
| slb_chemicals | [Chemical demulsifiers](https://www.slb.com/products-and-services/innovating-in-oil-and-gas/well-production/production-chemicals-and-services/demulsifiers) | Mecanismo de desestabilização de emulsões e critérios de formulação/aplicação | Orientação curta; não substitui qualificação com o fluido e o arranjo reais |
| slb_chemicals | [Microbially induced corrosion management](https://www.slb.com/products-and-services/innovating-in-oil-and-gas/well-production/production-chemicals-and-services/bacteria-management) | Objetivo do biocida, ponto de aplicação, contato, compatibilidade e acompanhamento | Orientação do fornecedor; não é procedimento universal de uma instalação |

## Instalação explícita

```bash
"$DOCUMENT_PYTHON" -m pipeline.qa_research.v2.install_corpora \
  --output dataset/professional_corpora_v2 \
  --sources dupont bakerhughes slb_chemicals \
  --max-documents 3 --max-pages 5 --depth 0
```

Os limites são por coleção; `max-pages` controla URLs visitadas, não o número de
páginas extraídas de cada PDF. O manual é processado integralmente. Profundidade
zero mantém esta coleta nas páginas explícitas e em PDFs permitidos vinculados;
não abre navegação ampla pelos sites. O catálogo restringe hosts e caminhos.
Outras coleções já instaladas são preservadas. Consulte `install_report.json`
para saber quais documentos foram efetivamente obtidos no servidor.

## Verificações realizadas

O download e a normalização dos cinco materiais terminaram sem falhas no teste
local. A busca BM25/RRF recuperou o caso de gás/MEG e os materiais de membranas e
biocidas com consultas específicas. A extração da SLB foi ajustada após detectar
que cartões de artigos relacionados estavam substituindo o corpo técnico.
Um teste de regressão reproduz essa estrutura HTML.

Isso verifica disponibilidade, extração e recuperação. A capacidade de fechar
cada ponto do pedido será julgada na nova geração. Os materiais continuam em
inglês no corpus factual; a síntese e o documento devem ser em português brasileiro.
