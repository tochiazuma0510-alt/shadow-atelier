#!/usr/bin/env python
# search/probe/sg_band_sweep/merge_g4_g5_shards.py
# Merges the 4 shard outputs of sg_g4_orb_driver_v1.g (36 g3_records windows
# split into 4x9 to respect the ~600s wall-clock convention) into the single
# G4/G5 companion report. Concatenation only -- no group theory recomputed.
import json, hashlib, sys

SHARDS = [
    "search/certs/sg_g4_g5_orb_20260806_shard1.json",
    "search/certs/sg_g4_g5_orb_20260806_shard2.json",
    "search/certs/sg_g4_g5_orb_20260806_shard3.json",
    "search/certs/sg_g4_g5_orb_20260806_shard4.json",
]
OUT = "search/certs/sg_g4_g5_orb_20260806.json"

def main():
    docs = [json.load(open(p, encoding="utf-8")) for p in SHARDS]

    g4_all = []
    g5_all = []
    handoff_all = []
    alerts_all = []
    for d in docs:
        g4_all.extend(d["g4_orb_records"])
        g5_all.extend(d["g5_classification"])
        handoff_all.extend(d["handoff_mismatches"])
        alerts_all.extend(d["g5_alerts_nonstandard_structure"])

    windows_total = docs[0]["windows_total"]
    windows_processed = sum(d["windows_in_this_shard"] for d in docs)
    if windows_processed + len(handoff_all) != windows_total:
        print(f"MERGE_FAIL: windows_processed({windows_processed})+handoff({len(handoff_all)}) != windows_total({windows_total})")
        sys.exit(1)

    class_counts = {}
    for d in docs:
        for k, v in d["g5_classification_counts"].items():
            class_counts[k] = class_counts.get(k, 0) + v

    base = docs[0]
    merged = {
        "schema": "shadow-atelier/sg-g4-g5-orb/v1",
        "note_merge": "MERGED from 4 shards (9 windows each) -- sharded per gaplib_common.g 600s wall-clock convention; merge is concatenation only, see merge_g4_g5_shards.py",
        "shard_provenance": [
            {"path": p, "shard_output_sha256": hashlib.sha256(open(p, "rb").read()).hexdigest(),
             "driver_self_sha256": d["driver_self_sha256"]}
            for p, d in zip(SHARDS, docs)
        ],
        "authority": base["authority"],
        "input_cert": base["input_cert"],
        "windows_total": windows_total,
        "windows_processed": windows_processed,
        "handoff_mismatches": handoff_all,
        "entry_gate_note": base["entry_gate_note"],
        "pruning_note": base["pruning_note"],
        "g4_orb_records": g4_all,
        "g5_classification": g5_all,
        "g5_classification_counts": class_counts,
        "g5_alerts_nonstandard_structure": alerts_all,
        "vocabulary_note": base["vocabulary_note"],
        "claims": base["claims"],
        "non_contact_declaration": base["non_contact_declaration"],
    }

    blob = json.dumps(merged, ensure_ascii=False, separators=(",", ":"))
    with open(OUT, "w", encoding="utf-8", newline="") as f:
        f.write(blob)
    print("Wrote", OUT)
    print("windows_total=", windows_total, "windows_processed=", windows_processed, "handoff=", len(handoff_all))
    print("g5_classification_counts=", class_counts)
    print("alerts=", len(alerts_all))
    sha = hashlib.sha256(open(OUT, "rb").read()).hexdigest()
    print("sha256=", sha)

if __name__ == "__main__":
    main()
