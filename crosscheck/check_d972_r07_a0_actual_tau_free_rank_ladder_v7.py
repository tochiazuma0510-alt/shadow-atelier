#!/usr/bin/env python3
"""Task461 independent rank-68 continuation transport checker."""
from __future__ import annotations
import argparse,hashlib,importlib.util,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];MARKER="R07_A0_ACTUAL_TAU_FREE_RANK_LADDER_V7_CHECKER"
V6=("crosscheck/check_d972_r07_a0_actual_tau_free_rank_ladder_v6.py",3590,"e902468fca7ead498e78c06496ccea596c10a1904e571f5d6b709962458b1739")
FROZEN=("search/certs/d972_r07_a0_actual_tau_free_rank68_checkpoint_v1.json",33015,"73ad85624d079d01ecc824ab6adc699c51b0dabfddcc36c0f7d2bd4384f7d5a4")
STATE_SHA="d900bbb4f3b69ee66f9c2f4000b169f69a9202091a69fe0bbb8d33c4ae061537";REASON="UNKNOWN_RESOURCE:tau_free_formula_seed:time_limit"
def need(x,m):
    if not x:raise RuntimeError(m)
def sha(x):return hashlib.sha256(x).hexdigest()
def canonical(x):return json.dumps(x,sort_keys=True,separators=(",",":" )).encode("ascii")
def raw(spec):
    p=ROOT/spec[0];x=p.read_bytes();need(len(x)==spec[1] and sha(x)==spec[2],"pin:"+spec[0]);return x
def load(spec,name):
    p=ROOT/spec[0];x=raw(spec);s=importlib.util.spec_from_file_location(name,p);need(s and s.loader,"loader");m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
c=load(V6,"task461_v6_checker")
def frozen_state():
    s=json.loads(raw(FROZEN));need(s.get("schema")==c.c.c.c.CP_SCHEMA and s.get("binding")==c.c.c.c.BINDING,"frozen schema/binding");h=s.get("state_sha256");body=dict(s);body.pop("state_sha256",None);need(h==STATE_SHA==sha(canonical(body)),"frozen internal seal");need(s.get("rank")==68 and s.get("accepted_count")==25 and s.get("round")==27 and s.get("reason")==REASON and len(s.get("accepted_sources",[]))==25,"frozen fields");[c.c.c.c.validate(x) for x in s["accepted_sources"]];return s
def continuation(cert,base):
    accepted=cert.get("accepted_sources");need(isinstance(accepted,list) and accepted[:25]==base["accepted_sources"],"rank68 exact prefix");need(cert.get("accepted_count")==len(accepted) and cert["accepted_count"]>=25,"monotone count");need(isinstance(cert.get("physical_rank"),int) and cert["physical_rank"]>=68,"monotone rank");need(isinstance(cert.get("round"),int) and cert["round"]>=27,"monotone round")
def check(cert):
    base=frozen_state();continuation(cert,base);c.check(cert)
def self_test():
    base=frozen_state();cert={"accepted_sources":list(base["accepted_sources"]),"accepted_count":25,"physical_rank":68,"round":27};continuation(cert,base);rejected=[]
    z=dict(base);z["state_sha256"]="0"*64
    try:
        body=dict(z);h=body.pop("state_sha256");need(h==STATE_SHA==sha(canonical(body)),"seal")
    except RuntimeError:rejected.append("checkpoint_seal")
    for label,change in (("altered_prefix",{"accepted_sources":[{}]+cert["accepted_sources"][1:]}),("decreasing_rank",{"physical_rank":67}),("decreasing_count",{"accepted_count":24,"accepted_sources":cert["accepted_sources"][:24]}),("decreasing_round",{"round":26})):
        q=dict(cert);q.update(change)
        try:continuation(q,base)
        except RuntimeError:rejected.append(label)
    need(len(rejected)==5,"mutations");return {"status":"PASS","frozen_rank":68,"frozen_count":25,"frozen_round":27,"mutation_rejections":rejected}
def main(argv=None):
    ap=argparse.ArgumentParser();ap.add_argument("artifact",nargs="?");ap.add_argument("--self-test",action="store_true");a=ap.parse_args(argv)
    if a.self_test:print(MARKER+"_SELFTEST_PASS "+json.dumps(self_test(),sort_keys=True));return 0
    need(a.artifact,"artifact");check(json.loads(Path(a.artifact).read_text(encoding="ascii")));print(MARKER+"_PASS");return 0
if __name__=="__main__":raise SystemExit(main())
