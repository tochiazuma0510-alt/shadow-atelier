#!/usr/bin/env python3
"""Independent Task527 checker for the actual task445 lazy K=0 successor."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "d972-r07-a0-actual-tau-free-lazy-k0-seed/v5"
CP_SCHEMA = SCHEMA + "/checkpoint"
MARKER = "R07_A0_ACTUAL_TAU_FREE_LAZY_K0_SEED_V9_CHECKER"
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
LEGACY_ACCEPTED = 68
LEGACY_RANK = 111
LEGACY_ROUND = 73
LEGACY_DUAL = "56ccd1f3cc6b54fe340a69ce6a0ec99f5aeb3358ae80288c6b11c3f1ec664864"
LEGACY_REMAINDER = "9eed8114d9e3172c7a11153d9c5cd6e5fc2e5184a8d6e3681cce5c82a83b4326"
COUNTER_KEYS = ("seeds_touched", "formulas_compiled", "support_fibres",
                "kernel_candidates", "identity_replays", "adds", "updates")
HEX = set("0123456789abcdef")


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def need(ok: Any, message: str) -> None:
    if not ok:
        raise RuntimeError(message)


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


old = load(OLD_CHECKER, "task527_checker_v7")
legacy_checker = old.c.c.c.c
low = legacy_checker.c
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


def zero_counters() -> dict[str, int]:
    return {key: 0 for key in COUNTER_KEYS}


def add_counters(left: dict[str, int], right: dict[str, int]) -> dict[str, int]:
    return {key: int(left.get(key, 0)) + int(right.get(key, 0)) for key in COUNTER_KEYS}


def validate_counters(value: Any) -> dict[str, int]:
    need(isinstance(value, dict) and set(value) == set(COUNTER_KEYS) and
         all(isinstance(value[key], int) and value[key] >= 0 for key in COUNTER_KEYS),
         "counter shape/type")
    return value


def legacy_metadata() -> dict[str, Any]:
    return {"bytes": LEGACY_BYTES, "sha256": LEGACY_SHA256,
            "prefix_sha256": LEGACY_PREFIX_SHA256, "accepted_count": LEGACY_ACCEPTED,
            "rank": LEGACY_RANK, "round": LEGACY_ROUND,
            "dual_digest": LEGACY_DUAL, "remainder_digest": LEGACY_REMAINDER}


def validate_new_source(source: dict[str, Any]) -> dict[str, Any]:
    legacy_checker.validate(source)
    need(source.get("record_version") == 5 and
         source.get("direct_scalar") == source.get("scalar") in (1, 2),
         "new record version/direct scalar")
    counters = validate_counters(source.get("selector_counters"))
    need(counters["adds"] == counters["updates"] == 1 and
         counters["identity_replays"] == 0, "single update/no identity")
    need(hex64(source.get("literal_delta_digest")), "literal delta digest")
    if source["kind"] == "action":
        need(source.get("selector_mode") == "ACTION" and
             all(counters[key] == 0 for key in
                 ("seeds_touched", "formulas_compiled", "support_fibres",
                  "kernel_candidates")), "action-first counters")
    else:
        need(source.get("selector_mode") == "K0_SUPPORT", "correction selector mode")
        need(source.get("K") == 0, "selected K!=0 rejected")
        need(source.get("formula_scalar") == source.get("scalar"), "formula scalar field")
        need(all(hex64(source.get(key)) for key in
                 ("seed_digest", "formula_digest", "support_schedule_digest",
                  "kernel_schedule_digest", "coordinate_blobs_digest",
                  "literal_conjugate_digest", "adjoint_digest")), "selector digests")
        need(isinstance(source.get("N_coefficients"), list) and
             len(source["N_coefficients"]) == 2 and
             all(value in (0, 1, 2) for value in source["N_coefficients"]),
             "N coefficient typing")
        need(isinstance(source.get("normalized_exponent_quotients"), list) and
             len(source["normalized_exponent_quotients"]) == 2 and
             source.get("exact_exponent_pair") ==
             [18 * value for value in source["normalized_exponent_quotients"]],
             "epsilon/18 typing")
        coords = source.get("required_coordinates")
        need(isinstance(coords, list) and coords == sorted(set(coords)) and
             all(value in (0, 1, 2) for value in coords), "recognized coordinates")
        cursor = source.get("support_cursor")
        need(isinstance(cursor, dict) and cursor.get("coordinate") in (0, 1, 2) and
             isinstance(cursor.get("fibre_ordinal"), int) and cursor["fibre_ordinal"] >= 0 and
             isinstance(cursor.get("kernel_ordinal"), int) and 0 <= cursor["kernel_ordinal"] < 9 and
             isinstance(cursor.get("target_hex"), str) and
             isinstance(cursor.get("q0_state_id"), int) and cursor["q0_state_id"] > 0 and
             isinstance(cursor.get("gamma_state_id"), int) and cursor["gamma_state_id"] > 0,
             "support cursor")
        need(counters["seeds_touched"] == counters["formulas_compiled"] and
             1 <= counters["formulas_compiled"] <= ROSTER_COUNT and
             counters["kernel_candidates"] >= 1, "lazy counters")
    return source


def validate_checkpoint(state: dict[str, Any]) -> dict[str, Any]:
    need(isinstance(state, dict) and state.get("schema") == CP_SCHEMA and
         state.get("binding") == BINDING, "checkpoint schema/binding")
    body = dict(state)
    seal = body.pop("state_sha256", None)
    need(hex64(seal) and seal == sha(canonical(body)), "checkpoint internal seal")
    need(state.get("legacy_input") == legacy_metadata(), "checkpoint legacy binding")
    accepted = state.get("accepted_sources")
    need(isinstance(accepted, list) and state.get("accepted_count") == len(accepted) and
         len(accepted) >= LEGACY_ACCEPTED, "checkpoint accepted count")
    need(sha(canonical(accepted[:LEGACY_ACCEPTED])) == LEGACY_PREFIX_SHA256,
         "checkpoint exact legacy prefix")
    need(state.get("rank") == 43 + len(accepted) and
         isinstance(state.get("round"), int) and state["round"] >= LEGACY_ROUND,
         "checkpoint cardinality/round")
    [legacy_checker.validate(source) for source in accepted[:LEGACY_ACCEPTED]]
    [validate_new_source(source) for source in accepted[LEGACY_ACCEPTED:]]
    for index, source in enumerate(accepted):
        need(source["old_rank"] == 43 + index and source["new_rank"] == 44 + index,
             "checkpoint rank chain")
    if accepted:
        need(state["round"] >= max(source["round"] for source in accepted),
             "checkpoint round monotonicity")
    validate_counters(state.get("counters"))
    validate_counters(state.get("attempt_counters"))
    need(isinstance(state.get("selector_progress"), dict), "selector progress")
    return state


def read_checkpoint(cert: dict[str, Any]) -> dict[str, Any]:
    durable = cert.get("durable_state")
    need(isinstance(durable, dict) and isinstance(durable.get("path"), str),
         "durable state metadata")
    path = Path(durable["path"])
    need(not path.is_absolute() and path.parent == Path("ci/out"), "checkpoint path")
    raw = path.read_bytes()
    need(len(raw) == durable.get("bytes") and sha(raw) == durable.get("sha256") and
         durable.get("binding") == BINDING, "checkpoint outer seal")
    state = validate_checkpoint(json.loads(raw))
    equality = {"accepted_sources": "accepted_sources", "accepted_count": "accepted_count",
                "rank": "physical_rank", "round": "round", "reason": "reason",
                "current_dual_profile": "current_dual_profile", "counters": "counters",
                "attempt_counters": "attempt_counters",
                "selector_progress": "selector_progress"}
    for state_key, cert_key in equality.items():
        need(state.get(state_key) == cert.get(cert_key),
             "checkpoint/result equality:" + state_key)
    need(durable.get("accepted_count") == state["accepted_count"] and
         durable.get("rank") == state["rank"], "durable cardinality")
    return state


def setup():
    v1 = low.load(low.V1, "task527_check_state_v1")
    v4 = v1.load(v1.V4, "task527_check_state_v4")
    m = v4.load_v1()
    v12 = m.load(m.V12, "task527_check_v12")
    p435 = m.load(m.P435, "task527_check_p435")
    p179 = m.load(m.P179, "task527_check_p179")
    args = type("A", (), {"seconds": None, "rss_bytes": None})()
    P = v4.adapt(m, m.prefix(v12, p435, args))
    words = [list(word) for word in P["pres"]["relators"]]
    need(len(words) == ROSTER_COUNT and sha(canonical(words)) == ROSTER_SHA256,
         "independent compact roster")
    return v1, m, p179, P, legacy_checker.update(P, m)


def anchor_legacy(P: dict[str, Any], state: tuple[Any, Any, Any]) -> None:
    dual, remainder, _ = state
    need(len(P["phys"].order) == LEGACY_RANK and dual is not None and
         P["v12"].row_digest(dual) == LEGACY_DUAL and
         P["v12"].row_digest(remainder) == LEGACY_REMAINDER,
         "independent legacy replay anchor")


def formula_for_seed(P: dict[str, Any], model: Any, raw: dict[bytes, int],
                     seed_index: int, adjoint_digest: str) -> dict[str, Any]:
    word = list(P["pres"]["relators"][seed_index - 1])
    occurrence = model.occurrence_data(word, raw)
    ex, ey = P["v12"].v3.exp_pair(word)
    need(ex % 18 == 0 and ey % 18 == 0, "independent seed exponent")
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


def support_states(sf: Any, coordinate: int) -> list[dict[str, Any]]:
    orders = tuple(getattr(sf, "kernel_orders", ()))
    need(len(orders) > coordinate and orders[coordinate] == 9,
         "independent kernel order nine")
    states = list(sf.ensure_kernel_prefix(coordinate, 9))
    need(len(states) == 9 and len({tuple(row["coordinate_blobs"]) for row in states}) == 9,
         "independent frozen kernel schedule")
    return states


def kernel_digest(states: list[dict[str, Any]]) -> str:
    public = [{"source_word": list(state["source_word"]),
               "coordinate_blobs": [blob.hex() for blob in state["coordinate_blobs"]]}
              for state in states]
    return sha(canonical(public))


def public_source(source: dict[str, Any]) -> dict[str, Any]:
    return {str(key): (value.hex() if isinstance(value, bytes) else value)
            for key, value in source.items()
            if isinstance(value, (str, int, bool, list, dict, bytes))}


def first_action(P: dict[str, Any], dual: dict[bytes, int]):
    actions = list(P["runtime"].old.pure_relations(4)[5:11])
    for candidate, source in P["q"].action_support_hits(
            P["runtime"], P["owner"], P["p176"], actions, dual):
        row = P["v12"].action_row(P["runtime"], P["owner"], P["p176"], P["q"], source)
        scalar = low.pair(dual, row)
        need(row == candidate and scalar == int(source["scalar"]) % 3 and scalar,
             "independent action direct scalar")
        return row, scalar, source
    return None


def replay_correction(P: dict[str, Any], m: Any, p179: Any, sf: Any,
                      record: dict[str, Any]) -> tuple[dict[bytes, int], dict[str, int]]:
    need(first_action(P, P["dual"]) is None, "correction violates action-first")
    raw, adjoint = low.adjoint(P)
    need(adjoint["adjoint_digest"] == record["adjoint_digest"], "independent adjoint")
    model = m.model179(p179, P)
    route = zero_counters()
    checked = 0
    for seed_index in range(1, ROSTER_COUNT + 1):
        formula = formula_for_seed(P, model, raw, seed_index, adjoint["adjoint_digest"])
        route["seeds_touched"] += 1
        route["formulas_compiled"] += 1
        need(formula["K"] == 0, "selected K!=0 record")
        need(all(coordinate in (0, 1, 2) for coordinate in formula["required_coordinates"]),
             "selected unsupported coordinate")
        for fibre_ordinal, (coordinate, target) in enumerate(sorted(
                formula["merged"], key=lambda item: (item[0], item[1]))):
            route["support_fibres"] += 1
            states = support_states(sf, coordinate)
            schedule_digest = kernel_digest(states)
            fibre = sf.canonical(coordinate, target)
            if fibre is None:
                continue
            for kernel_ordinal, eta in enumerate(states):
                candidate = sf.kernel_candidate(fibre, eta)
                route["kernel_candidates"] += 1
                checked += 1
                scalar = formula_scalar(formula, candidate["coordinate_blobs"])
                if scalar == 0:
                    continue
                need(seed_index == record["seed_index"], "record is not first predicted seed")
                delta = list(candidate["source_word"])
                blobs = tuple(candidate["coordinate_blobs"])
                need(tuple(p179.coordinate_blobs(sf.rt, delta)) == blobs,
                     "independent literal coordinates")
                conjugate = p179.reduce_word(delta + formula["word"] +
                                             p179.inverse_word(delta))
                row = P["v12"].aggregate(P["v12"].replay_atom(
                    seed_index, delta, P["runtime"], P["model"], P["pres"],
                    P["owner"], P["p176"], P["q"]))
                fresh = P["v12"].aggregate(P["v12"].seed_v12(
                    P["model"], P["runtime"].old, P["owner"], P["p176"],
                    P["q"], conjugate))
                need(row == fresh, "independent row/fresh")
                ex, ey = P["v12"].v3.exp_pair(conjugate)
                need(ex % 18 == 0 and ey % 18 == 0 and
                     all(not key.startswith(b"E") for key in row) and
                     all(not key.startswith(b"N") or len(key) == 2 and key[1] in (1, 2)
                         for key in row), "independent exponent/N/E")
                direct = low.pair(P["dual"], row)
                need(direct in (1, 2) and direct == scalar, "independent formula/direct scalar")
                reduced, _ = P["phys"].reduce(row)
                need(bool(reduced), "independent dependent row")
                pivot = min(reduced).hex()
                cursor = {"fibre_ordinal": fibre_ordinal, "coordinate": coordinate,
                          "target_hex": target.hex(), "kernel_ordinal": kernel_ordinal,
                          "q0_state_id": int(candidate["q0_state_id"]),
                          "gamma_state_id": int(candidate["gamma_state_id"])}
                route["adds"] = route["updates"] = 1
                expected = {
                    "seed_digest": formula["seed_digest"],
                    "formula_digest": formula["formula_digest"], "K": 0,
                    "N_coefficients": formula["N_coefficients"],
                    "normalized_exponent_quotients": [ex // 18, ey // 18],
                    "required_coordinates": formula["required_coordinates"],
                    "support_schedule_digest": formula["support_schedule_digest"],
                    "kernel_schedule_digest": schedule_digest,
                    "support_cursor": cursor, "delta_word": delta,
                    "literal_delta_digest": sha(canonical(delta)),
                    "literal_conjugate_digest": sha(canonical(conjugate)),
                    "coordinate_blobs_digest": sha(canonical([blob.hex() for blob in blobs])),
                    "exact_exponent_pair": [ex, ey], "formula_scalar": scalar,
                    "direct_scalar": direct, "checked_fibres": checked,
                    "predicted_pivot": pivot, "selector_counters": route,
                }
                for key, value in expected.items():
                    need(record.get(key) == value, "independent selector field:" + key)
                return row, route
    raise RuntimeError("selected correction absent from complete K0 schedule")


def replay_new(P: dict[str, Any], m: Any, p179: Any,
               accepted: list[dict[str, Any]], state: tuple[Any, Any, Any]):
    counters = zero_counters()
    sf = None
    for record in accepted[LEGACY_ACCEPTED:]:
        validate_new_source(record)
        dual, remainder, _ = state
        need(dual is not None and len(P["phys"].order) == record["old_rank"] and
             P["v12"].row_digest(dual) == record["pre_dual_digest"] and
             P["v12"].row_digest(remainder) == record["pre_remainder_digest"],
             "independent new pre-state")
        if record["kind"] == "action":
            hit = first_action(P, dual)
            need(hit is not None, "missing recorded action")
            row, scalar, source = hit
            route = zero_counters(); route["adds"] = route["updates"] = 1
            need(public_source(source) == record["action_source"] and
                 scalar == record["scalar"] and record["selector_counters"] == route and
                 record["literal_delta_digest"] == sha(canonical([])),
                 "independent action record")
            physical_source = source
        else:
            if sf is None:
                _, sf = m.selective_runtime(
                    P, p179, type("A", (), {"seconds": None, "rss_bytes": None})())
            row, route = replay_correction(P, m, p179, sf, record)
            scalar = low.pair(dual, row)
            physical_source = {"family": "DIRECT_CORRECTION",
                               "seed_index": record["seed_index"],
                               "delta_word": record["delta_word"],
                               "source_digest": record["row_digest"]}
        need(P["v12"].row_digest(row) == record["row_digest"] and
             scalar == record["scalar"], "independent row/scalar")
        reduced, _ = P["phys"].reduce(row)
        need(bool(reduced) and min(reduced).hex() == record["predicted_pivot"] ==
             record["pivot"], "independent predicted pivot")
        source = dict(physical_source); source["row_digest"] = record["row_digest"]
        rise, pivot = P["phys"].add(row, source)
        need(rise and pivot.hex() == record["pivot"] and
             len(P["phys"].order) == record["new_rank"], "independent single add")
        state = legacy_checker.update(P, m)
        post_dual, post_remainder, _ = state
        need(P["v12"].row_digest(post_remainder) == record["post_remainder_digest"] and
             (None if post_dual is None else P["v12"].row_digest(post_dual)) ==
             record["post_dual_digest"], "independent post-state")
        counters = add_counters(counters, route)
        if sf is not None:
            sf.cache.clear()
    return state, counters


def reason_type(status: str, reason: Any) -> None:
    if status == "UNKNOWN_RESOURCE":
        need(isinstance(reason, str) and reason.startswith("UNKNOWN_RESOURCE:") and
             not reason.startswith("UNKNOWN_RESOURCE:INVARIANT:"), "resource reason type")
    elif status == "UNKNOWN":
        need(isinstance(reason, str) and reason.startswith("INVARIANT:"),
             "invariant reason type")
    else:
        need(reason is None, "common reason")


def check(cert: dict[str, Any]) -> None:
    verify_authorities()
    need(cert.get("schema") == SCHEMA and cert.get("status") in
         {"UNKNOWN_RESOURCE", "UNKNOWN", "COMMON_CANDIDATE"} and
         cert.get("terminal") == cert.get("status"), "schema/status/terminal")
    status = cert["status"]
    reason_type(status, cert.get("reason"))
    expected_claims = {"A0": status == "COMMON_CANDIDATE", "COMMON": False,
                       "NONMEMBER": False, "fake": False, "Ihara": False}
    need(cert.get("claims") == expected_claims and cert.get("pins") == PIN_BINDING and
         cert.get("legacy_accepted_count") == LEGACY_ACCEPTED, "claims/pins/legacy count")
    state_cp = read_checkpoint(cert)
    accepted = cert["accepted_sources"]
    need(cert["accepted_count"] == len(accepted) and
         cert["physical_rank"] == 43 + len(accepted), "terminal cardinality")
    v1, m, p179, P, state = setup()
    state = legacy_checker.replay(P, m, p179, accepted[:LEGACY_ACCEPTED], state)
    anchor_legacy(P, state)
    state, counters = replay_new(P, m, p179, accepted, state)
    need(counters == cert["counters"], "independent completed counters")
    need(len(P["phys"].order) == cert["physical_rank"], "independent physical rank")
    dual, remainder, coefficient = state
    if status == "COMMON_CANDIDATE":
        need(dual is None and cert.get("current_dual_profile") is None and
             v1.positive(P, m, coefficient) == cert.get("terminal_replay"),
             "independent COMMON candidate")
    else:
        need(dual is not None and cert.get("terminal_replay") is None,
             "noncommon dual boundary")
        legacy_checker.independent_profile(P, m, p179,
                                           cert.get("current_dual_profile"),
                                           cert.get("reason"))
    need(state_cp["accepted_count"] == len(accepted), "checked terminal state")


def self_test() -> dict[str, Any]:
    base_result = old.self_test()
    need(base_result["status"] == "PASS", "v7 imported self-test")
    rejected = []
    sample = {"kind": "correction", "round": 74, "old_rank": 111,
              "new_rank": 112, "scalar": 1, "row_digest": "a" * 64,
              "pivot": "ab", "pre_remainder_digest": "b" * 64,
              "pre_dual_digest": "c" * 64, "post_remainder_digest": "d" * 64,
              "post_dual_digest": "e" * 64, "seed_index": 1,
              "delta_word": [1], "exact_exponent_pair": [0, 0],
              "adjoint_digest": "f" * 64, "record_version": 5,
              "selector_mode": "K0_SUPPORT", "K": 0, "direct_scalar": 1,
              "formula_scalar": 1, "literal_delta_digest": "1" * 64,
              "literal_conjugate_digest": "2" * 64, "seed_digest": "3" * 64,
              "formula_digest": "4" * 64, "support_schedule_digest": "5" * 64,
              "kernel_schedule_digest": "6" * 64, "coordinate_blobs_digest": "7" * 64,
              "N_coefficients": [0, 0], "normalized_exponent_quotients": [0, 0],
              "required_coordinates": [0],
              "support_cursor": {"fibre_ordinal": 0, "coordinate": 0,
                                 "target_hex": "00", "kernel_ordinal": 0,
                                 "q0_state_id": 1, "gamma_state_id": 1},
              "checked_fibres": 1, "predicted_pivot": "ab",
              "selector_counters": {"seeds_touched": 1, "formulas_compiled": 1,
                                    "support_fibres": 1, "kernel_candidates": 1,
                                    "identity_replays": 0, "adds": 1, "updates": 1}}
    validate_new_source(sample)
    for label, mutate in (("K!=0", {"K": 1}),
                          ("second_insert", {"selector_counters":
                           dict(sample["selector_counters"], adds=2)}),
                          ("direct_scalar", {"direct_scalar": 2}),
                          ("epsilon", {"normalized_exponent_quotients": [1, 0]})):
        changed = dict(sample); changed.update(mutate)
        try:
            validate_new_source(changed)
        except RuntimeError:
            rejected.append(label)
    need(len(rejected) == 4, "checker mutation fixture")
    return {"status": "PASS", "actual_imported_checker": OLD_CHECKER[2],
            "v7_self_test": base_result, "mutation_rejections": rejected,
            "producer_selector_imported": False,
            "coordinated_row_scalar_checked_by": "independent replay_correction"}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("artifact", nargs="?")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args(argv)
    if args.self_test:
        print(MARKER + "_SELFTEST_PASS " + json.dumps(self_test(), sort_keys=True))
        return 0
    need(args.artifact, "artifact required")
    check(json.loads(Path(args.artifact).read_text(encoding="ascii")))
    print(MARKER + "_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
