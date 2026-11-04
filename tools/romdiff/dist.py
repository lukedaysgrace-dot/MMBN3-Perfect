import os,sys
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import paths
import sys,re; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from common import *; from names import chip
import lz10
VER={'B':(B,{'shoppool':0x44bb0,'order':0x45130,'gmd':0x287f8,'num':0x478f8}),
     'W':(W,{'shoppool':0x44bc8,'order':0x45148,'gmd':0x28810,'num':0x47910})}
def drops(buf):
    s={}
    for i in range(0x100):
        a=0x160a8+i*0x38
        for k in range(28):
            v=h(buf,a+2*k)
            if v>>14==0 and v&0x1ff:
                s.setdefault(((v&0x1ff),(v>>9)&0x1f),set()).add(('drop',i,k))
    return s
def shops(buf,o):
    s={}
    a=o['shoppool']
    for k in range(0x5a0//8):
        t,c,i,code,_,p=struct.unpack_from('<BBHBBH',buf,a+8*k)
        if t==2: s.setdefault((i,code),set()).add(('shop',k//8,k%8,p))
    a=o['order']; k=0
    while True:
        t,c,i,code,_,p=struct.unpack_from('<BBHBBH',buf,a+8*k)
        if t==0: break
        if t==2: s.setdefault((i,code),set()).add(('order',k,p))
        k+=1
    return s
def gmd(buf,o):
    s={}
    base=o['gmd']
    md={0x10:[0,1,2],0x11:[0,1],0x12:[0,1],0x13:[0,1,3],0x14:[0,1,2,3,4,5,6],0x15:[0,1,2]}
    for area,subs in md.items():
        for sa in subs:
            sp=wd(buf,base+4*area)-0x08000000+4*sa
            ad=wd(buf,sp)-0x08000000
            data=bytes(lz10.gba_decompress(bytearray(buf[ad:ad+0x8000])))
            for m in re.finditer(rb'\xf1\x00\xfb\x04\x0f(.{32})',data,re.S):
                x=m.group(1)
                for j in range(0,32,2): s.setdefault((x[j],x[j+1]),set()).add(('gmd',area,sa,j//2))
    return s
def numtr(buf,o):
    s={}; a=o['num']; n=0
    while True:
        t,code,cid,enc=struct.unpack_from('<BBH8s',buf,a)
        if t==0xff: break
        if t==0: s.setdefault((cid,code),set()).add(('number',n,enc.hex()))
        a+=12; n+=1
    return s
res={}
for v,(buf,o) in VER.items():
    d={}
    for f in (drops(buf),shops(buf,o),gmd(buf,o),numtr(buf,o)):
        for k,x in f.items(): d.setdefault(k,set()).update(x)
    res[v]=d
import pickle; pickle.dump(res,open(os.path.join(paths.OUT,'dist.pkl','wb'))
onlyW=sorted(set(res['W'])-set(res['B'])); onlyB=sorted(set(res['B'])-set(res['W']))
print('W-only pairs',len(onlyW),' B-only pairs',len(onlyB))
for k in onlyW: print('W', chip(k[0],k[1]), sorted(res['W'][k])[:4])
