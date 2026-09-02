#!/usr/bin/env python3
"""Task529: exact-schema repair of the task445 lazy K=0 successor."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import tempfile
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "d972-r07-a0-actual-tau-free-lazy-k0-seed/v6"
CP_SCHEMA = SCHEMA + "/checkpoint"
MARKER = "R07_A0_ACTUAL_TAU_FREE_LAZY_K0_SEED_V6"
BASE = ("search/d972_r07_a0_actual_tau_free_rank_ladder_v3.py", 12215,
        "0140447110cfa568a77300bd7d43d51c622597704b7b91ed5209c63168c9ef37")
OLD_CHECKER = ("crosscheck/check_d972_r07_a0_actual_tau_free_rank_ladder_v7.py", 3653,
               "e1b80c586985f5113b300508f6bc78d055a37243e3fd6795b8f81148b0988de1")
PAPER = ("sol/proof_r07_lazy_positive_formula_seed_selector_v433.md", 10495,
         "3a8b5085e3a0a712dfd32c246cf472ca16616a2e3d7af494e4fcc8b30d02d940")
AUDIT = ("sol/sol_reply_524_audit_r07_lazy_positive_compact_seed_selector_v433.md", 13304,
         "3b028e05ac74310a2001494e0d112d0ab389bee82b83c5b8ed7cb84a91c39af5")
ROSTER_COUNT = 44
ROSTER_SHA256 = "7612682d024b61f873928ad122c9a5d7462c812a6633112f08706cda4412b6c8"
LEGACY_BYTES = 85934
LEGACY_SHA256 = "69a7ec3da4907f24af0f68c1975538b9ff9b6102f14e334f7c0725d2542dfd93"
LEGACY_PREFIX_SHA256 = "684039158b841d607aa40617778b9267ea96d64a38d952f74e63791b23ea3932"
LEGACY_STATE_SHA256 = "3e0d4bc8e2f9a467a0e50ad8435a7360e1953c2baee369225d8aa6fd71379610"
LEGACY_ACCEPTED = 68
LEGACY_RANK = 111
LEGACY_ROUND = 73
LEGACY_DUAL = "56ccd1f3cc6b54fe340a69ce6a0ec99f5aeb3358ae80288c6b11c3f1ec664864"
LEGACY_REMAINDER = "9eed8114d9e3172c7a11153d9c5cd6e5fc2e5184a8d6e3681cce5c82a83b4326"
LEGACY_REASON = "UNKNOWN_RESOURCE:tau_free_formula_seed:time_limit"
COUNTER_KEYS = ("seeds_touched", "formulas_compiled", "support_fibres",
                "kernel_candidates", "identity_replays", "adds", "updates")
HEX = set("0123456789abcdef")


class InvariantFailure(RuntimeError):
    pass


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def need(ok: Any, message: str) -> None:
    if not ok:
        raise RuntimeError(message)


def inv(ok: Any, message: str) -> None:
    if not ok:
        raise InvariantFailure(message)


def resource(message: str) -> None:
    raise RuntimeError("UNKNOWN_RESOURCE:" + message)


def raw_pin(spec: tuple[str, int, str]) -> bytes:
    raw = (ROOT / spec[0]).read_bytes()
    need(len(raw) == spec[1] and sha(raw) == spec[2], "pin:" + spec[0])
    return raw


def load(spec: tuple[str, int, str], name: str):
    path = ROOT / spec[0]
    raw = raw_pin(spec)
    loader = importlib.util.spec_from_file_location(name, path)
    need(loader is not None and loader.loader is not None, "loader:" + spec[0])
    module = importlib.util.module_from_spec(loader)
    loader.loader.exec_module(module)
    return module


base = load(BASE, "task529_task445_v3")
PIN_BINDING = {
    "schema": SCHEMA,
    "task445": {"path": BASE[0], "bytes": BASE[1], "sha256": BASE[2]},
    "checker_v7": {"path": OLD_CHECKER[0], "bytes": OLD_CHECKER[1], "sha256": OLD_CHECKER[2]},
    "paper_v433": {"path": PAPER[0], "bytes": PAPER[1], "sha256": PAPER[2]},
    "audit_524": {"path": AUDIT[0], "bytes": AUDIT[1], "sha256": AUDIT[2]},
    "compact_roster": {"count": ROSTER_COUNT, "sha256": ROSTER_SHA256},
    "legacy_input": {"bytes": LEGACY_BYTES, "sha256": LEGACY_SHA256,
                     "prefix_sha256": LEGACY_PREFIX_SHA256},
}
BINDING = sha(canonical(PIN_BINDING))


def verify_authorities() -> None:
    for spec in (BASE, OLD_CHECKER, PAPER, AUDIT):
        raw_pin(spec)


def hex64(value: Any) -> bool:
    return isinstance(value, str) and len(value) == 64 and set(value) <= HEX


def exact_int(value: Any, message: str) -> int:
    need(type(value) is int, message)
    return value


def exact_int_list(value: Any, length: int | None, message: str) -> list[int]:
    need(isinstance(value, list) and (length is None or len(value) == length) and
         all(type(item) is int for item in value), message)
    return value


def reject_noninteger_numbers(value: Any, message: str) -> None:
    need(type(value) not in (bool, float), message)
    if isinstance(value, dict):
        for key, item in value.items():
            reject_noninteger_numbers(item, message + ":" + str(key))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            reject_noninteger_numbers(item, message + ":" + str(index))


def zero_counters() -> dict[str, int]:
    return {key: 0 for key in COUNTER_KEYS}


def add_counters(left: dict[str, int], right: dict[str, int]) -> dict[str, int]:
    validate_counters(left)
    validate_counters(right)
    return {key: left[key] + right[key] for key in COUNTER_KEYS}


def validate_counters(value: Any) -> dict[str, int]:
    need(isinstance(value, dict) and set(value) == set(COUNTER_KEYS), "counter shape")
    need(all(type(value[key]) is int and value[key] >= 0 for key in COUNTER_KEYS),
         "counter type")
    return value


def validate_progress(value: Any) -> dict[str, Any]:
    need(isinstance(value, dict), "selector progress")
    reject_noninteger_numbers(value, "selector progress numeric type")
    for key in ("round", "seed_index", "fibre_ordinal", "coordinate",
                "kernel_ordinal", "record_index"):
        if key in value:
            exact_int(value[key], "selector progress integer:" + key)
    return value


def validate_new_source(source: dict[str, Any]) -> dict[str, Any]:
    need(isinstance(source, dict), "new record object")
    reject_noninteger_numbers(source, "new record numeric type")
    for key in ("round", "old_rank", "new_rank", "scalar", "record_version",
                "direct_scalar"):
        exact_int(source.get(key), "new record integer:" + key)
    base.b.validate_source(source)
    need(source["record_version"] == 6, "new record version")
    counters = validate_counters(source.get("selector_counters"))
    need(counters["adds"] == counters["updates"] == 1, "one add/update")
    need(counters["identity_replays"] == 0, "no eager identity replay")
    need(source.get("direct_scalar") == source.get("scalar") in (1, 2), "direct scalar")
    need(hex64(source.get("literal_delta_digest")), "literal delta digest")
    if source["kind"] == "action":
        need(source.get("selector_mode") == "ACTION", "action selector mode")
        action_source = source.get("action_source")
        need(isinstance(action_source, dict), "action source object")
        exact_int(action_source.get("family_index"), "action source family index")
        exact_int(action_source.get("scalar"), "action source scalar")
        need(all(counters[key] == 0 for key in ("seeds_touched", "formulas_compiled",
                                                "support_fibres", "kernel_candidates")),
             "action zero formula work")
    else:
        for key in ("seed_index", "K", "formula_scalar", "checked_fibres"):
            exact_int(source.get(key), "correction integer:" + key)
        delta = exact_int_list(source.get("delta_word"), None,
                               "delta integer typing")
        need(all(letter in (1, -1, 2, -2) for letter in delta), "delta alphabet")
        exponent = exact_int_list(source.get("exact_exponent_pair"), 2,
                                  "exact exponent integer typing")
        need(source.get("selector_mode") == "K0_SUPPORT" and source["K"] == 0,
             "K0-only correction")
        need(hex64(source.get("seed_digest")) and hex64(source.get("formula_digest")) and
             hex64(source.get("support_schedule_digest")) and
             hex64(source.get("kernel_schedule_digest")) and
             hex64(source.get("coordinate_blobs_digest")), "selector digests")
        need(source["formula_scalar"] == source["scalar"], "formula scalar")
        n_coefficients = exact_int_list(source.get("N_coefficients"), 2,
                                        "N coefficient integer typing")
        need(all(x in (0, 1, 2) for x in n_coefficients), "N coefficients")
        quotients = exact_int_list(source.get("normalized_exponent_quotients"), 2,
                                   "epsilon quotient integer typing")
        need(exponent == [18 * x for x in quotients], "epsilon/18 typing")
        coords = exact_int_list(source.get("required_coordinates"), None,
                                "coordinate integer typing")
        need(coords == sorted(set(coords)) and
             all(x in (0, 1, 2) for x in coords), "recognized coordinates")
        cursor = source.get("support_cursor")
        need(isinstance(cursor, dict), "support cursor object")
        for key in ("fibre_ordinal", "coordinate", "kernel_ordinal",
                    "q0_state_id", "gamma_state_id"):
            exact_int(cursor.get(key), "support cursor integer:" + key)
        need(cursor["coordinate"] in (0, 1, 2) and
             cursor["fibre_ordinal"] >= 0 and
             0 <= cursor["kernel_ordinal"] < 9 and
             isinstance(cursor.get("target_hex"), str) and
             cursor["q0_state_id"] > 0 and cursor["gamma_state_id"] > 0,
             "support cursor")
        need(counters["seeds_touched"] == counters["formulas_compiled"] and
             1 <= counters["formulas_compiled"] <= ROSTER_COUNT and
             counters["kernel_candidates"] >= 1, "lazy counters")
    return source


def validate_new_round_chain(records: Any, terminal_round: Any = None) -> int:
    need(isinstance(records, list), "new round chain records")
    previous = LEGACY_ROUND
    for index, record in enumerate(records):
        need(isinstance(record, dict), "new round chain record")
        current = exact_int(record.get("round"), "new round integer:%d" % index)
        need(current > previous, "new round strict chain:%d" % index)
        previous = current
    if terminal_round is not None:
        current_terminal = exact_int(terminal_round, "checkpoint/result round integer")
        need(current_terminal >= previous, "checkpoint/result round tail")
    return previous


def legacy_metadata() -> dict[str, Any]:
    return {"bytes": LEGACY_BYTES, "sha256": LEGACY_SHA256,
            "prefix_sha256": LEGACY_PREFIX_SHA256, "accepted_count": LEGACY_ACCEPTED,
            "rank": LEGACY_RANK, "round": LEGACY_ROUND,
            "dual_digest": LEGACY_DUAL, "remainder_digest": LEGACY_REMAINDER}


def validate_legacy_object(state: dict[str, Any]) -> dict[str, Any]:
    need(state.get("schema") == base.CP_SCHEMA and state.get("binding") == base.BINDING,
         "legacy schema/binding")
    body = dict(state)
    seal = body.pop("state_sha256", None)
    need(seal == LEGACY_STATE_SHA256 == sha(canonical(body)), "legacy state seal")
    accepted = state.get("accepted_sources")
    need(isinstance(accepted, list) and len(accepted) == LEGACY_ACCEPTED and
         state.get("accepted_count") == LEGACY_ACCEPTED, "legacy accepted count")
    need(sha(canonical(accepted)) == LEGACY_PREFIX_SHA256, "legacy exact prefix")
    need(state.get("rank") == LEGACY_RANK and state.get("round") == LEGACY_ROUND and
         state.get("reason") == LEGACY_REASON, "legacy rank/round/reason")
    profile = state.get("current_dual_profile")
    need(isinstance(profile, dict) and profile.get("dual_digest") == LEGACY_DUAL and
         profile.get("remainder_digest") == LEGACY_REMAINDER and
         profile.get("normalized_exponents") == {"N1": 0, "N2": 0} and
         profile.get("tau_coefficients") == {"1": 0, "2": 0, "3": 0} and
         profile.get("unrecognized_keys") == [], "legacy K0 profile")
    [base.b.validate_source(source) for source in accepted]
    return state


def parse_legacy(raw: bytes) -> dict[str, Any]:
    need(len(raw) == LEGACY_BYTES and sha(raw) == LEGACY_SHA256, "legacy outer pin")
    return validate_legacy_object(json.loads(raw))


def checkpoint_body(accepted: list[dict[str, Any]], round_no: int, rank: int,
                    reason: str | None, profile: dict[str, Any] | None,
                    counters: dict[str, int], attempt: dict[str, int],
                    progress: dict[str, Any]) -> dict[str, Any]:
    need(isinstance(accepted, list), "checkpoint accepted list")
    exact_int(round_no, "checkpoint round integer")
    exact_int(rank, "checkpoint rank integer")
    need(rank == 43 + len(accepted), "checkpoint generated rank")
    validate_new_round_chain(accepted[LEGACY_ACCEPTED:], round_no)
    validate_counters(counters)
    validate_counters(attempt)
    validate_progress(progress)
    state = {"schema": CP_SCHEMA, "binding": BINDING,
             "legacy_input": legacy_metadata(), "accepted_sources": accepted,
             "accepted_count": len(accepted), "round": round_no, "rank": rank,
             "reason": reason, "current_dual_profile": profile,
             "counters": counters, "attempt_counters": attempt,
             "selector_progress": progress}
    state["state_sha256"] = sha(canonical(state))
    return state


def validate_checkpoint(state: dict[str, Any]) -> dict[str, Any]:
    need(state.get("schema") == CP_SCHEMA and state.get("binding") == BINDING,
         "checkpoint schema/binding")
    body = dict(state)
    seal = body.pop("state_sha256", None)
    need(hex64(seal) and seal == sha(canonical(body)), "checkpoint state seal")
    reject_noninteger_numbers(state.get("legacy_input"), "legacy binding numeric type")
    need(state.get("legacy_input") == legacy_metadata(), "legacy binding")
    accepted = state.get("accepted_sources")
    exact_int(state.get("accepted_count"), "checkpoint accepted count integer")
    exact_int(state.get("rank"), "checkpoint rank integer")
    exact_int(state.get("round"), "checkpoint round integer")
    need(isinstance(accepted, list) and state["accepted_count"] == len(accepted) and
         len(accepted) >= LEGACY_ACCEPTED, "checkpoint accepted count")
    need(sha(canonical(accepted[:LEGACY_ACCEPTED])) == LEGACY_PREFIX_SHA256,
         "checkpoint legacy prefix")
    need(state["rank"] == 43 + len(accepted) and state["round"] >= LEGACY_ROUND,
         "checkpoint rank/round")
    [base.b.validate_source(source) for source in accepted[:LEGACY_ACCEPTED]]
    [validate_new_source(source) for source in accepted[LEGACY_ACCEPTED:]]
    for index, source in enumerate(accepted):
        need(source["old_rank"] == 43 + index and source["new_rank"] == 44 + index,
             "checkpoint rank chain")
    validate_new_round_chain(accepted[LEGACY_ACCEPTED:], state["round"])
    validate_counters(state.get("counters"))
    validate_counters(state.get("attempt_counters"))
    validate_progress(state.get("selector_progress"))
    return state


def read_resume(path: str) -> tuple[dict[str, Any], bool]:
    source = Path(path)
    need(not source.is_absolute() and source.parent == Path("ci/out"), "resume path")
    raw = source.read_bytes()
    parsed = json.loads(raw)
    if parsed.get("schema") == base.CP_SCHEMA:
        return parse_legacy(raw), True
    return validate_checkpoint(parsed), False


def write_checkpoint(path: str, state: dict[str, Any]) -> dict[str, Any]:
    need(path, "checkpoint required")
    target = Path(path)
    need(not target.is_absolute() and target.parent == Path("ci/out"), "checkpoint path")
    target.parent.mkdir(parents=True, exist_ok=True)
    raw = canonical(state) + b"\n"
    with tempfile.NamedTemporaryFile(dir=target.parent, delete=False) as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
        temporary = Path(stream.name)
    os.replace(temporary, target)
    return {"path": str(target), "bytes": len(raw), "sha256": sha(raw),
            "accepted_count": state["accepted_count"], "rank": state["rank"],
            "binding": BINDING}


def roster_gate(count: int, digest: str) -> None:
    inv(count == ROSTER_COUNT and digest == ROSTER_SHA256, "compact roster")


def authenticate_roster(P: dict[str, Any]) -> None:
    words = [list(word) for word in P["pres"]["relators"]]
    roster_gate(len(words), sha(canonical(words)))


def setup(args: argparse.Namespace, started: float):
    v1 = base.load(base.b.V1, "task529_state_v1")
    v4 = v1.load(v1.V4, "task529_state_v4")
    m = v4.load_v1()
    m.RUN_STARTED = started
    m.MARKER = MARKER
    v12 = m.load(m.V12, "task529_v12")
    p435 = m.load(m.P435, "task529_p435")
    p179 = m.load(m.P179, "task529_p179")
    P = v4.adapt(m, m.prefix(v12, p435, args))
    P["started"] = started
    authenticate_roster(P)
    return v1, m, p179, P, base.b.update(P, m)


def anchor_legacy(P: dict[str, Any], state: tuple[Any, Any, Any]) -> None:
    dual, remainder, _ = state
    inv(len(P["phys"].order) == LEGACY_RANK and dual is not None and
        P["v12"].row_digest(dual) == LEGACY_DUAL and
        P["v12"].row_digest(remainder) == LEGACY_REMAINDER,
        "legacy replay anchor")


def formula_for_seed(P: dict[str, Any], m: Any, model: Any, raw: dict[bytes, int],
                     seed_index: int, adjoint_digest: str) -> dict[str, Any]:
    word = list(P["pres"]["relators"][seed_index - 1])
    occurrence = model.occurrence_data(word, raw)
    ex, ey = P["v12"].v3.exp_pair(word)
    inv(ex % 18 == 0 and ey % 18 == 0, "seed normalized exponent")
    n = [int(P["dual"].get(b"N\x01", 0)) % 3,
         int(P["dual"].get(b"N\x02", 0)) % 3]
    quotients = [ex // 18, ey // 18]
    constant = (n[0] * quotients[0] + n[1] * quotients[1]) % 3
    merged = {(int(coordinate), target): int(value) % 3
              for (coordinate, target), value in occurrence["merged"].items()
              if int(value) % 3}
    public_merged = [[coordinate, target.hex(), value]
                     for (coordinate, target), value in
                     sorted(merged.items(), key=lambda item: (item[0][0], item[0][1]))]
    seed_digest = sha(canonical(word))
    body = {"seed_index": seed_index, "seed_digest": seed_digest,
            "adjoint_digest": adjoint_digest, "K": constant,
            "N_coefficients": n, "normalized_exponent_quotients": quotients,
            "merged": public_merged}
    return {"seed_index": seed_index, "word": word, "merged": merged,
            "required_coordinates": sorted({coordinate for coordinate, _ in merged}),
            "K": constant, "N_coefficients": n,
            "normalized_exponent_quotients": quotients,
            "seed_digest": seed_digest, "formula_digest": sha(canonical(body)),
            "support_schedule_digest": sha(canonical(public_merged))}


def formula_scalar(formula: dict[str, Any], blobs: Any) -> int:
    return (int(formula["K"]) + sum(value for (coordinate, target), value in
            formula["merged"].items() if blobs[coordinate] == target)) % 3


def kernel_digest(states: list[dict[str, Any]]) -> str:
    public = [{"source_word": list(state["source_word"]),
               "coordinate_blobs": [blob.hex() for blob in state["coordinate_blobs"]]}
              for state in states]
    return sha(canonical(public))


def support_states(sf: Any, coordinate: int) -> list[dict[str, Any]]:
    orders = tuple(getattr(sf, "kernel_orders", ()))
    if len(orders) <= coordinate or orders[coordinate] != 9:
        resource("UNSUPPORTED_KERNEL_ORDER:S%d" % coordinate)
    states = list(sf.ensure_kernel_prefix(coordinate, 9))
    identities = {tuple(state["coordinate_blobs"]) for state in states}
    if len(states) != 9 or len(identities) != 9:
        resource("UNSUPPORTED_KERNEL_ORDER:S%d" % coordinate)
    return states


def direct_correction(P: dict[str, Any], p179: Any, sf: Any,
                      formula: dict[str, Any], candidate: dict[str, Any],
                      scalar: int, cursor: dict[str, Any], checked: int,
                      route: dict[str, int], adjoint_digest: str,
                      schedule_digest: str) -> dict[str, Any]:
    delta = list(candidate["source_word"])
    blobs = tuple(candidate["coordinate_blobs"])
    inv(tuple(p179.coordinate_blobs(sf.rt, delta)) == blobs, "literal coordinates")
    conjugate = p179.reduce_word(delta + formula["word"] + p179.inverse_word(delta))
    row = P["v12"].aggregate(P["v12"].replay_atom(
        formula["seed_index"], delta, P["runtime"], P["model"], P["pres"],
        P["owner"], P["p176"], P["q"]))
    fresh = P["v12"].aggregate(P["v12"].seed_v12(
        P["model"], P["runtime"].old, P["owner"], P["p176"], P["q"], conjugate))
    inv(row == fresh, "formula row/fresh mismatch")
    ex, ey = P["v12"].v3.exp_pair(conjugate)
    inv(ex % 18 == 0 and ey % 18 == 0, "conjugate exponent typing")
    inv(all(not key.startswith(b"E") for key in row), "forbidden E coordinate")
    inv(all(not key.startswith(b"N") or len(key) == 2 and key[1] in (1, 2)
            for key in row), "N coordinate typing")
    direct = base.b.pair(P["dual"], row)
    inv(direct in (1, 2) and direct == scalar, "formula/direct scalar mismatch")
    reduced, _ = P["phys"].reduce(row)
    inv(bool(reduced), "dependent selected row")
    pivot = min(reduced)
    extra = {"record_version": 6, "selector_mode": "K0_SUPPORT",
             "seed_index": formula["seed_index"], "seed_digest": formula["seed_digest"],
             "formula_digest": formula["formula_digest"], "K": 0,
             "N_coefficients": formula["N_coefficients"],
             "normalized_exponent_quotients": [ex // 18, ey // 18],
             "required_coordinates": formula["required_coordinates"],
             "support_schedule_digest": formula["support_schedule_digest"],
             "kernel_schedule_digest": schedule_digest, "support_cursor": cursor,
             "delta_word": delta, "literal_delta_digest": sha(canonical(delta)),
             "literal_conjugate_digest": sha(canonical(conjugate)),
             "coordinate_blobs_digest": sha(canonical([blob.hex() for blob in blobs])),
             "exact_exponent_pair": [ex, ey], "adjoint_digest": adjoint_digest,
             "formula_scalar": scalar, "direct_scalar": direct,
             "checked_fibres": checked, "predicted_pivot": pivot.hex(),
             "selector_counters": route}
    source = {"family": "DIRECT_CORRECTION", "seed_index": formula["seed_index"],
              "delta_word": delta, "source_digest": P["v12"].row_digest(row)}
    return {"kind": "correction", "row": row, "scalar": direct, "source": source,
            "extra": extra, "predicted_pivot": pivot, "route": route}


def select_one(P: dict[str, Any], m: Any, p179: Any, state: tuple[Any, Any, Any],
               sf_holder: list[Any], args: argparse.Namespace,
               progress: dict[str, Any], route: dict[str, int]) -> dict[str, Any]:
    dual, remainder, _ = state
    actions = list(P["runtime"].old.pure_relations(4)[5:11])
    progress.clear(); progress.update({"phase": "actions"})
    for candidate, source0 in P["q"].action_support_hits(
            P["runtime"], P["owner"], P["p176"], actions, dual):
        row = P["v12"].action_row(P["runtime"], P["owner"], P["p176"], P["q"], source0)
        scalar = base.b.pair(dual, row)
        inv(row == candidate and scalar == int(source0["scalar"]) % 3 and scalar,
            "action direct scalar")
        reduced, _ = P["phys"].reduce(row)
        inv(bool(reduced), "dependent action row")
        pivot = min(reduced)
        route["adds"] = route["updates"] = 1
        extra = {"record_version": 6, "selector_mode": "ACTION",
                 "action_source": v1_public(source0),
                 "literal_delta_digest": sha(canonical([])), "direct_scalar": scalar,
                 "predicted_pivot": pivot.hex(), "selector_counters": route}
        return {"kind": "action", "row": row, "scalar": scalar, "source": source0,
                "extra": extra, "predicted_pivot": pivot, "route": route}
    profile = base.b.profile(P)
    if any(profile["tau_coefficients"].values()):
        resource("NONZERO_TAU_PHASE_SELECTOR")
    progress.clear(); progress.update({"phase": "adjoint"})
    raw, adjoint = base.tau_free_adjoint(P, m, args)
    model = m.model179(p179, P)
    m.budget_check(P, args, "lazy_k0_before_seed1")
    checked = 0
    for seed_index in range(1, ROSTER_COUNT + 1):
        progress.clear(); progress.update({"phase": "seed", "seed_index": seed_index})
        m.budget_check(P, args, "lazy_k0_seed")
        formula = formula_for_seed(P, m, model, raw, seed_index, adjoint["adjoint_digest"])
        route["seeds_touched"] += 1
        route["formulas_compiled"] += 1
        if formula["K"] != 0:
            resource("K_NONZERO_UNSUPPORTED:seed=%d" % seed_index)
        unsupported = [coordinate for coordinate in formula["required_coordinates"]
                       if coordinate not in (0, 1, 2)]
        if unsupported:
            resource("UNSUPPORTED_COORDINATE:S%s:seed=%d" %
                     (",".join(map(str, unsupported)), seed_index))
        for fibre_ordinal, (coordinate, target) in enumerate(sorted(
                formula["merged"], key=lambda item: (item[0], item[1]))):
            route["support_fibres"] += 1
            progress.clear(); progress.update({"phase": "fibre", "seed_index": seed_index,
                                                "fibre_ordinal": fibre_ordinal,
                                                "coordinate": coordinate,
                                                "target_hex": target.hex()})
            if sf_holder[0] is None:
                _, sf_holder[0] = m.selective_runtime(P, p179, args)
            sf = sf_holder[0]
            states = support_states(sf, coordinate)
            schedule_digest = kernel_digest(states)
            fibre = sf.canonical(coordinate, target)
            if fibre is None:
                continue
            for kernel_ordinal, eta in enumerate(states):
                progress["kernel_ordinal"] = kernel_ordinal
                m.budget_check(P, args, "lazy_k0_support_fibre")
                candidate = sf.kernel_candidate(fibre, eta)
                route["kernel_candidates"] += 1
                checked += 1
                scalar = formula_scalar(formula, candidate["coordinate_blobs"])
                if scalar == 0:
                    continue
                cursor = {"fibre_ordinal": fibre_ordinal, "coordinate": coordinate,
                          "target_hex": target.hex(), "kernel_ordinal": kernel_ordinal,
                          "q0_state_id": int(candidate["q0_state_id"]),
                          "gamma_state_id": int(candidate["gamma_state_id"])}
                route["adds"] = route["updates"] = 1
                return direct_correction(P, p179, sf, formula, candidate, scalar,
                                         cursor, checked, route,
                                         adjoint["adjoint_digest"], schedule_digest)
    resource("K0_NO_HIT")


def v1_public(source: dict[str, Any]) -> dict[str, Any]:
    return {str(key): (value.hex() if isinstance(value, bytes) else value)
            for key, value in source.items()
            if isinstance(value, (str, int, bool, list, dict, bytes))}


def commit(P: dict[str, Any], m: Any, accepted: list[dict[str, Any]], round_no: int,
           state: tuple[Any, Any, Any], selected: dict[str, Any]) -> tuple[dict[str, Any], tuple[Any, Any, Any]]:
    exact_int(round_no, "committed round integer")
    dual, remainder, _ = state
    old_rank = len(P["phys"].order)
    inv(dual is P["dual"] and remainder is P["remainder"] and
        base.b.pair(dual, selected["row"]) == selected["scalar"], "stale dual anchor")
    reduced, _ = P["phys"].reduce(selected["row"])
    inv(bool(reduced) and min(reduced) == selected["predicted_pivot"], "predicted pivot drift")
    row_digest = P["v12"].row_digest(selected["row"])
    physical_source = dict(selected["source"])
    physical_source["row_digest"] = row_digest
    rise, pivot = P["phys"].add(selected["row"], physical_source)
    inv(rise and pivot == selected["predicted_pivot"] and
        len(P["phys"].order) == old_rank + 1, "single physical add")
    post = base.b.update(P, m)
    post_dual, post_remainder, _ = post
    record = {"kind": selected["kind"], "round": round_no,
              "old_rank": old_rank, "new_rank": old_rank + 1,
              "scalar": selected["scalar"], "row_digest": row_digest,
              "pivot": pivot.hex(),
              "pre_remainder_digest": P["v12"].row_digest(remainder),
              "pre_dual_digest": P["v12"].row_digest(dual),
              "post_remainder_digest": P["v12"].row_digest(post_remainder),
              "post_dual_digest": None if post_dual is None else
                                  P["v12"].row_digest(post_dual)}
    record.update(selected["extra"])
    validate_new_source(record)
    accepted.append(record)
    return record, post


def replay_new(P: dict[str, Any], m: Any, p179: Any,
               accepted: list[dict[str, Any]], state: tuple[Any, Any, Any],
               args: argparse.Namespace) -> tuple[tuple[Any, Any, Any], dict[str, int]]:
    new_records = accepted[LEGACY_ACCEPTED:]
    validate_new_round_chain(new_records)
    counters = zero_counters()
    sf_holder: list[Any] = [None]
    authenticated_previous_round = LEGACY_ROUND
    for record in new_records:
        validate_new_source(record)
        authenticated_round = record["round"]
        inv(authenticated_round > authenticated_previous_round,
            "authenticated replay round chain")
        route = zero_counters()
        progress: dict[str, Any] = {}
        replay_args = argparse.Namespace(seconds=None, rss_bytes=None)
        selected = select_one(P, m, p179, state, sf_holder, replay_args, progress, route)
        inv(selected["kind"] == record["kind"] and
            selected["extra"] == {key: record[key] for key in selected["extra"]} and
            P["v12"].row_digest(selected["row"]) == record["row_digest"] and
            selected["scalar"] == record["scalar"] and
            selected["predicted_pivot"].hex() == record["pivot"], "new resume selector")
        generated, state = commit(P, m, [], authenticated_round, state, selected)
        inv(generated["round"] == authenticated_round and generated == record,
            "new resume authenticated-round record")
        authenticated_previous_round = authenticated_round
        counters = add_counters(counters, route)
        if sf_holder[0] is not None:
            sf_holder[0].cache.clear()
    return state, counters


def terminal(status: str, reason: str | None, accepted: list[dict[str, Any]],
             round_no: int, rank: int, profile: dict[str, Any] | None,
             counters: dict[str, int], attempt: dict[str, int],
             progress: dict[str, Any], seal: dict[str, Any], started: float,
             positive: Any = None) -> dict[str, Any]:
    exact_int(round_no, "result round integer")
    exact_int(rank, "result rank integer")
    need(rank == 43 + len(accepted), "result rank cardinality")
    validate_new_round_chain(accepted[LEGACY_ACCEPTED:], round_no)
    validate_counters(counters)
    validate_counters(attempt)
    validate_progress(progress)
    return {"schema": SCHEMA, "status": status, "terminal": status,
            "reason": reason, "accepted_sources": accepted,
            "accepted_count": len(accepted), "legacy_accepted_count": LEGACY_ACCEPTED,
            "round": round_no, "physical_rank": rank,
            "current_dual_profile": profile, "counters": counters,
            "attempt_counters": attempt, "selector_progress": progress,
            "terminal_replay": positive, "durable_state": seal,
            "claims": {"A0": status == "COMMON_CANDIDATE", "COMMON": False,
                       "NONMEMBER": False, "fake": False, "Ihara": False},
            "pins": PIN_BINDING, "elapsed_seconds": time.monotonic() - started}


def run(args: argparse.Namespace) -> dict[str, Any]:
    need(args.resume, "resume required")
    verify_authorities()
    started = time.monotonic()
    resume, legacy = read_resume(args.resume)
    v1, m, p179, P, state = setup(args, started)
    accepted = list(resume["accepted_sources"])
    round_no = resume["round"]
    state = base.replay(P, m, p179, accepted[:LEGACY_ACCEPTED], state)
    anchor_legacy(P, state)
    state, replayed_counters = replay_new(P, m, p179, accepted, state, args)
    inv(len(P["phys"].order) == 43 + len(accepted), "resume physical rank")
    counters = zero_counters() if legacy else validate_counters(resume["counters"])
    inv(counters == replayed_counters, "resume completed counters")
    new_rises = 0
    sf_holder: list[Any] = [None]
    attempt = zero_counters()
    progress: dict[str, Any] = {"phase": "migrated_legacy" if legacy else "resumed_v6"}
    profile = base.b.profile(P) if state[0] is not None else None
    state0 = checkpoint_body(accepted, round_no, len(P["phys"].order),
                             "initial_or_resumed", profile, counters, attempt, progress)
    seal = write_checkpoint(args.checkpoint, state0)
    while True:
        durable_rank = 43 + len(accepted)
        durable_profile = base.b.profile(P) if state[0] is not None else None
        attempt = zero_counters()
        progress = {"phase": "round_start"}
        try:
            dual, remainder, coefficient = state
            round_no += 1
            progress["round"] = round_no
            if dual is None:
                positive = v1.positive(P, m, coefficient)
                profile = None
                cp = checkpoint_body(accepted, round_no, durable_rank, None, profile,
                                     counters, attempt, {"phase": "common_candidate"})
                seal = write_checkpoint(args.checkpoint, cp)
                return terminal("COMMON_CANDIDATE", None, accepted, round_no,
                                durable_rank, profile, counters, attempt,
                                {"phase": "common_candidate"}, seal, started, positive)
            if new_rises >= args.max_rises:
                resource("max_rises")
            current = base.b.profile(P)
            if current["unrecognized_keys"]:
                resource("UNRECOGNIZED_DUAL_KEYS")
            selected = select_one(P, m, p179, state, sf_holder, args, progress, attempt)
            validate_new_round_chain(accepted[LEGACY_ACCEPTED:] + [{"round": round_no}])
            record, state = commit(P, m, accepted, round_no, state, selected)
            counters = add_counters(counters, selected["route"])
            new_rises += 1
            durable_rank = len(P["phys"].order)
            durable_profile = base.b.profile(P) if state[0] is not None else None
            if sf_holder[0] is not None:
                sf_holder[0].cache.clear()
            profile = durable_profile
            progress = {"phase": "rank_rise", "record_index": len(accepted),
                        "row_digest": record["row_digest"]}
            cp = checkpoint_body(accepted, round_no, len(P["phys"].order), "rank_rise",
                                 profile, counters, zero_counters(), progress)
            seal = write_checkpoint(args.checkpoint, cp)
            print(f"{MARKER} progress round={round_no} rank={len(P['phys'].order)} "
                  f"accepted_count={len(accepted)} new_rises={new_rises}", flush=True)
        except Exception as error:
            is_resource = isinstance(error, RuntimeError) and str(error).startswith("UNKNOWN_RESOURCE:")
            status = "UNKNOWN_RESOURCE" if is_resource else "UNKNOWN"
            reason = str(error) if is_resource else "INVARIANT:" + type(error).__name__ + ":" + str(error)
            cp = checkpoint_body(accepted, round_no, durable_rank, reason, durable_profile,
                                 counters, attempt, progress)
            seal = write_checkpoint(args.checkpoint, cp)
            return terminal(status, reason, accepted, round_no, durable_rank,
                            durable_profile, counters, attempt, progress, seal, started)


def schema_fixture_record() -> dict[str, Any]:
    return {"kind": "correction", "round": 74, "old_rank": 111,
            "new_rank": 112, "scalar": 1, "row_digest": "a" * 64,
            "pivot": "ab", "pre_remainder_digest": "b" * 64,
            "pre_dual_digest": "c" * 64, "post_remainder_digest": "d" * 64,
            "post_dual_digest": "e" * 64, "seed_index": 1,
            "delta_word": [1], "exact_exponent_pair": [0, 0],
            "adjoint_digest": "f" * 64, "record_version": 6,
            "selector_mode": "K0_SUPPORT", "K": 0, "direct_scalar": 1,
            "formula_scalar": 1, "literal_delta_digest": "1" * 64,
            "literal_conjugate_digest": "2" * 64, "seed_digest": "3" * 64,
            "formula_digest": "4" * 64, "support_schedule_digest": "5" * 64,
            "kernel_schedule_digest": "6" * 64,
            "coordinate_blobs_digest": "7" * 64,
            "N_coefficients": [0, 0], "normalized_exponent_quotients": [0, 0],
            "required_coordinates": [0],
            "support_cursor": {"fibre_ordinal": 0, "coordinate": 0,
                               "target_hex": "00", "kernel_ordinal": 0,
                               "q0_state_id": 1, "gamma_state_id": 1},
            "checked_fibres": 1, "predicted_pivot": "ab",
            "selector_counters": {"seeds_touched": 1, "formulas_compiled": 1,
                                  "support_fibres": 1, "kernel_candidates": 1,
                                  "identity_replays": 0, "adds": 1, "updates": 1}}


def fixture_mutation(source: dict[str, Any], path: tuple[Any, ...], value: Any) -> dict[str, Any]:
    changed = json.loads(canonical(source))
    target: Any = changed
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = value
    return changed


def fixture() -> dict[str, Any]:
    imported = base.fixture()
    need(imported["status"] == "PASS", "actual task445 fixture")
    roster_rejections = []
    for label, count, digest in (("43", 43, ROSTER_SHA256),
                                 ("45", 45, ROSTER_SHA256),
                                 ("6441", 6441, ROSTER_SHA256),
                                 ("digest", 44, "0" * 64)):
        try:
            roster_gate(count, digest)
        except InvariantFailure:
            roster_rejections.append(label)
    need(len(roster_rejections) == 4, "roster mutations")
    action = zero_counters(); action["adds"] = action["updates"] = 1
    need(action["formulas_compiled"] == action["identity_replays"] == 0,
         "action zero formula fixture")
    resource_rejections = []
    for label, value in (("K!=0", 1), ("K0", 0)):
        try:
            if value:
                resource("K_NONZERO_UNSUPPORTED:seed=1")
        except RuntimeError:
            resource_rejections.append(label)
    need(resource_rejections == ["K!=0"], "K branch fixture")
    sample = schema_fixture_record()
    validate_new_source(sample)
    numeric_rejections = []
    for label, path, value in (
            ("bool_scalar", ("scalar",), True),
            ("float_direct_scalar", ("direct_scalar",), 1.0),
            ("float_exponent", ("exact_exponent_pair", 0), 0.0),
            ("float_N", ("N_coefficients", 0), 0.0),
            ("bool_counter", ("selector_counters", "identity_replays"), False),
            ("float_cursor", ("support_cursor", "fibre_ordinal"), 0.0)):
        try:
            validate_new_source(fixture_mutation(sample, path, value))
        except RuntimeError:
            numeric_rejections.append(label)
    need(len(numeric_rejections) == 6, "exact integer mutation fixture")
    round_rejections = []
    round_cases = (
        ("first_1", [fixture_mutation(sample, ("round",), 1)]),
        ("first_73", [fixture_mutation(sample, ("round",), 73)]),
        ("duplicate", [sample, fixture_mutation(sample, ("round",), 74)]),
        ("decreasing", [fixture_mutation(sample, ("round",), 75), sample]),
        ("noninteger", [fixture_mutation(sample, ("round",), 74.0)]),
    )
    for label, records in round_cases:
        try:
            validate_new_round_chain(records)
        except RuntimeError:
            round_rejections.append(label)
    need(len(round_rejections) == 5, "strict round mutation fixture")
    return {"status": "PASS", "actual_imported_task445": BASE[2],
            "task445_fixture": imported, "roster_mutation_rejections": roster_rejections,
            "action_zero_formula_counters": action,
            "K_nonzero_is_resource": True, "identity_replays": 0,
            "exact_integer_mutation_rejections": numeric_rejections,
            "round_chain_mutation_rejections": round_rejections,
            "production_selector_function": "select_one"}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("PRODUCTION", "FIXTURE"), default="PRODUCTION")
    parser.add_argument("--output", default="ci/out/d972_r07_a0_actual_tau_free_lazy_k0_seed_v6.json")
    parser.add_argument("--checkpoint", default="ci/out/d972_r07_a0_actual_tau_free_lazy_k0_seed_v6_output.checkpoint")
    parser.add_argument("--resume")
    parser.add_argument("--seconds", type=float, default=7200)
    parser.add_argument("--rss-bytes", type=int, default=4_800_000_000)
    parser.add_argument("--max-rises", type=int, default=64)
    args = parser.parse_args(argv)
    try:
        result = {"schema": SCHEMA, "status": "FIXTURE", "fixture": fixture(),
                  "claims": {"A0": False, "COMMON": False, "NONMEMBER": False,
                             "fake": False, "Ihara": False}} if args.mode == "FIXTURE" else run(args)
    except Exception as error:
        result = {"schema": SCHEMA,
                  "status": "UNKNOWN_RESOURCE" if str(error).startswith("UNKNOWN_RESOURCE:") else "UNKNOWN",
                  "reason": str(error),
                  "claims": {"A0": False, "COMMON": False, "NONMEMBER": False,
                             "fake": False, "Ihara": False}}
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(canonical(result) + b"\n")
    print(f"{MARKER} status={result['status']}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
