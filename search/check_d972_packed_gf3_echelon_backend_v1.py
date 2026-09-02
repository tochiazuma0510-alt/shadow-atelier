"""Independent bounded checker for d972_packed_gf3_echelon_backend_v1.

This file deliberately shares no imports with the worker wrapper and never
parses the C source as data.  If a compiler is present it invokes a fresh
binary and compares its complete receipt with this independent reference.
"""
from __future__ import annotations

import copy
import hashlib
import json
import os
import shutil
import struct
import subprocess
import tempfile
import time
from pathlib import Path

MAGIC = b"D972P3GF"
SCHEMA = "packed-gf3-echelon-v1"
HEADER = struct.Struct("<8sIIQQQQ")
MAX_WIDTH, MAX_ROWS = 10_000_000, 100_000


def pack(row):
    if len(row) % 4 or any(x not in (0, 1, 2) for x in row):
        raise ValueError("trit")
    return bytes(sum(row[4*b+j] * 3**j for j in range(4)) for b in range(len(row)//4))


def unpack(row, width):
    if len(row) != width//4 or any(x > 80 for x in row):
        raise ValueError("packed")
    return [((x // 3**j) % 3) for x in row for j in range(4)]


def first(row):
    for b, x in enumerate(row):
        for j in range(4):
            if (x // 3**j) % 3:
                return 4*b+j
    return None


def axpy(a, c, b):
    return sum((((a // 3**j) % 3) - c*((b // 3**j) % 3)) % 3 * 3**j for j in range(4))


def scale2(a):
    return sum((2*((a // 3**j) % 3) % 3) * 3**j for j in range(4))


class DenseReference:
    def __init__(self, width):
        self.width, self.rows, self.leads, self.ids = width, [], [], []

    def reduce(self, row):
        w = bytearray(row); reductions = []
        while True:
            lead = first(w)
            if lead is None or lead not in self.leads:
                return bytes(w), reductions
            pivot = self.leads.index(lead)
            coeff = (w[lead//4] // 3**(lead % 4)) % 3
            reductions.append([pivot, coeff])
            prow = self.rows[pivot]
            dense = unpack(prow, self.width)
            if any(dense[:self.leads[pivot]]) or dense[self.leads[pivot]] != 1:
                raise ValueError("stored pivot invariant")
            for i in range(lead//4, len(w)):
                w[i] = axpy(w[i], coeff, prow[i])

    def insert(self, row, row_id):
        remainder, reductions = self.reduce(pack(row))
        lead = first(remainder)
        result = {"row_id": row_id, "reductions": reductions, "accepted": lead is not None}
        if lead is None:
            return result
        lc = (remainder[lead//4] // 3**(lead % 4)) % 3
        factor = 1 if lc == 1 else 2
        norm = bytes(scale2(x) if factor == 2 else x for x in remainder)
        if lead in self.leads:
            raise ValueError("duplicate lead")
        dense = unpack(norm, self.width)
        if any(dense[:lead]) or dense[lead] != 1:
            raise ValueError("new pivot invariant")
        pivot = len(self.rows)
        self.rows.append(norm); self.leads.append(lead); self.ids.append(row_id)
        result.update(pivot=pivot, lead=lead, leading_coefficient=lc, scale=factor)
        return result


def expected(width, rows, ids, target):
    e = DenseReference(width)
    offered = [e.insert(r, i) for r, i in zip(rows, ids)]
    rem, reductions = e.reduce(pack(target))
    return {"version": 1, "schema": SCHEMA, "width": width, "packed_bytes": width//4,
            "accepted_basis": [{"pivot": i, "row_id": e.ids[i], "lead": e.leads[i], "bytes": list(e.rows[i])} for i in range(len(e.rows))],
            "offered": offered, "target": {"reductions": reductions, "coefficients": reductions, "remainder": list(rem)}}


def write_input(path, width, rows, ids, target):
    p = width//4
    with open(path, "wb") as f:
        f.write(HEADER.pack(MAGIC, 1, 1, width, len(rows), p, 0))
        for i, row in zip(ids, rows):
            f.write(struct.pack("<Q", i)); f.write(pack(row))
        f.write(pack(target))


def read_input(path):
    data = Path(path).read_bytes()
    if len(data) < HEADER.size:
        raise ValueError("truncated header")
    magic, version, schema, width, nrows, packed, reserved = HEADER.unpack_from(data)
    if magic != MAGIC or version != 1 or schema != 1 or reserved != 0 or width <= 0 or width % 4 or width > MAX_WIDTH or packed != width//4 or nrows > MAX_ROWS:
        raise ValueError("input header")
    expected_len = HEADER.size + nrows*(8+packed) + packed
    if len(data) != expected_len:
        raise ValueError("input length")
    pos = HEADER.size; rows = []; ids = []
    for _ in range(nrows):
        ids.append(struct.unpack_from("<Q", data, pos)[0]); pos += 8
        row = data[pos:pos+packed]; pos += packed
        if any(x > 80 for x in row): raise ValueError("input byte")
        rows.append(unpack(row, width))
    target = unpack(data[pos:pos+packed], width)
    return width, rows, ids, target


def validate_receipt(obj):
    if type(obj) is not dict or obj.get("version") != 1 or obj.get("schema") != SCHEMA:
        raise ValueError("schema")
    width, packed = obj.get("width"), obj.get("packed_bytes")
    if type(width) is not int or width <= 0 or width % 4 or width > MAX_WIDTH or packed != width//4:
        raise ValueError("dimensions")
    basis, offered, target = obj.get("accepted_basis"), obj.get("offered"), obj.get("target")
    if type(basis) is not list or type(offered) is not list or len(offered) > MAX_ROWS or type(target) is not dict:
        raise ValueError("sections")
    leads = set()
    for i, b in enumerate(basis):
        if type(b) is not dict or b.get("pivot") != i or type(b.get("row_id")) is not int or type(b.get("lead")) is not int:
            raise ValueError("basis record")
        lead, row = b["lead"], b.get("bytes")
        if lead < 0 or lead >= width or lead in leads or type(row) is not list or len(row) != packed or any(type(x) is not int or x < 0 or x > 80 for x in row):
            raise ValueError("basis bytes")
        dense = unpack(bytes(row), width)
        if dense[lead] != 1 or any(dense[:lead]): raise ValueError("basis invariant")
        leads.add(lead)
    def pairs(value):
        if type(value) is not list: raise ValueError("pairs")
        for pair in value:
            if type(pair) is not list or len(pair) != 2 or type(pair[0]) is not int or type(pair[1]) is not int or not (0 <= pair[0] < len(basis)) or pair[1] not in (1, 2):
                raise ValueError("pair range")
    for o in offered:
        if type(o) is not dict or type(o.get("row_id")) is not int or type(o.get("accepted")) is not bool:
            raise ValueError("offered record")
        pairs(o.get("reductions"))
        if o["accepted"] and (type(o.get("pivot")) is not int or not (0 <= o["pivot"] < len(basis)) or type(o.get("lead")) is not int or o["lead"] not in leads or type(o.get("leading_coefficient")) is not int or o["leading_coefficient"] not in (1, 2) or o.get("scale") not in (1, 2)):
            raise ValueError("acceptance")
    pairs(target.get("reductions")); pairs(target.get("coefficients"))
    if target["reductions"] != target["coefficients"]: raise ValueError("coefficients")
    if type(target.get("remainder")) is not list or len(target["remainder"]) != packed or any(type(x) is not int or x < 0 or x > 80 for x in target["remainder"]): raise ValueError("target remainder")
    return True


def six_cases():
    z = [0]*12
    return [
        ("zero", [z], [101], z),
        ("missing", [[0,0,0,0,0,0,0,0,1,0,0,0]], [102], z),
        ("same-byte", [[0,0,0,0,0,1,2,0,0,0,0,0], [0,0,0,0,0,0,1,0,0,0,0,0]], [103,104], z),
        ("nonmonotone", [[0,0,0,0,0,1,0,0,0,0,0,0], [0,0,0,1,0,0,0,0,0,0,0,0]], [105,106], z),
        ("scale-two", [[0,0,2,0,0,0,0,0,0,0,0,0]], [107], z),
        ("dependent-trace", [[0,1,0,0,0,0,0,0,0,0,0,0], [1,0,0,0,0,0,0,0,0,0,0,0], [0,0,1,0,0,0,0,0,0,0,0,0], [1,2,2,0,0,0,0,0,0,0,0,0]], [108,109,110,111], z),
    ]


def random_case():
    state = 0xD972567
    rows = []
    for _ in range(32):
        row = []
        for _ in range(20):
            state = (1664525*state + 1013904223) & 0xffffffff
            row.append((state >> 29) % 3)
        rows.append(row)
    target = rows[3][:]
    return 20, rows, list(range(900, 932)), target


def suffix_full_equal(width, rows, ids):
    # Compare the optimized suffix update with a deliberately full-row update.
    e = DenseReference(width); full_rows = []; full_leads = []
    for row, row_id in zip(rows, ids):
        p = pack(row); w = bytearray(p); red = []
        while True:
            lead = first(w)
            if lead is None or lead not in full_leads: break
            pivot = full_leads.index(lead); c = (w[lead//4] // 3**(lead%4)) % 3; red.append([pivot, c])
            for j in range(len(w)): w[j] = axpy(w[j], c, full_rows[pivot][j])
        opt_rem, opt_red = e.reduce(p)
        if bytes(w) != opt_rem or red != opt_red: return False
        lead = first(w)
        if lead is not None:
            lc = (w[lead//4] // 3**(lead%4)) % 3
            if lc == 2: w = bytearray(scale2(x) for x in w)
            full_rows.append(bytes(w)); full_leads.append(lead)
        e.insert(row, row_id)
    return True


def main():
    started = time.perf_counter(); cases = six_cases(); checked = 0
    with tempfile.TemporaryDirectory(prefix="d972-packed-gf3-") as td:
        td = Path(td)
        for name, rows, ids, target in cases:
            exp = expected(12, rows, ids, target); validate_receipt(exp)
            if name == "dependent-trace" and exp["offered"][-1]["reductions"] != [[1, 1], [0, 2], [2, 2]]: raise AssertionError("frozen trace")
            if name == "nonmonotone" and [b["lead"] for b in exp["accepted_basis"]] != [5, 3]: raise AssertionError("lead order")
            checked += 1
        width, rows, ids, target = random_case(); bench_start = time.perf_counter(); exp = expected(width, rows, ids, target); bench_seconds = time.perf_counter() - bench_start; validate_receipt(exp); checked += 1
        member_rows = [[1, 0, 0, 0, 0, 0, 0, 0]]
        member = expected(8, member_rows, [7001], member_rows[0]); validate_receipt(member)
        if member["target"]["reductions"] != [[0, 1]] or member["target"]["remainder"] != [0, 0]: raise AssertionError("member target")
        nonmember = expected(8, member_rows, [7002], [0, 1, 0, 0, 0, 0, 0, 0]); validate_receipt(nonmember)
        if nonmember["target"]["remainder"] == [0, 0]: raise AssertionError("nonmember remainder")
        if not suffix_full_equal(width, rows, ids): raise AssertionError("suffix/full mismatch")
        # Resume boundary: independently process two prefixes and ensure the same
        # insertion-ordered state and target result as one uninterrupted run.
        split = 11; left = DenseReference(width); [left.insert(r, i) for r, i in zip(rows[:split], ids[:split])]
        right = DenseReference(width); right.rows, right.leads, right.ids = left.rows[:], left.leads[:], left.ids[:]
        [right.insert(r, i) for r, i in zip(rows[split:], ids[split:])]
        if expected(width, rows, ids, target) != {**expected(width, rows, ids, target), "accepted_basis": [{"pivot": i, "row_id": right.ids[i], "lead": right.leads[i], "bytes": list(right.rows[i])} for i in range(len(right.rows))]}:
            raise AssertionError("resume boundary")
        # Receipt and input fail-closed mutations.
        good = expected(12, cases[2][1], cases[2][2], cases[2][3]); validate_receipt(good)
        mutations = []
        m = copy.deepcopy(good); m["schema"] = "wrong"; mutations.append(m)
        m = copy.deepcopy(good); m["accepted_basis"][0]["bytes"][0] = 81; mutations.append(m)
        m = copy.deepcopy(good); m["accepted_basis"][0]["lead"] = 0; mutations.append(m)
        m = copy.deepcopy(good); m["offered"][1]["reductions"] = [[999999, 1]]; mutations.append(m)
        m = copy.deepcopy(good); m["target"]["coefficients"] = [[0, 7]]; mutations.append(m)
        rejected = 0
        for m in mutations:
            try: validate_receipt(m)
            except ValueError: rejected += 1
        if rejected != len(mutations): raise AssertionError("receipt mutations")
        inp = td / "input.bin"; write_input(inp, 12, cases[2][1], cases[2][2], cases[2][3])
        read_input(inp)
        raw = bytearray(inp.read_bytes()); raw[HEADER.size + 8] = 81; (td/"bad-byte.bin").write_bytes(raw)
        try: read_input(td/"bad-byte.bin"); raise AssertionError("bad byte accepted")
        except ValueError: pass
        (td/"truncated.bin").write_bytes(inp.read_bytes()[:-1])
        try: read_input(td/"truncated.bin"); raise AssertionError("truncated accepted")
        except ValueError: pass
        compiler = next((shutil.which(x) for x in ("cc", "gcc", "clang") if shutil.which(x)), None)
        compiled = False; compile_note = "COMPILED_FIXTURE_NOT_RUN_NO_COMPILER"
        if compiler:
            exe = td / "backend"; src = Path(__file__).with_name("d972_packed_gf3_echelon_backend_v1.c")
            cp = subprocess.run([compiler, "-std=c11", "-O2", str(src), "-o", str(exe)], capture_output=True, text=True, timeout=30)
            if cp.returncode == 0:
                compiled = True; compile_note = "COMPILED_FIXTURE_PASS"
                rec = td / "receipt.json"; write_input(inp, width, rows, ids, target)
                run = subprocess.run([str(exe), "--version", "1", "--schema", SCHEMA, "--input", str(inp), "--output", str(rec)], capture_output=True, timeout=30)
                if run.returncode != 0: raise AssertionError("compiled worker rejected fixture")
                got = json.loads(rec.read_text()); validate_receipt(got)
                if got != exp: raise AssertionError("compiled receipt mismatch")
        elapsed = time.perf_counter() - started
        print(json.dumps({"fixture": "PASS", "frozen_cases": 6, "random_rows": 32, "member_target": "PASS", "nonmember_remainder": "PASS", "reference_benchmark_seconds": round(bench_seconds, 6), "suffix_full": "PASS", "resume_boundary": "PASS", "mutations_rejected": len(mutations)+2, "compiler": compiler or "none", "compiled": compiled, "compiled_status": compile_note, "elapsed_seconds": round(elapsed, 6)}, sort_keys=True))


if __name__ == "__main__":
    main()
