#!/usr/bin/env python3
"""Lossless task192-v3 to task193/task186-v2 receipt adapter."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
from pathlib import Path
from types import SimpleNamespace


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "d972-r07-cached-v3-task193-compat-adapter/v1"
SELFTEST_SCHEMA = SCHEMA + "/selftest"
COMMON = "R07_CACHED_V3_TASK193_COMPAT_ADAPTER_V1"
V3_SCHEMA = "d972-r07-normalized-exact-cached-colgen/v3"
V3_COMMON = "R07_NORMALIZED_EXACT_CACHED_COLGEN_V3_COMMON_WORD"
V2_SCHEMA = "d972-r07-normalized-exact-common-word-colgen/v2"
V2_COMMON = "R07_NORMALIZED_EXACT_COMMON_WORD_COLGEN_V2_COMMON_WORD"
V3_LINE = "R07_NORMALIZED_EXACT_CACHED_COLGEN_V3_CHECKER_PASS terminal=" + V3_COMMON
V2_LINE = "R07_NORMALIZED_EXACT_COMMON_WORD_COLGEN_V2_CHECKER_PASS terminal=" + V2_COMMON
SELF_V3_LINE = "V3_CHECKER_PLACEHOLDER type=SELFTEST terminal=" + V3_COMMON
SELF_V2_LINE = "V2_CHECKER_PLACEHOLDER type=SELFTEST terminal=" + V2_COMMON
UI = "UNKNOWN_INPUT"

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

CONSUMED = (
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
FORBIDDEN = {"negative_claim", "fake_claim", "fake_witness", "fake", "cofinal_claim", "cofinal_lift", "cofinal", "ihara_claim", "ihara_witness"}


def require(value, message):
    if not value:
        raise RuntimeError(message)


def canon(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("ascii")


def sha_bytes(raw):
    return hashlib.sha256(raw).hexdigest()


def sha_value(value):
    return sha_bytes(canon(value))


def sparse_digest(row):
    require(type(row) is list, "sparse row shape")
    parsed = {}
    public_keys = []
    for item in row:
        require(type(item) is list and len(item) == 2 and type(item[0]) is str and type(item[1]) is int and item[1] in (1, 2), "sparse item type")
        require(len(item[0]) % 2 == 0 and re.fullmatch(r"[0-9a-f]+", item[0]) is not None, "canonical sparse key")
        try:
            key = bytes.fromhex(item[0])
        except ValueError as exc:
            raise RuntimeError("sparse key hex") from exc
        require(key and key not in parsed, "sparse key duplicate/empty")
        parsed[key] = item[1]
        public_keys.append(item[0])
    require(public_keys == sorted(public_keys), "canonical sparse key order")
    payload = bytearray()
    for key in sorted(parsed):
        payload.extend(len(key).to_bytes(4, "big"))
        payload.extend(key)
        payload.append(parsed[key] % 3)
    return sha_bytes(bytes(payload))


def strict_equal(left, right):
    if type(left) is not type(right):
        return False
    if isinstance(left, dict):
        return set(left) == set(right) and all(strict_equal(left[key], right[key]) for key in sorted(left))
    if isinstance(left, list):
        return len(left) == len(right) and all(strict_equal(a, b) for a, b in zip(left, right))
    return left == right


def seal(value):
    body = dict(value)
    body.pop("self_digest", None)
    body["self_digest"] = sha_value(body)
    return body


def is_sealed(value):
    if not isinstance(value, dict):
        return False
    body = dict(value)
    claimed = body.pop("self_digest", None)
    return type(claimed) is str and claimed == sha_value(body)


def path_text(path):
    return Path(path).as_posix()


def safe_external_path(path):
    original = str(path)
    text = path_text(path)
    require(original == text, "noncanonical external path")
    require("\\" not in original and not Path(original).is_absolute(), "absolute/backslash external path")
    require(re.fullmatch(r"[A-Za-z0-9_./-]+", original) is not None, "unsafe external path characters")
    require(original.startswith("ci/in/task197/") and not original.endswith("/"), "external path prefix")
    parts = original.split("/")
    require(all(part not in ("", ".", "..") for part in parts), "external path segment")
    require(".." not in original and "//" not in original and "\\" not in original and "ci/out" not in original, "external path traversal")
    base = (ROOT / "ci/in/task197").resolve()
    require((ROOT / original).resolve().is_relative_to(base), "external path resolved outside task197 input directory")
    return original


def exact_internal_path(path, expected):
    original = str(path)
    text = path_text(path)
    require(original == expected and text == expected, "internal path binding:" + expected)
    require("\\" not in original and not Path(original).is_absolute(), "absolute/backslash internal path")
    require(re.fullmatch(r"[A-Za-z0-9_./-]+", text) is not None and ".." not in text and "//" not in text and "\\" not in text, "unsafe internal path")
    return text


def require_absent(paths):
    for path in paths:
        require(not Path(path).exists(), "stale output:" + path_text(path))


def read_json(path):
    raw = Path(path).read_bytes()
    require(raw, "empty input")
    value = json.loads(raw.decode("ascii"))
    require(raw == canon(value) + b"\n", "noncanonical JSON input")
    return value, raw


def auth_sources():
    identities = {}
    for name, (rel, size, expected) in PINS.items():
        raw = (ROOT / rel).read_bytes()
        require(len(raw) == size and sha_bytes(raw) == expected, "pin:" + name)
        identities[name] = {"path": rel, "bytes": size, "sha256": expected}
    return identities


def metadata(args, raw):
    out = {}
    for field in sorted(ARTIFACT_KEYS):
        value = getattr(args, field)
        require(value is not None and str(value) != "", "missing artifact binding:" + field)
        if field == "member_bytes":
            require(re.fullmatch(r"[0-9]+", str(value)) is not None, "member bytes syntax")
            out[field] = int(value)
        else:
            out[field] = str(value)
    require(out["member_bytes"] == len(raw), "artifact member byte binding")
    require(out["member_sha256"].lower() == sha_bytes(raw), "artifact member hash binding")
    for field in ("zip_sha256", "member_sha256"):
        require(re.fullmatch(r"[0-9a-fA-F]{64}", out[field]) is not None, "artifact hash syntax:" + field)
        out[field] = out[field].lower()
    require(re.fullmatch(r"[0-9]+", out["run_id"]) is not None, "artifact run id syntax")
    require(re.fullmatch(r"[0-9]+", out["artifact_id"]) is not None, "artifact id syntax")
    require(re.fullmatch(r"[0-9a-fA-F]{40}", out["head_sha"]) is not None, "head sha syntax")
    out["head_sha"] = out["head_sha"].lower()
    require(re.fullmatch(r"[A-Za-z0-9_.-]+", out["artifact_name"]) is not None, "artifact name syntax")
    require(out["member_path"] == "task192_v3_receipt.json", "member path binding")
    return out


def reject_forbidden_claims(value):
    if isinstance(value, dict):
        for key, item in value.items():
            harmless = item is None or item is False or (type(item) is str and item == "") or (type(item) is list and not item) or (type(item) is dict and not item)
            require(key not in FORBIDDEN or harmless, "forbidden mathematical claim:" + str(key))
            reject_forbidden_claims(item)
    elif isinstance(value, list):
        for item in value:
            reject_forbidden_claims(item)


def positive_v3(value):
    require(is_sealed(value), "v3 self digest")
    require(value.get("schema") == V3_SCHEMA and value.get("status") == "COMMON_WORD" and value.get("terminal") == V3_COMMON, "v3 positive envelope")
    require("checkpoint" not in value, "positive v3 checkpoint must be absent for adapter")
    reject_forbidden_claims(value)
    ex = value.get("exactification", {})
    require(type(ex) is dict, "v3 exactification type")
    lit = ex.get("literal", {})
    require(type(lit) is dict, "v3 literal type")
    direct = value.get("exact_direct_replay", {})
    require(type(direct) is dict, "v3 direct replay type")
    require(ex.get("positive_receipt") is True and ex.get("source") == "authenticated task179 roster ordinals", "v3 exactification provenance")
    require(type(lit.get("c_exact")) is list, "v3 c_exact")
    require(type(ex.get("exponents")) is dict and type(ex.get("A")) is int and type(ex.get("B")) is int, "v3 exponent fields")
    require(type(direct.get("row")) is list and type(direct.get("row_sha256")) is str and direct["row_sha256"] == sparse_digest(direct["row"]), "v3 direct row")
    require(type(direct.get("star_row")) is list and type(direct.get("star_row_sha256")) is str and direct["star_row_sha256"] == sparse_digest(direct["star_row"]), "v3 star row")
    require(strict_equal(direct["row"], direct["star_row"]), "v3 direct/star row equality")
    require(direct.get("right_g760_multiplication") is True and direct.get("hexagons") is True and direct.get("pentagon_printed_order") is True, "v3 direct gates")
    replay = direct.get("replay", {})
    require(type(replay) is dict, "v3 replay type")
    require(replay.get("direct_all_seven_replay") is True and type(replay.get("corrected_word")) is list and replay["corrected_word"], "v3 corrected replay")


def exact_attestation(path, expected):
    raw = Path(path).read_bytes()
    require(raw == (expected + "\n").encode("ascii"), "checker attestation")
    return raw


def diff_values(left, right, path=""):
    changes = []
    if type(left) is not type(right):
        changes.append({"kind": "changed", "path": path, "left": left, "right": right})
    elif isinstance(left, dict):
        for key in sorted(set(left) | set(right)):
            child = path + "/" + str(key)
            if key not in left:
                changes.append({"kind": "added", "path": child, "value": right[key]})
            elif key not in right:
                changes.append({"kind": "deleted", "path": child, "value": left[key]})
            else:
                changes.extend(diff_values(left[key], right[key], child))
    elif isinstance(left, list):
        if not strict_equal(left, right):
            changes.append({"kind": "changed", "path": path, "left": left, "right": right})
    elif not strict_equal(left, right):
        changes.append({"kind": "changed", "path": path, "left": left, "right": right})
    return changes


def get_path(value, dotted):
    current = value
    for part in dotted.split("."):
        require(isinstance(current, dict) and part in current, "missing consumed field:" + dotted)
        current = current[part]
    return current


def convert(v3):
    positive_v3(v3)
    converted = copy.deepcopy(v3)
    converted.pop("self_digest", None)
    converted["schema"] = V2_SCHEMA
    converted["terminal"] = V2_COMMON
    require(converted.get("status") == "COMMON_WORD", "v2 status conversion")
    changes = diff_values({k: v for k, v in v3.items() if k != "self_digest"}, converted)
    expected = [
        {"kind": "changed", "path": "/schema", "left": V3_SCHEMA, "right": V2_SCHEMA},
        {"kind": "changed", "path": "/terminal", "left": V3_COMMON, "right": V2_COMMON},
    ]
    require(strict_equal(changes, expected), "non-lossless conversion")
    return seal(converted), changes


def semantic_equal(v3, v2):
    for field in CONSUMED:
        require(strict_equal(get_path(v3, field), get_path(v2, field)), "converted field changed:" + field)


def artifact_block(meta):
    require(type(meta) is dict and set(meta) == ARTIFACT_KEYS, "artifact exact keyset")
    return {key: meta[key] for key in sorted(ARTIFACT_KEYS)}


def mode_paths(mode):
    require(mode in ("SELFTEST", "PRODUCTION"), "execution mode")
    return SELF_PATHS if mode == "SELFTEST" else PROD_PATHS


def bind_phase_paths(mode, v3_path, v3_attestation, v2_path, prepared_path, v2_attestation=None, cert_path=None):
    paths = mode_paths(mode)
    if mode == "SELFTEST":
        exact_internal_path(v3_path, paths["v3_receipt"])
    else:
        safe_external_path(v3_path)
    exact_internal_path(v3_attestation, paths["v3_attestation"])
    exact_internal_path(v2_path, paths["v2_receipt"])
    exact_internal_path(prepared_path, paths["prepared"])
    if v2_attestation is not None:
        exact_internal_path(v2_attestation, paths["v2_attestation"])
    if cert_path is not None:
        exact_internal_path(cert_path, paths["certificate"])


def prepare(v3_path, v3_attestation, v2_path, prepared_path, args, mode, expected_v3_line, emit=True):
    bind_phase_paths(mode, v3_path, v3_attestation, v2_path, prepared_path)
    identities = auth_sources()
    require(set(identities) == set(PINS), "source identity keyset")
    v3, raw = read_json(v3_path)
    positive_v3(v3)
    require(sha_bytes(raw) == str(args.member_sha256).lower() and len(raw) == int(args.member_bytes), "receipt/member identity")
    att_raw = exact_attestation(v3_attestation, expected_v3_line)
    meta = metadata(args, raw)
    v2, changes = convert(v3)
    raw2 = canon(v2) + b"\n"
    Path(v2_path).write_bytes(raw2)
    record = {
        "schema": SCHEMA + "/prepared", "execution_mode": mode,
        "input": {"path": path_text(v3_path), "bytes": len(raw), "sha256": sha_bytes(raw)},
        "artifact": artifact_block(meta),
        "v3_checker_attestation_path": path_text(v3_attestation),
        "v3_checker_attestation": expected_v3_line,
        "v3_checker_attestation_sha256": sha_bytes(att_raw),
        "changes": changes,
        "v2": {"path": path_text(v2_path), "bytes": len(raw2), "sha256": sha_bytes(raw2)},
    }
    Path(prepared_path).write_bytes(canon(seal(record)) + b"\n")
    if emit:
        print(COMMON + "_PREPARE_PASS")


def validate_prepared(prepared, mode, v3, raw3, v2, raw2, meta, v3_path, v3_attestation, v2_path):
    expected_keys = {"schema", "execution_mode", "input", "artifact", "v3_checker_attestation_path", "v3_checker_attestation", "v3_checker_attestation_sha256", "changes", "v2", "self_digest"}
    require(type(prepared) is dict and set(prepared) == expected_keys and is_sealed(prepared), "prepared exact sealed keyset")
    require(prepared["schema"] == SCHEMA + "/prepared" and prepared["execution_mode"] == mode, "prepared mode envelope")
    require(strict_equal(prepared["input"], {"path": path_text(v3_path), "bytes": len(raw3), "sha256": sha_bytes(raw3)}), "prepared input binding")
    require(strict_equal(prepared["artifact"], artifact_block(meta)), "prepared artifact binding")
    require(prepared["v3_checker_attestation_path"] == path_text(v3_attestation), "prepared attestation path")
    require(strict_equal(prepared["v2"], {"path": path_text(v2_path), "bytes": len(raw2), "sha256": sha_bytes(raw2)}), "prepared v2 binding")
    expected_changes = diff_values({key: value for key, value in v3.items() if key != "self_digest"}, {key: value for key, value in v2.items() if key != "self_digest"})
    require(strict_equal(prepared["changes"], expected_changes), "prepared conversion diff")


def validate_final_bundle(v3, raw3, v2, raw2, cert, meta, att3_raw, att2_raw, mode, v3_path, v2_path, v3_attestation, v2_attestation, expected_v3_line, expected_v2_line):
    positive_v3(v3)
    require(raw3 == canon(v3) + b"\n" and raw2 == canon(v2) + b"\n", "bundle canonical bytes")
    require(is_sealed(v2) and v2.get("schema") == V2_SCHEMA and v2.get("status") == "COMMON_WORD" and v2.get("terminal") == V2_COMMON, "v2 positive envelope")
    reject_forbidden_claims(v2)
    converted, changes = convert(v3)
    require(strict_equal(converted, v2), "converted receipt mismatch")
    semantic_equal(v3, v2)
    full_changes = diff_values(v3, v2)
    expected_full_changes = [
        {"kind": "changed", "path": "/schema", "left": V3_SCHEMA, "right": V2_SCHEMA},
        {"kind": "changed", "path": "/self_digest", "left": v3["self_digest"], "right": v2["self_digest"]},
        {"kind": "changed", "path": "/terminal", "left": V3_COMMON, "right": V2_COMMON},
    ]
    require(strict_equal(full_changes, expected_full_changes) and v3["self_digest"] != v2["self_digest"], "complete three-field conversion diff")
    require(type(cert) is dict and set(cert) == CERT_KEYS and is_sealed(cert), "certificate exact sealed keyset")
    require(cert["schema"] == SCHEMA + "/certificate" and cert["status"] == "PASS" and cert["terminal"] == COMMON and cert["execution_mode"] == mode, "certificate envelope/mode")
    reject_forbidden_claims(cert)
    require(strict_equal(cert["artifact"], artifact_block(meta)), "certificate artifact binding")
    require(strict_equal(cert["sources"], auth_sources()), "certificate source identity table")
    require(type(cert["v3"]) is dict and set(cert["v3"]) == IDENTITY_KEYS and type(cert["v2"]) is dict and set(cert["v2"]) == IDENTITY_KEYS, "certificate receipt identity keysets")
    require(strict_equal(cert["v3"], {"path": path_text(v3_path), "bytes": len(raw3), "sha256": sha_bytes(raw3), "self_digest": v3["self_digest"]}), "certificate v3 identity")
    require(strict_equal(cert["v2"], {"path": path_text(v2_path), "bytes": len(raw2), "sha256": sha_bytes(raw2), "self_digest": v2["self_digest"]}), "certificate v2 identity")
    require(att3_raw == (expected_v3_line + "\n").encode("ascii") and att2_raw == (expected_v2_line + "\n").encode("ascii"), "certificate exact checker lines")
    require(cert["v3_checker_line"] == expected_v3_line and cert["v2_checker_line"] == expected_v2_line, "certificate checker line values")
    require(cert["v3_checker_attestation_path"] == path_text(v3_attestation) and cert["v2_checker_attestation_path"] == path_text(v2_attestation), "certificate checker paths")
    require(cert["v3_checker_attestation_sha256"] == sha_bytes(att3_raw) and cert["v2_checker_attestation_sha256"] == sha_bytes(att2_raw), "certificate checker hashes")
    require(strict_equal(cert["field_diff"], full_changes) and cert["self_digest_only_changed"] is True, "certificate field diff")
    require(strict_equal(cert["consumed_field_equality"], {field: True for field in CONSUMED}), "certificate consumed ledger")
    require(cert["corrected_word_equal"] is True and cert["c_exact_equal"] is True and cert["direct_row_equal"] is True and cert["checkpoint_absent"] is True, "certificate equality gates")


def finalize(v3_path, v2_path, prepared_path, cert_path, v3_attestation, v2_attestation, args, mode, expected_v3_line, expected_v2_line, emit=True):
    bind_phase_paths(mode, v3_path, v3_attestation, v2_path, prepared_path, v2_attestation, cert_path)
    v3, raw3 = read_json(v3_path)
    v2, raw2 = read_json(v2_path)
    prepared, _ = read_json(prepared_path)
    meta = metadata(args, raw3)
    att3_raw = exact_attestation(v3_attestation, expected_v3_line)
    att2_raw = exact_attestation(v2_attestation, expected_v2_line)
    validate_prepared(prepared, mode, v3, raw3, v2, raw2, meta, v3_path, v3_attestation, v2_path)
    require(prepared["v3_checker_attestation"] == expected_v3_line and prepared["v3_checker_attestation_sha256"] == sha_bytes(att3_raw), "prepared checker binding")
    converted, changes = convert(v3)
    require(strict_equal(converted, v2), "converted receipt mismatch")
    semantic_equal(v3, v2)
    full_changes = diff_values(v3, v2)
    cert = {
        "schema": SCHEMA + "/certificate", "status": "PASS", "terminal": COMMON, "execution_mode": mode,
        "artifact": artifact_block(meta), "sources": auth_sources(),
        "v3": {"path": path_text(v3_path), "bytes": len(raw3), "sha256": sha_bytes(raw3), "self_digest": v3["self_digest"]},
        "v2": {"path": path_text(v2_path), "bytes": len(raw2), "sha256": sha_bytes(raw2), "self_digest": v2["self_digest"]},
        "field_diff": full_changes, "self_digest_only_changed": True,
        "v3_checker_line": expected_v3_line, "v2_checker_line": expected_v2_line,
        "v3_checker_attestation_path": path_text(v3_attestation), "v2_checker_attestation_path": path_text(v2_attestation),
        "v3_checker_attestation_sha256": sha_bytes(att3_raw), "v2_checker_attestation_sha256": sha_bytes(att2_raw),
        "consumed_field_equality": {field: True for field in CONSUMED},
        "corrected_word_equal": True, "c_exact_equal": True, "direct_row_equal": True,
        "checkpoint_absent": "checkpoint" not in v3 and "checkpoint" not in v2,
    }
    cert = seal(cert)
    validate_final_bundle(v3, raw3, v2, raw2, cert, meta, att3_raw, att2_raw, mode, v3_path, v2_path, v3_attestation, v2_attestation, expected_v3_line, expected_v2_line)
    Path(cert_path).write_bytes(canon(cert) + b"\n")
    if emit:
        print(COMMON + "_FINALIZE_PASS terminal=" + COMMON)


def toy_v3():
    row = [["524f5701", 2], ["524f5702", 1]]
    base = {
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
    return seal(base)


def selftest_expected():
    raw = (ROOT / PINS["adapter_fixture"][0]).read_bytes()
    require(len(raw) == PINS["adapter_fixture"][1] and sha_bytes(raw) == PINS["adapter_fixture"][2], "selftest fixture pin")
    value = json.loads(raw.decode("ascii"))
    require(type(value) is dict and set(value) == {"schema", "expected"} and raw == canon(value) + b"\n" and value.get("schema") == SELFTEST_SCHEMA + "/fixture" and type(value.get("expected")) is dict, "selftest fixture schema")
    return value["expected"]


def derived_toy_expectation(v3):
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


def reseal(value):
    return seal(value)


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


def run_selftest(output_path):
    exact_internal_path(output_path, SELF_PATHS["summary"])
    phase_outputs = [SELF_PATHS[key] for key in ("v3_receipt", "v3_attestation", "v2_receipt", "v2_attestation", "prepared", "certificate")]
    require_absent(phase_outputs + [SELF_PATHS["summary"]])
    Path(SELF_PATHS["v3_receipt"]).parent.mkdir(parents=True, exist_ok=True)
    v3 = toy_v3()
    raw3 = canon(v3) + b"\n"
    Path(SELF_PATHS["v3_receipt"]).write_bytes(raw3)
    Path(SELF_PATHS["v3_attestation"]).write_bytes((SELF_V3_LINE + "\n").encode("ascii"))
    meta = SimpleNamespace(
        run_id="197001", head_sha="a" * 40, artifact_id="197", artifact_name="task192-v3-selftest",
        zip_sha256="0" * 64, member_path="task192_v3_receipt.json",
        member_bytes=str(len(raw3)), member_sha256=sha_bytes(raw3),
    )
    prepare(SELF_PATHS["v3_receipt"], SELF_PATHS["v3_attestation"], SELF_PATHS["v2_receipt"], SELF_PATHS["prepared"], meta, "SELFTEST", SELF_V3_LINE, emit=False)
    Path(SELF_PATHS["v2_attestation"]).write_bytes((SELF_V2_LINE + "\n").encode("ascii"))
    finalize(SELF_PATHS["v3_receipt"], SELF_PATHS["v2_receipt"], SELF_PATHS["prepared"], SELF_PATHS["certificate"], SELF_PATHS["v3_attestation"], SELF_PATHS["v2_attestation"], meta, "SELFTEST", SELF_V3_LINE, SELF_V2_LINE, emit=False)

    v3, raw3 = read_json(SELF_PATHS["v3_receipt"])
    v2, raw2 = read_json(SELF_PATHS["v2_receipt"])
    cert, _ = read_json(SELF_PATHS["certificate"])
    meta_value = metadata(meta, raw3)
    att3_raw = Path(SELF_PATHS["v3_attestation"]).read_bytes()
    att2_raw = Path(SELF_PATHS["v2_attestation"]).read_bytes()
    validate_final_bundle(v3, raw3, v2, raw2, cert, meta_value, att3_raw, att2_raw, "SELFTEST", SELF_PATHS["v3_receipt"], SELF_PATHS["v2_receipt"], SELF_PATHS["v3_attestation"], SELF_PATHS["v2_attestation"], SELF_V3_LINE, SELF_V2_LINE)

    rejected = []
    for name in MUTATIONS:
        try:
            if name == "stale_output":
                require_absent([SELF_PATHS["v2_receipt"]])
            elif name == "selftest_as_production":
                bind_phase_paths("PRODUCTION", SELF_PATHS["v3_receipt"], SELF_PATHS["v3_attestation"], SELF_PATHS["v2_receipt"], SELF_PATHS["prepared"], SELF_PATHS["v2_attestation"], SELF_PATHS["certificate"])
            elif name.startswith("external_path_"):
                bad_paths = {
                    "external_path_absolute": "/tmp/task192.json",
                    "external_path_traversal": "ci/in/task197/../task192.json",
                    "external_path_metachar": "ci/in/task197/task192;id.json",
                    "external_path_glob": "ci/in/task197/*.json",
                    "external_path_whitespace": "ci/in/task197/task 192.json",
                    "external_path_ci_out": "ci/out/task192.json",
                }
                require(name in bad_paths, "registered external path mutation")
                safe_external_path(bad_paths[name])
            elif name == "internal_path_substitution":
                exact_internal_path("ci/out/wrong.json", SELF_PATHS["v2_receipt"])
            else:
                a, b, c, x3, x2 = mutated_bundle(name, v3, v2, cert, att3_raw, att2_raw)
                validate_final_bundle(a, canon(a) + b"\n", b, canon(b) + b"\n", c, meta_value, x3, x2, "SELFTEST", SELF_PATHS["v3_receipt"], SELF_PATHS["v2_receipt"], SELF_PATHS["v3_attestation"], SELF_PATHS["v2_attestation"], SELF_V3_LINE, SELF_V2_LINE)
        except RuntimeError:
            rejected.append(name)
        else:
            raise RuntimeError("selftest mutation accepted:" + name)
    require(tuple(rejected) == MUTATIONS, "exact mutation ledger")
    expected = selftest_expected()
    require(strict_equal(expected, derived_toy_expectation(v3)), "fixture full semantic binding")
    return seal({
        "schema": SELFTEST_SCHEMA, "status": "PASS", "terminal": COMMON + "_SELFTEST_PASS",
        "execution_mode": "SELFTEST", "paths": {key: SELF_PATHS[key] for key in sorted(SELF_PATHS) if key != "summary"},
        "artifact": artifact_block(meta_value),
        "identities": {
            "v3": {"bytes": len(raw3), "sha256": sha_bytes(raw3)},
            "v2": {"bytes": len(raw2), "sha256": sha_bytes(raw2)},
            "certificate": {"bytes": len(canon(cert) + b"\n"), "sha256": sha_bytes(canon(cert) + b"\n")},
        },
        "mutation_controls": {"attempted": len(MUTATIONS), "rejected": len(rejected), "names": list(MUTATIONS)},
        "toy": expected,
    })


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("SELFTEST", "PRODUCTION"), default="SELFTEST")
    parser.add_argument("--phase", choices=("PREPARE", "FINALIZE"))
    parser.add_argument("--v3-receipt")
    parser.add_argument("--v3-attestation")
    parser.add_argument("--v2-receipt")
    parser.add_argument("--v2-attestation")
    parser.add_argument("--prepared")
    parser.add_argument("--certificate")
    parser.add_argument("--output")
    for name in sorted(ARTIFACT_KEYS):
        parser.add_argument("--" + name.replace("_", "-"), required=False)
    args = parser.parse_args(argv)
    if args.mode == "SELFTEST":
        irrelevant_paths = (args.v3_receipt, args.v3_attestation, args.v2_receipt, args.v2_attestation, args.prepared, args.certificate)
        irrelevant_metadata = tuple(getattr(args, name) for name in sorted(ARTIFACT_KEYS))
        require(args.phase is None and args.output is not None and not any(irrelevant_paths) and not any(irrelevant_metadata), "selftest argument shape")
        result = run_selftest(args.output)
        Path(args.output).write_bytes(canon(result) + b"\n")
        print(COMMON + "_PRODUCER_SELFTEST_PASS terminal=" + COMMON + "_SELFTEST_PASS")
        return 0
    try:
        require(args.phase in ("PREPARE", "FINALIZE"), "production phase")
        if args.phase == "PREPARE":
            require(args.v3_receipt and args.v3_attestation and args.v2_receipt and args.prepared and not args.v2_attestation and not args.certificate and not args.output, "production prepare argument shape")
            require_absent([args.v2_receipt, args.prepared])
            prepare(args.v3_receipt, args.v3_attestation, args.v2_receipt, args.prepared, args, "PRODUCTION", V3_LINE)
        else:
            require(args.v3_receipt and args.v3_attestation and args.v2_receipt and args.v2_attestation and args.prepared and args.certificate and not args.output, "production finalize argument shape")
            require_absent([args.certificate])
            finalize(args.v3_receipt, args.v2_receipt, args.prepared, args.certificate, args.v3_attestation, args.v2_attestation, args, "PRODUCTION", V3_LINE, V2_LINE)
    except (OSError, ValueError, UnicodeError, RuntimeError, KeyError, TypeError, AttributeError) as exc:
        print(UI + ":" + str(exc))
        return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
