import os,sys
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import paths
import pickle,bisect,struct
B=open(paths.BLUE,'rb').read(); W=open(paths.WHITE,'rb').read()
chain=pickle.load(open(os.path.join(paths.OUT,'chain.pkl','rb'))
starts=[c[0] for c in chain]
def b2w(x):
    k=bisect.bisect_right(starts,x)-1
    return x+(chain[k][2] if k>=0 else 0)
wst=sorted([(c[0]+c[2],c) for c in chain])
wstarts=[x[0] for x in wst]
def w2b(x):
    k=bisect.bisect_right(wstarts,x)-1
    return x-(wst[k][1][2] if k>=0 else 0)
cl=pickle.load(open(os.path.join(paths.OUT,'clusters.pkl','rb'))
def h(buf,a): return struct.unpack_from('<H',buf,a)[0]
def wd(buf,a): return struct.unpack_from('<I',buf,a)[0]
