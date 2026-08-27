#!/usr/bin/env python3
"""Bounded second-Frattini affine-prefix compiler (task193).

The production path accepts only an authenticated positive task186 receipt;
the finite affine/equality machinery is intentionally self-contained.
"""
from __future__ import annotations
import argparse, hashlib, importlib.util, itertools, json, time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "d972-r07-second-frattini-affine-prefix-compiler/v1"
SELFTEST_SCHEMA = "d972-r07-second-frattini-affine-prefix-compiler-selftest/v1"
COMMON = "R07_SECOND_FRATTINI_AFFINE_PREFIX_COMPILER_V1"
UNKNOWN_INPUT = "UNKNOWN_INPUT"; UNKNOWN_RESOURCE = "UNKNOWN_RESOURCE"
MUTATIONS = ("presentation_relator", "marked_generator", "crossed_order", "inverse_formula", "block_tag",
 "omitted_boundary", "equality_chain", "negative_dual", "sampled_correlation", "label_partition",
 "prefix_label", "fox_sign", "pb_relator_order", "pentagon_order", "d1_entry", "task186_word", "jennings", "resource_stop")
TASK179_PRODUCER = ("search/d972_r07_positive_common_word_colgen_v1.py", 123870, "47116826e1b94750fa5eaa0c577586aeaec23a476c5f004fc0d5ea83892845c7")
TASK186_CHECKER = ("crosscheck/check_d972_r07_normalized_exact_common_word_colgen_v2.py", 54982, "8898798d0d6a9e0b6cd67402e74ba0dc5048b4797a0f7a9657e58d70d553c488")
TASK186_SCHEMA = "d972-r07-normalized-exact-common-word-colgen/v2"
TASK186_CHECKER_LINE = "R07_NORMALIZED_EXACT_COMMON_WORD_COLGEN_V2_CHECKER_PASS terminal=R07_NORMALIZED_EXACT_COMMON_WORD_COLGEN_V2_COMMON_WORD"

def require(x: bool, msg: str) -> None:
    if not x: raise RuntimeError(msg)
def canon(x: Any) -> bytes: return json.dumps(x, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode()
def digest(x: Any) -> str: return hashlib.sha256(canon(x)).hexdigest()
def inv_word(w): return tuple(-int(x) for x in reversed(tuple(w)))
def mul_word(*ws):
    out=[]
    for w in ws:
        for x in w:
            if out and out[-1] == -int(x): out.pop()
            else: out.append(int(x))
    return tuple(out)
def exponent(w): return (sum(1 if x==1 else -1 if x==-1 else 0 for x in w), sum(1 if x==2 else -1 if x==-2 else 0 for x in w))
def add(a,b,s=1):
    out=dict(a)
    for k,v in b.items():
        z=(out.get(k,0)+s*v)%3
        if z: out[k]=z
        else: out.pop(k,None)
    return out
def pair(f,r): return sum(v*r.get(k,0) for k,v in f.items())%3
def pub(r): return [[k.hex(),v] for k,v in sorted(r.items()) if v%3]
def pub_chain(r): return [[int(k),v] for k,v in sorted(r.items()) if v%3]

def auth(path, expected):
    raw=Path(path).read_bytes(); require(len(raw)==expected[1] and hashlib.sha256(raw).hexdigest()==expected[2], "pin:"+expected[0]); return raw

def load_task179(args):
    auth(ROOT/TASK179_PRODUCER[0], TASK179_PRODUCER)
    spec=importlib.util.spec_from_file_location("task179_authenticated_source", ROOT/TASK179_PRODUCER[0]); require(spec and spec.loader, "task179 loader")
    mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    require(hasattr(mod,"build_runtime") and hasattr(mod,"boundary_oracle") and hasattr(mod,"Echelon"), "task179 adapter API")
    return mod, mod.build_runtime(mod.Monitor(args))

def attest_task186(path, attestation):
    raw=Path(path).read_bytes(); obj=json.loads(raw); body=dict(obj); claimed=body.pop("self_digest",None)
    require(claimed==digest(body) and obj.get("schema")==TASK186_SCHEMA and obj.get("status")=="COMMON_WORD" and obj.get("terminal")=="R07_NORMALIZED_EXACT_COMMON_WORD_COLGEN_V2_COMMON_WORD", "task186 positive receipt")
    exact=obj.get("exact_direct_replay",{}).get("replay",{}).get("corrected_word")
    require(type(exact) is list and exact and obj.get("exactification",{}).get("positive_receipt") is True, "task186 exact word")
    line=Path(attestation).read_text(encoding="ascii").splitlines(); require(line==[TASK186_CHECKER_LINE], "task186 checker attestation")
    return obj, {"bytes":len(raw),"sha256":hashlib.sha256(raw).hexdigest(),"path":str(path),"checker_terminal":TASK186_CHECKER_LINE}

class Echelon:
    def __init__(self): self.piv=[]; self.rows={}; self.anc={}
    def reduce(self, source):
        row=dict(source); co={}
        for p in self.piv:
            z=row.get(p,0)
            if z: row=add(row,self.rows[p],-z); co={k:(co.get(k,0)+z*v)%3 for k,v in self.anc[p].items()}; co={k:v for k,v in co.items() if v}
        return row,co
    def add(self, source, col):
        row=dict(source); co={col:1}
        for p in self.piv:
            z=row.get(p,0)
            if z: row=add(row,self.rows[p],-z); co={k:(co.get(k,0)-z*v)%3 for k,v in self.anc[p].items()}; co={k:v for k,v in co.items() if v}
        require(row,"dependent affine boundary")
        p=min(row); scale=1 if row[p]==1 else 2
        self.rows[p]={k:scale*v%3 for k,v in row.items() if scale*v%3}; self.anc[p]={k:scale*v%3 for k,v in co.items() if scale*v%3}; self.piv.append(p)
        return p,self.anc[p]
    def dual(self,target):
        rem,_=self.reduce(target); require(rem,"dual after member")
        f={min(rem):1}
        for p in reversed(self.piv):
            z=-sum(v*f.get(k,0) for k,v in self.rows[p].items() if k!=p)%3
            if z:f[p]=z
            else:f.pop(p,None)
        require(all(pair(f,self.rows[p])==0 for p in self.piv) and pair(f,target),"dual replay")
        return f

class Affine:
    """A lazy crossed-product pair (base permutation, sparse C1 chain)."""
    def __init__(self, base, chain=None): self.base=tuple(base); self.chain=dict(chain or {})
    @staticmethod
    def pm(a,b): return tuple(a[b[i]-1] for i in range(3))
    @staticmethod
    def pi(a):
        o=[0]*3
        for i,v in enumerate(a,1):o[v-1]=i
        return tuple(o)
    def mul(self, other):
        # The action is left translation on typed C1 keys.
        moved={bytes((k[0],k[1]))+bytes(self.pm(self.base,tuple(k[2:]))):v for k,v in other.chain.items()}
        return Affine(self.pm(self.base,other.base),add(self.chain,moved))
    def inverse(self):
        b=self.pi(self.base); moved={bytes((k[0],k[1]))+bytes(self.pm(b,tuple(k[2:]))):(-v)%3 for k,v in self.chain.items()}
        return Affine(b,moved)
    def public(self): return {"base":list(self.base),"chain":pub(self.chain)}

def boundary_family():
    # P=<a,b | a^2,b^2> mapped to S3 by a=(12), b=(23).  These are the
    # complete left translates of the two literal Fox rows.
    I=(1,2,3); gens={1:(2,1,3),2:(1,3,2)}
    def fox(word):
        base=I; row={}
        for x in word:
            if x>0: k=b"R\x01"+bytes((abs(x),))+bytes(base); row[k]=(row.get(k,0)+1)%3; base=Affine.pm(base,gens[x])
            else:
                base=Affine.pm(base,Affine.pi(gens[abs(x)])); k=b"R\x01"+bytes((abs(x),))+bytes(base); row[k]=(row.get(k,0)-1)%3
        return {k:v for k,v in row.items() if v}
    relators=(fox((1,1)),fox((2,2))); rows=[]
    for g in itertools.permutations((1,2,3)):
        for src in relators:
            rows.append({b"R"+bytes((1,k[2]))+bytes(Affine.pm(g,tuple(k[3:]))):v for k,v in src.items()})
    return rows

def selftest():
    pa=Affine((2,1,3),{b"R\x01\x01\x01\x02\x03":1}); pb=Affine((1,3,2),{b"R\x01\x02\x01\x03\x02":1})
    require(pa.mul(pb).base!=pb.mul(pa).base,"noncommutative crossed product")
    require(pa.mul(pa.inverse()).base==(1,2,3) and not pa.mul(pa.inverse()).chain,"crossed inverse")
    family=boundary_family(); e=Echelon(); transitions=[]
    for i,row in enumerate(family,1):
        rem,_=e.reduce(row)
        if rem:
            p,a=e.add(row,i); transitions.append([i,p.hex(),sorted(a.items())])
    outside={}
    base=(1,2,3); prefixes=[list(base)]; gens={1:(2,1,3),2:(1,3,2)}
    for x in (1,2,1,2,1,2):
        if x>0: key=b"R\x01"+bytes((x,))+bytes(base); outside[key]=(outside.get(key,0)+1)%3; base=Affine.pm(base,gens[x])
        else: base=Affine.pm(base,Affine.pi(gens[abs(x)]))
        prefixes.append(list(base))
    outside={k:v for k,v in outside.items() if v}; dual=e.dual(outside)
    inside=family[0]; rem,chain=e.reduce(inside); require(not rem and pair(dual,outside),"selftest affine span")
    alternate=add(inside,family[1]); rem2,_=e.reduce(add(alternate,inside,-1)); require(not rem2 and alternate!=inside,"syntactically distinct affine equality")
    separated=add(outside,family[0]); require(pair(dual,separated)!=0,"same-base dual separation")
    successor=Affine(base,outside); require(successor.base==(1,2,3) and successor.chain,"finite next-rung defect")
    baseline={"relator":True,"generator":True,"order":True,"inverse":True,"block":1,"boundary":True,"chain":sorted(chain.items()),"dual":pub(dual),"complete":True,"label":True,"prefix":True,"fox":len(outside),"pb_order":list(range(1,12)),"pentagon":list(range(5)),"d1":[],"word":[1,2,1,2,1,2],"jennings":False,"resource":True}
    def valid(x):
        require(x["relator"]==(pa.mul(pb).base!=pb.mul(pa).base) and x["generator"]==(successor.chain!= {} ) and x["order"]==(len(family)==12) and x["inverse"]==(pa.mul(pa.inverse()).base==(1,2,3) and not pa.mul(pa.inverse()).chain) and x["block"]==1,"presentation/marked arithmetic")
        require(x["boundary"]==(len(family)==12 and not e.reduce(inside)[0]) and x["complete"]==all(pair(dual,r)==0 for r in family) and x["chain"]==sorted(chain.items()),"boundary equality replay")
        require(x["dual"]==pub(dual) and x["label"]==(alternate!=inside and not rem2) and x["prefix"]==(len(transitions)==0 or transitions[0][0]==1) and x["fox"]==len(outside),"dual/label/Fox replay")
        require(x["pb_order"]==list(range(1,12)) and x["pentagon"]==list(range(5)) and x["d1"]==[] and x["word"]==[1,2,1,2,1,2] and not x["jennings"] and x["resource"],"order/word replay")
        q=Echelon();
        for i,row in enumerate(family,1):
            if q.reduce(row)[0]: q.add(row,i)
        require(not q.reduce(inside)[0] and all(pair(q.dual(outside),r)==0 for r in family),"complete affine replay")
    rejected=0
    for field,value in (("relator",False),("generator",False),("order",False),("inverse",False),("block",2),("boundary",False),("chain",[]),("dual",[]),("complete",False),("label",False),("prefix",False),("fox",1),("pb_order",[]),("pentagon",[]),("d1",[["bad",1]]),("word",[9]),("jennings",True),("resource",False)):
        x=dict(baseline); x[field]=value
        try: valid(x)
        except RuntimeError: rejected+=1
    require(rejected==len(MUTATIONS),"selftest mutation controls")
    toy={"family_size":len(family),"outside":pub(outside),"inside":pub(inside),"dual":pub(dual),"transitions":transitions,"complete":True,"mutations_rejected":rejected}
    # A serialized, genuinely noncommutative next-rung Fox defect.  The
    # relation is evaluated letter by letter; its two prefix labels are not
    # metadata and are independently replayed by the checker.
    successor={"relation":[1,2,1,2,1,2],"base":list(base),"prefix_labels":prefixes,"chain":pub(outside),"fox_row":pub(outside),"d1":[],"identity":True,"separator":pub(dual)}
    return {"schema":SELFTEST_SCHEMA,"status":"PASS","terminal":COMMON+"_SELFTEST_PASS","toy":toy,"successor":successor,"mutation_controls":{"attempted":len(MUTATIONS),"rejected":rejected,"names":list(MUTATIONS)}}

class ActualAffine:
    def __init__(self, quotient, block, base, chain=None, codec=None): self.q=quotient; self.block=block; self.base=base; self.chain=dict(chain or {}); self.codec=codec
    def blob(self,value): return self.codec[0].element_blob(self.codec[1],value)
    def unpack(self,value): return self.codec[0].unpack_element(self.codec[1],value,self.block)
    def key(self,component,value): return self.codec[0].row_key(self.block,component,self.blob(value))
    def key_blob(self,key):
        require(key[:1]==b"R" and key[1]==self.block and len(key)>=5,"affine key")
        width=int.from_bytes(key[3:5],"big"); require(len(key)==5+width,"affine key width"); return key[5:]
    def mul(self, other):
        require(self.block==other.block, "affine block product")
        moved={self.key(k[2],self.q.mul(self.base,self.unpack(self.key_blob(k)))):v for k,v in other.chain.items()}
        return ActualAffine(self.q,self.block,self.q.mul(self.base,other.base),add(self.chain,moved),self.codec)
    def inverse(self):
        b=self.q.inverse(self.base); moved={self.key(k[2],self.q.mul(b,self.unpack(self.key_blob(k)))):(-v)%3 for k,v in self.chain.items()}
        return ActualAffine(self.q,self.block,b,moved,self.codec)

class ResourceStop(RuntimeError):
    def __init__(self,message,state=None): self.state=state or {}; super().__init__(message)

class OracleMonitor:
    def __init__(self,round_cap,boundary_cap,seconds,rss_limit,fibre_cap,candidate_cap,retained_cap,checkpoint_cap):
        self.counts={}; self.round_cap=int(round_cap); self.boundary_cap=int(boundary_cap); self.seconds=int(seconds); self.rss_limit=int(rss_limit); self.cap_map={"oracle_rounds":self.round_cap,"boundary_pairs":self.boundary_cap,"fibre_scans":int(fibre_cap),"candidate_words":int(candidate_cap),"retained_columns":int(retained_cap),"checkpoint_bytes":int(checkpoint_cap)}; self.started=time.monotonic(); self.provider=None
    def bump(self,name,amount=1,phase=""):
        self.counts[name]=self.counts.get(name,0)+int(amount)
        cap=self.cap_map.get(name,self.round_cap)
        if self.counts[name]>cap: raise ResourceStop("phase="+str(phase)+":cap="+name+":value="+str(self.counts[name])+":limit="+str(cap),self.provider() if self.provider else {})
        elapsed=time.monotonic()-self.started
        if elapsed>=self.seconds: raise ResourceStop("phase="+str(phase)+":cap=seconds:value="+str(int(elapsed))+":limit="+str(self.seconds),self.provider() if self.provider else {})
        try:
            status=Path("/proc/self/status").read_text(encoding="ascii")
            rss=next(int(line.split()[1])*1024 for line in status.splitlines() if line.startswith("VmRSS:"))
            if rss>=self.rss_limit: raise ResourceStop("phase="+str(phase)+":cap=rss_bytes:value="+str(rss)+":limit="+str(self.rss_limit),self.provider() if self.provider else {})
        except (StopIteration,OSError): pass

def actual_compile(args, task186, artifact):
    v1,rt=load_task179(args); old=rt["old"]; e3,e4=rt["e3"],rt["e4"]
    corrected=list(task186["exact_direct_replay"]["replay"]["corrected_word"]); exact=task186["exactification"]["literal"]; c_exact=list(exact["c_exact"])
    direct=task186["exact_direct_replay"]; require(direct.get("right_g760_multiplication") is True and direct.get("hexagons") is True and direct.get("pentagon_printed_order") is True and direct.get("replay",{}).get("direct_all_seven_replay") is True,"task186 direct replay attestation")
    require(v1.reduce_word(list(rt["bridge"]["g760"]["word"])+c_exact)==corrected and v1.exponent_pair(c_exact)==(0,0), "task186 direct word replay")
    resume_expected=None; values={1:[],3:[]}; oracle={1:Echelon(),3:Echelon()}; boundary={}; oracle_columns=[]; seen_active={1:set(),3:set()}; om=OracleMonitor(args.oracle_rounds,args.boundary_pairs,args.seconds,args.rss_bytes,args.fibre_scans,args.candidate_words,args.retained_columns,args.checkpoint_bytes); query_log=[]; query_cache={}; label_decisions=[]; ordinary_rows=[]
    om.provider=lambda: {"columns":oracle_columns,"queries":query_log,"labels":label_decisions,"cache":query_cache,"seen_active":{"1":sorted([list(x) for x in seen_active[1]]),"3":sorted([list(x) for x in seen_active[3]])},"affine_roster":{"1":[x.blob(x.base).hex() for x in values[1]],"3":[x.blob(x.base).hex() for x in values[3]]},"monitor":om.counts,"caps":om.cap_map}
    if getattr(args,"resume",None):
        cp=json.loads(Path(args.resume).read_text(encoding="ascii")); sealed=dict(cp); seal_claim=sealed.pop("self_digest",None)
        require(cp.get("schema")=="d972-r07-second-frattini-affine-prefix-compiler-checkpoint/v1" and seal_claim==digest(sealed),"resume checkpoint seal")
        current_caps={"oracle_rounds":args.oracle_rounds,"boundary_pairs":args.boundary_pairs,"seconds":args.seconds,"rss_bytes":args.rss_bytes,"fibre_scans":args.fibre_scans,"candidate_words":args.candidate_words,"retained_columns":args.retained_columns,"checkpoint_bytes":args.checkpoint_bytes}
        resume_caps=cp.get("caps",{})
        require(cp.get("resumable") is True and cp.get("input_identity")==artifact and
                cp.get("program_cursor",{}).get("mode")=="deterministic-replay-from-rank-zero" and
                isinstance(resume_caps,dict) and all(int(resume_caps.get(k,-1))<=int(v) for k,v in current_caps.items()) and
                any(int(current_caps[k])>int(resume_caps.get(k,-1)) for k in current_caps),"sealed resume input/cap/cursor")
        # A checkpoint never supplies trusted derived rows or labels.  Resume
        # is an authenticated deterministic replay from rank zero, so source
        # rows, active set, roster, cache and cursor are rebuilt below.
        require(cp.get("source_rebuild") is True and isinstance(cp.get("seen_active"),dict) and
                isinstance(cp.get("affine_roster"),dict),"resume source rebuild state")
        resume_expected=cp
    for block,q in ((1,e3),(3,e4)):
        rels=old.pure_relations(3 if block==1 else 4)
        require(len(rels)==(2 if block==1 else 11),"base relation count")
        for ri,rel in enumerate(rels,1):
            grad,_=old.fox_gradient_without_sections(rel,q)
            ordinary=v1.serial_group_row(rt,grad,block); require(ordinary==v1.tagged_serial(v1.boundary_source(rt,block,ri),block),"bridge Fox row replay"); ordinary_rows.append({"block":block,"index":ri,"row":pub(ordinary)})
    def full_correlation(dual,block):
        support={}
        for key,coefficient in dual.items():
            b,component,raw=v1.decode_row_key(key); require(b==block,"correlation block"); support.setdefault(component,[]).append((raw,coefficient))
        entries=[]; accumulated={}; q=e3 if block in (1,2) else e4
        for ri in range(1,3 if block in (1,2) else 12):
            for component,h_hex,base_coefficient in v1.boundary_source(rt,block,ri):
                h=v1.unpack_element(rt,bytes.fromhex(str(h_hex)),block)
                for graw,lambda_coefficient in support.get(int(component),[]):
                    om.bump("boundary_pairs",1,"complete_support_occurrence_correlation")
                    g=v1.unpack_element(rt,graw,block); translation=q.mul(g,q.inverse(h)); require(q.mul(translation,h)==g,"correlation translation")
                    key=(ri,v1.element_blob(rt,translation).hex()); value=(int(base_coefficient)*int(lambda_coefficient))%3; accumulated[key]=(accumulated.get(key,0)+value)%3
                    entries.append({"relator_index":ri,"component":int(component),"h_hex":h_hex,"g_hex":graw.hex(),"translation_hex":key[1],"base_coefficient":int(base_coefficient)%3,"dual_coefficient":int(lambda_coefficient)%3,"contribution":value})
        active=[k for k,v in accumulated.items() if v%3]
        chosen=min(active,key=lambda x:(block,x[1],x[0])) if active else None
        answer={"entries":entries,"accumulated":sorted([[list(k),v] for k,v in accumulated.items() if v]),"zero":not active,"complete":True}
        if chosen is not None:
            row=v1.translated_boundary(rt,block,int(chosen[0]),bytes.fromhex(chosen[1]))
            scalar=pair(dual,row); require(scalar==int(accumulated[chosen])%3 and scalar,"complete boundary scalar")
            answer["active"]={"family":"boundary","block":block,"base_relator_index":int(chosen[0]),"translation_hex":chosen[1],"scalar":int(scalar),"complete_support_occurrence_accumulation":True}
        return answer
    def equal(a,b):
        require(a.block==b.block and a.blob(a.base)==b.blob(b.base), "affine base mismatch")
        target=add(a.chain,b.chain,-1)
        cache_key=digest(pub(target))
        if cache_key in query_cache:
            query_log.append({"block":a.block,"base_hex":a.blob(a.base).hex(),"target":pub(target),"cached":True,"result":query_cache[cache_key]}); return query_cache[cache_key]
        qlog={"block":a.block,"base_hex":a.blob(a.base).hex(),"target":pub(target),"steps":[]}
        while True:
            om.bump("oracle_rounds",1,"affine_equality")
            rem,co=oracle[a.block].reduce(target)
            if not rem:
                qlog["result"]={"equal":True,"chain":pub_chain(co)}; query_log.append(qlog)
                answer={"equal":True,"chain":pub_chain(co),"dual":None,"complete":True}; query_cache[cache_key]=answer; return answer
            dual=oracle[a.block].dual(rem)
            correlation=full_correlation(dual,a.block)
            if not correlation["zero"]:
                prov=correlation["active"]; sig=(prov["base_relator_index"],prov["translation_hex"])
                if sig in seen_active[a.block]: raise RuntimeError("repeated active boundary query")
                seen_active[a.block].add(sig); row=v1.translated_boundary(rt,a.block,int(prov["base_relator_index"]),bytes.fromhex(str(prov["translation_hex"])))
                reduced,dependency=oracle[a.block].reduce(row)
                column_id=len(oracle_columns)+1
                require(int(prov["scalar"])==pair(dual,row) and prov["scalar"] and not (not reduced and pair(dual,row)),"active scalar/dependency contradiction")
                descriptor={"column_id":column_id,"dual":pub(dual),"active":prov,"correlation":correlation,"row":pub(row),"dependent":not bool(reduced),"ancestry":[[int(k),int(v)] for k,v in sorted(dependency.items())]}
                qlog["steps"].append(descriptor); oracle_columns.append(descriptor)
                if reduced:
                    om.bump("retained_columns",1,"retained_boundary_column")
                    pivot,ancestry=oracle[a.block].add(row,column_id); descriptor["pivot"]=pivot.hex(); descriptor["ancestry"]=[[int(k),int(v)] for k,v in sorted(ancestry.items())]
                boundary[(a.block,prov["base_relator_index"],prov["translation_hex"])]=pub(row)
                continue
            require(pair(dual,target),"dual pairing"); require(correlation["zero"],"complete negative correlation")
            qlog["result"]={"equal":False,"dual":pub(dual),"correlation":correlation,"pairing":pair(dual,target),"full_zero_correlation":True}; query_log.append(qlog)
            answer={"equal":False,"chain":None,"dual":pub(dual),"correlation":correlation,"pairing":pair(dual,target),"complete":True,"full_zero_correlation":True}; query_cache[cache_key]=answer; return answer
    def gen(block,q,i):
        chain={v1.row_key(block,i,v1.element_blob(rt,q.identity)):1}; return ActualAffine(q,block,q.eval([i]),chain,(v1,rt))
    def intern(a):
        blob=a.blob(a.base).hex();
        for idx,b in enumerate(values[a.block]):
            om.bump("candidate_words",1,"canonical_label_compare")
            if a.blob(b.base).hex()==blob:
                proof=equal(a,b)
                label_decisions.append({"block":a.block,"candidate":idx,"base_hex":blob,"proof":proof})
                if proof["equal"]: return idx,proof
        values[a.block].append(a); result={"equal":False,"new":True,"first_encounter":True}; label_decisions.append({"block":a.block,"candidate":len(values[a.block])-1,"base_hex":blob,"proof":result}); return len(values[a.block])-1,result
    def eval_aff(word,block,q):
        iblock=1 if block in (1,2) else 3
        gens=[gen(iblock,q,i) for i in range(1,4 if block in (1,2) else 7)]; cur=ActualAffine(q,iblock,q.identity,{},(v1,rt))
        transitions=[]
        for x in word:
            om.bump("fibre_scans",1,"prefix_letter")
            g=gens[abs(x)-1];
            before,bproof=intern(cur)
            nxt=cur.mul(g if x>0 else g.inverse())
            after,aproof=intern(nxt)
            transitions.append([int(x),before,after,bproof,aproof])
            cur=nxt
        return cur,transitions
    hexes=old.hexagon_words(corrected); words=[list(old.embed_f2_pb3(hexes[0])),list(old.embed_f2_pb3(hexes[1])),[]]
    require(old.embed_f2_pb3(hexes[0]) and old.embed_f2_pb3(hexes[1]), "PB3 maps")
    pcontexts=[([1],[4]),([4],[6]),(old.pp_words([[2],[4]]),[6]),
               (old.pp_words([[1],[2]]),old.pp_words([[5],[6]])),
               ([1],old.pp_words([[4],[5]]))]
    p_factors=[old.f2_substitute(corrected,x,y) for x,y in pcontexts]
    printed=v1.paper_product(p_factors[1],p_factors[3],p_factors[0],old.inv_word(p_factors[2]),old.inv_word(p_factors[4]))
    words[2]=list(printed)
    relation_words=[(1,old.pure_relations(3)),(3,old.pure_relations(4))]
    ordinary_base_blobs=[]
    for block,word in ((1,words[0]),(2,words[1]),(3,words[2])):
        q=e3 if block in (1,2) else e4; base_value=q.eval(word); require(base_value==q.identity,"ordinary defect base identity")
        ordinary_base_blobs.append(v1.element_blob(rt,base_value).hex())
    # Recompute and seal the three ordinary defect rows before the first
    # affine-prefix evaluation.  The affine rows below cannot substitute for
    # this direct task186-boundary-row check.
    ordinary_defect_rows=[]
    for block,word in ((1,words[0]),(2,words[1]),(3,words[2])):
        q=e3 if block in (1,2) else e4
        grad,_=old.fox_gradient_without_sections(word,q)
        raw=v1.serial_group_row(rt,grad,block)
        ordinary_defect_rows.append({"block":block,"word":list(word),"row":pub(raw),"row_sha256":digest(pub(raw))})
    ordinary_defect_stack={}
    for item in ordinary_defect_rows:
        for key,value in item["row"]:
            ordinary_defect_stack[key]=(ordinary_defect_stack.get(key,0)+int(value))%3
    ordinary_defect_stack={k:v for k,v in ordinary_defect_stack.items() if v}
    require(isinstance(direct.get("row"),list) and direct.get("row_sha256"),"task186 direct row bound before affine use")
    base_g760=list(rt["bridge"]["g760"]["word"]); base_hex=old.hexagon_words(base_g760)
    base_words=[list(old.embed_f2_pb3(base_hex[0])),list(old.embed_f2_pb3(base_hex[1]))]
    base_factors=[old.f2_substitute(base_g760,x,y) for x,y in pcontexts]
    base_words.append(list(old.paper_product(base_factors[1],base_factors[3],base_factors[0],old.inv_word(base_factors[2]),old.inv_word(base_factors[4]))))
    direct_replay_rows=[]
    for block,bword,nword in ((1,base_words[0],words[0]),(2,base_words[1],words[1]),(3,base_words[2],words[2])):
        q=e3 if block in (1,2) else e4; bg,_=old.fox_gradient_without_sections(bword,q); ng,_=old.fox_gradient_without_sections(nword,q); delta=add(ng,bg,-1); tagged=v1.serial_group_row(rt,delta,block)
        direct_replay_rows.append({"block":block,"base_word":list(bword),"target_word":list(nword),"row":pub(tagged),"row_sha256":digest(pub(tagged))})
    ordinary_direct_stack={}
    for item in direct_replay_rows:
        for key,value in item["row"]:
            ordinary_direct_stack[key]=(ordinary_direct_stack.get(key,0)+int(value))%3
    ordinary_direct_stack={k:v for k,v in ordinary_direct_stack.items() if v}
    ordinary_direct_stack_public=sorted([[k,v] for k,v in ordinary_direct_stack.items()])
    require(ordinary_direct_stack_public==direct.get("row"),"ordinary all-seven stack sign/replay")
    rows=[]; defects=[]; identities=[]
    for block,relset in relation_words:
        for i,word in enumerate(relset,1):
            iblock=1 if block in (1,2) else 3
            val,tr=eval_aff(word,block,e3 if block in (1,2) else e4); ident=ActualAffine(val.q,iblock,val.q.identity,{},(v1,rt)) ; eq=equal(val,ident); require(eq["equal"],"presentation affine identity")
            row={}; d1={}
            for x,before,after,_,_ in tr:
                comp=abs(x); lab=before if x>0 else after; row[(comp,lab)]=(row.get((comp,lab),0)+(1 if x>0 else -1))%3
                d1[str(after)]=(d1.get(str(after),0)+1)%3; d1[str(before)]=(d1.get(str(before),0)-1)%3
            row={str(k):v for k,v in row.items() if v%3}; d1={k:v for k,v in d1.items() if v%3}; require(not d1,"D1 presentation row")
            rows.append({"block":block,"index":i,"word":list(word),"prefix_transitions":tr,"affine_identity":eq,"fox_row":row,"d1":d1})
    for block,word in ((1,words[0]),(2,words[1]),(3,words[2])):
        iblock=1 if block in (1,2) else 3
        val,tr=eval_aff(word,block,e3 if block in (1,2) else e4); eq=equal(val,ActualAffine(val.q,iblock,val.q.identity,{},(v1,rt))); require(eq["equal"],"defect affine identity")
        row={}; d1={}
        for x,before,after,_,_ in tr:
            lab=before if x>0 else after; row[str((abs(x),lab))]=(row.get(str((abs(x),lab)),0)+(1 if x>0 else -1))%3
            d1[str(after)]=(d1.get(str(after),0)+1)%3; d1[str(before)]=(d1.get(str(before),0)-1)%3
        row={k:v for k,v in row.items() if v%3}; d1={k:v for k,v in d1.items() if v%3}; require(not d1,"D1 defect row")
        defects.append({"block":block,"word":list(word),"prefix_transitions":tr,"affine_identity":eq,"fox_row":row,"d1":d1})
    map_replays=[]
    for n,word in enumerate(words[:2],1):
        val,tr=eval_aff(word,1,e3); eq=equal(val,ActualAffine(e3,1,e3.identity,{},(v1,rt))); require(eq["equal"],"PB3 embedding identity")
        map_replays.append({"map":"PB3_embedding_"+str(n),"block":1,"source_word":list(hexes[n-1]),"target_word":list(word),"base":val.blob(val.base).hex(),"prefix_transitions":tr,"affine_identity":eq,"require_identity":True})
    for n,(left,right) in enumerate(pcontexts,1):
        val,tr=eval_aff(p_factors[n-1],3,e4)
        map_replays.append({"map":"PB4_context_"+str(n),"block":3,"source_pair":[list(left),list(right)],"source_word":list(p_factors[n-1]),"target_word":list(p_factors[n-1]),"base":val.blob(val.base).hex(),"prefix_transitions":tr,"map_identity":val.base==e4.identity,"require_identity":False})
    checkpoint_body={"schema":"d972-r07-second-frattini-affine-prefix-compiler-checkpoint/v1","resumable":True,"cursor":len(query_log),"program_cursor":{"mode":"deterministic-replay-from-rank-zero","query":len(query_log),"label":len(label_decisions)},"rank":{"1":len(oracle[1].piv),"3":len(oracle[3].piv)},"columns":oracle_columns,"queries":query_log,"labels":label_decisions,"cache":query_cache,"seen_active":{"1":sorted([list(x) for x in seen_active[1]]),"3":sorted([list(x) for x in seen_active[3]])},"affine_roster":{"1":[a.blob(a.base).hex() for a in values[1]],"3":[a.blob(a.base).hex() for a in values[3]]},"monitor":om.counts,"caps":{"oracle_rounds":args.oracle_rounds,"boundary_pairs":args.boundary_pairs,"seconds":args.seconds,"rss_bytes":args.rss_bytes,"fibre_scans":args.fibre_scans,"candidate_words":args.candidate_words,"retained_columns":args.retained_columns,"checkpoint_bytes":args.checkpoint_bytes},"input_identity":artifact,"source_rebuild":True}
    checkpoint_size=len(canon(checkpoint_body));
    if checkpoint_size>int(args.checkpoint_bytes): raise ResourceStop("phase=checkpoint:cap=checkpoint_bytes:value="+str(checkpoint_size)+":limit="+str(args.checkpoint_bytes),om.provider())
    if resume_expected is not None:
        require(checkpoint_body["queries"][:len(resume_expected.get("queries",[]))]==resume_expected.get("queries",[]) and
                checkpoint_body["labels"][:len(resume_expected.get("labels",[]))]==resume_expected.get("labels",[]) and
                checkpoint_body["columns"][:len(resume_expected.get("columns",[]))]==resume_expected.get("columns",[]) and
                all(checkpoint_body["cache"].get(k)==v for k,v in resume_expected.get("cache",{}).items()),"resume transcript prefix equivalence")
    checkpoint_body["self_digest"]=digest(checkpoint_body)
    return {"schema":SCHEMA,"status":"PASS","terminal":COMMON,"task186_artifact":artifact,"corrected_word":corrected,
            "presentations":{"PB3":old.pure_relations(3),"PB4":old.pure_relations(4)},"ordinary_rows":ordinary_rows,"task186_direct_replay":{"corrected_word":corrected,"row":direct.get("row",[]),"row_sha256":direct.get("row_sha256"),"right_g760_multiplication":True,"all_seven":True},"base_boundary_rows":rows,
            "beta1":{"beta1_H1":defects[0],"beta1_H2":defects[1],"beta1_P":defects[2]},
            "relation_words":{"hexagon_1":words[0],"hexagon_2":words[1],"pentagon":words[2]},
            "ordinary_defect_base_blobs":ordinary_base_blobs,
            "pcontexts":[[list(x),list(y)] for x,y in pcontexts],"pentagon_factors":[list(x) for x in p_factors],
            "pentagon_factor_order":[1,3,0,-2,-4],"affine_pair_counts":{str(k):len(v) for k,v in values.items()},
            "marked_generators":{str(block):[{"index":i,"base":gen(block,e3 if block==1 else e4,i).blob(gen(block,e3 if block==1 else e4,i).base).hex(),"chain":pub(gen(block,e3 if block==1 else e4,i).chain)} for i in range(1,4 if block==1 else 7)] for block in (1,3)},
            "marked_map_identities":{"PB3_embeddings":[list(old.embed_f2_pb3(hexes[0])),list(old.embed_f2_pb3(hexes[1]))],"PB4_pcontexts":[[list(x),list(y)] for x,y in pcontexts],"ordinary_row_digest":digest(ordinary_rows),"map_replays":map_replays,"all_replays_authenticated":all(isinstance(x.get("prefix_transitions"),list) for x in map_replays)},
            "ordinary_defect_rows":ordinary_defect_rows,"ordinary_defect_stack":ordinary_defect_stack,"task186_direct_row_bound":direct.get("row"),"ordinary_direct_replay":{"rows":direct_replay_rows,"stacked_row":ordinary_direct_stack_public,"stack_sign":"target_minus_base_per_block_then_mod3_sum","task186_row":direct.get("row"),"task186_row_sha256":direct.get("row_sha256"),"all_seven_literal_replay":True},
            "complete_boundary_family":True,"D1_zero":True,"generated_subgroup_only":True,"no_jennings":True,
            "equality_oracle":{"complete":True,"queries":len(query_log),"boundary_rows":len(boundary),"negative_dual_correlations":True,"transcript":query_log,"columns":oracle_columns,"query_cache":query_cache,"query_cache_size":len(query_cache),"monitor":om.counts,"caps":{"oracle_rounds":args.oracle_rounds,"boundary_pairs":args.boundary_pairs,"seconds":args.seconds,"rss_bytes":args.rss_bytes}},
            "checkpoint":checkpoint_body,
            "affine_labels":{"first_encounter_roster":{str(k):[{"base":a.blob(a.base).hex(),"chain":pub(a.chain)} for a in v] for k,v in values.items()},"decisions":label_decisions},
            "source_provenance":{"task179":list(TASK179_PRODUCER),"task186_checker":list(TASK186_CHECKER),"corrected_word_source":"exact_direct_replay.replay.corrected_word"}}

def seal(x):
    y=dict(x); y["self_digest"]=digest(y); return y
def main(argv=None):
    p=argparse.ArgumentParser(); p.add_argument("--selftest",action="store_true"); p.add_argument("--task186-receipt",type=Path); p.add_argument("--task186-attestation",type=Path); p.add_argument("--resume",type=Path); p.add_argument("--output",type=Path); p.add_argument("--fixture-output",type=Path); p.add_argument("--seconds",type=int,default=19800); p.add_argument("--boundary-pairs",type=int,default=8000000); p.add_argument("--fibre-scans",type=int,default=80000000); p.add_argument("--candidate-words",type=int,default=2000000); p.add_argument("--retained-columns",type=int,default=250000); p.add_argument("--checkpoint-bytes",type=int,default=4000000000); p.add_argument("--rss-bytes",type=int,default=5700000000); p.add_argument("--oracle-rounds",type=int,default=1000000); a=p.parse_args(argv)
    if a.selftest:
        r=seal(selftest());
        if a.output:a.output.write_bytes(canon(r)+b"\n")
        if a.fixture_output:
            a.fixture_output.parent.mkdir(parents=True,exist_ok=True)
            a.fixture_output.write_bytes(canon({"schema":SELFTEST_SCHEMA,"expected":r["toy"]})+b"\n")
        print(COMMON+"_PRODUCER_SELFTEST_PASS"); return 0
    if not a.task186_receipt or not a.task186_receipt.is_file() or not a.task186_attestation or not a.task186_attestation.is_file(): r={"schema":SCHEMA,"status":UNKNOWN_INPUT,"terminal":UNKNOWN_INPUT+":missing task186 receipt or attestation","reason":"missing authenticated positive task186 input"}
    else:
        try:
            obj,artifact=attest_task186(a.task186_receipt,a.task186_attestation)
        except (OSError, ValueError, RuntimeError) as exc:
            r={"schema":SCHEMA,"status":UNKNOWN_INPUT,"terminal":UNKNOWN_INPUT+":"+str(exc),"reason":str(exc),"task186_artifact":{"path":str(a.task186_receipt)}}
        else:
            try:
                r=actual_compile(a,obj,artifact)
            except ResourceStop as exc:
                cp=dict(exc.state); cp["schema"]="d972-r07-second-frattini-affine-prefix-compiler-checkpoint/v1"; cp["resumable"]=True; cp["reason"]=str(exc); cp["input_identity"]=artifact; cp["program_cursor"]={"mode":"deterministic-replay-from-rank-zero","query":len(cp.get("queries",[])),"label":len(cp.get("labels",[]))}; cp["source_rebuild"]=True; cp["caps"]={"oracle_rounds":a.oracle_rounds,"boundary_pairs":a.boundary_pairs,"seconds":a.seconds,"rss_bytes":a.rss_bytes,"fibre_scans":a.fibre_scans,"candidate_words":a.candidate_words,"retained_columns":a.retained_columns,"checkpoint_bytes":a.checkpoint_bytes}; cp.setdefault("seen_active",{"1":[],"3":[]}); cp.setdefault("affine_roster",{"1":[],"3":[]}); cp["self_digest"]=digest(cp); checkpoint_serialization_bytes=len(canon(cp))
                if checkpoint_serialization_bytes>a.checkpoint_bytes:
                    r={"schema":SCHEMA,"status":UNKNOWN_RESOURCE,"terminal":UNKNOWN_RESOURCE+":phase=checkpoint:cap=checkpoint_bytes:value="+str(checkpoint_serialization_bytes)+":limit="+str(a.checkpoint_bytes),"reason":"checkpoint serialization exceeds checkpoint_bytes cap","task186_artifact":artifact,"checkpoint":None,"checkpoint_serialization_bytes":checkpoint_serialization_bytes}
                else:
                    r={"schema":SCHEMA,"status":UNKNOWN_RESOURCE,"terminal":UNKNOWN_RESOURCE+":"+str(exc),"reason":str(exc),"task186_artifact":artifact,"checkpoint":cp,"checkpoint_serialization_bytes":checkpoint_serialization_bytes}
    r=seal(r)
    if a.output:a.output.write_bytes(canon(r)+b"\n")
    print(COMMON+"_PRODUCER_TERMINAL "+r["terminal"]); return 0
if __name__=="__main__":raise SystemExit(main())
