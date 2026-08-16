#!/usr/bin/env python3
"""Independent checker for one numeric simplified-presentation ordering shard."""
from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path
from typing import Any
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"search/certs/d972_b4_p2_magnus_input_v2_20260816.json"; WORDS=ROOT/"search/certs/d972_b4_word_key_artifact_v1_20260816.json"
SOURCE_SHA="c61b2b77131127aca83a8d7c56b7fdadd2d519b040ea4d91093622c813c2b4a9"; RELATOR_SHA="12fc1146dce5179c2b5fc44a3ceed6356a6b2c4835a564b55e9a9cd679fccd2e"; RHO=((-6,-5,-3),(3,),(5,),(-3,-2,-1),(-5,-4,-1),(1,)); NORM_SHA="ecf0cc8425bc24bdf6a8a352c223398221c4b179e09ee9a0bfe3dc888861683e"; WORDS_SHA="564a921be8114bdeb963f679c121e8d9aa90e148c65e95e393874fcba843e9f9"; TARGET_SHA="9c77e6768feb7ffe7143abf18f753af70e81b8e9cc792910c30ae0075d3b1d62"; TUPLE_SHA="32e78ca5b97cd8a6fa59a150dac77719c1b8cb527f0467570c4d284600465a91"; TRANSPORT_SHA="535d033019140e76cb9d3d7452b3e551c156f50ce74728b76bf6238d81806323"; SIMPLE_REL_SHA="6d614c32365753d62477cad8803420ffa58bcca0b5d18b0e5eadaaf6bf81b35a"; SIMPLE_NORM_SHA="127f029a2bafc7f8adf249b8c5f37cda594b105d3e1b567ba00400771cdca63e"
PERMS=((1,2,3,4,5),(2,1,3,4,5),(3,2,1,4,5),(4,2,3,1,5),(5,2,3,4,1),(2,3,4,5,1),(5,1,2,3,4),(2,1,4,3,5),(3,4,5,1,2),(5,4,3,2,1))
def dig(x:Any)->str:return hashlib.sha256(json.dumps(x,separators=(",",":"),ensure_ascii=True).encode()).hexdigest()
def red(w):
 o=[]
 for x in w:
  if x==0 or abs(x)>6:raise ValueError("F6")
  if o and o[-1]==-x:o.pop()
  else:o.append(x)
 return o
def rho(w):
 o=[]
 for x in w:
  a=list(RHO[abs(x)-1]);o.extend([-y for y in reversed(a)] if x<0 else a)
 return red(o)
def norm(w):
 c=red([(1 if x>0 else -1) if abs(x)==1 else (4 if x>0 else -4) for x in w]);a=[]
 for _ in range(5):a.append(c);c=rho(c)
 o=[]
 for q in reversed(a):o=red(o+q)
 return o
def sub(w,mp):
 o=[]
 for x in w:
  a=list(mp[abs(x)-1]);a=[-y for y in reversed(a)] if x<0 else a
  for y in a:
   if o and o[-1]==-y:o.pop()
   else:o.append(y)
 return o
def rows(v,n,width,name):
 if not isinstance(v,list) or len(v)!=n:raise ValueError(name+" count")
 if any(not isinstance(w,list) or any(not isinstance(x,int) or x==0 or abs(x)>width for x in w) for w in v):raise ValueError(name+" shape")
 return [list(w) for w in v]
def canonical():
 sr=SOURCE.read_bytes();wr=WORDS.read_bytes()
 if hashlib.sha256(sr).hexdigest()!=SOURCE_SHA or hashlib.sha256(wr).hexdigest()!=WORDS_SHA:raise ValueError("artifact SHA")
 so=json.loads(sr);wo=json.loads(wr)
 if so.get("schema")!="d972-b4-p2-magnus-input/v2" or so.get("rho_words")!=[list(x) for x in RHO] or so.get("all_relators_sha256")!=RELATOR_SHA or len(so.get("all_relators",[]))!=158:raise ValueError("source")
 if wo.get("schema")!="d972-b4-word-key-artifact/v1" or wo.get("count")!=972 or wo.get("source_target_key_digest")!=TARGET_SHA or wo.get("frozen_tuple_sha256")!=TUPLE_SHA:raise ValueError("words")
 n=[];normal=[]
 for i,(_,k,w) in enumerate(wo["rows"]):
  if w=="":
   if i not in (0,891):raise ValueError("empty")
   w=[]
  normal.append([wo["rows"][i][0],k,[int(x) for x in w]])
 if dig(normal)!=wo.get("canonical_bytes_sha256"):raise ValueError("row digest")
 n=[norm(r[2]) for r in normal]
 if dig(n)!=NORM_SHA:raise ValueError("norm digest")
 return n
def verify(tp,r,norms):
 tr=tp.read_bytes()
 if hashlib.sha256(tr).hexdigest()!=TRANSPORT_SHA:raise ValueError("transport SHA")
 t=json.loads(tr)
 if t.get("schema")!="d972-b4-u-simplified-transport/v1" or t.get("source_sha256")!=SOURCE_SHA or t.get("relator_sha256")!=RELATOR_SHA or t.get("roof_norm_sha256")!=NORM_SHA or t.get("simple_relators_sha256")!=SIMPLE_REL_SHA or t.get("simple_norms_sha256")!=SIMPLE_NORM_SHA:raise ValueError("transport pins")
 sr=rows(t["simple_relators"],141,5,"relators");sn=rows(t["simple_norm_words"],972,5,"norms");mp=rows(t["original_to_simple_words"],6,5,"map")
 if dig(sr)!=SIMPLE_REL_SHA or dig(sn)!=SIMPLE_NORM_SHA or [sub(w,mp) for w in norms]!=sn:raise ValueError("transport replay")
 if r.get("schema")!="d972-b4-simplified-orderings/v1" or r.get("transport_receipt_sha256")!=TRANSPORT_SHA:raise ValueError("ordering schema")
 for k,v in (("source_sha256",SOURCE_SHA),("relator_sha256",RELATOR_SHA),("roof_norm_sha256",NORM_SHA),("simple_relators_sha256",SIMPLE_REL_SHA),("simple_norms_sha256",SIMPLE_NORM_SHA)):
  if r.get(k)!=v:raise ValueError(k)
 oi=r.get("ordering_index");pi=r.get("permutation_index")
 if not isinstance(oi,int) or oi<1 or oi>8 or not isinstance(pi,int) or pi<1 or pi>10 or r.get("permutation")!=list(PERMS[pi-1]):raise ValueError("selector drift")
 rw=rows(r.get("reduced_norm_words"),972,5,"reduced")
 if dig(rw)!=r.get("reduced_norm_words_sha256"):raise ValueError("reduced digest")
 empty=sum(not w for w in rw)
 if r.get("empty_count")!=empty:raise ValueError("empty count")
 status=str(r.get("status"));final="UNKNOWN_ORDERING_NOT_NORMAL_STOP"
 if status=="ALL_EMPTY_REWRITE_CANDIDATE":final="UNKNOWN_ORDERING_ALL_EMPTY"
 elif status=="NONZERO_REDUCED_WORDS":final="UNKNOWN_ORDERING_NONZERO"
 return {"schema":"d972-b4-simplified-orderings-independent-check/v1","status":final,"ordering_index":oi,"permutation_index":pi,"norm_count":972,"empty_count":empty,"transport_words_replayed":True,"terminal_claim":False}
def main():
 p=argparse.ArgumentParser();p.add_argument("--receipt",type=Path,required=True);p.add_argument("--transport",type=Path,required=True);p.add_argument("--output",type=Path,required=True);a=p.parse_args();r=verify(a.transport.resolve(),json.loads(a.receipt.resolve().read_text()),canonical());raw=a.receipt.resolve().read_bytes();r["ordering_receipt_sha256"]=hashlib.sha256(raw).hexdigest();a.output.resolve().write_text(json.dumps(r,sort_keys=True,indent=2)+"\n",encoding="utf-8");print(json.dumps(r,sort_keys=True));return 2
if __name__=="__main__":raise SystemExit(main())
