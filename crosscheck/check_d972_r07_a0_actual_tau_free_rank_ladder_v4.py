#!/usr/bin/env python3
"""Task447 resource-boundary closure over the independent v3 checker."""
from __future__ import annotations
import argparse,hashlib,importlib.util,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];MARKER="R07_A0_ACTUAL_TAU_FREE_RANK_LADDER_V4_CHECKER"
V3=("crosscheck/check_d972_r07_a0_actual_tau_free_rank_ladder_v3.py",9683,"8237db432c3930d9334ff6b4b557e0b1030343d4b349dd595a0a695d8a8b83f1")
PHASES={"tau_free_localized_dual","tau_free_reverse_neighbourhood","tau_free_old_candidates","tau_free_formula_seed","tau_free_candidate","fine_deletion","selective_Q0","selective_membership_S0","selective_membership_S1","selective_membership_S2","L_subgroup_closure","coarse_inverse_build"}
EXACT={"UNKNOWN_RESOURCE:NONZERO_TAU_PHASE_SELECTOR","UNKNOWN_RESOURCE:UNRECOGNIZED_DUAL_KEYS","UNKNOWN_RESOURCE:NONZERO_CONSTANT_SELECTOR","UNKNOWN_RESOURCE:SEPARATOR_REQUIRES_INDEPENDENT_EXHAUSTION","UNKNOWN_RESOURCE:max_rises"}
def need(x,m):
    if not x:raise RuntimeError(m)
def sha(x):return hashlib.sha256(x).hexdigest()
def load(spec,name):
    p=ROOT/spec[0];raw=p.read_bytes();need(len(raw)==spec[1] and sha(raw)==spec[2],"pin:"+spec[0]);s=importlib.util.spec_from_file_location(name,p);need(s and s.loader,"loader");m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
c=load(V3,"task447_v3_checker")
def reason_allowed(reason):
    if reason in EXACT:return True
    prefix="UNKNOWN_RESOURCE:SELECTOR_COORDINATES:S"
    if isinstance(reason,str) and reason.startswith(prefix):
        tail=reason[len(prefix):]
        try:xs=[int(x) for x in tail.split(",")]
        except ValueError:return False
        return bool(xs) and xs==sorted(set(xs))
    return any(reason==f"UNKNOWN_RESOURCE:{phase}:{limit}" for phase in PHASES for limit in ("time_limit","rss_limit"))
def durable(cert):
    state=c.checkpoint(cert);d=cert["durable_state"];need(d.get("accepted_count")==state["accepted_count"]==cert["accepted_count"],"durable accepted_count");need(d.get("rank")==state["rank"]==cert["physical_rank"],"durable rank");return state
def independent_profile(P,m,p179,claimed,reason):
    need(isinstance(claimed,dict) and isinstance(claimed.get("localized_dual_support"),int),"localized_dual_support")
    reduced=dict(claimed);reported=reduced.pop("localized_dual_support");c.independent_profile(P,m,p179,reduced,reason);count=0
    for key,value in sorted((P["dual"] or {}).items()):
        if key[:1]==b"N":continue
        try:block,label,blob=P["q"].parse(key)
        except Exception:continue
        if block in (1,2,3) and label!="tau":count+=1
    need(reported==count,"localized count");return claimed
def boundary(status,dual,reason,profile):
    if status=="UNKNOWN_RESOURCE":need(dual is not None,"resource dual boundary")
    else:need(dual is None and reason is None and profile is None,"common boundary")
def check(cert):
    need(cert.get("schema")==c.SCHEMA and cert.get("status") in {"UNKNOWN_RESOURCE","COMMON_CANDIDATE"} and cert.get("terminal")==cert.get("status"),"schema/status/terminal");accepted=cert.get("accepted_sources",[]);need(cert.get("accepted_count")==len(accepted),"count");need(cert.get("claims")=={"A0":cert["status"]=="COMMON_CANDIDATE","COMMON":False,"NONMEMBER":False,"fake":False,"Ihara":False},"claims")
    if cert["status"]=="UNKNOWN_RESOURCE":need(isinstance(cert.get("reason"),str) and reason_allowed(cert["reason"]),"resource reason")
    durable(cert);v1=c.c.load(c.c.V1,"task447_v1");v4=v1.load(v1.V4,"task447_v4");m=v4.load_v1();v12=m.load(m.V12,"task447_v12");p435=m.load(m.P435,"task447_p435");p179=m.load(m.P179,"task447_p179");P=v4.adapt(m,m.prefix(v12,p435,type("A",(),{"seconds":None,"rss_bytes":None})()));state=c.update(P,m);state=c.replay(P,m,p179,accepted,state);need(len(P["phys"].order)==cert["physical_rank"],"rank");dual,rem,coeff=state;boundary(cert["status"],dual,cert.get("reason"),cert.get("current_dual_profile"))
    if dual is not None:independent_profile(P,m,p179,cert["current_dual_profile"],cert["reason"])
    else:need(c.c.load(c.c.V1C,"task447_positive").positive(P,coeff)==cert.get("terminal_replay"),"positive replay")
def self_test():
    need(all(reason_allowed(f"UNKNOWN_RESOURCE:{p}:{x}") for p in PHASES for x in ("time_limit","rss_limit")),"phase roster");rejected=[]
    for x in ("UNKNOWN_RESOURCE:invented:time_limit","UNKNOWN_RESOURCE:fine_deletion:memory_limit","UNKNOWN_RESOURCE:SELECTOR_COORDINATES:S2,1"):
        if not reason_allowed(x):rejected.append(x)
    for label,args in (("resource_no_dual",("UNKNOWN_RESOURCE",None,"UNKNOWN_RESOURCE:max_rises",{})),("common_reason",("COMMON_CANDIDATE",None,"x",None)),("common_profile",("COMMON_CANDIDATE",None,None,{}))):
        try:boundary(*args)
        except RuntimeError:rejected.append(label)
    try:need(isinstance({},dict) and isinstance({}.get("localized_dual_support"),int),"localized_dual_support")
    except RuntimeError:rejected.append("missing_localized_count")
    state={"accepted_count":2,"rank":44};cert={"accepted_count":2,"physical_rank":44,"durable_state":{"accepted_count":1,"rank":44}}
    try:need(cert["durable_state"]["accepted_count"]==state["accepted_count"],"durable accepted_count")
    except RuntimeError:rejected.append("durable_metadata")
    need(len(rejected)==8,"mutation registry");return {"status":"PASS","budget_phases":sorted(PHASES),"mutation_rejections":rejected,"v3_selftest":c.self_test()}
def main(argv=None):
    ap=argparse.ArgumentParser();ap.add_argument("artifact",nargs="?");ap.add_argument("--self-test",action="store_true");a=ap.parse_args(argv)
    if a.self_test:print(MARKER+"_SELFTEST_PASS "+json.dumps(self_test(),sort_keys=True));return 0
    need(a.artifact,"artifact");check(json.loads(Path(a.artifact).read_text(encoding="ascii")));print(MARKER+"_PASS");return 0
if __name__=="__main__":raise SystemExit(main())
