#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
delta_table_gen.py -- CV-12 machine-generation script for the delta(n) lookup table.

Definition (docs/notes/tmax_budget_and_holes_v1.md sec.1.2, Sol reply 95 W95-4.1):
    delta(n) = (n mod 4)/2 + (2/3)*(n mod 3)
    6*delta(n) = 3*(n mod 4) + 4*(n mod 3)

delta(n) depends only on n mod 12. This script:
  1. Computes 6*delta(n) for n mod 12 = 0..11 directly from the definition.
  2. Cross-checks against Sol's corrected reference row (sol_reply_95_math22.md
     W95-4.1): [0,7,14,9,4,11,6,13,8,3,10,17]. Exits 1 on mismatch (fail-closed).
  3. Numerically checks, for n = 1..1000, the identity
         2*floor(n/4) + 2*floor(n/3) == (7/6)*n - delta(n)
     (as an exact fraction comparison, no float rounding).
  4. Emits a markdown table and a JSON cert with script/definition digests.

Usage:
    python delta_table_gen.py [--out-json PATH] [--out-md PATH]

Exit codes:
    0 = all self-checks passed, files written
    1 = self-check or identity check failed (fail-closed)
"""

import argparse
import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path

# Reference row from Sol reply 95, W95-4.1 (n mod 12 = 0..11)
SOL_REFERENCE_6DELTA = [0, 7, 14, 9, 4, 11, 6, 13, 8, 3, 10, 17]

DEFINITION_TEXT = (
    "delta(n) = (n mod 4)/2 + (2/3)*(n mod 3); "
    "6*delta(n) = 3*(n mod 4) + 4*(n mod 3)"
)


def delta_frac(n: int) -> Fraction:
    """Exact delta(n) as a Fraction, from the definition."""
    return Fraction(n % 4, 1) / 2 + Fraction(2, 3) * (n % 3)


def six_delta_int(n: int) -> int:
    """6*delta(n), guaranteed integer by the closed form 3*(n mod 4) + 4*(n mod 3)."""
    val = 3 * (n % 4) + 4 * (n % 3)
    # cross-check against the fractional definition scaled by 6
    frac_val = delta_frac(n) * 6
    assert frac_val == val, f"internal mismatch at n={n}: {frac_val} != {val}"
    return val


def build_table():
    """Return dict: n mod 12 -> 6*delta(n) for representative n = residue (0..11)."""
    table = {}
    for r in range(12):
        table[r] = six_delta_int(r)
    return table


def self_check(table):
    """Compare generated table against Sol's reference row. Return list of mismatches."""
    mismatches = []
    for r in range(12):
        generated = table[r]
        expected = SOL_REFERENCE_6DELTA[r]
        if generated != expected:
            mismatches.append((r, generated, expected))
    return mismatches


def identity_check(n_max: int = 1000):
    """
    Check 2*floor(n/4) + 2*floor(n/3) == (7/6)*n - delta(n) exactly, for n = 1..n_max.
    Returns list of failing n (empty if all pass).
    """
    failures = []
    for n in range(1, n_max + 1):
        lhs = Fraction(2 * (n // 4) + 2 * (n // 3))
        rhs = Fraction(7, 6) * n - delta_frac(n)
        if lhs != rhs:
            failures.append(n)
    return failures


def identity_check_6delta(n_max: int = 1000):
    """
    Check 6*delta(n) == 3*(n mod 4) + 4*(n mod 3) exactly, for n = 1..n_max
    (definition-vs-closed-form identity referenced in W95-4.1).
    Returns list of failing n (empty if all pass).
    """
    failures = []
    for n in range(1, n_max + 1):
        lhs = delta_frac(n) * 6
        rhs = Fraction(3 * (n % 4) + 4 * (n % 3))
        if lhs != rhs:
            failures.append(n)
    return failures


def sha256_of_file(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def sha256_of_text(text: str) -> str:
    h = hashlib.sha256()
    h.update(text.encode("utf-8"))
    return h.hexdigest()


def render_markdown(table) -> str:
    header = "| $n\\bmod12$ | " + " | ".join(str(r) for r in range(12)) + " |"
    sep = "|---|" + "---:|" * 12
    row = "| $6\\delta$ | " + " | ".join(f"**{table[r]}**" for r in range(12)) + " |"
    return "\n".join([header, sep, row])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--out-json",
        default=str(
            Path(__file__).resolve().parents[3]
            / "search"
            / "certs"
            / "delta_table_20260801.json"
        ),
    )
    ap.add_argument("--out-md", default="")
    args = ap.parse_args()

    table = build_table()
    mismatches = self_check(table)
    id1_failures = identity_check(1000)
    id2_failures = identity_check_6delta(1000)

    ok = (not mismatches) and (not id1_failures) and (not id2_failures)

    script_path = Path(__file__).resolve()
    script_digest = sha256_of_file(script_path)
    definition_digest = sha256_of_text(DEFINITION_TEXT)

    md_table = render_markdown(table)

    cert = {
        "schema": "delta_table_cert/v1",
        "convention": "CV-12",
        "generated_by": "search/probe/wac_v1/delta_table_gen.py",
        "script_sha256": script_digest,
        "definition_text": DEFINITION_TEXT,
        "definition_sha256": definition_digest,
        "table_n_mod_12_to_6delta": {str(r): table[r] for r in range(12)},
        "table_as_list_r0_to_r11": [table[r] for r in range(12)],
        "sol_reference_6delta": SOL_REFERENCE_6DELTA,
        "self_check": {
            "mismatches": mismatches,
            "passed": not mismatches,
        },
        "identity_check_floor_form": {
            "description": "2*floor(n/4)+2*floor(n/3) == (7/6)*n - delta(n), n=1..1000",
            "n_max": 1000,
            "failures": id1_failures,
            "passed": not id1_failures,
        },
        "identity_check_6delta_closed_form": {
            "description": "6*delta(n) == 3*(n mod 4) + 4*(n mod 3), n=1..1000",
            "n_max": 1000,
            "failures": id2_failures,
            "passed": not id2_failures,
        },
        "markdown_table": md_table,
        "overall_pass": ok,
    }

    out_json = Path(args.out_json)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(cert, indent=2, ensure_ascii=False), encoding="utf-8")

    if args.out_md:
        Path(args.out_md).write_text(md_table + "\n", encoding="utf-8")

    print("=== delta_table_gen.py ===")
    print(f"script sha256:     {script_digest}")
    print(f"definition sha256: {definition_digest}")
    print("generated table (n mod 12 -> 6*delta(n)):")
    print(md_table)
    print(f"self_check mismatches: {mismatches}")
    print(f"identity_check_floor_form failures: {len(id1_failures)}")
    print(f"identity_check_6delta_closed_form failures: {len(id2_failures)}")
    print(f"overall_pass: {ok}")
    print(f"wrote: {out_json}")

    if not ok:
        print("FAIL-CLOSED: self-check or identity check failed.", file=sys.stderr)
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
