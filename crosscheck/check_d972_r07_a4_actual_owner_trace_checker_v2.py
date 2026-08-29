#!/usr/bin/env python3
"""Task358 v6b checker-side, independently written rows 1--7 route.

Only public JSON/group-independent facts are shared with the producer.  The
physical owner, codecs, typed row checks, event trace, and mutation handling
are deliberately implemented here again so a producer fixture cannot make a
checker acceptance by declaration.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import shutil
import stat
import tempfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "d972-r07-a4-actual-owner-trace/v2"
FIXTURE_REL = "search/certs/d972_r07_a4_actual_owner_trace_authority_fixture_v2_20260829.json"
FIXTURE_BYTES = 8457
FIXTURE_SHA = "8fd4de7b89eb07e3adb272782f3052c9b9b3bb90bf7a27212933ae40f892a91d"
FIXTURE_SELF = "abd50579d5d18857ea015bc07fcef4b3bdc7f8f145cfe555f0146f746700d88f"
RECEIPT_REL = "ci/in/d972_r07_seven_context_roof_presentation_v1.json"
MANIFEST_REL = "ci/in/d972_r07_seven_context_roof_presentation_v1.acceptance_v2.json"
RECEIPT_NAME = Path(RECEIPT_REL).name
MANIFEST_NAME = Path(MANIFEST_REL).name
RECEIPT_BYTES = 31017244
RECEIPT_SHA = "82f7955580039f2a0271896c928515d26996f636d8e73231331da6a37f6b19f5"
RECEIPT_SELF = "c8f7e65f6ec7553ab31928c911575de45fc0e3d70cd6e1d678bbebfee7502b9f"
MANIFEST_BYTES = 2722
MANIFEST_SHA = "cc8c16c8ad8f2d094868f0897bcca2a98adba75c18bf7ff397f0da67fd233ea4"
MANIFEST_SELF = "0f630669a906c93a3b7d40bd36633213316ff8da1b46ca254a552b3636963684"
ROWS = 6441
LAYER_COUNTS = {"Gamma_Cayley": 6318, "action": 104, "Q0_lift": 19}
COORDINATE_WIDTHS = [40, 40, 40, 40, 40, 154, 154, 154, 154, 154]
COORDINATE_LEDGER_SHA = "9f9c081e9653d6e141e4d6d231e2d6db9526850b7ccd33c0859d13825f3fa83c"
OCCURRENCE_LEDGER_SHA = "040ab853535db8aad06fba295adf8b59bb1cd77435e7c64a1edcc34cdacb4cd7"
COORDINATE_OWNER = [
    {"construction": "d_E(C21)", "context_id": 21, "index": 0, "role": "hexagon_fxy", "source": "(x,y)", "type": "E3"}, {"construction": "d_E(C22)", "context_id": 22, "index": 1, "role": "hexagon_fxz", "source": "(x,z)", "type": "E3"}, {"construction": "d_E(C23)", "context_id": 23, "index": 2, "role": "hexagon_fyz", "source": "(y,z)", "type": "E3"}, {"construction": "d_E(C24)", "context_id": 24, "index": 3, "role": "hexagon_fux", "source": "(u,x)", "type": "E3"}, {"construction": "d_E(C25)", "context_id": 25, "index": 4, "role": "hexagon_fuy", "source": "(u,y)", "type": "E3"}, {"construction": "C1", "context_id": 1, "index": 5, "role": "pentagon_b1", "source": "b1/phi234", "type": "E4"}, {"construction": "C27", "context_id": 27, "index": 6, "role": "pentagon_b2", "source": "b2/phi1_23_4", "type": "E4"}, {"construction": "C21", "context_id": 21, "index": 7, "role": "pentagon_b3", "source": "b3/phi123", "type": "E4"}, {"construction": "C26", "context_id": 26, "index": 8, "role": "pentagon_b5_inverse_slot", "source": "b5/phi12_3_4", "type": "E4"}, {"construction": "C28", "context_id": 28, "index": 9, "role": "pentagon_b4_inverse_slot", "source": "b4/phi1_2_34", "type": "E4"},
]
OCCURRENCE_LEDGER = [
    {"ordinal": 1, "block": "H1", "block_index": 1, "block_slot": 1, "occurrence": "H1_fxy", "type": "E3", "ten_index": 0, "context_id": 21, "role": "hexagon_fxy", "factor_sign": 1, "orientation": "direct", "fox_prefix_occurrences": [3, 2]}, {"ordinal": 2, "block": "H1", "block_index": 1, "block_slot": 2, "occurrence": "H1_fxz", "type": "E3", "ten_index": 1, "context_id": 22, "role": "hexagon_fxz", "factor_sign": -1, "orientation": "inverse", "fox_prefix_occurrences": [3]}, {"ordinal": 3, "block": "H1", "block_index": 1, "block_slot": 3, "occurrence": "H1_fyz", "type": "E3", "ten_index": 2, "context_id": 23, "role": "hexagon_fyz", "factor_sign": 1, "orientation": "direct", "fox_prefix_occurrences": []}, {"ordinal": 4, "block": "H2", "block_index": 2, "block_slot": 1, "occurrence": "H2_fux", "type": "E3", "ten_index": 3, "context_id": 24, "role": "hexagon_fux", "factor_sign": -1, "orientation": "inverse", "fox_prefix_occurrences": [6, 5]}, {"ordinal": 5, "block": "H2", "block_index": 2, "block_slot": 2, "occurrence": "H2_fxy", "type": "E3", "ten_index": 0, "context_id": 21, "role": "hexagon_fxy", "factor_sign": -1, "orientation": "inverse", "fox_prefix_occurrences": [6]}, {"ordinal": 6, "block": "H2", "block_index": 2, "block_slot": 3, "occurrence": "H2_fuy", "type": "E3", "ten_index": 4, "context_id": 25, "role": "hexagon_fuy", "factor_sign": 1, "orientation": "direct", "fox_prefix_occurrences": []}, {"ordinal": 7, "block": "P1", "block_index": 3, "block_slot": 1, "occurrence": "P_b1", "type": "E4", "ten_index": 5, "context_id": 1, "role": "pentagon_b1", "factor_sign": 1, "orientation": "direct", "fox_prefix_occurrences": [11, 10, 9, 8]}, {"ordinal": 8, "block": "P2", "block_index": 4, "block_slot": 1, "occurrence": "P_b2", "type": "E4", "ten_index": 6, "context_id": 27, "role": "pentagon_b2", "factor_sign": 1, "orientation": "direct", "fox_prefix_occurrences": [11, 10, 9]}, {"ordinal": 9, "block": "P3", "block_index": 5, "block_slot": 1, "occurrence": "P_b3", "type": "E4", "ten_index": 7, "context_id": 21, "role": "pentagon_b3", "factor_sign": 1, "orientation": "direct", "fox_prefix_occurrences": [11, 10]}, {"ordinal": 10, "block": "P5", "block_index": 6, "block_slot": 1, "occurrence": "P_b5_inverse", "type": "E4", "ten_index": 8, "context_id": 26, "role": "pentagon_b5_inverse_slot", "factor_sign": -1, "orientation": "inverse", "fox_prefix_occurrences": [11]}, {"ordinal": 11, "block": "P4", "block_index": 7, "block_slot": 1, "occurrence": "P_b4_inverse", "type": "E4", "ten_index": 9, "context_id": 28, "role": "pentagon_b4_inverse_slot", "factor_sign": -1, "orientation": "inverse", "fox_prefix_occurrences": []},
]
MUTATIONS = ("per_layer_ordinal", "authority_binding", "canonical_input_bytes", "resolved_path_traversal", "normal_generation_proof", "bridge_typed_occurrence_ledger", "evaluator_abi_canary")
OWNER_BY_NAME = {"per_layer_ordinal": "authority.receipt.Delta0.presentation.rows[0].ordinal", "authority_binding": "authority.manifest.accepted", "canonical_input_bytes": "authority.receipt.raw_bytes", "resolved_path_traversal": "authority.receipt.path", "normal_generation_proof": "authority.receipt.Delta0.presentation.normal_generation_proof.Gamma_cayley_edge_count", "bridge_typed_occurrence_ledger": "authority.receipt.bridge.occurrence_ledger[0].block", "evaluator_abi_canary": "authority.receipt.evaluator.coordinate_widths[0]"}
ROW_KEYS = {"Gamma_Cayley": {"ancestry", "generator", "layer", "ordinal", "state", "target_state", "word"}, "action": {"ancestry", "layer", "letter", "ordinal", "orientation", "record", "target_state", "word"}, "Q0_lift": {"ancestry", "layer", "ordinal", "target_state", "word"}}
ANCESTRY_KEYS = {"Gamma_Cayley": {"record_word", "section_source_word", "section_target_word"}, "action": {"record_word", "section_target_word", "tokens"}, "Q0_lift": {"q0_relator_word", "section_target_word"}}
BRIDGE_KEYS = {"branch", "eleven_delete_duplicate", "image_order", "inverse_algorithm", "kernel_order", "marked_inverse_count", "marked_replay", "marked_replay_count", "occurrence_ledger", "occurrence_ledger_sha256", "order_computation", "relator_replay", "seven_blocks", "ten_to_eleven", "typed_coordinate_ledger_sha256"}
EVALUATOR_KEYS = {"canaries", "context_maps", "coordinate_ledger_sha256", "coordinate_widths", "encoding", "entry_points", "joint_coordinate_image", "module", "registry_callable", "relator_rows_sha256", "runtime_constructor", "schema", "semantics"}
TOP_RECEIPT_KEYS = {"D_all", "Delta0", "Gamma", "Ihara_witness", "Q0", "bridge", "cofinal_lift", "direct_Delta_states_enumerated", "evaluator", "fake", "input", "million_row_Q0_Schreier_stream", "resource", "resume", "schema", "self_digest_sha256", "status", "terminal"}
CHUNK_KEYS = {"end", "prefix_complete", "sealed", "sha256", "start"}
ABI_ENCODING = {"roof_value": "ten lowercase hex typed coordinate blobs", "source_word": "strict signed F2 list", "state_ids": "one-based Gamma and Q0 ids"}
ABI_ENTRY_POINTS = {"action": {"arguments": ["runtime", "actor_word", "value"], "callable": "roof_action"}, "eval": {"arguments": ["runtime", "word"], "callable": "roof_eval"}, "inverse": {"arguments": ["runtime", "value"], "callable": "roof_inverse"}, "multiply": {"arguments": ["runtime", "left", "right"], "callable": "roof_multiply"}, "section_cocycle": {"arguments": ["runtime", "left_section_word", "right_section_word", "product_section_word"], "callable": "roof_section_cocycle"}, "source_section": {"arguments": ["runtime", "gamma_state_id", "q0_state_id"], "callable": "roof_source_section"}}
ABI_SEMANTICS = {"action": "actor*value*actor_inverse", "multiplication": "left_then_right", "section_cocycle": "s_left*s_right*s_product_inverse"}

class CheckerInputStop(RuntimeError):
    pass

class NarrowRejection(RuntimeError):
    def __init__(self, validator: str, stage: str, reason: str):
        self.validator, self.stage, self.reason = validator, stage, reason; super().__init__(reason)

class CheckerMutationAccepted(RuntimeError):
    pass

class CheckerMeter:
    CAPS = {"opened_bytes": 250_000_000, "temporary_bytes": 250_000_000, "canonical_bytes": 750_000_000, "dom_bytes": 1_500_000_000, "peak_live_bytes": 750_000_000, "opens": 256, "writes": 256, "events": 10_000, "mutations": 7}
    def __init__(self) -> None:
        self.counts = {k: 0 for k in self.CAPS}; self.reserved = {k: 0 for k in self.CAPS}; self.live_peak = 0; self.peak_seen = 0
        # Retained owner tokens cover the lifetime of cached wire data and
        # parsed/cloned DOMs; transient serialization uses reserve_peak.
        self.retained_peaks: dict[str, int] = {}
    def reserve(self, key: str, amount: int) -> None:
        if key not in self.CAPS or type(amount) is not int or amount < 0 or self.counts[key] + self.reserved[key] + amount > self.CAPS[key]: raise CheckerInputStop("checker:meter:reserve:" + key)
        self.reserved[key] += amount
    def charge(self, key: str, amount: int = 1) -> None:
        if key not in self.CAPS or type(amount) is not int or amount < 0 or self.counts[key] + amount > self.CAPS[key]: raise CheckerInputStop("checker:meter:registry_or_cap:" + key)
        self.reserved[key] = max(0, self.reserved[key] - amount); self.counts[key] += amount
    def release(self, key: str, amount: int) -> None:
        if key not in self.CAPS or type(amount) is not int or amount < 0 or amount > self.reserved[key]: raise CheckerInputStop("checker:meter:release")
        self.reserved[key] -= amount
    def reserve_peak(self, amount: int) -> None:
        if type(amount) is not int or amount < 0 or self.live_peak + amount > self.CAPS["peak_live_bytes"]: raise CheckerInputStop("checker:meter:peak_live")
        self.live_peak += amount; self.peak_seen = max(self.peak_seen, self.live_peak)
    def release_peak(self, amount: int) -> None:
        if type(amount) is not int or amount < 0 or amount > self.live_peak: raise CheckerInputStop("checker:meter:peak_release")
        self.live_peak -= amount
    def retain_peak(self, owner: str, amount: int) -> None:
        if type(owner) is not str or not owner or type(amount) is not int or amount < 0: raise CheckerInputStop("checker:meter:peak_owner")
        self.reserve_peak(amount); self.retained_peaks[owner] = self.retained_peaks.get(owner, 0) + amount
    def release_retained(self, owner: str) -> None:
        amount = self.retained_peaks.pop(owner, 0)
        if amount: self.release_peak(amount)
    def public(self) -> dict[str, Any]:
        return {"caps": dict(self.CAPS), "counts": dict(self.counts), "peak_live_bytes": self.peak_seen, "one_meter": True}

def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("ascii")

def canon_meter(value: Any, meter: CheckerMeter, bound: int = 35_000_000, retained_owner: str | None = None) -> bytes:
    reserved_before = meter.reserved["canonical_bytes"]
    peak_hold = min(bound, meter.CAPS["peak_live_bytes"]); peak_reserved = False
    completed = False
    try:
        meter.reserve("canonical_bytes", bound)
        if retained_owner is None: meter.reserve_peak(peak_hold)
        else: meter.retain_peak(retained_owner, peak_hold)
        peak_reserved = True; raw = canonical(value); meter.charge("canonical_bytes", len(raw)); completed = True; return raw
    finally:
        meter.release("canonical_bytes", meter.reserved["canonical_bytes"] - reserved_before)
        if peak_reserved and retained_owner is None: meter.release_peak(peak_hold)
        if peak_reserved and retained_owner is not None and not completed: meter.release_retained(retained_owner)

def digest_bytes(raw: bytes | bytearray) -> str:
    h = hashlib.sha256(); h.update(raw); return h.hexdigest()

def digest_object(value: Any, meter: CheckerMeter, bound: int = 35_000_000) -> str:
    return digest_bytes(canon_meter(value, meter, bound))

def _int(value: Any) -> bool: return type(value) is int
def _ints(value: Any) -> bool: return type(value) is list and all(type(x) is int and x in (-2, -1, 1, 2) for x in value)

def strict_equal(actual: Any, expected: Any) -> bool:
    if type(expected) is dict:
        return type(actual) is dict and set(actual) == set(expected) and all(strict_equal(actual[k], expected[k]) for k in expected)
    if type(expected) is list:
        return type(actual) is list and len(actual) == len(expected) and all(strict_equal(a, e) for a, e in zip(actual, expected))
    return type(actual) is type(expected) and actual == expected

class EventLog:
    def __init__(self, meter: CheckerMeter):
        self.meter = meter; self.events: list[dict[str, Any]] = []; self._observed: dict[str, dict[str, Any]] = {}; self.canonical_after: dict[str, str] = {}; self.terminal_count = 0; self.rows_digest: str | None = None
    @property
    def observed(self) -> dict[str, dict[str, Any]]: return self._observed
    def enter(self, validator: str, stage: str, owner: str) -> None:
        self.meter.charge("events"); self.events.append({"ordinal": len(self.events) + 1, "validator": validator, "stage": stage, "owner": owner})
    def digest(self) -> str: return digest_object(self.events, self.meter, 1_000_000)
    def terminal(self) -> None: self.terminal_count += 1

def _inside(child: Path, parent: Path) -> bool:
    try: return os.path.commonpath((os.path.abspath(child), os.path.abspath(parent))) == os.path.abspath(parent)
    except ValueError: return False

def _nofollow(path: Path) -> int:
    if os.name == "nt": raise CheckerInputStop("checker:windows:one_handle_reparse_unsupported")
    nofollow = getattr(os, "O_NOFOLLOW", 0)
    if nofollow == 0: raise CheckerInputStop("checker:posix:no_follow_unsupported")
    absolute = Path(os.path.abspath(path)); current = os.open(os.path.sep, os.O_RDONLY | os.O_DIRECTORY | nofollow)
    try:
        for part in absolute.parts[1:-1]:
            nxt = os.open(part, os.O_RDONLY | os.O_DIRECTORY | nofollow, dir_fd=current); os.close(current); current = nxt
        return os.open(absolute.name, os.O_RDONLY | nofollow, dir_fd=current)
    finally: os.close(current)

def _identity(before: os.stat_result, after: os.stat_result, pathname: os.stat_result, path: Path, kind: str, sha: str | None) -> dict[str, Any]:
    stable = all(getattr(before, k) == getattr(after, k) == getattr(pathname, k) for k in ("st_dev", "st_ino", "st_size", "st_mtime_ns", "st_mode", "st_nlink"))
    return {"identity_kind": kind, "path": str(path), "exists": True, "type": "regular" if stat.S_ISREG(before.st_mode) else "nonregular", "mode": int(before.st_mode), "bytes": int(after.st_size), "sha256": sha, "device": int(before.st_dev), "inode": int(before.st_ino), "mtime_ns": int(before.st_mtime_ns), "nlink": int(after.st_nlink), "single_open_handle": True, "opened_handle_stable": stable, "pathname_matches_opened_handle": stable, "substitution_detected": not stable}

def _path_identity(path: Path, kind: str) -> dict[str, Any]:
    lexical = Path(os.path.abspath(path))
    try: st = os.lstat(lexical)
    except (FileNotFoundError, OSError): return {"identity_kind": kind, "path": str(lexical), "exists": False, "type": "missing", "mode": None, "bytes": None, "sha256": None, "device": None, "inode": None, "mtime_ns": None, "nlink": None, "single_open_handle": False, "opened_handle_stable": False, "pathname_matches_opened_handle": False, "substitution_detected": False}
    return {"identity_kind": kind, "path": str(lexical), "exists": True, "type": "regular" if stat.S_ISREG(st.st_mode) else "nonregular", "mode": int(st.st_mode), "bytes": int(st.st_size), "sha256": None, "device": int(st.st_dev), "inode": int(st.st_ino), "mtime_ns": int(st.st_mtime_ns), "nlink": int(st.st_nlink), "single_open_handle": False, "opened_handle_stable": False, "pathname_matches_opened_handle": False, "substitution_detected": False}

class AuthenticatedOwner:
    def __init__(self, meter: CheckerMeter): self.meter = meter; self.cache: dict[str, tuple[bytes | bytearray, dict[str, Any]]] = {}
    def read(self, path: Path, role: str, expected: tuple[int, str] | None = None, events: EventLog | None = None) -> tuple[bytes | bytearray, dict[str, Any]]:
        lexical = Path(os.path.abspath(path)); key = str(lexical)
        if key in self.cache:
            raw, identity = self.cache[key]
            if events is not None: events.observed[role] = identity
            return raw, identity
        opened_hold = 0; dom_hold = 0; peak_hold = 0; peak_owned = False; open_hold = 0; cache_owner = "cache:" + key
        self.meter.reserve("opens", 1); open_hold = 1
        try: fd = _nofollow(lexical)
        except Exception as exc:
            if open_hold: self.meter.release("opens", open_hold)
            if isinstance(exc, CheckerInputStop): raise
            raise CheckerInputStop("checker:open:" + role) from exc
        try:
            before = os.fstat(fd)
            if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1: raise CheckerInputStop("checker:physical:file_identity:" + role)
            size = int(before.st_size)
            if size < 0 or size > self.meter.CAPS["temporary_bytes"]: raise CheckerInputStop("checker:physical:size:" + role)
            self.meter.reserve("opened_bytes", size); opened_hold = size; self.meter.reserve("dom_bytes", size); dom_hold = size; peak_hold = min(size * 2, self.meter.CAPS["peak_live_bytes"])
            if peak_hold: self.meter.retain_peak(cache_owner, peak_hold); peak_owned = True
            buf = bytearray(); remain = size
            while remain:
                part = os.read(fd, min(1_048_576, remain))
                if not part: raise CheckerInputStop("checker:physical:short_read:" + role)
                buf.extend(part); remain -= len(part)
            after = os.fstat(fd); pathname = os.stat(lexical, follow_symlinks=False); content_sha = digest_bytes(buf); identity = _identity(before, after, pathname, lexical, "file", content_sha)
            if not identity["opened_handle_stable"] or after.st_nlink != 1: raise CheckerInputStop("checker:physical:toctou:" + role)
            if expected is not None and (len(buf) != expected[0] or content_sha != expected[1]): raise CheckerInputStop("checker:pin:" + role)
        except OSError as exc:
            if opened_hold: self.meter.release("opened_bytes", opened_hold)
            if dom_hold: self.meter.release("dom_bytes", dom_hold)
            if peak_owned: self.meter.release_retained(cache_owner)
            if open_hold: self.meter.release("opens", open_hold)
            raise CheckerInputStop("checker:read:" + role) from exc
        except Exception:
            if opened_hold: self.meter.release("opened_bytes", opened_hold)
            if dom_hold: self.meter.release("dom_bytes", dom_hold)
            if peak_owned: self.meter.release_retained(cache_owner)
            if open_hold: self.meter.release("opens", open_hold)
            raise
        finally: os.close(fd)
        committed = False
        try:
            self.meter.charge("opened_bytes", len(buf)); opened_hold = 0
            self.meter.charge("dom_bytes", len(buf)); dom_hold = 0
            self.meter.charge("opens"); open_hold = 0
            self.cache[key] = (buf, identity); committed = True
        except Exception:
            if opened_hold: self.meter.release("opened_bytes", opened_hold)
            if dom_hold: self.meter.release("dom_bytes", dom_hold)
            if open_hold: self.meter.release("opens", open_hold)
            if peak_owned and not committed: self.meter.release_retained(cache_owner)
            raise
        if events is not None: events.observed[role] = identity
        return buf, identity
    def recheck_identity(self, path: Path, expected: dict[str, Any], role: str) -> None:
        open_hold = 0; self.meter.reserve("opens", 1); open_hold = 1
        try: fd = _nofollow(Path(os.path.abspath(path)))
        except Exception:
            if open_hold: self.meter.release("opens", open_hold)
            raise
        try:
            before = os.fstat(fd); after = os.fstat(fd); pathname = os.stat(Path(os.path.abspath(path)), follow_symlinks=False)
            if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1 or not all(getattr(before, k) == getattr(after, k) == getattr(pathname, k) for k in ("st_dev", "st_ino", "st_size", "st_mtime_ns", "st_mode", "st_nlink")) or int(after.st_size) != expected.get("bytes") or int(after.st_ino) != expected.get("inode") or int(after.st_dev) != expected.get("device") or int(after.st_mode) != expected.get("mode") or int(after.st_nlink) != expected.get("nlink"): raise CheckerInputStop("checker:baseline:identity_changed:" + role)
        except Exception:
            if open_hold: self.meter.release("opens", open_hold)
            raise
        finally: os.close(fd)
        self.meter.charge("opens")
    def evict_workspace(self, workspace: Path) -> None:
        root = Path(os.path.abspath(workspace))
        for key in list(self.cache):
            if _inside(Path(key), root): del self.cache[key]; self.meter.release_retained("cache:" + key)
        if any(_inside(Path(key), root) for key in self.cache): raise CheckerInputStop("checker:cache:eviction")
    def close(self) -> None:
        for key in list(self.cache):
            del self.cache[key]; self.meter.release_retained("cache:" + key)

def admit(path: Path, role: str, workspace: Path | None, events: EventLog) -> Path:
    events.enter("checker.transport.path_containment", "transport", role + ".path"); lexical = Path(os.path.abspath(path)); registered = Path(os.path.abspath(ROOT / (RECEIPT_REL if role == "receipt" else MANIFEST_REL)))
    if lexical != registered and not (workspace is not None and _inside(lexical, workspace)):
        events.observed[role + ".path"] = _path_identity(lexical, "path"); raise NarrowRejection("checker.transport.path_containment", "transport", "checker:path:registered_containment")
    cursor = Path(lexical.anchor)
    for part in lexical.parts[1:]:
        cursor = cursor / part
        if cursor.is_symlink(): events.observed[role + ".path"] = _path_identity(lexical, "path"); raise NarrowRejection("checker.transport.path_containment", "transport", "checker:path:registered_containment")
    return lexical

def parse_object(raw: bytes | bytearray, label: str, meter: CheckerMeter, exact: bool = True, retained_owner: str | None = None) -> dict[str, Any]:
    hold = len(raw); meter.reserve("dom_bytes", hold); dom_hold = hold
    peak_hold = min(hold * 6, meter.CAPS["peak_live_bytes"]); peak_active = False
    try:
        if peak_hold:
            if retained_owner is None: meter.reserve_peak(peak_hold)
            else: meter.retain_peak(retained_owner, peak_hold)
            peak_active = True
        value = json.loads(raw)
        meter.charge("dom_bytes", hold); dom_hold = 0
    except Exception as exc:
        if dom_hold: meter.release("dom_bytes", dom_hold)
        if peak_active:
            if retained_owner is None: meter.release_peak(peak_hold)
            else: meter.release_retained(retained_owner)
        if isinstance(exc, CheckerInputStop): raise
        raise CheckerInputStop("checker:json:" + label) from exc
    if type(value) is not dict:
        if peak_active:
            if retained_owner is None: meter.release_peak(peak_hold)
            else: meter.release_retained(retained_owner)
        raise CheckerInputStop("checker:object:" + label)
    try:
        if exact and canon_meter(value, meter, len(raw)) != raw: raise CheckerInputStop("checker:json:noncanonical:" + label)
    except Exception:
        if peak_active:
            if retained_owner is None: meter.release_peak(peak_hold)
            else: meter.release_retained(retained_owner)
        raise
    if retained_owner is None and peak_active: meter.release_peak(peak_hold)
    return value

def validate_seal(value: dict[str, Any], label: str, meter: CheckerMeter) -> None:
    if label == "receipt":
        if set(value) != TOP_RECEIPT_KEYS or "manifest_self_digest_sha256" in value: raise NarrowRejection("checker.transport.receipt_seal", "transport", "checker:transport:receipt_self_seal")
        key = "self_digest_sha256"
    else:
        if "self_digest_sha256" in value or type(value.get("manifest_self_digest_sha256")) is not str: raise NarrowRejection("checker.transport.manifest_seal", "transport", "checker:transport:manifest_self_seal")
        key = "manifest_self_digest_sha256"
    claimed = value.get(key); body = dict(value); body.pop(key, None)
    if type(claimed) is not str or claimed != digest_object(body, meter): raise NarrowRejection("checker.transport." + label + ".self_seal", "transport", "checker:transport:" + label + "_self_seal")

MANIFEST_FIXED = {"schema": "d972-r07-seven-context-roof-presentation/v1/acceptance-manifest/v3", "synthetic": False, "independent": True, "producer": {"artifact_id": "9686477718", "head": "bed1d5e6b41477b8799f2a33a24e46f7800f9510", "member": {"basename": RECEIPT_NAME, "bytes": RECEIPT_BYTES, "sha256": RECEIPT_SHA}, "run": "33155710862", "terminal_line_sha256": "b5ab577d14ed490af12e3921ee41cfea533abcbf92d60cc037f0d40035ba5090", "zip_sha256": "8e1d218cb3d0e09e7a633d2c7d4481f232b33e76eaafc51223c307a2c62e0854"}, "checker": {"artifact_id": "9686477718", "head": "bed1d5e6b41477b8799f2a33a24e46f7800f9510", "member": {"basename": RECEIPT_NAME, "bytes": RECEIPT_BYTES, "sha256": RECEIPT_SHA}, "run": "33155710862", "terminal_line_sha256": "260eb23f73a8fb6b9cd2316aa4ea6c29a4a6db92e77d8c5c6f4f1dd6e7ff290e", "zip_sha256": "8e1d218cb3d0e09e7a633d2c7d4481f232b33e76eaafc51223c307a2c62e0854"}, "producer_attestation": {"basename": "d972_r07_seven_context_roof_presentation_v1.producer.attestation.txt", "bytes": 81, "sha256": "b5ab577d14ed490af12e3921ee41cfea533abcbf92d60cc037f0d40035ba5090"}, "checker_attestation": {"basename": "d972_r07_seven_context_roof_presentation_v1.checker.attestation.txt", "bytes": 95, "sha256": "260eb23f73a8fb6b9cd2316aa4ea6c29a4a6db92e77d8c5c6f4f1dd6e7ff290e"}, "checker_verdict": {"accepted": True, "basename": "d972_r07_seven_context_roof_presentation_v1.checker.verdict.json", "bytes": 150, "independent": True, "receipt_terminal": "ROOF_BRIDGE_ISOMORPHISM", "schema": "d972-r07-seven-context-roof-presentation/v1/crosscheck/v2", "sha256": "ac841c5a979bbe89bdd47c73151ecabf29783793b7b288b4d08c4824596251de"}, "task198_source_identities": {"producer": {"bytes": 137169, "path": "search/d972_r07_seven_context_roof_presentation_v1.py", "sha256": "6b2645b80f97256a659af81e856c086cca724b36e2a22ae70335b29ffa95d44c"}, "checker": {"bytes": 157253, "path": "crosscheck/check_d972_r07_seven_context_roof_presentation_v1.py", "sha256": "001277d44dbbc2acd7e03c6ecb6c6419df84996ae188cbb4be7b18f7cfb56ca1"}, "driver": {"bytes": 20541, "path": "search/d972_r07_seven_context_roof_presentation_gha_driver_v1.g", "sha256": "6048174be12d5f6f48508f1b2e80c87b3e1cb9df9ed348b30b6d3e19420b5068"}}}

def validate_manifest(value: dict[str, Any], receipt_path: Path, receipt: dict[str, Any] | None, raw: bytes | bytearray | None, meter: CheckerMeter, raw_sha256: str | None = None) -> None:
    if set(value) != set(MANIFEST_FIXED) | {"accepted", "accepted_receipt_basename", "receipt", "manifest_self_digest_sha256"} or "self_digest_sha256" in value: raise NarrowRejection("checker.authority.manifest_schema", "authority", "checker:authority:manifest_schema")
    validate_seal(value, "manifest", meter)
    for key, fixed in MANIFEST_FIXED.items():
        if key in ("schema", "synthetic", "independent"): continue
        if not strict_equal(value.get(key), fixed): raise NarrowRejection("checker.authority.manifest_graph", "authority", "checker:authority:manifest_graph:" + key)
    if value.get("schema") != MANIFEST_FIXED["schema"] or value.get("synthetic") is not False or value.get("independent") is not True: raise NarrowRejection("checker.authority.manifest_flags", "authority", "checker:authority:manifest_flags")
    if value.get("accepted") is not True: raise NarrowRejection("checker.authority.manifest_acceptance", "authority", "checker:authority:manifest_acceptance")
    binding = value.get("receipt")
    if type(binding) is not dict or set(binding) != {"basename", "bytes", "sha256", "self_digest_sha256"} or binding.get("basename") != receipt_path.name or type(binding.get("bytes")) is not int or type(binding.get("sha256")) is not str or type(binding.get("self_digest_sha256")) is not str: raise NarrowRejection("checker.authority.manifest_receipt_binding", "authority", "checker:authority:manifest_receipt_binding")
    if receipt is not None and raw is not None and (binding["bytes"] != len(raw) or binding["sha256"] != (raw_sha256 if raw_sha256 is not None else digest_bytes(raw)) or binding["self_digest_sha256"] != receipt.get("self_digest_sha256")): raise NarrowRejection("checker.authority.manifest_receipt_binding", "authority", "checker:authority:manifest_receipt_binding")
    if value.get("accepted_receipt_basename") != receipt_path.name: raise NarrowRejection("checker.authority.manifest_receipt_binding", "authority", "checker:authority:manifest_receipt_binding")

GENERATION = {"Gamma_cayley_edge_count": 6318, "Gamma_cayley_state_count": 243, "Q0_defect_normal_closure_order": 243, "Q0_defect_normal_closure_rounds": [243], "Q0_lift_count": 19, "Q0_order_proof": {"G9_abstract_presentation_order": 2916, "G9_direct_image_order": 2916, "P_abstract_presentation_order": 504, "P_direct_image_order": 504, "Q0_marked_image_order": 1469664, "Q0_presentation_order_upper_bound": 1469664, "complete_relator_count": 19, "complete_relators_sha256": "dcb8ce42c8324b0ce2a5018007f3d664da5568ee73182758a9f358deba84bc2a", "cross_commutator_count": 4, "factor_payload_sha256": "6eb95a6830b19e729c5e2a9b4f861fb6105ac0be1f1058cc566898d1b48758ba", "marked_splitting_equation_count": 2, "method": "producer-owned SymPy factor orders plus direct marked-permutation enumeration"}, "all_record_generator_closure_order": 243, "marked_action_loop_count": 104, "normal_closure_exact": True, "presentation_quotient_order_upper_bound": 357128352, "selected_gamma_closure_order": 243, "selected_gamma_records": [1, 3, 6, 9], "surjective_marked_image_order": 357128352, "theorem": "v190 Cayley--action--lift order bound", "upper_bound_equals_image_order": True}

def _typed_row(row: Any, pos: int) -> None:
    layer = "Gamma_Cayley" if pos <= 6318 else "action" if pos <= 6422 else "Q0_lift"; local = pos if layer == "Gamma_Cayley" else pos - 6318 if layer == "action" else pos - 6422
    if type(row) is not dict or set(row) != ROW_KEYS[layer] or row.get("layer") != layer or type(row.get("ordinal")) is not int or row.get("ordinal") != local: raise NarrowRejection("checker.authority.row_order", "authority", "checker:authority:layer_ordinal")
    anc = row.get("ancestry")
    if type(anc) is not dict or set(anc) != ANCESTRY_KEYS[layer] or any(not _ints(anc[k]) for k in anc): raise NarrowRejection("checker.authority.row_shape", "authority", "checker:authority:row_shape")
    if not _ints(row.get("word")): raise NarrowRejection("checker.authority.row_shape", "authority", "checker:authority:row_word")
    for key in ("generator", "state", "target_state", "letter", "record", "orientation"):
        if key in row and type(row[key]) is not int: raise NarrowRejection("checker.authority.row_shape", "authority", "checker:authority:row_type")

def validate_rows(receipt: dict[str, Any], meter: CheckerMeter, baseline_digest: str | None = None, baseline_rows: list[Any] | None = None) -> str:
    p = receipt.get("Delta0", {}).get("presentation")
    if type(p) is not dict or set(p) != {"chunks", "layer_counts", "normal_closure_exact", "normal_generation", "normal_generation_proof", "resume_cursor", "row_count", "rows", "rows_sha256", "source_word_encoding", "task172_legacy_rows_sha256"}: raise NarrowRejection("checker.authority.row_order", "authority", "checker:authority:presentation_shape")
    if type(receipt.get("Delta0")) is not dict or set(receipt["Delta0"]) != {"marked_generators", "normal_closure_exact", "order", "presentation"}: raise NarrowRejection("checker.authority.row_order", "authority", "checker:authority:presentation_shape")
    if type(p.get("chunks")) is not list or any(type(chunk) is not dict or set(chunk) != CHUNK_KEYS or type(chunk.get("start")) is not int or type(chunk.get("end")) is not int or type(chunk.get("prefix_complete")) is not bool or type(chunk.get("sealed")) is not bool or type(chunk.get("sha256")) is not str for chunk in p["chunks"]): raise NarrowRejection("checker.authority.row_order", "authority", "checker:authority:chunk_shape")
    if type(p.get("normal_closure_exact")) is not bool or type(p.get("normal_generation")) is not bool or type(p.get("resume_cursor")) is not int or type(p.get("source_word_encoding")) is not str or type(p.get("task172_legacy_rows_sha256")) is not str: raise NarrowRejection("checker.authority.row_order", "authority", "checker:authority:presentation_types")
    rows = p.get("rows")
    if type(rows) is not list or len(rows) != ROWS or type(p.get("row_count")) is not int or p["row_count"] != ROWS or p.get("layer_counts") != LAYER_COUNTS: raise NarrowRejection("checker.authority.row_order", "authority", "checker:authority:row_count")
    for pos, row in enumerate(rows, 1): _typed_row(row, pos)
    actual = baseline_digest if baseline_rows is not None and rows == baseline_rows and baseline_digest is not None else digest_object(rows, meter)
    if p.get("rows_sha256") != actual: raise NarrowRejection("checker.authority.row_order", "authority", "checker:authority:row_digest")
    return actual

def validate_generation(receipt: dict[str, Any]) -> None:
    proof = receipt["Delta0"]["presentation"].get("normal_generation_proof")
    if type(proof) is not dict or not strict_equal(proof, GENERATION): raise NarrowRejection("checker.authority.normal_generation", "authority", "checker:authority:normal_generation_proof")

def validate_bridge(receipt: dict[str, Any], meter: CheckerMeter) -> None:
    bridge = receipt.get("bridge")
    if type(bridge) is not dict or set(bridge) != BRIDGE_KEYS: raise NarrowRejection("checker.authority.bridge_occurrence", "authority", "checker:authority:bridge_shape")
    ledger = bridge.get("occurrence_ledger"); fields = {"block", "block_index", "block_slot", "context_id", "factor_sign", "fox_prefix_occurrences", "occurrence", "ordinal", "orientation", "role", "ten_index", "type"}
    if type(ledger) is not list or len(ledger) != 11: raise NarrowRejection("checker.authority.bridge_occurrence", "authority", "checker:authority:bridge_occurrence_ledger")
    for actual, expected in zip(ledger, OCCURRENCE_LEDGER):
        if type(actual) is not dict or set(actual) != fields or not strict_equal(actual, expected) or any(type(actual[k]) is not int for k in ("ordinal", "block_index", "block_slot", "context_id", "factor_sign", "ten_index")) or type(actual["fox_prefix_occurrences"]) is not list or any(type(x) is not int for x in actual["fox_prefix_occurrences"]): raise NarrowRejection("checker.authority.bridge_occurrence", "authority", "checker:authority:bridge_occurrence_ledger")
    if digest_object(ledger, meter, 100_000) != bridge.get("occurrence_ledger_sha256") or bridge.get("occurrence_ledger_sha256") != OCCURRENCE_LEDGER_SHA: raise NarrowRejection("checker.authority.bridge_occurrence", "authority", "checker:authority:bridge_occurrence_digest")
    if bridge.get("typed_coordinate_ledger_sha256") != digest_object(COORDINATE_OWNER, meter, 10_000) or bridge.get("typed_coordinate_ledger_sha256") != COORDINATE_LEDGER_SHA: raise NarrowRejection("checker.authority.bridge_occurrence", "authority", "checker:authority:coordinate_ledger")

def validate_abi(receipt: dict[str, Any], meter: CheckerMeter) -> None:
    ev = receipt.get("evaluator")
    if type(ev) is not dict or set(ev) != EVALUATOR_KEYS or not strict_equal(ev.get("coordinate_widths"), COORDINATE_WIDTHS) or ev.get("coordinate_ledger_sha256") != digest_object(COORDINATE_OWNER, meter, 10_000) or ev.get("coordinate_ledger_sha256") != COORDINATE_LEDGER_SHA: raise NarrowRejection("checker.authority.evaluator_abi", "authority", "checker:authority:evaluator_abi_canary")
    if ev.get("context_maps") is not None or ev.get("joint_coordinate_image") is not None or not strict_equal(ev.get("encoding"), ABI_ENCODING) or not strict_equal(ev.get("entry_points"), ABI_ENTRY_POINTS) or not strict_equal(ev.get("semantics"), ABI_SEMANTICS) or ev.get("schema") != "d972-r07-v188-roof-consumer-action-abi/v1" or ev.get("registry_callable") != "v188_consumer_action_abi" or ev.get("runtime_constructor") != "load_runtime" or type(ev.get("canaries")) is not dict or set(ev["canaries"]) != {"nonsplit_y_y_section_cocycle", "source_2_2", "x", "y", "x_inverse", "xy", "xy_section_cocycle", "x_action_y"}: raise NarrowRejection("checker.authority.evaluator_abi", "authority", "checker:authority:evaluator_coordinate_owner")

def validate_receipt(raw: bytes | bytearray, events: EventLog, meter: CheckerMeter, rows_digest: str | None = None, baseline_rows: list[Any] | None = None, retained_owner: str | None = None, raw_sha256: str | None = None) -> dict[str, Any]:
    receipt = parse_object(raw, "receipt", meter, True, retained_owner); events.canonical_after["receipt"] = raw_sha256 if raw_sha256 is not None else digest_bytes(raw); validate_seal(receipt, "receipt", meter)
    if set(receipt) != TOP_RECEIPT_KEYS or receipt.get("schema") != "d972-r07-seven-context-roof-presentation/v1" or receipt.get("status") != "COMPLETE": raise NarrowRejection("checker.authority.receipt_envelope", "authority", "checker:authority:receipt_envelope")
    events.enter("checker.authority.row_order", "authority", "receipt.Delta0.presentation.rows"); row_digest = validate_rows(receipt, meter, rows_digest, baseline_rows); events.rows_digest = row_digest
    events.enter("checker.authority.normal_generation", "authority", "receipt.Delta0.presentation.normal_generation_proof"); validate_generation(receipt)
    events.enter("checker.authority.bridge_occurrence", "authority", "receipt.bridge.occurrence_ledger"); validate_bridge(receipt, meter)
    events.enter("checker.authority.evaluator_abi", "authority", "receipt.evaluator"); validate_abi(receipt, meter); return receipt

def ordinary(manifest_path: Path, receipt_path: Path, workspace: Path | None, store: AuthenticatedOwner, events: EventLog, meter: CheckerMeter, rows_digest: str | None = None, baseline_rows: list[Any] | None = None, retained_owner: str | None = None) -> dict[str, Any]:
    manifest_owner = None if retained_owner is None else retained_owner + ":manifest"; receipt_owner = None if retained_owner is None else retained_owner + ":receipt"
    mp = admit(manifest_path, "manifest", workspace, events); events.enter("checker.transport.manifest_open", "transport", "manifest.bytes"); mraw, mid = store.read(mp, "manifest", (MANIFEST_BYTES, MANIFEST_SHA) if workspace is None else None, events); events.enter("checker.transport.manifest_decode", "decode", "manifest.bytes"); manifest = parse_object(mraw, "manifest", meter, True, manifest_owner); events.canonical_after["manifest"] = mid["sha256"]
    rp = admit(receipt_path, "receipt", workspace, events); events.enter("checker.authority.manifest_acceptance", "authority", "manifest.accepted"); events.enter("checker.transport.receipt_open", "transport", "receipt.bytes"); rraw, rid = store.read(rp, "receipt", (RECEIPT_BYTES, RECEIPT_SHA) if workspace is None else None, events)
    binding = manifest.get("receipt")
    if type(binding) is not dict or binding.get("bytes") != len(rraw) or binding.get("sha256") != rid.get("sha256"): raise NarrowRejection("checker.transport.receipt_identity", "transport", "checker:transport:receipt_sha256")
    validate_manifest(manifest, rp, None, None, meter); receipt = validate_receipt(rraw, events, meter, rows_digest, baseline_rows, receipt_owner, rid.get("sha256")); validate_manifest(manifest, rp, receipt, rraw, meter, rid.get("sha256"))
    return {"manifest": manifest, "receipt": receipt, "manifest_raw": mraw, "receipt_raw": rraw, "manifest_identity": mid, "receipt_identity": rid, "paths": (mp, rp), "rows_digest": events.rows_digest}

def authenticate(store: AuthenticatedOwner, events: EventLog) -> None:
    pins = (("ci/in/d972_r07_seven_context_roof_presentation_v1.producer.attestation.txt", 81, "b5ab577d14ed490af12e3921ee41cfea533abcbf92d60cc037f0d40035ba5090"), ("ci/in/d972_r07_seven_context_roof_presentation_v1.checker.attestation.txt", 95, "260eb23f73a8fb6b9cd2316aa4ea6c29a4a6db92e77d8c5c6f4f1dd6e7ff290e"), ("ci/in/d972_r07_seven_context_roof_presentation_v1.checker.verdict.json", 150, "ac841c5a979bbe89bdd47c73151ecabf29783793b7b288b4d08c4824596251de"), ("search/d972_r07_seven_context_roof_presentation_v1.py", 137169, "6b2645b80f97256a659af81e856c086cca724b36e2a22ae70335b29ffa95d44c"), ("crosscheck/check_d972_r07_seven_context_roof_presentation_v1.py", 157253, "001277d44dbbc2acd7e03c6ecb6c6419df84996ae188cbb4be7b18f7cfb56ca1"), ("search/d972_r07_seven_context_roof_presentation_gha_driver_v1.g", 20541, "6048174be12d5f6f48508f1b2e80c87b3e1cb9df9ed348b30b6d3e19420b5068"))
    for path, size, sha in pins: events.enter("checker.transport.source_pin", "transport", path); store.read(ROOT / path, path, (size, sha), events)

def load_fixture(store: AuthenticatedOwner, meter: CheckerMeter, argument: str) -> dict[str, Any]:
    if Path(argument).is_absolute() or argument.replace("\\", "/") != FIXTURE_REL: raise CheckerInputStop("checker:fixture:path")
    raw, _ = store.read(ROOT / FIXTURE_REL, "fixture", (FIXTURE_BYTES, FIXTURE_SHA)); fixture = parse_object(raw, "fixture", meter, False, "fixture"); body = dict(fixture); seal = body.pop("self_digest_sha256", None)
    if type(seal) is not str or seal != digest_object(body, meter, 1_000_000) or seal != FIXTURE_SELF or fixture.get("schema") != SCHEMA + "/authority-fixture/v2" or fixture.get("synthetic") is not False or fixture.get("candidate_only") is not True or fixture.get("full_a4_selftest") is not False or fixture.get("covered_rows") != [1, 2, 3, 4, 5, 6, 7] or fixture.get("remaining_rows") != list(range(8, 49)) or set(fixture.get("producer", {})) != set(MUTATIONS) or set(fixture.get("checker", {})) != set(MUTATIONS): raise CheckerInputStop("checker:fixture:shape")
    if fixture.get("immutable_input_identities") != {"task198_receipt": {"bytes": RECEIPT_BYTES, "self_digest_sha256": RECEIPT_SELF, "sha256": RECEIPT_SHA}, "task198_manifest": {"bytes": MANIFEST_BYTES, "manifest_self_digest_sha256": MANIFEST_SELF, "sha256": MANIFEST_SHA}}: raise CheckerInputStop("checker:fixture:immutable_inputs")
    return fixture

def seal_receipt(value: dict[str, Any], meter: CheckerMeter, retained_owner: str | None = None) -> bytes:
    body = dict(value); body.pop("self_digest_sha256", None); body.pop("manifest_self_digest_sha256", None); body_owner = None if retained_owner is None else retained_owner + ":body"; raw = canon_meter(body, meter, retained_owner=body_owner)
    try: body["self_digest_sha256"] = digest_bytes(raw)
    finally:
        # The body bytes die before the separately owned final envelope is
        # serialized, so the peak token follows the actual live lifetime.
        del raw
        if body_owner is not None: meter.release_retained(body_owner)
    return canon_meter(body, meter, retained_owner=retained_owner)

def seal_manifest(value: dict[str, Any], meter: CheckerMeter, retained_owner: str | None = None) -> bytes:
    body = dict(value); body.pop("manifest_self_digest_sha256", None)
    if "self_digest_sha256" in body: raise CheckerInputStop("checker:manifest:foreign_seal")
    body_owner = None if retained_owner is None else retained_owner + ":body"; raw = canon_meter(body, meter, 10_000, body_owner)
    try: body["manifest_self_digest_sha256"] = digest_bytes(raw)
    finally:
        del raw
        if body_owner is not None: meter.release_retained(body_owner)
    return canon_meter(body, meter, 10_000, retained_owner)

def copy_manifest(manifest: dict[str, Any], receipt_path: Path, raw: bytes | bytearray, receipt: dict[str, Any], meter: CheckerMeter, retained_owner: str | None = None) -> dict[str, Any]:
    bound = 10_000; meter.reserve("dom_bytes", bound); dom_hold = bound; peak_active = False
    try:
        if retained_owner is None: meter.reserve_peak(bound)
        else: meter.retain_peak(retained_owner, bound)
        peak_active = True; out = copy.deepcopy(manifest); meter.charge("dom_bytes", bound); dom_hold = 0
        return {**out, "accepted_receipt_basename": receipt_path.name, "receipt": {"basename": receipt_path.name, "bytes": len(raw), "sha256": digest_bytes(raw), "self_digest_sha256": receipt["self_digest_sha256"]}}
    except Exception:
        if dom_hold: meter.release("dom_bytes", dom_hold)
        if peak_active:
            if retained_owner is None: meter.release_peak(bound)
            else: meter.release_retained(retained_owner)
            peak_active = False
        raise
    finally:
        if retained_owner is None and peak_active: meter.release_peak(bound)

def clone_small(value: dict[str, Any], meter: CheckerMeter, retained_owner: str | None = None) -> dict[str, Any]:
    bound = 10_000; meter.reserve("dom_bytes", bound); dom_hold = bound; peak_active = False
    try:
        if retained_owner is None: meter.reserve_peak(bound)
        else: meter.retain_peak(retained_owner, bound)
        peak_active = True; clone = copy.deepcopy(value); meter.charge("dom_bytes", bound); dom_hold = 0; return clone
    except Exception:
        if dom_hold: meter.release("dom_bytes", dom_hold)
        if peak_active:
            if retained_owner is None: meter.release_peak(bound)
            else: meter.release_retained(retained_owner)
            peak_active = False
        raise
    finally:
        if retained_owner is None and peak_active: meter.release_peak(bound)

def clone_owner(value: dict[str, Any], bound: int, meter: CheckerMeter, retained_owner: str | None = None) -> dict[str, Any]:
    bound = max(bound, 200_000_000); meter.reserve("dom_bytes", bound); dom_hold = bound; peak_active = False
    try:
        if retained_owner is None: meter.reserve_peak(bound)
        else: meter.retain_peak(retained_owner, bound)
        peak_active = True; clone = copy.deepcopy(value); meter.charge("dom_bytes", bound); dom_hold = 0; return clone
    except Exception:
        if dom_hold: meter.release("dom_bytes", dom_hold)
        if peak_active:
            if retained_owner is None: meter.release_peak(bound)
            else: meter.release_retained(retained_owner)
            peak_active = False
        raise
    finally:
        if retained_owner is None and peak_active: meter.release_peak(bound)

def mutate_wire(source: bytes | bytearray, meter: CheckerMeter, retained_owner: str) -> bytearray:
    bound = len(source); meter.reserve("dom_bytes", bound); dom_hold = bound; peak_active = False
    try:
        meter.retain_peak(retained_owner, bound); peak_active = True; changed = bytearray(source); meter.charge("dom_bytes", bound); dom_hold = 0; changed[-1] ^= 1; return changed
    except Exception:
        if dom_hold: meter.release("dom_bytes", dom_hold)
        if peak_active: meter.release_retained(retained_owner)
        raise

def _mutate(receipt: dict[str, Any], name: str) -> None:
    if name == "per_layer_ordinal": receipt["Delta0"]["presentation"]["rows"][0]["ordinal"] += 1
    elif name == "normal_generation_proof": receipt["Delta0"]["presentation"]["normal_generation_proof"]["Gamma_cayley_edge_count"] += 1
    elif name == "bridge_typed_occurrence_ledger": receipt["bridge"]["occurrence_ledger"][0]["block"] = "H1_mutated"
    elif name == "evaluator_abi_canary": receipt["evaluator"]["coordinate_widths"][0] += 1

def _spec(name: str) -> tuple[str, str, str, str]:
    if name == "authority_binding": return "manifest", "file", "task198/manifest/accepted", "checker.authority.manifest_acceptance"
    if name == "resolved_path_traversal": return "receipt", "path", "task198/receipt/path", "checker.transport.path_containment"
    if name == "canonical_input_bytes": return "receipt", "file", "task198/receipt/raw-bytes", "checker.transport.receipt_identity"
    if name == "per_layer_ordinal": return "receipt", "file", "task198/receipt/row-0001/ordinal", "checker.authority.row_order"
    if name == "normal_generation_proof": return "receipt", "file", "task198/receipt/normal-generation-proof", "checker.authority.normal_generation"
    if name == "bridge_typed_occurrence_ledger": return "receipt", "file", "task198/receipt/bridge-occurrence-ledger", "checker.authority.bridge_occurrence"
    return "receipt", "file", "task198/receipt/evaluator-coordinate-abi", "checker.authority.evaluator_abi"

def run_case(name: str, baseline: dict[str, Any], fixture: dict[str, Any], meter: CheckerMeter, store: AuthenticatedOwner, workspace: Path) -> dict[str, Any]:
    meter.charge("mutations"); role, kind, logical, ordinary_validator = _spec(name); before = baseline[role + "_identity"]; mp, rp = baseline["paths"]; resealed: list[str] = []
    if name == "authority_binding":
        changed = clone_small(baseline["manifest"], meter, "case:" + name + ":clone"); changed["accepted"] = False; mp = workspace / "manifest.json"; manifest_owner = "case:" + name + ":manifest_raw"
        try: atomic_write(mp, seal_manifest(changed, meter, manifest_owner), workspace, meter)
        finally: meter.release_retained(manifest_owner)
        resealed = ["manifest.manifest_self_digest_sha256"]
    elif name == "canonical_input_bytes":
        wire_owner = "case:" + name + ":wire"; raw = mutate_wire(baseline["receipt_raw"], meter, wire_owner)
        try: rp = workspace / RECEIPT_NAME; atomic_write(rp, raw, workspace, meter)
        finally:
            del raw
            meter.release_retained(wire_owner)
    elif name == "resolved_path_traversal": rp = workspace.parent / (RECEIPT_NAME + ".outside")
    elif name in {"per_layer_ordinal", "normal_generation_proof", "bridge_typed_occurrence_ledger", "evaluator_abi_canary"}:
        changed = clone_owner(baseline["receipt"], len(baseline["receipt_raw"]), meter, "case:" + name + ":clone"); _mutate(changed, name); rp = workspace / RECEIPT_NAME; receipt_owner = "case:" + name + ":receipt_raw"; rraw: bytes | None = None
        try:
            rraw = seal_receipt(changed, meter, receipt_owner); atomic_write(rp, rraw, workspace, meter)
            # Keep the returned receipt envelope owned until its manifest
            # binding has consumed the same bytes.
            changed_manifest = copy_manifest(baseline["manifest"], rp, rraw, changed, meter, "case:" + name + ":manifest")
        finally:
            if rraw is not None: del rraw
            meter.release_retained(receipt_owner)
        mp = workspace / MANIFEST_NAME; manifest_owner = "case:" + name + ":manifest_raw"
        try: atomic_write(mp, seal_manifest(changed_manifest, meter, manifest_owner), workspace, meter)
        finally: meter.release_retained(manifest_owner)
        resealed = ["receipt.self_digest_sha256", "manifest.receipt.bytes", "manifest.receipt.sha256", "manifest.receipt.self_digest_sha256", "manifest.manifest_self_digest_sha256"]
    events = EventLog(meter); events._observed = {}
    try: ordinary(mp, rp, workspace, store, events, meter, baseline["rows_digest"], baseline["rows"], "case:" + name)
    except NarrowRejection as rejection:
        events.terminal(); after = events.observed.get(role) or events.observed.get(role + ".path")
        if after is None or all(after.get(k) == before.get(k) for k in ("path", "exists", "type", "mode", "bytes", "sha256", "device", "inode", "nlink")): raise CheckerInputStop("checker:trace:owner_unchanged:" + name)
        expected = fixture["checker"][name]
        if expected["owner"] != OWNER_BY_NAME[name]: raise CheckerInputStop("checker:fixture:owner:" + name)
        first = {"validator": rejection.validator, "stage": rejection.stage, "narrow_reason": rejection.reason}
        if first != expected["first_rejection"] or expected["ordinary_validator"] != ordinary_validator or expected["identity_kind"] != kind or expected["logical_case_path"] != logical or expected["allowed_downstream_reseals"] != resealed or events.terminal_count != 1 or [e["validator"] for e in events.events].count(ordinary_validator) != 1: raise CheckerInputStop("checker:fixture:trace:" + name)
        def proj(identity: dict[str, Any], after_digest: str) -> dict[str, Any]:
            readable = identity.get("exists") is True and identity.get("sha256") is not None
            return {"logical_case_path": logical, "owner_kind": identity.get("identity_kind"), "byte_length": identity.get("bytes") if readable else "UNREADABLE_AT_REGISTERED_STAGE", "content_sha256": identity.get("sha256") if readable else "UNREADABLE_AT_REGISTERED_STAGE", "link_count": identity.get("nlink") if identity.get("nlink") is not None else "UNREADABLE_AT_REGISTERED_STAGE", "symlink_or_reparse": identity.get("type") != "regular", "logical_link_target": "none" if identity.get("type") in ("regular", "missing") else identity.get("type"), "single_open_handle": identity.get("single_open_handle") is True, "opened_handle_stable": identity.get("opened_handle_stable") is True, "pathname_matches_opened_handle": identity.get("pathname_matches_opened_handle") is True, "substitution_detected": identity.get("substitution_detected") is True, "canonical_before_sha256": baseline[role + "_canonical"], "canonical_after_sha256": after_digest}
        evidence = {"id": name, "owner": OWNER_BY_NAME[name], "identity_kind": kind, "before_identity": proj(before, baseline[role + "_canonical"]), "after_identity": proj(after, events.canonical_after.get(role, "UNREADABLE_AT_REGISTERED_STAGE")), "resealed_nodes": resealed, "entered_validators": [e["validator"] for e in events.events], "first_rejection": first, "event_trace_digest": events.digest(), "terminal_count": events.terminal_count, "baseline_revalidated": False, "owner_disposed": False}
        source_for_link = (mp if role == "manifest" else rp); hardlink = workspace / ".case-owner-link"
        if source_for_link.exists(): os.link(source_for_link, hardlink)
        if hardlink.exists(): os.unlink(hardlink)
        if hardlink.exists(): raise CheckerInputStop("checker:workspace:hardlink_eviction:" + name)
        store.evict_workspace(workspace); shutil.rmtree(workspace); evidence["owner_disposed"] = not workspace.exists()
        store.recheck_identity(ROOT / MANIFEST_REL, baseline["manifest_identity"], "manifest"); store.recheck_identity(ROOT / RECEIPT_REL, baseline["receipt_identity"], "receipt"); evidence["baseline_revalidated"] = True
        if evidence["owner_disposed"] is not True: raise CheckerInputStop("checker:workspace:dispose:" + name)
        return evidence
    raise CheckerMutationAccepted("checker:mutation_accepted:" + name)

def atomic_write(path: Path, raw: bytes, workspace: Path, meter: CheckerMeter) -> None:
    if os.name == "nt" or not _inside(path, workspace): raise CheckerInputStop("checker:atomic:unsupported_or_containment")
    meter.reserve("temporary_bytes", len(raw)); meter.charge("temporary_bytes", len(raw)); meter.charge("writes"); meter.reserve("opens", 2); opens_hold = 2
    try: fd, tmp = tempfile.mkstemp(prefix=".checker-trace-", dir=str(workspace))
    except Exception: meter.release("opens", opens_hold); raise
    meter.charge("opens"); opens_hold = 1
    try:
        offset = 0
        while offset < len(raw): offset += os.write(fd, raw[offset:offset + 1_048_576])
        os.fsync(fd)
    finally: os.close(fd)
    try: os.replace(tmp, path)
    except Exception:
        if opens_hold: meter.release("opens", opens_hold)
        raise
    try: dfd = os.open(workspace, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
    except Exception:
        if opens_hold: meter.release("opens", opens_hold)
        raise
    meter.charge("opens"); opens_hold = 0
    try: os.fsync(dfd)
    finally: os.close(dfd)

def execute(fixture: dict[str, Any], meter: CheckerMeter, store: AuthenticatedOwner) -> dict[str, Any]:
    events = EventLog(meter); events._observed = {}; authenticate(store, events); baseline = ordinary(ROOT / MANIFEST_REL, ROOT / RECEIPT_REL, None, store, events, meter, retained_owner="baseline"); baseline["rows"] = baseline["receipt"]["Delta0"]["presentation"]["rows"]; baseline["rows_digest"] = baseline["rows_digest"] or digest_object(baseline["rows"], meter); baseline["receipt_canonical"] = baseline["receipt_identity"]["sha256"]; baseline["manifest_canonical"] = baseline["manifest_identity"]["sha256"]; baseline["baseline_revalidated"] = False
    records = []
    for name in MUTATIONS:
        workspace = Path(tempfile.mkdtemp(prefix="d972-r07-a4-checker-"))
        if _inside(workspace, ROOT): shutil.rmtree(workspace); raise CheckerInputStop("checker:workspace:repository_overlap")
        try:
            record = run_case(name, baseline, fixture, meter, store, workspace); baseline["baseline_revalidated"] = record["baseline_revalidated"]; records.append(record)
        finally:
            meter.release_retained("case:" + name + ":manifest"); meter.release_retained("case:" + name + ":clone")
            store.evict_workspace(workspace)
            if workspace.exists(): shutil.rmtree(workspace)
    result = {"schema": SCHEMA, "candidate_only": True, "synthetic": False, "covered_rows": [1, 2, 3, 4, 5, 6, 7], "remaining_rows": list(range(8, 49)), "full_a4_selftest": False, "baseline": {"receipt_canonical_sha256": baseline["receipt_canonical"], "manifest_canonical_sha256": baseline["manifest_canonical"], "rows_sha256": baseline["rows_digest"], "baseline_revalidated": baseline["baseline_revalidated"]}, "rows": records, "resource": meter.public()}
    # The fixture is released by main; baseline DOM references die here before
    # their retained owners are released.
    del baseline
    meter.release_retained("baseline:manifest"); meter.release_retained("baseline:receipt")
    return result

def write_output(path: Path, value: dict[str, Any], meter: CheckerMeter) -> None:
    target = Path(os.path.abspath(path)); out = Path(os.path.abspath(ROOT / "ci" / "out"))
    if not _inside(target, out) or target.exists() or not target.parent.exists(): raise CheckerInputStop("checker:output:stale_or_containment")
    meter.reserve("opens", 2); output_opens = 2
    try: parent_fd = os.open(target.parent, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
    except Exception: meter.release("opens", output_opens); raise
    meter.charge("opens"); output_opens = 1; parent_before = os.fstat(parent_fd); workspace: Path | None = None
    output_owner = "output:receipt_raw"; raw: bytes | None = None
    try:
        raw = seal_receipt(value, meter, output_owner); workspace = Path(tempfile.mkdtemp(prefix=".checker-stage-", dir=str(target.parent)))
        atomic_write(workspace / "staged.json", raw, workspace, meter)
        try: os.link(workspace / "staged.json", target)
        except FileExistsError as exc: raise CheckerInputStop("checker:output:stale_race") from exc
        os.unlink(workspace / "staged.json"); dfd = None
        try:
            dfd = os.open(target.parent, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)); meter.charge("opens"); output_opens = 0; os.fsync(dfd)
        finally:
            if dfd is not None: os.close(dfd)
    finally:
        if raw is not None: del raw
        meter.release_retained(output_owner)
        try:
            if workspace is not None and workspace.exists(): shutil.rmtree(workspace)
            parent_after = os.fstat(parent_fd)
        finally:
            os.close(parent_fd)
            if output_opens: meter.release("opens", output_opens)
        if (parent_before.st_dev, parent_before.st_ino, parent_before.st_mode, parent_before.st_nlink) != (parent_after.st_dev, parent_after.st_ino, parent_after.st_mode, parent_after.st_nlink): raise CheckerInputStop("checker:output:parent_identity")

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--fixture", default=FIXTURE_REL); parser.add_argument("--output"); args = parser.parse_args(argv)
    if os.name == "nt": raise CheckerInputStop("checker:windows:one_handle_reparse_unsupported")
    meter = CheckerMeter(); store = AuthenticatedOwner(meter)
    try:
        fixture = load_fixture(store, meter, args.fixture); result = execute(fixture, meter, store)
        del fixture; meter.release_retained("fixture")
        if args.output: write_output(Path(args.output), result, meter)
        return 0
    finally:
        meter.release_retained("baseline:manifest"); meter.release_retained("baseline:receipt"); meter.release_retained("fixture")
        store.close()

if __name__ == "__main__": raise SystemExit(main())
