"""Parada por novidade útil, cobertura e recuperação; independente do teto operacional."""
import math

VERSION='coverage-novelty-recovery-v1'


def diagnostics(records,documents,cfg):
    measured=[r for r in records if r.get('novelty_measurable')]
    used={r['doc_id'] for r in records if r.get('judge',{} ) and r['judge'].get('valid')}
    facets={d['facet_id'] for d in documents};visited={r['facet_id'] for r in measured}
    doc_fraction=len(used)/max(1,len(documents));facet_fraction=len(visited & facets)/max(1,len(facets))
    coverage_ok=bool(documents and len(measured)>=cfg.minimum_subtopic_candidates and
                     doc_fraction>=cfg.coverage_fraction and facet_fraction>=cfg.coverage_fraction)
    n=cfg.novelty_window; windows=[]
    # Janelas completas, disjuntas, sobre candidatas com decisão utilizável, sem falhas de API.
    for end in range(n,len(measured)+1,n):
        window=measured[end-n:end];before=measured[:end-n]
        baseline={r.get('target_id') for r in before if r.get('useful_novel')}
        targets={r.get('target_id') for r in window if r.get('useful_novel')}-baseline-{None,''}
        windows.append({'end':end,'n':n,'novel_count':sum(bool(r.get('useful_novel')) for r in window),
            'novel_yield':sum(bool(r.get('useful_novel')) for r in window)/n,
            'quality_yield':sum(bool(r.get('quality_approved')) for r in window)/n,'new_targets':len(targets)})
    last=windows[-cfg.novelty_patience:]
    low=bool(len(last)==cfg.novelty_patience and all(w['novel_yield']<=cfg.minimum_novelty_yield and
                                                  w['new_targets']==0 for w in last))
    evidence_quality=bool(last and all(w['quality_yield']>.10 for w in last))
    return {'version':VERSION,'measured_candidates':len(measured),'candidate_count':len(records),
        'document_coverage':round(doc_fraction,4),'facet_coverage':round(facet_fraction,4),
        'coverage_ok':coverage_ok,'window_size':n,'windows':last,
        'low_novelty_persistent':low,'quality_not_stalled':evidence_quality,
        'suspect_saturation':coverage_ok and low,'unmeasurable_candidates':len(records)-len(measured)}


def update_status(state,records,documents,cfg):
    diag=diagnostics(records,documents,cfg)
    phase=state.get('phase','exploring')
    if phase in ('saturated','quality_blocked'):
        after=records[state.get('closed_at',len(records)):]
        return {**state,'diagnostics':diag,'observed_novel_after_signal':sum(bool(r.get('useful_novel')) for r in after)}
    if phase=='recovery':
        start=state['recovery_start'];recent=records[start:]
        measured=[r for r in recent if r.get('novelty_measurable')]
        if any(r.get('useful_novel') for r in recent):
            return {'phase':'exploring','diagnostics':diag,'recovered_at':len(records),
                    'recovery_count':state.get('recovery_count',0),'suppress_until':len(records)+cfg.novelty_window}
        distinct_docs={r['doc_id'] for r in measured}
        required_docs=min(2,len(documents))
        if len(measured)>=cfg.recovery_candidates and len(distinct_docs)>=required_docs:
            quality=sum(bool(r.get('quality_approved')) for r in measured)/len(measured)
            return {**state,'phase':'saturated' if quality>.10 else 'quality_blocked',
                    'diagnostics':diag,'recovery_measured':len(measured),'recovery_documents':len(distinct_docs),
                    'closed_at':len(records),
                    'reason':'persistent_low_novelty_after_recovery' if quality>.10 else 'quality_stalled_after_recovery'}
        return {**state,'diagnostics':diag,'recovery_measured':len(measured)}
    if diag['suspect_saturation'] and len(records)>=state.get('suppress_until',0):
        return {'phase':'recovery','recovery_start':len(records),'diagnostics':diag,
                'recovery_count':state.get('recovery_count',0)+1}
    return {**state,'phase':'exploring','diagnostics':diag}


def topic_status(subtopics):
    phases=[s['phase'] for s in subtopics.values()]
    closed=bool(phases and all(p in ('saturated','quality_blocked') for p in phases))
    return {'would_stop':closed,'all_saturated':closed and all(p=='saturated' for p in phases),
        'reason':('topic_saturated' if all(p=='saturated' for p in phases) else 'quality_blocked') if closed else None,
        'subtopics':subtopics,'version':VERSION}
