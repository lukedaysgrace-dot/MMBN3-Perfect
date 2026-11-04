import os,sys
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import paths
import sys; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from emu import Emu
import struct
ROM=sys.argv[1] if len(sys.argv)>1 else paths.OUT_ROM
STATE=os.path.join(paths.REPO,'Megaman Battle Network 3 - Blue Version (U).ss1')
e=Emu(ROM); e.run(10); e.load(STATE); e.run(2)
rom=open(ROM,'rb').read()
fails=0
def check(name,cond,info=''):
    global fails
    print(('PASS ' if cond else 'FAIL ')+name+(' '+str(info) if info else ''))
    if not cond: fails+=1
# --- legality
names={0x12e:'DeltaRay',0x12f:'FoldrBak',0x130:'NavRcycl',0x131:'AlphArmS',0x132:'Bass',0x133:'Serenade',0x134:'Balance',0x135:'DarkAura',0x136:'AlphArmO',0x137:'Bass+',0x138:'BassGS',0x1:'Cannon'}
lib=0x2000330
for flagset in (False,True):
    # flag 0x1938 = byte 0x2000357 bit 0x80
    b=e.r8(0x2000357); e.w8(0x2000357,(b|0x80) if flagset else (b&0x7f))
    for c,n in names.items():
        steps,r0=e.call(0x08001A48,c)
        hidden=e.zflag()
        expect_hidden = (c in (0x132,0x137)) and flagset
        check('legality %s BassGSflag=%d'%(n,flagset), hidden==expect_hidden and r0==c, 'hidden=%s r0=%x'%(hidden,r0))
    e.w8(0x2000357,b)
# --- drop table hook
blue_tbl=0x080160a8
white=None
cnt={'B':0,'W':0}
for bc in range(200):
    e.w16(0x2001DCA,bc)
    steps,p=e.call(0x08016098,0x05)
    if p==blue_tbl+5*0x38: cnt['B']+=1
    else:
        cnt['W']+=1; white=p-5*0x38
    steps,p2=e.call(0x08016098,0x05)
    check('drop table stable within battle %d'%bc,p2==p) if bc<3 else None
check('drop mix both tables used',cnt['B']>60 and cnt['W']>60,cnt)
W=open(paths.WHITE,'rb').read()
_ex2=lambda d: d[:0xd5*0x38]+d[0xd7*0x38:]
if white:
    off=white-0x08000000
    check('white drop table matches White ROM (except optional Punk rows)', _ex2(rom[off:off+0x3570])==_ex2(W[0x160a8:0x160a8+0x3570]))
    # BassGS row in white table = Bass X
    v=struct.unpack_from('<H',rom,off+0xf2*0x38)[0]
    check('BassGS white row drops Bass X', v==0x2f32, hex(v))
_b=open(paths.BLUE,'rb').read()
_ex=lambda d: d[:0xd5*0x38]+d[0xd7*0x38:]   # Punk alpha/beta rows are changed by the optional Punk patch
check('blue drop table untouched (except optional Punk rows)', _ex(rom[0x160a8:0x160a8+0x3570])==_ex(_b[0x160a8:0x160a8+0x3570]))
# --- art
for i,c in enumerate(range(0x130,0x135)):
    a=0x11510+c*0x20
    img,pal=struct.unpack_from('<II',rom,a+0x18)
    src=0x6F4460+i*0x720
    check('art %s'%names[c], rom[img-0x8000000:img-0x8000000+0x700]==W[src:src+0x700] and rom[pal-0x8000000:pal-0x8000000+0x20]==W[src+0x700:src+0x720])
# --- AlphArm double give: pack counts 0x2001F60 + chip*0x12
def pack(c): return bytes(e.r8(0x2001F60+c*0x12+i) for i in range(6))
a0,s0=pack(0x136),pack(0x131)
import re
# find GiveBothAlphArms address via bl at 0x47e88
hi,lo=struct.unpack_from('<HH',rom,0x47e88)
off=((hi&0x7ff)<<12)|((lo&0x7ff)<<1)
if off&0x400000: off-=0x800000
fn=0x08047e88+4+off
steps,_=e.call(fn)
a1,s1=pack(0x136),pack(0x131)
check('AlphArm: gives AlphArmO',sum(a1)==sum(a0)+1,(a0.hex(),a1.hex()))
check('AlphArm: gives AlphArmS',sum(s1)==sum(s0)+1,(s0.hex(),s1.hex()))
# --- shops: run InitShops (0x08045BD0) and inspect RAM
e.call(0x08045BD0)
def slot(shop,j):
    a=0x20035E0+(shop*8+j)*8
    return struct.unpack('<BBHBBH',bytes(e.r8(a+i) for i in range(8)))
check('UN2 frag shop has FoldrBak',slot(10,5)[2]==0x12f)
check('UN2 frag shop has NavRcycl',slot(10,6)[2]==0x130 and slot(10,6)[3]==26, slot(10,6))
check('UN6 frag shop DeltaRay/Balance',slot(12,6)[2]==0x12e and slot(12,7)[2]==0x134)
check('Chip order AirSwrd R', slot(22,312)[2]==0x2a and slot(22,312)[3]==17, slot(22,312))
# --- optional extras
import struct as _s
def _blt(a):
    hi,lo=_s.unpack_from('<HH',rom,a); o=((hi&0x7ff)<<12)|((lo&0x7ff)<<1)
    if o&0x400000: o-=0x800000
    return 0x08000000+a+4+o
pa=_blt(0x12d93a); ea=_blt(0x2a392)
check('Press usable when owned', e.call(pa)[1]==1)
check('EngyChng usable when owned', e.call(ea)[1]==1)
sv=e.r32(0x2001ad0); e.w32(0x2001ad0,0)
check('Press not usable when not owned/equipped', e.call(pa)[1]==0)
e.w32(0x2001ad0,sv)
c0=e.call(0x08001794)[1]
e.call(0x08011280,0x110,15,1)
check('Punk P counts as a Mega in the library', e.call(0x08001794)[1]==c0+1)
check('anti-cheat verify still passes with Punk', e.call(0x08007ECA)[1]==1)
pa_row=[_s.unpack_from('<H',rom,0x160a8+0xd5*0x38+2*k)[0] for k in range(28)]
pb_row=[_s.unpack_from('<H',rom,0x160a8+0xd6*0x38+2*k)[0] for k in range(28)]
van=open(paths.BLUE,'rb').read()
va=[_s.unpack_from('<H',van,0x160a8+0xd5*0x38+2*k)[0] for k in range(28)]
check('Punk alpha: Punk P only in top busting slots 10-13', all((pa_row[k]==0x1f10) == (k%14>=10) for k in range(28)) and all(pa_row[k]==va[k] for k in range(28) if k%14<10), [hex(x) for x in pa_row[:14]])
check('Punk beta: Punk P in slots 5,7,9-13', all((pb_row[k]==0x1f10) == (k%14 in (5,7,9,10,11,12,13)) for k in range(28)), [hex(x) for x in pb_row[:14]])
print('FAILS',fails)
