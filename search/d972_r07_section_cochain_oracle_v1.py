#!/usr/bin/env python3
"""Task959: one accepted separator, complete v548 source-cochain oracle.

All outputs are candidates. A--D export every finite scalar equation.
Selected cycle/word/P1/physical materialization E is deliberately pending.
Only own retained producer primitives are imported, never a checker solver.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import signal
import sys
import time
from typing import Any
import uuid

import numpy as np

SCHEMA = "d972.r07.section-cochain-oracle.v1"
SEARCH = Path(__file__).resolve().parent
PROJECT = SEARCH.parent
REFINEMENT_MODULE = "d972_r07_full_origin_refinement_v1.py"
REFINEMENT_MODULE_SHA = "d7e32aad9a9667c6af54ed7514d0417e48b3e363c60652ab585ce4633f2aedfa"
N, EDGES, CHORDS = 54432, 108864, 54433
P1_ROWS, LOWER, TOP, PHYSICAL = 8059, 96776, 36288, 48384
OLD_RANKS, NEW_RANKS = (505, 503, 503, 503), (1509, 1512, 1512, 1512)
OLD_OFFSETS, NEW_OFFSETS = (0, 505, 1008, 1511), (2014, 3523, 5035, 6547)
CHARACTERS = ((0, 0), (0, 1), (1, 0), (1, 1))
SENTINEL = 4294967295
ASSURANCE = {"candidate": True, "cross_checked": False, "verified": False}
FORMULA = "v548:section-corrected-homogeneous-dual;v546:five-carry;v543:complete-tree"
SCOPE = {"vertices": N, "positive_edges": EDGES, "chords": CHORDS, "legality_rows": 5,
    "normalized_auxiliaries": 2, "p1_rows": P1_ROWS, "characters": [0, 1, 2, 3],
    "source_tags": 6, "snapshot_count": 1, "complete_finite_test": True, "physical_appends": 0}
# Observed completion candidate: the saved producer prefix is unchanged.
REFINEMENT_ARTIFACT: dict[str, Any] = {
    "run": 33971897879, "attempt": 1,
    "head": "64475e1dfab1537a38d1b3131971bfed5fc3071c", "id": 9971466432,
    "name": "d972-r07-full-origin-checker-completion-v1-candidate-33971897879-1",
    "bytes": 51943596,
    "sha256": "sha256:0d4af3475ca62da1d7436246bd36109d380e0a463a713de1c1e3db69f90c9db8",
}
REFINEMENT_FILES: dict[str, tuple[int, str]] = {
    "output/HEAD": (921, "6bf3b4fce6a3f159563c13a9aa50f6478827fbad1af13d820b70359b3b2f5cba"),
    "output/result.json": (3988, "04a88c1423f6d99f5e94ded601d20efa5b338ba2b4fae8e9f73023695cd69211"),
    "output/start.json": (11011, "1a709c2853a6d0c239bc31d50ba6e03b0fb4707d93b625d291a487e6d43dc131"),
    "output/owner.json": (8432, "c4fd8b27590450d0b73e72efe9d45bf9319e111b5e21d1f3ff0b0ee23910f48c"),
    "output/source.json": (1139, "7e99018f58f3f49e371b55e6daab491b71855bb463c8c47cd872dffb57b5774f"),
    "output/canonical-index.json": (6078393, "452fe97a9229fa5188493256d1478ead1e684b495bbfed0db03a64f5acf4f00e"),
    "source-receipt.json": (2355, "5d65f4313aaed81f30354cba5c90ead201816f72f15fcd799606ed5feab43f3e"),
    "checker-result.json": (57583, "ccb0b3dd225587dde0e08edca5dfa66b1446b7db01091a3e8118c7aeb4ed2e9c"),
    "completion-run-receipt.json": (1849, "b1c653283593a2fdef835c938bcc0c8502248b53c92d264842a2133bd4561e57"),
    "preserved-input.json": (183567, "746e097f23c78418a3b43754348099a753639fcceac006e4f1d634ad3fb57298"),
}
REFINEMENT_SNAPSHOT: dict[str, Any] = {
    "completed_steps": 26, "terminal": "UNKNOWN_RESOURCE", "rank": 1385, "generation": 8090,
    "state_head": "8f6605a28d337cd8541a7eacf6aef78f5a70308a6bb71fd105138803ca623a61",
    "lambda_sha256": "1e720af4a30bac955ab4565366f0242b5c2d43125eb280e241df20976331cdf1",
    "target_remainder_sha256": "111d12e064b96a6bf579f39a9c9d5e35181560c0403bf0d237bffc924230c0ad",
}
STARTED = time.monotonic()
DEADLINE: float | None = None
STOP_REQUESTED = False


class ResourceStop(RuntimeError):
    pass


def require(condition: bool, reason: str) -> None:
    if not condition:
        raise RuntimeError(reason)


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":")) + "\n").encode("ascii")


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def seal(kind: str, body: dict[str, Any]) -> dict[str, Any]:
    require("schema" not in body and "sha256" not in body, "seal_reserved_fields")
    unsigned = {"schema": SCHEMA + "." + kind, **body}
    return {**unsigned, "sha256": sha(canonical(unsigned))}


def sealed_ok(value: Any, kind: str | None = None) -> bool:
    return isinstance(value, dict) and (kind is None or value.get("schema") == SCHEMA + "." + kind) and \
        value.get("sha256") == sha(canonical({k: v for k, v in value.items() if k != "sha256"}))


def check_deadline(phase: str) -> None:
    if STOP_REQUESTED or (DEADLINE is not None and time.monotonic() >= DEADLINE):
        raise ResourceStop(phase)


def progress(phase: str, **fields: Any) -> None:
    print(json.dumps({"phase": phase, "elapsed_seconds": round(time.monotonic() - STARTED, 3), **fields},
                     sort_keys=True), file=sys.stderr, flush=True)
    check_deadline(phase)


def safe_file(root: Path, name: str) -> Path:
    require(isinstance(name, str) and name and not Path(name).is_absolute() and
            all(part not in ("", ".", "..") for part in name.replace("\\", "/").split("/")), "relative_file_name")
    path = root / name
    require(path.is_file() and not path.is_symlink() and not any(p.is_symlink() for p in path.parents),
            "regular_file:" + name)
    return path


def read_fixed(root: Path, name: str, pin: tuple[int, str]) -> bytes:
    path = safe_file(root, name)
    require(path.stat().st_size == pin[0], "file_size:" + name)
    raw = path.read_bytes()
    require(sha(raw) == pin[1], "file_sha256:" + name)
    return raw


def json_bytes(raw: bytes) -> Any:
    value = json.loads(raw.decode("ascii"))
    require(canonical(value) == raw, "canonical_json_bytes")
    return value


def read_json(root: Path, name: str) -> Any:
    path = safe_file(root, name)
    require(path.stat().st_size <= 1 << 28, "json_cap")
    return json_bytes(path.read_bytes())


def file_pin(path: Path) -> dict[str, Any]:
    require(path.is_file() and not path.is_symlink(), "pin_regular_file")
    digest, count = hashlib.sha256(), 0
    with path.open("rb") as stream:
        while True:
            raw = stream.read(1 << 20)
            if not raw:
                break
            digest.update(raw)
            count += len(raw)
            check_deadline("file-pin:" + path.name)
    return {"bytes": count, "sha256": digest.hexdigest()}


def pack(row: np.ndarray) -> bytes:
    values = np.asarray(row, dtype=np.uint8).reshape(-1)
    require(values.size % 4 == 0 and not np.any(values > 2), "pack_trits")
    groups = values.reshape(-1, 4).astype(np.uint16)
    return (groups[:, 0] + 3 * groups[:, 1] + 9 * groups[:, 2] + 27 * groups[:, 3]).astype(np.uint8).tobytes()


def unpack(raw: bytes, width: int) -> np.ndarray:
    data = np.frombuffer(raw, dtype=np.uint8)
    require(len(raw) * 4 == width and not np.any(data >= 81), "packed_shape_or_encoding")
    return ((data[:, None] // np.asarray((1, 3, 9, 27), dtype=np.uint8)) % 3).reshape(-1).copy()


def dot(left: np.ndarray, right: np.ndarray) -> int:
    require(left.size == right.size, "dot_shape")
    return int(np.sum(left.reshape(-1).astype(np.uint32) * right.reshape(-1).astype(np.uint32), dtype=np.uint64) % 3)


def sync_directory(path: Path) -> None:
    if os.name != "nt":
        fd = os.open(path, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
        try:
            os.fsync(fd)
        finally:
            os.close(fd)


def write_atomic(root: Path, name: str, raw: bytes, replace: bool = False) -> None:
    require(Path(name).name == name and name not in ("", ".", "..") and not root.is_symlink(), "output_name")
    target = root / name
    require(not target.is_symlink() and (replace or not target.exists()), "output_fresh_file")
    pending = root / ("." + name + ".pending-" + uuid.uuid4().hex)
    with pending.open("xb") as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(pending, target)
    sync_directory(root)


def array_payload(value: Any, dtype: str) -> tuple[bytes, str, Any]:
    if dtype == "json":
        return canonical(value), dtype, None
    array = np.asarray(value)
    if dtype == "u8":
        require(np.all((array >= 0) & (array <= 2)), "u8_trits")
        raw = array.astype(np.uint8).tobytes(order="C")
    elif dtype == "u32le":
        require(np.all((array >= 0) & (array <= SENTINEL)), "u32_range")
        raw = array.astype("<u4").tobytes(order="C")
    else:
        require(dtype == "packed3", "array_dtype")
        raw = pack(array)
    return raw, dtype, list(array.shape)


def write_stage(output: Path, stage: str, owner_sha: str, snapshot_sha: str,
                inputs: dict[str, str], payloads: dict[str, tuple[bytes, str, Any]]) -> Any:
    check_deadline("before-stage:" + stage)
    require(not (output / stage).exists(), "stage_fresh")
    pending = output / ("." + stage + ".pending-" + uuid.uuid4().hex)
    pending.mkdir()
    files = []
    for name in sorted(payloads):
        raw, dtype, shape = payloads[name]
        write_atomic(pending, name, raw)
        files.append({"file": name, "bytes": len(raw), "sha256": sha(raw), "dtype": dtype, "shape": shape})
        check_deadline("stage-file:" + stage + "/" + name)
    manifest = seal("stage-manifest", {"stage": stage, "owner_sha256": owner_sha,
        "snapshot_sha256": snapshot_sha, "inputs": inputs, "files": files})
    write_atomic(pending, "manifest.json", canonical(manifest))
    os.replace(pending, output / stage)
    sync_directory(output)
    progress("stage-durable", stage=stage, files=len(files))
    return manifest


def own_dependencies() -> Any:
    path = safe_file(SEARCH, REFINEMENT_MODULE)
    require(sha(path.read_bytes()) == REFINEMENT_MODULE_SHA, "refinement_producer_pin")
    if str(SEARCH) not in sys.path:
        sys.path.insert(0, str(SEARCH))
    spec = importlib.util.spec_from_file_location("task959_own_refinement", path)
    require(spec is not None and spec.loader is not None, "own_import_spec")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    module.check_deadline = check_deadline
    p2 = module.fixed_module()
    p2.check_deadline = check_deadline
    m, base, descriptors = p2.dependencies()
    return module, p2, m, base, descriptors


def qid(context: Any, value: Any) -> int:
    p, e0, e1, k = value
    return ((2 * int(e0) + int(e1)) * 27 + 9 * int(k[0]) + 3 * int(k[1]) + int(k[2])) * 504 + context.psidx[p]


def coordinates() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    indices = np.arange(N, dtype=np.int64)
    p = indices % 504
    parity = indices // (504 * 27)
    kid = (indices // 504) % 27
    kernel = np.stack((kid // 9, (kid // 3) % 3, kid % 3), axis=1)
    return p, parity, kernel


def sign_vectors(parity: np.ndarray) -> np.ndarray:
    e0, e1 = parity // 2, parity % 2
    return np.stack((1 - 2 * e1, 1 - 2 * e0, 1 - 2 * (e0 ^ e1)), axis=-1)


class RightMaps:
    """Right multiplication in the registered qid universe, never pmap(left)."""
    def __init__(self, arith: Any, context: Any):
        self.arith, self.context = arith, context
        self.p, self.parity, self.kernel = coordinates()
        self.cache: dict[int, np.ndarray] = {}

    def at(self, value: Any) -> np.ndarray:
        key = qid(self.context, value)
        if key not in self.cache:
            pmap = np.asarray([self.context.psidx[self.arith._seed_perm_mul(p, value[0])]
                               for p in self.context.psels], dtype=np.int64)
            hp = 2 * value[1] + value[2]
            signs = sign_vectors(np.asarray(hp, dtype=np.int64))
            kernel = (self.kernel * signs + np.asarray(value[3], dtype=np.int64)) % 3
            kid = 9 * kernel[:, 0] + 3 * kernel[:, 1] + kernel[:, 2]
            self.cache[key] = (((self.parity ^ hp) * 27 + kid) * 504 + pmap[self.p]).astype(np.uint32)
        return self.cache[key]


def validate_marking(arith: Any, context: Any) -> str:
    data_path = safe_file(PROJECT, "scratchpad/fuda1_a0_rmax_data.g")
    raw = data_path.read_bytes()
    expected = "625b4d11ca882c9419d9e0d78510bf323a117673722b8dd9ec7d7e85554267ba"
    require(len(raw) == 4709 and sha(raw) == expected, "actual_q0_marking_pin")
    match = re.search(r"FUDA1_Q0PERMS\s*:=\s*(\[\s*\[.*?\]\s*,\s*\[.*?\]\s*\])\s*;;",
                      raw.decode("ascii"), re.S)
    require(match is not None, "actual_q0_marking_parse")
    q36 = json.loads(match.group(1))
    require(len(q36) == 2 and all(len(row) == 36 for row in q36), "actual_q0_marking_shape")
    for slot, (parity, k9) in enumerate(((2, (1, 0, 0)), (1, (1, 1, 1)))):
        signs = sign_vectors(np.asarray(parity, dtype=np.int64))
        expected_row = [int(x) + 1 for x in context.images[slot][0]]
        for block in range(3):
            expected_row.extend(10 + 9 * block + (int(signs[block]) * u + k9[block]) % 9 for u in range(9))
        require(expected_row == q36[slot] and tuple(context.images[slot][3]) == k9,
                "actual_q0_full36_section_kernel_marking")
    require(arith._seed_affine_mul(context.images[0], context.pb3_b) ==
            arith._seed_affine_inv(context.images[1]), "actual_qnorm_XB_equals_Yinverse")
    return expected


def positive_tree(next_pos: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    count = next_pos.shape[0]
    require(next_pos.shape == (count, 2) and np.all(next_pos < count), "tree_successor_shape")
    parent = np.full(count, SENTINEL, dtype=np.uint32)
    parent_edge = np.full(count, SENTINEL, dtype=np.uint32)
    seen = np.zeros(count, dtype=bool)
    seen[0] = True
    order = [0]
    cursor = 0
    while cursor < len(order):
        tail = order[cursor]
        cursor += 1
        for slot in range(2):
            head = int(next_pos[tail, slot])
            if not seen[head]:
                seen[head] = True
                parent[head], parent_edge[head] = tail, 2 * tail + slot
                order.append(head)
        if cursor % 4096 == 0:
            check_deadline("positive-bfs")
    require(len(order) == count and np.all(seen) and len(np.unique(parent_edge[1:])) == count - 1,
            "positive_bfs_complete_tree")
    is_tree = np.zeros(2 * count, dtype=bool)
    is_tree[parent_edge[1:]] = True
    chord_edges = np.flatnonzero(~is_tree).astype(np.uint32)
    require(chord_edges.size == count + 1, "positive_bfs_chord_eof")
    return parent, parent_edge, np.asarray(order, dtype=np.uint32), chord_edges


def geometry_inputs(arith: Any, context: Any) -> Any:
    marking_sha = validate_marking(arith, context)
    maps = RightMaps(arith, context)
    next_pos = np.stack([maps.at(x) for x in context.images], axis=1)
    prev_pos = np.empty_like(next_pos)
    for slot in range(2):
        require(np.array_equal(np.sort(next_pos[:, slot]), np.arange(N)), "right_positive_bijection")
        prev_pos[next_pos[:, slot], slot] = np.arange(N, dtype=np.uint32)
        require(np.array_equal(prev_pos[:, slot], maps.at(arith._seed_affine_inv(context.images[slot]))),
                "right_inverse_permutation")
    parent, parent_edge, bfs_order, chord_edges = positive_tree(next_pos)
    require(chord_edges.size == CHORDS, "actual_tree_chord_count")
    phi = np.empty((6, N), dtype=np.uint32)
    tags = []
    for tag, words in enumerate(arith.SEED_OO):
        endpoints, terms = [], []
        for word in words:
            gradient, endpoint = arith._seed_affine_fox(tuple(word), context.images)
            endpoints.append(endpoint)
            terms.append([[int(c), qid(context, h), int(d)] for (c, h), d in gradient.items()])
        rights = [maps.at(x) for x in endpoints]
        phi[tag, 0] = 0
        for done, vertex0 in enumerate(bfs_order[1:], 1):
            vertex = int(vertex0)
            phi[tag, vertex] = rights[int(parent_edge[vertex]) % 2][phi[tag, parent[vertex]]]
            if done % 8192 == 0:
                check_deadline("tag-tree-map")
        require(np.array_equal(np.sort(phi[tag]), np.arange(N)), "tag_map_bijection")
        for slot in range(2):
            require(np.array_equal(phi[tag, next_pos[:, slot]], rights[slot][phi[tag]]),
                    "tag_map_all_positive_edges")
        tags.append({"tag": tag, "words": [list(x) for x in words],
                     "images": [qid(context, x) for x in endpoints], "fox": terms})
        progress("geometry-tag", tag=tag, vertices=N, edges=EDGES)
    require(np.array_equal(phi[0], np.arange(N)) and np.array_equal(phi[4], np.arange(N)),
            "duplicate_identity_tags_retained")
    p, parity, kernel = maps.p, maps.parity, maps.kernel
    signs = sign_vectors(parity)
    rotation = (signs * kernel) % 3
    carry = np.zeros((N, 2, 5), dtype=np.uint8)
    for slot, rotation9 in enumerate(((1, 0, 0), (8, 1, 8))):
        numerator = rotation + signs * np.asarray(rotation9, dtype=np.int64)
        reduced = numerator % 3
        head = next_pos[:, slot]
        require(np.array_equal(reduced, rotation[head]), "carry_actual_successor_rotation")
        carry[:, slot, :3] = ((numerator - reduced) // 3) % 3
        carry[:, slot, 3 + slot] = 1
    qnorm_second = maps.at(context.pb3_b)[next_pos[:, 0]]
    require(np.array_equal(qnorm_second, prev_pos[:, 1]), "all_vertex_qnorm_right_XB_identity")
    metadata = seal("geometry", {"vertices": N, "edges": EDGES, "tree_edges": N - 1, "chords": CHORDS,
        "characters": [list(x) for x in CHARACTERS], "actors": [1, 2],
        "qid_order": "parity,k-base3,psl-fastest", "edge_order": "2*q+slot", "tree_order": "positive-bfs-X,Y",
        "chord_order": "edge-id-ascending", "group_convention": "section-left/kernel-right;perm=right[left[i]]",
        "fox_convention": "left-prefix;positive-edge-right-product",
        "carry_convention": "rotation-left;integer-carry-before-mod3", "sentinel": SENTINEL,
        "transport": [[list(context.transport[t][a]) for a in CHARACTERS] for t in range(6)],
        "q0_marking_sha256": marking_sha,
        "psl_elements_sha256": sha(canonical([list(x) for x in context.psels])),
        "full_vertex_eof": True, "full_edge_eof": True, "all_phi_edges_checked": True,
        "phi_bijections": 6, "qnorm_right_identity_checked": True})
    arrays = {"next-pos.u32": (next_pos, "u32le"), "prev-pos.u32": (prev_pos, "u32le"),
        "phi.u32": (phi, "u32le"), "parent.u32": (parent, "u32le"),
        "parent-edge.u32": (parent_edge, "u32le"), "bfs-order.u32": (bfs_order, "u32le"),
        "carry.u8": (carry.reshape(EDGES, 5), "u8"), "chord-edges.u32": (chord_edges, "u32le"),
        "geometry.json": (metadata, "json"), "tag-fox.json": ({"tags": tags}, "json")}
    return {"arrays": arrays, "next": next_pos, "prev": prev_pos, "phi": phi,
        "parent": parent, "parent_edge": parent_edge, "order": bfs_order, "chords": chord_edges,
        "carry": carry.reshape(EDGES, 5), "tags": tags, "maps": maps}


class PackedRows:
    def __init__(self, root: Path, descriptor: dict[str, Any]):
        self.path = safe_file(root, descriptor["file"])
        self.rows, self.width = descriptor["rows"], descriptor["width"]
        require(self.width % 4 == 0 and descriptor["bytes"] == self.rows * self.width // 4 and
                file_pin(self.path) == {k: descriptor[k] for k in ("bytes", "sha256")}, "packed_blob_pin")
        self.stream = self.path.open("rb", buffering=1 << 20)

    def row(self, index: int) -> np.ndarray:
        require(0 <= index < self.rows, "packed_row_index")
        self.stream.seek(index * (self.width // 4))
        return unpack(self.stream.read(self.width // 4), self.width)

    def close(self) -> None:
        self.stream.close()


def interpolate_rows(width: int, leads: list[int], values: np.ndarray, row_at: Any) -> tuple[np.ndarray, list[int]]:
    """Use original leads; insertion order is an ID, not a triangular order."""
    require(len(leads) == len(values) and len(set(leads)) == len(leads) and
            all(type(x) is int and 0 <= x < width for x in leads), "interpolation_leads")
    answer = np.zeros(width, dtype=np.uint8)
    order = sorted(range(len(leads)), key=lambda i: leads[i], reverse=True)
    for count, index in enumerate(order):
        row = row_at(index)
        lead = leads[index]
        require(row.shape == (width,) and not np.any(row > 2) and row[lead] == 1 and
                not np.any(row[:lead]) and answer[lead] == 0, "normalized_original_lead")
        answer[lead] = (int(values[index]) - dot(answer, row)) % 3
        if (count + 1) % 256 == 0:
            check_deadline("dual-original-lead-interpolation")
    return answer, order


def current_roots_and_values(base: Any, tables: Any, state: Any, p1: Any) -> tuple[np.ndarray, np.ndarray]:
    q = np.asarray([base.ARITH.sparse_adjoint(table["forward"]["B"], TOP, PHYSICAL, state["lambda"])
                    for table in tables], dtype=np.uint8)
    require(q.shape == (4, TOP) and not np.any(q > 2), "all_four_fresh_B_adjoints")
    values = np.empty((4, P1_ROWS), dtype=np.uint8)
    digest, count = hashlib.sha256(), 0
    path = safe_file(p1["root"], p1["cache"]["path"])
    require(path.stat().st_size == P1_ROWS * TOP == p1["cache"]["bytes"], "p1_cache_size")
    with path.open("rb", buffering=1 << 20) as stream:
        for begin in range(0, P1_ROWS, 16):
            size = min(16, P1_ROWS - begin)
            raw = stream.read(size * TOP)
            require(len(raw) == size * TOP, "p1_contraction_chunk_eof")
            digest.update(raw)
            count += len(raw)
            dense = unpack(raw, size * 4 * TOP).reshape(size, 4, TOP)
            for character in range(4):
                products = dense[:, character, :].astype(np.uint32) * q[character].astype(np.uint32)
                values[character, begin:begin + size] = np.sum(products, axis=1, dtype=np.uint64) % 3
            del dense, products
            if (begin + size) % 256 == 0 or begin + size == P1_ROWS:
                progress("current-section-p1", rows=begin + size, total=P1_ROWS)
        require(stream.read(1) == b"", "p1_contraction_full_eof")
    require(count == p1["cache"]["bytes"] and digest.hexdigest() == p1["cache"]["sha256"], "p1_contraction_cache_pin")
    return q, values


def current_section(base: Any, tables: Any, state: Any, p1: Any, task554: Any) -> Any:
    q, values = current_roots_and_values(base, tables, state, p1)
    chi = (np.sum(values, axis=0, dtype=np.uint32) % 3).astype(np.uint8)
    k1 = np.zeros((4, 18144), dtype=np.uint8)
    original = np.zeros(P1_ROWS, dtype=np.uint32)
    embedded = np.zeros(P1_ROWS, dtype=np.uint32)
    new_order, new_metadata = [], []
    # A parsed Task554 body is released before the next one is opened.
    for owner in range(4):
        block = base._state_descriptor(task554["blocks"][owner], owner, need_blobs=True)
        leads = [int(x) for x in block["body"]["pivot_leads"]]
        require(len(leads) == NEW_RANKS[owner] and
                all(node["pivot"] == i and node["lead"] == leads[i]
                    for i, node in enumerate(block["body"]["dag_nodes"])), "new_original_lead_join")
        descriptor, root = copy.deepcopy(block["body"]["basis_blob"]), block["root"]
        del block
        rows = PackedRows(root, descriptor)
        try:
            begin = NEW_OFFSETS[owner]
            k1[owner], order = interpolate_rows(18144, leads, chi[begin:begin + len(leads)], rows.row)
        finally:
            rows.close()
        for local, lead in enumerate(leads):
            original[begin + local] = lead
            embedded[begin + local] = 24192 + owner * 18144 + lead
        new_order.extend(begin + local for local in order)
        new_metadata.append({"root": root, "descriptor": descriptor, "leads": leads})
        progress("current-section-new", owner=owner, rows=len(leads))
    prepare = base._state_descriptor(task554["prepare"], -1, need_blobs=True)
    old_metadata = []
    for owner, old in enumerate(prepare["body"]["old_blocks"]):
        nodes = old["record"]["dag_nodes"]
        leads = [int(node["lead"]) for node in nodes]
        require(len(leads) == OLD_RANKS[owner] and all(node["pivot"] == i for i, node in enumerate(nodes)),
                "old_original_lead_join")
        old_metadata.append({"root": prepare["root"], "leads": leads,
            "lower": copy.deepcopy(old["lower_basis_blob"]), "grade": copy.deepcopy(old["lifted_grade_blob"])})
    del nodes, old, prepare
    beta = np.empty(2014, dtype=np.uint8)
    old_leads = [0] * 2014
    old_owner_local = [(-1, -1)] * 2014
    lower_rows = []
    try:
        for owner, meta in enumerate(old_metadata):
            low = PackedRows(meta["root"], meta["lower"])
            lower_rows.append(low)
            grade = PackedRows(meta["root"], meta["grade"])
            try:
                for local, lead in enumerate(meta["leads"]):
                    index = OLD_OFFSETS[owner] + local
                    require(0 <= lead < 6056, "old_original_lead_range")
                    beta[index] = (int(chi[index]) - dot(k1, grade.row(local))) % 3
                    old_leads[index] = owner * 6048 + lead if lead < 6048 else 24192 + lead - 6048
                    original[index] = lead
                    embedded[index] = owner * 6048 + lead if lead < 6048 else 96768 + lead - 6048
                    old_owner_local[index] = owner, local
                    if (local + 1) % 128 == 0:
                        check_deadline("old-grade-beta")
            finally:
                grade.close()

        def old_row(index: int) -> np.ndarray:
            owner, local = old_owner_local[index]
            raw = lower_rows[owner].row(local)
            lead = int(original[index])
            require(raw[lead] == 1 and not np.any(raw[:lead]) and
                    (owner == 0 or not np.any(raw[6048:])), "old_shared_aux_original_lead")
            value = np.zeros(24200, dtype=np.uint8)
            value[owner * 6048:(owner + 1) * 6048] = raw[:6048]
            value[24192:] = raw[6048:]
            return value

        kE, old_order = interpolate_rows(24200, old_leads, beta, old_row)
        kappa = np.concatenate((kE[:24192], k1.reshape(-1), kE[24192:]))
        require(kappa.shape == (LOWER,), "joint_kappa_shape")
        equations = np.empty(P1_ROWS, dtype=np.uint8)
        # Every dot is checked against the final, identical joint kappa.
        for owner, meta in enumerate(old_metadata):
            grade = PackedRows(meta["root"], meta["grade"])
            try:
                for local in range(OLD_RANKS[owner]):
                    index = OLD_OFFSETS[owner] + local
                    equations[index] = (dot(kE, old_row(index)) + dot(k1, grade.row(local))) % 3
                    if (local + 1) % 128 == 0:
                        check_deadline("final-old-kappa-equalities")
            finally:
                grade.close()
    finally:
        for rows in lower_rows:
            rows.close()
    for owner, meta in enumerate(new_metadata):
        rows = PackedRows(meta["root"], meta["descriptor"])
        try:
            for local in range(NEW_RANKS[owner]):
                equations[NEW_OFFSETS[owner] + local] = dot(k1[owner], rows.row(local))
                if (local + 1) % 256 == 0:
                    check_deadline("final-new-kappa-equalities")
        finally:
            rows.close()
    residuals = ((equations.astype(np.int16) - chi.astype(np.int16)) % 3).astype(np.uint8)
    require(not np.any(residuals) and len(new_order) == 6045 and len(old_order) == 2014 and
            len(set(int(x) for x in embedded)) == P1_ROWS, "all8059_joint_kappa_equalities")
    metadata = seal("section", {"rows": P1_ROWS, "old_rows": 2014, "new_rows": 6045,
        "source_lower_trits": LOWER, "shared_auxiliaries": 8,
        "formula": "v548:chi=sum_a<B_a^*lambda,z_i[a]>;kappa(b_i)=chi_i",
        "solve_order": "new-owner-major-descending-original-lead;old-global-descending-embedded-original-lead",
        "free_coordinates": 0, "p1_cache_sha256": p1["cache"]["sha256"],
        "lower_blob_pin_sha256": base.LOWER_BLOB_PIN_SHA256, "p1_passes": 1,
        "all_equations_checked": P1_ROWS, "equation_eof": True, "old_arithmetic_replayed": False})
    arrays = {"q.bin": (q, "packed3"), "p1-values.u8": (values, "u8"), "chi.u8": (chi, "u8"),
        "equation-values.u8": (equations, "u8"), "equation-residuals.u8": (residuals, "u8"),
        "beta.u8": (beta, "u8"), "kappa.bin": (kappa, "packed3"),
        "lead-original.u32": (original, "u32le"), "lead-embedded.u32": (embedded, "u32le"),
        "new-solve-order.u32": (np.asarray(new_order), "u32le"),
        "old-solve-order.u32": (np.asarray(old_order), "u32le"), "section.json": (metadata, "json")}
    progress("current-section-complete", equations=P1_ROWS)
    return {"arrays": arrays, "q": q, "kappa": kappa}


def score_array(arith: Any, context: Any, q: np.ndarray, kappa: np.ndarray) -> np.ndarray:
    require(q.shape == (4, TOP) and kappa.shape == (LOWER,), "source_adjoint_shapes")
    qview = q.reshape(4, 6, 2, 6, 504).astype(np.int32)
    k0 = kappa[:24192].reshape(4, 6, 2, 504).astype(np.int32)
    k1 = kappa[24192:96768].reshape(4, 6, 2, 3, 504).astype(np.int32)
    score = np.zeros((6, 2, 4, 27, 504), dtype=np.uint8)
    for parity_index, parity in enumerate(CHARACTERS):
        for kid in range(27):
            kernel = kid // 9, (kid // 3) % 3, kid % 3
            polynomial = arith._seed_e_poly(kernel).astype(np.int32)
            for tag in range(6):
                total = np.zeros((2, 504), dtype=np.int32)
                for character, label in enumerate(CHARACTERS):
                    sign = arith._seed_cv(context.transport[tag][label], parity)
                    top = np.sum(qview[character, tag] * polynomial[None, 4:, None], axis=1, dtype=np.int32)
                    lower = k0[character, tag] + np.sum(
                        k1[character, tag] * polynomial[None, 1:4, None], axis=1, dtype=np.int32)
                    total += sign * (top - lower)
                score[tag, :, parity_index, kid] = total % 3
        progress("source-score-parity", parity=parity_index, vertices=(parity_index + 1) * 27 * 504)
    return score.reshape(6, 2, N)


def affine_from_qid(context: Any, index: int) -> Any:
    require(0 <= index < N, "affine_qid")
    p, rest = index % 504, index // 504
    kid, parity = rest % 27, rest // 27
    return context.psels[p], parity // 2, parity % 2, (kid // 9, (kid // 3) % 3, kid % 3)


def raw_edge_pullback(context: Any, geometry: Any, score: np.ndarray, kappa: np.ndarray) -> np.ndarray:
    require(score.shape == (6, 2, N) and kappa.shape == (LOWER,), "raw_edge_pullback_shape")
    result = np.zeros((N, 2), dtype=np.int32)
    for tag in geometry["tags"]:
        index = tag["tag"]
        for slot, terms in enumerate(tag["fox"]):
            for component, prefix, coefficient in terms:
                # s = phi(q) * prefix. This is a right map applied to phi(q),
                # hence precisely LEFT translation of each fixed Fox prefix.
                s = geometry["maps"].at(affine_from_qid(context, prefix))[geometry["phi"][index]]
                if component == 0:
                    result[:, slot] += int(coefficient) * (
                        -score[index, 0, geometry["next"][s, 0]].astype(np.int32)
                        -score[index, 1, geometry["prev"][s, 1]].astype(np.int32)
                        -int(kappa[96768 + index]))
                else:
                    require(component == 1, "raw_fox_component")
                    result[:, slot] += int(coefficient) * score[index, 1, s].astype(np.int32)
            result[:, slot] %= 3
        progress("source-edge-tag", tag=index, edges=EDGES)
    return (result % 3).astype(np.uint8).reshape(EDGES)


def source_cochain(arith: Any, context: Any, geometry: Any, section: Any) -> Any:
    score = score_array(arith, context, section["q"], section["kappa"])
    f = raw_edge_pullback(context, geometry, score, section["kappa"])
    b_aux = ((-section["kappa"][96774:96776].astype(np.int16)) % 3).astype(np.uint8)
    metadata = seal("cochain", {"formula": "v548:sum_a q_a Psi2[a]-kappa Psi1", "tags": 6,
        "components": 2, "vertices": N, "edges": EDGES, "score_eof": True, "edge_eof": True,
        "shared_eta": True, "normalized_aux_rule": "b_aux=-kappa_aux[6:8];no-mod3-division-by18",
        "raw_edge_adapter": "tagged-Fox-left;right-X-XB-qnorm", "physical_mixed_C_used": False})
    return {"arrays": {"score.u8": (score, "u8"), "f.u8": (f, "u8"), "b-aux.u8": (b_aux, "u8"),
                       "cochain.json": (metadata, "json")}, "f": f, "b_aux": b_aux}


def integrate_tree(next_pos: np.ndarray, parent: np.ndarray, parent_edge: np.ndarray,
                   order: np.ndarray, values: np.ndarray) -> np.ndarray:
    count = len(parent)
    require(parent.shape == parent_edge.shape == order.shape == (count,) and
            values.shape[0] == 2 * count and int(order[0]) == 0 and
            np.array_equal(np.sort(order), np.arange(count)), "tree_integrate_shapes")
    potential = np.zeros((count, *values.shape[1:]), dtype=np.uint8)
    visited = np.zeros(count, dtype=bool)
    visited[0] = True
    require(int(parent[0]) == int(parent_edge[0]) == SENTINEL, "tree_root_sentinel")
    for done, head0 in enumerate(order[1:], 1):
        head = int(head0)
        tail, edge = int(parent[head]), int(parent_edge[head])
        require(0 <= tail < count and visited[tail] and edge // 2 == tail and
                int(next_pos[tail, edge % 2]) == head, "tree_parent_positive_edge")
        potential[head] = (potential[tail].astype(np.uint16) + values[edge].astype(np.uint16)) % 3
        visited[head] = True
        if done % 8192 == 0:
            check_deadline("tree-potential-integration")
    require(np.all(visited), "tree_potential_all_vertices")
    return potential


def chord_values(next_pos: np.ndarray, chords: np.ndarray, values: np.ndarray, potential: np.ndarray) -> np.ndarray:
    tails = chords.astype(np.int64) // 2
    heads = next_pos[tails, chords.astype(np.int64) % 2]
    return ((values[chords].astype(np.int16) + potential[tails].astype(np.int16)
             - potential[heads].astype(np.int16)) % 3).astype(np.uint8)


def first_independent(tau: np.ndarray) -> list[int]:
    require(tau.ndim == 2 and tau.shape[1] == 5 and not np.any(tau > 2), "five_tau_columns_shape")
    basis: dict[int, np.ndarray] = {}
    selected = []
    for index, column in enumerate(tau):
        row = column.astype(np.int16).copy()
        for coordinate in range(5):
            if row[coordinate] and coordinate in basis:
                row = (row - int(row[coordinate]) * basis[coordinate]) % 3
            elif row[coordinate]:
                row = (row * int(row[coordinate])) % 3
                basis[coordinate] = row
                selected.append(index)
                break
        if len(selected) == 5:
            return selected
        if (index + 1) % 4096 == 0:
            check_deadline("five-tau-independent-scan")
    raise RuntimeError("complete_tau_rank_is_not_five")


def solve_five(matrix: np.ndarray, rhs: np.ndarray) -> np.ndarray:
    require(matrix.shape == (5, 5) and rhs.shape == (5,), "five_solve_shape")
    aug = np.concatenate((matrix.astype(np.int16), rhs.astype(np.int16)[:, None]), axis=1) % 3
    for column in range(5):
        hits = np.flatnonzero(aug[column:, column])
        require(len(hits) > 0, "five_solve_singular")
        pivot = column + int(hits[0])
        aug[[column, pivot]] = aug[[pivot, column]]
        aug[column] = (int(aug[column, column]) * aug[column]) % 3
        for row in range(5):
            if row != column and aug[row, column]:
                aug[row] = (aug[row] - int(aug[row, column]) * aug[column]) % 3
    answer = aug[:, 5].astype(np.uint8)
    require(np.array_equal((matrix.astype(np.int32) @ answer.astype(np.int32)) % 3, rhs % 3), "five_solve_residual")
    return answer


def classify_complete(chords: np.ndarray, tau: np.ndarray, values: np.ndarray, residuals: np.ndarray,
                      selected: list[int], fit: np.ndarray, b_aux: np.ndarray, expected_chords: int,
                      eof: bool) -> tuple[str, Any, Any]:
    require(eof is True and len(chords) == expected_chords and values.shape == residuals.shape == (expected_chords,) and
            tau.shape == (expected_chords, 5) and b_aux.shape == (2,) and
            len(selected) == 5 and len(set(selected)) == 5 and
            np.all(np.diff(chords.astype(np.int64)) > 0), "complete_chord_roster_eof")
    calculated = ((values.astype(np.int32) - tau.astype(np.int32) @ fit.astype(np.int32)) % 3).astype(np.uint8)
    require(np.array_equal(calculated, residuals) and not np.any(residuals[selected]), "complete_chord_residual_identity")
    failed = np.flatnonzero(residuals)
    basis_ids = [int(chords[i]) for i in selected]
    first_failed = int(chords[int(failed[0])]) if len(failed) else None
    aux_hits = np.flatnonzero(b_aux)
    if len(aux_hits):
        coordinate = int(aux_hits[0])
        eta = [0, 0]
        eta[coordinate] = 1
        witness = seal("witness", {"kind": "auxiliary", "coordinate": coordinate,
            "cycles": [], "eta": eta, "tau": [0] * 5, "scalar": int(b_aux[coordinate]),
            "materialization": "MATERIALIZATION_PENDING"})
        terminal = "VIOLATION_CANDIDATE"
    elif len(failed):
        index = int(failed[0])
        matrix = tau[selected].T
        d = solve_five(matrix, tau[index])
        terms = [{"edge": int(chords[index]), "coefficient": 1}] + [
            {"edge": edge, "coefficient": (-int(c)) % 3} for edge, c in zip(basis_ids, d)]
        tau_check = (tau[index].astype(np.int32) - matrix.astype(np.int32) @ d.astype(np.int32)) % 3
        scalar = (int(values[index]) - sum(int(c) * int(values[i]) for c, i in zip(d, selected))) % 3
        require(not np.any(tau_check) and scalar == int(residuals[index]) and scalar in (1, 2),
                "six_cycle_tau_and_scalar")
        witness = seal("witness", {"kind": "chord", "failed_chord": int(chords[index]),
            "basis_chords": basis_ids, "basis_coefficients": [int(x) for x in d], "cycles": terms,
            "eta": [0, 0], "tau": [int(x) for x in tau_check], "scalar": scalar,
            "materialization": "MATERIALIZATION_PENDING"})
        terminal = "VIOLATION_CANDIDATE"
    else:
        witness = seal("witness", {"kind": "none", "cycles": [], "eta": [0, 0], "tau": [0] * 5,
            "scalar": 0, "materialization": "NOT_NEEDED_FOR_ZERO_TEST"})
        terminal = "COMPLETE_ZERO_CANDIDATE"
    metadata = seal("tree", {"vertices": expected_chords - 1, "tree_edges": expected_chords - 2,
        "chords": expected_chords, "independent_tau_columns": 5,
        "selection_order": "first-independent-chord;coordinate0-through4", "selected_chords": basis_ids,
        "fit": [int(x) for x in fit], "aux_values": [int(x) for x in b_aux],
        "first_failed_chord": first_failed, "residual_nonzero": int(len(failed)), "full_chord_eof": True,
        "terminal": terminal, "materialization": witness["materialization"]})
    return terminal, witness, metadata


def complete_tree_test(geometry: Any, cochain: Any) -> Any:
    f, carry = cochain["f"], geometry["carry"]
    p = integrate_tree(geometry["next"], geometry["parent"], geometry["parent_edge"], geometry["order"], f)
    pt = integrate_tree(geometry["next"], geometry["parent"], geometry["parent_edge"], geometry["order"], carry)
    chords = geometry["chords"]
    require(len(chords) == CHORDS, "complete_tree_fixed_chord_roster")
    r = chord_values(geometry["next"], chords, f, p)
    tau = chord_values(geometry["next"], chords, carry, pt)
    selected = first_independent(tau)
    fit = solve_five(tau[selected], r[selected])
    residuals = ((r.astype(np.int32) - tau.astype(np.int32) @ fit.astype(np.int32)) % 3).astype(np.uint8)
    check_deadline("all-chord-residuals-complete")
    terminal, witness, metadata = classify_complete(chords, tau, r, residuals, selected, fit,
                                                    cochain["b_aux"], CHORDS, True)
    arrays = {"potential-f.u8": (p, "u8"), "potential-tau.u8": (pt, "u8"),
        "chord-values.u8": (r, "u8"), "chord-tau.u8": (tau, "u8"), "chord-residuals.u8": (residuals, "u8"),
        "selected-chords.u32": (chords[selected], "u32le"), "fit.u8": (fit, "u8"),
        "witness.json": (witness, "json"), "tree.json": (metadata, "json")}
    progress("complete-tree-test", chords=CHORDS, terminal=terminal)
    return {"arrays": arrays, "terminal": terminal, "witness": witness, "metadata": metadata}


def read_refinement_metadata(refinement: Any, m: Any, root: Path) -> tuple[Any, Any]:
    require(REFINEMENT_ARTIFACT and REFINEMENT_FILES and REFINEMENT_SNAPSHOT,
            "actual_refinement_acceptance_pins_pending")
    objects = {name: json_bytes(read_fixed(root, name, pin)) for name, pin in REFINEMENT_FILES.items()}
    head = objects["output/HEAD"]
    require(type(head.get("completed_steps")) is int and 0 <= head["completed_steps"] <= refinement.CAP,
            "accepted_refinement_step_count")
    bundles = []
    for step in range(1, head["completed_steps"] + 1):
        directory = root / "output" / "steps" / str(step).zfill(6)
        require(directory.is_dir() and not directory.is_symlink(), "accepted_refinement_step_directory")
        manifest = read_json(directory, "manifest.json")
        require(refinement.sealed_ok(manifest, "step-manifest"), "accepted_refinement_manifest_seal")
        files = manifest["files"]
        require(files == sorted(files, key=lambda item: item["file"]) and
                len(files) == len({item["file"] for item in files}) and
                {p.name for p in directory.iterdir()} == {item["file"] for item in files} | {"manifest.json"},
                "accepted_refinement_manifest_file_roster")
        payloads = {}
        needed = {"result.json", "instruction.json", "physical-normalized.bin", "target-remainder.bin", "lambda.bin"}
        for item in files:
            path = safe_file(directory, item["file"])
            require(set(item) == {"file", "bytes", "sha256"} and
                    file_pin(path) == {key: item[key] for key in ("bytes", "sha256")},
                    "accepted_refinement_payload_pin")
            if item["file"] in needed:
                payloads[item["file"]] = path.read_bytes()
        # Large materialization/old scan bodies are authenticated and dropped.
        # Only the small typed row/target metadata survives this iteration.
        bundles.append({"manifest": manifest, "payloads": payloads,
                        "result": json_bytes(payloads["result.json"]),
                        "instruction": json_bytes(payloads["instruction.json"])})
        check_deadline("accepted-refinement-bundle")
    return objects, bundles


def refinement_parent_layout(refinement: Any, p2: Any, objects: Any, bundles: Any) -> Any:
    """Exact accepted JSON/chain join, shared with the metadata-only canary."""
    for name, pin in REFINEMENT_FILES.items():
        require(len(canonical(objects[name])) == pin[0] and sha(canonical(objects[name])) == pin[1],
                "accepted_refinement_entry_pin:" + name)
    head, result, checked, start, owner, source, index = (objects[name] for name in
        ("output/HEAD", "output/result.json", "checker-result.json", "output/start.json",
         "output/owner.json", "output/source.json", "output/canonical-index.json"))
    for value, kind in ((head, "head"), (result, "result"), (start, "start"), (owner, "owner"),
                        (source, "source"), (index, "canonical-p1-index")):
        require(refinement.sealed_ok(value, kind), "accepted_refinement_sealed:" + kind)
    require(head["kind"] == "Separator" and result["status"] == checked["status"] == "PASS" and
            checked["schema"] == refinement.SCHEMA + ".checker-result" and
            all(value.get("cross_checked") is False and value.get("verified") is False for value in (result, checked)),
            "accepted_refinement_separator_checker")
    for key in ("completed_steps", "rank", "generation", "state_head", "owner_sha256"):
        require(head[key] == result[key] == checked[key], "accepted_refinement_final_join:" + key)
    require(checked["prefix_steps_replayed"] == head["completed_steps"] and
            checked["canonical_index_sha256"] == head["canonical_index_sha256"] and
            result["terminal"] == checked["terminal"] == REFINEMENT_SNAPSHOT["terminal"] and
            result["head_sha256"] == checked["head_sha256"] == sha(canonical(head)) and
            checked["result_sha256"] == sha(canonical(result)) and
            head["owner_sha256"] == sha(canonical(owner)) and head["start_sha256"] == sha(canonical(start)) and
            head["source_sha256"] == sha(canonical(source)) and head["canonical_index_sha256"] == sha(canonical(index)) and
            head["producer_sha256"] == source["producer_sha256"] == REFINEMENT_MODULE_SHA,
            "accepted_refinement_owner_source_head")
    require(source["modules"] == {refinement.FIXED_MODULE: refinement.FIXED_MODULE_SHA, **p2.MODULE_PINS} and
            source["data"] == p2.DATA_PINS and result["scope"] == owner["scope"] == refinement.SCOPE and
            result["claims"] == refinement.CLAIMS and
            result["scan_manifest_sha256"] == head["current_scan_manifest_sha256"] and
            owner["accepted_packet_manifest_sha256"] == head["packet_manifest_sha256"] ==
                refinement.PACKET_FILES["output/packet/manifest.json"][1], "accepted_refinement_scope_source")
    require((start["rank"], start["generation"], start["state_head"], start["lambda_sha256"],
             start["target_remainder_sha256"]) == (refinement.START_RANK, refinement.START_GENERATION,
                refinement.START_HEAD, refinement.START_LAMBDA, refinement.START_TARGET), "accepted_refinement_base_start")
    require(len(bundles) == head["completed_steps"], "accepted_refinement_complete_prefix")
    previous_head, previous_target = refinement.START_HEAD, refinement.START_TARGET
    previous_manifest = None
    layouts = []
    for step, bundle in enumerate(bundles, 1):
        manifest, row, instruction, payloads = (bundle[k] for k in ("manifest", "result", "instruction", "payloads"))
        expected_files = {"physical-raw.bin", "physical-remainder.bin", "physical-normalized.bin",
            "target-remainder.bin", "source-d.bin", "source-full-top.bin", "materialization.json",
            "instruction.json", "result.json", "lambda.bin"}
        require({item["file"] for item in manifest["files"]} == expected_files and
                set(payloads) == {"result.json", "instruction.json", "physical-normalized.bin", "target-remainder.bin", "lambda.bin"} and
                refinement.sealed_ok(manifest, "step-manifest") and
                refinement.sealed_ok(row, "step-result") and
                canonical(row) == payloads["result.json"] and canonical(instruction) == payloads["instruction.json"],
                "accepted_refinement_step_payloads")
        unsigned = {k: v for k, v in instruction.items() if k != "rolling_sha256"}
        require(instruction["schema"] == refinement.SCHEMA + ".instruction" and "sha256" not in instruction and
                instruction["predecessor"] == previous_head and instruction["rolling_sha256"] ==
                sha(bytes.fromhex(previous_head) + canonical(unsigned)), "accepted_refinement_rolling_instruction")
        target = row["target"]
        require(set(target) == {"parent_remainder_sha256", "remainder_sha256", "scalar"} and
                type(target["scalar"]) is int and target["scalar"] in (0, 1, 2) and
                target["parent_remainder_sha256"] == previous_target and
                target["scalar"] == instruction["target_scalar"] and
                target["remainder_sha256"] == instruction["target_remainder_sha256"] == sha(payloads["target-remainder.bin"]),
                "accepted_refinement_plain_target")
        require(manifest["step"] == row["step"] == instruction["step"] == step and
                manifest["predecessor_step_manifest_sha256"] == previous_manifest and
                manifest["parent_state_head"] == row["parent_state_head"] == previous_head and
                manifest["state_head"] == row["state_head"] == instruction["rolling_sha256"] and
                manifest["owner_sha256"] == row["owner_sha256"] == head["owner_sha256"] and
                manifest["packet_manifest_sha256"] == row["packet_manifest_sha256"] == instruction["packet_manifest_sha256"] ==
                    head["packet_manifest_sha256"] and
                manifest["rank"] == row["rank_after"] == instruction["rank"] == refinement.START_RANK + step and
                manifest["generation"] == row["generation_after"] == instruction["generation"] == refinement.START_GENERATION + step and
                row["rank_before"] == manifest["rank"] - 1 and row["generation_before"] == instruction["offer"] ==
                    manifest["generation"] - 1 and manifest["kind"] == row["kind"] == "Separator" and
                instruction["physical_offset"] == (manifest["rank"] - 1) * 12096 and
                row["pivot"]["normalized_sha256"] == instruction["physical_sha256"] == sha(payloads["physical-normalized.bin"]) and
                row["pivot"]["lead"] == instruction["lead"] and row["pivot"]["scale"] == instruction["sigma"] and
                row["pivot"]["reductions"] == instruction["physical_reductions"] and
                row["separator"]["lambda_sha256"] == sha(payloads["lambda.bin"]), "accepted_refinement_step_chain")
        layouts.append({"step": step, "manifest_sha256": sha(canonical(manifest)),
            "result_sha256": sha(canonical(row)), "instruction_sha256": sha(canonical(instruction)),
            "target_sha256": sha(canonical(target)), "state_head": manifest["state_head"],
            "parent_state_head": previous_head, "rank": manifest["rank"], "generation": manifest["generation"],
            "lead": instruction["lead"], "target_scalar": target["scalar"],
            "physical_normalized_sha256": sha(payloads["physical-normalized.bin"]),
            "lambda_sha256": sha(payloads["lambda.bin"]), "target_remainder_sha256": target["remainder_sha256"]})
        previous_head, previous_manifest, previous_target = (manifest["state_head"],
            sha(canonical(manifest)), target["remainder_sha256"])
    lambda_sha = layouts[-1]["lambda_sha256"] if layouts else refinement.START_LAMBDA
    require(previous_head == head["state_head"] and previous_manifest == head["step_manifest_sha256"] and
            {"completed_steps": head["completed_steps"], "terminal": result["terminal"], "rank": head["rank"],
             "generation": head["generation"], "state_head": previous_head, "lambda_sha256": lambda_sha,
             "target_remainder_sha256": previous_target} == REFINEMENT_SNAPSHOT, "accepted_refinement_snapshot_pin")
    return seal("refinement-parent-layout", {"artifact": REFINEMENT_ARTIFACT,
        "entry_files": [{"file": name, "bytes": pin[0], "sha256": pin[1]} for name, pin in sorted(REFINEMENT_FILES.items())],
        **REFINEMENT_SNAPSHOT, "steps": layouts, "old_arithmetic_replayed": False})


def accepted_snapshot(refinement: Any, p2: Any, m: Any, base: Any, descriptors: Any, args: Any) -> Any:
    objects, bundles = read_refinement_metadata(refinement, m, args.refinement_root)
    layout = refinement_parent_layout(refinement, p2, objects, bundles)
    state, old_start, old_owner, p1, task554, tables, packet = refinement.load_start(p2, m, base, descriptors, args)
    require(old_start == objects["output/start.json"] and old_owner == objects["output/owner.json"],
            "accepted_refinement_all_retained_parents_join")
    refinement.validate_index(objects["output/canonical-index.json"], p1, packet)
    # Old instructions are authenticated bytes; old scans and insert arithmetic
    # are accepted premises. They are not executed by this intake.
    for step, bundle in enumerate(bundles, 1):
        manifest, instruction, payloads = (bundle[k] for k in ("manifest", "instruction", "payloads"))
        normalized, target = payloads["physical-normalized.bin"], payloads["target-remainder.bin"]
        row, reduced = unpack(normalized, PHYSICAL), unpack(target, PHYSICAL)
        lead = instruction["lead"]
        require(type(lead) is int and 0 <= lead < PHYSICAL and lead not in state["leads"] and
                row[lead] == 1 and not np.any(row[:lead]) and
                all(row[x] == reduced[x] == 0 for x in state["leads"]) and reduced[lead] == 0 and
                np.any(reduced), "accepted_refinement_normalized_row_type")
        require(bundle["result"]["separator"]["lambda_rho2"] == refinement.derived_rho2(m, state, step),
                "accepted_refinement_derived_target_chain")
        refinement.advance_state(m, state, manifest, instruction, normalized, target, payloads["lambda.bin"])
        check_deadline("accepted_refinement_row_attachment")
    state["current_scan_manifest_sha256"] = objects["output/HEAD"]["current_scan_manifest_sha256"]
    require(refinement.head_record(state, sha(canonical(old_owner)), packet, old_start, objects["output/source.json"],
                sha(canonical(objects["output/canonical-index.json"]))) == objects["output/HEAD"],
            "accepted_refinement_attached_head")
    direct = m.check_final_separator(state["lambda"], state["rows"], state["previous_target_raw"], state["target_raw"])
    parents = copy.deepcopy(state["accepted_target_derivation_parents"])
    for item in layout["steps"]:
        parents.append({"role": "refinement-step-" + str(item["step"]), **{key: item[key] for key in
                        ("manifest_sha256", "result_sha256", "target_sha256", "state_head")}})
    derived = {"mode": "derived", "value": 1, "original_rho2_directly_read": False,
        "original_rho2_packed_sha256": m.RHO2_SHA256, "accepted_target_derivation_parents": parents,
        "identity_convention": {
            "base": "rho2 - base_remainder = sum(target.reductions.scalar * base_normalized_row)",
            "saved_deltas": "parent_remainder - child_remainder = sum(target.new_reductions.scalar * saved_normalized_row)",
            "packet_and_refinement_steps": "parent_remainder - child_remainder = target.scalar * accepted_normalized_row"},
        "new_target_steps_executed": 0}
    start = seal("start", {"kind": "Separator", "rank": state["rank"], "generation": state["generation"],
        "state_head": state["head"], "lambda_sha256": sha(state["lambda_raw"]),
        "target_remainder_sha256": sha(state["target_raw"]), "accepted_refinement_layout": layout,
        "accepted_target_derivation_parents": parents, "lambda_rho2": derived, "direct_pairing": direct})
    owner = seal("owner", {"formula_id": FORMULA, "scope": SCOPE,
        "accepted_refinement_owner_sha256": sha(canonical(old_owner)),
        "accepted_refinement_head_sha256": sha(canonical(objects["output/HEAD"])),
        **{key: old_owner[key] for key in ("p1_parent", "task554_parent", "task712_parent",
             "task712_manifest_sha256", "word_dictionary_sha256", "relator_dictionary_sha256")}})
    progress("accepted-current-snapshot", rank=state["rank"], generation=state["generation"], rows_checked=direct["rows"])
    return state, start, owner, p1, task554, tables


def raw_edge_source_fixture(arith: Any, context: Any, tail_word: tuple[int, ...], slot: int,
                            *, wrong_left: bool = False) -> Any:
    """One unclosed edge's linear source map, for the changed ABI canary.

    This is a small forward scatter, not a cycle/P1/physical materializer.
    In particular it assigns no normalized eta from an edge exponent.
    """
    parts = (np.zeros((4, 6048), dtype=np.uint8), np.zeros((4, 18144), dtype=np.uint8),
             np.zeros((4, TOP), dtype=np.uint8), np.zeros(8, dtype=np.uint8))
    for tag, words in enumerate(arith.SEED_OO):
        phi_tail = arith._seed_affine_eval(arith._seed_substitute(tail_word, *words), context.images)
        gradient, endpoint = arith._seed_affine_fox(tuple(words[slot]), context.images)
        require(endpoint != arith.SEED_AFFINE_IDENTITY, "raw_edge_nonclosed_generator")
        normal = []
        for (component, prefix), coefficient in gradient.items():
            s = arith._seed_affine_mul(prefix, phi_tail) if wrong_left else arith._seed_affine_mul(phi_tail, prefix)
            if component == 0:
                first = arith._seed_affine_mul(s, context.images[0])
                second = arith._seed_affine_mul(first, context.pb3_b)
                parts[3][tag] = (int(parts[3][tag]) + coefficient) % 3
                normal.extend(((0, first, -coefficient), (1, second, -coefficient)))
            else:
                normal.append((1, s, coefficient))
        for component, vertex, coefficient in normal:
            p = context.psidx[vertex[0]]
            polynomial = arith._seed_e_poly(vertex[3])
            for character, label in enumerate(CHARACTERS):
                weight = coefficient * arith._seed_cv(context.transport[tag][label], (vertex[1], vertex[2]))
                c0 = (tag * 2 + component) * 504 + p
                parts[0][character, c0] = (int(parts[0][character, c0]) + weight) % 3
                for mono in range(3):
                    c1 = ((tag * 2 + component) * 3 + mono) * 504 + p
                    parts[1][character, c1] = (int(parts[1][character, c1]) + weight * int(polynomial[1 + mono])) % 3
                for mono in range(6):
                    c2 = ((tag * 2 + component) * 6 + mono) * 504 + p
                    parts[2][character, c2] = (int(parts[2][character, c2]) + weight * int(polynomial[4 + mono])) % 3
    return parts


def expect_reject(action: Any, name: str) -> None:
    try:
        action()
    except ResourceStop:
        raise
    except Exception:
        return
    raise RuntimeError("mutation_was_accepted:" + name)


def parent_layout_selftest(args: Any) -> Any:
    refinement, p2, m, _base, _descriptors = own_dependencies()
    accepted = refinement.parent_layout_selftest(args)
    objects, bundles = read_refinement_metadata(refinement, m, args.refinement_root)
    layout = refinement_parent_layout(refinement, p2, objects, bundles)
    require(len(bundles) > 0, "actual_parent_canary_requires_observed_nonempty_refinement")
    rejected = list(accepted["rejected_cases"])
    for name in ("refinement-instruction-generic-seal", "refinement-target-generic-seal",
                 "refinement-target-parent", "refinement-step-chain", "refinement-final-head"):
        changed_objects, changed_bundles = copy.deepcopy(objects), copy.deepcopy(bundles)
        if name == "refinement-instruction-generic-seal":
            changed_bundles[0]["instruction"]["sha256"] = "0" * 64
        elif name == "refinement-target-generic-seal":
            changed_bundles[0]["result"]["target"]["sha256"] = "0" * 64
        elif name == "refinement-target-parent":
            changed_bundles[-1]["result"]["target"]["parent_remainder_sha256"] = "0" * 64
        elif name == "refinement-step-chain":
            changed_bundles[-1]["manifest"]["predecessor_step_manifest_sha256"] = "0" * 64
        else:
            changed_objects["output/HEAD"]["state_head"] = "0" * 64
        expect_reject(lambda: refinement_parent_layout(refinement, p2, changed_objects, changed_bundles), name)
        rejected.append(name)
    require(len(rejected) == 15, "actual_parent_fifteen_mutations")
    return {"schema": SCHEMA + ".parent-layout-selftest", "status": "PASS", "metadata_only": True,
        "parent_layout": accepted["parent_layout"], "accepted_packet_layout": accepted["accepted_packet_layout"],
        "accepted_refinement_layout": layout, "rejected_cases": rejected, "cross_checked": False, "verified": False}


def selftest() -> Any:
    # This fixture reproduces the nonmonotone lead issue: the second inserted
    # row retains the first row's pivot coordinate. Reversing IDs is wrong.
    rows = np.asarray(((0, 0, 1, 0), (1, 0, 2, 0)), dtype=np.uint8)
    values = np.asarray((2, 1), dtype=np.uint8)
    dual, order = interpolate_rows(4, [2, 0], values, lambda i: rows[i])
    require(order == [0, 1] and all(dot(dual, row) == int(value) for row, value in zip(rows, values)),
            "nonmonotone_original_lead_canary")
    wrong = np.zeros(4, dtype=np.uint8)
    for index in (1, 0):
        lead = (2, 0)[index]
        wrong[lead] = (int(values[index]) - dot(wrong, rows[index])) % 3
    require(any(dot(wrong, row) != int(value) for row, value in zip(rows, values)), "wrong_reverse_insertion_detected")
    bad_rows = rows.copy()
    bad_rows[0, 1] = 1
    expect_reject(lambda: interpolate_rows(4, [2, 0], values, lambda i: bad_rows[i]), "original-lead-prefix")
    _refinement, _p2, _m, base, _descriptors = own_dependencies()
    context, _words = base.source_context()
    arith = base.ARITH
    geometry = geometry_inputs(arith, context)
    tail_word, slot = (1, 2), 0
    tail = arith._seed_affine_eval(tail_word, context.images)
    left_product = arith._seed_affine_mul(tail, context.images[0])
    wrong_product = arith._seed_affine_mul(context.images[0], tail)
    require(left_product != wrong_product and geometry["next"][qid(context, tail), slot] == qid(context, left_product),
            "noncommuting_right_edge_canary")
    raw = raw_edge_source_fixture(arith, context, tail_word, slot)
    wrong_raw = raw_edge_source_fixture(arith, context, tail_word, slot, wrong_left=True)
    require(any(not np.array_equal(a, b) for a, b in zip(raw, wrong_raw)), "wrong_fox_prefix_left_order_detected")
    expect_reject(lambda: arith._seed_qnorm((1,), context), "closed_only_helper_nonclosed_edge")
    lower = np.concatenate((raw[0].reshape(-1), raw[1].reshape(-1), raw[3]))
    edge = 2 * qid(context, tail) + slot
    probe_receipts = []
    for degree in (0, 1, 2):
        q, kappa = np.zeros((4, TOP), dtype=np.uint8), np.zeros(LOWER, dtype=np.uint8)
        positions = np.flatnonzero(raw[degree].reshape(-1))
        require(len(positions) > 0, "nonclosed_edge_has_each_degree")
        position = int(positions[0])
        if degree == 2:
            q.reshape(-1)[position] = 1
            kappa[96774:] = (1, 2)
        else:
            kappa[(0 if degree == 0 else 24192) + position] = 1
        replay = source_cochain(arith, context, geometry, {"q": q, "kappa": kappa})
        expected = (dot(q, raw[2]) - dot(kappa, lower)) % 3
        require(int(replay["f"][edge]) == expected and expected in (1, 2), "actual_nonclosed_edge_adjoint_canary")
        if degree == 2:
            require(list(replay["b_aux"]) == [2, 1], "shared_eta_not_divided_by18")
        probe_receipts.append({"degree": degree, "edge": edge, "scalar": expected,
                               "source_sha256": sha(pack(raw[degree]))})
    # Test the actual all-roster classifier at a final chord after the basis.
    tau = np.vstack((np.eye(5, dtype=np.uint8), np.asarray((1, 2, 1, 0, 2), dtype=np.uint8)))
    chords = np.arange(6, dtype=np.uint32) * 2
    fit = np.asarray((1, 2, 0, 1, 2), dtype=np.uint8)
    values = (tau.astype(np.int32) @ fit.astype(np.int32) % 3).astype(np.uint8)
    selected = first_independent(tau)
    fit2 = solve_five(tau[selected], values[selected])
    zeros = np.zeros(6, dtype=np.uint8)
    terminal, witness, _meta = classify_complete(chords, tau, values, zeros, selected, fit2,
                                                np.zeros(2, dtype=np.uint8), 6, True)
    require(terminal == "COMPLETE_ZERO_CANDIDATE" and witness["kind"] == "none", "complete_zero_classifier")
    changed = values.copy()
    changed[-1] = (int(changed[-1]) + 1) % 3
    residual = zeros.copy()
    residual[-1] = 1
    terminal, witness, _meta = classify_complete(chords, tau, changed, residual, selected, fit2,
                                                np.zeros(2, dtype=np.uint8), 6, True)
    require(terminal == "VIOLATION_CANDIDATE" and witness["failed_chord"] == int(chords[-1]) and
            witness["scalar"] == 1 and len(witness["cycles"]) == 6, "final_chord_six_cycle_witness")
    expect_reject(lambda: classify_complete(chords, tau, changed, zeros, selected, fit2,
                                           np.zeros(2, dtype=np.uint8), 6, True), "false-zero-residual-tail")
    expect_reject(lambda: classify_complete(chords[:-1], tau[:-1], values[:-1], zeros[:-1], selected, fit2,
                                           np.zeros(2, dtype=np.uint8), 6, True), "truncated-chord-eof")
    expect_reject(lambda: classify_complete(chords, tau, values, zeros, selected, fit2,
                                           np.zeros(2, dtype=np.uint8), 6, False), "false-eof")
    _terminal, aux_witness, _meta = classify_complete(chords, tau, changed, residual, selected, fit2,
                                                    np.asarray((2, 1), dtype=np.uint8), 6, True)
    require(aux_witness["kind"] == "auxiliary" and aux_witness["coordinate"] == 0 and
            aux_witness["scalar"] == 2, "auxiliary_before_failed_chord")
    roundtrip = json_bytes(canonical(witness))
    require(sealed_ok(roundtrip, "witness"), "witness_canonical_seal")
    roundtrip["scalar"] = 0
    require(not sealed_ok(roundtrip, "witness"), "witness_scalar_corruption")
    return {"schema": SCHEMA + ".selftest", "status": "PASS", "tests": [
        "nonmonotone-original-lead-not-insertion", "actual-right-edge-left-Fox-nonclosed-d0-d1-d2-eta",
        "all-chord-tail-eof-six-cycle-and-aux-priority"], "nonclosed_edge_probes": probe_receipts,
        "cross_checked": False, "verified": False}


def run_actual(args: Any) -> Any:
    output = args.output_root.resolve()
    parents = [args.state_root, args.delta_root, args.seed34_root, args.packet_root, args.refinement_root,
               args.prepare_root, *args.block_root, args.p1_root, args.task712_root]
    require(not args.output_root.is_symlink() and not output.exists(), "fresh_output_directory")
    for path in parents:
        root = path.resolve()
        require(path.is_dir() and not path.is_symlink() and root != output and
                root not in output.parents and output not in root.parents, "disjoint_output_and_parents")
    refinement, p2, m, base, descriptors = own_dependencies()
    state, start, owner, p1, task554, tables = accepted_snapshot(refinement, p2, m, base, descriptors, args)
    modules = {REFINEMENT_MODULE: REFINEMENT_MODULE_SHA,
               refinement.FIXED_MODULE: refinement.FIXED_MODULE_SHA, **p2.MODULE_PINS}
    source = seal("source", {"producer_sha256": sha(Path(__file__).read_bytes()), "modules": modules,
        "data": p2.DATA_PINS, "python": sys.version, "numpy": np.__version__})
    owner_sha, snapshot_sha, source_sha = (sha(canonical(x)) for x in (owner, start, source))
    check_deadline("before-output-initialization")
    output.mkdir(parents=True)
    for name, value in (("owner.json", owner), ("start.json", start), ("source.json", source)):
        write_atomic(output, name, canonical(value))
    context, _words = base.source_context()
    manifests = {}

    def publish(stage: str, value: Any, inputs: dict[str, str]) -> None:
        payloads = {name: array_payload(array, dtype) for name, (array, dtype) in value["arrays"].items()}
        manifest = write_stage(output, stage, owner_sha, snapshot_sha, inputs, payloads)
        manifests[stage] = sha(canonical(manifest))

    geometry = geometry_inputs(base.ARITH, context)
    publish("geometry", geometry, {})
    section = current_section(base, tables, state, p1, task554)
    publish("section", section, {})
    cochain = source_cochain(base.ARITH, context, geometry, section)
    publish("cochain", cochain, {key: manifests[key] for key in ("geometry", "section")})
    tree = complete_tree_test(geometry, cochain)
    publish("tree", tree, {key: manifests[key] for key in ("geometry", "cochain")})
    result = seal("result", {"status": "PASS", "terminal": tree["terminal"],
        "materialization": tree["witness"]["materialization"], "owner_sha256": owner_sha,
        "snapshot_sha256": snapshot_sha, "source_sha256": source_sha, "state_head": state["head"],
        "rank": state["rank"], "generation": state["generation"], "lambda_sha256": sha(state["lambda_raw"]),
        "target_remainder_sha256": sha(state["target_raw"]), "stage_manifests": manifests,
        "witness_sha256": sha(canonical(tree["witness"])), "lambda_rho2": start["lambda_rho2"],
        "direct_pairing": start["direct_pairing"], "complete_source_and_conn_premises_retained": True,
        "all8059_section_equalities": True, "all54433_chords_checked": True, "normalized_auxiliary_tests": 2,
        "physical_appends": 0, "grade2_member": "NOT_DECIDED",
        "grade2_nonmember": "CANDIDATE_ONLY" if tree["terminal"] == "COMPLETE_ZERO_CANDIDATE" else "NOT_DECIDED",
        "full_A0": False, **ASSURANCE})
    check_deadline("before-complete-result-publication")
    write_atomic(output, "result.json", canonical(result))
    files = [{"file": name, "bytes": len(canonical(value)), "sha256": sha(canonical(value))}
             for name, value in sorted((("owner.json", owner), ("start.json", start),
                                        ("source.json", source), ("result.json", result)))]
    manifest = seal("manifest", {"owner_sha256": owner_sha, "snapshot_sha256": snapshot_sha,
        "source_sha256": source_sha, "result_sha256": sha(canonical(result)), "stage_manifests": manifests,
        "files": files, "file_roster": ["cochain", "geometry", "manifest.json", "owner.json", "result.json",
            "section", "source.json", "start.json", "tree"], **ASSURANCE})
    write_atomic(output, "manifest.json", canonical(manifest))
    return result


def request_stop(_signal: int, _frame: Any) -> None:
    global STOP_REQUESTED
    STOP_REQUESTED = True


def main() -> int:
    global DEADLINE
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--parent-layout-selftest", action="store_true")
    parser.add_argument("--max-seconds", type=float, default=1800.0)
    names = ("state-root", "delta-root", "seed34-root", "packet-root", "refinement-root",
             "prepare-root", "p1-root", "task712-root")
    for name in names:
        parser.add_argument("--" + name, type=Path)
    parser.add_argument("--block-root", type=Path, action="append", default=[])
    parser.add_argument("--output", dest="output_root", type=Path)
    args = parser.parse_args()
    try:
        require(0 < args.max_seconds < float("inf"), "finite_positive_resource_bound")
        DEADLINE = STARTED + args.max_seconds
        for signum in (signal.SIGINT, signal.SIGTERM):
            signal.signal(signum, request_stop)
        if args.selftest:
            require(not args.parent_layout_selftest and not args.block_root and args.output_root is None and
                    all(getattr(args, name.replace("-", "_")) is None for name in names), "selftest_no_parent_paths")
            result = selftest()
        elif args.parent_layout_selftest:
            require(not args.block_root and args.output_root is None and
                    all(getattr(args, name.replace("-", "_")) is not None for name in names[:5]) and
                    all(getattr(args, name.replace("-", "_")) is None for name in names[5:]), "metadata_only_five_roots")
            result = parent_layout_selftest(args)
        else:
            require(len(args.block_root) == 4 and args.output_root is not None and
                    all(getattr(args, name.replace("-", "_")) is not None for name in names), "actual_twelve_parent_roots")
            result = run_actual(args)
        print(canonical(result).decode("ascii"), end="", flush=True)
        return 0
    except ResourceStop as exc:
        output = args.output_root.resolve() if args.output_root is not None else None
        stages = [stage for stage in ("geometry", "section", "cochain", "tree") if output is not None and
                  (output / stage / "manifest.json").is_file() and not (output / stage).is_symlink()]
        diagnostic = seal("resource-stop", {"status": "UNKNOWN_RESOURCE", "terminal": "UNKNOWN_RESOURCE",
            "phase": str(exc), "completed_stages": stages, "candidate": False, "cross_checked": False, "verified": False})
        if output is not None and output.is_dir() and not output.is_symlink():
            write_atomic(output, "resource-stop.json", canonical(diagnostic), replace=True)
        print(canonical(diagnostic).decode("ascii"), end="", flush=True)
        return 3
    except Exception as exc:
        print(canonical({"status": "REJECTED", "reason": str(exc), "error_type": type(exc).__name__,
                         "cross_checked": False, "verified": False}).decode("ascii"), end="", flush=True)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
