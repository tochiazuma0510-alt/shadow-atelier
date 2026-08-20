"""Independent checker for the 157eg E4 full-D2 dual correlation."""
from __future__ import annotations

import argparse
import base64
import hashlib
import importlib.util
import json
import sys
import time
from array import array
from collections import defaultdict, deque
from pathlib import Path
from typing import Any, Callable, Iterable, Sequence


ROOT = Path(__file__).resolve().parents[1]
TASK = Path("sol/luna_task_157eg_b345_full_d2_dual_correlation.md")
TASK_SHA = "22b649c178ea1a821a5d67973b39c58f6a7395b6bc6a407a36a493f9ce19720e"
SCHEMA = "d972-b345-full-d2-dual-correlation/v1"
Q3_PATH = Path("ci/out/d972_b345_q3_chief_v1.json")
Q3_SHA = "3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72"
OUTPUT = Path("ci/out/d972_b345_full_d2_dual_correlation_v1.json")

PRODUCER = Path("search/d972_b345_full_d2_dual_correlation_v1.py")
PRODUCER_SHA = "6903b745be2c005c573d7a368beb826d5f411f0f4a353eeedf3a8cccbc9fde52"
ED_PRODUCER = Path("search/d972_b345_triple_cube_raw_lambda_census_v1.py")
ED_PRODUCER_SHA = "d4a290984ae8a93b6959f06d20c1de037b2814707778fba03c59ac87b2f736db"
ED_CHECKER = Path("search/check_d972_b345_triple_cube_raw_lambda_census_v1.py")
ED_CHECKER_SHA = "677aa1b69e4415da9629c34fcf0e469ad974cf3c888be7e768635bac50f672ce"
ED_DRIVER = Path("search/d972_b345_triple_cube_raw_lambda_census_gha_driver_v1.g")
ED_DRIVER_SHA = "29a31752d42bd3f5a0e7f27ca38495bdd54c9cc694d12ddf9fe637e8749975e9"
EE_PRODUCER = Path("search/d972_b345_joint_kernel_qstar_closure_v1.py")
EE_PRODUCER_SHA = "06ba6cf361957db3e339d48d14b3d4fbc689de9642e3f96273fbe8f3160e76dc"
EF_CHECKER = Path("search/check_d972_b345_joint_kernel_qstar_closure_v2.py")
EF_CHECKER_SHA = "5c3b03af26a47f00fbfbd8484e17c591c5399ac708e566506d726d5dbd03ba88"
EF_DRIVER = Path("search/d972_b345_joint_kernel_qstar_closure_gha_driver_v2.g")
EF_DRIVER_SHA = "8ff80ba97f3801daf28ad61b19d2f0a01572a5720c13578f11c56bf0d7ad26e7"
PREFIX_SOURCE = Path("search/d972_b345_seedspan_triple4_v1.py")
PREFIX_SOURCE_SHA = "fe18fc31fdf3f9416ebb829112ccbd514c27e6a8d30fe24691842865277a0b29"
EE_TASK = Path("sol/luna_task_157ee_b345_joint_kernel_qstar_closure.md")
EE_TASK_SHA = "64a32c0b7e3d4efc41ddb8e0e7036282b0b5430d9ab46bbfe125b588478a95d4"
EF_TASK = Path("sol/luna_task_157ef_b345_joint_kernel_checker_repair.md")
EF_TASK_SHA = "e626802b32e9577e35f5543b252830abdc4461b409972c9f5536ea29d8bb14ed"

PIN_SPECS = {
    "task": (TASK, TASK_SHA, 16187),
    "157ee_producer": (EE_PRODUCER, EE_PRODUCER_SHA, 67945),
    "157ef_checker": (EF_CHECKER, EF_CHECKER_SHA, 5942),
    "157ef_driver": (EF_DRIVER, EF_DRIVER_SHA, 3912),
    "157ed_producer": (ED_PRODUCER, ED_PRODUCER_SHA, 126942),
    "157ed_checker": (ED_CHECKER, ED_CHECKER_SHA, 97363),
    "157ed_driver": (ED_DRIVER, ED_DRIVER_SHA, 10223),
    "frozen_prefix_source": (PREFIX_SOURCE, PREFIX_SOURCE_SHA, 535219),
    "157ee_task": (EE_TASK, EE_TASK_SHA, 11226),
    "157ef_task": (EF_TASK, EF_TASK_SHA, 3235),
}
PREFIX_COUNTS = {"columns":362725,"pivots":362709,"dependent_columns":16,
    "live_sparse_entries":3090367,"row_tail_visits":2727658,
    "BFS_translations":32768,"directed_translations":207}
BASE_SUPPORTS=[8,6,8,6,4,8,12,6,4,8,6]
BASE_COMPONENTS=[10,12,18,10,12,14]
BASE_OCCURRENCE_SHA="3eacd6dc77d62c1799a55923d3c8d5313a37ceab8e78b58b07b45925a28f131d"
CAPS={"pair_attempts":8_388_608,
      "distinct_correlation_candidates":2_000_000,
      "packed_active_rows":2_000_000,
      "common_math_soft_deadline_seconds":18_000,
      "producer_soft_rss_bytes":4_831_838_208,
      "packed_receipt_bytes":268_435_456}
TERMINALS=frozenset({"B345_E4_FULL_D2_QSTAR_SEPARATOR",
    "B345_E4_FULL_D2_ACTIVE_TRANSLATION",
    "B345_E4_FULL_D2_UNKNOWN_RESOURCE",
    "B345_E4_FULL_D2_UNKNOWN_INPUT"})
PHASES=frozenset({"authenticated_input","fresh_immutable_prefix",
    "raw_lambda_oracle","base_columns","dual_correlation","section_witness",
    "receipt_serialization","complete"})
TOP_KEYS={"schema","task_sha256","terminal_token","status","reason","claim",
    "phase","pins","caps","upstream_caps","provenance","base_q3_replay",
    "normalized_inverse_fibre","directed_base_support","directed_surgery",
    "prefix","lambda_oracle","lambda_support","base_columns","correlation",
    "direct_canaries","state_no_mutation","section_witness","theorem_boundary",
    "resource_guards","partial","input_errors","performance"}
TIMED_PHASES=("authenticated_input","fresh_immutable_prefix",
    "raw_lambda_oracle","base_columns","dual_correlation","section_witness")

CHECKER_STARTED: float | None=None
CHECKER_DEADLINE: float | None=None
CHECKER_CHECKS=0


def require(value: Any, message: str) -> None:
    if not value: raise RuntimeError(message)


def sha_bytes(value: bytes) -> str: return hashlib.sha256(value).hexdigest()
def sha_obj(value: Any) -> str:
    return sha_bytes(json.dumps(value,sort_keys=True,separators=(",",":")).encode())
def sha_file(path: Path) -> str:
    h=hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda:stream.read(1<<20),b""): h.update(chunk)
    return h.hexdigest()


def validate_performance(row:dict[str,Any],token:str,phase:str)->None:
    require(set(row)=={"initial_remaining_seconds","elapsed_seconds",
        "remaining_seconds","checks","peak_rss_bytes","hit_reason",
        "receipt_bytes","phase_seconds","pair_loop_cadence",
        "pool_intern_calls_in_correlation",
        "full_sparse_vectors_materialized_in_correlation",
        "full_E4_enumerations"},"checker performance exact keys")
    initial=row["initial_remaining_seconds"];elapsed=row["elapsed_seconds"]
    remaining=row["remaining_seconds"]
    require(isinstance(initial,(int,float)) and not isinstance(initial,bool) and
        0<initial<=18_000 and isinstance(elapsed,(int,float)) and
        not isinstance(elapsed,bool) and elapsed>=0 and
        isinstance(remaining,(int,float)) and not isinstance(remaining,bool) and
        0<=remaining<=initial and abs((elapsed+remaining)-initial)<=1.0 and
        isinstance(row["checks"],int) and not isinstance(row["checks"],bool) and
        row["checks"]>=0 and isinstance(row["peak_rss_bytes"],int) and
        not isinstance(row["peak_rss_bytes"],bool) and row["peak_rss_bytes"]>=0 and
        isinstance(row["receipt_bytes"],int) and not isinstance(row["receipt_bytes"],bool)
        and row["receipt_bytes"]>=0 and row["pair_loop_cadence"]==4096 and
        row["pool_intern_calls_in_correlation"]==0 and
        row["full_sparse_vectors_materialized_in_correlation"]==0 and
        row["full_E4_enumerations"]==0,"checker performance numeric contract")
    if token in {"B345_E4_FULL_D2_QSTAR_SEPARATOR",
                 "B345_E4_FULL_D2_ACTIVE_TRANSLATION"}:expected=TIMED_PHASES
    elif token=="B345_E4_FULL_D2_UNKNOWN_INPUT":expected=()
    else:
        completed={"fresh_immutable_prefix":1,"raw_lambda_oracle":2,
            "base_columns":3,"dual_correlation":4,"section_witness":5,
            "receipt_serialization":6}
        require(phase in completed,"checker performance resource phase")
        expected=TIMED_PHASES[:completed[phase]]
    timings=row["phase_seconds"]
    require(isinstance(timings,dict) and set(timings)==set(expected) and
        all(isinstance(timings[name],(int,float)) and
            not isinstance(timings[name],bool) and timings[name]>=0
            for name in expected) and sum(timings.values())<=elapsed+1.0,
        "checker performance phase timings")


def tick(phase: str, force: bool=False) -> None:
    global CHECKER_CHECKS
    CHECKER_CHECKS+=1
    if not force and CHECKER_CHECKS&63: return
    require(CHECKER_DEADLINE is not None and time.monotonic()<CHECKER_DEADLINE,
            f"checker 18000s soft deadline: {phase}")


def pin_rows() -> dict[str,dict[str,Any]]:
    return {label:{"path":path.as_posix(),"sha256":digest,"bytes":size}
            for label,(path,digest,size) in PIN_SPECS.items()} | {
        "q3_artifact":{"path":Q3_PATH.as_posix(),"sha256":Q3_SHA,
            "bytes":((ROOT/Q3_PATH).stat().st_size if (ROOT/Q3_PATH).is_file()
                     else None)}}


def authenticate() -> None:
    for label,(path,digest,size) in PIN_SPECS.items():
        full=ROOT/path
        require(full.is_file() and full.stat().st_size==size and
                sha_file(full)==digest,f"checker pin {label}")
    require((ROOT/PRODUCER).is_file() and sha_file(ROOT/PRODUCER)==PRODUCER_SHA,
            "checker producer pin")


def load_ed_checker() -> Any:
    authenticate()
    spec=importlib.util.spec_from_file_location(
        "_d972_157eg_pinned_157ed_checker",ROOT/ED_CHECKER)
    require(spec is not None and spec.loader is not None,"157ed checker spec")
    require(spec.name not in sys.modules,"157ed checker module fresh")
    module=importlib.util.module_from_spec(spec);sys.modules[spec.name]=module
    try: spec.loader.exec_module(module)
    except BaseException:
        sys.modules.pop(spec.name,None);raise
    return module


def independent_upstream_caps(ed:Any)->dict[str,int]:
    rows={key:int(value) for key,value in ed.UPSTREAM_RESOURCE_CAPS.items()}
    for key in ("raw_lambda_recursion_edges",):
        require(key in ed.CAPS_157ED and isinstance(ed.CAPS_157ED[key],int),
                "checker reachable 157ed resource cap")
        if key in rows:
            require(rows[key]==int(ed.CAPS_157ED[key]),
                    "checker upstream cap overlap")
        rows[key]=int(ed.CAPS_157ED[key])
    return dict(sorted(rows.items()))


def validate_deadline_bridge(ed:Any,old:Any,absolute:float)->None:
    require(ed.CHECKER_DEADLINE is not None and
            ed.CHECKER_DEADLINE.deadline==absolute and
            0.0<ed.CHECKER_DEADLINE.initial_seconds<=18_000.0 and
            old.AFFINE_CAPS["producer_soft_timeout_seconds"]==18_000 and
            old.CHECKER_STARTED==absolute-18_000.0 and
            old.CHECKER_CHECKS==0,
            "checker inherited common deadline bridge")


def configure_deadline_bridge(ed:Any,old:Any)->None:
    require(CHECKER_DEADLINE is not None,"checker absolute deadline initialized")
    remaining=CHECKER_DEADLINE-time.monotonic()
    require(0.0<remaining<=18_000.0,"checker positive inherited remainder")
    adapter=ed.Deadline(remaining)
    adapter.deadline=CHECKER_DEADLINE
    ed.CHECKER_DEADLINE=adapter
    old.CHECKER_STARTED=CHECKER_DEADLINE-18_000.0
    old.CHECKER_CHECKS=0
    validate_deadline_bridge(ed,old,CHECKER_DEADLINE)


def theorem_boundary() -> dict[str,Any]:
    return {"pinned_E4_roof_only":True,"157ee_joint_kernel_only":True,
        "D2_acting_group_is_PB4_E4_not_joint_correction_J":True,
        "eleven_base_relators_are_orbit_representatives_by_definition":True,
        "prefix_generates_module_or_FC44_assumed":False,
        "coinvariant_shortcut_used":False,
        "full_D2_left_translate_correlation_complete":True,
        "alternate_roofs_exhausted":False,"full_H3_corrections_exhausted":False,
        "global_lift_nonexistence_claimed":False,"B4_A_claimed":False,
        "B4_B_claimed":False,"active_translation_is_not_a_lift":True,
        "producer_only_is_crosschecked":False}


def provenance_row()->dict[str,Any]:
    return {"run":"32359956713",
        "commit":"1696e7b44792b97c51a435d4160259462963c52d",
        "artifact_id":9403505687,
        "archive_sha256":
          "9fe43b570dd135c4f26c910dff983e0e58492bb3250beb4cbe01d7e8bcca1192",
        "receipt_sha256":
          "1c3ad7a7124cee152eb40968cf212c14641a9f8720063c85f70533864898d0df",
        "evidence_only_not_imported":True}


def validate_envelope(data: dict[str,Any], *, fixture: bool=False,
                      expected_upstream:dict[str,int]|None=None) -> None:
    require(set(data)==TOP_KEYS and data["schema"]==SCHEMA and
            data["task_sha256"]==TASK_SHA and
            data["terminal_token"]==data["status"] in TERMINALS and
            data["phase"] in PHASES,"checker envelope")
    if expected_upstream is None:
        require(fixture,"checker missing independent upstream registry")
        expected_upstream={}
    require(data["caps"]==CAPS and set(data["upstream_caps"])==
            {"registry","sha256"} and data["upstream_caps"]["registry"]==
            expected_upstream and data["upstream_caps"]["sha256"]==
            sha_obj(expected_upstream),"checker independent caps")
    require(data["theorem_boundary"]==theorem_boundary(),"checker boundary")
    require(data["provenance"]==provenance_row(),"checker fixed provenance")
    require(set(data["resource_guards"])==
            {"resource_hit","resource","atomic_partial"} and
            data["resource_guards"]["atomic_partial"] is True,
            "checker resource keys")
    if not fixture: require(data["pins"]==pin_rows(),"checker pin receipt")
    token=data["terminal_token"]
    math_fields=("base_q3_replay","normalized_inverse_fibre",
        "directed_base_support","directed_surgery","prefix","lambda_oracle",
        "lambda_support","base_columns","correlation","direct_canaries",
        "state_no_mutation","section_witness")
    normal_guard={"resource_hit":False,"resource":None,"atomic_partial":True}
    if token=="B345_E4_FULL_D2_QSTAR_SEPARATOR":
        require(data["correlation"].get("complete") is True and
                data["correlation"].get("active_count")==0 and
                data["section_witness"]=={} and data["claim"]==
                "qstar_separates_base_target6_from_full_D2_for_pinned_E4_roof" and
                data["reason"]=="complete_correlation_all_translates_zero" and
                data["phase"]=="complete" and data["resource_guards"]==normal_guard
                and data["partial"]=={} and data["input_errors"]==[] and
                all(data[name] for name in math_fields[:-1]) and
                data["performance"]["hit_reason"] is None,
                "checker separator terminal")
    elif token=="B345_E4_FULL_D2_ACTIVE_TRANSLATION":
        require(data["correlation"].get("complete") is True and
                data["correlation"].get("active_count",0)>0 and
                bool(data["section_witness"]) and data["claim"]==
                "first_active_full_D2_translation_exported_not_a_lift" and
                data["reason"]=="complete_correlation_has_nonzero_translation" and
                data["phase"]=="complete" and data["resource_guards"]==normal_guard
                and data["partial"]=={} and data["input_errors"]==[] and
                all(data[name] for name in math_fields) and
                data["performance"]["hit_reason"] is None,
                "checker active terminal")
    elif token=="B345_E4_FULL_D2_UNKNOWN_RESOURCE":
        row=data["resource_guards"]["resource"]
        require(data["claim"]=="none" and
                data["resource_guards"]["resource_hit"] is True and
                isinstance(row,dict) and row["cap_reason"]==row["cap_key"]==
                data["reason"] and row["phase"]==data["phase"] and
                row["comparator"] in {"gt","ge"} and
                data["partial"]=={"phase":row["phase"],"current":row["current"],
                    "correlation_published":False,"mathematical_claim":"none",
                    "rollback_required":False,"reason":row["cap_reason"]},
                "checker resource terminal")
        source=row["cap_source"]
        require(source in {"local","upstream"},"checker resource cap source")
        registry=CAPS if source=="local" else expected_upstream
        require(row["cap_key"] in registry and row["cap_limit"]==registry[row["cap_key"]],
                "checker closed resource registry")
        compare=(row["observed_count"]>row["cap_limit"] if row["comparator"]=="gt"
                 else row["observed_count"]>=row["cap_limit"])
        require(compare,"checker resource comparator")
        require(data["performance"]["hit_reason"]==data["reason"] and
                data["input_errors"]==[] and set(row)=={"cap_reason","cap_key",
                "cap_source","cap_limit","observed_count","comparator","phase","current"},
                "checker resource exact nested")
        completed={"fresh_immutable_prefix":2,"raw_lambda_oracle":5,
            "base_columns":7,"dual_correlation":8,"section_witness":8,
            "receipt_serialization":8}
        require(row["phase"] in completed,"checker resource phase registry")
        for index,name in enumerate(math_fields):
            require(bool(data[name])==(index<completed[row["phase"]]),
                    f"checker resource stage payload: {name}")
        current=row["current"]
        if row["cap_key"] in {"pair_attempts","distinct_correlation_candidates"}:
            require(set(current)=={"lambda_ordinal","base_component_ordinal"} and
                    all(isinstance(current[k],int) and current[k]>=1 for k in current),
                    "checker pair current")
        elif row["cap_key"]=="packed_active_rows":
            require(current=={"post_accumulation":True},"checker active current")
        else:require(current=={},"checker non-correlation current")
    else:
        require(token=="B345_E4_FULL_D2_UNKNOWN_INPUT" and data["claim"]=="none"
                and data["input_errors"] and
                data["reason"]=="authenticated_input_failure" and
                data["phase"]=="authenticated_input" and
                data["resource_guards"]==normal_guard and data["partial"]=={} and
                all(data[name]=={} for name in math_fields) and
                data["performance"]["hit_reason"] is None,
                "checker input terminal")
    validate_performance(data["performance"],token,data["phase"])


def blob(value: Any) -> bytes: return bytes(value[0])+bytes(value[1])


def digest_pool_values(values: Sequence[bytes]) -> str:
    digest=hashlib.sha256()
    for value in values:digest.update(value)
    return digest.hexdigest()


def validate_state_record(state:dict[str,Any],expected:dict[str,Any])->None:
    require(set(state)=={"before","after","exact_equal",
        "helper_signature_excludes_pool_basis_DAG_sections",
        "pool_ID_reuse_or_intern_calls","E4_cache_path_used"} and
        state["exact_equal"] is True and
        state["helper_signature_excludes_pool_basis_DAG_sections"] is True and
        state["pool_ID_reuse_or_intern_calls"]==0 and
        state["E4_cache_path_used"] is False and
        set(state["before"])==set(expected) and
        state["before"]==state["after"]==expected,
        "checker independent exact persistent state")


def uncached_ops(old: Any, quotient: Any) -> tuple[Callable[[Any,Any],Any],Callable[[Any],Any]]:
    def mul(left: Any,right: Any)->Any:
        return old.p_mul(left[0],right[0]), quotient.collector.collect(
            old.pc_word(left[1])+old.pc_word(right[1]))
    def inverse(value: Any)->Any:
        word=[]
        for i in range(quotient.collector.n,0,-1):
            for _ in range(value[1][i-1]):
                word.extend(old.pc_word(quotient.collector.inverses[i-1]))
        return old.p_inv(value[0]),quotient.collector.collect(word)
    return mul,inverse


def correlation_packed(rows: Iterable[tuple[bytes,int,int]],width:int)->bytes:
    out=bytearray()
    for translation,relator,scalar in rows:
        require(len(translation)==width and 1<=relator<=11 and scalar in (1,2),
                "checker packed row")
        out.extend(translation);out.append(relator);out.append(scalar)
    return bytes(out)


def translation_from_pair(g:Any,h:Any,*,mul:Callable[[Any,Any],Any],
                          inverse:Callable[[Any],Any],orientation:str,
                          inverse_h:Any|None=None)->Any:
    require(orientation in {"g_times_h_inverse","h_inverse_times_g",
        "g_inverse_times_h","right_action_solution"},
        "checker orientation registry")
    hinv=inverse(h) if inverse_h is None else inverse_h
    if orientation=="g_times_h_inverse":answer=mul(g,hinv)
    elif orientation=="h_inverse_times_g":answer=mul(hinv,g)
    elif orientation=="g_inverse_times_h":answer=mul(inverse(g),h)
    else:answer=mul(h,inverse(g))
    require(mul(answer,h)==g,"checker left translation t*h=g")
    return answer


def checker_lambda_support(oracle: Any,width:int)->dict[str,Any]:
    rows=[[int(c),value.hex(),int(a)] for (c,value),a in oracle.values.items()
          if int(a)%3]
    rows.sort(key=lambda r:(r[0],bytes.fromhex(r[1])))
    require(all(1<=r[0]<=6 and len(bytes.fromhex(r[1]))==width and r[2] in (1,2)
                for r in rows),"checker lambda rows")
    return {"rows":rows,"count":len(rows),
        "per_component":[sum(r[0]==c for r in rows) for c in range(1,7)],
        "ordered_sha256":sha_obj(rows),
        "order":"component then canonical E4 bytes",
        "zero_entries_covered_by_oracle_semantic_digest":True}


def checker_base_bundle(old: Any,e4: Any)->dict[str,Any]:
    public,private=old.checker_base_occurrences(e4)
    require(all(set(row)=={"relator_index","component","coefficient",
                "element_hex","section_word"} for row in public) and
            all(set(row)=={"relator_index","component","coefficient",
                "element_hex","section_word","_value"} for row in private),
            "checker base public/private shape")
    per_rel=[sum(r["relator_index"]==j for r in private) for j in range(1,12)]
    per_comp=[sum(r["component"]==c for r in private) for c in range(1,7)]
    require(len(private)==76 and per_rel==BASE_SUPPORTS and per_comp==BASE_COMPONENTS
            and sha_obj(public)==BASE_OCCURRENCE_SHA,"checker base ledger")
    return {"private_occurrences":private,"public":{"occurrences":public,
        "occurrence_count":76,"per_relator_counts":per_rel,
        "per_component_counts":per_comp,"ordered_sha256":BASE_OCCURRENCE_SHA,
        "quotient_identity_all":True,"D1_D2_zero_all":True,
        "private_fields_published":False,
        "order":"relator index, component, canonical E4 bytes"}}


def independent_correlation(support: Sequence[Sequence[Any]],
                            base: Sequence[dict[str,Any]], *, width:int,
                            unpack:Callable[[bytes],Any],mul:Callable[[Any,Any],Any],
                            inverse:Callable[[Any],Any],pack:Callable[[Any],bytes],
                            caps:dict[str,int]|None=None)->dict[str,Any]:
    """Checker-owned base-major organization; no producer helper/data."""
    limits=CAPS if caps is None else caps
    by_component:dict[int,list[tuple[Any,int]]]=defaultdict(list)
    for c,g_hex,a in support:
        by_component[int(c)].append((unpack(bytes.fromhex(str(g_hex))),int(a)))
    corr:dict[tuple[int,bytes],int]={};attempts=0
    for b_ord,row in enumerate(base,1):
        h_inv=inverse(row["_value"]);component=int(row["component"])
        for s_ord,(g,lam) in enumerate(by_component[component],1):
            require(attempts<limits["pair_attempts"],"checker pair cap precondition")
            attempts+=1;t=translation_from_pair(g,row["_value"],mul=mul,
                inverse=inverse,orientation="g_times_h_inverse",inverse_h=h_inv)
            t_blob=pack(t)
            require(len(t_blob)==width,"checker left action")
            key=(int(row["relator_index"]),t_blob)
            require(key in corr or len(corr)<limits["distinct_correlation_candidates"],
                    "checker candidate cap precondition")
            corr[key]=(corr.get(key,0)+int(row["coefficient"])*lam)%3
            if attempts&4095==0:tick("checker correlation")
    expected=sum(sum(int(r[0])==c for r in support)*sum(b["component"]==c for b in base)
                 for c in range(1,7))
    require(attempts==expected,"checker pair attempts")
    ordered=sorted(corr,key=lambda k:(k[1],k[0]))
    active=[(t,j,corr[(j,t)]) for j,t in ordered if corr[(j,t)]]
    require(len(active)<=limits["packed_active_rows"],"checker active cap precondition")
    zero=[(j,t) for j,t in ordered if not corr[(j,t)]]
    first=None if not active else {"translation_hex":active[0][0].hex(),
        "relator_index":active[0][1],"scalar":active[0][2]}
    contributor=None
    if first:
        target=(int(first["relator_index"]),bytes.fromhex(first["translation_hex"]))
        choices:list[tuple[tuple[Any,...],dict[str,Any]]]=[]
        for c,g_hex,lam in support:
            g_blob=bytes.fromhex(str(g_hex));g=unpack(g_blob)
            for row in (x for x in base if x["component"]==int(c) and
                        x["relator_index"]==target[0]):
                if pack(translation_from_pair(g,row["_value"],mul=mul,
                    inverse=inverse,orientation="g_times_h_inverse"))==target[1]:
                    candidate={"component":int(c),"g_hex":str(g_hex),
                        "lambda_coefficient":int(lam),"relator_index":target[0],
                        "h_hex":row["element_hex"],
                        "base_coefficient":int(row["coefficient"]),
                        "translation_hex":target[1].hex(),"formula":"t=g*h^-1",
                        "selection_order":
                          "component,g_blob,h_blob,lambda_coefficient,base_coefficient"}
                    order=(int(c),g_blob,bytes.fromhex(row["element_hex"]),
                           int(lam),int(row["coefficient"]))
                    choices.append((order,candidate))
        require(choices,"checker contributor")
        contributor=min(choices,key=lambda item:item[0])[1]
    packed=correlation_packed(active,width)
    return {"_candidate_values":corr,"_zero_keys":zero,
        "first_contributing_pair":contributor,"public":{"complete":True,
        "pair_attempts":attempts,"candidate_count_before_zero_deletion":len(corr),
        "cancellation_to_zero_count":len(zero),"active_count":len(active),
        "scalar_distribution":{"1":sum(x[2]==1 for x in active),
                               "2":sum(x[2]==2 for x in active)},
        "packed_row_width":width+2,"packed_rows_sha256":sha_bytes(packed),
        "packed_rows_bytes":len(packed),
        "public_order":"translation blob lexicographic, relator index",
        "first_active":first,"candidate_queries_interned":0,
        "full_E4_enumerated":False}}


def direct_scalar(t:Any,j:int,base:Sequence[dict[str,Any]],
                  support:dict[tuple[int,bytes],int],mul:Callable[[Any,Any],Any],
                  pack:Callable[[Any],bytes])->int:
    return sum(int(r["coefficient"])*support.get((int(r["component"]),
        pack(mul(t,r["_value"]))),0) for r in base if r["relator_index"]==j)%3


def independent_canaries(corr:dict[str,Any],support_rows:Sequence[Sequence[Any]],
                         base:Sequence[dict[str,Any]],identity:Any,
                         unpack:Callable[[bytes],Any],mul:Callable[[Any,Any],Any],
                         pack:Callable[[Any],bytes])->dict[str,Any]:
    support={(int(c),bytes.fromhex(str(g))):int(a) for c,g,a in support_rows}
    iblob=pack(identity);identity_rows=[]
    for j in range(1,12):
        value=direct_scalar(identity,j,base,support,mul,pack)
        require(value==corr["_candidate_values"].get((j,iblob),0),
                "checker identity canary")
        identity_rows.append([j,value])
    ordered=sorted(corr["_candidate_values"],key=lambda k:(k[1],k[0]))
    require(len(ordered)>=4,"checker four sample candidates")
    keys=ordered[:4]
    if corr["_zero_keys"]:
        z=sorted(corr["_zero_keys"],key=lambda k:(k[1],k[0]))[0]
        if z not in keys:keys.append(z)
    samples=[]
    for j,tb in keys:
        value=direct_scalar(unpack(tb),j,base,support,mul,pack)
        require(value==corr["_candidate_values"][(j,tb)],"checker sample")
        samples.append({"translation_hex":tb.hex(),"relator_index":j,
                        "scalar":value,"cancellation_row":value==0})
    first=corr["public"]["first_active"];first_value=None
    if first:
        first_value=direct_scalar(unpack(bytes.fromhex(first["translation_hex"])),
            int(first["relator_index"]),base,support,mul,pack)
        require(first_value==int(first["scalar"]),"checker first direct")
    return {"identity_translation":identity_rows,"identity_translation_pass":True,
        "deterministic_samples":samples,"sample_count":len(samples),
        "cancellation_sample_included":not corr["_zero_keys"] or
            any(r["cancellation_row"] for r in samples),
        "first_active_direct_scalar":first_value,
        "first_active_full_column_replayed":first is None or first_value is not None,
        "left_orientation":"t=g*h^-1","orientation_mutations_rejected":True}


def decode_expression_details(old:Any,payload:dict[str,Any],e4:Any)\
        ->tuple[list[Any],list[list[int]],Sequence[int],Sequence[int],Sequence[int]]:
    values=old.decode_section_expressions(payload,e4)
    arrays=payload["arrays"];n=payload["node_count"]
    kinds=old._decode_packed_array(arrays["kind"],"uint8","B",
                                   old.CAPS["directed_section_expr_nodes"])
    left=old._decode_packed_array(arrays["left"],"uint32","I",
                                  old.CAPS["directed_section_expr_nodes"])
    right=old._decode_packed_array(arrays["right"],"uint32","I",
                                   old.CAPS["directed_section_expr_nodes"])
    signed=old._decode_packed_array(arrays["signed_generator"],"int8","b",
                                    old.CAPS["directed_section_expr_nodes"])
    offsets=old._decode_packed_array(arrays["flat_offsets"],"uint32","I",
                                     old.CAPS["directed_section_expr_nodes"]+1)
    letters=old._decode_packed_array(arrays["flat_letters"],"int16","h",
        old.CAPS["directed_section_expr_nodes"]*old.CAPS["single_word_or_section_length"])
    words=[]
    for i in range(n):
        if kinds[i]==0:word=[]
        elif kinds[i]==1:word=[int(signed[i])]
        elif kinds[i]==4:word=[int(x) for x in letters[offsets[i]:offsets[i+1]]]
        elif kinds[i]==3:word=old.inv_word(words[int(left[i])])
        else:
            require(kinds[i]==2,"checker expression kind")
            word=old.reduce_word(words[int(left[i])]+words[int(right[i])])
        require(e4.eval(word)==values[i],"checker expression word/value")
        words.append(word)
    return values,words,kinds,left,right


def registered_bfs_hits(old:Any,e4:Any,wanted:set[bytes])->dict[bytes,list[int]]:
    steps=list(enumerate(e4.generators,1))+[
        (-i,e4.inverse_generators[i-1]) for i in range(1,7)]
    seen={e4.identity};queue=deque([(e4.identity,[])])
    found:dict[bytes,list[int]]={}
    while queue and len(seen)<=32768:
        value,word=queue.popleft();b=blob(value)
        if b in wanted and b not in found:found[b]=word
        if len(seen)==32768:continue
        for letter,step in steps:
            child=e4.mul(value,step)
            if child not in seen:
                seen.add(child);queue.append((child,old.reduce_word(word+[letter])))
                if len(seen)==32768:break
        if len(seen)&4095==0:tick("checker registered BFS")
    require(len(seen)==32768,"checker registered BFS count")
    return found


def validate_witness_dag_core(old:Any,e4:Any,witness:dict[str,Any],
                              pair:dict[str,Any],expected_h_word:Sequence[int]) \
        ->tuple[list[Any],list[list[int]],Sequence[int],Sequence[int],Sequence[int]]:
    roles=witness["node_roles"]
    require(set(roles)=={"g","t","h","inverse_h","u","h0"},
            "checker role keys")
    values,words,kinds,left,right=decode_expression_details(
        old,witness["section_expressions"],e4)
    for name in ("g","t","h","inverse_h"):
        require(isinstance(roles[name],int) and 0<=roles[name]<len(values),
                f"checker role {name}")
    g_id,t_id,h_id,ih_id=(roles[x] for x in ("g","t","h","inverse_h"))
    g_blob=bytes.fromhex(pair["g_hex"]);h_blob=bytes.fromhex(pair["h_hex"])
    t_blob=bytes.fromhex(pair["translation_hex"])
    require(blob(values[g_id])==g_blob and blob(values[h_id])==h_blob and
            blob(values[t_id])==t_blob and kinds[ih_id]==3 and
            int(left[ih_id])==h_id and kinds[t_id]==2 and
            int(left[t_id])==g_id and int(right[t_id])==ih_id,
            "checker witness t=g*h^-1 DAG")
    require(words[h_id]==list(expected_h_word),
            "checker contributing base-prefix section")
    replay=witness["direct_replay"]
    require(set(replay)=={"g_word_length","g_word_sha256","t_word_length",
        "t_word_sha256","g_value_hex","t_value_hex","both_exact"} and
        replay=={"g_word_length":len(words[g_id]),"g_word_sha256":sha_obj(words[g_id]),
        "t_word_length":len(words[t_id]),"t_word_sha256":sha_obj(words[t_id]),
        "g_value_hex":g_blob.hex(),"t_value_hex":t_blob.hex(),"both_exact":True},
        "checker direct witness replay")
    return values,words,kinds,left,right


def validate_section_witness(old:Any,e4:Any,data:dict[str,Any],
                             base:Sequence[dict[str,Any]],corr:dict[str,Any])->None:
    witness=data["section_witness"]
    require(set(witness)=={"first_active","contributing_pair","recovery",
        "node_roles","section_expressions","direct_replay",
        "typed_PRODUCT_INVERSE_only_above_registered_leaves",
        "transient_pool_ID_exported"},"checker witness keys")
    require(witness["first_active"]==corr["public"]["first_active"] and
            witness["contributing_pair"]==corr["first_contributing_pair"] and
            witness["typed_PRODUCT_INVERSE_only_above_registered_leaves"] is True and
            witness["transient_pool_ID_exported"] is False,"checker witness binding")
    pair=corr["first_contributing_pair"]
    contributing_h=next(r for r in base if r["relator_index"]==pair["relator_index"]
        and r["component"]==int(pair["component"]) and
        r["element_hex"]==pair["h_hex"])
    values,words,kinds,left,right=validate_witness_dag_core(
        old,e4,witness,pair,contributing_h["section_word"])
    roles=witness["node_roles"]
    g_id=roles["g"]
    g_blob=bytes.fromhex(pair["g_hex"])
    r0=old.substitute(old.embed_f2(old.hexagon_words(old.FIXED_WORD)[0]),
                      old.cofaces(3)[0])
    raw,value,sections=old.fox_with_sections(r0,e4)
    g=values[g_id];component=int(pair["component"])
    direct=sections.get(g) if (component,g) in raw else None
    recovery=witness["recovery"]
    if direct is not None:
        expected={"method":"base_target6_fox_prefix","component":component,
            "g_hex":g_blob.hex(),"source_word_sha256":sha_obj(direct)}
        require(recovery==expected and roles["u"] is None and roles["h0"] is None
                and words[g_id]==direct,"checker direct g recovery")
    else:
        candidates=sorted((r for r in base if r["component"]==component),
            key=lambda r:(r["relator_index"],bytes.fromhex(r["element_hex"])))
        possible={blob(e4.mul(g,e4.inverse(r["_value"]))) for r in candidates}
        bfs=registered_bfs_hits(old,e4,possible)
        directed={bytes.fromhex(r["translation_element_hex"])
                  for r in data["directed_surgery"]["translations"]}
        found=None
        for row in candidates:
            u=e4.mul(g,e4.inverse(row["_value"]));ub=blob(u)
            if ub in bfs or ub in directed:
                found=(row,u,ub);break
        require(found is not None,"checker sparse recovery existence")
        row,u,ub=found
        expected={"method":"registered_translation_times_base_prefix",
            "component":component,"g_hex":g_blob.hex(),
            "base_relator_index":row["relator_index"],
            "base_h0_hex":row["element_hex"],"registered_u_hex":ub.hex()}
        require(recovery==expected and isinstance(roles["u"],int) and
                isinstance(roles["h0"],int),"checker sparse recovery row")
        u_id,h0_id=roles["u"],roles["h0"]
        require(values[u_id]==u and blob(values[h0_id])==bytes.fromhex(row["element_hex"])
                and words[h0_id]==row["section_word"] and kinds[g_id]==2 and
                int(left[g_id])==u_id and int(right[g_id])==h0_id,
                "checker sparse recovery DAG")


def check_receipt(q3_path:Path,receipt_path:Path)->dict[str,Any]:
    ed=load_ed_checker();old=ed.load_old();configure_deadline_bridge(ed,old)
    q3=ed.load_q3(q3_path)
    raw=receipt_path.read_bytes();data=json.loads(raw.decode("utf-8"))
    require(raw==(json.dumps(data,sort_keys=True,separators=(",",":"))+"\n").encode(),
            "checker canonical JSON")
    expected_upstream=independent_upstream_caps(ed)
    validate_envelope(data,expected_upstream=expected_upstream)
    require(data["performance"]["receipt_bytes"]==len(raw) and
            len(raw)<=CAPS["packed_receipt_bytes"],"checker receipt bytes")
    if data["terminal_token"]=="B345_E4_FULL_D2_UNKNOWN_INPUT":return data
    e3,e4=old.reconstruct(q3);tick("checker quotient",True)
    old.validate_base_replay(data,q3,e3,e4)
    normalized,base_key,inverse_words=old.rebuild_normalized_inverse_fibre(q3,e4)
    require(data["normalized_inverse_fibre"]==normalized,"checker normalized inverse")
    if not data["prefix"]:
        require(data["terminal_token"]=="B345_E4_FULL_D2_UNKNOWN_RESOURCE" and
                data["phase"]=="fresh_immutable_prefix","checker pre-prefix resource")
        return data
    pool,basis,events=ed.replay_prefix(old,data,e4,normalized,base_key)
    require(data["prefix"]["prefix_pool_checkpoint"]==976408 and
            len(pool.values)==976408,"checker pool checkpoint")
    if not data["lambda_oracle"]:
        require(data["terminal_token"]=="B345_E4_FULL_D2_UNKNOWN_RESOURCE" and
                data["phase"]=="raw_lambda_oracle","checker pre-lambda resource")
        return data
    oracle=ed.RawOracle(old,pool,basis,ed.validate_qstar_label(ed.QSTAR,154))
    pivot_zero=[oracle.packed(row) for _,row in
                sorted(basis.rows.items(),key=lambda item:pool.pivot_order(item[0]))]
    require(pivot_zero==[0]*362709,"checker pivot annihilation")
    dep=[]
    for event in events:
        vector={}
        for component,value_hex,coefficient in event["raw_column"]:
            identifier=pool.ids.get(bytes.fromhex(value_hex))
            require(identifier is not None,"checker dependent pool")
            vector[old.replay_pack_key(component,identifier)]=coefficient
        require(oracle.packed(vector)==0,"checker dependent annihilation");dep.append(0)
    r0=old.substitute(old.embed_f2(old.hexagon_words(old.FIXED_WORD)[0]),
                      old.cofaces(3)[0])
    r0raw,r0value=old.fox(r0,e4)
    require(r0value==e4.identity and oracle.sparse(r0raw)==2,
            "checker target6 lambda")
    oracle.public.update({"pivot_annihilation_count":len(pivot_zero),
        "pivot_annihilation_sha256":sha_obj(pivot_zero),
        "dependent_annihilation_count":len(dep),
        "dependent_annihilation_sha256":sha_obj(dep),
        "base_target6_lambda":2,"base_target6_name":"hexagon_1_coface_0"})
    require(data["lambda_oracle"]==oracle.public,"checker lambda oracle")
    support=checker_lambda_support(oracle,154)
    require(data["lambda_support"]==support,"checker lambda support")
    if data["terminal_token"]=="B345_E4_FULL_D2_UNKNOWN_RESOURCE" and \
            not data["base_columns"]:
        require(data["phase"]=="base_columns","checker base-column resource phase")
        return data
    bundle=checker_base_bundle(old,e4)
    require(data["base_columns"]==bundle["public"] and
            data["directed_base_support"]=={"occurrences":bundle["public"]["occurrences"],
            "occurrence_count":76,"ordered_sha256":BASE_OCCURRENCE_SHA,
            "order":"relator index, component, canonical E4 bytes",
            "all_prefix_sections_directly_replayed":True},"checker base projection")
    if data["terminal_token"]=="B345_E4_FULL_D2_UNKNOWN_RESOURCE" and not data["correlation"]:
        require(data["phase"] in {"dual_correlation","section_witness",
                "receipt_serialization"},"checker correlation resource phase")
        return data
    pool_order_before=digest_pool_values(pool.values)
    pool_size_before=len(pool.values);pool_ids_before=len(pool.ids)
    mul,inverse=uncached_ops(old,e4)
    corr=independent_correlation(support["rows"],bundle["private_occurrences"],
        width=154,unpack=pool.unpack,mul=mul,inverse=inverse,
        pack=lambda v:blob(v))
    require(data["correlation"]==corr["public"],"checker complete correlation")
    canaries=independent_canaries(corr,support["rows"],
        bundle["private_occurrences"],e4.identity,pool.unpack,mul,blob)
    require(data["direct_canaries"]==canaries,"checker direct canaries")
    require(len(pool.values)==pool_size_before and len(pool.ids)==pool_ids_before and
            digest_pool_values(pool.values)==pool_order_before,
            "checker correlation pool neutrality")
    state=data["state_no_mutation"]
    dag_accounting=data["prefix"]["accounting"]["provenance_DAG"]
    section_accounting=data["directed_surgery"]["section_oracle"][
        "expression_accounting"]
    expected_state={"pool_size":pool_size_before,"pool_ids":pool_ids_before,
        "pool_order_sha256":pool_order_before,"basis_pivots":len(basis.rows),
        "basis_live_sparse_entries":basis.live_entries,
        "basis_columns":basis.columns_seen,
        "DAG_nodes":dag_accounting["live_nodes"],
        "DAG_edges":dag_accounting["live_edges"],
        "section_bindings":32768+207,
        "section_expression_nodes":section_accounting["live_nodes"],
        "section_expression_edges":section_accounting["live_edges"]}
    validate_state_record(state,expected_state)
    expected=("B345_E4_FULL_D2_ACTIVE_TRANSLATION" if corr["public"]["active_count"]
              else "B345_E4_FULL_D2_QSTAR_SEPARATOR")
    require(data["terminal_token"]==expected,"checker terminal selection")
    if corr["public"]["active_count"]:
        validate_section_witness(old,e4,data,bundle["private_occurrences"],corr)
    else:require(data["section_witness"]=={},"checker separator no witness")
    tick("checker complete",True)
    return data


###############################################################################
# Bounded shared-production-core fixture
###############################################################################

def p_mul(a:tuple[int,...],b:tuple[int,...])->tuple[int,...]:
    return tuple(a[b[i]] for i in range(len(a)))
def p_inv(a:tuple[int,...])->tuple[int,...]:
    out=[0]*len(a)
    for i,x in enumerate(a):out[x]=i
    return tuple(out)


def fixture_envelope(corr:dict[str,Any],active:bool)->dict[str,Any]:
    token="B345_E4_FULL_D2_ACTIVE_TRANSLATION" if active else \
          "B345_E4_FULL_D2_QSTAR_SEPARATOR"
    data={key:{} for key in TOP_KEYS}
    data.update({"schema":SCHEMA,"task_sha256":TASK_SHA,"terminal_token":token,
        "status":token,"reason":"complete_correlation_has_nonzero_translation" if active
        else "complete_correlation_all_translates_zero",
        "claim":"first_active_full_D2_translation_exported_not_a_lift" if active
        else "qstar_separates_base_target6_from_full_D2_for_pinned_E4_roof",
        "phase":"complete","pins":{},"caps":CAPS,
        "upstream_caps":{"registry":{},"sha256":sha_obj({})},"correlation":corr,
        "section_witness":{"toy":True} if active else {},
        "theorem_boundary":theorem_boundary(),"provenance":provenance_row(),
        "resource_guards":{
            "resource_hit":False,"resource":None,"atomic_partial":True},
        "partial":{},"input_errors":[],"performance":{
            "initial_remaining_seconds":30.0,"elapsed_seconds":0.0,
            "remaining_seconds":30.0,"checks":0,"peak_rss_bytes":0,
            "hit_reason":None,"receipt_bytes":0,"phase_seconds":{},
            "pair_loop_cadence":4096,"pool_intern_calls_in_correlation":0,
            "full_sparse_vectors_materialized_in_correlation":0,
            "full_E4_enumerations":0}})
    for name in ("base_q3_replay","normalized_inverse_fibre",
                 "directed_base_support","directed_surgery","prefix",
                 "lambda_oracle","lambda_support","base_columns",
                 "direct_canaries","state_no_mutation"):
        data[name]={"toy":True}
    data["performance"]["phase_seconds"]={name:0.0 for name in TIMED_PHASES}
    return data


def fixture_packed_array(values:Sequence[int]|bytes,kind:str,typecode:str,
                         cap:int)->dict[str,Any]:
    if typecode=="B":
        raw=bytes(values);length=len(raw);itemsize=1
    else:
        packed=array(typecode,values)
        if sys.byteorder!="little":packed.byteswap()
        raw=packed.tobytes();length=len(packed);itemsize=packed.itemsize
    require(length<=cap,"fixture packed cap")
    return {"type":kind,"array_typecode":typecode,"endianness":"little",
        "length":length,"itemsize":itemsize,"byte_length":len(raw),"cap":cap,
        "sha256":sha_bytes(raw),"base64":base64.b64encode(raw).decode("ascii")}


def fixture_section_case(old:Any,*,wrong_inverse_parent:bool=False) \
        ->tuple[Any,dict[str,Any],dict[str,Any],dict[str,Any]]:
    one=(0,1,2);r=(1,2,0);s=(1,0,2)
    identity_element=(one,());g=(r,());h=(s,())
    def typed_blob(value:Any)->bytes:
        require(isinstance(value,tuple) and len(value)==2 and
                isinstance(value[0],tuple) and len(value[0])==3 and
                isinstance(value[1],tuple) and len(value[1])==0,
                "checker toy production Element shape")
        result=bytes(value[0])+bytes(value[1])
        require(len(result)==3,"checker toy production blob width")
        return result
    class ToyCollector:n=0
    class ToyQ:
        degree=3
        def __init__(self)->None:
            self.collector=ToyCollector();self.pc=self.collector
            self.identity=identity_element
            self.generators=[g,h,identity_element,identity_element,
                             identity_element,identity_element]
            self.inverse_generators=[(p_inv(x[0]),()) for x in self.generators]
        @staticmethod
        def mul(a:Any,b:Any)->Any:
            typed_blob(a);typed_blob(b)
            return (p_mul(a[0],b[0]),())
        @staticmethod
        def inverse(a:Any)->Any:
            typed_blob(a)
            return (p_inv(a[0]),())
        def eval(self,word:Sequence[int],images:Sequence[Any]|None=None)->Any:
            marked=self.generators if images is None else images;out=self.identity
            for letter in word:
                value=marked[abs(letter)-1]
                out=self.mul(out,value if letter>0 else self.inverse(value))
            return out
    q=ToyQ()
    require(q.degree==3 and q.pc.n==0 and
            len(typed_blob(identity_element))==q.degree+q.pc.n,
            "checker toy Element/blob contract")
    parent=1 if wrong_inverse_parent else 2
    inverse_value=q.inverse([identity_element,g,h][parent])
    translation=q.mul(g,inverse_value)
    values=[identity_element,g,h,inverse_value,g,translation]
    caps=old.CAPS
    arrays={
        "kind":fixture_packed_array(bytes([0,4,4,3,2,2]),"uint8","B",
            caps["directed_section_expr_nodes"]),
        "signed_generator":fixture_packed_array([0,0,0,0,0,0],"int8","b",
            caps["directed_section_expr_nodes"]),
        "left":fixture_packed_array([0,0,0,parent,0,4],"uint32","I",
            caps["directed_section_expr_nodes"]),
        "right":fixture_packed_array([0,0,0,0,1,3],"uint32","I",
            caps["directed_section_expr_nodes"]),
        "flat_offsets":fixture_packed_array([0,0,1,2,2,2,2],"uint32","I",
            caps["directed_section_expr_nodes"]+1),
        "flat_letters":fixture_packed_array([1,2],"int16","h",
            caps["directed_section_expr_nodes"]*
            caps["single_word_or_section_length"]),
        "canonical_values":fixture_packed_array(
            b"".join(typed_blob(x) for x in values),"uint8","B",
            caps["directed_section_expr_nodes"]*3),
    }
    manifest={name:{k:v for k,v in row.items() if k!="base64"}
              for name,row in arrays.items()}
    payload={"format":"typed-section-expression-arrays/v1",
        "node_order":"zero_based_topological","ordinary_word_composition":True,
        "canonical_value_width":3,"node_count":6,"edge_count":5,
        "roots":[5],"arrays":arrays,
        "manifest_sha256":sha_obj({"arrays":manifest,"roots":[5]})}
    correct_t=q.mul(g,q.inverse(h));pair={"g_hex":typed_blob(g).hex(),
        "h_hex":typed_blob(h).hex(),"translation_hex":typed_blob(correct_t).hex()}
    gword=[1];tword=old.reduce_word([1,-2])
    witness={"node_roles":{"g":4,"t":5,"h":2,"inverse_h":3,
        "u":None,"h0":None},"section_expressions":payload,
        "direct_replay":{"g_word_length":len(gword),
            "g_word_sha256":sha_obj(gword),"t_word_length":len(tword),
            "t_word_sha256":sha_obj(tword),"g_value_hex":typed_blob(g).hex(),
            "t_value_hex":typed_blob(correct_t).hex(),"both_exact":True}}
    return q,witness,pair,{"expected_h_word":[2],"expected_t":correct_t}


def expect_failure(action:Callable[[],Any],label:str)->None:
    try:action()
    except (RuntimeError,ValueError):return
    raise RuntimeError(f"checker selftest mutation accepted: {label}")


def self_test()->None:
    global CHECKER_DEADLINE
    one=(0,1,2);r=(1,2,0);s=(1,0,2)
    vals=[one,r,p_mul(r,r),s,p_mul(r,s),p_mul(s,r)]
    support=[]
    for c in (1,2):
        for i,v in enumerate(vals):
            if (i+c)%2==0:support.append([c,bytes(v).hex(),1+(i%2)])
    support.sort(key=lambda x:(x[0],bytes.fromhex(x[1])))
    base=[]
    for j in range(1,3):
        for c,v,a in ((1,vals[j],1),(1,vals[j+2],2),(2,vals[j+1],1),(2,vals[j+3],2)):
            base.append({"relator_index":j,"component":c,"coefficient":a,
                         "element_hex":bytes(v).hex(),"_value":v,"section_word":[j,c]})
    corr=independent_correlation(support,base,width=3,unpack=lambda b:tuple(b),
        mul=p_mul,inverse=p_inv,pack=bytes,caps={"pair_attempts":1000,
        "distinct_correlation_candidates":1000,"packed_active_rows":1000})
    require(corr["public"]["active_count"]>0,"checker active fixture")
    validate_envelope(fixture_envelope(corr["public"],True),fixture=True)
    zero=independent_correlation([],base,width=3,unpack=lambda b:tuple(b),
        mul=p_mul,inverse=p_inv,pack=bytes,caps={"pair_attempts":1000,
        "distinct_correlation_candidates":1000,"packed_active_rows":1000})
    validate_envelope(fixture_envelope(zero["public"],False),fixture=True)
    cancel=independent_correlation([[1,bytes(one).hex(),1]],
        [{"relator_index":1,"component":1,"coefficient":1,
          "element_hex":bytes(one).hex(),"_value":one},
         {"relator_index":1,"component":1,"coefficient":2,
          "element_hex":bytes(one).hex(),"_value":one}],width=3,
        unpack=lambda b:tuple(b),mul=p_mul,inverse=p_inv,pack=bytes,
        caps={"pair_attempts":10,"distinct_correlation_candidates":10,
              "packed_active_rows":10})
    require(cancel["public"]["cancellation_to_zero_count"]==1,
            "checker cancellation")
    # The actual production translation helper rejects three distinct wrong
    # values on a noncommuting S4 fixture.
    g=(1,2,3,0);h=(1,0,2,3)
    answers=[p_mul(g,p_inv(h)),p_mul(p_inv(h),g),p_mul(p_inv(g),h),
             p_mul(h,p_inv(g))]
    require(len(set(answers))==4,"checker orientation values distinct")
    require(translation_from_pair(g,h,mul=p_mul,inverse=p_inv,
        orientation="g_times_h_inverse")==p_mul(g,p_inv(h)),
        "checker correct orientation")
    for orientation in ("h_inverse_times_g","g_inverse_times_h",
                        "right_action_solution"):
        try:translation_from_pair(g,h,mul=p_mul,inverse=p_inv,
                                  orientation=orientation)
        except RuntimeError:pass
        else:raise RuntimeError("checker accepted wrong orientation")
    # Production packed decoder + production witness-DAG replay.  The
    # fixture provider changes only the small quotient and leaf payload.
    ed=load_ed_checker();old=ed.load_old()
    reachable_caps=independent_upstream_caps(ed)
    require("raw_lambda_recursion_edges" in reachable_caps and
            "single_word_or_section_length" in reachable_caps and
            "packed_receipt_bytes" not in reachable_caps and
            "cube_count" not in reachable_caps,
            "checker reachable upstream resource registry")
    saved_absolute=CHECKER_DEADLINE;saved_ed_deadline=ed.CHECKER_DEADLINE
    saved_old_started=old.CHECKER_STARTED;saved_old_checks=old.CHECKER_CHECKS
    CHECKER_DEADLINE=time.monotonic()+5.0
    configure_deadline_bridge(ed,old)
    ed.CHECKER_DEADLINE.check("toy inherited deadline",True)
    old.CHECKER_CHECKS=255;old.checker_deadline("toy inherited cadence")
    require(old.CHECKER_CHECKS==256,"checker inherited cadence")
    old.CHECKER_CHECKS=0;validate_deadline_bridge(ed,old,CHECKER_DEADLINE)
    ed.CHECKER_DEADLINE.deadline+=1.0
    expect_failure(lambda:validate_deadline_bridge(ed,old,CHECKER_DEADLINE),
                   "inherited deadline extension")
    ed.CHECKER_DEADLINE.deadline=CHECKER_DEADLINE
    old.CHECKER_STARTED-=1.0
    expect_failure(lambda:validate_deadline_bridge(ed,old,CHECKER_DEADLINE),
                   "inherited deadline backdate")
    ed.CHECKER_DEADLINE=saved_ed_deadline
    old.CHECKER_STARTED=saved_old_started;old.CHECKER_CHECKS=saved_old_checks
    CHECKER_DEADLINE=saved_absolute
    toy_q,witness,pair,expected=fixture_section_case(old)
    values,words,kinds,left,right=validate_witness_dag_core(
        old,toy_q,witness,pair,expected["expected_h_word"])
    require(values[witness["node_roles"]["t"]]==expected["expected_t"] and
            words[witness["node_roles"]["t"]]==old.reduce_word([1,-2]) and
            kinds[witness["node_roles"]["inverse_h"]]==3,
            "checker production section core")
    expect_failure(lambda:toy_q.mul((0,1,2),expected["expected_t"]),
                   "bare permutation Element")
    _,bad_witness,bad_pair,bad_expected=fixture_section_case(
        old,wrong_inverse_parent=True)
    expect_failure(lambda:validate_witness_dag_core(old,toy_q,bad_witness,
        bad_pair,bad_expected["expected_h_word"]),"inverse parent/value/role")
    bad_witness=json.loads(json.dumps(witness))
    bad_witness["node_roles"]["g"],bad_witness["node_roles"]["h"]= \
        bad_witness["node_roles"]["h"],bad_witness["node_roles"]["g"]
    expect_failure(lambda:validate_witness_dag_core(old,toy_q,bad_witness,
        pair,expected["expected_h_word"]),"section role")
    bad_witness=json.loads(json.dumps(witness));payload=bad_witness[
        "section_expressions"]
    payload["arrays"]["kind"]=fixture_packed_array(
        bytes([0,4,4,2,2,2]),"uint8","B",
        old.CAPS["directed_section_expr_nodes"])
    manifest={name:{k:v for k,v in row.items() if k!="base64"}
              for name,row in payload["arrays"].items()}
    payload["manifest_sha256"]=sha_obj({"arrays":manifest,
                                         "roots":payload["roots"]})
    expect_failure(lambda:validate_witness_dag_core(old,toy_q,bad_witness,
        pair,expected["expected_h_word"]),"section opcode")
    bad_witness=json.loads(json.dumps(witness));payload=bad_witness[
        "section_expressions"]
    raw=bytearray(base64.b64decode(payload["arrays"]["canonical_values"]["base64"]))
    raw[-1]^=1
    payload["arrays"]["canonical_values"]=fixture_packed_array(raw,
        "uint8","B",old.CAPS["directed_section_expr_nodes"]*3)
    manifest={name:{k:v for k,v in row.items() if k!="base64"}
              for name,row in payload["arrays"].items()}
    payload["manifest_sha256"]=sha_obj({"arrays":manifest,
                                         "roots":payload["roots"]})
    expect_failure(lambda:validate_witness_dag_core(old,toy_q,bad_witness,
        pair,expected["expected_h_word"]),"section canonical value")
    # Exact independent persistent-state helper and an inner-field mutation.
    expected_state={"pool_size":6,"pool_ids":6,"pool_order_sha256":"toy",
        "basis_pivots":2,"basis_live_sparse_entries":3,"basis_columns":4,
        "DAG_nodes":5,"DAG_edges":6,"section_bindings":7,
        "section_expression_nodes":4,"section_expression_edges":3}
    state={"before":dict(expected_state),"after":dict(expected_state),
        "exact_equal":True,"helper_signature_excludes_pool_basis_DAG_sections":True,
        "pool_ID_reuse_or_intern_calls":0,"E4_cache_path_used":False}
    validate_state_record(state,expected_state)
    bad_state=json.loads(json.dumps(state));bad_state["before"]["pool_size"]+=1
    expect_failure(lambda:validate_state_record(bad_state,expected_state),
                   "persistent-state inner field")
    # Exact public/private mutation rejection.
    public={k:v for k,v in base[0].items() if not k.startswith("_")}
    require("_value" not in public,"checker public shape")
    bad=fixture_envelope(zero["public"],False);bad["extra"]=1
    expect_failure(lambda:validate_envelope(bad,fixture=True),"top-level schema")
    normal=fixture_envelope(zero["public"],False)
    for field,value in (("reason","forged"),("phase","section_witness"),
                        ("partial",{"forged":True}),
                        ("resource_guards",{"resource_hit":True,
                          "resource":None,"atomic_partial":True})):
        bad=json.loads(json.dumps(normal));bad[field]=value
        expect_failure(lambda bad=bad:validate_envelope(bad,fixture=True),
                       f"normal terminal {field}")
    resource=json.loads(json.dumps(normal))
    resource["terminal_token"]=resource["status"]= \
        "B345_E4_FULL_D2_UNKNOWN_RESOURCE"
    resource["reason"]="pair_attempts";resource["claim"]="none"
    resource["phase"]="dual_correlation"
    for name in ("correlation","direct_canaries","state_no_mutation",
                 "section_witness"):resource[name]={}
    row={"cap_reason":"pair_attempts","cap_key":"pair_attempts",
        "cap_source":"local",
        "cap_limit":CAPS["pair_attempts"],
        "observed_count":CAPS["pair_attempts"]+1,"comparator":"gt",
        "phase":"dual_correlation",
        "current":{"lambda_ordinal":1,"base_component_ordinal":1}}
    resource["resource_guards"]={"resource_hit":True,"resource":row,
        "atomic_partial":True}
    resource["partial"]={"phase":"dual_correlation","current":row["current"],
        "correlation_published":False,"mathematical_claim":"none",
        "rollback_required":False,"reason":"pair_attempts"}
    resource["performance"]["hit_reason"]="pair_attempts"
    resource["performance"]["phase_seconds"]={
        name:0.0 for name in TIMED_PHASES[:4]}
    validate_envelope(resource,fixture=True)
    bad=json.loads(json.dumps(resource));bad["correlation"]={"forged":True}
    expect_failure(lambda:validate_envelope(bad,fixture=True),
                   "resource later-field injection")
    bad=json.loads(json.dumps(resource))
    bad["resource_guards"]["resource"]["cap_reason"]="forged"
    expect_failure(lambda:validate_envelope(bad,fixture=True),
                   "resource reason mutation")
    serialization=json.loads(json.dumps(normal))
    serialization["terminal_token"]=serialization["status"]= \
        "B345_E4_FULL_D2_UNKNOWN_RESOURCE"
    serialization["reason"]="packed_receipt_bytes"
    serialization["claim"]="none";serialization["phase"]="receipt_serialization"
    for name in ("correlation","direct_canaries","state_no_mutation",
                 "section_witness"):serialization[name]={}
    srow={"cap_reason":"packed_receipt_bytes","cap_key":"packed_receipt_bytes",
        "cap_source":"local","cap_limit":CAPS["packed_receipt_bytes"],
        "observed_count":CAPS["packed_receipt_bytes"]+1,"comparator":"gt",
        "phase":"receipt_serialization","current":{}}
    serialization["resource_guards"]={"resource_hit":True,"resource":srow,
        "atomic_partial":True}
    serialization["partial"]={"phase":"receipt_serialization","current":{},
        "correlation_published":False,"mathematical_claim":"none",
        "rollback_required":False,"reason":"packed_receipt_bytes"}
    serialization["performance"]["hit_reason"]="packed_receipt_bytes"
    validate_envelope(serialization,fixture=True)
    upstream_limit=16_777_216
    upstream=json.loads(json.dumps(serialization))
    upstream_registry={"packed_receipt_bytes":upstream_limit}
    upstream["upstream_caps"]={"registry":upstream_registry,
        "sha256":sha_obj(upstream_registry)}
    upstream["resource_guards"]["resource"]["cap_source"]="upstream"
    upstream["resource_guards"]["resource"]["cap_limit"]=upstream_limit
    upstream["resource_guards"]["resource"]["observed_count"]=upstream_limit+1
    validate_envelope(upstream,fixture=True,expected_upstream=upstream_registry)
    bad=json.loads(json.dumps(serialization))
    bad["resource_guards"]["resource"]["cap_source"]="upstream"
    expect_failure(lambda:validate_envelope(bad,fixture=True),
                   "resource cap-source collision")
    for local_only in ("common_math_soft_deadline_seconds",
                       "producer_soft_rss_bytes"):
        bad=json.loads(json.dumps(serialization))
        bad["upstream_caps"]={"registry":reachable_caps,
            "sha256":sha_obj(reachable_caps)}
        badrow=bad["resource_guards"]["resource"]
        badrow["cap_source"]="upstream"
        badrow["cap_reason"]=badrow["cap_key"]=bad["reason"]=local_only
        badrow["cap_limit"]=CAPS[local_only]
        badrow["observed_count"]=CAPS[local_only]+1
        badrow["comparator"]="ge"
        bad["partial"]["reason"]=local_only
        bad["performance"]["hit_reason"]=local_only
        expect_failure(lambda bad=bad:validate_envelope(
            bad,fixture=True,expected_upstream=reachable_caps),
            "local-only cap upstream masquerade "+local_only)
    upstream_real=json.loads(json.dumps(normal))
    upstream_real["terminal_token"]=upstream_real["status"]= \
        "B345_E4_FULL_D2_UNKNOWN_RESOURCE"
    upstream_real["reason"]="raw_lambda_recursion_edges"
    upstream_real["claim"]="none";upstream_real["phase"]="raw_lambda_oracle"
    for name in ("lambda_oracle","lambda_support","base_columns","correlation",
                 "direct_canaries","state_no_mutation","section_witness"):
        upstream_real[name]={}
    upstream_real["upstream_caps"]={"registry":reachable_caps,
        "sha256":sha_obj(reachable_caps)}
    ulimit=reachable_caps["raw_lambda_recursion_edges"]
    urow={"cap_reason":"raw_lambda_recursion_edges",
        "cap_key":"raw_lambda_recursion_edges","cap_source":"upstream",
        "cap_limit":ulimit,"observed_count":ulimit+1,"comparator":"gt",
        "phase":"raw_lambda_oracle","current":{}}
    upstream_real["resource_guards"]={"resource_hit":True,"resource":urow,
        "atomic_partial":True}
    upstream_real["partial"]={"phase":"raw_lambda_oracle","current":{},
        "correlation_published":False,"mathematical_claim":"none",
        "rollback_required":False,"reason":"raw_lambda_recursion_edges"}
    upstream_real["performance"]["hit_reason"]="raw_lambda_recursion_edges"
    upstream_real["performance"]["phase_seconds"]={
        name:0.0 for name in TIMED_PHASES[:2]}
    validate_envelope(upstream_real,fixture=True,
                      expected_upstream=reachable_caps)
    bad=json.loads(json.dumps(upstream_real));badrow=bad["resource_guards"]["resource"]
    badrow["cap_reason"]=badrow["cap_key"]=bad["reason"]="cube_count"
    badrow["cap_limit"]=ed.CAPS_157ED["cube_count"]
    badrow["observed_count"]=ed.CAPS_157ED["cube_count"]+1
    bad["partial"]["reason"]="cube_count"
    bad["performance"]["hit_reason"]="cube_count"
    expect_failure(lambda:validate_envelope(bad,fixture=True,
        expected_upstream=reachable_caps),"hard-equality cap masquerade")
    unknown=json.loads(json.dumps(normal))
    unknown["terminal_token"]=unknown["status"]= \
        "B345_E4_FULL_D2_UNKNOWN_INPUT"
    unknown["reason"]="authenticated_input_failure";unknown["claim"]="none"
    unknown["phase"]="authenticated_input";unknown["input_errors"]=["toy"]
    for name in ("base_q3_replay","normalized_inverse_fibre",
        "directed_base_support","directed_surgery","prefix","lambda_oracle",
        "lambda_support","base_columns","correlation","direct_canaries",
        "state_no_mutation","section_witness"):unknown[name]={}
    unknown["performance"]["phase_seconds"]={}
    validate_envelope(unknown,fixture=True)
    bad=json.loads(json.dumps(unknown));bad["lambda_support"]={"forged":True}
    expect_failure(lambda:validate_envelope(bad,fixture=True),
                   "unknown input math injection")
    bad=json.loads(json.dumps(normal));bad["provenance"]["run"]="0"
    expect_failure(lambda:validate_envelope(bad,fixture=True),
                   "provenance mutation")
    bad=json.loads(json.dumps(normal));bad["performance"]["remaining_seconds"]=31.0
    expect_failure(lambda:validate_envelope(bad,fixture=True),
                   "performance remaining mutation")
    bad=json.loads(json.dumps(normal));bad["performance"]["phase_seconds"][
        "forged_phase"]=0.0
    expect_failure(lambda:validate_envelope(bad,fixture=True),
                   "performance phase mutation")
    print("D972_B345_FULL_D2_DUAL_CORRELATION_CHECKER_SELFTEST_PASS "
          "production_correlation=1 terminal_schema=1 active=1 separator=1 "
          "cancellation=1 orientations=3 public_shape=1 resource_schema=1 "
          "section_decoder=1 inverse_mutation=1 state_snapshot=1 "
          "cap_sources=2 deadline_bridge=1 provenance=1 performance=1",flush=True)


def main(argv:Sequence[str]|None=None)->int:
    global CHECKER_STARTED,CHECKER_DEADLINE,CHECKER_CHECKS
    parser=argparse.ArgumentParser();parser.add_argument("--self-test",action="store_true")
    parser.add_argument("--q3",type=Path,default=ROOT/Q3_PATH)
    parser.add_argument("--receipt",type=Path,default=ROOT/OUTPUT)
    parser.add_argument("--seconds",type=float,default=18_000.0)
    args=parser.parse_args(argv)
    require(0.0<args.seconds<=18_000.0,"checker common deadline input")
    CHECKER_STARTED=time.monotonic();CHECKER_DEADLINE=CHECKER_STARTED+args.seconds
    CHECKER_CHECKS=0
    if args.self_test:self_test();return 0
    result=check_receipt(args.q3,args.receipt)
    print("D972_B345_FULL_D2_DUAL_CORRELATION_CHECKER_PASS "
          f"terminal={result['terminal_token']}",flush=True)
    return 0


if __name__=="__main__":raise SystemExit(main())
