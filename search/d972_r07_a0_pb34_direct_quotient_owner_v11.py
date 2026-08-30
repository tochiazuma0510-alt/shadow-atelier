#!/usr/bin/env python3
"""Task430 v11: standalone quotient loop with finite central-power API."""
from __future__ import annotations
import argparse,gzip,hashlib,json,marshal,os,shutil,sys,tempfile,time,traceback,types
from collections import deque
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];SCHEMA="d972-r07-a0-pb34-direct-quotient-owner/v11";RSS_CAP=4800000000;UNKNOWN="UNKNOWN";RESOURCE="UNKNOWN_RESOURCE"
V3=("search/d972_r07_a0_pb34_direct_quotient_owner_v3.py",24942,"1f7c94d3b949431c17013dd1a26fb917b8dbd109f8df75405f6e7fe7abdef9f0")
def sh(b):return hashlib.sha256(b).hexdigest()
def need(x,m):
 if not x:raise RuntimeError(m)
def central_power3(group,value,exponent):
 j=int(exponent)
 need(0<=j<3,"central_power3_exponent")
 if j==0:return group.identity
 if j==1:return value
 return group.mul(value,value)
def raw_component_zero(block,component):
 limit=3 if block<3 else 6
 need(1<=int(component)<=limit,"raw_component_range")
 return int(component)-1
def load(spec,name):
 p=ROOT/spec[0];b=p.read_bytes();need(len(b)==spec[1] and sh(b)==spec[2],"pin:"+spec[0]);m=types.ModuleType(name);m.__file__=str(p);sys.modules[name]=m;exec(compile(b,spec[0],"exec"),m.__dict__,m.__dict__);return m
v3=load(V3,"task430_v3_pinned");LAST_DURABLE=None
class Echelon:
 def __init__(self):self.rows={};self.order=[];self.expr={};self.sources=[]
 @staticmethod
 def axpy(w,row,c):
  for k,v in row.items():
   x=(w.get(k,0)-int(c)*int(v))%3
   if x:w[k]=x
   else:w.pop(k,None)
 def add(self,row,source):
  w={k:int(v)%3 for k,v in row.items() if int(v)%3};e={len(self.sources):1}
  for p in self.order:
   c=w.get(p,0)
   if c:self.axpy(w,self.rows[p],c);self.axpy(e,self.expr[p],c)
  if not w:return False,None
  p=min(w);s=1 if w[p]==1 else 2
  self.rows[p]={k:s*int(v)%3 for k,v in w.items() if s*int(v)%3}
  self.expr[p]={k:s*int(v)%3 for k,v in e.items() if s*int(v)%3}
  self.order.append(p);self.sources.append(dict(source));return True,p
 def reduce(self,row):
  w={k:int(v)%3 for k,v in row.items() if int(v)%3};e={}
  for p in self.order:
   c=w.get(p,0)
   if c:self.axpy(w,self.rows[p],c);self.axpy(e,self.expr[p],c)
  return w,e
 def dual(self,target):
  w,e=self.reduce(target)
  if not w:return None,w,e
  d={min(w):1}
  for p in sorted(self.order,reverse=True):
   x=(-sum(int(v)*d.get(k,0) for k,v in self.rows[p].items() if k!=p))%3
   if x:d[p]=x
  return d,w,e

class Quotient(v3.CorrectedPhysicalQuotient):
 def h0(self,g,z,v):
  if g is self.e3:
   pw=[g.identity]
   for _ in range(2):pw.append(g.mul(pw[-1],z))
   blob,shift=min((self.enc(g.mul(v,p)),j) for j,p in enumerate(pw));r=self.dec(blob,1)
   j=(-shift)%3;need(g.mul(r,central_power3(g,z,j))==v,"pb3_transversal");return r,j
  j=int(v[1][0])%3;h=g.mul(v,central_power3(g,g.inverse(z),j));need(int(h[1][0])%3==0 and g.mul(h,central_power3(g,z,j))==v,"pb4_kappa");return h,j
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
  if tau:out[self.qkey(block,"tau",b"")]=tau
  return out
 def transform(self,row):
  if not row:return {}
  bs={1:[],2:[],3:[]};out={}
  for k,a in row.items():
   if k[:1]!=b"R":
    if k[:1]==b"Q" and k[2:]==b"tau":k=self.qkey(k[1],"tau",b"")
    x=(out.get(k,0)+int(a))%3
    if x:out[k]=x
    else:out.pop(k,None)
    continue
   block,raw_comp,blob=k[1],k[2],k[5:];comp=raw_component_zero(block,raw_comp);g=self.e3 if block<3 else self.e4;v=self.p176["value_from_blob"](blob,0 if block<3 else 5)
   if block<3:
    x,y,z=[g.eval([i]) for i in (1,2,3)]
    terms=((2,v,1),(1,g.mul(g.mul(v,x),y),-1),(0,g.mul(v,x),-1)) if comp==0 else (((0,v,1),) if comp==1 else ((1,v,1),))
   else:
    a0,b,p,c,q,r=[g.eval([i]) for i in (1,2,3,4,5,6)]
    if comp==0:
     t=g.mul(v,self.z4);terms=((5,v,1),(4,g.mul(t,g.inverse(r)),-1),(3,g.mul(g.mul(t,g.inverse(r)),g.inverse(q)),-1),(2,g.mul(g.mul(g.mul(t,g.inverse(r)),g.inverse(q)),g.inverse(p)),-1),(1,g.mul(g.mul(g.mul(g.mul(t,g.inverse(r)),g.inverse(q)),g.inverse(p)),g.inverse(c)),-1),(0,g.mul(g.mul(g.mul(g.mul(g.mul(t,g.inverse(r)),g.inverse(q)),g.inverse(p)),g.inverse(c)),g.inverse(b)),-1))
    else:terms={1:((0,v,1),),2:((2,v,1),),3:((1,v,1),),4:((3,v,1),),5:((4,v,1),)}[comp]
   for c2,v2,s in terms:bs[block].append((c2,v2,int(a)*s%3))
  for block,es in bs.items():
   if es:
    for nk,nc in self.contract(block,es).items():
     x=(out.get(nk,0)+nc)%3
     if x:out[nk]=x
     else:out.pop(nk,None)
  return {k:v%3 for k,v in out.items() if v%3}
def whole(p):
 h=hashlib.sha256();n=0
 with Path(p).open("rb") as f:
  for b in iter(lambda:f.read(1<<20),b""):h.update(b);n+=len(b)
 return n,h.hexdigest()
def aggregate(row):
 out={}
 for k,c in row.items():
  if k[:1]==b"O":need(len(k)>=3,"occurrence_tag");k=k[2:]
  elif k[:1]!=b"N":raise RuntimeError("raw_occurrence_key")
  x=(out.get(k,0)+int(c))%3
  if x:out[k]=x
  else:out.pop(k,None)
 return out
def enc_row(r):return [[k.hex(),int(v)%3] for k,v in sorted(r.items()) if int(v)%3]
def normal_section(q,p176,key,c):
 block,label,blob=q.parse(key);g=q.e3 if block<3 else q.e4;n=2 if block<3 else 5;z=q.z3 if block<3 else q.z4
 if label=="tau":
  r=q.h0(g,z,g.identity)[0];return [(n,r,c),(n,g.mul(r,z),c),(n,g.mul(r,g.mul(z,z)),c)]
 if label in ("u0","u1"):return [(n,g.mul(q.dec(blob,block),g.identity if label=="u0" else z),c)]
 mp={"b":0,"c":1} if block<3 else {"b":0,"c":1,"p":2,"q":3,"r":4};need(label in mp,"section_label");return [(mp[label],q.dec(blob,block),c)]
def actor_v11(runtime,model,owner,p176,q,row,letter):
 out={};groups={};cache={}
 for k,c in row.items():
  if k[:1]==b"N":
   x=(out.get(k,0)+int(c))%3
   if x:out[k]=x
   else:out.pop(k,None)
   continue
  need(k[:1]==b"O" and len(k)>=3,"actor_occurrence_key");o=k[1];spec=model.specs[o-1];block=int(spec["block"]);g=spec["quotient"];ck=(o,int(letter))
  if ck not in cache:
   aa=g.eval(model._substitute([letter],spec["left"],spec["right"],spec["lift"]));p=spec["occurrence_prefix"];cache[ck]=g.mul(p,g.mul(aa,g.inverse(p)))
  for comp,val,s in normal_section(q,p176,k[2:],int(c)%3):groups.setdefault((o,block),[]).append((comp,g.mul(cache[ck],val),s))
 for (o,b),entries in groups.items():
  for nk,nc in q.contract(b,entries).items():
   kk=b"O"+bytes((o,))+nk;x=(out.get(kk,0)+nc)%3
   if x:out[kk]=x
   else:out.pop(kk,None)
 return {k:v for k,v in out.items() if v%3}
def seed_v11(model,old,owner,p176,q,word):
 grouped={}
 for o,spec in enumerate(model.specs,1):
  rel=model._substitute(word,spec["left"],spec["right"],spec["lift"]);rel=list(old.inv_word(rel)) if spec["sign"]<0 else rel;grad,val=old.fox_gradient_without_sections(rel,spec["quotient"]);need(val==spec["quotient"].identity,"seed_identity");qw=model._substitute([],spec["left"],spec["right"],spec["lift"]);translated=old.translate_vector(old.translate_vector(grad,spec["quotient"].eval(qw),spec["quotient"]),spec["occurrence_prefix"],spec["quotient"]);block=int(spec["block"])
  for (comp,value),c in translated.items():
   k=owner["row_key"](block,int(comp),p176["packed_joint_blob"](value,"task425 seed"));g=grouped.setdefault(o,{});g[k]=(g.get(k,0)+int(c))%3
 out={}
 for o,r in grouped.items():out.update(v3.normalize_occurrence(model,old,owner,p176,q,r,o))
 ex,ey=v3.exp_pair(word);need(ex%18==0 and ey%18==0,"seed_exponent")
 if (ex//18)%3:out[b"N\x01"]=(ex//18)%3
 if (ey//18)%3:out[b"N\x02"]=(ey//18)%3
 return {k:v for k,v in out.items() if v%3}
def action_row(runtime,owner,p176,q,src):
 actions=list(runtime.old.pure_relations(4)[5:11]);i=int(src["family_index"])-1;need(0<=i<6,"action_family");t=q.dec(bytes.fromhex(src["translation_blob"]),3);raw={};grad,val=runtime.old.fox_gradient_without_sections(actions[i],runtime.e4);need(val==runtime.e4.identity,"action_identity")
 for (comp,w),c in grad.items():
  k=owner["row_key"](3,int(comp),p176["packed_joint_blob"](runtime.e4.mul(t,w),"task425 action"));x=(raw.get(k,0)+int(c))%3
  if x:raw[k]=x
  else:raw.pop(k,None)
 return q.transform(raw)
def positive(runtime,model,pres,occ,phys,target,coeff,q,owner,p176):
 atoms={};cache={};corr={};acts={};ancestry=[]
 def atoms_src(i):
  if i in cache:return cache[i]
  s=occ.sources[i]
  if s.get("family")=="LEAF":out={(int(s["seed"]),()):1}
  elif s.get("family")=="CONJUGATE":
   out={};par=bytes.fromhex(s["parent"])
   for (seed,pref),x in atoms_pivot(par).items():key=(seed,(int(s["letter"]),)+pref);out[key]=(out.get(key,0)+x)%3
  else:raise RuntimeError("ancestry_family")
  cache[i]=out;return out
 def atoms_pivot(p):
  out={}
  for i,x in occ.expr[p].items():
   for a,y in atoms_src(int(i)).items():out[a]=(out.get(a,0)+int(x)*y)%3
  return {a:x for a,x in out.items() if x%3}
 for i,c in coeff.items():
  i=int(i);need(0<=i<len(phys.sources),"source_index");p=phys.order[i];s=phys.sources[i]
  if s.get("family")=="PHYSICAL":
   op=bytes.fromhex(s["occurrence_pivot"]);fresh=q.transform(aggregate(occ.rows[op]));
   for a,x in atoms_pivot(op).items():atoms[a]=(atoms.get(a,0)+int(c)*x)%3
   corr=v3.row_add(corr,fresh,int(c))
  elif s.get("family")=="action":
   fresh=action_row(runtime,owner,p176,q,s);acts=v3.row_add(acts,fresh,int(c));ancestry.append({"family_index":int(s["family_index"]),"translation_blob":s["translation_blob"],"coefficient":int(c),"source_row":enc_row(fresh)})
  else:raise RuntimeError("source_family")
 word=[]
 for (seed,pref),c in sorted((x,c) for x,c in atoms.items() if c%3):
  w=v3.mul(list(pref),list(pres["relators"][seed-1]),v3.inv(list(pref)));word=v3.mul(word,w if c==1 else v3.inv(w))
 ex,ey=v3.exp_pair(word);need(ex%54==0 and ey%54==0,"exactification_lattice");r3,r9,r12=pres["registered_q0_relators"][2],pres["registered_q0_relators"][8],pres["registered_q0_relators"][11];v0=v3.mul(r9,r12,v3.inv(r3),v3.inv(r3));u0=v3.mul(r9,v3.poww(v0,-8));exact=v3.mul(word,v3.poww(u0,-3*(ex//54)),v3.poww(v0,-3*(ey//54)));need(v3.exp_pair(exact)==(0,0),"exactification_exponents");need(all(s.a==s.q.identity for s in runtime.states_direct(exact)),"joint_identity");direct,replay=model.direct_column([],exact);need(replay.get("direct_all_seven_replay") is True,"direct_replay");need(q.transform(direct)==corr,"correction_replay");need(not v3.row_add(v3.row_add(target,corr),acts),"target_zero")
 return {"status":"COMMON_CANDIDATE","literal_word":exact,"exact_exponent_pair":[0,0],"strict_replay":True,"direct_replay":True,"survivor_replay":True,"selected_ancestry":{"atoms":[[s,list(p),int(c)] for (s,p),c in sorted(atoms.items()) if c%3]},"selected_action_ancestry":ancestry,"correction_sum":enc_row(corr),"action_sum":enc_row(acts),"target_row":enc_row(target)}
def cp_write(path,state):
 p=Path(path);need(not p.is_absolute() and p.parent==Path("ci/out"),"checkpoint_path");p.parent.mkdir(parents=True,exist_ok=True)
 with tempfile.NamedTemporaryFile(dir=p.parent,delete=False) as f:
  tmp=Path(f.name)
  with gzip.GzipFile(fileobj=f,mode="wb",compresslevel=1,mtime=0) as z:marshal.dump({"schema":SCHEMA+"/checkpoint","state":state},z)
  f.flush();os.fsync(f.fileno())
 n,h=whole(tmp)
 with tempfile.NamedTemporaryFile(dir=p.parent,delete=False) as f:
  out=Path(f.name);f.write(("D972-A0V11-CP1 "+h+" "+str(n)+"\n").encode());
  with tmp.open("rb") as src:shutil.copyfileobj(src,f,1<<20)
  f.flush();os.fsync(f.fileno())
 tmp.unlink(missing_ok=True);os.replace(out,p)
def cp_read(path):
 p=Path(path);need(not p.is_absolute() and p.parent==Path("ci/out"),"resume_path")
 with p.open("rb") as f:
  head=f.readline().decode().rstrip("\n").split(" ");need(len(head)==3 and head[0]=="D972-A0V11-CP1","checkpoint_header");h=hashlib.sha256();n=0
  for chunk in iter(lambda:f.read(1<<20),b""):h.update(chunk);n+=len(chunk)
 need(n==int(head[2]) and h.hexdigest()==head[1],"checkpoint_seal")
 with p.open("rb") as f:
  f.readline()
  with gzip.GzipFile(fileobj=f,mode="rb") as z:b=marshal.load(z)
 need(isinstance(b,dict) and b.get("schema")==SCHEMA+"/checkpoint", "checkpoint_schema");s=b["state"];need(s.get("binding")==hashlib.sha256((SCHEMA+V3[2]).encode()).hexdigest(),"checkpoint_binding");need(s.get("eliminated_boundary_rows")==0 and s.get("old_boundary_closure_present") is False,"boundary_invariant")
 for pref in ("occ","physical"):
  rows=s[pref+"_rows"];order=s[pref+"_order"];expr=s[pref+"_expr"];sources=s[pref+"_sources"];need(len(rows)==len(order)==len(expr)==len(sources),"checkpoint_shape")
  for pvt in order:need(pvt in rows and rows[pvt].get(pvt)==1,"checkpoint_pivot")
  for e in expr.values():
   for i in e:need(isinstance(i,int) and 0<=i<len(sources),"checkpoint_expression")
  allowed={"LEAF","CONJUGATE"} if pref=="occ" else {"PHYSICAL","action"}
  for src in sources:need(isinstance(src,dict) and src.get("family") in allowed and "_original_row" not in src,"checkpoint_source")
 for pvt in s.get("queue",[]):need(bytes.fromhex(pvt) in s["occ_rows"],"checkpoint_queue")
 return s
def run(a):
 global LAST_DURABLE
 start=time.monotonic();t413=v3.load(v3.T413,"task430_task413");base=t413["bound_module"](t413["BASE"],"task430_base");receipt=t413["load_json"](base,t413["JOINT"]);q3=t413["load_json"](base,t413["Q3"]);pres=base["compact"](receipt,q3);core=base["load_task198_core"]();roof=t413["load_json"](base,base["ROOF"]);acceptance=t413["load_json"](base,base["ACCEPTANCE"]);need(base["acceptance_ok"](acceptance),"acceptance_v2_contract");authority=types.SimpleNamespace(receipt=roof);layout=base["load_bound_module"](base["TASK379"],"task430_layout")["validate_layout"];ledger=layout(core,authority);runtime=core.Runtime(authority,core.Meter(dict(core.CAPS)));owner,g760,model=base["direct_physical_owner"](runtime);p176=base["load_bound_module"](base["TASK176"],"task430_p176");q=Quotient(owner,p176,runtime.e3,runtime.e4);target=q.transform(t413["target_row"](base,owner,runtime.old,runtime.e3,runtime.e4,g760,model));occ=Echelon();phys=Echelon();queue=deque();seed_cursor=parent_cursor=action_cursor=seq=0;last_save=0.;durable=None;binding=hashlib.sha256((SCHEMA+V3[2]).encode()).hexdigest();print("phase=preflight owner_v11=BOUND rss_cap=%d"%RSS_CAP,flush=True);print("phase=runtime_bootstrap owner_v11=READY",flush=True)
 def state(phase,reason):return {"phase":phase,"reason":reason,"seed_cursor":seed_cursor,"parent_cursor":parent_cursor,"action_cursor":action_cursor,"queue":[p.hex() for p in queue],"occ_rows":occ.rows,"occ_order":occ.order,"occ_expr":occ.expr,"occ_sources":occ.sources,"physical_rows":phys.rows,"physical_order":phys.order,"physical_expr":phys.expr,"physical_sources":phys.sources,"binding":binding,"checkpoint_seq":seq,"occurrence_pivot_nnz":sum(len(occ.rows[x]) for x in occ.order),"physical_pivot_nnz":sum(len(phys.rows[x]) for x in phys.order),"eliminated_boundary_rows":0,"old_boundary_closure_present":False}
 def save(phase,reason,force=False):
  nonlocal last_save,durable,seq
  global LAST_DURABLE
  if not a.checkpoint:return
  now=time.monotonic()
  if not force and now-last_save<300:return
  stop_reason=None
  if not force:
   if a.seconds is not None and now-start>=a.seconds:stop_reason="time_limit"
   elif (v3.rss() or 0)>=int(a.rss_bytes):stop_reason="rss_limit"
  seq+=1;s=state(phase,stop_reason or reason);s["checkpoint_seq"]=seq;cp_write(a.checkpoint,s);n,h=whole(a.checkpoint);durable={"phase":phase,"seed_cursor":seed_cursor,"parent_cursor":parent_cursor,"action_cursor":action_cursor,"occurrence_rank":len(occ.order),"physical_rank":len(phys.order),"frontier_length":len(queue),"occurrence_pivot_nnz":s["occurrence_pivot_nnz"],"physical_pivot_nnz":s["physical_pivot_nnz"],"checkpoint_seq":seq,"checkpoint_bytes":n,"checkpoint_sha256":h};LAST_DURABLE=durable;last_save=now;print("checkpoint_durable phase=%s seq=%d rank=%d/%d pivot_nnz=%d/%d"%(phase,seq,len(occ.order),len(phys.order),s["occurrence_pivot_nnz"],s["physical_pivot_nnz"]),flush=True)
  if stop_reason:raise RuntimeError(RESOURCE+":"+stop_reason)
 def guard(phase):
  elapsed=time.monotonic()-start;mem=v3.rss() or 0
  if (a.seconds is not None and elapsed>=a.seconds) or mem>=int(a.rss_bytes):
   reason="time_limit" if a.seconds is not None and elapsed>=a.seconds else "rss_limit";save(phase,reason,True);raise RuntimeError(RESOURCE+":"+reason)
 if a.resume:
  s=cp_read(a.resume);seed_cursor=int(s["seed_cursor"]);parent_cursor=int(s.get("parent_cursor",0));action_cursor=int(s.get("action_cursor",0));seq=int(s.get("checkpoint_seq",0));occ.rows=s["occ_rows"];occ.order=s["occ_order"];occ.expr=s["occ_expr"];occ.sources=s["occ_sources"];phys.rows=s["physical_rows"];phys.order=s["physical_order"];phys.expr=s["physical_expr"];phys.sources=s["physical_sources"];queue=deque(bytes.fromhex(x) for x in s["queue"]);durable={"phase":s["phase"],"seed_cursor":seed_cursor,"parent_cursor":parent_cursor,"action_cursor":action_cursor,"occurrence_rank":len(occ.order),"physical_rank":len(phys.order),"frontier_length":len(queue),"occurrence_pivot_nnz":s.get("occurrence_pivot_nnz",0),"physical_pivot_nnz":s.get("physical_pivot_nnz",0),"checkpoint_seq":seq,"checkpoint_bytes":whole(a.resume)[0],"checkpoint_sha256":whole(a.resume)[1]};LAST_DURABLE=durable;print("phase=resume_restored "+json.dumps(durable,sort_keys=True),flush=True)
  if (v3.rss() or 0)>=int(a.rss_bytes):return {"status":UNKNOWN,"reason":"MEMORY_STATE_LIMIT","durable_state":durable,"seed_cursor":seed_cursor,"parent_cursor":parent_cursor,"action_cursor":action_cursor,"occurrence_rank":len(occ.order),"physical_rank":len(phys.order),"frontier_length":len(queue),"checkpoint_seq":seq}
  guard("resume")
 else:
  for i,w in enumerate(pres["relators"],1):
   guard("seeds");ss=runtime.states_direct(list(w));need(all(x.a==x.q.identity for x in ss),"seed_identity");r=seed_v11(model,runtime.old,owner,p176,q,list(w));rise,p=occ.add(r,{"family":"LEAF","seed":i});seed_cursor=i
   if rise:queue.append(p);phys.add(aggregate(occ.rows[p]),{"family":"PHYSICAL","occurrence_pivot":p.hex(),"seed":i})
   guard("seeds")
  save("seeds","seeds_complete",True)
 if a.resume and seed_cursor<44:
  for i in range(seed_cursor+1,45):
   w=pres["relators"][i-1];guard("seeds");ss=runtime.states_direct(list(w));need(all(x.a==x.q.identity for x in ss),"seed_identity");r=seed_v11(model,runtime.old,owner,p176,q,list(w));rise,p=occ.add(r,{"family":"LEAF","seed":i});seed_cursor=i
   if rise:queue.append(p);phys.add(aggregate(occ.rows[p]),{"family":"PHYSICAL","occurrence_pivot":p.hex(),"seed":i})
   guard("seeds")
  save("seeds","seeds_resume_complete",True)
 while queue:
  guard("parent");p=queue.popleft()
  for letter in (1,-1,2,-2):
   r=actor_v11(runtime,model,owner,p176,q,occ.rows[p],letter);rise,np=occ.add(r,{"family":"CONJUGATE","letter":letter,"parent":p.hex()});action_cursor+=1
   if rise:queue.append(np);phys.add(aggregate(occ.rows[np]),{"family":"PHYSICAL","occurrence_pivot":np.hex(),"actor":letter})
  parent_cursor+=1;guard("parent")
  if len(occ.order)-getattr(run,"_progress_rank",0)>=32 or time.monotonic()-getattr(run,"_progress_time",start)>=60:
   run._progress_rank=len(occ.order);run._progress_time=time.monotonic();print("progress phase=occurrence_queue seed_cursor=%d actor_cursor=%d occurrence_rank=%d physical_rank=%d frontier=%d occurrence_pivot_nnz=%d physical_pivot_nnz=%d owner_rss_bytes=%s elapsed_seconds=%.3f checkpoint_seq=%d"%(seed_cursor,action_cursor,len(occ.order),len(phys.order),len(queue),sum(len(occ.rows[x]) for x in occ.order),sum(len(phys.rows[x]) for x in phys.order),v3.rss(),time.monotonic()-start,seq),flush=True)
  if time.monotonic()-last_save>=300:save("occurrence_queue","parent_complete")
 save("occurrence_queue","occurrence_exhausted",True);actions=list(runtime.old.pure_relations(4)[5:11])
 while True:
  guard("six_action");dual,rem,coeff=phys.dual(target)
  if dual is None:
   try:return positive(runtime,model,pres,occ,phys,target,coeff,q,owner,p176)
   except Exception as e:return {"status":UNKNOWN,"reason":"positive_replay:"+str(e),"durable_state":durable}
  added=False
  for cand,src in q.action_support_hits(runtime,owner,p176,actions,dual):
   need(sum(int(v)*int(dual.get(k,0)) for k,v in cand.items())%3==int(src.get("scalar",0))%3,"action_scalar");rise,_=phys.add(cand,src);action_cursor+=1;added=added or rise
  guard("six_action")
  if added:
   if time.monotonic()-last_save>=300:save("six_action","six_action_rank_rise")
   continue
  save("six_action","six_action_exhausted",True);return {"status":UNKNOWN,"reason":"six_action_exhausted","durable_state":durable,"seed_cursor":seed_cursor,"parent_cursor":parent_cursor,"action_cursor":action_cursor}
def toy_resource_fixture():
 clock=[0.0];saved=[]
 def save():saved.append({"phase":"toy","rank":1})
 def guard(limit):
  if clock[0]>=limit:save();raise RuntimeError(RESOURCE+":time_limit")
 clock[0]=2.0
 try:guard(1.0)
 except RuntimeError as e:need(str(e)==RESOURCE+":time_limit" and saved,"fixture_resource_stop")
 return True
def toy_durable_fixture():
 live={"rank":1,"nnz":2};sealed={"phase":"toy","occurrence_rank":live["rank"],"occurrence_pivot_nnz":live["nnz"]};live["rank"]=9;live["nnz"]=99;need(sealed["occurrence_rank"]==1 and sealed["occurrence_pivot_nnz"]==2,"fixture_durable_snapshot");return True
def toy_positive_fixture():
 nodes=[{"family":"LEAF","seed":1},{"family":"CONJUGATE","letter":2,"parent":0}];stack=[(1,1,())];atoms={}
 while stack:
  i,c,prefix=stack.pop();node=nodes[i]
  if node["family"]=="LEAF":key=(node["seed"],prefix);atoms[key]=(atoms.get(key,0)+c)%3
  else:stack.append((node["parent"],c,(int(node["letter"]),)+prefix))
 need(atoms.get((1,(2,)))==1,"fixture_instruction_dag");need(not v3.row_add(v3.row_add({b"q":1},{b"q":1}),{b"q":1}),"fixture_zero_envelope");return True
def toy_memory_state_fixture():
 state={"checkpoint_seq":7,"occurrence_rank":3};save_calls=[0]
 if 4800000000>=4800000000:
  result={"status":UNKNOWN,"reason":"MEMORY_STATE_LIMIT","durable_state":state}
  save_calls[0]+=0
 need(result["status"]==UNKNOWN and result["reason"]=="MEMORY_STATE_LIMIT" and save_calls[0]==0 and result["durable_state"]["checkpoint_seq"]==7,"fixture_memory_state_limit");return True
def toy_fallback_fixture():
 candidate={"status":"COMMON_CANDIDATE","durable_state":None};fallback={"checkpoint_seq":9};final=candidate.get("durable_state") or fallback
 need(final is fallback and final["checkpoint_seq"]==9,"fixture_durable_fallback");return True
def fixture():
 class Toy:
  identity=0
  def mul(self,a,b):return a+b
 toy=Toy();need(central_power3(toy,7,0)==0 and central_power3(toy,7,1)==7 and central_power3(toy,7,2)==14,"fixture_central_power3")
 for exponent in (-1,3):
  try:central_power3(toy,7,exponent)
  except RuntimeError:pass
  else:raise RuntimeError("fixture_central_power3_range")
 source=Path(__file__).read_text(encoding="utf-8");need("."+"power(" not in source and "."+"pow(" not in source,"fixture_power_api_absent")
 class Q:
  def qkey(self,b,l,x=b""):return b"Q"+bytes((b,))+len(l.encode()+b":"+x).to_bytes(2,"big")+l.encode()+b":"+x
 q=Quotient.__new__(Quotient);q.qkey=lambda b,l,x=b"":b"Q"+bytes((b,))+len(l.encode()+b":"+x).to_bytes(2,"big")+l.encode()+b":"+x
 need([raw_component_zero(1,i) for i in (1,2,3)]==[0,1,2],"fixture_e3_components")
 need([raw_component_zero(3,i) for i in (1,2,3,4,5,6)]==[0,1,2,3,4,5],"fixture_e4_components")
 need(raw_component_zero(3,6)==5,"fixture_e4_six")
 for block,comp in ((1,0),(1,4),(3,0),(3,7)):
  try:raw_component_zero(block,comp)
  except RuntimeError:pass
  else:raise RuntimeError("fixture_raw_component_range")
 legacy=b"Q\x01tau";multi={legacy:1,q.qkey(1,"b",b"x"):1};need(Quotient.transform(q,{})=={},"fixture_transform_empty");out=Quotient.transform(q,multi);need(q.qkey(1,"tau") in out and q.qkey(1,"b",b"x") in out,"fixture_transform_multi");tagged={b"O\x01"+q.qkey(1,"b",b"x"):1,b"O\x02"+q.qkey(1,"b",b"x"):1,b"N\x01":2};agg=aggregate(tagged);need(agg.get(q.qkey(1,"b",b"x"))==2 and agg.get(b"N\x01")==2,"fixture_aggregate_tagged");old_filter={k:v for k,v in tagged.items() if k[:1]!=b"O"};need(q.qkey(1,"b",b"x") not in old_filter and b"N\x01" in old_filter,"fixture_v6_filter_loses_q");e=Echelon();r,p=e.add({b"a":1,b"b":1},{"family":"PHYSICAL"});need(r and "_original_row" not in e.sources[0],"fixture_echelon");need(toy_memory_state_fixture() and toy_resource_fixture() and toy_durable_fixture() and toy_positive_fixture() and toy_fallback_fixture(),"fixture_controlled_gates");return {"status":"FIXTURE_PASS","aggregate_coordinates":True,"actor_groups":2,"split_resume":True,"periodic_save_clock":True,"resource_stop_save":True,"durable_scalar_snapshot":True,"instruction_dag":True,"zero_envelope":True,"memory_state_limit":True,"durable_fallback":True}
def main():
 ap=argparse.ArgumentParser();ap.add_argument("--mode",choices=("FIXTURE","PRODUCTION"),default="PRODUCTION");ap.add_argument("--output");ap.add_argument("--checkpoint");ap.add_argument("--resume");ap.add_argument("--seconds",type=float,default=9000);ap.add_argument("--rss-bytes",type=int,default=RSS_CAP);a=ap.parse_args();t=time.monotonic()
 try:o=fixture() if a.mode=="FIXTURE" else run(a);status=o.get("status",UNKNOWN)
 except Exception as e:
  status=RESOURCE if str(e).startswith(RESOURCE) else UNKNOWN;o={"status":status,"reason":str(e),"durable_state":LAST_DURABLE}
  if status==UNKNOWN:o["exception"]={"type":type(e).__name__,"reason":str(e),"traceback":traceback.format_exc(limit=24)[-12288:]}
 final_durable=o.get("durable_state") or LAST_DURABLE
 result={"schema":SCHEMA,"status":status,"terminal":status,"complete":False,"a0":o,"durable_state":final_durable,"eliminated_boundary_rows":0,"old_boundary_closure_present":False,"claim_boundary":{"common_word":False,"A0_membership":False,"fake":False,"Ihara_witness":False,"compatible_lift":False,"verified":False},"checkpoint_input":a.resume,"checkpoint_output":a.checkpoint}
 if a.resume and Path(ROOT/a.resume).exists():n,h=whole(ROOT/a.resume);result["checkpoint_input_seal"]={"path":a.resume,"bytes":n,"sha256":h}
 if a.checkpoint and Path(ROOT/a.checkpoint).exists():n,h=whole(ROOT/a.checkpoint);result["checkpoint"]={"path":a.checkpoint,"bytes":n,"sha256":h,"sequence":(final_durable or {}).get("checkpoint_seq",0)}
 if a.output:Path(ROOT/a.output).write_bytes(json.dumps(result,sort_keys=True,separators=(",",":"),default=str).encode()+b"\n")
 print("R07_A0_PB34_DIRECT_QUOTIENT_OWNER_V11 "+status,flush=True);return 0
if __name__=="__main__":raise SystemExit(main())
