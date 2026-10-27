#!/usr/bin/env python3
"""G14 compared to G13/G12/G11/G8/G10: 677 old + 140 new cases.

New 140-case cohort was fixed without reading G14 comparative CI results.
Each method must produce the identical entire canonical selected tuple.
Store all losses, certificate outcomes and paired repeated runtimes.
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

from benchmarks.g13_rfp_three_cohorts import all_cases as previous_cases
from experiments.v03.g14_certified_hybrid import solve_g14
from experiments.v03.g14_three_omission_certificate import certify_g14
from experiments.v03.g13_certified_hybrid import solve_g13
from experiments.v03.g12_certified_hybrid import solve_g12
from experiments.v03.g11_hybrid import solve_g11
from experiments.v03.g11_bounded_g8 import solve_g8
from experiments.v03.g10_direct_next import solve_g10

SEED=27102714
METHODS={'g14':solve_g14,'g13':solve_g13,'g12':solve_g12,
         'g11':solve_g11,'g8':solve_g8,'g10':solve_g10}


def new_cases():
    rng=random.Random(SEED)
    for h in (10,12,19,32,48,64,65,90,110,120):
        for extra in (2,30):
            n=h+extra
            m=n*(n+1)//2-h
            for family in ('three_omissions','two_omissions','one_omission',
                           'convex_quadratic','random_signed',
                           'broken_suffix','flat'):
                if family.endswith('omissions') or family=='one_omission':
                    if family=='one_omission':
                        Q={h}
                    elif family=='two_omissions':
                        u=(h-1)//2
                        Q={u,h-u}
                    else:
                        Q={1,2,h-3}
                    a=tuple((-10**160 if i in Q else 4**i)
                            for i in range(1,n+1))
                elif family=='convex_quadratic':
                    a=tuple(i*i for i in range(n))
                elif family=='random_signed':
                    a=tuple(rng.randint(-1000,1000) for _ in range(n))
                elif family=='broken_suffix':
                    a=tuple([i*i for i in range(n-1)]+[-1])
                else:
                    a=(0,)*n
                yield {'id':f'fresh_h{h}_n{n}_{family}',
                       'family':family,'cohort':'new_g14_holdout',
                       'n':n,'h':h,'m':m,'a':a}


def fixtures(profile):
    old=list(previous_cases('smoke' if profile=='smoke' else 'full'))
    if profile=='smoke':
        new=[c for index,c in enumerate(new_cases()) if index%7==0]
    else:
        new=list(new_cases())
    for c in old:
        yield dict(c,id='previous_'+c['id'],cohort='previous')
    yield from new


def summary(rows):
    ratios=[p['baseline_over_g14'] for p in rows]
    return {'paired':len(ratios),
            'g14_wins':sum(x>1 for x in ratios),
            'g14_losses':sum(x<1 for x in ratios),
            'median_ratio':statistics.median(ratios) if ratios else None}


def benchmark(profile,repeats):
    cases=list(fixtures(profile))
    assert len({x['id'] for x in cases})==len(cases)
    schedule=[(i,solver) for i in range(len(cases)) for solver in METHODS]
    random.Random(SEED+11).shuffle(schedule)
    certs={}
    results={}
    rows=[]
    for ci,name in schedule:
        c=cases[ci]
        if ci not in certs:
            metrics={}
            candidate=certify_g14(c['a'],c['m'],counters=metrics)
            certs[ci]={'status':metrics['status'],
                       'certified':candidate is not None}
        record={'case_id':c['id'],'method':name,
                'status':'PENDING','samples_ns':[]}
        try:
            fun=METHODS[name]
            fun(c['a'],c['m'])
            for _ in range(repeats):
                start=time.perf_counter_ns()
                answer=fun(c['a'],c['m'])
                record['samples_ns'].append(time.perf_counter_ns()-start)
                if ci in results and answer!=results[ci]:
                    raise AssertionError('nonidentical canonical selected tuple')
                results[ci]=answer
            record.update(status='PASS',feasible=bool(answer),
                          median_ns=statistics.median(record['samples_ns']))
        except Exception as exc:
            record.update(status='ERROR',reason=repr(exc))
        rows.append(record)
    timings={(r['case_id'],r['method']):r for r in rows
             if r['status']=='PASS'}
    comparisons={}
    for old in METHODS:
        if old=='g14':
            continue
        pairs=[]
        for idx,c in enumerate(cases):
            candidate=timings.get((c['id'],'g14'))
            baseline=timings.get((c['id'],old))
            if candidate is None or baseline is None:
                continue
            pairs.append({'case_id':c['id'],'cohort':c['cohort'],
                'family':c['family'],'h':c['h'],
                'certificate':certs[idx]['status'],
                'feasible':candidate['feasible'],
                'baseline_over_g14':
                    baseline['median_ns']/candidate['median_ns']})
        comparisons[old]={
            'all':summary(pairs),
            'previous':summary([p for p in pairs if p['cohort']=='previous']),
            'new_holdout':summary([p for p in pairs if p['cohort']=='new_g14_holdout']),
            'feasible':summary([p for p in pairs if p['feasible']]),
            'infeasible':summary([p for p in pairs if not p['feasible']]),
            'three_omissions':summary([p for p in pairs
                                      if p['certificate']=='three_omissions']),
            'abstained':summary([p for p in pairs
                                 if p['certificate'].startswith('unresolved')]),
            'pairs':pairs}
    root=Path(__file__).resolve().parents[1]
    paths=('experiments/v03/g14_three_omission_certificate.py',
           'experiments/v03/g14_certified_hybrid.py',
           'experiments/v03/g13_two_sided_certificate.py',
           'experiments/v03/g11_hybrid.py',
           'experiments/v03/g11_bounded_g8.py',
           'experiments/v03/g10_direct_next.py',
           'benchmarks/g14_rfp_three_omission_screen.py')
    sources={p:hashlib.sha256((root/p).read_bytes()).hexdigest()
             for p in paths}
    git=subprocess.run(['git','rev-parse','HEAD'],cwd=root,
                       capture_output=True,text=True)
    return {'meta':{'seed':SEED,'profile':profile,'repeats':repeats,
            'count':len(cases),'python':sys.version,
            'platform':platform.platform(),'head':git.stdout.strip(),
            'source_sha256':sources,
            'limitations':'one-host experimental medians; no statistical '
                          'or worldwide SOTA claims'},
            'cases':[{k:(hashlib.sha256(json.dumps([v,c['m']]).encode()).hexdigest()
                          if k=='a' else v) for k,v in c.items()} for c in cases],
            'certificate':{cases[i]['id']:x for i,x in certs.items()},
            'rows':rows,'comparisons':comparisons,
            'errors':sum(r['status']=='ERROR' for r in rows)}


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--profile',choices=('smoke','full'),default='smoke')
    parser.add_argument('--repeats',type=int,default=3)
    parser.add_argument('--output',default='g14_rfp_results.json')
    a=parser.parse_args()
    if not 1<=a.repeats<=30:
        parser.error('repeats 1..30')
    res=benchmark(a.profile,a.repeats)
    Path(a.output).write_text(json.dumps(res,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'output':a.output,'cases':res['meta']['count'],
        'errors':res['errors'],
        'comparisons':{k:{n:v for n,v in x.items() if n!='pairs'}
                       for k,x in res['comparisons'].items()}},indent=2))
    raise SystemExit(1 if res['errors'] else 0)
