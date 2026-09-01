#!/usr/bin/env python3
"""Task448 phase-correct localized-support profile checker."""
from __future__ import annotations
import argparse,hashlib,importlib.util,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];MARKER="R07_A0_ACTUAL_TAU_FREE_RANK_LADDER_V5_CHECKER"
V4=("crosscheck/check_d972_r07_a0_actual_tau_free_rank_ladder_v4.py",5876,"fcd1fd1e4cbff30a4e472b1776aea011d62abe95cb8f51141883ad98db45242e")
def need(x,m):
    if not x:raise RuntimeError(m)
def sha(x):return hashlib.sha256(x).hexdigest()
def load(spec,name):
    p=ROOT/spec[0];raw=p.read_bytes();need(len(raw)==spec[1] and sha(raw)==spec[2],"pin:"+spec[0]);s=importlib.util.spec_from_file_location(name,p);need(s and s.loader,"loader");m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
c=load(V4,"task448_v4_checker")
def profile_shape(claimed):
    need(isinstance(claimed,dict),"profile object");complete="adjoint_digest" in claimed;has_count="localized_dual_support" in claimed;need(has_count==complete,"localized count phase");return complete
def independent_profile(P,m,p179,claimed,reason):
    complete=profile_shape(claimed)
    if not complete:return c.c.independent_profile(P,m,p179,claimed,reason)
    need(isinstance(claimed["localized_dual_support"],int),"localized count type");reduced=dict(claimed);reported=reduced.pop("localized_dual_support");c.c.independent_profile(P,m,p179,reduced,reason);count=0
    for key,value in sorted((P["dual"] or {}).items()):
        if key[:1]==b"N":continue
        try:block,label,blob=P["q"].parse(key)
        except Exception:continue
        if block in (1,2,3) and label!="tau":count+=1
    need(reported==count,"localized count");return claimed
c.independent_profile=independent_profile
def check(cert):return c.check(cert)
def self_test():
    need(profile_shape({"physical_rank":43}) is False,"valid basic");need(profile_shape({"adjoint_digest":"a"*64,"localized_dual_support":7}) is True,"valid adjoint");rejected=[]
    for label,p in (("basic_added_count",{"physical_rank":43,"localized_dual_support":0}),("adjoint_deleted_count",{"adjoint_digest":"a"*64})):
        try:profile_shape(p)
        except RuntimeError:rejected.append(label)
    need(len(rejected)==2,"phase mutations");return {"status":"PASS","valid_shapes":["basic_without_localized_count","adjoint_with_localized_count"],"mutation_rejections":rejected,"v4_selftest":c.self_test()}
def main(argv=None):
    ap=argparse.ArgumentParser();ap.add_argument("artifact",nargs="?");ap.add_argument("--self-test",action="store_true");a=ap.parse_args(argv)
    if a.self_test:print(MARKER+"_SELFTEST_PASS "+json.dumps(self_test(),sort_keys=True));return 0
    need(a.artifact,"artifact");check(json.loads(Path(a.artifact).read_text(encoding="ascii")));print(MARKER+"_PASS");return 0
if __name__=="__main__":raise SystemExit(main())
