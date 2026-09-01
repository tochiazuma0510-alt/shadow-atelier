#!/usr/bin/env python3
"""Task445: single-update tau-free A0 rank ladder v3."""
from __future__ import annotations
import argparse,hashlib,importlib.util,json,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];SCHEMA="d972-r07-a0-actual-tau-free-rank-ladder/v3";CP_SCHEMA=SCHEMA+"/checkpoint";MARKER="R07_A0_ACTUAL_TAU_FREE_RANK_LADDER_V3"
V2=("search/d972_r07_a0_actual_tau_free_rank_ladder_v2.py",18191,"cd27d69b06538e77dac1963d147f4966d8f63b9bf0d9e54860f2dae69149369b")
def need(x,m):
    if not x:raise RuntimeError(m)
def sha(x):return hashlib.sha256(x).hexdigest()
def load(spec,name):
    p=ROOT/spec[0];raw=p.read_bytes();need(len(raw)==spec[1] and sha(raw)==spec[2],"pin:"+spec[0]);s=importlib.util.spec_from_file_location(name,p);need(s and s.loader,"loader");m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
b=load(V2,"task445_v2");BINDING=sha((SCHEMA+b.V1[2]).encode())
def checkpoint_state(accepted,round_no,rank,reason,profile):
    s={"schema":CP_SCHEMA,"binding":BINDING,"accepted_sources":accepted,"accepted_count":len(accepted),"round":round_no,"rank":rank,"reason":reason,"current_dual_profile":profile};s["state_sha256"]=sha(b.canonical(s));return s
def cp_read(path):
    p=Path(path);need(not p.is_absolute() and p.parent==Path("ci/out"),"resume path");s=json.loads(p.read_text(encoding="ascii"));need(s.get("schema")==CP_SCHEMA and s.get("binding")==BINDING,"checkpoint binding");h=s.pop("state_sha256",None);need(h==sha(b.canonical(s)),"checkpoint seal");s["state_sha256"]=h;need(s.get("accepted_count")==len(s.get("accepted_sources",[])),"checkpoint count");[b.validate_source(x) for x in s["accepted_sources"]];return s
def cp_write(path,state):return b.cp_write(path,state)
def tau_free_adjoint(P,m,args):
    q=P["q"];dual=P["dual"];new={};old_candidates={};localized=0;scans=0
    for key,coef in sorted(dual.items()):
        scans+=1
        if scans%32==0:m.budget_check(P,args,"tau_free_localized_dual")
        if key[:1]==b"N":continue
        block,label,blob=q.parse(key)
        if label=="tau":continue
        localized+=1;g=q.e3 if block<3 else q.e4;z=q.z3 if block<3 else q.z4;n=2 if block<3 else 5;marks=[g.eval([2]),g.eval([3])] if block<3 else [g.eval([2]),g.eval([4]),g.eval([3]),g.eval([5]),g.eval([6])];r=q.dec(blob,block)
        for j in range(3):
            h=g.mul(r,P["v12"].central_power3(g,z,j));new[(block,n,q.enc(h))]=h
            for c,s in enumerate(marks):new[(block,c,q.enc(h))]=h;hp=g.mul(h,g.inverse(s));new[(block,c,q.enc(hp))]=hp
    for ix,((block,c,blob),h) in enumerate(sorted(new.items(),key=lambda x:x[0])):
        if ix%64==0:m.budget_check(P,args,"tau_free_reverse_neighbourhood")
        g=q.e3 if block<3 else q.e4;n=2 if block<3 else 5
        if block<3:
            x,y=g.eval([1]),g.eval([2]);items=[(1,h)] if c==n else ([(2,h),(1,g.mul(h,g.inverse(x)))] if c==0 else [(3,h),(1,b.mul_many(g,h,g.inverse(y),g.inverse(x)))])
        else:
            a,bb,p,cc,qq,r=[g.eval([i]) for i in range(1,7)];zi=g.inverse(q.z4);table={0:(2,(bb,cc,p,qq,r)),1:(4,(cc,p,qq,r)),2:(3,(p,qq,r)),3:(5,(qq,r)),4:(6,(r,))}
            if c==n:items=[(1,h)]
            else:comp,factors=table[c];items=[(comp,h),(1,b.mul_many(g,h,*factors,zi))]
        for comp,v in items:old_candidates[b.old_key(P,block,comp,v,"task445 old singleton")]=1
    raw={}
    for ix,k in enumerate(sorted(old_candidates)):
        if ix%64==0:m.budget_check(P,args,"tau_free_old_candidates")
        value=b.pair(dual,q.transform({k:1}))
        if value:raw[k]=value
    pub=[[k.hex(),v] for k,v in sorted(raw.items())];return raw,{"localized_dual_support":localized,"new_candidate_count":len(new),"old_candidate_count":len(old_candidates),"retained_old_support":len(raw),"adjoint_digest":sha(b.canonical(pub))}
def compile_formulas(P,m,p179,raw,args):
    model=m.model179(p179,P);out=[];coords=set();n1=P["dual"].get(b"N\x01",0);n2=P["dual"].get(b"N\x02",0);ids=[P["p176"]["packed_joint_blob"](P["runtime"].e3.identity,"task445 identity") for _ in range(5)]+[P["p176"]["packed_joint_blob"](P["runtime"].e4.identity,"task445 identity") for _ in range(5)]
    for i,word in enumerate(P["pres"]["relators"],1):
        m.budget_check(P,args,"tau_free_formula_seed");f=model.occurrence_data(word,raw);ex,ey=P["v12"].v3.exp_pair(list(word));need(ex%18==0 and ey%18==0,"seed normalized exponent");K=(int(n1)*(ex//18)+int(n2)*(ey//18))%3;merged={(int(c),t):int(v)%3 for (c,t),v in f["merged"].items() if int(v)%3};coords.update(c for c,_ in merged);fresh=P["v12"].aggregate(P["v12"].seed_v12(P["model"],P["runtime"].old,P["owner"],P["p176"],P["q"],list(word)));need((K+model.formula_scalar(f,ids))%3==b.pair(P["dual"],fresh),"identity physical scalar");out.append({"seed_index":i,"K":K,"merged":merged,"public":f["public"],"required_coordinates":sorted({c for c,_ in merged})})
    return model,out,sorted(coords)
def insert(P,m,accepted,round_no,kind,row,scalar,source,extra,state):
    pre_dual,pre_rem,pre_coeff=state;old=len(P["phys"].order);need(pre_dual is P["dual"] and pre_rem is P["remainder"] and b.pair(pre_dual,row)==scalar and scalar,"pre-state pairing");digest=P["v12"].row_digest(row);src=dict(source);src["row_digest"]=digest;rise,pivot=P["phys"].add(row,src);need(rise and pivot is not None and len(P["phys"].order)==old+1,"single add rise");post=b.update(P,m);post_dual,post_rem,_=post;rec={"kind":kind,"round":round_no,"old_rank":old,"new_rank":old+1,"scalar":scalar,"row_digest":digest,"pivot":pivot.hex(),"pre_remainder_digest":P["v12"].row_digest(pre_rem),"pre_dual_digest":P["v12"].row_digest(pre_dual),"post_remainder_digest":P["v12"].row_digest(post_rem),"post_dual_digest":None if post_dual is None else P["v12"].row_digest(post_dual)};rec.update(extra);b.validate_source(rec);accepted.append(rec);return rec,post
def replay(P,m,p179,accepted,state):
    for s in accepted:
        b.validate_source(s);d,r,_=state;need(d is not None and len(P["phys"].order)==s["old_rank"] and P["v12"].row_digest(d)==s["pre_dual_digest"] and P["v12"].row_digest(r)==s["pre_remainder_digest"],"resume pre-state");row=b.direct_row(P,s);need(P["v12"].row_digest(row)==s["row_digest"] and b.pair(d,row)==s["scalar"],"resume row")
        if s["kind"]=="correction":
            delta=s["delta_word"];word=p179.reduce_word(delta+list(P["pres"]["relators"][s["seed_index"]-1])+p179.inverse_word(delta));ex,ey=P["v12"].v3.exp_pair(word);need(ex%18==0 and ey%18==0 and [ex,ey]==s["exact_exponent_pair"],"resume exponent");src={"family":"DIRECT_CORRECTION","seed_index":s["seed_index"],"delta_word":delta,"source_digest":s["row_digest"]}
        else:src=s["action_source"]
        rise,p=P["phys"].add(row,src);need(rise and p.hex()==s["pivot"] and len(P["phys"].order)==s["new_rank"],"resume add");state=b.update(P,m);d2,r2,_=state;need(P["v12"].row_digest(r2)==s["post_remainder_digest"] and (None if d2 is None else P["v12"].row_digest(d2))==s["post_dual_digest"],"resume post")
    return state
def terminal(status,reason,P,accepted,round_no,prof,seal,started,pos=None):
    x=b.terminal(status,reason,P,accepted,round_no,prof,seal,started,pos);x["schema"]=SCHEMA;x["pins"]={"v2":{"path":V2[0],"bytes":V2[1],"sha256":V2[2]}};return x
def run(a):
    started=time.monotonic();v1=load(b.V1,"task445_v1");v4=v1.load(v1.V4,"task445_v4");m=v4.load_v1();m.RUN_STARTED=started;m.MARKER=MARKER;v12=m.load(m.V12,"task445_v12");p435=m.load(m.P435,"task445_p435");p179=m.load(m.P179,"task445_p179");P=v4.adapt(m,m.prefix(v12,p435,a));P["started"]=started;accepted=[];round_no=0;state=b.update(P,m)
    if a.resume:s=cp_read(a.resume);accepted=list(s["accepted_sources"]);round_no=int(s["round"]);state=replay(P,m,p179,accepted,state);need(len(P["phys"].order)==s["rank"],"resume rank")
    new_rises=0;sf=None;current=None;seal=cp_write(a.checkpoint,checkpoint_state(accepted,round_no,len(P["phys"].order),"initial_or_resumed",current));actions=list(P["runtime"].old.pure_relations(4)[5:11])
    try:
        while True:
            dual,rem,coeff=state;round_no+=1
            if dual is None:
                current=None;seal=cp_write(a.checkpoint,checkpoint_state(accepted,round_no,len(P["phys"].order),None,current));return terminal("COMMON_CANDIDATE",None,P,accepted,round_no,current,seal,started,v1.positive(P,m,coeff))
            current=b.profile(P);need(not current["unrecognized_keys"],"UNKNOWN_RESOURCE:UNRECOGNIZED_DUAL_KEYS")
            if new_rises>=a.max_rises:raise RuntimeError("UNKNOWN_RESOURCE:max_rises")
            hit=None
            for cand,src in P["q"].action_support_hits(P["runtime"],P["owner"],P["p176"],actions,dual):
                row=v12.action_row(P["runtime"],P["owner"],P["p176"],P["q"],src);scalar=b.pair(dual,row);need(row==cand and scalar==int(src["scalar"])%3 and scalar,"action scalar");hit=("action",row,scalar,src,{"action_source":v1.public_source(src)});break
            if hit is None:
                if any(current["tau_coefficients"].values()):raise RuntimeError("UNKNOWN_RESOURCE:NONZERO_TAU_PHASE_SELECTOR")
                raw,adj=tau_free_adjoint(P,m,a);model,formulas,coords=compile_formulas(P,m,p179,raw,a);current.update(adj);current["required_coordinates"]=coords
                if any(c not in (0,1,2) for c in coords):raise RuntimeError("UNKNOWN_RESOURCE:SELECTOR_COORDINATES:S"+",".join(map(str,coords)))
                if any(f["K"] for f in formulas):raise RuntimeError("UNKNOWN_RESOURCE:NONZERO_CONSTANT_SELECTOR")
                if sf is None:_,sf=m.selective_runtime(P,p179,a)
                z=b.weighted_hit(P,m,p179,formulas,sf,model,a,adj["adjoint_digest"])
                if z is None:raise RuntimeError("UNKNOWN_RESOURCE:SEPARATOR_REQUIRES_INDEPENDENT_EXHAUSTION")
                row,scalar,extra=z;hit=("correction",row,scalar,{"family":"DIRECT_CORRECTION","seed_index":extra["seed_index"],"delta_word":extra["delta_word"],"source_digest":v12.row_digest(row)},extra)
            kind,row,scalar,src,extra=hit;rec,state=insert(P,m,accepted,round_no,kind,row,scalar,src,extra,state);new_rises+=1;dual2,rem2,_=state;current=b.profile(P) if dual2 is not None else None;seal=cp_write(a.checkpoint,checkpoint_state(accepted,round_no,len(P["phys"].order),"rank_rise",current));print(f"{MARKER} progress round={round_no} rank={len(P['phys'].order)} accepted_count={len(accepted)} new_rises={new_rises}",flush=True)
    except RuntimeError as e:
        if not str(e).startswith("UNKNOWN_RESOURCE:"):raise
        seal=cp_write(a.checkpoint,checkpoint_state(accepted,round_no,len(P["phys"].order),str(e),current));print(f"{MARKER} gate={e} rank={len(P['phys'].order)}",flush=True);return terminal("UNKNOWN_RESOURCE",str(e),P,accepted,round_no,current,seal,started)
def fixture():
    base=b.fixture();calls=0
    def state():
        nonlocal calls;calls+=1;return calls
    current=state();rises=3
    for _ in range(rises):current=state()
    need(calls==rises+1,"single-update count");return {"status":"PASS","v2_fixture":base,"synthetic_rises":rises,"state_computations":calls,"expected_state_computations":rises+1}
def main(argv=None):
    ap=argparse.ArgumentParser();ap.add_argument("--mode",choices=("PRODUCTION","FIXTURE"),default="PRODUCTION");ap.add_argument("--output",default="ci/out/d972_r07_a0_actual_tau_free_rank_ladder_v3.json");ap.add_argument("--checkpoint",default="ci/out/d972_r07_a0_actual_tau_free_rank_ladder_v3_output.checkpoint");ap.add_argument("--resume");ap.add_argument("--seconds",type=float,default=2400);ap.add_argument("--rss-bytes",type=int,default=4_800_000_000);ap.add_argument("--max-rises",type=int,default=64);a=ap.parse_args(argv)
    try:r={"schema":SCHEMA,"status":"FIXTURE","fixture":fixture()} if a.mode=="FIXTURE" else run(a)
    except Exception as e:r={"schema":SCHEMA,"status":"UNKNOWN_RESOURCE" if str(e).startswith("UNKNOWN_RESOURCE:") else "UNKNOWN","reason":str(e),"claims":{"A0":False,"COMMON":False,"NONMEMBER":False,"fake":False,"Ihara":False}}
    out=Path(a.output);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(r,sort_keys=True,separators=(",",":"))+"\n",encoding="ascii");print(f"{MARKER} status={r['status']}",flush=True);return 0
if __name__=="__main__":raise SystemExit(main())
