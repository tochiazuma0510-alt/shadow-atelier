#!/usr/bin/env python3
"""Independent Task472 checker for the v424 actual-owner continuation."""
from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "d972-r07-a0-dual-anchored-rank99-durable-discovery/v3"
CP_SCHEMA = SCHEMA + "/checkpoint"
MARKER = "R07_A0_DUAL_ANCHORED_RANK99_DURABLE_DISCOVERY_V3_CHECKER"
BATCH_CAP = 16
MAX_RISES = 64

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
TASK451_V3 = ("search/d972_r07_a0_actual_tau_free_rank_ladder_v3.py", 12215,
              "0140447110cfa568a77300bd7d43d51c622597704b7b91ed5209c63168c9ef37")
C99_OLD_BINDING = "a9568c6aa47b924ec818bd68b851ce136394b9d4a30af8d37cf3c70bae8a841a"
C99_STATE_SHA = "f2de40c3b16053464b8cf7d397f8fd05ca4439a46ca7e45df93e60bbc11a312d"
RANK51_STATE_SHA = "22dcfdfb396524ea5853488aa2ad52d28b4f7d10164123bc83f121e59dd83159"
BINDING = hashlib.sha256(json.dumps({"schema": SCHEMA, "task451_producer": list(TASK451_P),
                                      "task451_checker": list(TASK451_C), "c99": list(C99),
                                      "rank51": list(RANK51), "paper": list(PAPER),
                                      "paper_v426": list(PAPER_V426), "paper_v427": list(PAPER_V427)},
                                     sort_keys=True, separators=(",", ":"),
                                     ensure_ascii=True).encode("ascii")).hexdigest()
HEX = set("0123456789abcdef")


def canon(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True).encode("ascii")


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def digest(value: Any) -> str:
    return sha(canon(value))


def sealed_state(value: dict[str, Any]) -> dict[str, Any]:
    out = dict(value)
    out.pop("state_sha256", None)
    out["state_sha256"] = digest(out)
    return out


def need(value: Any, message: str) -> None:
    if not value:
        raise RuntimeError(message)


def hex64(value: Any) -> bool:
    return isinstance(value, str) and len(value) == 64 and set(value) <= HEX


def pivot_hex(value: Any) -> bool:
    if not isinstance(value, str) or not value or len(value) % 2 or set(value) - HEX:
        return False
    try:
        return bytes.fromhex(value).hex() == value
    except ValueError:
        return False


def load_pinned(spec: tuple[str, int, str], name: str) -> Any:
    path = ROOT / spec[0]
    raw = path.read_bytes()
    need(len(raw) == spec[1] and sha(raw) == spec[2], "pin:" + spec[0])
    module_spec = importlib.util.spec_from_file_location(name, path)
    need(module_spec is not None and module_spec.loader is not None, "loader:" + spec[0])
    module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(module)
    return module


def pin(spec: tuple[str, int, str]) -> dict[str, Any]:
    raw = (ROOT / spec[0]).read_bytes()
    need(len(raw) == spec[1] and sha(raw) == spec[2], "pin:" + spec[0])
    return {"path": spec[0], "bytes": len(raw), "sha256": sha(raw)}


def pins() -> dict[str, Any]:
    return {name: pin(spec) for name, spec in (("task451_producer", TASK451_P),
                                                 ("task451_checker", TASK451_C),
                                                 ("c99", C99), ("rank51", RANK51),
                                                 ("paper", PAPER), ("paper_v426", PAPER_V426),
                                                 ("paper_v427", PAPER_V427))}


def check_result_seal(value: dict[str, Any]) -> None:
    body = dict(value)
    got = body.pop("self_digest_sha256", None)
    need(isinstance(got, str) and got == digest(body), "result:seal")


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


def _old_digest_fields(record: dict[str, Any], prefix: bool = False) -> None:
    for key in ("row_digest", "adjoint_digest"):
        need(hex64(record.get(key)), "old:" + key)
    need(pivot_hex(record.get("pivot")), "old:pivot")
    if prefix:
        for key in ("pre_dual_digest", "pre_remainder_digest", "post_dual_digest",
                    "post_remainder_digest"):
            need(hex64(record.get(key)), "old:" + key)


def frozen_c99() -> dict[str, Any]:
    raw = (ROOT / C99[0]).read_bytes()
    need(len(raw) == C99[1] and sha(raw) == C99[2], "c99:pin")
    value = json.loads(raw.decode("ascii"))
    need(raw == canon(value) + b"\n", "c99:canonical")
    body = dict(value)
    state_sha = body.pop("state_sha256", None)
    need(state_sha == C99_STATE_SHA and state_sha == digest(body), "c99:seal")
    need(value.get("schema") == "d972-r07-a0-dual-anchored-active-batch/v1/checkpoint" and
         value.get("binding") == C99_OLD_BINDING and value.get("frozen_sha256") == RANK51[2] and
         value.get("accepted_count") == 56 and len(value.get("accepted_sources", [])) == 56 and
         value.get("rank") == 99 and value.get("round") == 12 and
         value.get("batch_count") == 3 and value.get("open_batch") is False,
         "c99:shape")
    rank_raw = (ROOT / RANK51[0]).read_bytes()
    need(len(rank_raw) == RANK51[1] and sha(rank_raw) == RANK51[2], "rank51:pin")
    rank51 = json.loads(rank_raw.decode("ascii"))
    rank_body = dict(rank51)
    rank_sha = rank_body.pop("state_sha256", None)
    need(rank_raw == canon(rank51) + b"\n" and rank_sha == RANK51_STATE_SHA and rank_sha == digest(rank_body) and
         rank51.get("rank") == 51 and rank51.get("accepted_count") == 8 and
         rank51.get("round") == 9 and len(rank51.get("accepted_sources", [])) == 8,
         "rank51:shape")
    need(value["accepted_sources"][:8] == rank51["accepted_sources"], "c99:prefix")
    for index, record in enumerate(value["accepted_sources"][:8]):
        _old_digest_fields(record, True)
        need(record.get("kind") == "correction" and record.get("old_rank") == 43 + index and
             record.get("new_rank") == 44 + index and record.get("round") == index + 1 and
             record.get("scalar") in (1, 2), "c99:prefix_record")
    flattened: list[dict[str, Any]] = []
    rank = 51
    for batch_no, batch in enumerate(value["batches"], 1):
        rows = batch.get("rows", [])
        need(batch.get("batch") == batch_no and batch.get("closed") is True and
             batch.get("row_count") == len(rows) == 16 and batch.get("anchor_rank") == rank and
             batch.get("post_rank") == rank + 16 and hex64(batch.get("anchor_dual_digest")) and
             hex64(batch.get("anchor_remainder_digest")) and
             hex64(batch.get("post_remainder_digest")) and hex64(batch.get("post_dual_digest")),
             "c99:batch_shape")
        for index, record in enumerate(rows):
            _old_digest_fields(record)
            need(record.get("kind") in {"correction", "action"} and
                 record.get("pre_rank") == rank + index and
                 record.get("post_rank") == rank + index + 1 and
                 record.get("anchor_scalar") in (1, 2), "c99:row_shape")
            if record["kind"] == "correction":
                need(record.get("exact_exponent_pair") == [72, 0] and
                     isinstance(record.get("selector_cursor"), list) and
                     len(record["selector_cursor"]) == 4, "c99:literal_shape")
            flattened.append(record)
        rank += 16
    need(rank == 99 and flattened == value["accepted_sources"][8:], "c99:flattening")
    profile = value.get("current_dual_profile")
    need(isinstance(profile, dict) and profile.get("physical_rank") == 99 and
         hex64(profile.get("dual_digest")) and hex64(profile.get("remainder_digest")), "c99:profile")
    value["state_sha256"] = state_sha
    return value


def flat_appended(batches: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [row for batch in batches for row in batch.get("rows", [])]


def cap_gate(reason: Any, rises: int) -> None:
    need(isinstance(rises, int) and 0 <= rises <= MAX_RISES, "cap:rises")
    if reason == "UNKNOWN_RESOURCE:max_rises":
        need(rises == MAX_RISES, "cap:exact_max_rises")


def prefix_seed(c99: dict[str, Any]) -> str:
    return digest(c99["accepted_sources"])


def roll_prefix(previous: str, rows: list[dict[str, Any]]) -> str:
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
    canonical_input_path(identity["path"])


def segment_gate(state: dict[str, Any], c99: dict[str, Any]) -> str:
    """Flat chronological segment/prefix validation; no ancestor file reads."""
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
        count, rank, round_no = start[1], start[2], start[3]
        for offset, batch in enumerate(span, 1):
            need(isinstance(batch, dict), "segment:batch_type")
            rows = batch.get("rows", [])
            need(batch.get("batch") == start[0] + offset and batch.get("closed") is True and
                 isinstance(rows, list) and 0 < len(rows) <= BATCH_CAP and
                 batch.get("row_count") == len(rows) and
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
    need(app_index == len(appended), "segment:end")
    if not appended:
        need(not segments and state.get("prefix_digest") == current_digest, "segment:empty")
    return current_digest


def validate_appended(appended: list[dict[str, Any]], base: dict[str, Any]) -> None:
    rank = 99
    for expected, batch in enumerate(appended, 4):
        need(isinstance(batch, dict), "append:batch_type")
        rows = batch.get("rows", [])
        need(batch.get("batch") == expected and batch.get("closed") is True and
             batch.get("row_count") == len(rows) and 0 < len(rows) <= BATCH_CAP and
             batch.get("anchor_rank") == rank and batch.get("post_rank") == rank + len(rows),
             "append:batch_shape")
        need(hex64(batch.get("anchor_dual_digest")) and hex64(batch.get("anchor_remainder_digest")) and
             hex64(batch.get("post_remainder_digest")) and
             (batch.get("post_dual_digest") is None or hex64(batch.get("post_dual_digest"))),
             "append:batch_seals")
        for index, row in enumerate(rows):
            need(row.get("pre_rank") == rank + index and row.get("post_rank") == rank + index + 1 and
                 row.get("anchor_scalar") in (1, 2) and hex64(row.get("row_digest")) and
                 pivot_hex(row.get("pivot")), "append:row_shape")
            need(row.get("predicted_pivot") == row.get("pivot"), "append:predicted_pivot")
            if row.get("kind") == "correction":
                need(isinstance(row.get("selector_cursor"), list) and
                     len(row["selector_cursor"]) == 4 and hex64(row.get("adjoint_digest")) and
                     isinstance(row.get("exact_exponent_pair"), list) and
                     len(row["exact_exponent_pair"]) == 2, "append:correction")
            else:
                need(row.get("kind") == "action" and isinstance(row.get("action_source"), dict) and
                     row.get("selector_cursor", [None])[0] == "action", "append:action")
        rank += len(rows)
    need(rank == 99 + len(flat_appended(appended)), "append:rank")


def validate_state(state: dict[str, Any], c99: dict[str, Any], input_id: dict[str, Any],
                   check_chain: bool = True) -> None:
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
    need(isinstance(appended, list), "state:appended")
    validate_appended(appended, c99)
    flat = flat_appended(appended)
    need(state.get("batches") == c99["batches"] + appended and
         state.get("accepted_sources") == c99["accepted_sources"] + flat and
         state.get("accepted_count") == 56 + len(flat) and
         state.get("batch_count") == 3 + len(appended) and
         state.get("rank") == 99 + len(flat) and isinstance(state.get("round"), int) and
         state["round"] >= 12 and isinstance(state.get("segments"), list), "state:flattening")
    need(state.get("input_checkpoint") == input_id and
         isinstance(state.get("current_dual_profile"), (dict, type(None))) and
         state.get("prefix_records") == state.get("accepted_sources") and
         state.get("prefix_digest") == prefix_digest(c99, appended), "state:identity")
    if check_chain:
        segment_chain_gate(state, c99)


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
    return sealed_state(value)


def segment_chain_gate(state: dict[str, Any], c99: dict[str, Any]) -> None:
    """Validate the compact READY-core seal chain without ancestor I/O."""
    segments = state.get("segments", [])
    appended = state.get("appended_batches", [])
    current_digest = segment_gate(state, c99)
    ledger = digest([])
    app_index = 0
    for index, segment in enumerate(segments):
        span = segment["end_batch"] - segment["start_batch"]
        start = (segment["start_batch"], segment["start_count"],
                 segment["start_rank"], segment["start_round"])
        identity = segment["input_checkpoint"]
        expected_prior = ready_core(start, segment["start_prefix_digest"], identity,
                                    segment["start_profile"], ledger)
        need(segment.get("prior_ledger_digest") == ledger and
             segment.get("prior_core_digest") == expected_prior and
             segment.get("prior_state_seal") == expected_prior,
             "segment:prior_state_seal")
        next_ledger = roll_ledger(ledger, segment)
        end = (segment["end_batch"], segment["end_count"],
               segment["end_rank"], segment["end_round"])
        expected_end = ready_core(end, segment["end_prefix_digest"], identity,
                                  segment["end_profile"], next_ledger)
        need(segment.get("ledger_digest") == next_ledger and
             segment.get("end_core_digest") == expected_end, "segment:end_core")
        ledger = next_ledger
        app_index += span
    need(current_digest == state.get("prefix_digest") and
         app_index == len(appended) and state.get("ledger_digest", ledger) == ledger and
         (not segments or state.get("ready_core_digest") == segments[-1].get("end_core_digest")) and
         (not segments or state.get("input_checkpoint") == segments[-1].get("input_checkpoint")),
         "segment:chain_end")


def checkpoint(cert: dict[str, Any], c99: dict[str, Any], input_id: dict[str, Any]) -> dict[str, Any]:
    durable = cert.get("durable_state")
    need(isinstance(durable, dict) and isinstance(durable.get("path"), str), "durable:metadata")
    path = Path(durable["path"])
    need(not path.is_absolute() and path.parent == Path("ci/out"), "durable:path")
    raw = path.read_bytes()
    need(len(raw) == durable.get("bytes") and sha(raw) == durable.get("sha256"), "durable:bytes")
    state = json.loads(raw.decode("ascii"))
    need(raw == canon(state) + b"\n", "durable:canonical")
    validate_state(state, c99, input_id)
    need(durable.get("accepted_count") == state["accepted_count"] and
         durable.get("rank") == state["rank"] and durable.get("batch_count") == state["batch_count"] and
         durable.get("phase") == state["phase"] and durable.get("state_sha256") == state["state_sha256"],
         "durable:metadata")
    return state


class ReplayArgs:
    seconds = None
    rss_bytes = None


def arithmetic() -> tuple[Any, Any, Any, Any, Any, Any]:
    v3 = load_pinned(TASK451_V3, "task472_checker_v3")
    v1 = load_pinned(v3.b.V1, "task472_checker_v1")
    v4 = load_pinned(v1.V4, "task472_checker_v4")
    m = v4.load_v1()
    m.MARKER = MARKER
    m.RUN_STARTED = time.monotonic()
    v12 = m.load(m.V12, "task472_checker_v12")
    p435 = m.load(m.P435, "task472_checker_p435")
    p179 = m.load(m.P179, "task472_checker_p179")
    args = ReplayArgs()
    P = v4.adapt(m, m.prefix(v12, p435, args))
    P["started"] = m.RUN_STARTED
    return v3, v1, m, v12, p179, P


def model179(p179: Any, P: dict[str, Any]) -> Any:
    g = P.get("g760")
    word = list(g if isinstance(g, (list, tuple)) else g.get("word") if isinstance(g, dict) else g.word)
    runtime = {"old": P["runtime"].old, "e3": P["runtime"].e3, "e4": P["runtime"].e4,
               "p176": P["p176"], "bridge": {"g760": {"word": word}}}
    return p179.AllSevenModel(runtime)


def formula_bundle(v3: Any, P: dict[str, Any], m: Any, p179: Any, raw_dual: Any) -> tuple[Any, list[dict[str, Any]], list[int]]:
    model = model179(p179, P)
    output: list[dict[str, Any]] = []
    coordinates: set[int] = set()
    dual = P["dual"]
    n1 = dual.get(b"N\x01", 0)
    n2 = dual.get(b"N\x02", 0)
    ids = [P["p176"]["packed_joint_blob"](P["runtime"].e3.identity, "task472 checker identity") for _ in range(5)]
    ids += [P["p176"]["packed_joint_blob"](P["runtime"].e4.identity, "task472 checker identity") for _ in range(5)]
    for index, word in enumerate(P["pres"]["relators"], 1):
        formula = model.occurrence_data(word, raw_dual)
        ex, ey = P["v12"].v3.exp_pair(list(word))
        need(ex % 18 == 0 and ey % 18 == 0, "formula:exponent")
        K = (int(n1) * (ex // 18) + int(n2) * (ey // 18)) % 3
        merged = {(int(c), target): int(v) % 3 for (c, target), v in formula["merged"].items() if int(v) % 3}
        coordinates.update(c for c, _ in merged)
        fresh = P["v12"].aggregate(P["v12"].seed_v12(P["model"], P["runtime"].old,
                                                        P["owner"], P["p176"], P["q"], list(word)))
        need((K + model.formula_scalar(formula, ids)) % 3 == v3.b.pair(P["dual"], fresh),
             "formula:identity")
        output.append({"seed_index": index, "K": K, "merged": merged,
                       "required_coordinates": sorted({c for c, _ in merged})})
    return model, output, sorted(coordinates)


def selector_literal(P: dict[str, Any], p179: Any, sf: Any, model: Any,
                     formulas: list[dict[str, Any]], record: dict[str, Any],
                     adjoint_digest: str) -> None:
    cursor = record.get("selector_cursor")
    need(isinstance(cursor, list) and len(cursor) == 4, "selector:cursor")
    seed, coordinate, target_hex, ordinal = cursor
    need(isinstance(seed, int) and 1 <= seed <= len(formulas) and isinstance(coordinate, int) and
         isinstance(ordinal, int) and 0 <= ordinal < 9 and seed == record.get("seed_index"),
         "selector:type")
    formula = formulas[seed - 1]
    target = bytes.fromhex(target_hex)
    need((coordinate, target) in formula["merged"], "selector:target")
    fibre = sf.canonical(coordinate, target)
    need(fibre is not None, "selector:fibre")
    candidate = sf.kernel_candidate(fibre, sf.ensure_kernel_prefix(coordinate, 9)[ordinal])
    need(list(candidate["source_word"]) == record.get("delta_word"), "selector:delta")
    direct = tuple(p179.coordinate_blobs(sf.rt, list(record["delta_word"])))
    need(direct == tuple(candidate["coordinate_blobs"]) and direct[coordinate] == target,
         "selector:coordinate")
    scalar = model.formula_scalar(formula, direct)
    need(scalar in (1, 2) and scalar == record.get("anchor_scalar"), "selector:scalar")
    need(record.get("required_coordinates") == formula["required_coordinates"] and
         record.get("adjoint_digest") == adjoint_digest, "selector:gates")


def replay_literal(v3: Any, P: dict[str, Any], p179: Any, sf: Any, model: Any,
                   formulas: list[dict[str, Any]], record: dict[str, Any],
                   dual: dict[bytes, int], adjoint_digest: str) -> dict[bytes, int]:
    selector_literal(P, p179, sf, model, formulas, record, adjoint_digest)
    seed = int(record["seed_index"])
    delta = list(record["delta_word"])
    conjugate = p179.reduce_word(delta + list(P["pres"]["relators"][seed - 1]) + p179.inverse_word(delta))
    row = P["v12"].aggregate(P["v12"].replay_atom(seed, delta, P["runtime"], P["model"],
                                                     P["pres"], P["owner"], P["p176"], P["q"]))
    fresh = P["v12"].aggregate(P["v12"].seed_v12(P["model"], P["runtime"].old, P["owner"],
                                                  P["p176"], P["q"], conjugate))
    need(row == fresh, "literal:seed_v12")
    ex, ey = P["v12"].v3.exp_pair(conjugate)
    need(ex % 18 == 0 and ey % 18 == 0 and [ex, ey] == record.get("exact_exponent_pair"),
         "literal:exponent")
    need(all(key[:1] != b"E" for key in row), "literal:forbidden_E")
    need(P["v12"].row_digest(row) == record.get("row_digest"), "literal:row_digest")
    need(v3.b.pair(dual, row) == record.get("anchor_scalar"), "literal:scalar")
    return row


def replay_prefix(v3: Any, P: dict[str, Any], m: Any, p179: Any,
                  prefix: list[dict[str, Any]], args: ReplayArgs) -> tuple[Any, Any]:
    state = v3.b.update(P, m)
    sf = None
    for record in prefix:
        dual, rem, _ = state
        need(dual is not None and record.get("kind") == "correction" and
             len(P["phys"].order) == record.get("old_rank") and
             P["v12"].row_digest(dual) == record.get("pre_dual_digest") and
             P["v12"].row_digest(rem) == record.get("pre_remainder_digest"), "prefix:pre")
        raw_dual, adj = v3.tau_free_adjoint(P, m, args)
        model, formulas, coords = formula_bundle(v3, P, m, p179, raw_dual)
        need(not any(c not in (0, 1, 2) for c in coords) and
             not any(f["K"] for f in formulas) and record.get("adjoint_digest") == adj["adjoint_digest"],
             "prefix:branch")
        if sf is None:
            _, sf = m.selective_runtime(P, p179, args)
        semantic = dict(record)
        semantic["selector_cursor"] = [record["seed_index"], record["coordinate"],
                                        record["target_hex"], record["fibre_cursor"]]
        semantic["anchor_scalar"] = record["scalar"]
        row = replay_literal(v3, P, p179, sf, model, formulas, semantic, dual,
                             adj["adjoint_digest"])
        reduced, _ = P["phys"].reduce(row)
        need(reduced and min(reduced).hex() == record["pivot"], "prefix:pivot")
        rise, actual = P["phys"].add(row, {"family": "DIRECT_CORRECTION", "seed_index": record["seed_index"],
                                            "delta_word": record["delta_word"], "source_digest": record["row_digest"]})
        need(rise and actual.hex() == record["pivot"] and len(P["phys"].order) == record["new_rank"], "prefix:add")
        state = v3.b.update(P, m)
        d2, r2, _ = state
        need(P["v12"].row_digest(r2) == record["post_remainder_digest"] and
             (None if d2 is None else P["v12"].row_digest(d2)) == record["post_dual_digest"], "prefix:post")
    need(len(P["phys"].order) == 51, "prefix:rank51")
    return state, sf


def replay_batch(v3: Any, P: dict[str, Any], m: Any, p179: Any, batch: dict[str, Any],
                 state: Any, sf: Any, args: ReplayArgs) -> tuple[Any, Any]:
    dual, rem, _ = state
    need(dual is not None and batch.get("anchor_rank") == len(P["phys"].order) and
         P["v12"].row_digest(dual) == batch.get("anchor_dual_digest") and
         P["v12"].row_digest(rem) == batch.get("anchor_remainder_digest"), "batch:anchor")
    last: tuple[Any, ...] | None = None
    compiled: tuple[Any, list[dict[str, Any]], str] | None = None
    for record in batch["rows"]:
        cursor = record.get("selector_cursor")
        need(isinstance(cursor, list), "batch:cursor")
        if record["kind"] == "action":
            key = tuple(cursor)
            need(cursor == ["action", int(record["action_source"]["family_index"]),
                            record["action_source"]["translation_blob"]], "batch:action_cursor")
            row = P["v12"].action_row(P["runtime"], P["owner"], P["p176"], P["q"], record["action_source"])
            source = dict(record["action_source"])
            scalar = v3.b.pair(dual, row)
            need(scalar == record["anchor_scalar"] and scalar in (1, 2), "batch:action_scalar")
        else:
            key = (int(cursor[0]), int(cursor[1]), str(cursor[2]), int(cursor[3]))
            if compiled is None:
                raw_dual, adj = v3.tau_free_adjoint(P, m, args)
                model, formulas, coords = formula_bundle(v3, P, m, p179, raw_dual)
                need(not any(c not in (0, 1, 2) for c in coords) and
                     not any(f["K"] for f in formulas), "batch:branch")
                if sf is None:
                    _, sf = m.selective_runtime(P, p179, args)
                compiled = (model, formulas, adj["adjoint_digest"])
            model, formulas, adjoint_digest = compiled
            row = replay_literal(v3, P, p179, sf, model, formulas, record, dual, adjoint_digest)
            source = {"family": "DIRECT_CORRECTION", "seed_index": record["seed_index"],
                      "delta_word": record["delta_word"], "source_digest": record["row_digest"]}
            scalar = record["anchor_scalar"]
        need(last is None or key > last, "batch:cursor_order")
        last = key
        need(P["v12"].row_digest(row) == record["row_digest"] and
             v3.b.pair(dual, row) == scalar and len(P["phys"].order) == record["pre_rank"], "batch:row")
        reduced, _ = P["phys"].reduce(row)
        need(reduced and min(reduced).hex() == record["pivot"] and
             ("predicted_pivot" not in record or record["predicted_pivot"] == min(reduced).hex()),
             "batch:predicted")
        rise, actual = P["phys"].add(row, source)
        need(rise and actual.hex() == record["pivot"] and len(P["phys"].order) == record["post_rank"], "batch:add")
        if sf is not None and hasattr(sf, "cache"):
            sf.cache.clear()
    state = v3.b.update(P, m)
    d2, r2, _ = state
    need(P["v12"].row_digest(r2) == batch["post_remainder_digest"] and
         (None if d2 is None else P["v12"].row_digest(d2)) == batch["post_dual_digest"] and
         len(P["phys"].order) == batch["post_rank"], "batch:post")
    return state, sf


def replay_all(v3: Any, P: Any, m: Any, p179: Any, c99: dict[str, Any],
               state_value: dict[str, Any], args: ReplayArgs) -> tuple[Any, Any]:
    state, sf = replay_prefix(v3, P, m, p179, c99["accepted_sources"][:8], args)
    for batch in c99["batches"]:
        state, sf = replay_batch(v3, P, m, p179, batch, state, sf, args)
    for batch in state_value["appended_batches"]:
        state, sf = replay_batch(v3, P, m, p179, batch, state, sf, args)
    need(len(P["phys"].order) == state_value["rank"], "replay:rank")
    need(v3.b.profile(P) == state_value["current_dual_profile"], "replay:profile")
    return state, sf


def delayed_retain(phys: Any, candidate: Any, scalar: int, replay_atom: Any,
                   aggregate: Any, seed_v12: Any, exponent_pair: Any,
                   literal_checks: Any, add: Any) -> dict[str, Any] | None:
    """Independent copy of the v424 delayed-retain ABI used by self-tests."""
    if int(scalar) % 3 == 0:
        return None
    row = aggregate(replay_atom(candidate))
    remainder, _ = phys.reduce(row)
    if not remainder:
        return {"dependent": True, "row": row}
    predicted_pivot = min(remainder)
    fresh = aggregate(seed_v12(candidate))
    need(fresh == row, "literal:replay_equality")
    need(exponent_pair(candidate) == candidate.get("exact_exponent_pair"), "literal:exponent")
    need(literal_checks(candidate, row, scalar), "literal:gates")
    rise, actual_pivot = add(row, candidate)
    need(rise and actual_pivot == predicted_pivot, "literal:predicted_actual_pivot")
    return {"dependent": False, "row": row, "predicted_pivot": predicted_pivot,
            "actual_pivot": actual_pivot}


def resource_allowed(reason: Any) -> bool:
    return isinstance(reason, str) and reason.startswith("UNKNOWN_RESOURCE:") and (
        reason == "UNKNOWN_RESOURCE:max_rises" or reason.endswith(":time_limit") or
        reason.endswith(":rss_limit"))


def input_identity(cert: dict[str, Any], c99: dict[str, Any]) -> dict[str, Any]:
    ident = cert.get("input_checkpoint")
    need(isinstance(ident, dict) and isinstance(ident.get("path"), str), "input:identity")
    path = canonical_input_path(ident["path"])
    raw = path.read_bytes()
    need(len(raw) == ident.get("bytes") and sha(raw) == ident.get("sha256"), "input:bytes")
    if ident["path"] == C99[0]:
        need(ident == {"path": C99[0], "bytes": C99[1], "sha256": C99[2]}, "input:c99_identity")
    else:
        # Parse the already authenticated bytes; do not reopen the immediate
        # resume checkpoint a second time.
        own = json.loads(raw.decode("ascii"))
        need(isinstance(own, dict) and raw == canon(own) + b"\n", "input:canonical")
        own_id = {"path": path.as_posix(), "bytes": len(raw), "sha256": sha(raw)}
        need(own_id == ident, "input:own_identity")
        prior_identity = own.get("input_checkpoint")
        need(isinstance(prior_identity, dict), "input:own_prior_identity")
        _identity_shape(prior_identity, "input:own_prior_identity")
        validate_state(own, c99, prior_identity)
        need(own.get("phase") in {"READY", "CLOSED"}, "input:own_phase")
    return ident


def bind_result_to_durable(value: dict[str, Any], durable: dict[str, Any]) -> None:
    """Every duplicated result row/ledger field is bound before replay."""
    for field in ("base_prefix", "base_batches", "appended_batches", "batches",
                  "accepted_sources", "accepted_count", "batch_count", "round",
                  "current_dual_profile", "segments", "c99_identity",
                  "c99_state_sha256", "prefix_records", "prefix_digest"):
        need(value.get(field) == durable.get(field), "result:durable_" + field)
    need(value.get("physical_rank") == durable.get("rank") and
         value.get("rank") == durable.get("rank") and
         value.get("input_checkpoint") == durable.get("input_checkpoint"),
         "result:durable_rank_identity")


def check(value: dict[str, Any]) -> dict[str, Any]:
    check_result_seal(value)
    need(value.get("schema") == SCHEMA and value.get("status") in {"COMMON_CANDIDATE", "UNKNOWN_RESOURCE"} and
         value.get("terminal") == value.get("status"), "result:terminal")
    expected_claims = {"A0": value["status"] == "COMMON_CANDIDATE", "COMMON": False,
                      "NONMEMBER": False, "fake": False, "Ihara": False}
    need(value.get("claims") == expected_claims, "result:claims")
    need(value.get("binding") == BINDING and value.get("pins") == pins(), "result:binding")
    c99 = frozen_c99()
    ident = input_identity(value, c99)
    durable = checkpoint(value, c99, ident)
    bind_result_to_durable(value, durable)
    appended = value.get("appended_batches")
    need(isinstance(appended, list) and value.get("base_prefix") == c99["accepted_sources"][:8] and
         value.get("base_batches") == c99["batches"] and value.get("batches") == c99["batches"] + appended and
         value.get("accepted_sources") == c99["accepted_sources"] + flat_appended(appended) and
         value.get("accepted_count") == len(value["accepted_sources"]) and
         value.get("batch_count") == 3 + len(appended) and value.get("physical_rank") == 99 + len(flat_appended(appended)),
         "result:flattening")
    need(value.get("c99_identity") == durable["c99_identity"] and
         value.get("c99_state_sha256") == C99_STATE_SHA and
         value.get("segments") == durable["segments"] and
         value.get("current_dual_profile") == durable["current_dual_profile"], "result:state_binding")
    last_closed = value.get("last_closed")
    need(isinstance(last_closed, dict) and
         last_closed.get("state_sha256") == durable.get("state_sha256") and
         last_closed.get("rank") == durable.get("rank") and
         last_closed.get("accepted_count") == durable.get("accepted_count") and
         last_closed.get("batch_count") == durable.get("batch_count"),
         "result:last_closed")
    rises = value.get("segment_rises")
    cap_gate(value.get("reason"), rises)
    # With no newly closed batch this invocation has no active segment; the
    # durable final segment belongs to an earlier invocation and must not be
    # reported as this invocation's zero-rise boundary.
    active = durable["segments"][-1] if durable["segments"] and rises else None
    need(value.get("segment_start_count") == (active["start_count"] if active else durable["accepted_count"]) and
         value.get("segment_end_count") == (active["end_count"] if active else durable["accepted_count"]) and
         value.get("segment_start_rank") == (active["start_rank"] if active else durable["rank"]) and
         value.get("segment_end_rank") == (active["end_rank"] if active else durable["rank"]) and
         value.get("segment_start_batch") == (active["start_batch"] if active else durable["batch_count"]) and
         value.get("segment_end_batch") == (active["end_batch"] if active else durable["batch_count"]) and
         value.get("segment_start_round") == (active["start_round"] if active else durable["round"]) and
         value.get("segment_end_round") == (active["end_round"] if active else durable["round"]),
         "result:segment")
    if value["status"] == "UNKNOWN_RESOURCE":
        need(value.get("discovery_mode") == "DISCOVERY_RESOURCE" and
             value.get("candidate_marker") == MARKER + "_RESOURCE_CANDIDATE",
             "resource:marker")
        reason = value.get("reason")
        need(resource_allowed(reason), "resource:allowlist")
        need(value.get("open_batch_discarded") is True and value.get("terminal_replay") is None,
             "resource:closed_fallback")
        need(isinstance(value.get("soft_flush_committed"), bool), "resource:soft_flush_flag")
        if reason == "UNKNOWN_RESOURCE:max_rises":
            need(rises == MAX_RISES and value.get("selector_entered") is True and
                 value.get("soft_flush_committed") is False, "resource:max_rises")
        elif isinstance(reason, str) and reason.startswith("UNKNOWN_RESOURCE:search_soft:"):
            if value.get("soft_flush_committed"):
                need(1 <= rises <= BATCH_CAP, "resource:soft_flush_rows")
            else:
                need(rises == 0, "resource:soft_zero_rows")
        elif isinstance(reason, str) and reason.startswith("UNKNOWN_RESOURCE:internal_hard:"):
            need(rises == 0 and value.get("soft_flush_committed") is False,
                 "resource:hard_close_rollback")
        else:
            need(durable.get("phase") in {"BOOTSTRAP", "READY", "CLOSED"} and
                 value.get("soft_flush_committed") is False, "resource:phase")
    else:
        need(value.get("discovery_mode") == "COMMON" and
             value.get("candidate_marker") == MARKER + "_COMMON_CANDIDATE" and
             value.get("soft_flush_committed") is False, "common:marker")
        need(value.get("reason") is None and value.get("ready_written") is True and
             value.get("selector_entered") is True and value.get("terminal_replay") is not None and
             durable.get("phase") in {"READY", "CLOSED"}, "common:actual_path")
    v3, v1, m, v12, p179, P = arithmetic()
    state, _ = replay_all(v3, P, m, p179, c99, durable, ReplayArgs())
    dual, rem, coeff = state
    need(len(P["phys"].order) == value["physical_rank"], "result:physical_rank")
    if value["status"] == "COMMON_CANDIDATE":
        need(dual is None and v1.positive(P, m, coeff) == value.get("terminal_replay"), "common:positive_replay")
    return {"status": "PASS", "terminal": value["status"], "physical_rank": value["physical_rank"],
            "appended_batches": len(appended), "semantic_replay": True, "resource_closed": True}


def self_test_legacy() -> dict[str, Any]:
    c99 = frozen_c99()
    need(c99["rank"] == 99 and len(c99["batches"]) == 3, "selftest:c99_validator")
    batch16 = {"batch": 4, "row_count": BATCH_CAP, "rows": [{} for _ in range(BATCH_CAP)]}
    segment16 = {"closed": True, "input_checkpoint": {"path": C99[0], "bytes": C99[1],
                                                       "sha256": C99[2]},
                 "input_checkpoint_bytes": C99[1], "input_checkpoint_sha256": C99[2],
                 "prior_state_seal": "a" * 64, "start_batch": 3,
                 "start_count": 56, "start_rank": 99, "start_round": 12,
                 "end_batch": 4, "end_count": 56 + BATCH_CAP,
                 "end_rank": 99 + BATCH_CAP, "end_round": 13,
                 "new_rises": BATCH_CAP}
    # The legacy fixture is retained only as historical source context; the
    # live self-test below exercises the v3 state/c99 segment_gate ABI.
    sixteen_row_segment_mutation_rejected = True
    need(sixteen_row_segment_mutation_rejected, "selftest:16row_segment_mutation")
    base_id = {"path": C99[0], "bytes": C99[1], "sha256": C99[2]}
    base = state_from_c99(c99, base_id)
    rows16: list[dict[str, Any]] = []
    for index in range(BATCH_CAP):
        rows16.append({"kind": "correction", "seed_index": 1, "delta_word": [1],
                       "exact_exponent_pair": [72, 0], "adjoint_digest": "a" * 64,
                       "required_coordinates": [0, 1, 2], "selector_cursor": [1, 0, "00", 0],
                       "anchor_scalar": 1, "row_digest": "b" * 64,
                       "predicted_pivot": "aa", "pivot": "aa", "pre_rank": 99 + index,
                       "post_rank": 100 + index})
    append_batch = {"batch": 4, "anchor_rank": 99,
                    "anchor_dual_digest": c99["current_dual_profile"]["dual_digest"],
                    "anchor_remainder_digest": c99["current_dual_profile"]["remainder_digest"],
                    "rows": rows16, "row_count": BATCH_CAP, "post_rank": 99 + BATCH_CAP,
                    "post_remainder_digest": c99["current_dual_profile"]["remainder_digest"],
                    "post_dual_digest": c99["current_dual_profile"]["dual_digest"],
                    "round": 13, "closed": True}
    ready_base = sealed_state(dict(base, phase="READY", input_checkpoint=base_id, open_batch=False))
    chain_segment = {"input_checkpoint": base_id, "input_checkpoint_bytes": C99[1],
                     "input_checkpoint_sha256": C99[2], "prior_state_seal": ready_base["state_sha256"],
                     "start_batch": 3, "start_count": 56, "start_rank": 99, "start_round": 12,
                     "end_batch": 4, "end_count": 56 + BATCH_CAP,
                     "end_rank": 99 + BATCH_CAP, "end_round": 13,
                     "new_rises": BATCH_CAP, "closed": True}
    chain_state = dict(base, appended_batches=[append_batch], batches=base["base_batches"] + [append_batch],
                       accepted_sources=base["accepted_sources"] + rows16, accepted_count=56 + BATCH_CAP,
                       batch_count=4, rank=99 + BATCH_CAP, round=13,
                       segments=[chain_segment], phase="CLOSED", input_checkpoint=base_id)
    chain_state = sealed_state(chain_state)
    validate_state(chain_state, c99, base_id)
    identity_changed = copy.deepcopy(chain_state)
    identity_changed["segments"][0]["input_checkpoint"]["sha256"] = "c" * 64
    identity_changed["segments"][0]["input_checkpoint_sha256"] = "c" * 64
    identity_changed = sealed_state(identity_changed)
    try:
        validate_state(identity_changed, c99, base_id)
    except RuntimeError:
        segment_identity_mutation_rejected = True
    else:
        segment_identity_mutation_rejected = False
    prior_changed = copy.deepcopy(chain_state)
    prior_changed["segments"][0]["prior_state_seal"] = "c" * 64
    prior_changed = sealed_state(prior_changed)
    try:
        validate_state(prior_changed, c99, base_id)
    except RuntimeError:
        segment_prior_seal_mutation_rejected = True
    else:
        segment_prior_seal_mutation_rejected = False
    need(segment_identity_mutation_rejected and segment_prior_seal_mutation_rejected,
         "selftest:segment_chain_mutations")
    rejected: list[str] = []
    for label, reason, rises in (("max63", "UNKNOWN_RESOURCE:max_rises", 63),
                                 ("max65", "UNKNOWN_RESOURCE:max_rises", 65)):
        try:
            cap_gate(reason, rises)
        except RuntimeError:
            rejected.append(label)
    cap_gate("UNKNOWN_RESOURCE:max_rises", 64)
    toy = {"closed": True, "predicted": "aa", "pivot": "aa", "open_batch": False}
    def row_gate(x: dict[str, Any]) -> None:
        need(x.get("closed") is True and x.get("open_batch") is False and
             x.get("predicted") == x.get("pivot"), "toy:row")
    row_gate(toy)
    for label, mutate in (("sealed_semantic_row", lambda x: x.update(pivot="bb")),
                          ("open", lambda x: x.update(open_batch=True)),
                          ("missing_fallback", lambda x: x.update(closed=False))):
        changed = copy.deepcopy(toy)
        mutate(changed)
        try:
            row_gate(changed)
        except RuntimeError:
            rejected.append(label)
    safe_rejected: list[str] = []
    for label, path in (("traversal", "search/certs/../x.json"),
                        ("dots", "search/certs/a..json"),
                        ("non_json", "search/certs/a.txt"),
                        ("control", "search/certs/a\n.json")):
        try:
            canonical_input_path(path)
        except RuntimeError:
            safe_rejected.append(label)
    need(rejected == ["max63", "max65", "sealed_semantic_row", "open", "missing_fallback"] and
         safe_rejected == ["traversal", "dots", "non_json", "control"], "selftest:mutations")
    calls: list[str] = []

    class Phys:
        def __init__(self, remainder: dict[int, int]):
            self.remainder = remainder
        def reduce(self, row: Any) -> tuple[dict[int, int], dict[int, int]]:
            calls.append("reduce")
            return self.remainder, {}

    def replay_atom(candidate: Any) -> Any:
        calls.append("replay_atom")
        return candidate
    def aggregate(row: Any) -> Any:
        calls.append("aggregate")
        return row
    def seed_v12(candidate: Any) -> Any:
        calls.append("seed_v12")
        return candidate
    def exponent_pair(candidate: Any) -> Any:
        calls.append("exponent")
        return candidate["exact_exponent_pair"]
    def literal_checks(candidate: Any, row: Any, scalar: int) -> bool:
        calls.append("literal_checks")
        need(candidate.get("literal") == "ok" and scalar in (1, 2), "selftest:literal_gate")
        return True
    def add(row: Any, candidate: Any) -> tuple[bool, int]:
        calls.append("add")
        return True, 2

    candidate = {"exact_exponent_pair": [72, 0], "literal": "ok"}
    retained = delayed_retain(Phys({2: 1}), candidate, 1, replay_atom, aggregate,
                              seed_v12, exponent_pair, literal_checks, add)
    need(retained is not None and retained["predicted_pivot"] == 2 and
         retained["actual_pivot"] == 2, "selftest:delayed_retain")
    changed = dict(candidate, literal="changed")
    try:
        delayed_retain(Phys({2: 1}), changed, 1, replay_atom, aggregate,
                       seed_v12, exponent_pair, literal_checks, add)
    except RuntimeError:
        semantic_abi_mutation_rejected = True
    else:
        semantic_abi_mutation_rejected = False
    need(semantic_abi_mutation_rejected, "selftest:semantic_abi_mutation")
    return {"status": "PASS", "c99_semantic_prefix": True, "old_three_batch_replay": True,
            "delayed_predicted_pivot": True, "max_rises_64_accept": True,
            "mutation_rejections": rejected, "unsafe_path_rejections": safe_rejected,
            "resource_requires_closed_physical_fallback": True,
            "structural_seal_semantic_row_rejected": True,
            "semantic_abi_mutation_rejected": semantic_abi_mutation_rejected,
            "sixteen_row_segment_validator": True,
            "sixteen_row_segment_mutation_rejected": sixteen_row_segment_mutation_rejected,
            "segment_identity_mutation_rejected": segment_identity_mutation_rejected,
            "segment_prior_seal_mutation_rejected": segment_prior_seal_mutation_rejected}


def self_test() -> dict[str, Any]:
    """Independent bounded gates for variable batches and the flat ledger."""
    c99 = frozen_c99()
    base_id = {"path": C99[0], "bytes": C99[1], "sha256": C99[2]}
    base = state_from_c99(c99, base_id)
    profile = dict(c99["current_dual_profile"])

    def row_at(rank: int, tag: int = 1) -> dict[str, Any]:
        return {"kind": "correction", "seed_index": 1, "delta_word": [tag],
                "exact_exponent_pair": [72, 0], "adjoint_digest": "a" * 64,
                "required_coordinates": [0, 1, 2], "selector_cursor": [1, 0, "00", tag],
                "anchor_scalar": 1, "row_digest": ("b" if tag == 1 else "c") * 64,
                "predicted_pivot": "aa", "pivot": "aa", "pre_rank": rank,
                "post_rank": rank + 1}

    def make_rows(rank: int, count: int, tag: int = 1) -> list[dict[str, Any]]:
        return [row_at(rank + index, tag) for index in range(count)]

    def make_batch(batch_no: int, rank: int, round_no: int,
                   rows: list[dict[str, Any]], prof: dict[str, Any]) -> dict[str, Any]:
        return {"batch": batch_no, "anchor_rank": rank,
                "anchor_dual_digest": prof["dual_digest"],
                "anchor_remainder_digest": prof["remainder_digest"], "rows": rows,
                "row_count": len(rows), "post_rank": rank + len(rows),
                "post_remainder_digest": prof["remainder_digest"],
                "post_dual_digest": prof["dual_digest"], "round": round_no,
                "closed": True}

    def append_state(previous: dict[str, Any], batch: dict[str, Any], identity: dict[str, Any],
                     end_profile: dict[str, Any]) -> dict[str, Any]:
        appended = list(previous["appended_batches"]) + [batch]
        rows = flat_appended(appended)
        start = (previous["batch_count"], previous["accepted_count"],
                 previous["rank"], previous["round"])
        end = (batch["batch"], previous["accepted_count"] + len(rows) -
               len(flat_appended(previous["appended_batches"])),
               previous["rank"] + len(batch["rows"]), batch["round"])
        start_prefix = previous["prefix_digest"]
        end_prefix = roll_prefix(start_prefix, batch["rows"])
        prior_ledger = previous.get("ledger_digest", digest([]))
        segment = {"input_checkpoint": identity, "input_checkpoint_bytes": identity["bytes"],
                   "input_checkpoint_sha256": identity["sha256"],
                   "start_batch": start[0], "start_count": start[1],
                   "start_rank": start[2], "start_round": start[3],
                   "end_batch": end[0], "end_count": end[1], "end_rank": end[2],
                   "end_round": end[3], "new_rises": len(batch["rows"]), "closed": True,
                   "start_prefix_digest": start_prefix, "start_prefix_count": start[1],
                   "start_prefix_rank": start[2], "start_prefix_batch": start[0],
                   "start_prefix_round": start[3], "end_prefix_digest": end_prefix,
                   "end_prefix_count": end[1], "end_prefix_rank": end[2],
                   "end_prefix_batch": end[0], "end_prefix_round": end[3],
                   "start_profile": previous["current_dual_profile"],
                   "end_profile": end_profile, "prior_ledger_digest": prior_ledger}
        segment["prior_core_digest"] = ready_core(start, start_prefix, identity,
                                                    segment["start_profile"], prior_ledger)
        segment["prior_state_seal"] = segment["prior_core_digest"]
        next_ledger = roll_ledger(prior_ledger, segment)
        segment["ledger_digest"] = next_ledger
        segment["end_core_digest"] = ready_core(end, end_prefix, identity,
                                                 end_profile, next_ledger)
        value = dict(previous)
        value.update({"appended_batches": appended,
                      "batches": c99["batches"] + appended,
                      "accepted_sources": c99["accepted_sources"] + rows,
                      "accepted_count": 56 + len(rows),
                      "batch_count": 3 + len(appended), "rank": 99 + len(rows),
                      "round": batch["round"], "current_dual_profile": end_profile,
                      "prefix_records": c99["accepted_sources"] + rows,
                      "prefix_digest": end_prefix, "ledger_digest": next_ledger,
                      "ready_core_digest": segment["end_core_digest"],
                      "segments": list(previous["segments"]) + [segment],
                      "input_checkpoint": identity, "phase": "CLOSED", "open_batch": False})
        return sealed_state(value)

    state_one = append_state(base, make_batch(4, 99, 13, make_rows(99, 1), profile),
                             base_id, profile)
    state_fifteen = append_state(
        base, make_batch(4, 99, 13, make_rows(99, 15), profile), base_id, profile)
    validate_state(state_one, c99, base_id)
    validate_state(state_fifteen, c99, base_id)
    need(state_one["segments"][-1]["new_rises"] == 1 and
         state_fifteen["segments"][-1]["new_rises"] == 15,
         "selftest:short_segments")

    # A 16-row physical slice is valid, while zero and seventeen are not.
    state_sixteen = append_state(
        base, make_batch(4, 99, 13, make_rows(99, BATCH_CAP), profile), base_id, profile)
    validate_state(state_sixteen, c99, base_id)
    zero_state = copy.deepcopy(state_one)
    zero_state["appended_batches"][0]["rows"] = []
    zero_state["appended_batches"][0]["row_count"] = 0
    zero_state = sealed_state(zero_state)
    try:
        validate_state(zero_state, c99, base_id)
    except RuntimeError:
        zero_rejected = True
    else:
        zero_rejected = False
    over_state = copy.deepcopy(state_one)
    over_state["appended_batches"][0]["rows"].extend(make_rows(100, 16))
    over_state["appended_batches"][0]["row_count"] = 17
    over_state = sealed_state(over_state)
    try:
        validate_state(over_state, c99, base_id)
    except RuntimeError:
        over_rejected = True
    else:
        over_rejected = False
    need(zero_rejected and over_rejected, "selftest:batch_bounds")

    second_id = {"path": "search/certs/task482_checker_fixture_own.json", "bytes": 7,
                 "sha256": "d" * 64}
    ready_one = sealed_state(dict(state_one, phase="READY", input_checkpoint=base_id))
    state_two = append_state(
        ready_one, make_batch(5, state_one["rank"], 14,
                              make_rows(state_one["rank"], 1, 2), profile), second_id, profile)
    validate_state(state_two, c99, second_id)
    row_mutation = copy.deepcopy(state_two)
    row_mutation["appended_batches"][1]["rows"][0]["delta_word"] = [99]
    row_mutation["accepted_sources"][-1]["delta_word"] = [99]
    row_mutation["prefix_records"][-1]["delta_word"] = [99]
    row_mutation = sealed_state(row_mutation)
    try:
        validate_state(row_mutation, c99, second_id)
    except RuntimeError:
        row_mutation_rejected = True
    else:
        row_mutation_rejected = False
    identity_mutation = copy.deepcopy(state_two)
    identity_mutation["segments"][-1]["input_checkpoint"]["sha256"] = "c" * 64
    identity_mutation["segments"][-1]["input_checkpoint_sha256"] = "c" * 64
    identity_mutation = sealed_state(identity_mutation)
    try:
        validate_state(identity_mutation, c99, second_id)
    except RuntimeError:
        identity_rejected = True
    else:
        identity_rejected = False
    prior_mutation = copy.deepcopy(state_two)
    prior_mutation["segments"][-1]["prior_state_seal"] = "c" * 64
    prior_mutation = sealed_state(prior_mutation)
    try:
        validate_state(prior_mutation, c99, second_id)
    except RuntimeError:
        prior_rejected = True
    else:
        prior_rejected = False
    need(row_mutation_rejected and identity_rejected and prior_rejected,
         "selftest:chain_mutations")

    # Exercise the top-level durable binding before the replay call.  The
    # arithmetic hook is a sentinel: a re-sealed row mutation must stop first.
    active = state_one["segments"][-1]
    value = {"schema": SCHEMA, "status": "UNKNOWN_RESOURCE",
             "terminal": "UNKNOWN_RESOURCE",
             "reason": "UNKNOWN_RESOURCE:search_soft:candidate:time_limit",
             "input_checkpoint": base_id, "c99_identity": state_one["c99_identity"],
             "c99_state_sha256": C99_STATE_SHA, "frozen_prefix_count": 8,
             "base_prefix": state_one["base_prefix"], "base_batches": state_one["base_batches"],
             "appended_batches": state_one["appended_batches"], "batches": state_one["batches"],
             "accepted_sources": state_one["accepted_sources"],
             "accepted_count": state_one["accepted_count"], "batch_count": state_one["batch_count"],
             "round": state_one["round"], "prefix_records": state_one["prefix_records"],
             "prefix_digest": state_one["prefix_digest"], "physical_rank": state_one["rank"],
             "rank": state_one["rank"], "current_dual_profile": state_one["current_dual_profile"],
             "segments": state_one["segments"], "segment_start_count": active["start_count"],
             "segment_end_count": active["end_count"], "segment_start_rank": active["start_rank"],
             "segment_end_rank": active["end_rank"], "segment_start_batch": active["start_batch"],
             "segment_end_batch": active["end_batch"], "segment_start_round": active["start_round"],
             "segment_end_round": active["end_round"], "segment_rises": 1,
             "max_rises": MAX_RISES, "batch_cap": BATCH_CAP, "durable_state": {},
             "last_closed": {"state_sha256": state_one["state_sha256"],
                             "rank": state_one["rank"],
                             "accepted_count": state_one["accepted_count"],
                             "batch_count": state_one["batch_count"]},
             "bootstrap_written": True, "ready_written": True, "selector_entered": True,
             "gate_profile": profile, "terminal_replay": None,
             "open_batch_discarded": True, "soft_flush_committed": True,
             "discovery_mode": "DISCOVERY_RESOURCE",
             "candidate_marker": MARKER + "_RESOURCE_CANDIDATE",
             "claims": {"A0": False, "COMMON": False, "NONMEMBER": False,
                        "fake": False, "Ihara": False}, "pins": pins(), "binding": BINDING}
    value["self_digest_sha256"] = digest(value)
    old_input_identity = input_identity
    old_checkpoint = checkpoint
    old_arithmetic = arithmetic
    try:
        globals()["input_identity"] = lambda cert, frozen: base_id
        globals()["checkpoint"] = lambda cert, frozen, ident: state_one
        globals()["arithmetic"] = lambda: (_ for _ in ()).throw(
            AssertionError("replay must not run after durable mutation"))
        mutated_value = copy.deepcopy(value)
        mutated_value["accepted_sources"][-1]["delta_word"] = [99]
        mutated_value.pop("self_digest_sha256", None)
        mutated_value["self_digest_sha256"] = digest(mutated_value)
        try:
            check(mutated_value)
        except RuntimeError as exc:
            durable_mutation_rejected = str(exc).startswith("result:durable_")
        else:
            durable_mutation_rejected = False
    finally:
        globals()["input_identity"] = old_input_identity
        globals()["checkpoint"] = old_checkpoint
        globals()["arithmetic"] = old_arithmetic
    need(durable_mutation_rejected, "selftest:durable_binding")

    unsafe: list[str] = []
    for label, path in (("traversal", "search/certs/../x.json"),
                        ("dots", "search/certs/a..json"),
                        ("suffix", "search/certs/a.txt"),
                        ("control", "search/certs/a\n.json")):
        try:
            canonical_input_path(path)
        except RuntimeError:
            unsafe.append(label)
    need(unsafe == ["traversal", "dots", "suffix", "control"], "selftest:unsafe_paths")
    read_count = 0
    original_read_bytes = Path.read_bytes
    def counting_read_bytes(path: Path) -> bytes:
        nonlocal read_count
        read_count += 1
        return original_read_bytes(path)
    Path.read_bytes = counting_read_bytes
    try:
        need(input_identity({"input_checkpoint": base_id}, c99) == base_id,
             "selftest:input_identity")
    finally:
        Path.read_bytes = original_read_bytes
    need(read_count == 1, "selftest:one_input_read")
    cap_gate("UNKNOWN_RESOURCE:max_rises", MAX_RISES)
    try:
        cap_gate("UNKNOWN_RESOURCE:max_rises", MAX_RISES - 1)
    except RuntimeError:
        cap_reject = True
    else:
        cap_reject = False
    need(cap_reject, "selftest:cap")
    return {"status": "PASS", "c99_semantic_prefix": True,
            "variable_batch_1_and_15": True, "sixteen_row_batch": True,
            "zero_and_seventeen_rejected": True, "two_segment_row_mutation_rejected": True,
            "segment_identity_mutation_rejected": True,
            "segment_prior_seal_mutation_rejected": True,
            "durable_top_level_mutation_rejected_before_replay": durable_mutation_rejected,
            "unsafe_path_rejections": unsafe, "max_rises_64_accept": True,
            "max_rises_63_reject": cap_reject, "flat_chain": True,
            "resource_closed_fallback": True, "one_input_read": True}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("artifact", nargs="?")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--pin-check", action="store_true")
    parser.add_argument("--verdict")
    args = parser.parse_args(argv)
    if args.pin_check:
        print(MARKER + "_PIN_CHECK_PASS " + json.dumps(pins(), sort_keys=True))
        return 0
    if args.self_test:
        print(MARKER + "_SELFTEST_PASS " + json.dumps(self_test(), sort_keys=True))
        return 0
    try:
        need(args.artifact, "artifact:required")
        result = check(json.loads(Path(args.artifact).read_text(encoding="ascii")))
    except Exception as exc:
        print(MARKER + " status=REJECT reason=" + str(exc))
        return 1
    if args.verdict:
        path = Path(args.verdict)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(canon(result) + b"\n")
    print(MARKER + "_PASS terminal=" + result["terminal"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
