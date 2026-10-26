#!/usr/bin/env python3
"""G10 versus G9/G8/T1/public: exploratory matched crossover screen.

Inherits frozen families, exclusions and independent oracle from G9 RFP suite;
adds fixed, named maximal-omission cases. No SOTA or statistical claims.
"""
import argparse
import hashlib
import json
import platform
import random
import statistics
import subprocess
import sys
import time
from pathlib import Path

from benchmarks.g9_rfp_comparative import (instances,independent_reference,
    validate,method_run,excluded,save_atomic,SEED)
from experiments.v03.g10_direct_next import solve_g10

METHODS=('g10_direct','g9_corrected','g8','t1_deficit','public_default')


def expanded_cases(profile):
    yield from instances(profile)
    ks=(2,3,5) if profile=='smoke' else (2,3,5,7,9,11)
    for k in ks:
        h=k*(k+1)//2
        n=h+15
        a=tuple([-10**200]*k+[4**i for i in range(k,n)])
        m=n*(n+1)//2-h
        yield {'case_id':f'forced-k{k}-h{h}','n':n,'h':h,'m':m,
               'family':'forced_omissions','a':a,
               'input_sha256':hashlib.sha256(json.dumps([a,m]).encode()).hexdigest()}


def run(name,a,m):
    return solve_g10(a,m) if name=='g10_direct' else method_run(name,a,m)


def compare(profile,repeats,output):
    cases=list(expanded_cases(profile))
    order=[(ix,name) for ix in range(len(cases)) for name in METHODS]
    random.Random(SEED+109).shuffle(order)
    answers={}
    rows=[]
    for ci,name in order:
        case=cases[ci]
        reason=excluded(name,case)
        record={'case_id':case['case_id'],'method':name,'status':'PENDING',
                'samples_ns':[]}
        if reason:
            record.update(status='PLANNED_SKIP',reason=reason)
            rows.append(record)
            continue
        a,m=case['a'],case['m']
        try:
            gold=independent_reference(a,m) if len(a)<=12 else None
            run(name,a,m)  # Full warmup, outside timed observations.
            samples=[]
            for _ in range(repeats):
                start=time.perf_counter_ns()
                value=run(name,a,m)
                samples.append(time.perf_counter_ns()-start)
                if not validate(a,m,value):
                    raise AssertionError('invalid witness')
                if gold is not None and value!=gold:
                    raise AssertionError('independent selected-subset oracle mismatch')
                if ci in answers and answers[ci]!=value:
                    raise AssertionError('full-witness cross-algorithm mismatch')
            answers[ci]=value
            record.update(status='PASS',samples_ns=samples,witness=list(value),
                          median_ns=statistics.median(samples),
                          verification=('exhaustive_oracle' if gold is not None
                                        else 'pending_cross_algorithm'))
        except Exception as exc:
            record.update(status='ERROR',reason=type(exc).__name__+': '+str(exc))
        rows.append(record)
    count={}
    for row in rows:
        if row['status']=='PASS':
            count[row['case_id']]=count.get(row['case_id'],0)+1
    for row in rows:
        if row['status']=='PASS' and row['verification']=='pending_cross_algorithm':
            row['verification']=('cross_algorithm_agreement'
                if count[row['case_id']]>=2 else 'single_method_unverified')
    times={(r['case_id'],r['method']):r['median_ns']
           for r in rows if r['status']=='PASS'}
    status={r['case_id']:len(r['witness'])
            for r in rows if r['status']=='PASS' and r['method']=='g10_direct'}
    comparison={}
    for baseline in METHODS[1:]:
        pairs=[]
        for case in cases:
            key=case['case_id']
            new=times.get((key,'g10_direct'))
            old=times.get((key,baseline))
            if new and old:
                pairs.append({'case_id':key,'family':case['family'],
                              'feasible':bool(status[key]),'baseline_over_g10':old/new})
        def split(subset):
            values=[v['baseline_over_g10'] for v in subset]
            return {'count':len(values),
                    'g10_faster':sum(v>1 for v in values),
                    'g10_slower':sum(v<1 for v in values),
                    'median_ratio':statistics.median(values) if values else None}
        comparison[baseline]={'all':split(pairs),
            'feasible':split([p for p in pairs if p['feasible']]),
            'infeasible':split([p for p in pairs if not p['feasible']]),
            'pairs':pairs}
    root=Path(__file__).resolve().parents[1]
    paths=['experiments/v03/g10_direct_next.py','experiments/v03/g9_corrected.py',
           'experiments/v03/g8_persistent_intervals.py','experiments/v03/deficit.py',
           'modconvex.py','benchmarks/g10_rfp_comparative.py']
    source_sha={p:hashlib.sha256((root/p).read_bytes()).hexdigest() for p in paths}
    git=subprocess.run(['git','rev-parse','HEAD'],cwd=root,capture_output=True,text=True)
    report={'meta':{'seed':SEED,'profile':profile,'repeats':repeats,
        'cases':len(cases),'python':sys.version,'platform':platform.platform(),
        'head_sha':git.stdout.strip() if git.returncode==0 else None,
        'sources':source_sha,
        'constraints':'Same-process exploratory medians; no hard time/memory budget'},
        'cases':[{**x,'a':list(x['a'])} for x in cases],
        'rows':rows,'comparisons':comparison}
    save_atomic(output,report)
    print(json.dumps({'output':output,'case_count':len(cases),
          'errors':sum(r['status']=='ERROR' for r in rows),
          'comparison':{k:{g:v for g,v in d.items() if g!='pairs'}
                        for k,d in comparison.items()}},indent=2))
    return int(any(r['status']=='ERROR' for r in rows))


if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--profile',choices=('smoke','ci','paper'),default='smoke')
    p.add_argument('--repeats',type=int,default=3)
    p.add_argument('--output',default='g10_rfp_results.json')
    a=p.parse_args()
    if not 1<=a.repeats<=30:
        p.error('repeats must be 1..30')
    raise SystemExit(compare(a.profile,a.repeats,a.output))
