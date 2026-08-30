#!/usr/bin/env python3
"""Task428: one-call Linux bootstrap traceback gate for the pinned v9 owner."""
from __future__ import annotations
import argparse,json,sys,traceback,types
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
V9=("search/d972_r07_a0_pb34_direct_quotient_owner_v9.py",26006,"98efac926970a5c3aa23a43b100ae64c52ce60ab0313d151f88b4dc37e6bd611")
MARK="R07_A0_V9_BOOTSTRAP_TRACE_V1"
def need(x,m):
 if not x:raise RuntimeError(m)
def sha(b):
 import hashlib
 return hashlib.sha256(b).hexdigest()
def load_v9():
 p=ROOT/V9[0];b=p.read_bytes();need(len(b)==V9[1] and sha(b)==V9[2],"v9_pin");m=types.ModuleType("task428_v9_pinned");m.__file__=str(p);exec(compile(b,V9[0],"exec"),m.__dict__,m.__dict__);return m
def receipt_for(call,path):
 status="BOOTSTRAP_READY";payload={"schema":"d972-r07-a0-v9-bootstrap-trace/v1"}
 expected=False
 try:
  result=call()
  expected=isinstance(result,dict) and result.get("status")=="UNKNOWN_RESOURCE" and str(result.get("reason","")).startswith("time_limit")
 except Exception as e:
  expected=type(e).__name__=="RuntimeError" and str(e).startswith("UNKNOWN_RESOURCE:time_limit")
  if not expected:
   status="TRACE_CAPTURED";payload["exception"]={"type":type(e).__name__,"message":str(e)[:2048],"traceback":traceback.format_exc(limit=40)[-16384:]}
 if not expected and status=="BOOTSTRAP_READY":status="TRACE_CAPTURED"
 payload["status"]=status;payload["terminal"]=status;payload["v9_pin"]={"path":V9[0],"bytes":V9[1],"sha256":V9[2]}
 if path is not None:Path(path).parent.mkdir(parents=True,exist_ok=True);Path(path).write_text(json.dumps(payload,sort_keys=True,separators=(",",":"))+"\n",encoding="utf-8")
 print(MARK+" "+("READY" if status=="BOOTSTRAP_READY" else "TRACE_CAPTURED"),flush=True);return payload
def fixture():
 def toy_stop():raise RuntimeError("UNKNOWN_RESOURCE:time_limit")
 ready=receipt_for(toy_stop,None);need(ready["status"]=="BOOTSTRAP_READY","fixture_ready")
 captured=receipt_for(lambda:(_ for _ in ()).throw(ValueError("toy failure")),None);need(captured["status"]=="TRACE_CAPTURED" and captured["exception"]["type"]=="ValueError","fixture_trace")
 return {"status":"FIXTURE_PASS","toy_ready":True,"toy_trace_captured":True}
def main():
 ap=argparse.ArgumentParser();ap.add_argument("--mode",choices=("PRODUCTION","FIXTURE"),default="PRODUCTION");a=ap.parse_args()
 if a.mode=="FIXTURE":print(MARK+" FIXTURE_PASS "+json.dumps(fixture(),sort_keys=True,separators=(",",":")));return 0
 v9=load_v9();args=types.SimpleNamespace(checkpoint=None,resume=None,seconds=0,rss_bytes=4800000000)
 receipt_for(lambda:v9.run(args),"ci/out/d972_r07_a0_v9_bootstrap_trace_v1.json");return 0
if __name__=="__main__":raise SystemExit(main())
