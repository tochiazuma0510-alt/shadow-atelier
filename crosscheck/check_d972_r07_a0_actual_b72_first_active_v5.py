#!/usr/bin/env python3
"""Task440 v5 checker: bind prefix dual into P before unchanged v1 gates."""
from __future__ import annotations
import argparse,hashlib,importlib.util,json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SCHEMA="d972-r07-a0-actual-b72-first-active/v4"
MARKER="R07_A0_ACTUAL_B72_FIRST_ACTIVE_V5_CHECKER"
V1=("crosscheck/check_d972_r07_a0_actual_b72_first_active_v1.py",13834,"3c58382737317aa31fd5e94039730d8dc0c152a9c2be8f4c263ef31f90004916")
def need(x,m):
    if not x:raise RuntimeError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def load_v1():
    p=ROOT/V1[0];b=p.read_bytes();need(len(b)==V1[1] and sha(b)==V1[2],"v1 checker pin");s=importlib.util.spec_from_file_location("task440_v1_checker",p);need(s and s.loader,"v1 checker loader");m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
class P176Adapter(dict):
    def __getattr__(self,name):
        try:return self[name]
        except KeyError:raise AttributeError(name)
def adapt(P):
    need(isinstance(P,dict) and isinstance(P.get("p176"),dict),"checker adapter input");P["p176"]=P176Adapter(P["p176"]);base=dict(P.get("base",{}));t413=P.get("t413",{});need("load_json" in t413,"checker loader ABI");base["load_json"]=t413["load_json"];P["base"]=base;need(P["base"]["load_json"] is P["t413"]["load_json"],"checker loader identity");return P
def bind_prefix(original,v12,P):
    result=original(v12,P);need(isinstance(result,tuple) and len(result)>=2 and result[1] is not None,"prefix dual ABI");dual=result[1];P["dual"]=dual;need(P["dual"] is dual,"prefix dual identity");return result
def toy():
    dual=object();P={}
    def original(v12,state):return ("phys",dual,"remainder",{"status":"toy"})
    result=bind_prefix(original,None,P);need(result[1] is dual and P["dual"] is result[1],"toy dual identity");return True
def main(argv=None):
    ap=argparse.ArgumentParser();ap.add_argument("artifact",nargs="?");ap.add_argument("--self-test",action="store_true");a=ap.parse_args(argv);m=load_v1();original_bootstrap=m.bootstrap;original_prefix=m.prefix
    def bootstrap(v12):return adapt(original_bootstrap(v12))
    def prefix(v12,P):return bind_prefix(original_prefix,v12,P)
    m.bootstrap=bootstrap;m.prefix=prefix;m.SCHEMA=SCHEMA;m.MARKER=MARKER
    if a.self_test:toy();r=m.self_test();print(f"{MARKER}_SELFTEST_PASS {json.dumps(r,sort_keys=True)}");return 0
    need(a.artifact,"artifact");m.check(json.loads(Path(a.artifact).read_text(encoding="ascii")));print(f"{MARKER}_PASS");return 0
if __name__=="__main__":raise SystemExit(main())
