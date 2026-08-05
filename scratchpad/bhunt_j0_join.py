#!/usr/bin/env python3
"""B-HUNT (J0): join lane S/V (hexagon, layered) with lane P (PENT, layer-independent)
to realize the 42 candidate keys via join, with zero new window computation.

Reads (all pre-existing artifacts, none modified):
  scratchpad/mainrun_results/S/join_manifest.json  (705,894 records: {flat_index,key:{e,m},status})
  scratchpad/mainrun_results/V/join_manifest.json  (same shape, independent lane, cross-check)
  scratchpad/mainrun_results/P/join_manifest.json  (117,649 records: {flat_index,key:{e},joined_pair_indices,status})

Streams with ijson (constant memory) since files are ~180MB each.

Writes scratchpad/bhunt_j0_output.json with:
  - per-layer S PASS counts, V PASS counts, S/V mismatch count (must be 0, per cert)
  - P lane global PASS count (must be 49)
  - per-layer pent(m) = S_pass[m] cap P_pass_global, as sorted e-tuples
  - L = pent(0) (7 elements expected)
  - pent(m0=1) (7 elements expected, generating layer u0=3)
"""
import ijson
import json
import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
S_PATH = ROOT / "scratchpad/mainrun_results/S/join_manifest.json"
V_PATH = ROOT / "scratchpad/mainrun_results/V/join_manifest.json"
P_PATH = ROOT / "scratchpad/mainrun_results/P/join_manifest.json"

XN_ORDERED = [0, 1, 2, 4, 5, 6]  # m values with gcd(2m+1,7)=1, ascending (candidate_key_lib.g)


def sha256_of(path, chunk=1 << 20):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            b = f.read(chunk)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def stream_lane_SV(path):
    """Yields (m, e_tuple, status) for every record, streaming."""
    with open(path, "rb") as f:
        for item in ijson.items(f, "shards.item.candidate_keys.item"):
            key = item["key"]
            yield key["m"], tuple(key["e"]), item["status"]


def stream_lane_P(path):
    """Yields (e_tuple, status) for every record, streaming."""
    with open(path, "rb") as f:
        for item in ijson.items(f, "shards.item.candidate_keys.item"):
            key = item["key"]
            yield tuple(key["e"]), item["status"]


def main():
    print("hashing input artifacts (sha256, streaming)...", file=sys.stderr)
    sha_s = sha256_of(S_PATH)
    sha_v = sha256_of(V_PATH)
    sha_p = sha256_of(P_PATH)
    print(f"S sha256={sha_s}", file=sys.stderr)
    print(f"V sha256={sha_v}", file=sys.stderr)
    print(f"P sha256={sha_p}", file=sys.stderr)

    print("streaming lane S...", file=sys.stderr)
    S_pass = {m: set() for m in XN_ORDERED}
    s_status_counts = {"PASS": 0, "FAIL": 0, "UNKNOWN": 0}
    s_total = 0
    for m, e, status in stream_lane_SV(S_PATH):
        s_total += 1
        s_status_counts[status] = s_status_counts.get(status, 0) + 1
        if status == "PASS":
            if m not in S_pass:
                raise SystemExit(f"UNEXPECTED m={m} in lane S (not in XN_ORDERED)")
            S_pass[m].add(e)

    print("streaming lane V...", file=sys.stderr)
    V_pass = {m: set() for m in XN_ORDERED}
    v_status_counts = {"PASS": 0, "FAIL": 0, "UNKNOWN": 0}
    v_total = 0
    for m, e, status in stream_lane_SV(V_PATH):
        v_total += 1
        v_status_counts[status] = v_status_counts.get(status, 0) + 1
        if status == "PASS":
            if m not in V_pass:
                raise SystemExit(f"UNEXPECTED m={m} in lane V (not in XN_ORDERED)")
            V_pass[m].add(e)

    print("streaming lane P...", file=sys.stderr)
    P_pass_global = set()
    p_status_counts = {"PASS": 0, "FAIL": 0, "UNKNOWN": 0}
    p_total = 0
    for e, status in stream_lane_P(P_PATH):
        p_total += 1
        p_status_counts[status] = p_status_counts.get(status, 0) + 1
        if status == "PASS":
            P_pass_global.add(e)

    # cross-check S vs V (mismatch must be 0, per cert claim)
    mismatch_count = 0
    mismatch_examples = []
    for m in XN_ORDERED:
        sym = S_pass[m].symmetric_difference(V_pass[m])
        if sym:
            mismatch_count += len(sym)
            if len(mismatch_examples) < 10:
                mismatch_examples.extend([{"m": m, "e": list(e)} for e in list(sym)[:10]])

    # J0 join: pent(m) = S_pass[m] (hex(m)) cap P_pass_global (D^{-1}(1))
    pent = {}
    for m in XN_ORDERED:
        pent[m] = sorted(S_pass[m] & P_pass_global)

    per_layer_counts = {str(m): len(pent[m]) for m in XN_ORDERED}
    total_pent = sum(per_layer_counts.values())

    L = pent[0]
    pent_m1 = pent[1]

    out = {
        "schema": "bhunt-j0-join/v1",
        "provenance": {
            "S_join_manifest": {"path": str(S_PATH.relative_to(ROOT)).replace("\\", "/"), "sha256": sha_s, "total_records": s_total, "status_counts": s_status_counts},
            "V_join_manifest": {"path": str(V_PATH.relative_to(ROOT)).replace("\\", "/"), "sha256": sha_v, "total_records": v_total, "status_counts": v_status_counts},
            "P_join_manifest": {"path": str(P_PATH.relative_to(ROOT)).replace("\\", "/"), "sha256": sha_p, "total_records": p_total, "status_counts": p_status_counts},
        },
        "xn_ordered": XN_ORDERED,
        "s_pass_per_layer_counts": {str(m): len(S_pass[m]) for m in XN_ORDERED},
        "v_pass_per_layer_counts": {str(m): len(V_pass[m]) for m in XN_ORDERED},
        "s_v_mismatch_count": mismatch_count,
        "s_v_mismatch_examples": mismatch_examples,
        "p_pass_global_count": len(P_pass_global),
        "pent_per_layer_counts": per_layer_counts,
        "pent_total": total_pent,
        "L_m0": [list(e) for e in L],
        "L_m0_count": len(L),
        "pent_m1": [list(e) for e in pent_m1],
        "pent_m1_count": len(pent_m1),
        "pent_all": {str(m): [list(e) for e in pent[m]] for m in XN_ORDERED},
    }

    out_path = ROOT / "scratchpad/bhunt_j0_output.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, sort_keys=False)
    print(f"wrote {out_path}", file=sys.stderr)
    print(json.dumps({
        "s_v_mismatch_count": mismatch_count,
        "p_pass_global_count": len(P_pass_global),
        "pent_per_layer_counts": per_layer_counts,
        "pent_total": total_pent,
        "L_m0_count": len(L),
        "pent_m1_count": len(pent_m1),
    }, indent=2))


if __name__ == "__main__":
    main()
