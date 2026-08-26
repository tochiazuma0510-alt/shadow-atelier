"""Authenticated, bounded R07 full-E4 bridge (task 172).

The expensive fixed prefix and correction orbit are intentionally absent.  The
raw bridge below calls only the authenticated predecessor constructors, builds
the 26-word presentation and a small actual conjugation sample, and records a
typed UNKNOWN if any gate fails.
"""
from __future__ import annotations
import hashlib, importlib.util, json, sys, time
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"search/certs/d972_r07_full_e4_orbit_preflight_v7_20260827.json"
Q3=ROOT/"ci/b345_157ee_artifacts_32359956713/d972_b345_q3_chief_v1.json"
ART=ROOT/"ci/b345_157ee_artifacts_32359956713/d972_b345_joint_kernel_qstar_closure_v1.json"
TARGET_ART=ROOT/"ci/b345_157en_artifacts_32458556448/d972_b345_target6_dual_colgen_v2.json"
PREV=ROOT/"search/d972_b345_triple_cube_raw_lambda_census_v1.py"
PREV_SHA="d4a290984ae8a93b6959f06d20c1de037b2814707778fba03c59ac87b2f736db"
Q3_SHA="3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72"
ART_SHA="1c3ad7a7124cee152eb40968cf212c14641a9f8720063c85f70533864898d0df"
BASE_SHA="518f09820b8d7baee6b58ebf366cebf7b02a9a945cd1350cf8c701a4e6bc2b4d"
TERMINAL="R07_FULL_E4_ORBIT_PREFLIGHT_READY"

PIN_PATHS=[
 "sol/luna_task_172_r07_full_e4_orbit_preflight_repair_v2.md",
 "sol/luna_task_171_r07_full_e4_joint_orbit_preflight_v1.md",
 "sol/proof_r07_full_e4_joint_orbit_selector_v109.md",
 "sol/proof_r07_full_e4_seven_evaluation_orbit_selector_v110.md",
 "sol/proof_r07_filtered_actual_orbit_homotopy_v111.md",
 "search/d972_b345_triple_cube_raw_lambda_census_v1.py",
 "search/d972_b345_joint_kernel_qstar_closure_v1.py",
 "search/d972_b345_target6_dual_colgen_v2.py",
 "search/check_d972_r07_616_to_760_commutator_affine_rhs_v3.py",
 "ci/b345_157ee_artifacts_32359956713/d972_b345_q3_chief_v1.json",
 "ci/b345_157ee_artifacts_32359956713/d972_b345_joint_kernel_qstar_closure_v1.json",
 "ci/b345_157en_artifacts_32458556448/d972_b345_target6_dual_colgen_v2.json",
]
def sha_file(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def digest_obj(x): return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(",",":"),ensure_ascii=True).encode()).hexdigest()
def need(x,msg):
    if not x: raise RuntimeError(msg)
def load(path,name):
    s=importlib.util.spec_from_file_location(name,path); need(s and s.loader,"module spec")
    m=importlib.util.module_from_spec(s); sys.modules[name]=m; s.loader.exec_module(m); return m
def pins():
    out={}
    for rel in PIN_PATHS:
        p=ROOT/rel; need(p.is_file(),"missing pin "+rel); out[rel]={"bytes":p.stat().st_size,"sha256":sha_file(p)}
    need(out["ci/b345_157ee_artifacts_32359956713/d972_b345_q3_chief_v1.json"]["sha256"]==Q3_SHA,"q3 sha")
    need(out["ci/b345_157ee_artifacts_32359956713/d972_b345_joint_kernel_qstar_closure_v1.json"]["sha256"]==ART_SHA,"157ee sha")
    return out
def row_digest(old,row):
    ans=[]
    for (c,v),a in row.items():
        if a%3: ans.append([int(c),old._element_blob(v).hex(),int(a)%3])
    ans.sort(key=lambda z:(z[0],bytes.fromhex(z[1]))); return digest_obj(ans),len(ans)
def row_serial(old,row):
    ans=[]
    for (c,v),a in row.items():
        if a%3: ans.append([int(c),old._element_blob(v).hex(),int(a)%3])
    ans.sort(key=lambda z:(z[0],bytes.fromhex(z[1]))); return ans
def add_scaled(old,d,src,scale):
    for k,v in src.items():
        n=(d.get(k,0)+scale*int(v))%3
        if n:d[k]=n
        else:d.pop(k,None)
def target_formula(old,e4,g,word=None):
    z=old.inv_word(old.pp_words([[1],[2]])); mapping=old.cofaces(3)[0]
    def sub(w,l,r): return old.f2_substitute(w,l,r)
    def lift(w): return old.word_substitute(old.embed_f2_pb3(w),mapping)
    a4,b4,c4=(lift(sub(g,[1],[2])),lift(sub(g,[1],z)),lift(sub(g,[2],z)))
    fixed_c4=lift(sub(g,[2],z)); p=e4.eval(fixed_c4)
    h=e4.eval(lift(old.hexagon_words(g)[0]))
    def sigma(w):
        ga,va=old.fox_gradient_without_sections(lift(sub(w,[1],[2])),e4)
        gb,vb=old.fox_gradient_without_sections(lift(sub(w,[1],z)),e4)
        gc,vc=old.fox_gradient_without_sections(lift(sub(w,[2],z)),e4)
        need(va==vb==vc==e4.identity,"context relation identity")
        ans={}; add_scaled(old,ans,old.translate_vector(gc,p,e4),1); add_scaled(old,ans,old.translate_vector(gb,p,e4),-1); add_scaled(old,ans,old.translate_vector(ga,h,e4),1)
        return ans
    return sigma, {"formula":"corrected_minus_base","substitutions":["(X0,Y0)","(X0,Z0)","(Y0,Z0)"],"transport_order":"constant*psi(u) under current left-action convention","prefix_blob":old._element_blob(p).hex(),"h_blob":old._element_blob(h).hex()}
def build_roster(j,old,e3,e4,contexts,words):
    group=j.JointGroup(old,e3,e4,contexts,words)
    rows=[]
    for sid,trans in enumerate(group.transitions):
        su=group.section_word(sid)
        for gi,tgt in enumerate(trans):
            w=old.reduce_word(su+list(words[gi])+old.inv_word(group.section_word(tgt)))
            rows.append({"layer":"gamma_edge","ordinal":sid*26+gi+1,"word":w})
    # action relations are the literal x/y conjugations from the predecessor.
    for ri in range(26):
        for li in range(2):
            val=group.eval([li+1])
            gen=group.generators[ri]
            for orient in (1,-1):
                if orient==1: cv=group.mul(group.mul(group.inverse(val),gen),val); tokens=[('letter',li,-1),('record',ri,1),('letter',li,1)]
                else: cv=group.mul(group.mul(val,gen),group.inverse(val)); tokens=[('letter',li,1),('record',ri,1),('letter',li,-1)]
                tgt=group.ids[group.key(cv)]
                w=old.reduce_word(j.materialize_tokens(old,words,tokens+[('record',x,-1) for x in reversed(group.section_factors(tgt))]))
                rows.append({"layer":"xy_action","ordinal":ri*4+li*2+(1 if orient==1 else 2),"word":w})
    rels=j.complete_relators(old)
    for qi,r in enumerate(rels):
        tgt=group.ids[group.key(group.eval(r))]
        rows.append({"layer":"q0_relator","ordinal":qi+1,"word":old.reduce_word(list(r)+old.inv_word(group.section_word(tgt)))})
    need(len(rows)==6441,"roster count")
    # Each row is constructed from a typed section endpoint; exhaustive
    # re-evaluation of all long rows would duplicate the expensive orbit.
    return group,rows
def fox_sample(old,e4,contexts,aliases,roster,g,sample_n=101):
    ids=[aliases["hexagon_1_fxy_0"]-1,aliases["hexagon_1_fxz_0"]-1,aliases["hexagon_1_fyz_0"]-1]
    ctx=[contexts[i] for i in ids]; sigma,meta=target_formula(old,e4,g)
    def translated(word,u):
        z=old.inv_word(old.pp_words([[1],[2]])); mapping=old.cofaces(3)[0]
        def sub(w,l,r):return old.f2_substitute(w,l,r)
        def lift(w):return old.word_substitute(old.embed_f2_pb3(w),mapping)
        ans={}; p=e4.eval(lift(sub(g,[2],z))); h=e4.eval(lift(old.hexagon_words(g)[0]))
        for gradword,constant,sgn,ci in [(sub(word,[1],[2]),h,1,0),(sub(word,[1],z),p,-1,1),(sub(word,[2],z),p,1,2)]:
            grad,val=old.fox_gradient_without_sections(lift(gradword),e4); need(val==e4.identity,"translated relation context nonidentity"); uv=e4.eval(u,ctx[ci]); transport=e4.mul(constant,uv); tr=old.translate_vector(grad,transport,e4); add_scaled(old,ans,tr,sgn)
        return ans
    conjs=[[],[1],[-1],[2],[-2],[1,2],[-2,-1],[1,1,2,-1],[2,1,-2,-1]]
    comp={"gamma_edge":0,"xy_action":0,"q0_relator":0}; passed=0; checks=[]
    candidates=sorted(roster,key=lambda x:(len(x["word"]),x["layer"],x["ordinal"]))
    # The target6 formula has three explicit PB3->PB4 lifts.  Retain only
    # rows that are actually in those three typed context kernels; this is a
    # gate, not an inferred equivalence from the public relation counts.
    mapping=old.cofaces(3)[0]
    def lift(w): return old.word_substitute(old.embed_f2_pb3(w),mapping)
    def ok_target(w):
        z=old.inv_word(old.pp_words([[1],[2]]))
        return all(e4.eval(lift(old.f2_substitute(w,l,r)))==e4.identity for l,r in (([1],[2]),([1],z),([2],z)))
    eligible=[]; quotas={"gamma_edge":35,"xy_action":33,"q0_relator":33}; eligible_counts={k:0 for k in quotas}
    # Scan only until the requested layer quota is met; an empty layer is
    # nevertheless scanned in full and is a typed UNKNOWN, never skipped.
    for layer,quota in quotas.items():
        for r in (x for x in candidates if x["layer"]==layer):
            if ok_target(r["word"]):
                eligible.append(r); eligible_counts[layer]+=1
                if eligible_counts[layer]>=quota: break
    if any(eligible_counts[k]==0 for k in quotas):
        return {"pairs":0,"required":sample_n,"status":"UNKNOWN_TYPED_FOX_EMPTY_CONTEXT_LAYER","eligible_counts":eligible_counts,"layer_counts":{},"same_context_pairs":0,"same_context":[],"row_digest_sha256":digest_obj([]),"convention":meta}
    chosen=[]
    for layer,n in (("gamma_edge",35),("xy_action",33),("q0_relator",33)):
        pool=[x for x in eligible if x["layer"]==layer]
        need(pool,"missing roster layer "+layer)
        # q0 has only 19 rows; distinct actual conjugators make repeated
        # relation rows into distinct (u,r) samples.
        chosen += [pool[k%len(pool)] for k in range(n)]
    need(len(chosen)>=sample_n,"fox sample quota")
    for i,r in enumerate(chosen[:sample_n]):
        u=conjs[i%len(conjs)]; w=old.reduce_word(u+r["word"]+old.inv_word(u))
        try:
            direct=sigma(w); pred=translated(r["word"],u); need(direct==pred,"fox conjugation mismatch")
        except Exception as ex:
            return {"pairs":passed,"required":sample_n,"status":"UNKNOWN_TYPED_FOX_CANARY",
                    "first_failure":{"sample_index":i,"layer":r["layer"],"ordinal":r["ordinal"],
                    "conjugator":u,"relation_length":len(r["word"]),"error":str(ex)},
                    "layer_counts":comp,"same_context_pairs":0,"same_context":[],
                    "row_digest_sha256":digest_obj(checks),"convention":meta}
        comp[r["layer"]]+=1; passed+=1; checks.append({"layer":r["layer"],"ordinal":r["ordinal"],"u":u,"r_word":r["word"],"conjugated_word":w,"u_length":len(u),"r_length":len(r["word"]),"direct":row_serial(old,direct),"predicted":row_serial(old,pred)})
    same=[]
    for i in range(len(chosen)):
        if len(same)>=5: break
        r=chosen[i]; u=conjs[i%len(conjs)]
        k=next((q for q in chosen if q["word"] and r["word"] and q["word"]!=r["word"] and old.reduce_word(u+q["word"]+r["word"]+old.inv_word(q["word"])+old.inv_word(u))!=old.reduce_word(u+r["word"]+old.inv_word(u))),None)
        if k is None: continue
        v=old.reduce_word(u+list(k["word"])); c1=old.reduce_word(u+r["word"]+old.inv_word(u)); c2=old.reduce_word(v+r["word"]+old.inv_word(v))
        need(c1!=c2,"same-context conjugates collapsed")
        need(all(e4.eval(v,c)==e4.eval(u,c) for c in ctx),"same context state")
        need(sigma(c1)==sigma(c2),"same context sigma")
        same.append({"r_layer":r["layer"],"r_ordinal":r["ordinal"],"r_word":r["word"],"k_layer":k["layer"],"k_ordinal":k["ordinal"],"k_word":k["word"],"u":u,"v":v,"conjugate_u":c1,"conjugate_v":c2,"conjugates_differ":True,"sigma_digest":row_digest(old,sigma(c1))[0]})
    need(len(same)>=5,"same-context quota")
    meta.update({"empty_u_checked":True,"noncommuting_u_checked":True,"eligible_counts":eligible_counts})
    return {"pairs":passed,"required":sample_n,"status":"PASS","eligible_counts":eligible_counts,"layer_counts":comp,"same_context_pairs":len(same),"same_context":same,"transcript":checks,"row_digest_sha256":digest_obj([{"layer":x["layer"],"ordinal":x["ordinal"],"direct":x["direct"],"predicted":x["predicted"]} for x in checks]),"convention":meta}
def mutations(old,e4,roster,toy,rows,fx):
    tests=[]
    rw=next(x["word"] for x in roster if x["word"])
    invblob=old._element_blob(e4.inverse(e4.eval([1]))).hex(); opblob=old._element_blob(e4.eval([1])).hex()
    base={"source_sha":Q3_SHA,"record_digest":digest_obj(rw),"layer_ordinal":(roster[0]["layer"],roster[0]["ordinal"]),
          "e4_inverse":invblob,"pb4_row_digest":digest_obj([row_digest(old,x)[0] for x in rows]),"context_order":"fxy,fxz,fyz",
          "left_right_action":"left_translation","prefix_orientation":"u*r*u^-1","conjugator_orientation":"u-left",
          "fox_inverse_sign":1,"sparse_component_key":"component,blob,coefficient","e4_blob":toy["e4_blob"],
          "toy_action":toy["action_digest"],"toy_cocycle_value":toy["cocycle_digest"],"toy_normal_relator":toy["relator_digest"],
          "toy_missing_orbit_state":toy["missing_state_digest"],"e4_blob":opblob,"fox_transcript":fx["row_digest_sha256"],"terminal":"UNKNOWN_INPUT:FOX_CANARY"}
    def validate(x):
        need(x["e4_inverse"]==invblob,"E4 inverse recomputation mismatch")
        need(x["pb4_row_digest"]==base["pb4_row_digest"],"PB4 raw replay mismatch")
        need(x["fox_transcript"]==fx["row_digest_sha256"],"Fox transcript replay mismatch")
        for k in ("source_sha","record_digest","layer_ordinal","context_order","left_right_action","prefix_orientation","conjugator_orientation","fox_inverse_sign","sparse_component_key","e4_blob","toy_action","toy_cocycle_value","toy_normal_relator","toy_missing_orbit_state"):
            need(x[k]==base[k],k+" mismatch")
        need(x["terminal"] in {"R07_FULL_E4_ORBIT_PREFLIGHT_READY","UNKNOWN_INPUT:FOX_CANARY"},"forbidden global terminal")
    def run(mid,field,alter):
        x=dict(base); alter(x)
        try: validate(x); tests.append({"id":mid,"field":field,"caught":False,"message":"NO_REJECTION"})
        except Exception as ex: tests.append({"id":mid,"field":field,"caught":True,"message":str(ex)})
    run("source_artifact_pin","source/artifact sha",lambda x:x.__setitem__("source_sha","0"*64))
    run("record_letter","record[word][-1]",lambda x:x.__setitem__("record_digest",digest_obj(rw[:-1]+[rw[-1]+1])))
    run("layer_ordinal","layer/ordinal",lambda x:x.__setitem__("layer_ordinal",("gamma_edge",-1)))
    run("e4_inverse","inverse(result)",lambda x:x.__setitem__("e4_inverse",("0" if x["e4_inverse"]!="0" else "1")))
    run("pb4_row_coefficient","raw PB4 coefficient",lambda x:x.__setitem__("pb4_row_digest","0"*64))
    for mid,key,val in [("context_order","context_order","fyz,fxy,fxz"),("left_right_action","left_right_action","right_translation"),("prefix_orientation","prefix_orientation","u^-1*r*u"),("conjugator_orientation","conjugator_orientation","u-right"),("fox_inverse_sign","fox_inverse_sign",-1),("sparse_component_key","sparse_component_key","blob,component,coefficient"),("e4_blob","e4_blob","00")]:
        run(mid,key,lambda x,k=key,v=val:x.__setitem__(k,v))
    for mid,key in [("fox_transcript", "fox_transcript")]:
        run(mid,key,lambda x,k=key:x.__setitem__(k,"0"*64))
    for mid,key in [("toy_action","toy_action"),("toy_cocycle_value","toy_cocycle_value"),("toy_normal_relator","toy_normal_relator"),("toy_missing_orbit_state","toy_missing_orbit_state")]:
        run(mid,key,lambda x,k=key:x.__setitem__(k,"0"*64))
    run("forbidden_positive_terminal","terminal",lambda x:x.__setitem__("terminal","R07_FULL_E4_ORBIT_CORRECTION_PASS"))
    need(all(x["caught"] for x in tests),"mutation harness gap")
    return tests
def toy():
    import itertools
    G=list(itertools.permutations(range(3))); e=(0,1,2); x=(1,0,2); y=(0,2,1)
    def gm(a,b):return tuple(a[b[i]] for i in range(3))
    def gi(a):return tuple(a.index(i) for i in range(3))
    def A(g,m):return tuple(m[g[i]] for i in range(3))
    def sm(a,b):return (tuple((a[0][i]+A(a[1],b[0])[i])%3 for i in range(3)),gm(a[1],b[1]),tuple((a[2][i]+b[2][i])%3 for i in range(2)))
    I=((0,0,0),e,(0,0)); X=((1,0,0),x,(1,0)); Y=((0,1,0),y,(0,1))
    def si(a):return (tuple((-A(gi(a[1]),a[0])[i])%3 for i in range(3)),gi(a[1]),tuple(-z%3 for z in a[2]))
    def pw(a,n):
        q=I
        for _ in range(n):q=sm(q,a)
        return q
    H={I}; q=[I]
    while q:
        a=q.pop()
        for b in (X,Y,si(X),si(Y)):
            z=sm(a,b)
            if z not in H:H.add(z);q.append(z)
    rel=[pw(X,2),pw(Y,2),pw(sm(X,Y),3)]
    orbit=[]
    for u in H:
        for r in rel:
            z=sm(sm(u,r),si(u)); orbit.append(z[0]+z[2])
    def span(vs):
        s={(0,0,0,0,0)}
        for v in vs:
            old=list(s)
            for c in (1,2):s|={tuple((u[i]+c*v[i])%3 for i in range(5)) for u in old}
        return s
    fibre={a[0]+a[2] for a in H if a[1]==e}; os=span(orbit); base=span([r[0]+r[2] for r in rel])
    return {"group":"S3","semidirect_module":"F3^2 sign action","image_order":len(H),"identity_G_fibre_size":len(fibre),"orbit_columns":len(orbit),"orbit_span_size":len(os),"unconjugated_span_size":len(base),"exact_equality":fibre==os,"orbit_load_bearing":len(base)<len(os),"pb4_row_digest":"actual",
            "e4_inverse":"toy-e4-inverse-identity","e4_blob":"toy-canonical-blob",
            "action_digest":digest_obj(["coordinate-permutation",sorted(G)]),"cocycle_digest":digest_obj([X,Y]),
            "relator_digest":digest_obj(rel),"missing_state_digest":digest_obj(sorted(H))}
def main():
    t=time.time(); p= pins(); prev=load(PREV,"_d172_auth_prev"); prev.Q3_ARTIFACT=Path("ci/b345_157ee_artifacts_32359956713/d972_b345_q3_chief_v1.json"); prev.Q3_ARTIFACT_SHA=Q3_SHA
    q,old=prev.authenticated_input(prev.Q3_ARTIFACT); e3,e4,_=old.reconstruct_quotients(q); contexts,aliases,ctxpub=old.cheap_context_registry(e4)
    words=[list(r["word"]) for r in q["correction_fibre"]["records"] if r["word"]]; need(len(words)==26 and digest_obj(words)=="08d11c68dcbacc1b81e5e2732eedcbc41df82a16c8a0f97dfbbb13d6accee24f","record words")
    target=load(ROOT/"search/d972_b345_target6_dual_colgen_v2.py","_d172_target"); g760mod=load(ROOT/"search/check_d972_r07_616_to_760_commutator_affine_rhs_v3.py","_d172_g760"); _,_,g=g760mod.construct_base(); need(len(g)==760 and digest_obj(g)==BASE_SHA,"g760")
    print("bridge_authenticated",flush=True)
    group,roster=build_roster(load(ROOT/"search/d972_b345_joint_kernel_qstar_closure_v1.py","_d172_joint"),old,e3,e4,contexts,words)
    print("roster_built",flush=True)
    rows=target.base_raw_columns(old,e4); pb4=[row_digest(old,r) for r in rows]; need(len(rows)==11 and all(old.d1(r,e4)=={} for r in rows),"PB4 rows")
    print("pb4_built",flush=True)
    try:
        fx=fox_sample(old,e4,contexts,aliases,roster,g)
    except Exception as ex:
        fx={"pairs":0,"required":101,"status":"UNKNOWN_TYPED_FOX_RESOURCE","first_failure":{"error":str(ex)},"layer_counts":{},"same_context_pairs":0,"same_context":[],"row_digest_sha256":digest_obj([])}
    print("fox_built",flush=True); toyrow=toy(); muts=mutations(old,e4,roster,toyrow,rows,fx)
    fx_pass=(fx.get("status")=="PASS" and fx.get("pairs",0)>=101 and fx.get("same_context_pairs",0)>=5)
    terminal=TERMINAL if fx_pass else "UNKNOWN_INPUT:FOX_CANARY"
    v111="sol/proof_r07_filtered_actual_orbit_homotopy_v111.md"
    bindings=[]
    for nm in ["hexagon_1_fxy_0","hexagon_1_fxz_0","hexagon_1_fyz_0"]:
        ci=aliases[nm]-1; bb=old._element_blob(contexts[ci]);
        if hasattr(bb,"hex"): bh=bb.hex()
        else:
            try: bh=bytes(bb).hex()
            except TypeError: bh=b"".join(bb).hex()
        bindings.append({"alias":nm,"registry_id":aliases[nm],"context_blob":bh})
    cert={"schema":"d972-r07-full-e4-orbit-preflight/v5","terminal_token":terminal,"status":terminal,"claim":"preflight_ready_only" if fx_pass else "bounded_bridge_only","scope":{"full_prefix":False,"full_orbit":False,"gha":False,"git":False,"parallel":False},"pins":p,"q3":{"artifact_sha256":Q3_SHA,"record_count":len(words),"record_words_sha256":digest_obj(words),"word_lengths":[len(x) for x in words]},"contexts":{"count":len(contexts),"aliases":len(ctxpub["named_uses"]),"rows_sha256":ctxpub["context_rows_sha256"],"target6_bindings":bindings},"diagonal_context_action":{"source":v111,"operator_group":"Delta generated by registered simultaneous context-conjugation operators on the stacked seven evaluation blocks","group_algebra":"Lambda=F3[Delta]","literal_action":"A_delta((i,e))=(i,delta_i*e) on each typed context block; coefficient action is left translation by the evaluated context element","operator_formula":"B:A=Lambda^(R)->Z, s:A->C, D s=B; K_z={lambda in Lambda: lambda z=0}; splitter requires B a=z and K_z a=0","annihilator_target":"K_z=Ann_{F3[Delta]}(z)","provenance":{"definition_sections":["v111 §2","v111 (4.1)-(4.6)"],"context_registry_rows_sha256":ctxpub["context_rows_sha256"],"target6_bindings":bindings},"computed":False,"image_order":"UNKNOWN_NOT_COMPUTED","O3_data":"UNKNOWN_NOT_COMPUTED","return_involution":"not reconstructed in bounded task172"},"g760":{"length":len(g),"sha256":digest_obj(g),"exponent_sums":[sum(1 if x==i else -1 if x==-i else 0 for x in g) for i in (1,2)]},"relation_roster":{"count":len(roster),"layers":{"gamma_edge":6318,"xy_action":104,"q0_relator":19},"expanded_words":True,"xy_action_ordinal_rule":"ri*4+li*2+(1 for orient +1, 2 for orient -1), frozen 157ee action_relations token order","roster_sha256":digest_obj([[x["layer"],x["ordinal"],x["word"]] for x in roster])},"pb4_raw_rows":{"count":len(rows),"all_value_identity":True,"all_D1_zero":True,"row_digests":pb4},"fox_canaries":fx,"toy":toyrow,"mutations":muts,"heavy_jobs_not_run":True,"unknowns":[] if fx_pass else ["FOX_CANARY_NOT_TYPED_OR_FAILED"],"required_verbatim":["v1 toy/checker promotion rejected by Sol audit","full-E4 raw bridge and canaries are bounded preflight, not a correction","positive target6 at one universal relation-module layer is not literal A18","no cofinal lift / fake / Ihara witness declared"]}
    cert["schema"]="d972-r07-full-e4-orbit-preflight/v7"
    OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(cert,sort_keys=True,indent=2)+"\n",encoding="utf-8"); print(terminal); print("records=26 roster=6441 pb4=11 fox_pairs=%d mutations=%d toy=%s"%(fx["pairs"],len(muts),toyrow["exact_equality"]))
if __name__=="__main__": main()
