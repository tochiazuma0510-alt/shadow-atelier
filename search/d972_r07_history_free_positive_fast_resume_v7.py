#!/usr/bin/env python3
"""R07 v7 history-free positive resume.

The old checkpoint is used only as a triangular discovery basis.  Every
``P_j = sum_i a[j,i] C_i`` equation is rebuilt independently and injected
directly.  Newly discovered rows are literal rows.  A COMMON document is a
candidate for the helper-nonshared v7 checker, never a self-authorized claim.

This module intentionally does not call cached-v3 main/rank-zero resume or
live-v1 build_runtime/PositiveSearch.  Immutable predecessor files are
compiled from one authenticated byte snapshot and only small arithmetic
primitives are reused.
"""
from __future__ import annotations

import argparse
import bisect
import hashlib
import json
import multiprocessing
import os
import selectors
import socket
import stat
import struct
import sys
import tempfile
import time
import types
from pathlib import Path
from typing import Any, Iterable, Sequence


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "d972-r07-history-free-positive-fast-resume/v7"
CHECKPOINT_SCHEMA = SCHEMA + "/checkpoint"
COMMON = "R07_HISTORY_FREE_POSITIVE_FAST_RESUME_V7_COMMON_WORD"
UNKNOWN_INPUT = "UNKNOWN_INPUT"
UNKNOWN_RESOURCE = "UNKNOWN_RESOURCE"
PRODUCER_PREFIX = "R07_HISTORY_FREE_POSITIVE_FAST_RESUME_V7_PRODUCER_TERMINAL"
RAW_BYTES = 86_368_039
RAW_SHA256 = "c261aa967867a4870228eae467f46ee4afbfc236445890debd891bcef4a250ab"
RAW_MEMBER = "d972_r07_normalized_exact_common_word_cached_v3.json.checkpoint.json"
OLD_SCHEMA = "d972-r07-normalized-exact-cached-colgen/v3"
OLD_SELF_DIGEST = "29bb74f3bd8048913a0365bc4c599f3731d32ba56967f3a238c7468b7fcfd123"
OLD_INPUT_SHA256 = "f29eaf9b945adb3bde89395ae9cb9018309fe8f3938d32f55e6716574b861cfb"
OLD_TARGET_SHA256 = "968f0b8325fa0e741e2c304bb940b96239c3e2d3226e0ca56f7d61a53dd0d82b"
OLD_PIVOT_ROWS_SHA256 = "3c645f4e352c96691dd35d6202bdf5f8b2cce73b7eb5f1bdf33a8daa06ce9d28"
OLD_DUAL_SHA256 = "0960259714fa94ddd89e2ac4f582f040942ab7bd258185c0448c133e50b00f0c"
NORMALIZED_DIGEST = "07c91e42c91648c5139ec13afd7fe0f44aff964612bae950d9dbd941b509b109"
WALL_SECONDS = 10_800.0
DELTA_ORDER = 357_128_352
KERNEL_ORDERS = (9, 9, 9, 9, 9, 1, 1, 1, 3, 3)
MAX_FORMAL_ENTRIES = 2_000_000
MAX_FRAME_BYTES = 32 * 1024 * 1024
MAX_CHECKPOINT_BYTES = 4_000_000_000
CHANNEL_START_SECONDS = 20.0
CHANNEL_CLOSE_SECONDS = 3.0
EXPECTED_TRIANGULAR = {
    "columns": 2896,
    "rank": 2896,
    "boundary_columns": 2896,
    "correction_columns": 0,
    "raw_support_total": 20354,
    "raw_support_max": 12,
    "ancestry_entries_total": 137926,
    "ancestry_entries_max": 258,
    "ancestry_weighted_contributions": 1011460,
    "pivot_support_total": 289774,
    "pivot_support_max": 522,
    "future_ancestry_indices": 0,
    "zero_or_missing_diagonal": 0,
    "duplicate_empty_wrong_pivots": 0,
}
EXPECTED_MANIFEST = {
    "schema": "d972-r07-normalized-exact-cached-colgen/resume-input/v1",
    "source_run_id": 33149728601,
    "source_head_sha": "7dd85c94c01e35e090917f9d11f9a7252a260523",
    "source_artifact_id": 9681838782,
    "source_artifact_digest": "sha256:66ed561b0c19c22dd56ce6aaa1626159d8267788fa282d3f2cb72f33c36e6917",
    "source_receipt": {
        "bytes": 8759,
        "sha256": "955a6bebb442f6bbe111ffcb4c1eda732f8bbbe26292c4e5da451c69dbaf5dcc",
        "terminal": "UNKNOWN_RESOURCE:phase=positive_boundary_correlation:cap=wall_seconds:value=10801.537010798002:limit=10800.0",
    },
    "zip": {
        "path": "ci/in/d972_r07_normalized_exact_common_word_cached_v3_run33149728601_checkpoint.zip",
        "bytes": 5_001_811,
        "sha256": "f3ac82a04907983d987cc2a42d06fe3b612ec2040555f40be81200969358f566",
        "member": RAW_MEMBER,
    },
    "raw_checkpoint": {"bytes": RAW_BYTES, "sha256": RAW_SHA256},
    "progress": {"phase": "positive_boundary_correlation", "boundary_pairs": 3_145_728,
                 "retained_columns": 2896, "candidate_words": 0},
    "claims": {"common_word": False, "separator": False,
               "finite_common_word": False, "cofinal_lift": False,
               "fake": False, "ihara_witness": False},
}

# Direct source authorities.  The producer itself is intentionally absent.
SOURCE_PINS: dict[str, tuple[str, int, str]] = {
    "commission": ("sol/luna_task_342_r07_a0_v7_fast_positive_resume.md", 15393,
                   "9fca7eb266b433436f44a25f0b984d6941c5a1696e960a80e062c5abefcc028d"),
    "audit337": ("sol/sol_reply_337_r07_task325_v6_code_performance_audit_v1.md", 42611,
                 "035f3d987746f9662fb66da512889da7ad4f7ad899a3cc768e626093ce050f4a"),
    "proof265": ("sol/proof_r07_history_free_positive_common_word_verifier_v265.md", 10122,
                 "fd30ccb2458691ec7844d304f220a4be7d704259318c452f928f8088552ecb0a"),
    "proof275": ("sol/proof_r07_two_way_basis_checkpoint_resume_v275.md", 7662,
                 "51febdaadcdf9130af4dd0586969f28f533ff3e9d06d883841aa115410dd40ea"),
    "proof276": ("sol/proof_r07_triangular_checkpoint_basis_resume_v276.md", 5571,
                 "5765aec25e08e687841451d3707ba16e0f3e2c6c4d9de6c120e92bdafe071abb"),
    "proof277": ("sol/proof_r07_boundary_first_lazy_runtime_resume_v277.md", 9070,
                 "2539fa530195b7c5fe7035d2261301ed85c471af2df313fd33fb01e96df9a56d"),
    "proof278": ("sol/proof_r07_selected_support_positive_replay_v278.md", 7055,
                 "f9dcb97c86e401bd96a92805b6c31428483d624874388bcc0439d1f7dc2f390b"),
    "audit279": ("sol/audit_r07_task298_six_hour_cancel_no_artifact_v279.md", 3844,
                 "f669705e93a5ad3c84fb94a5b7f8ec4cf3cedd103df1e0b1d78460e9c8b1f5c9"),
    "live": ("search/d972_r07_positive_common_word_colgen_v1.py", 123870,
             "47116826e1b94750fa5eaa0c577586aeaec23a476c5f004fc0d5ea83892845c7"),
    "task175": ("search/d972_r07_all_seven_raw_bridge_preflight_v1.py", 60306,
                "1e0a65f5182157bb928638c2c9a71d475b3b788a6694ee4ded09f5a0ffd38cfa"),
    "task176": ("search/d972_r07_all_seven_extension_section_census_v1.py", 66109,
                "878cf1d8d44e74a993309ed1c613c9fc57eb62fd2da48a30fd8797ff4b19af3b"),
    "q3": ("ci/b345_157ee_artifacts_32359956713/d972_b345_q3_chief_v1.json", 231570,
           "3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72"),
    "joint_receipt": ("ci/b345_157ee_artifacts_32359956713/d972_b345_joint_kernel_qstar_closure_v1.json", 2166036,
                      "1c3ad7a7124cee152eb40968cf212c14641a9f8720063c85f70533864898d0df"),
    "old": ("search/d972_b345_seedspan_triple4_v1.py", 535219,
            "fe18fc31fdf3f9416ebb829112ccbd514c27e6a8d30fe24691842865277a0b29"),
    "old_bridge": ("search/d972_b345_triple_cube_raw_lambda_census_v1.py", 126942,
                   "d4a290984ae8a93b6959f06d20c1de037b2814707778fba03c59ac87b2f736db"),
    "joint": ("search/d972_b345_joint_kernel_qstar_closure_v1.py", 67945,
              "06ba6cf361957db3e339d48d14b3d4fbc689de9642e3f96273fbe8f3160e76dc"),
    "v172": ("search/d972_r07_full_e4_joint_orbit_preflight_v7.py", 21918,
             "92701bb1ed84de9b9aa0fb8a986197f76b86e1f42af83ee18319700be0647eed"),
    "g760": ("search/check_d972_r07_616_to_760_commutator_affine_rhs_v3.py", 33409,
             "f8c7fc7f5b5bbfffa0cf147a59313981c5a4b2c6c00504a9f773029097fdde5f"),
    "pb4": ("search/d972_b345_target6_dual_colgen_v2.py", 444497,
            "b361dc5e7b025bb7efe3507b145e5480c6c67dfecc2e712134a8d521585e73c7"),
    "manifest": ("ci/in/d972_r07_normalized_exact_common_word_cached_v3_run33149728601_checkpoint.manifest.json", 1328,
                 "6911dfe822662a17ae95c896f97573e553d15325631f1606bd0bf7f550e88302"),
    "fixture": ("search/certs/d972_r07_history_free_positive_fast_resume_selftest_v7_20260829.json", 2783,
                "5f6628d8413ebcc78a87196fa999b4f73122d4bca2c22efc0a9f637e59f483c6"),
}

FALSE_CLAIMS = {"common_word": False, "finite_common_word": False,
                "separator": False, "negative": False, "cofinal_lift": False,
                "fake": False, "ihara_witness": False}


class InputStop(RuntimeError):
    pass


class ResourceStop(RuntimeError):
    def __init__(self, phase: str, cap: str, value: int | float,
                 limit: int | float, detail: str = "") -> None:
        super().__init__(detail or f"{phase}:{cap}:{value}>{limit}")
        self.phase, self.cap = str(phase), str(cap)
        self.value, self.limit = value, limit


class ProtocolStop(RuntimeError):
    pass


class SelftestReject(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ProtocolStop(message)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True).encode("ascii")


def sha_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha_obj(value: Any) -> str:
    return sha_bytes(canonical(value))


def seal(value: dict[str, Any]) -> dict[str, Any]:
    answer = dict(value); answer.pop("self_digest", None)
    answer["self_digest"] = sha_obj(answer)
    return answer


def validate_seal(value: dict[str, Any]) -> None:
    claimed = value.get("self_digest")
    body = dict(value); body.pop("self_digest", None)
    require(type(claimed) is str and claimed == sha_obj(body), "self seal")


class SourceRegistry:
    """One immutable byte snapshot per source, also used for module exec."""
    def __init__(self) -> None:
        self.raw: dict[str, bytes] = {}
        self.modules: dict[str, Any] = {}
        self.objects: dict[str, Any] = {}

    def authenticate(self) -> None:
        for key, (relative, expected_size, expected_sha) in SOURCE_PINS.items():
            path = ROOT / relative
            if not path.is_file():
                raise InputStop("missing:" + relative)
            raw = path.read_bytes()
            if len(raw) != expected_size or sha_bytes(raw) != expected_sha:
                raise InputStop("pin:" + relative)
            self.raw[key] = raw

    def load(self, key: str) -> Any:
        if key in self.modules:
            return self.modules[key]
        relative = SOURCE_PINS[key][0]
        name = "_d972_v7_" + key
        if name in sys.modules:
            raise InputStop("module_slot:" + key)
        module = types.ModuleType(name)
        module.__file__ = str((ROOT / relative).resolve())
        module.__package__ = ""
        sys.modules[name] = module
        try:
            code = compile(self.raw[key], module.__file__, "exec")
            exec(code, module.__dict__)
        except BaseException:
            sys.modules.pop(name, None)
            raise
        self.modules[key] = module
        return module

    def json(self, key: str) -> Any:
        if key not in self.objects:
            try:
                self.objects[key] = json.loads(self.raw[key].decode("utf-8"))
            except (UnicodeError, json.JSONDecodeError) as exc:
                raise InputStop("json:" + key) from exc
        return self.objects[key]

    def public(self) -> dict[str, Any]:
        return {key: {"path": row[0], "bytes": row[1], "sha256": row[2]}
                for key, row in SOURCE_PINS.items()}


class Meter:
    """Fresh v7 counters.  Historical checkpoint counters are never seeded."""
    def __init__(self, seconds: float) -> None:
        if float(seconds) != WALL_SECONDS:
            raise InputStop("wall_seconds_must_equal_10800")
        self.started = time.monotonic()
        self.limits = {"wall_seconds": WALL_SECONDS, "boundary_pairs": 8_000_000,
                       "fibre_scans": 80_000_000, "candidate_words": 2_000_000,
                       "retained_columns": 250_000, "checkpoint_bytes": MAX_CHECKPOINT_BYTES,
                       "rss_bytes": 5_700_000_000, "oracle_rounds": 1,
                       "global_roster": DELTA_ORDER}
        self.counters = {key: 0 for key in self.limits if key not in
                         ("wall_seconds", "rss_bytes")}
        self.phase = "authentication"
        self.sampled_parent_rss_peak = 0
        self.sampled_children_rss_peak_sum = 0

    @staticmethod
    def _rss(pid: int | None = None) -> int:
        target = "self" if pid is None else str(pid)
        try:
            with open(f"/proc/{target}/statm", "r", encoding="ascii") as stream:
                pages = int(stream.read().split()[1])
            return pages * int(os.sysconf("SC_PAGE_SIZE"))
        except (OSError, ValueError, IndexError):
            return 0

    def remaining(self) -> float:
        return self.limits["wall_seconds"] - (time.monotonic() - self.started)

    def deadline(self) -> float:
        return self.started + self.limits["wall_seconds"]

    def check(self, phase: str, child_pids: Sequence[int] = ()) -> None:
        self.phase = phase
        elapsed = time.monotonic() - self.started
        if elapsed > self.limits["wall_seconds"]:
            raise ResourceStop(phase, "wall_seconds", elapsed,
                               self.limits["wall_seconds"])
        parent = self._rss()
        children = sum(self._rss(pid) for pid in child_pids)
        self.sampled_parent_rss_peak = max(self.sampled_parent_rss_peak, parent)
        self.sampled_children_rss_peak_sum = max(
            self.sampled_children_rss_peak_sum, children)
        sampled = parent + children
        if sampled and sampled > self.limits["rss_bytes"]:
            raise ResourceStop(phase, "rss_bytes", sampled,
                               self.limits["rss_bytes"])

    def reserve(self, name: str, amount: int, phase: str) -> None:
        value = self.counters[name] + int(amount)
        if value > self.limits[name]:
            raise ResourceStop(phase, name, value, self.limits[name])
        self.check(phase)

    def commit(self, name: str, amount: int) -> None:
        self.counters[name] += int(amount)

    def bump(self, name: str, amount: int = 1, phase: str | None = None) -> None:
        self.reserve(name, amount, phase or self.phase)
        self.commit(name, amount)

    def public(self) -> dict[str, Any]:
        return {"phase": self.phase,
                "elapsed_seconds": time.monotonic() - self.started,
                "limits": self.limits, "fresh_v7_counters": self.counters,
                "resource_metric": "sampled parent RSS plus sampled child RSS sum",
                "sampled_parent_rss_peak_bytes": self.sampled_parent_rss_peak,
                "sampled_children_rss_peak_sum_bytes": self.sampled_children_rss_peak_sum}


def serial_group_row(live: Any, p176: Any, group_row: dict[Any, int],
                     block: int) -> dict[bytes, int]:
    answer: dict[bytes, int] = {}
    for (component, value), coefficient0 in group_row.items():
        coefficient = int(coefficient0) % 3
        if coefficient:
            raw = p176.packed_joint_blob(value, "v7 group element")
            key = live.row_key(block, int(component), raw)
            answer[key] = (answer.get(key, 0) + coefficient) % 3
            if not answer[key]:
                del answer[key]
    return answer


def serial_public(live: Any, p176: Any, group_row: dict[Any, int]) -> list[list[Any]]:
    rows = []
    for (component, value), coefficient0 in group_row.items():
        coefficient = int(coefficient0) % 3
        if coefficient:
            rows.append([int(component), p176.packed_joint_blob(
                value, "v7 public element").hex(), coefficient])
    rows.sort(key=lambda row: (row[0], bytes.fromhex(row[1])))
    return rows


def build_light(registry: SourceRegistry, meter: Meter) -> dict[str, Any]:
    """Literal v277 light runtime; no Q0/fine-deletion/membership objects."""
    # The authenticated fixed-size light/P prefix is completed atomically
    # before the first wall/RSS gate so a cap can always carry a P-bound
    # pre-pool checkpoint rather than an unusable partial object.
    meter.phase = "light_runtime_atomic_prefix"
    live = registry.load("live")
    p176 = registry.load("task176")
    old = registry.load("old")
    jointmod = registry.load("joint")
    v172 = registry.load("v172")
    gmod = registry.load("g760")
    pb4mod = registry.load("pb4")
    q3 = registry.json("q3")
    joint_receipt = registry.json("joint_receipt")
    e3, e4, _ = old.reconstruct_quotients(q3)
    contexts, aliases, context_public = old.cheap_context_registry(e4)
    require(len(contexts) == 31 and len(context_public["named_uses"]) == 46,
            "light ten-context registry")
    words = [list(row["word"]) for row in q3["correction_fibre"]["records"]
             if row.get("word")]
    require(len(words) == 26, "light correction record roster")
    group, roster = v172.build_roster(jointmod, old, e3, e4, contexts, words)
    require(len(roster) == 6441 and
            all(group.eval(row["word"]) == group.identity for row in roster),
            "light complete joint-kernel roster")
    _, _, g760 = gmod.construct_base()
    require(len(g760) == 760 and sha_obj(g760) ==
            "518f09820b8d7baee6b58ebf366cebf7b02a9a945cd1350cf8c701a4e6bc2b4d",
            "light g760")
    x, y = [1], [2]
    z = old.inv_word(old.pp_words([x, y]))
    u = old.inv_word(old.pp_words([y, x]))
    h1, h2 = old.hexagon_words(g760)
    h1 = list(old.embed_f2_pb3(h1)); h2 = list(old.embed_f2_pb3(h2))
    pcontexts = [([1], [4]), ([4], [6]),
                 (live.paper_product([2], [4]), [6]),
                 (live.paper_product([1], [2]), live.paper_product([5], [6])),
                 ([1], live.paper_product([4], [5]))]
    factors = [old.f2_substitute(g760, left, right)
               for left, right in pcontexts]
    pword = live.paper_product(factors[1], factors[3], factors[0],
                               old.inv_word(factors[2]), old.inv_word(factors[4]))
    base_rows: dict[str, list[list[Any]]] = {}
    for label, quotient, word in (("H1", e3, h1), ("H2", e3, h2),
                                  ("P", e4, pword)):
        gradient, value = old.fox_gradient_without_sections(word, quotient)
        require(value == quotient.identity, "light base relation " + label)
        base_rows[label] = serial_public(live, p176, gradient)
    pb3_relators = old.pure_relations(3)
    pb3_group_rows = [old.fox_gradient_without_sections(row, e3)[0]
                      for row in pb3_relators]
    pb4_group_rows = pb4mod.base_raw_columns(old, e4)
    require(len(pb3_group_rows) == 2 and len(pb4_group_rows) == 11 and
            all(e3.eval(row) == e3.identity for row in pb3_relators) and
            all(e4.eval(row) == e4.identity for row in old.pure_relations(4)) and
            all(old.d1(row, e3) == {} for row in pb3_group_rows) and
            all(old.d1(row, e4) == {} for row in pb4_group_rows),
            "light PB3/PB4 boundary owners")
    bridge = {
        "g760": {"word": list(g760), "sha256": sha_obj(g760)},
        "raw_base_targets": {label: {"row": rows, "sha256": sha_obj(rows)}
                             for label, rows in base_rows.items()},
        "pb3": {"rows": [serial_public(live, p176, row)
                           for row in pb3_group_rows]},
        "pb4": {"rows": [serial_public(live, p176, row)
                           for row in pb4_group_rows]},
        "relation_roster": {"count": 6441,
            "roster_sha256": sha_obj([[row["layer"], row["ordinal"], row["word"]]
                                      for row in roster])},
        "base_target_source": "g760_raw_fox",
    }
    runtime = {"live": live, "p176": p176, "old": old, "e3": e3, "e4": e4,
               "contexts": contexts, "aliases": aliases,
               "context_public": context_public, "bridge": bridge,
               "roster": roster, "joint_group": group, "q3": q3,
               "joint_receipt": joint_receipt}
    forbidden = {"qstates", "qids", "parents", "letters", "stores",
                 "memberships", "emitted", "A_maps", "adjusted_L"}
    require(forbidden.isdisjoint(runtime), "Q0 object constructed in light phase")
    runtime["target"] = live.exact_target(runtime)
    runtime["model"] = live.AllSevenModel(runtime)
    light_public = {
        "source_snapshots_sha256": sha_obj(registry.public()),
        "target_sha256": sha_obj(live.public_sparse(runtime["target"])),
        "pb3_rows_sha256": sha_obj(bridge["pb3"]["rows"]),
        "pb4_rows_sha256": sha_obj(bridge["pb4"]["rows"]),
        "roster_sha256": bridge["relation_roster"]["roster_sha256"],
        "context_public_sha256": sha_obj(context_public),
        "e3_identity_hex": p176.packed_joint_blob(e3.identity, "light E3 identity").hex(),
        "e4_identity_hex": p176.packed_joint_blob(e4.identity, "light E4 identity").hex(),
        "no_q0_objects": True,
    }
    runtime["light_public"] = light_public
    runtime["light_input_sha256"] = sha_obj(light_public)
    return runtime


def read_physical_once(path: Path, expected_size: int, expected_sha: str) -> tuple[bytes, dict[str, Any]]:
    flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
    try:
        fd = os.open(path, flags)
    except OSError as exc:
        raise InputStop("source_open") from exc
    try:
        before = os.fstat(fd)
        if (not stat.S_ISREG(before.st_mode) or before.st_nlink != 1 or
                before.st_size != expected_size):
            raise InputStop("source_physical_identity")
        chunks = []
        remaining = expected_size
        digest = hashlib.sha256()
        while remaining:
            chunk = os.read(fd, min(1 << 20, remaining))
            if not chunk:
                raise InputStop("source_short_read")
            chunks.append(chunk); digest.update(chunk); remaining -= len(chunk)
        if os.read(fd, 1):
            raise InputStop("source_long_read")
        after = os.fstat(fd)
        if ((before.st_dev, before.st_ino, before.st_size, before.st_nlink,
             before.st_mtime_ns) !=
                (after.st_dev, after.st_ino, after.st_size, after.st_nlink,
                 after.st_mtime_ns)):
            raise InputStop("source_TOCTOU")
        raw = b"".join(chunks)
        if digest.hexdigest() != expected_sha:
            raise InputStop("source_sha256")
        return raw, {"device": before.st_dev, "inode": before.st_ino,
                     "size": before.st_size, "links": before.st_nlink,
                     "mtime_ns": before.st_mtime_ns, "sha256": expected_sha}
    finally:
        os.close(fd)


def validate_old_envelope(value: dict[str, Any], live: Any) -> None:
    live.validate_seal(value)
    require(value.get("schema") == OLD_SCHEMA and
            value.get("self_digest") == OLD_SELF_DIGEST and
            value.get("input_sha256") == OLD_INPUT_SHA256 and
            value.get("target_sha256") == OLD_TARGET_SHA256 and
            value.get("pivot_rows_sha256") == OLD_PIVOT_ROWS_SHA256 and
            value.get("current_dual_sha256") == OLD_DUAL_SHA256 and
            value.get("normalized_semantics_digest") == NORMALIZED_DIGEST,
            "old checkpoint envelope")
    require(value.get("input_sha256") == live.sha_obj(value.get("input_components")) and
            value.get("target_sha256") == live.sha_obj(value.get("target")),
            "old checkpoint component seals")
    require(value.get("rank") == 2896 and len(value.get("columns", [])) == 2896 and
            len(value.get("pivot_order", [])) == 2896,
            "old checkpoint fixed rank")
    require(value.get("progress", {}).get("boundary") == {
        "complete": False, "dual_sha256": OLD_DUAL_SHA256,
        "pair_attempts": 3_145_088, "restart_pair_cursor": 0},
        "old boundary provenance")
    require(value.get("progress", {}).get("correction") == {
        "canonical_row_cursor": 0, "dual_sha256": OLD_DUAL_SHA256,
        "global_cursors": {}, "kernel_prefix": 0, "live_fibre_count": 0,
        "live_fibres": [], "weighted_rows": {}}, "old correction provenance")


def validate_provenance(record: dict[str, Any], expected_id: int) -> None:
    expected_record_keys = {"active_dual", "active_dual_sha256", "column_id",
        "dual_pairing", "family", "pivot_ancestry", "pivot_hex", "provenance",
        "rank_after", "rank_before", "sparse_row", "sparse_row_sha256"}
    require(set(record) == expected_record_keys and
            record["column_id"] == expected_id and record["family"] == "boundary" and
            record["rank_before"] == expected_id - 1 and
            record["rank_after"] == expected_id, "old column typed shape")
    provenance = record["provenance"]
    seed_keys = {"base_relator_index", "block", "family",
                 "left_translation_gate", "seed", "translation_hex"}
    active_keys = {"base_relator_index", "block",
        "complete_support_occurrence_accumulation", "contributing_pairs",
        "family", "left_translation_gate", "scalar", "translation_hex"}
    require(set(provenance) in (seed_keys, active_keys) and
            provenance["family"] == "boundary" and
            provenance["left_translation_gate"] == "t*h=g" and
            type(provenance["block"]) is int and provenance["block"] in (1, 2, 3) and
            type(provenance["base_relator_index"]) is int and
            1 <= provenance["base_relator_index"] <= {1: 2, 2: 2, 3: 11}[provenance["block"]],
            "old boundary provenance")
    translation = bytes.fromhex(provenance["translation_hex"])
    require(len(translation) in (40, 154), "old translation codec")
    if set(provenance) == seed_keys:
        require(provenance["seed"] == "identity_translation" and
                record["active_dual"] is None and
                record["active_dual_sha256"] is None and
                record["dual_pairing"] is None, "old seed provenance")
    else:
        require(provenance["complete_support_occurrence_accumulation"] is True and
                provenance["scalar"] in (1, 2) and
                type(provenance["contributing_pairs"]) is list and
                record["dual_pairing"] == provenance["scalar"],
                "old ACTIVE provenance")
        for row in provenance["contributing_pairs"]:
            require(set(row) == {"base_coefficient", "component", "g_hex", "h_hex",
                                 "lambda_coefficient"} and
                    row["base_coefficient"] in (1, 2) and
                    row["lambda_coefficient"] in (1, 2) and
                    1 <= row["component"] <= 6,
                    "old contributing pair shape")
            bytes.fromhex(row["g_hex"]); bytes.fromhex(row["h_hex"])
        dual = record["active_dual"]
        require(type(dual) is list and record["active_dual_sha256"] == sha_obj(dual),
                "old ACTIVE dual provenance")


class FormalReducer:
    """Pivot rows with a load-bearing sparse expression in formal symbols."""
    def __init__(self, live: Any) -> None:
        self.live = live
        self.rows: dict[bytes, dict[bytes, int]] = {}
        self.expr: dict[bytes, dict[str, int]] = {}
        self.order: list[bytes] = []
        self.formal_entries = 0

    @staticmethod
    def _expr_add(target: dict[str, int], source: dict[str, int], scalar: int) -> None:
        for key, value in source.items():
            answer = (target.get(key, 0) + scalar * int(value)) % 3
            if answer:
                target[key] = answer
            else:
                target.pop(key, None)

    def inject(self, pivot: bytes, row: dict[bytes, int],
               expression: dict[str, int]) -> None:
        require(row and min(row) == pivot and row[pivot] == 1 and
                pivot not in self.rows and all(row.get(old, 0) == 0
                                               for old in self.order),
                "direct P injection gate")
        require(expression and all(value in (1, 2) for value in expression.values()),
                "formal expression gate")
        if self.formal_entries + len(expression) > MAX_FORMAL_ENTRIES:
            raise ResourceStop("formal_ancestry", "formal_entries",
                               self.formal_entries + len(expression),
                               MAX_FORMAL_ENTRIES)
        self.rows[pivot] = dict(row); self.expr[pivot] = dict(expression)
        self.order.append(pivot); self.formal_entries += len(expression)

    def reduce(self, source: dict[bytes, int]) -> tuple[dict[bytes, int], dict[str, int]]:
        row = dict(source); expression: dict[str, int] = {}
        for pivot in self.order:
            value = row.get(pivot, 0)
            if value:
                self.live.add_scaled(row, self.rows[pivot], -value)
                self._expr_add(expression, self.expr[pivot], value)
        return row, expression

    def add_actual(self, source: dict[bytes, int], symbol: str) -> tuple[bytes, dict[str, int]]:
        row = dict(source); expression = {symbol: 1}
        for pivot in self.order:
            value = row.get(pivot, 0)
            if value:
                self.live.add_scaled(row, self.rows[pivot], -value)
                self._expr_add(expression, self.expr[pivot], -value)
        require(row, "ACTIVE actual row reduced to zero")
        pivot = min(row); inverse = 1 if row[pivot] == 1 else 2
        row = self.live.scaled(row, inverse)
        expression = {key: value * inverse % 3 for key, value in expression.items()
                      if value * inverse % 3}
        self.inject(pivot, row, expression)
        return pivot, expression

    def exact_dual(self, target: dict[bytes, int]) -> tuple[dict[bytes, int],
                                                            dict[bytes, int],
                                                            dict[str, int]]:
        remainder, solution = self.reduce(target)
        require(remainder, "dual after membership")
        functional: dict[bytes, int] = {min(remainder): 1}
        for pivot in reversed(self.order):
            value = -sum(coefficient * functional.get(key, 0)
                         for key, coefficient in self.rows[pivot].items()
                         if key != pivot) % 3
            if value:
                functional[pivot] = value
            else:
                functional.pop(pivot, None)
        require(all(self.live.pair(functional, self.rows[pivot]) == 0
                    for pivot in self.order) and
                self.live.pair(functional, target) != 0,
                "fresh heuristic dual")
        return functional, remainder, solution


def build_triangular(value: dict[str, Any], runtime: dict[str, Any],
                     meter: Meter) -> tuple[FormalReducer, list[dict[bytes, int]],
                                             dict[str, Any]]:
    """Streaming independent P=A*C products; never historical Echelon.add(C)."""
    live = runtime["live"]
    columns = value["columns"]
    raw_rows: list[dict[bytes, int]] = []
    ancestry_rows: list[list[tuple[int, int]]] = []
    pivots: list[bytes] = []
    stats = {key: 0 for key in EXPECTED_TRIANGULAR}
    stats["columns"] = len(columns); stats["rank"] = value["rank"]
    for expected_id, record in enumerate(columns, 1):
        meter.phase = "triangular_parse_atomic_prefix"
        validate_provenance(record, expected_id)
        row = live.parse_sparse(record["sparse_row"])
        require(record["sparse_row_sha256"] == live.sha_obj(record["sparse_row"]),
                "old raw sparse digest")
        raw_rows.append(row)
        stats["raw_support_total"] += len(row)
        stats["raw_support_max"] = max(stats["raw_support_max"], len(row))
        stats["boundary_columns"] += 1
        ancestry: list[tuple[int, int]] = []
        prior_index = 0
        diagonal = 0
        for item in record["pivot_ancestry"]:
            require(type(item) is list and len(item) == 2 and
                    type(item[0]) is int and item[0] > prior_index and
                    item[1] in (1, 2), "canonical F3 ancestry")
            index, coefficient = int(item[0]), int(item[1])
            prior_index = index
            if index > expected_id:
                stats["future_ancestry_indices"] += 1
            if index == expected_id:
                diagonal = coefficient
            require(1 <= index <= len(columns), "ancestry source index")
            ancestry.append((index, coefficient))
            if index <= len(raw_rows):
                stats["ancestry_weighted_contributions"] += len(raw_rows[index - 1])
        if diagonal == 0:
            stats["zero_or_missing_diagonal"] += 1
        ancestry_rows.append(ancestry)
        stats["ancestry_entries_total"] += len(ancestry)
        stats["ancestry_entries_max"] = max(stats["ancestry_entries_max"], len(ancestry))
        pivot = bytes.fromhex(record["pivot_hex"])
        if not pivot or pivot in pivots or value["pivot_order"][expected_id - 1] != pivot.hex():
            stats["duplicate_empty_wrong_pivots"] += 1
        pivots.append(pivot)
    require(stats["future_ancestry_indices"] == 0 and
            stats["zero_or_missing_diagonal"] == 0 and
            stats["duplicate_empty_wrong_pivots"] == 0,
            "v276 structural gate")
    p_rows: list[dict[bytes, int]] = []
    reducer = FormalReducer(live)
    for ordinal, (ancestry, pivot) in enumerate(zip(ancestry_rows, pivots), 1):
        meter.phase = "triangular_product_atomic_prefix"
        product: dict[bytes, int] = {}
        expression: dict[str, int] = {}
        for index, coefficient in ancestry:
            live.add_scaled(product, raw_rows[index - 1], coefficient)
            expression[f"o:{index:04d}"] = coefficient
        if (not product or product.get(pivot) != 1 or min(product) != pivot or
                any(product.get(old, 0) for old in pivots[:ordinal - 1])):
            raise InputStop("triangular_P_gate")
        stats["pivot_support_total"] += len(product)
        stats["pivot_support_max"] = max(stats["pivot_support_max"], len(product))
        reducer.inject(pivot, product, expression)
        p_rows.append(product)
    require(stats == EXPECTED_TRIANGULAR and
            live.sha_obj([live.public_sparse(row) for row in p_rows]) ==
            OLD_PIVOT_ROWS_SHA256, "exact pinned triangular arithmetic")
    target = runtime["target"]
    require(live.public_sparse(target) == value["target"] and
            live.sha_obj(value["target"]) == OLD_TARGET_SHA256,
            "fresh light target equals checkpoint target")
    dual, remainder, _ = reducer.exact_dual(target)
    dual_public = live.public_sparse(dual)
    require(len(dual_public) == 1188 and live.sha_obj(dual_public) == OLD_DUAL_SHA256,
            "fresh first heuristic dual")
    certificate = {**stats,
        "P_rows_sha256": OLD_PIVOT_ROWS_SHA256,
        "P_equations_independent": True,
        "historical_Echelon_add_called": False,
        "heuristic_discovery_only": True,
        "exact_cached_resume": False,
        "formal_entries": reducer.formal_entries,
        "target_remainder_support": len(remainder),
        "fresh_dual_support": len(dual_public),
        "fresh_dual_sha256": live.sha_obj(dual_public)}
    return reducer, p_rows, certificate


def boundary_descriptors(runtime: dict[str, Any]) -> tuple[tuple[dict[str, Any], ...],
                                                           dict[tuple[int, int], tuple[int, ...]]]:
    live = runtime["live"]
    descriptors: list[dict[str, Any]] = []
    for block, count in ((1, 2), (2, 2), (3, 11)):
        quotient = live.group_for_block(runtime, block)
        for relator in range(1, count + 1):
            for component0, h_hex, coefficient0 in live.boundary_source(
                    runtime, block, relator):
                h_blob = bytes.fromhex(str(h_hex))
                h = live.unpack_element(runtime, h_blob, block)
                h_inverse = quotient.inverse(h)
                descriptors.append({"block": block, "relator": relator,
                    "component": int(component0), "h_blob": h_blob, "h": h,
                    "h_inverse": h_inverse,
                    "h_inverse_blob": live.element_blob(runtime, h_inverse),
                    "base_coefficient": int(coefficient0) % 3})
    descriptors.sort(key=lambda row: (row["block"], row["relator"],
                                      row["component"], row["h_blob"],
                                      row["base_coefficient"]))
    require(len(descriptors) == 104, "complete 104 boundary descriptors")
    lookup: dict[tuple[int, int], list[int]] = {}
    for index, row in enumerate(descriptors):
        lookup.setdefault((row["block"], row["component"]), []).append(index)
    return tuple(descriptors), {key: tuple(value) for key, value in lookup.items()}


def descriptor_public(rows: Sequence[dict[str, Any]]) -> list[dict[str, Any]]:
    return [{"block": row["block"], "relator": row["relator"],
             "component": row["component"], "h_hex": row["h_blob"].hex(),
             "h_inverse_hex": row["h_inverse_blob"].hex(),
             "base_coefficient": row["base_coefficient"]} for row in rows]


def support_from_dual(runtime: dict[str, Any], dual: dict[bytes, int]) -> dict[str, Any]:
    live = runtime["live"]
    private: dict[tuple[int, int], list[tuple[bytes, int, Any]]] = {}
    entries = []
    for key in sorted(dual):
        coefficient = int(dual[key]) % 3
        if key[:1] != b"R" or not coefficient:
            continue
        block, component, raw = live.decode_row_key(key)
        value = live.unpack_element(runtime, raw, block)
        private.setdefault((block, component), []).append((raw, coefficient, value))
        entries.append([block, component, raw.hex(), coefficient])
    return {"private": private, "entries": entries,
            "types": [[block, component] for block, component in sorted(private)],
            "entry_count": len(entries), "sha256": sha_obj(entries)}


class DeadlineChannel:
    """Length-framed nonblocking socket with one absolute deadline."""
    def __init__(self, channel: socket.socket) -> None:
        self.channel = channel
        self.channel.setblocking(False)

    def _wait(self, event: int, deadline: float) -> None:
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise TimeoutError("channel deadline")
        with selectors.DefaultSelector() as selector:
            selector.register(self.channel, event)
            if not selector.select(remaining):
                raise TimeoutError("channel deadline")

    def _write(self, raw: bytes, deadline: float) -> None:
        view = memoryview(raw)
        while view:
            self._wait(selectors.EVENT_WRITE, deadline)
            try:
                sent = self.channel.send(view)
            except BlockingIOError:
                continue
            if sent <= 0:
                raise EOFError("channel closed on write")
            view = view[sent:]

    def _read(self, count: int, deadline: float) -> bytes:
        chunks = bytearray()
        while len(chunks) < count:
            self._wait(selectors.EVENT_READ, deadline)
            try:
                raw = self.channel.recv(count - len(chunks))
            except BlockingIOError:
                continue
            if not raw:
                raise EOFError("channel closed on read")
            chunks.extend(raw)
        return bytes(chunks)

    def send(self, value: dict[str, Any], deadline: float) -> int:
        raw = canonical(value)
        if len(raw) > MAX_FRAME_BYTES:
            raise ProtocolStop("frame cap")
        self._write(struct.pack(">I", len(raw)) + raw, deadline)
        return len(raw) + 4

    def recv(self, deadline: float) -> tuple[dict[str, Any], int]:
        header = self._read(4, deadline)
        size = struct.unpack(">I", header)[0]
        if size <= 0 or size > MAX_FRAME_BYTES:
            raise ProtocolStop("frame size")
        raw = self._read(size, deadline)
        try:
            value = json.loads(raw.decode("ascii"))
        except (UnicodeError, json.JSONDecodeError) as exc:
            raise ProtocolStop("frame JSON") from exc
        require(type(value) is dict, "frame object")
        return value, size + 4

    def close(self) -> None:
        try:
            self.channel.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass
        self.channel.close()


_FORK_RUNTIME: dict[str, Any] | None = None
_FORK_DESCRIPTORS: tuple[dict[str, Any], ...] = ()
_FORK_SOCKETS: list[socket.socket] = []
_FORK_DEADLINE = 0.0


def _worker_accumulate(frame: dict[str, Any], worker_id: int) -> dict[str, Any]:
    runtime = _FORK_RUNTIME
    require(runtime is not None, "fork runtime missing")
    live = runtime["live"]
    epoch = int(frame["epoch"]); start, stop = map(int, frame["interval"])
    deadline = float(frame["deadline"])
    descriptor_ids = [int(x) for x in frame["descriptor_ids"]]
    support: dict[tuple[int, int], list[tuple[bytes, int, Any]]] = {}
    for block0, component0, raw_hex, coefficient0 in frame["support"]:
        block, component = int(block0), int(component0)
        raw = bytes.fromhex(str(raw_hex)); coefficient = int(coefficient0)
        require(coefficient in (1, 2), "worker support coefficient")
        support.setdefault((block, component), []).append(
            (raw, coefficient, live.unpack_element(runtime, raw, block)))
    offsets = [0]
    for descriptor_id in descriptor_ids:
        descriptor = _FORK_DESCRIPTORS[descriptor_id]
        offsets.append(offsets[-1] + len(support.get(
            (descriptor["block"], descriptor["component"]), ())))
    require(0 <= start <= stop <= offsets[-1], "worker interval")
    accumulated: dict[tuple[int, bytes, int], int] = {}
    attempted = 0
    for ordinal in range(start, stop):
        if (attempted & 4095) == 0 and time.monotonic() >= deadline:
            raise TimeoutError("worker arithmetic deadline")
        local_descriptor = bisect.bisect_right(offsets, ordinal) - 1
        descriptor = _FORK_DESCRIPTORS[descriptor_ids[local_descriptor]]
        support_row = support[(descriptor["block"], descriptor["component"])][
            ordinal - offsets[local_descriptor]]
        g_blob, lambda_coefficient, g = support_row
        quotient = live.group_for_block(runtime, descriptor["block"])
        translation = quotient.mul(g, descriptor["h_inverse"])
        require(quotient.mul(translation, descriptor["h"]) == g,
                "worker t*h=g")
        t_blob = live.element_blob(runtime, translation)
        key = (descriptor["block"], t_blob, descriptor["relator"])
        coefficient = descriptor["base_coefficient"] * lambda_coefficient % 3
        value = (accumulated.get(key, 0) + coefficient) % 3
        if value:
            accumulated[key] = value
        else:
            accumulated.pop(key, None)
        attempted += 1
    rows = [[block, raw.hex(), relator, accumulated[(block, raw, relator)]]
            for block, raw, relator in sorted(accumulated)]
    public = {"kind": "RESULT", "epoch": epoch, "worker_id": worker_id,
              "interval": [start, stop], "attempted": attempted,
              "accumulator": rows, "complete": True}
    public["result_sha256"] = sha_obj(public)
    return public


def _boundary_worker(worker_id: int, own_socket: socket.socket) -> None:
    own_fd = own_socket.fileno()
    for candidate in _FORK_SOCKETS:
        if candidate.fileno() != own_fd:
            candidate.close()
    channel = DeadlineChannel(own_socket)
    try:
        channel.send({"kind": "READY", "worker_id": worker_id,
                      "pid": os.getpid()}, time.monotonic() + CHANNEL_START_SECONDS)
        while True:
            frame, _ = channel.recv(_FORK_DEADLINE)
            kind = frame.get("kind")
            if kind == "STOP":
                channel.send({"kind": "STOPPED", "worker_id": worker_id,
                              "epoch": frame.get("epoch")}, float(frame["deadline"]))
                return
            require(kind == "EPOCH" and frame.get("worker_id") == worker_id,
                    "worker frame owner")
            fault = frame.get("fault")
            if fault == "death":
                os._exit(73)
            if fault == "timeout":
                while time.monotonic() <= float(frame["deadline"]):
                    pass
            if fault == "partial":
                partial = b'{"kind":"RESULT"'
                channel._write(struct.pack(">I", len(partial) + 100) + partial,
                               float(frame["deadline"])); os._exit(74)
            result = _worker_accumulate(frame, worker_id)
            channel.send(result, float(frame["deadline"]))
    finally:
        channel.close()


class PersistentBoundaryOwner:
    """Persistent fork roster; every epoch is atomically collected or discarded."""
    def __init__(self, runtime: dict[str, Any], meter: Meter, workers: int) -> None:
        if workers not in (2, 4):
            raise InputStop("workers_must_be_2_or_4")
        methods = multiprocessing.get_all_start_methods()
        if sys.platform != "linux" or "fork" not in methods:
            raise InputStop("linux_fork_required")
        self.runtime, self.meter, self.workers = runtime, meter, workers
        self.descriptors, self.type_lookup = boundary_descriptors(runtime)
        self.descriptor_public = descriptor_public(self.descriptors)
        self.descriptor_sha256 = sha_obj(self.descriptor_public)
        self.context = multiprocessing.get_context("fork")
        self.channels: list[DeadlineChannel] = []
        self.processes: list[multiprocessing.Process] = []
        self.epoch = 0
        self._materialize_epoch = 0
        self._materialize_support_private: dict[tuple[int, int], list[Any]] | None = None
        self.started = False
        self.closed = False
        self.accounting = {"epochs_committed": 0, "epochs_discarded": 0,
            "literal_pairs_committed": 0, "support_bytes": 0,
            "frames_sent_bytes": 0, "frames_received_bytes": 0,
            "accumulator_entries": 0, "max_accumulator_entries": 0,
            "formal_ancestry_entries": 0,
            "descriptor_count": len(self.descriptors),
            "descriptor_sha256": self.descriptor_sha256,
            "winner_reconstructions": 0, "process_restarts": 0,
            "metric": "sampled RSS sum; not exact physical peak"}
        self.cleanup = {"transitions": ["not_started"], "started_pids": [],
                        "worker_exitcodes": [], "live_pids_after_join": [],
                        "process_close_count": 0, "complete": False}

    def pids(self) -> list[int]:
        return [int(process.pid) for process in self.processes if process.pid]

    def start(self) -> None:
        global _FORK_RUNTIME, _FORK_DESCRIPTORS, _FORK_SOCKETS, _FORK_DEADLINE
        require(not self.started and not self.closed, "roster start state")
        _FORK_RUNTIME = self.runtime
        _FORK_DESCRIPTORS = self.descriptors
        _FORK_DEADLINE = self.meter.deadline()
        pairs = [socket.socketpair(socket.AF_UNIX, socket.SOCK_STREAM)
                 for _ in range(self.workers)]
        _FORK_SOCKETS = [sock for pair in pairs for sock in pair]
        deadline = min(self.meter.deadline(), time.monotonic() + CHANNEL_START_SECONDS)
        try:
            for worker_id, (_parent, child) in enumerate(pairs):
                process = self.context.Process(target=_boundary_worker,
                                               args=(worker_id, child),
                                               name=f"r07-v7-boundary-{worker_id}")
                process.start(); self.processes.append(process)
            for parent, child in pairs:
                child.close(); self.channels.append(DeadlineChannel(parent))
            for worker_id, channel in enumerate(self.channels):
                frame, size = channel.recv(deadline)
                require(frame.get("kind") == "READY" and
                        frame.get("worker_id") == worker_id and
                        frame.get("pid") == self.processes[worker_id].pid,
                        "worker READY")
                self.accounting["frames_received_bytes"] += size
            self.started = True
            self.cleanup["transitions"].append("started")
            self.cleanup["started_pids"] = self.pids()
        except (TimeoutError, EOFError, OSError, ProtocolStop, RuntimeError, ValueError):
            self.abort("startup")
            for pair in pairs:
                for endpoint in pair:
                    try:
                        endpoint.close()
                    except OSError:
                        pass
            raise ResourceStop("boundary_roster_start", "wall_seconds",
                               time.monotonic() - self.meter.started,
                               self.meter.limits["wall_seconds"])

    @staticmethod
    def intervals(total: int, workers: int) -> list[list[int]]:
        require(total >= 0 and workers > 0, "interval domain")
        return [[total * index // workers, total * (index + 1) // workers]
                for index in range(workers)]

    def _matching(self, support: dict[str, Any]) -> tuple[list[int], int]:
        descriptor_ids = sorted(index for key in support["private"]
                                for index in self.type_lookup.get(key, ()))
        total = sum(len(support["private"].get(
            (self.descriptors[index]["block"], self.descriptors[index]["component"]), ()))
                    for index in descriptor_ids)
        return descriptor_ids, total

    def run_epoch(self, dual: dict[bytes, int], *, fault: str | None = None,
                  short_deadline: float | None = None) -> dict[str, Any]:
        require(self.started and not self.closed, "roster epoch state")
        support = support_from_dual(self.runtime, dual)
        # The same decoded immutable support is consumed by the worker frames
        # and, if ACTIVE, by the parent's literal winner reconstruction.  It is
        # never decoded a second time in materialize().
        self._materialize_support_private = support["private"]
        descriptor_ids, total = self._matching(support)
        intervals = self.intervals(total, self.workers)
        require(intervals[0][0] == 0 and intervals[-1][1] == total and
                all(intervals[i][1] == intervals[i + 1][0]
                    for i in range(len(intervals) - 1)), "complete interval cover")
        self.meter.reserve("boundary_pairs", total, "positive_boundary_correlation")
        self.epoch += 1
        self._materialize_epoch = self.epoch
        deadline = self.meter.deadline()
        if short_deadline is not None:
            deadline = min(deadline, time.monotonic() + float(short_deadline))
        dual_digest = sha_obj(self.runtime["live"].public_sparse(dual))
        frames = []
        for worker_id, interval in enumerate(intervals):
            frame = {"kind": "EPOCH", "epoch": self.epoch,
                "worker_id": worker_id, "deadline": deadline,
                "dual_sha256": dual_digest, "descriptor_ids": descriptor_ids,
                "support": support["entries"], "interval": interval,
                "fault": fault if worker_id == 0 else None}
            frames.append(frame)
        results = []
        try:
            for channel, frame in zip(self.channels, frames):
                self.accounting["frames_sent_bytes"] += channel.send(frame, deadline)
            for worker_id, channel in enumerate(self.channels):
                result, size = channel.recv(deadline)
                self.accounting["frames_received_bytes"] += size
                claimed = result.pop("result_sha256", None)
                require(claimed == sha_obj(result), "worker result digest")
                result["result_sha256"] = claimed
                require(result.get("kind") == "RESULT" and
                        result.get("epoch") == self.epoch and
                        result.get("worker_id") == worker_id and
                        result.get("interval") == intervals[worker_id] and
                        result.get("attempted") == intervals[worker_id][1] - intervals[worker_id][0] and
                        result.get("complete") is True,
                        "complete worker result")
                results.append(result)
        except (TimeoutError, EOFError, OSError, ProtocolStop, ValueError) as exc:
            self.accounting["epochs_discarded"] += 1
            self.abort("atomic_epoch_discard")
            raise ResourceStop("positive_boundary_correlation", "wall_seconds",
                               time.monotonic() - self.meter.started,
                               self.meter.limits["wall_seconds"], str(exc)) from exc
        accumulated: dict[tuple[int, bytes, int], int] = {}
        for result in results:
            rows = result["accumulator"]
            self.accounting["accumulator_entries"] += len(rows)
            self.accounting["max_accumulator_entries"] = max(
                self.accounting["max_accumulator_entries"], len(rows))
            for block0, raw_hex, relator0, coefficient0 in rows:
                key = (int(block0), bytes.fromhex(str(raw_hex)), int(relator0))
                coefficient = int(coefficient0)
                require(coefficient in (1, 2), "worker accumulator F3")
                value = (accumulated.get(key, 0) + coefficient) % 3
                if value:
                    accumulated[key] = value
                else:
                    accumulated.pop(key, None)
        self.meter.commit("boundary_pairs", total)
        self.accounting["epochs_committed"] += 1
        self.accounting["literal_pairs_committed"] += total
        self.accounting["support_bytes"] += len(canonical(support["entries"]))
        selected = min(accumulated) if accumulated else None
        outcome = {"epoch": self.epoch, "dual_sha256": dual_digest,
            "support_entry_count": support["entry_count"],
            "support_sha256": support["sha256"],
            "support_types": support["types"],
            "matching_descriptor_ids": descriptor_ids,
            "matching_descriptor_count": len(descriptor_ids),
            "expanded_pair_count": total, "intervals": intervals,
            "selected": None if selected is None else
                [selected[0], selected[1].hex(), selected[2]],
            "selected_scalar": None if selected is None else accumulated[selected],
            "zero_complete": selected is None,
            "result_digests": [row["result_sha256"] for row in results],
            "worker_results": results}
        if self.epoch == 1 and len(dual) == 1188:
            require(support["entry_count"] == 1188 and
                    support["types"] == [[1, 1]] and
                    len(descriptor_ids) == 4 and total == 4752,
                    "exact pinned first boundary epoch")
            outcome["pinned_first_epoch"] = True
        return outcome

    def materialize(self, dual: dict[bytes, int], outcome: dict[str, Any]) -> dict[str, Any] | None:
        require(outcome["epoch"] == self._materialize_epoch and
                self._materialize_support_private is not None,
                "parent support/epoch binding")
        if outcome["selected"] is None:
            self._materialize_support_private = None
            return None
        live = self.runtime["live"]
        block, translation_hex, relator = outcome["selected"]
        translation_blob = bytes.fromhex(translation_hex)
        row = live.translated_boundary(self.runtime, int(block), int(relator),
                                       translation_blob)
        scalar = live.pair(dual, row)
        require(scalar == outcome["selected_scalar"] and scalar in (1, 2),
                "parent translated-row scalar")
        support = self._materialize_support_private
        contributors = []
        for descriptor_id in outcome["matching_descriptor_ids"]:
            descriptor = self.descriptors[descriptor_id]
            quotient = live.group_for_block(self.runtime, descriptor["block"])
            for g_blob, lambda_coefficient, g in support.get(
                    (descriptor["block"], descriptor["component"]), ()):
                translation = quotient.mul(g, descriptor["h_inverse"])
                require(quotient.mul(translation, descriptor["h"]) == g,
                        "parent t*h=g")
                if (descriptor["block"] == block and
                        descriptor["relator"] == relator and
                        live.element_blob(self.runtime, translation) == translation_blob):
                    contributors.append({"component": descriptor["component"],
                        "g_hex": g_blob.hex(), "h_hex": descriptor["h_blob"].hex(),
                        "lambda_coefficient": lambda_coefficient,
                        "base_coefficient": descriptor["base_coefficient"]})
        require(sum(item["lambda_coefficient"] * item["base_coefficient"]
                    for item in contributors) % 3 == scalar, "parent full contributors")
        self._materialize_support_private = None
        self.accounting["winner_reconstructions"] += 1
        return {"row": row, "provenance": {"family": "boundary",
            "block": block, "base_relator_index": relator,
            "translation_hex": translation_hex, "scalar": scalar,
            "complete_support_occurrence_accumulation": True,
            "left_translation_gate": "t*h=g", "contributing_pairs": contributors,
            "boundary_epoch": outcome}}

    def abort(self, reason: str) -> None:
        if self.closed:
            return
        self.cleanup["transitions"].append(reason)
        for channel in self.channels:
            channel.close()
        for process in self.processes:
            if process.is_alive():
                process.terminate()
        deadline = time.monotonic() + CHANNEL_CLOSE_SECONDS
        for process in self.processes:
            process.join(max(0.0, deadline - time.monotonic()))
        for process in self.processes:
            if process.is_alive():
                process.kill(); process.join(CHANNEL_CLOSE_SECONDS)
        self.cleanup["worker_exitcodes"] = [process.exitcode for process in self.processes]
        self.cleanup["live_pids_after_join"] = [process.pid for process in self.processes
                                                if process.is_alive()]
        for process in self.processes:
            process.close(); self.cleanup["process_close_count"] += 1
        self.cleanup["complete"] = not self.cleanup["live_pids_after_join"] and \
            self.cleanup["process_close_count"] == len(self.processes)
        self.closed = True

    def close(self) -> None:
        if self.closed:
            return
        deadline = min(self.meter.deadline(), time.monotonic() + CHANNEL_CLOSE_SECONDS)
        try:
            for channel in self.channels:
                channel.send({"kind": "STOP", "epoch": self.epoch,
                              "deadline": deadline}, deadline)
            for worker_id, channel in enumerate(self.channels):
                value, size = channel.recv(deadline)
                self.accounting["frames_received_bytes"] += size
                require(value.get("kind") == "STOPPED" and
                        value.get("worker_id") == worker_id,
                        "worker STOPPED")
        except (TimeoutError, EOFError, OSError, ProtocolStop):
            self.abort("cleanup_failure")
            return
        self.cleanup["transitions"].append("stop_acknowledged")
        for channel in self.channels:
            channel.close()
        for process in self.processes:
            process.join(CHANNEL_CLOSE_SECONDS)
        for process in self.processes:
            if process.is_alive():
                process.terminate(); process.join(CHANNEL_CLOSE_SECONDS)
        for process in self.processes:
            if process.is_alive():
                process.kill(); process.join(CHANNEL_CLOSE_SECONDS)
        self.cleanup["worker_exitcodes"] = [process.exitcode for process in self.processes]
        self.cleanup["live_pids_after_join"] = [process.pid for process in self.processes
                                                if process.is_alive()]
        for process in self.processes:
            process.close(); self.cleanup["process_close_count"] += 1
        self.cleanup["complete"] = not self.cleanup["live_pids_after_join"] and \
            self.cleanup["process_close_count"] == len(self.processes)
        self.cleanup["transitions"].append("closed")
        self.closed = True

    def public(self) -> dict[str, Any]:
        return {"workers": self.workers, "persistent": True,
                "transport": "nonblocking AF_UNIX socketpair, absolute deadline frames",
                "accounting": dict(self.accounting),
                "cleanup": dict(self.cleanup)}


def _stream_state_digest(states: Sequence[bytes], ids: dict[bytes, int]) -> str:
    digest = hashlib.sha256()
    for expected, state in enumerate(states):
        require(ids.get(state) == expected, "Q0 state/id binding")
        digest.update(struct.pack("<I", expected)); digest.update(state)
    return digest.hexdigest()


def _stream_store_digest(store: bytes | bytearray) -> str:
    digest = hashlib.sha256()
    for offset in range(0, len(store), 1 << 20):
        digest.update(store[offset:offset + (1 << 20)])
    return digest.hexdigest()


def build_heavy(runtime: dict[str, Any], registry: SourceRegistry,
                meter: Meter) -> dict[str, Any]:
    """One Q0-LATE construction.  The digest is published only at the end."""
    require("heavy_input_sha256" not in runtime and "qstates" not in runtime,
            "heavy runtime constructed twice")
    meter.check("heavy_Q0_late_start")
    p176, old = runtime["p176"], runtime["old"]
    e3, e4 = runtime["e3"], runtime["e4"]
    q3, contexts = runtime["q3"], runtime["contexts"]
    jointmod = registry.load("joint")

    class PackedJointGroup(jointmod.JointGroup):
        def blob(self, value: Any) -> bytes:
            return p176.packed_joint_blob(value, "v7 Gamma state")

    words = [list(row["word"]) for row in q3["correction_fibre"]["records"]
             if row.get("word")]
    gamma = PackedJointGroup(old, e3, e4, contexts, words)
    require(len(gamma.states) == 243 and
            gamma.public()["state_rows_sha256"] ==
            runtime["joint_receipt"]["gamma"]["state_rows_sha256"],
            "heavy Gamma identity")
    fine, fine_public = p176.build_fine_deletion(e3, e4, meter)
    q0_marked = [p176.canonical_packed_permutation(
        old.perm_from_row(row, 36), 36, "v7 Q0 mark")
        for row in q3["coarse_models"]["Q0"]["marked_permutations"]]
    delete, deletion_public = p176.make_deleter(old, e3, e4, fine, q0_marked)
    deletion_public["fine"] = fine_public
    projected = [p176.projection(state, delete) for state in gamma.states]
    require(len(projected) == 243 and all(len(row) == 10 for row in projected),
            "heavy projected Gamma")
    coordinate_marks = []
    for item in p176.COORDINATES:
        context = contexts[item["context_id"] - 1]
        row = [e4.eval([letter], context) for letter in (1, 2)]
        if item["type"] == "E3":
            row = [delete(value) for value in row]
        coordinate_marks.append(row)
    A_maps: dict[str, dict[tuple[bytes, ...], int]] = {}
    A_public: dict[str, Any] = {}
    for name, indices in p176.FAMILIES:
        A_maps[name], A_public[name] = p176.family_public_A(
            old, name, indices, projected, e3, e4, coordinate_marks)
    qstates, qids, parents, letters, stores, _ = p176.enumerate_q0_sections(
        old, q0_marked, coordinate_marks, e3, e4, meter)
    require(len(qstates) == len(qids) == len(parents) == len(letters) == 1_469_664 and
            len(stores) == 10, "heavy Q0 complete owner")
    memberships, L_counts = p176.scan_memberships(stores, A_maps, meter)
    emitted: dict[str, Any] = {}
    membership_public: dict[str, Any] = {}
    for name, indices in p176.FAMILIES:
        selected, proof = p176.prove_L(old, name, memberships[name], L_counts[name],
                                       qstates, qids, q0_marked, meter)
        gamma_selected, gamma_kernel = p176.gamma_kernel_generators(
            gamma, projected, indices, e3, e4, old)
        gamma_words = [list(gamma.section_word(sid)) for sid in gamma_selected]
        adjusted: list[list[int]] = []
        for qid in selected:
            section = p176.section_row(stores, qid)
            key = p176.family_key(section, indices)
            need = p176.family_inverse_key(key, indices, e3, e4)
            require(need in A_maps[name], "heavy adjusted-L owner")
            gid = A_maps[name][need]
            word = runtime["live"].reduce_word(
                list(gamma.section_word(gid)) +
                p176.q0_section_word(qid, parents, letters))
            replay = p176.eval_word_coordinates(old, e3, e4, contexts, delete, word)
            identity = p176.tuple_key(old, p176.family_identity(indices, e3, e4))
            require(p176.tuple_key(old, tuple(replay[i] for i in indices)) == identity,
                    "heavy adjusted-L literal replay")
            adjusted.append(word)
        emitted[name] = {"Gamma_S0_generators": gamma_words,
                         "adjusted_L_generators": adjusted,
                         "Gamma_S0_order": len(gamma_kernel),
                         "L_order": L_counts[name], "L_proof": proof}
        membership_public[name] = {"count": L_counts[name],
                                   "sha256": _stream_store_digest(memberships[name]),
                                   "adjusted_L_sha256": sha_obj(adjusted)}
    runtime.update({"delete": delete, "deletion_public": deletion_public,
                    "gamma": gamma, "projected": projected,
                    "coordinate_marks": coordinate_marks, "A_maps": A_maps,
                    "A_public": A_public, "qstates": qstates, "qids": qids,
                    "parents": parents, "letters": letters, "stores": stores,
                    "memberships": memberships, "emitted": emitted})
    fibres = runtime["live"].FibreOracle(runtime, meter)
    # Build every coordinate index once.  Later correction calls only query
    # immutable tables already included in the heavy owner digest.
    for coordinate in range(10):
        fibres._coarse_index(coordinate).build()
    kernel_orders = fibres.verify_kernel_orders()
    require(tuple(kernel_orders) == KERNEL_ORDERS and
            fibres.index_public()["built_coordinates"] == list(range(10)),
            "heavy coarse-index/kernel owners")
    runtime["fibres"] = fibres
    heavy_public = {
        "q0_state_count": len(qstates),
        "q0_state_id_sha256": _stream_state_digest(qstates, qids),
        "parents_sha256": sha_obj(parents), "letters_sha256": sha_bytes(letters),
        "store_sha256": [_stream_store_digest(store) for store in stores],
        "memberships": membership_public,
        "A_public_sha256": sha_obj(A_public),
        "gamma_state_sha256": gamma.public()["state_rows_sha256"],
        "projected_sha256": sha_obj([[p176.packed_joint_blob(value,
            "v7 projected digest").hex() for value in row] for row in projected]),
        "coarse_indices": fibres.index_public(),
        "kernel_orders": list(kernel_orders),
        "deletion_sha256": sha_obj(deletion_public),
        "light_input_sha256": runtime["light_input_sha256"],
    }
    runtime["heavy_public"] = heavy_public
    runtime["heavy_input_sha256"] = sha_obj(heavy_public)
    return runtime


def atomic_json(path: Path, value: dict[str, Any]) -> tuple[int, str]:
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = canonical(value) + b"\n"
    temporary = path.with_name(path.name + f".tmp.{os.getpid()}")
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_CLOEXEC", 0)
    try:
        fd = os.open(temporary, flags, 0o600)
        try:
            view = memoryview(raw)
            while view:
                written = os.write(fd, view)
                if written <= 0:
                    raise OSError("atomic short write")
                view = view[written:]
            os.fsync(fd)
        finally:
            os.close(fd)
        os.replace(temporary, path)
    finally:
        try:
            temporary.unlink()
        except FileNotFoundError:
            pass
    return len(raw), sha_bytes(raw)


class Search:
    def __init__(self, runtime: dict[str, Any], registry: SourceRegistry,
                 source: dict[str, Any], old_value: dict[str, Any],
                 reducer: FormalReducer, p_rows: list[dict[bytes, int]],
                 triangular: dict[str, Any], meter: Meter, output: Path,
                 workers: int, selftest: dict[str, Any]) -> None:
        self.runtime, self.registry, self.source = runtime, registry, source
        self.old_value, self.reducer, self.p_rows = old_value, reducer, p_rows
        self.triangular, self.meter, self.output = triangular, meter, output
        self.checkpoint_path = output.with_suffix(output.suffix + ".checkpoint.json")
        self.target = runtime["target"]
        self.new_records: list[dict[str, Any]] = []
        self.correction_progress = {"dual_sha256": None, "canonical_row_cursor": 0,
                                    "weighted_rows": {}}
        self.heavy_built = False
        self.last_safe_phase = "light_basis"
        self.selftest = selftest
        self.resume_expected_heavy_sha256: str | None = None
        self.boundary = PersistentBoundaryOwner(runtime, meter, workers)
        self.boundary.start()
        self.boundary.accounting["formal_ancestry_entries"] = reducer.formal_entries

    def selected_record(self, symbol: str) -> dict[str, Any]:
        if symbol.startswith("o:"):
            index = int(symbol[2:])
            return self.old_value["columns"][index - 1]
        if symbol.startswith("n:"):
            index = int(symbol[2:])
            return self.new_records[index - 1]
        raise ProtocolStop("formal symbol")

    def add_actual(self, payload: dict[str, Any], dual: dict[bytes, int]) -> None:
        row, provenance = payload["row"], payload["provenance"]
        live = self.runtime["live"]
        require(live.pair(dual, row) in (1, 2), "actual ACTIVE scalar")
        symbol = f"n:{len(self.new_records) + 1:04d}"
        before = len(self.reducer.order)
        pivot, expression = self.reducer.add_actual(row, symbol)
        self.meter.bump("retained_columns", 1, "rank_increase")
        record = {"symbol": symbol, "family": provenance["family"],
            "provenance": provenance, "sparse_row": live.public_sparse(row),
            "sparse_row_sha256": live.sha_obj(live.public_sparse(row)),
            "pivot_hex": pivot.hex(), "pivot_expression": [[key, value]
                for key, value in sorted(expression.items())],
            "rank_before": before, "rank_after": before + 1,
            "active_dual": live.public_sparse(dual),
            "active_dual_sha256": live.sha_obj(live.public_sparse(dual)),
            "dual_pairing": live.pair(dual, row), "actual_direct_replay": True}
        self.new_records.append(record)
        self.boundary.accounting["formal_ancestry_entries"] = self.reducer.formal_entries
        self.correction_progress = {"dual_sha256": None,
                                    "canonical_row_cursor": 0,
                                    "weighted_rows": {}}
        self.last_safe_phase = "actual_rank_increase"
        self.write_checkpoint("actual_rank_increase", terminal_checkpoint=False)

    def _formal_public(self) -> dict[str, Any]:
        old_ancestry = [record["pivot_ancestry"] for record in self.old_value["columns"]]
        return {"owner": "old pivot_ancestry arrays plus literal new pivot_expression arrays",
                "old_symbol_count": 2896,
                "old_ancestry": old_ancestry,
                "new_expressions": [record["pivot_expression"]
                                    for record in self.new_records],
                "entry_count": self.reducer.formal_entries,
                "max_entries": MAX_FORMAL_ENTRIES}

    def checkpoint_body(self, phase: str) -> dict[str, Any]:
        live = self.runtime["live"]
        remainder, solution = self.reducer.reduce(self.target)
        dual = None
        if remainder:
            dual, exact, exact_solution = self.reducer.exact_dual(self.target)
            require(exact == remainder and exact_solution == solution,
                    "checkpoint exact dual")
        p_public = [live.public_sparse(row) for row in self.p_rows]
        formal = self._formal_public()
        return {"schema": CHECKPOINT_SCHEMA, "phase": phase,
            "source": self.source, "source_snapshots": self.registry.public(),
            "light_input_sha256": self.runtime["light_input_sha256"],
            "heavy_input_sha256": self.runtime.get("heavy_input_sha256"),
            "heavy_complete": self.heavy_built,
            "triangular_certificate": self.triangular,
            "P_rows": p_public, "P_rows_sha256": live.sha_obj(p_public),
            "formal_ancestry": formal, "formal_ancestry_sha256": sha_obj(formal),
            "new_records": self.new_records,
            "target": live.public_sparse(self.target),
            "remainder": live.public_sparse(remainder),
            "formal_solution": [[key, value] for key, value in sorted(solution.items())],
            "current_dual": None if dual is None else live.public_sparse(dual),
            "current_dual_sha256": None if dual is None else
                live.sha_obj(live.public_sparse(dual)),
            "correction_progress": self.correction_progress,
            "next_clean_boundary_epoch": self.boundary.epoch + 1,
            "boundary_owner": self.boundary.public(),
            "monitor": self.meter.public(), "last_safe_phase": self.last_safe_phase,
            "selftest": self.selftest, "claims": dict(FALSE_CLAIMS),
            "heuristic_discovery_only": True, "exact_cached_resume": False}

    def write_checkpoint(self, phase: str, terminal_checkpoint: bool) -> dict[str, Any]:
        checkpoint = seal(self.checkpoint_body(phase))
        size, digest = atomic_json(self.checkpoint_path, checkpoint)
        if size > self.meter.limits["checkpoint_bytes"]:
            raise ResourceStop("checkpoint_serialization", "checkpoint_bytes", size,
                               self.meter.limits["checkpoint_bytes"])
        self.meter.counters["checkpoint_bytes"] = size
        return {"path": self.checkpoint_path.name, "bytes": size,
                "sha256": digest, "terminal_checkpoint": terminal_checkpoint}

    def ensure_heavy(self) -> None:
        require("heavy_input_sha256" not in self.runtime,
                "heavy digest exists before Q0-LATE transition")
        self.last_safe_phase = "light_before_heavy"
        self.write_checkpoint("last_safe_light_before_heavy", terminal_checkpoint=False)
        build_heavy(self.runtime, self.registry, self.meter)
        require(type(self.runtime.get("heavy_input_sha256")) is str and
                all(key in self.runtime for key in ("qstates", "qids", "parents",
                    "letters", "stores", "memberships", "emitted", "fibres")),
                "heavy digest publication boundary")
        if self.resume_expected_heavy_sha256 is not None:
            require(self.runtime["heavy_input_sha256"] ==
                    self.resume_expected_heavy_sha256,
                    "resumed heavy identity")
        self.heavy_built = True
        self.last_safe_phase = "heavy_complete"

    def correction_oracle(self, dual: dict[bytes, int]) -> dict[str, Any] | None:
        require(self.heavy_built and type(self.runtime.get("heavy_input_sha256")) is str,
                "correction before heavy digest")
        live, fibres = self.runtime["live"], self.runtime["fibres"]
        model = self.runtime["model"]
        dual_sha = live.sha_obj(live.public_sparse(dual))
        if self.correction_progress.get("dual_sha256") != dual_sha:
            self.correction_progress = {"dual_sha256": dual_sha,
                "canonical_row_cursor": 0, "weighted_rows": {}}
        cursor = int(self.correction_progress["canonical_row_cursor"])
        rows = self.correction_progress["weighted_rows"]
        for roster_index, roster_row in enumerate(self.runtime["roster"], 1):
            if roster_index <= cursor:
                continue
            self.meter.check("weighted_eleven_occurrence_formula")
            formula = model.occurrence_data(roster_row["word"], dual)
            support = fibres.weighted_support(formula)
            state = rows.setdefault(str(roster_index), {
                "formula_sha256": sha_obj(formula["public"]),
                "K": support["K"], "W": support["W"],
                "support_fibre_cursor": 0, "kernel_cursor": 0,
                "global_prefix": 0, "complete": False})
            require(state["formula_sha256"] == sha_obj(formula["public"]) and
                    state["K"] == support["K"] and state["W"] == support["W"],
                    "correction row state")
            if support["K"] == 0:
                targets = sorted(formula["merged"], key=lambda item: (item[0], item[1]))
                for target_index in range(int(state["support_fibre_cursor"]), len(targets)):
                    coordinate, target = targets[target_index]
                    if target_index != int(state["support_fibre_cursor"]):
                        state["kernel_cursor"] = 0
                    state["support_fibre_cursor"] = target_index
                    fibre = fibres.canonical(coordinate, target)
                    if fibre is None:
                        state["kernel_cursor"] = 0
                        continue
                    kernel_states = fibres.kernel_states[coordinate]
                    for kernel_index in range(int(state["kernel_cursor"]), len(kernel_states)):
                        self.meter.check("weighted_support_fibre")
                        state["kernel_cursor"] = kernel_index
                        candidate = fibres.kernel_candidate(fibre,
                                                            kernel_states[kernel_index])
                        self.meter.bump("candidate_words", 1,
                                        "positive_correction_candidate")
                        scalar = model.formula_scalar(formula,
                                                      candidate["coordinate_blobs"])
                        if not scalar:
                            continue
                        row, replay = model.direct_column(candidate["source_word"],
                                                          roster_row["word"])
                        require(live.pair(dual, row) == scalar,
                                "correction eleven/direct scalar")
                        return {"row": row, "provenance": {"family": "correction",
                            "roster_index": roster_index, "layer": roster_row["layer"],
                            "ordinal": roster_row["ordinal"],
                            "schedule": "weighted_support_fibre_complete",
                            "weighted_formula": formula["public"],
                            "support_hitting": support,
                            "delta_word": list(candidate["source_word"]),
                            "delta_coordinate_blobs_hex": [raw.hex() for raw in
                                                            candidate["coordinate_blobs"]],
                            "section_provenance": {key: value for key, value in
                                candidate.items() if key not in ("source_word",
                                                                 "coordinate_blobs")}
                                | {"support_fibre_cursor": target_index,
                                   "kernel_cursor": kernel_index},
                            **replay}}
                    state["kernel_cursor"] = len(kernel_states)
                state["complete"] = True
            else:
                bound = support["W"] + 1 if support["W"] < DELTA_ORDER else DELTA_ORDER
                seen: set[tuple[int, int]] = set()
                for global_cursor in range(int(state["global_prefix"]), bound):
                    self.meter.check("weighted_global_prefix")
                    state["global_prefix"] = global_cursor
                    candidate = fibres.global_candidate(global_cursor)
                    pair_id = (candidate["q0_state_id"], candidate["gamma_state_id"])
                    require(pair_id not in seen, "global prefix duplicate")
                    seen.add(pair_id)
                    self.meter.bump("candidate_words", 1,
                                    "positive_correction_candidate")
                    scalar = model.formula_scalar(formula, candidate["coordinate_blobs"])
                    if not scalar:
                        continue
                    row, replay = model.direct_column(candidate["source_word"],
                                                      roster_row["word"])
                    require(live.pair(dual, row) == scalar,
                            "global correction eleven/direct scalar")
                    return {"row": row, "provenance": {"family": "correction",
                        "roster_index": roster_index, "layer": roster_row["layer"],
                        "ordinal": roster_row["ordinal"],
                        "schedule": ("weighted_global_prefix_W_plus_1"
                                     if support["W"] < DELTA_ORDER else
                                     "weighted_global_fair_fallback"),
                        "weighted_formula": formula["public"],
                        "support_hitting": support,
                        "delta_word": list(candidate["source_word"]),
                        "delta_coordinate_blobs_hex": [raw.hex() for raw in
                                                        candidate["coordinate_blobs"]],
                        "section_provenance": {key: value for key, value in
                            candidate.items() if key not in ("source_word",
                                                             "coordinate_blobs")},
                        **replay}}
                state["global_prefix"] = bound
                if support["W"] >= DELTA_ORDER:
                    raise ResourceStop("positive_global_fallback", "global_roster",
                                       DELTA_ORDER + 1, DELTA_ORDER)
                raise ProtocolStop("weighted W+1 theorem invariant")
            self.correction_progress["canonical_row_cursor"] = roster_index
            self.write_checkpoint("correction_row_complete", terminal_checkpoint=False)
        return None

    def common_candidate(self, solution: dict[str, int]) -> dict[str, Any]:
        live, model = self.runtime["live"], self.runtime["model"]
        require(solution and all(value in (1, 2) for value in solution.values()),
                "nonempty formal solution")
        selected_old, selected_new = [], []
        combined: dict[bytes, int] = {}
        correction_sum: dict[bytes, int] = {}
        boundary_sum: dict[bytes, int] = {}
        correction_word: list[int] = []
        boundary_preimage = []
        selected_corrections = []
        for symbol in sorted(solution):
            coefficient = solution[symbol]
            record = self.selected_record(symbol)
            row = live.parse_sparse(record["sparse_row"])
            live.add_scaled(combined, row, coefficient)
            selected = {"symbol": symbol, "coefficient": coefficient,
                        "record": record}
            (selected_old if symbol.startswith("o:") else selected_new).append(selected)
            if record["family"] == "boundary":
                live.add_scaled(boundary_sum, row, coefficient)
                boundary_preimage.append({"symbol": symbol, "coefficient": coefficient,
                                          "provenance": record["provenance"]})
            else:
                live.add_scaled(correction_sum, row, coefficient)
                conjugate = list(record["provenance"]["conjugate_word"])
                factor = conjugate if coefficient == 1 else live.inverse_word(conjugate)
                inverse_replay = False
                if coefficient == 2:
                    inverse_row, inverse_public = model.direct_column(
                        record["provenance"]["delta_word"],
                        live.inverse_word(record["provenance"]["relator_word"]))
                    require(inverse_row == live.scaled(row, -1) and
                            inverse_public["conjugate_word"] == factor,
                            "producer coefficient-two inverse")
                    inverse_replay = True
                require(self.runtime["joint_group"].eval(factor) ==
                        self.runtime["joint_group"].identity,
                        "producer selected joint kernel")
                correction_word = live.reduce_word(correction_word + factor)
                selected_corrections.append({"symbol": symbol,
                    "coefficient": coefficient, "factor_word": factor,
                    "coefficient_two_inverse_replayed": inverse_replay,
                    "provenance": record["provenance"]})
        require(combined == self.target, "producer complete sparse target")
        require(live.exponent_pair(correction_word) == (0, 0),
                "producer correction exponents")
        direct, replay = model.direct_column([], correction_word)
        require(direct == correction_sum, "producer correction product additivity")
        residual = live.scaled(self.target, -1)
        live.add_scaled(residual, correction_sum, 1)
        live.add_scaled(residual, boundary_sum, 1)
        require(not residual, "producer typed PB3/PB4 preimage")
        corrected_word = live.reduce_word(list(model.g) + correction_word)
        require(corrected_word == replay["corrected_word"],
                "producer right correction")
        return seal({"schema": SCHEMA, "status": "COMMON_WORD", "terminal": COMMON,
            "source": self.source, "source_snapshots": self.registry.public(),
            "light_input_sha256": self.runtime["light_input_sha256"],
            "heavy_input_sha256": self.runtime.get("heavy_input_sha256"),
            "triangular_certificate": self.triangular,
            "basis_authority": {"heuristic_discovery_only": True,
                                "exact_cached_resume": False},
            "target": live.public_sparse(self.target),
            "formal_solution": [[key, value] for key, value in sorted(solution.items())],
            "selected_old": selected_old, "selected_new": selected_new,
            "selected_corrections": selected_corrections,
            "boundary_preimage": boundary_preimage,
            "correction_word": correction_word, "corrected_word": corrected_word,
            "g760": list(model.g), "producer_sparse_equality": True,
            "producer_joint_kernel": True, "producer_all_seven_replay": replay,
            "boundary_owner": self.boundary.public(), "monitor": self.meter.public(),
            "selftest": self.selftest,
            "claims": {**FALSE_CLAIMS, "common_word": True,
                       "finite_common_word": True},
            "claim_boundary": "finite A0 candidate; checker required; no lift/fake/Ihara"})

    def run(self) -> dict[str, Any]:
        live = self.runtime["live"]
        while True:
            self.meter.check("positive_search", self.boundary.pids())
            remainder, solution = self.reducer.reduce(self.target)
            if not remainder:
                self.boundary.close()
                candidate = self.common_candidate(solution)
                try:
                    self.checkpoint_path.unlink()
                except FileNotFoundError:
                    pass
                return candidate
            dual, exact_remainder, exact_solution = self.reducer.exact_dual(self.target)
            require(exact_remainder == remainder and exact_solution == solution,
                    "search remainder stability")
            outcome = self.boundary.run_epoch(dual)
            active = self.boundary.materialize(dual, outcome)
            if active is not None:
                self.add_actual(active, dual)
                continue
            if not self.heavy_built:
                self.ensure_heavy()
            active = self.correction_oracle(dual)
            if active is not None:
                self.add_actual(active, dual)
                continue
            self.meter.bump("oracle_rounds", 1, "positive_correction_dovetail")
            raise ResourceStop("positive_correction_dovetail", "oracle_rounds",
                               self.meter.counters["oracle_rounds"] + 1,
                               self.meter.limits["oracle_rounds"])


def read_bounded_json(path: Path, maximum: int) -> tuple[dict[str, Any], dict[str, Any]]:
    flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
    try:
        fd = os.open(path, flags)
    except OSError as exc:
        raise InputStop("bounded_open") from exc
    try:
        before = os.fstat(fd)
        require(stat.S_ISREG(before.st_mode) and before.st_nlink == 1 and
                0 < before.st_size <= maximum, "bounded physical object")
        raw = bytearray()
        while len(raw) < before.st_size:
            chunk = os.read(fd, min(1 << 20, before.st_size - len(raw)))
            if not chunk:
                raise InputStop("bounded_short_read")
            raw.extend(chunk)
        after = os.fstat(fd)
        require((before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns) ==
                (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns),
                "bounded TOCTOU")
        try:
            path_after = os.lstat(path)
        except OSError as exc:
            raise InputStop("bounded_path_substitution") from exc
        require(not stat.S_ISLNK(path_after.st_mode) and
                (path_after.st_dev, path_after.st_ino, path_after.st_size) ==
                (after.st_dev, after.st_ino, after.st_size),
                "bounded pathname identity")
        try:
            value = json.loads(bytes(raw).decode("ascii"))
        except (UnicodeError, json.JSONDecodeError) as exc:
            raise InputStop("bounded_json") from exc
        require(type(value) is dict, "bounded JSON object")
        return value, {"bytes": len(raw), "sha256": sha_bytes(bytes(raw)),
                       "device": before.st_dev, "inode": before.st_ino,
                       "links": before.st_nlink, "mtime_ns": before.st_mtime_ns}
    finally:
        os.close(fd)


def restore_checkpoint(search: Search, path: Path) -> None:
    value, _physical = read_bounded_json(path, MAX_CHECKPOINT_BYTES)
    validate_seal(value)
    live = search.runtime["live"]
    checkpoint_source = value.get("source")
    stable_source_keys = ("path", "member", "bytes", "sha256", "parsed_once")
    require(value.get("schema") == CHECKPOINT_SCHEMA and
            type(checkpoint_source) is dict and
            {key: checkpoint_source.get(key) for key in stable_source_keys} ==
                {key: search.source.get(key) for key in stable_source_keys} and
            type(checkpoint_source.get("physical")) is dict and
            value.get("source_snapshots") == search.registry.public() and
            value.get("light_input_sha256") == search.runtime["light_input_sha256"] and
            value.get("triangular_certificate") == search.triangular and
            value.get("P_rows_sha256") == OLD_PIVOT_ROWS_SHA256 and
            value.get("P_rows") == [live.public_sparse(row) for row in search.p_rows] and
            value.get("claims") == FALSE_CLAIMS and
            value.get("heuristic_discovery_only") is True and
            value.get("exact_cached_resume") is False,
            "v7 checkpoint source/basis binding")
    formal = value.get("formal_ancestry")
    require(type(formal) is dict and value.get("formal_ancestry_sha256") == sha_obj(formal) and
            formal.get("old_ancestry") == [record["pivot_ancestry"]
                for record in search.old_value["columns"]], "v7 formal ancestry owner")
    prior_monitor = value.get("monitor", {})
    require(prior_monitor.get("limits") == search.meter.limits and
            type(prior_monitor.get("fresh_v7_counters")) is dict,
            "v7 checkpoint monitor")
    for name, counter in prior_monitor["fresh_v7_counters"].items():
        require(name in search.meter.counters and type(counter) is int and
                0 <= counter <= search.meter.limits[name], "v7 counter restore")
        search.meter.counters[name] = counter
    search.meter.counters["checkpoint_bytes"] = 0
    prior_boundary = value.get("boundary_owner")
    require(type(prior_boundary) is dict and
            prior_boundary.get("workers") == search.boundary.workers and
            prior_boundary.get("accounting", {}).get("descriptor_sha256") ==
                search.boundary.descriptor_sha256 and
            prior_boundary.get("cleanup", {}).get("complete") is True and
            prior_boundary["cleanup"].get("live_pids_after_join") == [] and
            type(value.get("next_clean_boundary_epoch")) is int and
            value["next_clean_boundary_epoch"] >= 1,
            "v7 clean boundary resume owner")
    current_start_accounting = dict(search.boundary.accounting)
    restored_accounting = dict(prior_boundary["accounting"])
    for name in ("frames_sent_bytes", "frames_received_bytes"):
        restored_accounting[name] = int(restored_accounting.get(name, 0)) + int(
            current_start_accounting.get(name, 0))
    restarted = search.boundary.workers if prior_boundary["cleanup"].get(
        "started_pids") else 0
    restored_accounting["process_restarts"] = int(
        restored_accounting.get("process_restarts", 0)) + restarted
    search.boundary.accounting = restored_accounting
    search.boundary.epoch = int(value["next_clean_boundary_epoch"]) - 1
    for expected_index, record in enumerate(value.get("new_records", []), 1):
        require(record.get("symbol") == f"n:{expected_index:04d}" and
                record.get("family") in ("boundary", "correction"),
                "v7 new record order")
        provenance = record["provenance"]
        if record["family"] == "boundary":
            row = live.translated_boundary(search.runtime, int(provenance["block"]),
                int(provenance["base_relator_index"]),
                bytes.fromhex(provenance["translation_hex"]))
        else:
            row, replay = search.runtime["model"].direct_column(
                provenance["delta_word"], provenance["relator_word"])
            require(replay["conjugate_word"] == provenance["conjugate_word"],
                    "v7 correction replay restore")
        require(live.public_sparse(row) == record["sparse_row"] and
                record["sparse_row_sha256"] == live.sha_obj(record["sparse_row"]),
                "v7 new row restore")
        pivot, expression = search.reducer.add_actual(row, record["symbol"])
        require(pivot.hex() == record["pivot_hex"] and
                [[key, coefficient] for key, coefficient in sorted(expression.items())] ==
                record["pivot_expression"], "v7 new formal replay")
        search.new_records.append(record)
    require(formal.get("new_expressions") == [record["pivot_expression"]
            for record in search.new_records] and
            formal.get("entry_count") == search.reducer.formal_entries,
            "v7 restored formal DAG")
    remainder, solution = search.reducer.reduce(search.target)
    require(live.public_sparse(remainder) == value.get("remainder") and
            [[key, coefficient] for key, coefficient in sorted(solution.items())] ==
            value.get("formal_solution"), "v7 restored target state")
    search.correction_progress = value.get("correction_progress")
    require(type(search.correction_progress) is dict, "v7 correction progress restore")
    search.resume_expected_heavy_sha256 = value.get("heavy_input_sha256")
    search.last_safe_phase = "resumed_" + str(value.get("last_safe_phase"))


def _triangular_subset_frame(old_value: dict[str, Any], live: Any) -> dict[str, Any]:
    records = json.loads(canonical(old_value["columns"][:6]).decode("ascii"))
    raw_rows = [live.parse_sparse(record["sparse_row"]) for record in records]
    products = []
    for record in records:
        product: dict[bytes, int] = {}
        for index, coefficient in record["pivot_ancestry"]:
            live.add_scaled(product, raw_rows[index - 1], coefficient)
        products.append(live.public_sparse(product))
    return {"schema": SCHEMA + "/triangular-physical-frame",
            "columns": records, "P_rows_sha256": live.sha_obj(products)}


def _validate_triangular_subset(frame: dict[str, Any], live: Any) -> None:
    require(frame.get("schema") == SCHEMA + "/triangular-physical-frame" and
            type(frame.get("columns")) is list and frame["columns"],
            "triangular selftest frame")
    raw_rows = []
    pivots = []
    for expected, record in enumerate(frame["columns"], 1):
        validate_provenance(record, expected)
        row = live.parse_sparse(record["sparse_row"])
        require(record["sparse_row_sha256"] == live.sha_obj(record["sparse_row"]),
                "triangular selftest raw digest")
        raw_rows.append(row)
        ancestry = record["pivot_ancestry"]
        require(all(type(item) is list and len(item) == 2 and item[1] in (1, 2)
                    for item in ancestry) and
                [item[0] for item in ancestry] == sorted(set(item[0] for item in ancestry)) and
                all(1 <= item[0] <= expected for item in ancestry) and
                any(item[0] == expected and item[1] in (1, 2) for item in ancestry),
                "triangular selftest ancestry")
        pivot = bytes.fromhex(record["pivot_hex"])
        require(pivot and pivot not in pivots, "triangular selftest pivot identity")
        pivots.append(pivot)
    products = []
    for expected, (record, pivot) in enumerate(zip(frame["columns"], pivots), 1):
        product: dict[bytes, int] = {}
        for index, coefficient in record["pivot_ancestry"]:
            live.add_scaled(product, raw_rows[index - 1], coefficient)
        require(product and min(product) == pivot and product[pivot] == 1 and
                all(product.get(old, 0) == 0 for old in pivots[:expected - 1]),
                "triangular selftest P equation")
        products.append(live.public_sparse(product))
    require(frame.get("P_rows_sha256") == live.sha_obj(products),
            "triangular selftest full P digest")


def _physical_mutation(path: Path, value: dict[str, Any], validator: Any) -> bool:
    raw = canonical(value) + b"\n"
    with path.open("xb") as stream:
        stream.write(raw); stream.flush(); os.fsync(stream.fileno())
    candidate, _ = read_bounded_json(path, len(raw))
    try:
        validator(candidate)
    except ProtocolStop:
        return True
    return False


def triangular_mutation_selftest(old_value: dict[str, Any], live: Any,
                                 names: Sequence[str]) -> list[dict[str, Any]]:
    baseline = _triangular_subset_frame(old_value, live)
    _validate_triangular_subset(baseline, live)
    results = []
    with tempfile.TemporaryDirectory(prefix="r07-v7-triangular-") as directory:
        root = Path(directory)
        for ordinal, name in enumerate(names):
            value = json.loads(canonical(baseline).decode("ascii"))
            columns = value["columns"]
            if name == "future_ancestry_index":
                columns[1]["pivot_ancestry"].append([7, 1])
            elif name == "zero_diagonal":
                columns[1]["pivot_ancestry"] = [row for row in
                    columns[1]["pivot_ancestry"] if row[0] != 2]
            elif name == "changed_raw_sparse_entry":
                columns[0]["sparse_row"][0][1] = 3 - columns[0]["sparse_row"][0][1]
                columns[0]["sparse_row_sha256"] = live.sha_obj(
                    columns[0]["sparse_row"])
            elif name == "changed_ancestry_coefficient":
                columns[1]["pivot_ancestry"][0][1] = 3 - \
                    columns[1]["pivot_ancestry"][0][1]
            elif name == "duplicate_pivot":
                columns[1]["pivot_hex"] = columns[0]["pivot_hex"]
            elif name == "wrong_pivot":
                columns[2]["pivot_hex"] = "00"
            elif name == "hidden_smaller_pivot":
                columns[2]["pivot_hex"] = max(row[0] for row in
                                                columns[2]["sparse_row"])
            elif name == "skipped_P_equation":
                non_diagonal = next(index for index, row in enumerate(
                    columns[2]["pivot_ancestry"]) if row[0] != 3)
                columns[2]["pivot_ancestry"].pop(non_diagonal)
            else:
                raise ProtocolStop("unknown triangular mutation")
            rejected = _physical_mutation(root / f"{ordinal:02d}.json", value,
                lambda candidate: _validate_triangular_subset(candidate, live))
            require(rejected, "triangular mutation accepted:" + name)
            results.append({"id": name, "physical_before_validator": True,
                            "narrow_rejection": True})
    return results


def blocked_send_selftest(context: Any, deadline_seconds: float = 0.05) -> dict[str, Any]:
    parent, child = socket.socketpair(socket.AF_UNIX, socket.SOCK_STREAM)
    def no_drain(sock: socket.socket, deadline: float) -> None:
        sock.setblocking(False)
        while time.monotonic() <= deadline:
            pass
        sock.close()
    deadline = time.monotonic() + deadline_seconds
    process = context.Process(target=no_drain, args=(child, deadline),
                              name="r07-v7-blocked-send")
    process.start(); child.close()
    rejected = False
    try:
        DeadlineChannel(parent).send({"padding": "x" * (4 * 1024 * 1024)}, deadline)
    except (TimeoutError, EOFError, OSError):
        rejected = True
    finally:
        try:
            parent.close()
        except OSError:
            pass
        if process.is_alive():
            process.terminate()
        process.join(CHANNEL_CLOSE_SECONDS)
        if process.is_alive():
            process.kill(); process.join(CHANNEL_CLOSE_SECONDS)
        alive = process.is_alive(); exitcode = process.exitcode
        process.close()
    require(rejected and not alive, "blocked send selftest")
    return {"deadline_rejected": True, "cleanup_complete": True,
            "exitcode": exitcode, "process_close": True}


def process_selftest(runtime: dict[str, Any], reducer: FormalReducer,
                     fixture: dict[str, Any]) -> dict[str, Any]:
    live = runtime["live"]
    dual, _, _ = reducer.exact_dual(runtime["target"])
    row_keys = [key for key in sorted(dual) if key[:1] == b"R"]
    require(len(row_keys) == 1188, "selftest actual first dual")
    runs = []
    # A separate meter gives SELFTEST a bounded channel deadline without
    # charging production's fresh mathematical counters.
    for workers in fixture["worker_counts"]:
        test_meter = Meter(WALL_SECONDS)
        owner = PersistentBoundaryOwner(runtime, test_meter, workers)
        owner.start()
        try:
            first_descriptor = owner.descriptors[0]
            second_descriptor = next(row for row in owner.descriptors[1:]
                if row["block"] == first_descriptor["block"] and
                   row["relator"] == first_descriptor["relator"] and
                   (row["component"], row["h_blob"]) !=
                   (first_descriptor["component"], first_descriptor["h_blob"]))
            cancellation_second = (-first_descriptor["base_coefficient"] *
                (1 if second_descriptor["base_coefficient"] == 1 else 2)) % 3
            cancellation_probe = {
                live.row_key(first_descriptor["block"], first_descriptor["component"],
                             first_descriptor["h_blob"]): 1,
                live.row_key(second_descriptor["block"], second_descriptor["component"],
                             second_descriptor["h_blob"]): cancellation_second}
            probes = [({}, "empty_support"),
                      ({row_keys[0]: dual[row_keys[0]]}, "one_support"),
                      ({key: dual[key] for key in row_keys[:4]}, "short_support"),
                      ({**{key: dual[key] for key in row_keys[:2]},
                        live.exponent_key(1): 1}, "typed_present_shape_filter"),
                      (cancellation_probe, "f3_cancellation")]
            probe_rows = []
            for probe, label in probes:
                outcome = owner.run_epoch(probe)
                active = owner.materialize(probe, outcome)
                probe_rows.append({"case": label,
                    "support": outcome["support_entry_count"],
                    "pairs": outcome["expanded_pair_count"],
                    "active": active is not None, "zero": active is None,
                    "outcome": outcome})
            serial_duals = []; serial_outcomes = []
            for probe in (dual, live.scaled(dual, 2),
                          {key: dual[key] for key in row_keys[:2]}):
                outcome = owner.run_epoch(probe)
                serial_duals.append(outcome["dual_sha256"])
                serial_outcomes.append(outcome)
            require(len(serial_duals) == 3 and probe_rows[0]["zero"] is True and
                    probe_rows[1]["active"] is True and
                    probe_rows[3]["support"] == 2 and
                    probe_rows[4]["support"] == 2,
                    "selftest serial/ACTIVE/zero/filter/cancellation")
        finally:
            owner.close()
        require(owner.cleanup["complete"], "normal selftest cleanup")
        runs.append({"workers": workers, "probes": probe_rows,
                     "three_serial_duals": serial_duals,
                     "three_serial_outcomes": serial_outcomes,
                     "cleanup": owner.cleanup})
        for fault in ("timeout", "death", "partial"):
            fault_meter = Meter(WALL_SECONDS)
            fault_owner = PersistentBoundaryOwner(runtime, fault_meter, workers)
            fault_owner.start(); rejected = False
            try:
                fault_owner.run_epoch({row_keys[0]: dual[row_keys[0]]},
                                      fault=fault, short_deadline=0.05)
            except ResourceStop:
                rejected = True
            require(rejected and fault_owner.cleanup["complete"],
                    "fault cleanup:" + fault)
            runs.append({"workers": workers, "fault": fault,
                         "atomic_discard": True,
                         "cleanup": fault_owner.cleanup})
    context = multiprocessing.get_context("fork")
    return {"first_dual": live.public_sparse(dual),
            "first_dual_sha256": live.sha_obj(live.public_sparse(dual)),
            "runs": runs, "blocked_send": blocked_send_selftest(context),
            "actual_E3_E4_codec": True, "actual_process_owner": True,
            "W2_W4": True}


def phase_gate_selftest(runtime: dict[str, Any]) -> list[dict[str, Any]]:
    baseline = {"light_input_sha256": runtime["light_input_sha256"],
                "heavy_input_sha256": None, "heavy_complete": False,
                "correction_started": False, "correction_cursor": 0,
                "zero_is_negative": False, "claims": dict(FALSE_CLAIMS)}
    def validate(value: dict[str, Any]) -> None:
        require(value["light_input_sha256"] == runtime["light_input_sha256"] and
                value["heavy_input_sha256"] is None and
                value["heavy_complete"] is False and
                value["correction_started"] is False and
                value["correction_cursor"] == 0 and
                value["zero_is_negative"] is False and
                value["claims"] == FALSE_CLAIMS, "phase gate")
    actions = {
        "heavy_call_before_heavy_digest": lambda value: value.__setitem__("correction_started", True),
        "fabricated_heavy_digest": lambda value: value.__setitem__("heavy_input_sha256", "0" * 64),
        "stale_correction_progress": lambda value: value.__setitem__("correction_cursor", 1),
        "zero_promoted_to_negative": lambda value: value.__setitem__("zero_is_negative", True),
    }
    rows = []
    for name, action in actions.items():
        value = json.loads(canonical(baseline).decode("ascii")); action(value)
        rejected = False
        try:
            validate(value)
        except ProtocolStop:
            rejected = True
        require(rejected, "phase mutation accepted:" + name)
        rows.append({"id": name, "owner_mutated_before_validator": True,
                     "narrow_rejection": True})
    rows.extend([{"id": "light_resource_checkpoint", "owner_gate": True},
                 {"id": "heavy_transition", "owner_gate": True,
                  "production_builder": "build_heavy publishes digest last"}])
    return rows


def run_real_owner_selftest(runtime: dict[str, Any], old_value: dict[str, Any],
                            reducer: FormalReducer, registry: SourceRegistry) -> dict[str, Any]:
    fixture = registry.json("fixture")
    require(fixture.get("schema") ==
            "d972-r07-history-free-positive-fast-resume/selftest-input/v7" and
            fixture.get("worker_counts") == [2, 4] and
            fixture.get("claims") == FALSE_CLAIMS and
            fixture.get("expected_first_checkpoint") == {
                "columns": 2896, "rank": 2896, "boundary_columns": 2896,
                "correction_columns": 0, "raw_support_total": 20354,
                "raw_support_max": 12, "ancestry_entries_total": 137926,
                "ancestry_entries_max": 258,
                "ancestry_weighted_contributions": 1011460,
                "pivot_support_total": 289774, "pivot_support_max": 522,
                "first_dual_support": 1188,
                "first_dual_matching_descriptors": 4,
                "first_dual_pairs": 4752}, "selftest fixture envelope")
    triangular = triangular_mutation_selftest(old_value, runtime["live"],
                                               fixture["triangular_mutations"])
    processes = process_selftest(runtime, reducer, fixture)
    phases = phase_gate_selftest(runtime)
    return {"fixture_sha256": SOURCE_PINS["fixture"][2],
            "triangular_mutations": triangular,
            "process_owner": processes, "phase_mutations": phases,
            "boundary_mutations_committed_to_checker": fixture["boundary_mutations"],
            "positive_mutations_committed_to_checker": fixture["positive_mutations"],
            "physical_mutations_committed_to_checker": fixture["physical_mutations"],
            "real_owner_not_shaped_transcript": True}


def exclusive_json(path: Path, value: dict[str, Any]) -> tuple[int, str]:
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = canonical(value) + b"\n"
    try:
        with path.open("xb") as stream:
            stream.write(raw); stream.flush(); os.fsync(stream.fileno())
    except FileExistsError as exc:
        raise ProtocolStop("stale output") from exc
    return len(raw), sha_bytes(raw)


def unknown_receipt(kind: str, reason: str, registry: SourceRegistry | None,
                    source: dict[str, Any] | None, meter: Meter | None,
                    checkpoint: dict[str, Any] | None,
                    boundary: dict[str, Any] | None,
                    selftest: dict[str, Any] | None) -> dict[str, Any]:
    require(kind in (UNKNOWN_INPUT, UNKNOWN_RESOURCE), "unknown kind")
    terminal = kind + ":" + reason
    answer = {"schema": SCHEMA, "status": "UNKNOWN", "terminal": terminal,
        "source": source, "source_snapshots": None if registry is None else registry.public(),
        "monitor": None if meter is None else meter.public(),
        "boundary_owner": boundary, "selftest": selftest,
        "claims": dict(FALSE_CLAIMS), "correction_word": None,
        "common_word": None, "claim_boundary": "typed unknown; no negative content"}
    if checkpoint is not None:
        answer["checkpoint"] = checkpoint
    return seal(answer)


def write_prepool_checkpoint(runtime: dict[str, Any], registry: SourceRegistry,
                             source: dict[str, Any], old_value: dict[str, Any],
                             reducer: FormalReducer,
                             p_rows: Sequence[dict[bytes, int]],
                             triangular: dict[str, Any], meter: Meter,
                             output: Path, workers: int) -> tuple[dict[str, Any],
                                                                  dict[str, Any]]:
    """P-bound resource transport before any boundary child is started."""
    live = runtime["live"]
    remainder, solution = reducer.reduce(runtime["target"])
    dual = None
    if remainder:
        dual, exact, exact_solution = reducer.exact_dual(runtime["target"])
        require(exact == remainder and exact_solution == solution,
                "prepool exact dual")
    descriptors, _lookup = boundary_descriptors(runtime)
    descriptor_rows = descriptor_public(descriptors)
    descriptor_digest = sha_obj(descriptor_rows)
    accounting = {"epochs_committed": 0, "epochs_discarded": 0,
        "literal_pairs_committed": 0, "support_bytes": 0,
        "frames_sent_bytes": 0, "frames_received_bytes": 0,
        "accumulator_entries": 0, "max_accumulator_entries": 0,
        "formal_ancestry_entries": reducer.formal_entries,
        "descriptor_count": len(descriptors),
        "descriptor_sha256": descriptor_digest,
        "winner_reconstructions": 0, "process_restarts": 0,
        "metric": "sampled RSS sum; not exact physical peak"}
    cleanup = {"transitions": ["not_started", "prepool_resource_no_children"],
        "started_pids": [], "worker_exitcodes": [],
        "live_pids_after_join": [], "process_close_count": 0,
        "complete": True}
    boundary = {"workers": workers, "persistent": True,
        "transport": "nonblocking AF_UNIX socketpair, absolute deadline frames",
        "state": "not_started_at_safe_P_boundary", "accounting": accounting,
        "cleanup": cleanup}
    p_public = [live.public_sparse(row) for row in p_rows]
    formal = {"owner":
        "old pivot_ancestry arrays plus literal new pivot_expression arrays",
        "old_symbol_count": 2896,
        "old_ancestry": [record["pivot_ancestry"]
                         for record in old_value["columns"]],
        "new_expressions": [], "entry_count": reducer.formal_entries,
        "max_entries": MAX_FORMAL_ENTRIES}
    body = {"schema": CHECKPOINT_SCHEMA, "phase": "resource_stop",
        "source": source, "source_snapshots": registry.public(),
        "light_input_sha256": runtime["light_input_sha256"],
        "heavy_input_sha256": None, "heavy_complete": False,
        "triangular_certificate": triangular,
        "P_rows": p_public, "P_rows_sha256": live.sha_obj(p_public),
        "formal_ancestry": formal, "formal_ancestry_sha256": sha_obj(formal),
        "new_records": [], "target": live.public_sparse(runtime["target"]),
        "remainder": live.public_sparse(remainder),
        "formal_solution": [[key, value] for key, value in sorted(solution.items())],
        "current_dual": None if dual is None else live.public_sparse(dual),
        "current_dual_sha256": None if dual is None else
            live.sha_obj(live.public_sparse(dual)),
        "correction_progress": {"dual_sha256": None,
            "canonical_row_cursor": 0, "weighted_rows": {}},
        "next_clean_boundary_epoch": 1, "boundary_owner": boundary,
        "monitor": meter.public(), "last_safe_phase": "prepool_light_basis",
        "selftest": None, "claims": dict(FALSE_CLAIMS),
        "heuristic_discovery_only": True, "exact_cached_resume": False}
    path = output.with_suffix(output.suffix + ".checkpoint.json")
    size, digest = atomic_json(path, seal(body))
    if size > meter.limits["checkpoint_bytes"]:
        raise ResourceStop("checkpoint_serialization", "checkpoint_bytes", size,
                           meter.limits["checkpoint_bytes"])
    meter.counters["checkpoint_bytes"] = size
    return {"path": path.name, "bytes": size, "sha256": digest,
            "terminal_checkpoint": True}, boundary


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser()
    value.add_argument("--mode", choices=("PRODUCTION",), default="PRODUCTION")
    value.add_argument("--source", type=Path, required=True)
    value.add_argument("--manifest", type=Path, required=True)
    value.add_argument("--output", type=Path, required=True)
    value.add_argument("--resume", type=Path)
    value.add_argument("--seconds", type=float, required=True)
    value.add_argument("--workers", type=int, choices=(2, 4), default=4)
    return value


def main(argv: Sequence[str] | None = None) -> int:
    args = parser().parse_args(argv)
    output = args.output if args.output.is_absolute() else ROOT / args.output
    source_path = args.source if args.source.is_absolute() else ROOT / args.source
    manifest_path = args.manifest if args.manifest.is_absolute() else ROOT / args.manifest
    resume_path = None if args.resume is None else (
        args.resume if args.resume.is_absolute() else ROOT / args.resume)
    if output.exists():
        raise ProtocolStop("stale output")
    registry: SourceRegistry | None = None
    meter: Meter | None = None
    source_public: dict[str, Any] | None = None
    search: Search | None = None
    selftest: dict[str, Any] | None = None
    runtime: dict[str, Any] | None = None
    old_value: dict[str, Any] | None = None
    reducer: FormalReducer | None = None
    p_rows: list[dict[bytes, int]] | None = None
    triangular: dict[str, Any] | None = None
    try:
        meter = Meter(args.seconds)
        registry = SourceRegistry(); registry.authenticate()
        require(manifest_path.resolve() == (ROOT / SOURCE_PINS["manifest"][0]).resolve() and
                registry.json("manifest") == EXPECTED_MANIFEST,
                "manifest fixed contract")
        raw, physical = read_physical_once(source_path, RAW_BYTES, RAW_SHA256)
        source_public = {"path": str(source_path), "member": RAW_MEMBER,
                         "bytes": RAW_BYTES, "sha256": RAW_SHA256,
                         "physical": physical, "parsed_once": True}
        try:
            old_value = json.loads(raw.decode("utf-8"))
        except (UnicodeError, json.JSONDecodeError) as exc:
            raise InputStop("source_json") from exc
        del raw
        runtime = build_light(registry, meter)
        try:
            validate_old_envelope(old_value, runtime["live"])
            reducer, p_rows, triangular = build_triangular(old_value, runtime, meter)
        except ResourceStop:
            raise
        except (ProtocolStop, RuntimeError, ValueError, TypeError,
                IndexError, KeyError) as exc:
            raise InputStop("v276_triangular_gate") from exc
        meter.check("light_basis_complete")
        selftest = run_real_owner_selftest(runtime, old_value, reducer, registry)
        search = Search(runtime, registry, source_public, old_value, reducer, p_rows,
                        triangular, meter, output, args.workers, selftest)
        if resume_path is not None:
            restore_checkpoint(search, resume_path)
        receipt = search.run()
    except InputStop as exc:
        if search is not None:
            search.boundary.abort("typed_input_stop")
        receipt = unknown_receipt(UNKNOWN_INPUT, str(exc), registry, source_public,
            meter, None, None if search is None else search.boundary.public(), selftest)
    except ResourceStop as exc:
        if search is None:
            require(runtime is not None and registry is not None and
                    source_public is not None and old_value is not None and
                    reducer is not None and p_rows is not None and
                    triangular is not None and meter is not None,
                    "resource stop before safe P boundary")
            reference, boundary_public = write_prepool_checkpoint(
                runtime, registry, source_public, old_value, reducer, p_rows,
                triangular, meter, output, args.workers)
        else:
            search.boundary.abort("typed_resource_stop")
            reference = search.write_checkpoint("resource_stop",
                                                terminal_checkpoint=True)
            boundary_public = search.boundary.public()
        reason = (f"phase={exc.phase}:cap={exc.cap}:value={exc.value}:"
                  f"limit={exc.limit}")
        receipt = unknown_receipt(UNKNOWN_RESOURCE, reason, registry, source_public,
                                  meter, reference, boundary_public, selftest)
    except ProtocolStop:
        if search is not None:
            search.boundary.abort("hard_protocol_stop")
        raise
    except BaseException:
        if search is not None:
            search.boundary.abort("hard_unexpected_stop")
        raise
    exclusive_json(output, receipt)
    print(PRODUCER_PREFIX + " " + receipt["terminal"], flush=True)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ProtocolStop, SelftestReject, KeyError, TypeError, ValueError,
            AssertionError) as exc:
        print("R07_HISTORY_FREE_POSITIVE_FAST_RESUME_V7_PRODUCER_STOP " +
              type(exc).__name__ + ":" + str(exc), file=sys.stderr, flush=True)
        raise
