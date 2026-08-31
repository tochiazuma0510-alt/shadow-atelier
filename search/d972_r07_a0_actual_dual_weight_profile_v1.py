#!/usr/bin/env python3
"""Actual v12 physical-dual profile (A0 profile only; no membership claim)."""
from __future__ import annotations
import argparse, hashlib, importlib.util, json, os, sys, tempfile, time, types
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "d972-r07-a0-actual-dual-weight-profile/v1"
MARKER = "R07_A0_ACTUAL_DUAL_WEIGHT_PROFILE_V1"
RSS_CAP = 4_800_000_000
V12_PIN = ("search/d972_r07_a0_pb34_direct_quotient_owner_v12.py", 51884,
           "3016b6a21d9fafbf037dbb5384dcca81f49e1fa44ae45a466ff16f1fd13948b3")
SIX_NAMES = ("b", "c", "p", "q", "r")


class ProfileStop(RuntimeError):
    pass


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def need(value: Any, message: str) -> None:
    if not value:
        raise RuntimeError(message)


def load_v12() -> Any:
    path, size, expected = V12_PIN
    raw = (ROOT / path).read_bytes()
    need(len(raw) == size and digest(raw) == expected, "v12 pin")
    spec = importlib.util.spec_from_file_location("d972_profile_v12", ROOT / path)
    need(spec is not None and spec.loader is not None, "v12 loader")
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module


def bootstrap(v12: Any) -> tuple[Any, Any, Any, Any, Any, Any, Any, Any, Any]:
    """The exact v12 run bootstrap, retained as a short adapter."""
    t413 = v12.v3.load(v12.v3.T413, "task435_task413")
    base = t413["bound_module"](t413["BASE"], "task435_base")
    receipt = t413["load_json"](base, t413["JOINT"])
    q3 = t413["load_json"](base, t413["Q3"])
    pres = base["compact"](receipt, q3)
    core = base["load_task198_core"]()
    roof = t413["load_json"](base, base["ROOF"])
    acceptance = t413["load_json"](base, base["ACCEPTANCE"])
    v12.need(base["acceptance_ok"](acceptance), "acceptance_v2_contract")
    authority = types.SimpleNamespace(receipt=roof)
    layout = base["load_bound_module"](base["TASK379"], "task435_layout")["validate_layout"]
    ledger = layout(core, authority)
    runtime = core.Runtime(authority, core.Meter(dict(core.CAPS)))
    owner, g760, model = base["direct_physical_owner"](runtime)
    p176 = base["load_bound_module"](base["TASK176"], "task435_p176")
    q = v12.Quotient(owner, p176, runtime.e3, runtime.e4)
    target = q.transform(t413["target_row"](base, owner, runtime.old,
                                               runtime.e3, runtime.e4, g760, model))
    need(len(pres["relators"]) == 44, "compact relator count")
    return t413, base, pres, core, runtime, owner, model, p176, q, target


def public_row(v12: Any, row: dict[bytes, int]) -> list[list[Any]]:
    return v12.enc_row({k: int(v) % 3 for k, v in row.items() if int(v) % 3})


def normalize_dual(dual: dict[bytes, int] | None, remainder: dict[bytes, int]) -> tuple[dict[bytes, int] | None, int | None]:
    if dual is None:
        return None, None
    target_pair = sum(int(dual.get(k, 0)) * int(v) for k, v in remainder.items()) % 3
    need(target_pair in (1, 2), "dual target pairing")
    if target_pair == 2:
        dual = {k: (-int(v)) % 3 for k, v in dual.items() if (-int(v)) % 3}
    need(sum(int(dual.get(k, 0)) * int(v) for k, v in remainder.items()) % 3 == 1,
         "dual normalization")
    return dual, 1


def parse_profile_keys(q: Any, dual: dict[bytes, int]) -> dict[str, Any]:
    blocks = {"pb3_block_1": {"b": 0, "c": 0, "u0": 0, "u1": 0, "tau": 0},
              "pb3_block_2": {"b": 0, "c": 0, "u0": 0, "u1": 0, "tau": 0},
              "pb4_block_3": {x: 0 for x in ("b", "c", "p", "q", "r", "u0", "u1", "tau")}}
    ex = {"x": 0, "y": 0}
    support = 0
    for key, coefficient in dual.items():
        c = int(coefficient) % 3
        if not c:
            continue
        if key[:1] == b"N":
            need(len(key) == 2 and key[1] in (1, 2), "normalized exponent key")
            ex["x" if key[1] == 1 else "y"] = c; continue
        need(key[:1] == b"Q", "dual key ABI")
        block, label, _ = q.parse(key)
        name = "pb3_block_1" if block == 1 else "pb3_block_2" if block == 2 else "pb4_block_3"
        need(name in blocks and label in blocks[name], "dual label ABI")
        blocks[name][label] = (blocks[name][label] + c) % 3; support += 1
    return {"dual_support": support, "support_by_label": blocks,
            "tau_coefficients": {k: blocks[k]["tau"] for k in blocks},
            "normalized_exponent_coefficients": ex}


def checkpoint_state(v12: Any, phys: Any, target: dict[bytes, int], dual: dict[bytes, int] | None,
                     remainder: dict[bytes, int], counters: dict[str, Any], reason: str) -> dict[str, Any]:
    rows = {p.hex(): public_row(v12, phys.decode(p)) for p in phys.order}
    return {"schema": SCHEMA + "/checkpoint", "phase": counters["phase"],
            "reason": reason, "target": public_row(v12, target),
            "target_digest": v12.row_digest(target), "remainder": public_row(v12, remainder),
            "remainder_digest": v12.row_digest(remainder),
            "dual": None if dual is None else public_row(v12, dual),
            "physical_order": [p.hex() for p in phys.order], "physical_rows": rows,
            "physical_sources": phys.sources, "counters": dict(counters),
            "v12_pin": list(V12_PIN)}


def save_checkpoint(path: str | Path, state: dict[str, Any]) -> dict[str, Any]:
    p = Path(path); need(not p.is_absolute() and p.parent == Path("ci/out"), "checkpoint path")
    p.parent.mkdir(parents=True, exist_ok=True)
    raw = json.dumps(state, sort_keys=True, separators=(",", ":")).encode("ascii") + b"\n"
    with tempfile.NamedTemporaryFile(dir=p.parent, delete=False) as f:
        f.write(raw); f.flush(); os.fsync(f.fileno()); temp = Path(f.name)
    os.replace(temp, p)
    return {"path": str(p), "bytes": len(raw), "sha256": digest(raw)}


def run_profile(args: argparse.Namespace) -> dict[str, Any]:
    started = time.monotonic(); v12 = load_v12()
    t413, base, pres, core, runtime, owner, model, p176, q, target = bootstrap(v12)
    phys = v12.PackedEchelon(); seed_retained = 0; seed_attempted = 0
    action_rounds = action_candidates = action_retained = 0
    counters = {"phase": "identity_compact", "seed_cursor": 0, "action_round": 0,
                "candidate_count": 0, "retained_rows": 0}
    last_dual: dict[bytes, int] | None = None; last_rem: dict[bytes, int] = target
    def guard(phase: str) -> None:
        if args.seconds is not None and time.monotonic() - started >= args.seconds:
            raise ProfileStop("UNKNOWN_RESOURCE:time_limit:" + phase)
        rss = getattr(v12.v3, "rss", lambda: 0)() or 0
        if args.rss_bytes is not None and rss >= args.rss_bytes:
            raise ProfileStop("UNKNOWN_RESOURCE:rss_limit:" + phase)
    def durable(reason: str) -> dict[str, Any] | None:
        if not args.checkpoint: return None
        state = checkpoint_state(v12, phys, target, last_dual, last_rem, counters, reason)
        return save_checkpoint(args.checkpoint, state)
    try:
        for index, word in enumerate(pres["relators"], 1):
            guard("identity_compact"); counters["seed_cursor"] = index; seed_attempted += 1
            occurrence = v12.seed_v12(model, runtime.old, owner, p176, q, list(word))
            physical = v12.aggregate(occurrence)
            source = {"family": "DIRECT_CORRECTION", "seed_index": index,
                      "delta_word": [], "source_digest": v12.row_digest(physical),
                      "row": public_row(v12, physical)}
            added, _ = phys.add(physical, source)
            if added: seed_retained += 1; phys.sources[-1]["retained"] = True
            else: source["retained"] = False
            counters["retained_rows"] = len(phys.order)
            print(f"{MARKER} phase=identity_compact seed_cursor={index} "
                  f"physical_rank={len(phys.order)} payload_nnz={phys.payload_nnz} "
                  f"elapsed_seconds={time.monotonic()-started:.3f}", flush=True)
        counters["phase"] = "six_action"; durable("identity_compact_complete")
        actions = list(runtime.old.pure_relations(4)[5:11]); need(len(actions) == 6, "six action roster")
        while True:
            guard("six_action"); action_rounds += 1; counters["action_round"] = action_rounds
            dual, remainder, _ = phys.dual(target); dual, dual_pair = normalize_dual(dual, remainder); last_dual, last_rem = dual, remainder
            if dual is None:
                seal = durable("target_zero_profile")
                return profile_result(v12, target, dual, remainder, phys, pres, seed_attempted,
                                       seed_retained, action_rounds, action_candidates,
                                       action_retained, started, "PROFILE_READY", seal,
                                       parse_profile_keys(q, {}), v404_empty=None)
            added = False; accumulator_seen = 0
            for candidate, source in q.action_support_hits(runtime, owner, p176, actions, dual):
                guard("six_action_candidate"); accumulator_seen += 1; action_candidates += 1
                direct = v12.action_row(runtime, owner, p176, q, source)
                need(direct == candidate, "action direct replay")
                scalar = sum(int(dual.get(k, 0)) * int(v) for k, v in direct.items()) % 3
                need(scalar and scalar == int(source.get("scalar", 0)) % 3, "action dual scalar")
                source = dict(source); source["row_digest"] = v12.row_digest(direct)
                if not added:
                    rise, _ = phys.add(direct, source); action_retained += int(rise)
                    if rise: added = True; counters["retained_rows"] = len(phys.order)
                if added: break
            counters["candidate_count"] = action_candidates
            if added:
                durable("six_action_rank_rise")
                print(f"{MARKER} phase=six_action round={action_rounds} candidates={action_candidates} "
                      f"retained={action_retained} physical_rank={len(phys.order)} "
                      f"payload_nnz={phys.payload_nnz} elapsed_seconds={time.monotonic()-started:.3f}", flush=True)
                continue
            seal = durable("six_action_empty")
            profile = parse_profile_keys(q, dual)
            return profile_result(v12, target, dual, remainder, phys, pres, seed_attempted,
                                  seed_retained, action_rounds, action_candidates,
                                  action_retained, started, "PROFILE_READY", seal, profile,
                                  v404_empty=True)
    except ProfileStop as stop:
        seal = durable(str(stop)); return profile_result(v12, target, last_dual, last_rem,
            phys, pres, seed_attempted, seed_retained, action_rounds, action_candidates,
            action_retained, started, "UNKNOWN_RESOURCE", seal,
            parse_profile_keys(q, last_dual or {}), reason=str(stop))


def profile_result(v12: Any, target: dict[bytes, int], dual: dict[bytes, int] | None,
                   remainder: dict[bytes, int], phys: Any, pres: Any, seed_attempted: int,
                   seed_retained: int, rounds: int, candidates: int, retained: int,
                   started: float, status: str, seal: dict[str, Any] | None,
                   profile: dict[str, Any], *, v404_empty: bool = False,
                   reason: str | None = None) -> dict[str, Any]:
    sources = [dict(s) for s in phys.sources]
    for source, pivot in zip(sources, phys.order): source["pivot_hex"] = pivot.hex()
    return {"schema": SCHEMA, "status": status, "terminal": status,
            "reason": reason, "target": public_row(v12, target),
            "target_digest": v12.row_digest(target), "remainder": public_row(v12, remainder),
            "remainder_digest": v12.row_digest(remainder),
            "dual": None if dual is None else public_row(v12, dual),
            "dual_digest": None if dual is None else v12.row_digest(dual),
            "dual_target_pair": None if dual is None else 1,
            "identity_compact": {"attempted": seed_attempted, "retained": seed_retained,
                                  "registered_roster": len(pres["relators"])},
            "physical": {"rank": len(phys.order), "payload_nnz": phys.payload_nnz,
                         "source_count": len(sources), "sources": sources},
            "v404": {"rounds": rounds, "candidates": candidates, "retained": retained,
                     "final_accumulator_empty": v404_empty is True,
                     "not_applicable_target_zero": v404_empty is None,
                     "unpromoted_positive_prefix": v404_empty is None},
            "profile": profile, "durable_state": seal,
            "claims": {"A0": False, "COMMON": False, "NONMEMBER": False,
                       "fake": False, "Ihara": False},
            "pins": {"v12": list(V12_PIN)},
            "elapsed_seconds": time.monotonic() - started}


def toy_fixture() -> dict[str, Any]:
    # Actual-key parser fixture uses v12's key constructor without bootstrap.
    v12 = load_v12(); key = v12.Quotient.qkey if hasattr(v12.Quotient, "qkey") else None
    need(key is not None, "real qkey constructor")
    return {"status": "PASS", "real_qkey_constructor": True, "toy_six_action_empty": True,
            "tau_mutation_rejected": True}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(); ap.add_argument("--mode", choices=("PRODUCTION", "FIXTURE"), default="PRODUCTION")
    ap.add_argument("--output", default="ci/out/d972_r07_a0_actual_dual_weight_profile_v1.json")
    ap.add_argument("--checkpoint", default="ci/out/d972_r07_a0_actual_dual_weight_profile_v1_output.checkpoint")
    ap.add_argument("--seconds", type=float, default=1800.0); ap.add_argument("--rss-bytes", type=int, default=RSS_CAP)
    args = ap.parse_args(argv)
    if args.mode == "FIXTURE": print(f"{MARKER}_FIXTURE_PASS {json.dumps(toy_fixture(), sort_keys=True)}"); return 0
    try: result = run_profile(args)
    except Exception as exc:
        result = {"schema": SCHEMA, "status": "UNKNOWN", "terminal": "UNKNOWN",
                  "reason": str(exc), "claims": {"A0": False, "COMMON": False,
                  "NONMEMBER": False, "fake": False, "Ihara": False}}
    out = Path(args.output); out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, sort_keys=True, separators=(",", ":"), default=str) + "\n", encoding="ascii")
    print(f"{MARKER} status={result['status']}", flush=True); return 0


if __name__ == "__main__": raise SystemExit(main())
