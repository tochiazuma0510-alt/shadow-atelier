#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
search/certs/ep_sweep744/run_laneb_sweep744.py

Lane B batch runner for the P5 sivar sweep: calls the SAME run_checker()
that search/ninfty-checker.py's own CLI (main()) calls, once per candidate,
looping in-process instead of spawning 744 separate python processes (pure
performance choice -- run_checker() itself is unchanged and is a pure
function of its candidate dict argument, so batching does not alter what is
computed).

Loaded by file path (module has hyphens in its filename, like the
lazy-loader pattern already used inside ninfty-checker.py for its own
native-construction submodule).

Usage: python search/certs/ep_sweep744/run_laneb_sweep744.py
Reads: search/certs/ep_sweep744/candidates_744.json
Writes: search/certs/ep_sweep744/laneb_results_744.json
"""

import hashlib
import importlib.util
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))


def _load_checker_module():
    path = os.path.join(ROOT, "search", "ninfty-checker.py")
    spec = importlib.util.spec_from_file_location("ninfty_checker_sweep744", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod, path


def sha256_of_file(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def main():
    checker_mod, checker_path = _load_checker_module()
    checker_digest = sha256_of_file(checker_path)

    cand_file = os.path.join(HERE, "candidates_744.json")
    with open(cand_file, "rb") as f:
        cand_raw = f.read()
    cand_digest = hashlib.sha256(cand_raw).hexdigest()
    cand_data = json.loads(cand_raw.decode("utf-8"))

    results = []
    for entry in cand_data["candidates"]:
        candidate = dict(entry["candidate"])
        try:
            r = checker_mod.run_checker(candidate)
            out = {
                "stage": r.get("stage"),
                "primary_reason_code": r.get("primary_reason_code"),
                "reason_codes": r.get("reason_codes"),
                "checker_id": r.get("checker_id"),
                "algorithm": r.get("algorithm"),
            }
        except Exception as e:  # noqa: BLE001 -- record, never crash the sweep
            out = {"error": type(e).__name__, "message": str(e)}
        results.append({"global_index": entry["global_index"], "lane_B": out})

    final_out = {
        "role_note": "Lane B (python, ninfty-checker.py run_checker) batch results for the 744-candidate P5 sweep.",
        "entry_point": "search/ninfty-checker.py :: run_checker (same function the CLI main() calls)",
        "entry_point_sha256": checker_digest,
        "input_candidates_file": "search/certs/ep_sweep744/candidates_744.json",
        "input_candidates_sha256": cand_digest,
        "total": len(results),
        "results": results,
    }
    out_path = os.path.join(HERE, "laneb_results_744.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(final_out, f, indent=2, ensure_ascii=True)
        f.write("\n")

    print(json.dumps({"total": len(results), "entry_point_sha256": checker_digest, "input_candidates_sha256": cand_digest}, indent=2))


if __name__ == "__main__":
    main()
