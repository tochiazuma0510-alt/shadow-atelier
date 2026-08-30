#!/usr/bin/env python3
"""Bounded receipt checker for task416 batch-lazy owner."""
from __future__ import annotations
import argparse,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def fail(s): raise RuntimeError(s)
def main():
    ap=argparse.ArgumentParser();ap.add_argument("--producer");ap.add_argument("--fixture",action="store_true");a=ap.parse_args()
    try:
        if a.fixture: print("R07_A0_BATCH_LAZY_CHECKER_FIXTURE_PASS");return 0
        if not a.producer:fail("producer_required")
        out=json.loads(Path(a.producer).read_bytes())
        if out.get("schema")!="d972-r07-a0-batch-lazy-owner/v4" or out.get("status")!=out.get("terminal"):fail("envelope")
        if out.get("claim_boundary",{}).get("fake") is not False or out.get("claim_boundary",{}).get("Ihara_witness") is not False:fail("claims")
        a0=out.get("a0");
        if not isinstance(a0,dict):fail("a0")
        status=a0.get("status")
        if status in ("UNKNOWN","UNKNOWN_RESOURCE"):
            if not isinstance(a0.get("reason"),str) or not a0["reason"]:fail("unknown_reason")
        elif status=="COMMON_CANDIDATE":
            if a0.get("strict_replay") is not False or a0.get("positive_discovery_only") is not True:fail("candidate_semantics")
        else: fail("terminal")
        for key in ("boundary_active","batch_added"):
            if key in a0 and (not isinstance(a0[key],int) or a0[key]<0):fail(key)
        if "batch_cap" in out and (not isinstance(out["batch_cap"],int) or out["batch_cap"]<1):fail("batch_cap")
        print("R07_A0_BATCH_LAZY_CHECKER_PASS status="+str(status));return 0
    except Exception as e:
        print("R07_A0_BATCH_LAZY_CHECKER_FAIL:"+str(e));return 1
if __name__=="__main__":raise SystemExit(main())
