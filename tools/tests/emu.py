import os,sys
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import paths
import ctypes, os
L=ctypes.CDLL(os.path.join(os.path.dirname(os.path.abspath(__file__)),'libharness.so'))
for n in ['h_r8','h_r16','h_r32','h_pc','h_reg']: getattr(L,n).restype=ctypes.c_uint
L.h_vbuf.restype=ctypes.c_void_p
K=dict(A=1,B=2,SELECT=4,START=8,RIGHT=16,LEFT=32,UP=64,DOWN=128,R=256,L=512)
class Emu:
    def __init__(s,rom,sav=''):
        r=L.h_open(rom.encode(),sav.encode()); assert r==0,r
    def run(s,n=1,*keys):
        k=0
        for x in keys: k|=K[x]
        L.h_frames(n,k)
    def press(s,key,hold=2,after=10):
        s.run(hold,key); s.run(after)
    r8=staticmethod(lambda a:L.h_r8(a)); r16=staticmethod(lambda a:L.h_r16(a)); r32=staticmethod(lambda a:L.h_r32(a))
    w8=staticmethod(lambda a,v:L.h_w8(a,v)); w16=staticmethod(lambda a,v:L.h_w16(a,v)); w32=staticmethod(lambda a,v:L.h_w32(a,v))
    def load(s,p): return L.h_loadstate(p.encode())
    def save(s,p): return L.h_savestate(p.encode())
    def shot(s,p):
        from PIL import Image
        buf=(ctypes.c_uint32*(240*160)).from_address(L.h_vbuf())
        im=Image.frombuffer('RGBA',(240,160),bytes(buf),'raw','RGBA',0,1).convert('RGB')
        im.save(p)
    def rd(s,a,n): return bytes(L.h_r8(a+i) for i in range(n))
L.h_call.restype=ctypes.c_long
L.h_call.argtypes=[ctypes.c_uint]*6+[ctypes.c_long]
def call(fn,r0=0,r1=0,r2=0,r3=0,maxsteps=2000000):
    ime=L.h_r16(0x4000208); L.h_w16(0x4000208,0)
    n=L.h_call(fn,r0,r1,r2,r3,0x08000000,maxsteps)
    L.h_w16(0x4000208,ime)
    return n, L.h_lastr0()
Emu.call=staticmethod(call)
Emu.reg=staticmethod(lambda i:L.h_reg(i))
Emu.setreg=staticmethod(lambda i,v:L.h_setreg(i,v))
L.h_cpsr.restype=ctypes.c_uint
Emu.cpsr=staticmethod(lambda: L.h_cpsr())
Emu.zflag=staticmethod(lambda: bool(L.h_cpsr() & (1<<30)))
def _save(s,p): return L.h_savefile(p.encode())
def _load(s,p):
    if p.endswith('.raw'): return L.h_loadfile(p.encode())
    return L.h_loadstate(p.encode())
Emu.save=_save; Emu.load=_load
L.h_watch.restype=ctypes.c_long
L.h_watch.argtypes=[ctypes.c_uint,ctypes.c_long,ctypes.POINTER(ctypes.c_uint),ctypes.c_int]
def watch(addr,maxsteps=3000000,maxpcs=40):
    buf=(ctypes.c_uint*maxpcs)()
    k=L.h_watch(addr,maxsteps,buf,maxpcs)
    return [(buf[i],buf[i+1]) for i in range(0,k,2)]
Emu.watch=staticmethod(watch)

L.h_lastr0.restype=ctypes.c_uint; L.h_lastcpsr.restype=ctypes.c_uint
Emu.zflag=staticmethod(lambda: bool(L.h_lastcpsr() & (1<<30)))
