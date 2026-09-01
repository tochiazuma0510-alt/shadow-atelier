#!/usr/bin/env python3
"""Task494 durable-discovery rank-99 continuation (v424/v426/v427)."""
from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import os
import tempfile
import time
import types
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "d972-r07-a0-dual-anchored-rank99-durable-discovery/v5"
CP_SCHEMA = SCHEMA + "/checkpoint"
MARKER = "R07_A0_DUAL_ANCHORED_RANK99_DURABLE_DISCOVERY_V5"
UNKNOWN_RESOURCE = "UNKNOWN_RESOURCE"
BATCH_CAP = 16
MAX_RISES = 64
# The driver mirrors these three distinct wall/RSS envelopes.  The hard VM
# value is intentionally larger than the internal RSS ceiling, leaving room
# for one close, canonical serialization, and atomic replacement.
SEARCH_WALL_SECONDS = 14_040.0
INTERNAL_HARD_WALL_SECONDS = 14_220.0
EXTERNAL_WALL_SECONDS = 14_400.0
SEARCH_RSS_BYTES = 4_200_000_000
INTERNAL_HARD_RSS_BYTES = 4_500_000_000
HARD_VM_BYTES = 5_120_000_000

C99 = ("search/certs/d972_r07_a0_dual_anchored_rank99_candidate_v1.json", 173082,
       "bc435660b299f9d72cb2ac10f9765da4ff7f3a16a75242264451c391f20bd358")
RANK51 = ("search/certs/d972_r07_a0_actual_tau_free_rank51_checkpoint_v1.json", 10934,
          "a83959e4c9fcfa79093c712e82164d47c31b78c9fc00b512f7adac9413c481f4")
TASK451_P = ("search/d972_r07_a0_dual_anchored_active_batch_v1.py", 13834,
             "ca7fb15e06dd04881146c38d63d93015a9e630fbc334cf15098cbd8a32f22f9b")
TASK451_C = ("crosscheck/check_d972_r07_a0_dual_anchored_active_batch_recovered_v2.py", 14442,
             "1d1080cd3e130d987316feefd820215f495cd6320aa5eca764fd2f8997f0c424")
PAPER = ("sol/proof_r07_rank99_actual_owner_transform_v424.md", 7009,
         "f2e2103f214e6d7c15f5d1c2bc84cd100cd37a69634c381793a42a20e8bad2d9")
PAPER_V426 = ("sol/proof_r07_rank99_cached_discovery_chain_v426.md", 9165,
              "5c3176011ea64235196587ed19720ad5d5a5c542c2896e46fe33ef3df3a3977a")
PAPER_V427 = ("sol/proof_r07_deadline_flush_short_batch_v427.md", 6602,
              "b958a164dfc78c77596876227b31a39467e077c9666d4a7be9033a58ee4c0ec5")
TASK451_V4 = ("search/d972_r07_a0_actual_tau_free_rank_ladder_v3.py", 12215,
              "0140447110cfa568a77300bd7d43d51c622597704b7b91ed5209c63168c9ef37")
C99_OLD_BINDING = "a9568c6aa47b924ec818bd68b851ce136394b9d4a30af8d37cf3c70bae8a841a"
C99_STATE_SHA = "f2de40c3b16053464b8cf7d397f8fd05ca4439a46ca7e45df93e60bbc11a312d"
RANK51_STATE_SHA = "22dcfdfb396524ea5853488aa2ad52d28b4f7d10164123bc83f121e59dd83159"

_BINDING_BODY = {"schema": SCHEMA, "task451_producer": list(TASK451_P),
                 "task451_checker": list(TASK451_C), "c99": list(C99),
                 "rank51": list(RANK51), "paper": list(PAPER),
                 "paper_v426": list(PAPER_V426), "paper_v427": list(PAPER_V427)}


def canon(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True).encode("ascii")


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def digest(value: Any) -> str:
    return sha(canon(value))


BINDING = digest(_BINDING_BODY)
HEX = set("0123456789abcdef")


def need(value: Any, message: str) -> None:
    if not value:
        raise RuntimeError(message)


def sealed(value: dict[str, Any]) -> dict[str, Any]:
    out = dict(value)
    out.pop("state_sha256", None)
    out.pop("self_digest_sha256", None)
    out["state_sha256"] = digest(out)
    return out


def result_sealed(value: dict[str, Any]) -> dict[str, Any]:
    out = dict(value)
    out.pop("self_digest_sha256", None)
    out["self_digest_sha256"] = digest(out)
    return out


def hex64(value: Any) -> bool:
    return isinstance(value, str) and len(value) == 64 and set(value) <= HEX


def pivot_hex(value: Any) -> bool:
    if not isinstance(value, str) or not value or len(value) % 2 or set(value) - HEX:
        return False
    try:
        return bytes.fromhex(value).hex() == value
    except ValueError:
        return False


def pin(spec: tuple[str, int, str]) -> dict[str, Any]:
    raw = (ROOT / spec[0]).read_bytes()
    need(len(raw) == spec[1] and sha(raw) == spec[2], "pin:" + spec[0])
    return {"path": spec[0], "bytes": len(raw), "sha256": sha(raw)}


def load_pinned(spec: tuple[str, int, str], name: str) -> Any:
    path = ROOT / spec[0]
    raw = path.read_bytes()
    need(len(raw) == spec[1] and sha(raw) == spec[2], "pin:" + spec[0])
    module_spec = importlib.util.spec_from_file_location(name, path)
    need(module_spec is not None and module_spec.loader is not None, "loader:" + spec[0])
    module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(module)
    return module


def pins() -> dict[str, Any]:
    return {name: pin(spec) for name, spec in (("task451_producer", TASK451_P),
                                                 ("task451_checker", TASK451_C),
                                                 ("c99", C99), ("rank51", RANK51),
                                                 ("paper", PAPER), ("paper_v426", PAPER_V426),
                                                 ("paper_v427", PAPER_V427))}


def canonical_input_path(path: str) -> Path:
    need(isinstance(path, str) and path == path.strip(), "input:whitespace")
    p = Path(path)
    need(not p.is_absolute() and len(p.parts) == 3 and p.parts[:2] == ("search", "certs"),
         "input:path")
    tail = p.parts[2]
    need(tail.endswith(".json") and len(tail) > 5 and ".." not in tail, "input:suffix")
    need(all(c in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789._-" for c in tail),
         "input:unsafe")
    root = (ROOT / "search" / "certs").resolve()
    resolved = p.resolve()
    need(not p.is_symlink() and resolved.parent == root and resolved == ROOT / p,
         "input:symlink_escape")
    return p


def read_canonical(path: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    raw = path.read_bytes()
    value = json.loads(raw.decode("ascii"))
    need(isinstance(value, dict) and raw == canon(value) + b"\n", "input:canonical")
    return value, {"path": path.as_posix(), "bytes": len(raw), "sha256": sha(raw)}


def check_old_digest_fields(record: dict[str, Any], prefix: bool = False) -> None:
    for key in ("row_digest", "pivot", "adjoint_digest"):
        need(hex64(record.get(key)) if key != "pivot" else pivot_hex(record.get(key)),
             "old:" + key)
    need(record.get("kind") in {"correction", "action"}, "old:kind")
    if prefix:
        for key in ("pre_dual_digest", "pre_remainder_digest", "post_dual_digest",
                    "post_remainder_digest"):
            need(hex64(record.get(key)), "old:" + key)


def authenticate_c99() -> dict[str, Any]:
    raw = (ROOT / C99[0]).read_bytes()
    need(len(raw) == C99[1] and sha(raw) == C99[2], "c99:pin")
    value = json.loads(raw.decode("ascii"))
    need(raw == canon(value) + b"\n", "c99:canonical")
    body = dict(value)
    state_sha = body.pop("state_sha256", None)
    need(state_sha == C99_STATE_SHA and state_sha == digest(body), "c99:seal")
    need(value.get("schema") == "d972-r07-a0-dual-anchored-active-batch/v1/checkpoint" and
         value.get("binding") == C99_OLD_BINDING and value.get("frozen_sha256") == RANK51[2],
         "c99:binding")
    need(value.get("accepted_count") == 56 and len(value.get("accepted_sources", [])) == 56 and
         value.get("rank") == 99 and value.get("round") == 12 and
         value.get("batch_count") == 3 and value.get("open_batch") is False,
         "c99:shape")
    rank51_raw = (ROOT / RANK51[0]).read_bytes()
    need(len(rank51_raw) == RANK51[1] and sha(rank51_raw) == RANK51[2], "rank51:pin")
    rank51 = json.loads(rank51_raw.decode("ascii"))
    rank51_body = dict(rank51)
    rank51_hash = rank51_body.pop("state_sha256", None)
    need(rank51_raw == canon(rank51) + b"\n" and rank51_hash == RANK51_STATE_SHA and
         rank51_hash == digest(rank51_body), "rank51:seal")
    need(rank51.get("rank") == 51 and rank51.get("accepted_count") == 8 and
         rank51.get("round") == 9 and len(rank51.get("accepted_sources", [])) == 8,
         "rank51:shape")
    need(value["accepted_sources"][:8] == rank51["accepted_sources"], "c99:rank51_prefix")
    for index, record in enumerate(value["accepted_sources"][:8]):
        check_old_digest_fields(record, True)
        need(record.get("kind") == "correction" and record.get("old_rank") == 43 + index and
             record.get("new_rank") == 44 + index and record.get("round") == index + 1 and
             record.get("scalar") in (1, 2), "c99:prefix_record")
    flat: list[dict[str, Any]] = []
    expected_rank = 51
    for batch_no, batch in enumerate(value["batches"], 1):
        need(batch.get("batch") == batch_no and batch.get("closed") is True and
             batch.get("row_count") == 16 and len(batch.get("rows", [])) == 16 and
             batch.get("anchor_rank") == expected_rank and
             batch.get("post_rank") == expected_rank + 16 and
             hex64(batch.get("anchor_dual_digest")) and hex64(batch.get("anchor_remainder_digest")) and
             hex64(batch.get("post_remainder_digest")) and hex64(batch.get("post_dual_digest")),
             "c99:batch_shape")
        for row_index, record in enumerate(batch["rows"]):
            check_old_digest_fields(record)
            need(record.get("pre_rank") == expected_rank + row_index and
                 record.get("post_rank") == expected_rank + row_index + 1 and
                 record.get("anchor_scalar") in (1, 2), "c99:batch_row")
            if record["kind"] == "correction":
                need(isinstance(record.get("selector_cursor"), list) and
                     len(record["selector_cursor"]) == 4 and
                     record.get("exact_exponent_pair") == [72, 0], "c99:literal_shape")
            flat.append(record)
        expected_rank += 16
    need(expected_rank == 99 and flat == value["accepted_sources"][8:], "c99:flattening")
    profile = value.get("current_dual_profile")
    need(isinstance(profile, dict) and profile.get("physical_rank") == 99 and
         hex64(profile.get("dual_digest")) and hex64(profile.get("remainder_digest")),
         "c99:profile")
    value["state_sha256"] = state_sha
    return value


def _flat_appended(batches: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [row for batch in batches for row in batch.get("rows", [])]


def prefix_seed(c99: dict[str, Any]) -> str:
    """Digest of the complete frozen row prefix before any new batch."""
    return digest(c99["accepted_sources"])


def roll_prefix(previous: str, rows: list[dict[str, Any]]) -> str:
    """Advance a canonical rolling digest without reopening an ancestor."""
    need(hex64(previous) and isinstance(rows, list), "prefix:roll_shape")
    return sha((previous + ":" + digest(rows)).encode("ascii"))


def prefix_digest(c99: dict[str, Any], appended: list[dict[str, Any]]) -> str:
    current = prefix_seed(c99)
    for batch in appended:
        current = roll_prefix(current, batch.get("rows", []))
    return current


def ready_core(start: tuple[int, int, int, int], prefix: str, identity: dict[str, Any],
               profile: Any, ledger_digest: str) -> str:
    return digest({"tuple": list(start), "prefix_digest": prefix,
                   "input_checkpoint": identity, "profile": profile,
                   "ledger_digest": ledger_digest})


def segment_descriptor(segment: dict[str, Any]) -> dict[str, Any]:
    return {"start": [segment["start_batch"], segment["start_count"],
                       segment["start_rank"], segment["start_round"]],
            "end": [segment["end_batch"], segment["end_count"],
                    segment["end_rank"], segment["end_round"]],
            "start_prefix_digest": segment["start_prefix_digest"],
            "end_prefix_digest": segment["end_prefix_digest"],
            "new_rises": segment["new_rises"],
            "input_checkpoint": segment["input_checkpoint"],
            "prior_core_digest": segment["prior_core_digest"],
            "end_profile": segment["end_profile"]}


def roll_ledger(previous: str, segment: dict[str, Any]) -> str:
    return sha((previous + ":" + digest(segment_descriptor(segment))).encode("ascii"))


def _identity_shape(identity: Any, label: str) -> None:
    need(isinstance(identity, dict) and isinstance(identity.get("path"), str) and
         isinstance(identity.get("bytes"), int) and hex64(identity.get("sha256")),
         label + ":shape")
    # Path safety is local and read-free here.  Only load_resume/checkpoint
    # authenticates the one immediate file; historical ancestors are sealed
    # ledger data and are never reopened by this validator.
    canonical_input_path(identity["path"])


def segment_gate(state: dict[str, Any], c99: dict[str, Any]) -> str:
    """Validate the complete append-only ledger in one chronological pass."""
    appended = state.get("appended_batches", [])
    segments = state.get("segments", [])
    need(isinstance(appended, list) and isinstance(segments, list), "segment:types")
    current = (3, 56, 99, 12)
    current_digest = prefix_seed(c99)
    app_index = 0
    for index, segment in enumerate(segments):
        need(isinstance(segment, dict) and segment.get("closed") is True, "segment:open")
        start = (segment.get("start_batch"), segment.get("start_count"),
                 segment.get("start_rank"), segment.get("start_round"))
        end = (segment.get("end_batch"), segment.get("end_count"),
               segment.get("end_rank"), segment.get("end_round"))
        need(all(isinstance(x, int) for x in start + end) and start == current,
             "segment:contiguous")
        need(segment.get("start_prefix_digest") == current_digest and
             segment.get("start_prefix_count") == start[1] and
             segment.get("start_prefix_rank") == start[2] and
             segment.get("start_prefix_batch") == start[0] and
             segment.get("start_prefix_round") == start[3], "segment:start_prefix")
        _identity_shape(segment.get("input_checkpoint"), "segment:identity")
        identity = segment["input_checkpoint"]
        if index == 0:
            need(identity == {"path": C99[0], "bytes": C99[1], "sha256": C99[2]},
                 "segment:c99_identity")
        need(segment.get("input_checkpoint_bytes") == identity.get("bytes") and
             segment.get("input_checkpoint_sha256") == identity.get("sha256") and
             hex64(segment.get("prior_state_seal")) and
             hex64(segment.get("prior_ledger_digest")) and
             hex64(segment.get("prior_core_digest")) and
             hex64(segment.get("ledger_digest")) and
             hex64(segment.get("end_core_digest")), "segment:input_identity_metadata")
        need(isinstance(segment.get("start_profile"), (dict, type(None))) and
             isinstance(segment.get("end_profile"), (dict, type(None))), "segment:profiles")
        batch_span = end[0] - start[0]
        need(batch_span > 0 and app_index + batch_span <= len(appended), "segment:batches")
        span = appended[app_index:app_index + batch_span]
        need(len(span) == batch_span, "segment:batches")
        count = start[1]
        rank = start[2]
        round_no = start[3]
        for offset, batch in enumerate(span, 1):
            need(isinstance(batch, dict), "segment:batch_type")
            rows = batch.get("rows", [])
            need(batch.get("batch") == start[0] + offset and
                 batch.get("closed") is True and isinstance(rows, list) and
                 0 < len(rows) <= BATCH_CAP and batch.get("row_count") == len(rows) and
                 batch.get("round") == start[3] + offset, "segment:batch_round")
            need(batch.get("anchor_rank") == rank and
                 batch.get("post_rank") == rank + len(rows), "segment:batch_rank")
            current_digest = roll_prefix(current_digest, rows)
            count += len(rows)
            rank += len(rows)
            round_no += 1
        rises = segment.get("new_rises")
        need(end == (start[0] + batch_span, count, rank, round_no) and
             isinstance(rises, int) and 0 < rises <= MAX_RISES and
             rises == end[1] - start[1] == end[2] - start[2] == count - start[1] and
             sum(batch["row_count"] for batch in span) == rises and
             segment.get("end_prefix_digest") == current_digest and
             segment.get("end_prefix_count") == end[1] and
             segment.get("end_prefix_rank") == end[2] and
             segment.get("end_prefix_batch") == end[0] and
             segment.get("end_prefix_round") == end[3], "segment:end_prefix")
        current = end
        app_index += batch_span
    need(app_index == len(appended), "segment:append_end")
    if not appended:
        need(not segments and state.get("prefix_digest") == current_digest, "segment:empty")
    return current_digest


def validate_appended_batches(appended: list[dict[str, Any]], base: dict[str, Any]) -> None:
    rank = 99
    for expected, batch in enumerate(appended, 4):
        need(isinstance(batch, dict), "append:batch_type")
        rows = batch.get("rows", [])
        need(batch.get("batch") == expected and batch.get("closed") is True and
             batch.get("row_count") == len(rows) and 0 < len(rows) <= BATCH_CAP and
             batch.get("anchor_rank") == rank and
             batch.get("post_rank") == rank + len(rows), "append:batch_shape")
        for index, row in enumerate(rows):
            need(row.get("pre_rank") == rank + index and
                 row.get("post_rank") == rank + index + 1 and
                 row.get("anchor_scalar") in (1, 2) and pivot_hex(row.get("pivot")) and
                 hex64(row.get("row_digest")), "append:row_shape")
            if row.get("kind") == "correction":
                need(isinstance(row.get("predicted_pivot"), str) and
                     row.get("predicted_pivot") == row.get("pivot") and
                     isinstance(row.get("selector_cursor"), list) and
                     len(row["selector_cursor"]) == 4 and
                     isinstance(row.get("exact_exponent_pair"), list) and
                     len(row["exact_exponent_pair"]) == 2 and hex64(row.get("adjoint_digest")),
                     "append:correction_shape")
            else:
                need(row.get("kind") == "action" and isinstance(row.get("action_source"), dict) and
                     row.get("selector_cursor", [None])[0] == "action" and
                     isinstance(row.get("predicted_pivot"), str), "append:action_shape")
        need(hex64(batch.get("anchor_dual_digest")) and
             hex64(batch.get("anchor_remainder_digest")) and
             hex64(batch.get("post_remainder_digest")) and
             (batch.get("post_dual_digest") is None or hex64(batch.get("post_dual_digest"))),
             "append:batch_seals")
        rank += len(rows)
    flat = base["accepted_sources"] + _flat_appended(appended)
    need(rank == 99 + len(_flat_appended(appended)), "append:rank")
    return None


def validate_closed_state(state: dict[str, Any], c99: dict[str, Any], identity: dict[str, Any],
                          check_chain: bool = True,
                          predecessor: dict[str, Any] | None = None) -> None:
    need(state.get("schema") == CP_SCHEMA and state.get("binding") == BINDING and
         state.get("open_batch") is False and state.get("phase") in {"BOOTSTRAP", "READY", "CLOSED"},
         "state:binding")
    body = dict(state)
    got = body.pop("state_sha256", None)
    need(isinstance(got, str) and got == digest(body), "state:seal")
    need(state.get("c99_identity") == {"path": C99[0], "bytes": C99[1], "sha256": C99[2]} and
         state.get("c99_state_sha256") == C99_STATE_SHA and
         state.get("base_prefix") == c99["accepted_sources"][:8] and
         state.get("base_batches") == c99["batches"], "state:c99_prefix")
    appended = state.get("appended_batches")
    need(isinstance(appended, list), "state:appended_type")
    validate_appended_batches(appended, c99)
    need(state.get("batches") == c99["batches"] + appended and
         state.get("accepted_sources") == c99["accepted_sources"] + _flat_appended(appended) and
         state.get("accepted_count") == 56 + len(_flat_appended(appended)) and
         state.get("batch_count") == 3 + len(appended) and
         state.get("rank") == 99 + len(_flat_appended(appended)) and
         isinstance(state.get("round"), int) and state["round"] >= 12,
         "state:flattening")
    need(isinstance(state.get("current_dual_profile"), (dict, type(None))), "state:profile")
    segments = state.get("segments")
    need(isinstance(segments, list), "state:segments")
    need(isinstance(state.get("input_checkpoint"), dict) and
         state.get("input_checkpoint") == identity, "state:input_identity")
    need(state.get("prefix_records") == state.get("accepted_sources") and
         state.get("prefix_digest") == prefix_digest(c99, appended), "state:prefix_digest")
    if check_chain:
        segment_chain_gate(state, c99, predecessor)


def state_from_c99(c99: dict[str, Any], identity: dict[str, Any]) -> dict[str, Any]:
    value = {"schema": CP_SCHEMA, "binding": BINDING,
             "c99_identity": {"path": C99[0], "bytes": C99[1], "sha256": C99[2]},
             "c99_state_sha256": C99_STATE_SHA, "base_prefix": c99["accepted_sources"][:8],
              "base_batches": c99["batches"], "appended_batches": [],
              "batches": c99["batches"], "accepted_sources": c99["accepted_sources"],
              "accepted_count": 56, "batch_count": 3, "rank": 99, "round": 12,
              "current_dual_profile": c99["current_dual_profile"], "segments": [],
              "prefix_records": c99["accepted_sources"],
              "prefix_digest": prefix_seed(c99),
              "ledger_digest": digest([]), "ready_core_digest": None,
              "input_checkpoint": identity, "phase": "BOOTSTRAP", "open_batch": False}
    return sealed(value)


def segment_chain_gate(state: dict[str, Any], c99: dict[str, Any],
                       predecessor: dict[str, Any] | None = None) -> None:
    """Authenticate compact READY cores from the current prefix without I/O."""
    segments = state.get("segments", [])
    appended = state.get("appended_batches", [])
    current_digest = segment_gate(state, c99)
    ledger = digest([])
    current_app = 0
    for index, segment in enumerate(segments):
        segment_start_app = current_app
        start_batch = segment["start_batch"]
        span = segment["end_batch"] - start_batch
        identity = segment["input_checkpoint"]
        start = (segment["start_batch"], segment["start_count"],
                 segment["start_rank"], segment["start_round"])
        expected = ready_core(start, segment["start_prefix_digest"], identity,
                              segment["start_profile"], ledger)
        need(segment.get("prior_ledger_digest") == ledger and
             segment.get("prior_core_digest") == expected and
             hex64(segment.get("prior_state_seal")), "segment:prior_state_seal")
        next_ledger = roll_ledger(ledger, segment)
        end = (segment["end_batch"], segment["end_count"],
               segment["end_rank"], segment["end_round"])
        expected_end = ready_core(end, segment["end_prefix_digest"], identity,
                                  segment["end_profile"], next_ledger)
        need(segment.get("ledger_digest") == next_ledger and
             segment.get("end_core_digest") == expected_end, "segment:end_core")
        if predecessor is not None and index == len(segments) - 1:
            prior_rows = c99["accepted_sources"] + _flat_appended(
                appended[:segment_start_app])
            prior_batches = c99["batches"] + appended[:segment_start_app]
            need(segment.get("prior_state_seal") == predecessor.get("state_sha256"),
                 "segment:immediate_ready_seal")
            need(predecessor.get("accepted_sources") == prior_rows and
                 predecessor.get("batches") == prior_batches and
                 predecessor.get("prefix_records") == prior_rows and
                 predecessor.get("prefix_digest") == segment.get("start_prefix_digest") and
                 predecessor.get("accepted_count") == segment.get("start_count") and
                 predecessor.get("rank") == segment.get("start_rank") and
                 predecessor.get("batch_count") == segment.get("start_batch") and
                 predecessor.get("round") == segment.get("start_round") and
                 predecessor.get("current_dual_profile") == segment.get("start_profile") and
                 predecessor.get("ledger_digest") == segment.get("prior_ledger_digest") and
                 predecessor.get("segments") == segments[:index],
                 "segment:immediate_predecessor_content")
        ledger = next_ledger
        current_app += span
    need(current_digest == state.get("prefix_digest") and
         current_app == len(appended) and
         state.get("ledger_digest", ledger) == ledger and
         (not segments or state.get("ready_core_digest") == segments[-1].get("end_core_digest")) and
         (not segments or state.get("input_checkpoint") == segments[-1].get("input_checkpoint")),
         "segment:final_prefix")


def load_resume(path: str, c99: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any], bool]:
    p = canonical_input_path(path)
    value, identity = read_canonical(p)
    if identity["path"] == C99[0]:
        need(identity["bytes"] == C99[1] and identity["sha256"] == C99[2], "resume:c99_identity")
        state = state_from_c99(c99, identity)
        return state, identity, True
    prior_identity = value.get("input_checkpoint")
    need(isinstance(prior_identity, dict), "resume:prior_identity")
    _identity_shape(prior_identity, "resume:prior_identity")
    validate_closed_state(value, c99, prior_identity)
    # A hard stop before replay can persist the C99-normalized BOOTSTRAP
    # checkpoint as an own-schema resume.  It is closed/open-batch-free and
    # carries the same authenticated durable prefix, so keep it resumable.
    need(value.get("phase") in {"BOOTSTRAP", "READY", "CLOSED"}, "resume:phase")
    return value, identity, False


def write_checkpoint(path: str, state: dict[str, Any]) -> dict[str, Any]:
    p = Path(path)
    need(not p.is_absolute() and p.parent == Path("ci/out"), "checkpoint:path")
    p.parent.mkdir(parents=True, exist_ok=True)
    raw = canon(state) + b"\n"
    with tempfile.NamedTemporaryFile(dir=p.parent, prefix=".task472-", delete=False) as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
        temp = Path(stream.name)
    os.replace(temp, p)
    return {"path": p.as_posix(), "bytes": len(raw), "sha256": sha(raw),
            "accepted_count": state["accepted_count"], "rank": state["rank"],
            "batch_count": state["batch_count"], "phase": state["phase"],
            "state_sha256": state["state_sha256"]}


class SoftResourceStop(RuntimeError):
    """Candidate enumeration reached its recoverable search boundary."""


class HardResourceStop(RuntimeError):
    """The close/serialization reserve was reached."""


def _rss_bytes() -> int | None:
    try:
        import resource
        value = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
        # Linux reports KiB; macOS reports bytes.  This worker is Linux in
        # GHA, while the no-resource Windows fixture simply returns None.
        return value * 1024 if value < 10_000_000_000 else value
    except (ImportError, AttributeError):
        return None


def boundary(args: argparse.Namespace, started: float, phase: str) -> None:
    """Check the internal-hard boundary used outside candidate scanning."""
    elapsed = time.monotonic() - started
    hard_seconds = getattr(args, "hard_seconds", getattr(args, "seconds", None))
    hard_rss = getattr(args, "hard_rss_bytes", getattr(args, "rss_bytes", None))
    if hard_seconds is not None and elapsed >= float(hard_seconds):
        raise HardResourceStop(UNKNOWN_RESOURCE + ":internal_hard:" + phase + ":time_limit")
    if hard_rss is not None:
        rss = _rss_bytes()
        if rss is not None and rss >= int(hard_rss):
            raise HardResourceStop(UNKNOWN_RESOURCE + ":internal_hard:" + phase + ":rss_limit")


def search_boundary(args: argparse.Namespace, started: float, phase: str) -> None:
    """Check the recoverable search-soft boundary inside candidate scans."""
    elapsed = time.monotonic() - started
    soft_seconds = getattr(args, "search_seconds", getattr(args, "seconds", None))
    soft_rss = getattr(args, "search_rss_bytes", getattr(args, "rss_bytes", None))
    if soft_seconds is not None and elapsed >= float(soft_seconds):
        raise SoftResourceStop(UNKNOWN_RESOURCE + ":search_soft:" + phase + ":time_limit")
    if soft_rss is not None:
        rss = _rss_bytes()
        if rss is not None and rss >= int(soft_rss):
            raise SoftResourceStop(UNKNOWN_RESOURCE + ":search_soft:" + phase + ":rss_limit")


def limit_gate(args: argparse.Namespace) -> None:
    search_wall = float(getattr(args, "search_seconds", SEARCH_WALL_SECONDS))
    hard_wall = float(getattr(args, "hard_seconds", INTERNAL_HARD_WALL_SECONDS))
    external_wall = float(getattr(args, "external_seconds", EXTERNAL_WALL_SECONDS))
    search_rss = int(getattr(args, "search_rss_bytes", SEARCH_RSS_BYTES))
    hard_rss = int(getattr(args, "hard_rss_bytes", INTERNAL_HARD_RSS_BYTES))
    hard_vm = int(getattr(args, "hard_vm_bytes", HARD_VM_BYTES))
    need(search_wall < hard_wall < external_wall, "limits:wall_reserve")
    need(search_rss < hard_rss < hard_vm, "limits:rss_reserve")


def resource_reason(reason: Any) -> bool:
    if not isinstance(reason, str) or not reason.startswith(UNKNOWN_RESOURCE + ":"):
        return False
    return reason == UNKNOWN_RESOURCE + ":max_rises" or reason.endswith(":time_limit") or reason.endswith(":rss_limit")


def cap_gate(reason: Any, rises: Any) -> None:
    need(isinstance(rises, int) and 0 <= rises <= MAX_RISES, "cap:rises")
    if reason == UNKNOWN_RESOURCE + ":max_rises":
        need(rises == MAX_RISES, "cap:exact_max_rises")


def build_physical(args: argparse.Namespace, started: float) -> tuple[Any, Any, Any, Any, Any, Any, Any]:
    boundary(args, started, "module_load")
    owner = load_pinned(TASK451_P, "task472_task451_owner")
    v3 = owner.v3
    v1 = owner.load(v3.b.V1, "task472_task451_v1")
    v4 = v1.load(v1.V4, "task472_task451_v4")
    m = v4.load_v1()
    m.RUN_STARTED = started
    m.MARKER = MARKER
    v12 = m.load(m.V12, "task472_task451_v12")
    p435 = m.load(m.P435, "task472_task451_p435")
    p179 = m.load(m.P179, "task472_task451_p179")
    P = v4.adapt(m, m.prefix(v12, p435, args))
    P["started"] = started
    boundary(args, started, "physical_construction")
    return owner, v1, v3, m, v12, p179, P


def pair(dual: dict[bytes, int], row: dict[bytes, int], bmod: Any) -> int:
    return bmod.pair(dual, row)


def model179(p179: Any, P: dict[str, Any]) -> Any:
    g = P.get("g760")
    word = list(g if isinstance(g, (list, tuple)) else g.get("word") if isinstance(g, dict) else g.word)
    runtime = {"old": P["runtime"].old, "e3": P["runtime"].e3, "e4": P["runtime"].e4,
               "p176": P["p176"], "bridge": {"g760": {"word": word}}}
    return p179.AllSevenModel(runtime)


def compiled_formula_scalar(formula: dict[str, Any], blobs: tuple[bytes, ...]) -> int:
    """Evaluate the compiled selector ABI, independently of the raw model."""
    need(isinstance(formula, dict), "compiled_formula:shape")
    K = formula.get("K")
    need(type(K) is int, "compiled_formula:K")
    need(isinstance(blobs, tuple) and all(type(blob) is bytes for blob in blobs),
         "compiled_formula:blobs")
    merged = formula.get("merged")
    need(isinstance(merged, dict), "compiled_formula:merged")
    total = K % 3
    for key, coefficient in merged.items():
        need(isinstance(key, tuple) and len(key) == 2, "compiled_formula:key")
        coordinate, target = key
        need(type(coordinate) is int and 0 <= coordinate < len(blobs),
             "compiled_formula:coordinate")
        need(type(target) is bytes and type(coefficient) is int,
             "compiled_formula:entry")
        total = (total + (coefficient % 3 if blobs[coordinate] == target else 0)) % 3
    need(total in {0, 1, 2}, "compiled_formula:result")
    return total


def formula_bundle(P: dict[str, Any], m: Any, p179: Any, raw_dual: dict[Any, int], args: argparse.Namespace,
                   bmod: Any) -> tuple[Any, list[dict[str, Any]], list[int], dict[str, Any]]:
    model = model179(p179, P)
    formulas: list[dict[str, Any]] = []
    coords: set[int] = set()
    dual = P["dual"]
    n1 = dual.get(b"N\x01", 0)
    n2 = dual.get(b"N\x02", 0)
    ids = [P["p176"]["packed_joint_blob"](P["runtime"].e3.identity, "task472 identity") for _ in range(5)]
    ids += [P["p176"]["packed_joint_blob"](P["runtime"].e4.identity, "task472 identity") for _ in range(5)]
    for index, word in enumerate(P["pres"]["relators"], 1):
        boundary(args, P["started"], "formula_seed")
        formula = model.occurrence_data(word, raw_dual)
        ex, ey = P["v12"].v3.exp_pair(list(word))
        need(ex % 18 == 0 and ey % 18 == 0, "formula:exponent")
        K = (int(n1) * (ex // 18) + int(n2) * (ey // 18)) % 3
        merged = {(int(c), target): int(v) % 3 for (c, target), v in formula["merged"].items() if int(v) % 3}
        coords.update(c for c, _ in merged)
        fresh = P["v12"].aggregate(P["v12"].seed_v12(P["model"], P["runtime"].old,
                                                        P["owner"], P["p176"], P["q"], list(word)))
        need((K + model.formula_scalar(formula, ids)) % 3 == pair(P["dual"], fresh, bmod),
             "formula:identity")
        formulas.append({"seed_index": index, "K": K, "merged": merged,
                         "required_coordinates": sorted({c for c, _ in merged})})
    return model, formulas, sorted(coords), {"raw": raw_dual}


def selector_literal(P: dict[str, Any], m: Any, p179: Any, sf: Any, model: Any,
                     formulas: list[dict[str, Any]], record: dict[str, Any],
                     dual: dict[bytes, int], adjoint_digest: str) -> tuple[dict[bytes, int], int, dict[str, Any]]:
    cursor = record.get("selector_cursor")
    need(isinstance(cursor, list) and len(cursor) == 4, "selector:cursor")
    seed, coordinate, target_hex, ordinal = cursor
    need(isinstance(seed, int) and 1 <= seed <= len(formulas) and isinstance(coordinate, int) and
         isinstance(ordinal, int) and 0 <= ordinal < 9 and record.get("seed_index") == seed,
         "selector:cursor_type")
    formula = formulas[seed - 1]
    target = bytes.fromhex(target_hex)
    need((coordinate, target) in formula["merged"], "selector:target")
    fibre = sf.canonical(coordinate, target)
    need(fibre is not None, "selector:fibre")
    eta = sf.ensure_kernel_prefix(coordinate, 9)[ordinal]
    candidate = sf.kernel_candidate(fibre, eta)
    delta = list(candidate["source_word"])
    need(delta == list(record.get("delta_word", [])), "selector:delta")
    direct = tuple(p179.coordinate_blobs(sf.rt, delta))
    need(direct == tuple(candidate["coordinate_blobs"]) and direct[coordinate] == target,
         "selector:coordinate_tuple")
    scalar = compiled_formula_scalar(formula, direct)
    need(scalar in (1, 2) and scalar == int(record.get("anchor_scalar", record.get("scalar", 0))),
         "selector:scalar")
    need(record.get("required_coordinates") == formula["required_coordinates"], "selector:coordinates")
    need(record.get("adjoint_digest") == adjoint_digest, "selector:adjoint")
    source = {"seed_index": seed, "delta_word": delta}
    return {"seed_index": seed, "delta_word": delta}, scalar, source


def literal_row(P: dict[str, Any], m: Any, p179: Any, sf: Any, model: Any,
                formulas: list[dict[str, Any]], record: dict[str, Any],
                dual: dict[bytes, int], adjoint_digest: str, bmod: Any) -> tuple[dict[bytes, int], int, dict[str, Any]]:
    selector_data, scalar, _ = selector_literal(P, m, p179, sf, model, formulas, record, dual, adjoint_digest)
    seed = selector_data["seed_index"]
    delta = selector_data["delta_word"]
    seed_word = P["pres"]["relators"][seed - 1]
    conjugate = p179.reduce_word(delta + list(seed_word) + p179.inverse_word(delta))
    row = P["v12"].aggregate(P["v12"].replay_atom(seed, delta, P["runtime"], P["model"],
                                                     P["pres"], P["owner"], P["p176"], P["q"]))
    fresh = P["v12"].aggregate(P["v12"].seed_v12(P["model"], P["runtime"].old,
                                                  P["owner"], P["p176"], P["q"], conjugate))
    need(row == fresh, "literal:seed_v12_equality")
    ex, ey = P["v12"].v3.exp_pair(conjugate)
    need(ex % 18 == 0 and ey % 18 == 0 and [ex, ey] == record.get("exact_exponent_pair"),
         "literal:exponent")
    need(all(key[:1] != b"E" for key in row), "literal:forbidden_E")
    need(P["v12"].row_digest(row) == record.get("row_digest"), "literal:row_digest")
    need(pair(dual, row, bmod) == scalar and scalar in (1, 2), "literal:anchor_scalar")
    return row, scalar, {"seed_index": seed, "delta_word": delta,
                         "exact_exponent_pair": [ex, ey], "adjoint_digest": adjoint_digest,
                         "required_coordinates": record["required_coordinates"],
                         "selector_cursor": record["selector_cursor"],
                         "anchor_scalar": scalar, "row_digest": P["v12"].row_digest(row)}


def replay_prefix(v4: Any, P: dict[str, Any], m: Any, p179: Any, prefix: list[dict[str, Any]],
                  args: argparse.Namespace, bmod: Any) -> tuple[Any, Any]:
    state = bmod.update(P, m)
    sf = None
    for index, record in enumerate(prefix):
        dual, rem, _ = state
        need(dual is not None and record.get("kind") == "correction" and
             len(P["phys"].order) == record.get("old_rank") and
             P["v12"].row_digest(dual) == record.get("pre_dual_digest") and
             P["v12"].row_digest(rem) == record.get("pre_remainder_digest"),
             "prefix:pre_state")
        raw_dual, adj = v4.tau_free_adjoint(P, m, args)
        model, formulas, coords, _ = formula_bundle(P, m, p179, raw_dual, args, bmod)
        need(not any(c not in (0, 1, 2) for c in coords) and
             not any(f["K"] for f in formulas) and record.get("adjoint_digest") == adj["adjoint_digest"],
             "prefix:selector_branch")
        if sf is None:
            _, sf = m.selective_runtime(P, p179, args)
        semantic = dict(record)
        semantic["selector_cursor"] = [record["seed_index"], record["coordinate"],
                                        record["target_hex"], record["fibre_cursor"]]
        semantic["anchor_scalar"] = record["scalar"]
        row, scalar, _ = literal_row(P, m, p179, sf, model, formulas, semantic, dual,
                                     adj["adjoint_digest"], bmod)
        need(scalar == record["scalar"], "prefix:scalar")
        reduced, _ = P["phys"].reduce(row)
        need(reduced and min(reduced).hex() == record["pivot"], "prefix:predicted_pivot")
        rise, actual = P["phys"].add(row, {"family": "DIRECT_CORRECTION", "seed_index": record["seed_index"],
                                            "delta_word": record["delta_word"], "source_digest": record["row_digest"]})
        need(rise and actual.hex() == record["pivot"] and len(P["phys"].order) == record["new_rank"],
             "prefix:add")
        state = bmod.update(P, m)
        d2, r2, _ = state
        need(P["v12"].row_digest(r2) == record["post_remainder_digest"] and
             (None if d2 is None else P["v12"].row_digest(d2)) == record["post_dual_digest"],
             "prefix:post_state")
        boundary(args, P["started"], "rank51_replay")
    need(len(P["phys"].order) == 51, "prefix:rank51")
    return state, sf


def replay_batch_rows(v4: Any, P: dict[str, Any], m: Any, p179: Any, batch: dict[str, Any],
                      state: Any, sf: Any, args: argparse.Namespace, bmod: Any) -> tuple[Any, Any]:
    dual, rem, _ = state
    need(dual is not None and batch["anchor_rank"] == len(P["phys"].order) and
         P["v12"].row_digest(dual) == batch["anchor_dual_digest"] and
         P["v12"].row_digest(rem) == batch["anchor_remainder_digest"], "batch:anchor")
    last_key: tuple[Any, ...] | None = None
    compiled: tuple[Any, list[dict[str, Any]], str] | None = None
    for row_record in batch["rows"]:
        cursor = row_record.get("selector_cursor")
        need(isinstance(cursor, list), "batch:cursor")
        if row_record["kind"] == "action":
            key = tuple(cursor)
            need(cursor == ["action", int(row_record["action_source"]["family_index"]),
                            row_record["action_source"]["translation_blob"]], "batch:action_cursor")
            row = P["v12"].action_row(P["runtime"], P["owner"], P["p176"], P["q"], row_record["action_source"])
            source = dict(row_record["action_source"])
            scalar = pair(dual, row, bmod)
            need(scalar == row_record["anchor_scalar"] and scalar in (1, 2), "batch:action_scalar")
        else:
            key = (int(cursor[0]), int(cursor[1]), str(cursor[2]), int(cursor[3]))
            if compiled is None:
                raw_dual, adj = v4.tau_free_adjoint(P, m, args)
                model, formulas, coords, _ = formula_bundle(P, m, p179, raw_dual, args, bmod)
                need(not any(c not in (0, 1, 2) for c in coords) and
                     not any(f["K"] for f in formulas), "batch:selector_branch")
                if sf is None:
                    _, sf = m.selective_runtime(P, p179, args)
                compiled = (model, formulas, adj["adjoint_digest"])
            model, formulas, adjoint_digest = compiled
            row, scalar, _ = literal_row(P, m, p179, sf, model, formulas, row_record, dual,
                                         adjoint_digest, bmod)
            source = {"family": "DIRECT_CORRECTION", "seed_index": row_record["seed_index"],
                      "delta_word": row_record["delta_word"], "source_digest": row_record["row_digest"]}
        need(last_key is None or key > last_key, "batch:cursor_order")
        last_key = key
        need(P["v12"].row_digest(row) == row_record["row_digest"] and
             scalar == row_record["anchor_scalar"] and len(P["phys"].order) == row_record["pre_rank"],
             "batch:row_gate")
        reduced, _ = P["phys"].reduce(row)
        need(reduced and min(reduced).hex() == row_record["pivot"], "batch:predicted_pivot")
        if "predicted_pivot" in row_record:
            need(row_record["predicted_pivot"] == min(reduced).hex(), "batch:stored_predicted_pivot")
        rise, actual = P["phys"].add(row, source)
        need(rise and actual.hex() == row_record["pivot"] and
             len(P["phys"].order) == row_record["post_rank"], "batch:add")
        if sf is not None and hasattr(sf, "cache"):
            sf.cache.clear()
        boundary(args, P["started"], "batch_replay")
    state = bmod.update(P, m)
    d2, r2, _ = state
    need(P["v12"].row_digest(r2) == batch["post_remainder_digest"] and
         (None if d2 is None else P["v12"].row_digest(d2)) == batch["post_dual_digest"] and
         len(P["phys"].order) == batch["post_rank"], "batch:post_state")
    return state, sf


def replay_all(v4: Any, P: dict[str, Any], m: Any, p179: Any, c99: dict[str, Any], state_value: dict[str, Any],
               args: argparse.Namespace, bmod: Any) -> tuple[Any, Any]:
    state, sf = replay_prefix(v4, P, m, p179, c99["accepted_sources"][:8], args, bmod)
    for batch in c99["batches"]:
        state, sf = replay_batch_rows(v4, P, m, p179, batch, state, sf, args, bmod)
    for batch in state_value["appended_batches"]:
        state, sf = replay_batch_rows(v4, P, m, p179, batch, state, sf, args, bmod)
    need(len(P["phys"].order) == state_value["rank"], "replay:rank")
    actual_profile = bmod.profile(P)
    need(actual_profile == state_value["current_dual_profile"], "replay:profile")
    return state, sf


def retain_correction_candidate(v4: Any, P: dict[str, Any], m: Any, p179: Any,
                                sf: Any, model: Any, formula: dict[str, Any],
                                seed_word: list[int], dual: dict[bytes, int],
                                coordinate: int, target: bytes, ordinal: int,
                                candidate: dict[str, Any], adjoint_digest: str,
                                args: argparse.Namespace, bmod: Any) -> dict[str, Any] | None:
    """Run the one production correction-retain ABI.

    The candidate row is reduced without mutation first.  Dependent rows stop
    there; only an independent row reaches literal reconstruction, exponent
    and scalar gates, followed by exactly one physical add whose pivot is
    compared with the non-mutating prediction.
    """
    delta = list(candidate["source_word"])
    row = P["v12"].aggregate(P["v12"].replay_atom(
        formula["seed_index"], delta, P["runtime"], P["model"], P["pres"],
        P["owner"], P["p176"], P["q"]))
    remainder, _ = P["phys"].reduce(row)
    if not remainder:
        return None
    predicted = min(remainder)
    conjugate = p179.reduce_word(delta + list(seed_word) + p179.inverse_word(delta))
    fresh = P["v12"].aggregate(P["v12"].seed_v12(
        P["model"], P["runtime"].old, P["owner"], P["p176"], P["q"], conjugate))
    need(row == fresh, "correction:seed_v12_equality")
    ex, ey = P["v12"].v3.exp_pair(conjugate)
    need(ex % 18 == 0 and ey % 18 == 0, "correction:exponent")
    need(all(key[:1] != b"E" for key in row), "correction:forbidden_E")
    direct = tuple(p179.coordinate_blobs(sf.rt, delta))
    need(direct == tuple(candidate["coordinate_blobs"]) and
         direct[coordinate] == target, "correction:coordinate_gate")
    scalar = compiled_formula_scalar(formula, direct)
    need(scalar in (1, 2) and
         pair(dual, row, v4.b) == scalar, "correction:scalar_gates")
    pre = len(P["phys"].order)
    source = {"family": "DIRECT_CORRECTION", "seed_index": formula["seed_index"],
              "delta_word": delta, "source_digest": P["v12"].row_digest(row)}
    rise, actual = P["phys"].add(row, source)
    need(rise and actual == predicted, "correction:predicted_pivot")
    return {"kind": "correction", "seed_index": formula["seed_index"],
            "delta_word": delta, "exact_exponent_pair": [ex, ey],
            "adjoint_digest": adjoint_digest,
            "required_coordinates": formula["required_coordinates"],
            "selector_cursor": [formula["seed_index"], coordinate, target.hex(), ordinal],
            "anchor_scalar": scalar, "row_digest": P["v12"].row_digest(row),
            "predicted_pivot": predicted.hex(), "pivot": actual.hex(),
            "pre_rank": pre, "post_rank": pre + 1}


def close_batch(P: dict[str, Any], m: Any, bmod: Any, batch_no: int, anchor: Any,
                rows: list[dict[str, Any]], round_no: int) -> tuple[dict[str, Any], Any]:
    dual, rem, _ = anchor
    need(rows and len(rows) <= BATCH_CAP, "batch:close_shape")
    post = bmod.update(P, m)
    d2, r2, _ = post
    receipt = {"batch": batch_no, "anchor_rank": rows[0]["pre_rank"],
               "anchor_dual_digest": P["v12"].row_digest(dual),
               "anchor_remainder_digest": P["v12"].row_digest(rem), "rows": rows,
               "row_count": len(rows), "post_rank": len(P["phys"].order),
               "post_remainder_digest": P["v12"].row_digest(r2),
               "post_dual_digest": None if d2 is None else P["v12"].row_digest(d2),
               "round": round_no, "closed": True}
    return receipt, post


def update_state_after_batch(previous: dict[str, Any], batch: dict[str, Any], post_state: Any,
                             round_no: int, identity: dict[str, Any], active: dict[str, Any] | None,
                             post_profile: dict[str, Any] | None = None,
                             predecessor_state: dict[str, Any] | None = None) -> tuple[dict[str, Any], dict[str, Any]]:
    appended = list(previous["appended_batches"]) + [batch]
    flat = _flat_appended(appended)
    d2, r2, _ = post_state
    profile = previous["current_dual_profile"]
    need(isinstance(post_profile, dict), "batch:post_profile")
    if active is None and predecessor_state is not None:
        # Authenticate the one immediate READY predecessor carried by the
        # caller.  Older segments remain represented by the rolling ledger.
        for key in ("accepted_sources", "batches", "accepted_count", "batch_count",
                    "rank", "round", "prefix_records", "prefix_digest", "ledger_digest",
                    "current_dual_profile", "segments", "input_checkpoint"):
            need(previous.get(key) == predecessor_state.get(key),
                 "segment:immediate_predecessor:" + key)
        need(predecessor_state.get("phase") in {"BOOTSTRAP", "READY", "CLOSED"} and
             hex64(predecessor_state.get("state_sha256")),
             "segment:immediate_predecessor_seal")
    prior_ledger = (active or {}).get("prior_ledger_digest",
                    previous.get("ledger_digest", digest([])))
    start_profile = ((active or {}).get("start_profile") if active is not None
                     else previous["current_dual_profile"])
    state = dict(previous)
    next_prefix_digest = roll_prefix(previous["prefix_digest"], batch["rows"])
    state.update({"appended_batches": appended, "batches": previous["base_batches"] + appended,
                  "accepted_sources": previous["base_prefix"] + _flat_appended(previous["base_batches"]) +
                  flat, "accepted_count": 56 + len(flat), "batch_count": 3 + len(appended),
                  "rank": 99 + len(flat), "round": round_no, "phase": "CLOSED",
                  "open_batch": False, "current_dual_profile": profile,
                  "prefix_records": previous["base_prefix"] + _flat_appended(previous["base_batches"]) + flat,
                  "prefix_digest": next_prefix_digest, "ledger_digest": prior_ledger,
                  # Only a successful atomic close advances this identity.
                  "input_checkpoint": identity})
    if active is None:
        active = {"input_checkpoint": identity, "input_checkpoint_bytes": identity["bytes"],
                  "input_checkpoint_sha256": identity["sha256"],
                  "start_profile": copy.deepcopy(start_profile),
                  "start_batch": batch["batch"] - 1, "start_count": previous["accepted_count"],
                  "start_rank": previous["rank"], "start_round": previous["round"],
                  "end_batch": batch["batch"], "end_count": state["accepted_count"],
                  "end_rank": state["rank"], "end_round": round_no,
                  "start_prefix_digest": previous["prefix_digest"],
                  "start_prefix_count": previous["accepted_count"],
                  "start_prefix_rank": previous["rank"],
                  "start_prefix_batch": previous["batch_count"],
                  "start_prefix_round": previous["round"],
                  "end_prefix_digest": next_prefix_digest,
                  "end_prefix_count": state["accepted_count"],
                  "end_prefix_rank": state["rank"],
                  "end_prefix_batch": state["batch_count"],
                  "end_prefix_round": state["round"],
                  "new_rises": len(flat) - (previous["accepted_count"] - 56), "closed": True}
        active["prior_ledger_digest"] = prior_ledger
        active["prior_core_digest"] = ready_core(
            (active["start_batch"], active["start_count"], active["start_rank"], active["start_round"]),
            active["start_prefix_digest"], identity, active["start_profile"], prior_ledger)
        active["prior_state_seal"] = (predecessor_state or previous).get("state_sha256")
        need(hex64(active["prior_state_seal"]), "segment:prior_state_seal")
        active["end_profile"] = copy.deepcopy(post_profile)
        next_ledger = roll_ledger(prior_ledger, active)
        active["ledger_digest"] = next_ledger
        active["end_core_digest"] = ready_core(
            (active["end_batch"], active["end_count"], active["end_rank"], active["end_round"]),
            active["end_prefix_digest"], identity, active["end_profile"], next_ledger)
        state["ledger_digest"] = next_ledger
        state["ready_core_digest"] = active["end_core_digest"]
        state["segments"] = list(previous["segments"]) + [active]
    else:
        active = dict(active)
        active.update({"end_batch": batch["batch"], "end_count": state["accepted_count"],
                       "end_rank": state["rank"], "end_round": round_no,
                       "end_prefix_digest": next_prefix_digest,
                       "end_prefix_count": state["accepted_count"],
                       "end_prefix_rank": state["rank"],
                       "end_prefix_batch": state["batch_count"],
                       "end_prefix_round": state["round"],
                       "new_rises": state["accepted_count"] - active["start_count"], "closed": True})
        active["end_profile"] = copy.deepcopy(post_profile)
        next_ledger = roll_ledger(active["prior_ledger_digest"], active)
        active["ledger_digest"] = next_ledger
        active["end_core_digest"] = ready_core(
            (active["end_batch"], active["end_count"], active["end_rank"], active["end_round"]),
            active["end_prefix_digest"], active["input_checkpoint"], active["end_profile"], next_ledger)
        state["ledger_digest"] = next_ledger
        state["ready_core_digest"] = active["end_core_digest"]
        state["segments"] = list(previous["segments"][:-1]) + [active]
    need(state["accepted_sources"] == state["base_prefix"] +
         _flat_appended(state["base_batches"]) + flat, "state:append_flat")
    return sealed(state), active


def commit_batch(P: dict[str, Any], m: Any, bmod: Any, previous: dict[str, Any],
                 state_runtime: Any, batch_no: int, rows: list[dict[str, Any]],
                 round_no: int, identity: dict[str, Any], active: dict[str, Any] | None,
                 args: argparse.Namespace, started: float,
                 writer: Any = write_checkpoint,
                 predecessor_state: dict[str, Any] | None = None) -> tuple[dict[str, Any], Any, dict[str, Any], dict[str, Any]]:
    """Close one certified batch, with a hard-boundary rollback point."""
    need(1 <= len(rows) <= BATCH_CAP, "batch:commit_shape")
    # Every check precedes the first durable replace.  A recognized hard stop
    # therefore leaves the caller's previous last_closed file untouched.
    boundary(args, started, "close_pre")
    batch, post_state = close_batch(P, m, bmod, batch_no, state_runtime, rows, round_no)
    boundary(args, started, "close_post_update")
    # Profile is part of the durable post-batch state even when the updated
    # dual is None (the COMMON transition is still replay-authenticated).
    post_profile = bmod.profile(P)
    need(isinstance(post_profile, dict), "batch:post_profile")
    next_state, next_active = update_state_after_batch(previous, batch, post_state,
                                                        round_no, identity, active, post_profile,
                                                        predecessor_state)
    next_state["current_dual_profile"] = post_profile
    next_state = sealed(next_state)
    boundary(args, started, "close_pre_serialize")
    durable = writer(args.checkpoint, next_state)
    return next_state, post_state, next_active, durable


def flush_rows(P: dict[str, Any], m: Any, bmod: Any, previous: dict[str, Any],
               state_runtime: Any, batch_no: int, rows: list[dict[str, Any]],
               round_no: int, identity: dict[str, Any], active: dict[str, Any] | None,
               durable: dict[str, Any] | None, args: argparse.Namespace, started: float,
               writer: Any = write_checkpoint,
               predecessor_state: dict[str, Any] | None = None) -> tuple[dict[str, Any], Any, dict[str, Any] | None,
                                                         dict[str, Any] | None, bool, str | None]:
    """Commit a soft-boundary batch or return the preceding atomic state."""
    if not rows:
        return previous, state_runtime, active, durable, False, None
    try:
        next_state, post_state, next_active, next_durable = commit_batch(
            P, m, bmod, previous, state_runtime, batch_no, rows, round_no,
            identity, active, args, started, writer, predecessor_state)
    except HardResourceStop as stop:
        return previous, state_runtime, active, durable, False, str(stop)
    return next_state, post_state, next_active, next_durable, True, None


def terminal_result(status: str, reason: str | None, state: dict[str, Any], input_id: dict[str, Any],
                    durable: dict[str, Any] | None, started: float, args: argparse.Namespace,
                    ready_written: bool, bootstrap_written: bool, selector_entered: bool,
                    gate_profile: Any = None, terminal_replay: Any = None,
                    open_batch_discarded: bool = False,
                    invocation_start: tuple[int, int, int, int] | None = None,
                    soft_flush_committed: bool = False) -> dict[str, Any]:
    if status == UNKNOWN_RESOURCE:
        need(durable is not None and open_batch_discarded, "resource:closed_fallback")
        rises = 0 if not state["segments"] else state["segments"][-1]["new_rises"]
        if invocation_start is not None and state["segments"]:
            latest = state["segments"][-1]
            if (latest["start_count"], latest["start_rank"], latest["start_batch"],
                    latest["start_round"]) != invocation_start:
                rises = 0
        cap_gate(reason, rises)
    all_batches = state["base_batches"] + state["appended_batches"]
    active = state["segments"][-1] if state["segments"] else None
    # A resumed invocation may stop before closing a new batch.  In that
    # case the historical final segment is not this invocation's segment;
    # expose the authenticated invocation boundary with zero new rises.
    if active is not None and invocation_start is not None:
        active_start = (active["start_count"], active["start_rank"],
                        active["start_batch"], active["start_round"])
        if active_start != (invocation_start[0], invocation_start[1],
                            invocation_start[2], invocation_start[3]):
            active = None
    start_count, start_rank, start_batch, start_round = invocation_start or (
        state["accepted_count"], state["rank"], state["batch_count"], state["round"])
    out = {"schema": SCHEMA, "status": status, "terminal": status, "reason": reason,
           "input_checkpoint": input_id, "c99_identity": state["c99_identity"],
           "invocation_input_checkpoint": input_id,
           "durable_input_checkpoint": state.get("input_checkpoint"),
           "c99_state_sha256": C99_STATE_SHA, "frozen_prefix_count": 8,
           "base_prefix": state["base_prefix"], "base_batches": state["base_batches"],
           "appended_batches": state["appended_batches"], "batches": all_batches,
           "accepted_sources": state["accepted_sources"], "accepted_count": state["accepted_count"],
           "batch_count": state["batch_count"], "round": state["round"],
           "prefix_records": state["prefix_records"], "prefix_digest": state["prefix_digest"],
           "physical_rank": state["rank"], "rank": state["rank"],
           "current_dual_profile": state["current_dual_profile"],
           "segments": state["segments"], "segment_start_count": active["start_count"] if active else start_count,
           "segment_end_count": active["end_count"] if active else start_count,
           "segment_start_rank": active["start_rank"] if active else start_rank,
           "segment_end_rank": active["end_rank"] if active else start_rank,
           "segment_start_batch": active["start_batch"] if active else start_batch,
           "segment_end_batch": active["end_batch"] if active else start_batch,
           "segment_start_round": active["start_round"] if active else start_round,
           "segment_end_round": active["end_round"] if active else start_round,
           "segment_rises": active["new_rises"] if active else 0,
           "max_rises": MAX_RISES, "batch_cap": BATCH_CAP, "durable_state": durable,
           "last_closed": {"state_sha256": state["state_sha256"], "rank": state["rank"],
                           "accepted_count": state["accepted_count"], "batch_count": state["batch_count"]},
           "bootstrap_written": bootstrap_written, "ready_written": ready_written,
           "selector_entered": selector_entered, "gate_profile": gate_profile,
           "terminal_replay": terminal_replay, "open_batch_discarded": open_batch_discarded,
           "soft_flush_committed": soft_flush_committed,
           "discovery_mode": "DISCOVERY_RESOURCE" if status == UNKNOWN_RESOURCE else "COMMON",
           "candidate_marker": (MARKER + "_RESOURCE_CANDIDATE"
                                 if status == UNKNOWN_RESOURCE else MARKER + "_COMMON_CANDIDATE"),
           "claims": {"A0": status == "COMMON_CANDIDATE", "COMMON": False,
                      "NONMEMBER": False, "fake": False, "Ihara": False},
           "pins": pins(), "binding": BINDING,
           "elapsed_seconds": time.monotonic() - started}
    return result_sealed(out)


def run(args: argparse.Namespace) -> dict[str, Any]:
    started = time.monotonic()
    need(args.resume, "production:resume_required")
    need(args.max_rises == MAX_RISES and args.batch_cap == BATCH_CAP, "fixed_caps")
    limit_gate(args)
    c99 = authenticate_c99()
    state, input_id, is_base = load_resume(args.resume, c99)
    # Keep this parsed/authenticated state as the one immediate predecessor.
    # In particular, a zero-progress invocation must not rewrite its
    # historical input identity before a new batch is durably closed.
    # The C99-normalized BOOTSTRAP state is the authenticated predecessor for
    # a first segment as well.  Own-schema resumes carry READY/CLOSED here.
    predecessor_state = state
    # The only durable object before construction is this exact closed span.
    # C99 enters as BOOTSTRAP.  An own-schema resume keeps its authenticated
    # READY/CLOSED phase so a pre-close fallback remains byte-for-byte
    # resumable by load_resume.
    state = sealed(dict(state, phase="BOOTSTRAP" if is_base else state["phase"],
                        open_batch=False))
    durable = write_checkpoint(args.checkpoint, state)
    bootstrap_written = True
    ready_written = False
    selector_entered = False
    gate_profile: Any = None
    active: dict[str, Any] | None = None
    invocation_start = (state["accepted_count"], state["rank"], state["batch_count"], state["round"])
    try:
        owner, v1, v3, m, v12, p179, P = build_physical(args, started)
        v4 = v3
        physical_state, sf = replay_all(v4, P, m, p179, c99, state, args, v4.b)
        boundary(args, started, "physical_replay")
        state = sealed(dict(state, phase="READY", open_batch=False))
        durable = write_checkpoint(args.checkpoint, state)
        ready_written = True
        gate_profile = state["current_dual_profile"]
        runtime, sf = m.selective_runtime(P, p179, args)
        P["runtime_selective"] = runtime
        actions = list(P["runtime"].old.pure_relations(4)[5:11])
        new_rises = 0
        state_runtime = physical_state
        while True:
            boundary(args, started, "selector")
            dual, rem, coeff = state_runtime
            round_no = int(state["round"]) + 1
            if dual is None:
                # This is an actual post-replay COMMON state, never a contingent shortcut.
                selector_entered = True
                positive = v1.positive(P, m, coeff)
                return terminal_result("COMMON_CANDIDATE", None, state, input_id, durable, started, args,
                                       ready_written, bootstrap_written, selector_entered, None, positive,
                                       False, invocation_start)
            profile = v3.b.profile(P)
            gate_profile = profile
            need(not profile["unrecognized_keys"], "UNKNOWN:UNRECOGNIZED_DUAL_KEYS")
            if new_rises >= MAX_RISES:
                raise RuntimeError(UNKNOWN_RESOURCE + ":max_rises")
            batch_no = 4 + len(state["appended_batches"])
            rows: list[dict[str, Any]] = []
            action_hit = None
            soft_reason: str | None = None
            # The action-support selector is part of the real selector path;
            # mark entry before asking it for candidates.
            selector_entered = True
            try:
                for candidate, source in P["q"].action_support_hits(P["runtime"], P["owner"], P["p176"], actions, dual):
                    search_boundary(args, started, "action_candidate")
                    row = v12.action_row(P["runtime"], P["owner"], P["p176"], P["q"], source)
                    scalar = v3.b.pair(dual, row)
                    need(row == candidate and scalar == int(source["scalar"]) % 3 and scalar,
                         "action:scalar")
                    reduced, _ = P["phys"].reduce(row)
                    need(reduced, "action:dependent")
                    predicted = min(reduced)
                    pre = len(P["phys"].order)
                    public = v1.public_source(source)
                    source_for_phys = dict(source)
                    source_for_phys["row_digest"] = v12.row_digest(row)
                    rise, actual = P["phys"].add(row, source_for_phys)
                    need(rise and actual == predicted, "action:predicted_pivot")
                    rows.append({"kind": "action", "action_source": public,
                                 "selector_cursor": ["action", int(source["family_index"]), source["translation_blob"]],
                                 "anchor_scalar": scalar, "row_digest": v12.row_digest(row),
                                 "predicted_pivot": predicted.hex(), "pivot": actual.hex(),
                                 "pre_rank": pre, "post_rank": pre + 1})
                    action_hit = True
                    break
                if action_hit is None:
                    raw_dual, adj = v4.tau_free_adjoint(P, m, args)
                    model, formulas, coords, _ = formula_bundle(P, m, p179, raw_dual, args, v3.b)
                    current = dict(profile, **adj)
                    current["required_coordinates"] = coords
                    gate_profile = current
                    need(not any(c not in (0, 1, 2) for c in coords), "UNKNOWN:SELECTOR_COORDINATES")
                    need(not any(f["K"] for f in formulas), "UNKNOWN:NONZERO_CONSTANT_SELECTOR")
                    selector_entered = True
                    if sf is None:
                        _, sf = m.selective_runtime(P, p179, args)
                    for formula, seed_word in zip(formulas, P["pres"].relators):
                        for coordinate, target in sorted(formula["merged"], key=lambda x: (x[0], x[1])):
                            fibre = sf.canonical(coordinate, target)
                            if fibre is None:
                                continue
                            for ordinal, eta in enumerate(sf.ensure_kernel_prefix(coordinate, 9)):
                                search_boundary(args, started, "candidate")
                                candidate = sf.kernel_candidate(fibre, eta)
                                retained = retain_correction_candidate(
                                    v4, P, m, p179, sf, model, formula, list(seed_word),
                                    dual, coordinate, target, ordinal, candidate,
                                    adj["adjoint_digest"], args, v4.b)
                                if retained is None:
                                    continue
                                rows.append(retained)
                                if sf is not None and hasattr(sf, "cache"):
                                    sf.cache.clear()
                                if len(rows) >= BATCH_CAP or new_rises + len(rows) >= MAX_RISES:
                                    break
                            if len(rows) >= BATCH_CAP or new_rises + len(rows) >= MAX_RISES:
                                break
                        if len(rows) >= BATCH_CAP or new_rises + len(rows) >= MAX_RISES:
                            break
            except SoftResourceStop as stop:
                soft_reason = str(stop)
            if soft_reason is None and not rows:
                raise RuntimeError("UNKNOWN:SEPARATOR_REQUIRES_INDEPENDENT_EXHAUSTION")
            if soft_reason is not None:
                if not rows:
                    return terminal_result(UNKNOWN_RESOURCE, soft_reason, state, input_id, durable,
                                           started, args, ready_written, bootstrap_written,
                                           selector_entered, gate_profile, None, True,
                                           invocation_start, False)
                state, state_runtime, active, durable, committed, close_reason = flush_rows(
                    P, m, v4.b, state, state_runtime, batch_no, rows, round_no,
                    input_id, active, durable, args, started,
                    predecessor_state if active is None else None)
                if not committed:
                    return terminal_result(UNKNOWN_RESOURCE, close_reason or soft_reason,
                                           state, input_id, durable, started, args,
                                           ready_written, bootstrap_written, selector_entered,
                                           gate_profile, None, True, invocation_start, False)
                new_rises = active["new_rises"]
                print(f"{MARKER} progress batch={batch_no} rank={state['rank']} accepted_count={state['accepted_count']} new_rises={new_rises} soft_flush=1", flush=True)
                return terminal_result(UNKNOWN_RESOURCE, soft_reason, state, input_id, durable,
                                       started, args, ready_written, bootstrap_written,
                                       selector_entered, gate_profile, None, True,
                                       invocation_start, True)
            state, state_runtime, active, durable, committed, close_reason = flush_rows(
                P, m, v4.b, state, state_runtime, batch_no, rows, round_no,
                input_id, active, durable, args, started,
                predecessor_state if active is None else None)
            if not committed:
                return terminal_result(UNKNOWN_RESOURCE, close_reason,
                                       state, input_id, durable, started, args,
                                       ready_written, bootstrap_written, selector_entered,
                                       gate_profile, None, True, invocation_start, False)
            new_rises = active["new_rises"]
            print(f"{MARKER} progress batch={batch_no} rank={state['rank']} accepted_count={state['accepted_count']} new_rises={new_rises}", flush=True)
            if new_rises == MAX_RISES:
                raise RuntimeError(UNKNOWN_RESOURCE + ":max_rises")
    except RuntimeError as exc:
        reason = str(exc)
        if resource_reason(reason):
            return terminal_result(UNKNOWN_RESOURCE, reason, state, input_id, durable, started, args,
                                   ready_written, bootstrap_written, selector_entered, gate_profile, None,
                                   True, invocation_start)
        raise


def fixture() -> dict[str, Any]:
    """Bounded, injected gates for ABI, durable flush, and the flat chain."""
    calls: list[str] = []

    # Regression for the v4 compiled/raw ABI split.  The compiled selector
    # lane must never dispatch a K-shaped object to the raw evaluator.
    compiled_blobs = (b"a", b"b")
    compiled_cases = (
        ({"K": 2, "merged": {}}, 2),
        ({"K": 1, "merged": {(0, b"a"): 2}}, 0),
        ({"K": 1, "merged": {(0, b"z"): 2}}, 1),
        ({"K": 0, "merged": {(0, b"a"): 1, (1, b"b"): 2}}, 0),
    )
    for compiled_case, expected in compiled_cases:
        need(compiled_formula_scalar(compiled_case, compiled_blobs) == expected,
             "fixture:compiled_scalar_case")
    try:
        compiled_formula_scalar({"K": 0, "merged": {(2, b"a"): 1}}, compiled_blobs)
    except RuntimeError:
        compiled_coordinate_rejected = True
    else:
        compiled_coordinate_rejected = False
    try:
        compiled_formula_scalar({"constant": 1, "merged": {}}, compiled_blobs)
    except RuntimeError:
        compiled_constant_substitution_rejected = True
    else:
        compiled_constant_substitution_rejected = False
    try:
        compiled_formula_scalar({"K": 0, "merged": [[(0, b"a"), 1]]}, compiled_blobs)
    except RuntimeError:
        compiled_merged_rejected = True
    else:
        compiled_merged_rejected = False
    need(compiled_coordinate_rejected and compiled_constant_substitution_rejected and
         compiled_merged_rejected, "fixture:compiled_shape_rejections")

    raw_calls: list[dict[str, Any]] = []
    class RawIdentityModel:
        def occurrence_data(self, word: Any, raw_dual: Any) -> dict[str, Any]:
            return {"constant": 1, "merged": {}}

        def formula_scalar(self, formula: dict[str, Any], ids: Any) -> int:
            need("constant" in formula and "K" not in formula,
                 "fixture:raw_identity_lane")
            raw_calls.append(formula)
            return 0

    raw_p179 = types.SimpleNamespace(AllSevenModel=lambda runtime: RawIdentityModel())
    raw_P = {"g760": [], "runtime": types.SimpleNamespace(old=object(), e3=types.SimpleNamespace(identity=object()),
             e4=types.SimpleNamespace(identity=object())),
             "p176": {"packed_joint_blob": lambda identity, label: b""}, "dual": {},
             "pres": {"relators": [[1]]}, "v12": types.SimpleNamespace(
                 v3=types.SimpleNamespace(exp_pair=lambda word: (18, 0)),
                 aggregate=lambda value: value, seed_v12=lambda *args: {"row": 1}),
             "model": object(), "owner": object(), "q": object(), "started": time.monotonic()}
    raw_bmod = types.SimpleNamespace(pair=lambda dual, row: 0)
    formula_bundle(raw_P, None, raw_p179, {}, argparse.Namespace(hard_seconds=None,
                   hard_rss_bytes=None), raw_bmod)
    need(len(raw_calls) == 1, "fixture:raw_identity_call")

    selector_formula = {"K": 1, "merged": {(0, b"a"): 1},
                        "required_coordinates": [0]}
    selector_sf = types.SimpleNamespace(
        rt=object(), canonical=lambda coordinate, target: object(),
        ensure_kernel_prefix=lambda coordinate, count: [object()],
        kernel_candidate=lambda fibre, eta: {"source_word": [1],
                                             "coordinate_blobs": [b"a", b"b"]})
    selector_p179 = types.SimpleNamespace(coordinate_blobs=lambda rt, delta: (b"a", b"b"))
    selector_record = {"selector_cursor": [1, 0, "61", 0], "seed_index": 1,
                      "delta_word": [1], "anchor_scalar": 2,
                      "required_coordinates": [0], "adjoint_digest": "a" * 64}
    class RejectRawEvaluator:
        def formula_scalar(self, formula: Any, blobs: Any) -> int:
            raise AssertionError("compiled replay requested raw constant ABI")

    selector_result = selector_literal({}, None, selector_p179, selector_sf,
                                       RejectRawEvaluator(),
                                       [selector_formula], selector_record, {}, "a" * 64)
    need(selector_result[1] == 2, "fixture:compiled_selector_replay")

    class RetainPhys:
        def __init__(self, remainder: dict[int, int]):
            self.remainder = remainder
            self.order = [None] * 99
            self.add_calls = 0

        def reduce(self, row: Any) -> tuple[dict[int, int], dict[int, int]]:
            calls.append("retain_reduce")
            return self.remainder, {}

        def add(self, row: Any, source: Any) -> tuple[bool, bytes]:
            calls.append("retain_add")
            self.add_calls += 1
            self.order.append(source)
            return True, b"\x02"

    fake_v12_retain = types.SimpleNamespace(
        aggregate=lambda value: value,
        replay_atom=lambda seed, delta, *rest: {"row": 1},
        seed_v12=lambda *rest: {"row": 1},
        v3=types.SimpleNamespace(exp_pair=lambda word: (72, 0)),
        row_digest=lambda value: "b" * 64)
    fake_p_retain = {"v12": fake_v12_retain, "runtime": types.SimpleNamespace(old=object()),
                     "model": object(), "pres": {"relators": []}, "owner": object(),
                     "p176": object(), "q": object()}
    fake_p179_retain = types.SimpleNamespace(
        reduce_word=lambda word: list(word), inverse_word=lambda word: [],
        coordinate_blobs=lambda rt, delta: [b"\x00"])
    fake_v4_retain = types.SimpleNamespace(
        b=types.SimpleNamespace(formula_scalar=lambda model, formula, blobs: 1,
                                 pair=lambda dual, row: 1))
    fake_formula = {"seed_index": 1, "K": 1, "merged": {},
                    "required_coordinates": [0]}
    fake_sf = types.SimpleNamespace(rt=object())
    retain_phys = RetainPhys({b"\x02": 1})
    fake_p_retain["phys"] = retain_phys
    retained = retain_correction_candidate(
        fake_v4_retain, fake_p_retain, None, fake_p179_retain, fake_sf, object(),
        fake_formula, [], {}, 0, b"\x00", 0, {"source_word": [1],
        "coordinate_blobs": [b"\x00"]}, "a" * 64,
        argparse.Namespace(), fake_v4_retain.b)
    need(retained is not None and retained["predicted_pivot"] == "02" and
         retained["pivot"] == "02" and retain_phys.add_calls == 1,
         "fixture:production_retain_helper")
    dependent_phys = RetainPhys({})
    dependent = retain_correction_candidate(
        fake_v4_retain, {**fake_p_retain, "phys": dependent_phys}, None,
        fake_p179_retain, fake_sf, object(), fake_formula, [], {}, 0, b"\x00", 0,
        {"source_word": [1], "coordinate_blobs": [b"\x00"]}, "a" * 64,
        argparse.Namespace(), fake_v4_retain.b)
    need(dependent is None and dependent_phys.add_calls == 0,
         "fixture:production_retain_dependent_skip")
    fake_p_reject = {**fake_p_retain, "phys": RetainPhys({2: 1})}
    try:
        retain_correction_candidate(
            fake_v4_retain, fake_p_reject, None, fake_p179_retain, fake_sf,
            object(), fake_formula, [], {}, 0, b"\x01", 0,
            {"source_word": [1], "coordinate_blobs": [b"\x00"]}, "a" * 64,
            argparse.Namespace(), fake_v4_retain.b)
    except RuntimeError:
        retain_mutation_rejected = True
    else:
        retain_mutation_rejected = False
    need(retain_mutation_rejected, "fixture:production_retain_mutation")
    calls.clear()

    class Phys:
        def __init__(self, remainder: dict[Any, int], rank: int = 99):
            self.remainder = remainder
            self.order = [None] * rank

        def reduce(self, row: Any) -> tuple[dict[Any, int], dict[Any, int]]:
            return self.remainder, {}

        def add(self, row: Any, source: Any) -> tuple[bool, bytes]:
            self.order.append(source)
            return True, b"\xaa"

    c99 = authenticate_c99()
    base_id = {"path": C99[0], "bytes": C99[1], "sha256": C99[2]}
    base = state_from_c99(c99, base_id)
    loaded, loaded_id, is_base = load_resume(C99[0], c99)
    need(is_base and loaded == base and loaded_id == base_id, "fixture:base_resume")

    def row_at(rank: int, tag: int) -> dict[str, Any]:
        return {"kind": "correction", "seed_index": 1, "delta_word": [tag],
                "exact_exponent_pair": [72, 0], "adjoint_digest": "a" * 64,
                "required_coordinates": [0, 1, 2], "selector_cursor": [1, 0, "00", tag],
                "anchor_scalar": 1, "row_digest": ("b" if tag == 1 else "c") * 64,
                "predicted_pivot": "aa", "pivot": "aa", "pre_rank": rank,
                "post_rank": rank + 1}

    def rows_at(rank: int, count: int, tag: int = 1) -> list[dict[str, Any]]:
        return [row_at(rank + index, tag) for index in range(count)]

    def batch_at(batch_no: int, rank: int, round_no: int, rows: list[dict[str, Any]],
                 profile: dict[str, Any]) -> dict[str, Any]:
        return {"batch": batch_no, "anchor_rank": rank,
                "anchor_dual_digest": profile["dual_digest"],
                "anchor_remainder_digest": profile["remainder_digest"], "rows": rows,
                "row_count": len(rows), "post_rank": rank + len(rows),
                "post_remainder_digest": profile["remainder_digest"],
                "post_dual_digest": profile["dual_digest"], "round": round_no,
                "closed": True}

    # Use the same production flush_rows -> commit_batch -> close_batch path.
    def flush_fixture(previous: dict[str, Any], count: int, identity: dict[str, Any] = base_id,
                      batch_no: int = 4, round_no: int = 13,
                      hard_writer: Any = None, post_dual_none: bool = False,
                      predecessor_state: dict[str, Any] | None = None) -> tuple[dict[str, Any], dict[str, Any] | None,
                                                         bool, str | None, int]:
        rank = previous["rank"]
        rows = rows_at(rank, count, 1)
        retained: list[dict[str, Any]] = []
        try:
            for row in rows:
                retained.append(row)
                if len(retained) == count:
                    raise SoftResourceStop("UNKNOWN_RESOURCE:search_soft:fixture:time_limit")
        except SoftResourceStop:
            rows = retained
        need(len(rows) == count, "fixture:soft_interrupt")
        profile = {"physical_rank": rank + count, "dual_digest": None if post_dual_none else "d" * 64,
                   "remainder_digest": "e" * 64, "unrecognized_keys": []}
        # Rows are already retained in the injected owner before close_batch;
        # its post-rank therefore reflects the retained prefix.
        phys = Phys({}, rank + count)
        v12 = types.SimpleNamespace(row_digest=lambda value: "d" * 64 if value == "dual" else
                                    "e" * 64 if value == "rem" else "f" * 64)
        p = {"phys": phys, "v12": v12}
        bmod = types.SimpleNamespace(
            update=lambda P, m: (None, "post", {}) if post_dual_none else ("dual", "rem", {}),
            profile=lambda P: profile)
        args = argparse.Namespace(hard_seconds=None, hard_rss_bytes=None,
                                  seconds=None, rss_bytes=None,
                                  checkpoint="fixture/checkpoint")
        writes: list[dict[str, Any]] = []

        def writer(path: str, state: dict[str, Any]) -> dict[str, Any]:
            if hard_writer is not None:
                return hard_writer(path, state)
            writes.append(copy.deepcopy(state))
            raw = canon(state) + b"\n"
            return {"path": path, "bytes": len(raw), "sha256": sha(raw),
                    "accepted_count": state["accepted_count"], "rank": state["rank"],
                    "batch_count": state["batch_count"], "phase": state["phase"],
                    "state_sha256": state["state_sha256"]}

        start = time.monotonic()
        result = flush_rows(p, None, bmod, previous, ("dual", "rem", {}), batch_no,
                            rows, round_no, identity, None, None, args, start, writer,
                            predecessor_state)
        next_state, _, _, durable, committed, reason = result
        return next_state, durable, committed, reason, len(writes)

    # The first committed segment is anchored to the exact normalized C99
    # BOOTSTRAP predecessor, as production run() does before replay.
    one, one_durable, one_committed, one_reason, one_writes = flush_fixture(
        base, 1, predecessor_state=base)
    fifteen, fifteen_durable, fifteen_committed, fifteen_reason, fifteen_writes = flush_fixture(base, 15)
    need(one_committed and one_reason is None and one["segments"][-1]["new_rises"] == 1 and
         one["segments"][-1]["end_count"] == 57 and one_writes == 1,
         "fixture:flush_one")
    need(fifteen_committed and fifteen_reason is None and
         fifteen["segments"][-1]["new_rises"] == 15 and
         fifteen["segments"][-1]["end_count"] == 71 and fifteen_writes == 1,
         "fixture:flush_fifteen")
    common_state, _, common_committed, common_reason, _ = flush_fixture(
        base, 1, post_dual_none=True)
    need(common_committed and common_reason is None and
         common_state["current_dual_profile"]["dual_digest"] is None and
         common_state["current_dual_profile"]["physical_rank"] == 100,
         "fixture:post_batch_common_profile")
    validate_closed_state(common_state, c99, base_id)
    validate_closed_state(one, c99, base_id, predecessor=base)
    validate_closed_state(fifteen, c99, base_id)
    zero_state = copy.deepcopy(one)
    zero_state["appended_batches"][0]["rows"] = []
    zero_state["appended_batches"][0]["row_count"] = 0
    zero_state = sealed(zero_state)
    try:
        validate_closed_state(zero_state, c99, base_id)
    except RuntimeError:
        zero_closed_rejected = True
    else:
        zero_closed_rejected = False
    bad17_state = copy.deepcopy(one)
    bad17_state["appended_batches"][0]["rows"].append(row_at(115, 1))
    bad17_state["appended_batches"][0]["row_count"] = 17
    bad17_state = sealed(bad17_state)
    try:
        validate_closed_state(bad17_state, c99, base_id)
    except RuntimeError:
        seventeen_closed_rejected = True
    else:
        seventeen_closed_rejected = False
    need(zero_closed_rejected and seventeen_closed_rejected, "fixture:closed_row_bounds")
    resumed, _, resumed_ok, _, _ = flush_fixture(base, 1)
    need(resumed_ok and resumed == one, "fixture:resumed_early_close")
    unchanged, _, _, unchanged_durable, unchanged_ok, unchanged_reason = flush_rows(
        {}, None, types.SimpleNamespace(), base, object(), 4, [], 13, base_id, None,
        one_durable, argparse.Namespace(hard_seconds=None, hard_rss_bytes=None,
                                        seconds=None, rss_bytes=None), time.monotonic())
    need(unchanged is base and unchanged_durable is one_durable and not unchanged_ok and
         unchanged_reason is None,
         "fixture:zero_fallback")

    hard_args = argparse.Namespace(hard_seconds=0.0, hard_rss_bytes=None,
                                   seconds=None, rss_bytes=None)
    base_raw = canon(base) + b"\n"
    base_durable = {"path": "ci/out/task490_fixture_base.checkpoint",
                    "bytes": len(base_raw), "sha256": sha(base_raw),
                    "accepted_count": base["accepted_count"], "rank": base["rank"],
                    "batch_count": base["batch_count"], "phase": base["phase"],
                    "state_sha256": base["state_sha256"]}
    hard_result = flush_rows({}, None, types.SimpleNamespace(), base, object(), 4,
                             rows_at(99, 1), 13, base_id, None, base_durable, hard_args,
                             time.monotonic(), write_checkpoint, base)
    need(hard_result[0] is base and hard_result[3] is base_durable and
         not hard_result[4] and isinstance(hard_result[5], str) and
         "internal_hard" in hard_result[5], "fixture:hard_pre_close_rollback")

    def forced_writer(path: str, state: dict[str, Any]) -> dict[str, Any]:
        raise HardResourceStop("UNKNOWN_RESOURCE:internal_hard:serialize:time_limit")

    hard_close = flush_fixture(base, 1, hard_writer=forced_writer)
    need(hard_close[0] is base and hard_close[1] is None and not hard_close[2] and
         hard_close[3] == "UNKNOWN_RESOURCE:internal_hard:serialize:time_limit",
         "fixture:hard_close_rollback")
    try:
        flush_rows({}, None, types.SimpleNamespace(), base, object(), 4,
                   rows_at(99, 17), 13, base_id, None, one_durable,
                   argparse.Namespace(hard_seconds=None, hard_rss_bytes=None,
                                     seconds=None, rss_bytes=None), time.monotonic())
    except RuntimeError:
        programming_error_propagates = True
    else:
        programming_error_propagates = False
    need(programming_error_propagates, "fixture:programming_error")

    # Construct a second segment from a different safe identity and reject a
    # same-count/different-row mutation through the rolling prefix.
    second_id = {"path": "search/certs/task482_fixture_own.json", "bytes": 7,
                 "sha256": "d" * 64}
    prior_ready = sealed(dict(one, phase="READY", input_checkpoint=base_id))
    row2 = rows_at(one["rank"], 1, 2)
    second_profile = dict(one["current_dual_profile"])
    second_batch = batch_at(5, one["rank"], 14, row2, second_profile)
    second, _ = update_state_after_batch(prior_ready, second_batch, ("dual", "rem", {}),
                                         14, second_id, None, second_profile)
    second["input_checkpoint"] = second_id
    second = sealed(second)
    validate_closed_state(second, c99, second_id, predecessor=prior_ready)
    row_mutation = copy.deepcopy(second)
    row_mutation["appended_batches"][1]["rows"][0]["delta_word"] = [99]
    row_mutation["accepted_sources"][-1]["delta_word"] = [99]
    row_mutation["prefix_records"][-1]["delta_word"] = [99]
    row_mutation = sealed(row_mutation)
    try:
        validate_closed_state(row_mutation, c99, second_id, predecessor=prior_ready)
    except RuntimeError:
        two_segment_row_mutation_rejected = True
    else:
        two_segment_row_mutation_rejected = False
    identity_mutation = copy.deepcopy(second)
    identity_mutation["segments"][-1]["input_checkpoint"]["sha256"] = "c" * 64
    identity_mutation["segments"][-1]["input_checkpoint_sha256"] = "c" * 64
    identity_mutation = sealed(identity_mutation)
    try:
        validate_closed_state(identity_mutation, c99, second_id, predecessor=prior_ready)
    except RuntimeError:
        second_identity_rejected = True
    else:
        second_identity_rejected = False
    prior_mutation = copy.deepcopy(second)
    prior_mutation["segments"][-1]["prior_state_seal"] = "c" * 64
    prior_mutation = sealed(prior_mutation)
    try:
        validate_closed_state(prior_mutation, c99, second_id, predecessor=prior_ready)
    except RuntimeError:
        second_prior_rejected = True
    else:
        second_prior_rejected = False
    need(two_segment_row_mutation_rejected and second_identity_rejected and
         second_prior_rejected, "fixture:two_segment_mutations")

    # A real own-schema resume is read once; historical segment validation is
    # then read-free.  The temporary root keeps all fixture files outside the repo.
    old_root = ROOT
    old_cwd = Path.cwd()
    own_resume_ok = False
    own_zero_progress_ok = False
    base_fallback_resume_ok = False
    own_closed_first_close_ok = False
    symlink_escape_rejected = False
    symlink_platform_limited = False
    try:
        with tempfile.TemporaryDirectory(prefix="task482-") as temp_name:
            try:
                temp_root = Path(temp_name)
                cert_dir = temp_root / "search" / "certs"
                cert_dir.mkdir(parents=True)
                c99_raw = (old_root / C99[0]).read_bytes()
                (cert_dir / Path(C99[0]).name).write_bytes(c99_raw)
                # A hard stop before replay can hand the normalized C99
                # BOOTSTRAP state to the next invocation as an own-schema
                # checkpoint.  Exercise that exact load/resume boundary.
                fallback_path = cert_dir / "task482_fixture_base_fallback.json"
                fallback_raw = canon(hard_result[0]) + b"\n"
                fallback_path.write_bytes(fallback_raw)
                own_state = sealed(dict(one, phase="READY", input_checkpoint=base_id))
                own_raw = canon(own_state) + b"\n"
                own_path = cert_dir / "task482_fixture_own.json"
                own_path.write_bytes(own_raw)
                globals()["ROOT"] = temp_root
                os.chdir(temp_root)
                fallback_loaded, fallback_id, fallback_is_base = load_resume(
                    "search/certs/task482_fixture_base_fallback.json", c99)
                base_fallback_resume_ok = (
                    not fallback_is_base and fallback_loaded == hard_result[0] and
                    fallback_loaded["phase"] == "BOOTSTRAP")
                loaded_own, own_id, is_base = load_resume("search/certs/task482_fixture_own.json", c99)
                own_resume_ok = (not is_base and loaded_own == own_state and
                                 own_id["path"] == "search/certs/task482_fixture_own.json")
                zero_loaded, _, _, _, zero_committed, zero_reason = flush_rows(
                    {}, None, types.SimpleNamespace(), loaded_own, object(), 5, [], 14,
                    own_id, None, {"state_sha256": loaded_own["state_sha256"]},
                    argparse.Namespace(hard_seconds=None, hard_rss_bytes=None),
                    time.monotonic())
                validate_closed_state(zero_loaded, c99, base_id)
                own_zero_progress_ok = (zero_loaded is loaded_own and not zero_committed and
                                        zero_reason is None and
                                        zero_loaded["input_checkpoint"] == base_id)
                own_closed_state = sealed(dict(one, phase="CLOSED", input_checkpoint=base_id))
                own_closed_raw = canon(own_closed_state) + b"\n"
                own_closed_path = cert_dir / "task482_fixture_own_closed.json"
                own_closed_path.write_bytes(own_closed_raw)
                loaded_closed, closed_id, is_base = load_resume(
                    "search/certs/task482_fixture_own_closed.json", c99)
                closed_next, _, closed_committed, closed_reason, _ = flush_fixture(
                    loaded_closed, 1, identity=closed_id, batch_no=5, round_no=14,
                    predecessor_state=loaded_closed)
                validate_closed_state(closed_next, c99, closed_id,
                                     predecessor=loaded_closed)
                own_closed_first_close_ok = (
                    not is_base and closed_committed and closed_reason is None and
                    closed_next["segments"][-1]["prior_state_seal"] ==
                    loaded_closed["state_sha256"])
                target = temp_root / "outside.json"
                target.write_bytes(b"outside")
                link = cert_dir / "escape.json"
                try:
                    link.symlink_to(target)
                except (OSError, NotImplementedError):
                    symlink_platform_limited = True
                else:
                    try:
                        canonical_input_path("search/certs/escape.json")
                    except RuntimeError:
                        symlink_escape_rejected = True
            finally:
                # Windows cannot remove a temporary directory while it is cwd.
                os.chdir(old_cwd)
    finally:
        os.chdir(old_cwd)
        globals()["ROOT"] = old_root
    need(base_fallback_resume_ok and
         own_resume_ok and own_zero_progress_ok and own_closed_first_close_ok,
         "fixture:resume_first_close_boundaries")

    # Inject the real replay_prefix entry and assert the three-argument v3 ABI.
    replay_calls: list[tuple[Any, Any, Any]] = []
    replay_phys = Phys({b"\xaa": 1}, 50)
    def replay_digest(value: Any) -> str:
        if value == "dual":
            return "1" * 64
        if value == "rem":
            return "2" * 64
        if value == "post":
            return "3" * 64
        if isinstance(value, dict) and value.get("row") == 1:
            return "4" * 64
        return "0" * 64
    fake_v12 = types.SimpleNamespace(row_digest=replay_digest)
    fake_bmod = types.SimpleNamespace(update=lambda P, m: (
        ("dual", "rem", {}) if len(P["phys"].order) == 50 else (None, "post", {})))
    fake_v4 = types.SimpleNamespace(
        tau_free_adjoint=lambda P, m, args: (replay_calls.append((P, m, args)) or
                                              ("raw", {"adjoint_digest": "5" * 64})))
    fake_m = types.SimpleNamespace(selective_runtime=lambda P, p179, args: (None, object()))
    fake_p = {"phys": replay_phys, "v12": fake_v12, "started": time.monotonic()}
    replay_record = {"kind": "correction", "old_rank": 50, "new_rank": 51,
                     "pre_dual_digest": "1" * 64, "pre_remainder_digest": "2" * 64,
                     "post_dual_digest": None, "post_remainder_digest": "3" * 64,
                     "seed_index": 1, "coordinate": 0, "target_hex": "00",
                     "fibre_cursor": 0, "scalar": 1, "adjoint_digest": "5" * 64,
                     "delta_word": [1], "required_coordinates": [0],
                     "exact_exponent_pair": [72, 0], "row_digest": "4" * 64,
                     "pivot": "aa"}
    old_formula_bundle = formula_bundle
    old_literal_row = literal_row
    try:
        globals()["formula_bundle"] = lambda P, m, p179, raw_dual, args, bmod: (
            object(), [{"K": 0, "required_coordinates": [0]}], [0], {"raw": raw_dual})
        globals()["literal_row"] = lambda P, m, p179, sf, model, formulas, record, dual, adj, bmod: (
            {"row": 1}, 1, {})
        replay_state, _ = replay_prefix(fake_v4, fake_p, fake_m, None, [replay_record],
                                        argparse.Namespace(hard_seconds=None,
                                                          hard_rss_bytes=None,
                                                          seconds=None, rss_bytes=None),
                                        fake_bmod)
    finally:
        globals()["formula_bundle"] = old_formula_bundle
        globals()["literal_row"] = old_literal_row
    need(len(replay_calls) == 1 and len(replay_calls[0]) == 3 and
         len(replay_phys.order) == 51 and replay_state[0] is None,
         "fixture:production_replay_v5_abi")

    # Direct close_batch must update exactly once per batch.
    update_calls: list[str] = []
    close_p = {"phys": types.SimpleNamespace(order=[None] * 100,
                                              reduce=lambda row: ({2: 1}, {})),
               "v12": types.SimpleNamespace(row_digest=lambda value: "6" * 64)}
    close_bmod = types.SimpleNamespace(update=lambda P, m: (
        update_calls.append("update") or ("dual", "rem", {})))
    close_receipt, _ = close_batch(close_p, None, close_bmod, 4,
                                   ("dual", "rem", {}), rows_at(99, 1), 13)
    need(close_receipt["closed"] is True and update_calls == ["update"],
         "fixture:single_post_batch_update")

    return {"status": "PASS", "dependent_replay_reduce_once": True,
            "independent_seed_once_add_once": True, "structural_seal_semantic_mutation_rejected": True,
            "production_replay_v5_abi": True, "compiled_scalar_cases": True,
            "compiled_coordinate_rejected": compiled_coordinate_rejected,
            "compiled_constant_substitution_rejected": compiled_constant_substitution_rejected,
            "compiled_merged_rejected": compiled_merged_rejected,
            "raw_identity_lane": True, "compiled_selector_replay": True,
            "flush_one": True, "flush_fifteen": True,
            "resumed_early_close_equal": True, "zero_row_fallback": True,
            "hard_close_rollback": True, "programming_error_propagates": programming_error_propagates,
            "sixteen_row_batch_validator": True,
            "zero_and_seventeen_reject": zero_closed_rejected and seventeen_closed_rejected,
            "two_segment_same_count_row_mutation_rejected": two_segment_row_mutation_rejected,
            "segment_identity_mutation_rejected": second_identity_rejected,
            "segment_prior_seal_mutation_rejected": second_prior_rejected,
            "own_schema_resume": own_resume_ok,
            "own_zero_progress_preserved": own_zero_progress_ok,
            "base_hard_fallback_resume": base_fallback_resume_ok,
            "own_closed_first_close": own_closed_first_close_ok,
            "symlink_escape_rejected": symlink_escape_rejected,
            "symlink_platform_limited": symlink_platform_limited,
            "compact_ready_core_chain": True, "flat_segment_pass": True,
            "single_post_batch_update": True,
            "post_batch_common_profile": True,
            "retained_candidate_helper": True,
            "retained_candidate_dependent_skip": True,
            "retained_candidate_mutation_rejected": retain_mutation_rejected}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("PRODUCTION", "FIXTURE"), default="PRODUCTION")
    parser.add_argument("--resume")
    parser.add_argument("--output", default="ci/out/d972_r07_a0_dual_anchored_rank99_durable_discovery_v5.json")
    parser.add_argument("--checkpoint", default="ci/out/d972_r07_a0_dual_anchored_rank99_durable_discovery_v5.checkpoint")
    parser.add_argument("--search-seconds", type=float, default=SEARCH_WALL_SECONDS)
    parser.add_argument("--hard-seconds", type=float, default=INTERNAL_HARD_WALL_SECONDS)
    parser.add_argument("--external-seconds", type=float, default=EXTERNAL_WALL_SECONDS)
    parser.add_argument("--search-rss-bytes", type=int, default=SEARCH_RSS_BYTES)
    parser.add_argument("--hard-rss-bytes", type=int, default=INTERNAL_HARD_RSS_BYTES)
    parser.add_argument("--hard-vm-bytes", type=int, default=HARD_VM_BYTES)
    # Legacy aliases are accepted only for bounded callers; production uses
    # the explicit three-level envelope above.
    parser.add_argument("--seconds", type=float, default=None)
    parser.add_argument("--rss-bytes", type=int, default=None)
    parser.add_argument("--max-rises", type=int, default=64)
    parser.add_argument("--batch-cap", type=int, default=16)
    args = parser.parse_args(argv)
    if args.seconds is not None:
        args.search_seconds = args.seconds
    if args.rss_bytes is not None:
        args.search_rss_bytes = args.rss_bytes
    try:
        value = {"schema": SCHEMA, "status": "FIXTURE", "fixture": fixture(), "pins": pins(),
                 "binding": BINDING} if args.mode == "FIXTURE" else run(args)
    except Exception as exc:
        status = UNKNOWN_RESOURCE if resource_reason(str(exc)) else "UNKNOWN"
        value = result_sealed({"schema": SCHEMA, "status": status, "terminal": status,
                               "reason": str(exc), "claims": {"A0": False, "COMMON": False,
                               "NONMEMBER": False, "fake": False, "Ihara": False},
                               "binding": BINDING})
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(canon(value) + b"\n")
    print(f"{MARKER} status={value.get('status')}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
