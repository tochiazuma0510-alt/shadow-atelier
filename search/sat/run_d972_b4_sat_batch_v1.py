#!/usr/bin/env python3
"""Run a bounded canonical-v2 SAT shard range sequentially.

This launcher is intentionally callable from the default ``gap-run`` workflow
through ``d972_b4_sat_batch_v1.g``.  The GAP preamble supplies only four
integers; all paths, input digests, solver repositories, and the OR shard size
are fixed here.  Kissat and DRAT-trim are built at pinned commits below a
temporary directory, while the canonical shard runner remains the independent
SAT/model/receipt implementation.

This is finite exploration only.  A checked SAT defect is a B4-A candidate;
every UNSAT result is finite-degree UNKNOWN.  A verified UNSAT proof permits
deleting the large CNF/proof from the collected artifact, but a small receipt
records their hashes and the independent DRAT-trim output.  Candidate or
unverified/error evidence is retained instead of being silently discarded.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time
from typing import Any, Iterable, Sequence

from plan_d972_b4_unique_roof_shards_v1 import build, load


ROOT = Path(__file__).resolve().parents[2]
SAT_DIR = ROOT / "search" / "sat"
WRAPPER = ROOT / "search" / "d972_b4_sat_batch_v1.g"
RELATORS = ROOT / "search" / "certs" / "d972_b4_p2_magnus_input_v2_20260816.json"
WORD_KEY_ARTIFACT = ROOT / "search" / "certs" / "d972_b4_word_key_artifact_v1_20260816.json"
RUNNER = SAT_DIR / "run_d972_b4_sat_shard_v1.py"
ENCODER = SAT_DIR / "encode_d972_b4_perm_v1.py"
MODEL_CHECKER = SAT_DIR / "check_d972_b4_perm_model_v1.py"
OR_CHECKER = SAT_DIR / "check_d972_b4_perm_or_v1.py"
PLANNER = SAT_DIR / "plan_d972_b4_unique_roof_shards_v1.py"
MATRIX = SAT_DIR / "prepare_d972_b4_sat_matrix_v1.py"

SCHEMA = "d972-b4-sat-batch/v1"
SHARD_SIZE = 8
MAX_DEGREE = 8
MAX_WORD_LENGTH = 94
P2_INPUT_SCHEMA = "d972-b4-p2-magnus-input/v2"
P2_INPUT_SHA256 = "c61b2b77131127aca83a8d7c56b7fdadd2d519b040ea4d91093622c813c2b4a9"
RHO_WORDS_SOURCE = "universal_v2_canonical"
RHO_WORDS_SHA256 = "23db316e11e6486e0475b8425ff8ea6666941b5bff0943bf872e39761d0398ed"
KISSAT_COMMIT = "8af8e56f174b778aef3aa45af9f739b2a5f492c2"
DRAT_TRIM_COMMIT = "2e3b2dc0ecf938addbd779d42877b6ed69d9a985"
KISSAT_REPO = "https://github.com/arminbiere/kissat.git"
DRAT_TRIM_REPO = "https://github.com/marijnheule/drat-trim.git"
OUTPUT_ROOT = ROOT / "ci" / "out" / "d972_b4_sat_batch_v1"


def sha_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def json_write(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n",
                    encoding="utf-8")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def checked_repo_path(path: Path, label: str) -> Path:
    resolved = path.resolve()
    require(resolved.is_file(), f"{label} is missing: {path}")
    try:
        resolved.relative_to(ROOT)
    except ValueError as exc:
        raise ValueError(f"{label} escapes repository root: {path}") from exc
    return resolved


def run_logged(argv: Sequence[str], *, cwd: Path, log: Path) -> None:
    log.parent.mkdir(parents=True, exist_ok=True)
    with log.open("a", encoding="utf-8", errors="replace") as stream:
        stream.write("$ " + " ".join(argv) + "\n")
        stream.flush()
        proc = subprocess.run(list(argv), cwd=cwd, stdout=stream,
                              stderr=subprocess.STDOUT, check=False)
    if proc.returncode != 0:
        raise RuntimeError(f"command failed ({proc.returncode}): {' '.join(argv)}")


@dataclass(frozen=True)
class Solvers:
    kissat: Path
    drat_trim: Path
    kissat_sha256: str
    drat_trim_sha256: str


def build_solvers(build_root: Path) -> Solvers:
    """Clone and build only the two pinned solver commits in /tmp."""
    build_root.mkdir(parents=True, exist_ok=False)
    log = build_root / "build.log"
    kissat_src = build_root / "kissat"
    drat_src = build_root / "drat-trim"
    run_logged(["git", "clone", "--no-tags", KISSAT_REPO, str(kissat_src)],
               cwd=build_root, log=log)
    run_logged(["git", "-C", str(kissat_src), "checkout", "--detach",
                KISSAT_COMMIT], cwd=build_root, log=log)
    run_logged(["git", "-C", str(kissat_src), "rev-parse", "--verify",
                KISSAT_COMMIT + "^{commit}"], cwd=build_root, log=log)
    run_logged(["./configure"], cwd=kissat_src, log=log)
    run_logged(["make", "-j2"], cwd=kissat_src, log=log)
    kissat = kissat_src / "build" / "kissat"
    require(kissat.is_file() and os.access(kissat, os.X_OK),
            "pinned Kissat binary missing")

    run_logged(["git", "clone", "--no-tags", DRAT_TRIM_REPO, str(drat_src)],
               cwd=build_root, log=log)
    run_logged(["git", "-C", str(drat_src), "checkout", "--detach",
                DRAT_TRIM_COMMIT], cwd=build_root, log=log)
    run_logged(["git", "-C", str(drat_src), "rev-parse", "--verify",
                DRAT_TRIM_COMMIT + "^{commit}"], cwd=build_root, log=log)
    run_logged(["make"], cwd=drat_src, log=log)
    drat_trim = drat_src / "drat-trim"
    require(drat_trim.is_file() and os.access(drat_trim, os.X_OK),
            "pinned DRAT-trim binary missing")
    return Solvers(kissat=kissat, drat_trim=drat_trim,
                   kissat_sha256=sha_file(kissat),
                   drat_trim_sha256=sha_file(drat_trim))


def run_source_selftests() -> None:
    scripts = [
        (ENCODER, "D972_B4_SAT_ENCODER_SELFTEST_PASS"),
        (MODEL_CHECKER, "D972_B4_SAT_CHECKER_SELFTEST_PASS"),
        (OR_CHECKER, "D972_B4_SAT_OR_CHECKER_SELFTEST_PASS"),
        (PLANNER, "D972_B4_SAT_SHARD_PLANNER_SELFTEST_PASS"),
        (MATRIX, "D972_B4_SAT_MATRIX_SELFTEST_PASS"),
        (RUNNER, "D972_B4_SAT_SHARD_RUNNER_SELFTEST_PASS"),
    ]
    for script, marker in scripts:
        proc = subprocess.run([sys.executable, "-B", str(script), "--self-test"],
                              cwd=ROOT, text=True, capture_output=True,
                              encoding="utf-8", errors="replace", check=False)
        if proc.returncode != 0 or marker not in proc.stdout:
            raise RuntimeError(
                f"source selftest failed: {script.name}\n"
                f"stdout={proc.stdout[-2000:]}\nstderr={proc.stderr[-2000:]}")


def validate_inputs(degree: int, shard_start: int, shard_end: int,
                    max_word_length: int) -> tuple[list[list[Any]], dict[str, Any]]:
    require(2 <= degree <= MAX_DEGREE, "degree must be in [2,8]")
    require(0 <= shard_start <= shard_end, "shard range must be nonempty and ordered")
    require(1 <= max_word_length <= MAX_WORD_LENGTH,
            "max word length must be in [1,94]")
    checked_repo_path(RELATORS, "canonical v2 input")
    checked_repo_path(WORD_KEY_ARTIFACT, "word/key artifact")
    require(sha_file(RELATORS) == P2_INPUT_SHA256,
            "canonical v2 input SHA-256 drift")
    rel_obj = json.loads(RELATORS.read_text(encoding="utf-8"))
    require(isinstance(rel_obj, dict) and rel_obj.get("schema") == P2_INPUT_SCHEMA,
            "canonical v2 input schema drift")
    require(rel_obj.get("rho_words_source") == RHO_WORDS_SOURCE,
            "canonical rho source drift")
    rows = load(WORD_KEY_ARTIFACT)
    plan = build(rows, SHARD_SIZE, max_word_length)
    require(shard_end < len(plan["shards"]),
            f"shard range exceeds planned count {len(plan['shards'])}")
    for shard in plan["shards"][shard_start:shard_end + 1]:
        require(int(shard["word_count"]) >= 2,
                f"shard {shard['shard']} has fewer than two OR words")
    return rows, plan


def file_manifest(directory: Path, names: Iterable[str]) -> list[dict[str, Any]]:
    result = []
    for name in names:
        path = directory / name
        if path.is_file():
            result.append({"path": name, "size": path.stat().st_size,
                           "sha256": sha_file(path)})
    return result


def preserve_evidence(work: Path, evidence: Path, status: str) -> dict[str, Any]:
    """Retain all evidence for SAT/error paths, light evidence for verified UNSAT."""
    evidence.mkdir(parents=True, exist_ok=False)
    receipt_path = work / "run_receipt.json"
    receipt = json.loads(receipt_path.read_text(encoding="utf-8")) if receipt_path.is_file() else {}
    verified_unsat = status == "UNKNOWN_FINITE_DEGREE_UNSAT_PROOF_VERIFIED"
    if not verified_unsat:
        shutil.copytree(work, evidence, dirs_exist_ok=True)
        return {"mode": "full", "path": str(evidence.relative_to(ROOT))}

    keep = ["run_receipt.json", "manifest.json", "drat_verify.txt",
            "solver.stdout.txt", "solver.stderr.txt", "solver_version.txt"]
    for name in keep:
        source = work / name
        if source.is_file():
            shutil.copy2(source, evidence / name)
    large = ["problem.cnf", "proof.drat", "core.cnf", "proof.lrat"]
    retention = {
        "schema": "d972-b4-sat-retention/v1",
        "status": status,
        "drat_independent_check": receipt.get("proof_verified") is True,
        "deleted_after_verified_drat": file_manifest(work, large),
    }
    json_write(evidence / "retention.json", retention)
    for name in large:
        path = work / name
        if path.is_file():
            path.unlink()
    return {"mode": "light_after_verified_drat",
            "path": str(evidence.relative_to(ROOT)),
            "deleted": retention["deleted_after_verified_drat"]}


def run_batch(degree: int, shard_start: int, shard_end: int,
              max_word_length: int, output_root: Path = OUTPUT_ROOT) -> dict[str, Any]:
    rows, plan = validate_inputs(degree, shard_start, shard_end, max_word_length)
    output_root = output_root.resolve()
    expected_root = (ROOT / "ci" / "out").resolve()
    try:
        output_root.relative_to(expected_root)
    except ValueError as exc:
        raise ValueError("batch output must stay below ci/out") from exc
    output_root.mkdir(parents=True, exist_ok=True)
    batch_id = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime()) + f"_{os.getpid()}"
    batch_dir = output_root / f"batch_{batch_id}"
    batch_dir.mkdir()
    source_paths = [RELATORS, WORD_KEY_ARTIFACT, WRAPPER, Path(__file__).resolve(), RUNNER, ENCODER,
                    MODEL_CHECKER, OR_CHECKER, PLANNER, MATRIX]
    source_sha256 = {str(path.relative_to(ROOT)): sha_file(path)
                     for path in source_paths}
    summaries: list[dict[str, Any]] = []
    with tempfile.TemporaryDirectory(prefix="d972-b4-sat-batch-") as temp_name:
        temp_root = Path(temp_name)
        solvers = build_solvers(temp_root / "solvers")
        for shard in range(shard_start, shard_end + 1):
            work = temp_root / f"shard_{shard:04d}"
            work.mkdir()
            command = [sys.executable, "-B", str(RUNNER),
                       "--degree", str(degree), "--shard", str(shard),
                       "--shard-size", str(SHARD_SIZE),
                       "--max-word-length", str(max_word_length),
                       "--relators", str(RELATORS),
                       "--word-key-artifact", str(WORD_KEY_ARTIFACT),
                       "--solver", str(solvers.kissat),
                       "--drat-trim", str(solvers.drat_trim),
                       "--output-dir", str(work)]
            proc = subprocess.run(command, cwd=ROOT, text=True,
                                  capture_output=True, encoding="utf-8",
                                  errors="replace", check=False)
            (work / "batch_runner.stdout.txt").write_text(
                proc.stdout, encoding="utf-8")
            (work / "batch_runner.stderr.txt").write_text(
                proc.stderr, encoding="utf-8")
            receipt_path = work / "run_receipt.json"
            if receipt_path.is_file():
                receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
            else:
                receipt = {"status": "UNKNOWN_BATCH_RUNNER_FAILURE",
                           "solver_exit_code": None}
            status = str(receipt.get("status", "UNKNOWN_BATCH_RUNNER_FAILURE"))
            evidence = batch_dir / f"shard_{shard:04d}_evidence"
            retention = preserve_evidence(work, evidence, status)
            summary = {
                "schema": "d972-b4-sat-shard-summary/v1",
                "degree": degree, "shard": shard,
                "shard_size": SHARD_SIZE,
                "max_word_length": max_word_length,
                "target_indices": receipt.get("target_indices",
                                               plan["shards"][shard]["row_indices"]),
                "status": status,
                "runner_returncode": proc.returncode,
                "solver_exit_code": receipt.get("solver_exit_code"),
                "proof_verified": receipt.get("proof_verified", False),
                "cnf_sha256": receipt.get("cnf_sha256"),
                "nvars": receipt.get("nvars"), "clauses": receipt.get("clauses"),
                "evidence": retention,
            }
            json_write(batch_dir / f"shard_{shard:04d}.summary.json", summary)
            summaries.append(summary)

    candidate = any(x["status"] == "B4-A_CANDIDATE_FINITE_SAT_OR"
                    for x in summaries)
    hard_failure = any(
        x["status"] in {"REJECTED_SAT_MODEL", "UNKNOWN_SOLVER",
                         "UNKNOWN_BATCH_RUNNER_FAILURE"} or
        int(x["runner_returncode"] or 0) not in {0}
        for x in summaries)
    if candidate:
        status = "B4-A_CANDIDATE_FINITE_SAT_OR"
    elif hard_failure:
        status = "UNKNOWN_BATCH_ERROR"
    else:
        status = "UNKNOWN_FINITE_SHARD_RANGE"
    receipt = {
        "schema": SCHEMA,
        "status": status,
        "bounded_status": "FINITE_CANDIDATE_ONLY",
        "degree": degree, "shard_start": shard_start,
        "shard_end": shard_end, "shard_size": SHARD_SIZE,
        "max_word_length": max_word_length,
        "unique_word_count": plan["unique_word_count"],
        "total_nonempty_unique_word_count": plan["total_nonempty_unique_word_count"],
        "empty_rows_excluded": plan["empty_rows_excluded"],
        "duplicate_copies_excluded": plan["duplicate_copies_excluded"],
        "p2_input_schema": P2_INPUT_SCHEMA,
        "p2_input_file_sha256": P2_INPUT_SHA256,
        "rho_words_source": RHO_WORDS_SOURCE,
        "rho_words_sha256": RHO_WORDS_SHA256,
        "kissat_commit": KISSAT_COMMIT,
        "drat_trim_commit": DRAT_TRIM_COMMIT,
        "kissat_sha256": solvers.kissat_sha256,
        "drat_trim_sha256": solvers.drat_trim_sha256,
        "source_sha256": source_sha256,
        "shards": summaries,
        "interpretation": (
            "SAT plus the independent OR receipt is a B4-A candidate. "
            "Every UNSAT result is finite-degree/shard UNKNOWN and never B."
        ),
    }
    json_write(batch_dir / "batch_receipt.json", receipt)
    json_write(output_root / "latest_summary.json", receipt)
    marker = (f"D972_B4_SAT_BATCH_FINAL_MARKER status={status} "
              f"degree={degree} shards={shard_start}-{shard_end}\n")
    (output_root / "final.marker").write_text(marker, encoding="ascii")
    print(json.dumps({"status": status, "batch_receipt": str(batch_dir / "batch_receipt.json"),
                      "shards": len(summaries)}, sort_keys=True))
    return receipt


def self_test() -> None:
    require(SHARD_SIZE == 8, "shard-size pin drift")
    require(P2_INPUT_SCHEMA.endswith("/v2"), "v2 input schema pin drift")
    require(len(KISSAT_COMMIT) == 40 and len(DRAT_TRIM_COMMIT) == 40,
            "solver commit pin length")
    require(Path(__file__).resolve().parent == SAT_DIR,
            "launcher path/root drift")
    require(ROOT == Path(__file__).resolve().parents[2], "repository root drift")
    rows, plan = validate_inputs(2, 0, 0, 40)
    require(len(rows) == 972 and plan["unique_word_count"] == 237,
            "bounded v2 planner selftest drift")
    require(plan["shards"][0]["word_count"] == 8,
            "first shard size drift")
    print("D972_B4_SAT_BATCH_SELFTEST_PASS")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--degree", type=int)
    ap.add_argument("--shard-start", type=int)
    ap.add_argument("--shard-end", type=int)
    ap.add_argument("--max-word-length", type=int)
    args = ap.parse_args()
    if args.self_test:
        self_test()
        return 0
    required = (args.degree, args.shard_start, args.shard_end,
                args.max_word_length)
    if any(x is None for x in required):
        ap.error("--degree, --shard-start, --shard-end, and --max-word-length are required")
    assert args.degree is not None and args.shard_start is not None
    assert args.shard_end is not None and args.max_word_length is not None
    try:
        run_source_selftests()
        receipt = run_batch(args.degree, args.shard_start, args.shard_end,
                            args.max_word_length)
    except Exception as exc:  # fail closed; wrapper sees no acceptable marker
        print(f"D972_B4_SAT_BATCH_FATAL: {exc}", file=sys.stderr)
        return 2
    if receipt["status"] == "UNKNOWN_BATCH_ERROR":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
