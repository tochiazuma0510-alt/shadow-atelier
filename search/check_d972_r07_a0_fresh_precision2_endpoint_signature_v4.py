#!/usr/bin/env python3
"""Independent fail-closed checker for the Task640 endpoint consumer."""
from __future__ import annotations
import argparse, ast, hashlib, json, os, re, struct, sys, tempfile, time, types
from collections import deque
from pathlib import Path
from typing import Any, Iterable, Sequence
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
T601_PRODUCER='ce036c4a1a92d16a78cb8da8c16dee282a6a981889f821e6df82eaecdd8fba0a'
T601_CHECKER='8c3dd039368f63d62ef79694a196f73d0b626134df39673c5e48c98c7c8787f9'
TASK601_MANIFEST_SHA='381f961fc808076c5c0adbc98e32c19742565087bffbcd5f99772533e05d5c22'
DECISION_BODY='62412762b3a208d31febb6c6b8d4707f880471ed32cf62c79c18108065ab7b5d'; DECISION_HEAD='07de7a817e8c5ae2e7346402a290c32631d05b0cc621d03702faa6cb43a948c0'; BASIS_SHA='b562c980c22a25a932bae1b548f72aeede5637b9612afc908fff9a9aecff069d'; REMAINDER_SHA='564cbfafc869a8c6eb761a392caa5e792b546bf577af7fe808177b2fdf13cbb0'
PREPARE_SHA='1f191d88a0453360021ec57d253a7d16c9a66ac059ddaaadb6db3e2b9293c865'
MARKER='R07_FRESH_PRECISION2_ENDPOINT_SIGNATURE_V4_CHECKER_PASS'
RHO2_MARKER='R07_FRESH_PRECISION2_ENDPOINT_SIGNATURE_V4_CANDIDATE'
FLAGS={'direct_occurrence_replay':False,'next_degree2_residual':None,'grade2_MEMBER':False,'grade2_NONMEMBER':False,'A0':False,'ORDER_54432':False,'full_Q0':False,'COMMON':False,'cofinal_lift':False,'FAKE':False,'IHARA':False,'cross_checked':False,'verified':False}
RECEIPT_NAMES={'rho2_packed':'rho2.bin','rho2_dense':'rho2-dense.bin','lower_dense':'lower-dense.bin','target_dense':'target-dense.bin','path_signatures':'path-signatures.json','signature_buckets':'signature-buckets.json','roots':'authenticated-roots.json'}
LOWER,TOP,PACKED=32260,48384,12096
WORDS_SHA='90ba603368307e16b27b2bad9d84847c7bedc501fab811b8919d96e3c8936893'
V484_PROOF_SHA256 = "25e292c8d996000c5dd442619f9afa269d83193ce5f58e4f3536c55b61f77492"
RUNTIME_PROFILE = {
    "profile": "endpoint-minimal-v4",
    "contexts": 31,
    "context_named_uses": 46,
    "fine_source_order": 59049,
    "q0_marked_rows": 2,
    "generic_joint_closure": False,
    "generic_roster": False,
    "base_fox_rows": False,
    "pb3_boundary_rows": False,
    "pb4_boundary_rows": False,
    "generic_target": False,
    "generic_runtime_model": False,
    "v484_proof_sha256": V484_PROOF_SHA256,
    "v12f_sha256": "22d2ebda554cfacc78393dda7f43a9a6550e7f134dd8f44f87ab0f62241bbbbb",
    "task565_prebuild_sha256": "acffa38731a28d85539f765537010e6bf20f55c7f7feae0099d56c58c808ffc8",
    "words_sha256": WORDS_SHA,
    "g760_sha256": "518f09820b8d7baee6b58ebf366cebf7b02a9a945cd1350cf8c701a4e6bc2b4d",
}

TEN=(0,1,2,3,0,4,5,6,7,8,9)
SIGNS=(1,-1,1,-1,-1,1,1,1,1,-1,-1)
PAPER_PINS={'sol/proof_r07_selected_slp_leaf_gated_precision2_join_v470.md':'b56aa15ee87b4831cc999525233cfadbe8e62cd25c0503c0c98fce3106fb2b7a','sol/sol_reply_611_audit_r07_selected_slp_leaf_gated_precision2_join_v1.md':'4212afae131eda13c8d1199bd2a41ad2b232957fd8de2d565fbfe24e34fccd92','sol/proof_r07_endpoint_signature_precision2_consumer_v471.md':'38d271514baf838953b6003f954be60c689771f0fd1c9fec14de1dfc55daf99f','sol/sol_reply_613_audit_r07_endpoint_signature_precision2_consumer_v1.md':'04acf864fd2fd95c13880510feb5087588f3f3970418f47ed44614f5bc74f75b','sol/sol_reply_622_reaudit_r07_task601_packed_memory_release_v3.md':'4eaf1f92f4ef1fdd0a7f3289175d7c8b97c5ac85714b0b368d4aa66a20f151e0'}
PAPER_PINS.update({'sol/sol_reply_627_audit_r07_task623_endpoint_consumer_v2.md':'5ce7efabb36c454c688248249acd47ee9c6e4594039cb872674101e34239538c','sol/sol_reply_630_audit_r07_precision2_actual_context_contract.md':'d64122daa3b6396e494d8309eb98ecadebad2062a173a80fca2ab88baacd7dd1','sol/proof_r07_eleven_endpoint_six_row_restriction_repair_v478.md':'a7e5df7f14d35b7dc971127e187fbc16abe00b3b5190fac341666b94bbf1e72b','sol/sol_reply_636_reaudit_r07_eleven_endpoint_six_row_v478.md':'2cdecfcb47cf6727d45cbc7cf494c84230a5be5af489d6bca306a4df04552c79','sol/sol_reply_639_audit_r07_task625_success_artifact.md':'b48fe4bfb43aedb76c9109e2ca73e7a9de323687c69c64807e74f3ad62db0a1b','sol/proof_r07_first_rung_witness_presentation_dovetail_v479.md':'df6850c9e7c86a83ade26c37064a7deb38ec3c8d7907b1eec6ff0d5268b22986','sol/sol_reply_641_audit_r07_first_rung_dovetail_v479.md':'498df880f86805cffab50756dc32435a2a79a3426071c7bdd290820a6dadddf7','sol/luna_task_643_r07_task640_compositional_parent_amendment.md':'0ae5a1e7724bb878a36d7382ad3f393cdaff486cc036e6fe41a7e565e257bac5','sol/proof_r07_a0_affine_truncated_two_rung_engine_v443.md':'80970217b415d7b764e399b5ce5892075b1f82f7f87f0c6199e9f6b0e404f24c','sol/proof_r07_a0_psl504_occurrence_floor_v437.md':'4671e1f46e5489355b850e7f2c04d73d36d96d7eca1feadde199b56ae273e3d6','sol/proof_r07_a0_relative_fibre_echelon_lift_v441.md':'5cb52ffd02d2cd5c89e08080931065123a7208f7d5a2878acddb5d9ac2958fbb','sol/proof_r07_first_rung_graded_fourier_blocks_v445.md':'98d073c896cae8304252327ea285b876f8868b6c2d00e8ba3c00465ea86612e7','sol/proof_r07_first_rung_character_blocks_coupled_monomials_v446.md':'389ceee1250b892ec4845753af23f4455e619e2d72782931645d8b8176764756','sol/proof_r07_grade1_to_grade2_split_presentation_handoff_repair_v451.md':'3ec2d1351e16bf0fcde3abe8da346b8765b26c30796ff48e415c46ac51d933b4','sol/proof_r07_selected_slp_adjoint_fox_replay_v467.md':'f80a63b2db0efe56777a48d1ddaab61518df9a802884549834e63e517e9a8dc5','sol/proof_r07_canonical_selected_dependency_slp_v468.md':'b1e0f09ae0c6f136804e37bc8db8cba85bccede0880ed5f26afed880d28829a6','sol/proof_r07_canonical_selected_dependency_slp_physical_replay_v469.md':'bae6864e6f00f65bfd3ff18a4c5676d5afe190ad0f2c6ffaf83cd9683d3f26f6','sol/proof_r07_selected_slp_staged_adjoint_repair_v475.md':'757ffab5aa011643efa3df4b133dc03d423895d57a003ed6830a47528388148e'})
LEAF_HEADER=struct.Struct('<8sBBBB32sQ'); LEAF_RECORD=struct.Struct('<IIBI')
SEVEN_PINS={
'old':('search/d972_b345_seedspan_triple4_v1.py',535219,'fe18fc31fdf3f9416ebb829112ccbd514c27e6a8d30fe24691842865277a0b29'),
'joint':('search/d972_b345_joint_kernel_qstar_closure_v1.py',67945,'06ba6cf361957db3e339d48d14b3d4fbc689de9642e3f96273fbe8f3160e76dc'),
'v172':('search/d972_r07_full_e4_joint_orbit_preflight_v7.py',21918,'92701bb1ed84de9b9aa0fb8a986197f76b86e1f42af83ee18319700be0647eed'),
'g760':('search/check_d972_r07_616_to_760_commutator_affine_rhs_v3.py',33409,'f8c7fc7f5b5bbfffa0cf147a59313981c5a4b2c6c00504a9f773029097fdde5f'),
'pb4':('search/d972_b345_target6_dual_colgen_v2.py',444497,'b361dc5e7b025bb7efe3507b145e5480c6c67dfecc2e712134a8d521585e73c7'),
'q3':('ci/b345_157ee_artifacts_32359956713/d972_b345_q3_chief_v1.json',231570,'3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72')}

def require(condition,message):
    if not condition: fail(message)
def sha_obj(value): return sha(json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=True).encode('ascii'))
class _Task640Floor:
    ID9=tuple(range(9)); OO=([1],[2]),([1],[-1,-2]),([2],[-1,-2]),([-2,-1],[1]),([1],[2]),([-2,-1],[2]); psels=[]; psidx={}; qb=None
    @staticmethod
    def M(a,b): return tuple(b[a[i]] for i in range(len(a)))
    @staticmethod
    def inv(a):
        out=[0]*len(a)
        for i,j in enumerate(a): out[j]=i
        return tuple(out)
    @staticmethod
    def wi(word): return [-x for x in reversed(word)]
    def wm(self,*parts):
        out=[]
        for part in parts:
            for letter in part:
                if out and out[-1]==-letter: out.pop()
                else: out.append(letter)
        return out
    def sub(self,word,x,y): return self.wm(*(x if q==1 else y if q==2 else self.wi(x) if q==-1 else self.wi(y) for q in word))
    def qmul(self,left,right): return self.M(left[0],right[0]),left[1]^right[1],left[2]^right[2]
    def qinv(self,value): return self.inv(value[0]),value[1],value[2]
    def qev(self,word,images):
        value=(self.ID9,0,0)
        for q in word: value=self.qmul(value,images[abs(q)-1] if q>0 else self.qinv(images[abs(q)-1]))
        return value
    def group(self,gens,reverse=False):
        steps=(gens[0],gens[1],self.inv(gens[0]),self.inv(gens[1])); steps=tuple(reversed(steps)) if reverse else steps
        elements=[self.ID9]; index={self.ID9:0}; queue=deque([self.ID9])
        while queue:
            value=queue.popleft()
            for generator in steps:
                product=self.M(value,generator)
                if product not in index: index[product]=len(elements); elements.append(product); queue.append(product)
        return elements,index
    @staticmethod
    def exps(word): return sum(1 if x==1 else -1 if x==-1 else 0 for x in word),sum(1 if x==2 else -1 if x==-2 else 0 for x in word)
def cfree(word,width=6):
    out=[]
    for x in map(int,word):
        require(x and abs(x)<=width,'local_word')
        if out and out[-1]==-x: out.pop()
        else: out.append(x)
    return tuple(out)
def cinv(word): return cfree(-x for x in reversed(word))
def cpp(words): return cfree(x for word in reversed(words) for x in word)
def csub(word,images):
    out=()
    for x in word:
        image=tuple(images[abs(int(x))-1]); out=cfree(out+(image if x>0 else cinv(image)))
    return out
def cpairs(rank): return [[i,j] for i in range(1,rank) for j in range(i+1,rank+1)]
def cpindex(rank,pair): return cpairs(rank).index(list(pair))+1
def cartin_step(rank,letter):
    i=abs(letter); images=[[j] for j in range(1,rank+1)]
    if letter>0: images[i-1],images[i]=[i,i+1,-i],[i]
    else: images[i-1],images[i]=[i+1],[-(i+1),i,i+1]
    return images
def cartin_images(rank,braid):
    images=[[j] for j in range(1,rank+1)]
    for x in braid: images=[list(csub(w,cartin_step(rank,x))) for w in images]
    return images
def caij(i,j): return list(range(j-1,i,-1))+[i,i]+[-k for k in range(i+1,j)]
def cpure(rank):
    if rank==2:return []
    old=cpairs(rank-1); rel=[list(csub(w,[[cpindex(rank,p)] for p in old])) for w in cpure(rank-1)]; kernel=[[cpindex(rank,[k,rank])] for k in range(1,rank)]
    for i,j in old:
        gen=cpindex(rank,[i,j]); action=cartin_images(rank-1,caij(i,j))
        for k in range(1,rank):
            h=cpindex(rank,[k,rank]); tail=csub(action[k-1],kernel); rel.append(list(cfree([-gen,h,gen]+list(cinv(tail)))))
    return rel
def pidentity(n): return bytes(range(n))
def pmul(a,b): return bytes(b[a[i]] for i in range(len(a)))
def pinv(a):
    out=[0]*len(a)
    for i,j in enumerate(a): out[j]=i
    return bytes(out)
def prow(row,n):
    v=[int(x) for x in (row.replace(',',' ').split() if isinstance(row,str) else row)]; require(len(v)==n,'perm_width'); out=bytes(x-1 for x in v); require(set(out)==set(range(n)),'perm'); return out
def coordword(row): return tuple(i for i,x in enumerate(row,1) for _ in range(x))
class LocalPc:
    def __init__(self,r):
        self.n=int(r['generator_count']); self.orders=list(map(int,r['relative_orders'])); self.powers=[self.coord(x) for x in r['power_relations']]; self.inverses=[self.coord(x) for x in r['inverses']]; self.conj={(int(x['i']),int(x['j'])):self.coord(x['coords']) for x in r['conjugate_relations']}; require(self.orders==[3]*self.n,'pc_orders')
    def coord(self,row):
        v=[int(x) for x in (row.replace(',',' ').split() if isinstance(row,str) else row)]; require(len(v)==self.n and all(0<=x<3 for x in v),'pc_coord'); return bytes(v)
    def one(self): return bytes(self.n)
    def collect(self,word):
        tok=[]
        for x in word: tok.extend((x,) if x>0 else coordword(self.inverses[-x-1]))
        cap=max(10000,1000*(1+len(tok))*(1+self.n)); steps=0
        while True:
            changed=False
            for p in range(len(tok)-1):
                if tok[p]>tok[p+1]: tok[p:p+2]=[tok[p+1]]+list(coordword(self.conj[(tok[p],tok[p+1])])) ; changed=True; break
            if not changed:
                p=0
                while p<len(tok):
                    e=p
                    while e<len(tok) and tok[e]==tok[p]:e+=1
                    if e-p>=3: tok[p:p+3]=list(coordword(self.powers[tok[p]-1])); changed=True; break
                    p=e
            if not changed: break
            steps+=1; require(steps<=cap,'pc_cap')
        out=[0]*self.n
        for x in tok: out[x-1]+=1
        require(all(x<3 for x in out),'pc_power'); return bytes(out)
    def mul(self,a,b): return self.collect(coordword(a)+coordword(b))
    def inverse(self,a):
        w=[]
        for i in range(self.n,0,-1):
            for _ in range(a[i-1]): w.extend(coordword(self.inverses[i-1]))
        return self.collect(w)
class LocalQ:
    def __init__(self,rank,degree,pc,gens): self.rank,self.degree,self.pc,self.generators=rank,degree,pc,list(gens); self.identity=(pidentity(degree),pc.one()); self.inverse_generators=[self.inverse(x) for x in self.generators]
    def mul(self,a,b): return pmul(a[0],b[0]),self.pc.mul(a[1],b[1])
    def inverse(self,a): return pinv(a[0]),self.pc.inverse(a[1])
    def eval(self,word,images=None):
        marked=self.generators if images is None else images; out=self.identity
        for x in word: out=self.mul(out,marked[abs(x)-1] if x>0 else self.inverse(marked[abs(x)-1]))
        return out
def local_quotients(data):
    p3,p4=LocalPc(data['groups']['PB3']),LocalPc(data['groups']['PB4']); m3=[p3.coord(x['coords']) for x in data['groups']['PB3']['marked_generators']]; m4=[p4.coord(x['coords']) for x in data['groups']['PB4']['marked_generators']]; q0,q4=data['coarse_models']['Q0'],data['coarse_models']['Q4']; a=[prow(x,int(q0['degree'])) for x in q0['marked_permutations']]; b=[prow(x,int(q4['degree'])) for x in q4['marked_permutations']]; z=pinv(pmul(a[1],a[0])); e3=LocalQ(3,int(q0['degree']),p3,[(a[0],m3[0]),(z,m3[1]),(a[1],m3[2])]); e4=LocalQ(4,int(q4['degree']),p4,list(zip(b,m4))); require(all(e3.eval(w)==e3.identity for w in cpure(3)) and all(e4.eval(w)==e4.identity for w in cpure(4)),'local_presentations'); return e3,e4
def cfox(word,q):
    prefix=q.identity; out={}
    for x in word:
        i=abs(x)
        if x<0: prefix=q.mul(prefix,q.inverse_generators[i-1])
        key=(i,prefix); out[key]=(out.get(key,0)+(1 if x>0 else 2))%3
        if not out[key]: del out[key]
        if x>0: prefix=q.mul(prefix,q.generators[i-1])
    return out,prefix
class LocalWords:
    inv_word=staticmethod(lambda w:list(cinv(w))); pp_words=staticmethod(lambda w:list(cpp(w))); f2_substitute=staticmethod(lambda w,x,y:list(csub(w,[x,y]))); embed_f2_pb3=staticmethod(lambda w:list(csub(w,[[1],[3]]))); fox_gradient_without_sections=staticmethod(cfox)
    @staticmethod
    def translate_vector(v,t,q):
        out={}
        for (c,e),a in v.items():
            key=(c,q.mul(t,e)); out[key]=(out.get(key,0)+a)%3
            if not out[key]: del out[key]
        return out
    pure_relations=staticmethod(cpure)
    @staticmethod
    def hexagon_words(f):
        x,y=[1],[2]; z=list(cinv(cpp([x,y]))); u=list(cinv(cpp([y,x]))); sub=lambda a,b:list(csub(f,[a,b])); return [list(cpp([sub(x,y),cinv(sub(x,z)),sub(y,z)])),list(cpp([cinv(sub(u,x)),cinv(sub(x,y)),sub(u,y)]))]
class SevenSources:
    def __init__(self): self.raw={}; self.objects={}
    def authenticate(self):
        for key,(relative,size,digest) in SEVEN_PINS.items():
            raw=(ROOT/relative).read_bytes()
            if len(raw)!=size or sha(raw)!=digest: fail('seven_source:'+key)
            self.raw[key]=raw
    def json(self,key):
        if key not in self.objects: self.objects[key]=json.loads(self.raw[key])
        return self.objects[key]
    @staticmethod
    def public(): return {key:{'path':row[0],'bytes':row[1],'sha256':row[2]} for key,row in SEVEN_PINS.items()}
EXPECTED_FILES={
'grade_edges':('grade-edges.bin',12372120,'aa3a506fd2f1358e6edce102d5fb6f129a4b75bd2675e03bb401f01904e47557'),'grade_nodes':('grade-nodes.bin',146276,'6b79485d9c69a05cf0d6c64788bc4f341792c8cedbb4f00cd1fdc887d42ca82b'),'grade_origins':('grade-origins.bin',30506112,'fcc5e5e43a9923b549e0b894c8ab995e545f78563134f37dae99917026283e68'),'literal_leaves':('literal-leaves.bin',565981,'4a0b631004c9fbbf0b3cc965ff606711e04081c7d79beecb2db6b7be264fc851'),'lower_companions':('lower-companions.bin',10045728,'299ff5f214d32a85bea401705bffe01b2cf4f4f327c50a34f26fed1ba433dcaa'),'lower_edges':('lower-edges.bin',1911741,'b83e05df054d43952640b4442f08fb54aadf3303675dedc5443268aa3c3e9809'),'lower_nodes':('lower-nodes.bin',48169,'4e9b5a98f9b434649d3eeac664fdcdc029d81a1247b193cb3260dabe2c22ee3c'),'lower_origins':('lower-origins.bin',3350237,'1cbbb4444858828d9b3ddb78c799a087c6ada69b058155f02d11e5f63316135c'),'lower_stored':('lower-stored.bin',3350237,'50361df9c85a525e0c3f73a2ef82a337a870b3cb4eb30caad5816df49c98a683'),'old_lower_zero':('old-lower-zero.bin',712001,'f2793fac59ae4cb798f479f764eb494b5db51256fb7d01dfc523000a7b217a33'),'roots':('roots.json',255846,'af1b035e0eb0af6e593770affb52a52905609fd9c19e988b0b7e8cf69e7592c5'),'selected_grade':('selected-grade.bits',631,'e2fd7f3147f4880e42d6da6f211f2ed7991af9d9d1925416ec30120c46ac832a'),'selected_lower':('selected-lower.bits',208,'771af58b72061d7c94ec28c9086c375bf4e1c5b55254cbb11a541fea4093d48e'),'source_ancestry':('source-ancestry.json',149359882,'315f9d9be5c7301b7b54ca5f545a17ca1d491f2d1d24e40f426ce831388f2908'),'source_refs':('source-refs.json',19876945,'18767d10ab9e697c5f9cb54fbdcabfbc1824c0f4e0afde15e0e550e4a3b781ea')}

def sha(data): return hashlib.sha256(data).hexdigest()
def canon(value): return (json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=True)+'\n').encode('ascii')
def fail(reason): raise RuntimeError(reason)
def resource_gate(started):
    if time.monotonic()-started>float(os.environ.get('TASK640_SECONDS','5400')): fail('UNKNOWN_RESOURCE:time')
    try:
        import resource
        if resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024>int(os.environ.get('TASK640_MAX_RSS',str(7*1024**3))): fail('UNKNOWN_RESOURCE:rss')
    except ImportError: pass
def authenticate_paper_pins():
    for name,digest in PAPER_PINS.items():
        path=ROOT/name
        if not path.is_file() or sha(path.read_bytes())!=digest: fail('paper_pin:'+name)
def load_independent_arithmetic():
    return sys.modules[__name__]
def independent_target(module,context,words):
    d0=np.zeros(module.PHYSICAL0,dtype=np.uint8); d1=np.zeros(module.PHYSICAL1,dtype=np.uint8); d2=np.zeros(module.PHYSICAL2,dtype=np.uint8); aux=np.zeros(4,dtype=np.uint8)
    g=tuple(map(int,words['g760'])); f=module.floor
    blocks=(tuple(f.wm(f.sub(g,*f.OO[2]),f.wi(f.sub(g,*f.OO[1])),f.sub(g,*f.OO[0]))),tuple(f.wm(f.sub(g,*f.OO[5]),f.wi(f.sub(g,*f.OO[4])),f.wi(f.sub(g,*f.OO[3])))))
    for block,word in enumerate(blocks):
        normal,augmentation=module.qnorm(word,context); aux[block]=(-augmentation)%3
        for component,value,coefficient in normal:
            polynomial=module.e_poly(value[3]); psl=context.psidx[value[0]]
            for character,label in enumerate(module.CHARACTERS):
                weight=-coefficient*module.cv(label,(value[1],value[2]))
                c0=(((character*2+block)*2+component)*504)+psl; d0[c0]=(int(d0[c0])+weight*int(polynomial[0]))%3
                for mono in range(3):
                    c1=((((character*2+block)*2+component)*3+mono)*504)+psl; d1[c1]=(int(d1[c1])+weight*int(polynomial[1+mono]))%3
                for mono in range(6):
                    c2=((((character*2+block)*2+component)*6+mono)*504)+psl; d2[c2]=(int(d2[c2])+weight*int(polynomial[4+mono]))%3
    return d0,d1,d2,aux
def independent_replay(module,context,words,terms):
    result=(np.zeros(module.PHYSICAL0,dtype=np.uint8),np.zeros(module.PHYSICAL1,dtype=np.uint8),np.zeros(module.PHYSICAL2,dtype=np.uint8),np.zeros(4,dtype=np.uint8))
    seeds=[module.evaluate_seed(context,tuple(map(int,row))) for row in words['relators']]; cache={}
    for seed,path,coefficient in terms:
        exact=tuple(map(int,path)); cache.setdefault(exact,context.word_tags(exact))
        physical=module.aggregate(context,module.act(context,seeds[seed-1],cache[exact]))
        module.add_full(result,physical,coefficient)
    return result
def freely_reduce(word):
    out=[]
    for raw in word:
        letter=int(raw)
        if letter not in (-2,-1,1,2): fail('actor_letter')
        if out and out[-1]==-letter: out.pop()
        else: out.append(letter)
    return tuple(out)
def canonical_terms(value):
    if not isinstance(value,list): fail('terms_shape')
    acc={}
    for item in value:
        if not isinstance(item,list) or len(item)!=3 or type(item[0]) is not int or not 1<=item[0]<=44 or type(item[2]) is not int or item[2] not in (1,2): fail('terms_semantics')
        key=(item[0],freely_reduce(item[1])); acc[key]=(acc.get(key,0)+item[2])%3
    return [[s,list(w),c] for (s,w),c in sorted(acc.items()) if c]
def parse_literal_leaves(raw,ancestry_digest):
    if len(raw)<LEAF_HEADER.size: fail('leaf_header_short')
    magic,version,quotient_specific,common,states_exported,binding,count=LEAF_HEADER.unpack_from(raw)
    if (magic,version,quotient_specific,common,states_exported)!=(b'R07LEAF1',1,1,0,0) or binding.hex()!=ancestry_digest: fail('leaf_header')
    if count>int(os.environ.get('TASK640_RECORD_CAP','100000')): fail('UNKNOWN_RESOURCE:record_cap')
    cursor=LEAF_HEADER.size; previous=None; answer=[]
    for _ in range(count):
        if cursor+LEAF_RECORD.size>len(raw): fail('leaf_record_short')
        payload,seed,coefficient,length=LEAF_RECORD.unpack_from(raw,cursor); cursor+=LEAF_RECORD.size
        if length>int(os.environ.get('TASK640_PATH_LENGTH_CAP','4096')): fail('UNKNOWN_RESOURCE:path_length_cap')
        if payload!=9+length or cursor+length>len(raw) or not 1<=seed<=44 or coefficient not in (1,2): fail('leaf_record')
        path=tuple(struct.unpack_from('<%db'%length,raw,cursor)) if length else (); cursor+=length
        if freely_reduce(path)!=path: fail('leaf_not_reduced')
        key=(seed,path)
        if previous is not None and key<=previous: fail('leaf_order')
        previous=key; answer.append([seed,list(path),coefficient])
    if cursor!=len(raw): fail('leaf_eof')
    return answer
def state_key(item): return (item.get('kind'),tuple(int(x) for x in item.get('ids',[])),tuple(int(x) for x in item.get('prefix',[])))
def char_sign(label,parity): return 1 if ((int(label[0])*int(parity[0])+int(label[1])*int(parity[1]))&1)==0 else 2
def independent_leaf_replay(ancestry):
    states=ancestry.get('derived',{}).get('states'); roots=ancestry.get('roots')
    if not isinstance(states,list) or not isinstance(roots,list): fail('derived_shape')
    table={}
    for state in states:
        key=state_key(state)
        if key in table: fail('derived_duplicate')
        table[key]=state
    pure=(((),(0,0)),((-2,)*9,(0,1)),((-2,-2,1,1,2,1,2,1,1),(1,0)),((-2,-2,-2,-1,-2,-1,-1,-1,-2,-1),(1,1)))
    leaves={}; visits=0
    def emit(seed,word,coefficient):
        key=(int(seed),freely_reduce(word)); value=(leaves.get(key,0)+int(coefficient))%3
        if value: leaves[key]=value
        else: leaves.pop(key,None)
    def walk(edge):
        nonlocal visits
        state=table.get(state_key(edge))
        if state is None: fail('derived_missing')
        visits+=1
        if visits>20000000: fail('UNKNOWN_RESOURCE:derived_edges')
        c=int(edge.get('coefficient',0))%3
        if state.get('kind')=='old':
            node=state.get('source_node',{}); origin=node.get('origin',{}) if isinstance(node,dict) else {}
            if origin.get('kind')=='projected_seed':
                seed=int(state.get('seed_index',origin.get('seed',0))); ref=state.get('source_ref',{}); ch=int(ref.get('character',0)); label=(ch>>1,ch&1)
                for word,parity in pure: emit(seed,tuple(state.get('prefix',[]))+tuple(word),c*char_sign(label,parity))
        for child in state.get('children',[]): walk(child)
    for root in roots: walk(root)
    return [[s,list(w),c] for (s,w),c in sorted(leaves.items())]
def auth_task601(path):
    raw=(path/'manifest.json').read_bytes(); manifest=json.loads(raw)
    if canon(manifest)!=raw or sha(raw)!=TASK601_MANIFEST_SHA or manifest.get('cursor')!=8059: fail('task601_manifest')
    if (manifest.get('lower_offer_count'),manifest.get('grade_offer_count'),manifest.get('lower_rank'),manifest.get('grade_rank'))!=(2014,6398,1661,5044): fail('task601_route')
    for key,expected in {'direct_occurrence_replay':False,'next_degree2_residual':None,'A0':False,'COMMON':False,'FAKE':False,'IHARA':False,'cross_checked':False,'verified':False}.items():
        if key not in manifest or manifest[key] is not expected: fail('task601_claims')
    files=manifest.get('files',{}); loaded={}
    if not isinstance(files,dict) or set(files)!=set(EXPECTED_FILES): fail('task601_files')
    for key,(filename,size,digest) in EXPECTED_FILES.items():
        rec=files[key]
        if rec!={'file':filename,'bytes':size,'sha256':digest}: fail('task601_receipt')
        target=path/filename
        if target.stat().st_size!=size: fail('task601_receipt_size')
        h=hashlib.sha256()
        with target.open('rb') as stream:
            for chunk in iter(lambda:stream.read(1024*1024),b''): h.update(chunk)
        if h.hexdigest()!=digest: fail('task601_receipt_sha')
        if key in ('roots','literal_leaves'): loaded[key]=target.read_bytes()
    if sum(row[1] for row in EXPECTED_FILES.values())!=232502114 or len(raw)+232502114!=232511148: fail('task601_payload_size')
    if manifest.get('roots')!=files.get('roots',{}).get('file'): fail('task601_roots_pointer')
    roots=json.loads(loaded['roots'])
    if canon(roots)!=loaded['roots']: fail('task601_noncanonical')
    rebuilt=parse_literal_leaves(loaded['literal_leaves'],EXPECTED_FILES['source_ancestry'][2])
    root_gate(roots)
    if len(roots.get('C_T',{}).get('children',[]))!=3317 or len(roots.get('C_<1',{}).get('terms',[]))!=2622: fail('complete_root_count')
    for key,expected in {'direct_occurrence_replay':False,'next_degree2_residual':None,'A0':False,'COMMON':False,'FAKE':False,'IHARA':False,'cross_checked':False,'verified':False}.items():
        if key not in roots or roots[key] is not expected: fail('task601_root_claims')
    verdict_raw=(path/'task625-verdict.json').read_bytes(); verdict=json.loads(verdict_raw)
    if len(verdict_raw)!=1120 or sha(verdict_raw)!='a650aa8d5d78f52145fff5ba7769ad2036cfd16e90e3caaf367b4517e07d2740' or canon(verdict)!=verdict_raw or verdict.get('marker')!='R07_GRADE1_SELECTED_SLP_V2_CHECKER_PASS' or verdict.get('cursor')!=8059 or verdict.get('coefficient_count')!=3317: fail('task601_verdict')
    if (path/'task625-replayed-verdict.json').read_bytes()!=verdict_raw: fail('task601_independent_replay')
    return manifest,loaded,roots,rebuilt
def auth_candidate(path,roots):
    head_raw=(path/'decision-v2.HEAD').read_bytes(); head=json.loads(head_raw)
    body_raw=(path/f'decision-v2.{DECISION_BODY}.json').read_bytes(); body=json.loads(body_raw); coefficients=body.get('member_coefficients')
    if sha(head_raw)!=DECISION_HEAD or canon(head)!=head_raw or head.get('body_sha256')!=DECISION_BODY or sha(body_raw)!=DECISION_BODY or canon(body)!=body_raw or body.get('terminal')!='GRADE1_DECISION_MEMBER' or len(coefficients or [])!=3317: fail('candidate')
    expected=[{'type':'GradeNodeRef','pivot':int(p),'coefficient':int(c)} for p,c in coefficients]
    if roots.get('C_T')!={'type':'OrderedProduct','children':expected}: fail('candidate_root_order')
    basis=(path/body['basis_receipt']['file']).read_bytes(); remainder=(path/body['remainder_receipt']['file']).read_bytes()
    if len(basis)!=30506112 or sha(basis)!=BASIS_SHA or len(remainder)!=6048 or sha(remainder)!=REMAINDER_SHA or any(remainder): fail('candidate_equation')
def auth_source_state(path):
    raw=(path/'prepare.HEAD').read_bytes(); value=json.loads(raw)
    if canon(value)!=raw or value.get('body_sha256')!=PREPARE_SHA: fail('state_prepare')
def affine_mul(left,right):
    """Independent marked affine fixture kernel; no producer/floor import."""
    perm=tuple(left[0][right[0][i]] for i in range(len(right[0])))
    return (perm,(left[1]+right[1])%2,(left[2]+right[2])%2,tuple((left[3][i]+right[3][i])%3 for i in range(3)))
def affine_inverse(value):
    inv=[0]*len(value[0])
    for i,j in enumerate(value[0]): inv[j]=i
    return (tuple(inv),value[1],value[2],tuple((-x)%3 for x in value[3]))
def truncated_product(a,b):
    out=[0]*10
    for i,x in enumerate(a):
        for j,y in enumerate(b):
            if i+j<10: out[i+j]=(out[i+j]+int(x)*int(y))%3
    return out
def occurrence_aggregate(rows):
    result=[0]*len(rows[0])
    for row,sign in zip(rows,(1,-1,1,-1,-1,1,1,1,1,-1,-1)):
        for i,value in enumerate(row): result[i]=(result[i]+sign*int(value))%3
    return result
def endpoint_gate(signature_values):
    identity=(tuple(range(4)),0,0,(0,0,0))
    if len(signature_values)!=11 or any(value!=identity for value in signature_values): fail('endpoint_failure')
def claim_gate(value):
    if {key:value.get(key) for key in FLAGS}!=FLAGS: fail('claim_flags')
def exact_parent_gate(value,expected):
    if value!=expected: fail('consumer_parent_binding')
def manifest_header_gate(value):
    if value.get('schema')!='d972.r07.a0.fresh-precision2-endpoint-signature.v4' or value.get('marker')!=RHO2_MARKER: fail('consumer_manifest')
def runtime_profile_gate(value):
    if value != RUNTIME_PROFILE: fail('runtime_profile')
def root_gate(roots):
    if roots.get('C_1')!={'type':'Compose','left':'C_<1','right':'C_T'} or roots.get('C_T',{}).get('type')!='OrderedProduct' or roots.get('C_<1',{}).get('type')!='RegisteredPriorProduct': fail('complete_root')
def raw_seed_gate(raw_terms):
    seeds=sorted({int(row[0]) for row in raw_terms})
    if any(not 1<=seed<=44 for seed in seeds): fail('raw_seed')
    return seeds
def typed_endpoint_gate(values,e3_identity,e4_identity):
    if len(values)!=10: fail('typed_endpoint_width')
    for index,value in enumerate(values):
        if value!=(e3_identity if index<5 else e4_identity): fail('typed_endpoint_identity')
def occurrence_contract_gate(types,coordinates,signs):
    if tuple(types)!=('E3',)*6+('E4',)*5 or tuple(coordinates)!=TEN or tuple(signs)!=SIGNS: fail('occurrence_contract')
def signed_relation(word,sign):
    if sign not in (-1,1): fail('occurrence_sign')
    return list(word) if sign>0 else list(cinv(word))
def signed_base_factor(base,sign,inverse):
    if sign not in (-1,1): fail('base_factor_sign')
    return base if sign>0 else inverse(base)
def occurrence_prefix_gate(specs,blocks,identity,multiply,evaluate):
    prefixes={}
    for block in blocks:
        prefix=identity(block); indices=[i for i,spec in enumerate(specs) if spec['block']==block]
        for index in reversed(indices):
            prefixes[index]=prefix; prefix=multiply(block,prefix,evaluate(block,specs[index]['base_factor']))
        block_product_gate(prefix,identity(block))
    out=[]
    for index,spec in enumerate(specs):
        prefix=prefixes[index]
        out.append(multiply(spec['block'],prefix,evaluate(spec['block'],spec['base_factor'])) if spec['sign']>0 else prefix)
    return out
def signature_extend_gate(parent,atom,multiply):
    if len(parent)!=11 or len(atom)!=11: fail('signature_width')
    if any(left[0]!=right[0] for left,right in zip(parent,atom)): fail('signature_type')
    return tuple((left[0],multiply(index,left[1],right[1])) for index,(left,right) in enumerate(zip(parent,atom)))
def signature_bucket_gate(complete,signatures):
    out={}
    for seed,path,coefficient in complete:
        key=(seed,signatures[tuple(path)]); old=out.get(key,(0,tuple(path))); out[key]=((old[0]+coefficient)%3,tuple(path))
    return {key:value for key,value in out.items() if value[0]}
def signature_recurrence_gate(calculated,direct):
    if calculated!=direct: fail('independent_trie_right_recurrence')
def direct_occurrence_gate(direct,occurrence):
    if direct!=occurrence: fail('checker all eleven/direct equality')
def block_product_gate(value,identity):
    if value!=identity: fail('checker base prefix identity')
def exact_receipt_gate(receipts,expected_bytes):
    expected={key:{'file':RECEIPT_NAMES[key],'bytes':len(expected_bytes[key]),'sha256':sha(expected_bytes[key])} for key in RECEIPT_NAMES}
    if receipts!=expected: fail('consumer_receipt_exact')
def dense_result_gate(blobs,target,lower,top,packed,module):
    if np.any(lower) or blobs['lower_dense']!=lower.tobytes(): fail('lower_coordinates')
    if blobs['target_dense']!=target or blobs['rho2_dense']!=top.tobytes() or blobs['rho2_packed']!=packed: fail('dense_coordinates')
    if not np.array_equal(module.unpack(np.frombuffer(packed,dtype=np.uint8),TOP),top): fail('rho2_packing')
def fixture_rejects():
    cases=[]
    def reject(fn):
        try: fn()
        except RuntimeError: cases.append(1)
        else: fail('fixture_mutation_accepted')
    parent={'task601_run':'1','task601_artifact_id':7,'task601_artifact_digest':'sha256:x'}; exact_parent_gate(parent,dict(parent)); reject(lambda:exact_parent_gate({**parent,'task601_run':1},parent)); reject(lambda:exact_parent_gate({**parent,'task601_artifact_digest':'sha256:y'},parent))
    header={'schema':'d972.r07.a0.fresh-precision2-endpoint-signature.v4','marker':RHO2_MARKER}; manifest_header_gate(header); reject(lambda:manifest_header_gate({**header,'schema':'mutated'})); reject(lambda:manifest_header_gate({**header,'marker':'mutated'}))
    runtime_profile_gate(dict(RUNTIME_PROFILE))
    bad_profile = dict(RUNTIME_PROFILE); bad_profile['contexts'] = 30
    reject(lambda: runtime_profile_gate(bad_profile))
    claim_gate(dict(FLAGS))
    for key in FLAGS:
        bad={**FLAGS}; bad[key]=([] if key=='next_degree2_residual' else True)
        reject(lambda bad=bad: claim_gate(bad))
    roots={'C_1':{'type':'Compose','left':'C_<1','right':'C_T'},'C_T':{'type':'OrderedProduct'},'C_<1':{'type':'RegisteredPriorProduct'}}; root_gate(roots)
    reject(lambda:root_gate({**roots,'C_1':{'type':'Compose','left':'C_T','right':'C_<1'}})); reject(lambda:root_gate({k:v for k,v in roots.items() if k!='C_T'}))
    if raw_seed_gate([[1,[],1],[2,[],1],[2,[],2]])!=[1,2]: fail('raw_seed_fixture')
    reject(lambda:raw_seed_gate([[45,[],1]]))
    e3,e4=b'E3',b'E4'; typed_endpoint_gate([e3]*5+[e4]*5,e3,e4)
    reject(lambda:typed_endpoint_gate([e3]*4+[e4]+[e4]*5,e3,e4)); reject(lambda:typed_endpoint_gate([e3]*5+[e3]+[e4]*4,e3,e4))
    occurrence_contract_gate(['E3']*6+['E4']*5,TEN,SIGNS)
    reject(lambda:occurrence_contract_gate(['E4']+['E3']*5+['E4']*5,TEN,SIGNS)); reject(lambda:occurrence_contract_gate(['E3']*6+['E4']*5,(4,)+TEN[1:],SIGNS)); reject(lambda:occurrence_contract_gate(['E3']*6+['E4']*5,TEN,(SIGNS[4],)+SIGNS[1:4]+(SIGNS[0],)+SIGNS[5:]))
    if signed_relation([1,2],SIGNS[0])!=[1,2] or signed_relation([1,2],SIGNS[4])!=[-2,-1]: fail('signed_relation_fixture')
    reject(lambda:signed_relation([1],0))
    cycle=bytes((1,2,0)); fixed_inverse=bytes((2,0,1))
    if signed_base_factor(cycle,-1,pinv)!=fixed_inverse or signed_base_factor(cycle,1,pinv)!=cycle: fail('signed_base_inverse_choice')
    reject(lambda:signed_base_factor(cycle,0,pinv))
    ident=bytes((0,1,2)); a=bytes((1,0,2)); b=bytes((0,2,1)); c=bytes((2,0,1)); tiny=[{'block':1,'base_factor':a,'sign':1},{'block':1,'base_factor':b,'sign':-1},{'block':1,'base_factor':c,'sign':1}]
    prefixes=occurrence_prefix_gate(tiny,(1,),lambda _b:ident,lambda _b,x,y:pmul(x,y),lambda _b,x:x)
    if prefixes!=[ident,c,c]: fail('occurrence_prefix_order')
    parent_sig=tuple([('E3',b'a')]*6+[('E4',b'a')]*5); atom=tuple([('E3',b'b')]*6+[('E4',b'b')]*5)
    good=signature_extend_gate(parent_sig,atom,lambda _i,a,b:a+b)
    reject(lambda:signature_recurrence_gate(signature_extend_gate(parent_sig,atom,lambda _i,a,b:b+a),good))
    reject(lambda:signature_extend_gate(parent_sig[:-1]+(('E3',b'a'),),atom,lambda _i,a,b:a+b))
    sigs={():parent_sig,(1,):good,(2,):good}; grouped=signature_bucket_gate([[1,[1],1],[1,[2],1]],sigs)
    if len(grouped)!=1: fail('full_signature_grouping')
    split=good[:-1]+(('E4',b'c'),); split_buckets=signature_bucket_gate([[1,[1],1],[1,[2],1]],{(1,):good,(2,):split})
    if len(split_buckets)!=2: fail('premature_signature_merge')
    reject(lambda:block_product_gate(b'nonidentity',b'identity')); direct_occurrence_gate({b'x':1},{b'x':1}); reject(lambda:direct_occurrence_gate({b'x':1},{b'x':2}))
    if list(cinv([1,2]))!=[-2,-1] or list(cpp([[1],[2]]))!=[2,1] or list(csub([1],[[2],[1]]))!=[2]: fail('word_order_fixture')
    expected_bytes={key:(key.encode('ascii')) for key in RECEIPT_NAMES}; receipts={key:{'file':RECEIPT_NAMES[key],'bytes':len(data),'sha256':sha(data)} for key,data in expected_bytes.items()}; exact_receipt_gate(receipts,expected_bytes)
    for field,value in (('file','renamed.bin'),('bytes',999),('sha256','0'*64)):
        bad={key:dict(row) for key,row in receipts.items()}; bad['rho2_packed'][field]=value; reject(lambda bad=bad:exact_receipt_gate(bad,expected_bytes))
    module=load_independent_arithmetic(); top=np.zeros(TOP,dtype=np.uint8); lower=np.zeros(LOWER,dtype=np.uint8); packed=module.pack(top); target=b'target'; blobs={'target_dense':target,'lower_dense':lower.tobytes(),'rho2_dense':top.tobytes(),'rho2_packed':packed}; dense_result_gate(blobs,target,lower,top,packed,module)
    for key in tuple(blobs):
        bad=dict(blobs); bad[key]=bytes([1])+bad[key][1:]; reject(lambda bad=bad:dense_result_gate(bad,target,lower,top,packed,module))
    bad_top=top.copy(); bad_top[0]=1; bad_packed=packed
    roundtrip_blobs={'target_dense':target,'lower_dense':lower.tobytes(),'rho2_dense':bad_top.tobytes(),'rho2_packed':bad_packed}
    reject(lambda:dense_result_gate(roundtrip_blobs,target,lower,bad_top,bad_packed,module))
    return len(cases)
def validate_payload(payload,task601,roots,leaves):
    started=time.monotonic()
    raw=(payload/'manifest.json').read_bytes(); manifest=json.loads(raw)
    if canon(manifest)!=raw: fail('consumer_manifest_canonical')
    manifest_header_gate(manifest)
    claim_gate(manifest)
    runtime_profile_gate(manifest.get('runtime_profile'))
    parent=manifest.get('parent',{}); ifsha=sha((task601/'manifest.json').read_bytes())
    expected_parent={'task601_run':'33734643746','task601_attempt':'1','task601_head':'b401d724bbdbef8cf67e96def22fc51c014ab546','task601_job':100582244001,'task601_job_name':'selected-slp','task601_artifact':'task625-grade1-selected-slp-staged-v3-33734643746-1','task601_artifact_id':9885925239,'task601_artifact_bytes':50793121,'task601_artifact_digest':'sha256:ac3121f3bc1a7e2a6c267f20352e953b7343f9085015dd74e4a67e4b90129a75','task601_manifest_sha256':ifsha,'task601_producer_sha256':T601_PRODUCER,'task601_checker_sha256':T601_CHECKER,'task601_replayed_verdict_sha256':'a650aa8d5d78f52145fff5ba7769ad2036cfd16e90e3caaf367b4517e07d2740','source_run':'33677346616','candidate_run':'33707397894','decision_sha256':DECISION_BODY,'basis_sha256':BASIS_SHA,'remainder_sha256':REMAINDER_SHA}
    exact_parent_gate(parent,expected_parent)
    if manifest.get('source_ancestry_sha256') is None or manifest.get('roots_sha256') is None: fail('consumer_receipt_binding')
    expected=set(RECEIPT_NAMES); files=manifest.get('files',{})
    if set(files)!=expected: fail('consumer_receipt_set')
    blobs={}
    for key,rec in files.items():
        if not isinstance(rec,dict) or set(rec)!={'file','bytes','sha256'} or rec['file']!=RECEIPT_NAMES[key]: fail('consumer_receipt')
        data=(payload/rec['file']).read_bytes()
        if len(data)!=rec['bytes'] or sha(data)!=rec['sha256']: fail('consumer_receipt_sha')
        blobs[key]=data
    if blobs['roots']!=(task601/'roots.json').read_bytes(): fail('consumer_roots')
    words_path=ROOT/'scratchpad/a0_paper_words_v1.json'
    if sha(words_path.read_bytes())!=WORDS_SHA: fail('words_sha256')
    module=load_independent_arithmetic(); words=json.loads(words_path.read_text(encoding='utf-8')); context=module.Context(words)
    raw_terms=roots['C_<1']['terms']+leaves
    reached=raw_seed_gate(raw_terms)
    complete=canonical_terms(raw_terms)
    sources=SevenSources(); sources.authenticate(); seven=build_checker_light(sources); model=seven['model']
    if tuple(context.aggregate_table)!=((0,0,1),(1,0,2),(2,0,1),(3,1,2),(4,1,2),(5,1,1)): fail('independent_first_six_table')
    occurrence_contract_gate(tuple('E3' if spec['block'] in (1,2) else 'E4' for spec in model.specs),TEN,tuple(spec['sign'] for spec in model.specs))
    for seed in reached:
        coordinates=model.coordinates(tuple(map(int,words['relators'][seed-1])))
        typed_endpoint_gate(coordinates,blob(seven,seven['e3'].identity),blob(seven,seven['e4'].identity))
        resource_gate(started)
    paths=sorted({tuple(path) for _seed,path,_coefficient in complete})
    if len(paths)>int(os.environ.get('TASK640_PATH_CAP','2000000')): fail('UNKNOWN_RESOURCE:path_cap')
    prefixes={()}
    for path in paths:
        prefixes.update(path[:n] for n in range(1,len(path)+1))
        if len(prefixes)>int(os.environ.get('TASK640_TRIE_CAP','2000000')): fail('UNKNOWN_RESOURCE:trie_cap')
    def direct_signature(path):
        coordinates=model.coordinates(path); return tuple(('E3' if j<6 else 'E4',coordinates[tag]) for j,tag in enumerate(TEN))
    signatures={():direct_signature(())}
    for path in sorted(prefixes,key=lambda value:(len(value),value)):
        if not path: continue
        atom=direct_signature((path[-1],)); parent=signatures[path[:-1]]
        def multiply(index,left_raw,right_raw):
            block=1 if index<6 else 3; quotient=group_for(seven,block)
            return blob(seven,quotient.mul(unpack_element(seven,left_raw,block),unpack_element(seven,right_raw,block)))
        signatures[path]=signature_extend_gate(parent,atom,multiply)
        signature_recurrence_gate(signatures[path],direct_signature(path))
    path_rows=[[list(path),[[kind,raw.hex()] for kind,raw in signatures[path]]] for path in sorted(signatures)]
    if blobs['path_signatures']!=canon(path_rows): fail('independent_path_signatures')
    for index,(seed,path,_coefficient) in enumerate(complete):
        model.direct_column(path,tuple(map(int,words['relators'][seed-1])))
        if index%64==0: resource_gate(started)
    buckets=signature_bucket_gate(complete,signatures)
    bucket_rows=[[seed,[[kind,raw.hex()] for kind,raw in sig],coefficient,list(path)] for (seed,sig),(coefficient,path) in sorted(buckets.items(),key=lambda row:(row[0][0],repr(row[0][1])))]
    if blobs['signature_buckets']!=canon(bucket_rows): fail('independent_signature_buckets')
    if len(complete)+len(signatures)+len(buckets)>int(os.environ.get('TASK640_STATE_CAP','50000000')): fail('UNKNOWN_RESOURCE:state_cap')
    bucket_terms=[[seed,list(path),coefficient] for (seed,_signature),(coefficient,path) in buckets.items()]
    replay=independent_replay(module,context,words,bucket_terms); target=independent_target(module,context,words)
    difference=tuple(((a.astype(np.int16)-b.astype(np.int16))%3).astype(np.uint8) for a,b in zip(target,replay)); lower=np.concatenate((difference[0],difference[1],difference[3])); top=difference[2]
    if lower.size!=LOWER: fail('lower_width')
    target_dense=np.concatenate(target).astype(np.uint8).tobytes()
    packed=module.pack(top)
    if len(packed)!=PACKED: fail('rho2_width')
    dense_result_gate(blobs,target_dense,lower,top,packed,module)
    sparse=[[int(index),int(top[index])] for index in np.flatnonzero(top)]; rho=manifest.get('rho2',{})
    if rho!={'support':len(sparse),'sparse_sha256':sha(canon(sparse)),'dense_sha256':sha(top.tobytes()),'packed_sha256':sha(packed),'packing_roundtrip':True}: fail('rho2_manifest')
    expected_keys={'schema','marker','parent','root','source_ancestry_sha256','roots_sha256','occurrence','compression','dimensions','rho2','files','degree1_task625_physical_replay','degree1_task595_member_equation_zero','member_coefficient_count','lower_all_zero','runtime_profile',*FLAGS}
    if set(manifest)!=expected_keys: fail('consumer_manifest_keys')
    if manifest['root']!='Compose(C_<1,C_T)' or manifest['source_ancestry_sha256']!=EXPECTED_FILES['source_ancestry'][2] or manifest['roots_sha256']!=sha(blobs['roots']): fail('consumer_root_binding')
    expected_occurrence={'count':11,'types':['E3']*6+['E4']*5,'coordinates':list(TEN),'signs':list(SIGNS),'base_checks':len(reached)*11,'max_base_checks':484,'all_seven_canary':True,'first_six_typed_restriction':True}
    occurrence_contract_gate(manifest.get('occurrence',{}).get('types',()),manifest.get('occurrence',{}).get('coordinates',()),manifest.get('occurrence',{}).get('signs',()))
    if manifest['occurrence']!=expected_occurrence: fail('consumer_occurrence')
    expected_compression={'L':len(complete),'U':len(signatures),'G':len(buckets),'G_le_L':len(buckets)<=len(complete),'seed_cache_count':44}
    if manifest['compression']!=expected_compression: fail('consumer_compression')
    if manifest['dimensions']!={'lower':LOWER,'top':TOP,'packed_rho2':PACKED}: fail('consumer_dimensions')
    if manifest['degree1_task625_physical_replay'] is not True or manifest['degree1_task595_member_equation_zero'] is not True or manifest['member_coefficient_count']!=3317 or manifest['lower_all_zero'] is not True: fail('consumer_degree1_gates')
    exact_receipt_gate(files,{'rho2_packed':packed,'rho2_dense':top.tobytes(),'lower_dense':lower.tobytes(),'target_dense':target_dense,'path_signatures':canon(path_rows),'signature_buckets':canon(bucket_rows),'roots':blobs['roots']})
    return manifest,blobs
def selftest():
    identity=(tuple(range(4)),0,0,(0,0,0)); x=( (1,0,3,2),1,0,(1,0,0)); xi=affine_inverse(x)
    if affine_mul(x,identity)!=x or affine_mul(x,xi)[1:]!=(0,0,(0,0,0)): fail('fixture_side_inverse')
    if (2*2)%3!=1 or truncated_product([1,2,0,0,0,0,0,0,0,0],[1,1,0,0,0,0,0,0,0,0])[1]!=0: fail('fixture_coefficient_two')
    rows=[[1,0]]+[[0,0]]*10
    if occurrence_aggregate(rows)!=[1,0]: fail('fixture_occurrence_order')
    mutations=fixture_rejects(); digest='22'*32; good=LEAF_HEADER.pack(b'R07LEAF1',1,1,0,0,bytes.fromhex(digest),1)+LEAF_RECORD.pack(10,1,1,1)+struct.pack('<b',-2)
    if parse_literal_leaves(good,digest)!=[[1,[-2],1]]: fail('fixture_leaf_live')
    for bad in (good[:-1],good+bytes(1),b'X'+good[1:]):
        try: parse_literal_leaves(bad,digest)
        except RuntimeError: mutations+=1
        else: fail('fixture_leaf_mutation')
    try: parse_literal_leaves(good,'33'*32)
    except RuntimeError: mutations+=1
    else: fail('fixture_ancestry_binding_mutation')
    print(json.dumps({'fixture':'PASS','actor_multiplication':'PASS','inverse_action':'PASS','coefficient_2':'PASS','occurrence_components':11,'endpoint_ceiling':484,'rho2_bytes':PACKED,'mutation_count':mutations},sort_keys=True))
"""Independent checker for Task565's grade-two module prebuild.

This file does not import the producer.  It implements its own canonical
state reader, base-3 packing, degree-two polynomial arithmetic, affine actor
and legal-projector replay.  The public checker accepts only the target-
independent MODULE_READY terminal; it never decides membership.
"""

import argparse
import ast
import hashlib
import json
import re
import tempfile
import time
from pathlib import Path
from typing import Any, Iterable

import numpy as np

floor = _Task640Floor()


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "d972.r07.a0.first-rung-grade2-prebuild.v1"
STATE_SCHEMA = SCHEMA + ".state"
GRADE1_STATE_SCHEMA = "d972.r07.a0.first-rung-grade1.v3.state"
CHARACTERS = ((0, 0), (0, 1), (1, 0), (1, 1))
ACTORS = (1, -1, 2, -2)
PURE_WORDS = {
    (0, 0): (),
    (0, 1): (-2, -2, -2, -2, -2, -2, -2, -2, -2),
    (1, 0): (-2, -2, 1, 1, 2, 1, 2, 1, 1),
    (1, 1): (-2, -2, -2, -1, -2, -1, -1, -1, -2, -1),
}
MONOMIALS = (
    (0, 0, 0),
    (1, 0, 0), (0, 1, 0), (0, 0, 1),
    (2, 0, 0), (1, 1, 0), (1, 0, 1),
    (0, 2, 0), (0, 1, 1), (0, 0, 2),
)
DEGREE2_MONOMIALS = MONOMIALS[4:]
MONOMIAL_INDEX = {value: index for index, value in enumerate(MONOMIALS)}
ETA = ((0, 1), (1, 0), (1, 1))
SOURCE0C = 6048
SOURCE1C = 18144
SOURCE2C = 36288
SOURCE0 = 24192
SOURCE1 = 72576
SOURCE2 = 145152
SOURCE_P1 = 96776
PHYSICAL0 = 8064
PHYSICAL1 = 24192
PHYSICAL2 = 48384
PHYSICAL_LOWER = 32260
PACK_ENCODING = "base3-four-trits-per-byte"

PREBUILD_PINS = {
    "sol/proof_r07_grade1_to_grade2_split_presentation_handoff_v450.md": "48acc55a73aba140aa73098791d73f936f1b46fc5316d6f56e668be242fdc630",
    "sol/luna_task_565_r07_a0_first_rung_grade2_prebuild_v1.md": "0c0c32831a5fbd055ba158b8f6b1c429aa51a4cdfe1d781e912a2eba016ebef3",
    "sol/proof_r07_first_rung_six_grade_character_schedule_v448.md": "168e3fc5ab38520faf8ed5d107013f1f8b53f22d2907032519b86b6e0f01182d",
    "sol/proof_r07_grade1_to_grade2_split_presentation_handoff_repair_v451.md": "3ec2d1351e16bf0fcde3abe8da346b8765b26c30796ff48e415c46ac51d933b4",
    "sol/sol_reply_566_audit_r07_grade1_to_grade2_handoff_v1.md": "b8c04819a27906cfaa88534627c147307e1fb7b9429e1f1246fc518b72f2297a",
}


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True) + "\n").encode("ascii")


def plain_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def add(destination: np.ndarray, source: np.ndarray, scalar: int = 1) -> None:
    scalar %= 3
    if scalar:
        destination[:] = (destination.astype(np.uint16) + scalar * source.astype(np.uint16)) % 3


def claim_flags() -> dict[str, bool]:
    return {
        "ORDER_54432": False, "FULL_Q0": False, "A0": False,
        "COMMON": False, "COFINAL_LIFT": False, "FAKE": False,
        "IHARA": False, "verified": False,
    }


def dimensions() -> dict[str, Any]:
    return {
        "characters": 4,
        "character_labels": [list(value) for value in CHARACTERS],
        "degree2_monomials": [list(value) for value in DEGREE2_MONOMIALS],
        "monomials_coupled": True,
        "source_degree0": SOURCE0,
        "source_degree1": SOURCE1,
        "source_degree2_per_character": SOURCE2C,
        "source_degree2_total": SOURCE2,
        "source_precision1_with_auxiliary": SOURCE_P1,
        "physical_degree0": PHYSICAL0,
        "physical_degree1": PHYSICAL1,
        "physical_lower_with_auxiliary": PHYSICAL_LOWER,
        "physical_degree2": PHYSICAL2,
        "packed_degree2_residual_bytes": 12096,
    }


def read_state(
    state_dir: Path, stem: str, parent: str | None, schema: str = STATE_SCHEMA
) -> tuple[dict[str, Any], str]:
    head_bytes = (state_dir / f"{stem}.HEAD").read_bytes()
    head = json.loads(head_bytes)
    if (
        canonical(head) != head_bytes
        or set(head) != {"schema", "stem", "body_sha256", "parent_sha256"}
        or head.get("schema") != schema + ".head"
        or head.get("stem") != stem
        or head.get("parent_sha256") != parent
        or re.fullmatch(r"[0-9a-f]{64}", head.get("body_sha256", "")) is None
    ):
        raise RuntimeError(f"head:{stem}")
    digest = head["body_sha256"]
    data = (state_dir / f"{stem}.{digest}.json").read_bytes()
    if sha(data) != digest:
        raise RuntimeError(f"body_hash:{stem}")
    body = json.loads(data)
    if canonical(body) != data or body.get("schema") != schema:
        raise RuntimeError(f"body_canonical:{stem}")
    return body, digest


def read_blob(state_dir: Path, receipt: Any, rows: int, width: int) -> Path:
    if not plain_int(rows) or not plain_int(width) or rows < 0 or width <= 0 or width % 4:
        raise RuntimeError("blob_expected_shape")
    expected = rows * (width // 4)
    if not isinstance(receipt, dict) or set(receipt) != {"file", "bytes", "sha256", "rows", "width", "encoding"}:
        raise RuntimeError("blob_receipt")
    name = receipt.get("file")
    digest = receipt.get("sha256")
    if (
        not isinstance(name, str) or Path(name).name != name
        or re.fullmatch(r"[0-9a-f]{64}", digest or "") is None
        or not name.endswith(f".{digest}.bin")
        or receipt.get("bytes") != expected
        or receipt.get("rows") != rows
        or receipt.get("width") != width
        or receipt.get("encoding") != PACK_ENCODING
    ):
        raise RuntimeError("blob_semantics")
    path = state_dir / name
    before = path.stat()
    if before.st_size != expected:
        raise RuntimeError("blob_size")
    hasher = hashlib.sha256()
    with path.open("rb") as stream:
        while True:
            chunk = stream.read(1024 * 1024)
            if not chunk:
                break
            hasher.update(chunk)
    after = path.stat()
    if (
        hasher.hexdigest() != digest
        or before.st_size != after.st_size or before.st_mtime_ns != after.st_mtime_ns
    ):
        raise RuntimeError("blob_authentication")
    return path


TRIT_DECODE = np.asarray(
    [[(value // (3 ** position)) % 3 for position in range(4)] for value in range(81)],
    dtype=np.uint8,
)
TRIT_WEIGHTS = np.asarray((1, 3, 9, 27), dtype=np.uint16)


def unpack(data: np.ndarray, width: int) -> np.ndarray:
    packed = np.asarray(data, dtype=np.uint8).reshape(-1)
    if packed.size * 4 != width or np.any(packed > 80):
        raise RuntimeError("packed_row")
    return TRIT_DECODE[packed].reshape(-1).copy()


def pack(row: np.ndarray) -> bytes:
    flat = np.asarray(row, dtype=np.uint8).reshape(-1)
    if flat.size % 4 or np.any(flat > 2):
        raise RuntimeError("dense_row")
    return np.sum(flat.reshape(-1, 4).astype(np.uint16) * TRIT_WEIGHTS, axis=1).astype(np.uint8).tobytes()


def matrix(data: bytes, rows: int, width: int) -> list[np.ndarray]:
    packed = np.frombuffer(data, dtype=np.uint8).reshape(rows, width // 4)
    return [unpack(packed[index], width) for index in range(rows)]


def cv(label: tuple[int, int], parity: tuple[int, int]) -> int:
    return 1 if ((label[0] * parity[0] + label[1] * parity[1]) & 1) == 0 else 2


def sign_kernel(parity: tuple[int, int], value: tuple[int, int, int]) -> tuple[int, int, int]:
    return tuple((cv(ETA[index], parity) * value[index]) % 3 for index in range(3))  # type: ignore[return-value]


Affine = tuple[tuple[int, ...], int, int, tuple[int, int, int]]


def affine_mul(left: Affine, right: Affine) -> Affine:
    acted = sign_kernel((right[1], right[2]), left[3])
    return (
        floor.M(left[0], right[0]), left[1] ^ right[1], left[2] ^ right[2],
        tuple((acted[index] + right[3][index]) % 3 for index in range(3)),
    )  # type: ignore[return-value]


def affine_inv(value: Affine) -> Affine:
    acted = sign_kernel((value[1], value[2]), value[3])
    return floor.inv(value[0]), value[1], value[2], tuple((-entry) % 3 for entry in acted)  # type: ignore[return-value]


def affine_eval(word: Iterable[int], images: tuple[Affine, Affine]) -> Affine:
    result: Affine = (floor.ID9, 0, 0, (0, 0, 0))
    inverses = affine_inv(images[0]), affine_inv(images[1])
    for letter in word:
        result = affine_mul(result, images[abs(letter) - 1] if letter > 0 else inverses[abs(letter) - 1])
    return result


def affine_fox(word: Iterable[int], images: tuple[Affine, Affine]) -> tuple[dict[tuple[int, Affine], int], Affine]:
    output: dict[tuple[int, Affine], int] = {}
    prefix: Affine = (floor.ID9, 0, 0, (0, 0, 0))
    inverses = affine_inv(images[0]), affine_inv(images[1])
    for letter in word:
        generator = abs(letter) - 1
        if letter > 0:
            key = generator, prefix
            output[key] = (output.get(key, 0) + 1) % 3
            prefix = affine_mul(prefix, images[generator])
        else:
            prefix = affine_mul(prefix, inverses[generator])
            key = generator, prefix
            output[key] = (output.get(key, 0) - 1) % 3
        if output.get(key) == 0:
            output.pop(key, None)
    return output, prefix


def matrix2_mul(left: tuple[tuple[int, int], tuple[int, int]], right: tuple[tuple[int, int], tuple[int, int]]) -> tuple[tuple[int, int], tuple[int, int]]:
    return (
        (left[0][0] * right[0][0] ^ left[0][1] * right[1][0], left[0][0] * right[0][1] ^ left[0][1] * right[1][1]),
        (left[1][0] * right[0][0] ^ left[1][1] * right[1][0], left[1][0] * right[0][1] ^ left[1][1] * right[1][1]),
    )


class Context:
    def __init__(self, words: dict[str, Any]):
        text = (ROOT / "scratchpad/fuda1_a0_rmax_data.g").read_text(encoding="utf-8")
        match = re.search(r"FUDA1_Q0PERMS\s*:=\s*\[\s*(\[.*?\])\s*,\s*(\[.*?\])\s*\]\s*;;", text, re.S)
        if match is None:
            raise RuntimeError("marking")
        q36 = tuple(tuple(value - 1 for value in ast.literal_eval(match.group(index))) for index in (1, 2))
        self.a, self.c = q36[0][:9], q36[1][:9]
        self.psels, self.psidx = floor.group((self.a, self.c))
        if len(self.psels) != 504:
            raise RuntimeError("psl_order")
        floor.psels, floor.psidx = self.psels, self.psidx
        self.q1_images = ((self.a, 1, 0), (self.c, 0, 1))
        floor.qb = floor.qinv(floor.qmul(self.q1_images[1], self.q1_images[0]))
        self.images: tuple[Affine, Affine] = (
            (self.a, 1, 0, (1, 0, 0)),
            (self.c, 0, 1, (1, 1, 1)),
        )
        self.pb3_b = affine_inv(affine_mul(self.images[1], self.images[0]))
        self.transport: list[dict[tuple[int, int], tuple[int, int]]] = []
        for left_word, right_word in floor.OO:
            left = floor.qev(left_word, self.q1_images)
            right = floor.qev(right_word, self.q1_images)
            action = ((left[1], right[1]), (left[2], right[2]))
            inverse = None
            for aa in range(2):
                for ab in range(2):
                    for ba in range(2):
                        for bb in range(2):
                            candidate = ((aa, ab), (ba, bb))
                            if matrix2_mul(action, candidate) == ((1, 0), (0, 1)) and matrix2_mul(candidate, action) == ((1, 0), (0, 1)):
                                inverse = candidate
            if inverse is None:
                raise RuntimeError("transport")
            self.transport.append({
                label: (
                    label[0] * inverse[0][0] ^ label[1] * inverse[1][0],
                    label[0] * inverse[0][1] ^ label[1] * inverse[1][1],
                ) for label in CHARACTERS
            })
        self.actor_tags = {
            letter: tuple(affine_eval(floor.sub((letter,), *pair), self.images) for pair in floor.OO)
            for letter in ACTORS
        }
        self.pure_tags = {
            parity: tuple(affine_eval(floor.sub(PURE_WORDS[parity], *pair), self.images) for pair in floor.OO)
            for parity in CHARACTERS
        }
        g760 = tuple(int(value) for value in words["g760"])
        tags = tuple(affine_eval(floor.sub(g760, *pair), self.images) for pair in floor.OO)
        self.shifts = (
            (floor.ID9, 0, 0, (0, 0, 0)), tags[2], tags[2],
            affine_mul(tags[5], affine_inv(tags[4])), tags[5], tags[5],
        )
        self.aggregate_table = ((0, 0, 1), (1, 0, 2), (2, 0, 1), (3, 1, 2), (4, 1, 2), (5, 1, 1))
        self.maps: dict[tuple[int, ...], np.ndarray] = {}

    def pmap(self, permutation: tuple[int, ...]) -> np.ndarray:
        if permutation not in self.maps:
            self.maps[permutation] = np.asarray([self.psidx[floor.M(permutation, value)] for value in self.psels], dtype=np.int32)
        return self.maps[permutation]

    def word_tags(self, word: tuple[int, ...]) -> tuple[Affine, ...]:
        return tuple(affine_eval(floor.sub(word, *pair), self.images) for pair in floor.OO)


def multiply_monomial(left: tuple[int, int, int], right: tuple[int, int, int]) -> tuple[int, int, int] | None:
    value = tuple(left[index] + right[index] for index in range(3))
    if any(entry > 2 for entry in value) or sum(value) > 2:
        return None
    return value  # type: ignore[return-value]


PRODUCT = [[-1] * 10 for _ in range(10)]
for _i, _left in enumerate(MONOMIALS):
    for _j, _right in enumerate(MONOMIALS):
        _value = multiply_monomial(_left, _right)
        if _value is not None:
            PRODUCT[_i][_j] = MONOMIAL_INDEX[_value]


def poly_mul(left: np.ndarray, right: np.ndarray) -> np.ndarray:
    output = np.zeros(10, dtype=np.uint8)
    for i in np.flatnonzero(left):
        for j in np.flatnonzero(right):
            target = PRODUCT[int(i)][int(j)]
            if target >= 0:
                output[target] = (int(output[target]) + int(left[i]) * int(right[j])) % 3
    return output


def e_poly(vector: tuple[int, int, int]) -> np.ndarray:
    output = np.zeros(10, dtype=np.uint8)
    output[0] = 1
    for variable, exponent0 in enumerate(vector):
        exponent = exponent0 % 3
        factor = np.zeros(10, dtype=np.uint8)
        factor[0] = 1
        if exponent:
            mono = [0, 0, 0]
            mono[variable] = 1
            factor[MONOMIAL_INDEX[tuple(mono)]] = exponent
        if exponent == 2:
            mono = [0, 0, 0]
            mono[variable] = 2
            factor[MONOMIAL_INDEX[tuple(mono)]] = 1
        output = poly_mul(output, factor)
    return output


def poly_rows_mul(factor: np.ndarray, rows: np.ndarray) -> np.ndarray:
    output = np.zeros_like(rows)
    for left in np.flatnonzero(factor):
        for right in range(10):
            target = PRODUCT[int(left)][right]
            if target >= 0:
                add(output[:, target], rows[:, right], int(factor[left]))
    return output


def lower_coord(tag: int, component: int, psl: int) -> int:
    return (tag * 2 + component) * 504 + psl


def grade1_coord(tag: int, component: int, monomial: int, psl: int) -> int:
    return ((tag * 2 + component) * 3 + monomial) * 504 + psl


def source_view(d0: np.ndarray, d1: np.ndarray, d2: np.ndarray, character: int, tag: int) -> np.ndarray:
    output = np.zeros((2, 10, 504), dtype=np.uint8)
    for component in (0, 1):
        begin = lower_coord(tag, component, 0)
        output[component, 0] = d0[character, begin:begin + 504]
        for monomial in range(3):
            begin = grade1_coord(tag, component, monomial, 0)
            output[component, 1 + monomial] = d1[character, begin:begin + 504]
        for monomial in range(6):
            begin = ((tag * 2 + component) * 6 + monomial) * 504
            output[component, 4 + monomial] = d2[character, begin:begin + 504]
    return output


def install_view(d0: np.ndarray, d1: np.ndarray, d2: np.ndarray, character: int, tag: int, value: np.ndarray) -> None:
    for component in (0, 1):
        begin = lower_coord(tag, component, 0)
        d0[character, begin:begin + 504] = value[component, 0]
        for monomial in range(3):
            begin = grade1_coord(tag, component, monomial, 0)
            d1[character, begin:begin + 504] = value[component, 1 + monomial]
        for monomial in range(6):
            begin = ((tag * 2 + component) * 6 + monomial) * 504
            d2[character, begin:begin + 504] = value[component, 4 + monomial]


def act(context: Context, row: tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray], tag_actors: tuple[Affine, ...]) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    d0, d1, d2, auxiliary = row
    output = (np.zeros_like(d0), np.zeros_like(d1), np.zeros_like(d2), auxiliary.copy())
    for tag, actor in enumerate(tag_actors):
        raw = np.zeros((4, 2, 10, 504), dtype=np.uint8)
        for parity_index, parity in enumerate(CHARACTERS):
            for source_index, source_label in enumerate(CHARACTERS):
                add(raw[parity_index], source_view(d0, d1, d2, source_index, tag), cv(context.transport[tag][source_label], parity))
        acted = np.zeros_like(raw)
        pmap = context.pmap(actor[0])
        for parity_index, parity in enumerate(CHARACTERS):
            target = (parity[0] ^ actor[1], parity[1] ^ actor[2])
            product = poly_rows_mul(e_poly(sign_kernel(parity, actor[3])), raw[parity_index])
            translated = np.zeros_like(product)
            translated[:, :, pmap] = product
            add(acted[CHARACTERS.index(target)], translated)
        for source_index, source_label in enumerate(CHARACTERS):
            value = np.zeros((2, 10, 504), dtype=np.uint8)
            tag_label = context.transport[tag][source_label]
            for parity_index, parity in enumerate(CHARACTERS):
                add(value, acted[parity_index], cv(tag_label, parity))
            install_view(output[0], output[1], output[2], source_index, tag, value)
    return output


def word_action(context: Context, row: tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray], word: tuple[int, ...]) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    return act(context, row, context.word_tags(word))


def associated_actor(context: Context, row: np.ndarray, character: int, letter: int) -> np.ndarray:
    output = np.zeros_like(row)
    label = CHARACTERS[character]
    source_q1 = floor.qev((letter,), context.q1_images)
    scalar = cv(label, (source_q1[1], source_q1[2]))
    for tag, actor in enumerate(context.actor_tags[letter]):
        pmap = context.pmap(actor[0])
        for component in (0, 1):
            for monomial in range(6):
                begin = ((tag * 2 + component) * 6 + monomial) * 504
                output[begin:begin + 504][pmap] = scalar * row[begin:begin + 504] % 3
    return output


def pure_project(context: Context, d2: np.ndarray, label: tuple[int, int]) -> np.ndarray:
    output = np.zeros_like(d2)
    zero0 = np.zeros((4, SOURCE0C), dtype=np.uint8)
    zero1 = np.zeros((4, SOURCE1C), dtype=np.uint8)
    zero_aux = np.zeros(8, dtype=np.uint8)
    row = (zero0, zero1, d2, zero_aux)
    for parity in CHARACTERS:
        acted = act(context, row, context.pure_tags[parity])
        add(output, acted[2], cv(label, parity))
    return output


def qnorm(word: tuple[int, ...], context: Context) -> tuple[list[tuple[int, Affine, int]], int]:
    gradient, endpoint = affine_fox(word, context.images)
    identity: Affine = (floor.ID9, 0, 0, (0, 0, 0))
    if endpoint != identity:
        raise RuntimeError("seed_endpoint")
    output: dict[tuple[int, Affine], int] = {}
    augmentation = 0
    for (generator, prefix), coefficient in gradient.items():
        if generator == 0:
            augmentation = (augmentation + coefficient) % 3
            first = affine_mul(prefix, context.images[0])
            second = affine_mul(first, context.pb3_b)
            for component, value in ((0, first), (1, second)):
                key = component, value
                output[key] = (output.get(key, 0) - coefficient) % 3
        else:
            key = 1, prefix
            output[key] = (output.get(key, 0) + coefficient) % 3
    return [(component, value, coefficient) for (component, value), coefficient in output.items() if coefficient], augmentation


def evaluate_seed(context: Context, word: tuple[int, ...]) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    d0 = np.zeros((4, SOURCE0C), dtype=np.uint8)
    d1 = np.zeros((4, SOURCE1C), dtype=np.uint8)
    d2 = np.zeros((4, SOURCE2C), dtype=np.uint8)
    auxiliary = np.zeros(8, dtype=np.uint8)
    for tag, pair in enumerate(floor.OO):
        normal, augmentation = qnorm(tuple(floor.sub(word, *pair)), context)
        auxiliary[tag] = augmentation
        for component, value, coefficient in normal:
            polynomial = e_poly(value[3])
            psl = context.psidx[value[0]]
            for character, label in enumerate(CHARACTERS):
                weight = coefficient * cv(context.transport[tag][label], (value[1], value[2]))
                d0[character, lower_coord(tag, component, psl)] = (int(d0[character, lower_coord(tag, component, psl)]) + weight * int(polynomial[0])) % 3
                for monomial in range(3):
                    coordinate = grade1_coord(tag, component, monomial, psl)
                    d1[character, coordinate] = (int(d1[character, coordinate]) + weight * int(polynomial[1 + monomial])) % 3
                for monomial in range(6):
                    coordinate = ((tag * 2 + component) * 6 + monomial) * 504 + psl
                    d2[character, coordinate] = (int(d2[character, coordinate]) + weight * int(polynomial[4 + monomial])) % 3
    exponent = floor.exps(word)
    if exponent[0] % 18 or exponent[1] % 18:
        raise RuntimeError("integral_exponent")
    auxiliary[6:] = (exponent[0] // 18 % 3, exponent[1] // 18 % 3)
    return d0, d1, d2, auxiliary


def split_p1(row: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    return row[:SOURCE0].reshape(4, SOURCE0C), row[SOURCE0:SOURCE0 + SOURCE1].reshape(4, SOURCE1C), row[-8:]


def flat_p1(row: tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]) -> np.ndarray:
    return np.concatenate((row[0].reshape(-1), row[1].reshape(-1), row[3]))


def combine(rows: list[np.ndarray], expression: list[list[int]], width: int) -> np.ndarray:
    output = np.zeros(width, dtype=np.uint8)
    for index, coefficient in expression:
        add(output, rows[index], coefficient)
    return output


def normalize_expression(entries: Iterable[Iterable[int]]) -> list[list[int]]:
    values: dict[int, int] = {}
    for index, coefficient in entries:
        values[int(index)] = (values.get(int(index), 0) + int(coefficient)) % 3
    return [[index, values[index]] for index in sorted(values) if values[index]]


def aggregate(context: Context, row: tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    d0, d1, d2, auxiliary = row
    output = np.zeros((4, 2, 2, 10, 504), dtype=np.uint8)
    for tag, block, sign in context.aggregate_table:
        raw = np.zeros((4, 2, 10, 504), dtype=np.uint8)
        for parity_index, parity in enumerate(CHARACTERS):
            for source_index, source_label in enumerate(CHARACTERS):
                add(raw[parity_index], source_view(d0, d1, d2, source_index, tag), cv(context.transport[tag][source_label], parity))
        shift = context.shifts[tag]
        acted = np.zeros_like(raw)
        pmap = context.pmap(shift[0])
        for parity_index, parity in enumerate(CHARACTERS):
            target = (parity[0] ^ shift[1], parity[1] ^ shift[2])
            value = poly_rows_mul(e_poly(sign_kernel(parity, shift[3])), raw[parity_index])
            translated = np.zeros_like(value)
            translated[:, :, pmap] = value
            add(acted[CHARACTERS.index(target)], translated)
        for character, label in enumerate(CHARACTERS):
            value = np.zeros((2, 10, 504), dtype=np.uint8)
            for parity_index, parity in enumerate(CHARACTERS):
                add(value, acted[parity_index], sign * cv(label, parity))
            add(output[character, block], value)
    physical0 = np.zeros(PHYSICAL0, dtype=np.uint8)
    physical1 = np.zeros(PHYSICAL1, dtype=np.uint8)
    physical2 = np.zeros(PHYSICAL2, dtype=np.uint8)
    for character in range(4):
        for block in range(2):
            for component in (0, 1):
                begin0 = ((character * 2 + block) * 2 + component) * 504
                physical0[begin0:begin0 + 504] = output[character, block, component, 0]
                for monomial in range(3):
                    begin1 = (((character * 2 + block) * 2 + component) * 3 + monomial) * 504
                    physical1[begin1:begin1 + 504] = output[character, block, component, 1 + monomial]
                for monomial in range(6):
                    begin2 = (((character * 2 + block) * 2 + component) * 6 + monomial) * 504
                    physical2[begin2:begin2 + 504] = output[character, block, component, 4 + monomial]
    physical_aux = np.zeros(4, dtype=np.uint8)
    for tag, block, sign in context.aggregate_table:
        physical_aux[block] = (int(physical_aux[block]) + sign * int(auxiliary[tag])) % 3
    physical_aux[2:] = auxiliary[6:]
    return physical0, physical1, physical2, physical_aux


def full_project(context: Context, row: tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray], label: tuple[int, int]) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    output = tuple(np.zeros_like(part) for part in row)
    for parity in CHARACTERS:
        acted = act(context, row, context.pure_tags[parity])
        for destination, source in zip(output, acted):
            add(destination, source, cv(label, parity))
    return output  # type: ignore[return-value]


def add_full(destination: tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray], source: tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray], scalar: int) -> None:
    for left, right in zip(destination, source):
        add(left, right, scalar)


def reduce_word(word: Iterable[int]) -> list[int]:
    answer: list[int] = []
    for raw in word:
        letter = int(raw)
        require(letter != 0 and abs(letter) in (1, 2, 3, 4, 5, 6),
                "free word letter")
        if answer and answer[-1] == -letter:
            answer.pop()
        else:
            answer.append(letter)
    return answer


def inverse_word(word: Sequence[int]) -> list[int]:
    return [-int(letter) for letter in reversed(word)]


def exponent_pair(word: Sequence[int]) -> tuple[int, int]:
    return (sum(1 if x == 1 else -1 if x == -1 else 0 for x in word) % 3,
            sum(1 if x == 2 else -1 if x == -2 else 0 for x in word) % 3)


def paper_product(*displayed: Sequence[int]) -> list[int]:
    return reduce_word(letter for factor in reversed(displayed) for letter in factor)


def row_key(block: int, component: int, raw: bytes) -> bytes:
    require(block in (1, 2, 3) and 1 <= component <= 6, "row key type")
    return b"R" + bytes((block, component)) + len(raw).to_bytes(2, "big") + raw


def exponent_key(index: int) -> bytes:
    require(index in (1, 2), "exponent key")
    return b"E" + bytes((index,))


def decode_row_key(key: bytes) -> tuple[int, int, bytes]:
    require(len(key) >= 5 and key[:1] == b"R", "decode row key")
    width = int.from_bytes(key[3:5], "big")
    require(len(key) == width + 5 and key[1] in (1, 2, 3) and
            1 <= key[2] <= 6, "decode row width/type")
    return key[1], key[2], key[5:]


def add_scaled(target: Sparse, source: Sparse, scalar: int) -> None:
    scalar %= 3
    for key, coefficient in source.items():
        value = (target.get(key, 0) + scalar * int(coefficient)) % 3
        if value:
            target[key] = value
        else:
            target.pop(key, None)


def scaled(source: Sparse, scalar: int) -> Sparse:
    return {key: int(value) * scalar % 3 for key, value in source.items()
            if int(value) * scalar % 3}


def pair(functional: Sparse, row: Sparse) -> int:
    return sum(int(value) * int(row.get(key, 0))
               for key, value in functional.items()) % 3


def public_sparse(row: Sparse) -> list[list[Any]]:
    return [[key.hex(), int(row[key]) % 3] for key in sorted(row)
            if int(row[key]) % 3]


def parse_sparse(rows: Sequence[Sequence[Any]]) -> Sparse:
    require(type(rows) is list, "sparse rows list")
    answer: Sparse = {}
    for item in rows:
        require(type(item) is list and len(item) == 2 and item[1] in (1, 2),
                "sparse item")
        key = bytes.fromhex(str(item[0]))
        require(key not in answer, "duplicate sparse key")
        answer[key] = int(item[1])
    require(public_sparse(answer) == list(rows), "canonical sparse order")
    return answer


def checker_packed_joint_blob(value: Any, label: str) -> bytes:
    require(type(value) is tuple and len(value) == 2,
            label + " tuple representation")
    permutation, pc = value
    require(type(permutation) in (bytes, tuple) and type(pc) is bytes,
            label + " component representation")
    degree = len(permutation)
    pc_width = {36: 4, 144: 10}.get(degree)
    require(pc_width is not None and len(pc) == pc_width and
            set(permutation) == set(range(degree)), label + " shape")
    return bytes(permutation) + pc


def checker_value_from_blob(raw: bytes, block: int) -> tuple[bytes, bytes]:
    degree = 36 if block in (1, 2) else 144
    width = degree + (4 if degree == 36 else 10)
    require(type(raw) is bytes and len(raw) == width and
            set(raw[:degree]) == set(range(degree)),
            "checker typed blob")
    return raw[:degree], raw[degree:]


def _serial_group(_unused: Any, row: dict[Any, int], block: int) -> Sparse:
    answer: Sparse = {}
    for (component, value), coefficient0 in row.items():
        coefficient = int(coefficient0) % 3
        if coefficient:
            raw = checker_packed_joint_blob(value, "checker group element")
            key = row_key(block, int(component), raw)
            answer[key] = (answer.get(key, 0) + coefficient) % 3
            if not answer[key]:
                del answer[key]
    return answer


def _serial_public(_unused: Any, row: dict[Any, int]) -> list[list[Any]]:
    result = []
    for (component, value), coefficient0 in row.items():
        coefficient = int(coefficient0) % 3
        if coefficient:
            result.append([int(component), checker_packed_joint_blob(
                value, "checker public element").hex(), coefficient])
    result.sort(key=lambda item: (item[0], bytes.fromhex(item[1])))
    return result


def build_checker_light(sources: SevenSources) -> dict[str, Any]:
    """Independent light reconstruction; no producer or old checker import."""
    old=LocalWords(); e3,e4=local_quotients(sources.json('q3'))
    words=json.loads((ROOT/'scratchpad/a0_paper_words_v1.json').read_text(encoding='utf-8')); g760=list(map(int,words['g760']))
    require(len(g760) == 760 and sha_obj(g760) ==
            "518f09820b8d7baee6b58ebf366cebf7b02a9a945cd1350cf8c701a4e6bc2b4d",
            "checker g760")
    h1, h2 = old.hexagon_words(g760)
    h1 = list(old.embed_f2_pb3(h1)); h2 = list(old.embed_f2_pb3(h2))
    pcontexts = [([1], [4]), ([4], [6]),
                 (paper_product([2], [4]), [6]),
                 (paper_product([1], [2]), paper_product([5], [6])),
                 ([1], paper_product([4], [5]))]
    factors = [old.f2_substitute(g760, left, right) for left, right in pcontexts]
    pword = paper_product(factors[1], factors[3], factors[0],
                          old.inv_word(factors[2]), old.inv_word(factors[4]))
    runtime = {"old": old, "e3": e3, "e4": e4,
               "g760": list(g760),
               "pcontexts": pcontexts}
    runtime["model"] = IndependentAllSeven(runtime)
    return runtime


def group_for(runtime: dict[str, Any], block: int) -> Any:
    return runtime["e3"] if block in (1, 2) else runtime["e4"]


def unpack_element(runtime: dict[str, Any], raw: bytes, block: int) -> Any:
    return checker_value_from_blob(raw, block)


def blob(runtime: dict[str, Any], value: Any) -> bytes:
    return checker_packed_joint_blob(value, "checker typed element")


def boundary_row(runtime: dict[str, Any], block: int, relator: int,
                 translation_hex: str) -> Sparse:
    rows = runtime["boundary_group"][block]
    require(1 <= relator <= len(rows), "checker boundary relator")
    quotient = group_for(runtime, block)
    translation = unpack_element(runtime, bytes.fromhex(translation_hex), block)
    answer: Sparse = {}
    for (component, value), coefficient0 in rows[relator - 1].items():
        translated = quotient.mul(translation, value)
        key = row_key(block, int(component), blob(runtime, translated))
        coefficient = int(coefficient0) % 3
        answer[key] = (answer.get(key, 0) + coefficient) % 3
        if not answer[key]:
            del answer[key]
    return answer


class IndependentAllSeven:
    def __init__(self, runtime: dict[str, Any]) -> None:
        self.rt = runtime; self.old = runtime["old"]
        self.e3, self.e4 = runtime["e3"], runtime["e4"]
        self.g = runtime["g760"]
        x, y = [1], [2]
        z = self.old.inv_word(self.old.pp_words([x, y]))
        u = self.old.inv_word(self.old.pp_words([y, x]))
        raw_specs = [(1, self.e3, x, y, 1, True, "H1_fxy"),
            (1, self.e3, x, z, -1, True, "H1_fxz"),
            (1, self.e3, y, z, 1, True, "H1_fyz"),
            (2, self.e3, u, x, -1, True, "H2_fux"),
            (2, self.e3, x, y, -1, True, "H2_fxy"),
            (2, self.e3, u, y, 1, True, "H2_fuy")]
        for natural, label in ((1, "P_b1"), (3, "P_b2"), (0, "P_b3"),
                               (2, "P_b5_inverse"), (4, "P_b4_inverse")):
            left, right = runtime["pcontexts"][natural]
            raw_specs.append((3, self.e4, left, right,
                              -1 if natural in (2, 4) else 1, False, label))
        self.specs = []
        for block, quotient, left, right, sign, lift, label in raw_specs:
            base = self._substitute(self.g, left, right, lift)
            factor = signed_base_factor(base,sign,self.old.inv_word)
            self.specs.append({"block": block, "quotient": quotient,
                "left": left, "right": right, "sign": sign, "lift": lift,
                "label": label, "base_factor": factor})
        occurrences=occurrence_prefix_gate(self.specs,(1,2,3),lambda block:group_for(runtime,block).identity,lambda block,a,b:group_for(runtime,block).mul(a,b),lambda block,word:group_for(runtime,block).eval(word))
        for spec,occurrence in zip(self.specs,occurrences): spec["occurrence_prefix"]=occurrence

    def _substitute(self, word: Sequence[int], left: Sequence[int],
                    right: Sequence[int], lift: bool) -> list[int]:
        result = self.old.f2_substitute(list(word), list(left), list(right))
        return list(self.old.embed_f2_pb3(result)) if lift else list(result)

    def occurrence_column(self, delta: Sequence[int], relator: Sequence[int]) -> Sparse:
        answer: Sparse = {}
        for spec in self.specs:
            quotient = spec["quotient"]
            relation = self._substitute(relator, spec["left"], spec["right"],
                                        spec["lift"])
            relation=signed_relation(relation,spec["sign"])
            gradient, value = self.old.fox_gradient_without_sections(relation, quotient)
            require(value == quotient.identity, "checker occurrence relation")
            qword = self._substitute(delta, spec["left"], spec["right"], spec["lift"])
            translated = self.old.translate_vector(
                self.old.translate_vector(gradient, quotient.eval(qword), quotient),
                spec["occurrence_prefix"], quotient)
            add_scaled(answer, _serial_group(None, translated,
                                             spec["block"]), 1)
        e1, e2 = exponent_pair(relator)
        if e1: answer[exponent_key(1)] = e1
        if e2: answer[exponent_key(2)] = e2
        return answer

    def coordinates(self, word: Sequence[int]) -> list[bytes]:
        """Ten independent E3/E4 coordinate blobs for a literal F2 word."""
        values = []
        for spec, coordinate in zip(self.specs,
                                    (0, 1, 2, 3, 0, 4, 5, 6, 7, 8, 9)):
            qword = self._substitute(word, spec["left"], spec["right"], spec["lift"])
            value = spec["quotient"].eval(qword)
            while len(values) <= coordinate:
                values.append(None)
            if values[coordinate] is None:
                values[coordinate] = blob(self.rt, value)
            else:
                require(values[coordinate] == blob(self.rt, value),
                        "checker repeated coordinate")
        require(len(values) == 10 and all(type(value) is bytes for value in values),
                "checker complete coordinates")
        return values

    def occurrence_data(self, relator: Sequence[int], dual: Sparse) -> dict[str, Any]:
        merged: dict[tuple[int, bytes], int] = {}
        occurrence_rows = []
        coordinate_order = (0, 1, 2, 3, 0, 4, 5, 6, 7, 8, 9)
        for ordinal, (spec, coordinate) in enumerate(zip(self.specs,
                                                          coordinate_order), 1):
            quotient = spec["quotient"]
            relation = self._substitute(relator, spec["left"], spec["right"],
                                        spec["lift"])
            relation=signed_relation(relation,spec["sign"])
            gradient, value = self.old.fox_gradient_without_sections(relation, quotient)
            require(value == quotient.identity, "checker formula relation")
            prefix_inverse = quotient.inverse(spec["occurrence_prefix"])
            count = 0
            for (component, base_value), base_coefficient in gradient.items():
                base_inverse = quotient.inverse(base_value)
                for key, lambda_coefficient in dual.items():
                    if key[:1] != b"R":
                        continue
                    block, dual_component, target_raw = decode_row_key(key)
                    if block != spec["block"] or dual_component != int(component):
                        continue
                    target = unpack_element(self.rt, target_raw, block)
                    required = quotient.mul(quotient.mul(prefix_inverse, target),
                                            base_inverse)
                    merged_key = (coordinate, blob(self.rt, required))
                    coefficient = int(base_coefficient) * int(lambda_coefficient) % 3
                    if coefficient:
                        value0 = (merged.get(merged_key, 0) + coefficient) % 3
                        if value0:
                            merged[merged_key] = value0
                        else:
                            merged.pop(merged_key, None)
                        count += 1
            occurrence_rows.append({"ordinal": ordinal, "label": spec["label"],
                "coordinate": coordinate, "factor_sign": spec["sign"],
                "raw_dual_pair_terms": count})
        e1, e2 = exponent_pair(relator)
        constant = (dual.get(exponent_key(1), 0) * e1 +
                    dual.get(exponent_key(2), 0) * e2) % 3
        ordered = sorted(merged.items(), key=lambda item: (item[0][0], item[0][1]))
        public = {"K": constant,
            "terms": [[coordinate, raw.hex(), coefficient]
                      for (coordinate, raw), coefficient in ordered],
            "same_target_merged_mod3": True, "zero_sums_deleted": True,
            "eleven_occurrences": occurrence_rows}
        return {"constant": constant, "merged": merged, "public": public}

    def _pentagon(self, word: Sequence[int]) -> list[int]:
        factors = [self.old.f2_substitute(list(word), left, right)
                   for left, right in self.rt["pcontexts"]]
        return paper_product(factors[1], factors[3], factors[0],
                             self.old.inv_word(factors[2]),
                             self.old.inv_word(factors[4]))

    def direct_column(self, delta: Sequence[int], relator: Sequence[int]) -> tuple[Sparse,
                                                                                   dict[str, Any]]:
        conjugate = reduce_word(list(delta) + list(relator) + inverse_word(delta))
        conjugate_coordinates=self.coordinates(conjugate)
        require(all(raw==blob(self.rt,self.e3.identity) for raw in conjugate_coordinates[:5]) and
                all(raw==blob(self.rt,self.e4.identity) for raw in conjugate_coordinates[5:]),
                "checker conjugate endpoint kernel")
        corrected = reduce_word(self.g + conjugate)
        base_hex = self.old.hexagon_words(self.g)
        corrected_hex = self.old.hexagon_words(corrected)
        words = [(1, self.e3, list(self.old.embed_f2_pb3(base_hex[0])),
                  list(self.old.embed_f2_pb3(corrected_hex[0]))),
                 (2, self.e3, list(self.old.embed_f2_pb3(base_hex[1])),
                  list(self.old.embed_f2_pb3(corrected_hex[1]))),
                 (3, self.e4, self._pentagon(self.g), self._pentagon(corrected))]
        answer: Sparse = {}; quotient_values = []
        for block, quotient, base_word, corrected_word in words:
            base_gradient, base_value = self.old.fox_gradient_without_sections(
                base_word, quotient)
            corrected_gradient, corrected_value = self.old.fox_gradient_without_sections(
                corrected_word, quotient)
            require(base_value == quotient.identity and corrected_value == quotient.identity,
                    "checker direct all-seven identity")
            difference = dict(corrected_gradient)
            for key, coefficient in base_gradient.items():
                value = (difference.get(key, 0) - int(coefficient)) % 3
                if value: difference[key] = value
                else: difference.pop(key, None)
            add_scaled(answer, _serial_group(None, difference, block), 1)
            quotient_values.append(blob(self.rt, corrected_value).hex())
        e1, e2 = exponent_pair(conjugate)
        if e1: answer[exponent_key(1)] = e1
        if e2: answer[exponent_key(2)] = e2
        occurrence = self.occurrence_column(delta, relator)
        direct_occurrence_gate(answer,occurrence)
        return answer, {"delta_word": list(delta), "relator_word": list(relator),
            "conjugate_word": conjugate, "corrected_word": corrected,
            "quotient_value_blobs": quotient_values,
            "eleven_occurrence_replay": True, "direct_all_seven_replay": True}


EXPECTED_TRIANGULAR = {
    "columns": 2896, "rank": 2896, "boundary_columns": 2896,
    "correction_columns": 0, "raw_support_total": 20354,
    "raw_support_max": 12, "ancestry_entries_total": 137926,
    "ancestry_entries_max": 258,
    "ancestry_weighted_contributions": 1011460,
    "pivot_support_total": 289774, "pivot_support_max": 522,
    "future_ancestry_indices": 0, "zero_or_missing_diagonal": 0,
    "duplicate_empty_wrong_pivots": 0,
}
OLD_DUAL_SHA256 = "0960259714fa94ddd89e2ac4f582f040942ab7bd258185c0448c133e50b00f0c"
OLD_TARGET_SHA256 = "968f0b8325fa0e741e2c304bb940b96239c3e2d3226e0ca56f7d61a53dd0d82b"
KERNEL_ORDERS = [9, 9, 9, 9, 9, 1, 1, 1, 3, 3]
K0_INVERSE_MAX_BYTES = 256 * 1024 * 1024
DELTA_ORDER = 357_128_352


def checker_descriptors(runtime: dict[str, Any]) -> tuple[list[dict[str, Any]],
                                                           dict[tuple[int, int], list[int]]]:
    rows = []
    for block, count in ((1, 2), (2, 2), (3, 11)):
        quotient = group_for(runtime, block)
        for relator in range(1, count + 1):
            for (component, h), coefficient0 in runtime["boundary_group"][block][
                    relator - 1].items():
                coefficient = int(coefficient0) % 3
                if not coefficient:
                    continue
                h_raw = blob(runtime, h); h_inverse = quotient.inverse(h)
                rows.append({"block": block, "relator": relator,
                    "component": int(component), "h": h, "h_blob": h_raw,
                    "h_inverse": h_inverse,
                    "h_inverse_blob": blob(runtime, h_inverse),
                    "base_coefficient": coefficient})
    rows.sort(key=lambda row: (row["block"], row["relator"], row["component"],
                               row["h_blob"], row["base_coefficient"]))
    require(len(rows) == 104, "checker complete descriptor owner")
    lookup: dict[tuple[int, int], list[int]] = {}
    for index, row in enumerate(rows):
        lookup.setdefault((row["block"], row["component"]), []).append(index)
    return rows, lookup


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--state',type=Path); ap.add_argument('--candidate',type=Path); ap.add_argument('--task601',type=Path); ap.add_argument('--payload',type=Path); ap.add_argument('--out',type=Path); ap.add_argument('--selftest',action='store_true'); a=ap.parse_args()
    try:
        if a.selftest: selftest(); return 0
        if not a.task601 or not a.payload or not a.out: fail('usage')
        if not a.state or not a.candidate: fail('usage_parents')
        authenticate_paper_pins(); auth_source_state(a.state); _manifest,_loaded,_roots,_leaves=auth_task601(a.task601); auth_candidate(a.candidate,_roots); manifest,_blobs=validate_payload(a.payload,a.task601,_roots,_leaves)
        if manifest.get('source_ancestry_sha256') != EXPECTED_FILES['source_ancestry'][2] or manifest.get('roots_sha256') != sha(_loaded['roots']): fail('consumer_parent_receipt_sha')
        if manifest.get('dimensions') != {'lower':LOWER,'top':TOP,'packed_rho2':PACKED}: fail('consumer_dimensions')
        verdict={'schema':'d972.r07.a0.fresh-precision2-endpoint-signature.v4.checker','marker':MARKER,'payload_manifest_sha256':sha((a.payload/'manifest.json').read_bytes()),'rho2_sha256':sha(_blobs['rho2_packed']),'lower_coordinates_checked':LOWER,'top_coordinates_checked':TOP,'cross_checked':False,'verified':False}
        a.out.write_bytes(canon(verdict)); print(MARKER); return 0
    except Exception as exc:
        error=str(exc); status='UNKNOWN_RESOURCE' if error.startswith('UNKNOWN_RESOURCE:') else 'NOT_READY'
        print(json.dumps({'status':status,'error':error},sort_keys=True),file=sys.stderr); return 1
if __name__=='__main__': raise SystemExit(main())


