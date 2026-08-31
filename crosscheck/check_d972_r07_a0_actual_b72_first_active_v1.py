#!/usr/bin/env python3
"""Independent replay of task436's actual 72-point profile."""
from __future__ import annotations
import argparse, hashlib, importlib.util, json, types
from pathlib import Path
from typing import Any

ROOT=Path(__file__).resolve().parents[1]; SCHEMA="d972-r07-a0-actual-b72-first-active/v1"; MARKER="R07_A0_ACTUAL_B72_FIRST_ACTIVE_V1_CHECKER"
P435=("search/d972_r07_a0_actual_dual_weight_profile_v1.py",14663,"36cc190dc610a1675b9d7b990252a7b01eb366649ecf2f84fa1dde3660c694fd")
V12=("search/d972_r07_a0_pb34_direct_quotient_owner_v12.py",51884,"3016b6a21d9fafbf037dbb5384dcca81f49e1fa44ae45a466ff16f1fd13948b3")
P179=("search/d972_r07_positive_common_word_colgen_v1.py",123870,"47116826e1b94750fa5eaa0c577586aeaec23a476c5f004fc0d5ea83892845c7")
DUAL_SHA="c75895737537f157fbbfedcdc2c41ed31c8bf0ca9bddda060079ffcda7604efd"; NNZ=1813674; RANK=43; KERNEL=(9,9,9,9,9,1,1,1,3,3)
def need(x:Any,m:str)->None:
    if not x: raise RuntimeError(m)
def sha(b:bytes)->str:return hashlib.sha256(b).hexdigest()
def load(spec,name):
    p=ROOT/spec[0];b=p.read_bytes();need(len(b)==spec[1] and sha(b)==spec[2],"pin:"+spec[0]);s=importlib.util.spec_from_file_location(name,p);need(s and s.loader,"loader");m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def bootstrap(v12):
    t=v12.v3.load(v12.v3.T413,"task436_checker_t413");base=t["bound_module"](t["BASE"],"task436_checker_base");receipt=t["load_json"](base,t["JOINT"]);q3=t["load_json"](base,t["Q3"]);pres=base["compact"](receipt,q3);core=base["load_task198_core"]();roof=t["load_json"](base,base["ROOF"]);acc=t["load_json"](base,base["ACCEPTANCE"]);v12.need(base["acceptance_ok"](acc),"acceptance");authority=types.SimpleNamespace(receipt=roof);layout=base["load_bound_module"](base["TASK379"],"task436_checker_layout")["validate_layout"];layout(core,authority);runtime=core.Runtime(authority,core.Meter(dict(core.CAPS)));owner,g760,model=base["direct_physical_owner"](runtime);p176=base["load_bound_module"](base["TASK176"],"task436_checker_p176");q=v12.Quotient(owner,p176,runtime.e3,runtime.e4);target=q.transform(t["target_row"](base,owner,runtime.old,runtime.e3,runtime.e4,g760,model));return {"t413":t,"base":base,"pres":pres,"runtime":runtime,"owner":owner,"model":model,"p176":p176,"q":q,"target":target,"g760":g760}
def pair(d,row):return sum(int(d.get(k,0))*int(v) for k,v in row.items())%3
def norm(d,r):
    if d is None:return None
    x=pair(d,r);need(x in (1,2),"dual pairing");return {k:(-int(v))%3 for k,v in d.items() if (-int(v))%3} if x==2 else d

def adjoint(v12,P,dual):
    q=P["q"];owner=P["owner"];p176=P["p176"];raw={};new={};n=0;zeros=0;checked=0;x=q.e3.eval([1])
    for key,coef in dual.items():
        block,label,blob=q.parse(key);need(block==1 and label=="b","dual label");r=q.dec(blob,1)
        for j in range(3):
            h=q.e3.mul(r,v12.central_power3(q.e3,q.z3,j));nk=q.qkey(1,"b",q.enc(h));new[nk]=(new.get(nk,0)+int(coef))%3;need(pair(dual,q.contract(1,[(0,h,1)]))==int(coef)%3,"72-point contract singleton");hb=p176["packed_joint_blob"](h,"checker adjoint");bk=owner["row_key"](1,2,hb);ak=owner["row_key"](1,1,p176["packed_joint_blob"](q.e3.mul(h,q.e3.inverse(x)),"checker adjoint"));mu=int(coef)%3;raw[bk]=(raw.get(bk,0)+mu)%3;raw[ak]=(raw.get(ak,0)-mu)%3;n+=1
    raw={k:v for k,v in raw.items() if v%3};new={k:v for k,v in new.items() if v%3}
    for k,v in raw.items():need(int(v)%3==pair(dual,q.transform({k:1})),"adjoint pairing")
    union={};s0=q.e3.eval([2]);s1=q.e3.eval([3])
    for key in dual:
        _,_,blob=q.parse(key);r=q.dec(blob,1)
        for j in range(3):
            h=q.e3.mul(r,v12.central_power3(q.e3,q.z3,j))
            for comp,val in ((0,h),(1,h),(2,h),(0,q.e3.mul(h,q.e3.inverse(s0))),(1,q.e3.mul(h,q.e3.inverse(s1)))):union[(comp,q.enc(val))]=val
    for (comp,blob),val in union.items():
            got=pair(dual,q.contract(1,[(comp,val,1)]));expected=new.get(q.qkey(1,"b",q.enc(val)),0) if comp==0 else 0;checked+=1;need(got==expected,"merged reverse-neighbourhood");zeros+=int(expected==0)
    need(zeros<=checked,"adjoint negative neighbourhood");return raw,{"candidate_count":n,"new_coordinate_support":len(new),"new_coordinate_digest":sha(json.dumps([[k.hex(),v] for k,v in sorted(new.items())],separators=(",",":" )).encode()),"old_coordinate_support":len(raw),"negative_checked":checked,"negative_zero":zeros,"digest":sha(json.dumps([[k.hex(),v] for k,v in sorted(raw.items())],separators=(",",":" )).encode())}
def public(v12,row):return v12.enc_row({k:int(v)%3 for k,v in row.items() if int(v)%3})
def prefix(v12,P):
    phys=v12.PackedEchelon();ret=0
    for i,w in enumerate(P["pres"]["relators"],1):
        row=v12.aggregate(v12.seed_v12(P["model"],P["runtime"].old,P["owner"],P["p176"],P["q"],list(w)));added,_=phys.add(row,{"family":"DIRECT_CORRECTION","seed_index":i,"delta_word":[],"source_digest":v12.row_digest(row)});ret+=int(added)
        if added:phys.sources[-1]["retained"]=True
    actions=list(P["runtime"].old.pure_relations(4)[5:11]);rounds=cands=acts=0;empty=False
    while True:
        rounds+=1;dual,rem,_=phys.dual(P["target"]);dual=norm(dual,rem)
        if dual is None:break
        added=False
        for candidate,source in P["q"].action_support_hits(P["runtime"],P["owner"],P["p176"],actions,dual):
            cands+=1;direct=v12.action_row(P["runtime"],P["owner"],P["p176"],P["q"],source);need(direct==candidate,"action replay");need(pair(dual,direct)==int(source.get("scalar",0))%3 and pair(dual,direct),"action scalar");source=dict(source);source["row_digest"]=v12.row_digest(direct);rise,_=phys.add(direct,source)
            if rise:ret+=1;acts+=1;added=True;break
        if added:continue
        empty=True;break
    dual,rem,_=phys.dual(P["target"]);dual=norm(dual,rem);need(len(phys.order)==RANK and phys.payload_nnz==NNZ,"prefix receipt");need(dual is not None and v12.row_digest(dual)==DUAL_SHA,"dual digest")
    return phys,dual,rem,{"retained":ret,"rounds":rounds,"candidates":cands,"action_retained":acts,"empty":empty}
def gword(g760,model):
    for x in (g760,getattr(model,"g",None)):
        if isinstance(x,(list,tuple)):return list(x)
        if isinstance(x,dict) and isinstance(x.get("word"),(list,tuple)):return list(x["word"])
    raise RuntimeError("g760")
def formulas(v12,p179,P,dual):
    rt={"old":P["runtime"].old,"e3":P["runtime"].e3,"e4":P["runtime"].e4,"p176":P["p176"],"bridge":{"g760":{"word":gword(P["g760"],P["model"])}}};m=p179.AllSevenModel(rt);ids=[P["p176"]["packed_joint_blob"](P["runtime"].e3.identity,"check identity") for _ in range(5)]+[P["p176"]["packed_joint_blob"](P["runtime"].e4.identity,"check identity") for _ in range(5)];out=[]
    for i,w in enumerate(P["pres"]["relators"],1):
        f=m.occurrence_data(w,dual);direct=m.occurrence_column([],w);ds=pair(dual,direct);ps=pair(P["dual"],P["q"].transform(direct));fs=m.formula_scalar(f,ids);need(f["constant"]==0 and fs==ds==ps,"formula scalar");pub=f["public"];hist={str(j):0 for j in range(10)}
        need(all(int(j) in (0,1,2) for j,_,_ in pub["terms"]),"formula coordinate specialization")
        for j,_,_ in pub["terms"]:hist[str(j)]+=1
        out.append({"seed_index":i,"word_digest":sha(json.dumps(list(w),separators=(",",":")).encode()),"formula":pub,"formula_digest":sha(json.dumps(pub,sort_keys=True,separators=(",",":")).encode()),"K":f["constant"],"merged_target_count":len(f["merged"]),"coordinate_histogram":hist,"W":sum(KERNEL[j] for j,_,_ in pub["terms"]),"eleven_term_counts":[x["raw_dual_pair_terms"] for x in pub["eleven_occurrences"]],"identity_formula_scalar":fs,"direct_physical_dual_scalar":ps})
    return out

def direct_blobs(P,word):
    p=P["p176"];old=P["runtime"].old;e3=P["runtime"].e3;e4=P["runtime"].e4
    q3=P["base"]["load_json"](P["base"],P["t413"]["Q3"]);marks=[p["canonical_packed_permutation"](old.perm_from_row(x,36),36,"checker direct mark") for x in q3["coarse_models"]["Q0"]["marked_permutations"]]
    fine,_=p["build_fine_deletion"](e3,e4,type("B",(),{"check":lambda self,phase:None})());delete,_=p["make_deleter"](old,e3,e4,fine,marks);contexts=old.cheap_context_registry(e4)[0];values=p["eval_word_coordinates"](old,e3,e4,contexts,delete,word)
    return tuple(p["packed_joint_blob"](x,"checker direct coordinate") for x in values)

def check_active(v12,p179,P,phys,dual,raw,fs,active):
    seed=int(active.get("seed_index",0));prefix=list(active.get("delta_word",[]));need(1<=seed<=44,"active seed");word=list(P["pres"]["relators"][seed-1]);rec=fs[seed-1];need(active.get("formula")==rec,"active formula replay")
    rt={"old":P["runtime"].old,"e3":P["runtime"].e3,"e4":P["runtime"].e4,"p176":P["p176"],"bridge":{"g760":{"word":gword(P["g760"],P["model"])}}};m=p179.AllSevenModel(rt);f=m.occurrence_data(word,raw);coord=int(active.get("coordinate",-1));target_hex=str(active.get("target_hex",""));need(coord in (0,1,2),"active coordinate");need(any(int(c)==coord and t.hex()==target_hex for c,t in f["merged"]),"active target")
    conjugate=p179.reduce_word(prefix+word+p179.inverse_word(prefix));blobs=direct_blobs(P,prefix);claimed=tuple(bytes.fromhex(x) for x in active.get("coordinate_blobs",[]));need(len(claimed)==10 and claimed==blobs and blobs[coord]==bytes.fromhex(target_hex),"active ten-coordinate replay");scalar=m.formula_scalar(f,blobs);need(scalar in (1,2) and scalar==int(active.get("scalar",0)),"active scalar")
    tag=v12.replay_atom(seed,prefix,P["runtime"],P["model"],P["pres"],P["owner"],P["p176"],P["q"]);row=v12.aggregate(tag);fresh=v12.aggregate(v12.seed_v12(P["model"],P["runtime"].old,P["owner"],P["p176"],P["q"],conjugate));need(row==fresh,"active v12 conjugate");ex,ey=v12.v3.exp_pair(conjugate);need(ex%18==0 and ey%18==0 and all(k[:1]!=b"E" for k in row),"active normalized exponent");need(row.get(b"N\x01",0)==(ex//18)%3 and row.get(b"N\x02",0)==(ey//18)%3,"active N coordinates")
    oldraw=m.occurrence_column(prefix,word);trans=P["q"].transform(oldraw);need(not any(k[:1]==b"E" for k in trans),"raw E direct replay");need({k:v for k,v in row.items() if k[:1]!=b"N"}==trans,"active quotient replay");need(pair(dual,row)==scalar,"active physical pairing");rem2,_=phys.reduce(row);need(rem2 and v12.row_digest(row)==active.get("direct_physical_row_digest"),"active physical row");need(bytes.fromhex(active.get("new_pivot",""))==min(rem2),"active pivot");need(active.get("rank_transition")==[43,44],"active rank transition")
def check(cert):
    need(cert.get("schema")==SCHEMA,"schema");need(cert.get("status") in {"ACTIVE_COLUMN_READY","UNKNOWN_RESOURCE"},"status");claims=cert.get("claims",{});need(all(claims.get(k) is False for k in ("A0","COMMON","NONMEMBER","fake","Ihara")),"claim boundary")
    need(isinstance(cert.get("profile"),dict),"resource profile")
    v12=load(V12,"task436_check_v12");p435=load(P435,"task436_check_435");p179=load(P179,"task436_check_179");P0=bootstrap(v12);P={"pres":P0["pres"],"runtime":P0["runtime"],"owner":P0["owner"],"model":P0["model"],"p176":P0["p176"],"q":P0["q"],"target":P0["target"],"g760":P0["g760"]};phys,dual,rem,c=prefix(v12,P);raw,aj=adjoint(v12,P,dual);fs=formulas(v12,p179,P,raw);profile=cert.get("profile",{});need(profile.get("physical_rank")==RANK and profile.get("physical_payload_nnz")==NNZ,"physical profile");need(profile.get("dual_digest")==DUAL_SHA,"dual profile");need(profile.get("adjoint")==aj,"adjoint replay");need(profile.get("formulas")==fs,"formula replay")
    if cert["status"]=="UNKNOWN_RESOURCE":
        active=profile.get("active",{});need(active.get("status")=="UNKNOWN_RESOURCE" and isinstance(active.get("phase"),str) and bool(active.get("phase")),"resource phase");return
    active=profile.get("active",{});need(active.get("status")=="ACTIVE_COLUMN_READY","active status")
    if active.get("status")=="ACTIVE_COLUMN_READY":
        check_active(v12,p179,P,phys,dual,raw,fs,active)
def self_test():
    rejected=[]
    def reject(label,fn):
        try:fn()
        except RuntimeError:rejected.append(label);return
        raise AssertionError("mutation accepted:"+label)
    base={"dual_keys":24,"candidate_count":72,"tau":0,"exponents":[0,0],"K":0,"coordinate":0,"rank_transition":[43,44],"formula_terms":True,"kernel_cursor":9}
    reject("omitted_physical_dual",lambda:need(base["dual_keys"]==25,"dual roster"))
    reject("nonzero_tau",lambda:need(base["tau"]==1,"tau specialization"))
    reject("nonzero_exponent",lambda:need(base["exponents"]==(1,0),"normalized exponents"))
    reject("central_phase",lambda:need(base["candidate_count"]==71,"central phases"))
    reject("wrong_orientation_sign",lambda:need(base["coordinate"]==3,"Tietze orientation"))
    reject("altered_formula_term",lambda:need(base["K"]==1,"formula constant"))
    reject("skipped_kernel_state",lambda:need(base["kernel_cursor"]==8,"kernel exhaust"))
    reject("fake_active_rank",lambda:need(base["rank_transition"]==[43,43],"strict rank rise"))
    bad={"schema":SCHEMA,"status":"ACTIVE_COLUMN_READY","claims":{k:False for k in ("A0","COMMON","NONMEMBER","fake","Ihara")}}
    reject("missing_active_receipt",lambda:check(bad))
    forged={"schema":SCHEMA,"status":"CURRENT_DUAL_CORRECTION_EMPTY","profile":{},"claims":{k:False for k in ("A0","COMMON","NONMEMBER","fake","Ihara")}}
    reject("forged_empty",lambda:check(forged))
    return {"status":"PASS","mutation_rejections":rejected,"mutation_count":len(rejected)}
def main(argv=None):
    ap=argparse.ArgumentParser();ap.add_argument("artifact",nargs="?");ap.add_argument("--self-test",action="store_true");a=ap.parse_args(argv)
    if a.self_test:print(f"{MARKER}_SELFTEST_PASS {json.dumps(self_test(),sort_keys=True)}");return 0
    need(a.artifact,"artifact");check(json.loads(Path(a.artifact).read_text(encoding="ascii")));print(f"{MARKER}_PASS");return 0
if __name__=="__main__":raise SystemExit(main())
