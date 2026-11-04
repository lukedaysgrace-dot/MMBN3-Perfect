import os,sys
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import paths
import sys;sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from emu import Emu
def setpos(e,x,y):
    for a in (0x2009584,0x2009590): e.w32(a,x<<16); e.w32(a+4,(y&0xffff)<<16 if y>=0 else ((y<<16)&0xffffffff))
def open_area(rom,x=0xa0,y=0x10):
    e=Emu(rom); e.run(10)
    e.load(os.path.join(paths.OUT,'area8c7.raw')); e.run(3)
    setpos(e,x,y); e.run(30)
    return e
import ctypes
from emu import L,K
def keys(*ks):
    k=0
    for x in ks: k|=K[x]
    return k
def hold(e,ks,n):
    L.h_frames(n,keys(*ks))
def talk_from(e,x,y,dirkeys,walk=6):
    setpos(e,x,y); e.run(10)
    hold(e,dirkeys,walk); e.run(4)
    hold(e,['A'],2); e.run(40)
