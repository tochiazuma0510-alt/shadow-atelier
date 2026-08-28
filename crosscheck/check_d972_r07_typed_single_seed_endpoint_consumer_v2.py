#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json
from collections import deque
from collections import deque
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]; SCHEMA="d972-r07-typed-single-seed-endpoint-consumer/v2"; SELFTEST_SCHEMA=SCHEMA+"/selftest"; SELFTEST="R07_TYPED_SINGLE_SEED_ENDPOINT_CONSUMER_V2_SELFTEST_PASS"; MEMBER="PROJECTED_MEMBER_SEED"; NONMEMBER="PROJECTED_NONMEMBER_DUAL"; UNKNOWN_INPUT="UNKNOWN_INPUT"; UNKNOWN_RESOURCE="UNKNOWN_RESOURCE"
TASK226="ci/in/d972_r07_actual_two_word_endpoint_specializer_v2.json"; TASK226_VERDICT="ci/in/d972_r07_actual_two_word_endpoint_specializer_v2.verdict.json"; TASK226_BINDING="ci/in/d972_r07_actual_two_word_endpoint_specializer_v2.binding.json"; COMPLETE="R07_ACTUAL_TWO_WORD_ENDPOINT_SPECIALIZER_V2_COMPLETE"
MUTATIONS=json.loads('["task226_binding","translated_provenance_keyset","original_ancestry","w_abi_binding","u0_abi_binding","target_abi_binding","noncentral_action_order","occurrence_basis_row","occurrence_ancestry","queue_invariance","orbit_vs_486","orbit_vs_729","premature_block_sum","member_lambda_u0","member_kappa_w","member_target","quotient_zero","dual_orbit_annihilation","dual_486_annihilation","dual_729_annihilation","dual_target_pairing","terminal_vocabulary","resource_terminal","forbidden_conclusion"]')
ACTUAL_ANCESTRY={"source":"task179_A18","substitution":"PB3/PB4_literal","prefix":"task198_one_based_signed"}
EXPECTED_GATES={"task226_binding":"ABI schema","translated_provenance_keyset":"ABI u0 row","original_ancestry":"ABI u0 row","w_abi_binding":"ABI w","u0_abi_binding":"ABI occurrence u0","target_abi_binding":"gate ABI binding","noncentral_action_order":"noncentral action order","occurrence_basis_row":"occurrence basis row","occurrence_ancestry":"occurrence ancestry replay","queue_invariance":"queue invariance","orbit_vs_486":"producer 486 exact","orbit_vs_729":"producer 729 exact","premature_block_sum":"block rows","member_lambda_u0":"lambda reconstruction","member_kappa_w":"kappa reconstruction","member_target":"C replay","quotient_zero":"member chain","dual_orbit_annihilation":"dual orbit","dual_486_annihilation":"dual 486","dual_729_annihilation":"dual 729","dual_target_pairing":"dual target","terminal_vocabulary":"terminal vocabulary","resource_terminal":"resource terminal","forbidden_conclusion":"forbidden conclusion"}
SCOPE_KEYS=["input_bytes","actor_operations","occurrence_support","orbit_actions","occurrence_rank_increases","block_rank_increases","block_rows","checker_roster","dual_work","mutation_work","serialized_bytes","wall_seconds"]
EXPECTED_CAPS={"input_bytes":500000000,"actor_operations":2000000,"occurrence_support":2000000,"orbit_actions":2000000,"occurrence_rank_increases":486,"block_rank_increases":486,"block_rows":100000,"checker_roster":729,"dual_work":1000000,"mutation_work":100000,"serialized_bytes":2000000000,"wall_seconds":21600}
class Stop(RuntimeError): pass
class MutationAccepted(RuntimeError): pass
def require(ok,msg):
    if ok is not True: raise Stop(msg)
def canonical(v): return json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=True).encode("ascii")
def obj_digest(v): return hashlib.sha256(canonical(v)).hexdigest()
def m(v): return v%9
def dims(width): require(width in (4,10),"Q width"); return (3,1) if width==4 else (6,4)
def bracket(width,i,j):
    d,c=dims(width); table={(0,1):(1,),(0,2):(-1,),(1,2):(1,)} if d==3 else {(0,1):(1,0,0,0),(0,3):(-1,0,0,0),(1,3):(1,0,0,0),(0,2):(0,1,0,0),(0,4):(0,-1,0,0),(2,4):(0,1,0,0),(1,2):(0,0,1,0),(1,5):(0,0,-1,0),(2,5):(0,0,1,0),(3,4):(0,0,0,1),(3,5):(0,0,0,-1),(4,5):(0,0,0,1)}; return tuple(table.get((i,j),(0,)*c))
def mul(a,b,width):
    d,c=dims(width); z=[m(a[d+i]+b[d+i]) for i in range(c)]
    for i in range(d):
        for j in range(i+1,d):
            for k,v in enumerate(bracket(width,i,j)): z[k]=m(z[k]-a[j]*b[i]*v)
    return tuple(m(a[i]+b[i]) for i in range(d))+tuple(z)
def inv(a,width):
    d,c=dims(width); z=list(tuple(m(-v) for v in a)); tail=z[d:]
    for i in range(d):
        for j in range(i+1,d):
            for k,v in enumerate(bracket(width,i,j)): tail[k]=m(tail[k]-a[i]*a[j]*v)
    return tuple(z[:d]+tail)
def power(a,n,width):
    out=(0,)*width
    for _ in range(n%9): out=mul(out,a,width)
    return out
def actor_mul(a,b): return (m(a[0]+b[0]),m(a[1]+b[1]),m(a[2]+b[2]-b[0]*a[1]))
def actor_inv(a): return (m(-a[0]),m(-a[1]),m(-a[2]-a[0]*a[1]))
def add(a,b):
    out=dict(a)
    for k,v in b.items(): out[k]=(out.get(k,0)+v)%3; out.pop(k,None) if out[k]==0 else None
    return out
def scale(a,s): return {k:(v*s)%3 for k,v in a.items() if (v*s)%3}
def terms(value,width):
    require(type(value) is list,"terms type"); out={}
    for t in value:
        key,co=(t.get("key"),t.get("coefficient")) if type(t) is dict else (t[0],t[1]); require(type(key) is list and len(key)==width and all(type(x) is int and 0<=x<9 for x in key) and co in (1,2),"term"); k=tuple(key); out[k]=(out.get(k,0)+co)%3
    out={k:v for k,v in out.items() if v}; require(value==[[list(k),v] for k,v in sorted(out.items())],"terms canonical"); return out
def vec_decode(value):
    require(type(value) is list,"vector encoding"); out={}
    for term in value:
        require(type(term) is list and len(term)==3 and type(term[0]) is list and type(term[1]) is int and type(term[2]) is int and term[2] in (1,2),"vector encoding"); k=(term[1],tuple(term[0])); out[k]=(out.get(k,0)+term[2])%3
    out={k:v for k,v in out.items() if v}; require(value==vec_encode(out),"vector canonical"); return out
def block_decode(value):
    require(type(value) is list,"block encoding type"); out={}
    for term in value:
        require(type(term) is list and len(term)==3 and type(term[0]) is str and type(term[1]) is list and type(term[2]) is int and term[2] in (1,2),"block encoding"); k=(term[0],tuple(term[1])); out[k]=(out.get(k,0)+term[2])%3
    out={k:v for k,v in out.items() if v}; require(value==[[b,list(k),v] for (b,k),v in sorted(out.items())],"block canonical"); return out
def actor_decode(value):
    require(type(value) is list,"actor encoding type"); out={}
    for term in value:
        require(type(term) is list and len(term)==2 and type(term[0]) is list and len(term[0])==3 and type(term[1]) is int and term[1] in (1,2),"actor encoding"); k=tuple(term[0]); out[k]=(out.get(k,0)+term[1])%3
    out={k:v for k,v in out.items() if v}; require(value==[[list(k),v] for k,v in sorted(out.items())],"actor canonical"); return out
def coefficient_decode(value):
    require(type(value) is list,"c_i encoding type"); out={}
    for term in value:
        require(type(term) is list and len(term)==2 and type(term[0]) is int and type(term[1]) is int and term[1] in (1,2),"c_i encoding"); out[term[0]]=(out.get(term[0],0)+term[1])%3
    out={k:v for k,v in out.items() if v}; require(value==[[k,v] for k,v in sorted(out.items())],"c_i canonical"); return out
def validate_resource(value,phase):
    require(type(value) is dict and set(value)=={"schema","terminal","phase","cap","value","limit","self_digest_sha256"},"resource terminal"); body=dict(value); claimed=body.pop("self_digest_sha256"); require(value.get("schema")==SCHEMA+"/resource-canary/v1" and value.get("terminal")==UNKNOWN_RESOURCE and value.get("phase")==phase and value.get("cap")=="serialized_bytes" and value.get("value")==0 and value.get("limit")==2000000000 and type(claimed) is str and claimed==obj_digest(body),"resource terminal")
def validate_scope_accounting(accounting):
    require(type(accounting) is dict and set(accounting)=={"roster","scopes","max_used","digest_sha256"},"scope accounting"); expected=["structural"]+["closure:"+name for name in ("case1","case2","case3","case4_member","case4_nonmember")]+["mutation:"+name for name in MUTATIONS]; require(accounting.get("roster")==expected and type(accounting.get("scopes")) is list and len(accounting["scopes"])==len(expected),"scope roster")
    for scope,label in zip(accounting["scopes"],expected):
        require(type(scope) is dict and set(scope)=={"label","used","digest_sha256"} and scope["label"]==label and type(scope["used"]) is dict and set(scope["used"])==set(SCOPE_KEYS) and all(type(value) in (int,float) and value>=0 and value<=EXPECTED_CAPS[key] for key,value in scope["used"].items()),"scope entry"); require(scope["digest_sha256"]==obj_digest({"label":scope["label"],"used":scope["used"]}),"scope digest")
    maximum={key:max(scope["used"][key] for scope in accounting["scopes"]) for key in SCOPE_KEYS}; require(accounting["max_used"]==maximum,"scope maximum"); body=dict(accounting); claimed=body.pop("digest_sha256"); require(type(claimed) is str and claimed==obj_digest(body),"scope seal")
def vec_encode(value): return [[list(k[1]),k[0],v] for k,v in sorted(value.items())]
def action(row,actor,rows):
    out={}
    for (ordinal,key),v in row.items():
        item=rows[ordinal]; width=item["key_width"]; p=tuple(item["p_o"]); x=tuple(item["q_o(x)"]); y=tuple(item["q_o(y)"]); h=mul(mul(mul(inv(x,width),inv(y,width),width),x,width),y,width); actor_value=mul(mul(power(x,actor[0],width),power(y,actor[1],width),width),power(h,actor[2],width),width); conjugated=mul(mul(p,actor_value,width),inv(p,width),width); nk=(ordinal,mul(conjugated,key,width)); out[nk]=(out.get(nk,0)+v)%3
    return {k:v for k,v in out.items() if v}
def ring(coeff,row,rows):
    out={}
    for actor,v in coeff.items(): out=add(out,scale(action(row,actor,rows),v))
    return out
def block_image(row,rows):
    out={}
    for (ordinal,key),v in row.items():
        k=(rows[ordinal]["combined_block"],key); out[k]=(out.get(k,0)+v)%3; out.pop(k,None) if out[k]==0 else None
    return out
def compare_sparse_spans(left,right):
    def basis(rows):
        out={}
        for row in rows:
            work=dict(row)
            for pivot in sorted(out):
                if pivot in work: work=add(work,scale(out[pivot],-work[pivot]))
            if work:
                pivot=min(work); lead=pow(work[pivot],-1,3); out[pivot]=scale(work,lead)
        return out
    def reduces(row,b):
        work=dict(row)
        for pivot in sorted(b):
            if pivot in work: work=add(work,scale(b[pivot],-work[pivot]))
        return work
    lb,rb=basis(left),basis(right); require(len(lb)==len(rb),"span rank"); require(all(not reduces(x,rb) for x in left) and all(not reduces(x,lb) for x in right),"span equality")
def check_q_axioms():
    for width in (4,10):
        d,_=dims(width); one=(0,)*width; basis=[]
        for i in range(d):
            value=[0]*width; value[i]=1; basis.append(tuple(value))
        for value in basis:
            require(mul(value,inv(value,width),width)==one and mul(inv(value,width),value,width)==one,"Q inverse")
            power=one
            for _ in range(9): power=mul(power,value,width)
            require(power==one,"Q ninth power")
        require(mul(mul(basis[0],basis[1],width),basis[2],width)==mul(basis[0],mul(basis[1],basis[2],width),width),"Q associativity")
def action_order_canary():
    p=(1,0,0,0); actor=(0,1,0,0); wrong=mul(mul(actor,p,4),inv(p,4),4); right=mul(mul(p,actor,4),inv(p,4),4); require(right!=wrong,"noncentral action canary")
def check_abi(abi):
    require(type(abi) is dict and abi.get("schema")=="d972-r07-v216-specialization-abi/v1" and abi.get("modulus")==9,"ABI schema"); require(abi.get("ten_to_eleven")==[0,1,2,3,0,4,5,6,7,8,9],"ABI insertion"); rows=abi.get("occurrences"); require(type(rows) is list and len(rows)==11,"ABI occurrences"); require(set(abi.get("bar_epsilon_1",{}))=={"H1","H2","P"},"ABI target"); require(type(abi["u0"]) is list and len(abi["u0"])==11,"ABI u0 exact")
    for block,width in (("H1",4),("H2",4),("P",10)):
        raw=abi["bar_epsilon_1"][block]; parsed=terms(raw,width); require(raw==[[list(k),v] for k,v in sorted(parsed.items())],"ABI target canonical")
    expected=[]
    for i,row in enumerate(rows):
        require(row.get("ordinal")==i+1 and row.get("combined_block")==("H1" if i<3 else "H2" if i<6 else "P"),"ABI row"); width=row.get("key_width"); require(row.get("q_degree")== (3 if width==4 else 4),"ABI degree"); require(type(row.get("q_o(x)")) is list and type(row.get("q_o(y)")) is list and type(row.get("p_o")) is list and type(row.get("u0")) is list and type(row.get("ancestry")) is dict and set(row["ancestry"])==set(ACTUAL_ANCESTRY) and row["ancestry"]==ACTUAL_ANCESTRY and all(field in row for field in ("rword_g","rword_f","fox_prefix_occurrences","orientation")) and row.get("orientation") in ("direct","inverse"),"ABI maps"); xi=terms(row["xi_o"],width); w=terms(row["w_o"],width); moved={}
        for key,v in xi.items(): nk=mul(tuple(row["p_o"]),key,width); moved[nk]=(moved.get(nk,0)+v*row["factor_sign"])%3
        require({k:v for k,v in moved.items() if v}==w,"ABI w")
        x=tuple(row["q_o(x)"]); y=tuple(row["q_o(y)"]); h=mul(mul(mul(inv(x,width),inv(y,width),width),x,width),y,width); z=power(h,3,width); c=mul(mul(tuple(row["p_o"]),z,width),inv(tuple(row["p_o"]),width),width); translated={}
        for key,v in w.items(): nk=mul(c,key,width); translated[nk]=(translated.get(nk,0)+v)%3
        provenance=[{"source":"translated","coefficient":1,"terms":[[list(k),v] for k,v in sorted(translated.items()) if v]},{"source":"original","coefficient":-1,"terms":[[list(k),v] for k,v in sorted(w.items())],"ancestry":row["ancestry"]}]; residual=add({(i,k):v for k,v in translated.items()},{(i,k):-v for k,v in w.items()}); residual={k:v%3 for k,v in residual.items() if v%3}; require(terms(row["translated"],width)==translated and terms(row["u0"],width)=={k[1]:v for k,v in residual.items()},"ABI occurrence u0"); expected.append({"ordinal":i+1,"terms":[[list(k),v] for k,v in sorted(w.items())],"translated_terms":[[list(k),v] for k,v in sorted(translated.items()) if v],"source_coefficient_terms":provenance}); require(row["u0"]==[[list(k),v] for k,v in sorted({k[1]:v for k,v in residual.items()}.items())],"ABI occurrence u0")
    for i,row in enumerate(abi["u0"]): require(type(row) is dict and set(row)=={"ordinal","terms","translated_terms","source_coefficient_terms"} and all(row[field]==expected[i][field] for field in ("ordinal","terms","translated_terms","source_coefficient_terms")),"ABI u0 row")
    check_q_axioms()
    action_order_canary()
    return rows
def independent_ideal(seed,rows):
    out=[]; z=(0,0,3)
    for a in range(9):
        for b in range(9):
            for r in range(3):
                t=(a,b,r); out.append(ring({actor_mul(t,z):1,t:2},seed,rows)); out.append(ring({actor_mul(actor_mul(t,z),z):1,actor_mul(t,z):1,t:1},seed,rows))
    require(len(out)==486,"486 roster"); return out
def abi_vectors(abi,rows):
    w={}; u0={}
    for i,row in enumerate(rows):
        source=terms(row["w_o"],row["key_width"]); residual=terms(row["u0"],row["key_width"])
        for key,value in source.items(): w[(i,key)]=value
        for key,value in residual.items(): u0[(i,key)]=value
    target={}
    for block,raw in abi["bar_epsilon_1"].items():
        width=10 if block=="P" else 4
        for key,value in terms(raw,width).items(): target[(block,key)]=value
    return w,u0,target
def rebuild_orbit(seed,rows):
    basis={}; queue=deque([(seed,{(0,0,0):1})])
    while queue:
        row,ancestry=queue.popleft(); work=dict(row); anc=dict(ancestry)
        for pivot in sorted(basis):
            if pivot in work:
                scalar=work[pivot]; work=add(work,scale(basis[pivot][0],-scalar))
                for actor,value in basis[pivot][1].items(): anc[actor]=(anc.get(actor,0)-scalar*value)%3
                anc={actor:value for actor,value in anc.items() if value}
        if not work: continue
        pivot=min(work); lead=pow(work[pivot],-1,3); work=scale(work,lead); anc=scale(anc,lead); basis[pivot]=(work,anc)
        for actor in ((0,8,0),(0,1,0),(8,0,0),(1,0,0)):
            moved=action(work,actor,rows)
            if moved: queue.append((moved,{actor_mul(actor,a):v for a,v in anc.items()}))
    return [basis[p][0] for p in sorted(basis)]
def rebuild_block_echelon(block):
    basis={}
    for i,row in enumerate(block):
        work=dict(row); ancestry={i:1}
        for pivot in sorted(basis):
            if pivot in work:
                scalar=work[pivot]; work=add(work,scale(basis[pivot][0],-scalar))
                for index,value in basis[pivot][1].items(): ancestry[index]=(ancestry.get(index,0)-scalar*value)%3
                ancestry={index:value for index,value in ancestry.items() if value}
        if work:
            pivot=min(work); lead=pow(work[pivot],-1,3); basis[pivot]=(scale(work,lead),scale(ancestry,lead))
    return basis
def verify_gate(gate,abi,expected_terminal,expected_phase):
    require(gate.get("terminal")==expected_terminal,"terminal vocabulary"); validate_resource(gate.get("resource"),expected_phase); require(all(gate.get(flag) is False for flag in ("boundary_membership","pointed_mu1","exact_pb_endpoint_zero","cofinal_lift","fake","Ihara_witness")),"forbidden conclusion")
    rows=check_abi(abi); w_exact,u0_exact,target_exact=abi_vectors(abi,rows); require(vec_decode(gate["w"])==w_exact and vec_decode(gate["u0"])==u0_exact and block_decode(gate["target"])==target_exact,"gate ABI binding"); occ=[vec_decode(x) for x in gate["occurrence_basis"]]; require(len(occ)==gate["rank"] and len(occ)<=486 and all(0<=ordinal<len(rows) and len(key)==rows[ordinal]["key_width"] for row in occ for ordinal,key in row),"occurrence basis row"); ancestry=[actor_decode(x) for x in gate["occurrence_ancestry"]]; require(len(ancestry)==len(occ),"ancestry rows"); block=[block_decode(x) for x in gate["block_basis"]]; require(len(block)==len(occ) and all(block[i]==block_image(occ[i],rows) for i in range(len(occ))),"block rows"); rebuilt_echelon=rebuild_block_echelon(block); expected_echelon=[[[p[0],list(p[1])],[[b,list(k),v] for (b,k),v in sorted(row.items())],[[i,v] for i,v in sorted(anc.items())]] for p,(row,anc) in sorted(rebuilt_echelon.items())]; require(gate.get("block_rank")==len(rebuilt_echelon) and gate.get("block_echelon")==expected_echelon,"block rows"); target=target_exact; ci=coefficient_decode(gate["c_i"]); lam=actor_decode(gate["lambda"]); kap=actor_decode(gate["kappa"]); require(all(0<=i<len(occ) for i in ci),"c_i rows"); combined={}
    for i,v in ci.items(): combined=add(combined,scale(occ[i],v))
    require(all(occ[i]==ring(ancestry[i],u0_exact,rows) for i in range(len(occ))),"occurrence ancestry replay")
    reconstructed={}
    for i,v in ci.items():
        for actor,c in ancestry[i].items(): reconstructed[actor]=(reconstructed.get(actor,0)+v*c)%3
    reconstructed={a:v for a,v in reconstructed.items() if v}; require(reconstructed==lam,"lambda reconstruction"); expected_k={}
    for actor,v in lam.items(): expected_k[actor_mul(actor,(0,0,3))]=(expected_k.get(actor_mul(actor,(0,0,3)),0)+v)%3; expected_k[actor]=(expected_k.get(actor,0)-v)%3
    expected_k={a:v for a,v in expected_k.items() if v}; require(expected_k==kap,"kappa reconstruction"); replay=gate["replay_rows"]; require(set(replay)=={"sum_c_i_rows","lambda_u0","kappa_w","C_kappa_w"},"replay rows"); require(vec_decode(replay["sum_c_i_rows"])==combined,"c_i replay"); require(vec_decode(replay["lambda_u0"])==ring(lam,vec_decode(gate["u0"]),rows),"lambda replay"); require(vec_decode(replay["kappa_w"])==ring(kap,vec_decode(gate["w"]),rows),"kappa replay"); require(block_decode(replay["C_kappa_w"])==block_image(vec_decode(replay["kappa_w"]),rows),"C replay"); require(gate["member"] is (expected_terminal==MEMBER),"terminal member")
    require(gate.get("action_order_probe")==vec_encode(action(vec_decode(gate["u0"]),(1,0,0),rows)),"noncentral action order")
    require(gate.get("queue_exhausted") is True and gate.get("actor_translate_count")==729,"queue invariance")
    rebuilt=rebuild_orbit(u0_exact,rows); ideal=independent_ideal(vec_decode(gate["w"]),rows); translates=independent_729(vec_decode(gate["u0"]),rows); require(len(gate["ideal_486"])==486 and [vec_decode(x) for x in gate["ideal_486"]]==ideal,"producer 486 exact"); require(len(gate["translate_729"])==729 and [vec_decode(x) for x in gate["translate_729"]]==translates,"producer 729 exact"); compare_sparse_spans(ideal,occ); compare_sparse_spans(occ,ideal); compare_sparse_spans(ideal,translates); compare_sparse_spans(translates,ideal); compare_sparse_spans(occ,translates); compare_sparse_spans(translates,occ); compare_sparse_spans(rebuilt,occ); compare_sparse_spans(occ,rebuilt); compare_sparse_spans([block_image(x,rows) for x in ideal],[block_image(x,rows) for x in translates]); compare_sparse_spans([block_image(x,rows) for x in translates],[block_image(x,rows) for x in ideal]); compare_sparse_spans([block_image(x,rows) for x in ideal],block); compare_sparse_spans(block,[block_image(x,rows) for x in ideal]);
    if expected_terminal==NONMEMBER:
        phi=block_decode(gate["dual"]); require(gate.get("dual_orbit_pairings")==[sum(phi.get(k,0)*v for k,v in block_image(x,rows).items())%3 for x in occ],"dual orbit"); require(gate.get("dual_486_pairings")==[sum(phi.get(k,0)*v for k,v in block_image(x,rows).items())%3 for x in ideal],"dual 486"); require(gate.get("dual_729_pairings")==[sum(phi.get(k,0)*v for k,v in block_image(x,rows).items())%3 for x in translates],"dual 729"); require(gate.get("dual_target_pairing")==sum(phi.get(k,0)*v for k,v in target.items())%3,"dual target")
    block_combined={}
    for i,v in ci.items(): block_combined=add(block_combined,scale(block[i],v))
    block_remainder=block_decode(gate.get("block_remainder",[])); require(add(block_combined,block_remainder)==target,"block remainder"); require((expected_terminal==MEMBER) is (not block_remainder),"block remainder")
    quotient=actor_decode(gate["quotient_remainder"]); require(type(gate.get("replay_digests")) is dict and all(type(v) is str for v in gate["replay_digests"].values()),"replay digests")
    for key in replay:
        encoded= replay[key] if key=="C_kappa_w" else replay[key]
        require(gate["replay_digests"].get(key)==obj_digest(encoded),"replay digest")
    if expected_terminal==MEMBER:
        require(not quotient and not block_remainder and block_decode(replay["C_kappa_w"])==target,"member chain")
    else:
        require(bool(block_remainder),"block remainder")
    if expected_terminal==NONMEMBER:
        phi=block_decode(gate["dual"]); require(phi and sum(phi.get(k,0)*v for k,v in target.items())%3==1,"dual target"); require(all(sum(phi.get(k,0)*v for k,v in row.items())%3==0 for row in block),"dual block"); require(all(sum(phi.get(k,0)*v for k,v in block_image(x,rows).items())%3==0 for x in ideal),"dual 486"); require(all(sum(phi.get(k,0)*v for k,v in block_image(x,rows).items())%3==0 for x in translates),"dual 729")
    return True
def independent_729(seed,rows):
    return [ring({(a,b,r):1},seed,rows) for a in range(9) for b in range(9) for r in range(9)]
def load_json(path,expected):
    p=Path(path); require(not p.is_absolute() and p.as_posix()==expected,"path"); raw=(ROOT/p).read_bytes(); value=json.loads(raw); require(raw==canonical(value),"canonical input"); return value
def authenticate(receipt,verdict,binding):
    require(receipt.get("schema")=="d972-r07-actual-two-word-endpoint-specializer/v2" and receipt.get("terminal")==COMPLETE,"task226 terminal"); claimed=receipt.get("self_digest_sha256"); body=dict(receipt); body.pop("self_digest_sha256",None); require(type(claimed) is str and claimed==obj_digest(body),"task226 receipt seal"); abi=receipt.get("result",{}).get("specialization_v216_abi"); require(type(abi) is dict,"task226 ABI"); require(verdict.get("accepted") is True and verdict.get("independent") is True and verdict.get("receipt_path")==TASK226 and verdict.get("receipt_bytes")==len(canonical(receipt)) and verdict.get("receipt_sha256")==obj_digest(receipt) and verdict.get("abi_sha256")==obj_digest(abi) and type(verdict.get("checker_reconstruction_sha256")) is str,"task226 verdict"); require(binding.get("schema")=="d972-r07-task226-production-binding/v1" and binding.get("receipt_path")==TASK226 and binding.get("verdict_path")==TASK226_VERDICT and binding.get("terminal")==COMPLETE and binding.get("checker_acceptance") is True,"task226 binding"); require(binding.get("receipt_bytes")==verdict["receipt_bytes"] and binding.get("receipt_sha256")==verdict["receipt_sha256"] and binding.get("verdict_bytes")==len(canonical(verdict)) and binding.get("verdict_sha256")==obj_digest(verdict) and binding.get("abi_sha256")==verdict["abi_sha256"] and binding.get("checker_reconstruction_sha256")==verdict["checker_reconstruction_sha256"],"task226 digests");
    for key in ("run","head","artifact_id","zip_sha256"): require(bool(type(binding.get(key)) is str and binding[key]),"task226 binding "+key)
    check_abi(abi); return abi
def set_path(value,path,replacement):
    current=value
    for key in path[:-1]: current=current[key]
    current[path[-1]]=replacement
def independent_mutations(cases):
    specs={"task226_binding":(("case1","specialization_v216_abi","schema"),"bad-schema"),"translated_provenance_keyset":(("case1","specialization_v216_abi","u0",0,"source_coefficient_terms",0,"source"),"bad-source"),"original_ancestry":(("case1","specialization_v216_abi","u0",0,"source_coefficient_terms",1,"ancestry"),"bad"),"w_abi_binding":(("case1","specialization_v216_abi","occurrences",0,"w_o"),[[[0,0,0,0],2]]),"u0_abi_binding":(("case1","specialization_v216_abi","occurrences",0,"u0"),[[[0,0,0,0],1]]),"target_abi_binding":(("case1","specialization_v216_abi","bar_epsilon_1","H1"),[[[0,0,0,0],1]]),"noncentral_action_order":(("case1","action_order_probe"),[]),"occurrence_basis_row":(("case1","occurrence_basis",0),[[[0,0,0,0],11,1]]),"occurrence_ancestry":(("case1","occurrence_ancestry",0),[]),"queue_invariance":(("case1","queue_exhausted"),False),"orbit_vs_486":(("case1","ideal_486",0),[]),"orbit_vs_729":(("case1","translate_729",0),[]),"premature_block_sum":(("case1","block_basis",0),[]),"member_lambda_u0":(("case2","lambda"),[]),"member_kappa_w":(("case2","kappa"),[]),"member_target":(("case2","replay_rows","C_kappa_w"),[]),"quotient_zero":(("case2","quotient_remainder"),[[[0,0,0],1]]),"dual_orbit_annihilation":(("case3","dual_orbit_pairings"),[1]),"dual_486_annihilation":(("case3","dual_486_pairings",0),1),"dual_729_annihilation":(("case3","dual_729_pairings",0),1),"dual_target_pairing":(("case3","dual_target_pairing"),0),"terminal_vocabulary":(("case1","terminal"),"BAD_TERMINAL"),"resource_terminal":(("case1","resource","cap"),"bad-cap"),"forbidden_conclusion":(("case1","pointed_mu1"),True)}
    records=[]
    for name in MUTATIONS:
        mutant=json.loads(json.dumps(cases)); path,replacement=specs[name]; key=path[0]; term=NONMEMBER if key=="case3" else MEMBER
        try:
            set_path(mutant,path,replacement); case=mutant[key]
            verify_gate(case,case["specialization_v216_abi"],term,"selftest")
            raise MutationAccepted("mutation accepted")
        except Stop as exc:
            require(str(exc)==EXPECTED_GATES[name],"mutation gate "+name); records.append({"name":name,"expected_gate":EXPECTED_GATES[name],"observed_reason":str(exc),"before_sha256":obj_digest(cases[key]),"after_sha256":obj_digest(mutant[key]),"rejected":True})
    require(len(records)==24 and [x["name"] for x in records]==MUTATIONS and all(x["rejected"] and x["before_sha256"]!=x["after_sha256"] for x in records),"independent mutation evidence"); return records
def independent_edge_controls(cases,claimed):
    expected=[("empty_task226_binding","TASK226_run","task226 binding run"),("empty_dual","CASE_DUAL_TARGET","dual target"),("empty_block_remainder","CASE_BLOCK_REMAINDER","block remainder")]
    require(type(claimed) is list and [x.get("name") for x in claimed]==[x[0] for x in expected],"edge control roster")
    binding={"run":"","head":"head","artifact_id":"artifact","zip_sha256":"zip"}
    try:
        for key in ("run","head","artifact_id","zip_sha256"): require(bool(type(binding.get(key)) is str and binding[key]),"task226 binding "+key)
        raise MutationAccepted("mutation accepted")
    except Stop as exc:
        require(str(exc)==expected[0][2],"edge binding gate")
    for index,(name,producer_gate,checker_gate) in enumerate(expected[1:],1):
        mutant=json.loads(json.dumps(cases["case3"])); mutant["dual" if name=="empty_dual" else "block_remainder"]=[]
        try:
            verify_gate(mutant,mutant["specialization_v216_abi"],NONMEMBER,"selftest")
            raise MutationAccepted("mutation accepted")
        except Stop as exc:
            require(str(exc)==checker_gate,"edge gate "+name)
        record=claimed[index]; require(record.get("expected_gate")==producer_gate and record.get("observed_reason")==producer_gate and record.get("rejected") is True and record.get("before_sha256")==obj_digest(cases["case3"]) and record.get("before_sha256")!=record.get("after_sha256"),"edge evidence "+name)
    binding_record=claimed[0]; require(binding_record.get("expected_gate")==expected[0][1] and binding_record.get("observed_reason")==expected[0][1] and binding_record.get("rejected") is True and binding_record.get("before_sha256")!=binding_record.get("after_sha256"),"edge evidence binding"); return True
def check_certificate(receipt,fixture,selftest):
    require(receipt.get("schema")== (SELFTEST_SCHEMA if selftest else SCHEMA),"consumer schema"); result=receipt.get("result"); require(type(result) is dict,"result");
    if not selftest and receipt.get("terminal") in (UNKNOWN_INPUT,UNKNOWN_RESOURCE): require(type(receipt.get("self_digest_sha256")) is str and type(result.get("phase",receipt.get("reason"))) is not type(None),"typed unknown"); return receipt["terminal"]
    abi=result.get("specialization_v216_abi"); check_abi(abi)
    if selftest:
        require(receipt.get("terminal")==SELFTEST and fixture.get("mutation_controls")==MUTATIONS,"selftest seal"); cases=result.get("cases"); require(type(cases) is dict and set(cases)=={"case1","case2","case3","case4_member","case4_nonmember"},"selftest cases"); accounting=result.get("scope_accounting"); validate_scope_accounting(accounting); resource=result.get("resource"); require(type(resource) is dict and set(resource)=={"caps","used"} and resource.get("caps")==EXPECTED_CAPS and resource.get("used")==accounting.get("max_used"),"resource accounting"); case_abis={name:cases[name].get("specialization_v216_abi") for name in cases}; require(all(type(case_abi) is dict for case_abi in case_abis.values()),"case ABI binding"); verify_gate(cases["case1"],case_abis["case1"],MEMBER,"selftest"); verify_gate(cases["case2"],case_abis["case2"],MEMBER,"selftest"); verify_gate(cases["case3"],case_abis["case3"],NONMEMBER,"selftest"); verify_gate(cases["case4_member"],case_abis["case4_member"],MEMBER,"selftest"); verify_gate(cases["case4_nonmember"],case_abis["case4_nonmember"],NONMEMBER,"selftest"); independent_edge_controls(cases,result.get("edge_controls")); checker_records=independent_mutations(cases); require([x["name"] for x in checker_records]==MUTATIONS and all(x["expected_gate"]==x["observed_reason"] for x in checker_records),"independent mutation roster"); controls=result.get("mutation_controls",{}); require(controls.get("attempted")==MUTATIONS and len(controls.get("rejected",[]))==len(MUTATIONS) and [x.get("name") for x in controls["rejected"]]==MUTATIONS and all({"name","changed_field","expected_gate","observed_reason","before_sha256","after_sha256","rejected"}<=set(x) and x["rejected"] is True and x["before_sha256"]!=x["after_sha256"] and x["observed_reason"]==x["expected_gate"] for x in controls["rejected"]),"mutation evidence"); return SELFTEST
    terminal=receipt.get("terminal"); require(terminal in (MEMBER,NONMEMBER,UNKNOWN_INPUT,UNKNOWN_RESOURCE),"terminal");
    if terminal in (MEMBER,NONMEMBER): verify_gate(result,abi,terminal,"production")
    require(all(receipt.get(flag) is False for flag in ("boundary_membership","pointed_mu1","exact_pb_endpoint_zero","cofinal_lift","fake","Ihara_witness")),"boundary flags")
    return terminal
def main(argv=None):
    parser=argparse.ArgumentParser(); parser.add_argument("receipt"); parser.add_argument("--selftest",action="store_true"); parser.add_argument("--fixture",default="search/certs/d972_r07_typed_single_seed_endpoint_consumer_selftest_v2_20260828.json"); parser.add_argument("--task226",default=TASK226); parser.add_argument("--task226-verdict",default=TASK226_VERDICT); parser.add_argument("--task226-binding",default=TASK226_BINDING); parser.add_argument("--verdict"); args=parser.parse_args(argv)
    try:
        receipt=json.loads(Path(args.receipt).read_bytes()); fixture=json.loads((ROOT/Path(args.fixture)).read_bytes()); abi=None if args.selftest else authenticate(load_json(args.task226,TASK226),load_json(args.task226_verdict,TASK226_VERDICT),load_json(args.task226_binding,TASK226_BINDING));
        if abi is not None: require(obj_digest(abi)==obj_digest(receipt.get("result",{}).get("specialization_v216_abi")),"embedded ABI mismatch")
        terminal=check_certificate(receipt,fixture,args.selftest)
        if args.verdict:
            p=Path(args.verdict); require(not p.exists() and not p.is_absolute() and p.as_posix().startswith("ci/out/"),"fresh verdict"); p.parent.mkdir(parents=True,exist_ok=True); p.write_bytes(canonical({"schema":SCHEMA+"/verdict","terminal":terminal,"accepted":terminal in (MEMBER,NONMEMBER),"independent":terminal in (MEMBER,NONMEMBER),"receipt_path":Path(args.receipt).as_posix(),"receipt_bytes":Path(args.receipt).stat().st_size,"receipt_sha256":obj_digest(receipt),"predecessor_abi_sha256":obj_digest(abi) if abi is not None else None,"recomputed_terminal":terminal,"occurrence_rank":receipt.get("result",{}).get("rank"),"block_rank":receipt.get("result",{}).get("block_rank"),"independent_reconstruction_sha256":obj_digest(receipt.get("result",{}))}))
        print("D227_CHECKER_TERMINAL "+terminal); return 0
    except (Stop,KeyError,ValueError,json.JSONDecodeError) as exc: print("D227_CHECKER_TERMINAL "+UNKNOWN_INPUT+" reason="+str(exc)); return 0
if __name__=="__main__": raise SystemExit(main())
