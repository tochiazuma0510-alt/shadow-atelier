"""Task 226/229 bounded actual two-word endpoint specializer.

The implementation is deliberately self contained.  In particular, the
checker has a second implementation; this file does not import it.
"""
from __future__ import annotations
import argparse, copy, hashlib, json, os, sys, time
try:
    import resource
except ImportError:
    resource=None
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "d972-r07-actual-two-word-endpoint-specializer/v2"
SELF_SCHEMA = SCHEMA + "/selftest"
SELFTEST = "R07_ACTUAL_TWO_WORD_ENDPOINT_SPECIALIZER_V2_SELFTEST_PASS"
COMPLETE = "R07_ACTUAL_TWO_WORD_ENDPOINT_SPECIALIZER_V2_COMPLETE"
UNKNOWN_INPUT = "UNKNOWN_INPUT"
UNKNOWN_RESOURCE = "UNKNOWN_RESOURCE"
MOD = 9
TASK192 = "ci/in/d972_r07_normalized_exact_common_word_cached_v3.json"
TASK198 = "ci/in/d972_r07_seven_context_roof_presentation_v1.json"
FIXTURE = "search/certs/d972_r07_actual_two_word_endpoint_specializer_selftest_v2_20260828.json"

MUTATIONS=["word_g0","word_a","word_f","ledger_block","ledger_sign","ledger_orientation","ledger_prefix","group_width","group_brackets","actor_convention","fox_d_occ","fox_d_raw","fox_B_a","fox_e","fox_D1_d","fox_D1_e","occurrence_p","u0_value","u0_provenance","abi_seal","task192_binding","task198_binding","terminal_input","terminal_resource","output_freshness","forbidden_conclusion"]

def canon(v):
    return json.dumps(v, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("ascii")
def digest(v): return hashlib.sha256(canon(v)).hexdigest()
def require(ok, msg):
    if ok is not True: raise Stop(msg)
class Stop(RuntimeError): pass
class MutationAccepted(RuntimeError): pass
def seal(value):
    """Verify a sealed receipt/ABI without changing its canonical payload."""
    require(type(value) is dict and type(value.get("self_digest_sha256")) is str,
            "missing receipt seal")
    body=dict(value); claimed=body.pop("self_digest_sha256")
    require(claimed==digest(body), "receipt seal mismatch")
    return body
def seal_task192(value):
    require(type(value) is dict and type(value.get("self_digest")) is str and "self_digest_sha256" not in value,"task192 seal dialect")
    body=dict(value);claimed=body.pop("self_digest");require(claimed==digest(body),"task192 seal mismatch");return body
def seal_task198(value):
    require(type(value) is dict and type(value.get("self_digest_sha256")) is str and "self_digest" not in value,"task198 seal dialect")
    return seal(value)
class ResourceStop(Stop):
    def __init__(self,phase,cap,value,limit): self.phase=phase; self.cap=cap; self.value=value; self.limit=limit
class Budget:
    caps={"input_bytes":2_100_000_000,"word_steps":2_000_000,"group_operations":2_000_000,"sparse_support":500_000,"mutation_work":100,"checker_work":2_000_000,"serialized_bytes":40_000_000,"wall_seconds":21600,"rss_bytes":6442450944}
    def __init__(self): self.used={k:0 for k in self.caps}; self.started=time.monotonic()
    def bump(self,cap,value,phase):
        self.used[cap]+=int(value)
        self.used["wall_seconds"]=max(self.used["wall_seconds"],int(time.monotonic()-self.started))
        if self.used[cap]>self.caps[cap]: raise ResourceStop(phase,cap,self.used[cap],self.caps[cap])
        if self.used["wall_seconds"]>self.caps["wall_seconds"]: raise ResourceStop(phase,"wall_seconds",self.used["wall_seconds"],self.caps["wall_seconds"])
    def output(self):
        rss=(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024 if resource else None)
        if rss is not None:
            self.used["rss_bytes"]=rss
            if rss>self.caps["rss_bytes"]: raise ResourceStop("rss measurement","rss_bytes",rss,self.caps["rss_bytes"])
        return {"caps":self.caps,"used":self.used,"peak_rss_bytes":rss}

def red(w):
    out=[]
    for x in w:
        require(type(x) is int and x != 0 and abs(x) <= 6, "word letter")
        if out and out[-1] == -x: out.pop()
        else: out.append(x)
    return out
def winv(w): return [-x for x in reversed(w)]
def pp(a,b): return red(list(b)+list(a))
def commword(a,b): return red(winv(a)+winv(b)+list(a)+list(b))
def subst(w,L,R):
    out=[]
    for x in w:
        z=L if abs(x)==1 else R
        out.extend(z if x>0 else winv(z))
    return red(out)

PB3 = ((1,2,3),(4,))
PB4 = ((1,2,3,4,5,6),(4,5,6,7))
PB3_BRACKETS = {(0,1):(1,),(0,2):(-1,),(1,2):(1,)}
PB4_BRACKETS = {
 (0,1):(1,0,0,0),(0,3):(-1,0,0,0),(1,3):(1,0,0,0),
 (0,2):(0,1,0,0),(0,4):(0,-1,0,0),(2,4):(0,1,0,0),
 (1,2):(0,0,1,0),(1,5):(0,0,-1,0),(2,5):(0,0,1,0),
 (3,4):(0,0,0,1),(3,5):(0,0,0,-1),(4,5):(0,0,0,1)
}
def bracket(i,j,d):
    if d==3:
        table=PB3_BRACKETS; width=1
    elif d==6:
        table=PB4_BRACKETS; width=4
    else:
        raise Stop("Q degree")
    if i==j:
        out=(0,)*width
    elif i>j:
        out=tuple(-x % MOD for x in bracket(j,i,d))
    else:
        out=tuple(x % MOD for x in table.get((i,j),(0,)*width))
    require(len(out)==width,"Q bracket width")
    return out
def cmul(a,b,d):
    na=a[:d]; nz=a[d:]; nb=b[:d]; nw=b[d:]
    c=[(na[i]+nb[i])%MOD for i in range(d)]
    z=[(nz[i]+nw[i])%MOD for i in range(len(nz))]
    for i in range(d):
        for j in range(i+1,d):
            q=bracket(i,j,d)
            for k in range(len(z)): z[k]=(z[k]-na[j]*nb[i]*q[k])%MOD
    return tuple(c+z)
def cinv(a,d):
    z=[(-x)%MOD for x in a[d:]]
    for i in range(d):
        for j in range(i+1,d):
            q=bracket(i,j,d)
            for k in range(len(z)): z[k]=(z[k]-a[i]*a[j]*q[k])%MOD
    return tuple([(-x)%MOD for x in a[:d]]+z)
def ceval(w,d):
    ncent=1 if d==3 else 4; one=(0,)*(d+ncent); value=one
    for letter in w:
        g=[0]*(d+ncent); g[abs(letter)-1]=1
        value=cmul(value,tuple(g),d) if letter>0 else cmul(value,cinv(tuple(g),d),d)
    return value
def class2_facts(d):
    ncent=1 if d==3 else 4; one=(0,)*(d+ncent); gens=[]
    for i in range(d):
        g=[0]*(d+ncent);g[i]=1;gens.append(tuple(g));require(cmul(gens[-1],cinv(gens[-1],d),d)==one,"Q inverse")
        q=one
        for _ in range(9):q=cmul(q,gens[-1],d)
        require(q==one,"Q ninth power")
    require(cmul(cmul(gens[0],gens[1],d),gens[2],d)==cmul(gens[0],cmul(gens[1],gens[2],d),d),"Q associativity")
    for i in range(d):
        for j in range(i+1,d):
            h=cmul(cmul(cmul(cinv(gens[i],d),cinv(gens[j],d),d),gens[i],d),gens[j],d)
            expected=[0]*ncent; q=bracket(i,j,d)
            require(h==tuple([0]*d+list(q)),"Q commutator")
    if d==3:
        require(bracket(0,1,d)==(1,),"Q positive PB3 canonical")
        require(bracket(0,2,d)==(8,),"Q negative PB3 canonical")
    if d==6:
        require(bracket(0,1,d)==(1,0,0,0),"Q positive PB4 canonical")
        require(bracket(0,3,d)==(8,0,0,0),"Q negative PB4 canonical")
    return {"degree":d,"width":d+ncent,"generator_count":len(gens),"brackets_checked":d*(d-1)//2}
def exhaustive_arithmetic_oracle():
    """Independent finite oracle: every PB3 element/pair and direct word roster."""
    one=(0,0,0,0); vals=[tuple(a)+tuple(z) for a in __import__("itertools").product(range(3),repeat=3) for z in __import__("itertools").product(range(3),repeat=1)]
    for a in vals:
        require(cmul(a,cinv(a,3),3)==one and cmul(cinv(a,3),a,3)==one,"PB3 exhaustive inverse")
        for b in vals:
            for c in vals:
                require(cmul(cmul(a,b,3),c,3)==cmul(a,cmul(b,c,3),3),"PB3 exhaustive associativity")
    for i,j in ((0,1),(0,2),(1,0),(1,2),(2,0),(2,1)):
        require(ceval(commword([i+1],[j+1]),3)==tuple([0,0,0]+list(bracket(i,j,3))),"PB3 direct bracket roster")
    for i,j in PB4_BRACKETS:
        require(ceval(commword([i+1],[j+1]),6)==tuple([0]*6+list(bracket(i,j,6))),"PB4 direct bracket roster")
        require(ceval(commword([j+1],[i+1]),6)==tuple([0]*6+list(bracket(j,i,6))),"PB4 inverse bracket roster")
def actor_mul(a,b):
    # Frozen normal form x^a y^b h^r: central coordinate r+r'-b*a'.
    return ((a[0]+b[0])%MOD,(a[1]+b[1])%MOD,(a[2]+b[2]-a[1]*b[0])%MOD)
def actor_inv(a): return ((-a[0])%MOD,(-a[1])%MOD,(-a[2]-a[0]*a[1])%MOD)
def actor_eval(w):
    x=(1,0,0); y=(0,1,0); v=(0,0,0)
    for q in w: v=actor_mul(v, x if q==1 else actor_inv(x) if q==-1 else y if q==2 else actor_inv(y))
    return v
def actor_facts():
    vals=[(i,j,k) for i in range(MOD) for j in range(MOD) for k in range(MOD)]
    one=(0,0,0); h=actor_eval([-1,-2,1,2]); z=actor_mul(actor_mul(h,h),h)
    require(h==(0,0,1) and z==(0,0,3), "actor commutator/cube")
    require(all(actor_mul(v,actor_inv(v))==one for v in vals), "actor inverse")
    require(actor_mul(actor_mul((1,2,3),(4,5,6)),(7,8,0))==actor_mul((1,2,3),actor_mul((4,5,6),(7,8,0))), "actor associativity")
    require(actor_eval([1]*9)==one and actor_eval([2]*9)==one, "actor ninth powers")
    cosets={frozenset(actor_mul((0,0,3*j),v) for j in range(3)) for v in vals}
    require(len(cosets)==243 and sum(len(x) for x in cosets)==729, "actor cosets")
    return {"order":729,"h":list(h),"z0":list(z),"quotient_order":243,"cosets":243}

def sparse_add(a,b,scale=1):
    r=dict(a)
    for k,v in b.items(): r[k]=(r.get(k,0)+scale*v)%3
    return {k:v for k,v in r.items() if v%3}
def sparse_scale(a,s): return {k:(v*s)%3 for k,v in a.items() if (v*s)%3}
def sparse_translate(a,g,d):
    out={}
    for k,v in a.items(): out= sparse_add(out,{cmul(g,k,d):v})
    return out
def tag(block,a): return {(block,i,q):v for (i,q),v in a.items()}
def chain_add(a,b,scale=1):
    r=dict(a)
    for k,v in b.items(): r[k]=(r.get(k,0)+scale*v)%3
    return {k:v for k,v in r.items() if v%3}
def chain_left(g,a,d):
    out={}
    for (block,i,q),v in a.items():
        k=(block,i,cmul(g,q,d)); out[k]=(out.get(k,0)+v)%3
    return {k:v for k,v in out.items() if v}
def left_group(g,a,d):
    out={}
    for (i,q),v in a.items():
        k=(i,cmul(g,q,d)); out[k]=(out.get(k,0)+v)%3
    return {k:v for k,v in out.items() if v}
def fox(w,d):
    one=(0,)*(d+(1 if d==3 else 4)); cur=one; out={}
    for letter in w:
        g=[0]*(d+(1 if d==3 else 4)); g[abs(letter)-1]=1; g=tuple(g)
        if letter>0:
            out[(abs(letter)-1,cur)]=(out.get((abs(letter)-1,cur),0)+1)%3; cur=cmul(cur,g,d)
        else:
            cur=cmul(cur,cinv(g,d),d); out[(abs(letter)-1,cur)]=(out.get((abs(letter)-1,cur),0)-1)%3
    return {k:v for k,v in out.items() if v}
def endpoint_block(chain,wanted_block,d):
    one=(0,)*(d+(1 if d==3 else 4)); r={}
    for (block,i,q),v in chain.items():
        if block != wanted_block: continue
        g=[0]*len(one); g[i]=1; g=tuple(g)
        qg=cmul(q,g,d); r[qg]=(r.get(qg,0)+v)%3; r[q]=(r.get(q,0)-v)%3
    return {k:v for k,v in r.items() if v}

def d1_block(chain,block,d):
    return endpoint_block(chain,block,d)
def jsparse(a):
    return [{"component":i,"key":list(q),"coefficient":v} for (i,q),v in sorted(a.items())]
def jschain(a):
    return [{"block":b,"component":i,"key":list(q),"coefficient":v} for (b,i,q),v in sorted(a.items())]
def jsg(a): return [{"key":list(q),"coefficient":v} for q,v in sorted(a.items())]

def ledger():
    blocks=["H1","H1","H1","H2","H2","H2","P1","P2","P3","P5","P4"]
    typ=["E3"]*6+["E4"]*5; ten=[0,1,2,3,0,4,5,6,7,8,9]
    ctx=[21,22,23,24,21,25,1,27,21,26,28]
    roles=["hexagon_fxy","hexagon_fxz","hexagon_fyz","hexagon_fux","hexagon_fxy","hexagon_fuy","pentagon_b1","pentagon_b2","pentagon_b3","pentagon_b5_inverse_slot","pentagon_b4_inverse_slot"]
    signs=[1,-1,1,-1,-1,1,1,1,1,-1,-1]
    orient=["direct","inverse","direct","inverse","inverse","direct","direct","direct","direct","inverse","inverse"]
    pref=[[3,2],[3],[],[6,5],[6],[],[11,10,9,8],[11,10,9],[11,10],[11],[]]
    return [{"ordinal":i+1,"block":b,"block_index":1 if b=="H1" else 2 if b=="H2" else i-3,"block_slot":1 if b not in ("H1","H2") else (i%3)+1,"occurrence":(["H1_fxy","H1_fxz","H1_fyz","H2_fux","H2_fxy","H2_fuy","P_b1","P_b2","P_b3","P_b5_inverse","P_b4_inverse"])[i],"type":typ[i],"ten_index":ten[i],"context_id":ctx[i],"role":roles[i],"factor_sign":signs[i],"orientation":orient[i],"fox_prefix_occurrences":pref[i]} for i,b in enumerate(blocks)]
EXPECTED=ledger()
def check_ledger(rows):
    require(rows==EXPECTED,"literal ledger differs from task198 A.18 roster")

def substitutions():
    x=[1]; y=[3]; z=winv(pp(x,y)); u=winv(pp(y,x))
    h1=[(x,y,1),(x,z,-1),(y,z,1)]
    h2=[(u,x,-1),(x,y,-1),(u,y,1)]
    a12=[1];a13=[2];a14=[3];a23=[4];a24=[5];a34=[6]
    b=[(a23,a34,1),(pp(a12,a13),pp(a24,a34),1),(a12,a23,1),(pp(a13,a23),a34,-1),(a12,pp(a23,a24),-1)]
    return {"PB3":{"x":x,"y":y,"z":z,"u":u,"H1":h1,"H2":h2},"PB4":{"generators":[a12,a13,a14,a23,a24,a34],"b_display":b,"natural_index":[1,3,0,2,4]}}
def display_factor_words(sub):
    e=sub["PB3"]; h=e["H1"]+e["H2"]
    p=sub["PB4"]["b_display"]
    return [commword(a,b) for a,b,s in h+p], [s for a,b,s in h+p]
def eval_pair(pair,d): return ceval(pair[0],d),ceval(pair[1],d)

def specialize(g0,a,rows):
    sub=substitutions(); factors, factor_signs=display_factor_words(sub); require(len(factors)==11,"factor count")
    pairs=[(a,b) for a,b,s in sub["PB3"]["H1"]+sub["PB3"]["H2"]+sub["PB4"]["b_display"]]
    f=red(g0+a); d=3; q4=6
    rwords_g=[red(subst(g0,L,R)) for L,R in pairs]
    rwords_f=[red(subst(f,L,R)) for L,R in pairs]
    rkeys_g=[ceval(w,3 if i<6 else 6) for i,w in enumerate(rwords_g)]
    rkeys_f=[ceval(w,3 if i<6 else 6) for i,w in enumerate(rwords_f)]
    base_g=[w if factor_signs[i]==1 else winv(w) for i,w in enumerate(rwords_g)]
    base_f=[w if factor_signs[i]==1 else winv(w) for i,w in enumerate(rwords_f)]
    rg=[]; rf=[]; occ=[]
    relation_words=[]; relation_words_f=[]
    for lo,hi in ((0,3),(3,6),(6,11)):
        bw=[]
        bwf=[]
        for j in reversed(range(lo,hi)): bw.extend(base_g[j]); bwf.extend(base_f[j])
        relation_words.append(red(bw))
        relation_words_f.append(red(bwf))
    rg=red([x for block in relation_words for x in block]); rf=red([x for block in relation_words_f for x in block])
    for idx,row in enumerate(rows):
        rr=rwords_g[idx]; dd=3 if idx<6 else 6; r=rkeys_g[idx]
        q=tuple((0,)*(dd+(1 if dd==3 else 4))); prefix_word=[]
        for j in row["fox_prefix_occurrences"]:
            zf=base_g[j-1]; prefix_word.extend(zf); q=cmul(q,ceval(zf,dd),dd)
        p=cmul(q,r,dd) if row["orientation"]=="direct" else q
        ri=cinv(r,dd); zero=(0,)*(dd+(1 if dd==3 else 4)); xi=sparse_add({}, {ri:1}); xi=sparse_add(xi,{zero:2}); w=sparse_scale(xi,row["factor_sign"])
        # left multiplication by p, performed explicitly for this occurrence
        w={k:v for k,v in w.items()}; w={cmul(p,k,dd):v for k,v in w.items()}
        qx,qy=eval_pair(pairs[idx],dd)
        comm=commword(pairs[idx][0],pairs[idx][1]); z0w=red(comm*3)
        hq=cmul(cmul(cmul(cinv(qx,dd),cinv(qy,dd),dd),qx,dd),qy,dd); kz=cmul(cmul(hq,hq,dd),hq,dd)
        actor_k=cmul(cmul(p,kz,dd),cinv(p,dd),dd)
        translated=sparse_translate(w,actor_k,dd); u0=sparse_add(translated,w,-1)
        cb="H1" if row["block"]=="H1" else "H2" if row["block"]=="H2" else "P"
        occ.append({"ordinal":row["ordinal"],"combined_block":cb,"block":row["block"],"block_index":row["block_index"],"block_slot":row["block_slot"],"occurrence":row["occurrence"],"type":row["type"],"q_degree":3 if dd==3 else 4,"key_width":4 if dd==3 else 10,"ten_index":row["ten_index"],"context_id":row["context_id"],"role":row["role"],"factor_sign":row["factor_sign"],"orientation":row["orientation"],"fox_prefix_occurrences":row["fox_prefix_occurrences"],"signed_prefix_word":list(prefix_word),"signed_prefix":list(q),"base_g":list(base_g[idx]),"base_f":list(base_f[idx]),"rword_g":list(red(subst(g0,pairs[idx][0],pairs[idx][1]))),"rword_f":list(red(subst(f,pairs[idx][0],pairs[idx][1]))),"r_g":list(r),"r_f":list(ceval(red(subst(f,pairs[idx][0],pairs[idx][1])),dd)),"p_o":list(p),"q_o(x)":list(qx),"q_o(y)":list(qy),"z0_source_word":z0w,"q_o(z0)":list(kz),"k_o(z0)":list(actor_k),"xi_o":jsg(xi),"w_o":jsg(w),"translated":jsg(translated),"translated_w_o":jsg(translated),"u0":jsg(u0),"ancestry":{"source":"task179_A18","substitution":"PB3/PB4_literal","prefix":"task198_one_based_signed"}})
    dchain={}; raw_chain={}; ba_chain={}; residual={}; eps_blocks={}
    d_occ_blocks={}; d_raw_blocks={}; ba_blocks={}; e_blocks={}; minus_f_blocks={}; minus_g_blocks={}
    one_g_blocks={}; one_f_blocks={}; d1_d_blocks={}; d1_e_blocks={}
    # Every block is decoded independently.  H1/H2 are Q3 and P is Q4;
    # no mixed chain is ever passed to a one-degree endpoint decoder.
    for lo,hi,cb,dd in ((0,3,"H1",3),(3,6,"H2",3),(6,11,"P",6)):
        bw=[]; bwf=[]
        for j in reversed(range(lo,hi)): bw.extend(base_g[j]); bwf.extend(base_f[j])
        block_raw=tag(cb,sparse_scale(fox(red(bw),dd),-1)); block_chain={}
        for row,o in zip(rows[lo:hi],occ[lo:hi]):
            po=tuple(o["p_o"]); grad=fox(winv(rwords_g[row["ordinal"]-1]),dd)
            block_chain=chain_add(block_chain,tag(cb,sparse_scale(left_group(po,grad,dd),row["factor_sign"])))
        block_g=tag(cb,fox(red(bw),dd)); block_f=tag(cb,fox(red(bwf),dd))
        block_ba=chain_add(block_f,block_g,-1); block_residual=chain_add(block_chain,block_ba,-1)
        dchain=chain_add(dchain,block_chain); raw_chain=chain_add(raw_chain,block_raw)
        ba_chain=chain_add(ba_chain,block_ba); residual=chain_add(residual,block_residual)
        d_occ_blocks[cb]=jschain(block_chain); d_raw_blocks[cb]=jschain(block_raw)
        ba_blocks[cb]=jschain(block_ba); e_blocks[cb]=jschain(block_residual)
        block_eps=endpoint_block(block_residual,cb,dd)
        eps_blocks[cb]=jsg(block_eps)
        one=(0,)*(dd+(1 if dd==3 else 4))
        eg=sparse_add({},{one:1}); eg=sparse_add(eg,{ceval(red(bw),dd):-1}); ef=sparse_add({},{one:1}); ef=sparse_add(ef,{ceval(red(bwf),dd):-1})
        one_g_blocks[cb]=jsg(eg); one_f_blocks[cb]=jsg(ef)
        minus_g_blocks[cb]=jschain(tag(cb,sparse_scale(fox(red(bw),dd),-1)))
        minus_f_blocks[cb]=jschain(tag(cb,sparse_scale(fox(red(bwf),dd),-1)))
        d1_d_blocks[cb]=jsg(endpoint_block(block_chain,cb,dd)); d1_e_blocks[cb]=jsg(endpoint_block(block_residual,cb,dd))
        require(block_chain==block_raw,"d_occ != d_raw in "+cb)
        require(block_residual==chain_add(block_chain,block_ba,-1),"e definition")
        require(endpoint_block(block_chain,cb,dd)==eg,"D1 d_occ "+cb)
        require(endpoint_block(block_residual,cb,dd)==ef,"D1 e "+cb)
        require(block_residual==tag(cb,sparse_scale(fox(red(bwf),dd),-1)),"e != -fox(Rf) "+cb)
    identities={}
    for cb in ("H1","H2","P"):
        identities["d_occ_equals_d_raw_"+cb]=d_occ_blocks[cb]==d_raw_blocks[cb]
        identities["e_equals_minus_fox_Rf_"+cb]=e_blocks[cb]==minus_f_blocks[cb]
        identities["D1_d_occ_"+cb]=d1_d_blocks[cb]==one_g_blocks[cb]
        identities["D1_e_"+cb]=d1_e_blocks[cb]==one_f_blocks[cb]
    identities["word_specific_boundary_not_used"]=True
    require(all(identities.values()),"computed Fox identity")
    group={"modulus":9,"q3_width":4,"q4_width":10,"actor_width":3,"PB3_brackets":[[list(k),list(v)] for k,v in PB3_BRACKETS.items()],"PB4_brackets":[[list(k),list(v)] for k,v in PB4_BRACKETS.items()],"PB3_facts":class2_facts(3),"PB4_facts":class2_facts(6),"actor":actor_facts()}
    u0_rows=[]
    for o in occ:
        u0_rows.append({"ordinal":o["ordinal"],"terms":o["w_o"],"translated_terms":o["translated"],"source_coefficient_terms":[{"source":"translated","coefficient":1,"terms":o["translated"]},{"source":"original","coefficient":-1,"terms":o["w_o"],"ancestry":o["ancestry"]}]})
    abi={"schema":"d972-r07-v216-specialization-abi/v1","modulus":9,"actor_convention":"x^a y^b h^r; [x,y]=x^-1 y^-1 x y=(0,0,1), product r+r'-b*a', inverse (-a,-b,-r-a*b) mod 9, z0=(0,0,3)","ledger":rows,"occurrences":occ,"bar_epsilon_1":eps_blocks,"u0":u0_rows,"ten_to_eleven":[r["ten_index"] for r in rows],"occurrence_ledger_sha256":digest(rows),"insertion_digest":digest({"substitutions":sub,"static_substitution_factors":factors}),"literals":{"substitutions":sub,"static_substitution_factors":[{"left":list(L),"right":list(R),"factor_sign":s} for L,R,s in sub["PB3"]["H1"]+sub["PB3"]["H2"]+sub["PB4"]["b_display"]],"relation_factors_g":[list(w) for w in base_g],"relation_factors_f":[list(w) for w in base_f],"relation_words_g":relation_words,"relation_words_f":relation_words_f,"rword_g":rwords_g,"rword_f":rwords_f,"R_B_g0":relation_words,"R_B_f":relation_words_f,"rg":rg,"rf":rf,"d_occ":d_occ_blocks,"d_raw":d_raw_blocks,"B_a":ba_blocks,"e":e_blocks,"one_minus_R_g":one_g_blocks,"one_minus_R_f":one_f_blocks,"D1_d_occ":d1_d_blocks,"D1_e":d1_e_blocks,"minus_fox_Rg":minus_g_blocks,"minus_fox_Rf":minus_f_blocks}}
    abi["self_digest_sha256"]=digest(abi)
    return {"words":{"g0":g0,"a":a,"f":f,"f_equals_reduce_g0_plus_a":f==red(g0+a)},"occurrences":rows,"group":group,"identities":identities,"w":[o["w_o"] for o in occ],"epsilon":eps_blocks,"u0":[{"ordinal":o["ordinal"],"terms":o["w_o"],"translated_terms":o["translated"],"u0":o["u0"]} for o in occ],"specialization_v216_abi":abi}

def validate_package(pkg):
    require(pkg.get("words",{}).get("f")==red(pkg["words"]["g0"]+pkg["words"]["a"]),"mutation word")
    check_ledger(pkg.get("occurrences")); require(pkg["group"]["q3_width"]==4 and pkg["group"]["q4_width"]==10,"mutation width")
    require(pkg["group"].get("PB3_brackets")==[[list(k),list(v)] for k,v in PB3_BRACKETS.items()] and pkg["group"].get("PB4_brackets")==[[list(k),list(v)] for k,v in PB4_BRACKETS.items()],"Q facts")
    require(pkg["group"]["actor"]["cosets"]==243,"mutation actor")
    require(all(type(v) is bool and v for v in pkg["identities"].values()),"mutation identity")
    require(len(pkg["u0"])==11 and all(set(q)=={"ordinal","terms","translated_terms","u0"} for q in pkg["u0"]),"mutation u0")
    require(all(pkg["u0"][i]["u0"]==pkg["specialization_v216_abi"]["occurrences"][i]["u0"] for i in range(11)),"u0 provenance")
    if "terminal_probes" in pkg:
        require(pkg["terminal_probes"].get("input",{}).get("terminal")==UNKNOWN_INPUT and pkg["terminal_probes"].get("resource",{}).get("terminal")==UNKNOWN_RESOURCE,"terminal probe gate")
    require(pkg.get("output_guard")=="fresh-output-only","fresh output gate")
    if "predecessor_bindings" in pkg:
        if "canary" in pkg["predecessor_bindings"].get("task192",{}): require(pkg["predecessor_bindings"].get("task192",{}).get("canary")=="task192-selftest-binding" and pkg["predecessor_bindings"].get("task198",{}).get("canary")=="task198-selftest-binding","predecessor binding gate")
    abi=pkg.get("specialization_v216_abi",{}); require(abi.get("schema")=="d972-r07-v216-specialization-abi/v1","mutation ABI schema")
    require(abi.get("actor_convention")=="x^a y^b h^r; [x,y]=x^-1 y^-1 x y=(0,0,1), product r+r'-b*a', inverse (-a,-b,-r-a*b) mod 9, z0=(0,0,3)","actor convention gate")
    claimed=abi.get("self_digest_sha256"); abi_body={k:v for k,v in abi.items() if k!="self_digest_sha256"}; require(type(claimed) is str and claimed==digest(abi_body),"ABI seal")
    require(set(abi.get("bar_epsilon_1",{}))=={"H1","H2","P"},"epsilon block schema")
    require(len(abi.get("u0",[]))==11 and all(set(q)=={"ordinal","terms","translated_terms","source_coefficient_terms"} for q in abi["u0"]),"u0 rows")
    for i,q in enumerate(abi["u0"]):
        o=abi["occurrences"][i]; src=q["source_coefficient_terms"]
        require(q["terms"]==o["w_o"] and q["translated_terms"]==o["translated"],"u0 summands")
        require(src==[{"source":"translated","coefficient":1,"terms":o["translated"]},{"source":"original","coefficient":-1,"terms":o["w_o"],"ancestry":o["ancestry"]}],"u0 provenance")
    lit=abi.get("literals",{}); require("static_substitution_factors" in lit and "relation_factors_g" in lit and "relation_factors_f" in lit,"typed literal ledger")
    pairs=[(L,R) for L,R,s in substitutions()["PB3"]["H1"]+substitutions()["PB3"]["H2"]+substitutions()["PB4"]["b_display"]]
    require(len(abi.get("occurrences",[]))==11 and len(lit.get("rword_g",[]))==11 and len(lit.get("rword_f",[]))==11,"actual word roster")
    for i,o in enumerate(abi["occurrences"]):
        require(o.get("rword_g")==red(subst(pkg["words"]["g0"],*pairs[i])) and o.get("rword_f")==red(subst(pkg["words"]["f"],*pairs[i])) and lit["rword_g"][i]==o["rword_g"] and lit["rword_f"][i]==o["rword_f"],"actual word replay")
    rebuilt=specialize(pkg["words"]["g0"],pkg["words"]["a"],pkg["occurrences"])
    for key in ("words","occurrences","group","identities","w","epsilon","u0","specialization_v216_abi"):
        require(pkg.get(key)==rebuilt.get(key),"fresh complete ABI rebuild" if key=="specialization_v216_abi" else "fresh complete "+key+" rebuild")
    for flag in ("boundary_membership","pointed_mu1","exact_pb_endpoint_zero","cofinal_lift","fake","Ihara_witness"): require(pkg.get(flag,False) is False,"forbidden conclusion:"+flag)
def zero_safe_oracle():
    one=(0,0,0,0); require(sparse_add({},{one:1})=={one:1},"r_o=1 setup")
    xi=sparse_add({one:1},{one:2}); endpoint_one_minus_two=sparse_add({one:1},{one:2})
    translated_minus_original=sparse_add({one:1},{one:1},-1)
    require(xi=={},"xi coincident key")
    require(endpoint_one_minus_two=={},"one-minus endpoint coincident key")
    require(translated_minus_original=={},"translated-minus-original coincident key")
MUTATION_GATES={"word_g0":"mutation word","word_a":"mutation word","word_f":"mutation word","ledger_block":"literal ledger","ledger_sign":"literal ledger","ledger_orientation":"literal ledger","ledger_prefix":"literal ledger","group_width":"mutation width","group_brackets":"Q facts","actor_convention":"actor convention","fox_d_occ":"fresh complete ABI rebuild","fox_d_raw":"fresh complete ABI rebuild","fox_B_a":"fresh complete ABI rebuild","fox_e":"fresh complete ABI rebuild","fox_D1_d":"fresh complete ABI rebuild","fox_D1_e":"fresh complete ABI rebuild","occurrence_p":"fresh complete ABI rebuild","u0_value":"u0 provenance","u0_provenance":"u0 provenance","abi_seal":"ABI seal","task192_binding":"predecessor binding","task198_binding":"predecessor binding","terminal_input":"terminal probe gate","terminal_resource":"terminal probe gate","output_freshness":"fresh output gate","forbidden_conclusion":"forbidden conclusion"}
def mutation_owner(bundle,name):
    if name=="word_g0": return bundle["words"]["g0"]
    if name=="word_a": return bundle["words"]["a"]
    if name=="word_f": return bundle["words"]["f"]
    if name=="ledger_block": return bundle["occurrences"][0]["block"]
    if name=="ledger_sign": return bundle["occurrences"][0]["factor_sign"]
    if name=="ledger_orientation": return bundle["occurrences"][0]["orientation"]
    if name=="ledger_prefix": return bundle["occurrences"][0]["fox_prefix_occurrences"]
    if name=="group_width": return {"q3":bundle["group"]["q3_width"],"q4":bundle["group"]["q4_width"]}
    if name=="group_brackets": return bundle["group"]["PB3_brackets"]+bundle["group"]["PB4_brackets"]
    if name=="actor_convention": return bundle["specialization_v216_abi"]["actor_convention"]
    if name=="fox_d_occ": return bundle["specialization_v216_abi"]["literals"]["d_occ"]
    if name=="fox_d_raw": return bundle["specialization_v216_abi"]["literals"]["d_raw"]
    if name=="fox_B_a": return bundle["specialization_v216_abi"]["literals"]["B_a"]
    if name=="fox_e": return bundle["specialization_v216_abi"]["literals"]["e"]
    if name=="fox_D1_d": return bundle["specialization_v216_abi"]["literals"]["D1_d_occ"]
    if name=="fox_D1_e": return bundle["specialization_v216_abi"]["literals"]["D1_e"]
    if name=="occurrence_p": return bundle["specialization_v216_abi"]["occurrences"][0]["p_o"]
    if name=="u0_value": return bundle["u0"][0]["u0"]
    if name=="u0_provenance": return bundle["specialization_v216_abi"]["u0"][0]["source_coefficient_terms"]
    if name=="abi_seal": return bundle["specialization_v216_abi"]["self_digest_sha256"]
    if name=="task192_binding": return bundle.get("predecessor_bindings",{}).get("task192",{})
    if name=="task198_binding": return bundle.get("predecessor_bindings",{}).get("task198",{})
    if name=="terminal_input": return bundle["terminal_probes"]["input"]
    if name=="terminal_resource": return bundle["terminal_probes"]["resource"]
    if name=="output_freshness": return bundle.get("output_guard")
    if name=="forbidden_conclusion": return [bundle.get(k,False) for k in ("boundary_membership","pointed_mu1","exact_pb_endpoint_zero","cofinal_lift","fake","Ihara_witness")]
    raise Stop("unregistered mutation owner")
def reseal_abi(bundle):
    ab=bundle["specialization_v216_abi"];ab["self_digest_sha256"]=digest({k:v for k,v in ab.items() if k!="self_digest_sha256"})
def mutation_execution(pkg):
    records=[]
    for name in MUTATIONS:
        changed=copy.deepcopy(pkg)
        changed_field=name
        before=digest(mutation_owner(pkg,name))
        try:
            if name=="word_g0": changed["words"]["g0"][1]=-2
            elif name=="word_a": changed["words"]["a"][0]=-2
            elif name=="word_f": changed["words"]["f"]=list(reversed(changed["words"]["f"]))
            elif name=="ledger_block": changed["occurrences"][0]["block"]="H2"
            elif name=="ledger_sign": changed["occurrences"][0]["factor_sign"]*=-1
            elif name=="ledger_orientation": changed["occurrences"][0]["orientation"]="inverse"
            elif name=="ledger_prefix": changed["occurrences"][0]["fox_prefix_occurrences"]=list(reversed(changed["occurrences"][0]["fox_prefix_occurrences"]))
            elif name=="group_width": changed["group"]["q3_width"]+=1
            elif name=="group_brackets": changed["group"]["PB3_brackets"][0][1][0]+=1
            elif name=="actor_convention": changed["specialization_v216_abi"]["actor_convention"]="mutated"
            elif name.startswith("fox_"): changed["specialization_v216_abi"]["literals"][{"fox_d_occ":"d_occ","fox_d_raw":"d_raw","fox_B_a":"B_a","fox_e":"e","fox_D1_d":"D1_d_occ","fox_D1_e":"D1_e"}[name]]["H1"]=[]
            elif name=="occurrence_p": changed["specialization_v216_abi"]["occurrences"][0]["p_o"]=[]
            elif name=="u0_value": changed["u0"][0]["u0"]=[]
            elif name=="u0_provenance": changed["specialization_v216_abi"]["u0"][0]["source_coefficient_terms"]=[]
            elif name=="abi_seal": changed["specialization_v216_abi"]["self_digest_sha256"]="0"*64
            elif name in ("task192_binding","task198_binding"): changed["predecessor_bindings"]["task192" if name.startswith("task192") else "task198"]["canary"]="mutated"
            elif name=="terminal_input": changed["terminal_probes"]["input"]["terminal"]=COMPLETE
            elif name=="terminal_resource": changed["terminal_probes"]["resource"]["terminal"]=COMPLETE
            elif name=="output_freshness": changed["output_guard"]="mutated"
            elif name=="forbidden_conclusion": changed["fake"]=True
            else: raise Stop("unregistered mutation owner")
            if name!="abi_seal": reseal_abi(changed)
            validate_package(changed)
        except MutationAccepted:
            raise
        except Stop as e:
            reason=str(e);gate=MUTATION_GATES[name];require(gate.lower() in reason.lower(),"mutation gate mismatch:"+name);after=digest(mutation_owner(changed,name));require(before!=after,"mutation did not change owner:"+name);records.append({"name":name,"changed_field":name,"expected_gate":gate,"observed_reason":reason,"target_before":before,"target_after":after,"rejected":True})
        else:
            raise MutationAccepted("accepted mutation:"+name)
    require(len(records)==len(MUTATIONS) and all(x["rejected"] for x in records),"mutation execution")
    return records
def envelope(schema,terminal,result,extra=None):
    v={"schema":schema,"terminal":terminal,"result":result};
    if extra: v.update(extra)
    v["self_digest_sha256"]=digest(v); return v
def input_json(path):
    raw_path=str(path); p0=Path(raw_path)
    require(not p0.is_absolute() and ".." not in p0.parts and raw_path.replace("\\","/")==p0.as_posix(),"input path alias")
    p=ROOT/p0; require(raw_path.startswith("ci/in/") and p.exists(),"missing input")
    raw=p.read_bytes(); return authenticate_input(raw,raw_path)
def authenticate_input(raw,raw_path):
    require(str(raw_path).startswith("ci/in/") and isinstance(raw,(bytes,bytearray)),"input authenticator path")
    v=json.loads(raw); require(raw==canon(v),"noncanonical input"); return v,bytes(raw)
def execute_terminal_probes(budget):
    try: authenticate_input(b"{","ci/in/fresh-malformed-probe.json"); raise Stop("malformed input unexpectedly accepted")
    except (Stop,KeyError,ValueError,json.JSONDecodeError,UnicodeError,TypeError) as e: bad=envelope(SCHEMA,UNKNOWN_INPUT,{"reason":str(e)})
    old=budget.caps["checker_work"]; budget.caps["checker_work"]=0
    try: budget.bump("checker_work",1,"live resource probe"); raise Stop("resource probe unexpectedly accepted")
    except ResourceStop as e: limited=envelope(SCHEMA,UNKNOWN_RESOURCE,{"reason":{"phase":e.phase,"cap":e.cap,"value":e.value,"limit":e.limit}})
    finally: budget.caps["checker_work"]=old
    return bad,limited
def attest(path,receipt_path,receipt_bytes,expected_schema):
    p0=Path(str(path)); require(not p0.is_absolute() and ".." not in p0.parts and str(path).replace("\\","/")==p0.as_posix() and str(path).startswith("ci/in/"),"attestation path alias")
    p=ROOT/p0; require(p.exists(),"missing attestation")
    raw=p.read_bytes(); require(raw==canon(json.loads(raw)),"noncanonical attestation"); v=json.loads(raw); seal(v); require(v.get("schema")==expected_schema,"attestation schema")
    require(v.get("receipt_path")==receipt_path and v.get("receipt_bytes")==len(receipt_bytes) and v.get("receipt_sha256")==hashlib.sha256(receipt_bytes).hexdigest(),"attestation receipt binding")
    receipt_value=json.loads(receipt_bytes); require(v.get("member_path")==receipt_path and v.get("member_bytes")==len(receipt_bytes) and v.get("member_sha256")==hashlib.sha256(receipt_bytes).hexdigest() and v.get("terminal")==receipt_value.get("terminal"),"attestation member binding")
    for key in ("run_id","head_sha","artifact_id","member_path","member_bytes","member_sha256","checker_path","checker_bytes","checker_sha256","checker_line"):
        require(key in v and v.get(key) not in (None,""),"attestation immutable field:"+key)
    require(v.get("terminal") not in (SELFTEST,UNKNOWN_INPUT,UNKNOWN_RESOURCE) and v.get("checker_acceptance") is True,"attestation positive")
    return v
def production(args):
    t192,b192=input_json(args.task192); t198,b198=input_json(args.task198)
    seal_task192(t192); seal_task198(t198)
    require(t192.get("schema")=="d972-r07-normalized-exact-common-word-cached/v3" and t192.get("terminal")=="R07_NORMALIZED_EXACT_CACHED_COLGEN_V3_COMMON_WORD","task192 receipt")
    require(t198.get("schema")=="d972-r07-seven-context-roof-presentation/v1" and t198.get("status")=="COMPLETE" and t198.get("terminal")=="ROOF_BRIDGE_ISOMORPHISM","task198 receipt")
    c=t192.get("exactification",{}).get("literal",{}).get("c_exact"); g=t192.get("g760")
    require(type(g) is list and type(c) is list and t192.get("exact_direct_replay",{}).get("replay",{}).get("corrected_word")==red(g+c),"task192 corrected word")
    replay=t192["exact_direct_replay"]["replay"]; require(replay.get("right_g760_multiplication") is True and replay.get("direct_all_seven_replay") is True,"task192 replay")
    bridge=t198.get("bridge",{}); rows=bridge.get("occurrence_ledger"); check_ledger(rows); require(bridge.get("ten_to_eleven")==[0,1,2,3,0,4,5,6,7,8,9],"insertion")
    require("section_cocycle" in t198.get("evaluator",{}).get("entry_points",{}),"evaluator ABI")
    a192=attest(args.task192_attestation,args.task192,b192,"d972-r07-task192-production-binding/v1"); a198=attest(args.task198_attestation,args.task198,b198,"d972-r07-task198-production-binding/v1")
    pkg=specialize(g,c,rows);pkg["output_guard"]="fresh-output-only";pkg["predecessor_bindings"]={"task192":{"receipt_path":args.task192,"receipt_sha256":hashlib.sha256(b192).hexdigest(),"sidecar_path":args.task192_attestation,"sidecar_sha256":digest(a192)},"task198":{"receipt_path":args.task198,"receipt_sha256":hashlib.sha256(b198).hexdigest(),"sidecar_path":args.task198_attestation,"sidecar_sha256":digest(a198)}};return pkg
def meter(): return {"input_bytes":0,"word_steps":0,"sparse_support":0,"group_operations":0,"mutation_work":0,"checker_work":0,"serialized_bytes":0,"wall_seconds":21600,"rss_bytes":6442450944}
def main(argv=None):
    ap=argparse.ArgumentParser(); ap.add_argument("--selftest",action="store_true"); ap.add_argument("--fixture",default=FIXTURE); ap.add_argument("--task192",default=TASK192); ap.add_argument("--task198",default=TASK198); ap.add_argument("--task192-attestation",default="ci/in/d972_r07_normalized_exact_common_word_cached_v3.attestation"); ap.add_argument("--task198-attestation",default="ci/in/d972_r07_seven_context_roof_presentation_v1.attestation"); ap.add_argument("--output",default="ci/out/d972_r07_actual_two_word_endpoint_specializer_v2.json"); args=ap.parse_args(argv)
    out0=Path(str(args.output)); require(not out0.is_absolute() and ".." not in out0.parts and str(args.output).replace("\\","/")==out0.as_posix() and str(args.output).startswith("ci/out/"),"output path")
    p=ROOT/out0
    if p.exists(): print("D226_PRODUCER_TERMINAL "+UNKNOWN_INPUT); return 0
    budget=Budget()
    try:
        for source in ([args.fixture] if args.selftest else [args.task192,args.task198,args.task192_attestation,args.task198_attestation]):
            candidate=ROOT/Path(source)
            if candidate.exists(): budget.bump("input_bytes",candidate.stat().st_size,"input staging")
        if args.selftest:
            pkg=specialize([1,2,1],[2,2],EXPECTED)
            zero_safe_oracle(); exhaustive_arithmetic_oracle()
            bad,limited=execute_terminal_probes(budget)
            pkg["terminal_probes"]={"input":bad,"resource":limited}
            pkg["output_guard"]="fresh-output-only"
            pkg["predecessor_bindings"]={"task192":{"canary":"task192-selftest-binding"},"task198":{"canary":"task198-selftest-binding"}}
            validate_package(pkg)
            require(pkg["words"]["f"]!=pkg["words"]["g0"] and any(o["rword_g"]!=o["rword_f"] for o in pkg["specialization_v216_abi"]["occurrences"]),"selftest word roles")
            muts=mutation_execution(pkg)
            pkg["mutation_execution"]={"attempted":MUTATIONS,"rejected":muts}
            validate_package(pkg)
            term=SELFTEST; schema=SELF_SCHEMA
            budget.bump("mutation_work",len(MUTATIONS),"selftest mutations")
        else: pkg=production(args); validate_package(pkg); term=COMPLETE; schema=SCHEMA
        budget.bump("word_steps",sum(len(v) for v in pkg.get("specialization_v216_abi",{}).get("literals",{}).get("rword_g",[])),"word evaluation")
        lit=pkg.get("specialization_v216_abi",{}).get("literals",{})
        budget.bump("group_operations",sum(len(v) for v in lit.get("relation_words_g",[]))+sum(len(v) for v in lit.get("relation_words_f",[])),"group replay")
        budget.bump("sparse_support",sum(len(v) for v in lit.get("d_occ",{}).values()),"sparse replay")
        out=envelope(schema,term,pkg,{"boundary_membership":False,"pointed_mu1":False,"exact_pb_endpoint_zero":False,"cofinal_lift":False,"fake":False,"Ihara_witness":False,"resource_meter":budget.output()})
    except FileNotFoundError as e: term=UNKNOWN_INPUT; out=envelope(SCHEMA,term,{"reason":str(e)})
    except ResourceStop as e: term=UNKNOWN_RESOURCE; out=envelope(SCHEMA,term,{"reason":{"phase":e.phase,"cap":e.cap,"value":e.value,"limit":e.limit},"resource_meter":budget.output()})
    except (Stop,KeyError,ValueError,json.JSONDecodeError,UnicodeError,TypeError) as e: term=UNKNOWN_INPUT; out=envelope(SCHEMA,term,{"reason":str(e)})
    except MemoryError as e: term=UNKNOWN_RESOURCE; out=envelope(SCHEMA,term,{"reason":"memory"})
    require(not p.exists(),"stale output refused")
    p.parent.mkdir(parents=True,exist_ok=True); payload=canon(out); budget.bump("serialized_bytes",len(payload),"receipt serialization"); p.write_bytes(payload); print("D226_PRODUCER_TERMINAL "+term); return 0
if __name__=="__main__": raise SystemExit(main())
