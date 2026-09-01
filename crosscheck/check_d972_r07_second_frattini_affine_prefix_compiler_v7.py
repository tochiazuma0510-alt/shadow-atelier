#!/usr/bin/env python3
"""Task500 independent provenance-boundary successor of frozen v6 body."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V6 = (
    "crosscheck/check_d972_r07_second_frattini_affine_prefix_compiler_v6.py",
    5428,
    "ce735eb1fafb743a53b17ef056b56f4cbd3bf1ff39969dabb5b708c4c43519fb",
)
GENERATED_BYTES = 13831
GENERATED_SHA256 = "4469ea689ca6dec1864fa842525cb680fa49463789a4dd6357406ff706776cb5"


def _sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _need(value: object, message: str) -> None:
    if not value:
        raise RuntimeError(message)


def _v6_generated() -> bytes:
    path = ROOT / V6[0]
    raw = path.read_bytes()
    _need(len(raw) == V6[1] and _sha(raw) == V6[2], "task500 v6 checker pin drift")
    saved = sys.argv
    sys.argv = [saved[0]]
    try:
        spec = importlib.util.spec_from_file_location("task500_v6_checker", path)
        _need(spec is not None and spec.loader is not None, "task500 v6 checker loader")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    finally:
        sys.argv = saved
    source = getattr(module, "_SOURCE", None)
    _need(isinstance(source, bytes), "task500 v6 checker generated source")
    _need(len(source) == 7831 and _sha(source) ==
          "b1e7b9047b839fcf5306cf32bb7876f4d55ef8e5f1eb0c48829a348811911ea3",
          "task500 v6 checker generated pin drift")
    return source


_PROVENANCE = b'''\
def _v7_provenance(c,v):
 inp=c.get("inputs")
 need(isinstance(inp,dict) and set(inp)=={"v5_result","v5_checkpoint","v5_checker_log","source_head","run_id","artifact_id"},"v7 inputs shape")
 art=inp.get("artifact_id")
 need(isinstance(art,str) and len(art)>0 and "1"<=art[0]<="9" and all("0"<=z<="9" for z in art),"v7 artifact_id")
 head="dd6d90b64e2bfba73d7f131f4da876235746f314";run="33553895281";bind="0e0123e99309a768910e150d5bf4725295a0dc35eab7e15eac66538a3a37d56b"
 need(inp.get("source_head")==head and inp.get("run_id")==run,"v7 input provenance")
 for k in ("v5_result","v5_checkpoint","v5_checker_log"):
  q=inp.get(k);need(isinstance(q,dict) and set(q)=={"path","bytes","sha256"} and isinstance(q["path"],str) and type(q["bytes"]) is int and q["bytes"]>0 and isinstance(q["sha256"],str) and len(q["sha256"])==64,"v7 physical identity")
 need(c.get("upstream")=={"schema":"d972-r07-a0-dual-anchored-rank99-durable-discovery/v5","binding":bind,"implementation_commit":head,"production_run_id":run,"production_artifact_id":art},"v7 upstream")
 need(v.get("inputs")==inp,"v7 verdict inputs")
 return True

'''

_FIXTURE = b'''\
def _v7_fixture():
 ident={"path":"ci/out/task500-toy.json","bytes":1,"sha256":"0"*64};pins={"producer":{"path":"search/d972_r07_a0_dual_anchored_rank99_durable_discovery_v5.py","bytes":104031,"sha256":"25c308ec11b9f36cc9779dfec46058a4956068969d664ee582a26f9cb0db7c09"},"checker":{"path":"crosscheck/check_d972_r07_a0_dual_anchored_rank99_durable_discovery_v5.py","bytes":71589,"sha256":"970ffe3a78687f3a27a222e089ae3d5e928bbfa048b9aef9f51fcf4c0b5d578d"},"driver":{"path":"search/d972_r07_a0_dual_anchored_rank99_durable_discovery_gha_driver_v5.g","bytes":9425,"sha256":"bed9105b36fef5e59120d954029ec507b16f393ab2859a7599867a19156b1b5d"},"frozen_rank51":{"path":"search/certs/d972_r07_a0_actual_tau_free_rank51_checkpoint_v1.json","bytes":10934,"sha256":"a83959e4c9fcfa79093c712e82164d47c31b78c9fc00b512f7adac9413c481f4"}};inp={"v5_result":ident,"v5_checkpoint":ident,"v5_checker_log":ident,"source_head":"dd6d90b64e2bfba73d7f131f4da876235746f314","run_id":"33553895281","artifact_id":"7331"};g=[1]*760;a=[2];f=g+a;d={"physical_row":[],"physical_row_sha256":hashlib.sha256(b"").hexdigest(),"replay":{"corrected_word":f},"direct_all_seven_replay":True,"eleven_occurrence_replay":True,"right_g760_multiplication":True,"joint_kernel":True,"hexagons":True,"pentagon_printed_order":True,"exact_exponent_pair":[0,0]};c=seal({"schema":"d972-r07-rank99-v5-task193-carrier/v1","status":"ACCEPTED","terminal":"R07_RANK99_V5_TASK193_CARRIER_V1_ACCEPTED","claims":{"carrier":True,"A2":False,"lift":False,"fake":False,"Ihara":False},"pins":pins,"inputs":inp,"upstream":{"schema":"d972-r07-a0-dual-anchored-rank99-durable-discovery/v5","binding":"0e0123e99309a768910e150d5bf4725295a0dc35eab7e15eac66538a3a37d56b","implementation_commit":"dd6d90b64e2bfba73d7f131f4da876235746f314","production_run_id":"33553895281","production_artifact_id":"7331"},"carrier":{"g760":g,"correction_word":a,"corrected_word":f,"direct_replay":d}});v=seal({"schema":"d972-r07-rank99-v5-task193-carrier/v1/checker","status":"PASS","terminal":"R07_RANK99_V5_TASK193_CARRIER_V1_CHECKER_PASS","carrier":ident,"inputs":dict(inp),"claims":{"literal_carrier_replayed":True,"A2":False,"lift":False,"fake":False,"Ihara":False}});_v7_provenance(c,v);boundary(c,v,ident);rejected=[]
 def attempt(label,fn):
  cc=json.loads(json.dumps(c));vv=json.loads(json.dumps(v));fn(cc,vv);cc.pop("self_digest",None);cc.update(seal(cc));vv.pop("self_digest",None);vv.update(seal(vv))
  try:boundary(cc,vv,ident)
  except (RuntimeError,TypeError,KeyError,AttributeError):rejected.append(label)
 for label,fn in [("missing_upstream",lambda x,y:x.pop("upstream")),("extra_upstream",lambda x,y:x["upstream"].update(extra=True)),("wrong_run",lambda x,y:x["inputs"].update(run_id="1")),("wrong_head",lambda x,y:x["inputs"].update(source_head="bad")),("artifact_0",lambda x,y:(x["inputs"].update(artifact_id="0"),x["upstream"].update(production_artifact_id="0"))), ("artifact_00",lambda x,y:(x["inputs"].update(artifact_id="00"),x["upstream"].update(production_artifact_id="00"))), ("artifact_01",lambda x,y:(x["inputs"].update(artifact_id="01"),x["upstream"].update(production_artifact_id="01"))), ("artifact_signed",lambda x,y:(x["inputs"].update(artifact_id="+1"),x["upstream"].update(production_artifact_id="+1"))), ("artifact_space",lambda x,y:(x["inputs"].update(artifact_id=" 1"),x["upstream"].update(production_artifact_id=" 1"))), ("artifact_unicode",lambda x,y:(x["inputs"].update(artifact_id=chr(0xff11)),x["upstream"].update(production_artifact_id=chr(0xff11)))), ("artifact_integer",lambda x,y:(x["inputs"].update(artifact_id=1),x["upstream"].update(production_artifact_id=1))), ("upstream_artifact_drift",lambda x,y:x["upstream"].update(production_artifact_id="7332")), ("verdict_artifact_drift",lambda x,y:y["inputs"].update(artifact_id="7332")), ("verdict_run_drift",lambda x,y:y["inputs"].update(run_id="1")), ("verdict_head_drift",lambda x,y:y["inputs"].update(source_head="bad")), ("verdict_result_drift",lambda x,y:y["inputs"].update(v5_result={"path":"x","bytes":1,"sha256":"1"*64})), ("verdict_checkpoint_drift",lambda x,y:y["inputs"].update(v5_checkpoint={"path":"x","bytes":1,"sha256":"1"*64})), ("verdict_log_drift",lambda x,y:y["inputs"].update(v5_checker_log={"path":"x","bytes":1,"sha256":"1"*64})), ("stale_v6",lambda x,y:x.update(schema="d972-r07-second-frattini-affine-prefix-compiler/v6")), ("binding_drift",lambda x,y:x["upstream"].update(binding="bad"))]:attempt(label,fn)
 need(len(rejected)==20,"v7 checker fixture mutation coverage");return {"status":"PASS","actual_common":False,"mutation_rejections":rejected,"dynamic_artifact":"7331"}

'''

_PATCHES = (
    (b'd972-r07-second-frattini-affine-prefix-compiler/v6', b'd972-r07-second-frattini-affine-prefix-compiler/v7', 1),
    (b'R07_SECOND_FRATTINI_AFFINE_PREFIX_COMPILER_V6', b'R07_SECOND_FRATTINI_AFFINE_PREFIX_COMPILER_V7', 2),
    (b'/checker-verdict/v6', b'/checker-verdict/v7', 2),
    (b'def boundary(c,v,ci):\n chk(c);chk(v);', _PROVENANCE + b'def boundary(c,v,ci):\n _v7_provenance(c,v);chk(c);chk(v);', 1),
    (b'def main(argv=None):\n', _FIXTURE + b'def main(argv=None):\n', 1),
    (b'if a.self_test:\n  need(synthetic_gate(),"synthetic gate");toy=verdict({}, {}, {}, {});', b'if a.self_test:\n  need(synthetic_gate(),"synthetic gate");need(_v7_fixture()["status"]=="PASS","v7 fixture");toy=verdict({}, {}, {}, {});', 1),
    (b'mutations=15 inner_key_transform=true', b'mutations=20 inner_key_transform=true', 1),
    (b'"v6 envelope")', b'"v6 envelope");sp=r.get("source_provenance",{});need(sp.get("carrier_provenance")=={"source_head":c["inputs"]["source_head"],"run_id":c["inputs"]["run_id"],"artifact_id":c["inputs"]["artifact_id"]},"v7 output provenance")', 1),
)


def _generate() -> tuple[bytes, list[dict[str, object]]]:
    raw = _v6_generated()
    report = []
    for old, new, expected in _PATCHES:
        before = raw.count(old)
        if before != expected or raw.count(new) != 0:
            raise RuntimeError("task500 checker patch cardinality drift")
        raw = raw.replace(old, new)
        if raw.count(old) != new.count(old) or raw.count(new) != expected:
            raise RuntimeError("task500 checker patch postcondition drift")
        report.append({"old_before": before, "old_after": raw.count(old), "new_after": raw.count(new)})
    return raw, report


_SOURCE, _REPORT = _generate()
if "--source-patch-info" in sys.argv[1:]:
    print(json.dumps({"owner": V6, "generated": {"bytes": len(_SOURCE), "sha256": _sha(_SOURCE)}, "patches": _REPORT}, sort_keys=True, separators=(",", ":")))
    raise SystemExit(0)
if GENERATED_BYTES and (len(_SOURCE) != GENERATED_BYTES or _sha(_SOURCE) != GENERATED_SHA256):
    raise RuntimeError("task500 v7 generated checker pin drift")
exec(compile(_SOURCE, str(ROOT / V6[0]), "exec"), globals(), globals())
