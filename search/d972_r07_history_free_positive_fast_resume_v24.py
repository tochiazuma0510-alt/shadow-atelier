#!/usr/bin/env python3
"""A0 v24: bounded streaming transport over the frozen v23 producer."""
from __future__ import annotations

import hashlib
from pathlib import Path

_V23 = Path(__file__).resolve().with_name(
    "d972_r07_history_free_positive_fast_resume_v23.py")
_V23_BYTES = 3729
_V23_SHA256 = "0e7ad85d5328b86b57086ca4710520ce748e591e0a0e1cc93cedeba3850fb8f3"


def _swap(source: bytes, old: bytes, new: bytes, label: str) -> bytes:
    if not old or not new or old == new or source.count(old) != 1 or source.count(new) != 0:
        raise SystemExit("v24 " + label + " source cardinality")
    result = source.replace(old, new, 1)
    if len(result) != len(source) - len(old) + len(new) or result.count(new) != 1:
        raise SystemExit("v24 " + label + " result cardinality")
    return result


_v23_raw = _V23.read_bytes()
if len(_v23_raw) != _V23_BYTES or hashlib.sha256(_v23_raw).hexdigest() != _V23_SHA256:
    raise SystemExit("v24 frozen v23 owner drift")
_scope = {"__file__": str(_V23), "__name__": "_r07_v23_for_v24"}
exec(compile(_v23_raw, str(_V23), "exec"), _scope, _scope)
_patched = _scope.get("_patched")
if type(_patched) is not bytes:
    raise SystemExit("v24 v23 generated owner missing")

# The parser is deliberately transport-only.  It retains the old semantic
# restore gates, but never creates a bytearray/bytes/str copy of the file.
_STREAM = r'''
class _ResumeJSONReader:
    def __init__(self, path, maximum, meter=None):
        self.path, self.maximum, self.meter = path, maximum, meter
        self.fd = None; self.before = None; self.buf = b""; self.at = 0
        self.total = 0; self.raw_hash = hashlib.sha256()
        self.body_hash = hashlib.sha256(); self.suppress = False

    def open(self):
        flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
        try: self.fd = os.open(self.path, flags)
        except OSError as exc: raise InputStop("bounded_open") from exc
        self.before = os.fstat(self.fd)
        require(stat.S_ISREG(self.before.st_mode) and self.before.st_nlink == 1 and
                0 < self.before.st_size <= self.maximum, "bounded physical object")

    def _pull(self):
        if self.total >= self.before.st_size: return False
        if self.meter is not None: self.meter.check("bounded_json_read")
        chunk = os.read(self.fd, min(1 << 20, self.before.st_size - self.total))
        if not chunk: raise InputStop("bounded_short_read")
        self.buf = chunk; self.at = 0; self.total += len(chunk)
        self.raw_hash.update(chunk); return True

    def take(self, body=True):
        if self.at >= len(self.buf) and not self._pull():
            raise InputStop("bounded_json_eof")
        value = self.buf[self.at:self.at + 1]; self.at += 1
        if body and not self.suppress: self.body_hash.update(value)
        return value

    def peek(self):
        if self.at >= len(self.buf) and not self._pull(): return b""
        return self.buf[self.at:self.at + 1]

    def ws(self):
        while self.peek() in (b" ", b"\t", b"\r", b"\n"): self.take()

    def literal_string(self, body=True):
        raw = bytearray(); raw.extend(self.take(body))
        require(raw == b'"', "JSON string opener")
        while True:
            ch = self.take(body); raw.extend(ch)
            if ch == b'"': break
            require(ch != b"\\" and ch >= b" " or ch == b"\\", "JSON string control")
            if ch == b"\\":
                esc = self.take(body); raw.extend(esc)
                require(esc in b'"\\/bfnrtu', "JSON string escape")
                if esc == b"u":
                    for _ in range(4):
                        digit = self.take(body); raw.extend(digit)
                        require(digit in b"0123456789abcdefABCDEF", "JSON unicode escape")
        try: value = json.loads(bytes(raw).decode("ascii"))
        except (UnicodeError, json.JSONDecodeError) as exc: raise InputStop("bounded_json") from exc
        require(type(value) is str, "JSON string value")
        return value, bytes(raw)

    def value(self):
        self.ws(); ch = self.peek()
        if ch == b"{": return self.object()
        if ch == b"[": return self.array()
        if ch == b'"': return self.literal_string()[0]
        raw = bytearray()
        while self.peek() and self.peek() not in b" \t\r\n,]}:": raw.extend(self.take())
        require(raw, "JSON scalar")
        try: value = json.loads(bytes(raw).decode("ascii"))
        except (UnicodeError, json.JSONDecodeError) as exc: raise InputStop("bounded_json") from exc
        require(type(value) in (str, int, float, bool) or value is None, "JSON scalar type")
        return value

    def object(self):
        require(self.take() == b"{", "JSON object opener"); answer = {}; seen = set(); self.ws()
        if self.peek() == b"}": self.take(); return answer
        while True:
            key, _ = self.literal_string(); require(key not in seen, "JSON duplicate object key")
            seen.add(key); self.ws(); require(self.take() == b":", "JSON object colon")
            answer[key] = self.value(); self.ws(); ch = self.take()
            if ch == b"}": return answer
            require(ch == b",", "JSON object separator"); self.ws()

    def array(self, callback=None):
        require(self.take() == b"[", "JSON array opener"); answer = []; self.ws()
        if self.peek() == b"]": self.take(); return answer
        while True:
            item = self.value()
            if callback is None: answer.append(item)
            else: callback(item)
            self.ws(); ch = self.take()
            if ch == b"]": return answer
            require(ch == b",", "JSON array separator"); self.ws()

    def finish(self):
        self.suppress = True; self.ws(); self.suppress = False
        require(self.peek() == b"", "JSON trailing data")
        after = os.fstat(self.fd)
        require((self.before.st_dev, self.before.st_ino, self.before.st_size,
                 self.before.st_mtime_ns, self.before.st_nlink) ==
                (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns,
                 after.st_nlink), "bounded TOCTOU")
        try: path_after = os.lstat(self.path)
        except OSError as exc: raise InputStop("bounded_path_substitution") from exc
        require(not stat.S_ISLNK(path_after.st_mode) and
                (path_after.st_dev, path_after.st_ino, path_after.st_size,
                 path_after.st_mtime_ns, path_after.st_nlink) ==
                (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns,
                 after.st_nlink), "bounded pathname identity")
        return {"bytes": self.total, "sha256": self.raw_hash.hexdigest(),
                "device": self.before.st_dev, "inode": self.before.st_ino,
                "links": self.before.st_nlink, "mtime_ns": self.before.st_mtime_ns}

_RESUME_TOP_KEYS = ("P_rows", "P_rows_sha256", "boundary_owner", "claims",
    "coefficient_solution_node_ids", "correction_progress", "current_dual",
    "current_dual_sha256", "exact_cached_resume", "formal_ancestry",
    "formal_ancestry_sha256", "heavy_complete", "heavy_input_sha256",
    "heavy_rebuild_frontier", "heavy_reconstructible", "heuristic_discovery_only",
    "last_safe_phase", "light_input_sha256", "monitor", "new_records", "phase",
    "remainder", "schema", "self_digest", "selftest", "solution_node_id",
    "source", "source_snapshots", "target", "target_node_id",
    "triangular_certificate")

def _stream_prepare(search, value):
    live = search.runtime["live"]
    formal = value.get("formal_ancestry")
    require(type(formal) is dict and value.get("formal_ancestry_sha256") == sha_obj(formal) and
            formal.get("dag_owner") == "hash-consed immutable structural DAG node ids" and
            type(formal.get("dag_nodes")) is list and type(formal.get("pivot_expr_ids")) is list and
            formal.get("formal_entries_meter") == "DAG literal-support allocations; never flat expansion" and
            formal.get("dag_literal_support_allocations") == formal.get("entry_count") and
            formal.get("unique_dag_nodes") == len(formal.get("dag_nodes")), "v10 formal DAG owner")
    validate_dag_nodes(formal["dag_nodes"])
    prior_monitor = value.get("monitor", {})
    require(prior_monitor.get("limits") == search.meter.limits and
            type(prior_monitor.get("fresh_v10_counters")) is dict, "v7 checkpoint monitor")
    for name, counter in prior_monitor["fresh_v10_counters"].items():
        require(name in search.meter.counters and type(counter) is int and
                0 <= counter <= search.meter.limits[name], "v7 counter restore")
        search.meter.counters[name] = counter
    search.meter.counters["checkpoint_bytes"] = 0
    prior_boundary = value.get("boundary_owner")
    require(type(prior_boundary) is dict and prior_boundary.get("workers") == search.boundary.workers and
            prior_boundary.get("accounting", {}).get("descriptor_sha256") == search.boundary.descriptor_sha256 and
            prior_boundary.get("cleanup", {}).get("complete") is True and
            prior_boundary["cleanup"].get("live_pids_after_join") == [] and
            type(value.get("next_clean_boundary_epoch")) is int and value["next_clean_boundary_epoch"] >= 1,
            "v7 clean boundary resume owner")
    current = dict(search.boundary.accounting); restored = dict(prior_boundary["accounting"])
    for name in ("frames_sent_bytes", "frames_received_bytes"):
        restored[name] = int(restored.get(name, 0)) + int(current.get(name, 0))
    restarted = search.boundary.workers if prior_boundary["cleanup"].get("started_pids") else 0
    restored["process_restarts"] = int(restored.get("process_restarts", 0)) + restarted
    search.boundary.accounting = restored; search.boundary.epoch = int(value["next_clean_boundary_epoch"]) - 1
    search.reducer.ancestry.nodes = [_freeze_dag_json(node) for node in formal["dag_nodes"]]
    search.reducer.ancestry.intern = {_freeze_dag_json(node): index for index, node in enumerate(formal["dag_nodes"])}
    bindings = formal["pivot_expr_ids"]
    require(type(bindings) is list and len(bindings) >= len(search.reducer.order), "v10 pivot DAG bindings")
    for pivot_hex, node_id in bindings[:len(search.reducer.order)]:
        pivot = bytes.fromhex(pivot_hex)
        require(pivot in search.reducer.rows and type(node_id) is int and
                0 <= node_id < len(search.reducer.ancestry.nodes), "v9 old pivot node binding")
        search.reducer.expr_ids[pivot] = node_id

def _stream_record(search, record):
    live = search.runtime["live"]; expected = len(search.new_records) + 1
    require(record.get("symbol") == f"n:{expected:04d}" and record.get("family") in ("boundary", "correction"),
            "v7 new record order")
    row = live.parse_sparse(record["sparse_row"])
    require(live.public_sparse(row) == record["sparse_row"] and
            record["sparse_row_sha256"] == live.sha_obj(record["sparse_row"]), "v7 new row restore")
    pivot = bytes.fromhex(record["pivot_hex"]); pivot_node_id = int(record["pivot_node_id"])
    require(pivot_node_id in range(len(search.reducer.ancestry.nodes)), "v7 new pivot DAG binding")
    search.reducer.inject(pivot, row, {record["symbol"]: 1}, expression_node=pivot_node_id)
    search.new_records.append(record)

def _stream_resume(search, path, expected_bytes=None, expected_sha256=None):
    reader = _ResumeJSONReader(path, MAX_CHECKPOINT_BYTES, search.meter); reader.open()
    value = {}; prepared = False; claimed = None
    try:
        require(reader.take() == b"{", "JSON top-level object")
        reader.ws(); index = 0; first = True
        while reader.peek() != b"}":
            if not first: require(reader.take(body=False) == b",", "JSON top-level separator")
            first = False; key, raw_key = reader.literal_string(body=False)
            require(index < len(_RESUME_TOP_KEYS) and key == _RESUME_TOP_KEYS[index], "top-level key order")
            index += 1
            if key == "self_digest":
                reader.ws(); require(reader.take(body=False) == b":", "JSON seal colon")
                reader.suppress = True; claimed = reader.value(); reader.suppress = False
            else:
                reader.body_hash.update((b"" if index == 1 else b",") + raw_key)
                reader.ws(); require(reader.take() == b":", "JSON top-level colon")
                if key == "new_records":
                    reader.ws(); require(reader.peek() == b"[", "new_records array")
                    def on_record(item):
                        nonlocal prepared
                        if not prepared:
                            _stream_prepare(search, value); prepared = True
                        _stream_record(search, item)
                    reader.array(callback=on_record); value[key] = []
                else: value[key] = reader.value()
            reader.ws()
        reader.take(body=False); require(index == len(_RESUME_TOP_KEYS), "top-level key completeness")
        reader.body_hash.update(b"}"); physical = reader.finish()
        require(type(claimed) is str and claimed == reader.body_hash.hexdigest(), "self seal")
        if expected_bytes is not None:
            require(physical["bytes"] == expected_bytes and physical["sha256"] == expected_sha256,
                    "resume checkpoint byte/SHA pin")
        require(prepared or ("new_records" in value and (_stream_prepare(search, value) or True)),
                "resume prepare")
        live = search.runtime["live"]; checkpoint_source = value.get("source")
        stable = ("path", "member", "bytes", "sha256", "parsed_once")
        require(value.get("schema") == CHECKPOINT_SCHEMA and type(checkpoint_source) is dict and
                {key: checkpoint_source.get(key) for key in stable} == {key: search.source.get(key) for key in stable} and
                type(checkpoint_source.get("physical")) is dict and value.get("source_snapshots") == search.registry.public() and
                value.get("light_input_sha256") == search.runtime["light_input_sha256"] and
                value.get("triangular_certificate") == search.triangular and value.get("P_rows_sha256") == OLD_PIVOT_ROWS_SHA256 and
                value.get("P_rows") == [live.public_sparse(row) for row in search.p_rows] and value.get("claims") == FALSE_CLAIMS and
                value.get("heuristic_discovery_only") is True and value.get("exact_cached_resume") is False,
                "v7 checkpoint source/basis binding")
        formal = value["formal_ancestry"]
        require(formal.get("dag_nodes") == [_thaw_dag_json(node) for node in search.reducer.ancestry.nodes] and
                formal.get("pivot_expr_ids") == [[pivot.hex(), search.reducer.expr_ids[pivot]] for pivot in search.reducer.order] and
                formal.get("entry_count") == search.reducer.formal_entries, "v7 restored formal DAG")
        remainder, solution_node = search.reducer.reduce(search.target)
        require(live.public_sparse(remainder) == value.get("remainder") and value.get("solution_node_id") == solution_node,
                "v10 restored target DAG state")
        if remainder:
            next_dual, derived_remainder, derived_solution_node = search.reducer.exact_dual(search.target)
            require(derived_remainder == remainder and derived_solution_node == solution_node and
                    live.public_sparse(next_dual) == value.get("current_dual") and
                    live.sha_obj(value.get("current_dual")) == value.get("current_dual_sha256"),
                    "v9 freshly derived resume dual")
            progress_dual = value.get("correction_progress", {}).get("dual_sha256")
            require(progress_dual in (None, live.sha_obj(value.get("current_dual"))), "v10 correction cursor dual binding")
        search.correction_progress = value.get("correction_progress")
        require(type(search.correction_progress) is dict, "v7 correction progress restore")
        search.resume_expected_heavy_sha256 = value.get("heavy_input_sha256")
        search.last_safe_phase = "resumed_" + str(value.get("last_safe_phase"))
        search.initial_state_pending = False; search.boundary.start()
    finally:
        os.close(reader.fd)
'''
_patched = _swap(_patched, b'def restore_checkpoint(search: Search, path: Path) -> None:',
                 _STREAM.encode("ascii") + b'\n\ndef restore_checkpoint(search: Search, path: Path) -> None:',
                 "streaming restore insertion")
_patched = _swap(_patched, b'            restore_checkpoint(search, resume_path)',
                 b'            _stream_resume(search, resume_path, 1663424241,\n'
                 b'                         "55c463335e89fb7e67a04ec9c0405a8216f6f909b2ce67a0fe7a8a4afaf2014d")',
                 "streaming production resume call")
exec(compile(_patched, str(Path(__file__).resolve()), "exec"), globals(), globals())
