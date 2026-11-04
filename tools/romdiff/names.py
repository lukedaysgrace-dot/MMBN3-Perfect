import os,sys
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import paths
names=open(os.path.join(paths.EXT,'MMBN3-Randomizer/src/data/chip_names.txt')).read().split('\n')
CS='ABCDEFGHIJKLMNOPQRSTUVWXYZ*'
def chip(cid,code=None):
    n=names[cid-1] if 0<cid<=len(names) else '#%x'%cid
    if code is None: return n
    return n+' '+(CS[code] if code<27 else '?%x'%code)
