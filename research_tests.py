import sys, os, itertools, random, time, statistics, platform, json, hashlib, tracemalloc, resource
sys.path.insert(0, os.path.dirname(__file__))
from modconvex import solve, oracle, verify, cubic_dp, index_only_upper

base = os.path.dirname(__file__)
seed = 20261023
rng = random.Random(seed)
unique = set()
executions = 0
threshold_execs = 0
failures = []
family_counts = {}

def check(a,m,extended=True):
    global executions, threshold_execs
    a=tuple(a)
    case=(a,m)
    assert case not in unique
    unique.add(case)
    executions += 1
    expected = oracle(a,m)
    out = solve(a,m)
    if out.status != 'OPTIMAL' or out.indices != expected or not verify(a,m,out.indices):
        failures.append(('opt',a,m,expected,out.__dict__))
        raise AssertionError(failures[-1])
    if len(a)<=5 and executions % 17 == 0:
        naive=cubic_dp(a,m)
        if naive != expected:
            failures.append(('cubic',a,m,expected,naive))
            raise AssertionError(failures[-1])
    if extended and (executions % 8 == 0):
        for K in (-1,0,1,len(a)//2,len(a),len(a)+1):
            d=solve(a,m,K=K)
            threshold_execs+=1
            if (d.status == 'FEASIBLE') != (len(expected)>=K) or (d.status=='FEASIBLE' and (len(d.indices)<K or not verify(a,m,d.indices))) or d.status=='RESOURCE_LIMIT':
                failures.append(('decision',a,m,K,expected,d.__dict__))
                raise AssertionError(failures[-1])
    return expected

for n in range(0,5):
    alphabet=(-2,-1,0,1,2)
    for a in itertools.product(alphabet,repeat=n):
        for m in range(2,n*(n+1)//2+4):
            check(a,m)
    family_counts[f'exhaustive n={n}, alphabet={alphabet}']=len(unique)-sum(family_counts.values())

# n=5, 3 alphabet, wider modulus
for a in itertools.product((-1,0,1),repeat=5):
    for m in range(2,20):
        check(a,m)
family_counts['exhaustive n=5, alphabet=(-1,0,1)']=len(unique)-sum(family_counts.values())

for t in range(350):
    n=rng.randrange(0,12)
    style=t%6
    if style==0:
        a=[rng.randrange(-20,21) for _ in range(n)]
    elif style==1:
        a=[rng.choice([-10**100,0,10**100]) for _ in range(n)]
    elif style==2:
        a=[i*i * (1 if rng.randrange(2) else -1) for i in range(n)]
    elif style==3:
        a=[rng.randrange(-5,6) for _ in range(n)]
    elif style==4:
        a=[rng.randrange(-10**120,10**120) for _ in range(n)]
    else:
        a=[0]*n
    m=rng.randrange(2,max(3, n*(n+1)+6))
    if (tuple(a),m) not in unique:
        check(a,m,extended=(t%3==0))
family_counts['seeded unique random cases']=len(unique)-sum(family_counts.values())

# Worst-case resource status, and benign budget early proof
budget_cases=[]
for a,m,K,steps in [([i*i for i in range(18)],2,16,0),([i*i for i in range(18)],5,16,3),([0]*18,2,10,0),([4,5,9],99,1,0)]:
    res=solve(a,m,K=K,max_operations=steps)
    assert res.status in ('RESOURCE_LIMIT','FEASIBLE','INFEASIBLE')
    assert verify(a,m,res.indices)
    if res.status=='INFEASIBLE':
        assert len(oracle(a,m))<K
    if res.status=='FEASIBLE':
        assert len(res.indices)>=K
    if res.status=='RESOURCE_LIMIT':
        assert len(res.indices)<K<=res.upper_bound
    budget_cases.append({'n':len(a),'m':m,'K':K,'max_operations':steps,**res.__dict__})

bench=[]
for n,m,kind in [(25,2,'convex'),(50,2,'convex'),(100,2,'convex'),(180,2,'convex'),
                 (25,20,'convex'),(50,20,'convex'),(100,20,'convex'),
                 (25,30,'convex'),(50,30,'convex'),(100,30,'convex'),
                 (100,20,'constant'),(100,20,'alternating'),(100,20,'random')]:
    if kind=='convex': a=[i*i for i in range(n)]
    elif kind=='constant': a=[0]*n
    elif kind=='alternating': a=[(-1)**i*(i*i+1) for i in range(n)]
    else:
        local=random.Random(541+n)
        a=[local.randrange(-10**20,10**20) for _ in range(n)]
    # Runtime without allocation instrumentation.
    times=[]
    for _ in range(3):
        start=time.perf_counter()
        out=solve(a,m)
        times.append(time.perf_counter()-start)
        assert out.status=='OPTIMAL' and verify(a,m,out.indices)
    if n <= 50:
        tracemalloc.start()
        out2=solve(a,m)
        heap_peak=tracemalloc.get_traced_memory()[1]
        tracemalloc.stop()
    else:
        out2=out
        heap_peak=None
    assert out2.indices==out.indices
    bench.append({'n':n,'m':m,'family':kind,'median_s':statistics.median(times),
                  'times_s':times,'peak_traced_heap_bytes':heap_peak,
                  'length':len(out.indices), 'counted_operations':out.operations})

report={'status':'PASS' if not failures else 'FAIL', 'unique_cases':len(unique),
        'optimization_executions':executions, 'decision_executions':threshold_execs,
        'duplicate_inputs':executions-len(unique), 'family_counts':family_counts,
        'seed':seed, 'failures':failures, 'benchmarks':bench,
        'budget_cases':budget_cases,
        'python':sys.version, 'platform':platform.platform(),
        'byteorder':sys.byteorder,
        'module_sha256':hashlib.sha256(open(os.path.join(base,'modconvex.py'),'rb').read()).hexdigest()}
with open(os.path.join(base,'report.json'),'w') as f: json.dump(report,f,indent=2)
print(json.dumps({k:report[k] for k in ('status','unique_cases','optimization_executions','decision_executions','duplicate_inputs','family_counts','seed','python','platform','module_sha256')},indent=2))
print('BENCHMARKS')
for b in bench: print(b)
print('BUDGET')
for b in budget_cases: print(b)
