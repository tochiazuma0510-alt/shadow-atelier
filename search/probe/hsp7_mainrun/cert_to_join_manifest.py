#!/usr/bin/env python3
"""Convert real lane certs to the independent join-checker manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from binding_gate_lib import (pcgs_basis_fingerprint as compute_pcgs_basis_fingerprint,
                              pcgs_basis_material_checks)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def status_from_record(lane: str, rec: dict) -> str:
    if rec.get("status") == "UNKNOWN":
        return "UNKNOWN"
    if lane == "P":
        value = rec.get("pentagon_verdict")
    elif lane == "S":
        value = rec.get("verdict")
    else:
        if rec.get("N_N0_agree") is not True:
            raise ValueError("Lane V record has N/N0 disagreement")
        value = rec.get("N", {}).get("verdict")
    if not isinstance(value, bool):
        raise ValueError("record lacks a Boolean lane verdict")
    return "PASS" if value else "FAIL"


def load_cert(path: Path) -> dict:
    obj = json.loads(path.read_text(encoding="utf-8"))
    if obj.get("schema") != "hsp7-lane-cert/v3" or obj.get("driver_done") is not True:
        raise ValueError(f"{path}: schema/driver_done gate failed")
    if obj.get("summary", {}).get("integrity_ok") is not True:
        raise ValueError(f"{path}: integrity_ok is not true")
    if obj["summary"].get("evaluated_count") != len(obj.get("records", [])):
        raise ValueError(f"{path}: evaluated_count != len(records)")
    lo, hi = obj["evaluated_range"]
    if lo < 0 or hi < lo:
        raise ValueError(f"{path}: registered-fixture cert cannot enter a main-run join")
    if hi - lo + 1 != len(obj["records"]):
        raise ValueError(f"{path}: range length != record count")
    return obj


def build(paths: list[Path], pcgs_id: str, pcgs_basis_fingerprint: str) -> dict:
    loaded = [(p, load_cert(p)) for p in paths]
    first = loaded[0][1]
    lane = first["lane"]
    axis = first["axis"]
    class_id = first["class_id"]
    source_digest = first["source_bindings"]["source_bundle_sha256"]
    if first.get("pcgs_basis_fingerprint") != pcgs_basis_fingerprint:
        raise ValueError("first cert runtime pcgs fingerprint differs from frozen manifest")
    for p, c in loaded:
        if (c["lane"], c["axis"], c["class_id"], c["source_bindings"]["source_bundle_sha256"],
                c.get("pcgs_basis_fingerprint")) != (
                lane, axis, class_id, source_digest, pcgs_basis_fingerprint):
            raise ValueError(f"{p}: cross-shard class/source binding mismatch")
        material_checks = pcgs_basis_material_checks(c.get("pcgs_basis_material"), lane)
        if not all(material_checks.values()):
            raise ValueError(f"{p}: runtime pcgs material shape/structure gate failed")
        if compute_pcgs_basis_fingerprint(c["pcgs_basis_material"]) != pcgs_basis_fingerprint:
            raise ValueError(f"{p}: runtime pcgs material hash mismatch")
    universe = {
        "lane": lane, "axis": axis, "radix": 7, "exponent_width": 6,
        "m_values": [0, 1, 2, 4, 5, 6], "f_total": 117649,
        "total_flat_indices": 117649 if lane == "P" else 705894,
        "pcgs_id": pcgs_id, "endian": "big", "class_id": class_id,
        "pcgs_basis_fingerprint": pcgs_basis_fingerprint,
        "driver_digest": source_digest, "source_bundle_sha256": source_digest,
    }
    shards = []
    for p, c in loaded:
        entries = []
        for r in c["records"]:
            if lane == "P":
                entries.append({"flat_index": r["f_index"], "key": r["f_key"],
                                "joined_pair_indices": r["joined_pair_indices"],
                                "status": status_from_record(lane, r)})
            else:
                entries.append({"flat_index": r["pair_index"], "key": r["candidate_key"],
                                "status": status_from_record(lane, r)})
        run = c["run"]
        shards.append({
            "shard_id": p.stem, "index_range": c["evaluated_range"],
            "pcgs_id": pcgs_id, "pcgs_basis_fingerprint": pcgs_basis_fingerprint,
            "endian": "big", "candidate_keys": entries,
            "receipt": {"run_id": run["run_id"], "run_attempt": run["run_attempt"],
                        "sha": run["commit_sha"], "driver_digest": source_digest,
                        "source_bundle_sha256": source_digest, "class_id": class_id,
                        "driver_done": c["driver_done"], "cert_sha256": sha256(p)},
        })
    return {"universe": universe, "shards": shards}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cert", action="append", required=True)
    ap.add_argument("--pcgs-id", required=True)
    ap.add_argument("--pcgs-basis-fingerprint", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    try:
        result = build([Path(x) for x in args.cert], args.pcgs_id,
                       args.pcgs_basis_fingerprint)
        Path(args.out).write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"CERT_JOIN_STOP: {exc}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
