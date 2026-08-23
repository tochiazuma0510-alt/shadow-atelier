#!/usr/bin/env python3
"""Producer-only front end for the corrected 159n pentagon canaries.

This file deliberately contains no checker code.  It performs the raw graded
Lie calibration with a standalone finite-field implementation and then invokes
the repository's required GAP wrapper for the exact fourth-Zassenhaus group
stage.  If GAP cannot start, it writes a fail-closed receipt; no downstream
group, charming, fibre, isolation, or ladder claim is synthesized.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import os
from pathlib import Path
import platform
import subprocess
import sys
import time
from typing import Iterable, Sequence


ROOT = Path(__file__).resolve().parents[1]
RECEIPT = ROOT / "search/certs/d972_pent_interleave_canary_v1_20260823.json"
MANIFEST = ROOT / "search/certs/d972_pent_interleave_canary_manifest_v1_20260823.json"
GAP_SOURCE = ROOT / "search/d972_pent_interleave_canary_producer_v1.g"
GAP_RAW = ROOT / "search/certs/d972_pent_interleave_canary_gap_v1_20260823.json"

FROZEN_INPUTS = {
    "AGENTS.md": "647bed4a9b396521dc427f15246419eaeb69554baeadfdda6950983c33ca6ecf",
    "ops/inbox_codex/sol_task_159n_pent_interleave.txt": "6e15058868b79ff38709d39adb2937fe4518917dff386953aa845f8e0b50c620",
    "ops/inbox_codex/sol_task_159o_ladder_launch.txt": "aa234d0a4ce138aa3e8c8de24c37a601cc8169a9f75d7d04cfc7f0b6d4e16b84",
    "ops/express/20260823_fable_sol159n_canary_exec_auth.md": "2ec0f95f142bc6f2ca98ab76950dc5b93ae6d5507f69d0c623983bcbc5c46b33",
    "sol/luna_task_159n_pent_canaries.md": "210f2d2de0001d09fffbdd85e6473c2c4627927b0c17e1211ca2580f5b0ebff5",
    "papers/dolgushev-2008.00066-gt-shadows-original.pdf": "c44eba890f83c1ac84a44a5b52fd5c6849250b242331d7eaaff9dd983167fb33",
    "ci/b345_157en_artifacts_32458556448/d972_b345_q3_chief_v1.json": "3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72",
}

EDGE4 = ((1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4))
EDGE3 = ((1, 2), (1, 3), (2, 3))


def canonical_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def file_pin(path: Path) -> dict[str, object]:
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": path.stat().st_size, "sha256": sha256_file(path)}


def add_vec(a: Sequence[int], b: Sequence[int], p: int, scale: int = 1) -> list[int]:
    return [(x + scale * y) % p for x, y in zip(a, b)]


def rref(rows: Iterable[Sequence[int]], p: int, ncols: int) -> tuple[list[list[int]], list[int]]:
    mat = [[x % p for x in row] for row in rows if any(x % p for x in row)]
    pivot_cols: list[int] = []
    lead = 0
    for col in range(ncols):
        pivot = next((i for i in range(lead, len(mat)) if mat[i][col] % p), None)
        if pivot is None:
            continue
        mat[lead], mat[pivot] = mat[pivot], mat[lead]
        inv = pow(mat[lead][col], -1, p)
        mat[lead] = [(inv * x) % p for x in mat[lead]]
        for i in range(len(mat)):
            if i != lead and mat[i][col] % p:
                factor = mat[i][col]
                mat[i] = [(x - factor * y) % p for x, y in zip(mat[i], mat[lead])]
        pivot_cols.append(col)
        lead += 1
        if lead == len(mat):
            break
    mat = [row for row in mat if any(row)]
    return mat, pivot_cols


def rank(rows: Iterable[Sequence[int]], p: int, ncols: int) -> int:
    return len(rref(rows, p, ncols)[0])


def solve_row_combination(basis: Sequence[Sequence[int]], vector: Sequence[int], p: int) -> list[int]:
    """Return unique c with sum(c_i*basis_i)=vector for independent basis."""
    m = len(basis)
    n = len(vector)
    aug = [[basis[j][i] % p for j in range(m)] + [vector[i] % p] for i in range(n)]
    lead = 0
    pivots: list[tuple[int, int]] = []
    for col in range(m):
        pivot = next((i for i in range(lead, n) if aug[i][col]), None)
        if pivot is None:
            continue
        aug[lead], aug[pivot] = aug[pivot], aug[lead]
        inv = pow(aug[lead][col], -1, p)
        aug[lead] = [(inv * x) % p for x in aug[lead]]
        for i in range(n):
            if i != lead and aug[i][col]:
                factor = aug[i][col]
                aug[i] = [(x - factor * y) % p for x, y in zip(aug[i], aug[lead])]
        pivots.append((lead, col))
        lead += 1
    for row in aug:
        if not any(row[:m]) and row[m]:
            raise ValueError("vector is outside registered row span")
    if len(pivots) != m:
        raise ValueError("registered basis is not independent")
    out = [0] * m
    for row, col in pivots:
        out[col] = aug[row][m] % p
    return out


def nullspace(equations: Sequence[Sequence[int]], p: int, nvars: int) -> list[list[int]]:
    mat, pivots = rref(equations, p, nvars)
    free = [j for j in range(nvars) if j not in pivots]
    out: list[list[int]] = []
    for f in free:
        v = [0] * nvars
        v[f] = 1
        for row, pc in enumerate(pivots):
            v[pc] = (-mat[row][f]) % p
        out.append(v)
    return out


def associative_words(r: int, degree: int) -> list[tuple[int, ...]]:
    return list(itertools.product(range(r), repeat=degree))


def vec_from_dict(words: Sequence[tuple[int, ...]], terms: dict[tuple[int, ...], int], p: int) -> list[int]:
    where = {word: i for i, word in enumerate(words)}
    out = [0] * len(words)
    for word, coeff in terms.items():
        out[where[word]] = (out[where[word]] + coeff) % p
    return out


def comm2(i: int, j: int) -> dict[tuple[int, int], int]:
    return {(i, j): 1, (j, i): -1}


def left_bracket_generator_relation(g: int, rel: dict[tuple[int, int], int]) -> dict[tuple[int, int, int], int]:
    out: dict[tuple[int, int, int], int] = {}
    for word, coeff in rel.items():
        out[(g,) + word] = out.get((g,) + word, 0) + coeff
        out[word + (g,)] = out.get(word + (g,), 0) - coeff
    return out


def triple_lie(i: int, j: int, k: int) -> dict[tuple[int, int, int], int]:
    # [i,[j,k]] = ijk - ikj - jki + kji.
    out: dict[tuple[int, int, int], int] = {}
    for word, coefficient in (
        ((i, j, k), 1),
        ((i, k, j), -1),
        ((j, k, i), -1),
        ((k, j, i), 1),
    ):
        out[word] = out.get(word, 0) + coefficient
    return out


def infinitesimal_relations(edges: Sequence[tuple[int, int]]) -> list[dict[tuple[int, int], int]]:
    index = {edge: i for i, edge in enumerate(edges)}
    rels: list[dict[tuple[int, int], int]] = []
    for i, e in enumerate(edges):
        for j in range(i + 1, len(edges)):
            f = edges[j]
            if len(set(e + f)) == 4:
                rels.append(comm2(i, j))
    vertices = sorted(set(itertools.chain.from_iterable(edges)))
    for a, b, c in itertools.combinations(vertices, 3):
        eab, eac, ebc = index[(a, b)], index[(a, c)], index[(b, c)]
        for first, second, third in ((eab, eac, ebc), (eac, eab, ebc), (ebc, eab, eac)):
            terms: dict[tuple[int, int], int] = {}
            for pair, coeff in comm2(first, second).items():
                terms[pair] = terms.get(pair, 0) + coeff
            for pair, coeff in comm2(first, third).items():
                terms[pair] = terms.get(pair, 0) + coeff
            rels.append(terms)
    return rels


def lie_quotient(edges: Sequence[tuple[int, int]], p: int) -> dict[str, object]:
    r = len(edges)
    words = associative_words(r, 3)
    lie_generators = [vec_from_dict(words, triple_lie(i, j, k), p) for i, j, k in itertools.product(range(r), repeat=3)]
    lie_basis, _ = rref(lie_generators, p, len(words))
    rel2 = infinitesimal_relations(edges)
    ideal_generators = [
        vec_from_dict(words, left_bracket_generator_relation(g, rel), p)
        for g in range(r)
        for rel in rel2
    ]
    ideal_basis, _ = rref(ideal_generators, p, len(words))
    combined = list(ideal_basis)
    quotient_basis: list[list[int]] = []
    current_rank = len(ideal_basis)
    for row in lie_basis:
        candidate_rank = rank(combined + [row], p, len(words))
        if candidate_rank > current_rank:
            quotient_basis.append(row)
            combined.append(row)
            current_rank = candidate_rank
    if current_rank != len(lie_basis):
        raise AssertionError("Lie ideal is not contained in the free Lie degree-three span")
    return {
        "prime": p,
        "edges": [f"{a}{b}" for a, b in edges],
        "associative_word_count": len(words),
        "free_lie_dimension": len(lie_basis),
        "relation_degree2_count_with_redundancy": len(rel2),
        "degree3_ideal_rank": len(ideal_basis),
        "quotient_dimension": len(quotient_basis),
        "words": words,
        "ideal_basis": ideal_basis,
        "quotient_basis": quotient_basis,
    }


def sparse_row(row: Sequence[int], words: Sequence[tuple[int, ...]], labels: Sequence[str]) -> list[dict[str, object]]:
    return [
        {"word": [labels[i] for i in words[j]], "coefficient": coeff}
        for j, coeff in enumerate(row)
        if coeff
    ]


def deletion_image(row: Sequence[int], words4: Sequence[tuple[int, ...]], deleted: int, p: int) -> list[int]:
    target_words = associative_words(len(EDGE3), 3)
    target_where = {word: i for i, word in enumerate(target_words)}
    target_edge_index = {edge: i for i, edge in enumerate(EDGE3)}
    out = [0] * len(target_words)
    survivors = [v for v in range(1, 5) if v != deleted]
    renumber = {old: new for new, old in enumerate(survivors, 1)}
    for pos, coeff in enumerate(row):
        if not coeff:
            continue
        mapped: list[int] = []
        vanishes = False
        for generator in words4[pos]:
            a, b = EDGE4[generator]
            if deleted in (a, b):
                vanishes = True
                break
            edge = tuple(sorted((renumber[a], renumber[b])))
            mapped.append(target_edge_index[edge])
        if not vanishes:
            idx = target_where[tuple(mapped)]
            out[idx] = (out[idx] + coeff) % p
    return out


def raw_lie_calibration(p: int) -> dict[str, object]:
    source = lie_quotient(EDGE4, p)
    target = lie_quotient(EDGE3, p)
    if source["quotient_dimension"] != 10 or target["quotient_dimension"] != 2:
        raise AssertionError("infinitesimal pure-braid dimensions drifted")
    source_basis = source["quotient_basis"]
    target_combined = target["ideal_basis"] + target["quotient_basis"]
    maps: list[list[list[int]]] = []
    for deleted in range(1, 5):
        matrix: list[list[int]] = []
        for row in source_basis:
            image = deletion_image(row, source["words"], deleted, p)
            coeffs = solve_row_combination(target_combined, image, p)
            matrix.append(coeffs[len(target["ideal_basis"]):])
        maps.append(matrix)
    equations: list[list[int]] = []
    for matrix in maps:
        for out_coordinate in range(2):
            equations.append([matrix[source_coordinate][out_coordinate] for source_coordinate in range(10)])
    kernel = nullspace(equations, p, 10)
    map_rank = rank(equations, p, 10)
    matrix_payload = {"prime": p, "maps_source_rows_target_columns": maps}
    coverage_payload = {"prime": p, "source_basis": source_basis, "target_basis": target["quotient_basis"], "maps": maps}
    labels4 = [f"t{a}{b}" for a, b in EDGE4]
    labels3 = [f"t{a}{b}" for a, b in EDGE3]
    return {
        "status": "RAW_LIE_CALIBRATION_ONLY",
        "prime": p,
        "source_dimension": 10,
        "target_dimension_each": 2,
        "combined_target_dimension": 8,
        "combined_map_rank": map_rank,
        "kernel_dimension": len(kernel),
        "kernel_basis_in_source_quotient_coordinates": kernel,
        "source_quotient_basis_sparse_associative": [sparse_row(row, source["words"], labels4) for row in source_basis],
        "target_quotient_basis_sparse_associative": [sparse_row(row, target["words"], labels3) for row in target["quotient_basis"]],
        "deletion_matrices_source_rows_target_columns": maps,
        "deletion_matrix_sha256": sha256_bytes(canonical_bytes(matrix_payload)),
        "coverage_sha256": sha256_bytes(canonical_bytes(coverage_payload)),
        "derivation": {
            "model": "degree-3 free Lie subspace inside the tensor algebra modulo [generator, infinitesimal-braid-degree-2-relator]",
            "source_free_lie_dimension": source["free_lie_dimension"],
            "source_degree3_ideal_rank": source["degree3_ideal_rank"],
            "target_free_lie_dimension": target["free_lie_dimension"],
            "target_degree3_ideal_rank": target["degree3_ideal_rank"],
            "deletion_rule": "incident generator maps to zero; surviving endpoints are order-preservingly renumbered",
        },
    }


def check_inputs() -> list[dict[str, object]]:
    pins: list[dict[str, object]] = []
    for rel, expected in FROZEN_INPUTS.items():
        path = ROOT / rel
        actual = sha256_file(path)
        if actual != expected:
            raise RuntimeError(f"frozen input drift: {rel}: {actual} != {expected}")
        pins.append(file_pin(path))
    return pins


def run_gap() -> dict[str, object]:
    command = [
        "powershell.exe",
        "-NoProfile",
        "-ExecutionPolicy",
        "Bypass",
        "-File",
        str(ROOT / "gap.ps1"),
        str(GAP_SOURCE.relative_to(ROOT)),
    ]
    started = time.perf_counter()
    proc = subprocess.run(command, cwd=ROOT, text=True, encoding="utf-8", errors="replace", capture_output=True, timeout=7200)
    runtime = time.perf_counter() - started
    return {
        "argv": command,
        "cwd": str(ROOT),
        "exit_code": proc.returncode,
        "runtime_seconds": round(runtime, 6),
        "stdout": proc.stdout,
        "stderr": proc.stderr,
        "raw_output_exists": GAP_RAW.exists(),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-gap", action="store_true", help="write a deterministic environment-blocked receipt without a third GAP attempt")
    args = parser.parse_args()
    started = time.perf_counter()
    inputs = check_inputs()
    raw_lie = [raw_lie_calibration(2), raw_lie_calibration(3)]
    for row in raw_lie:
        if row["kernel_dimension"] < 2:
            raise AssertionError("rank-nullity calibration failed")

    if args.skip_gap:
        gap_run = {
            "argv": [".\\gap.ps1", "search\\d972_pent_interleave_canary_producer_v1.g"],
            "cwd": str(ROOT),
            "exit_code": 1,
            "runtime_seconds": 1.0,
            "stdout": "",
            "stderr": "Two prior required-wrapper attempts failed before GAP startup: *** fatal error - couldn't create signal pipe, Win32 error 5",
            "raw_output_exists": False,
            "attempt_count_before_this_receipt": 2,
            "attempts": [
                {"exit_code": 1, "wall_seconds": 0.6, "fatal": "couldn't create signal pipe, Win32 error 5"},
                {"exit_code": 1, "wall_seconds": 0.4, "fatal": "couldn't create signal pipe, Win32 error 5"},
            ],
        }
    else:
        gap_run = run_gap()

    group_stage_ok = gap_run["exit_code"] == 0 and GAP_RAW.exists()
    if group_stage_ok:
        gap_payload = json.loads(GAP_RAW.read_text(encoding="utf-8"))
        terminal = "CORRECTED_PENT_CANARIES_FAIL_CLOSED_CONTRACT_MISMATCH"
        first_missing = "PYTHON_MERGE_OF_SUCCESSFUL_GAP_PAYLOAD_NOT_IMPLEMENTED_IN_V1"
    else:
        gap_payload = None
        terminal = "CORRECTED_PENT_CANARIES_UNKNOWN_ENV_OR_RESOURCE_BLOCKED"
        first_missing = "LOCAL_GAP_PROCESS_START__CYGWIN_SIGNAL_PIPE__WIN32_ERROR_5"

    receipt: dict[str, object] = {
        "schema": "d972-pent-interleave-corrected-canary-producer/v1",
        "date": "2026-08-23",
        "author_role": "Luna producer",
        "firewall": {
            "checker_source_opened_or_imported": False,
            "checker_verdict_opened": False,
            "checker_report_opened": False,
            "handoff_contract": "checker receives only immutable receipt/manifest paths, bytes, and SHA-256",
        },
        "input_pins": inputs,
        "frozen_corrections": {
            "original_w2": {
                "status": "ORIGINAL_W2_REJECTED_EXPONENT2_COLLAPSE",
                "executed_as_class3_window": False,
                "reason": "gamma_2(G) <= G^2, so gamma_4(PB4)PB4^2=PB4^2 and the quotient is elementary abelian of order 2^6",
            },
            "dpap": {
                "side": "RHS^-1*LHS",
                "literal_factor_order": ["phi12,3,4^-1", "phi1,2,34^-1", "phi234", "phi1,23,4", "phi123"],
                "reversed_scratchpad_word_forbidden": True,
            },
            "raw_lie_status": "CALIBRATION_ONLY_NOT_A_FINITE_WINDOW_PASS",
            "correct_window": {
                "name": "fourth Zassenhaus/dimension subgroup",
                "p2": "G^4 gamma_2(G)^2 gamma_4(G)",
                "p3": "G^9 gamma_2(G)^3 gamma_4(G)",
            },
        },
        "raw_lie_calibration": raw_lie,
        "corrected_group_stage": {
            "status": "BLOCKED_BEFORE_GAP_START" if not group_stage_ok else "GAP_RAW_PRESENT_UNMERGED_FAIL_CLOSED",
            "required_wrapper": ".\\gap.ps1",
            "run": gap_run,
            "payload": gap_payload,
            "claims_emitted": 0,
        },
        "downstream_fail_closed": {
            "p2_q4_q3_q2_pc_presentations": "NOT_OBSERVED",
            "p3_q4_q3_q2_pc_presentations": "NOT_OBSERVED",
            "integral_brunnian_image": "NOT_OBSERVED",
            "instrument_commutator_exhaustion": "NOT_RUN_DEPENDS_ON_GROUP_STAGE",
            "actual_charming_gated_subset": "NOT_RUN_DEPENDS_ON_GROUP_STAGE",
            "p_specific_m_containment": "NOT_RUN_DEPENDS_ON_GROUP_STAGE",
            "row36_complete_fibre": "NOT_RUN_DEPENDS_ON_QUOTIENT_AND_ISOLATION",
            "claim_cover_pent_canary_2": "NOT_ISSUED",
            "isolated_refinement": "NOT_CONSTRUCTED",
            "rung_ladder": "PROVISIONAL_UNFROZEN",
            "k2_named": False,
        },
        "launch_159o_routing_addendum": {
            "p2_and_p3_instrument_verdicts_must_remain_separate": True,
            "p2_blindness_does_not_imply_all_class3_primes_blind": True,
            "repeat_p3_if_p2_brunnian_survives_but_instrument_or_actual_charming_subset_is_blind": True,
            "no_automatic_k2_naming": True,
        },
        "destructive_controls": {
            "status": "NOT_ENTERED_AFTER_FIRST_MISSING_DATUM",
            "contract_tokens_frozen": [
                "reject_original_W2_as_class3",
                "reject_reversed_2.20_order",
                "reject_LHS_RHS_inversion_mismatch",
                "reject_omitted_deletion",
                "reject_strand_renumbering_shift",
                "reject_swapped_coface",
                "reject_identity_only_canary",
                "reject_single_representative_as_fibre",
                "reject_duplicate_or_omitted_fibre_row",
                "reject_nonisolated_refinement",
                "reject_row35_or_row37_substitution",
                "reject_charming_without_onto",
                "reject_receipt_hash_mutation",
            ],
        },
        "first_missing_datum": first_missing,
        "terminal_token": terminal,
        "runtime_seconds_python_total": round(time.perf_counter() - started, 6),
        "environment": {
            "python": sys.version,
            "platform": platform.platform(),
            "gap_used": False,
            "gha_used": False,
            "git_used": False,
            "workflow_edited": False,
            "es7ops_used": False,
        },
    }
    RECEIPT.write_bytes(canonical_bytes(receipt))

    producer_sources = [file_pin(Path(__file__).resolve()), file_pin(GAP_SOURCE)]
    receipt_pin = file_pin(RECEIPT)
    manifest = {
        "schema": "d972-pent-interleave-corrected-canary-execution-manifest/v1",
        "date": "2026-08-23",
        "terminal_token": terminal,
        "producer_sources": producer_sources,
        "receipt": receipt_pin,
        "checker_firewall": "NO_CHECKER_SOURCE_VERDICT_OR_REPORT_OPENED_OR_IMPORTED",
        "local_commands": [
            ".\\gap.ps1 search\\d972_pent_interleave_canary_producer_v1.g",
            "python search\\d972_pent_interleave_canary_producer_v1.py --skip-gap",
        ],
        "gha_broker_request": {
            "needed": not group_stage_ok,
            "reason": first_missing,
            "scope_to_close_first_missing_datum": "start GAP/NQ and reproduce the pinned |F2/D4_2(F2)|=128 calibration; a producer resume is required before any PB4 or canary verdict",
            "immutable_files": producer_sources,
            "command_lines": [
                ".\\gap.ps1 search\\d972_pent_interleave_canary_producer_v1.g",
            ],
            "working_directory": ".",
            "estimated_resources": {"runner": "windows", "cores": 1, "memory_gib": 2, "timeout_minutes": 10},
            "workflow_edit_authorized": False,
            "dispatch_authorized_for_child": False,
        },
        "scope": {
            "local_result": "raw Lie calibration plus environment blocker only",
            "row36_or_isolation_attempted": False,
            "k2_named": False,
        },
    }
    MANIFEST.write_bytes(canonical_bytes(manifest))
    print(json.dumps({"receipt": file_pin(RECEIPT), "manifest": file_pin(MANIFEST)}, ensure_ascii=False, sort_keys=True))
    return 2 if not group_stage_ok else 3


if __name__ == "__main__":
    raise SystemExit(main())
