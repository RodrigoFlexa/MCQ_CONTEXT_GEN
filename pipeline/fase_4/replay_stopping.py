"""Replay de sinais na trajetória observada; não simula mudanças na geração."""
import argparse
import csv
from dataclasses import replace
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
from pipeline.fase_4.config import QAConfig,SCHEMA_VERSION
from pipeline.fase_4.storage import read_jsonl,atomic_json
from pipeline.fase_4.stopping import update_status
import json


def replay(rows,documents,cfg):
    state={};first_recovery=None;first_closed=None;at_closed=None
    for i in range(1,len(rows)+1):
        state=update_status(state,rows[:i],documents,cfg)
        if first_recovery is None and state['phase']=='recovery':first_recovery=i
        if first_closed is None and state['phase'] in ('saturated','quality_blocked'):
            first_closed=i;at_closed=dict(state)
    after=rows[first_closed:] if first_closed is not None else []
    return {'candidates':len(rows),'measured_candidates':sum(bool(r.get('novelty_measurable')) for r in rows),
        'first_recovery_at':first_recovery,'first_closed_at':first_closed,
        'closed_reason':at_closed.get('reason') if at_closed else None,
        'novel_after_signal':sum(bool(r.get('useful_novel')) for r in after),
        'measured_after_signal':sum(bool(r.get('novelty_measurable')) for r in after),
        'accepted_after_signal':sum(bool(r.get('accepted')) for r in after),
        'final_phase':state.get('phase','no_candidates')}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--windows',type=int,nargs='+',default=[12,20,30])
    p.add_argument('--patiences',type=int,nargs='+',default=[2,3])
    p.add_argument('--coverages',type=float,nargs='+',default=[.5,.75,1.0])
    args=p.parse_args()
    manifest=json.loads((args.output/'run_config.json').read_text(encoding='utf-8'))
    if manifest['schema_version']!=SCHEMA_VERSION:raise ValueError('Replay requer os registros QA v3')
    settings={k:v for k,v in manifest['config'].items() if k in QAConfig.__dataclass_fields__}
    cfg=QAConfig(**settings)
    rows=read_jsonl(args.output/'candidatas_metricas.jsonl')
    audits=read_jsonl(args.output/'auditorias_contexto.jsonl')
    pairs=sorted({(r['topic'],r['subtopic']) for r in audits})
    result=[]
    for window in args.windows:
        for patience in args.patiences:
            for coverage in args.coverages:
                policy=replace(cfg,novelty_window=window,novelty_patience=patience,coverage_fraction=coverage)
                policy.validate()
                for topic,sub in pairs:
                    observed=[r for r in rows if r['topic']==topic and r['subtopic']==sub]
                    docs=[{'doc_id':r['doc_id'],'facet_id':r['audit']['facet_id']} for r in audits
                          if r['approved'] and r['topic']==topic and r['subtopic']==sub]
                    result.append({'topic':topic,'subtopic':sub,'window':window,'patience':patience,
                                   'coverage_required':coverage,'recovery_candidates':policy.recovery_candidates,
                                   **replay(observed,docs,policy)})
    directory=args.output/'analise_parada';directory.mkdir(parents=True,exist_ok=True)
    atomic_json(directory/'replay.json',{'method':'observed_trajectory_replay',
        'limitations':['Não reproduz mudanças de seleção ou geração causadas pela política.',
                       'Ausência de sinal nesta amostra não demonstra que o subtópico não satura.',
                       'Novidade útil é estimada pelos avaliadores, não certificada por especialista.'],
        'results':result})
    with (directory/'replay.csv').open('w',encoding='utf-8-sig',newline='') as stream:
        fields=list(result[0]) if result else ['topic','subtopic']
        writer=csv.DictWriter(stream,fieldnames=fields);writer.writeheader();writer.writerows(result)
    print(f'Replay salvo em {directory}; {len(result)} combinações de política e subtópico')


if __name__=='__main__':main()
