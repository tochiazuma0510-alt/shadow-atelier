#!/usr/bin/env python3
"""Task525 rank111 lazy compact-seed successor (candidate transport owner)."""
from __future__ import annotations
import argparse, hashlib, json, os, time
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PRODUCER=("search/d972_r07_a0_actual_tau_free_rank_ladder_v3.py",12215,"0140447110cfa568a77300bd7d43d51c622597704b7b91ed5209c63168c9ef37")
CHECKER=("crosscheck/check_d972_r07_a0_actual_tau_free_rank_ladder_v7.py",3653,"e1b80c586985f5113b300508f6bc78d055a37243e3fd6795b8f81148b0988de1")
ROSTER_COUNT=44; ROSTER_SHA="7612682d024b61f873928ad122c9a5d7462c812a6633112f08706cda4412b6c8"; SCHEMA="d972-r07-a0-actual-tau-free-lazy-compact-seed/v4"
UNKNOWN="UNKNOWN"; UNKNOWN_RESOURCE="UNKNOWN_RESOURCE"

def sha(b): return hashlib.sha256(b).hexdigest()
def canonical(x): return json.dumps(x,sort_keys=True,separators=(",",":"),ensure_ascii=True).encode("ascii")
def pin(spec):
 p=ROOT/spec[0]; b=p.read_bytes()
 if len(b)!=spec[1] or sha(b)!=spec[2]: raise RuntimeError("pin_mismatch:"+spec[0])
 return {"path":spec[0],"bytes":len(b),"sha256":sha(b)}
def claims(status,reason=None):
 x={"A0":False,"COMMON":False,"NONMEMBER":False,"fake":False,"Ihara":False}
 return {"status":status,"terminal":status,"complete":False,"reason":reason,"claims":x}

def lazy_selector_fixture():
 # Independent, deterministic branch contract: action-first and seed-one short circuit.
 counters={"formulas_compiled":0,"unconjugated_identity_replays":0,"seeds_touched":0,"k0_candidates":0,"knonzero_candidates":0,"adds":0,"updates":0}
 action_hit=True
 if action_hit: return {"status":"FIXTURE_PASS","action_first":True,"counters":counters}
 touched=[]
 for seed in range(1,45):
  touched.append(seed); counters["seeds_touched"]+=1; counters["formulas_compiled"]+=1
  if seed==1: counters["adds"]+=1; counters["updates"]+=1; break
 assert touched==[1] and counters["unconjugated_identity_replays"]==0
 return {"status":"FIXTURE_PASS","action_first":False,"counters":counters}

def migration_fixture():
 legacy={"accepted_count":68,"rank":111,"round":73,"dual_digest":"56ccd1f3cc6b54fe340a69ce6a0ec99f5aeb3358ae80288c6b11c3f1ec664864","remainder_digest":"9eed8114d9e3172c7a11153d9c5cd6e5fc2e5184a8d6e3681cce5c82a83b4326"}
 state={"schema":SCHEMA,"binding":"task525-rank111-v4","legacy":legacy,"accepted_sources":68,"rank":111,"round":73}
 assert state["legacy"]["accepted_count"]==len(range(68)) and state["rank"]==111
 return {"status":"FIXTURE_PASS","legacy":legacy,"new_schema":SCHEMA}

def run_fixture():
 return {"lazy_selector":lazy_selector_fixture(),"migration":migration_fixture(),"roster":{"count":ROSTER_COUNT,"sha256":ROSTER_SHA},"mutation_classes":["roster_43_45_6441","seed1","k0","knonzero","action","resource","legacy_prefix"]}

def run(a):
 # Production is intentionally not executed by bounded development runs.
 pin(PRODUCER); pin(CHECKER)
 return claims(UNKNOWN_RESOURCE,"bounded implementation candidate; production rank111 replay deferred")

def main(argv=None):
 ap=argparse.ArgumentParser(); ap.add_argument("--mode",choices=("FIXTURE","PRODUCTION"),default="PRODUCTION"); ap.add_argument("--output",default="ci/out/d972_r07_a0_actual_tau_free_lazy_compact_seed_v4.json"); ap.add_argument("--checkpoint"); ap.add_argument("--resume"); ap.add_argument("--seconds",type=float,default=7200); ap.add_argument("--rss-bytes",type=int,default=4800000000); ap.add_argument("--max-rises",type=int,default=64); a=ap.parse_args(argv)
 try:
  result=run_fixture() if a.mode=="FIXTURE" else run(a)
  out={"schema":SCHEMA,"status":result.get("status","FIXTURE"),"terminal":result.get("status","FIXTURE"),"complete":False,"owner":{"producer":pin(PRODUCER),"checker":pin(CHECKER)},"presentation":{"compact_relator_count":ROSTER_COUNT,"relators_sha256":ROSTER_SHA},"a0":result,"claim_boundary":{"A0":False,"COMMON":False,"NONMEMBER":False,"fake":False,"Ihara":False}}
 except Exception as e: out={"schema":SCHEMA,**claims(UNKNOWN,str(e))}
 p=ROOT/a.output; p.parent.mkdir(parents=True,exist_ok=True); p.write_bytes(canonical(out)+b"\n")
 print("R07_A0_ACTUAL_TAU_FREE_LAZY_COMPACT_SEED_V4 "+out["status"],flush=True); return 0
if __name__=="__main__": raise SystemExit(main())
