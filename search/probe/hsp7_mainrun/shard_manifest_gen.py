#!/usr/bin/env python3
"""search/probe/hsp7_mainrun/shard_manifest_gen.py

Shard manifest generator for the HS main-run (prereg v2). NEW file
(individually digested, not part of the frozen predicate library).

Purely arithmetic: partitions a flat index range [0, total-1] into
contiguous, non-overlapping shards of a given target size, using the SAME
pair-flat-index / f-index semantics as candidate_key_lib.g (this script does
not call GAP, does not build any group, and does not evaluate any judgement
predicate -- it only computes integer ranges). Lane S/V use the pair index
range [0, 705893]; Lane P (after the accepted PENT-does-not-depend-on-m
optimization, Sol 便104 F104-1.5) uses the smaller f-index range
[0, 117648].

This generator does not decide shard size on its own authority: shard_size
must be supplied by the caller (structural design values are proposed in
prereg v1 appendix C / appendix C v2 SS1.2, still unconfirmed as of this
bundle -- Sol 便104 F104-1.3 flagged the Actions max-parallel/256-job-per-
workflow constraints that bound feasible shard counts).
"""
import argparse
import hashlib
import json
import sys


LANE_TOTALS = {
    "S": 705894,
    "V": 705894,
    "P": 117649,  # post-optimization f-index axis (Sol F104-1.5)
}

# Immutable v3 operational partition.  These are not timing predictions:
# they are the exact arithmetic partition bound to the HS class draft.
FROZEN_SHARD_SIZES_V3 = {"S": 3678, "V": 54000, "P": 3678}
FROZEN_TIMEOUT_MIN_V3 = 60


def make_shards(total, shard_size):
    if shard_size <= 0:
        raise ValueError("shard_size must be positive")
    shards = []
    lo = 0
    idx = 0
    while lo < total:
        hi = min(lo + shard_size - 1, total - 1)
        shards.append({"name": f"shard_{idx:05d}", "lo": lo, "hi": hi})
        lo = hi + 1
        idx += 1
    return shards


def verify_partition(shards, total):
    """Exact-cover check: shards must partition [0,total-1] with no gap,
    no overlap, sorted ascending. This mirrors the check join_checker.py
    performs against REAL per-shard cert output after a run; here it is run
    against the manifest itself as a structural self-test before any job is
    dispatched."""
    covered = 0
    prev_hi = -1
    for s in shards:
        if s["lo"] != prev_hi + 1:
            return False, f"gap or overlap before {s['name']}: lo={s['lo']} expected {prev_hi+1}"
        if s["hi"] < s["lo"]:
            return False, f"empty/inverted shard {s['name']}"
        covered += s["hi"] - s["lo"] + 1
        prev_hi = s["hi"]
    if prev_hi != total - 1:
        return False, f"coverage ends at {prev_hi}, expected {total-1}"
    if covered != total:
        return False, f"covered count {covered} != total {total}"
    return True, "exact cover confirmed"


def build_manifest(lane, shard_size, timeout_min, frozen_driver_digest, max_parallel=20,
                    max_jobs_per_workflow=256, class_id="UNSET", source_bundle_sha256="UNSET",
                    pcgs_id="UNSET", pcgs_basis_contract="UNSET",
                    pcgs_basis_fingerprint=None,
                    pcgs_source_artifact_path="UNSET",
                    pcgs_source_artifact_sha256="UNSET"):
    if lane not in LANE_TOTALS:
        raise ValueError(f"unknown lane {lane!r}, expected one of {list(LANE_TOTALS)}")
    total = LANE_TOTALS[lane]
    shards = make_shards(total, shard_size)
    ok, msg = verify_partition(shards, total)
    if not ok:
        raise RuntimeError(f"INTERNAL_STOP: generated shard set failed its own partition check: {msg}")
    n_shards = len(shards)
    n_workflow_batches = (n_shards + max_jobs_per_workflow - 1) // max_jobs_per_workflow
    manifest = {
        "schema": "hsp7-mainrun-shard-manifest/v2",
        "class_id": class_id,
        "source_bundle_sha256": source_bundle_sha256,
        "pcgs_id": pcgs_id,
        "pcgs_basis_contract": pcgs_basis_contract,
        "pcgs_basis_fingerprint": pcgs_basis_fingerprint,
        "pcgs_source_artifact_path": pcgs_source_artifact_path,
        "pcgs_source_artifact_sha256": pcgs_source_artifact_sha256,
        "endian": "big",
        "key_semantics": {
            "radix": 7,
            "exponent_width": 6,
            "m_values": [0, 1, 2, 4, 5, 6],
            "f_total": 117649,
            "axis": "f" if lane == "P" else "pair",
        },
        "lane": lane,
        "total_candidates": total,
        "shard_size_target": shard_size,
        "n_shards": n_shards,
        "max_parallel": max_parallel,
        "max_jobs_per_workflow": max_jobs_per_workflow,
        "n_workflow_batches_needed": n_workflow_batches,
        "timeout_min": timeout_min,
        "frozen_driver_digest": frozen_driver_digest,
        "partition_self_check": msg,
        "shards": shards,
    }
    if n_shards > max_jobs_per_workflow:
        manifest["_note_workflow_split_required"] = (
            f"{n_shards} shards exceeds the {max_jobs_per_workflow}-job-per-workflow-run "
            f"ceiling (Sol 便104 F104-1.3); dispatch must split into "
            f"{n_workflow_batches} sequential workflow-run batches, not one matrix."
        )
    return manifest


def canonical_bytes(manifest):
    """Canonical serialization for hashing (sorted keys, no whitespace
    ambiguity) -- used so re-ordering shards in the list does not change the
    join checker's notion of the manifest's content-identity, matching
    appendix C v2 SS2 item 3 ('shard の並び替えだけは集合として PASS')."""
    m2 = dict(manifest)
    m2["shards"] = sorted(manifest["shards"], key=lambda s: s["lo"])
    return json.dumps(m2, sort_keys=True, separators=(",", ":")).encode("utf-8")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--lane", required=True, choices=sorted(LANE_TOTALS))
    ap.add_argument("--shard-size", type=int, default=None,
                    help="must equal the frozen v3 lane value; omitted selects it")
    ap.add_argument("--timeout-min", type=int, default=FROZEN_TIMEOUT_MIN_V3)
    ap.add_argument("--frozen-driver-digest", default="UNSET")
    ap.add_argument("--max-parallel", type=int, default=20)
    ap.add_argument("--max-jobs-per-workflow", type=int, default=256)
    ap.add_argument("--class-id", required=True)
    ap.add_argument("--source-bundle-sha256", required=True)
    ap.add_argument("--pcgs-id", required=True)
    ap.add_argument("--pcgs-basis-contract", required=True)
    ap.add_argument("--pcgs-basis-fingerprint", required=True)
    ap.add_argument("--pcgs-source-artifact-path", required=True)
    ap.add_argument("--pcgs-source-artifact-sha256", required=True)
    ap.add_argument("--out", default=None, help="write manifest JSON here (default: stdout)")
    args = ap.parse_args(argv)

    frozen_size = FROZEN_SHARD_SIZES_V3[args.lane]
    shard_size = frozen_size if args.shard_size is None else args.shard_size
    if shard_size != frozen_size:
        ap.error(f"class-v3 shard size for lane {args.lane} is frozen at {frozen_size}, got {shard_size}")
    if args.timeout_min != FROZEN_TIMEOUT_MIN_V3:
        ap.error(f"class-v3 timeout is frozen at {FROZEN_TIMEOUT_MIN_V3} minutes")
    if args.max_parallel != 20 or args.max_jobs_per_workflow != 256:
        ap.error("class-v3 workflow limits are frozen at max_parallel=20 and max_jobs_per_workflow=256")
    manifest = build_manifest(
        args.lane, shard_size, args.timeout_min, args.frozen_driver_digest,
        args.max_parallel, args.max_jobs_per_workflow, args.class_id,
        args.source_bundle_sha256, args.pcgs_id,
        args.pcgs_basis_contract, args.pcgs_basis_fingerprint,
        args.pcgs_source_artifact_path, args.pcgs_source_artifact_sha256,
    )
    manifest["manifest_sha256"] = hashlib.sha256(canonical_bytes(manifest)).hexdigest()
    out_text = json.dumps(manifest, indent=2, sort_keys=True)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(out_text)
    else:
        print(out_text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
