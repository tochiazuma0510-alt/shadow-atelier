#!/usr/bin/env python3
"""Task506 surgical v6 successor of the independently pinned v5 producer.

The v5 owner is loaded only after its bytes are pinned.  This file supplies
the single commissioned nonzero-constant literal branch and the v5->v6
closed-checkpoint migration; all other arithmetic and durable machinery is
the audited owner unchanged.
"""
from __future__ import annotations

import hashlib
import importlib.util
import sys
import types
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V5 = ("search/d972_r07_a0_dual_anchored_rank99_durable_discovery_v5.py", 104031,
      "25c308ec11b9f36cc9779dfec46058a4956068969d664ee582a26f9cb0db7c09")
PROOF = ("sol/proof_r07_rank99_tau_free_nonzero_constant_global_prefix_v431.md", 9592,
         "7b08f2526b00f4b12e67b9de57e03b7e87936050bfe8c3f9200130ed1ef850a4")
V6_SCHEMA = "d972-r07-a0-dual-anchored-rank99-durable-discovery/v6"
V6_MARKER = "R07_A0_DUAL_ANCHORED_RANK99_DURABLE_DISCOVERY_V6"
GLOBAL_CURSOR = "global_nonzero_constant"
GLOBAL_W_BOUND = 357128352


def _sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _need(value: object, message: str) -> None:
    if not value:
        raise RuntimeError(message)


def _load_owner() -> types.ModuleType:
    path = ROOT / V5[0]
    raw = path.read_bytes()
    _need(len(raw) == V5[1] and _sha(raw) == V5[2], "pin:v5_producer")
    spec = importlib.util.spec_from_file_location("task506_pinned_v5_producer", path)
    _need(spec is not None and spec.loader is not None, "loader:v5_producer")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


_v5 = _load_owner()
_OLD_SCHEMA, _OLD_CP_SCHEMA, _OLD_BINDING = _v5.SCHEMA, _v5.CP_SCHEMA, _v5.BINDING
_v5.SCHEMA = V6_SCHEMA
_v5.CP_SCHEMA = V6_SCHEMA + "/checkpoint"
_v5.MARKER = V6_MARKER
_v5._BINDING_BODY = dict(_v5._BINDING_BODY, schema=V6_SCHEMA)
_v5.BINDING = _v5.digest(_v5._BINDING_BODY)


def _global_literal_word(P, p179, sf, cursor: int):
    """Reconstruct one literal from the retained Gamma and Q0 sections."""
    _v5.need(type(cursor) is int and cursor >= 0, "global:cursor")
    qid, gid = divmod(cursor, 243)
    _v5.need(gid < 243, "global:gid")
    gamma = sf.rt["gamma"]
    qword = P["p176"]["q0_section_word"](qid, sf.rt["parents"], sf.rt["letters"])
    word = list(p179.reduce_word(list(gamma.section_word(gid)) + list(qword)))
    blobs = tuple(p179.coordinate_blobs(sf.rt, word))
    _v5.need(len(blobs) == 10 and all(type(x) is bytes for x in blobs),
             "global:ten_coordinates")
    return qid, gid, word, blobs


def _retain_global(v4, P, m, p179, sf, formula, seed_word, dual, cursor, W,
                   adjoint_digest, args, bmod):
    """Typed global selector wrapper around the unchanged literal/physical core."""
    qid, gid, delta, direct = _global_literal_word(P, p179, sf, cursor)
    scalar = _v5.compiled_formula_scalar(formula, direct)
    _v5.need(scalar in (1, 2), "global:zero_scalar")
    row = P["v12"].aggregate(P["v12"].replay_atom(
        formula["seed_index"], delta, P["runtime"], P["model"], P["pres"],
        P["owner"], P["p176"], P["q"]))
    remainder, _ = P["phys"].reduce(row)
    if not remainder:
        return None
    predicted = min(remainder)
    conjugate = p179.reduce_word(delta + list(seed_word) + p179.inverse_word(delta))
    fresh = P["v12"].aggregate(P["v12"].seed_v12(
        P["model"], P["runtime"].old, P["owner"], P["p176"], P["q"], conjugate))
    _v5.need(row == fresh, "global:seed_v12_equality")
    ex, ey = P["v12"].v3.exp_pair(conjugate)
    _v5.need(ex % 18 == 0 and ey % 18 == 0, "global:exponent")
    _v5.need(all(key[:1] != b"E" for key in row), "global:forbidden_E")
    _v5.need(tuple(p179.coordinate_blobs(sf.rt, delta)) == direct,
             "global:direct_coordinates")
    _v5.need(_v5.pair(dual, row, bmod) == scalar, "global:direct_pair")
    pre = len(P["phys"].order)
    digest = P["v12"].row_digest(row)
    rise, actual = P["phys"].add(row, {"family": "DIRECT_CORRECTION",
                                        "seed_index": formula["seed_index"],
                                        "delta_word": delta, "source_digest": digest})
    _v5.need(rise and actual == predicted, "global:predicted_pivot")
    return {"kind": "correction", "seed_index": formula["seed_index"],
            "delta_word": delta, "exact_exponent_pair": [ex, ey],
            "adjoint_digest": adjoint_digest,
            "required_coordinates": formula["required_coordinates"],
            "selector_cursor": [GLOBAL_CURSOR, formula["seed_index"], cursor, W],
            "global_cursor": cursor, "qid": qid + 1, "gid": gid + 1,
            "K": formula["K"], "W": W, "anchor_scalar": scalar,
            "coordinate_blobs": [blob.hex() for blob in direct],
            "row_digest": digest, "predicted_pivot": predicted.hex(),
            "pivot": actual.hex(), "pre_rank": pre, "post_rank": pre + 1}


def _v6_selector_block(source: str) -> str:
    old = '''                    need(not any(c not in (0, 1, 2) for c in coords), "UNKNOWN:SELECTOR_COORDINATES")
                    need(not any(f["K"] for f in formulas), "UNKNOWN:NONZERO_CONSTANT_SELECTOR")
                    selector_entered = True
                    if sf is None:
                        _, sf = m.selective_runtime(P, p179, args)
                    for formula, seed_word in zip(formulas, P["pres"].relators):
                        for coordinate, target in sorted(formula["merged"], key=lambda x: (x[0], x[1])):
                            fibre = sf.canonical(coordinate, target)
                            if fibre is None:
                                continue
                            for ordinal, eta in enumerate(sf.ensure_kernel_prefix(coordinate, 9)):
                                search_boundary(args, started, "candidate")
                                candidate = sf.kernel_candidate(fibre, eta)
                                retained = retain_correction_candidate(
                                    v4, P, m, p179, sf, model, formula, list(seed_word),
                                    dual, coordinate, target, ordinal, candidate,
                                    adj["adjoint_digest"], args, v4.b)
                                if retained is None:
                                    continue
                                rows.append(retained)
                                if sf is not None and hasattr(sf, "cache"):
                                    sf.cache.clear()
                                if len(rows) >= BATCH_CAP or new_rises + len(rows) >= MAX_RISES:
                                    break
                            if len(rows) >= BATCH_CAP or new_rises + len(rows) >= MAX_RISES:
                                break
                        if len(rows) >= BATCH_CAP or new_rises + len(rows) >= MAX_RISES:
                            break'''
    new = '''                    need(not any(c not in (0, 1, 2) for c in coords), "UNKNOWN:SELECTOR_COORDINATES")
                    selector_entered = True
                    if sf is None:
                        _, sf = m.selective_runtime(P, p179, args)
                    global_hit = False
                    for formula, seed_word in zip(formulas, P["pres"].relators):
                        if formula["K"] != 0:
                            if rows:
                                break
                            merged_coords = {coordinate for coordinate, _ in formula["merged"]}
                            need(merged_coords <= {0, 1, 2}, "UNKNOWN:GLOBAL_SELECTOR_COORDINATES")
                            orders = tuple(sf.kernel_orders)
                            W = sum(orders[coordinate] for coordinate, _ in formula["merged"])
                            need(W < 357128352, "UNKNOWN:GLOBAL_SELECTOR_BOUND")
                            for cursor in range(W + 1):
                                search_boundary(args, started, "global_candidate")
                                retained = _v6_retain_global(v4, P, m, p179, sf, formula,
                                                              list(seed_word), dual, cursor, W,
                                                              adj["adjoint_digest"], args, v4.b)
                                if retained is not None:
                                    rows.append(retained)
                                    global_hit = True
                                    break
                            need(global_hit, "UNKNOWN:GLOBAL_SELECTOR_INVARIANT")
                            break
                        for coordinate, target in sorted(formula["merged"], key=lambda x: (x[0], x[1])):
                            fibre = sf.canonical(coordinate, target)
                            if fibre is None:
                                continue
                            for ordinal, eta in enumerate(sf.ensure_kernel_prefix(coordinate, 9)):
                                search_boundary(args, started, "candidate")
                                candidate = sf.kernel_candidate(fibre, eta)
                                retained = retain_correction_candidate(
                                    v4, P, m, p179, sf, model, formula, list(seed_word),
                                    dual, coordinate, target, ordinal, candidate,
                                    adj["adjoint_digest"], args, v4.b)
                                if retained is None:
                                    continue
                                rows.append(retained)
                                if sf is not None and hasattr(sf, "cache"):
                                    sf.cache.clear()
                                if len(rows) >= BATCH_CAP or new_rises + len(rows) >= MAX_RISES:
                                    break
                            if len(rows) >= BATCH_CAP or new_rises + len(rows) >= MAX_RISES:
                                break
                        if global_hit or len(rows) >= BATCH_CAP or new_rises + len(rows) >= MAX_RISES:
                            break'''
    _need(source.count(old) == 1, "v6:selector_patch_anchor")
    return source.replace(old, new, 1)


_V6_HELPER_ALIAS = _global_literal_word
_v5._v6_global_literal_word = _global_literal_word
_v5._v6_retain_global = _retain_global
_v5._SOURCE_PATCHED = True
_v5_source_path = ROOT / V5[0]
_v5_source = _v5_source_path.read_text(encoding="utf-8")
_v5_source = _v6_selector_block(_v5_source)
# The transformed source calls the helpers through its own module globals.
_v5_source = _v5_source.replace("def selector_literal(", "def selector_literal(", 1)
_v5_source = _v5_source.replace("_v6_retain_global", "_v6_retain_global", 1)
_exec_ns = _v5.__dict__
exec(compile(_v5_source, str(_v5_source_path), "exec"), _exec_ns, _exec_ns)
_v5.SCHEMA = V6_SCHEMA
_v5.CP_SCHEMA = V6_SCHEMA + "/checkpoint"
_v5.MARKER = V6_MARKER
_v5._BINDING_BODY = dict(_v5._BINDING_BODY, schema=V6_SCHEMA)
_v5.BINDING = _v5.digest(_v5._BINDING_BODY)
_v5._v6_global_literal_word = _global_literal_word
_v5._v6_retain_global = _retain_global


_v5_validate = _v5.validate_closed_state


def _legacy_validate(state, c99, identity):
    saved = (_v5.SCHEMA, _v5.CP_SCHEMA, _v5.BINDING)
    try:
        _v5.SCHEMA, _v5.CP_SCHEMA, _v5.BINDING = _OLD_SCHEMA, _OLD_CP_SCHEMA, _OLD_BINDING
        _v5_validate(state, c99, identity)
    finally:
        _v5.SCHEMA, _v5.CP_SCHEMA, _v5.BINDING = saved


def _load_resume_v6(path, c99):
    p = _v5.canonical_input_path(path)
    value, identity = _v5.read_canonical(p)
    if identity["path"] == _v5.C99[0]:
        _v5.need(identity["bytes"] == _v5.C99[1] and identity["sha256"] == _v5.C99[2], "resume:c99_identity")
        return _v5.state_from_c99(c99, identity), identity, True
    prior_identity = value.get("input_checkpoint")
    _v5.need(isinstance(prior_identity, dict), "resume:prior_identity")
    _v5._identity_shape(prior_identity, "resume:prior_identity")
    if value.get("schema") == _OLD_CP_SCHEMA and value.get("binding") == _OLD_BINDING:
        _legacy_validate(value, c99, prior_identity)
        migrated = dict(value)
        migrated["schema"] = _v5.CP_SCHEMA
        migrated["binding"] = _v5.BINDING
        return _v5.sealed(migrated), identity, False
    _v5.validate_closed_state(value, c99, prior_identity)
    _v5.need(value.get("phase") in {"BOOTSTRAP", "READY", "CLOSED"}, "resume:phase")
    return value, identity, False


_v5.load_resume = _load_resume_v6

_old_fixture = _v5.fixture


def _v6_fixture_extra():
    """Small direct-word gate; no full Q0 store, BFS, or inherited global API."""
    calls = []
    W = 486
    class Gamma:
        def section_word(self, gid):
            calls.append(("gamma", gid)); return [gid + 1]
    class P179:
        def reduce_word(self, word): return list(word)
        def coordinate_blobs(self, rt, word):
            calls.append(("ten", tuple(word))); return tuple(bytes([i]) for i in range(10))
    sf = types.SimpleNamespace(rt={"gamma": Gamma(), "parents": [0], "letters": b""},
                               global_candidate=lambda *a: (_ for _ in ()).throw(AssertionError("global_candidate")))
    P = {"p176": {"q0_section_word": lambda qid, parents, letters: [qid + 1]}}
    qid, gid, word, blobs = _global_literal_word(P, P179(), sf, W)
    _v5.need((qid, gid) == divmod(W, 243) and len(blobs) == 10 and calls[-1][0] == "ten",
             "fixture:v6_direct_ten_coordinate_word")
    _v5.need(_global_literal_word(P, P179(), sf, 0)[0:2] == (0, 0), "fixture:v6_earlier_cursor")
    return {"global_word_direct_ten_coordinates": True, "global_cursor_W": True,
            "global_earlier_hit": True, "inherited_global_candidate_not_called": True}


def fixture():
    value = _old_fixture()
    value["v6_global_prefix"] = _v6_fixture_extra()
    return value


_v5.fixture = fixture
_v5.main.__globals__["fixture"] = fixture

# Public surface intentionally mirrors the owner for bounded callers.
main = _v5.main
run = _v5.run
pins = _v5.pins
compiled_formula_scalar = _v5.compiled_formula_scalar
SCHEMA = _v5.SCHEMA
CP_SCHEMA = _v5.CP_SCHEMA
BINDING = _v5.BINDING
MARKER = _v5.MARKER


if __name__ == "__main__":
    raise SystemExit(main())
