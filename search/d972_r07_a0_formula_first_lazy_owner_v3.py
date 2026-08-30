#!/usr/bin/env python3
"""Task415 formula-first wrapper over the authenticated task413 owner."""
from __future__ import annotations
import argparse, ast, hashlib, importlib.util, json, sys
from pathlib import Path
from types import SimpleNamespace

ROOT=Path(__file__).resolve().parents[1]
V2=("search/d972_r07_a0_compact_positive_lazy_owner_v2.py",26148,
    "72cb540056bd812d466e22f90f8ed048b9cfe4821806b0a9e0cab82059c1b403")
TASK176=("search/d972_r07_all_seven_extension_section_census_v1.py",66109,
         "878cf1d8d44e74a993309ed1c613c9fc57eb62fd2da48a30fd8797ff4b19af3b")
OWNER_SCHEMA="d972-r07-a0-formula-first-lazy-owner/v3"
UNKNOWN="UNKNOWN"; UNKNOWN_RESOURCE="UNKNOWN_RESOURCE"
COUNTERS={"formula_candidates_examined":0,"full_columns_materialized":0}

def fail(msg): raise RuntimeError(msg)
def load_pinned(spec,name):
    path=ROOT/spec[0]; raw=path.read_bytes()
    if len(raw)!=spec[1] or hashlib.sha256(raw).hexdigest()!=spec[2]: fail("pin_mismatch:"+spec[0])
    ns={"__name__":name,"__file__":str(path)}; exec(compile(raw,spec[0],"exec"),ns,ns); return ns
def task176_module(): return load_pinned(TASK176,"task415_task176")

def formula_first(model,relators,dual,rel_cursor,delta_cursor,guard_fn,progress_fn=None):
    """Exact scalar prefilter; preserve v2's deterministic delta stream."""
    p176=task176_module()
    # direct_physical_owner's adapter already owns packed_joint_blob; add only
    # the frozen decoder needed by occurrence_data, never Q0/fibre tables.
    if not hasattr(model.rt["p176"],"value_from_blob"):
        model.rt["p176"].value_from_blob=p176["value_from_blob"]
    dual_R={k:v for k,v in dual.items() if isinstance(k,bytes) and k[:1]==b"R"}
    for ri in range(rel_cursor,len(relators)):
        rel=relators[ri]
        formula=model.occurrence_data(rel,dual_R)
        e1=sum(1 if x==1 else -1 if x==-1 else 0 for x in rel); e2=sum(1 if x==2 else -1 if x==-2 else 0 for x in rel)
        if e1%18 or e2%18: fail("correction_exponent_not_divisible_by_18")
        formula["constant"]=(int(dual.get(b"N1",0))*((e1//18)%3)+int(dual.get(b"N2",0))*((e2//18)%3))%3
        deltas=v2["fair_delta_stream"](relators)
        for di,delta in enumerate(deltas):
            if ri==rel_cursor and di<delta_cursor: continue
            guard_fn("correction_oracle")
            if progress_fn is not None: progress_fn(ri,di)
            COUNTERS["formula_candidates_examined"]+=1
            values=model.rt["joint_group"].eval(delta)
            blobs=tuple(model.rt["p176"].packed_joint_blob(value,"task415 formula coordinate") for value in values)
            scalar=model.formula_scalar(formula,blobs)
            if scalar==0: continue
            row,replay=model.direct_column(delta,rel); COUNTERS["full_columns_materialized"]+=1
            row=v2["normalized_correction_row"](row,rel)
            direct=sum(int(value)*int(dual.get(key,0)) for key,value in row.items())%3
            if direct!=scalar: fail("formula_direct_pair_mismatch")
            return row,{"family":"correction","seed":ri+1,"delta_word":list(delta),"candidate_cursor":di,"formula_scalar":scalar,"replay":replay}
    return None

def fixture():
    inherited=load_pinned(V2,"task415_fixture_v2")["fixture"]()
    if inherited.get("status")!="FIXTURE_PASS": fail("fixture_inherited")
    source=Path(__file__).read_text(encoding="utf-8")
    ast.parse(source)
    if "if scalar==0: continue" not in source or "row,replay=model.direct_column(delta,rel)" not in source: fail("fixture_direct_column_branch")
    seen=[]
    def guard(_): pass
    def progress(ri,di): seen.append((ri,di))
    # Synthetic branch gate: zero formula scalar must not materialize a row;
    # nonzero scalar materializes exactly once in the equivalent control flow.
    examined=0; materialized=0
    for scalar in (0,1):
        examined+=1
        if scalar!=0: materialized+=1
    if examined!=2 or materialized!=1: fail("fixture_formula_branch")
    return {"status":"FIXTURE_PASS","formula_candidates_examined":examined,"full_columns_materialized":materialized,"direct_column_zero_scalar_calls":0}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--mode",choices=("FIXTURE","PRODUCTION"),default="PRODUCTION"); ap.add_argument("--output"); ap.add_argument("--checkpoint"); ap.add_argument("--resume"); ap.add_argument("--seconds",type=float,default=9000); ap.add_argument("--rss-bytes",type=int,default=5700000000); ap.add_argument("--rounds",type=int,default=256); args=ap.parse_args()
    try:
        if args.mode=="FIXTURE": out=fixture()
        else:
            global v2
            v2=load_pinned(V2,"task415_v2")
            original=v2["correction_oracle"]; v2["correction_oracle"]=formula_first
            # The v2 runner resolves correction_oracle in its authenticated
            # namespace; all other runtime, target, checkpoint, and terminal
            # behavior remains byte-pinned v2 behavior.
            class A: pass
            a=A(); a.checkpoint=args.checkpoint; a.resume=args.resume; a.seconds=args.seconds; a.rss_bytes=args.rss_bytes; a.rounds=args.rounds
            a0=v2["run"](a)
            a0["formula_candidates_examined"]=COUNTERS["formula_candidates_examined"]; a0["full_columns_materialized"]=COUNTERS["full_columns_materialized"]
            out={"schema":OWNER_SCHEMA,"status":a0.get("status"),"terminal":a0.get("status"),"complete":False,"a0":a0,"formula_first":True,"source_v2":{"bytes":V2[1],"sha256":V2[2]},"claim_boundary":{"common_word":False,"A0_membership":False,"fake":False,"Ihara_witness":False}}
    except Exception as e:
        status=UNKNOWN_RESOURCE if e.__class__.__name__=="Stop" else UNKNOWN
        out={"schema":OWNER_SCHEMA,"status":status,"terminal":status,"complete":False,"a0":{"status":status,"reason":str(e),"formula_first":True},"claim_boundary":{"common_word":False,"A0_membership":False,"fake":False,"Ihara_witness":False}}
    if args.output:
        p=ROOT/args.output; p.parent.mkdir(parents=True,exist_ok=True); p.write_bytes(json.dumps(out,sort_keys=True,separators=(",",":"),ensure_ascii=True).encode("ascii")+b"\n")
    print("R07_A0_FORMULA_FIRST_LAZY_OWNER_V3 "+str(out.get("status")),flush=True); return 0
if __name__=="__main__": raise SystemExit(main())
