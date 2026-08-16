#!/usr/bin/env python3
"""Independent checker for the typed five-coface N3 harness."""
from __future__ import annotations
import argparse,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DEFAULT_ARTIFACT=ROOT/"ci"/"out"/"d972_b4_marity_phaseb1_n3_v2.json"
def validate(o,source="artifact"):
    if not isinstance(o,dict) or o.get("schema")!="d972-b4-marity-phaseb1-n3/v2": raise AssertionError(f"{source}: schema")
    if o.get("status")!="N3_TYPED_CANONICAL_REPLAY" or o.get("source_group")!="PB3" or o.get("target_group")!="PB3/M": raise AssertionError(f"{source}: domain")
    p=o.get("pb3",{});
    if p.get("generator_labels")!=["x12","x13","x23"] or not isinstance(p.get("relator_count"),int) or p["relator_count"]<1 or p.get("index_in_B3")!=6 or p.get("center_replay") is not True: raise AssertionError(f"{source}: PB3")
    if o.get("target_marking")!=["X","X^-1Y^-1","Y"]: raise AssertionError(f"{source}: target marking")
    c=o.get("cofaces",{});
    if c.get("paper_order")!=["x12","x23","x13"] or c.get("canonical_order")!=["x12","x13","x23"] or c.get("count")!=5 or c.get("all_relators_replayed") is not True: raise AssertionError(f"{source}: cofaces")
    paper=[["x12","x23","x13"],["x23","x34","x24"],["x13*x23","x34","x14*x24"],["x12*x13","x24*x34","x14"],["x12","x23*x24","x13*x14"]]
    canon=[["x12","x13","x23"],["x23","x24","x34"],["x13*x23","x14*x24","x34"],["x12*x13","x14","x24*x34"],["x12","x13*x14","x23*x24"]]
    if c.get("paper_triples")!=paper or c.get("canonical_triples")!=canon: raise AssertionError(f"{source}: triple order/losslessness")
    if not isinstance(o.get("cm_quotient_order"),int) or o["cm_quotient_order"]<1: raise AssertionError(f"{source}: CM")
    n=o.get("N3",{});
    if not all(isinstance(n.get(k),int) and n[k]>=1 for k in ("quotient_order","F2_image_order","M_over_N3_order")) or n.get("N3_le_M") is not True: raise AssertionError(f"{source}: N3")
    if not isinstance(o.get("composites"),list) or len(o["composites"])!=5 or any(not isinstance(x,list) or len(x)!=4 for x in o["composites"]): raise AssertionError(f"{source}: 20 composites")
    if o.get("gentle_fiber_gate")!={"status":"BLOCKED_NOT_IMPLEMENTED","expected_targets":972,"enumerated":False}: raise AssertionError(f"{source}: fiber gate")
    if o.get("typing_boundary")!={"M_B4_stable":False,"GT_descent":"UNPROVED"}: raise AssertionError(f"{source}: boundary")
def selftest():
    paper=[["x12","x23","x13"],["x23","x34","x24"],["x13*x23","x34","x14*x24"],["x12*x13","x24*x34","x14"],["x12","x23*x24","x13*x14"]]; canon=[["x12","x13","x23"],["x23","x24","x34"],["x13*x23","x14*x24","x34"],["x12*x13","x14","x24*x34"],["x12","x13*x14","x23*x24"]]
    f={"schema":"d972-b4-marity-phaseb1-n3/v2","status":"N3_TYPED_CANONICAL_REPLAY","source_group":"PB3","target_group":"PB3/M","pb3":{"generator_labels":["x12","x13","x23"],"relator_count":1,"index_in_B3":6,"center_replay":True},"target_marking":["X","X^-1Y^-1","Y"],"cm_quotient_order":1,"cofaces":{"paper_order":["x12","x23","x13"],"canonical_order":["x12","x13","x23"],"count":5,"all_relators_replayed":True,"paper_triples":paper,"canonical_triples":canon},"composites":[[[],[],[],[]]]*5,"N3":{"quotient_order":1,"F2_image_order":1,"M_over_N3_order":1,"N3_le_M":True},"gentle_fiber_gate":{"status":"BLOCKED_NOT_IMPLEMENTED","expected_targets":972,"enumerated":False},"typing_boundary":{"M_B4_stable":False,"GT_descent":"UNPROVED"}}
    validate(f,"selftest"); print("D972_B4_MARITY_PHASEB1_N3_V2_SELFTEST_PASS")
def main():
    ap=argparse.ArgumentParser();ap.add_argument("--selftest",action="store_true");ap.add_argument("--check",type=Path,default=DEFAULT_ARTIFACT);a=ap.parse_args()
    if a.selftest:selftest()
    else:validate(json.loads(a.check.read_text(encoding="utf-8")),str(a.check));print("D972_B4_MARITY_PHASEB1_N3_V2_CHECK_PASS",a.check)
if __name__=="__main__":main()
