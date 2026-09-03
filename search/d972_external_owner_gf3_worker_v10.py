"""External-owner GF(3) v10 client and durable owner."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import queue
import struct
import subprocess
import threading
import time
from contextlib import ExitStack
from pathlib import Path

HEADER = struct.Struct("<4sBBBB10Q")
REC_HEADER = struct.Struct("<4sBBH6Q")
MAGIC_REQ, MAGIC_RESP, REC_MAGIC = b"EORA", b"EOWA", b"EOTA"
VERSION, SCHEMA = 10, "external-owner-v10"
MAX_WIDTH, MAX_COMPANION_WIDTH, MAX_RANK = 36288, 48384, 4095
DEPENDENT, ACCEPTED, UNKNOWN_RESOURCE, MALFORMED, FATAL, STATS, CLOSED = range(7)
_WEIGHTS = (1, 3, 9, 27)
FIRST_TRIT = tuple(
    next((index for index, weight in enumerate(_WEIGHTS) if (value // weight) % 3), 4)
    for value in range(81)
)
_NONCANONICAL = bytes(0 if value <= 80 else 1 for value in range(256))


class ProtocolError(ValueError):
    pass


class NotReady(RuntimeError):
    pass


def _write_file_exact(path, data):
    with Path(path).open("wb") as stream:
        done = 0
        while done < len(data):
            count = stream.write(data[done:])
            if not count:
                raise ProtocolError("short_file_write")
            done += count
        stream.flush()
        os.fsync(stream.fileno())


def _canonical_bytes(data):
    return 1 not in data.translate(_NONCANONICAL)


def packed(value, size):
    try:
        view = memoryview(value).cast("B")
    except (TypeError, ValueError) as exc:
        raise ProtocolError("packed_type") from exc
    if view.ndim != 1 or view.nbytes != size:
        raise ProtocolError("packed_row")
    raw = view.tobytes()
    if not _canonical_bytes(raw):
        raise ProtocolError("packed_row")
    return raw


def pair_code(pivot, coefficient, rank_cap):
    if type(pivot) is not int or not 0 <= pivot < rank_cap or coefficient not in (1, 2):
        raise ProtocolError("pair")
    return struct.pack("<H", 2 * pivot + coefficient - 1)


def decode_pairs(data, rank_cap):
    if len(data) & 1:
        raise ProtocolError("pair_bytes")
    out = []
    for offset in range(0, len(data), 2):
        code = struct.unpack_from("<H", data, offset)[0]
        pivot, remainder = divmod(code, 2)
        if pivot >= rank_cap or remainder not in (0, 1):
            raise ProtocolError("pair")
        out.append((pivot, remainder + 1))
    return out


def first_lead(row, width):
    for byte_index, value in enumerate(row):
        if value:
            return byte_index * 4 + FIRST_TRIT[value]
    return width


def lead_coefficient(row, lead):
    if type(lead) is not int or lead < 0:
        raise ProtocolError("lead")
    return (row[lead // 4] // _WEIGHTS[lead % 4]) % 3


def _u64(value, name):
    if type(value) is not int or not 0 <= value < 1 << 64:
        raise ProtocolError(name)
    return value


def _product(a, b, name):
    if type(a) is not int or type(b) is not int or a < 0 or b < 0 or a * b >= 1 << 64:
        raise ProtocolError(name)
    return a * b


class OwnerSession:
    def __init__(
        self,
        exe,
        directory,
        *,
        width,
        rank_cap,
        offer_cap,
        byte_cap,
        companion_width=0,
        session=0,
        parent_id=0,
        input_id=0,
        response_deadline=None,
    ):
        if (
            type(width) is not int
            or not 0 < width <= MAX_WIDTH
            or width % 4
            or type(companion_width) is not int
            or not 0 <= companion_width <= MAX_COMPANION_WIDTH
            or companion_width % 4
        ):
            raise ProtocolError("width")
        if (
            type(rank_cap) is not int
            or not 0 < rank_cap <= MAX_RANK
            or type(offer_cap) is not int
            or not 0 < offer_cap < 1 << 64
            or type(byte_cap) is not int
            or not 0 < byte_cap < 1 << 64
        ):
            raise ProtocolError("caps")
        if response_deadline is not None and (
            isinstance(response_deadline, bool)
            or not isinstance(response_deadline, (int, float))
            or not math.isfinite(response_deadline)
            or response_deadline <= 0
        ):
            raise ProtocolError("response_deadline")
        self.exe, self.d = Path(exe), Path(directory)
        if not self.exe.is_file():
            raise NotReady("compiled_worker_missing")
        self.width, self.companion_width = width, companion_width
        self.p, self.cp = width // 4, companion_width // 4
        self.rank_cap, self.offer_cap, self.byte_cap = rank_cap, offer_cap, byte_cap
        self.session, self.parent_id, self.input_id = (
            _u64(session, "session"),
            _u64(parent_id, "parent_id"),
            _u64(input_id, "input_id"),
        )
        self.response_deadline = response_deadline
        self.d.mkdir(parents=True, exist_ok=True)
        self.manifest_path = self.d / "manifest.json"
        self.names = ["basis.bin"] + (["companion.bin"] if self.cp else []) + [
            "transcript.bin",
            "offsets.bin",
            "leads.bin",
        ]
        self._paths = {name: self.d / name for name in self.names}
        self._digest, self._lengths, self._streams = {}, {}, {}
        self.generation = self.offers = self.accepted = self.logical_bytes = self.last_id = 0
        self._accepted_ids = []
        self.proc = None
        self._pump_queue = None
        self._pump_thread = None
        self._pump_buffer = bytearray()
        self._poisoned = False
        self._closed = False
        self._cleaning = False
        try:
            if self.manifest_path.exists():
                self._resume_manifest()
            else:
                self._fresh_state()
            self._open_streams()
            self._launch()
            self._stats_check()
        except BaseException:
            self._poison()
            raise

    def _fresh_state(self):
        for path in self._paths.values():
            if path.exists() and path.stat().st_size:
                raise ProtocolError("unmanifested_state")
            path.touch()
        _write_file_exact(self._paths["offsets.bin"], struct.pack("<Q", 0))
        for path in self._paths.values():
            with path.open("ab") as stream:
                stream.flush()
                os.fsync(stream.fileno())
        self._lengths = {name: self._paths[name].stat().st_size for name in self.names}
        self._digest = {
            name: self._digest_prefix(self._paths[name], self._lengths[name])
            for name in self.names
        }
        self.logical_bytes = sum(self._lengths.values())
        if self.logical_bytes > self.byte_cap:
            raise ProtocolError("byte_cap")
        self._publish_manifest()

    def _digest_prefix(self, path, length):
        digest = hashlib.sha256()
        left = length
        with path.open("rb") as stream:
            while left:
                block = stream.read(min(1 << 20, left))
                if not block:
                    raise ProtocolError("short_committed_file")
                digest.update(block)
                left -= len(block)
        return digest

    def _resume_manifest(self):
        try:
            manifest = json.loads(self.manifest_path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            raise ProtocolError("invalid_manifest") from exc
        required = {
            "version",
            "schema",
            "session",
            "parent_id",
            "input_id",
            "width",
            "companion_width",
            "rank_cap",
            "offer_cap",
            "byte_cap",
            "generation",
            "offers",
            "accepted",
            "logical_bytes",
            "last_id",
            "lengths",
            "sha256",
        }
        if set(manifest) != required or manifest["version"] != VERSION or manifest["schema"] != SCHEMA:
            raise ProtocolError("manifest_schema")
        for key in (
            "session",
            "parent_id",
            "input_id",
            "width",
            "companion_width",
            "rank_cap",
            "offer_cap",
            "byte_cap",
            "generation",
            "offers",
            "accepted",
            "logical_bytes",
            "last_id",
        ):
            _u64(manifest[key], "manifest_scalar")
        if (
            not 0 < manifest["width"] <= MAX_WIDTH
            or manifest["width"] % 4
            or manifest["companion_width"] > MAX_COMPANION_WIDTH
            or manifest["companion_width"] % 4
            or not 0 < manifest["rank_cap"] <= MAX_RANK
        ):
            raise ProtocolError("manifest_config")
        mine = (
            self.session,
            self.parent_id,
            self.input_id,
            self.width,
            self.companion_width,
            self.rank_cap,
            self.offer_cap,
            self.byte_cap,
        )
        got = (
            manifest["session"],
            manifest["parent_id"],
            manifest["input_id"],
            manifest["width"],
            manifest["companion_width"],
            manifest["rank_cap"],
            manifest["offer_cap"],
            manifest["byte_cap"],
        )
        if (
            got != mine
            or manifest["offers"] > self.offer_cap
            or manifest["accepted"] > self.rank_cap
            or manifest["accepted"] > manifest["offers"]
            or manifest["logical_bytes"] > self.byte_cap
        ):
            raise ProtocolError("manifest_binding")
        if (
            type(manifest["lengths"]) is not dict
            or type(manifest["sha256"]) is not dict
            or set(manifest["lengths"]) != set(self._paths)
            or set(manifest["sha256"]) != set(self._paths)
        ):
            raise ProtocolError("manifest_files")
        for name in self.names:
            length = manifest["lengths"][name]
            if type(length) is not int or not 0 <= length < 1 << 64:
                raise ProtocolError("manifest_length_scalar")
        if (
            manifest["lengths"]["offsets.bin"]
            != _product(manifest["offers"] + 1, 8, "offset_count")
            or manifest["lengths"]["basis.bin"]
            != _product(manifest["accepted"], self.p, "basis_length")
            or manifest["lengths"]["leads.bin"]
            != _product(manifest["accepted"], 16, "leads_length")
            or (
                self.cp
                and manifest["lengths"]["companion.bin"]
                != _product(manifest["accepted"], self.cp, "companion_length")
            )
        ):
            raise ProtocolError("state_length")
        if sum(manifest["lengths"].values()) != manifest["logical_bytes"]:
            raise ProtocolError("logical_bytes")
        if not all(
            self._paths[name].exists()
            and self._paths[name].stat().st_size >= manifest["lengths"][name]
            for name in self.names
        ):
            raise ProtocolError("manifest_file_missing")
        for name in self.names:
            length = manifest["lengths"][name]
            digest = self._digest_prefix(self._paths[name], length)
            if digest.hexdigest() != manifest["sha256"][name]:
                raise ProtocolError("committed_corruption")
            self._digest[name], self._lengths[name] = digest, length
        self._parse_prefix(manifest)
        for name in self.names:
            with self._paths[name].open("r+b") as stream:
                stream.truncate(self._lengths[name])
        self.generation = manifest["generation"]

    @staticmethod
    def _take(stream, length, reason):
        data = stream.read(length)
        if len(data) != length:
            raise ProtocolError(reason)
        return data

    def _parse_prefix(self, manifest):
        transcript_length = self._lengths["transcript.bin"]
        if self._lengths["offsets.bin"] != _product(manifest["offers"] + 1, 8, "offset_count"):
            raise ProtocolError("offset_count")
        if (
            self._lengths["basis.bin"] != _product(manifest["accepted"], self.p, "basis_length")
            or self._lengths["leads.bin"]
            != _product(manifest["accepted"], 16, "leads_length")
            or (
                self.cp
                and self._lengths["companion.bin"]
                != _product(manifest["accepted"], self.cp, "companion_length")
            )
        ):
            raise ProtocolError("state_length")
        self.offers = self.accepted = 0
        self.last_id = 0
        self._accepted_ids = []
        with ExitStack() as stack:
            transcript = stack.enter_context(self._paths["transcript.bin"].open("rb"))
            offsets = stack.enter_context(self._paths["offsets.bin"].open("rb"))
            basis = stack.enter_context(self._paths["basis.bin"].open("rb"))
            companion = (
                stack.enter_context(self._paths["companion.bin"].open("rb")) if self.cp else None
            )
            leads = stack.enter_context(self._paths["leads.bin"].open("rb"))
            origin = self._take(offsets, 8, "offset_origin")
            if struct.unpack("<Q", origin)[0] != 0:
                raise ProtocolError("offset_origin")
            previous = 0
            for _ in range(manifest["offers"]):
                start = transcript.tell()
                header = self._take(transcript, REC_HEADER.size, "record_header")
                magic, version, status, reserved, oid, pivot, lead, lc, scale, nq = REC_HEADER.unpack(header)
                if (
                    magic != REC_MAGIC
                    or version != VERSION
                    or reserved
                    or oid == 0
                    or (self.offers and oid <= self.last_id)
                ):
                    raise ProtocolError("record_binding")
                if nq > self.rank_cap:
                    raise ProtocolError("record_count")
                pair_bytes = self._take(transcript, _product(nq, 2, "record_pairs"), "record_count")
                pairs = decode_pairs(pair_bytes, self.rank_cap)
                if any(pair_pivot >= self.accepted for pair_pivot, _ in pairs):
                    raise ProtocolError("future_pivot")
                current = struct.unpack("<Q", self._take(offsets, 8, "offset_short"))[0]
                if (
                    start != previous
                    or current < previous
                    or current != transcript.tell()
                    or current > transcript_length
                ):
                    raise ProtocolError("record_offset_binding")
                previous = current
                if status == DEPENDENT:
                    if any((pivot, lead, lc, scale)):
                        raise ProtocolError("dependent_meta")
                elif status == ACCEPTED:
                    if (
                        pivot != self.accepted
                        or not 0 <= lead < self.width
                        or lc not in (1, 2)
                        or scale != lc
                    ):
                        raise ProtocolError("accepted_meta")
                    row = self._take(basis, self.p, "basis_binding")
                    if (
                        not _canonical_bytes(row)
                        or first_lead(row, self.width) != lead
                        or lead_coefficient(row, lead) != 1
                    ):
                        raise ProtocolError("basis_binding")
                    if self.cp:
                        companion_row = self._take(companion, self.cp, "companion_binding")
                        if not _canonical_bytes(companion_row):
                            raise ProtocolError("companion_binding")
                    lead_record = self._take(leads, 16, "lead_binding")
                    if struct.unpack("<QQ", lead_record) != (lead, oid):
                        raise ProtocolError("lead_binding")
                    self._accepted_ids.append(oid)
                    self.accepted += 1
                else:
                    raise ProtocolError("record_status")
                self.offers += 1
                self.last_id = oid
            declared_positions = {
                "transcript.bin": transcript.tell(),
                "offsets.bin": offsets.tell(),
                "basis.bin": basis.tell(),
                "leads.bin": leads.tell(),
            }
            if self.cp:
                declared_positions["companion.bin"] = companion.tell()
            if any(declared_positions[name] != self._lengths[name] for name in self.names):
                raise ProtocolError("declared_eof")
            if previous != transcript_length:
                raise ProtocolError("offset_eof")
        if (self.offers, self.accepted, self.last_id) != (
            manifest["offers"],
            manifest["accepted"],
            manifest["last_id"],
        ):
            raise ProtocolError("record_counts")
        self.logical_bytes = sum(self._lengths.values())
        if self.logical_bytes != manifest["logical_bytes"]:
            raise ProtocolError("logical_bytes")

    def _open_streams(self):
        self._streams = {name: self._paths[name].open("ab") for name in self.names}

    def _launch(self):
        args = [
            str(self.exe),
            "--serve",
            "--width",
            str(self.width),
            "--companion-width",
            str(self.companion_width),
            "--rank-cap",
            str(self.rank_cap),
            "--offer-cap",
            str(self.offer_cap),
            "--byte-cap",
            str(self.byte_cap),
            "--session",
            str(self.session),
            "--committed-offers",
            str(self.offers),
            "--committed-accepted",
            str(self.accepted),
            "--logical-bytes",
            str(self.logical_bytes),
            "--basis",
            str(self._paths["basis.bin"]),
            "--leads",
            str(self._paths["leads.bin"]),
        ]
        if self.cp:
            args += ["--companion", str(self._paths["companion.bin"])]
        self.proc = subprocess.Popen(
            args,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=None,
        )
        self._start_pump()

    def _start_pump(self):
        self._pump_queue = queue.Queue()
        self._pump_buffer = bytearray()

        def pump():
            try:
                while True:
                    if hasattr(self.proc.stdout, "read1"):
                        chunk = self.proc.stdout.read1(65536)
                    else:
                        chunk = os.read(self.proc.stdout.fileno(), 65536)
                    if not chunk:
                        self._pump_queue.put(None)
                        return
                    self._pump_queue.put(chunk)
            except BaseException as exc:
                self._pump_queue.put(exc)

        self._pump_thread = threading.Thread(target=pump, name="eow-v10-stdout", daemon=True)
        self._pump_thread.start()

    def _absolute_deadline(self):
        return None if self.response_deadline is None else time.monotonic() + self.response_deadline

    def _ensure_usable(self):
        if self._poisoned:
            raise NotReady("session_poisoned")
        if self._closed:
            raise NotReady("session_closed")
        if self.proc is None or self.proc.poll() is not None:
            self._poison()
            raise NotReady("service_stopped")

    def _read_exact(self, length, absolute_deadline=None):
        if self._poisoned:
            raise NotReady("session_poisoned")
        while len(self._pump_buffer) < length:
            timeout = None
            if absolute_deadline is not None:
                timeout = absolute_deadline - time.monotonic()
                if timeout <= 0:
                    self._poison()
                    raise ProtocolError("response_deadline")
            try:
                item = self._pump_queue.get(timeout=timeout)
            except queue.Empty as exc:
                self._poison()
                raise ProtocolError("response_deadline") from exc
            if item is None:
                self._poison()
                raise ProtocolError("service_eof")
            if isinstance(item, BaseException):
                self._poison()
                raise ProtocolError("service_reader") from item
            self._pump_buffer.extend(item)
        data = bytes(self._pump_buffer[:length])
        del self._pump_buffer[:length]
        return data

    def _expect_eof(self, absolute_deadline=None):
        if self._pump_buffer:
            raise ProtocolError("trailing_response")
        timeout = None
        if absolute_deadline is not None:
            timeout = absolute_deadline - time.monotonic()
            if timeout <= 0:
                raise ProtocolError("response_deadline")
        try:
            item = self._pump_queue.get(timeout=timeout)
        except queue.Empty as exc:
            raise ProtocolError("response_deadline") from exc
        if item is None:
            return
        if isinstance(item, BaseException):
            raise ProtocolError("service_reader") from item
        raise ProtocolError("trailing_response")

    def _close_streams(self):
        streams, self._streams = self._streams, {}
        for stream in streams.values():
            try:
                stream.flush()
            except Exception:
                pass
            try:
                stream.close()
            except Exception:
                pass

    def _shutdown(self, force):
        if self._cleaning:
            return
        self._cleaning = True
        try:
            proc = self.proc
            if proc is not None:
                if force and proc.poll() is None:
                    try:
                        proc.kill()
                    except Exception:
                        pass
                if proc.stdin is not None:
                    try:
                        proc.stdin.close()
                    except Exception:
                        pass
                if force and proc.poll() is None:
                    try:
                        proc.kill()
                    except Exception:
                        pass
                try:
                    proc.wait()
                except Exception:
                    pass
                if proc.stdout is not None:
                    try:
                        proc.stdout.close()
                    except Exception:
                        pass
            if self._pump_thread is not None and self._pump_thread is not threading.current_thread():
                self._pump_thread.join()
            self._close_streams()
            self._closed = True
        finally:
            self._cleaning = False

    def _poison(self):
        self._poisoned = True
        self._shutdown(force=True)

    def _request(self, op, oid=0, row=None, companion=None):
        self._ensure_usable()
        pn, cn = (self.p, self.cp) if op == 1 else (0, 0)
        payload = (row if row is not None else b"") + (companion if companion is not None else b"")
        if len(payload) != pn + cn:
            raise ProtocolError("request_length")
        wire = HEADER.pack(
            MAGIC_REQ,
            VERSION,
            op,
            0,
            0,
            oid,
            self.offers,
            self.accepted,
            0,
            0,
            0,
            0,
            0,
            pn,
            cn,
        )
        if len(wire) != HEADER.size:
            raise ProtocolError("request_header_length")
        data = wire + payload
        deadline = self._absolute_deadline()
        try:
            done = 0
            while done < len(data):
                count = self.proc.stdin.write(data[done:])
                if not count:
                    raise ProtocolError("short_request_write")
                done += count
            self.proc.stdin.flush()
            unpacked = HEADER.unpack(self._read_exact(HEADER.size, deadline))
            magic, version, status, flags, reserved, *values = unpacked
            if (magic, version, flags, reserved) != (MAGIC_RESP, VERSION, 0, 0):
                raise ProtocolError("response_header")
            rid, offers, accepted, pivot, lead, lc, scale, nq, response_pn, response_cn = values
            if (
                rid != oid
                or offers < self.offers
                or accepted < self.accepted
                or status not in range(7)
            ):
                raise ProtocolError("response_counts")
            if status in (UNKNOWN_RESOURCE, MALFORMED, FATAL) and (
                offers != self.offers
                or accepted != self.accepted
                or any((pivot, lead, lc, scale, nq, response_pn, response_cn))
            ):
                raise ProtocolError("terminal_fields")
            if status in (STATS, CLOSED) and (
                rid != 0 or any((pivot, lead, lc, scale, nq, response_pn, response_cn))
            ):
                raise ProtocolError("control_fields")
            if nq > self.rank_cap or response_pn > self.p or response_cn > self.cp:
                raise ProtocolError("response_length_bound")
            if status == DEPENDENT and (response_pn != 0 or response_cn != self.cp):
                raise ProtocolError("dependent_lengths")
            if status == ACCEPTED and (response_pn != self.p or response_cn != self.cp):
                raise ProtocolError("accepted_lengths")
            body = self._read_exact(2 * nq + response_pn + response_cn, deadline)
            packed_body = body[2 * nq :]
            if not _canonical_bytes(packed_body):
                raise ProtocolError("packed_response")
            return (
                status,
                rid,
                offers,
                accepted,
                pivot,
                lead,
                lc,
                scale,
                decode_pairs(body[: 2 * nq], self.rank_cap),
                body[2 * nq : 2 * nq + response_pn],
                body[2 * nq + response_pn :],
            )
        except Exception as exc:
            self._poison()
            if isinstance(exc, ProtocolError):
                raise
            raise ProtocolError("service_io") from exc

    def offer(self, row_id, row, companion=None):
        self._ensure_usable()
        row = packed(row, self.p)
        if self.cp:
            companion = packed(companion, self.cp)
        elif companion is not None:
            raise ProtocolError("unexpected_companion")
        row_id = _u64(row_id, "row_id")
        if row_id == 0 or (self.offers and row_id <= self.last_id):
            raise ProtocolError("id_chronology")
        old_offers, old_accepted = self.offers, self.accepted
        result = self._request(1, row_id, row, companion)
        status, rid, offers, accepted, pivot, lead, lc, scale, pairs, primary, comp = result
        if status == UNKNOWN_RESOURCE:
            return {"status": "UNKNOWN_RESOURCE", "row_id": rid, "reductions": pairs}
        if status in (MALFORMED, FATAL):
            self._poison()
            raise ProtocolError("terminal_response")
        if (
            status not in (DEPENDENT, ACCEPTED)
            or offers != old_offers + 1
            or accepted not in (old_accepted, old_accepted + 1)
        ):
            self._poison()
            raise ProtocolError("offer_result")
        if any(pair_pivot >= old_accepted for pair_pivot, _ in pairs):
            self._poison()
            raise ProtocolError("future_pivot")
        if status == DEPENDENT:
            if any((pivot, lead, lc, scale)) or accepted != old_accepted or primary or len(comp) != self.cp:
                self._poison()
                raise ProtocolError("dependent_payload")
        elif (
            accepted != old_accepted + 1
            or pivot != old_accepted
            or not 0 <= lead < self.width
            or len(primary) != self.p
            or len(comp) != self.cp
            or lc not in (1, 2)
            or scale != lc
            or first_lead(primary, self.width) != lead
            or lead_coefficient(primary, lead) != 1
        ):
            self._poison()
            raise ProtocolError("accepted_payload")
        charge = 56 + 2 * len(pairs) + 8 + (self.p + self.cp + 16 if status == ACCEPTED else 0)
        if old_offers >= self.offer_cap or self.logical_bytes + charge > self.byte_cap:
            self._poison()
            raise ProtocolError("local_cap_mismatch")
        self._append_record(status, rid, pivot, lead, lc, scale, pairs, primary, comp, charge)
        return {
            "status": status,
            "row_id": rid,
            "reductions": pairs,
            "pivot": pivot,
            "lead": lead,
            "leading_coefficient": lc,
            "scale": scale,
            "normalized": primary,
            "companion": comp,
        }

    def _write(self, name, data):
        if not data:
            return
        done = 0
        while done < len(data):
            count = self._streams[name].write(data[done:])
            if not count:
                raise ProtocolError("short_durable_write")
            done += count
        self._streams[name].flush()
        self._digest[name].update(data)
        self._lengths[name] += len(data)

    def _append_record(self, status, oid, pivot, lead, lc, scale, pairs, primary, comp, charge):
        before = sum(self._lengths.values())
        record = REC_HEADER.pack(
            REC_MAGIC,
            VERSION,
            status,
            0,
            oid,
            pivot if status == ACCEPTED else 0,
            lead if status == ACCEPTED else 0,
            lc if status == ACCEPTED else 0,
            scale if status == ACCEPTED else 0,
            len(pairs),
        ) + b"".join(pair_code(pair_pivot, coefficient, self.rank_cap) for pair_pivot, coefficient in pairs)
        try:
            self._write("transcript.bin", record)
            self._write("offsets.bin", struct.pack("<Q", self._lengths["transcript.bin"]))
            if status == ACCEPTED:
                self._write("basis.bin", primary)
                if self.cp:
                    self._write("companion.bin", comp)
                self._write("leads.bin", struct.pack("<QQ", lead, oid))
                self._accepted_ids.append(oid)
            self.offers += 1
            self.last_id = oid
            self.accepted += status == ACCEPTED
            self.logical_bytes = sum(self._lengths.values())
            if self.logical_bytes != before + charge:
                raise ProtocolError("byte_charge")
        except BaseException:
            self._poison()
            raise

    def _stats_check(self):
        try:
            result = self._request(2)
            if result[0] != STATS or result[1] != 0 or result[2] != self.offers or result[3] != self.accepted:
                raise ProtocolError("stats_binding")
            if result[4:8] != (0, 0, 0, 0) or result[8] or result[9] or result[10]:
                raise ProtocolError("stats_binding")
        except BaseException:
            self._poison()
            raise

    def checkpoint(self):
        try:
            self._stats_check()
            for stream in self._streams.values():
                stream.flush()
                os.fsync(stream.fileno())
            self.generation += 1
            self._publish_manifest()
            return self.generation
        except BaseException:
            self._poison()
            raise

    def _manifest(self):
        return {
            "version": VERSION,
            "schema": SCHEMA,
            "session": self.session,
            "parent_id": self.parent_id,
            "input_id": self.input_id,
            "width": self.width,
            "companion_width": self.companion_width,
            "rank_cap": self.rank_cap,
            "offer_cap": self.offer_cap,
            "byte_cap": self.byte_cap,
            "generation": self.generation,
            "offers": self.offers,
            "accepted": self.accepted,
            "logical_bytes": self.logical_bytes,
            "last_id": self.last_id,
            "lengths": self._lengths.copy(),
            "sha256": {
                name: self._digest[name].copy().hexdigest() for name in self.names
            },
        }

    def _publish_manifest(self):
        data = json.dumps(self._manifest(), sort_keys=True, separators=(",", ":")).encode()
        temporary = self.d / "manifest.tmp"
        _write_file_exact(temporary, data)
        os.replace(temporary, self.manifest_path)
        if os.name != "nt":
            descriptor = os.open(self.d, os.O_RDONLY)
            try:
                os.fsync(descriptor)
            finally:
                os.close(descriptor)

    def cursor(self, origin_count, actor_order=(0, 1, 2, 3)):
        if type(origin_count) is not int or origin_count < 0 or tuple(actor_order) != (0, 1, 2, 3):
            raise ProtocolError("cursor_args")
        complete = self.offers >= origin_count
        if not complete:
            index = actor = next_pivot = next_source_id = None
            exhausted = False
        else:
            index, actor = divmod(self.offers - origin_count, 4)
            next_pivot = index if index < len(self._accepted_ids) else None
            next_source_id = self._accepted_ids[index] if index < len(self._accepted_ids) else None
            exhausted = index >= len(self._accepted_ids)
        next_id = None if self.last_id == (1 << 64) - 1 else self.last_id + 1
        if exhausted:
            next_pivot = next_source_id = actor = next_id = None
        return {
            "accepted_ids": tuple(self._accepted_ids),
            "origins_complete": complete,
            "next_pivot": next_pivot,
            "next_source_id": next_source_id,
            "next_actor_index": actor,
            "next_id": next_id,
            "fifo_exhausted": exhausted,
        }

    def finalize(self, origin_count):
        success = False
        result = None
        try:
            self._ensure_usable()
            result = self.cursor(origin_count)
            if (
                not result["origins_complete"]
                or self.offers != origin_count + 4 * self.accepted
                or not result["fifo_exhausted"]
            ):
                raise ProtocolError("finalize_incomplete")
            self._stats_check()
            closed = self._request(3)
            if (
                closed[0] != CLOSED
                or closed[1:8] != (0, self.offers, self.accepted, 0, 0, 0, 0)
                or closed[8]
                or closed[9]
                or closed[10]
            ):
                raise ProtocolError("closed_binding")
            self._expect_eof(self._absolute_deadline())
            if self.proc.wait(timeout=self.response_deadline) != 0:
                raise ProtocolError("service_exit")
            success = True
            return result
        finally:
            if success:
                self._shutdown(force=False)
            else:
                self._poison()


def load_campaign(path):
    try:
        manifest = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise ProtocolError("campaign") from exc
    if (
        manifest.get("width"),
        manifest.get("companion_width"),
        manifest.get("origin_count"),
    ) != (8, 8, 4):
        raise ProtocolError("campaign_header")
    offers = []
    try:
        for item in manifest.get("offers", []):
            primary = bytes.fromhex(item["primary"])
            companion = bytes.fromhex(item["companion"])
            if (
                len(primary) != 2
                or len(companion) != 2
                or not _canonical_bytes(primary)
                or not _canonical_bytes(companion)
            ):
                raise ProtocolError("campaign_length")
            offers.append((item["id"], primary, companion))
    except (KeyError, TypeError, ValueError) as exc:
        raise ProtocolError("campaign") from exc
    if [item[0] for item in offers] != list(range(1, 17)):
        raise ProtocolError("campaign_ids")
    return manifest, offers


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixture", action="store_true")
    parser.add_argument("--campaign", required=True)
    parser.add_argument("--exe", required=True)
    parser.add_argument("--directory", required=True)
    parser.add_argument("--kill-after", type=int, default=-1)
    parser.add_argument("--rank-cap", type=int, default=8)
    parser.add_argument("--offer-cap", type=int, default=64)
    parser.add_argument("--byte-cap", type=int, default=1 << 20)
    parser.add_argument("--response-deadline", type=float, default=None)
    args = parser.parse_args()
    campaign, offers = load_campaign(args.campaign)
    session = OwnerSession(
        args.exe,
        args.directory,
        width=campaign["width"],
        companion_width=campaign["companion_width"],
        rank_cap=args.rank_cap,
        offer_cap=args.offer_cap,
        byte_cap=args.byte_cap,
        session=17,
        response_deadline=args.response_deadline,
    )
    for index, (oid, row, companion) in enumerate(offers[session.offers :], session.offers + 1):
        session.offer(oid, row, companion)
        if args.kill_after == index:
            session.proc.kill()
            return 137
        if index % 4 == 0:
            session.checkpoint()
    print(
        json.dumps(
            {
                "cursor": session.cursor(campaign["origin_count"]),
                "finalize": session.finalize(campaign["origin_count"]),
            },
            sort_keys=True,
            default=list,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
