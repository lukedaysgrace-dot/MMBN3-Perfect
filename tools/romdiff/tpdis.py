import os,sys
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import paths
import re,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
INI=os.path.join(paths.EXT,'TextPet/TextPet/plugins/mmbn3.ini')
def load():
    cmds=[];cur=None;par=None
    for line in open(INI,encoding='utf-8'):
        line=line.rstrip('\n')
        if line.startswith('#['): cur=None; par=None; continue
        if line.startswith('#') : continue
        if line.strip()=='[Command]': cur={'params':[]}; cmds.append(cur); par=None; continue
        if line.strip()=='[Parameter]':
            par={}
            if cur is not None: cur['params'].append(par)
            continue
        if line.strip().startswith('[') : cur=None; par=None; continue
        m=re.match(r'(\w+)\s*=\s*(.*)',line)
        if not m or cur is None: continue
        k,v=m.group(1),m.group(2)
        (par if par is not None else cur)[k]=v
    for c in cmds:
        c['maskb']=bytes.fromhex(c['mask']); c['baseb']=bytes.fromhex(c['base'])
    # longer base first
    cmds.sort(key=lambda c:-sum(1 for b in c['maskb'] if b))
    return cmds
CMDS=load()
from archives import cd
def param(c,p,data):
    o=p.get('offs','0'); 
    if '.' in o: by,bi=o.split('.'); by=int(by); bi=int(bi)
    else: by=int(o); bi=0
    bits=int(p.get('bits','8'))
    val=int.from_bytes(data[by:by+4].ljust(4,b'\0'),'little')>>bi
    return val&((1<<bits)-1)
def dis(s):
    i=0; out=[]; txt=''
    while i<len(s):
        b=s[i]
        if b<0xe7:
            txt+=cd.get(b,'?') if b<0x80 else '{%02x}'%b; i+=1; continue
        if b==0xe8: txt+='\\n'; i+=1; continue
        found=None
        for c in CMDS:
            n=len(c['maskb'])
            seg=s[i:i+n]
            if len(seg)<len(c['baseb']): continue
            if all((seg[j] if j<len(seg) else 0)&c['maskb'][j]==c['baseb'][j] for j in range(len(c['baseb']))):
                found=c;break
        if txt: out.append('"%s"'%txt); txt=''
        if not found: out.append('?%02x'%b); i+=1; continue
        n=len(found['maskb'])
        seg=s[i:i+n]
        ps=' '.join('%s=%s'%(p['name'],hex(param(found,p,seg))) for p in found['params'])
        out.append('%s(%s)'%(found['name'],ps)); i+=n
    if txt: out.append('"%s"'%txt)
    return out
if __name__=='__main__':
    from archives import *
    off=int(sys.argv[1],16)
    sb=get_arch(B,off,off in comp,uncomp.get(off))
    idx=[int(x) for x in sys.argv[2:]] if len(sys.argv)>2 else sorted(sb)
    seen={}
    for i in idx:
        s=sb[i]
        if not s: continue
        print('#%d (0x%x):'%(i,i)); print('   '+'\n   '.join(dis(s)))
