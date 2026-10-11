"""Adaptação QA da rubrica do notebook de dificuldade preservado no backup."""
import json
import math

VERSION='qa-difficulty-four-dimensions-v1'
BACKUP_ORIGIN='pipeline/backup/pre_petroquest_qa_2026-10-10/fase_4/avaliacao_dificuldade_azure.ipynb'
DIMENSIONS=('integracao_conhecimento','cadeia_raciocinio','demanda_cognitiva','especificidade_tecnica')
SYSTEM_PROMPT='''Você estima dificuldade intrínseca de QA para um profissional que estudou adequadamente o domínio FPSO/FSO e produção subsea. Julgue a resolução necessária, sem confundir extensão, siglas, obscuridade, redação ruim ou dependência de documento com dificuldade.
Avalie exatamente quatro dimensões com inteiros de 1 a 3:
- integracao_conhecimento: 1=recordação de um conceito; 2=interpretação/aplicação de um conceito em uma condição; 3=integração indispensável de dois ou mais conceitos/condições.
- cadeia_raciocinio: 1=decisão direta; 2=relação causal, comparação ou aplicação com etapas necessárias; 3=múltiplas inferências indispensáveis ou trade-offs, sem atalhos de recordação.
- demanda_cognitiva: 1=lembrar/compreender; 2=aplicar; 3=analisar, avaliar ou sintetizar sob condições/critério.
- especificidade_tecnica: 1=definição canônica ou conhecimento geral do domínio; 2=princípio técnico contextualizado; 3=conhecimento especializado, condicionado ou quantitativo necessário à resposta.
Avalie o raciocínio MÍNIMO suficiente, mesmo se a resposta editorial for longa. Uma comparação entre definições pode ser direta. Cenário e verbos como analisar não elevam o nível sozinhos. Conhecimento difícil de localizar na fonte não define a dificuldade: a fonte não será apresentada ao respondente.
Não há alternativas/distratores e nenhuma pontuação correspondente. O nível pedido ao gerador não é fornecido. A avaliação técnica da resposta pertence ao Judge separado. Informe justificativas curtas observáveis para cada dimensão; não exponha cadeia interna de pensamento.'''


def difficulty_prompt(questions):
    items=[{k:q[k] for k in ('id','question','answer','topic','subtopic') if k in q} for q in questions]
    return SYSTEM_PROMPT, f'''Avalie cada QA independentemente:
{json.dumps(items,ensure_ascii=False)}
Retorne JSON {{"evaluations":[{{"id":"id recebido","integracao_conhecimento":1,"cadeia_raciocinio":1,"demanda_cognitiva":1,"especificidade_tecnica":1,"reasons":{{"integracao_conhecimento":"...","cadeia_raciocinio":"...","demanda_cognitiva":"...","especificidade_tecnica":"..."}},"confidence":0.9}}]}}.
Exatamente uma avaliação por ID; não receba nem invente dificuldade originalmente solicitada.'''


def parse_difficulty(raw):
    if not isinstance(raw,dict) or any(type(raw.get(k)) is not int or raw[k] not in (1,2,3) for k in DIMENSIONS):
        return {'valid':False,'reason':'invalid_difficulty_dimensions','raw':raw}
    reasons=raw.get('reasons');conf=raw.get('confidence')
    if not isinstance(reasons,dict) or any(not isinstance(reasons.get(k),str) or not reasons[k].strip() for k in DIMENSIONS):
        return {'valid':False,'reason':'missing_difficulty_reasons','raw':raw}
    if isinstance(conf,bool) or not isinstance(conf,(int,float)) or not math.isfinite(conf) or not 0<=conf<=1:
        return {'valid':False,'reason':'invalid_difficulty_confidence','raw':raw}
    score=sum(raw[k] for k in DIMENSIONS)/4
    label='facil' if score<=1.66 else 'media' if score<=2.33 else 'dificil'
    if label=='dificil' and (raw['cadeia_raciocinio']<2 or raw['demanda_cognitiva']<2): label='media'
    return {'valid':True,'version':VERSION,'origin':BACKUP_ORIGIN,'scores':{k:raw[k] for k in DIMENSIONS},
            'reasons':reasons,'confidence':conf,'score':round(score,3),'difficulty':label,
            'requires_human_review':conf<.75}


def evaluate_difficulty(client,questions):
    if not questions:return {}
    system,user=difficulty_prompt(questions)
    result=client.complete_json(user,system=system,max_tokens=10000)
    records=result.get('evaluations',[]) if isinstance(result,dict) else []
    if not isinstance(records,list):records=[]
    mapping,duplicates={},set()
    for raw in records:
        if not isinstance(raw,dict) or not isinstance(raw.get('id'),str):continue
        if raw['id'] in mapping:duplicates.add(raw['id'])
        mapping[raw['id']]=raw
    return {q['id']:parse_difficulty(None if q['id'] in duplicates else mapping.get(q['id'])) for q in questions}
