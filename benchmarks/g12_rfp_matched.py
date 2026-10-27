#!/usr/bin/env python3
"""Prospective G12-v-G11/G8/G10 matched benchmark incl. holdout and negatives.

Freeze before GitHub execution. No learned thresholds, no chosen-only cases.
Scores use whole canonical tuple equality. One process/host, multiple paired
repetitions; NOT a statistically certified universal SOTA comparison.
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

from benchmarks.g11_rfp_paired import cases as earlier_cases
from benchmarks.g11_rfp_holdout import cases as holdout_cases
from experiments.v03.g12_certified_hybrid import solve_g12
from experiments.v03.g12_linear_certificate import certify_up_to_two_omissions
from experiments.v03.g11_hybrid import solve_g11
from experiments.v03.g11_bounded_g8 import solve_g8
from experiments.v03.g10_direct_next import solve_g10

METHODS={'g12':solve_g12,'g11':solve_g11,
         'g8':solve_g8,'g10':solve_g10}
SEED=271026


def fixed_cases(profile):
    for idx,c in enumerate(earlier_cases('smoke' if profile=='smoke' else 'paper')):
        yield {'id':f'original_{idx}_{c["id"]}',
               'family':c['family'],'h':c['h'],'n':c['n'],
               'm':c['m'],'a':c['a'],'cohort':'original'}
    for idx,c in enumerate(holdout_cases()):
        if profile=='smoke' and (idx%8!=0):
            continue
        yield {'id':f'holdout_{idx}_{c["id"]}',
               'family':c['family'],'h':c['h'],'n':c['n'],
               'm':c['m'],'a':c['a'],'cohort':'holdout'}
    # Strictly feasible canonical two-omission instances, not in earlier sets.
    for h in (3,7,18,19,24,32,48,60,64,65,75,90,110,150):
        n=h+16
        u=(h-1)//2
        v=h-u
        if not 1<=u<v:
            continue
        bad={u,v}
        a=tuple((-10**170 if i in bad else 4**i) for i in range(1,n+1))
        yield {'id':f'two_omissions_h{h}', 'family':'known_two_omissions',
               'h':h,'n':n,'m':n*(n+1)//2-h,'a':a,'cohort':'constructed_t2'}


def summarize(pairs):
    ratios=[p['baseline_over_g12'] for p in pairs]
    return {'paired':len(ratios),'g12_wins':sum(r>1 for r in ratios),
            'g12_losses':sum(r<1 for r in ratios),
            'median_ratio':statistics.median(ratios) if ratios else None}


def execute(profile,repeats):
    cases=list(fixed_cases(profile))
    if len({c['id'] for c in cases})!=len(cases):
        raise AssertionError('case identifier collision')
    pairs=[(ix,name) for ix in range(len(cases)) for name in METHODS]
    random.Random(SEED+7).shuffle(pairs)
    witnesses={}
    records=[]
    certificates={}
    for ix,name in pairs:
        case=cases[ix]
        a,m=case['a'],case['m']
        if ix not in certificates:
            trace={}
            value=certify_up_to_two_omissions(a,m,counters=trace)
            certificates[ix]={
                'status':trace['status'],
                'certified':value is not None,
                'length':len(value) if value is not None else None}
        record={'case_id':case['id'],'method':name,
                'samples_ns':[],'status':'PENDING'}
        try:
            solver=METHODS[name]
            solver(a,m)  # fixed untimed warmup
            for _ in range(repeats):
                start=time.perf_counter_ns()
                witness=solver(a,m)
                record['samples_ns'].append(time.perf_counter_ns()-start)
                if ix in witnesses and witnesses[ix]!=witness:
                    raise AssertionError('canonical full-witness mismatch')
                witnesses[ix]=witness
            record.update(status='PASS',
                          median_ns=statistics.median(record['samples_ns']),
                          feasible=bool(witness))
        except Exception as exc:
            record.update(status='ERROR',reason=repr(exc))
        records.append(record)
    times={(r['case_id'],r['method']):r['median_ns']
           for r in records if r['status']=='PASS'}
    table={c['id']:c for c in cases}
    values={c['id']:certificates[i] for i,c in enumerate(cases)}
    compared={}
    for other in ('g11','g8','g10'):
        ps=[]
        for case in cases:
            key=case['id']
            if (key,'g12') not in times or (key,other) not in times:
                continue
            # The full witness of G12 must have been independently agreed to
            # by another algorithm on this exact same input.
            ps.append({'case_id':key,'cohort':case['cohort'],
                'family':case['family'],'h':case['h'],
                'certificate':values[key]['status'],
                'feasible':bool(witnesses[cases.index(case)]),
                'baseline_over_g12':times[(key,other)]/times[(key,'g12')]})
        compared[other]={
            'all':summarize(ps),
            'original':summarize([p for p in ps if p['cohort']=='original']),
            'holdout':summarize([p for p in ps if p['cohort']=='holdout']),
            'certified':summarize([p for p in ps if p['certificate']!='unresolved']),
            'unresolved':summarize([p for p in ps if p['certificate']=='unresolved']),
            'feasible':summarize([p for p in ps if p['feasible']]),
            'infeasible':summarize([p for p in ps if not p['feasible']]),
            'two_omissions':summarize([p for p in ps if p['certificate']=='two_omissions']),
            'pairs':ps}
    root=Path(__file__).resolve().parents[1]
    sources=('experiments/v03/g12_linear_certificate.py',
             'experiments/v03/g12_certified_hybrid.py',
             'experiments/v03/g11_hybrid.py',
             'experiments/v03/g11_bounded_g8.py',
             'experiments/v03/g10_direct_next.py',
             'benchmarks/g12_rfp_matched.py')
    source_hashes={p:hashlib.sha256((root/p).read_bytes()).hexdigest()
                   for p in sources}
    rev=subprocess.run(['git','rev-parse','HEAD'],cwd=root,
                       capture_output=True,text=True,check=False)
    return {'meta':{'seed':SEED,'profile':profile,'repeats':repeats,
            'case_count':len(cases),'source_sha256':source_hashes,
            'python':sys.version,'platform':platform.platform(),
            'head':rev.stdout.strip(),
            'limitations':'single-host Python exploratory medians; no new '
                          'theoretical SOTA or confidence interval'},
            'cases':[{k:(hashlib.sha256(json.dumps([v,c['m']]).encode()).hexdigest()
                          if k=='a' else v) for k,v in c.items()} for c in cases],
            'certificate_outcomes':values,'records':records,
            'comparisons':compared,
            'errors':sum(r['status']=='ERROR' for r in records)}


if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--profile',choices=('smoke','full'),default='smoke')
    p.add_argument('--repeats',type=int,default=3)
    p.add_argument('--output',default='g12_rfp_matched.json')
    a=p.parse_args()
    if not 1<=a.repeats<=30:
        p.error('repeats must be 1..30')
    result=execute(a.profile,a.repeats)
    Path(a.output).write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'output':a.output,'cases':result['meta']['case_count'],
        'errors':result['errors'],
        'comparisons':{k:{n:v for n,v in comp.items() if n!='pairs'}
                       for k,comp in result['comparisons'].items()}},indent=2))
    raise SystemExit(1 if result['errors'] else 0)
