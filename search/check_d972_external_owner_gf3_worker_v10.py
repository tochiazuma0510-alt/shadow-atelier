"""Bounded v10 checker for the external-owner GF(3) worker."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import queue
import shutil
import struct
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
C_SOURCE = ROOT / "search/d972_external_owner_gf3_worker_v10.c"
WRAPPER = ROOT / "search/d972_external_owner_gf3_worker_v10.py"
WIRE = struct.Struct("<4sBBBB10Q")
RECORD = struct.Struct("<4sBBH6Q")
MAGIC_REQ, MAGIC_RESP, REC_MAGIC = b"EORA", b"EOWA", b"EOTA"
VERSION = 10
DEP, ACC, UNK, MAL, FATAL, STATS, CLOSED = range(7)
MAX_WIDTH, MAX_COMPANION_WIDTH, MAX_RANK = 36288, 48384, 4095


def pack_trits(values):
    if any(type(value) is not int or value not in (0, 1, 2) for value in values):
        raise AssertionError("noncanonical_trit")
    packed = bytearray((len(values) + 3) // 4)
    for index, value in enumerate(values):
        packed[index // 4] += value * 3 ** (index % 4)
    assert all(value <= 80 for value in packed)
    return bytes(packed)


def unpack_trits(data, width):
    assert len(data) == width // 4 and all(value <= 80 for value in data)
    return [(data[index // 4] // (3 ** (index % 4))) % 3 for index in range(width)]


def encode_pair(pivot, coefficient):
    assert 0 <= pivot < MAX_RANK and coefficient in (1, 2)
    return struct.pack("<H", 2 * pivot + coefficient - 1)


def decode_pair_bytes(data, rank_cap):
    assert len(data) % 2 == 0
    result = []
    for (code,) in struct.iter_unpack("<H", data):
        pivot, remainder = divmod(code, 2)
        assert pivot < rank_cap and remainder in (0, 1)
        result.append((pivot, remainder + 1))
    return result


def campaign_rows():
    def padded(*values):
        return list(values) + [0] * (8 - len(values))

    rows = [
        padded(1),
        padded(0, 1),
        padded(2),
        padded(0, 2),
        padded(1, 1),
        padded(),
        padded(2, 1),
        padded(1, 2),
        padded(),
        padded(0, 0, 1),
        padded(0, 0, 2),
        padded(1, 0, 1),
        padded(0, 1, 1),
        padded(1, 1, 1),
        padded(2, 2, 2),
        padded(),
    ]
    companions = [
        padded(2),
        padded(0, 2),
        padded(1),
        padded(0, 1),
        padded(1, 1),
        padded(0, 0, 1),
        padded(2, 2),
        padded(1, 2),
        padded(2, 1),
        padded(2, 1, 0),
        padded(1, 1, 0),
        padded(2, 2, 0),
        padded(1, 2, 1),
        padded(2, 1, 2),
        padded(1, 1, 1),
        padded(0, 0, 2),
    ]
    assert all(len(row) == 8 and all(value in (0, 1, 2) for value in row) for row in rows + companions)
    return rows, companions


def write_campaign(path):
    rows, companions = campaign_rows()
    offers = [
        {"id": oid, "primary": pack_trits(row).hex(), "companion": pack_trits(companion).hex()}
        for oid, (row, companion) in enumerate(zip(rows, companions), 1)
    ]
    campaign = {"width": 8, "companion_width": 8, "origin_count": 4, "offers": offers}
    Path(path).write_text(
        json.dumps(campaign, sort_keys=True, separators=(",", ":")), encoding="utf-8"
    )
    return campaign


def decode_campaign(path):
    campaign = json.loads(Path(path).read_text(encoding="utf-8"))
    assert set(campaign) == {"width", "companion_width", "origin_count", "offers"}
    width, companion_width = campaign["width"], campaign["companion_width"]
    assert (width, companion_width, campaign["origin_count"]) == (8, 8, 4)
    offers = []
    for item in campaign["offers"]:
        assert set(item) == {"id", "primary", "companion"}
        primary = bytes.fromhex(item["primary"])
        companion = bytes.fromhex(item["companion"])
        assert len(primary) == width // 4 and len(companion) == companion_width // 4
        assert all(value <= 80 for value in primary + companion)
        offers.append((item["id"], primary, companion))
    assert [item[0] for item in offers] == list(range(1, 17))
    return campaign, offers


def dense_image(campaign_path):
    campaign, offers = decode_campaign(campaign_path)
    width, companion_width = campaign["width"], campaign["companion_width"]
    basis, companion_basis, lead_order = [], [], []
    results = []
    transcript = bytearray()
    offsets = bytearray(struct.pack("<Q", 0))
    basis_bytes, companion_bytes, lead_bytes = bytearray(), bytearray(), bytearray()
    for oid, packed_primary, packed_companion in offers:
        work = unpack_trits(packed_primary, width)
        companion = unpack_trits(packed_companion, companion_width)
        reductions = []
        while True:
            lead = next((index for index, value in enumerate(work) if value), None)
            if lead is None or lead not in lead_order:
                break
            pivot = lead_order.index(lead)
            coefficient = work[lead]
            reductions.append((pivot, coefficient))
            work = [(left - coefficient * right) % 3 for left, right in zip(work, basis[pivot])]
            companion = [
                (left - coefficient * right) % 3
                for left, right in zip(companion, companion_basis[pivot])
            ]
        lead = next((index for index, value in enumerate(work) if value), None)
        if lead is None:
            result = {
                "id": oid,
                "status": DEP,
                "reductions": reductions,
                "pivot": 0,
                "lead": 0,
                "lc": 0,
                "scale": 0,
                "primary": b"",
                "companion": pack_trits(companion),
            }
        else:
            lc = work[lead]
            scale = 1 if lc == 1 else 2
            work = [(scale * value) % 3 for value in work]
            companion = [(scale * value) % 3 for value in companion]
            normalized = pack_trits(work)
            normalized_companion = pack_trits(companion)
            pivot = len(basis)
            basis.append(work)
            companion_basis.append(companion)
            lead_order.append(lead)
            basis_bytes.extend(normalized)
            companion_bytes.extend(normalized_companion)
            lead_bytes.extend(struct.pack("<QQ", lead, oid))
            result = {
                "id": oid,
                "status": ACC,
                "reductions": reductions,
                "pivot": pivot,
                "lead": lead,
                "lc": lc,
                "scale": scale,
                "primary": normalized,
                "companion": normalized_companion,
            }
        record = RECORD.pack(
            REC_MAGIC,
            VERSION,
            result["status"],
            0,
            oid,
            result["pivot"],
            result["lead"],
            result["lc"],
            result["scale"],
            len(reductions),
        ) + b"".join(encode_pair(pivot, coefficient) for pivot, coefficient in reductions)
        transcript.extend(record)
        offsets.extend(struct.pack("<Q", len(transcript)))
        results.append(result)
    accepted_ids = [result["id"] for result in results if result["status"] == ACC]
    assert accepted_ids == [1, 2, 10]
    streams = {
        "basis.bin": bytes(basis_bytes),
        "companion.bin": bytes(companion_bytes),
        "transcript.bin": bytes(transcript),
        "offsets.bin": bytes(offsets),
        "leads.bin": bytes(lead_bytes),
    }
    return {
        "campaign": campaign,
        "offers": offers,
        "results": results,
        "streams": streams,
        "accepted_ids": accepted_ids,
    }


def load_owner_module():
    spec = importlib.util.spec_from_file_location("d972_external_owner_v10_checked", WRAPPER)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class WireClient:
    def __init__(self, process):
        self.process = process
        self.queue = queue.Queue()
        self.buffer = bytearray()
        self.closed = False

        def pump():
            try:
                while True:
                    if hasattr(process.stdout, "read1"):
                        chunk = process.stdout.read1(65536)
                    else:
                        chunk = os.read(process.stdout.fileno(), 65536)
                    if not chunk:
                        self.queue.put(None)
                        return
                    self.queue.put(chunk)
            except BaseException as exc:
                self.queue.put(exc)

        self.thread = threading.Thread(target=pump, name="eow-v10-checker-wire", daemon=True)
        self.thread.start()

    def write(self, data, fragments=False):
        parts = (data[index : index + 1] for index in range(len(data))) if fragments else (data,)
        for part in parts:
            done = 0
            while done < len(part):
                count = self.process.stdin.write(part[done:])
                if not count:
                    self.abort()
                    raise AssertionError("short_request_write")
                done += count
            self.process.stdin.flush()

    def read_exact(self, length, deadline):
        while len(self.buffer) < length:
            left = deadline - time.monotonic()
            if left <= 0:
                self.abort()
                raise AssertionError("response_deadline")
            try:
                item = self.queue.get(timeout=left)
            except queue.Empty as exc:
                self.abort()
                raise AssertionError("response_deadline") from exc
            if item is None:
                raise AssertionError("service_eof")
            if isinstance(item, BaseException):
                raise AssertionError("service_reader") from item
            self.buffer.extend(item)
        data = bytes(self.buffer[:length])
        del self.buffer[:length]
        return data

    def expect_eof(self, timeout=5):
        if self.buffer:
            raise AssertionError("trailing_output")
        deadline = time.monotonic() + timeout
        while True:
            left = deadline - time.monotonic()
            if left <= 0:
                self.abort()
                raise AssertionError("eof_deadline")
            try:
                item = self.queue.get(timeout=left)
            except queue.Empty as exc:
                self.abort()
                raise AssertionError("eof_deadline") from exc
            if item is None:
                return
            if isinstance(item, BaseException):
                raise AssertionError("service_reader") from item
            self.buffer.extend(item)
            if self.buffer:
                raise AssertionError("trailing_output")

    def close_stdin(self):
        try:
            self.process.stdin.close()
        except Exception:
            pass

    def finish(self, expected_code, timeout=5):
        try:
            code = self.process.wait(timeout=timeout)
        except subprocess.TimeoutExpired as exc:
            self.abort()
            raise AssertionError("service_exit_deadline") from exc
        assert code == expected_code, (code, expected_code)
        self.close_stdin()
        try:
            self.process.stdout.close()
        except Exception:
            pass
        self.thread.join(timeout=timeout)
        assert not self.thread.is_alive()
        self.closed = True
        return code

    def abort(self):
        if self.closed:
            return
        if self.process.poll() is None:
            self.process.kill()
        self.close_stdin()
        try:
            self.process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            self.process.kill()
            self.process.wait()
        try:
            self.process.stdout.close()
        except Exception:
            pass
        self.thread.join(timeout=5)
        assert not self.thread.is_alive()
        self.closed = True


def launch(
    exe,
    directory,
    *,
    width=8,
    companion_width=8,
    rank_cap=8,
    offer_cap=64,
    byte_cap=1 << 20,
    committed_offers=0,
    committed_accepted=0,
    logical_bytes=0,
):
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    for name in ("basis.bin", "companion.bin", "transcript.bin", "offsets.bin", "leads.bin"):
        path = directory / name
        if not path.exists():
            path.write_bytes(b"")
    args = [
        str(exe),
        "--serve",
        "--width",
        str(width),
        "--companion-width",
        str(companion_width),
        "--rank-cap",
        str(rank_cap),
        "--offer-cap",
        str(offer_cap),
        "--byte-cap",
        str(byte_cap),
        "--session",
        "17",
        "--committed-offers",
        str(committed_offers),
        "--committed-accepted",
        str(committed_accepted),
        "--logical-bytes",
        str(logical_bytes),
        "--basis",
        str(directory / "basis.bin"),
        "--leads",
        str(directory / "leads.bin"),
    ]
    if companion_width:
        args += ["--companion", str(directory / "companion.bin")]
    process = subprocess.Popen(
        args,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    )
    return WireClient(process)


def read_response(client, *, timeout=5, rank_cap=MAX_RANK, width=MAX_WIDTH, companion_width=MAX_COMPANION_WIDTH):
    deadline = time.monotonic() + timeout
    values = WIRE.unpack(client.read_exact(WIRE.size, deadline))
    magic, version, status, flags, reserved, rid, offers, accepted, pivot, lead, lc, scale, nq, pn, cn = values
    assert (magic, version, flags, reserved) == (MAGIC_RESP, VERSION, 0, 0)
    assert status in range(7) and nq <= rank_cap and pn <= width // 4 and cn <= companion_width // 4
    body = client.read_exact(2 * nq + pn + cn, deadline)
    pairs = decode_pair_bytes(body[: 2 * nq], rank_cap)
    primary = body[2 * nq : 2 * nq + pn]
    companion = body[2 * nq + pn :]
    assert all(value <= 80 for value in primary + companion)
    return {
        "status": status,
        "id": rid,
        "offers": offers,
        "accepted": accepted,
        "pivot": pivot,
        "lead": lead,
        "lc": lc,
        "scale": scale,
        "pairs": pairs,
        "primary": primary,
        "companion": companion,
        "pn": pn,
        "cn": cn,
    }


def send_offer(
    client,
    oid,
    offers,
    accepted,
    primary,
    companion,
    *,
    width,
    companion_width,
    rank_cap,
    fragments=False,
):
    pn, cn = width // 4, companion_width // 4
    assert len(primary) == pn and len(companion) == cn
    header = WIRE.pack(
        MAGIC_REQ,
        VERSION,
        1,
        0,
        0,
        oid,
        offers,
        accepted,
        0,
        0,
        0,
        0,
        0,
        pn,
        cn,
    )
    assert len(header) == WIRE.size == 88
    frame = header + primary + companion
    assert len(frame) == WIRE.size + pn + cn
    client.write(frame, fragments=fragments)
    return read_response(
        client,
        rank_cap=rank_cap,
        width=width,
        companion_width=companion_width,
    )


def send_control(client, op, offers, accepted):
    header = WIRE.pack(
        MAGIC_REQ,
        VERSION,
        op,
        0,
        0,
        0,
        offers,
        accepted,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
    )
    assert len(header) == WIRE.size == 88
    client.write(header)
    return read_response(client)


def assert_control(response, status, offers, accepted):
    assert response == {
        "status": status,
        "id": 0,
        "offers": offers,
        "accepted": accepted,
        "pivot": 0,
        "lead": 0,
        "lc": 0,
        "scale": 0,
        "pairs": [],
        "primary": b"",
        "companion": b"",
        "pn": 0,
        "cn": 0,
    }


def close_clean(client, offers, accepted):
    stats = send_control(client, 2, offers, accepted)
    assert_control(stats, STATS, offers, accepted)
    closed = send_control(client, 3, offers, accepted)
    assert_control(closed, CLOSED, offers, accepted)
    client.expect_eof()
    client.finish(0)


def direct_campaign(exe, campaign_path, work_root):
    expected = dense_image(campaign_path)
    campaign, offers = decode_campaign(campaign_path)
    client = launch(exe, Path(work_root) / "direct")
    offer_count = accepted_count = 0
    try:
        for want, (oid, primary, companion) in zip(expected["results"], offers):
            response = send_offer(
                client,
                oid,
                offer_count,
                accepted_count,
                primary,
                companion,
                width=campaign["width"],
                companion_width=campaign["companion_width"],
                rank_cap=8,
            )
            assert response["id"] == oid
            assert response["status"] == want["status"]
            assert response["pairs"] == want["reductions"]
            assert response["offers"] == offer_count + 1
            assert response["accepted"] == accepted_count + (want["status"] == ACC)
            assert (response["pivot"], response["lead"], response["lc"], response["scale"]) == (
                want["pivot"],
                want["lead"],
                want["lc"],
                want["scale"],
            )
            assert response["primary"] == want["primary"]
            assert response["companion"] == want["companion"]
            offer_count += 1
            accepted_count += want["status"] == ACC
        assert (offer_count, accepted_count) == (16, 3)
        close_clean(client, offer_count, accepted_count)
    finally:
        client.abort()
    return {"offers": 16, "accepted": 3, "stats": "PASS", "closed_eof_exit0": "PASS"}


def coefficient_one_cancellation_gate(exe, work_root):
    client = launch(
        exe,
        Path(work_root) / "coefficient_one",
        width=4,
        companion_width=0,
        rank_cap=2,
        logical_bytes=0,
    )
    row = pack_trits([1, 0, 0, 0])
    try:
        first = send_offer(
            client, 1, 0, 0, row, b"", width=4, companion_width=0, rank_cap=2
        )
        assert first["status"] == ACC and first["primary"] == row and first["lead"] == 0
        second = send_offer(
            client, 2, 1, 1, row, b"", width=4, companion_width=0, rank_cap=2
        )
        assert second["status"] == DEP
        assert second["pairs"] == [(0, 1)]
        assert second["primary"] == b"" and second["offers"] == 2 and second["accepted"] == 1
        close_clean(client, 2, 1)
    finally:
        client.abort()
    return {"SUB_coefficient_1_identical_byte": "CANCELS_TO_ZERO", "witness": [1, 1, 0]}


def cap_gate(exe, work_root):
    e0 = pack_trits([1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    e1 = pack_trits([0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    e0_e1 = pack_trits([1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    cases = (
        ("rank", {"rank_cap": 1, "offer_cap": 8, "byte_cap": 1 << 20}, e1),
        ("offer", {"rank_cap": 8, "offer_cap": 1, "byte_cap": 1 << 20}, e1),
        ("byte_after_pair", {"rank_cap": 8, "offer_cap": 8, "byte_cap": 175}, e0_e1),
    )
    result = {}
    for name, caps, rejected_row in cases:
        client = launch(
            exe,
            Path(work_root) / f"cap_{name}",
            width=12,
            companion_width=0,
            logical_bytes=8,
            **caps,
        )
        try:
            accepted = send_offer(
                client, 1, 0, 0, e0, b"", width=12, companion_width=0, rank_cap=caps["rank_cap"]
            )
            assert accepted["status"] == ACC and (accepted["offers"], accepted["accepted"]) == (1, 1)
            unknown = send_offer(
                client,
                2,
                1,
                1,
                rejected_row,
                b"",
                width=12,
                companion_width=0,
                rank_cap=caps["rank_cap"],
            )
            assert unknown == {
                "status": UNK,
                "id": 2,
                "offers": 1,
                "accepted": 1,
                "pivot": 0,
                "lead": 0,
                "lc": 0,
                "scale": 0,
                "pairs": [],
                "primary": b"",
                "companion": b"",
                "pn": 0,
                "cn": 0,
            }
            close_clean(client, 1, 1)
            result[name] = "UNKNOWN_UNCHANGED_STATS_CLOSED_EOF_EXIT0"
        finally:
            client.abort()
    return result


def parse_state(directory, expected):
    directory = Path(directory)
    manifest = json.loads((directory / "manifest.json").read_text(encoding="utf-8"))
    assert (manifest["version"], manifest["schema"]) == (10, "external-owner-v10")
    assert (manifest["offers"], manifest["accepted"], manifest["last_id"]) == (16, 3, 16)
    raw = {name: (directory / name).read_bytes() for name in expected["streams"]}
    for name, wanted in expected["streams"].items():
        assert raw[name] == wanted, name
        assert manifest["lengths"][name] == len(wanted)
        assert manifest["sha256"][name] == hashlib.sha256(wanted).hexdigest()
    assert manifest["logical_bytes"] == sum(len(value) for value in raw.values())
    offsets = [value[0] for value in struct.iter_unpack("<Q", raw["offsets.bin"])]
    assert len(offsets) == 17 and offsets[0] == 0 and offsets[-1] == len(raw["transcript.bin"])
    accepted_index = 0
    for index, want in enumerate(expected["results"]):
        start, end = offsets[index], offsets[index + 1]
        header = RECORD.unpack_from(raw["transcript.bin"], start)
        magic, version, status, reserved, oid, pivot, lead, lc, scale, nq = header
        assert (magic, version, reserved, oid, status) == (
            REC_MAGIC,
            VERSION,
            0,
            want["id"],
            want["status"],
        )
        assert (pivot, lead, lc, scale) == (
            want["pivot"],
            want["lead"],
            want["lc"],
            want["scale"],
        )
        pair_bytes = raw["transcript.bin"][start + RECORD.size : end]
        assert len(pair_bytes) == 2 * nq
        assert decode_pair_bytes(pair_bytes, 8) == want["reductions"]
        if status == ACC:
            assert raw["basis.bin"][accepted_index * 2 : (accepted_index + 1) * 2] == want["primary"]
            assert raw["companion.bin"][accepted_index * 2 : (accepted_index + 1) * 2] == want["companion"]
            assert struct.unpack_from("<QQ", raw["leads.bin"], accepted_index * 16) == (
                want["lead"],
                want["id"],
            )
            accepted_index += 1
    assert accepted_index == 3
    return manifest


def run_wrapper(exe, directory, campaign_path, kill_after=-1):
    args = [
        sys.executable,
        str(WRAPPER),
        "--fixture",
        "--campaign",
        str(campaign_path),
        "--exe",
        str(exe),
        "--directory",
        str(directory),
        "--response-deadline",
        "3",
    ]
    if kill_after >= 0:
        args += ["--kill-after", str(kill_after)]
    return subprocess.run(
        args,
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        timeout=30,
    )


def assert_physical_provisional(directory):
    directory = Path(directory)
    manifest = json.loads((directory / "manifest.json").read_text(encoding="utf-8"))
    assert (manifest["generation"], manifest["offers"], manifest["accepted"], manifest["last_id"]) == (
        1,
        4,
        2,
        4,
    )
    for name, length in manifest["lengths"].items():
        physical = (directory / name).read_bytes()
        assert len(physical) >= length
        assert hashlib.sha256(physical[:length]).hexdigest() == manifest["sha256"][name]
    offsets_raw = (directory / "offsets.bin").read_bytes()
    transcript = (directory / "transcript.bin").read_bytes()
    assert len(offsets_raw) >= 7 * 8
    offsets = [struct.unpack_from("<Q", offsets_raw, 8 * index)[0] for index in range(7)]
    assert offsets[4] == manifest["lengths"]["transcript.bin"]
    provisional = []
    for record_index in (4, 5):
        start, end = offsets[record_index], offsets[record_index + 1]
        assert end <= len(transcript) and end > start
        header = RECORD.unpack_from(transcript, start)
        nq = header[-1]
        assert end - start == RECORD.size + 2 * nq
        assert (header[0], header[1], header[3], header[4]) == (
            REC_MAGIC,
            VERSION,
            0,
            record_index + 1,
        )
        provisional.append(header[4])
    assert provisional == [5, 6]
    return {"committed_offers": 4, "physical_provisional_ids": provisional, "physical_offsets": 7}


def durable_cursor_gate(exe, campaign_path, work_root):
    expected = dense_image(campaign_path)
    base = Path(work_root) / "durable_base"
    complete = run_wrapper(exe, base, campaign_path)
    assert complete.returncode == 0, complete.stderr
    parse_state(base, expected)
    output = json.loads(complete.stdout)
    expected_cursor = {
        "accepted_ids": [1, 2, 10],
        "origins_complete": True,
        "next_pivot": None,
        "next_source_id": None,
        "next_actor_index": None,
        "next_id": None,
        "fifo_exhausted": True,
    }
    assert output == {"cursor": expected_cursor, "finalize": expected_cursor}

    resumed = Path(work_root) / "hard_kill_resume"
    interrupted = run_wrapper(exe, resumed, campaign_path, 6)
    assert interrupted.returncode == 137, (interrupted.returncode, interrupted.stderr)
    provisional = assert_physical_provisional(resumed)
    resumed_result = run_wrapper(exe, resumed, campaign_path)
    assert resumed_result.returncode == 0, resumed_result.stderr
    parse_state(resumed, expected)
    resumed_output = json.loads(resumed_result.stdout)
    assert resumed_output == {"cursor": expected_cursor, "finalize": expected_cursor}
    for name in (*expected["streams"].keys(), "manifest.json"):
        assert (base / name).read_bytes() == (resumed / name).read_bytes(), name
    return {
        "five_stream_whole_byte_image": "PASS",
        "cursor_finalize": "PASS",
        "suffix_resume_from_id5": "PASS",
        "hard_kill": provisional,
    }


def rehash(directory, names):
    directory = Path(directory)
    manifest_path = directory / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    for name in names:
        data = (directory / name).read_bytes()
        manifest["lengths"][name] = len(data)
        manifest["sha256"][name] = hashlib.sha256(data).hexdigest()
    manifest["logical_bytes"] = sum(manifest["lengths"].values())
    manifest_path.write_text(
        json.dumps(manifest, sort_keys=True, separators=(",", ":")), encoding="utf-8"
    )


def authenticate_offsets(directory):
    directory = Path(directory)
    manifest = json.loads((directory / "manifest.json").read_text(encoding="utf-8"))
    offsets_raw = (directory / "offsets.bin").read_bytes()
    transcript = (directory / "transcript.bin").read_bytes()
    assert hashlib.sha256(offsets_raw).hexdigest() == manifest["sha256"]["offsets.bin"]
    assert hashlib.sha256(transcript).hexdigest() == manifest["sha256"]["transcript.bin"]
    offsets = [value[0] for value in struct.iter_unpack("<Q", offsets_raw)]
    assert offsets[0] == 0 and offsets[-1] == len(transcript) and len(offsets) == manifest["offers"] + 1
    return manifest, offsets, transcript


def mutate_future_pair(directory):
    directory = Path(directory)
    _, offsets, original = authenticate_offsets(directory)
    transcript = bytearray(original)
    accepted_before = 0
    for index in range(len(offsets) - 1):
        header = RECORD.unpack_from(transcript, offsets[index])
        if header[-1]:
            pair_offset = offsets[index] + RECORD.size
            transcript[pair_offset : pair_offset + 2] = encode_pair(accepted_before, 1)
            break
        if header[2] == ACC:
            accepted_before += 1
    else:
        raise AssertionError("no_reduction_record")
    (directory / "transcript.bin").write_bytes(transcript)
    rehash(directory, ["transcript.bin"])


def mutate_lead_id_swap(directory):
    directory = Path(directory)
    leads = bytearray((directory / "leads.bin").read_bytes())
    assert len(leads) >= 32
    first_id = struct.unpack_from("<Q", leads, 8)[0]
    second_id = struct.unpack_from("<Q", leads, 24)[0]
    assert first_id and second_id and first_id != second_id
    struct.pack_into("<Q", leads, 8, second_id)
    struct.pack_into("<Q", leads, 24, first_id)
    (directory / "leads.bin").write_bytes(leads)
    rehash(directory, ["leads.bin"])


def mutate_offset_interval(directory):
    directory = Path(directory)
    _, offsets, _ = authenticate_offsets(directory)
    assert offsets[0] < offsets[1] + 1 < offsets[2]
    data = bytearray((directory / "offsets.bin").read_bytes())
    struct.pack_into("<Q", data, 8, offsets[1] + 1)
    (directory / "offsets.bin").write_bytes(data)
    rehash(directory, ["offsets.bin"])


def mutate_record_and_leads_lead(directory, width=8):
    directory = Path(directory)
    _, offsets, original = authenticate_offsets(directory)
    transcript = bytearray(original)
    for index in range(len(offsets) - 1):
        start = offsets[index]
        fields = list(RECORD.unpack_from(transcript, start))
        if fields[2] == ACC:
            old_lead = fields[6]
            new_lead = (old_lead + 1) % width
            assert new_lead != old_lead
            fields[6] = new_lead
            transcript[start : start + RECORD.size] = RECORD.pack(*fields)
            leads = bytearray((directory / "leads.bin").read_bytes())
            struct.pack_into("<Q", leads, 0, new_lead)
            (directory / "transcript.bin").write_bytes(transcript)
            (directory / "leads.bin").write_bytes(leads)
            rehash(directory, ["transcript.bin", "leads.bin"])
            return
    raise AssertionError("no_accepted_record")


def mutation_gate(exe, campaign_path, work_root):
    expected = dense_image(campaign_path)
    base = Path(work_root) / "mutation_base"
    result = run_wrapper(exe, base, campaign_path)
    assert result.returncode == 0, result.stderr
    parse_state(base, expected)
    cases = (
        ("future_pair", mutate_future_pair, "future_pivot"),
        ("lead_id_swap", mutate_lead_id_swap, "lead_binding"),
        ("offset_interval", mutate_offset_interval, "record_offset_binding"),
        ("record_basis_lead", mutate_record_and_leads_lead, "basis_binding"),
    )
    outcomes = {}
    for name, mutation, reason in cases:
        control = Path(work_root) / f"control_{name}"
        shutil.copytree(base, control)
        clean = run_wrapper(exe, control, campaign_path)
        assert clean.returncode == 0, (name, clean.stderr)
        parse_state(control, expected)
        for filename in (*expected["streams"].keys(), "manifest.json"):
            assert (control / filename).read_bytes() == (base / filename).read_bytes()

        mutant = Path(work_root) / f"mutant_{name}"
        shutil.copytree(base, mutant)
        mutation(mutant)
        rejected = run_wrapper(exe, mutant, campaign_path)
        assert rejected.returncode != 0, name
        assert reason in rejected.stderr, (name, reason, rejected.stderr)
        outcomes[name] = reason
    return {"clean_resume_controls": 4, "isolated_rejections": outcomes}


def terminal_response(client, expected_status, expected_id, expected_exit):
    response = read_response(client, width=4, companion_width=0, rank_cap=2)
    assert response == {
        "status": expected_status,
        "id": expected_id,
        "offers": 0,
        "accepted": 0,
        "pivot": 0,
        "lead": 0,
        "lc": 0,
        "scale": 0,
        "pairs": [],
        "primary": b"",
        "companion": b"",
        "pn": 0,
        "cn": 0,
    }
    client.expect_eof()
    client.finish(expected_exit)


def raw_partial_header_gate(exe, work_root):
    valid = WIRE.pack(MAGIC_REQ, VERSION, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    assert len(valid) == 88
    for length in range(1, 88):
        client = launch(
            exe,
            Path(work_root) / f"partial_{length:02d}",
            width=4,
            companion_width=0,
            rank_cap=2,
        )
        try:
            client.write(valid[:length])
            client.close_stdin()
            client.expect_eof()
            client.finish(6)
        finally:
            client.abort()
    return {"lengths": [1, 87], "cases": 87, "terminal_exit": 6}


def raw_terminal_gate(exe, work_root):
    malformed = launch(
        exe, Path(work_root) / "malformed", width=4, companion_width=0, rank_cap=2
    )
    try:
        header = WIRE.pack(MAGIC_REQ, VERSION, 4, 0, 0, 41, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        malformed.write(header)
        terminal_response(malformed, MAL, 41, 6)
    finally:
        malformed.abort()

    noncanonical = launch(
        exe, Path(work_root) / "noncanonical", width=4, companion_width=0, rank_cap=2
    )
    try:
        header = WIRE.pack(MAGIC_REQ, VERSION, 1, 0, 0, 42, 0, 0, 0, 0, 0, 0, 0, 1, 0)
        noncanonical.write(header + bytes([81]))
        terminal_response(noncanonical, MAL, 42, 6)
    finally:
        noncanonical.abort()
    return {"malformed": "MALFORMED_EOF_EXIT6", "noncanonical": "MALFORMED_EOF_EXIT6"}


def allocation_fatal_gate(test_exe, work_root):
    client = launch(
        test_exe,
        Path(work_root) / "allocation_fatal",
        width=4,
        companion_width=0,
        rank_cap=2,
    )
    try:
        header = WIRE.pack(MAGIC_REQ, VERSION, 1, 0, 0, 43, 0, 0, 0, 0, 0, 0, 0, 1, 0)
        client.write(header + pack_trits([1, 0, 0, 0]))
        terminal_response(client, FATAL, 43, 6)
    finally:
        client.abort()
    return "TEST_ONLY_FATAL_EOF_EXIT6"


def fragmented_request_gate(exe, work_root):
    client = launch(
        exe,
        Path(work_root) / "fragmented_request",
        width=4,
        companion_width=0,
        rank_cap=2,
    )
    try:
        response = send_offer(
            client,
            1,
            0,
            0,
            pack_trits([1, 0, 0, 0]),
            b"",
            width=4,
            companion_width=0,
            rank_cap=2,
            fragments=True,
        )
        assert response["status"] == ACC and (response["offers"], response["accepted"]) == (1, 1)
        close_clean(client, 1, 1)
    finally:
        client.abort()
    return {"frame_bytes": 89, "fragments": 89, "result": "ACCEPTED_CLOSED"}


def owner_transport_fixture_gate():
    owner = load_owner_module()
    assert len(owner.FIRST_TRIT) == 81
    for value in range(81):
        digits = [(value // (3 ** index)) % 3 for index in range(4)]
        assert owner.FIRST_TRIT[value] == next(
            (index for index, digit in enumerate(digits) if digit), 4
        )
    assert owner._canonical_bytes(bytes([0, 3, 80]))
    assert not owner._canonical_bytes(bytes([81]))

    def harness(code):
        process = subprocess.Popen(
            [sys.executable, "-u", "-c", code],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        )
        session = owner.OwnerSession.__new__(owner.OwnerSession)
        session.proc = process
        session._streams = {}
        session._pump_queue = None
        session._pump_thread = None
        session._pump_buffer = bytearray()
        session._poisoned = False
        session._closed = False
        session._cleaning = False
        session._start_pump()
        return session

    fragmented_code = (
        "import os,time\n"
        "data=b'F'*88\n"
        "for a,b in ((0,1),(1,8),(8,31),(31,88)):\n"
        " os.write(1,data[a:b]); time.sleep(0.02)\n"
    )
    fragmented = harness(fragmented_code)
    assert fragmented._read_exact(88, time.monotonic() + 2) == b"F" * 88
    fragmented._poison()
    assert fragmented.proc.poll() is not None and not fragmented._pump_thread.is_alive()

    stalled = harness("import time; time.sleep(30)\n")
    start = time.monotonic()
    try:
        stalled._read_exact(1, time.monotonic() + 0.2)
        raise AssertionError("stalled_response_accepted")
    except owner.ProtocolError as exc:
        assert str(exc) == "response_deadline"
    assert time.monotonic() - start < 5
    assert stalled._poisoned and stalled._closed and stalled.proc.poll() is not None
    assert not stalled._pump_thread.is_alive()
    try:
        stalled._read_exact(1, time.monotonic() + 0.2)
        raise AssertionError("poison_reuse")
    except owner.NotReady as exc:
        assert str(exc) == "session_poisoned"

    short = harness("import os; os.write(1,b'S'*17)\n")
    try:
        short._read_exact(88, time.monotonic() + 2)
        raise AssertionError("short_response_accepted")
    except owner.ProtocolError as exc:
        assert str(exc) == "service_eof"
    assert short._poisoned and short._closed and short.proc.poll() is not None
    assert not short._pump_thread.is_alive()
    return {
        "packed_first_table_81": "PASS",
        "fragmented_response": "PASS",
        "stalled_response": "DEADLINE_POISON_REAP_CLOSE_JOIN",
        "short_response": "EOF_POISON_REAP_CLOSE_JOIN",
        "poison_reuse": "REJECTED",
    }


def static_source_gate():
    c_text = C_SOURCE.read_text(encoding="utf-8")
    py_text = WRAPPER.read_text(encoding="utf-8")
    assert "SUB[coefficient][left][right]" in c_text
    assert "free(q)" not in c_text
    assert "while (done < n)" in c_text
    assert "#ifdef EOW_TEST_FAIL_ACCEPT_ALLOC" in c_text
    assert "read1(65536)" in py_text
    assert "response_deadline=None" in py_text
    assert "FIRST_TRIT" in py_text and "ExitStack" in py_text
    assert "MAX_WIDTH, MAX_COMPANION_WIDTH, MAX_RANK = 36288, 48384, 4095" in py_text
    assert "MAX_RANK 4095u" in c_text
    return "PASS"


def compile_worker(compiler, output, *, allocation_failpoint=False):
    is_msvc = Path(compiler).name.lower() in ("cl", "cl.exe")
    if is_msvc:
        command = [compiler, "/nologo", "/std:c11", "/W4", "/WX", "/TC"]
        if allocation_failpoint:
            command.append("/DEOW_TEST_FAIL_ACCEPT_ALLOC=1")
        command += [str(C_SOURCE), "/Fe:" + str(output)]
    else:
        command = [compiler, "-std=c11", "-O2", "-Wall", "-Wextra", "-Werror", "-pedantic"]
        if allocation_failpoint:
            command.append("-DEOW_TEST_FAIL_ACCEPT_ALLOC=1")
        command += [str(C_SOURCE), "-o", str(output)]
    try:
        result = subprocess.run(
            command,
            cwd=output.parent,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=60,
        )
    except subprocess.TimeoutExpired as exc:
        raise AssertionError("compile_deadline") from exc
    assert result.returncode == 0, result.stdout + result.stderr
    assert output.is_file()
    return command


def main():
    started = time.perf_counter()
    report = {
        "version": VERSION,
        "production": False,
        "verified": False,
        "wire_header_bytes": WIRE.size,
        "record_header_bytes": RECORD.size,
        "rank_contract": MAX_RANK,
        "grade1_rank_8059_adapter": "OUT_OF_SCOPE",
        "static_source": static_source_gate(),
    }
    transport = owner_transport_fixture_gate()
    report["owner_transport_fixtures"] = transport
    with tempfile.TemporaryDirectory(prefix="d972-v10-check-") as temporary:
        work_root = Path(temporary)
        campaign_path = work_root / "campaign.json"
        write_campaign(campaign_path)
        expected = dense_image(campaign_path)
        coefficient_one = expected["results"][4]
        assert coefficient_one["status"] == DEP
        assert coefficient_one["reductions"] == [(0, 1), (1, 1)]
        report.update(
            {
                "dense_reference": "PASS",
                "dense_coefficient_one_witness": "ID5_DEPENDENT_AFTER_C1_C1",
                "offers": len(expected["results"]),
                "accepted_reference": len(expected["accepted_ids"]),
                "expected_stream_sha256": {
                    name: hashlib.sha256(data).hexdigest()
                    for name, data in expected["streams"].items()
                },
            }
        )
        compiler = next(
            (shutil.which(name) for name in ("cc", "gcc", "clang", "cl") if shutil.which(name)),
            None,
        )
        if compiler is None:
            report["compiler"] = "NONE"
            for key in (
                "strict_compile",
                "compiled_campaign",
                "coefficient_one_cancellation",
                "five_stream_image",
                "literal_stats_closed_eof",
                "caps",
                "partial_headers_1_87",
                "terminal_malformed_noncanonical",
                "allocation_fatal_test_binary",
                "fragmented_request",
                "hard_kill_provisional",
                "suffix_resume",
                "semantic_mutations",
                "cursor_finalize",
                "interoperability",
            ):
                report[key] = "NOT_RUN_NO_COMPILER"
        else:
            report["compiler"] = compiler
            production_exe = work_root / ("worker.exe" if os.name == "nt" else "worker")
            fail_exe = work_root / ("worker_fail.exe" if os.name == "nt" else "worker_fail")
            production_command = compile_worker(compiler, production_exe)
            fail_command = compile_worker(compiler, fail_exe, allocation_failpoint=True)
            report["strict_compile"] = {
                "production": production_command,
                "test_only_allocation": fail_command,
                "production_failpoint_define": "ABSENT",
            }
            direct = direct_campaign(production_exe, campaign_path, work_root)
            cancellation = coefficient_one_cancellation_gate(production_exe, work_root)
            caps = cap_gate(production_exe, work_root)
            durable = durable_cursor_gate(production_exe, campaign_path, work_root)
            mutations = mutation_gate(production_exe, campaign_path, work_root)
            partial = raw_partial_header_gate(production_exe, work_root)
            terminal = raw_terminal_gate(production_exe, work_root)
            allocation = allocation_fatal_gate(fail_exe, work_root)
            fragmented_request = fragmented_request_gate(production_exe, work_root)
            report.update(
                {
                    "compiled_campaign": direct,
                    "coefficient_one_cancellation": cancellation,
                    "five_stream_image": durable["five_stream_whole_byte_image"],
                    "literal_stats_closed_eof": "PASS",
                    "caps": caps,
                    "partial_headers_1_87": partial,
                    "terminal_malformed_noncanonical": terminal,
                    "allocation_fatal_test_binary": allocation,
                    "fragmented_request": fragmented_request,
                    "hard_kill_provisional": durable["hard_kill"],
                    "suffix_resume": durable["suffix_resume_from_id5"],
                    "semantic_mutations": mutations,
                    "cursor_finalize": durable["cursor_finalize"],
                    "interoperability": "PASS",
                }
            )
    report["seconds"] = round(time.perf_counter() - started, 6)
    print(json.dumps(report, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
