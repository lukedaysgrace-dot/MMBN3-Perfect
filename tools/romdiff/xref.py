import os,sys
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import paths
import sys; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from common import *
def ldr_users(lit, buf=B, lo=0, hi=0x140000):
    out=[]
    for a in range(max(lo,lit-1024)&~1, min(lit,hi), 2):
        x=h(buf,a)
        if (x&0xF800)==0x4800:
            t=((a+4)&~3)+(x&0xff)*4
            if t==lit: out.append(a)
    return out
def bl_callers(target, buf=B, lo=0, hi=0x140000):
    out=[]
    for a in range(lo,hi,2):
        hi_=h(buf,a); lo_=h(buf,a+2)
        if (hi_&0xF800)==0xF000 and (lo_&0xF800)==0xF800:
            off=((hi_&0x7FF)<<12)|((lo_&0x7FF)<<1)
            if off&0x400000: off-=0x800000
            if a+4+off==target: out.append(a)
    return out
if __name__=='__main__':
    for x in sys.argv[1:]:
        v=int(x,16); print(x,'ldr users',[hex(a) for a in ldr_users(v)])
