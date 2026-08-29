#!/usr/bin/env python3
"""Task376 production binder: frozen direct A5/A6 v3 -> exact task292 core.

This version deliberately implements the canonical-M lane only.  A nonzero
canonical endpoint is a controlled resource frontier, never an A7 negative.
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
LITERAL_SCHEMA = "d972-r07-actual-three-exact-pb-endpoints/v3/literal-input"
CHECKPOINT_SCHEMA = SCHEMA + "/checkpoint/v1"
SIDECAR_SCHEMA = SCHEMA + "/a5-sidecar/v1"
PRODUCER_LINE = "R07_DIRECT_RELATOR_A5_A7_FUSION_V4_PRODUCER_TERMINAL"
MEMBER = "R07_DIRECT_RELATOR_A5_A7_FUSION_MEMBER"
NONMEMBER = "R07_ZERO_BASE_A5_A6_NONMEMBER"
UNKNOWN_INPUT = "UNKNOWN_INPUT"
UNKNOWN_RESOURCE = "UNKNOWN_RESOURCE"
MODULUS = 3

BASE_PIN = (
    "search/d972_r07_zero_base_a5_a6_compiler_v3.py", 59239,
    "c287011d5e573452094e62c76020ab4b1076bc427103174b1771a22a1bb4fbd8")
TASK292_PIN = (
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


class InputStop(RuntimeError):
    pass


class ResourceStop(RuntimeError):
    pass


def need(value: bool, message: str) -> None:
    if value is not True:
        raise InputStop(message)


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
        need(letter != 0 and (alphabet is None or letter in alphabet), "word:letter")
        if out and out[-1] == -letter:
            out.pop()
        else:
            out.append(letter)
    return tuple(out)


def product(*words: Sequence[int]) -> tuple[int, ...]:
    return reduced(letter for word in words for letter in word)


def inverse(word: Sequence[int]) -> tuple[int, ...]:
    return tuple(-int(letter) for letter in reversed(tuple(word)))


def inside(raw: str | Path, area: str | None = None,
           must_exist: bool = True) -> Path:
    text = str(raw).replace("\\", "/")
    path = Path(text)
    need(not path.is_absolute() and ".." not in path.parts and "." not in path.parts,
         "path:lexical:" + text)
    try:
        value = (ROOT / path).resolve(strict=must_exist)
        value.relative_to(ROOT.resolve())
        if area is not None:
            value.relative_to((ROOT / area).resolve(strict=True))
    except (OSError, ValueError) as exc:
        raise InputStop("path:containment:" + text) from exc
    if must_exist:
        cursor = ROOT
        for part in path.parts:
            cursor /= part
            need(not stat.S_ISLNK(os.lstat(cursor).st_mode), "path:symlink")
    return value


def identity(path: Path) -> dict[str, Any]:
    raw = path.read_bytes()
    return {"path": path.relative_to(ROOT).as_posix(),
            "bytes": len(raw), "sha256": sha(raw)}


def read_json(raw_path: str, label: str, area: str = "ci/in"
              ) -> tuple[dict[str, Any], dict[str, Any]]:
    path = inside(raw_path, area)
    before = path.stat()
    raw = path.read_bytes()
    after = path.stat()
    need((before.st_dev, before.st_ino, before.st_size,
          getattr(before, "st_mtime_ns", 0)) ==
         (after.st_dev, after.st_ino, after.st_size,
          getattr(after, "st_mtime_ns", 0)), label + ":changed")
    try:
        value = json.loads(raw.decode("ascii"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise InputStop(label + ":json") from exc
    need(type(value) is dict, label + ":object")
    return value, {"path": path.relative_to(ROOT).as_posix(),
                   "bytes": len(raw), "sha256": sha(raw)}


def check_seal(value: dict[str, Any], label: str) -> None:
    claimed = value.get("self_digest_sha256")
    body = dict(value)
    body.pop("self_digest_sha256", None)
    need(type(claimed) is str and claimed == digest(body), label + ":seal")


def load_pinned(pin: tuple[str, int, str], name: str) -> types.ModuleType:
    path = inside(pin[0])
    raw = path.read_bytes()
    need(len(raw) == pin[1] and sha(raw) == pin[2], name + ":pin")
    spec = importlib.util.spec_from_file_location(name, path)
    need(spec is not None and spec.loader is not None, name + ":loader")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def source_identity() -> dict[str, Any]:
    return identity(Path(__file__).resolve())


def output_path(raw: str) -> Path:
    path = Path(str(raw).replace("\\", "/"))
    need(not path.is_absolute() and ".." not in path.parts and "." not in path.parts,
         "output:lexical")
    target = (ROOT / path).resolve(strict=False)
    need(target.parent == (ROOT / "ci/out").resolve(strict=True),
         "output:containment")
    return target


def write_exclusive(raw_path: str, value: dict[str, Any]) -> dict[str, Any]:
    path = output_path(raw_path)
    need(not path.exists(), "output:stale:" + str(raw_path))
    encoded = canon(value) + b"\n"
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    try:
        view = memoryview(encoded)
        while view:
            view = view[os.write(fd, view):]
        os.fsync(fd)
    finally:
        os.close(fd)
    return {"path": path.relative_to(ROOT).as_posix(),
            "bytes": len(encoded), "sha256": sha(encoded)}


def write_checkpoint(raw_path: str, value: dict[str, Any], limit: int
                     ) -> dict[str, Any]:
    path = output_path(raw_path)
    encoded = canon(value) + b"\n"
    if len(encoded) > int(limit):
        raise ResourceStop("phase=checkpoint:cap=checkpoint_bytes:value=" +
                           str(len(encoded)) + ":limit=" + str(limit))
    temporary = path.with_name(path.name + ".tmp")
    need(not temporary.exists(), "checkpoint:stale_temporary")
    fd = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    try:
        view = memoryview(encoded)
        while view:
            view = view[os.write(fd, view):]
        os.fsync(fd)
    finally:
        os.close(fd)
    os.replace(temporary, path)
    return {"path": path.relative_to(ROOT).as_posix(),
            "bytes": len(encoded), "sha256": sha(encoded)}


def static_bindings() -> dict[str, Any]:
    return {
        "a5_v3": {"path": BASE_PIN[0], "bytes": BASE_PIN[1], "sha256": BASE_PIN[2]},
        "task292_producer_v2": {"path": TASK292_PIN[0], "bytes": TASK292_PIN[1],
                                "sha256": TASK292_PIN[2]},
        "task292_checker_v2": {"path": TASK292_CHECKER_PIN[0],
                               "bytes": TASK292_CHECKER_PIN[1],
                               "sha256": TASK292_CHECKER_PIN[2]},
    }


def check_static_pin(pin: tuple[str, int, str], label: str) -> dict[str, Any]:
    got = identity(inside(pin[0]))
    want = {"path": pin[0], "bytes": pin[1], "sha256": pin[2]}
    need(got == want, label + ":pin")
    return want


def resume_load(args: argparse.Namespace) -> dict[str, Any] | None:
    supplied = (args.resume_path is not None, args.resume_bytes is not None,
                args.resume_sha256 is not None)
    need(len(set(supplied)) == 1, "resume:all_or_none")
    if not supplied[0]:
        return None
    value, got = read_json(args.resume_path, "resume", "ci/in")
    need(got["bytes"] == args.resume_bytes and
         got["sha256"] == args.resume_sha256, "resume:physical_identity")
    check_seal(value, "resume")
    need(value.get("schema") == CHECKPOINT_SCHEMA and
         value.get("source") == source_identity() and
         value.get("static_bindings") == static_bindings(),
         "resume:source_binding")
    return value


def normalize_block(raw: str) -> str:
    return "P" if raw.startswith("P") else raw


def validate_layout(helper: Any, authority: Any) -> list[dict[str, Any]]:
    ledger = authority.receipt.get("bridge", {}).get("occurrence_ledger")
    expected = getattr(helper, "BRIDGE_OWNER_LAYOUT", None)
    need(type(ledger) is list and type(expected) is tuple and len(ledger) == 11 and
         len(expected) == 11, "owner:ledger_cardinality")
    for index, (item, row) in enumerate(zip(ledger, expected), 1):
        actual = (item.get("block"), int(item.get("block_index")),
                  int(item.get("block_slot")), item.get("occurrence"),
                  item.get("type"), int(item.get("ten_index")),
                  int(item.get("context_id")), item.get("role"),
                  int(item.get("factor_sign")), item.get("orientation"),
                  tuple(item.get("fox_prefix_occurrences", ())))
        need(int(item.get("ordinal")) == index and actual == row,
             "owner:ledger_row:" + str(index))
    return ledger


def relation_word(words: list[tuple[int, ...]], ledger: list[dict[str, Any]],
                  block: str) -> tuple[int, ...]:
    selected = [(item, words[int(item["ordinal"]) - 1]) for item in ledger
                if normalize_block(str(item["block"])) == block]
    factors = [word if int(item["factor_sign"]) > 0 else inverse(word)
               for item, word in selected]
    return product(*(factors[index] for index in reversed(range(len(factors)))))


def literal_owner(base: Any, helper: Any, runtime: Any, authority: Any,
                  task193: dict[str, Any], pairs: list[dict[str, Any]],
                  bindings: dict[str, Any], task292: Any
                  ) -> tuple[dict[str, Any], dict[str, Any]]:
    ledger = validate_layout(helper, authority)
    g0 = reduced(task193.get("g760", ()), (1, -1, 2, -2))
    correction = reduced(task193.get("correction_word", ()), (1, -1, 2, -2))
    corrected = product(g0, correction)
    need(len(g0) == 760 and list(corrected) == task193.get("corrected_word"),
         "task193:corrected_literal")
    need(task193.get("literal_binding") == list(correction),
         "task193:correction_binding")

    contexts = runtime.contexts
    need(type(contexts) is list and len(contexts) == 10, "task198:contexts")
    r_g: list[tuple[int, ...]] = []
    r_f: list[tuple[int, ...]] = []
    for item in ledger:
        context = contexts[int(item["ten_index"])]
        need((context.get("type"), int(context.get("id"))) ==
             (item.get("type"), int(item.get("context_id"))),
             "task198:context_owner:" + str(item["ordinal"]))
        images = (context["left"], context["right"])
        r_g.append(tuple(runtime.old.f2_substitute(g0, *images)))
        r_f.append(tuple(runtime.old.f2_substitute(corrected, *images)))

    signed = [r_g[i] if int(ledger[i]["factor_sign"]) > 0 else inverse(r_g[i])
              for i in range(11)]
    occurrences = []
    for index, item in enumerate(ledger):
        prefix = product(*(signed[int(k) - 1]
                           for k in item["fox_prefix_occurrences"]))
        p_word = product(prefix, r_g[index]) if int(item["factor_sign"]) > 0 else prefix
        block = normalize_block(str(item["block"]))
        context = contexts[int(item["ten_index"])]
        occurrences.append({
            "ordinal": index + 1,
            "block": block,
            "position": POSITIONS[index],
            "type": item["type"],
            "registry_label": "C" + str(int(item["context_id"])),
            "repeated_e3_key": "E3_xy" if index + 1 in (1, 5) else None,
            "rank": 3 if block in ("H1", "H2") else 4,
            "rho": {"x": list(context["left"]), "y": list(context["right"])},
            "sigma": int(item["factor_sign"]),
            "prefix_word": list(p_word),
            "inverse_slot": int(item["factor_sign"]) == -1,
            "orientation": item["orientation"],
            "d_sources": [{
                "coefficient": 1,
                "left_word": [],
                "fox_word": list(inverse(r_g[index])),
                "provenance": {"owner": "task198-physical-bridge", "ordinal": index + 1,
                               "ten_index": int(item["ten_index"]),
                               "g760_sha256": digest(list(g0))},
            }],
        })

    relation = {block: relation_word(r_f, ledger, block) for block in BLOCKS}
    physical = task193.get("relation_words", {})
    need(list(relation["H1"]) == physical.get("hexagon_1"),
         "task193:relation_word:H1")
    need(list(relation["H2"]) == physical.get("hexagon_2"),
         "task193:relation_word:H2")
    need(list(relation["P"]) == physical.get("pentagon"),
         "task193:relation_word:P")
    epsilon = {
        block: [{"coefficient": -1, "left_word": [],
                 "fox_word": list(relation[block]),
                 "provenance": {"owner": "task193-v3", "block": block,
                                "corrected_sha256": digest(list(corrected))}}]
        for block in BLOCKS
    }

    m_terms = []
    for index, item in enumerate(pairs, 1):
        need(type(item) is dict and type(item.get("positive_word")) is list and
             type(item.get("negative_word")) is list, "v3:M_pair:" + str(index))
        m_terms.append({
            "coefficient": int(item["coefficient"]),
            "U": list(item["positive_word"]),
            "V": list(item["negative_word"]),
            "ancestry": {"prefix": item["prefix"],
                         "relator_index": int(item["relator_index"]),
                         "source_receipt_term": index},
        })
    aggregate = task292.aggregate_m(m_terms)
    literal = {
        "schema": LITERAL_SCHEMA,
        "mode": "PRODUCTION",
        "source_words": {"g0": list(g0), "corrected": list(corrected),
                         "correction": list(correction)},
        "M_terms": m_terms,
        "M_immutable_digest_sha256": aggregate["immutable_digest_sha256"],
        "occurrences": occurrences,
        "epsilon_sources": epsilon,
        "bindings": bindings,
    }
    replay = {"ledger_owner_exact": True, "context_owner_exact": True,
              "d1_pointed_replay": True, "corrected_relation_words": True,
              "task193_sign": "d1=-D1(g760),e1=-beta1"}
    return literal, replay


def task292_compile(task292: Any, literal: dict[str, Any],
                    bindings: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    internal = dict(literal)
    internal["schema"] = task292.SCHEMA + "/literal-input"
    budget = task292.Budget()
    try:
        terminal, result = task292.compile_literal(internal, bindings, budget)
    except task292.ResourceStop as exc:
        raise ResourceStop("phase=" + exc.phase + ":cap=" + exc.cap +
                           ":value=" + str(exc.value) + ":limit=" +
                           str(exc.limit)) from exc
    except task292.Stop as exc:
        raise InputStop("task292:" + str(exc)) from exc
    return terminal, result


def checkpoint_value(phase: str, owners: dict[str, Any] | None,
                     a5: dict[str, Any] | None,
                     endpoint_terminal: str | None,
                     endpoint_digest: str | None) -> dict[str, Any]:
    return seal({
        "schema": CHECKPOINT_SCHEMA,
        "mode": "PRODUCTION",
        "phase": phase,
        "source": source_identity(),
        "static_bindings": static_bindings(),
        "owners": owners,
        "a5_result": a5,
        "endpoint_terminal": endpoint_terminal,
        "endpoint_digest_sha256": endpoint_digest,
        "resume_contract": {"all_or_none_path_bytes_sha256": True,
                            "single_restore_before_search": True,
                            "canonical_M_only": True},
    })


def sidecar_value(owners: dict[str, Any], a5: dict[str, Any]) -> dict[str, Any]:
    return seal({"schema": SIDECAR_SCHEMA, "status": "ACCEPTED_A5_MEMBER",
                 "terminal": "R07_ZERO_BASE_A5_A6_MEMBER",
                 "source": source_identity(), "static_bindings": static_bindings(),
                 "owners": owners, "a5_result": a5,
                 "claims": {"A5": "MEMBER", "A6_M": True,
                            "A7": "NONE", "fake": "NONE", "Ihara": "NONE"}})


def build(args: argparse.Namespace, resume: dict[str, Any] | None
          ) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any] | None]:
    base = load_pinned(BASE_PIN, "r07_a5_v3_for_fusion_v4")
    task292 = load_pinned(TASK292_PIN, "r07_task292_v2_for_fusion_v4")
    check_static_pin(TASK292_CHECKER_PIN, "task292:checker")
    helper = base.load_task198()
    try:
        limits = dict(helper.CAPS)
        limits["wall_seconds"] = int(args.seconds)
        limits["rss_bytes"] = int(args.rss_bytes)
        meter = helper.Meter(limits)
        authority = helper.AuthorityAdapter(args, meter)
        runtime = helper.Runtime(authority, meter)
        boundary = helper.BoundaryLedger(runtime, meter)
        task193, task193_id, _verdict = base.load_task193(
            args.task193_receipt, args.task193_verdict)
        budget = base.Budget(args.max_operations)
        engine = base.DirectEngine(helper, authority, runtime, boundary, task193, budget)
    except (helper.ResourceStop, base.ResourceStop) as exc:
        raise ResourceStop(str(exc)) from exc
    except (helper.InputStop, helper.Reject, base.InputStop) as exc:
        raise InputStop(str(exc)) from exc

    owners = {"task198": authority.identity, "task193_v3": task193_id}
    if resume is not None:
        need(resume.get("owners") == owners, "resume:owner_binding")
        a5 = resume.get("a5_result")
        need(type(a5) is dict and a5.get("terminal_kind") == "MEMBER",
             "resume:a5_member_phase")
    else:
        try:
            a5 = engine.run()
        except base.ResourceStop as exc:
            raise ResourceStop(str(exc)) from exc
        except base.InputStop as exc:
            raise InputStop(str(exc)) from exc

    if a5.get("terminal_kind") == "NONMEMBER":
        checkpoint = checkpoint_value("A5_NONMEMBER_COMPLETE", owners, a5, None, None)
        receipt = seal({
            "schema": SCHEMA, "status": "COMPLETE", "terminal": NONMEMBER,
            "mode": "PRODUCTION", "source": source_identity(),
            "static_bindings": static_bindings(), "owners": owners,
            "result": {"a5": a5, "canonical_M_only": True,
                       "v351_lift_null": "NOT_IMPLEMENTED"},
            "claims": {"A5": "NONMEMBER", "A6_M": False, "A7": "NONE",
                       "compatible_lift": "NONE", "fake": "NONE", "Ihara": "NONE"},
        })
        return receipt, checkpoint, None

    need(a5.get("terminal_kind") == "MEMBER", "a5:terminal_kind")
    sidecar = sidecar_value(owners, a5)
    bindings = {"task198": authority.identity, "task193_v3": task193_id,
                "a5_v3_in_process": {"source": static_bindings()["a5_v3"],
                                     "result_digest_sha256": digest(a5)}}
    literal, owner_replay = literal_owner(base, helper, runtime, authority,
                                          task193, a5["M"]["pairs"],
                                          bindings, task292)
    endpoint_terminal, endpoint = task292_compile(task292, literal, bindings)
    endpoint_digest = digest(endpoint)
    if endpoint_terminal == task292.ZERO:
        need(all(endpoint["endpoints"][block]["zero"] for block in BLOCKS),
             "endpoint:zero_flags")
        checkpoint = checkpoint_value("CANONICAL_ENDPOINT_ZERO_COMPLETE", owners,
                                      a5, endpoint_terminal, endpoint_digest)
        receipt = seal({
            "schema": SCHEMA, "status": "COMPLETE", "terminal": MEMBER,
            "mode": "PRODUCTION", "source": source_identity(),
            "static_bindings": static_bindings(), "owners": owners,
            "result": {"terminal_kind": "MEMBER", "a5": a5,
                       "mu1": a5["mu1"], "M": endpoint["M"],
                       "literal_binding": {"schema": LITERAL_SCHEMA,
                                           "digest_sha256": digest(literal),
                                           "owner_replay": owner_replay},
                       "endpoint_exact": endpoint,
                       "canonical_M_only": True,
                       "v351_lift_null": "NOT_IMPLEMENTED"},
            "claims": {"A5": "MEMBER", "A6_M": True, "A7": "ZERO",
                       "compatible_lift": "NONE", "fake": "NONE", "Ihara": "NONE"},
        })
        return receipt, checkpoint, sidecar

    need(type(endpoint_terminal) is str and endpoint_terminal.startswith(task292.NONZERO),
         "endpoint:typed_terminal")
    checkpoint = checkpoint_value("CANONICAL_ENDPOINT_NONZERO_LIFT_NULL_PENDING",
                                  owners, a5, endpoint_terminal, endpoint_digest)
    terminal = (UNKNOWN_RESOURCE + ":phase=v351_lift_null:cap=not_implemented:"
                "value=canonical_endpoint_nonzero:limit=positive_dovetail_required")
    receipt = seal({
        "schema": SCHEMA, "status": UNKNOWN_RESOURCE, "terminal": terminal,
        "mode": "PRODUCTION", "source": source_identity(),
        "static_bindings": static_bindings(), "owners": owners,
        "result": {"reason": "canonical M exact endpoint is nonzero; v351 lift-null dovetail is not implemented",
                   "a5": a5, "mu1": a5["mu1"], "M": endpoint["M"],
                   "literal_binding": {"schema": LITERAL_SCHEMA,
                                       "digest_sha256": digest(literal),
                                       "owner_replay": owner_replay},
                   "canonical_endpoint": endpoint,
                   "canonical_M_only": True,
                   "v351_lift_null": "NOT_IMPLEMENTED",
                   "bounded_miss_is_A7_negative": False},
        "claims": {"A5": "MEMBER", "A6_M": True, "A7": "UNKNOWN_RESOURCE",
                   "compatible_lift": "NONE", "fake": "NONE", "Ihara": "NONE"},
    })
    return receipt, checkpoint, sidecar


def parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=("PRODUCTION",), default="PRODUCTION")
    ap.add_argument("--task193-receipt", required=True)
    ap.add_argument("--task193-verdict", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--checkpoint", required=True)
    ap.add_argument("--a5-sidecar", required=True)
    ap.add_argument("--resume-path")
    ap.add_argument("--resume-bytes", type=int)
    ap.add_argument("--resume-sha256")
    ap.add_argument("--max-operations", type=int, default=2_000_000_000)
    ap.add_argument("--seconds", type=int, default=14_400)
    ap.add_argument("--rss-bytes", type=int, default=8_000_000_000)
    ap.add_argument("--checkpoint-bytes", type=int, default=2_000_000_000)
    for key, value in TASK198_DEFAULTS.items():
        ap.add_argument("--task198-" + key, dest="task198_" + key, default=value)
    return ap


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    receipt: dict[str, Any]
    checkpoint: dict[str, Any]
    sidecar: dict[str, Any] | None = None
    checkpoint_id: dict[str, Any] | None = None
    sidecar_id: dict[str, Any] | None = None
    try:
        need(args.max_operations == 2_000_000_000 and args.seconds == 14_400 and
             args.rss_bytes == 8_000_000_000 and
             args.checkpoint_bytes == 2_000_000_000, "arguments:frozen_caps")
        resume = resume_load(args)
        receipt, checkpoint, sidecar = build(args, resume)
    except ResourceStop as exc:
        checkpoint = checkpoint_value("CONTROLLED_RESOURCE", None, None, None, None)
        receipt = seal({"schema": SCHEMA, "status": UNKNOWN_RESOURCE,
                        "terminal": UNKNOWN_RESOURCE + ":" + str(exc),
                        "mode": "PRODUCTION", "source": source_identity(),
                        "static_bindings": static_bindings(), "owners": None,
                        "result": {"reason": str(exc), "canonical_M_only": True,
                                   "v351_lift_null": "NOT_IMPLEMENTED"},
                        "claims": {"A5": "NONE", "A6_M": False, "A7": "NONE",
                                   "compatible_lift": "NONE", "fake": "NONE",
                                   "Ihara": "NONE"}})
    except (InputStop, OSError, ValueError, TypeError, KeyError, AttributeError) as exc:
        checkpoint = checkpoint_value("INPUT_REJECTED", None, None, None, None)
        receipt = seal({"schema": SCHEMA, "status": UNKNOWN_INPUT,
                        "terminal": UNKNOWN_INPUT + ":" + str(exc),
                        "mode": "PRODUCTION", "source": source_identity(),
                        "static_bindings": static_bindings(), "owners": None,
                        "result": {"reason": str(exc)},
                        "claims": {"A5": "NONE", "A6_M": False, "A7": "NONE",
                                   "compatible_lift": "NONE", "fake": "NONE",
                                   "Ihara": "NONE"}})

    checkpoint_id = write_checkpoint(args.checkpoint, checkpoint,
                                     args.checkpoint_bytes)
    if sidecar is not None:
        sidecar_id = write_exclusive(args.a5_sidecar, sidecar)
    receipt = dict(receipt)
    receipt.pop("self_digest_sha256", None)
    receipt["artifacts"] = {"checkpoint": checkpoint_id,
                            "a5_sidecar": sidecar_id}
    receipt = seal(receipt)
    write_exclusive(args.output, receipt)
    print(PRODUCER_LINE + " " + str(receipt["terminal"]), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
