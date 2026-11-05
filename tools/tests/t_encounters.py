# Random-encounter check (0x080146BC): per-check chance, vanilla Blue vs this ROM.
# Calls the game's own check with a forced step count and random seeds in the
# BowlMan Undernet area (tier 5) and counts how often it starts a battle.
import os,sys,random
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import paths, mkarea
from mm import *
state=os.path.join(paths.OUT,'p_area.raw')
mkarea.make(paths.OUT_ROM,state)
HALVED = os.path.exists(os.path.join(paths.REPO,'patches','extra_encounter_rate.asm')) and \
         'extra_encounter_rate.asm"' in open(os.path.join(paths.REPO,'main.asm')).read().split('// ----')[-1]
fails=0
def check(n,c,i=''):
    global fails; print(('PASS ' if c else 'FAIL ')+n,i); fails+= (not c)
def rate(rom,row,n=3000):
    e=Emu(rom); e.run(10); e.load(state); e.run(3)
    s=e.r32(0x080004C0+0x78); r7=e.r32(0x080004C0+8)
    hits=0; rnd=random.Random(row)
    for i in range(n):
        e.w32(0x02009800,rnd.getrandbits(32))
        e.w32(s+0x2c,64*row); e.w32(s+0x30,64*(row-1)); e.w32(r7+0x2c,0)
        e.call(0x080146BC|1)
        hits+= e.r32(r7+0x2c)!=0
    return hits/n
T={8:1,12:5,16:12}                       # tier-5 thresholds out of 32 (table 0x0800D26C)
for row,t in T.items():
    v=rate(paths.BLUE,row); p=rate(paths.OUT_ROM,row)
    want=t/64 if HALVED else t/32
    check('check #%d: vanilla %.1f%% (expect %.1f%%), this ROM %.1f%% (expect %.1f%%)'%(row,100*v,100*t/32,100*p,100*want),
          abs(v-t/32)<0.03 and abs(p-want)<0.03)
print('FAILS',fails)
