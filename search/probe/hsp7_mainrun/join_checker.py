#!/usr/bin/env python3
"""Independent fail-closed join checker for the HS P/S/V lane certificates.

This module imports no GAP/candidate-key helper.  It re-derives both maps

  flat pair index <-> (m,e1,...,ew)
  Lane-P f index -> every pair index sharing that f key

from arithmetic fields pinned in the manifest.  Consequently a common
permutation bug in a producer and its serialized key is not accepted merely
because the producer is internally self-consistent.
"""

from __future__ import annotations

import hashlib
import json
import sys
from typing import Any


class JoinCheckError(Exception):
    def __init__(self, reason: str, detail: dict[str, Any] | None = None):
        super().__init__(reason)
        self.reason = reason
        self.detail = detail or {}


REQUIRED_RECEIPT_FIELDS = (
    "run_id", "run_attempt", "sha", "driver_digest", "source_bundle_sha256",
    "class_id", "driver_done", "cert_sha256",
)
REQUIRED_SHARD_FIELDS = (
    "shard_id", "index_range", "pcgs_id", "pcgs_basis_fingerprint", "endian",
    "candidate_keys", "receipt",
)
REQUIRED_UNIVERSE_FIELDS = (
    "lane", "axis", "radix", "exponent_width", "m_values", "f_total",
    "total_flat_indices", "pcgs_id", "pcgs_basis_fingerprint", "endian", "class_id",
    "driver_digest", "source_bundle_sha256",
)


def _stop(reason: str, **detail: Any) -> None:
    raise JoinCheckError(reason, detail)


def _exp_from_f_index(idx: int, radix: int, width: int) -> list[int]:
    if not isinstance(idx, int) or isinstance(idx, bool):
        _stop("INVALID_FLAT_INDEX", flat_index=idx)
    e = [0] * width
    rem = idx
    for j in range(width - 1, -1, -1):
        e[j] = rem % radix
        rem //= radix
    if rem:
        _stop("INVALID_FLAT_INDEX", flat_index=idx)
    return e


def _expected_key(universe: dict[str, Any], flat_index: int) -> tuple[dict[str, Any], list[int] | None]:
    f_total = universe["f_total"]
    if universe["axis"] == "pair":
        m_index, f_index = divmod(flat_index, f_total)
        try:
            m = universe["m_values"][m_index]
        except IndexError:
            _stop("INVALID_FLAT_INDEX", flat_index=flat_index)
        return {
            "m": m,
            "e": _exp_from_f_index(f_index, universe["radix"], universe["exponent_width"]),
        }, None
    e = _exp_from_f_index(flat_index, universe["radix"], universe["exponent_width"])
    joined = [mi * f_total + flat_index for mi in range(len(universe["m_values"]))]
    return {"e": e}, joined


def _check_universe(manifest: dict[str, Any]) -> dict[str, Any]:
    u = manifest.get("universe")
    if not isinstance(u, dict):
        _stop("MISSING_UNIVERSE")
    missing = [k for k in REQUIRED_UNIVERSE_FIELDS if k not in u or u[k] in (None, "")]
    if missing:
        _stop("MISSING_UNIVERSE_FIELD", missing_fields=missing)
    if u["lane"] not in ("P", "S", "V"):
        _stop("INVALID_LANE", lane=u["lane"])
    expected_axis = "f" if u["lane"] == "P" else "pair"
    if u["axis"] != expected_axis:
        _stop("LANE_AXIS_MISMATCH", lane=u["lane"], axis=u["axis"], expected=expected_axis)
    if not isinstance(u["radix"], int) or u["radix"] < 2:
        _stop("INVALID_RADIX", radix=u["radix"])
    if not isinstance(u["exponent_width"], int) or u["exponent_width"] < 1:
        _stop("INVALID_EXPONENT_WIDTH", exponent_width=u["exponent_width"])
    if not isinstance(u["m_values"], list) or not u["m_values"] or len(set(u["m_values"])) != len(u["m_values"]):
        _stop("INVALID_M_VALUES", m_values=u["m_values"])
    if u["f_total"] != u["radix"] ** u["exponent_width"]:
        _stop("F_TOTAL_ARITHMETIC_MISMATCH", declared=u["f_total"], derived=u["radix"] ** u["exponent_width"])
    expected_total = u["f_total"] if u["axis"] == "f" else len(u["m_values"]) * u["f_total"]
    if u["total_flat_indices"] != expected_total:
        _stop("UNIVERSE_TOTAL_ARITHMETIC_MISMATCH", declared=u["total_flat_indices"], derived=expected_total)
    return u


def _check_shard_structure(shards: Any) -> list[dict[str, Any]]:
    if not isinstance(shards, list) or not shards:
        _stop("NO_SHARDS")
    ids: set[str] = set()
    for shard in shards:
        if not isinstance(shard, dict):
            _stop("MALFORMED_SHARD", shard=shard)
        missing = [k for k in REQUIRED_SHARD_FIELDS if k not in shard]
        if missing:
            _stop("MALFORMED_SHARD", shard_id=shard.get("shard_id"), missing_fields=missing)
        if shard["shard_id"] in ids:
            _stop("DUPLICATE_SHARD_ID", shard_id=shard["shard_id"])
        ids.add(shard["shard_id"])
    return shards


def _check_receipts(u: dict[str, Any], shards: list[dict[str, Any]]) -> None:
    for shard in shards:
        r = shard["receipt"]
        if not isinstance(r, dict):
            _stop("RECEIPT_FIELD_MISSING", shard_id=shard["shard_id"], note="receipt is not an object")
        missing = [k for k in REQUIRED_RECEIPT_FIELDS if k not in r or r[k] in (None, "")]
        if missing:
            _stop("RECEIPT_FIELD_MISSING", shard_id=shard["shard_id"], missing_fields=missing)
        if r["driver_done"] is not True:
            _stop("DRIVER_NOT_DONE", shard_id=shard["shard_id"], driver_done=r["driver_done"])
        for rk, uk in (("class_id", "class_id"), ("driver_digest", "driver_digest"),
                       ("source_bundle_sha256", "source_bundle_sha256")):
            if r[rk] != u[uk]:
                _stop("RECEIPT_BINDING_MISMATCH", shard_id=shard["shard_id"], field=rk,
                      expected=u[uk], actual=r[rk])


def _check_ranges(u: dict[str, Any], shards: list[dict[str, Any]]) -> None:
    n = u["total_flat_indices"]
    intervals: list[tuple[int, int, str]] = []
    for shard in shards:
        rng = shard["index_range"]
        if (not isinstance(rng, list) or len(rng) != 2 or
                any(not isinstance(x, int) or isinstance(x, bool) for x in rng) or
                rng[0] < 0 or rng[0] > rng[1] or rng[1] >= n):
            _stop("INVALID_INDEX_RANGE", shard_id=shard["shard_id"], index_range=rng)
        intervals.append((rng[0], rng[1], shard["shard_id"]))
    intervals.sort()
    nxt = 0
    for lo, hi, sid in intervals:
        if lo < nxt:
            _stop("INDEX_RANGE_OVERLAP", shard_id=sid, got_start=lo, expected_next=nxt)
        if lo > nxt:
            _stop("COVERAGE_GAP", shard_id=sid, got_start=lo, expected_next=nxt)
        nxt = hi + 1
    if nxt != n:
        _stop("COVERAGE_GAP", got_covered_upto=nxt, expected_total=n)


def _check_entries(u: dict[str, Any], shards: list[dict[str, Any]]) -> None:
    n = u["total_flat_indices"]
    seen: set[int] = set()
    for shard in shards:
        lo, hi = shard["index_range"]
        if (shard["pcgs_id"] != u["pcgs_id"] or
                shard["pcgs_basis_fingerprint"] != u["pcgs_basis_fingerprint"] or
                shard["endian"] != u["endian"]):
            _stop("PCGS_ENDIAN_MISMATCH", shard_id=shard["shard_id"])
        entries = shard["candidate_keys"]
        if not isinstance(entries, list):
            _stop("MALFORMED_CANDIDATE_KEYS", shard_id=shard["shard_id"])
        for entry in entries:
            if not isinstance(entry, dict) or "flat_index" not in entry or "key" not in entry or "status" not in entry:
                _stop("MALFORMED_CANDIDATE_KEY_ENTRY", shard_id=shard["shard_id"], entry=entry)
            fi = entry["flat_index"]
            if not isinstance(fi, int) or isinstance(fi, bool) or fi < 0 or fi >= n:
                _stop("INVALID_FLAT_INDEX", shard_id=shard["shard_id"], flat_index=fi)
            if not lo <= fi <= hi:
                _stop("ENTRY_OUTSIDE_DECLARED_RANGE", shard_id=shard["shard_id"], flat_index=fi, index_range=[lo, hi])
            if fi in seen:
                _stop("DUPLICATE_FLAT_INDEX", flat_index=fi)
            if entry["status"] not in ("PASS", "FAIL", "UNKNOWN"):
                _stop("INVALID_RESULT_STATUS", flat_index=fi, status=entry["status"])
            expected_key, expected_joined = _expected_key(u, fi)
            if entry["key"] != expected_key:
                _stop("SEMANTIC_KEY_MISMATCH", flat_index=fi, expected=expected_key, actual=entry["key"])
            if u["axis"] == "f":
                if entry.get("joined_pair_indices") != expected_joined:
                    _stop("P_EXPANSION_MISMATCH", flat_index=fi, expected=expected_joined,
                          actual=entry.get("joined_pair_indices"))
            elif "joined_pair_indices" in entry:
                _stop("UNEXPECTED_P_EXPANSION", flat_index=fi)
            seen.add(fi)
    if len(seen) != n:
        missing = sorted(set(range(n)) - seen)
        _stop("CANDIDATE_KEY_MISSING", expected_total=n, got_total=len(seen), missing_flat_indices=missing[:100],
              missing_count=len(missing))


def _canonical_form(u: dict[str, Any], shards: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "universe": {k: u[k] for k in REQUIRED_UNIVERSE_FIELDS},
        "shards": [
            {
                **{k: s[k] for k in ("shard_id", "index_range", "pcgs_id",
                                     "pcgs_basis_fingerprint", "endian")},
                "candidate_keys": sorted(s["candidate_keys"], key=lambda e: e["flat_index"]),
                "receipt": {k: s["receipt"][k] for k in REQUIRED_RECEIPT_FIELDS},
            }
            for s in sorted(shards, key=lambda s: (s["index_range"][0], s["shard_id"]))
        ],
    }


def check_join(manifest: dict[str, Any]) -> dict[str, Any]:
    try:
        u = _check_universe(manifest)
        shards = _check_shard_structure(manifest.get("shards"))
        _check_receipts(u, shards)
        _check_ranges(u, shards)
        _check_entries(u, shards)
        canon = _canonical_form(u, shards)
        digest = hashlib.sha256(json.dumps(canon, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
        counts = {"PASS": 0, "FAIL": 0, "UNKNOWN": 0}
        for s in shards:
            for e in s["candidate_keys"]:
                counts[e["status"]] += 1
        return {"verdict": "PASS", "reason": "complete_semantic_partition",
                "detail": {"lane": u["lane"], "total_flat_indices": u["total_flat_indices"],
                           "shard_count": len(shards), "status_counts": counts},
                "canonical_sort_hash": digest}
    except JoinCheckError as exc:
        return {"verdict": "STOP", "reason": exc.reason, "detail": exc.detail}


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: join_checker.py MANIFEST.json", file=sys.stderr)
        return 2
    try:
        with open(argv[1], encoding="utf-8") as f:
            manifest = json.load(f)
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"verdict": "STOP", "reason": "INPUT_JSON_ERROR", "detail": {"error": str(exc)}}))
        return 1
    result = check_join(manifest)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["verdict"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
