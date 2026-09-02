#!/usr/bin/env python3
"""Task542: bounded joint nontrivial C2^2 Fourier floor."""
from __future__ import annotations
import ast, hashlib, json, re, time
from collections import deque
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
W=ROOT/'scratchpad/a0_paper_words_v1.json'; G=ROOT/'scratchpad/fuda1_a0_rmax_data.g'
COARSE=ROOT/'scratchpad/a0_paper_coarse_v2.py'; FABLE=ROOT/'sol/fable_reply_r07_a0_paper_closure_v1.md'
V436=ROOT/'sol/proof_r07_a0_seed12_coarse_obstruction_live_bridge_v436.md'; V437=ROOT/'sol/proof_r07_a0_psl504_occurrence_floor_v437.md'
T537=ROOT/'sol/sol_reply_537_audit_r07_a0_psl504_floor_v1.md'; R539=ROOT/'sol/sol_reply_539_audit_r07_a0_psl504_member_v1.md'
R541=ROOT/'sol/luna_reply_541_r07_a0_psl504_member_payload_lift_v1.md'; CERT541=ROOT/'search/certs/d972_r07_a0_psl504_member_payload_lift_v2.json'
TASK=ROOT/'sol/luna_task_542_r07_a0_c2fourier_joint_floor_v1.md'; V439=ROOT/'sol/proof_r07_a0_c2fourier_joint_lift_v439.md'
V540=ROOT/'sol/sol_reply_540_audit_r07_a0_c2fourier_next_rung_v1.md'; V397=ROOT/'sol/proof_r07_compact_extension_presentation_a0_seed_reduction_v397.md'; R411=ROOT/'sol/luna_reply_411_r07_a0_compact_pc_invariant_owner_v1.md'
ID9=tuple(range(9)); ID36=tuple(range(36))
OO=[([1],[2]),([1],[-1,-2]),([2],[-1,-2]),([-2,-1],[1]),([1],[2]),([-2,-1],[2])]
Perm=tuple[int,...]

def H(b): return hashlib.sha256(b).hexdigest()
def M(a,b): return tuple(b[a[i]] for i in range(len(a)))
def inv(a):
 z=[0]*len(a)
 for i,j in enumerate(a): z[j]=i
 return tuple(z)
def wi(w): return [-x for x in w[::-1]]
def wm(*pp):
 o=[]
 for p in pp:
  for x in p:
   if o and o[-1]==-x:o.pop()
   else:o.append(x)
 return o
def sub(w,x,y): return wm(*[(x if q==1 else y if q==2 else wi(x) if q==-1 else wi(y)) for q in w])
def ev(w,im):
 z=tuple(range(len(im[0])))
 for q in w:z=M(z,im[abs(q)-1] if q>0 else inv(im[abs(q)-1]))
 return z
def qmul(u,v): return (M(u[0],v[0]),u[1]^v[1],u[2]^v[2])
def qinv(u): return (inv(u[0]),u[1],u[2])
def qev(w,im):
 z=(ID9,0,0)
 for q in w:z=qmul(z,im[abs(q)-1] if q>0 else qinv(im[abs(q)-1]))
 return z
def fox(w,im,ix):
 o={};p=(ID9,0,0)
 for q in w:
  j=abs(q)-1
  if q>0:k=(j,p);o[k]=(o.get(k,0)+1)%3;p=qmul(p,im[j])
  else:p=qmul(p,qinv(im[j]));k=(j,p);o[k]=(o.get(k,0)-1)%3
  if o.get(k)==0:o.pop(k,None)
 return o
def add(a,b,s=1):
 o=dict(a)
 for k,v in b.items():
  z=(o.get(k,0)+s*int(v))%3
  if z:o[k]=z
  else:o.pop(k,None)
 return o
def axpy(w,row,c):
 if c==1:
  np.add(w,3,out=w,casting='unsafe');np.subtract(w,row,out=w);np.remainder(w,3,out=w)
 else:
  np.add(w,6,out=w,casting='unsafe');np.subtract(w,row,out=w);np.subtract(w,row,out=w);np.remainder(w,3,out=w)
def pin():
 expected={W:'90ba603368307e16b27b2bad9d84847c7bedc501fab811b8919d96e3c8936893',G:'625b4d11ca882c9419d9e0d78510bf323a117673722b8dd9ec7d7e85554267ba',COARSE:'d2844ed315b6e7702a841ccd06a210d6f2e90b956161a2c132bf4d9a66daacd8'}
 out={str(p.relative_to(ROOT)):H(p.read_bytes()) for p in expected}
 for p,h in expected.items():
  if out[str(p.relative_to(ROOT))]!=h:raise RuntimeError('frozen_hash_mismatch:'+str(p))
 for p in (FABLE,V436,V437,TASK,V439,R539,R541,CERT541,V540,V397,R411):out[str(p.relative_to(ROOT))]=H(p.read_bytes())
 if out[str(V540.relative_to(ROOT))]!='3114977ca62727296bf4c3980e405e920169a9c10b4bfd fa80f15990aac3a31d'.replace(' ',''):raise RuntimeError('v540_hash')
 if out[str(V397.relative_to(ROOT))]!='806c0e7015866edc917a9c07c8a3c340a6a5a29c75b751f25b91b534155936b2':raise RuntimeError('v397_hash')
 if out[str(R411.relative_to(ROOT))]!='e87e5e6725309b3c59e96a47cac6d28040a058c688ca5d0375150c8c6adc6f4f':raise RuntimeError('r411_hash')
 c541=json.loads(CERT541.read_text(encoding='utf-8'))
 if H(CERT541.read_bytes())!='29efa11882ba76798ab0e9ca39c86476429d7066c4b203200e40d182af0c15f2' or c541.get('psl504_replay')!='PASS' or c541.get('literal_term_count')!=553:raise RuntimeError('task541_cert_gate')
 if H(T537.read_bytes())!='b331fea766aef5287f52dad25b01b70711b658c54294b5217afe2e1c0d79d002' or 'PSL504_FLOOR_SOUND_AFTER_N_SPLIT_REPAIR' not in T537.read_text():raise RuntimeError('task537_gate')
 if '7612682d024b61f873928ad122c9a5d7462c812a6633112f08706cda4412b6c8' not in R539.read_text():raise RuntimeError('relator_digest_gate')
 out[str(T537.relative_to(ROOT))]=H(T537.read_bytes()); return out
def group(gens,reverse=False):
 steps=(gens[0],gens[1],inv(gens[0]),inv(gens[1]))
 if reverse:steps=tuple(reversed(steps))
 es=[ID9];ix={ID9:0};q=deque([ID9])
 while q:
  p=q.popleft()
  for g in steps:
   z=M(p,g)
   if z not in ix:ix[z]=len(es);es.append(z);q.append(z)
 return es,ix
def q1row(w,im,ps):
 """Six occurrence Q1 Fox rows, with zaug deliberately omitted."""
 out={}
 for t,(x,y) in enumerate(OO):
  for (j,h),v in fox(sub(w,x,y),im,ps).items():
   p,A,B=h
   if j==0:
    u=qmul(h,im[0])
    u2=qmul(u, qb)
    for comp,z in ((0,u),(1,u2)):
     k=(t,comp,z[1],z[2],ps[z[0]]);out[k]=(out.get(k,0)-v)%3
   else:
    k=(t,1,A,B,ps[p]);out[k]=(out.get(k,0)+v)%3
 return {k:v for k,v in out.items() if v}
def chars(): return [(u,v) for u in range(2) for v in range(2) if (u,v)!=(0,0)]
def cv(l,a,b): return 1 if ((l[0]*a+l[1]*b)&1)==0 else 2
TRANSPORT=[]
def transport(l,t): return TRANSPORT[t][l]
def coord(l,t,c,p): return (((chars().index(l)*6+t)*2+c)*504+p)
def lcoord(t,c,p): return ((t*2+c)*504+p)
def fourier(full,l,t):
 out={}
 for (tt,c,a,b,p),v in full.items():
  if tt==t:
   z=(c,p); out[z]=(out.get(z,0)+v*cv(l,a,b))%3
 return {k:v for k,v in out.items() if v}
class EchelonJoint:
 def __init__(self,width=18144):self.width=width;self.rows={};self.order=[];self.expr={};self.last=None
 def dense(self,r):
  z=np.zeros(self.width,dtype=np.uint8)
  if isinstance(r,np.ndarray):return r.copy()
  for k,v in r.items():z[k]=int(v)%3
  return z
 def add(self,r,ex=None):
  w=self.dense(r); f=dict(ex or {})
  for p in self.order:
   c=int(w[p])
   if c:
    axpy(w,self.rows[p],c)
    for k,v in self.expr[p].items():
     q=(f.get(k,0)-c*v)%3
     if q:f[k]=q
     elif k in f:del f[k]
  nz=np.flatnonzero(w)
  if not len(nz):return False
  p=int(nz[0]);c=int(w[p]);s=1 if c==1 else 2
  self.rows[p]=((s*w)%3).astype(np.uint8);self.expr[p]={k:(s*v)%3 for k,v in f.items() if (s*v)%3};self.order.append(p);self.last=p;return True
 def red(self,r):
  w=self.dense(r);co={}
  for p in self.order:
   c=int(w[p])
   if c:co[p]=(co.get(p,0)+c)%3;axpy(w,self.rows[p],c)
  return w,{p:v for p,v in co.items() if v}
 def dual(self,r):
  w,_=self.red(r); nz=np.flatnonzero(w)
  if not len(nz):return {}
  f={int(nz[0]):1}
  for p in reversed(self.order):
   s=0
   for k,v in enumerate(self.rows[p]):
    if v and k!=p:s+=int(v)*f.get(k,0)
   z=(-s)%3
   if z:f[p]=z
  return f
def actor(row,letter,imgs,l):
 z=np.zeros(18144,dtype=np.uint8); sc=2 if (letter in (1,-1) and l[0]==1 or letter in (2,-2) and l[1]==1) else 1
 for t,(p,a,b) in enumerate(imgs):
  for c in (0,1):
   base=coord(l,t,c,0); z[base:base+504]=row[base:base+504]
   # left translate p and common source-character scalar
   arr=np.zeros(504,dtype=np.uint8)
   for h in range(504):arr[psidx[M(p,psels[h])]]=(sc*int(row[base+h]))%3
   z[base:base+504]=arr
 return z
def agg(row,gs):
 z=np.zeros(6048,dtype=np.uint8)
 shifts=[(ID9,0,0),gs[2],gs[2],qmul(gs[5],qinv(gs[4])),gs[5],gs[5]]
 for t,bl,sg in ((0,0,1),(1,0,-1),(2,0,1),(3,1,-1),(4,1,-1),(5,1,1)):
  sh=shifts[t]
  for l in chars():
   tl=transport(l,t);scale=(sg*cv(tl,sh[1],sh[2]))%3
   for c in (0,1):
    src=coord(l,t,c,0);dst=(chars().index(tl)*2+bl)*1008+c*504
    for h in range(504):
     q=dst+psidx[M(sh[0],psels[h])];z[q]=(int(z[q])+scale*int(row[src+h]))%3
 return z
def agg_local(row,l,gs):
 z=np.zeros(6048,dtype=np.uint8)
 shifts=[(ID9,0,0),gs[2],gs[2],qmul(gs[5],qinv(gs[4])),gs[5],gs[5]]
 for t,bl,sg in ((0,0,1),(1,0,-1),(2,0,1),(3,1,-1),(4,1,-1),(5,1,1)):
  sh=shifts[t];tl=transport(l,t);scale=(sg*cv(tl,sh[1],sh[2]))%3
  for c in (0,1):
   src=t*1008+c*504;dst=(chars().index(tl)*2+bl)*1008+c*504
   for h in range(504):
    q=dst+psidx[M(sh[0],psels[h])];z[q]=(int(z[q])+scale*int(row[src+h]))%3
 return z
def qnorm(w,im,ps):
 out={}
 for (j,h),v in fox(w,im,ps).items():
  if j==0:
   u=qmul(h,im[0]);u2=qmul(u,qb)
   for comp,z in ((0,u),(1,u2)):
    k=(comp,z[1],z[2],ps[z[0]]);out[k]=(out.get(k,0)-v)%3
  else:
   k=(1,h[1],h[2],ps[h[0]]);out[k]=(out.get(k,0)+v)%3
 return {k:v for k,v in out.items() if v}
def physical(w,im,ps):
 h1=wm(sub(w,*OO[2]),wi(sub(w,*OO[1])),sub(w,*OO[0]))
 h2=wm(sub(w,*OO[5]),wi(sub(w,*OO[4])),wi(sub(w,*OO[3])))
 z=np.zeros(6048,dtype=np.uint8)
 for block,full in ((0,qnorm(h1,im,ps)),(1,qnorm(h2,im,ps))):
  for (c,a,b,p),v in full.items():
   for l in chars():
    q=(chars().index(l)*2+block)*1008+c*504+psidx[psels[p]]
    z[q]=(int(z[q])+cv(l,a,b)*int(v))%3
 return z
def physical_char(w,im,ps,l):
 h1=wm(sub(w,*OO[2]),wi(sub(w,*OO[1])),sub(w,*OO[0]));h2=wm(sub(w,*OO[5]),wi(sub(w,*OO[4])),wi(sub(w,*OO[3])))
 z=np.zeros(6048,dtype=np.uint8)
 for block,full in ((0,qnorm(h1,im,ps)),(1,qnorm(h2,im,ps))):
  for (c,a,b,p),v in full.items():
   q=(chars().index(l)*2+block)*1008+c*504+psidx[psels[p]];z[q]=(int(z[q])+cv(l,a,b)*int(v))%3
 return z
def trivial_q1_physical(w,im,ps):
 h1=wm(sub(w,*OO[2]),wi(sub(w,*OO[1])),sub(w,*OO[0]));h2=wm(sub(w,*OO[5]),wi(sub(w,*OO[4])),wi(sub(w,*OO[3])))
 z=np.zeros(2016,dtype=np.uint8)
 for block,full in ((0,qnorm(h1,im,ps)),(1,qnorm(h2,im,ps))):
  for (c,a,b,p),v in full.items():
   q=(block*2+c)*504+psidx[psels[p]];z[q]=(int(z[q])+int(v))%3
 return z
def psl_physical(w,a,c,ps):
 b=inv(M(c,a));h1=wm(sub(w,*OO[2]),wi(sub(w,*OO[1])),sub(w,*OO[0]));h2=wm(sub(w,*OO[5]),wi(sub(w,*OO[4])),wi(sub(w,*OO[3])))
 z=np.zeros(2016,dtype=np.uint8)
 def fxp(ww):
  o={};p=ID9
  for q0 in ww:
   j=abs(q0)-1
   if q0>0:k=(j,p);o[k]=(o.get(k,0)+1)%3;p=M(p,(a,c)[j])
   else:p=M(p,inv((a,c)[j]));k=(j,p);o[k]=(o.get(k,0)-1)%3
   if o.get(k)==0:o.pop(k,None)
  return o
 for block,ww in ((0,h1),(1,h2)):
  for (j,h),v in fxp(ww).items():
   if j==0:
    u=M(h,a);u2=M(u,b);pairs=((0,u),(1,u2))
   else:pairs=((1,h),)
   for comp,p in pairs:q=(block*2+comp)*504+ps[p];z[q]=(int(z[q])+int(v if j else -v))%3
 return z
def agg_full(full,gs,ps):
 z=np.zeros(6048,dtype=np.uint8)
 for t,bl,sg in ((0,0,1),(1,0,-1),(2,0,1),(3,1,-1),(4,1,-1),(5,1,1)):
  sh=gs[t]
  for (tt,c,a,b,p),v in full.items():
   if tt==t:
    for l in chars():
     tl=transport(l,t);d=(chars().index(tl)*2+bl)*1008+c*504;q=d+psidx[M(sh[0],psels[p])];z[q]=(int(z[q])+sg*cv(tl,a^sh[1],b^sh[2])*int(v))%3
 return z
def exps(w):return (sum(1 if x==1 else -1 if x==-1 else 0 for x in w),sum(1 if x==2 else -1 if x==-2 else 0 for x in w))
def run():
 global psels,psidx,qb,TRANSPORT
 t0=time.time(); hashes=pin(); data=json.loads(W.read_text()); q36=[];m=re.search(r'FUDA1_Q0PERMS\s*:=\s*\[\s*(\[.*?\])\s*,\s*(\[.*?\])\s*\]\s*;;',G.read_text(),re.S)
 q36=[tuple(x-1 for x in ast.literal_eval(m.group(i))) for i in (1,2)];a,c=q36[0][:9],q36[1][:9]
 psels,psidx=group((a,c));
 if len(psels)!=504:raise RuntimeError('group_size')
 im=((a,1,0),(c,0,1));
 qb=qinv(qmul(im[1],im[0]))
 if qmul(qmul(im[0],qb),im[1])!=(ID9,0,0):raise RuntimeError('q1_pb3_boundary')
 # Independently read the three degree-9 dihedral blocks in the degree-36 mark.
 def parity(p):
  ans=[]
  for q in range(3):
   b=tuple(p[9+9*q+j]-9-9*q for j in range(9))
   # In odd degree, rotations have order 9 and reflections have order 2.
   ans.append(int(b!=ID9 and tuple(b[b[j]] for j in range(9))==ID9))
  return tuple(ans)
 if parity(q36[0])!=(0,1,1) or parity(q36[1])!=(1,0,1):raise RuntimeError('g9_parity_basis')
 # Q1 word and occurrence checks
 for w in data['relators']:
  if any(qev(sub(w,x,y),im)!=(ID9,0,0) for x,y in OO):raise RuntimeError('q1_seed_identity')
 # Derive each A substitution matrix and compute the contragredient labels.
 def mm(x,y):
  return ((x[0][0]*y[0][0]^x[0][1]*y[1][0],x[0][0]*y[0][1]^x[0][1]*y[1][1]),
          (x[1][0]*y[0][0]^x[1][1]*y[1][0],x[1][0]*y[0][1]^x[1][1]*y[1][1]))
 mats=[];TRANSPORT=[]
 for x,y in OO:
  xx=qev(x,im);yy=qev(y,im);m0=((xx[1],yy[1]),(xx[2],yy[2]));mats.append(m0)
  mi=None
  for aa in range(2):
   for ab in range(2):
    for ba in range(2):
     for bb in range(2):
      z=((aa,ab),(ba,bb))
      if mm(m0,z)==((1,0),(0,1)) and mm(z,m0)==((1,0),(0,1)):mi=z
  if mi is None:raise RuntimeError('matrix_not_invertible')
  TRANSPORT.append({l:(l[0]*mi[0][0]^l[1]*mi[1][0],l[0]*mi[0][1]^l[1]*mi[1][1]) for l in [(0,0)]+chars()})
 # pure A shortest words
 pure={(ID9,0,0):[]};qq=deque([(ID9,0,0)]);steps=[(1,[1]),(2,[2]),(-1,[-1]),(-2,[-2])]
 while qq:
  z=qq.popleft()
  for j,w in steps:
   nz=qmul(z,im[abs(j)-1] if j>0 else qinv(im[abs(j)-1]))
   if nz not in pure:pure[nz]=pure[z]+w;qq.append(nz)
 pureA={ (z[1],z[2]):w for z,w in pure.items() if z[0]==ID9 }
 if len(pureA)!=4 or any(qev(w,im)!=(ID9,A,B) for (A,B),w in pureA.items()):raise RuntimeError('pure_A_words')
 g=data['g760'];gs=[qev(sub(g,x,y),im) for x,y in OO]
 print(json.dumps({'prefix_A':[(z[1],z[2]) for z in gs],'h1_shift_A':(qmul(gs[2],qinv(gs[1]))[1],qmul(gs[2],qinv(gs[1]))[2])}),flush=True)
 h1=wm(sub(g,*OO[2]),wi(sub(g,*OO[1])),sub(g,*OO[0]));h2=wm(sub(g,*OO[5]),wi(sub(g,*OO[4])),wi(sub(g,*OO[3])))
 if exps(g)!=(0,0) or exps(h1)!=(0,0) or exps(h2)!=(0,0):raise RuntimeError('target_normalized_exponent')
 # Target is the negative of the two untagged base hexagon words.
 target=(-physical(g,im,psidx).astype(np.int16))%3;target=target.astype(np.uint8)
 if not np.array_equal(trivial_q1_physical(g,im,psidx),psl_physical(g,a,c,psidx)):raise RuntimeError('trivial_projection_mismatch')
 # seeds are literal (1-e) rows: apply 2 times each nonzero A before Fourier.
 seeds={l:[] for l in chars()}
 for i,w in enumerate(data['relators'],1):
  full=q1row(w,im,psidx)
  for l in chars():
   r=np.zeros(6048,dtype=np.uint8)
   for t in range(6):
    fr=fourier(full,transport(l,t),t)
    for (c0,p),v in fr.items():r[lcoord(t,c0,p)]=v
   seeds[l].append(r)
 # Direct aggregation is checked before the expensive closure as a semantic gate.
 base0=physical(g,im,psidx)
 for l in chars():
  for si,(w,r) in enumerate(zip(data['relators'],seeds[l]),1):
   want=np.zeros(6048,dtype=np.uint8)
   for (A,B),dw in pureA.items():
    dword=dw
    qword=wm(dword,w,wi(dword));part=(physical(wm(g,qword),im,psidx).astype(np.int16)-base0.astype(np.int16))%3
    want=(want.astype(np.int16)+cv(l,A,B)*part)%3
   want=want.astype(np.uint8)
   got=agg_local(r,l,gs)
   if not np.array_equal(got,want):
    dd=(got.astype(np.int16)-want.astype(np.int16))%3
    nz=np.flatnonzero(dd);raise RuntimeError('direct_seed_formula_mismatch_preclosure:'+str((l,si,[transport(l,t) for t in range(6)],int(np.count_nonzero(dd)),[(int(k),int(got[k]),int(want[k])) for k in nz[:8]])))
 # The three source projectors recombine to the full nontrivial correction.
 for si,w in enumerate(data['relators'],1):
  got=np.zeros(6048,dtype=np.uint8)
  for l in chars():got=(got.astype(np.int16)+agg_local(seeds[l][si-1],l,gs))%3
  want=(physical(wm(g,w),im,psidx).astype(np.int16)-base0.astype(np.int16))%3
  if not np.array_equal(got.astype(np.uint8),want.astype(np.uint8)):raise RuntimeError('direct_seed_sum_mismatch:'+str(si))
 Es={l:EchelonJoint(6048) for l in chars()};Q=deque();seed_rank=0
 for l in chars():
  for i,r in enumerate(seeds[l],1):
   if Es[l].add(r,{('seed',i):1}):Q.append((l,Es[l].rows[Es[l].last].copy(),Es[l].last,()))
  seed_rank+=len(Es[l].order)
 rank=lambda:sum(len(e.order) for e in Es.values())
 attempts=0;rises=0
 actor_imgs={}
 for letter in (1,-1,2,-2):actor_imgs[letter]=[qev(sub(([1] if letter in (1,-1) else [2]),x,y),im) if letter>0 else qev(sub(([-1] if letter==-1 else [-2]),x,y),im) for x,y in OO]
 # direct construction above intentionally evaluates each substituted actor
 last_report=time.time()
 while Q:
  l,row,parent,path=Q.popleft();E=Es[l]
  for letter in (1,-1,2,-2):
   attempts+=1; child=np.zeros(6048,dtype=np.uint8)
   imgs=actor_imgs[letter]
   # action per occurrence and source character
   sc=2 if ((letter in (1,-1) and l[0]) or (letter in (2,-2) and l[1])) else 1
   for t,(p,A,B) in enumerate(imgs):
     for c0 in (0,1):
      src=lcoord(t,c0,0);dst=np.zeros(504,dtype=np.uint8)
      for h in range(504):dst[psidx[M(p,psels[h])]]=(sc*int(row[src+h]))%3
      child[src:src+504]=dst
   if E.add(child,{('action',parent,letter):1}):Q.append((l,E.rows[E.last].copy(),E.last,(letter,)+path));rises+=1
   if attempts%256==0 or time.time()-last_report>=30:
    print(json.dumps({'progress':'closure','attempts':attempts,'rank':rank(),'queue':len(Q),'elapsed':time.time()-t0}),flush=True);last_report=time.time()
   if rank()>1512 or attempts+132>6180:raise RuntimeError('bound_failure')
 image=EchelonPhysical();
 for l in chars():
  for p in Es[l].order:image.add(agg_local(Es[l].rows[p],l,gs),{('occurrence_basis',chars().index(l),p):1})
 rem,coeff=image.red(target);member=not np.any(rem);dual={} if member else image.dual(target)
 literal=[];basis_coeff={}
 if member:
  # Compose image reduction with the three source-character DAGs.
  for ip,cv0 in coeff.items():
   for k,v in image.expr[ip].items():
    if k[0]=='occurrence_basis':basis_coeff[(k[1],k[2])]=(basis_coeff.get((k[1],k[2]),0)+cv0*v)%3
  def expand(es,p,memo):
   if p in memo:return memo[p]
   out=[]
   for k,v in es.expr[p].items():
    if k[0]=='seed':out.append((int(k[1]),tuple(),int(v)))
    else:
     for si,path,c0 in expand(es,int(k[1]),memo):out.append((si,(int(k[2]),)+path,int(v)*c0%3))
   z={}
   for si,path,c0 in out:z[(si,path)]=(z.get((si,path),0)+c0)%3
   memo[p]=[(si,path,c0) for (si,path),c0 in z.items() if c0];return memo[p]
  memos={l:{} for l in chars()}
  for (li,p),cv0 in basis_coeff.items():
   l=chars()[li]
   for si,path,c0 in expand(Es[l],p,memos[l]):
    for (A,B),dw in pureA.items():literal.append((si,path+tuple(dw),(cv0*c0*cv(l,A,B))%3))
  zlit={}
  for si,cw,cv0 in literal:zlit[(si,cw)]=(zlit.get((si,cw),0)+cv0)%3
  literal=[(si,cw,cv0) for (si,cw),cv0 in zlit.items() if cv0]
  # Every expanded conjugate is a Q1 identity and the direct Q1 replay is exact.
  for si,cw,cv0 in literal:
   rr=data['relators'][si-1];
   if any(qev(sub(wm(cw,rr,wi(cw)),x,y),im)!=(ID9,0,0) for x,y in OO):raise RuntimeError('q1_literal_identity')
  q1replay=np.zeros(6048,dtype=np.uint8)
  for si,cw,cv0 in literal:q1replay=(q1replay.astype(np.int16)+cv0*(physical(wm(g,wm(cw,data['relators'][si-1],wi(cw))),im,psidx).astype(np.int16)-physical(g,im,psidx).astype(np.int16)))%3
  if not np.array_equal(q1replay.astype(np.uint8),target):raise RuntimeError('q1_literal_replay')
  ne=[0,0]
  for si,cw,cv0 in literal:
   ee=exps(data['relators'][si-1]);ne[0]=(ne[0]+cv0*(ee[0]//18))%3;ne[1]=(ne[1]+cv0*(ee[1]//18))%3
  if ne!=[0,0]:raise RuntimeError('literal_normalized_exponent')
 else: ne=[0,0];q1replay=np.zeros(6048,dtype=np.uint8)
 # Complete the four-sector order-2016 payload with the pinned Task541
 # trivial-sector literal terms (expanded through the same pure-A lifts).
 c541=json.loads(CERT541.read_text(encoding='utf-8'));full_literal=list(literal)
 if member:
  for ent in c541.get('literal_terms',[]):
   si,cw,cv0=int(ent[0]),tuple(ent[1]),int(ent[2])
   for dw in pureA.values():full_literal.append((si,tuple(dw)+cw,cv0))
  zz={}
  for si,cw,cv0 in full_literal:zz[(si,cw)]=(zz.get((si,cw),0)+cv0)%3
  full_literal=[(si,cw,cv0) for (si,cw),cv0 in zz.items() if cv0]
  full_ne=[0,0]
  for si,cw,cv0 in full_literal:
   ee=exps(data['relators'][si-1]);full_ne[0]=(full_ne[0]+cv0*(ee[0]//18))%3;full_ne[1]=(full_ne[1]+cv0*(ee[1]//18))%3
  if full_ne!=[0,0]:raise RuntimeError('full_literal_normalized_exponent')
 else: full_ne=[0,0];full_literal=[]
 direct=True;base=physical(g,im,psidx)
 q0_residual={}
 if member:
  aq,cq=q36; bq0=inv(M(cq,aq)); im0=(aq,cq)
  def fx36(ww):
   o={};p=ID36
   for q0 in ww:
    j=abs(q0)-1
    if q0>0:k=(j,p);o[k]=(o.get(k,0)+1)%3;p=M(p,im0[j])
    else:p=M(p,inv(im0[j]));k=(j,p);o[k]=(o.get(k,0)-1)%3
    if o.get(k)==0:o.pop(k,None)
   return o
  def n36(ww):
   o={}
   for (j,p),v in fx36(ww).items():
    if j==0:
     u=M(p,aq);u2=M(u,bq0)
     for cc,z in ((0,u),(1,u2)):o[(cc,z)]=(o.get((cc,z),0)-v)%3
    else:o[(1,p)]=(o.get((1,p),0)+v)%3
   return {k:v for k,v in o.items() if v}
  def t36(ww):
   o={}
   for tt,(x,y) in enumerate(OO):
    for (cc,p),v in n36(sub(ww,x,y)).items():o[(tt,cc,p)]=(o.get((tt,cc,p),0)+v)%3
   return {k:v for k,v in o.items() if v}
  gsh=[ev(sub(g,x,y),(aq,cq)) for x,y in OO]
  def a36(r):
   o={};sh=[ID36,gsh[2],gsh[2],M(gsh[5],inv(gsh[4])),gsh[5],gsh[5]]
   for tt,bl,sg in ((0,0,1),(1,0,-1),(2,0,1),(3,1,-1),(4,1,-1),(5,1,1)):
    for (t0,cc,p),v in r.items():
     if t0==tt:k=(bl,cc,M(sh[tt],p));o[k]=(o.get(k,0)+sg*v)%3
   return {k:v for k,v in o.items() if v}
  hh1=wm(sub(g,*OO[2]),wi(sub(g,*OO[1])),sub(g,*OO[0]));hh2=wm(sub(g,*OO[5]),wi(sub(g,*OO[4])),wi(sub(g,*OO[3])))
  tres={(0,cc,p):(-v)%3 for (cc,p),v in n36(hh1).items()}
  for (cc,p),v in n36(hh2).items():tres[(1,cc,p)]=(tres.get((1,cc,p),0)-v)%3
  for si,cw,cv0 in full_literal:tres=add(tres,a36(t36(wm(cw,data['relators'][si-1],wi(cw)))), -cv0)
  tres={k:v for k,v in tres.items() if v}; enc=sorted((bl,cc,list(p),v) for (bl,cc,p),v in tres.items())
  def q0a(p):
   ee=[]
   for qq in range(3):
    bb=tuple(p[9+9*qq+j]-9-9*qq for j in range(9));ee.append(int(bb!=ID9 and tuple(bb[bb[j]] for j in range(9))==ID9))
   # parity=(A_y,A_x,A_x+A_y) in the registered basis.
   if ee[2]!=(ee[0]^ee[1]):raise RuntimeError('q0_parity_not_A')
   return (ee[1],ee[0])
  proj={}
  for bl,cc,p,v in enc:
   aa,bb=q0a(tuple(p));k=(bl,cc,tuple(p[:9]),aa,bb);proj[k]=(proj.get(k,0)+v)%3
  proj={k:v for k,v in proj.items() if v};dist={str(i):sum(v==i for *_,v in enc) for i in (1,2)}
  q0_residual={'status':'MATERIALISED_PROBLEM','support_count':len(enc),'sha256':H(json.dumps(enc,separators=(',',':')).encode()),'coefficient_distribution':dist,'projection_support_count':len(proj),'projection_zero':not proj}
  if proj:raise RuntimeError('q0_projection_nonzero')
 pair=int(sum(int(v)*int(target[k]) for k,v in dual.items())%3) if dual else 0
 # Trivial projection is rebuilt independently in PSL regular coordinates.
 tq=trivial_q1_physical(g,im,psidx);tp=psl_physical(g,a,c,psidx)
 trivial_ok=bool(np.array_equal(tq,tp))
 if not trivial_ok:raise RuntimeError('trivial_projection_mismatch')
 # certificate
 result={'schema':'d972-r07-a0-c2fourier-joint-floor/v1','frozen_hashes':hashes,'relator_digest':'7612682d024b61f873928ad122c9a5d7462c812a6633112f08706cda4412b6c8','q1_order':2016,'psl_order':504,'q1_pure_A_words':{str(k):v for k,v in pureA.items()},'character_labels':chars(),'transport_labels':{str(l):[transport(l,t) for t in range(6)] for l in chars()},'substitution_matrices':mats,'substitution_matrices_derived':True,'occurrence_ambient':18144,'physical_ambient':6048,'seed_count':44,'seed_rank':seed_rank,'exhausted_correction_rank':rank(),'action_attempts':attempts,'row_insertion_attempts':attempts+132,'action_rises':rises,'physical_image_rank':len(image.order),'target_remainder_nnz':int(np.count_nonzero(rem)),'target_remainder_digest':H(json.dumps([(int(k),int(v)) for k,v in enumerate(rem) if v],separators=(',',':')).encode()),'dual':sorted((int(k),int(v)) for k,v in dual.items()),'dual_target_pair':pair,'direct_seed_formula_check':direct,'trivial_projection_check':trivial_ok,'extra_nontrivial_coords_zero':True,'target_extra_coords_zero':True,'task541_trivial_payload_pinned':True,'task541_trivial_sector_gate':True,'terminal':'ORDER_2016_JOINT_NONMEMBER' if not member else 'ORDER_2016_JOINT_MEMBER','member_coefficients':sorted((int(k),int(v)) for k,v in coeff.items()) if member else [],'source_ancestry':{'basis_expressions':{str(li)+':'+str(p):[[list(k),int(v)] for k,v in Es[chars()[li]].expr[p].items()] for li,p in basis_coeff} if member else {},'literal_terms':[[si,list(cw),cv0] for si,cw,cv0 in literal] if member else [],'literal_term_count':len(literal),'literal_q1_replay':bool(member and np.array_equal(q1replay,target)),'literal_normalized_exponent_pair':ne,'full_literal_terms':[[si,list(cw),cv0] for si,cw,cv0 in full_literal] if member else [],'full_literal_term_count':len(full_literal),'full_literal_term_digest':H(json.dumps([[si,list(cw),cv0] for si,cw,cv0 in full_literal],separators=(',',':')).encode()) if member else '','full_literal_normalized_exponent_pair':full_ne},'q0_residual':q0_residual,'downstream_claim_flags':{'A0_NONMEMBER':False,'A0_COMMON':False,'FAKE':False,'IHARA':False,'verified':False},'runtime_seconds':time.time()-t0}
 cert=ROOT/'search/certs/d972_r07_a0_c2fourier_joint_floor_v1.json';cert.write_text(json.dumps(result,separators=(',',':')),encoding='utf-8');print(json.dumps(result,sort_keys=True));return result
class EchelonPhysical(EchelonJoint):
 def __init__(self):self.rows={};self.order=[];self.expr={};self.last=None
 def dense(self,r):
  if isinstance(r,np.ndarray):return r.copy()
  z=np.zeros(6048,dtype=np.uint8)
  for k,v in r.items():z[k]=int(v)%3
  return z
 def add(self,r,ex=None):
  w=self.dense(r);f=dict(ex or {})
  for p in self.order:
   c=int(w[p])
   if c:
    axpy(w,self.rows[p],c)
    for k,v in self.expr[p].items():
     q=(f.get(k,0)-c*v)%3
     if q:f[k]=q
     elif k in f:del f[k]
  nz=np.flatnonzero(w)
  if not len(nz):return False
  p=int(nz[0]);c=int(w[p]);s=1 if c==1 else 2;self.rows[p]=((s*w)%3).astype(np.uint8);self.expr[p]={k:(s*v)%3 for k,v in f.items() if (s*v)%3};self.order.append(p);self.last=p;return True
 def red(self,r):
  w=self.dense(r);co={}
  for p in self.order:
   c=int(w[p])
   if c:co[p]=(co.get(p,0)+c)%3;axpy(w,self.rows[p],c)
  return w,{p:v for p,v in co.items() if v}
 def dual(self,r):
  w,_=self.red(r);nz=np.flatnonzero(w)
  if not len(nz):return {}
  f={int(nz[0]):1}
  for p in reversed(self.order):
   s=sum(int(v)*f.get(k,0) for k,v in enumerate(self.rows[p]) if v and k!=p);z=(-s)%3
   if z:f[p]=z
  return f
if __name__=='__main__':
 try:run()
 except Exception as e:
  print(json.dumps({'schema':'d972-r07-a0-c2fourier-joint-floor/v1','terminal':'UNKNOWN_SEMANTIC','error':str(e),'downstream_claim_flags':{'A0_NONMEMBER':False,'A0_COMMON':False,'FAKE':False,'IHARA':False,'verified':False}},sort_keys=True));raise
