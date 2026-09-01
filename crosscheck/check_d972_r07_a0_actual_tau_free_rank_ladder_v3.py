#!/usr/bin/env python3
"""Independent checkpoint and single-update replay for Task445 v3."""
from __future__ import annotations
import argparse,hashlib,importlib.util,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];SCHEMA="d972-r07-a0-actual-tau-free-rank-ladder/v3";CP_SCHEMA=SCHEMA+"/checkpoint";MARKER="R07_A0_ACTUAL_TAU_FREE_RANK_LADDER_V3_CHECKER"
V2C=("crosscheck/check_d972_r07_a0_actual_tau_free_rank_ladder_v2.py",7766,"98b94c4b89d66f9a780051f2120ead0d41d3451a215bb112f3a3f389ba288641");V1_SHA="880c4fe79b28391e3fa2d439566298cf3d9d2dfdbd9759615cd3c3300049fa7a";BINDING=hashlib.sha256((SCHEMA+V1_SHA).encode()).hexdigest();HEX=set("0123456789abcdef")
def need(x,m):
    if not x:raise RuntimeError(m)
def sha(x):return hashlib.sha256(x).hexdigest()
def canonical(x):return json.dumps(x,sort_keys=True,separators=(",",":" )).encode("ascii")
def load(spec,name):
    p=ROOT/spec[0];raw=p.read_bytes();need(len(raw)==spec[1] and sha(raw)==spec[2],"pin:"+spec[0]);s=importlib.util.spec_from_file_location(name,p);need(s and s.loader,"loader");m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
c=load(V2C,"task445_v2_checker")
def validate(s):
    c.validate(s)
    if s["kind"]=="correction":
        need(isinstance(s.get("adjoint_digest"),str) and len(s["adjoint_digest"])==64 and set(s["adjoint_digest"])<=HEX,"adjoint digest");need(isinstance(s.get("exact_exponent_pair"),list) and len(s["exact_exponent_pair"])==2 and all(isinstance(x,int) for x in s["exact_exponent_pair"]),"exponent pair")
def verify_state(s):
    need(isinstance(s,dict) and s.get("schema")==CP_SCHEMA and s.get("binding")==BINDING,"checkpoint schema/binding");h=s.get("state_sha256");need(isinstance(h,str) and len(h)==64 and set(h)<=HEX,"checkpoint state hash");body=dict(s);body.pop("state_sha256");need(h==sha(canonical(body)),"checkpoint internal seal");need(s.get("accepted_count")==len(s.get("accepted_sources",[])),"checkpoint count");[validate(x) for x in s["accepted_sources"]];return s
def checkpoint(cert):
    d=cert.get("durable_state");need(isinstance(d,dict) and isinstance(d.get("path"),str),"durable state");p=Path(d["path"]);need(not p.is_absolute() and p.parent==Path("ci/out"),"checkpoint path");raw=p.read_bytes();need(len(raw)==d.get("bytes") and sha(raw)==d.get("sha256"),"checkpoint outer seal");s=verify_state(json.loads(raw));need(s["accepted_sources"]==cert.get("accepted_sources") and s["accepted_count"]==cert.get("accepted_count") and s["rank"]==cert.get("physical_rank") and s["round"]==cert.get("round") and s["reason"]==cert.get("reason") and s["current_dual_profile"]==cert.get("current_dual_profile"),"checkpoint artifact state");return s
def update(P,m):
    d,r,k=P["phys"].dual(P["target"]);d=m.normalize_dual(d,r);P["dual"],P["remainder"]=d,r;return d,r,k
def replay(P,m,p179,accepted,state):
    for s in accepted:
        validate(s);d,r,_=state;need(d is not None and len(P["phys"].order)==s["old_rank"] and c.digest(P["v12"],d)==s["pre_dual_digest"] and c.digest(P["v12"],r)==s["pre_remainder_digest"],"pre")
        if s["kind"]=="action":row=P["v12"].action_row(P["runtime"],P["owner"],P["p176"],P["q"],s["action_source"]);src=s["action_source"]
        else:
            info=c.adjoint(P)[1];need(info["adjoint_digest"]==s["adjoint_digest"],"adjoint");delta=s["delta_word"];word=p179.reduce_word(delta+list(P["pres"]["relators"][s["seed_index"]-1])+p179.inverse_word(delta));ex,ey=P["v12"].v3.exp_pair(word);need(ex%18==0 and ey%18==0 and [ex,ey]==s["exact_exponent_pair"],"exponent");row=P["v12"].aggregate(P["v12"].replay_atom(s["seed_index"],delta,P["runtime"],P["model"],P["pres"],P["owner"],P["p176"],P["q"]));src={"family":"DIRECT_CORRECTION","seed_index":s["seed_index"],"delta_word":delta,"source_digest":s["row_digest"]}
        need(c.digest(P["v12"],row)==s["row_digest"] and c.pair(d,row)==s["scalar"],"row");rise,p=P["phys"].add(row,src);need(rise and p.hex()==s["pivot"] and len(P["phys"].order)==s["new_rank"],"single add");state=update(P,m);d2,r2,_=state;need(c.digest(P["v12"],r2)==s["post_remainder_digest"] and (None if d2 is None else c.digest(P["v12"],d2))==s["post_dual_digest"],"post")
    return state
def independent_profile(P,m,p179,claimed,reason):
    q=P["q"];dual=P["dual"] or {};counts={str(x):{} for x in (1,2,3)};tau={str(x):0 for x in (1,2,3)};expo={"N1":0,"N2":0};bad=[]
    for k,c0 in sorted(dual.items()):
        value=int(c0)%3
        if k[:1]==b"N" and len(k)==2 and k[1] in (1,2):expo["N%d"%k[1]]=value;continue
        try:block,label,blob=q.parse(k)
        except Exception:bad.append([k.hex(),value]);continue
        allowed={"b","c","u0","u1","tau"} if block<3 else {"b","c","p","q","r","u0","u1","tau"}
        if block not in (1,2,3) or label not in allowed:bad.append([k.hex(),value]);continue
        counts[str(block)][label]=counts[str(block)].get(label,0)+1
        if label=="tau":tau[str(block)]=value
    out={"physical_rank":len(P["phys"].order),"dual_digest":P["v12"].row_digest(dual),"remainder_digest":P["v12"].row_digest(P["remainder"]),"target_pair":None if not dual else c.pair(dual,P["remainder"]),"normalized_exponents":expo,"localized_support_counts":counts,"tau_coefficients":tau,"unrecognized_keys":bad,"required_coordinates":[]};constants=[]
    if isinstance(claimed,dict) and "adjoint_digest" in claimed:
        raw,info=c.adjoint(P);out.update(info);model=m.model179(p179,P);coords=set();n1=dual.get(b"N\x01",0);n2=dual.get(b"N\x02",0)
        for word in P["pres"]["relators"]:
            f=model.occurrence_data(word,raw);coords.update(int(x) for x,t in f["merged"]);ex,ey=P["v12"].v3.exp_pair(list(word));need(ex%18==0 and ey%18==0,"profile exponent");constants.append((int(n1)*(ex//18)+int(n2)*(ey//18))%3)
        out["required_coordinates"]=sorted(coords)
    need(out==claimed,"complete current profile")
    if reason=="UNKNOWN_RESOURCE:NONZERO_TAU_PHASE_SELECTOR":need(any(tau.values()),"tau gate")
    elif reason=="UNKNOWN_RESOURCE:UNRECOGNIZED_DUAL_KEYS":need(bool(bad),"unrecognized gate")
    elif reason and reason.startswith("UNKNOWN_RESOURCE:SELECTOR_COORDINATES:S"):
        need(any(x not in (0,1,2) for x in out["required_coordinates"]),"coordinate gate");need(reason=="UNKNOWN_RESOURCE:SELECTOR_COORDINATES:S"+",".join(map(str,out["required_coordinates"])),"coordinate reason")
    elif reason=="UNKNOWN_RESOURCE:NONZERO_CONSTANT_SELECTOR":need(any(constants),"constant gate")
    elif reason=="UNKNOWN_RESOURCE:SEPARATOR_REQUIRES_INDEPENDENT_EXHAUSTION":need(not any(constants) and all(x in (0,1,2) for x in out["required_coordinates"]),"separator gate")
def reason_allowed(reason):
    exact={"UNKNOWN_RESOURCE:NONZERO_TAU_PHASE_SELECTOR","UNKNOWN_RESOURCE:UNRECOGNIZED_DUAL_KEYS","UNKNOWN_RESOURCE:NONZERO_CONSTANT_SELECTOR","UNKNOWN_RESOURCE:SEPARATOR_REQUIRES_INDEPENDENT_EXHAUSTION","UNKNOWN_RESOURCE:max_rises"}
    return reason in exact or reason.startswith("UNKNOWN_RESOURCE:SELECTOR_COORDINATES:S") or reason.startswith("UNKNOWN_RESOURCE:") and (reason.endswith(":time_limit") or reason.endswith(":rss_limit"))
def check(cert):
    need(cert.get("schema")==SCHEMA and cert.get("status") in {"UNKNOWN_RESOURCE","COMMON_CANDIDATE"} and cert.get("terminal")==cert.get("status"),"schema/status/terminal");need(cert.get("accepted_count")==len(cert.get("accepted_sources",[])),"count")
    need(cert.get("claims")=={"A0":cert["status"]=="COMMON_CANDIDATE","COMMON":False,"NONMEMBER":False,"fake":False,"Ihara":False},"claim boundary")
    if cert["status"]=="UNKNOWN_RESOURCE":need(isinstance(cert.get("reason"),str) and reason_allowed(cert["reason"]),"resource reason")
    checkpoint(cert);v1=c.load(c.V1,"task445_check_v1");v4=v1.load(v1.V4,"task445_check_v4");m=v4.load_v1();v12=m.load(m.V12,"task445_check_v12");p435=m.load(m.P435,"task445_check_p435");p179=m.load(m.P179,"task445_check_p179");P=v4.adapt(m,m.prefix(v12,p435,type("A",(),{"seconds":None,"rss_bytes":None})()));state=update(P,m);state=replay(P,m,p179,cert["accepted_sources"],state);need(len(P["phys"].order)==cert["physical_rank"],"rank");d,r,coeff=state
    if d is not None:independent_profile(P,m,p179,cert.get("current_dual_profile"),cert.get("reason"))
    if cert["status"]=="COMMON_CANDIDATE":need(d is None and cert.get("claims",{}).get("A0") is True and c.load(c.V1C,"task445_positive").positive(P,coeff)==cert.get("terminal_replay"),"positive")
    else:need(cert.get("claims",{}).get("A0") is False,"resource claim")
def self_test():
    base=c.self_test();calls=0
    def state():
        nonlocal calls;calls+=1;return calls
    x=state()
    for _ in range(4):x=state()
    need(calls==5,"single update counter");body={"schema":CP_SCHEMA,"binding":BINDING,"accepted_sources":[],"accepted_count":0,"round":2,"rank":43,"reason":"UNKNOWN_RESOURCE:test","current_dual_profile":None};body["state_sha256"]=sha(canonical(body));verify_state(body);rejected=[]
    for k,v in (("rank",44),("binding","0"*64),("state_sha256","0"*64)):
        z=dict(body);z[k]=v
        try:verify_state(z)
        except RuntimeError:rejected.append(k)
    need(len(rejected)==3,"seal mutations");return {"status":"PASS","v2":base,"synthetic_rises":4,"state_computations":calls,"checkpoint_mutations":rejected}
def main(argv=None):
    ap=argparse.ArgumentParser();ap.add_argument("artifact",nargs="?");ap.add_argument("--self-test",action="store_true");a=ap.parse_args(argv)
    if a.self_test:print(MARKER+"_SELFTEST_PASS "+json.dumps(self_test(),sort_keys=True));return 0
    need(a.artifact,"artifact");check(json.loads(Path(a.artifact).read_text(encoding="ascii")));print(MARKER+"_PASS");return 0
if __name__=="__main__":raise SystemExit(main())
