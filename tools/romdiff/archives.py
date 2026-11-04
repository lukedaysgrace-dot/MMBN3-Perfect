import os,sys
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import paths
import sys,re; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from common import *
import lz10
src=open(os.path.join(paths.EXT,'ap/worlds/mmbn3/BN3RomUtils.py')).read()
uncomp=eval(re.search(r'ArchiveToSizeUncomp = (\{.*?\})',src).group(1))
comp=eval(re.search(r'ArchiveToSizeComp = (\{.*?\})',src).group(1))
refs=eval(re.search(r'ArchiveToReferences = (\{.*?\})\n',src).group(1))
cd={}
for l in re.findall(r"'(.)': (0x[0-9A-F]{2})",src): cd[int(l[1],16)]=l[0]
def text(bs):
    o=''
    for x in bs:
        o+= cd.get(x,'') if x<0x80 else ('\\n' if x==0xE8 else '{%02x}'%x)
    return o
def get_arch(buf,off,isc,size=None):
    if isc:
        assert buf[off]==0x10
        n=buf[off+1]|buf[off+2]<<8|buf[off+3]<<16
        data=bytes(lz10.gba_decompress(buf[off:off+0x10000+n]))[:n]
    else:
        data=buf[off:off+size]
    cnt=(data[0]|data[1]<<8)>>1
    offs=[data[2*i]|data[2*i+1]<<8 for i in range(cnt)]+[len(data)]
    scripts={}
    for i in range(cnt):
        # next offset: smallest offset > offs[i]
        nxt=min([o for o in offs if o>offs[i]]+[len(data)])
        scripts[i]=data[offs[i]:nxt]
    return scripts
def white_off(off):
    # use refs: read pointer in White at mapped ref location
    for r in refs.get(off,[]):
        rw=b2w(r)
        p=wd(W,rw)
        if 0x08000000<=p<0x09000000: return p-0x08000000
    return b2w(off)
def gives(s):
    out=[]
    for m in re.finditer(rb'\xf6\x10(..)(.)(.)',s,re.S):
        cid=m.group(1)[0]|m.group(1)[1]<<8; out.append((cid,m.group(2)[0],m.group(3)[0]))
    return out
