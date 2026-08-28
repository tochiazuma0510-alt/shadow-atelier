#!/usr/bin/env python3
"""Helper-nonshared checker for the task197 lossless conversion."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "d972-r07-cached-v3-task193-compat-adapter/v1"
SELF = SCHEMA + "/selftest"
COMMON = "R07_CACHED_V3_TASK193_COMPAT_ADAPTER_V1"
V3_SCHEMA = "d972-r07-normalized-exact-cached-colgen/v3"
V3_COMMON = "R07_NORMALIZED_EXACT_CACHED_COLGEN_V3_COMMON_WORD"
V2_SCHEMA = "d972-r07-normalized-exact-common-word-colgen/v2"
V2_COMMON = "R07_NORMALIZED_EXACT_COMMON_WORD_COLGEN_V2_COMMON_WORD"
V3_LINE = "R07_NORMALIZED_EXACT_CACHED_COLGEN_V3_CHECKER_PASS terminal=" + V3_COMMON
V2_LINE = "R07_NORMALIZED_EXACT_COMMON_WORD_COLGEN_V2_CHECKER_PASS terminal=" + V2_COMMON
SELF_V3_LINE = "V3_CHECKER_PLACEHOLDER type=SELFTEST terminal=" + V3_COMMON
SELF_V2_LINE = "V2_CHECKER_PLACEHOLDER type=SELFTEST terminal=" + V2_COMMON

PROD_PATHS = {
    "v3_attestation": "ci/out/d972_r07_cached_v3_task193_compat_adapter_v1.v3.attestation",
    "v2_receipt": "ci/out/d972_r07_cached_v3_task193_compat_adapter_v1.task193_compatible_v2.json",
    "v2_attestation": "ci/out/d972_r07_cached_v3_task193_compat_adapter_v1.v2.attestation",
    "prepared": "ci/out/d972_r07_cached_v3_task193_compat_adapter_v1.prepared.json",
    "certificate": "ci/out/d972_r07_cached_v3_task193_compat_adapter_v1.adapter_certificate_v1.json",
}
SELF_PATHS = {
    "v3_receipt": "ci/out/d972_r07_cached_v3_task193_compat_adapter_v1.selftest.v3.json",
    "v3_attestation": "ci/out/d972_r07_cached_v3_task193_compat_adapter_v1.selftest.v3.attestation",
    "v2_receipt": "ci/out/d972_r07_cached_v3_task193_compat_adapter_v1.selftest.v2.json",
    "v2_attestation": "ci/out/d972_r07_cached_v3_task193_compat_adapter_v1.selftest.v2.attestation",
    "prepared": "ci/out/d972_r07_cached_v3_task193_compat_adapter_v1.selftest.prepared.json",
    "certificate": "ci/out/d972_r07_cached_v3_task193_compat_adapter_v1.selftest.certificate.json",
    "summary": "ci/out/d972_r07_cached_v3_task193_compat_adapter_v1.selftest.json",
}
FIXTURE = ROOT / "search/certs/d972_r07_cached_v3_task193_compat_adapter_selftest_v1_20260828.json"

# Refreshed only after the task192 owner declares its three files stable.
PINS = {
    "task192_producer": ("search/d972_r07_normalized_exact_common_word_cached_v3.py", 193704, "f27b4971351832b8730fb8cce4e782e893a958dfb850203cc735c7bc3aa31f37"),
    "task192_checker": ("crosscheck/check_d972_r07_normalized_exact_common_word_cached_v3.py", 154009, "dfc8cbbd96a1da45f15e01607ed343b66a78a7201f4a80952fba33aaeb361e10"),
    "task192_driver": ("search/d972_r07_normalized_exact_common_word_cached_gha_driver_v3.g", 11548, "2f7ff7b459e46d014268907ff5ba5f03c035836e8f8df79a2c5f4cdc3b75351d"),
    "task192_fixture": ("search/certs/d972_r07_normalized_exact_common_word_cached_selftest_v3_20260827.json", 276, "c49f434ad3daf1cc661ba45563dbb9557d436f91dca78c8ee0f47ed70332da12"),
    "task186_producer": ("search/d972_r07_normalized_exact_common_word_colgen_v2.py", 63053, "ec73db0a474b3b52d69e19862e8185ae22423b2406f3922b5669d9a4e85fafab"),
    "task186_checker": ("crosscheck/check_d972_r07_normalized_exact_common_word_colgen_v2.py", 54982, "8898798d0d6a9e0b6cd67402e74ba0dc5048b4797a0f7a9657e58d70d553c488"),
    "task186_driver": ("search/d972_r07_normalized_exact_common_word_colgen_gha_driver_v2.g", 9630, "a1c0fc034b127174e5c5795347648db0629314262b9e59689705e887371a7e4e"),
    "task186_fixture": ("search/certs/d972_r07_normalized_exact_common_word_colgen_selftest_v2_20260827.json", 234, "34dd389d9a3aff50486e57137f8dafea7b14825baec13e3288ed595046940963"),
    "task193_producer": ("search/d972_r07_second_frattini_affine_prefix_compiler_v1.py", 37956, "7ec85fe5b359a371e7c7c6b701426c5521d2a9651f560cba0193fa9c34aa2530"),
    "task193_checker": ("crosscheck/check_d972_r07_second_frattini_affine_prefix_compiler_v1.py", 33149, "278903c62c8f742cb985f44267f5f428c12dac9c514117f91eb6ae0daea17940"),
    "task193_driver": ("search/d972_r07_second_frattini_affine_prefix_compiler_gha_driver_v1.g", 9799, "4ad4231c7e1f10006bd27f4ff8877ebe7ed60dd44a97a6188392234ec0f548ec"),
    "task197_contract": ("sol/luna_task_197_r07_cached_v3_task193_compat_adapter_v1.md", 8931, "f4cbaa9f84b3b50f24902e8d37bcac56043f80b75a6ff0e26f234f569e612b5f"),
    "v188_contract": ("sol/proof_r07_compressed_diagonal_successor_relation_module_v188.md", 11314, "6512e810011105f83f845e9a41f63ee51fe278371f2cee6cc241e8022a41e822"),
    "adapter_fixture": ("search/certs/d972_r07_cached_v3_task193_compat_adapter_selftest_v1_20260828.json", 673, "1d7ae0025aff04094123e9c6fb85cb0d27f83328ef192329eb464ebc84e863b9"),
}

FIELDS = (
    "status", "correction_word", "solution_coefficients", "columns", "target",
    "exactification.positive_receipt", "exactification.source", "exactification.literal.c_star",
    "exactification.literal.v0", "exactification.literal.u0", "exactification.literal.h",
    "exactification.literal.c_exact", "exactification.exponents", "exactification.A", "exactification.B",
    "exactification.factor_sources", "exactification.joint_kernel_replay",
    "exact_direct_replay.row", "exact_direct_replay.row_sha256", "exact_direct_replay.star_row",
    "exact_direct_replay.star_row_sha256", "exact_direct_replay.replay.corrected_word",
    "exact_direct_replay.replay.direct_all_seven_replay", "exact_direct_replay.right_g760_multiplication",
    "exact_direct_replay.hexagons", "exact_direct_replay.pentagon_printed_order",
)

MUTATIONS = (
    "v3_schema", "v3_status", "v3_terminal", "v3_self_digest",
    "artifact_run_id", "artifact_head_sha", "artifact_id", "artifact_name",
    "artifact_zip_sha256", "artifact_member_path", "artifact_member_bytes",
    "artifact_member_bytes_bool", "artifact_member_sha256",
    "v3_checker_line", "v3_checker_source_pin",
    "v2_schema", "v2_status", "v2_terminal", "v2_self_digest",
    "v2_checker_line", "v2_checker_source_pin",
    "corrected_word_sign", "corrected_word_order", "c_exact_sign", "c_exact_order",
    "exponent_value", "A_value", "B_value",
    "direct_sparse_key", "direct_sparse_coefficient", "direct_sparse_order", "direct_row_sha256",
    "direct_star_row", "direct_star_row_sha256",
    "flag_all_seven", "flag_hexagons", "flag_pentagon", "flag_right_multiplication",
    "solution_coefficient", "solution_coefficient_bool", "selected_column",
    "unwhitelisted_added_field", "unwhitelisted_deleted_field", "unwhitelisted_changed_field",
    "certificate_extra_field", "certificate_equality_flag", "stale_output", "selftest_as_production",
    "external_path_absolute", "external_path_traversal", "external_path_metachar",
    "external_path_glob", "external_path_whitespace", "external_path_ci_out", "internal_path_substitution",
)

ARTIFACT_KEYS = {"run_id", "head_sha", "artifact_id", "artifact_name", "zip_sha256", "member_path", "member_bytes", "member_sha256"}
IDENTITY_KEYS = {"path", "bytes", "sha256", "self_digest"}
CERT_KEYS = {
    "schema", "status", "terminal", "execution_mode", "artifact", "sources", "v3", "v2",
    "field_diff", "self_digest_only_changed", "v3_checker_line", "v2_checker_line",
    "v3_checker_attestation_path", "v2_checker_attestation_path",
    "v3_checker_attestation_sha256", "v2_checker_attestation_sha256",
    "consumed_field_equality", "corrected_word_equal", "c_exact_equal", "direct_row_equal",
    "checkpoint_absent", "self_digest",
}
SUMMARY_KEYS = {"schema", "status", "terminal", "execution_mode", "paths", "artifact", "identities", "mutation_controls", "toy", "self_digest"}
FORBIDDEN = {"negative_claim", "fake_claim", "fake_witness", "fake", "cofinal_claim", "cofinal_lift", "cofinal", "ihara_claim", "ihara_witness"}


def req(value, message):
    if not value:
        raise RuntimeError(message)


def enc(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("ascii")


def sh(raw):
    return hashlib.sha256(raw).hexdigest()


def sv(value):
    return sh(enc(value))


def sparse_digest(row):
    req(type(row) is list, "sparse row shape")
    parsed = {}
    public_keys = []
    for item in row:
        req(type(item) is list and len(item) == 2 and type(item[0]) is str and type(item[1]) is int and item[1] in (1, 2), "sparse item type")
        req(len(item[0]) % 2 == 0 and re.fullmatch(r"[0-9a-f]+", item[0]) is not None, "canonical sparse key")
        try:
            key = bytes.fromhex(item[0])
        except ValueError as exc:
            raise RuntimeError("sparse key hex") from exc
        req(key and key not in parsed, "sparse key duplicate/empty")
        parsed[key] = item[1]
        public_keys.append(item[0])
    req(public_keys == sorted(public_keys), "canonical sparse key order")
    payload = bytearray()
    for key in sorted(parsed):
        payload.extend(len(key).to_bytes(4, "big"))
        payload.extend(key)
        payload.append(parsed[key] % 3)
    return sh(bytes(payload))


def strict_equal(left, right):
    if type(left) is not type(right):
        return False
    if isinstance(left, dict):
        return set(left) == set(right) and all(strict_equal(left[key], right[key]) for key in sorted(left))
    if isinstance(left, list):
        return len(left) == len(right) and all(strict_equal(a, b) for a, b in zip(left, right))
    return left == right


def sealed(value):
    if not isinstance(value, dict):
        return False
    body = dict(value)
    claimed = body.pop("self_digest", None)
    return type(claimed) is str and claimed == sv(body)


def reseal(value):
    body = dict(value)
    body.pop("self_digest", None)
    body["self_digest"] = sv(body)
    return body


def read(path):
    raw = Path(path).read_bytes()
    req(raw, "empty receipt")
    value = json.loads(raw.decode("ascii"))
    req(raw == enc(value) + b"\n", "noncanonical JSON input")
    return value, raw


def path_text(path):
    return Path(path).as_posix()


def safe_external_path(path):
    original = str(path)
    text = path_text(path)
    req(original == text, "noncanonical external path")
    req("\\" not in original and not Path(original).is_absolute(), "absolute/backslash external path")
    req(re.fullmatch(r"[A-Za-z0-9_./-]+", original) is not None, "unsafe external path characters")
    req(original.startswith("ci/in/task197/") and not original.endswith("/"), "external path prefix")
    req(all(part not in ("", ".", "..") for part in original.split("/")), "external path segment")
    req(".." not in original and "//" not in original and "\\" not in original and "ci/out" not in original, "external path traversal")
    base = (ROOT / "ci/in/task197").resolve()
    req((ROOT / original).resolve().is_relative_to(base), "external path resolved outside task197 input directory")
    return original


def exact_internal_path(path, expected):
    original = str(path)
    text = path_text(path)
    req(original == expected and text == expected, "internal path binding:" + expected)
    req("\\" not in original and not Path(original).is_absolute(), "absolute/backslash internal path")
    req(re.fullmatch(r"[A-Za-z0-9_./-]+", text) is not None and ".." not in text and "//" not in text and "\\" not in text, "unsafe internal path")
    return text


def require_absent(paths):
    for path in paths:
        req(not Path(path).exists(), "stale output:" + path_text(path))


def source_identities():
    out = {}
    for name, (rel, size, expected) in PINS.items():
        raw = (ROOT / rel).read_bytes()
        req(len(raw) == size and sh(raw) == expected, "source pin:" + name)
        out[name] = {"path": rel, "bytes": size, "sha256": expected}
    return out


def reject_forbidden_claims(value):
    if isinstance(value, dict):
        for key, item in value.items():
            harmless = item is None or item is False or (type(item) is str and item == "") or (type(item) is list and not item) or (type(item) is dict and not item)
            req(key not in FORBIDDEN or harmless, "forbidden mathematical claim:" + str(key))
            reject_forbidden_claims(item)
    elif isinstance(value, list):
        for item in value:
            reject_forbidden_claims(item)


def paths_diff(left, right, path=""):
    out = []
    if type(left) is not type(right):
        out.append({"kind": "changed", "path": path, "left": left, "right": right})
    elif isinstance(left, dict):
        for key in sorted(set(left) | set(right)):
            child = path + "/" + str(key)
            if key not in left:
                out.append({"kind": "added", "path": child, "value": right[key]})
            elif key not in right:
                out.append({"kind": "deleted", "path": child, "value": left[key]})
            else:
                out.extend(paths_diff(left[key], right[key], child))
    elif isinstance(left, list):
        if not strict_equal(left, right):
            out.append({"kind": "changed", "path": path, "left": left, "right": right})
    elif not strict_equal(left, right):
        out.append({"kind": "changed", "path": path, "left": left, "right": right})
    return out


def at(value, dotted):
    current = value
    for part in dotted.split("."):
        req(isinstance(current, dict) and part in current, "missing field:" + dotted)
        current = current[part]
    return current


def check_envelopes(v3, v2):
    req(sealed(v3) and sealed(v2), "receipt seals")
    req(v3.get("schema") == V3_SCHEMA and v3.get("status") == "COMMON_WORD" and v3.get("terminal") == V3_COMMON, "v3 envelope")
    req(v2.get("schema") == V2_SCHEMA and v2.get("status") == "COMMON_WORD" and v2.get("terminal") == V2_COMMON, "v2 envelope")
    req("checkpoint" not in v3 and "checkpoint" not in v2, "positive checkpoint")
    reject_forbidden_claims(v3)
    reject_forbidden_claims(v2)
    expected_diff = [
        {"kind": "changed", "path": "/schema", "left": V3_SCHEMA, "right": V2_SCHEMA},
        {"kind": "changed", "path": "/self_digest", "left": v3["self_digest"], "right": v2["self_digest"]},
        {"kind": "changed", "path": "/terminal", "left": V3_COMMON, "right": V2_COMMON},
    ]
    diff = paths_diff(v3, v2)
    req(strict_equal(diff, expected_diff) and v3["self_digest"] != v2["self_digest"], "complete three-field lossless diff")
    for field in FIELDS:
        req(strict_equal(at(v3, field), at(v2, field)), "changed consumed field:" + field)
    exact = v3.get("exactification", {})
    direct = v3.get("exact_direct_replay", {})
    req(type(exact) is dict and type(direct) is dict, "exactification/direct types")
    req(exact.get("positive_receipt") is True and exact.get("source") == "authenticated task179 roster ordinals", "exactification provenance")
    literal = exact.get("literal", {})
    req(type(literal) is dict and type(literal.get("c_exact")) is list, "c_exact")
    req(type(exact.get("exponents")) is dict and type(exact.get("A")) is int and type(exact.get("B")) is int, "exponent types")
    req(type(direct.get("row")) is list and direct.get("row_sha256") == sparse_digest(direct["row"]), "direct row")
    req(type(direct.get("star_row")) is list and direct.get("star_row_sha256") == sparse_digest(direct["star_row"]), "star row")
    req(strict_equal(direct["row"], direct["star_row"]), "direct/star row equality")
    replay = direct.get("replay", {})
    req(type(replay) is dict, "direct replay type")
    req(direct.get("right_g760_multiplication") is True and direct.get("hexagons") is True and direct.get("pentagon_printed_order") is True and replay.get("direct_all_seven_replay") is True, "direct gates")
    req(type(replay.get("corrected_word")) is list and replay["corrected_word"], "corrected word")
    return diff


def check_artifact(meta, raw3):
    req(type(meta) is dict and set(meta) == ARTIFACT_KEYS, "artifact exact keyset")
    req(type(meta["run_id"]) is str and re.fullmatch(r"[0-9]+", meta["run_id"]) is not None, "run id")
    req(type(meta["artifact_id"]) is str and re.fullmatch(r"[0-9]+", meta["artifact_id"]) is not None, "artifact id")
    req(type(meta["head_sha"]) is str and re.fullmatch(r"[0-9a-f]{40}", meta["head_sha"]) is not None, "head sha")
    req(type(meta["zip_sha256"]) is str and re.fullmatch(r"[0-9a-f]{64}", meta["zip_sha256"]) is not None, "zip sha")
    req(type(meta["member_sha256"]) is str and re.fullmatch(r"[0-9a-f]{64}", meta["member_sha256"]) is not None, "member sha")
    req(type(meta["member_bytes"]) is int and meta["member_bytes"] == len(raw3), "member bytes type/binding")
    req(meta["member_sha256"] == sh(raw3), "member hash binding")
    req(type(meta["artifact_name"]) is str and re.fullmatch(r"[A-Za-z0-9_.-]+", meta["artifact_name"]) is not None, "artifact name")
    req(meta["member_path"] == "task192_v3_receipt.json", "member path")


def bind_paths(mode, v3_path, v2_path, cert_path, v3_attestation, v2_attestation):
    req(mode in ("SELFTEST", "PRODUCTION"), "checker mode")
    paths = SELF_PATHS if mode == "SELFTEST" else PROD_PATHS
    if mode == "SELFTEST":
        exact_internal_path(v3_path, paths["v3_receipt"])
    else:
        safe_external_path(v3_path)
    exact_internal_path(v2_path, paths["v2_receipt"])
    exact_internal_path(cert_path, paths["certificate"])
    exact_internal_path(v3_attestation, paths["v3_attestation"])
    exact_internal_path(v2_attestation, paths["v2_attestation"])


def validate_bundle_values(v3, raw3, v2, raw2, cert, att3_raw, att2_raw, meta, mode, v3_path, v2_path, cert_path, v3_attestation, v2_attestation, expected_v3_line, expected_v2_line):
    req(raw3 == enc(v3) + b"\n" and raw2 == enc(v2) + b"\n", "canonical bundle bytes")
    diff = check_envelopes(v3, v2)
    check_artifact(meta, raw3)
    req(type(cert) is dict and set(cert) == CERT_KEYS and sealed(cert), "certificate exact sealed keyset")
    req(cert["schema"] == SCHEMA + "/certificate" and cert["status"] == "PASS" and cert["terminal"] == COMMON and cert["execution_mode"] == mode, "certificate envelope/mode")
    reject_forbidden_claims(cert)
    req(strict_equal(cert["artifact"], meta), "certificate artifact")
    req(strict_equal(cert["sources"], source_identities()), "source identity table")
    req(type(cert["v3"]) is dict and set(cert["v3"]) == IDENTITY_KEYS and type(cert["v2"]) is dict and set(cert["v2"]) == IDENTITY_KEYS, "receipt identity keysets")
    expected_v3 = {"path": path_text(v3_path), "bytes": len(raw3), "sha256": sh(raw3), "self_digest": v3["self_digest"]}
    expected_v2 = {"path": path_text(v2_path), "bytes": len(raw2), "sha256": sh(raw2), "self_digest": v2["self_digest"]}
    req(strict_equal(cert["v3"], expected_v3) and strict_equal(cert["v2"], expected_v2), "receipt identities")
    req(att3_raw == (expected_v3_line + "\n").encode("ascii") and att2_raw == (expected_v2_line + "\n").encode("ascii"), "checker attestation bytes")
    req(cert["v3_checker_line"] == expected_v3_line and cert["v2_checker_line"] == expected_v2_line, "checker lines")
    req(cert["v3_checker_attestation_path"] == path_text(v3_attestation) and cert["v2_checker_attestation_path"] == path_text(v2_attestation), "checker attestation paths")
    req(cert["v3_checker_attestation_sha256"] == sh(att3_raw) and cert["v2_checker_attestation_sha256"] == sh(att2_raw), "checker attestation identities")
    req(strict_equal(cert["field_diff"], diff) and cert["self_digest_only_changed"] is True, "certificate diff")
    req(strict_equal(cert["consumed_field_equality"], {field: True for field in FIELDS}), "consumed equality ledger")
    req(cert["corrected_word_equal"] is True and cert["c_exact_equal"] is True and cert["direct_row_equal"] is True and cert["checkpoint_absent"] is True, "certificate equality claims")


def production(v3_path, v2_path, cert_path, v3_attestation, v2_attestation, meta, mode, expected_v3_line, expected_v2_line):
    bind_paths(mode, v3_path, v2_path, cert_path, v3_attestation, v2_attestation)
    v3, raw3 = read(v3_path)
    v2, raw2 = read(v2_path)
    cert, _ = read(cert_path)
    att3_raw = Path(v3_attestation).read_bytes()
    att2_raw = Path(v2_attestation).read_bytes()
    validate_bundle_values(v3, raw3, v2, raw2, cert, att3_raw, att2_raw, meta, mode, v3_path, v2_path, cert_path, v3_attestation, v2_attestation, expected_v3_line, expected_v2_line)
    return v3, raw3, v2, raw2, cert, att3_raw, att2_raw


def expected_toy_v3():
    row = [["524f5701", 2], ["524f5702", 1]]
    value = {
        "schema": V3_SCHEMA, "status": "COMMON_WORD", "terminal": V3_COMMON,
        "correction_word": [1, -2, 3], "solution_coefficients": [[1, 2]],
        "columns": [
            {"column_id": 1, "sparse_row": row, "family": "correction", "provenance": {"conjugate_word": [1, -2, 3]}},
            {"column_id": 2, "sparse_row": [["524f5703", 1]], "family": "correction", "provenance": {"conjugate_word": [2]}},
        ],
        "target": row,
        "exactification": {
            "positive_receipt": True, "source": "authenticated task179 roster ordinals",
            "literal": {"c_star": [1, -2, 3], "v0": [2], "u0": [1, -2], "h": [2], "c_exact": [1, -2, 4]},
            "exponents": {"c_star": [54, 0], "v0": [0, 54], "u0": [54, 54], "h": [0, 0], "c_exact": [0, 0]},
            "A": 1, "B": 2,
            "factor_sources": {"correction_conjugates_only": True, "registered_cubes": ["r3", "r9", "r12"], "boundary_words_included": False},
            "joint_kernel_replay": {"r3": True, "r9": True, "r12": True, "u0": True, "v0": True},
        },
        "exact_direct_replay": {
            "row": row, "star_row": row, "row_sha256": sparse_digest(row), "star_row_sha256": sparse_digest(row),
            "replay": {"corrected_word": [760, 1, -2, 4], "direct_all_seven_replay": True},
            "right_g760_multiplication": True, "hexagons": True, "pentagon_printed_order": True,
        },
    }
    return reseal(value)


def derived_fixture_expectation(v3):
    word = v3["correction_word"]
    coefficients = v3["solution_coefficients"]
    direct = v3["exact_direct_replay"]
    c_exact = v3["exactification"]["literal"]["c_exact"]
    return {
        "c_exact": c_exact,
        "coefficient_two": any(type(pair) is list and len(pair) == 2 and type(pair[1]) is int and pair[1] == 2 for pair in coefficients),
        "correction_word": word,
        "diff_paths": ["/schema", "/self_digest", "/terminal"],
        "direct_all_seven_replay": direct["replay"]["direct_all_seven_replay"],
        "direct_corrected_word": direct["replay"]["corrected_word"],
        "direct_row": direct["row"],
        "hexagons": direct["hexagons"],
        "mutation_count": len(MUTATIONS),
        "nonempty_signed_word": bool(word) and any(type(item) is int and item < 0 for item in word) and any(type(item) is int and item > 0 for item in word),
        "nonempty_sparse_row": bool(direct["row"]),
        "nontrivial_c_exact": bool(c_exact) and not strict_equal(c_exact, word),
        "pentagon_printed_order": direct["pentagon_printed_order"],
        "right_g760_multiplication": direct["right_g760_multiplication"],
        "selected_column": coefficients[0][0],
        "solution_coefficients": coefficients,
        "v2_schema": V2_SCHEMA,
        "v3_schema": V3_SCHEMA,
    }


def mutated_bundle(name, v3, v2, cert, att3_raw, att2_raw):
    a, b, c = copy.deepcopy(v3), copy.deepcopy(v2), copy.deepcopy(cert)
    x3, x2 = bytes(att3_raw), bytes(att2_raw)
    if name == "v3_schema": a["schema"] = "bad"; a = reseal(a)
    elif name == "v3_status": a["status"] = "UNKNOWN"; a = reseal(a)
    elif name == "v3_terminal": a["terminal"] = "bad"; a = reseal(a)
    elif name == "v3_self_digest": a["self_digest"] = "0" * 64
    elif name == "artifact_run_id": c["artifact"]["run_id"] = "999"; c = reseal(c)
    elif name == "artifact_head_sha": c["artifact"]["head_sha"] = "b" * 40; c = reseal(c)
    elif name == "artifact_id": c["artifact"]["artifact_id"] = "999"; c = reseal(c)
    elif name == "artifact_name": c["artifact"]["artifact_name"] = "wrong"; c = reseal(c)
    elif name == "artifact_zip_sha256": c["artifact"]["zip_sha256"] = "1" * 64; c = reseal(c)
    elif name == "artifact_member_path": c["artifact"]["member_path"] = "wrong.json"; c = reseal(c)
    elif name == "artifact_member_bytes": c["artifact"]["member_bytes"] += 1; c = reseal(c)
    elif name == "artifact_member_bytes_bool": c["artifact"]["member_bytes"] = True; c = reseal(c)
    elif name == "artifact_member_sha256": c["artifact"]["member_sha256"] = "2" * 64; c = reseal(c)
    elif name == "v3_checker_line": x3 = b"WRONG type=SELFTEST\n"
    elif name == "v3_checker_source_pin": c["sources"]["task192_checker"]["sha256"] = "3" * 64; c = reseal(c)
    elif name == "v2_schema": b["schema"] = "bad"; b = reseal(b)
    elif name == "v2_status": b["status"] = "UNKNOWN"; b = reseal(b)
    elif name == "v2_terminal": b["terminal"] = "bad"; b = reseal(b)
    elif name == "v2_self_digest": b["self_digest"] = "0" * 64
    elif name == "v2_checker_line": x2 = b"WRONG type=SELFTEST\n"
    elif name == "v2_checker_source_pin": c["sources"]["task186_checker"]["sha256"] = "4" * 64; c = reseal(c)
    elif name == "corrected_word_sign": a["exact_direct_replay"]["replay"]["corrected_word"][1] *= -1; a = reseal(a)
    elif name == "corrected_word_order": a["exact_direct_replay"]["replay"]["corrected_word"][1:3] = list(reversed(a["exact_direct_replay"]["replay"]["corrected_word"][1:3])); a = reseal(a)
    elif name == "c_exact_sign": a["exactification"]["literal"]["c_exact"][0] *= -1; a = reseal(a)
    elif name == "c_exact_order": a["exactification"]["literal"]["c_exact"][0:2] = list(reversed(a["exactification"]["literal"]["c_exact"][0:2])); a = reseal(a)
    elif name == "exponent_value": a["exactification"]["exponents"]["c_exact"][0] = 1; a = reseal(a)
    elif name == "A_value": a["exactification"]["A"] += 1; a = reseal(a)
    elif name == "B_value": a["exactification"]["B"] += 1; a = reseal(a)
    elif name == "direct_sparse_key": a["exact_direct_replay"]["row"][0][0] = "524f57ff"; a = reseal(a)
    elif name == "direct_sparse_coefficient": a["exact_direct_replay"]["row"][0][1] = 1; a = reseal(a)
    elif name == "direct_sparse_order": a["exact_direct_replay"]["row"] = list(reversed(a["exact_direct_replay"]["row"])); a = reseal(a)
    elif name == "direct_row_sha256": a["exact_direct_replay"]["row_sha256"] = "5" * 64; a = reseal(a)
    elif name == "direct_star_row": a["exact_direct_replay"]["star_row"][0][1] = 1; a = reseal(a)
    elif name == "direct_star_row_sha256": a["exact_direct_replay"]["star_row_sha256"] = "6" * 64; a = reseal(a)
    elif name == "flag_all_seven": a["exact_direct_replay"]["replay"]["direct_all_seven_replay"] = False; a = reseal(a)
    elif name == "flag_hexagons": a["exact_direct_replay"]["hexagons"] = False; a = reseal(a)
    elif name == "flag_pentagon": a["exact_direct_replay"]["pentagon_printed_order"] = False; a = reseal(a)
    elif name == "flag_right_multiplication": a["exact_direct_replay"]["right_g760_multiplication"] = False; a = reseal(a)
    elif name == "solution_coefficient": a["solution_coefficients"][0][1] = 1; a = reseal(a)
    elif name == "solution_coefficient_bool": a["solution_coefficients"][0][1] = True; a = reseal(a)
    elif name == "selected_column": a["solution_coefficients"][0][0] = 2; a = reseal(a)
    elif name == "unwhitelisted_added_field": a["unexpected_mathematics"] = 1; a = reseal(a)
    elif name == "unwhitelisted_deleted_field": a.pop("target"); a = reseal(a)
    elif name == "unwhitelisted_changed_field": a["target"] = [["524f57aa", 1]]; a = reseal(a)
    elif name == "certificate_extra_field": c["fake_claim"] = True; c = reseal(c)
    elif name == "certificate_equality_flag": c["c_exact_equal"] = False; c = reseal(c)
    else:
        raise RuntimeError("unregistered mutation:" + name)
    return a, b, c, x3, x2


def fixture_expected():
    raw = FIXTURE.read_bytes()
    rel, size, expected_sha = PINS["adapter_fixture"]
    req(path_text(FIXTURE.relative_to(ROOT)) == rel and len(raw) == size and sh(raw) == expected_sha, "fixture identity")
    fixture = json.loads(raw.decode("ascii"))
    req(raw == enc(fixture) + b"\n" and set(fixture) == {"schema", "expected"} and fixture["schema"] == SELF + "/fixture" and type(fixture["expected"]) is dict, "fixture envelope")
    return fixture["expected"]


def selfcheck(summary_path):
    exact_internal_path(summary_path, SELF_PATHS["summary"])
    summary, _ = read(summary_path)
    req(set(summary) == SUMMARY_KEYS and sealed(summary), "selftest exact sealed keyset")
    req(summary["schema"] == SELF and summary["status"] == "PASS" and summary["terminal"] == COMMON + "_SELFTEST_PASS" and summary["execution_mode"] == "SELFTEST", "selftest envelope")
    expected_paths = {key: SELF_PATHS[key] for key in sorted(SELF_PATHS) if key != "summary"}
    req(strict_equal(summary["paths"], expected_paths), "selftest path table")
    controls = summary["mutation_controls"]
    req(type(controls) is dict and set(controls) == {"attempted", "rejected", "names"}, "mutation control keyset")
    req(type(controls["attempted"]) is int and type(controls["rejected"]) is int and controls["attempted"] == controls["rejected"] == len(MUTATIONS), "mutation counts")
    req(tuple(controls["names"]) == MUTATIONS, "exact registered mutation names")
    expected_fixture = fixture_expected()
    req(strict_equal(summary["toy"], expected_fixture), "fixture/value equality")
    meta = summary["artifact"]
    v3, raw3, v2, raw2, cert, att3_raw, att2_raw = production(
        SELF_PATHS["v3_receipt"], SELF_PATHS["v2_receipt"], SELF_PATHS["certificate"],
        SELF_PATHS["v3_attestation"], SELF_PATHS["v2_attestation"], meta,
        "SELFTEST", SELF_V3_LINE, SELF_V2_LINE,
    )
    independently_reconstructed_v3 = expected_toy_v3()
    req(strict_equal(v3, independently_reconstructed_v3), "independently reconstructed toy v3")
    req(strict_equal(expected_fixture, derived_fixture_expectation(independently_reconstructed_v3)), "fixture full semantic binding")
    expected_identities = {
        "v3": {"bytes": len(raw3), "sha256": sh(raw3)},
        "v2": {"bytes": len(raw2), "sha256": sh(raw2)},
        "certificate": {"bytes": len(enc(cert) + b"\n"), "sha256": sh(enc(cert) + b"\n")},
    }
    req(strict_equal(summary["identities"], expected_identities), "selftest identity table")
    rejected = []
    for name in MUTATIONS:
        try:
            if name == "stale_output":
                require_absent([SELF_PATHS["v2_receipt"]])
            elif name == "selftest_as_production":
                bind_paths("PRODUCTION", SELF_PATHS["v3_receipt"], SELF_PATHS["v2_receipt"], SELF_PATHS["certificate"], SELF_PATHS["v3_attestation"], SELF_PATHS["v2_attestation"])
            elif name.startswith("external_path_"):
                bad_paths = {
                    "external_path_absolute": "/tmp/task192.json",
                    "external_path_traversal": "ci/in/task197/../task192.json",
                    "external_path_metachar": "ci/in/task197/task192;id.json",
                    "external_path_glob": "ci/in/task197/*.json",
                    "external_path_whitespace": "ci/in/task197/task 192.json",
                    "external_path_ci_out": "ci/out/task192.json",
                }
                req(name in bad_paths, "registered external path mutation")
                safe_external_path(bad_paths[name])
            elif name == "internal_path_substitution":
                exact_internal_path("ci/out/wrong.json", SELF_PATHS["v2_receipt"])
            else:
                a, b, c, x3, x2 = mutated_bundle(name, v3, v2, cert, att3_raw, att2_raw)
                validate_bundle_values(a, enc(a) + b"\n", b, enc(b) + b"\n", c, x3, x2, meta, "SELFTEST", SELF_PATHS["v3_receipt"], SELF_PATHS["v2_receipt"], SELF_PATHS["certificate"], SELF_PATHS["v3_attestation"], SELF_PATHS["v2_attestation"], SELF_V3_LINE, SELF_V2_LINE)
        except RuntimeError:
            rejected.append(name)
        else:
            raise RuntimeError("mutation accepted:" + name)
    req(tuple(rejected) == MUTATIONS, "independent exact mutation replay")
    return COMMON + "_CHECKER_PASS terminal=" + COMMON + "_SELFTEST_PASS"


def metadata_from_args(args):
    raw = {
        "run_id": args.run_id, "head_sha": args.head_sha, "artifact_id": args.artifact_id,
        "artifact_name": args.artifact_name, "zip_sha256": args.zip_sha256,
        "member_path": args.member_path, "member_bytes": args.member_bytes,
        "member_sha256": args.member_sha256,
    }
    req(all(value is not None for value in raw.values()), "missing artifact argument")
    req(re.fullmatch(r"[0-9]+", str(raw["member_bytes"])) is not None, "member bytes argument")
    return {
        "run_id": str(raw["run_id"]), "head_sha": str(raw["head_sha"]).lower(),
        "artifact_id": str(raw["artifact_id"]), "artifact_name": str(raw["artifact_name"]),
        "zip_sha256": str(raw["zip_sha256"]).lower(), "member_path": str(raw["member_path"]),
        "member_bytes": int(raw["member_bytes"]), "member_sha256": str(raw["member_sha256"]).lower(),
    }


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("receipt")
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--v2-receipt")
    parser.add_argument("--certificate")
    parser.add_argument("--v3-attestation")
    parser.add_argument("--v2-attestation")
    parser.add_argument("--run-id")
    parser.add_argument("--head-sha")
    parser.add_argument("--artifact-id")
    parser.add_argument("--artifact-name")
    parser.add_argument("--zip-sha256")
    parser.add_argument("--member-path")
    parser.add_argument("--member-bytes")
    parser.add_argument("--member-sha256")
    args = parser.parse_args(argv)
    try:
        if args.selftest:
            req(not any((args.v2_receipt, args.certificate, args.v3_attestation, args.v2_attestation, args.run_id, args.head_sha, args.artifact_id, args.artifact_name, args.zip_sha256, args.member_path, args.member_bytes, args.member_sha256)), "selftest argument shape")
            line = selfcheck(args.receipt)
        else:
            req(args.v2_receipt and args.certificate and args.v3_attestation and args.v2_attestation, "production checker arguments")
            meta = metadata_from_args(args)
            production(args.receipt, args.v2_receipt, args.certificate, args.v3_attestation, args.v2_attestation, meta, "PRODUCTION", V3_LINE, V2_LINE)
            line = COMMON + "_CHECKER_PASS terminal=" + COMMON
    except Exception as exc:
        print(COMMON + "_CHECKER_FAIL " + str(exc))
        return 1
    print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
