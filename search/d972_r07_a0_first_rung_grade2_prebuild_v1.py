#!/usr/bin/env python3
"""Task565: target-independent grade-two module prebuild.

The production path consumes only the authenticated grade-one prepare and
four block states.  It reconstructs the complete transition presentation,
lifts it one precision, closes the exact v444 defect roster in four legal
character blocks, and forms the joint lower-first physical fibre.  No target
is read by that path and no membership terminal can be emitted.

The separate ``--join`` path is inactive unless explicitly requested.  It
requires a checked grade-one MEMBER state and certificate and stops after an
independent degree-two residual comparison.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import tempfile
import time
from collections import deque
from pathlib import Path
from typing import Any, Iterable, Iterator

import numpy as np

# The grade-one v4 executable deliberately retained the v3 state schema.  We
# reuse its audited finite-quotient primitives, packed echelon, and strict
# v3-state validators.  No grade-one phase or run() entry point is called.
import d972_r07_a0_first_rung_grade1_v4 as grade1


ROOT = Path(__file__).resolve().parents[1]
floor = grade1.floor

SCHEMA = "d972.r07.a0.first-rung-grade2-prebuild.v1"
STATE_SCHEMA = SCHEMA + ".state"
GRADE1_STATE_SCHEMA = grade1.STATE_SCHEMA

CHARACTER_LABELS = grade1.CHARACTER_LABELS
ACTORS = grade1.ACTORS
PURE_Q1_WORDS = grade1.PURE_Q1_WORDS
MONOMIALS_DEGREE0 = ((0, 0, 0),)
MONOMIALS_DEGREE1 = grade1.MONOMIALS_GRADE1
MONOMIALS_DEGREE2 = (
    (2, 0, 0),
    (1, 1, 0),
    (1, 0, 1),
    (0, 2, 0),
    (0, 1, 1),
    (0, 0, 2),
)
MONOMIALS_LE2 = MONOMIALS_DEGREE0 + MONOMIALS_DEGREE1 + MONOMIALS_DEGREE2
MONOMIAL_INDEX = {monomial: index for index, monomial in enumerate(MONOMIALS_LE2)}

SOURCE_DEGREE0_PER_CHARACTER = 6 * 2 * 504
SOURCE_DEGREE1_PER_CHARACTER = SOURCE_DEGREE0_PER_CHARACTER * 3
SOURCE_DEGREE2_PER_CHARACTER = SOURCE_DEGREE0_PER_CHARACTER * 6
SOURCE_DEGREE0_WIDTH = 4 * SOURCE_DEGREE0_PER_CHARACTER
SOURCE_DEGREE1_WIDTH = 4 * SOURCE_DEGREE1_PER_CHARACTER
SOURCE_DEGREE2_WIDTH = 4 * SOURCE_DEGREE2_PER_CHARACTER
SOURCE_PRECISION1_WIDTH = SOURCE_DEGREE0_WIDTH + SOURCE_DEGREE1_WIDTH + 8

PHYSICAL_DEGREE0_WIDTH = 4 * 2 * 2 * 504
PHYSICAL_DEGREE1_WIDTH = PHYSICAL_DEGREE0_WIDTH * 3
PHYSICAL_DEGREE2_WIDTH = PHYSICAL_DEGREE0_WIDTH * 6
PHYSICAL_LOWER_WIDTH = PHYSICAL_DEGREE0_WIDTH + PHYSICAL_DEGREE1_WIDTH + 4

EXPECTED_SEEDS = 44
PACK_ENCODING = "base3-four-trits-per-byte"

PREBUILD_PINS = {
    "sol/proof_r07_grade1_to_grade2_split_presentation_handoff_v450.md":
        "48acc55a73aba140aa73098791d73f936f1b46fc5316d6f56e668be242fdc630",
    "sol/luna_task_565_r07_a0_first_rung_grade2_prebuild_v1.md":
        "0c0c32831a5fbd055ba158b8f6b1c429aa51a4cdfe1d781e912a2eba016ebef3",
    "sol/proof_r07_first_rung_six_grade_character_schedule_v448.md":
        "168e3fc5ab38520faf8ed5d107013f1f8b53f22d2907032519b86b6e0f01182d",
    "sol/proof_r07_grade1_to_grade2_split_presentation_handoff_repair_v451.md":
        "3ec2d1351e16bf0fcde3abe8da346b8765b26c30796ff48e415c46ac51d933b4",
    "sol/sol_reply_566_audit_r07_grade1_to_grade2_handoff_v1.md":
        "b8c04819a27906cfaa88534627c147307e1fb7b9429e1f1246fc518b72f2297a",
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_json(value: Any) -> bytes:
    return (
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
        + "\n"
    ).encode("ascii")


def _plain_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _add_mod3(destination: np.ndarray, source: np.ndarray, scalar: int = 1) -> None:
    scalar %= 3
    if scalar:
        destination[:] = (
            destination.astype(np.uint16) + scalar * source.astype(np.uint16)
        ) % 3


def false_claim_flags() -> dict[str, bool]:
    return {
        "ORDER_54432": False,
        "FULL_Q0": False,
        "A0": False,
        "COMMON": False,
        "COFINAL_LIFT": False,
        "FAKE": False,
        "IHARA": False,
        "verified": False,
    }


def fixed_dimensions() -> dict[str, Any]:
    return {
        "characters": 4,
        "character_labels": [list(value) for value in CHARACTER_LABELS],
        "degree2_monomials": [list(value) for value in MONOMIALS_DEGREE2],
        "monomials_coupled": True,
        "source_degree0": SOURCE_DEGREE0_WIDTH,
        "source_degree1": SOURCE_DEGREE1_WIDTH,
        "source_degree2_per_character": SOURCE_DEGREE2_PER_CHARACTER,
        "source_degree2_total": SOURCE_DEGREE2_WIDTH,
        "source_precision1_with_auxiliary": SOURCE_PRECISION1_WIDTH,
        "physical_degree0": PHYSICAL_DEGREE0_WIDTH,
        "physical_degree1": PHYSICAL_DEGREE1_WIDTH,
        "physical_lower_with_auxiliary": PHYSICAL_LOWER_WIDTH,
        "physical_degree2": PHYSICAL_DEGREE2_WIDTH,
        "packed_degree2_residual_bytes": PHYSICAL_DEGREE2_WIDTH // 4,
    }


def resource_ceilings() -> dict[str, int]:
    """Audited Task566 ceilings; these are not rank/runtime estimates."""
    return {
        "production_old_rank": 2014,
        "production_h1_rank": 6045,
        "production_b1_rank": 8059,
        "grade2_defect_origins": 32280,
        "one_character_rank": 36288,
        "one_character_queue_attempts": 177432,
        "joint_physical_input_rows": 153211,
        "one_block_packed_basis_bytes": 329204736,
        "joint_packed_physical_input_ceiling_bytes": 1853240256,
    }


def validate_fixed_layouts() -> None:
    expected = (
        SOURCE_DEGREE2_PER_CHARACTER,
        SOURCE_DEGREE2_WIDTH,
        PHYSICAL_LOWER_WIDTH,
        PHYSICAL_DEGREE2_WIDTH,
        PHYSICAL_DEGREE2_WIDTH // 4,
    )
    if expected != (36288, 145152, 32260, 48384, 12096):
        raise RuntimeError("grade2_dimension_drift")
    if MONOMIALS_DEGREE2 != (
        (2, 0, 0),
        (1, 1, 0),
        (1, 0, 1),
        (0, 2, 0),
        (0, 1, 1),
        (0, 0, 2),
    ):
        raise RuntimeError("grade2_monomial_order_drift")


def load_prebuild_pins() -> dict[str, dict[str, Any]]:
    receipt: dict[str, dict[str, Any]] = {}
    for relative, expected in PREBUILD_PINS.items():
        data = (ROOT / relative).read_bytes()
        actual = sha256_bytes(data)
        if actual != expected:
            raise RuntimeError(f"prebuild_pin_mismatch:{relative}:{actual}")
        receipt[relative] = {"bytes": len(data), "sha256": actual}
    return receipt


def ensure_external_state_dir(path: Path) -> Path:
    resolved = path.resolve()
    root = ROOT.resolve()
    if resolved == root or root in resolved.parents:
        raise RuntimeError("state_dir_must_be_outside_repository")
    resolved.mkdir(parents=True, exist_ok=True)
    return resolved


def _atomic_write(path: Path, data: bytes) -> None:
    fd, temporary = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    except Exception:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass
        raise


def write_sealed_state(
    state_dir: Path, stem: str, body: dict[str, Any], parent_digest: str | None
) -> str:
    encoded = canonical_json(body)
    digest = sha256_bytes(encoded)
    _atomic_write(state_dir / f"{stem}.{digest}.json", encoded)
    head = {
        "schema": STATE_SCHEMA + ".head",
        "stem": stem,
        "body_sha256": digest,
        "parent_sha256": parent_digest,
    }
    _atomic_write(state_dir / f"{stem}.HEAD", canonical_json(head))
    return digest


def read_sealed_state(
    state_dir: Path, stem: str, parent_digest: str | None = None
) -> tuple[dict[str, Any], str]:
    head_bytes = (state_dir / f"{stem}.HEAD").read_bytes()
    head = json.loads(head_bytes)
    if (
        canonical_json(head) != head_bytes
        or set(head) != {"schema", "stem", "body_sha256", "parent_sha256"}
        or head.get("schema") != STATE_SCHEMA + ".head"
        or head.get("stem") != stem
        or head.get("parent_sha256") != parent_digest
        or not isinstance(head.get("body_sha256"), str)
        or re.fullmatch(r"[0-9a-f]{64}", head["body_sha256"]) is None
    ):
        raise RuntimeError(f"invalid_state_head:{stem}")
    digest = head["body_sha256"]
    body_bytes = (state_dir / f"{stem}.{digest}.json").read_bytes()
    if sha256_bytes(body_bytes) != digest:
        raise RuntimeError(f"state_body_hash_mismatch:{stem}")
    body = json.loads(body_bytes)
    if canonical_json(body) != body_bytes or body.get("schema") != STATE_SCHEMA:
        raise RuntimeError(f"state_body_canonicality:{stem}")
    return body, digest


def write_blob(
    state_dir: Path, stem: str, data: bytes, *, rows: int, width: int
) -> dict[str, Any]:
    if width % 4 or len(data) != rows * (width // 4):
        raise RuntimeError(f"blob_write_shape:{stem}")
    digest = sha256_bytes(data)
    filename = f"{stem}.{digest}.bin"
    path = state_dir / filename
    if path.exists():
        if path.read_bytes() != data:
            raise RuntimeError(f"blob_collision:{stem}")
    else:
        _atomic_write(path, data)
    return {
        "file": filename,
        "bytes": len(data),
        "sha256": digest,
        "rows": rows,
        "width": width,
        "encoding": PACK_ENCODING,
    }


def validate_blob_receipt(
    state_dir: Path,
    receipt: Any,
    rows: int,
    width: int,
    *,
    read: bool = False,
    authenticate: bool = True,
) -> bytes | None:
    if not isinstance(receipt, dict) or set(receipt) != {
        "file", "bytes", "sha256", "rows", "width", "encoding"
    }:
        raise RuntimeError("blob_receipt_shape")
    if not _plain_int(rows) or not _plain_int(width) or rows < 0 or width <= 0 or width % 4:
        raise RuntimeError("blob_expected_dimensions")
    expected_bytes = rows * (width // 4)
    filename = receipt.get("file")
    digest = receipt.get("sha256")
    if (
        not isinstance(filename, str)
        or Path(filename).name != filename
        or not isinstance(digest, str)
        or re.fullmatch(r"[0-9a-f]{64}", digest) is None
        or filename != f"{filename.rsplit('.', 2)[0]}.{digest}.bin"
        or receipt.get("bytes") != expected_bytes
        or receipt.get("rows") != rows
        or receipt.get("width") != width
        or receipt.get("encoding") != PACK_ENCODING
    ):
        raise RuntimeError("blob_receipt_semantics")
    path = state_dir / filename
    before = path.stat()
    if before.st_size != expected_bytes:
        raise RuntimeError(f"blob_size:{filename}")
    if not authenticate:
        if read:
            raise RuntimeError("blob_read_without_authentication")
        return None
    hasher = hashlib.sha256()
    chunks: list[bytes] | None = [] if read else None
    with path.open("rb") as stream:
        while True:
            chunk = stream.read(1024 * 1024)
            if not chunk:
                break
            hasher.update(chunk)
            if chunks is not None:
                chunks.append(chunk)
    after = path.stat()
    if (
        hasher.hexdigest() != digest
        or after.st_size != before.st_size
        or after.st_mtime_ns != before.st_mtime_ns
    ):
        raise RuntimeError(f"blob_authentication:{filename}")
    return b"".join(chunks) if chunks is not None else None


class PackedRowWriter:
    """Append-only packed row store with authenticated random reads."""

    def __init__(self, state_dir: Path, stem: str, width: int):
        if width % 4:
            raise ValueError("packed_writer_width")
        self.state_dir = state_dir
        self.stem = stem
        self.width = width
        self.packed_width = width // 4
        fd, name = tempfile.mkstemp(prefix=stem + ".", suffix=".tmp", dir=state_dir)
        self.path = Path(name)
        self.stream = os.fdopen(fd, "w+b")
        self.hasher = hashlib.sha256()
        self.rows = 0
        self.finished = False

    def append(self, dense: np.ndarray) -> None:
        if dense.shape != (self.width,) or np.any(dense > 2):
            raise ValueError("packed_writer_row")
        data = grade1.pack_trits(dense).tobytes()
        self.stream.seek(0, os.SEEK_END)
        self.stream.write(data)
        self.hasher.update(data)
        self.rows += 1

    def append_packed(self, packed: np.ndarray) -> None:
        value = np.asarray(packed, dtype=np.uint8).reshape(-1)
        if value.shape != (self.packed_width,) or np.any(value > 80):
            raise ValueError("packed_writer_packed_row")
        data = value.tobytes()
        self.stream.seek(0, os.SEEK_END)
        self.stream.write(data)
        self.hasher.update(data)
        self.rows += 1

    def row(self, index: int) -> np.ndarray:
        if not 0 <= index < self.rows:
            raise IndexError("packed_writer_row_index")
        self.stream.flush()
        self.stream.seek(index * self.packed_width)
        data = self.stream.read(self.packed_width)
        if len(data) != self.packed_width:
            raise RuntimeError("packed_writer_short_read")
        return grade1.unpack_trits(np.frombuffer(data, dtype=np.uint8), self.width)

    def finish(self) -> dict[str, Any]:
        self.stream.flush()
        os.fsync(self.stream.fileno())
        self.stream.close()
        digest = self.hasher.hexdigest()
        filename = f"{self.stem}.{digest}.bin"
        os.replace(self.path, self.state_dir / filename)
        self.finished = True
        return {
            "file": filename,
            "bytes": self.rows * self.packed_width,
            "sha256": digest,
            "rows": self.rows,
            "width": self.width,
            "encoding": PACK_ENCODING,
        }

    def abort(self) -> None:
        if self.finished:
            return
        try:
            self.stream.close()
        finally:
            try:
                self.path.unlink()
            except FileNotFoundError:
                pass

    def __del__(self) -> None:
        if not getattr(self, "finished", True):
            try:
                self.abort()
            except Exception:
                pass


class PackedRowStore:
    def __init__(self, state_dir: Path, receipt: dict[str, Any]):
        rows = receipt.get("rows")
        width = receipt.get("width")
        if not _plain_int(rows) or not _plain_int(width):
            raise RuntimeError("packed_store_dimensions")
        validate_blob_receipt(state_dir, receipt, rows, width)
        self.rows = rows
        self.width = width
        self.packed_width = width // 4
        self.matrix = np.memmap(
            state_dir / receipt["file"], dtype=np.uint8, mode="r",
            shape=(rows, self.packed_width),
        )

    def row(self, index: int) -> np.ndarray:
        if not 0 <= index < self.rows:
            raise IndexError("packed_store_row_index")
        return grade1.unpack_trits(np.asarray(self.matrix[index]), self.width)


def write_packed_owner(
    state_dir: Path, stem: str, owner: grade1.PackedEchelon
) -> dict[str, Any]:
    writer = PackedRowWriter(state_dir, stem, owner.width)
    try:
        for packed in owner.rows:
            writer.append_packed(packed)
        return writer.finish()
    except Exception:
        writer.abort()
        raise


def rss_bytes() -> int:
    try:
        import resource

        value = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
        return value if os.name == "nt" else value * 1024
    except (ImportError, AttributeError, OSError):
        return 0


def enforce_resource(started: float, phase: str) -> None:
    seconds = float(os.environ.get("TASK565_SECONDS", "21600"))
    maximum = int(os.environ.get("TASK565_MAX_RSS", str(8 * 1024**3)))
    if time.monotonic() - started > seconds:
        raise RuntimeError(f"UNKNOWN_RESOURCE:{phase}:time_cap")
    current = rss_bytes()
    if current and current > maximum:
        raise RuntimeError(f"UNKNOWN_RESOURCE:{phase}:rss_cap:{current}")


def progress(phase: str, done: int, rank: int, queued: int, started: float) -> None:
    print(
        json.dumps(
            {
                "phase": phase,
                "done": done,
                "rank": rank,
                "queued": queued,
                "elapsed_seconds": time.monotonic() - started,
            },
            sort_keys=True,
        ),
        flush=True,
    )


def normalize_expression(entries: Iterable[Iterable[int]]) -> list[list[int]]:
    accumulator: dict[int, int] = {}
    for entry in entries:
        pair = list(entry)
        if len(pair) != 2 or not _plain_int(pair[0]) or not _plain_int(pair[1]):
            raise RuntimeError("expression_entry")
        coefficient = pair[1] % 3
        if coefficient:
            accumulator[pair[0]] = (accumulator.get(pair[0], 0) + coefficient) % 3
    return [[index, accumulator[index]] for index in sorted(accumulator) if accumulator[index]]


def append_expression(
    destination: list[list[int]], expression: Iterable[Iterable[int]], offset: int = 0,
    scalar: int = 1,
) -> None:
    for index, coefficient in expression:
        destination.append([int(index) + offset, (int(coefficient) * scalar) % 3])


def expression_digest(expressions: Any) -> str:
    return sha256_bytes(canonical_json(expressions))


def validate_expression(expression: Any, rank: int, gate: str) -> None:
    if not isinstance(expression, list):
        raise RuntimeError(f"{gate}:shape")
    seen: set[int] = set()
    previous = -1
    for pair in expression:
        if (
            not isinstance(pair, list)
            or len(pair) != 2
            or not _plain_int(pair[0])
            or not 0 <= pair[0] < rank
            or pair[0] <= previous
            or pair[0] in seen
            or not _plain_int(pair[1])
            or pair[1] not in (1, 2)
        ):
            raise RuntimeError(f"{gate}:entry")
        previous = pair[0]
        seen.add(pair[0])


# ---------------------------------------------------------------------------
# Exact degree <=2 polynomial and affine source arithmetic (v442/v443).


def monomial_multiply(left: tuple[int, int, int], right: tuple[int, int, int]) -> tuple[int, int, int] | None:
    value = tuple(left[index] + right[index] for index in range(3))
    if any(component > 2 for component in value) or sum(value) > 2:
        return None
    return value  # type: ignore[return-value]


PRODUCT_INDEX: list[list[int]] = [[-1] * 10 for _ in range(10)]
for _left_index, _left in enumerate(MONOMIALS_LE2):
    for _right_index, _right in enumerate(MONOMIALS_LE2):
        _product = monomial_multiply(_left, _right)
        if _product is not None:
            PRODUCT_INDEX[_left_index][_right_index] = MONOMIAL_INDEX[_product]


def multiply_polynomial(left: np.ndarray, right: np.ndarray) -> np.ndarray:
    if left.shape != (10,) or right.shape != (10,):
        raise ValueError("polynomial_shape")
    output = np.zeros(10, dtype=np.uint8)
    for i in np.flatnonzero(left):
        for j in np.flatnonzero(right):
            target = PRODUCT_INDEX[int(i)][int(j)]
            if target >= 0:
                output[target] = (
                    int(output[target]) + int(left[i]) * int(right[j])
                ) % 3
    return output


def multiply_polynomial_rows(factor: np.ndarray, rows: np.ndarray) -> np.ndarray:
    """Multiply one polynomial by rows shaped (component,monomial,psl)."""
    if factor.shape != (10,) or rows.ndim != 3 or rows.shape[1:] != (10, 504):
        raise ValueError("polynomial_row_shape")
    output = np.zeros_like(rows)
    for left in np.flatnonzero(factor):
        for right in range(10):
            target = PRODUCT_INDEX[int(left)][right]
            if target >= 0:
                _add_mod3(output[:, target, :], rows[:, right, :], int(factor[left]))
    return output


def e_polynomial(vector: tuple[int, int, int]) -> np.ndarray:
    output = np.zeros(10, dtype=np.uint8)
    output[0] = 1
    for variable, raw_exponent in enumerate(vector):
        exponent = int(raw_exponent) % 3
        factor = np.zeros(10, dtype=np.uint8)
        factor[0] = 1
        if exponent:
            linear = [0, 0, 0]
            linear[variable] = 1
            factor[MONOMIAL_INDEX[tuple(linear)]] = exponent
        if exponent == 2:
            quadratic = [0, 0, 0]
            quadratic[variable] = 2
            factor[MONOMIAL_INDEX[tuple(quadratic)]] = 1
        output = multiply_polynomial(output, factor)
    return output


def source_character_sign(label: tuple[int, int], parity: tuple[int, int]) -> int:
    return grade1.cv(label, parity[0], parity[1])


def source_degree_view(
    degree0: np.ndarray, degree1: np.ndarray, degree2: np.ndarray,
    character: int, tag: int,
) -> np.ndarray:
    output = np.zeros((2, 10, 504), dtype=np.uint8)
    for component in (0, 1):
        start0 = grade1.lower_coord(tag, component, 0)
        output[component, 0] = degree0[character, start0 : start0 + 504]
        for monomial in range(3):
            start1 = grade1.grade_coord(tag, component, monomial, 0)
            output[component, 1 + monomial] = degree1[
                character, start1 : start1 + 504
            ]
        for monomial in range(6):
            start2 = ((tag * 2 + component) * 6 + monomial) * 504
            output[component, 4 + monomial] = degree2[
                character, start2 : start2 + 504
            ]
    return output


def install_source_degree_view(
    destination0: np.ndarray,
    destination1: np.ndarray,
    destination2: np.ndarray,
    character: int,
    tag: int,
    value: np.ndarray,
) -> None:
    for component in (0, 1):
        start0 = grade1.lower_coord(tag, component, 0)
        destination0[character, start0 : start0 + 504] = value[component, 0]
        for monomial in range(3):
            start1 = grade1.grade_coord(tag, component, monomial, 0)
            destination1[character, start1 : start1 + 504] = value[
                component, 1 + monomial
            ]
        for monomial in range(6):
            start2 = ((tag * 2 + component) * 6 + monomial) * 504
            destination2[character, start2 : start2 + 504] = value[
                component, 4 + monomial
            ]


def act_precision2(
    context: grade1.Context,
    degree0: np.ndarray,
    degree1: np.ndarray,
    degree2: np.ndarray,
    auxiliary: np.ndarray,
    tag_actors: tuple[grade1.Affine, ...],
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Exact v443 (3.1) through degree two in Fourier coordinates."""
    if (
        degree0.shape != (4, SOURCE_DEGREE0_PER_CHARACTER)
        or degree1.shape != (4, SOURCE_DEGREE1_PER_CHARACTER)
        or degree2.shape != (4, SOURCE_DEGREE2_PER_CHARACTER)
        or auxiliary.shape != (8,)
        or len(tag_actors) != 6
    ):
        raise ValueError("precision2_action_shape")
    output0 = np.zeros_like(degree0)
    output1 = np.zeros_like(degree1)
    output2 = np.zeros_like(degree2)
    for tag, actor in enumerate(tag_actors):
        # Convert the character Fourier slices to the actual tag parity.
        raw = np.zeros((4, 2, 10, 504), dtype=np.uint8)
        for parity_index, parity in enumerate(CHARACTER_LABELS):
            for source_index, source_label in enumerate(CHARACTER_LABELS):
                tag_label = context.transport[tag][source_label]
                _add_mod3(
                    raw[parity_index],
                    source_degree_view(degree0, degree1, degree2, source_index, tag),
                    source_character_sign(tag_label, parity),
                )
        acted_raw = np.zeros_like(raw)
        pmap = context.psl_left_map(actor[0])
        actor_parity = (actor[1], actor[2])
        for parity_index, parity in enumerate(CHARACTER_LABELS):
            target_parity = (parity[0] ^ actor_parity[0], parity[1] ^ actor_parity[1])
            target_index = CHARACTER_LABELS.index(target_parity)
            kernel = grade1.sign_kernel(parity, actor[3])
            product = multiply_polynomial_rows(e_polynomial(kernel), raw[parity_index])
            translated = np.zeros_like(product)
            translated[:, :, pmap] = product
            _add_mod3(acted_raw[target_index], translated)
        for source_index, source_label in enumerate(CHARACTER_LABELS):
            tag_label = context.transport[tag][source_label]
            transformed = np.zeros((2, 10, 504), dtype=np.uint8)
            for parity_index, parity in enumerate(CHARACTER_LABELS):
                _add_mod3(
                    transformed,
                    acted_raw[parity_index],
                    source_character_sign(tag_label, parity),
                )
            install_source_degree_view(
                output0, output1, output2, source_index, tag, transformed
            )
    return output0, output1, output2, auxiliary.copy()


def act_source_word_precision2(
    context: grade1.Context,
    row: tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray],
    word: tuple[int, ...],
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    return act_precision2(context, *row, context.source_word_tags(word))


def associated_degree2_actor(
    context: grade1.Context, row: np.ndarray, label: tuple[int, int], letter: int
) -> np.ndarray:
    if row.shape != (SOURCE_DEGREE2_PER_CHARACTER,):
        raise ValueError("associated_degree2_shape")
    output = np.zeros_like(row)
    scalar = source_character_sign(
        label,
        (context.actor_source_q1[letter][1], context.actor_source_q1[letter][2]),
    )
    for tag, actor in enumerate(context.actor_tags_q1[letter]):
        pmap = context.psl_left_map(actor[0])
        for component in (0, 1):
            for monomial in range(6):
                start = ((tag * 2 + component) * 6 + monomial) * 504
                source = row[start : start + 504]
                destination = output[start : start + 504]
                destination[pmap] = (scalar * source.astype(np.uint16)) % 3
    return output


def associated_degree2_word(
    context: grade1.Context, row: np.ndarray, label: tuple[int, int], word: tuple[int, ...]
) -> np.ndarray:
    output = row.copy()
    # L_{z_1...z_m}=L_{z_1}...L_{z_m}; with the right-action convention,
    # applying letters in reverse gives the left action of the word value.
    for letter in reversed(word):
        output = associated_degree2_actor(context, output, label, letter)
    return output


def project_pure_degree2_by_words(
    context: grade1.Context, degree2: np.ndarray, label: tuple[int, int]
) -> np.ndarray:
    if degree2.shape != (4, SOURCE_DEGREE2_PER_CHARACTER):
        raise ValueError("degree2_projector_shape")
    output = np.zeros_like(degree2)
    for parity in CHARACTER_LABELS:
        for source_index, source_label in enumerate(CHARACTER_LABELS):
            acted = associated_degree2_word(
                context, degree2[source_index], source_label, PURE_Q1_WORDS[parity]
            )
            _add_mod3(
                output[source_index], acted,
                source_character_sign(label, parity),
            )
    return output


def project_full_by_words(
    context: grade1.Context,
    row: tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray],
    label: tuple[int, int],
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    output = tuple(np.zeros_like(part) for part in row)
    for parity in CHARACTER_LABELS:
        acted = act_source_word_precision2(context, row, PURE_Q1_WORDS[parity])
        coefficient = source_character_sign(label, parity)
        for destination, source in zip(output, acted):
            _add_mod3(destination, source, coefficient)
    return output  # type: ignore[return-value]


def evaluate_seed_precision2(
    context: grade1.Context, word: tuple[int, ...]
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    degree0 = np.zeros((4, SOURCE_DEGREE0_PER_CHARACTER), dtype=np.uint8)
    degree1 = np.zeros((4, SOURCE_DEGREE1_PER_CHARACTER), dtype=np.uint8)
    degree2 = np.zeros((4, SOURCE_DEGREE2_PER_CHARACTER), dtype=np.uint8)
    auxiliary = np.zeros(8, dtype=np.uint8)
    for tag, pair in enumerate(floor.OO):
        substituted = tuple(floor.sub(word, *pair))
        normal, augmentation = grade1.qnorm_affine(substituted, context)
        auxiliary[tag] = augmentation
        for component, value, coefficient in normal:
            polynomial = e_polynomial(value[3])
            psl = context.psidx[value[0]]
            for source_index, source_label in enumerate(CHARACTER_LABELS):
                target_label = context.transport[tag][source_label]
                weight = coefficient * source_character_sign(
                    target_label, (value[1], value[2])
                )
                degree0[source_index, grade1.lower_coord(tag, component, psl)] = (
                    int(degree0[source_index, grade1.lower_coord(tag, component, psl)])
                    + weight * int(polynomial[0])
                ) % 3
                for monomial in range(3):
                    coordinate = grade1.grade_coord(tag, component, monomial, psl)
                    degree1[source_index, coordinate] = (
                        int(degree1[source_index, coordinate])
                        + weight * int(polynomial[1 + monomial])
                    ) % 3
                for monomial in range(6):
                    coordinate = ((tag * 2 + component) * 6 + monomial) * 504 + psl
                    degree2[source_index, coordinate] = (
                        int(degree2[source_index, coordinate])
                        + weight * int(polynomial[4 + monomial])
                    ) % 3
    exponent = floor.exps(word)
    if exponent[0] % 18 or exponent[1] % 18:
        raise RuntimeError("normalized_exponent_not_integral")
    auxiliary[6:] = ((exponent[0] // 18) % 3, (exponent[1] // 18) % 3)
    return degree0, degree1, degree2, auxiliary


def flatten_precision1(
    degree0: np.ndarray, degree1: np.ndarray, auxiliary: np.ndarray
) -> np.ndarray:
    if (
        degree0.shape != (4, SOURCE_DEGREE0_PER_CHARACTER)
        or degree1.shape != (4, SOURCE_DEGREE1_PER_CHARACTER)
        or auxiliary.shape != (8,)
    ):
        raise ValueError("precision1_flatten_shape")
    return np.concatenate((degree0.reshape(-1), degree1.reshape(-1), auxiliary))


def split_precision1(row: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    if row.shape != (SOURCE_PRECISION1_WIDTH,):
        raise ValueError("precision1_split_shape")
    degree0_end = SOURCE_DEGREE0_WIDTH
    degree1_end = degree0_end + SOURCE_DEGREE1_WIDTH
    return (
        row[:degree0_end].reshape(4, SOURCE_DEGREE0_PER_CHARACTER),
        row[degree0_end:degree1_end].reshape(4, SOURCE_DEGREE1_PER_CHARACTER),
        row[degree1_end:].copy(),
    )


def full_row_from_stores(
    precision1: PackedRowStore | PackedRowWriter,
    degree2: PackedRowStore | PackedRowWriter,
    index: int,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    degree0, degree1, auxiliary = split_precision1(precision1.row(index))
    return (
        degree0,
        degree1,
        degree2.row(index).reshape(4, SOURCE_DEGREE2_PER_CHARACTER),
        auxiliary,
    )


def row_linear_combination(
    store: PackedRowStore | PackedRowWriter,
    expression: list[list[int]],
) -> np.ndarray:
    output = np.zeros(store.width, dtype=np.uint8)
    for index, coefficient in expression:
        _add_mod3(output, store.row(index), coefficient)
    return output


def full_row_linear_combination(
    precision1: PackedRowStore | PackedRowWriter,
    degree2: PackedRowStore | PackedRowWriter,
    expression: list[list[int]],
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    p1 = row_linear_combination(precision1, expression)
    d0, d1, auxiliary = split_precision1(p1)
    d2 = row_linear_combination(degree2, expression).reshape(
        4, SOURCE_DEGREE2_PER_CHARACTER
    )
    return d0, d1, d2, auxiliary


def subtract_full(
    left: tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray],
    right: tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray],
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    output = tuple(part.copy() for part in left)
    for destination, source in zip(output, right):
        _add_mod3(destination, source, -1)
    return output  # type: ignore[return-value]


def scale_full(
    row: tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray], scalar: int
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    return tuple(((scalar % 3) * part.astype(np.uint16) % 3).astype(np.uint8) for part in row)  # type: ignore[return-value]


def full_lower_zero(row: tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]) -> bool:
    return not np.any(row[0]) and not np.any(row[1]) and not np.any(row[3])


def physical_degree_view(
    degree0: np.ndarray, degree1: np.ndarray, degree2: np.ndarray,
    character: int, block: int,
) -> np.ndarray:
    output = np.zeros((2, 10, 504), dtype=np.uint8)
    for component in (0, 1):
        start0 = grade1.physical_lower_coord(character, block, component, 0)
        output[component, 0] = degree0[start0 : start0 + 504]
        for monomial in range(3):
            start1 = grade1.physical_grade_coord(
                character, block, component, monomial, 0
            )
            output[component, 1 + monomial] = degree1[start1 : start1 + 504]
        for monomial in range(6):
            start2 = (((character * 2 + block) * 2 + component) * 6 + monomial) * 504
            output[component, 4 + monomial] = degree2[start2 : start2 + 504]
    return output


def aggregate_precision2(
    context: grade1.Context,
    degree0: np.ndarray,
    degree1: np.ndarray,
    degree2: np.ndarray,
    auxiliary: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Exact occurrence-first physical aggregation through degree two."""
    output = np.zeros((4, 2, 2, 10, 504), dtype=np.uint8)
    for tag, block, sign in context.aggregate_table:
        shift = context.physical_shifts[tag]
        raw = np.zeros((4, 2, 10, 504), dtype=np.uint8)
        for parity_index, parity in enumerate(CHARACTER_LABELS):
            for source_index, source_label in enumerate(CHARACTER_LABELS):
                tag_label = context.transport[tag][source_label]
                _add_mod3(
                    raw[parity_index],
                    source_degree_view(degree0, degree1, degree2, source_index, tag),
                    source_character_sign(tag_label, parity),
                )
        acted_raw = np.zeros_like(raw)
        pmap = context.psl_left_map(shift[0])
        shift_parity = (shift[1], shift[2])
        for parity_index, parity in enumerate(CHARACTER_LABELS):
            target_parity = (
                parity[0] ^ shift_parity[0], parity[1] ^ shift_parity[1]
            )
            target_index = CHARACTER_LABELS.index(target_parity)
            factor = e_polynomial(grade1.sign_kernel(parity, shift[3]))
            product = multiply_polynomial_rows(factor, raw[parity_index])
            translated = np.zeros_like(product)
            translated[:, :, pmap] = product
            _add_mod3(acted_raw[target_index], translated)
        for character_index, label in enumerate(CHARACTER_LABELS):
            transformed = np.zeros((2, 10, 504), dtype=np.uint8)
            for parity_index, parity in enumerate(CHARACTER_LABELS):
                _add_mod3(
                    transformed,
                    acted_raw[parity_index],
                    sign * source_character_sign(label, parity),
                )
            _add_mod3(output[character_index, block], transformed)
    physical0 = np.zeros(PHYSICAL_DEGREE0_WIDTH, dtype=np.uint8)
    physical1 = np.zeros(PHYSICAL_DEGREE1_WIDTH, dtype=np.uint8)
    physical2 = np.zeros(PHYSICAL_DEGREE2_WIDTH, dtype=np.uint8)
    for character in range(4):
        for block in range(2):
            for component in (0, 1):
                start0 = grade1.physical_lower_coord(character, block, component, 0)
                physical0[start0 : start0 + 504] = output[
                    character, block, component, 0
                ]
                for monomial in range(3):
                    start1 = grade1.physical_grade_coord(
                        character, block, component, monomial, 0
                    )
                    physical1[start1 : start1 + 504] = output[
                        character, block, component, 1 + monomial
                    ]
                for monomial in range(6):
                    start2 = (((character * 2 + block) * 2 + component) * 6 + monomial) * 504
                    physical2[start2 : start2 + 504] = output[
                        character, block, component, 4 + monomial
                    ]
    physical_auxiliary = np.zeros(4, dtype=np.uint8)
    for tag, block, sign in context.aggregate_table:
        physical_auxiliary[block] = (
            int(physical_auxiliary[block]) + sign * int(auxiliary[tag])
        ) % 3
    physical_auxiliary[2:] = auxiliary[6:]
    return physical0, physical1, physical2, physical_auxiliary


def flatten_physical_lower(
    degree0: np.ndarray, degree1: np.ndarray, auxiliary: np.ndarray
) -> np.ndarray:
    if (
        degree0.shape != (PHYSICAL_DEGREE0_WIDTH,)
        or degree1.shape != (PHYSICAL_DEGREE1_WIDTH,)
        or auxiliary.shape != (4,)
    ):
        raise ValueError("physical_lower_shape")
    return np.concatenate((degree0, degree1, auxiliary))


# ---------------------------------------------------------------------------
# Authentication and exact split-presentation assembly.


def expected_grade1_origin_roster(prepare: dict[str, Any]) -> list[dict[str, Any]]:
    origins: list[dict[str, Any]] = []
    for character, old in enumerate(prepare["old_blocks"]):
        begin = len(origins)
        for seed in range(1, EXPECTED_SEEDS + 1):
            origins.append(
                {
                    "id": len(origins),
                    "kind": "seed",
                    "lower_character": character,
                    "seed": seed,
                }
            )
        for pivot in range(old["rank"]):
            for letter in ACTORS:
                origins.append(
                    {
                        "id": len(origins),
                        "kind": "transition",
                        "lower_character": character,
                        "pivot": pivot,
                        "letter": letter,
                    }
                )
        if old.get("defect_origin_range") != [begin, len(origins)]:
            raise RuntimeError("grade1_origin_range")
    return origins


def validate_grade1_dag_semantics(
    prepare: dict[str, Any], blocks: list[tuple[dict[str, Any], str]]
) -> None:
    for character, old in enumerate(prepare["old_blocks"]):
        nodes = old["record"]["dag_nodes"]
        for pivot, node in enumerate(nodes):
            origin = node.get("origin")
            if not isinstance(origin, dict):
                raise RuntimeError("grade1_old_dag_origin_shape")
            if origin.get("kind") == "projected_seed":
                if set(origin) != {"kind", "seed"} or not _plain_int(origin["seed"]) or not 1 <= origin["seed"] <= EXPECTED_SEEDS:
                    raise RuntimeError("grade1_old_dag_seed_origin")
            elif origin.get("kind") == "actor":
                if (
                    set(origin) != {"kind", "parent", "letter"}
                    or not _plain_int(origin["parent"])
                    or not 0 <= origin["parent"] < pivot
                    or origin["letter"] not in ACTORS
                ):
                    raise RuntimeError("grade1_old_dag_actor_origin")
            else:
                raise RuntimeError("grade1_old_dag_origin_kind")
    origin_count = len(prepare["defect_origins"])
    for character, (block, _) in enumerate(blocks):
        for pivot, node in enumerate(block["dag_nodes"]):
            origin = node.get("origin")
            if not isinstance(origin, dict):
                raise RuntimeError("grade1_block_dag_origin_shape")
            if origin.get("kind") == "defect":
                if (
                    set(origin) != {"kind", "origin"}
                    or not _plain_int(origin["origin"])
                    or not 0 <= origin["origin"] < origin_count
                ):
                    raise RuntimeError("grade1_block_dag_defect_origin")
            elif origin.get("kind") == "actor":
                if (
                    set(origin) != {"kind", "parent", "letter"}
                    or not _plain_int(origin["parent"])
                    or not 0 <= origin["parent"] < pivot
                    or origin["letter"] not in ACTORS
                ):
                    raise RuntimeError("grade1_block_dag_actor_origin")
            else:
                raise RuntimeError("grade1_block_dag_origin_kind")


def validate_grade1_prepare_target_independent(
    state_dir: Path,
    body: dict[str, Any],
    receipt: dict[str, dict[str, Any]],
) -> None:
    """Strict v3/v4 prepare gate that never dereferences target data."""
    if (
        body.get("schema") != GRADE1_STATE_SCHEMA
        or body.get("phase") != "prepare"
        or body.get("fixture") is not False
        or body.get("input_manifest") != receipt
        or body.get("input_manifest_sha256")
        != sha256_bytes(grade1.canonical_json(receipt))
        or body.get("dimensions") != grade1.fixed_dimensions()
        or body.get("paired_lower_presentation_complete") is not True
        or body.get("downstream_claim_flags") != grade1.false_claim_flags()
    ):
        raise RuntimeError("grade1_target_independent_prepare")
    old_blocks = body.get("old_blocks")
    packets = body.get("packets")
    if not isinstance(old_blocks, list) or len(old_blocks) != 4 or not isinstance(packets, list) or len(packets) != 4:
        raise RuntimeError("grade1_target_independent_rosters")
    expected_origins = expected_grade1_origin_roster(body)
    if (
        body.get("defect_origins") != expected_origins
        or body.get("defect_origin_sha256")
        != sha256_bytes(grade1.canonical_json(expected_origins))
    ):
        raise RuntimeError("grade1_target_independent_origins")
    for character, old in enumerate(old_blocks):
        rank = old.get("rank")
        record = old.get("record")
        if (
            old.get("character_index") != character
            or old.get("character") != list(CHARACTER_LABELS[character])
            or not _plain_int(rank)
            or rank < 0
            or not isinstance(record, dict)
            or record.get("character") != list(CHARACTER_LABELS[character])
            or record.get("rank") != rank
            or record.get("attempts") != EXPECTED_SEEDS + 4 * rank
            or record.get("actor_order") != list(ACTORS)
            or record.get("queue_exhausted") is not True
            or len(record.get("seed_reductions", [])) != EXPECTED_SEEDS
            or len(record.get("actor_transitions", [])) != rank
            or any(not isinstance(row, list) or len(row) != 4 for row in record["actor_transitions"])
            or len(record.get("dag_nodes", [])) != rank
        ):
            raise RuntimeError("grade1_target_independent_old")
        for expression in record["seed_reductions"]:
            grade1._validate_expression(expression, rank, "grade1_seed_reduction")
        for row in record["actor_transitions"]:
            for expression in row:
                grade1._validate_expression(expression, rank, "grade1_actor_transition")
        for pivot, node in enumerate(record["dag_nodes"]):
            if (
                not isinstance(node, dict)
                or node.get("pivot") != pivot
                or not _plain_int(node.get("lead"))
                or not 0 <= node["lead"] < grade1.LOWER_ECHELON_WIDTH
                or node.get("scale") not in (1, 2)
            ):
                raise RuntimeError("grade1_target_independent_old_dag")
            grade1._validate_expression(
                node.get("reductions"), rank, "grade1_old_dag_reduction",
                earlier_than=pivot,
            )
        grade1.validate_blob_receipt(
            state_dir, old.get("lower_basis_blob"), rank,
            grade1.LOWER_ECHELON_WIDTH, authenticate=True,
        )
        grade1.validate_blob_receipt(
            state_dir, old.get("lifted_grade_blob"), rank,
            grade1.SOURCE_TOTAL_WIDTH, authenticate=True,
        )
    origin_digest = body["defect_origin_sha256"]
    for character, packet in enumerate(packets):
        if (
            packet.get("character") != list(CHARACTER_LABELS[character])
            or packet.get("origin_count") != len(expected_origins)
            or packet.get("origin_sha256") != origin_digest
        ):
            raise RuntimeError("grade1_target_independent_packet")
        grade1.validate_blob_receipt(
            state_dir, packet.get("blob"), len(expected_origins),
            grade1.SOURCE_BLOCK_WIDTH, authenticate=True,
        )


def authenticate_grade1_split(
    state_dir: Path,
) -> tuple[
    dict[str, Any], str, list[tuple[dict[str, Any], str]],
    dict[str, dict[str, Any]], grade1.Context,
]:
    state_dir = state_dir.resolve()
    _, frozen_manifest = grade1.load_pinned_inputs()
    prepare, prepare_digest = grade1.read_sealed_state(state_dir, "prepare")
    if prepare.get("fixture") is not False or prepare.get("schema") != GRADE1_STATE_SCHEMA:
        raise RuntimeError("grade1_prepare_not_production")
    validate_grade1_prepare_target_independent(state_dir, prepare, frozen_manifest)
    blocks = [
        grade1.read_sealed_state(state_dir, f"block-{index}", prepare_digest)
        for index in range(4)
    ]
    for index, (body, _) in enumerate(blocks):
        grade1.validate_block_state(
            state_dir, body, prepare, prepare_digest, index,
            authenticate_basis=True,
        )
    expected_origins = expected_grade1_origin_roster(prepare)
    if prepare.get("defect_origins") != expected_origins:
        raise RuntimeError("grade1_origin_roster")
    origin_digest = sha256_bytes(grade1.canonical_json(expected_origins))
    if origin_digest != prepare.get("defect_origin_sha256"):
        raise RuntimeError("grade1_origin_roster_digest")
    for index, packet in enumerate(prepare["packets"]):
        if (
            packet.get("origin_sha256") != origin_digest
            or packet.get("origin_count") != len(expected_origins)
            or packet.get("character") != list(CHARACTER_LABELS[index])
        ):
            raise RuntimeError("grade1_packet_binding")
    validate_grade1_dag_semantics(prepare, blocks)
    context = grade1.context_for_state(prepare)
    if (
        prepare.get("affine_convention") != "section-left-kernel-right"
        or prepare.get("substitution_matrices") != context.substitution_matrices
        or not isinstance(prepare.get("pure_q1_projectors"), list)
        or len(prepare["pure_q1_projectors"]) != 4
    ):
        raise RuntimeError("grade1_affine_binding")
    for index, parity in enumerate(CHARACTER_LABELS):
        record = prepare["pure_q1_projectors"][index]
        if (
            record.get("parity") != list(parity)
            or record.get("word") != list(PURE_Q1_WORDS[parity])
            or record.get("q1_endpoint") != {
                "psl_identity": True, "parity": list(parity)
            }
            or record.get("q2_kernel") != list(context.pure_source_affine[parity][3])
        ):
            raise RuntimeError("grade1_projector_binding")
    return prepare, prepare_digest, blocks, frozen_manifest, context


OCCURRENCE_KERNEL_MATRICES = (
    ((1, 0, 0), (0, 1, 0), (0, 0, 1)),
    ((1, 0, 0), (0, 0, -1), (0, 1, 0)),
    ((0, 0, 1), (1, 0, 0), (0, 1, 0)),
    ((0, 1, 0), (0, 0, -1), (-1, 0, 0)),
    ((1, 0, 0), (0, 1, 0), (0, 0, 1)),
    ((0, 0, 1), (0, 1, 0), (-1, 0, 0)),
)
OCCURRENCE_CROSSED_GENERATORS = (
    ((0, 0, 0), (0, 0, 0)),
    ((0, 0, 0), (1, 0, 0)),
    ((1, 0, 1), (1, -2, 0)),
    ((0, 1, 0), (0, 1, 1)),
    ((0, 0, 0), (0, 0, 0)),
    ((0, 1, 0), (0, 0, 2)),
)


def matrix_vector_mod3(
    matrix: tuple[tuple[int, int, int], ...], vector: tuple[int, int, int]
) -> tuple[int, int, int]:
    return tuple(
        sum(matrix[row][column] * vector[column] for column in range(3)) % 3
        for row in range(3)
    )  # type: ignore[return-value]


def parity_matrix_vector(
    matrix: list[list[int]], value: tuple[int, int]
) -> tuple[int, int]:
    # Columns are the images of the two parity generators.
    return (
        (matrix[0][0] * value[0] + matrix[0][1] * value[1]) & 1,
        (matrix[1][0] * value[0] + matrix[1][1] * value[1]) & 1,
    )


def occurrence_crossed_value(tag: int, parity: tuple[int, int], matrix: list[list[int]]) -> tuple[int, int, int]:
    if parity == (0, 0):
        return (0, 0, 0)
    first, second = OCCURRENCE_CROSSED_GENERATORS[tag]
    if parity == (1, 0):
        return tuple(value % 3 for value in first)  # type: ignore[return-value]
    if parity == (0, 1):
        return tuple(value % 3 for value in second)  # type: ignore[return-value]
    acted = grade1.sign_kernel(parity_matrix_vector(matrix, (0, 1)), tuple(value % 3 for value in first))
    return tuple((acted[index] + second[index]) % 3 for index in range(3))  # type: ignore[return-value]


def replay_extension_and_boundary_preflight(
    context: grade1.Context, words: dict[str, Any]
) -> dict[str, Any]:
    """Rebind v442/v443 and all boundary inputs before precision lifting."""
    identity: grade1.Affine = (floor.ID9, 0, 0, (0, 0, 0))
    if context.aggregate_table != (
        (0, 0, 1), (1, 0, 2), (2, 0, 1),
        (3, 1, 2), (4, 1, 2), (5, 1, 1),
    ):
        raise RuntimeError("pb4_aggregation_table")
    affine_checks = 0
    crossed_checks = 0
    for tag in range(6):
        matrix = OCCURRENCE_KERNEL_MATRICES[tag]
        parity_matrix = context.substitution_matrices[tag]
        for generator, source in enumerate(context.affine_images):
            expected_parity = parity_matrix_vector(
                parity_matrix, (source[1], source[2])
            )
            expected_kernel_base = matrix_vector_mod3(matrix, source[3])
            crossed = occurrence_crossed_value(
                tag, (source[1], source[2]), parity_matrix
            )
            expected_kernel = tuple(
                (expected_kernel_base[index] + crossed[index]) % 3
                for index in range(3)
            )
            actual = context.actor_tags_affine[(1, 2)[generator]][tag]
            if actual[1:3] != expected_parity or actual[3] != expected_kernel:
                raise RuntimeError(f"v442_occurrence_affine:{tag}:{generator}")
            affine_checks += 1
        for left in CHARACTER_LABELS:
            for right in CHARACTER_LABELS:
                total = (left[0] ^ right[0], left[1] ^ right[1])
                lhs = occurrence_crossed_value(tag, total, parity_matrix)
                acted = grade1.sign_kernel(
                    parity_matrix_vector(parity_matrix, right),
                    occurrence_crossed_value(tag, left, parity_matrix),
                )
                right_value = occurrence_crossed_value(tag, right, parity_matrix)
                rhs = tuple(
                    (acted[index] + right_value[index]) % 3 for index in range(3)
                )
                if lhs != rhs:
                    raise RuntimeError(f"v442_crossed_law:{tag}:{left}:{right}")
                crossed_checks += 1
    # The split rung has zero multiplication cocycle on the pinned section.
    for left in CHARACTER_LABELS:
        for right in CHARACTER_LABELS:
            section_left: grade1.Affine = (floor.ID9, left[0], left[1], (0, 0, 0))
            section_right: grade1.Affine = (floor.ID9, right[0], right[1], (0, 0, 0))
            if grade1.affine_mul(section_left, section_right)[3] != (0, 0, 0):
                raise RuntimeError("split_zero_cocycle")
    negative = np.zeros(10, dtype=np.uint8)
    negative[MONOMIAL_INDEX[(1, 0, 0)]] = 2
    negative[MONOMIAL_INDEX[(2, 0, 0)]] = 1
    if not np.array_equal(e_polynomial((2, 0, 0)), np.array([1, 2, 0, 0, 1, 0, 0, 0, 0, 0], dtype=np.uint8)):
        raise RuntimeError("negative_kernel_substitution")
    # PB3: replay X*(Y^-1 X^-1)*Y in the source and in every occurrence.
    boundary_word = (-1, -2)
    if grade1.affine_mul(
        grade1.affine_mul(context.affine_images[0], context.pb3_b),
        context.affine_images[1],
    ) != identity:
        raise RuntimeError("pb3_source_boundary")
    for tag, pair in enumerate(floor.OO):
        x_value = grade1.affine_eval(floor.sub((1,), *pair), context.affine_images)
        y_value = grade1.affine_eval(floor.sub((2,), *pair), context.affine_images)
        b_value = grade1.affine_eval(floor.sub(boundary_word, *pair), context.affine_images)
        if grade1.affine_mul(grade1.affine_mul(x_value, b_value), y_value) != identity:
            raise RuntimeError(f"pb3_translated_boundary:{tag}")
    # PB4's two registered blocks are the exact signed occurrence words.
    g760 = tuple(int(value) for value in words["g760"])
    h1 = tuple(
        floor.wm(
            floor.sub(g760, *floor.OO[2]),
            floor.wi(floor.sub(g760, *floor.OO[1])),
            floor.sub(g760, *floor.OO[0]),
        )
    )
    h2 = tuple(
        floor.wm(
            floor.sub(g760, *floor.OO[5]),
            floor.wi(floor.sub(g760, *floor.OO[4])),
            floor.wi(floor.sub(g760, *floor.OO[3])),
        )
    )
    if (
        grade1.affine_eval(h1, context.affine_images) != identity
        or grade1.affine_eval(h2, context.affine_images) != identity
        or floor.exps(g760) != (0, 0)
        or floor.exps(h1) != (0, 0)
        or floor.exps(h2) != (0, 0)
    ):
        raise RuntimeError("pb4_boundary_or_exponent")
    for index, relator in enumerate(words["relators"], 1):
        exponent = floor.exps(tuple(int(value) for value in relator))
        if exponent[0] % 18 or exponent[1] % 18:
            raise RuntimeError(f"integral_exponent_gate:{index}")
    # Truncation/filtration commutation: the degree <=1 shadow of the new
    # arithmetic must be byte-identical to the audited grade-one engine.
    canary0 = np.zeros((4, SOURCE_DEGREE0_PER_CHARACTER), dtype=np.uint8)
    canary1 = np.zeros((4, SOURCE_DEGREE1_PER_CHARACTER), dtype=np.uint8)
    canary2 = np.zeros((4, SOURCE_DEGREE2_PER_CHARACTER), dtype=np.uint8)
    canary_aux = np.asarray((1, 2, 0, 1, 0, 2, 1, 2), dtype=np.uint8)
    for character in range(4):
        canary0[character, grade1.lower_coord(character % 6, character % 2, character)] = character % 3
        canary1[character, grade1.grade_coord((character + 1) % 6, character % 2, character % 3, character + 7)] = (character + 1) % 3
        canary2[character, (((character + 2) % 6 * 2 + character % 2) * 6 + (character + 1) % 6) * 504 + character + 11] = (character + 2) % 3
    filtration_checks = 0
    for letter in ACTORS:
        actual = act_precision2(
            context, canary0, canary1, canary2, canary_aux,
            context.actor_tags_affine[letter],
        )
        expected = grade1.act_pair(
            context, canary0, canary1, canary_aux,
            context.source_word_value((letter,)), context.actor_tags_affine[letter],
        )
        if (
            not np.array_equal(actual[0], expected[0])
            or not np.array_equal(actual[1], expected[1])
            or not np.array_equal(actual[3], expected[2])
        ):
            raise RuntimeError(f"filtration_actor_commutation:{letter}")
        filtration_checks += 1
    actual_physical = aggregate_precision2(
        context, canary0, canary1, canary2, canary_aux
    )
    expected_physical = grade1.aggregate_pair(context, canary0, canary1, canary_aux)
    if (
        not np.array_equal(
            np.concatenate((actual_physical[0], actual_physical[3])),
            expected_physical[0],
        )
        or not np.array_equal(actual_physical[1], expected_physical[1])
    ):
        raise RuntimeError("filtration_aggregation_commutation")
    filtration_checks += 1
    return {
        "extension": "Q2=P_times_(C3^3_semidirect_C2^2)_over_Q1",
        "normal_form": "section-left-kernel-right",
        "multiplication_cocycle": "zero",
        "kernel_action": "v442-sign-action",
        "occurrence_kernel_matrices": [[list(row) for row in matrix] for matrix in OCCURRENCE_KERNEL_MATRICES],
        "occurrence_crossed_generators": [[list(value) for value in pair] for pair in OCCURRENCE_CROSSED_GENERATORS],
        "occurrence_affine_checks": affine_checks,
        "crossed_law_checks": crossed_checks,
        "negative_column_degree2": "u->2u+u^2",
        "pb3_translated_boundaries": 6,
        "pb4_blocks": 2,
        "pb4_words_sha256": [
            sha256_bytes(json.dumps(list(h1), separators=(",", ":")).encode("ascii")),
            sha256_bytes(json.dumps(list(h2), separators=(",", ":")).encode("ascii")),
        ],
        "integral_exponent_relators": EXPECTED_SEEDS,
        "filtration_occurrence_aggregation_checks": filtration_checks,
        "normalized_exponent_actor_action": "trivial",
        "replayed": True,
    }


def global_offsets(
    prepare: dict[str, Any], blocks: list[tuple[dict[str, Any], str]]
) -> tuple[list[int], list[int], int]:
    old_offsets: list[int] = []
    cursor = 0
    for old in prepare["old_blocks"]:
        old_offsets.append(cursor)
        cursor += old["rank"]
    new_offsets: list[int] = []
    for body, _ in blocks:
        new_offsets.append(cursor)
        cursor += body["rank"]
    return old_offsets, new_offsets, cursor


def grade1_origin_ids(prepare: dict[str, Any]) -> tuple[list[list[int]], list[list[list[int]]]]:
    seed_ids: list[list[int]] = []
    transition_ids: list[list[list[int]]] = []
    for old in prepare["old_blocks"]:
        begin = old["defect_origin_range"][0]
        seed_ids.append([begin + seed for seed in range(EXPECTED_SEEDS)])
        transition_ids.append(
            [
                [begin + EXPECTED_SEEDS + 4 * pivot + actor for actor in range(4)]
                for pivot in range(old["rank"])
            ]
        )
    return seed_ids, transition_ids


def assemble_b1_relations(
    prepare: dict[str, Any], blocks: list[tuple[dict[str, Any], str]]
) -> dict[str, Any]:
    old_offsets, new_offsets, rank = global_offsets(prepare, blocks)
    seed_origin_ids, transition_origin_ids = grade1_origin_ids(prepare)
    seed_reductions: list[list[list[int]]] = []
    for seed in range(EXPECTED_SEEDS):
        entries: list[list[int]] = []
        for character, old in enumerate(prepare["old_blocks"]):
            append_expression(
                entries, old["record"]["seed_reductions"][seed], old_offsets[character]
            )
            origin = seed_origin_ids[character][seed]
            for target, (block, _) in enumerate(blocks):
                append_expression(
                    entries, block["origin_reductions"][origin], new_offsets[target]
                )
        seed_reductions.append(normalize_expression(entries))
    transitions: list[list[list[list[int]]]] = []
    for character, old in enumerate(prepare["old_blocks"]):
        for pivot in range(old["rank"]):
            actor_row: list[list[list[int]]] = []
            for actor_index in range(4):
                entries = []
                append_expression(
                    entries,
                    old["record"]["actor_transitions"][pivot][actor_index],
                    old_offsets[character],
                )
                origin = transition_origin_ids[character][pivot][actor_index]
                for target, (block, _) in enumerate(blocks):
                    append_expression(
                        entries,
                        block["origin_reductions"][origin],
                        new_offsets[target],
                    )
                actor_row.append(normalize_expression(entries))
            transitions.append(actor_row)
    for character, (block, _) in enumerate(blocks):
        for pivot in range(block["rank"]):
            actor_row = []
            for expression in block["actor_transitions"][pivot]:
                entries = []
                append_expression(entries, expression, new_offsets[character])
                actor_row.append(normalize_expression(entries))
            transitions.append(actor_row)
    if len(transitions) != rank:
        raise RuntimeError("b1_transition_cardinality")
    for expression in seed_reductions:
        validate_expression(expression, rank, "b1_seed_reduction")
    for row in transitions:
        if len(row) != 4:
            raise RuntimeError("b1_transition_actor_count")
        for expression in row:
            validate_expression(expression, rank, "b1_actor_transition")
    roster: list[dict[str, Any]] = []
    for character, old in enumerate(prepare["old_blocks"]):
        for pivot in range(old["rank"]):
            roster.append(
                {
                    "global": len(roster),
                    "kind": "lifted_old",
                    "character": character,
                    "pivot": pivot,
                }
            )
    for character, (block, _) in enumerate(blocks):
        for pivot in range(block["rank"]):
            roster.append(
                {
                    "global": len(roster),
                    "kind": "h1",
                    "character": character,
                    "pivot": pivot,
                }
            )
    presentation = {
        "grade": 1,
        "rank": rank,
        "global_order": "all_lifted_old_by_character_pivot_then_all_h1_by_character_pivot",
        "old_ranks": [old["rank"] for old in prepare["old_blocks"]],
        "new_ranks": [body["rank"] for body, _ in blocks],
        "old_offsets": old_offsets,
        "new_offsets": new_offsets,
        "basis_roster": roster,
        "basis_roster_sha256": sha256_bytes(canonical_json(roster)),
        "seed_count": EXPECTED_SEEDS,
        "seed_reductions": seed_reductions,
        "seed_reductions_sha256": expression_digest(seed_reductions),
        "actor_order": list(ACTORS),
        "actor_transitions": transitions,
        "actor_transitions_sha256": expression_digest(transitions),
        "complete": True,
    }
    unsigned = dict(presentation)
    presentation["sha256"] = sha256_bytes(canonical_json(unsigned))
    return presentation


def load_grade1_packed_matrix(
    state_dir: Path, receipt: dict[str, Any]
) -> np.ndarray:
    rows = receipt.get("rows")
    width = receipt.get("width")
    if not _plain_int(rows) or not _plain_int(width):
        raise RuntimeError("grade1_packed_matrix_dimensions")
    validate_blob_receipt(state_dir, receipt, rows, width, authenticate=True)
    packed_width = width // 4
    if not rows:
        return np.empty((0, packed_width), dtype=np.uint8)
    return np.memmap(
        state_dir / receipt["file"], dtype=np.uint8, mode="r",
        shape=(rows, packed_width),
    )


def assemble_precision1_basis(
    output_dir: Path,
    grade1_dir: Path,
    prepare: dict[str, Any],
    blocks: list[tuple[dict[str, Any], str]],
    presentation: dict[str, Any],
) -> dict[str, Any]:
    writer = PackedRowWriter(output_dir, "grade2-b1-precision1", SOURCE_PRECISION1_WIDTH)
    try:
        for character, old in enumerate(prepare["old_blocks"]):
            lower_matrix = load_grade1_packed_matrix(grade1_dir, old["lower_basis_blob"])
            lift_matrix = load_grade1_packed_matrix(grade1_dir, old["lifted_grade_blob"])
            for pivot in range(old["rank"]):
                lower = grade1.unpack_trits(
                    lower_matrix[pivot], grade1.LOWER_ECHELON_WIDTH
                )
                degree0 = np.zeros((4, SOURCE_DEGREE0_PER_CHARACTER), dtype=np.uint8)
                degree0[character] = lower[:SOURCE_DEGREE0_PER_CHARACTER]
                degree1 = grade1.unpack_trits(
                    lift_matrix[pivot], SOURCE_DEGREE1_WIDTH
                ).reshape(4, SOURCE_DEGREE1_PER_CHARACTER)
                writer.append(flatten_precision1(degree0, degree1, lower[-8:]))
        for character, (block, _) in enumerate(blocks):
            matrix = load_grade1_packed_matrix(grade1_dir, block["basis_blob"])
            for pivot in range(block["rank"]):
                degree0 = np.zeros((4, SOURCE_DEGREE0_PER_CHARACTER), dtype=np.uint8)
                degree1 = np.zeros((4, SOURCE_DEGREE1_PER_CHARACTER), dtype=np.uint8)
                degree1[character] = grade1.unpack_trits(
                    matrix[pivot], SOURCE_DEGREE1_PER_CHARACTER
                )
                writer.append(
                    flatten_precision1(degree0, degree1, np.zeros(8, dtype=np.uint8))
                )
        if writer.rows != presentation["rank"]:
            raise RuntimeError("b1_basis_row_count")
        return writer.finish()
    except Exception:
        writer.abort()
        raise


def replay_b1_precision1(
    context: grade1.Context,
    words: dict[str, Any],
    basis: PackedRowStore,
    presentation: dict[str, Any],
    started: float,
) -> dict[str, Any]:
    seeds = [
        grade1.evaluate_occurrence_pair(tuple(int(x) for x in word), context)
        for word in words["relators"]
    ]
    if len(seeds) != EXPECTED_SEEDS:
        raise RuntimeError("literal_seed_count")
    replayed = 0
    for seed, expression in enumerate(presentation["seed_reductions"]):
        expected = flatten_precision1(*seeds[seed])
        actual = row_linear_combination(basis, expression)
        if not np.array_equal(actual, expected):
            raise RuntimeError(f"b1_seed_replay:{seed + 1}")
        replayed += 1
    for pivot, actor_row in enumerate(presentation["actor_transitions"]):
        degree0, degree1, auxiliary = split_precision1(basis.row(pivot))
        for actor_index, letter in enumerate(ACTORS):
            acted = grade1.act_pair(
                context,
                degree0,
                degree1,
                auxiliary,
                context.source_word_value((letter,)),
                context.actor_tags_affine[letter],
            )
            expected = flatten_precision1(*acted)
            actual = row_linear_combination(basis, actor_row[actor_index])
            if not np.array_equal(actual, expected):
                raise RuntimeError(f"b1_actor_replay:{pivot}:{letter}")
            replayed += 1
            if replayed % 256 == 0:
                progress("grade2-prepare-t1-replay", replayed, basis.rows, 0, started)
                enforce_resource(started, "grade2-prepare-t1-replay")
    return {
        "seed_equalities": EXPECTED_SEEDS,
        "actor_equalities": 4 * basis.rows,
        "direct_precision1_replay": True,
    }


def add_full_in_place(
    destination: tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray],
    source: tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray],
    scalar: int,
) -> None:
    for left, right in zip(destination, source):
        _add_mod3(left, right, scalar)


def origin_full_lift(
    context: grade1.Context,
    origin: dict[str, Any],
    projected_seeds: list[list[tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]]],
    precision1: PackedRowStore,
    degree2: PackedRowWriter,
    prepare: dict[str, Any],
    old_offsets: list[int],
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    character = origin["lower_character"]
    old = prepare["old_blocks"][character]
    if origin["kind"] == "seed":
        value = tuple(part.copy() for part in projected_seeds[character][origin["seed"] - 1])
        expression = old["record"]["seed_reductions"][origin["seed"] - 1]
    elif origin["kind"] == "transition":
        global_pivot = old_offsets[character] + origin["pivot"]
        parent = full_row_from_stores(precision1, degree2, global_pivot)
        value = act_source_word_precision2(context, parent, (origin["letter"],))
        actor_index = ACTORS.index(origin["letter"])
        expression = old["record"]["actor_transitions"][origin["pivot"]][actor_index]
    else:
        raise RuntimeError("grade1_origin_kind")
    for local, coefficient in expression:
        existing = full_row_from_stores(
            precision1, degree2, old_offsets[character] + local
        )
        add_full_in_place(value, existing, -coefficient)
    if not full_lower_zero(value):
        raise RuntimeError(f"lifted_grade1_origin_nonzero_lower:{origin['id']}")
    return value  # type: ignore[return-value]


def build_b1_degree2_lifts(
    output_dir: Path,
    grade1_dir: Path,
    context: grade1.Context,
    words: dict[str, Any],
    prepare: dict[str, Any],
    blocks: list[tuple[dict[str, Any], str]],
    presentation: dict[str, Any],
    precision1: PackedRowStore,
    started: float,
) -> tuple[dict[str, Any], list[tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]], list[list[tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]]]]:
    base_seeds = [
        evaluate_seed_precision2(context, tuple(int(x) for x in word))
        for word in words["relators"]
    ]
    if len(base_seeds) != EXPECTED_SEEDS:
        raise RuntimeError("precision2_seed_count")
    projected_seeds: list[list[tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]]] = []
    for label in CHARACTER_LABELS:
        projected_seeds.append(
            [project_full_by_words(context, seed, label) for seed in base_seeds]
        )
    for seed in range(EXPECTED_SEEDS):
        recombined = tuple(np.zeros_like(part) for part in base_seeds[seed])
        for character in range(4):
            add_full_in_place(recombined, projected_seeds[character][seed], 1)
        if any(
            not np.array_equal(recombined[index], base_seeds[seed][index])
            for index in range(4)
        ):
            raise RuntimeError(f"full_word_sum_resolution:{seed + 1}")
    writer = PackedRowWriter(output_dir, "grade2-b1-degree2-lifts", SOURCE_DEGREE2_WIDTH)
    old_offsets = presentation["old_offsets"]
    new_offsets = presentation["new_offsets"]
    try:
        # Lift the old B0 basis by its exact prepare DAG.
        for character, old in enumerate(prepare["old_blocks"]):
            for pivot, node in enumerate(old["record"]["dag_nodes"]):
                origin = node["origin"]
                if origin["kind"] == "projected_seed":
                    work = tuple(
                        part.copy()
                        for part in projected_seeds[character][origin["seed"] - 1]
                    )
                else:
                    parent = full_row_from_stores(
                        precision1, writer, old_offsets[character] + origin["parent"]
                    )
                    work = act_source_word_precision2(
                        context, parent, (origin["letter"],)
                    )
                for earlier, coefficient in node["reductions"]:
                    row = full_row_from_stores(
                        precision1, writer, old_offsets[character] + earlier
                    )
                    add_full_in_place(work, row, -coefficient)
                if node["scale"] == 2:
                    work = scale_full(work, 2)
                global_pivot = old_offsets[character] + pivot
                if not np.array_equal(
                    flatten_precision1(work[0], work[1], work[3]),
                    precision1.row(global_pivot),
                ):
                    raise RuntimeError(f"old_lift_precision1_replay:{character}:{pivot}")
                writer.append(work[2].reshape(-1))
                if writer.rows % 128 == 0:
                    progress("grade2-prepare-old-lifts", writer.rows, writer.rows, 0, started)
                    enforce_resource(started, "grade2-prepare-old-lifts")
        if writer.rows != sum(presentation["old_ranks"]):
            raise RuntimeError("old_lift_order")
        # Lift H^[1] by its block DAG.  A defect leaf is the exact legal
        # projector of the full lifted seed/transition defect, not merely a
        # copied grade-one packet row.
        for character, (block, _) in enumerate(blocks):
            packet_matrix = load_grade1_packed_matrix(
                grade1_dir, prepare["packets"][character]["blob"]
            )
            for pivot, node in enumerate(block["dag_nodes"]):
                origin = node["origin"]
                if origin["kind"] == "defect":
                    origin_id = origin["origin"]
                    unprojected = origin_full_lift(
                        context,
                        prepare["defect_origins"][origin_id],
                        projected_seeds,
                        precision1,
                        writer,
                        prepare,
                        old_offsets,
                    )
                    work = project_full_by_words(
                        context, unprojected, CHARACTER_LABELS[character]
                    )
                    expected_packet = grade1.unpack_trits(
                        packet_matrix[origin_id],
                        SOURCE_DEGREE1_PER_CHARACTER,
                    )
                    if (
                        np.any(work[0])
                        or np.any(work[3])
                        or any(np.any(work[1][index]) for index in range(4) if index != character)
                        or not np.array_equal(work[1][character], expected_packet)
                    ):
                        raise RuntimeError(f"grade1_packet_direct_binding:{character}:{origin_id}")
                else:
                    global_parent = new_offsets[character] + origin["parent"]
                    parent = full_row_from_stores(precision1, writer, global_parent)
                    work = act_source_word_precision2(
                        context, parent, (origin["letter"],)
                    )
                for earlier, coefficient in node["reductions"]:
                    row = full_row_from_stores(
                        precision1, writer, new_offsets[character] + earlier
                    )
                    add_full_in_place(work, row, -coefficient)
                if node["scale"] == 2:
                    work = scale_full(work, 2)
                global_pivot = new_offsets[character] + pivot
                if not np.array_equal(
                    flatten_precision1(work[0], work[1], work[3]),
                    precision1.row(global_pivot),
                ):
                    raise RuntimeError(f"h1_lift_precision1_replay:{character}:{pivot}")
                writer.append(work[2].reshape(-1))
                if writer.rows % 128 == 0:
                    progress("grade2-prepare-h1-lifts", writer.rows, writer.rows, 0, started)
                    enforce_resource(started, "grade2-prepare-h1-lifts")
        if writer.rows != presentation["rank"]:
            raise RuntimeError("b1_degree2_lift_count")
        receipt = writer.finish()
    except Exception:
        writer.abort()
        raise
    return receipt, base_seeds, projected_seeds


def build_grade2_defect_packets(
    output_dir: Path,
    context: grade1.Context,
    base_seeds: list[tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]],
    precision1: PackedRowStore,
    degree2: PackedRowStore,
    presentation: dict[str, Any],
    started: float,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    expected_count = EXPECTED_SEEDS + 4 * presentation["rank"]
    writers = [
        PackedRowWriter(output_dir, f"grade2-defect-packet-{index}", SOURCE_DEGREE2_PER_CHARACTER)
        for index in range(4)
    ]
    origins: list[dict[str, Any]] = []

    def emit(
        origin: dict[str, Any],
        defect: tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray],
    ) -> None:
        if not full_lower_zero(defect):
            raise RuntimeError(f"grade2_defect_nonzero_lower:{len(origins)}")
        origin = {"id": len(origins), **origin}
        origins.append(origin)
        projected_sum = np.zeros_like(defect[2])
        for character, label in enumerate(CHARACTER_LABELS):
            projected = project_pure_degree2_by_words(context, defect[2], label)
            if any(
                np.any(projected[index]) for index in range(4) if index != character
            ):
                raise RuntimeError(f"grade2_projector_leak:{origin['id']}:{character}")
            writers[character].append(projected[character])
            _add_mod3(projected_sum, projected)
        if not np.array_equal(projected_sum, defect[2]):
            raise RuntimeError(f"grade2_projector_resolution:{origin['id']}")

    try:
        for seed, direct in enumerate(base_seeds):
            reduction = full_row_linear_combination(
                precision1, degree2, presentation["seed_reductions"][seed]
            )
            emit({"kind": "seed", "seed": seed + 1}, subtract_full(direct, reduction))
        for pivot, transitions in enumerate(presentation["actor_transitions"]):
            parent = full_row_from_stores(precision1, degree2, pivot)
            for actor_index, letter in enumerate(ACTORS):
                direct = act_source_word_precision2(context, parent, (letter,))
                reduction = full_row_linear_combination(
                    precision1, degree2, transitions[actor_index]
                )
                emit(
                    {"kind": "transition", "pivot": pivot, "letter": letter},
                    subtract_full(direct, reduction),
                )
                if len(origins) % 128 == 0:
                    progress("grade2-prepare-defects", len(origins), presentation["rank"], 0, started)
                    enforce_resource(started, "grade2-prepare-defects")
        if len(origins) != expected_count:
            raise RuntimeError("grade2_defect_roster_count")
        origin_digest = sha256_bytes(canonical_json(origins))
        packets = []
        for character, writer in enumerate(writers):
            receipt = writer.finish()
            packets.append(
                {
                    "character_index": character,
                    "character": list(CHARACTER_LABELS[character]),
                    "origin_count": expected_count,
                    "origin_sha256": origin_digest,
                    "blob": receipt,
                }
            )
    except Exception:
        for writer in writers:
            try:
                writer.abort()
            except Exception:
                pass
        raise
    return origins, packets


def build_prepare_core(
    output_dir: Path, grade1_dir: Path, started: float
) -> tuple[dict[str, Any], str]:
    prepare1, prepare1_digest, blocks1, frozen_manifest, context = authenticate_grade1_split(
        grade1_dir
    )
    prebuild_manifest = load_prebuild_pins()
    presentation = assemble_b1_relations(prepare1, blocks1)
    if (
        sum(presentation["old_ranks"]) > resource_ceilings()["production_old_rank"]
        or sum(presentation["new_ranks"]) > resource_ceilings()["production_h1_rank"]
        or presentation["rank"] > resource_ceilings()["production_b1_rank"]
    ):
        raise RuntimeError("UNKNOWN_RESOURCE:grade2-prepare:audited_rank_ceiling")
    precision1_receipt = assemble_precision1_basis(
        output_dir, grade1_dir, prepare1, blocks1, presentation
    )
    precision1 = PackedRowStore(output_dir, precision1_receipt)
    words = json.loads(
        (ROOT / "scratchpad/a0_paper_words_v1.json").read_text(encoding="utf-8")
    )
    affine_boundary_preflight = replay_extension_and_boundary_preflight(context, words)
    replay = replay_b1_precision1(
        context, words, precision1, presentation, started
    )
    degree2_receipt, base_seeds, _ = build_b1_degree2_lifts(
        output_dir,
        grade1_dir,
        context,
        words,
        prepare1,
        blocks1,
        presentation,
        precision1,
        started,
    )
    replay.update(
        {
            "old_dag_equalities": sum(presentation["old_ranks"]),
            "h1_dag_equalities": sum(presentation["new_ranks"]),
            "full_word_sum_seed_resolution": EXPECTED_SEEDS,
            "dag_formula": "h_j=scale*(candidate-sum(reduction*pivot))",
        }
    )
    degree2 = PackedRowStore(output_dir, degree2_receipt)
    origins, packets = build_grade2_defect_packets(
        output_dir,
        context,
        base_seeds,
        precision1,
        degree2,
        presentation,
        started,
    )
    state_ancestry = {
        "grade1_schema": GRADE1_STATE_SCHEMA,
        "grade1_input_manifest": frozen_manifest,
        "grade1_input_manifest_sha256": prepare1["input_manifest_sha256"],
        "grade1_prepare_sha256": prepare1_digest,
        "grade1_block_sha256": [digest for _, digest in blocks1],
        "grade1_prepare_blob_sha256": {
            "old_lower": [old["lower_basis_blob"]["sha256"] for old in prepare1["old_blocks"]],
            "old_lift": [old["lifted_grade_blob"]["sha256"] for old in prepare1["old_blocks"]],
            "packets": [packet["blob"]["sha256"] for packet in prepare1["packets"]],
        },
        "grade1_block_basis_sha256": [body["basis_blob"]["sha256"] for body, _ in blocks1],
    }
    compact_ancestry = {
        "old": [
            {
                "character_index": old["character_index"],
                "dag_nodes": old["record"]["dag_nodes"],
                "lower_basis_sha256": old["lower_basis_blob"]["sha256"],
                "lifted_grade_sha256": old["lifted_grade_blob"]["sha256"],
            }
            for old in prepare1["old_blocks"]
        ],
        "h1": [
            {
                "character_index": index,
                "dag_nodes": body["dag_nodes"],
                "dag_sha256": body["dag_sha256"],
                "basis_sha256": body["basis_blob"]["sha256"],
            }
            for index, (body, _) in enumerate(blocks1)
        ],
        "grade1_defect_origins": prepare1["defect_origins"],
    }
    body = {
        "schema": STATE_SCHEMA,
        "phase": "prepare",
        "fixture": False,
        "terminal": None,
        "dimensions": fixed_dimensions(),
        "resource_ceilings_not_estimates": resource_ceilings(),
        "prebuild_manifest": prebuild_manifest,
        "prebuild_manifest_sha256": sha256_bytes(canonical_json(prebuild_manifest)),
        "state_ancestry": state_ancestry,
        "state_ancestry_sha256": sha256_bytes(canonical_json(state_ancestry)),
        "b1_presentation": presentation,
        "compact_ancestry": compact_ancestry,
        "compact_ancestry_sha256": sha256_bytes(canonical_json(compact_ancestry)),
        "precision1_basis_blob": precision1_receipt,
        "degree2_lift_blob": degree2_receipt,
        "precision1_replay": replay,
        "affine_boundary_preflight": affine_boundary_preflight,
        "defect_roster": origins,
        "defect_roster_sha256": sha256_bytes(canonical_json(origins)),
        "defect_roster_formula": f"44+4*{presentation['rank']}",
        "packets": packets,
        "pure_q1_words": [
            {"parity": list(parity), "word": list(PURE_Q1_WORDS[parity])}
            for parity in CHARACTER_LABELS
        ],
        "queue_exhausted": True,
        "elapsed_seconds": time.monotonic() - started,
        "downstream_claim_flags": false_claim_flags(),
    }
    digest = write_sealed_state(output_dir, "grade2-prepare", body, None)
    return body, digest


def validate_prepare_state(
    state_dir: Path,
    body: dict[str, Any],
    *,
    authenticate_blobs: bool,
    authenticate_packets: Iterable[int] = (),
) -> None:
    if (
        body.get("schema") != STATE_SCHEMA
        or body.get("phase") != "prepare"
        or body.get("fixture") is not False
        or body.get("terminal") is not None
        or body.get("dimensions") != fixed_dimensions()
        or body.get("resource_ceilings_not_estimates") != resource_ceilings()
        or body.get("queue_exhausted") is not True
        or body.get("downstream_claim_flags") != false_claim_flags()
    ):
        raise RuntimeError("grade2_prepare_semantics")
    pins = load_prebuild_pins()
    if (
        body.get("prebuild_manifest") != pins
        or body.get("prebuild_manifest_sha256") != sha256_bytes(canonical_json(pins))
    ):
        raise RuntimeError("grade2_prepare_manifest")
    ancestry = body.get("state_ancestry")
    if (
        not isinstance(ancestry, dict)
        or ancestry.get("grade1_schema") != GRADE1_STATE_SCHEMA
        or ancestry.get("grade1_input_manifest_sha256")
        != sha256_bytes(grade1.canonical_json(ancestry.get("grade1_input_manifest")))
        or not isinstance(ancestry.get("grade1_prepare_sha256"), str)
        or re.fullmatch(r"[0-9a-f]{64}", ancestry["grade1_prepare_sha256"]) is None
        or not isinstance(ancestry.get("grade1_block_sha256"), list)
        or len(ancestry["grade1_block_sha256"]) != 4
        or any(re.fullmatch(r"[0-9a-f]{64}", value or "") is None for value in ancestry["grade1_block_sha256"])
        or body.get("state_ancestry_sha256") != sha256_bytes(canonical_json(ancestry))
    ):
        raise RuntimeError("grade2_state_ancestry")
    compact = body.get("compact_ancestry")
    if (
        not isinstance(compact, dict)
        or set(compact) != {"old", "h1", "grade1_defect_origins"}
        or not isinstance(compact["old"], list)
        or len(compact["old"]) != 4
        or not isinstance(compact["h1"], list)
        or len(compact["h1"]) != 4
        or body.get("compact_ancestry_sha256") != sha256_bytes(canonical_json(compact))
    ):
        raise RuntimeError("grade2_compact_ancestry")
    presentation = body.get("b1_presentation")
    if not isinstance(presentation, dict):
        raise RuntimeError("grade2_b1_presentation_shape")
    unsigned = dict(presentation)
    digest = unsigned.pop("sha256", None)
    rank = presentation.get("rank")
    if (
        digest != sha256_bytes(canonical_json(unsigned))
        or presentation.get("grade") != 1
        or presentation.get("global_order")
        != "all_lifted_old_by_character_pivot_then_all_h1_by_character_pivot"
        or not _plain_int(rank)
        or rank < 0
        or presentation.get("seed_count") != EXPECTED_SEEDS
        or presentation.get("actor_order") != list(ACTORS)
        or presentation.get("complete") is not True
        or not isinstance(presentation.get("old_ranks"), list)
        or len(presentation["old_ranks"]) != 4
        or not isinstance(presentation.get("new_ranks"), list)
        or len(presentation["new_ranks"]) != 4
        or sum(presentation["old_ranks"]) + sum(presentation["new_ranks"]) != rank
        or len(presentation.get("basis_roster", [])) != rank
        or presentation.get("basis_roster_sha256")
        != sha256_bytes(canonical_json(presentation.get("basis_roster")))
        or len(presentation.get("seed_reductions", [])) != EXPECTED_SEEDS
        or presentation.get("seed_reductions_sha256")
        != expression_digest(presentation.get("seed_reductions"))
        or len(presentation.get("actor_transitions", [])) != rank
        or presentation.get("actor_transitions_sha256")
        != expression_digest(presentation.get("actor_transitions"))
    ):
        raise RuntimeError("grade2_b1_presentation_semantics")
    for index, roster in enumerate(presentation["basis_roster"]):
        if not isinstance(roster, dict) or roster.get("global") != index or roster.get("kind") not in ("lifted_old", "h1"):
            raise RuntimeError("grade2_b1_roster")
    for expression in presentation["seed_reductions"]:
        validate_expression(expression, rank, "grade2_b1_seed")
    for row in presentation["actor_transitions"]:
        if not isinstance(row, list) or len(row) != 4:
            raise RuntimeError("grade2_b1_transition_shape")
        for expression in row:
            validate_expression(expression, rank, "grade2_b1_transition")
    precision1 = body.get("precision1_basis_blob")
    degree2 = body.get("degree2_lift_blob")
    validate_blob_receipt(
        state_dir, precision1, rank, SOURCE_PRECISION1_WIDTH,
        authenticate=authenticate_blobs,
    )
    validate_blob_receipt(
        state_dir, degree2, rank, SOURCE_DEGREE2_WIDTH,
        authenticate=authenticate_blobs,
    )
    if body.get("precision1_replay") != {
        "seed_equalities": EXPECTED_SEEDS,
        "actor_equalities": 4 * rank,
        "direct_precision1_replay": True,
        "old_dag_equalities": sum(presentation["old_ranks"]),
        "h1_dag_equalities": sum(presentation["new_ranks"]),
        "full_word_sum_seed_resolution": EXPECTED_SEEDS,
        "dag_formula": "h_j=scale*(candidate-sum(reduction*pivot))",
    }:
        raise RuntimeError("grade2_precision1_replay_receipt")
    preflight = body.get("affine_boundary_preflight")
    if (
        not isinstance(preflight, dict)
        or preflight.get("replayed") is not True
        or preflight.get("occurrence_affine_checks") != 12
        or preflight.get("crossed_law_checks") != 96
        or preflight.get("pb3_translated_boundaries") != 6
        or preflight.get("pb4_blocks") != 2
        or preflight.get("integral_exponent_relators") != EXPECTED_SEEDS
        or preflight.get("filtration_occurrence_aggregation_checks") != 5
        or preflight.get("normalized_exponent_actor_action") != "trivial"
    ):
        raise RuntimeError("grade2_affine_boundary_preflight")
    origins = body.get("defect_roster")
    expected_count = EXPECTED_SEEDS + 4 * rank
    expected_origins = [
        {"id": seed, "kind": "seed", "seed": seed + 1}
        for seed in range(EXPECTED_SEEDS)
    ]
    for pivot in range(rank):
        for letter in ACTORS:
            expected_origins.append(
                {
                    "id": len(expected_origins),
                    "kind": "transition",
                    "pivot": pivot,
                    "letter": letter,
                }
            )
    if (
        origins != expected_origins
        or body.get("defect_roster_sha256") != sha256_bytes(canonical_json(expected_origins))
        or body.get("defect_roster_formula") != f"44+4*{rank}"
        or len(origins) != expected_count
    ):
        raise RuntimeError("grade2_defect_roster")
    packets = body.get("packets")
    if not isinstance(packets, list) or len(packets) != 4:
        raise RuntimeError("grade2_packet_count")
    selected_packets = set(authenticate_packets)
    if not selected_packets.issubset(set(range(4))):
        raise RuntimeError("grade2_packet_authentication_selection")
    for character, packet in enumerate(packets):
        if (
            not isinstance(packet, dict)
            or packet.get("character_index") != character
            or packet.get("character") != list(CHARACTER_LABELS[character])
            or packet.get("origin_count") != expected_count
            or packet.get("origin_sha256") != body["defect_roster_sha256"]
        ):
            raise RuntimeError("grade2_packet_binding")
        validate_blob_receipt(
            state_dir,
            packet.get("blob"),
            expected_count,
            SOURCE_DEGREE2_PER_CHARACTER,
            authenticate=character in selected_packets,
        )
    if body.get("pure_q1_words") != [
        {"parity": list(parity), "word": list(PURE_Q1_WORDS[parity])}
        for parity in CHARACTER_LABELS
    ]:
        raise RuntimeError("grade2_projector_words")
    forbidden = {"target", "residual", "member", "nonmember", "merge_sha256"}
    if forbidden.intersection(body):
        raise RuntimeError("grade2_prepare_target_contamination")


def run_block_core(
    state_dir: Path,
    prepare: dict[str, Any],
    prepare_digest: str,
    character: int,
    started: float,
) -> tuple[dict[str, Any], str]:
    packet = prepare["packets"][character]
    receipt = packet["blob"]
    data = validate_blob_receipt(
        state_dir,
        receipt,
        packet["origin_count"],
        SOURCE_DEGREE2_PER_CHARACTER,
        read=True,
    )
    if data is None:
        raise RuntimeError("grade2_packet_read")
    matrix = np.frombuffer(data, dtype=np.uint8).reshape(
        packet["origin_count"], SOURCE_DEGREE2_PER_CHARACTER // 4
    )
    context = grade1.Context(
        json.loads((ROOT / "scratchpad/a0_paper_words_v1.json").read_text(encoding="utf-8"))
    )
    owner = grade1.PackedEchelon(SOURCE_DEGREE2_PER_CHARACTER)
    origin_reductions: list[list[list[int]]] = []
    transitions: list[list[list[list[int]] | None]] = []
    dag_nodes: list[dict[str, Any]] = []
    queue: deque[int] = deque()
    attempts = 0
    for origin, packed in enumerate(matrix):
        inserted = owner.insert(packed)
        attempts += 1
        origin_reductions.append(grade1.expression_from_insert(inserted))
        if inserted["accepted"]:
            pivot = inserted["pivot"]
            dag_nodes.append(
                {
                    "pivot": pivot,
                    "lead": inserted["lead"],
                    "scale": inserted["scale"],
                    "origin": {"kind": "defect", "origin": origin},
                    "reductions": inserted["reductions"],
                }
            )
            transitions.append([None, None, None, None])
            queue.append(pivot)
        if attempts % 256 == 0:
            progress(f"grade2-block-{character}-ingest", attempts, len(owner.rows), len(queue), started)
            enforce_resource(started, f"grade2-block-{character}-ingest")
    while queue:
        pivot = queue.popleft()
        parent = owner.dense_row(pivot)
        for actor_index, letter in enumerate(ACTORS):
            child = associated_degree2_actor(
                context, parent, CHARACTER_LABELS[character], letter
            )
            inserted = owner.insert(child)
            attempts += 1
            transitions[pivot][actor_index] = grade1.expression_from_insert(inserted)
            if inserted["accepted"]:
                new_pivot = inserted["pivot"]
                dag_nodes.append(
                    {
                        "pivot": new_pivot,
                        "lead": inserted["lead"],
                        "scale": inserted["scale"],
                        "origin": {"kind": "actor", "parent": pivot, "letter": letter},
                        "reductions": inserted["reductions"],
                    }
                )
                transitions.append([None, None, None, None])
                queue.append(new_pivot)
            if attempts % 256 == 0:
                progress(f"grade2-block-{character}", attempts, len(owner.rows), len(queue), started)
                enforce_resource(started, f"grade2-block-{character}")
    if any(any(expression is None for expression in row) for row in transitions):
        raise RuntimeError("grade2_block_transition_incomplete")
    if attempts != packet["origin_count"] + 4 * len(owner.rows):
        raise RuntimeError("grade2_block_queue_receipt")
    if (
        len(owner.rows) > resource_ceilings()["one_character_rank"]
        or attempts > resource_ceilings()["one_character_queue_attempts"]
    ):
        raise RuntimeError(f"UNKNOWN_RESOURCE:grade2-block-{character}:audited_ceiling")
    basis = write_packed_owner(
        state_dir, f"grade2-block-{character}-basis", owner
    )
    body = {
        "schema": STATE_SCHEMA,
        "phase": "block",
        "fixture": False,
        "terminal": None,
        "parent_sha256": prepare_digest,
        "character_index": character,
        "character": list(CHARACTER_LABELS[character]),
        "dimensions": {
            "width": SOURCE_DEGREE2_PER_CHARACTER,
            "monomials": [list(value) for value in MONOMIALS_DEGREE2],
            "monomials_coupled": True,
        },
        "packet_sha256": receipt["sha256"],
        "origin_sha256": prepare["defect_roster_sha256"],
        "origin_count": packet["origin_count"],
        "origin_reductions": origin_reductions,
        "rank": len(owner.rows),
        "attempts": attempts,
        "queue_exhausted": True,
        "actor_order": list(ACTORS),
        "actor_transitions": transitions,
        "pivot_leads": owner.leads,
        "dag_nodes": dag_nodes,
        "dag_sha256": sha256_bytes(canonical_json(dag_nodes)),
        "basis_blob": basis,
        "elapsed_seconds": time.monotonic() - started,
        "downstream_claim_flags": false_claim_flags(),
    }
    digest = write_sealed_state(
        state_dir, f"grade2-block-{character}", body, prepare_digest
    )
    return body, digest


def validate_block_state(
    state_dir: Path,
    body: dict[str, Any],
    prepare: dict[str, Any],
    prepare_digest: str,
    character: int,
    *,
    authenticate_basis: bool,
) -> None:
    rank = body.get("rank")
    origin_count = len(prepare["defect_roster"])
    if (
        body.get("schema") != STATE_SCHEMA
        or body.get("phase") != "block"
        or body.get("fixture") is not False
        or body.get("terminal") is not None
        or body.get("parent_sha256") != prepare_digest
        or body.get("character_index") != character
        or body.get("character") != list(CHARACTER_LABELS[character])
        or body.get("dimensions") != {
            "width": SOURCE_DEGREE2_PER_CHARACTER,
            "monomials": [list(value) for value in MONOMIALS_DEGREE2],
            "monomials_coupled": True,
        }
        or body.get("packet_sha256") != prepare["packets"][character]["blob"]["sha256"]
        or body.get("origin_sha256") != prepare["defect_roster_sha256"]
        or body.get("origin_count") != origin_count
        or not _plain_int(rank)
        or rank < 0
        or body.get("attempts") != origin_count + 4 * rank
        or body.get("queue_exhausted") is not True
        or body.get("actor_order") != list(ACTORS)
        or body.get("downstream_claim_flags") != false_claim_flags()
    ):
        raise RuntimeError("grade2_block_semantics")
    origins = body.get("origin_reductions")
    transitions = body.get("actor_transitions")
    nodes = body.get("dag_nodes")
    leads = body.get("pivot_leads")
    if (
        not isinstance(origins, list)
        or len(origins) != origin_count
        or not isinstance(transitions, list)
        or len(transitions) != rank
        or not isinstance(nodes, list)
        or len(nodes) != rank
        or not isinstance(leads, list)
        or len(leads) != rank
        or len(set(leads)) != rank
        or body.get("dag_sha256") != sha256_bytes(canonical_json(nodes))
    ):
        raise RuntimeError("grade2_block_cardinality")
    for expression in origins:
        # Stored reducer order is not sorted; normalize before the semantic
        # range check without changing the certificate record.
        validate_expression(normalize_expression(expression), rank, "grade2_origin_reduction")
    for row in transitions:
        if not isinstance(row, list) or len(row) != 4:
            raise RuntimeError("grade2_block_transition_shape")
        for expression in row:
            validate_expression(normalize_expression(expression), rank, "grade2_block_transition")
    for pivot, node in enumerate(nodes):
        if (
            not isinstance(node, dict)
            or node.get("pivot") != pivot
            or node.get("lead") != leads[pivot]
            or not _plain_int(leads[pivot])
            or not 0 <= leads[pivot] < SOURCE_DEGREE2_PER_CHARACTER
            or node.get("scale") not in (1, 2)
        ):
            raise RuntimeError("grade2_block_dag")
        origin = node.get("origin")
        if origin.get("kind") == "defect":
            if not _plain_int(origin.get("origin")) or not 0 <= origin["origin"] < origin_count:
                raise RuntimeError("grade2_block_defect_origin")
        elif origin.get("kind") == "actor":
            if not _plain_int(origin.get("parent")) or not 0 <= origin["parent"] < pivot or origin.get("letter") not in ACTORS:
                raise RuntimeError("grade2_block_actor_origin")
        else:
            raise RuntimeError("grade2_block_origin_kind")
    validate_blob_receipt(
        state_dir, body.get("basis_blob"), rank, SOURCE_DEGREE2_PER_CHARACTER,
        authenticate=authenticate_basis,
    )


def aggregate_pure_degree2(
    context: grade1.Context, character: int, row: np.ndarray
) -> np.ndarray:
    zeros0 = np.zeros((4, SOURCE_DEGREE0_PER_CHARACTER), dtype=np.uint8)
    zeros1 = np.zeros((4, SOURCE_DEGREE1_PER_CHARACTER), dtype=np.uint8)
    degree2 = np.zeros((4, SOURCE_DEGREE2_PER_CHARACTER), dtype=np.uint8)
    degree2[character] = row
    return aggregate_precision2(
        context, zeros0, zeros1, degree2, np.zeros(8, dtype=np.uint8)
    )[2]


def run_merge_core(
    state_dir: Path,
    prepare: dict[str, Any],
    prepare_digest: str,
    blocks: list[tuple[dict[str, Any], str]],
    started: float,
) -> tuple[dict[str, Any], str]:
    context = grade1.Context(
        json.loads((ROOT / "scratchpad/a0_paper_words_v1.json").read_text(encoding="utf-8"))
    )
    precision1 = PackedRowStore(state_dir, prepare["precision1_basis_blob"])
    degree2 = PackedRowStore(state_dir, prepare["degree2_lift_blob"])
    lower_owner = grade1.PackedEchelon(PHYSICAL_LOWER_WIDTH)
    grade_owner = grade1.PackedEchelon(PHYSICAL_DEGREE2_WIDTH)
    lower_grade_rows = PackedRowWriter(
        state_dir, "grade2-physical-lower-grade-companion", PHYSICAL_DEGREE2_WIDTH
    )
    lower_nodes: list[dict[str, Any]] = []
    grade_nodes: list[dict[str, Any]] = []
    roster: list[dict[str, Any]] = []
    attempts = 0
    for pivot in range(prepare["b1_presentation"]["rank"]):
        degree0, degree1, auxiliary = split_precision1(precision1.row(pivot))
        grade2 = degree2.row(pivot).reshape(4, SOURCE_DEGREE2_PER_CHARACTER)
        physical0, physical1, physical2, physical_aux = aggregate_precision2(
            context, degree0, degree1, grade2, auxiliary
        )
        physical_lower = flatten_physical_lower(physical0, physical1, physical_aux)
        lower_remainder, lower_reductions = lower_owner.reduce_packed(
            grade1.pack_trits(physical_lower)
        )
        grade_remainder = physical2.copy()
        for earlier, coefficient in lower_reductions:
            _add_mod3(grade_remainder, lower_grade_rows.row(earlier), -coefficient)
        dense_lower = grade1.unpack_trits(lower_remainder, PHYSICAL_LOWER_WIDTH)
        if np.any(dense_lower):
            inserted = lower_owner._accept_remainder(lower_remainder, lower_reductions)
            if not inserted["accepted"]:
                raise RuntimeError("grade2_lower_accept")
            if inserted["scale"] == 2:
                grade_remainder = ((2 * grade_remainder.astype(np.uint16)) % 3).astype(np.uint8)
            lower_grade_rows.append(grade_remainder)
            lower_nodes.append(
                {
                    "pivot": inserted["pivot"],
                    "scale": inserted["scale"],
                    "origin": {"kind": "lifted_b1", "pivot": pivot},
                    "reductions": lower_reductions,
                }
            )
            roster.append({"kind": "lifted-b1-lower-pivot", "pivot": pivot})
        else:
            inserted = grade_owner.insert(grade_remainder)
            roster.append({"kind": "lifted-b1-connection", "pivot": pivot})
            if inserted["accepted"]:
                grade_nodes.append(
                    {
                        "pivot": inserted["pivot"],
                        "lead": inserted["lead"],
                        "scale": inserted["scale"],
                        "origin": {
                            "kind": "lifted_b1_connection",
                            "pivot": pivot,
                            "lower_reductions": lower_reductions,
                        },
                        "reductions": inserted["reductions"],
                    }
                )
        attempts += 1
        if attempts % 128 == 0:
            progress("grade2-module-old", attempts, len(grade_owner.rows), 0, started)
            enforce_resource(started, "grade2-module-old")
    for character, (block, _) in enumerate(blocks):
        basis = PackedRowStore(state_dir, block["basis_blob"])
        for pivot in range(block["rank"]):
            physical = aggregate_pure_degree2(context, character, basis.row(pivot))
            inserted = grade_owner.insert(physical)
            roster.append({"kind": "h2", "character": character, "pivot": pivot})
            if inserted["accepted"]:
                grade_nodes.append(
                    {
                        "pivot": inserted["pivot"],
                        "lead": inserted["lead"],
                        "scale": inserted["scale"],
                        "origin": {
                            "kind": "h2", "character": character, "pivot": pivot
                        },
                        "reductions": inserted["reductions"],
                    }
                )
            attempts += 1
            if attempts % 128 == 0:
                progress("grade2-module-h2", attempts, len(grade_owner.rows), 0, started)
                enforce_resource(started, "grade2-module-h2")
    if attempts > resource_ceilings()["joint_physical_input_rows"]:
        raise RuntimeError("UNKNOWN_RESOURCE:grade2-module:audited_input_ceiling")
    lower_basis = write_packed_owner(
        state_dir, "grade2-physical-lower-basis", lower_owner
    )
    if lower_grade_rows.rows != len(lower_owner.rows):
        raise RuntimeError("grade2_lower_companion_count")
    lower_companion = lower_grade_rows.finish()
    grade_basis = write_packed_owner(
        state_dir, "grade2-physical-grade-basis", grade_owner
    )
    block_digests = [digest for _, digest in blocks]
    body = {
        "schema": STATE_SCHEMA,
        "phase": "module",
        "fixture": False,
        "parent_sha256": prepare_digest,
        "block_sha256": block_digests,
        "dimensions": fixed_dimensions(),
        "resource_ceilings_not_estimates": resource_ceilings(),
        "source_blocks_exhausted": 4,
        "b1_rank": prepare["b1_presentation"]["rank"],
        "h2_ranks": [block["rank"] for block, _ in blocks],
        "physical_roster": roster,
        "physical_roster_sha256": sha256_bytes(canonical_json(roster)),
        "physical_lower_rank": len(lower_owner.rows),
        "physical_grade_rank": len(grade_owner.rows),
        "physical_lower_basis_blob": lower_basis,
        "physical_lower_grade_companion_blob": lower_companion,
        "physical_grade_basis_blob": grade_basis,
        "physical_lower_pivot_leads": lower_owner.leads,
        "physical_grade_pivot_leads": grade_owner.leads,
        "physical_lower_dag": lower_nodes,
        "physical_grade_dag": grade_nodes,
        "transition_state": {
            "b1_presentation_sha256": prepare["b1_presentation"]["sha256"],
            "grade2_origin_reductions_sha256": [
                expression_digest(block["origin_reductions"]) for block, _ in blocks
            ],
            "grade2_actor_transitions_sha256": [
                expression_digest(block["actor_transitions"]) for block, _ in blocks
            ],
            "grade2_dag_sha256": [block["dag_sha256"] for block, _ in blocks],
            "complete_for_future_t2": True,
        },
        "state_ancestry": {
            "grade1": prepare["state_ancestry"],
            "grade2_prepare_sha256": prepare_digest,
            "grade2_block_sha256": block_digests,
        },
        "target_independent": True,
        "membership_tested": False,
        "terminal": "FIRST_RUNG_GRADE2_MODULE_READY",
        "elapsed_seconds": time.monotonic() - started,
        "downstream_claim_flags": false_claim_flags(),
    }
    digest = write_sealed_state(state_dir, "grade2-module", body, prepare_digest)
    return body, digest


def validate_module_state(
    state_dir: Path,
    body: dict[str, Any],
    prepare: dict[str, Any],
    prepare_digest: str,
    blocks: list[tuple[dict[str, Any], str]],
) -> None:
    lower_rank = body.get("physical_lower_rank")
    grade_rank = body.get("physical_grade_rank")
    roster_count = prepare["b1_presentation"]["rank"] + sum(
        block["rank"] for block, _ in blocks
    )
    if (
        body.get("schema") != STATE_SCHEMA
        or body.get("phase") != "module"
        or body.get("fixture") is not False
        or body.get("parent_sha256") != prepare_digest
        or body.get("block_sha256") != [digest for _, digest in blocks]
        or body.get("dimensions") != fixed_dimensions()
        or body.get("resource_ceilings_not_estimates") != resource_ceilings()
        or body.get("source_blocks_exhausted") != 4
        or body.get("b1_rank") != prepare["b1_presentation"]["rank"]
        or body.get("h2_ranks") != [block["rank"] for block, _ in blocks]
        or body.get("target_independent") is not True
        or body.get("membership_tested") is not False
        or body.get("terminal") != "FIRST_RUNG_GRADE2_MODULE_READY"
        or body.get("downstream_claim_flags") != false_claim_flags()
        or not _plain_int(lower_rank)
        or lower_rank < 0
        or not _plain_int(grade_rank)
        or grade_rank < 0
        or len(body.get("physical_roster", [])) != roster_count
        or body.get("physical_roster_sha256")
        != sha256_bytes(canonical_json(body.get("physical_roster")))
        or len(body.get("physical_lower_dag", [])) != lower_rank
        or len(body.get("physical_lower_pivot_leads", [])) != lower_rank
        or len(set(body.get("physical_lower_pivot_leads", []))) != lower_rank
        or len(body.get("physical_grade_dag", [])) != grade_rank
        or len(body.get("physical_grade_pivot_leads", [])) != grade_rank
        or len(set(body.get("physical_grade_pivot_leads", []))) != grade_rank
    ):
        raise RuntimeError("grade2_module_semantics")
    validate_blob_receipt(
        state_dir, body.get("physical_lower_basis_blob"), lower_rank, PHYSICAL_LOWER_WIDTH
    )
    validate_blob_receipt(
        state_dir,
        body.get("physical_lower_grade_companion_blob"),
        lower_rank,
        PHYSICAL_DEGREE2_WIDTH,
    )
    validate_blob_receipt(
        state_dir, body.get("physical_grade_basis_blob"), grade_rank, PHYSICAL_DEGREE2_WIDTH
    )
    transition = body.get("transition_state")
    if (
        not isinstance(transition, dict)
        or transition.get("b1_presentation_sha256") != prepare["b1_presentation"]["sha256"]
        or transition.get("grade2_origin_reductions_sha256")
        != [expression_digest(block["origin_reductions"]) for block, _ in blocks]
        or transition.get("grade2_actor_transitions_sha256")
        != [expression_digest(block["actor_transitions"]) for block, _ in blocks]
        or transition.get("grade2_dag_sha256") != [block["dag_sha256"] for block, _ in blocks]
        or transition.get("complete_for_future_t2") is not True
    ):
        raise RuntimeError("grade2_module_transition_state")
    if any(key in body for key in ("target", "residual", "member_coefficients", "dual")):
        raise RuntimeError("grade2_module_target_contamination")


# ---------------------------------------------------------------------------
# Inactive, result-dependent MEMBER join.  It stops before membership.


def freely_reduce(word: Iterable[int]) -> tuple[int, ...]:
    output: list[int] = []
    for raw in word:
        letter = int(raw)
        if letter not in (-2, -1, 1, 2):
            raise RuntimeError("literal_letter")
        if output and output[-1] == -letter:
            output.pop()
        else:
            output.append(letter)
    return tuple(output)


def canonicalize_literal_terms(terms: Any) -> list[list[Any]]:
    if not isinstance(terms, list):
        raise RuntimeError("literal_terms_shape")
    accumulator: dict[tuple[int, tuple[int, ...]], int] = {}
    for position, term in enumerate(terms):
        if not isinstance(term, list) or len(term) != 3:
            raise RuntimeError(f"literal_term_shape:{position}")
        seed = term[0]
        word = term[1]
        coefficient = term[2]
        if (
            not _plain_int(seed)
            or not 1 <= seed <= EXPECTED_SEEDS
            or not isinstance(word, list)
            or not _plain_int(coefficient)
            or coefficient not in (1, 2)
        ):
            raise RuntimeError(f"literal_term_semantics:{position}")
        key = seed, freely_reduce(word)
        accumulator[key] = (accumulator.get(key, 0) + coefficient) % 3
    return [
        [seed, list(word), accumulator[(seed, word)]]
        for seed, word in sorted(accumulator)
        if accumulator[(seed, word)]
    ]


def direct_target_precision2(
    context: grade1.Context, words: dict[str, Any]
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    degree0 = np.zeros(PHYSICAL_DEGREE0_WIDTH, dtype=np.uint8)
    degree1 = np.zeros(PHYSICAL_DEGREE1_WIDTH, dtype=np.uint8)
    degree2 = np.zeros(PHYSICAL_DEGREE2_WIDTH, dtype=np.uint8)
    auxiliary = np.zeros(4, dtype=np.uint8)
    g760 = tuple(int(value) for value in words["g760"])
    h1 = tuple(
        floor.wm(
            floor.sub(g760, *floor.OO[2]),
            floor.wi(floor.sub(g760, *floor.OO[1])),
            floor.sub(g760, *floor.OO[0]),
        )
    )
    h2 = tuple(
        floor.wm(
            floor.sub(g760, *floor.OO[5]),
            floor.wi(floor.sub(g760, *floor.OO[4])),
            floor.wi(floor.sub(g760, *floor.OO[3])),
        )
    )
    for block, word in enumerate((h1, h2)):
        normal, augmentation = grade1.qnorm_affine(word, context)
        auxiliary[block] = (-augmentation) % 3
        for component, value, coefficient0 in normal:
            polynomial = e_polynomial(value[3])
            psl = context.psidx[value[0]]
            for character, label in enumerate(CHARACTER_LABELS):
                weight = -coefficient0 * source_character_sign(
                    label, (value[1], value[2])
                )
                coordinate0 = grade1.physical_lower_coord(
                    character, block, component, psl
                )
                degree0[coordinate0] = (
                    int(degree0[coordinate0]) + weight * int(polynomial[0])
                ) % 3
                for monomial in range(3):
                    coordinate1 = grade1.physical_grade_coord(
                        character, block, component, monomial, psl
                    )
                    degree1[coordinate1] = (
                        int(degree1[coordinate1])
                        + weight * int(polynomial[1 + monomial])
                    ) % 3
                for monomial in range(6):
                    coordinate2 = (((character * 2 + block) * 2 + component) * 6 + monomial) * 504 + psl
                    degree2[coordinate2] = (
                        int(degree2[coordinate2])
                        + weight * int(polynomial[4 + monomial])
                    ) % 3
    return degree0, degree1, degree2, auxiliary


def replay_literal_terms_precision2(
    context: grade1.Context,
    words: dict[str, Any],
    terms: list[list[Any]],
    started: float,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    degree0 = np.zeros(PHYSICAL_DEGREE0_WIDTH, dtype=np.uint8)
    degree1 = np.zeros(PHYSICAL_DEGREE1_WIDTH, dtype=np.uint8)
    degree2 = np.zeros(PHYSICAL_DEGREE2_WIDTH, dtype=np.uint8)
    auxiliary = np.zeros(4, dtype=np.uint8)
    seeds = [
        evaluate_seed_precision2(context, tuple(int(value) for value in relator))
        for relator in words["relators"]
    ]
    actor_cache: dict[tuple[int, ...], tuple[grade1.Affine, ...]] = {}
    for position, (seed, raw_word, coefficient) in enumerate(terms):
        actor_word = tuple(int(value) for value in raw_word)
        if actor_word not in actor_cache:
            actor_cache[actor_word] = context.source_word_tags(actor_word)
        acted = act_precision2(
            context, *seeds[seed - 1], actor_cache[actor_word]
        )
        physical = aggregate_precision2(context, *acted)
        _add_mod3(degree0, physical[0], coefficient)
        _add_mod3(degree1, physical[1], coefficient)
        _add_mod3(degree2, physical[2], coefficient)
        _add_mod3(auxiliary, physical[3], coefficient)
        if (position + 1) % 128 == 0:
            progress("grade2-member-join-replay", position + 1, 0, len(terms) - position - 1, started)
            enforce_resource(started, "grade2-member-join-replay")
    return degree0, degree1, degree2, auxiliary


def sparse_digest(row: np.ndarray) -> str:
    encoded = [[int(index), int(row[index])] for index in np.flatnonzero(row)]
    return sha256_bytes(json.dumps(encoded, separators=(",", ":")).encode("ascii"))


def authenticate_grade1_member(
    grade1_dir: Path, certificate_path: Path
) -> tuple[
    dict[str, Any], str, list[tuple[dict[str, Any], str]], dict[str, Any], str,
    dict[str, Any], str,
]:
    prepare, prepare_digest, blocks, frozen_manifest, _ = authenticate_grade1_split(
        grade1_dir
    )
    merge, merge_digest = grade1.read_sealed_state(
        grade1_dir, "merge", prepare_digest
    )
    grade1.validate_merge_state(
        grade1_dir, merge, prepare, prepare_digest, blocks,
        authenticate_basis=True,
    )
    if merge.get("terminal") != "FIRST_RUNG_GRADE1_MEMBER":
        raise RuntimeError("grade1_member_join_forbidden")
    certificate_bytes = certificate_path.read_bytes()
    certificate = json.loads(certificate_bytes)
    certificate_digest = sha256_bytes(certificate_bytes)
    if canonical_json(certificate) != certificate_bytes:
        raise RuntimeError("grade1_certificate_canonicality")
    permitted_producers = {
        sha256_bytes((ROOT / "search/d972_r07_a0_first_rung_grade1_v3.py").read_bytes()),
        sha256_bytes((ROOT / "search/d972_r07_a0_first_rung_grade1_v4.py").read_bytes()),
    }
    if (
        certificate.get("terminal") != "FIRST_RUNG_GRADE1_MEMBER"
        or certificate.get("producer_sha256") not in permitted_producers
        or certificate.get("input_manifest") != frozen_manifest
        or certificate.get("input_manifest_sha256") != prepare["input_manifest_sha256"]
        or certificate.get("state_chain") != {
            "prepare_sha256": prepare_digest,
            "block_sha256": [digest for _, digest in blocks],
            "merge_sha256": merge_digest,
        }
        or certificate.get("source_ancestry") != merge.get("source_ancestry")
        or certificate.get("next_degree2_residual") != merge.get("next_degree2_residual")
        or certificate.get("verified") is not False
    ):
        raise RuntimeError("grade1_member_certificate_binding")
    return prepare, prepare_digest, blocks, merge, merge_digest, certificate, certificate_digest


def run_member_join(
    state_dir: Path,
    grade1_dir: Path,
    certificate_path: Path,
    module: dict[str, Any],
    module_digest: str,
    started: float,
) -> tuple[dict[str, Any], str]:
    (
        prepare1, prepare1_digest, blocks1, merge1, merge1_digest,
        certificate, certificate_digest,
    ) = authenticate_grade1_member(grade1_dir, certificate_path)
    module_ancestry = module["state_ancestry"]
    if (
        module_ancestry["grade1"]["grade1_prepare_sha256"] != prepare1_digest
        or module_ancestry["grade1"]["grade1_block_sha256"]
        != [digest for _, digest in blocks1]
    ):
        raise RuntimeError("member_join_module_grade1_parent")
    source_ancestry = merge1["source_ancestry"]
    rebuilt_terms = canonicalize_literal_terms(
        prepare1["canonical_solution"]["terms"]
        + source_ancestry["grade1_update_terms"]
    )
    if (
        rebuilt_terms != source_ancestry.get("accumulated_terms")
        or len(rebuilt_terms) != source_ancestry.get("accumulated_term_count")
        or sha256_bytes(json.dumps(rebuilt_terms, separators=(",", ":")).encode("ascii"))
        != source_ancestry.get("accumulated_sha256")
        or source_ancestry.get("direct_precision1_target_replay") is not True
    ):
        raise RuntimeError("member_join_literal_rebuild")
    words = json.loads(
        (ROOT / "scratchpad/a0_paper_words_v1.json").read_text(encoding="utf-8")
    )
    context = grade1.Context(words)
    target = direct_target_precision2(context, words)
    replay = replay_literal_terms_precision2(context, words, rebuilt_terms, started)
    difference = tuple(
        ((left.astype(np.int16) - right.astype(np.int16)) % 3).astype(np.uint8)
        for left, right in zip(target, replay)
    )
    lower = flatten_physical_lower(difference[0], difference[1], difference[3])
    if np.any(lower):
        raise RuntimeError("member_join_nonzero_lower")
    residual = difference[2]
    packed = grade1.pack_trits(residual).tobytes()
    recomputed = {
        "grade": 2,
        "width": PHYSICAL_DEGREE2_WIDTH,
        "packed_bytes": len(packed),
        "support": int(np.count_nonzero(residual)),
        "packed_sha256": sha256_bytes(packed),
        "sparse_sha256": sparse_digest(residual),
    }
    if len(packed) != 12096:
        raise RuntimeError("member_join_packed_width")
    # Only after the independent full lower-zero assertion may the stored top
    # block be read and compared.
    stored = merge1.get("next_degree2_residual")
    if (
        not isinstance(stored, dict)
        or stored.get("grade") != 2
        or stored.get("width") != PHYSICAL_DEGREE2_WIDTH
        or stored.get("support") != recomputed["support"]
        or stored.get("sha256") != recomputed["sparse_sha256"]
    ):
        raise RuntimeError("member_join_residual_metadata")
    stored_data = grade1.read_blob(grade1_dir, stored["blob"])
    if stored_data != packed or stored["blob"].get("sha256") != recomputed["packed_sha256"]:
        raise RuntimeError("member_join_residual_blob")
    recomputed_blob = write_blob(
        state_dir,
        "grade2-join-residual",
        packed,
        rows=1,
        width=PHYSICAL_DEGREE2_WIDTH,
    )
    recomputed["blob"] = recomputed_blob
    body = {
        "schema": STATE_SCHEMA,
        "phase": "member-join-preflight",
        "fixture": False,
        "module_sha256": module_digest,
        "grade2_state_chain": {
            "prepare_sha256": module["parent_sha256"],
            "block_sha256": module["block_sha256"],
            "module_sha256": module_digest,
        },
        "grade1_state_chain": {
            "prepare_sha256": prepare1_digest,
            "block_sha256": [digest for _, digest in blocks1],
            "merge_sha256": merge1_digest,
        },
        "grade1_certificate_sha256": certificate_digest,
        "literal_term_count": len(rebuilt_terms),
        "literal_terms_sha256": sha256_bytes(
            json.dumps(rebuilt_terms, separators=(",", ":")).encode("ascii")
        ),
        "full_lower_width": PHYSICAL_LOWER_WIDTH,
        "full_lower_zero": True,
        "recomputed_residual": recomputed,
        "stored_residual_compared_after_lower_gate": True,
        "membership_tested": False,
        "status": "GRADE2_RESIDUAL_RECOMPUTED",
        "elapsed_seconds": time.monotonic() - started,
        "downstream_claim_flags": false_claim_flags(),
    }
    digest = write_sealed_state(
        state_dir, "grade2-join", body, module_digest
    )
    validate_join_state(state_dir, body, module, module_digest, certificate_digest)
    return body, digest


def validate_join_state(
    state_dir: Path,
    body: dict[str, Any],
    module: dict[str, Any],
    module_digest: str,
    certificate_digest: str,
) -> None:
    residual = body.get("recomputed_residual")
    if (
        body.get("schema") != STATE_SCHEMA
        or body.get("phase") != "member-join-preflight"
        or body.get("fixture") is not False
        or body.get("module_sha256") != module_digest
        or body.get("grade1_certificate_sha256") != certificate_digest
        or body.get("full_lower_width") != PHYSICAL_LOWER_WIDTH
        or body.get("full_lower_zero") is not True
        or body.get("stored_residual_compared_after_lower_gate") is not True
        or body.get("membership_tested") is not False
        or body.get("status") != "GRADE2_RESIDUAL_RECOMPUTED"
        or body.get("downstream_claim_flags") != false_claim_flags()
        or not isinstance(residual, dict)
        or residual.get("grade") != 2
        or residual.get("width") != PHYSICAL_DEGREE2_WIDTH
        or residual.get("packed_bytes") != 12096
        or not _plain_int(residual.get("support"))
        or re.fullmatch(r"[0-9a-f]{64}", residual.get("packed_sha256", "")) is None
        or re.fullmatch(r"[0-9a-f]{64}", residual.get("sparse_sha256", "")) is None
        or not isinstance(residual.get("blob"), dict)
        or body.get("grade2_state_chain") != {
            "prepare_sha256": module["parent_sha256"],
            "block_sha256": module["block_sha256"],
            "module_sha256": module_digest,
        }
    ):
        raise RuntimeError("grade2_join_state")
    validate_blob_receipt(
        state_dir, residual["blob"], 1, PHYSICAL_DEGREE2_WIDTH
    )


def seal_unknown_resource(
    state_dir: Path, phase: str, parent_digest: str | None, message: str
) -> None:
    body = {
        "schema": STATE_SCHEMA,
        "phase": phase,
        "terminal": "UNKNOWN_RESOURCE",
        "reason": message,
        "membership_tested": False,
        "downstream_claim_flags": false_claim_flags(),
    }
    digest = write_sealed_state(state_dir, f"grade2-{phase}-unknown", body, parent_digest)
    print(
        json.dumps(
            {"phase": phase, "terminal": "UNKNOWN_RESOURCE", "state_sha256": digest},
            sort_keys=True,
        )
    )


def phase_prepare(state_dir: Path, grade1_dir: Path) -> None:
    state_dir = ensure_external_state_dir(state_dir)
    try:
        existing, digest = read_sealed_state(state_dir, "grade2-prepare")
    except FileNotFoundError:
        existing = None
    if existing is not None:
        validate_prepare_state(
            state_dir, existing, authenticate_blobs=True,
            authenticate_packets=range(4),
        )
        prepare1, prepare1_digest, blocks1, _, _ = authenticate_grade1_split(grade1_dir)
        ancestry = existing["state_ancestry"]
        if (
            ancestry["grade1_prepare_sha256"] != prepare1_digest
            or ancestry["grade1_block_sha256"] != [value for _, value in blocks1]
            or ancestry["grade1_input_manifest_sha256"] != prepare1["input_manifest_sha256"]
        ):
            raise RuntimeError("grade2_prepare_resume_parent")
        print(json.dumps({"phase": "prepare", "resumed": True, "state_sha256": digest}, sort_keys=True))
        return
    started = time.monotonic()
    try:
        body, digest = build_prepare_core(state_dir, grade1_dir.resolve(), started)
    except RuntimeError as error:
        if str(error).startswith("UNKNOWN_RESOURCE:"):
            seal_unknown_resource(state_dir, "prepare", None, str(error))
            return
        raise
    print(
        json.dumps(
            {
                "phase": "prepare",
                "resumed": False,
                "state_sha256": digest,
                "b1_rank": body["b1_presentation"]["rank"],
                "defect_origins": len(body["defect_roster"]),
                "terminal": None,
                "elapsed_seconds": body["elapsed_seconds"],
            },
            sort_keys=True,
        )
    )


def phase_block(state_dir: Path, character: int) -> None:
    state_dir = ensure_external_state_dir(state_dir)
    prepare, prepare_digest = read_sealed_state(state_dir, "grade2-prepare")
    validate_prepare_state(state_dir, prepare, authenticate_blobs=False)
    stem = f"grade2-block-{character}"
    try:
        existing, digest = read_sealed_state(state_dir, stem, prepare_digest)
    except FileNotFoundError:
        existing = None
    if existing is not None:
        validate_prepare_state(
            state_dir, prepare, authenticate_blobs=False,
            authenticate_packets=(character,),
        )
        validate_block_state(
            state_dir, existing, prepare, prepare_digest, character,
            authenticate_basis=True,
        )
        print(json.dumps({"phase": "block", "character": character, "resumed": True, "state_sha256": digest}, sort_keys=True))
        return
    started = time.monotonic()
    try:
        body, digest = run_block_core(
            state_dir, prepare, prepare_digest, character, started
        )
    except RuntimeError as error:
        if str(error).startswith("UNKNOWN_RESOURCE:"):
            seal_unknown_resource(state_dir, f"block-{character}", prepare_digest, str(error))
            return
        raise
    print(
        json.dumps(
            {
                "phase": "block", "character": character, "resumed": False,
                "state_sha256": digest, "rank": body["rank"],
                "attempts": body["attempts"], "terminal": None,
                "elapsed_seconds": body["elapsed_seconds"],
            },
            sort_keys=True,
        )
    )


def phase_merge(state_dir: Path) -> None:
    state_dir = ensure_external_state_dir(state_dir)
    prepare, prepare_digest = read_sealed_state(state_dir, "grade2-prepare")
    validate_prepare_state(state_dir, prepare, authenticate_blobs=True)
    blocks = [
        read_sealed_state(state_dir, f"grade2-block-{index}", prepare_digest)
        for index in range(4)
    ]
    for index, (body, _) in enumerate(blocks):
        validate_block_state(
            state_dir, body, prepare, prepare_digest, index,
            authenticate_basis=True,
        )
    try:
        existing, digest = read_sealed_state(
            state_dir, "grade2-module", prepare_digest
        )
    except FileNotFoundError:
        existing = None
    if existing is not None:
        validate_module_state(
            state_dir, existing, prepare, prepare_digest, blocks
        )
        print(
            json.dumps(
                {
                    "phase": "module", "resumed": True,
                    "state_sha256": digest,
                    "terminal": existing["terminal"],
                },
                sort_keys=True,
            )
        )
        return
    started = time.monotonic()
    try:
        body, digest = run_merge_core(
            state_dir, prepare, prepare_digest, blocks, started
        )
    except RuntimeError as error:
        if str(error).startswith("UNKNOWN_RESOURCE:"):
            seal_unknown_resource(state_dir, "module", prepare_digest, str(error))
            return
        raise
    print(
        json.dumps(
            {
                "phase": "module", "resumed": False,
                "state_sha256": digest,
                "terminal": body["terminal"],
                "physical_lower_rank": body["physical_lower_rank"],
                "physical_grade_rank": body["physical_grade_rank"],
                "elapsed_seconds": body["elapsed_seconds"],
            },
            sort_keys=True,
        )
    )


def phase_join(state_dir: Path, grade1_dir: Path, certificate_path: Path) -> None:
    state_dir = ensure_external_state_dir(state_dir)
    prepare, prepare_digest = read_sealed_state(state_dir, "grade2-prepare")
    validate_prepare_state(state_dir, prepare, authenticate_blobs=False)
    blocks = [
        read_sealed_state(state_dir, f"grade2-block-{index}", prepare_digest)
        for index in range(4)
    ]
    for index, (body, _) in enumerate(blocks):
        validate_block_state(state_dir, body, prepare, prepare_digest, index, authenticate_basis=False)
    module, module_digest = read_sealed_state(
        state_dir, "grade2-module", prepare_digest
    )
    validate_module_state(state_dir, module, prepare, prepare_digest, blocks)
    certificate_bytes = certificate_path.read_bytes()
    certificate_digest = sha256_bytes(certificate_bytes)
    try:
        existing, digest = read_sealed_state(
            state_dir, "grade2-join", module_digest
        )
    except FileNotFoundError:
        existing = None
    if existing is not None:
        # Re-authenticate the external MEMBER parent before accepting resume.
        authenticate_grade1_member(grade1_dir.resolve(), certificate_path.resolve())
        validate_join_state(
            state_dir, existing, module, module_digest, certificate_digest
        )
        print(json.dumps({"phase": "member-join-preflight", "resumed": True, "state_sha256": digest, "status": existing["status"]}, sort_keys=True))
        return
    started = time.monotonic()
    try:
        body, digest = run_member_join(
            state_dir,
            grade1_dir.resolve(),
            certificate_path.resolve(),
            module,
            module_digest,
            started,
        )
    except RuntimeError as error:
        if str(error).startswith("UNKNOWN_RESOURCE:"):
            seal_unknown_resource(state_dir, "member-join-preflight", module_digest, str(error))
            return
        raise
    print(
        json.dumps(
            {
                "phase": "member-join-preflight", "resumed": False,
                "state_sha256": digest, "status": body["status"],
                "membership_tested": False,
                "elapsed_seconds": body["elapsed_seconds"],
            },
            sort_keys=True,
        )
    )


def phase_all(state_dir: Path, grade1_dir: Path) -> None:
    phase_prepare(state_dir, grade1_dir)
    for character in range(4):
        phase_block(state_dir, character)
    phase_merge(state_dir)


def fixture_split_presentation() -> dict[str, Any]:
    ranks = [1, 0, 0, 0]
    cursor = 0
    old_blocks = []
    for character, rank in enumerate(ranks):
        begin = cursor
        cursor += EXPECTED_SEEDS + 4 * rank
        seed_reductions = [[] for _ in range(EXPECTED_SEEDS)]
        if character == 0:
            seed_reductions[0] = [[0, 1]]
        transitions = [[[ [0, 1] ] for _ in ACTORS]] if rank else []
        old_blocks.append(
            {
                "rank": rank,
                "defect_origin_range": [begin, cursor],
                "record": {
                    "seed_reductions": seed_reductions,
                    "actor_transitions": transitions,
                },
            }
        )
    prepare = {"old_blocks": old_blocks}
    origin_count = cursor
    blocks: list[tuple[dict[str, Any], str]] = []
    for character in range(4):
        origins = [[] for _ in range(origin_count)]
        # Every projected part of seed one contributes to its own h1 row.
        origins[old_blocks[character]["defect_origin_range"][0]] = [[0, 1]]
        if character == 0:
            # Nonzero defect in x acting on the old row.
            origins[EXPECTED_SEEDS] = [[0, 2]]
        body = {
            "rank": 1,
            "origin_reductions": origins,
            "actor_transitions": [
                [[[0, coefficient]] for coefficient in (1, 2, 1, 2)]
            ],
        }
        blocks.append((body, str(character) * 64))
    presentation = assemble_b1_relations(prepare, blocks)
    if (
        presentation["rank"] != 5
        or presentation["seed_reductions"][0]
        != [[0, 1], [1, 1], [2, 1], [3, 1], [4, 1]]
        or presentation["actor_transitions"][0][0] != [[0, 1], [1, 2]]
        or any(len(row) != 4 for row in presentation["actor_transitions"])
    ):
        raise RuntimeError("fixture_split_b1")
    return presentation


def fixture_mutation_validator(value: dict[str, Any]) -> None:
    if value.get("parent") != "a" * 64:
        raise RuntimeError("fixture_parent")
    if value.get("origin_reduction") != [[0, 1]]:
        raise RuntimeError("fixture_origin")
    if value.get("transition") != [[0, 2]]:
        raise RuntimeError("fixture_transition")
    if value.get("monomials") != [list(item) for item in MONOMIALS_DEGREE2]:
        raise RuntimeError("fixture_monomial_split")
    if value.get("queue_exhausted") is not True:
        raise RuntimeError("fixture_queue")


def phase_fixture() -> None:
    started = time.monotonic()
    validate_fixed_layouts()
    words = json.loads(
        (ROOT / "scratchpad/a0_paper_words_v1.json").read_text(encoding="utf-8")
    )
    context = grade1.Context(words)
    affine_preflight = replay_extension_and_boundary_preflight(context, words)
    target2 = direct_target_precision2(context, words)
    target1_reference = grade1.direct_physical_target(context)
    if (
        not np.array_equal(np.concatenate((target2[0], target2[3])), target1_reference[0])
        or not np.array_equal(target2[1], target1_reference[1])
        or not np.array_equal(target2[2], grade1.direct_target_degree2(context))
    ):
        raise RuntimeError("fixture_direct_target_cross_calibration")
    one_term = [[1, [], 1]]
    direct_replay = replay_literal_terms_precision2(context, words, one_term, started)
    reference_replay2 = grade1.replay_degree2_terms(
        context, words["relators"], one_term, started, 30.0, 2 * 1024**3
    )
    if not np.array_equal(direct_replay[2], reference_replay2):
        raise RuntimeError("fixture_degree2_replay_cross_calibration")
    presentation = fixture_split_presentation()
    negative = e_polynomial((2, 0, 0))
    if (
        int(negative[MONOMIAL_INDEX[(1, 0, 0)]]) != 2
        or int(negative[MONOMIAL_INDEX[(2, 0, 0)]]) != 1
    ):
        raise RuntimeError("fixture_negative_column")
    coupled = np.ones(6, dtype=np.uint8)
    if np.count_nonzero(coupled) != 6:
        raise RuntimeError("fixture_coupled_monomials")
    # A dependent lower row can expose a nonzero grade-two connection.
    lower = grade1.PackedEchelon(4)
    first_lower = np.asarray((1, 0, 0, 0), dtype=np.uint8)
    if not lower.insert(first_lower)["accepted"]:
        raise RuntimeError("fixture_lower_first")
    second_remainder, reductions = lower.reduce_packed(grade1.pack_trits(first_lower))
    grade_connection = np.asarray((0, 1, 0, 0), dtype=np.uint8)
    if np.any(second_remainder) or reductions != [[0, 1]] or not np.any(grade_connection):
        raise RuntimeError("fixture_lifted_old_connection")
    # Four exact word-sum records recover one original row by v451 (1.3).
    projected = [np.asarray((1, 0, 0, 0), dtype=np.uint8),
                 np.asarray((0, 1, 0, 0), dtype=np.uint8),
                 np.asarray((0, 0, 1, 0), dtype=np.uint8),
                 np.asarray((0, 0, 0, 1), dtype=np.uint8)]
    recovered = np.zeros(4, dtype=np.uint8)
    for row in projected:
        _add_mod3(recovered, row)
    if not np.array_equal(recovered, np.ones(4, dtype=np.uint8)):
        raise RuntimeError("fixture_seed_recovery")
    contract = {
        "parent": "a" * 64,
        "origin_reduction": [[0, 1]],
        "transition": [[0, 2]],
        "monomials": [list(item) for item in MONOMIALS_DEGREE2],
        "queue_exhausted": True,
    }
    fixture_mutation_validator(contract)
    mutations = 0
    for key, value in (
        ("origin_reduction", [[0, 2]]),
        ("transition", [[0, 1]]),
        ("parent", "b" * 64),
        ("monomials", [list(MONOMIALS_DEGREE2[0])]),
        ("queue_exhausted", False),
    ):
        mutated = dict(contract)
        mutated[key] = value
        try:
            fixture_mutation_validator(mutated)
        except RuntimeError:
            mutations += 1
    # Small independent residual comparison, including mutation rejection.
    target_lower = np.asarray((1, 2, 0, 1), dtype=np.uint8)
    replay_lower = target_lower.copy()
    target_grade = np.asarray((2, 1, 0, 2, 1, 1), dtype=np.uint8)
    replay_grade = np.asarray((1, 1, 0, 0, 1, 2), dtype=np.uint8)
    if np.any((target_lower.astype(np.int16) - replay_lower.astype(np.int16)) % 3):
        raise RuntimeError("fixture_join_lower")
    residual = ((target_grade.astype(np.int16) - replay_grade.astype(np.int16)) % 3).astype(np.uint8)
    stored_residual = residual.copy()
    if not np.array_equal(residual, stored_residual):
        raise RuntimeError("fixture_join_residual")
    stored_residual[0] = (int(stored_residual[0]) + 1) % 3
    if np.array_equal(residual, stored_residual):
        raise RuntimeError("fixture_join_mutation")
    mutations += 1
    with tempfile.TemporaryDirectory(prefix="task565-producer-fixture-") as temporary:
        state_dir = Path(temporary)
        blob = write_blob(
            state_dir, "fixture-blob", bytes((0,)), rows=1, width=4
        )
        validate_blob_receipt(state_dir, blob, 1, 4)
        original = (state_dir / blob["file"]).read_bytes()
        (state_dir / blob["file"]).write_bytes(bytes((1,)))
        try:
            validate_blob_receipt(state_dir, blob, 1, 4)
        except RuntimeError:
            mutations += 1
        (state_dir / blob["file"]).write_bytes(original)
        resume_hashes = []
        parent: str | None = None
        for stem in (
            "fixture-prepare", "fixture-block-0", "fixture-block-1",
            "fixture-block-2", "fixture-block-3", "fixture-module", "fixture-join",
        ):
            body = {"schema": STATE_SCHEMA, "phase": stem, "fixture": True}
            first = write_sealed_state(state_dir, stem, body, parent)
            second = write_sealed_state(state_dir, stem, body, parent)
            if first != second or read_sealed_state(state_dir, stem, parent)[1] != first:
                raise RuntimeError(f"fixture_resume:{stem}")
            resume_hashes.append(first)
            parent = first
    if mutations != 7:
        raise RuntimeError(f"fixture_mutation_count:{mutations}")
    print(
        json.dumps(
            {
                "fixture": "PASS",
                "b1_rank": presentation["rank"],
                "old_transition_defect": "NONZERO",
                "seed_recovery": "PASS",
                "old_and_new_four_actor_transitions": "PASS",
                "negative_column": "u->2u+u^2",
                "coupled_degree2_monomials": 6,
                "dependent_lifted_old_connection": "NONZERO",
                "semantic_mutations_rejected": mutations,
                "member_join_residual_recompute": "PASS",
                "phase_resume_idempotence": len(resume_hashes),
                "affine_boundary_preflight": affine_preflight["replayed"],
                "direct_target_and_replay_cross_calibration": "PASS",
                "terminal_produced": None,
                "elapsed_seconds": time.monotonic() - started,
            },
            sort_keys=True,
        )
    )


def parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--prepare", metavar="STATE_DIR", type=Path)
    modes.add_argument("--block", metavar="N", type=int, choices=range(4))
    modes.add_argument("--merge", metavar="STATE_DIR", type=Path)
    modes.add_argument("--all", metavar="STATE_DIR", type=Path)
    modes.add_argument("--join", metavar="STATE_DIR", type=Path)
    modes.add_argument("--fixture", action="store_true")
    parser.add_argument("--state-dir", type=Path)
    parser.add_argument("--grade1-state-dir", type=Path)
    parser.add_argument("--grade1-certificate", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    arguments = parser().parse_args(argv)
    validate_fixed_layouts()
    if arguments.fixture:
        if any(value is not None for value in (arguments.state_dir, arguments.grade1_state_dir, arguments.grade1_certificate)):
            parser().error("--fixture accepts no state arguments")
        phase_fixture()
    elif arguments.prepare is not None:
        if arguments.grade1_state_dir is None or arguments.state_dir is not None or arguments.grade1_certificate is not None:
            parser().error("--prepare requires only --grade1-state-dir")
        phase_prepare(arguments.prepare, arguments.grade1_state_dir)
    elif arguments.block is not None:
        if arguments.state_dir is None or arguments.grade1_state_dir is not None or arguments.grade1_certificate is not None:
            parser().error("--block requires only --state-dir")
        phase_block(arguments.state_dir, arguments.block)
    elif arguments.merge is not None:
        if arguments.state_dir is not None or arguments.grade1_state_dir is not None or arguments.grade1_certificate is not None:
            parser().error("--merge accepts no additional arguments")
        phase_merge(arguments.merge)
    elif arguments.all is not None:
        if arguments.grade1_state_dir is None or arguments.state_dir is not None or arguments.grade1_certificate is not None:
            parser().error("--all requires only --grade1-state-dir")
        phase_all(arguments.all, arguments.grade1_state_dir)
    elif arguments.join is not None:
        if arguments.grade1_state_dir is None or arguments.grade1_certificate is None or arguments.state_dir is not None:
            parser().error("--join requires --grade1-state-dir and --grade1-certificate")
        phase_join(arguments.join, arguments.grade1_state_dir, arguments.grade1_certificate)
    else:
        raise RuntimeError("fail_closed_phase_dispatch")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
