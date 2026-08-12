#!/usr/bin/env python3
"""Compare the wall-derived Xi model with the independent AGL x S_t lane."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def class_signature(row: dict) -> tuple:
    return (
        row["index"],
        row["class_size"],
        row["maximal_is_normal"],
        row["primitive_order"],
        tuple(row["primitive_id"] or ()),
        row["socle_order"],
        row["crown_abelian"],
    )


def census_signature(census: dict) -> dict:
    return {
        "group_order": census["group_order"],
        "frattini_order": census["frattini_order"],
        "quotient_order": census["quotient_order"],
        "maximal_class_count": census["maximal_class_count"],
        "abelian_crown_count": census["abelian_crown_count"],
        "nonabelian_crown_count": census["nonabelian_crown_count"],
        "class_multiset": sorted(class_signature(row) for row in census["classes"]),
    }


def distinct_prime_count(value: int) -> int:
    count = 0
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            count += 1
            while value % divisor == 0:
                value //= divisor
        divisor += 1
    return count + (value > 1)


def theory_signature(ell: int, t: int) -> dict:
    """Independent direct-product maximal-class count.

    AGL(1,ell) contributes one complement class plus one normal class for
    each distinct prime divisor of ell-1.  S5 has four maximal classes and
    S6 has six.  Both factors have a C2 quotient, producing one additional
    diagonal maximal class.  The nonnormal S_t classes have socle A_t; all
    remaining primitive socles are cyclic of prime order.
    """
    omega = distinct_prime_count(ell - 1)
    symmetric_maximal_classes = {5: 4, 6: 6}[t]
    return {
        "group_order": ell * (ell - 1) * math.factorial(t),
        "frattini_order": 1,
        "quotient_order": ell * (ell - 1) * math.factorial(t),
        "maximal_class_count": omega + 1 + symmetric_maximal_classes + 1,
        "abelian_crown_count": omega + 3,
        "nonabelian_crown_count": symmetric_maximal_classes - 1,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--producer", type=Path, required=True)
    parser.add_argument("--model", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    producer = json.loads(args.producer.read_text(encoding="utf-8"))
    model = json.loads(args.model.read_text(encoding="utf-8"))
    p_by_label = {row["label"]: row for row in producer["walls"]}
    m_by_label = {row["label"]: row for row in model["walls"]}

    rows = []
    for label in ("wall24", "wall28", "wall36", "wall37"):
        p = p_by_label[label]
        m = m_by_label[label]
        ps = census_signature(p["census"])
        ms = census_signature(m)
        ts = theory_signature(p["ell"], p["t"])
        theory_fields_equal = all(ps[key] == value for key, value in ts.items())
        rows.append(
            {
                "label": label,
                "all_charming_layers_represented": p[
                    "all_charming_layers_represented"
                ],
                "xi_image_equals_normalizer": p["xi_image_equals_normalizer"],
                "producer_signature": ps,
                "model_signature": ms,
                "signatures_equal": ps == ms,
                "independent_theory_signature": ts,
                "independent_theory_fields_equal": theory_fields_equal,
            }
        )

    controls = {row["label"]: row["census"] for row in producer["positive_controls"]}
    output = {
        "schema": "wall-crown-census-check/v1",
        "generated_by": "search/check_wall_crown_census_v1.py",
        "producer_path": f"search/certs/{args.producer.name}",
        "producer_sha256": digest(args.producer),
        "model_path": f"search/certs/{args.model.name}",
        "model_sha256": digest(args.model),
        "positive_controls": {
            "K9_maximal_class_count": controls["K9"]["maximal_class_count"],
            "roof972_maximal_class_count": controls["roof972"][
                "maximal_class_count"
            ],
        },
        "walls": rows,
        "all_signatures_equal": all(row["signatures_equal"] for row in rows),
        "all_independent_theory_fields_equal": all(
            row["independent_theory_fields_equal"] for row in rows
        ),
        "quarantine": {
            "K9": "group-theory positive control only",
            "K5": "not accessed",
            "name_collide": "wall-window instance",
            "u_c": "not accessed",
        },
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(
        "WALL_CROWN_CENSUS_CHECK_DONE "
        f"all_signatures_equal={output['all_signatures_equal']}"
    )


if __name__ == "__main__":
    main()
