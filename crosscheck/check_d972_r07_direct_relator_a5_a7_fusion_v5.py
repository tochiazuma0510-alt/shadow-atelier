#!/usr/bin/env python3
"""Independent task377 checker for a positive lift-null MEMBER receipt.

The v5 producer is never imported.  Selected Schreier ancestry is replayed
with task198-v14 and the final literal is replayed by the independent
task292 checker implementation.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import os
import stat
import sys
import types
from pathlib import Path
from typing import Any, Iterable, Sequence


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "d972-r07-direct-relator-a5-a7-fusion/v5"
CHECK_SCHEMA = SCHEMA + "/checker-verdict/v5"
LITERAL_SCHEMA = "d972-r07-actual-three-exact-pb-endpoints/v3/literal-input"
CHECKPOINT_SCHEMA = SCHEMA + "/checkpoint/v2"
SIDECAR_SCHEMA = SCHEMA + "/a5-sidecar/v2"
CHECKER_LINE = "R07_DIRECT_RELATOR_A5_A7_FUSION_V5_CHECKER"
MEMBER = "R07_DIRECT_RELATOR_A5_A7_FUSION_MEMBER"
MODULUS = 3
LETTERS = (1, -1, 2, -2)
BLOCKS = ("H1", "H2", "P")

PRODUCER_PIN = (
    "search/d972_r07_direct_relator_a5_a7_fusion_v5.py", 57482,
    "ce9c6b0d7ba587f877634b60e0162f8ad3f60091b182b3031775b512f719f2ff")
V4_PIN = (
    "search/d972_r07_direct_relator_a5_a7_fusion_v4.py", 26841,
    "0f07716b38c427eeaa9bd920721a170ede85d0cad805f2fa55bbe614bd9229f1")
V4_CHECKER_PIN = (
    "crosscheck/check_d972_r07_direct_relator_a5_a7_fusion_v4.py", 24239,
    "f494d12c050e4d1c5f199fa771d56ca5326c365439e617f2cbe892cf7b3b6a01")
BASE_PIN = (
    "search/d972_r07_zero_base_a5_a6_compiler_v3.py", 59239,
    "c287011d5e573452094e62c76020ab4b1076bc427103174b1771a22a1bb4fbd8")
BASE_CHECKER_PIN = (
    "crosscheck/check_d972_r07_zero_base_a5_a6_compiler_v3.py", 45942,
    "e86806444efa146954213da4bbb13726a8b5dc79b16c0a4b97aaa5c7b05b1cb0")
TASK292_PIN = (
    "search/d972_r07_actual_three_exact_pb_endpoints_v2.py", 40044,
    "c44d2c8e7fdd7dcbf691600ba823445d1ac45695ef173043c723874a409f7208")
TASK292_CHECKER_PIN = (
    "crosscheck/check_d972_r07_actual_three_exact_pb_endpoints_v2.py", 46873,
    "8d7598f376715af16ccec7bae5550f2c5329922b1b36326643a2a4e9e7cf72d8")
TASK198_V12_PIN = (
    "search/d972_r07_word_independent_successor_kernel_v12.py", 7209,
    "816bae92d86ac4bf3a6feb05297f505680072c2ce793db97135154cef928e9c5")
TASK198_V14_PIN = (
    "crosscheck/check_d972_r07_word_independent_successor_kernel_v14.py", 8074,
    "7ff0fb8888b46febb8b373914a3ba31ee555e43c829e60dae915bacfb16b7b47")
TASK198_V6_PIN = (
    "search/d972_r07_word_independent_successor_kernel_v6.py", 219187,
    "aaa8a60960698eeeab0c300f7fb65bb902bbae7e5507e4bef933cdff26263a6a")
TASK198_CHECKER_V6_PIN = (
    "crosscheck/check_d972_r07_word_independent_successor_kernel_v6.py", 258847,
    "432bcaadfa1dcfd9526749c40fb3d56c1bdb5671a1959d571a8076c20ba29ccf")
TASK193_PRODUCER_PIN = (
    "search/d972_r07_second_frattini_affine_prefix_compiler_v3.py", 2826,
    "1ac65ca533e11ac39def79c84de0bbdcb018d463ac10bca6158db254a61da741")
TASK193_CHECKER_PIN = (
    "crosscheck/check_d972_r07_second_frattini_affine_prefix_compiler_v3.py", 2792,
    "5b3c5b3e607077e0bebcf0153c592465983ba210b768c93ea62aeb2201c905c6")
TASK193_DRIVER_PIN = (
    "search/d972_r07_second_frattini_affine_prefix_compiler_gha_driver_v3.g", 5798,
    "c11074bd1e634aa38d4d164699542e17087e659115c31b8f5b8cc322dc5dfd84")

TASK198_DEFAULTS = {
    "receipt": "ci/in/d972_r07_seven_context_roof_presentation_v1.json",
    "manifest": "ci/in/d972_r07_seven_context_roof_presentation_v1.acceptance_v2.json",
    "producer": "ci/in/d972_r07_seven_context_roof_presentation_v1.producer.attestation.txt",
    "checker": "ci/in/d972_r07_seven_context_roof_presentation_v1.checker.attestation.txt",
    "verdict": "ci/in/d972_r07_seven_context_roof_presentation_v1.checker.verdict.json",
}


class Reject(RuntimeError):
    pass


def require(value: bool, message: str) -> None:
    if value is not True:
        raise Reject(message)


def canon(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def digest(value: Any) -> str:
    return sha(canon(value))


def seal(value: dict[str, Any]) -> dict[str, Any]:
    body = dict(value)
    body.pop("self_digest_sha256", None)
    body["self_digest_sha256"] = digest(body)
    return body


def reduced(word: Iterable[int]) -> tuple[int, ...]:
    out: list[int] = []
    for raw in word:
        letter = int(raw)
        require(letter in LETTERS, "word:letter")
        if out and out[-1] == -letter:
            out.pop()
        else:
            out.append(letter)
    return tuple(out)


def product(*words: Sequence[int]) -> tuple[int, ...]:
    return reduced(letter for word in words for letter in word)


def inverse(word: Sequence[int]) -> tuple[int, ...]:
    return tuple(-int(letter) for letter in reversed(tuple(word)))


def inside(raw: str | Path, area: str | None = None) -> Path:
    text = str(raw).replace("\\", "/")
    path = Path(text)
    require(not path.is_absolute() and ".." not in path.parts and
            "." not in path.parts, "path:lexical:" + text)
    try:
        value = (ROOT / path).resolve(strict=True)
        value.relative_to(ROOT.resolve())
        if area is not None:
            value.relative_to((ROOT / area).resolve(strict=True))
    except (OSError, ValueError) as exc:
        raise Reject("path:containment:" + text) from exc
    cursor = ROOT
    for part in path.parts:
        cursor /= part
        require(not stat.S_ISLNK(os.lstat(cursor).st_mode), "path:symlink")
    return value


def identity(path: Path) -> dict[str, Any]:
    raw = path.read_bytes()
    return {"path": path.relative_to(ROOT).as_posix(),
            "bytes": len(raw), "sha256": sha(raw)}


def pin_value(pin: tuple[str, int, str]) -> dict[str, Any]:
    return {"path": pin[0], "bytes": pin[1], "sha256": pin[2]}


def pin_identity(pin: tuple[str, int, str], label: str) -> dict[str, Any]:
    got = identity(inside(pin[0]))
    want = pin_value(pin)
    require(got == want, label + ":pin")
    return want


def load_pinned(pin: tuple[str, int, str], name: str) -> types.ModuleType:
    path = inside(pin[0])
    pin_identity(pin, name)
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None, name + ":loader")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def static_bindings() -> dict[str, Any]:
    return {
        "v4_producer": pin_value(V4_PIN),
        "v4_checker": pin_value(V4_CHECKER_PIN),
        "a5_v3_producer": pin_value(BASE_PIN),
        "a5_v3_checker": pin_value(BASE_CHECKER_PIN),
        "task292_v2_producer": pin_value(TASK292_PIN),
        "task292_v2_checker": pin_value(TASK292_CHECKER_PIN),
        "task198_v12_wrapper": pin_value(TASK198_V12_PIN),
        "task198_v14_wrapper": pin_value(TASK198_V14_PIN),
        "task198_v6_frozen": pin_value(TASK198_V6_PIN),
        "task198_v6_checker_frozen": pin_value(TASK198_CHECKER_V6_PIN),
        "task193_v3_producer": pin_value(TASK193_PRODUCER_PIN),
        "task193_v3_checker": pin_value(TASK193_CHECKER_PIN),
        "task193_v3_driver": pin_value(TASK193_DRIVER_PIN),
    }


def read_json(raw_path: str, label: str, area: str
              ) -> tuple[dict[str, Any], dict[str, Any]]:
    path = inside(raw_path, area)
    before = path.stat()
    raw = path.read_bytes()
    after = path.stat()
    require((before.st_dev, before.st_ino, before.st_size,
             getattr(before, "st_mtime_ns", 0)) ==
            (after.st_dev, after.st_ino, after.st_size,
             getattr(after, "st_mtime_ns", 0)), label + ":changed")
    try:
        value = json.loads(raw.decode("ascii"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise Reject(label + ":json") from exc
    require(type(value) is dict, label + ":object")
    return value, {"path": path.relative_to(ROOT).as_posix(),
                   "bytes": len(raw), "sha256": sha(raw)}


def check_seal(value: dict[str, Any], label: str) -> None:
    claimed = value.get("self_digest_sha256")
    body = dict(value)
    body.pop("self_digest_sha256", None)
    require(type(claimed) is str and claimed == digest(body), label + ":seal")


def authenticate(raw_path: str, claimed: dict[str, Any], label: str
                 ) -> tuple[dict[str, Any], dict[str, Any]]:
    require(type(claimed) is dict, label + ":claim")
    value, got = read_json(raw_path, label, "ci/out")
    require(got == claimed, label + ":physical_identity")
    check_seal(value, label)
    return value, got


def affine_state_public(helper: Any, state: Any) -> dict[str, Any]:
    gradient = []
    for (component, element), raw in sorted(
            state.u.items(), key=lambda item:
            (int(item[0][0]), helper.element_blob(item[0][1]))):
        value = int(raw) % MODULUS
        if value:
            gradient.append([int(component), helper.element_blob(element).hex(), value])
    return {"roof": helper.element_blob(state.a).hex(), "gradient": gradient}


def state_public(helper: Any, arithmetic: Any,
                 word: Sequence[int]) -> list[dict[str, Any]]:
    states = [arithmetic.direct(word, index) for index in range(10)]
    return [affine_state_public(helper, state) for state in states]


def endpoint_buckets(value: dict[str, Any]) -> dict[str, dict[str, int]]:
    answer: dict[str, dict[str, int]] = {}
    for block in BLOCKS:
        table: dict[str, int] = {}
        for row in value["endpoints"][block]["buckets"]:
            key = json.dumps(row["full_artin_key"], separators=(",", ":"))
            coefficient = int(row["coefficient_mod_3"]) % MODULUS
            require(coefficient and key not in table,
                    "endpoint:bucket_shape:" + block)
            table[key] = coefficient
        answer[block] = table
    return answer


def schedule_contract() -> dict[str, Any]:
    return {
        "cayley": "one next shortlex marked edge per round",
        "translations": "one next freely-reduced shortlex F2 word per round",
        "pairs": "cyclic seed roster; each seed advances one translation cursor per turn",
        "proof": ("Delta1 is finite; hence every finite Cayley edge is explored. "
                  "Every reduced F2 word is generated.  The finite eventual seed "
                  "roster is visited cyclically, so every (seed,V) pair receives "
                  "a turn absent a resource stop."),
        "positive_only": True,
        "bounded_miss_is_A7_negative": False,
    }


def lift_term(seed: dict[str, Any], translation: Sequence[int],
              coefficient: int) -> dict[str, Any]:
    v_word = reduced(translation)
    n_word = reduced(seed["word"])
    return {
        "coefficient": int(coefficient) % MODULUS,
        "U": list(product(v_word, n_word)),
        "V": list(v_word),
        "ancestry": {
            "owner": "v351-translated-schreier-lift-null",
            "seed_index": int(seed["seed_index"]),
            "source_word": list(seed["source_word"]),
            "letter": int(seed["letter"]),
            "target_word": list(seed["target_word"]),
            "schreier_word": list(n_word),
            "translating_word": list(v_word),
            "formula": "V*(s(q)*t*s(qt)^-1)-V",
        },
    }


def check_selected(selected: list[dict[str, Any]], checkpoint: dict[str, Any],
                   helper: Any, arithmetic: Any
                   ) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    require(type(selected) is list and selected, "lift:selected")
    search = checkpoint.get("search")
    require(type(search) is dict and
            search.get("schedule") == schedule_contract(),
            "checkpoint:search_schedule")
    columns = search.get("basis_columns")
    solution = search.get("pending_solution")
    require(type(columns) is list and type(solution) is dict,
            "checkpoint:positive_ancestry")
    identity_public = search.get("identity_state_key")
    require(type(identity_public) is list and len(identity_public) == 10 and
            sha(canon(identity_public)) ==
            search.get("identity_state_key_sha256"), "checkpoint:identity_state")
    actual_identity = state_public(helper, arithmetic, ())
    require(actual_identity == identity_public, "rho1:identity_owner")
    terms: list[dict[str, Any]] = []
    selected_replay = []
    for ordinal, item in enumerate(selected, 1):
        require(type(item) is dict, "lift:selected_row:" + str(ordinal))
        column_id = int(item.get("column_id"))
        coefficient = int(item.get("coefficient")) % MODULUS
        require(coefficient in (1, 2) and 0 <= column_id < len(columns) and
                int(solution.get(str(column_id), 0)) % MODULUS == coefficient,
                "lift:solution_ancestry:" + str(ordinal))
        column = columns[column_id]
        require(int(column.get("column_id")) == column_id and
                item.get("endpoint_column_sha256") ==
                column.get("endpoint_column_sha256") and
                int(item.get("endpoint_coordinate_count")) ==
                int(column.get("endpoint_coordinate_count")),
                "lift:column_binding:" + str(ordinal))
        seed = item.get("seed")
        require(type(seed) is dict and seed == column.get("seed"),
                "lift:seed_binding:" + str(ordinal))
        source = reduced(seed.get("source_word", ()))
        target = reduced(seed.get("target_word", ()))
        letter = int(seed.get("letter"))
        require(letter in LETTERS, "lift:edge_letter")
        edge_word = product(source, (letter,))
        require(state_public(helper, arithmetic, edge_word) ==
                state_public(helper, arithmetic, target),
                "lift:edge_target:" + str(ordinal))
        n_word = product(source, (letter,), inverse(target))
        require(n_word and list(n_word) == seed.get("word") and
                state_public(helper, arithmetic, n_word) == identity_public,
                "lift:schreier_identity:" + str(ordinal))
        translation = reduced(item.get("translating_word", ()))
        require(list(translation) == item.get("translating_word") and
                list(translation) == column.get("translating_word"),
                "lift:translation_binding:" + str(ordinal))
        term = lift_term(seed, translation, coefficient)
        require(list(term["U"]) == item.get("positive_word") and
                list(term["V"]) == item.get("negative_word") and
                state_public(helper, arithmetic, term["U"]) ==
                state_public(helper, arithmetic, term["V"]) and
                digest(term) == item.get("M_term_digest_sha256"),
                "lift:translated_null_pair:" + str(ordinal))
        base_term = copy.deepcopy(column.get("term"))
        require(type(base_term) is dict, "lift:base_term")
        base_term["coefficient"] = coefficient
        require(base_term == term, "lift:term_binding:" + str(ordinal))
        terms.append(term)
        selected_replay.append({"column_id": column_id,
                                "rho1_edge": True,
                                "rho1_seed_identity": True,
                                "rho1_translated_pair_equal": True})
    return terms, {"selected_count": len(terms),
                   "selected_replay": selected_replay,
                   "task198_v14_independent": True}


def check(args: argparse.Namespace) -> dict[str, Any]:
    producer_source = pin_identity(PRODUCER_PIN, "producer")
    for label, pin in (("v4:producer", V4_PIN),
                       ("v4:checker", V4_CHECKER_PIN),
                       ("a5:producer", BASE_PIN),
                       ("a5:checker", BASE_CHECKER_PIN),
                       ("task292:producer", TASK292_PIN),
                       ("task292:checker", TASK292_CHECKER_PIN),
                       ("task198:v12", TASK198_V12_PIN),
                       ("task198:v14", TASK198_V14_PIN),
                       ("task198:v6", TASK198_V6_PIN),
                       ("task198:checker_v6", TASK198_CHECKER_V6_PIN),
                       ("task193:producer", TASK193_PRODUCER_PIN),
                       ("task193:checker", TASK193_CHECKER_PIN),
                       ("task193:driver", TASK193_DRIVER_PIN)):
        pin_identity(pin, label)
    v4 = load_pinned(V4_CHECKER_PIN, "r07_fusion_v4_checker_for_v5")
    base = load_pinned(BASE_CHECKER_PIN, "r07_a5_v3_checker_for_fusion_v5")
    task292 = load_pinned(TASK292_CHECKER_PIN,
                          "r07_task292_v2_checker_for_fusion_v5")
    helper = base.load_helper()
    limits = dict(helper.CAPS)
    limits["wall_seconds"] = int(args.seconds)
    limits["rss_bytes"] = int(args.rss_bytes)
    try:
        meter = helper.Meter(limits)
        authority = helper.Authority(args, meter)
        arithmetic = helper.CheckerArithmetic(authority, meter)
        boundary = helper.Boundary(arithmetic, meter)
    except (helper.Reject, helper.ResourceStop) as exc:
        raise Reject(str(exc)) from exc
    task193, task193_id = base.load_task193(args.task193_receipt,
                                           args.task193_verdict)
    receipt, receipt_id = read_json(args.receipt, "producer_receipt", "ci/out")
    check_seal(receipt, "producer_receipt")
    require(receipt.get("schema") == SCHEMA and
            receipt.get("status") == "COMPLETE" and
            receipt.get("terminal") == MEMBER and
            receipt.get("mode") == "PRODUCTION" and
            receipt.get("source") == producer_source and
            receipt.get("static_bindings") == static_bindings(),
            "producer:member_envelope")
    require(receipt.get("owners", {}).get("task193_v3") == task193_id,
            "producer:task193_binding")
    owner198 = receipt.get("owners", {}).get("task198", {})
    require(owner198.get("receipt_sha256") ==
            authority.identity.get("receipt_sha256") and
            owner198.get("manifest_sha256") ==
            authority.identity.get("manifest_sha256"),
            "producer:task198_binding")
    result = receipt.get("result")
    require(type(result) is dict and result.get("terminal_kind") == "MEMBER",
            "producer:result")
    a5 = result.get("a5")
    require(type(a5) is dict and a5.get("terminal_kind") == "MEMBER",
            "producer:a5")
    require(result.get("mu1") == a5.get("mu1") and
            receipt.get("claims", {}).get("A5") == "MEMBER" and
            receipt.get("claims", {}).get("A6_M") is True and
            receipt.get("claims", {}).get("A7") == "ZERO" and
            receipt.get("claims", {}).get("fixed_word_only") is True and
            all(receipt.get("claims", {}).get(key) == "NONE"
                for key in ("A8", "A9", "compatible_lift", "fake", "Ihara")),
            "producer:claim_scope")

    checkpoint, _ = authenticate(
        args.checkpoint, receipt.get("artifacts", {}).get("checkpoint"),
        "checkpoint")
    require(checkpoint.get("schema") == CHECKPOINT_SCHEMA and
            checkpoint.get("source") == producer_source and
            checkpoint.get("static_bindings") == static_bindings() and
            checkpoint.get("owners") == receipt.get("owners") and
            checkpoint.get("a5_result") == a5 and
            checkpoint.get("a5_digest_sha256") == digest(a5) and
            checkpoint.get("resume_contract") == {
                "all_or_none_path_bytes_sha256": True,
                "source_owner_a5_canonical_bound": True,
                "affine_states_reconstructed_from_literal_words": True,
                "no_unauthenticated_python_objects": True,
                "fair_positive_dovetail": True},
            "checkpoint:binding")
    sidecar, _ = authenticate(
        args.a5_sidecar, receipt.get("artifacts", {}).get("a5_sidecar"),
        "a5_sidecar")
    require(sidecar.get("schema") == SIDECAR_SCHEMA and
            sidecar.get("status") == "ACCEPTED_A5_MEMBER" and
            sidecar.get("terminal") == base.MEMBER and
            sidecar.get("source") == producer_source and
            sidecar.get("static_bindings") == static_bindings() and
            sidecar.get("owners") == receipt.get("owners") and
            sidecar.get("a5_result") == a5,
            "sidecar:binding")

    model = base.CheckerModel(helper, authority, arithmetic, boundary, task193)
    a5_replay = base.check_member(model, a5)
    terms = base.coefficient_terms(a5.get("coefficient_terms"))
    pairs = base.expected_m(model, terms)
    bindings = {
        "task198": receipt["owners"]["task198"],
        "task193_v3": receipt["owners"]["task193_v3"],
        "a5_v3_in_process": {"source": pin_value(BASE_PIN),
                              "result_digest_sha256": digest(a5)},
    }
    canonical_literal = v4.literal_owner(base, helper, model, task193,
                                         pairs, bindings)
    task292.CHECK_BUDGET = task292.CheckerBudget()
    canonical_literal["M_immutable_digest_sha256"] = task292.collect_m(
        canonical_literal["M_terms"])["immutable_digest_sha256"]
    canonical_digest = digest(canonical_literal)
    require(checkpoint.get("canonical_literal_digest_sha256") ==
            canonical_digest, "canonical:literal_binding")
    try:
        canonical_exact = task292.replay_literal(canonical_literal)
    except (task292.CheckerResource, task292.CheckStop) as exc:
        raise Reject("task292:canonical:" + str(exc)) from exc
    producer_canonical = (result.get("endpoint_exact")
                          if result.get("canonical_M_only") is True else
                          result.get("canonical_endpoint"))
    require(type(producer_canonical) is dict and
            type(checkpoint.get("canonical_endpoint")) is dict and
            checkpoint.get("canonical_endpoint_terminal") ==
            canonical_exact["terminal"] and
            checkpoint.get("canonical_endpoint_digest_sha256") ==
            digest(producer_canonical) and
            endpoint_buckets(checkpoint.get("canonical_endpoint")) ==
            endpoint_buckets(canonical_exact) and
            endpoint_buckets(producer_canonical) ==
            endpoint_buckets(canonical_exact),
            "canonical:independent_replay")

    if result.get("canonical_M_only") is True:
        require(result.get("v351_lift_null") == "NOT_NEEDED" and
                checkpoint.get("phase") == "CANONICAL_ENDPOINT_ZERO_COMPLETE" and
                canonical_exact["terminal"] == task292.ZERO,
                "canonical:zero_lane")
        final_literal = canonical_literal
        selected_replay = None
        final_exact = canonical_exact
    else:
        require(result.get("v351_lift_null") == "IMPLEMENTED_MEMBER" and
                result.get("fixed_word_only") is True and
                checkpoint.get("phase") == "LIFT_NULL_MEMBER_COMPLETE" and
                canonical_exact["terminal"].startswith(task292.NONZERO),
                "lift:member_lane")
        certificate = result.get("lift_null_certificate")
        require(type(certificate) is dict and certificate.get("theorem") == "v351" and
                certificate.get("state_key") ==
                "all ten affine roofs plus all ten sparse gradients" and
                certificate.get("schedule") == schedule_contract(),
                "lift:certificate")
        require(certificate.get("canonical_endpoint_digest_sha256") ==
                digest(producer_canonical), "lift:canonical_digest")
        selected = certificate.get("selected")
        require(type(selected) is list and
                certificate.get("selected_sha256") == digest(selected) and
                int(certificate.get("selected_count")) == len(selected),
                "lift:selected_digest")
        lift_terms, selected_replay = check_selected(
            selected, checkpoint, helper, arithmetic)
        lift_binding = {
            "theorem": "v351",
            "selected_sha256": digest(selected),
            "selected_count": len(selected),
            "rho1_owner": "task198-v12 Runtime.states_direct ten-affine",
            "endpoint_owner": "task292-v2 exact core",
        }
        final_literal = copy.deepcopy(canonical_literal)
        final_literal["bindings"] = dict(final_literal["bindings"])
        final_literal["bindings"]["v351_lift_null"] = lift_binding
        final_literal["M_terms"] = list(final_literal["M_terms"]) + lift_terms
        final_literal["M_immutable_digest_sha256"] = task292.collect_m(
            final_literal["M_terms"])["immutable_digest_sha256"]
        require(certificate.get("final_literal_digest_sha256") ==
                digest(final_literal), "lift:final_literal_digest")
        try:
            final_exact = task292.replay_literal(final_literal)
        except (task292.CheckerResource, task292.CheckStop) as exc:
            raise Reject("task292:final:" + str(exc)) from exc
    require(final_exact["terminal"] == task292.ZERO and
            all(not final_exact["endpoints"][block]["buckets"]
                for block in BLOCKS) and
            all(final_exact["full_C1_replay"]["blocks"][block]["D1_z_zero"]
                for block in BLOCKS), "endpoint:final_zero")
    producer_endpoint = result.get("endpoint_exact")
    require(type(producer_endpoint) is dict and
            producer_endpoint.get("M", {}).get("immutable_digest_sha256") ==
            final_exact["M"]["immutable_digest_sha256"] and
            endpoint_buckets(producer_endpoint) == endpoint_buckets(final_exact),
            "endpoint:producer_binding")
    if result.get("canonical_M_only") is not True:
        require(result["lift_null_certificate"].get("final_M_digest_sha256") ==
                final_exact["M"]["immutable_digest_sha256"],
                "lift:final_M_digest")
    literal_binding = result.get("literal_binding")
    require(type(literal_binding) is dict and
            literal_binding.get("schema") == LITERAL_SCHEMA and
            literal_binding.get("digest_sha256") == digest(final_literal) and
            all(literal_binding.get("owner_replay", {}).values()),
            "literal:producer_binding")

    return seal({
        "schema": CHECK_SCHEMA, "status": "ACCEPTED",
        "terminal": MEMBER, "independent": True,
        "receipt": receipt_id, "task193_v3": task193_id,
        "task198": authority.identity,
        "a5_replay": a5_replay,
        "selected_lift_null_replay": selected_replay,
        "endpoint_replay": {
            "canonical_terminal": canonical_exact["terminal"],
            "final_terminal": final_exact["terminal"],
            "final_M_digest_sha256":
                final_exact["M"]["immutable_digest_sha256"],
            "independent_task292_replay": True,
            "full_C1_zero": True,
        },
        "artifacts": receipt["artifacts"],
        "claims": {"A5": "MEMBER", "A6_M": True, "A7": "ZERO",
                   "fixed_word_only": True, "A8": "NONE", "A9": "NONE",
                   "compatible_lift": "NONE", "mixed_prime": "NONE",
                   "perfect_core": "NONE", "fake": "NONE", "Ihara": "NONE"},
        "resource": meter.public(strict=False),
    })


def output_path(raw: str) -> Path:
    path = Path(str(raw).replace("\\", "/"))
    require(not path.is_absolute() and ".." not in path.parts and
            "." not in path.parts, "output:lexical")
    target = (ROOT / path).resolve(strict=False)
    require(target.parent == (ROOT / "ci/out").resolve(strict=True),
            "output:containment")
    return target


def write_exclusive(raw: str, value: dict[str, Any]) -> None:
    path = output_path(raw)
    require(not path.exists(), "output:stale")
    encoded = canon(value) + b"\n"
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    try:
        view = memoryview(encoded)
        while view:
            view = view[os.write(fd, view):]
        os.fsync(fd)
    finally:
        os.close(fd)


def parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=("PRODUCTION",), default="PRODUCTION")
    ap.add_argument("--task193-receipt", required=True)
    ap.add_argument("--task193-verdict", required=True)
    ap.add_argument("--receipt", required=True)
    ap.add_argument("--checkpoint", required=True)
    ap.add_argument("--a5-sidecar", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--seconds", type=int, default=14_400)
    ap.add_argument("--rss-bytes", type=int, default=5_000_000_000)
    for key, value in TASK198_DEFAULTS.items():
        ap.add_argument("--task198-" + key, dest="task198_" + key,
                        default=value)
    return ap


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        require(args.seconds > 0 and args.rss_bytes > 0,
                "arguments:positive_caps")
        verdict = check(args)
        write_exclusive(args.output, verdict)
        print(CHECKER_LINE + " terminal=" + str(verdict["terminal"]), flush=True)
        return 0
    except (Reject, OSError, ValueError, TypeError, KeyError,
            AttributeError) as exc:
        print(CHECKER_LINE + "_ERROR " + str(exc), flush=True)
        return 1
    except Exception as exc:
        print(CHECKER_LINE + "_ERROR " + str(exc), flush=True)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
