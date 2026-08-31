#!/usr/bin/env python3
"""Task439 v4 independent checker wrapper and exact-section toy."""
from __future__ import annotations
import argparse,hashlib,importlib.util,json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1];SCHEMA="d972-r07-a0-actual-b72-first-active/v4";MARKER="R07_A0_ACTUAL_B72_FIRST_ACTIVE_V4_CHECKER"
V1=("crosscheck/check_d972_r07_a0_actual_b72_first_active_v1.py",13834,"3c58382737317aa31fd5e94039730d8dc0c152a9c2be8f4c263ef31f90004916")
def need(x,m):
    if not x:raise RuntimeError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def load_v1():
    p=ROOT/V1[0];b=p.read_bytes();need(len(b)==V1[1] and sha(b)==V1[2],"v1 checker pin");s=importlib.util.spec_from_file_location("task439_v1_checker",p);need(s and s.loader,"v1 checker loader");m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
class P176Adapter(dict):
    def __getattr__(self,name):
        try:return self[name]
        except KeyError:raise AttributeError(name)
def adapt(P):
    need(isinstance(P,dict) and isinstance(P.get("p176"),dict),"checker adapter input");P["p176"]=P176Adapter(P["p176"]);base=dict(P.get("base",{}));t413=P.get("t413",{});need("load_json" in t413,"checker loader ABI");base["load_json"]=t413["load_json"];P["base"]=base;need(P["base"]["load_json"] is P["t413"]["load_json"],"checker loader identity");return P
def exact_section(records,target):
    for qid,row in enumerate(records):
        if row[:36]!=target[:36]:continue
        if row!=target:continue
        return qid
    return None
def toy():
    value=lambda x:("value",x);loader=lambda *x:("load",x);P=adapt({"p176":{"value_from_blob":value},"base":{},"t413":{"load_json":loader}});need(P["p176"].value_from_blob("x")==("value","x") and P["base"]["load_json"] is loader,"bootstrap adapters");coarse=b"c"*36;wrong=coarse+b"bad!";exact=coarse+b"good";need(exact_section([wrong,exact],exact)==1,"full section exact acceptance");need(exact_section([wrong],exact) is None,"full section collision rejection");return True
def main(argv=None):
    ap=argparse.ArgumentParser();ap.add_argument("artifact",nargs="?");ap.add_argument("--self-test",action="store_true");a=ap.parse_args(argv);m=load_v1();original=m.bootstrap
    def bootstrap(v12):return adapt(original(v12))
    m.bootstrap=bootstrap;m.SCHEMA=SCHEMA;m.MARKER=MARKER
    if a.self_test:toy();r=m.self_test();print(f"{MARKER}_SELFTEST_PASS {json.dumps(r,sort_keys=True)}");return 0
    need(a.artifact,"artifact");m.check(json.loads(Path(a.artifact).read_text(encoding="ascii")));print(f"{MARKER}_PASS");return 0
if __name__=="__main__":raise SystemExit(main())
