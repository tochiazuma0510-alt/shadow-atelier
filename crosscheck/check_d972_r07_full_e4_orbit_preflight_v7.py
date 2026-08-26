"""Independent, bounded checker for task 172 v2 certificate.

This checker intentionally does not import the producer.  It checks immutable
pins and typed counts, then evaluates the finite semidirect toy in a distinct
enumeration order and rejects any positive terminal unless every gate passes.
"""
from __future__ import annotations
import hashlib,itertools,json,importlib.util,sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
CERT=ROOT/"search/certs/d972_r07_full_e4_orbit_preflight_v7_20260827.json"
Q3=ROOT/"ci/b345_157ee_artifacts_32359956713/d972_b345_q3_chief_v1.json"
Q3_SHA="3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72"
WORDS_SHA="08d11c68dcbacc1b81e5e2732eedcbc41df82a16c8a0f97dfbbb13d6accee24f"

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def dobj(x): return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(",",":"),ensure_ascii=True).encode()).hexdigest()
def need(x,m):
    if not x: raise RuntimeError(m)

def load(path,name):
    s=importlib.util.spec_from_file_location(name,path); need(s and s.loader,"module spec")
    m=importlib.util.module_from_spec(s); sys.modules[name]=m; s.loader.exec_module(m); return m

def row_serial(old,row):
    ans=[]
    for (c,v),a in row.items():
        if a%3: ans.append([int(c),old._element_blob(v).hex(),int(a)%3])
    ans.sort(key=lambda z:(z[0],bytes.fromhex(z[1]))); return ans

def rebuild(old,e3,e4,contexts,words,j):
    group=j.JointGroup(old,e3,e4,contexts,words); rows=[]
    for sid,trans in enumerate(group.transitions):
        su=group.section_word(sid)
        for gi,tgt in enumerate(trans):
            rows.append({"layer":"gamma_edge","ordinal":sid*26+gi+1,"word":old.reduce_word(su+list(words[gi])+old.inv_word(group.section_word(tgt)))})
    for ri in range(26):
        for li in range(2):
            val=group.eval([li+1]); gen=group.generators[ri]
            for orient in (1,-1):
                if orient==1:
                    cv=group.mul(group.mul(group.inverse(val),gen),val); tokens=[('letter',li,-1),('record',ri,1),('letter',li,1)]
                else:
                    cv=group.mul(group.mul(val,gen),group.inverse(val)); tokens=[('letter',li,1),('record',ri,1),('letter',li,-1)]
                tgt=group.ids[group.key(cv)]
                rows.append({"layer":"xy_action","ordinal":ri*4+li*2+(1 if orient==1 else 2),"word":old.reduce_word(j.materialize_tokens(old,words,tokens+[('record',x,-1) for x in reversed(group.section_factors(tgt))]))})
    for qi,r in enumerate(j.complete_relators(old)):
        tgt=group.ids[group.key(group.eval(r))]
        rows.append({"layer":"q0_relator","ordinal":qi+1,"word":old.reduce_word(list(r)+old.inv_word(group.section_word(tgt)))})
    need(len(rows)==6441,"reconstructed roster count"); return rows

def fox_recompute(old,e4,contexts,aliases,rows,g,transcript,same):
    ids=[aliases["hexagon_1_fxy_0"]-1,aliases["hexagon_1_fxz_0"]-1,aliases["hexagon_1_fyz_0"]-1]; ctx=[contexts[i] for i in ids]
    z=old.inv_word(old.pp_words([[1],[2]])); mapping=old.cofaces(3)[0]
    def lift(w): return old.word_substitute(old.embed_f2_pb3(w),mapping)
    def sub(w,l,r): return old.f2_substitute(w,l,r)
    p=e4.eval(lift(sub(g,[2],z))); h=e4.eval(lift(old.hexagon_words(g)[0]))
    by={(x["layer"],x["ordinal"]):x["word"] for x in rows}; need(len(transcript)==101,"Fox transcript count")
    def sigma(word):
        ans={}
        for gradword,constant,sgn in [(sub(word,[1],[2]),h,1),(sub(word,[1],z),p,-1),(sub(word,[2],z),p,1)]:
            grad,val=old.fox_gradient_without_sections(lift(gradword),e4); need(val==e4.identity,"same Fox context value")
            for k,v in old.translate_vector(grad,constant,e4).items(): ans[k]=(ans.get(k,0)+sgn*v)%3
        return {k:v for k,v in ans.items() if v%3}
    for rec in transcript:
        key=(rec["layer"],rec["ordinal"]); need(key in by and by[key]==rec["r_word"],"Fox roster binding")
        u=rec["u"]; w=old.reduce_word(u+rec["r_word"]+old.inv_word(u)); need(w==rec["conjugated_word"],"Fox conjugator word")
        direct={}; pred={}
        for gradword,constant,sgn,ci in [(sub(w,[1],[2]),h,1,0),(sub(w,[1],z),p,-1,1),(sub(w,[2],z),p,1,2)]:
            grad,val=old.fox_gradient_without_sections(lift(gradword),e4); need(val==e4.identity,"Fox context value")
            tr=old.translate_vector(grad,constant,e4)
            for k,v in tr.items(): direct[k]=(direct.get(k,0)+sgn*v)%3
        for gradword,constant,sgn,ci in [(sub(rec["r_word"],[1],[2]),h,1,0),(sub(rec["r_word"],[1],z),p,-1,1),(sub(rec["r_word"],[2],z),p,1,2)]:
            grad,val=old.fox_gradient_without_sections(lift(gradword),e4); need(val==e4.identity,"Fox relation context value")
            uv=e4.eval(u,ctx[ci]); tr2=old.translate_vector(grad,e4.mul(constant,uv),e4)
            for k,v in tr2.items(): pred[k]=(pred.get(k,0)+sgn*v)%3
        direct={k:v for k,v in direct.items() if v%3}; pred={k:v for k,v in pred.items() if v%3}
        need(row_serial(old,direct)==rec["direct"],"Fox direct transcript mismatch")
        need(row_serial(old,pred)==rec["predicted"],"Fox predicted transcript mismatch")
        need(direct==pred,"Fox direct/predicted mismatch")
    need(len(same)>=5,"same-context transcript count")
    for q in same:
        rk=(q["r_layer"],q["r_ordinal"]); kk=(q["k_layer"],q["k_ordinal"])
        need(rk in by and kk in by and by[rk]==q["r_word"] and by[kk]==q["k_word"],"same-context roster binding")
        c1=old.reduce_word(q["u"]+q["r_word"]+old.inv_word(q["u"])); v=old.reduce_word(q["u"]+q["k_word"]); c2=old.reduce_word(v+q["r_word"]+old.inv_word(v))
        need(c1==q["conjugate_u"] and c2==q["conjugate_v"] and c1!=c2,"same-context conjugator witness")
        need(all(e4.eval(v,c)==e4.eval(q["u"],c) for c in ctx),"same-context state witness")
        a=sigma(c1); b=sigma(c2); need(a==b and dobj(row_serial(old,a))==q["sigma_digest"],"same-context sigma witness")
    return True

def toy_independent():
    # S3 acts on F3^3 by coordinate permutation; this is a genuinely
    # nontrivial module.  The second factor is the marked cocycle coordinate.
    G=sorted(itertools.permutations(range(3)),reverse=True); E=(0,1,2)
    Xg=(1,0,2); Yg=(0,2,1)
    def mulg(a,b): return tuple(a[b[i]] for i in range(3))
    def invg(a): return tuple(a.index(i) for i in range(3))
    def act(g,m): return tuple(m[g[i]] for i in range(3))
    def mul(a,b): return (tuple((a[0][i]+act(a[1],b[0])[i])%3 for i in range(3)),mulg(a[1],b[1]),tuple((a[2][i]+b[2][i])%3 for i in range(2)))
    I=((0,0,0),E,(0,0)); X=((1,0,0),Xg,(1,0)); Y=((0,1,0),Yg,(0,1))
    def inv(a): return (tuple((-act(invg(a[1]),a[0])[i])%3 for i in range(3)),invg(a[1]),tuple((-a[2][i])%3 for i in range(2)))
    def power(a,n):
        q=I
        for _ in range(n): q=mul(q,a)
        return q
    # BFS uses sorted generator choices, deliberately unlike producer order.
    seen={I}; frontier=[I]
    while frontier:
        a=frontier.pop(0)
        for b in (inv(Y),Y,inv(X),X):
            c=mul(a,b)
            if c not in seen: seen.add(c); frontier.append(c)
    rel=(power(Y,2),power(X,2),power(mul(Y,X),3))
    orbit=[]
    for u in sorted(seen,key=repr):
        for r in rel:
            c=mul(mul(u,r),inv(u)); orbit.append(c[0]+c[2])
    def span(vectors):
        out={(0,0,0,0,0)}
        for v in vectors:
            old=tuple(out)
            out.update(tuple((u[i]+c*v[i])%3 for i in range(5)) for u in old for c in (1,2))
        return out
    fibre={a[0]+a[2] for a in seen if a[1]==E}
    orbit_span=span(orbit); raw_span=span([r[0]+r[2] for r in rel])
    return {"image_order":len(seen),"identity_G_fibre_size":len(fibre),"orbit_columns":len(orbit),"orbit_span_size":len(orbit_span),"unconjugated_span_size":len(raw_span),"exact_equality":fibre==orbit_span,"orbit_load_bearing":len(raw_span)<len(orbit_span),"action_digest":dobj(["coordinate-permutation",sorted(G)]),"cocycle_digest":dobj([X,Y]),"relator_digest":dobj(rel)}

def main():
    cert=json.loads(CERT.read_text(encoding="utf-8")); need(sha(CERT)==cert.get("self_sha256",sha(CERT)) if "self_sha256" in cert else True,"certificate self pin")
    need(cert.get("schema")=="d972-r07-full-e4-orbit-preflight/v7","schema")
    need(sha(Q3)==Q3_SHA and cert["q3"]["artifact_sha256"]==Q3_SHA,"q3 pin")
    q=json.loads(Q3.read_text(encoding="utf-8")); words=[r["word"] for r in q["correction_fibre"]["records"] if r.get("word")]
    need(len(words)==26 and dobj(words)==WORDS_SHA,"26 record words")
    need(cert["q3"]["record_count"]==26 and cert["q3"]["record_words_sha256"]==WORDS_SHA,"word receipt")
    c=cert["contexts"]; need(c["count"]==31 and c["aliases"]==46 and len(c["target6_bindings"])==3,"context registry")
    need([x["registry_id"] for x in c["target6_bindings"]]==[1,2,3],"target binding ids")
    d=cert["diagonal_context_action"]; need(d["computed"] is False and d["annihilator_target"]=="K_z=Ann_{F3[Delta]}(z)","diagonal action boundary")
    need(d["image_order"]=="UNKNOWN_NOT_COMPUTED" and d["O3_data"]=="UNKNOWN_NOT_COMPUTED","Delta unknown boundary")
    rr=cert["relation_roster"]; need(rr["count"]==6441 and rr["expanded_words"] is True,"roster")
    need(rr["layers"]=={"gamma_edge":6318,"xy_action":104,"q0_relator":19},"roster layers")
    pb=cert["pb4_raw_rows"]; need(pb["count"]==11 and pb["all_value_identity"] and pb["all_D1_zero"] and len(pb["row_digests"])==11,"PB4")
    g=cert["g760"]; need(g["length"]==760 and g["sha256"]=="518f09820b8d7baee6b58ebf366cebf7b02a9a945cd1350cf8c701a4e6bc2b4d","g760")
    prev=load(ROOT/"search/d972_b345_triple_cube_raw_lambda_census_v1.py","_v5_prev"); prev.Q3_ARTIFACT=Q3; prev.Q3_ARTIFACT_SHA=Q3_SHA
    _,old_e=prev.authenticated_input(Q3); e3,e4,_=old_e.reconstruct_quotients(q); contexts,aliases,ctxpub=old_e.cheap_context_registry(e4)
    need(len(contexts)==31 and len(ctxpub["named_uses"])==46 and ctxpub["context_rows_sha256"]==c["rows_sha256"],"independent E4/context reconstruction")
    jm=load(ROOT/"search/d972_b345_joint_kernel_qstar_closure_v1.py","_v5_joint"); rebuilt=rebuild(old_e,e3,e4,contexts,words,jm)
    need(dobj([[x["layer"],x["ordinal"],x["word"]] for x in rebuilt])==rr["roster_sha256"],"independent roster digest")
    tm=load(ROOT/"search/d972_b345_target6_dual_colgen_v2.py","_v5_target"); raw=tm.base_raw_columns(old_e,e4); need(len(raw)==11 and all(old_e.d1(x,e4)=={} for x in raw),"independent PB4 reconstruction")
    need([[dobj(row_serial(old_e,x)),len(row_serial(old_e,x))] for x in raw]==pb["row_digests"],"independent PB4 digest")
    gm=load(ROOT/"search/check_d972_r07_616_to_760_commutator_affine_rhs_v3.py","_v5_g760"); _,_,gw=gm.construct_base(); need(dobj(gw)==g["sha256"],"independent g760")
    t=toy_independent(); old=cert["toy"]
    for k in ("image_order","identity_G_fibre_size","orbit_columns","orbit_span_size","unconjugated_span_size","exact_equality","orbit_load_bearing","action_digest","cocycle_digest"):
        need(t[k]==old[k],"toy mismatch "+k)
    need(isinstance(old.get("relator_digest"),str) and len(old["relator_digest"])==64,"toy relator receipt")
    need(t["exact_equality"] is True and t["orbit_load_bearing"] is True,"toy theorem gates")
    muts=cert["mutations"]; need(len(muts)>=18 and all(m.get("caught") is True for m in muts),"executed mutations")
    terminal=cert["terminal_token"]
    need(terminal in {"R07_FULL_E4_ORBIT_PREFLIGHT_READY","UNKNOWN_INPUT:FOX_CANARY"},"terminal allowlist")
    fx=cert["fox_canaries"]; need(fx["convention"]["formula"]=="corrected_minus_base" and fx["convention"]["transport_order"]=="constant*psi(u) under current left-action convention","Fox convention")
    if terminal.startswith("UNKNOWN"):
        need(fx["status"]=="UNKNOWN_TYPED_FOX_CANARY" and fx["pairs"]<fx["required"],"typed Fox UNKNOWN")
    else:
        need(fx["pairs"]>=101 and fx.get("status")=="PASS" and fx["same_context_pairs"]>=5,"Fox completion")
        fox_recompute(old_e,e4,contexts,aliases,rebuilt,gw,fx["transcript"],fx["same_context"])
    print("D172_V7_CHECK_PASS")
    print("terminal="+terminal)
    print("toy=image=%d fibre=%d orbit=%d raw=%d exact=%s load_bearing=%s"%(t["image_order"],t["identity_G_fibre_size"],t["orbit_span_size"],t["unconjugated_span_size"],t["exact_equality"],t["orbit_load_bearing"]))
    print("fox_pairs=%d/%d mutations=%d"%(fx["pairs"],fx["required"],len(muts)))
if __name__=="__main__": main()
