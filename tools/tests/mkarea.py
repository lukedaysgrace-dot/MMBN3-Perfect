import os,sys
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import paths
import sys;sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from emu import Emu
def make(rom,out,area=0x8c,sub=7):
    e=Emu(rom); e.run(10)
    e.load(os.path.join(paths.REPO,'MMBN3 - Perfect Version.ss3')); e.run(3)
    e.w8(0x2001884,area); e.w8(0x2001885,sub)
    seq=['START','A','B','B','B','B','B','B']
    for it in range(90):
        e.run(3,seq[it%len(seq)]); e.run(8)
    for i in range(30): e.run(3,'A'); e.run(10)
    e.run(3,'B'); e.run(30); e.run(3,'B'); e.run(30)
    e.save(out); return e
if __name__=='__main__': make(sys.argv[1],sys.argv[2])
