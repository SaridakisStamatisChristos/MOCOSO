import sys, time, statistics, random, json, os, resource, tracemalloc, platform, hashlib
sys.path.insert(0,os.path.dirname(__file__))
from modconvex import solve, oracle, cubic_dp, verify
records=[]
for n,m in [(8,2),(10,5),(12,5),(14,10)]:
 a=[i*i for i in range(n)]
 for label, fn in [('sweep',lambda:solve(a,m).indices),('forward_cubic',lambda:cubic_dp(a,m)),('exhaustive',lambda:oracle(a,m))]:
  times=[]
  for rep in range(3):
   st=time.perf_counter();sol=fn();times.append(time.perf_counter()-st)
  assert verify(a,m,sol)
  records.append({'comparison':'alternatives','n':n,'m':m,'algorithm':label,'median_s':statistics.median(times),'raw_s':times})
for n,h in [(25,8),(50,10),(100,12),(100,15)]:
 U=n*(n+1)//2
 m=U-h
 a=[i*i for i in range(n)]
 for cut in [0,15]:
  if cut==0 and n>25: continue
  st=time.perf_counter();sol=solve(a,m,complement_cutoff=cut);secs=time.perf_counter()-st
  assert sol.status=='OPTIMAL' and verify(a,m,sol.indices)
  records.append({'comparison':'complement','n':n,'m':m,'h':h,'cutoff':cut,'algorithm':'sweep' if cut==0 else 'complement','elapsed_s':secs,'length':len(sol.indices)})
for n,m in [(50,20),(100,30),(180,2)]:
 a=[i*i for i in range(n)]
 before=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
 sol=solve(a,m)
 after=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
 records.append({'comparison':'memory','n':n,'m':m,'rss_hiwater_before_kib':before,'rss_hiwater_after_kib':after,'DP_theoretical_array_bytes':8*(n*(n-1)//2)*m,'array_itemsize':__import__('array').array('i').itemsize})
# The below checks are deliberately not exhaustive resource-usage measurements.
a=[i*i for i in range(50)]
for lims in [{'max_operations':0},{'max_seconds':0},{'max_heap_bytes':1000}]:
 result=solve(a,11,K=49,**lims)
 assert result.status=='RESOURCE_LIMIT' and verify(a,11,result.indices)
 records.append({'comparison':'limit','budget':lims,'status':result.status,'lower_bound':result.lower_bound,'upper_bound':result.upper_bound,'operations':result.operations,'reason':result.reason})
with open(os.path.join(os.path.dirname(__file__),'extra_report.json'),'w') as f: json.dump(records,f,indent=2)
for r in records:print(r)
