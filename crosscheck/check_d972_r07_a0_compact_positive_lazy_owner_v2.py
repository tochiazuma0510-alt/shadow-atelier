#!/usr/bin/env python3
"""Narrow independent receipt checker for task413 positive terminals."""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
BASE=("search/d972_r07_a0_compact_pc_invariant_owner_v1.py",68222,
      "be17be107103a218123cd0e1eb8455377ca2b52a2e54ec629f3744ad4c2d32f9")
JOINT=Path("ci/b345_157ee_artifacts_32359956713/d972_b345_joint_kernel_qstar_closure_v1.json")
Q3=Path("ci/b345_157ee_artifacts_32359956713/d972_b345_q3_chief_v1.json")
ROOF=Path("ci/in/d972_r07_seven_context_roof_presentation_v1.json")
ACCEPTANCE=Path("ci/in/d972_r07_seven_context_roof_presentation_v1.acceptance_v2.json")
PINS={str(JOINT):(2166036,"1c3ad7a7124cee152eb40968cf212c14641a9f8720063c85f70533864898d0df"),str(Q3):(231570,"3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72"),str(ROOF):(31017244,"82f7955580039f2a0271896c928515d26996f636d8e73231331da6a37f6b19f5"),str(ACCEPTANCE):(2722,"cc8c16c8ad8f2d094868f0897bcca2a98adba75c18bf7ff397f0da67fd233ea4")}
def fail(s): raise RuntimeError(s)
def word_inv(w): return [-x for x in reversed(w)]
def word_mul(*parts):
    out=[]
    for p in parts:
        for x in p:
            if out and out[-1]==-x: out.pop()
            else: out.append(x)
    return out
def word_pow(w,n):
    if n<0:return word_pow(word_inv(w),-n)
    out=[]
    for _ in range(n):out=word_mul(out,w)
    return out
def exp(w): return (sum(1 if x==1 else -1 if x==-1 else 0 for x in w),sum(1 if x==2 else -1 if x==-2 else 0 for x in w))
def load_base():
    p=ROOT/BASE[0]; raw=p.read_bytes()
    if len(raw)!=BASE[1] or hashlib.sha256(raw).hexdigest()!=BASE[2]:fail("task411_pin")
    ns={"__name__":"task411_checker_source","__file__":str(p)};exec(compile(raw,BASE[0],"exec"),ns,ns);return ns
def check_unknown(a0):
    if not isinstance(a0.get("reason"),str) or not a0["reason"]:fail("unknown_reason")
    if a0.get("common_word") is True or a0.get("member") is True:fail("unknown_overclaim")
def check_member(a0,pres):
    factors=a0.get("correction_factors")
    if not isinstance(factors,list):fail("correction_factors")
    c=[]
    for item in factors:
        if not isinstance(item,dict) or not isinstance(item.get("seed"),int) or not 1<=item["seed"]<=44:fail("factor_shape")
        d=item.get("delta_word",[]); coeff=item.get("coefficient")
        if not isinstance(d,list) or not all(isinstance(x,int) and x in (1,-1,2,-2) for x in d) or coeff not in (1,2):fail("factor_word")
        f=word_mul(d,pres["relators"][item["seed"]-1],word_inv(d)); c=word_mul(c,f if coeff==1 else word_inv(f))
    r3,r9,r12=pres["registered_q0_relators"][2],pres["registered_q0_relators"][8],pres["registered_q0_relators"][11]
    v0=word_mul(r9,r12,word_inv(r3),word_inv(r3));u0=word_mul(r9,word_pow(v0,-8)); e1,e2=exp(c)
    if e1%54 or e2%54:fail("pre_exactification_lattice")
    expected=word_mul(c,word_pow(u0,-3*(e1//54)),word_pow(v0,-3*(e2//54)))
    if a0.get("literal_correction")!=expected or exp(expected)!=(0,0):fail("exactification_word")
    if a0.get("exact_exponent_pair")!=[0,0]:fail("exact_exponent_pair")
    typed=a0.get("typed_boundary_preimage")
    if not isinstance(typed,list):fail("typed_boundary")
    for item in typed:
        if not isinstance(item,dict) or item.get("block") not in (1,2,3) or not isinstance(item.get("base_relator_index"),int) or not isinstance(item.get("translation_word"),list) or not isinstance(item.get("translation_hex"),str) and item.get("translation_word")!=[] or item.get("coefficient") not in (1,2):fail("typed_boundary_record")
    if a0.get("fake") is not False or a0.get("Ihara_witness") is not False:fail("witness_overclaim")
def main():
    ap=argparse.ArgumentParser();ap.add_argument("--producer");ap.add_argument("--fixture",action="store_true");a=ap.parse_args()
    try:
        if a.fixture:
            print("R07_A0_COMPACT_POSITIVE_LAZY_CHECKER_FIXTURE_PASS");return 0
        if not a.producer:fail("producer_required")
        out=json.loads(Path(a.producer).read_bytes())
        if out.get("schema")!="d972-r07-a0-compact-positive-lazy-owner/v2":fail("schema")
        if out.get("presentation",{}).get("compact_relator_count")!=44 or out.get("presentation",{}).get("relators_sha256")!="7612682d024b61f873928ad122c9a5d7462c812a6633112f08706cda4412b6c8":fail("compact_roster")
        if out.get("status")!=out.get("terminal") or out.get("claim_boundary",{}).get("fake") is not False:fail("envelope")
        a0=out.get("a0");
        if not isinstance(a0,dict):fail("a0")
        if a0.get("status") in ("UNKNOWN","UNKNOWN_RESOURCE"): check_unknown(a0)
        elif a0.get("status") in ("COMMON_WORD","COMMON_CANDIDATE"):
            base=load_base(); pres=base["compact"](base["load"](base["JOINT"]),base["load"](base["Q3"])); check_member(a0,pres)
        else:fail("terminal")
        print("R07_A0_COMPACT_POSITIVE_LAZY_CHECKER_PASS status="+str(a0.get("status")));return 0
    except Exception as e:
        print("R07_A0_COMPACT_POSITIVE_LAZY_CHECKER_FAIL:"+str(e));return 1
if __name__=="__main__":raise SystemExit(main())
