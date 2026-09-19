# Regeneração do tópico 1 — Gestão do Desempenho Empresarial (KPI)

Set/2026. O especialista reescreveu a instrução do tópico 1 no docx
*SUGESTÃO DE FRASES PARA COMPOR PROMPT MÚLTIPLA ESCOLHA V14 (09/09/26)*:

| | antes | agora |
|---|---|---|
| tópico | `Gestão do Desempenho` | `Gestão do Desempenho Empresarial (KPI)` |
| subtópico | `Geral` | `Gestão do Desempenho Empresarial (KPI)` |
| recorte | "aspectos de gestão e desempenho de FPSOs…" | "aspectos de gestão e desempenho **empresarial (KPI)** de FPSOs…" |
| alvo | — | 200 questões |

As 512 questões antigas do tópico foram geradas a partir do texto velho e saem
do dataset.

O subtópico deixou de se chamar `Geral` de propósito: o estado do pipeline é
gravado em `estado/<hash do NOME do subtópico>.json`, e o `Geral` deste tópico
dividia o mesmo arquivo com o `Geral` de *Descomissionamento* — os dois tópicos
escreviam `ids_pool` e `historico_entropia` no mesmo estado (862 ids = 512 + 350).
Com nomes distintos, cada tópico volta a ter estado próprio.

## O que mudou no código

| arquivo | mudança |
|---|---|
| `topicos.py` | tópico 1 renomeado + texto novo do especialista |
| `purgar_topico.py` | **novo** — remove de `saida_fase3/` as questões de um tópico, com backup |
| `pipeline_mcq_fase3_completo.py` | `--topico`, `--max-questoes`; facetas e varredura do corpus continuam cobrindo os 40 subtópicos |
| `utils_fase3.py` | `executar_subtopico(..., max_questoes=N)` — encerra o subtópico ao atingir o alvo |

Por que facetas/varredura seguem cobrindo os 40 subtópicos mesmo gerando um só:
a assinatura de `varrer_corpus` inclui o conjunto de facetas, então varrer só o
tópico 1 sobrescreveria `indices/candidatos.jsonl` com um índice parcial e
obrigaria a revarrer o corpus inteiro na próxima execução dos outros 39.

## Passo a passo no servidor Petrobras

```bash
cd <raiz do repositório>
git pull                      # traz topicos.py, purgar_topico.py e as flags novas
source venv/bin/activate      # venv\Scripts\activate no Windows

# 1) conferir o corpus que o pipeline espera
ls dataset/corpus-SemProcessamento-publico-PetrolesCompleto

# 2) simular a purga (não escreve nada) — esperado: 512 a remover, 15.321 a manter
python pipeline/fase_3/purgar_topico.py --topico "Gestão do Desempenho"

# 3) aplicar (backups .bak_purga_<timestamp> ficam ao lado de cada arquivo)
python pipeline/fase_3/purgar_topico.py --topico "Gestão do Desempenho" --aplicar

# 4) regenerar só o tópico 1, com alvo de 200 questões
python pipeline/fase_3/pipeline_mcq_fase3_completo.py \
    --topico "Gestão do Desempenho Empresarial (KPI)" \
    --max-questoes 200
```

O passo 4 faz, nesta ordem: extrai as facetas novas do tópico 1 (`gpt-5-mini`,
as outras 232 vêm do cache) → **revarre o corpus inteiro** porque o conjunto de
facetas mudou (alguns minutos, é a parte longa) → monta plano de documentos e
codebook só do tópico 1 → gera em rodadas até estagnar a entropia ou bater 200
questões.

`executar_subtopico` roda no máximo 60 rodadas por chamada. Se parar em 60 antes
das 200 questões, **rode o mesmo comando de novo**: o estado é retomável e ele
continua de onde parou (o corpus não é revarrido na segunda vez, a assinatura já
confere).

## Conferência depois

```bash
python - <<'EOF'
import json, collections
c = collections.Counter()
for l in open('pipeline/fase_3/saida_fase3/questoes_fase3.jsonl', encoding='utf-8'):
    d = json.loads(l); c[(d['topico'], d.get('difficulty'))] += 1
for k, v in sorted(c.items()):
    print(v, k)
EOF
```

Esperado: nenhuma linha com `Gestão do Desempenho` (nome antigo) e ~200 com
`Gestão do Desempenho Empresarial (KPI)`.

## Pendências que isto abre

* `pipeline/fase_4/resultados_dificuldade_azure/` avaliou as 512 questões
  antigas. As novas precisam passar pela avaliação de dificuldade da fase 4 se
  ela for usada nas análises seguintes.
* A filtragem da fase 5 (similaridade com o texto do especialista) usa o
  `difficulty` da própria geração, então não depende da fase 4.
