import json,subprocess,glob,os,concurrent.futures as cf
from urllib.parse import urlsplit
os.chdir(os.path.dirname(os.path.abspath(__file__)))
def norm(u):
    s=urlsplit(u.strip()); return s.netloc.lower().removeprefix('www.')+s.path.rstrip('/').lower()
def resolve(u):
    if 'google.com/goto' not in u: return u
    r=subprocess.run(['curl','-sL','-m','20','-o','/dev/null','-w','%{url_effective}',u],capture_output=True,text=True); return r.stdout or u
def urls(f):
    d=json.load(open(f))
    if f.startswith('dfs'): return [i['url'] for i in d[0]['items'] if i['type']=='organic'][:10]
    if f.startswith('mrs'): return [i.get('link','') for i in d.get('organic',[])][:10]
    def find(o):
        if isinstance(o,dict):
            for k in ('organic','organic_results','organicResults','results'):
                if isinstance(o.get(k),list) and o[k] and isinstance(o[k][0],dict): return o[k]
            for v in o.values():
                x=find(v)
                if x: return x
        if isinstance(o,list):
            for v in o:
                x=find(v)
                if x: return x
    rows=find(d) or []
    return [r.get('link') or r.get('url') or '' for r in rows][:10]
truth=json.load(open('truth.json'))
files=sorted(glob.glob('*_r*_*.json'))
L={f:urls(f) for f in files}
allu={u for v in L.values() for u in v}
with cf.ThreadPoolExecutor(6) as ex: res=dict(zip(allu,ex.map(resolve,allu)))
print(f"{'file':16} n  ∩truth(of top)  unresolved")
for f in files:
    k=f.split('_')[-1][0]; got=[norm(res[u]) for u in L[f]]; t=truth[k]
    print(f"{f:16} {len(got):2} {len(set(got)&set(t)):2}/{len(t)}  {sum(x.startswith('google.com') for x in got)}")
