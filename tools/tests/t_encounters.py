# Random-encounter check (0x080146BC): vanilla Blue vs this ROM.
# Calls the game's own check with a forced map, step count and random seeds and
# counts how often it starts a battle. Outlier maps should drop to level 5;
# every other map must be unchanged.
import os,sys,random
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import paths, mkarea
from mm import *
state=os.path.join(paths.OUT,'p_area.raw')
mkarea.make(paths.OUT_ROM,state)
ENABLED='extra_encounter_rate.asm"' in open(os.path.join(paths.REPO,'main.asm')).read().split('// ----')[-1]
fails=0
def check(n,c,i=''):
    global fails; print(('PASS ' if c else 'FAIL ')+n,i); fails+= (not c)
def rate(rom,group,sub,row=12,n=2000):
    e=Emu(rom); e.run(10); e.load(state); e.run(3)
    s=e.r32(0x080004C0+0x78); r7=e.r32(0x080004C0+8)
    hits=0; rnd=random.Random(group*16+sub)
    for i in range(n):
        e.w32(0x02009800,rnd.getrandbits(32)); e.w8(r7+4,group); e.w8(r7+5,sub)
        e.w32(s+0x2c,64*row); e.w32(s+0x30,64*(row-1)); e.w32(r7+0x2c,0)
        e.call(0x080146BC|1)
        hits+= e.r32(r7+0x2c)!=0
    return hits/n
CURVE12={3:10,4:8,5:5,6:0}     # threshold/32 at the 12th check (table 0x0800D26C)
CURVE16={3:18,4:16,5:12,6:12}
cases=[(0x8C,13,3,5),(0x8C,14,3,5),(0x8C,15,3,5),(0x83,4,4,5),   # outliers
       (0x8C,7,5,5),(0x8A,2,5,5),(0x88,3,5,5),(0x8D,4,5,5),(0x81,2,6,6)]  # untouched
for g,sb,old,new in cases:
    if not ENABLED: new=old
    row=12 if old!=6 else 16; C=CURVE12 if row==12 else CURVE16
    v=rate(paths.BLUE,g,sb,row); p=rate(paths.OUT_ROM,g,sb,row)
    check('%X/%d check #%d: vanilla %.1f%% (lv%d, expect %.1f%%), this ROM %.1f%% (lv%d, expect %.1f%%)'%(
          g,sb,row,100*v,old,100*C[old]/32,100*p,new,100*C[new]/32),
          abs(v-C[old]/32)<0.035 and abs(p-C[new]/32)<0.035)
print('FAILS',fails)
