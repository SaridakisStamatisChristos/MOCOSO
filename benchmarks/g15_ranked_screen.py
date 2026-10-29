#!/usr/bin/env python3
"""Frozen G15 screen: old 817, new 70 small-deficit, 48 expanded-domain cases.

Primary performance metric: median paired baseline/candidate runtime, with
all losses and ratio of sums also reported. Five repeats, one warmup; order
randomized per repetition. Synthetic exploratory evidence, not external SOTA.
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

from benchmarks.g14_rfp_three_omission_screen import fixtures
from experiments.v03.g15_ranked_omissions import solve_g15, solve_ranked
from experiments.v03.g14_certified_hybrid import solve_g14
from experiments.v03.g13_certified_hybrid import solve_g13
from experiments.v03.g10_direct_next import solve_g10
from experiments.v03.g11_bounded_g8 import solve_g8
from edge_dp import solve_edge

SEED = 2026102915
METHODS = dict(g15=solve_g15, ranked=solve_ranked, g14=solve_g14,
               g13=solve_g13, g10=solve_g10, g8=solve_g8, edge=solve_edge)


def new_cases():
    rng = random.Random(SEED)
    for h in (24,48,96,192,384):
        for extra in (2,37):
            n=h+extra
            for family in ('many_omissions','three_omissions','quadratic',
                           'signed_noise','convex_perturbed','flat','broken_suffix'):
                if family=='many_omissions':
                    t=1
                    while (t+1)*(t+2)//2 < h: t+=1
                    # Distinct omissions with exact sum h.
                    q=set(range(1,t)) | {h-t*(t-1)//2}
                    a=tuple(-10**400 if i in q else 4**i for i in range(1,n+1))
                elif family=='three_omissions':
                    a=tuple(-10**400 if i in (1,2,h-3) else 4**i
                            for i in range(1,n+1))
                elif family=='quadratic': a=tuple(i*i for i in range(n))
                elif family=='signed_noise': a=tuple(rng.randrange(-1000,1001) for _ in range(n))
                elif family=='convex_perturbed': a=tuple(i*i+rng.randrange(-3,4) for i in range(n))
                elif family=='flat': a=(0,)*n
                else: a=tuple(i*i for i in range(n-1))+(-1,)
                yield dict(id=f'new_h{h}_n{n}_{family}',cohort='new_small_deficit',
                           family=family,h=h,n=n,m=n*(n+1)//2-h,a=a)
    for n in (8,12,20,32):
        u=n*(n+1)//2
        for h in (n,2*n,min(3*n,(u-1)//2)):
            for family in ('quadratic','exponential','signed_noise','flat'):
                a=(tuple(i*i for i in range(n)) if family=='quadratic' else
                   tuple(4**i for i in range(n)) if family=='exponential' else
                   tuple(rng.randrange(-20,21) for _ in range(n))
                   if family=='signed_noise' else (0,)*n)
                yield dict(id=f'extended_n{n}_h{h}_{family}',cohort='extended',
                           family=family,h=h,n=n,m=u-h,a=a)


def cases(profile):
    old=[dict(c,cohort='previous_817') for c in fixtures('full')]
    fresh=list(new_cases())
    if profile=='smoke':
        old=old[::81]
        fresh=[c for c in fresh if c['n']<=50]
    return old+fresh


def source_manifest():
    root=Path(__file__).resolve().parents[1]
    # Includes transitive algorithm/generator/test dependencies, not just G15.
    paths=sorted(set(root.glob('experiments/v03/*.py')) |
                 set(root.glob('benchmarks/*.py')) |
                 {root/'edge_dp.py',root/'modconvex.py',
                  root/'tests/test_v03_g15_ranked_omissions.py'})
    return {str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest()
            for p in paths}


def run(profile,repeats,output):
    suite=cases(profile)
    assert len({c['id'] for c in suite})==len(suite)
    assert profile!='full' or len(suite)==935
    root=Path(__file__).resolve().parents[1]
    git=lambda *args:subprocess.check_output(['git',*args],cwd=root,text=True).strip()
    selected={c['id']:(('g15','ranked','edge') if c['cohort']=='extended'
                      else ('g15','ranked','g14','g13','g10','g8')) for c in suite}
    records={(c['id'],name):dict(case_id=c['id'],method=name,samples_ns=[])
             for c in suite for name in selected[c['id']]}
    gold={}
    schedule=[(c,name) for c in suite for name in selected[c['id']]]
    rng=random.Random(SEED+1)
    for rep in range(-1,repeats):
        rng.shuffle(schedule)
        for c,name in schedule:
            start=time.perf_counter_ns()
            answer=METHODS[name](c['a'],c['m'])
            elapsed=time.perf_counter_ns()-start
            if c['id'] in gold:
                assert answer==gold[c['id']],(c['id'],name,'whole witness mismatch')
            else:
                gold[c['id']]=answer
            if rep>=0: records[c['id'],name]['samples_ns'].append(elapsed)
    for (ci,name),r in records.items():
        r.update(median_ns=statistics.median(r['samples_ns']),status='PASS',
                 witness_sha256=hashlib.sha256(repr(gold[ci]).encode()).hexdigest())
    comparisons={}
    for name in ('g14','g13','g10','g8','edge','ranked'):
        groups={}
        for cohort in sorted({c['cohort'] for c in suite})+['all']:
            group=[c for c in suite if (cohort=='all' or c['cohort']==cohort)
                   and (c['id'],name) in records]
            if not group: continue
            x=[records[c['id'],name]['median_ns'] for c in group]
            y=[records[c['id'],'g15']['median_ns'] for c in group]
            ratios=[b/a for a,b in zip(y,x)]
            groups[cohort]=dict(cases=len(group),wins=sum(v>1 for v in ratios),
                losses=sum(v<1 for v in ratios),median_ratio=statistics.median(ratios),
                sum_ratio=sum(x)/sum(y))
        comparisons[name]=groups
    modes={}
    for c in suite:
        details={}
        solve_g15(c['a'],c['m'],counters=details)
        modes[c['id']]=details
    report=dict(meta=dict(seed=SEED,profile=profile,repeats=repeats,
        head=git('rev-parse','HEAD'),tree=git('rev-parse','HEAD^{tree}'),
        tracked_dirty=bool(git('diff','HEAD','--name-only')),
        python=sys.version,platform=platform.platform(),
        sources=source_manifest(),limits='synthetic; one host; no CI/novelty inference'),
        cases=[{**c,'a':list(c['a'])} for c in suite],rows=list(records.values()),
        modes=modes,comparisons=comparisons,errors=0)
    Path(output).write_text(json.dumps(report,sort_keys=True,indent=2)+'\n')
    print(json.dumps(dict(cases=len(suite),errors=0,comparisons=comparisons),indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--profile',choices=('smoke','full'),default='full')
    parser.add_argument('--repeats',type=int,default=5)
    parser.add_argument('--output',required=True)
    args=parser.parse_args()
    if not 1<=args.repeats<=30: parser.error('repeats must be 1..30')
    run(args.profile,args.repeats,args.output)
