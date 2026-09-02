#!/usr/bin/env python3
"""Independent envelope checker for the task525 lazy successor candidate."""
import argparse,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SCHEMA="d972-r07-a0-actual-tau-free-lazy-compact-seed/v4"
ROSTER_SHA="7612682d024b61f873928ad122c9a5d7462c812a6633112f08706cda4412b6c8"
def fail(s): raise RuntimeError(s)
def main(argv=None):
 ap=argparse.ArgumentParser();ap.add_argument("--producer");ap.add_argument("--fixture",action="store_true");a=ap.parse_args(argv)
 try:
  if a.fixture: print("R07_A0_ACTUAL_TAU_FREE_LAZY_COMPACT_SEED_V8_CHECKER_FIXTURE_PASS");return 0
  if not a.producer: fail("producer_required")
  x=json.loads(Path(a.producer).read_bytes())
  if x.get("schema")!=SCHEMA: fail("schema")
  p=x.get("presentation",{})
  if p.get("compact_relator_count")!=44 or p.get("relators_sha256")!=ROSTER_SHA: fail("roster")
  if x.get("complete") is not False: fail("complete_claim")
  c=x.get("claim_boundary",{})
  if any(c.get(k) is not False for k in ("A0","COMMON","NONMEMBER","fake","Ihara")): fail("claim_boundary")
  print("R07_A0_ACTUAL_TAU_FREE_LAZY_COMPACT_SEED_V8_CHECKER_PASS status="+str(x.get("status")));return 0
 except Exception as e: print("R07_A0_ACTUAL_TAU_FREE_LAZY_COMPACT_SEED_V8_CHECKER_FAIL:"+str(e));return 1
if __name__=="__main__": raise SystemExit(main())
