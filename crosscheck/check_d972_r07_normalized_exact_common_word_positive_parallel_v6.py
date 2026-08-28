#!/usr/bin/env python3
"""Independent task325 v6 transport, kernel, and positive checker.

This file never imports the v6 producer.  Only a physical cached-v3 COMMON
receipt causes the pinned cached-v3 mathematical checker to be invoked.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import struct
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "d972-r07-normalized-exact-common-word-positive-parallel/v6"
SELFTEST_SCHEMA = SCHEMA + "/selftest"
CHECKPOINT_SCHEMA = SCHEMA + "/checkpoint-state"
FIXTURE_SCHEMA = SCHEMA + "/fixture/v6"
COMMON = "R07_NORMALIZED_EXACT_COMMON_WORD_POSITIVE_PARALLEL_V6_COMMON_WORD"
SELFTEST_PASS = "R07_NORMALIZED_EXACT_COMMON_WORD_POSITIVE_PARALLEL_V6_SELFTEST_PASS"
V3_SCHEMA = "d972-r07-normalized-exact-cached-colgen/v3"
V3_COMMON = "R07_NORMALIZED_EXACT_CACHED_COLGEN_V3_COMMON_WORD"
V3_PASS_LINE = (
    "R07_NORMALIZED_EXACT_CACHED_COLGEN_V3_CHECKER_PASS "
    "terminal=R07_NORMALIZED_EXACT_CACHED_COLGEN_V3_COMMON_WORD"
)
CHECKER_SELFTEST_PASS = (
    "R07_NORMALIZED_EXACT_COMMON_WORD_POSITIVE_PARALLEL_V6_CHECKER_SELFTEST_PASS"
)
CHECKER_PREFIX = (
    "R07_NORMALIZED_EXACT_COMMON_WORD_POSITIVE_PARALLEL_V6_CHECKER_TERMINAL"
)
PAIR_ORDER = "descriptor_order_then_typed_support_insertion_order/v3"
WINNER_ORDER = "(block,translation_blob,relator_index)/v3"
F3_ENCODING = "canonical_nonzero_1_or_2"
HOOK_NAME = "boundary_descriptor_cache_correlation_positive_parallel_v6"
FIXTURE = (
    "search/certs/"
    "d972_r07_normalized_exact_common_word_positive_parallel_selftest_v6_20260828.json"
)
WORKER_COUNTS = (2, 4)


DEPENDENCY_PINS = {
    "commission_v6": (
        "sol/luna_task_325_r07_task192_positive_only_persistent_parallel_v6.md",
        10172,
        "b22813ff9aa5250af25412db34f98b6e40996115a874e895b497e3a8753e4bf8",
    ),
    "positive_only_v140": (
        "sol/proof_r07_positive_only_common_word_colgen_v140.md",
        10073,
        "6d388a74c75d55d215b0035496c451aa9de5bbc7a8248c277e76021092b8562b",
    ),
    "history_free_v265": (
        "sol/proof_r07_history_free_positive_common_word_verifier_v265.md",
        10122,
        "fd30ccb2458691ec7844d304f220a4be7d704259318c452f928f8088552ecb0a",
    ),
    "resume_semantics_v253": (
        "sol/audit_r07_task192_boundary_resume_semantics_v253.md",
        4110,
        "a1d9f6d3d8cb31d8b261dd5cb1977865abfeba24bfc6aae7436d2a893e3ef19a",
    ),
    "mapreduce_v254": (
        "sol/proof_r07_frozen_dual_boundary_mapreduce_v254.md",
        6195,
        "e9fc7a69525200e8e1c0e8152652229227877ba923378ade8afa199c4f4ee1a0",
    ),
    "adapter_state_v255": (
        "sol/proof_r07_boundary_adapter_state_and_local_provenance_v255.md",
        8814,
        "06c93c46b48b681e0316d302058b72bc0b76fe9d12888cde3f7e45dc3a93ffa0",
    ),
    "counters_v256": (
        "sol/audit_r07_task192_cumulative_pairs_and_persistent_pool_v256.md",
        4790,
        "f5a0c6e625e5113e4213b62762267fc9a5437cafd9f9751e603b055c549c1251",
    ),
    "task319_audit": (
        "sol/sol_reply_319_r07_task311_persistent_parallel_code_performance_audit.md",
        20604,
        "9b9908eadf0f8c8204f9397d2af0511ba98959a979a00058c7b28cae9c74f981",
    ),
    "task321_commission": (
        "sol/luna_task_321_r07_task192_persistent_parallel_adapter_v5_rewrite.md",
        9128,
        "681b7a1a4b8edcd6f788f8d01aca930d60f3e61330293e70a4db47df205d2cc9",
    ),
    "task321_reply": (
        "sol/luna_reply_321_r07_task192_persistent_parallel_adapter_v5.md",
        12122,
        "bd8104b462f35979af2fd2ee820ad08a1c1c165cac6e2558a8e4eba6e7946c8b",
    ),
    "task303_producer": (
        "search/d972_r07_normalized_exact_common_word_parallel_v5.py",
        39234,
        "19a2970fcf072c25c606d0305fd999c8481353e0be20879de4be2aa26f6fb90c",
    ),
    "task303_checker": (
        "crosscheck/check_d972_r07_normalized_exact_common_word_parallel_v5.py",
        32486,
        "530d67c854017a538fa2185b8bc5c48834a785f5bd6db38452db3551695cf1df",
    ),
    "task303_driver": (
        "search/d972_r07_normalized_exact_common_word_parallel_gha_driver_v5.g",
        7971,
        "0ac1b26d1844fdc16cc2701c536f50fd5415a7ef2479e030ebde96af79af4902",
    ),
    "task303_fixture": (
        "search/certs/d972_r07_normalized_exact_common_word_parallel_selftest_v5_20260828.json",
        1195,
        "4d481ba84e3c452c79f344e66a0eea5322ec8b64c15a81f1a290c22ce18e3fc9",
    ),
    "cached_v3_producer": (
        "search/d972_r07_normalized_exact_common_word_cached_v3.py",
        193704,
        "f27b4971351832b8730fb8cce4e782e893a958dfb850203cc735c7bc3aa31f37",
    ),
    "cached_v3_checker": (
        "crosscheck/check_d972_r07_normalized_exact_common_word_cached_v3.py",
        154009,
        "dfc8cbbd96a1da45f15e01607ed343b66a78a7201f4a80952fba33aaeb361e10",
    ),
    "cached_v3_driver": (
        "search/d972_r07_normalized_exact_common_word_cached_gha_driver_v3.g",
        11548,
        "2f7ff7b459e46d014268907ff5ba5f03c035836e8f8df79a2c5f4cdc3b75351d",
    ),
    "cached_v3_fixture": (
        "search/certs/d972_r07_normalized_exact_common_word_cached_selftest_v3_20260827.json",
        276,
        "c49f434ad3daf1cc661ba45563dbb9557d436f91dca78c8ee0f47ed70332da12",
    ),
    "task298_driver": (
        "search/d972_r07_normalized_exact_common_word_cached_resume_gha_driver_v2.g",
        19682,
        "169da7aa149d68907abb435f380b9ec2994c2bc285c6a17f13431614a388f5ad",
    ),
    "task298_reply": (
        "sol/luna_reply_298_r07_task192_checkpoint_resume_transport_v2.md",
        9200,
        "732c9b1d279e9201d4cce3b432b5a4805a60d346d6104865246ce0a3030af22f",
    ),
    "checkpoint_zip": (
        "ci/in/d972_r07_normalized_exact_common_word_cached_v3_run33149728601_checkpoint.zip",
        5_001_811,
        "f3ac82a04907983d987cc2a42d06fe3b612ec2040555f40be81200969358f566",
    ),
    "checkpoint_manifest": (
        "ci/in/d972_r07_normalized_exact_common_word_cached_v3_run33149728601_checkpoint.manifest.json",
        1328,
        "6911dfe822662a17ae95c896f97573e553d15325631f1606bd0bf7f550e88302",
    ),
    "selftest_fixture_v6": (
        FIXTURE,
        4102,
        "a6ade562478f86fcd986f119f4d349949c7a866332999acb1d9605a039fcb8ad",
    ),
}

CURRENT_PINS = {
    "producer": (
        "search/d972_r07_normalized_exact_common_word_positive_parallel_v6.py",
        127376,
        "6f06465bc4599f91dee32ecab9624971c33461b12c7d38139684f578ee9d9218",
    ),
    "fixture": DEPENDENCY_PINS["selftest_fixture_v6"],
}

FALSE_CLAIMS = {
    "common_word": False,
    "separator": False,
    "negative": False,
    "finite_common_word": False,
    "cofinal_lift": False,
    "fake": False,
    "ihara_witness": False,
}
POSITIVE_CLAIMS = {
    **FALSE_CLAIMS,
    "common_word": True,
    "finite_common_word": True,
}


class CheckError(RuntimeError):
    pass


class MutationReject(RuntimeError):
    def __init__(self, stage, reason):
        super().__init__(stage + ":" + reason)
        self.stage = stage
        self.reason = reason


def require(condition, message):
    if not condition:
        raise CheckError(message)


def canonical(value):
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode("ascii")


def digest_bytes(value):
    return hashlib.sha256(value).hexdigest()


def digest_obj(value):
    return digest_bytes(canonical(value))


def dependency_public():
    return {
        label: {"path": path, "bytes": size, "sha256": sha}
        for label, (path, size, sha) in DEPENDENCY_PINS.items()
    }


def pins_digest():
    return digest_obj(dependency_public())


def authenticate_local_sources():
    for table_name, table in (
            ("dependency", DEPENDENCY_PINS), ("current", CURRENT_PINS)):
        for label, (relative, expected_bytes, expected_sha) in table.items():
            path = ROOT / relative
            if not path.is_file():
                raise CheckError(table_name + " source missing:" + label)
            raw = path.read_bytes()
            if len(raw) != expected_bytes or digest_bytes(raw) != expected_sha:
                raise CheckError(table_name + " source pin:" + label)


def validate_outer_seal(value):
    require(isinstance(value, dict), "outer object")
    body = dict(value)
    claimed = body.pop("self_digest_sha256", None)
    require(isinstance(claimed, str) and claimed == digest_obj(body),
            "outer self digest")


def validate_v3_seal(value):
    require(isinstance(value, dict), "cached-v3 object")
    body = dict(value)
    claimed = body.pop("self_digest", None)
    require(isinstance(claimed, str) and claimed == digest_obj(body),
            "cached-v3 self digest")


def validate_source_binding(receipt):
    require(receipt.get("source_pins") == dependency_public() and
            receipt.get("source_pins_sha256") == pins_digest(),
            "outer source pins")


def validate_claims(claims, positive):
    expected = POSITIVE_CLAIMS if positive else FALSE_CLAIMS
    require(claims == expected, "claim vector")


def validate_cleanup(cleanup, allow_not_started=True):
    require(isinstance(cleanup, dict) and cleanup.get("complete") is True and
            cleanup.get("live_pids_after_join") == [],
            "worker cleanup/live PID")
    transitions = cleanup.get("transitions")
    permitted = [
        ["started", "closing", "joined"],
        ["started", "closing", "terminating", "joined"],
    ]
    if allow_not_started:
        permitted.append(["not_started"])
    require(transitions in permitted, "worker cleanup state transition")
    started = cleanup.get("started_pids")
    require(isinstance(started, list) and
            all(type(pid) is int and pid > 0 for pid in started),
            "worker PID roster")


def validate_counters(counters):
    names = {
        "historical_attempted_pairs", "historical_committed_pairs",
        "historical_discarded_pairs", "historical_retried_pairs",
        "attempted_pairs", "committed_pairs", "discarded_pairs",
        "retried_pairs", "historical_attempted_epochs",
        "historical_committed_epochs", "historical_discarded_epochs",
        "historical_retried_epochs", "attempted_epochs",
        "committed_epochs", "discarded_epochs", "retried_epochs",
        "retry_pending_pairs",
    }
    require(isinstance(counters, dict) and set(counters) == names and
            all(type(counters[name]) is int and counters[name] >= 0
                for name in names), "adapter counter shape")
    require(counters["attempted_pairs"] ==
            counters["committed_pairs"] + counters["discarded_pairs"] and
            counters["attempted_epochs"] ==
            counters["committed_epochs"] + counters["discarded_epochs"],
            "adapter counter conservation")
    for unit in ("pairs", "epochs"):
        for stem in ("attempted", "committed", "discarded", "retried"):
            require(counters[stem + "_" + unit] >=
                    counters["historical_" + stem + "_" + unit],
                    "historical adapter counter reset")
    require(counters["retried_pairs"] <= counters["attempted_pairs"] and
            counters["retried_epochs"] <= counters["attempted_epochs"],
            "adapter retry bounds")


def validate_adapter_state(state):
    require(isinstance(state, dict) and
            state.get("schema") == CHECKPOINT_SCHEMA and
            state.get("hook") == HOOK_NAME and
            state.get("owner") ==
            "cached-v3 BoundaryDescriptorCache.correlation" and
            state.get("source_pins_sha256") == pins_digest(),
            "adapter owner/source binding")
    require(state.get("persistent_processes") is True and
            state.get("serial_dual_epochs") is True and
            state.get("atomic_full_epoch") is True and
            state.get("pair_order") == PAIR_ORDER and
            state.get("winner_order") == WINNER_ORDER and
            state.get("f3_encoding") == F3_ENCODING and
            state.get("historical_replay_claim") is False,
            "adapter execution contract")
    require(state.get("worker_count") in WORKER_COUNTS,
            "adapter worker count")
    validate_counters(state.get("counters"))
    serialization = state.get("serialization")
    require(isinstance(serialization, dict) and set(serialization) == {
        "sent_bytes", "received_bytes", "max_frame_bytes",
        "max_epoch_inflight_bytes", "support_bytes_last_epoch",
        "support_cap_bytes", "frame_cap_bytes", "epoch_cap_bytes",
    } and all(type(value) is int and value >= 0
              for value in serialization.values()),
            "adapter serialization counters")
    require(serialization["support_cap_bytes"] == 1_048_576 and
            serialization["frame_cap_bytes"] == 33_554_432 and
            serialization["epoch_cap_bytes"] == 268_435_456 and
            serialization["support_bytes_last_epoch"] <=
            serialization["support_cap_bytes"] and
            serialization["max_frame_bytes"] <=
            serialization["frame_cap_bytes"] and
            serialization["max_epoch_inflight_bytes"] <=
            serialization["epoch_cap_bytes"],
            "adapter serialization caps")
    resource = state.get("resource")
    require(isinstance(resource, dict) and set(resource) == {
        "parent_rss_peak_bytes", "children_rss_peak_bytes",
        "aggregate_rss_peak_bytes", "rss_samples", "worker_restarts",
        "checkpoint_bytes",
    } and all(type(value) is int and value >= 0
              for value in resource.values()) and
            resource["aggregate_rss_peak_bytes"] >=
            resource["parent_rss_peak_bytes"] and
            resource["worker_restarts"] == 0,
            "adapter live resources")
    require(state.get("epoch_records_retained") in (0, 1) and
            isinstance(state.get("epoch_chain_sha256"), str) and
            len(state["epoch_chain_sha256"]) == 64,
            "bounded epoch state")
    validate_cleanup(state.get("cleanup"))


def typed_boundary_ancestry(inner):
    columns = inner.get("columns", [])
    answer = []
    for basis_index, witness in enumerate(inner.get("nu_kernel_ancestry", []), 1):
        boundary_terms = []
        for item in witness.get("boundary_coefficients", []):
            require(isinstance(item, list) and len(item) == 2,
                    "boundary coefficient item")
            column_id, coefficient = int(item[0]), int(item[1])
            require(1 <= column_id <= len(columns) and coefficient in (1, 2),
                    "boundary coefficient range")
            record = columns[column_id - 1]
            provenance = record.get("provenance", {})
            require(record.get("family") == "boundary" and
                    provenance.get("family") == "boundary",
                    "boundary ancestry typed family")
            boundary_terms.append({
                "column_id": column_id,
                "coefficient": coefficient,
                "block": int(provenance["block"]),
                "base_relator_index": int(provenance["base_relator_index"]),
                "translation_hex": str(provenance["translation_hex"]),
                "scalar": int(provenance["scalar"]),
                "left_translation_gate": provenance.get(
                    "left_translation_gate"
                ),
                "complete_support_occurrence_accumulation": provenance.get(
                    "complete_support_occurrence_accumulation"
                ),
                "contributing_pairs": copy.deepcopy(
                    provenance.get("contributing_pairs", [])
                ),
            })
        answer.append({
            "basis_index": basis_index,
            "nu": copy.deepcopy(witness.get("nu")),
            "coefficients": copy.deepcopy(witness.get("coefficients", [])),
            "boundary_coefficients": copy.deepcopy(
                witness.get("boundary_coefficients", [])
            ),
            "correction_coefficients": copy.deepcopy(
                witness.get("correction_coefficients", [])
            ),
            "boundary_terms": boundary_terms,
            "B_zero_sha256": witness.get("B_zero_sha256"),
            "correction_boundary_zero_sha256": witness.get(
                "correction_boundary_zero_sha256"
            ),
        })
    return answer


def independent_compact_view(inner):
    require(inner.get("schema") == V3_SCHEMA and
            inner.get("terminal") == V3_COMMON and
            inner.get("status") == "COMMON_WORD",
            "inner cached-v3 COMMON envelope")
    exactification = inner.get("exactification", {})
    words = exactification.get("r_words", {})
    literal = exactification.get("literal", {})
    require(set(words) == {"3", "9", "12"} and
            set(literal) == {"c_star", "v0", "u0", "h", "c_exact"},
            "inner exactification words")
    return {
        "c_star": copy.deepcopy(inner.get("correction_word", [])),
        "solution_coefficients": copy.deepcopy(
            inner.get("solution_coefficients", [])
        ),
        "exact_words": copy.deepcopy(literal),
        "registered_relators": {
            "3": copy.deepcopy(words["3"]),
            "9": copy.deepcopy(words["9"]),
            "12": copy.deepcopy(words["12"]),
        },
        "exponents": copy.deepcopy(exactification.get("exponents", {})),
        "A": exactification.get("A"),
        "B": exactification.get("B"),
        "joint_kernel_replay": copy.deepcopy(
            exactification.get("joint_kernel_replay", {})
        ),
        "direct_all_seven_replay": copy.deepcopy(
            inner.get("exact_direct_replay", {})
        ),
        "typed_boundary_ancestry": typed_boundary_ancestry(inner),
        "boundary_words_not_inserted": inner.get(
            "boundary_words_not_inserted"
        ),
    }


def expected_sidecar(receipt_path, suffix):
    return receipt_path.with_suffix(receipt_path.suffix + suffix)


def validate_ref_path(reference, expected):
    require(isinstance(reference, dict) and
            reference.get("path") == expected.relative_to(ROOT).as_posix() and
            reference.get("basename") == expected.name,
            "sidecar path/basename binding")


def read_bound_json(reference, expected, seal_field):
    validate_ref_path(reference, expected)
    require(expected.is_file(), "bound sidecar missing")
    raw = expected.read_bytes()
    require(raw and raw.endswith(b"\n") and
            reference.get("bytes") == len(raw) and
            reference.get("sha256") == digest_bytes(raw),
            "bound sidecar byte digest")
    value = json.loads(raw.decode("utf-8"))
    require(canonical(value) + b"\n" == raw, "bound sidecar canonical bytes")
    if seal_field == "self_digest":
        validate_v3_seal(value)
    else:
        validate_outer_seal(value)
    require(reference.get(seal_field) == value.get(seal_field),
            "bound sidecar self digest")
    return value, raw


def invoke_v3_checker_once(inner_path, timeout_seconds):
    checker_path = ROOT / DEPENDENCY_PINS["cached_v3_checker"][0]
    completed = subprocess.run(
        [sys.executable, "-B", str(checker_path), str(inner_path)],
        cwd=ROOT,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="strict",
        timeout=float(timeout_seconds),
        check=False,
    )
    stdout_lines = completed.stdout.splitlines()
    require(completed.returncode == 0 and
            stdout_lines == [V3_PASS_LINE] and
            completed.stderr == "",
            "cached-v3 exact-one full-line PASS terminal")
    return V3_PASS_LINE


def validate_positive(receipt, receipt_path, timeout_seconds):
    require(receipt.get("schema") == SCHEMA and
            receipt.get("status") == "COMMON_WORD" and
            receipt.get("terminal") == COMMON and
            receipt.get("positive_only") is True and
            receipt.get("retrospective_epoch_replay_claim") is None,
            "v6 positive envelope")
    validate_source_binding(receipt)
    validate_adapter_state(receipt.get("adapter_state"))
    validate_claims(receipt.get("claims"), True)
    require(receipt.get("checkpoint") is None and
            not expected_sidecar(receipt_path, ".checkpoint.json").exists(),
            "COMMON checkpoint/orphan sidecar")
    inner_path = expected_sidecar(receipt_path, ".inner_v3.json")
    inner, _ = read_bound_json(
        receipt.get("inner_cached_v3"), inner_path, "self_digest"
    )
    reference = receipt["inner_cached_v3"]
    require(reference.get("schema") == V3_SCHEMA and
            reference.get("terminal") == V3_COMMON and
            reference.get("source_pins") == {
                label: dependency_public()[label]
                for label in (
                    "cached_v3_producer", "cached_v3_checker",
                    "cached_v3_driver", "cached_v3_fixture",
                )
            }, "inner cached-v3 immutable pins")
    line = invoke_v3_checker_once(inner_path, timeout_seconds)
    compact = independent_compact_view(inner)
    require(receipt.get("compact_positive_view") == compact,
            "outer/accepted-inner compact view mismatch")
    return {
        "mathematical_positive_accepted": True,
        "cached_v3_checker_invocations": 1,
        "cached_v3_checker_full_line": line,
        "inner_receipt_sha256": reference["sha256"],
        "compact_view_sha256": digest_obj(compact),
    }


def validate_checkpoint_sidecar(receipt, receipt_path):
    checkpoint_path = expected_sidecar(receipt_path, ".checkpoint.json")
    checkpoint, raw = read_bound_json(
        receipt.get("checkpoint"), checkpoint_path, "self_digest"
    )
    reference = receipt["checkpoint"]
    require(reference.get("schema") == checkpoint.get("schema") and
            reference.get("source_pins_sha256") == pins_digest(),
            "checkpoint source/schema reference")
    state = checkpoint.get("positive_parallel_v6")
    require(state == receipt.get("adapter_state"),
            "checkpoint adapter-state binding")
    validate_adapter_state(state)
    clean = state.get("next_clean_epoch")
    require(isinstance(clean, dict) and clean == {
        "atomic_cursor": 0,
        "prefix_accumulator": [],
        "partial_epoch_committed": False,
        "retry_pending_pairs": state["counters"]["retry_pending_pairs"],
    }, "last-safe next clean epoch")
    require(state.get("historical_replay_claim") is False and
            state.get("resource", {}).get("checkpoint_bytes") == len(raw) and
            checkpoint.get("monitor", {}).get("counters", {}).get(
                "checkpoint_bytes") == len(raw),
            "checkpoint live bytes/replay boundary")
    return reference["sha256"]


def validate_nonpositive(receipt, receipt_path):
    require(receipt.get("schema") == SCHEMA and
            receipt.get("positive_only") is True and
            receipt.get("retrospective_epoch_replay_claim") is None,
            "v6 nonpositive envelope")
    validate_source_binding(receipt)
    validate_claims(receipt.get("claims"), False)
    validate_adapter_state(receipt.get("adapter_state"))
    terminal = str(receipt.get("terminal", ""))
    status = receipt.get("status")
    require(status in ("UNKNOWN_INPUT", "UNKNOWN_RESOURCE") and
            terminal.startswith(status + ":") and
            receipt.get("reason") == terminal[len(status) + 1:] and
            bool(receipt.get("reason")),
            "typed nonpositive terminal/reason")
    require(receipt.get("inner_cached_v3") is None and
            receipt.get("compact_positive_view") is None and
            not expected_sidecar(receipt_path, ".inner_v3.json").exists(),
            "nonpositive inner COMMON sidecar")
    checkpoint_sha = None
    if status == "UNKNOWN_RESOURCE":
        require(str(receipt.get("inner_terminal", "")).startswith(
            "UNKNOWN_RESOURCE:"
        ) and receipt.get("reason", "").startswith("cached_v3:"),
                "resource owner terminal binding")
        checkpoint_sha = validate_checkpoint_sidecar(receipt, receipt_path)
    else:
        require(receipt.get("checkpoint") is None and
                not expected_sidecar(receipt_path, ".checkpoint.json").exists(),
                "UNKNOWN_INPUT checkpoint sidecar")
    return {
        "mathematical_positive_accepted": False,
        "cached_v3_checker_invocations": 0,
        "transport_resource_checked": True,
        "checkpoint_sha256": checkpoint_sha,
    }


def _mreject(stage, reason):
    raise MutationReject(stage, reason)


def _c17_descriptor_check(descriptors):
    previous = None
    for descriptor in descriptors:
        if set(descriptor) != {
                "block", "relator_index", "component", "h_hex",
                "base_coefficient"}:
            raise CheckError("C17 descriptor fields")
        raw = bytes.fromhex(str(descriptor["h_hex"]))
        key = (
            int(descriptor["block"]), int(descriptor["relator_index"]),
            int(descriptor["component"]), raw,
            int(descriptor["base_coefficient"]),
        )
        require(len(raw) == 1 and raw[0] < 17 and key[4] in (0, 1, 2),
                "C17 canonical descriptor")
        require(previous is None or previous <= key,
                "C17 descriptor canonical order")
        previous = key


def _encode_support_independent(support):
    raw = bytearray(struct.pack(">I", len(support)))
    seen = set()
    typed = {}
    for position, item in enumerate(support):
        if not isinstance(item, list) or len(item) != 4:
            raise CheckError("C17 support record")
        block, component = int(item[0]), int(item[1])
        blob = bytes.fromhex(str(item[2]))
        coefficient = int(item[3])
        require(len(blob) == 1 and blob[0] < 17 and coefficient in (1, 2),
                "C17 canonical support")
        identity = (block, component, blob)
        require(identity not in seen, "C17 duplicate support")
        seen.add(identity)
        raw.extend(struct.pack(">HHBI", block, component, coefficient, 1))
        raw.extend(blob)
        typed.setdefault((block, component), []).append(
            (blob[0], blob.hex(), coefficient, position)
        )
    return bytes(raw), typed


def _expanded_pairs(descriptors, support):
    support_raw, typed = _encode_support_independent(support)
    pairs = []
    offsets = [0]
    for descriptor in descriptors:
        block = int(descriptor["block"])
        relator = int(descriptor["relator_index"])
        component = int(descriptor["component"])
        h = bytes.fromhex(descriptor["h_hex"])[0]
        base = int(descriptor["base_coefficient"])
        for g, g_hex, coefficient, support_position in typed.get(
                (block, component), []):
            t = (g - h) % 17
            require((t + h) % 17 == g, "independent C17 t*h=g")
            pairs.append({
                "key": (block, relator, "%02x" % t),
                "coefficient": base * coefficient % 3,
                "provenance": {
                    "component": component, "g_hex": g_hex,
                    "h_hex": "%02x" % h,
                    "lambda_coefficient": coefficient,
                    "base_coefficient": base,
                    "support_position": support_position,
                },
            })
        offsets.append(len(pairs))
    return pairs, offsets, support_raw, typed


def _winner_order_public(key):
    return (int(key[0]), bytes.fromhex(str(key[2])), int(key[1]))


def _accumulate_pair_slice(pairs, start, stop):
    accumulator = {}
    first = {}
    for pair_index in range(start, stop):
        pair = pairs[pair_index]
        key = tuple(pair["key"])
        value = (accumulator.get(key, 0) + int(pair["coefficient"])) % 3
        if value:
            accumulator[key] = value
        else:
            accumulator.pop(key, None)
        first.setdefault(key, {
            "pair_index": pair_index,
            "component": pair["provenance"]["component"],
            "g_hex": pair["provenance"]["g_hex"],
            "h_hex": pair["provenance"]["h_hex"],
            "lambda_coefficient": pair["provenance"]["lambda_coefficient"],
            "base_coefficient": pair["provenance"]["base_coefficient"],
        })
    winner = min(accumulator, key=_winner_order_public) if accumulator else None
    return accumulator, winner, None if winner is None else first[winner]


def _accumulator_public(accumulator):
    return [
        [[key[0], key[1], key[2]], accumulator[key]]
        for key in sorted(accumulator, key=_winner_order_public)
        if accumulator[key] % 3
    ]


def _merge_accumulator(target, source):
    for key, coefficient in source.items():
        value = (target.get(key, 0) + coefficient) % 3
        if value:
            target[key] = value
        else:
            target.pop(key, None)


def _expected_intervals(total, workers):
    active = min(int(total), int(workers))
    if not active:
        return []
    return [[index * total // active, (index + 1) * total // active]
            for index in range(active)]


def _typed_digests(typed):
    return {
        "%d:%d" % key: digest_obj([
            [item[1], item[2], item[3]] for item in values
        ]) for key, values in sorted(typed.items())
    }


def _winner_provenance(descriptors, support, selected):
    if selected is None:
        return []
    block, relator, translation_hex = selected
    translation = bytes.fromhex(translation_hex)[0]
    lookup = {
        (int(item[0]), int(item[1]), str(item[2])): int(item[3])
        for item in support
    }
    answer = []
    for descriptor in descriptors:
        if int(descriptor["block"]) != int(block) or \
                int(descriptor["relator_index"]) != int(relator):
            continue
        h = bytes.fromhex(descriptor["h_hex"])[0]
        g_hex = "%02x" % ((translation + h) % 17)
        coefficient = lookup.get((
            int(block), int(descriptor["component"]), g_hex
        ))
        if coefficient is not None:
            answer.append({
                "component": int(descriptor["component"]),
                "g_hex": g_hex, "h_hex": str(descriptor["h_hex"]),
                "lambda_coefficient": coefficient,
                "base_coefficient": int(descriptor["base_coefficient"]),
            })
    return answer


def _translated_row(descriptors, selected):
    if selected is None:
        return []
    block, relator, translation_hex = selected
    translation = bytes.fromhex(translation_hex)[0]
    row = {}
    for descriptor in descriptors:
        if int(descriptor["block"]) != int(block) or \
                int(descriptor["relator_index"]) != int(relator):
            continue
        h = bytes.fromhex(descriptor["h_hex"])[0]
        key = (
            int(block), int(descriptor["component"]),
            "%02x" % ((translation + h) % 17),
        )
        value = (row.get(key, 0) + int(descriptor["base_coefficient"])) % 3
        if value:
            row[key] = value
        else:
            row.pop(key, None)
    return [
        [[key[0], key[1], key[2]], row[key]]
        for key in sorted(row, key=lambda item: (
            item[0], bytes.fromhex(item[2]), item[1]
        ))
    ]


def _direct_scalar(row, support):
    dual = {
        (int(item[0]), int(item[1]), str(item[2])): int(item[3])
        for item in support
    }
    return sum(dual.get(tuple(item[0]), 0) * int(item[1])
               for item in row) % 3


def _result_digest(shard):
    body = {key: copy.deepcopy(value) for key, value in shard.items()
            if key != "result_digest"}
    return digest_obj(body)


def _validate_kernel_selftest(run, descriptors, worker_count):
    try:
        _c17_descriptor_check(descriptors)
        pairs, offsets, support_raw, typed = _expanded_pairs(
            descriptors, run.get("support")
        )
    except (CheckError, TypeError, ValueError, KeyError):
        _mreject("kernel.dual", "noncanonical_c17_codec")
    support = run["support"]
    dual_digest = digest_obj(support)
    if run.get("dual_digest") != dual_digest or \
            run.get("identity", {}).get("dual_digest") != dual_digest or \
            run.get("support_buffer_hex") != support_raw.hex():
        _mreject("kernel.dual", "dual_digest")
    descriptor_digest = digest_obj(descriptors)
    identity = run.get("identity", {})
    if run.get("descriptor_digest") != descriptor_digest or \
            identity.get("descriptor_digest") != descriptor_digest:
        _mreject("kernel.epoch", "cross_epoch_result")
    if identity.get("support_public_digest") != digest_obj(support) or \
            identity.get("support_buffer_digest") != digest_bytes(support_raw) or \
            identity.get("typed_support_digests") != _typed_digests(typed) or \
            identity.get("prefix_offsets") != offsets or \
            identity.get("prefix_digest") != digest_obj(offsets) or \
            identity.get("expanded_pair_count") != len(pairs) or \
            identity.get("pair_order") != PAIR_ORDER or \
            identity.get("winner_order") != WINNER_ORDER or \
            identity.get("f3_encoding") != F3_ENCODING or \
            identity.get("owner_epoch_context") != {"universe": "C17"} or \
            type(identity.get("serial_epoch")) is not int or \
            identity.get("serial_epoch") <= 0 or \
            digest_obj(identity) != run.get("epoch_id"):
        _mreject("kernel.epoch", "cross_epoch_result")
    expected_cover = _expected_intervals(len(pairs), worker_count)
    cover = run.get("intervals")
    shards = run.get("shards")
    if not isinstance(cover, list) or not isinstance(shards, list) or \
            len(cover) != len(shards):
        _mreject("kernel.cover", "missing_interval")
    if cover != expected_cover:
        for left, right in zip(cover, cover[1:]):
            if right[0] < left[1]:
                _mreject("kernel.cover", "overlapping_interval")
        _mreject("kernel.cover", "missing_interval")
    merged = {}
    for worker_id, (interval, shard) in enumerate(zip(cover, shards)):
        if shard.get("dual_digest") != dual_digest:
            _mreject("kernel.dual", "dual_digest")
        if shard.get("epoch_id") != run.get("epoch_id") or \
                shard.get("descriptor_digest") != descriptor_digest or \
                shard.get("support_digest") != digest_bytes(support_raw) or \
                shard.get("prefix_digest") != digest_obj(offsets):
            _mreject("kernel.epoch", "cross_epoch_result")
        if shard.get("complete") is not True or \
                shard.get("attempted") != interval[1] - interval[0]:
            _mreject("kernel.completion", "partial_return")
        if shard.get("worker_id") != worker_id or \
                shard.get("interval") != interval:
            _mreject("kernel.cover", "missing_interval")
        expected, local_winner, local_provenance = _accumulate_pair_slice(
            pairs, interval[0], interval[1]
        )
        if shard.get("accumulator") != _accumulator_public(expected):
            _mreject("kernel.merge", "accumulator")
        local_public = None if local_winner is None else list(local_winner)
        if shard.get("local_winner") != local_public or \
                shard.get("local_provenance") != local_provenance:
            _mreject("kernel.winner", "winner_provenance")
        if shard.get("result_digest") != _result_digest(shard):
            _mreject("kernel.merge", "accumulator")
        _merge_accumulator(merged, expected)
    if run.get("accumulator") != _accumulator_public(merged):
        _mreject("kernel.merge", "accumulator")
    winner = min(merged, key=_winner_order_public) if merged else None
    winner_public = None if winner is None else list(winner)
    scalar = 0 if winner is None else merged[winner]
    if run.get("selected_key") != winner_public or \
            run.get("selected_scalar") != scalar or \
            run.get("winner_provenance") != _winner_provenance(
                descriptors, support, winner_public):
        _mreject("kernel.winner", "winner_provenance")
    row = _translated_row(descriptors, winner_public)
    direct = _direct_scalar(row, support)
    if run.get("translated_row") != row or \
            run.get("direct_scalar") != direct or direct != scalar:
        _mreject("kernel.scalar", "direct_scalar")
    if run.get("pair_count") != len(pairs):
        _mreject("kernel.cover", "missing_interval")
    if run.get("batch_complete") is not True:
        _mreject("kernel.completion", "partial_return")


def _kernel_projection(run):
    return {
        key: copy.deepcopy(run[key]) for key in (
            "accumulator", "selected_key", "selected_scalar",
            "winner_provenance", "translated_row", "direct_scalar",
            "pair_count", "batch_complete",
        )
    }


def _serial_digest(descriptors, support):
    pairs, _, _, _ = _expanded_pairs(descriptors, support)
    accumulator, winner, _ = _accumulate_pair_slice(pairs, 0, len(pairs))
    winner_public = None if winner is None else list(winner)
    row = _translated_row(descriptors, winner_public)
    direct = _direct_scalar(row, support)
    return digest_obj({
        "pair_count": len(pairs),
        "accumulator": _accumulator_public(accumulator),
        "selected_key": winner_public,
        "selected_scalar": 0 if winner is None else accumulator[winner],
        "direct_scalar": direct,
        "row": row,
        "winner_contributors": [
            {
                "pair_index": index,
                "support_position": pair["provenance"]["support_position"],
                "component": pair["provenance"]["component"],
                "g_hex": pair["provenance"]["g_hex"],
                "h_hex": pair["provenance"]["h_hex"],
                "lambda_coefficient": pair["provenance"][
                    "lambda_coefficient"
                ],
                "base_coefficient": pair["provenance"]["base_coefficient"],
            }
            for index, pair in enumerate(pairs)
            if winner is not None and tuple(pair["key"]) == winner
        ],
    })


def _mutation_outer_seal(value, stage):
    if not isinstance(value, dict):
        _mreject(stage, "shape")
    body = dict(value)
    claimed = body.pop("self_digest_sha256", None)
    if claimed != digest_obj(body):
        _mreject(stage, "seal")


def _synthetic_compact(inner):
    return {
        "c_star": copy.deepcopy(inner["correction_word"]),
        "exact_words": copy.deepcopy(inner["exact_words"]),
        "registered_relators": copy.deepcopy(inner["registered_relators"]),
        "exponents": copy.deepcopy(inner["exponents"]),
        "direct_all_seven_replay": copy.deepcopy(
            inner["direct_all_seven_replay"]
        ),
        "typed_boundary_ancestry": copy.deepcopy(
            inner["typed_boundary_ancestry"]
        ),
    }


def _mutation_claims(claims, positive):
    expected = POSITIVE_CLAIMS if positive else FALSE_CLAIMS
    if not isinstance(claims, dict):
        _mreject("claims", "shape")
    for field in ("separator", "cofinal_lift", "fake", "ihara_witness"):
        if claims.get(field) is not expected[field]:
            _mreject("claims", field)
    if claims != expected:
        _mreject("claims", "claim_vector")


def _mutation_cleanup(cleanup):
    if not isinstance(cleanup, dict) or cleanup.get("complete") is not True or \
            cleanup.get("live_pids_after_join") != [] or \
            cleanup.get("transitions") not in (
                ["started", "closing", "joined"],
                ["started", "closing", "terminating", "joined"],
                ["not_started"],
            ):
        _mreject("cleanup", "child_alive")


def _mutation_counter_check(counters):
    try:
        validate_counters(counters)
    except CheckError:
        _mreject("counters", "historical_reset")


def _validate_synthetic_positive(value):
    _mutation_outer_seal(value, "positive.inner")
    if value.get("status") != "COMMON_WORD" or \
            value.get("terminal") != "SYNTHETIC_V6_COMMON" or \
            value.get("checkpoint") is not None:
        _mreject("envelope", "terminal")
    try:
        raw = bytes.fromhex(str(value.get("inner_raw_hex", "")))
        inner = json.loads(raw.decode("ascii"))
    except (ValueError, UnicodeError, json.JSONDecodeError):
        _mreject("positive.inner", "inner_digest")
    reference = value.get("inner_ref", {})
    if reference.get("bytes") != len(raw) or \
            reference.get("sha256") != digest_bytes(raw):
        _mreject("positive.inner", "inner_digest")
    body = dict(inner)
    claimed = body.pop("self_digest", None)
    if claimed != digest_obj(body) or reference.get("self_digest") != claimed or \
            reference.get("terminal") != inner.get("terminal"):
        _mreject("positive.inner", "inner_digest")
    exact_line = (
        "SYNTHETIC_CACHED_V3_CHECKER_PASS "
        "terminal=SYNTHETIC_CACHED_V3_COMMON"
    )
    if value.get("checker_invocations") != 1 or \
            value.get("checker_line") != exact_line:
        _mreject("positive.checker", "checker_terminal")
    if value.get("compact_view") != _synthetic_compact(inner):
        _mreject("positive.compact", "compact_view")
    _mutation_claims(value.get("claims"), True)
    if value.get("output_fresh") is not True:
        _mreject("transport", "stale_output")


def _validate_synthetic_resource(value):
    _mutation_outer_seal(value, "resource.checkpoint")
    if value.get("status") != "UNKNOWN_RESOURCE" or \
            value.get("terminal") != "UNKNOWN_RESOURCE:synthetic_live_timeout":
        _mreject("envelope", "terminal")
    adapter = value.get("adapter_state", {})
    _mutation_cleanup(adapter.get("cleanup"))
    _mutation_counter_check(adapter.get("counters"))
    try:
        raw = bytes.fromhex(str(value.get("checkpoint_raw_hex", "")))
        checkpoint = json.loads(raw.decode("ascii"))
    except (ValueError, UnicodeError, json.JSONDecodeError):
        _mreject("resource.checkpoint", "checkpoint_binding")
    reference = value.get("checkpoint_ref", {})
    if reference.get("bytes") != len(raw) or \
            reference.get("sha256") != digest_bytes(raw):
        _mreject("resource.checkpoint", "checkpoint_binding")
    body = dict(checkpoint)
    claimed = body.pop("self_digest", None)
    if claimed != digest_obj(body) or reference.get("self_digest") != claimed or \
            checkpoint.get("positive_parallel_v6") != adapter:
        _mreject("resource.checkpoint", "checkpoint_binding")
    claims = value.get("claims", {})
    if claims.get("common_word") is not False or \
            claims.get("finite_common_word") is not False:
        _mreject("resource.claims", "positive_claim")
    _mutation_claims(claims, False)
    if value.get("inner_cached_v3") is not None or \
            value.get("compact_positive_view") is not None or \
            value.get("checker_invocations") != 0:
        _mreject("resource.claims", "positive_claim")
    if value.get("output_fresh") is not True:
        _mreject("transport", "stale_output")


def _validate_document(document, fixture):
    if not isinstance(document, dict) or document.get("schema") != \
            SELFTEST_SCHEMA + "/document":
        _mreject("document", "schema")
    full = fixture["descriptors"]
    if document.get("full_descriptors") != full:
        _mreject("kernel.epoch", "cross_epoch_result")
    cases = document.get("cases")
    if not isinstance(cases, list) or \
            [case.get("name") for case in cases] != \
            [case["name"] for case in fixture["cases"]]:
        _mreject("kernel.epoch", "cross_epoch_result")
    for case, specification in zip(cases, fixture["cases"]):
        descriptors = full[:int(specification["descriptor_prefix"])]
        if case.get("descriptors") != descriptors or \
                case.get("run", {}).get("support") != specification["support"]:
            _mreject("kernel.epoch", "cross_epoch_result")
        _validate_kernel_selftest(case["run"], descriptors, 2)
        if case.get("serial_digest") != _serial_digest(
                descriptors, specification["support"]):
            _mreject("kernel.merge", "accumulator")
        _mutation_cleanup(case.get("pool_cleanup"))
    persistent = document.get("persistent_epochs", {})
    if set(persistent) != {"2", "4"}:
        _mreject("kernel.cover", "missing_interval")
    for workers in WORKER_COUNTS:
        record = persistent[str(workers)]
        runs = record.get("runs")
        if not isinstance(runs, list) or len(runs) != 3 or \
                record.get("one_roster_reused") is not True or \
                record.get("started_pids") != record.get("cleanup", {}).get(
                    "started_pids") or \
                len(record.get("started_pids", [])) != workers or \
                len(set(record.get("started_pids", []))) != workers:
            _mreject("kernel.epoch", "cross_epoch_result")
        for run, epoch in zip(runs, fixture["persistent_epochs"]):
            if run.get("support") != epoch["support"]:
                _mreject("kernel.epoch", "cross_epoch_result")
            _validate_kernel_selftest(run, full, workers)
        if len({run["dual_digest"] for run in runs}) != 3:
            _mreject("kernel.epoch", "cross_epoch_result")
        _mutation_cleanup(record.get("cleanup"))
    for run2, run4 in zip(persistent["2"]["runs"],
                          persistent["4"]["runs"]):
        if _kernel_projection(run2) != _kernel_projection(run4):
            _mreject("kernel.merge", "accumulator")
    faults = document.get("fault_controls")
    if not isinstance(faults, list) or \
            [item.get("name") for item in faults] != fixture["faults"]:
        _mreject("kernel.completion", "partial_return")
    expected_faults = {
        "live_timeout": ("wall_seconds", "live_deadline"),
        "worker_death": ("worker_death", "worker_death"),
        "partial_return": ("worker_protocol", "merge_protocol:partial worker return"),
    }
    for fault in faults:
        expected_cap, expected_reason = expected_faults[fault["name"]]
        error = fault.get("error", {})
        if fault.get("rejected") is not True or \
                error.get("cap") != expected_cap or \
                error.get("reason") != expected_reason:
            _mreject("kernel.completion", "partial_return")
        _mutation_cleanup(fault.get("cleanup"))
        _mutation_counter_check(fault.get("counters"))
    _validate_synthetic_positive(document.get("positive_envelope"))
    _validate_synthetic_resource(document.get("resource_envelope"))


def _reseal_synthetic(value):
    answer = copy.deepcopy(value)
    answer.pop("self_digest_sha256", None)
    answer["self_digest_sha256"] = digest_obj(answer)
    return answer


def _refresh_result(shard):
    shard["result_digest"] = _result_digest(shard)


def _mutate(document, name):
    run = document["persistent_epochs"]["2"]["runs"][2]
    positive = document["positive_envelope"]
    resource = document["resource_envelope"]
    if name == "wrong_dual_digest":
        run["shards"][0]["dual_digest"] = "0" * 64
        _refresh_result(run["shards"][0])
    elif name == "noncanonical_c17_alias":
        run["support"][0][2] = "14"
    elif name == "missing_interval":
        run["intervals"].pop()
        run["shards"].pop()
    elif name == "overlapping_interval":
        run["intervals"][1][0] = run["intervals"][0][1] - 1
        run["shards"][1]["interval"] = copy.deepcopy(run["intervals"][1])
        _refresh_result(run["shards"][1])
    elif name == "changed_accumulator":
        run["accumulator"][0][1] = 1 if run["accumulator"][0][1] == 2 else 2
    elif name == "changed_winner_provenance":
        run["winner_provenance"][0]["g_hex"] = "00"
    elif name == "changed_direct_scalar":
        run["direct_scalar"] = 1 if run["direct_scalar"] != 1 else 2
    elif name == "cross_epoch_result":
        run["shards"][0]["epoch_id"] = \
            document["persistent_epochs"]["2"]["runs"][1]["epoch_id"]
        _refresh_result(run["shards"][0])
    elif name == "partial_return_accepted":
        run["shards"][0]["complete"] = False
        run["shards"][0]["attempted"] -= 1
        _refresh_result(run["shards"][0])
    elif name == "child_left_alive":
        resource["adapter_state"]["cleanup"]["live_pids_after_join"] = [41001]
        resource["adapter_state"]["cleanup"]["complete"] = False
        document["resource_envelope"] = _reseal_synthetic(resource)
    elif name == "counter_reset":
        resource["adapter_state"]["counters"]["attempted_pairs"] = 0
        document["resource_envelope"] = _reseal_synthetic(resource)
    elif name == "unbound_checkpoint":
        resource["checkpoint_ref"]["sha256"] = "0" * 64
        document["resource_envelope"] = _reseal_synthetic(resource)
    elif name == "changed_inner_receipt_digest":
        positive["inner_ref"]["sha256"] = "0" * 64
        document["positive_envelope"] = _reseal_synthetic(positive)
    elif name == "fake_v3_checker_terminal":
        positive["checker_line"] = "synthetic prefix " + positive["checker_line"]
        document["positive_envelope"] = _reseal_synthetic(positive)
    elif name == "compact_view_mismatch":
        positive["compact_view"]["c_star"].append(99)
        document["positive_envelope"] = _reseal_synthetic(positive)
    elif name == "positive_claim_on_resource_exit":
        resource["claims"]["common_word"] = True
        document["resource_envelope"] = _reseal_synthetic(resource)
    elif name in ("separator_flip", "cofinal_flip", "fake_flip", "ihara_flip"):
        field = {
            "separator_flip": "separator", "cofinal_flip": "cofinal_lift",
            "fake_flip": "fake", "ihara_flip": "ihara_witness",
        }[name]
        positive["claims"][field] = True
        document["positive_envelope"] = _reseal_synthetic(positive)
    elif name == "terminal_reseal":
        positive["terminal"] = "SYNTHETIC_V6_COMMON_RESEALED"
        document["positive_envelope"] = _reseal_synthetic(positive)
    elif name == "stale_output":
        positive["output_fresh"] = False
        document["positive_envelope"] = _reseal_synthetic(positive)
    else:
        raise CheckError("unknown mutation:" + name)


def validate_selftest(receipt, fixture, fixture_raw):
    require(receipt.get("schema") == SELFTEST_SCHEMA and
            receipt.get("status") == "SELFTEST_PASS" and
            receipt.get("terminal") == SELFTEST_PASS,
            "selftest envelope")
    validate_outer_seal(receipt)
    validate_source_binding(receipt)
    reference = receipt.get("fixture", {})
    require(reference == {
        "path": FIXTURE,
        "bytes": len(fixture_raw),
        "sha256": digest_bytes(fixture_raw),
        "digest": digest_obj(fixture),
    }, "selftest fixture binding")
    codec = fixture.get("codec")
    require(codec == {
        "name": "C17-canonical-one-byte", "identity_hex": "00",
        "elements": 17, "multiplication": "(a+b) mod 17",
        "inverse": "(-a) mod 17", "translation_gate": "t*h=g",
    }, "selftest C17 codec")
    require(fixture.get("worker_counts") == list(WORKER_COUNTS) and
            fixture.get("faults") == [
                "live_timeout", "worker_death", "partial_return"
            ], "selftest public rosters")
    document = receipt.get("document")
    try:
        _validate_document(document, fixture)
    except MutationReject as error:
        raise CheckError("baseline selftest rejected:" + str(error)) from error
    controls = receipt.get("mutation_controls", {})
    names = [item["name"] for item in fixture["mutations"]]
    require(controls.get("names") == names and
            controls.get("attempted") == len(names) and
            controls.get("rejected") == len(names) and
            isinstance(controls.get("effects"), list) and
            len(controls["effects"]) == len(names),
            "selftest mutation summary")
    baseline_digest = digest_obj(document)
    independent_effects = []
    for specification, recorded in zip(fixture["mutations"],
                                       controls["effects"]):
        mutant = copy.deepcopy(document)
        _mutate(mutant, specification["name"])
        mutant_digest = digest_obj(mutant)
        require(mutant_digest != baseline_digest,
                "checker mutation no-op:" + specification["name"])
        try:
            _validate_document(mutant, fixture)
        except MutationReject as error:
            require(error.stage == specification["stage"] and
                    error.reason == specification["reason"],
                    "checker narrow mutation stage/reason:" +
                    specification["name"])
            expected = {
                "name": specification["name"],
                "stage": error.stage,
                "reason": error.reason,
                "baseline_digest": baseline_digest,
                "mutant_digest": mutant_digest,
                "rejected": True,
            }
            require(recorded == expected,
                    "producer/checker mutation effect mismatch:" +
                    specification["name"])
            independent_effects.append(expected)
        else:
            raise CheckError("checker mutation survived:" +
                             specification["name"])
    require(receipt.get("production_executed") is False and
            receipt.get("actual_common_checker_invocations") == 0 and
            receipt.get("retrospective_epoch_replay_claim") is None and
            receipt.get("claims") == FALSE_CLAIMS,
            "selftest nonproduction claims")
    return {
        "mathematical_positive_accepted": False,
        "cached_v3_checker_invocations": 0,
        "synthetic_positive_envelope_checked": True,
        "synthetic_resource_envelope_checked": True,
        "mutation_attempted": len(independent_effects),
        "mutation_rejected": len(independent_effects),
    }


def load_fixture():
    path = ROOT / FIXTURE
    raw = path.read_bytes()
    expected = CURRENT_PINS["fixture"]
    require(len(raw) == expected[1] and digest_bytes(raw) == expected[2],
            "checker fixture pin")
    value = json.loads(raw.decode("ascii"))
    require(value.get("schema") == FIXTURE_SCHEMA,
            "checker fixture schema")
    return value, raw


def receipt_path_value(path_value):
    path = Path(path_value)
    if path.is_absolute():
        resolved = path.resolve()
    else:
        require(".." not in path.parts and
                path.as_posix().startswith("ci/out/"),
                "receipt path boundary")
        resolved = (ROOT / path).resolve()
    output_root = (ROOT / "ci/out").resolve()
    require(resolved.parent == output_root and resolved.suffix == ".json",
            "receipt resolved boundary")
    return resolved


def verdict_path_value(path_value):
    path = Path(path_value)
    require(not path.is_absolute() and ".." not in path.parts and
            path.as_posix().startswith("ci/out/") and
            path.suffix == ".json", "verdict path boundary")
    resolved = ROOT / path
    require(not resolved.exists(), "stale verdict")
    return resolved


def seal_verdict(value):
    answer = copy.deepcopy(value)
    answer.pop("self_digest_sha256", None)
    answer["self_digest_sha256"] = digest_obj(answer)
    return answer


def write_exclusive(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as stream:
        stream.write(canonical(value) + b"\n")


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("receipt")
    parser.add_argument("--output", required=True)
    parser.add_argument("--v3-checker-seconds", type=float, default=21_600.0)
    args = parser.parse_args(argv)
    authenticate_local_sources()
    fixture, fixture_raw = load_fixture()
    receipt_path = receipt_path_value(args.receipt)
    verdict_path = verdict_path_value(args.output)
    raw = receipt_path.read_bytes()
    require(raw and raw.endswith(b"\n"), "receipt bytes")
    receipt = json.loads(raw.decode("utf-8"))
    require(canonical(receipt) + b"\n" == raw, "receipt canonical bytes")
    terminal = str(receipt.get("terminal", ""))
    if receipt.get("schema") == SELFTEST_SCHEMA:
        result = validate_selftest(receipt, fixture, fixture_raw)
        mode = "SELFTEST"
    else:
        validate_outer_seal(receipt)
        owner_hook = receipt.get("owner_hook", {})
        require(owner_hook.get("registered_hook") == HOOK_NAME and
                owner_hook.get("owner_class") == "BoundaryDescriptorCache" and
                owner_hook.get("replaced_method") == "correlation" and
                owner_hook.get("unchanged_owner_functions") == [
                    "rank", "dual", "correction", "candidate",
                    "COMMON", "ordinary_checkpoint",
                ], "outer owner hook")
        if terminal == COMMON:
            result = validate_positive(
                receipt, receipt_path, args.v3_checker_seconds
            )
        else:
            result = validate_nonpositive(receipt, receipt_path)
        mode = "PRODUCTION"
    verdict = seal_verdict({
        "schema": SCHEMA + "/checker-verdict",
        "status": "PASS",
        "mode": mode,
        "terminal": terminal,
        "receipt": {
            "path": receipt_path.relative_to(ROOT).as_posix(),
            "basename": receipt_path.name,
            "bytes": len(raw), "sha256": digest_bytes(raw),
            "self_digest_sha256": receipt.get("self_digest_sha256"),
        },
        "current_pins": {
            label: {"path": path, "bytes": size, "sha256": sha}
            for label, (path, size, sha) in CURRENT_PINS.items()
        },
        "dependency_pins_sha256": pins_digest(),
        "result": result,
        "negative_or_separator_accepted": False,
        "retrospective_epoch_replay_claim": None,
    })
    write_exclusive(verdict_path, verdict)
    if mode == "SELFTEST":
        print(CHECKER_SELFTEST_PASS, flush=True)
    print(CHECKER_PREFIX + " terminal=" + terminal, flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
