import os,sys
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import paths, mkarea
from mm import *
state=os.path.join(paths.OUT,'p_area.raw')
mkarea.make(paths.OUT_ROM,state)
fails=0
def check(n,c,i=''):
    global fails; print(('PASS ' if c else 'FAIL ')+n,i); fails+= (not c)
e=open_p(0x98,0x10,state)
objs=[(e.r16(0x2004560+k*0xc4+0x3c),e.r8(0x2004560+k*0xc4+0x1c)) for k in range(8)]
check('MistMan NPC spawned (sprite 0x59, text 9)',(0x59,9) in objs)
check('BowlMan NPC still spawned (sprite 0x58, text 10)',(0x58,0x0a) in objs)
def setf(f,v):
    a=0x2000030+(f>>3); b=0x80>>(f&7); e.w8(a,(e.r8(a)|b) if v else (e.r8(a)&~b))
# BowlMan progress (1,0,0), MistMan progress (0,0,0)
e=open_p(0x76-0x18,-0x1c,state)
for f,v in ((0x12f,1),(0x130,0),(0x131,0),(0x1f0,0),(0x1f1,0),(0x1f2,0)): setf(f,v)
start_mm_battle(e)
for i in range(4): hold(e,['A'],2); e.run(70)
f0=flags(e)
check('White mode active during MistMan talk/battle',f0['0x125e']==0 and f0['0x15c']==1, f0)
check('MistMan battle loaded (HP 1000 enemy)', e.r16(0x2037368)==1000, e.r16(0x2037368))
for i in range(200):
    if e.r16(0x2037368)>1: e.w16(0x2037368,1)
    k=['START','A','B','B','B','A'][i%6]
    e.run(2,k); e.run(28)
    if flag(e,0x125e)==1: break
e.run(60)
f1=flags(e)
check('Blue mode restored after the fight',f1['0x125e']==1,f1)
check('BowlMan progress unchanged',(f1['0x12f'],f1['0x130'],f1['0x131'])==(1,0,0),f1)
check('MistMan V1 recorded separately',(f1['0x1f0'],f1['0x1f1'],f1['0x1f2'])==(1,0,0),f1)
print('FAILS',fails)
