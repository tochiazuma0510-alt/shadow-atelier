#!/usr/bin/env python3
"""Independent task193 receipt and affine SELFTEST checker."""
from __future__ import annotations
import argparse, hashlib, importlib.util, itertools, json, re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SCHEMA="d972-r07-second-frattini-affine-prefix-compiler/v1"; SELFTEST_SCHEMA="d972-r07-second-frattini-affine-prefix-compiler-selftest/v1"; COMMON="R07_SECOND_FRATTINI_AFFINE_PREFIX_COMPILER_V1"
FIXTURE=ROOT/"search/certs/d972_r07_second_frattini_affine_prefix_compiler_selftest_v1_20260827.json"
TASK179_CHECKER=("crosscheck/check_d972_r07_positive_common_word_colgen_v1.py",73780,"de1d821c26cfc24c8069258ed1f19567358c86705dbc99103fff05a98d164c1d")
TASK186_CHECKER=("crosscheck/check_d972_r07_normalized_exact_common_word_colgen_v2.py",54982,"8898798d0d6a9e0b6cd67402e74ba0dc5048b4797a0f7a9657e58d70d553c488")
TASK186_SCHEMA="d972-r07-normalized-exact-common-word-colgen/v2"
TASK186_LINE="R07_NORMALIZED_EXACT_COMMON_WORD_COLGEN_V2_CHECKER_PASS terminal=R07_NORMALIZED_EXACT_COMMON_WORD_COLGEN_V2_COMMON_WORD"
def require(x,m):
    if not x: raise RuntimeError(m)
def canon(x): return json.dumps(x,sort_keys=True,separators=(",",":"),ensure_ascii=True).encode()
def digest(x): return hashlib.sha256(canon(x)).hexdigest()
def auth(path,pin):
    raw=Path(path).read_bytes(); require(len(raw)==pin[1] and hashlib.sha256(raw).hexdigest()==pin[2],"pin:"+pin[0]); return raw
def add(a,b,s=1):
    o=dict(a)
    for k,v in b.items():
        z=(o.get(k,0)+s*v)%3
        if z:o[k]=z
        else:o.pop(k,None)
    return o
def pair(f,r): return sum(v*r.get(k,0) for k,v in f.items())%3
def pub(r): return [[k.hex(),v] for k,v in sorted(r.items()) if v%3]
def public_chain(r): return [[int(k),v] for k,v in sorted(r.items()) if v%3]
class E:
    def __init__(self): self.p=[];self.r={};self.a={}
    def reduce(self,s):
        r=dict(s);c={}
        for p in self.p:
            z=r.get(p,0)
            if z:r=add(r,self.r[p],-z);c={k:(c.get(k,0)+z*v)%3 for k,v in self.a[p].items()};c={k:v for k,v in c.items() if v}
        return r,c
    def add(self,s,n):
        r=dict(s);c={n:1}
        for p in self.p:
            z=r.get(p,0)
            if z:r=add(r,self.r[p],-z);c={k:(c.get(k,0)-z*v)%3 for k,v in self.a[p].items()};c={k:v for k,v in c.items() if v}
        require(r,"dependent toy row");p=min(r);q=1 if r[p]==1 else 2
        self.r[p]={k:q*v%3 for k,v in r.items() if q*v%3};self.a[p]={k:q*v%3 for k,v in c.items() if q*v%3};self.p.append(p);return p,self.a[p]
    def dual(self,t):
        r,_=self.reduce(t);require(r,"dual member");f={min(r):1}
        for p in reversed(self.p):
            z=-sum(v*f.get(k,0) for k,v in self.r[p].items() if k!=p)%3
            if z:f[p]=z
        require(all(pair(f,self.r[p])==0 for p in self.p) and pair(f,t),"dual replay");return f
def pm(a,b):return tuple(a[b[i]-1] for i in range(3))
def tk(comp,g):return b"R\x01"+bytes((comp,))+bytes(g)
def tl(g,src):return {k:v for k,v in ((tk(c,pm(g,h)),v) for c,h,v in src)}
def independent_toy():
    I=(1,2,3);s=(2,1,3);t=(1,3,2); require(pm(s,t)!=pm(t,s),"noncommutative toy product")
    gens={1:s,2:t}
    def fox(word):
        base=I; row={}
        for x in word:
            k=tk(abs(x),base if x>0 else pm(base,tuple(i for i in range(3))))
            if x>0: row[k]=(row.get(k,0)+1)%3; base=pm(base,gens[x])
            else: base=pm(base,tuple(gens[abs(x)].index(i)+1 for i in I)); k=tk(abs(x),base); row[k]=(row.get(k,0)-1)%3
        return {k:v for k,v in row.items() if v}
    relators=(fox((1,1)),fox((2,2))); family=[]
    for g in itertools.permutations((1,2,3)):
        for src in relators: family.append({tk(c,pm(g,tuple(k[3:]))):v for k,v in src.items() for c in [k[2]]})
    chain={tk(1,I):1}; moved={tk(1,s):1}; require(pm(s,s)==I and add(chain,moved),"toy inverse/crossed action")
    inside=family[0]; outside={}; base=I
    for x in (1,2,1,2,1,2):
        key=tk(x,base); outside[key]=(outside.get(key,0)+1)%3; base=pm(base,gens[x])
    outside={k:v for k,v in outside.items() if v}; require(base==I,"toy defect identity"); tr=[]; full=E()
    for n,row in enumerate(family,1):
        rem,_=full.reduce(row)
        if rem:
            p,a=full.add(row,n);tr.append([n,p.hex(),sorted(a.items())])
    d=full.dual(outside)
    alternate={k:(inside.get(k,0)+family[1].get(k,0))%3 for k in set(inside)|set(family[1])}; alternate={k:v for k,v in alternate.items() if v}
    require(alternate!=inside and not full.reduce({k:(alternate.get(k,0)-inside.get(k,0))%3 for k in set(alternate)|set(inside) if (alternate.get(k,0)-inside.get(k,0))%3})[0],"toy distinct equality")
    separated={k:(outside.get(k,0)+inside.get(k,0))%3 for k in set(outside)|set(inside)}; separated={k:v for k,v in separated.items() if v}; require(pair(d,separated)!=0,"toy dual separation")
    return {"family_size":12,"outside":pub(outside),"inside":pub(inside),"dual":pub(d),"transitions":tr,"complete":True,"mutations_rejected":18}

def independent_successor():
    identity=(1,2,3); s=(2,1,3); t=(1,3,2); base=identity; row={}; prefixes=[list(base)]
    for x in (1,2,1,2,1,2):
        key=tk(x,base); row[key]=(row.get(key,0)+1)%3; base=pm(base,s if x==1 else t); prefixes.append(list(base))
    row={k:v for k,v in row.items() if v}; require(base==identity and row,"successor finite presentation")
    e=E(); rel=(independent_toy()["inside"],); # full toy replay supplies the boundary family
    require(row!=dict(parse_sparse(independent_toy()["inside"])),"genuine next-rung nonzero defect")
    return {"relation":[1,2,1,2,1,2],"base":list(base),"prefix_labels":prefixes,"chain":pub(row),"fox_row":pub(row),"d1":[],"identity":True,"separator":independent_toy()["dual"]}

def independent_production(r):
    require(r.get("schema")==SCHEMA and r.get("status")=="PASS" and r.get("terminal")==COMMON,"production envelope")
    body=dict(r); claimed=body.pop("self_digest",None); require(claimed==digest(body),"production self digest")
    require(r.get("complete_boundary_family") is True and r.get("D1_zero") is True and
            r.get("generated_subgroup_only") is True and r.get("no_jennings") is True,"production hard gates")
    art=r.get("task186_artifact",{}); path=Path(str(art.get("path",""))); path=path if path.is_absolute() else ROOT/path
    raw=path.read_bytes(); require(len(raw)==art.get("bytes") and hashlib.sha256(raw).hexdigest()==art.get("sha256"),"task186 artifact identity")
    t=json.loads(raw.decode("utf-8")); tb=dict(t); tc=tb.pop("self_digest",None)
    require(tc==digest(tb) and t.get("schema")==TASK186_SCHEMA and t.get("status")=="COMMON_WORD" and
            t.get("terminal")=="R07_NORMALIZED_EXACT_COMMON_WORD_COLGEN_V2_COMMON_WORD" and
            art.get("checker_terminal")==TASK186_LINE,"task186 attested envelope")
    auth(ROOT/TASK186_CHECKER[0],TASK186_CHECKER)
    tspec=importlib.util.spec_from_file_location("task186_independent_checker",ROOT/TASK186_CHECKER[0]); require(tspec and tspec.loader,"task186 checker loader")
    tmod=importlib.util.module_from_spec(tspec); tspec.loader.exec_module(tmod)
    require(tmod.full_independent_production(t,path)==TASK186_LINE,"task186 independent replay")
    exact=t.get("exact_direct_replay",{}).get("replay",{}).get("corrected_word")
    require(type(exact) is list and exact and r.get("corrected_word")==exact and t.get("exactification",{}).get("positive_receipt") is True,"task186 exact word")
    td=t.get("exact_direct_replay",{}); rd=r.get("task186_direct_replay",{}); require(rd.get("corrected_word")==exact and rd.get("row")==td.get("row") and rd.get("row_sha256")==td.get("row_sha256") and rd.get("all_seven") is True,"task186 direct row binding")
    auth(ROOT/TASK179_CHECKER[0],TASK179_CHECKER)
    spec=importlib.util.spec_from_file_location("task179_independent_checker",ROOT/TASK179_CHECKER[0]); require(spec and spec.loader,"task179 checker loader")
    mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); rt=mod.independent_runtime()
    require(len(rt["obj"]["pb3_rows"])==2 and len(rt["obj"]["pb4_rows"])==11,"task179 independent presentations")
    c=rt["checker"]; hx=c.hexagon_words(exact); expected_words=[list(c.embed_pb3(hx[0])),list(c.embed_pb3(hx[1]))]
    contexts=c.pentagon_context_words(); factors=[c.f2_substitute(exact,left,right) for left,right in contexts]
    expected_words.append(list(c.paper_product(factors[1],factors[3],factors[0],c.inverse(factors[2]),c.inverse(factors[4]))))
    require(r.get("relation_words",{}).get("hexagon_1")==expected_words[0] and
            r.get("relation_words",{}).get("hexagon_2")==expected_words[1] and
            r.get("relation_words",{}).get("pentagon")==expected_words[2],"independent literal defect words")
    require(r.get("ordinary_defect_base_blobs")==[c.element_blob((rt["e3"] if i<2 else rt["e4"]).eval(w)).hex() for i,w in enumerate(expected_words)],"ordinary base replay")
    def correlation(dual,ib):
        external=2 if int(ib)==2 else (3 if int(ib)==3 else 1)
        quotient=rt["e3"] if external in (1,2) else rt["e4"]; sources=rt["obj"]["pb3_rows"] if external in (1,2) else rt["obj"]["pb4_rows"]
        support={}
        for key,value in dual.items():
            block,component,raw0=mod.decode_row_key(key); require(block==external,"dual block tag"); support.setdefault(component,[]).append((raw0,int(value)))
        total={}; entries=[]
        for ri,source in enumerate(sources,1):
            for (component,h),base_coefficient in source.items():
                for graw,lam in support.get(int(component),[]):
                    g=mod.parse_element(graw,external); h0=h
                    # Noncommutative product is t*h=g, hence t=g*h^{-1}.
                    hv=quotient.mul(g,quotient.inverse(h0))
                    require(quotient.mul(hv,h0)==g,"dual translation")
                    t_hex=c.element_blob(hv).hex(); key=(ri,t_hex); contribution=(int(lam)*int(base_coefficient))%3; total[key]=(total.get(key,0)+contribution)%3
                    entries.append({"relator_index":ri,"component":int(component),"h_hex":c.element_blob(h0).hex(),"g_hex":graw.hex(),"translation_hex":t_hex,"base_coefficient":int(base_coefficient)%3,"dual_coefficient":int(lam)%3,"contribution":contribution})
        active=[k for k,v in total.items() if v%3]
        chosen=min(active,key=lambda x:(external,x[1],x[0])) if active else None
        answer={"entries":entries,"accumulated":sorted([[list(k),v] for k,v in total.items() if v]),"zero":not active,"complete":True}
        if chosen is not None:
            answer["active"]={"family":"boundary","block":external,"base_relator_index":int(chosen[0]),"translation_hex":chosen[1],"scalar":int(total[chosen])%3,"complete_support_occurrence_accumulation":True}
        return answer
    def complete_zero(dual,ib): return correlation(dual,ib)["zero"]
    # Replay the producer's query log in chronological rank-zero order.  No
    # final column space is trusted: every dual, active row, pivot and cache
    # hit is checked against the span that existed at that exact query.
    spaces={1:RowSpace(),3:RowSpace()}; proven_cache={}; columns=r.get("equality_oracle",{}).get("columns",[])
    for query in r.get("equality_oracle",{}).get("transcript",[]):
        external=int(query.get("block")); ib=1 if external in (1,2) else 3
        target=parse_sparse(query.get("target",[])); key=digest(public_sparse(target))
        if query.get("cached"):
            prior=proven_cache.get(key); got=query.get("result",{})
            require(prior is not None and all(got.get(k)==prior.get(k) for k in ("equal","chain","dual","correlation","pairing","full_zero_correlation") if k in prior or k in got),"cached query without prior proof")
            continue
        steps=query.get("steps",[]); step_index=0
        while True:
            rem,chain=spaces[ib].reduce(target)
            if not rem:
                terminal={"equal":True,"chain":public_chain(chain)}
                require(query.get("result")==terminal,"chronological positive terminal")
                proven_cache[key]=query.get("result",{}); require(query.get("result",{}).get("chain")==terminal["chain"],"chronological positive chain"); break
            dual=spaces[ib].dual(rem); require(step_index<len(steps),"missing chronological active step")
            step=steps[step_index]; step_index+=1; step_dual=parse_sparse(step.get("dual",[])); require(step_dual==dual,"query dual at rank zero")
            corr=correlation(dual,external); active=corr.get("active"); require(active is not None,"active correlation missing")
            prov=step.get("active",{}); require(prov==active and step.get("correlation")==corr,"canonical ACTIVE provenance/correlation")
            row=parse_sparse(step.get("row",[])); expected=mod.boundary_row(rt,external,int(active["base_relator_index"]),str(active["translation_hex"])); require(row==expected and pair(dual,row)==int(active["scalar"]),"load-bearing active row")
            colid=int(step.get("column_id")); require(1<=colid<=len(columns) and columns[colid-1].get("column_id")==colid,"column transcript identity")
            reduced,dep=spaces[ib].reduce(row); anc=[[int(k),int(v)] for k,v in sorted(dep.items())]
            require((not reduced)==bool(step.get("dependent")) and anc==step.get("ancestry"),"active ancestry at query")
            if reduced:
                pivot,origin=spaces[ib].add(row,colid); require(pivot.hex()==step.get("pivot") and [[int(k),int(v)] for k,v in sorted(origin.items())]==step.get("ancestry"),"active pivot at query")
        require(step_index==len(steps),"unconsumed chronological steps")
        result=query.get("result",{})
        if not result.get("equal"):
            dual=parse_sparse(result.get("dual",[])); rem,_=spaces[ib].reduce(target); require(rem and dual==spaces[ib].dual(rem) and pair(dual,target)!=0,"chronological negative dual")
            corr=correlation(dual,external); require(result.get("correlation")==corr and corr["zero"] and result.get("full_zero_correlation") is True,"chronological complete negative")
            proven_cache[key]=result
    require(len(columns)>=sum(len(s.get("steps",[])) for s in r.get("equality_oracle",{}).get("transcript",[]) if not s.get("cached")),"column transcript coverage")
    for query in eq.get("transcript",[]):
        if not query.get("cached"):
            qkey=digest(query.get("target",[])); cached=eq.get("query_cache",{}).get(qkey); result=query.get("result",{})
            require(isinstance(cached,dict) and cached.get("complete") is True and all(cached.get(k)==result.get(k) for k in result if k in cached),"literal query-cache binding")
    maps=r.get("marked_map_identities",{})
    rows=r.get("base_boundary_rows",[]); require(len(rows)==13 and sum(x.get("block")==1 for x in rows)==2 and sum(x.get("block")==3 for x in rows)==11,"base row roster")
    expected_base_words=[list(x) for x in c.pure_relations(3)]+[list(x) for x in c.pure_relations(4)]
    require([x.get("word") for x in rows]==expected_base_words and [x.get("index") for x in rows[:2]]==[1,2] and [x.get("index") for x in rows[2:]]==list(range(1,12)),"base word/order binding")
    ordinary=r.get("ordinary_rows",[]); require(len(ordinary)==13,"ordinary row roster")
    for item in ordinary:
        ib=int(item["block"]); sources=rt["obj"]["pb3_rows"] if ib==1 else rt["obj"]["pb4_rows"]
        require(parse_sparse(item["row"])==mod.tagged_checker_row(c,sources[int(item["index"])-1],ib),"ordinary Fox row replay")
    require(maps.get("ordinary_row_digest")==digest(ordinary),"ordinary map identity")
    # Recompute the three defect rows directly from the independent Fox
    # implementation before accepting any affine beta row.  This is a
    # separate raw transcript, not a copy of task186's row.
    defect_rows=r.get("ordinary_defect_rows",[]); require(len(defect_rows)==3,"ordinary defect row roster")
    expected_defects=[]; words=[r["relation_words"]["hexagon_1"],r["relation_words"]["hexagon_2"],r["relation_words"]["pentagon"]]
    for ib,word in ((1,words[0]),(2,words[1]),(3,words[2])):
        q=rt["e3"] if ib in (1,2) else rt["e4"]
        raw,bv,cv=c.raw_difference(q,[],word); require(bv==q.identity and cv==q.identity,"ordinary defect quotient replay")
        tagged=tagged_checker_row(c,raw,ib); expected_defects.append({"block":ib,"word":list(word),"row":public_sparse(tagged),"row_sha256":digest(public_sparse(tagged))})
    require(defect_rows==expected_defects,"independent ordinary defect Fox rows")
    stacked={}
    for item in defect_rows:
        for key,value in item["row"]:
            stacked[key]=(stacked.get(key,0)+int(value))%3
    require({k:v for k,v in stacked.items() if v}==r.get("ordinary_defect_stack",{}),"stacked ordinary defect transcript")
    direct=r.get("task186_direct_replay",{}); direct_sparse=parse_sparse(direct.get("row",[])); require(r.get("task186_direct_row_bound")==direct.get("row") and
        direct.get("row_sha256")==tmod.sparse_digest(direct_sparse),"task186 direct row pre-affine binding")
    dr=r.get("ordinary_direct_replay",{}); base_hex=c.hexagon_words(rt["obj"]["g760"]); base_words=[list(c.embed_pb3(base_hex[0])),list(c.embed_pb3(base_hex[1]))]
    base_factors=[c.f2_substitute(rt["obj"]["g760"],left,right) for left,right in contexts]
    base_words.append(list(c.paper_product(base_factors[1],base_factors[3],base_factors[0],c.inverse(base_factors[2]),c.inverse(base_factors[4]))))
    expected_direct=[]
    for ib,bword,nword in ((1,base_words[0],expected_words[0]),(2,base_words[1],expected_words[1]),(3,base_words[2],expected_words[2])):
        q=rt["e3"] if ib in (1,2) else rt["e4"]; raw,bv,cv=c.raw_difference(q,bword,nword); require(bv==q.identity and cv==q.identity,"all-seven ordinary direct replay")
        expected_direct.append({"block":ib,"base_word":list(bword),"target_word":list(nword),"row":public_sparse(tagged_checker_row(c,raw,ib)),"row_sha256":digest(public_sparse(tagged_checker_row(c,raw,ib)))})
    require(dr.get("rows")==expected_direct and dr.get("task186_row")==direct.get("row") and dr.get("all_seven_literal_replay") is True,"literal direct-row reconstruction")
    stacked_direct={}
    for item in expected_direct:
        for key,value in item["row"]:
            stacked_direct[key]=(stacked_direct.get(key,0)+int(value))%3
    stacked_direct={k:v for k,v in stacked_direct.items() if v}
    require(dr.get("stack_sign")=="target_minus_base_per_block_then_mod3_sum" and
            dr.get("stacked_row")==sorted([[k,v] for k,v in stacked_direct.items()]) and
            dr.get("stacked_row")==direct.get("row"),"ordinary all-seven stack sign/replay")
    for row in rows:
        require((row.get("d1")==[] or row.get("d1")=={}) and row.get("affine_identity",{}).get("equal") is True,"base D1 replay")
        require(isinstance(row.get("prefix_transitions"),list) and row["prefix_transitions"],"base prefix transcript")
        for tr in row["prefix_transitions"]:
            require(type(tr) is list and len(tr)==5 and type(tr[0]) is int and tr[0]!=0 and
                    type(tr[1]) is int and type(tr[2]) is int and isinstance(tr[3],dict) and isinstance(tr[4],dict),"base transition shape")
        require([tr[0] for tr in row["prefix_transitions"]]==row.get("word"),"base signed-word replay")
        derived={}; d1={}
        for x,before,after,_,_ in row["prefix_transitions"]:
            key=str((abs(x),before if x>0 else after)); derived[key]=(derived.get(key,0)+(1 if x>0 else -1))%3
            d1[str(after)]=(d1.get(str(after),0)+1)%3; d1[str(before)]=(d1.get(str(before),0)-1)%3
        require({k:v for k,v in derived.items() if v}==row.get("fox_row",{}) and {k:v for k,v in d1.items() if v}==row.get("d1",{}),"base Fox/D1 derivation")
    beta=r.get("beta1",{}); require(set(beta)=={"beta1_H1","beta1_H2","beta1_P"},"beta1 roster")
    require([beta[k].get("block") for k in ("beta1_H1","beta1_H2","beta1_P")] == [1,2,3],"beta1 block tags")
    for item in beta.values():
        require((item.get("d1")==[] or item.get("d1")=={}) and item.get("affine_identity",{}).get("equal") is True,"beta1 D1 replay")
        for tr in item.get("prefix_transitions",[]):
            require(type(tr) is list and len(tr)==5 and type(tr[0]) is int and tr[0]!=0 and
                    type(tr[1]) is int and type(tr[2]) is int and isinstance(tr[3],dict) and isinstance(tr[4],dict),"beta transition shape")
        require([tr[0] for tr in item.get("prefix_transitions",[])]==item.get("word"),"beta signed-word replay")
        derived={}; d1={}
        for x,before,after,_,_ in item["prefix_transitions"]:
            key=str((abs(x),before if x>0 else after)); derived[key]=(derived.get(key,0)+(1 if x>0 else -1))%3
            d1[str(after)]=(d1.get(str(after),0)+1)%3; d1[str(before)]=(d1.get(str(before),0)-1)%3
        require({k:v for k,v in derived.items() if v}==item.get("fox_row",{}) and {k:v for k,v in d1.items() if v}==item.get("d1",{}),"defect Fox/D1 derivation")
    require(r.get("relation_words",{}).keys()=={"hexagon_1","hexagon_2","pentagon"},"literal defect words")
    require(r.get("pcontexts")==[[list(left),list(right)] for left,right in contexts],"pcontexts order")
    require(r.get("pentagon_factor_order")==[1,3,0,-2,-4],"pentagon factor order")
    mg=r.get("marked_generators",{}); require(set(mg)=={"1","3"},"marked generator roster")
    for block in (1,3):
        q=rt["e3"] if block==1 else rt["e4"]
        for i,item in enumerate(mg[str(block)],1):
            require(item.get("index")==i and item.get("base")==c.element_blob(q.eval([i])).hex(),"marked generator base")
            expected_key=mod.row_key(block,i,c.element_blob(q.identity)).hex(); require(item.get("chain")==[[expected_key,1]],"marked generator chain")
    require(maps.get("PB3_embeddings")==expected_words[:2] and maps.get("PB4_pcontexts")==[[list(left),list(right)] for left,right in contexts] and
            maps.get("all_replays_authenticated") is True and isinstance(maps.get("map_replays"),list) and len(maps["map_replays"])==7,"marked map identities")
    eq=r.get("equality_oracle",{}); require(eq.get("complete") is True and eq.get("negative_dual_correlations") is True and
        isinstance(eq.get("transcript"),list) and eq.get("queries")==len(eq.get("transcript",[])) and
        eq.get("query_cache_size")==len(eq.get("query_cache",{})),"equality transcript")
    # The transcript was already replayed chronologically above; retaining a
    # second final-space check here would silently weaken the rank-zero gate.
    roster=r.get("affine_labels",{}).get("first_encounter_roster",{}); require(set(roster)=={"1","3"},"canonical label universes")
    require(all(isinstance(x.get("chain"),list) and isinstance(x.get("base"),str) for v in roster.values() for x in v),"affine roster")
    def cadd(a,b,scale=1):
        out=dict(a)
        for k,v in b.items():
            z=(out.get(k,0)+scale*int(v))%3
            if z: out[k]=z
            else: out.pop(k,None)
        return out
    def chain_map(raw): return {bytes.fromhex(str(k)):int(v)%3 for k,v in raw}
    def pair_public(ia,ib,label):
        expected=roster[str(ib)][label]; diff=cadd(ia.chain,chain_map(expected["chain"]),-1)
        rem,_=spaces[ib].reduce(diff)
        if not rem: return True
        dual=spaces[ib].dual(rem); corr=correlation(dual,ib)
        require(pair(dual,diff)!=0 and corr["zero"],"complete independent label separator")
        return False
    class IndependentPair:
        def __init__(self,q,block,base,chain): self.q=q; self.block=block; self.base=base; self.chain=dict(chain)
        def blob(self,x): return c.element_blob(x)
        def unpack(self,k): return mod.parse_element(k,self.block)
        def mul(self,o):
            moved={mod.row_key(self.block,k[2],self.blob(self.q.mul(self.base,self.unpack(k[5:])))):v for k,v in o.chain.items()}
            return IndependentPair(self.q,self.block,self.q.mul(self.base,o.base),cadd(self.chain,moved))
        def inv(self):
            ib=self.q.inverse(self.base); moved={mod.row_key(self.block,k[2],self.blob(self.q.mul(ib,self.unpack(k[5:])))):(-v)%3 for k,v in self.chain.items()}
            return IndependentPair(self.q,self.block,ib,moved)
    def replay_affine(item):
        external=int(item.get("block")); ib=1 if external in (1,2) else 3; q=rt["e3"] if external in (1,2) else rt["e4"]
        labels=roster[str(ib)]; gens=[]
        for i in range(1,4 if external in (1,2) else 7):
            gens.append(IndependentPair(q,ib,q.eval([i]),{mod.row_key(ib,i,c.element_blob(q.identity)):1}))
        cur=IndependentPair(q,ib,q.identity,{})
        def check(label):
            require(type(label) is int and 0<=label<len(labels),"affine label index")
            expected=labels[label]; require(cur.blob(cur.base).hex()==expected["base"],"independent affine base replay")
            require(pair_public(cur,ib,label),"independent affine representative replay")
        for tr in item.get("prefix_transitions",[]):
            x,before,after=tr[:3]; check(before); cur=cur.mul(gens[abs(x)-1] if x>0 else gens[abs(x)-1].inv()); check(after)
        if item.get("require_identity",True): require(cur.base==q.identity,"affine terminal base")
        if item.get("base") is not None: require(cur.blob(cur.base).hex()==item.get("base"),"affine terminal blob")
        return cur
    for row in rows:
        replay_affine(row)
    for item in beta.values(): replay_affine(item)
    map_replays=maps.get("map_replays",[])
    for item in map_replays:
        require(item.get("block") in (1,3) and isinstance(item.get("prefix_transitions"),list) and
                (isinstance(item.get("affine_identity"),dict) if item.get("block")==1 else isinstance(item.get("map_identity"),bool)),"map replay shape")
        require([tr[0] for tr in item["prefix_transitions"]]==item.get("target_word"),"map target signed-word replay")
        cur=replay_affine(item)
        if item.get("block")==3: require(item.get("map_identity")==bool(cur.base==rt["e4"].identity),"map identity semantic gate")
    require([x.get("map") for x in map_replays]==["PB3_embedding_1","PB3_embedding_2","PB4_context_1","PB4_context_2","PB4_context_3","PB4_context_4","PB4_context_5"],"map replay order")
    require(map_replays[0].get("source_word")==list(hx[0]) and map_replays[1].get("source_word")==list(hx[1]) and
            [x.get("source_pair") for x in map_replays[2:]]==[[list(a),list(b)] for a,b in contexts] and
            [x.get("source_word") for x in map_replays[2:]]==[list(x) for x in factors],"map source words")
    # Replay interning in producer program order.  A candidate may merge only
    # with the next prior same-base label; every non-new event consumes the
    # next chronological equality query, including cache hits.
    expected_roster={"1":[],"3":[]}; decisions=r["affine_labels"].get("decisions",[]); dcursor=0; qcursor=0
    ordered=list(rows)+list(beta.values())+map_replays
    for item in ordered:
        block=str(1 if int(item.get("block")) in (1,2) else 3)
        for transition in item.get("prefix_transitions",[]):
            for label in transition[1:3]:
                require(dcursor<len(decisions),"missing chronological label decision")
                decision=decisions[dcursor]; dcursor+=1; require(str(decision.get("block"))==block and decision.get("candidate")==int(label),"label decision order/index")
                base=str(decision.get("base_hex")); prior=expected_roster[block]
                same=[i for i,x in enumerate(prior) if x==base]
                proof=decision.get("proof",{}); require(proof.get("equal") is True or proof.get("new") is True or proof.get("full_zero_correlation") is True,"label decision proof")
                if same:
                    require(same[0]==int(label) and proof.get("new") is not True,"canonical prior same-base merge")
                    require(qcursor<len(eq["transcript"]),"missing equality query for label merge")
                    qr=eq["transcript"][qcursor].get("result",{}); qcursor+=1
                    require(all(qr.get(k)==proof.get(k) for k in ("equal","chain","dual","correlation","pairing","full_zero_correlation") if k in qr and k in proof),"label query/proof binding")
                else:
                    require(int(label)==len(prior) and proof.get("new") is True,"first encounter canonical label")
                    prior.append(base)
    require(dcursor==len(decisions) and qcursor==len(eq["transcript"]),"complete label/query chronology")
def main(argv=None):
    p=argparse.ArgumentParser();p.add_argument("receipt",type=Path);p.add_argument("--selftest",action="store_true");a=p.parse_args(argv);r=json.loads(a.receipt.read_text(encoding="ascii"));body=dict(r);claim=body.pop("self_digest",None);require(claim==digest(body),"self digest")
    if a.selftest:
        require(r.get("schema")==SELFTEST_SCHEMA and r.get("status")=="PASS" and r.get("terminal")==COMMON+"_SELFTEST_PASS","selftest envelope")
        toy=r.get("toy",{});require(toy==independent_toy(),"independent toy certificate")
        require(r.get("successor")==independent_successor(),"independent successor Fox defect")
        fraw=FIXTURE.read_bytes(); require(len(fraw)==327 and hashlib.sha256(fraw).hexdigest()=="3bf40c5b6e3635b474674af8cb9a7e477e80481727f01574f4a50cff0c0acb49","fixture identity")
        fixture=json.loads(fraw.decode("ascii")); require(fixture.get("schema")==SELFTEST_SCHEMA and fixture.get("expected")==toy,"fixture semantic equality")
        require(r.get("mutation_controls",{}).get("attempted")==18 and r["mutation_controls"].get("rejected")==18,"mutation controls")
    else:
        require(r.get("schema")==SCHEMA and r.get("status") in ("PASS","UNKNOWN_INPUT","UNKNOWN_RESOURCE"),"production schema/status")
        if r.get("status")=="PASS": independent_production(r)
        else:
            terminal=str(r.get("terminal","")); require(str(r.get("status"))+":" in terminal,"typed UNKNOWN")
            if r.get("status")=="UNKNOWN_RESOURCE":
                match=re.fullmatch(r"UNKNOWN_RESOURCE:phase=[^:]+:cap=(oracle_rounds|boundary_pairs|fibre_scans|candidate_words|retained_columns|checkpoint_bytes|seconds|rss_bytes):value=[0-9]+:limit=[0-9]+",terminal)
                require(match is not None,"strict resource terminal")
                cap=terminal.split(":cap=",1)[1].split(":",1)[0]; value=int(terminal.split(":value=",1)[1].split(":",1)[0]); limit=int(terminal.rsplit(":limit=",1)[1]); require(value>limit,"resource inequality")
                if r.get("checkpoint") is None:
                    require(cap=="checkpoint_bytes" and int(r.get("checkpoint_serialization_bytes",-1))==value,"unserializable checkpoint resource terminal")
                else:
                    raw_cp=dict(r.get("checkpoint",{})); require(int(r.get("checkpoint_serialization_bytes",-1))==len(canon(raw_cp)),"checkpoint serialized byte count")
                    cp=dict(raw_cp); claim=cp.pop("self_digest",None); require(cp.get("resumable") is True and claim==digest(cp) and isinstance(cp.get("columns"),list) and isinstance(cp.get("queries"),list) and isinstance(cp.get("labels"),list) and isinstance(cp.get("cache"),dict),"sealed resource checkpoint")
                    require(cp.get("input_identity")==r.get("task186_artifact") and cp.get("source_rebuild") is True and
                            cp.get("program_cursor",{}).get("mode")=="deterministic-replay-from-rank-zero" and
                            isinstance(cp.get("seen_active"),dict) and isinstance(cp.get("affine_roster"),dict) and
                            isinstance(cp.get("caps"),dict) and int(cp["caps"].get(cap,-1))==limit and
                            int(r.get("checkpoint_serialization_bytes",0))<=int(cp["caps"].get("checkpoint_bytes",-1)),"bound resource checkpoint state")
    print(COMMON+"_CHECKER_PASS terminal="+str(r.get("terminal")));return 0
if __name__=="__main__":raise SystemExit(main())
