#!/usr/bin/env python3
"""Decision-first grade-one probe.

This is deliberately a thin consumer of the frozen v3 producer.  It reads
sealed prepare/block states, routes the registered lower-first stream with
v3's vectorized PackedEchelon, reduces the target, and seals only the finite
membership decision.
"""
from __future__ import annotations
import argparse, bisect, hashlib, importlib.util, json, os, sys, time
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]; V3_PATH=ROOT/"search/d972_r07_a0_first_rung_grade1_v3.py"
sys.path.insert(0,str(V3_PATH.parent))
_spec=importlib.util.spec_from_file_location("grade1_v3_frozen",V3_PATH)
if _spec is None or _spec.loader is None: raise RuntimeError("v3_import")
v3=importlib.util.module_from_spec(_spec); _spec.loader.exec_module(v3)
V3_PRODUCER_DIGEST="bf872b30149e1351762b243d590d7a1f876e048b92a053d8f9c17bba5c45bcff"
V2_PRODUCER_DIGEST=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
DECISION_SCHEMA="d972.r07.a0.first-rung-grade1.decision.v2"

def atomic(path:Path,data:bytes)->None:
    tmp=path.with_name(path.name+".tmp")
    try:
        tmp.write_bytes(data)
        with tmp.open("r+b") as f: os.fsync(f.fileno())
        os.replace(tmp,path)
    except Exception:
        try: tmp.unlink()
        except FileNotFoundError: pass
        raise
def seal(d:Path,body:dict)->str:
    head=d/"decision-v2.HEAD"
    if head.exists(): raise RuntimeError("decision_head_exists")
    raw=v3.canonical_json(body); digest=v3.sha256_bytes(raw); atomic(d/f"decision-v2.{digest}.json",raw)
    atomic(head,v3.canonical_json({"schema":DECISION_SCHEMA+".head","stem":"decision-v2","body_sha256":digest}))
    return digest
def limits(started:float,phase:str)->None:
    seconds=float(os.environ.get("TASK595_SECONDS","21600")); rss=int(os.environ.get("TASK595_MAX_RSS",str(8*1024**3)))
    if time.monotonic()-started>seconds: raise RuntimeError(f"UNKNOWN_RESOURCE:{phase}:time_cap")
    current=v3.rss_bytes()
    if current and current>rss: raise RuntimeError(f"UNKNOWN_RESOURCE:{phase}:rss_cap:{current}")
def progress(obj:dict)->None:
    print(json.dumps(obj,sort_keys=True),flush=True)
def accept_already_reduced(owner,remainder,reductions):
    """v3 insert tail, for a remainder already reduced by the same owner."""
    nonzero=v3.np.flatnonzero(remainder)
    if not len(nonzero): return {"accepted":False,"reductions":reductions}
    byte_index=int(nonzero[0]); lead=4*byte_index+int(v3._PACKED_FIRST[int(remainder[byte_index])]); coefficient=owner.coefficient(remainder,lead); scale=1 if coefficient==1 else 2; normalized=remainder if scale==1 else v3._PACKED_SCALE2[remainder]; pivot=len(owner.rows)
    owner.rows.append(normalized.copy()); owner.leads.append(lead); position=bisect.bisect_left(owner._ordered_keys,(lead,pivot)); owner._ordered_keys.insert(position,(lead,pivot)); owner.ordered_pivots.insert(position,pivot); owner.lead_to_pivot[lead]=pivot
    return {"accepted":True,"pivot":pivot,"lead":lead,"leading_coefficient":coefficient,"scale":scale,"reductions":reductions}
def check_accept_equivalence()->None:
    seed=v3.np.array([1,0,0,0,0,0,0,0],dtype=v3.np.uint8)
    for row,seeded in ((v3.np.array([2,0,0,0,0,0,0,0],dtype=v3.np.uint8),False),(seed,True)):
        a=v3.PackedEchelon(8); b=v3.PackedEchelon(8)
        if seeded: a.insert(seed); b.insert(seed)
        packed=v3.pack_trits(row); rem,reductions=b.reduce_packed(packed); left=accept_already_reduced(a,rem,reductions); right=b.insert(row); assert left==right and a.matrix_bytes()==b.matrix_bytes()
def probe(state_dir:Path)->dict:
    d=v3.ensure_external_state_dir(state_dir); started=time.monotonic()
    if hashlib.sha256(V3_PATH.read_bytes()).hexdigest()!=V3_PRODUCER_DIGEST: raise RuntimeError("UNKNOWN_INPUT:v3_hash")
    _,receipt=v3.load_pinned_inputs(); prepare,prepare_digest=v3.read_sealed_state(d,"prepare")
    v3.validate_prepare_state(d,prepare,receipt,fixture=False,authenticate_residual=True,authenticate_old=True,authenticate_packets=range(4))
    blocks=[v3.read_sealed_state(d,f"block-{i}",prepare_digest) for i in range(4)]
    old_ranks=[int(x["lower_basis_blob"]["rows"]) for x in prepare.get("old_blocks",[])]; block_ranks=[int(x[0]["rank"]) for x in blocks]
    if old_ranks!=[505,503,503,503] or block_ranks!=[1509,1512,1512,1512]: raise RuntimeError("UNKNOWN_INPUT:rank_receipt")
    for i,(body,_) in enumerate(blocks): v3.validate_block_state(d,body,prepare,prepare_digest,i,authenticate_basis=True)
    context=v3.context_for_state(prepare); lower=v3.PackedEchelon(v3.PHYSICAL_LOWER_WIDTH); grade=v3.PackedEchelon(v3.PHYSICAL_GRADE_WIDTH)
    lower_grade=[]; logical=0; lower_offers=grade_offers=0
    def route(lower_row,grade_row,aux):
        nonlocal logical,lower_offers,grade_offers
        if logical==8058: progress({"marker":"LAST_LOGICAL_ROW_BEGIN","logical":logical+1})
        lower_offers += 1
        physical_lower,physical_grade=v3.aggregate_pair(context,lower_row,grade_row,aux)
        rem,reductions=lower.reduce_packed(v3.pack_trits(physical_lower)); companion=physical_grade.copy()
        for earlier,coefficient in reductions: v3._add_mod3(companion,lower_grade[int(earlier)],-int(coefficient))
        if v3.unpack_trits(rem,v3.PHYSICAL_LOWER_WIDTH).any():
            inserted=accept_already_reduced(lower,rem,reductions)
            if not inserted["accepted"]: raise RuntimeError("lower_insert_disagreement")
            if int(inserted["scale"])==2: companion[:]=(2*companion.astype("uint16"))%3
            lower_grade.append(companion)
        else:
            grade.insert(companion); grade_offers+=1
        logical+=1
        if logical%256==0: progress({"logical":logical,"lower_rank":len(lower.rows),"grade_rank":len(grade.rows),"phase":"route"})
        limits(started,"route")
    for old in prepare.get("old_blocks",[]):
        char=int(old["character_index"]); lb=old["lower_basis_blob"]; lg=old["lifted_grade_blob"]
        lower_data=v3.read_blob(d,lb); lift_data=v3.read_blob(d,lg); rank=int(lb["rows"])
        lower_matrix=v3.np.frombuffer(lower_data,dtype=v3.np.uint8).reshape(rank,v3.LOWER_ECHELON_WIDTH//4)
        lift_matrix=v3.np.frombuffer(lift_data,dtype=v3.np.uint8).reshape(rank,v3.SOURCE_TOTAL_WIDTH//4)
        for pivot in range(rank):
            lr=v3.unpack_trits(lower_matrix[pivot],v3.LOWER_ECHELON_WIDTH); ol=v3.np.zeros((4,v3.SOURCE_BASE_WIDTH),dtype=v3.np.uint8); ol[char]=lr[:v3.SOURCE_BASE_WIDTH]
            og=v3.unpack_trits(lift_matrix[pivot],v3.SOURCE_TOTAL_WIDTH).reshape(4,v3.SOURCE_BLOCK_WIDTH)
            route(ol,og,lr[v3.SOURCE_BASE_WIDTH:])
    if logical!=2014: raise RuntimeError(f"UNKNOWN_INPUT:old_logical:{logical}")
    for block,(body,_) in enumerate(blocks):
        owner=v3.load_block_owner(d,body)
        for pivot in range(len(owner.rows)):
            if logical==8058: progress({"marker":"LAST_LOGICAL_ROW_BEGIN","logical":logical+1})
            grade.insert(v3.aggregate_pure_grade(context,block,owner.dense_row(pivot))); grade_offers+=1; logical+=1
            if logical%256==0: progress({"logical":logical,"lower_rank":len(lower.rows),"grade_rank":len(grade.rows),"phase":"route"})
            limits(started,"route")
    if logical!=8059: raise RuntimeError(f"UNKNOWN_INPUT:logical_cursor:{logical}")
    progress({"marker":"LAST_LOGICAL_ROW_END","logical":logical})
    progress({"marker":"TARGET_REDUCTION_BEGIN","logical":logical})
    residual_data=v3.read_blob(d,prepare["residual_blob"]); residual=v3.unpack_trits(v3.np.frombuffer(residual_data,dtype=v3.np.uint8),v3.PHYSICAL_GRADE_WIDTH)
    remainder,coefficients=grade.reduce_packed(v3.pack_trits(residual)); member=not bool(v3.np.any(remainder)); limits(started,"target")
    progress({"marker":"TARGET_REDUCTION_END","member":member,"grade_rank":len(grade.rows)})
    basis_blob=v3.write_blob(d,"decision-v2-grade-basis",grade.matrix_bytes(),rows=len(grade.rows),width=v3.PHYSICAL_GRADE_WIDTH,encoding="base3-four-trits-per-byte")
    rem_bytes=remainder.tobytes(); rem_blob=v3.write_blob(d,"decision-v2-remainder",rem_bytes,rows=1,width=v3.PHYSICAL_GRADE_WIDTH,encoding="base3-four-trits-per-byte")
    block_digests=[digest for _,digest in blocks]; body={"schema":DECISION_SCHEMA,"phase":"decision","terminal":"GRADE1_DECISION_MEMBER" if member else "GRADE1_DECISION_NONMEMBER","prepare_sha256":prepare_digest,"block_sha256":block_digests,"producer_sha256":V2_PRODUCER_DIGEST,"v3_producer_sha256":V3_PRODUCER_DIGEST,"logical_cursor":logical,"old_ranks":old_ranks,"block_ranks":block_ranks,"old_logical_count":2014,"block_logical_count":6045,"lower_offer_count":lower_offers,"grade_offer_count":grade_offers,"lower_rank":len(lower.rows),"grade_rank":len(grade.rows),"grade_pivot_leads":[int(x) for x in grade.leads],"basis_receipt":basis_blob,"residual_receipt":prepare["residual_blob"],"remainder_receipt":rem_blob,"residual_sha256":v3.sha256_bytes(residual.tobytes()),"remainder_sha256":v3.sha256_bytes(rem_bytes),"remainder_support":int(v3.np.count_nonzero(v3.unpack_trits(remainder,v3.PHYSICAL_GRADE_WIDTH))),"remainder_packed_support":[int(i) for i in v3.np.flatnonzero(remainder)],"member_coefficients":coefficients if member else [],"elapsed_seconds":time.monotonic()-started}
    digest=seal(d,body); progress({"marker":"DECISION_SEAL_DONE","decision_sha256":digest,"terminal":body["terminal"]}); return body
def fixture(state_dir:Path, nonmember:bool=False)->dict:
    """Tiny protocol-only fixture; it never substitutes for the real probe."""
    check_accept_equivalence(); d=Path(state_dir); d.mkdir(parents=True,exist_ok=True); owner=v3.PackedEchelon(8)
    owner.insert(v3.np.array([1,0,0,0,0,0,0,0],dtype=v3.np.uint8)); owner.insert(v3.np.array([0,1,0,0,0,0,0,0],dtype=v3.np.uint8))
    progress({"logical":2,"lower_rank":0,"grade_rank":2,"phase":"route"}); progress({"marker":"LAST_LOGICAL_ROW_BEGIN","logical":2}); progress({"marker":"LAST_LOGICAL_ROW_END","logical":2}); progress({"marker":"TARGET_REDUCTION_BEGIN","logical":2})
    target=v3.np.array([0,0,1,0,0,0,0,0],dtype=v3.np.uint8) if nonmember else v3.np.array([1,1,0,0,0,0,0,0],dtype=v3.np.uint8); remainder,co=owner.reduce_packed(v3.pack_trits(target)); progress({"marker":"TARGET_REDUCTION_END","member":not bool(v3.np.any(remainder)),"grade_rank":2})
    basis=v3.write_blob(d,"decision-v2-grade-basis",owner.matrix_bytes(),rows=2,width=8,encoding="base3-four-trits-per-byte"); rem=v3.write_blob(d,"decision-v2-remainder",remainder.tobytes(),rows=1,width=8,encoding="base3-four-trits-per-byte")
    body={"schema":DECISION_SCHEMA,"phase":"decision","terminal":"GRADE1_DECISION_NONMEMBER" if nonmember else "GRADE1_DECISION_MEMBER","prepare_sha256":"0"*64,"block_sha256":["0"*64]*4,"producer_sha256":V2_PRODUCER_DIGEST,"v3_producer_sha256":V3_PRODUCER_DIGEST,"logical_cursor":2,"lower_offer_count":0,"grade_offer_count":2,"lower_rank":0,"grade_rank":2,"grade_pivot_leads":owner.leads,"basis_receipt":basis,"residual_receipt":rem,"remainder_receipt":rem,"residual_sha256":v3.sha256_bytes(remainder.tobytes()),"remainder_sha256":v3.sha256_bytes(remainder.tobytes()),"remainder_support":int(v3.np.count_nonzero(remainder)),"remainder_packed_support":[int(i) for i in v3.np.flatnonzero(remainder)],"member_coefficients":co if not nonmember else [],"elapsed_seconds":0.0}; digest=seal(d,body); progress({"marker":"DECISION_SEAL_DONE","decision_sha256":digest,"terminal":body["terminal"]}); return body
def main()->int:
    ap=argparse.ArgumentParser(); modes=ap.add_mutually_exclusive_group(required=True); modes.add_argument("--probe",type=Path); modes.add_argument("--fixture",type=Path); ap.add_argument("--nonmember",action="store_true"); a=ap.parse_args()
    try: body=probe(a.probe) if a.probe is not None else fixture(a.fixture,a.nonmember); progress({"phase":"decision","terminal":body["terminal"]}); return 0
    except RuntimeError as exc:
        msg=str(exc); kind="UNKNOWN_RESOURCE" if msg.startswith("UNKNOWN_RESOURCE") else "UNKNOWN_INPUT"; progress({"phase":"decision","status":kind,"error":msg}); return 3
if __name__=="__main__": raise SystemExit(main())
