# Revisão do primeiro lote pelo especialista

Pareceres do especialista sobre as 60 questões do formulário (`../formulario_especialista`),
respondidos em 21/10/2026, um formulário por tópico principal.

| Parecer | Qtde | Destino |
|---|---:|---|
| Aprovada | 40 | Repositório definitivo, sem alteração |
| Aprovada com ressalvas | 16 | Editada conforme o parecer e guardada no repositório definitivo; documento de contexto corrigido |
| Reprovada | 4 | Fora do repositório; documento de contexto corrigido |

Reprovadas: Q045 (08_01), Q052 (09_01), Q058 e Q059 (10_01).
Com ressalvas: Q003, Q004 (01_01); Q007, Q009 (02_02); Q014 (03_03); Q023 (04_01); Q027 (05_02);
Q030 (05_01); Q034, Q036 (06_07); Q035 (06_05); Q040 (07_02); Q044 (08_03); Q047 (08_02);
Q050 (09_01); Q057 (10_01).

## Arquivos

- `respostas/` — planilhas exportadas do Google Forms. Ficam só na máquina local (estão no `.gitignore`), porque trazem nome e e-mail do especialista e o repositório é público. Nos arquivos gerados, o avaliador aparece como `especialista_01`.
- `edicoes_questoes.json` — nova redação de cada questão aprovada com ressalvas, com justificativa,
  e observações do especialista sobre questões aprovadas (dificuldade, escopo).
- `edicoes_documentos.json` — trechos alterados nos documentos de contexto (antes/depois), cada um
  ligado às questões e ao comentário que o motivaram.
- `aplicar_revisao.py` — consolida os pareceres e gera as saídas abaixo.
- `pareceres.json` — gerado: parecer, motivos e comentário das 60 questões. É o único lugar onde as
  reprovadas continuam registradas, como origem das correções nos documentos.

Saídas:

- `../repositorio_definitivo/questoes.jsonl` e `.csv` — 56 questões (40 aprovadas + 16 editadas).
- `../relatorios/dez_areas_final_v2/` — 40 documentos; 14 editados, 26 idênticos à v1.
  Registro em `REVISAO_ESPECIALISTA.md` e `revisao_especialista.json`. A v1 não foi alterada.

## Reproduzir

Na raiz do repositório:

```bash
python pipeline/qa_research/revisao_especialista/aplicar_revisao.py
```

O script recria a v2 a partir da v1 e falha se algum trecho "antes" não ocorrer exatamente uma vez,
se o `documento.md` divergir do `documento.json`, se faltar parecer para alguma das 60 questões,
se uma ressalva ficar sem nova redação ou se uma ressalva/reprovação ficar sem correção no documento.

## Pontos para decisão

- O especialista indicou que Q044, Q046 e Q048 (área 08) não são questões de SMS: tratam de
  processo (água produzida, resfriamento). Foram mantidas no tópico de origem, com a observação
  registrada; uma reclassificação para 02_03 e 05_01 fica a critério da equipe.
- Comentários de dificuldade (Q005, Q016, Q017, Q018, Q050) estão registrados, sem reclassificar
  o nível original.
- Para a próxima geração usar os documentos corrigidos, aponte `documents_root` para
  `pipeline/qa_research/relatorios/dez_areas_final_v2`.
