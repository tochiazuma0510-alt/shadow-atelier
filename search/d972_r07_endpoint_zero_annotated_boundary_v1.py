#!/usr/bin/env python3
"""Task378 production compiler from a task377 endpoint ZERO to A8 chains.

The compiler uses complete Artin action tuples as PB equality keys, performs
finite fundamental-cycle elimination over GF(3), and records an annotated
recursive pure-braid combing trace using only task292's original relators.
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
from collections import deque
from pathlib import Path
from typing import Any, Iterable, Sequence


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "d972-r07-endpoint-zero-annotated-boundary/v1"
CHECKPOINT_SCHEMA = SCHEMA + "/checkpoint/v1"
MEMBER = "R07_ENDPOINT_ZERO_ANNOTATED_BOUNDARY_MEMBER"
PARENT_MEMBER = "R07_DIRECT_RELATOR_A5_A7_FUSION_MEMBER"
UNKNOWN_INPUT = "UNKNOWN_INPUT"
UNKNOWN_RESOURCE = "UNKNOWN_RESOURCE"
BLOCKS = ("H1", "H2", "P")
RANK = {"H1": 3, "H2": 3, "P": 4}
MODULUS = 3

PARENT_PRODUCER_PIN = (
    "search/d972_r07_direct_relator_a5_a7_fusion_v5.py", 57482,
    "ce9c6b0d7ba587f877634b60e0162f8ad3f60091b182b3031775b512f719f2ff")
PARENT_CHECKER_PIN = (
    "crosscheck/check_d972_r07_direct_relator_a5_a7_fusion_v5.py", 29559,
    "e651ad1909e3a50152e9ff7574b6a3f7dddf841402fff04ef809c81e940ccfba")
PARENT_DRIVER_PIN = (
    "search/d972_r07_direct_relator_a5_a7_fusion_gha_driver_v5.g", 6675,
    "5f1aefba79c4fde1c5a0688a62a83effe3bb590e16c016c95a6797514d6f2dea")
TASK292_PIN = (
    "search/d972_r07_actual_three_exact_pb_endpoints_v2.py", 40044,
    "c44d2c8e7fdd7dcbf691600ba823445d1ac45695ef173043c723874a409f7208")
TASK292_CHECKER_PIN = (
    "crosscheck/check_d972_r07_actual_three_exact_pb_endpoints_v2.py", 46873,
    "8d7598f376715af16ccec7bae5550f2c5329922b1b36326643a2a4e9e7cf72d8")

PARENT_SCHEMA = "d972-r07-direct-relator-a5-a7-fusion/v5"
PARENT_VERDICT_SCHEMA = PARENT_SCHEMA + "/checker-verdict/v5"
PARENT_CHECKPOINT_SCHEMA = PARENT_SCHEMA + "/checkpoint/v2"
PARENT_SIDECAR_SCHEMA = PARENT_SCHEMA + "/a5-sidecar/v2"


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


def check_seal(value: dict[str, Any], label: str) -> None:
    claimed = value.get("self_digest_sha256")
    body = dict(value)
    body.pop("self_digest_sha256", None)
    need(type(claimed) is str and claimed == digest(body), label + ":seal")


def reduced(word: Iterable[int], width: int | None = None) -> list[int]:
    out: list[int] = []
    for raw in word:
        need(type(raw) is int and raw != 0, "word:letter")
        if width is not None:
            need(abs(raw) <= width, "word:width")
        if out and out[-1] == -raw:
            out.pop()
        else:
            out.append(raw)
    return out


def inverse(word: Sequence[int]) -> list[int]:
    return [-int(letter) for letter in reversed(word)]


def product(*words: Sequence[int], width: int | None = None) -> list[int]:
    return reduced((letter for word in words for letter in word), width)


def inside(raw: str | Path, areas: tuple[str, ...] | None = None,
           must_exist: bool = True) -> Path:
    text = str(raw).replace("\\", "/")
    path = Path(text)
    need(not path.is_absolute() and ".." not in path.parts and
         "." not in path.parts, "path:lexical:" + text)
    try:
        value = (ROOT / path).resolve(strict=must_exist)
        value.relative_to(ROOT.resolve())
        if areas is not None:
            need(any(value.is_relative_to((ROOT / area).resolve(strict=True))
                     for area in areas), "path:area:" + text)
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
        "task377_v5_producer": pin_value(PARENT_PRODUCER_PIN),
        "task377_v5_checker": pin_value(PARENT_CHECKER_PIN),
        "task377_v5_driver": pin_value(PARENT_DRIVER_PIN),
        "task292_v2_producer": pin_value(TASK292_PIN),
        "task292_v2_checker": pin_value(TASK292_CHECKER_PIN),
    }


def check_all_pins() -> None:
    for label, pin in (("parent:producer", PARENT_PRODUCER_PIN),
                       ("parent:checker", PARENT_CHECKER_PIN),
                       ("parent:driver", PARENT_DRIVER_PIN),
                       ("task292:producer", TASK292_PIN),
                       ("task292:checker", TASK292_CHECKER_PIN)):
        check_pin(pin, label)


def read_json(raw_path: str, label: str,
              areas: tuple[str, ...] = ("ci/in", "ci/out")
              ) -> tuple[dict[str, Any], dict[str, Any]]:
    path = inside(raw_path, areas)
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
    need(type(value) is dict and raw == canon(value) + b"\n",
         label + ":canonical")
    return value, {"path": path.relative_to(ROOT).as_posix(),
                   "bytes": len(raw), "sha256": sha(raw)}


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
    need(not path.exists(), "output:stale:" + raw_path)
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
            _fields_ = [("cb", wintypes.DWORD),
                        ("PageFaultCount", wintypes.DWORD),
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
            ctypes.windll.kernel32.GetCurrentProcess(),
            ctypes.byref(counters), counters.cb)
        return int(counters.WorkingSetSize) if ok else 0
    except Exception:
        return 0


class Guard:
    def __init__(self, args: argparse.Namespace):
        self.args = args
        self.started = time.monotonic()
        self.operations = 0
        self.peak_rss = process_rss_bytes()
        self.last_checkpoint_operations = 0

    def bump(self, amount: int, phase: str) -> None:
        need(type(amount) is int and amount >= 0, "resource:operation_input")
        self.operations += amount
        if self.operations > int(self.args.max_operations):
            raise ResourceStop("phase=" + phase + ":cap=max_operations:value=" +
                               str(self.operations) + ":limit=" +
                               str(self.args.max_operations))
        self.check(phase)

    def check(self, phase: str) -> None:
        elapsed = time.monotonic() - self.started
        if elapsed >= float(self.args.seconds) * 0.97:
            raise ResourceStop("phase=" + phase +
                               ":cap=wall_seconds_soft:value=" +
                               format(elapsed, ".3f") + ":limit=" +
                               str(self.args.seconds))
        rss = process_rss_bytes()
        self.peak_rss = max(self.peak_rss, rss)
        if rss and rss >= int(self.args.rss_bytes) * 9 // 10:
            raise ResourceStop("phase=" + phase +
                               ":cap=rss_bytes_soft:value=" + str(rss) +
                               ":limit=" + str(self.args.rss_bytes))

    def checkpoint_due(self) -> bool:
        return (self.operations - self.last_checkpoint_operations >=
                int(self.args.cadence))

    def marked_checkpoint(self) -> None:
        self.last_checkpoint_operations = self.operations

    def public(self) -> dict[str, Any]:
        return {"operations": self.operations,
                "max_operations": int(self.args.max_operations),
                "elapsed_seconds": time.monotonic() - self.started,
                "seconds_cap": int(self.args.seconds),
                "peak_process_rss_bytes": self.peak_rss,
                "rss_bytes_cap": int(self.args.rss_bytes),
                "soft_wall_fraction": 0.97,
                "soft_rss_fraction": 0.90}


def authenticate_parent(args: argparse.Namespace, task292: Any
                        ) -> tuple[dict[str, Any], dict[str, Any]]:
    receipt, receipt_id = read_json(args.parent_receipt, "parent_receipt")
    verdict, verdict_id = read_json(args.parent_verdict, "parent_verdict")
    checkpoint, checkpoint_id = read_json(args.parent_checkpoint,
                                          "parent_checkpoint")
    sidecar, sidecar_id = read_json(args.parent_a5_sidecar,
                                    "parent_a5_sidecar")
    for label, value in (("parent_receipt", receipt),
                         ("parent_verdict", verdict),
                         ("parent_checkpoint", checkpoint),
                         ("parent_a5_sidecar", sidecar)):
        check_seal(value, label)
    producer_id = pin_value(PARENT_PRODUCER_PIN)
    need(receipt.get("schema") == PARENT_SCHEMA and
         receipt.get("status") == "COMPLETE" and
         receipt.get("terminal") == PARENT_MEMBER and
         receipt.get("mode") == "PRODUCTION" and
         receipt.get("source") == producer_id,
         "parent:member_envelope")
    claims = receipt.get("claims", {})
    need(claims.get("A5") == "MEMBER" and claims.get("A6_M") is True and
         claims.get("A7") == "ZERO" and
         claims.get("fixed_word_only") is True and
         all(claims.get(key) == "NONE" for key in
             ("A8", "A9", "compatible_lift", "mixed_prime",
              "perfect_core", "fake", "Ihara")),
         "parent:fixed_word_claim_scope")
    parent_bindings = receipt.get("static_bindings")
    need(type(parent_bindings) is dict and
         parent_bindings.get("task292_v2_producer") == pin_value(TASK292_PIN) and
         parent_bindings.get("task292_v2_checker") ==
             pin_value(TASK292_CHECKER_PIN),
         "parent:static_bindings")
    artifacts = receipt.get("artifacts")
    need(type(artifacts) is dict and
         artifacts.get("checkpoint") == checkpoint_id and
         artifacts.get("a5_sidecar") == sidecar_id,
         "parent:artifact_links")
    need(verdict.get("schema") == PARENT_VERDICT_SCHEMA and
         verdict.get("status") == "ACCEPTED" and
         verdict.get("terminal") == PARENT_MEMBER and
         verdict.get("independent") is True and
         verdict.get("receipt") == receipt_id and
         verdict.get("artifacts") == artifacts and
         verdict.get("claims") == claims,
         "parent:accepted_verdict")
    replay = verdict.get("endpoint_replay", {})
    need(replay.get("final_terminal") == task292.ZERO and
         replay.get("independent_task292_replay") is True and
         replay.get("full_C1_zero") is True,
         "parent:task292_zero_terminal")
    result = receipt.get("result")
    need(type(result) is dict and result.get("terminal_kind") == "MEMBER" and
         result.get("fixed_word_only") is True,
         "parent:result_scope")
    a5 = result.get("a5")
    need(type(a5) is dict and a5.get("terminal_kind") == "MEMBER",
         "parent:a5_member")
    need(checkpoint.get("schema") == PARENT_CHECKPOINT_SCHEMA and
         checkpoint.get("source") == producer_id and
         checkpoint.get("static_bindings") == parent_bindings and
         checkpoint.get("owners") == receipt.get("owners") and
         checkpoint.get("a5_result") == a5 and
         checkpoint.get("a5_digest_sha256") == digest(a5),
         "parent:checkpoint_binding")
    expected_parent_phase = ("CANONICAL_ENDPOINT_ZERO_COMPLETE"
                             if result.get("canonical_M_only") is True else
                             "LIFT_NULL_MEMBER_COMPLETE")
    need(checkpoint.get("phase") == expected_parent_phase,
         "parent:checkpoint_terminal_phase")
    need(sidecar.get("schema") == PARENT_SIDECAR_SCHEMA and
         sidecar.get("status") == "ACCEPTED_A5_MEMBER" and
         sidecar.get("terminal") == "R07_ZERO_BASE_A5_A6_MEMBER" and
         sidecar.get("source") == producer_id and
         sidecar.get("static_bindings") == parent_bindings and
         sidecar.get("owners") == receipt.get("owners") and
         sidecar.get("a5_result") == a5,
         "parent:sidecar_binding")
    endpoint = result.get("endpoint_exact")
    need(type(endpoint) is dict and
         endpoint.get("full_C1_replay", {}).get("performed") is True and
         endpoint.get("full_C1_replay", {}).get("q_B_extracted") is False,
         "parent:full_C1_owner")
    presentations = endpoint.get("complete_presentations", {})
    for rank in (3, 4):
        rows = presentations.get("PB" + str(rank), {}).get("relators")
        need(type(rows) is list and
             [row.get("relator") for row in rows] == task292.pure_relations(rank),
             "parent:presentation_roster:PB" + str(rank))
    for block in BLOCKS:
        need(endpoint.get("endpoints", {}).get(block, {}).get("zero") is True,
             "parent:endpoint_zero:" + block)
        full = endpoint["full_C1_replay"].get("blocks", {}).get(block)
        need(type(full) is dict and full.get("D1_z_zero") is True and
             full.get("D1_z_buckets") == [] and
             full.get("complete_presentation") == "PB" + str(RANK[block]) and
             type(full.get("z_finite_support")) is list,
             "parent:z_owner:" + block)
    parents = {"receipt": receipt_id, "verdict": verdict_id,
               "checkpoint": checkpoint_id, "a5_sidecar": sidecar_id,
               "producer_source": producer_id,
               "checker_authority": pin_value(PARENT_CHECKER_PIN),
               "driver_authority": pin_value(PARENT_DRIVER_PIN)}
    return endpoint, parents


def key_public(key: Sequence[Sequence[int]]) -> list[list[int]]:
    return [list(part) for part in key]


def key_tuple(key: Any) -> tuple[tuple[int, ...], ...]:
    need(type(key) is list and key, "artin_key:shape")
    return tuple(tuple(int(letter) for letter in part) for part in key)


def key_token(key: Sequence[Sequence[int]]) -> str:
    return canon(key_public(key)).decode("ascii")


def chain_map(rows: list[dict[str, Any]]) -> dict[tuple[int, tuple], int]:
    out: dict[tuple[int, tuple], int] = {}
    for row in rows:
        component = int(row.get("component"))
        key = key_tuple(row.get("full_artin_key"))
        coefficient = int(row.get("coefficient_mod_3")) % MODULUS
        need(coefficient in (1, 2), "chain:nonzero_coefficient")
        need((component, key) not in out, "chain:duplicate_coordinate")
        out[(component, key)] = coefficient
    return out


def scale_chain(rows: list[dict[str, Any]], coefficient: int,
                origin: dict[str, Any]) -> list[dict[str, Any]]:
    out = []
    for row in rows:
        out.append({"component": int(row["component"]),
                    "coefficient": coefficient *
                    int(row["coefficient_mod_3"]),
                    "unreduced_group_word": list(row["representative_word"]),
                    "free_reduced_group_word": list(row["representative_word"]),
                    "full_artin_key": copy.deepcopy(row["full_artin_key"]),
                    "origin": dict(origin)})
    return out


def compile_graph(block: str, parent_block: dict[str, Any], task292: Any,
                  normalizer: Any, guard: Guard) -> dict[str, Any]:
    rank = RANK[block]
    width = len(task292.pair_list(rank))
    support = copy.deepcopy(parent_block["z_finite_support"])
    target = chain_map(support)
    vertices: dict[str, dict[str, Any]] = {}
    edges: dict[tuple[str, int], dict[str, Any]] = {}
    support_paths: list[dict[str, Any]] = []

    def exact(word: Sequence[int]) -> tuple[tuple[int, ...], ...]:
        value = reduced(word, width)
        key = normalizer.key(rank, value)
        guard.bump(1 + len(value), "graph_artin_key")
        return key

    def vertex(word: Sequence[int], origin: str) -> str:
        value = reduced(word, width)
        key = exact(value)
        token = key_token(key)
        if token not in vertices:
            vertices[token] = {"full_artin_key": key_public(key),
                               "representative_word": value,
                               "origins": [origin]}
        elif origin not in vertices[token]["origins"]:
            vertices[token]["origins"].append(origin)
        return token

    def positive_edge(source_word: Sequence[int], component: int,
                      origin: str) -> tuple[str, str]:
        need(1 <= component <= width, "graph:component")
        source = vertex(source_word, origin + ":source")
        source_rep = vertices[source]["representative_word"]
        target_word = reduced(source_rep + [component], width)
        target_token = vertex(target_word, origin + ":target")
        edge_key = (source, component)
        if edge_key not in edges:
            edges[edge_key] = {"source_token": source,
                               "target_token": target_token,
                               "component": component,
                               "source_word": list(source_rep),
                               "origins": [origin]}
        else:
            need(edges[edge_key]["target_token"] == target_token,
                 "graph:edge_target")
            if origin not in edges[edge_key]["origins"]:
                edges[edge_key]["origins"].append(origin)
        return source, target_token

    def path(word: Sequence[int], origin: str) -> str:
        cursor: list[int] = []
        vertex(cursor, origin + ":root")
        for index, letter in enumerate(reduced(word, width), 1):
            if letter > 0:
                _source, target_token = positive_edge(
                    cursor, letter, origin + ":step:" + str(index))
                cursor = reduced(cursor + [letter], width)
            else:
                next_word = reduced(cursor + [letter], width)
                source_token, _target = positive_edge(
                    next_word, -letter, origin + ":step:" + str(index))
                cursor = next_word
                target_token = source_token
            need(key_token(exact(cursor)) == target_token,
                 "graph:path_target")
        return key_token(exact(cursor))

    identity_token = vertex([], "identity")
    for ordinal, row in enumerate(support, 1):
        component = int(row.get("component"))
        representative = reduced(row.get("representative_word", []), width)
        need(representative == row.get("representative_word"),
             "support:representative_reduced")
        source_key = exact(representative)
        need(source_key == key_tuple(row.get("full_artin_key")),
             "support:source_key")
        source_token = path(representative, "support:" + str(ordinal) + ":source")
        target_word = reduced(representative + [component], width)
        target_token = path(target_word,
                            "support:" + str(ordinal) + ":target")
        edge_source, _ = positive_edge(representative, component,
                                       "support:" + str(ordinal) + ":cell")
        need(source_token == edge_source, "support:cell_source")
        support_paths.append({
            "support_ordinal": ordinal,
            "component": component,
            "source_word": representative,
            "target_word": target_word,
            "source_full_artin_key": key_public(source_key),
            "target_full_artin_key":
                copy.deepcopy(vertices[target_token]["full_artin_key"])})

    ordered_tokens = sorted(vertices)
    vertex_id = {token: index for index, token in enumerate(ordered_tokens)}
    ordered_edge_keys = sorted(edges, key=lambda item: (item[0], item[1]))
    edge_rows = []
    incidence: dict[str, list[tuple[int, int, str, int]]] = {
        token: [] for token in ordered_tokens}
    for edge_id, edge_key in enumerate(ordered_edge_keys):
        row = edges[edge_key]
        source, target_token = row["source_token"], row["target_token"]
        edge_rows.append({"edge_id": edge_id,
                          "source_vertex": vertex_id[source],
                          "target_vertex": vertex_id[target_token],
                          "source_full_artin_key":
                              copy.deepcopy(vertices[source]["full_artin_key"]),
                          "target_full_artin_key":
                              copy.deepcopy(vertices[target_token]["full_artin_key"]),
                          "component": row["component"],
                          "source_word": row["source_word"],
                          "origins": sorted(row["origins"])})
        incidence[source].append((edge_id, 1, target_token, row["component"]))
        incidence[target_token].append((edge_id, -1, source, row["component"]))

    parent: dict[str, tuple[str, int, int] | None] = {identity_token: None}
    queue: deque[str] = deque([identity_token])
    while queue:
        here = queue.popleft()
        for edge_id, orientation, there, component in sorted(incidence[here]):
            if there in parent:
                continue
            parent[there] = (here, edge_id, orientation)
            queue.append(there)
    need(len(parent) == len(vertices), "graph:connected")
    tree_edges = {value[1] for value in parent.values() if value is not None}
    paths: dict[str, list[int]] = {identity_token: []}
    pending = set(ordered_tokens) - {identity_token}
    while pending:
        advanced = False
        for token in sorted(pending):
            link = parent[token]
            need(link is not None, "tree:parent")
            prior, _edge_id, orientation = link
            if prior not in paths:
                continue
            edge = edge_rows[link[1]]
            letter = edge["component"] if orientation == 1 else -edge["component"]
            paths[token] = reduced(paths[prior] + [letter], width)
            need(key_token(exact(paths[token])) == token, "tree:path_key")
            pending.remove(token)
            advanced = True
            break
        need(advanced, "tree:path_progress")

    for row in edge_rows:
        row["tree_edge"] = row["edge_id"] in tree_edges
    vertex_rows = []
    for token in ordered_tokens:
        vertex_rows.append({"vertex_id": vertex_id[token],
                            "full_artin_key":
                                copy.deepcopy(vertices[token]["full_artin_key"]),
                            "representative_word":
                                list(vertices[token]["representative_word"]),
                            "tree_path_word": list(paths[token]),
                            "origins": sorted(vertices[token]["origins"])})

    cycles = []
    decomposition_raw: list[dict[str, Any]] = []
    residual = dict(target)
    elimination_steps = []
    for row in edge_rows:
        if row["tree_edge"]:
            continue
        source_token = ordered_tokens[row["source_vertex"]]
        target_token = ordered_tokens[row["target_vertex"]]
        loop_raw = (paths[source_token] + [row["component"]] +
                    inverse(paths[target_token]))
        loop = reduced(loop_raw, width)
        loop_key = normalizer.key(rank, loop)
        guard.bump(1 + len(loop), "fundamental_loop_artin")
        identity_key = normalizer.key(rank, [])
        need(loop_key == identity_key, "fundamental_loop:identity")
        fox = task292.chain_sources(
            [{"coefficient": 1, "left_word": [], "fox_word": loop,
              "provenance": "task378_fundamental_loop"}],
            rank, normalizer,
            {"kind": "fundamental_cycle", "block": block,
             "edge_id": row["edge_id"]})
        cycle_support, cycle_deleted = task292.collect_chain_terms(fox)
        coordinate = (row["component"],
                      key_tuple(row["source_full_artin_key"]))
        coefficient = target.get(coordinate, 0)
        cycle_index = len(cycles)
        cycle = {"cycle_index": cycle_index,
                 "edge_id": row["edge_id"],
                 "coefficient_mod_3": coefficient,
                 "loop_word_unreduced": loop_raw,
                 "loop_word": loop,
                 "loop_full_artin_key": key_public(loop_key),
                 "cycle_uncollected_terms": fox,
                 "cycle_finite_support": cycle_support,
                 "cycle_zero_deletions": cycle_deleted,
                 "trace_status": "PENDING",
                 "trace_entries": None,
                 "annotation_dag": None,
                 "recursive_normal_form": None}
        cycles.append(cycle)
        decomposition_raw.extend(scale_chain(
            cycle_support, coefficient,
            {"kind": "fundamental_cycle_decomposition",
             "block": block, "cycle_index": cycle_index}))
        for coordinate, value in chain_map(cycle_support).items():
            next_value = (residual.get(coordinate, 0) -
                          coefficient * value) % MODULUS
            if next_value:
                residual[coordinate] = next_value
            else:
                residual.pop(coordinate, None)
        elimination_steps.append({
            "cycle_index": cycle_index, "edge_id": row["edge_id"],
            "coefficient_mod_3": coefficient,
            "residual_coordinates": [
                {"component": coordinate[0],
                 "full_artin_key": key_public(coordinate[1]),
                 "coefficient_mod_3": value}
                for coordinate, value in sorted(residual.items(), key=repr)]})
    decomposed, decomposition_deleted = task292.collect_chain_terms(
        decomposition_raw)
    need(not residual and chain_map(decomposed) == target,
         "cycle_decomposition:equality")
    tree_rows = []
    for token in ordered_tokens:
        link = parent[token]
        tree_rows.append({"vertex_id": vertex_id[token],
                          "parent_vertex": None if link is None else
                              vertex_id[link[0]],
                          "parent_edge": None if link is None else link[1],
                          "orientation": None if link is None else link[2],
                          "tree_path_word": list(paths[token])})
    return {
        "rank": rank,
        "z_finite_support": support,
        "z_coordinate_count": len(target),
        "graph": {"root_vertex": vertex_id[identity_token],
                  "vertex_count": len(vertex_rows),
                  "edge_count": len(edge_rows),
                  "vertices": vertex_rows, "edges": edge_rows,
                  "support_paths": support_paths},
        "tree": {"deterministic_bfs": True,
                 "tree_edge_ids": sorted(tree_edges),
                 "paths": tree_rows},
        "cycles": cycles,
        "decomposition": {
            "uncollected_terms": decomposition_raw,
            "finite_support": decomposed,
            "zero_deletions": decomposition_deleted,
            "tree_edge_elimination": elimination_steps,
            "equals_z": True},
        "q_accumulator_sources": [],
        "q": None,
        "D2_replay": None,
    }


class TraceDAG:
    def __init__(self, relators: list[list[int]], width: int,
                 public: dict[str, Any] | None = None):
        self.relators = [reduced(row, width) for row in relators]
        self.width = width
        self.words: list[list[int]] = []
        self.word_index: dict[tuple[int, ...], int] = {}
        self.nodes: list[dict[str, Any]] = []
        if public is not None:
            need(type(public.get("word_nodes")) is list and
                 type(public.get("trace_nodes")) is list,
                 "annotation_dag:shape")
            for word in public["word_nodes"]:
                self.word(word)
            need(self.words == public["word_nodes"], "annotation_dag:words")
            for row in public["trace_nodes"]:
                need(type(row) is dict and row.get("node_id") == len(self.nodes),
                     "annotation_dag:node_order")
                self.nodes.append(copy.deepcopy(row))
                self.validate_node(len(self.nodes) - 1)

    def word(self, raw: Sequence[int]) -> int:
        value = reduced(raw, self.width)
        key = tuple(value)
        if key not in self.word_index:
            self.word_index[key] = len(self.words)
            self.words.append(value)
        return self.word_index[key]

    def value(self, word_id: int) -> list[int]:
        need(type(word_id) is int and 0 <= word_id < len(self.words),
             "annotation_dag:word_id")
        return self.words[word_id]

    def endpoints(self, node_id: int) -> tuple[list[int], list[int]]:
        need(type(node_id) is int and 0 <= node_id < len(self.nodes),
             "annotation_dag:trace_id")
        row = self.nodes[node_id]
        return self.value(row["left_word"]), self.value(row["right_word"])

    def append(self, row: dict[str, Any]) -> int:
        row = dict(row)
        row["node_id"] = len(self.nodes)
        self.nodes.append(row)
        self.validate_node(row["node_id"])
        return row["node_id"]

    def empty(self, left: Sequence[int], right: Sequence[int] | None = None
              ) -> int:
        right_value = left if right is None else right
        need(reduced(left, self.width) == reduced(right_value, self.width),
             "annotation:free_equality")
        return self.append({"kind": "empty", "left_word": self.word(left),
                            "right_word": self.word(right_value)})

    def atom(self, left: Sequence[int], right: Sequence[int],
             conjugator: Sequence[int], relator_index: int, sign: int) -> int:
        need(sign in (-1, 1) and
             1 <= relator_index <= len(self.relators), "annotation:atom")
        return self.append({"kind": "atom", "left_word": self.word(left),
                            "right_word": self.word(right),
                            "conjugator_word": self.word(conjugator),
                            "relator_index": relator_index, "sign": sign})

    def context(self, prefix: Sequence[int], suffix: Sequence[int],
                child: int) -> int:
        left, right = self.endpoints(child)
        return self.append({"kind": "context",
                            "left_word": self.word(product(prefix, left, suffix,
                                                           width=self.width)),
                            "right_word": self.word(product(prefix, right, suffix,
                                                            width=self.width)),
                            "prefix_word": self.word(prefix),
                            "suffix_word": self.word(suffix),
                            "child": child})

    def reverse(self, child: int) -> int:
        left, right = self.endpoints(child)
        return self.append({"kind": "reverse",
                            "left_word": self.word(right),
                            "right_word": self.word(left),
                            "child": child})

    def concat(self, children: Sequence[int]) -> int:
        roster = [int(value) for value in children]
        need(bool(roster), "annotation:concat_empty")
        for left_id, right_id in zip(roster, roster[1:]):
            need(self.endpoints(left_id)[1] == self.endpoints(right_id)[0],
                 "annotation:concat_endpoint")
        return self.append({"kind": "concat",
                            "left_word": self.word(self.endpoints(roster[0])[0]),
                            "right_word": self.word(self.endpoints(roster[-1])[1]),
                            "children": roster})

    def validate_node(self, node_id: int) -> None:
        row = self.nodes[node_id]
        need(row.get("node_id") == node_id and
             type(row.get("kind")) is str, "annotation_dag:node")
        left = self.value(row.get("left_word"))
        right = self.value(row.get("right_word"))
        kind = row["kind"]
        if kind == "empty":
            need(left == right, "annotation:empty")
        elif kind == "atom":
            index = int(row.get("relator_index"))
            sign = int(row.get("sign"))
            need(sign in (-1, 1) and 1 <= index <= len(self.relators),
                 "annotation:atom_roster")
            relator = self.relators[index - 1]
            signed = relator if sign == 1 else inverse(relator)
            conjugator = self.value(row.get("conjugator_word"))
            discrepancy = product(left, inverse(right), width=self.width)
            claimed = product(conjugator, signed, inverse(conjugator),
                              width=self.width)
            need(discrepancy == claimed, "annotation:atom_invariant")
        elif kind == "context":
            child_id = int(row.get("child"))
            need(0 <= child_id < node_id, "annotation:context_ancestry")
            child_left, child_right = self.endpoints(child_id)
            prefix = self.value(row.get("prefix_word"))
            suffix = self.value(row.get("suffix_word"))
            need(left == product(prefix, child_left, suffix, width=self.width) and
                 right == product(prefix, child_right, suffix, width=self.width),
                 "annotation:context_invariant")
        elif kind == "reverse":
            child_id = int(row.get("child"))
            need(0 <= child_id < node_id, "annotation:reverse_ancestry")
            child_left, child_right = self.endpoints(child_id)
            need(left == child_right and right == child_left,
                 "annotation:reverse_invariant")
        elif kind == "concat":
            children = row.get("children")
            need(type(children) is list and children,
                 "annotation:concat_children")
            need(all(type(child) is int and 0 <= child < node_id
                     for child in children), "annotation:concat_ancestry")
            for first, second in zip(children, children[1:]):
                need(self.endpoints(first)[1] == self.endpoints(second)[0],
                     "annotation:concat_invariant")
            need(left == self.endpoints(children[0])[0] and
                 right == self.endpoints(children[-1])[1],
                 "annotation:concat_boundary")
        else:
            raise InputStop("annotation:unknown_kind")

    def flatten(self, node_id: int) -> list[dict[str, Any]]:
        need(type(node_id) is int and 0 <= node_id < len(self.nodes),
             "annotation:flatten_root")
        output: list[dict[str, Any]] = []
        stack: list[tuple[int, list[int], bool]] = [(node_id, [], False)]
        while stack:
            current, outer_prefix, reversed_trace = stack.pop()
            row = self.nodes[current]
            kind = row["kind"]
            if kind == "empty":
                continue
            if kind == "atom":
                output.append({
                    "conjugator_word": product(
                        outer_prefix, self.value(row["conjugator_word"]),
                        width=self.width),
                    "relator_index": int(row["relator_index"]),
                    "sign": int(row["sign"]) *
                            (-1 if reversed_trace else 1)})
                continue
            if kind == "context":
                prefix = product(outer_prefix,
                                 self.value(row["prefix_word"]),
                                 width=self.width)
                stack.append((int(row["child"]), prefix, reversed_trace))
                continue
            if kind == "reverse":
                stack.append((int(row["child"]), outer_prefix,
                              not reversed_trace))
                continue
            children = list(row["children"])
            desired = list(reversed(children)) if reversed_trace else children
            for child in reversed(desired):
                stack.append((int(child), list(outer_prefix), reversed_trace))
        return output

    def trace_product(self, entries: Sequence[dict[str, Any]]) -> list[int]:
        value: list[int] = []
        for row in entries:
            index = int(row["relator_index"])
            sign = int(row["sign"])
            relator = self.relators[index - 1]
            signed = relator if sign == 1 else inverse(relator)
            conjugator = reduced(row["conjugator_word"], self.width)
            value = product(value, conjugator, signed, inverse(conjugator),
                            width=self.width)
        return value

    def public(self) -> dict[str, Any]:
        return {"word_nodes": copy.deepcopy(self.words),
                "trace_nodes": copy.deepcopy(self.nodes)}

    def mark(self) -> tuple[int, int]:
        return len(self.words), len(self.nodes)

    def rollback(self, mark: tuple[int, int]) -> None:
        word_count, node_count = mark
        self.words = self.words[:word_count]
        self.nodes = self.nodes[:node_count]
        self.word_index = {tuple(word): index
                           for index, word in enumerate(self.words)}


class CombingMachine:
    def __init__(self, task292: Any, top_rank: int, input_word: list[int],
                 guard: Guard, public: dict[str, Any] | None = None):
        self.task292 = task292
        self.top_rank = top_rank
        self.width = len(task292.pair_list(top_rank))
        self.guard = guard
        self.relators = task292.pure_relations(top_rank)
        self.normalizer = task292.ExactArtin(task292.Budget())
        if public is None:
            self.input_word = reduced(input_word, self.width)
            self.current_word = list(self.input_word)
            self.rank_cursor = top_rank
            self.dag = TraceDAG(self.relators, self.width)
            self.trace_root = self.dag.empty(self.input_word)
            self.steps = 0
            self.last_action = None
        else:
            need(public.get("top_rank") == top_rank and
                 public.get("input_word") == reduced(input_word, self.width),
                 "combing:resume_input")
            self.input_word = list(public["input_word"])
            self.current_word = reduced(public.get("current_word", []),
                                        self.width)
            need(self.current_word == public.get("current_word"),
                 "combing:resume_current")
            self.rank_cursor = int(public.get("rank_cursor"))
            need(2 <= self.rank_cursor <= top_rank, "combing:resume_rank")
            self.dag = TraceDAG(self.relators, self.width,
                                public.get("annotation_dag"))
            self.trace_root = int(public.get("trace_root"))
            left, right = self.dag.endpoints(self.trace_root)
            need(left == self.input_word and right == self.current_word,
                 "combing:resume_trace_boundary")
            self.steps = int(public.get("steps"))
            self.last_action = copy.deepcopy(public.get("last_action"))
        identity_key = self.normalizer.key(self.top_rank, [])
        need(self.normalizer.key(self.top_rank, self.input_word) == identity_key,
             "combing:input_artin_identity")

    def local_pairs(self, rank: int) -> list[list[int]]:
        return self.task292.pair_list(rank)

    def local_to_top_index(self, rank: int, local_index: int) -> int:
        pair = self.local_pairs(rank)[local_index - 1]
        return self.task292.pair_index(self.top_rank, pair)

    def top_to_local_letter(self, rank: int, letter: int) -> int:
        pair = self.task292.pair_list(self.top_rank)[abs(letter) - 1]
        need(pair[1] <= rank, "combing:subgroup_letter")
        value = self.task292.pair_index(rank, pair)
        return value if letter > 0 else -value

    def embed_word(self, rank: int, word: Sequence[int]) -> list[int]:
        return [self.local_to_top_index(rank, abs(letter)) *
                (1 if letter > 0 else -1) for letter in word]

    def phi(self, rank: int, old_letter: int,
            kernel_word: Sequence[int]) -> list[int]:
        pairs = self.local_pairs(rank)
        pair = pairs[abs(old_letter) - 1]
        need(pair[1] < rank, "combing:phi_old")
        braid = self.task292.aij_braid(*pair)
        if old_letter < 0:
            braid = self.task292.inverse_word(braid)
        action = self.task292.artin_images(rank - 1, braid,
                                           self.normalizer.budget)
        kernel = [[self.task292.pair_index(rank, [k, rank])]
                  for k in range(1, rank)]
        images = [self.task292.substitute(image, kernel,
                                          len(pairs)) for image in action]
        kernel_indices = [row[0] for row in kernel]
        value_raw: list[int] = []
        for letter in kernel_word:
            need(abs(letter) in kernel_indices, "combing:phi_kernel_letter")
            image = images[kernel_indices.index(abs(letter))]
            value_raw.extend(image if letter > 0 else inverse(image))
        value = reduced(value_raw, len(pairs))
        self.guard.bump(1 + len(value), "combing_phi_action")
        return value

    def relation_index(self, rank: int, old_generator: int,
                       kernel_generator: int) -> int:
        phi = self.phi(rank, old_generator, [kernel_generator])
        relation = reduced([-old_generator, kernel_generator, old_generator] +
                           inverse(phi), len(self.local_pairs(rank)))
        roster = self.task292.pure_relations(rank)
        matches = [index for index, row in enumerate(roster, 1)
                   if reduced(row, len(self.local_pairs(rank))) == relation]
        need(len(matches) == 1, "combing:unique_original_relator")
        index = matches[0]
        need(self.relators[index - 1] == self.embed_word(rank, roster[index - 1]),
             "combing:embedded_original_relator")
        return index

    def positive_atom(self, rank: int, kernel_letter: int,
                      old_generator: int) -> tuple[list[int], int]:
        need(old_generator > 0 and kernel_letter != 0,
             "combing:positive_atom_input")
        kernel_generator = abs(kernel_letter)
        relation_index = self.relation_index(rank, old_generator,
                                             kernel_generator)
        left = [kernel_letter, old_generator]
        right = [old_generator] + self.phi(rank, old_generator,
                                           [kernel_letter])
        if kernel_letter > 0:
            conjugator = [old_generator]
            sign = 1
        else:
            conjugator = [-kernel_generator, old_generator]
            sign = -1
        node = self.dag.atom(self.embed_word(rank, left),
                             self.embed_word(rank, right),
                             self.embed_word(rank, conjugator),
                             relation_index, sign)
        self.guard.bump(1 + len(right), "combing_positive_crossing")
        return reduced(right, len(self.local_pairs(rank))), node

    def positive_collect(self, rank: int, kernel_word: Sequence[int],
                         old_generator: int) -> tuple[list[int], int]:
        width = len(self.local_pairs(rank))
        original = reduced(kernel_word, width)
        current = original + [old_generator]
        root = self.dag.empty(self.embed_word(rank, current))
        suffix: list[int] = []
        for index in range(len(original) - 1, -1, -1):
            image, atom = self.positive_atom(rank, original[index],
                                             old_generator)
            step = self.dag.context(self.embed_word(rank, original[:index]),
                                    self.embed_word(rank, suffix), atom)
            expected_left = self.embed_word(rank, current)
            need(self.dag.endpoints(step)[0] ==
                 reduced(expected_left, self.width),
                 "combing:positive_collect_left")
            next_local = reduced(original[:index] + image + suffix, width)
            need(self.dag.endpoints(step)[1] ==
                 reduced(self.embed_word(rank, next_local), self.width),
                 "combing:positive_collect_right")
            root = self.dag.concat([root, step])
            current = next_local
            suffix = reduced(image[1:] + suffix, width)
        target = reduced([old_generator] +
                         self.phi(rank, old_generator, original), width)
        need(current == target and
             self.dag.endpoints(root) ==
             (reduced(self.embed_word(rank, original + [old_generator]),
                      self.width),
              reduced(self.embed_word(rank, target), self.width)),
             "combing:positive_collect_target")
        return target, root

    def crossing(self, rank: int, kernel_letter: int,
                 old_letter: int) -> tuple[list[int], int, dict[str, Any]]:
        width = len(self.local_pairs(rank))
        if old_letter > 0:
            right, node = self.positive_atom(rank, kernel_letter, old_letter)
            return right, node, {"kind": "positive_old",
                                 "phi_word": right[1:]}
        old_generator = -old_letter
        h = self.phi(rank, -old_generator, [kernel_letter])
        positive_right, positive_trace = self.positive_collect(
            rank, h, old_generator)
        need(positive_right == reduced([old_generator, kernel_letter], width),
             "combing:old_inverse_action_inverse")
        reversed_trace = self.dag.reverse(positive_trace)
        node = self.dag.context(self.embed_word(rank, [-old_generator]),
                                self.embed_word(rank, [-old_generator]),
                                reversed_trace)
        left = self.embed_word(rank, [kernel_letter, -old_generator])
        right_local = reduced([-old_generator] + h, width)
        need(self.dag.endpoints(node) ==
             (reduced(left, self.width),
              reduced(self.embed_word(rank, right_local), self.width)),
             "combing:old_inverse_context")
        return right_local, node, {"kind": "negative_old",
                                  "inverse_action_word": h,
                                  "positive_action_replay": positive_right}

    def find_inversion(self, rank: int) -> tuple[int, int, int] | None:
        top_pairs = self.task292.pair_list(self.top_rank)
        for position in range(len(self.current_word) - 1):
            first, second = self.current_word[position:position + 2]
            first_pair = top_pairs[abs(first) - 1]
            second_pair = top_pairs[abs(second) - 1]
            if (first_pair[1] == rank and second_pair[1] < rank):
                return (position,
                        self.top_to_local_letter(rank, first),
                        self.top_to_local_letter(rank, second))
        return None

    def step(self) -> bool:
        if self.rank_cursor < 3:
            return True
        inversion = self.find_inversion(self.rank_cursor)
        if inversion is None:
            self.rank_cursor -= 1
            self.steps += 1
            self.last_action = {"kind": "rank_complete",
                                "completed_rank": self.rank_cursor + 1}
            self.guard.bump(1, "combing_rank_descent")
            return self.rank_cursor < 3
        position, kernel_letter, old_letter = inversion
        mark = self.dag.mark()
        prior_root = self.trace_root
        prior_word = list(self.current_word)
        try:
            right_local, local_trace, action = self.crossing(
                self.rank_cursor, kernel_letter, old_letter)
            prefix = self.current_word[:position]
            suffix = self.current_word[position + 2:]
            embedded_right = self.embed_word(self.rank_cursor, right_local)
            global_trace = self.dag.context(prefix, suffix, local_trace)
            need(self.dag.endpoints(global_trace)[0] == self.current_word,
                 "combing:global_crossing_left")
            next_word = reduced(prefix + embedded_right + suffix, self.width)
            need(self.dag.endpoints(global_trace)[1] == next_word,
                 "combing:global_crossing_right")
            self.trace_root = self.dag.concat([self.trace_root, global_trace])
            self.current_word = next_word
            self.steps += 1
            self.last_action = dict(action, rank=self.rank_cursor,
                                    position=position,
                                    kernel_letter=kernel_letter,
                                    old_letter=old_letter,
                                    current_word=list(next_word))
            self.guard.bump(1 + len(embedded_right), "combing_rewrite_commit")
            return False
        except Exception:
            self.dag.rollback(mark)
            self.trace_root = prior_root
            self.current_word = prior_word
            raise

    def finish(self) -> tuple[list[dict[str, Any]], dict[str, Any]]:
        need(self.rank_cursor < 3, "combing:not_finished")
        identity_key = self.normalizer.key(self.top_rank, [])
        need(self.normalizer.key(self.top_rank, self.current_word) == identity_key,
             "combing:normal_form_artin_identity")
        need(self.current_word == [], "combing:recursive_normal_form_nonempty")
        entries = self.dag.flatten(self.trace_root)
        self.guard.bump(1 + sum(len(row["conjugator_word"]) for row in entries),
                        "combing_final_trace_flatten")
        discrepancy = product(self.input_word, inverse(self.current_word),
                              width=self.width)
        need(self.dag.trace_product(entries) == discrepancy,
             "combing:final_literal_trace")
        return entries, {"top_rank": self.top_rank,
                         "normal_form": list(self.current_word),
                         "trace_root": self.trace_root,
                         "steps": self.steps,
                         "annotation_dag": self.dag.public(),
                         "literal_trace_equality": True,
                         "faithful_artin_identity": True}

    def public(self) -> dict[str, Any]:
        return {"top_rank": self.top_rank,
                "input_word": list(self.input_word),
                "current_word": list(self.current_word),
                "rank_cursor": self.rank_cursor,
                "trace_root": self.trace_root,
                "steps": self.steps,
                "last_action": copy.deepcopy(self.last_action),
                "annotation_dag": self.dag.public()}


def collect_q(block: str, block_result: dict[str, Any], task292: Any,
              normalizer: Any, guard: Guard) -> None:
    rank = RANK[block]
    expected_sources: list[dict[str, Any]] = []
    for cycle in block_result["cycles"]:
        coefficient = int(cycle["coefficient_mod_3"]) % MODULUS
        entries = cycle.get("trace_entries")
        need(type(entries) is list, "q:trace_complete")
        for trace_index, entry in enumerate(entries):
            local = coefficient * int(entry["sign"]) % MODULUS
            if not local:
                continue
            relation_index = int(entry["relator_index"])
            expected_sources.append({
                "coefficient": local,
                "left_word": list(entry["conjugator_word"]),
                "relator_index": relation_index,
                "fox_word": task292.pure_relations(rank)[relation_index - 1],
                "provenance": "task378_cycle_trace",
                "cycle_index": int(cycle["cycle_index"]),
                "trace_index": trace_index})
    sources = block_result.get("q_accumulator_sources")
    need(type(sources) is list and sources == expected_sources,
         "q:checkpoint_accumulator")
    table: dict[tuple[int, tuple], dict[str, Any]] = {}
    for source_index, source in enumerate(sources):
        key = normalizer.key(rank, source["left_word"])
        coordinate = (source["relator_index"], key)
        if coordinate not in table:
            table[coordinate] = {
                "relator_index": source["relator_index"],
                "full_artin_key": key_public(key),
                "representative_word": list(source["left_word"]),
                "integer_sum": 0, "contributors": []}
        table[coordinate]["integer_sum"] += source["coefficient"]
        table[coordinate]["contributors"].append({
            "source_index": source_index,
            "coefficient": source["coefficient"],
            "cycle_index": source["cycle_index"],
            "trace_index": source["trace_index"]})
        guard.bump(1 + len(source["left_word"]), "q_collection")
    collected, deleted = [], []
    for coordinate in sorted(table, key=repr):
        row = table[coordinate]
        row["coefficient_mod_3"] = row["integer_sum"] % MODULUS
        (collected if row["coefficient_mod_3"] else deleted).append(row)
    fox_sources = []
    relators = task292.pure_relations(rank)
    for row in collected:
        fox_sources.append({"coefficient": row["coefficient_mod_3"],
                            "left_word": row["representative_word"],
                            "fox_word": relators[row["relator_index"] - 1],
                            "provenance": "task378_collected_q"})
    d2_raw = task292.chain_sources(
        fox_sources, rank, normalizer,
        {"kind": "task378_D2_q", "block": block})
    d2_support, d2_deleted = task292.collect_chain_terms(d2_raw)
    need(chain_map(d2_support) == chain_map(block_result["z_finite_support"]),
         "D2_q_equals_z:" + block)
    block_result["q"] = {"uncollected_sources": sources,
                         "finite_support": collected,
                         "zero_deletions": deleted,
                         "original_relator_roster_only": True}
    block_result["D2_replay"] = {
        "uncollected_terms": d2_raw,
        "finite_support": d2_support,
        "zero_deletions": d2_deleted,
        "target_z": copy.deepcopy(block_result["z_finite_support"]),
        "equals_z": True,
        "coordinate_key": "(component,full_artin_key)"}


def checkpoint_value(phase: str, parents: dict[str, Any] | None,
                     state: dict[str, Any] | None,
                     resource: dict[str, Any] | None) -> dict[str, Any]:
    return seal({"schema": CHECKPOINT_SCHEMA, "mode": "PRODUCTION",
                 "phase": phase, "source": source_identity(),
                 "static_bindings": static_bindings(),
                 "parents": parents, "state": state,
                 "resource": resource,
                 "resume_contract": {
                     "all_or_none_path_bytes_sha256": True,
                     "four_parent_artifacts_bound": True,
                     "exact_artin_keys_recomputed": True,
                     "relator_words_recomputed": True,
                     "annotation_dag_only": True,
                     "no_unauthenticated_python_objects": True}})


def resume_load(args: argparse.Namespace, parents: dict[str, Any]
                ) -> dict[str, Any] | None:
    supplied = (args.resume_path is not None, args.resume_bytes is not None,
                args.resume_sha256 is not None)
    need(len(set(supplied)) == 1, "resume:all_or_none")
    if not supplied[0]:
        return None
    value, got = read_json(args.resume_path, "resume")
    need(got["bytes"] == args.resume_bytes and
         got["sha256"] == args.resume_sha256,
         "resume:physical_identity")
    check_seal(value, "resume")
    need(value.get("schema") == CHECKPOINT_SCHEMA and
         value.get("source") == source_identity() and
         value.get("static_bindings") == static_bindings() and
         value.get("parents") == parents and
         type(value.get("state")) is dict,
         "resume:source_parent_binding")
    return copy.deepcopy(value["state"])


def validate_resumed_state(state: dict[str, Any], endpoint: dict[str, Any],
                           task292: Any, guard: Guard) -> None:
    need(state.get("version") == 1 and
         state.get("phase") in ("GRAPHS", "COMBING", "BOUNDARIES",
                                "COMPLETE", "RESOURCE"),
         "resume:state_envelope")
    blocks = state.get("blocks")
    need(type(blocks) is dict and set(blocks).issubset(BLOCKS),
         "resume:blocks")
    for block in BLOCKS:
        if block not in blocks:
            continue
        normalizer = task292.ExactArtin(task292.Budget())
        current = blocks[block]
        rank = RANK[block]
        width = len(task292.pair_list(rank))
        relators = task292.pure_relations(rank)
        need(current.get("rank") == RANK[block] and
             chain_map(current.get("z_finite_support")) ==
             chain_map(endpoint["full_C1_replay"]["blocks"][block]
                       ["z_finite_support"]),
             "resume:block_parent:" + block)
        for vertex in current.get("graph", {}).get("vertices", []):
            key = normalizer.key(RANK[block], vertex["representative_word"])
            need(key == key_tuple(vertex["full_artin_key"]),
                 "resume:vertex_key:" + block)
            guard.bump(1 + len(vertex["representative_word"]),
                       "resume_artin_replay")
        vertices = current.get("graph", {}).get("vertices", [])
        for edge in current.get("graph", {}).get("edges", []):
            source = int(edge["source_vertex"])
            target = int(edge["target_vertex"])
            component = int(edge["component"])
            need(0 <= source < len(vertices) and 0 <= target < len(vertices),
                 "resume:edge_vertices:" + block)
            source_word = reduced(edge["source_word"], width)
            need(normalizer.key(rank, source_word) ==
                 key_tuple(vertices[source]["full_artin_key"]) and
                 normalizer.key(rank, source_word + [component]) ==
                 key_tuple(vertices[target]["full_artin_key"]),
                 "resume:edge_action:" + block)
        for cycle in current.get("cycles", []):
            loop = reduced(cycle.get("loop_word", []), width)
            need(normalizer.key(rank, loop) == normalizer.key(rank, []) and
                 key_tuple(cycle.get("loop_full_artin_key")) ==
                 normalizer.key(rank, []),
                 "resume:cycle_identity:" + block)
            fox = task292.chain_sources(
                [{"coefficient": 1, "left_word": [], "fox_word": loop,
                  "provenance": "task378_resume_cycle"}], rank, normalizer,
                {"kind": "task378_resume_cycle", "block": block,
                 "cycle_index": int(cycle["cycle_index"])})
            finite, _ = task292.collect_chain_terms(fox)
            need(chain_map(finite) ==
                 chain_map(cycle.get("cycle_finite_support")),
                 "resume:cycle_fox:" + block)
            if cycle.get("trace_status") == "COMPLETE":
                entries = cycle.get("trace_entries")
                need(type(entries) is list and
                     cycle.get("recursive_normal_form") == [],
                     "resume:cycle_trace:" + block)
                dag = TraceDAG(relators, width, cycle.get("annotation_dag"))
                root = int(cycle.get("trace_root"))
                need(dag.flatten(root) == entries and
                     dag.endpoints(root) == (loop, []) and
                     dag.trace_product(entries) == loop,
                     "resume:cycle_literal_replay:" + block)
        accumulated = []
        for cycle in current.get("cycles", []):
            if cycle.get("trace_status") != "COMPLETE":
                continue
            coefficient = int(cycle["coefficient_mod_3"]) % MODULUS
            for trace_index, entry in enumerate(cycle["trace_entries"]):
                local = coefficient * int(entry["sign"]) % MODULUS
                if local:
                    relation_index = int(entry["relator_index"])
                    accumulated.append({
                        "coefficient": local,
                        "left_word": list(entry["conjugator_word"]),
                        "relator_index": relation_index,
                        "fox_word": relators[relation_index - 1],
                        "provenance": "task378_cycle_trace",
                        "cycle_index": int(cycle["cycle_index"]),
                        "trace_index": trace_index})
        need(current.get("q_accumulator_sources") == accumulated,
             "resume:q_accumulator:" + block)
        need(chain_map(current.get("decomposition", {}).get("finite_support")) ==
             chain_map(current.get("z_finite_support")) and
             current.get("decomposition", {}).get("equals_z") is True,
             "resume:cycle_decomposition:" + block)
        if current.get("q") is not None:
            need(current.get("D2_replay", {}).get("equals_z") is True and
                 chain_map(current["D2_replay"]["finite_support"]) ==
                 chain_map(current.get("z_finite_support")),
                 "resume:D2_q:" + block)
        need(relators ==
             [row["relator"] for row in
              endpoint["complete_presentations"]["PB" + str(RANK[block])]
              ["relators"]], "resume:relator_roster:" + block)
    active = state.get("active_combing")
    if active is not None:
        block = state.get("block_cursor")
        cycle_index = int(state.get("cycle_cursor"))
        need(block in blocks and
             0 <= cycle_index < len(blocks[block]["cycles"]),
             "resume:active_cursor")
        cycle = blocks[block]["cycles"][cycle_index]
        CombingMachine(task292, RANK[block], cycle["loop_word"],
                       guard, active)


def progress(state: dict[str, Any], guard: Guard) -> str:
    block = state.get("block_cursor")
    cycle = int(state.get("cycle_cursor", 0))
    graphs = len(state.get("blocks", {}))
    completed_cycles = sum(sum(row.get("trace_status") == "COMPLETE"
                               for row in value.get("cycles", []))
                           for value in state.get("blocks", {}).values())
    return ("phase=" + str(state.get("phase")) + " block=" + str(block) +
            " cycle=" + str(cycle) + " graphs=" + str(graphs) +
            " completed_cycles=" + str(completed_cycles) +
            " operations=" + str(guard.operations))


def compile_all(args: argparse.Namespace, endpoint: dict[str, Any],
                parents: dict[str, Any], task292: Any, guard: Guard,
                state: dict[str, Any] | None
                ) -> tuple[dict[str, Any], dict[str, Any]]:
    if state is None:
        state = {"version": 1, "phase": "GRAPHS", "blocks": {},
                 "block_cursor": BLOCKS[0], "cycle_cursor": 0,
                 "active_combing": None}
    else:
        validate_resumed_state(state, endpoint, task292, guard)
        if state.get("phase") == "RESOURCE":
            state["phase"] = state.pop("interrupted_phase", None) or (
                "COMBING" if state.get("blocks") else "GRAPHS")

    last_checkpoint: dict[str, Any] | None = None

    def save(phase: str) -> dict[str, Any]:
        nonlocal last_checkpoint
        state["phase"] = phase
        value = checkpoint_value(phase, parents, state, guard.public())
        last_checkpoint = write_checkpoint(args.checkpoint, value,
                                           args.checkpoint_bytes)
        guard.marked_checkpoint()
        print("R07_ANNOTATED_BOUNDARY_PROGRESS " + progress(state, guard),
              flush=True)
        return last_checkpoint

    if not output_path(args.checkpoint).exists():
        save(state["phase"])
    for block in BLOCKS:
        if block in state["blocks"]:
            continue
        state["block_cursor"] = block
        normalizer = task292.ExactArtin(task292.Budget())
        parent_block = endpoint["full_C1_replay"]["blocks"][block]
        replay_chain = [{"component": row["component"],
                         "coefficient": row["coefficient_mod_3"],
                         "unreduced_group_word": row["representative_word"],
                         "free_reduced_group_word": row["representative_word"],
                         "full_artin_key": row["full_artin_key"],
                         "origin": {"kind": "task378_parent_z"}}
                        for row in parent_block["z_finite_support"]]
        d1_raw = task292.endpoint_of_chain(replay_chain, RANK[block],
                                           normalizer, "task378_D1_z")
        d1_support, _ = task292.collect_group_terms(d1_raw)
        need(not d1_support, "parent:D1_z_direct_replay:" + block)
        state["blocks"][block] = compile_graph(
            block, parent_block, task292, normalizer, guard)
        save("GRAPHS")

    state["phase"] = "COMBING"
    for block in BLOCKS:
        state["block_cursor"] = block
        block_result = state["blocks"][block]
        for cycle_index, cycle in enumerate(block_result["cycles"]):
            if cycle.get("trace_status") == "COMPLETE":
                continue
            state["cycle_cursor"] = cycle_index
            active = state.get("active_combing")
            machine = CombingMachine(task292, RANK[block], cycle["loop_word"],
                                     guard, active)
            while not machine.step():
                state["active_combing"] = machine.public()
                if guard.checkpoint_due():
                    save("COMBING")
            entries, proof = machine.finish()
            cycle["trace_status"] = "COMPLETE"
            cycle["trace_entries"] = entries
            cycle["annotation_dag"] = proof["annotation_dag"]
            cycle["recursive_normal_form"] = proof["normal_form"]
            cycle["trace_root"] = proof["trace_root"]
            cycle["combing_steps"] = proof["steps"]
            cycle["literal_trace_equality"] = True
            cycle["faithful_artin_identity"] = True
            coefficient = int(cycle["coefficient_mod_3"]) % MODULUS
            relators = task292.pure_relations(RANK[block])
            for trace_index, entry in enumerate(entries):
                local = coefficient * int(entry["sign"]) % MODULUS
                if local:
                    relation_index = int(entry["relator_index"])
                    block_result["q_accumulator_sources"].append({
                        "coefficient": local,
                        "left_word": list(entry["conjugator_word"]),
                        "relator_index": relation_index,
                        "fox_word": relators[relation_index - 1],
                        "provenance": "task378_cycle_trace",
                        "cycle_index": int(cycle["cycle_index"]),
                        "trace_index": trace_index})
            state["active_combing"] = None
            state["cycle_cursor"] = cycle_index + 1
            if guard.checkpoint_due():
                save("COMBING")

    state["phase"] = "BOUNDARIES"
    for block in BLOCKS:
        if state["blocks"][block].get("q") is not None:
            continue
        state["block_cursor"] = block
        normalizer = task292.ExactArtin(task292.Budget())
        collect_q(block, state["blocks"][block], task292, normalizer, guard)
        save("BOUNDARIES")
    state["phase"] = "COMPLETE"
    state["block_cursor"] = None
    state["cycle_cursor"] = 0
    state["active_combing"] = None
    checkpoint_id = save("COMPLETE")
    result = {"parent_terminal": PARENT_MEMBER,
              "task292_terminal": task292.ZERO,
              "fixed_word_only": True,
              "blocks": state["blocks"],
              "resource": guard.public(),
              "compiler_theorems": {
                  "finite_fundamental_cycle_decomposition": True,
                  "annotated_recursive_PB_combing": True,
                  "original_task292_relators_only": True,
                  "direct_D2_q_equals_z": True}}
    receipt = seal({"schema": SCHEMA, "status": "COMPLETE",
                    "terminal": MEMBER, "mode": "PRODUCTION",
                    "source": source_identity(),
                    "static_bindings": static_bindings(),
                    "parents": parents, "result": result,
                    "artifacts": {"checkpoint": checkpoint_id},
                    "claims": {"A8": "MEMBER", "fixed_word_only": True,
                               "A9": "NONE", "compatible_lift": "NONE",
                               "mixed_prime": "NONE", "perfect_core": "NONE",
                               "fake": "NONE", "Ihara": "NONE"}})
    return receipt, state


def resource_receipt(reason: str, parents: dict[str, Any] | None,
                     state: dict[str, Any] | None,
                     checkpoint_id: dict[str, Any] | None,
                     guard: Guard | None) -> dict[str, Any]:
    return seal({"schema": SCHEMA, "status": UNKNOWN_RESOURCE,
                 "terminal": UNKNOWN_RESOURCE + ":" + reason,
                 "mode": "PRODUCTION", "source": source_identity(),
                 "static_bindings": static_bindings(), "parents": parents,
                 "result": {"reason": reason,
                            "progress": None if state is None else
                                {"phase": state.get("phase"),
                                 "block_cursor": state.get("block_cursor"),
                                 "cycle_cursor": state.get("cycle_cursor")},
                            "resource": None if guard is None else guard.public()},
                 "artifacts": {"checkpoint": checkpoint_id},
                 "claims": {"A8": "UNKNOWN_RESOURCE",
                            "fixed_word_only": True if parents else "NONE",
                            "A9": "NONE", "compatible_lift": "NONE",
                            "mixed_prime": "NONE", "perfect_core": "NONE",
                            "fake": "NONE", "Ihara": "NONE"}})


def parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=("PRODUCTION",), default="PRODUCTION")
    ap.add_argument("--parent-receipt", required=True)
    ap.add_argument("--parent-verdict", required=True)
    ap.add_argument("--parent-checkpoint", required=True)
    ap.add_argument("--parent-a5-sidecar", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--checkpoint", required=True)
    ap.add_argument("--resume-path")
    ap.add_argument("--resume-bytes", type=int)
    ap.add_argument("--resume-sha256")
    ap.add_argument("--cadence", type=int, default=256)
    ap.add_argument("--max-operations", type=int, default=2_000_000_000)
    ap.add_argument("--seconds", type=int, default=14_400)
    ap.add_argument("--rss-bytes", type=int, default=5_000_000_000)
    ap.add_argument("--checkpoint-bytes", type=int, default=2_000_000_000)
    return ap


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    parents: dict[str, Any] | None = None
    state: dict[str, Any] | None = None
    guard: Guard | None = None
    checkpoint_id: dict[str, Any] | None = None
    task292: Any | None = None
    try:
        need(args.cadence > 0 and args.max_operations > 0 and
             args.seconds > 0 and args.rss_bytes > 0 and
             args.checkpoint_bytes > 0, "arguments:positive_caps")
        check_all_pins()
        task292 = load_pinned(TASK292_PIN, "task378_task292_producer")
        endpoint, parents = authenticate_parent(args, task292)
        guard = Guard(args)
        state = resume_load(args, parents)
        if state is None:
            state = {"version": 1, "phase": "GRAPHS", "blocks": {},
                     "block_cursor": BLOCKS[0], "cycle_cursor": 0,
                     "active_combing": None}
        receipt, state = compile_all(args, endpoint, parents, task292,
                                     guard, state)
        checkpoint_id = receipt["artifacts"]["checkpoint"]
    except Exception as exc:
        task292_resource = (task292 is not None and
                            isinstance(exc, task292.ResourceStop))
        if isinstance(exc, ResourceStop) or task292_resource:
            if task292_resource:
                reason = ("phase=" + str(exc.phase) + ":cap=" + str(exc.cap) +
                          ":value=" + str(exc.value) + ":limit=" +
                          str(exc.limit))
            else:
                reason = str(exc)
            if state is not None:
                interrupted = str(state.get("phase"))
                state["phase"] = "RESOURCE"
                state["interrupted_phase"] = interrupted
            checkpoint_path = output_path(args.checkpoint)
            try:
                if state is not None and "cap=checkpoint_bytes" not in reason:
                    checkpoint_id = write_checkpoint(
                        args.checkpoint,
                        checkpoint_value("RESOURCE", parents, state,
                                         None if guard is None else guard.public()),
                        args.checkpoint_bytes)
                elif checkpoint_path.exists():
                    checkpoint_id = identity(checkpoint_path)
            except ResourceStop:
                checkpoint_id = (identity(checkpoint_path)
                                 if checkpoint_path.exists() else None)
            receipt = resource_receipt(reason, parents, state,
                                       checkpoint_id, guard)
        else:
            reason = str(exc)
            checkpoint = checkpoint_value(
                "INPUT_REJECTED", parents, state,
                None if guard is None else guard.public())
            checkpoint_id = write_checkpoint(args.checkpoint, checkpoint,
                                             args.checkpoint_bytes)
            receipt = seal({"schema": SCHEMA, "status": UNKNOWN_INPUT,
                            "terminal": UNKNOWN_INPUT + ":" + reason,
                            "mode": "PRODUCTION", "source": source_identity(),
                            "static_bindings": static_bindings(),
                            "parents": parents, "result": {"reason": reason},
                            "artifacts": {"checkpoint": checkpoint_id},
                            "claims": {"A8": "NONE",
                                       "fixed_word_only": "NONE",
                                       "A9": "NONE",
                                       "compatible_lift": "NONE",
                                       "mixed_prime": "NONE",
                                       "perfect_core": "NONE",
                                       "fake": "NONE", "Ihara": "NONE"}})
    write_exclusive(args.output, receipt)
    print("R07_ENDPOINT_ZERO_ANNOTATED_BOUNDARY_V1_PRODUCER_TERMINAL " +
          str(receipt["terminal"]), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
