#!/usr/bin/env python3
"""Task444: general tau-free quotient-weighted A0 rank ladder v2."""
from __future__ import annotations
import argparse,hashlib,importlib.util,json,os,tempfile,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SCHEMA="d972-r07-a0-actual-tau-free-rank-ladder/v2";CP_SCHEMA=SCHEMA+"/checkpoint";MARKER="R07_A0_ACTUAL_TAU_FREE_RANK_LADDER_V2"
V1=("search/d972_r07_a0_actual_b72_rank_ladder_v1.py",16068,"880c4fe79b28391e3fa2d439566298cf3d9d2dfdbd9759615cd3c3300049fa7a")
BINDING=hashlib.sha256((SCHEMA+V1[2]).encode()).hexdigest();HEX=set("0123456789abcdef")
def need(x,m):
    if not x:raise RuntimeError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def load(spec,name):
    p=ROOT/spec[0];b=p.read_bytes();need(len(b)==spec[1] and sha(b)==spec[2],"pin:"+spec[0]);s=importlib.util.spec_from_file_location(name,p);need(s and s.loader,"loader");m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def pair(d,row):return sum(int(d.get(k,0))*int(v) for k,v in row.items())%3
def hex64(x):return isinstance(x,str) and len(x)==64 and set(x)<=HEX
def pivot_hex(x):
    if not isinstance(x,str) or not x or len(x)%2 or set(x)>HEX:return False
    try:return bytes.fromhex(x).hex()==x
    except ValueError:return False
def canonical(x):return json.dumps(x,sort_keys=True,separators=(",",":")).encode("ascii")
def validate_source(s):
    need(isinstance(s,dict) and s.get("kind") in {"correction","action"},"source kind")
    for k in ("round","old_rank","new_rank","scalar"):need(isinstance(s.get(k),int),"source "+k)
    need(s["new_rank"]==s["old_rank"]+1 and s["scalar"] in (1,2),"source rank/scalar")
    for k in ("row_digest","pre_remainder_digest","pre_dual_digest","post_remainder_digest"):need(hex64(s.get(k)),"source "+k)
    need(s.get("post_dual_digest") is None or hex64(s.get("post_dual_digest")),"post dual");need(pivot_hex(s.get("pivot")),"source pivot")
    if s["kind"]=="correction":need(1<=int(s.get("seed_index",0))<=44 and isinstance(s.get("delta_word"),list) and all(x in (1,-1,2,-2) for x in s["delta_word"]) and isinstance(s.get("exact_exponent_pair"),list) and len(s["exact_exponent_pair"])==2 and hex64(s.get("adjoint_digest")),"correction source")
    else:need(isinstance(s.get("action_source"),dict) and int(s["action_source"].get("family_index",0)) in range(1,7) and isinstance(s["action_source"].get("translation_blob"),str),"action source")
    return s
def checkpoint_state(accepted,round_no,rank,reason,profile):
    s={"schema":CP_SCHEMA,"binding":BINDING,"accepted_sources":accepted,"accepted_count":len(accepted),"round":round_no,"rank":rank,"reason":reason,"current_dual_profile":profile};s["state_sha256"]=sha(canonical(s));return s
def cp_write(path,s):
    need(path,"checkpoint required");p=Path(path);need(not p.is_absolute() and p.parent==Path("ci/out"),"checkpoint path");p.parent.mkdir(parents=True,exist_ok=True);raw=canonical(s)+b"\n"
    with tempfile.NamedTemporaryFile(dir=p.parent,delete=False) as f:f.write(raw);f.flush();os.fsync(f.fileno());tmp=Path(f.name)
    os.replace(tmp,p);return {"path":str(p),"bytes":len(raw),"sha256":sha(raw),"accepted_count":len(s["accepted_sources"]),"rank":s["rank"]}
def cp_read(path):
    p=Path(path);need(not p.is_absolute() and p.parent==Path("ci/out"),"resume path");s=json.loads(p.read_text(encoding="ascii"));need(s.get("schema")==CP_SCHEMA and s.get("binding")==BINDING,"checkpoint binding");h=s.pop("state_sha256",None);need(h==sha(canonical(s)),"checkpoint seal");s["state_sha256"]=h;need(s.get("accepted_count")==len(s.get("accepted_sources",[])),"checkpoint count");[validate_source(x) for x in s["accepted_sources"]];return s
def update(P,m):
    d,r,c=P["phys"].dual(P["target"]);d=m.normalize_dual(d,r);P["dual"],P["remainder"]=d,r;return d,r,c
def profile(P):
    q=P["q"];dual=P["dual"] or {};counts={str(b):{} for b in (1,2,3)};tau={str(b):0 for b in (1,2,3)};expo={"N1":0,"N2":0};bad=[]
    for k,c0 in sorted(dual.items()):
        c=int(c0)%3
        if k[:1]==b"N" and len(k)==2 and k[1] in (1,2):expo["N%d"%k[1]]=c;continue
        try:b,label,blob=q.parse(k)
        except Exception:bad.append([k.hex(),c]);continue
        if b not in (1,2,3) or label not in ({"b","c","u0","u1","tau"} if b<3 else {"b","c","p","q","r","u0","u1","tau"}):bad.append([k.hex(),c]);continue
        counts[str(b)][label]=counts[str(b)].get(label,0)+1
        if label=="tau":tau[str(b)]=c
    return {"physical_rank":len(P["phys"].order),"dual_digest":P["v12"].row_digest(dual),"remainder_digest":P["v12"].row_digest(P["remainder"]),"target_pair":None if not dual else pair(dual,P["remainder"]),"normalized_exponents":expo,"localized_support_counts":counts,"tau_coefficients":tau,"unrecognized_keys":bad,"required_coordinates":[]}
def mul_many(g,*xs):
    out=g.identity
    for x in xs:out=g.mul(out,x)
    return out
def old_key(P,block,comp,h,label):return P["owner"]["row_key"](block,comp,P["p176"]["packed_joint_blob"](h,label))
def tau_free_adjoint(P):
    q=P["q"];dual=P["dual"];new={};old_candidates={};localized=0
    for key,coef in sorted(dual.items()):
        if key[:1]==b"N":continue
        block,label,blob=q.parse(key)
        if label=="tau":continue
        localized+=1;g=q.e3 if block<3 else q.e4;z=q.z3 if block<3 else q.z4;n=2 if block<3 else 5;marks=[g.eval([2]),g.eval([3])] if block<3 else [g.eval([2]),g.eval([4]),g.eval([3]),g.eval([5]),g.eval([6])];r=q.dec(blob,block)
        for j in range(3):
            h=g.mul(r,P["v12"].central_power3(g,z,j));new[(block,n,q.enc(h))]=h
            for c,s in enumerate(marks):new[(block,c,q.enc(h))]=h;hp=g.mul(h,g.inverse(s));new[(block,c,q.enc(hp))]=hp
    for (block,c,blob),h in sorted(new.items(),key=lambda x:x[0]):
        g=q.e3 if block<3 else q.e4;n=2 if block<3 else 5
        if block<3:
            x,y=[g.eval([1]),g.eval([2])]
            if c==n:items=[(1,h)]
            elif c==0:items=[(2,h),(1,g.mul(h,g.inverse(x)))]
            else:items=[(3,h),(1,mul_many(g,h,g.inverse(y),g.inverse(x)))]
        else:
            a,b,p,cg,qg,r=[g.eval([i]) for i in range(1,7)];zi=g.inverse(P["q"].z4);labels={0:(2,(b,cg,p,qg,r)),1:(4,(cg,p,qg,r)),2:(3,(p,qg,r)),3:(5,(qg,r)),4:(6,(r,))}
            if c==n:items=[(1,h)]
            else:
                comp,factors=labels[c];pred=mul_many(g,h,*factors,zi);items=[(comp,h),(1,pred)]
        for comp,v in items:old_candidates[old_key(P,block,comp,v,"task444 old singleton")]=1
    raw={}
    for k in sorted(old_candidates):
        value=pair(dual,q.transform({k:1}))
        if value:raw[k]=value;need(pair(dual,q.transform({k:1}))==value,"direct singleton pairing")
    pub=[[k.hex(),v] for k,v in sorted(raw.items())];info={"localized_dual_support":localized,"new_candidate_count":len(new),"old_candidate_count":len(old_candidates),"retained_old_support":len(raw),"adjoint_digest":sha(canonical(pub))};return raw,info
def compile_formulas(P,m,p179,raw):
    model=m.model179(p179,P);out=[];coords=set();n1=P["dual"].get(b"N\x01",0);n2=P["dual"].get(b"N\x02",0);ids=[P["p176"]["packed_joint_blob"](P["runtime"].e3.identity,"task444 identity") for _ in range(5)]+[P["p176"]["packed_joint_blob"](P["runtime"].e4.identity,"task444 identity") for _ in range(5)]
    for i,word in enumerate(P["pres"]["relators"],1):
        f=model.occurrence_data(word,raw);ex,ey=P["v12"].v3.exp_pair(list(word));need(ex%18==0 and ey%18==0,"seed normalized exponent");K=(int(n1)*(ex//18)+int(n2)*(ey//18))%3;merged={(int(c),t):int(v)%3 for (c,t),v in f["merged"].items() if int(v)%3};coords.update(c for c,_ in merged);identity=(K+model.formula_scalar(f,ids))%3;fresh=P["v12"].aggregate(P["v12"].seed_v12(P["model"],P["runtime"].old,P["owner"],P["p176"],P["q"],list(word)));need(identity==pair(P["dual"],fresh),"identity physical scalar");out.append({"seed_index":i,"K":K,"merged":merged,"public":f["public"],"required_coordinates":sorted({c for c,_ in merged})})
    return model,out,sorted(coords)
def formula_scalar(model,f,blobs):return (f["K"]+sum(v for (c,t),v in f["merged"].items() if blobs[c]==t))%3
def weighted_hit(P,m,p179,formulas,sf,model,args,adj_digest):
    checked=0
    for f,seedword in zip(formulas,P["pres"]["relators"]):
        for coordinate,target in sorted(f["merged"],key=lambda x:(x[0],x[1])):
            fibre=sf.canonical(coordinate,target)
            if fibre is None:continue
            for k,eta in enumerate(sf.ensure_kernel_prefix(coordinate,9)):
                m.budget_check(P,args,"tau_free_candidate");checked+=1;cand=sf.kernel_candidate(fibre,eta);scalar=formula_scalar(model,f,cand["coordinate_blobs"])
                if not scalar:continue
                delta=list(cand["source_word"]);conj=p179.reduce_word(delta+list(seedword)+p179.inverse_word(delta));row=P["v12"].aggregate(P["v12"].replay_atom(f["seed_index"],delta,P["runtime"],P["model"],P["pres"],P["owner"],P["p176"],P["q"]));fresh=P["v12"].aggregate(P["v12"].seed_v12(P["model"],P["runtime"].old,P["owner"],P["p176"],P["q"],conj));need(row==fresh and pair(P["dual"],row)==scalar,"weighted direct scalar");ex,ey=P["v12"].v3.exp_pair(conj);need(ex%18==0 and ey%18==0 and all(x[:1]!=b"E" for x in row),"weighted exponent");return row,scalar,{"seed_index":f["seed_index"],"delta_word":delta,"exact_exponent_pair":[ex,ey],"adjoint_digest":adj_digest,"required_coordinates":f["required_coordinates"],"coordinate":coordinate,"target_hex":target.hex(),"fibre_cursor":k,"checked_fibres":checked}
    return None
def direct_row(P,s):
    if s["kind"]=="action":return P["v12"].action_row(P["runtime"],P["owner"],P["p176"],P["q"],s["action_source"])
    return P["v12"].aggregate(P["v12"].replay_atom(s["seed_index"],s["delta_word"],P["runtime"],P["model"],P["pres"],P["owner"],P["p176"],P["q"]))
def insert(P,m,accepted,round_no,kind,row,scalar,source,extra,pre_dual,pre_rem):
    old=len(P["phys"].order);need(pre_dual is P["dual"] and pre_rem is P["remainder"] and pair(pre_dual,row)==scalar and scalar,"pre-state pairing");digest=P["v12"].row_digest(row);src=dict(source);src["row_digest"]=digest;rise,pivot=P["phys"].add(row,src);need(rise and pivot is not None and len(P["phys"].order)==old+1,"single add rise");post_dual,post_rem,_=update(P,m);rec={"kind":kind,"round":round_no,"old_rank":old,"new_rank":old+1,"scalar":scalar,"row_digest":digest,"pivot":pivot.hex(),"pre_remainder_digest":P["v12"].row_digest(pre_rem),"pre_dual_digest":P["v12"].row_digest(pre_dual),"post_remainder_digest":P["v12"].row_digest(post_rem),"post_dual_digest":None if post_dual is None else P["v12"].row_digest(post_dual)};rec.update(extra);validate_source(rec);accepted.append(rec);return rec
def update(P,m):
    d,r,c=P["phys"].dual(P["target"]);d=m.normalize_dual(d,r);P["dual"],P["remainder"]=d,r;return d,r,c
def replay(P,m,p179,accepted):
    for s in accepted:
        validate_source(s);d,r,_=update(P,m);need(d is not None and len(P["phys"].order)==s["old_rank"] and P["v12"].row_digest(d)==s["pre_dual_digest"] and P["v12"].row_digest(r)==s["pre_remainder_digest"],"resume pre-state");row=direct_row(P,s);need(P["v12"].row_digest(row)==s["row_digest"] and pair(d,row)==s["scalar"],"resume row")
        if s["kind"]=="correction":
            delta=s["delta_word"];word=p179.reduce_word(delta+list(P["pres"]["relators"][s["seed_index"]-1])+p179.inverse_word(delta));ex,ey=P["v12"].v3.exp_pair(word);need(ex%18==0 and ey%18==0 and [ex,ey]==s["exact_exponent_pair"],"resume exact exponent");src={"family":"DIRECT_CORRECTION","seed_index":s["seed_index"],"delta_word":delta,"source_digest":s["row_digest"]}
        else:src=s["action_source"]
        rise,p=P["phys"].add(row,src);need(rise and p.hex()==s["pivot"] and len(P["phys"].order)==s["new_rank"],"resume single add");d2,r2,_=update(P,m);need(P["v12"].row_digest(r2)==s["post_remainder_digest"] and (None if d2 is None else P["v12"].row_digest(d2))==s["post_dual_digest"],"resume post-state")
def terminal(status,reason,P,accepted,round_no,profile0,seal,started,positive=None):return {"schema":SCHEMA,"status":status,"terminal":status,"reason":reason,"accepted_sources":accepted,"accepted_count":len(accepted),"round":round_no,"physical_rank":len(P["phys"].order),"current_dual_profile":profile0,"terminal_replay":positive,"durable_state":seal,"claims":{"A0":status=="COMMON_CANDIDATE","COMMON":False,"NONMEMBER":False,"fake":False,"Ihara":False},"pins":{"v1":{"path":V1[0],"bytes":V1[1],"sha256":V1[2]}},"elapsed_seconds":time.monotonic()-started}
def run(a):
    started=time.monotonic();v1=load(V1,"task444_v1");v4=v1.load(v1.V4,"task444_v4");m=v4.load_v1();m.RUN_STARTED=started;m.MARKER=MARKER;v12=m.load(m.V12,"task444_v12");p435=m.load(m.P435,"task444_p435");p179=m.load(m.P179,"task444_p179");P=v4.adapt(m,m.prefix(v12,p435,a));P["started"]=started;accepted=[];round_no=0
    if a.resume:s=cp_read(a.resume);accepted=list(s["accepted_sources"]);round_no=int(s["round"]);replay(P,m,p179,accepted);need(len(P["phys"].order)==s["rank"],"resume rank")
    new_rises=0;sf=None;model=None;current=None;seal=cp_write(a.checkpoint,checkpoint_state(accepted,round_no,len(P["phys"].order),"initial_or_resumed",current));actions=list(P["runtime"].old.pure_relations(4)[5:11])
    try:
        while True:
            dual,rem,coeff=update(P,m);round_no+=1
            if dual is None:pos=v1.positive(P,m,coeff);return terminal("COMMON_CANDIDATE",None,P,accepted,round_no,current,seal,started,pos)
            current=profile(P);need(not current["unrecognized_keys"],"UNKNOWN_RESOURCE:UNRECOGNIZED_DUAL_KEYS")
            if new_rises>=a.max_rises:raise RuntimeError("UNKNOWN_RESOURCE:max_rises")
            added=False
            for cand,src in P["q"].action_support_hits(P["runtime"],P["owner"],P["p176"],actions,dual):
                row=v12.action_row(P["runtime"],P["owner"],P["p176"],P["q"],src);scalar=pair(dual,row);need(row==cand and scalar==int(src["scalar"])%3 and scalar,"action scalar");rec=insert(P,m,accepted,round_no,"action",row,scalar,src,{"action_source":v1.public_source(src)},dual,rem);added=True;break
            if not added:
                if any(current["tau_coefficients"].values()):raise RuntimeError("UNKNOWN_RESOURCE:NONZERO_TAU_PHASE_SELECTOR")
                raw,adj=tau_free_adjoint(P);model,formulas,coords=compile_formulas(P,m,p179,raw);current.update(adj);current["required_coordinates"]=coords
                if any(c not in (0,1,2) for c in coords):raise RuntimeError("UNKNOWN_RESOURCE:SELECTOR_COORDINATES:S"+",".join(map(str,coords)))
                if any(f["K"] for f in formulas):raise RuntimeError("UNKNOWN_RESOURCE:NONZERO_CONSTANT_SELECTOR")
                if sf is None:_,sf=m.selective_runtime(P,p179,a)
                hit=weighted_hit(P,m,p179,formulas,sf,model,a,adj["adjoint_digest"])
                if hit is None:raise RuntimeError("UNKNOWN_RESOURCE:SEPARATOR_REQUIRES_INDEPENDENT_EXHAUSTION")
                row,scalar,extra=hit;src={"family":"DIRECT_CORRECTION","seed_index":extra["seed_index"],"delta_word":extra["delta_word"],"source_digest":v12.row_digest(row)};rec=insert(P,m,accepted,round_no,"correction",row,scalar,src,extra,dual,rem);sf.cache.clear()
            new_rises+=1;dual2,rem2,_=update(P,m);current=profile(P) if dual2 is not None else None;seal=cp_write(a.checkpoint,checkpoint_state(accepted,round_no,len(P["phys"].order),"rank_rise",current));rss=getattr(v12.v3,"rss",lambda:0)() or 0;print(f"{MARKER} progress round={round_no} rank={len(P['phys'].order)} accepted_count={len(accepted)} new_rises={new_rises} elapsed_seconds={time.monotonic()-started:.3f} rss_bytes={rss}",flush=True)
    except RuntimeError as e:
        if not str(e).startswith("UNKNOWN_RESOURCE:"):raise
        seal=cp_write(a.checkpoint,checkpoint_state(accepted,round_no,len(P["phys"].order),str(e),current));print(f"{MARKER} gate={e} rank={len(P['phys'].order)}",flush=True);return terminal("UNKNOWN_RESOURCE",str(e),P,accepted,round_no,current,seal,started)
def fixture():
    good={"kind":"correction","round":1,"old_rank":43,"new_rank":44,"scalar":1,"row_digest":"a"*64,"pivot":"ab"*46,"pre_remainder_digest":"b"*64,"pre_dual_digest":"c"*64,"post_remainder_digest":"d"*64,"post_dual_digest":"e"*64,"seed_index":1,"delta_word":[1,-2],"exact_exponent_pair":[0,0],"adjoint_digest":"f"*64};validate_source(good);need(len(good["pivot"])==92,"92 pivot");rejected=[]
    for label,field,bad in (("odd_pivot","pivot","a"),("noncanonical_pivot","pivot","AB"),("illegal_delta","delta_word",[3]),("bad_digest","row_digest","g"*64)):
        z=dict(good);z[field]=bad
        try:validate_source(z)
        except RuntimeError:rejected.append(label)
    history=[good];max_rises=2;new_rises=0;need(len(history)==1 and new_rises<max_rises,"resumed invocation budget");new_rises+=2;need(new_rises==max_rises,"new-rise cap");v1=load(V1,"task444_fixture_v1");base=v1.fixture();need(base["positive_reconstruction"],"positive helper fixture");return {"status":"PASS","pivot_92_hex":True,"mutation_rejections":rejected,"resumed_history":1,"new_rise_budget":2,"positive_helper":True}
def main(argv=None):
    ap=argparse.ArgumentParser();ap.add_argument("--mode",choices=("PRODUCTION","FIXTURE"),default="PRODUCTION");ap.add_argument("--output",default="ci/out/d972_r07_a0_actual_tau_free_rank_ladder_v2.json");ap.add_argument("--checkpoint",default="ci/out/d972_r07_a0_actual_tau_free_rank_ladder_v2_output.checkpoint");ap.add_argument("--resume");ap.add_argument("--seconds",type=float,default=2400);ap.add_argument("--rss-bytes",type=int,default=4_800_000_000);ap.add_argument("--max-rises",type=int,default=64);a=ap.parse_args(argv)
    try:r={"schema":SCHEMA,"status":"FIXTURE","fixture":fixture()} if a.mode=="FIXTURE" else run(a)
    except Exception as e:r={"schema":SCHEMA,"status":"UNKNOWN_RESOURCE" if str(e).startswith("UNKNOWN_RESOURCE:") else "UNKNOWN","reason":str(e),"claims":{"A0":False,"COMMON":False,"NONMEMBER":False,"fake":False,"Ihara":False}}
    out=Path(a.output);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(r,sort_keys=True,separators=(",",":"))+"\n",encoding="ascii");print(f"{MARKER} status={r['status']}",flush=True);return 0
if __name__=="__main__":raise SystemExit(main())
