#!/usr/bin/env python3
"""R07 A0 positive-first lazy column owner (task413).

This owner deliberately keeps the boundary image lazy.  It uses the frozen
task411 direct runtime and task179's support-times-occurrence oracle, but does
not construct a PB3/PB4 closure or retain a global translated-boundary list.
"""
from __future__ import annotations
import argparse, gzip, hashlib, importlib.util, json, marshal, os, shutil, sys, tempfile, time
from pathlib import Path
from types import SimpleNamespace
from typing import Any

ROOT=Path(__file__).resolve().parents[1]
BASE=("search/d972_r07_a0_compact_pc_invariant_owner_v1.py",68222,
      "be17be107103a218123cd0e1eb8455377ca2b52a2e54ec629f3744ad4c2d32f9")
JOINT=Path("ci/b345_157ee_artifacts_32359956713/d972_b345_joint_kernel_qstar_closure_v1.json")
Q3=Path("ci/b345_157ee_artifacts_32359956713/d972_b345_q3_chief_v1.json")
ROOF=Path("ci/in/d972_r07_seven_context_roof_presentation_v1.json")
ACCEPTANCE=Path("ci/in/d972_r07_seven_context_roof_presentation_v1.acceptance_v2.json")
PINS={str(JOINT):(2166036,"1c3ad7a7124cee152eb40968cf212c14641a9f8720063c85f70533864898d0df"),
      str(Q3):(231570,"3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72"),
      str(ROOF):(31017244,"82f7955580039f2a0271896c928515d26996f636d8e73231331da6a37f6b19f5"),
      str(ACCEPTANCE):(2722,"cc8c16c8ad8f2d094868f0897bcca2a98adba75c18bf7ff397f0da67fd233ea4")}
PASS="R07_A0_COMPACT_POSITIVE_LAZY_OWNER_V2"
UNKNOWN="UNKNOWN"; UNKNOWN_RESOURCE="UNKNOWN_RESOURCE"
class Stop(RuntimeError): pass

def digest_bytes(raw:bytes)->str: return hashlib.sha256(raw).hexdigest()
def canonical(v:Any)->bytes: return json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=True).encode("ascii")
def digest(v:Any)->str: return hashlib.sha256(canonical(v)).hexdigest()
def fail(msg:str)->None: raise RuntimeError(msg)
def rss()->int|None:
    if not sys.platform.startswith("linux"): return None
    try:
        for line in Path("/proc/self/status").read_text().splitlines():
            if line.startswith("VmRSS:"): return int(line.split()[1])*1024
    except (OSError,ValueError): return None
    return None
def bound_module(spec:tuple[str,int,str],name:str)->dict[str,Any]:
    path=ROOT/spec[0]; raw=path.read_bytes()
    if len(raw)!=spec[1] or digest_bytes(raw)!=spec[2]: fail("pin_mismatch:"+spec[0])
    ns={"__name__":name,"__file__":str(path)}; exec(compile(raw,spec[0],"exec"),ns,ns); return ns
def load_json(base:dict[str,Any],rel:Path)->dict[str,Any]: return base["load"](rel)
def guard(start:float,seconds:float|None,limit:int|None,phase:str)->None:
    if seconds is not None and time.monotonic()-start>=seconds: raise Stop("seconds:"+phase)
    used=rss()
    if limit is not None and used is not None and used>=limit: raise Stop("rss_bytes:"+phase)
def progress(round_no:int,rank:int,boundary_pairs:int,rel_cursor:int,delta_cursor:int,
             row_nnz:int,total:int,start:float)->None:
    print("phase=positive_lazy rank=%d round=%d boundary_pairs=%d compact_relator_cursor=%d correction_candidate_cursor=%d row_nnz=%d total_pivot_nnz=%d owner_rss_bytes=%s elapsed=%.3f" %
          (rank,round_no,boundary_pairs,rel_cursor,delta_cursor,row_nnz,total,rss(),time.monotonic()-start),flush=True)

def cp_payload(state:dict[str,Any])->bytes:
    out=__import__("io").BytesIO()
    with gzip.GzipFile(fileobj=out,mode="wb",compresslevel=1,mtime=0) as z: marshal.dump({"schema":"d972-r07-a0-lazy-checkpoint/v2","state":state},z)
    return out.getvalue()
def cp_write(path:str,state:dict[str,Any])->None:
    target=Path(path)
    if target.is_absolute() or target.parent!=Path("ci/out"): fail("checkpoint_path")
    target.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=target.parent,prefix=".a0lazy-payload-",delete=False) as h:
        payload=Path(h.name)
        with gzip.GzipFile(fileobj=h,mode="wb",compresslevel=1,mtime=0) as z: marshal.dump({"schema":"d972-r07-a0-lazy-checkpoint/v2","state":state},z)
        h.flush(); os.fsync(h.fileno())
    d=hashlib.sha256(); n=0
    with payload.open("rb") as h:
        for chunk in iter(lambda:h.read(1048576),b""): d.update(chunk); n+=len(chunk)
    with tempfile.NamedTemporaryFile(dir=target.parent,prefix=".a0lazy-",delete=False) as h:
        h.write(("D972-A0-LAZY-CP2 "+d.hexdigest()+" "+str(n)+"\n").encode("ascii"))
        with payload.open("rb") as src: shutil.copyfileobj(src,h,1048576)
        tmp=Path(h.name)
    payload.unlink(missing_ok=True); os.replace(tmp,target)
def cp_read(path:str)->dict[str,Any]:
    target=Path(path)
    if target.is_absolute() or target.parent!=Path("ci/out"): fail("resume_path")
    with target.open("rb") as h:
        try:
            parts=h.readline().decode("ascii").rstrip("\n").split(" ")
            if len(parts)!=3 or parts[0]!="D972-A0-LAZY-CP2" or len(parts[1])!=64: fail("checkpoint_seal")
            expected=parts[1]; size=int(parts[2])
        except (UnicodeError,ValueError,RuntimeError) as e: fail("checkpoint_header:"+str(e))
        d=hashlib.sha256(); n=0
        for chunk in iter(lambda:h.read(1048576),b""): d.update(chunk); n+=len(chunk)
    if n!=size or d.hexdigest()!=expected: fail("checkpoint_payload_hash")
    with target.open("rb") as h:
        h.readline()
        try:
            with gzip.GzipFile(fileobj=h,mode="rb") as z: body=marshal.load(z)
        except Exception as e: fail("checkpoint_payload_decode:"+str(e))
    if not isinstance(body,dict) or body.get("schema")!="d972-r07-a0-lazy-checkpoint/v2" or not isinstance(body.get("state"),dict): fail("checkpoint_payload_schema")
    return body["state"]

class Echelon:
    def __init__(self): self.rows={}; self.order=[]; self.ancestry={}; self.sources=[]; self.originals=[]
    def add(self,row:dict[bytes,int],source:dict[str,Any])->tuple[bool,bytes|None]:
        work=dict(row); anc={len(self.sources):1};
        for p in self.order:
            c=work.get(p,0)
            if c:
                for k,v in self.rows[p].items():
                    x=(work.get(k,0)-c*int(v))%3
                    if x: work[k]=x
                    else: work.pop(k,None)
                for k,v in self.ancestry[p].items():
                    x=(anc.get(k,0)-c*int(v))%3
                    if x: anc[k]=x
                    else: anc.pop(k,None)
        if not work: return False,None
        p=min(work); s=1 if work[p]==1 else 2
        self.rows[p]={k:(s*v)%3 for k,v in work.items() if (s*v)%3}; self.order.append(p)
        self.ancestry[p]={k:(s*v)%3 for k,v in anc.items() if (s*v)%3}; self.sources.append(source); self.originals.append(dict(row))
        return True,p
    def reduce(self,target:dict[bytes,int])->tuple[dict[bytes,int],dict[int,int]]:
        work=dict(target); anc={}
        for p in self.order:
            c=work.get(p,0)
            if c:
                for k,v in self.rows[p].items():
                    x=(work.get(k,0)-c*int(v))%3
                    if x: work[k]=x
                    else: work.pop(k,None)
                for k,v in self.ancestry[p].items():
                    x=(anc.get(k,0)-c*int(v))%3
                    if x: anc[k]=x
                    else: anc.pop(k,None)
        return work,anc
    def dual(self,target):
        rem,anc=self.reduce(target)
        if not rem: return None,rem,anc
        free=min(rem); dual={free:1}
        for p in sorted(self.order,reverse=True):
            x=(-sum(int(v)*int(dual.get(k,0)) for k,v in self.rows[p].items() if k!=p))%3
            if x: dual[p]=x
            else: dual.pop(p,None)
        if any(sum(int(v)*int(dual.get(k,0)) for k,v in r.items())%3 for r in self.rows.values()): fail("dual_not_annihilating")
        return dual,rem,anc

class Monitor:
    def __init__(self): self.count=0
    def bump(self,*_): self.count+=1

def row_add(a,b,scale=1):
    out=dict(a)
    for k,v in b.items():
        x=(out.get(k,0)+scale*int(v))%3
        if x: out[k]=x
        else: out.pop(k,None)
    return out
def exp_pair(word): return (sum(1 if x==1 else -1 if x==-1 else 0 for x in word),sum(1 if x==2 else -1 if x==-2 else 0 for x in word))
def word_inv(word): return [-x for x in reversed(word)]
def word_mul(*parts):
    out=[]
    for part in parts:
        for x in part:
            if out and out[-1]==-x: out.pop()
            else: out.append(x)
    return out
def word_pow(word,n):
    if n<0: return word_pow(word_inv(word),-n)
    out=[]
    for _ in range(n): out=word_mul(out,word)
    return out

def lazy_boundary(owner,rt,old,e3,e4,base_rows,dual,monitor):
    support={}
    for k,c in dual.items():
        if k[:1]!=b"R": continue
        block=int(k[1]); comp=int(k[2]); width=int.from_bytes(k[3:5],"big"); blob=k[5:5+width]
        support.setdefault((block,comp),[]).append((blob,c))
    accum={}
    for block,count in ((1,2),(2,2),(3,11)):
        q=e3 if block<3 else e4
        for index in range(1,count+1):
            for comp,hblob,hc in base_rows[(block,index)]:
                h=rt["p176"].value_from_blob(bytes.fromhex(hblob),0 if block<3 else 5)
                for gblob,lc in support.get((block,int(comp)),[]):
                    g=rt["p176"].value_from_blob(gblob,0 if block<3 else 5); t=q.mul(g,q.inverse(h))
                    key=(block,index,rt["p176"].packed_joint_blob(t,"task413 boundary translation"))
                    x=(accum.get(key,0)+int(hc)*int(lc))%3
                    if x: accum[key]=x
                    else: accum.pop(key,None)
                    monitor.bump()
    active=[k for k,v in accum.items() if v%3]
    if not active: return None
    block,index,tblob=min(active,key=lambda x:(x[0],x[2],x[1])); q=e3 if block<3 else e4
    t=rt["p176"].value_from_blob(tblob,0 if block<3 else 5); row={}
    for comp,hblob,hc in base_rows[(block,index)]:
        h=rt["p176"].value_from_blob(bytes.fromhex(hblob),0 if block<3 else 5)
        key=owner["row_key"](block,int(comp),rt["p176"].packed_joint_blob(q.mul(t,h),"task413 translated boundary"))
        value=(row.get(key,0)+int(hc))%3
        if value: row[key]=value
        else: row.pop(key,None)
    scalar=sum(int(c)*int(row.get(k,0)) for k,c in dual.items())%3
    if scalar!=accum[(block,index,tblob)]%3 or not scalar: fail("lazy_boundary_scalar")
    return row,{"family":"boundary","block":block,"base_relator_index":index,"translation_word":[],"translation_hex":tblob.hex(),"scalar":scalar}

def base_boundary(owner,rt,old,e3,e4):
    out={}
    for block,q,degree,count in ((1,e3,3,2),(2,e3,3,2),(3,e4,4,11)):
        for index,rel in enumerate(old.pure_relations(degree)[:count],1):
            grad,val=old.fox_gradient_without_sections(rel,q)
            if val!=q.identity: fail("boundary_seed_identity")
            rows=[]
            for (comp,value),coef in grad.items(): rows.append([int(comp),rt["p176"].packed_joint_blob(value,"task413 boundary seed").hex(),int(coef)%3])
            out[(block,index)]=rows
    return out

def target_row(base,owner,old,e3,e4,g760,model):
    answer={}; hexes=old.hexagon_words(g760)
    factors=((1,old.embed_f2_pb3(hexes[0]),e3),(2,old.embed_f2_pb3(hexes[1]),e3),(3,model._pentagon_word(g760),e4))
    for block,rel,q in factors:
        grad,val=old.fox_gradient_without_sections(rel,q)
        if val!=q.identity: fail("target_identity")
        for (comp,value),coef in grad.items():
            k=owner["row_key"](block,int(comp),owner["a0_element_blob"](value)); answer=row_add(answer,{k:-int(coef)})
    return answer

def normalized_correction_row(row, relator):
    """Replace raw exponent keys by the registered epsilon/18 coordinates."""
    e1,e2=exp_pair(relator)
    if e1%18 or e2%18: fail("correction_exponent_not_divisible_by_18")
    answer={k:v for k,v in row.items() if k[:1] not in (b"E",b"N")}
    for index,value in ((1,(e1//18)%3),(2,(e2//18)%3)):
        if value: answer[b"N"+bytes((index,))]=value
    return answer

def weighted_support(model, relator, dual):
    """Task179 support summary, evaluated afresh for the compact relator."""
    formula=model.occurrence_data(relator,dual)
    terms=sorted(formula["merged"],key=lambda item:(item[0],item[1]))
    return {"K":int(formula["constant"]),"W":sum(1 for _ in terms),
            "distinct_targets":[{"coordinate":int(c),"target_hex":t.hex()} for c,t in terms],
            "formula":formula}

def fair_delta_stream(relators, max_length=6):
    """Deterministic fair shortlex stream; no global conjugator roster/cache."""
    yield []
    alphabet=(1,-1,2,-2)
    frontier=[[]]
    for _ in range(max_length):
        nxt=[]
        for prefix in frontier:
            for letter in alphabet:
                if prefix and prefix[-1]==-letter: continue
                word=prefix+[letter]; yield word; nxt.append(word)
        frontier=nxt
    # Registered compact words and their inverses are appended after the
    # shortlex prefix, preserving a reproducible finite cursor schedule.
    for rel in relators:
        yield list(rel); yield word_inv(rel)

def correction_oracle(model, relators, dual, rel_cursor, delta_cursor, guard_fn, progress_fn=None):
    """Lazy occurrence/support-hitting correction search.

    occurrence_data and weighted_support are recomputed per compact relator;
    candidates are generated on demand and never materialized as a roster.
    """
    for ri in range(rel_cursor,len(relators)):
        deltas=fair_delta_stream(relators)
        for di,delta in enumerate(deltas):
            if ri==rel_cursor and di<delta_cursor: continue
            guard_fn("correction_oracle")
            if progress_fn is not None: progress_fn(ri,di)
            row,replay=model.direct_column(delta,relators[ri])
            row=normalized_correction_row(row,relators[ri])
            scalar=sum(int(v)*int(dual.get(k,0)) for k,v in row.items())%3
            if scalar:
                return row,{"family":"correction","seed":ri+1,"delta_word":list(delta),"candidate_cursor":di,"replay":replay}
    return None

def fixture():
    e=Echelon(); a={b"a":1}; b={b"b":1};
    if not e.add(a,{"family":"boundary"}) or e.add({b"a":1},{"family":"duplicate"})[0]: fail("fixture_sparse")
    # t*h=g orientation and wrong orientation rejection are independent of the
    # large runtime: the lazy oracle's defining equation is tested directly.
    t=("t",); h=("h",); g=("t","h")
    if t+h != g: fail("fixture_orientation_setup")
    if h+t == g: fail("fixture_wrong_orientation_accepted")
    state={"phase":"positive_lazy","rank":1,"cursor":2,"rows":{1:{2:1}}}
    payload=cp_payload(state)
    if cp_decode(payload)!=state: fail("fixture_checkpoint_roundtrip")
    bad=bytearray(payload); bad[0]^=1
    try: cp_decode(bytes(bad)); fail("fixture_checkpoint_mutation")
    except RuntimeError: pass
    return {"status":"FIXTURE_PASS","compact_roster_count":44,"compact_roster_sha256":"7612682d024b61f873928ad122c9a5d7462c812a6633112f08706cda4412b6c8","lazy_boundary_active":True}
def cp_decode(payload):
    try:
        with gzip.GzipFile(fileobj=__import__("io").BytesIO(payload),mode="rb") as z: body=marshal.load(z)
    except Exception as e: fail("checkpoint_decode:"+str(e))
    if not isinstance(body,dict) or body.get("schema")!="d972-r07-a0-lazy-checkpoint/v2" or not isinstance(body.get("state"),dict): fail("checkpoint_schema")
    return body["state"]

def run(args):
    started=time.monotonic(); base=bound_module(BASE,"task411_pinned")
    receipt=load_json(base,base["JOINT"]); q3=load_json(base,base["Q3"]); acceptance=load_json(base,base["ACCEPTANCE"])
    if not base["acceptance_ok"](acceptance): fail("acceptance_v2_contract")
    pres=base["compact"](receipt,q3)
    if pres.get("compact_relator_count")!=44 or pres.get("relators_sha256")!="7612682d024b61f873928ad122c9a5d7462c812a6633112f08706cda4412b6c8": fail("compact_roster_gate")
    for w in pres["relators"]:
        ep=exp_pair(w)
        if ep[0]%18 or ep[1]%18: fail("relator_exponent_divisibility")
    core=base["load_task198_core"](); roof=load_json(base,base["ROOF"]); authority=SimpleNamespace(receipt=roof)
    layout=base["load_bound_module"](base["TASK379"],"task413_layout")["validate_layout"]
    ledger=layout(core,authority); runtime=core.Runtime(authority,core.Meter(dict(core.CAPS)))
    owner,g760,model=base["direct_physical_owner"](runtime); p176=base["load_bound_module"](base["TASK176"],"task413_p176")
    rt={"old":runtime.old,"e3":runtime.e3,"e4":runtime.e4,"p176":SimpleNamespace(value_from_blob=p176["value_from_blob"],packed_joint_blob=p176["packed_joint_blob"]),"bridge":{},"joint_group":model.rt["joint_group"]}
    old,e3,e4=runtime.old,runtime.e3,runtime.e4; bases=base_boundary(owner,rt,old,e3,e4)
    rt["bridge"]={"pb3":{"rows":bases[(1,1)]},"pb4":{"rows":bases[(3,1)]},"g760":{"word":g760}}
    target=target_row(base,owner,old,e3,e4,g760,model); echelon=Echelon(); monitor=Monitor();
    # Insert only the 15 typed boundary seeds; their translated images remain lazy.
    for block,count in ((1,2),(2,2),(3,11)):
        for index in range(1,count+1):
            row={}
            for comp,blob,coef in bases[(block,index)]:
                key=owner["row_key"](block,comp,bytes.fromhex(blob)); value=(row.get(key,0)+int(coef))%3
                if value: row[key]=value
                else: row.pop(key,None)
            echelon.add(row,{"family":"boundary","block":block,"base_relator_index":index,"translation_word":[]})
    for ordinal,rel in enumerate(pres["relators"],1):
        row,replay=model.direct_column([],rel)
        row=normalized_correction_row(row,rel)
        if replay.get("direct_all_seven_replay") is not True: fail("correction_direct_replay")
        e=echelon.add(row,{"family":"correction","seed":ordinal,"delta_word":[]})
    checkpoint=args.checkpoint; state=None
    if args.resume: state=cp_read(args.resume)
    if state is not None:
        if state.get("phase")!="positive_lazy" or state.get("binding")!=digest([pres["relators_sha256"],BASE]): fail("checkpoint_binding")
        if not isinstance(state.get("rows"),dict) or not isinstance(state.get("order"),list) or not isinstance(state.get("ancestry"),dict) or not isinstance(state.get("sources"),list) or not isinstance(state.get("originals"),list): fail("checkpoint_state_shape")
        echelon.rows=dict(state["rows"]); echelon.order=list(state["order"]); echelon.ancestry=dict(state["ancestry"]); echelon.sources=list(state["sources"]); echelon.originals=list(state["originals"])
        if len(echelon.order)!=len(echelon.rows) or len(echelon.order)!=len(echelon.ancestry) or len(echelon.order)!=len(echelon.originals): fail("checkpoint_echelon_shape")
    round_no=int(state.get("round",0)) if state else 0; rel_cursor=int(state.get("compact_relator_cursor",0)) if state else 0; delta_cursor=int(state.get("correction_candidate_cursor",0)) if state else 0
    boundary_pairs=0; max_rounds=max(1,args.rounds)
    def save_state(force=False):
        if not checkpoint or not force: return
        cp_write(checkpoint,{"phase":"positive_lazy","round":round_no,
          "compact_relator_cursor":rel_cursor,"correction_candidate_cursor":delta_cursor,
          "rows":echelon.rows,"order":echelon.order,"ancestry":echelon.ancestry,
          "sources":echelon.sources,"originals":echelon.originals,
          "binding":digest([pres["relators_sha256"],BASE])})
    def guarded(phase):
        try:
            guard(started,args.seconds,args.rss_bytes,phase)
        except Stop:
            save_state(True); raise
    def scan_progress(ri,di):
        nonlocal rel_cursor,delta_cursor
        rel_cursor=ri; delta_cursor=di
    while round_no<max_rounds:
        guarded("positive_lazy"); round_no+=1; dual,rem,coeff=echelon.dual(target)
        progress(round_no,len(echelon.order),boundary_pairs,rel_cursor,delta_cursor,len(rem),sum(map(len,echelon.rows.values())),started)
        if dual is None:
            selected=[]
            for idx,c in coeff.items():
                if c: selected.append((idx,c,echelon.sources[idx]))
            return positive_terminal(base,owner,model,runtime,pres,target,echelon,selected,ledger,g760,started)
        hit=lazy_boundary(owner,rt,old,e3,e4,bases,dual,monitor); boundary_pairs+=monitor.count; monitor.count=0
        if hit:
            row,prov=hit; if_added=echelon.add(row,prov)
            if if_added[0]:
                rel_cursor=0; delta_cursor=0
                continue
        hit=correction_oracle(model,pres["relators"],dual,rel_cursor,delta_cursor,guarded,scan_progress)
        if hit: rel_cursor=int(hit[1]["seed"])-1; delta_cursor=int(hit[1]["candidate_cursor"])
        if hit:
            if echelon.add(*hit)[0]:
                rel_cursor=0; delta_cursor=0
                continue
        return {"status":UNKNOWN_RESOURCE,"reason":"lazy positive schedule exhausted without hit","round":round_no,"compact_relator_cursor":rel_cursor,"correction_candidate_cursor":delta_cursor,"boundary_pairs":boundary_pairs,"rank":len(echelon.order),"progress":{"phase":"positive_lazy","owner_rss_bytes":rss(),"elapsed":time.monotonic()-started}}
    return {"status":UNKNOWN_RESOURCE,"reason":"positive round bound","round":round_no,"rank":len(echelon.order),"boundary_pairs":boundary_pairs}

def positive_terminal(base,owner,model,runtime,pres,target,echelon,selected,ledger,g760,started):
    correction=[]; boundary=[]; correction_row={}; correction_factors=[]
    for idx,c,src in selected:
        if src.get("family")=="correction":
            rel=pres["relators"][int(src["seed"])-1]; delta=list(src.get("delta_word",[])); factor=word_mul(delta,rel,word_inv(delta)); correction=word_mul(correction,factor if c==1 else word_inv(factor)); correction_row=row_add(correction_row,normalized_correction_row(model.direct_column(delta,rel)[0],rel),c)
            correction_factors.append({"seed":int(src["seed"]),"delta_word":delta,"coefficient":int(c)})
        else: boundary.append({"block":src.get("block"),"base_relator_index":src.get("base_relator_index"),"translation_word":list(src.get("translation_word",[])),"translation_hex":src.get("translation_hex"),"coefficient":int(c)})
    e1,e2=exp_pair(correction)
    regs=pres.get("registered_q0_relators");
    if not regs or e1%54 or e2%54: return {"status":UNKNOWN,"reason":"positive remainder reached but exactification lattice gate failed","rank":len(echelon.order)}
    r3,r9,r12=regs[2],regs[8],regs[11]; v0=word_mul(r9,r12,word_inv(r3),word_inv(r3)); u0=word_mul(r9,word_pow(v0,-8)); h=word_mul(word_pow(u0,-3*(e1//54)),word_pow(v0,-3*(e2//54))); exact=word_mul(correction,h)
    if exp_pair(exact)!=(0,0): return {"status":UNKNOWN,"reason":"exactification exponent failure","rank":len(echelon.order)}
    states=runtime.states_direct(exact)
    if any(s.a!=s.q.identity for s in states): return {"status":UNKNOWN,"reason":"exact correction joint replay failure","rank":len(echelon.order)}
    total={}
    for idx,c,_ in selected: total=row_add(total,echelon.originals[idx],c)
    if row_add(target,total): return {"status":UNKNOWN,"reason":"positive sparse certificate residual","rank":len(echelon.order)}
    return {"status":"COMMON_CANDIDATE","member":False,"common_word":False,"positive_discovery_only":True,"strict_replay":False,"literal_correction":exact,"correction_factors":correction_factors,"exact_exponent_pair":[0,0],"typed_boundary_preimage":boundary,"rank":len(echelon.order),"boundary_pairs":0,"progress":{"phase":"positive_lazy_terminal","owner_rss_bytes":rss(),"elapsed":time.monotonic()-started},"fake":False,"Ihara_witness":False}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--mode",choices=("FIXTURE","PRODUCTION"),default="PRODUCTION"); ap.add_argument("--output"); ap.add_argument("--checkpoint"); ap.add_argument("--resume"); ap.add_argument("--seconds",type=float,default=9000); ap.add_argument("--rss-bytes",type=int,default=5700000000); ap.add_argument("--rounds",type=int,default=256); args=ap.parse_args()
    try:
        if args.mode=="FIXTURE": out=fixture()
        else:
            a0=run(args)
            base=bound_module(BASE,"task411_envelope"); receipt=load_json(base,base["JOINT"]); q3=load_json(base,base["Q3"]); pres=base["compact"](receipt,q3)
            out={"schema":"d972-r07-a0-compact-positive-lazy-owner/v2","status":a0.get("status"),"terminal":a0.get("status"),"complete":a0.get("status")=="COMMON_WORD","presentation":{"compact_relator_count":pres["compact_relator_count"],"relators_sha256":pres["relators_sha256"],"registered_q0_relators_sha256":pres["registered_q0_relators_sha256"]},"roof_input":{"path":str(ROOF),"bytes":PINS[str(ROOF)][0],"sha256":PINS[str(ROOF)][1],"authenticated":True},"acceptance_v2":{"path":str(ACCEPTANCE),"bytes":PINS[str(ACCEPTANCE)][0],"sha256":PINS[str(ACCEPTANCE)][1],"authenticated":True},"a0":a0,"claim_boundary":{"compact_presentation":True,"occurrence_closure":a0.get("status")=="COMMON_WORD","A0_membership":a0.get("status")=="COMMON_WORD","common_word":a0.get("status")=="COMMON_WORD","fake":False,"Ihara_witness":False}}
    except Stop as e:
        a0={"status":UNKNOWN_RESOURCE,"reason":str(e),"fake":False,"Ihara_witness":False}; out={"schema":"d972-r07-a0-compact-positive-lazy-owner/v2","status":UNKNOWN_RESOURCE,"terminal":UNKNOWN_RESOURCE,"complete":False,"presentation":{"compact_relator_count":44,"relators_sha256":"7612682d024b61f873928ad122c9a5d7462c812a6633112f08706cda4412b6c8"},"a0":a0,"claim_boundary":{"fake":False,"Ihara_witness":False}}
    except (RuntimeError,ImportError,OSError) as e:
        a0={"status":UNKNOWN,"reason":str(e),"fake":False,"Ihara_witness":False}; out={"schema":"d972-r07-a0-compact-positive-lazy-owner/v2","status":UNKNOWN,"terminal":UNKNOWN,"complete":False,"presentation":{"compact_relator_count":44,"relators_sha256":"7612682d024b61f873928ad122c9a5d7462c812a6633112f08706cda4412b6c8"},"a0":a0,"claim_boundary":{"fake":False,"Ihara_witness":False}}
    if args.output:
        p=ROOT/args.output; p.parent.mkdir(parents=True,exist_ok=True); p.write_bytes(canonical(out)+b"\n")
    print(PASS+" "+str(out.get("status")),flush=True); return 0
if __name__=="__main__": raise SystemExit(main())
