#!/usr/bin/env python3
"""Task377 production lift-null dovetail over the frozen v4 binder.

The only new branch is canonical endpoint NONZERO.  It streams the marked
Cayley graph of the complete ten-affine task198-v12 image, enumerates every
translated Schreier pair fairly, and keeps exact task292 endpoint ancestry.
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
import time
import types
from pathlib import Path
from typing import Any, Iterable, Sequence


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "d972-r07-direct-relator-a5-a7-fusion/v5"
LITERAL_SCHEMA = "d972-r07-actual-three-exact-pb-endpoints/v3/literal-input"
CHECKPOINT_SCHEMA = SCHEMA + "/checkpoint/v2"
SIDECAR_SCHEMA = SCHEMA + "/a5-sidecar/v2"
PRODUCER_LINE = "R07_DIRECT_RELATOR_A5_A7_FUSION_V5_PRODUCER_TERMINAL"
MEMBER = "R07_DIRECT_RELATOR_A5_A7_FUSION_MEMBER"
NONMEMBER = "R07_ZERO_BASE_A5_A6_NONMEMBER"
UNKNOWN_INPUT = "UNKNOWN_INPUT"
UNKNOWN_RESOURCE = "UNKNOWN_RESOURCE"
MODULUS = 3
LETTERS = (1, -1, 2, -2)
BLOCKS = ("H1", "H2", "P")

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


def reduced(word: Iterable[int]) -> tuple[int, ...]:
    out: list[int] = []
    for raw in word:
        letter = int(raw)
        need(letter in LETTERS, "word:letter")
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
    need(not path.is_absolute() and ".." not in path.parts and
         "." not in path.parts, "path:lexical:" + text)
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


def pin_value(pin: tuple[str, int, str]) -> dict[str, Any]:
    return {"path": pin[0], "bytes": pin[1], "sha256": pin[2]}


def check_pin(pin: tuple[str, int, str], label: str) -> dict[str, Any]:
    got = identity(inside(pin[0]))
    want = pin_value(pin)
    need(got == want, label + ":pin")
    return want


def load_pinned(pin: tuple[str, int, str], name: str) -> types.ModuleType:
    path = inside(pin[0])
    check_pin(pin, name)
    spec = importlib.util.spec_from_file_location(name, path)
    need(spec is not None and spec.loader is not None, name + ":loader")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def source_identity() -> dict[str, Any]:
    return identity(Path(__file__).resolve())


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


def check_all_pins() -> None:
    for label, pin in (
            ("v4:producer", V4_PIN), ("v4:checker", V4_CHECKER_PIN),
            ("a5:producer", BASE_PIN), ("a5:checker", BASE_CHECKER_PIN),
            ("task292:producer", TASK292_PIN),
            ("task292:checker", TASK292_CHECKER_PIN),
            ("task198:v12", TASK198_V12_PIN),
            ("task198:v14", TASK198_V14_PIN),
            ("task198:v6", TASK198_V6_PIN),
            ("task198:checker_v6", TASK198_CHECKER_V6_PIN),
            ("task193:producer", TASK193_PRODUCER_PIN),
            ("task193:checker", TASK193_CHECKER_PIN),
            ("task193:driver", TASK193_DRIVER_PIN)):
        check_pin(pin, label)


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
        raise InputStop(label + ":json") from exc
    need(type(value) is dict, label + ":object")
    return value, {"path": path.relative_to(ROOT).as_posix(),
                   "bytes": len(raw), "sha256": sha(raw)}


def check_seal(value: dict[str, Any], label: str) -> None:
    claimed = value.get("self_digest_sha256")
    body = dict(value)
    body.pop("self_digest_sha256", None)
    need(type(claimed) is str and claimed == digest(body), label + ":seal")


def output_path(raw: str) -> Path:
    path = Path(str(raw).replace("\\", "/"))
    need(not path.is_absolute() and ".." not in path.parts and
         "." not in path.parts, "output:lexical")
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


def affine_state_public(helper: Any, state: Any) -> dict[str, Any]:
    gradient = []
    for (component, element), raw in sorted(
            state.u.items(), key=lambda item:
            (int(item[0][0]), helper.element_blob(item[0][1]))):
        value = int(raw) % MODULUS
        if value:
            gradient.append([int(component), helper.element_blob(element).hex(), value])
    return {"roof": helper.element_blob(state.a).hex(), "gradient": gradient}


def state_public(helper: Any, states: Sequence[Any]) -> list[dict[str, Any]]:
    need(len(states) == 10, "rho1:ten_affine_states")
    return [affine_state_public(helper, state) for state in states]


def state_key(helper: Any, states: Sequence[Any]) -> bytes:
    return canon(state_public(helper, states))


def endpoint_vector(endpoint: dict[str, Any]) -> dict[str, int]:
    out: dict[str, int] = {}
    for block in BLOCKS:
        rows = endpoint.get("endpoints", {}).get(block, {}).get("buckets")
        need(type(rows) is list, "endpoint:buckets:" + block)
        for row in rows:
            key = canon([block, row.get("full_artin_key")]).decode("ascii")
            coefficient = int(row.get("coefficient_mod_3")) % MODULUS
            need(coefficient and key not in out, "endpoint:coordinate:" + block)
            out[key] = coefficient
    return out


def sparse_add(left: dict[str, int], right: dict[str, int], scale: int = 1
               ) -> dict[str, int]:
    out = dict(left)
    for key, raw in right.items():
        value = (out.get(key, 0) + int(scale) * int(raw)) % MODULUS
        if value:
            out[key] = value
        else:
            out.pop(key, None)
    return out


def sparse_scale(row: dict[str, int], factor: int) -> dict[str, int]:
    return {key: int(value) * int(factor) % MODULUS
            for key, value in row.items()
            if int(value) * int(factor) % MODULUS}


class SparseEchelon:
    def __init__(self, public: dict[str, Any] | None = None):
        self.pivots: list[str] = []
        self.rows: dict[str, dict[str, int]] = {}
        self.ancestry: dict[str, dict[str, int]] = {}
        if public is not None:
            need(type(public.get("pivots")) is list and
                 type(public.get("rows")) is dict and
                 type(public.get("ancestry")) is dict, "echelon:shape")
            self.pivots = [str(value) for value in public["pivots"]]
            need(self.pivots == sorted(set(self.pivots)), "echelon:pivots")
            self.rows = {str(p): {str(k): int(v) % MODULUS
                                  for k, v in public["rows"][str(p)].items()
                                  if int(v) % MODULUS}
                         for p in self.pivots}
            self.ancestry = {
                str(p): {str(k): int(v) % MODULUS
                         for k, v in public["ancestry"][str(p)].items()
                         if int(v) % MODULUS}
                for p in self.pivots}
            for pivot in self.pivots:
                need(self.rows[pivot].get(pivot) == 1 and
                     pivot == min(self.rows[pivot]), "echelon:normalized")

    def insert(self, row: dict[str, int], column: int) -> bool:
        remainder = {str(k): int(v) % MODULUS for k, v in row.items()
                     if int(v) % MODULUS}
        ancestry = {str(int(column)): 1}
        for pivot in self.pivots:
            factor = remainder.get(pivot, 0)
            if factor:
                remainder = sparse_add(remainder, self.rows[pivot], -factor)
                ancestry = sparse_add(ancestry, self.ancestry[pivot], -factor)
        if not remainder:
            return False
        pivot = min(remainder)
        factor = 1 if remainder[pivot] == 1 else 2
        remainder = sparse_scale(remainder, factor)
        ancestry = sparse_scale(ancestry, factor)
        self.pivots.append(pivot)
        self.pivots.sort()
        self.rows[pivot] = remainder
        self.ancestry[pivot] = ancestry
        return True

    def solve(self, target: dict[str, int]) -> dict[str, int] | None:
        remainder = {str(k): int(v) % MODULUS for k, v in target.items()
                     if int(v) % MODULUS}
        solution: dict[str, int] = {}
        for pivot in self.pivots:
            factor = remainder.get(pivot, 0)
            if factor:
                remainder = sparse_add(remainder, self.rows[pivot], -factor)
                solution = sparse_add(solution, self.ancestry[pivot], factor)
        return solution if not remainder else None

    def public(self) -> dict[str, Any]:
        return {"pivots": list(self.pivots),
                "rows": {p: self.rows[p] for p in self.pivots},
                "ancestry": {p: self.ancestry[p] for p in self.pivots}}


def process_rss_bytes() -> int:
    try:
        with open("/proc/self/statm", "r", encoding="ascii") as stream:
            resident = int(stream.read().split()[1])
        return resident * int(os.sysconf("SC_PAGE_SIZE"))
    except (OSError, ValueError, IndexError, AttributeError):
        pass
    try:
        import ctypes
        from ctypes import wintypes
        class Counters(ctypes.Structure):
            _fields_ = [("cb", wintypes.DWORD), ("PageFaultCount", wintypes.DWORD),
                        ("PeakWorkingSetSize", ctypes.c_size_t),
                        ("WorkingSetSize", ctypes.c_size_t),
                        ("QuotaPeakPagedPoolUsage", ctypes.c_size_t),
                        ("QuotaPagedPoolUsage", ctypes.c_size_t),
                        ("QuotaPeakNonPagedPoolUsage", ctypes.c_size_t),
                        ("QuotaNonPagedPoolUsage", ctypes.c_size_t),
                        ("PagefileUsage", ctypes.c_size_t),
                        ("PeakPagefileUsage", ctypes.c_size_t)]
        counters = Counters()
        counters.cb = ctypes.sizeof(Counters)
        ok = ctypes.windll.psapi.GetProcessMemoryInfo(
            ctypes.windll.kernel32.GetCurrentProcess(), ctypes.byref(counters),
            counters.cb)
        return int(counters.WorkingSetSize) if ok else 0
    except Exception:
        return 0


class Guard:
    def __init__(self, args: argparse.Namespace, started: float,
                 initial_operations: int):
        self.args = args
        self.started = float(started)
        self.initial_operations = int(initial_operations)
        self.operations = int(initial_operations)
        self.peak_rss = process_rss_bytes()

    def bump(self, amount: int, phase: str) -> None:
        self.operations += int(amount)
        if self.operations > int(self.args.max_operations):
            raise ResourceStop("phase=" + phase + ":cap=max_operations:value=" +
                               str(self.operations) + ":limit=" +
                               str(self.args.max_operations))

    def check(self, phase: str) -> None:
        elapsed = time.monotonic() - self.started
        if elapsed >= float(self.args.seconds) * 0.97:
            raise ResourceStop("phase=" + phase + ":cap=wall_seconds_soft:value=" +
                               format(elapsed, ".3f") + ":limit=" +
                               str(self.args.seconds))
        rss = process_rss_bytes()
        self.peak_rss = max(self.peak_rss, rss)
        if rss and rss >= int(self.args.rss_bytes) * 9 // 10:
            raise ResourceStop("phase=" + phase + ":cap=rss_bytes_soft:value=" +
                               str(rss) + ":limit=" + str(self.args.rss_bytes))

    def public(self) -> dict[str, Any]:
        return {"max_operations": int(self.args.max_operations),
                "operations_this_invocation": self.operations,
                "seconds_cap": int(self.args.seconds),
                "elapsed_seconds": time.monotonic() - self.started,
                "rss_bytes_cap": int(self.args.rss_bytes),
                "peak_process_rss_bytes": self.peak_rss,
                "soft_wall_fraction": 0.97, "soft_rss_fraction": 0.90}


class IncrementalEndpointCore:
    def __init__(self, task292: Any, canonical_literal: dict[str, Any]):
        for name in ("Budget", "ExactArtin", "aggregate_m", "build_occurrences",
                     "endpoint_terms_for_block", "collect_group_terms"):
            need(hasattr(task292, name), "task292:incremental_symbol:" + name)
        self.task292 = task292
        self.normalizer = task292.ExactArtin(task292.Budget())
        self.occurrences = task292.build_occurrences(
            canonical_literal, self.normalizer)

    def column(self, term: dict[str, Any]) -> tuple[dict[str, int], dict[str, Any]]:
        m = self.task292.aggregate_m([term])
        endpoints: dict[str, Any] = {}
        for block in BLOCKS:
            raw = self.task292.endpoint_terms_for_block(
                block, self.occurrences, m, [], self.normalizer)
            buckets, deletions = self.task292.collect_group_terms(raw)
            endpoints[block] = {"unreduced_terms": raw, "buckets": buckets,
                                "zero_deletions": deletions,
                                "zero": not buckets}
        public = {
            "M": m, "endpoints": endpoints,
            "endpoint_formula":
                "zero_epsilon-sum_o sigma_o P_o (rho_o(U)-rho_o(V)) xi_o",
            "incremental_formula_replay": True,
            "empty_epsilon_sources": {block: [] for block in BLOCKS},
        }
        return endpoint_vector(public), public


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


def initial_search(helper: Any, runtime: Any
                   ) -> tuple[dict[str, Any], dict[bytes, int], set[tuple[int, ...]]]:
    identity_states = runtime.states_direct(())
    public = state_public(helper, identity_states)
    key = canon(public)
    search = {
        "version": 1,
        "cayley_words": [[]],
        "cayley_edge_cursor": 0,
        "cayley_complete": False,
        "identity_state_key": public,
        "identity_state_key_sha256": sha(key),
        "seed_roster": [],
        "translations": [[]],
        "translation_parent_cursor": 0,
        "translation_letter_cursor": 0,
        "seed_translation_cursors": [],
        "seed_turn_cursor": 0,
        "echelon": SparseEchelon().public(),
        "basis_columns": [],
        "tested_columns": 0,
        "zero_columns": 0,
        "dependent_columns": 0,
        "rounds": 0,
        "operation_total": 10,
        "pending_solution": None,
        "schedule": schedule_contract(),
    }
    return search, {key: 0}, set()


def restore_search(helper: Any, runtime: Any, raw: dict[str, Any]
                   ) -> tuple[dict[str, Any], dict[bytes, int],
                              SparseEchelon, set[tuple[int, ...]]]:
    need(type(raw) is dict and raw.get("version") == 1 and
         raw.get("schedule") == schedule_contract(), "resume:search_envelope")
    words_raw = raw.get("cayley_words")
    need(type(words_raw) is list and words_raw, "resume:cayley_words")
    words = [list(reduced(word)) for word in words_raw]
    need(words[0] == [] and words == words_raw, "resume:cayley_reduced")
    by_key: dict[bytes, int] = {}
    for index, word in enumerate(words):
        key = state_key(helper, runtime.states_direct(word))
        need(key not in by_key, "resume:cayley_duplicate_state")
        by_key[key] = index
    identity_public = raw.get("identity_state_key")
    need(type(identity_public) is list and len(identity_public) == 10 and
         canon(identity_public) in by_key and by_key[canon(identity_public)] == 0 and
         sha(canon(identity_public)) == raw.get("identity_state_key_sha256"),
         "resume:identity_state")
    edge_cursor = int(raw.get("cayley_edge_cursor"))
    need(0 <= edge_cursor <= 4 * len(words), "resume:cayley_cursor")
    seeds = raw.get("seed_roster")
    need(type(seeds) is list, "resume:seeds")
    seen_seed: set[tuple[int, ...]] = set()
    for index, seed in enumerate(seeds):
        need(type(seed) is dict, "resume:seed:" + str(index))
        word = reduced(seed.get("word", ()))
        need(word and list(word) == seed.get("word") and word not in seen_seed,
             "resume:seed_word:" + str(index))
        seen_seed.add(word)
        need(seed.get("rho1_identity_state_sha256") ==
             raw.get("identity_state_key_sha256"), "resume:seed_identity")
    translations = raw.get("translations")
    need(type(translations) is list and translations and translations[0] == [],
         "resume:translations")
    for index, word in enumerate(translations):
        need(list(reduced(word)) == word, "resume:translation:" + str(index))
    parent = int(raw.get("translation_parent_cursor"))
    letter = int(raw.get("translation_letter_cursor"))
    need(0 <= parent < len(translations) and 0 <= letter < len(LETTERS),
         "resume:translation_cursor")
    cursors = raw.get("seed_translation_cursors")
    need(type(cursors) is list and len(cursors) == len(seeds) and
         all(type(value) is int and 0 <= value <= len(translations)
             for value in cursors), "resume:pair_cursors")
    turn = int(raw.get("seed_turn_cursor"))
    need((not seeds and turn == 0) or (seeds and 0 <= turn < len(seeds)),
         "resume:seed_turn")
    columns = raw.get("basis_columns")
    need(type(columns) is list, "resume:columns")
    for index, column in enumerate(columns):
        need(type(column) is dict and int(column.get("column_id")) == index and
             type(column.get("term")) is dict and
             int(column["term"].get("coefficient")) == 1,
             "resume:column:" + str(index))
    echelon = SparseEchelon(raw.get("echelon"))
    for ancestry in echelon.ancestry.values():
        need(all(0 <= int(key) < len(columns) for key in ancestry),
             "resume:echelon_ancestry")
    pending = raw.get("pending_solution")
    need(pending is None or (type(pending) is dict and
         all(0 <= int(key) < len(columns) and int(value) % MODULUS
             for key, value in pending.items())), "resume:pending_solution")
    search = raw
    search["cayley_words"] = words
    search["translations"] = [list(reduced(word)) for word in translations]
    search["echelon"] = echelon.public()
    return search, by_key, echelon, seen_seed


def next_translation(search: dict[str, Any]) -> None:
    translations = search["translations"]
    while True:
        parent = int(search["translation_parent_cursor"])
        letter_index = int(search["translation_letter_cursor"])
        need(0 <= parent < len(translations), "translation:parent")
        word = tuple(translations[parent])
        letter = LETTERS[letter_index]
        letter_index += 1
        if letter_index == len(LETTERS):
            search["translation_parent_cursor"] = parent + 1
            search["translation_letter_cursor"] = 0
        else:
            search["translation_letter_cursor"] = letter_index
        if word and word[-1] == -letter:
            continue
        translations.append(list(word + (letter,)))
        return


def explore_cayley_edge(search: dict[str, Any], by_key: dict[bytes, int],
                        seed_words: set[tuple[int, ...]],
                        helper: Any, runtime: Any) -> None:
    cursor = int(search["cayley_edge_cursor"])
    words = search["cayley_words"]
    if cursor >= 4 * len(words):
        search["cayley_complete"] = True
        return
    source_index, letter_index = divmod(cursor, len(LETTERS))
    need(source_index < len(words), "cayley:cursor")
    source_word = tuple(words[source_index])
    letter = LETTERS[letter_index]
    edge_word = product(source_word, (letter,))
    edge_key = state_key(helper, runtime.states_direct(edge_word))
    target_index = by_key.get(edge_key)
    if target_index is None:
        target_index = len(words)
        words.append(list(edge_word))
        by_key[edge_key] = target_index
    target_word = tuple(words[target_index])
    seed_word = product(source_word, (letter,), inverse(target_word))

    # This direct replay is deliberately before both identity and duplicate
    # suppression.  It is the executable rho1(n)=1 proof for every edge.
    seed_public = state_public(helper, runtime.states_direct(seed_word))
    identity_public = search["identity_state_key"]
    need(seed_public == identity_public, "cayley:schreier_rho1_identity")
    search["cayley_edge_cursor"] = cursor + 1
    if search["cayley_edge_cursor"] >= 4 * len(words):
        search["cayley_complete"] = True
    if not seed_word:
        return
    if seed_word in seed_words:
        return
    seed_words.add(seed_word)
    search["seed_roster"].append({
        "seed_index": len(search["seed_roster"]),
        "source_state_index": source_index,
        "source_word": list(source_word),
        "letter": letter,
        "target_state_index": target_index,
        "target_word": list(target_word),
        "word": list(seed_word),
        "rho1_identity_state_sha256":
            search["identity_state_key_sha256"],
        "rho1_n_equals_identity": True,
    })
    search["seed_translation_cursors"].append(0)


def lift_term(seed: dict[str, Any], translation: Sequence[int],
              coefficient: int = 1) -> dict[str, Any]:
    v_word = reduced(translation)
    n_word = reduced(seed["word"])
    u_word = product(v_word, n_word)
    need(u_word != v_word, "lift_pair:diagonal")
    return {
        "coefficient": int(coefficient) % MODULUS,
        "U": list(u_word),
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


def next_pair(search: dict[str, Any]
              ) -> tuple[int, int, dict[str, Any], list[int]] | None:
    seeds = search["seed_roster"]
    if not seeds:
        return None
    index = int(search["seed_turn_cursor"])
    need(0 <= index < len(seeds), "pair:seed_turn")
    search["seed_turn_cursor"] = (index + 1) % len(seeds)
    cursor = int(search["seed_translation_cursors"][index])
    if cursor >= len(search["translations"]):
        return None
    return index, cursor, seeds[index], search["translations"][cursor]


def selected_terms(search: dict[str, Any], solution: dict[str, int]
                   ) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    terms: list[dict[str, Any]] = []
    selected: list[dict[str, Any]] = []
    for raw_index in sorted(solution, key=lambda value: int(value)):
        index = int(raw_index)
        coefficient = int(solution[raw_index]) % MODULUS
        if not coefficient:
            continue
        column = search["basis_columns"][index]
        term = copy.deepcopy(column["term"])
        term["coefficient"] = coefficient
        terms.append(term)
        selected.append({
            "column_id": index,
            "coefficient": coefficient,
            "seed": copy.deepcopy(column["seed"]),
            "translating_word": list(column["translating_word"]),
            "positive_word": list(term["U"]),
            "negative_word": list(term["V"]),
            "endpoint_column_sha256": column["endpoint_column_sha256"],
            "endpoint_coordinate_count": column["endpoint_coordinate_count"],
            "M_term_digest_sha256": digest(term),
        })
    need(bool(terms), "solution:empty")
    return terms, selected


def final_literal(v4: Any, task292: Any, canonical_literal: dict[str, Any],
                  search: dict[str, Any], solution: dict[str, int]
                  ) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    terms, selected = selected_terms(search, solution)
    literal = copy.deepcopy(canonical_literal)
    lift_binding = {
        "theorem": "v351",
        "selected_sha256": digest(selected),
        "selected_count": len(selected),
        "rho1_owner": "task198-v12 Runtime.states_direct ten-affine",
        "endpoint_owner": "task292-v2 exact core",
    }
    literal["bindings"] = dict(literal["bindings"])
    literal["bindings"]["v351_lift_null"] = lift_binding
    literal["M_terms"] = list(literal["M_terms"]) + terms
    literal["M_immutable_digest_sha256"] = task292.aggregate_m(
        literal["M_terms"])["immutable_digest_sha256"]
    return literal, selected


def checkpoint_value(phase: str, owners: dict[str, Any] | None,
                     a5: dict[str, Any] | None,
                     canonical_literal_digest: str | None,
                     canonical_terminal: str | None,
                     canonical_endpoint: dict[str, Any] | None,
                     search: dict[str, Any] | None) -> dict[str, Any]:
    return seal({
        "schema": CHECKPOINT_SCHEMA,
        "mode": "PRODUCTION",
        "phase": phase,
        "source": source_identity(),
        "static_bindings": static_bindings(),
        "owners": owners,
        "a5_result": a5,
        "a5_digest_sha256": None if a5 is None else digest(a5),
        "canonical_literal_digest_sha256": canonical_literal_digest,
        "canonical_endpoint_terminal": canonical_terminal,
        "canonical_endpoint_digest_sha256": (
            None if canonical_endpoint is None else digest(canonical_endpoint)),
        "canonical_endpoint": canonical_endpoint,
        "search": search,
        "resume_contract": {
            "all_or_none_path_bytes_sha256": True,
            "source_owner_a5_canonical_bound": True,
            "affine_states_reconstructed_from_literal_words": True,
            "no_unauthenticated_python_objects": True,
            "fair_positive_dovetail": True,
        },
    })


def sidecar_value(owners: dict[str, Any], a5: dict[str, Any]) -> dict[str, Any]:
    return seal({
        "schema": SIDECAR_SCHEMA,
        "status": "ACCEPTED_A5_MEMBER",
        "terminal": "R07_ZERO_BASE_A5_A6_MEMBER",
        "source": source_identity(),
        "static_bindings": static_bindings(),
        "owners": owners,
        "a5_result": a5,
        "claims": {"A5": "MEMBER", "A6_M": True, "A7": "NONE",
                   "compatible_lift": "NONE", "fake": "NONE",
                   "Ihara": "NONE"},
    })


def resource_receipt(reason: str, owners: dict[str, Any] | None,
                     a5: dict[str, Any] | None,
                     canonical_literal: dict[str, Any] | None,
                     canonical_terminal: str | None,
                     canonical_endpoint: dict[str, Any] | None,
                     search: dict[str, Any] | None,
                     guard: Guard | None) -> dict[str, Any]:
    accepted = type(a5) is dict and a5.get("terminal_kind") == "MEMBER"
    result: dict[str, Any] = {
        "reason": reason,
        "a5": a5,
        "canonical_M_only": False,
        "v351_lift_null": "POSITIVE_DOVETAIL_INCOMPLETE",
        "bounded_miss_is_A7_negative": False,
        "search_progress": None if search is None else {
            "cayley_states": len(search["cayley_words"]),
            "cayley_edges": int(search["cayley_edge_cursor"]),
            "cayley_complete": bool(search["cayley_complete"]),
            "seeds": len(search["seed_roster"]),
            "translations": len(search["translations"]),
            "tested_columns": int(search["tested_columns"]),
            "endpoint_rank": len(search["echelon"]["pivots"]),
            "rounds": int(search["rounds"]),
            "schedule": schedule_contract(),
        },
        "resource": None if guard is None else guard.public(),
    }
    if accepted:
        result.update({
            "mu1": a5["mu1"],
            "M": None if canonical_endpoint is None else canonical_endpoint.get("M"),
            "canonical_endpoint": canonical_endpoint,
            "literal_binding": None if canonical_literal is None else {
                "schema": LITERAL_SCHEMA,
                "digest_sha256": digest(canonical_literal),
            },
        })
    terminal = UNKNOWN_RESOURCE + ":" + reason
    return seal({
        "schema": SCHEMA, "status": UNKNOWN_RESOURCE, "terminal": terminal,
        "mode": "PRODUCTION", "source": source_identity(),
        "static_bindings": static_bindings(), "owners": owners,
        "result": result,
        "claims": {"A5": "MEMBER" if accepted else "NONE",
                   "A6_M": accepted,
                   "A7": "UNKNOWN_RESOURCE" if accepted else "NONE",
                   "compatible_lift": "NONE", "fake": "NONE", "Ihara": "NONE"},
    })


def verify_selected_rho1(helper: Any, runtime: Any,
                         selected: list[dict[str, Any]],
                         identity_public: list[dict[str, Any]],
                         guard: Guard) -> None:
    for item in selected:
        seed = item["seed"]
        source = reduced(seed["source_word"])
        target = reduced(seed["target_word"])
        letter = int(seed["letter"])
        n_word = product(source, (letter,), inverse(target))
        need(list(n_word) == seed["word"], "selected:schreier_formula")
        need(state_public(helper, runtime.states_direct(n_word)) == identity_public,
             "selected:rho1_seed")
        u_word = reduced(item["positive_word"])
        v_word = reduced(item["negative_word"])
        need(u_word == product(v_word, n_word), "selected:translated_pair")
        need(state_key(helper, runtime.states_direct(u_word)) ==
             state_key(helper, runtime.states_direct(v_word)),
             "selected:lift_null")
        guard.bump(4, "selected_rho1_replay")


def run_dovetail(args: argparse.Namespace, v4: Any, task292: Any,
                  helper: Any, runtime: Any,
                  owners: dict[str, Any], a5: dict[str, Any],
                  canonical_literal: dict[str, Any],
                  canonical_terminal: str,
                  canonical_endpoint: dict[str, Any],
                  raw_search: dict[str, Any] | None,
    guard: Guard) -> tuple[str, dict[str, Any], dict[str, Any]]:
    if raw_search is None:
        search, by_key, seed_words = initial_search(helper, runtime)
        echelon = SparseEchelon()
    else:
        search, by_key, echelon, seed_words = restore_search(
            helper, runtime, raw_search)
    target = sparse_scale(endpoint_vector(canonical_endpoint), 2)
    need(bool(target), "dovetail:canonical_target_nonzero")
    def checkpoint(phase: str) -> dict[str, Any]:
        search["echelon"] = echelon.public()
        value = checkpoint_value(phase, owners, a5, digest(canonical_literal),
                                 canonical_terminal, canonical_endpoint, search)
        write_checkpoint(args.checkpoint, value, args.checkpoint_bytes)
        return value

    checkpoint("LIFT_NULL_DOVETAIL_RUNNING")
    core = IncrementalEndpointCore(task292, canonical_literal)
    while True:
        guard.check("lift_null_dovetail")
        solution = search.get("pending_solution")
        if solution is not None:
            literal, selected = final_literal(v4, task292, canonical_literal,
                                              search, solution)
            verify_selected_rho1(helper, runtime, selected,
                                 search["identity_state_key"], guard)
            guard.check("lift_null_final_exact_before")
            final_terminal, final_endpoint = v4.task292_compile(
                task292, literal, literal["bindings"])
            guard.check("lift_null_final_exact_after")
            need(final_terminal == task292.ZERO and
                 all(final_endpoint["endpoints"][block]["zero"]
                     for block in BLOCKS), "lift_null:final_direct_not_zero")
            certificate = {
                "theorem": "v351",
                "rho1_owner": "task198-v12 Runtime.states_direct",
                "state_key": "all ten affine roofs plus all ten sparse gradients",
                "selected": selected,
                "selected_sha256": digest(selected),
                "selected_count": len(selected),
                "canonical_endpoint_digest_sha256": digest(canonical_endpoint),
                "final_literal_digest_sha256": digest(literal),
                "final_M_digest_sha256":
                    final_endpoint["M"]["immutable_digest_sha256"],
                "final_direct_task292_zero": True,
                "schedule": schedule_contract(),
            }
            search["echelon"] = echelon.public()
            final_checkpoint = checkpoint_value(
                "LIFT_NULL_MEMBER_COMPLETE", owners, a5,
                digest(canonical_literal), canonical_terminal,
                canonical_endpoint, search)
            receipt = seal({
                "schema": SCHEMA, "status": "COMPLETE", "terminal": MEMBER,
                "mode": "PRODUCTION", "source": source_identity(),
                "static_bindings": static_bindings(), "owners": owners,
                "result": {
                    "terminal_kind": "MEMBER", "a5": a5,
                    "mu1": a5["mu1"], "M": final_endpoint["M"],
                    "canonical_endpoint": canonical_endpoint,
                    "literal_binding": {
                        "schema": LITERAL_SCHEMA,
                        "canonical_digest_sha256": digest(canonical_literal),
                        "digest_sha256": digest(literal),
                        "owner_replay": {
                            "v4_v352_literal_owner": True,
                            "incremental_task292_formula": True,
                            "selected_task198_rho1": True,
                            "final_direct_task292": True,
                        },
                    },
                    "endpoint_exact": final_endpoint,
                    "lift_null_certificate": certificate,
                    "canonical_M_only": False,
                    "v351_lift_null": "IMPLEMENTED_MEMBER",
                    "fixed_word_only": True,
                    "resource": guard.public(),
                },
                "claims": {"A5": "MEMBER", "A6_M": True, "A7": "ZERO",
                           "fixed_word_only": True,
                           "A8": "NONE", "A9": "NONE",
                           "compatible_lift": "NONE", "mixed_prime": "NONE",
                           "perfect_core": "NONE", "fake": "NONE",
                           "Ihara": "NONE"},
            })
            return MEMBER, receipt, final_checkpoint

        explore_cayley_edge(search, by_key, seed_words, helper, runtime)
        guard.bump(2, "cayley_edge")
        search["operation_total"] = int(search["operation_total"]) + 2
        next_translation(search)
        guard.bump(1, "translation_enumeration")
        search["operation_total"] = int(search["operation_total"]) + 1
        pair = next_pair(search)
        if pair is not None:
            seed_index, translation_index, seed, translation = pair
            term = lift_term(seed, translation)
            column, exact = core.column(term)
            guard.check("endpoint_column_complete")
            guard.bump(1 + len(column), "endpoint_column")
            search["seed_translation_cursors"][seed_index] = (
                translation_index + 1)
            search["operation_total"] = (int(search["operation_total"]) +
                                         1 + len(column))
            search["tested_columns"] = int(search["tested_columns"]) + 1
            if not column:
                search["zero_columns"] = int(search["zero_columns"]) + 1
            else:
                column_id = len(search["basis_columns"])
                inserted = echelon.insert(column, column_id)
                if inserted:
                    search["basis_columns"].append({
                        "column_id": column_id,
                        "seed": copy.deepcopy(seed),
                        "translating_word": list(translation),
                        "term": term,
                        "endpoint_column": column,
                        "endpoint_column_sha256": digest(column),
                        "endpoint_exact_sha256": digest(exact),
                        "endpoint_coordinate_count": len(column),
                        "incremental_formula_replay": True,
                        "empty_epsilon_sources": True,
                    })
                    solution = echelon.solve(target)
                    if solution is not None:
                        search["pending_solution"] = solution
                        search["echelon"] = echelon.public()
                        checkpoint("LIFT_NULL_FINAL_REPLAY_PENDING")
                else:
                    search["dependent_columns"] = int(
                        search["dependent_columns"]) + 1
            search["echelon"] = echelon.public()
        search["rounds"] = int(search["rounds"]) + 1
        if int(search["rounds"]) % int(args.cadence) == 0:
            search["echelon"] = echelon.public()
            checkpoint("LIFT_NULL_DOVETAIL_RUNNING")
            print("R07_LIFT_NULL_PROGRESS rounds=" + str(search["rounds"]) +
                  " states=" + str(len(search["cayley_words"])) +
                  " edges=" + str(search["cayley_edge_cursor"]) +
                  " seeds=" + str(len(search["seed_roster"])) +
                  " translations=" + str(len(search["translations"])) +
                  " columns=" + str(search["tested_columns"]) +
                  " rank=" + str(len(echelon.pivots)) +
                  " operations=" + str(guard.operations), flush=True)


def build(args: argparse.Namespace, resume: dict[str, Any] | None
          ) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any] | None]:
    check_all_pins()
    v4 = load_pinned(V4_PIN, "r07_fusion_v4_for_v5")
    base = load_pinned(BASE_PIN, "r07_a5_v3_for_fusion_v5")
    task292 = load_pinned(TASK292_PIN, "r07_task292_v2_for_fusion_v5")
    helper = base.load_task198()
    started = time.monotonic()
    owners: dict[str, Any] | None = None
    a5: dict[str, Any] | None = None
    canonical_literal: dict[str, Any] | None = None
    canonical_terminal: str | None = None
    canonical_endpoint: dict[str, Any] | None = None
    raw_search = None if resume is None else copy.deepcopy(resume.get("search"))
    sidecar_id: dict[str, Any] | None = None
    guard: Guard | None = None
    try:
        limits = dict(helper.CAPS)
        limits["wall_seconds"] = int(args.seconds)
        limits["rss_bytes"] = int(args.rss_bytes)
        meter = helper.Meter(limits)
        started = meter.started
        authority = helper.AuthorityAdapter(args, meter)
        runtime = helper.Runtime(authority, meter)
        boundary = helper.BoundaryLedger(runtime, meter)
        task193, task193_id, _task193_verdict = base.load_task193(
            args.task193_receipt, args.task193_verdict)
        owners = {"task198": authority.identity, "task193_v3": task193_id}
        budget = base.Budget(args.max_operations)
        engine = base.DirectEngine(helper, authority, runtime, boundary,
                                   task193, budget)
        if resume is None:
            a5 = engine.run()
        else:
            need(resume.get("owners") == owners, "resume:owner_binding")
            a5 = resume.get("a5_result")
            need(type(a5) is dict and a5.get("terminal_kind") == "MEMBER" and
                 resume.get("a5_digest_sha256") == digest(a5),
                 "resume:a5_member_binding")
        guard = Guard(args, started, budget.count)

        if a5.get("terminal_kind") == "NONMEMBER":
            checkpoint = checkpoint_value("A5_NONMEMBER_COMPLETE", owners, a5,
                                          None, None, None, None)
            receipt = seal({
                "schema": SCHEMA, "status": "COMPLETE", "terminal": NONMEMBER,
                "mode": "PRODUCTION", "source": source_identity(),
                "static_bindings": static_bindings(), "owners": owners,
                "result": {"a5": a5, "canonical_M_only": True,
                           "v351_lift_null": "NOT_REACHED"},
                "claims": {"A5": "NONMEMBER", "A6_M": False, "A7": "NONE",
                           "compatible_lift": "NONE", "fake": "NONE",
                           "Ihara": "NONE"},
            })
            return receipt, checkpoint, None

        need(a5.get("terminal_kind") == "MEMBER", "a5:terminal_kind")
        sidecar_id = write_exclusive(args.a5_sidecar,
                                     sidecar_value(owners, a5))
        bindings = {
            "task198": authority.identity,
            "task193_v3": task193_id,
            "a5_v3_in_process": {
                "source": pin_value(BASE_PIN),
                "result_digest_sha256": digest(a5),
            },
        }
        canonical_literal, owner_replay = v4.literal_owner(
            base, helper, runtime, authority, task193, a5["M"]["pairs"],
            bindings, task292)
        canonical_digest = digest(canonical_literal)
        if resume is None:
            canonical_terminal, canonical_endpoint = v4.task292_compile(
                task292, canonical_literal, bindings)
        else:
            need(resume.get("canonical_literal_digest_sha256") ==
                 canonical_digest, "resume:canonical_literal")
            canonical_terminal = resume.get("canonical_endpoint_terminal")
            canonical_endpoint = resume.get("canonical_endpoint")
            need(type(canonical_terminal) is str and
                 type(canonical_endpoint) is dict and
                 resume.get("canonical_endpoint_digest_sha256") ==
                 digest(canonical_endpoint), "resume:canonical_endpoint")

        if canonical_terminal == task292.ZERO:
            need(all(canonical_endpoint["endpoints"][block]["zero"]
                     for block in BLOCKS), "endpoint:canonical_zero")
            checkpoint = checkpoint_value(
                "CANONICAL_ENDPOINT_ZERO_COMPLETE", owners, a5,
                canonical_digest, canonical_terminal, canonical_endpoint, None)
            receipt = seal({
                "schema": SCHEMA, "status": "COMPLETE", "terminal": MEMBER,
                "mode": "PRODUCTION", "source": source_identity(),
                "static_bindings": static_bindings(), "owners": owners,
                "result": {
                    "terminal_kind": "MEMBER", "a5": a5, "mu1": a5["mu1"],
                    "M": canonical_endpoint["M"],
                    "literal_binding": {"schema": LITERAL_SCHEMA,
                                         "digest_sha256": canonical_digest,
                                         "owner_replay": owner_replay},
                    "endpoint_exact": canonical_endpoint,
                    "canonical_M_only": True,
                    "v351_lift_null": "NOT_NEEDED",
                    "fixed_word_only": True,
                },
                "claims": {"A5": "MEMBER", "A6_M": True, "A7": "ZERO",
                           "fixed_word_only": True, "A8": "NONE", "A9": "NONE",
                           "compatible_lift": "NONE", "fake": "NONE",
                           "Ihara": "NONE"},
            })
            return receipt, checkpoint, sidecar_id

        need(canonical_terminal.startswith(task292.NONZERO),
             "endpoint:canonical_terminal")
        if resume is not None:
            need(resume.get("phase") in (
                "LIFT_NULL_DOVETAIL_RUNNING",
                "LIFT_NULL_FINAL_REPLAY_PENDING",
                "LIFT_NULL_RESOURCE"), "resume:phase")
        try:
            _terminal, receipt, checkpoint = run_dovetail(
                args, v4, task292, helper, runtime, owners, a5,
                canonical_literal, canonical_terminal, canonical_endpoint,
                raw_search, guard)
            return receipt, checkpoint, sidecar_id
        except (ResourceStop, helper.ResourceStop, base.ResourceStop,
                v4.ResourceStop, task292.ResourceStop) as exc:
            reason = str(exc)
            search = raw_search
            # run_dovetail mutates the supplied resume object in place.  A
            # fresh search is checkpointed before its first resource-bearing
            # loop, so the physical checkpoint remains the recovery owner.
            if search is None and output_path(args.checkpoint).exists():
                prior, _ = read_json(args.checkpoint, "live_checkpoint", "ci/out")
                check_seal(prior, "live_checkpoint")
                search = prior.get("search")
            checkpoint = checkpoint_value(
                "LIFT_NULL_RESOURCE", owners, a5, canonical_digest,
                canonical_terminal, canonical_endpoint, search)
            receipt = resource_receipt(
                reason, owners, a5, canonical_literal, canonical_terminal,
                canonical_endpoint, search, guard)
            return receipt, checkpoint, sidecar_id
    except (ResourceStop, helper.ResourceStop, base.ResourceStop,
            v4.ResourceStop, task292.ResourceStop) as exc:
        reason = str(exc)
        checkpoint = checkpoint_value("CONTROLLED_RESOURCE", owners, a5,
                                      None if canonical_literal is None else
                                      digest(canonical_literal),
                                      canonical_terminal, canonical_endpoint,
                                      raw_search)
        return (resource_receipt(reason, owners, a5, canonical_literal,
                                 canonical_terminal, canonical_endpoint,
                                 raw_search, guard), checkpoint, sidecar_id)
    except Exception:
        raise


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
    ap.add_argument("--cadence", type=int, default=64)
    ap.add_argument("--max-operations", type=int, default=2_000_000_000)
    ap.add_argument("--seconds", type=int, default=14_400)
    ap.add_argument("--rss-bytes", type=int, default=5_000_000_000)
    ap.add_argument("--checkpoint-bytes", type=int, default=2_000_000_000)
    for key, value in TASK198_DEFAULTS.items():
        ap.add_argument("--task198-" + key, dest="task198_" + key,
                        default=value)
    return ap


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    sidecar_id: dict[str, Any] | None = None
    try:
        need(args.cadence > 0 and args.max_operations > 0 and
             args.seconds > 0 and args.rss_bytes > 0 and
             args.checkpoint_bytes > 0, "arguments:positive_caps")
        resume = resume_load(args)
        receipt, checkpoint, sidecar_id = build(args, resume)
    except (InputStop, OSError, ValueError, TypeError, KeyError,
            AttributeError) as exc:
        checkpoint = checkpoint_value("INPUT_REJECTED", None, None, None,
                                      None, None, None)
        receipt = seal({
            "schema": SCHEMA, "status": UNKNOWN_INPUT,
            "terminal": UNKNOWN_INPUT + ":" + str(exc),
            "mode": "PRODUCTION", "source": source_identity(),
            "static_bindings": static_bindings(), "owners": None,
            "result": {"reason": str(exc)},
            "claims": {"A5": "NONE", "A6_M": False, "A7": "NONE",
                       "compatible_lift": "NONE", "fake": "NONE",
                       "Ihara": "NONE"},
        })
    except Exception as exc:
        checkpoint = checkpoint_value("INPUT_REJECTED", None, None, None,
                                      None, None, None)
        receipt = seal({
            "schema": SCHEMA, "status": UNKNOWN_INPUT,
            "terminal": UNKNOWN_INPUT + ":unexpected:" + str(exc),
            "mode": "PRODUCTION", "source": source_identity(),
            "static_bindings": static_bindings(), "owners": None,
            "result": {"reason": "unexpected:" + str(exc)},
            "claims": {"A5": "NONE", "A6_M": False, "A7": "NONE",
                       "compatible_lift": "NONE", "fake": "NONE",
                       "Ihara": "NONE"},
        })

    checkpoint_id = write_checkpoint(args.checkpoint, checkpoint,
                                     args.checkpoint_bytes)
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
