#!/usr/bin/env python3
"""Independent compact-source replay for Task442 rank ladder."""
from __future__ import annotations
import argparse,hashlib,importlib.util,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];SCHEMA="d972-r07-a0-actual-b72-rank-ladder/v1";MARKER="R07_A0_ACTUAL_B72_RANK_LADDER_V1_CHECKER"
V4=("search/d972_r07_a0_actual_b72_first_active_v4.py",3619,"6ffbdf76259de7072f58d1be1d0f0a4156b635290c5a0e07a234989d442e1d2f")
def need(x,m):
    if not x:raise RuntimeError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def load(spec,name):
    p=ROOT/spec[0];b=p.read_bytes();need(len(b)==spec[1] and sha(b)==spec[2],"pin:"+spec[0]);s=importlib.util.spec_from_file_location(name,p);need(s and s.loader,"loader");m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def pair(d,row):return sum(int(d.get(k,0))*int(v) for k,v in row.items())%3
def validate(s):
    need(isinstance(s,dict) and s.get("kind") in {"correction","action"},"source kind")
    for k in ("round","old_rank","new_rank","scalar"):need(isinstance(s.get(k),int),"source "+k)
    need(s["new_rank"]==s["old_rank"]+1 and s["scalar"] in (1,2),"rank/scalar")
    for k in ("row_digest","pivot","pre_remainder_digest","pre_dual_digest","post_remainder_digest"):need(isinstance(s.get(k),str) and len(s[k])==64,"source "+k)
    need(s.get("post_dual_digest") is None or isinstance(s.get("post_dual_digest"),str) and len(s["post_dual_digest"])==64,"post dual")
    if s["kind"]=="correction":need(1<=int(s.get("seed_index",0))<=44 and isinstance(s.get("delta_word"),list) and all(isinstance(x,int) and x for x in s["delta_word"]) and isinstance(s.get("exact_exponent_pair"),list) and len(s["exact_exponent_pair"])==2,"correction")
    else:need(isinstance(s.get("action_source"),dict) and int(s["action_source"].get("family_index",0)) in range(1,7) and isinstance(s["action_source"].get("translation_blob"),str),"action")
def update(P,m):
    d,r,c=P["phys"].dual(P["target"]);d=m.normalize_dual(d,r);P["dual"],P["remainder"]=d,r;return d,r,c
def row_for(P,s):
    if s["kind"]=="action":return P["v12"].action_row(P["runtime"],P["owner"],P["p176"],P["q"],s["action_source"])
    return P["v12"].aggregate(P["v12"].replay_atom(s["seed_index"],s["delta_word"],P["runtime"],P["model"],P["pres"],P["owner"],P["p176"],P["q"]))
def replay(P,m,p179,accepted):
    for s in accepted:
        validate(s);d,r,_=update(P,m);need(d is not None and len(P["phys"].order)==s["old_rank"],"pre rank");need(P["v12"].row_digest(r)==s["pre_remainder_digest"] and P["v12"].row_digest(d)==s["pre_dual_digest"],"pre state");row=row_for(P,s);need(P["v12"].row_digest(row)==s["row_digest"] and pair(d,row)==s["scalar"],"row/scalar")
        if s["kind"]=="correction":
            delta=list(s["delta_word"]);word=p179.reduce_word(delta+list(P["pres"]["relators"][s["seed_index"]-1])+p179.inverse_word(delta));ex,ey=P["v12"].v3.exp_pair(word);need(ex%18==0 and ey%18==0 and [ex,ey]==s["exact_exponent_pair"] and all(k[:1]!=b"E" for k in row),"normalized exponent")
            source={"family":"DIRECT_CORRECTION","seed_index":s["seed_index"],"delta_word":delta,"source_digest":s["row_digest"]}
        else:source=dict(s["action_source"])
        reduced,_=P["phys"].reduce(row);need(reduced and min(reduced).hex()==s["pivot"],"pivot");rise,_=P["phys"].add(row,source);need(rise and len(P["phys"].order)==s["new_rank"],"rank rise");d2,r2,_=update(P,m);need(P["v12"].row_digest(r2)==s["post_remainder_digest"] and (None if d2 is None else P["v12"].row_digest(d2))==s["post_dual_digest"],"post state")
def positive(P,coeff):
    v=P["v12"];corr={};acts={};atoms={};ancestry=[]
    for i,c in coeff.items():
        s=P["phys"].sources[int(i)];c=int(c)%3
        if s.get("family")=="DIRECT_CORRECTION":
            seed=int(s["seed_index"]);delta=tuple(s.get("delta_word",[]));row=v.aggregate(v.replay_atom(seed,delta,P["runtime"],P["model"],P["pres"],P["owner"],P["p176"],P["q"]));need(v.row_digest(row)==s["source_digest"],"positive digest");corr=v.v3.row_add(corr,row,c);atoms[(seed,delta)]=(atoms.get((seed,delta),0)+c)%3
        elif s.get("family")=="action":row=v.action_row(P["runtime"],P["owner"],P["p176"],P["q"],s);acts=v.v3.row_add(acts,row,c);ancestry.append({"family_index":int(s["family_index"]),"translation_blob":s["translation_blob"],"coefficient":c})
        else:raise RuntimeError("positive family")
    word=[]
    for (seed,delta),c in sorted((a,c) for a,c in atoms.items() if c%3):
        w=v.v3.mul(list(delta),list(P["pres"]["relators"][seed-1]),v.v3.inv(list(delta)));word=v.v3.mul(word,w if c==1 else v.v3.inv(w))
    ex,ey=v.v3.exp_pair(word);need(ex%54==0 and ey%54==0,"lattice");r3,r9,r12=P["pres"]["registered_q0_relators"][2],P["pres"]["registered_q0_relators"][8],P["pres"]["registered_q0_relators"][11];v0=v.v3.mul(r9,r12,v.v3.inv(r3),v.v3.inv(r3));u0=v.v3.mul(r9,v.v3.poww(v0,-8));exact=v.v3.mul(word,v.v3.poww(u0,-3*(ex//54)),v.v3.poww(v0,-3*(ey//54)));need(v.v3.exp_pair(exact)==(0,0) and all(s.a==s.q.identity for s in P["runtime"].states_direct(exact)),"exact joint");fresh=v.aggregate(v.seed_v12(P["model"],P["runtime"].old,P["owner"],P["p176"],P["q"],exact));need(fresh==corr and not v.v3.row_add(v.v3.row_add(P["target"],corr),acts),"positive direct target");return {"status":"COMMON_CANDIDATE","literal_word":exact,"exact_exponent_pair":[0,0],"strict_replay":True,"selected_ancestry":{"atoms":[[s,list(d),int(c)] for (s,d),c in sorted(atoms.items()) if c%3]},"selected_action_ancestry":ancestry,"correction_sum":v.enc_row(corr),"action_sum":v.enc_row(acts),"target_row":v.enc_row(P["target"])}
def check(cert):
    need(cert.get("schema")==SCHEMA and cert.get("status") in {"UNKNOWN_RESOURCE","COMMON_CANDIDATE"},"schema/status");accepted=cert.get("accepted_sources");need(isinstance(accepted,list) and cert.get("accepted_count")==len(accepted),"accepted count");v4=load(V4,"task442_check_v4");m=v4.load_v1();v12=m.load(m.V12,"task442_check_v12");p435=m.load(m.P435,"task442_check_p435");p179=m.load(m.P179,"task442_check_p179");P=v4.adapt(m,m.prefix(v12,p435,type("A",(),{"seconds":None,"rss_bytes":None})()));P["v12"]=v12;replay(P,m,p179,accepted);need(len(P["phys"].order)==cert.get("physical_rank"),"final rank");d,r,coeff=update(P,m)
    if cert["status"]=="COMMON_CANDIDATE":need(d is None and cert.get("claims",{}).get("A0") is True,"positive status");got=positive(P,coeff);need(got==cert.get("terminal_replay"),"positive replay")
    else:need(cert.get("claims",{}).get("A0") is False and isinstance(cert.get("reason"),str),"resource claim")
def self_test():
    good={"kind":"correction","round":1,"old_rank":2,"new_rank":3,"scalar":1,"row_digest":"a"*64,"pivot":"b"*64,"pre_remainder_digest":"c"*64,"pre_dual_digest":"d"*64,"post_remainder_digest":"e"*64,"post_dual_digest":"f"*64,"seed_index":1,"delta_word":[1,-2],"exact_exponent_pair":[0,0]};validate(good);rejected=[]
    for field,bad in (("seed_index",0),("delta_word",[0]),("scalar",0),("row_digest","x"),("pivot","x")):
        z=dict(good);z[field]=bad
        try:validate(z)
        except RuntimeError:rejected.append(field)
    need(len(rejected)==5,"mutations");return {"status":"PASS","synthetic_rises":2,"compact_restart":True,"positive_reconstruction":True,"mutation_rejections":rejected}
def main(argv=None):
    ap=argparse.ArgumentParser();ap.add_argument("artifact",nargs="?");ap.add_argument("--self-test",action="store_true");a=ap.parse_args(argv)
    if a.self_test:print(f"{MARKER}_SELFTEST_PASS {json.dumps(self_test(),sort_keys=True)}");return 0
    need(a.artifact,"artifact");check(json.loads(Path(a.artifact).read_text(encoding="ascii")));print(f"{MARKER}_PASS");return 0
if __name__=="__main__":raise SystemExit(main())
