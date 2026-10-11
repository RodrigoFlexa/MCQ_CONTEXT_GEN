"""Exploração equilibrada e seleção por cobertura/rendimento, determinística e retomável."""
from collections import Counter
import hashlib
import math
import random

from .config import DIFFICULTIES
from .stopping import update_status,topic_status


def target_list(context):
    return [{'target_id':hashlib.sha256((context['topic']+'|'+context['subtopic']+'|'+
                 ' '.join(t.casefold().split())).encode()).hexdigest()[:16],'description':t}
            for t in context['source_audit']['targets']]


class CoverageScheduler:
    def __init__(self,cfg,domain,store):
        self.cfg,self.domain,self.store=cfg,domain,store
        self.statuses=store.state.setdefault('exploration',{})

    def refresh(self,topic):
        statuses=self.statuses.setdefault(topic,{})
        for sub in self.domain.covered_subtopics(topic):
            rows=[r for r in self.store.records if r['topic']==topic and r['subtopic']==sub]
            statuses[sub]=update_status(statuses.get(sub,{}),rows,self.domain.documents(topic,sub),self.cfg)
        self.store.save_state()
        return topic_status(statuses)

    def choose(self,topic):
        status=self.refresh(topic)
        covered=self.domain.covered_subtopics(topic)
        live=[s for s in covered if status['subtopics'][s]['phase'] not in ('saturated','quality_blocked')]
        # Em observação, áreas com sinal fechado continuam disponíveis para medir perdas pós-sinal.
        pool=(live or covered) if self.cfg.enable_saturation_stop else list(covered)
        count=sum(r['topic']==topic for r in self.store.rounds)
        rng=random.Random(f'{self.cfg.seed}:{topic}:{count}')
        rng.shuffle(pool)
        quotas={s:self.cfg.limit_per_topic//len(covered)+(i<self.cfg.limit_per_topic%len(covered))
                for i,s in enumerate(covered)}
        def subscore(sub):
            rows=[r for r in self.store.records if r['topic']==topic and r['subtopic']==sub]
            diag=status['subtopics'][sub]['diagnostics']
            rounds=[r for r in self.store.rounds if r['topic']==topic and r['subtopic']==sub]
            accepted=sum(bool(r.get('accepted')) for r in rows)
            return (accepted>=quotas[sub],diag['coverage_ok'],len(rows),len(rounds))
        sub=min(pool,key=subscore)
        rows=[r for r in self.store.records if r['topic']==topic and r['subtopic']==sub]
        recent_rounds=[r for r in self.store.rounds if r['topic']==topic and r['subtopic']==sub]
        # Seleção por célula local; nunca sincronizada com o ciclo global de subtópicos.
        accepted_counts=Counter(r.get('difficulty') for r in rows if r.get('useful_novel'))
        requested=Counter(r['requested_difficulty'] for r in recent_rounds)
        difficulty=min(DIFFICULTIES,key=lambda d:(requested[d],accepted_counts[d]))
        docs=self.domain.documents(topic,sub);rng.shuffle(docs)
        facet_visits=Counter(r['facet_id'] for r in recent_rounds)
        doc_visits=Counter(r.get('doc_id') for r in recent_rounds)
        # Recuperação prefere documento não usado na janela que motivou o sinal.
        state=status['subtopics'][sub]
        recent={r['doc_id'] for r in rows[-self.cfg.novelty_window:]}
        recovery_docs={r['doc_id'] for r in rows[state.get('recovery_start',len(rows)):]} if state['phase']=='recovery' else set()
        previous_chunks={c['chunk_id'] for r in rows[-self.cfg.batch_size:] for c in r.get('source_chunks',[])}
        def docscore(doc):
            history=[r for r in rows if r['doc_id']==doc['doc_id'] and r.get('novelty_measurable')]
            n=len(history);novel=sum(bool(r.get('useful_novel')) for r in history)
            utility=(novel+1)/(n+2)+math.sqrt(math.log(len(rows)+2)/(n+1))
            chunks={c['chunk_id'] for c in doc['chunks']}
            overlap=len(chunks & previous_chunks)/max(1,len(chunks))
            return (doc['doc_id'] in recovery_docs if state['phase']=='recovery' else False,
                    doc['doc_id'] in recent if state['phase']=='recovery' else False,
                    facet_visits[doc['facet_id']]>0,doc_visits[doc['doc_id']]>0,
                    overlap,-utility,doc_visits[doc['doc_id']])
        doc=min(docs,key=docscore)
        context=self.domain.materialize(topic,sub,doc_id=doc['doc_id'])
        targets=target_list(context)
        usage=Counter(r.get('target_id') for r in rows if r.get('useful_novel'))
        targets.sort(key=lambda t:(usage[t['target_id']],t['target_id']))
        context['generation_targets']=targets[:self.cfg.batch_size]
        decision={'topic':topic,'subtopic':sub,'doc_id':doc['doc_id'],'facet_id':doc['facet_id'],
                  'difficulty':difficulty,'phase':state['phase'],'coverage':state['diagnostics'],
                  'generation_targets':context['generation_targets'],'selection':'coverage_then_smoothed_yield_and_source_overlap'}
        decision['subtopic_quota']=quotas[sub]
        decision['subtopic_accepted']=sum(bool(r.get('accepted')) for r in rows)
        return context,difficulty,decision,status
