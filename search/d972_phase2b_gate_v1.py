#!/usr/bin/env python3
"""Scale and structure preflight for the Phase-2b nonsplit candidate.

This gate does not enumerate GT shadows or form a reduction image.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import threading
import time
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def gap_library_path() -> Path:
    return Path(os.environ.get("ProgramFiles", r"C:\Program Files")) / (
        "GAP-4.16.0/runtime/opt/gap-4.16.0/grp/perf5.grp"
    )


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def atomic_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(
        json.dumps(value, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8"
    )
    os.replace(temporary, path)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="search/certs/d972_phase2b_gate_v1_20260813.json")
    parser.add_argument(
        "--checkpoint", default="search/certs/d972_phase2b_gate_v1_checkpoint.json"
    )
    parser.add_argument("--hard-timeout-seconds", type=int, default=120)
    args = parser.parse_args()
    output = ROOT / args.output
    checkpoint = ROOT / args.checkpoint
    started = time.monotonic()
    state: dict[str, object] = {
        "schema": "d972_phase2b_gate_checkpoint/v1",
        "stage": "start",
        "complete": False,
    }
    atomic_json(checkpoint, state)

    def timeout() -> None:
        time.sleep(args.hard_timeout_seconds)
        if not state.get("complete"):
            state.update(stage="hard_timeout")
            atomic_json(checkpoint, state)
            os._exit(124)

    threading.Thread(target=timeout, daemon=True).start()
    try:
        library = gap_library_path()
        text = library.read_text(encoding="utf-8")
        begin = text.index("# 32256.2")
        end = text.index("PERFGRP[73]", begin)
        entry = text[begin:end]
        metadata_present = all(token in entry for token in (
            '"abcuvwxyz"', '[[a*v*w,c,x]]', '[72]', '"L2(8) N 2^6"', '[16,6,2]'
        ))
        relation_count = entry.split("[[a*v*w,c,x]]", 1)[0].count("^-1")
        # The count above is only a text-integrity receipt, not a presentation invariant.
        source_pure_order = 2916 * 32256
        target_pure_order = 2916 * 504
        source_full_order = 6 * source_pure_order
        candidate_scan_bound = 6 * 32256
        selected_lift_pair_bound = 8 * 64
        now = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        cert = {
            "schema": "d972_phase2b_gate/v1",
            "run_id": f"d972-phase2b-gate-{now}",
            "generated_by": {
                "script": "search/d972_phase2b_gate_v1.py",
                "tool": "Python 3.13 standard library",
            },
            "candidate": {
                "library_id": "PerfectGroup(32256,2)",
                "library_label": "L2(8) N 2^6",
                "order": 32256,
                "normal_module_order": 64,
                "simple_quotient_order": 504,
                "library_permutation_degree": 72,
                "library_metadata_tokens_present": metadata_present,
                "entry_inverse_token_count": relation_count,
                "library_path": str(library),
                "library_sha256": sha256(library),
                "library_attribution": "GAP perfect-groups data based on Holt/Plesken",
            },
            "scale": {
                "source_pure_roof_quotient_order": source_pure_order,
                "source_full_roof_quotient_order": source_full_order,
                "target_pure_roof_quotient_order": target_pure_order,
                "candidate_hexagon_scan_upper_bound": candidate_scan_bound,
                "fixed_quotient_lift_pair_upper_bound": selected_lift_pair_bound,
                "permutation_degree": 72,
                "hard_timeout_seconds_for_official_run": 900,
            },
            "premeasurement_gates": {
                "PH2_VOID_question": (
                    "does the candidate split as a solvable group direct-product PSL(2,8)?"
                ),
                "PH2_VOID_expected_raw_boolean": False,
                "nonsplit_and_perfect_must_be_recomputed": True,
                "normal_module_irreducibility_must_be_recomputed": True,
                "isolatedness_must_be_settled_before_measurement": True,
                "source_shadow_count_must_be_positive_before_measurement": True,
            },
            "candidate_selection": {
                "selected": "nonsplit 2^6 extension",
                "PGammaL_route_selected": False,
                "PGammaL_note": (
                    "the arithmetic normalizer alone supplies neither a pure-kernel inclusion "
                    "K subset M nor a new PB3 quotient; it is not used as an automatic refinement"
                ),
            },
            "measurement_performed": False,
            "reduction_image_formed": False,
            "u_touched": False,
            "c_touched": False,
            "sealed_k5_touched": False,
            "elapsed_ms": int(1000 * (time.monotonic() - started)),
        }
        atomic_json(output, cert)
        state.update(
            stage="complete", complete=True, output=args.output, run_id=cert["run_id"]
        )
        atomic_json(checkpoint, state)
        print(json.dumps({
            "run_id": cert["run_id"],
            "candidate_order": 32256,
            "scan_bound": candidate_scan_bound,
            "measurement_performed": False,
        }, sort_keys=True))
        return 0
    except Exception as exc:
        state.update(stage="error", error=repr(exc))
        atomic_json(checkpoint, state)
        raise


if __name__ == "__main__":
    raise SystemExit(main())
