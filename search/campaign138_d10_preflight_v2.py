#!/usr/bin/env python3
"""Second parser revision for the frozen [16,10,1] preflight universe."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from sympy.combinatorics.free_groups import free_group

import campaign138_d10_preflight_v1 as prior


ROOT = Path(__file__).resolve().parents[1]
PREREG = ROOT / "search/certs/campaign138_d10_preflight_prereg_v2_20260815.json"


def parse_v2() -> dict:
    library = prior.LIBRARY.read_text(encoding="utf-8", errors="replace")
    label_at = library.index(f'"{prior.LABEL}"')
    start = library.rfind("# 516096.", 0, label_at)
    finish = library.find("PERFGRP[", label_at)
    segment = library[start:finish]
    uncommented = re.sub(r"#[^\r\n]*", "", segment)
    compact = re.sub(r"\s+", "", uncommented)
    names = re.search(r'\[\[1,"([a-z]+)"', compact).group(1)
    expression_start = compact.index("return") + len("return")
    expression_end = prior.matching_square(compact, expression_start)
    outer = prior.base.list_items(compact[expression_start : expression_end + 1])
    free_data = free_group(",".join(names))
    namespace = dict(zip(names, free_data[1:]))

    def translate(expression: str):
        expression = re.sub(
            r"\b([a-z])\^([a-z])\b",
            lambda match: (
                f"({match.group(2)}**-1*{match.group(1)}*{match.group(2)})"
            ),
            expression,
        )
        return eval(expression.replace("^", "**"), {"__builtins__": {}}, namespace)

    return {
        "names": names,
        "free": free_data[0],
        "generators": tuple(free_data[1:]),
        "relations": [translate(item) for item in prior.base.list_items(outer[0])],
        "subgroup_lists": [
            [translate(item) for item in prior.base.list_items(subgroup)]
            for subgroup in prior.base.list_items(outer[1])
        ],
        "segment_sha256": hashlib.sha256(segment.encode()).hexdigest(),
    }


def main() -> int:
    prior.parse = parse_v2
    prior.PREREG = PREREG
    prior.__file__ = __file__
    return prior.main()


if __name__ == "__main__":
    raise SystemExit(main())
