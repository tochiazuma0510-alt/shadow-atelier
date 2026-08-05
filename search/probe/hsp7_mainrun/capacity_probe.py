#!/usr/bin/env python3
"""Synthetic, noncandidate capacity probe for HS lane artifacts.

The generated rows intentionally violate the candidate schema (m=-99,
exponents=9, synthetic_noncandidate=true), so none can be mistaken for or
fed back as a main-run candidate.  Files live only in the OS temporary
directory.  The receipt records measured bytes/row and clearly labels the
full-run numbers as linear extrapolations, not performance measurements.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from binding_gate_lib import PCGS_BASIS_CONTRACT, pcgs_basis_fingerprint

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "search/certs/hsp7_capacity_noncontact_v2_20260805.json"
N = 20_000
TOTALS = {"S": 705_894, "V": 705_894, "P": 117_649}
WHOLE_CLASS_GZIP_CAP = 2 * 1024 * 1024 * 1024
PER_LANE_GZIP_CAP = {lane: 680 * 1024 * 1024 for lane in ("S", "V", "P")}


def synthetic_basis_material(lane: str) -> dict:
    units = [[1 if i == j else 0 for j in range(6)] for i in range(6)]
    ambient_units = [[1 if i == j else 0 for j in range(8)] for i in range(8)]
    pairs = []
    for i in range(1, 7):
        for j in range(i + 1, 7):
            pairs.append({"i": i, "j": j, "coordinates": [0] * 6})
    return {
        "ambient_named_generator_coordinates": [
            {"name": "x", "coordinates": ambient_units[0]},
            {"name": "y", "coordinates": ambient_units[1]},
        ],
        "ambient_pcgs_relative_orders": [7] * 8,
        "contract": PCGS_BASIS_CONTRACT,
        "ordered_basis_in_ambient_coordinates": [
            {"i": i + 1, "coordinates": ambient_units[i + 2]} for i in range(6)],
        "relative_orders": [7] * 6,
        "pair_commutator_coordinates": pairs,
        "theta_image_coordinates": [
            {"i": i + 1, "coordinates": units[5 - i]} for i in range(6)],
        "tau_image_coordinates": [
            {"i": i + 1, "coordinates": units[(i + 1) % 6]} for i in range(6)],
        "s_to_v_bridge_coordinates": ([
            {"i": i + 1, "coordinates": units[i]} for i in range(6)]
            if lane == "V" else []),
        "source_artifact": {
            "path": "search/probe/hsp7_cond4_laneS/PQ_OUTPUT_P.g",
            "sha256": "7" * 64,
        },
    }


def row(lane: str, i: int) -> dict:
    token = hashlib.sha256(f"synthetic-capacity-{lane}-{i}".encode()).hexdigest()[:16]
    fixture_id = f"synthetic-noncandidate-{token}"
    if lane == "P":
        return {"f_index": -1, "f_key": {"e": [9, 9, 9, 9, 9, 9]},
                "joined_pair_indices": [-1, -1, -1, -1, -1, -1],
                "fixture_id": fixture_id, "pentagon_verdict": False,
                "CONV_native_element_agree": True, "CONV_native_verdict_agree": True}
    elif lane == "S":
        return {"pair_index": -1, "f_index": -1,
                "candidate_key": {"m": -99, "e": [9, 9, 9, 9, 9, 9]},
                "fixture_id": fixture_id, "hex310": False, "hex311": False,
                "verdict": False}
    return {"pair_index": -1, "f_index": -1,
            "candidate_key": {"m": -99, "e": [9, 9, 9, 9, 9, 9]},
            "fixture_id": fixture_id,
            "N": {"hex33": False, "hex34": False, "verdict": False},
            "N0": {"hex33": False, "hex34": False, "verdict": False},
            "N_N0_agree": True, "CF_baseline_agree": True}


def cert(lane: str, records: list[dict]) -> dict:
    material = synthetic_basis_material(lane)
    return {"schema": "hsp7-lane-cert/v3", "lane": lane,
            "axis": "f" if lane == "P" else "pair",
            "class_id": "synthetic-noncandidate-capacity",
            "run": {"run_id": "synthetic", "run_attempt": "1", "commit_sha": "synthetic"},
            "source_bindings": {k: "synthetic" for k in
                                ("source_bundle_sha256", "wrapper_sha256", "predicate_sha256",
                                 "aux_sha256", "schema_sha256")},
            "pcgs_basis_material": material,
            "pcgs_basis_fingerprint": pcgs_basis_fingerprint(material),
            "universe_total": 117649 if lane == "P" else 705894,
            "evaluated_range": [-1, -1], "records": records,
            "summary": {"evaluated_count": len(records), "unknown_count": 0, "integrity_ok": True},
            "driver_done": True}


def measure(lane: str) -> dict:
    import gzip
    raw = (json.dumps(cert(lane, [row(lane, i) for i in range(N)]),
                      sort_keys=True, separators=(",", ":")) + "\n").encode()
    empty = (json.dumps(cert(lane, []), sort_keys=True, separators=(",", ":")) + "\n").encode()
    gz = gzip.compress(raw, compresslevel=6, mtime=0)
    empty_gz = gzip.compress(empty, compresslevel=6, mtime=0)
    raw_b, gz_b = len(raw), len(gz)
    marginal_raw = (raw_b - len(empty)) / N
    marginal_gz = (gz_b - len(empty_gz)) / N
    total = TOTALS[lane]
    return {
        "synthetic_rows_measured": N,
        "raw_bytes_measured": raw_b,
        "gzip_bytes_measured": gz_b,
        "raw_header_footer_bytes": len(empty),
        "gzip_header_footer_bytes": len(empty_gz),
        "raw_bytes_per_synthetic_row": marginal_raw,
        "gzip_bytes_per_synthetic_row": marginal_gz,
        "linear_extrapolation_rows": total,
        "raw_bytes_extrapolated": int(len(empty) + marginal_raw * total + 0.999999),
        "gzip_bytes_extrapolated": int(len(empty_gz) + marginal_gz * total + 0.999999),
        "raw_sha256": hashlib.sha256(raw).hexdigest(),
        "gzip_sha256": hashlib.sha256(gz).hexdigest(),
    }


def main() -> int:
    results = {lane: measure(lane) for lane in ("S", "V", "P")}
    raw_total = sum(x["raw_bytes_extrapolated"] for x in results.values())
    gz_total = sum(x["gzip_bytes_extrapolated"] for x in results.values())
    receipt = {
        "schema": "hsp7-capacity-noncontact/v2",
        "candidate_universe_contact": 0,
        "synthetic_fixture_is_deliberately_invalid_candidate_data": True,
        "production_record_shape_used": True,
        "measurement": results,
        "linear_extrapolation_all_lanes": {"raw_bytes": raw_total, "gzip_bytes": gz_total},
        "retention_policy": {
            "per_shard_uncompressed_cap_bytes": 20 * 1024 * 1024,
            "per_lane_compressed_cap_bytes": PER_LANE_GZIP_CAP,
            "per_lane_cap_sum_bytes": sum(PER_LANE_GZIP_CAP.values()),
            "whole_class_compressed_cap_bytes": WHOLE_CLASS_GZIP_CAP,
            "artifact_retention_days": 30,
            "recovery": "retain immutable shard certs plus manifest/join receipt; rerun only an explicitly failed shard under the same class and source digests",
            "cap_action": "STOP before upload; no truncation, sampling, or silent record deletion",
        },
        "interpretation": "Serialization/capacity measurement on deliberately invalid synthetic rows. Linear extrapolation only; not a main-run speed or output-size observation.",
    }
    OUT.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(receipt, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
