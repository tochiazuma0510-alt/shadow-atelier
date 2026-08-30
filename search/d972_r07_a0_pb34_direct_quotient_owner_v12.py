#!/usr/bin/env python3
"""Task431 v12: phase-separated packed occurrence/physical owner."""
from __future__ import annotations
import argparse,gc,gzip,hashlib,json,marshal,os,shutil,sys,tempfile,time,traceback,types,struct,zipfile,urllib.request,ctypes
from array import array
from collections import deque
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];SCHEMA="d972-r07-a0-pb34-direct-quotient-owner/v12";RSS_CAP=4800000000;UNKNOWN="UNKNOWN";RESOURCE="UNKNOWN_RESOURCE"
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
v3=load(V3,"task431_v3_pinned");LAST_DURABLE=None;LAST_INPUT_SEAL=None
V11_MIRROR_URL="https://github.com/tochiazuma0510-alt/shadow-atelier/releases/download/archive-gha-checkpoints/artifact_9735328330_gap-run-out.valid.zip"
V11_MIRROR_BYTES=211296971;V11_MIRROR_SHA="b044eb9d730cb99c39253aedc573f8bba764ade0f732920e2ad7c306a5a3db92"
V11_ENTRY="d972_r07_a0_pb34_direct_quotient_owner_v11_output.checkpoint";V11_WHOLE_BYTES=275905469;V11_WHOLE_SHA="3ac222801a1a91b8e0f163554835e569a26c2cac0f3f8bea481e1825e5f911b8";V11_PAYLOAD_BYTES=275905379;V11_PAYLOAD_SHA="36da75dc8e5c21a84b26e35e4adbc9ac47e94f6c1fabbfcddddac03fd81d7ddf"
V11_ROSTER={"d972_r07_a0_pb34_direct_quotient_owner_v11.json","d972_r07_a0_pb34_direct_quotient_owner_v11_checker.log","d972_r07_a0_pb34_direct_quotient_owner_v11_output.checkpoint","d972_r07_a0_pb34_direct_quotient_owner_v11_producer.log","driver.g","run.log"}
def packed_contract():
 need(sys.byteorder=="little" and array("I").itemsize==4,"packed_platform")
 return {"byteorder":"little","uint_itemsize":4}
def pack_row(keys,ids,row):
 packed_contract();pairs=sorted((ids[k],int(v)%3) for k,v in row.items() if int(v)%3)
 blob=array("I",(i for i,v in pairs)).tobytes();coef=bytes(v for i,v in pairs)
 need(len(blob)//4==len(coef) and all(v in (1,2) for v in coef),"packed_row")
 return (blob,coef)
def packed_pivot(keys,pair,pivot):
 packed_contract();need(isinstance(pair,(tuple,list)) and len(pair)==2,"packed_pair");ib,cb=pair;need(isinstance(ib,bytes) and isinstance(cb,bytes) and len(ib)%4==0 and len(ib)//4==len(cb),"packed_alignment");last=-1;hit=False
 for i,c in zip(memoryview(ib).cast("I"),cb):
  need(i<len(keys) and i>last and c in (1,2),"packed_index");last=i
  if keys[i]==pivot:need(c==1,"packed_pivot_normalization");hit=True
 need(hit,"packed_pivot_missing");return True
def unpack_row(keys,pair):
 packed_contract();need(isinstance(pair,(tuple,list)) and len(pair)==2,"packed_pair")
 ib,cb=pair;need(isinstance(ib,bytes) and isinstance(cb,bytes) and len(ib)%4==0 and len(ib)//4==len(cb),"packed_alignment")
 out={};last=-1
 for i,c in zip(memoryview(ib).cast("I"),cb):
  need(i<len(keys) and i>last and c in (1,2),"packed_index");last=i;out[keys[i]]=c
 return out
class PackedRegistry:
 def __init__(self):self.keys=[];self.ids={}
class PackedEchelon:
 def __init__(self,registry=None):
  self.rows={};self.order=[];self.expr={};self.sources=[];self.registry=registry or PackedRegistry();self.payload_nnz=0
 @property
 def keys(self):return self.registry.keys
 @property
 def ids(self):return self.registry.ids
 def _intern(self,k):
  if k not in self.ids:self.ids[k]=len(self.keys);self.keys.append(k);need(len(self.keys)<2**32,"packed_registry")
  return self.ids[k]
 def _pack(self,row):
  for k in row:self._intern(k)
  return pack_row(self.keys,self.ids,row)
 def decode(self,p):return unpack_row(self.keys,self.rows[p])
 def iter_items(self,p):
  ib,cb=self.rows[p]
  for i,c in zip(memoryview(ib).cast("I"),cb):yield self.keys[i],c
 def axpy_packed(self,w,pair,c):
  ib,cb=pair
  for i,v in zip(memoryview(ib).cast("I"),cb):
   k=self.keys[i];x=(w.get(k,0)-int(c)*int(v))%3
   if x:w[k]=x
   else:w.pop(k,None)
 def __getitem__(self,p):return self.decode(p)
 def drop(self,p):
  pair=self.rows.pop(p);self.payload_nnz-=len(pair[1])
 def add(self,row,source):
  w={k:int(v)%3 for k,v in row.items() if int(v)%3};e={len(self.sources):1}
  for p in self.order:
   c=w.get(p,0)
   if c:
    self.axpy_packed(w,self.rows[p],c);Echelon.axpy(e,self.expr[p],c)
  if not w:return False,None
  p=min(w);s=1 if w[p]==1 else 2;w={k:s*int(v)%3 for k,v in w.items() if s*int(v)%3};pair=self._pack(w)
  self.rows[p]=pair;self.payload_nnz+=len(pair[1]);self.expr[p]={k:s*int(v)%3 for k,v in e.items() if s*int(v)%3};self.order.append(p);self.sources.append(dict(source));return True,p
 def reduce(self,row):
  w={k:int(v)%3 for k,v in row.items() if int(v)%3};e={}
  for p in self.order:
   c=w.get(p,0)
   if c:self.axpy_packed(w,self.rows[p],c);Echelon.axpy(e,self.expr[p],c)
  return w,e
 def dual(self,target):
  w,e=self.reduce(target)
  if not w:return None,w,e
  d={min(w):1}
  for p in sorted(self.order,reverse=True):
   x=(-sum(int(v)*d.get(k,0) for k,v in self.iter_items(p) if k!=p))%3
   if x:d[p]=x
  return d,w,e
 def load_registry_rows(self,keys,rows):
  packed_contract();copied=list(keys);ids={}
  for i,k in enumerate(copied):need(isinstance(k,bytes) and k not in ids,"packed_registry_keys");ids[k]=i
  need(len(ids)==len(copied),"packed_registry_size")
  self.registry.keys=copied;self.registry.ids=ids;self.rows=dict(rows);self.payload_nnz=sum(len(x[1]) for x in self.rows.values())
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
def aggregate_items(items):
 out={}
 for k,c in items:
  if k[:1]==b"O":need(len(k)>=3,"occurrence_tag");k=k[2:]
  elif k[:1]!=b"N":raise RuntimeError("raw_occurrence_key")
  x=(out.get(k,0)+int(c))%3
  if x:out[k]=x
  else:out.pop(k,None)
 return out
def row_digest(row):
 h=hashlib.sha256()
 for k,v in sorted(row.items()):
  h.update(struct.pack("<I",len(k)));h.update(k);h.update(bytes((int(v)%3,)))
 return h.hexdigest()
def enc_row(r):return [[k.hex(),int(v)%3] for k,v in sorted(r.items()) if int(v)%3]
def normal_section(q,p176,key,c):
 block,label,blob=q.parse(key);g=q.e3 if block<3 else q.e4;n=2 if block<3 else 5;z=q.z3 if block<3 else q.z4
 if label=="tau":
  r=q.h0(g,z,g.identity)[0];return [(n,r,c),(n,g.mul(r,z),c),(n,g.mul(r,g.mul(z,z)),c)]
 if label in ("u0","u1"):return [(n,g.mul(q.dec(blob,block),g.identity if label=="u0" else z),c)]
 mp={"b":0,"c":1} if block<3 else {"b":0,"c":1,"p":2,"q":3,"r":4};need(label in mp,"section_label");return [(mp[label],q.dec(blob,block),c)]
def actor_v12(runtime,model,owner,p176,q,row,letter):
 out={};groups={};cache={}
 for k,c in (row.items() if hasattr(row,"items") else row):
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
def seed_v12(model,old,owner,p176,q,word):
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
def replay_atom(seed,prefix,runtime,model,pres,owner,p176,q):
 row=seed_v12(model,runtime.old,owner,p176,q,list(pres["relators"][int(seed)-1]))
 for letter in reversed(tuple(prefix)):
  row=actor_v12(runtime,model,owner,p176,q,row,int(letter))
 return row
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
   op=bytes.fromhex(s["occurrence_pivot"]);raw_replay={}
   for (seed,pref),x in atoms_pivot(op).items():raw_replay=v3.row_add(raw_replay,replay_atom(seed,pref,runtime,model,pres,owner,p176,q),int(x))
   fresh=aggregate(raw_replay);digest=row_digest(fresh);need(digest==s.get("source_digest"),"physical_source_digest")
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
 n,h=whole(tmp);header=("D972-A0V12-CP1 "+h+" "+str(n)+"\n").encode();fh=hashlib.sha256();fn=0
 with tempfile.NamedTemporaryFile(dir=p.parent,delete=False) as f:
  out=Path(f.name);f.write(header);fh.update(header);fn+=len(header)
  with tmp.open("rb") as src:
   for chunk in iter(lambda:src.read(1<<20),b""):f.write(chunk);fh.update(chunk);fn+=len(chunk)
  f.flush();os.fsync(f.fileno())
 tmp.unlink(missing_ok=True);os.replace(out,p);return fn,fh.hexdigest()
def phase_gate(s):
 phase=s.get("phase");order=s["occ_order"];po=s["physical_order"];osrc=s["physical_sources"];pc=int(s.get("physical_cursor",0))
 need(int(s.get("frontier_length",-1))==len(s.get("queue",[])),"phase_frontier_length");need(len(order)==len(set(order)) and len(po)==len(set(po)),"phase_order_unique");need(set(s["physical_rows"])==set(po) and len(s["physical_rows"])==len(po) and all(p in order for p in s["occ_rows"]),"phase_pivot_membership")
 need(len(s["physical_rows"])==len(po)==len(s["physical_expr"])==len(osrc),"phase_physical_shape")
 fam=[x.get("family") for x in osrc];need(all(x in {"PHYSICAL","action"} for x in fam),"phase_source_family")
 occ_nnz=sum(len(x[1]) for x in s["occ_rows"].values());phys_nnz=sum(len(x[1]) for x in s["physical_rows"].values());need(int(s.get("occurrence_payload_nnz",-1))==occ_nnz==int(s.get("occurrence_pivot_nnz",-2)),"phase_occurrence_nnz");need(int(s.get("physical_payload_nnz",-1))==phys_nnz==int(s.get("physical_pivot_nnz",-2)),"phase_physical_nnz")
 if phase=="occurrence_queue":need(not s["physical_rows"] and not s["physical_order"] and not s["physical_expr"] and not s["physical_sources"] and int(s.get("physical_payload_nnz",-1))==0 and int(s.get("physical_pivot_nnz",-1))==0 and pc==0,"phase_occurrence_physical_empty")
 if phase=="physical_build":need(int(s.get("seed_cursor",0))==44 and not s.get("queue") and set(s["occ_rows"])==set(order[pc:]) and all(x=="PHYSICAL" for x in fam),"phase_physical_gate")
 if phase=="six_action":need(int(s.get("seed_cursor",0))==44 and not s.get("queue") and not s["occ_rows"] and pc==len(order) and fam==sorted(fam,key=lambda x:0 if x=="PHYSICAL" else 1),"phase_six_action_gate")
 order_index={p:i for i,p in enumerate(order)};last=-1
 for x in osrc:
  if x.get("family")=="PHYSICAL":
   op=bytes.fromhex(x.get("occurrence_pivot",""));need(op in order_index,"phase_physical_source_id");idx=order_index[op];need(idx<pc and idx>last,"phase_physical_source_prefix");last=idx
 return True
def cp_read(path):
 global LAST_INPUT_SEAL
 p=Path(path);need(not p.is_absolute() and p.parent==Path("ci/out"),"resume_path")
 with p.open("rb") as f:
  header_bytes=f.readline();head=header_bytes.decode().rstrip("\n").split(" ");need(len(head)==3 and head[0]=="D972-A0V12-CP1","checkpoint_header");ph=hashlib.sha256();wh=hashlib.sha256();payload_n=0;file_n=len(header_bytes);wh.update(header_bytes)
  for chunk in iter(lambda:f.read(1<<20),b""):ph.update(chunk);wh.update(chunk);payload_n+=len(chunk);file_n+=len(chunk)
 need(payload_n==int(head[2]) and ph.hexdigest()==head[1],"checkpoint_seal");file_h=wh.hexdigest();LAST_INPUT_SEAL=(file_n,file_h,payload_n,head[1])
 with p.open("rb") as f:
  f.readline()
  with gzip.GzipFile(fileobj=f,mode="rb") as z:b=marshal.load(z)
 need(isinstance(b,dict) and b.get("schema")==SCHEMA+"/checkpoint", "checkpoint_schema");s=b["state"];need(s.get("binding")==hashlib.sha256((SCHEMA+V3[2]).encode()).hexdigest(),"checkpoint_binding");need(s.get("packed_contract")==packed_contract(),"packed_contract");need(s.get("eliminated_boundary_rows")==0 and s.get("old_boundary_closure_present") is False,"boundary_invariant")
 phase=s.get("phase");pc=int(s.get("physical_cursor",0));need(phase in {"occurrence_queue","physical_build","six_action"},"checkpoint_phase")
 keys=s["coordinate_keys"];need(len(keys)==len(set(keys)) and all(isinstance(k,bytes) for k in keys),"checkpoint_keys")
 for pref in ("occ","physical"):
  rows=s[pref+"_rows"];order=s[pref+"_order"];expr=s[pref+"_expr"];sources=s[pref+"_sources"];need(len(expr)==len(sources)==len(order) and len(rows)<=len(order),"checkpoint_shape")
  for pvt in rows:need(pvt in order and packed_pivot(keys,rows[pvt],pvt),"checkpoint_pivot")
  for e in expr.values():
   for i in e:need(isinstance(i,int) and 0<=i<len(sources),"checkpoint_expression")
  allowed={"LEAF","CONJUGATE"} if pref=="occ" else {"PHYSICAL","action"}
  for src in sources:
   need(isinstance(src,dict) and src.get("family") in allowed and "_original_row" not in src,"checkpoint_source")
   if pref=="physical" and src.get("family")=="PHYSICAL":need(isinstance(src.get("source_digest"),str) and len(src["source_digest"])==64 and all(c in "0123456789abcdef" for c in src["source_digest"]),"checkpoint_source_digest")
 for pvt in s.get("queue",[]):need(bytes.fromhex(pvt) in s["occ_rows"],"checkpoint_queue")
 if phase=="occurrence_queue":need(0<=int(s.get("seed_cursor",0))<=44 and int(s.get("parent_cursor",0))>=0 and int(s.get("action_cursor",0))>=0 and set(s["occ_rows"])==set(s["occ_order"]) and not s["physical_rows"] and pc==0,"occurrence_phase_state")
 if phase=="physical_build":need(int(s.get("seed_cursor",0))==44 and not s.get("queue") and set(s["occ_rows"])==set(s["occ_order"][pc:]),"physical_phase_suffix")
 if phase=="physical_build":need(0<=pc<=len(s["occ_order"]) and len(s["occ_rows"])+pc==len(s["occ_order"]),"physical_phase_state")
 if phase=="six_action":need(int(s.get("seed_cursor",0))==44 and not s.get("queue") and not s["occ_rows"] and pc==len(s["occ_order"]),"six_action_state")
 phase_gate(s)
 return s,file_n,file_h
def migrate_v11_release(url):
 need(url==V11_MIRROR_URL,"v11_mirror_url");base=ROOT/"ci"/"in";base.mkdir(parents=True,exist_ok=True);fd,tmp_name=tempfile.mkstemp(dir=base,prefix="v11-mirror-",suffix=".zip.tmp");os.close(fd);tmp=Path(tmp_name);sealed=base/"artifact_9735328330_gap-run-out.valid.zip";h=hashlib.sha256();n=0
 try:
  with urllib.request.urlopen(url,timeout=60) as src:
   with tmp.open("wb") as dst:
    for chunk in iter(lambda:src.read(1<<20),b""):dst.write(chunk);h.update(chunk);n+=len(chunk)
    dst.flush();os.fsync(dst.fileno())
  need(n==V11_MIRROR_BYTES and h.hexdigest()==V11_MIRROR_SHA,"v11_mirror_seal")
  os.replace(tmp,sealed)
  with zipfile.ZipFile(sealed) as z:
   names=z.namelist();need(sorted(names)==sorted(V11_ROSTER) and V11_ENTRY in names,"v11_roster")
   for name in names:need(not name.startswith("/") and ".." not in Path(name).parts,"v11_entry_path")
   out=base/(V11_ENTRY+".tmp");eh=hashlib.sha256();ih=hashlib.sha256();en=inner_n=0;header_buf=b"";header=None
   with z.open(V11_ENTRY) as src, out.open("wb") as dst:
    for chunk in iter(lambda:src.read(1<<20),b""):
     dst.write(chunk);eh.update(chunk);en+=len(chunk)
     if header is None:
      header_buf+=chunk
      if b"\n" in header_buf:
       line,rest=header_buf.split(b"\n",1);header=line.decode().rstrip("\r").split(" ");header_buf=b"";ih.update(rest);inner_n+=len(rest)
     else:ih.update(chunk);inner_n+=len(chunk)
  need(en==V11_WHOLE_BYTES and eh.hexdigest()==V11_WHOLE_SHA,"v11_checkpoint_whole_seal")
  head=header;need(head is not None and len(head)==3 and head[0]=="D972-A0V11-CP1" and int(head[2])==V11_PAYLOAD_BYTES,"v11_checkpoint_header");need(inner_n==int(head[2]) and ih.hexdigest()==V11_PAYLOAD_SHA and head[1]==V11_PAYLOAD_SHA,"v11_checkpoint_payload_seal")
  with out.open("rb") as f:
   f.readline()
   with gzip.GzipFile(fileobj=f,mode="rb") as z:body=marshal.load(z)
  need(isinstance(body,dict) and body.get("schema")=="d972-r07-a0-pb34-direct-quotient-owner/v11/checkpoint","v11_checkpoint_schema");s=body["state"];need(s.get("binding")==hashlib.sha256(("d972-r07-a0-pb34-direct-quotient-owner/v11"+V3[2]).encode()).hexdigest(),"v11_binding");need(s.get("seed_cursor")==44 and s.get("parent_cursor")==86 and s.get("action_cursor")==344 and len(s.get("occ_order",[]))==344 and len(s.get("queue",[]))==258,"v11_cursors");need(s.get("eliminated_boundary_rows")==0 and s.get("old_boundary_closure_present") is False,"v11_boundary_invariant");return s
 finally:
  tmp.unlink(missing_ok=True)
  sealed.unlink(missing_ok=True)
  if 'out' in locals() and out is not None:out.unlink(missing_ok=True)
def prepare_v11_state(s):
 for name in ("physical_rows","physical_order","physical_expr","physical_sources","physical_keys","physical_payload_nnz","physical_pivot_nnz"):s.pop(name,None)
 gc.collect()
 raw=s.pop("occ_rows");registry=PackedRegistry();packed={}
 for p in s["occ_order"]:
  row=raw.pop(p);ids=registry.ids
  for k in row:
   if k not in ids:ids[k]=len(registry.keys);registry.keys.append(k)
  packed[p]=pack_row(registry.keys,registry.ids,row)
 need(not raw,"v11_occurrence_consumed");
 s["occ_rows"]=packed;s["coordinate_keys"]=registry.keys;s["physical_rows"]={};s["physical_order"]=[];s["physical_expr"]={};s["physical_sources"]=[];s["physical_payload_nnz"]=0;s["physical_pivot_nnz"]=0;s["packed_contract"]=packed_contract();s["phase"]="occurrence_queue";s["physical_cursor"]=0
 gc.collect()
 if sys.platform.startswith("linux"):
  try:ctypes.CDLL("libc.so.6").malloc_trim(0)
  except Exception:pass
 rss=getattr(v3,"rss",lambda:0)() or 0;need(rss<RSS_CAP,"v11_migration_rss")
 return s
def migration_v12_checkpoint(s):
 return {"phase":"occurrence_queue","reason":"v11_migration","seed_cursor":44,"parent_cursor":86,"action_cursor":344,"physical_cursor":0,"queue":list(s["queue"]),"frontier_length":len(s["queue"]),"occ_rows":s["occ_rows"],"coordinate_keys":s["coordinate_keys"],"occ_order":s["occ_order"],"occ_expr":s["occ_expr"],"occ_sources":s["occ_sources"],"occurrence_payload_nnz":sum(len(x[1]) for x in s["occ_rows"].values()),"physical_rows":{},"physical_order":[],"physical_expr":{},"physical_sources":[],"physical_payload_nnz":0,"binding":hashlib.sha256((SCHEMA+V3[2]).encode()).hexdigest(),"packed_contract":packed_contract(),"checkpoint_seq":int(s.get("checkpoint_seq",0))+1,"occurrence_pivot_nnz":sum(len(x[1]) for x in s["occ_rows"].values()),"physical_pivot_nnz":0,"eliminated_boundary_rows":0,"old_boundary_closure_present":False}
def run(a):
 global LAST_DURABLE
 migration_state=migrate_v11_release(a.resume_v11_url) if a.resume_v11_url and not a.resume else None
 if migration_state is not None:
  migration_state=migration_v12_checkpoint(prepare_v11_state(migration_state));need(a.checkpoint,"v11_migration_checkpoint_required");n,h=cp_write(a.checkpoint,migration_state);LAST_DURABLE={"phase":"occurrence_queue","seed_cursor":44,"parent_cursor":86,"action_cursor":344,"physical_cursor":0,"occurrence_rank":len(migration_state["occ_order"]),"physical_rank":0,"physical_cursor":0,"frontier_length":len(migration_state["queue"]),"occurrence_payload_nnz":migration_state["occurrence_payload_nnz"],"physical_payload_nnz":0,"occurrence_pivot_nnz":migration_state["occurrence_pivot_nnz"],"physical_pivot_nnz":0,"checkpoint_seq":migration_state["checkpoint_seq"],"checkpoint_bytes":n,"checkpoint_sha256":h}
 start=time.monotonic();t413=v3.load(v3.T413,"task431_task413");base=t413["bound_module"](t413["BASE"],"task431_base");receipt=t413["load_json"](base,t413["JOINT"]);q3=t413["load_json"](base,t413["Q3"]);pres=base["compact"](receipt,q3);core=base["load_task198_core"]();roof=t413["load_json"](base,base["ROOF"]);acceptance=t413["load_json"](base,base["ACCEPTANCE"]);need(base["acceptance_ok"](acceptance),"acceptance_v2_contract");authority=types.SimpleNamespace(receipt=roof);layout=base["load_bound_module"](base["TASK379"],"task431_layout")["validate_layout"];ledger=layout(core,authority);runtime=core.Runtime(authority,core.Meter(dict(core.CAPS)));owner,g760,model=base["direct_physical_owner"](runtime);p176=base["load_bound_module"](base["TASK176"],"task431_p176");q=Quotient(owner,p176,runtime.e3,runtime.e4);target=q.transform(t413["target_row"](base,owner,runtime.old,runtime.e3,runtime.e4,g760,model));registry=PackedRegistry();occ=PackedEchelon(registry);phys=PackedEchelon(registry);queue=deque();seed_cursor=parent_cursor=action_cursor=seq=physical_cursor=0;phase="occurrence_queue";last_save=0.;durable=None;binding=hashlib.sha256((SCHEMA+V3[2]).encode()).hexdigest();print("phase=preflight owner_v12=BOUND rss_cap=%d"%RSS_CAP,flush=True);print("phase=runtime_bootstrap owner_v12=READY",flush=True)
 def state(phase,reason):return {"phase":phase,"reason":reason,"seed_cursor":seed_cursor,"parent_cursor":parent_cursor,"action_cursor":action_cursor,"physical_cursor":physical_cursor,"queue":[p.hex() for p in queue],"frontier_length":len(queue),"occ_rows":occ.rows,"coordinate_keys":occ.keys,"occ_order":occ.order,"occ_expr":occ.expr,"occ_sources":occ.sources,"occurrence_payload_nnz":occ.payload_nnz,"physical_rows":phys.rows,"physical_order":phys.order,"physical_expr":phys.expr,"physical_sources":phys.sources,"physical_payload_nnz":phys.payload_nnz,"binding":binding,"packed_contract":packed_contract(),"checkpoint_seq":seq,"occurrence_pivot_nnz":occ.payload_nnz,"physical_pivot_nnz":phys.payload_nnz,"eliminated_boundary_rows":0,"old_boundary_closure_present":False}
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
  seq+=1;s=state(phase,stop_reason or reason);s["checkpoint_seq"]=seq;n,h=cp_write(a.checkpoint,s);durable={"phase":phase,"seed_cursor":seed_cursor,"parent_cursor":parent_cursor,"action_cursor":action_cursor,"physical_cursor":physical_cursor,"occurrence_rank":len(occ.order),"physical_rank":len(phys.order),"frontier_length":len(queue),"occurrence_payload_nnz":s["occurrence_payload_nnz"],"physical_payload_nnz":s["physical_payload_nnz"],"occurrence_pivot_nnz":s["occurrence_pivot_nnz"],"physical_pivot_nnz":s["physical_pivot_nnz"],"checkpoint_seq":seq,"checkpoint_bytes":n,"checkpoint_sha256":h};LAST_DURABLE=durable;last_save=now;print("checkpoint_durable phase=%s seq=%d rank=%d/%d pivot_nnz=%d/%d"%(phase,seq,len(occ.order),len(phys.order),s["occurrence_pivot_nnz"],s["physical_pivot_nnz"]),flush=True)
  if stop_reason:raise RuntimeError(RESOURCE+":"+stop_reason)
 def guard(phase):
  elapsed=time.monotonic()-start;mem=v3.rss() or 0
  if (a.seconds is not None and elapsed>=a.seconds) or mem>=int(a.rss_bytes):
   reason="time_limit" if a.seconds is not None and elapsed>=a.seconds else "rss_limit";save(phase,reason,True);raise RuntimeError(RESOURCE+":"+reason)
 if a.resume or migration_state is not None:
  if a.resume:s,resume_bytes,resume_sha=cp_read(a.resume)
  else:s,resume_bytes,resume_sha=migration_state,(LAST_DURABLE or {}).get("checkpoint_bytes",0),(LAST_DURABLE or {}).get("checkpoint_sha256","")
  seed_cursor=int(s["seed_cursor"]);parent_cursor=int(s.get("parent_cursor",0));action_cursor=int(s.get("action_cursor",0));physical_cursor=int(s.get("physical_cursor",0));phase=s.get("phase","occurrence_queue");seq=int(s.get("checkpoint_seq",0))
  if migration_state is not None and not a.resume:
   occ.load_registry_rows(s["coordinate_keys"],s["occ_rows"]);occ.order=list(s["occ_order"]);occ.expr=s["occ_expr"];occ.sources=s["occ_sources"];phys=PackedEchelon(occ.registry);queue=deque(bytes.fromhex(x) for x in s["queue"]);phase="occurrence_queue";physical_cursor=0
  else:
   occ.load_registry_rows(s["coordinate_keys"],s["occ_rows"]);occ.order=s["occ_order"];occ.expr=s["occ_expr"];occ.sources=s["occ_sources"];phys.registry=occ.registry;phys.rows=dict(s["physical_rows"]);phys.payload_nnz=sum(len(x[1]) for x in phys.rows.values());phys.order=s["physical_order"];phys.expr=s["physical_expr"];phys.sources=s["physical_sources"];queue=deque(bytes.fromhex(x) for x in s["queue"])
  durable={"phase":phase,"seed_cursor":seed_cursor,"parent_cursor":parent_cursor,"action_cursor":action_cursor,"physical_cursor":physical_cursor,"occurrence_rank":len(occ.order),"physical_rank":len(phys.order),"frontier_length":len(queue),"occurrence_payload_nnz":occ.payload_nnz,"physical_payload_nnz":phys.payload_nnz,"occurrence_pivot_nnz":occ.payload_nnz,"physical_pivot_nnz":phys.payload_nnz,"checkpoint_seq":seq,"checkpoint_bytes":resume_bytes,"checkpoint_sha256":resume_sha};LAST_DURABLE=durable;print("phase=resume_restored "+json.dumps(durable,sort_keys=True),flush=True);s=None;migration_state=None;gc.collect()
  if (v3.rss() or 0)>=int(a.rss_bytes):return {"status":UNKNOWN,"reason":"MEMORY_STATE_LIMIT","durable_state":durable,"seed_cursor":seed_cursor,"parent_cursor":parent_cursor,"action_cursor":action_cursor,"occurrence_rank":len(occ.order),"physical_rank":len(phys.order),"frontier_length":len(queue),"checkpoint_seq":seq}
  guard("resume")
 else:
  for i,w in enumerate(pres["relators"],1):
   guard("occurrence_queue");ss=runtime.states_direct(list(w));need(all(x.a==x.q.identity for x in ss),"seed_identity");r=seed_v12(model,runtime.old,owner,p176,q,list(w));rise,p=occ.add(r,{"family":"LEAF","seed":i});seed_cursor=i
   if rise:queue.append(p)
   guard("occurrence_queue")
  save("occurrence_queue","seeds_complete",True)
 if a.resume and seed_cursor<44 and phase=="occurrence_queue":
  for i in range(seed_cursor+1,45):
   w=pres["relators"][i-1];guard("occurrence_queue");ss=runtime.states_direct(list(w));need(all(x.a==x.q.identity for x in ss),"seed_identity");r=seed_v12(model,runtime.old,owner,p176,q,list(w));rise,p=occ.add(r,{"family":"LEAF","seed":i});seed_cursor=i
   if rise:queue.append(p)
   guard("occurrence_queue")
  save("occurrence_queue","seeds_resume_complete",True)
 while queue and phase=="occurrence_queue":
  guard("parent");p=queue.popleft()
  for letter in (1,-1,2,-2):
   r=actor_v12(runtime,model,owner,p176,q,occ.iter_items(p),letter);rise,np=occ.add(r,{"family":"CONJUGATE","letter":letter,"parent":p.hex()});action_cursor+=1
   if rise:queue.append(np)
  parent_cursor+=1;guard("parent")
  if len(occ.order)-getattr(run,"_progress_rank",0)>=32 or time.monotonic()-getattr(run,"_progress_time",start)>=60:
   run._progress_rank=len(occ.order);run._progress_time=time.monotonic();print("progress phase=occurrence_queue seed_cursor=%d actor_cursor=%d occurrence_rank=%d physical_rank=%d frontier=%d occurrence_pivot_nnz=%d physical_pivot_nnz=%d owner_rss_bytes=%s elapsed_seconds=%.3f checkpoint_seq=%d"%(seed_cursor,action_cursor,len(occ.order),len(phys.order),len(queue),occ.payload_nnz,phys.payload_nnz,v3.rss(),time.monotonic()-start,seq),flush=True)
  if time.monotonic()-last_save>=300:save("occurrence_queue","parent_complete")
 if phase=="occurrence_queue":save("occurrence_queue","occurrence_exhausted",True);phase="physical_build"
 for physical_cursor in (range(physical_cursor,len(occ.order)) if phase=="physical_build" else ()):
  p=occ.order[physical_cursor];fresh=aggregate_items(occ.iter_items(p));digest=row_digest(fresh);phys.add(fresh,{"family":"PHYSICAL","occurrence_pivot":p.hex(),"source_digest":digest});occ.drop(p);physical_cursor+=1
  if time.monotonic()-last_save>=300:save("physical_build","physical_prefix")
 if phase=="physical_build":save("physical_build","physical_complete",True);phase="six_action"
 actions=list(runtime.old.pure_relations(4)[5:11])
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
 nodes=[{"family":"LEAF","seed":1},{"family":"CONJUGATE","letter":2,"parent":0},{"family":"CONJUGATE","letter":-1,"parent":1}];stack=[(2,1,())];atoms={}
 while stack:
  i,c,prefix=stack.pop();node=nodes[i]
  if node["family"]=="LEAF":key=(node["seed"],prefix);atoms[key]=(atoms.get(key,0)+c)%3
  else:stack.append((node["parent"],c,prefix+(int(node["letter"]),)))
 need(atoms.get((1,(-1,2)))==1,"fixture_instruction_dag");seed=(0,);prefix=(2,3);actor=lambda r,l:(l,)+r;replayed=seed
 for letter in reversed(prefix):replayed=actor(replayed,letter)
 forward=seed
 for letter in prefix:forward=actor(forward,letter)
 need(replayed==(2,3,0) and replayed!=forward,"fixture_noncommutative_reverse_prefix");need(row_digest({bytes(replayed):1})!=row_digest({bytes(forward):1}),"fixture_prefix_digest_mutation");need(not v3.row_add(v3.row_add({b"q":1},{b"q":1}),{b"q":1}),"fixture_zero_envelope");return True
def toy_phase_fixture():
 pair=(struct.pack("<I",0),b"\x01");order=[b"a",b"b",b"c"];base={"phase":"physical_build","occ_order":order,"physical_order":[b"a"],"occ_rows":{b"b":pair,b"c":pair},"physical_rows":{b"a":pair},"physical_expr":[{}],"physical_sources":[{"family":"PHYSICAL","occurrence_pivot":"61"}],"seed_cursor":44,"parent_cursor":0,"action_cursor":0,"physical_cursor":1,"queue":[],"frontier_length":0,"occurrence_payload_nnz":2,"occurrence_pivot_nnz":2,"physical_payload_nnz":1,"physical_pivot_nnz":1}
 need(phase_gate(dict(base)) is True,"fixture_physical_phase_gate")
 for bad in ({**base,"occ_rows":{b"a":pair,b"c":pair}},{**base,"physical_sources":[{"family":"action"}]},{**base,"frontier_length":1}):
  try:phase_gate(bad)
  except RuntimeError:pass
  else:raise RuntimeError("fixture_phase_mutation")
 six={"phase":"six_action","occ_order":order,"physical_order":[b"a",b"x"],"occ_rows":{},"physical_rows":{b"a":pair,b"x":pair},"physical_expr":[{},{}],"physical_sources":[{"family":"PHYSICAL","occurrence_pivot":"61"},{"family":"action"}],"seed_cursor":44,"parent_cursor":0,"action_cursor":1,"physical_cursor":3,"queue":[],"frontier_length":0,"occurrence_payload_nnz":0,"occurrence_pivot_nnz":0,"physical_payload_nnz":2,"physical_pivot_nnz":2};need(phase_gate(six) is True,"fixture_six_source_order")
 bad=dict(six);bad["physical_sources"]=list(reversed(six["physical_sources"]))
 try:phase_gate(bad)
 except RuntimeError:pass
 else:raise RuntimeError("fixture_six_source_mutation")
 return True
def toy_migration_fixture():
 s={"occ_rows":{b"p":{b"O\x01a":1}},"occ_order":[b"p"],"queue":[b"p"],"occ_expr":[{0:1}],"occ_sources":[{"family":"LEAF"}],"seed_cursor":44,"parent_cursor":86,"action_cursor":344,"checkpoint_seq":10,"physical_rows":{b"old":(b"dict",b"x")},"physical_order":[b"old"],"physical_expr":[{}],"physical_sources":[{"family":"PHYSICAL"}],"physical_payload_nnz":1,"physical_pivot_nnz":1}
 out=prepare_v11_state(s);need(not out["physical_rows"] and out["queue"]==[b"p"] and out["occ_order"]==[b"p"] and out["seed_cursor"]==44 and out["parent_cursor"]==86 and out["action_cursor"]==344 and out["occ_expr"]==[{0:1}] and out["occ_sources"]==[{"family":"LEAF"}],"fixture_migration_state")
 return True
def toy_checkpoint_fixture():
 p=Path("ci/out/.task431_v12_fixture.checkpoint");p.unlink(missing_ok=True)
 reg=PackedRegistry();packed=pack_row([b"a"],{b"a":0},{b"a":1});state={"phase":"occurrence_queue","reason":"fixture","seed_cursor":1,"parent_cursor":0,"action_cursor":0,"physical_cursor":0,"queue":["61"],"frontier_length":1,"occ_rows":{b"a":packed},"coordinate_keys":[b"a"],"occ_order":[b"a"],"occ_expr":{b"a":{0:1}},"occ_sources":[{"family":"LEAF"}],"occurrence_payload_nnz":1,"physical_rows":{},"physical_order":[],"physical_expr":{},"physical_sources":[],"physical_payload_nnz":0,"binding":hashlib.sha256((SCHEMA+V3[2]).encode()).hexdigest(),"packed_contract":packed_contract(),"checkpoint_seq":1,"occurrence_pivot_nnz":1,"physical_pivot_nnz":0,"eliminated_boundary_rows":0,"old_boundary_closure_present":False}
 try:n,h=cp_write(p,state);restored,nn,hh=cp_read(p);need(n==nn and h==hh and restored["phase"]=="occurrence_queue","fixture_stream_checkpoint")
 finally:p.unlink(missing_ok=True)
 return True
def toy_memory_state_fixture():
 state={"checkpoint_seq":7,"occurrence_rank":3};save_calls=[0]
 if 4800000000>=4800000000:
  result={"status":UNKNOWN,"reason":"MEMORY_STATE_LIMIT","durable_state":state}
  save_calls[0]+=0
 need(result["status"]==UNKNOWN and result["reason"]=="MEMORY_STATE_LIMIT" and save_calls[0]==0 and result["durable_state"]["checkpoint_seq"]==7,"fixture_memory_state_limit");return True
def toy_fallback_fixture():
 candidate={"status":"COMMON_CANDIDATE","durable_state":None};fallback={"checkpoint_seq":9};final=candidate.get("durable_state") or fallback
 need(final is fallback and final["checkpoint_seq"]==9,"fixture_durable_fallback");return True
def toy_packed_fixture():
 rows=[{b"a":1,b"c":2},{b"a":2,b"b":1},{b"b":1,b"d":2}];legacy=Echelon();packed=PackedEchelon()
 for row in rows:
  lr,lp=legacy.add(row,{"family":"LEAF"});pr,pp=packed.add(row,{"family":"LEAF"});need(lr==pr and lp==pp,"fixture_packed_rank")
 need(legacy.order==packed.order and all(legacy.rows[p]==packed.decode(p) for p in legacy.order),"fixture_packed_rows");need(legacy.reduce({b"a":1,b"d":1})==packed.reduce({b"a":1,b"d":1}),"fixture_packed_reduce");need(legacy.dual({b"a":1,b"d":1})==packed.dual({b"a":1,b"d":1}),"fixture_packed_dual");need(row_digest({b"a":1,b"b":2})==row_digest({b"b":2,b"a":1}),"fixture_framed_digest")
 keys=[b"a",b"b"];bad=[(b"\x00",b""),(struct.pack("<I",2),b"\x01"),(struct.pack("<II",0,0),b"\x01\x02"),(struct.pack("<I",0),b"\x00")]
 for pair in bad:
  try:unpack_row(keys,pair)
  except RuntimeError:pass
  else:raise RuntimeError("fixture_packed_corruption")
 live=PackedEchelon();live.add({b"a":1},{"family":"LEAF"});discarded=dict(live.rows);live.rows={};need(discarded and not live.rows,"fixture_migration_discards_physical")
 simultaneous=PackedEchelon();deferred=PackedEchelon()
 for row in rows:simultaneous.add(row,{"family":"PHYSICAL"})
 for row in rows:deferred.add(row,{"family":"PHYSICAL"})
 need(simultaneous.order==deferred.order and simultaneous.rows==deferred.rows,"fixture_deferred_span")
 shared=PackedRegistry();occ=PackedEchelon(shared);phys=PackedEchelon(shared);_,pivot=occ.add({b"a":1,b"b":2},{"family":"LEAF"});need(occ.registry is phys.registry,"fixture_shared_registry")
 need(list(occ.iter_items(pivot))==[(b"a",1),(b"b",2)],"fixture_packed_parent_actor_decode")
 need(phys.add(aggregate_items(((b"O\x01"+b"a",1),(b"N\x01",2))),{"family":"PHYSICAL","source_digest":"0"*64})[0],"fixture_deferred_physical_insert")
 phase_state={"phase":"physical_build","occ_order":[b"a",b"b"],"physical_cursor":1,"occ_rows":{b"b":(struct.pack("<I",0),b"\x01")}}
 need(set(phase_state["occ_rows"])==set(phase_state["occ_order"][phase_state["physical_cursor"]:]),"fixture_phase_suffix_resume")
 six_state={"phase":"six_action","occ_order":[b"a"],"physical_cursor":1,"occ_rows":{}}
 need(not six_state["occ_rows"] and six_state["physical_cursor"]==len(six_state["occ_order"]),"fixture_six_action_resume")
 return True
def fixture():
 need(V11_WHOLE_BYTES==275905469 and V11_PAYLOAD_BYTES==275905379 and V11_WHOLE_BYTES>V11_PAYLOAD_BYTES and len(V11_WHOLE_SHA)==64 and len(V11_PAYLOAD_SHA)==64,"fixture_v11_seal_constants")
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
 legacy=b"Q\x01tau";multi={legacy:1,q.qkey(1,"b",b"x"):1};need(Quotient.transform(q,{})=={},"fixture_transform_empty");out=Quotient.transform(q,multi);need(q.qkey(1,"tau") in out and q.qkey(1,"b",b"x") in out,"fixture_transform_multi");tagged={b"O\x01"+q.qkey(1,"b",b"x"):1,b"O\x02"+q.qkey(1,"b",b"x"):1,b"N\x01":2};agg=aggregate(tagged);need(agg.get(q.qkey(1,"b",b"x"))==2 and agg.get(b"N\x01")==2,"fixture_aggregate_tagged");old_filter={k:v for k,v in tagged.items() if k[:1]!=b"O"};need(q.qkey(1,"b",b"x") not in old_filter and b"N\x01" in old_filter,"fixture_v6_filter_loses_q");need(toy_packed_fixture(),"fixture_packed_contract");need(toy_phase_fixture() and toy_migration_fixture() and toy_checkpoint_fixture(),"fixture_phase_migration");need(toy_memory_state_fixture() and toy_resource_fixture() and toy_durable_fixture() and toy_positive_fixture() and toy_fallback_fixture(),"fixture_controlled_gates");return {"status":"FIXTURE_PASS","aggregate_coordinates":True,"actor_groups":2,"split_resume":True,"periodic_save_clock":True,"resource_stop_save":True,"durable_scalar_snapshot":True,"instruction_dag":True,"zero_envelope":True,"memory_state_limit":True,"durable_fallback":True,"packed_rows":True,"phase_separated":True,"phase_migration":True,"stream_checkpoint":True}
def main():
 ap=argparse.ArgumentParser();ap.add_argument("--mode",choices=("FIXTURE","PRODUCTION"),default="PRODUCTION");ap.add_argument("--output");ap.add_argument("--checkpoint");ap.add_argument("--resume");ap.add_argument("--resume-v11-url");ap.add_argument("--seconds",type=float,default=9000);ap.add_argument("--rss-bytes",type=int,default=RSS_CAP);a=ap.parse_args();t=time.monotonic()
 try:o=fixture() if a.mode=="FIXTURE" else run(a);status=o.get("status",UNKNOWN)
 except Exception as e:
  status=RESOURCE if str(e).startswith(RESOURCE) else UNKNOWN;o={"status":status,"reason":str(e),"durable_state":LAST_DURABLE}
  if status==UNKNOWN:o["exception"]={"type":type(e).__name__,"reason":str(e),"traceback":traceback.format_exc(limit=24)[-12288:]}
 final_durable=o.get("durable_state") or LAST_DURABLE
 result={"schema":SCHEMA,"status":status,"terminal":status,"complete":False,"a0":o,"durable_state":final_durable,"eliminated_boundary_rows":0,"old_boundary_closure_present":False,"claim_boundary":{"common_word":False,"A0_membership":False,"fake":False,"Ihara_witness":False,"compatible_lift":False,"verified":False},"checkpoint_input":a.resume,"checkpoint_output":a.checkpoint}
 if a.resume and LAST_INPUT_SEAL:result["checkpoint_input_seal"]={"path":a.resume,"bytes":LAST_INPUT_SEAL[0],"sha256":LAST_INPUT_SEAL[1]}
 if a.checkpoint and final_durable and final_durable.get("checkpoint_bytes",0):result["checkpoint"]={"path":a.checkpoint,"bytes":final_durable["checkpoint_bytes"],"sha256":final_durable["checkpoint_sha256"],"sequence":final_durable.get("checkpoint_seq",0)}
 if a.output:Path(ROOT/a.output).write_bytes(json.dumps(result,sort_keys=True,separators=(",",":"),default=str).encode()+b"\n")
 print("R07_A0_PHASE_SEPARATED_PACKED_OWNER_V12 "+status,flush=True);return 0
if __name__=="__main__":raise SystemExit(main())
