#!/usr/bin/env python3
"""Independent checker for canonical PB3/M Phase-A v3 artifacts."""
from __future__ import annotations
import argparse, copy, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ARTIFACT = ROOT / "ci" / "out" / "d972_b4_marity_m_export_v3.json"

def _perm(x, d):
    return isinstance(x, list) and sorted(x) == list(range(1, d + 1))

def validate(o, source="artifact"):
    if not isinstance(o, dict) or o.get("schema") != "d972-b4-marity-m-export/v3": raise AssertionError(f"{source}: schema")
    if o.get("status") != "PB3_CANONICAL_CENTER_CHECKED" or o.get("source_group") != "PB3" or o.get("target_group") != "PB3/M": raise AssertionError(f"{source}: domain")
    p=o.get("presentation")
    if p != {"name":"PB3_kernel_of_B3_to_S3","generator_labels":["x12","x13","x23"],"relator_count":p.get("relator_count") if isinstance(p,dict) else None,"relator_replay":True,"index_in_B3":6,"kernel_index":6,"kernel_marking":True}: raise AssertionError(f"{source}: presentation")
    if not isinstance(p.get("relator_count"), int) or p["relator_count"] < 1: raise AssertionError(f"{source}: relator count")
    c=o.get("center")
    if c != {"source_word":"x12*x13*x23","ambient_word":"(s1*s2)^3","replay":True,"target_replay":True}: raise AssertionError(f"{source}: center gate")
    comps=o.get("components")
    for n,d,order in (("K^(9)",27,2916),("N_S4",9,504)):
        x=comps.get(n) if isinstance(comps,dict) else None
        if not isinstance(x,dict) or x.get("degree")!=d or x.get("order")!=order or x.get("onto") is not True or len(x.get("generator_images",[]))!=3 or any(not _perm(v,d) for v in x["generator_images"]): raise AssertionError(f"{source}: component {n}")
    m=o.get("combined")
    if not isinstance(m,dict) or m.get("name")!="M" or m.get("degree")!=36 or m.get("order")!=1469664 or m.get("onto") is not True or m.get("generator_names")!=["XM","X13M","YM"] or len(m.get("generator_images",[]))!=3 or any(not _perm(v,36) for v in m["generator_images"]): raise AssertionError(f"{source}: M")
    d=o.get("diagonal_kernel_identity")
    if d != {"status":"CHECKED_BY_COMMON_PB3_SOURCE","component_relator_replay":True,"diagonal_relator_replay":True,"kernel_identity":True}: raise AssertionError(f"{source}: diagonal identity")
    if o.get("typing_boundary") != {"M_normal_in":"PB3","M_B4_stable":False,"four_face_GT_descent":"UNPROVED"}: raise AssertionError(f"{source}: boundary")

def _fixture():
    i27=list(range(1,28)); i9=list(range(1,10)); i36=list(range(1,37))
    return {"schema":"d972-b4-marity-m-export/v3","status":"PB3_CANONICAL_CENTER_CHECKED","source_group":"PB3","target_group":"PB3/M",
      "presentation":{"name":"PB3_kernel_of_B3_to_S3","generator_labels":["x12","x13","x23"],"relator_count":1,"relator_replay":True,"index_in_B3":6,"kernel_index":6,"kernel_marking":True},
      "center":{"source_word":"x12*x13*x23","ambient_word":"(s1*s2)^3","replay":True,"target_replay":True},
      "components":{"K^(9)":{"degree":27,"order":2916,"onto":True,"generator_images":[i27[:],i27[:],i27[:]]},"N_S4":{"degree":9,"order":504,"onto":True,"generator_images":[i9[:],i9[:],i9[:]]}},
      "combined":{"name":"M","definition":"K^(9) intersect N_S4","degree":36,"order":1469664,"onto":True,"generator_names":["XM","X13M","YM"],"generator_images":[i36[:],i36[:],i36[:]]},
      "diagonal_kernel_identity":{"status":"CHECKED_BY_COMMON_PB3_SOURCE","component_relator_replay":True,"diagonal_relator_replay":True,"kernel_identity":True},
      "typing_boundary":{"M_normal_in":"PB3","M_B4_stable":False,"four_face_GT_descent":"UNPROVED"}}

def selftest():
    f=_fixture(); validate(f,"selftest")
    bad=copy.deepcopy(f); bad["combined"]["generator_names"]=["XM","YM^-1*XM^-1","YM"]
    try: validate(bad,"marking mutation")
    except AssertionError: pass
    else: raise AssertionError("wrong A13 marking accepted")
    bad=copy.deepcopy(f); bad["center"]["target_replay"]=False
    try: validate(bad,"center mutation")
    except AssertionError: pass
    else: raise AssertionError("center mutation accepted")
    print("D972_B4_MARITY_M_EXPORT_V3_SELFTEST_PASS")

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--selftest",action="store_true"); ap.add_argument("--check",type=Path,default=DEFAULT_ARTIFACT); a=ap.parse_args()
    if a.selftest: selftest()
    else: validate(json.loads(a.check.read_text(encoding="utf-8")),str(a.check)); print("D972_B4_MARITY_M_EXPORT_V3_CHECK_PASS",a.check)

if __name__ == "__main__": main()
