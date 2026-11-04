import os,sys
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import paths
import numpy as np, pickle, struct, bisect
b=open(paths.BLUE,'rb').read(); w=open(paths.WHITE,'rb').read()
segs=pickle.load(open(os.path.join(paths.OUT,'segs.pkl','rb'))  # (bstart,bend,delta,count)
# LIS over segments by white start
segs=sorted(segs)
ws=[s[0]+s[2] for s in segs]
# weighted LIS by count (DP O(n^2) fine for ~600)
n=len(segs); best=[s[3] for s in segs]; prev=[-1]*n
for i in range(n):
    for j in range(i):
        if segs[j][1]<=segs[i][0]+0 and segs[j][1]+segs[j][2]<=ws[i] and best[j]+segs[i][3]>best[i]:
            best[i]=best[j]+segs[i][3]; prev[i]=j
i=max(range(n),key=lambda k:best[k]); chain=[]
while i>=0: chain.append(segs[i]); i=prev[i]
chain=chain[::-1]
# extend each segment's region and build piecewise map
# map blue offset->white: find seg with start<=x; use its delta
starts=[c[0] for c in chain]
def b2w(x):
    k=bisect.bisect_right(starts,x)-1
    if k<0: return x
    return x+chain[k][2]
pickle.dump(chain,open(os.path.join(paths.OUT,'chain.pkl','wb'))
# Diff regions
out=[]
for k in range(len(chain)):
    s,e,d,c=chain[k]
    ne = chain[k+1][0] if k+1<len(chain) else len(b)
    nd = chain[k+1][2] if k+1<len(chain) else d
    # aligned region from s to ne with delta d if next delta equal else structural gap
    region_end = ne if nd==d else e
    out.append(('A',s,region_end,d))
    if nd!=d:
        out.append(('G',e,ne,d,nd))  # blue [e,ne) vs white [e+d, ne+nd)
pickle.dump(out,open(os.path.join(paths.OUT,'regions.pkl','wb'))
print(len(chain))
