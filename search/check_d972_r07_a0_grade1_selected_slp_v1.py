#!/usr/bin/env python3
"""Independent compact parser and replay for the selected SLP payload."""
from __future__ import annotations

import argparse
import gc
import hashlib
import importlib.util
import json
import os
import struct
import sys
import time
from pathlib import Path

import numpy as np

try:
    import resource
except ImportError:
    resource = None


ROOT = Path(__file__).resolve().parents[1]
MARKER = "R07_GRADE1_SELECTED_SLP_V1_CHECKER_PASS"
BODY_SHA = "62412762b3a208d31febb6c6b8d4707f880471ed32cf62c79c18108065ab7b5d"
PREPARE_SHA = "1f191d88a0453360021ec57d253a7d16c9a66ac059ddaaadb6db3e2b9293c865"
BASIS_SHA = "b562c980c22a25a932bae1b548f72aeede5637b9612afc908fff9a9aecff069d"
REMAINDER_SHA = "564cbfafc869a8c6eb761a392caa5e792b546bf577af7fe808177b2fdf13cbb0"
V3_SHA = "bf872b30149e1351762b243d590d7a1f876e048b92a053d8f9c17bba5c45bcff"
ROUTER_PATH = ROOT / "crosscheck/check_d972_r07_a0_first_rung_grade1_full_routing_v2.py"
ROUTER_SHA = "a0504ae6a2562aab3b9af5ba7ed672bcc87bbd1cfdf5cc9fd3489240e51008e3"
WIDTH = 24192
GRADE_BYTES = WIDTH // 4
LOWER_WIDTH = 8068
LOWER_BYTES = LOWER_WIDTH // 4
GRADE = 5044
LOWER = 1661
NODE = struct.Struct("<IBQIQI")
EDGE = struct.Struct("<HB")
LEAF_MAGIC = b"R07LEAF1"
LEAF_VERSION = 1
LEAF_SCHEMA = "d972.r07.a0.literal-leaves.v1"
LEAF_HEADER = struct.Struct("<8sBBBB32sQ")
LEAF_RECORD = struct.Struct("<IIBI")
PURE_Q1_WORDS = {
    (0, 0): (),
    (0, 1): (-2, -2, -2, -2, -2, -2, -2, -2, -2),
    (1, 0): (-2, -2, 1, 1, 2, 1, 2, 1, 1),
    (1, 1): (-2, -2, -2, -1, -2, -1, -1, -1, -2, -1),
}
ACTORS = (1, -1, 2, -2)
CHARACTERS = ((0, 0), (0, 1), (1, 0), (1, 1))
TRITS = np.asarray(
    [[(value // 3**digit) % 3 for digit in range(4)] for value in range(81)],
    dtype=np.uint8,
)
WEIGHTS = np.asarray((1, 3, 9, 27), dtype=np.uint16)
AXPY = np.zeros((3, 81, 81), dtype=np.uint8)
for coefficient in range(3):
    for left in range(81):
        for right in range(81):
            AXPY[coefficient, left, right] = int(
                np.dot(
                    (
                        TRITS[left].astype(np.int16)
                        - coefficient * TRITS[right].astype(np.int16)
                    )
                    % 3,
                    WEIGHTS,
                )
            )
SCALE2 = np.asarray(
    [int(np.dot((2 * TRITS[value]) % 3, WEIGHTS)) for value in range(81)],
    dtype=np.uint8,
)

_STARTED = time.monotonic()
_LAST_PHASE = "startup"
_LAST_RSS = 0
_LAST_PEAK = 0
_LAST_CURSORS: dict[str, int | str] = {}
_EMERGENCY: bytearray | None = bytearray(64 * 1024)


def sha(data) -> str:
    return hashlib.sha256(data).hexdigest()


def canon(value) -> bytes:
    return (
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
        + "\n"
    ).encode("ascii")


def fail(reason: str) -> None:
    raise RuntimeError(reason)


def current_rss() -> int:
    if sys.platform.startswith("linux"):
        try:
            fields = Path("/proc/self/statm").read_text(encoding="ascii").split()
            return int(fields[1]) * int(os.sysconf("SC_PAGE_SIZE"))
        except (OSError, ValueError, IndexError):
            return 0
    return 0


def peak_rss() -> int:
    if resource is None:
        return 0
    value = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    return value * 1024 if sys.platform.startswith("linux") else value


def phase(name: str, **cursors: int | str) -> None:
    global _LAST_PHASE, _LAST_RSS, _LAST_PEAK, _LAST_CURSORS
    _LAST_PHASE = name
    _LAST_RSS = current_rss()
    _LAST_PEAK = peak_rss()
    _LAST_CURSORS = dict(cursors)
    record = {
        "phase": name,
        "elapsed_seconds": round(time.monotonic() - _STARTED, 6),
        "rss_bytes": _LAST_RSS,
        "peak_rss_bytes": _LAST_PEAK,
    }
    record.update(cursors)
    os.write(2, canon(record))


def emergency_unknown_resource() -> None:
    global _EMERGENCY
    _EMERGENCY = None
    try:
        cursors = ",".join(
            "%s=%s" % (key, _LAST_CURSORS[key]) for key in sorted(_LAST_CURSORS)
        )
        message = (
            "UNKNOWN_RESOURCE MemoryError phase=%s rss=%d peak=%d cursors=%s\n"
            % (_LAST_PHASE, _LAST_RSS, _LAST_PEAK, cursors)
        ).encode("ascii", "replace")[:1024]
        os.write(2, message)
    except BaseException:
        try:
            os.write(2, b"UNKNOWN_RESOURCE MemoryError\n")
        except BaseException:
            pass


def guard(started: float) -> None:
    if time.monotonic() - started > float(os.environ.get("TASK601_SECONDS", "2400")):
        fail("UNKNOWN_RESOURCE:time")
    if peak_rss() > int(os.environ.get("TASK601_MAX_RSS", str(7 * 1024**3))):
        fail("UNKNOWN_RESOURCE:rss")


def same_bytes(left, right) -> bool:
    return memoryview(left).cast("B") == memoryview(right).cast("B")


class NodeView:
    def __init__(self, data):
        self.data = memoryview(data).cast("B")
        if len(self.data) % NODE.size:
            fail("node_record_size")

    def __len__(self):
        return len(self.data) // NODE.size

    def __getitem__(self, index: int):
        if not 0 <= index < len(self):
            raise IndexError(index)
        return NODE.unpack_from(self.data, index * NODE.size)


class EdgeView:
    def __init__(self, data):
        self.data = memoryview(data).cast("B")
        if len(self.data) % EDGE.size:
            fail("edge_record_size")

    def __len__(self):
        return len(self.data) // EDGE.size

    def __getitem__(self, index: int):
        if not 0 <= index < len(self):
            raise IndexError(index)
        return EDGE.unpack_from(self.data, index * EDGE.size)


class RowView:
    def __init__(self, data, width: int, count: int, label: str):
        self.data = memoryview(data).cast("B")
        self.width = width
        self.count = count
        self.label = label
        if len(self.data) != width * count:
            fail(label + "_size")
        if len(self.data) and int(np.frombuffer(self.data, dtype=np.uint8).max()) > 80:
            fail(label + "_noncanonical")

    def __len__(self):
        return self.count

    def __getitem__(self, index: int):
        if not 0 <= index < self.count:
            raise IndexError(index)
        start = index * self.width
        return self.data[start : start + self.width]


def bits(data, count: int) -> list[bool]:
    raw = memoryview(data).cast("B")
    if len(raw) != (count + 7) // 8:
        fail("bitset_size")
    if count % 8 and raw[-1] >> (count % 8):
        fail("bitset_padding")
    return [bool(raw[index // 8] & (1 << (index % 8))) for index in range(count)]


def packed_axpy(work: np.ndarray, coefficient: int, pivot) -> None:
    pivot_array = np.frombuffer(pivot, dtype=np.uint8)
    if pivot_array.shape != work.shape:
        fail("packed_axpy_shape")
    work[:] = AXPY[int(coefficient), work, pivot_array]


def word_mul(*words) -> tuple[int, ...]:
    output = []
    for word in words:
        for letter in word:
            letter = int(letter)
            if output and output[-1] == -letter:
                output.pop()
            else:
                output.append(letter)
    return tuple(output)


def cv(label, first: int, second: int) -> int:
    return 1 if ((label[0] * first + label[1] * second) & 1) == 0 else 2


def require_false_claim_flags(value: dict, label: str) -> None:
    required = {
        "direct_occurrence_replay": False,
        "next_degree2_residual": None,
        "cross_checked": False,
        "verified": False,
        "A0": False,
        "COMMON": False,
        "FAKE": False,
        "IHARA": False,
    }
    if any(key not in value or value[key] is not expected for key, expected in required.items()):
        fail(label + "_claim_flags")


def load_candidate(directory: Path):
    head_raw = (directory / "decision-v2.HEAD").read_bytes()
    head = json.loads(head_raw)
    if (
        sha(head_raw)
        != "07de7a817e8c5ae2e7346402a290c32631d05b0cc621d03702faa6cb43a948c0"
        or head.get("body_sha256") != BODY_SHA
        or canon(head) != head_raw
    ):
        fail("candidate_head")
    body_raw = (directory / f"decision-v2.{BODY_SHA}.json").read_bytes()
    body = json.loads(body_raw)
    if (
        sha(body_raw) != BODY_SHA
        or canon(body) != body_raw
        or body.get("terminal") != "GRADE1_DECISION_MEMBER"
        or body.get("grade_rank") != GRADE
        or body.get("lower_rank") != LOWER
        or len(body.get("member_coefficients", [])) != 3317
    ):
        fail("candidate_body")
    basis_receipt = body.get("basis_receipt", {})
    remainder_receipt = body.get("remainder_receipt", {})
    basis = (directory / basis_receipt["file"]).read_bytes()
    remainder = (directory / remainder_receipt["file"]).read_bytes()
    if (
        len(basis) != GRADE * GRADE_BYTES
        or sha(basis) != BASIS_SHA
        or len(remainder) != GRADE_BYTES
        or sha(remainder) != REMAINDER_SHA
        or sha(remainder) != remainder_receipt.get("sha256")
    ):
        fail("candidate_blobs")
    return body, basis, remainder


def load_prepare_and_residual(state: Path):
    head_raw = (state / "prepare.HEAD").read_bytes()
    head = json.loads(head_raw)
    if (
        head.get("body_sha256") != PREPARE_SHA
        or head.get("stem") != "prepare"
        or head.get("parent_sha256") is not None
        or canon(head) != head_raw
    ):
        fail("prepare_head")
    body_raw = (state / f"prepare.{PREPARE_SHA}.json").read_bytes()
    prepare = json.loads(body_raw)
    if sha(body_raw) != PREPARE_SHA or canon(prepare) != body_raw:
        fail("prepare_body")
    receipt = prepare.get("residual_blob", {})
    residual = (state / receipt.get("file", "")).read_bytes()
    if (
        len(residual) != GRADE_BYTES
        or sha(residual) != receipt.get("sha256")
    ):
        fail("residual_auth")
    return prepare, residual


def sealed_body(state: Path, stem: str, digest: str):
    raw = (state / f"{stem}.{digest}.json").read_bytes()
    if sha(raw) != digest:
        fail("source_body_auth")
    body = json.loads(raw)
    if canon(body) != raw:
        fail("source_body_auth")
    return body


def compare_root_binding(roots, member_roots) -> None:
    expected = [
        {
            "kind": "grade",
            "ids": [int(item["pivot"])],
            "prefix": [],
            "coefficient": int(item["coefficient"]),
        }
        for item in member_roots
    ]
    if roots != expected:
        fail("typed_root_binding")


def validate_derived_metadata(derived) -> dict:
    expected_leaf_metadata = {
        "file": "literal-leaves.bin",
        "schema": LEAF_SCHEMA,
        "quotient_specific_evaluation": True,
        "common_source_witness": False,
        "states_exported": False,
    }
    if (
        not isinstance(derived, dict)
        or derived.get("schema") != "d972.r07.a0.selected-literal-derived.v2"
        or derived.get("leaf_receipt") != expected_leaf_metadata
        or set(derived) != {"schema", "leaf_receipt"}
        or "states" in derived
        or "literal_leaves" in derived
    ):
        fail("derived_compact_schema")
    return expected_leaf_metadata


def validate_ancestry(
    ancestry: dict,
    refs: list,
    coefficients: list,
    declared_grade: list[bool],
    declared_lower: list[bool],
):
    if ancestry.get("schema") != "d972.r07.a0.selected-ancestry.v3":
        fail("source_ancestry_schema")
    if ancestry.get("selected_refs") != refs:
        fail("source_ancestry_refs")
    expected_leaf_metadata = validate_derived_metadata(ancestry.get("derived"))
    structure = ancestry.get("structure")
    if (
        not isinstance(structure, dict)
        or structure.get("schema") != "d972.r07.a0.selected-slp-structure.v2"
        or structure.get("syntax_contract")
        != ["origin", "ordered_signed_reductions", "scale_power"]
    ):
        fail("source_structure_schema")
    expected_member = [
        {"pivot": int(pivot), "coefficient": int(coefficient)}
        for pivot, coefficient in coefficients
    ]
    if (
        structure.get("member_roots") != expected_member
        or structure.get("grade_selected")
        != [index for index, selected in enumerate(declared_grade) if selected]
        or structure.get("lower_selected")
        != [index for index, selected in enumerate(declared_lower) if selected]
    ):
        fail("source_structure_closure")
    roots = ancestry.get("roots")
    if not isinstance(roots, list):
        fail("typed_roots")
    compare_root_binding(roots, expected_member)

    source_items = structure.get("source_nodes")
    defect_items = structure.get("defect_nodes")
    expression_items = structure.get("expressions")
    if not all(isinstance(value, list) for value in (source_items, defect_items, expression_items)):
        fail("source_structure_groups")
    source_keys = [item.get("key") for item in source_items if isinstance(item, dict)]
    defect_keys = [item.get("key") for item in defect_items if isinstance(item, dict)]
    expression_keys = [item.get("key") for item in expression_items if isinstance(item, dict)]
    if (
        len(source_keys) != len(source_items)
        or len(defect_keys) != len(defect_items)
        or len(expression_keys) != len(expression_items)
        or source_keys != sorted(source_keys)
        or defect_keys != sorted(defect_keys)
        or expression_keys != sorted(expression_keys)
        or len(source_keys) != len(set(source_keys))
        or len(defect_keys) != len(set(defect_keys))
        or len(expression_keys) != len(set(expression_keys))
        or set(source_keys) & set(defect_keys)
    ):
        fail("source_structure_identity")
    source_map = dict(zip(source_keys, source_items))
    defect_map = dict(zip(defect_keys, defect_items))
    expression_map = dict(zip(expression_keys, expression_items))
    present = set(source_map) | set(defect_map)
    for item_map in (source_map, defect_map):
        for key, item in item_map.items():
            if item.get("kind") != key.split(":", 1)[0]:
                fail("source_structure_kind")
            children = item.get("children")
            if (
                not isinstance(children, list)
                or any(
                    not isinstance(child, str) or child not in present
                    for child in children
                )
            ):
                fail("source_structure_dependency")
    if any(
        not key.startswith(("seed:", "actor:"))
        for key in expression_map
    ):
        fail("source_expression_identity")

    words_path = ROOT / "scratchpad/a0_paper_words_v1.json"
    words_raw = words_path.read_bytes()
    words = json.loads(words_raw.decode("utf-8"))
    literal = structure.get("literal_dictionary", {})
    if literal != {
        "schema": "d972.r07.a0.literal-dictionary.v1",
        "source_file": "scratchpad/a0_paper_words_v1.json",
        "source_sha256": sha(words_raw),
        "relators_sha256": words.get("relators_sha256"),
        "relators": words["relators"],
        "pure_q1_words": {str(key): list(value) for key, value in PURE_Q1_WORDS.items()},
        "literal_actor_words": {
            "x": [1],
            "x_inverse": [-1],
            "y": [2],
            "y_inverse": [-2],
        },
    }:
        fail("literal_dictionary_binding")
    return structure, source_map, defect_map, expression_map, expected_leaf_metadata


def validate_physical_streams(
    loaded: dict,
    grade_nodes: NodeView,
    lower_nodes: NodeView,
    grade_edges: EdgeView,
    lower_edges: EdgeView,
    basis: bytes,
    declared_grade: list[bool],
    declared_lower: list[bool],
):
    for index in range(len(grade_edges)):
        if grade_edges[index][1] not in (1, 2):
            fail("grade_edge_coefficient")
    for index in range(len(lower_edges)):
        if lower_edges[index][1] not in (1, 2):
            fail("lower_edge_coefficient")
    for pivot in range(len(grade_nodes)):
        _, scale, edge_start, edge_count, lower_start, lower_count = grade_nodes[pivot]
        if (
            scale not in (1, 2)
            or edge_start + edge_count > len(grade_edges)
            or lower_start + lower_count > len(lower_edges)
        ):
            fail("grade_node")
        for index in range(edge_start, edge_start + edge_count):
            if grade_edges[index][0] >= pivot:
                fail("grade_acyclic")
    for pivot in range(len(lower_nodes)):
        _, scale, edge_start, edge_count, _, _ = lower_nodes[pivot]
        if scale not in (1, 2) or edge_start + edge_count > len(lower_edges):
            fail("lower_node")
        for index in range(edge_start, edge_start + edge_count):
            if lower_edges[index][0] >= pivot:
                fail("lower_acyclic")

    grade_origins = RowView(loaded["grade_origins"], GRADE_BYTES, GRADE, "grade_origins")
    lower_origins = RowView(loaded["lower_origins"], LOWER_BYTES, LOWER, "lower_origins")
    lower_stored = RowView(loaded["lower_stored"], LOWER_BYTES, LOWER, "lower_stored")
    lower_companions = RowView(
        loaded["lower_companions"], GRADE_BYTES, LOWER, "lower_companions"
    )
    old_zero_raw = loaded["old_lower_zero"]
    if len(old_zero_raw) % LOWER_BYTES:
        fail("old_lower_zero_size")
    old_zero_count = len(old_zero_raw) // LOWER_BYTES
    old_lower_zero = RowView(
        old_zero_raw, LOWER_BYTES, old_zero_count, "old_lower_zero"
    )
    for index in range(len(old_lower_zero)):
        if any(old_lower_zero[index]):
            fail("old_origin_lower_nonzero")
    basis_rows = RowView(basis, GRADE_BYTES, GRADE, "candidate_basis")

    for pivot, selected in enumerate(declared_lower):
        if not selected:
            continue
        work = np.frombuffer(lower_origins[pivot], dtype=np.uint8).copy()
        _, scale, edge_start, edge_count, _, _ = lower_nodes[pivot]
        for edge_index in range(edge_start, edge_start + edge_count):
            earlier, coefficient = lower_edges[edge_index]
            packed_axpy(work, coefficient, lower_stored[earlier])
        if scale == 2:
            work[:] = SCALE2[work]
        if not same_bytes(work, lower_stored[pivot]):
            fail("lower_origin_replay")

    for pivot, selected in enumerate(declared_grade):
        if not selected:
            continue
        work = np.frombuffer(grade_origins[pivot], dtype=np.uint8).copy()
        _, scale, edge_start, edge_count, _, _ = grade_nodes[pivot]
        for edge_index in range(edge_start, edge_start + edge_count):
            earlier, coefficient = grade_edges[edge_index]
            packed_axpy(work, coefficient, basis_rows[earlier])
        if scale == 2:
            work[:] = SCALE2[work]
        if not same_bytes(work, basis_rows[pivot]):
            fail("grade_origin_replay")
    if any(declared_lower[index] and index >= len(lower_stored) for index in range(LOWER)):
        fail("selected_lower_replay")
    return {
        "grade_origins": grade_origins,
        "lower_origins": lower_origins,
        "lower_stored": lower_stored,
        "lower_companions": lower_companions,
        "old_lower_zero": old_lower_zero,
        "basis": basis_rows,
    }


def expected_old_ref(prepare: dict, logical: int, character: int, pivot: int) -> dict:
    item = prepare["old_blocks"][character]
    record = item["record"]
    node = record["dag_nodes"][pivot]
    origin = node["origin"]
    seed = int(origin["seed"]) if origin["kind"] == "projected_seed" else None
    return {
        "logical": logical,
        "kind": "old",
        "character": character,
        "pivot": pivot,
        "old_dag_node": node,
        "defect_origin_range": item.get("defect_origin_range"),
        "seed_index": seed,
        "seed_reduction": record["seed_reductions"][seed - 1] if seed is not None else None,
        "ancestry_key": f"old:{character}:{pivot}",
    }


def selected_source_graph_replay(
    state: Path,
    prepare: dict,
    block_digests: list[str],
    refs: list,
    source_map: dict,
    defect_map: dict,
    expression_map: dict,
    grade_nodes: NodeView,
    lower_nodes: NodeView,
    grade_edges: EdgeView,
    lower_edges: EdgeView,
    physical: dict,
):
    v3_path = ROOT / "search/d972_r07_a0_first_rung_grade1_v3.py"
    if sha(v3_path.read_bytes()) != V3_SHA:
        fail("source_replay_v3_hash")
    module_spec = importlib.util.spec_from_file_location("sealed_v3", v3_path)
    if module_spec is None or module_spec.loader is None:
        fail("source_replay_loader")
    v3 = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(v3)
    context = v3.context_for_state(prepare)
    refs_by_character = {index: [] for index in range(4)}
    logical_seen = set()
    ancestry_seen = set()
    for ref in refs:
        if not isinstance(ref, dict):
            fail("source_ref_shape")
        logical = int(ref.get("logical", -1))
        ancestry_key = ref.get("ancestry_key")
        if logical in logical_seen or ancestry_key in ancestry_seen:
            fail("source_ref_identity")
        logical_seen.add(logical)
        ancestry_seen.add(ancestry_key)
        if ref.get("kind") == "old":
            character = int(ref.get("character", -1))
        elif ref.get("kind") == "block":
            character = int(ref.get("block", -1))
        else:
            fail("source_ref_kind")
        if character not in range(4):
            fail("source_ref_character")
        refs_by_character[character].append(ref)

    lower_by_logical = {
        int(lower_nodes[index][0]): index for index in range(len(lower_nodes))
    }
    grade_by_logical = {
        int(grade_nodes[index][0]): index for index in range(len(grade_nodes))
    }
    expected_source = set()
    expected_defects = set()
    expected_expressions = set()

    def match(mapping: dict, key: str, expected: dict, reason: str) -> None:
        if mapping.get(key) != expected:
            fail(reason)

    def expect_old(character: int, roots) -> None:
        record = prepare["old_blocks"][character]["record"]
        todo = [int(value) for value in roots]
        while todo:
            pivot = todo.pop()
            key = f"old:{character}:{pivot}"
            if key in expected_source:
                continue
            node = record["dag_nodes"][pivot]
            origin = node["origin"]
            children = []
            if origin["kind"] == "actor":
                parent = int(origin["parent"])
                children.append(f"old:{character}:{parent}")
                todo.append(parent)
            for earlier, _ in node["reductions"]:
                earlier = int(earlier)
                children.append(f"old:{character}:{earlier}")
                todo.append(earlier)
            expected = {
                "key": key,
                "kind": "old",
                "character": character,
                "pivot": pivot,
                "node": node,
                "children": children,
                "expression_key": None,
                "syntax": {
                    "origin": origin,
                    "reductions": [
                        {"pivot": int(q), "coefficient": int(c)}
                        for q, c in node["reductions"]
                    ],
                    "scale": int(node["scale"]),
                },
            }
            match(source_map, key, expected, "source_structure_node_exact")
            expected_source.add(key)

    def expect_defect(source_block: int, origin_index: int) -> str:
        key = f"defect:{origin_index}"
        if key in expected_defects:
            return key
        origin = prepare["defect_origins"][origin_index]
        character = int(origin["lower_character"])
        record = prepare["old_blocks"][character]["record"]
        if origin["kind"] == "seed":
            seed = int(origin["seed"])
            expression = record["seed_reductions"][seed - 1]
            expression_key = f"seed:{character}:{seed}"
            expected_expression = {
                "key": expression_key,
                "kind": "seed_reduction",
                "character": character,
                "seed": seed,
                "expression": expression,
            }
            old_roots = [int(q) for q, _ in expression]
        elif origin["kind"] == "transition":
            pivot = int(origin["pivot"])
            letter = int(origin["letter"])
            expression = record["actor_transitions"][pivot][ACTORS.index(letter)]
            expression_key = f"actor:{character}:{pivot}:{letter}"
            expected_expression = {
                "key": expression_key,
                "kind": "actor_transition_expression",
                "character": character,
                "pivot": pivot,
                "letter": letter,
                "expression": expression,
            }
            old_roots = [pivot] + [int(q) for q, _ in expression]
        else:
            fail("source_expected_defect_origin")
        match(
            expression_map,
            expression_key,
            expected_expression,
            "source_structure_expression_exact",
        )
        expected_expressions.add(expression_key)
        children = []
        if origin["kind"] == "transition":
            children.append(f"old:{character}:{int(origin['pivot'])}")
        children.extend(f"old:{character}:{int(q)}" for q, _ in expression)
        expected = {
            "key": key,
            "kind": "defect",
            "source_block": source_block,
            "origin": origin,
            "children": children,
            "expression_key": expression_key,
        }
        match(defect_map, key, expected, "source_structure_defect_exact")
        expected_defects.add(key)
        expect_old(character, old_roots)
        return key

    for character in range(4):
        character_refs = sorted(
            refs_by_character[character], key=lambda item: int(item["logical"])
        )
        old_refs = [ref for ref in character_refs if ref["kind"] == "old"]
        block_refs = [ref for ref in character_refs if ref["kind"] == "block"]
        for ref in old_refs:
            logical = int(ref["logical"])
            pivot = int(ref["pivot"])
            if ref != expected_old_ref(prepare, logical, character, pivot):
                fail("source_old_binding")
            expect_old(character, [pivot])

        if old_refs:
            item = prepare["old_blocks"][character]
            rank = int(item["rank"])
            low_raw = v3.read_blob(state, item["lower_basis_blob"])
            lift_raw = v3.read_blob(state, item["lifted_grade_blob"])
            low = np.frombuffer(low_raw, dtype=np.uint8).reshape(
                rank, v3.LOWER_ECHELON_WIDTH // 4
            )
            lift = np.frombuffer(lift_raw, dtype=np.uint8).reshape(
                rank, v3.SOURCE_TOTAL_WIDTH // 4
            )
            for ref in old_refs:
                logical = int(ref["logical"])
                pivot = int(ref["pivot"])
                lower_pivot = lower_by_logical.get(logical)
                grade_pivot = grade_by_logical.get(logical)
                if (lower_pivot is None) == (grade_pivot is None):
                    fail("source_physical_origin_kind")
                lower_row = v3.unpack_trits(low[pivot], v3.LOWER_ECHELON_WIDTH)
                occurrence_lower = np.zeros(
                    (4, v3.SOURCE_BASE_WIDTH), dtype=np.uint8
                )
                occurrence_lower[character] = lower_row[: v3.SOURCE_BASE_WIDTH]
                occurrence_grade = v3.unpack_trits(
                    lift[pivot], v3.SOURCE_TOTAL_WIDTH
                ).reshape(4, v3.SOURCE_BLOCK_WIDTH)
                source_lower, source_grade = v3.aggregate_pair(
                    context,
                    occurrence_lower,
                    occurrence_grade,
                    lower_row[v3.SOURCE_BASE_WIDTH :],
                )
                packed_lower = v3.pack_trits(source_lower)
                packed_grade = v3.pack_trits(source_grade)
                if lower_pivot is not None:
                    if not same_bytes(
                        packed_lower, physical["lower_origins"][lower_pivot]
                    ):
                        fail("sealed_old_lower_origin")
                    _, scale, edge_start, edge_count, _, _ = lower_nodes[lower_pivot]
                    companion = packed_grade.copy()
                    for edge_index in range(edge_start, edge_start + edge_count):
                        earlier, coefficient = lower_edges[edge_index]
                        packed_axpy(
                            companion,
                            coefficient,
                            physical["lower_companions"][earlier],
                        )
                    if scale == 2:
                        companion[:] = SCALE2[companion]
                    if not same_bytes(
                        companion, physical["lower_companions"][lower_pivot]
                    ):
                        fail("sealed_old_companion")
                else:
                    _, _, _, _, lower_start, lower_count = grade_nodes[grade_pivot]
                    lower_remainder = packed_lower.copy()
                    companion = packed_grade.copy()
                    for edge_index in range(lower_start, lower_start + lower_count):
                        earlier, coefficient = lower_edges[edge_index]
                        packed_axpy(
                            lower_remainder,
                            coefficient,
                            physical["lower_stored"][earlier],
                        )
                        packed_axpy(
                            companion,
                            coefficient,
                            physical["lower_companions"][earlier],
                        )
                    if np.any(lower_remainder):
                        fail("sealed_old_lower_nonzero")
                    if not same_bytes(
                        companion, physical["grade_origins"][grade_pivot]
                    ):
                        fail("sealed_old_grade_origin")
            del low, lift, low_raw, lift_raw

        if block_refs:
            body = sealed_body(state, f"block-{character}", block_digests[character])
            v3.validate_block_state(
                state,
                body,
                prepare,
                PREPARE_SHA,
                character,
                authenticate_basis=False,
            )
            owner = v3.load_block_owner(state, body)
            roots = []
            for ref in block_refs:
                logical = int(ref["logical"])
                pivot = int(ref["pivot"])
                node = body["dag_nodes"][pivot]
                expected_ref = {
                    "logical": logical,
                    "kind": "block",
                    "block": character,
                    "pivot": pivot,
                    "block_dag_node": node,
                    "ancestry_key": f"block:{character}:{pivot}",
                }
                if ref != expected_ref:
                    fail("source_block_ref")
                grade_pivot = grade_by_logical.get(logical)
                if grade_pivot is None:
                    fail("source_block_physical_origin")
                source = v3.aggregate_pure_grade(
                    context, character, owner.dense_row(pivot)
                )
                if not same_bytes(
                    v3.pack_trits(source), physical["grade_origins"][grade_pivot]
                ):
                    fail("sealed_block_grade_origin")
                roots.append(pivot)

            todo = list(roots)
            while todo:
                pivot = todo.pop()
                key = f"block:{character}:{pivot}"
                if key in expected_source:
                    continue
                node = body["dag_nodes"][pivot]
                origin = node["origin"]
                children = []
                if origin["kind"] == "actor":
                    parent = int(origin["parent"])
                    children.append(f"block:{character}:{parent}")
                    todo.append(parent)
                elif origin["kind"] == "defect":
                    children.append(
                        expect_defect(character, int(origin["origin"]))
                    )
                else:
                    fail("source_block_origin")
                for earlier, _ in node["reductions"]:
                    earlier = int(earlier)
                    children.append(f"block:{character}:{earlier}")
                    todo.append(earlier)
                expected = {
                    "key": key,
                    "kind": "block",
                    "character": character,
                    "pivot": pivot,
                    "node": node,
                    "children": children,
                    "syntax": {
                        "origin": origin,
                        "reductions": [
                            {"pivot": int(q), "coefficient": int(c)}
                            for q, c in node["reductions"]
                        ],
                        "scale": int(node["scale"]),
                    },
                }
                match(source_map, key, expected, "source_structure_node_exact")
                expected_source.add(key)
            del owner, body
        gc.collect()
        phase(
            "selected-character-replay-released",
            character=character,
            selected_old=len(old_refs),
            selected_block=len(block_refs),
            source_nodes=len(expected_source),
        )

    if (
        expected_source != set(source_map)
        or expected_defects != set(defect_map)
        or expected_expressions != set(expression_map)
    ):
        fail("source_structure_key_closure")
    return True


def valid_leaf_key(seed: int, path: tuple[int, ...], coefficient: int) -> None:
    if not 0 < seed <= 0xFFFFFFFF or coefficient not in (1, 2):
        fail("leaf_scalar")
    if len(path) > 0xFFFFFFFF:
        fail("leaf_path_length")
    for index, letter in enumerate(path):
        if letter not in (-2, -1, 1, 2):
            fail("leaf_letter")
        if index and path[index - 1] == -letter:
            fail("leaf_not_reduced")


def validate_leaf_syntax(data, ancestry_sha256: str) -> None:
    raw = memoryview(data).cast("B")
    if len(raw) < LEAF_HEADER.size:
        fail("leaf_header")
    magic, version, quotient, common, states, binding, count = LEAF_HEADER.unpack_from(raw)
    if (
        magic != LEAF_MAGIC
        or version != LEAF_VERSION
        or (quotient, common, states) != (1, 0, 0)
        or binding != bytes.fromhex(ancestry_sha256)
    ):
        fail("leaf_header")
    cursor = LEAF_HEADER.size
    previous = None
    for _ in range(count):
        if cursor + LEAF_RECORD.size > len(raw):
            fail("leaf_record_short")
        payload, seed, coefficient, length = LEAF_RECORD.unpack_from(raw, cursor)
        cursor += LEAF_RECORD.size
        if payload != 9 + length or cursor + length > len(raw):
            fail("leaf_record_length")
        path = (
            tuple(struct.unpack_from("<%db" % length, raw, cursor)) if length else ()
        )
        cursor += length
        valid_leaf_key(seed, path, coefficient)
        key = (seed, path)
        if previous is not None and key <= previous:
            fail("leaf_order")
        previous = key
    if cursor != len(raw):
        fail("leaf_trailing")


def checker_leaf_chunks(leaf_map: dict, ancestry_sha256: str):
    keys = sorted(leaf_map)
    yield LEAF_HEADER.pack(
        LEAF_MAGIC,
        LEAF_VERSION,
        1,
        0,
        0,
        bytes.fromhex(ancestry_sha256),
        len(keys),
    )
    previous = None
    for seed, path in keys:
        path = tuple(int(letter) for letter in path)
        coefficient = int(leaf_map[(seed, path)])
        valid_leaf_key(int(seed), path, coefficient)
        key = (int(seed), path)
        if previous is not None and key <= previous:
            fail("leaf_expected_order")
        previous = key
        yield LEAF_RECORD.pack(9 + len(path), int(seed), coefficient, len(path))
        if path:
            yield struct.pack("<%db" % len(path), *path)


def compare_leaf_stream(data, leaf_map: dict, ancestry_sha256: str) -> None:
    validate_leaf_syntax(data, ancestry_sha256)
    raw = memoryview(data).cast("B")
    cursor = 0
    for chunk in checker_leaf_chunks(leaf_map, ancestry_sha256):
        end = cursor + len(chunk)
        if end > len(raw) or raw[cursor:end] != memoryview(chunk):
            fail("literal_leaf_binding")
        cursor = end
    if cursor != len(raw):
        fail("literal_leaf_binding")


def recompute_leaf_map(
    coefficients,
    refs: list,
    grade_nodes: NodeView,
    lower_nodes: NodeView,
    grade_edges: EdgeView,
    lower_edges: EdgeView,
    source_map: dict,
    defect_map: dict,
    expression_map: dict,
    started: float,
):
    refs_by_logical = {int(ref["logical"]): ref for ref in refs}
    pending = {}
    leaves = {}
    processed = 0
    maximum_path = 0

    def push(kind: str, ids: tuple[int, ...], prefix, coefficient: int) -> None:
        nonlocal maximum_path
        coefficient %= 3
        if not coefficient:
            return
        prefix = tuple(int(value) for value in prefix)
        maximum_path = max(maximum_path, len(prefix))
        key = (kind,) + tuple(int(value) for value in ids) + (prefix,)
        value = (pending.get(key, 0) + coefficient) % 3
        if value:
            pending[key] = value
        else:
            pending.pop(key, None)

    def leaf(seed: int, path, coefficient: int) -> None:
        nonlocal maximum_path
        coefficient %= 3
        if not coefficient:
            return
        path = tuple(int(value) for value in path)
        maximum_path = max(maximum_path, len(path))
        key = (int(seed), path)
        value = (leaves.get(key, 0) + coefficient) % 3
        if value:
            leaves[key] = value
        else:
            leaves.pop(key, None)

    for pivot, coefficient in coefficients:
        push("grade", (int(pivot),), (), int(coefficient))

    while pending:
        state, coefficient = pending.popitem()
        kind = state[0]
        ids = tuple(int(value) for value in state[1:-1])
        prefix = tuple(state[-1])
        processed += 1
        if kind == "grade":
            pivot = ids[0]
            logical, scale, edge_start, edge_count, lower_start, lower_count = grade_nodes[pivot]
            ref = refs_by_logical[int(logical)]
            if ref["kind"] == "old":
                push(
                    "old",
                    (int(ref["character"]), int(ref["pivot"])),
                    prefix,
                    coefficient * int(scale),
                )
                for index in range(lower_start, lower_start + lower_count):
                    earlier, value = lower_edges[index]
                    push(
                        "lower",
                        (int(earlier),),
                        prefix,
                        -coefficient * int(scale) * int(value),
                    )
            elif ref["kind"] == "block":
                push(
                    "block",
                    (int(ref["block"]), int(ref["pivot"])),
                    prefix,
                    coefficient * int(scale),
                )
            else:
                fail("leaf_grade_origin")
            for index in range(edge_start, edge_start + edge_count):
                earlier, value = grade_edges[index]
                push(
                    "grade",
                    (int(earlier),),
                    prefix,
                    -coefficient * int(scale) * int(value),
                )
        elif kind == "lower":
            pivot = ids[0]
            logical, scale, edge_start, edge_count, _, _ = lower_nodes[pivot]
            ref = refs_by_logical[int(logical)]
            push(
                "old",
                (int(ref["character"]), int(ref["pivot"])),
                prefix,
                coefficient * int(scale),
            )
            for index in range(edge_start, edge_start + edge_count):
                earlier, value = lower_edges[index]
                push(
                    "lower",
                    (int(earlier),),
                    prefix,
                    -coefficient * int(scale) * int(value),
                )
        elif kind == "block":
            character, pivot = ids
            node = source_map[f"block:{character}:{pivot}"]["node"]
            scale = int(node["scale"])
            origin = node["origin"]
            if origin["kind"] == "defect":
                label = CHARACTERS[character]
                for parity, word in PURE_Q1_WORDS.items():
                    push(
                        "defect",
                        (int(origin["origin"]),),
                        word_mul(prefix, word),
                        coefficient * scale * cv(label, parity[0], parity[1]),
                    )
            elif origin["kind"] == "actor":
                push(
                    "block",
                    (character, int(origin["parent"])),
                    word_mul(prefix, (int(origin["letter"]),)),
                    coefficient * scale,
                )
            else:
                fail("leaf_block_origin")
            for earlier, value in node["reductions"]:
                push(
                    "block",
                    (character, int(earlier)),
                    prefix,
                    -coefficient * scale * int(value),
                )
        elif kind == "defect":
            item = defect_map[f"defect:{ids[0]}"]
            origin = item["origin"]
            character = int(origin["lower_character"])
            expression = expression_map[item["expression_key"]]["expression"]
            if origin["kind"] == "seed":
                seed = int(origin["seed"])
                label = CHARACTERS[character]
                for parity, word in PURE_Q1_WORDS.items():
                    leaf(
                        seed,
                        word_mul(prefix, word),
                        coefficient * cv(label, parity[0], parity[1]),
                    )
            elif origin["kind"] == "transition":
                push(
                    "old",
                    (character, int(origin["pivot"])),
                    word_mul(prefix, (int(origin["letter"]),)),
                    coefficient,
                )
            else:
                fail("leaf_defect_origin")
            for earlier, value in expression:
                push(
                    "old",
                    (character, int(earlier)),
                    prefix,
                    -coefficient * int(value),
                )
        elif kind == "old":
            character, pivot = ids
            node = source_map[f"old:{character}:{pivot}"]["node"]
            scale = int(node["scale"])
            origin = node["origin"]
            if origin["kind"] == "projected_seed":
                seed = int(origin["seed"])
                label = CHARACTERS[character]
                for parity, word in PURE_Q1_WORDS.items():
                    leaf(
                        seed,
                        word_mul(prefix, word),
                        coefficient * scale * cv(label, parity[0], parity[1]),
                    )
            elif origin["kind"] == "actor":
                push(
                    "old",
                    (character, int(origin["parent"])),
                    word_mul(prefix, (int(origin["letter"]),)),
                    coefficient * scale,
                )
            else:
                fail("leaf_old_origin")
            for earlier, value in node["reductions"]:
                push(
                    "old",
                    (character, int(earlier)),
                    prefix,
                    -coefficient * scale * int(value),
                )
        else:
            fail("leaf_state_kind")
        if processed % 65536 == 0:
            guard(started)
            phase(
                "leaf-replay-progress",
                processed=processed,
                pending=len(pending),
                leaves=len(leaves),
                maximum_path_length=maximum_path,
            )
    return leaves, processed, maximum_path


class OnlineReceipts:
    def __init__(
        self,
        lower_nodes: NodeView,
        grade_nodes: NodeView,
        lower_edges: EdgeView,
        grade_edges: EdgeView,
        rows: dict[str, RowView],
    ):
        self.lower_nodes = lower_nodes
        self.grade_nodes = grade_nodes
        self.lower_edges = lower_edges
        self.grade_edges = grade_edges
        self.rows = rows
        self.cursor = {
            "lower_nodes": 0,
            "grade_nodes": 0,
            "lower_edges": 0,
            "grade_edges": 0,
            **{name: 0 for name in rows},
        }

    def expect_node(self, name: str, expected: tuple) -> None:
        view = self.lower_nodes if name == "lower_nodes" else self.grade_nodes
        index = self.cursor[name]
        if index >= len(view) or tuple(int(value) for value in view[index]) != expected:
            fail("authoritative_" + name + "_mismatch")
        self.cursor[name] += 1

    def expect_edges(self, name: str, reductions) -> None:
        view = self.lower_edges if name == "lower_edges" else self.grade_edges
        for pivot, coefficient in reductions:
            index = self.cursor[name]
            if index >= len(view) or view[index] != (int(pivot), int(coefficient)):
                fail("authoritative_" + name + "_mismatch")
            self.cursor[name] += 1

    def expect_row(self, name: str, row) -> None:
        view = self.rows[name]
        index = self.cursor[name]
        if index >= len(view) or not same_bytes(view[index], row):
            fail("authoritative_" + name + "_mismatch")
        self.cursor[name] += 1

    def snapshot(self) -> dict:
        return dict(self.cursor)

    def finish(self) -> None:
        expected = {
            "lower_nodes": len(self.lower_nodes),
            "grade_nodes": len(self.grade_nodes),
            "lower_edges": len(self.lower_edges),
            "grade_edges": len(self.grade_edges),
            **{name: len(view) for name, view in self.rows.items()},
        }
        if self.cursor != expected:
            fail("authoritative_cursor_exhaustion")


def independent_transcript_check(
    state: Path,
    manifest: dict,
    body: dict,
    candidate_basis: bytes,
    candidate_remainder: bytes,
    target_raw: bytes,
    grade_nodes: NodeView,
    lower_nodes: NodeView,
    grade_edges: EdgeView,
    lower_edges: EdgeView,
    physical: dict,
    started: float,
):
    if sha(ROUTER_PATH.read_bytes()) != ROUTER_SHA:
        fail("router_hash")
    module_spec = importlib.util.spec_from_file_location(
        "independent_router", ROUTER_PATH
    )
    if module_spec is None or module_spec.loader is None:
        fail("router_loader")
    router = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(router)
    (
        router_prepare,
        prepare_digest,
        residual_receipt,
        residual,
        old_rows,
        blocks,
    ) = router.load_source(state)
    if (
        prepare_digest != PREPARE_SHA
        or body.get("block_sha256") != [item[1] for item in blocks]
        or body.get("block_sha256") != manifest.get("block_sha256")
        or body.get("residual_receipt") != residual_receipt
        or not same_bytes(residual, target_raw)
    ):
        fail("router_parent_binding")
    del router_prepare

    online = OnlineReceipts(
        lower_nodes,
        grade_nodes,
        lower_edges,
        grade_edges,
        {
            "lower_origins": physical["lower_origins"],
            "lower_stored": physical["lower_stored"],
            "lower_companions": physical["lower_companions"],
            "grade_origins": physical["grade_origins"],
            "old_lower_zero": physical["old_lower_zero"],
        },
    )
    context = router.Arithmetic()
    lower = router.IndependentOwner(router.PHYSICAL_LOWER)
    grade = router.IndependentOwner(router.PHYSICAL_GRADE)
    companions = []
    logical = 0
    lower_offers = 0
    grade_offers = 0

    for character in range(4):
        rank, low_raw, lift_raw, source_character = old_rows[character]
        if source_character != character:
            fail("router_old_character")
        low = low_raw.reshape(rank, router.LOWER_WIDTH // 4)
        lift = lift_raw.reshape(rank, router.SOURCE_TOTAL // 4)
        for pivot in range(rank):
            lower_row = router.unpack(low[pivot], router.LOWER_WIDTH)
            occurrence_lower = np.zeros((4, router.SOURCE_BASE), dtype=np.uint8)
            occurrence_lower[character] = lower_row[: router.SOURCE_BASE]
            occurrence_grade = router.unpack(
                lift[pivot], router.SOURCE_TOTAL
            ).reshape(4, router.SOURCE_BLOCK)
            physical_lower, physical_grade = router.aggregate_pair(
                context,
                occurrence_lower,
                occurrence_grade,
                lower_row[router.SOURCE_BASE :],
            )
            lower_offers += 1
            remainder, reductions = lower.reduce(router.pack(physical_lower))
            companion = physical_grade.copy()
            for earlier, coefficient in reductions:
                router.add_mod(companion, companions[int(earlier)], -int(coefficient))
            if np.any(remainder):
                accepted = lower.accept_reduced(remainder, reductions)
                if (
                    not accepted["accepted"]
                    or accepted["reductions"] != reductions
                    or int(accepted["pivot"]) != online.cursor["lower_nodes"]
                ):
                    fail("router_lower_accept")
                edge_start = online.cursor["lower_edges"]
                online.expect_node(
                    "lower_nodes",
                    (
                        logical,
                        int(accepted["scale"]),
                        edge_start,
                        len(reductions),
                        0,
                        0,
                    ),
                )
                online.expect_edges("lower_edges", reductions)
                online.expect_row("lower_origins", router.pack(physical_lower))
                online.expect_row("lower_stored", lower.rows[-1])
                if int(accepted["scale"]) == 2:
                    companion = (
                        2 * companion.astype(np.uint16) % 3
                    ).astype(np.uint8)
                companions.append(companion)
                online.expect_row("lower_companions", router.pack(companion))
            else:
                online.expect_row("old_lower_zero", remainder)
                grade_offers += 1
                inserted = grade.insert(companion)
                if inserted["accepted"]:
                    lower_start = online.cursor["lower_edges"]
                    edge_start = online.cursor["grade_edges"]
                    if int(inserted["pivot"]) != online.cursor["grade_nodes"]:
                        fail("router_grade_pivot")
                    online.expect_node(
                        "grade_nodes",
                        (
                            logical,
                            int(inserted["scale"]),
                            edge_start,
                            len(inserted["reductions"]),
                            lower_start,
                            len(reductions),
                        ),
                    )
                    online.expect_edges("lower_edges", reductions)
                    online.expect_edges("grade_edges", inserted["reductions"])
                    online.expect_row("grade_origins", router.pack(companion))
            logical += 1
            if logical % 256 == 0:
                guard(started)
        old_rows[character] = None
        del low, lift, low_raw, lift_raw
        gc.collect()
        phase(
            "independent-old-boundary",
            character=character,
            logical=logical,
            lower_nodes=online.cursor["lower_nodes"],
            grade_nodes=online.cursor["grade_nodes"],
            lower_edges=online.cursor["lower_edges"],
            grade_edges=online.cursor["grade_edges"],
            old_lower_zero=online.cursor["old_lower_zero"],
        )

    if logical != 2014 or len(lower.rows) != LOWER:
        fail("router_old_counts")
    del lower, companions, old_rows
    gc.collect()

    for block_index in range(4):
        block_body, block_digest, raw, leads = blocks[block_index]
        rank = len(leads)
        matrix = raw.reshape(rank, router.SOURCE_BLOCK // 4)
        for pivot in range(rank):
            grade_offers += 1
            origin = router.aggregate_pure(
                context,
                block_index,
                router.unpack(matrix[pivot], router.SOURCE_BLOCK),
            )
            inserted = grade.insert(origin)
            if inserted["accepted"]:
                edge_start = online.cursor["grade_edges"]
                if int(inserted["pivot"]) != online.cursor["grade_nodes"]:
                    fail("router_grade_pivot")
                online.expect_node(
                    "grade_nodes",
                    (
                        logical,
                        int(inserted["scale"]),
                        edge_start,
                        len(inserted["reductions"]),
                        0,
                        0,
                    ),
                )
                online.expect_edges("grade_edges", inserted["reductions"])
                online.expect_row("grade_origins", router.pack(origin))
            logical += 1
            if logical % 256 == 0:
                guard(started)
        blocks[block_index] = None
        del block_body, raw, leads, matrix
        gc.collect()
        phase(
            "independent-block-boundary",
            block=block_index,
            logical=logical,
            grade_nodes=online.cursor["grade_nodes"],
            grade_edges=online.cursor["grade_edges"],
            grade_origins=online.cursor["grade_origins"],
        )

    if (
        logical,
        lower_offers,
        grade_offers,
        len(grade.rows),
    ) != (8059, 2014, 6398, GRADE):
        fail("router_counts")
    online.finish()

    candidate_rows = physical["basis"]
    basis_digest = hashlib.sha256()
    for pivot, row in enumerate(grade.rows):
        if not same_bytes(row, candidate_rows[pivot]):
            fail("authoritative_basis_mismatch")
        basis_digest.update(memoryview(row))
    if (
        basis_digest.hexdigest() != BASIS_SHA
        or grade.leads != body.get("grade_pivot_leads")
    ):
        fail("authoritative_basis_hash")

    target = np.frombuffer(target_raw, dtype=np.uint8).copy()
    remainder, coefficients = grade.reduce(target)
    if (
        np.any(remainder)
        or not same_bytes(remainder, candidate_remainder)
        or coefficients != body.get("member_coefficients")
    ):
        fail("router_member")
    reconstructed = np.zeros(GRADE_BYTES, dtype=np.uint8)
    for pivot, coefficient in coefficients:
        reconstructed = router.PACKED_AXPY[
            (3 - int(coefficient)) % 3,
            reconstructed,
            grade.rows[int(pivot)],
        ]
    if not np.array_equal(reconstructed, target):
        fail("member_equation")
    dense_target = router.unpack(target, router.PHYSICAL_GRADE)
    if (
        sha(target) != residual_receipt["sha256"]
        or sha(dense_target.tobytes()) != body["residual_sha256"]
        or sha(candidate_remainder) != REMAINDER_SHA
    ):
        fail("router_target_hash")
    phase(
        "basis-member-complete",
        cursor=logical,
        lower_rank=LOWER,
        grade_rank=GRADE,
        coefficients=len(coefficients),
    )
    return {
        "cursor": logical,
        "lower_offer_count": lower_offers,
        "grade_offer_count": grade_offers,
        "lower_rank": LOWER,
        "grade_rank": GRADE,
        "coefficient_count": len(coefficients),
    }


def replay(payload: Path, candidate: Path, state: Path, output: Path | None) -> int:
    global _STARTED
    _STARTED = time.monotonic()
    started = _STARTED
    manifest_raw = (payload / "manifest.json").read_bytes()
    manifest = json.loads(manifest_raw)
    if canon(manifest) != manifest_raw:
        fail("manifest_canonical")
    require_false_claim_flags(manifest, "manifest")
    if (
        manifest.get("schema") != "d972.r07.a0.grade1-selected-slp.v1"
        or manifest.get("marker") != "R07_GRADE1_SELECTED_SLP_V1_CANDIDATE"
        or manifest.get("decision_sha256") != BODY_SHA
        or manifest.get("prepare_sha256") != PREPARE_SHA
        or manifest.get("cursor") != 8059
        or manifest.get("lower_offer_count") != 2014
        or manifest.get("grade_offer_count") != 6398
        or manifest.get("lower_rank") != LOWER
        or manifest.get("grade_rank") != GRADE
        or manifest.get("coefficient_count") != 3317
    ):
        fail("manifest_binding")
    payload_manifest_sha256 = sha(manifest_raw)
    body, basis, candidate_remainder = load_candidate(candidate)
    if (
        body.get("prepare_sha256") != manifest["prepare_sha256"]
        or body.get("block_sha256") != manifest.get("block_sha256")
    ):
        fail("parent_binding")

    expected_file_keys = {
        "grade_nodes",
        "grade_edges",
        "lower_nodes",
        "lower_edges",
        "lower_origins",
        "lower_stored",
        "lower_companions",
        "grade_origins",
        "old_lower_zero",
        "selected_grade",
        "selected_lower",
        "source_refs",
        "source_ancestry",
        "literal_leaves",
        "roots",
    }
    files = manifest.get("files")
    if not isinstance(files, dict) or set(files) != expected_file_keys:
        fail("receipt_set")
    payload_names = {path.name for path in payload.iterdir() if path.is_file()}
    loaded = {}
    for key, receipt in files.items():
        if (
            not isinstance(receipt, dict)
            or receipt.get("file") not in payload_names
            or set(receipt) != {"file", "bytes", "sha256"}
        ):
            fail("receipt_file")
        data = (payload / receipt["file"]).read_bytes()
        if len(data) != receipt["bytes"] or sha(data) != receipt["sha256"]:
            fail("receipt_auth")
        loaded[key] = data
    if (
        manifest.get("roots") != files["roots"]["file"]
        or sum(receipt["bytes"] for receipt in files.values()) > 7 * 1024**3
    ):
        fail("manifest_receipts")

    roots_json = json.loads(loaded["roots"])
    if canon(roots_json) != loaded["roots"]:
        fail("roots_canonical")
    require_false_claim_flags(roots_json, "roots")
    refs = json.loads(loaded["source_refs"])
    if canon(refs) != loaded["source_refs"] or not isinstance(refs, list) or not refs:
        fail("source_refs_schema")
    ancestry = json.loads(loaded["source_ancestry"])
    if canon(ancestry) != loaded["source_ancestry"]:
        fail("source_ancestry_canonical")
    ancestry_sha256 = files["source_ancestry"]["sha256"]
    del loaded["roots"], loaded["source_refs"], loaded["source_ancestry"]

    grade_nodes = NodeView(loaded["grade_nodes"])
    lower_nodes = NodeView(loaded["lower_nodes"])
    grade_edges = EdgeView(loaded["grade_edges"])
    lower_edges = EdgeView(loaded["lower_edges"])
    if len(grade_nodes) != GRADE or len(lower_nodes) != LOWER:
        fail("transcript_shape")
    declared_grade = bits(loaded["selected_grade"], GRADE)
    declared_lower = bits(loaded["selected_lower"], LOWER)
    coefficients = body["member_coefficients"]
    grade_roots = {int(pivot) for pivot, _ in coefficients}
    if len(coefficients) != 3317 or any(
        not 0 <= pivot < GRADE or not declared_grade[pivot] for pivot in grade_roots
    ):
        fail("grade_roots")

    computed_grade = [False] * GRADE
    computed_lower = [False] * LOWER
    for pivot in grade_roots:
        computed_grade[pivot] = True
    for pivot in range(GRADE - 1, -1, -1):
        if not computed_grade[pivot]:
            continue
        _, _, edge_start, edge_count, lower_start, lower_count = grade_nodes[pivot]
        for index in range(edge_start, edge_start + edge_count):
            earlier, _ = grade_edges[index]
            if earlier >= pivot:
                fail("grade_closure")
            computed_grade[earlier] = True
        for index in range(lower_start, lower_start + lower_count):
            earlier, _ = lower_edges[index]
            if earlier >= LOWER:
                fail("lower_closure_index")
            computed_lower[earlier] = True
    for pivot in range(LOWER - 1, -1, -1):
        if not computed_lower[pivot]:
            continue
        _, _, edge_start, edge_count, _, _ = lower_nodes[pivot]
        for index in range(edge_start, edge_start + edge_count):
            earlier, _ = lower_edges[index]
            if earlier >= pivot:
                fail("lower_closure")
            computed_lower[earlier] = True
    if computed_grade != declared_grade or computed_lower != declared_lower:
        fail("closure_bitsets")
    expected_origins = {
        int(grade_nodes[index][0])
        for index, selected in enumerate(computed_grade)
        if selected
    }
    expected_origins.update(
        int(lower_nodes[index][0])
        for index, selected in enumerate(computed_lower)
        if selected
    )
    if {int(ref["logical"]) for ref in refs} != expected_origins:
        fail("source_ref_closure_binding")

    structure, source_map, defect_map, expression_map, leaf_metadata = validate_ancestry(
        ancestry, refs, coefficients, declared_grade, declared_lower
    )
    phase(
        "receipts-single-ancestry-parse-complete",
        grade_nodes=len(grade_nodes),
        lower_nodes=len(lower_nodes),
        grade_edges=len(grade_edges),
        lower_edges=len(lower_edges),
        selected_refs=len(refs),
    )
    physical = validate_physical_streams(
        loaded,
        grade_nodes,
        lower_nodes,
        grade_edges,
        lower_edges,
        basis,
        declared_grade,
        declared_lower,
    )
    prepare, target_raw = load_prepare_and_residual(state)
    selected_source_graph_replay(
        state,
        prepare,
        manifest["block_sha256"],
        refs,
        source_map,
        defect_map,
        expression_map,
        grade_nodes,
        lower_nodes,
        grade_edges,
        lower_edges,
        physical,
    )

    leaves, processed, maximum_path = recompute_leaf_map(
        coefficients,
        refs,
        grade_nodes,
        lower_nodes,
        grade_edges,
        lower_edges,
        source_map,
        defect_map,
        expression_map,
        started,
    )
    if (
        leaf_metadata["file"] != files["literal_leaves"]["file"]
        or leaf_metadata["schema"] != LEAF_SCHEMA
    ):
        fail("literal_leaf_receipt_pointer")
    compare_leaf_stream(loaded["literal_leaves"], leaves, ancestry_sha256)
    leaf_count = len(leaves)

    expected_children = [
        {
            "type": "GradeNodeRef",
            "pivot": int(pivot),
            "coefficient": int(coefficient),
        }
        for pivot, coefficient in coefficients
    ]
    if (
        roots_json.get("C_T") != {
            "type": "OrderedProduct",
            "children": expected_children,
        }
        or roots_json.get("C_<1")
        != {
            "type": "RegisteredPriorProduct",
            "terms": prepare.get("canonical_solution", {}).get("terms", []),
        }
        or roots_json.get("C_1")
        != {"type": "Compose", "left": "C_<1", "right": "C_T"}
    ):
        fail("roots_update")

    del (
        ancestry,
        structure,
        source_map,
        defect_map,
        expression_map,
        refs,
        leaves,
        prepare,
    )
    loaded.pop("literal_leaves")
    gc.collect()
    phase(
        "before-standalone-router",
        leaf_count=leaf_count,
        leaf_states_processed=processed,
        maximum_path_length=maximum_path,
        grade_node_cursor=0,
        lower_node_cursor=0,
    )
    routing = independent_transcript_check(
        state,
        manifest,
        body,
        basis,
        candidate_remainder,
        target_raw,
        grade_nodes,
        lower_nodes,
        grade_edges,
        lower_edges,
        physical,
        started,
    )

    verdict = {
        "basis_sha256": BASIS_SHA,
        "coefficient_count": 3317,
        "cross_checked": False,
        "cursor": 8059,
        "grade_offer_count": 6398,
        "grade_rank": GRADE,
        "literal_leaves_sha256": files["literal_leaves"]["sha256"],
        "lower_offer_count": 2014,
        "lower_rank": LOWER,
        "marker": MARKER,
        "payload_manifest_sha256": payload_manifest_sha256,
        "prepare_sha256": PREPARE_SHA,
        "remainder_sha256": REMAINDER_SHA,
        "roots_sha256": files["roots"]["sha256"],
        "source_ancestry_sha256": ancestry_sha256,
        "verified": False,
    }
    if routing != {
        "cursor": 8059,
        "lower_offer_count": 2014,
        "grade_offer_count": 6398,
        "lower_rank": LOWER,
        "grade_rank": GRADE,
        "coefficient_count": 3317,
    }:
        fail("router_terminal_receipt")
    if output is not None:
        guard(started)
        output.write_bytes(canon(verdict))
    phase(
        "verdict-sealed",
        cursor=8059,
        lower_rank=LOWER,
        grade_rank=GRADE,
        coefficients=3317,
        leaves=leaf_count,
    )
    print(json.dumps(verdict, sort_keys=True))
    return 0


def selftest() -> int:
    if int(AXPY[2, 2, 1]) != 0 or int(AXPY[2, 1, 2]) != 0:
        fail("fixture_coefficient_2")

    node_raw = bytearray(NODE.size)
    NODE.pack_into(node_raw, 0, 0, 1, 0, 1, 0, 0)
    edge_raw = EDGE.pack(0, 1)
    rows = {"row": RowView(bytes([1]), 1, 1, "fixture_row")}
    online = OnlineReceipts(
        NodeView(node_raw),
        NodeView(b""),
        EdgeView(edge_raw),
        EdgeView(b""),
        rows,
    )
    online.expect_node("lower_nodes", (0, 1, 0, 1, 0, 0))
    online.expect_edges("lower_edges", [(0, 1)])
    online.expect_row("row", bytes([1]))
    online.finish()
    try:
        unfinished = OnlineReceipts(
            NodeView(node_raw),
            NodeView(b""),
            EdgeView(edge_raw),
            EdgeView(b""),
            rows,
        )
        unfinished.finish()
    except RuntimeError as exc:
        if str(exc) != "authoritative_cursor_exhaustion":
            raise
    else:
        fail("fixture_cursor_exhaustion_not_rejected")
    try:
        broken = OnlineReceipts(
            NodeView(node_raw),
            NodeView(b""),
            EdgeView(edge_raw),
            EdgeView(b""),
            rows,
        )
        broken.expect_node("lower_nodes", (1, 1, 0, 1, 0, 0))
    except RuntimeError:
        pass
    else:
        fail("fixture_transcript_mutation")

    ancestry_digest = "22" * 32
    leaf_map = {(1, ()): 1, (2, (-2, 1)): 2}
    leaf_raw = b"".join(checker_leaf_chunks(leaf_map, ancestry_digest))
    compare_leaf_stream(leaf_raw, leaf_map, ancestry_digest)
    header = leaf_raw[: LEAF_HEADER.size]
    _, _, _, first_length = LEAF_RECORD.unpack_from(leaf_raw, LEAF_HEADER.size)
    first_size = LEAF_RECORD.size + first_length
    swapped = (
        header
        + leaf_raw[LEAF_HEADER.size + first_size :]
        + leaf_raw[LEAF_HEADER.size : LEAF_HEADER.size + first_size]
    )
    mutations = [swapped, leaf_raw + b"\0"]
    coefficient_zero = bytearray(leaf_raw)
    coefficient_zero[LEAF_HEADER.size + 8] = 0
    mutations.append(bytes(coefficient_zero))
    for mutation in mutations:
        try:
            validate_leaf_syntax(mutation, ancestry_digest)
        except RuntimeError:
            pass
        else:
            fail("fixture_leaf_mutation")
    states_header = bytearray(leaf_raw)
    states_header[len(LEAF_MAGIC) + 3] = 1
    try:
        validate_leaf_syntax(bytes(states_header), ancestry_digest)
    except RuntimeError as exc:
        if str(exc) != "leaf_header":
            raise
    else:
        fail("fixture_leaf_states_not_rejected")

    false_flags = {
        "direct_occurrence_replay": False,
        "next_degree2_residual": None,
        "cross_checked": False,
        "verified": False,
        "A0": False,
        "COMMON": False,
        "FAKE": False,
        "IHARA": False,
    }
    require_false_claim_flags(false_flags, "selftest")
    for key in false_flags:
        mutated = dict(false_flags)
        mutated[key] = [] if key == "next_degree2_residual" else True
        try:
            require_false_claim_flags(mutated, "selftest")
        except RuntimeError:
            pass
        else:
            fail("claim_flag_mutation_not_rejected")
    derived = {
        "schema": "d972.r07.a0.selected-literal-derived.v2",
        "leaf_receipt": {
            "file": "literal-leaves.bin",
            "schema": LEAF_SCHEMA,
            "quotient_specific_evaluation": True,
            "common_source_witness": False,
            "states_exported": False,
        },
    }
    validate_derived_metadata(derived)
    forbidden_derived = dict(derived)
    forbidden_derived["states"] = []
    try:
        validate_derived_metadata(forbidden_derived)
    except RuntimeError as exc:
        if str(exc) != "derived_compact_schema":
            raise
    else:
        fail("fixture_derived_states_not_rejected")
    print(
        json.dumps(
            {
                "claim_flag_mutation_count": 8,
                "coefficient_2": "PASS",
                "compact_leaf_mutation_count": 4,
                "compact_leaf_roundtrip": "PASS",
                "derived_states_absent": "PASS",
                "false_null_claim_gates": "PASS",
                "forbidden_state_mutation_count": 2,
                "zero_copy_cursor_exhaustion": "PASS",
                "zero_copy_transcript_mutation": "PASS",
            },
            sort_keys=True,
        )
    )
    return 0


def execute(args) -> int:
    if args.selftest:
        return selftest()
    if not args.payload or not args.candidate or not args.state:
        fail("usage")
    return replay(args.payload, args.candidate, args.state, args.out)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--payload", type=Path)
    parser.add_argument("--candidate", type=Path)
    parser.add_argument("--state", type=Path)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args()
    try:
        return execute(args)
    except MemoryError:
        emergency_unknown_resource()
        return 2
    except Exception as exc:
        print(json.dumps({"status": "REJECTED", "error": str(exc)}), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
