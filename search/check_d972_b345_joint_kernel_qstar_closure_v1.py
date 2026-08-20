"""Independent checker for the 157ee joint-kernel qstar certificate."""
from __future__ import annotations

import argparse
import base64
import hashlib
import importlib.util
import json
import struct
import sys
import time
from collections import Counter
from pathlib import Path
from typing import Any, Iterable, Sequence


ROOT = Path(__file__).resolve().parents[1]
TASK = Path("sol/luna_task_157ee_b345_joint_kernel_qstar_closure.md")
TASK_SHA = "64a32c0b7e3d4efc41ddb8e0e7036282b0b5430d9ab46bbfe125b588478a95d4"
PRODUCER = Path("search/d972_b345_joint_kernel_qstar_closure_v1.py")
PRODUCER_SHA = "06ba6cf361957db3e339d48d14b3d4fbc689de9642e3f96273fbe8f3160e76dc"
PREV = Path("search/check_d972_b345_triple_cube_raw_lambda_census_v1.py")
PREV_SHA = "677aa1b69e4415da9629c34fcf0e469ad974cf3c888be7e768635bac50f672ce"
PREV_PRODUCER = Path("search/d972_b345_triple_cube_raw_lambda_census_v1.py")
PREV_PRODUCER_SHA = "d4a290984ae8a93b6959f06d20c1de037b2814707778fba03c59ac87b2f736db"
PREV_DRIVER = Path("search/d972_b345_triple_cube_raw_lambda_census_gha_driver_v1.g")
PREV_DRIVER_SHA = "29a31752d42bd3f5a0e7f27ca38495bdd54c9cc694d12ddf9fe637e8749975e9"
PREV_TASK = Path("sol/luna_task_157ed_b345_triple_cube_raw_lambda_census.md")
PREV_TASK_SHA = "15511f73e665a90f1e518383cb7bd218d8dd8e747026c498c3b4acce62837c2f"
Q3_PATH = Path("ci/out/d972_b345_q3_chief_v1.json")
Q3_SHA = "3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72"
SCHEMA = "d972-b345-joint-kernel-qstar-closure/v1"

TERMINALS = frozenset({
    "B345_JOINT_KERNEL_QSTAR_CLOSED",
    "B345_JOINT_KERNEL_QSTAR_ACTIVE",
    "B345_JOINT_KERNEL_QSTAR_UNKNOWN_RESOURCE",
    "B345_JOINT_KERNEL_QSTAR_UNKNOWN_INPUT",
})

P_RELATORS = [
    [-2,-2,1,1,2,1,2,1,1],
    [1,-2,-2,-2,-2,1,-2,-2,-2,-2],
    [-1,2,-1,-2,-1,-1,-2,-2,-1,-1,-2],
    [2,1,1,2,-1,2,-1,-1,2,-1,-1,2,-1],
    [-1,-2,-1,-1,-2,1,2,1,1,1,-2,-1,-1,-1],
]
G9_RELATORS = [
    [1,2,2,-1,2,2],
    [2,-1,-1,-2,-1,-1],
    [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [2,1,-2,-2,-2,-2,-2,-2,-2,-2,1,2,1,-2,-2,-2,-2,-2,-2,-2,-2,1],
    [1,2,1,2,-1,-2,-1,-2,-1,-2,1,2,-1,-1,-1,-1,2,1,2,1,2,1,2,1,2,1,2,1,2,-1,2,1,1,1,1,2,-1,-2],
    [-1,-1,-1,2,1,2,-1,-2,-1,-2,-1,-2,-1,-2,-1,2,1,2,1,-2,-1,-1,-1,-2,1,-2,-1,-2,-1,-2,-1,-2,-1,-2,-1,-2,1,-2,1,-2],
    [1,-2,-1,-2,1,2,1,2,1,2,1,2,1,-2,-1,-2,1,1,1,1,1,1,-2,-1,-2,1,2,1,2,1,2,1,2,1,-2,-1,-2,1,1,1,1,1],
]
SPLIT_WORDS = [
    [1,-2,1,1,2,-1,-2,-2,1,-2,-1,-1,-2,-1,-1,-2,-2,1,-2,-2],
    [-1,-1,-2,-1,-1,2,1,2,1,1,2,1,2,2],
    [1,2,2,-1,2,2,1,1,2,1,1,2,-1,2,2,1,-2,-1,-1,2,-1],
    [-2,-2,-1,-2,-1,-1,-2,-1,-2,1,1,2,1,1,2],
]
FACTOR_PAYLOAD = [[504,2916,1469664],P_RELATORS,G9_RELATORS,SPLIT_WORDS]
FACTOR_PAYLOAD_SHA = "6eb95a6830b19e729c5e2a9b4f861fb6105ac0be1f1058cc566898d1b48758ba"
COMPLETE_RELATORS_SHA = "dcb8ce42c8324b0ce2a5018007f3d664da5568ee73182758a9f358deba84bc2a"

TOP_KEYS = {"schema","task_sha256","terminal_token","status","reason",
            "claim","fixed_prefix_only","claim_flags","pins","source_hashes",
            "base_q3_replay","normalized_inverse_fibre",
            "directed_base_support","directed_surgery","prefix",
            "lambda_oracle","base_target6","record_manifest",
            "context_registry","gamma",
            "internal_relations","action_relations","q0_presentation",
            "q0_relations","direct_canaries","theorem_boundary","performance",
            "resource_guards","partial"}


def require(value: Any, message: str) -> None:
    if not value:
        raise RuntimeError(message)


def digest_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def digest_obj(value: Any) -> str:
    return digest_bytes(json.dumps(value,sort_keys=True,separators=(",",":"),
                                   ensure_ascii=True).encode("utf-8"))


def digest_file(path: Path) -> str:
    h=hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda:stream.read(1<<20),b""):
            h.update(block)
    return h.hexdigest()


class Deadline:
    def __init__(self,seconds:float)->None:
        require(0 < seconds <= 18000,"checker deadline")
        self.end=time.monotonic()+seconds;self.checks=0
    def check(self,phase:str,force:bool=False)->None:
        self.checks+=1
        if (force or self.checks%64==0) and time.monotonic()>=self.end:
            raise RuntimeError("checker common deadline exhausted: "+phase)


DEADLINE: Deadline | None = None


def tick(phase:str,force:bool=False)->None:
    if DEADLINE is not None: DEADLINE.check(phase,force)


def load_prev()->Any:
    for path,sha in ((TASK,TASK_SHA),(PRODUCER,PRODUCER_SHA),(PREV,PREV_SHA),
                     (PREV_PRODUCER,PREV_PRODUCER_SHA),
                     (PREV_DRIVER,PREV_DRIVER_SHA),(PREV_TASK,PREV_TASK_SHA)):
        require((ROOT/path).is_file() and digest_file(ROOT/path)==sha,
                "157ee checker authenticated pin: "+path.as_posix())
    name="_d972_157ee_independent_157ed_checker"
    require(name not in sys.modules,"157ee checker module name")
    spec=importlib.util.spec_from_file_location(name,ROOT/PREV)
    require(spec is not None and spec.loader is not None,"157ee checker spec")
    module=importlib.util.module_from_spec(spec);sys.modules[name]=module
    try: spec.loader.exec_module(module)
    except BaseException:
        sys.modules.pop(name,None);raise
    return module


def load_q3(path:Path)->dict[str,Any]:
    require(path.resolve()==(ROOT/Q3_PATH).resolve() and path.is_file() and
            digest_file(path)==Q3_SHA,"157ee checker q3 pin")
    data=json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(data,dict),"157ee checker q3 object")
    return data


def pack_u16(values:Iterable[int])->dict[str,Any]:
    rows=[int(x) for x in values];raw=b"".join(struct.pack("<H",x) for x in rows)
    return {"encoding":"u16-le","count":len(rows),"byte_length":len(raw),
            "sha256":digest_bytes(raw),"base64":base64.b64encode(raw).decode("ascii"),
            "decoded_sha256":digest_obj(rows)}


def pack_u8(values:Iterable[int])->dict[str,Any]:
    rows=[int(x) for x in values];require(all(0<=x<=255 for x in rows),"u8")
    raw=bytes(rows)
    return {"encoding":"u8","count":len(rows),"byte_length":len(raw),
            "sha256":digest_bytes(raw),"base64":base64.b64encode(raw).decode("ascii"),
            "decoded_sha256":digest_obj(rows)}


def pack_bytes(raw:bytes,encoding:str)->dict[str,Any]:
    return {"encoding":encoding,"byte_length":len(raw),"sha256":digest_bytes(raw),
            "base64":base64.b64encode(raw).decode("ascii")}


def decode_u16(field:dict[str,Any],label:str)->list[int]:
    require(set(field)=={"encoding","count","byte_length","sha256",
                         "base64","decoded_sha256"} and
            field["encoding"]=="u16-le",label+" u16 schema")
    raw=base64.b64decode(field["base64"],validate=True)
    values=[struct.unpack_from("<H",raw,2*i)[0] for i in range(field["count"])]
    require(len(raw)==field["byte_length"]==2*field["count"] and
            digest_bytes(raw)==field["sha256"] and
            digest_obj(values)==field["decoded_sha256"],label+" u16 binding")
    return values


def decode_u8(field:dict[str,Any],label:str)->list[int]:
    require(set(field)=={"encoding","count","byte_length","sha256",
                         "base64","decoded_sha256"} and field["encoding"]=="u8",
            label+" u8 schema")
    raw=base64.b64decode(field["base64"],validate=True);values=list(raw)
    require(len(raw)==field["byte_length"]==field["count"] and
            digest_bytes(raw)==field["sha256"] and
            digest_obj(values)==field["decoded_sha256"],label+" u8 binding")
    return values


def validate_packed_cayley(public:dict[str,Any],order:int,
                           generator_count:int)->list[list[int]]:
    flat=decode_u16(public["transitions"],"checker Cayley transitions")
    parents=decode_u16(public["section_parent_states"],"checker Cayley parents")
    generators=decode_u8(public["section_parent_generators"],"checker Cayley generators")
    require(len(flat)==order*generator_count and len(parents)==len(generators)==order,
            "checker Cayley dimensions")
    transitions=[flat[i*generator_count:(i+1)*generator_count] for i in range(order)]
    require(all(1<=x<=order for row in transitions for x in row) and
            parents[0]==generators[0]==0,"checker Cayley root/ranges")
    for state in range(1,order):
        require(1<=parents[state]<=state and 1<=generators[state]<=generator_count and
                transitions[parents[state]-1][generators[state]-1]==state+1,
                "checker Cayley section tree")
    packed=public["canonical_states"]
    require(set(packed)=={"encoding","byte_length","sha256","base64",
                          "state_count","factor_widths_bytes","row_width_bytes"} and
            packed["encoding"]=="state-major exact blobs: E3 then 31 E4" and
            packed["state_count"]==order and
            packed["row_width_bytes"]==sum(packed["factor_widths_bytes"]),
            "checker Cayley state schema")
    raw=base64.b64decode(packed["base64"],validate=True)
    require(len(raw)==packed["byte_length"]==order*packed["row_width_bytes"] and
            digest_bytes(raw)==packed["sha256"],"checker Cayley state bytes")
    rows=[];offset=0
    for _ in range(order):
        row=[]
        for width in packed["factor_widths_bytes"]:
            require(isinstance(width,int) and width>0,"checker Cayley factor width")
            row.append(raw[offset:offset+width]);offset+=width
        rows.append(row)
    require(len({tuple(row) for row in rows})==order and
            public["state_rows_sha256"]==digest_obj([[x.hex() for x in row] for row in rows]) and
            public["transition_rows_sha256"]==digest_obj([[x-1 for x in row] for row in transitions]),
            "checker Cayley state/transition binding")
    return transitions


def p_mul(left:tuple[int,...],right:tuple[int,...])->tuple[int,...]:
    return tuple(left[right[i]-1] for i in range(len(left)))


def p_inv(value:tuple[int,...])->tuple[int,...]:
    out=[0]*len(value)
    for i,x in enumerate(value,1):out[x-1]=i
    return tuple(out)


def p_eval(word:Sequence[int],generators:Sequence[tuple[int,...]])->tuple[int,...]:
    value=tuple(range(1,len(generators[0])+1));inverse=list(map(p_inv,generators))
    for letter in word:
        value=p_mul(value,generators[abs(letter)-1] if letter>0
                    else inverse[abs(letter)-1])
    return value


def enumerate_perm_group(generators:Sequence[tuple[int,...]])->list[tuple[int,...]]:
    identity=tuple(range(1,len(generators[0])+1));states=[identity];seen={identity}
    for state in states:
        for generator in generators:
            value=p_mul(state,generator)
            if value not in seen:seen.add(value);states.append(value)
    return states


def substitute(old:Any,relator:Sequence[int],left:Sequence[int],right:Sequence[int])->list[int]:
    out=[]
    for letter in relator:
        word=left if abs(letter)==1 else right
        out=old.reduce_word(out+(list(word) if letter>0 else old.inv_word(word)))
    return out


def complete_relators(old:Any)->list[list[int]]:
    result=([substitute(old,row,SPLIT_WORDS[0],SPLIT_WORDS[1]) for row in P_RELATORS]+
            [substitute(old,row,SPLIT_WORDS[2],SPLIT_WORDS[3]) for row in G9_RELATORS]+
            [old.commutator(a,b) for a in SPLIT_WORDS[:2] for b in SPLIT_WORDS[2:]]+
            [old.reduce_word([1]+old.inv_word(old.reduce_word(SPLIT_WORDS[0]+SPLIT_WORDS[2]))),
             old.reduce_word([2]+old.inv_word(old.reduce_word(SPLIT_WORDS[1]+SPLIT_WORDS[3])))])
    require(len(result)==19 and digest_obj(result)==COMPLETE_RELATORS_SHA,
            "checker complete relators")
    return result


def element_blob(value:Any)->bytes:
    return bytes(value[0])+bytes(value[1])


class JointGroup:
    def __init__(self,old:Any,e3:Any,e4:Any,contexts:Sequence[Any],words:Sequence[Sequence[int]])->None:
        self.old,self.e3,self.e4=old,e3,e4;self.contexts=list(contexts)
        self.words=[list(x) for x in words]
        self.identity=(e3.identity,tuple(e4.identity for _ in contexts))
        self.generators=[self.eval(word) for word in words]
        self.states=[self.identity];self.ids={self.key(self.identity):0}
        self.parent=[None];self.parent_generator=[None]
        for state_id,state in enumerate(self.states):
            for generator_id,generator in enumerate(self.generators):
                value=self.mul(state,generator);key=self.key(value)
                if key not in self.ids:
                    self.ids[key]=len(self.states);self.states.append(value)
                    self.parent.append(state_id);self.parent_generator.append(generator_id)
        require(len(self.states)==243,"checker Gamma order")
        self.transitions=[[self.ids[self.key(self.mul(state,generator))]
                           for generator in self.generators] for state in self.states]

    def blob(self,value:Any)->bytes:return element_blob(value)
    def key(self,state:Any)->tuple[bytes,...]:
        return (self.blob(state[0]),)+tuple(self.blob(x) for x in state[1])
    def mul(self,left:Any,right:Any)->Any:
        return (self.e3.mul(left[0],right[0]),tuple(self.e4.mul(left[1][i],right[1][i])
                for i in range(len(self.contexts))))
    def inverse(self,value:Any)->Any:
        return (self.e3.inverse(value[0]),tuple(self.e4.inverse(x) for x in value[1]))
    def eval(self,word:Sequence[int])->Any:
        return (self.e3.eval(self.old.embed_f2(word)),tuple(
            self.e4.eval(word,[left,right]) for left,right in self.contexts))
    def section_factors(self,state:int)->list[int]:
        answer=[]
        while state:
            parent=self.parent[state];generator=self.parent_generator[state]
            require(parent is not None and generator is not None,"checker section")
            answer.append(generator);state=parent
        return list(reversed(answer))
    def closure_ids(self,generators:Iterable[int])->set[int]:
        rows=list(dict.fromkeys(int(x) for x in generators));seen={0};queue=[0]
        for state in queue:
            for generator in rows:
                target=self.ids[self.key(self.mul(self.states[state],self.states[generator]))]
                if target not in seen:seen.add(target);queue.append(target)
        return seen
    def invariants(self)->dict[str,Any]:
        inverse=[self.ids[self.key(self.inverse(x))] for x in self.states]
        def mul_id(a:int,b:int)->int:
            return self.ids[self.key(self.mul(self.states[a],self.states[b]))]
        greedy=[];subgroup={0}
        for value in self.generators:
            index=self.ids[self.key(value)]
            if index not in subgroup:greedy.append(index);subgroup=self.closure_ids(greedy)
        orders=[]
        for value in range(243):
            product=0
            for exponent in range(1,28):
                product=mul_id(product,value)
                if product==0:orders.append(exponent);break
        center=[v for v in range(243) if all(mul_id(v,g)==mul_id(g,v) for g in greedy)]
        comm=[mul_id(mul_id(inverse[a],inverse[b]),mul_id(a,b)) for a in greedy for b in greedy]
        derived=self.closure_ids(comm)
        cubes=self.closure_ids(mul_id(mul_id(v,v),v) for v in range(243))
        frattini=self.closure_ids(derived|cubes)
        unseen=set(range(243));classes=[]
        while unseen:
            seed=min(unseen);orbit={seed};queue=[seed]
            for value in queue:
                for generator in greedy:
                    target=mul_id(mul_id(inverse[generator],value),generator)
                    if target not in orbit:orbit.add(target);queue.append(target)
            unseen-=orbit;classes.append(len(orbit))
        normal=True
        for outer in (self.eval([1]),self.eval([2])):
            oi=self.inverse(outer)
            for generator in greedy:
                normal &= self.key(self.mul(self.mul(oi,self.states[generator]),outer)) in self.ids
        depth=[0]*243
        for state in range(1,243):
            parent=self.parent[state];require(parent is not None,"checker depth")
            depth[state]=depth[parent]+1
        result={"order":243,"edge_count":6318,"generator_count":26,
          "greedy_generator_state_ids":[x+1 for x in greedy],
          "greedy_generator_count":len(greedy),"max_section_factors":max(depth),
          "order_distribution":{str(k):v for k,v in sorted(Counter(orders).items())},
          "exponent":max(orders),"center_order":len(center),"derived_order":len(derived),
          "cube_subgroup_order":len(cubes),"frattini_order":len(frattini),
          "frattini_quotient_order":243//len(frattini),"frattini_dimension_F3":2,
          "derived_in_center":derived<=set(center),
          "conjugacy_class_size_distribution":{str(k):v for k,v in sorted(Counter(classes).items())},
          "normal_under_x_y":bool(normal),
          "state_rows_sha256":digest_obj([[x.hex() for x in self.key(state)] for state in self.states]),
          "transition_rows_sha256":digest_obj(self.transitions)}
        require(result["order_distribution"]=={"1":1,"3":26,"9":216} and
                result["center_order"]==27 and result["derived_order"]==3 and
                result["cube_subgroup_order"]==9 and result["frattini_order"]==27 and
                result["conjugacy_class_size_distribution"]=={"1":27,"3":72} and
                result["normal_under_x_y"] is True and result["max_section_factors"]==4,
                "checker Gamma invariants")
        return result
    def public(self)->dict[str,Any]:
        rows=[self.key(state) for state in self.states];widths=[len(x) for x in rows[0]]
        require(all([len(x) for x in row]==widths for row in rows),"checker state widths")
        raw=b"".join(x for row in rows for x in row)
        return {**self.invariants(),
          "transitions":pack_u16(x+1 for row in self.transitions for x in row),
          "section_parent_states":pack_u16(0 if x is None else x+1 for x in self.parent),
          "section_parent_generators":pack_u8(0 if x is None else x+1 for x in self.parent_generator),
          "canonical_states":{**pack_bytes(raw,"state-major exact blobs: E3 then 31 E4"),
             "state_count":243,"factor_widths_bytes":widths,"row_width_bytes":sum(widths)},
          "canonical_state_key":"E3 blob then 31 E4 blobs","first_seen_BFS":True}


class ScalarEngine:
    def __init__(self,prev:Any,old:Any,e4:Any,oracle:Any,words:Sequence[Sequence[int]],aliases:dict[str,int])->None:
        self.old,self.e4,self.oracle=old,e4,oracle;self.words=[list(x) for x in words]
        leaves=prev.target_leaves(old,e4,self.words);self.leaves=leaves
        self.spec={"a":(aliases["hexagon_1_fxy_0"]-1,leaves["outer"]["h"]),
                   "b":(aliases["hexagon_1_fxz_0"]-1,leaves["outer"]["C"]),
                   "c":(aliases["hexagon_1_fyz_0"]-1,leaves["outer"]["C"])}
        z=old.inv_word(old.pp([[1],[2]]));mapping=old.cofaces(3)[0]
        ops={"a":lambda w:old.f2_sub(w,[1],[2]),
             "b":lambda w:old.f2_sub(w,[1],z),"c":lambda w:old.f2_sub(w,[2],z)}
        self.letters={name:[old.fox(old.substitute(old.embed_f2(op(word)),mapping),e4)
                            for word in ([1],[2])] for name,op in ops.items()}
        self.cache={}
    def token_data(self,name:str,kind:str,index:int)->tuple[Any,Any]:
        if kind=="record":return self.leaves[name]["gradients"][index],self.leaves[name]["values"][index]
        return self.letters[name][index]
    def token_scalar(self,name:str,kind:str,index:int,sign:int,left:Any)->int:
        key=(name,kind,index,sign,element_blob(left))
        if key in self.cache:return self.cache[key]
        gradient,value=self.token_data(name,kind,index);coefficient=1
        if sign<0:left=self.e4.mul(left,self.e4.inverse(value));coefficient=2
        total=sum(coefficient*int(term)*self.oracle.lookup(
            component,self.e4.mul(left,element))
            for (component,element),term in gradient.items())%3
        self.cache[key]=total;return total
    def route(self,name:str,tokens:Sequence[tuple[str,int,int]])->int:
        prefix=self.e4.identity;total=0;outer=self.spec[name][1]
        for kind,index,sign in tokens:
            total=(total+self.token_scalar(name,kind,index,sign,self.e4.mul(outer,prefix)))%3
            _,value=self.token_data(name,kind,index)
            prefix=self.e4.mul(prefix,value if sign>0 else self.e4.inverse(value))
        require(prefix==self.e4.identity,"checker typed relation route")
        return total
    def vector(self,tokens:Sequence[tuple[str,int,int]])->tuple[int,int,int]:
        return tuple(self.route(name,tokens) for name in ("a","b","c"))  # type: ignore[return-value]
    @staticmethod
    def target(vector:Sequence[int])->int:return (int(vector[2])-int(vector[1])+int(vector[0]))%3
    def edge_scalar(self,name:str,state_value:Any,generator:int)->int:
        return self.token_scalar(name,"record",generator,1,
                                 self.e4.mul(self.spec[name][1],state_value))


def token_word(old:Any,words:Sequence[Sequence[int]],token:tuple[str,int,int])->list[int]:
    kind,index,sign=token;word=list(words[index]) if kind=="record" else ([1] if index==0 else [2])
    return word if sign>0 else old.inv_word(word)


def materialize(old:Any,words:Sequence[Sequence[int]],tokens:Sequence[tuple[str,int,int]])->list[int]:
    out=[]
    for token in tokens:out=old.reduce_word(out+token_word(old,words,token))
    return out


def internal_relations(group:JointGroup,engine:ScalarEngine)->tuple[dict[str,Any],list[Any],list[Any]|None]:
    potentials=[None]*243;potentials[0]=(0,0,0);queue=[0]
    for state in queue:
        for generator,target in enumerate(group.transitions[state]):
            edge=tuple(engine.edge_scalar(name,group.states[state][1][engine.spec[name][0]],generator)
                       for name in ("a","b","c"))
            value=tuple((potentials[state][i]+edge[i])%3 for i in range(3))  # type: ignore[index]
            if potentials[target] is None:potentials[target]=value;queue.append(target)
    require(all(x is not None for x in potentials),"checker potential coverage")
    rows=[];first=None;first_tokens=None
    for state,transitions in enumerate(group.transitions):
        for generator,target in enumerate(transitions):
            edge=tuple(engine.edge_scalar(name,group.states[state][1][engine.spec[name][0]],generator)
                       for name in ("a","b","c"))
            discrepancy=tuple((potentials[state][i]+edge[i]-potentials[target][i])%3 for i in range(3))  # type: ignore[index]
            scalar=engine.target(discrepancy);rows.append([state+1,generator+1,target+1,*discrepancy,scalar])
            if scalar and first is None:
                first=["internal",len(rows),scalar]
                first_tokens=([("record",x,1) for x in group.section_factors(state)]+[("record",generator,1)]+
                              [("record",x,-1) for x in reversed(group.section_factors(target))])
    flat=[x for row in rows for x in row[3:6]]
    public={"row_count":6318,"all_component_zero":all(x==0 for x in flat),
      "target_scalar_counts":{str(v):sum(row[6]==v for row in rows) for v in range(3)},
      "component_vector_distribution":{str(vector):sum(tuple(row[3:6])==vector for row in rows)
          for vector in sorted(set(tuple(row[3:6]) for row in rows))},
      "rows_sha256":digest_obj(rows),"packed_component_vectors":pack_u8(flat),
      "presentation_complete_for_record_generators":True,"first_active":first}
    state,generator=1,0;target=group.transitions[state][generator]
    canary=([("record",x,1) for x in group.section_factors(state)]+[("record",generator,1)]+
            [("record",x,-1) for x in reversed(group.section_factors(target))])
    return public,canary,first_tokens


def action_relations(group:JointGroup,engine:ScalarEngine)->tuple[dict[str,Any],list[list[Any]]]:
    outer=[group.eval([1]),group.eval([2])];rows=[];token_rows=[]
    for record,generator in enumerate(group.generators):
        for letter,value in enumerate(outer):
            for orientation in (1,-1):
                if orientation==1:
                    conjugate=group.mul(group.mul(group.inverse(value),generator),value)
                    tokens=[("letter",letter,-1),("record",record,1),("letter",letter,1)]
                else:
                    conjugate=group.mul(group.mul(value,generator),group.inverse(value))
                    tokens=[("letter",letter,1),("record",record,1),("letter",letter,-1)]
                target=group.ids[group.key(conjugate)]
                tokens += [("record",x,-1) for x in reversed(group.section_factors(target))]
                vector=engine.vector(tokens);scalar=engine.target(vector)
                rows.append([record+1,letter+1,orientation,target+1,
                             len(group.section_factors(target)),*vector,scalar]);token_rows.append(tokens)
    return {"row_count":104,"all_component_zero":all(row[5:8]==[0,0,0] and row[-1]==0 for row in rows),
      "rows":rows,"rows_sha256":digest_obj(rows),
      "target_scalar_counts":{str(v):sum(row[-1]==v for row in rows) for v in range(3)},
      "conjugation_order":"record, x/y, g^-1*r*g then g*r*g^-1"},token_rows


def fp_order(relators:Sequence[Sequence[int]])->int:
    from sympy.combinatorics.free_groups import free_group
    from sympy.combinatorics.fp_groups import FpGroup
    free,x,y=free_group("x,y");generators=(x,y)
    rows=[]
    for relator in relators:
        value=free.identity
        for letter in relator:value*=generators[abs(letter)-1]**(1 if letter>0 else -1)
        rows.append(value)
    return int(FpGroup(free,rows).order(strategy="coset_table_based"))


def factor_presentation(q3:dict[str,Any],old:Any)->tuple[dict[str,Any],list[list[int]]]:
    require(digest_obj(FACTOR_PAYLOAD)==FACTOR_PAYLOAD_SHA,"checker factor payload")
    marked=q3["coarse_models"]["Q0"]["marked_permutations"]
    qgens=[tuple(x) for x in marked];pgens=[tuple(x[:9]) for x in marked]
    ggens=[tuple(v-9 for v in x[9:]) for x in marked]
    require(fp_order(P_RELATORS)==504 and fp_order(G9_RELATORS)==2916,
            "checker independent SymPy factor presentation orders")
    require(len(enumerate_perm_group(pgens))==504 and len(enumerate_perm_group(ggens))==2916,
            "checker factor marked image orders")
    pid=tuple(range(1,10));gid=tuple(range(1,28))
    require([(p_eval(w,pgens),p_eval(w,ggens)) for w in SPLIT_WORDS]==
            [(pgens[0],gid),(pgens[1],gid),(pid,ggens[0]),(pid,ggens[1])],
            "checker split word images")
    relators=complete_relators(old);qid=tuple(range(1,37))
    require(all(p_eval(w,qgens)==qid for w in relators),"checker complete Q0 relators")
    return {"factor_payload_sha256":FACTOR_PAYLOAD_SHA,"P_order":504,"G9_order":2916,
      "Q0_order":1469664,"P_state_count":504,"G9_state_count":2916,
      "P_relator_count":5,"G9_relator_count":8,"split_word_lengths":list(map(len,SPLIT_WORDS)),
      "split_word_sha256":digest_obj(SPLIT_WORDS),"complete_relator_count":19,
      "complete_relators_sha256":digest_obj(relators),
      "completeness_argument":"factor presentations plus cross commutation and x/y splitting",
      "producer_factor_enumeration":"independent marked-permutation BFS"},relators


def q0_relations(group:JointGroup,engine:ScalarEngine,relators:Sequence[Sequence[int]])->tuple[dict[str,Any],list[list[Any]]]:
    relation_ids=[group.ids[group.key(group.eval(row))] for row in relators]
    normal=list(dict.fromkeys(relation_ids));x,y=group.eval([1]),group.eval([2]);rounds=[]
    while True:
        subgroup=group.closure_ids(normal);add=[]
        for outer in (x,y):
            oi=group.inverse(outer)
            for generator in normal:
                target=group.ids[group.key(group.mul(group.mul(oi,group.states[generator]),outer))]
                if target not in subgroup and target not in add:add.append(target)
        if not add:break
        normal+=add;rounds.append({"added":len(add),"order_after":len(group.closure_ids(normal))})
    require(len(group.closure_ids(normal))==243,"checker Q0 defect normal closure")
    rows=[];tokens_all=[]
    for ordinal,(relator,target) in enumerate(zip(relators,relation_ids),1):
        tokens=[("letter",abs(x)-1,1 if x>0 else -1) for x in relator]
        tokens += [("record",x,-1) for x in reversed(group.section_factors(target))]
        vector=engine.vector(tokens);scalar=engine.target(vector)
        rows.append([ordinal,len(relator),target+1,len(group.section_factors(target)),*vector,scalar]);tokens_all.append(tokens)
    return {"row_count":19,"rows":rows,"rows_sha256":digest_obj(rows),
      "all_component_zero":all(row[4:7]==[0,0,0] and row[-1]==0 for row in rows),
      "relator_image_subgroup_order":len(group.closure_ids(relation_ids)),
      "relator_image_normal_closure_order":len(group.closure_ids(normal)),
      "normal_closure_rounds":rounds,
      "target_scalar_counts":{str(v):sum(row[-1]==v for row in rows) for v in range(3)}},tokens_all


def direct_canary(prev:Any,old:Any,e3:Any,e4:Any,contexts:Sequence[Any],pool:Any,basis:Any,
                  oracle:Any,word:Sequence[int],expected:int,label:str)->dict[str,Any]:
    require(e3.eval(old.embed_f2(word))==e3.identity and all(
        e4.eval(word,[left,right])==e4.identity for left,right in contexts),"checker canary typing")
    detail=old.checker_target6_formula(word,e4,include_gradient=True);raw=detail["direct_gradient"]
    public=old.checker_target6_public_from_detail(word,detail)
    require(public["quotient_identity"] is True and public["formula_equals_direct"] is True,
            "checker canary formula")
    direct=oracle.sparse(raw);remainder=old.checker_probe_remainder(raw,pool,basis)
    nf=prev.public_remainder_coefficient(remainder)
    require(direct==nf==expected,"checker canary direct/NF")
    return {"label":label,"word_length":len(word),"word_sha256":digest_obj(list(word)),
      "scalar":direct,"remainder_support":len(remainder),
      "remainder_sha256":digest_obj(sorted(remainder.items())),
      "formula_direct_equal":True,"NF_equal":True}


def validate_envelope(receipt:dict[str,Any])->None:
    require(set(receipt)==TOP_KEYS and receipt["schema"]==SCHEMA and
            receipt["task_sha256"]==TASK_SHA and receipt["terminal_token"] in TERMINALS and
            receipt["status"]==receipt["terminal_token"] and receipt["fixed_prefix_only"] is True,
            "checker exact envelope")
    flags=receipt["claim_flags"]
    require(set(flags)=={"whole_joint_kernel_fixed_prefix_closed","new_qstar_direction_found",
            "full_D2_claimed","full_H3_claimed","lift_nonexistence_claimed","B4_A_claimed","B4_B_claimed"}
            and all(flags[x] is False for x in ("full_D2_claimed","full_H3_claimed",
                "lift_nonexistence_claimed","B4_A_claimed","B4_B_claimed")),"checker no overclaim")
    require(receipt["pins"]=={"task_sha256":TASK_SHA,"157ed_producer_sha256":PREV_PRODUCER_SHA,
      "157ed_checker_sha256":PREV_SHA,"157ed_driver_sha256":PREV_DRIVER_SHA,
      "157ed_task_sha256":PREV_TASK_SHA,"q3_artifact_sha256":Q3_SHA},"checker pins")
    require(receipt["source_hashes"]=={"producer_path":PRODUCER.as_posix(),
                                      "producer_sha256":PRODUCER_SHA},"checker producer source")
    token=receipt["terminal_token"]
    if token=="B345_JOINT_KERNEL_QSTAR_CLOSED":
        require(receipt["reason"]=="joint_kernel_presentation_potential_zero" and
                receipt["claim"]=="fixed_prefix_whole_joint_kernel_qstar_closed" and
                flags["whole_joint_kernel_fixed_prefix_closed"] is True and
                flags["new_qstar_direction_found"] is False,"checker CLOSED envelope")
    elif token=="B345_JOINT_KERNEL_QSTAR_ACTIVE":
        require(receipt["reason"]=="defining_relation_nonzero" and
                receipt["claim"]=="positive_new_fixed_prefix_qstar_direction" and
                flags["whole_joint_kernel_fixed_prefix_closed"] is False and
                flags["new_qstar_direction_found"] is True,"checker ACTIVE envelope")
    elif token=="B345_JOINT_KERNEL_QSTAR_UNKNOWN_RESOURCE":
        require(receipt["claim"]=="none" and
                flags["whole_joint_kernel_fixed_prefix_closed"] is False and
                flags["new_qstar_direction_found"] is False and
                set(receipt["partial"])=={"phase","resource"} and
                receipt["reason"]==receipt["partial"]["resource"]["cap_reason"]==
                    receipt["partial"]["resource"]["cap_key"],"checker RESOURCE envelope")
    else:
        require(receipt["reason"]=="authenticated_external_input" and
                receipt["claim"]=="none" and
                flags["whole_joint_kernel_fixed_prefix_closed"] is False and
                flags["new_qstar_direction_found"] is False,"checker INPUT envelope")


def check_receipt(q3_path:Path,receipt_path:Path,seconds:float)->dict[str,Any]:
    global DEADLINE
    DEADLINE=Deadline(seconds);prev=load_prev();prev.CHECKER_DEADLINE=prev.Deadline(seconds)
    raw=receipt_path.read_bytes();receipt=json.loads(raw.decode("ascii"))
    require(raw==(json.dumps(receipt,sort_keys=True,separators=(",",":"),ensure_ascii=True)+"\n").encode("ascii"),
            "checker canonical receipt")
    validate_envelope(receipt);token=receipt["terminal_token"]
    if token=="B345_JOINT_KERNEL_QSTAR_UNKNOWN_INPUT":
        require(receipt["reason"]=="authenticated_external_input" and receipt["claim"]=="none",
                "checker input terminal")
        return receipt
    q3=load_q3(q3_path);old=prev.load_old();e3,e4=old.reconstruct(q3)
    old.validate_base_replay(receipt,q3,e3,e4)
    normalized,base_key,_=old.rebuild_normalized_inverse_fibre(q3,e4)
    require(receipt["normalized_inverse_fibre"]==normalized,"checker normalized inverse")
    contexts,aliases,context_public=old.independent_context_registry(e4)
    require(len(contexts)==31 and len(context_public["named_uses"])==46,"checker contexts")
    require(receipt["context_registry"]==context_public,"checker context registry")
    words=[list(row["word"]) for row in q3["correction_fibre"]["records"] if row["word"]]
    qgens=[tuple(row) for row in q3["coarse_models"]["Q0"]["marked_permutations"]]
    qid=tuple(range(1,37))
    require(len(words)==26 and len(set(map(tuple,words)))==26 and
            all(p_eval(word,qgens)==qid for word in words),"checker record kernel")
    expected_manifest={"record_count":26,"words_sha256":digest_obj(words),
      "record_order":"q3 nonempty rows 2..27","total_letters":sum(map(len,words)),
      "lengths":list(map(len,words)),"all_Q0_identity":True}
    require(receipt["record_manifest"]==expected_manifest,"checker record manifest")
    if not receipt["prefix"]:
        require(token=="B345_JOINT_KERNEL_QSTAR_UNKNOWN_RESOURCE","checker pre-prefix resource")
        return receipt
    tick("checker prefix",True)
    pool,basis,events=prev.replay_prefix(old,receipt,e4,normalized,base_key)
    if not receipt["lambda_oracle"]:
        require(token=="B345_JOINT_KERNEL_QSTAR_UNKNOWN_RESOURCE","checker pre-oracle resource")
        return receipt
    oracle=prev.RawOracle(old,pool,basis,prev.validate_qstar_label(prev.QSTAR,e4.degree+e4.collector.n))
    pivot_zero=[oracle.packed(row[0] if isinstance(row,tuple) else row)
                for _,row in sorted(basis.rows.items(),key=lambda item:pool.pivot_order(item[0]))]
    dependent_zero=[]
    for event in events:
        vector={}
        for component,blob_hex,coefficient in event["raw_column"]:
            identifier=pool.ids.get(bytes.fromhex(blob_hex));require(identifier is not None,"checker dependent key")
            vector[old.replay_pack_key(component,identifier)]=coefficient
        require(old.checker_full_remainder(vector,basis,pool)=={},"checker dependent NF")
        dependent_zero.append(oracle.packed(vector))
    require(pivot_zero==[0]*362709 and dependent_zero==[0]*16,"checker lambda annihilation")
    oracle.public.update({"pivot_annihilation_count":362709,
      "pivot_annihilation_sha256":digest_obj(pivot_zero),"dependent_annihilation_count":16,
      "dependent_annihilation_sha256":digest_obj(dependent_zero)})
    require(receipt["lambda_oracle"]==oracle.public,"checker lambda public")
    mapping=old.cofaces(3)[0]
    r0=old.substitute(old.embed_f2(old.hexagon_words(old.FIXED_WORD)[0]),mapping)
    base_raw,base_value=old.fox(r0,e4);require(base_value==e4.identity,"checker base value")
    base_rem=old.checker_probe_remainder(base_raw,pool,basis);base_lambda=oracle.sparse(base_raw)
    expected_base={"quotient_identity":True,"lambda":2,"negative_base_lambda":1,
      "remainder_support":len(base_rem),"remainder_sha256":digest_obj(sorted(base_rem.items())),
      "raw_gradient_support":len(base_raw),"raw_gradient_sha256":digest_obj(sorted(
        ([c,element_blob(v).hex(),int(x)%3] for (c,v),x in base_raw.items()),key=lambda z:(z[0],z[1]))),
      "direct_NF_equal":True}
    require(base_lambda==prev.public_remainder_coefficient(base_rem)==2 and
            receipt["base_target6"]==expected_base,"checker base target6")
    group=JointGroup(old,e3,e4,contexts,words)
    validate_packed_cayley(receipt["gamma"],243,26)
    require(receipt["gamma"]==group.public(),"checker Gamma")
    engine=ScalarEngine(prev,old,e4,oracle,words,aliases)
    internal,internal_canary,internal_active=internal_relations(group,engine)
    require(receipt["internal_relations"]==internal,"checker internal relations")
    actions,action_tokens=action_relations(group,engine)
    require(receipt["action_relations"]==actions,"checker action relations")
    tick("checker SymPy factor orders",True)
    q0_public,relators=factor_presentation(q3,old)
    require(receipt["q0_presentation"]==q0_public,"checker Q0 presentation")
    q0_rows,q0_tokens=q0_relations(group,engine,relators)
    require(receipt["q0_relations"]==q0_rows,"checker Q0 relations")
    active=[]
    if internal["first_active"] is not None:
        _,ordinal,scalar=internal["first_active"];require(internal_active is not None,"checker internal witness")
        active.append(("internal",ordinal,scalar,internal_active))
    for ordinal,(row,tokens) in enumerate(zip(actions["rows"],action_tokens),1):
        if row[-1]:active.append(("action",ordinal,row[-1],tokens))
    for ordinal,(row,tokens) in enumerate(zip(q0_rows["rows"],q0_tokens),1):
        if row[-1]:active.append(("q0",ordinal,row[-1],tokens))
    specs=[]
    if active:
        category,ordinal,scalar,tokens=active[0];specs=[(category,ordinal,tokens,scalar)]
    else:
        specs=[("internal",1,internal_canary,0),("action",53,action_tokens[52],0),
               ("action",104,action_tokens[103],0),("q0",1,q0_tokens[0],0),("q0",18,q0_tokens[17],0)]
    canaries=[direct_canary(prev,old,e3,e4,contexts,pool,basis,oracle,
               materialize(old,words,tokens),expected,f"{category}:{ordinal}")
              for category,ordinal,tokens,expected in specs]
    require(receipt["direct_canaries"]==canaries,"checker direct canaries")
    closed=internal["all_component_zero"] and actions["all_component_zero"] and q0_rows["all_component_zero"] and not active
    expected_token="B345_JOINT_KERNEL_QSTAR_CLOSED" if closed else "B345_JOINT_KERNEL_QSTAR_ACTIVE"
    require(token==expected_token,"checker mechanical terminal")
    expected_boundary={"fixed_prefix_only":True,"joint_kernel":"ker(Q0 x E3 x 31 E4 contexts)",
      "full_D2_claimed":False,"full_H3_claimed":False,"lift_nonexistence_claimed":False,
      "B4_A_claimed":False,"B4_B_claimed":False,"raw_lambda_global_E4_invariance_claimed":False,
      "presentation_layers":{"Gamma_full_Cayley_relations":6318,"x_y_action_relations":104,
        "complete_Q0_relations":19,"Q0_relator_defects_normally_generate_Gamma":True,
        "mu_is_homomorphism_on_joint_kernel":True}}
    require(receipt["theorem_boundary"]==expected_boundary,"checker theorem boundary")
    if closed:
        require(receipt["reason"]=="joint_kernel_presentation_potential_zero" and
                receipt["claim"]=="fixed_prefix_whole_joint_kernel_qstar_closed" and
                receipt["claim_flags"]["whole_joint_kernel_fixed_prefix_closed"] is True and
                receipt["claim_flags"]["new_qstar_direction_found"] is False,"checker CLOSED claim")
    else:
        require(receipt["reason"]=="defining_relation_nonzero" and
                receipt["claim"]=="positive_new_fixed_prefix_qstar_direction" and
                receipt["claim_flags"]["new_qstar_direction_found"] is True and
                receipt["claim_flags"]["whole_joint_kernel_fixed_prefix_closed"] is False,
                "checker ACTIVE claim")
    require(receipt["partial"]=={} and isinstance(receipt["performance"],dict),"checker completed shape")
    tick("checker complete",True);return receipt


def self_test()->None:
    require(digest_obj(FACTOR_PAYLOAD)==FACTOR_PAYLOAD_SHA and
            digest_obj(complete_relators(type("Toy",(),{
              "reduce_word":staticmethod(lambda word:_toy_reduce(word)),
              "inv_word":staticmethod(lambda word:[-x for x in reversed(word)]),
              "commutator":staticmethod(lambda a,b:_toy_reduce([-x for x in reversed(a)]+[-x for x in reversed(b)]+list(a)+list(b)))})()))==COMPLETE_RELATORS_SHA,
            "checker selftest manifests")
    require(fp_order([[1,1],[2,2,2],[1,2,1,2]])==6,"checker selftest SymPy S3")
    # Independent nonabelian packed Cayley fixture through the production decoder.
    a=(2,1,3);b=(2,3,1);generators=[a,b]
    states=enumerate_perm_group(generators);ids={state:i for i,state in enumerate(states)}
    transitions=[[ids[p_mul(state,g)]+1 for g in generators] for state in states]
    parents=[0];parent_generators=[0]
    for state in range(1,6):
        found=None
        for parent,row in enumerate(transitions[:state]):
            for generator,target in enumerate(row):
                if target==state+1:found=(parent+1,generator+1);break
            if found is not None:break
        require(found is not None,"checker selftest S3 section")
        parents.append(found[0]);parent_generators.append(found[1])
    raw=b"".join(bytes(state) for state in states)
    toy={"transitions":pack_u16(x for row in transitions for x in row),
      "section_parent_states":pack_u16(parents),
      "section_parent_generators":pack_u8(parent_generators),
      "canonical_states":{**pack_bytes(raw,"state-major exact blobs: E3 then 31 E4"),
        "state_count":6,"factor_widths_bytes":[3],"row_width_bytes":3},
      "state_rows_sha256":digest_obj([[bytes(state).hex()] for state in states]),
      "transition_rows_sha256":digest_obj([[x-1 for x in row] for row in transitions])}
    validate_packed_cayley(toy,6,2)
    for mutation in ("transition","section","state"):
        bad=json.loads(json.dumps(toy))
        if mutation=="transition":
            values=decode_u16(bad["transitions"],"checker toy transition")
            values[0]=1;bad["transitions"]=pack_u16(values)
            bad["transition_rows_sha256"]=digest_obj(
                [[x-1 for x in values[2*i:2*i+2]] for i in range(6)])
        elif mutation=="section":
            values=decode_u16(bad["section_parent_states"],"checker toy section")
            values[1]=2;bad["section_parent_states"]=pack_u16(values)
        else:
            value=bytearray(base64.b64decode(bad["canonical_states"]["base64"]))
            value[3:6]=value[0:3]
            bad["canonical_states"].update(pack_bytes(
                bytes(value),"state-major exact blobs: E3 then 31 E4"))
            bad["state_rows_sha256"]=digest_obj(
                [[bytes(value[3*i:3*i+3]).hex()] for i in range(6)])
        try:validate_packed_cayley(bad,6,2)
        except RuntimeError:pass
        else:raise RuntimeError("checker Cayley mutation "+mutation)
    pins={"task_sha256":TASK_SHA,"157ed_producer_sha256":PREV_PRODUCER_SHA,
      "157ed_checker_sha256":PREV_SHA,"157ed_driver_sha256":PREV_DRIVER_SHA,
      "157ed_task_sha256":PREV_TASK_SHA,"q3_artifact_sha256":Q3_SHA}
    flags={"whole_joint_kernel_fixed_prefix_closed":False,
      "new_qstar_direction_found":False,"full_D2_claimed":False,
      "full_H3_claimed":False,"lift_nonexistence_claimed":False,
      "B4_A_claimed":False,"B4_B_claimed":False}
    fixture={key:{} for key in TOP_KEYS};fixture.update({"schema":SCHEMA,
      "task_sha256":TASK_SHA,"terminal_token":"B345_JOINT_KERNEL_QSTAR_UNKNOWN_INPUT",
      "status":"B345_JOINT_KERNEL_QSTAR_UNKNOWN_INPUT",
      "reason":"authenticated_external_input","claim":"none","fixed_prefix_only":True,
      "claim_flags":flags,"pins":pins,"source_hashes":{
       "producer_path":PRODUCER.as_posix(),"producer_sha256":PRODUCER_SHA},"partial":{}})
    validate_envelope(fixture)
    resource=json.loads(json.dumps(fixture));resource.update({
      "terminal_token":"B345_JOINT_KERNEL_QSTAR_UNKNOWN_RESOURCE",
      "status":"B345_JOINT_KERNEL_QSTAR_UNKNOWN_RESOURCE","reason":"toy_cap",
      "partial":{"phase":"toy","resource":{"cap_key":"toy_cap",
       "cap_reason":"toy_cap","cap_limit":3,"observed_count":4,
       "trigger_relation":"gt"}}})
    validate_envelope(resource)
    closed=json.loads(json.dumps(fixture));closed.update({
      "terminal_token":"B345_JOINT_KERNEL_QSTAR_CLOSED",
      "status":"B345_JOINT_KERNEL_QSTAR_CLOSED",
      "reason":"joint_kernel_presentation_potential_zero",
      "claim":"fixed_prefix_whole_joint_kernel_qstar_closed"})
    closed["claim_flags"]["whole_joint_kernel_fixed_prefix_closed"]=True
    validate_envelope(closed)
    active=json.loads(json.dumps(fixture));active.update({
      "terminal_token":"B345_JOINT_KERNEL_QSTAR_ACTIVE",
      "status":"B345_JOINT_KERNEL_QSTAR_ACTIVE","reason":"defining_relation_nonzero",
      "claim":"positive_new_fixed_prefix_qstar_direction"})
    active["claim_flags"]["new_qstar_direction_found"]=True
    validate_envelope(active)
    for mutation in ("extra","claim","resource_reason"):
        bad=json.loads(json.dumps(resource if mutation=="resource_reason" else fixture))
        if mutation=="extra":bad["extra"]=1
        elif mutation=="claim":bad["claim"]="global"
        else:bad["reason"]="forged"
        try:validate_envelope(bad)
        except RuntimeError:pass
        else:raise RuntimeError("checker envelope mutation "+mutation)
    print("D972_B345_JOINT_KERNEL_QSTAR_CHECKER_SELFTEST_PASS "
          "factor_sympy=S3 nonabelian_fixture=S3 cayley_mutations=3 "
          "terminals=4 schema_mutations=3",flush=True)


def _toy_reduce(word:Iterable[int])->list[int]:
    out=[]
    for x in word:
        if out and out[-1]==-x:out.pop()
        else:out.append(x)
    return out


def main()->int:
    parser=argparse.ArgumentParser();parser.add_argument("q3",nargs="?")
    parser.add_argument("receipt",nargs="?");parser.add_argument("remaining_seconds",nargs="?",type=float,default=18000.0)
    parser.add_argument("--self-test",action="store_true");args=parser.parse_args()
    if args.self_test:self_test();return 0
    require(args.q3 is not None and args.receipt is not None,"checker arguments")
    check_receipt((ROOT/Path(args.q3)).resolve(),(ROOT/Path(args.receipt)).resolve(),args.remaining_seconds)
    print("D972_B345_JOINT_KERNEL_QSTAR_CHECKER_PASS",flush=True);return 0


if __name__=="__main__":raise SystemExit(main())
