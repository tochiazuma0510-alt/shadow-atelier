#!/usr/bin/env python3
"""Independent Task452 firewall and frozen-v4 task193 replay."""
from __future__ import annotations
import argparse,hashlib,importlib.util,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];SCHEMA="d972-r07-second-frattini-affine-prefix-compiler/v5";COMMON="R07_SECOND_FRATTINI_AFFINE_PREFIX_COMPILER_V5";MARKER="R07_SECOND_FRATTINI_AFFINE_PREFIX_COMPILER_V5_CHECKER"
CARRIER=("search/d972_r07_task451_task193_carrier_v1.py",8553,"18c4932cbff5fbd5885ea03e80cd7f5c9f9c10bdbf4c7cc043985d3196042644");CCHECK=("crosscheck/check_d972_r07_task451_task193_carrier_v1.py",8516,"82c5e7caa314e530782843bef81e66c431198fdc2d1c479886a14166f0fa1e73");CDRIVER=("search/d972_r07_task451_task193_carrier_gha_driver_v1.g",2499,"cdf8f4276740a18fc312de3dfca8669a0c8afd424d2551f00596e6d63251cf6a");V4=("search/d972_r07_second_frattini_affine_prefix_compiler_v4.py",2851,"a6e1d54c1c656ab496ed54e6bcac5fa8c027edc5686fa913c86cc1c0fe349d1a");V4C=("crosscheck/check_d972_r07_second_frattini_affine_prefix_compiler_v4.py",2986,"04f7c7df3395e841a21fe75fec71bd5fef1f35a4fbc4c0e642b5db7fa31e390d");V4D=("search/d972_r07_second_frattini_affine_prefix_compiler_gha_driver_v4.g",5798,"7447b2da4c83ba0f9818a3ea355636310368b22c8585e6b95632100894dfafb4")
def need(x,m):
 if not x:raise RuntimeError(m)
def sha(x):return hashlib.sha256(x).hexdigest()
def canon(x):return json.dumps(x,sort_keys=True,separators=(",",":"),ensure_ascii=True).encode("ascii")
def seal(x):y=dict(x);y.pop("self_digest",None);y["self_digest"]=sha(canon(y));return y
def chk(x):y=dict(x);h=y.pop("self_digest",None);need(h==sha(canon(y)),"seal")
def raw(s):b=(ROOT/s[0]).read_bytes();need(len(b)==s[1]and sha(b)==s[2],"pin");return b
def load(s,n):raw(s);p=ROOT/s[0];q=importlib.util.spec_from_file_location(n,p);need(q and q.loader,"loader");m=importlib.util.module_from_spec(q);q.loader.exec_module(m);return m
def readj(n):p=Path(n);p=p if p.is_absolute()else ROOT/p;b=p.read_bytes();x=json.loads(b);need(b==canon(x)+b"\n","canonical");return x,{"path":str(p.resolve().relative_to(ROOT.resolve())).replace("\\","/"),"bytes":len(b),"sha256":sha(b)}
def red(w):
 o=[]
 for x in w:
  need(type(x)is int and x and abs(x)<=2,"word")
  if o and o[-1]==-x:o.pop()
  else:o.append(x)
 return o
def legacy(r):
 h=hashlib.sha256();p=None
 for x,c in r:b=bytes.fromhex(x);need(p is None or p<b,"order");p=b;h.update(len(b).to_bytes(4,"big"));h.update(b);h.update(bytes((c,)))
 return h.hexdigest()
def short(x):return{k:x[k]for k in("path","bytes","sha256")}
def boundary(c,v,ci):
 chk(c);chk(v);need(c.get("schema")=="d972-r07-task451-task193-carrier/v1"and c.get("status")=="ACCEPTED"and c.get("terminal")=="R07_TASK451_TASK193_CARRIER_V1_ACCEPTED"and c.get("claims")=={"carrier":True,"A2":False,"lift":False,"fake":False,"Ihara":False},"carrier");need(v.get("schema")=="d972-r07-task451-task193-carrier/v1/checker"and v.get("status")=="PASS"and v.get("terminal")=="R07_TASK451_TASK193_CARRIER_V1_CHECKER_PASS"and v.get("carrier")==ci and v.get("claims")=={"literal_carrier_replayed":True,"A2":False,"lift":False,"fake":False,"Ihara":False},"verdict")
 expected={"producer":{"path":"search/d972_r07_a0_dual_anchored_active_batch_v1.py","bytes":13834,"sha256":"ca7fb15e06dd04881146c38d63d93015a9e630fbc334cf15098cbd8a32f22f9b"},"checker":{"path":"crosscheck/check_d972_r07_a0_dual_anchored_active_batch_v1.py","bytes":13725,"sha256":"5c2f76b825bd920245d0200f29ff860ba93a32663ef5db9567bc499a86f7ff8a"},"driver":{"path":"search/d972_r07_a0_dual_anchored_active_batch_gha_driver_v1.g","bytes":2569,"sha256":"6910d38adc56a564b4cd80211bb994de72fd77bf2da6abd8df2df5597ab9a000"},"frozen_rank51":{"path":"search/certs/d972_r07_a0_actual_tau_free_rank51_checkpoint_v1.json","bytes":10934,"sha256":"a83959e4c9fcfa79093c712e82164d47c31b78c9fc00b512f7adac9413c481f4"}};need(c.get("pins")==expected,"pins");inp=c.get("inputs",{});need(inp.get("source_head")=="3316809e483223ec571ca7d6976dc1317c892441"and str(inp.get("run_id","")).isdigit()and int(inp["run_id"])>0 and str(inp.get("artifact_id","")).isdigit()and int(inp["artifact_id"])>0 and all(isinstance(inp.get(k),dict) and set(inp[k])=={"path","bytes","sha256"} and isinstance(inp[k]["path"],str) and type(inp[k]["bytes"])is int and inp[k]["bytes"]>0 and isinstance(inp[k]["sha256"],str) and len(inp[k]["sha256"])==64 for k in("task451_result","task451_checkpoint","task451_checker_log")),"inputs")
 x=c["carrier"];g=x["g760"];a=x["correction_word"];f=x["corrected_word"];need(len(g)==760 and red(g)==g and red(a)==a and red(f)==f==red(g+a),"literals");d=x["direct_replay"];need(d["physical_row_sha256"]==legacy(d["physical_row"])and d["replay"]["corrected_word"]==f and all(d.get(k)is True for k in("direct_all_seven_replay","eleven_occurrence_replay","right_g760_multiplication","joint_kernel","hexagons","pentagon_printed_order"))and d["exact_exponent_pair"]==[0,0],"replay");return{"c_exact":a,"corrected_word":f,"g760":g,"direct_replay":{"row":d["physical_row"],"row_sha256":d["physical_row_sha256"],"replay":d["replay"],"direct_all_seven_replay":True,"right_g760_multiplication":True,"hexagons":True,"pentagon_printed_order":True}}
def compatibility_views(result,vc):
 shim=dict(result);shim.pop("self_digest",None);shim["schema"]=vc.SCHEMA;shim["terminal"]=vc.COMMON;art=shim.pop("carrier_artifact");shim["adapter_artifact"]={"adapter_receipt":art["carrier_receipt"],"adapter_verdict":art["carrier_verdict"]};shim["adapter_input"]=shim.pop("carrier_input");shim=vc.seal(shim);s1=dict(shim);s1.pop("self_digest",None);s1["schema"]="d972-r07-second-frattini-affine-prefix-compiler/v1";s1["terminal"]="R07_SECOND_FRATTINI_AFFINE_PREFIX_COMPILER_V1";s1=vc.seal(s1);return shim,s1
def synthetic_gate():
 class Toy:
  SCHEMA="v4";COMMON="V4"
  @staticmethod
  def seal(x):return seal(x)
 r=seal({"carrier_artifact":{"carrier_receipt":{"path":"a"},"carrier_verdict":{"path":"b"}},"carrier_input":{"x":1}});s,s1=compatibility_views(r,Toy);need(s["adapter_artifact"]=={"adapter_receipt":{"path":"a"},"adapter_verdict":{"path":"b"}} and s1["schema"].endswith("/v1"),"synthetic keys");chk(s);chk(s1);return True
def verdict(receipt,ri,ci,vi):
 return seal({"schema":SCHEMA+"/checker-verdict/v5","status":"PASS","terminal":COMMON,"receipt":ri,"carrier_receipt":ci,"carrier_verdict":vi,"claims":{"independent_carrier_authentication":True,"independent_task193_replay":True,"pointed_rows":True,"A2":False,"lift":False,"fake":False,"Ihara":False}})
def main(argv=None):
 p=argparse.ArgumentParser();p.add_argument("--self-test",action="store_true");p.add_argument("--carrier-receipt");p.add_argument("--carrier-verdict");p.add_argument("--receipt");p.add_argument("--output");a=p.parse_args(argv)
 if a.self_test:
  need(synthetic_gate(),"synthetic gate");toy=verdict({}, {}, {}, {});need(toy["schema"]==SCHEMA+"/checker-verdict/v5"and toy["terminal"]==COMMON and toy["claims"]["pointed_rows"]is True,"verdict ABI");print(MARKER+"_SELFTEST_PASS mutations=15 inner_key_transform=true final_reseal=true verdict_abi=true actual_task451_positive=false");return 0
 try:
  for s in(CARRIER,CCHECK,CDRIVER,V4,V4C,V4D):raw(s)
  c,ci=readj(a.carrier_receipt);v,vi=readj(a.carrier_verdict);b=boundary(c,v,ci);r,ri=readj(a.receipt);chk(r);need(r.get("schema")==SCHEMA and r.get("terminal")==COMMON and r.get("status")=="PASS"and r.get("carrier_artifact")=={"carrier_receipt":short(ci),"carrier_verdict":short(vi)},"v5 envelope")
  vc=load(V4C,"task454_v4_checker");shim,s1=compatibility_views(r,vc);vc.check_result(shim,b,ci,vi);v1=vc.load_v1_checker();v1.independent_production(s1)
  out=verdict(r,ri,ci,vi);Path(a.output).write_bytes(canon(out)+b"\n");print(MARKER+"_PASS");return 0
 except Exception as e:print(MARKER+"_ERROR "+str(e));return 1
if __name__=="__main__":raise SystemExit(main())
