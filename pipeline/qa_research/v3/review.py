"""Revisão conjunta: qualidade das afirmações e cobertura são decisões distintas."""
import json
import re

from pipeline.inventario.llm import BudgetExceeded
from pipeline.inventario.textutil import atomic_json
from pipeline.qa_research.v2.language import lint_ptbr
from . import contracts as C, prompts as P
from .retrieval import prompt_source
from .runtime import CallFailure, Fatal


def input_size(payload, prompt):
    return len(json.dumps(payload,ensure_ascii=False))+len(prompt)


def outline(sections):
    return [{k:s[k] for k in ('id','titulo','pontos')} for s in sections]


def clean_headings(body, section_title, document_title):
    """Hierarquia de apresentação; não modifica o conteúdo técnico."""
    lines=body.strip().splitlines()
    if lines and re.sub(r'^#+\s*','',lines[0]).strip() in (section_title,document_title):lines=lines[1:]
    levels=[len(m[1]) for line in lines if (m:=re.match(r'^(#{1,6})\s+',line))]
    shift=max(0,3-min(levels)) if levels else 0
    return '\n'.join(re.sub(r'^(#{1,6})(?=\s)',lambda m:'#'*min(6,len(m[1])+shift),line) for line in lines).strip()


def editor_issues(section):
    body=section['texto'];issues=lint_ptbr(body)
    reading=(r'https?://|\bE[a-f0-9]{20}\b|'
        r'\b(?:(?:o|este|esse) trecho (?:consultado|citado|lido|fornecido|apresentado)|'
        r'a fonte afirma|nos ensaios relatados|referências? (?:consultadas?|disponíveis)|'
        r'(?:as? fontes?|as? referências?) (?:apontam|indicam|afirmam)|conforme a referência(?: consultada)?|'
        r'a base (?:disponível|documental)|o (?:conjunto|material) (?:disponível|fornecido) '
        r'(?:sustenta|indica|permite|mostra))\b')
    if re.search(reading,body,re.I):
        issues.append('Referências e relato de fonte devem ficar nos auxiliares; redija conhecimento autônomo')
    return issues


def apply_editorial(report,current):
    rows=[]
    for original in report['secoes']:
        row=dict(original)
        issues=editor_issues(current[row['id']])
        if issues and not row.get('operacional'):
            row.update(decisao='corrigir',motivo=row['motivo']+'; pendência editorial local',
                correcao='; '.join(filter(None,[row['correcao'],*issues])))
        rows.append(row)
    return dict(report,secoes=rows)


async def review_all(current,suffix,*,entrada,plan,pools,config,calls,errors,work):
    def review_payload(sections, coherence=False):
        source_map={s['id']:s for sources in pools.values() for s in sources}
        used={f for s in sections for f in s['fontes']}
        payload=dict(entrada=entrada,checklist=plan['pontos'],sumario=plan['secoes'],
            secoes_enviadas=sections,fontes=[] if coherence else [source_map[k] for k in sorted(used)],
            modo='coerencia_final' if coherence else 'tecnica_completa')
        if input_size(payload,P.REVIEW)>config['max_input_chars']:
            payload.update(sumario=outline(plan['secoes']),fontes=[prompt_source(s) for s in payload['fontes']])
        return payload

    groups=[]
    def divide(sections):
        payload=review_payload(sections)
        if len(json.dumps(payload,ensure_ascii=False))+len(P.REVIEW)<=config['max_input_chars']:
            groups.append(sections)
        elif len(sections)>1:
            middle=len(sections)//2;divide(sections[:middle]);divide(sections[middle:])
        else:groups.append(sections)  # O limite é diagnosticado pela chamada, sem cortar fontes.
    divide(list(current.values()))
    reports=[];decisions={};coverage={p['id']:dict(id=p['id'],estado='ausente',secoes=[],motivo='Sem revisão concluída') for p in plan['pontos']}
    omissions=[]
    async def one(sections, name, coherence=False):
        expected=[s['id'] for s in sections]
        try:
            result=await calls.call('review',name,review_payload(sections,coherence),lambda d:C.review(d,expected,coverage))
            reports.append(result)
            return result
        except (Fatal,BudgetExceeded):raise
        except (CallFailure,ValueError) as exc:
            errors.append(dict(etapa='revisao',secoes=expected,erro=str(exc)))
            return dict(secoes=[dict(id=s,decisao='corrigir',motivo='Revisão não concluída',correcao='Retomar revisão',consultas=[],lacunas_essenciais=[],limites=[],operacional=True) for s in expected],cobertura=[],omissoes_escopo=[])
    for gi,group in enumerate(groups,1):
        result=await one(group,f'revisao_{suffix}_{gi}')
        decisions.update((r['id'],r) for r in result['secoes'])
        omissions.extend(result['omissoes_escopo'])
        order={'ausente':0,'parcial':1,'atendido':2}
        for p in result['cobertura']:
            old=coverage[p['id']]
            if order[p['estado']]>order[old['estado']]:coverage[p['id']]=p
            elif p['estado']==old['estado']:
                old['secoes']=sorted(set(old['secoes'])|set(p['secoes']))
    if len(groups)>1:
        coherent=await one(list(current.values()),'coerencia_'+suffix,True)
        for r in coherent['secoes']:
            if r['decisao']=='corrigir':decisions[r['id']]=r
        coverage.update((p['id'],p) for p in coherent['cobertura'])
        omissions.extend(coherent['omissoes_escopo'])
    # Um ponto pode ter sido atendido por outra seção de um grupo diferente.
    for row in decisions.values():
        row['lacunas_essenciais']=[g for g in row['lacunas_essenciais'] if coverage[g['ponto']]['estado']!='atendido']
    result=dict(secoes=list(decisions.values()),cobertura=list(coverage.values()),omissoes_escopo=sorted(set(omissions)))
    atomic_json(work/('revisao_'+suffix+'_modelo.json'),result)
    result=apply_editorial(result,current)
    atomic_json(work/('revisao_'+suffix+'.json'),result)
    return result

