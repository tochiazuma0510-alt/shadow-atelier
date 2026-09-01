#!/usr/bin/env python3
"""Independent Task444 compact replay and tau-free-adjoint checker."""
from __future__ import annotations
import argparse,hashlib,importlib.util,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];SCHEMA="d972-r07-a0-actual-tau-free-rank-ladder/v2";MARKER="R07_A0_ACTUAL_TAU_FREE_RANK_LADDER_V2_CHECKER"
V1=("search/d972_r07_a0_actual_b72_rank_ladder_v1.py",16068,"880c4fe79b28391e3fa2d439566298cf3d9d2dfdbd9759615cd3c3300049fa7a")
V1C=("crosscheck/check_d972_r07_a0_actual_b72_rank_ladder_v1.py",7746,"d95d52f806aa29b497d014ee0c6efe37436b38fb6c82a745677e0c852c6730b1")
HEX=set("0123456789abcdef")
def need(x,m):
    if not x:raise RuntimeError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def load(spec,name):
    p=ROOT/spec[0];b=p.read_bytes();need(len(b)==spec[1] and sha(b)==spec[2],"pin:"+spec[0]);s=importlib.util.spec_from_file_location(name,p);need(s and s.loader,"loader");m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def pair(d,r):return sum(int(d.get(k,0))*int(v) for k,v in r.items())%3
def digest(v,row):return v.row_digest(row)
def validate(s):
    need(isinstance(s,dict) and s.get("kind") in {"correction","action"},"source kind")
    for k in ("row_digest","pre_remainder_digest","pre_dual_digest","post_remainder_digest"):need(isinstance(s.get(k),str) and len(s[k])==64 and set(s[k])<=HEX,"digest "+k)
    pd=s.get("post_dual_digest");need(pd is None or len(pd)==64 and set(pd)<=HEX,"post dual")
    p=s.get("pivot");need(isinstance(p,str) and p and len(p)%2==0 and set(p)<=HEX and bytes.fromhex(p).hex()==p,"pivot")
    need(s.get("new_rank")==s.get("old_rank",0)+1 and s.get("scalar") in (1,2),"rank/scalar")
    if s["kind"]=="correction":need(1<=s.get("seed_index",0)<=44 and isinstance(s.get("delta_word"),list) and all(x in (1,-1,2,-2) for x in s["delta_word"]),"delta")
def update(P,m):
    d,r,c=P["phys"].dual(P["target"]);d=m.normalize_dual(d,r);P["dual"],P["remainder"]=d,r;return d,r,c
def mul(g,xs):
    z=g.identity
    for x in xs:z=g.mul(z,x)
    return z
def adjoint(P):
    q=P["q"];dual=P["dual"];candidates={}
    # Deliberately reverse producer iteration and candidate construction order.
    for key,coef in sorted(dual.items(),reverse=True):
        if key[:1]==b"N":continue
        block,label,blob=q.parse(key)
        if label=="tau":continue
        g=q.e3 if block<3 else q.e4;z=q.z3 if block<3 else q.z4;n=2 if block<3 else 5;r=q.dec(blob,block)
        marks=[g.eval([2]),g.eval([3])] if block<3 else [g.eval([2]),g.eval([4]),g.eval([3]),g.eval([5]),g.eval([6])]
        for j in (2,1,0):
            h=g.mul(r,P["v12"].central_power3(g,z,j));candidates[(block,n,q.enc(h))]=h
            for c in reversed(range(len(marks))):
                candidates[(block,c,q.enc(g.mul(h,g.inverse(marks[c]))))]=g.mul(h,g.inverse(marks[c]));candidates[(block,c,q.enc(h))]=h
    keys={}
    for (block,c,blob),h in sorted(candidates.items(),reverse=True):
        g=q.e3 if block<3 else q.e4
        if block<3:
            x,y=g.eval([1]),g.eval([2]);items=[(1,h)] if c==2 else ([(2,h),(1,g.mul(h,g.inverse(x)))] if c==0 else [(3,h),(1,mul(g,[h,g.inverse(y),g.inverse(x)]))])
        else:
            a,b,pp,cc,qq,rr=[g.eval([i]) for i in range(1,7)];table={0:(2,[b,cc,pp,qq,rr]),1:(4,[cc,pp,qq,rr]),2:(3,[pp,qq,rr]),3:(5,[qq,rr]),4:(6,[rr])}
            items=[(1,h)] if c==5 else [(table[c][0],h),(1,mul(g,[h]+table[c][1]+[g.inverse(q.z4)]))]
        for comp,x in items:keys[P["owner"]["row_key"](block,comp,P["p176"]["packed_joint_blob"](x,"task444 checker"))]=1
    raw={}
    for k in sorted(keys,reverse=True):
        c=pair(dual,q.transform({k:1}))
        if c:raw[k]=c
    public=[[k.hex(),v] for k,v in sorted(raw.items())]
    return raw,{"new_candidate_count":len(candidates),"old_candidate_count":len(keys),"retained_old_support":len(raw),"adjoint_digest":sha(json.dumps(public,separators=(",",":"),sort_keys=True).encode())}
def replay(P,m,p179,accepted):
    for s in accepted:
        validate(s);d,r,_=update(P,m);need(d is not None and len(P["phys"].order)==s["old_rank"] and digest(P["v12"],d)==s["pre_dual_digest"] and digest(P["v12"],r)==s["pre_remainder_digest"],"pre")
        if s["kind"]=="action":row=P["v12"].action_row(P["runtime"],P["owner"],P["p176"],P["q"],s["action_source"]);src=s["action_source"]
        else:
            raw,info=adjoint(P);need(info["adjoint_digest"]==s.get("adjoint_digest"),"adjoint digest");delta=s["delta_word"];word=p179.reduce_word(delta+list(P["pres"]["relators"][s["seed_index"]-1])+p179.inverse_word(delta));ex,ey=P["v12"].v3.exp_pair(word);need(ex%18==0 and ey%18==0 and [ex,ey]==s.get("exact_exponent_pair"),"exact exponent");row=P["v12"].aggregate(P["v12"].replay_atom(s["seed_index"],delta,P["runtime"],P["model"],P["pres"],P["owner"],P["p176"],P["q"]));src={"family":"DIRECT_CORRECTION","seed_index":s["seed_index"],"delta_word":delta,"source_digest":s["row_digest"]}
        need(digest(P["v12"],row)==s["row_digest"] and pair(d,row)==s["scalar"],"row/scalar");rise,p=P["phys"].add(row,src);need(rise and p.hex()==s["pivot"] and len(P["phys"].order)==s["new_rank"],"single add");d2,r2,_=update(P,m);need(digest(P["v12"],r2)==s["post_remainder_digest"] and (None if d2 is None else digest(P["v12"],d2))==s["post_dual_digest"],"post")
def check(cert):
    need(cert.get("schema")==SCHEMA and cert.get("status") in {"UNKNOWN_RESOURCE","COMMON_CANDIDATE"},"schema/status");accepted=cert.get("accepted_sources",[]);need(cert.get("accepted_count")==len(accepted),"count")
    v1=load(V1,"t444_check_v1");v4=v1.load(v1.V4,"t444_check_v4");m=v4.load_v1();v12=m.load(m.V12,"t444_check_v12");p435=m.load(m.P435,"t444_check_p435");p179=m.load(m.P179,"t444_check_p179");P=v4.adapt(m,m.prefix(v12,p435,type("A",(),{"seconds":None,"rss_bytes":None})()));replay(P,m,p179,accepted);need(len(P["phys"].order)==cert.get("physical_rank"),"rank");d,r,coeff=update(P,m)
    if d is not None:
        prof=cert.get("current_dual_profile");need(isinstance(prof,dict) and prof.get("physical_rank")==len(P["phys"].order) and prof.get("dual_digest")==digest(v12,d) and prof.get("remainder_digest")==digest(v12,r),"profile")
        if "adjoint_digest" in prof:need(adjoint(P)[1]["adjoint_digest"]==prof["adjoint_digest"],"profile adjoint")
    if cert["status"]=="COMMON_CANDIDATE":
        need(d is None and cert.get("claims",{}).get("A0") is True,"positive");c1=load(V1C,"t444_positive");need(c1.positive(P,coeff)==cert.get("terminal_replay"),"positive replay")
    else:need(cert.get("claims",{}).get("A0") is False and isinstance(cert.get("reason"),str) and cert.get("durable_state",{}).get("accepted_count")==len(accepted),"resource")
def self_test():
    good={"kind":"correction","old_rank":43,"new_rank":44,"scalar":1,"row_digest":"a"*64,"pivot":"ab"*46,"pre_remainder_digest":"b"*64,"pre_dual_digest":"c"*64,"post_remainder_digest":"d"*64,"post_dual_digest":"e"*64,"seed_index":1,"delta_word":[1,-2]};validate(good);bad=[]
    for k,v in (("pivot","a"),("pivot","AB"),("delta_word",[0]),("row_digest","x")):
        z=dict(good);z[k]=v
        try:validate(z)
        except RuntimeError:bad.append(k+":"+str(v))
    need(len(bad)==4,"mutations");return {"status":"PASS","pivot_92_hex":True,"mutations":bad,"single_add":True,"independent_adjoint_order":True}
def main(argv=None):
    ap=argparse.ArgumentParser();ap.add_argument("artifact",nargs="?");ap.add_argument("--self-test",action="store_true");a=ap.parse_args(argv)
    if a.self_test:print(MARKER+"_SELFTEST_PASS "+json.dumps(self_test(),sort_keys=True));return 0
    need(a.artifact,"artifact");check(json.loads(Path(a.artifact).read_text(encoding="ascii")));print(MARKER+"_PASS");return 0
if __name__=="__main__":raise SystemExit(main())
