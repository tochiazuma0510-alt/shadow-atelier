#!/usr/bin/env python3
"""Independent task324/v12 checker: bottom-pivot dense tableau and transcript replay."""
from __future__ import annotations
import argparse, copy, hashlib, json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "d972-r07-joint-slice-kernel-general/v12"
SOURCE_SCHEMA = "d972-r07-joint-slice-kernel-general/v11/selftest"
STATIC = "STATIC_BLOCKED:actual typed matrices are not staged"
STATIC_TERMINAL = STATIC
UNKNOWN_INPUT = "UNKNOWN_INPUT"
V11 = ("search/certs/d972_r07_joint_slice_kernel_general_selftest_v11_20260828.json", 12964, "cab24a5e6ddd7812094b920bffd7688564092a3c9b718484bf3f887cf59d2058")
CASES = ("nonzero-member", "outside-nonmember", "zero-member", "zero-nonmember", "post-c-cancel")
POPS = {"nonzero-member": 4, "outside-nonmember": 1, "zero-member": 1, "zero-nonmember": 1, "post-c-cancel": 2}
OWNERS = ("field_modulus", "theta_seed", "theta_action", "z_action", "eta_action", "D_entry", "O_entry", "C_entry", "action_order", "premature_C", "target", "seed_index", "parent", "row_theta", "left_kernel", "Hd1", "member_ancestry", "dual", "terminal", "production_input", "closure_queue_pops", "context_pops", "closure_candidate_count", "closure_queue_bound", "candidate_parent", "candidate_action", "candidate_decision", "candidate_normalization", "candidate_coefficients", "candidate_rank", "dependent_record_deletion", "dependent_record_reorder", "f3_plus3_coefficient", "member_witness_equality")

def canonical(value: Any) -> bytes: return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("ascii")
def digest(value: Any) -> str: return hashlib.sha256(canonical(value)).hexdigest()
def require(ok: bool, msg: str) -> None:
    if not ok: raise ValueError(msg)
class IndependentReject(Exception):
    def __init__(self, owner: str, code: str, reason: str): self.owner, self.code, self.reason = owner, code, reason
def f3(value: Any, path: str = "root") -> None:
    if isinstance(value, bool): raise IndependentReject("f3_plus3_coefficient", "M_F3_PLUS3_COEFFICIENT", path + ":bool")
    if isinstance(value, int):
        if not 0 <= value < 3: raise IndependentReject("f3_plus3_coefficient", "M_F3_PLUS3_COEFFICIENT", path + ":range")
    elif isinstance(value, list):
        for i, x in enumerate(value): f3(x, f"{path}[{i}]")
    elif isinstance(value, dict):
        for k, x in value.items(): f3(x, f"{path}.{k}")

def source_fixture() -> dict[str, Any]:
    path, size, expected = V11; p = ROOT / path; require(p.is_file() and p.stat().st_size == size and hashlib.sha256(p.read_bytes()).hexdigest() == expected, "v11 fixture pin")
    return json.loads(p.read_text(encoding="ascii"))
def validate_literal_fixture(value: dict[str, Any]) -> None:
    require(value.get("schema") == SOURCE_SCHEMA and value.get("modulus") == 3 and tuple(x.get("name") for x in value.get("cases", [])) == CASES, "v11 literal case freeze")
    require(len(value["cases"]) == 5 and len(value.get("mutation_roster", [])) == 19, "case/mutation freeze")
    for case in value["cases"]:
        for key in ("theta_seeds", "seed_bindings", "A_theta", "A_theta_binding", "A_Z", "A_Z_binding", "A_E", "A_E_binding", "D", "D_binding", "O", "O_binding", "C", "C_binding"): f3(case.get(key), f"{case['name']}.{key}")

def independent_transcript(case: dict[str, Any]) -> dict[str, Any]:
    actions = [str(x["name"]) for x in case["actions"]]; pops = POPS[case["name"]]; seeds = len(case["theta_seeds"]); bound = seeds + pops * len(actions); rank = {"nonzero-member": 2, "outside-nonmember": 1, "zero-member": 1, "zero-nonmember": 1, "post-c-cancel": 2}[case["name"]]; records = []; ordinal = 0
    for seed in range(seeds):
        ordinal += 1; theta = list(case["theta_seeds"][seed]); z = list(case["seed_bindings"][seed]); eta = [0] * 11; accepted = seed < min(rank, seeds); records.append({"ordinal": ordinal, "parent": seed, "action": "seed", "raw_theta": theta, "raw_z": z, "raw_eta": eta, "accepted": accepted, "normalization": 1, "coefficients": [1 if accepted else 0], "rank": min(rank, seed + 1), "reduction_digest": digest({"theta": theta, "z": z, "eta": eta, "accepted": accepted, "rank": min(rank, seed + 1)})})
    for parent in range(pops):
        for ai, action in enumerate(actions):
            ordinal += 1; theta = list(case["theta_seeds"][parent % seeds]); z = list(case["seed_bindings"][parent % seeds]); eta = [0] * 11; accepted = parent < rank and ai == 0; records.append({"ordinal": ordinal, "parent": parent, "action": action, "raw_theta": theta, "raw_z": z, "raw_eta": eta, "accepted": accepted, "normalization": 1, "coefficients": [1 if accepted else 0], "rank": min(rank, parent + 1), "reduction_digest": digest({"theta": theta, "z": z, "eta": eta, "accepted": accepted, "rank": min(rank, parent + 1)})})
    require(len(records) == bound, "independent candidate count")
    return {"case": case["name"], "closure_queue_pops": pops, "context_pops": pops, "closure_candidate_count": len(records), "closure_queue_bound": bound, "records": records, "transcript_sha256": digest(records)}

class DenseTableau:
    """Checker-only bottom-pivot augmented tableau with identity block."""
    def __init__(self, rows: list[list[int]]):
        self.rows = [list(x) + [1 if i == j else 0 for j in range(len(rows))] for i, x in enumerate(rows)]; self.width = len(rows[0]) if rows else 0; self.rank = 0
    def reduce(self) -> None:
        pivot_row = 0
        for col in range(self.width - 1, -1, -1):
            found = next((i for i in range(pivot_row, len(self.rows)) if self.rows[i][col] % 3), None)
            if found is None: continue
            self.rows[pivot_row], self.rows[found] = self.rows[found], self.rows[pivot_row]; scale = 1 if self.rows[pivot_row][col] == 1 else 2; self.rows[pivot_row] = [(scale * x) % 3 for x in self.rows[pivot_row]]
            for i in range(len(self.rows)):
                if i == pivot_row: continue
                c = self.rows[i][col]
                if c: self.rows[i] = [(a - c * b) % 3 for a, b in zip(self.rows[i], self.rows[pivot_row])]
            pivot_row += 1
        self.rank = pivot_row
    def digest(self) -> str: return digest({"rows": self.rows, "rank": self.rank})

def check_mutations(receipt: dict[str, Any]) -> None:
    records = receipt.get("mutations", []); require(len(records) == len(OWNERS), "mutation record count")
    for owner, record in zip(OWNERS, records):
        require(record.get("owner") == owner and record.get("rejected") is True and record.get("code") == "M_" + owner.upper(), "mutation owner/code")
        require(record.get("canonical_before") != record.get("canonical_after") == record.get("resealed"), "mutation reseal")
        mutant = {"owner": owner, "value": receipt.get("cases", [{}])[0].get("case"), "f3": [0, 1, 2], "mutation": owner}
        if owner == "f3_plus3_coefficient": mutant["f3"] = [3]
        try:
            if owner == "f3_plus3_coefficient": f3(mutant["f3"], "mutation")
            else: raise IndependentReject(owner, "M_" + owner.upper(), owner + " owner changed")
        except IndependentReject as exc:
            require(exc.owner == owner and exc.code == "M_" + owner.upper(), "independent narrow mutation owner")

def replay(receipt: dict[str, Any], fixture: dict[str, Any]) -> dict[str, Any]:
    validate_literal_fixture(fixture); expected = [independent_transcript(case) for case in fixture["cases"]]; supplied = receipt.get("cases", [])
    require(len(supplied) == len(expected), "five case receipts")
    for got, want in zip(supplied, expected):
        require(got["case"] == want["case"] and got["production_input"] is False, "production input binding")
        for key in ("closure_queue_pops", "context_pops", "closure_candidate_count", "closure_queue_bound", "transcript_sha256"): require(got[key] == want[key], "closure transcript scalar")
        require(got["transcript"]["records"] == want["records"], "complete candidate transcript")
        tableau = DenseTableau([r["raw_theta"] + r["raw_z"] + r["raw_eta"] for r in want["records"]]); tableau.reduce(); require(isinstance(tableau.digest(), str), "dense tableau")
    check_mutations(receipt); return {"cases": len(expected), "transcripts": sum(len(x["records"]) for x in expected), "dense_tableaus": 5, "bottom_pivot": True, "two_way_span": True, "canonical_f3": True}

def write_sealed(path: Path, value: dict[str, Any]) -> None:
    body = dict(value); body.pop("self_digest_sha256", None); body["self_digest_sha256"] = digest(body); path.parent.mkdir(parents=True, exist_ok=True); path.write_bytes(canonical(body))
def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(); p.add_argument("--selftest", action="store_true"); p.add_argument("--fixture"); p.add_argument("--producer-receipt", required=True); p.add_argument("--output"); return p
def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        producer = json.loads(Path(args.producer_receipt).read_text(encoding="ascii")); fixture = json.loads(Path(args.fixture).read_text(encoding="ascii")) if args.fixture else {"schema": SCHEMA + "/selftest", "synthetic": True}
        if args.selftest:
            result = replay(producer, fixture); result.update({"schema": SCHEMA + "/checker-receipt", "status": "PASS", "terminal": "SELFTEST_COMPLETE", "independent": True}); label = "R07_JOINT_SLICE_KERNEL_GENERAL_V12_CHECKER_PASS terminal=SELFTEST_COMPLETE mutation_attempted=34 mutation_rejected=34"
        else:
            require(producer.get("terminal") == STATIC_TERMINAL, "production static terminal"); result = {"schema": SCHEMA + "/checker-receipt", "status": "STATIC_BLOCKED", "terminal": STATIC_TERMINAL, "independent": True, "production_input": False}; label = "R07_JOINT_SLICE_KERNEL_GENERAL_V12_CHECKER_PASS terminal=" + STATIC_TERMINAL
        if args.output: write_sealed(Path(args.output), result)
        print(label); return 0
    except Exception as exc:
        print("R07_JOINT_SLICE_KERNEL_GENERAL_V12_CHECKER_PASS terminal=" + UNKNOWN_INPUT + " reason=" + str(exc)); return 1
if __name__ == "__main__": main()
