#!/usr/bin/env python3
"""Independent task376 checker for the canonical-M exact endpoint binder.

No producer or producer arithmetic helper is imported.  Frozen A5 checker
v3 restores task198-v14, while frozen task292 checker v2 supplies the second
Artin implementation.
"""
from __future__ import annotations

import argparse
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
SCHEMA = "d972-r07-direct-relator-a5-a7-fusion/v4"
CHECK_SCHEMA = SCHEMA + "/checker-verdict/v4"
LITERAL_SCHEMA = "d972-r07-actual-three-exact-pb-endpoints/v3/literal-input"
CHECKPOINT_SCHEMA = SCHEMA + "/checkpoint/v1"
SIDECAR_SCHEMA = SCHEMA + "/a5-sidecar/v1"
CHECKER_LINE = "R07_DIRECT_RELATOR_A5_A7_FUSION_V4_CHECKER"
MEMBER = "R07_DIRECT_RELATOR_A5_A7_FUSION_MEMBER"
NONMEMBER = "R07_ZERO_BASE_A5_A6_NONMEMBER"
UNKNOWN_RESOURCE = "UNKNOWN_RESOURCE"

PRODUCER_PIN = (
    "search/d972_r07_direct_relator_a5_a7_fusion_v4.py", 26841,
    "0f07716b38c427eeaa9bd920721a170ede85d0cad805f2fa55bbe614bd9229f1")
BASE_CHECKER_PIN = (
    "crosscheck/check_d972_r07_zero_base_a5_a6_compiler_v3.py", 45942,
    "e86806444efa146954213da4bbb13726a8b5dc79b16c0a4b97aaa5c7b05b1cb0")
TASK292_PRODUCER_PIN = (
    "search/d972_r07_actual_three_exact_pb_endpoints_v2.py", 40044,
    "c44d2c8e7fdd7dcbf691600ba823445d1ac45695ef173043c723874a409f7208")
TASK292_CHECKER_PIN = (
    "crosscheck/check_d972_r07_actual_three_exact_pb_endpoints_v2.py", 46873,
    "8d7598f376715af16ccec7bae5550f2c5329922b1b36326643a2a4e9e7cf72d8")
TASK198_DEFAULTS = {
    "receipt": "ci/in/d972_r07_seven_context_roof_presentation_v1.json",
    "manifest": "ci/in/d972_r07_seven_context_roof_presentation_v1.acceptance_v2.json",
    "producer": "ci/in/d972_r07_seven_context_roof_presentation_v1.producer.attestation.txt",
    "checker": "ci/in/d972_r07_seven_context_roof_presentation_v1.checker.attestation.txt",
    "verdict": "ci/in/d972_r07_seven_context_roof_presentation_v1.checker.verdict.json",
}
BLOCKS = ("H1", "H2", "P")
POSITIONS = (1, 2, 3, 1, 2, 3, 1, 2, 3, 5, 4)


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


def reduced(word: Iterable[int], alphabet: tuple[int, ...] | None = None
            ) -> tuple[int, ...]:
    out: list[int] = []
    for raw in word:
        letter = int(raw)
        require(letter != 0 and (alphabet is None or letter in alphabet), "word:letter")
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


def pin_identity(pin: tuple[str, int, str], label: str) -> dict[str, Any]:
    got = identity(inside(pin[0]))
    want = {"path": pin[0], "bytes": pin[1], "sha256": pin[2]}
    require(got == want, label + ":pin")
    return want


def load_pinned(pin: tuple[str, int, str], name: str) -> types.ModuleType:
    pin_identity(pin, name)
    path = inside(pin[0])
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None, name + ":loader")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def static_bindings() -> dict[str, Any]:
    return {
        "a5_v3": {"path": "search/d972_r07_zero_base_a5_a6_compiler_v3.py",
                  "bytes": 59239,
                  "sha256": "c287011d5e573452094e62c76020ab4b1076bc427103174b1771a22a1bb4fbd8"},
        "task292_producer_v2": {"path": TASK292_PRODUCER_PIN[0],
                                "bytes": TASK292_PRODUCER_PIN[1],
                                "sha256": TASK292_PRODUCER_PIN[2]},
        "task292_checker_v2": {"path": TASK292_CHECKER_PIN[0],
                               "bytes": TASK292_CHECKER_PIN[1],
                               "sha256": TASK292_CHECKER_PIN[2]},
    }


def normalize_block(raw: str) -> str:
    return "P" if raw.startswith("P") else raw


def validate_layout(helper: Any, authority: Any) -> list[dict[str, Any]]:
    ledger = authority.receipt.get("bridge", {}).get("occurrence_ledger")
    expected = getattr(helper, "CHECKER_BRIDGE_OWNER_LAYOUT", None)
    require(type(ledger) is list and type(expected) is tuple and
            len(ledger) == len(expected) == 11, "owner:ledger_cardinality")
    for index, (item, row) in enumerate(zip(ledger, expected), 1):
        actual = (item.get("block"), int(item.get("block_index")),
                  int(item.get("block_slot")), item.get("occurrence"),
                  item.get("type"), int(item.get("ten_index")),
                  int(item.get("context_id")), item.get("role"),
                  int(item.get("factor_sign")), item.get("orientation"),
                  tuple(item.get("fox_prefix_occurrences", ())))
        require(int(item.get("ordinal")) == index and actual == row,
                "owner:ledger_row:" + str(index))
    return ledger


def relation_word(words: list[tuple[int, ...]], ledger: list[dict[str, Any]],
                  block: str) -> tuple[int, ...]:
    selected = [(item, words[int(item["ordinal"]) - 1]) for item in ledger
                if normalize_block(str(item["block"])) == block]
    factors = [word if int(item["factor_sign"]) > 0 else inverse(word)
               for item, word in selected]
    return product(*(factors[index] for index in reversed(range(len(factors)))))


def literal_owner(base: Any, helper: Any, model: Any,
                  task193: dict[str, Any], pairs: list[dict[str, Any]],
                  bindings: dict[str, Any]) -> dict[str, Any]:
    ledger = validate_layout(helper, model.authority)
    g0 = reduced(task193.get("g760", ()), (1, -1, 2, -2))
    correction = reduced(task193.get("correction_word", ()), (1, -1, 2, -2))
    corrected = product(g0, correction)
    require(len(g0) == 760 and list(corrected) == task193.get("corrected_word") and
            task193.get("literal_binding") == list(correction),
            "task193:corrected_literal")
    contexts = model.a.contexts
    require(type(contexts) is list and len(contexts) == 10, "task198:contexts")

    r_g = [model.substituted(g0, item) for item in ledger]
    r_f = [model.substituted(corrected, item) for item in ledger]
    signed = [r_g[i] if int(ledger[i]["factor_sign"]) > 0 else inverse(r_g[i])
              for i in range(11)]
    occurrences = []
    for index, item in enumerate(ledger):
        context = contexts[int(item["ten_index"])]
        require((context.get("type"), int(context.get("id"))) ==
                (item.get("type"), int(item.get("context_id"))),
                "task198:context_owner:" + str(index + 1))
        prefix = product(*(signed[int(k) - 1]
                           for k in item["fox_prefix_occurrences"]))
        p_word = product(prefix, r_g[index]) if int(item["factor_sign"]) > 0 else prefix
        block = normalize_block(str(item["block"]))
        occurrences.append({
            "ordinal": index + 1, "block": block, "position": POSITIONS[index],
            "type": item["type"],
            "registry_label": "C" + str(int(item["context_id"])),
            "repeated_e3_key": "E3_xy" if index + 1 in (1, 5) else None,
            "rank": 3 if block in ("H1", "H2") else 4,
            "rho": {"x": list(context["left"]), "y": list(context["right"])},
            "sigma": int(item["factor_sign"]), "prefix_word": list(p_word),
            "inverse_slot": int(item["factor_sign"]) == -1,
            "orientation": item["orientation"],
            "d_sources": [{"coefficient": 1, "left_word": [],
                           "fox_word": list(inverse(r_g[index])),
                           "provenance": {"owner": "task198-physical-bridge",
                                          "ordinal": index + 1,
                                          "ten_index": int(item["ten_index"]),
                                          "g760_sha256": digest(list(g0))}}],
        })
    relation = {block: relation_word(r_f, ledger, block) for block in BLOCKS}
    physical = task193.get("relation_words", {})
    require(list(relation["H1"]) == physical.get("hexagon_1") and
            list(relation["H2"]) == physical.get("hexagon_2") and
            list(relation["P"]) == physical.get("pentagon"),
            "task193:relation_words")
    epsilon = {
        block: [{"coefficient": -1, "left_word": [],
                 "fox_word": list(relation[block]),
                 "provenance": {"owner": "task193-v3", "block": block,
                                "corrected_sha256": digest(list(corrected))}}]
        for block in BLOCKS
    }
    m_terms = [{"coefficient": int(item["coefficient"]),
                "U": list(item["positive_word"]),
                "V": list(item["negative_word"]),
                "ancestry": {"prefix": item["prefix"],
                             "relator_index": int(item["relator_index"]),
                             "source_receipt_term": index}}
               for index, item in enumerate(pairs, 1)]
    return {"schema": LITERAL_SCHEMA, "mode": "PRODUCTION",
            "source_words": {"g0": list(g0), "corrected": list(corrected),
                             "correction": list(correction)},
            "M_terms": m_terms, "occurrences": occurrences,
            "epsilon_sources": epsilon, "bindings": bindings}


def endpoint_buckets(value: dict[str, Any]) -> dict[str, dict[str, int]]:
    answer: dict[str, dict[str, int]] = {}
    for block in BLOCKS:
        table: dict[str, int] = {}
        for row in value["endpoints"][block]["buckets"]:
            key = json.dumps(row["full_artin_key"], separators=(",", ":"))
            coefficient = int(row["coefficient_mod_3"]) % 3
            require(coefficient and key not in table, "endpoint:bucket_shape")
            table[key] = coefficient
        answer[block] = table
    return answer


def authenticate_artifact(raw_path: str, claimed: dict[str, Any],
                          label: str) -> tuple[dict[str, Any], dict[str, Any]]:
    value, got = read_json(raw_path, label, "ci/out")
    require(got == claimed, label + ":identity")
    check_seal(value, label)
    return value, got


def check_checkpoint(args: argparse.Namespace, receipt: dict[str, Any],
                     a5: dict[str, Any]) -> dict[str, Any]:
    claimed = receipt.get("artifacts", {}).get("checkpoint")
    require(type(claimed) is dict, "checkpoint:artifact")
    checkpoint, _ = authenticate_artifact(args.checkpoint, claimed, "checkpoint")
    require(checkpoint.get("schema") == CHECKPOINT_SCHEMA and
            checkpoint.get("source") == pin_identity(PRODUCER_PIN, "producer") and
            checkpoint.get("static_bindings") == static_bindings() and
            checkpoint.get("owners") == receipt.get("owners") and
            checkpoint.get("a5_result") == a5 and
            checkpoint.get("resume_contract") == {
                "all_or_none_path_bytes_sha256": True,
                "single_restore_before_search": True,
                "canonical_M_only": True}, "checkpoint:binding")
    return checkpoint


def check_sidecar(args: argparse.Namespace, receipt: dict[str, Any],
                  a5: dict[str, Any], base: Any, model: Any
                  ) -> tuple[dict[str, Any], dict[str, Any]]:
    claimed = receipt.get("artifacts", {}).get("a5_sidecar")
    require(type(claimed) is dict, "sidecar:artifact")
    sidecar, _ = authenticate_artifact(args.a5_sidecar, claimed, "sidecar")
    require(sidecar.get("schema") == SIDECAR_SCHEMA and
            sidecar.get("status") == "ACCEPTED_A5_MEMBER" and
            sidecar.get("terminal") == base.MEMBER and
            sidecar.get("source") == pin_identity(PRODUCER_PIN, "producer") and
            sidecar.get("static_bindings") == static_bindings() and
            sidecar.get("owners") == receipt.get("owners") and
            sidecar.get("a5_result") == a5, "sidecar:binding")
    return sidecar, base.check_member(model, a5)


def check(args: argparse.Namespace) -> dict[str, Any]:
    producer_source = pin_identity(PRODUCER_PIN, "producer")
    pin_identity(TASK292_PRODUCER_PIN, "task292:producer")
    base = load_pinned(BASE_CHECKER_PIN, "r07_a5_v3_checker_for_fusion_v4")
    task292 = load_pinned(TASK292_CHECKER_PIN, "r07_task292_v2_checker_for_fusion_v4")
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
    require(receipt.get("schema") == SCHEMA and receipt.get("mode") == "PRODUCTION" and
            receipt.get("source") == producer_source and
            receipt.get("static_bindings") == static_bindings(),
            "producer:envelope")
    require(receipt.get("owners", {}).get("task193_v3") == task193_id,
            "producer:task193_binding")
    owner198 = receipt.get("owners", {}).get("task198", {})
    require(owner198.get("receipt_sha256") == authority.identity.get("receipt_sha256") and
            owner198.get("manifest_sha256") == authority.identity.get("manifest_sha256"),
            "producer:task198_binding")
    model = base.CheckerModel(helper, authority, arithmetic, boundary, task193)
    result = receipt.get("result")
    require(type(result) is dict, "producer:result")
    a5 = result.get("a5")
    require(type(a5) is dict, "producer:a5")
    checkpoint = check_checkpoint(args, receipt, a5)

    if receipt.get("terminal") == NONMEMBER:
        require(receipt.get("status") == "COMPLETE" and
                receipt.get("artifacts", {}).get("a5_sidecar") is None and
                result.get("canonical_M_only") is True and
                result.get("v351_lift_null") == "NOT_IMPLEMENTED",
                "nonmember:envelope")
        replay = base.check_nonmember(model, a5)
        require(checkpoint.get("phase") == "A5_NONMEMBER_COMPLETE",
                "nonmember:checkpoint")
        endpoint_replay = None
        status = "ACCEPTED"
    else:
        require(receipt.get("terminal") == MEMBER or
                (type(receipt.get("terminal")) is str and
                 receipt["terminal"].startswith(UNKNOWN_RESOURCE + ":")),
                "producer:terminal")
        _sidecar, member_replay = check_sidecar(args, receipt, a5, base, model)
        terms = base.coefficient_terms(a5.get("coefficient_terms"))
        pairs = base.expected_m(model, terms)
        bindings = {"task198": receipt["owners"]["task198"],
                    "task193_v3": receipt["owners"]["task193_v3"],
                    "a5_v3_in_process": {
                        "source": static_bindings()["a5_v3"],
                        "result_digest_sha256": digest(a5)}}
        literal = literal_owner(base, helper, model, task193, pairs, bindings)
        task292.CHECK_BUDGET = task292.CheckerBudget()
        literal["M_immutable_digest_sha256"] = task292.collect_m(
            literal["M_terms"])["immutable_digest_sha256"]
        try:
            exact = task292.replay_literal(literal)
        except task292.CheckerResource as exc:
            raise Reject("task292:resource:" + exc.phase) from exc
        except task292.CheckStop as exc:
            raise Reject("task292:" + str(exc)) from exc
        producer_literal = result.get("literal_binding", {})
        require(producer_literal.get("schema") == LITERAL_SCHEMA and
                producer_literal.get("digest_sha256") == digest(literal) and
                all(producer_literal.get("owner_replay", {}).values()),
                "literal:binding")
        producer_endpoint = result.get(
            "endpoint_exact" if receipt.get("terminal") == MEMBER else
            "canonical_endpoint")
        require(type(producer_endpoint) is dict and
                producer_endpoint.get("M", {}).get("immutable_digest_sha256") ==
                exact["M"]["immutable_digest_sha256"] and
                endpoint_buckets(producer_endpoint) == endpoint_buckets(exact),
                "endpoint:independent_replay")
        endpoint_replay = {"terminal": exact["terminal"],
                           "M_digest_sha256": exact["M"]["immutable_digest_sha256"],
                           "bucket_support": {block: len(endpoint_buckets(exact)[block])
                                              for block in BLOCKS},
                           "independent_task292_replay": True}
        replay = member_replay
        if receipt.get("terminal") == MEMBER:
            require(receipt.get("status") == "COMPLETE" and
                    exact["terminal"] == task292.ZERO and
                    all(not exact["endpoints"][block]["buckets"] for block in BLOCKS) and
                    all(exact["full_C1_replay"]["blocks"][block]["D1_z_zero"]
                        for block in BLOCKS) and
                    checkpoint.get("phase") == "CANONICAL_ENDPOINT_ZERO_COMPLETE" and
                    result.get("canonical_M_only") is True and
                    result.get("v351_lift_null") == "NOT_IMPLEMENTED",
                    "member:exact_zero")
            status = "ACCEPTED"
        else:
            require(receipt.get("status") == UNKNOWN_RESOURCE and
                    exact["terminal"].startswith(task292.NONZERO) and
                    checkpoint.get("phase") ==
                    "CANONICAL_ENDPOINT_NONZERO_LIFT_NULL_PENDING" and
                    checkpoint.get("endpoint_terminal") == exact["terminal"] and
                    checkpoint.get("endpoint_digest_sha256") == digest(producer_endpoint) and
                    result.get("canonical_M_only") is True and
                    result.get("v351_lift_null") == "NOT_IMPLEMENTED" and
                    result.get("bounded_miss_is_A7_negative") is False,
                    "resource:honest_frontier")
            status = "ACCEPTED_RESOURCE"

    return seal({
        "schema": CHECK_SCHEMA, "status": status,
        "terminal": receipt["terminal"], "independent": True,
        "receipt": receipt_id, "task193_v3": task193_id,
        "task198": authority.identity, "a5_replay": replay,
        "endpoint_replay": endpoint_replay,
        "artifacts": receipt["artifacts"],
        "claims": {"A5_terminal": True,
                   "A6_M": receipt["terminal"] != NONMEMBER,
                   "A7": ("ZERO" if receipt["terminal"] == MEMBER else
                          "NONE" if receipt["terminal"] == NONMEMBER else
                          "UNKNOWN_RESOURCE"),
                   "canonical_M_only": True,
                   "v351_lift_null": "NOT_IMPLEMENTED",
                   "compatible_lift": "NONE", "fake": "NONE", "Ihara": "NONE"},
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
    ap.add_argument("--rss-bytes", type=int, default=8_000_000_000)
    for key, value in TASK198_DEFAULTS.items():
        ap.add_argument("--task198-" + key, dest="task198_" + key, default=value)
    return ap


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        require(args.seconds == 14_400 and args.rss_bytes == 8_000_000_000,
                "arguments:frozen_caps")
        verdict = check(args)
        write_exclusive(args.output, verdict)
        print(CHECKER_LINE + " terminal=" + str(verdict["terminal"]), flush=True)
        return 0
    except (Reject, OSError, ValueError, TypeError, KeyError, AttributeError) as exc:
        print(CHECKER_LINE + "_ERROR " + str(exc), flush=True)
        return 1
    except Exception as exc:
        print(CHECKER_LINE + "_ERROR " + str(exc), flush=True)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
