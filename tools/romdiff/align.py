import os,sys
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import paths
import numpy as np, sys, pickle
b=np.fromfile(paths.BLUE,dtype=np.uint8); w=np.fromfile(paths.WHITE,dtype=np.uint8)
K=16
def keys(a):
    n=len(a)-K+1
    v=np.zeros(n,dtype=np.uint64)
    for i in range(K):
        v = v*np.uint64(1099511628211) ^ a[i:i+n].astype(np.uint64)
    return v
kb=keys(b); kw=keys(w)
def uniq(k):
    vals,idx,cnt=np.unique(k,return_index=True,return_counts=True)
    m=cnt==1
    return vals[m],idx[m]
vb,ib=uniq(kb); vw,iw=uniq(kw)
common,xb,xw=np.intersect1d(vb,vw,return_indices=True)
pb=ib[xb]; pw=iw[xw]
o=np.argsort(pb); pb=pb[o]; pw=pw[o]
# keep monotone (longest increasing subsequence approx: drop non-monotonic using delta continuity)
d=pw.astype(np.int64)-pb.astype(np.int64)
np.save(os.path.join(paths.OUT,'anch.npy',np.stack([pb,pw]))
print(len(pb))
# summarize delta segments
segs=[]
s=0
for i in range(1,len(pb)):
    if d[i]!=d[i-1] or pb[i]-pb[i-1]>4096:
        segs.append((pb[s],pb[i-1]+K,d[s],i-s)); s=i
segs.append((pb[s],pb[-1]+K,d[s],len(pb)-s))
big=[x for x in segs if x[3]>=8]
print(len(segs),len(big))
pickle.dump(big,open(os.path.join(paths.OUT,'segs.pkl','wb'))
for x in big[:400]: print(hex(x[0]),hex(x[1]),hex(x[2]) if x[2]>=0 else '-'+hex(-x[2]),x[3])
