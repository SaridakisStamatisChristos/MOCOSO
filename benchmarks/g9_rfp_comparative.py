#!/usr/bin/env python3
"""Prospective exploratory G8/G9/T1/public crossover screen. Not SOTA evidence.

No original solver is changed. Each method has a warmup and repeated complete
witness timings in the same Python process. No hard timeout, independent host,
process isolation, statistical confidence interval, or performance certification.
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
from experiments.v03.g9_corrected import solve_g9
from experiments.v03.g8_persistent_intervals import solve_g8
from experiments.v03.deficit import solve_deficit
from modconvex import solve as solve_public

SEED = 20261026
METHODS = ('g9_corrected', 'g8', 't1_deficit', 'public_default')


def instances(profile):
    if profile == 'smoke':
        ns, hs = (8, 16), (0, 2, 5)
    elif profile == 'ci':
        ns, hs = (8, 12, 24, 40), (0, 1, 3, 8, 12, 19)
    else:
        ns, hs = (12, 24, 40, 64), (0, 1, 3, 8, 12, 19, 30)
    for n in ns:
        U = n * (n + 1)//2
        for h in hs:
            if h >= n or U-h < 2 or 2*(U-h) <= U:
                continue
            m = U-h
            rng = random.Random(SEED*1000+n*101+h)
            families = {
                'powers4': tuple(4**i for i in range(n)),
                'quadratic': tuple(i*i for i in range(n)),
                'signed_jitter': tuple(i*i+rng.randrange(-3*i,3*i+1) for i in range(n)),
                'flat': (0,)*n,
                'suffix_fault': tuple([4**i for i in range(n-1)]+[-1]),
            }
            for name, a in families.items():
                digest = hashlib.sha256(json.dumps([a,m]).encode()).hexdigest()
                yield {'case_id':f'n{n}-h{h}-{name}', 'n':n,'h':h,
                       'family':name,'m':m,'a':a,'input_sha256':digest}


def independent_reference(a,m):
    best = ()
    for mask in range(1 << len(a)):
        s = tuple(i+1 for i in range(len(a)) if mask >> i & 1)
        if sum(s)%m:
            continue
        if any(a[i-1]+a[k-1] <= 2*a[j-1]
               for i,j,k in zip(s,s[1:],s[2:])):
            continue
        if len(s)>len(best) or (len(s)==len(best) and s<best):
            best=s
    return best


def validate(a,m,s):
    return (all(type(i) is int and 1<=i<=len(a) for i in s)
            and all(i<j for i,j in zip(s,s[1:]))
            and sum(s)%m == 0
            and all(a[i-1]+a[k-1] > 2*a[j-1]
                    for i,j,k in zip(s,s[1:],s[2:])))


def method_run(name,a,m):
    if name=='g9_corrected':
        return solve_g9(a,m)
    if name=='g8':
        return solve_g8(a,m)
    if name=='t1_deficit':
        result=solve_deficit(a,m)
    elif name=='public_default':
        result=solve_public(a,m)
    else:
        raise ValueError(name)
    if result.status!='OPTIMAL':
        raise RuntimeError(name+' did not certify OPTIMAL: '+result.status)
    return tuple(result.indices)


def excluded(name,case):
    if name=='public_default' and case['n']>16:
        return 'predeclared public size cap n>16'
    if name=='public_default' and case['h']>12:
        return 'predeclared public deficit cap h>12'
    if name=='t1_deficit' and case['h']>19:
        return 'predeclared T1 partition cap h>19'
    return None


def save_atomic(path,data):
    p=Path(path)
    p.parent.mkdir(parents=True,exist_ok=True)
    tmp=p.with_suffix(p.suffix+'.tmp')
    tmp.write_text(json.dumps(data,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    tmp.replace(p)


def main(profile,repeats,plan_only,output):
    cases=list(instances(profile))
    pairs=[(ix,name) for ix in range(len(cases)) for name in METHODS]
    random.Random(SEED+97).shuffle(pairs)
    observed={}
    rows=[]
    for index,name in pairs:
        case=cases[index]
        reason=excluded(name,case)
        row={'case_id':case['case_id'],'method':name,
             'status':'PLANNED_SKIP' if reason else 'PENDING',
             'measurements_ns':[]}
        if reason:
            row['reason']=reason
        if plan_only or reason:
            rows.append(row)
            continue
        a,m=case['a'],case['m']
        try:
            reference=independent_reference(a,m) if len(a)<=12 else None
            method_run(name,a,m)  # untraced warmup
            samples=[]
            for _ in range(repeats):
                start=time.perf_counter_ns()
                witness=method_run(name,a,m)
                samples.append(time.perf_counter_ns()-start)
                if not validate(a,m,witness):
                    raise AssertionError('invalid witness')
                if reference is not None and reference!=witness:
                    raise AssertionError('exhaustive oracle disagrees')
                if index in observed and observed[index]!=witness:
                    raise AssertionError('exact cross-algorithm witness disagrees')
            observed[index]=witness
            row.update(status='PASS',measurements_ns=samples,
                       median_ns=statistics.median(samples),
                       witness=list(witness),
                       verification=('exhaustive_oracle' if reference is not None
                                     else 'pending_cross_algorithm'))
        except Exception as error:
            row.update(status='ERROR',reason=type(error).__name__+': '+str(error))
        rows.append(row)
    counts={}
    for row in rows:
        if row['status']=='PASS':
            counts[row['case_id']]=counts.get(row['case_id'],0)+1
    for row in rows:
        if row['status']=='PASS' and row['verification']=='pending_cross_algorithm':
            row['verification']=('cross_algorithm_agreement'
                                  if counts[row['case_id']]>=2
                                  else 'single_method_unverified')
    bykey={(r['case_id'],r['method']):r['median_ns']
           for r in rows if r['status']=='PASS'}
    comparison={}
    for baseline in METHODS[1:]:
        exact=[]
        for case in cases:
            key=case['case_id']
            g9=bykey.get((key,'g9_corrected'))
            older=bykey.get((key,baseline))
            if g9 and older:
                exact.append({'case_id':key,'baseline_over_g9':older/g9})
        comparison[baseline]={
            'paired_count':len(exact),
            'g9_faster':sum(v['baseline_over_g9']>1 for v in exact),
            'g9_slower':sum(v['baseline_over_g9']<1 for v in exact),
            'median_pairwise_ratio':(statistics.median(v['baseline_over_g9'] for v in exact)
                                     if exact else None),
            'pairs':exact}
    root=Path(__file__).resolve().parents[1]
    source_paths=['experiments/v03/g9_corrected.py',
                  'experiments/v03/g8_persistent_intervals.py',
                  'experiments/v03/deficit.py','modconvex.py',
                  'benchmarks/g9_rfp_comparative.py']
    hashes={p:(hashlib.sha256((root/p).read_bytes()).hexdigest()
               if (root/p).exists() else None) for p in source_paths}
    rev=subprocess.run(['git','rev-parse','HEAD'],cwd=root,
                       capture_output=True,text=True,check=False)
    metadata={'seed':SEED,'profile':profile,'repeats':repeats,
              'plan_only':plan_only,'case_count':len(cases),
              'errors':sum(r['status']=='ERROR' for r in rows),
              'python':sys.version,'platform':platform.platform(),
              'processor':platform.processor(),
              'head_sha':rev.stdout.strip() if rev.returncode==0 else None,
              'source_sha256':hashes,
              'limits':'Same-process exploratory medians, no hard timeout or SOTA claim'}
    result={'metadata':metadata,'cases':[{**x,'a':list(x['a'])} for x in cases],
            'rows':rows,'comparisons':comparison}
    save_atomic(output,result)
    print(json.dumps({'output':output,'cases':len(cases),'errors':metadata['errors'],
                      'summary':{k:{p:v for p,v in x.items() if p!='pairs'}
                                 for k,x in comparison.items()}},indent=2))
    return 1 if metadata['errors'] else 0


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--profile',choices=('smoke','ci','paper'),default='smoke')
    parser.add_argument('--repeats',type=int,default=3)
    parser.add_argument('--plan-only',action='store_true')
    parser.add_argument('--output',default='g9_rfp_results.json')
    arg=parser.parse_args()
    if not 1<=arg.repeats<=30:
        parser.error('repeats must be 1..30')
    raise SystemExit(main(arg.profile,arg.repeats,arg.plan_only,arg.output))
