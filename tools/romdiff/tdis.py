import os,sys
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import paths
import capstone,sys
md=capstone.Cs(capstone.CS_ARCH_ARM,capstone.CS_MODE_THUMB)
b=open(paths.BLUE,'rb').read(); w=open(paths.WHITE,'rb').read()
def dis(buf,a,n,label):
    print('--',label)
    for ins in md.disasm(buf[a:a+n],0x08000000+a):
        print('  %08x: %-12s %s %s'%(ins.address,ins.bytes.hex(),ins.mnemonic,ins.op_str))
a=int(sys.argv[1],16); n=int(sys.argv[2],16); d=int(sys.argv[3],16) if len(sys.argv)>3 else 0
dis(b,a,n,'BLUE'); dis(w,a+d,n,'WHITE')
