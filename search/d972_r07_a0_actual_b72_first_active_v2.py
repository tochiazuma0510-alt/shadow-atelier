#!/usr/bin/env python3
"""Task437 v2: thin ABI wrapper around the authenticated Task436 producer."""
from __future__ import annotations
import argparse, hashlib, importlib.util, json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SCHEMA="d972-r07-a0-actual-b72-first-active/v2"
MARKER="R07_A0_ACTUAL_B72_FIRST_ACTIVE_V2"
V1=("search/d972_r07_a0_actual_b72_first_active_v1.py",24643,"5eecdfbce8c3224e52e990fcb3e923e01394b22f0da106d2969aa7e1fb8436cc")

def need(x,m):
    if not x: raise RuntimeError(m)
def sha(b): return hashlib.sha256(b).hexdigest()
def load_v1():
    p=ROOT/V1[0]; b=p.read_bytes(); need(len(b)==V1[1] and sha(b)==V1[2],"v1 producer pin")
    spec=importlib.util.spec_from_file_location("task437_v1_producer",p); need(spec and spec.loader,"v1 loader")
    m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

def run(a):
    m=load_v1(); original_prefix=m.prefix
    def adapted_prefix(v12,p435,args):
        P=original_prefix(v12,p435,args)
        P["p176"]=m._P176Adapter(P["p176"])
        return P
    m.prefix=adapted_prefix; m.SCHEMA=SCHEMA; m.MARKER=MARKER
    return m.run(a)

def main(argv=None):
    ap=argparse.ArgumentParser(); ap.add_argument("--mode",choices=("PRODUCTION","FIXTURE"),default="PRODUCTION")
    ap.add_argument("--output",default="ci/out/d972_r07_a0_actual_b72_first_active_v2.json")
    ap.add_argument("--checkpoint",default="ci/out/d972_r07_a0_actual_b72_first_active_v2_output.checkpoint")
    ap.add_argument("--seconds",type=float,default=2400); ap.add_argument("--rss-bytes",type=int,default=4_800_000_000); a=ap.parse_args(argv)
    try:
        if a.mode=="FIXTURE":
            m=load_v1(); r={"schema":SCHEMA,"status":"FIXTURE","fixture":m.fixture()}
        else: r=run(a); r["schema"]=SCHEMA
    except Exception as e:
        status="UNKNOWN_RESOURCE" if str(e).startswith("UNKNOWN_RESOURCE:") else "UNKNOWN"
        r={"schema":SCHEMA,"status":status,"terminal":status,"reason":str(e),"claims":{"A0":False,"COMMON":False,"NONMEMBER":False,"fake":False,"Ihara":False}}
    out=Path(a.output); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(r,sort_keys=True,separators=(",",":"))+"\n",encoding="ascii")
    print(f"{MARKER} status={r['status']}",flush=True); return 0
if __name__=="__main__": raise SystemExit(main())
