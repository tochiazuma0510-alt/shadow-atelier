#!/usr/bin/env python3
"""
search/xi-set-equality-check.py -- direct GAP-vs-python accepted-SET
equality/digest comparison for the 15 Xi windows (梯子13 + I10-1 2), per
裁定227 (P86-3 item 2 / Sol 便86 sol_reply_86_math13.md S2).

This is a crosscheck script, not a searcher and not a re-implementation of
either side's scan: it reads two ALREADY-PRODUCED artifact sets

  - GAP side:    search/certs/xi_uid_gap_<safe_wid>_20260731.json (x15),
                 written by search/xi-uid-export.g (GAP's own
                 CorrectedShadowsXi, re-run to export the raw accepted set
                 instead of only a digest)
  - python side: search/certs/ladder_xi_recheck_<wid>_20260730.json (x13)
                 and search/certs/i10_1_xi_recheck_20260730.json (x2 windows
                 inside), written by search/ladder-xi-recheck.py (the
                 independent, GAP-free sympy re-implementation)

and compares their accepted_uids sets / accepted_set_digest_sha256 fields
DIRECTLY against each other -- not against any third self-consistency gate.
This closes F86-2.2 欠落2 ("GAP の 26/27 は GAP 内二経路の比較であって、
Python の accepted_set_digest_sha256 との比較ではない"): this script performs
exactly the missing direct comparison.

Both sides already produce UIDs in the identical canonical format Sol
specified:  window_id|m|u2N|full permutation array
(python: candidate_uid() in ladder-xi-recheck.py; GAP: CandidateUid() in
xi-uid-export.g -- same string shape, independently written).

Output: search/certs/xi_set_equality_20260731.json. Raw measurement only
(set equal True/False per window + digest match True/False); no
interpretation of what a mismatch would mean mathematically.
"""

import json
import time

WINDOWS = [
    "W-E-A10-9t1", "W-E-A10-9t1-o2", "W-E-A10-9t1-o3", "W-E-A10-9t1-o4",
    "W-E-A10-9t1-o5", "W-E-A10-9t1-o6",
    "W-E-A11-9t2", "W-E-A11-9t2-o2", "W-E-A11-9t2-o3",
    "W-E-A12-9t3", "W-E-A12-9t3-o2", "W-E-A12-9t3-o3",
    "W-E-A13-9t4",
    "W-E-A10-5x2t0",
    "W-E-A15-5x3t0",
]

I10_1_WINDOWS = {"W-E-A10-5x2t0", "W-E-A15-5x3t0"}

CERT_DIR = "search/certs"


def gap_cert_path(wid):
    safe = wid.replace("-", "_")
    return "%s/xi_uid_gap_%s_20260731.json" % (CERT_DIR, safe)


def python_ladder_cert_path(wid):
    return "%s/ladder_xi_recheck_%s_20260730.json" % (CERT_DIR, wid)


def load_json(path):
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def load_python_i10_1():
    obj = load_json("%s/i10_1_xi_recheck_20260730.json" % CERT_DIR)
    by_wid = {}
    for w in obj["windows"]:
        by_wid[w["wid"]] = w
    return by_wid


def main():
    print("=== search/xi-set-equality-check.py: GAP vs python accepted-set comparison ===")

    py_i10_1 = load_python_i10_1()

    results = []
    all_set_equal = True
    all_digest_match = True

    for wid in WINDOWS:
        gpath = gap_cert_path(wid)
        gcert = load_json(gpath)
        gap_uids = set(gcert["accepted_uids"])
        gap_digest = gcert["accepted_set_digest_sha256"]
        gap_deg = gcert["deg"]
        gap_nord = gcert["N_ord"]

        if wid in I10_1_WINDOWS:
            pentry = py_i10_1[wid]
            py_uids = set(pentry["accepted_uids"])
            py_digest = pentry["accepted_set_digest_sha256"]
            ppath = "%s/i10_1_xi_recheck_20260730.json (window %s)" % (CERT_DIR, wid)
        else:
            ppath = python_ladder_cert_path(wid)
            pcert = load_json(ppath)
            py_uids = set(pcert["accepted_uids"])
            py_digest = pcert["accepted_set_digest_sha256"]

        digest_match = (gap_digest == py_digest)
        set_equal = (gap_uids == py_uids)
        only_in_gap = sorted(gap_uids - py_uids)
        only_in_py = sorted(py_uids - gap_uids)

        if not digest_match:
            all_digest_match = False
        if not set_equal:
            all_set_equal = False

        entry = dict(
            wid=wid,
            gap_cert=gpath, python_cert=ppath,
            deg=gap_deg, N_ord=gap_nord,
            gap_accepted_count=len(gap_uids), python_accepted_count=len(py_uids),
            gap_accepted_set_digest_sha256=gap_digest,
            python_accepted_set_digest_sha256=py_digest,
            digest_match=digest_match,
            set_equal=set_equal,
            only_in_gap_count=len(only_in_gap),
            only_in_python_count=len(only_in_py),
            only_in_gap_sample=only_in_gap[:20],
            only_in_python_sample=only_in_py[:20],
        )
        results.append(entry)
        print("[%s] gap_accepted=%d python_accepted=%d digest_match=%s set_equal=%s"
              % (wid, len(gap_uids), len(py_uids), digest_match, set_equal))
        if not set_equal:
            print("    only_in_gap=%d only_in_python=%d" % (len(only_in_gap), len(only_in_py)))

    out = dict(
        schema="xi-set-equality-check/v1",
        generated_by=dict(tool="python3", script="search/xi-set-equality-check.py",
                           date=time.strftime("%Y-%m-%dT%H:%M:%S%z")),
        note=(
            "Direct comparison of GAP's (search/xi-uid-export.g) and python's "
            "(search/ladder-xi-recheck.py) independently-produced accepted-set "
            "UID lists/digests, per 裁定227 P86-3 item 2. Not a re-scan; reads "
            "only the already-written certificate artifacts from both sides. "
            "Raw measurement only -- 'set_equal'/'digest_match' are computed "
            "booleans per window, no further interpretation."
        ),
        windows_checked=len(WINDOWS),
        all_windows_digest_match=all_digest_match,
        all_windows_set_equal=all_set_equal,
        windows=results,
    )
    out_path = "%s/xi_set_equality_20260731.json" % CERT_DIR
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=2, ensure_ascii=False)
    print("\nWROTE %s" % out_path)
    print("all_windows_digest_match=%s all_windows_set_equal=%s"
          % (all_digest_match, all_set_equal))


if __name__ == "__main__":
    main()
