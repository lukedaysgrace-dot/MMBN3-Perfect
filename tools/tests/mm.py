import os,sys
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import paths
import sys;sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from area import *
ROM=paths.OUT_ROM
def open_p(x,y,state=os.path.join(paths.OUT,'p_area.raw')):
    e=Emu(ROM); e.run(10); e.load(state); e.run(3); setpos(e,x,y); e.run(30); return e
def flag(e,f): return (e.r8(0x2000030+(f>>3))>>(7-(f&7)))&1
def flags(e): return {hex(f):flag(e,f) for f in (0x125e,0x12f,0x130,0x131,0x132,0x1f0,0x1f1,0x1f2,0x1f3,0x15b,0x15c)}
def start_mm_battle(e):
    talk_from(e,0x76-0x18,-0x1c,['UP','RIGHT'],8)
    e.run(90); hold(e,['A'],2); e.run(90); hold(e,['A'],2); e.run(150)
    hold(e,['LEFT'],3); e.run(15)
    hold(e,['A'],2); e.run(20)
def win_battle(e, hpaddr=0x2037368, frames_max=4000):
    # custom screen: confirm, then shoot until the enemy is gone
    seq=['START','A','B','B','B','B','B','B']
    for it in range(120):
        if e.r16(hpaddr)>1: e.w16(hpaddr,1)
        e.run(3,seq[it%len(seq)]); e.run(8)
    for i in range(30): e.run(3,'A'); e.run(10)
