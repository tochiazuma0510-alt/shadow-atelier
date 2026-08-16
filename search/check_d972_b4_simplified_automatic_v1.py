#!/usr/bin/env python3
"""Independent receipt checker for the simplified AutomaticStructure lane."""
from __future__ import annotations
import argparse, hashlib, json, re
from pathlib import Path
from typing import Any

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"search"/"certs"/"d972_b4_p2_magnus_input_v2_20260816.json"
WORDS=ROOT/"search"/"certs"/"d972_b4_word_key_artifact_v1_20260816.json"
SOURCE_SHA="c61b2b77131127aca83a8d7c56b7fdadd2d519b040ea4d91093622c813c2b4a9"
RELATOR_SHA="12fc1146dce5179c2b5fc44a3ceed6356a6b2c4835a564b55e9a9cd679fccd2e"
RHO=((-6,-5,-3),(3,),(5,),(-3,-2,-1),(-5,-4,-1),(1,))
NORM_SHA="ecf0cc8425bc24bdf6a8a352c223398221c4b179e09ee9a0bfe3dc888861683e"
WORDS_SHA="564a921be8114bdeb963f679c121e8d9aa90e148c65e95e393874fcba843e9f9"
TARGET_SHA="9c77e6768feb7ffe7143abf18f753af70e81b8e9cc792910c30ae0075d3b1d62"
TUPLE_SHA="32e78ca5b97cd8a6fa59a150dac77719c1b8cb527f0467570c4d284600465a91"
TRANSPORT_SHA="535d033019140e76cb9d3d7452b3e551c156f50ce74728b76bf6238d81806323"
SIMPLE_REL_SHA="6d614c32365753d62477cad8803420ffa58bcca0b5d18b0e5eadaaf6bf81b35a"
SIMPLE_NORM_SHA="127f029a2bafc7f8adf249b8c5f37cda594b105d3e1b567ba00400771cdca63e"
EXPECTED_SQ_ORDER=111577100832

def digest(x:Any)->str:
    return hashlib.sha256(json.dumps(x,separators=(",",":"),ensure_ascii=True).encode()).hexdigest()
def red(w:list[int])->list[int]:
    o=[]
    for x in w:
        if x==0 or abs(x)>6: raise ValueError("F6 drift")
        if o and o[-1]==-x:o.pop()
        else:o.append(x)
    return o
def rho(w:list[int])->list[int]:
    o=[]
    for x in w:
        a=list(RHO[abs(x)-1]); o.extend([-y for y in reversed(a)] if x<0 else a)
    return red(o)
def norm(w:list[int])->list[int]:
    c=red([(1 if x>0 else -1) if abs(x)==1 else (4 if x>0 else -4) for x in w]); orb=[]
    for _ in range(5): orb.append(c); c=rho(c)
    o=[]
    for a in reversed(orb):o=red(o+a)
    return o
def words(v:Any,n:int,width:int,name:str)->list[list[int]]:
    if not isinstance(v,list) or len(v)!=n:raise ValueError(name+" count")
    o=[]
    for w in v:
        if not isinstance(w,list) or any(not isinstance(x,int) or x==0 or abs(x)>width for x in w):raise ValueError(name+" shape")
        o.append(list(w))
    return o
def sub(w:list[int],images:list[list[int]])->list[int]:
    o=[]
    for x in w:
        a=list(images[abs(x)-1]); a=[-y for y in reversed(a)] if x<0 else a
        for y in a:
            if o and o[-1]==-y:o.pop()
            else:o.append(y)
    return o
def canonical()->list[list[int]]:
    sr=SOURCE.read_bytes(); wr=WORDS.read_bytes()
    if hashlib.sha256(sr).hexdigest()!=SOURCE_SHA or hashlib.sha256(wr).hexdigest()!=WORDS_SHA:raise ValueError("artifact SHA")
    so=json.loads(sr); wo=json.loads(wr)
    if so.get("schema")!="d972-b4-p2-magnus-input/v2" or so.get("rho_words")!=[list(x) for x in RHO] or so.get("all_relators_sha256")!=RELATOR_SHA or len(so.get("all_relators",[]))!=158:raise ValueError("source gate")
    if wo.get("schema")!="d972-b4-word-key-artifact/v1" or wo.get("count")!=972 or wo.get("source_target_key_digest")!=TARGET_SHA or wo.get("frozen_tuple_sha256")!=TUPLE_SHA:raise ValueError("word gate")
    rows=wo.get("rows"); out=[]
    if not isinstance(rows,list) or len(rows)!=972:raise ValueError("rows")
    normal=[]
    for i,row in enumerate(rows):
        m,key,w=row
        if w=="":
            if i not in (0,891):raise ValueError("empty row")
            w=[]
        normal.append([m,key,[int(x) for x in w]])
    if digest(normal)!=wo.get("canonical_bytes_sha256"):raise ValueError("row digest")
    out=[norm(row[2]) for row in normal]
    if digest(out)!=NORM_SHA:raise ValueError("norm digest")
    return out
def verify(tp:Path,r:dict[str,Any],norms:list[list[int]])->dict[str,Any]:
    tr=tp.read_bytes()
    if hashlib.sha256(tr).hexdigest()!=TRANSPORT_SHA:raise ValueError("transport SHA")
    t=json.loads(tr)
    if t.get("schema")!="d972-b4-u-simplified-transport/v1" or t.get("source_sha256")!=SOURCE_SHA or t.get("relator_sha256")!=RELATOR_SHA or t.get("roof_norm_sha256")!=NORM_SHA or t.get("simple_relators_sha256")!=SIMPLE_REL_SHA or t.get("simple_norms_sha256")!=SIMPLE_NORM_SHA:raise ValueError("transport pins")
    sr=words(t.get("simple_relators"),141,5,"relators"); sn=words(t.get("simple_norm_words"),972,5,"norms"); mp=words(t.get("original_to_simple_words"),6,5,"map")
    if digest(sr)!=SIMPLE_REL_SHA or digest(sn)!=SIMPLE_NORM_SHA or [sub(w,mp) for w in norms]!=sn:raise ValueError("transport replay")
    if r.get("schema")!="d972-b4-simplified-automatic/v1" or r.get("transport_receipt_sha256")!=TRANSPORT_SHA:raise ValueError("automatic schema/pin")
    for k,v in (("source_sha256",SOURCE_SHA),("relator_sha256",RELATOR_SHA),("roof_norm_sha256",NORM_SHA),("simple_relators_sha256",SIMPLE_REL_SHA),("simple_norms_sha256",SIMPLE_NORM_SHA)):
        if r.get(k)!=v:raise ValueError(k+" drift")
    status=str(r.get("status"))
    if status=="AUTOMATIC_STRUCTURE_FAILED" and r.get("reduced_norm_words")==[]:
        rw=[]
    else:
        rw=words(r.get("reduced_norm_words"),972,5,"reduced")
    if digest(rw)!=r.get("reduced_norm_words_sha256"):raise ValueError("reduced digest")
    empty=sum(not w for w in rw)
    if r.get("empty_count")!=empty:raise ValueError("empty count")
    final="UNKNOWN_AUTOMATIC_FAILURE"
    size_status=r.get("rws_size_status")
    size_value=r.get("rws_size")
    size_match=r.get("rws_size_matches_expected")
    if r.get("expected_sq_order")!=EXPECTED_SQ_ORDER:raise ValueError("expected SQ order drift")
    if size_status=="COMPUTED":
        if type(size_value) is not int and size_value not in ("infinity","unknown"):
            raise ValueError("RWS size type")
        computed_match=type(size_value) is int and size_value==EXPECTED_SQ_ORDER
        if size_match is not computed_match:raise ValueError("RWS size match drift")
    elif size_match is True:
        raise ValueError("RWS size skipped but marked matching")
    if status=="B4_B_CANDIDATE_PENDING_REPLAY":
        if r.get("automatic_success") is not True or r.get("automatic_axiom_checked") is not True:
            raise ValueError("automatic success/axiom gate")
        if size_status!="COMPUTED":raise ValueError("RWS size missing on B candidate")
        names=r.get("automaton_names"); states=r.get("automaton_states"); shas=r.get("automaton_sha256")
        paths=r.get("automaton_paths"); bindings=r.get("automaton_bindings")
        expected_names=["wa","diff1","diff2"]
        expected_bindings=["D972SAWA","D972SADiff1","D972SADiff2"]
        if isinstance(names,list) and len(names)==4 and names[3]=="reduction":
            expected_names.append("reduction"); expected_bindings.append("D972SAReduction")
        if names!=expected_names or bindings!=expected_bindings or not isinstance(states,list) or len(states)!=len(expected_names) or any(not isinstance(x,int) or x<=0 for x in states) or not isinstance(shas,list) or len(shas)!=len(expected_names) or any(not isinstance(x,str) or len(x)!=64 for x in shas) or not isinstance(paths,list) or len(paths)!=len(expected_names) or any(not isinstance(x,str) or not x for x in paths) or not isinstance(r.get("kbmag_package_version"),str) or not r.get("kbmag_package_version"):
            raise ValueError("automaton receipt gate")
        for path, expected, expected_states in zip(paths, shas, states):
            raw_fsa=Path(path).read_bytes()
            if hashlib.sha256(raw_fsa).hexdigest()!=expected:
                raise ValueError("automaton file digest drift")
            text_fsa=raw_fsa.decode("utf-8")
            match=re.search(r"states\s*:=\s*\[([^]]*)\]", text_fsa, re.S)
            if match is None:
                raise ValueError("automaton state ledger missing")
            state_text=match.group(1).strip()
            if state_text.startswith("1.."):
                parsed_states=int(state_text[3:].strip())
            else:
                parsed_states=len([x for x in state_text.split(",") if x.strip()])
            if parsed_states!=expected_states:
                raise ValueError("automaton state count drift")
        final="B4_B_CANDIDATE_PENDING_REPLAY_EQUAL_ORDER" if size_match is True else "B4_B_CANDIDATE_PENDING_REPLAY"
    elif status=="AUTOMATIC_ALL_EMPTY_CANDIDATE":final="UNKNOWN_AUTOMATIC_ALL_EMPTY_AXIOM_CANDIDATE"
    elif status=="AUTOMATIC_NONZERO_REDUCED_WORDS":final="UNKNOWN_AUTOMATIC_NONZERO"
    return {"schema":"d972-b4-simplified-automatic-independent-check/v1","status":final,"norm_count":972,"empty_count":empty,"transport_words_replayed":True,"automatic_receipt_replayed":True,"automaton_files_replayed":status=="B4_B_CANDIDATE_PENDING_REPLAY","rws_size_status":size_status,"rws_size":size_value,"expected_sq_order":EXPECTED_SQ_ORDER,"rws_size_matches_expected":size_match,"terminal_claim":False}
def main()->int:
    p=argparse.ArgumentParser();p.add_argument("--receipt",type=Path,required=True);p.add_argument("--transport",type=Path,required=True);p.add_argument("--output",type=Path,required=True);a=p.parse_args()
    r=verify(a.transport.resolve(),json.loads(a.receipt.resolve().read_text()),canonical()); raw=a.receipt.resolve().read_bytes();r["automatic_receipt_sha256"]=hashlib.sha256(raw).hexdigest();a.output.resolve().write_text(json.dumps(r,sort_keys=True,indent=2)+"\n",encoding="utf-8");print(json.dumps(r,sort_keys=True));return 2
if __name__=="__main__":raise SystemExit(main())
