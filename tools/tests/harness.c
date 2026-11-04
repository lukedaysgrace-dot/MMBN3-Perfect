#include <mgba/core/core.h>
#include <mgba/core/serialize.h>
#include <mgba/core/config.h>
#include <mgba-util/vfs.h>
#include <mgba/internal/arm/arm.h>
#include <mgba/internal/gba/gba.h>
#include <stdlib.h>
#include <string.h>
#include <fcntl.h>
#include <mgba/internal/arm/isa-inlines.h>
static struct mCore* core;
#include <mgba/core/log.h>
static void nolog(struct mLogger* l,int c,enum mLogLevel lv,const char* f,va_list a){}
static struct mLogger quiet={.log=nolog};
static color_t* vbuf;
int h_open(const char* rom, const char* sav){
  mLogSetDefaultLogger(&quiet); core = mCoreFind(rom); if(!core) return -1;
  core->init(core);
  mCoreInitConfig(core, NULL);
  struct mCoreOptions opts = { .useBios = false, .skipBios = true, .volume=0 };
  mCoreConfigLoadDefaults(&core->config, &opts);
  mCoreLoadConfig(core);
  unsigned w,h; core->desiredVideoDimensions(core,&w,&h);
  vbuf = malloc(w*h*BYTES_PER_PIXEL); core->setVideoBuffer(core, vbuf, w);
  if(!mCoreLoadFile(core, rom)) return -2;
  if(sav && *sav){ struct VFile* vf=VFileOpen(sav,O_RDWR|O_CREAT); if(vf) core->loadSave(core,vf);} 
  core->reset(core);
  return 0;
}
void h_frames(int n, int keys){ core->setKeys(core,keys); for(int i=0;i<n;i++) core->runFrame(core); }
unsigned h_r8(unsigned a){ return core->rawRead8(core,a,-1); }
unsigned h_r16(unsigned a){ return core->rawRead16(core,a,-1); }
unsigned h_r32(unsigned a){ return core->rawRead32(core,a,-1); }
void h_w8(unsigned a,unsigned v){ core->rawWrite8(core,a,-1,v); }
void h_w16(unsigned a,unsigned v){ core->rawWrite16(core,a,-1,v); }
void h_w32(unsigned a,unsigned v){ core->rawWrite32(core,a,-1,v); }
int h_loadstate(const char* p){ struct VFile* vf=VFileOpen(p,O_RDONLY); if(!vf) return -1; int r=mCoreLoadStateNamed(core,vf,SAVESTATE_SAVEDATA*0|SAVESTATE_RTC); vf->close(vf); return r; }
int h_savestate(const char* p){ struct VFile* vf=VFileOpen(p,O_WRONLY|O_CREAT|O_TRUNC); if(!vf) return -1; int r=mCoreSaveStateNamed(core,vf,0); vf->close(vf); return r; }
void* h_vbuf(void){ return vbuf; }
unsigned h_pc(void){ struct ARMCore* cpu=core->cpu; return cpu->gprs[15]; }
unsigned h_reg(int i){ struct ARMCore* cpu=core->cpu; return cpu->gprs[i]; }
void h_setreg(int i, unsigned v){ struct ARMCore* cpu=core->cpu; cpu->gprs[i]=v; if(i==15){ /* refill pipeline */ cpu->gprs[15]=v; ARMWritePC(cpu);} }
int h_thumb(void){ struct ARMCore* cpu=core->cpu; return cpu->executionMode; }
/* call a Thumb function: sets r0-r3, lr=sentinel, pc=fn; runs until pc==sentinel or maxsteps */
static unsigned lastr0, lastcpsr;
unsigned h_lastr0(void){return lastr0;}
unsigned h_lastcpsr(void){return lastcpsr;}
long h_call(unsigned fn, unsigned r0, unsigned r1, unsigned r2, unsigned r3, unsigned sentinel, long maxsteps){
  struct ARMCore* cpu=core->cpu;
  int32_t saved[16]; for(int i=0;i<16;i++) saved[i]=cpu->gprs[i];
  union PSR scpsr=cpu->cpsr; enum ExecutionMode smode=cpu->executionMode;
  int32_t p0=cpu->prefetch[0], p1=cpu->prefetch[1];
  cpu->gprs[0]=r0; cpu->gprs[1]=r1; cpu->gprs[2]=r2; cpu->gprs[3]=r3;
  cpu->gprs[14]=sentinel|1;
  cpu->gprs[15]=fn&~1; 
  if(cpu->executionMode!=MODE_THUMB){ cpu->cpsr.t=1; ARMSetPrivilegeMode(cpu, cpu->cpsr.priv); cpu->executionMode=MODE_THUMB; }
  ThumbWritePC(cpu);
  long n=0;
  while(n<maxsteps){
    if(cpu->executionMode==MODE_THUMB && cpu->gprs[15] == ((sentinel&~1)+2)) break;
    core->step(core); n++;
  }
  lastr0=cpu->gprs[0]; lastcpsr=cpu->cpsr.packed;
  for(int i=0;i<16;i++) cpu->gprs[i]=saved[i];
  cpu->cpsr=scpsr; cpu->executionMode=smode; cpu->prefetch[0]=p0; cpu->prefetch[1]=p1;
  cpu->memory.setActiveRegion(cpu, cpu->gprs[15]);
  return n<maxsteps? n : -1;
}
unsigned h_cpsr(void){ struct ARMCore* cpu=core->cpu; return cpu->cpsr.packed; }
#include <stdio.h>
int h_savefile(const char* p){ size_t n=core->stateSize(core); void* b=malloc(n); if(!core->saveState(core,b)){free(b);return -1;} FILE* f=fopen(p,"wb"); fwrite(b,1,n,f); fclose(f); free(b); return (int)n; }
int h_loadfile(const char* p){ size_t n=core->stateSize(core); void* b=malloc(n); FILE* f=fopen(p,"rb"); if(!f){free(b);return -1;} size_t r=fread(b,1,n,f); fclose(f); int ok=core->loadState(core,b); free(b); return ok? (int)r : -2; }
long h_watch(unsigned addr, long maxsteps, unsigned* pcs, int maxpcs){
  struct ARMCore* cpu=core->cpu; unsigned v=core->rawRead32(core,addr,-1); long n=0; int k=0;
  while(n<maxsteps && k<maxpcs){ unsigned pc=cpu->gprs[15]; core->step(core); n++; unsigned nv=core->rawRead32(core,addr,-1); if(nv!=v){ pcs[k++]=pc; pcs[k++]=nv; v=nv; } }
  return k;
}
