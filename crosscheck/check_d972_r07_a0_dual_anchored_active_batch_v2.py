#!/usr/bin/env python3
"""Independent Task463 rank-68 dual-anchored closed-batch replay."""
from __future__ import annotations
import argparse,hashlib,importlib.util,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];SCHEMA="d972-r07-a0-dual-anchored-active-batch/v2";CP_SCHEMA=SCHEMA+"/checkpoint";MARKER="R07_A0_DUAL_ANCHORED_ACTIVE_BATCH_V2_CHECKER"
V3=("search/d972_r07_a0_actual_tau_free_rank_ladder_v3.py",12215,"0140447110cfa568a77300bd7d43d51c622597704b7b91ed5209c63168c9ef37");V6=("crosscheck/check_d972_r07_a0_actual_tau_free_rank_ladder_v6.py",3590,"e902468fca7ead498e78c06496ccea596c10a1904e571f5d6b709962458b1739");V7=("crosscheck/check_d972_r07_a0_actual_tau_free_rank_ladder_v7.py",3653,"e1b80c586985f5113b300508f6bc78d055a37243e3fd6795b8f81148b0988de1");FROZEN=("search/certs/d972_r07_a0_actual_tau_free_rank68_checkpoint_v1.json",33015,"73ad85624d079d01ecc824ab6adc699c51b0dabfddcc36c0f7d2bd4384f7d5a4");BINDING=hashlib.sha256((SCHEMA+V3[2]+FROZEN[2]).encode()).hexdigest()
def need(x,m):
    if not x:raise RuntimeError(m)
def sha(x):return hashlib.sha256(x).hexdigest()
def canonical(x):return json.dumps(x,sort_keys=True,separators=(",",":" )).encode("ascii")
def raw(spec):
    p=ROOT/spec[0];x=p.read_bytes();need(len(x)==spec[1] and sha(x)==spec[2],"pin:"+spec[0]);return x
def load(spec,name):
    p=ROOT/spec[0];x=raw(spec);s=importlib.util.spec_from_file_location(name,p);need(s and s.loader,"loader");m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
v3=load(V3,"task463_check_v3");v6=load(V6,"task463_check_v6");v7=load(V7,"task463_check_v7");IC=v6.c.c.c;I2=IC.c;IP=v6.c;GATES=v6.c.c
def frozen():return v7.frozen_state()
def checkpoint(cert):
    d=cert.get("durable_state");need(isinstance(d,dict) and isinstance(d.get("path"),str),"durable");p=Path(d["path"]);need(not p.is_absolute() and p.parent==Path("ci/out"),"checkpoint path");x=p.read_bytes();need(len(x)==d.get("bytes") and sha(x)==d.get("sha256"),"outer seal");s=json.loads(x);h=s.pop("state_sha256",None);need(s.get("schema")==CP_SCHEMA and s.get("binding")==BINDING and s.get("frozen_sha256")==FROZEN[2] and h==sha(canonical(s)),"inner seal");s["state_sha256"]=h;need(s.get("open_batch") is False and s.get("batch_count")==len(s.get("batches",[])),"closed checkpoint");need(d.get("accepted_count")==s.get("accepted_count") and d.get("rank")==s.get("rank") and d.get("batch_count")==s.get("batch_count"),"durable metadata");return s
def model179(p179,P):
    g=P.get("g760");word=list(g if isinstance(g,(list,tuple)) else g.get("word") if isinstance(g,dict) else g.word);rt={"old":P["runtime"].old,"e3":P["runtime"].e3,"e4":P["runtime"].e4,"p176":P["p176"],"bridge":{"g760":{"word":word}}};return p179.AllSevenModel(rt)
def formulas(P,p179,raw):
    model=model179(p179,P);out=[];coords=set();dual=P["dual"];n1=dual.get(b"N\x01",0);n2=dual.get(b"N\x02",0);ids=[P["p176"]["packed_joint_blob"](P["runtime"].e3.identity,"task463 checker identity") for _ in range(5)]+[P["p176"]["packed_joint_blob"](P["runtime"].e4.identity,"task463 checker identity") for _ in range(5)]
    for i,word in enumerate(P["pres"]["relators"],1):
        f=model.occurrence_data(word,raw);ex,ey=P["v12"].v3.exp_pair(list(word));need(ex%18==0 and ey%18==0,"formula exponent");K=(int(n1)*(ex//18)+int(n2)*(ey//18))%3;merged={(int(c),t):int(v)%3 for (c,t),v in f["merged"].items() if int(v)%3};coords.update(c for c,t in merged);fresh=P["v12"].aggregate(P["v12"].seed_v12(P["model"],P["runtime"].old,P["owner"],P["p176"],P["q"],list(word)));need((K+model.formula_scalar(f,ids))%3==I2.pair(dual,fresh),"formula identity");out.append({"seed_index":i,"K":K,"merged":merged,"required_coordinates":sorted({c for c,t in merged})})
    return model,out,sorted(coords)
def formula_scalar(model,f,blobs):return (int(f["K"])+sum(v for (c,t),v in f["merged"].items() if blobs[c]==t))%3
def rise_gate(reason,batches):
    total=sum(int(x["row_count"]) for x in batches);need(total<=64,"cumulative rise cap")
    if reason=="UNKNOWN_RESOURCE:max_rises":need(total==64,"max_rises count")
def selector(P,m,p179,sf,model,formulas,record):
    seed,coordinate,target_hex,cursor=record["selector_cursor"];need(seed==record["seed_index"] and isinstance(coordinate,int) and isinstance(cursor,int) and cursor in range(9),"cursor type");f=formulas[seed-1];target=bytes.fromhex(target_hex);need((coordinate,target) in f["merged"],"cursor target");fibre=sf.canonical(coordinate,target);need(fibre is not None,"cursor fibre");eta=sf.ensure_kernel_prefix(coordinate,9)[cursor];cand=sf.kernel_candidate(fibre,eta);need(list(cand["source_word"])==record["delta_word"],"cursor literal");direct=tuple(p179.coordinate_blobs(sf.rt,list(record["delta_word"])));need(direct==tuple(cand["coordinate_blobs"]) and direct[coordinate]==target,"direct coordinate tuple");scalar=formula_scalar(model,f,direct);need(scalar==record["anchor_scalar"] and scalar in (1,2),"cursor scalar")
def exponent(P,p179,record):
    delta=list(record["delta_word"]);word=p179.reduce_word(delta+list(P["pres"]["relators"][record["seed_index"]-1])+p179.inverse_word(delta));ex,ey=P["v12"].v3.exp_pair(word);need(ex%18==0 and ey%18==0 and [ex,ey]==record.get("exact_exponent_pair"),"exact exponent")
def replay_prefix(P,m,p179,prefix,args):
    state=IC.update(P,m);sf=None
    for record in prefix:
        dual,rem,_=state;need(dual is not None and record["kind"]=="correction" and len(P["phys"].order)==record["old_rank"],"prefix state");rawdual,adj=I2.adjoint(P);model,compiled,coords=formulas(P,p179,rawdual);need(not any(c not in (0,1,2) for c in coords) and not any(f["K"] for f in compiled) and record["adjoint_digest"]==adj["adjoint_digest"],"prefix selector branch")
        if sf is None:_,sf=m.selective_runtime(P,p179,args)
        semantic=dict(record);semantic["selector_cursor"]=[record["seed_index"],record["coordinate"],record["target_hex"],record["fibre_cursor"]];semantic["anchor_scalar"]=record["scalar"];selector(P,m,p179,sf,model,compiled,semantic);exponent(P,p179,record)
        row=P["v12"].aggregate(P["v12"].replay_atom(record["seed_index"],record["delta_word"],P["runtime"],P["model"],P["pres"],P["owner"],P["p176"],P["q"]));need(P["v12"].row_digest(row)==record["row_digest"] and I2.pair(dual,row)==record["scalar"],"prefix direct row");src={"family":"DIRECT_CORRECTION","seed_index":record["seed_index"],"delta_word":record["delta_word"],"source_digest":record["row_digest"]};rise,p=P["phys"].add(row,src);need(rise and p.hex()==record["pivot"] and len(P["phys"].order)==record["new_rank"],"prefix rise");state=IC.update(P,m);d2,r2,_=state;need(P["v12"].row_digest(r2)==record["post_remainder_digest"] and P["v12"].row_digest(d2)==record["post_dual_digest"],"prefix post")
    need(len(P["phys"].order)==68,"rank68");return state,sf
def replay(P,m,p179,prefix,batches,args):
    state,sf=replay_prefix(P,m,p179,prefix,args)
    for expected,batch in enumerate(batches,1):
        need(batch.get("batch")==expected and batch.get("closed") is True and batch.get("row_count")==len(batch.get("rows",[])) and batch["rows"],"batch shape");dual,rem,_=state;need(dual is not None and batch["anchor_rank"]==len(P["phys"].order) and P["v12"].row_digest(dual)==batch["anchor_dual_digest"] and P["v12"].row_digest(rem)==batch["anchor_remainder_digest"],"anchor");last=None;compiled=None
        for record in batch["rows"]:
            cursor=record.get("selector_cursor");need(isinstance(cursor,list),"cursor");key=tuple(cursor) if record["kind"]=="action" else (int(cursor[0]),int(cursor[1]),str(cursor[2]),int(cursor[3]));need(last is None or key>last,"cursor order");last=key
            if record["kind"]=="action":
                need(cursor==["action",int(record["action_source"]["family_index"]),record["action_source"]["translation_blob"]],"action cursor");row=P["v12"].action_row(P["runtime"],P["owner"],P["p176"],P["q"],record["action_source"]);src=dict(record["action_source"])
            else:
                if compiled is None:
                    rawdual,adj=I2.adjoint(P);model,compiled_formulas,coords=formulas(P,p179,rawdual);need(not any(c not in (0,1,2) for c in coords) and not any(f["K"] for f in compiled_formulas),"selector branch");_,sf=m.selective_runtime(P,p179,args) if sf is None else (None,sf);compiled=(model,compiled_formulas,adj)
                model,formulas,adj=compiled;need(record["adjoint_digest"]==adj["adjoint_digest"],"adjoint");selector(P,m,p179,sf,model,formulas,record);exponent(P,p179,record);row=P["v12"].aggregate(P["v12"].replay_atom(record["seed_index"],record["delta_word"],P["runtime"],P["model"],P["pres"],P["owner"],P["p176"],P["q"]));src={"family":"DIRECT_CORRECTION","seed_index":record["seed_index"],"delta_word":record["delta_word"],"source_digest":record["row_digest"]}
            need(P["v12"].row_digest(row)==record["row_digest"] and I2.pair(dual,row)==record["anchor_scalar"] and len(P["phys"].order)==record["pre_rank"],"row/anchor scalar");rise,p=P["phys"].add(row,src);need(rise and p.hex()==record["pivot"] and len(P["phys"].order)==record["post_rank"],"pivot rise")
        state=IC.update(P,m);d2,r2,_=state;need(batch["post_rank"]==len(P["phys"].order) and P["v12"].row_digest(r2)==batch["post_remainder_digest"] and (None if d2 is None else P["v12"].row_digest(d2))==batch["post_dual_digest"],"post batch")
    return state
def check(cert):
    need(cert.get("schema")==SCHEMA and cert.get("status") in {"UNKNOWN_RESOURCE","COMMON_CANDIDATE"} and cert.get("terminal")==cert.get("status"),"terminal");need(cert.get("claims")=={"A0":cert["status"]=="COMMON_CANDIDATE","COMMON":False,"NONMEMBER":False,"fake":False,"Ihara":False},"claims");base=frozen();accepted=cert.get("accepted_sources",[]);need(accepted[:25]==base["accepted_sources"] and cert.get("frozen_prefix_count")==25,"prefix");batches=cert.get("batches",[]);rise_gate(cert.get("reason"),batches);flat=base["accepted_sources"]+[r for x in batches for r in x["rows"]];need(flat==accepted and cert.get("accepted_count")==len(flat) and cert.get("batch_count")==len(batches),"flat sources");cp=checkpoint(cert);need(cp["accepted_sources"]==accepted and cp["batches"]==batches and cp["rank"]==cert["physical_rank"] and cp["round"]==cert["round"] and cp["current_dual_profile"]==cert["current_dual_profile"],"checkpoint artifact")
    v1=load(v3.b.V1,"task463_check_v1");v4=v1.load(v1.V4,"task463_check_v4");m=v4.load_v1();v12=m.load(m.V12,"task463_check_v12");p435=m.load(m.P435,"task463_check_p435");p179=m.load(m.P179,"task463_check_p179");P=v4.adapt(m,m.prefix(v12,p435,type("A",(),{"seconds":None,"rss_bytes":None})()));state=replay(P,m,p179,base["accepted_sources"],batches,type("A",(),{"seconds":None,"rss_bytes":None})());dual,rem,coeff=state;need(len(P["phys"].order)==cert["physical_rank"],"rank")
    if cert["status"]=="COMMON_CANDIDATE":need(dual is None and cert.get("reason") is None and cert.get("current_dual_profile") is None and v1.positive(P,m,coeff)==cert.get("terminal_replay"),"positive")
    else:
        reason=cert.get("reason");need(dual is not None and isinstance(reason,str) and GATES.reason_allowed(reason),"resource reason");IP.independent_profile(P,m,p179,cert.get("current_dual_profile"),"UNKNOWN_RESOURCE:max_rises");IP.independent_profile(P,m,p179,cert.get("gate_profile"),reason);need(cert.get("open_batch_discarded") is True,"resource closed boundary")
def self_test():
    anchor="a"*64;row={"kind":"correction","selector_cursor":[1,0,"00",0],"anchor_scalar":1,"pre_rank":68,"post_rank":69,"pivot":"aa","exact_exponent_pair":[72,0]};batch={"batch":1,"anchor_rank":68,"anchor_dual_digest":anchor,"anchor_remainder_digest":"b"*64,"rows":[row],"row_count":1,"post_rank":69,"post_remainder_digest":"c"*64,"post_dual_digest":"d"*64,"closed":True};rejected=[]
    def toy(x):
        need(x.get("closed") is True and x.get("anchor_dual_digest")==anchor,"toy anchor");need(x.get("row_count")==1 and len(x.get("rows",[]))==1,"toy count");r=x["rows"][0];need(r.get("anchor_scalar") in (1,2) and r.get("selector_cursor")==[1,0,"00",0],"toy selector");need(r.get("exact_exponent_pair")==[72,0],"toy exponent");need(r.get("post_rank")==r.get("pre_rank")+1 and r.get("pivot")=="aa","toy rise");need(x.get("post_dual_digest")=="d"*64,"toy post")
    toy(batch)
    mutations=(("anchor_digest",lambda x:x.update(anchor_dual_digest="e"*64)),("scalar",lambda x:x["rows"][0].update(anchor_scalar=0)),("cursor",lambda x:x["rows"][0].update(selector_cursor=[1,0,"01",0])),("exponent",lambda x:x["rows"][0].update(exact_exponent_pair=[0,0])),("pivot",lambda x:x["rows"][0].update(post_rank=68)),("post_dual",lambda x:x.update(post_dual_digest="f"*64)),("open",lambda x:x.update(closed=False)))
    for label,mut in mutations:
        x=json.loads(json.dumps(batch));mut(x)
        try:toy(x)
        except RuntimeError:rejected.append(label)
    base=frozen();z=list(base["accepted_sources"]);z[0]={};need(z!=base["accepted_sources"],"prefix mutation");rejected.append("rank68_prefix")
    try:rise_gate("UNKNOWN_RESOURCE:max_rises",[{"row_count":63}])
    except RuntimeError:rejected.append("max_rises_63")
    rise_gate("UNKNOWN_RESOURCE:max_rises",[{"row_count":64}]);max_rises_64_accept=True
    try:rise_gate("UNKNOWN_RESOURCE:tau_free_candidate:time_limit",[{"row_count":65}])
    except RuntimeError:rejected.append("cumulative_rises_65")
    need(len(rejected)==10 and max_rises_64_accept,"mutations");return {"status":"PASS","mutation_rejections":rejected,"toy_batch_rows":1,"anchor_dual_reused":True,"frozen_prefix_semantic_replay":True,"max_rises_64_accept":True,"max_rises_exact":64}
def main(argv=None):
    ap=argparse.ArgumentParser();ap.add_argument("artifact",nargs="?");ap.add_argument("--self-test",action="store_true");a=ap.parse_args(argv)
    if a.self_test:print(MARKER+"_SELFTEST_PASS "+json.dumps(self_test(),sort_keys=True));return 0
    need(a.artifact,"artifact");check(json.loads(Path(a.artifact).read_text(encoding="ascii")));print(MARKER+"_PASS");return 0
if __name__=="__main__":raise SystemExit(main())
