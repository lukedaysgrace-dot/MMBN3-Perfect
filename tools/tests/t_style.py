import os,sys
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import paths
import sys; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from emu import Emu
import collections
def run(rom):
    e=Emu(rom); e.run(10); e.load(os.path.join(paths.REPO,'Megaman Battle Network 3 - Blue Version (U).ss1')); e.run(2)
    sl=e.reg(10)
    res=collections.Counter()
    for trial in range(40):
        for i,v in enumerate([0,0,0,0,50,50,0]): e.w8(0x2000E60+i,v)
        e.w8(0x2001894,0x11)   # stored style ElecCust (type 2)
        e.w8(0x2001881,0x11)
        n,r=e.call(0x08015CA8)
        res[r]+=1
        e.run(1)
    return res
print('vanilla', dict(run(paths.BLUE)))
print('patched', dict(run(paths.OUT_ROM)))
