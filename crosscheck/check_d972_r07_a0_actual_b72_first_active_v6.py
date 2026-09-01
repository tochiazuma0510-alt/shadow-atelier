#!/usr/bin/env python3
"""Task441 v6 checker: close the audited dual/base/t413 context edges."""
from __future__ import annotations
import argparse,hashlib,importlib.util,json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SCHEMA="d972-r07-a0-actual-b72-first-active/v4"
MARKER="R07_A0_ACTUAL_B72_FIRST_ACTIVE_V6_CHECKER"
V1=("crosscheck/check_d972_r07_a0_actual_b72_first_active_v1.py",13834,"3c58382737317aa31fd5e94039730d8dc0c152a9c2be8f4c263ef31f90004916")
def need(x,m):
    if not x:raise RuntimeError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def load_v1():
    p=ROOT/V1[0];b=p.read_bytes();need(len(b)==V1[1] and sha(b)==V1[2],"v1 checker pin");s=importlib.util.spec_from_file_location("task441_v1_checker",p);need(s and s.loader,"v1 checker loader");m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
class P176Adapter(dict):
    def __getattr__(self,name):
        try:return self[name]
        except KeyError:raise AttributeError(name)
def adapt(P):
    need(isinstance(P,dict) and isinstance(P.get("p176"),dict),"checker adapter input");P["p176"]=P176Adapter(P["p176"]);base=dict(P.get("base",{}));t413=P.get("t413",{});need("load_json" in t413,"checker loader ABI");base["load_json"]=t413["load_json"];P["base"]=base;need(P["base"]["load_json"] is P["t413"]["load_json"],"checker loader identity");return P
def close_bootstrap(original,state,v12):
    P0=adapt(original(v12));state["base"]=P0["base"];state["t413"]=P0["t413"];need(state["base"] is P0["base"] and state["t413"] is P0["t413"],"bootstrap closure identity");return P0
def close_prefix(original,state,v12,P):
    result=original(v12,P);need(isinstance(result,tuple) and len(result)>=2 and result[1] is not None,"prefix dual ABI");need("base" in state and "t413" in state,"bootstrap closure state");P["dual"]=result[1];P["base"]=state["base"];P["t413"]=state["t413"];need(P["dual"] is result[1] and P["base"] is state["base"] and P["t413"] is state["t413"],"reduced context identity");return result
def toy():
    dual=object();t413={"load_json":lambda *x:x};original_base={"sentinel":object()};raw_result=("phys",dual,"remainder",{"status":"toy"});state={}
    def original_bootstrap(v12):return {"p176":{"value_from_blob":lambda x:x},"base":original_base,"t413":t413}
    P0=close_bootstrap(original_bootstrap,state,None);reduced={}
    def original_prefix(v12,P):return raw_result
    result=close_prefix(original_prefix,state,None,reduced);need(result is raw_result,"prefix tuple identity");need(reduced["dual"] is dual and reduced["base"] is P0["base"] and reduced["t413"] is t413,"three-object identity");need(reduced["dual"] is not reduced["base"] and reduced["dual"] is not reduced["t413"] and reduced["base"] is not reduced["t413"],"separate sentinels");return True
def main(argv=None):
    ap=argparse.ArgumentParser();ap.add_argument("artifact",nargs="?");ap.add_argument("--self-test",action="store_true");a=ap.parse_args(argv);m=load_v1();original_bootstrap=m.bootstrap;original_prefix=m.prefix;state={}
    def bootstrap(v12):return close_bootstrap(original_bootstrap,state,v12)
    def prefix(v12,P):return close_prefix(original_prefix,state,v12,P)
    m.bootstrap=bootstrap;m.prefix=prefix;m.SCHEMA=SCHEMA;m.MARKER=MARKER
    if a.self_test:toy();r=m.self_test();print(f"{MARKER}_SELFTEST_PASS {json.dumps(r,sort_keys=True)}");return 0
    need(a.artifact,"artifact");m.check(json.loads(Path(a.artifact).read_text(encoding="ascii")));print(f"{MARKER}_PASS");return 0
if __name__=="__main__":raise SystemExit(main())
