"""Strict ABI wrapper and small reference for the packed GF(3) worker.

The wrapper never silently falls back to Python when a compiled executable is
absent.  Python reference functions are intentionally useful only for tests.
"""
from __future__ import annotations

import json
import os
import struct
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Sequence

MAGIC = b"D972P3GF"
VERSION = 1
SCHEMA = "packed-gf3-echelon-v1"
HEADER = struct.Struct("<8sIIQQQQ")
MAX_WIDTH = 10_000_000
MAX_ROWS = 100_000
MAX_LEDGER = 10_000_000


class BackendError(ValueError):
    pass


class BackendUnavailable(RuntimeError):
    pass


def _check_shape(width: int, rows: Sequence[Sequence[int]], target: Sequence[int], ids: Sequence[int]) -> int:
    if not isinstance(width, int) or width <= 0 or width % 4 or width > MAX_WIDTH:
        raise BackendError("width")
    if len(rows) != len(ids) or len(rows) > MAX_ROWS or len(target) != width:
        raise BackendError("row_count")
    for row in (*rows, target):
        if len(row) != width or any(type(x) is not int or x not in (0, 1, 2) for x in row):
            raise BackendError("dense_row")
    if any(type(x) is not int or x < 0 or x >= 2**64 for x in ids):
        raise BackendError("row_id")
    return width // 4


def pack_row(row: Sequence[int]) -> bytes:
    if len(row) % 4:
        raise BackendError("pack_width")
    out = bytearray(len(row) // 4)
    for b in range(len(out)):
        x = 0
        for j in range(4):
            v = row[4 * b + j]
            if type(v) is not int or v not in (0, 1, 2):
                raise BackendError("trit")
            x += v * (3**j)
        out[b] = x
    return bytes(out)


def unpack_row(packed: bytes, width: int | None = None) -> list[int]:
    if width is None:
        width = len(packed) * 4
    if width <= 0 or width % 4 or len(packed) != width // 4 or any(x > 80 for x in packed):
        raise BackendError("packed_row")
    out: list[int] = []
    for x in packed:
        for j in range(4):
            out.append((x // (3**j)) % 3)
    return out


def write_input(path: str | os.PathLike[str], width: int, rows: Sequence[Sequence[int]], target: Sequence[int], row_ids: Sequence[int] | None = None) -> None:
    ids = list(range(len(rows))) if row_ids is None else list(row_ids)
    packed = _check_shape(width, rows, target, ids)
    with open(path, "wb") as f:
        f.write(HEADER.pack(MAGIC, VERSION, 1, width, len(rows), packed, 0))
        for row_id, row in zip(ids, rows):
            f.write(struct.pack("<Q", row_id))
            f.write(pack_row(row))
        f.write(pack_row(target))


def run_compiled(input_path: str | os.PathLike[str], receipt_path: str | os.PathLike[str], executable: str | os.PathLike[str] | None = None) -> dict[str, Any]:
    """Run only an explicitly selected compiled worker; missing worker fails closed."""
    exe = str(executable or os.environ.get("D972_PACKED_GF3_BACKEND", ""))
    if not exe:
        raise BackendUnavailable("compiled_backend_not_configured")
    if not Path(exe).is_file():
        raise BackendUnavailable("compiled_backend_missing")
    cmd = [exe, "--version", "1", "--schema", SCHEMA, "--input", str(input_path), "--output", str(receipt_path)]
    try:
        cp = subprocess.run(cmd, check=False, capture_output=True, text=True, timeout=30)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise BackendUnavailable("compiled_backend_failed") from exc
    if cp.returncode != 0:
        raise BackendError("compiled_backend_rejected")
    return parse_receipt(receipt_path)


def _first(row: bytearray) -> int | None:
    for b, x in enumerate(row):
        if x:
            for j in range(4):
                if (x // (3**j)) % 3:
                    return 4 * b + j
    return None


def _axpy(a: int, c: int, b: int) -> int:
    z = 0
    for j in range(4):
        v = ((a // (3**j)) % 3 - c * ((b // (3**j)) % 3)) % 3
        z += v * (3**j)
    return z


def _scale2(a: int) -> int:
    z = 0
    for j in range(4):
        z += (2 * ((a // (3**j)) % 3) % 3) * (3**j)
    return z


@dataclass
class ReferenceEchelon:
    width: int
    rows: list[bytes]
    leads: list[int]
    row_ids: list[int]

    def __init__(self, width: int):
        if width <= 0 or width % 4:
            raise BackendError("width")
        self.width, self.rows, self.leads, self.row_ids = width, [], [], []

    def reduce(self, packed: bytes) -> tuple[bytes, list[list[int]]]:
        if len(packed) != self.width // 4 or any(x > 80 for x in packed):
            raise BackendError("packed_row")
        work = bytearray(packed)
        reductions: list[list[int]] = []
        while True:
            lead = _first(work)
            if lead is None:
                break
            try:
                pivot = self.leads.index(lead)
            except ValueError:
                break
            coeff = (work[lead // 4] // (3 ** (lead % 4))) % 3
            reductions.append([pivot, coeff])
            pivot_row = self.rows[pivot]
            if any(unpack_row(pivot_row, self.width)[: self.leads[pivot]]):
                raise BackendError("pivot_invariant")
            start = lead // 4
            for j in range(start, len(work)):
                work[j] = _axpy(work[j], coeff, pivot_row[j])
        return bytes(work), reductions

    def insert(self, row: Sequence[int], row_id: int = 0) -> dict[str, Any]:
        packed = pack_row(row)
        rem, reductions = self.reduce(packed)
        lead = _first(bytearray(rem))
        result: dict[str, Any] = {"row_id": row_id, "reductions": reductions, "accepted": lead is not None}
        if lead is None:
            return result
        lc = (rem[lead // 4] // (3 ** (lead % 4))) % 3
        scale = 1 if lc == 1 else 2
        norm = bytes(_scale2(x) if scale == 2 else x for x in rem)
        if lead in self.leads:
            raise BackendError("duplicate_lead")
        if any(unpack_row(norm, self.width)[:lead]) or unpack_row(norm, self.width)[lead] != 1:
            raise BackendError("pivot_invariant")
        pivot = len(self.rows)
        self.rows.append(norm); self.leads.append(lead); self.row_ids.append(row_id)
        result.update(pivot=pivot, lead=lead, leading_coefficient=lc, scale=scale)
        return result

    def receipt(self, rows: Sequence[Sequence[int]], ids: Sequence[int], target: Sequence[int]) -> dict[str, Any]:
        offered = [self.insert(row, int(row_id)) for row, row_id in zip(rows, ids)]
        rem, reductions = self.reduce(pack_row(target))
        return {"version": 1, "schema": SCHEMA, "width": self.width, "packed_bytes": self.width // 4,
                "accepted_basis": [{"pivot": i, "row_id": self.row_ids[i], "lead": self.leads[i], "bytes": list(self.rows[i])} for i in range(len(self.rows))],
                "offered": offered, "target": {"reductions": reductions, "coefficients": reductions, "remainder": list(rem)}}


def reference_receipt(width: int, rows: Sequence[Sequence[int]], target: Sequence[int], row_ids: Sequence[int] | None = None) -> dict[str, Any]:
    ids = list(range(len(rows))) if row_ids is None else list(row_ids)
    _check_shape(width, rows, target, ids)
    return ReferenceEchelon(width).receipt(rows, ids, target)


def _pairs(value: Any) -> list[list[int]]:
    if type(value) is not list or any(type(x) is not list or len(x) != 2 or any(type(y) is not int or y < 0 for y in x) for x in value):
        raise BackendError("reductions")
    return value


def parse_receipt(path: str | os.PathLike[str]) -> dict[str, Any]:
    try:
        with open(path, "rb") as f:
            raw = f.read()
        obj = json.loads(raw.decode("utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise BackendError("receipt_json") from exc
    if type(obj) is not dict or obj.get("version") != 1 or obj.get("schema") != SCHEMA:
        raise BackendError("receipt_schema")
    width, packed = obj.get("width"), obj.get("packed_bytes")
    if type(width) is not int or width <= 0 or width % 4 or type(packed) is not int or packed != width // 4 or width > MAX_WIDTH:
        raise BackendError("receipt_dimensions")
    basis = obj.get("accepted_basis"); offered = obj.get("offered"); target = obj.get("target")
    if type(basis) is not list or type(offered) is not list or len(offered) > MAX_ROWS or type(target) is not dict:
        raise BackendError("receipt_sections")
    leads: set[int] = set()
    for i, item in enumerate(basis):
        if type(item) is not dict or item.get("pivot") != i or type(item.get("row_id")) is not int or not (0 <= item["row_id"] < 2**64) or type(item.get("lead")) is not int:
            raise BackendError("basis_record")
        lead = item["lead"]; row = item.get("bytes")
        if lead < 0 or lead >= width or lead in leads or type(row) is not list or len(row) != packed or any(type(x) is not int or x < 0 or x > 80 for x in row):
            raise BackendError("basis_row")
        dense = unpack_row(bytes(row), width)
        if dense[lead] != 1 or any(dense[:lead]):
            raise BackendError("basis_invariant")
        leads.add(lead)
    for item in offered:
        if type(item) is not dict or type(item.get("row_id")) is not int or not (0 <= item["row_id"] < 2**64):
            raise BackendError("offered_record")
        pairs = _pairs(item.get("reductions"))
        if any(p[0] >= len(basis) or p[1] not in (1, 2) for p in pairs):
            raise BackendError("reduction_range")
        if type(item.get("accepted")) is not bool:
            raise BackendError("accepted_flag")
        if item["accepted"]:
            if type(item.get("pivot")) is not int or not (0 <= item["pivot"] < len(basis)) or type(item.get("lead")) is not int or item["lead"] not in leads or type(item.get("leading_coefficient")) is not int or item["leading_coefficient"] not in (1, 2) or type(item.get("scale")) is not int or item["scale"] not in (1, 2):
                raise BackendError("accepted_record")
    _pairs(target.get("reductions")); _pairs(target.get("coefficients"))
    if target["reductions"] != target["coefficients"]:
        raise BackendError("target_coefficients")
    rem = target.get("remainder")
    if type(rem) is not list or len(rem) != packed or any(type(x) is not int or x < 0 or x > 80 for x in rem):
        raise BackendError("target_remainder")
    return obj


__all__ = ["BackendError", "BackendUnavailable", "SCHEMA", "ReferenceEchelon", "pack_row", "unpack_row", "write_input", "run_compiled", "parse_receipt", "reference_receipt"]
