#!/usr/bin/env python3
"""Task437 v2: independent checker wrapper with the Task436 p176 ABI adapter."""
from __future__ import annotations
import argparse, hashlib, importlib.util, json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SCHEMA="d972-r07-a0-actual-b72-first-active/v2"
MARKER="R07_A0_ACTUAL_B72_FIRST_ACTIVE_V2_CHECKER"
V1=("crosscheck/check_d972_r07_a0_actual_b72_first_active_v1.py",13834,"3c58382737317aa31fd5e94039730d8dc0c152a9c2be8f4c263ef31f90004916")
def need(x,m):
    if not x: raise RuntimeError(m)
def sha(b): return hashlib.sha256(b).hexdigest()
def load_v1():
    p=ROOT/V1[0]; b=p.read_bytes(); need(len(b)==V1[1] and sha(b)==V1[2],"v1 checker pin")
    spec=importlib.util.spec_from_file_location("task437_v1_checker",p); need(spec and spec.loader,"v1 checker loader")
    m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
def adapted_checker():
    m=load_v1()
    class P176Adapter(dict):
        def __getattr__(self,name):
            try:return self[name]
            except KeyError: raise AttributeError(name)
    original=m.bootstrap
    def bootstrap(v12):
        P=original(v12); P["p176"]=P176Adapter(P["p176"]); return P
    m.bootstrap=bootstrap; m.SCHEMA=SCHEMA; m.MARKER=MARKER; return m
def main(argv=None):
    ap=argparse.ArgumentParser(); ap.add_argument("artifact",nargs="?"); ap.add_argument("--self-test",action="store_true"); a=ap.parse_args(argv); m=adapted_checker()
    if a.self_test:
        print(f"{MARKER}_SELFTEST_PASS {json.dumps(m.self_test(),sort_keys=True)}"); return 0
    need(a.artifact,"artifact"); m.check(json.loads(Path(a.artifact).read_text(encoding="ascii"))); print(f"{MARKER}_PASS"); return 0
if __name__=="__main__": raise SystemExit(main())
