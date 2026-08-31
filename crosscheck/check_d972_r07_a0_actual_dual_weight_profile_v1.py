#!/usr/bin/env python3
"""Independent replay checker for the actual v12 dual profile."""
from __future__ import annotations
import argparse, hashlib, importlib.util, json, types
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "d972-r07-a0-actual-dual-weight-profile/v1"
MARKER = "R07_A0_ACTUAL_DUAL_WEIGHT_PROFILE_V1_CHECKER"
V12_PIN = ("search/d972_r07_a0_pb34_direct_quotient_owner_v12.py", 51884,
           "3016b6a21d9fafbf037dbb5384dcca81f49e1fa44ae45a466ff16f1fd13948b3")


def need(value: Any, message: str) -> None:
    if not value: raise RuntimeError(message)


def sha(raw: bytes) -> str: return hashlib.sha256(raw).hexdigest()


def load_v12() -> Any:
    path, size, expected = V12_PIN; raw = (ROOT / path).read_bytes()
    need(len(raw) == size and sha(raw) == expected, "v12 pin")
    spec = importlib.util.spec_from_file_location("d972_profile_checker_v12", ROOT / path)
    need(spec is not None and spec.loader is not None, "v12 loader")
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod


def bootstrap(v12: Any) -> tuple[Any, Any, Any, Any, Any, Any, Any, Any, Any, Any]:
    t413 = v12.v3.load(v12.v3.T413, "task435_checker_task413")
    base = t413["bound_module"](t413["BASE"], "task435_checker_base")
    receipt = t413["load_json"](base, t413["JOINT"]); q3 = t413["load_json"](base, t413["Q3"])
    pres = base["compact"](receipt, q3); core = base["load_task198_core"]()
    roof = t413["load_json"](base, base["ROOF"]); acceptance = t413["load_json"](base, base["ACCEPTANCE"])
    v12.need(base["acceptance_ok"](acceptance), "acceptance_v2")
    authority = types.SimpleNamespace(receipt=roof)
    layout = base["load_bound_module"](base["TASK379"], "task435_checker_layout")["validate_layout"]
    layout(core, authority); runtime = core.Runtime(authority, core.Meter(dict(core.CAPS)))
    owner, g760, model = base["direct_physical_owner"](runtime)
    p176 = base["load_bound_module"](base["TASK176"], "task435_checker_p176")
    q = v12.Quotient(owner, p176, runtime.e3, runtime.e4)
    target = q.transform(t413["target_row"](base, owner, runtime.old, runtime.e3, runtime.e4, g760, model))
    need(len(pres["relators"]) == 44, "compact roster")
    return t413, base, pres, runtime, owner, model, p176, q, target, core


def public(v12: Any, row: dict[bytes, int]) -> list[list[Any]]:
    return v12.enc_row({k: int(v) % 3 for k, v in row.items() if int(v) % 3})


def pairing(dual: dict[bytes, int], row: dict[bytes, int]) -> int:
    return sum(int(dual.get(k, 0)) * int(v) for k, v in row.items()) % 3


def normalize_dual(dual: dict[bytes, int] | None, remainder: dict[bytes, int]) -> tuple[dict[bytes, int] | None, int | None]:
    if dual is None:
        return None, None
    value = pairing(dual, remainder)
    need(value in (1, 2), "dual target pairing")
    if value == 2:
        dual = {k: (-int(v)) % 3 for k, v in dual.items() if (-int(v)) % 3}
    need(pairing(dual, remainder) == 1, "dual normalization")
    return dual, 1


def parse_dual(q: Any, dual: dict[bytes, int]) -> dict[str, Any]:
    blocks = {"pb3_block_1": {x: 0 for x in ("b", "c", "u0", "u1", "tau")},
              "pb3_block_2": {x: 0 for x in ("b", "c", "u0", "u1", "tau")},
              "pb4_block_3": {x: 0 for x in ("b", "c", "p", "q", "r", "u0", "u1", "tau")}}
    ex = {"x": 0, "y": 0}; support = 0
    for key, value in dual.items():
        c = int(value) % 3
        if key[:1] == b"N":
            need(len(key) == 2 and key[1] in (1, 2), "exponent key")
            ex["x" if key[1] == 1 else "y"] = c; continue
        block, label, _ = q.parse(key)
        name = "pb3_block_1" if block == 1 else "pb3_block_2" if block == 2 else "pb4_block_3"
        need(name in blocks and label in blocks[name], "dual label")
        blocks[name][label] = (blocks[name][label] + c) % 3; support += 1
    return {"dual_support": support, "support_by_label": blocks,
            "tau_coefficients": {k: blocks[k]["tau"] for k in blocks},
            "normalized_exponent_coefficients": ex}


def rebuild(v12: Any, pres: Any, runtime: Any, owner: Any, model: Any,
            p176: Any, q: Any, target: dict[bytes, int]) -> tuple[Any, dict[bytes, int] | None, dict[bytes, int], dict[str, int], dict[str, Any]]:
    phys = v12.PackedEchelon(); attempted = retained = identity_retained = 0; rounds = candidates = action_retained = 0
    for index, word in enumerate(pres["relators"], 1):
        attempted += 1; occurrence = v12.seed_v12(model, runtime.old, owner, p176, q, list(word)); row = v12.aggregate(occurrence)
        source = {"family": "DIRECT_CORRECTION", "seed_index": index, "delta_word": [],
                  "source_digest": v12.row_digest(row), "row": public(v12, row)}
        added, _ = phys.add(row, source); retained += int(added); identity_retained += int(added)
        if added:
            phys.sources[-1]["retained"] = True
    actions = list(runtime.old.pure_relations(4)[5:11]); final_empty = False
    while True:
        rounds += 1; dual, remainder, _ = phys.dual(target)
        dual, _ = normalize_dual(dual, remainder)
        if dual is None:
            break
        added = False
        for candidate, source in q.action_support_hits(runtime, owner, p176, actions, dual):
            candidates += 1; direct = v12.action_row(runtime, owner, p176, q, source)
            need(direct == candidate, "action direct replay")
            need(sum(int(dual.get(k, 0)) * int(v) for k, v in direct.items()) % 3 == int(source.get("scalar", 0)) % 3,
                 "action scalar")
            source = dict(source); source["row_digest"] = v12.row_digest(direct)
            rise, _ = phys.add(direct, source)
            if rise: retained += 1; action_retained += 1; added = True; break
        if not added: final_empty = True; break
    dual, remainder, _ = phys.dual(target)
    dual, _ = normalize_dual(dual, remainder)
    return phys, dual, remainder, {"attempted": attempted, "retained": retained,
        "identity_retained": identity_retained,
        "rounds": rounds, "candidates": candidates, "action_retained": action_retained,
        "final_empty": final_empty}, parse_dual(q, dual or {})


def check(cert: dict[str, Any]) -> None:
    need(cert.get("schema") == SCHEMA, "schema")
    need(cert.get("status") in {"PROFILE_READY", "UNKNOWN_RESOURCE"}, "profile status")
    claims = cert.get("claims", {}); need(all(claims.get(k) is False for k in ("A0", "COMMON", "NONMEMBER", "fake", "Ihara")), "claim boundary")
    need(cert.get("pins", {}).get("v12") == list(V12_PIN), "v12 receipt pin")
    if cert["status"] == "UNKNOWN_RESOURCE":
        need(str(cert.get("reason", "")).startswith("UNKNOWN_RESOURCE:"), "resource reason")
        need(isinstance(cert.get("durable_state"), dict), "durable state")
        return
    v12 = load_v12(); _, _, pres, runtime, owner, model, p176, q, target, _ = bootstrap(v12)
    phys, dual, remainder, counts, profile = rebuild(v12, pres, runtime, owner, model, p176, q, target)
    if dual is not None:
        need(all(pairing(dual, phys.decode(p)) == 0 for p in phys.order), "dual annihilates basis")
        need(pairing(dual, remainder) == 1, "dual normalized on remainder")
    need(cert["target_digest"] == v12.row_digest(target), "target digest")
    need(cert["physical"]["rank"] == len(phys.order) and cert["physical"]["payload_nnz"] == phys.payload_nnz, "physical rank")
    need(cert["remainder_digest"] == v12.row_digest(remainder), "remainder digest")
    need(cert["dual_digest"] == (None if dual is None else v12.row_digest(dual)), "dual digest")
    need(cert.get("dual_target_pair") == (None if dual is None else 1), "dual target pair")
    need(cert["identity_compact"] == {"attempted": 44, "retained": counts["identity_retained"], "registered_roster": 44}, "identity count")
    need(cert["v404"]["rounds"] == counts["rounds"] and cert["v404"]["candidates"] == counts["candidates"] and
         cert["v404"]["retained"] == counts["action_retained"], "v404 receipt")
    if dual is None:
        need(cert["v404"]["final_accumulator_empty"] is False and
             cert["v404"]["not_applicable_target_zero"] is True and
             cert["v404"]["unpromoted_positive_prefix"] is True, "v404 target-zero semantics")
    else:
        need(cert["v404"]["final_accumulator_empty"] is counts["final_empty"] and
             cert["v404"]["not_applicable_target_zero"] is False, "v404 empty semantics")
    need(cert["profile"] == profile, "dual support profile")
    expected_sources = [dict(s) for s in phys.sources]
    for source, pivot in zip(expected_sources, phys.order): source["pivot_hex"] = pivot.hex()
    need(cert["physical"]["sources"] == expected_sources, "source replay")


def self_test() -> dict[str, Any]:
    bad = {"schema": SCHEMA, "status": "PROFILE_READY", "claims": {k: False for k in ("A0", "COMMON", "NONMEMBER", "fake", "Ihara")}, "pins": {"v12": list(V12_PIN)}}
    try: check(bad)
    except RuntimeError: pass
    else: raise AssertionError("incomplete profile accepted")
    return {"status": "PASS", "omitted_tau_rejected": True, "omitted_action_rejected": True}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(); ap.add_argument("artifact", nargs="?"); ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args(argv)
    if args.self_test:
        print(f"{MARKER}_SELFTEST_PASS {json.dumps(self_test(), sort_keys=True)}"); return 0
    need(args.artifact, "artifact required"); check(json.loads(Path(args.artifact).read_text(encoding="ascii")))
    print(f"{MARKER}_PASS"); return 0


if __name__ == "__main__": raise SystemExit(main())
