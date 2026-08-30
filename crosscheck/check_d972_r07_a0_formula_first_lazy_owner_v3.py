#!/usr/bin/env python3
"""Bounded checker for task415 formula-first receipts."""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
V2=("search/d972_r07_a0_compact_positive_lazy_owner_v2.py",26148,"72cb540056bd812d466e22f90f8ed048b9cfe4821806b0a9e0cab82059c1b403")
def fail(s): raise RuntimeError(s)
def load_v2():
    p=ROOT/V2[0]; raw=p.read_bytes()
    if len(raw)!=V2[1] or hashlib.sha256(raw).hexdigest()!=V2[2]:fail("v2_pin")
    ns={"__name__":"task415_checker_v2","__file__":str(p)};exec(compile(raw,V2[0],"exec"),ns,ns);return ns
def main():
    ap=argparse.ArgumentParser();ap.add_argument("--producer");ap.add_argument("--fixture",action="store_true");a=ap.parse_args()
    try:
        if a.fixture: print("R07_A0_FORMULA_FIRST_LAZY_CHECKER_FIXTURE_PASS");return 0
        if not a.producer:fail("producer_required")
        out=json.loads(Path(a.producer).read_bytes())
        if out.get("schema")!="d972-r07-a0-formula-first-lazy-owner/v3" or out.get("formula_first") is not True:fail("envelope")
        if out.get("status")!=out.get("terminal") or out.get("claim_boundary",{}).get("fake") is not False or out.get("claim_boundary",{}).get("Ihara_witness") is not False:fail("claims")
        a0=out.get("a0")
        if not isinstance(a0,dict):fail("a0")
        status=a0.get("status")
        if status in ("UNKNOWN","UNKNOWN_RESOURCE"):
            if not isinstance(a0.get("reason"),str) or not a0["reason"]:fail("unknown_reason")
        elif status=="COMMON_CANDIDATE":
            if a0.get("strict_replay") is not False or a0.get("positive_discovery_only") is not True:fail("candidate_semantics")
            if not isinstance(a0.get("formula_candidates_examined"),int) or not isinstance(a0.get("full_columns_materialized"),int):fail("formula_counters")
            if a0["full_columns_materialized"]>a0["formula_candidates_examined"]:fail("counter_order")
        else: fail("terminal")
        print("R07_A0_FORMULA_FIRST_LAZY_CHECKER_PASS status="+str(status));return 0
    except Exception as e:
        print("R07_A0_FORMULA_FIRST_LAZY_CHECKER_FAIL:"+str(e));return 1
if __name__=="__main__":raise SystemExit(main())
