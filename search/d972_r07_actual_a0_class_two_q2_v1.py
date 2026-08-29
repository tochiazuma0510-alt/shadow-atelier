#!/usr/bin/env python3
"""Task379: exact class-two q2 compiler for the accepted task193 A0 word.

This executable authenticates the physical task193 and task198 owners, then
performs only the finite PB3/PB4 class-two scan specified by v355.  In
particular, the applied word is task193.correction_word; no A5 coefficient
or endpoint receipt is an input to this compiler.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import stat
import time
import types
from pathlib import Path
from typing import Any, Iterable, Sequence


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "d972-r07-actual-a0-class-two-q2/v1"
CHECKPOINT_SCHEMA = SCHEMA + "/checkpoint/v1"
COMPLETE = "R07_ACTUAL_A0_CLASS_TWO_Q2_V1_COMPLETE"
UNKNOWN_INPUT = "UNKNOWN_INPUT"
UNKNOWN_RESOURCE = "UNKNOWN_RESOURCE"
PRODUCER_LINE = "R07_ACTUAL_A0_CLASS_TWO_Q2_V1_PRODUCER_TERMINAL"
BLOCKS = ("H1", "H2", "P")
MODULUS = 3

TASK193_SCHEMA = "d972-r07-second-frattini-affine-prefix-compiler/v3"
TASK193_TERMINAL = "R07_SECOND_FRATTINI_AFFINE_PREFIX_COMPILER_V3"
TASK193_CHECK_SCHEMA = TASK193_SCHEMA + "/checker-verdict/v3"
TASK193_PRODUCER_PIN = (
    "search/d972_r07_second_frattini_affine_prefix_compiler_v3.py", 2826,
    "1ac65ca533e11ac39def79c84de0bbdcb018d463ac10bca6158db254a61da741")
TASK193_CHECKER_PIN = (
    "crosscheck/check_d972_r07_second_frattini_affine_prefix_compiler_v3.py", 2792,
    "5b3c5b3e607077e0bebcf0153c592465983ba210b768c93ea62aeb2201c905c6")
TASK193_DRIVER_PIN = (
    "search/d972_r07_second_frattini_affine_prefix_compiler_gha_driver_v3.g", 5798,
    "c11074bd1e634aa38d4d164699542e17087e659115c31b8f5b8cc322dc5dfd84")
TASK292_PIN = (
    "search/d972_r07_actual_three_exact_pb_endpoints_v2.py", 40044,
    "c44d2c8e7fdd7dcbf691600ba823445d1ac45695ef173043c723874a409f7208")
TASK292_CHECKER_PIN = (
    "crosscheck/check_d972_r07_actual_three_exact_pb_endpoints_v2.py", 46873,
    "8d7598f376715af16ccec7bae5550f2c5329922b1b36326643a2a4e9e7cf72d8")
TASK198_WRAPPER_PIN = (
    "search/d972_r07_word_independent_successor_kernel_v12.py", 7209,
    "816bae92d86ac4bf3a6feb05297f505680072c2ce793db97135154cef928e9c5")
TASK198_V6_PIN = (
    "search/d972_r07_word_independent_successor_kernel_v6.py", 219187,
    "aaa8a60960698eeeab0c300f7fb65bb902bbae7e5507e4bef933cdff26263a6a")
TASK198_CHECKER_WRAPPER_PIN = (
    "crosscheck/check_d972_r07_word_independent_successor_kernel_v14.py", 8074,
    "7ff0fb8888b46febb8b373914a3ba31ee555e43c829e60dae915bacfb16b7b47")
TASK198_CHECKER_V6_PIN = (
    "crosscheck/check_d972_r07_word_independent_successor_kernel_v6.py", 258847,
    "432bcaadfa1dcfd9526749c40fb3d56c1bdb5671a1959d571a8076c20ba29ccf")

TASK198_DEFAULTS = {
    "receipt": "ci/in/d972_r07_seven_context_roof_presentation_v1.json",
    "manifest": "ci/in/d972_r07_seven_context_roof_presentation_v1.acceptance_v2.json",
    "producer": "ci/in/d972_r07_seven_context_roof_presentation_v1.producer.attestation.txt",
    "checker": "ci/in/d972_r07_seven_context_roof_presentation_v1.checker.attestation.txt",
    "verdict": "ci/in/d972_r07_seven_context_roof_presentation_v1.checker.verdict.json",
}

# Physical task198 ordinal order.  Literal printed factor order is the reverse
# order within each block, as witnessed by fox_prefix_occurrences.
EXPECTED_LAYOUT = (
    ("H1", 1, 1, "H1_fxy", "E3", 0, 21, "hexagon_fxy", 1, "direct", (3, 2)),
    ("H1", 1, 2, "H1_fxz", "E3", 1, 22, "hexagon_fxz", -1, "inverse", (3,)),
    ("H1", 1, 3, "H1_fyz", "E3", 2, 23, "hexagon_fyz", 1, "direct", ()),
    ("H2", 2, 1, "H2_fux", "E3", 3, 24, "hexagon_fux", -1, "inverse", (6, 5)),
    ("H2", 2, 2, "H2_fxy", "E3", 0, 21, "hexagon_fxy", -1, "inverse", (6,)),
    ("H2", 2, 3, "H2_fuy", "E3", 4, 25, "hexagon_fuy", 1, "direct", ()),
    ("P1", 3, 1, "P_b1", "E4", 5, 1, "pentagon_b1", 1, "direct", (11, 10, 9, 8)),
    ("P2", 4, 1, "P_b2", "E4", 6, 27, "pentagon_b2", 1, "direct", (11, 10, 9)),
    ("P3", 5, 1, "P_b3", "E4", 7, 21, "pentagon_b3", 1, "direct", (11, 10)),
    ("P5", 6, 1, "P_b5_inverse", "E4", 8, 26, "pentagon_b5_inverse_slot", -1, "inverse", (11,)),
    ("P4", 7, 1, "P_b4_inverse", "E4", 9, 28, "pentagon_b4_inverse_slot", -1, "inverse", ()),
)
FACTOR_ORDER = {"H1": (3, 2, 1), "H2": (6, 5, 4),
                "P": (11, 10, 9, 8, 7)}
GLOBAL_FACTOR_ORDER = tuple(value for block in BLOCKS for value in FACTOR_ORDER[block])
REGISTERED_POSITIONS = (1, 2, 3, 1, 2, 3, 1, 2, 3, 5, 4)


class InputStop(RuntimeError):
    pass


class ResourceStop(RuntimeError):
    pass


def need(value: bool, message: str) -> None:
    if value is not True:
        raise InputStop(message)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def digest(value: Any) -> str:
    return sha(canonical(value))


def seal(value: dict[str, Any]) -> dict[str, Any]:
    answer = dict(value)
    answer.pop("self_digest_sha256", None)
    answer["self_digest_sha256"] = digest(answer)
    return answer


def check_seal(value: dict[str, Any], label: str) -> None:
    claimed = value.get("self_digest_sha256", value.get("self_digest"))
    body = dict(value)
    body.pop("self_digest_sha256", None)
    body.pop("self_digest", None)
    need(type(claimed) is str and claimed == digest(body), label + ":seal")


def inside(raw: str | Path, area: str | None = None,
           must_exist: bool = True) -> Path:
    text = str(raw).replace("\\", "/")
    path = Path(text)
    need(not path.is_absolute() and ".." not in path.parts and
         "." not in path.parts, "path:lexical:" + text)
    try:
        result = (ROOT / path).resolve(strict=must_exist)
        result.relative_to(ROOT.resolve())
        if area is not None:
            result.relative_to((ROOT / area).resolve(strict=True))
    except (OSError, ValueError) as exc:
        raise InputStop("path:containment:" + text) from exc
    if must_exist:
        cursor = ROOT
        for part in path.parts:
            cursor /= part
            need(not stat.S_ISLNK(os.lstat(cursor).st_mode),
                 "path:symlink:" + text)
    return result


def identity(path: Path) -> dict[str, Any]:
    raw = path.read_bytes()
    return {"path": path.relative_to(ROOT).as_posix(),
            "bytes": len(raw), "sha256": sha(raw)}


def check_pin(pin: tuple[str, int, str], label: str) -> dict[str, Any]:
    got = identity(inside(pin[0]))
    wanted = {"path": pin[0], "bytes": pin[1], "sha256": pin[2]}
    need(got == wanted, label + ":pin")
    return wanted


def read_json(raw_path: str, label: str, area: str
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
        raise InputStop(label + ":ascii_json") from exc
    need(type(value) is dict, label + ":object")
    return value, {"path": path.relative_to(ROOT).as_posix(),
                   "bytes": len(raw), "sha256": sha(raw)}


def output_path(raw: str) -> Path:
    path = Path(str(raw).replace("\\", "/"))
    need(not path.is_absolute() and ".." not in path.parts and
         "." not in path.parts, "output:lexical")
    result = (ROOT / path).resolve(strict=False)
    need(result.parent == (ROOT / "ci/out").resolve(strict=True),
         "output:containment")
    return result


def write_exclusive(raw_path: str, value: dict[str, Any]) -> dict[str, Any]:
    path = output_path(raw_path)
    need(not path.exists(), "output:stale:" + raw_path)
    raw = canonical(value) + b"\n"
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    try:
        view = memoryview(raw)
        while view:
            view = view[os.write(fd, view):]
        os.fsync(fd)
    finally:
        os.close(fd)
    return {"path": path.relative_to(ROOT).as_posix(),
            "bytes": len(raw), "sha256": sha(raw)}


def write_checkpoint(raw_path: str, value: dict[str, Any], cap: int
                     ) -> dict[str, Any]:
    path = output_path(raw_path)
    raw = canonical(value) + b"\n"
    if len(raw) > int(cap):
        raise ResourceStop("phase=checkpoint:cap=checkpoint_bytes:value=" +
                           str(len(raw)) + ":limit=" + str(int(cap)))
    temporary = path.with_name(path.name + ".tmp")
    need(not temporary.exists(), "checkpoint:stale_temporary")
    fd = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    try:
        view = memoryview(raw)
        while view:
            view = view[os.write(fd, view):]
        os.fsync(fd)
    finally:
        os.close(fd)
    os.replace(temporary, path)
    return {"path": path.relative_to(ROOT).as_posix(),
            "bytes": len(raw), "sha256": sha(raw)}


def source_identity() -> dict[str, Any]:
    return identity(Path(__file__).resolve())


def static_bindings() -> dict[str, Any]:
    return {
        "task193_producer_v3": {"path": TASK193_PRODUCER_PIN[0],
                                 "bytes": TASK193_PRODUCER_PIN[1],
                                 "sha256": TASK193_PRODUCER_PIN[2]},
        "task193_checker_v3": {"path": TASK193_CHECKER_PIN[0],
                                "bytes": TASK193_CHECKER_PIN[1],
                                "sha256": TASK193_CHECKER_PIN[2]},
        "task193_driver_v3": {"path": TASK193_DRIVER_PIN[0],
                               "bytes": TASK193_DRIVER_PIN[1],
                               "sha256": TASK193_DRIVER_PIN[2]},
        "task292_producer_v2": {"path": TASK292_PIN[0],
                                 "bytes": TASK292_PIN[1],
                                 "sha256": TASK292_PIN[2]},
        "task292_checker_v2": {"path": TASK292_CHECKER_PIN[0],
                                "bytes": TASK292_CHECKER_PIN[1],
                                "sha256": TASK292_CHECKER_PIN[2]},
        "task198_producer_v12": {"path": TASK198_WRAPPER_PIN[0],
                                  "bytes": TASK198_WRAPPER_PIN[1],
                                  "sha256": TASK198_WRAPPER_PIN[2]},
        "task198_producer_v6": {"path": TASK198_V6_PIN[0],
                                 "bytes": TASK198_V6_PIN[1],
                                 "sha256": TASK198_V6_PIN[2]},
        "task198_checker_v14": {"path": TASK198_CHECKER_WRAPPER_PIN[0],
                                 "bytes": TASK198_CHECKER_WRAPPER_PIN[1],
                                 "sha256": TASK198_CHECKER_WRAPPER_PIN[2]},
        "task198_checker_v6": {"path": TASK198_CHECKER_V6_PIN[0],
                                "bytes": TASK198_CHECKER_V6_PIN[1],
                                "sha256": TASK198_CHECKER_V6_PIN[2]},
    }


def restore_static_sources() -> dict[str, Any]:
    for label, pin in (
            ("task193_producer_v3", TASK193_PRODUCER_PIN),
            ("task193_checker_v3", TASK193_CHECKER_PIN),
            ("task193_driver_v3", TASK193_DRIVER_PIN),
            ("task292_producer_v2", TASK292_PIN),
            ("task292_checker_v2", TASK292_CHECKER_PIN),
            ("task198_producer_v12", TASK198_WRAPPER_PIN),
            ("task198_producer_v6", TASK198_V6_PIN),
            ("task198_checker_v14", TASK198_CHECKER_WRAPPER_PIN),
            ("task198_checker_v6", TASK198_CHECKER_V6_PIN)):
        check_pin(pin, label)
    return static_bindings()


def load_pinned(pin: tuple[str, int, str], name: str) -> types.ModuleType:
    check_pin(pin, name)
    path = inside(pin[0])
    spec = importlib.util.spec_from_file_location(name, path)
    need(spec is not None and spec.loader is not None, name + ":loader")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_task198() -> types.ModuleType:
    wrapper_path = inside(TASK198_WRAPPER_PIN[0])
    wrapper_raw = wrapper_path.read_bytes()
    need(len(wrapper_raw) == TASK198_WRAPPER_PIN[1] and
         sha(wrapper_raw) == TASK198_WRAPPER_PIN[2], "task198:v12_wrapper_pin")
    spec = importlib.util.spec_from_file_location("r07_task198_v12_q2_wrapper",
                                                  wrapper_path)
    need(spec is not None and spec.loader is not None, "task198:wrapper_loader")
    wrapper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(wrapper)
    source = Path(wrapper.SOURCE)
    raw = source.read_bytes()
    need(len(raw) == int(wrapper.SOURCE_BYTES) and
         sha(raw) == str(wrapper.SOURCE_SHA256) and
         identity(source) == {"path": TASK198_V6_PIN[0],
                              "bytes": TASK198_V6_PIN[1],
                              "sha256": TASK198_V6_PIN[2]},
         "task198:v6_source_pin")
    for index, pair in enumerate(wrapper.PATCHES):
        need(type(pair) is tuple and len(pair) == 2,
             "task198:patch_shape:" + str(index))
        old, new = pair
        need(type(old) is bytes and type(new) is bytes and old and new and
             old != new and raw.count(old) == 1,
             "task198:patch_cardinality:" + str(index))
        raw = raw.replace(old, new)
    module = types.ModuleType("r07_task198_v12_q2_runtime")
    module.__file__ = str(source)
    module.__package__ = None
    exec(compile(raw, str(source), "exec"), module.__dict__, module.__dict__)
    for name in ("Meter", "AuthorityAdapter", "Runtime", "BRIDGE_OWNER_LAYOUT"):
        need(hasattr(module, name), "task198:runtime_symbol:" + name)
    return module


class Budget:
    def __init__(self, seconds: int, rss_bytes: int, operations: int):
        self.seconds = int(seconds)
        self.rss_bytes = int(rss_bytes)
        self.operations = int(operations)
        self.used_operations = 0
        self.started = time.monotonic()
        self.peak_rss = 0
        self.phase = "START"

    def _rss(self) -> int:
        try:
            usage = int(__import__("resource").getrusage(0).ru_maxrss)
            return usage * 1024
        except Exception:
            return 0

    def check(self, phase: str) -> None:
        self.phase = phase
        elapsed = time.monotonic() - self.started
        self.peak_rss = max(self.peak_rss, self._rss())
        if elapsed > self.seconds:
            raise ResourceStop("phase=" + phase + ":cap=seconds:value=" +
                               str(elapsed) + ":limit=" + str(self.seconds))
        if self.peak_rss > self.rss_bytes:
            raise ResourceStop("phase=" + phase + ":cap=rss_bytes:value=" +
                               str(self.peak_rss) + ":limit=" + str(self.rss_bytes))
        if self.used_operations > self.operations:
            raise ResourceStop("phase=" + phase + ":cap=operations:value=" +
                               str(self.used_operations) + ":limit=" +
                               str(self.operations))

    def bump(self, amount: int, phase: str) -> None:
        before = self.used_operations
        self.used_operations += max(0, int(amount))
        if (self.used_operations > self.operations or
                self.used_operations // 4096 != before // 4096):
            self.check(phase)

    def snapshot(self) -> dict[str, Any]:
        self.check(self.phase)
        return {"caps": {"seconds": self.seconds, "rss_bytes": self.rss_bytes,
                         "operations": self.operations},
                "used": {"seconds": time.monotonic() - self.started,
                         "rss_bytes": self.peak_rss,
                         "operations": self.used_operations},
                "last_phase": self.phase}


def helper_limits(helper: Any, args: argparse.Namespace) -> dict[str, int | float]:
    limits = dict(helper.CAPS)
    limits["wall_seconds"] = min(float(limits["wall_seconds"]), float(args.seconds))
    limits["rss_bytes"] = min(int(limits["rss_bytes"]), int(args.rss_bytes))
    kinds = getattr(helper, "COUNTER_TYPES", {})
    for key, kind in kinds.items():
        if kind in ("semantic", "validation"):
            limits[key] = min(int(limits[key]), int(args.max_operations))
    return limits


def helper_charge(meter: Any, budget: Budget, phase: str) -> None:
    counters = getattr(meter, "counters", {})
    kinds = getattr(meter, "counter_types", {})
    amount = sum(int(value) for key, value in counters.items()
                 if kinds.get(key) in ("semantic", "validation"))
    budget.bump(amount, phase)


def free_reduce(word: Iterable[int], width: int | None = None) -> tuple[int, ...]:
    answer: list[int] = []
    for raw in word:
        need(type(raw) is int and raw != 0, "word:letter")
        if width is not None:
            need(abs(raw) <= width, "word:width")
        if answer and answer[-1] == -raw:
            answer.pop()
        else:
            answer.append(raw)
    return tuple(answer)


def inverse(word: Sequence[int]) -> tuple[int, ...]:
    return tuple(-int(letter) for letter in reversed(tuple(word)))


def product(*words: Sequence[int], width: int | None = None) -> tuple[int, ...]:
    return free_reduce((letter for word in words for letter in word), width)


def exponent_sums(word: Sequence[int], width: int) -> list[int]:
    result = [0] * width
    for letter in word:
        result[abs(int(letter)) - 1] += 1 if int(letter) > 0 else -1
    return result


def sparse_add(left: dict[int, int], right: dict[int, int], scale: int = 1
               ) -> dict[int, int]:
    answer = dict(left)
    for key, value in right.items():
        updated = (answer.get(int(key), 0) + int(scale) * int(value)) % MODULUS
        if updated:
            answer[int(key)] = updated
        else:
            answer.pop(int(key), None)
    return answer


def sparse_scale(row: dict[int, int], scale: int) -> dict[int, int]:
    return {int(key): (int(value) * int(scale)) % MODULUS
            for key, value in row.items()
            if (int(value) * int(scale)) % MODULUS}


def sparse_public(row: dict[int, int]) -> list[list[int]]:
    return [[int(key), int(row[key]) % MODULUS] for key in sorted(row)
            if int(row[key]) % MODULUS]


def sparse_parse(raw: Any, width: int, label: str) -> dict[int, int]:
    need(type(raw) is list, label + ":list")
    answer: dict[int, int] = {}
    last = 0
    for item in raw:
        need(type(item) is list and len(item) == 2 and
             type(item[0]) is int and type(item[1]) is int,
             label + ":entry")
        key, value = item
        need(last < key <= width and value in (1, 2), label + ":canonical")
        answer[key] = value
        last = key
    return answer


def wedge_basis(dimension: int) -> list[tuple[int, int]]:
    return [(i, j) for i in range(1, dimension)
            for j in range(i + 1, dimension + 1)]


def wedge(left: dict[int, int], right: dict[int, int], dimension: int
          ) -> dict[int, int]:
    answer: dict[int, int] = {}
    for column, (i, j) in enumerate(wedge_basis(dimension), 1):
        value = (left.get(i, 0) * right.get(j, 0) -
                 left.get(j, 0) * right.get(i, 0)) % MODULUS
        if value:
            answer[column] = value
    return answer


def scan_word(word: Sequence[int], dimension: int, budget: Budget,
              phase: str) -> tuple[dict[int, int], dict[int, int]]:
    linear: dict[int, int] = {}
    quadratic: dict[int, int] = {}
    for letter in word:
        index = abs(int(letter))
        need(1 <= index <= dimension, phase + ":letter")
        step = {index: 1 if int(letter) > 0 else 2}
        quadratic = sparse_add(quadratic, wedge(linear, step, dimension), 2)
        linear = sparse_add(linear, step)
        budget.bump(max(1, len(linear) + len(quadratic)), phase)
    return linear, quadratic


def rref(rows: Sequence[dict[int, int]], columns: int
         ) -> list[dict[int, int]]:
    work = [{int(key): int(value) % MODULUS for key, value in row.items()
             if int(value) % MODULUS} for row in rows]
    work = [row for row in work if row]
    cursor = 0
    for column in range(1, columns + 1):
        selected = next((index for index in range(cursor, len(work))
                         if work[index].get(column, 0)), None)
        if selected is None:
            continue
        work[cursor], work[selected] = work[selected], work[cursor]
        pivot_value = work[cursor][column]
        work[cursor] = sparse_scale(work[cursor], 1 if pivot_value == 1 else 2)
        for index in range(len(work)):
            if index != cursor and work[index].get(column, 0):
                work[index] = sparse_add(work[index], work[cursor],
                                         -work[index][column])
        cursor += 1
        if cursor == len(work):
            break
    return work[:cursor]


def reduce_mod_relations(row: dict[int, int], echelon: Sequence[dict[int, int]]
                         ) -> dict[int, int]:
    answer = dict(row)
    for pivot_row in echelon:
        pivot = min(pivot_row)
        coefficient = answer.get(pivot, 0)
        if coefficient:
            answer = sparse_add(answer, pivot_row, -coefficient)
    return answer


def load_task193(receipt_path: str, verdict_path: str
                 ) -> tuple[dict[str, Any], dict[str, Any]]:
    sources = {"producer": check_pin(TASK193_PRODUCER_PIN, "task193:producer"),
               "checker": check_pin(TASK193_CHECKER_PIN, "task193:checker"),
               "driver": check_pin(TASK193_DRIVER_PIN, "task193:driver")}
    receipt, receipt_id = read_json(receipt_path, "task193:receipt", "ci/in")
    verdict, verdict_id = read_json(verdict_path, "task193:verdict", "ci/in")
    check_seal(receipt, "task193:receipt")
    check_seal(verdict, "task193:verdict")
    need(receipt.get("schema") == TASK193_SCHEMA and
         receipt.get("status") == "PASS" and
         receipt.get("terminal") == TASK193_TERMINAL,
         "task193:not_member")
    need(verdict.get("schema") == TASK193_CHECK_SCHEMA and
         verdict.get("status") == "PASS" and
         verdict.get("terminal") == TASK193_TERMINAL,
         "task193:checker_not_accepted")
    bound = verdict.get("receipt", {})
    need(bound.get("bytes") == receipt_id["bytes"] and
         bound.get("sha256") == receipt_id["sha256"],
         "task193:verdict_binding")
    claims = verdict.get("claims", {})
    need(claims.get("independent_task193_replay") is True and
         claims.get("pointed_rows") is True, "task193:checker_claims")
    frontier = receipt.get("claims", {})
    need(frontier.get("lift") == "NONE" and frontier.get("fake") == "NONE" and
         frontier.get("Ihara") == "NONE", "task193:frontier")
    return receipt, {"receipt": receipt_id, "verdict": verdict_id,
                     "sources": sources,
                     "accepted_lane": "task193-v3-PASS-member"}


def task193_words(task193: dict[str, Any]) -> dict[str, Any]:
    g0 = free_reduce(task193.get("g760", ()), 2)
    correction = free_reduce(task193.get("correction_word", ()), 2)
    corrected = free_reduce(task193.get("corrected_word", ()), 2)
    need(type(task193.get("g760")) is list and len(g0) == 760 and
         list(g0) == task193.get("g760"), "task193:g760")
    need(type(task193.get("correction_word")) is list and
         list(correction) == task193.get("correction_word"),
         "task193:correction_word")
    need(type(task193.get("corrected_word")) is list and
         list(corrected) == task193.get("corrected_word") and
         corrected == product(g0, correction, width=2),
         "task193:corrected_literal")
    need(task193.get("literal_binding") == list(correction),
         "task193:applied_word_binding")
    relations = task193.get("relation_words")
    need(type(relations) is dict and
         set(relations) == {"hexagon_1", "hexagon_2", "pentagon"},
         "task193:relation_words")
    h1 = free_reduce(relations["hexagon_1"], 3)
    h2 = free_reduce(relations["hexagon_2"], 3)
    pentagon = free_reduce(relations["pentagon"], 6)
    need(list(h1) == relations["hexagon_1"] and
         list(h2) == relations["hexagon_2"] and
         list(pentagon) == relations["pentagon"],
         "task193:relation_words_reduced")
    sums = {"g760": exponent_sums(g0, 2),
            "correction_word": exponent_sums(correction, 2),
            "corrected_word": exponent_sums(corrected, 2)}
    need(all(value == [0, 0] for value in sums.values()),
         "task193:v356_exponent_zero_abi")
    return {"g760": list(g0), "correction_word": list(correction),
            "corrected_word": list(corrected),
            "relation_words": {"H1": list(h1), "H2": list(h2),
                               "P": list(pentagon)},
            "exponent_sums_F2": sums,
            "applied_word_owner": "task193.correction_word",
            "a5_mu_used": False}


def normalize_block(value: str) -> str:
    return "P" if str(value).startswith("P") else str(value)


def validate_layout(helper: Any, authority: Any) -> list[dict[str, Any]]:
    need(tuple(helper.BRIDGE_OWNER_LAYOUT) == EXPECTED_LAYOUT,
         "task198:producer_layout_drift")
    ledger = authority.receipt.get("bridge", {}).get("occurrence_ledger")
    need(type(ledger) is list and len(ledger) == len(EXPECTED_LAYOUT),
         "task198:ledger_cardinality")
    for index, (item, expected) in enumerate(zip(ledger, EXPECTED_LAYOUT), 1):
        actual = (item.get("block"), int(item.get("block_index")),
                  int(item.get("block_slot")), item.get("occurrence"),
                  item.get("type"), int(item.get("ten_index")),
                  int(item.get("context_id")), item.get("role"),
                  int(item.get("factor_sign")), item.get("orientation"),
                  tuple(item.get("fox_prefix_occurrences", ())))
        need(int(item.get("ordinal")) == index and actual == expected,
             "task198:ledger_row:" + str(index))
    for block in BLOCKS:
        for position, ordinal in enumerate(FACTOR_ORDER[block], 1):
            item = ledger[ordinal - 1]
            need(normalize_block(item["block"]) == block and
                 tuple(item["fox_prefix_occurrences"]) ==
                 tuple(FACTOR_ORDER[block][:position - 1]),
                 "task198:printed_prefix:" + block + ":" + str(position))
    return ledger


def build_pb_owner(task292: Any, rank: int, budget: Budget
                   ) -> tuple[dict[str, Any], list[dict[int, int]]]:
    pairs = task292.pair_list(rank)
    need(pairs == [[i, j] for i in range(1, rank)
                   for j in range(i + 1, rank + 1)], "task292:pair_order")
    dimension = len(pairs)
    wedge_pairs = wedge_basis(dimension)
    relators = task292.pure_relations(rank)
    need(len(relators) == (2 if rank == 3 else 11),
         "task292:relator_count")
    rows: list[dict[int, int]] = []
    records = []
    for index, raw in enumerate(relators, 1):
        word = free_reduce(raw, dimension)
        need(list(word) == raw, "task292:relator_reduced:" + str(index))
        ell, tau = scan_word(word, dimension, budget,
                             "PB" + str(rank) + "_RELATOR_" + str(index))
        need(not ell, "task292:relator_degree_one:" + str(index))
        rows.append(tau)
        records.append({"index": index, "word": list(word),
                        "raw": {"ell": sparse_public(ell),
                                "tau": sparse_public(tau)}})
    echelon = rref(rows, len(wedge_pairs))
    expected_dimension = 1 if rank == 3 else 4
    need(len(wedge_pairs) - len(echelon) == expected_dimension,
         "task292:class_two_dimension:PB" + str(rank))
    for record, row in zip(records, rows):
        reduced = reduce_mod_relations(row, echelon)
        need(not reduced, "task292:full_relator_nonzero:" +
             str(record["index"]))
        record["relation_reduced"] = {"ell": [], "tau": sparse_public(reduced)}
        record["vanishes"] = True
    owner = {
        "tag": "PB" + str(rank),
        "rank": rank,
        "generator_basis": [{"index": index + 1, "pair": pair}
                            for index, pair in enumerate(pairs)],
        "wedge_basis": [{"index": index + 1, "generators": list(pair)}
                        for index, pair in enumerate(wedge_pairs)],
        "relators": records,
        "initial_form_matrix": [sparse_public(row) for row in rows],
        "initial_form_echelon": [sparse_public(row) for row in echelon],
        "relation_rank": len(echelon),
        "quotient_dimension": expected_dimension,
        "all_full_relators_zero": True,
    }
    return owner, echelon


def occurrence_words(task292: Any, runtime: Any, ledger: list[dict[str, Any]],
                     words: dict[str, Any], budget: Budget
                     ) -> list[dict[str, Any]]:
    g0 = words["g760"]
    correction = words["correction_word"]
    corrected = words["corrected_word"]
    contexts = runtime.contexts
    need(type(contexts) is list and len(contexts) == 10,
         "task198:producer_contexts")
    g_values: list[tuple[int, ...]] = []
    a_values: list[tuple[int, ...]] = []
    f_values: list[tuple[int, ...]] = []
    for index, item in enumerate(ledger):
        context = contexts[int(item["ten_index"])]
        need((context.get("type"), int(context.get("id"))) ==
             (item.get("type"), int(item.get("context_id"))),
             "task198:context_owner:" + str(index + 1))
        width = 3 if item["type"] == "E3" else 6
        left, right = list(context["left"]), list(context["right"])
        g = tuple(task292.substitute_f2(g0, left, right, width))
        a = tuple(task292.substitute_f2(correction, left, right, width))
        f = tuple(task292.substitute_f2(corrected, left, right, width))
        need(f == product(g, a, width=width),
             "task193:substitution_right_correction:" + str(index + 1))
        g_values.append(g)
        a_values.append(a)
        f_values.append(f)
        budget.bump(len(g) + len(a) + len(f), "OCCURRENCE_SUBSTITUTION")
    signed_g = [g_values[index] if int(item["factor_sign"]) > 0
                else inverse(g_values[index])
                for index, item in enumerate(ledger)]
    result = []
    for index, item in enumerate(ledger):
        ordinal = index + 1
        block = normalize_block(item["block"])
        width = 3 if block in ("H1", "H2") else 6
        prefix_ordinals = tuple(int(value)
                                for value in item["fox_prefix_occurrences"])
        old_prefix = product(*(signed_g[value - 1]
                               for value in prefix_ordinals), width=width)
        p_hat = (product(old_prefix, g_values[index], width=width)
                 if int(item["factor_sign"]) > 0 else old_prefix)
        applied = (a_values[index] if int(item["factor_sign"]) > 0
                   else inverse(a_values[index]))
        d_word = product(p_hat, applied, inverse(p_hat), width=width)
        result.append({
            "ordinal": ordinal,
            "block": block,
            "physical_position": FACTOR_ORDER[block].index(ordinal) + 1,
            "registered_position": REGISTERED_POSITIONS[index],
            "occurrence": item["occurrence"],
            "type": item["type"],
            "context_id": int(item["context_id"]),
            "registry_label": "C" + str(int(item["context_id"])),
            "repeated_e3_key": "E3_xy" if ordinal in (1, 5) else None,
            "rank": 3 if block in ("H1", "H2") else 4,
            "ten_index": int(item["ten_index"]),
            "role": item["role"],
            "sigma": int(item["factor_sign"]),
            "inverse_slot": int(item["factor_sign"]) == -1,
            "orientation": item["orientation"],
            "rho": {"x": list(runtime.contexts[int(item["ten_index"])]["left"]),
                    "y": list(runtime.contexts[int(item["ten_index"])]["right"])},
            "old_prefix_ordinals": list(prefix_ordinals),
            "g_o": list(g_values[index]),
            "a_o": list(a_values[index]),
            "corrected_o": list(f_values[index]),
            "old_prefix_word": list(old_prefix),
            "p_hat_word": list(p_hat),
            "applied_signed_word": list(applied),
            "d_word": list(d_word),
        })
    return result


def attach_coordinate(record: dict[str, Any], echelon: Sequence[dict[int, int]],
                      budget: Budget) -> dict[str, Any]:
    answer = dict(record)
    dimension = 3 if record["block"] in ("H1", "H2") else 6
    ell, tau = scan_word(record["d_word"], dimension, budget,
                         "OCCURRENCE_" + str(record["ordinal"]))
    reduced_tau = reduce_mod_relations(tau, echelon)
    answer["class_two"] = {
        "raw": {"ell": sparse_public(ell), "tau": sparse_public(tau)},
        "relation_reduced": {"ell": sparse_public(ell),
                             "tau": sparse_public(reduced_tau)},
    }
    return answer


def build_blocks(records: Sequence[dict[str, Any]], words: dict[str, Any],
                 echelons: dict[int, list[dict[int, int]]], budget: Budget
                 ) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    by_ordinal = {int(record["ordinal"]): record for record in records}
    blocks: dict[str, Any] = {}
    q2_triple = []
    relation_names = {"H1": "hexagon_1", "H2": "hexagon_2",
                      "P": "pentagon"}
    for block in BLOCKS:
        rank_dimension = 3 if block in ("H1", "H2") else 6
        echelon = echelons[rank_dimension]
        order = FACTOR_ORDER[block]
        factors = [by_ordinal[ordinal] for ordinal in order]
        old_signed = [tuple(item["g_o"]) if int(item["sigma"]) > 0
                      else inverse(item["g_o"]) for item in factors]
        corrected_signed = [tuple(item["corrected_o"])
                            if int(item["sigma"]) > 0
                            else inverse(item["corrected_o"])
                            for item in factors]
        old_relation = product(*old_signed, width=rank_dimension)
        corrected_relation = product(*corrected_signed, width=rank_dimension)
        expected_relation = tuple(words["relation_words"][block])
        need(corrected_relation == expected_relation,
             "task193:relation_word:" + block)
        ratio = product(corrected_relation, inverse(old_relation),
                        width=rank_dimension)
        ordered_d = product(*(item["d_word"] for item in factors),
                            width=rank_dimension)
        need(ordered_d == ratio, "v355:literal_ratio:" + block)

        sum_ell: dict[int, int] = {}
        q_raw: dict[int, int] = {}
        prior: list[dict[int, int]] = []
        for item in factors:
            raw = item["class_two"]["raw"]
            ell = sparse_parse(raw["ell"], rank_dimension,
                               "occurrence:ell")
            tau = sparse_parse(raw["tau"],
                               len(wedge_basis(rank_dimension)),
                               "occurrence:tau")
            q_raw = sparse_add(q_raw, tau)
            for earlier in prior:
                q_raw = sparse_add(q_raw,
                                   wedge(earlier, ell, rank_dimension), 2)
            prior.append(ell)
            sum_ell = sparse_add(sum_ell, ell)
        q_reduced = reduce_mod_relations(q_raw, echelon)
        ratio_ell, ratio_tau = scan_word(ratio, rank_dimension, budget,
                                         "RATIO_" + block)
        ratio_reduced = reduce_mod_relations(ratio_tau, echelon)
        need(ratio_ell == sum_ell and ratio_reduced == q_reduced,
             "v355:ratio_coordinate:" + block)
        tag = "PB3" if block in ("H1", "H2") else "PB4"
        blocks[block] = {
            "block": block,
            "relation_name": relation_names[block],
            "pb_owner": tag,
            "factor_order_ordinals": list(order),
            "factor_occurrences": [item["occurrence"] for item in factors],
            "old_relation_word": list(old_relation),
            "corrected_relation_word": list(corrected_relation),
            "ratio_word": list(ratio),
            "ordered_d_product_word": list(ordered_d),
            "literal_ratio_replay": True,
            "formula_coordinate": {
                "raw": {"ell": sparse_public(sum_ell),
                        "tau": sparse_public(q_raw)},
                "relation_reduced": {"ell": sparse_public(sum_ell),
                                     "tau": sparse_public(q_reduced)}},
            "ratio_scan_coordinate": {
                "raw": {"ell": sparse_public(ratio_ell),
                        "tau": sparse_public(ratio_tau)},
                "relation_reduced": {"ell": sparse_public(ratio_ell),
                                     "tau": sparse_public(ratio_reduced)}},
            "coordinate_replay": True,
            "q2": sparse_public(q_reduced),
        }
        q2_triple.append({"block": block, "pb_owner": tag,
                          "vector": sparse_public(q_reduced)})
    need(all(item["vector"] == [] for item in q2_triple),
         "v356:q2_nonzero_abi_mismatch")
    return blocks, q2_triple


def checkpoint_value(phase: str, binding: dict[str, Any] | None,
                     inputs: dict[str, Any] | None,
                     pb_owners: dict[str, Any],
                     occurrences: list[dict[str, Any]],
                     terminal_reason: str | None = None) -> dict[str, Any]:
    return seal({
        "schema": CHECKPOINT_SCHEMA,
        "mode": "PRODUCTION",
        "phase": phase,
        "source": source_identity(),
        "static_bindings": static_bindings(),
        "owner_binding": binding,
        "input_words": inputs,
        "global_factor_order_ordinals": list(GLOBAL_FACTOR_ORDER),
        "pb_owners": pb_owners,
        "occurrences": occurrences,
        "terminal_reason": terminal_reason,
        "resume_contract": {"all_or_none_path_bytes_sha256": True,
                            "sources_and_physical_owners_bound": True,
                            "pb_roster_then_occurrence_prefix": True},
    })


def load_resume(args: argparse.Namespace, binding: dict[str, Any],
                inputs: dict[str, Any]) -> dict[str, Any] | None:
    supplied = (args.resume_path is not None, args.resume_bytes is not None,
                args.resume_sha256 is not None)
    need(len(set(supplied)) == 1, "resume:all_or_none")
    if not supplied[0]:
        return None
    value, got = read_json(args.resume_path, "resume", "ci/in")
    need(got["bytes"] == int(args.resume_bytes) and
         got["sha256"] == args.resume_sha256, "resume:physical_identity")
    check_seal(value, "resume")
    need(value.get("schema") == CHECKPOINT_SCHEMA and
         value.get("mode") == "PRODUCTION" and
         value.get("source") == source_identity() and
         value.get("static_bindings") == static_bindings() and
         value.get("owner_binding") == binding and
         value.get("input_words") == inputs and
         value.get("global_factor_order_ordinals") == list(GLOBAL_FACTOR_ORDER),
         "resume:binding")
    need(type(value.get("pb_owners")) is dict and
         type(value.get("occurrences")) is list and
         len(value["occurrences"]) <= 11 and
         [item.get("ordinal") for item in value["occurrences"]] ==
         list(GLOBAL_FACTOR_ORDER[:len(value["occurrences"])]),
         "resume:prefix")
    pb_keys = set(value["pb_owners"])
    need(pb_keys in (set(), {"PB3"}, {"PB3", "PB4"}) and
         (not value["occurrences"] or pb_keys == {"PB3", "PB4"}),
         "resume:phase_prefix")
    return value


def compile_receipt(args: argparse.Namespace, budget: Budget,
                    state: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    state["static_bindings"] = restore_static_sources()
    task292 = load_pinned(TASK292_PIN, "r07_task292_v2_q2_producer")
    helper = load_task198()
    task193, task193_id = load_task193(args.task193_receipt,
                                      args.task193_verdict)
    words = task193_words(task193)
    budget.bump(sum(len(value) for key, value in words.items()
                    if key in ("g760", "correction_word", "corrected_word")),
                "TASK193_WORDS")
    try:
        task_meter = helper.Meter(helper_limits(helper, args))
        authority = helper.AuthorityAdapter(args, task_meter)
        runtime = helper.Runtime(authority, task_meter)
        task_meter.check("TASK379_TASK198_CONTEXTS")
    except helper.ResourceStop as exc:
        raise ResourceStop("phase=task198:cap=upstream:value=" + str(exc)) from exc
    except helper.InputStop as exc:
        raise InputStop("task198:" + str(exc)) from exc
    helper_charge(task_meter, budget, "TASK198_AUTHORITY")
    ledger = validate_layout(helper, authority)
    owners = {"task193_v3": task193_id, "task198": authority.identity}
    binding = {"source": source_identity(),
               "static_bindings": static_bindings(), "owners": owners}
    state.update({"owners": owners, "binding": binding, "inputs": words,
                  "pb_owners": {}, "occurrences": []})
    resume = load_resume(args, binding, words)
    if resume is not None:
        write_checkpoint(args.checkpoint, resume, args.checkpoint_bytes)

    pb_owners: dict[str, Any] = {}
    echelons: dict[int, list[dict[int, int]]] = {}
    for rank in (3, 4):
        owner, echelon = build_pb_owner(task292, rank, budget)
        tag = "PB" + str(rank)
        if resume is not None and tag in resume["pb_owners"]:
            need(resume["pb_owners"][tag] == owner,
                 "resume:pb_owner:" + tag)
        pb_owners[tag] = owner
        echelons[len(owner["generator_basis"])] = echelon
        state["pb_owners"] = pb_owners
        if resume is None or tag not in resume["pb_owners"]:
            write_checkpoint(args.checkpoint,
                             checkpoint_value(tag + "_ROSTER", binding, words,
                                              pb_owners, state["occurrences"]),
                             args.checkpoint_bytes)
        budget.check(tag + "_CHECKPOINT")

    base_records = occurrence_words(task292, runtime, ledger, words, budget)
    by_ordinal = {record["ordinal"]: record for record in base_records}
    restored = [] if resume is None else resume["occurrences"]
    occurrences: list[dict[str, Any]] = []
    for index, ordinal in enumerate(GLOBAL_FACTOR_ORDER):
        rank_dimension = 3 if by_ordinal[ordinal]["block"] in ("H1", "H2") else 6
        record = attach_coordinate(by_ordinal[ordinal],
                                   echelons[rank_dimension], budget)
        if index < len(restored):
            need(restored[index] == record,
                 "resume:occurrence:" + str(ordinal))
        occurrences.append(record)
        state["occurrences"] = occurrences
        if index >= len(restored):
            write_checkpoint(args.checkpoint,
                             checkpoint_value("OCCURRENCE_" + str(index + 1),
                                              binding, words, pb_owners,
                                              occurrences),
                             args.checkpoint_bytes)
        budget.check("OCCURRENCE_" + str(index + 1) + "_CHECKPOINT")

    blocks, q2_triple = build_blocks(occurrences, words, echelons, budget)
    final_checkpoint = checkpoint_value("COMPLETE", binding, words,
                                        pb_owners, occurrences)
    checkpoint_id = write_checkpoint(args.checkpoint, final_checkpoint,
                                     args.checkpoint_bytes)
    receipt = seal({
        "schema": SCHEMA,
        "mode": "PRODUCTION",
        "status": "COMPLETE",
        "terminal": COMPLETE,
        "complete": True,
        "source": source_identity(),
        "static_bindings": static_bindings(),
        "owners": owners,
        "authenticated_input": words,
        "global_factor_order_ordinals": list(GLOBAL_FACTOR_ORDER),
        "occurrence_ledger": occurrences,
        "blocks": blocks,
        "pb_owners": pb_owners,
        "q2_triple": q2_triple,
        "v356_zero_canary": {
            "computed_after_eleven_factor_replay": True,
            "task193_exponent_zero_authenticated": True,
            "all_three_q2_zero": True,
            "hard_coded_zero": False,
            "nonzero_policy": "fail_closed_as_abi_mismatch"},
        "claims": {"q2_computed": True, "q2_return": "NONE",
                   "A9_completion": "NONE", "compatible_lift": "NONE",
                   "mixed_prime_perfect_core": "NONE", "fake": "NONE",
                   "Ihara": "NONE"},
        "checkpoint": checkpoint_id,
        "resource": {"task379": budget.snapshot(),
                     "task198": {"caps": task_meter.limits,
                                 "used": task_meter.counters}},
    })
    return receipt, checkpoint_id


def terminal_checkpoint(args: argparse.Namespace, state: dict[str, Any],
                        terminal: str, reason: str) -> dict[str, Any] | None:
    existing = output_path(args.checkpoint)
    if existing.exists():
        # A cap or late ABI failure must not destroy the last complete resume
        # boundary already written by this invocation.
        return identity(existing)
    value = checkpoint_value(terminal, state.get("binding"),
                             state.get("inputs"),
                             state.get("pb_owners", {}),
                             state.get("occurrences", []), reason)
    try:
        return write_checkpoint(args.checkpoint, value, args.checkpoint_bytes)
    except (InputStop, ResourceStop, OSError):
        minimal = checkpoint_value(terminal, state.get("binding"), None,
                                   {}, [], reason)
        try:
            return write_checkpoint(args.checkpoint, minimal,
                                    args.checkpoint_bytes)
        except (InputStop, ResourceStop, OSError):
            return None


def unknown_receipt(terminal: str, reason: str, state: dict[str, Any],
                    checkpoint: dict[str, Any] | None,
                    budget: Budget) -> dict[str, Any]:
    try:
        resource = budget.snapshot()
    except ResourceStop:
        resource = {"caps": {"seconds": budget.seconds,
                              "rss_bytes": budget.rss_bytes,
                              "operations": budget.operations},
                    "used": {"seconds": time.monotonic() - budget.started,
                             "rss_bytes": budget.peak_rss,
                             "operations": budget.used_operations},
                    "last_phase": budget.phase}
    return seal({
        "schema": SCHEMA, "mode": "PRODUCTION", "status": "UNKNOWN",
        "terminal": terminal, "complete": False, "reason": reason,
        "source": source_identity(),
        "static_bindings": state.get("static_bindings", static_bindings()),
        "owners": state.get("owners"), "checkpoint": checkpoint,
        "resource": resource,
        "claims": {"q2_computed": False, "q2_return": "NONE",
                   "A9_completion": "NONE", "compatible_lift": "NONE",
                   "mixed_prime_perfect_core": "NONE", "fake": "NONE",
                   "Ihara": "NONE"},
    })


def parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=("PRODUCTION",), required=True)
    ap.add_argument("--task193-receipt", required=True)
    ap.add_argument("--task193-verdict", required=True)
    for key, value in TASK198_DEFAULTS.items():
        ap.add_argument("--task198-" + key, dest="task198_" + key,
                        default=value)
    ap.add_argument("--output", default="ci/out/d972_r07_actual_a0_class_two_q2_v1.json")
    ap.add_argument("--checkpoint", default="ci/out/d972_r07_actual_a0_class_two_q2_v1.checkpoint.json")
    ap.add_argument("--seconds", type=int, default=14400)
    ap.add_argument("--rss-bytes", type=int, default=5000000000)
    ap.add_argument("--max-operations", type=int, default=2000000000)
    ap.add_argument("--checkpoint-bytes", type=int, default=200000000)
    ap.add_argument("--resume-path")
    ap.add_argument("--resume-bytes", type=int)
    ap.add_argument("--resume-sha256")
    return ap


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    if (args.seconds <= 0 or args.rss_bytes <= 0 or
            args.max_operations <= 0 or args.checkpoint_bytes < 65536):
        raise SystemExit("task379 invalid positive resource cap")
    output = output_path(args.output)
    checkpoint = output_path(args.checkpoint)
    if output == checkpoint or output.exists() or checkpoint.exists():
        raise SystemExit("task379 stale or aliased output")
    supplied = (args.resume_path is not None, args.resume_bytes is not None,
                args.resume_sha256 is not None)
    if len(set(supplied)) != 1:
        raise SystemExit("task379 resume path/bytes/SHA must be all-or-none")
    if supplied[0] and (type(args.resume_sha256) is not str or
                        len(args.resume_sha256) != 64):
        raise SystemExit("task379 bad resume SHA")
    budget = Budget(args.seconds, args.rss_bytes, args.max_operations)
    state: dict[str, Any] = {}
    try:
        result, _ = compile_receipt(args, budget, state)
        terminal = COMPLETE
    except ResourceStop as exc:
        reason = str(exc)
        reference = terminal_checkpoint(args, state, UNKNOWN_RESOURCE, reason)
        result = unknown_receipt(UNKNOWN_RESOURCE, reason, state, reference, budget)
        terminal = UNKNOWN_RESOURCE
    except (InputStop, OSError, ValueError, KeyError, TypeError) as exc:
        reason = str(exc)
        reference = terminal_checkpoint(args, state, UNKNOWN_INPUT, reason)
        result = unknown_receipt(UNKNOWN_INPUT, reason, state, reference, budget)
        terminal = UNKNOWN_INPUT
    write_exclusive(args.output, result)
    print(PRODUCER_LINE + " " + terminal, flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
