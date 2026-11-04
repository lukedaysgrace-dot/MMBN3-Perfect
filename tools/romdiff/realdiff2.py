import os,sys
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import paths
import pickle, struct, bisect
b=open(paths.BLUE,'rb').read(); w=open(paths.WHITE,'rb').read()
chain=pickle.load(open(os.path.join(paths.OUT,'chain.pkl','rb'))
regions=pickle.load(open(os.path.join(paths.OUT,'regions.pkl','rb'))
starts=[c[0] for c in chain]
def b2w(x):
    k=bisect.bisect_right(starts,x)-1
    return x+(chain[k][2] if k>=0 else 0)
def h(buf,a): return struct.unpack_from('<H',buf,a)[0]
def bl_target(buf,a):
    hi=h(buf,a); lo=h(buf,a+2)
    if (hi&0xF800)==0xF000 and (lo&0xF800)==0xF800:
        off=((hi&0x7FF)<<12)|((lo&0x7FF)<<1)
        if off&0x400000: off-=0x800000
        return a+4+off
    return None
def ptr_ok(a,d):
    a&=~3
    bw=struct.unpack_from('<I',b,a)[0]; ww=struct.unpack_from('<I',w,a+d)[0]
    return 0x08000000<=bw<0x09000000 and 0x08000000<=ww<0x09000000 and abs(b2w(bw-0x08000000)+0x08000000-ww)<=1
def bl_ok(i,d):
    # i inside a bl pair starting at i&~1 or (i&~1)-2
    for a in ((i&~1),(i&~1)-2):
        tb=bl_target(b,a); tw=bl_target(w,a+d)
        if tb is not None and tw is not None and b2w(tb)==tw: return True
    return False
diffs=[]
for r in regions:
    if r[0]!='A': diffs.append(r); continue
    _,s,e,d=r
    i=s
    while i<e:
        if b[i]!=w[i+d]:
            if ptr_ok(i,d): i=(i&~3)+4; continue
            if bl_ok(i,d): i+=1; continue
            diffs.append(('d',i,d))
        i+=1
cl=[]
for x in diffs:
    if x[0]=='G': cl.append(x); continue
    if cl and cl[-1][0]=='D' and x[1]-cl[-1][2]<=8 and cl[-1][3]==x[2]: cl[-1]=('D',cl[-1][1],x[1]+1,x[2])
    else: cl.append(('D',x[1],x[1]+1,x[2]))
pickle.dump(cl,open(os.path.join(paths.OUT,'clusters.pkl','wb'))
for c in cl:
    if c[0]=='D': print('D %06x-%06x (w %06x) len %d'%(c[1],c[2],c[1]+c[3],c[2]-c[1]))
    else: print('G b %06x-%06x  w %06x-%06x  blen %d wlen %d'%(c[1],c[2],c[3],c[4],c[2]-c[1],c[4]-c[3]))
