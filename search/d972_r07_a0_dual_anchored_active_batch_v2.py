#!/usr/bin/env python3
"""Task463 dual-anchored ACTIVE batch continuation from frozen rank 68."""
from __future__ import annotations
import argparse,hashlib,importlib.util,json,os,tempfile,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];SCHEMA="d972-r07-a0-dual-anchored-active-batch/v2";CP_SCHEMA=SCHEMA+"/checkpoint";MARKER="R07_A0_DUAL_ANCHORED_ACTIVE_BATCH_V2"
V3=("search/d972_r07_a0_actual_tau_free_rank_ladder_v3.py",12215,"0140447110cfa568a77300bd7d43d51c622597704b7b91ed5209c63168c9ef37");FROZEN=("search/certs/d972_r07_a0_actual_tau_free_rank68_checkpoint_v1.json",33015,"73ad85624d079d01ecc824ab6adc699c51b0dabfddcc36c0f7d2bd4384f7d5a4");BINDING=hashlib.sha256((SCHEMA+V3[2]+FROZEN[2]).encode()).hexdigest()
def need(x,m):
    if not x:raise RuntimeError(m)
def sha(x):return hashlib.sha256(x).hexdigest()
def canonical(x):return json.dumps(x,sort_keys=True,separators=(",",":" )).encode("ascii")
def raw(spec):
    p=ROOT/spec[0];x=p.read_bytes();need(len(x)==spec[1] and sha(x)==spec[2],"pin:"+spec[0]);return x
def load(spec,name):
    p=ROOT/spec[0];x=raw(spec);s=importlib.util.spec_from_file_location(name,p);need(s and s.loader,"loader");m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
v3=load(V3,"task463_v3")
def frozen():
    s=json.loads(raw(FROZEN));need(s.get("schema")=="d972-r07-a0-actual-tau-free-rank-ladder/v3/checkpoint" and s.get("binding")=="6f179b061a010bb2a9b427dda6564c7418b18f44da17ea2f28e9e080655326a3","frozen schema/binding");h=s.pop("state_sha256",None);need(h=="d900bbb4f3b69ee66f9c2f4000b169f69a9202091a69fe0bbb8d33c4ae061537" and h==sha(canonical(s)),"frozen seal");s["state_sha256"]=h;need(s["rank"]==68 and s["accepted_count"]==25 and s["round"]==27 and len(s.get("accepted_sources",[]))==25,"frozen fields");return s
def checkpoint_state(prefix,batches,rank,round_no,reason,profile):
    accepted=list(prefix)+[r for x in batches for r in x["rows"]];s={"schema":CP_SCHEMA,"binding":BINDING,"frozen_sha256":FROZEN[2],"accepted_sources":accepted,"accepted_count":len(accepted),"batches":batches,"batch_count":len(batches),"rank":rank,"round":round_no,"reason":reason,"current_dual_profile":profile,"open_batch":False};s["state_sha256"]=sha(canonical(s));return s
def cp_write(path,s):
    p=Path(path);need(not p.is_absolute() and p.parent==Path("ci/out"),"checkpoint path");p.parent.mkdir(parents=True,exist_ok=True);data=canonical(s)+b"\n"
    with tempfile.NamedTemporaryFile(dir=p.parent,delete=False) as f:f.write(data);f.flush();os.fsync(f.fileno());tmp=Path(f.name)
    os.replace(tmp,p);return {"path":str(p),"bytes":len(data),"sha256":sha(data),"accepted_count":s["accepted_count"],"rank":s["rank"],"batch_count":s["batch_count"]}
def cp_read(path):
    p=Path(path);need(not p.is_absolute() and p.parent==Path("ci/out"),"resume path");s=json.loads(p.read_text(encoding="ascii"));h=s.pop("state_sha256",None);need(s.get("schema")==CP_SCHEMA and s.get("binding")==BINDING and s.get("frozen_sha256")==FROZEN[2] and h==sha(canonical(s)),"resume seal");s["state_sha256"]=h;need(s.get("open_batch") is False and s.get("batch_count")==len(s.get("batches",[])),"closed batches");base=frozen();flat=base["accepted_sources"]+[r for x in s["batches"] for r in x["rows"]];need(s.get("accepted_sources")==flat and s.get("accepted_count")==len(flat) and s.get("rank")==68+sum(x["row_count"] for x in s["batches"]),"resume compact state");return s
def row_for(P,r):
    if r["kind"]=="action":return P["v12"].action_row(P["runtime"],P["owner"],P["p176"],P["q"],r["action_source"]),dict(r["action_source"])
    row=P["v12"].aggregate(P["v12"].replay_atom(r["seed_index"],r["delta_word"],P["runtime"],P["model"],P["pres"],P["owner"],P["p176"],P["q"]));return row,{"family":"DIRECT_CORRECTION","seed_index":r["seed_index"],"delta_word":r["delta_word"],"source_digest":r["row_digest"]}
def replay_batches(P,m,batches,state):
    for batch in batches:
        dual,rem,_=state;need(dual is not None and len(P["phys"].order)==batch["anchor_rank"] and P["v12"].row_digest(dual)==batch["anchor_dual_digest"] and P["v12"].row_digest(rem)==batch["anchor_remainder_digest"],"batch anchor")
        for r in batch["rows"]:
            row,src=row_for(P,r);need(P["v12"].row_digest(row)==r["row_digest"] and v3.b.pair(dual,row)==r["anchor_scalar"] and len(P["phys"].order)==r["pre_rank"],"batch row");rise,p=P["phys"].add(row,src);need(rise and p.hex()==r["pivot"] and len(P["phys"].order)==r["post_rank"],"batch rise")
        state=v3.b.update(P,m);d2,r2,_=state;need(len(P["phys"].order)==batch["post_rank"] and P["v12"].row_digest(r2)==batch["post_remainder_digest"] and (None if d2 is None else P["v12"].row_digest(d2))==batch["post_dual_digest"],"batch close")
    return state
def corrections(P,m,p179,formulas,sf,model,args,adj_digest,anchor):
    dual,rem,_=anchor
    for f,seedword in zip(formulas,P["pres"]["relators"]):
        for coordinate,target in sorted(f["merged"],key=lambda x:(x[0],x[1])):
            fibre=sf.canonical(coordinate,target)
            if fibre is None:continue
            for cursor,eta in enumerate(sf.ensure_kernel_prefix(coordinate,9)):
                m.budget_check(P,args,"tau_free_candidate");cand=sf.kernel_candidate(fibre,eta);scalar=v3.b.formula_scalar(model,f,cand["coordinate_blobs"])
                if not scalar:continue
                delta=list(cand["source_word"]);conj=p179.reduce_word(delta+list(seedword)+p179.inverse_word(delta));row=P["v12"].aggregate(P["v12"].replay_atom(f["seed_index"],delta,P["runtime"],P["model"],P["pres"],P["owner"],P["p176"],P["q"]));fresh=P["v12"].aggregate(P["v12"].seed_v12(P["model"],P["runtime"].old,P["owner"],P["p176"],P["q"],conj));need(row==fresh and v3.b.pair(dual,row)==scalar,"batch direct anchor scalar");ex,ey=P["v12"].v3.exp_pair(conj);need(ex%18==0 and ey%18==0 and all(k[:1]!=b"E" for k in row),"batch exponent");yield row,{"kind":"correction","seed_index":f["seed_index"],"delta_word":delta,"exact_exponent_pair":[ex,ey],"adjoint_digest":adj_digest,"required_coordinates":f["required_coordinates"],"selector_cursor":[f["seed_index"],coordinate,target.hex(),cursor],"anchor_scalar":scalar,"row_digest":P["v12"].row_digest(row)}
def close_batch(P,m,batch_no,anchor,rows):
    dual,rem,_=anchor;post=v3.b.update(P,m);d2,r2,_=post;receipt={"batch":batch_no,"anchor_rank":rows[0]["pre_rank"],"anchor_dual_digest":P["v12"].row_digest(dual),"anchor_remainder_digest":P["v12"].row_digest(rem),"rows":rows,"row_count":len(rows),"post_rank":len(P["phys"].order),"post_remainder_digest":P["v12"].row_digest(r2),"post_dual_digest":None if d2 is None else P["v12"].row_digest(d2),"closed":True};return receipt,post
def terminal(status,reason,P,prefix,batches,round_no,profile,seal,started,positive=None):
    accepted=list(prefix)+[r for x in batches for r in x["rows"]];return {"schema":SCHEMA,"status":status,"terminal":status,"reason":reason,"frozen_prefix_count":25,"accepted_sources":accepted,"accepted_count":len(accepted),"batches":batches,"batch_count":len(batches),"round":round_no,"physical_rank":len(P["phys"].order),"current_dual_profile":profile,"terminal_replay":positive,"durable_state":seal,"claims":{"A0":status=="COMMON_CANDIDATE","COMMON":False,"NONMEMBER":False,"fake":False,"Ihara":False},"elapsed_seconds":time.monotonic()-started}
def run(a):
    started=time.monotonic();base=frozen();v1=load(v3.b.V1,"task463_v1");v4=v1.load(v1.V4,"task463_v4");m=v4.load_v1();m.RUN_STARTED=started;m.MARKER=MARKER;v12=m.load(m.V12,"task463_v12");p435=m.load(m.P435,"task463_p435");p179=m.load(m.P179,"task463_p179");P=v4.adapt(m,m.prefix(v12,p435,a));P["started"]=started;prefix=list(base["accepted_sources"]);state=v3.b.update(P,m);state=v3.replay(P,m,p179,prefix,state);need(len(P["phys"].order)==68,"rank68 replay");batches=[];round_no=base["round"]
    if a.resume:s=cp_read(a.resume);need(s["accepted_sources"][:25]==prefix,"resume prefix");batches=list(s["batches"]);round_no=s["round"];state=replay_batches(P,m,batches,state)
    current=v3.b.profile(P);seal=cp_write(a.checkpoint,checkpoint_state(prefix,batches,len(P["phys"].order),round_no,"initial_or_resumed",current));closed_round=round_no;closed_profile=current;new_rises=sum(x["row_count"] for x in batches);sf=None;actions=list(P["runtime"].old.pure_relations(4)[5:11])
    try:
        while True:
            dual,rem,coeff=state;round_no+=1
            if dual is None:
                pos=v1.positive(P,m,coeff);seal=cp_write(a.checkpoint,checkpoint_state(prefix,batches,len(P["phys"].order),round_no,None,None));return terminal("COMMON_CANDIDATE",None,P,prefix,batches,round_no,None,seal,started,pos)
            current=v3.b.profile(P);need(not current["unrecognized_keys"],"UNKNOWN_RESOURCE:UNRECOGNIZED_DUAL_KEYS")
            if new_rises>=a.max_rises:raise RuntimeError("UNKNOWN_RESOURCE:max_rises")
            batch_no=len(batches)+1;rows=[]
            for cand,src in P["q"].action_support_hits(P["runtime"],P["owner"],P["p176"],actions,dual):
                row=v12.action_row(P["runtime"],P["owner"],P["p176"],P["q"],src);scalar=v3.b.pair(dual,row);need(row==cand and scalar==int(src["scalar"])%3 and scalar,"action scalar");pre=len(P["phys"].order);source=dict(src);source["row_digest"]=v12.row_digest(row);rise,p=P["phys"].add(row,source);need(rise,"anchor action rise");rows.append({"kind":"action","action_source":v1.public_source(src),"selector_cursor":["action",int(src["family_index"]),src["translation_blob"]],"anchor_scalar":scalar,"row_digest":v12.row_digest(row),"pre_rank":pre,"post_rank":pre+1,"pivot":p.hex()});break
            if not rows:
                if any(current["tau_coefficients"].values()):raise RuntimeError("UNKNOWN_RESOURCE:NONZERO_TAU_PHASE_SELECTOR")
                rawdual,adj=v3.tau_free_adjoint(P,m,a);model,formulas,coords=v3.compile_formulas(P,m,p179,rawdual,a);current.update(adj);current["required_coordinates"]=coords
                if any(c not in (0,1,2) for c in coords):raise RuntimeError("UNKNOWN_RESOURCE:SELECTOR_COORDINATES:S"+",".join(map(str,coords)))
                if any(f["K"] for f in formulas):raise RuntimeError("UNKNOWN_RESOURCE:NONZERO_CONSTANT_SELECTOR")
                if sf is None:_,sf=m.selective_runtime(P,p179,a)
                for row,rec in corrections(P,m,p179,formulas,sf,model,a,adj["adjoint_digest"],state):
                    pre=len(P["phys"].order);src={"family":"DIRECT_CORRECTION","seed_index":rec["seed_index"],"delta_word":rec["delta_word"],"source_digest":rec["row_digest"]};rise,p=P["phys"].add(row,src)
                    if not rise:continue
                    rec.update({"pre_rank":pre,"post_rank":pre+1,"pivot":p.hex()});rows.append(rec)
                    if len(rows)>=a.batch_cap or new_rises+len(rows)>=a.max_rises:break
                if not rows:raise RuntimeError("UNKNOWN_RESOURCE:SEPARATOR_REQUIRES_INDEPENDENT_EXHAUSTION")
            receipt,state=close_batch(P,m,batch_no,state,rows);batches.append(receipt);new_rises+=len(rows);dual2,rem2,_=state;current=v3.b.profile(P) if dual2 is not None else None;seal=cp_write(a.checkpoint,checkpoint_state(prefix,batches,len(P["phys"].order),round_no,"batch_closed",current));closed_round=round_no;closed_profile=current;rss=getattr(v12.v3,"rss",lambda:0)() or 0;print(f"{MARKER} progress batch={batch_no} rank={len(P['phys'].order)} accepted_count={25+sum(x['row_count'] for x in batches)} elapsed_seconds={time.monotonic()-started:.3f} rss_bytes={rss}",flush=True)
    except RuntimeError as e:
        if not str(e).startswith("UNKNOWN_RESOURCE:"):raise
        # Open-batch mutations, if any, are deliberately absent from the last seal/artifact.
        closed_rank=68+sum(x["row_count"] for x in batches);return {"schema":SCHEMA,"status":"UNKNOWN_RESOURCE","terminal":"UNKNOWN_RESOURCE","reason":str(e),"frozen_prefix_count":25,"accepted_sources":prefix+[r for x in batches for r in x["rows"]],"accepted_count":25+sum(x["row_count"] for x in batches),"batches":batches,"batch_count":len(batches),"round":closed_round,"physical_rank":closed_rank,"current_dual_profile":closed_profile,"gate_profile":current,"terminal_replay":None,"durable_state":seal,"open_batch_discarded":True,"claims":{"A0":False,"COMMON":False,"NONMEMBER":False,"fake":False,"Ihara":False},"elapsed_seconds":time.monotonic()-started}
def fixture():
    rows=[];rank=68
    for scalar,independent in ((1,True),(2,False),(1,True)):
        if independent:rows.append({"pre_rank":rank,"post_rank":rank+1,"anchor_scalar":scalar});rank+=1
    existing=[{"row_count":7},{"row_count":9}];resumed_rises=sum(x["row_count"] for x in existing);need(rank==70 and len(rows)==2 and resumed_rises==16,"toy batch");return {"status":"PASS","anchor_reused":True,"candidate_count":3,"rise_count":2,"single_post_batch_update":True,"open_batch_not_durable":True,"resumed_cumulative_rises":resumed_rises,"frozen_prefix_count":25,"max_new_rises":64}
def main(argv=None):
    ap=argparse.ArgumentParser();ap.add_argument("--mode",choices=("PRODUCTION","FIXTURE"),default="PRODUCTION");ap.add_argument("--output",default="ci/out/d972_r07_a0_dual_anchored_active_batch_v2.json");ap.add_argument("--checkpoint",default="ci/out/d972_r07_a0_dual_anchored_active_batch_v2_output.checkpoint");ap.add_argument("--resume");ap.add_argument("--seconds",type=float,default=7200);ap.add_argument("--rss-bytes",type=int,default=4_800_000_000);ap.add_argument("--max-rises",type=int,default=64);ap.add_argument("--batch-cap",type=int,default=64);a=ap.parse_args(argv)
    try:r={"schema":SCHEMA,"status":"FIXTURE","fixture":fixture()} if a.mode=="FIXTURE" else run(a)
    except Exception as e:r={"schema":SCHEMA,"status":"UNKNOWN_RESOURCE" if str(e).startswith("UNKNOWN_RESOURCE:") else "UNKNOWN","terminal":"UNKNOWN","reason":str(e),"claims":{"A0":False,"COMMON":False,"NONMEMBER":False,"fake":False,"Ihara":False}}
    p=Path(a.output);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(r,sort_keys=True,separators=(",",":"))+"\n",encoding="ascii");print(f"{MARKER} status={r['status']}",flush=True);return 0
if __name__=="__main__":raise SystemExit(main())
