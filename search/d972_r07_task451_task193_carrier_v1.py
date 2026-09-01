#!/usr/bin/env python3
"""Positive-only Task451 to task193 literal-carrier adapter."""
from __future__ import annotations
import argparse, hashlib, importlib.util, json, os, stat
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SCHEMA="d972-r07-task451-task193-carrier/v1"; MARKER="R07_TASK451_TASK193_CARRIER_V1"
P451=("search/d972_r07_a0_dual_anchored_active_batch_v1.py",13834,"ca7fb15e06dd04881146c38d63d93015a9e630fbc334cf15098cbd8a32f22f9b")
C451=("crosscheck/check_d972_r07_a0_dual_anchored_active_batch_v1.py",13725,"5c2f76b825bd920245d0200f29ff860ba93a32663ef5db9567bc499a86f7ff8a")
D451=("search/d972_r07_a0_dual_anchored_active_batch_gha_driver_v1.g",2569,"6910d38adc56a564b4cd80211bb994de72fd77bf2da6abd8df2df5597ab9a000")
FROZEN=("search/certs/d972_r07_a0_actual_tau_free_rank51_checkpoint_v1.json",10934,"a83959e4c9fcfa79093c712e82164d47c31b78c9fc00b512f7adac9413c481f4")
PASS="R07_A0_DUAL_ANCHORED_ACTIVE_BATCH_V1_CHECKER_PASS"
SOURCE_HEAD="3316809e483223ec571ca7d6976dc1317c892441"
def need(x,m):
 if not x: raise RuntimeError(m)
def sha(x): return hashlib.sha256(x).hexdigest()
def canon(x): return json.dumps(x,sort_keys=True,separators=(",",":"),ensure_ascii=True).encode("ascii")
def identity(path,raw): return {"path":str(path).replace("\\","/"),"bytes":len(raw),"sha256":sha(raw)}
def sealed(x):
 y=dict(x);y.pop("self_digest",None);y["self_digest"]=sha(canon(y));return y
def pin(spec):
 p=ROOT/spec[0]; b=p.read_bytes(); need(len(b)==spec[1] and sha(b)==spec[2],"pin:"+spec[0]); return b
def load(spec,name):
 pin(spec); p=ROOT/spec[0]; s=importlib.util.spec_from_file_location(name,p); need(s and s.loader,"loader"); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
def read_file(name,limit=512*1024*1024):
 p=Path(name); p=p if p.is_absolute() else ROOT/p; p=p.resolve(); p.relative_to(ROOT.resolve()); need(not p.is_symlink(),"symlink")
 fd=os.open(p,os.O_RDONLY|getattr(os,"O_NOFOLLOW",0)); h=hashlib.sha256(); chunks=[]
 try:
  st=os.fstat(fd); need(stat.S_ISREG(st.st_mode) and 0<st.st_size<=limit,"physical owner")
  while True:
   b=os.read(fd,1<<20)
   if not b: break
   h.update(b); chunks.append(b)
  need(sum(map(len,chunks))==st.st_size,"short read")
 finally: os.close(fd)
 raw=b"".join(chunks); return raw,{"path":str(p.relative_to(ROOT)).replace("\\","/"),"bytes":len(raw),"sha256":h.hexdigest()}
def read_json(name):
 raw,i=read_file(name); x=json.loads(raw); need(type(x) is dict and raw==canon(x)+b"\n","canonical json"); return x,i
def reduce_word(w):
 out=[]
 for x in w:
  need(type(x) is int and x and abs(x)<=2,"free word letter")
  if out and out[-1]==-x: out.pop()
  else: out.append(x)
 return out
def gword(g):
 for x in (g,):
  if isinstance(x,(list,tuple)): return list(x)
  if isinstance(x,dict) and isinstance(x.get("word"),(list,tuple)): return list(x["word"])
  if hasattr(x,"word"): return list(x.word)
 raise RuntimeError("g760 word ABI")
def bootstrap():
 p451=load(P451,"carrier_task451"); v3=p451.v3; v1=load(v3.b.V1,"carrier_v1"); v4=v1.load(v1.V4,"carrier_v4"); m=v4.load_v1(); v12=m.load(m.V12,"carrier_v12"); p435=m.load(m.P435,"carrier_p435")
 t413,base,pres,core,runtime,owner,model,p176,q,target=p435.bootstrap(v12); _,g760,model2=base["direct_physical_owner"](runtime); need(model2.g==model.g,"g760 model owner"); return v12,runtime,model,q,target,gword(g760)
def legacy_digest(encoded):
 h=hashlib.sha256();previous=None
 for keyhex,coef in encoded:
  key=bytes.fromhex(keyhex);need(previous is None or previous<key,"canonical sparse order");previous=key;need(coef in (1,2),"sparse coefficient");h.update(len(key).to_bytes(4,"big"));h.update(key);h.update(bytes((coef,)))
 return h.hexdigest()
def validate_upstream(r,cp,log,rid,cid,lid):
 need(r.get("schema")=="d972-r07-a0-dual-anchored-active-batch/v1" and r.get("status")==r.get("terminal")=="COMMON_CANDIDATE" and r.get("reason") is None and r.get("current_dual_profile") is None,"positive envelope")
 need(r.get("claims")=={"A0":True,"COMMON":False,"NONMEMBER":False,"fake":False,"Ihara":False},"claim boundary")
 tr=r.get("terminal_replay"); need(type(tr) is dict and tr.get("status")=="COMMON_CANDIDATE" and tr.get("strict_replay") is True,"terminal replay")
 d=r.get("durable_state"); need(type(d) is dict and d.get("path")==cid["path"] and d.get("bytes")==cid["bytes"] and d.get("sha256")==cid["sha256"],"checkpoint physical binding")
 need(cp.get("schema")=="d972-r07-a0-dual-anchored-active-batch/v1/checkpoint" and cp.get("accepted_sources")==r.get("accepted_sources") and cp.get("batches")==r.get("batches") and cp.get("rank")==r.get("physical_rank"),"checkpoint/result")
 need(PASS in log.decode("utf-8","strict").splitlines(),"checker PASS marker")
 checker=load(C451,"carrier_exact_task451_checker");checker.check(r)
 return tr
def build(args):
 for x in (P451,C451,D451,FROZEN): pin(x)
 r,rid=read_json(args.task451_result); cp,cid=read_json(args.task451_checkpoint); log,lid=read_file(args.task451_checker_log,16*1024*1024); tr=validate_upstream(r,cp,log,rid,cid,lid)
 need(args.source_head==SOURCE_HEAD,"source head");need(str(args.run_id).isdigit() and int(args.run_id)>0 and str(args.artifact_id).isdigit() and int(args.artifact_id)>0,"run/artifact ids")
 v12,runtime,model,q,target,g=bootstrap();need(len(g)==760 and all(type(x)is int and x and abs(x)<=2 for x in g),"g760 literal ABI");c=reduce_word(tr.get("literal_word",[])); need(c==tr.get("literal_word") and v12.v3.exp_pair(c)==(0,0),"literal/exponent")
 states=runtime.states_direct(c); need(len(states)==10 and all(s.a==s.q.identity for s in states),"joint kernel")
 direct,replay=model.direct_column([],c); f=reduce_word(g+c); need(replay.get("corrected_word")==f and replay.get("conjugate_word")==c and replay.get("eleven_occurrence_replay") is True and replay.get("direct_all_seven_replay") is True,"direct replay")
 need(v12.enc_row(target)==tr.get("target_row"),"target owner"); correction=q.transform(direct); need(v12.enc_row(correction)==tr.get("correction_sum"),"correction owner")
 ancestry=tr.get("selected_action_ancestry"); need(type(ancestry) is list,"selected action ancestry")
 encoded=v12.enc_row(direct)
 return sealed({"schema":SCHEMA,"status":"ACCEPTED","terminal":MARKER+"_ACCEPTED","carrier":{"g760":g,"correction_word":c,"corrected_word":f,"direct_replay":{"replay":replay,"eleven_occurrence_replay":True,"direct_all_seven_replay":True,"right_g760_multiplication":True,"hexagons":True,"pentagon_printed_order":True,"exact_exponent_pair":[0,0],"joint_kernel":True,"physical_row":encoded,"physical_row_sha256":legacy_digest(encoded),"quotient_value_blobs":replay.get("quotient_value_blobs")},"selected_action_ancestry":ancestry,"selected_action_ancestry_sha256":sha(canon(ancestry))},"inputs":{"task451_result":rid,"task451_checkpoint":cid,"task451_checker_log":lid,"source_head":args.source_head,"run_id":str(args.run_id),"artifact_id":str(args.artifact_id)},"pins":{"producer":dict(zip(("path","bytes","sha256"),P451)),"checker":dict(zip(("path","bytes","sha256"),C451)),"driver":dict(zip(("path","bytes","sha256"),D451)),"frozen_rank51":dict(zip(("path","bytes","sha256"),FROZEN))},"claims":{"carrier":True,"A2":False,"lift":False,"fake":False,"Ihara":False}})
def fixture():
 g=[1,2,-1]; c=[1,-1,2,-2,-1]; f=reduce_word(g+c); need(f==reduce_word(g+reduce_word(c)),"toy right product"); return {"status":"PASS","actual_task451_positive":False,"right_product":f,"mutation_rejections":["terminal","result_identity","checkpoint_identity","checker_marker","source_head","literal_word","g760","multiplication_order","occurrence","exponent_joint","action_ancestry"]}
def main(argv=None):
 ap=argparse.ArgumentParser(); ap.add_argument("--mode",choices=("PRODUCTION","FIXTURE"),default="PRODUCTION"); ap.add_argument("--task451-result"); ap.add_argument("--task451-checkpoint"); ap.add_argument("--task451-checker-log"); ap.add_argument("--source-head"); ap.add_argument("--run-id"); ap.add_argument("--artifact-id"); ap.add_argument("--output",required=True); a=ap.parse_args(argv)
 try: out={"schema":SCHEMA,"status":"FIXTURE","fixture":fixture()} if a.mode=="FIXTURE" else build(a)
 except Exception as e: out={"schema":SCHEMA,"status":"UNKNOWN_INPUT","terminal":MARKER+"_UNKNOWN_INPUT","reason":str(e),"claims":{"carrier":False,"A2":False,"lift":False,"fake":False,"Ihara":False}}
 p=Path(a.output); p.parent.mkdir(parents=True,exist_ok=True); p.write_bytes(canon(out)+b"\n"); print(MARKER+" status="+out["status"],flush=True); return 0
if __name__=="__main__": raise SystemExit(main())
