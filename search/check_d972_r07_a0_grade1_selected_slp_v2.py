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
MARKER = "R07_GRADE1_SELECTED_SLP_V2_CHECKER_PASS"
BODY_SHA = "62412762b3a208d31febb6c6b8d4707f880471ed32cf62c79c18108065ab7b5d"
PREPARE_SHA = "1f191d88a0453360021ec57d253a7d16c9a66ac059ddaaadb6db3e2b9293c865"
BASIS_SHA = "b562c980c22a25a932bae1b548f72aeede5637b9612afc908fff9a9aecff069d"
REMAINDER_SHA = "564cbfafc869a8c6eb761a392caa5e792b546bf577af7fe808177b2fdf13cbb0"
V3_SHA = "bf872b30149e1351762b243d590d7a1f876e048b92a053d8f9c17bba5c45bcff"
V475_PATH = ROOT / "sol/proof_r07_selected_slp_staged_adjoint_repair_v475.md"
V475_SHA = "757ffab5aa011643efa3df4b133dc03d423895d57a003ed6830a47528388148e"
V475_BYTES = 8253
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
DEFAULT_ACCUMULATED_CAP = 2_000_000
DEFAULT_PATH_CAP = 2_000_000
DEFAULT_PATH_LENGTH_CAP = 4096
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


class UnknownResource(RuntimeError):
    pass


def resource_fail(reason: str) -> None:
    raise UnknownResource("UNKNOWN_RESOURCE:" + reason)


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
        resource_fail("time")
    if peak_rss() > int(os.environ.get("TASK601_MAX_RSS", str(7 * 1024**3))):
        resource_fail("rss")


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


def checker_staged_caps() -> dict[str, int | float]:
    return {
        "accumulated_states": int(
            os.environ.get("TASK625_ACCUMULATED_CAP", str(DEFAULT_ACCUMULATED_CAP))
        ),
        "interned_paths": int(
            os.environ.get("TASK625_PATH_CAP", str(DEFAULT_PATH_CAP))
        ),
        "path_length": int(
            os.environ.get("TASK625_PATH_LENGTH_CAP", str(DEFAULT_PATH_LENGTH_CAP))
        ),
        "durable_bytes": int(
            os.environ.get("TASK625_DURABLE_CAP", str(7 * 1024**3))
        ),
        "seconds": float(os.environ.get("TASK601_SECONDS", "2400")),
        "rss_bytes": int(os.environ.get("TASK601_MAX_RSS", str(7 * 1024**3))),
    }


def checker_inclusive_durable_total(
    receipt_bytes: int, manifest_raw: bytes, cap: int
) -> int:
    if (
        type(receipt_bytes) is not int
        or receipt_bytes < 0
        or type(manifest_raw) is not bytes
        or type(cap) is not int
        or cap < 1
    ):
        fail("checker_durable_accounting")
    total = receipt_bytes + len(manifest_raw)
    if total > cap:
        fail("manifest_receipts")
    return total


def checker_staged_adjoint(
    stages,
    roots,
    edge_iterator,
    caps: dict,
    *,
    started_at: float | None = None,
    clock=time.monotonic,
    reporter=None,
    durable_bytes: int = 0,
    product=word_mul,
):
    """Independent exact-tuple staged accumulation for the repaired v475 order."""
    cap_keys = {
        "accumulated_states",
        "interned_paths",
        "path_length",
        "durable_bytes",
        "seconds",
        "rss_bytes",
    }
    if (
        set(caps) != cap_keys
        or any(caps[key] < 1 for key in cap_keys - {"seconds"})
        or not isinstance(caps["seconds"], (int, float))
        or float(caps["seconds"]) <= 0
    ):
        fail("checker_staged_caps")
    if started_at is None:
        started_at = clock()
    if type(durable_bytes) is not int or durable_bytes < 0:
        fail("checker_staged_durable_bytes")
    if durable_bytes > int(caps["durable_bytes"]):
        resource_fail("staged_durable_cap")

    sequence = []
    ranges = []
    for label, values in stages:
        first = len(sequence)
        sequence.extend(tuple(values))
        ranges.append((str(label), first, len(sequence)))
    if len(sequence) != len(set(sequence)):
        fail("checker_staged_duplicate_node")
    ordinal = {node: index for index, node in enumerate(sequence)}

    def resource_gate() -> None:
        if clock() - started_at > float(caps["seconds"]):
            resource_fail("staged_time_cap")
        if peak_rss() > int(caps["rss_bytes"]):
            resource_fail("staged_rss_cap")

    def validate_word(
        result: tuple[int, ...], *, require_builtin_int: bool = False
    ) -> tuple[int, ...]:
        if len(result) > int(caps["path_length"]):
            resource_fail("staged_path_length_cap")
        previous = None
        for letter in result:
            if require_builtin_int and type(letter) is not int:
                fail("checker_staged_product_type")
            if letter not in (-2, -1, 1, 2):
                fail("checker_staged_path_letter")
            if previous == -letter:
                fail("checker_staged_path_not_reduced")
            previous = letter
        return result

    def normalize_word(value) -> tuple[int, ...]:
        return validate_word(tuple(int(letter) for letter in value))

    def audit_edge(edge, source_ordinal: int):
        if type(edge) is not tuple or len(edge) != 7:
            fail("checker_staged_edge_shape")
        target, seed, weight, suffix, category, source_pivot, target_pivot = edge
        weight = int(weight) % 3
        if weight not in (1, 2):
            fail("checker_staged_edge_scalar")
        suffix = normalize_word(suffix)
        if category == "reduction":
            if (
                type(source_pivot) is not int
                or type(target_pivot) is not int
                or target_pivot >= source_pivot
            ):
                fail("checker_staged_reduction_not_earlier")
        elif category == "actor":
            if (
                type(source_pivot) is not int
                or type(target_pivot) is not int
                or target_pivot >= source_pivot
            ):
                fail("checker_staged_actor_parent_not_earlier")
        elif category not in ("link", "literal"):
            fail("checker_staged_edge_relation")
        if target is None:
            if category != "literal" or type(seed) is not int or seed <= 0:
                fail("checker_staged_leaf_edge")
        else:
            destination = ordinal.get(target)
            if seed is not None or destination is None:
                fail("checker_staged_missing_node")
            if destination <= source_ordinal:
                fail("checker_staged_processed_destination")
        return target, seed, weight, suffix

    for source_ordinal, node in enumerate(sequence):
        for edge in edge_iterator(node):
            audit_edge(edge, source_ordinal)
        if source_ordinal % 1024 == 0:
            resource_gate()

    bins = {}
    leaf_coefficients = {}
    exact_paths = {()}
    live_bins = 0
    inserted = 0
    contributions = 0
    traversals = 0
    cancellations = 0
    expanded = 0
    max_live = 0
    max_length = 0
    current_ordinal = -1
    local_peak = 0

    def retain_exact(exact: tuple[int, ...]) -> tuple[int, ...]:
        nonlocal max_length
        max_length = max(max_length, len(exact))
        if exact not in exact_paths:
            if len(exact_paths) >= int(caps["interned_paths"]):
                resource_fail("staged_path_cap")
            exact_paths.add(exact)
        return exact

    def remember(path) -> tuple[int, ...]:
        return retain_exact(normalize_word(path))

    def remember_product(path) -> tuple[int, ...]:
        if type(path) is not tuple:
            fail("checker_staged_product_type")
        return retain_exact(validate_word(path, require_builtin_int=True))

    def count_live() -> None:
        nonlocal max_live, local_peak
        total = live_bins + len(leaf_coefficients)
        max_live = max(max_live, total)
        local_peak = max(local_peak, total)
        if total > int(caps["accumulated_states"]):
            resource_fail("staged_state_cap")

    def send_node(destination, path, value: int) -> None:
        nonlocal live_bins, inserted, contributions, cancellations
        value %= 3
        if not value:
            return
        destination_ordinal = ordinal.get(destination)
        if destination_ordinal is None:
            fail("checker_staged_missing_node")
        if destination_ordinal <= current_ordinal:
            fail("checker_staged_processed_destination")
        contributions += 1
        table = bins.setdefault(destination, {})
        combined = (table.get(path, 0) + value) % 3
        if combined:
            if path not in table:
                live_bins += 1
                inserted += 1
                if inserted > int(caps["accumulated_states"]):
                    resource_fail("staged_state_cap")
            table[path] = combined
        elif path in table:
            del table[path]
            live_bins -= 1
            cancellations += 1
            if not table:
                del bins[destination]
        count_live()

    def send_leaf(seed: int, path, value: int) -> None:
        nonlocal inserted, contributions, cancellations
        value %= 3
        if not value:
            return
        contributions += 1
        key = (int(seed), path)
        combined = (leaf_coefficients.get(key, 0) + value) % 3
        if combined:
            if key not in leaf_coefficients:
                inserted += 1
                if inserted > int(caps["accumulated_states"]):
                    resource_fail("staged_state_cap")
            leaf_coefficients[key] = combined
        elif key in leaf_coefficients:
            del leaf_coefficients[key]
            cancellations += 1
        count_live()

    for node, path, value in roots:
        send_node(node, remember(path), int(value))

    stage_receipts = []
    processed_nodes = 0
    active_nodes = 0
    first_stage = True
    for stage, first, stop in ranges:
        prior_inserted = 0 if first_stage else inserted
        prior_contributions = 0 if first_stage else contributions
        prior_cancellations = 0 if first_stage else cancellations
        prior_expanded = expanded
        prior_traversals = traversals
        first_stage = False
        local_peak = live_bins + len(leaf_coefficients)
        stage_active = 0
        for current_ordinal in range(first, stop):
            node = sequence[current_ordinal]
            table = bins.pop(node, None)
            processed_nodes += 1
            if not table:
                continue
            stage_active += 1
            active_nodes += 1
            live_bins -= len(table)
            count_live()
            outgoing = tuple(
                audit_edge(edge, current_ordinal) for edge in edge_iterator(node)
            )
            for path, coefficient in table.items():
                expanded += 1
                for target, seed, weight, suffix in outgoing:
                    traversals += 1
                    next_path = remember_product(product(path, suffix)) if suffix else path
                    emitted = coefficient * weight
                    if target is None:
                        send_leaf(seed, next_path, emitted)
                    else:
                        send_node(target, next_path, emitted)
                if expanded % 65536 == 0:
                    resource_gate()
            del outgoing
            del table
        resource_gate()
        receipt = {
            "stage": stage,
            "processed_nodes": stop - first,
            "nonzero_nodes": stage_active,
            "accumulated_states": inserted - prior_inserted,
            "incoming_contributions": contributions - prior_contributions,
            "cancelled_states": cancellations - prior_cancellations,
            "expanded_states": expanded - prior_expanded,
            "state_edge_traversals": traversals - prior_traversals,
            "interned_paths": len(exact_paths),
            "maximum_live_entries": local_peak,
            "maximum_path_length": max_length,
            "leaf_count": len(leaf_coefficients),
            "observation": {
                "elapsed_seconds": round(clock() - started_at, 6),
                "rss_bytes": current_rss(),
                "peak_rss_bytes": peak_rss(),
                "durable_bytes": durable_bytes,
            },
        }
        stage_receipts.append(receipt)
        if reporter is not None:
            reporter(receipt)

    if bins:
        fail("checker_staged_unprocessed_accumulator")
    leaf_receipt = {
        "stage": "leaves",
        "processed_nodes": 0,
        "nonzero_nodes": 0,
        "accumulated_states": 0,
        "incoming_contributions": 0,
        "cancelled_states": 0,
        "expanded_states": 0,
        "state_edge_traversals": 0,
        "interned_paths": len(exact_paths),
        "maximum_live_entries": len(leaf_coefficients),
        "maximum_path_length": max_length,
        "leaf_count": len(leaf_coefficients),
        "observation": {
            "elapsed_seconds": round(clock() - started_at, 6),
            "rss_bytes": current_rss(),
            "peak_rss_bytes": peak_rss(),
            "durable_bytes": durable_bytes,
        },
    }
    stage_receipts.append(leaf_receipt)
    if reporter is not None:
        reporter(leaf_receipt)

    resource_gate()
    summary = {
        "schema": "d972.r07.a0.staged-adjoint-statistics.v2",
        "schedule": [label for label, _, _ in ranges] + ["leaves"],
        "caps": dict(caps),
        "stages": stage_receipts,
        "totals": {
            "processed_nodes": processed_nodes,
            "nonzero_nodes": active_nodes,
            "accumulated_states": inserted,
            "incoming_contributions": contributions,
            "cancelled_states": cancellations,
            "expanded_states": expanded,
            "state_edge_traversals": traversals,
            "interned_paths": len(exact_paths),
            "maximum_live_entries": max_live,
            "maximum_path_length": max_length,
            "leaf_count": len(leaf_coefficients),
            "observation": {
                "elapsed_seconds": round(clock() - started_at, 6),
                "rss_bytes": current_rss(),
                "peak_rss_bytes": peak_rss(),
                "durable_bytes": durable_bytes,
            },
        },
    }
    return leaf_coefficients, summary


def scheduler_projection(statistics: dict, caps: dict, label: str) -> dict:
    expected_top = {"schema", "schedule", "caps", "stages", "totals"}
    if not isinstance(statistics, dict) or set(statistics) != expected_top:
        fail(label + "_schema")
    expected_schedule = [
        "physical-grade",
        "physical-lower",
        "block-0",
        "block-1",
        "block-2",
        "block-3",
        "defect",
        "old-0",
        "old-1",
        "old-2",
        "old-3",
        "leaves",
    ]
    if (
        statistics.get("schema") != "d972.r07.a0.staged-adjoint-statistics.v2"
        or statistics.get("schedule") != expected_schedule
        or statistics.get("caps") != caps
        or not isinstance(statistics.get("stages"), list)
        or len(statistics["stages"]) != len(expected_schedule)
    ):
        fail(label + "_binding")
    deterministic_fields = {
        "stage",
        "processed_nodes",
        "nonzero_nodes",
        "accumulated_states",
        "incoming_contributions",
        "cancelled_states",
        "expanded_states",
        "state_edge_traversals",
        "interned_paths",
        "maximum_live_entries",
        "maximum_path_length",
        "leaf_count",
    }
    projected_stages = []
    elapsed = -1.0
    for expected_name, record in zip(expected_schedule, statistics["stages"]):
        if (
            not isinstance(record, dict)
            or set(record) != deterministic_fields | {"observation"}
            or record.get("stage") != expected_name
        ):
            fail(label + "_stage")
        if any(
            type(record[field]) is not int or record[field] < 0
            for field in deterministic_fields - {"stage"}
        ):
            fail(label + "_stage_count")
        observation = record["observation"]
        if (
            not isinstance(observation, dict)
            or set(observation)
            != {"elapsed_seconds", "rss_bytes", "peak_rss_bytes", "durable_bytes"}
            or not isinstance(observation["elapsed_seconds"], (int, float))
            or observation["elapsed_seconds"] < elapsed
            or type(observation["rss_bytes"]) is not int
            or type(observation["peak_rss_bytes"]) is not int
            or not 0 <= observation["rss_bytes"] <= int(caps["rss_bytes"])
            or not 0 <= observation["peak_rss_bytes"] <= int(caps["rss_bytes"])
            or type(observation["durable_bytes"]) is not int
            or not 0 <= observation["durable_bytes"] <= int(caps["durable_bytes"])
            or float(observation["elapsed_seconds"]) > float(caps["seconds"])
            or record["interned_paths"] > int(caps["interned_paths"])
            or record["maximum_live_entries"] > int(caps["accumulated_states"])
            or record["maximum_path_length"] > int(caps["path_length"])
        ):
            fail(label + "_stage_observation")
        elapsed = float(observation["elapsed_seconds"])
        projected_stages.append(
            {field: record[field] for field in sorted(deterministic_fields)}
        )
    totals = statistics["totals"]
    total_fields = deterministic_fields - {"stage"}
    if (
        not isinstance(totals, dict)
        or set(totals) != total_fields | {"observation"}
        or any(type(totals[field]) is not int or totals[field] < 0 for field in total_fields)
        or totals["processed_nodes"]
        != sum(record["processed_nodes"] for record in statistics["stages"])
        or totals["expanded_states"]
        != sum(record["expanded_states"] for record in statistics["stages"])
        or totals["state_edge_traversals"]
        != sum(record["state_edge_traversals"] for record in statistics["stages"])
        or totals["nonzero_nodes"]
        != sum(record["nonzero_nodes"] for record in statistics["stages"])
        or totals["accumulated_states"]
        != sum(record["accumulated_states"] for record in statistics["stages"])
        or totals["incoming_contributions"]
        != sum(record["incoming_contributions"] for record in statistics["stages"])
        or totals["cancelled_states"]
        != sum(record["cancelled_states"] for record in statistics["stages"])
        or totals["interned_paths"] != statistics["stages"][-1]["interned_paths"]
        or totals["maximum_live_entries"]
        != max(record["maximum_live_entries"] for record in statistics["stages"])
        or totals["maximum_path_length"]
        != max(record["maximum_path_length"] for record in statistics["stages"])
        or totals["leaf_count"] != statistics["stages"][-1]["leaf_count"]
        or totals["accumulated_states"] > int(caps["accumulated_states"])
        or totals["interned_paths"] > int(caps["interned_paths"])
        or totals["maximum_live_entries"] > int(caps["accumulated_states"])
        or totals["maximum_path_length"] > int(caps["path_length"])
    ):
        fail(label + "_totals")
    final_observation = totals["observation"]
    if (
        not isinstance(final_observation, dict)
        or set(final_observation)
        != {"elapsed_seconds", "rss_bytes", "peak_rss_bytes", "durable_bytes"}
        or not isinstance(final_observation["elapsed_seconds"], (int, float))
        or float(final_observation["elapsed_seconds"]) < elapsed
        or float(final_observation["elapsed_seconds"]) > float(caps["seconds"])
        or type(final_observation["rss_bytes"]) is not int
        or type(final_observation["peak_rss_bytes"]) is not int
        or not 0 <= final_observation["rss_bytes"] <= int(caps["rss_bytes"])
        or not 0 <= final_observation["peak_rss_bytes"] <= int(caps["rss_bytes"])
        or type(final_observation["durable_bytes"]) is not int
        or not 0 <= final_observation["durable_bytes"] <= int(caps["durable_bytes"])
    ):
        fail(label + "_total_observation")
    return {
        "schema": statistics["schema"],
        "schedule": list(statistics["schedule"]),
        "caps": dict(statistics["caps"]),
        "stages": projected_stages,
        "totals": {field: totals[field] for field in sorted(total_fields)},
    }


def recompute_staged_leaf_map(
    coefficients,
    refs: list,
    declared_grade: list[bool],
    declared_lower: list[bool],
    grade_nodes: NodeView,
    lower_nodes: NodeView,
    grade_edges: EdgeView,
    lower_edges: EdgeView,
    source_map: dict,
    defect_map: dict,
    expression_map: dict,
    caps: dict,
    started: float,
    durable_bytes: int,
):
    refs_by_logical = {int(ref["logical"]): ref for ref in refs}
    block_pivots = {character: [] for character in range(4)}
    old_pivots = {character: [] for character in range(4)}
    for item in source_map.values():
        kind = item["kind"]
        character = int(item["character"])
        pivot = int(item["pivot"])
        if kind == "block":
            block_pivots[character].append(pivot)
        elif kind == "old":
            old_pivots[character].append(pivot)
        else:
            fail("checker_staged_source_kind")
    defect_origins = sorted(int(key.split(":", 1)[1]) for key in defect_map)
    stages = [
        (
            "physical-grade",
            tuple(
                ("grade", pivot)
                for pivot in range(GRADE - 1, -1, -1)
                if declared_grade[pivot]
            ),
        ),
        (
            "physical-lower",
            tuple(
                ("lower", pivot)
                for pivot in range(LOWER - 1, -1, -1)
                if declared_lower[pivot]
            ),
        ),
    ]
    for character in range(4):
        stages.append(
            (
                f"block-{character}",
                tuple(
                    ("block", character, pivot)
                    for pivot in sorted(block_pivots[character], reverse=True)
                ),
            )
        )
    stages.append(("defect", tuple(("defect", origin) for origin in defect_origins)))
    for character in range(4):
        stages.append(
            (
                f"old-{character}",
                tuple(
                    ("old", character, pivot)
                    for pivot in sorted(old_pivots[character], reverse=True)
                ),
            )
        )

    def to_node(
        target,
        coefficient: int,
        suffix=(),
        category="link",
        source_pivot=None,
        target_pivot=None,
    ):
        return (
            target,
            None,
            int(coefficient),
            tuple(int(letter) for letter in suffix),
            category,
            source_pivot,
            target_pivot,
        )

    def to_leaf(seed: int, coefficient: int, suffix=()):
        return (
            None,
            int(seed),
            int(coefficient),
            tuple(int(letter) for letter in suffix),
            "literal",
            None,
            None,
        )

    def edges(identifier):
        kind = identifier[0]
        if kind == "grade":
            pivot = int(identifier[1])
            logical, scale, first, count, lower_first, lower_count = grade_nodes[pivot]
            ref = refs_by_logical.get(int(logical))
            if ref is None:
                fail("checker_staged_missing_physical_origin")
            if ref["kind"] == "old":
                yield to_node(
                    ("old", int(ref["character"]), int(ref["pivot"])), int(scale)
                )
                for edge_index in range(lower_first, lower_first + lower_count):
                    earlier, value = lower_edges[edge_index]
                    yield to_node(("lower", int(earlier)), -int(scale) * int(value))
            elif ref["kind"] == "block":
                yield to_node(
                    ("block", int(ref["block"]), int(ref["pivot"])), int(scale)
                )
            else:
                fail("checker_staged_grade_origin")
            for edge_index in range(first, first + count):
                earlier, value = grade_edges[edge_index]
                yield to_node(
                    ("grade", int(earlier)),
                    -int(scale) * int(value),
                    category="reduction",
                    source_pivot=pivot,
                    target_pivot=int(earlier),
                )
        elif kind == "lower":
            pivot = int(identifier[1])
            logical, scale, first, count, _, _ = lower_nodes[pivot]
            ref = refs_by_logical.get(int(logical))
            if ref is None or ref.get("kind") != "old":
                fail("checker_staged_lower_origin")
            yield to_node(
                ("old", int(ref["character"]), int(ref["pivot"])), int(scale)
            )
            for edge_index in range(first, first + count):
                earlier, value = lower_edges[edge_index]
                yield to_node(
                    ("lower", int(earlier)),
                    -int(scale) * int(value),
                    category="reduction",
                    source_pivot=pivot,
                    target_pivot=int(earlier),
                )
        elif kind == "block":
            character, pivot = int(identifier[1]), int(identifier[2])
            item = source_map.get(f"block:{character}:{pivot}")
            if item is None:
                fail("checker_staged_missing_block")
            node = item["node"]
            scale = int(node["scale"])
            origin = node["origin"]
            if origin["kind"] == "defect":
                label = CHARACTERS[character]
                for parity, suffix in PURE_Q1_WORDS.items():
                    yield to_node(
                        ("defect", int(origin["origin"])),
                        scale * cv(label, parity[0], parity[1]),
                        suffix,
                    )
            elif origin["kind"] == "actor":
                parent = int(origin["parent"])
                yield to_node(
                    ("block", character, parent),
                    scale,
                    (int(origin["letter"]),),
                    category="actor",
                    source_pivot=pivot,
                    target_pivot=parent,
                )
            else:
                fail("checker_staged_block_origin")
            for earlier, value in node["reductions"]:
                yield to_node(
                    ("block", character, int(earlier)),
                    -scale * int(value),
                    category="reduction",
                    source_pivot=pivot,
                    target_pivot=int(earlier),
                )
        elif kind == "defect":
            origin_index = int(identifier[1])
            item = defect_map.get(f"defect:{origin_index}")
            if item is None:
                fail("checker_staged_missing_defect")
            origin = item["origin"]
            character = int(origin["lower_character"])
            expression_item = expression_map.get(item["expression_key"])
            if expression_item is None:
                fail("checker_staged_missing_expression")
            expression = expression_item["expression"]
            if origin["kind"] == "seed":
                label = CHARACTERS[character]
                for parity, suffix in PURE_Q1_WORDS.items():
                    yield to_leaf(
                        int(origin["seed"]),
                        cv(label, parity[0], parity[1]),
                        suffix,
                    )
            elif origin["kind"] == "transition":
                yield to_node(
                    ("old", character, int(origin["pivot"])),
                    1,
                    (int(origin["letter"]),),
                )
            else:
                fail("checker_staged_defect_origin")
            for earlier, value in expression:
                yield to_node(("old", character, int(earlier)), -int(value))
        elif kind == "old":
            character, pivot = int(identifier[1]), int(identifier[2])
            item = source_map.get(f"old:{character}:{pivot}")
            if item is None:
                fail("checker_staged_missing_old")
            node = item["node"]
            scale = int(node["scale"])
            origin = node["origin"]
            if origin["kind"] == "projected_seed":
                label = CHARACTERS[character]
                for parity, suffix in PURE_Q1_WORDS.items():
                    yield to_leaf(
                        int(origin["seed"]),
                        scale * cv(label, parity[0], parity[1]),
                        suffix,
                    )
            elif origin["kind"] == "actor":
                parent = int(origin["parent"])
                yield to_node(
                    ("old", character, parent),
                    scale,
                    (int(origin["letter"]),),
                    category="actor",
                    source_pivot=pivot,
                    target_pivot=parent,
                )
            else:
                fail("checker_staged_old_origin")
            for earlier, value in node["reductions"]:
                yield to_node(
                    ("old", character, int(earlier)),
                    -scale * int(value),
                    category="reduction",
                    source_pivot=pivot,
                    target_pivot=int(earlier),
                )
        else:
            fail("checker_staged_node_kind")

    def report(record: dict) -> None:
        phase(
            "staged-adjoint-checker-stage-complete",
            stage=record["stage"],
            processed_nodes=record["processed_nodes"],
            accumulated_states=record["accumulated_states"],
            expanded_states=record["expanded_states"],
            state_edge_traversals=record["state_edge_traversals"],
            interned_paths=record["interned_paths"],
            maximum_live_entries=record["maximum_live_entries"],
            maximum_path_length=record["maximum_path_length"],
            leaves=record["leaf_count"],
            durable_bytes=record["observation"]["durable_bytes"],
        )

    return checker_staged_adjoint(
        stages,
        tuple(
            (("grade", int(pivot)), (), int(coefficient))
            for pivot, coefficient in coefficients
        ),
        edges,
        caps,
        started_at=started,
        reporter=report,
        durable_bytes=durable_bytes,
    )




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
    if output is not None and output.exists():
        fail("output_exists")
    manifest_raw = (payload / "manifest.json").read_bytes()
    manifest = json.loads(manifest_raw)
    if canon(manifest) != manifest_raw:
        fail("manifest_canonical")
    require_false_claim_flags(manifest, "manifest")
    caps = checker_staged_caps()
    expected_theorem = {
        "file": "sol/proof_r07_selected_slp_staged_adjoint_repair_v475.md",
        "bytes": V475_BYTES,
        "sha256": V475_SHA,
    }
    expected_resource_caps = {
        "virtual_memory_bytes": 8 * 1024**3,
        "rss_bytes": int(caps["rss_bytes"]),
        "durable_bytes": int(caps["durable_bytes"]),
        "wall_seconds": float(caps["seconds"]),
        "accumulated_states": int(caps["accumulated_states"]),
        "interned_paths": int(caps["interned_paths"]),
        "path_length": int(caps["path_length"]),
    }
    if V475_PATH.stat().st_size != V475_BYTES or sha(V475_PATH.read_bytes()) != V475_SHA:
        fail("v475_hash")
    if (
        manifest.get("schema") != "d972.r07.a0.grade1-selected-slp.v2"
        or manifest.get("marker") != "R07_GRADE1_SELECTED_SLP_V2_CANDIDATE"
        or manifest.get("decision_sha256") != BODY_SHA
        or manifest.get("prepare_sha256") != PREPARE_SHA
        or manifest.get("cursor") != 8059
        or manifest.get("lower_offer_count") != 2014
        or manifest.get("grade_offer_count") != 6398
        or manifest.get("lower_rank") != LOWER
        or manifest.get("grade_rank") != GRADE
        or manifest.get("coefficient_count") != 3317
        or manifest.get("staged_theorem") != expected_theorem
        or manifest.get("resource_caps") != expected_resource_caps
    ):
        fail("manifest_binding")
    producer_scheduler_projection = scheduler_projection(
        manifest.get("staged_adjoint"), caps, "producer_scheduler"
    )
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
    payload_durable_bytes = checker_inclusive_durable_total(
        sum(int(receipt["bytes"]) for receipt in files.values()),
        manifest_raw,
        int(caps["durable_bytes"]),
    )
    if (
        manifest.get("roots") != files["roots"]["file"]
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

    leaves, checker_scheduler_statistics = recompute_staged_leaf_map(
        coefficients,
        refs,
        declared_grade,
        declared_lower,
        grade_nodes,
        lower_nodes,
        grade_edges,
        lower_edges,
        source_map,
        defect_map,
        expression_map,
        caps,
        started,
        payload_durable_bytes,
    )
    checker_scheduler_projection = scheduler_projection(
        checker_scheduler_statistics, caps, "checker_scheduler"
    )
    if checker_scheduler_projection != producer_scheduler_projection:
        fail("staged_adjoint_statistics_mismatch")
    if (
        leaf_metadata["file"] != files["literal_leaves"]["file"]
        or leaf_metadata["schema"] != LEAF_SCHEMA
    ):
        fail("literal_leaf_receipt_pointer")
    compare_leaf_stream(loaded["literal_leaves"], leaves, ancestry_sha256)
    leaf_count = len(leaves)
    scheduler_totals = checker_scheduler_statistics["totals"]

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
        leaf_states_processed=scheduler_totals["expanded_states"],
        maximum_path_length=scheduler_totals["maximum_path_length"],
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
        "staged_adjoint_manifest_sha256": sha(canon(manifest["staged_adjoint"])),
        "staged_adjoint_projection_sha256": sha(canon(producer_scheduler_projection)),
        "staged_theorem_sha256": V475_SHA,
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
        payload_bytes=payload_durable_bytes,
    )
    print(json.dumps(verdict, sort_keys=True))
    return 0


def checker_scheduler_selftest() -> dict:
    base_caps = {
        "accumulated_states": 100,
        "interned_paths": 100,
        "path_length": 20,
        "durable_bytes": 1_000_000,
        "seconds": 60.0,
        "rss_bytes": 2**63 - 1,
    }

    def run(
        stages,
        roots,
        graph,
        caps=None,
        *,
        clock=None,
        started_at=None,
        durable_bytes=0,
        provider_calls=None,
        product_function=None,
    ):
        def provider(node):
            if provider_calls is not None:
                provider_calls[node] = provider_calls.get(node, 0) + 1
            return iter(graph.get(node, ()))

        return checker_staged_adjoint(
            stages,
            roots,
            provider,
            dict(base_caps if caps is None else caps),
            started_at=started_at,
            clock=time.monotonic if clock is None else clock,
            durable_bytes=durable_bytes,
            product=word_mul if product_function is None else product_function,
        )

    def leaf(seed=1, coefficient=1, word=()):
        return (None, seed, coefficient, tuple(word), "literal", None, None)

    def link(target, coefficient=1, word=()):
        return (target, None, coefficient, tuple(word), "link", None, None)

    def actor_link(target, source_pivot, target_pivot, word):
        return (
            target,
            None,
            1,
            tuple(word),
            "actor",
            source_pivot,
            target_pivot,
        )

    diamond_graph = {
        "a": (link("m", 1),),
        "b": (link("m", 2),),
        "m": (leaf(),),
    }
    cancelled, cancelled_stats = run(
        (("roots", ("a", "b")), ("merge", ("m",))),
        (("a", (), 1), ("b", (), 1)),
        diamond_graph,
    )
    if cancelled or cancelled_stats["totals"]["cancelled_states"] != 1:
        fail("checker_fixture_staged_diamond_cancel")

    third_graph = dict(diamond_graph)
    third_graph["c"] = (link("m", 1),)
    third, third_stats = run(
        (("roots", ("a", "b", "c")), ("merge", ("m",))),
        (("a", (), 1), ("b", (), 1), ("c", (), 1)),
        third_graph,
    )
    if third != {(1, ()): 1}:
        fail("checker_fixture_staged_diamond_third")

    captured_products = []

    def capture_product(left, right):
        product = word_mul(left, right)
        captured_products.append(product)
        return product

    actor, actor_stats = run(
        (("actor", ("a",)), ("terminal", ("m",))),
        (("a", (1,), 1),),
        {"a": (actor_link("m", 1, 0, (-1, 2)),), "m": (leaf(),)},
        product_function=capture_product,
    )
    if (
        actor != {(1, (2,)): 1}
        or len(captured_products) != 1
        or next(iter(actor))[1] is not captured_products[0]
    ):
        fail("checker_fixture_staged_actor_cancellation")

    raw_path = [1, 2]
    raw_leaf, _ = run(
        (("raw", ("a",)),),
        (("a", raw_path, 1),),
        {"a": (leaf(),)},
    )
    raw_leaf_path = next(iter(raw_leaf))[1]
    if type(raw_leaf_path) is not tuple or raw_leaf_path != (1, 2):
        fail("checker_fixture_staged_raw_path_canonicalization")
    for bad_path, expected in (
        ((1, -1), "checker_staged_path_not_reduced"),
        ((3,), "checker_staged_path_letter"),
    ):
        try:
            run((("raw", ("a",)),), (("a", bad_path, 1),), {})
        except RuntimeError as exc:
            if str(exc) != expected:
                raise
        else:
            fail("checker_fixture_staged_raw_path_gate")

    coefficient_two, coefficient_stats = run(
        (("coefficient", ("a",)),),
        (("a", (), 2),),
        {"a": (leaf(),)},
    )
    if coefficient_two != {(1, ()): 2}:
        fail("checker_fixture_staged_coefficient_two")

    provider_calls = {}
    distinct, distinct_stats = run(
        (("roots", ("a", "b")), ("merge", ("m",))),
        (("a", (), 1), ("b", (), 1)),
        {
            "a": (link("m", word=(1,)),),
            "b": (link("m", word=(2,)),),
            "m": (leaf(),),
        },
        provider_calls=provider_calls,
    )
    if len((1,)) != len((2,)) or distinct != {
        (1, (1,)): 1,
        (1, (2,)): 1,
    } or distinct_stats["totals"]["state_edge_traversals"] != 4 or provider_calls.get(
        "m"
    ) != 2:
        fail("checker_fixture_staged_exact_words")

    bad_cases = (
        (
            "checker_staged_reduction_not_earlier",
            (("bad", ("a", "b")),),
            {"a": (("b", None, 1, (), "reduction", 0, 0),)},
        ),
        (
            "checker_staged_actor_parent_not_earlier",
            (("bad", ("a", "b")),),
            {"a": (("b", None, 1, (1,), "actor", 0, 0),)},
        ),
        (
            "checker_staged_processed_destination",
            (("cycle", ("a", "b")),),
            {"a": (link("b"),), "b": (link("a"),)},
        ),
    )
    for expected, stages, graph in bad_cases:
        try:
            run(stages, (("a", (), 1),), graph)
        except RuntimeError as exc:
            if str(exc) != expected:
                raise
        else:
            fail("checker_fixture_staged_bad_edge_not_rejected")

    resource_cases = [
        (
            (("roots", ("a", "b")),),
            (("a", (), 1), ("b", (), 1)),
            {},
            dict(base_caps, accumulated_states=1),
            None,
            None,
        ),
        (
            (("path", ("a",)),),
            (("a", (1,), 1),),
            {},
            dict(base_caps, interned_paths=1),
            None,
            None,
        ),
        (
            (("path", ("a",)),),
            (("a", (1, 2), 1),),
            {},
            dict(base_caps, path_length=1),
            None,
            None,
        ),
        (
            (("time", ("a",)),),
            (("a", (), 1),),
            {},
            dict(base_caps, seconds=0.5),
            lambda: 1.0,
            0.0,
        ),
        (
            (("durable", ("a",)),),
            (("a", (), 1),),
            {},
            dict(base_caps, durable_bytes=1),
            None,
            None,
            2,
        ),
    ]
    for case in resource_cases:
        stages, roots, graph, caps, *resource_options = case
        try:
            run(
                stages,
                roots,
                graph,
                caps,
                clock=resource_options[0],
                started_at=resource_options[1],
                durable_bytes=(
                    resource_options[2] if len(resource_options) > 2 else 0
                ),
            )
        except UnknownResource as exc:
            if not str(exc).startswith("UNKNOWN_RESOURCE:"):
                raise
        else:
            fail("checker_fixture_staged_resource_cap_not_rejected")

    production_stage_names = (
        "physical-grade",
        "physical-lower",
        "block-0",
        "block-1",
        "block-2",
        "block-3",
        "defect",
        "old-0",
        "old-1",
        "old-2",
        "old-3",
    )
    projection_stages = tuple(
        (name, ("a",) if index == 0 else ())
        for index, name in enumerate(production_stage_names)
    )
    _, projection_statistics = run(
        projection_stages,
        (("a", (), 1),),
        {"a": (leaf(),)},
    )
    projection = scheduler_projection(
        projection_statistics, base_caps, "checker_fixture_scheduler"
    )
    if (
        projection["totals"]["expanded_states"] != 1
        or projection["totals"]["state_edge_traversals"] != 1
    ):
        fail("checker_fixture_scheduler_projection")

    if checker_inclusive_durable_total(9, b"x", 10) != 10:
        fail("checker_fixture_manifest_inclusive_total")
    try:
        checker_inclusive_durable_total(10, b"x", 10)
    except RuntimeError as exc:
        if str(exc) != "manifest_receipts":
            raise
    else:
        fail("checker_fixture_manifest_byte_cap")

    positive = (
        cancelled_stats,
        third_stats,
        actor_stats,
        coefficient_stats,
        distinct_stats,
    )
    return {
        "fixtures": 9,
        "positive_expanded_states": sum(
            item["totals"]["expanded_states"] for item in positive
        ),
        "positive_maximum_live_entries": max(
            item["totals"]["maximum_live_entries"] for item in positive
        ),
        "positive_state_edge_traversals": sum(
            item["totals"]["state_edge_traversals"] for item in positive
        ),
        "resource_caps_rejected": len(resource_cases),
        "statistics_projection": "PASS",
        "two_path_provider_calls": provider_calls["m"],
        "canonical_tuple_reuse": "PASS",
        "raw_word_gates": "PASS",
        "manifest_inclusive_cap": "PASS",
    }


def selftest() -> int:
    scheduler_fixture = checker_scheduler_selftest()
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
                "staged_scheduler": scheduler_fixture,
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
    except UnknownResource as exc:
        try:
            os.write(2, (str(exc) + "\n").encode("ascii", "replace")[:1024])
        except BaseException:
            pass
        return 2
    except MemoryError:
        emergency_unknown_resource()
        return 2
    except Exception as exc:
        print(json.dumps({"status": "REJECTED", "error": str(exc)}), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
