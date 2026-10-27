#!/usr/bin/env python3
"""Prospective G13-v-G12/G11/G8/G10 677-case study (old 425 + new 252).

New cases and seed are frozen BEFORE examining G13 comparative CI performance.
Retain every loss, infeasible result, source digest, and full witness equality.
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

from benchmarks.g12_rfp_matched import fixed_cases
from experiments.v03.g13_certified_hybrid import solve_g13
from experiments.v03.g13_two_sided_certificate import certify_g13
from experiments.v03.g12_certified_hybrid import solve_g12
from experiments.v03.g11_hybrid import solve_g11
from experiments.v03.g11_bounded_g8 import solve_g8
from experiments.v03.g10_direct_next import solve_g10

SEED=26102713
METHODS={'g13':solve_g13,'g12':solve_g12,
         'g11':solve_g11,'g8':solve_g8,'g10':solve_g10}


def new_holdout():
    rng=random.Random(SEED)
    for h in (8,12,19,24,32,48,60,64,65,75,90,110):
        for extra in (2,5,50):
            n=h+extra
            U=n*(n+1)//2
            for family in ('flat','core_signed','nearconvex','plateau',
                           'one_omission','two_omissions','three_omissions'):
                omitted=()
                if family=='flat':
                    a=(0,)*n
                elif family=='core_signed':
                    a=tuple(rng.randint(-1000,1000) if i<h
                            else 4**i for i in range(n))
                elif family=='nearconvex':
                    x=[i*i for i in range(n)]
                    x[max(2,h//2)]+=rng.randint(10,1000)
                    a=tuple(x)
                elif family=='plateau':
                    a=tuple(i if i<h else 4**i for i in range(n))
                else:
                    if family=='one_omission':
                        omitted=(h,)
                    elif family=='two_omissions':
                        u=(h-1)//2
                        omitted=(u,h-u)
                    else:
                        omitted=(1,2,h-3)
                    marked=set(omitted)
                    a=tuple((-10**140 if i in marked else 4**i)
                            for i in range(1,n+1))
                yield {'id':f'new_h{h}_n{n}_{family}',
                       'h':h,'n':n,'m':U-h,'a':a,'family':family,
                       'cohort':'new_holdout'}


def all_cases(profile):
    if profile=='smoke':
        old=[c for idx,c in enumerate(fixed_cases('smoke')) if idx%4==0]
        new=[c for idx,c in enumerate(new_holdout()) if idx%12==0]
    else:
        old=list(fixed_cases('full'))
        new=list(new_holdout())
    for c in old:
        yield dict(c,id='legacy_'+c['id'],cohort='legacy')
    yield from new


def summarize(pairs):
    ratios=[x['baseline_over_g13'] for x in pairs]
    return {'paired':len(ratios),
            'g13_wins':sum(x>1 for x in ratios),
            'g13_losses':sum(x<1 for x in ratios),
            'median_ratio':statistics.median(ratios) if ratios else None}


def evaluate(profile,repeats):
    cases=list(all_cases(profile))
    ids=[c['id'] for c in cases]
    if len(ids)!=len(set(ids)):
        raise AssertionError('duplicate case ids')
    order=[(idx,name) for idx in range(len(cases)) for name in METHODS]
    random.Random(SEED+107).shuffle(order)
    values={}
    provenance={}
    records=[]
    for index,name in order:
        c=cases[index]
        if index not in provenance:
            info={}
            certificate=certify_g13(c['a'],c['m'],counters=info)
            provenance[index]={'status':info['status'],
                               'certified':certificate is not None}
        record={'case_id':c['id'],'method':name,'status':'PENDING',
                'samples_ns':[]}
        try:
            solver=METHODS[name]
            solver(c['a'],c['m'])
            for _ in range(repeats):
                start=time.perf_counter_ns()
                witness=solver(c['a'],c['m'])
                record['samples_ns'].append(time.perf_counter_ns()-start)
                if index in values and values[index]!=witness:
                    raise AssertionError('whole canonical witness mismatch')
                values[index]=witness
            record.update(status='PASS',feasible=bool(witness),
                          median_ns=statistics.median(record['samples_ns']))
        except Exception as exc:
            record.update(status='ERROR',reason=repr(exc))
        records.append(record)
    timings={(r['case_id'],r['method']):r for r in records
             if r['status']=='PASS'}
    comparisons={}
    for other in METHODS:
        if other=='g13':
            continue
        pairs=[]
        for index,c in enumerate(cases):
            g13=timings.get((c['id'],'g13'))
            baseline=timings.get((c['id'],other))
            if g13 is None or baseline is None:
                continue
            pairs.append({'case_id':c['id'],'family':c['family'],
                'cohort':c['cohort'],'h':c['h'],
                'certification':provenance[index]['status'],
                'feasible':g13['feasible'],
                'baseline_over_g13':baseline['median_ns']/g13['median_ns']})
        comparisons[other]={
            'all':summarize(pairs),
            'legacy':summarize([p for p in pairs if p['cohort']=='legacy']),
            'new_holdout':summarize([p for p in pairs if p['cohort']=='new_holdout']),
            'feasible':summarize([p for p in pairs if p['feasible']]),
            'infeasible':summarize([p for p in pairs if not p['feasible']]),
            'certified':summarize([p for p in pairs if p['certification']!='unresolved']),
            'abstained':summarize([p for p in pairs if p['certification']=='unresolved']),
            'weighted_infeasible':summarize([p for p in pairs
                         if p['certification']=='weighted_hitting_infeasible']),
            'pairs':pairs}
    root=Path(__file__).resolve().parents[1]
    paths=('experiments/v03/g13_two_sided_certificate.py',
           'experiments/v03/g13_certified_hybrid.py',
           'experiments/v03/g12_linear_certificate.py',
           'experiments/v03/g11_hybrid.py',
           'experiments/v03/g11_bounded_g8.py',
           'experiments/v03/g10_direct_next.py',
           'benchmarks/g13_rfp_three_cohorts.py')
    sha={p:hashlib.sha256((root/p).read_bytes()).hexdigest() for p in paths}
    rev=subprocess.run(['git','rev-parse','HEAD'],cwd=root,
                       capture_output=True,text=True)
    return {'meta':{'seed':SEED,'profile':profile,'repeats':repeats,
            'case_count':len(cases),'head':rev.stdout.strip(),
            'sources':sha,'python':sys.version,'platform':platform.platform(),
            'limits':'exploratory, same-process paired medians; neither '
                     'statistical significance nor global SOTA is implied'},
            'cases':[{k:(hashlib.sha256(json.dumps([v,c['m']]).encode()).hexdigest()
                          if k=='a' else v) for k,v in c.items()} for c in cases],
            'certificate_status':{cases[i]['id']:v for i,v in provenance.items()},
            'records':records,'comparisons':comparisons,
            'errors':sum(r['status']=='ERROR' for r in records)}


if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--profile',choices=('smoke','full'),default='smoke')
    ap.add_argument('--repeats',type=int,default=3)
    ap.add_argument('--output',default='g13_rfp_benchmark.json')
    args=ap.parse_args()
    if not 1<=args.repeats<=30:
        ap.error('repeats must be between 1 and 30')
    report=evaluate(args.profile,args.repeats)
    Path(args.output).write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'output':args.output,
        'case_count':report['meta']['case_count'],'errors':report['errors'],
        'comparisons':{name:{k:v for k,v in d.items() if k!='pairs'}
                       for name,d in report['comparisons'].items()}},indent=2))
    raise SystemExit(1 if report['errors'] else 0)
