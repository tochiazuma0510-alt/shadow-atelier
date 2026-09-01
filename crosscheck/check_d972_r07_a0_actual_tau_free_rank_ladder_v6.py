#!/usr/bin/env python3
"""Task450 independent rank-51 continuation transport checker."""
from __future__ import annotations
import argparse,hashlib,importlib.util,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];MARKER="R07_A0_ACTUAL_TAU_FREE_RANK_LADDER_V6_CHECKER"
V5=("crosscheck/check_d972_r07_a0_actual_tau_free_rank_ladder_v5.py",2859,"e783028862bbae84acf769ec64de9693dfae1c4c99e9444e8e92af76e08a2da0")
FROZEN=("search/certs/d972_r07_a0_actual_tau_free_rank51_checkpoint_v1.json",10934,"a83959e4c9fcfa79093c712e82164d47c31b78c9fc00b512f7adac9413c481f4")
STATE_SHA="22dcfdfb396524ea5853488aa2ad52d28b4f7d10164123bc83f121e59dd83159"
def need(x,m):
    if not x:raise RuntimeError(m)
def sha(x):return hashlib.sha256(x).hexdigest()
def canonical(x):return json.dumps(x,sort_keys=True,separators=(",",":" )).encode("ascii")
def raw(spec):
    p=ROOT/spec[0];x=p.read_bytes();need(len(x)==spec[1] and sha(x)==spec[2],"pin:"+spec[0]);return x
def load(spec,name):
    p=ROOT/spec[0];x=raw(spec);s=importlib.util.spec_from_file_location(name,p);need(s and s.loader,"loader");m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
c=load(V5,"task450_v5_checker")
def frozen_state():
    s=json.loads(raw(FROZEN));need(s.get("schema")==c.c.c.CP_SCHEMA and s.get("binding")==c.c.c.BINDING,"frozen schema/binding");h=s.get("state_sha256");body=dict(s);body.pop("state_sha256",None);need(h==STATE_SHA==sha(canonical(body)),"frozen internal seal");need(s.get("rank")==51 and s.get("accepted_count")==8 and s.get("round")==9 and len(s.get("accepted_sources",[]))==8,"frozen fields");[c.c.c.validate(x) for x in s["accepted_sources"]];return s
def continuation(cert,base):
    accepted=cert.get("accepted_sources");need(isinstance(accepted,list) and accepted[:8]==base["accepted_sources"],"rank51 exact prefix");need(cert.get("accepted_count")==len(accepted) and cert["accepted_count"]>=base["accepted_count"],"monotone count");need(isinstance(cert.get("physical_rank"),int) and cert["physical_rank"]>=base["rank"],"monotone rank");need(isinstance(cert.get("round"),int) and cert["round"]>=base["round"],"monotone round")
def check(cert):
    base=frozen_state();continuation(cert,base);c.check(cert)
def self_test():
    base=frozen_state();cert={"accepted_sources":list(base["accepted_sources"]),"accepted_count":8,"physical_rank":51,"round":9};continuation(cert,base);rejected=[]
    z=dict(base);z["state_sha256"]="0"*64
    try:
        body=dict(z);h=body.pop("state_sha256");need(h==STATE_SHA==sha(canonical(body)),"seal")
    except RuntimeError:rejected.append("checkpoint_seal")
    for label,change in (("altered_prefix",{"accepted_sources":[{}]+cert["accepted_sources"][1:]}),("decreasing_rank",{"physical_rank":50}),("decreasing_count",{"accepted_count":7,"accepted_sources":cert["accepted_sources"][:7]}),("decreasing_round",{"round":8})):
        q=dict(cert);q.update(change)
        try:continuation(q,base)
        except RuntimeError:rejected.append(label)
    need(len(rejected)==5,"mutations");return {"status":"PASS","frozen_rank":51,"frozen_count":8,"frozen_round":9,"mutation_rejections":rejected}
def main(argv=None):
    ap=argparse.ArgumentParser();ap.add_argument("artifact",nargs="?");ap.add_argument("--self-test",action="store_true");a=ap.parse_args(argv)
    if a.self_test:print(MARKER+"_SELFTEST_PASS "+json.dumps(self_test(),sort_keys=True));return 0
    need(a.artifact,"artifact");check(json.loads(Path(a.artifact).read_text(encoding="ascii")));print(MARKER+"_PASS");return 0
if __name__=="__main__":raise SystemExit(main())
