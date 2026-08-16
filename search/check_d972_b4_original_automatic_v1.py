#!/usr/bin/env python3
"""Independent checker for the direct 6-generator AutomaticStructure lane."""
from __future__ import annotations
import argparse, hashlib, json, re
from pathlib import Path
from typing import Any

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"search/certs/d972_b4_p2_magnus_input_v2_20260816.json"
WORDS=ROOT/"search/certs/d972_b4_word_key_artifact_v1_20260816.json"
SOURCE_SHA="c61b2b77131127aca83a8d7c56b7fdadd2d519b040ea4d91093622c813c2b4a9"
WORDS_SHA="564a921be8114bdeb963f679c121e8d9aa90e148c65e95e393874fcba843e9f9"
RELATOR_SHA="12fc1146dce5179c2b5fc44a3ceed6356a6b2c4835a564b55e9a9cd679fccd2e"
RHO=((-6,-5,-3),(3,),(5,),(-3,-2,-1),(-5,-4,-1),(1,))
RHO_SHA="23db316e11e6486e0475b8425ff8ea6666941b5bff0943bf872e39761d0398ed"
ROOF_SHA="3015b4e00a02ca2a9d6183dad4cb7ddabfd21ef03828837198aa96b2dc3461f8"
NORM_SHA="ecf0cc8425bc24bdf6a8a352c223398221c4b179e09ee9a0bfe3dc888861683e"
TARGET_SHA="9c77e6768feb7ffe7143abf18f753af70e81b8e9cc792910c30ae0075d3b1d62"
TUPLE_SHA="32e78ca5b97cd8a6fa59a150dac77719c1b8cb527f0467570c4d284600465a91"
EXPECTED_SQ_ORDER=111577100832

def digest(x:Any)->str:
    return hashlib.sha256(json.dumps(x,separators=(",",":"),ensure_ascii=True).encode()).hexdigest()
def red(w:list[int])->list[int]:
    out=[]
    for x in w:
        if x==0 or abs(x)>6: raise ValueError("F6 word drift")
        if out and out[-1]==-x: out.pop()
        else: out.append(x)
    return out
def rho(w:list[int])->list[int]:
    out=[]
    for x in w:
        a=list(RHO[abs(x)-1]); out.extend([-y for y in reversed(a)] if x<0 else a)
    return red(out)
def norm(w:list[int])->list[int]:
    j=red([(1 if x>0 else -1) if abs(x)==1 else (4 if x>0 else -4) for x in w])
    orbit=[]; v=j
    for _ in range(5): orbit.append(v); v=rho(v)
    out=[]
    for a in reversed(orbit): out=red(out+a)
    return out
def rows(v:Any,n:int,width:int,name:str)->list[list[int]]:
    if not isinstance(v,list) or len(v)!=n: raise ValueError(name+" count")
    out=[]
    for w in v:
        if not isinstance(w,list) or any(type(x) is not int or x==0 or abs(x)>width for x in w): raise ValueError(name+" shape")
        out.append(list(w))
    return out
def canonical()->tuple[list[list[int]],list[list[int]]]:
    sr=SOURCE.read_bytes(); wr=WORDS.read_bytes()
    if hashlib.sha256(sr).hexdigest()!=SOURCE_SHA or hashlib.sha256(wr).hexdigest()!=WORDS_SHA: raise ValueError("artifact SHA")
    so=json.loads(sr); wo=json.loads(wr)
    if so.get("schema")!="d972-b4-p2-magnus-input/v2" or so.get("rho_words")!=[list(x) for x in RHO] or so.get("rho_words_source")!="universal_v2_canonical" or so.get("all_relators_sha256")!=RELATOR_SHA: raise ValueError("source gate")
    rel=rows(so.get("all_relators"),158,6,"relators"); roof=rows(so.get("roof_words"),972,6,"source roofs")
    if digest(rel)!=RELATOR_SHA or digest(roof)!=ROOF_SHA: raise ValueError("source digest")
    if wo.get("schema")!="d972-b4-word-key-artifact/v1" or wo.get("count")!=972 or wo.get("source_target_key_digest")!=TARGET_SHA or wo.get("frozen_tuple_sha256")!=TUPLE_SHA: raise ValueError("word artifact gate")
    rawrows=wo.get("rows")
    if not isinstance(rawrows,list) or len(rawrows)!=972: raise ValueError("word rows")
    normal=[]; artifact_roof=[]
    for i,row in enumerate(rawrows):
        if not isinstance(row,list) or len(row)!=3: raise ValueError("row shape")
        m,key,w=row
        if w=="":
            if i not in (0,891): raise ValueError("unexpected empty row")
            w=[]
        w=rows([w],1,2,"word")[0]
        normal.append([m,key,w]); artifact_roof.append(w)
    if digest(normal)!=wo.get("canonical_bytes_sha256"): raise ValueError("word row digest")
    if artifact_roof!=roof: raise ValueError("source/artifact roof mismatch")
    norms=[norm(w) for w in artifact_roof]
    if digest(norms)!=NORM_SHA: raise ValueError("norm digest")
    return rel,norms
def verify(receipt:dict[str,Any],rel:list[list[int]],norms:list[list[int]])->dict[str,Any]:
    if receipt.get("schema")!="d972-b4-original-automatic/v1": raise ValueError("schema")
    for k,v in (("source_sha256",SOURCE_SHA),("word_artifact_sha256",WORDS_SHA),("relator_sha256",RELATOR_SHA),("rho_words_sha256",RHO_SHA),("roof_words_sha256",ROOF_SHA),("roof_norm_sha256",NORM_SHA)):
        if receipt.get(k)!=v: raise ValueError(k+" drift")
    if receipt.get("norm_count")!=972: raise ValueError("norm count")
    rw=receipt.get("reduced_norm_words")
    if not isinstance(rw,list) or len(rw)!=972: raise ValueError("reduced ledger")
    for w in rw:
        if not isinstance(w,list) or any(type(x) is not int or x==0 or abs(x)>6 for x in w): raise ValueError("reduced shape")
    if digest(rw)!=receipt.get("reduced_norm_words_sha256"): raise ValueError("reduced digest")
    empty=sum(not w for w in rw)
    if receipt.get("empty_count")!=empty: raise ValueError("empty count")
    size_status=receipt.get("rws_size_status"); size_value=receipt.get("rws_size"); size_match=receipt.get("rws_size_matches_expected")
    if receipt.get("expected_sq_order")!=EXPECTED_SQ_ORDER: raise ValueError("expected size drift")
    if size_status=="COMPUTED":
        if type(size_value) is not int and size_value not in ("infinity","unknown"): raise ValueError("size type")
        if size_match is not (type(size_value) is int and size_value==EXPECTED_SQ_ORDER): raise ValueError("size match")
    elif size_match is True: raise ValueError("size skipped but matching")
    status=str(receipt.get("status")); final="UNKNOWN_ORIGINAL_AUTOMATIC"
    names=receipt.get("automaton_names"); states=receipt.get("automaton_states"); shas=receipt.get("automaton_sha256"); paths=receipt.get("automaton_paths")
    if status=="B4_B_CANDIDATE_PENDING_REPLAY":
        if receipt.get("automatic_success") is not True or receipt.get("automatic_axiom_checked") is not True or size_status!="COMPUTED": raise ValueError("candidate gate")
        if names not in (["wa","diff1","diff2"],["wa","diff1","diff2","reduction"]): raise ValueError("automaton names")
        if not isinstance(states,list) or len(states)!=len(names) or any(type(x) is not int or x<=0 for x in states): raise ValueError("automaton states")
        if not isinstance(shas,list) or len(shas)!=len(names) or any(not isinstance(x,str) or len(x)!=64 for x in shas): raise ValueError("automaton hashes")
        if not isinstance(paths,list) or len(paths)!=len(names): raise ValueError("automaton paths")
        for path,expected,nstates in zip(paths,shas,states):
            raw=Path(path).read_bytes()
            if hashlib.sha256(raw).hexdigest()!=expected: raise ValueError("automaton SHA")
            m=re.search(rb"states\s*:=\s*\[([^]]*)\]",raw,re.S)
            if m is None: raise ValueError("automaton states ledger")
            txt=m.group(1).strip()
            got=int(txt[3:].strip()) if txt.startswith(b"1..") else len([x for x in txt.split(b",") if x.strip()])
            if got!=nstates: raise ValueError("automaton state drift")
        final="B4_B_CANDIDATE_PENDING_REPLAY_EQUAL_ORDER" if size_match is True else "B4_B_CANDIDATE_PENDING_REPLAY"
    elif status=="AUTOMATIC_ALL_EMPTY_SIZE_NOT_COMPUTED": final="UNKNOWN_ORIGINAL_ALL_EMPTY_SIZE_MISSING"
    elif status=="AUTOMATIC_NONZERO_REDUCED_WORDS": final="UNKNOWN_ORIGINAL_NONZERO"
    elif status=="AUTOMATIC_STRUCTURE_FAILED": final="UNKNOWN_ORIGINAL_AUTOMATIC_FAILURE"
    return {"schema":"d972-b4-original-automatic-independent-check/v1","status":final,"norm_count":972,"empty_count":empty,"canonical_norms_replayed":True,"automatic_receipt_replayed":True,"rws_size_status":size_status,"rws_size":size_value,"expected_sq_order":EXPECTED_SQ_ORDER,"rws_size_matches_expected":size_match,"terminal_claim":False}
def main()->int:
    p=argparse.ArgumentParser(); p.add_argument("--receipt",type=Path,required=True); p.add_argument("--output",type=Path,required=True); a=p.parse_args()
    rel,norms=canonical(); receipt=json.loads(a.receipt.resolve().read_text()); out=verify(receipt,rel,norms); out["receipt_sha256"]=hashlib.sha256(a.receipt.resolve().read_bytes()).hexdigest(); a.output.resolve().write_text(json.dumps(out,sort_keys=True,indent=2)+"\n",encoding="utf-8"); print(json.dumps(out,sort_keys=True)); return 2
if __name__=="__main__": raise SystemExit(main())
