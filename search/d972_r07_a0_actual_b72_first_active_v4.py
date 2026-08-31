#!/usr/bin/env python3
"""Task439 v4: exact 40-byte section guard around Task436 v1."""
from __future__ import annotations
import argparse, hashlib, json, types
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SCHEMA="d972-r07-a0-actual-b72-first-active/v4"
MARKER="R07_A0_ACTUAL_B72_FIRST_ACTIVE_V4"
V1=("search/d972_r07_a0_actual_b72_first_active_v1.py",24643,"5eecdfbce8c3224e52e990fcb3e923e01394b22f0da106d2969aa7e1fb8436cc")
OLD='                if qid is None:continue\n                qword='
NEW='                if qid is None:continue\n                section=p["section_row"](self.rt["stores"],qid)\n                if section[coordinate]!=st:continue\n                qword='
def need(x,m):
    if not x:raise RuntimeError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def load_v1():
    path=ROOT/V1[0];raw=path.read_bytes();need(len(raw)==V1[1] and sha(raw)==V1[2],"v1 producer pin");source=raw.decode("utf-8").replace("\r\n","\n");need(source.count(OLD)==1,"canonical patch site");source=source.replace(OLD,NEW,1);m=types.ModuleType("task439_v1_producer");m.__file__=str(path);exec(compile(source,str(path),"exec"),m.__dict__);return m
def adapt(m,P):
    need(isinstance(P,dict) and isinstance(P.get("p176"),dict),"producer adapter input");P["p176"]=m._P176Adapter(P["p176"]);base=dict(P.get("base",{}));t413=P.get("t413",{});need("load_json" in t413,"producer loader ABI");base["load_json"]=t413["load_json"];P["base"]=base;need(P["base"]["load_json"] is P["t413"]["load_json"],"producer loader identity");return P
def exact_section(records,target):
    for qid,row in enumerate(records):
        if row[:36]!=target[:36]:continue
        if row!=target:continue
        return qid
    return None
def toy(m):
    value=lambda x:("value",x);loader=lambda *x:("load",x);P=adapt(m,{"p176":{"value_from_blob":value},"base":{},"t413":{"load_json":loader}});need(P["p176"].value_from_blob("x")==("value","x") and P["base"]["load_json"] is loader,"bootstrap adapters")
    coarse=b"c"*36;wrong=coarse+b"bad!";exact=coarse+b"good";need(exact_section([wrong,exact],exact)==1,"full section exact acceptance");need(exact_section([wrong],exact) is None,"full section collision rejection");return True
def run(a):
    m=load_v1();original=m.prefix
    def adapted_prefix(v12,p435,args):return adapt(m,original(v12,p435,args))
    m.prefix=adapted_prefix;m.SCHEMA=SCHEMA;m.MARKER=MARKER;return m.run(a)
def main(argv=None):
    ap=argparse.ArgumentParser();ap.add_argument("--mode",choices=("PRODUCTION","FIXTURE"),default="PRODUCTION");ap.add_argument("--output",default="ci/out/d972_r07_a0_actual_b72_first_active_v4.json");ap.add_argument("--checkpoint",default="ci/out/d972_r07_a0_actual_b72_first_active_v4_output.checkpoint");ap.add_argument("--seconds",type=float,default=2400);ap.add_argument("--rss-bytes",type=int,default=4_800_000_000);a=ap.parse_args(argv)
    try:
        if a.mode=="FIXTURE":m=load_v1();toy(m);r={"schema":SCHEMA,"status":"FIXTURE","fixture":m.fixture(),"exact_section_guard":"PASS"}
        else:r=run(a);r["schema"]=SCHEMA
    except Exception as e:
        status="UNKNOWN_RESOURCE" if str(e).startswith("UNKNOWN_RESOURCE:") else "UNKNOWN";r={"schema":SCHEMA,"status":status,"terminal":status,"reason":str(e),"claims":{"A0":False,"COMMON":False,"NONMEMBER":False,"fake":False,"Ihara":False}}
    out=Path(a.output);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(r,sort_keys=True,separators=(",",":"))+"\n",encoding="ascii");print(f"{MARKER} status={r['status']}",flush=True);return 0
if __name__=="__main__":raise SystemExit(main())
