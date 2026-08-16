#!/usr/bin/env python3
"""Generate and solve one bounded B4 SAT shard on a CI runner.

The CNF is deliberately generated under the runner's temporary output
directory; no giant CNF is committed.  A SAT model is handed to the
independent OR checker, whose receipt is the only finite-image witness output
that can receive the ``B4-A_CANDIDATE`` classification.  UNSAT is always
reported as finite-degree UNKNOWN, whether or not its DRAT proof verifies.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
from typing import Any, Sequence

from encode_d972_b4_perm_v1 import encode_targets, load_relators, load_word_keys
from plan_d972_b4_unique_roof_shards_v1 import build


def sha_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_capture(argv: Sequence[str], *, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(list(argv), cwd=cwd, text=True, capture_output=True,
                          check=False)


def classify_solver(solver_code: int, checker_code: int | None,
                    proof_verified: bool) -> str:
    if solver_code == 10:
        return ("B4-A_CANDIDATE_FINITE_SAT_OR" if checker_code == 0
                else "REJECTED_SAT_MODEL")
    if solver_code == 20:
        return ("UNKNOWN_FINITE_DEGREE_UNSAT_PROOF_VERIFIED"
                if proof_verified else
                "UNKNOWN_FINITE_DEGREE_UNSAT_PROOF_UNVERIFIED")
    return "UNKNOWN_SOLVER"


def choose_shard(rows: list[list[Any]], shard: int, shard_size: int,
                 max_word_length: int) -> tuple[dict[str, Any], list[int]]:
    if shard_size < 2:
        raise ValueError("OR SAT shard-size must be at least two")
    if max_word_length < 1:
        raise ValueError("max-word-length must be positive")
    plan = build(rows, shard_size, max_word_length)
    shards = plan["shards"]
    if not 0 <= shard < len(shards):
        raise ValueError(f"shard {shard} outside planned range 0..{len(shards)-1}")
    selected = shards[shard]
    indices = [int(i) for i in selected["row_indices"]]
    if len(indices) < 2:
        raise ValueError("selected OR shard has fewer than two nonempty words")
    words = [rows[i][2] for i in indices]
    if any(not word for word in words) or len({tuple(word) for word in words}) != len(words):
        raise ValueError("selected shard contains an empty or duplicate roof")
    return plan, indices


def verify_drat(drat_trim: Path, cnf: Path, proof: Path, out_dir: Path) -> tuple[bool, str]:
    if not proof.is_file():
        return False, "proof file missing"
    core = out_dir / "core.cnf"
    lrat = out_dir / "proof.lrat"
    proc = run_capture([str(drat_trim), str(cnf), str(proof), "-c", str(core),
                        "-L", str(lrat)])
    text = proc.stdout + "\n" + proc.stderr
    (out_dir / "drat_verify.txt").write_text(text, encoding="utf-8")
    return proc.returncode == 0 and "s VERIFIED" in text, text[-1000:]


def run(args: argparse.Namespace) -> dict[str, Any]:
    out_dir = args.output_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    rels, rel_sha = load_relators(args.relators)
    rows, artifact_sha, _ = load_word_keys(args.word_key_artifact)
    plan, indices = choose_shard(rows, args.shard, args.shard_size,
                                 args.max_word_length)

    cnf = out_dir / "problem.cnf"
    manifest_path = out_dir / "manifest.json"
    manifest_obj = None
    encoded, manifest_obj = encode_targets(args.degree, rels, rows, indices)
    manifest_obj.update({
        "runner_schema": "d972-b4-sat-shard-run/v1",
        "shard": args.shard,
        "shard_size": args.shard_size,
        "max_word_length": args.max_word_length,
        "plan_unique_word_count": plan["unique_word_count"],
        "empty_rows_excluded": plan["empty_rows_excluded"],
        "duplicate_copies_excluded": plan["duplicate_copies_excluded"],
    })
    encoded.write(cnf, [str(manifest_obj["schema"]),
                        json.dumps(manifest_obj, sort_keys=True)])
    manifest_obj["cnf_sha256"] = sha_file(cnf)
    manifest_path.write_text(json.dumps(manifest_obj, indent=2, sort_keys=True) + "\n",
                             encoding="utf-8")

    proof = out_dir / "proof.drat"
    solver_stdout = out_dir / "solver.stdout.txt"
    solver_stderr = out_dir / "solver.stderr.txt"
    solver_proc = run_capture([str(args.solver), str(cnf), str(proof), "--no-binary"])
    solver_stdout.write_text(solver_proc.stdout, encoding="utf-8")
    solver_stderr.write_text(solver_proc.stderr, encoding="utf-8")
    solver_version = run_capture([str(args.solver), "--version"])
    (out_dir / "solver_version.txt").write_text(
        solver_version.stdout + "\n" + solver_version.stderr, encoding="utf-8")

    checker_code: int | None = None
    checker_status: str | None = None
    finite_receipt: Path | None = None
    checker_stdout = ""
    if solver_proc.returncode == 10:
        model = out_dir / "model_vlines.txt"
        model.write_text("\n".join(
            line for line in solver_proc.stdout.splitlines()
            if line.lstrip().startswith("v")
        ) + "\n", encoding="utf-8")
        finite_receipt = out_dir / "finite_image_receipt.json"
        checker = args.checker
        checker_proc = run_capture([
            sys.executable, str(checker), "--cnf", str(cnf),
            "--manifest", str(manifest_path), "--model", str(model),
            "--relators", str(args.relators),
            "--word-key-artifact", str(args.word_key_artifact),
            "--receipt", str(finite_receipt),
        ])
        checker_code = checker_proc.returncode
        checker_stdout = checker_proc.stdout + "\n" + checker_proc.stderr
        (out_dir / "model_checker.txt").write_text(checker_stdout,
                                                    encoding="utf-8")
        if finite_receipt.is_file():
            try:
                checker_status = json.loads(finite_receipt.read_text(
                    encoding="utf-8")).get("status")
            except (OSError, json.JSONDecodeError):
                checker_status = None

    proof_verified = False
    proof_tail = ""
    if solver_proc.returncode == 20 and args.drat_trim is not None:
        proof_verified, proof_tail = verify_drat(args.drat_trim, cnf, proof, out_dir)

    status = classify_solver(solver_proc.returncode, checker_code, proof_verified)
    # A zero checker exit is necessary but not sufficient: the expected
    # finite-image receipt must also be present and carry its exact schema
    # status.  This keeps a malformed/partial checker result fail-closed.
    if (solver_proc.returncode == 10 and checker_code == 0 and
            checker_status != "B4-A_CANDIDATE_FINITE_SAT_OR"):
        status = "REJECTED_SAT_MODEL"
    receipt: dict[str, Any] = {
        "schema": "d972-b4-sat-shard-run/v1",
        "status": status,
        "bounded_status": "FINITE_CANDIDATE_ONLY",
        "degree": args.degree,
        "shard": args.shard,
        "shard_size": args.shard_size,
        "max_word_length": args.max_word_length,
        "target_indices": indices,
        "target_count": len(indices),
        "target_words": [rows[i][2] for i in indices],
        "relator_sha256": rel_sha,
        "rho_words_source": manifest_obj["rho_words_source"],
        "rho_words_sha256": manifest_obj["rho_words_sha256"],
        "p2_input_schema": manifest_obj["p2_input_schema"],
        "p2_input_file_sha256": manifest_obj["p2_input_file_sha256"],
        "target_artifact_sha256": artifact_sha,
        "cnf_sha256": sha_file(cnf),
        "nvars": manifest_obj["nvars"],
        "clauses": manifest_obj["clauses"],
        "solver": str(args.solver),
        "solver_exit_code": solver_proc.returncode,
        "solver_version": (solver_version.stdout + solver_version.stderr).strip(),
        "proof_verified": proof_verified,
        "checker_exit_code": checker_code,
        "checker_status": checker_status,
        "finite_image_receipt_sha256": (
            sha_file(finite_receipt) if finite_receipt and finite_receipt.is_file()
            else None
        ),
        "interpretation": (
            "SAT plus independent finite-image receipt is a B4-A candidate; "
            "UNSAT is UNKNOWN at this finite degree/shard and cannot imply B."
        ),
    }
    if proof_tail:
        receipt["proof_tail"] = proof_tail
    (out_dir / "run_receipt.json").write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return receipt


def self_test() -> None:
    assert classify_solver(10, 0, False) == "B4-A_CANDIDATE_FINITE_SAT_OR"
    assert classify_solver(10, 1, False) == "REJECTED_SAT_MODEL"
    assert classify_solver(20, None, True) == "UNKNOWN_FINITE_DEGREE_UNSAT_PROOF_VERIFIED"
    assert classify_solver(20, None, False) == "UNKNOWN_FINITE_DEGREE_UNSAT_PROOF_UNVERIFIED"
    assert classify_solver(0, None, False) == "UNKNOWN_SOLVER"
    rows = [[0, [0], [1]], [0, [1], [1]], [0, [2], [2]], [0, [3], [2]]]
    try:
        choose_shard(rows, 0, 1, 40)
    except ValueError:
        pass
    else:
        raise AssertionError("singleton OR shard accepted")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--degree", type=int)
    ap.add_argument("--shard", type=int)
    ap.add_argument("--shard-size", type=int, default=8)
    ap.add_argument("--max-word-length", type=int, default=40)
    ap.add_argument("--relators", type=Path)
    ap.add_argument("--word-key-artifact", type=Path)
    ap.add_argument("--solver", type=Path)
    ap.add_argument("--drat-trim", type=Path)
    ap.add_argument("--checker", type=Path,
                    default=Path(__file__).with_name("check_d972_b4_perm_or_v1.py"))
    ap.add_argument("--output-dir", type=Path)
    args = ap.parse_args()
    if args.self_test:
        self_test()
        print("D972_B4_SAT_SHARD_RUNNER_SELFTEST_PASS")
        return 0
    required = (args.degree, args.shard, args.relators, args.word_key_artifact,
                args.solver, args.output_dir)
    if any(value is None for value in required):
        ap.error("--degree, --shard, --relators, --word-key-artifact, --solver, and --output-dir are required unless --self-test")
    if not 2 <= args.degree <= 8:
        ap.error("--degree must be in [2,8]")
    receipt = run(args)
    print(json.dumps(receipt, sort_keys=True))
    # A finite UNKNOWN is a successful bounded run, not a workflow failure.
    # A SAT model rejected by the independent checker (or a solver launch
    # failure) remains a hard CI failure.
    status = str(receipt["status"])
    if status.startswith("UNKNOWN_") or status == "B4-A_CANDIDATE_FINITE_SAT_OR":
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
