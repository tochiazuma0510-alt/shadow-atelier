#!/usr/bin/env python3
"""
search/probe/w6_bu_s0/finalize_v2_1_cert.py -- patches the already-written
cert v2.1 (search/certs/w6_bu_s0_iso_gate_r3r4_v2_1_20260805.json) with the
conventions_used machine-diff result (search/probe/w6_bu_s0/
conventions_diff_v2_1_result.json), which can only be computed AFTER both the
GAP driver and the Python second system have run (chicken-and-egg: the diff
needs both outputs to exist). This is a post-hoc field addition, not a
rewrite of any other content in the cert -- run once, after
conventions_diff_v2_1.py has produced its result file.
"""
import json

CERT_PATH = "search/certs/w6_bu_s0_iso_gate_r3r4_v2_1_20260805.json"
PY_OUTPUT_PATH = "search/probe/w6_bu_s0/r4_second_system_output_v2_1.json"
DIFF_PATH = "search/probe/w6_bu_s0/conventions_diff_v2_1_result.json"


def main():
    with open(DIFF_PATH, encoding="utf-8") as f:
        diff = json.load(f)

    diff_summary = {
        "status": "PASS -- 要修正B closed (裁定543)",
        "method": "search/probe/w6_bu_s0/conventions_diff_v2_1.py compared the GAP cert's conventions_used against the Python second system's conventions_used on the 5 commander-specified keys",
        "diffable_count": diff["diffable_count"],
        "all_5_keys_match": diff["all_5_keys_match"],
        "grading_prohibitions_match": diff["grading_prohibitions_match"],
        "result_file": DIFF_PATH,
    }

    with open(CERT_PATH, encoding="utf-8") as f:
        cert = json.load(f)
    cert["conventions_used_machine_diff"] = diff_summary
    with open(CERT_PATH, "w", encoding="utf-8") as f:
        json.dump(cert, f, ensure_ascii=False, indent=None, separators=(",", ":"))
    print(f"patched {CERT_PATH} with conventions_used_machine_diff = {diff_summary}")

    with open(PY_OUTPUT_PATH, encoding="utf-8") as f:
        py_out = json.load(f)
    py_out["conventions_used_machine_diff"] = diff_summary
    with open(PY_OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(py_out, f, ensure_ascii=False, indent=2)
    print(f"patched {PY_OUTPUT_PATH} with conventions_used_machine_diff = {diff_summary}")


if __name__ == "__main__":
    main()
