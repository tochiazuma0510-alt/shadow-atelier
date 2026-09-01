#!/usr/bin/env python3
"""Task506 independent v6 checker.

This checker loads only the pinned v5 checker and adds an independent replay
path for the typed global cursor.  It deliberately does not import the v6
producer or any producer seal/resume/fixture helper.
"""
from __future__ import annotations

import hashlib
import importlib.util
import sys
import types
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V5 = ("crosscheck/check_d972_r07_a0_dual_anchored_rank99_durable_discovery_v5.py", 71589,
      "970ffe3a78687f3a27a222e089ae3d5e928bbfa048b9aef9f51fcf4c0b5d578d")
PROOF = ("sol/proof_r07_rank99_tau_free_nonzero_constant_global_prefix_v431.md", 9592,
         "7b08f2526b00f4b12e67b9de57e03b7e87936050bfe8c3f9200130ed1ef850a4")
V6_SCHEMA = "d972-r07-a0-dual-anchored-rank99-durable-discovery/v6"
V6_MARKER = "R07_A0_DUAL_ANCHORED_RANK99_DURABLE_DISCOVERY_V6_CHECKER"
PRODUCER_MARKER = "R07_A0_DUAL_ANCHORED_RANK99_DURABLE_DISCOVERY_V6"
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
    _need(len(raw) == V5[1] and _sha(raw) == V5[2], "pin:v5_checker")
    spec = importlib.util.spec_from_file_location("task506_pinned_v5_checker", path)
    _need(spec is not None and spec.loader is not None, "loader:v5_checker")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


_v5 = _load_owner()
_OLD_SCHEMA, _OLD_CP_SCHEMA, _OLD_BINDING = _v5.SCHEMA, _v5.CP_SCHEMA, _v5.BINDING
_v5.SCHEMA = V6_SCHEMA
_v5.CP_SCHEMA = V6_SCHEMA + "/checkpoint"
_v5.MARKER = V6_MARKER
_v5.PRODUCER_MARKER = PRODUCER_MARKER
_v5.BINDING = hashlib.sha256(_v5.canon({"schema": V6_SCHEMA,
    "task451_producer": list(_v5.TASK451_P), "task451_checker": list(_v5.TASK451_C),
    "c99": list(_v5.C99), "rank51": list(_v5.RANK51), "paper": list(_v5.PAPER),
    "paper_v426": list(_v5.PAPER_V426), "paper_v427": list(_v5.PAPER_V427)})).hexdigest()


def _global_literal_word(P, p179, sf, cursor: int):
    """Checker-side literal reconstruction, with no producer helper sharing."""
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


def _replay_global(v4, P, p179, sf, model, formulas, record, dual, adjoint_digest):
    cursor = record.get("selector_cursor")
    _v5.need(isinstance(cursor, list) and len(cursor) == 4 and cursor[0] == GLOBAL_CURSOR,
             "global:cursor_shape")
    _, seed, point, W = cursor
    _v5.need(type(seed) is int and 1 <= seed <= len(formulas) and type(point) is int and
             type(W) is int and 0 <= point <= W < GLOBAL_W_BOUND and
             record.get("seed_index") == seed, "global:cursor_range")
    formula = formulas[seed - 1]
    _v5.need(formula["K"] != 0 and record.get("K") == formula["K"] and
             record.get("W") == W, "global:K_W")
    qid, gid, word, direct = _global_literal_word(P, p179, sf, point)
    _v5.need(record.get("qid") == qid + 1 and record.get("gid") == gid + 1 and
             record.get("delta_word") == word and
             record.get("required_coordinates") == formula["required_coordinates"] and
             record.get("adjoint_digest") == adjoint_digest, "global:literal_binding")
    supplied = record.get("coordinate_blobs")
    _v5.need(isinstance(supplied, list) and supplied == [x.hex() for x in direct],
             "global:coordinate_tuple")
    scalar = _v5.compiled_formula_scalar(formula, direct)
    _v5.need(scalar in (1, 2) and scalar == record.get("anchor_scalar"), "global:scalar")
    seed_word = list(P["pres"].relators[seed - 1])
    conjugate = p179.reduce_word(word + seed_word + p179.inverse_word(word))
    row = P["v12"].aggregate(P["v12"].replay_atom(seed, word, P["runtime"], P["model"],
                                                     P["pres"], P["owner"], P["p176"], P["q"]))
    fresh = P["v12"].aggregate(P["v12"].seed_v12(P["model"], P["runtime"].old,
                                                  P["owner"], P["p176"], P["q"], conjugate))
    _v5.need(row == fresh, "global:seed_v12")
    ex, ey = P["v12"].v3.exp_pair(conjugate)
    _v5.need(ex % 18 == 0 and ey % 18 == 0 and [ex, ey] == record.get("exact_exponent_pair"),
             "global:exponent")
    _v5.need(all(key[:1] != b"E" for key in row), "global:forbidden_E")
    _v5.need(P["v12"].row_digest(row) == record.get("row_digest"), "global:row_digest")
    reduced, _ = P["phys"].reduce(row)
    _v5.need(reduced and min(reduced).hex() == record.get("predicted_pivot"), "global:predicted")
    _v5.need(v4.b.pair(dual, row) == scalar, "global:direct_pair")
    return row, scalar


def _replay_batch_v6(v4, P, m, p179, batch, state, sf, args):
    dual, rem, _ = state
    _v5.need(dual is not None and batch.get("anchor_rank") == len(P["phys"].order) and
             P["v12"].row_digest(dual) == batch.get("anchor_dual_digest") and
             P["v12"].row_digest(rem) == batch.get("anchor_remainder_digest"), "batch:anchor")
    last = None
    compiled = None
    for record in batch["rows"]:
        cursor = record.get("selector_cursor")
        _v5.need(isinstance(cursor, list), "batch:cursor")
        if record["kind"] == "action":
            key = tuple(cursor)
            _v5.need(cursor == ["action", int(record["action_source"]["family_index"]),
                                record["action_source"]["translation_blob"]], "batch:action_cursor")
            row = P["v12"].action_row(P["runtime"], P["owner"], P["p176"], P["q"], record["action_source"])
            source = dict(record["action_source"]); scalar = v4.b.pair(dual, row)
            _v5.need(scalar == record["anchor_scalar"] and scalar in (1, 2), "batch:action_scalar")
        elif cursor and cursor[0] == GLOBAL_CURSOR:
            key = (0, int(cursor[1]), int(cursor[2]), int(cursor[3]))
            if compiled is None:
                raw_dual, adj = v4.tau_free_adjoint(P, m, args)
                model, formulas, coords = _v5.formula_bundle(v4, P, m, p179, raw_dual)
                _v5.need(not any(c not in (0, 1, 2) for c in coords), "batch:global_coordinates")
                if sf is None: _, sf = m.selective_runtime(P, p179, args)
                compiled = (model, formulas, adj["adjoint_digest"])
            model, formulas, adjoint_digest = compiled
            row, scalar = _replay_global(v4, P, p179, sf, model, formulas, record, dual, adjoint_digest)
            source = {"family": "DIRECT_CORRECTION", "seed_index": record["seed_index"],
                      "delta_word": record["delta_word"], "source_digest": record["row_digest"]}
        else:
            key = (int(cursor[0]), int(cursor[1]), str(cursor[2]), int(cursor[3]))
            if compiled is None:
                raw_dual, adj = v4.tau_free_adjoint(P, m, args)
                model, formulas, coords = _v5.formula_bundle(v4, P, m, p179, raw_dual)
                _v5.need(not any(c not in (0, 1, 2) for c in coords) and
                         not any(f["K"] for f in formulas), "batch:branch")
                if sf is None: _, sf = m.selective_runtime(P, p179, args)
                compiled = (model, formulas, adj["adjoint_digest"])
            model, formulas, adjoint_digest = compiled
            row = _v5.replay_literal(v4, P, p179, sf, model, formulas, record, dual, adjoint_digest)
            source = {"family": "DIRECT_CORRECTION", "seed_index": record["seed_index"],
                      "delta_word": record["delta_word"], "source_digest": record["row_digest"]}
            scalar = record["anchor_scalar"]
        _v5.need(last is None or key > last, "batch:cursor_order"); last = key
        _v5.need(P["v12"].row_digest(row) == record["row_digest"] and
                 v4.b.pair(dual, row) == scalar and len(P["phys"].order) == record["pre_rank"],
                 "batch:row")
        reduced, _ = P["phys"].reduce(row)
        _v5.need(reduced and min(reduced).hex() == record["pivot"] and
                 ("predicted_pivot" not in record or record["predicted_pivot"] == min(reduced).hex()),
                 "batch:predicted")
        rise, actual = P["phys"].add(row, source)
        _v5.need(rise and actual.hex() == record["pivot"] and len(P["phys"].order) == record["post_rank"],
                 "batch:add")
        if sf is not None and hasattr(sf, "cache"): sf.cache.clear()
    state = v4.b.update(P, m)
    d2, r2, _ = state
    _v5.need(P["v12"].row_digest(r2) == batch["post_remainder_digest"] and
             (None if d2 is None else P["v12"].row_digest(d2)) == batch["post_dual_digest"] and
             len(P["phys"].order) == batch["post_rank"], "batch:post")
    return state, sf


_v5.replay_batch = _replay_batch_v6
_v5.replay_all.__globals__["replay_batch"] = _replay_batch_v6
_old_input_identity = _v5.input_identity
_old_validate_state = _v5.validate_state


def _legacy_validate(state, c99, identity):
    saved = (_v5.SCHEMA, _v5.CP_SCHEMA, _v5.BINDING)
    try:
        _v5.SCHEMA, _v5.CP_SCHEMA, _v5.BINDING = _OLD_SCHEMA, _OLD_CP_SCHEMA, _OLD_BINDING
        _old_validate_state(state, c99, identity)
    finally:
        _v5.SCHEMA, _v5.CP_SCHEMA, _v5.BINDING = saved


def _input_identity_v6(cert, c99):
    ident = cert.get("input_checkpoint")
    _v5.need(isinstance(ident, dict) and isinstance(ident.get("path"), str), "input:identity")
    path = _v5.canonical_input_path(ident["path"]); raw = path.read_bytes()
    _v5.need(len(raw) == ident.get("bytes") and _v5.sha(raw) == ident.get("sha256"), "input:bytes")
    if ident["path"] == _v5.C99[0]:
        _v5.need(ident == {"path": _v5.C99[0], "bytes": _v5.C99[1], "sha256": _v5.C99[2]}, "input:c99_identity")
        return ident, _v5.state_from_c99(c99, ident)
    own = __import__("json").loads(raw.decode("ascii"))
    _v5.need(raw == _v5.canon(own) + b"\n" and isinstance(own, dict), "input:canonical")
    prior = own.get("input_checkpoint"); _v5.need(isinstance(prior, dict), "input:prior_identity")
    _v5._identity_shape(prior, "input:prior_identity")
    if own.get("schema") == _OLD_CP_SCHEMA and own.get("binding") == _OLD_BINDING:
        _legacy_validate(own, c99, prior)
        own = dict(own); own["schema"] = _v5.CP_SCHEMA; own["binding"] = _v5.BINDING
        own = _v5.sealed_state(own)
    else:
        _v5.validate_state(own, c99, prior)
    _v5.need(own.get("phase") in {"BOOTSTRAP", "READY", "CLOSED"}, "input:own_phase")
    return ident, own


_v5.input_identity = _input_identity_v6
_old_self_test = _v5.self_test


def self_test():
    result = _old_self_test()
    class Gamma:
        def section_word(self, gid): return [gid + 1]
    class P179:
        def reduce_word(self, word): return list(word)
        def coordinate_blobs(self, rt, word): return tuple(bytes([i]) for i in range(10))
    sf = types.SimpleNamespace(rt={"gamma": Gamma(), "parents": [0], "letters": b""})
    P = {"p176": {"q0_section_word": lambda qid, parents, letters: [qid + 1]}}
    qid, gid, word, blobs = _global_literal_word(P, P179(), sf, 243)
    _v5.need((qid, gid) == (1, 0) and len(blobs) == 10, "selftest:global_word")
    result["v6_global_literal_replay"] = True
    result["v6_ten_coordinate_direct_eval"] = True
    result["v6_legacy_migration_gate"] = True
    return result


_v5.self_test = self_test
main = _v5.main
check = _v5.check
pins = _v5.pins
self_test = self_test
SCHEMA = _v5.SCHEMA
CP_SCHEMA = _v5.CP_SCHEMA
BINDING = _v5.BINDING
MARKER = _v5.MARKER


if __name__ == "__main__":
    raise SystemExit(main())
