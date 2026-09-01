#!/usr/bin/env python3
"""Helper-nonshared checker for the Task451/task193 literal carrier."""
from __future__ import annotations
import argparse,hashlib,importlib.util,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];SCHEMA="d972-r07-task451-task193-carrier/v1";MARKER="R07_TASK451_TASK193_CARRIER_V1_CHECKER"
P451=("search/d972_r07_a0_dual_anchored_active_batch_v1.py",13834,"ca7fb15e06dd04881146c38d63d93015a9e630fbc334cf15098cbd8a32f22f9b");C451=("crosscheck/check_d972_r07_a0_dual_anchored_active_batch_v1.py",13725,"5c2f76b825bd920245d0200f29ff860ba93a32663ef5db9567bc499a86f7ff8a");D451=("search/d972_r07_a0_dual_anchored_active_batch_gha_driver_v1.g",2569,"6910d38adc56a564b4cd80211bb994de72fd77bf2da6abd8df2df5597ab9a000");FROZEN=("search/certs/d972_r07_a0_actual_tau_free_rank51_checkpoint_v1.json",10934,"a83959e4c9fcfa79093c712e82164d47c31b78c9fc00b512f7adac9413c481f4");PASS="R07_A0_DUAL_ANCHORED_ACTIVE_BATCH_V1_CHECKER_PASS"
SOURCE_HEAD="3316809e483223ec571ca7d6976dc1317c892441";ACCEPTED="R07_TASK451_TASK193_CARRIER_V1_ACCEPTED"
def need(x,m):
 if not x:raise RuntimeError(m)
def sha(x):return hashlib.sha256(x).hexdigest()
def canon(x):return json.dumps(x,sort_keys=True,separators=(",",":"),ensure_ascii=True).encode("ascii")
def seal(x):
 y=dict(x);y.pop("self_digest",None);y["self_digest"]=sha(canon(y));return y
def checkseal(x):
 y=dict(x);h=y.pop("self_digest",None);need(isinstance(h,str) and h==sha(canon(y)),"carrier seal")
def raw(spec):
 b=(ROOT/spec[0]).read_bytes();need(len(b)==spec[1] and sha(b)==spec[2],"pin:"+spec[0]);return b
def load(spec,name):
 raw(spec);p=ROOT/spec[0];s=importlib.util.spec_from_file_location(name,p);need(s and s.loader,"loader");m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def read(path):
 p=Path(path);p=p if p.is_absolute() else ROOT/p;b=p.read_bytes();return b,{"path":str(p.resolve().relative_to(ROOT.resolve())).replace("\\","/"),"bytes":len(b),"sha256":sha(b)}
def readj(path):
 b,i=read(path);x=json.loads(b);need(type(x)is dict and b==canon(x)+b"\n","canonical json");return x,i
def red(w):
 o=[]
 for x in w:
  need(type(x)is int and x and abs(x)<=2,"word")
  if o and o[-1]==-x:o.pop()
  else:o.append(x)
 return o
def gword(x):
 if isinstance(x,(list,tuple)):return list(x)
 if isinstance(x,dict):return list(x["word"])
 return list(x.word)
def boot():
 p=load(P451,"carrier_check_p451");v3=p.v3;v1=load(v3.b.V1,"carrier_check_v1");v4=v1.load(v1.V4,"carrier_check_v4");m=v4.load_v1();v12=m.load(m.V12,"carrier_check_v12");p435=m.load(m.P435,"carrier_check_p435");_,base,_,_,rt,_,model,_,q,target=p435.bootstrap(v12);_,g,_=base["direct_physical_owner"](rt);return v12,rt,model,q,target,gword(g)
def legacy_digest(encoded):
 h=hashlib.sha256();prev=None
 for keyhex,coef in encoded:
  k=bytes.fromhex(keyhex);need(prev is None or prev<k,"sparse order");prev=k;need(coef in (1,2),"sparse coefficient");h.update(len(k).to_bytes(4,"big"));h.update(k);h.update(bytes((coef,)))
 return h.hexdigest()
def check(a):
 for s in (P451,C451,D451,FROZEN):raw(s)
 art,aid=readj(a.carrier);r,rid=readj(a.task451_result);cp,cid=readj(a.task451_checkpoint);log,lid=read(a.task451_checker_log)
 need(PASS in log.decode().splitlines(),"checker marker");need(r.get("status")==r.get("terminal")=="COMMON_CANDIDATE" and r.get("reason")is None and r.get("current_dual_profile")is None and r.get("claims")=={"A0":True,"COMMON":False,"NONMEMBER":False,"fake":False,"Ihara":False},"upstream envelope")
 need(r.get("durable_state",{}).get("path")==cid["path"] and r.get("durable_state",{}).get("bytes")==cid["bytes"] and r.get("durable_state",{}).get("sha256")==cid["sha256"] and cp.get("accepted_sources")==r.get("accepted_sources") and cp.get("batches")==r.get("batches"),"physical checkpoint")
 exact=load(C451,"carrier_check_exact_c451");exact.check(r)
 tr=r.get("terminal_replay");need(type(tr)is dict and tr.get("status")=="COMMON_CANDIDATE" and tr.get("strict_replay")is True,"positive replay")
 checkseal(art);need(art.get("schema")==SCHEMA and art.get("status")=="ACCEPTED" and art.get("terminal")==ACCEPTED and art.get("claims")=={"carrier":True,"A2":False,"lift":False,"fake":False,"Ihara":False},"carrier envelope")
 inputs=art.get("inputs",{});need(inputs.get("task451_result")==rid and inputs.get("task451_checkpoint")==cid and inputs.get("task451_checker_log")==lid and inputs.get("source_head")==SOURCE_HEAD and str(inputs.get("run_id","")).isdigit() and int(inputs["run_id"])>0 and str(inputs.get("artifact_id","")).isdigit() and int(inputs["artifact_id"])>0,"input identities")
 need(art.get("pins")=={"producer":dict(zip(("path","bytes","sha256"),P451)),"checker":dict(zip(("path","bytes","sha256"),C451)),"driver":dict(zip(("path","bytes","sha256"),D451)),"frozen_rank51":dict(zip(("path","bytes","sha256"),FROZEN))},"exact pins")
 v12,rt,model,q,target,g=boot();need(len(g)==760 and all(type(x)is int and x and abs(x)<=2 for x in g),"g760 literal ABI");car=art.get("carrier",{});c=red(car.get("correction_word",[]));f=red(g+c);need(g==car.get("g760") and c==tr.get("literal_word")==car.get("correction_word") and f==car.get("corrected_word"),"literal right carrier")
 need(v12.v3.exp_pair(c)==(0,0) and len(rt.states_direct(c))==10 and all(s.a==s.q.identity for s in rt.states_direct(c)),"exact joint kernel")
 direct,replay=model.direct_column([],c);need(replay.get("corrected_word")==f and replay.get("eleven_occurrence_replay")is True and replay.get("direct_all_seven_replay")is True,"independent direct replay")
 need(v12.enc_row(target)==tr.get("target_row") and v12.enc_row(q.transform(direct))==tr.get("correction_sum"),"target/correction owner")
 dr=car.get("direct_replay",{});encoded=v12.enc_row(direct);need(dr.get("replay")==replay and dr.get("physical_row")==encoded and dr.get("physical_row_sha256")==legacy_digest(encoded) and dr.get("exact_exponent_pair")==[0,0] and dr.get("joint_kernel")is True and dr.get("eleven_occurrence_replay")is True and dr.get("direct_all_seven_replay")is True and dr.get("right_g760_multiplication")is True and dr.get("hexagons")is True and dr.get("pentagon_printed_order")is True,"carrier gates")
 anc=tr.get("selected_action_ancestry");need(car.get("selected_action_ancestry")==anc and car.get("selected_action_ancestry_sha256")==sha(canon(anc)),"action ancestry")
 return seal({"schema":SCHEMA+"/checker","status":"PASS","terminal":MARKER+"_PASS","carrier":aid,"claims":{"literal_carrier_replayed":True,"A2":False,"lift":False,"fake":False,"Ihara":False}})
def selftest():
 base={"terminal":ACCEPTED,"result":"a","checkpoint":"b","marker":PASS,"head":SOURCE_HEAD,"run":"1","artifact":"2","c":[1],"g":[2],"f":[2,1],"occ":True,"exp":[0,0],"joint":True,"anc":[],"row_digest":legacy_digest([["01",1]]),"replay":{"corrected_word":[2,1]},"hexagons":True,"pentagon":True}
 def gate(x):
  need(x["terminal"]==ACCEPTED and x["result"]=="a" and x["checkpoint"]=="b" and x["marker"]==PASS and x["head"]==SOURCE_HEAD and x["run"].isdigit() and int(x["run"])>0 and x["artifact"].isdigit() and int(x["artifact"])>0,"toy provenance")
  need(x["c"]==[1] and x["g"]==[2] and x["f"]==red(x["g"]+x["c"]),"toy literals")
  need(x["occ"] is True and x["exp"]==[0,0] and x["joint"] is True and x["anc"]==[] and x["row_digest"]==legacy_digest([["01",1]]) and x["replay"]=={"corrected_word":[2,1]} and x["hexagons"]is True and x["pentagon"]is True,"toy replay")
 labels=list(("terminal result checkpoint marker head run artifact c g f occ exp joint anc row_digest replay hexagons pentagon").split());rejected=[];gate(base)
 for k in labels:
  x=json.loads(json.dumps(base));x[k]=None
  try:gate(x)
  except (RuntimeError,TypeError,AttributeError):rejected.append(k)
 need(len(rejected)==18,"mutation fixture");return {"status":"PASS","actual_task451_positive":False,"mutation_rejections":rejected,"canonical_seal":seal({"toy":True})["self_digest"]}
def main(argv=None):
 ap=argparse.ArgumentParser();ap.add_argument("--self-test",action="store_true");ap.add_argument("--carrier");ap.add_argument("--task451-result");ap.add_argument("--task451-checkpoint");ap.add_argument("--task451-checker-log");ap.add_argument("--output");a=ap.parse_args(argv)
 if a.self_test:print(MARKER+"_SELFTEST_PASS "+json.dumps(selftest(),sort_keys=True));return 0
 try:o=check(a)
 except Exception as e:print(MARKER+"_ERROR "+str(e),flush=True);return 1
 if a.output:Path(a.output).write_bytes(canon(o)+b"\n")
 print(MARKER+"_PASS",flush=True);return 0
if __name__=="__main__":raise SystemExit(main())
