#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
delta_table_check.py -- CV-12 build-time checker for the delta(n) lookup table
embedded in docs/notes/tmax_budget_and_holes_v1.md.

Parses the "correct table" markdown block in the note (the one introduced by
the erratum in W95-4.1 / delta_table_gen.py), extracts the twelve 6*delta(n)
values, and re-derives them independently from the algebraic definition
(without importing delta_table_gen.py, so this is a genuine re-check, not a
re-display of the same computation).

Fail-closed: any parse failure or numeric mismatch -> exit 1.

Usage:
    python delta_table_check.py [NOTE_PATH]
"""

import re
import sys
from fractions import Fraction
from pathlib import Path

DEFAULT_NOTE = (
    Path(__file__).resolve().parents[3]
    / "docs"
    / "notes"
    / "tmax_budget_and_holes_v1.md"
)

# Marker text that precedes the corrected table (must appear right before it,
# so the erratum's now-struck-through OLD table is never picked up instead).
CORRECT_TABLE_MARKER = "正しい表(機械生成"


def delta_frac(n: int) -> Fraction:
    return Fraction(n % 4, 1) / 2 + Fraction(2, 3) * (n % 3)


def six_delta_int(n: int) -> int:
    val = 3 * (n % 4) + 4 * (n % 3)
    assert delta_frac(n) * 6 == val
    return val


def independent_reference_table():
    """Recompute 6*delta(n) for n mod 12 = 0..11 directly from the definition."""
    return [six_delta_int(r) for r in range(12)]


def extract_table_after_marker(text: str, marker: str):
    r"""
    Find `marker`, then the next markdown table's data row (the row that
    starts with a $6\delta$-style label), and return the 12 integer cells.
    """
    idx = text.find(marker)
    if idx == -1:
        raise ValueError(f"marker not found in note: {marker!r}")
    tail = text[idx:]

    # Find markdown table lines after the marker: a header row, a separator
    # row (---), then the data row we want.
    lines = tail.splitlines()
    table_lines = [ln for ln in lines if ln.strip().startswith("|")]
    if len(table_lines) < 3:
        raise ValueError("expected at least 3 table lines (header/sep/data) after marker")

    header, sep, data = table_lines[0], table_lines[1], table_lines[2]
    if not re.match(r"^\|[\s:\-|]+\|$", sep.strip()):
        raise ValueError(f"second table line does not look like a markdown separator: {sep!r}")

    cells = [c.strip() for c in data.strip().strip("|").split("|")]
    # first cell is the row label (e.g. "$6\delta$"), remaining 12 are values
    label, values_raw = cells[0], cells[1:]
    if len(values_raw) != 12:
        raise ValueError(f"expected 12 value cells, got {len(values_raw)}: {values_raw}")

    values = []
    for v in values_raw:
        v_clean = v.replace("*", "").strip()
        if not re.match(r"^-?\d+$", v_clean):
            raise ValueError(f"non-integer cell value: {v!r} (cleaned: {v_clean!r})")
        values.append(int(v_clean))
    return label, values


def main():
    note_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_NOTE
    if not note_path.exists():
        print(f"FAIL: note not found: {note_path}", file=sys.stderr)
        sys.exit(1)

    text = note_path.read_text(encoding="utf-8")

    try:
        label, doc_values = extract_table_after_marker(text, CORRECT_TABLE_MARKER)
    except ValueError as e:
        print(f"FAIL: could not parse table from note: {e}", file=sys.stderr)
        sys.exit(1)

    ref_values = independent_reference_table()

    mismatches = [
        (r, doc_values[r], ref_values[r]) for r in range(12) if doc_values[r] != ref_values[r]
    ]

    print("=== delta_table_check.py ===")
    print(f"note:          {note_path}")
    print(f"table row label in doc: {label}")
    print(f"doc values:    {doc_values}")
    print(f"reference values (independent re-derivation): {ref_values}")

    if mismatches:
        print(f"FAIL: {len(mismatches)} mismatch(es): {mismatches}", file=sys.stderr)
        sys.exit(1)

    print("PASS: note table matches independent re-derivation from definition (12/12).")
    sys.exit(0)


if __name__ == "__main__":
    main()
