# MCQs revisadas pelo especialista

Origem: Questoes_100_por_topico_revisadas.docx, 1.000 questões, 100 por área.
Extração OOXML determinística e offline. O original permanece intacto.

| Situação do parecer humano | Questões | Entra no fluxo? |
|---|---:|---|
| Aprovação explícita sem observações | 446 | Sim |
| Aprovação com observações ou ressalvas | 272 | Não |
| Descarte/reprovação | 277 | Não |
| Parecer indeterminado | 5 | Não |

Critério conservador: conteúdo completo do parecer igual a "aprovada",
"aprovado" ou "aprovar", ignorando caixa, espaços e pontuação final simples.
Não se infere aprovação sem ressalvas a partir de comentários adicionais,
mesmo quando apenas descritivos. Nenhum modelo decide a aprovação humana.
Não há filtro de similaridade nem deduplicação desta entrada.

O extrator reconhece cinco grafias observadas para o rótulo de comentário,
incluindo erros de digitação. Isso recupera quatro aprovações e um descarte;
o teor original é preservado, assim como o bloco original de parágrafos.
A alternativa correta é identificada por negrito em pelo menos 80% do texto
da alternativa, exigindo uma única opção marcada. Todas as 446 selecionadas
têm gabarito único, quatro alternativas e nenhuma pendência de extração.

aprovadas_mcq.jsonl contém as candidatas enviadas ao conversor. Cada registro
tem conjunto_especialista=mcq_revisada_aprovada e UID especialista_revisada:NNNN,
distintos do conjunto autoral. revisao_humana contém o parecer e a seleção;
aprovada no QA final indica a decisão posterior do validador automático.

curadoria_todas.jsonl preserva as 1.000 MCQs, alternativas, gabaritos,
pareceres, tópicos, subtópicos, texto original e parágrafos de origem.
curadoria.csv é a versão resumida para conferência. extracao.json registra
as contagens e o SHA-256 do DOCX. Os dois registros com parágrafos adicionais
não interpretados já estão fora da seleção pelo parecer humano.

O agrupamento e o subtópico originais são preservados sem adaptação à
taxonomia atual. A área KPI não tem subtítulo próprio no corpo do DOCX e
mantém subtopico_original=null; o modelo atribui separadamente um dos 40
subtópicos do programa. O servidor não precisa do DOCX ou do Word.
