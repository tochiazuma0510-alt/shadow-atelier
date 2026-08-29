#!/usr/bin/env python3
"""Independent checker for task379 actual-A0 class-two q2 receipts.

The new producer is never imported.  This checker restores task198-v14 and
the checker-side task292 presentation, rebuilds all eleven literal factors,
and compares sparse mathematical coordinates in independently constructed
PB3/PB4 class-two quotients.
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
SCHEMA = "d972-r07-actual-a0-class-two-q2/v2"
CHECK_SCHEMA = SCHEMA + "/checker-verdict/v2"
CHECKPOINT_SCHEMA = SCHEMA + "/checkpoint/v2"
COMPLETE = "R07_ACTUAL_A0_CLASS_TWO_Q2_V2_COMPLETE"
UNKNOWN_RESOURCE = "UNKNOWN_RESOURCE"
REJECTED = "REJECTED"
CHECKER_LINE = "R07_ACTUAL_A0_CLASS_TWO_Q2_V2_CHECKER"
BLOCKS = ("H1", "H2", "P")
MODULUS = 3

PRODUCER_PIN = (
    "search/d972_r07_actual_a0_class_two_q2_v2.py", 50355,
    "125eb99d54764c546511741ac8eaefaa07c1fdaf2026117ee99fbfa4e6010627")
TASK193_SCHEMA = "d972-r07-second-frattini-affine-prefix-compiler/v4"
TASK193_TERMINAL = "R07_SECOND_FRATTINI_AFFINE_PREFIX_COMPILER_V4"
TASK193_CHECK_SCHEMA = TASK193_SCHEMA + "/checker-verdict/v4"
TASK193_PRODUCER_PIN = (
    "search/d972_r07_second_frattini_affine_prefix_compiler_v4.py", 2851,
    "a6e1d54c1c656ab496ed54e6bcac5fa8c027edc5686fa913c86cc1c0fe349d1a")
TASK193_CHECKER_PIN = (
    "crosscheck/check_d972_r07_second_frattini_affine_prefix_compiler_v4.py", 2986,
    "04f7c7df3395e841a21fe75fec71bd5fef1f35a4fbc4c0e642b5db7fa31e390d")
TASK193_DRIVER_PIN = (
    "search/d972_r07_second_frattini_affine_prefix_compiler_gha_driver_v4.g", 5798,
    "7447b2da4c83ba0f9818a3ea355636310368b22c8585e6b95632100894dfafb4")
TASK292_CHECKER_PIN = (
    "crosscheck/check_d972_r07_actual_three_exact_pb_endpoints_v2.py", 46873,
    "8d7598f376715af16ccec7bae5550f2c5329922b1b36326643a2a4e9e7cf72d8")
TASK292_PRODUCER_PIN = (
    "search/d972_r07_actual_three_exact_pb_endpoints_v2.py", 40044,
    "c44d2c8e7fdd7dcbf691600ba823445d1ac45695ef173043c723874a409f7208")
TASK198_WRAPPER_PIN = (
    "crosscheck/check_d972_r07_word_independent_successor_kernel_v14.py", 8074,
    "7ff0fb8888b46febb8b373914a3ba31ee555e43c829e60dae915bacfb16b7b47")
TASK198_V6_PIN = (
    "crosscheck/check_d972_r07_word_independent_successor_kernel_v6.py", 258847,
    "432bcaadfa1dcfd9526749c40fb3d56c1bdb5671a1959d571a8076c20ba29ccf")
TASK198_PRODUCER_WRAPPER_PIN = (
    "search/d972_r07_word_independent_successor_kernel_v12.py", 7209,
    "816bae92d86ac4bf3a6feb05297f505680072c2ce793db97135154cef928e9c5")
TASK198_PRODUCER_V6_PIN = (
    "search/d972_r07_word_independent_successor_kernel_v6.py", 219187,
    "aaa8a60960698eeeab0c300f7fb65bb902bbae7e5507e4bef933cdff26263a6a")

TASK198_DEFAULTS = {
    "receipt": "ci/in/d972_r07_seven_context_roof_presentation_v1.json",
    "manifest": "ci/in/d972_r07_seven_context_roof_presentation_v1.acceptance_v2.json",
    "producer": "ci/in/d972_r07_seven_context_roof_presentation_v1.producer.attestation.txt",
    "checker": "ci/in/d972_r07_seven_context_roof_presentation_v1.checker.attestation.txt",
    "verdict": "ci/in/d972_r07_seven_context_roof_presentation_v1.checker.verdict.json",
}

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


class Reject(RuntimeError):
    pass


class ResourceStop(RuntimeError):
    pass


def require(value: bool, message: str) -> None:
    if value is not True:
        raise Reject(message)


def packed(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def hexdigest(value: Any) -> str:
    return sha(packed(value))


def seal(value: dict[str, Any]) -> dict[str, Any]:
    answer = dict(value)
    answer.pop("self_digest_sha256", None)
    answer["self_digest_sha256"] = hexdigest(answer)
    return answer


def check_seal(value: dict[str, Any], label: str) -> None:
    claimed = value.get("self_digest_sha256", value.get("self_digest"))
    body = dict(value)
    body.pop("self_digest_sha256", None)
    body.pop("self_digest", None)
    require(type(claimed) is str and claimed == hexdigest(body), label + ":seal")


def inside(raw: str | Path, area: str | None = None,
           must_exist: bool = True) -> Path:
    text = str(raw).replace("\\", "/")
    path = Path(text)
    require(not path.is_absolute() and ".." not in path.parts and
            "." not in path.parts, "path:lexical:" + text)
    try:
        result = (ROOT / path).resolve(strict=must_exist)
        result.relative_to(ROOT.resolve())
        if area is not None:
            result.relative_to((ROOT / area).resolve(strict=True))
    except (OSError, ValueError) as exc:
        raise Reject("path:containment:" + text) from exc
    if must_exist:
        cursor = ROOT
        for part in path.parts:
            cursor /= part
            require(not stat.S_ISLNK(os.lstat(cursor).st_mode),
                    "path:symlink:" + text)
    return result


def identity(path: Path) -> dict[str, Any]:
    raw = path.read_bytes()
    return {"path": path.relative_to(ROOT).as_posix(),
            "bytes": len(raw), "sha256": sha(raw)}


def check_pin(pin: tuple[str, int, str], label: str) -> dict[str, Any]:
    got = identity(inside(pin[0]))
    wanted = {"path": pin[0], "bytes": pin[1], "sha256": pin[2]}
    require(got == wanted, label + ":pin")
    return wanted


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
        raise Reject(label + ":ascii_json") from exc
    require(type(value) is dict, label + ":object")
    return value, {"path": path.relative_to(ROOT).as_posix(),
                   "bytes": len(raw), "sha256": sha(raw)}


def output_path(raw: str) -> Path:
    path = Path(str(raw).replace("\\", "/"))
    require(not path.is_absolute() and ".." not in path.parts and
            "." not in path.parts, "output:lexical")
    result = (ROOT / path).resolve(strict=False)
    require(result.parent == (ROOT / "ci/out").resolve(strict=True),
            "output:containment")
    return result


def write_exclusive(raw_path: str, value: dict[str, Any]) -> dict[str, Any]:
    path = output_path(raw_path)
    require(not path.exists(), "output:stale:" + raw_path)
    raw = packed(value) + b"\n"
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


def source_identity() -> dict[str, Any]:
    return identity(Path(__file__).resolve())


def producer_static_bindings() -> dict[str, Any]:
    return {
        "task193_producer_v4": {"path": TASK193_PRODUCER_PIN[0],
                                 "bytes": TASK193_PRODUCER_PIN[1],
                                 "sha256": TASK193_PRODUCER_PIN[2]},
        "task193_checker_v4": {"path": TASK193_CHECKER_PIN[0],
                                "bytes": TASK193_CHECKER_PIN[1],
                                "sha256": TASK193_CHECKER_PIN[2]},
        "task193_driver_v4": {"path": TASK193_DRIVER_PIN[0],
                               "bytes": TASK193_DRIVER_PIN[1],
                               "sha256": TASK193_DRIVER_PIN[2]},
        "task292_producer_v2": {
            "path": TASK292_PRODUCER_PIN[0],
            "bytes": TASK292_PRODUCER_PIN[1],
            "sha256": TASK292_PRODUCER_PIN[2]},
        "task292_checker_v2": {
            "path": TASK292_CHECKER_PIN[0], "bytes": TASK292_CHECKER_PIN[1],
            "sha256": TASK292_CHECKER_PIN[2]},
        "task198_producer_v12": {
            "path": TASK198_PRODUCER_WRAPPER_PIN[0],
            "bytes": TASK198_PRODUCER_WRAPPER_PIN[1],
            "sha256": TASK198_PRODUCER_WRAPPER_PIN[2]},
        "task198_producer_v6": {
            "path": TASK198_PRODUCER_V6_PIN[0],
            "bytes": TASK198_PRODUCER_V6_PIN[1],
            "sha256": TASK198_PRODUCER_V6_PIN[2]},
        "task198_checker_v14": {
            "path": TASK198_WRAPPER_PIN[0], "bytes": TASK198_WRAPPER_PIN[1],
            "sha256": TASK198_WRAPPER_PIN[2]},
        "task198_checker_v6": {
            "path": TASK198_V6_PIN[0], "bytes": TASK198_V6_PIN[1],
            "sha256": TASK198_V6_PIN[2]},
    }


def checker_sources() -> dict[str, Any]:
    pins = {
        "producer": PRODUCER_PIN,
        "task193_producer_v4": TASK193_PRODUCER_PIN,
        "task193_checker_v4": TASK193_CHECKER_PIN,
        "task193_driver_v4": TASK193_DRIVER_PIN,
        "task292_producer_v2": TASK292_PRODUCER_PIN,
        "task292_checker_v2": TASK292_CHECKER_PIN,
        "task198_producer_v12": TASK198_PRODUCER_WRAPPER_PIN,
        "task198_producer_v6": TASK198_PRODUCER_V6_PIN,
        "task198_checker_v14": TASK198_WRAPPER_PIN,
        "task198_checker_v6": TASK198_V6_PIN,
    }
    return {label: check_pin(pin, label) for label, pin in pins.items()}


def load_pinned(pin: tuple[str, int, str], name: str) -> types.ModuleType:
    check_pin(pin, name)
    path = inside(pin[0])
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None, name + ":loader")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_task198() -> types.ModuleType:
    wrapper_path = inside(TASK198_WRAPPER_PIN[0])
    wrapper_raw = wrapper_path.read_bytes()
    require(len(wrapper_raw) == TASK198_WRAPPER_PIN[1] and
            sha(wrapper_raw) == TASK198_WRAPPER_PIN[2],
            "task198:v14_wrapper_pin")
    spec = importlib.util.spec_from_file_location("r07_task198_v14_q2_wrapper",
                                                  wrapper_path)
    require(spec is not None and spec.loader is not None,
            "task198:wrapper_loader")
    wrapper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(wrapper)
    source = Path(wrapper.SOURCE)
    raw = source.read_bytes()
    require(len(raw) == int(wrapper.SOURCE_BYTES) and
            sha(raw) == str(wrapper.SOURCE_SHA256) and
            identity(source) == {"path": TASK198_V6_PIN[0],
                                 "bytes": TASK198_V6_PIN[1],
                                 "sha256": TASK198_V6_PIN[2]},
            "task198:v6_checker_pin")
    for index, pair in enumerate(wrapper.PATCHES):
        require(type(pair) is tuple and len(pair) == 2,
                "task198:patch_shape:" + str(index))
        old, new = pair
        require(type(old) is bytes and type(new) is bytes and old and new and
                old != new and raw.count(old) == 1,
                "task198:patch_cardinality:" + str(index))
        raw = raw.replace(old, new)
    module = types.ModuleType("r07_task198_v14_q2_checker")
    module.__file__ = str(source)
    module.__package__ = None
    exec(compile(raw, str(source), "exec"), module.__dict__, module.__dict__)
    for name in ("Meter", "Authority", "CheckerArithmetic",
                 "CHECKER_BRIDGE_OWNER_LAYOUT"):
        require(hasattr(module, name), "task198:checker_symbol:" + name)
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

    def rss(self) -> int:
        try:
            return int(__import__("resource").getrusage(0).ru_maxrss) * 1024
        except Exception:
            return 0

    def check(self, phase: str) -> None:
        self.phase = phase
        elapsed = time.monotonic() - self.started
        self.peak_rss = max(self.peak_rss, self.rss())
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
    for key, kind in getattr(helper, "COUNTER_TYPES", {}).items():
        if kind in ("semantic", "validation"):
            limits[key] = min(int(limits[key]), int(args.max_operations))
    return limits


def helper_charge(meter: Any, budget: Budget, phase: str) -> None:
    amount = sum(int(value) for key, value in meter.counters.items()
                 if meter.counter_types.get(key) in ("semantic", "validation"))
    budget.bump(amount, phase)


def cancel_local(word: Iterable[int], width: int | None = None) -> tuple[int, ...]:
    result: list[int] = []
    for letter in word:
        require(type(letter) is int and letter != 0, "word:letter")
        if width is not None:
            require(abs(letter) <= width, "word:width")
        if result and result[-1] + letter == 0:
            result.pop()
        else:
            result.append(letter)
    return tuple(result)


def reverse_inverse_local(word: Sequence[int]) -> tuple[int, ...]:
    return tuple(-int(value) for value in tuple(word)[::-1])


def multiply(*words: Sequence[int], width: int | None = None) -> tuple[int, ...]:
    return cancel_local((letter for word in words for letter in word), width)


def exponent_sums(word: Sequence[int], width: int) -> list[int]:
    answer = [0] * width
    for letter in word:
        answer[abs(int(letter)) - 1] += 1 if int(letter) > 0 else -1
    return answer


def plus(left: dict[int, int], right: dict[int, int], scale: int = 1
         ) -> dict[int, int]:
    answer = dict(left)
    for key, value in right.items():
        updated = (answer.get(int(key), 0) + int(scale) * int(value)) % MODULUS
        if updated:
            answer[int(key)] = updated
        else:
            answer.pop(int(key), None)
    return answer


def scale(row: dict[int, int], coefficient: int) -> dict[int, int]:
    return {int(key): int(value) * int(coefficient) % MODULUS
            for key, value in row.items()
            if int(value) * int(coefficient) % MODULUS}


def public(row: dict[int, int]) -> list[list[int]]:
    return [[key, row[key] % MODULUS] for key in sorted(row)
            if row[key] % MODULUS]


def parse_sparse(raw: Any, columns: int, label: str) -> dict[int, int]:
    require(type(raw) is list, label + ":list")
    answer: dict[int, int] = {}
    previous = 0
    for item in raw:
        require(type(item) is list and len(item) == 2 and
                type(item[0]) is int and type(item[1]) is int,
                label + ":entry")
        column, value = item
        require(previous < column <= columns and value in (1, 2),
                label + ":canonical")
        answer[column] = value
        previous = column
    return answer


def exterior_pairs(dimension: int) -> list[tuple[int, int]]:
    return [(a, b) for a in range(1, dimension + 1)
            for b in range(a + 1, dimension + 1)]


def exterior(left: dict[int, int], right: dict[int, int], dimension: int
             ) -> dict[int, int]:
    answer: dict[int, int] = {}
    for number, (a, b) in enumerate(exterior_pairs(dimension), 1):
        coefficient = (left.get(a, 0) * right.get(b, 0) -
                       left.get(b, 0) * right.get(a, 0)) % MODULUS
        if coefficient:
            answer[number] = coefficient
    return answer


def collect(word: Sequence[int], dimension: int, budget: Budget,
            phase: str) -> tuple[dict[int, int], dict[int, int]]:
    degree_one: dict[int, int] = {}
    degree_two: dict[int, int] = {}
    for letter in word:
        generator = abs(int(letter))
        require(1 <= generator <= dimension, phase + ":letter")
        atom = {generator: 1 if int(letter) > 0 else 2}
        degree_two = plus(degree_two,
                          exterior(degree_one, atom, dimension), 2)
        degree_one = plus(degree_one, atom)
        budget.bump(1 + len(degree_one) + len(degree_two), phase)
    return degree_one, degree_two


def gaussian(rows: Sequence[dict[int, int]], columns: int
             ) -> list[dict[int, int]]:
    matrix = [{key: value % MODULUS for key, value in row.items()
               if value % MODULUS} for row in rows]
    matrix = [row for row in matrix if row]
    row_index = 0
    for column in range(1, columns + 1):
        chosen = None
        for index in range(row_index, len(matrix)):
            if matrix[index].get(column, 0):
                chosen = index
                break
        if chosen is None:
            continue
        matrix[row_index], matrix[chosen] = matrix[chosen], matrix[row_index]
        pivot_value = matrix[row_index][column]
        matrix[row_index] = scale(matrix[row_index],
                                  1 if pivot_value == 1 else 2)
        for index in range(len(matrix)):
            if index == row_index:
                continue
            coefficient = matrix[index].get(column, 0)
            if coefficient:
                matrix[index] = plus(matrix[index], matrix[row_index],
                                     -coefficient)
        row_index += 1
        if row_index == len(matrix):
            break
    return matrix[:row_index]


def quotient_reduce(row: dict[int, int], rows: Sequence[dict[int, int]]
                    ) -> dict[int, int]:
    answer = dict(row)
    for relation in rows:
        pivot = min(relation)
        coefficient = answer.get(pivot, 0)
        if coefficient:
            answer = plus(answer, relation, -coefficient)
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
    require(receipt.get("schema") == TASK193_SCHEMA and
            receipt.get("status") == "PASS" and
            receipt.get("terminal") == TASK193_TERMINAL,
            "task193:not_member")
    require(verdict.get("schema") == TASK193_CHECK_SCHEMA and
            verdict.get("status") == "PASS" and
            verdict.get("terminal") == TASK193_TERMINAL,
            "task193:checker_not_accepted")
    bound = verdict.get("receipt", {})
    require(bound.get("bytes") == receipt_id["bytes"] and
            bound.get("sha256") == receipt_id["sha256"],
            "task193:verdict_binding")
    claims = verdict.get("claims", {})
    require(claims.get("independent_task193_replay") is True and
            claims.get("pointed_rows") is True, "task193:checker_claims")
    frontier = receipt.get("claims", {})
    require(frontier.get("lift") == "NONE" and frontier.get("fake") == "NONE" and
            frontier.get("Ihara") == "NONE", "task193:frontier")
    return receipt, {"receipt": receipt_id, "verdict": verdict_id,
                     "sources": sources,
                     "accepted_lane": "task193-v4-PASS-member"}


def authenticated_words(task193: dict[str, Any]) -> dict[str, Any]:
    g0 = cancel_local(task193.get("g760", ()), 2)
    correction = cancel_local(task193.get("correction_word", ()), 2)
    corrected = cancel_local(task193.get("corrected_word", ()), 2)
    require(type(task193.get("g760")) is list and len(g0) == 760 and
            list(g0) == task193["g760"], "task193:g760")
    require(type(task193.get("correction_word")) is list and
            list(correction) == task193["correction_word"],
            "task193:correction_word")
    require(type(task193.get("corrected_word")) is list and
            list(corrected) == task193["corrected_word"] and
            corrected == multiply(g0, correction, width=2),
            "task193:corrected_literal")
    require(task193.get("literal_binding") == list(correction),
            "task193:applied_word_binding")
    relation = task193.get("relation_words")
    require(type(relation) is dict and
            set(relation) == {"hexagon_1", "hexagon_2", "pentagon"},
            "task193:relation_words")
    h1 = cancel_local(relation["hexagon_1"], 3)
    h2 = cancel_local(relation["hexagon_2"], 3)
    pentagon = cancel_local(relation["pentagon"], 6)
    require(list(h1) == relation["hexagon_1"] and
            list(h2) == relation["hexagon_2"] and
            list(pentagon) == relation["pentagon"],
            "task193:relation_words_reduced")
    sums = {"g760": exponent_sums(g0, 2),
            "correction_word": exponent_sums(correction, 2),
            "corrected_word": exponent_sums(corrected, 2)}
    require(all(value == [0, 0] for value in sums.values()),
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
    require(tuple(helper.CHECKER_BRIDGE_OWNER_LAYOUT) == EXPECTED_LAYOUT,
            "task198:checker_layout_drift")
    ledger = authority.receipt.get("bridge", {}).get("occurrence_ledger")
    require(type(ledger) is list and len(ledger) == 11,
            "task198:ledger_cardinality")
    for index, (item, expected) in enumerate(zip(ledger, EXPECTED_LAYOUT), 1):
        actual = (item.get("block"), int(item.get("block_index")),
                  int(item.get("block_slot")), item.get("occurrence"),
                  item.get("type"), int(item.get("ten_index")),
                  int(item.get("context_id")), item.get("role"),
                  int(item.get("factor_sign")), item.get("orientation"),
                  tuple(item.get("fox_prefix_occurrences", ())))
        require(int(item.get("ordinal")) == index and actual == expected,
                "task198:ledger_row:" + str(index))
    for block in BLOCKS:
        for position, ordinal in enumerate(FACTOR_ORDER[block], 1):
            item = ledger[ordinal - 1]
            require(normalize_block(item["block"]) == block and
                    tuple(item["fox_prefix_occurrences"]) ==
                    tuple(FACTOR_ORDER[block][:position - 1]),
                    "task198:printed_prefix:" + block + ":" + str(position))
    return ledger


def build_pb(task292: Any, rank: int, budget: Budget
             ) -> tuple[dict[str, Any], list[dict[int, int]]]:
    pairs = task292.pure_pairs(rank)
    require(pairs == [[i, j] for i in range(1, rank)
                      for j in range(i + 1, rank + 1)],
            "task292:pair_order")
    dimension = len(pairs)
    wedges = exterior_pairs(dimension)
    relators = task292.presentation_relators(rank)
    require(len(relators) == (2 if rank == 3 else 11),
            "task292:relator_count")
    rows = []
    records = []
    for index, raw in enumerate(relators, 1):
        word = cancel_local(raw, dimension)
        require(list(word) == raw,
                "task292:relator_reduced:" + str(index))
        ell, tau = collect(word, dimension, budget,
                           "PB" + str(rank) + "_RELATOR_" + str(index))
        require(not ell, "task292:relator_degree_one:" + str(index))
        rows.append(tau)
        records.append({"index": index, "word": list(word),
                        "raw": {"ell": public(ell), "tau": public(tau)}})
    echelon = gaussian(rows, len(wedges))
    expected_dimension = 1 if rank == 3 else 4
    require(len(wedges) - len(echelon) == expected_dimension,
            "task292:class_two_dimension")
    for record, row in zip(records, rows):
        remainder = quotient_reduce(row, echelon)
        require(not remainder, "task292:relator_nonzero")
        record["relation_reduced"] = {"ell": [], "tau": public(remainder)}
        record["vanishes"] = True
    owner = {
        "tag": "PB" + str(rank), "rank": rank,
        "generator_basis": [{"index": index + 1, "pair": pair}
                            for index, pair in enumerate(pairs)],
        "wedge_basis": [{"index": index + 1, "generators": list(pair)}
                        for index, pair in enumerate(wedges)],
        "relators": records,
        "initial_form_matrix": [public(row) for row in rows],
        "initial_form_echelon": [public(row) for row in echelon],
        "relation_rank": len(echelon),
        "quotient_dimension": expected_dimension,
        "all_full_relators_zero": True,
    }
    return owner, echelon


def compare_pb_owner(stored: Any, own: dict[str, Any],
                     own_echelon: Sequence[dict[int, int]], label: str) -> None:
    require(type(stored) is dict, label + ":object")
    for key in ("tag", "rank", "generator_basis", "wedge_basis",
                "relators", "initial_form_matrix", "relation_rank",
                "quotient_dimension", "all_full_relators_zero"):
        require(stored.get(key) == own.get(key), label + ":" + key)
    columns = len(own["wedge_basis"])
    stored_rows = [parse_sparse(row, columns, label + ":echelon")
                   for row in stored.get("initial_form_echelon", [])]
    stored_echelon = gaussian(stored_rows, columns)
    require(len(stored_echelon) == len(own_echelon), label + ":rank")
    for row in stored_echelon:
        require(not quotient_reduce(row, own_echelon),
                label + ":stored_span")
    for row in own_echelon:
        require(not quotient_reduce(row, stored_echelon),
                label + ":checker_span")


def reconstruct_occurrences(task292: Any, arithmetic: Any,
                            ledger: list[dict[str, Any]],
                            words: dict[str, Any], budget: Budget
                            ) -> list[dict[str, Any]]:
    contexts = arithmetic.contexts
    require(type(contexts) is list and len(contexts) == 10,
            "task198:checker_contexts")
    g_values = []
    a_values = []
    f_values = []
    for index, item in enumerate(ledger):
        context = contexts[int(item["ten_index"])]
        require((context.get("type"), int(context.get("id"))) ==
                (item.get("type"), int(item.get("context_id"))),
                "task198:context_owner:" + str(index + 1))
        width = 3 if item["type"] == "E3" else 6
        images = [list(context["left"]), list(context["right"])]
        g = tuple(task292.replace_letters(words["g760"], images, width))
        a = tuple(task292.replace_letters(words["correction_word"], images, width))
        f = tuple(task292.replace_letters(words["corrected_word"], images, width))
        require(f == multiply(g, a, width=width),
                "task193:substitution_right_correction:" + str(index + 1))
        g_values.append(g)
        a_values.append(a)
        f_values.append(f)
        budget.bump(len(g) + len(a) + len(f), "OCCURRENCE_SUBSTITUTION")
    signed_g = [g_values[index] if int(item["factor_sign"]) > 0
                else reverse_inverse_local(g_values[index])
                for index, item in enumerate(ledger)]
    records = []
    for index, item in enumerate(ledger):
        ordinal = index + 1
        block = normalize_block(item["block"])
        width = 3 if block in ("H1", "H2") else 6
        prefix_ordinals = tuple(int(value)
                                for value in item["fox_prefix_occurrences"])
        old_prefix = multiply(*(signed_g[value - 1]
                                for value in prefix_ordinals), width=width)
        p_hat = (multiply(old_prefix, g_values[index], width=width)
                 if int(item["factor_sign"]) > 0 else old_prefix)
        applied = (a_values[index] if int(item["factor_sign"]) > 0
                   else reverse_inverse_local(a_values[index]))
        factor = multiply(p_hat, applied, reverse_inverse_local(p_hat),
                          width=width)
        records.append({
            "ordinal": ordinal, "block": block,
            "physical_position": FACTOR_ORDER[block].index(ordinal) + 1,
            "registered_position": REGISTERED_POSITIONS[index],
            "occurrence": item["occurrence"], "type": item["type"],
            "context_id": int(item["context_id"]),
            "registry_label": "C" + str(int(item["context_id"])),
            "repeated_e3_key": "E3_xy" if ordinal in (1, 5) else None,
            "rank": 3 if block in ("H1", "H2") else 4,
            "ten_index": int(item["ten_index"]), "role": item["role"],
            "sigma": int(item["factor_sign"]),
            "inverse_slot": int(item["factor_sign"]) == -1,
            "orientation": item["orientation"],
            "rho": {"x": list(contexts[int(item["ten_index"])]["left"]),
                    "y": list(contexts[int(item["ten_index"])]["right"])},
            "old_prefix_ordinals": list(prefix_ordinals),
            "g_o": list(g_values[index]), "a_o": list(a_values[index]),
            "corrected_o": list(f_values[index]),
            "old_prefix_word": list(old_prefix), "p_hat_word": list(p_hat),
            "applied_signed_word": list(applied), "d_word": list(factor),
        })
    return records


def attach_coordinate(record: dict[str, Any], echelon: Sequence[dict[int, int]],
                      budget: Budget) -> dict[str, Any]:
    answer = dict(record)
    dimension = 3 if record["block"] in ("H1", "H2") else 6
    ell, tau = collect(record["d_word"], dimension, budget,
                       "OCCURRENCE_" + str(record["ordinal"]))
    answer["class_two"] = {
        "raw": {"ell": public(ell), "tau": public(tau)},
        "relation_reduced": {"ell": public(ell),
                             "tau": public(quotient_reduce(tau, echelon))},
    }
    return answer


def compare_coordinate(stored: Any, own: dict[str, Any], dimension: int,
                       echelon: Sequence[dict[int, int]], label: str) -> None:
    require(type(stored) is dict, label + ":object")
    columns = len(exterior_pairs(dimension))
    for stage in ("raw", "relation_reduced"):
        require(type(stored.get(stage)) is dict, label + ":" + stage)
        stored_ell = parse_sparse(stored[stage].get("ell"), dimension,
                                  label + ":ell")
        own_ell = parse_sparse(own[stage]["ell"], dimension,
                               label + ":own_ell")
        require(stored_ell == own_ell, label + ":ell_value")
        stored_tau = parse_sparse(stored[stage].get("tau"), columns,
                                  label + ":tau")
        own_tau = parse_sparse(own[stage]["tau"], columns,
                               label + ":own_tau")
        if stage == "raw":
            require(stored_tau == own_tau, label + ":raw_tau")
        else:
            require(not quotient_reduce(plus(stored_tau, own_tau, -1), echelon),
                    label + ":quotient_tau")


def compare_occurrence(stored: Any, own: dict[str, Any],
                       echelon: Sequence[dict[int, int]], label: str) -> None:
    require(type(stored) is dict, label + ":object")
    for key, value in own.items():
        if key != "class_two":
            require(stored.get(key) == value, label + ":" + key)
    dimension = 3 if own["block"] in ("H1", "H2") else 6
    compare_coordinate(stored.get("class_two"), own["class_two"],
                       dimension, echelon, label + ":coordinate")


def reconstruct_blocks(records: Sequence[dict[str, Any]], words: dict[str, Any],
                       echelons: dict[int, list[dict[int, int]]],
                       budget: Budget
                       ) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    by_ordinal = {record["ordinal"]: record for record in records}
    answer = {}
    triple = []
    names = {"H1": "hexagon_1", "H2": "hexagon_2", "P": "pentagon"}
    for block in BLOCKS:
        dimension = 3 if block in ("H1", "H2") else 6
        echelon = echelons[dimension]
        order = FACTOR_ORDER[block]
        factors = [by_ordinal[ordinal] for ordinal in order]
        old_signed = [tuple(item["g_o"]) if item["sigma"] > 0
                      else reverse_inverse_local(item["g_o"])
                      for item in factors]
        new_signed = [tuple(item["corrected_o"]) if item["sigma"] > 0
                      else reverse_inverse_local(item["corrected_o"])
                      for item in factors]
        old_relation = multiply(*old_signed, width=dimension)
        new_relation = multiply(*new_signed, width=dimension)
        require(new_relation == tuple(words["relation_words"][block]),
                "task193:relation_word:" + block)
        ratio = multiply(new_relation, reverse_inverse_local(old_relation),
                         width=dimension)
        factor_product = multiply(*(item["d_word"] for item in factors),
                                  width=dimension)
        require(ratio == factor_product, "v355:literal_ratio:" + block)
        ell_sum: dict[int, int] = {}
        q_raw: dict[int, int] = {}
        previous = []
        for item in factors:
            raw = item["class_two"]["raw"]
            ell = parse_sparse(raw["ell"], dimension, "factor:ell")
            tau = parse_sparse(raw["tau"], len(exterior_pairs(dimension)),
                               "factor:tau")
            q_raw = plus(q_raw, tau)
            for earlier in previous:
                q_raw = plus(q_raw, exterior(earlier, ell, dimension), 2)
            previous.append(ell)
            ell_sum = plus(ell_sum, ell)
        q_reduced = quotient_reduce(q_raw, echelon)
        ratio_ell, ratio_tau = collect(ratio, dimension, budget,
                                       "RATIO_" + block)
        ratio_reduced = quotient_reduce(ratio_tau, echelon)
        require(ratio_ell == ell_sum and ratio_reduced == q_reduced,
                "v355:ratio_coordinate:" + block)
        tag = "PB3" if block in ("H1", "H2") else "PB4"
        answer[block] = {
            "block": block, "relation_name": names[block], "pb_owner": tag,
            "factor_order_ordinals": list(order),
            "factor_occurrences": [item["occurrence"] for item in factors],
            "old_relation_word": list(old_relation),
            "corrected_relation_word": list(new_relation),
            "ratio_word": list(ratio),
            "ordered_d_product_word": list(factor_product),
            "literal_ratio_replay": True,
            "formula_coordinate": {
                "raw": {"ell": public(ell_sum), "tau": public(q_raw)},
                "relation_reduced": {"ell": public(ell_sum),
                                     "tau": public(q_reduced)}},
            "ratio_scan_coordinate": {
                "raw": {"ell": public(ratio_ell), "tau": public(ratio_tau)},
                "relation_reduced": {"ell": public(ratio_ell),
                                     "tau": public(ratio_reduced)}},
            "coordinate_replay": True, "q2": public(q_reduced),
        }
        triple.append({"block": block, "pb_owner": tag,
                       "vector": public(q_reduced)})
    require(all(item["vector"] == [] for item in triple),
            "v356:q2_nonzero_abi_mismatch")
    return answer, triple


def compare_block(stored: Any, own: dict[str, Any], dimension: int,
                  echelon: Sequence[dict[int, int]], label: str) -> None:
    require(type(stored) is dict, label + ":object")
    for key in ("block", "relation_name", "pb_owner",
                "factor_order_ordinals", "factor_occurrences",
                "old_relation_word", "corrected_relation_word", "ratio_word",
                "ordered_d_product_word", "literal_ratio_replay",
                "coordinate_replay"):
        require(stored.get(key) == own.get(key), label + ":" + key)
    compare_coordinate(stored.get("formula_coordinate"),
                       own["formula_coordinate"], dimension, echelon,
                       label + ":formula")
    compare_coordinate(stored.get("ratio_scan_coordinate"),
                       own["ratio_scan_coordinate"], dimension, echelon,
                       label + ":ratio_scan")
    columns = len(exterior_pairs(dimension))
    stored_q2 = parse_sparse(stored.get("q2"), columns, label + ":q2")
    own_q2 = parse_sparse(own["q2"], columns, label + ":own_q2")
    require(not quotient_reduce(plus(stored_q2, own_q2, -1), echelon),
            label + ":q2_class")


def same_task198(producer: Any, checker: Any) -> bool:
    if type(producer) is not dict or type(checker) is not dict:
        return False
    if (producer.get("receipt_sha256") != checker.get("receipt_sha256") or
            producer.get("manifest_sha256") != checker.get("manifest_sha256")):
        return False
    left = producer.get("task198", {})
    right = checker.get("task198", {})
    if set(left) != set(right):
        return False
    if (producer.get("receipt_bytes") != left.get("receipt", {}).get("bytes") or
            left.get("receipt", {}).get("bytes") !=
            right.get("receipt", {}).get("bytes")):
        return False
    for key in left:
        if (left[key].get("bytes") != right[key].get("bytes") or
                left[key].get("sha256") != right[key].get("sha256") or
                Path(left[key].get("path", "")).name !=
                Path(right[key].get("path", "")).name):
            return False
    for section in ("task176", "task176_source_identities"):
        lsection = producer.get(section, {})
        rsection = checker.get(section, {})
        if set(lsection) != set(rsection):
            return False
        for key in lsection:
            if (lsection[key].get("bytes") != rsection[key].get("bytes") or
                    lsection[key].get("sha256") != rsection[key].get("sha256")):
                return False
    return True


def check_checkpoint(args: argparse.Namespace, receipt: dict[str, Any],
                     producer_id: dict[str, Any], owners: dict[str, Any],
                     words: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    checkpoint, checkpoint_id = read_json(args.checkpoint, "checkpoint", "ci/out")
    check_seal(checkpoint, "checkpoint")
    require(receipt.get("checkpoint") == checkpoint_id,
            "checkpoint:receipt_binding")
    expected_binding = {"source": producer_id,
                        "static_bindings": producer_static_bindings(),
                        "owners": owners}
    require(checkpoint.get("schema") == CHECKPOINT_SCHEMA and
            checkpoint.get("mode") == "PRODUCTION" and
            checkpoint.get("phase") == "COMPLETE" and
            checkpoint.get("source") == producer_id and
            checkpoint.get("static_bindings") == producer_static_bindings() and
            checkpoint.get("owner_binding") == expected_binding and
            checkpoint.get("input_words") == words and
            checkpoint.get("global_factor_order_ordinals") ==
            list(GLOBAL_FACTOR_ORDER) and
            checkpoint.get("pb_owners") == receipt.get("pb_owners") and
            checkpoint.get("occurrences") == receipt.get("occurrence_ledger"),
            "checkpoint:complete_replay")
    return checkpoint, checkpoint_id


def check_complete(args: argparse.Namespace, budget: Budget,
                   sources: dict[str, Any]) -> dict[str, Any]:
    producer_id = sources["producer"]
    task292 = load_pinned(TASK292_CHECKER_PIN, "r07_task292_v2_q2_checker")
    helper = load_task198()
    task193, task193_id = load_task193(args.task193_receipt,
                                      args.task193_verdict)
    words = authenticated_words(task193)
    try:
        task_meter = helper.Meter(helper_limits(helper, args))
        authority = helper.Authority(args, task_meter)
        arithmetic = helper.CheckerArithmetic(authority, task_meter)
        task_meter.check("TASK379_CHECKER_CONTEXTS")
    except helper.ResourceStop as exc:
        raise ResourceStop("phase=task198:cap=upstream:value=" + str(exc)) from exc
    except helper.Reject as exc:
        raise Reject("task198:" + str(exc)) from exc
    helper_charge(task_meter, budget, "TASK198_AUTHORITY")
    ledger = validate_layout(helper, authority)

    receipt, receipt_id = read_json(args.receipt, "producer_receipt", "ci/out")
    check_seal(receipt, "producer_receipt")
    require(receipt.get("schema") == SCHEMA and
            receipt.get("mode") == "PRODUCTION" and
            receipt.get("status") == "COMPLETE" and
            receipt.get("terminal") == COMPLETE and
            receipt.get("complete") is True and
            receipt.get("source") == producer_id and
            receipt.get("static_bindings") == producer_static_bindings(),
            "producer:envelope")
    claims = {"q2_computed": True, "q2_return": "NONE",
              "A9_completion": "NONE", "compatible_lift": "NONE",
              "mixed_prime_perfect_core": "NONE", "fake": "NONE",
              "Ihara": "NONE"}
    require(receipt.get("claims") == claims, "producer:claim_boundary")
    owners = receipt.get("owners")
    require(type(owners) is dict and owners.get("task193_v4") == task193_id and
            same_task198(owners.get("task198"), authority.identity),
            "producer:physical_owners")
    require(receipt.get("authenticated_input") == words and
            receipt.get("global_factor_order_ordinals") ==
            list(GLOBAL_FACTOR_ORDER), "producer:applied_word")

    own_pb = {}
    echelons = {}
    for rank in (3, 4):
        owner, echelon = build_pb(task292, rank, budget)
        tag = "PB" + str(rank)
        compare_pb_owner(receipt.get("pb_owners", {}).get(tag), owner,
                         echelon, "producer:" + tag)
        own_pb[tag] = owner
        echelons[len(owner["generator_basis"])] = echelon

    base_records = reconstruct_occurrences(task292, arithmetic, ledger, words,
                                           budget)
    by_ordinal = {record["ordinal"]: record for record in base_records}
    own_occurrences = []
    stored_occurrences = receipt.get("occurrence_ledger")
    require(type(stored_occurrences) is list and len(stored_occurrences) == 11 and
            [item.get("ordinal") for item in stored_occurrences] ==
            list(GLOBAL_FACTOR_ORDER), "producer:occurrence_order")
    for index, ordinal in enumerate(GLOBAL_FACTOR_ORDER):
        dimension = 3 if by_ordinal[ordinal]["block"] in ("H1", "H2") else 6
        own = attach_coordinate(by_ordinal[ordinal], echelons[dimension], budget)
        compare_occurrence(stored_occurrences[index], own,
                           echelons[dimension],
                           "producer:occurrence:" + str(ordinal))
        own_occurrences.append(own)

    own_blocks, own_triple = reconstruct_blocks(own_occurrences, words,
                                                echelons, budget)
    stored_blocks = receipt.get("blocks")
    require(type(stored_blocks) is dict and set(stored_blocks) == set(BLOCKS),
            "producer:blocks")
    for block in BLOCKS:
        dimension = 3 if block in ("H1", "H2") else 6
        compare_block(stored_blocks[block], own_blocks[block], dimension,
                      echelons[dimension], "producer:block:" + block)
    require(receipt.get("q2_triple") == own_triple and
            receipt.get("v356_zero_canary") == {
                "computed_after_eleven_factor_replay": True,
                "task193_exponent_zero_authenticated": True,
                "all_three_q2_zero": True,
                "hard_coded_zero": False,
                "nonzero_policy": "fail_closed_as_abi_mismatch"},
            "producer:v356_canary")
    checkpoint, checkpoint_id = check_checkpoint(args, receipt, producer_id,
                                                 owners, words)
    budget.check("CHECKER_COMPLETE")
    return seal({
        "schema": CHECK_SCHEMA, "status": "ACCEPTED", "terminal": COMPLETE,
        "accepted": True, "independent": True,
        "checker_source": source_identity(), "source_bindings": sources,
        "receipt": receipt_id, "checkpoint": checkpoint_id,
        "task193_v4": task193_id, "task198": authority.identity,
        "replay": {"physical_occurrences": 11,
                   "factor_order_ordinals": list(GLOBAL_FACTOR_ORDER),
                   "literal_ratio_blocks": list(BLOCKS),
                   "pb_relator_counts": {"PB3": 2, "PB4": 11},
                   "q2_triple": own_triple,
                   "v356_all_three_zero": True,
                   "producer_pivots_imported": False,
                   "producer_imported": False},
        "claims": claims,
        "resource": {"task379_checker": budget.snapshot(),
                     "task198_checker": {"caps": task_meter.limits,
                                         "used": task_meter.counters}},
    })


def parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=("PRODUCTION",), required=True)
    ap.add_argument("--task193-receipt", required=True)
    ap.add_argument("--task193-verdict", required=True)
    for key, value in TASK198_DEFAULTS.items():
        ap.add_argument("--task198-" + key, dest="task198_" + key,
                        default=value)
    ap.add_argument("--receipt", required=True)
    ap.add_argument("--checkpoint", required=True)
    ap.add_argument("--output", default="ci/out/d972_r07_actual_a0_class_two_q2_v2.checker.json")
    ap.add_argument("--seconds", type=int, default=14400)
    ap.add_argument("--rss-bytes", type=int, default=5000000000)
    ap.add_argument("--max-operations", type=int, default=2000000000)
    return ap


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    if args.seconds <= 0 or args.rss_bytes <= 0 or args.max_operations <= 0:
        raise SystemExit("task379 checker invalid positive resource cap")
    output = output_path(args.output)
    if output.exists():
        raise SystemExit("task379 checker stale output")
    budget = Budget(args.seconds, args.rss_bytes, args.max_operations)
    sources: dict[str, Any] = {}
    try:
        sources = checker_sources()
        result = check_complete(args, budget, sources)
        terminal = COMPLETE
    except ResourceStop as exc:
        terminal = UNKNOWN_RESOURCE
        result = seal({"schema": CHECK_SCHEMA, "status": "UNKNOWN",
                       "terminal": terminal, "accepted": False,
                       "independent": True, "reason": str(exc),
                       "checker_source": source_identity(),
                       "source_bindings": sources,
                       "claims": {"q2_computed": False,
                                  "q2_return": "NONE",
                                  "A9_completion": "NONE",
                                  "compatible_lift": "NONE",
                                  "mixed_prime_perfect_core": "NONE",
                                  "fake": "NONE", "Ihara": "NONE"}})
    except (Reject, OSError, ValueError, KeyError, TypeError) as exc:
        terminal = REJECTED
        result = seal({"schema": CHECK_SCHEMA, "status": "REJECTED",
                       "terminal": terminal, "accepted": False,
                       "independent": True, "reason": str(exc),
                       "checker_source": source_identity(),
                       "source_bindings": sources,
                       "claims": {"q2_computed": False,
                                  "q2_return": "NONE",
                                  "A9_completion": "NONE",
                                  "compatible_lift": "NONE",
                                  "mixed_prime_perfect_core": "NONE",
                                  "fake": "NONE", "Ihara": "NONE"}})
    write_exclusive(args.output, result)
    print(CHECKER_LINE + " terminal=" + terminal, flush=True)
    return 0 if terminal != REJECTED else 1


if __name__ == "__main__":
    raise SystemExit(main())
