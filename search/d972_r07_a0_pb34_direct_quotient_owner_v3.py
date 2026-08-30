#!/usr/bin/env python3
"""Task421 A0 owner: occurrence-first v405 selector.

This is a new owner.  v2 is deliberately not imported or dispatched.  The
frozen task413/physical-owner ABIs are loaded by digest, while the occurrence
queue and its source ancestry are owned here.
"""
from __future__ import annotations
import argparse,gzip,hashlib,json,marshal,os,sys,tempfile,time,types,shutil
from collections import deque
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
T413=("search/d972_r07_a0_compact_positive_lazy_owner_v2.py",26148,"72cb540056bd812d466e22f90f8ed048b9cfe4821806b0a9e0cab82059c1b403")
OLD=("search/d972_r07_a0_compact_pc_invariant_owner_v1.py",68222,"be17be107103a218123cd0e1eb8455377ca2b52a2e54ec629f3744ad4c2d32f9")
CERT=("search/certs/d972_r07_pb4_central_split_v1_20260830.json",3774,"e1588853db01d196a9bf60ed29d3073bdc71ad25f2aca4c706e51f6f593b4866")
ROSTER="7612682d024b61f873928ad122c9a5d7462c812a6633112f08706cda4412b6c8"; SCHEMA="d972-r07-a0-pb34-direct-quotient-owner/v3"
UNKNOWN="UNKNOWN"; UNKNOWN_RESOURCE="UNKNOWN_RESOURCE"
def sh(b):return hashlib.sha256(b).hexdigest()
def need(x,m):
 if not x:raise RuntimeError(m)
def load(spec,name):
 p=ROOT/spec[0]; b=p.read_bytes();need(len(b)==spec[1] and sh(b)==spec[2],"pin:"+spec[0]);m=types.ModuleType(name);m.__file__=str(p);sys.modules[name]=m;exec(compile(b,spec[0],"exec"),m.__dict__,m.__dict__);return m.__dict__
def dig(x):return sh(json.dumps(x,sort_keys=True,separators=(",",":"),default=str).encode())
def rss():
 if not sys.platform.startswith("linux"):return None
 try:
  for x in Path("/proc/self/status").read_text().splitlines():
   if x.startswith("VmRSS:"):return int(x.split()[1])*1024
 except (OSError,ValueError):pass
 return None
def cp_write(path,state):
 p=Path(path);need(not p.is_absolute() and p.parent==Path("ci/out"),"checkpoint_path");p.parent.mkdir(parents=True,exist_ok=True)
 with tempfile.NamedTemporaryFile(dir=p.parent,prefix=".a0v3-",delete=False) as f:
  tmp=Path(f.name)
  with gzip.GzipFile(fileobj=f,mode="wb",compresslevel=1,mtime=0) as z:marshal.dump({"schema":SCHEMA+"/checkpoint","state":state},z)
  f.flush();os.fsync(f.fileno())
 h=hashlib.sha256();n=0
 with tmp.open("rb") as f:
  for b in iter(lambda:f.read(1<<20),b""):h.update(b);n+=len(b)
 with tempfile.NamedTemporaryFile(dir=p.parent,prefix=".a0v3-sealed-",delete=False) as f:
  out=Path(f.name);f.write(("D972-A0V3-CP1 "+h.hexdigest()+" "+str(n)+"\n").encode());
  with tmp.open("rb") as src:shutil.copyfileobj(src,f,1<<20)
  f.flush();os.fsync(f.fileno())
 tmp.unlink(missing_ok=True);os.replace(out,p)
def cp_read(path):
 p=Path(path);need(not p.is_absolute() and p.parent==Path("ci/out"),"resume_path")
 with p.open("rb") as f:
  head=f.readline().decode().rstrip("\n").split(" ");raw=f.read()
 need(len(head)==3 and head[0]=="D972-A0V3-CP1" and len(raw)==int(head[2]) and sh(raw)==head[1],"checkpoint_seal")
 try:
  with gzip.GzipFile(fileobj=__import__("io").BytesIO(raw),mode="rb") as z:b=marshal.load(z)
 except Exception as e:raise RuntimeError("checkpoint_decode:"+str(e))
 need(isinstance(b,dict) and b.get("schema")==SCHEMA+"/checkpoint" and isinstance(b.get("state"),dict),"checkpoint_schema");return b["state"]
def exp_pair(w):return (sum(1 if x==1 else -1 if x==-1 else 0 for x in w),sum(1 if x==2 else -1 if x==-2 else 0 for x in w))
def inv(w):return [-x for x in reversed(w)]
def mul(*parts):
 o=[]
 for p in parts:
  for x in p:
   if o and o[-1]==-x:o.pop()
   else:o.append(x)
 return o
def poww(w,n):
 if n<0:return poww(inv(w),-n)
 o=[]
 for _ in range(n):o=mul(o,w)
 return o
def row_add(a,b,c=1):
 o=dict(a)
 for k,v in b.items():
  x=(o.get(k,0)+c*int(v))%3
  if x:o[k]=x
  else:o.pop(k,None)
 return o
class Echelon:
 def __init__(self):self.rows={};self.order=[];self.expr={};self.sources=[];self.originals={}
 def add(self,row,source):
  w={k:int(v)%3 for k,v in row.items() if int(v)%3};e={len(self.sources):1}
  for p in self.order:
   c=w.get(p,0)
   if c:w=row_add(w,self.rows[p],-c);e=row_add(e,self.expr[p],-c)
  if not w:return False,None
  p=min(w);s=1 if w[p]==1 else 2;self.rows[p]={k:s*v%3 for k,v in w.items() if s*v%3};self.expr[p]={k:s*v%3 for k,v in e.items() if s*v%3};self.order.append(p);self.sources.append(dict(source));self.originals[p]=dict(row);return True,p
 def reduce(self,row):
  w=dict(row);e={}
  for p in self.order:
   c=w.get(p,0)
   if c:w=row_add(w,self.rows[p],-c);e=row_add(e,self.expr[p],-c)
  return w,e
 def dual(self,target):
  w,e=self.reduce(target)
  if not w:return None,w,e
  d={min(w):1}
  for p in sorted(self.order,reverse=True):
   x=(-sum(v*d.get(k,0) for k,v in self.rows[p].items() if k!=p))%3
   if x:d[p]=x
  return d,w,e
class CorrectedPhysicalQuotient:
 def __init__(self,owner,p176,e3,e4):self.owner=owner;self.p176=p176;self.e3=e3;self.e4=e4;self.z3=e3.eval([1,2,3]);self.z4=e4.eval([1,2,4,3,5,6])
 def dec(self,b,block):return self.p176["value_from_blob"](b,0 if block<3 else 5)
 def enc(self,v):return self.owner["a0_element_blob"](v)
 def parse(self,k):
  need(k[:1]==b"Q" and len(k)>=5,"quotient_key");n=int.from_bytes(k[2:4],"big");raw=k[4:4+n];lab,b=raw.split(b":",1);return k[1],lab.decode(),b
 def h0(self,g,z,v):
  if g is self.e3:
   pw=[g.identity]
   for _ in range(2):pw.append(g.mul(pw[-1],z))
   choices=[(self.enc(g.mul(v,p)),j) for j,p in enumerate(pw)];blob,j=min(choices);return self.dec(blob,1),j
  j=int(v[1][0])%3;h=g.mul(v,g.power(g.inverse(z),j));need(int(h[1][0])%3==0 and g.mul(h,g.power(z,j))==v,"kappa_normal_form");return h,j
 def qkey(self,block,label,b):
  x=label.encode()+b":"+b;return b"Q"+bytes((block,))+len(x).to_bytes(2,"big")+x
 def contract(self,block,entries):
  g,z,n,names=((self.e3,self.z3,2,("b","c")) if block<3 else (self.e4,self.z4,5,("b","c","p","q","r")));pw=[g.identity]
  for _ in range(2):pw.append(g.mul(pw[-1],z))
  reps={};vals={}
  for c,v,a in entries:
   h,j=self.h0(g,z,v);b=self.enc(h);reps[b]=h;vals[(c,b,j)]=(vals.get((c,b,j),0)+a)%3
  central={(b,j):vals.get((n,b,j),0) for b in reps for j in range(3)};gens=[g.eval([2]),g.eval([3])] if block<3 else [g.eval([2]),g.eval([4]),g.eval([3]),g.eval([5]),g.eval([6])]
  for c in range(n):
   for b,h0 in list(reps.items()):
    bv=[vals.get((c,b,j),0) for j in range(3)]
    for lam,j in (((-bv[1]-bv[2])%3,0),((-bv[2])%3,1)):
     if not lam:continue
     h2,j2=self.h0(g,z,g.mul(g.mul(h0,pw[j]),gens[c]));b2=self.enc(h2);reps.setdefault(b2,h2)
     for jj in range(3):central.setdefault((b2,jj),0)
     central[(b2,j2)]=(central[(b2,j2)]-lam)%3;central[(b,j)]=(central[(b,j)]+lam)%3
    vals[(c,b,0)]=sum(bv)%3;vals[(c,b,1)]=vals[(c,b,2)]=0
  out={}
  for b in reps:
   for c in range(n):
    x=sum(vals.get((c,b,j),0) for j in range(3))%3
    if x:out[self.qkey(block,names[c],b)]=x
   for lab,x in (("u0",central[(b,0)]-central[(b,2)]),("u1",central[(b,1)]-central[(b,2)])):
    if x%3:out[self.qkey(block,lab,b)]=x%3
  tau=sum(central[(b,2)] for b in reps)%3
  if tau:out[b"Q"+bytes((block,))+b"tau"]=tau
  return out
 def transform(self,row):
  bs={1:[],2:[],3:[]};out={}
  for k,a in row.items():
   if k[:1]!=b"R":out[k]=(out.get(k,0)+int(a))%3;continue
   block,comp,blob=k[1],k[2],k[5:];g=self.e3 if block<3 else self.e4;v=self.p176["value_from_blob"](blob,0 if block<3 else 5)
   if block<3:
    x,y,z=[g.eval([i]) for i in (1,2,3)];terms=((2,v,1),(1,g.mul(g.mul(v,x),y),-1),(0,g.mul(v,x),-1)) if comp==0 else (((0,v,1),) if comp==1 else ((1,v,1),))
   else:
    a,b,p,c,q,r=[g.eval([i]) for i in (1,2,3,4,5,6)]
    if comp==0:
     t=g.mul(v,self.z4);terms=((5,v,1),(4,g.mul(t,g.inverse(r)),-1),(3,g.mul(g.mul(t,g.inverse(r)),g.inverse(q)),-1),(2,g.mul(g.mul(g.mul(t,g.inverse(r)),g.inverse(q)),g.inverse(p)),-1),(1,g.mul(g.mul(g.mul(g.mul(t,g.inverse(r)),g.inverse(q)),g.inverse(p)),g.inverse(c)),-1),(0,g.mul(g.mul(g.mul(g.mul(g.mul(t,g.inverse(r)),g.inverse(q)),g.inverse(p)),g.inverse(c)),g.inverse(b)),-1))
    else:terms=({1:((0,v,1),),2:((2,v,1),),3:((1,v,1),),4:((3,v,1),),5:((4,v,1),)}[comp])
   for c2,v2,s in terms:bs[block].append((c2,v2,int(a)*s%3))
  for block,es in bs.items():
   if es:out.update(self.contract(block,es))
  return {k:v%3 for k,v in out.items() if v%3}
 def action_support_hits(self,runtime,owner,p176,relations,dual):
  names={"b","c","p","q","r"};points=[]
  for k,c in dual.items():
   if k[:1]==b"Q" and k[1]==3 and len(k)>=5:
    try:_,lab,b=self.parse(k)
    except (ValueError,TypeError):continue
    if lab in names:points.append((lab,self.h0(self.e4,self.z4,self.dec(b,3))[0],int(c)%3))
  for ai,rel in enumerate(relations):
   grad,val=runtime.old.fox_gradient_without_sections(rel,self.e4);need(val==self.e4.identity,"action_identity");supports=[]
   for (comp,v),c in grad.items():
    b=p176["packed_joint_blob"](v,"action base");k=owner["row_key"](3,int(comp),b);qrow=self.transform({k:int(c)%3})
    for qk,qc in qrow.items():
     if qk[:1]==b"Q" and qk[1]==3:
      try:_,lab,hb=self.parse(qk)
      except (ValueError,TypeError):continue
      if lab in names:supports.append((lab,self.h0(self.e4,self.z4,self.dec(hb,3))[0],int(qc)%3))
   acc={}
   for lab,g,cg in points:
    for lab2,h,ch in supports:
     if lab==lab2:
      t=self.e4.mul(g,self.e4.inverse(h));tb=self.enc(t);acc[(ai,tb)]=(acc.get((ai,tb),0)+cg*ch)%3
   for (ai,tb),c in sorted(acc.items(),key=lambda x:(x[0][0],x[0][1])):
    if c:
     t=self.dec(tb,3);raw={}
     for (comp,v),a in runtime.old.fox_gradient_without_sections(relations[ai],self.e4)[0].items():
      blob=p176["packed_joint_blob"](self.e4.mul(t,v),"action");rk=owner["row_key"](3,int(comp),blob);x=(raw.get(rk,0)+int(a))%3
      if x:raw[rk]=x
      else:raw.pop(rk,None)
     yield self.transform(raw),{"family":"action","family_index":ai+1,"translation_blob":tb.hex(),"scalar":int(c)}
def normalize_occurrence(old_model,old,owner,p176,q,raw,ordinal):
 """Normal-map one occurrence before adding its ordinal tag."""
 physical={}
 for key,coef in raw.items():
  block,comp,blob=key[1],key[2],key[5:];rk=owner["row_key"](block,comp,blob);physical[rk]=(physical.get(rk,0)+int(coef))%3
 out=q.transform(physical)
 return {b"O"+bytes((ordinal,))+k:int(v)%3 for k,v in out.items() if int(v)%3}
def raw_occurrence(runtime,model,old,owner,p176,delta,word,ledger):
 """Return eleven separately tagged Fox rows from the frozen specs."""
 out={}
 for ordinal,spec in enumerate(model.specs,1):
  q=spec["quotient"];rel=model._substitute(word,spec["left"],spec["right"],spec["lift"])
  if spec["sign"]<0:rel=list(old.inv_word(rel))
  grad,val=old.fox_gradient_without_sections(rel,q);need(val==q.identity,"occurrence_identity")
  qw=model._substitute(delta,spec["left"],spec["right"],spec["lift"])
  translated=old.translate_vector(old.translate_vector(grad,q.eval(qw),q),spec["occurrence_prefix"],q)
  for (comp,value),coef in translated.items():
   blob=p176["packed_joint_blob"](value,"task421 occurrence");block=1 if spec["block"]<3 else 3;rk=owner["row_key"](block,int(comp),blob);x=(out.get((ordinal,rk),0)+int(coef))%3
   if x:out[(ordinal,rk)]=x
   else:out.pop((ordinal,rk),None)
 return out
def occurrence_seed(mod,runtime,model,old,owner,p176,q,delta,word,ledger,states):
 grouped={}
 for (ordinal,rk),coef in raw_occurrence(runtime,model,old,owner,p176,delta,word,ledger).items():grouped.setdefault(ordinal,{})[rk]=coef
 out={}
 for ordinal,row in grouped.items():out.update(normalize_occurrence(model,old,owner,p176,q,row,ordinal))
 ex,ey=exp_pair(word);need(ex%18==0 and ey%18==0,"occurrence_exponent_divisibility")
 for i,x in ((1,(ex//18)%3),(2,(ey//18)%3)):
  if x:out[b"N"+bytes((i,))]=x
 return {k:v for k,v in out.items() if v%3}
def normal_section(q,owner,p176,key,coefficient):
 """Sparse section of one Q-coordinate (including u/tau)."""
 block,label,blob=q.parse(key);grp=q.e3 if block<3 else q.e4;n=2 if block<3 else 5
 if label=="tau":
  z=q.z3 if block<3 else q.z4;value=q.h0(grp,z,grp.identity)[0];vals=[value,grp.mul(value,z),grp.mul(value,grp.mul(z,z))]
  return [(n,v,coefficient) for v in vals]
 if label in ("u0","u1"):
  rep=q.dec(blob,block);j=0 if label=="u0" else 1;return [(n,grp.mul(rep,(grp.identity if j==0 else (q.z3 if block<3 else q.z4))),coefficient)]
 mapping=({"b":1,"c":2} if block<3 else {"b":1,"c":3,"p":2,"q":4,"r":5})
 need(label in mapping,"normal_coordinate_section");return [(mapping[label],q.dec(blob,block),coefficient)]
def occurrence_actor(mod,runtime,model,old,owner,p176,q,row,ledger,letter):
 """Q_o L_actor iota_o on one tagged normal row, sparsely."""
 out={}
 for k,coef in row.items():
  if k[:1]==b"N":out[k]=(out.get(k,0)+int(coef))%3;continue
  ordinal=k[1];spec=model.specs[ordinal-1];grp=spec["quotient"];actor=grp.eval(model._substitute([letter],spec["left"],spec["right"],spec["lift"]));pre=spec["occurrence_prefix"];actor=grp.mul(pre,grp.mul(actor,grp.inverse(pre)))
  for comp,value,scale in normal_section(q,owner,p176,k[2:],int(coef)%3):
   moved=grp.mul(actor,value);blob=p176["packed_joint_blob"](moved,"task421 actor section");rk=owner["row_key"](int(spec["block"]),int(comp),blob);nrow=q.transform({rk:int(scale)%3})
   for nk,nc in nrow.items():
    tagged=b"O"+bytes((ordinal,))+nk;x=(out.get(tagged,0)+int(nc))%3
    if x:out[tagged]=x
    else:out.pop(tagged,None)
 return {k:v for k,v in out.items() if v%3}
def untag(row):
 out={}
 for k,v in row.items():out[k[2:] if k[:1]==b"O" else k]=(out.get(k[2:] if k[:1]==b"O" else k,0)+int(v))%3
 return {k:v for k,v in out.items() if v%3}
def six_action_words(old):
 phi={(2,3):[3,6,3,-6,-3],(2,5):[3,6,-3,-6,5,6,3,-6,-3],(2,6):[3,6,-3],(4,3):[3],(4,5):[5,6,5,-6,-5],(4,6):[5,6,-5]}
 words=[[-s,u,s]+inv(w) for (s,u),w in phi.items()]
 need([len(w) for w in words]==[8,12,6,4,8,6],"action_word_lengths")
 frozen=list(old.pure_relations(4)[5:11]);need(words==frozen,"action_roster_slice")
 return words
def positive_terminal(runtime,model,pres,occ,phys,target,coeff):
 """Strict v403 replay for a zero physical remainder."""
 atoms={};cache={}
 def src_atoms(index):
  if index in cache:return cache[index]
  s=occ.sources[index];f=s.get("family");out={}
  if f=="LEAF":out[(int(s["seed"]),())]=1
  elif f=="CONJUGATE":
   parent=bytes.fromhex(s["parent"]);need(parent in occ.expr,"ancestry_parent");pi=occ.order.index(parent)
   for (seed,pref),v in src_atoms_for_pivot(parent).items():out[(seed,pref+(int(s["letter"]),))]=(out.get((seed,pref+(int(s["letter"]),)),0)+v)%3
  else:raise RuntimeError("ancestry_family")
  cache[index]=out;return out
 def src_atoms_for_pivot(pivot):
  out={}
  for index,v in occ.expr[pivot].items():
   for atom,x in src_atoms(int(index)).items():out[atom]=(out.get(atom,0)+int(v)*x)%3
  return {k:v for k,v in out.items() if v%3}
 selected=[]
 for index,c in coeff.items():
  if not c:continue
  pivot=phys.order[int(index)];s=phys.sources[int(index)]
  need(s.get("family")=="PHYSICAL" and "occurrence_pivot" in s,"selected_action_requires_replay")
  op=bytes.fromhex(s["occurrence_pivot"])
  for atom,v in src_atoms_for_pivot(op).items():atoms[atom]=(atoms.get(atom,0)+int(c)*v)%3
 selected_atoms={k:v for k,v in atoms.items() if v%3};correction=[]
 for (seed,prefix),c in sorted(selected_atoms.items()):
  w=mul(list(prefix),list(pres["relators"][seed-1]),inv(list(prefix)));correction=mul(correction,w if c==1 else inv(w))
 ex,ey=exp_pair(correction);need(ex%54==0 and ey%54==0,"exactification_lattice")
 regs=pres.get("registered_q0_relators");need(regs and len(regs)>=12,"registered_q0_words")
 r3,r9,r12=regs[2],regs[8],regs[11];v0=mul(r9,r12,inv(r3),inv(r3));u0=mul(r9,poww(v0,-8))
 exact=mul(correction,poww(u0,-3*(ex//54)),poww(v0,-3*(ey//54)))
 need(exp_pair(exact)==(0,0),"exactification_exponents");states=runtime.states_direct(exact);need(all(x.a==x.q.identity for x in states),"exact_word_joint_identity")
 corr={}
 for index,c in coeff.items():corr=row_add(corr,phys.rows[phys.order[int(index)]],int(c))
 direct,replay=model.direct_column([],exact);need(replay.get("direct_all_seven_replay") is True,"exact_direct_replay")
 need(quotient.transform(direct)==corr,"fresh_fox_source_replay");need(not row_add(target,corr),"target_correction_replay")
 return {"status":"COMMON_WORD","literal_word":exact,"selected_ancestry":{"atoms":[[s,list(p),int(c)] for (s,p),c in sorted(selected_atoms.items())]},"selected_action_ancestry":[],"survivor_replay":True,"strict_replay":True,"exact_exponent_pair":[0,0],"direct_replay":True}
def run(a):
 st=time.monotonic();cert_raw=(ROOT/CERT[0]).read_bytes();need(len(cert_raw)==CERT[1] and sh(cert_raw)==CERT[2],"task418_certificate_pin");need(isinstance(json.loads(cert_raw),dict),"task418_certificate_object");t413=load(T413,"task421_t413");mod=load(OLD,"task421_occurrence_owner");receipt=t413["load_json"](t413,t413["JOINT"]);q3=t413["load_json"](t413,t413["Q3"]);pres=t413["compact"](receipt,q3);need(pres["compact_relator_count"]==44 and pres["relators_sha256"]==ROSTER,"roster")
 base=t413["bound_module"](t413["BASE"],"task421_base");core=base["load_task198_core"]();roof=t413["load_json"](base,base["ROOF"]);authority=types.SimpleNamespace(receipt=roof);layout=base["load_bound_module"](base["TASK379"],"task421_layout")["validate_layout"];ledger=layout(core,authority);runtime=core.Runtime(authority,core.Meter(dict(core.CAPS)));owner,g760,model=base["direct_physical_owner"](runtime);p176=base["load_bound_module"](base["TASK176"],"task421_p176")
 quotient=CorrectedPhysicalQuotient(owner,p176,runtime.e3,runtime.e4);target=quotient.transform(t413["target_row"](base,owner,runtime.old,runtime.e3,runtime.e4,g760,model));occ=Echelon();phys=Echelon();queue=deque();seed=0;actor_cursor=0
 binding=dig([T413,OLD,CERT,ROSTER,SCHEMA])
 def save(reason):
  if a.checkpoint:cp_write(a.checkpoint,{"phase":"occurrence_queue","seed_cursor":seed,"queue":[p.hex() for p in queue],"actor_cursor":actor_cursor,"occ_rows":occ.rows,"occ_order":occ.order,"occ_expr":occ.expr,"occ_sources":occ.sources,"physical_rows":phys.rows,"physical_order":phys.order,"physical_expr":phys.expr,"physical_sources":phys.sources,"physical_originals":phys.originals,"binding":binding,"reason":reason})
 def guard(phase):
  if a.seconds is not None and time.monotonic()-st>=a.seconds:return False
  if a.rss_bytes is not None and (rss() or 0)>=a.rss_bytes:return False
  return True
 if a.resume:
  s=cp_read(a.resume);need(s.get("binding")==binding,"checkpoint_binding");occ.rows=s["occ_rows"];occ.order=s["occ_order"];occ.expr=s["occ_expr"];occ.sources=s["occ_sources"];phys.rows=s["physical_rows"];phys.order=s["physical_order"];phys.expr=s["physical_expr"];phys.sources=s["physical_sources"];phys.originals=s.get("physical_originals",{});queue=deque(bytes.fromhex(x) for x in s.get("queue",[]));seed=int(s.get("seed_cursor",0));actor_cursor=int(s.get("actor_cursor",0))
 else:
  for i,word in enumerate(pres["relators"],1):
   if not guard("seeds"):save("resource_seeds");return {"status":UNKNOWN_RESOURCE,"reason":"seed resource stop","seed_cursor":i-1,"occurrence_rank":len(occ.order)}
   states=runtime.states_direct(list(word));need(all(x.a==x.q.identity for x in states),"seed_joint_identity");row=occurrence_seed(mod,runtime,model,runtime.old,owner,p176,quotient,[],list(word),ledger,states);rise,p=occ.add(row,{"family":"LEAF","seed":i,"delta_word":[]});seed=i
   if rise:queue.append(p);phys.add(quotient.transform(untag(occ.rows[p])),{"family":"PHYSICAL","occurrence_pivot":p.hex(),"seed":i})
  save("seeds_complete")
 if a.resume and seed<44:
  for i in range(seed+1,45):
   if not guard("seeds_resume"):save("resource_seeds_resume");return {"status":UNKNOWN_RESOURCE,"reason":"seed resource stop on resume","seed_cursor":i-1,"occurrence_rank":len(occ.order)}
   word=pres["relators"][i-1];states=runtime.states_direct(list(word));need(all(x.a==x.q.identity for x in states),"seed_joint_identity");row=occurrence_seed(mod,runtime,model,runtime.old,owner,p176,quotient,[],list(word),ledger,states);rise,p=occ.add(row,{"family":"LEAF","seed":i,"delta_word":[]});seed=i
   if rise:queue.append(p);phys.add(quotient.transform(untag(occ.rows[p])),{"family":"PHYSICAL","occurrence_pivot":p.hex(),"seed":i})
  save("seeds_resume_complete")
 while queue:
  if not guard("actors"):save("resource_actors");return {"status":UNKNOWN_RESOURCE,"reason":"actor resource stop","seed_cursor":seed,"occurrence_rank":len(occ.order),"physical_rank":len(phys.order)}
  p=queue.popleft();parent=occ.rows[p]
  for letter in (1,-1,2,-2):
   child=occurrence_actor(mod,runtime,model,runtime.old,owner,p176,quotient,parent,ledger,letter);rise,np=occ.add(child,{"family":"CONJUGATE","letter":letter,"parent":p.hex()});actor_cursor+=1
   if rise:queue.append(np);phys.add(quotient.transform(untag(occ.rows[np])),{"family":"PHYSICAL","occurrence_pivot":np.hex(),"actor":letter})
  if len(occ.order)%32==0:print("phase=occurrence_queue occurrence_rank=%d frontier=%d physical_rank=%d owner_rss_bytes=%s elapsed=%.3f"%(len(occ.order),len(queue),len(phys.order),rss(),time.monotonic()-st),flush=True)
 save("occurrence_exhausted")
 actions=six_action_words(runtime.old)
 for rel in actions:
  grad,val=runtime.old.fox_gradient_without_sections(rel,runtime.e4);need(val==runtime.e4.identity,"action_identity");raw={}
  for (comp,value),coef in grad.items():
   blob=p176["packed_joint_blob"](value,"action gate");rk=owner["row_key"](3,int(comp),blob);raw[rk]=(raw.get(rk,0)+int(coef))%3
  for k in quotient.transform(raw):
   need(k[:1]==b"Q" and k[1]==3 and quotient.parse(k)[1] in {"b","c","p","q","r"},"action_closed_survivor")
 while True:
  if not guard("six_action"):save("resource_six_action");return {"status":UNKNOWN_RESOURCE,"reason":"six-action resource stop","occurrence_rank":len(occ.order),"physical_rank":len(phys.order)}
  dual,rem,coeff=phys.dual(target)
  if dual is None:
   try:return positive_terminal(runtime,model,pres,occ,phys,target,coeff)
   except Exception as exc:save("target_zero_strict_replay_failed");return {"status":UNKNOWN,"reason":"target_zero_requires_v403_replay:"+str(exc),"occurrence_rank":len(occ.order),"physical_rank":len(phys.order)}
  added=False
  for candidate,source in quotient.action_support_hits(runtime,owner,p176,actions,dual):
   direct=sum(int(v)*int(dual.get(k,0)) for k,v in candidate.items())%3;need(direct==int(source.get("scalar",0))%3,"action_scalar_pairing");rise,_=phys.add(candidate,source);actor_cursor+=1
   if rise:added=True
  if added:save("six_action_rank_rise");continue
  save("exhausted_incomplete_replay");return {"status":UNKNOWN_RESOURCE,"reason":"exact occurrence and six-action closure; independent positive/negative replay pending","occurrence_rank":len(occ.order),"physical_rank":len(phys.order),"actor_cursor":actor_cursor}
def fixture():
 # Small ownership gates; production queue is not invoked locally.
 e=Echelon();need(e.add({b"a":1},{"family":"LEAF","seed":1})[0],"fixture_seed");need(not e.add({b"a":1},{"family":"duplicate"})[0],"fixture_duplicate")
 st={"phase":"occurrence_queue","seed_cursor":3,"queue":["61"],"actor_cursor":4,"occ_rows":{b"a":{b"a":1}},"occ_order":[b"a"],"occ_expr":{b"a":{0:1}},"occ_sources":[{"family":"LEAF"}],"physical_rows":{},"physical_order":[],"physical_expr":{},"physical_sources":[]};raw=marshal.dumps({"schema":SCHEMA+"/checkpoint","state":st});o=__import__("io").BytesIO();
 with gzip.GzipFile(fileobj=o,mode="wb",compresslevel=1,mtime=0) as z:marshal.dump({"schema":SCHEMA+"/checkpoint","state":st},z)
 need(marshal.loads(gzip.decompress(o.getvalue()))["state"]==st,"fixture_checkpoint_roundtrip")
 return {"status":"FIXTURE_PASS","exact_seed_count":44,"actors":[1,-1,2,-2],"resume_seed_and_actor":True,"queue_pop_front_avoided":True,"action_slice":"[5:11]"}
def main():
 ap=argparse.ArgumentParser();ap.add_argument("--mode",choices=("FIXTURE","PRODUCTION"),default="PRODUCTION");ap.add_argument("--output");ap.add_argument("--checkpoint");ap.add_argument("--resume");ap.add_argument("--seconds",type=float,default=9000);ap.add_argument("--rss-bytes",type=int,default=5700000000);a=ap.parse_args();t=time.monotonic()
 try:o=fixture() if a.mode=="FIXTURE" else run(a);status=o["status"]
 except Exception as e:status=UNKNOWN;o={"status":status,"reason":str(e)}
 result={"schema":SCHEMA,"status":status,"terminal":status,"complete":status=="COMMON_WORD","a0":o,"pins":{"task413":{"path":T413[0],"bytes":T413[1],"sha256":T413[2]},"occurrence_owner":{"path":OLD[0],"bytes":OLD[1],"sha256":OLD[2]},"task418_certificate":{"path":CERT[0],"bytes":CERT[1],"sha256":CERT[2]}},"claim_boundary":{"common_word":status=="COMMON_WORD","A0_membership":status=="COMMON_WORD","fake":False,"Ihara_witness":False,"compatible_lift":False,"verified":False},"elapsed_seconds":time.monotonic()-t}
 if a.output:
  p=ROOT/a.output;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(json.dumps(result,sort_keys=True,separators=(",",":"),default=str).encode()+b"\n")
 print("R07_A0_PB34_DIRECT_QUOTIENT_OWNER_V3 "+status,flush=True);return 0
if __name__=="__main__":raise SystemExit(main())
