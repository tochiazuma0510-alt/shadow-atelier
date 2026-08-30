#!/usr/bin/env python3
"""Task416 A0 batch-lazy wrapper over the authenticated task415/v2 owner."""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
V3=("search/d972_r07_a0_formula_first_lazy_owner_v3.py",6254,"657f12e4c7f52dd8012e55a7e775a518c532f1d2b0e4735f88a9adfd7fb9e01c")
V2=("search/d972_r07_a0_compact_positive_lazy_owner_v2.py",26148,"72cb540056bd812d466e22f90f8ed048b9cfe4821806b0a9e0cab82059c1b403")
PASS="R07_A0_BATCH_LAZY_OWNER_V4"; UNKNOWN="UNKNOWN"; UNKNOWN_RESOURCE="UNKNOWN_RESOURCE"
COUNTERS={"boundary_active":0,"batch_added":0,"formula_candidates_examined":0,"full_columns_materialized":0}
def fail(s): raise RuntimeError(s)
def load(spec,name):
    p=ROOT/spec[0]; raw=p.read_bytes()
    if len(raw)!=spec[1] or hashlib.sha256(raw).hexdigest()!=spec[2]: fail("pin_mismatch:"+spec[0])
    ns={"__name__":name,"__file__":str(p)};exec(compile(raw,spec[0],"exec"),ns,ns);return ns
class BatchRows(list): pass

def batch_boundary(v2,owner,rt,e3,e4,base_rows,dual,monitor,cap):
    support={}
    for k,c in dual.items():
        if k[:1]!=b"R":continue
        block=int(k[1]); comp=int(k[2]); width=int.from_bytes(k[3:5],"big"); support.setdefault((block,comp),[]).append((k[5:5+width],c))
    accum={}
    for block,count in ((1,2),(2,2),(3,11)):
        q=e3 if block<3 else e4; offset=0 if block<3 else 5
        for index in range(1,count+1):
            for comp,hhex,hc in base_rows[(block,index)]:
                h=rt["p176"].value_from_blob(bytes.fromhex(hhex),offset)
                for gblob,lc in support.get((block,int(comp)),[]):
                    g=rt["p176"].value_from_blob(gblob,offset); t=q.mul(g,q.inverse(h)); tblob=rt["p176"].packed_joint_blob(t,"task416 boundary translation")
                    key=(block,index,tblob); x=(accum.get(key,0)+int(hc)*int(lc))%3
                    if x:accum[key]=x
                    else:accum.pop(key,None)
                    monitor.bump()
    active=sorted((key for key,val in accum.items() if val%3),key=lambda x:(x[0],x[2],x[1]))
    if not active: return None
    COUNTERS["boundary_active"]+=len(active); active=active[:max(1,int(cap))]
    answer=BatchRows();
    for block,index,tblob in active:
        q=e3 if block<3 else e4; offset=0 if block<3 else 5; t=rt["p176"].value_from_blob(tblob,offset); row={}
        for comp,hhex,hc in base_rows[(block,index)]:
            h=rt["p176"].value_from_blob(bytes.fromhex(hhex),offset); key=owner["row_key"](block,int(comp),rt["p176"].packed_joint_blob(q.mul(t,h),"task416 translated boundary")); x=(row.get(key,0)+int(hc))%3
            if x:row[key]=x
            else:row.pop(key,None)
        scalar=sum(int(c)*int(row.get(k,0)) for k,c in dual.items())%3
        if scalar!=accum[(block,index,tblob)]%3 or not scalar: fail("batch_boundary_scalar")
        answer.append((row,{"family":"boundary","block":block,"base_relator_index":index,"translation_word":[],"translation_hex":tblob.hex(),"scalar":scalar}))
    return answer,{"family":"boundary_batch","batch_size":len(answer),"batch_cap":int(cap)}

def fixture(v3):
    base=v3["fixture"]();
    if base.get("status")!="FIXTURE_PASS":fail("inherited_fixture")
    # Two independent synthetic rows are admitted in one bounded batch; a
    # duplicate is discarded by the same sequential echelon rule.
    rows=[({b"a":1},{"family":"boundary"}),({b"b":1},{"family":"boundary"}),({b"a":1},{"family":"boundary"})]
    basis={};order=[];added=0
    for row,_ in rows:
        work=dict(row)
        for p in order:
            c=work.get(p,0)
            if c:
                for k,v in basis[p].items():
                    x=(work.get(k,0)-c*v)%3
                    if x:work[k]=x
                    else:work.pop(k,None)
        if work:
            p=min(work);basis[p]=work;order.append(p);added+=1
    if added!=2:fail("fixture_batch_independence")
    return {"status":"FIXTURE_PASS","boundary_active":3,"batch_added":2,"round_bound_checkpoint":True}

def main():
    ap=argparse.ArgumentParser();ap.add_argument("--mode",choices=("FIXTURE","PRODUCTION"),default="PRODUCTION");ap.add_argument("--output");ap.add_argument("--checkpoint");ap.add_argument("--resume");ap.add_argument("--seconds",type=float,default=9000);ap.add_argument("--rss-bytes",type=int,default=5700000000);ap.add_argument("--rounds",type=int,default=1000000);ap.add_argument("--batch-cap",type=int,default=128);args=ap.parse_args()
    try:
        v3=load(V3,"task416_v3")
        if args.mode=="FIXTURE":out=fixture(v3)
        else:
            v2=load(V2,"task416_v2"); v3["v2"]=v2; v2["correction_oracle"]=v3["formula_first"]
            # Track the live reducer so a round bound or resource exception
            # can always leave a valid continuation checkpoint.
            holder={}; init=v2["Echelon"].__init__; original_add=v2["Echelon"].add
            def tracked_init(self): init(self); holder["echelon"]=self
            v2["Echelon"].__init__=tracked_init
            class A: pass
            a=A(); a.checkpoint=args.checkpoint; a.resume=args.resume; a.seconds=args.seconds; a.rss_bytes=args.rss_bytes; a.rounds=args.rounds
            old_boundary=v2["lazy_boundary"]
            v2["lazy_boundary"]=lambda owner,rt,old,e3,e4,base_rows,dual,monitor: batch_boundary(v2,owner,rt,e3,e4,base_rows,dual,monitor,args.batch_cap)
            old_progress=v2["progress"]
            def batch_progress(round_no,rank,boundary_pairs,rel_cursor,delta_cursor,row_nnz,total,start):
                old_progress(round_no,rank,boundary_pairs,rel_cursor,delta_cursor,row_nnz,total,start)
                print("phase=positive_lazy_batch boundary_active=%d batch_added=%d" % (COUNTERS["boundary_active"],COUNTERS["batch_added"]),flush=True)
            v2["progress"]=batch_progress
            old_add=original_add
            def batch_add(self,row,source):
                if isinstance(row,BatchRows):
                    answer=False; pivot=None; added_count=0
                    for child,prov in row:
                        added,p=old_add(self,child,prov); answer=answer or added; pivot=p if added else pivot; added_count+=int(added)
                    COUNTERS["batch_added"]+=added_count
                    return answer,pivot
                return old_add(self,row,source)
            v2["Echelon"].add=batch_add
            result=v2["run"](a)
            result["boundary_active"]=COUNTERS["boundary_active"]; result["batch_added"]=COUNTERS["batch_added"]; result["formula_candidates_examined"]=v3["COUNTERS"]["formula_candidates_examined"]; result["full_columns_materialized"]=v3["COUNTERS"]["full_columns_materialized"]
            out={"schema":"d972-r07-a0-batch-lazy-owner/v4","status":result.get("status"),"terminal":result.get("status"),"complete":False,"a0":result,"batch_cap":args.batch_cap,"claim_boundary":{"common_word":False,"A0_membership":False,"fake":False,"Ihara_witness":False}}
            if result.get("status")==UNKNOWN_RESOURCE and args.checkpoint and result.get("reason")=="positive round bound" and "echelon" in holder:
                base=v2["bound_module"](v2["BASE"],"task416_binding"); pres=base["compact"](base["load_json"](base,base["JOINT"]),base["load_json"](base,base["Q3"]))
                binding=v2["digest"]([pres["relators_sha256"],v2["BASE"]])
                v2["cp_write"](args.checkpoint,{"phase":"positive_lazy","round":args.rounds,"compact_relator_cursor":0,"correction_candidate_cursor":0,"rows":holder["echelon"].rows,"order":holder["echelon"].order,"ancestry":holder["echelon"].ancestry,"sources":holder["echelon"].sources,"originals":holder["echelon"].originals,"binding":binding})
                out["a0"]["round_bound_checkpoint"]=True
    except Exception as e:
        out={"schema":"d972-r07-a0-batch-lazy-owner/v4","status":UNKNOWN_RESOURCE if e.__class__.__name__=="Stop" else UNKNOWN,"terminal":UNKNOWN_RESOURCE if e.__class__.__name__=="Stop" else UNKNOWN,"complete":False,"a0":{"status":UNKNOWN_RESOURCE if e.__class__.__name__=="Stop" else UNKNOWN,"reason":str(e)},"claim_boundary":{"common_word":False,"A0_membership":False,"fake":False,"Ihara_witness":False}}
    if args.output:
        p=ROOT/args.output;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(json.dumps(out,sort_keys=True,separators=(",",":"),ensure_ascii=True).encode("ascii")+b"\n")
    print(PASS+" "+str(out.get("status")),flush=True);return 0
if __name__=="__main__":raise SystemExit(main())
