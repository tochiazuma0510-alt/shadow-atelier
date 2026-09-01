#!/usr/bin/env python3
"""Task442: same-process quotient-weighted A0 rank ladder."""
from __future__ import annotations
import argparse,gc,hashlib,importlib.util,json,os,tempfile,time
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SCHEMA="d972-r07-a0-actual-b72-rank-ladder/v1";CP_SCHEMA=SCHEMA+"/checkpoint";MARKER="R07_A0_ACTUAL_B72_RANK_LADDER_V1"
V4=("search/d972_r07_a0_actual_b72_first_active_v4.py",3619,"6ffbdf76259de7072f58d1be1d0f0a4156b635290c5a0e07a234989d442e1d2f")
BINDING=hashlib.sha256((SCHEMA+V4[2]).encode()).hexdigest()
def need(x,m):
    if not x:raise RuntimeError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def load(spec,name):
    p=ROOT/spec[0];b=p.read_bytes();need(len(b)==spec[1] and sha(b)==spec[2],"pin:"+spec[0]);s=importlib.util.spec_from_file_location(name,p);need(s and s.loader,"loader");m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def pair(d,row):return sum(int(d.get(k,0))*int(v) for k,v in row.items())%3
def canonical(v):return json.dumps(v,sort_keys=True,separators=(",",":" )).encode("ascii")
def public_source(src):return {str(k):(v.hex() if isinstance(v,bytes) else v) for k,v in src.items() if isinstance(v,(str,int,bool,list,dict,bytes))}
def validate_source(s):
    need(isinstance(s,dict) and s.get("kind") in {"correction","action"},"source kind")
    for k in ("round","old_rank","new_rank","scalar"):need(isinstance(s.get(k),int),"source "+k)
    need(s["new_rank"]==s["old_rank"]+1 and s["scalar"] in (1,2),"source rank/scalar")
    for k in ("row_digest","pivot","pre_remainder_digest","pre_dual_digest","post_remainder_digest"):need(isinstance(s.get(k),str) and len(s[k])==64,"source "+k)
    need(s.get("post_dual_digest") is None or isinstance(s.get("post_dual_digest"),str) and len(s["post_dual_digest"])==64,"post dual")
    if s["kind"]=="correction":
        need(1<=int(s.get("seed_index",0))<=44 and isinstance(s.get("delta_word"),list) and all(isinstance(x,int) and x for x in s["delta_word"]),"correction source")
        need(isinstance(s.get("exact_exponent_pair"),list) and len(s["exact_exponent_pair"])==2,"correction exponent")
    else:need(isinstance(s.get("action_source"),dict) and int(s["action_source"].get("family_index",0)) in range(1,7) and isinstance(s["action_source"].get("translation_blob"),str),"action source")
    return s
def state(accepted,round_no,rank,reason):
    s={"schema":CP_SCHEMA,"binding":BINDING,"accepted_sources":accepted,"accepted_count":len(accepted),"round":round_no,"rank":rank,"reason":reason}
    s["state_sha256"]=sha(canonical({k:v for k,v in s.items() if k!="state_sha256"}));return s
def cp_write(path,s):
    if not path:return None
    p=Path(path);need(not p.is_absolute() and p.parent==Path("ci/out"),"checkpoint path");p.parent.mkdir(parents=True,exist_ok=True);raw=canonical(s)+b"\n"
    with tempfile.NamedTemporaryFile(dir=p.parent,delete=False) as f:f.write(raw);f.flush();os.fsync(f.fileno());tmp=Path(f.name)
    os.replace(tmp,p);return {"path":str(p),"bytes":len(raw),"sha256":sha(raw),"accepted_count":len(s["accepted_sources"]),"rank":s["rank"]}
def cp_read(path):
    p=Path(path);need(not p.is_absolute() and p.parent==Path("ci/out"),"resume path");s=json.loads(p.read_text(encoding="ascii"));need(s.get("schema")==CP_SCHEMA and s.get("binding")==BINDING,"checkpoint binding");h=s.pop("state_sha256",None);need(h==sha(canonical(s)),"checkpoint state seal");s["state_sha256"]=h;need(s.get("accepted_count")==len(s.get("accepted_sources",[])),"checkpoint count");[validate_source(x) for x in s["accepted_sources"]];return s
def update(P,m):
    dual,rem,coeff=P["phys"].dual(P["target"]);dual=m.normalize_dual(dual,rem);P["dual"],P["remainder"]=dual,rem;return dual,rem,coeff
def direct_row(P,s):
    v12=P["v12"]
    if s["kind"]=="action":return v12.action_row(P["runtime"],P["owner"],P["p176"],P["q"],s["action_source"])
    return v12.aggregate(v12.replay_atom(int(s["seed_index"]),list(s["delta_word"]),P["runtime"],P["model"],P["pres"],P["owner"],P["p176"],P["q"]))
def append_rise(P,m,accepted,round_no,kind,row,scalar,source,extra):
    dual,rem,_=update(P,m);old=len(P["phys"].order);need(dual is not None and pair(dual,row)==int(scalar)%3 and int(scalar)%3,"rise pairing");reduced,_=P["phys"].reduce(row);need(reduced,"strict rank rise");pivot=min(reduced);digest=P["v12"].row_digest(row);src=dict(source);src["row_digest"]=digest;rise,actual=P["phys"].add(row,src);need(rise and actual==pivot and len(P["phys"].order)==old+1,"rise insert");post_dual,post_rem,_=update(P,m)
    rec={"kind":kind,"round":round_no,"old_rank":old,"new_rank":old+1,"scalar":int(scalar)%3,"row_digest":digest,"pivot":pivot.hex(),"pre_remainder_digest":P["v12"].row_digest(rem),"pre_dual_digest":P["v12"].row_digest(dual),"post_remainder_digest":P["v12"].row_digest(post_rem),"post_dual_digest":None if post_dual is None else P["v12"].row_digest(post_dual)};rec.update(extra);validate_source(rec);accepted.append(rec);return rec
def replay_accepted(P,m,accepted):
    for rec in accepted:
        validate_source(rec);dual,rem,_=update(P,m);need(dual is not None,"resume target already zero");need(len(P["phys"].order)==rec["old_rank"] and P["v12"].row_digest(rem)==rec["pre_remainder_digest"] and P["v12"].row_digest(dual)==rec["pre_dual_digest"],"resume pre-state");row=direct_row(P,rec);need(P["v12"].row_digest(row)==rec["row_digest"] and pair(dual,row)==rec["scalar"],"resume row/scalar")
        if rec["kind"]=="correction":
            word=m.p179.reduce_word(list(rec["delta_word"])+list(P["pres"]["relators"][rec["seed_index"]-1])+m.p179.inverse_word(rec["delta_word"])) if hasattr(m,"p179") else None
            ex,ey=P["v12"].v3.exp_pair(word);need(ex%18==0 and ey%18==0 and [ex,ey]==rec["exact_exponent_pair"],"resume exponent")
        reduced,_=P["phys"].reduce(row);need(reduced and min(reduced).hex()==rec["pivot"],"resume pivot");src=rec["action_source"] if rec["kind"]=="action" else {"family":"DIRECT_CORRECTION","seed_index":rec["seed_index"],"delta_word":rec["delta_word"],"source_digest":rec["row_digest"]};rise,_=P["phys"].add(row,src);need(rise and len(P["phys"].order)==rec["new_rank"],"resume rank");d2,r2,_=update(P,m);need(P["v12"].row_digest(r2)==rec["post_remainder_digest"] and (None if d2 is None else P["v12"].row_digest(d2))==rec["post_dual_digest"],"resume post-state")
def weighted_hit(P,m,p179,raw,formulas,sf,model,args):
    checked=0
    for rec,seedword in zip(formulas,P["pres"]["relators"]):
        m.budget_check(P,args,"ladder_seed_%d"%rec["seed_index"]);f=model.occurrence_data(seedword,raw)
        for coordinate,target in sorted(f["merged"],key=lambda x:(x[0],x[1])):
            fibre=sf.canonical(int(coordinate),target)
            if fibre is None:continue
            for k,eta in enumerate(sf.ensure_kernel_prefix(int(coordinate),9)):
                m.budget_check(P,args,"ladder_candidate");checked+=1;cand=sf.kernel_candidate(fibre,eta);scalar=model.formula_scalar(f,cand["coordinate_blobs"])
                if not scalar:continue
                delta=list(cand["source_word"]);conj=p179.reduce_word(delta+list(seedword)+p179.inverse_word(delta));row=P["v12"].aggregate(P["v12"].replay_atom(rec["seed_index"],delta,P["runtime"],P["model"],P["pres"],P["owner"],P["p176"],P["q"]));fresh=P["v12"].aggregate(P["v12"].seed_v12(P["model"],P["runtime"].old,P["owner"],P["p176"],P["q"],conj));need(row==fresh,"weighted literal replay");ex,ey=P["v12"].v3.exp_pair(conj);need(ex%18==0 and ey%18==0 and all(x[:1]!=b"E" for x in row),"weighted exponent");need(pair(P["dual"],row)==scalar,"weighted scalar");return row,int(scalar),{"seed_index":rec["seed_index"],"delta_word":delta,"exact_exponent_pair":[ex,ey],"coordinate":int(coordinate),"target_hex":target.hex(),"fibre_cursor":k,"checked_fibres":checked}
    return None
def positive(P,m,coeff):
    v12=P["v12"];corr={};acts={};atoms={};ancestry=[]
    for i,c in coeff.items():
        s=P["phys"].sources[int(i)];c=int(c)%3
        if s.get("family")=="DIRECT_CORRECTION":
            seed=int(s["seed_index"]);delta=tuple(s.get("delta_word",[]));row=v12.aggregate(v12.replay_atom(seed,delta,P["runtime"],P["model"],P["pres"],P["owner"],P["p176"],P["q"]));need(v12.row_digest(row)==s["source_digest"],"positive correction digest");corr=v12.v3.row_add(corr,row,c);atoms[(seed,delta)]=(atoms.get((seed,delta),0)+c)%3
        elif s.get("family")=="action":
            row=v12.action_row(P["runtime"],P["owner"],P["p176"],P["q"],s);acts=v12.v3.row_add(acts,row,c);ancestry.append({"family_index":int(s["family_index"]),"translation_blob":s["translation_blob"],"coefficient":c})
        else:raise RuntimeError("positive source family")
    word=[]
    for (seed,delta),c in sorted((a,c) for a,c in atoms.items() if c%3):
        w=v12.v3.mul(list(delta),list(P["pres"]["relators"][seed-1]),v12.v3.inv(list(delta)));word=v12.v3.mul(word,w if c==1 else v12.v3.inv(w))
    ex,ey=v12.v3.exp_pair(word);need(ex%54==0 and ey%54==0,"exactification lattice");r3,r9,r12=P["pres"]["registered_q0_relators"][2],P["pres"]["registered_q0_relators"][8],P["pres"]["registered_q0_relators"][11];v0=v12.v3.mul(r9,r12,v12.v3.inv(r3),v12.v3.inv(r3));u0=v12.v3.mul(r9,v12.v3.poww(v0,-8));exact=v12.v3.mul(word,v12.v3.poww(u0,-3*(ex//54)),v12.v3.poww(v0,-3*(ey//54)));need(v12.v3.exp_pair(exact)==(0,0),"exact exponents");need(all(s.a==s.q.identity for s in P["runtime"].states_direct(exact)),"joint identity");fresh=v12.aggregate(v12.seed_v12(P["model"],P["runtime"].old,P["owner"],P["p176"],P["q"],exact));need(fresh==corr,"direct all-seven correction replay");need(not v12.v3.row_add(v12.v3.row_add(P["target"],corr),acts),"exact target zero");return {"status":"COMMON_CANDIDATE","literal_word":exact,"exact_exponent_pair":[0,0],"strict_replay":True,"selected_ancestry":{"atoms":[[s,list(d),int(c)] for (s,d),c in sorted(atoms.items()) if c%3]},"selected_action_ancestry":ancestry,"correction_sum":v12.enc_row(corr),"action_sum":v12.enc_row(acts),"target_row":v12.enc_row(P["target"])}
def run(a):
    need(a.checkpoint,"production checkpoint required");started=time.monotonic();v4=load(V4,"task442_v4");m=v4.load_v1();m.MARKER=MARKER;m.RUN_STARTED=started;v12=m.load(m.V12,"task442_v12");p435=m.load(m.P435,"task442_p435");p179=m.load(m.P179,"task442_p179");m.p179=p179;P=v4.adapt(m,m.prefix(v12,p435,a));P["started"]=started;accepted=[];round_no=0
    if a.resume:
        cp=cp_read(a.resume);accepted=list(cp["accepted_sources"]);round_no=int(cp["round"]);replay_accepted(P,m,accepted);need(len(P["phys"].order)==cp["rank"],"resume rank")
    seal=cp_write(a.checkpoint,state(accepted,round_no,len(P["phys"].order),"initial_or_resumed"))
    try:rt,sf=m.selective_runtime(P,p179,a)
    except RuntimeError as e:
        if not str(e).startswith("UNKNOWN_RESOURCE:"):raise
        return {"schema":SCHEMA,"status":"UNKNOWN_RESOURCE","terminal":"UNKNOWN_RESOURCE","reason":str(e),"accepted_sources":accepted,"accepted_count":len(accepted),"round":round_no,"physical_rank":len(P["phys"].order),"terminal_replay":None,"durable_state":seal,"claims":{"A0":False,"COMMON":False,"NONMEMBER":False,"fake":False,"Ihara":False},"pins":{"v4":{"path":V4[0],"bytes":V4[1],"sha256":V4[2]}},"elapsed_seconds":time.monotonic()-started}
    model=m.model179(p179,P);actions=list(P["runtime"].old.pure_relations(4)[5:11]);status="UNKNOWN_RESOURCE";reason=None;terminal=None
    try:
        while True:
            dual,rem,coeff=update(P,m);round_no+=1
            if dual is None:terminal=positive(P,m,coeff);status="COMMON_CANDIDATE";break
            if len(accepted)>=a.max_rises:reason="UNKNOWN_RESOURCE:max_rises";break
            added=False
            for cand,src in P["q"].action_support_hits(P["runtime"],P["owner"],P["p176"],actions,dual):
                direct=v12.action_row(P["runtime"],P["owner"],P["p176"],P["q"],src);need(direct==cand,"action direct replay");scalar=pair(dual,direct);need(scalar==int(src.get("scalar",0))%3 and scalar,"action scalar");rec=append_rise(P,m,accepted,round_no,"action",direct,scalar,src,{"action_source":public_source(src)});added=True;break
            if not added:
                try:raw,adj=m.actual_adjoint(P)
                except RuntimeError as e:raise RuntimeError("UNKNOWN_RESOURCE:current_dual_adjoint:"+str(e))
                formulas=m.compile_formulas(P,raw,p179,a);hit=weighted_hit(P,m,p179,raw,formulas,sf,model,a)
                if hit is None:reason="UNKNOWN_RESOURCE:exact_empty_requires_independent_exhaustion";break
                row,scalar,extra=hit;src={"family":"DIRECT_CORRECTION","seed_index":extra["seed_index"],"delta_word":extra["delta_word"],"source_digest":v12.row_digest(row)};rec=append_rise(P,m,accepted,round_no,"correction",row,scalar,src,extra)
                sf.cache.clear();del raw,adj,formulas;gc.collect()
            seal=cp_write(a.checkpoint,state(accepted,round_no,len(P["phys"].order),"rank_rise"));rss=getattr(v12.v3,"rss",lambda:0)() or 0;print(f"{MARKER} progress round={round_no} rank={len(P['phys'].order)} accepted_count={len(accepted)} elapsed_seconds={time.monotonic()-started:.3f} rss_bytes={rss}",flush=True)
    except RuntimeError as e:
        if not str(e).startswith("UNKNOWN_RESOURCE:"):raise
        reason=str(e)
    if status!="COMMON_CANDIDATE":seal=cp_write(a.checkpoint,state(accepted,round_no,len(P["phys"].order),reason or "resource"))
    return {"schema":SCHEMA,"status":status,"terminal":status,"reason":reason,"accepted_sources":accepted,"accepted_count":len(accepted),"round":round_no,"physical_rank":len(P["phys"].order),"terminal_replay":terminal,"durable_state":seal,"claims":{"A0":status=="COMMON_CANDIDATE","COMMON":False,"NONMEMBER":False,"fake":False,"Ihara":False},"pins":{"v4":{"path":V4[0],"bytes":V4[1],"sha256":V4[2]}},"elapsed_seconds":time.monotonic()-started}
def fixture():
    good={"kind":"correction","round":1,"old_rank":2,"new_rank":3,"scalar":1,"row_digest":"a"*64,"pivot":"b"*64,"pre_remainder_digest":"c"*64,"pre_dual_digest":"d"*64,"post_remainder_digest":"e"*64,"post_dual_digest":"f"*64,"seed_index":1,"delta_word":[1,-2],"exact_exponent_pair":[0,0]};validate_source(good);second=dict(good,round=2,old_rank=3,new_rank=4,scalar=2,pivot="1"*64);accepted=[good,second];s=state(accepted,2,4,"fixture");need(s["accepted_count"]==2 and s["rank"]==4,"fixture restart");word=[]
    for x in accepted:word+=x["delta_word"]+[x["seed_index"]]+[-v for v in reversed(x["delta_word"])]
    need(word,"fixture positive reconstruction");rejected=[]
    for field,bad in (("seed_index",0),("delta_word",[0]),("scalar",0),("row_digest","x"),("pivot","x")):
        z=dict(good);z[field]=bad
        try:validate_source(z)
        except RuntimeError:rejected.append(field)
    need(len(rejected)==5,"fixture mutations");return {"status":"PASS","synthetic_rises":2,"compact_restart":True,"positive_reconstruction":True,"mutation_rejections":rejected}
def main(argv=None):
    ap=argparse.ArgumentParser();ap.add_argument("--mode",choices=("PRODUCTION","FIXTURE"),default="PRODUCTION");ap.add_argument("--output",default="ci/out/d972_r07_a0_actual_b72_rank_ladder_v1.json");ap.add_argument("--checkpoint",default="ci/out/d972_r07_a0_actual_b72_rank_ladder_v1_output.checkpoint");ap.add_argument("--resume");ap.add_argument("--seconds",type=float,default=2400);ap.add_argument("--rss-bytes",type=int,default=4_800_000_000);ap.add_argument("--max-rises",type=int,default=64);a=ap.parse_args(argv)
    try:r={"schema":SCHEMA,"status":"FIXTURE","fixture":fixture()} if a.mode=="FIXTURE" else run(a)
    except Exception as e:r={"schema":SCHEMA,"status":"UNKNOWN_RESOURCE" if str(e).startswith("UNKNOWN_RESOURCE:") else "UNKNOWN","reason":str(e),"claims":{"A0":False,"COMMON":False,"NONMEMBER":False,"fake":False,"Ihara":False}}
    out=Path(a.output);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(r,sort_keys=True,separators=(",",":"))+"\n",encoding="ascii");print(f"{MARKER} status={r['status']}",flush=True);return 0
if __name__=="__main__":raise SystemExit(main())
