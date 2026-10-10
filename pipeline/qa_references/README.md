# Fontes QA para exemplos de formato

Este conjunto serve para exemplificar **como uma pergunta e sua resposta podem ser escritas**. Não fornece fatos para questões de óleo e gás, não valida respostas do PetroQuest e não deve ser usado para imitar cenários técnicos das fontes.

## Fontes incluídas

| Identificador | Fonte e papel no prompt | Idioma | Licença indicada pela fonte |
|---|---|---|---|
| `pira_ptbr` | Pirá: perguntas e respostas em português sobre oceano, costa brasileira e clima; a fonte tem curadoria humana e avaliações. É a referência prioritária para forma em português, mas não é uma fonte geral de operação de FPSO. | PT/EN | CC BY 4.0 |
| `arc_challenge` | ARC-Challenge: perguntas de ciências com raciocínio; a exportação mantém apenas pergunta e alternativa correta convertida em resposta. | EN | CC BY-SA 4.0 |
| `arc_easy` | ARC-Easy: estrutura direta de QA em ciências, com alternativas removidas. | EN | CC BY-SA 4.0 |
| `squad_v2` | SQuAD 2.0: perguntas de compreensão de texto com respostas curtas; respostas sem gabarito são removidas e referências explícitas ao texto/passage são filtradas. | EN | CC BY-SA 4.0 |
| `hotpotqa` | HotpotQA: exemplos de perguntas de comparação e raciocínio em múltiplos passos. Contextos e fatos de apoio não são exportados. | EN | CC BY-SA 4.0 |
| `boolq` | BoolQ: formato de pergunta direta de sim/não; o passage de apoio é descartado. | EN | CC BY-SA 3.0 |

O ARC é de múltipla escolha na origem. O normalizador usa a chave correta para obter o texto da resposta e descarta completamente o campo de alternativas. Além disso, remove enunciados que explicitamente peçam “uma das alternativas”, “qual das seguintes” ou seleção de opção. Nenhum passage, conjunto de choices, explicação ou texto de suporte sai no JSONL.

SciQ não entra por padrão: a ficha consultada indica CC BY-NC 3.0, condição que pode conflitar com reutilização fora de pesquisa não comercial. OpenBookQA também fica fora até haver confirmação clara da licença dos dados na fonte original. Evitamos ainda bases grandes ou com licença/proveniência incerta quando há opções menores e rastreáveis.

## Baixar exemplos

O script usa a API pública do Dataset Viewer do Hugging Face, sem instalação adicional:

```powershell
python pipeline/qa_references/download_qa_examples.py
```

Por padrão, busca até 500 itens brutos por fonte, com páginas amostradas de forma determinística, e salva apenas QA normalizado em `pipeline/qa_references/data/qa_examples.jsonl`. Para selecionar fontes ou alterar o volume:

```powershell
python pipeline/qa_references/download_qa_examples.py --only pira_ptbr arc_challenge arc_easy --max-per-dataset 1000
```

Para solicitar todos os registros disponíveis em cada split configurado:

```powershell
python pipeline/qa_references/download_qa_examples.py --max-per-dataset 0
```

O arquivo gerado tem uma linha JSON por exemplo, com `question`, `answer`, `source_dataset`, `source_url`, `source_license`, `source_language`, `source_split` e `example_role`. A aplicação deve passar ao modelo somente `question` e `answer`; proveniência fica para auditoria e atribuição. Deduplicação e seleção do lote few-shot devem acontecer depois do download, com amostragem por variedade de forma e dificuldade.

Os registros CC BY-SA permanecem identificados por origem e licença. Se qualquer parte transformada for distribuída, revisar as obrigações de atribuição e compartilhamento pela mesma licença. O uso como exemplos internos também deve manter a proveniência no conjunto de dados local.

## Classificar a revisão do especialista

```powershell
python pipeline/qa_references/extrair_pareceres_especialista.py
```

O extrator gera:

- `pipeline/qa_references/review/resumo_curadoria.md`: contagens e regra de triagem;
- `pipeline/qa_references/review/questoes_revisadas_classificadas.csv`: tabela completa para revisão humana;
- `pipeline/qa_references/review/questoes_revisadas_classificadas.jsonl`: extração estruturada, incluindo pareceres e ressalvas;
- `pipeline/qa_references/review/sementes_qa_candidatas.jsonl`: somente pergunta e resposta para aprovações sem ressalvas detectadas.

A classificação automática é intencionalmente conservadora. “Aprovada com ressalvas”, qualquer sinal de repetição, dúvida técnica ou de escopo, e parecer ausente ficam fora da lista automática de seeds. Observações apenas sobre distratores não bloqueiam uma semente QA, pois as alternativas não são exportadas. A triagem precisa ser confirmada por leitura humana, sobretudo para identificar as duas questões envolvidas quando o comentário diz “repetida” ou “questão anterior”.

O fluxo QA completo em [`../fase_4/README.md`](../fase_4/README.md) integra essas candidatas com as vencedoras da avaliação humana da fase 2 e novas questões de nota alta do Judge. Os fatos são recuperados do corpus Petrolês. A geração atual mantém cosine e saturação como observação, com Scorer/Refiner/Judge de qualidade ativos.

## Referências

- [Pirá — repositório e descrição do dataset](https://github.com/C4AI/Pira) · [Pirá no Hugging Face](https://huggingface.co/datasets/paulopirozelli/pira)
- [ARC — dataset card e licença](https://huggingface.co/datasets/allenai/ai2_arc) · [artigo do ARC](https://arxiv.org/abs/1803.05457)
- [SQuAD 2.0](https://huggingface.co/datasets/rajpurkar/squad_v2)
- [HotpotQA — dataset card](https://huggingface.co/datasets/hotpotqa/hotpot_qa) · [repositório oficial](https://github.com/hotpotqa/hotpot)
- [BoolQ — dataset card](https://huggingface.co/datasets/google/boolq)
- [Documentação oficial do Dataset Viewer API](https://huggingface.co/docs/dataset-viewer/en/quick_start)
