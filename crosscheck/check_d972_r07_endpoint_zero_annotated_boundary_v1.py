#!/usr/bin/env python3
"""Independent checker for task378 annotated PB boundary receipts.

The new producer is never imported.  All PB equality and Fox calculations
use the separately implemented task292 checker owner.
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
from collections import deque
from pathlib import Path
from typing import Any, Iterable, Sequence


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "d972-r07-endpoint-zero-annotated-boundary/v1"
VERDICT_SCHEMA = SCHEMA + "/checker-verdict/v1"
CHECKPOINT_SCHEMA = SCHEMA + "/checkpoint/v1"
MEMBER = "R07_ENDPOINT_ZERO_ANNOTATED_BOUNDARY_MEMBER"
PARENT_MEMBER = "R07_DIRECT_RELATOR_A5_A7_FUSION_MEMBER"
BLOCKS = ("H1", "H2", "P")
RANK = {"H1": 3, "H2": 3, "P": 4}
MODULUS = 3

# Filled with the final immutable producer identity before driver pinning.
PRODUCER_PIN = (
    "search/d972_r07_endpoint_zero_annotated_boundary_v1.py", 79194,
    "c6e4b0d99ed79f9eabedf225c964a598b2f21b3ab10758cb9d5f83a60ceb5d11")
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


def check_seal(value: dict[str, Any], label: str) -> None:
    claimed = value.get("self_digest_sha256")
    body = dict(value)
    body.pop("self_digest_sha256", None)
    require(type(claimed) is str and claimed == digest(body), label + ":seal")


def reduced(word: Iterable[int], width: int | None = None) -> list[int]:
    out: list[int] = []
    for raw in word:
        require(type(raw) is int and raw != 0, "word:letter")
        if width is not None:
            require(abs(raw) <= width, "word:width")
        if out and out[-1] == -raw:
            out.pop()
        else:
            out.append(raw)
    return out


def inverse(word: Sequence[int]) -> list[int]:
    return [-int(letter) for letter in reversed(word)]


def product(*words: Sequence[int], width: int | None = None) -> list[int]:
    return reduced((letter for word in words for letter in word), width)


def inside(raw: str | Path, areas: tuple[str, ...] | None = None) -> Path:
    text = str(raw).replace("\\", "/")
    path = Path(text)
    require(not path.is_absolute() and ".." not in path.parts and
            "." not in path.parts, "path:lexical:" + text)
    try:
        value = (ROOT / path).resolve(strict=True)
        value.relative_to(ROOT.resolve())
        if areas is not None:
            require(any(value.is_relative_to((ROOT / area).resolve(strict=True))
                        for area in areas), "path:area:" + text)
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


def check_pin(pin: tuple[str, int, str], label: str) -> dict[str, Any]:
    got = identity(inside(pin[0]))
    want = pin_value(pin)
    require(got == want, label + ":pin")
    return want


def load_pinned(pin: tuple[str, int, str], name: str) -> types.ModuleType:
    path = inside(pin[0])
    check_pin(pin, name)
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None, name + ":loader")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def source_identity() -> dict[str, Any]:
    return identity(Path(__file__).resolve())


def static_bindings() -> dict[str, Any]:
    return {"task377_v5_producer": pin_value(PARENT_PRODUCER_PIN),
            "task377_v5_checker": pin_value(PARENT_CHECKER_PIN),
            "task377_v5_driver": pin_value(PARENT_DRIVER_PIN),
            "task292_v2_producer": pin_value(TASK292_PIN),
            "task292_v2_checker": pin_value(TASK292_CHECKER_PIN)}


def read_json(raw_path: str, label: str,
              areas: tuple[str, ...] = ("ci/in", "ci/out")
              ) -> tuple[dict[str, Any], dict[str, Any]]:
    path = inside(raw_path, areas)
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
    require(type(value) is dict and raw == canon(value) + b"\n",
            label + ":canonical")
    return value, {"path": path.relative_to(ROOT).as_posix(),
                   "bytes": len(raw), "sha256": sha(raw)}


def output_path(raw: str) -> Path:
    path = Path(str(raw).replace("\\", "/"))
    require(not path.is_absolute() and ".." not in path.parts and
            "." not in path.parts, "output:lexical")
    target = (ROOT / path).resolve(strict=False)
    require(target.parent == (ROOT / "ci/out").resolve(strict=True),
            "output:containment")
    return target


def write_exclusive(raw_path: str, value: dict[str, Any]) -> None:
    path = output_path(raw_path)
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


def key_tuple(key: Any) -> tuple[tuple[int, ...], ...]:
    require(type(key) is list and key, "artin_key:shape")
    return tuple(tuple(int(letter) for letter in part) for part in key)


def key_public(key: Sequence[Sequence[int]]) -> list[list[int]]:
    return [list(part) for part in key]


def key_token(key: Sequence[Sequence[int]]) -> str:
    return canon(key_public(key)).decode("ascii")


def chain_map(rows: list[dict[str, Any]]) -> dict[tuple[int, tuple], int]:
    output: dict[tuple[int, tuple], int] = {}
    require(type(rows) is list, "chain:rows")
    for row in rows:
        coordinate = (int(row.get("component")),
                      key_tuple(row.get("full_artin_key")))
        coefficient = int(row.get("coefficient_mod_3")) % MODULUS
        require(coefficient in (1, 2) and coordinate not in output,
                "chain:coordinate")
        output[coordinate] = coefficient
    return output


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
    require(receipt.get("schema") == PARENT_SCHEMA and
            receipt.get("status") == "COMPLETE" and
            receipt.get("terminal") == PARENT_MEMBER and
            receipt.get("mode") == "PRODUCTION" and
            receipt.get("source") == producer_id,
            "parent:member_envelope")
    claims = receipt.get("claims", {})
    require(claims.get("A5") == "MEMBER" and
            claims.get("A6_M") is True and claims.get("A7") == "ZERO" and
            claims.get("fixed_word_only") is True and
            all(claims.get(key) == "NONE" for key in
                ("A8", "A9", "compatible_lift", "mixed_prime",
                 "perfect_core", "fake", "Ihara")),
            "parent:claim_scope")
    parent_bindings = receipt.get("static_bindings")
    require(type(parent_bindings) is dict and
            parent_bindings.get("task292_v2_producer") == pin_value(TASK292_PIN) and
            parent_bindings.get("task292_v2_checker") ==
                pin_value(TASK292_CHECKER_PIN),
            "parent:static_bindings")
    artifacts = receipt.get("artifacts")
    require(type(artifacts) is dict and
            artifacts.get("checkpoint") == checkpoint_id and
            artifacts.get("a5_sidecar") == sidecar_id,
            "parent:artifact_links")
    require(verdict.get("schema") == PARENT_VERDICT_SCHEMA and
            verdict.get("status") == "ACCEPTED" and
            verdict.get("terminal") == PARENT_MEMBER and
            verdict.get("independent") is True and
            verdict.get("receipt") == receipt_id and
            verdict.get("artifacts") == artifacts and
            verdict.get("claims") == claims,
            "parent:accepted_verdict")
    replay = verdict.get("endpoint_replay", {})
    require(replay.get("final_terminal") == task292.ZERO and
            replay.get("independent_task292_replay") is True and
            replay.get("full_C1_zero") is True,
            "parent:task292_zero_terminal")
    result = receipt.get("result")
    require(type(result) is dict and result.get("terminal_kind") == "MEMBER" and
            result.get("fixed_word_only") is True,
            "parent:result")
    a5 = result.get("a5")
    require(type(a5) is dict and a5.get("terminal_kind") == "MEMBER",
            "parent:a5")
    require(checkpoint.get("schema") == PARENT_CHECKPOINT_SCHEMA and
            checkpoint.get("source") == producer_id and
            checkpoint.get("static_bindings") == parent_bindings and
            checkpoint.get("owners") == receipt.get("owners") and
            checkpoint.get("a5_result") == a5 and
            checkpoint.get("a5_digest_sha256") == digest(a5),
            "parent:checkpoint_binding")
    expected_parent_phase = ("CANONICAL_ENDPOINT_ZERO_COMPLETE"
                             if result.get("canonical_M_only") is True else
                             "LIFT_NULL_MEMBER_COMPLETE")
    require(checkpoint.get("phase") == expected_parent_phase,
            "parent:checkpoint_terminal_phase")
    require(sidecar.get("schema") == PARENT_SIDECAR_SCHEMA and
            sidecar.get("status") == "ACCEPTED_A5_MEMBER" and
            sidecar.get("terminal") == "R07_ZERO_BASE_A5_A6_MEMBER" and
            sidecar.get("source") == producer_id and
            sidecar.get("static_bindings") == parent_bindings and
            sidecar.get("owners") == receipt.get("owners") and
            sidecar.get("a5_result") == a5,
            "parent:sidecar_binding")
    endpoint = result.get("endpoint_exact")
    require(type(endpoint) is dict and
            endpoint.get("full_C1_replay", {}).get("performed") is True,
            "parent:full_C1")
    for rank in (3, 4):
        rows = endpoint.get("complete_presentations", {}).get(
            "PB" + str(rank), {}).get("relators")
        require(type(rows) is list and
                [row.get("relator") for row in rows] ==
                task292.presentation_relators(rank),
                "parent:presentation:PB" + str(rank))
    for block in BLOCKS:
        full = endpoint["full_C1_replay"].get("blocks", {}).get(block)
        require(endpoint.get("endpoints", {}).get(block, {}).get("zero") is True and
                type(full) is dict and full.get("D1_z_zero") is True and
                full.get("D1_z_buckets") == [] and
                type(full.get("z_finite_support")) is list,
                "parent:z:" + block)
        for row in full["z_finite_support"]:
            representative = reduced(row.get("representative_word", []),
                                     len(task292.pure_pairs(RANK[block])))
            require(representative == row.get("representative_word") and
                    task292.exact_key(RANK[block], representative) ==
                    key_tuple(row.get("full_artin_key")),
                    "parent:z_artin_key:" + block)
        replay_chain = [{"component": row["component"],
                         "coefficient": row["coefficient_mod_3"],
                         "unreduced_group_word": row["representative_word"],
                         "free_reduced_group_word": row["representative_word"],
                         "full_artin_key": row["full_artin_key"],
                         "origin": {"kind": "task378_checker_parent_z"}}
                        for row in full["z_finite_support"]]
        d1 = task292.boundary_one(replay_chain, RANK[block],
                                  "task378_checker_D1_z")
        d1_support, _ = task292.collect_group(d1)
        require(not d1_support, "parent:D1_z_replay:" + block)
    parents = {"receipt": receipt_id, "verdict": verdict_id,
               "checkpoint": checkpoint_id, "a5_sidecar": sidecar_id,
               "producer_source": producer_id,
               "checker_authority": pin_value(PARENT_CHECKER_PIN),
               "driver_authority": pin_value(PARENT_DRIVER_PIN)}
    return endpoint, parents


def expected_graph_cells(block: str, support: list[dict[str, Any]],
                         task292: Any
                         ) -> tuple[set[str], set[tuple[str, int]], str]:
    rank = RANK[block]
    width = len(task292.pure_pairs(rank))
    vertices: set[str] = set()
    cells: set[tuple[str, int]] = set()

    def exact(word: Sequence[int]) -> str:
        return key_token(task292.exact_key(rank, reduced(word, width)))

    root = exact([])
    vertices.add(root)

    def add_positive(source_word: Sequence[int], component: int) -> None:
        source = exact(source_word)
        target = exact(reduced(list(source_word) + [component], width))
        vertices.add(source)
        vertices.add(target)
        cells.add((source, component))

    def add_path(word: Sequence[int]) -> None:
        cursor: list[int] = []
        for letter in reduced(word, width):
            if letter > 0:
                add_positive(cursor, letter)
            else:
                next_word = reduced(cursor + [letter], width)
                add_positive(next_word, -letter)
            cursor = reduced(cursor + [letter], width)

    for row in support:
        source_word = row["representative_word"]
        component = int(row["component"])
        add_path(source_word)
        add_path(reduced(source_word + [component], width))
        add_positive(source_word, component)
    return vertices, cells, root


def walk_uses_graph(word: Sequence[int], rank: int, task292: Any,
                    cells: set[tuple[str, int]]) -> None:
    width = len(task292.pure_pairs(rank))
    cursor: list[int] = []
    for letter in reduced(word, width):
        if letter > 0:
            coordinate = (key_token(task292.exact_key(rank, cursor)), letter)
        else:
            next_word = reduced(cursor + [letter], width)
            coordinate = (key_token(task292.exact_key(rank, next_word)), -letter)
        require(coordinate in cells, "graph:path_cell")
        cursor = reduced(cursor + [letter], width)


def audit_annotation_dag(public: dict[str, Any], relators: list[list[int]],
                         width: int, trace_root: int,
                         expected_entries: list[dict[str, Any]],
                         loop_word: list[int]) -> None:
    require(type(public) is dict and type(public.get("word_nodes")) is list and
            type(public.get("trace_nodes")) is list,
            "annotation_dag:shape")
    words = public["word_nodes"]
    nodes = public["trace_nodes"]
    for word in words:
        require(reduced(word, width) == word, "annotation_dag:word")

    def word(index: Any) -> list[int]:
        require(type(index) is int and 0 <= index < len(words),
                "annotation_dag:word_id")
        return words[index]

    def endpoints(index: Any) -> tuple[list[int], list[int]]:
        require(type(index) is int and 0 <= index < len(nodes),
                "annotation_dag:trace_id")
        return word(nodes[index].get("left_word")), word(nodes[index].get("right_word"))

    for index, row in enumerate(nodes):
        require(type(row) is dict and row.get("node_id") == index,
                "annotation_dag:node_order")
        left, right = endpoints(index)
        kind = row.get("kind")
        if kind == "empty":
            require(left == right, "annotation_dag:empty")
        elif kind == "atom":
            relator_index = int(row.get("relator_index"))
            sign = int(row.get("sign"))
            require(sign in (-1, 1) and
                    1 <= relator_index <= len(relators),
                    "annotation_dag:atom_roster")
            relator = relators[relator_index - 1]
            signed = relator if sign == 1 else inverse(relator)
            conjugator = word(row.get("conjugator_word"))
            require(product(left, inverse(right), width=width) ==
                    product(conjugator, signed, inverse(conjugator), width=width),
                    "annotation_dag:atom_invariant")
        elif kind == "context":
            child_id = int(row.get("child"))
            require(0 <= child_id < index, "annotation_dag:context_ancestry")
            child_left, child_right = endpoints(child_id)
            prefix, suffix = word(row.get("prefix_word")), word(row.get("suffix_word"))
            require(left == product(prefix, child_left, suffix, width=width) and
                    right == product(prefix, child_right, suffix, width=width),
                    "annotation_dag:context_invariant")
        elif kind == "reverse":
            child_id = int(row.get("child"))
            require(0 <= child_id < index, "annotation_dag:reverse_ancestry")
            child_left, child_right = endpoints(child_id)
            require(left == child_right and right == child_left,
                    "annotation_dag:reverse_invariant")
        elif kind == "concat":
            children = row.get("children")
            require(type(children) is list and children,
                    "annotation_dag:concat")
            require(all(type(child) is int and 0 <= child < index
                        for child in children),
                    "annotation_dag:concat_ancestry")
            for first, second in zip(children, children[1:]):
                require(endpoints(first)[1] == endpoints(second)[0],
                        "annotation_dag:concat_endpoint")
            require(left == endpoints(children[0])[0] and
                    right == endpoints(children[-1])[1],
                    "annotation_dag:concat_boundary")
        else:
            raise Reject("annotation_dag:kind")

    def flatten(index: int) -> list[dict[str, Any]]:
        require(0 <= index < len(nodes), "annotation_dag:flatten_root")
        output: list[dict[str, Any]] = []
        stack: list[tuple[int, list[int], bool]] = [(index, [], False)]
        while stack:
            current, outer_prefix, reversed_trace = stack.pop()
            row = nodes[current]
            kind = row["kind"]
            if kind == "empty":
                continue
            if kind == "atom":
                output.append({
                    "conjugator_word": product(
                        outer_prefix, word(row["conjugator_word"]), width=width),
                    "relator_index": int(row["relator_index"]),
                    "sign": int(row["sign"]) *
                            (-1 if reversed_trace else 1)})
                continue
            if kind == "context":
                prefix = product(outer_prefix, word(row["prefix_word"]),
                                 width=width)
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

    entries = flatten(trace_root)
    require(entries == expected_entries, "annotation_dag:flattened_trace")
    trace_word: list[int] = []
    for entry in entries:
        relator = relators[int(entry["relator_index"]) - 1]
        signed = relator if int(entry["sign"]) == 1 else inverse(relator)
        conjugator = reduced(entry["conjugator_word"], width)
        trace_word = product(trace_word, conjugator, signed,
                             inverse(conjugator), width=width)
    require(trace_word == reduced(loop_word, width),
            "annotation_dag:literal_loop_trace")
    root_left, root_right = endpoints(trace_root)
    require(root_left == reduced(loop_word, width) and root_right == [],
            "annotation_dag:root_boundary")


def collect_q_coordinates(block: str, cycles: list[dict[str, Any]],
                          task292: Any
                          ) -> tuple[dict[tuple[int, tuple], int],
                                     list[dict[str, Any]]]:
    rank = RANK[block]
    table: dict[tuple[int, tuple], int] = {}
    representative: dict[tuple[int, tuple], list[int]] = {}
    for cycle in cycles:
        cycle_coefficient = int(cycle["coefficient_mod_3"]) % MODULUS
        for entry in cycle["trace_entries"]:
            coefficient = cycle_coefficient * int(entry["sign"]) % MODULUS
            if not coefficient:
                continue
            relator_index = int(entry["relator_index"])
            word = reduced(entry["conjugator_word"],
                           len(task292.pure_pairs(rank)))
            key = task292.exact_key(rank, word)
            coordinate = (relator_index, key)
            table[coordinate] = (table.get(coordinate, 0) + coefficient) % MODULUS
            if coordinate not in representative:
                representative[coordinate] = word
            if not table[coordinate]:
                table.pop(coordinate)
    sources = [{"coefficient": coefficient,
                "left_word": representative[coordinate],
                "fox_word": task292.presentation_relators(rank)[coordinate[0] - 1],
                "provenance": "task378_checker_q"}
               for coordinate, coefficient in sorted(table.items(), key=repr)]
    return table, sources


def check_block(block: str, parent_block: dict[str, Any],
                produced: dict[str, Any], task292: Any) -> dict[str, Any]:
    rank = RANK[block]
    width = len(task292.pure_pairs(rank))
    relators = task292.presentation_relators(rank)
    support = parent_block["z_finite_support"]
    target = chain_map(support)
    require(produced.get("rank") == rank and
            chain_map(produced.get("z_finite_support")) == target,
            "block:z_binding:" + block)
    expected_vertices, expected_cells, root_token = expected_graph_cells(
        block, support, task292)
    graph = produced.get("graph")
    require(type(graph) is dict and type(graph.get("vertices")) is list and
            type(graph.get("edges")) is list and
            graph.get("vertex_count") == len(graph["vertices"]) and
            graph.get("edge_count") == len(graph["edges"]),
            "graph:shape:" + block)
    vertices = graph["vertices"]
    vertex_tokens: list[str] = []
    for index, row in enumerate(vertices):
        require(row.get("vertex_id") == index and
                reduced(row.get("representative_word", []), width) ==
                row.get("representative_word"),
                "graph:vertex:" + block)
        exact = task292.exact_key(rank, row["representative_word"])
        require(exact == key_tuple(row.get("full_artin_key")),
                "graph:vertex_key:" + block)
        vertex_tokens.append(key_token(exact))
    require(len(set(vertex_tokens)) == len(vertex_tokens) and
            set(vertex_tokens) == expected_vertices and
            vertex_tokens == sorted(vertex_tokens),
            "graph:vertex_roster:" + block)
    root = int(graph.get("root_vertex"))
    require(0 <= root < len(vertices) and vertex_tokens[root] == root_token,
            "graph:root:" + block)
    cells: set[tuple[str, int]] = set()
    edge_by_id: dict[int, dict[str, Any]] = {}
    for index, row in enumerate(graph["edges"]):
        require(row.get("edge_id") == index, "graph:edge_id:" + block)
        source, target_vertex = int(row["source_vertex"]), int(row["target_vertex"])
        component = int(row["component"])
        require(0 <= source < len(vertices) and
                0 <= target_vertex < len(vertices) and
                1 <= component <= width,
                "graph:edge_shape:" + block)
        source_word = reduced(row.get("source_word", []), width)
        source_key = task292.exact_key(rank, source_word)
        target_key = task292.exact_key(rank, source_word + [component])
        require(key_token(source_key) == vertex_tokens[source] and
                key_token(target_key) == vertex_tokens[target_vertex] and
                key_tuple(row["source_full_artin_key"]) == source_key and
                key_tuple(row["target_full_artin_key"]) == target_key,
                "graph:edge_action:" + block)
        coordinate = (vertex_tokens[source], component)
        require(coordinate not in cells, "graph:duplicate_cell:" + block)
        cells.add(coordinate)
        edge_by_id[index] = row
    require(cells == expected_cells, "graph:exact_finite_closure:" + block)
    support_paths = graph.get("support_paths")
    require(type(support_paths) is list and len(support_paths) == len(support),
            "graph:support_paths:" + block)
    for ordinal, (path_row, support_row) in enumerate(
            zip(support_paths, support), 1):
        source_word = reduced(support_row["representative_word"], width)
        component = int(support_row["component"])
        target_word = reduced(source_word + [component], width)
        require(path_row == {
            "support_ordinal": ordinal,
            "component": component,
            "source_word": source_word,
            "target_word": target_word,
            "source_full_artin_key": key_public(
                task292.exact_key(rank, source_word)),
            "target_full_artin_key": key_public(
                task292.exact_key(rank, target_word))},
            "graph:support_path_row:" + block)

    tree = produced.get("tree")
    require(type(tree) is dict and tree.get("deterministic_bfs") is True and
            type(tree.get("tree_edge_ids")) is list and
            type(tree.get("paths")) is list and
            len(tree["paths"]) == len(vertices),
            "tree:shape:" + block)
    tree_edges = set(int(value) for value in tree["tree_edge_ids"])
    require(len(tree_edges) == max(0, len(vertices) - 1) and
            all(value in edge_by_id for value in tree_edges),
            "tree:edge_count:" + block)
    deterministic_seen = {root}
    deterministic_queue: deque[int] = deque([root])
    deterministic_edges: set[int] = set()
    full_incidence: dict[int, list[tuple[int, int]]] = {
        index: [] for index in range(len(vertices))}
    for edge_id, edge in edge_by_id.items():
        source = int(edge["source_vertex"])
        target_vertex = int(edge["target_vertex"])
        full_incidence[source].append((edge_id, target_vertex))
        full_incidence[target_vertex].append((edge_id, source))
    while deterministic_queue:
        here = deterministic_queue.popleft()
        for edge_id, there in sorted(full_incidence[here]):
            if there in deterministic_seen:
                continue
            deterministic_seen.add(there)
            deterministic_edges.add(edge_id)
            deterministic_queue.append(there)
    require(deterministic_edges == tree_edges,
            "tree:deterministic_bfs:" + block)
    path_rows = {int(row["vertex_id"]): row for row in tree["paths"]}
    require(set(path_rows) == set(range(len(vertices))), "tree:path_roster:" + block)
    adjacency: dict[int, list[int]] = {index: [] for index in range(len(vertices))}
    for edge_id in tree_edges:
        edge = edge_by_id[edge_id]
        adjacency[int(edge["source_vertex"])].append(int(edge["target_vertex"]))
        adjacency[int(edge["target_vertex"])].append(int(edge["source_vertex"]))
    seen = {root}
    queue: deque[int] = deque([root])
    while queue:
        here = queue.popleft()
        for there in adjacency[here]:
            if there not in seen:
                seen.add(there)
                queue.append(there)
    require(len(seen) == len(vertices), "tree:connected:" + block)
    for vertex_id, row in path_rows.items():
        path_word = reduced(row.get("tree_path_word", []), width)
        require(path_word == row.get("tree_path_word") and
                vertices[vertex_id].get("tree_path_word") == path_word and
                task292.exact_key(rank, path_word) ==
                key_tuple(vertices[vertex_id]["full_artin_key"]),
                "tree:path_key:" + block)
        walk_uses_graph(path_word, rank, task292, cells)
        if vertex_id == root:
            require(row.get("parent_vertex") is None and
                    row.get("parent_edge") is None and
                    row.get("orientation") is None and path_word == [],
                    "tree:root_row:" + block)
        else:
            parent_vertex = int(row.get("parent_vertex"))
            edge_id = int(row.get("parent_edge"))
            orientation = int(row.get("orientation"))
            require(edge_id in tree_edges and orientation in (-1, 1),
                    "tree:parent_row:" + block)
            edge = edge_by_id[edge_id]
            if orientation == 1:
                require(int(edge["source_vertex"]) == parent_vertex and
                        int(edge["target_vertex"]) == vertex_id,
                        "tree:parent_orientation:" + block)
                letter = int(edge["component"])
            else:
                require(int(edge["target_vertex"]) == parent_vertex and
                        int(edge["source_vertex"]) == vertex_id,
                        "tree:parent_orientation:" + block)
                letter = -int(edge["component"])
            require(path_word == reduced(path_rows[parent_vertex]
                                         ["tree_path_word"] + [letter], width),
                    "tree:path_recursion:" + block)
    for edge_id, edge in edge_by_id.items():
        require(edge.get("tree_edge") is (edge_id in tree_edges),
                "tree:edge_flag:" + block)

    cycles = produced.get("cycles")
    non_tree = [edge_id for edge_id in edge_by_id if edge_id not in tree_edges]
    require(type(cycles) is list and len(cycles) == len(non_tree),
            "cycles:roster:" + block)
    decomposition_raw: list[dict[str, Any]] = []
    residual = dict(target)
    elimination_steps = []
    for cycle_index, (cycle, edge_id) in enumerate(zip(cycles, non_tree)):
        require(cycle.get("cycle_index") == cycle_index and
                int(cycle.get("edge_id")) == edge_id and
                cycle.get("trace_status") == "COMPLETE" and
                cycle.get("recursive_normal_form") == [] and
                cycle.get("literal_trace_equality") is True and
                cycle.get("faithful_artin_identity") is True,
                "cycle:envelope:" + block)
        edge = edge_by_id[edge_id]
        source, target_vertex = int(edge["source_vertex"]), int(edge["target_vertex"])
        loop_raw = (path_rows[source]["tree_path_word"] +
                    [int(edge["component"])] +
                    inverse(path_rows[target_vertex]["tree_path_word"]))
        loop = reduced(loop_raw, width)
        require(loop_raw == cycle.get("loop_word_unreduced") and
                loop == cycle.get("loop_word") and
                task292.exact_key(rank, loop) == task292.exact_key(rank, []) and
                key_tuple(cycle.get("loop_full_artin_key")) ==
                task292.exact_key(rank, []),
                "cycle:literal_loop:" + block)
        fox = task292.fox_expand(
            [{"coefficient": 1, "left_word": [], "fox_word": loop,
              "provenance": "task378_checker_cycle"}], rank,
            {"kind": "task378_checker_cycle", "block": block,
             "cycle_index": cycle_index})
        finite, _deleted = task292.collect_chain(fox)
        require(chain_map(finite) ==
                chain_map(cycle.get("cycle_finite_support")),
                "cycle:fox_chain:" + block)
        coordinate = (int(edge["component"]),
                      key_tuple(edge["source_full_artin_key"]))
        coefficient = target.get(coordinate, 0)
        require(int(cycle.get("coefficient_mod_3")) % MODULUS == coefficient,
                "cycle:coefficient:" + block)
        for chain_coordinate, value in chain_map(finite).items():
            next_value = (residual.get(chain_coordinate, 0) -
                          coefficient * value) % MODULUS
            if next_value:
                residual[chain_coordinate] = next_value
            else:
                residual.pop(chain_coordinate, None)
        elimination_steps.append({
            "cycle_index": cycle_index, "edge_id": edge_id,
            "coefficient_mod_3": coefficient,
            "residual_coordinates": [
                {"component": chain_coordinate[0],
                 "full_artin_key": key_public(chain_coordinate[1]),
                 "coefficient_mod_3": value}
                for chain_coordinate, value in sorted(residual.items(), key=repr)]})
        for row in finite:
            decomposition_raw.append({
                "component": row["component"],
                "coefficient": coefficient * row["coefficient_mod_3"],
                "unreduced_group_word": row["representative_word"],
                "free_reduced_group_word": row["representative_word"],
                "full_artin_key": row["full_artin_key"],
                "origin": {"kind": "task378_checker_decomposition",
                           "cycle_index": cycle_index}})
        entries = cycle.get("trace_entries")
        require(type(entries) is list, "cycle:trace_entries:" + block)
        for entry in entries:
            require(type(entry) is dict and int(entry.get("sign")) in (-1, 1) and
                    1 <= int(entry.get("relator_index")) <= len(relators) and
                    reduced(entry.get("conjugator_word", []), width) ==
                    entry.get("conjugator_word"),
                    "cycle:trace_entry:" + block)
        audit_annotation_dag(cycle.get("annotation_dag"), relators, width,
                             int(cycle.get("trace_root")), entries, loop)
    decomposed, _ = task292.collect_chain(decomposition_raw)
    require(not residual and chain_map(decomposed) == target and
            produced.get("decomposition", {}).get("equals_z") is True and
            chain_map(produced["decomposition"]["finite_support"]) == target and
            produced["decomposition"].get("tree_edge_elimination") ==
                elimination_steps,
            "cycle:complete_decomposition:" + block)

    accumulated = []
    for cycle in cycles:
        cycle_coefficient = int(cycle["coefficient_mod_3"]) % MODULUS
        for trace_index, entry in enumerate(cycle["trace_entries"]):
            coefficient = cycle_coefficient * int(entry["sign"]) % MODULUS
            if coefficient:
                relation_index = int(entry["relator_index"])
                accumulated.append({
                    "coefficient": coefficient,
                    "left_word": list(entry["conjugator_word"]),
                    "relator_index": relation_index,
                    "fox_word": relators[relation_index - 1],
                    "provenance": "task378_cycle_trace",
                    "cycle_index": int(cycle["cycle_index"]),
                    "trace_index": trace_index})
    require(produced.get("q_accumulator_sources") == accumulated,
            "q:checkpoint_accumulator:" + block)
    q_coordinates, fox_sources = collect_q_coordinates(block, cycles, task292)
    producer_q = produced.get("q")
    require(type(producer_q) is dict and
            producer_q.get("original_relator_roster_only") is True and
            producer_q.get("uncollected_sources") == accumulated,
            "q:envelope:" + block)
    got_q: dict[tuple[int, tuple], int] = {}
    for row in producer_q.get("finite_support", []):
        word = reduced(row.get("representative_word", []), width)
        key = task292.exact_key(rank, word)
        require(key == key_tuple(row.get("full_artin_key")),
                "q:source_key:" + block)
        coordinate = (int(row.get("relator_index")), key)
        coefficient = int(row.get("coefficient_mod_3")) % MODULUS
        require(coefficient in (1, 2) and coordinate not in got_q,
                "q:coordinate:" + block)
        got_q[coordinate] = coefficient
    require(got_q == q_coordinates, "q:independent_collection:" + block)
    d2_raw = task292.fox_expand(
        fox_sources, rank, {"kind": "task378_checker_D2_q", "block": block})
    d2_support, _ = task292.collect_chain(d2_raw)
    require(chain_map(d2_support) == target and
            produced.get("D2_replay", {}).get("equals_z") is True and
            produced["D2_replay"].get("coordinate_key") ==
            "(component,full_artin_key)" and
            chain_map(produced["D2_replay"]["finite_support"]) == target and
            chain_map(produced["D2_replay"]["target_z"]) == target,
            "D2_q_equals_z:" + block)
    return {"rank": rank, "vertices": len(vertices),
            "edges": len(edge_by_id), "cycles": len(cycles),
            "trace_entries": sum(len(cycle["trace_entries"])
                                 for cycle in cycles),
            "q_coordinates": len(q_coordinates),
            "D2_q_equals_z": True}


def check(args: argparse.Namespace) -> dict[str, Any]:
    producer_source = check_pin(PRODUCER_PIN, "producer")
    for label, pin in (("parent:producer", PARENT_PRODUCER_PIN),
                       ("parent:checker", PARENT_CHECKER_PIN),
                       ("parent:driver", PARENT_DRIVER_PIN),
                       ("task292:producer", TASK292_PIN),
                       ("task292:checker", TASK292_CHECKER_PIN)):
        check_pin(pin, label)
    task292 = load_pinned(TASK292_CHECKER_PIN, "task378_task292_checker")
    task292.CHECK_BUDGET = task292.CheckerBudget()
    endpoint, parents = authenticate_parent(args, task292)
    receipt, receipt_id = read_json(args.receipt, "producer_receipt",
                                    ("ci/out",))
    check_seal(receipt, "producer_receipt")
    require(receipt.get("schema") == SCHEMA and
            receipt.get("status") == "COMPLETE" and
            receipt.get("terminal") == MEMBER and
            receipt.get("mode") == "PRODUCTION" and
            receipt.get("source") == producer_source and
            receipt.get("static_bindings") == static_bindings() and
            receipt.get("parents") == parents,
            "producer:member_envelope")
    claims = receipt.get("claims", {})
    require(claims == {"A8": "MEMBER", "fixed_word_only": True,
                       "A9": "NONE", "compatible_lift": "NONE",
                       "mixed_prime": "NONE", "perfect_core": "NONE",
                       "fake": "NONE", "Ihara": "NONE"},
            "producer:claim_scope")
    checkpoint, checkpoint_id = read_json(args.checkpoint,
                                          "producer_checkpoint",
                                          ("ci/out",))
    check_seal(checkpoint, "producer_checkpoint")
    require(receipt.get("artifacts", {}).get("checkpoint") == checkpoint_id and
            checkpoint.get("schema") == CHECKPOINT_SCHEMA and
            checkpoint.get("phase") == "COMPLETE" and
            checkpoint.get("source") == producer_source and
            checkpoint.get("static_bindings") == static_bindings() and
            checkpoint.get("parents") == parents and
            checkpoint.get("resume_contract") == {
                "all_or_none_path_bytes_sha256": True,
                "four_parent_artifacts_bound": True,
                "exact_artin_keys_recomputed": True,
                "relator_words_recomputed": True,
                "annotation_dag_only": True,
                "no_unauthenticated_python_objects": True},
            "checkpoint:binding")
    result = receipt.get("result")
    require(type(result) is dict and result.get("parent_terminal") == PARENT_MEMBER and
            result.get("task292_terminal") == task292.ZERO and
            result.get("fixed_word_only") is True and
            result.get("compiler_theorems") == {
                "finite_fundamental_cycle_decomposition": True,
                "annotated_recursive_PB_combing": True,
                "original_task292_relators_only": True,
                "direct_D2_q_equals_z": True},
            "producer:result_scope")
    blocks = result.get("blocks")
    require(type(blocks) is dict and set(blocks) == set(BLOCKS) and
            checkpoint.get("state", {}).get("blocks") == blocks and
            checkpoint.get("state", {}).get("phase") == "COMPLETE" and
            checkpoint.get("state", {}).get("active_combing") is None,
            "checkpoint:complete_state")
    replay = {}
    for block in BLOCKS:
        replay[block] = check_block(
            block, endpoint["full_C1_replay"]["blocks"][block],
            blocks[block], task292)
    return seal({"schema": VERDICT_SCHEMA, "status": "ACCEPTED",
                 "terminal": MEMBER, "accepted": True, "independent": True,
                 "source": source_identity(), "producer": producer_source,
                 "receipt": receipt_id, "checkpoint": checkpoint_id,
                 "parents": parents, "block_replays": replay,
                 "task292_checker": pin_value(TASK292_CHECKER_PIN),
                 "producer_imported": False,
                 "claims": {"A8": "MEMBER", "fixed_word_only": True,
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
    ap.add_argument("--receipt", required=True)
    ap.add_argument("--checkpoint", required=True)
    ap.add_argument("--output", required=True)
    return ap


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        verdict = check(args)
        write_exclusive(args.output, verdict)
        print("R07_ENDPOINT_ZERO_ANNOTATED_BOUNDARY_V1_CHECKER terminal=" +
              MEMBER, flush=True)
        return 0
    except Exception as exc:
        print("R07_ENDPOINT_ZERO_ANNOTATED_BOUNDARY_V1_CHECKER_ERROR " +
              str(exc), flush=True)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
