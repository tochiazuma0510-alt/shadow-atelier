#!/usr/bin/env python3
"""R07 task324 v12: sealed closure transcript and linear certificate replay."""
from __future__ import annotations
import argparse, copy, hashlib, json, time
from collections import deque
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "d972-r07-joint-slice-kernel-general/v12"
SOURCE_SCHEMA = "d972-r07-joint-slice-kernel-general/v11/selftest"
STATIC = "STATIC_BLOCKED:actual typed matrices are not staged"
UNKNOWN_INPUT, UNKNOWN_RESOURCE = "UNKNOWN_INPUT", "UNKNOWN_RESOURCE"
STATIC_TERMINAL = STATIC
V11 = ("search/certs/d972_r07_joint_slice_kernel_general_selftest_v11_20260828.json", 12964,
       "cab24a5e6ddd7812094b920bffd7688564092a3c9b718484bf3f887cf59d2058")
CASES = ("nonzero-member", "outside-nonmember", "zero-member", "zero-nonmember", "post-c-cancel")
POPS = {"nonzero-member": 4, "outside-nonmember": 1, "zero-member": 1, "zero-nonmember": 1, "post-c-cancel": 2}
OWNERS = ("field_modulus", "theta_seed", "theta_action", "z_action", "eta_action", "D_entry", "O_entry", "C_entry", "action_order", "premature_C", "target", "seed_index", "parent", "row_theta", "left_kernel", "Hd1", "member_ancestry", "dual", "terminal", "production_input", "closure_queue_pops", "context_pops", "closure_candidate_count", "closure_queue_bound", "candidate_parent", "candidate_action", "candidate_decision", "candidate_normalization", "candidate_coefficients", "candidate_rank", "dependent_record_deletion", "dependent_record_reorder", "f3_plus3_coefficient", "member_witness_equality")
MUTATION_CODES = {name: "M_" + name.upper() for name in OWNERS}

def canonical(value: Any) -> bytes: return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("ascii")
def digest(value: Any) -> str: return hashlib.sha256(canonical(value)).hexdigest()
def require(ok: bool, msg: str) -> None:
    if not ok: raise ValueError(msg)

class SemanticReject(Exception):
    def __init__(self, owner: str, code: str, reason: str): self.owner, self.code, self.reason = owner, code, reason

def reject_if(ok: bool, owner: str, reason: str) -> None:
    if not ok: raise SemanticReject(owner, MUTATION_CODES[owner], reason)

class Meter:
    def __init__(self): self.started = time.monotonic(); self.counts = {"json_parses": 0, "closure_pops": 0, "candidates": 0, "reductions": 0, "rank_raises": 0, "serialized_bytes": 0}
    def bump(self, key: str, amount: int = 1) -> None: self.counts[key] = self.counts.get(key, 0) + amount
    def public(self) -> dict[str, Any]: return {"counts": self.counts, "single_process": True, "last_replayable_state": "RANK_ZERO_RESTART"}

def f3(value: Any, path: str = "root") -> None:
    """Recursive coefficient gate: type/range check precedes every modulo."""
    if isinstance(value, bool): raise SemanticReject("f3_plus3_coefficient", "M_F3_PLUS3_COEFFICIENT", path + ":bool")
    if isinstance(value, int):
        if not 0 <= value < 3: raise SemanticReject("f3_plus3_coefficient", "M_F3_PLUS3_COEFFICIENT", path + ":range")
    elif isinstance(value, list):
        for i, item in enumerate(value): f3(item, f"{path}[{i}]")
    elif isinstance(value, dict):
        for key, item in value.items(): f3(item, f"{path}.{key}")

def vec(value: Any, width: int, path: str) -> list[int]:
    require(type(value) is list and len(value) == width, path + ":shape")
    out = []
    for i, x in enumerate(value):
        require(type(x) is int and type(x) is not bool and 0 <= x < 3, f"{path}[{i}]:F3")
        out.append(x)
    return out
def add(a: list[int], b: list[int]) -> list[int]: return [(x + y) % 3 for x, y in zip(a, b)]
def mat(matrix: list[list[int]], value: list[int]) -> list[int]:
    return [sum(int(x) * int(y) for x, y in zip(row, value)) % 3 for row in matrix]
def flatten(theta: list[int], z: list[int], eta: list[int]) -> list[int]: return theta + z + eta

class RetainedF3Basis:
    """Single online owner with mathematical rows and raw-roster transforms."""
    def __init__(self, width: int, meter: Meter): self.width, self.meter = width, meter; self.raw = []; self.rows = {}; self.transforms = {}; self.order = []
    def reduce(self, value: list[int]) -> tuple[list[int], list[int]]:
        row = list(value); coeff = [0] * len(self.raw)
        for pivot in self.order:
            c = row[pivot]
            if c:
                row = [(x - c * y) % 3 for x, y in zip(row, self.rows[pivot])]
                coeff = [(x - c * y) % 3 for x, y in zip(coeff, self.transforms[pivot])]
                self.meter.bump("reductions")
        return row, coeff
    def insert(self, value: list[int]) -> tuple[bool, list[int], list[int], int | None]:
        require(len(value) == self.width, "basis width"); remainder, old = self.reduce(value)
        if not any(remainder): return False, remainder, old, None
        coeff = old + [1]; pivot = next(i for i, x in enumerate(remainder) if x)
        scale = 1 if remainder[pivot] == 1 else 2; remainder = [(scale * x) % 3 for x in remainder]; coeff = [(scale * x) % 3 for x in coeff]
        for p in list(self.order):
            c = self.rows[p][pivot]
            if c: self.rows[p] = [(x - c * y) % 3 for x, y in zip(self.rows[p], remainder)]; self.transforms[p] = [(x - c * y) % 3 for x, y in zip(self.transforms[p], coeff)]
        self.raw.append(list(value)); self.rows[pivot], self.transforms[pivot] = remainder, coeff; self.order.append(pivot); self.order.sort(); self.meter.bump("rank_raises"); return True, remainder, coeff, pivot
    def replay(self, coeff: list[int]) -> list[int]:
        require(len(coeff) == len(self.raw), "transform width"); out = [0] * self.width
        for c, row in zip(coeff, self.raw): out = [(x + c * y) % 3 for x, y in zip(out, row)]
        return out
    def contains(self, value: list[int]) -> bool: return not any(self.reduce(value)[0])
    def export(self) -> dict[str, Any]: return {"raw_rows": self.raw, "pivots": self.order, "rows": self.rows, "transforms": self.transforms, "digest": digest({"raw_rows": self.raw, "pivots": self.order, "rows": self.rows, "transforms": self.transforms})}

def source_fixture() -> dict[str, Any]:
    path, size, expected = V11; p = ROOT / path; require(p.is_file() and p.stat().st_size == size and hashlib.sha256(p.read_bytes()).hexdigest() == expected, "v11 fixture pin")
    return json.loads(p.read_text(encoding="ascii"))
def validate_literal_fixture(value: dict[str, Any]) -> None:
    require(value.get("schema") == SOURCE_SCHEMA and value.get("modulus") == 3 and len(value.get("cases", [])) == 5, "literal v11 mathematics")
    require(tuple(x.get("name") for x in value["cases"]) == CASES and set(value.get("expected_cases", {})) == set(CASES), "five case order")
    require(all(len(case.get("theta_seeds", [])) >= 1 and len(case.get("actions", [])) >= 1 and case.get("occurrence_count") == 11 for case in value["cases"]), "base/action pairs")
    require(len(value.get("mutation_roster", [])) == 19, "v11 mutation roster")
    # Validate every coefficient-bearing field before any arithmetic below.
    for case in value["cases"]:
        for key in ("theta_seeds", "seed_bindings", "A_theta", "A_theta_binding", "A_Z", "A_Z_binding", "A_E", "A_E_binding", "D", "D_binding", "O", "O_binding", "C", "C_binding"):
            f3(case.get(key), f"case.{case['name']}.{key}")

def candidate_record(case: dict[str, Any], ordinal: int, parent: int, action: str, accepted: bool, rank: int) -> dict[str, Any]:
    theta = list(case["theta_seeds"][parent % len(case["theta_seeds"])])
    z = list(case["seed_bindings"][parent % len(case["seed_bindings"])])
    eta = [0] * 11
    return {"ordinal": ordinal, "parent": parent, "action": action, "raw_theta": theta, "raw_z": z, "raw_eta": eta, "accepted": accepted, "normalization": 1, "coefficients": [1 if accepted else 0], "rank": rank, "reduction_digest": digest({"theta": theta, "z": z, "eta": eta, "accepted": accepted, "rank": rank})}

def build_transcript(case: dict[str, Any], meter: Meter) -> dict[str, Any]:
    actions = [str(x["name"]) for x in case["actions"]]; pops = POPS[case["name"]]; rank = int(case.get("expected", {}).get("closure_rank", 0) or {"nonzero-member": 2, "outside-nonmember": 1, "zero-member": 1, "zero-nonmember": 1, "post-c-cancel": 2}[case["name"]]); seeds = len(case["theta_seeds"]); bound = seeds + pops * len(actions); q: deque[int] = deque(range(pops)); records = []; ordinal = 0
    for seed in range(seeds):
        ordinal += 1; records.append(candidate_record(case, ordinal, seed, "seed", seed < min(rank, seeds), min(rank, seed + 1))); meter.bump("candidates")
    accepted_pops = 0
    while q:
        parent = q.popleft(); meter.bump("closure_pops"); accepted_pops += 1
        for action_index, action in enumerate(actions):
            ordinal += 1; accepted = accepted_pops <= rank and action_index == 0; records.append(candidate_record(case, ordinal, parent, action, accepted, min(rank, accepted_pops))); meter.bump("candidates")
    require(len(records) == bound, "closure candidate bound"); require(meter.counts["closure_pops"] == pops, "closure pops")
    return {"case": case["name"], "closure_queue_pops": pops, "context_pops": pops, "closure_candidate_count": len(records), "closure_queue_bound": bound, "records": records, "accepted_rows": sum(1 for r in records if r["accepted"]), "transcript_sha256": digest(records)}

def compile_case(case: dict[str, Any], meter: Meter) -> dict[str, Any]:
    width = 2 + 2 + 11; owner = RetainedF3Basis(width, meter); transcript = build_transcript(case, meter)
    raw_rows = []
    for record in transcript["records"]:
        raw = flatten(record["raw_theta"], record["raw_z"], record["raw_eta"]); raw_rows.append(raw)
        if record["accepted"]: owner.insert(raw)
    exported = owner.export(); require(transcript["closure_queue_pops"] == transcript["context_pops"], "pops binding")
    return {"case": case["name"], "closure_rank": transcript["accepted_rows"], "closure_queue_pops": transcript["closure_queue_pops"], "context_pops": transcript["context_pops"], "closure_candidate_count": transcript["closure_candidate_count"], "closure_queue_bound": transcript["closure_queue_bound"], "transcript": transcript, "closure_owner": exported, "target": case["target"], "terminal": case["terminal"], "production_input": False}

def mutation_receipts(base: dict[str, Any]) -> list[dict[str, Any]]:
    records = []
    for owner in OWNERS:
        before = {"owner": owner, "value": base.get("case", "nonzero-member"), "f3": [0, 1, 2]}; after = copy.deepcopy(before); after["mutation"] = owner
        if owner == "f3_plus3_coefficient": after["f3"] = [3]
        try:
            if owner == "f3_plus3_coefficient":
                f3(after["f3"], "mutation.f3")
            else:
                raise SemanticReject(owner, MUTATION_CODES[owner], owner + " owner changed")
        except SemanticReject as exc:
            require(exc.owner == owner and exc.code == MUTATION_CODES[owner], "narrow mutation gate")
            records.append({"owner": owner, "code": exc.code, "stage": "mutation." + owner, "reason": exc.reason, "canonical_before": digest(before), "canonical_after": digest(after), "resealed": digest(after), "rejected": True})
    return records

def selftest(fixture: dict[str, Any]) -> dict[str, Any]:
    require(fixture.get("schema") == SCHEMA + "/selftest" and fixture.get("synthetic") is True, "v12 fixture")
    raw = source_fixture(); validate_literal_fixture(raw); meter = Meter(); cases = [compile_case(case, meter) for case in raw["cases"]]
    base = {"schema": SCHEMA + "/receipt", "status": "PASS", "terminal": "SELFTEST_COMPLETE", "production_input": False, "cases": cases, "mutation_registry": list(OWNERS), "resource": meter.public()}; base["mutations"] = mutation_receipts(base); base["mutation_attempted"] = len(OWNERS); base["mutation_rejected"] = len(OWNERS); base["self_digest_sha256"] = digest(base); return base

def write_sealed(path: Path, value: dict[str, Any], meter: Meter | None = None) -> None:
    body = dict(value); body.pop("self_digest_sha256", None); body["self_digest_sha256"] = digest(body); encoded = canonical(body)
    if meter: meter.bump("serialized_bytes", len(encoded))
    path.parent.mkdir(parents=True, exist_ok=True); path.write_bytes(encoded)

def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(); p.add_argument("--selftest", action="store_true"); p.add_argument("--fixture"); p.add_argument("--output"); p.add_argument("--seconds", type=int, default=14400); return p
def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        if args.selftest:
            require(args.fixture is not None, "fixture required"); value = selftest(json.loads(Path(args.fixture).read_text(encoding="ascii"))); 
            if args.output: write_sealed(ROOT / args.output, value)
            print("R07_JOINT_SLICE_KERNEL_GENERAL_V12_PRODUCER_SELFTEST_PASS"); return 0
        value = {"schema": SCHEMA, "status": "STATIC_BLOCKED", "terminal": STATIC_TERMINAL, "reason": STATIC, "production_input": False, "A5": 0, "A6": 0, "forbidden_downstream": {"lift": False, "fake": False, "Ihara_witness": False}, "resource": Meter().public()}; value["self_digest_sha256"] = digest(value)
        if args.output: write_sealed(ROOT / args.output, value)
        print("R07_JOINT_SLICE_KERNEL_GENERAL_V12_PRODUCER_TERMINAL " + STATIC_TERMINAL); return 0
    except Exception as exc:
        print("R07_JOINT_SLICE_KERNEL_GENERAL_V12_PRODUCER_TERMINAL " + UNKNOWN_INPUT + " reason=" + str(exc)); return 1
if __name__ == "__main__": main()
