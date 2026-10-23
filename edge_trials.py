import sys, os, itertools, random, time, json, statistics
sys.path.insert(0,os.path.dirname(__file__))
from edge_dp import solve_edge
from modconvex import oracle, solve, verify
count=0
for n in range(6):
 for a in itertools.product((-1,0,1),repeat=n):
  for m in range(2,n*(n+1)//2+4):
   exp=oracle(a,m)
   got=solve_edge(a,m)
   assert got==exp,(a,m,exp,got)
   count+=1
rng=random.Random(7919)
for rep in range(400):
 n=rng.randrange(0,13)
 a=[rng.choice([rng.randrange(-10**50,10**50),rng.randrange(-5,6)]) for i in range(n)]
 m=rng.randrange(2,max(3,n*(n+1)+10))
 got=solve_edge(a,m)
 exp=oracle(a,m)
 assert got==exp,(a,m,exp,got)
 count+=1
bench=[]
for n,m,kind in [(30,2,'convex'),(50,2,'convex'),(100,2,'convex'),(50,10,'convex'),(100,10,'convex'),(100,20,'constant')]:
 a=[i*i for i in range(n)] if kind=='convex' else [0]*n
 for label, fn in [('edge', lambda:solve_edge(a,m)), ('sweep',lambda:solve(a,m).indices)]:
  times=[]
  for _ in range(3):
   t=time.perf_counter(); sol=fn(); times.append(time.perf_counter()-t)
  assert verify(a,m,sol)
  bench.append({'n':n,'m':m,'family':kind,'algorithm':label,'median_s':statistics.median(times),'raw_s':times,'length':len(sol)})
with open(os.path.join(os.path.dirname(__file__),'edge_report.json'),'w') as f:json.dump({'unique_cases':count,'seed':7919,'benchmarks':bench},f,indent=2)
print('PASS',count,'oracle matched')
for v in bench:print(v)
