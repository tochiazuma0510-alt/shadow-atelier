#!/usr/bin/env python3
"""Generate synthetic positive/mutant manifests for the independent join gate."""

from __future__ import annotations

import copy
import json
from pathlib import Path

FIXTURE_DIR = Path(__file__).parent / "join_fixtures"
COMMON = {
    "radix": 2,
    "exponent_width": 2,
    "m_values": [0, 2, 3],
    "f_total": 4,
    "pcgs_id": "toy-pcgs-sha256",
    "pcgs_basis_fingerprint": "f" * 64,
    "endian": "big",
    "class_id": "HS-TOY-CLASS-v2",
    "driver_digest": "toy-driver-sha256",
    "source_bundle_sha256": "toy-source-bundle-sha256",
}


def universe(lane: str) -> dict:
    return {**COMMON, "lane": lane, "axis": "f" if lane == "P" else "pair",
            "total_flat_indices": 4 if lane == "P" else 12}


def receipt(tag: str) -> dict:
    return {
        "run_id": f"toy-run-{tag}", "run_attempt": "1", "sha": f"toy-commit-{tag}",
        "driver_digest": COMMON["driver_digest"],
        "source_bundle_sha256": COMMON["source_bundle_sha256"],
        "class_id": COMMON["class_id"], "driver_done": True,
        "cert_sha256": f"toy-cert-{tag}-sha256",
    }


def exp(idx: int) -> list[int]:
    return [idx // 2, idx % 2]


def pair_entry(idx: int) -> dict:
    mi, fi = divmod(idx, 4)
    return {"flat_index": idx, "key": {"m": COMMON["m_values"][mi], "e": exp(fi)},
            "status": ("PASS", "FAIL", "UNKNOWN")[idx % 3]}


def p_entry(idx: int) -> dict:
    return {"flat_index": idx, "key": {"e": exp(idx)},
            "joined_pair_indices": [idx, 4 + idx, 8 + idx],
            "status": ("PASS", "FAIL", "UNKNOWN")[idx % 3]}


def shard(sid: str, lo: int, hi: int, entries: list[dict], tag: str) -> dict:
    return {"shard_id": sid, "index_range": [lo, hi], "pcgs_id": COMMON["pcgs_id"],
            "pcgs_basis_fingerprint": COMMON["pcgs_basis_fingerprint"],
            "endian": COMMON["endian"], "candidate_keys": entries, "receipt": receipt(tag)}


def good_s() -> dict:
    return {"universe": universe("S"), "shards": [
        shard("s0", 0, 3, [pair_entry(i) for i in range(0, 4)], "0"),
        shard("s1", 4, 7, [pair_entry(i) for i in range(4, 8)], "1"),
        shard("s2", 8, 11, [pair_entry(i) for i in range(8, 12)], "2"),
    ]}


def good_p() -> dict:
    return {"universe": universe("P"), "shards": [
        shard("p0", 0, 1, [p_entry(0), p_entry(1)], "p0"),
        shard("p1", 2, 3, [p_entry(2), p_entry(3)], "p1"),
    ]}


def mutate_good_s(mutator):
    obj = copy.deepcopy(good_s())
    mutator(obj)
    return obj


def reorder_s() -> dict:
    obj = copy.deepcopy(good_s())
    obj["shards"].reverse()
    for s in obj["shards"]:
        s["candidate_keys"].reverse()
    return obj


def missing_shard() -> dict:
    return mutate_good_s(lambda o: o["shards"].pop())


def missing_candidate_key() -> dict:
    return mutate_good_s(lambda o: o["shards"][1]["candidate_keys"].pop())


def duplicate_flat_index() -> dict:
    return mutate_good_s(lambda o: o["shards"][0]["candidate_keys"].append(copy.deepcopy(o["shards"][0]["candidate_keys"][0])))


def overlap() -> dict:
    return mutate_good_s(lambda o: o["shards"][1].update(index_range=[3, 7]))


def pcgs_endian_mismatch() -> dict:
    return mutate_good_s(lambda o: o["shards"][1].update(
        pcgs_id="wrong", pcgs_basis_fingerprint="e" * 64, endian="little"))


def entry_outside_range() -> dict:
    return mutate_good_s(lambda o: o["shards"][1]["candidate_keys"].append(pair_entry(3)))


def receipt_missing_field() -> dict:
    def mut(o):
        del o["shards"][1]["receipt"]["sha"]
    return mutate_good_s(mut)


def driver_not_done() -> dict:
    return mutate_good_s(lambda o: o["shards"][1]["receipt"].update(driver_done=False))


def common_permutation() -> dict:
    ## Producer and serialized key share the same e1/e2 reversal.  A checker
    ## that trusts the key would pass; arithmetic re-derivation must STOP.
    return mutate_good_s(lambda o: o["shards"][0]["candidate_keys"][1]["key"].update(e=[1, 0]))


def wrong_m_semantics() -> dict:
    return mutate_good_s(lambda o: o["shards"][1]["candidate_keys"][0]["key"].update(m=0))


def p_expansion_mismatch() -> dict:
    obj = copy.deepcopy(good_p())
    obj["shards"][0]["candidate_keys"][1]["joined_pair_indices"] = [1, 5, 10]
    return obj


def p_key_permutation() -> dict:
    obj = copy.deepcopy(good_p())
    obj["shards"][0]["candidate_keys"][1]["key"]["e"] = [1, 0]
    return obj


FIXTURES = {
    "good": (good_s, "PASS", None),
    "reorder": (reorder_s, "PASS", None),
    "good_p": (good_p, "PASS", None),
    "missing_shard": (missing_shard, "STOP", "COVERAGE_GAP"),
    "missing_candidate_key": (missing_candidate_key, "STOP", "CANDIDATE_KEY_MISSING"),
    "duplicate_key": (duplicate_flat_index, "STOP", "DUPLICATE_FLAT_INDEX"),
    "overlap": (overlap, "STOP", "INDEX_RANGE_OVERLAP"),
    "pcgs_endian_mismatch": (pcgs_endian_mismatch, "STOP", "PCGS_ENDIAN_MISMATCH"),
    "same_flat_index_different_key": (entry_outside_range, "STOP", "ENTRY_OUTSIDE_DECLARED_RANGE"),
    "receipt_missing_field": (receipt_missing_field, "STOP", "RECEIPT_FIELD_MISSING"),
    "driver_not_done": (driver_not_done, "STOP", "DRIVER_NOT_DONE"),
    "common_permutation": (common_permutation, "STOP", "SEMANTIC_KEY_MISMATCH"),
    "wrong_m_semantics": (wrong_m_semantics, "STOP", "SEMANTIC_KEY_MISMATCH"),
    "p_expansion_mismatch": (p_expansion_mismatch, "STOP", "P_EXPANSION_MISMATCH"),
    "p_key_permutation": (p_key_permutation, "STOP", "SEMANTIC_KEY_MISMATCH"),
}


def write_all() -> None:
    FIXTURE_DIR.mkdir(parents=True, exist_ok=True)
    expected = {f"{name}.json" for name in FIXTURES}
    for old in FIXTURE_DIR.glob("*.json"):
        if old.name not in expected:
            old.unlink()
    for name, (builder, _verdict, _reason) in FIXTURES.items():
        (FIXTURE_DIR / f"{name}.json").write_text(
            json.dumps(builder(), indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


if __name__ == "__main__":
    write_all()
