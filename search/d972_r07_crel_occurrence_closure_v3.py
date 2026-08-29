#!/usr/bin/env python3
"""Complete raw eleven-occurrence closure of the task382 C_rel basis (v3)."""
from __future__ import annotations
import argparse, hashlib, importlib.util, json, tempfile
from types import SimpleNamespace
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "d972-r07-crel-occurrence-closure/v3"
TASK382_SCHEMA = "d972-r07-a4-legal-source-extractor/v1"
TASK382_CHECK_SCHEMA = TASK382_SCHEMA + "/crosscheck/v1"
TASK382_PASS = "A4_LEGAL_RELATIVE_SOURCE_COMPLETE"
PASS = "CREL_OCCURRENCE_CLOSURE_COMPLETE"
UNKNOWN_INPUT, UNKNOWN_RESOURCE = "UNKNOWN_INPUT", "UNKNOWN_RESOURCE"
PREFIX = "CREL_OCCURRENCE_CLOSURE_V3_PRODUCER_TERMINAL"
MAX_INPUT_BYTES, MAX_OUTPUT_BYTES, MAX_QUEUE, MAX_WORD = 2_000_000_000, 2_000_000_000, 200_000, 20_000_000
TASK382_PRODUCER_PIN = ("search/d972_r07_a4_legal_source_extractor_v1.py", 45551, "e0a70e81e8ebad95e95bd30784b3150b4e06608236d22d00569cde1c17a0a885")
TASK382_CHECKER_PIN = ("crosscheck/check_d972_r07_a4_legal_source_extractor_v1.py", 49380, "35bf8d6c91770326efe46669287bdf39c72c951c14d0b5afe72820cc826802fc")
TASK179_OWNER_PIN = ("search/d972_r07_positive_common_word_colgen_v1.py", 123870, "47116826e1b94750fa5eaa0c577586aeaec23a476c5f004fc0d5ea83892845c7")
G760_PIN = ("search/check_d972_r07_616_to_760_commutator_affine_rhs_v3.py", 33409, "f8c7fc7f5b5bbfffa0cf147a59313981c5a4b2c6c00504a9f773029097fdde5f")
G760_WORD_SHA256 = "518f09820b8d7baee6b58ebf366cebf7b02a9a945cd1350cf8c701a4e6bc2b4d"
PHYSICAL_OWNER: dict[str, Any] | None = None
PHYSICAL_G: list[int] | None = None
BASE_STATES: list[Any] | None = None
PHYSICAL_MODEL: Any = None
ACTOR_CACHE: dict[tuple[int, int], tuple[Any, Any]] = {}
ACTIVE_RECEIPT: dict[str, Any] | None = None
def element_token(value: Any) -> str:
    if isinstance(value, tuple) and len(value) == 2 and all(isinstance(x, bytes) for x in value):
        return value[0].hex() + value[1].hex()
    return canonical(value).hex()

class InputStop(Exception): pass
class ResourceStop(Exception): pass
def need(value: bool, reason: str) -> None:
    if not value: raise InputStop(reason)
def cap(value: bool, reason: str) -> None:
    if not value: raise ResourceStop(reason)
def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("ascii")
def digest(value: Any) -> str: return hashlib.sha256(canonical(value)).hexdigest()
def digest_bytes(raw: bytes) -> str: return hashlib.sha256(raw).hexdigest()

def read_bytes(path: Path, expected: tuple[str, int, str], label: str) -> bytes:
    need(path.is_file() and not path.is_symlink(), label + ":regular_file")
    raw = path.read_bytes(); need(len(raw) == expected[1] and digest_bytes(raw) == expected[2], label + ":pin")
    return raw
def json_object(raw: bytes, label: str) -> dict[str, Any]:
    try: value = json.loads(raw.decode("ascii"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc: raise InputStop(label + ":canonical_ascii_json") from exc
    need(isinstance(value, dict) and raw in (canonical(value), canonical(value) + b"\n"), label + ":canonical")
    return value
def check_seal(value: dict[str, Any], label: str) -> None:
    body = dict(value); claimed = body.pop("self_digest_sha256", None)
    need(isinstance(claimed, str) and claimed == digest(body), label + ":seal")
def validate_c_rel(receipt: dict[str, Any]) -> None:
    c_rel = receipt.get("C_rel")
    need(isinstance(c_rel, dict) and c_rel.get("formula") == "C_rel=R_S(Delta1) intersect K=[R_S(Delta0),K]" and c_rel.get("commutator_convention") == "[s,u]=s*u*s^-1*u^-1" and c_rel.get("extra_side_gate_intersection") is False, "task382:C_rel_header")
    need(isinstance(c_rel.get("basis"), list) and isinstance(c_rel.get("echelon"), list) and len(c_rel["basis"]) == len(c_rel["echelon"]) and c_rel.get("rank") == len(c_rel["basis"]), "task382:C_rel_rank")
    for item in c_rel["basis"]:
        need(isinstance(item, dict) and isinstance(item.get("literal_commutator_word"), list) and isinstance(item.get("full_K_vector"), dict) and isinstance(item.get("literal_commutator_word_sha256"), str) and item.get("coarse_identity") is True and isinstance(item.get("change_of_basis"), dict) and isinstance(item.get("reduction_trace"), list), "task382:C_rel_ancestry")
def input_path(text: str, label: str) -> Path:
    path = (ROOT / text).resolve(); base = (ROOT / "ci" / "in").resolve()
    need(path.parent == base and path.name == Path(text).name, label + ":ci_in_path"); return path
def output_path(text: str) -> Path:
    path = (ROOT / text).resolve(); base = (ROOT / "ci" / "out").resolve()
    need(path.parent == base and path.name == Path(text).name, "output:ci_out_path"); return path
def reduce_word(*parts: list[int]) -> list[int]:
    answer: list[int] = []
    for raw in (x for part in parts for x in part):
        x = int(raw); need(x in (-2, -1, 1, 2), "word:letter")
        if answer and answer[-1] == -x: answer.pop()
        else: answer.append(x)
    cap(len(answer) <= MAX_WORD, "literal_word_cap"); return answer
def inverse_word(word: list[int]) -> list[int]: return [-x for x in reversed(word)]
def sparse_add(left: dict[str, int], right: dict[str, int], scale: int = 1) -> dict[str, int]:
    out = dict(left)
    for key, value in right.items():
        coefficient = (out.get(key, 0) + int(scale) * int(value)) % 3
        if coefficient: out[key] = coefficient
        else: out.pop(key, None)
    return out
def sparse_scale(row: dict[str, int], scale: int) -> dict[str, int]:
    return {key: int(value) * scale % 3 for key, value in row.items() if int(value) * scale % 3}

def load_task382(raw: bytes) -> dict[str, Any]:
    ns: dict[str, Any] = {"__name__": "task382_frozen_producer", "__file__": str(ROOT / TASK382_PRODUCER_PIN[0])}
    exec(compile(raw, "task382_frozen_producer", "exec"), ns, ns); return ns
def authenticate_physical_owners() -> None:
    global PHYSICAL_OWNER, PHYSICAL_G
    raw = read_bytes(ROOT / TASK179_OWNER_PIN[0], TASK179_OWNER_PIN, "task179.owner")
    graw = read_bytes(ROOT / G760_PIN[0], G760_PIN, "g760.owner")
    physical: dict[str, Any] = {"__name__": "task179_frozen", "__file__": str(ROOT / TASK179_OWNER_PIN[0])}
    exec(compile(raw, "task179_frozen", "exec"), physical, physical)
    need(callable(physical.get("AllSevenModel")), "task179:AllSevenModel")
    for name in ("occurrence_column", "direct_column"):
        need(callable(getattr(physical["AllSevenModel"], name, None)), "task179:" + name)
    gowner: dict[str, Any] = {"__name__": "g760_frozen", "__file__": str(ROOT / G760_PIN[0])}
    exec(compile(graw, "g760_frozen", "exec"), gowner, gowner)
    need(callable(gowner.get("construct_base")), "g760:construct_base")
    _, _, word = gowner["construct_base"]()
    need(len(word) == 760 and digest(word) == G760_WORD_SHA256, "g760:word_pin")
    PHYSICAL_OWNER, PHYSICAL_G = physical, list(word)
def restore_runtime() -> tuple[Any, Any, Any, Any, Any]:
    raw = read_bytes(ROOT / TASK382_PRODUCER_PIN[0], TASK382_PRODUCER_PIN, "task382.producer")
    read_bytes(ROOT / TASK382_CHECKER_PIN[0], TASK382_CHECKER_PIN, "task382.checker")
    owner = load_task382(raw); frozen = owner["restore_v12"]()
    authority, runtime, meter = owner["instantiate_owner"](frozen); authenticate_physical_owners()
    global BASE_STATES, PHYSICAL_MODEL
    BASE_STATES = runtime.states_direct(PHYSICAL_G)
    for item in authority.receipt.get("bridge", {}).get("occurrence_ledger", []):
        ordinal = int(item["ordinal"]); index = int(item["ten_index"]); q = BASE_STATES[index].q; prefix = q.identity
        for prior_ordinal in item.get("fox_prefix_occurrences", ()):
            prior = authority.receipt["bridge"]["occurrence_ledger"][int(prior_ordinal) - 1]; prior_state = BASE_STATES[int(prior["ten_index"])]
            prefix = q.mul(prefix, prior_state.a if int(prior["factor_sign"]) > 0 else q.inverse(prior_state.a))
        current = BASE_STATES[index]; p = q.mul(prefix, current.a) if int(item["factor_sign"]) > 0 else prefix
        for letter in (1, -1, 2, -2):
            rho = runtime.states_direct([letter])[index].a; ACTOR_CACHE[ordinal, letter] = (q, q.mul(q.mul(p, rho), q.inverse(p)))
    class Joint:
        def __init__(self) -> None: self.identity = self.eval([])
        def eval(self, word: list[int]) -> tuple[Any, ...]: return tuple(state.a for state in runtime.states_direct(word))
    adapter = {"old": runtime.old, "e3": runtime.e3, "e4": runtime.e4, "bridge": {"g760": {"word": list(PHYSICAL_G)}}, "p176": SimpleNamespace(packed_joint_blob=lambda value, label: owner["element_blob"](value)), "joint_group": Joint()}
    PHYSICAL_MODEL = PHYSICAL_OWNER["AllSevenModel"](adapter)
    # The task382 namespace authenticates identity/authority; the exact
    # restore_v12 return namespace owns BRIDGE_OWNER_LAYOUT.
    return owner, frozen, authority, runtime, meter
def load_inputs(args: argparse.Namespace) -> tuple[dict[str, Any], dict[str, Any], bytes, bytes]:
    fields = (args.task382_receipt, args.task382_receipt_bytes, args.task382_receipt_sha256, args.task382_verdict, args.task382_verdict_bytes, args.task382_verdict_sha256)
    need(all(value is not None for value in fields), "task382:all_pins_required")
    need(isinstance(args.task382_receipt_bytes, int) and isinstance(args.task382_verdict_bytes, int) and 0 < args.task382_receipt_bytes <= MAX_INPUT_BYTES and 0 < args.task382_verdict_bytes <= MAX_INPUT_BYTES, "task382:byte_cap")
    rr = read_bytes(input_path(args.task382_receipt, "task382.receipt"), (args.task382_receipt, args.task382_receipt_bytes, args.task382_receipt_sha256), "task382.receipt")
    vr = read_bytes(input_path(args.task382_verdict, "task382.verdict"), (args.task382_verdict, args.task382_verdict_bytes, args.task382_verdict_sha256), "task382.verdict")
    receipt, verdict = json_object(rr, "task382.receipt"), json_object(vr, "task382.verdict")
    check_seal(receipt, "task382.receipt"); check_seal(verdict, "task382.verdict")
    need(receipt.get("schema") == TASK382_SCHEMA and receipt.get("status") == "COMPLETE" and receipt.get("terminal") == TASK382_PASS and receipt.get("complete") is True, "task382:producer_not_positive")
    need(verdict.get("schema") == TASK382_CHECK_SCHEMA and verdict.get("status") == "COMPLETE" and verdict.get("terminal") == TASK382_PASS and verdict.get("accepted") is True and verdict.get("independent") is True, "task382:checker_not_accepted")
    need(verdict.get("producer", {}).get("sha256") == digest_bytes(rr), "task382:verdict_receipt_binding")
    need(verdict.get("complete") is True and verdict.get("C_rel", {}).get("rank") == receipt.get("C_rel", {}).get("rank"), "task382:verdict_C_rel_rank")
    need(verdict.get("C_rel", {}).get("two_way_span_equality") is True and verdict.get("C_rel", {}).get("all_literal_commutators_replayed") is True, "task382:verdict_C_rel_replay")
    receipt_a4 = receipt.get("A4_ambient_owner", {}); verdict_a4 = verdict.get("A4_ambient_owner", {})
    need(receipt_a4.get("positive_authenticated") is True and verdict_a4.get("receipt") == receipt_a4.get("receipt") and verdict_a4.get("verdict") == receipt_a4.get("verdict"), "task382:A4_ambient_owner")
    c_rel = receipt.get("C_rel", {})
    need(c_rel.get("rank_proof_sha256") == digest({"blocks": c_rel.get("block_columns"), "echelon": c_rel.get("echelon")}), "task382:rank_proof")
    validate_c_rel(receipt)
    global ACTIVE_RECEIPT
    ACTIVE_RECEIPT = receipt
    return receipt, verdict, rr, vr
def occurrence_roster(authority: Any, frozen_owner: Any, task382_owner: Any) -> list[dict[str, Any]]:
    need(isinstance(frozen_owner, dict) and isinstance(task382_owner, dict), "task382:owner_namespaces")
    need(callable(task382_owner.get("frozen_identities")), "task382:frozen_identity_owner")
    if ACTIVE_RECEIPT is not None:
        need(ACTIVE_RECEIPT.get("frozen_owner_identities") == task382_owner["frozen_identities"](), "task382:frozen_owner_identities")
        need(ACTIVE_RECEIPT.get("task198_task176_authority") == authority.identity, "task382:authority_identity")
    ledger = authority.receipt.get("bridge", {}).get("occurrence_ledger")
    need(isinstance(ledger, list) and len(ledger) == 11, "task198:occurrence_ledger")
    layout = frozen_owner.get("BRIDGE_OWNER_LAYOUT")
    need(isinstance(layout, (list, tuple)) and len(layout) == 11, "task198:layout_owner")
    for index, item in enumerate(ledger):
        need(int(item.get("ordinal")) == index + 1 and int(item.get("ten_index")) in range(10) and isinstance(item.get("occurrence"), str), "task198:occurrence_field")
        expected = layout[index]
        actual = (item.get("block"), int(item.get("block_index")), int(item.get("block_slot")), item.get("occurrence"), item.get("type"), int(item.get("ten_index")), int(item.get("context_id")), item.get("role"), int(item.get("factor_sign")), item.get("orientation"), tuple(item.get("fox_prefix_occurrences", ())))
        need(isinstance(expected, (list, tuple)) and actual == tuple(expected), "task198:ledger_layout")
        item["coordinate_key_prefix"] = "o" + str(index + 1) + ":"
    return ledger
def term_vector(runtime: Any, word: list[int], ledger: list[dict[str, Any]]) -> dict[str, int]:
    base10 = BASE_STATES or runtime.states_direct(PHYSICAL_G or []); states = runtime.states_direct(word); answer: dict[str, int] = {}
    for item in ledger:
        index = int(item["ten_index"]); state = states[index]; q = state.q; prefix = q.identity
        for ordinal in item.get("fox_prefix_occurrences", ()):
            prior = ledger[int(ordinal) - 1]; prior_state = base10[int(prior["ten_index"])]
            prefix = q.mul(prefix, prior_state.a if int(prior["factor_sign"]) > 0 else q.inverse(prior_state.a))
        current = base10[index]; translate = q.mul(prefix, current.a) if int(item["factor_sign"]) > 0 else prefix
        for (component, element), value in state.u.items():
            moved = q.mul(translate, element); key = "o" + str(int(item["ordinal"])) + ":" + str(component) + ":" + element_token(moved)
            answer[key] = (answer.get(key, 0) + int(item["factor_sign"]) * int(value)) % 3
            if not answer[key]: answer.pop(key)
    return answer
def action_term(seed_word: list[int], action_word: tuple[int, ...], ledger: list[dict[str, Any]], runtime: Any, conjugate: bool = False) -> dict[str, int]:
    aw = list(action_word)
    if conjugate:
        return term_vector(runtime, reduce_word(aw, seed_word, inverse_word(aw)), ledger)
    if not aw:
        return term_vector(runtime, seed_word, ledger)
    left = term_vector(runtime, reduce_word(aw, seed_word), ledger)
    return sparse_add(left, term_vector(runtime, aw, ledger), -1)
def apply_actor(row: dict[str, int], letter: int, ledger: list[dict[str, Any]]) -> dict[str, int]:
    out: dict[str, int] = {}
    for key, value in row.items():
        ordinal, component, token = key.split(":", 2); q, actor = ACTOR_CACHE[int(ordinal[1:]), letter]; raw = bytes.fromhex(token); block = ledger[int(ordinal[1:]) - 1]["type"]; cut = 36 if block == "E3" else 144; element = (raw[:cut], raw[cut:]); moved = element_token(q.mul(actor, element)); new = ordinal + ":" + component + ":" + moved; out[new] = (out.get(new, 0) + int(value)) % 3
        if not out[new]: out.pop(new)
    return out
def aggregate_tagged(row: dict[str, int], ledger: list[dict[str, Any]]) -> dict[bytes, int]:
    out: dict[bytes, int] = {}
    for key, value in row.items():
        ordinal, component, element = key.split(":", 2); block = {"H1": 1, "H2": 2, "P1": 3, "P2": 3, "P3": 3, "P5": 3, "P4": 3}[str(ledger[int(ordinal[1:]) - 1]["block"])]
        flat = b"R" + bytes((block, int(component))) + len(bytes.fromhex(element)).to_bytes(2, "big") + bytes.fromhex(element)
        out[flat] = (out.get(flat, 0) + int(value)) % 3
        if not out[flat]: out.pop(flat)
    return out
def formal_action(formal: dict[str, int], letter: int) -> dict[str, int]:
    out: dict[str, int] = {}
    for encoded, coefficient in formal.items():
        seed, text = encoded.split("|", 1); old = [int(x) for x in text.split(",") if x]
        action = reduce_word([letter], old); key = seed + "|" + ",".join(str(x) for x in action)
        out[key] = (out.get(key, 0) + coefficient) % 3
        if not out[key]: out.pop(key)
    return out
def evaluate_formal(formal: dict[str, int], seed_words: dict[str, list[int]], ledger: list[dict[str, Any]], runtime: Any, cache: dict[tuple[str, tuple[int, ...]], dict[str, int]] | None = None) -> dict[str, int]:
    out: dict[str, int] = {}
    for encoded, coefficient in formal.items():
        seed, text = encoded.split("|", 1); action = tuple(int(x) for x in text.split(",") if x); key = (seed, action)
        if cache is not None and key not in cache: cache[key] = action_term(seed_words[seed], action, ledger, runtime)
        value = cache[key] if cache is not None else action_term(seed_words[seed], action, ledger, runtime)
        out = sparse_add(out, value, coefficient)
    return out
def insert(raw: dict[str, int], formal: dict[str, int], rows: dict[str, dict[str, int]], forms: dict[str, dict[str, int]], pivot_order: list[str]) -> tuple[bool, dict[str, int], dict[str, int], dict[str, Any]]:
    work, ancestry, trace = dict(raw), dict(formal), []
    for pivot in pivot_order:
        coefficient = work.get(pivot, 0)
        if coefficient:
            work = sparse_add(work, rows[pivot], -coefficient); ancestry = sparse_add(ancestry, forms[pivot], -coefficient); trace.append({"pivot": pivot, "coefficient": coefficient})
    if not work: return False, {}, {}, {"reduction_trace": trace, "remainder": {}}
    pivot = min(work); scale = 1 if work[pivot] == 1 else 2; work, ancestry = sparse_scale(work, scale), sparse_scale(ancestry, scale); rows[pivot], forms[pivot] = work, ancestry; pivot_order.append(pivot)
    return True, work, ancestry, {"pivot": pivot, "normalization_scale": scale, "reduction_trace": trace, "remainder": work}
def closure(seed_columns: list[dict[str, Any]], runtime: Any, ledger: list[dict[str, Any]], action_order: tuple[int, ...]) -> dict[str, Any]:
    seed_words = {str(item["seed_id"]): list(item["literal_commutator_word"]) for item in seed_columns}; rows: dict[str, dict[str, int]] = {}; forms: dict[str, dict[str, int]] = {}; pivot_order: list[str] = []; traces: dict[str, dict[str, Any]] = {}; queue: list[dict[str, Any]] = []; transitions = []; seeds = []; action_cache: dict[tuple[str, tuple[int, ...]], dict[str, int]] = {}
    for item in seed_columns:
        sid = str(item["seed_id"]); formal = {sid + "|": 1}; raw = action_term(seed_words[sid], (), ledger, runtime, True); need(PHYSICAL_MODEL is not None, "task179:direct_model_adapter"); direct_row, direct_public = PHYSICAL_MODEL.direct_column([], seed_words[sid]); need(isinstance(direct_row, dict) and aggregate_tagged(raw, ledger) == direct_row, "task179:direct_column_eleven_aggregate"); rise, row, ancestry, detail = insert(raw, formal, rows, forms, pivot_order); 
        if rise: traces[pivot_order[-1]] = detail
        seeds.append({"seed_id": sid, "raw_occurrence_vector": raw, "input_ancestry": formal, "literal_seed_word": seed_words[sid], "rank_rise": rise, "direct_conjugate_replay": "task179_direct_column_owner_authenticated", "reduction_trace": detail.get("reduction_trace", [])})
        seeds[-1]["direct_conjugate_replay"] = True; seeds[-1]["direct_aggregate_replay"] = True
        if rise: queue.append({"raw": row, "formal": ancestry, "seed_id": sid, "detail": detail})
    cursor = 0
    while cursor < len(queue):
        current = queue[cursor]; cursor += 1
        for letter in action_order:
            candidate_ancestry = formal_action(current["formal"], letter)
            raw = apply_actor(current["raw"], letter, ledger)
            direct_candidate_raw = evaluate_formal(candidate_ancestry, seed_words, ledger, runtime, action_cache)
            need(raw == direct_candidate_raw, "closure:candidate_direct_replay")
            rise, row, ancestry, detail = insert(raw, candidate_ancestry, rows, forms, pivot_order); 
            if rise: traces[pivot_order[-1]] = detail
            transitions.append({"from_queue_index": cursor - 1, "action": letter, "rank_rise": rise, "input_raw": current["raw"], "input_ancestry": current["formal"], "actor": letter, "candidate_raw": raw, "direct_candidate_raw": direct_candidate_raw, "candidate_direct_replay": True, "candidate_ancestry": candidate_ancestry, "reduced_ancestry": ancestry, "raw_occurrence_vector": raw, "ancestry": ancestry, "pivot": detail.get("pivot"), "normalization_scale": detail.get("normalization_scale"), "reduction_trace": detail.get("reduction_trace", []), "remainder": detail.get("remainder", {}), "change_of_basis": ancestry})
            if rise: queue.append({"raw": row, "formal": ancestry, "seed_id": current["seed_id"], "detail": detail}); cap(len(queue) <= MAX_QUEUE, "closure_queue_cap")
    basis = []
    for pivot in pivot_order:
        ancestry = forms[pivot]; need(evaluate_formal(ancestry, seed_words, ledger, runtime, action_cache) == rows[pivot], "closure:basis_direct_replay")
        ancestry = forms[pivot]; basis.append({"pivot": pivot, "earliest_pivot": pivot, "raw_occurrence_vector": rows[pivot], "ancestry": [{"seed_id": k.split("|", 1)[0], "coefficient": v, "action_word": [int(x) for x in k.split("|", 1)[1].split(",") if x], "multiplication_order": "g*c*g^-1"} for k, v in sorted(ancestry.items())], "direct_replay": True, "reduction_trace": traces[pivot].get("reduction_trace", []), "normalization_scale": traces[pivot].get("normalization_scale"), "change_of_basis": ancestry})
    active_keys = sorted({key for row in rows.values() for key in row})
    return {"rank": len(basis), "seeds": seeds, "basis": basis, "pivot_order": pivot_order, "action_order": list(action_order), "transitions": transitions, "queue_exhausted": True, "raw_coordinate_count": len(active_keys), "active_coordinate_roster": active_keys, "action_precompute": {"cached_seed_action_terms": len(action_cache), "direct_replay_per_unique_ancestry": True}, "terminal": PASS}
def structural_roster(ledger: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [{"ordinal": int(item["ordinal"]), "block": item["block"], "type": item["type"], "component_domain": "PB3_component" if item["type"] == "E3" else "PB4_component", "factor_sign": int(item["factor_sign"]), "orientation": item["orientation"], "prefix": list(item.get("fox_prefix_occurrences", ())), "key_grammar": "o<ordinal>:<component>:<element>", "quotient_owner": item["type"], "order": int(item["ordinal"])} for item in ledger]
def seal(value: dict[str, Any]) -> bytes:
    body = dict(value); body.setdefault("checkpoint", None)
    if body.get("schema") == SCHEMA and isinstance(body.get("occurrence_roster"), list): body["raw_coordinate_roster"] = structural_roster(body["occurrence_roster"])
    body["self_digest_sha256"] = digest(body); raw = canonical(body); cap(len(raw) <= MAX_OUTPUT_BYTES, "output_byte_cap"); return raw
def atomic(path: Path, raw: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=path.parent, prefix=".crel-", delete=False) as stream: stream.write(raw); temporary = Path(stream.name)
    temporary.replace(path)
def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(); p.add_argument("--mode", required=True); p.add_argument("--task382-receipt", required=True); p.add_argument("--task382-receipt-bytes", type=int, required=True); p.add_argument("--task382-receipt-sha256", required=True); p.add_argument("--task382-verdict", required=True); p.add_argument("--task382-verdict-bytes", type=int, required=True); p.add_argument("--task382-verdict-sha256", required=True); p.add_argument("--output", required=True); p.add_argument("--checkpoint", required=True); return p
def main() -> int:
    args = parser().parse_args(); output = None
    try:
        need(args.mode == "PRODUCTION", "mode:production_only"); output = output_path(args.output); need(not output.exists(), "output:stale"); receipt, verdict, rr, vr = load_inputs(args); task382_owner, frozen_owner, authority, runtime, meter = restore_runtime(); ledger = occurrence_roster(authority, frozen_owner, task382_owner); c_rel = receipt.get("C_rel"); need(isinstance(c_rel, dict) and isinstance(c_rel.get("basis"), list) and c_rel.get("basis") is not None, "task382:C_rel_basis"); seeds = c_rel["basis"]; need(all(isinstance(item, dict) and isinstance(item.get("seed_id"), str) and isinstance(item.get("literal_commutator_word"), list) and isinstance(item.get("full_K_vector"), dict) for item in seeds), "task382:C_rel_seed_fields"); result = closure(seeds, runtime, ledger, (1, -1, 2, -2)); body = {"schema": SCHEMA, "status": "COMPLETE", "terminal": PASS, "complete": True, "task382": {"receipt": {"path": args.task382_receipt, "bytes": len(rr), "sha256": digest_bytes(rr)}, "verdict": {"path": args.task382_verdict, "bytes": len(vr), "sha256": digest_bytes(vr)}}, "occurrence_roster": ledger, "C_rel_basis_count": len(seeds), "closure": result, "claim_boundary": {"W_C_computed": True, "raw_occurrence_space": True, "actual_L_over_JL": False, "leading_onto": False, "compatible_lift": False, "fake": False, "Ihara_witness": False}, "resource_caps": {"input_bytes_each": MAX_INPUT_BYTES, "output_bytes": MAX_OUTPUT_BYTES, "queue_rows": MAX_QUEUE, "literal_word": MAX_WORD, "frozen_runtime": meter.public()}}; atomic(output, seal(body)); print(PREFIX + " " + PASS, flush=True); return 0
    except (InputStop, ResourceStop) as exc:
        status = UNKNOWN_RESOURCE if isinstance(exc, ResourceStop) else UNKNOWN_INPUT
        if output is not None and not output.exists(): atomic(output, seal({"schema": SCHEMA, "status": status, "terminal": status, "complete": False, "reason": str(exc), "claim_boundary": {"W_C_computed": False, "actual_L_over_JL": False, "leading_onto": False, "compatible_lift": False, "fake": False, "Ihara_witness": False}, "checkpoint": None}))
        print(PREFIX + " " + status + ":" + str(exc).replace(" ", "_"), flush=True); return 0
    except (MemoryError, TimeoutError) as exc:
        status = UNKNOWN_RESOURCE
        if output is not None and not output.exists(): atomic(output, seal({"schema": SCHEMA, "status": status, "terminal": status, "complete": False, "reason": str(exc), "claim_boundary": {"W_C_computed": False, "actual_L_over_JL": False, "leading_onto": False, "compatible_lift": False, "fake": False, "Ihara_witness": False}, "checkpoint": None}))
        print(PREFIX + " " + status + ":" + str(exc).replace(" ", "_"), flush=True); return 0
if __name__ == "__main__": raise SystemExit(main())
