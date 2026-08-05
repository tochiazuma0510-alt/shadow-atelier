#!/usr/bin/env python3
"""Pure fail-closed binding checks shared by HS runner/workflow/tests.

No GAP import, group construction, candidate generation, or subprocess call
occurs in this module.  Every function returns named Boolean checks; callers
must require ``all(checks.values())`` and treat any false value as STOP.
"""

from __future__ import annotations

import gzip
import hashlib
import json
import re
from pathlib import Path
from typing import Any

PCGS_BASIS_CONTRACT = "hsp7-ordered-pcgs-material/v1"
FREEZE_SENTINEL = "UNSET_REQUIRES_FREEZE"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def manifest_self_digest(manifest: dict[str, Any]) -> str:
    obj = dict(manifest)
    obj.pop("manifest_sha256", None)
    obj["shards"] = sorted(obj.get("shards", []), key=lambda s: s.get("lo", -1))
    return sha256_bytes(json.dumps(obj, sort_keys=True, separators=(",", ":")).encode())


def pcgs_basis_fingerprint(material: dict[str, Any]) -> str:
    canonical = json.dumps(material, sort_keys=True, separators=(",", ":")).encode("ascii")
    return sha256_bytes(canonical)


def normalized_workflow_template_bytes(data: bytes) -> bytes:
    """Canonicalize only the two post-freeze workflow sentinel values.

    This avoids the class-manifest/workflow fixed point: the class binds all
    workflow bytes except the approved path/SHA literal substitutions, while
    the installed workflow still binds the final class file exactly at run
    time.
    """
    text = data.decode("utf-8").replace("\r\n", "\n").replace("\r", "\n")
    for key in ("FROZEN_CLASS_MANIFEST_PATH", "FROZEN_CLASS_MANIFEST_SHA256"):
        pattern = rf"(?m)^(\s*{key}:\s*).*$"
        text, count = re.subn(pattern, rf"\g<1>{FREEZE_SENTINEL}", text)
        if count != 1:
            raise ValueError(f"workflow template must contain exactly one {key}, got {count}")
    return text.encode("utf-8")


def workflow_template_digest(data: bytes) -> str:
    return sha256_bytes(normalized_workflow_template_bytes(data))


def pcgs_basis_material_checks(material: Any, lane: str,
                               expected_source_artifact_path: str | None = None,
                               expected_source_artifact_sha256: str | None = None) -> dict[str, bool]:
    """Validate the ordered-runtime-basis identity material.

    In this class-4 rank-2 group ``D=[P,P]`` is abelian: all fifteen
    pair-commutator rows are therefore expected to be zero.  They remain in
    the material as mathematically meaningful identity data, while the
    non-self-relational anchor is supplied by the source-artifact digest and
    the ambient ``Pcgs(P)`` coordinates of named ``x,y`` and the ordered six
    generators of ``D``.
    """
    expected_keys = {
        "ambient_named_generator_coordinates", "ambient_pcgs_relative_orders",
        "contract", "ordered_basis_in_ambient_coordinates",
        "relative_orders", "pair_commutator_coordinates", "source_artifact",
        "theta_image_coordinates", "tau_image_coordinates",
        "s_to_v_bridge_coordinates",
    }
    is_obj = isinstance(material, dict)
    obj = material if is_obj else {}

    def coords(value: Any, width: int = 6) -> bool:
        return (isinstance(value, list) and len(value) == width
                and all(isinstance(x, int) and not isinstance(x, bool) and 0 <= x < 7
                        for x in value))

    pair_rows = obj.get("pair_commutator_coordinates")
    pair_rows = pair_rows if isinstance(pair_rows, list) else []
    expected_pairs = [(i, j) for i in range(1, 7) for j in range(i + 1, 7)]
    pair_shape = len(pair_rows) == 15 and all(
        isinstance(row, dict) and set(row) == {"i", "j", "coordinates"}
        and (row.get("i"), row.get("j")) == expected_pairs[k]
        and coords(row.get("coordinates"))
        for k, row in enumerate(pair_rows))

    def action_rows(name: str) -> tuple[bool, list[dict[str, Any]]]:
        rows = obj.get(name)
        rows = rows if isinstance(rows, list) else []
        ok = len(rows) == 6 and all(
            isinstance(row, dict) and set(row) == {"i", "coordinates"}
            and row.get("i") == k + 1 and coords(row.get("coordinates"))
            for k, row in enumerate(rows))
        return ok, rows

    theta_shape, theta_rows = action_rows("theta_image_coordinates")
    tau_shape, tau_rows = action_rows("tau_image_coordinates")
    bridge_shape, bridge_rows = action_rows("s_to_v_bridge_coordinates")
    if lane != "V":
        raw_bridge = obj.get("s_to_v_bridge_coordinates")
        bridge_shape = isinstance(raw_bridge, list) and raw_bridge == []
        bridge_rows = []

    units = [[1 if i == j else 0 for j in range(6)] for i in range(6)]
    pair_identity = pair_shape and all(row["coordinates"] == [0] * 6
                                       for row in pair_rows)
    theta_nonidentity = theta_shape and any(row["coordinates"] != units[i]
                                             for i, row in enumerate(theta_rows))
    tau_nonidentity = tau_shape and any(row["coordinates"] != units[i]
                                         for i, row in enumerate(tau_rows))
    theta_rows_unique = theta_shape and len({tuple(r["coordinates"]) for r in theta_rows}) == 6
    tau_rows_unique = tau_shape and len({tuple(r["coordinates"]) for r in tau_rows}) == 6

    def rank_mod7(rows: list[dict[str, Any]]) -> int:
        matrix = [list(row["coordinates"]) for row in rows]
        rank = 0
        for col in range(6):
            pivot = next((r for r in range(rank, len(matrix))
                          if matrix[r][col] % 7), None)
            if pivot is None:
                continue
            matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
            inv = pow(matrix[rank][col] % 7, -1, 7)
            matrix[rank] = [(x * inv) % 7 for x in matrix[rank]]
            for r in range(len(matrix)):
                if r != rank and matrix[r][col] % 7:
                    factor = matrix[r][col] % 7
                    matrix[r] = [(a - factor * b) % 7
                                 for a, b in zip(matrix[r], matrix[rank])]
            rank += 1
        return rank

    theta_invertible = theta_shape and rank_mod7(theta_rows) == 6
    tau_invertible = tau_shape and rank_mod7(tau_rows) == 6
    bridge_units = (bridge_shape and (lane != "V" or
                    all(row["coordinates"] == units[i] for i, row in enumerate(bridge_rows))))
    ambient_orders = obj.get("ambient_pcgs_relative_orders")
    ambient_named = obj.get("ambient_named_generator_coordinates")
    ambient_named = ambient_named if isinstance(ambient_named, list) else []
    ambient_named_shape = (len(ambient_named) == 2
                           and [r.get("name") for r in ambient_named
                                if isinstance(r, dict)] == ["x", "y"]
                           and all(isinstance(r, dict)
                                   and set(r) == {"name", "coordinates"}
                                   and coords(r.get("coordinates"), 8)
                                   for r in ambient_named))
    ambient_named_nontrivial = (ambient_named_shape
                                and ambient_named[0]["coordinates"] != [0] * 8
                                and ambient_named[1]["coordinates"] != [0] * 8
                                and ambient_named[0]["coordinates"] !=
                                ambient_named[1]["coordinates"])
    ambient_basis = obj.get("ordered_basis_in_ambient_coordinates")
    ambient_basis = ambient_basis if isinstance(ambient_basis, list) else []
    ambient_basis_shape = len(ambient_basis) == 6 and all(
        isinstance(row, dict) and set(row) == {"i", "coordinates"}
        and row.get("i") == i + 1 and coords(row.get("coordinates"), 8)
        for i, row in enumerate(ambient_basis))
    ambient_basis_unique = (ambient_basis_shape
                            and len({tuple(r["coordinates"]) for r in ambient_basis}) == 6)
    ambient_basis_nonzero = (ambient_basis_shape
                             and all(r["coordinates"] != [0] * 8 for r in ambient_basis))
    source_artifact = obj.get("source_artifact")
    source_artifact = source_artifact if isinstance(source_artifact, dict) else {}
    source_path = source_artifact.get("path")
    source_sha = source_artifact.get("sha256")
    source_shape = (set(source_artifact) == {"path", "sha256"}
                    and isinstance(source_path, str) and bool(source_path)
                    and isinstance(source_sha, str)
                    and re.fullmatch(r"[0-9a-f]{64}", source_sha) is not None)
    source_expected = ((expected_source_artifact_path is None
                        or source_path == expected_source_artifact_path)
                       and (expected_source_artifact_sha256 is None
                            or source_sha == expected_source_artifact_sha256))
    return {
        "pcgs_material_object": is_obj,
        "pcgs_material_exact_keys": is_obj and set(obj) == expected_keys,
        "pcgs_material_contract": obj.get("contract") == PCGS_BASIS_CONTRACT,
        "pcgs_ambient_relative_orders": ambient_orders == [7] * 8,
        "pcgs_ambient_named_shape": ambient_named_shape,
        "pcgs_ambient_named_nontrivial": ambient_named_nontrivial,
        "pcgs_ambient_basis_shape": ambient_basis_shape,
        "pcgs_ambient_basis_unique": ambient_basis_unique,
        "pcgs_ambient_basis_nonzero": ambient_basis_nonzero,
        "pcgs_source_artifact_shape": source_shape,
        "pcgs_source_artifact_expected": source_shape and source_expected,
        "pcgs_relative_orders": obj.get("relative_orders") == [7, 7, 7, 7, 7, 7],
        "pcgs_pair_rows_shape": pair_shape,
        "pcgs_pair_rows_identity_expected": pair_identity,
        "pcgs_theta_rows_shape": theta_shape,
        "pcgs_theta_nonidentity": theta_nonidentity,
        "pcgs_theta_rows_unique": theta_rows_unique,
        "pcgs_theta_invertible": theta_invertible,
        "pcgs_tau_rows_shape": tau_shape,
        "pcgs_tau_nonidentity": tau_nonidentity,
        "pcgs_tau_rows_unique": tau_rows_unique,
        "pcgs_tau_invertible": tau_invertible,
        "pcgs_bridge_shape": bridge_shape,
        "pcgs_bridge_pointwise_units": bridge_units,
    }


def lane_record_checks(records: Any, lane: str,
                       index_range: list[int] | None = None) -> dict[str, bool]:
    """Check lane-specific record semantics absent from the generic schema."""
    rows = records if isinstance(records, list) else []

    def integer(value: Any) -> bool:
        return isinstance(value, int) and not isinstance(value, bool)

    def exp6(value: Any) -> bool:
        return (isinstance(value, list) and len(value) == 6
                and all(integer(x) and 0 <= x < 7 for x in value))

    def boolean(value: Any) -> bool:
        return isinstance(value, bool)

    def row_ok(row: Any) -> bool:
        if (not isinstance(row, dict) or not isinstance(row.get("fixture_id"), str)
                or not row["fixture_id"]):
            return False
        unknown = row.get("status") == "UNKNOWN"
        if unknown and (not isinstance(row.get("unknown_reason"), str)
                        or not row["unknown_reason"]):
            return False
        if lane in ("S", "V"):
            key = row.get("candidate_key", {})
            base = (integer(row.get("pair_index")) and integer(row.get("f_index"))
                    and isinstance(key, dict) and set(key) == {"m", "e"}
                    and key.get("m") in [0, 1, 2, 4, 5, 6]
                    and exp6(key.get("e"))
                    and row["f_index"] == sum(key["e"][i] * 7 ** (5 - i)
                                               for i in range(6))
                    and row["pair_index"] == [0, 1, 2, 4, 5, 6].index(key["m"]) * 117649
                    + row["f_index"])
            if unknown:
                return base
            if lane == "S":
                return (base and all(boolean(row.get(k))
                                     for k in ("hex310", "hex311", "verdict"))
                        and row["verdict"] == (row["hex310"] and row["hex311"]))
            n, n0 = row.get("N", {}), row.get("N0", {})
            return (base and isinstance(n, dict) and isinstance(n0, dict)
                    and all(boolean(n.get(k)) and boolean(n0.get(k))
                            for k in ("hex33", "hex34", "verdict"))
                    and n["verdict"] == (n["hex33"] and n["hex34"])
                    and n0["verdict"] == (n0["hex33"] and n0["hex34"])
                    and row.get("N_N0_agree") is True
                    and n["verdict"] == n0["verdict"]
                    and row.get("CF_baseline_agree") is True)
        if lane != "P":
            return False
        key = row.get("f_key", {})
        base = (integer(row.get("f_index")) and isinstance(key, dict)
                and set(key) == {"e"} and exp6(key.get("e"))
                and row["f_index"] == sum(key["e"][i] * 7 ** (5 - i)
                                           for i in range(6)))
        if unknown:
            return base
        joined = row.get("joined_pair_indices")
        return (base and isinstance(joined, list)
                and joined == [row["f_index"] + i * 117649 for i in range(6)]
                and boolean(row.get("pentagon_verdict"))
                and row.get("CONV_native_element_agree") is True
                and row.get("CONV_native_verdict_agree") is True)

    shape_ok = isinstance(records, list) and all(row_ok(row) for row in rows)
    exact_indices = True
    if (isinstance(index_range, list) and len(index_range) == 2
            and all(integer(x) for x in index_range) and index_range[0] >= 0):
        field = "f_index" if lane == "P" else "pair_index"
        exact_indices = [r.get(field) for r in rows if isinstance(r, dict)] == list(
            range(index_range[0], index_range[1] + 1))
    return {"axis_record_shape": shape_ok, "axis_record_exact_indices": exact_indices}


def class_lock_checks(*, class_bytes: bytes, class_obj: dict[str, Any],
                      actual_path: str, expected_path: str,
                      expected_sha256: str, required_status: str) -> dict[str, bool]:
    paths_ok = isinstance(actual_path, str) and isinstance(expected_path, str)
    authorization = class_obj.get("authorization", {})
    authorization = authorization if isinstance(authorization, dict) else {}
    return {
        "class_schema": class_obj.get("schema") == "hsp7-class-manifest-draft/v1",
        "class_path": paths_ok and Path(actual_path).as_posix() == Path(expected_path).as_posix(),
        "class_sha256": sha256_bytes(class_bytes) == expected_sha256,
        "class_status": class_obj.get("status") == required_status,
        "class_authorization_main_run": authorization.get("main_run") is True,
        "class_authorization_workflow_dispatch": authorization.get("workflow_dispatch") is True,
    }


def manifest_binding_checks(*, class_obj: dict[str, Any], manifest_obj: dict[str, Any],
                            manifest_bytes: bytes, actual_manifest_path: str,
                            lane: str, live_source_bundle_sha256: str) -> dict[str, bool]:
    lanes = class_obj.get("lanes", {})
    lane_row = lanes.get(lane, {}) if isinstance(lanes, dict) else {}
    lane_row = lane_row if isinstance(lane_row, dict) else {}
    partition = lane_row.get("partition", {})
    partition = partition if isinstance(partition, dict) else {}
    expected_total = 117649 if lane == "P" else 705894
    expected_size = {"S": 3678, "V": 54000, "P": 3678}.get(lane)
    expected_semantics = {
        "radix": 7, "exponent_width": 6, "m_values": [0, 1, 2, 4, 5, 6],
        "f_total": 117649, "axis": "f" if lane == "P" else "pair",
    }
    shards = manifest_obj.get("shards", [])
    shards_are_rows = isinstance(shards, list) and all(isinstance(s, dict) for s in shards)
    try:
        sorted_shards = sorted(shards, key=lambda s: s.get("lo", -1)) if shards_are_rows else []
    except TypeError:
        sorted_shards = []
    names_ok = bool(sorted_shards) and len({s.get("name") for s in sorted_shards}) == len(sorted_shards)
    cover_ok = bool(sorted_shards)
    nxt = 0
    for i, shard in enumerate(sorted_shards):
        lo, hi = shard.get("lo"), shard.get("hi")
        if (shard.get("name") != f"shard_{i:05d}" or lo != nxt or
                not isinstance(lo, int) or isinstance(lo, bool) or
                not isinstance(hi, int) or isinstance(hi, bool) or hi < lo):
            cover_ok = False
            break
        nxt = hi + 1
    cover_ok = cover_ok and nxt == manifest_obj.get("total_candidates")
    expected_manifest_path = lane_row.get("shard_manifest")
    paths_ok = isinstance(actual_manifest_path, str) and isinstance(expected_manifest_path, str)
    try:
        self_digest_ok = manifest_obj.get("manifest_sha256") == manifest_self_digest(manifest_obj)
    except (KeyError, TypeError, ValueError):
        self_digest_ok = False
    class_exact = class_obj.get("exact_universe", {})
    class_exact = class_exact if isinstance(class_exact, dict) else {}
    capacity = class_obj.get("capacity", {})
    capacity = capacity if isinstance(capacity, dict) else {}
    lane_caps = capacity.get("per_lane_compressed_cap_bytes", {})
    lane_caps = lane_caps if isinstance(lane_caps, dict) else {}
    frozen_fp = lane_row.get("pcgs_basis_fingerprint")
    fp_shape = isinstance(frozen_fp, str) and re.fullmatch(r"[0-9a-f]{64}", frozen_fp) is not None
    return {
        "manifest_schema": manifest_obj.get("schema") == "hsp7-mainrun-shard-manifest/v2",
        "manifest_lane": manifest_obj.get("lane") == lane,
        "manifest_path": paths_ok and Path(actual_manifest_path).as_posix() == Path(expected_manifest_path).as_posix(),
        "manifest_file_sha256": sha256_bytes(manifest_bytes) == lane_row.get("shard_manifest_file_sha256"),
        "manifest_self_sha256": self_digest_ok,
        "class_id": manifest_obj.get("class_id") == class_obj.get("class_id"),
        "source_bundle_class": manifest_obj.get("source_bundle_sha256") == lane_row.get("source_bundle_sha256"),
        "source_bundle_live": manifest_obj.get("source_bundle_sha256") == live_source_bundle_sha256,
        "driver_digest": manifest_obj.get("frozen_driver_digest") == live_source_bundle_sha256,
        "partition_total": manifest_obj.get("total_candidates") == partition.get("total") == expected_total,
        "partition_size": manifest_obj.get("shard_size_target") == partition.get("target_size") == expected_size,
        "partition_count": manifest_obj.get("n_shards") == partition.get("n_shards") == len(shards),
        "timeout": manifest_obj.get("timeout_min") == partition.get("timeout_min") == 60,
        "max_parallel": manifest_obj.get("max_parallel") == partition.get("max_parallel") == 20,
        "max_jobs": manifest_obj.get("max_jobs_per_workflow") == 256 and len(shards) <= 256,
        "lane_compressed_cap": (lane_row.get("compressed_cap_bytes") ==
                                lane_caps.get(lane)),
        "key_semantics": manifest_obj.get("key_semantics") == expected_semantics,
        "endian": manifest_obj.get("endian") == "big",
        "pcgs_source_artifact": manifest_obj.get("pcgs_id") == class_obj.get("exact_universe", {}).get("pcgs_id"),
        "pcgs_basis_contract": (manifest_obj.get("pcgs_basis_contract") == PCGS_BASIS_CONTRACT
                                == class_exact.get("pcgs_basis_contract")),
        "pcgs_basis_fingerprint": manifest_obj.get("pcgs_basis_fingerprint") == frozen_fp,
        "pcgs_source_artifact_path": (manifest_obj.get("pcgs_source_artifact_path") ==
                                      class_exact.get("pcgs_source_artifact_path")),
        "pcgs_source_artifact_sha256": (manifest_obj.get("pcgs_source_artifact_sha256") ==
                                        class_exact.get("pcgs_source_artifact_sha256")),
        "pcgs_basis_fingerprint_frozen_ready": class_obj.get("status") != "FROZEN_AUTHORIZED" or fp_shape,
        "shard_names_unique": names_ok,
        "shard_exact_cover": cover_ok,
    }


def cert_binding_checks(*, cert: dict[str, Any], lane: str, axis: str,
                        universe_total: int, class_id: str,
                        run_id: str, run_attempt: str, commit_sha: str,
                        source_bundle_sha256: str, wrapper_sha256: str,
                        predicate_sha256: str, aux_sha256: str,
                        schema_sha256: str, index_range: list[int],
                        expected_count: int,
                        expected_pcgs_basis_fingerprint: str,
                        expected_pcgs_source_artifact_path: str,
                        expected_pcgs_source_artifact_sha256: str) -> dict[str, bool]:
    source = cert.get("source_bindings", {})
    source = source if isinstance(source, dict) else {}
    run = cert.get("run", {})
    run = run if isinstance(run, dict) else {}
    summary = cert.get("summary", {})
    summary = summary if isinstance(summary, dict) else {}
    records = cert.get("records", [])
    records_list = records if isinstance(records, list) else []
    actual_unknown = sum(1 for row in records_list
                         if isinstance(row, dict) and row.get("status") == "UNKNOWN")
    unknown_count = summary.get("unknown_count")
    run_id_ok = isinstance(run_id, str) and re.fullmatch(r"[1-9][0-9]*", run_id) is not None
    run_attempt_ok = (isinstance(run_attempt, str)
                      and re.fullmatch(r"[1-9][0-9]*", run_attempt) is not None)
    commit_ok = (isinstance(commit_sha, str)
                 and re.fullmatch(r"[0-9a-fA-F]{40}|[0-9a-fA-F]{64}", commit_sha) is not None)
    material = cert.get("pcgs_basis_material")
    material_checks = pcgs_basis_material_checks(
        material, lane, expected_pcgs_source_artifact_path,
        expected_pcgs_source_artifact_sha256)
    computed_fp = pcgs_basis_fingerprint(material) if isinstance(material, dict) else None
    checks = {
        "schema": cert.get("schema") == "hsp7-lane-cert/v3",
        "lane": cert.get("lane") == lane,
        "axis": cert.get("axis") == axis,
        "universe_total": cert.get("universe_total") == universe_total,
        "class_id": cert.get("class_id") == class_id,
        "run_id": run_id_ok and run.get("run_id") == run_id,
        "run_attempt": run_attempt_ok and run.get("run_attempt") == run_attempt,
        "commit_sha": commit_ok and run.get("commit_sha") == commit_sha,
        "source_bundle_sha256": source.get("source_bundle_sha256") == source_bundle_sha256,
        "wrapper_sha256": source.get("wrapper_sha256") == wrapper_sha256,
        "predicate_sha256": source.get("predicate_sha256") == predicate_sha256,
        "aux_sha256": source.get("aux_sha256") == aux_sha256,
        "schema_sha256": source.get("schema_sha256") == schema_sha256,
        "pcgs_basis_fingerprint_self": cert.get("pcgs_basis_fingerprint") == computed_fp,
        "pcgs_basis_fingerprint_frozen": (isinstance(expected_pcgs_basis_fingerprint, str)
                                           and cert.get("pcgs_basis_fingerprint") ==
                                           expected_pcgs_basis_fingerprint),
        "range": cert.get("evaluated_range") == index_range,
        "records_is_list": isinstance(records, list),
        "count": isinstance(records, list) and summary.get("evaluated_count") == expected_count == len(records_list),
        "unknown_count_type": isinstance(unknown_count, int) and not isinstance(unknown_count, bool) and unknown_count >= 0,
        "unknown_count_consistency": unknown_count == actual_unknown,
        "integrity": summary.get("integrity_ok") is True,
        "driver_done": cert.get("driver_done") is True,
    }
    checks.update(material_checks)
    checks.update(lane_record_checks(records, lane, index_range))
    return checks


def receipt_cert_checks(*, receipt: dict[str, Any] | None, cert_bytes: bytes | None,
                        per_shard_raw_cap: int) -> dict[str, bool]:
    has_receipt = isinstance(receipt, dict)
    has_cert = isinstance(cert_bytes, bytes)
    actual_sha = sha256_bytes(cert_bytes) if has_cert else None
    raw_bytes = len(cert_bytes) if has_cert else None
    gzip_bytes = len(gzip.compress(cert_bytes, compresslevel=6, mtime=0)) if has_cert else None
    return {
        "receipt_present": has_receipt,
        "receipt_pass": has_receipt and receipt.get("status") == "PASS" and receipt.get("reason") == "exact-shard-complete",
        "cert_present": has_cert,
        "cert_sha256": has_receipt and has_cert and receipt.get("cert_sha256") == actual_sha,
        "raw_bytes_receipt": has_receipt and has_cert and receipt.get("raw_bytes") == raw_bytes,
        "gzip_bytes_receipt": has_receipt and has_cert and receipt.get("gzip_bytes") == gzip_bytes,
        "per_shard_raw_cap": has_cert and raw_bytes <= per_shard_raw_cap,
    }


def receipt_binding_checks(*, receipt: dict[str, Any], lane: str, class_id: str,
                           class_manifest_path: str, class_manifest_sha256: str,
                           manifest_path: str, manifest_sha256: str,
                           source_bundle_sha256: str, shard_id: str,
                           index_range: list[int],
                           expected_pcgs_basis_fingerprint: str) -> dict[str, bool]:
    """Bind a job receipt to its exact frozen class/lane/shard inputs."""
    def path_equal(value: Any, expected: str) -> bool:
        return isinstance(value, str) and Path(value).as_posix() == Path(expected).as_posix()

    return {
        "receipt_schema": receipt.get("schema") == "hsp7-lane-job-receipt/v1",
        "receipt_lane": receipt.get("lane") == lane,
        "receipt_class_id": receipt.get("class_id") == class_id,
        "receipt_class_manifest_path": path_equal(receipt.get("class_manifest"), class_manifest_path),
        "receipt_class_manifest_sha256": receipt.get("class_manifest_sha256") == class_manifest_sha256,
        "receipt_manifest_path": path_equal(receipt.get("manifest"), manifest_path),
        "receipt_manifest_sha256": receipt.get("manifest_sha256") == manifest_sha256,
        "receipt_source_bundle_sha256": receipt.get("source_bundle_sha256") == source_bundle_sha256,
        "receipt_shard_id": receipt.get("shard_id") == shard_id,
        "receipt_index_range": receipt.get("index_range") == index_range,
        "receipt_runtime_pcgs_preflight": receipt.get("runtime_pcgs_preflight") == "PASS",
        "receipt_runtime_pcgs_fingerprint": (
            receipt.get("measured_pcgs_basis_fingerprint") ==
            expected_pcgs_basis_fingerprint),
    }


def collection_capacity_checks(*, receipts: list[dict[str, Any]],
                               expected_receipt_count: int,
                               collection_gzip_cap: int,
                               expected_shard_ids: set[str] | None = None) -> dict[str, bool]:
    rows_are_dicts = all(isinstance(r, dict) for r in receipts)
    gzip_values = [r.get("gzip_bytes") for r in receipts] if rows_are_dicts else []
    gzip_ok = all(isinstance(v, int) and not isinstance(v, bool) and v >= 0
                  for v in gzip_values)
    cap_ok = (isinstance(collection_gzip_cap, int)
              and not isinstance(collection_gzip_cap, bool)
              and collection_gzip_cap > 0)
    total_gzip = sum(gzip_values) if gzip_ok else ((collection_gzip_cap + 1) if cap_ok else 1)
    actual_ids = [r.get("shard_id") for r in receipts] if rows_are_dicts else []
    ids_are_strings = all(isinstance(v, str) for v in actual_ids)
    shard_set_ok = (True if expected_shard_ids is None else
                    ids_are_strings and len(actual_ids) == len(set(actual_ids))
                    and set(actual_ids) == expected_shard_ids)
    return {
        "receipt_count": len(receipts) == expected_receipt_count,
        "all_receipts_pass": rows_are_dicts and all(
            r.get("status") == "PASS" and r.get("reason") == "exact-shard-complete"
            for r in receipts),
        "exact_unique_shard_set": shard_set_ok,
        "gzip_values_nonnegative": gzip_ok,
        "collection_gzip_cap_shape": cap_ok,
        "collection_gzip_cap": cap_ok and total_gzip <= collection_gzip_cap,
    }


def class_lane_capacity_checks(capacity: Any) -> dict[str, bool]:
    """Ensure lane collection caps compose into the advertised class cap."""
    obj = capacity if isinstance(capacity, dict) else {}
    whole = obj.get("whole_class_compressed_cap_bytes")
    lane_caps = obj.get("per_lane_compressed_cap_bytes")
    recorded_sum = obj.get("per_lane_cap_sum_bytes")
    whole_ok = isinstance(whole, int) and not isinstance(whole, bool) and whole > 0
    lanes_ok = isinstance(lane_caps, dict) and set(lane_caps) == {"S", "V", "P"}
    values_ok = lanes_ok and all(
        isinstance(lane_caps[lane], int) and not isinstance(lane_caps[lane], bool)
        and lane_caps[lane] > 0 for lane in ("S", "V", "P"))
    actual_sum = sum(lane_caps.values()) if values_ok else None
    return {
        "whole_class_cap_shape": whole_ok,
        "lane_cap_keys": lanes_ok,
        "lane_cap_values": values_ok,
        "lane_cap_sum_recorded": (values_ok and isinstance(recorded_sum, int)
                                  and not isinstance(recorded_sum, bool)
                                  and recorded_sum == actual_sum),
        "lane_cap_sum_within_class": values_ok and whole_ok and actual_sum <= whole,
    }
