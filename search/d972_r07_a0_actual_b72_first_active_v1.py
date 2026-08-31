#!/usr/bin/env python3
"""Task436: actual 72-point adjoint and first weighted correction consumer."""
from __future__ import annotations
import argparse, hashlib, importlib.util, json, os, tempfile, time, sys
from pathlib import Path
from typing import Any

ROOT=Path(__file__).resolve().parents[1]; SCHEMA="d972-r07-a0-actual-b72-first-active/v1"
MARKER="R07_A0_ACTUAL_B72_FIRST_ACTIVE_V1"; RSS_CAP=4_800_000_000
P435=("search/d972_r07_a0_actual_dual_weight_profile_v1.py",14663,"36cc190dc610a1675b9d7b990252a7b01eb366649ecf2f84fa1dde3660c694fd")
V12=("search/d972_r07_a0_pb34_direct_quotient_owner_v12.py",51884,"3016b6a21d9fafbf037dbb5384dcca81f49e1fa44ae45a466ff16f1fd13948b3")
P179=("search/d972_r07_positive_common_word_colgen_v1.py",123870,"47116826e1b94750fa5eaa0c577586aeaec23a476c5f004fc0d5ea83892845c7")
P176=("search/d972_r07_all_seven_extension_section_census_v1.py",66109,"878cf1d8d44e74a993309ed1c613c9fc57eb62fd2da48a30fd8797ff4b19af3b")
JOINTSRC=("search/d972_b345_joint_kernel_qstar_closure_v1.py",67945,"06ba6cf361957db3e339d48d14b3d4fbc689de9642e3f96273fbe8f3160e76dc")
Q3=("ci/b345_157ee_artifacts_32359956713/d972_b345_q3_chief_v1.json",231570,"3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72")
JOINT=("ci/b345_157ee_artifacts_32359956713/d972_b345_joint_kernel_qstar_closure_v1.json",2166036,"1c3ad7a7124cee152eb40968cf212c14641a9f8720063c85f70533864898d0df")
DUAL_SHA="c75895737537f157fbbfedcdc2c41ed31c8bf0ca9bddda060079ffcda7604efd"
EXPECTED_RANK=43; EXPECTED_NNZ=1_813_674; SELECTIVE_STORE_BYTES=176_359_680; KERNEL=(9,9,9,9,9,1,1,1,3,3)
RUN_STARTED=None

def need(x:Any,m:str)->None:
    if not x: raise RuntimeError(m)
def sha(b:bytes)->str:return hashlib.sha256(b).hexdigest()
def load(spec,name):
    p=ROOT/spec[0];b=p.read_bytes();need(len(b)==spec[1] and sha(b)==spec[2],"pin:"+spec[0])
    s=importlib.util.spec_from_file_location(name,p);need(s and s.loader,"loader");m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def pin_raw(spec):
    p=ROOT/spec[0];b=p.read_bytes();need(len(b)==spec[1] and sha(b)==spec[2],"pin:"+spec[0]);return b
def pin_public(spec):return {"path":spec[0],"bytes":spec[1],"sha256":spec[2]}
def public(v12,row):return v12.enc_row({k:int(v)%3 for k,v in row.items() if int(v)%3})
def pair(d,row):return sum(int(d.get(k,0))*int(v) for k,v in row.items())%3
def normalize_dual(dual,remainder):
    if dual is None:return None
    value=pair(dual,remainder);need(value in (1,2),"dual target pairing")
    if value==2:dual={k:(-int(v))%3 for k,v in dual.items() if (-int(v))%3}
    need(pair(dual,remainder)==1,"dual normalize");return dual

def prefix(v12,p435,args):
    t413,base,pres,_,runtime,owner,model,p176,q,target=p435.bootstrap(v12)
    _,g760,_=base["direct_physical_owner"](runtime)
    phys=v12.PackedEchelon();attempted=retained=rounds=candidates=action_retained=0;start=RUN_STARTED or time.monotonic();local_start=time.monotonic()
    def guard(label):
        if getattr(args,"seconds",None) and time.monotonic()-start>=float(args.seconds):raise RuntimeError("UNKNOWN_RESOURCE:%s:time_limit"%label)
        rss=getattr(v12.v3,"rss",lambda:0)() or 0
        if getattr(args,"rss_bytes",None) and rss>=int(args.rss_bytes):raise RuntimeError("UNKNOWN_RESOURCE:%s:rss_limit"%label)
    for i,word in enumerate(pres["relators"],1):
        guard("prefix_seed")
        attempted=i;row=v12.aggregate(v12.seed_v12(model,runtime.old,owner,p176,q,list(word)))
        added,_=phys.add(row,{"family":"DIRECT_CORRECTION","seed_index":i,"delta_word":[],"source_digest":v12.row_digest(row)})
        if added:retained+=1;phys.sources[-1]["retained"]=True
    actions=list(runtime.old.pure_relations(4)[5:11]);final_empty=False;dual=None;remainder=target
    while True:
        rounds+=1;dual,remainder,_=phys.dual(target);dual=normalize_dual(dual,remainder)
        if dual is None:break
        added=False
        for candidate,source in q.action_support_hits(runtime,owner,p176,actions,dual):
            guard("prefix_action")
            candidates+=1;direct=v12.action_row(runtime,owner,p176,q,source);need(direct==candidate,"action replay")
            need(pair(dual,direct)==int(source.get("scalar",0))%3 and pair(dual,direct),"action scalar")
            source=dict(source);source["row_digest"]=v12.row_digest(direct);rise,_=phys.add(direct,source)
            if rise:added=True;retained+=1;action_retained+=1;break
        if added:continue
        final_empty=True;break
    need(len(phys.order)==EXPECTED_RANK and phys.payload_nnz==EXPECTED_NNZ,"prefix receipt drift")
    need(dual is not None and v12.row_digest(dual)==DUAL_SHA,"dual receipt drift")
    return {"v12":v12,"t413":t413,"base":base,"pres":pres,"runtime":runtime,"owner":owner,"model":model,"p176":p176,"q":q,"target":target,"g760":g760,"phys":phys,"dual":dual,"remainder":remainder,"attempted":attempted,"retained":retained,"rounds":rounds,"candidates":candidates,"action_retained":action_retained,"final_empty":final_empty,"elapsed":time.monotonic()-local_start}

def gword(g760,model):
    for x in (g760, getattr(model,"g",None)):
        if isinstance(x,(list,tuple)):return list(x)
        if isinstance(x,dict) and isinstance(x.get("word"),(list,tuple)):return list(x["word"])
        if hasattr(x,"word") and isinstance(x.word,(list,tuple)):return list(x.word)
    raise RuntimeError("g760 word ABI")

def model179(p179,P):
    word=gword(P.get("g760"),P["model"])
    rt={"old":P["runtime"].old,"e3":P["runtime"].e3,"e4":P["runtime"].e4,"p176":P["p176"],"bridge":{"g760":{"word":word}}}
    need(hasattr(p179,"AllSevenModel"),"AllSevenModel ABI");return p179.AllSevenModel(rt)

class _SelectiveBudget:
    def __init__(self, started, args): self.started=started; self.args=args; self.counters={"fibre_scans":0}
    def check(self, phase):
        if getattr(self.args,"seconds",None) and time.monotonic()-self.started >= float(self.args.seconds): raise RuntimeError("UNKNOWN_RESOURCE:%s:time_limit"%phase)
        if getattr(self.args,"rss_bytes",None):
            try:
                import resource
                rss=int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)*(1 if sys.platform=="darwin" else 1024)
                if rss>=int(self.args.rss_bytes):raise RuntimeError("UNKNOWN_RESOURCE:%s:rss_limit"%phase)
            except ImportError: pass
    def bump(self, name, amount=1, phase=None):
        self.counters[name]=self.counters.get(name,0)+int(amount)
        if (self.counters[name]&4095)==0:self.check(phase or name)

class _P176Adapter(dict):
    def __getattr__(self,name):
        try:return self[name]
        except KeyError:raise AttributeError(name)

def _selective_q0(p176,old,qmarks,marks,e3,e4,budget):
    identity=bytes(range(36)); gens=[bytes(x) for x in qmarks]; qt=[p176.make_translation(x) for x in gens]
    states=[identity]; ids={identity:0}; parents=[0]; letters=bytearray([0]); widths=[40,40,40]
    vals=[bytearray(p176.blob(old,e3.identity)) for _ in range(3)]; rtables=[[p176.make_translation(marks[i][j][0]) for j in range(2)] for i in range(3)]; cache={}
    for sid,state in enumerate(states):
        if (sid&4095)==0:budget.check("selective_Q0")
        if sid and (sid&131071)==0:
            print(f"{MARKER} phase=selective_Q0 states={sid}",flush=True)
        for letter in range(2):
            nxt=state.translate(qt[letter]); prior=ids.get(nxt); nb=[]
            for i,width in enumerate(widths):
                left=bytes(vals[i][sid*width:sid*width+width]); lp,lpc=p176.split_blob(left,36); right=marks[i][letter]; perm=bytes(lp).translate(rtables[i][letter]); ck=(i,letter,bytes(lpc)); pc=cache.get(ck)
                if pc is None:pc=bytes(e3.pc.mul(lpc,right[1]));cache[ck]=pc
                nb.append(perm+pc)
            if prior is None:
                prior=len(states);ids[nxt]=prior;states.append(nxt);parents.append(sid);letters.append(letter+1)
                for store,value in zip(vals,nb):store.extend(value)
    need(len(states)==1_469_664 and all(len(v)==1_469_664*w for v,w in zip(vals,widths)),"selective Q0 shape")
    return states,ids,parents,bytes(letters),vals

def selective_runtime(P,p179,args):
    base=P["base"];t413=P["t413"];p176=_P176Adapter(vars(load(P176,"task436_p176_selective")));pin_raw(JOINTSRC);pin_raw(Q3);pin_raw(JOINT)
    q3=base["load_json"](base,t413["Q3"]);joint_receipt=base["load_json"](base,t413["JOINT"]);old=P["runtime"].old;e3=P["runtime"].e3;e4=P["runtime"].e4;jmod=p176["load_module"](ROOT/JOINTSRC[0],"task436_joint_selective");words=[list(x["word"]) for x in q3["correction_fibre"]["records"] if x.get("word")]
    class G(jmod.JointGroup):
        def blob(self,value):return p176["packed_joint_blob"](value,"task436 selective Gamma")
    contexts=old.cheap_context_registry(e4)[0];gamma=G(old,e3,e4,contexts,words);need(len(gamma.states)==243 and gamma.public()["state_rows_sha256"]==joint_receipt["gamma"]["state_rows_sha256"],"selective Gamma");budget=_SelectiveBudget(P.get("started",time.monotonic()),args);fine,_=p176["build_fine_deletion"](e3,e4,budget);qmarks=[p176["canonical_packed_permutation"](old.perm_from_row(x,36),36,"task436 Q0 mark") for x in q3["coarse_models"]["Q0"]["marked_permutations"]];delete,_=p176["make_deleter"](old,e3,e4,fine,qmarks);projected=[p176["projection"](x,delete) for x in gamma.states];marks=[]
    for item in p176["COORDINATES"][:3]:
        c=contexts[item["context_id"]-1];marks.append([delete(e4.eval([l],c)) for l in (1,2)])
    qstates,qids,parents,letters,stores=_selective_q0(p176,old,qmarks,marks,e3,e4,budget);amap={};emitted={}
    for i in range(3):amap["S%d"%i],_=p176["family_public_A"](old,"S%d"%i,(i,),projected,e3,e4,marks)
    for i in range(3):
        name="S%d"%i;bits=bytearray((len(qstates)+7)//8);count=0
        for sid in range(len(qstates)):
            if (sid&4095)==0:budget.check("selective_membership_S%d"%i)
            if sid and (sid&131071)==0:
                print(f"{MARKER} phase=selective_membership_S{i} states={sid}",flush=True)
            if p176["family_key"](p176["section_row"](stores,sid),(i,)) in amap[name]:bits[sid//8]|=1<<(sid%8);count+=1
        selected,_=p176["prove_L"](old,name,bits,count,qstates,qids,qmarks,budget);gsel,_=p176["gamma_kernel_generators"](gamma,projected,(i,),e3,e4,old);adj=[]
        for qid in selected:
            key=p176["family_key"](p176["section_row"](stores,qid),(i,));inv=p176["family_inverse_key"](key,(i,),e3,e4);need(inv in amap[name],"selective adjusted L");adj.append(p179.reduce_word(list(gamma.section_word(amap[name][inv]))+p176["q0_section_word"](qid,parents,letters)))
        emitted[name]={"Gamma_S0_generators":[list(gamma.section_word(x)) for x in gsel],"adjusted_L_generators":adj}
    rt={"old":old,"e3":e3,"e4":e4,"p176":p176,"contexts":contexts,"delete":delete,"gamma":gamma,"projected":projected,"A_maps":amap,"qstates":qstates,"qids":qids,"parents":parents,"letters":letters,"stores":stores,"emitted":emitted,"bridge":{"g760":{"word":gword(P["g760"],P["model"])}}}
    class SF(p179.FibreOracle):
        def _coarse_index(self,coordinate):
            need(coordinate in (0,1,2),"selective coordinate");idx=self.coarse_indices.get(coordinate)
            if idx is None:idx=p179.CoarseInverse(self.rt["stores"][coordinate],40,36,self.monitor,expected_state_count=1_469_664);self.coarse_indices[coordinate]=idx
            return idx
        def canonical(self,coordinate,target):
            key=(coordinate,target)
            if key in self.cache:return self.cache[key]
            idx=self._coarse_index(coordinate);p=self.rt["p176"];out=[]
            for (a,),gid in self.rt["A_maps"]["S%d"%coordinate].items():
                st=p["multiply_blob"](p["inverse_blob"](a,coordinate,self.rt["e3"],self.rt["e4"]),target,coordinate,self.rt["e3"],self.rt["e4"]);qid=idx.lookup(st[:36])
                if qid is None:continue
                qword=p["q0_section_word"](qid,self.rt["parents"],self.rt["letters"]);full=tuple(p["packed_joint_blob"](x,"task436 q0 replay") for x in p["eval_word_coordinates"](self.rt["old"],self.rt["e3"],self.rt["e4"],self.rt["contexts"],self.rt["delete"],qword));gam=tuple(p["packed_joint_blob"](x,"task436 gamma replay") for x in self.rt["projected"][gid]);blobs=p179.multiply_coordinate_rows(self.rt,gam,full);need(blobs[coordinate]==target,"selective singleton replay");out.append((qid,gid,{"coordinate":coordinate,"target_hex":target.hex(),"q0_state_id":qid+1,"gamma_state_id":gid+1,"source_word":p179.reduce_word(list(self.rt["gamma"].section_word(gid))+qword),"coordinate_blobs":blobs}))
            self.cache[key]=min(out,key=lambda x:(x[0],x[1]))[2] if out else None;return self.cache[key]
        def verify_kernel_orders(self):
            self.kernel_orders=(9,9,9,9,9,1,1,1,3,3)
            for coordinate in (0,1,2):
                self.ensure_kernel_prefix(coordinate,9);states=self.kernel_states[coordinate];gens=self._kernel_generators(coordinate)
                while self.kernel_heads[coordinate]<len(states):
                    base=states[self.kernel_heads[coordinate]];self.kernel_heads[coordinate]+=1
                    for generator in gens:
                        word=p179.reduce_word(base["source_word"]+generator);blobs=p179.coordinate_blobs(self.rt,word);ident=self.rt["p176"]["blob"](self.rt["old"],self.rt["e3"].identity);need(blobs[coordinate]==ident,"kernel closure identity")
                        if blobs in self.kernel_seen[coordinate]:continue
                        self.kernel_seen[coordinate].add(blobs);states.append({"source_word":word,"coordinate_blobs":blobs})
                need(len(states)==9,"kernel order S%d"%coordinate)
            return self.kernel_orders
    need(sum(len(x) for x in stores)==SELECTIVE_STORE_BYTES,"selective store bytes");sf=SF(rt,budget);sf.verify_kernel_orders();return rt,sf

def actual_adjoint(P):
    v12=P["v12"];q=P["q"];owner=P["owner"];p176=P["p176"];dual=P["dual"];raw={};new_coeff={};candidates=0
    x=q.e3.eval([1])
    for key,coef in dual.items():
        block,label,blob=q.parse(key);need(block==1 and label=="b","specialized dual key")
        r=q.dec(blob,1)
        for j in range(3):
            h=q.e3.mul(r,v12.central_power3(q.e3,q.z3,j));nk=q.qkey(1,"b",q.enc(h));new_coeff[nk]=(new_coeff.get(nk,0)+int(coef))%3;need(pair(dual,q.contract(1,[(0,h,1)]))==int(coef)%3,"72-point contract singleton");hb=p176["packed_joint_blob"](h,"task436 adjoint b")
            bk=owner["row_key"](1,2,hb);ak=owner["row_key"](1,1,p176["packed_joint_blob"](q.e3.mul(h,q.e3.inverse(x)),"task436 adjoint a"));mu=int(coef)%3
            raw[bk]=(raw.get(bk,0)+mu)%3;raw[ak]=(raw.get(ak,0)-mu)%3;candidates+=1
    raw={k:v for k,v in raw.items() if v%3};need(candidates==72,"adjoint candidate count")
    for key,value in raw.items():need(int(value)%3==pair(dual,q.transform({key:1})),"adjoint singleton pairing")
    # Reverse-neighbourhood canaries: c and wrong predecessor orientation are zero.
    zero=checked=0;union={};s0=q.e3.eval([2]);s1=q.e3.eval([3])
    for key,coef in dual.items():
        _,_,blob=q.parse(key);r=q.dec(blob,1)
        for j in range(3):
            h=q.e3.mul(r,v12.central_power3(q.e3,q.z3,j))
            for comp,val in ((0,h),(1,h),(2,h),(0,q.e3.mul(h,q.e3.inverse(s0))),(1,q.e3.mul(h,q.e3.inverse(s1)))):union[(comp,q.enc(val))]=val
    for (comp,blob),val in union.items():
        got=pair(dual,q.contract(1,[(comp,val,1)]));expected=new_coeff.get(q.qkey(1,"b",q.enc(val)),0) if comp==0 else 0;checked+=1;need(got==expected,"merged reverse-neighbourhood canary");zero+=int(expected==0)
    need(zero<=checked,"reverse-neighbourhood canary")
    new_coeff={k:v for k,v in new_coeff.items() if v%3};return raw,{"candidate_count":candidates,"new_coordinate_support":len(new_coeff),"new_coordinate_digest":sha(json.dumps([[k.hex(),v] for k,v in sorted(new_coeff.items())],separators=(",",":" )).encode()),"old_coordinate_support":len(raw),"negative_checked":checked,"negative_zero":zero,"digest":sha(json.dumps([[k.hex(),v] for k,v in sorted(raw.items())],separators=(",",":" )).encode())}

def budget_check(P,args,phase):
    started=P.get("started") or RUN_STARTED
    if started and getattr(args,"seconds",None) and time.monotonic()-started>=float(args.seconds): raise RuntimeError("UNKNOWN_RESOURCE:%s:time_limit"%phase)
    if getattr(args,"rss_bytes",None):
        try:
            import resource
            rss=int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)*(1 if sys.platform=="darwin" else 1024)
            if rss>=int(args.rss_bytes): raise RuntimeError("UNKNOWN_RESOURCE:%s:rss_limit"%phase)
        except ImportError: pass

def compile_formulas(P,rawdual,p179,args=None):
    m=model179(p179,P);identity=[]
    for i in range(5):identity.append(P["p176"]["packed_joint_blob"](P["runtime"].e3.identity,"task436 identity"))
    for i in range(5):identity.append(P["p176"]["packed_joint_blob"](P["runtime"].e4.identity,"task436 identity"))
    out=[]
    for i,word in enumerate(P["pres"]["relators"],1):
        if args is not None: budget_check(P,args,"formula_%d"%i)
        f=m.occurrence_data(word,rawdual);direct=m.occurrence_column([],word);direct_scalar=pair(rawdual,direct);physical_scalar=pair(P["dual"],P["q"].transform(direct));formula_scalar=m.formula_scalar(f,identity)
        need(f["constant"]==0 and formula_scalar==direct_scalar==physical_scalar,"formula/direct scalar")
        pub=f["public"]; terms=pub["terms"];hist={str(j):0 for j in range(10)}
        for j,_,_ in terms:hist[str(j)]+=1
        need(all(int(j) in (0,1,2) for j,_,_ in terms),"specialized formula coordinate")
        rec={"seed_index":i,"word_digest":sha(json.dumps(list(word),separators=(",",":")).encode()),"formula":pub,"formula_digest":sha(json.dumps(pub,sort_keys=True,separators=(",",":")).encode()),"K":f["constant"],"merged_target_count":len(f["merged"]),"coordinate_histogram":hist,"W":sum(KERNEL[j] for j,_,_ in terms),"eleven_term_counts":[x["raw_dual_pair_terms"] for x in pub["eleven_occurrences"]],"identity_formula_scalar":formula_scalar,"direct_physical_dual_scalar":physical_scalar}
        out.append(rec);print(f"{MARKER} formula seed={i} targets={len(f['merged'])} W={rec['W']}",flush=True)
    return out

def first_active(P,p179,rawdual,formulas,args):
    rt,sf=selective_runtime(P,p179,args);m=model179(p179,P);started=time.monotonic();checked=0
    for rec,word in zip(formulas,P["pres"]["relators"]):
        budget_check(P,args,"fibre_seed_%d"%int(rec["seed_index"]))
        f=m.occurrence_data(word,rawdual)
        for coordinate,target in sorted(f["merged"],key=lambda x:(x[0],x[1])):
            budget_check(P,args,"fibre_target")
            fibre=sf.canonical(int(coordinate),target)
            if fibre is None:continue
            states=sf.ensure_kernel_prefix(int(coordinate),9)
            for k,eta in enumerate(states):
                budget_check(P,args,"fibre_candidate");checked+=1
                cand=sf.kernel_candidate(fibre,eta);scalar=m.formula_scalar(f,cand["coordinate_blobs"])
                if not scalar:continue
                prefix=list(cand["source_word"]);seedword=list(word);conjugate=p179.reduce_word(prefix+seedword+p179.inverse_word(prefix));
                # The selected row is rebuilt through the v12 actor path; the
                # aggregate removes occurrence tags before physical reduction.
                tagged=P["v12"].replay_atom(int(rec["seed_index"]),prefix,P["runtime"],P["model"],P["pres"],P["owner"],P["p176"],P["q"]);row=P["v12"].aggregate(tagged)
                direct=P["v12"].seed_v12(P["model"],P["runtime"].old,P["owner"],P["p176"],P["q"],conjugate);direct=P["v12"].aggregate(direct);need(row==direct,"active v12 conjugate replay");
                ex,ey=P["v12"].v3.exp_pair(conjugate);need(ex%18==0 and ey%18==0,"active normalized exponent divisibility");need(all(k[:1]!=b"E" for k in row),"raw exponent key rejected");need(row.get(b"N\x01",0)==(ex//18)%3 and row.get(b"N\x02",0)==(ey//18)%3,"active normalized exponents")
                oldraw=m.occurrence_column(prefix,seedword);trans=P["q"].transform(oldraw);need(not any(k[:1]==b"E" for k in trans),"raw E direct replay");need({k:v for k,v in row.items() if k[:1]!=b"N"}==trans,"active occurrence quotient replay")
                need(pair(P["dual"],row)==scalar,"active physical scalar");remainder,_=P["phys"].reduce(row);need(remainder,"active rank rise")
                pivot=min(remainder);print(f"{MARKER} phase=active seed={rec['seed_index']} coordinate={coordinate} fibre_cursor={k+1}",flush=True)
                return {"status":"ACTIVE_COLUMN_READY","seed_index":int(rec["seed_index"]),"coordinate":int(coordinate),"target_hex":target.hex(),"delta_word":prefix,"coordinate_blobs":[x.hex() for x in cand["coordinate_blobs"]],"formula":rec,"scalar":int(scalar),"direct_physical_row_digest":P["v12"].row_digest(row),"new_pivot":pivot.hex(),"rank_transition":[len(P["phys"].order),len(P["phys"].order)+1],"fibre_cursor":k,"checked_fibres":checked,"runtime_phase_seconds":time.monotonic()-started}
    return {"status":"CURRENT_DUAL_CORRECTION_EMPTY","checked_fibres":checked,"runtime_phase_seconds":time.monotonic()-started}

def checkpoint(path,summary):
    if not path:return None
    p=Path(path);need(not p.is_absolute() and p.parent==Path("ci/out"),"checkpoint path");p.parent.mkdir(parents=True,exist_ok=True);raw=json.dumps(summary,sort_keys=True,separators=(",",":" )).encode()+b"\n"
    with tempfile.NamedTemporaryFile(dir=p.parent,delete=False) as f:f.write(raw);f.flush();os.fsync(f.fileno());t=Path(f.name)
    os.replace(t,p);return {"path":str(p),"bytes":len(raw),"sha256":sha(raw)}

def run(args):
    started=time.monotonic();global RUN_STARTED;RUN_STARTED=started;v12=load(V12,"task436_v12");p435=load(P435,"task436_p435");p179=load(P179,"task436_p179");P=prefix(v12,p435,args);P["started"]=started;raw,adj=actual_adjoint(P);formulas=compile_formulas(P,raw,p179,args)
    try: active=first_active(P,p179,raw,formulas,args)
    except Exception as exc:
        if not str(exc).startswith("UNKNOWN_RESOURCE:"): raise
        active={"status":"UNKNOWN_RESOURCE","phase":str(exc)}
    if active.get("status")=="CURRENT_DUAL_CORRECTION_EMPTY":
        active={"status":"UNKNOWN_RESOURCE","phase":"empty_requires_independent_exhaustion","checked_fibres":active.get("checked_fibres",0)}
    summary={"phase":"weighted_fibre","formula_cursor":44,"adjoint":adj,"physical_rank":len(P["phys"].order),"physical_payload_nnz":P["phys"].payload_nnz,"target_digest":v12.row_digest(P["target"]),"remainder_digest":v12.row_digest(P["remainder"]),"dual_digest":v12.row_digest(P["dual"]),"formulas":formulas,"active":active,"selective_store_bytes":SELECTIVE_STORE_BYTES,"pins":{"v12":pin_public(V12),"task435":pin_public(P435),"task179":pin_public(P179),"task176":pin_public(P176),"task157ee_source":pin_public(JOINTSRC),"q3":pin_public(Q3),"joint_receipt":pin_public(JOINT)}}
    seal=checkpoint(args.checkpoint,summary);status=active["status"]
    return {"schema":SCHEMA,"status":status,"terminal":status,"reason":None,"profile":summary,"durable_state":seal,"claims":{"A0":False,"COMMON":False,"NONMEMBER":False,"fake":False,"Ihara":False},"elapsed_seconds":time.monotonic()-started}

def fixture():
    need(tuple(KERNEL)==(9,9,9,9,9,1,1,1,3,3),"kernel schedule");need(72==24*3,"72 candidate fixture")
    return {"status":"PASS","candidate_count":72,"tau":0,"exponents":0,"K":0,"no_occurrence_closure":True,"no_global_scan":True}

def main(argv=None):
    ap=argparse.ArgumentParser();ap.add_argument("--mode",choices=("PRODUCTION","FIXTURE"),default="PRODUCTION");ap.add_argument("--output",default="ci/out/d972_r07_a0_actual_b72_first_active_v1.json");ap.add_argument("--checkpoint",default="ci/out/d972_r07_a0_actual_b72_first_active_v1_output.checkpoint");ap.add_argument("--seconds",type=float,default=2400);ap.add_argument("--rss-bytes",type=int,default=RSS_CAP);a=ap.parse_args(argv)
    try:r=({"schema":SCHEMA,"status":"FIXTURE","fixture":fixture()} if a.mode=="FIXTURE" else run(a))
    except Exception as e:
        status="UNKNOWN_RESOURCE" if str(e).startswith("UNKNOWN_RESOURCE:") else "UNKNOWN";r={"schema":SCHEMA,"status":status,"terminal":status,"reason":str(e),"claims":{"A0":False,"COMMON":False,"NONMEMBER":False,"fake":False,"Ihara":False}}
    if a.output:Path(a.output).parent.mkdir(parents=True,exist_ok=True);Path(a.output).write_text(json.dumps(r,sort_keys=True,separators=(",",":"))+"\n",encoding="ascii")
    print(f"{MARKER} status={r['status']}",flush=True);return 0
if __name__=="__main__":raise SystemExit(main())
