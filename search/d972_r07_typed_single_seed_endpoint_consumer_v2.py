#!/usr/bin/env python3
from __future__ import annotations
import argparse, copy, hashlib, json, time
from collections import deque
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SCHEMA="d972-r07-typed-single-seed-endpoint-consumer/v2"; SELFTEST_SCHEMA=SCHEMA+"/selftest"
SELFTEST="R07_TYPED_SINGLE_SEED_ENDPOINT_CONSUMER_V2_SELFTEST_PASS"; MEMBER="PROJECTED_MEMBER_SEED"; NONMEMBER="PROJECTED_NONMEMBER_DUAL"
UNKNOWN_INPUT="UNKNOWN_INPUT"; UNKNOWN_RESOURCE="UNKNOWN_RESOURCE"
TASK226="ci/in/d972_r07_actual_two_word_endpoint_specializer_v2.json"; TASK226_VERDICT="ci/in/d972_r07_actual_two_word_endpoint_specializer_v2.verdict.json"; TASK226_BINDING="ci/in/d972_r07_actual_two_word_endpoint_specializer_v2.binding.json"
FIXTURE="search/certs/d972_r07_typed_single_seed_endpoint_consumer_selftest_v2_20260828.json"; TASK226_SCHEMA="d972-r07-actual-two-word-endpoint-specializer/v2"; TASK226_COMPLETE="R07_ACTUAL_TWO_WORD_ENDPOINT_SPECIALIZER_V2_COMPLETE"
MUTATIONS=["task226_binding","translated_provenance_keyset","original_ancestry","w_abi_binding","u0_abi_binding","target_abi_binding","noncentral_action_order","occurrence_basis_row","occurrence_ancestry","queue_invariance","orbit_vs_486","orbit_vs_729","premature_block_sum","member_lambda_u0","member_kappa_w","member_target","quotient_zero","dual_orbit_annihilation","dual_486_annihilation","dual_729_annihilation","dual_target_pairing","terminal_vocabulary","resource_terminal","forbidden_conclusion"]
ACTUAL_ANCESTRY={"source":"task179_A18","substitution":"PB3/PB4_literal","prefix":"task198_one_based_signed"}
EXPECTED_GATES={"task226_binding":"ABI_SCHEMA_MODULUS","translated_provenance_keyset":"U0_TRANSLATED_PROVENANCE","original_ancestry":"U0_ORIGINAL_PROVENANCE","w_abi_binding":"ABI_W_RECOMPUTE","u0_abi_binding":"ABI_OCCURRENCE_U0_RECOMPUTE","target_abi_binding":"CASE_TARGET_BINDING","noncentral_action_order":"CASE_ACTION_ORDER","occurrence_basis_row":"CASE_OCCURRENCE_BASIS","occurrence_ancestry":"CASE_OCCURRENCE_ANCESTRY","queue_invariance":"CASE_QUEUE_INVARIANCE","orbit_vs_486":"CASE_ORBIT_486","orbit_vs_729":"CASE_ORBIT_729","premature_block_sum":"CASE_BLOCK_BASIS","member_lambda_u0":"CASE_MEMBER_LAMBDA","member_kappa_w":"CASE_MEMBER_KAPPA","member_target":"CASE_MEMBER_TARGET","quotient_zero":"CASE_QUOTIENT_ZERO","dual_orbit_annihilation":"CASE_DUAL_ORBIT","dual_486_annihilation":"CASE_DUAL_486","dual_729_annihilation":"CASE_DUAL_729","dual_target_pairing":"CASE_DUAL_TARGET","terminal_vocabulary":"CASE_TERMINAL","resource_terminal":"CASE_RESOURCE","forbidden_conclusion":"CASE_FORBIDDEN"}
CAPS={"input_bytes":500000000,"actor_operations":2000000,"occurrence_support":2000000,"orbit_actions":2000000,"occurrence_rank_increases":486,"block_rank_increases":486,"block_rows":100000,"checker_roster":729,"dual_work":1000000,"mutation_work":100000,"serialized_bytes":2000000000,"wall_seconds":21600}
class InputStop(RuntimeError): pass
class MutationAccepted(RuntimeError): pass
class ResourceStop(RuntimeError):
    def __init__(self,phase,cap,value,limit): super().__init__(f"phase={phase}:cap={cap}:value={value}:limit={limit}"); self.phase,self.cap,self.value,self.limit=phase,cap,value,limit
class Budget:
    def __init__(self): self.started=time.monotonic(); self.used={k:0 for k in CAPS}
    def bump(self,key,count,phase):
        self.used[key]+=count
        if self.used[key]>CAPS[key]: raise ResourceStop(phase,key,self.used[key],CAPS[key])
        elapsed=time.monotonic()-self.started
        if elapsed>CAPS["wall_seconds"]: raise ResourceStop(phase,"wall_seconds",elapsed,CAPS["wall_seconds"])
def canonical(v): return json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=True).encode("ascii")
def digest_obj(v): return hashlib.sha256(canonical(v)).hexdigest()
def require(ok,msg):
    if ok is not True: raise InputStop(msg)
def mod(v): return v%9
def dims(width): require(width in (4,10),"Q_KEY_WIDTH"); return (3,1) if width==4 else (6,4)
def bracket(width,i,j):
    d,c=dims(width)
    table={(0,1):(1,),(0,2):(-1,),(1,2):(1,)} if d==3 else {(0,1):(1,0,0,0),(0,3):(-1,0,0,0),(1,3):(1,0,0,0),(0,2):(0,1,0,0),(0,4):(0,-1,0,0),(2,4):(0,1,0,0),(1,2):(0,0,1,0),(1,5):(0,0,-1,0),(2,5):(0,0,1,0),(3,4):(0,0,0,1),(3,5):(0,0,0,-1),(4,5):(0,0,0,1)}
    return tuple(table.get((i,j),(0,)*c))
def qmul(a,b,width,budget=None,phase="qmul"):
    d,c=dims(width); out=[mod(a[d+i]+b[d+i]) for i in range(c)]
    for i in range(d):
        for j in range(i+1,d):
            for k,v in enumerate(bracket(width,i,j)): out[k]=mod(out[k]-a[j]*b[i]*v)
    if budget: budget.bump("actor_operations",1,phase); budget.bump("orbit_actions",1,phase)
    return tuple(mod(a[i]+b[i]) for i in range(d))+tuple(out)
def qinv(a,width,budget=None):
    d,c=dims(width); out=list(tuple(mod(-v) for v in a)); z=out[d:]
    for i in range(d):
        for j in range(i+1,d):
            for k,v in enumerate(bracket(width,i,j)): z[k]=mod(z[k]-a[i]*a[j]*v)
    if budget: budget.bump("actor_operations",1,"q_inverse")
    return tuple(out[:d]+z)
def qpow(a,n,width,budget=None):
    out=(0,)*width
    for _ in range(n%9): out=qmul(out,a,width,budget,"q_power")
    return out
def actor_mul(a,b): return (mod(a[0]+b[0]),mod(a[1]+b[1]),mod(a[2]+b[2]-b[0]*a[1]))
def actor_inv(a): return (mod(-a[0]),mod(-a[1]),mod(-a[2]-a[0]*a[1]))
def sparse_add(a,b):
    out=dict(a)
    for k,v in b.items(): out[k]=(out.get(k,0)+v)%3; out.pop(k,None) if out[k]==0 else None
    return out
def sparse_scale(a,s): return {k:(v*s)%3 for k,v in a.items() if (v*s)%3}
def encode_sparse(row): return [[list(k),v] for k,v in sorted(row.items())]
def parse_sparse(value,width,label):
    require(type(value) is list,label+"_TYPE"); out={}
    for term in value:
        key,co=(term.get("key"),term.get("coefficient")) if type(term) is dict else (term[0],term[1])
        require(type(key) is list and len(key)==width and all(type(x) is int and 0<=x<9 for x in key) and type(co) is int and co in (1,2),label+"_TERM")
        k=tuple(key); out[k]=(out.get(k,0)+co)%3
    out={k:v for k,v in out.items() if v}; require(value==encode_sparse(out),label+"_CANONICAL"); return out
def encode_vector(row): return [[list(k[1]),k[0],v] for k,v in sorted(row.items())]
def occurrence_width(item): width=item.get("key_width"); require(width in (4,10) and item.get("q_degree")== (3 if width==4 else 4),"OCCURRENCE_WIDTH"); return width
def occurrence_actor(actor,item,budget=None):
    width=occurrence_width(item); x=tuple(item["q_o(x)"]); y=tuple(item["q_o(y)"]); h=qmul(qmul(qmul(qinv(x,width,budget),qinv(y,width,budget),width,budget),x,width,budget),y,width,budget)
    return qmul(qmul(qpow(x,actor[0],width,budget),qpow(y,actor[1],width,budget),width,budget),qpow(h,actor[2],width,budget),width,budget)
def actor_translate(row,actor,items,budget=None):
    out={}
    for (ordinal,key),v in row.items():
        item=items[ordinal]; width=occurrence_width(item); p=tuple(item["p_o"]); g=occurrence_actor(actor,item,budget); kg=qmul(qmul(p,g,width,budget),qinv(p,width,budget),width,budget); nk=(ordinal,qmul(kg,key,width,budget,"actor_translate")); out[nk]=(out.get(nk,0)+v)%3
    return {k:v for k,v in out.items() if v}
def action_group_ring(coeff,row,items,budget=None):
    out={}
    for actor,v in coeff.items(): out=sparse_add(out,sparse_scale(actor_translate(row,actor,items,budget),v))
    return out
def add_echelon(basis,row,ancestry,cap,budget,phase):
    work=dict(row); anc=dict(ancestry)
    for pivot in sorted(basis):
        if pivot not in work: continue
        s=work[pivot]; work=sparse_add(work,sparse_scale(basis[pivot][0],-s)); keys=set(anc)|set(basis[pivot][1]); anc={k:(anc.get(k,0)-s*basis[pivot][1].get(k,0))%3 for k in keys}; anc={k:v for k,v in anc.items() if v}
    if not work: return False,None
    require(len(basis)<cap,phase+":RANK_CAP_EXCEEDED"); lead=pow(work[min(work)],-1,3); work=sparse_scale(work,lead); anc=sparse_scale(anc,lead); basis[min(work)]=(work,anc); budget.bump("block_rank_increases" if phase=="block_span" else "occurrence_rank_increases",1,phase); return True,min(work)
def reduce_with_ancestry(basis,row):
    work=dict(row); coeff={}
    for pivot in sorted(basis):
        if pivot not in work: continue
        s=work[pivot]; work=sparse_add(work,sparse_scale(basis[pivot][0],-s))
        for rid,v in basis[pivot][1].items(): coeff[rid]=(coeff.get(rid,0)+s*v)%3
    return work,{k:v for k,v in coeff.items() if v}
def block_image(row,items):
    out={}
    for (ordinal,key),v in row.items():
        k=(items[ordinal]["combined_block"],key); out[k]=(out.get(k,0)+v)%3; out.pop(k,None) if out[k]==0 else None
    return out
def target_vector(abi):
    out={}
    for block,terms in abi["bar_epsilon_1"].items():
        for k,v in parse_sparse(terms,10 if block=="P" else 4,"TARGET").items(): out[(block,k)]=v
    return out
def kappa_from_lambda(lam,budget=None):
    out={}; z0=(0,0,3)
    for actor,v in lam.items():
        shifted=actor_mul(actor,z0); out[shifted]=(out.get(shifted,0)+v)%3; out[actor]=(out.get(actor,0)-v)%3
        if budget: budget.bump("dual_work",1,"quotient_reduction")
    out={k:v for k,v in out.items() if v}; quotient={}
    for (a,b,r),v in out.items(): quotient[(a,b,r%3)]=(quotient.get((a,b,r%3),0)+v)%3
    return out,{k:v for k,v in quotient.items() if v}
def dual_for(target,rows,budget=None):
    coords=sorted(set(target)|{k for row in rows for k in row}); matrix=[[row.get(k,0) for k in coords] for row in rows]; piv=[]; pr=0
    for col in range(len(coords)):
        found=next((r for r in range(pr,len(matrix)) if matrix[r][col]),None)
        if found is None: continue
        matrix[pr],matrix[found]=matrix[found],matrix[pr]; s=pow(matrix[pr][col],-1,3); matrix[pr]=[(v*s)%3 for v in matrix[pr]]
        for r in range(len(matrix)):
            if r!=pr and matrix[r][col]:
                f=matrix[r][col]; matrix[r]=[(matrix[r][j]-f*matrix[pr][j])%3 for j in range(len(coords))]
        piv.append(col); pr+=1
    for free in [j for j in range(len(coords)) if j not in piv]:
        cand=[0]*len(coords); cand[free]=1
        for r,col in reversed(list(enumerate(piv))): cand[col]=(-sum(matrix[r][j]*cand[j] for j in range(len(coords))))%3
        pair=sum(cand[j]*target.get(coords[j],0) for j in range(len(coords)))%3
        if budget: budget.bump("dual_work",1,"dual_search")
        if pair:
            s=pow(pair,-1,3); return {coords[j]:(cand[j]*s)%3 for j in range(len(coords)) if cand[j]*s%3}
    return {}
def validate_abi(abi):
    require(type(abi) is dict and abi.get("schema")=="d972-r07-v216-specialization-abi/v1" and abi.get("modulus")==9,"ABI_SCHEMA_MODULUS"); require(abi.get("ten_to_eleven")==[0,1,2,3,0,4,5,6,7,8,9],"ABI_INSERTION")
    items=abi.get("occurrences"); require(type(items) is list and len(items)==11,"ABI_OCCURRENCES"); require(type(abi.get("bar_epsilon_1")) is dict and set(abi["bar_epsilon_1"])=={"H1","H2","P"},"ABI_TARGET"); require(type(abi["u0"]) is list and len(abi["u0"])==11,"ABI_U0_ROWS")
    for block,width in (("H1",4),("H2",4),("P",10)):
        raw=abi["bar_epsilon_1"][block]; parsed=parse_sparse(raw,width,"TARGET_"+block); require(raw==encode_sparse(parsed),"TARGET_"+block+"_CANONICAL")
    for i,item in enumerate(items):
        require(item.get("ordinal")==i+1 and item.get("combined_block")==("H1" if i<3 else "H2" if i<6 else "P"),"ABI_ORDINAL_BLOCK"); width=occurrence_width(item); require(type(item.get("p_o")) is list and len(item["p_o"])==width and type(item.get("q_o(x)")) is list and len(item["q_o(x)"])==width and type(item.get("q_o(y)")) is list and len(item["q_o(y)"])==width,"ABI_MAPS"); require(item.get("factor_sign") in (-1,1),"ABI_SIGN"); parse_sparse(item.get("xi_o"),width,"XI"); parse_sparse(item.get("w_o"),width,"W"); parse_sparse(item.get("translated"),width,"TRANSLATED"); parse_sparse(item.get("u0"),width,"OCCURRENCE_U0"); require(type(item.get("ancestry")) is dict and set(item["ancestry"])==set(ACTUAL_ANCESTRY) and item["ancestry"]==ACTUAL_ANCESTRY and all(field in item for field in ("rword_g","rword_f","fox_prefix_occurrences","orientation")) and item.get("orientation") in ("direct","inverse"),"ABI_OCCURRENCE_TAGS")
    for i,row in enumerate(abi["u0"]):
        require(type(row) is dict and set(row)=={"ordinal","terms","translated_terms","source_coefficient_terms"} and row["ordinal"]==i+1,"ABI_U0_ROW"); width=4 if i<6 else 10; parse_sparse(row["terms"],width,"U0_TERMS"); parse_sparse(row["translated_terms"],width,"U0_TRANSLATED"); require(type(row["source_coefficient_terms"]) is list and len(row["source_coefficient_terms"])==2,"U0_PROVENANCE_ROWS"); translated_record,original_record=row["source_coefficient_terms"]; require(type(translated_record) is dict and set(translated_record)=={"source","coefficient","terms"} and translated_record["source"]=="translated" and translated_record["coefficient"]==1,"U0_TRANSLATED_PROVENANCE"); require(type(original_record) is dict and set(original_record)=={"source","coefficient","terms","ancestry"} and original_record["source"]=="original" and original_record["coefficient"]==-1 and type(original_record["ancestry"]) is dict and set(original_record["ancestry"])==set(ACTUAL_ANCESTRY) and original_record["ancestry"]==ACTUAL_ANCESTRY,"U0_ORIGINAL_PROVENANCE")
    return items
def recompute_package(abi,budget):
    items=validate_abi(abi); w={}; seed={}; expected=[]
    for i,item in enumerate(items):
        width=occurrence_width(item); p=tuple(item["p_o"]); xi=parse_sparse(item["xi_o"],width,"XI"); source=parse_sparse(item["w_o"],width,"W"); moved={}
        for key,v in xi.items(): nk=qmul(p,key,width,budget,"w_recompute"); moved[nk]=(moved.get(nk,0)+v*(item["factor_sign"]%3))%3
        moved={k:v for k,v in moved.items() if v}; require(moved==source,"ABI_W_RECOMPUTE"); z=qpow(qmul(qmul(qmul(qinv(tuple(item["q_o(x)"]),width,budget),qinv(tuple(item["q_o(y)"]),width,budget),width,budget),tuple(item["q_o(x)"]),width,budget),tuple(item["q_o(y)"]),width,budget),3,width,budget); conjugate=qmul(qmul(p,z,width,budget),qinv(p,width,budget),width,budget); translated={}
        for key,v in source.items(): nk=qmul(conjugate,key,width,budget,"z0_action"); translated[nk]=(translated.get(nk,0)+v)%3
        translated={k:v for k,v in translated.items() if v}; row=sparse_add(translated,sparse_scale(source,-1)); seed.update({(i,k):v for k,v in row.items()}); ancestry=item.get("ancestry"); require(type(ancestry) is dict and set(ancestry)==set(ACTUAL_ANCESTRY) and ancestry==ACTUAL_ANCESTRY,"ABI_OCCURRENCE_ANCESTRY"); provenance=[{"source":"translated","coefficient":1,"terms":encode_sparse(translated)},{"source":"original","coefficient":-1,"terms":encode_sparse(source),"ancestry":ancestry}]; require(parse_sparse(item["translated"],width,"TRANSLATED")==translated and parse_sparse(item["u0"],width,"OCCURRENCE_U0")==row,"ABI_OCCURRENCE_U0_RECOMPUTE"); expected_row={"ordinal":i+1,"terms":encode_sparse(source),"translated_terms":encode_sparse(translated),"source_coefficient_terms":provenance}; require(all(abi["u0"][i].get(field)==expected_row[field] for field in ("ordinal","terms","translated_terms","source_coefficient_terms")),"ABI_OCCURRENCE_U0_ROW"); expected.append(expected_row)
    require(all(all(abi["u0"][i][field]==expected[i][field] for field in ("ordinal","terms","translated_terms","source_coefficient_terms")) for i in range(11)),"ABI_U0_RECOMPUTE"); seed={k:v for k,v in seed.items() if v}; w={(i,k):v for i,item in enumerate(items) for k,v in parse_sparse(item["w_o"],occurrence_width(item),"W").items()}; return items,w,seed
def actor_roster(budget):
    states=[(a,b,r) for a in range(9) for b in range(9) for r in range(9)]; x=(1,0,0); y=(0,1,0); h=actor_mul(actor_mul(actor_mul(actor_inv(x),actor_inv(y)),x),y); z=actor_mul(actor_mul(h,h),h); require(len(states)==729 and h==(0,0,1) and z==(0,0,3),"ACTOR_ROSTER"); one=(0,0,0)
    for g in states: budget.bump("checker_roster",1,"actor_roster"); require(actor_mul(g,actor_inv(g))==one and actor_mul(actor_inv(g),g)==one,"ACTOR_INVERSE")
    require(all(actor_mul(z,g)==actor_mul(g,z) for g in states),"ACTOR_Z0_CENTRAL")
def q_axioms(budget):
    for width in (4,10):
        d,_=dims(width); one=(0,)*width; basis=[]
        for i in range(d):
            value=[0]*width; value[i]=1; basis.append(tuple(value))
        for value in basis:
            require(qmul(value,qinv(value,width,budget),width,budget)==one and qmul(qinv(value,width,budget),value,width,budget)==one,"Q_INVERSE")
            power=one
            for _ in range(9): power=qmul(power,value,width,budget)
            require(power==one,"Q_NINTH_POWER")
        require(qmul(qmul(basis[0],basis[1],width,budget),basis[2],width,budget)==qmul(basis[0],qmul(basis[1],basis[2],width,budget),width,budget),"Q_ASSOCIATIVITY")
def ideal_rows(seed,items,budget=None):
    rows=[]; z=(0,0,3)
    for a in range(9):
        for b in range(9):
            for r in range(3):
                t=(a,b,r); rows.append(action_group_ring({actor_mul(t,z):1,t:2},seed,items,budget)); rows.append(action_group_ring({actor_mul(actor_mul(t,z),z):1,actor_mul(t,z):1,t:1},seed,items,budget))
    require(len(rows)==486,"486_ROSTER"); return rows
def independent_orbit(seed,items,budget):
    basis={}; queue=deque([(seed,{(0,0,0):1})])
    while queue:
        row,anc=queue.popleft(); added,pivot=add_echelon(basis,row,anc,486,budget,"independent_orbit")
        if not added: continue
        kept=basis[pivot][0]
        for actor in ((8,0,0),(0,8,0),(0,1,0),(1,0,0)):
            moved=actor_translate(kept,actor,items,budget)
            if moved: queue.append((moved,{actor_mul(actor,a):v for a,v in basis[pivot][1].items()}))
    require(len(basis)<=486,"CASE_QUEUE_INVARIANCE"); return [basis[p][0] for p in sorted(basis)]
def rebuild_block_echelon(block,budget):
    basis={}
    for i,row in enumerate(block): add_echelon(basis,row,{i:1},486,budget,"block_span")
    return basis
def closure(abi,budget,structural=None):
    items,w,seed=recompute_package(abi,budget)
    if structural is None: actor_roster(budget); q_axioms(budget)
    require(structural is None or structural is True,"STRUCTURAL_CHECKS")
    basis={}; queue=deque()
    if seed: queue.append((seed,{(0,0,0):1}))
    for row,anc in list(queue): pass
    while queue:
        row,anc=queue.popleft(); added,pivot=add_echelon(basis,row,anc,486,budget,"occurrence_closure")
        if not added: continue
        kept=basis[pivot][0]
        for g in ((1,0,0),(8,0,0),(0,1,0),(0,8,0)):
            moved=actor_translate(kept,g,items,budget)
            if moved: queue.append((moved,{actor_mul(g,a):v for a,v in basis[pivot][1].items()}))
    rows=[basis[p][0] for p in sorted(basis)]; ancestry=[basis[p][1] for p in sorted(basis)]; blocks=[block_image(r,items) for r in rows]; budget.bump("block_rows",len(blocks),"block_span"); target=target_vector(abi); eb={}
    for i,row in enumerate(blocks): add_echelon(eb,row,{i:1},100000,budget,"block_span")
    remainder,ci=reduce_with_ancestry(eb,target); member=not remainder; lam={}
    for rid,c in ci.items():
        for a,v in ancestry[rid].items(): lam[a]=(lam.get(a,0)+c*v)%3
    lam={a:v for a,v in lam.items() if v}; kappa,quotient=kappa_from_lambda(lam,budget); sumrows={}
    for rid,c in ci.items(): sumrows=sparse_add(sumrows,sparse_scale(rows[rid],c))
    replay={"sum_c_i_rows":sumrows,"lambda_u0":action_group_ring(lam,seed,items,budget),"kappa_w":action_group_ring(kappa,w,items,budget)}; replay["C_kappa_w"]=block_image(replay["kappa_w"],items)
    if member: require(not quotient and replay["sum_c_i_rows"]==replay["lambda_u0"] and replay["lambda_u0"]==replay["kappa_w"] and replay["C_kappa_w"]==target,"MEMBER_REPLAY")
    else:
        dual=dual_for(target,blocks,budget); require(dual,"DUAL_CONSTRUCTION"); require(all(sum(dual.get(k,0)*v for k,v in row.items())%3==0 for row in blocks),"DUAL_ANNIHILATION"); require(sum(dual.get(k,0)*v for k,v in target.items())%3==1,"DUAL_TARGET_PAIRING")
    return {"items":items,"w":w,"u0":seed,"occurrence_basis":rows,"occurrence_ancestry":ancestry,"block_basis":blocks,"block_echelon":eb,"block_remainder":remainder,"target":target,"member":member,"dual":{} if member else dual,"rank":len(rows),"block_rank":len(eb),"queue_exhausted":True,"actor_translate_count":729,"ideal_486":ideal_rows(w,items,budget),"translate_729":[action_group_ring({(a,b,r):1},seed,items,budget) for a in range(9) for b in range(9) for r in range(9)],"c_i":ci,"lambda":lam,"kappa":kappa,"replay_rows":replay,"quotient_remainder":quotient}
def encode_actors(v): return [[list(a),c] for a,c in sorted(v.items())]
def encode_row_coefficients(v): return [[i,c] for i,c in sorted(v.items())]
def encode_block(v): return [[b,list(k),c] for (b,k),c in sorted(v.items())]
def encode_gate(run):
    out=dict(run); out["action_order_probe"]=encode_vector(actor_translate(run["u0"],(1,0,0),run["items"])); out["w"]=encode_vector(run["w"]); out["u0"]=encode_vector(run["u0"]); out["occurrence_basis"]=[encode_vector(x) for x in run["occurrence_basis"]]; out["occurrence_ancestry"]=[encode_actors(x) for x in run["occurrence_ancestry"]]; out["block_basis"]=[encode_block(x) for x in run["block_basis"]]; out["block_echelon"]=[[list(p),encode_block(row),encode_row_coefficients(anc)] for p,(row,anc) in sorted(run["block_echelon"].items())]; out["block_remainder"]=encode_block(run["block_remainder"]); out["target"]=encode_block(run["target"]); out["dual_orbit_pairings"]=[sum(run["dual"].get(k,0)*v for k,v in block_image(x,run["items"]).items())%3 for x in run["occurrence_basis"]]; out["dual_486_pairings"]=[sum(run["dual"].get(k,0)*v for k,v in block_image(x,run["items"]).items())%3 for x in run["ideal_486"]]; out["dual_729_pairings"]=[sum(run["dual"].get(k,0)*v for k,v in block_image(x,run["items"]).items())%3 for x in run["translate_729"]]; out["dual_target_pairing"]=sum(run["dual"].get(k,0)*v for k,v in run["target"].items())%3; out["dual"]=encode_block(run["dual"]); out["c_i"]=[[i,v] for i,v in sorted(run["c_i"].items())]; out["lambda"]=encode_actors(run["lambda"]); out["kappa"]=encode_actors(run["kappa"]); out["quotient_remainder"]=encode_actors(run["quotient_remainder"]); out["ideal_486"]=[encode_vector(x) for x in run["ideal_486"]]; out["translate_729"]=[encode_vector(x) for x in run["translate_729"]]; out["replay_rows"]={k:encode_vector(v) if k!="C_kappa_w" else encode_block(v) for k,v in run["replay_rows"].items()}; out["replay_digests"]={k:digest_obj(encode_vector(v) if k!="C_kappa_w" else encode_block(v)) for k,v in run["replay_rows"].items()}; return out
def resource_canary(phase):
    value={"schema":SCHEMA+"/resource-canary/v1","terminal":UNKNOWN_RESOURCE,"phase":phase,"cap":"serialized_bytes","value":0,"limit":CAPS["serialized_bytes"]}; value["self_digest_sha256"]=digest_obj(value); return value
def validate_resource(value,phase):
    require(type(value) is dict and set(value)=={"schema","terminal","phase","cap","value","limit","self_digest_sha256"},"CASE_RESOURCE"); body=dict(value); claimed=body.pop("self_digest_sha256"); require(value.get("schema")==SCHEMA+"/resource-canary/v1" and value.get("terminal")==UNKNOWN_RESOURCE and value.get("phase")==phase and value.get("cap")=="serialized_bytes" and value.get("value")==0 and value.get("limit")==CAPS["serialized_bytes"] and type(claimed) is str and claimed==digest_obj(body),"CASE_RESOURCE")
def encode_case(abi,run):
    case=encode_gate(run); case["specialization_v216_abi"]=abi; case["terminal"]=MEMBER if run["member"] else NONMEMBER; case["resource"]=resource_canary("selftest"); case.update({"boundary_membership":False,"pointed_mu1":False,"exact_pb_endpoint_zero":False,"cofinal_lift":False,"fake":False,"Ihara_witness":False}); return case
def certificate(terminal,result=None,reason=None):
    schema=SELFTEST_SCHEMA if terminal==SELFTEST else SCHEMA; out={"schema":schema,"status":terminal,"terminal":terminal,"reason":reason,"result":result,"boundary_membership":False,"pointed_mu1":False,"exact_pb_endpoint_zero":False,"cofinal_lift":False,"fake":False,"Ihara_witness":False}; out["self_digest_sha256"]=digest_obj(out); return out
def seal(v): claimed=v.get("self_digest_sha256"); body=dict(v); body.pop("self_digest_sha256",None); require(type(claimed) is str and claimed==digest_obj(body),"SEAL")
def guarded_json(path_text,expected,budget):
    path=Path(path_text); require(not path.is_absolute() and path.as_posix()==expected and expected.startswith("ci/in/"),"INPUT_PATH"); raw=(ROOT/path).read_bytes(); budget.bump("input_bytes",len(raw),"input"); value=json.loads(raw); require(raw==canonical(value),"NONCANONICAL_INPUT"); return value
def authenticate_task226(receipt,verdict,binding,budget):
    require(receipt.get("schema")==TASK226_SCHEMA and receipt.get("terminal")==TASK226_COMPLETE,"TASK226_TERMINAL"); seal(receipt); require(verdict.get("accepted") is True and verdict.get("independent") is True,"TASK226_VERDICT_ACCEPTANCE"); require(verdict.get("receipt_path")==TASK226 and verdict.get("receipt_bytes")==len(canonical(receipt)) and verdict.get("receipt_sha256")==digest_obj(receipt) and type(verdict.get("abi_sha256")) is str and type(verdict.get("checker_reconstruction_sha256")) is str,"TASK226_VERDICT_BINDING"); require(binding.get("schema")=="d972-r07-task226-production-binding/v1" and binding.get("receipt_path")==TASK226 and binding.get("verdict_path")==TASK226_VERDICT and binding.get("terminal")==TASK226_COMPLETE and binding.get("checker_acceptance") is True,"TASK226_BINDING")
    for key in ("run","head","artifact_id","zip_sha256"): require(type(binding.get(key)) is str and binding[key],"TASK226_"+key)
    require(binding.get("receipt_bytes")==verdict["receipt_bytes"] and binding.get("receipt_sha256")==verdict["receipt_sha256"] and binding.get("verdict_bytes")==len(canonical(verdict)) and binding.get("verdict_sha256")==digest_obj(verdict) and binding.get("abi_sha256")==verdict["abi_sha256"] and binding.get("checker_reconstruction_sha256")==verdict["checker_reconstruction_sha256"],"TASK226_DIGESTS"); abi=receipt.get("result",{}).get("specialization_v216_abi"); require(type(abi) is dict and verdict["abi_sha256"]==digest_obj(abi),"TASK226_ABI"); validate_abi(abi); return abi
def toy_abi(zero=False):
    rows=[]
    for i in range(11):
        width=4 if i<6 else 10; x=[0]*width; y=[0]*width; x[0]=1; y[1]=1; p=[0]*width; p[-1]=(i+1)%9; xi=[] if zero else [[[1]+[0]*(width-1),1]]; w=[]
        for key,v in xi: w.append([[(p[j]+key[j])%9 for j in range(width)],v])
        rows.append({"ordinal":i+1,"combined_block":"H1" if i<3 else "H2" if i<6 else "P","q_degree":3 if width==4 else 4,"key_width":width,"factor_sign":1,"p_o":p,"xi_o":xi,"w_o":w,"q_o(x)":x,"q_o(y)":y,"rword_g":[],"rword_f":[],"fox_prefix_occurrences":[],"orientation":"direct","ancestry":dict(ACTUAL_ANCESTRY),"translated":[],"u0":[]})
    return {"schema":"d972-r07-v216-specialization-abi/v1","modulus":9,"occurrences":rows,"ten_to_eleven":[0,1,2,3,0,4,5,6,7,8,9],"bar_epsilon_1":{"H1":[],"H2":[],"P":[]},"u0":[{"ordinal":i,"terms":[],"translated_terms":[],"source_coefficient_terms":[]} for i in range(1,12)]}
def fill_exact_u0(abi,budget):
    rows=[]
    for item in abi["occurrences"]:
        width=occurrence_width(item); source=parse_sparse(item["w_o"],width,"W"); x=tuple(item["q_o(x)"]); y=tuple(item["q_o(y)"]); p=tuple(item["p_o"]); h=qmul(qmul(qmul(qinv(x,width,budget),qinv(y,width,budget),width,budget),x,width,budget),y,width,budget); z=qpow(h,3,width,budget); conjugate=qmul(qmul(p,z,width,budget),qinv(p,width,budget),width,budget); translated={}
        for key,v in source.items(): nk=qmul(conjugate,key,width,budget); translated[nk]=(translated.get(nk,0)+v)%3
        translated={k:v for k,v in translated.items() if v}; row={"ordinal":item["ordinal"],"terms":encode_sparse(source),"translated_terms":encode_sparse(translated),"source_coefficient_terms":[{"source":"translated","coefficient":1,"terms":encode_sparse(translated)},{"source":"original","coefficient":-1,"terms":encode_sparse(source),"ancestry":dict(ACTUAL_ANCESTRY)}]}; item["translated"]=encode_sparse(translated); item["u0"]=encode_sparse(sparse_add(translated,sparse_scale(source,-1))); rows.append(row)
    abi["u0"]=rows
def set_target_from_rows(abi,rows):
    target={"H1":{},"H2":{},"P":{}}
    for row in rows[:2]:
        for (block,key),v in row.items(): target[block][key]=(target[block].get(key,0)+v)%3
    abi["bar_epsilon_1"]={block:encode_sparse({k:v for k,v in value.items() if v}) for block,value in target.items()}
def decode_vector(value):
    require(type(value) is list,"CASE_VECTOR_ENCODING"); out={}
    for term in value:
        require(type(term) is list and len(term)==3,"CASE_VECTOR_ENCODING"); coords,ordinal,coefficient=term
        require(type(coords) is list and type(ordinal) is int and type(coefficient) is int and coefficient in (1,2),"CASE_VECTOR_ENCODING"); out[(ordinal,tuple(coords))]=(out.get((ordinal,tuple(coords)),0)+coefficient)%3
    out={k:v for k,v in out.items() if v}; require(value==encode_vector(out),"CASE_VECTOR_CANONICAL"); return out
def decode_block(value):
    require(type(value) is list,"CASE_BLOCK_ENCODING"); out={}
    for term in value:
        require(type(term) is list and len(term)==3,"CASE_BLOCK_ENCODING"); block,coords,coefficient=term
        require(type(block) is str and type(coords) is list and type(coefficient) is int and coefficient in (1,2),"CASE_BLOCK_ENCODING"); out[(block,tuple(coords))]=(out.get((block,tuple(coords)),0)+coefficient)%3
    out={k:v for k,v in out.items() if v}; require(value==encode_block(out),"CASE_BLOCK_CANONICAL"); return out
def decode_actors(value):
    require(type(value) is list,"CASE_ACTOR_ENCODING"); out={}
    for term in value:
        require(type(term) is list and len(term)==2,"CASE_ACTOR_ENCODING"); actor,coefficient=term
        require(type(actor) is list and len(actor)==3 and all(type(x) is int and 0<=x<9 for x in actor) and type(coefficient) is int and coefficient in (1,2),"CASE_ACTOR_ENCODING"); out[tuple(actor)]=(out.get(tuple(actor),0)+coefficient)%3
    out={k:v for k,v in out.items() if v}; require(value==encode_actors(out),"CASE_ACTOR_CANONICAL"); return out
def decode_coefficients(value):
    require(type(value) is list,"CASE_CI_ENCODING"); out={}
    for term in value:
        require(type(term) is list and len(term)==2 and type(term[0]) is int and type(term[1]) is int and term[1] in (1,2),"CASE_CI_ENCODING"); out[term[0]]=(out.get(term[0],0)+term[1])%3
    out={k:v for k,v in out.items() if v}; require(value==[[k,v] for k,v in sorted(out.items())],"CASE_CI_CANONICAL"); return out
def validate_encoded_case(case,terminal,budget):
    abi=case.get("specialization_v216_abi"); items,w,u0=recompute_package(abi,budget); require(case.get("w")==encode_vector(w),"CASE_W_ABI"); require(case.get("u0")==encode_vector(u0),"CASE_U0_ABI"); target=target_vector(abi); require(case.get("target")==encode_block(target),"CASE_TARGET_BINDING")
    require(case.get("terminal")==terminal,"CASE_TERMINAL"); validate_resource(case.get("resource"),"selftest"); require(all(case.get(flag) is False for flag in ("boundary_membership","pointed_mu1","exact_pb_endpoint_zero","cofinal_lift","fake","Ihara_witness")),"CASE_FORBIDDEN")
    occ=[decode_vector(x) for x in case.get("occurrence_basis",[])]; anc=[decode_actors(x) for x in case.get("occurrence_ancestry",[])]; block=[decode_block(x) for x in case.get("block_basis",[])]; require(case.get("rank")==len(occ) and len(occ)<=486 and all(0<=ordinal<len(items) and all(len(key)==occurrence_width(items[ordinal]) for ordinal,key in row) for row in occ),"CASE_OCCURRENCE_BASIS"); require(len(anc)==len(occ) and all(occ[i]==action_group_ring(anc[i],u0,items,budget) for i in range(len(occ))),"CASE_OCCURRENCE_ANCESTRY"); require(len(block)==len(occ) and all(block[i]==block_image(occ[i],items) for i in range(len(occ))),"CASE_BLOCK_BASIS"); echelon=case.get("block_echelon",[]); rebuilt_echelon=rebuild_block_echelon(block,budget); expected_echelon=[[list(p),encode_block(row),encode_row_coefficients(anc)] for p,(row,anc) in sorted(rebuilt_echelon.items())]; require(case.get("block_rank")==len(rebuilt_echelon) and echelon==expected_echelon,"CASE_BLOCK_BASIS"); require(case.get("queue_exhausted") is True and case.get("actor_translate_count")==729,"CASE_QUEUE_INVARIANCE"); expected_ideal=ideal_rows(w,items,budget); expected_translates=[action_group_ring({(a,b,r):1},u0,items, budget) for a in range(9) for b in range(9) for r in range(9)]; require(len(case.get("ideal_486",[]))==486 and [decode_vector(x) for x in case["ideal_486"]]==expected_ideal,"CASE_ORBIT_486"); require(len(case.get("translate_729",[]))==729 and [decode_vector(x) for x in case["translate_729"]]==expected_translates,"CASE_ORBIT_729"); require(case.get("action_order_probe")==encode_vector(actor_translate(u0,(1,0,0),items)),"CASE_ACTION_ORDER")
    # Rebuild the two spans in both directions, then solve the printed block map.
    require(len(occ)==len(case.get("occurrence_ancestry",[])),"CASE_OCCURRENCE_ANCESTRY"); require(len(expected_ideal)==486,"CASE_ORBIT_486")
    def span_equal(left,right):
        def basis(rows):
            out={}
            for row in rows:
                work=dict(row)
                for pivot in sorted(out):
                    if pivot in work: work=sparse_add(work,sparse_scale(out[pivot][0],-work[pivot]))
                if work:
                    pivot=min(work); out[pivot]=(sparse_scale(work,pow(work[pivot],-1,3)),{})
            return {p:v[0] for p,v in out.items()}
        def reduces(row,basis_rows):
            work=dict(row)
            for pivot in sorted(basis_rows):
                if pivot in work: work=sparse_add(work,sparse_scale(basis_rows[pivot],-work[pivot]))
            return work
        lb,rb=basis(left),basis(right); require(len(lb)==len(rb),"CASE_SPAN_RANK"); require(all(not reduces(row,rb) for row in left) and all(not reduces(row,lb) for row in right),"CASE_SPAN_EQUAL")
    rebuilt=independent_orbit(u0,items,budget); span_equal(rebuilt,occ); span_equal(occ,rebuilt); span_equal(expected_ideal,occ); span_equal(occ,expected_ideal); span_equal(expected_ideal,expected_translates); span_equal(expected_translates,expected_ideal); span_equal(occ,expected_translates); span_equal(expected_translates,occ)
    ci=decode_coefficients(case.get("c_i",[])); require(all(0<=i<len(block) and v in (1,2) for i,v in ci.items()),"CASE_BLOCK_BASIS"); combined={}
    for i,v in ci.items(): combined=sparse_add(combined,sparse_scale(occ[i],v))
    block_combined={}
    for i,v in ci.items(): block_combined=sparse_add(block_combined,sparse_scale(block[i],v))
    block_remainder=decode_block(case.get("block_remainder",[])); require(sparse_add(block_combined,block_remainder)==target,"CASE_BLOCK_REMAINDER"); require((terminal==MEMBER) is (not block_remainder),"CASE_BLOCK_REMAINDER")
    reconstructed={}
    for i,v in ci.items():
        for actor,c in anc[i].items(): reconstructed[actor]=(reconstructed.get(actor,0)+v*c)%3
    reconstructed={a:v for a,v in reconstructed.items() if v}; lam=decode_actors(case.get("lambda",[])); require(reconstructed==lam,"CASE_MEMBER_LAMBDA"); expected_k={}
    for actor,v in lam.items(): expected_k[actor_mul(actor,(0,0,3))]=(expected_k.get(actor_mul(actor,(0,0,3)),0)+v)%3; expected_k[actor]=(expected_k.get(actor,0)-v)%3
    expected_k={a:v for a,v in expected_k.items() if v}; kap=decode_actors(case.get("kappa",[])); require(expected_k==kap,"CASE_MEMBER_KAPPA")
    replay=case.get("replay_rows",{}); require(set(replay)=={"sum_c_i_rows","lambda_u0","kappa_w","C_kappa_w"},"CASE_MEMBER_LAMBDA"); require(decode_vector(replay["sum_c_i_rows"])==combined,"CASE_MEMBER_LAMBDA"); require(decode_vector(replay["lambda_u0"])==action_group_ring(lam,u0,items,budget),"CASE_MEMBER_LAMBDA"); require(decode_vector(replay["kappa_w"])==action_group_ring(kap,w,items,budget),"CASE_MEMBER_KAPPA"); require(decode_block(replay["C_kappa_w"])==block_image(decode_vector(replay["kappa_w"]),items),"CASE_MEMBER_TARGET")
    quotient=decode_actors(case.get("quotient_remainder",[])); require(type(case.get("replay_digests")) is dict and all(case["replay_digests"].get(k)==digest_obj(replay[k]) for k in replay),"CASE_MEMBER_LAMBDA")
    if terminal==MEMBER:
        require(not quotient,"CASE_QUOTIENT_ZERO"); require(decode_block(replay["C_kappa_w"])==target,"CASE_MEMBER_TARGET")
    else:
        require(block_remainder,"CASE_BLOCK_REMAINDER")
        dual=decode_block(case.get("dual",[])); expected_orbit=[sum(dual.get(k,0)*v for k,v in block_image(x,items).items())%3 for x in occ]; expected_486=[sum(dual.get(k,0)*v for k,v in block_image(x,items).items())%3 for x in expected_ideal]; expected_729=[sum(dual.get(k,0)*v for k,v in block_image(x,items).items())%3 for x in expected_translates]; expected_target=sum(dual.get(k,0)*v for k,v in target.items())%3; require(dual and expected_target==1,"CASE_DUAL_TARGET"); require(case.get("dual_orbit_pairings")==expected_orbit and not any(expected_orbit),"CASE_DUAL_ORBIT"); require(case.get("dual_486_pairings")==expected_486 and not any(expected_486),"CASE_DUAL_486"); require(case.get("dual_729_pairings")==expected_729 and not any(expected_729),"CASE_DUAL_729"); require(case.get("dual_target_pairing")==expected_target==1,"CASE_DUAL_TARGET"); require(all(sum(dual.get(k,0)*v for k,v in row.items())%3==0 for row in block),"CASE_DUAL_BLOCK")
    return True
def selftest(fixture):
    require(fixture.get("schema")==SELFTEST_SCHEMA+"/fixture" and fixture.get("mutation_controls")==MUTATIONS,"FIXTURE"); budget=Budget(); actor_roster(budget); q_axioms(budget); structural=True; abi=toy_abi(); fill_exact_u0(abi,budget); run=closure(abi,budget,structural); require(run["rank"]>=2,"SELFTEST_CASE1_RANK"); member=copy.deepcopy(abi); set_target_from_rows(member,run["block_basis"]); member_run=closure(member,budget,structural); nonmember=copy.deepcopy(member); support=nonmember["bar_epsilon_1"]["H1"] if nonmember["bar_epsilon_1"]["H1"] else nonmember["bar_epsilon_1"]["H2"]; require(len(support)>=2,"SELFTEST_SUPPORT"); support[0][1]=1 if support[0][1]==2 else 2; nonmember_run=closure(nonmember,budget,structural); zero=toy_abi(True); fill_exact_u0(zero,budget); zero_member=closure(zero,budget,structural); zero_non=copy.deepcopy(zero); zero_non["bar_epsilon_1"]["H1"]=[[[0,0,0,0],1]]; zero_non_run=closure(zero_non,budget,structural); require(member_run["member"] and not nonmember_run["member"] and zero_member["member"] and not zero_non_run["member"],"SELFTEST_CASES")
    cases={"case1":encode_case(abi,run),"case2":encode_case(member,member_run),"case3":encode_case(nonmember,nonmember_run),"case4_member":encode_case(zero,zero_member),"case4_nonmember":encode_case(zero_non,zero_non_run)}; controls={"attempted":MUTATIONS,"rejected":mutation_execution(cases,budget)}; result={"schema":SELFTEST_SCHEMA,"specialization_v216_abi":abi,"cases":cases,"mutation_controls":controls,"resource":{"caps":CAPS,"used":budget.used},"actor_translate_count":729,"occurrence_rank_cap":486}; return certificate(SELFTEST,result)
def set_path(value,path,replacement):
    current=value
    for key in path[:-1]: current=current[key]
    current[path[-1]]=replacement
def mutation_execution(cases,budget=None):
    specs={"task226_binding":(("case1","specialization_v216_abi","schema"),"bad-schema"),"translated_provenance_keyset":(("case1","specialization_v216_abi","u0",0,"source_coefficient_terms",0,"source"),"bad-source"),"original_ancestry":(("case1","specialization_v216_abi","u0",0,"source_coefficient_terms",1,"ancestry"),"bad"),"w_abi_binding":(("case1","specialization_v216_abi","occurrences",0,"w_o"),[[[0,0,0,0],2]]),"u0_abi_binding":(("case1","specialization_v216_abi","occurrences",0,"u0"),[[[0,0,0,0],1]]),"target_abi_binding":(("case1","specialization_v216_abi","bar_epsilon_1","H1"),[[[0,0,0,0],1]]),"noncentral_action_order":(("case1","action_order_probe"),[]),"occurrence_basis_row":(("case1","occurrence_basis",0),[[[0,0,0,0],11,1]]),"occurrence_ancestry":(("case1","occurrence_ancestry",0),[]),"queue_invariance":(("case1","queue_exhausted"),False),"orbit_vs_486":(("case1","ideal_486",0),[]),"orbit_vs_729":(("case1","translate_729",0),[]),"premature_block_sum":(("case1","block_basis",0),[]),"member_lambda_u0":(("case2","lambda"),[]),"member_kappa_w":(("case2","kappa"),[]),"member_target":(("case2","replay_rows","C_kappa_w"),[]),"quotient_zero":(("case2","quotient_remainder"),[[[0,0,0],1]]),"dual_orbit_annihilation":(("case3","dual_orbit_pairings"),[1]),"dual_486_annihilation":(("case3","dual_486_pairings",0),1),"dual_729_annihilation":(("case3","dual_729_pairings",0),1),"dual_target_pairing":(("case3","dual_target_pairing"),0),"terminal_vocabulary":(("case1","terminal"),"BAD_TERMINAL"),"resource_terminal":(("case1","resource","cap"),"bad-cap"),"forbidden_conclusion":(("case1","pointed_mu1"),True)}
    observations=[]
    for name in MUTATIONS:
        if budget: budget.bump("mutation_work",1,"mutation_"+name)
        mutant=copy.deepcopy(cases); path,replacement=specs[name]; changed=".".join(str(k) for k in path); key=path[0]; expected_terminal=NONMEMBER if key=="case3" else MEMBER
        try:
            set_path(mutant,path,replacement)
            validate_encoded_case(mutant[key],expected_terminal,budget)
            raise MutationAccepted("mutation accepted")
        except InputStop as exc:
            require(str(exc)==EXPECTED_GATES[name],"MUTATION_GATE_"+name)
            observations.append({"name":name,"changed_field":changed,"expected_gate":EXPECTED_GATES[name],"observed_reason":str(exc),"before_sha256":digest_obj(cases[key]),"after_sha256":digest_obj(mutant[key]),"rejected":True})
    require(len(observations)==len(MUTATIONS) and [x["name"] for x in observations]==MUTATIONS,"MUTATION_REJECTION"); return observations
def main(argv=None):
    parser=argparse.ArgumentParser(); parser.add_argument("--selftest",action="store_true"); parser.add_argument("--fixture",default=FIXTURE); parser.add_argument("--task226",default=TASK226); parser.add_argument("--task226-verdict",default=TASK226_VERDICT); parser.add_argument("--task226-binding",default=TASK226_BINDING); parser.add_argument("--output"); args=parser.parse_args(argv)
    try:
        budget=Budget(); result=selftest(json.loads((ROOT/Path(args.fixture)).read_bytes())) if args.selftest else None
        if not args.selftest:
            abi=authenticate_task226(guarded_json(args.task226,TASK226,budget),guarded_json(args.task226_verdict,TASK226_VERDICT,budget),guarded_json(args.task226_binding,TASK226_BINDING,budget),budget); run=closure(abi,budget); payload=encode_case(abi,run); payload["resource"]=resource_canary("production"); result=certificate(MEMBER if run["member"] else NONMEMBER,payload)
        if args.output:
            encoded=canonical(result); budget.bump("serialized_bytes",len(encoded),"serialize"); output=Path(args.output); require(not output.is_absolute() and output.as_posix().startswith("ci/out/") and not output.exists(),"OUTPUT_PATH"); output.parent.mkdir(parents=True,exist_ok=True); output.write_bytes(encoded)
        print("D227_PRODUCER_TERMINAL "+result["terminal"]); return 0
    except ResourceStop as exc:
        result=certificate(UNKNOWN_RESOURCE,{"phase":exc.phase,"cap":exc.cap,"value":exc.value,"limit":exc.limit});
        if args.output and not Path(args.output).exists(): Path(args.output).parent.mkdir(parents=True,exist_ok=True); Path(args.output).write_bytes(canonical(result))
        print("D227_PRODUCER_TERMINAL "+UNKNOWN_RESOURCE); return 0
    except (InputStop,KeyError,ValueError,json.JSONDecodeError) as exc:
        result=certificate(UNKNOWN_INPUT,reason=str(exc));
        if args.output and not Path(args.output).exists(): Path(args.output).parent.mkdir(parents=True,exist_ok=True); Path(args.output).write_bytes(canonical(result))
        print("D227_PRODUCER_TERMINAL "+UNKNOWN_INPUT); return 0
if __name__=="__main__": raise SystemExit(main())
