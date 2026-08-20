#!/usr/bin/env python3
"""Memo/fusion successor for the registered-4096 WordExpr/Fox lane.

The input is the frozen, independently checked 157da q=3 receipt.  This
program never constructs H=ker(PB4->E4).  It uses the equivariant Fox chain

    F3[E]^11 -> F3[E]^6 -> F3[E]

and emits a shared lossless provenance DAG for every positive Phi_3(H)
membership.  A bounded search miss is explicitly UNKNOWN.
"""

from __future__ import annotations

import argparse
import copy
import base64
import gc
import hashlib
import importlib.util
import json
import math
import os
import sys
import time
from array import array
from collections import OrderedDict, deque
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Iterator, Sequence

try:  # Linux production; the Windows selftest uses the documented fallback.
    import resource as _resource
except ImportError:  # pragma: no cover - exercised by the Windows selftest.
    _resource = None


SCHEMA = "d972-b345-relative-frattini3-wordexpr-memo/v9"
Q3_SCHEMA = "d972-b345-q-chief/v1"
Q3_PRODUCER = Path("search/d972_b345_q3_chief_v1.g")
Q3_PRODUCER_SHA = "b95fc29b326c3d6a378249cdeb03595eed8d0211a7fe0358fc02447d70d5f755"
Q3_CHECKER = Path("search/check_d972_b345_q3_chief_v1.py")
Q3_CHECKER_SHA = "ddb52ddae18327209692f0f6eb8b4f65cbdd446155be660a621de24274cc3f73"
Q3_DRIVER = Path("search/d972_b345_q3_gha_driver_v1.g")
Q3_DRIVER_SHA = "c397cd837ff6814f7b7a8ca0604c6aed54fa0bc85bb577516ea1c6e7df83a831"
FORMULA_SHA = "b43284edac5b4dae945bb3b30ac0f177dc47df8724cb32acd6057b26d82a27ef"
Q3_ARTIFACT_SHA = "3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72"
Q3_ARTIFACT_PATH = Path("ci/out/d972_b345_q3_chief_v1.json")
OUTPUT_PATH = Path("ci/out/d972_b345_relfrat3_wordexpr_memo_v9.json")
V8_PRODUCER = Path("search/d972_b345_relfrat3_wordexpr_v8.py")
V8_PRODUCER_SHA = "ea2c2901e316bfaa1c42d3f9966de5ec76323139728dfef46d2032608997e8db"
V8_CHECKER = Path("search/check_d972_b345_relfrat3_wordexpr_v8.py")
V8_CHECKER_SHA = "9d3368504953862e688f474871e72cdc1ae4153e4737b8b6260ba260804db413"
V8_DRIVER = Path("search/d972_b345_relfrat3_wordexpr_gha_driver_v8.g")
V8_DRIVER_SHA = "63e9a8dcc87c446fb130665dfe94c29cbe0836f1b87682f9b5ac4a7eb7c25018"
V7_PRODUCER = Path("search/d972_b345_relfrat3_pivot_surgery_v7.py")
V7_PRODUCER_SHA = "a19c3353c5cfc6da8ad0b7d941ba94bde043c80e69e33c889c5710c897d7a757"
V7_CHECKER = Path("search/check_d972_b345_relfrat3_pivot_surgery_v7.py")
V7_CHECKER_SHA = "fbe033704180a808320c897c52613ca6847305dd85ddcd7a70aa825161e8bfa0"
V7_DRIVER = Path("search/d972_b345_relfrat3_pivot_surgery_gha_driver_v7.g")
V7_DRIVER_SHA = "1be0ec44674108a2f6319057ba18283206756cf2ef73bfe1e1e5896a6f893d8d"
V6_PRODUCER = Path("search/d972_b345_relfrat3_fixed_candidate_v6.py")
V6_PRODUCER_SHA = "178c7e63dafba0b9deb8b4e363552ff87a0b7d1c2a120457f593845d56d9d493"
V6_CHECKER = Path("search/check_d972_b345_relfrat3_fixed_candidate_v6.py")
V6_CHECKER_SHA = "12c5475c984aa2855c502930169a01cc656ec67507a6aa56d098cd314db011fd"
V6_DRIVER = Path("search/d972_b345_relfrat3_fixed_candidate_gha_driver_v6.g")
V6_DRIVER_SHA = "2b36db96d440316292d271c22e662da507dc6afeba20aa0222c8388bab6f4ada"
V5_PRODUCER = Path("search/d972_b345_relfrat3_fixed_candidate_v5.py")
V5_PRODUCER_SHA = "e4675906601714ee16219d747cf95ffef54b19e354228dd6e7d3cd99d59127ea"
V5_CHECKER = Path("search/check_d972_b345_relfrat3_fixed_candidate_v5.py")
V5_CHECKER_SHA = "0cb7e0173fe022f304010c64ef89b7200464f4ad8c1e1bc7c3ad4001ffe12246"
V5_DRIVER = Path("search/d972_b345_relfrat3_fixed_candidate_gha_driver_v5.g")
V5_DRIVER_SHA = "3bcb19326bfff1e313870a64cca95840b0e581aa1f7c713ee18300faf149261d"
V4_PRODUCER = Path("search/d972_b345_relfrat3_v4.py")
V4_PRODUCER_SHA = "ff2e021647fdaf84697c91f741f2d039575036bc1f389d9dc59dee512e6ca7e1"
V4_CHECKER = Path("search/check_d972_b345_relfrat3_v4.py")
V4_CHECKER_SHA = "54308d8628cd434bbc6a4522fe86296d72d01b42de8db2bc72ea9a6961157c2b"
V4_DRIVER = Path("search/d972_b345_relfrat3_gha_driver_v4.g")
V4_DRIVER_SHA = "b717b6a214913d26207ba4683bbe0403123d5139b5aa45cd7bba62be2b885d56"
V3_PRODUCER = Path("search/d972_b345_relfrat3_v3.py")
V3_PRODUCER_SHA = "df60849f9fa4bb6a09e0d23d799e31473960544728db6eb5507a6fd54749343b"
V3_CHECKER = Path("search/check_d972_b345_relfrat3_v3.py")
V3_CHECKER_SHA = "11345a8db5ff6d08fa8395301c270532d0d96714cc8d77d98643dac04a6856cf"
V3_DRIVER = Path("search/d972_b345_relfrat3_gha_driver_v3.g")
V3_DRIVER_SHA = "fe7a76191a484194696931c5acb59ec6ee0115af75d543613281c28e4d6a4d7a"
V2_PRODUCER = Path("search/d972_b345_relfrat3_v2.py")
V2_PRODUCER_SHA = "fad364043926dbdc03e56accf089f454d625e0b315c98a7647bc891677313cc8"
V2_CHECKER = Path("search/check_d972_b345_relfrat3_v2.py")
V2_CHECKER_SHA = "3c8967bea6946b42cef08cd097eab4e9071aae203ee27ac38038c4d5adb83f07"
V2_DRIVER = Path("search/d972_b345_relfrat3_gha_driver_v2.g")
V2_DRIVER_SHA = "006e33e97c6f9ac1982887206c904dbcf423c95790ec2fe0c45d9a1b3a2e38aa"
V1_PRODUCER = Path("search/d972_b345_relfrat3_v1.py")
V1_PRODUCER_SHA = "4b73fbfe19bb33a9decdec5fda437f58f61a3ecb1989090bd08151f60ce6609e"
V1_CHECKER = Path("search/check_d972_b345_relfrat3_v1.py")
V1_CHECKER_SHA = "3d86240237229b250943c4795c24c32ac75af9229534c73d16bd838f6d6d0101"
V1_DRIVER = Path("search/d972_b345_relfrat3_gha_driver_v1.g")
V1_DRIVER_SHA = "fce9b3ba8c9b686fb6af2bd5a6da1b29f7486616948a6907982af14cd5d8738b"
FIXED_WORD = [-2, -2, -1, -1, 2, 2, 1, -2, -1, -1,
              2, 2, 2, -1, -2, -2, 1, 1, 1, 1]

TERMINALS = {
    "B345_RELFRAT3_WORDEXPR_PASS",
    "B345_RELFRAT3_WORDEXPR_SEARCH_INCOMPLETE",
    "B345_RELFRAT3_WORDEXPR_UNKNOWN_RESOURCE",
    "B345_RELFRAT3_WORDEXPR_UNKNOWN_INPUT",
}

CAPS = {
    "small_representation_dimension": 64,
    "candidate_correction_dictionary": 4096,
    "coefficient_translates_per_relator": 32768,
    "total_sparse_group_ring_keys": 4_194_304,
    "single_sparse_elimination_row": 4_194_304,
    "target_elimination_support": 4_194_304,
    "sparse_pivot_rows": 1_000_000,
    "provenance_dag_nodes": 2_000_000,
    "provenance_dag_edges": 4_000_000,
    "single_word_or_section_length": 100_000,
    "affine_residual_dimension": 12,
    "explicit_affine_candidates": 531441,
    "ambient_PB5_ANUPQ": 1,
    "relative_ANUPQ_RS_full_Elements": 0,
    "producer_soft_timeout_seconds": 7_200,
    "producer_soft_rss_bytes": 4_831_838_208,
    "element_pool": 2_000_000,
    "element_product_cache": 262_144,
    "element_inverse_cache": 65_536,
    "pc_pair_product_cache": 65_536,
    "pc_inverse_cache": 16_384,
    "section_slp_nodes": 65_536,
    "persistent_candidate_gradient_entries": 0,
    "blocker_table": 4_096,
    "transaction_trace_records": 100_000,
    "cheap_contexts": 64,
    "progress_interval_seconds": 10,
    "directed_surgery_rounds": 256,
    "directed_unique_translations": 32_768,
    "directed_columns": 360_448,
    "directed_section_expr_nodes": 131_072,
    "directed_section_expr_edges": 262_144,
    "wordexpr_nodes_per_candidate": 262_144,
    "wordexpr_edges_per_candidate": 1_048_576,
    "dictionary_word_records": 4_096,
    "wordexpr_flat_leaves_per_candidate": 16_384,
    "wordexpr_expanded_letter_count_per_target": 4_194_304,
    "candidate_live_gradient_entries_total": 1_000_000,
    "gradient_memo_sparse_entries": 1_000_000,
    "gradient_memo_nodes": 16_384,
    "gradient_memo_estimated_bytes_per_sparse_entry": 256,
    "gradient_memo_additional_budget_bytes": 256_000_000,
    "gradient_memo_pinned_source_roots": 6,
    "memo_progress_records": 200_000,
    "candidate_element_pool_suffix": 1_000_000,
    "candidate_scan_records": 4_096,
}

V7_PREFIX_BINDINGS = {
    "stable_rounds_projection_sha256": "75a2894da0f19d0e541e27924ee63e220a6eca35e852b21088ee304ba42fc42d",
    "volatile_rounds_sha256_provenance_only": "e1c11cd5a436229c8730d5174b9a6981a508901a6e44d5362219e03d74557391",
    "translations_sha256": "a4b952bce888713e293587cd63d710465121e782448a3e2a571d80b992ea363f",
    "columns_sha256": "cb57176146b926df16e508429db5aa1ff6b5b0ec691f2328371973681089b343",
    "blocker_history_sha256": "b5f100e45e874ce5ee3270cd31350b4318cf40931055571ac70066e69d62de53",
    "final_blocker_sha256": "0cd653ee0966ccc83d270802bbb5d00b61731f28e27eec1918bb5ea282e00903",
}

V5_CAPS = {**CAPS,
           "total_sparse_group_ring_keys": 1_000_000,
           "element_pool": 1_000_000}
V6_CAPS = {key: value for key, value in CAPS.items()
           if key not in {"directed_surgery_rounds",
                          "directed_unique_translations", "directed_columns",
                          "directed_section_expr_nodes",
                          "directed_section_expr_edges"}}
CAP_CALIBRATION = {
    "source_run": 32212335985,
    "source_receipt_sha256":
        "c9231ebb8fe65c47107556c6e06873fa68b74e148e1ab248cfada08a699975d4",
    "source_stop_reason": "total_sparse_group_ring_keys",
    "source_translations": 10809,
    "source_live_sparse_entries": 999999,
    "source_element_pool": 330011,
    "source_peak_RSS": 296407040,
    "old_sparse_cap": 1_000_000,
    "new_sparse_cap": 4_194_304,
    "old_pool_cap": 1_000_000,
    "new_pool_cap": 2_000_000,
    "semantics_changed": False,
    "resume_used": False,
}


class Reject(ValueError):
    pass


class ResourceStop(RuntimeError):
    def __init__(self, reason: str, *, cap_key: str | None = None,
                 cap_limit: int | None = None,
                 observed_count: int | None = None,
                 trigger_relation: str | None = None):
        super().__init__(reason)
        self.reason = reason
        self.cap_key = cap_key or reason
        if cap_limit is None:
            caps = globals().get("AFFINE_CAPS", {})
            inherited = globals().get("CAPS", {})
            cap_limit = caps.get(self.cap_key, inherited.get(self.cap_key))
            if cap_limit is None and self.cap_key == "producer_soft_rss":
                cap_limit = caps.get("producer_soft_rss_bytes",
                                     inherited.get("producer_soft_rss_bytes"))
            if cap_limit is None and self.cap_key == "producer_soft_timeout":
                cap_limit = caps.get("producer_soft_timeout_seconds",
                                     inherited.get("producer_soft_timeout_seconds"))
        self.cap_limit = int(cap_limit) if cap_limit is not None else 0
        # A stop receipt must report the measured/attempted value.  Never
        # synthesize cap+1: that would turn an uninstrumented raise into a
        # false operational witness.
        self.observed_count = (None if observed_count is None
                               else int(observed_count))
        self.trigger_relation = trigger_relation


class AffineInput(RuntimeError):
    """Authenticated external-input drift; serialized as UNKNOWN_INPUT."""

    pass


def current_rss_bytes() -> int:
    """Current RSS on Linux; bounded portable fallback for the selftest."""
    status = Path("/proc/self/status")
    if status.exists():
        for line in status.read_text(encoding="ascii").splitlines():
            if line.startswith("VmRSS:"):
                fields = line.split()
                require(len(fields) >= 3 and fields[2] == "kB", "VmRSS format")
                return int(fields[1]) * 1024
    if _resource is not None:
        # ru_maxrss is a peak rather than current RSS, hence conservative.
        value = int(_resource.getrusage(_resource.RUSAGE_SELF).ru_maxrss)
        return value if sys.platform == "darwin" else value * 1024
    return 0


class ResourceMonitor:
    """Fail-closed wall/RSS monitor plus bounded live progress reporting."""

    def __init__(self, start: float, seconds: int,
                 rss_reader: Any = current_rss_bytes) -> None:
        require(seconds == CAPS["producer_soft_timeout_seconds"],
                "soft-timeout configuration")
        self.start = start
        self.seconds = seconds
        self.rss_limit = CAPS["producer_soft_rss_bytes"]
        self.rss_reader = rss_reader
        self.last_phase = "initializing"
        self.check_count = 0
        self.current_rss = 0
        self.peak_rss = 0
        self.last_progress = start
        self.accounting_supplier: Any = None
        self.hit_reason: str | None = None

    def bind_accounting(self, supplier: Any) -> None:
        self.accounting_supplier = supplier

    def _sample(self) -> None:
        value = int(self.rss_reader())
        require(value >= 0, "RSS sample")
        self.current_rss = value
        self.peak_rss = max(self.peak_rss, value)

    def _progress(self, force: bool = False) -> None:
        now = time.monotonic()
        if not force and now-self.last_progress < CAPS["progress_interval_seconds"]:
            return
        fields = {
            "translations": 0, "columns": 0, "pivots": 0,
            "live_sparse_entries": 0, "element_pool": 0,
            "dag_nodes": 0, "dag_edges": 0, "candidate_cache": 0,
            "pc_cache_hits": 0, "pc_cache_misses": 0,
            "pc_cache_evictions": 0,
            "transactions": 0, "rollbacks": 0, "blockers": 0,
            "current_candidate": 0, "current_target": 0,
        }
        if self.accounting_supplier is not None:
            fields.update(self.accounting_supplier())
        body = " ".join(f"{key}={fields[key]}" for key in fields)
        print("D972_B345_RELFRAT3_WORDEXPR_MEMO_V9_PROGRESS "
              f"phase={self.last_phase} elapsed={now-self.start:.3f} "
              f"current_rss={self.current_rss} peak_rss={self.peak_rss} {body}",
              flush=True)
        self.last_progress = now

    def check(self, phase_name: str, force: bool = False) -> None:
        self.last_phase = phase_name
        self.check_count += 1
        now = time.monotonic()
        sampled = force or (self.check_count & 255) == 0 or \
            now-self.last_progress >= CAPS["progress_interval_seconds"]
        if sampled:
            self._sample()
            self._progress(force=force)
            if self.current_rss >= self.rss_limit:
                self.hit_reason = "producer_soft_rss"
                raise ResourceStop(self.hit_reason,
                                   cap_key="producer_soft_rss",
                                   cap_limit=self.rss_limit,
                                   observed_count=self.current_rss,
                                   trigger_relation="ge")
        if now-self.start >= self.seconds:
            self.hit_reason = "producer_soft_timeout"
            raise ResourceStop(self.hit_reason,
                               cap_key="producer_soft_timeout",
                               cap_limit=self.seconds,
                               observed_count=int(now-self.start),
                               trigger_relation="ge")

    def reserve(self, phase_name: str, additional_bytes: int) -> None:
        require(isinstance(additional_bytes, int) and additional_bytes >= 0,
                "RSS reservation")
        self.last_phase = phase_name
        self.check_count += 1
        self._sample()
        self._progress(force=True)
        if self.current_rss + additional_bytes >= self.rss_limit:
            self.hit_reason = "producer_soft_rss"
            raise ResourceStop(self.hit_reason,
                               cap_key="producer_soft_rss",
                               cap_limit=self.rss_limit,
                               observed_count=self.current_rss + additional_bytes,
                               trigger_relation="ge")
        if time.monotonic()-self.start >= self.seconds:
            self.hit_reason = "producer_soft_timeout"
            raise ResourceStop(self.hit_reason,
                               cap_key="producer_soft_timeout",
                               cap_limit=self.seconds,
                               observed_count=int(time.monotonic()-self.start),
                               trigger_relation="ge")

    def receipt(self, hit: bool) -> dict[str, Any]:
        return {
            "seconds": self.seconds,
            "minutes": self.seconds // 60,
            "rss_bytes": self.rss_limit,
            "rss_gib": 4.5,
            "external_job_limit_minutes": 330,
            "safety_margin_minutes": 30,
            "clock": "time.monotonic",
            "rss_primary": "/proc/self/status VmRSS",
            "rss_portable_fallback": "getrusage peak or injected selftest reader",
            "hit": hit,
            "hit_reason": self.hit_reason,
            "last_checked_phase": self.last_phase,
            "check_count": self.check_count,
            "current_rss_bytes": self.current_rss,
            "peak_rss_bytes": self.peak_rss,
            "terminal_on_hit": "B345_RELFRAT3_WORDEXPR_UNKNOWN_RESOURCE",
            "consulted_in_selftest": False,
        }


# Keep the old annotation name out of the hot-path code while retaining the
# same method contract for frozen helper signatures.
SoftDeadline = ResourceMonitor


def require(condition: bool, message: str) -> None:
    if not condition:
        raise Reject(message)


def phase(label: str, start: float) -> float:
    now = time.monotonic()
    print(f"D972_B345_RELFRAT3_PHASE {label} elapsed_s={now-start:.6f}", flush=True)
    return now


def canonical_bytes(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True).encode("ascii")


def digest_obj(obj: Any) -> str:
    return hashlib.sha256(canonical_bytes(obj)).hexdigest()


def digest_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def checked_write(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp-relfrat3")
    try:
        encoder = json.JSONEncoder(sort_keys=True, separators=(",", ":"),
                                   ensure_ascii=True)
        expected_hash = hashlib.sha256()
        expected_bytes = 0
        with temporary.open("wb") as stream:
            for piece in encoder.iterencode(obj):
                raw_piece = piece.encode("ascii")
                stream.write(raw_piece)
                expected_hash.update(raw_piece)
                expected_bytes += len(raw_piece)
            stream.write(b"\n")
            expected_hash.update(b"\n")
            expected_bytes += 1
            stream.flush()
            os.fsync(stream.fileno())
        def streamed_digest(target: Path) -> tuple[int, str]:
            digest = hashlib.sha256()
            size = 0
            with target.open("rb") as source:
                while True:
                    chunk = source.read(1 << 20)
                    if not chunk:
                        break
                    digest.update(chunk)
                    size += len(chunk)
            return size, digest.hexdigest()
        expected = expected_hash.hexdigest()
        require(streamed_digest(temporary) == (expected_bytes, expected),
                "temporary output streamed readback")
        os.replace(temporary, path)
        require(streamed_digest(path) == (expected_bytes, expected),
                "final output streamed readback")
    finally:
        if temporary.exists():
            temporary.unlink()


def reduce_word(word: Iterable[int]) -> list[int]:
    out: list[int] = []
    for letter in word:
        require(isinstance(letter, int) and letter != 0, "invalid signed word letter")
        if out and out[-1] == -letter:
            out.pop()
        else:
            out.append(letter)
        if len(out) > CAPS["single_word_or_section_length"]:
            raise ResourceStop("single_word_or_section_length",
                               cap_key="single_word_or_section_length",
                               cap_limit=CAPS["single_word_or_section_length"],
                               observed_count=len(out), trigger_relation="gt")
    return out


def inv_word(word: Sequence[int]) -> list[int]:
    return reduce_word(-letter for letter in reversed(word))


def word_substitute(word: Sequence[int], images: Sequence[Sequence[int]]) -> list[int]:
    out: list[int] = []
    for letter in word:
        require(1 <= abs(letter) <= len(images), "word substitution index")
        out.extend(images[abs(letter)-1] if letter > 0 else inv_word(images[-letter-1]))
        out = reduce_word(out)
    return out


def pp_words(words: Sequence[Sequence[int]]) -> list[int]:
    require(bool(words), "empty paper-product word")
    return reduce_word(x for word in reversed(words) for x in word)


def commutator(a: Sequence[int], b: Sequence[int]) -> list[int]:
    return reduce_word(inv_word(a) + inv_word(b) + list(a) + list(b))


def exponent_sums(word: Sequence[int], width: int) -> list[int]:
    return [sum(1 if x > 0 else -1 for x in word if abs(x) == i)
            for i in range(1, width + 1)]


def derived_commutator_ledger(word: Sequence[int]) -> dict[str, Any]:
    """Losslessly bubble a zero-abelianization F2 word to the identity.

    If W=AabB and W'=AbaB, then W=[Aa^-1A^-1,Ab^-1A^-1] W'.
    Thus every swap is one explicit commutator and the product is literally W.
    """
    require(exponent_sums(word, 2) == [0, 0], "derived ledger exponent sums")
    current = reduce_word(word)
    factors: list[dict[str, Any]] = []
    while True:
        pos = next((i for i in range(len(current)-1)
                    if abs(current[i]) == 2 and abs(current[i+1]) == 1), None)
        if pos is None:
            break
        prefix = current[:pos]
        a, b = current[pos], current[pos+1]
        left = reduce_word(prefix + [-a] + inv_word(prefix))
        right = reduce_word(prefix + [-b] + inv_word(prefix))
        factors.append({"left": left, "right": right})
        current = reduce_word(current[:pos] + [b, a] + current[pos+2:])
    require(current == [], "derived bubble normal form is not identity")
    expanded: list[int] = []
    for row in factors:
        expanded = reduce_word(expanded + commutator(row["left"], row["right"]))
    require(expanded == reduce_word(word), "derived commutator product mismatch")
    return {"convention": "[a,b]=a^-1*b^-1*a*b",
            "factors": factors, "expanded_word": expanded,
            "factor_count": len(factors)}


###############################################################################
# Pure braid presentations and literal cofaces.
###############################################################################


def pairs(rank: int) -> list[list[int]]:
    return [[i, j] for i in range(1, rank) for j in range(i+1, rank+1)]


def pair_index(rank: int, pair: Sequence[int]) -> int:
    try:
        return pairs(rank).index(list(pair)) + 1
    except ValueError as exc:
        raise Reject(f"bad PB{rank} pair {pair}") from exc


def artin_step(rank: int, letter: int) -> list[list[int]]:
    i = abs(letter)
    require(1 <= i < rank, "Artin letter")
    images = [[j] for j in range(1, rank+1)]
    if letter > 0:
        images[i-1], images[i] = [i, i+1, -i], [i]
    else:
        images[i-1], images[i] = [i+1], [-(i+1), i, i+1]
    return images


def artin_images(rank: int, braid: Sequence[int]) -> list[list[int]]:
    images = [[j] for j in range(1, rank+1)]
    for letter in braid:
        step = artin_step(rank, letter)
        images = [word_substitute(w, step) for w in images]
    return images


def aij_braid(i: int, j: int) -> list[int]:
    return list(range(j-1, i, -1)) + [i, i] + [-k for k in range(i+1, j)]


def pure_relations(rank: int) -> list[list[int]]:
    if rank == 2:
        return []
    old_pairs = pairs(rank-1)
    old_map = [[pair_index(rank, p)] for p in old_pairs]
    rels = [word_substitute(w, old_map) for w in pure_relations(rank-1)]
    kernel = [[pair_index(rank, [k, rank])] for k in range(1, rank)]
    for i, j in old_pairs:
        g = pair_index(rank, [i, j])
        action = artin_images(rank-1, aij_braid(i, j))
        for k in range(1, rank):
            h = pair_index(rank, [k, rank])
            rels.append(reduce_word([-g, h, g] +
                                    inv_word(word_substitute(action[k-1], kernel))))
    return rels


def coface_generator(rank: int, slot: int, pair: Sequence[int]) -> list[int]:
    i, j = pair
    if slot == 0:
        return [pair_index(rank+1, [i+1, j+1])]
    if slot == rank+1:
        return [pair_index(rank+1, [i, j])]
    require(1 <= slot <= rank, "coface slot")
    if i == slot:
        return [pair_index(rank+1, [slot, j+1]),
                pair_index(rank+1, [slot+1, j+1])]
    if j == slot:
        return [pair_index(rank+1, [i, slot]),
                pair_index(rank+1, [i, slot+1])]
    return [pair_index(rank+1, [i + (i > slot), j + (j > slot)])]


def cofaces(rank: int) -> list[list[list[int]]]:
    return [[coface_generator(rank, slot, p) for p in pairs(rank)]
            for slot in range(rank+2)]


def relevant_formula() -> dict[str, Any]:
    c34 = cofaces(3)
    return {
        "convention": {
            "pair_order": "lexicographic_i_then_j",
            "word_product": "left_to_right",
            "paper_product": "displayed_factors_multiplied_right_to_left",
            "coface_slots": "0=left endpoint,1..r=strand doubling,r+1=right endpoint",
        },
        "presentations": {
            f"PB{r}": {"pairs": pairs(r), "relations": pure_relations(r)}
            for r in (3, 4, 5)
        },
        "cofaces_3_4": c34,
        "a18_order": {
            "names": ["phi_123", "phi_234", "phi_12_3_4",
                      "phi_1_23_4", "phi_1_2_34"],
            "slots": [4, 0, 1, 2, 3],
            "maps": [c34[i] for i in (4, 0, 1, 2, 3)],
        },
    }


###############################################################################
# Independent finite quotient arithmetic from the receipt.
###############################################################################


Perm = bytes
Pc = bytes
EKey = tuple[Perm, Pc]
VectorKey = tuple[int, EKey]
SparseVector = dict[VectorKey, int]


def perm_from_row(row: Sequence[int], degree: int) -> Perm:
    require(len(row) == degree and all(isinstance(x, int) for x in row),
            "permutation row")
    value = bytes(x-1 for x in row)
    require(set(value) == set(range(degree)), "permutation is not bijective")
    return value


def perm_one(degree: int) -> Perm:
    require(degree <= 256, "packed permutation degree")
    return bytes(range(degree))


def perm_mul(a: Perm, b: Perm) -> Perm:
    require(len(a) == len(b), "permutation degree")
    return bytes(b[a[i]] for i in range(len(a)))


def perm_inv(a: Perm) -> Perm:
    out = [0] * len(a)
    for i, image in enumerate(a):
        out[image] = i
    return bytes(out)


def perm_order(value: Perm) -> int:
    seen = [False] * len(value)
    answer = 1
    for i in range(len(value)):
        if seen[i]:
            continue
        j, length = i, 0
        while not seen[j]:
            seen[j] = True
            j = value[j]
            length += 1
        answer = math.lcm(answer, length)
    return answer


def coords_word(coords: Sequence[int]) -> list[int]:
    return [i for i, exponent in enumerate(coords, 1) for _ in range(exponent)]


class BoundedLRU:
    """Exact bounded cache; eviction is semantics-neutral."""

    def __init__(self, capacity: int) -> None:
        require(isinstance(capacity, int) and capacity > 0, "LRU capacity")
        self.capacity = capacity
        self.data: OrderedDict[Any, Any] = OrderedDict()
        self.hits = 0
        self.misses = 0
        self.evictions = 0
        self.clears = 0
        self.peak = 0

    def get(self, key: Any) -> Any | None:
        if key not in self.data:
            self.misses += 1
            return None
        self.hits += 1
        self.data.move_to_end(key)
        return self.data[key]

    def put(self, key: Any, value: Any) -> None:
        if key in self.data:
            self.data[key] = value
            self.data.move_to_end(key)
            return
        if len(self.data) >= self.capacity:
            self.data.popitem(last=False)
            self.evictions += 1
        self.data[key] = value
        self.peak = max(self.peak, len(self.data))

    def clear(self) -> None:
        self.data.clear()
        self.clears += 1

    def accounting(self) -> dict[str, int]:
        return {"capacity": self.capacity, "size": len(self.data),
                "peak": self.peak, "hits": self.hits,
                "misses": self.misses, "evictions": self.evictions,
                "clears": self.clears}


@dataclass
class PcCollector:
    receipt: dict[str, Any]

    def __post_init__(self) -> None:
        self.n = int(self.receipt["generator_count"])
        self.orders = list(self.receipt["relative_orders"])
        require(self.n == len(self.orders) and self.n <= 175 and
                all(x == 3 for x in self.orders), "pc rank/orders")
        self.powers = [self.coord(x) for x in self.receipt["power_relations"]]
        self.inverses = [self.coord(x) for x in self.receipt["inverses"]]
        self.conjugates = {(x["i"], x["j"]): self.coord(x["coords"])
                           for x in self.receipt["conjugate_relations"]}
        self.inverse_conjugates = {
            (x["i"], x["j"]): self.coord(x["coords"])
            for x in self.receipt["inverse_conjugate_relations"]}
        require(len(self.conjugates) == self.n*(self.n-1)//2 and
                set(self.conjugates) == set(self.inverse_conjugates),
                "pc conjugate tables")
        self.pair_cache = BoundedLRU(CAPS["pc_pair_product_cache"])
        self.inverse_cache = BoundedLRU(CAPS["pc_inverse_cache"])

    def coord(self, row: Sequence[int]) -> Pc:
        require(len(row) == self.n and all(isinstance(x, int) for x in row) and
                all(0 <= x < 3 for x in row), "pc coordinate")
        return bytes(row)

    def one(self) -> Pc:
        return bytes(self.n)

    def unit(self, index: int) -> Pc:
        require(1 <= index <= self.n, "pc unit")
        row = [0] * self.n
        row[index-1] = 1
        return bytes(row)

    def collect_uncached(self, word: Sequence[int]) -> Pc:
        tokens: list[int] = []
        for x in word:
            require(1 <= abs(x) <= self.n, "pc letter")
            tokens.extend([x] if x > 0 else coords_word(self.inverses[-x-1]))
        steps = 0
        cap = max(10000, 1000*(1+len(tokens))*(1+self.n))
        while True:
            changed = False
            for pos in range(len(tokens)-1):
                a, b = tokens[pos], tokens[pos+1]
                if a > b:
                    tokens[pos:pos+2] = [b] + coords_word(self.conjugates[(a, b)])
                    changed = True
                    break
            if not changed:
                pos = 0
                while pos < len(tokens):
                    i, run = tokens[pos], pos
                    while run < len(tokens) and tokens[run] == i:
                        run += 1
                    if run-pos >= 3:
                        tokens[pos:pos+3] = coords_word(self.powers[i-1])
                        changed = True
                        break
                    pos = run
            if not changed:
                break
            steps += 1
            require(steps <= cap, "pc collection cap")
        row = [0] * self.n
        last = 0
        for x in tokens:
            require(x >= last, "pc order")
            row[x-1] += 1
            require(row[x-1] < 3, "pc power")
            last = x
        return bytes(row)

    def collect(self, word: Sequence[int]) -> Pc:
        # Arbitrary full-token words are deliberately never retained.
        return self.collect_uncached(word)

    def mul(self, a: Pc, b: Pc) -> Pc:
        require(len(a) == len(b) == self.n, "pc product width")
        key = a + b
        cached = self.pair_cache.get(key)
        if cached is not None:
            return cached
        answer = self.collect_uncached(coords_word(a) + coords_word(b))
        self.pair_cache.put(key, answer)
        return answer

    def inverse(self, a: Pc) -> Pc:
        require(len(a) == self.n, "pc inverse width")
        cached = self.inverse_cache.get(a)
        if cached is not None:
            return cached
        word: list[int] = []
        for i in range(self.n, 0, -1):
            for _ in range(a[i-1]):
                word.extend(coords_word(self.inverses[i-1]))
        answer = self.collect_uncached(word)
        self.inverse_cache.put(a, answer)
        return answer

    def eval(self, word: Sequence[int], images: Sequence[Pc]) -> Pc:
        out = self.one()
        for x in word:
            value = images[abs(x)-1]
            out = self.mul(out, value if x > 0 else self.inverse(value))
        return out

    def cache_accounting(self) -> dict[str, Any]:
        pair = self.pair_cache.accounting()
        inverse = self.inverse_cache.accounting()
        return {
            "policy": "bounded exact pair-product and inverse LRU; no full-word cache",
            "pair_product": pair,
            "inverse": inverse,
            "hits": pair["hits"] + inverse["hits"],
            "misses": pair["misses"] + inverse["misses"],
            "evictions": pair["evictions"] + inverse["evictions"],
            "unbounded_full_token_word_cache": False,
        }

    def clear_caches(self) -> None:
        self.pair_cache.clear()
        self.inverse_cache.clear()


@dataclass
class MatchedQuotient:
    rank: int
    degree: int
    pc: PcCollector
    generators: list[EKey]

    def __post_init__(self) -> None:
        require(len(self.generators) == len(pairs(self.rank)), "matched marked width")
        self.identity: EKey = (perm_one(self.degree), self.pc.one())
        self.inverse_generators = [self.inverse(g) for g in self.generators]

    def mul(self, a: EKey, b: EKey) -> EKey:
        return perm_mul(a[0], b[0]), self.pc.mul(a[1], b[1])

    def inverse(self, a: EKey) -> EKey:
        return perm_inv(a[0]), self.pc.inverse(a[1])

    def eval(self, word: Sequence[int], images: Sequence[EKey] | None = None) -> EKey:
        marked = self.generators if images is None else images
        out = self.identity
        for x in word:
            value = marked[abs(x)-1]
            out = self.mul(out, value if x > 0 else self.inverse(value))
        return out


def eval_perm_word(word: Sequence[int], images: Sequence[Perm]) -> Perm:
    out = perm_one(len(images[0]))
    for x in word:
        value = images[abs(x)-1]
        out = perm_mul(out, value if x > 0 else perm_inv(value))
    return out


def enumerate_generated(identity: Any, generators: Sequence[Any], mul: Any,
                        inverse: Any, cap: int) -> set[Any]:
    steps = list(generators) + [inverse(x) for x in generators]
    seen = {identity}
    queue = [identity]
    while queue:
        a = queue.pop()
        for g in steps:
            b = mul(a, g)
            if b not in seen:
                seen.add(b)
                require(len(seen) <= cap, "small subgroup cap")
                queue.append(b)
    return seen


def paper_conjugate(value: Any, y: Any, identity: Any, mul: Any, inverse: Any) -> Any:
    # PP([value^-1,y,value]) = value*y*value^-1.
    return mul(mul(value, y), inverse(value))


###############################################################################
# Literal B3/B4 words.
###############################################################################


def f2_substitute(word: Sequence[int], x: Sequence[int], y: Sequence[int]) -> list[int]:
    return word_substitute(word, [x, y])


def hexagon_words(f: Sequence[int]) -> list[list[int]]:
    x, y = [1], [2]
    z = inv_word(pp_words([x, y]))
    u = inv_word(pp_words([y, x]))
    fxy = f2_substitute(f, x, y)
    fxz = f2_substitute(f, x, z)
    fyz = f2_substitute(f, y, z)
    fux = f2_substitute(f, u, x)
    fuy = f2_substitute(f, u, y)
    return [pp_words([fxy, inv_word(fxz), fyz]),
            pp_words([inv_word(fux), inv_word(fxy), fuy])]


def embed_f2_pb3(word: Sequence[int]) -> list[int]:
    # PB3 pair order is A12,A13,A23.
    return word_substitute(word, [[1], [3]])


def pentagon_word(f: Sequence[int]) -> list[int]:
    g = [[i] for i in range(1, 7)]
    contexts = [
        [g[0], g[3]],
        [g[3], g[5]],
        [pp_words([g[1], g[3]]), g[5]],
        [pp_words([g[0], g[1]]), pp_words([g[4], g[5]])],
        [g[0], pp_words([g[3], g[4]])],
    ]
    parts = [f2_substitute(f, x, y) for x, y in contexts]
    return pp_words([inv_word(pp_words([parts[4], parts[2]])),
                     parts[1], parts[3], parts[0]])


def source_words_m0(f: Sequence[int]) -> list[list[int]]:
    ff = word_substitute(f, [[1], [4]])
    g = word_substitute(f, [[1], [2]])
    gs = word_substitute(f, [[4], [5]])
    f1234 = word_substitute(f, [[4, 2], [6]])
    h = word_substitute(f, [[2, 1], [3]])
    middle = word_substitute(f, [[2, 1], [6, 5]])
    return [
        [1],
        reduce_word(inv_word(g) + [2] + g),
        reduce_word(inv_word(ff) + inv_word(h) + [3] + h + ff),
        reduce_word(inv_word(ff) + [4] + ff),
        reduce_word(inv_word(ff) + inv_word(middle) + inv_word(gs) + [5] +
                    gs + middle + ff),
        reduce_word(inv_word(f1234) + [6] + f1234),
    ]


def two_sided_residuals(source: Sequence[Sequence[int]],
                        inverse_words: Sequence[Sequence[int]]) \
        -> tuple[list[list[int]], list[list[int]]]:
    forward_residuals = [reduce_word(word_substitute(inverse_words[i], source) +
                                     [-(i+1)]) for i in range(6)]
    inverse_residuals = [reduce_word(word_substitute(source[i], inverse_words) +
                                     [-(i+1)]) for i in range(6)]
    return forward_residuals, inverse_residuals


def normalized_inverse_fibre(data: dict[str, Any], quotient: MatchedQuotient) \
        -> tuple[dict[str, Any], tuple[EKey, ...], list[list[int]]]:
    powers = data["canonical_roof_powers"]
    rows = powers["rows"]
    require([row["exponent"] for row in rows] == [1, 2, 4, 5, 7, 8] and
            powers["canonicalized_each_step"] is True and
            powers["literal_power_words_retained"] is False,
            "normalized q3 power receipt")
    row7s = [row for row in rows if row["exponent"] == 7]
    row2s = [row for row in rows if row["exponent"] == 2]
    require(len(row7s) == len(row2s) == 1, "normalized exponent-two/seven rows")
    row7 = row7s[0]
    corrections = data["correction_fibre"]
    records = corrections["records"]
    require(len(records) == 27 and corrections["certificate"]["order"] == 27 and
            corrections["certificate"]["enumerated_count"] == 27 and
            corrections["certificate"]["all_words_coarse_identity"] is True,
            "normalized inverse correction fibre")
    selected_q3 = data["selected_solution"]
    selected_index = selected_q3["correction_index"]
    require(selected_q3["exponent"] == 2 and 1 <= selected_index <= 27 and
            reduce_word(row2s[0]["word"] + records[selected_index-1]["word"]) ==
            FIXED_WORD,
            "fixed exponent-two tuple/canonical fibre binding")
    base_source = source_words_m0(FIXED_WORD)
    base_key = tuple(quotient.eval(word) for word in base_source)
    tested: list[int] = []
    passing: list[int] = []
    candidates: dict[int, tuple[list[int], list[list[int]]]] = {}
    for index, record in enumerate(records, 1):
        candidate = reduce_word(row7["word"] + record["word"])
        inverse_words = source_words_m0(candidate)
        st, ts = two_sided_residuals(base_source, inverse_words)
        tested.append(index)
        if all(quotient.eval(word) == quotient.identity for word in st + ts):
            passing.append(index)
            candidates[index] = (candidate, inverse_words)
    require(tested == list(range(1, 28)) and passing,
            "normalized exponent-seven fibre has no E4 two-sided inverse")
    selected = passing[0]
    selected_candidate, selected_inverse = candidates[selected]
    max_length = max(map(len, selected_inverse))
    require(max_length <= CAPS["single_word_or_section_length"],
            "normalized inverse word cap")
    public = {
        "source": "pinned q3 canonical exponent-seven row times the complete authenticated 27-element correction fibre",
        "normalized_exponent": 7,
        "normalized_roof_order": 9,
        "normalized_power_row": row7,
        "correction_fibre_size": 27,
        "tested_indices": tested,
        "passing_indices": passing,
        "selection_policy": ("unique" if len(passing) == 1 else
                             "deterministic first; full passing set retained"),
        "selected_correction_index": selected,
        "selected_correction_word": records[selected-1]["word"],
        "selected_inverse_candidate_word": selected_candidate,
        "selected_inverse_words": selected_inverse,
        "max_inverse_word_length": max_length,
        "raw_endomorphism_powering_used": False,
        "componentwise_Q4_Pi4_inverse_words_combined": False,
    }
    return public, base_key, selected_inverse


def finite_normalized_inverse(
        f: Sequence[int], quotient: MatchedQuotient,
        pool: "ElementPool",
        inverse_cache: dict[tuple[int, ...], list[list[int]]],
        cache_stats: dict[str, int], normalized: dict[str, Any]) -> dict[str, Any]:
    source = source_words_m0(f)
    source_key = tuple(pool.intern(quotient.eval(word)) for word in source)
    cached = inverse_cache.get(source_key)
    if cached is None:
        cache_stats["misses"] += 1
        raise ResourceStop("missing_bounded_inverse_representative",
                           cap_key="missing_bounded_inverse_representative",
                           cap_limit=0, observed_count=cache_stats["misses"],
                           trigger_relation="gt")
    cache_stats["hits"] += 1
    inverse_words = [list(word) for word in cached]
    forward_residuals, inverse_residuals = two_sided_residuals(
        source, inverse_words)
    require(all(quotient.eval(w) == quotient.identity
                for w in forward_residuals),
            "normalized cached inverse does not give S(T_i)=x_i on E4")
    max_length = max(map(len, inverse_words))
    cache_stats["max_inverse_word_length"] = max(
        cache_stats["max_inverse_word_length"], max_length)
    return {
        "normalized_exponent": 7,
        "normalized_roof_order": 9,
        "source_words": source,
        "inverse_words": inverse_words,
        "ST_residuals": forward_residuals,
        "TS_residuals": inverse_residuals,
        "construction": "finite normalized exponent-seven inverse from the pinned complete 27-fibre",
        "max_inverse_word_length": max_length,
        "cache_hit": True,
        "cache_key_exact_six_E4_images": True,
        "cache_hit_ST_replay_in_E4": True,
        "TS_replay_diagnostic_only": True,
        "candidate_acceptance_or_certificate_reused": False,
        "componentwise_Q4_Pi4_inverse_words_combined": False,
        "normalized_fibre_selected_correction_index":
            normalized["selected_correction_index"],
        "normalized_fibre_passing_indices": normalized["passing_indices"],
    }


###############################################################################
# Sparse left-Fox calculus and translated-relator Gaussian search.
###############################################################################


def add_term(vector: SparseVector, key: VectorKey, coefficient: int) -> None:
    coefficient %= 3
    if not coefficient:
        return
    value = (vector.get(key, 0) + coefficient) % 3
    if value:
        vector[key] = value
    else:
        vector.pop(key, None)


def add_scaled(target: dict[Any, int], source: dict[Any, int], scalar: int) -> None:
    scalar %= 3
    if not scalar:
        return
    for key, coefficient in source.items():
        value = (target.get(key, 0) + scalar*coefficient) % 3
        if value:
            target[key] = value
        else:
            target.pop(key, None)


def scaled(source: dict[Any, int], scalar: int) -> dict[Any, int]:
    scalar %= 3
    return {key: (scalar*value) % 3 for key, value in source.items()
            if (scalar*value) % 3}


def fox_gradient(word: Sequence[int], quotient: MatchedQuotient) \
        -> tuple[SparseVector, EKey, dict[EKey, list[int]]]:
    prefix = quotient.identity
    prefix_word: list[int] = []
    gradient: SparseVector = {}
    sections: dict[EKey, list[int]] = {prefix: []}
    for letter in word:
        index = abs(letter)
        require(1 <= index <= len(quotient.generators), "Fox generator index")
        if letter > 0:
            add_term(gradient, (index, prefix), 1)
            prefix = quotient.mul(prefix, quotient.generators[index-1])
            prefix_word = reduce_word(prefix_word + [index])
        else:
            prefix = quotient.mul(prefix, quotient.inverse_generators[index-1])
            prefix_word = reduce_word(prefix_word + [-index])
            add_term(gradient, (index, prefix), 2)
        sections.setdefault(prefix, list(prefix_word))
    return gradient, prefix, sections


def fox_gradient_without_sections(
        word: Sequence[int], quotient: MatchedQuotient,
        progress_hook: Any = None) -> tuple[SparseVector, EKey]:
    """Same exact left Fox value/gradient, without unused section words.

    The frozen bridge and WordExpr evaluator consume only the first two
    outputs.  Avoiding repeated free reduction of every prefix removes an
    accidental quadratic cost while leaving the Fox recurrence unchanged.
    """
    prefix = quotient.identity
    gradient: SparseVector = {}
    for offset, letter in enumerate(word, 1):
        index = abs(letter)
        require(1 <= index <= len(quotient.generators),
                "Fox generator index")
        if letter > 0:
            add_term(gradient, (index, prefix), 1)
            prefix = quotient.mul(prefix, quotient.generators[index-1])
        else:
            prefix = quotient.mul(prefix,
                                  quotient.inverse_generators[index-1])
            add_term(gradient, (index, prefix), 2)
        if progress_hook is not None and (offset & 1023) == 0:
            progress_hook("flat_left_fox", offset, None)
    return gradient, prefix


def d1(vector: SparseVector, quotient: MatchedQuotient) -> dict[EKey, int]:
    out: dict[EKey, int] = {}
    for (index, element), coefficient in vector.items():
        add_scaled(out, {quotient.mul(element, quotient.generators[index-1]): 1,
                         element: 2}, coefficient)
    return out


def translate_vector(vector: SparseVector, translation: EKey,
                     quotient: MatchedQuotient) -> SparseVector:
    out: SparseVector = {}
    for (component, element), coefficient in vector.items():
        add_term(out, (component, quotient.mul(translation, element)), coefficient)
    return out


class _V2ReferenceProvenanceDAG:
    """Shared immutable F3 straight-line program for boundary witnesses."""

    def __init__(self, deadline: SoftDeadline | None = None) -> None:
        # Node ids are one-based and list order is topological.  The empty
        # linear combination is the unique zero node.
        self.nodes: list[dict[str, Any]] = [
            {"kind": "linear_combination", "terms": []},
        ]
        self.edge_count = 0
        self.max_nodes = 1
        self.max_edges = 0
        self.deadline = deadline

    def checkpoint(self) -> tuple[int, int]:
        return len(self.nodes), self.edge_count

    def rollback(self, checkpoint: tuple[int, int]) -> None:
        node_count, edge_count = checkpoint
        require(1 <= node_count <= len(self.nodes) and
                0 <= edge_count <= self.edge_count, "DAG rollback checkpoint")
        del self.nodes[node_count:]
        self.edge_count = edge_count

    def _append(self, node: dict[str, Any], edges: int) -> int:
        if len(self.nodes) + 1 > CAPS["provenance_dag_nodes"]:
            raise ResourceStop("provenance_dag_nodes",
                               cap_key="provenance_dag_nodes",
                               cap_limit=CAPS["provenance_dag_nodes"],
                               observed_count=len(self.nodes)+1,
                               trigger_relation="gt")
        if self.edge_count + edges > CAPS["provenance_dag_edges"]:
            raise ResourceStop("provenance_dag_edges",
                               cap_key="provenance_dag_edges",
                               cap_limit=CAPS["provenance_dag_edges"],
                               observed_count=self.edge_count+edges,
                               trigger_relation="gt")
        self.nodes.append(node)
        self.edge_count += edges
        self.max_nodes = max(self.max_nodes, len(self.nodes))
        self.max_edges = max(self.max_edges, self.edge_count)
        if self.deadline is not None and (len(self.nodes) & 1023) == 0:
            self.deadline.check("provenance_dag_growth")
        return len(self.nodes)

    def leaf(self, relator_index: int, translation: EKey) -> int:
        require(relator_index >= 1, "DAG leaf relator index")
        return self._append({
            "kind": "translated_relator_leaf",
            "relator_index": relator_index,
            "translation": translation,
            "translation_action": "left",
        }, 0)

    def linear(self, terms: Sequence[tuple[int, int]]) -> int:
        merged: dict[int, int] = {}
        for node_id, coefficient in terms:
            require(1 <= node_id <= len(self.nodes), "DAG backward reference")
            if node_id == 1:
                continue
            coefficient %= 3
            if coefficient:
                value = (merged.get(node_id, 0) + coefficient) % 3
                if value:
                    merged[node_id] = value
                else:
                    merged.pop(node_id, None)
        ordered = sorted(merged.items())
        if not ordered:
            return 1
        if len(ordered) == 1 and ordered[0][1] == 1:
            return ordered[0][0]
        return self._append({
            "kind": "linear_combination",
            "terms": ordered,
        }, len(ordered))

    def accounting(self) -> dict[str, int]:
        return {
            "live_nodes": len(self.nodes),
            "live_edges": self.edge_count,
            "peak_nodes": self.max_nodes,
            "peak_edges": self.max_edges,
        }

    def reachable(self, roots: Sequence[int]) -> set[int]:
        pending = list(roots)
        reached: set[int] = set()
        while pending:
            node_id = pending.pop()
            require(1 <= node_id <= len(self.nodes), "DAG root/reference range")
            if node_id in reached:
                continue
            reached.add(node_id)
            node = self.nodes[node_id-1]
            if node["kind"] == "linear_combination":
                pending.extend(parent for parent, _ in node["terms"])
        return reached


class _V2ReferenceSparseBoundaryBasis:
    def __init__(self, quotient: MatchedQuotient,
                 relator_columns: list[SparseVector], dag: _V2ReferenceProvenanceDAG,
                 deadline: SoftDeadline | None = None) -> None:
        self.quotient = quotient
        self.relator_columns = relator_columns
        self.dag = dag
        self.deadline = deadline
        self.rows: dict[VectorKey, tuple[SparseVector, int]] = {}
        self.translation_sections: dict[EKey, list[int]] = {quotient.identity: []}
        self.columns_seen = 0
        self.dependent_columns = 0
        self.max_vector_support = 0
        self.max_transient_vector_support = 0
        self.live_vector_entries = 0
        self.elimination_operations = 0

    @staticmethod
    def pivot(vector: SparseVector) -> VectorKey:
        return min(vector)

    def _resource_gate(self) -> None:
        if self.live_vector_entries > CAPS["total_sparse_group_ring_keys"]:
            raise ResourceStop("total_sparse_group_ring_keys",
                               cap_key="total_sparse_group_ring_keys",
                               cap_limit=CAPS["total_sparse_group_ring_keys"],
                               observed_count=self.live_vector_entries,
                               trigger_relation="gt")
        if len(self.rows) > CAPS["sparse_pivot_rows"]:
            raise ResourceStop("sparse_pivot_rows",
                               cap_key="sparse_pivot_rows",
                               cap_limit=CAPS["sparse_pivot_rows"],
                               observed_count=len(self.rows),
                               trigger_relation="gt")

    def accounting(self) -> dict[str, Any]:
        return {
            "live_sparse_vector_entries": self.live_vector_entries,
            "pivot_count": len(self.rows),
            "max_pivot_vector_support": self.max_vector_support,
            "max_transient_vector_support": self.max_transient_vector_support,
            "elimination_operations": self.elimination_operations,
            "dag": self.dag.accounting(),
        }

    def _deadline_gate(self, phase_name: str) -> None:
        self.elimination_operations += 1
        if self.deadline is not None and \
                (self.elimination_operations & 1023) == 0:
            self.deadline.check(phase_name)

    def add_column(self, relator_index: int, translation: EKey,
                   translation_word: Sequence[int]) -> None:
        checkpoint = self.dag.checkpoint()
        vector = translate_vector(self.relator_columns[relator_index-1],
                                  translation, self.quotient)
        node_id = self.dag.leaf(relator_index, translation)
        try:
            while vector:
                self.max_transient_vector_support = max(
                    self.max_transient_vector_support, len(vector))
                if len(vector) > CAPS["total_sparse_group_ring_keys"]:
                    raise ResourceStop("single_sparse_elimination_row",
                                       cap_key="single_sparse_elimination_row",
                                       cap_limit=CAPS["single_sparse_elimination_row"],
                                       observed_count=len(vector),
                                       trigger_relation="gt")
                pivot = self.pivot(vector)
                if pivot not in self.rows:
                    coefficient = vector[pivot]
                    inverse = 1 if coefficient == 1 else 2
                    vector = scaled(vector, inverse)
                    node_id = self.dag.linear([(node_id, inverse)])
                    if self.live_vector_entries + len(vector) > \
                            CAPS["total_sparse_group_ring_keys"]:
                        raise ResourceStop(
                            "total_sparse_group_ring_keys",
                            cap_key="total_sparse_group_ring_keys",
                            cap_limit=CAPS["total_sparse_group_ring_keys"],
                            observed_count=self.live_vector_entries + len(vector),
                            trigger_relation="gt")
                    if len(self.rows) + 1 > CAPS["sparse_pivot_rows"]:
                        raise ResourceStop(
                            "sparse_pivot_rows", cap_key="sparse_pivot_rows",
                            cap_limit=CAPS["sparse_pivot_rows"],
                            observed_count=len(self.rows)+1,
                            trigger_relation="gt")
                    self.rows[pivot] = (vector, node_id)
                    self.live_vector_entries += len(vector)
                    self.max_vector_support = max(self.max_vector_support, len(vector))
                    self.translation_sections.setdefault(translation,
                                                         list(translation_word))
                    self.columns_seen += 1
                    self._resource_gate()
                    return
                coefficient = vector[pivot]
                basis_vector, basis_node = self.rows[pivot]
                add_scaled(vector, basis_vector, -coefficient)
                node_id = self.dag.linear([(node_id, 1),
                                           (basis_node, -coefficient)])
                self._deadline_gate("pivot_column_elimination")
            self.dag.rollback(checkpoint)
            self.columns_seen += 1
            self.dependent_columns += 1
        except Exception:
            self.dag.rollback(checkpoint)
            raise

    def solve(self, target: SparseVector) -> int | None:
        checkpoint = self.dag.checkpoint()
        vector = dict(target)
        answer_node = 1
        try:
            while vector:
                self.max_transient_vector_support = max(
                    self.max_transient_vector_support, len(vector))
                pivot = self.pivot(vector)
                row = self.rows.get(pivot)
                if row is None:
                    self.dag.rollback(checkpoint)
                    return None
                coefficient = vector[pivot]
                add_scaled(vector, row[0], -coefficient)
                answer_node = self.dag.linear([(answer_node, 1),
                                               (row[1], coefficient)])
                if len(vector) > CAPS["total_sparse_group_ring_keys"]:
                    raise ResourceStop("target_elimination_support",
                                       cap_key="target_elimination_support",
                                       cap_limit=CAPS["target_elimination_support"],
                                       observed_count=len(vector),
                                       trigger_relation="gt")
                self._deadline_gate("target_sparse_elimination")
            return answer_node
        except Exception:
            self.dag.rollback(checkpoint)
            raise


def _v2_reference_translation_bfs(quotient: MatchedQuotient, cap: int) \
        -> Iterator[tuple[EKey, list[int]]]:
    steps = list(enumerate(quotient.generators, 1)) + [
        (-i, quotient.inverse_generators[i-1]) for i in range(1, 7)]
    seen = {quotient.identity}
    queue: deque[tuple[EKey, list[int]]] = deque([(quotient.identity, [])])
    while queue and len(seen) <= cap:
        element, word = queue.popleft()
        yield element, word
        if len(seen) == cap:
            continue
        for letter, step in steps:
            value = quotient.mul(element, step)
            if value not in seen:
                seen.add(value)
                queue.append((value, reduce_word(word + [letter])))
                if len(seen) == cap:
                    break


PackedSparseVector = dict[int, int]


def pack_vector_key(component: int, element_id: int) -> int:
    require(1 <= component <= 6 and 0 <= element_id < CAPS["element_pool"],
            "packed vector key")
    return element_id * 8 + component - 1


def unpack_vector_key(key: int) -> tuple[int, int]:
    require(isinstance(key, int) and key >= 0 and key % 8 < 6,
            "packed vector key decode")
    return key % 8 + 1, key // 8


class ElementPool:
    """Exact compact interning for all persistent E4 elements."""

    def __init__(self, quotient: MatchedQuotient) -> None:
        self.quotient = quotient
        self.width = quotient.degree + quotient.pc.n
        self.values: list[bytes] = []
        self.ids: dict[bytes, int] = {}
        self.hits = 0
        self.misses = 0
        self.peak = 0
        self.product_cache = BoundedLRU(CAPS["element_product_cache"])
        self.inverse_cache = BoundedLRU(CAPS["element_inverse_cache"])
        self.transaction_rollbacks = 0
        self.transaction_commits = 0
        self.rollback_suffix_removed = 0
        self.max_rollback_suffix = 0
        self.rollback_lru_clears = 0
        self.identity_id = self.intern(quotient.identity)
        self.generator_ids = [self.intern(x) for x in quotient.generators]
        self.inverse_generator_ids = [self.inverse_id(x)
                                      for x in self.generator_ids]

    def pack(self, value: EKey) -> bytes:
        require(len(value[0]) == self.quotient.degree and
                len(value[1]) == self.quotient.pc.n, "element packing width")
        blob = value[0] + value[1]
        require(len(blob) == self.width, "element packed width")
        return blob

    def unpack(self, blob: bytes) -> EKey:
        require(isinstance(blob, bytes) and len(blob) == self.width,
                "canonical packed element")
        return blob[:self.quotient.degree], blob[self.quotient.degree:]

    def intern(self, value: EKey) -> int:
        blob = self.pack(value)
        existing = self.ids.get(blob)
        if existing is not None:
            self.hits += 1
            return existing
        self.misses += 1
        if len(self.values) >= CAPS["element_pool"]:
            raise ResourceStop("element_pool", cap_key="element_pool",
                               cap_limit=CAPS["element_pool"],
                               observed_count=len(self.values),
                               trigger_relation="ge")
        identifier = len(self.values)
        # The same immutable bytes object is retained by the list and dict;
        # no second canonical payload is allocated.
        self.values.append(blob)
        self.ids[blob] = identifier
        self.peak = max(self.peak, len(self.values))
        return identifier

    def blob(self, identifier: int) -> bytes:
        require(0 <= identifier < len(self.values), "element id range")
        return self.values[identifier]

    def value(self, identifier: int) -> EKey:
        return self.unpack(self.blob(identifier))

    def mul_id(self, left: int, right: int) -> int:
        require(0 <= left < len(self.values) and 0 <= right < len(self.values),
                "element product ids")
        key = left * CAPS["element_pool"] + right
        cached = self.product_cache.get(key)
        if cached is not None:
            return int(cached)
        answer = self.intern(self.quotient.mul(self.value(left), self.value(right)))
        self.product_cache.put(key, answer)
        return answer

    def inverse_id(self, identifier: int) -> int:
        require(0 <= identifier < len(self.values), "element inverse id")
        cached = self.inverse_cache.get(identifier)
        if cached is not None:
            return int(cached)
        answer = self.intern(self.quotient.inverse(self.value(identifier)))
        self.inverse_cache.put(identifier, answer)
        return answer

    def eval_id(self, word: Sequence[int], images: Sequence[int] | None = None) -> int:
        marked = self.generator_ids if images is None else images
        out = self.identity_id
        for letter in word:
            require(1 <= abs(letter) <= len(marked), "packed evaluation letter")
            value = marked[abs(letter)-1]
            if letter < 0:
                value = self.inverse_id(value)
            out = self.mul_id(out, value)
        return out

    def pivot_order(self, packed_key: int) -> tuple[int, bytes]:
        component, identifier = unpack_vector_key(packed_key)
        return component, self.blob(identifier)

    def accounting(self) -> dict[str, Any]:
        return {
            "capacity": CAPS["element_pool"],
            "size": len(self.values),
            "peak": self.peak,
            "packed_width_bytes": self.width,
            "packed_payload_bytes": len(self.values) * self.width,
            "hits": self.hits,
            "misses": self.misses,
            "exact_equality": "canonical permutation bytes concatenated with PC-coordinate bytes",
            "canonical_order": "lexicographic canonical packed bytes, identical to EKey=(permutation,PC) tuple order",
            "digest_used_as_equality": False,
            "product_cache": self.product_cache.accounting(),
            "inverse_cache": self.inverse_cache.accounting(),
            "transaction_rollbacks": self.transaction_rollbacks,
            "transaction_commits": self.transaction_commits,
            "rollback_suffix_removed": self.rollback_suffix_removed,
            "max_rollback_suffix": self.max_rollback_suffix,
            "rollback_lru_clears": self.rollback_lru_clears,
        }

    def checkpoint(self) -> int:
        require(len(self.values) == len(self.ids), "element pool checkpoint integrity")
        return len(self.values)

    def rollback(self, checkpoint: int) -> int:
        require(0 <= checkpoint <= len(self.values), "element pool rollback checkpoint")
        removed = len(self.values)-checkpoint
        # Numeric IDs may be reused only after every ID-bearing LRU is empty.
        self.product_cache.clear()
        self.inverse_cache.clear()
        self.rollback_lru_clears += 2
        for identifier in range(len(self.values)-1, checkpoint-1, -1):
            blob = self.values[identifier]
            require(self.ids.get(blob) == identifier,
                    "element pool rollback suffix binding")
            del self.ids[blob]
        del self.values[checkpoint:]
        require(len(self.values) == len(self.ids) == checkpoint,
                "element pool rollback integrity")
        self.transaction_rollbacks += 1
        self.rollback_suffix_removed += removed
        self.max_rollback_suffix = max(self.max_rollback_suffix, removed)
        return removed

    def commit(self, checkpoint: int) -> None:
        require(0 <= checkpoint <= len(self.values), "element pool commit checkpoint")
        self.transaction_commits += 1

    def clear_caches(self) -> None:
        self.product_cache.clear()
        self.inverse_cache.clear()

    def clear_large(self) -> None:
        self.clear_caches()
        self.ids.clear()
        self.values.clear()


class LazySectionSLP:
    """First-seen freely reduced BFS sections as parent plus signed letter."""

    def __init__(self, identity_id: int) -> None:
        self.parent = array("I", [0])
        self.letter = array("b", [0])
        self.last = array("b", [0])
        self.depth = array("I", [0])
        self.by_element: dict[int, int] = {identity_id: 0}
        self.peak = 1

    def append(self, parent: int, letter: int) -> int:
        require(0 <= parent < len(self.parent) and 1 <= abs(letter) <= 6,
                "section SLP append")
        if self.last[parent] == -letter:
            return int(self.parent[parent])
        if len(self.parent) >= CAPS["section_slp_nodes"]:
            raise ResourceStop("section_slp_nodes", cap_key="section_slp_nodes",
                               cap_limit=CAPS["section_slp_nodes"],
                               observed_count=len(self.parent),
                               trigger_relation="ge")
        self.parent.append(parent)
        self.letter.append(letter)
        self.last.append(letter)
        self.depth.append(self.depth[parent] + 1)
        self.peak = max(self.peak, len(self.parent))
        return len(self.parent)-1

    def bind(self, element_id: int, node_id: int) -> None:
        require(element_id not in self.by_element and
                0 <= node_id < len(self.parent), "section binding")
        self.by_element[element_id] = node_id

    def node_for(self, element_id: int) -> int:
        require(element_id in self.by_element, "missing lazy section")
        return self.by_element[element_id]

    def materialize(self, node_id: int) -> list[int]:
        require(0 <= node_id < len(self.parent), "section node range")
        out: list[int] = []
        cursor = node_id
        while cursor:
            out.append(int(self.letter[cursor]))
            cursor = int(self.parent[cursor])
        out.reverse()
        require(len(out) == self.depth[node_id], "section SLP depth")
        return out

    def accounting(self) -> dict[str, Any]:
        return {"capacity": CAPS["section_slp_nodes"],
                "live_nodes": len(self.parent), "peak_nodes": self.peak,
                "bound_elements": len(self.by_element),
                "representation": "parent element-section node plus signed generator letter"}

    def clear(self) -> None:
        self.by_element.clear()
        del self.parent[:]
        del self.letter[:]
        del self.last[:]
        del self.depth[:]


class SectionExpressionDAG:
    """Sparse, canonical-byte-bound section expressions for directed surgery."""

    IDENTITY = 0
    SIGNED_GENERATOR = 1
    PRODUCT = 2
    INVERSE = 3
    FLAT = 4

    def __init__(self, pool: ElementPool) -> None:
        self.pool = pool
        self.kind = bytearray([self.IDENTITY])
        self.signed_generator = array("b", [0])
        self.left = array("I", [0])
        self.right = array("I", [0])
        self.flat_words: list[tuple[int, ...] | None] = [()]
        self.value_blobs: list[bytes] = [pool.blob(pool.identity_id)]
        self.keys: dict[tuple[Any, ...], int] = {("identity",): 0}
        self.roles: dict[int, set[str]] = {0: {"identity"}}
        self.edge_count = 0
        self.peak_nodes = 1
        self.peak_edges = 0

    def _append(self, key: tuple[Any, ...], kind: int, signed: int,
                left: int, right: int, flat: tuple[int, ...] | None,
                value_blob: bytes, edges: int, role: str) -> int:
        old = self.keys.get(key)
        if old is not None:
            require(self.value_blobs[old] == value_blob,
                    "section expression canonical-value deduplication")
            self.roles.setdefault(old, set()).add(role)
            return old
        if len(self.kind) >= CAPS["directed_section_expr_nodes"]:
            raise ResourceStop(
                "directed_section_expr_nodes",
                cap_key="directed_section_expr_nodes",
                cap_limit=CAPS["directed_section_expr_nodes"],
                observed_count=len(self.kind), trigger_relation="ge")
        if self.edge_count + edges > CAPS["directed_section_expr_edges"]:
            raise ResourceStop(
                "directed_section_expr_edges",
                cap_key="directed_section_expr_edges",
                cap_limit=CAPS["directed_section_expr_edges"],
                observed_count=self.edge_count+edges, trigger_relation="gt")
        node = len(self.kind)
        self.keys[key] = node
        self.kind.append(kind)
        self.signed_generator.append(signed)
        self.left.append(left)
        self.right.append(right)
        self.flat_words.append(flat)
        self.value_blobs.append(value_blob)
        self.roles[node] = {role}
        self.edge_count += edges
        self.peak_nodes = max(self.peak_nodes, len(self.kind))
        self.peak_edges = max(self.peak_edges, self.edge_count)
        return node

    def identity(self, role: str = "identity") -> int:
        self.roles[0].add(role)
        return 0

    def generator(self, letter: int, role: str) -> int:
        require(1 <= abs(letter) <= 6, "section expression marked generator")
        value = (self.pool.quotient.generators[abs(letter)-1]
                 if letter > 0 else
                 self.pool.quotient.inverse_generators[abs(letter)-1])
        blob = self.pool.pack(value)
        return self._append(("generator", letter), self.SIGNED_GENERATOR,
                            letter, 0, 0, None, blob, 0, role)

    def flat(self, word: Sequence[int], value_blob: bytes, role: str) -> int:
        reduced = tuple(reduce_word(word))
        require(len(reduced) <= CAPS["single_word_or_section_length"],
                "registered flat section word cap")
        require(self.pool.pack(self.pool.quotient.eval(reduced)) == value_blob,
                "registered flat section direct quotient replay")
        return self._append(("flat", reduced, value_blob), self.FLAT, 0, 0, 0,
                            reduced, value_blob, 0, role)

    def inverse(self, parent: int, role: str) -> int:
        require(0 <= parent < len(self.kind), "section inverse parent")
        value = self.pool.quotient.inverse(
            self.pool.unpack(self.value_blobs[parent]))
        return self._append(("inverse", parent), self.INVERSE, 0, parent, 0,
                            None, self.pool.pack(value), 1, role)

    def product(self, left: int, right: int, role: str) -> int:
        require(0 <= left < len(self.kind) and 0 <= right < len(self.kind),
                "section product parents")
        value = self.pool.quotient.mul(
            self.pool.unpack(self.value_blobs[left]),
            self.pool.unpack(self.value_blobs[right]))
        return self._append(("product", left, right), self.PRODUCT, 0,
                            left, right, None, self.pool.pack(value), 2, role)

    def value_blob(self, node: int) -> bytes:
        require(0 <= node < len(self.kind), "section expression node")
        return self.value_blobs[node]

    def materialize(self, node: int) -> list[int]:
        require(0 <= node < len(self.kind), "section expression materialize node")
        memo: dict[int, list[int]] = {}

        def visit(current: int) -> list[int]:
            if current in memo:
                return memo[current]
            kind = self.kind[current]
            if kind == self.IDENTITY:
                word: list[int] = []
            elif kind == self.SIGNED_GENERATOR:
                word = [int(self.signed_generator[current])]
            elif kind == self.FLAT:
                flat = self.flat_words[current]
                require(flat is not None, "flat section payload")
                word = list(flat)
            elif kind == self.INVERSE:
                word = inverse_word(visit(int(self.left[current])))
            else:
                require(kind == self.PRODUCT, "section expression kind")
                word = reduce_word(visit(int(self.left[current])) +
                                   visit(int(self.right[current])))
            if len(word) > CAPS["single_word_or_section_length"]:
                raise ResourceStop(
                    "single_word_or_section_length",
                    cap_key="single_word_or_section_length",
                    cap_limit=CAPS["single_word_or_section_length"],
                    observed_count=len(word), trigger_relation="gt")
            require(self.pool.pack(self.pool.quotient.eval(word)) ==
                    self.value_blobs[current],
                    "section expression materialization binding")
            memo[current] = word
            return word

        return visit(node)

    def reachable(self, roots: Sequence[int]) -> set[int]:
        pending = list(roots)
        reached: set[int] = set()
        while pending:
            node = pending.pop()
            require(0 <= node < len(self.kind), "section expression root")
            if node in reached:
                continue
            reached.add(node)
            kind = self.kind[node]
            if kind == self.INVERSE:
                pending.append(int(self.left[node]))
            elif kind == self.PRODUCT:
                pending.extend((int(self.left[node]), int(self.right[node])))
        return reached

    def serialize_reachable(self, roots: Sequence[int],
                            monitor: ResourceMonitor | None) \
            -> tuple[dict[str, Any], dict[int, int]]:
        reached = self.reachable(roots)
        ordered = sorted(reached)
        renumber = {old: new for new, old in enumerate(ordered)}
        kinds = bytearray()
        signed = array("b")
        left = array("I")
        right = array("I")
        flat_offsets = array("I", [0])
        flat_letters = array("h")
        values = bytearray()
        for old in ordered:
            kind = self.kind[old]
            kinds.append(kind)
            signed.append(int(self.signed_generator[old]))
            left.append(renumber[int(self.left[old])] if kind in
                        (self.PRODUCT, self.INVERSE) else 0)
            right.append(renumber[int(self.right[old])] if kind == self.PRODUCT else 0)
            flat = self.flat_words[old] if kind == self.FLAT else None
            if flat is not None:
                flat_letters.extend(flat)
            flat_offsets.append(len(flat_letters))
            values.extend(self.value_blobs[old])
        arrays = {
            "kind": _packed_array_block("uint8", "B", kinds,
                                         CAPS["directed_section_expr_nodes"], monitor),
            "signed_generator": _packed_array_block(
                "int8", "b", signed, CAPS["directed_section_expr_nodes"], monitor),
            "left": _packed_array_block("uint32", "I", left,
                                         CAPS["directed_section_expr_nodes"], monitor),
            "right": _packed_array_block("uint32", "I", right,
                                          CAPS["directed_section_expr_nodes"], monitor),
            "flat_offsets": _packed_array_block(
                "uint32", "I", flat_offsets,
                CAPS["directed_section_expr_nodes"]+1, monitor),
            "flat_letters": _packed_array_block(
                "int16", "h", flat_letters,
                CAPS["directed_section_expr_nodes"] *
                CAPS["single_word_or_section_length"], monitor),
            "canonical_values": _packed_array_block(
                "uint8", "B", values,
                CAPS["directed_section_expr_nodes"] * self.pool.width, monitor),
        }
        manifest = {name: {key: value for key, value in block.items()
                           if key != "base64"} for name, block in arrays.items()}
        root_rows = [renumber[root] for root in roots]
        payload = {
            "format": "typed-section-expression-arrays/v1",
            "node_order": "zero_based_topological",
            "ordinary_word_composition": True,
            "canonical_value_width": self.pool.width,
            "node_count": len(ordered),
            "edge_count": sum(1 if self.kind[old] == self.INVERSE else
                              2 if self.kind[old] == self.PRODUCT else 0
                              for old in ordered),
            "roots": root_rows,
            "arrays": arrays,
            "manifest_sha256": digest_obj({"arrays": manifest,
                                             "roots": root_rows}),
        }
        return payload, renumber

    def accounting(self) -> dict[str, Any]:
        return {
            "live_nodes": len(self.kind), "live_edges": self.edge_count,
            "peak_nodes": self.peak_nodes, "peak_edges": self.peak_edges,
            "node_cap": CAPS["directed_section_expr_nodes"],
            "edge_cap": CAPS["directed_section_expr_edges"],
            "canonical_byte_bound": True,
            "role_counts": {
                role: sum(role in roles for roles in self.roles.values())
                for role in sorted({role for roles in self.roles.values()
                                    for role in roles})},
        }

    def clear(self) -> None:
        self.keys.clear()
        self.roles.clear()
        self.flat_words.clear()
        self.value_blobs.clear()
        del self.kind[:]
        del self.signed_generator[:]
        del self.left[:]
        del self.right[:]


class SparseSectionOracle:
    """BFS sections plus sparse canonical bindings for directed translations."""

    EXPR_TAG = 1 << 31

    def __init__(self, pool: ElementPool) -> None:
        self.pool = pool
        self.bfs = LazySectionSLP(pool.identity_id)
        self.expressions = SectionExpressionDAG(pool)
        self.by_blob: dict[bytes, int] = {
            pool.blob(pool.identity_id): 0,
        }
        self.directed_blobs: set[bytes] = set()
        self.directed_roots: dict[bytes, int] = {}
        self.base_prefix_roots: dict[tuple[int, bytes], int] = {}

    @property
    def parent(self) -> array:
        return self.bfs.parent

    @property
    def by_element(self) -> dict[int, int]:
        return self.bfs.by_element

    def append(self, parent: int, letter: int) -> int:
        require(parent < self.EXPR_TAG, "BFS section parent tag")
        return self.bfs.append(parent, letter)

    def bind(self, element_id: int, node_id: int) -> None:
        require(node_id < self.EXPR_TAG, "BFS section bind tag")
        self.bfs.bind(element_id, node_id)
        blob = self.pool.blob(element_id)
        old = self.by_blob.get(blob)
        require(old is None or old == node_id, "BFS canonical section binding")
        self.by_blob[blob] = node_id

    def node_for(self, element_id: int) -> int:
        blob = self.pool.blob(element_id)
        require(blob in self.by_blob, "missing sparse translation section")
        return self.by_blob[blob]

    def materialize(self, node_id: int) -> list[int]:
        if node_id < self.EXPR_TAG:
            return self.bfs.materialize(node_id)
        return self.expressions.materialize(node_id-self.EXPR_TAG)

    def expression_root(self, node_id: int, role: str) -> int:
        if node_id >= self.EXPR_TAG:
            root = node_id-self.EXPR_TAG
            self.expressions.roles.setdefault(root, set()).add(role)
            return root
        word = self.bfs.materialize(node_id)
        value = self.pool.eval_id(word)
        return self.expressions.flat(word, self.pool.blob(value), role)

    def register_base_prefix(self, component: int, blob: bytes,
                             word: Sequence[int]) -> int:
        key = (component, blob)
        root = self.base_prefix_roots.get(key)
        if root is None:
            root = self.expressions.flat(word, blob, "base_D2_prefix")
            self.base_prefix_roots[key] = root
        else:
            require(self.expressions.value_blob(root) == blob,
                    "base prefix canonical binding")
        return root

    def register_directed(self, value: EKey, root: int) \
            -> tuple[int, bool]:
        blob = self.pool.pack(value)
        require(self.expressions.value_blob(root) == blob,
                "directed section expression binding")
        old = self.by_blob.get(blob)
        if old is not None:
            return old, False
        if len(self.directed_blobs) >= CAPS["directed_unique_translations"]:
            raise ResourceStop(
                "directed_unique_translations",
                cap_key="directed_unique_translations",
                cap_limit=CAPS["directed_unique_translations"],
                observed_count=len(self.directed_blobs), trigger_relation="ge")
        element_id = self.pool.intern(value)
        tagged = self.EXPR_TAG + root
        self.by_blob[blob] = tagged
        self.directed_blobs.add(blob)
        self.directed_roots[blob] = root
        require(self.pool.blob(element_id) == blob, "directed element pool binding")
        return tagged, True

    def recover_blocker(self, component: int, blob: bytes,
                        transient: dict[tuple[int, bytes], list[int]],
                        base_occurrences: Sequence[dict[str, Any]]) \
            -> tuple[int, dict[str, Any]]:
        direct = transient.get((component, blob))
        if direct is not None:
            root = self.expressions.flat(direct, blob,
                                         "exported_target_blocker")
            return root, {"method": "target_support_prefix",
                          "component": component, "element_hex": blob.hex()}
        g = self.pool.unpack(blob)
        candidates = [row for row in base_occurrences
                      if row["component"] == component]
        candidates.sort(key=lambda row: (row["relator_index"],
                                         bytes.fromhex(row["element_hex"])))
        for row in candidates:
            h_blob = bytes.fromhex(row["element_hex"])
            h = self.pool.unpack(h_blob)
            t0 = self.pool.quotient.mul(g, self.pool.quotient.inverse(h))
            t0_blob = self.pool.pack(t0)
            registered = self.by_blob.get(t0_blob)
            if registered is None:
                continue
            t0_root = self.expression_root(registered,
                                           "registered_translation_for_blocker")
            h_root = int(row["section_expression_root"])
            root = self.expressions.product(t0_root, h_root,
                                            "recovered_raw_column_blocker")
            require(self.expressions.value_blob(root) == blob,
                    "raw-column blocker recovery value")
            return root, {
                "method": "registered_translation_times_base_prefix",
                "component": component, "element_hex": blob.hex(),
                "relator_index": row["relator_index"],
                "base_element_hex": row["element_hex"],
                "registered_translation_hex": t0_blob.hex(),
            }
        raise Reject("sparse section oracle failed to recover exact blocker")

    def accounting(self) -> dict[str, Any]:
        return {
            "bfs": self.bfs.accounting(),
            "directed_registered": len(self.directed_blobs),
            "canonical_translation_bindings": len(self.by_blob),
            "base_prefix_bindings": len(self.base_prefix_roots),
            "expressions": self.expressions.accounting(),
            "all_pool_elements_have_sections": False,
        }

    def clear(self) -> None:
        self.by_blob.clear()
        self.directed_blobs.clear()
        self.directed_roots.clear()
        self.base_prefix_roots.clear()
        self.bfs.clear()
        self.expressions.clear()


def add_packed_term(vector: PackedSparseVector, key: int, coefficient: int) -> None:
    coefficient %= 3
    if not coefficient:
        return
    value = (vector.get(key, 0) + coefficient) % 3
    if value:
        vector[key] = value
    else:
        vector.pop(key, None)


def fox_gradient_packed(word: Sequence[int], pool: ElementPool) \
        -> tuple[PackedSparseVector, int]:
    prefix = pool.identity_id
    gradient: PackedSparseVector = {}
    for letter in word:
        component = abs(letter)
        require(1 <= component <= len(pool.generator_ids), "packed Fox index")
        if letter > 0:
            add_packed_term(gradient, pack_vector_key(component, prefix), 1)
            prefix = pool.mul_id(prefix, pool.generator_ids[component-1])
        else:
            prefix = pool.mul_id(prefix, pool.inverse_generator_ids[component-1])
            add_packed_term(gradient, pack_vector_key(component, prefix), 2)
    return gradient, prefix


def d1_packed(vector: PackedSparseVector, pool: ElementPool) -> dict[int, int]:
    out: dict[int, int] = {}
    for key, coefficient in vector.items():
        component, element = unpack_vector_key(key)
        add_packed_term(out, pool.mul_id(element, pool.generator_ids[component-1]),
                        coefficient)
        add_packed_term(out, element, -coefficient)
    return out


def translate_vector_packed(vector: PackedSparseVector, translation: int,
                            pool: ElementPool) -> PackedSparseVector:
    out: PackedSparseVector = {}
    for key, coefficient in vector.items():
        component, element = unpack_vector_key(key)
        add_packed_term(out, pack_vector_key(
            component, pool.mul_id(translation, element)), coefficient)
    return out


def intern_raw_vector(vector: SparseVector, pool: ElementPool) -> PackedSparseVector:
    out: PackedSparseVector = {}
    for (component, element), coefficient in vector.items():
        add_packed_term(out, pack_vector_key(component, pool.intern(element)),
                        coefficient)
    return out


class ProvenanceDAG:
    """Packed parallel-array F3 straight-line program."""

    ZERO = 0
    LEAF = 1
    LINEAR = 2

    def __init__(self, deadline: SoftDeadline | None = None) -> None:
        self.kind = bytearray([self.LINEAR])
        self.leaf_relator = array("H", [0])
        self.leaf_translation = array("I", [0])
        self.edge_start = array("I", [0])
        self.edge_length = array("I", [0])
        self.edge_parent = array("I")
        self.edge_coefficient = bytearray()
        self.max_nodes = 1
        self.max_edges = 0
        self.deadline = deadline

    @property
    def node_count(self) -> int:
        return len(self.kind)

    @property
    def edge_count(self) -> int:
        return len(self.edge_parent)

    def checkpoint(self) -> tuple[int, int]:
        return self.node_count, self.edge_count

    def rollback(self, checkpoint: tuple[int, int]) -> None:
        nodes, edges = checkpoint
        require(1 <= nodes <= self.node_count and 0 <= edges <= self.edge_count,
                "packed DAG rollback checkpoint")
        del self.kind[nodes:]
        del self.leaf_relator[nodes:]
        del self.leaf_translation[nodes:]
        del self.edge_start[nodes:]
        del self.edge_length[nodes:]
        del self.edge_parent[edges:]
        del self.edge_coefficient[edges:]

    def _append_node(self, kind: int, relator: int, translation: int,
                     terms: Sequence[tuple[int, int]]) -> int:
        if self.node_count + 1 > CAPS["provenance_dag_nodes"]:
            raise ResourceStop("provenance_dag_nodes",
                               cap_key="provenance_dag_nodes",
                               cap_limit=CAPS["provenance_dag_nodes"],
                               observed_count=self.node_count+1,
                               trigger_relation="gt")
        if self.edge_count + len(terms) > CAPS["provenance_dag_edges"]:
            raise ResourceStop("provenance_dag_edges",
                               cap_key="provenance_dag_edges",
                               cap_limit=CAPS["provenance_dag_edges"],
                               observed_count=self.edge_count+len(terms),
                               trigger_relation="gt")
        start = self.edge_count
        self.kind.append(kind)
        self.leaf_relator.append(relator)
        self.leaf_translation.append(translation)
        self.edge_start.append(start)
        self.edge_length.append(len(terms))
        for parent, coefficient in terms:
            self.edge_parent.append(parent)
            self.edge_coefficient.append(coefficient)
        self.max_nodes = max(self.max_nodes, self.node_count)
        self.max_edges = max(self.max_edges, self.edge_count)
        if self.deadline is not None and (self.node_count & 1023) == 0:
            self.deadline.check("packed_provenance_dag_growth")
        return self.node_count

    def leaf(self, relator_index: int, translation_id: int) -> int:
        require(relator_index >= 1 and translation_id >= 0, "packed DAG leaf")
        return self._append_node(self.LEAF, relator_index, translation_id, [])

    def terms(self, node_id: int) -> list[tuple[int, int]]:
        require(1 <= node_id <= self.node_count, "packed DAG node")
        index = node_id-1
        start = int(self.edge_start[index])
        stop = start + int(self.edge_length[index])
        return [(int(self.edge_parent[i]), int(self.edge_coefficient[i]))
                for i in range(start, stop)]

    def linear(self, terms: Sequence[tuple[int, int]]) -> int:
        merged: dict[int, int] = {}
        for node_id, coefficient in terms:
            require(1 <= node_id <= self.node_count, "packed DAG backward reference")
            if node_id == 1:
                continue
            coefficient %= 3
            if coefficient:
                value = (merged.get(node_id, 0) + coefficient) % 3
                if value:
                    merged[node_id] = value
                else:
                    merged.pop(node_id, None)
        ordered = sorted(merged.items())
        if not ordered:
            return 1
        if len(ordered) == 1 and ordered[0][1] == 1:
            return ordered[0][0]
        return self._append_node(self.LINEAR, 0, 0, ordered)

    def accounting(self) -> dict[str, Any]:
        return {
            "live_nodes": self.node_count, "live_edges": self.edge_count,
            "peak_nodes": self.max_nodes, "peak_edges": self.max_edges,
            "packed_arrays": True,
            "node_payload_bytes": (len(self.kind) + self.leaf_relator.itemsize *
                len(self.leaf_relator) + self.leaf_translation.itemsize *
                len(self.leaf_translation) + self.edge_start.itemsize *
                len(self.edge_start) + self.edge_length.itemsize *
                len(self.edge_length)),
            "edge_payload_bytes": (self.edge_parent.itemsize * len(self.edge_parent) +
                                   len(self.edge_coefficient)),
        }

    def reachable(self, roots: Sequence[int]) -> set[int]:
        pending = list(roots)
        reached: set[int] = set()
        while pending:
            node_id = pending.pop()
            require(1 <= node_id <= self.node_count, "packed DAG reference range")
            if node_id in reached:
                continue
            reached.add(node_id)
            if self.kind[node_id-1] == self.LINEAR:
                pending.extend(parent for parent, _ in self.terms(node_id))
        return reached

    def clear(self) -> None:
        del self.kind[:]
        del self.leaf_relator[:]
        del self.leaf_translation[:]
        del self.edge_start[:]
        del self.edge_length[:]
        del self.edge_parent[:]
        del self.edge_coefficient[:]


class SparseBoundaryBasis:
    def __init__(self, pool: ElementPool,
                 relator_columns: list[PackedSparseVector], dag: ProvenanceDAG,
                 sections: SparseSectionOracle,
                 deadline: SoftDeadline | None = None) -> None:
        self.pool = pool
        self.relator_columns = relator_columns
        self.dag = dag
        self.sections = sections
        self.deadline = deadline
        self.rows: dict[int, tuple[PackedSparseVector, int]] = {}
        self.columns_seen = 0
        self.dependent_columns = 0
        self.max_vector_support = 0
        self.max_transient_vector_support = 0
        self.live_vector_entries = 0
        self.elimination_operations = 0
        self.blocker_watches: set[tuple[int, bytes]] = set()
        self.pivot_introductions: list[dict[str, Any]] = []

    def pivot(self, vector: PackedSparseVector) -> int:
        # Never use insertion-order element IDs: this is exactly v2's
        # (component,EKey) canonical order.
        return min(vector, key=self.pool.pivot_order)

    def _resource_gate(self) -> None:
        if self.live_vector_entries > CAPS["total_sparse_group_ring_keys"]:
            raise ResourceStop(
                "total_sparse_group_ring_keys",
                cap_key="total_sparse_group_ring_keys",
                cap_limit=CAPS["total_sparse_group_ring_keys"],
                observed_count=self.live_vector_entries,
                trigger_relation="gt")
        if len(self.rows) > CAPS["sparse_pivot_rows"]:
            raise ResourceStop(
                "sparse_pivot_rows", cap_key="sparse_pivot_rows",
                cap_limit=CAPS["sparse_pivot_rows"],
                observed_count=len(self.rows), trigger_relation="gt")

    def accounting(self) -> dict[str, Any]:
        return {
            "live_sparse_vector_entries": self.live_vector_entries,
            "pivot_count": len(self.rows),
            "max_pivot_vector_support": self.max_vector_support,
            "max_transient_vector_support": self.max_transient_vector_support,
            "elimination_operations": self.elimination_operations,
            "dag": self.dag.accounting(),
            "element_pool": self.pool.accounting(),
            "lazy_sections": self.sections.accounting(),
            "blocker_watch_count": len(self.blocker_watches),
            "matching_pivot_introduction_count": len(self.pivot_introductions),
        }

    def _cadence(self, phase_name: str) -> None:
        self.elimination_operations += 1
        if self.deadline is not None and (self.elimination_operations & 1023) == 0:
            self.deadline.check(phase_name)

    def watch_blocker(self, component: int, blob: bytes) -> None:
        require(1 <= component <= 6 and isinstance(blob, bytes) and
                len(blob) == self.pool.width, "blocker watch")
        self.blocker_watches.add((component, blob))

    def add_column(self, relator_index: int, translation_id: int,
                   section_node: int, translation_ordinal: int = 0) -> None:
        require(self.sections.node_for(translation_id) == section_node,
                "translation/section binding")
        checkpoint = self.dag.checkpoint()
        vector = translate_vector_packed(
            self.relator_columns[relator_index-1], translation_id, self.pool)
        node_id = self.dag.leaf(relator_index, translation_id)
        try:
            while vector:
                self.max_transient_vector_support = max(
                    self.max_transient_vector_support, len(vector))
                if len(vector) > CAPS["total_sparse_group_ring_keys"]:
                    raise ResourceStop(
                        "single_sparse_elimination_row",
                        cap_key="single_sparse_elimination_row",
                        cap_limit=CAPS["single_sparse_elimination_row"],
                        observed_count=len(vector), trigger_relation="gt")
                pivot = self.pivot(vector)
                if pivot not in self.rows:
                    coefficient = vector[pivot]
                    factor = 1 if coefficient == 1 else 2
                    vector = scaled(vector, factor)
                    node_id = self.dag.linear([(node_id, factor)])
                    if self.live_vector_entries + len(vector) > \
                            CAPS["total_sparse_group_ring_keys"]:
                        raise ResourceStop(
                            "total_sparse_group_ring_keys",
                            cap_key="total_sparse_group_ring_keys",
                            cap_limit=CAPS["total_sparse_group_ring_keys"],
                            observed_count=self.live_vector_entries + len(vector),
                            trigger_relation="gt")
                    if len(self.rows) + 1 > CAPS["sparse_pivot_rows"]:
                        raise ResourceStop(
                            "sparse_pivot_rows", cap_key="sparse_pivot_rows",
                            cap_limit=CAPS["sparse_pivot_rows"],
                            observed_count=len(self.rows)+1,
                            trigger_relation="gt")
                    self.rows[pivot] = (vector, node_id)
                    self.live_vector_entries += len(vector)
                    self.max_vector_support = max(self.max_vector_support, len(vector))
                    component, element_id = unpack_vector_key(pivot)
                    blob = self.pool.blob(element_id)
                    if (component, blob) in self.blocker_watches:
                        self.pivot_introductions.append({
                            "component": component,
                            "element_hex": blob.hex(),
                            "translation_ordinal": translation_ordinal,
                            "relator_index": relator_index,
                        })
                    self.columns_seen += 1
                    self._resource_gate()
                    return
                coefficient = vector[pivot]
                basis_vector, basis_node = self.rows[pivot]
                add_scaled(vector, basis_vector, -coefficient)
                node_id = self.dag.linear([(node_id, 1),
                                           (basis_node, -coefficient)])
                self._cadence("packed_pivot_column_elimination")
            self.dag.rollback(checkpoint)
            self.columns_seen += 1
            self.dependent_columns += 1
        except Exception:
            self.dag.rollback(checkpoint)
            raise

    def solve_with_blocker(self, target: PackedSparseVector) \
            -> tuple[int | None, int | None]:
        checkpoint = self.dag.checkpoint()
        vector = dict(target)
        answer_node = 1
        try:
            while vector:
                self.max_transient_vector_support = max(
                    self.max_transient_vector_support, len(vector))
                pivot = self.pivot(vector)
                row = self.rows.get(pivot)
                if row is None:
                    self.dag.rollback(checkpoint)
                    return None, pivot
                coefficient = vector[pivot]
                add_scaled(vector, row[0], -coefficient)
                answer_node = self.dag.linear([(answer_node, 1),
                                               (row[1], coefficient)])
                if len(vector) > CAPS["total_sparse_group_ring_keys"]:
                    raise ResourceStop(
                        "target_elimination_support",
                        cap_key="target_elimination_support",
                        cap_limit=CAPS["target_elimination_support"],
                        observed_count=len(vector), trigger_relation="gt")
                self._cadence("packed_target_sparse_elimination")
            return answer_node, None
        except Exception:
            self.dag.rollback(checkpoint)
            raise

    def solve(self, target: PackedSparseVector) -> int | None:
        root, _ = self.solve_with_blocker(target)
        return root

    def clear(self) -> None:
        self.rows.clear()
        self.relator_columns.clear()
        self.blocker_watches.clear()
        self.pivot_introductions.clear()


def translation_bfs(pool: ElementPool, sections: SparseSectionOracle, cap: int) \
        -> Iterator[tuple[int, int]]:
    steps = list(zip(range(1, 7), pool.generator_ids)) + \
        list(zip(range(-1, -7, -1), pool.inverse_generator_ids))
    seen = {pool.identity_id}
    queue: deque[int] = deque([pool.identity_id])
    while queue and len(seen) <= cap:
        element_id = queue.popleft()
        section_node = sections.node_for(element_id)
        yield element_id, section_node
        if len(seen) == cap:
            continue
        for letter, step_id in steps:
            value_id = pool.mul_id(element_id, step_id)
            if value_id not in seen:
                seen.add(value_id)
                child = sections.append(section_node, letter)
                sections.bind(value_id, child)
                queue.append(value_id)
                if len(seen) == cap:
                    break


def packed_fox_model(rank: int, pool: ElementPool) -> dict[str, Any]:
    require(rank == pool.quotient.rank, "packed Fox rank")
    relations = pure_relations(rank)
    columns: list[PackedSparseVector] = []
    for relator in relations:
        gradient, value = fox_gradient_packed(relator, pool)
        require(value == pool.identity_id, f"PB{rank} packed relator quotient image")
        require(d1_packed(gradient, pool) == {}, f"PB{rank} packed D1D2")
        columns.append(gradient)
    return {"rank": rank, "relations": relations, "columns": columns,
            "D1D2_zero": True}


def fox_model(rank: int, quotient: MatchedQuotient) -> dict[str, Any]:
    relators = pure_relations(rank)
    columns: list[SparseVector] = []
    sections: list[dict[EKey, list[int]]] = []
    for relator in relators:
        gradient, value, support_sections = fox_gradient(relator, quotient)
        require(value == quotient.identity, f"PB{rank} relator quotient image")
        require(d1(gradient, quotient) == {}, f"PB{rank} D1D2")
        columns.append(gradient)
        sections.append(support_sections)
    return {"rank": rank, "relations": relators, "columns": columns,
            "sections": sections, "D1D2_zero": True}


def freeze_base_support_occurrences(model4: dict[str, Any],
                                    pool: ElementPool,
                                    sections: SparseSectionOracle) \
        -> list[dict[str, Any]]:
    """Canonical nonzero PB4 D2 occurrences with exact prefix sections."""
    rows: list[dict[str, Any]] = []
    for relator_index, (gradient, support_sections) in enumerate(
            zip(model4["columns"], model4["sections"]), 1):
        ordered = sorted(gradient.items(),
                         key=lambda item: (item[0][0], pool.pack(item[0][1])))
        for (component, value), coefficient in ordered:
            blob = pool.pack(value)
            require(value in support_sections and coefficient in (1, 2),
                    "base D2 support section/coefficient")
            word = support_sections[value]
            root = sections.register_base_prefix(component, blob, word)
            rows.append({
                "relator_index": relator_index,
                "component": component,
                "coefficient": coefficient,
                "element_hex": blob.hex(),
                "section_word": list(word),
                "section_expression_root": root,
                "_value": value,
            })
    require(rows == sorted(rows, key=lambda row: (
        row["relator_index"], row["component"],
        bytes.fromhex(row["element_hex"]))), "base occurrence canonical order")
    return rows


def public_base_occurrences(rows: Sequence[dict[str, Any]]) \
        -> list[dict[str, Any]]:
    return [{key: value for key, value in row.items()
             if not key.startswith("_") and
             key != "section_expression_root"}
            for row in rows]


def remap_expression_root_fields(value: Any,
                                 renumber: dict[int, int]) -> Any:
    if isinstance(value, list):
        return [remap_expression_root_fields(row, renumber) for row in value]
    if isinstance(value, dict):
        out: dict[str, Any] = {}
        for key, item in value.items():
            if key in {"section_expression_root",
                       "blocker_section_expression_root"}:
                require(isinstance(item, int) and item in renumber,
                        "section expression receipt root")
                out[key] = renumber[item]
            else:
                out[key] = remap_expression_root_fields(item, renumber)
        return out
    return value


###############################################################################
# Frozen q=3 reconstruction and base-gate replay.
###############################################################################


def marked_pc(receipt: dict[str, Any]) -> list[Pc]:
    pc = PcCollector(receipt)
    return [pc.coord(row["coords"]) for row in receipt["marked_generators"]]


def reconstruct_quotients(data: dict[str, Any]) \
        -> tuple[MatchedQuotient, MatchedQuotient, dict[str, Any]]:
    pc3 = PcCollector(data["groups"]["PB3"])
    pc4 = PcCollector(data["groups"]["PB4"])
    p3 = [pc3.coord(row["coords"]) for row in
          data["groups"]["PB3"]["marked_generators"]]
    p4 = [pc4.coord(row["coords"]) for row in
          data["groups"]["PB4"]["marked_generators"]]
    q0_model = data["coarse_models"]["Q0"]
    q4_model = data["coarse_models"]["Q4"]
    q0 = [perm_from_row(row, q0_model["degree"])
          for row in q0_model["marked_permutations"]]
    q4 = [perm_from_row(row, q4_model["degree"])
          for row in q4_model["marked_permutations"]]
    require(len(q0) == 2 and len(q4) == 6, "coarse marked widths")
    # In the m=0 PB3 source, A13 is z=(A23*A12)^-1, exactly the hexagon z.
    q0z = perm_inv(perm_mul(q0[1], q0[0]))
    e3 = MatchedQuotient(3, q0_model["degree"], pc3,
                         [(q0[0], p3[0]), (q0z, p3[1]), (q0[1], p3[2])])
    e4 = MatchedQuotient(4, q4_model["degree"], pc4,
                         list(zip(q4, p4)))
    for rank, quotient in ((3, e3), (4, e4)):
        require(all(quotient.eval(r) == quotient.identity for r in pure_relations(rank)),
                f"PB{rank} matched presentation")
    return e3, e4, {"pc3": pc3, "pc4": pc4, "q0": q0, "q4": q4}


def replay_base_q3(data: dict[str, Any], e3: MatchedQuotient,
                   e4: MatchedQuotient) -> dict[str, Any]:
    require(data["schema"] == Q3_SCHEMA and
            data["terminal_token"] ==
            "B345_Q3_TYPED_SIGN_EXACT_WITH_WORD_CORRECTION",
            "frozen q3 terminal")
    selected = data["selected_solution"]
    require(selected == data["direct_word_scan"]["solutions"][0] and
            data["direct_word_scan"]["solution_count"] == 1,
            "frozen q3 selected solution")
    require(selected["typed_source_word"] == FIXED_WORD and
            selected["correction_word"] == [] and
            selected["correction_index"] == 1 and selected["exponent"] == 2,
            "fixed outside word/empty correction")
    require(exponent_sums(FIXED_WORD, 2) == [0, 0], "fixed word abelianization")
    hex_words = hexagon_words(FIXED_WORD)
    hex_pb3 = [embed_f2_pb3(w) for w in hex_words]
    hex_values = [e3.eval(w) for w in hex_pb3]
    require(hex_values == [e3.identity, e3.identity], "base q3 hexagon replay")
    pent = pentagon_word(FIXED_WORD)
    require(e4.eval(pent) == e4.identity, "base q3 pentagon replay")
    derived = derived_commutator_ledger(FIXED_WORD)

    models = data["coarse_models"]
    p_rows = [perm_from_row(row, models["P"]["degree"])
              for row in models["P"]["marked_permutations"]]
    g_rows = [perm_from_row(row, models["G9"]["degree"])
              for row in models["G9"]["marked_permutations"]]
    p_one, g_one = perm_one(9), perm_one(27)
    f_p = eval_perm_word(FIXED_WORD, p_rows)
    f_g = eval_perm_word(FIXED_WORD, g_rows)
    p_onto = len(enumerate_generated(
        p_one, [p_rows[0], paper_conjugate(f_p, p_rows[1], p_one,
                                            perm_mul, perm_inv)],
        perm_mul, perm_inv, 504)) == 504
    g_onto = len(enumerate_generated(
        g_one, [g_rows[0], paper_conjugate(f_g, g_rows[1], g_one,
                                            perm_mul, perm_inv)],
        perm_mul, perm_inv, 2916)) == 2916
    b2 = [e3.generators[0][1], e3.generators[2][1]]
    f_b = e3.pc.eval(FIXED_WORD, b2)
    b_onto = len(enumerate_generated(
        e3.pc.one(), [b2[0], paper_conjugate(f_b, b2[1], e3.pc.one(),
                                              e3.pc.mul, e3.pc.inverse)],
        e3.pc.mul, e3.pc.inverse, 27)) == 27
    require(p_onto and g_onto and b_onto, "base q3 onto replay")
    q0_value = eval_perm_word(FIXED_WORD,
                              [e3.generators[0][0], e3.generators[2][0]])
    require(perm_order(q0_value) == 9 and selected["roof_reduction_exact"] is True,
            "outside roof/order replay")
    settlement = selected["settlement"]
    source = source_words_m0(FIXED_WORD)
    require(settlement["source_words"] == source and
            settlement["Q4_bijective"] is True and
            settlement["Pi4_q3_bijective"] is True,
            "base settled map binding")
    require([e4.eval(w) for w in source] != [], "source map evaluation")
    return {
        "fixed_word": FIXED_WORD,
        "roof_exponent": 2,
        "roof_order": 9,
        "arithmetic_outside_by_index_three": True,
        "marking_m": 0,
        "lambda": 1,
        "hexagon_residual_words_F2": hex_words,
        "pentagon_residual_word_PB4": pent,
        "derived_membership": derived,
        "onto_small_factors": {"P_order_504": p_onto,
                                 "G9_order_2916": g_onto,
                                 "B2_order_27": b_onto},
        "settled_source_words": source,
        "replayed_not_copied": True,
    }


def correction_dictionary(data: dict[str, Any], e3: MatchedQuotient) -> dict[str, Any]:
    base_words = [reduce_word(row["word"] * 3)
                  for row in data["correction_fibre"]["records"]
                  if row["word"]]
    base_words = list(dict.fromkeys(tuple(w) for w in base_words))
    seeds: list[list[int]] = []
    for raw in base_words:
        k = list(raw)
        require(e3.eval(embed_f2_pb3(k)) == e3.identity,
                "authenticated cube is not in H3")
        for generator in ([1], [2]):
            for word in (commutator(k, generator), commutator(generator, k)):
                if word and exponent_sums(word, 2) == [0, 0] and word not in seeds:
                    require(e3.eval(embed_f2_pb3(word)) == e3.identity,
                            "commutator correction is not H3")
                    seeds.append(word)
    # Complete preregistered shortlex-by-construction universe.  Only
    # exponent-zero H3 words are admitted, so every candidate has an explicit
    # free-derived representative; this is a bounded positive lane, not a
    # completeness claim for all H3 corrections.
    words: list[list[int]] = [[]]
    parent_indices = [0]
    signed_seed_edges = [0]
    seen = {()}
    queue: deque[int] = deque([1])
    signed_steps = [(index+1, word) for index, word in enumerate(seeds)] + [
        (-(index+1), inv_word(word)) for index, word in enumerate(seeds)]
    # Seed authentication plus the homomorphism/closure recurrence is an exact
    # E3-kernel proof for every descendant; no long descendant is re-evaluated.
    require(all(e3.eval(embed_f2_pb3(word)) == e3.identity for word in seeds),
            "dictionary seed E3 kernel")
    while queue and len(words) < CAPS["candidate_correction_dictionary"]:
        parent_index = queue.popleft()
        prefix = words[parent_index-1]
        for signed_edge, step in signed_steps:
            word = reduce_word(prefix + step)
            key = tuple(word)
            if key not in seen:
                require(exponent_sums(word, 2) == [0, 0],
                        "dictionary free-derived invariant")
                seen.add(key)
                words.append(word)
                parent_indices.append(parent_index)
                signed_seed_edges.append(signed_edge)
                queue.append(len(words))
                if len(words) == CAPS["candidate_correction_dictionary"]:
                    break
    for index in range(1, len(words)):
        parent = parent_indices[index]
        edge = signed_seed_edges[index]
        step = seeds[abs(edge)-1]
        if edge < 0:
            step = inv_word(step)
        require(1 <= parent <= index and
                reduce_word(words[parent-1]+step) == words[index] and
                exponent_sums(words[index], 2) == [0, 0],
                "dictionary parent/edge reconstruction")
    provenance = {
        "parent_indices": parent_indices,
        "signed_seed_edges": signed_seed_edges,
        "word_sha256": [digest_obj(word) for word in words],
    }
    return {
        "order": "identity, then breadth-first products of authenticated H3 commutator seeds and inverses",
        "source": "commutators with cubes of the frozen 27-word coarse-trivial exponent-three fibre",
        "words": words,
        "count": len(words),
        "cap": CAPS["candidate_correction_dictionary"],
        "all_words_in_H3": True,
        "all_words_in_coarse_J_H": True,
        "all_words_free_exponent_zero": True,
        "not_complete_for_all_H3": True,
        "membership_in_finer_J_Phi_required": False,
        "J_Phi_cosets_are_the_lift_freedom": True,
        "seed_words": seeds,
        "parent_indices": parent_indices,
        "signed_seed_edges": signed_seed_edges,
        "identity_parent_edge": [0, 0],
        "all_parent_edges_reconstructed": True,
        "E3_kernel_proof": "identity plus authenticated kernel seeds, inverse/product closure",
        "all_words_E3_kernel_by_recurrence": True,
        "provenance_sha256": digest_obj(provenance),
    }


def quotient_product(quotient: MatchedQuotient,
                     values: Sequence[EKey]) -> EKey:
    out = quotient.identity
    for value in values:
        out = quotient.mul(out, value)
    return out


def quotient_paper_product(quotient: MatchedQuotient,
                           values: Sequence[EKey]) -> EKey:
    return quotient_product(quotient, list(reversed(values)))


def cheap_candidate_bad(candidate: Sequence[int], correction: Sequence[int],
                        e4: MatchedQuotient) -> list[str]:
    """Evaluate the fixed literal equations without expanding substituted words."""
    coarse_bad: list[str] = []
    hex1_bad: list[str] = []
    hex2_bad: list[str] = []
    for slot, mapping in enumerate(cofaces(3)):
        x = e4.eval(mapping[0])
        y = e4.eval(mapping[2])
        if e4.eval(correction, [x, y]) != e4.identity:
            coarse_bad.append(f"correction_coarse_J_H_coface_{slot}")
        z = e4.inverse(quotient_paper_product(e4, [x, y]))
        u = e4.inverse(quotient_paper_product(e4, [y, x]))
        fxy = e4.eval(candidate, [x, y])
        fxz = e4.eval(candidate, [x, z])
        fyz = e4.eval(candidate, [y, z])
        fux = e4.eval(candidate, [u, x])
        fuy = e4.eval(candidate, [u, y])
        h1 = quotient_paper_product(
            e4, [fxy, e4.inverse(fxz), fyz])
        h2 = quotient_paper_product(
            e4, [e4.inverse(fux), e4.inverse(fxy), fuy])
        if h1 != e4.identity:
            hex1_bad.append(f"hexagon_1_coface_{slot}")
        if h2 != e4.identity:
            hex2_bad.append(f"hexagon_2_coface_{slot}")

    bad = coarse_bad + hex1_bad + hex2_bad

    g = e4.generators
    contexts = [
        [g[0], g[3]],
        [g[3], g[5]],
        [quotient_paper_product(e4, [g[1], g[3]]), g[5]],
        [quotient_paper_product(e4, [g[0], g[1]]),
         quotient_paper_product(e4, [g[4], g[5]])],
        [g[0], quotient_paper_product(e4, [g[3], g[4]])],
    ]
    parts = [e4.eval(candidate, context) for context in contexts]
    pent = quotient_paper_product(
        e4, [e4.inverse(quotient_paper_product(e4, [parts[4], parts[2]])),
             parts[1], parts[3], parts[0]])
    if pent != e4.identity:
        bad.append("ordered_A18_pentagon")

    ff = e4.eval(candidate, [g[0], g[3]])
    gv = e4.eval(candidate, [g[0], g[1]])
    gs = e4.eval(candidate, [g[3], g[4]])
    f1234 = e4.eval(candidate, [quotient_product(e4, [g[3], g[1]]), g[5]])
    h = e4.eval(candidate, [quotient_product(e4, [g[1], g[0]]), g[2]])
    middle = e4.eval(candidate, [quotient_product(e4, [g[1], g[0]]),
                                 quotient_product(e4, [g[5], g[4]])])
    source = [
        g[0],
        quotient_product(e4, [e4.inverse(gv), g[1], gv]),
        quotient_product(e4, [e4.inverse(ff), e4.inverse(h), g[2], h, ff]),
        quotient_product(e4, [e4.inverse(ff), g[3], ff]),
        quotient_product(e4, [e4.inverse(ff), e4.inverse(middle),
                              e4.inverse(gs), g[4], gs, middle, ff]),
        quotient_product(e4, [e4.inverse(f1234), g[5], f1234]),
    ]
    for index, relator in enumerate(pure_relations(4), 1):
        if e4.eval(relator, source) != e4.identity:
            bad.append(f"S_relation_{index}")
    return bad


def _element_blob(value: EKey) -> bytes:
    return value[0] + value[1]


def cheap_context_registry(e4: MatchedQuotient) \
        -> tuple[list[tuple[EKey, EKey]], dict[str, int], dict[str, Any]]:
    """All fixed two-generator uses in the frozen cheap predicate."""
    contexts: list[tuple[EKey, EKey]] = []
    exact_ids: dict[tuple[EKey, EKey], int] = {}
    named: list[dict[str, Any]] = []
    by_name: dict[str, int] = {}

    def add(name: str, left: EKey, right: EKey) -> None:
        require(name not in by_name, "duplicate cheap context use")
        pair = (left, right)
        context_id = exact_ids.get(pair)
        if context_id is None:
            context_id = len(contexts)+1
            exact_ids[pair] = context_id
            contexts.append(pair)
        by_name[name] = context_id
        named.append({"name": name, "context_id": context_id})

    for slot, mapping in enumerate(cofaces(3)):
        x = e4.eval(mapping[0])
        y = e4.eval(mapping[2])
        z = e4.inverse(quotient_paper_product(e4, [x, y]))
        u = e4.inverse(quotient_paper_product(e4, [y, x]))
        add(f"correction_coface_{slot}", x, y)
        add(f"hexagon_1_fxy_{slot}", x, y)
        add(f"hexagon_1_fxz_{slot}", x, z)
        add(f"hexagon_1_fyz_{slot}", y, z)
        add(f"hexagon_2_fux_{slot}", u, x)
        add(f"hexagon_2_fxy_{slot}", x, y)
        add(f"hexagon_2_fuy_{slot}", u, y)

    g = e4.generators
    pentagon_contexts = [
        (g[0], g[3]),
        (g[3], g[5]),
        (quotient_paper_product(e4, [g[1], g[3]]), g[5]),
        (quotient_paper_product(e4, [g[0], g[1]]),
         quotient_paper_product(e4, [g[4], g[5]])),
        (g[0], quotient_paper_product(e4, [g[3], g[4]])),
    ]
    for index, pair in enumerate(pentagon_contexts):
        add(f"pentagon_part_{index}", pair[0], pair[1])

    source_contexts = [
        ("source_ff", g[0], g[3]),
        ("source_g", g[0], g[1]),
        ("source_gs", g[3], g[4]),
        ("source_f1234", quotient_product(e4, [g[3], g[1]]), g[5]),
        ("source_h", quotient_product(e4, [g[1], g[0]]), g[2]),
        ("source_middle", quotient_product(e4, [g[1], g[0]]),
         quotient_product(e4, [g[5], g[4]])),
    ]
    for name, left, right in source_contexts:
        add(name, left, right)

    require(len(contexts) <= CAPS["cheap_contexts"], "cheap context cap")
    context_rows = [{
        "context_id": index,
        "left_hex": _element_blob(pair[0]).hex(),
        "right_hex": _element_blob(pair[1]).hex(),
    } for index, pair in enumerate(contexts, 1)]
    public = {
        "context_count": len(contexts),
        "contexts": context_rows,
        "named_uses": named,
        "named_use_count": len(named),
        "named_use_mapping_sha256": digest_obj(named),
        "context_rows_sha256": digest_obj(context_rows),
        "deduplication": "exact E4 pair equality",
    }
    return contexts, by_name, public


def _set_bit(bits: bytearray, index: int) -> None:
    bits[index // 8] |= 1 << (index % 8)


def _cheap_bad_from_dp(index: int, correction_values: list[list[EKey]],
                       base_values: list[EKey], by_name: dict[str, int],
                       e4: MatchedQuotient) -> list[str]:
    def correction(name: str) -> EKey:
        return correction_values[by_name[name]-1][index]

    def candidate(name: str) -> EKey:
        context = by_name[name]-1
        return e4.mul(base_values[context], correction_values[context][index])

    coarse_bad: list[str] = []
    hex1_bad: list[str] = []
    hex2_bad: list[str] = []
    for slot in range(5):
        if correction(f"correction_coface_{slot}") != e4.identity:
            coarse_bad.append(f"correction_coarse_J_H_coface_{slot}")
        fxy = candidate(f"hexagon_1_fxy_{slot}")
        fxz = candidate(f"hexagon_1_fxz_{slot}")
        fyz = candidate(f"hexagon_1_fyz_{slot}")
        fux = candidate(f"hexagon_2_fux_{slot}")
        fxy2 = candidate(f"hexagon_2_fxy_{slot}")
        fuy = candidate(f"hexagon_2_fuy_{slot}")
        h1 = quotient_paper_product(e4, [fxy, e4.inverse(fxz), fyz])
        h2 = quotient_paper_product(e4, [e4.inverse(fux),
                                         e4.inverse(fxy2), fuy])
        if h1 != e4.identity:
            hex1_bad.append(f"hexagon_1_coface_{slot}")
        if h2 != e4.identity:
            hex2_bad.append(f"hexagon_2_coface_{slot}")
    bad = coarse_bad + hex1_bad + hex2_bad

    parts = [candidate(f"pentagon_part_{i}") for i in range(5)]
    pent = quotient_paper_product(
        e4, [e4.inverse(quotient_paper_product(e4, [parts[4], parts[2]])),
             parts[1], parts[3], parts[0]])
    if pent != e4.identity:
        bad.append("ordered_A18_pentagon")

    g = e4.generators
    ff = candidate("source_ff")
    gv = candidate("source_g")
    gs = candidate("source_gs")
    f1234 = candidate("source_f1234")
    h = candidate("source_h")
    middle = candidate("source_middle")
    source = [
        g[0],
        quotient_product(e4, [e4.inverse(gv), g[1], gv]),
        quotient_product(e4, [e4.inverse(ff), e4.inverse(h), g[2], h, ff]),
        quotient_product(e4, [e4.inverse(ff), g[3], ff]),
        quotient_product(e4, [e4.inverse(ff), e4.inverse(middle),
                              e4.inverse(gs), g[4], gs, middle, ff]),
        quotient_product(e4, [e4.inverse(f1234), g[5], f1234]),
    ]
    for relator_index, relator in enumerate(pure_relations(4), 1):
        if e4.eval(relator, source) != e4.identity:
            bad.append(f"S_relation_{relator_index}")
    return bad


def fixed_context_cheap_dp(dictionary: dict[str, Any], e4: MatchedQuotient,
                           monitor: ResourceMonitor,
                           prefix: dict[str, Any]) \
        -> tuple[dict[str, Any], list[list[str]]]:
    phase_start = time.monotonic()
    before = e4.pc.cache_accounting()
    contexts, by_name, context_public = cheap_context_registry(e4)
    seeds = dictionary["seed_words"]
    signed_steps = [(index+1, word) for index, word in enumerate(seeds)] + [
        (-(index+1), inv_word(word)) for index, word in enumerate(seeds)]
    signed_lookup = {edge: word for edge, word in signed_steps}
    seed_images: list[dict[int, EKey]] = []
    seed_digest = hashlib.sha256()
    for context_index, (left, right) in enumerate(contexts, 1):
        row: dict[int, EKey] = {}
        for edge, word in signed_steps:
            value = e4.eval(word, [left, right])
            row[edge] = value
            seed_digest.update(context_index.to_bytes(2, "little"))
            seed_digest.update(int(edge).to_bytes(2, "little", signed=True))
            seed_digest.update(_element_blob(value))
        seed_images.append(row)
    require(set(signed_lookup) == set(seed_images[0]), "signed seed image domain")

    parents = dictionary["parent_indices"]
    edges = dictionary["signed_seed_edges"]
    word_count = len(dictionary["words"])
    correction_values: list[list[EKey]] = []
    propagated_digest = hashlib.sha256()
    for context_index, _ in enumerate(contexts):
        values = [e4.identity]
        propagated_digest.update(_element_blob(e4.identity))
        for word_index in range(1, word_count):
            parent = parents[word_index]-1
            edge = edges[word_index]
            require(0 <= parent < word_index and edge in signed_lookup,
                    "cheap DP parent/edge")
            value = e4.mul(values[parent], seed_images[context_index][edge])
            values.append(value)
            propagated_digest.update(_element_blob(value))
        correction_values.append(values)
    base_values = [e4.eval(FIXED_WORD, list(context)) for context in contexts]

    failures: list[list[str]] = []
    survivors: list[int] = []
    gate_bits: dict[str, bytearray] = {}
    gate_counts: dict[str, int] = {}
    evaluated_prefix_digest = hashlib.sha256()
    survivor_prefix_digest = hashlib.sha256()
    prefix["cheap"]["current_candidate"] = 1
    for zero_index in range(word_count):
        monitor.check("fixed_context_cheap_DP")
        bad = _cheap_bad_from_dp(zero_index, correction_values, base_values,
                                 by_name, e4)
        failures.append(bad)
        if not bad:
            survivors.append(zero_index+1)
            survivor_prefix_digest.update((zero_index+1).to_bytes(4, "little"))
        for gate in bad:
            bits = gate_bits.setdefault(gate, bytearray((word_count+7)//8))
            _set_bit(bits, zero_index)
            gate_counts[gate] = gate_counts.get(gate, 0)+1
        prefix["cheap"]["evaluated"] = zero_index+1
        evaluated_prefix_digest.update(
            canonical_bytes([zero_index+1, bad]) + b"\n")
        prefix["cheap"]["survivor_count"] = len(survivors)
        prefix["cheap"]["survivor_indices_sha256"] = digest_obj(survivors)
        prefix["cheap"]["evaluated_prefix_sha256"] = \
            evaluated_prefix_digest.hexdigest()
        prefix["cheap"]["survivor_prefix_sha256"] = \
            survivor_prefix_digest.hexdigest()
        prefix["cheap"]["current_candidate"] = zero_index+2 \
            if zero_index+1 < word_count else None
    all_gate_names = [f"correction_coarse_J_H_coface_{i}" for i in range(5)] + \
        [f"hexagon_1_coface_{i}" for i in range(5)] + \
        [f"hexagon_2_coface_{i}" for i in range(5)] + \
        ["ordered_A18_pentagon"] + \
        [f"S_relation_{i}" for i in range(1, 12)]
    bitset_rows = []
    for gate in all_gate_names:
        raw = bytes(gate_bits.get(gate, bytearray((word_count+7)//8)))
        bitset_rows.append({
            "gate": gate,
            "failure_count": gate_counts.get(gate, 0),
            "byte_length": len(raw),
            "sha256": hashlib.sha256(raw).hexdigest(),
            "base64": base64.b64encode(raw).decode("ascii"),
        })
    failure_digest = digest_obj([[i+1, row] for i, row in enumerate(failures)])
    survivor_digest = digest_obj(survivors)
    prefix["cheap"].update({
        "completed": True, "survivor_count": len(survivors),
        "survivor_indices_sha256": survivor_digest,
        "evaluated_prefix_sha256": evaluated_prefix_digest.hexdigest(),
        "survivor_prefix_sha256": survivor_prefix_digest.hexdigest(),
        "current_candidate": None,
    })
    after = e4.pc.cache_accounting()
    public = {
        "complete": True,
        "evaluated": word_count,
        "current_candidate": None,
        "contexts": context_public,
        "signed_seed_count": len(signed_steps),
        "signed_seed_images_sha256": seed_digest.hexdigest(),
        "propagated_correction_values_sha256": propagated_digest.hexdigest(),
        "recurrence": "rho(c_i)=rho(c_parent)*rho(signed_seed)",
        "free_reduction_value_invariant": True,
        "failure_bitsets": bitset_rows,
        "failure_lists_sha256": failure_digest,
        "survivor_count": len(survivors),
        "survivor_indices": survivors,
        "survivor_indices_sha256": survivor_digest,
        "per_gate_failure_counts": {row["gate"]: row["failure_count"]
                                    for row in bitset_rows},
        "PC_cache_delta": {
            "hits": after["hits"]-before["hits"],
            "misses": after["misses"]-before["misses"],
            "evictions": after["evictions"]-before["evictions"],
        },
        "runtime_seconds": time.monotonic()-phase_start,
        "direct_word_replay_required_for_full_lane": True,
    }
    print("D972_B345_RELFRAT3_V4_CHEAP_COMPLETE "
          f"evaluated={word_count} survivors={len(survivors)} "
          f"survivor_sha256={survivor_digest}", flush=True)
    return public, failures


def prepare_candidate(candidate: Sequence[int], correction: Sequence[int],
                      e4: MatchedQuotient) -> dict[str, Any]:
    f = reduce_word(candidate)
    require(exponent_sums(f, 2) == [0, 0],
            "candidate free-derived precondition")
    bad = cheap_candidate_bad(f, correction, e4)
    return {"selected_word": f, "correction_word": list(correction),
            "inverse": None, "targets": [], "quotient_bad": bad,
            "_cheap_direct_evaluation": True, "_materialized": False}


def materialize_candidate(base: dict[str, Any], e4: MatchedQuotient) \
        -> dict[str, Any]:
    candidate = base["selected_word"]
    correction = base["correction_word"]
    c34 = cofaces(3)
    coarse_jh_words = [word_substitute(embed_f2_pb3(correction), mapping)
                       for mapping in c34]
    coarse_jh_bad = [f"correction_coarse_J_H_coface_{slot}"
                     for slot, word in enumerate(coarse_jh_words)
                     if e4.eval(word) != e4.identity]
    f = reduce_word(candidate)
    derived = derived_commutator_ledger(f)
    charming_error = reduce_word(f + inv_word(derived["expanded_word"]))
    charming_words = [word_substitute(embed_f2_pb3(charming_error), mapping)
                      for mapping in c34]
    hex_f2 = hexagon_words(f)
    hex_cofaces: list[tuple[str, list[int]]] = []
    for hindex, residual in enumerate(hex_f2, 1):
        source = embed_f2_pb3(residual)
        for slot, mapping in enumerate(c34):
            hex_cofaces.append((f"hexagon_{hindex}_coface_{slot}",
                                word_substitute(source, mapping)))
    pent = pentagon_word(f)
    source = source_words_m0(f)
    source_relations = [(f"S_relation_{index}", word_substitute(relator, source))
                        for index, relator in enumerate(pure_relations(4), 1)]
    cheap_targets: list[tuple[str, str, list[int]]] = []
    cheap_targets.extend((f"charming_error_coface_{slot}", "charming", word)
                         for slot, word in enumerate(charming_words))
    cheap_targets.extend((name, "hexagon", word) for name, word in hex_cofaces)
    cheap_targets.append(("ordered_A18_pentagon", "pentagon", pent))
    cheap_targets.extend((name, "endomorphism_relation", word)
                         for name, word in source_relations)
    quotient_bad = coarse_jh_bad + [name for name, _, word in cheap_targets
                                    if e4.eval(word) != e4.identity]
    materialized = {
        "selected_word": f,
        "correction_word": list(correction),
        "correction_coarse_J_H_coface_words": coarse_jh_words,
        "correction_coarse_J_H_all_five": not coarse_jh_bad,
        "correction_in_finer_J_Phi_required": False,
        "correction_J_Phi_coset_is_lift_freedom": True,
        "derived_witness": derived,
        "charming_error_word": charming_error,
        "hexagon_words_F2": hex_f2,
        "pentagon_word_PB4": pent,
        "marking_residuals": [],
        "representative_residuals": [],
        "marking_reason": "m=0,lambda=1 has no additional literal generator equality",
        "inverse": None,
        "targets": cheap_targets,
        "quotient_bad": quotient_bad,
        "_source_words": source,
        "_source_relations": source_relations,
        "J_H_definition": "kernel of the authenticated coarse source E3 map, gated again by all five coface images in H4",
        "J_Phi_definition": "intersection of all five PB3-to-PB4 coface preimages of Phi4",
        "J_Phi_not_identified_with_Phi3_H3": True,
    }
    require(materialized["quotient_bad"] == base["quotient_bad"],
            "direct cheap/full quotient gate drift")
    base.update(materialized)
    base["_cheap_direct_evaluation"] = True
    base["_materialized"] = True
    return base


def complete_candidate(base: dict[str, Any], e4: MatchedQuotient,
                       pool: ElementPool,
                       inverse_cache: dict[tuple[int, ...], list[list[int]]],
                       inverse_cache_stats: dict[str, int],
                       normalized_inverse: dict[str, Any]) \
        -> dict[str, Any]:
    if not base["_materialized"]:
        base = materialize_candidate(base, e4)
    if base["quotient_bad"]:
        return base
    source = base["_source_words"]
    source_relations = base["_source_relations"]
    inverse = finite_normalized_inverse(
        base["selected_word"], e4, pool, inverse_cache, inverse_cache_stats,
        normalized_inverse)
    twords = inverse["inverse_words"]
    relation_residuals: list[tuple[str, list[int]]] = []
    for index, relator in enumerate(pure_relations(4), 1):
        relation_residuals.append((f"S_relation_{index}",
                                   source_relations[index-1][1]))
        relation_residuals.append((f"T_relation_{index}",
                                   word_substitute(relator, twords)))
    onto_residuals = [(f"ST_generator_{i+1}", word)
                      for i, word in enumerate(inverse["ST_residuals"])] + [
        (f"TS_generator_{i+1}", word)
        for i, word in enumerate(inverse["TS_residuals"])]
    targets = base["targets"][:-len(source_relations)]
    targets.extend((name, "endomorphism_relation", word)
                   for name, word in relation_residuals)
    targets.extend((name, "onto_two_sided_inverse", word)
                   for name, word in onto_residuals)
    base["inverse"] = inverse
    base["targets"] = targets
    base["quotient_bad"] = [name for name, _, word in targets
                            if e4.eval(word) != e4.identity]
    return base


def corrected_def29_targets(candidate: dict[str, Any],
                            e4: MatchedQuotient) -> dict[str, Any]:
    """Freeze the IF-FIRST 33 acceptance / 17 T-only diagnostic split."""
    acceptance: list[tuple[str, str, list[int]]] = []
    diagnostics: list[tuple[str, str, list[int]]] = []
    for name, kind, word in candidate["targets"]:
        if name.startswith("T_relation_") or name.startswith("TS_generator_"):
            diagnostics.append((name, kind, word))
        else:
            acceptance.append((name, kind, word))
    acceptance_names = [row[0] for row in acceptance]
    diagnostic_names = [row[0] for row in diagnostics]
    expected_acceptance = (
        [f"charming_error_coface_{i}" for i in range(5)] +
        [f"hexagon_{j}_coface_{i}" for j in (1, 2) for i in range(5)] +
        ["ordered_A18_pentagon"] +
        [f"S_relation_{i}" for i in range(1, 12)] +
        [f"ST_generator_{i}" for i in range(1, 7)])
    expected_diagnostics = (
        [f"T_relation_{i}" for i in range(1, 12)] +
        [f"TS_generator_{i}" for i in range(1, 7)])
    require(acceptance_names == expected_acceptance and
            diagnostic_names == expected_diagnostics and
            len(acceptance) == 33 and len(diagnostics) == 17,
            "corrected Def2.9 target order")
    diagnostic_rows = []
    for name, kind, word in diagnostics:
        value = e4.eval(word)
        diagnostic_rows.append({
            "name": name, "kind": kind, "word": list(word),
            "quotient_value_hex": (bytes(value[0])+bytes(value[1])).hex(),
            "quotient_identity": value == e4.identity,
            "Fox_membership_eligible": value == e4.identity,
            "Fox_membership_tested": False,
            "feeds_acceptance": False,
        })
    acceptance_bad = [name for name, _, word in acceptance
                      if e4.eval(word) != e4.identity]
    candidate["all_v6_targets"] = candidate["targets"]
    candidate["targets"] = acceptance
    candidate["diagnostic_targets"] = diagnostics
    candidate["diagnostic_rows"] = diagnostic_rows
    candidate["quotient_bad"] = acceptance_bad
    candidate["corrected_Def2_9"] = {
        "acceptance_target_count": 33,
        "diagnostic_target_count": 17,
        "acceptance_target_names": acceptance_names,
        "diagnostic_target_names": diagnostic_names,
        "T_canaries_required_for_acceptance": False,
        "corrected_Def2_9_IF_FIRST_frozen_pre_run": True,
        "diagnostic_quotient_pass_count": sum(
            row["quotient_identity"] for row in diagnostic_rows),
        "diagnostic_false_allowed_on_PASS": True,
    }
    return candidate


###############################################################################
# Candidate-local typed WordExpr DAG and exact left-Fox chain rule.
###############################################################################


class WordExprDAG:
    """Hash-consed ordinary-word expressions over the six PB4 generators."""

    IDENTITY = 1
    FLAT_WORD = 2
    PRODUCT = 3
    INVERSE = 4
    SUBSTITUTE_WORD = 5
    OPCODE_NAMES = {
        IDENTITY: "IDENTITY", FLAT_WORD: "FLAT_WORD",
        PRODUCT: "PRODUCT", INVERSE: "INVERSE",
        SUBSTITUTE_WORD: "SUBSTITUTE_WORD",
    }

    def __init__(self) -> None:
        self.opcode: list[int] = []
        self.rank: list[int] = []
        self.word: list[tuple[int, ...]] = []
        self.children: list[tuple[int, ...]] = []
        self.expanded_count: list[int] = []
        self.by_payload: dict[tuple[Any, ...], int] = {}
        self.edge_count = 0
        self.flat_leaf_count = 0
        self._substitution_cache: dict[tuple[int, tuple[int, ...]], int] = {}

    def _add(self, opcode: int, rank: int, word: tuple[int, ...],
             children: tuple[int, ...], expanded: int) -> int:
        require(rank > 0 and expanded >= 0, "WordExpr node rank/count")
        key = (opcode, rank, word, children)
        prior = self.by_payload.get(key)
        if prior is not None:
            return prior
        if len(self.opcode) >= CAPS["wordexpr_nodes_per_candidate"]:
            raise ResourceStop(
                "wordexpr_nodes_per_candidate",
                cap_key="wordexpr_nodes_per_candidate",
                cap_limit=CAPS["wordexpr_nodes_per_candidate"],
                observed_count=len(self.opcode), trigger_relation="ge")
        if self.edge_count + len(children) > CAPS["wordexpr_edges_per_candidate"]:
            raise ResourceStop(
                "wordexpr_edges_per_candidate",
                cap_key="wordexpr_edges_per_candidate",
                cap_limit=CAPS["wordexpr_edges_per_candidate"],
                observed_count=self.edge_count+len(children),
                trigger_relation="gt")
        identifier = len(self.opcode)+1
        require(all(1 <= child < identifier for child in children),
                "WordExpr backward references")
        self.opcode.append(opcode)
        self.rank.append(rank)
        self.word.append(word)
        self.children.append(children)
        self.expanded_count.append(expanded)
        self.by_payload[key] = identifier
        self.edge_count += len(children)
        if opcode == self.FLAT_WORD:
            self.flat_leaf_count += 1
            if self.flat_leaf_count > CAPS["wordexpr_flat_leaves_per_candidate"]:
                raise ResourceStop(
                    "wordexpr_flat_leaves_per_candidate",
                    cap_key="wordexpr_flat_leaves_per_candidate",
                    cap_limit=CAPS["wordexpr_flat_leaves_per_candidate"],
                    observed_count=self.flat_leaf_count,
                    trigger_relation="gt")
        return identifier

    def identity(self, rank: int = 6) -> int:
        return self._add(self.IDENTITY, rank, (), (), 0)

    def flat(self, word: Sequence[int], rank: int = 6) -> int:
        raw = tuple(int(x) for x in word)
        require(all(x and abs(x) <= rank for x in raw),
                "WordExpr flat generator range")
        if len(raw) > CAPS["single_word_or_section_length"]:
            raise ResourceStop(
                "single_word_or_section_length",
                cap_key="single_word_or_section_length",
                cap_limit=CAPS["single_word_or_section_length"],
                observed_count=len(raw), trigger_relation="gt")
        return self._add(self.FLAT_WORD, rank, raw, (), len(raw))

    def product(self, left: int, right: int) -> int:
        require(1 <= left <= len(self.opcode) and
                1 <= right <= len(self.opcode) and
                self.rank[left-1] == self.rank[right-1],
                "WordExpr product ranks")
        return self._add(
            self.PRODUCT, self.rank[left-1], (), (left, right),
            self.expanded_count[left-1]+self.expanded_count[right-1])

    def product_many(self, roots: Sequence[int]) -> int:
        roots = list(roots)
        require(bool(roots), "WordExpr nonempty product_many")
        def balanced(lo: int, hi: int) -> int:
            if hi-lo == 1:
                return roots[lo]
            mid = (lo+hi)//2
            return self.product(balanced(lo, mid), balanced(mid, hi))
        return balanced(0, len(roots))

    def paper_product(self, roots: Sequence[int]) -> int:
        roots = list(roots)
        require(bool(roots), "WordExpr nonempty paper product")
        return self.product_many(list(reversed(roots)))

    def inverse(self, parent: int) -> int:
        require(1 <= parent <= len(self.opcode), "WordExpr inverse parent")
        return self._add(self.INVERSE, self.rank[parent-1], (), (parent,),
                         self.expanded_count[parent-1])

    def substitute(self, outer_word: Sequence[int], images: Sequence[int]) -> int:
        images = tuple(int(x) for x in images)
        require(bool(images) and all(1 <= x <= len(self.opcode) for x in images),
                "WordExpr substitution images")
        target_rank = self.rank[images[0]-1]
        require(all(self.rank[x-1] == target_rank for x in images),
                "WordExpr substitution target ranks")
        outer = tuple(int(x) for x in outer_word)
        require(all(x and abs(x) <= len(images) for x in outer),
                "WordExpr substitution outer range")
        if len(outer) > CAPS["single_word_or_section_length"]:
            raise ResourceStop(
                "single_word_or_section_length",
                cap_key="single_word_or_section_length",
                cap_limit=CAPS["single_word_or_section_length"],
                observed_count=len(outer), trigger_relation="gt")
        expanded = sum(self.expanded_count[images[abs(letter)-1]-1]
                       for letter in outer)
        return self._add(self.SUBSTITUTE_WORD, target_rank, outer, images,
                         expanded)

    def substitute_expr(self, root: int, images: Sequence[int]) -> int:
        images_tuple = tuple(int(x) for x in images)
        cache_key = (root, images_tuple)
        prior = self._substitution_cache.get(cache_key)
        if prior is not None:
            return prior
        require(self.rank[root-1] == len(images_tuple),
                "WordExpr recursive substitution source rank")
        opcode = self.opcode[root-1]
        if opcode == self.IDENTITY:
            answer = self.identity(self.rank[images_tuple[0]-1])
        elif opcode == self.FLAT_WORD:
            answer = self.substitute(self.word[root-1], images_tuple)
        elif opcode == self.PRODUCT:
            left, right = self.children[root-1]
            answer = self.product(self.substitute_expr(left, images_tuple),
                                  self.substitute_expr(right, images_tuple))
        elif opcode == self.INVERSE:
            answer = self.inverse(self.substitute_expr(
                self.children[root-1][0], images_tuple))
        else:
            require(opcode == self.SUBSTITUTE_WORD,
                    "WordExpr recursive substitution opcode")
            child_images = [self.substitute_expr(child, images_tuple)
                            for child in self.children[root-1]]
            answer = self.substitute(self.word[root-1], child_images)
        self._substitution_cache[cache_key] = answer
        return answer

    def dependencies(self, node: int) -> tuple[int, ...]:
        require(1 <= node <= len(self.opcode), "WordExpr dependency node")
        return self.children[node-1]

    def expand_reduced_below_flat_cap(self, root: int) -> list[int]:
        require(self.expanded_count[root-1] <=
                CAPS["single_word_or_section_length"],
                "WordExpr flat bridge expansion cap")
        memo: dict[int, list[int]] = {}
        reached = self._reachable_from([root])
        for node in range(1, root+1):
            if node not in reached:
                continue
            opcode = self.opcode[node-1]
            if opcode == self.IDENTITY:
                word: list[int] = []
            elif opcode == self.FLAT_WORD:
                word = reduce_word(self.word[node-1])
            elif opcode == self.PRODUCT:
                left, right = self.children[node-1]
                word = reduce_word(memo[left]+memo[right])
            elif opcode == self.INVERSE:
                word = inv_word(memo[self.children[node-1][0]])
            else:
                require(opcode == self.SUBSTITUTE_WORD,
                        "WordExpr flat bridge opcode")
                word = word_substitute(self.word[node-1],
                                       [memo[x] for x in self.children[node-1]])
            require(len(word) <= CAPS["single_word_or_section_length"],
                    "WordExpr reduced flat bridge cap")
            memo[node] = word
        return memo[root]

    def _reachable_from(self, roots: Sequence[int]) -> set[int]:
        reached: set[int] = set()
        pending = list(roots)
        while pending:
            node = pending.pop()
            if node in reached:
                continue
            reached.add(node)
            pending.extend(self.children[node-1])
        return reached

    def accounting(self, roots: Sequence[int]) -> dict[str, Any]:
        counts = {name: 0 for name in self.OPCODE_NAMES.values()}
        for opcode in self.opcode:
            counts[self.OPCODE_NAMES[opcode]] += 1
        return {
            "node_count": len(self.opcode), "edge_count": self.edge_count,
            "flat_leaf_count": self.flat_leaf_count,
            "opcode_counts": counts,
            "root_count": len(roots),
            "max_expanded_letter_count": max(
                (self.expanded_count[root-1] for root in roots), default=0),
            "association": "fixed recursively balanced ordinary PRODUCT",
            "hash_consing": "full opcode/rank/word/child payload equality",
            "digest_is_binding_only": True,
        }

    def serialize_reachable(self, named_roots: Sequence[tuple[str, int]]) \
            -> dict[str, Any]:
        reached: set[int] = set()
        pending = [root for _, root in named_roots]
        while pending:
            node = pending.pop()
            require(1 <= node <= len(self.opcode), "WordExpr root range")
            if node in reached:
                continue
            reached.add(node)
            pending.extend(self.children[node-1])
        ordered = sorted(reached)
        renumber = {old: index+1 for index, old in enumerate(ordered)}
        rows = []
        for old in ordered:
            children = [renumber[x] for x in self.children[old-1]]
            require(all(x < renumber[old] for x in children),
                    "serialized WordExpr topology")
            rows.append({
                "node_id": renumber[old],
                "opcode": self.OPCODE_NAMES[self.opcode[old-1]],
                "rank": self.rank[old-1],
                "flat_word": list(self.word[old-1]),
                "children": children,
                "expanded_letter_count": self.expanded_count[old-1],
            })
        roots = [{"name": name, "node_id": renumber[root]}
                 for name, root in named_roots]
        return {
            "format": "typed-wordexpr-dag/v1",
            "node_order": "one_based_topological",
            "nodes": rows, "roots": roots,
            "node_count": len(rows),
            "edge_count": sum(len(row["children"]) for row in rows),
            "ordinary_product": True,
            "free_reduction_semantic_bridge":
                "recursive expansion then free reduction equals the literal word; D(xx^-1)=0",
            "manifest_sha256": digest_obj({"nodes": rows, "roots": roots}),
        }


def _raw_gradient_add(target: SparseVector, source: SparseVector,
                      scalar: int = 1) -> None:
    add_scaled(target, source, scalar)


def _raw_gradient_translate(source: SparseVector, value: EKey,
                            quotient: MatchedQuotient,
                            scalar: int = 1) -> SparseVector:
    out: SparseVector = {}
    scalar %= 3
    for (component, element), coefficient in source.items():
        add_term(out, (component, quotient.mul(value, element)),
                 scalar*coefficient)
    return out


@dataclass(frozen=True)
class MemoStaticQuotientBinding:
    presentation_sha256: str
    leaf_bindings_sha256: str
    quotient_binding_sha256: str
    rank: int
    degree: int
    pc_rank: int
    quotient_object_identity: int


def build_memo_static_quotient_binding(
        quotient: MatchedQuotient) -> MemoStaticQuotientBinding:
    presentation_sha256 = digest_obj(quotient.pc.receipt)
    leaf_bindings_sha256 = digest_obj([
        _element_blob(value).hex() for value in quotient.generators])
    quotient_binding_sha256 = digest_obj({
        "rank": quotient.rank, "degree": quotient.degree,
        "pc_rank": quotient.pc.n,
        "presentation_sha256": presentation_sha256,
        "leaf_bindings_sha256": leaf_bindings_sha256,
    })
    return MemoStaticQuotientBinding(
        presentation_sha256, leaf_bindings_sha256,
        quotient_binding_sha256, quotient.rank, quotient.degree,
        quotient.pc.n, id(quotient))


class CandidateGradientMemo:
    """Bounded exact memo keyed by the complete typed candidate binding.

    The cache owns raw E4-keyed Fox vectors only.  It never contains element
    pool identifiers, proof-DAG identifiers, sparse-basis rows, or section
    state, so clearing it at the candidate rollback boundary cannot retain a
    transaction suffix.
    """

    def __init__(self, dag: WordExprDAG, quotient: MatchedQuotient,
                 candidate_binding: Any, *, node_cap: int | None = None,
                 sparse_cap: int | None = None,
                 static_quotient_binding: MemoStaticQuotientBinding | None =
                 None) -> None:
        self.dag = dag
        self.quotient = quotient
        self.candidate_binding_sha256 = digest_obj(candidate_binding)
        static = (build_memo_static_quotient_binding(quotient)
                  if static_quotient_binding is None else
                  static_quotient_binding)
        require(static.quotient_object_identity == id(quotient) and
                (static.rank, static.degree, static.pc_rank) ==
                (quotient.rank, quotient.degree, quotient.pc.n),
                "gradient memo injected quotient binding identity/dimensions")
        self.presentation_sha256 = static.presentation_sha256
        self.leaf_bindings_sha256 = static.leaf_bindings_sha256
        self.quotient_binding_sha256 = static.quotient_binding_sha256
        self.node_cap = (CAPS["gradient_memo_nodes"] if node_cap is None
                         else int(node_cap))
        self.sparse_cap = (CAPS["gradient_memo_sparse_entries"]
                           if sparse_cap is None else int(sparse_cap))
        require(self.node_cap > 0 and self.sparse_cap > 0,
                "gradient memo positive caps")
        require(self.sparse_cap *
                CAPS["gradient_memo_estimated_bytes_per_sparse_entry"] <=
                CAPS["gradient_memo_additional_budget_bytes"] <= 512_000_000,
                "gradient memo registered additional-memory budget")
        self.typed_keys: list[str] = []
        for node, opcode in enumerate(dag.opcode, 1):
            children = dag.children[node-1]
            self.typed_keys.append(digest_obj({
                "format": "typed-gradient-key/v1",
                "opcode": dag.OPCODE_NAMES[opcode],
                "rank": dag.rank[node-1],
                "arity": len(children),
                "flat_or_outer_word": list(dag.word[node-1]),
                "child_typed_sha256": [self.typed_keys[x-1]
                                        for x in children],
                "candidate_binding_sha256":
                    self.candidate_binding_sha256,
                "quotient_binding_sha256": self.quotient_binding_sha256,
                "leaf_bindings_sha256": self.leaf_bindings_sha256,
            }))
        self.entries: OrderedDict[str, tuple[int, SparseVector]] = OrderedDict()
        self.pinned_keys: set[str] = set()
        self.requested_pins: set[int] = set()
        self.unretained_requested_pins: set[int] = set()
        self.ever_stored: set[str] = set()
        self.sparse_entries = 0
        self.hits = 0
        self.misses = 0
        self.evictions = 0
        self.skipped_oversize = 0
        self.recomputations = 0
        self.rollbacks = 0
        self.discarded_nodes = 0
        self.discarded_sparse_entries = 0
        self.peak_nodes = 0
        self.peak_sparse_entries = 0
        self.peak_working_plus_cached = 0
        self.cross_candidate_rejections = 0
        self.forged_key_rejections = 0
        self.pin_store_fallbacks = 0
        self.pin_evictions = 0

    def typed_key(self, node: int) -> str:
        require(1 <= node <= len(self.typed_keys), "gradient memo node")
        return self.typed_keys[node-1]

    def request_pins(self, nodes: Sequence[int]) -> None:
        rows = [int(node) for node in nodes]
        require(len(rows) == CAPS["gradient_memo_pinned_source_roots"] and
                len(set(rows)) == len(rows), "six distinct source anchors")
        self.requested_pins.update(rows)
        for node in rows:
            key = self.typed_key(node)
            if key in self.entries:
                self.pinned_keys.add(key)
                self.unretained_requested_pins.discard(node)

    def lookup(self, node: int, *, candidate_binding_sha256: str | None = None,
               supplied_key: str | None = None) -> SparseVector | None:
        if (candidate_binding_sha256 is not None and
                candidate_binding_sha256 != self.candidate_binding_sha256):
            self.cross_candidate_rejections += 1
            raise Reject("gradient memo cross-candidate reuse")
        key = self.typed_key(node)
        if supplied_key is not None and supplied_key != key:
            self.forged_key_rejections += 1
            raise Reject("gradient memo forged typed key")
        entry = self.entries.get(key)
        if entry is None:
            self.misses += 1
            if key in self.ever_stored:
                self.recomputations += 1
            return None
        require(entry[0] == node, "gradient memo typed-node collision")
        self.hits += 1
        self.entries.move_to_end(key)
        return entry[1]

    def contains(self, node: int) -> bool:
        return self.typed_key(node) in self.entries

    def _evict_one(self, active_keys: set[str], *, allow_pinned: bool) -> bool:
        for key, (node, gradient) in list(self.entries.items()):
            if key in active_keys or (key in self.pinned_keys and
                                      not allow_pinned):
                continue
            self.entries.pop(key)
            self.sparse_entries -= len(gradient)
            self.evictions += 1
            if key in self.pinned_keys:
                self.pinned_keys.remove(key)
                self.unretained_requested_pins.add(node)
                self.pin_evictions += 1
            return True
        return False

    def store(self, node: int, gradient: SparseVector,
              active_keys: set[str]) -> bool:
        key = self.typed_key(node)
        pin = node in self.requested_pins
        prior = self.entries.get(key)
        if prior is not None:
            require(prior[0] == node and prior[1] == gradient,
                    "gradient memo recomputation drift")
            if pin:
                self.pinned_keys.add(key)
                self.unretained_requested_pins.discard(node)
            self.entries.move_to_end(key)
            return True
        size = len(gradient)
        if size > self.sparse_cap:
            if pin:
                self.unretained_requested_pins.add(node)
                self.pin_store_fallbacks += 1
            self.skipped_oversize += 1
            return False
        while (len(self.entries) >= self.node_cap or
               self.sparse_entries+size > self.sparse_cap):
            if (not self._evict_one(active_keys, allow_pinned=False) and
                    not self._evict_one(active_keys, allow_pinned=True)):
                if pin:
                    self.unretained_requested_pins.add(node)
                    self.pin_store_fallbacks += 1
                self.skipped_oversize += 1
                return False
        self.entries[key] = (node, gradient)
        self.ever_stored.add(key)
        self.sparse_entries += size
        if pin:
            self.pinned_keys.add(key)
            self.unretained_requested_pins.discard(node)
        self.peak_nodes = max(self.peak_nodes, len(self.entries))
        self.peak_sparse_entries = max(
            self.peak_sparse_entries, self.sparse_entries)
        return True

    def seal_pin_stage(self) -> None:
        require(len(self.requested_pins) ==
                CAPS["gradient_memo_pinned_source_roots"] and
                all(((self.typed_key(node) in self.entries and
                      self.typed_key(node) in self.pinned_keys) or
                     node in self.unretained_requested_pins)
                    for node in self.requested_pins),
                "gradient memo source anchors retained or cold-fallback")

    def trim_for_working(self, working: int, active_keys: set[str]) -> None:
        """Keep cache overhead from turning a valid cold computation terminal."""
        require(working >= 0, "gradient memo working entries")
        while (working+self.sparse_entries >
               CAPS["candidate_live_gradient_entries_total"]):
            if (not self._evict_one(active_keys, allow_pinned=False) and
                    not self._evict_one(active_keys, allow_pinned=True)):
                break

    def clear_candidate(self) -> None:
        self.discarded_nodes += len(self.entries)
        self.discarded_sparse_entries += self.sparse_entries
        self.entries.clear()
        self.pinned_keys.clear()
        self.requested_pins.clear()
        self.unretained_requested_pins.clear()
        self.ever_stored.clear()
        self.sparse_entries = 0
        self.rollbacks += 1

    def accounting(self) -> dict[str, Any]:
        return {
            "format": "candidate-local-typed-gradient-memo/v1",
            "candidate_binding_sha256": self.candidate_binding_sha256,
            "quotient_binding_sha256": self.quotient_binding_sha256,
            "presentation_sha256": self.presentation_sha256,
            "leaf_bindings_sha256": self.leaf_bindings_sha256,
            "key_binds_rank_arity_candidate_quotient_leafs": True,
            "equal_group_value_is_not_a_cache_key": True,
            "cross_candidate_sharing": False,
            "pool_or_proof_identifiers_stored": False,
            "node_cap": self.node_cap, "sparse_entry_cap": self.sparse_cap,
            "estimated_bytes_per_sparse_entry":
                CAPS["gradient_memo_estimated_bytes_per_sparse_entry"],
            "additional_budget_bytes":
                CAPS["gradient_memo_additional_budget_bytes"],
            "hits": self.hits, "misses": self.misses,
            "evictions": self.evictions,
            "skipped_oversize": self.skipped_oversize,
            "recomputations": self.recomputations,
            "peak_cached_nodes": self.peak_nodes,
            "peak_cached_sparse_entries": self.peak_sparse_entries,
            "peak_working_plus_cached_sparse_entries":
                self.peak_working_plus_cached,
            "pinned_source_count": len(self.pinned_keys),
            "requested_source_count": len(self.requested_pins),
            "unretained_requested_source_count":
                len(self.unretained_requested_pins),
            "pin_store_fallbacks": self.pin_store_fallbacks,
            "pin_evictions": self.pin_evictions,
            "cache_capacity_is_nonterminal": True,
            "rollbacks": self.rollbacks,
            "discarded_nodes": self.discarded_nodes,
            "discarded_sparse_entries": self.discarded_sparse_entries,
            "eviction_changes_performance_only": True,
        }


class WordExprEvaluator:
    """Independent-of-pool value and exact memoized left-Fox evaluator."""

    def __init__(self, dag: WordExprDAG, quotient: MatchedQuotient,
                 candidate_binding: Any | None = None,
                 progress_hook: Any = None, *, memo_node_cap: int | None = None,
                 memo_sparse_cap: int | None = None,
                 memo_static_binding: MemoStaticQuotientBinding | None =
                 None) -> None:
        self.dag = dag
        self.quotient = quotient
        self.values: list[EKey] = []
        self.live_gradient_peak = 0
        self.target_gradient_entry_peak = 0
        self.progress_hook = progress_hook
        self.memo = CandidateGradientMemo(
            dag, quotient,
            {"legacy_fixture": True} if candidate_binding is None
            else candidate_binding,
            node_cap=memo_node_cap, sparse_cap=memo_sparse_cap,
            static_quotient_binding=memo_static_binding)

    def evaluate_values(self, roots: Sequence[int] | None = None) -> list[EKey]:
        reached = (set(range(1, len(self.dag.opcode)+1)) if roots is None
                   else self.dag._reachable_from(list(roots)))
        # Unreached nodes are never read by a requested PB4 root.  Keep
        # identity placeholders so the evaluator's indexed value table stays
        # compatible with the memo/gradient core.
        values: list[EKey] = [self.quotient.identity] * len(self.dag.opcode)
        q = self.quotient
        for node, opcode in enumerate(self.dag.opcode, 1):
            if node not in reached:
                continue
            rank = self.dag.rank[node-1]
            # A positive seed-span replay keeps the correction expression in
            # its native F2 rank and substitutes it into PB4 roots before any
            # value/gradient is requested.  Such rank-2 nodes are therefore
            # deliberately unreachable from the evaluated PB4 roots.  Keep a
            # typed placeholder in the parallel value table; evaluating a
            # rank-2 leaf as a PB4 word would silently change y from A23 to
            # A13 and invalidate the typed replay.
            if rank != len(q.generators):
                require(rank == 2 and opcode in {
                    WordExprDAG.IDENTITY, WordExprDAG.FLAT_WORD,
                    WordExprDAG.PRODUCT, WordExprDAG.INVERSE,
                    WordExprDAG.SUBSTITUTE_WORD},
                        "WordExpr non-PB4 typed node")
                values[node-1] = q.identity
                continue
            if opcode == WordExprDAG.IDENTITY:
                require(rank == len(q.generators), "WordExpr identity target rank")
                value = q.identity
            elif opcode == WordExprDAG.FLAT_WORD:
                require(rank == len(q.generators), "WordExpr flat target rank")
                value = q.eval(self.dag.word[node-1])
            elif opcode == WordExprDAG.PRODUCT:
                left, right = self.dag.children[node-1]
                value = q.mul(values[left-1], values[right-1])
            elif opcode == WordExprDAG.INVERSE:
                value = q.inverse(values[self.dag.children[node-1][0]-1])
            else:
                require(opcode == WordExprDAG.SUBSTITUTE_WORD,
                        "WordExpr value opcode")
                children = self.dag.children[node-1]
                prefix = q.identity
                for letter in self.dag.word[node-1]:
                    child_value = values[children[abs(letter)-1]-1]
                    prefix = q.mul(prefix, child_value if letter > 0 else
                                   q.inverse(child_value))
                value = prefix
            values[node-1] = value
            if self.progress_hook is not None and (node & 255) == 0:
                self.progress_hook("wordexpr_values", node, None)
        self.values = values
        return values

    def pin_source_roots(self, roots: Sequence[int]) -> None:
        self.memo.request_pins(roots)
        # Evaluate one anchor at a time.  If all six do not fit, older anchors
        # may be evicted and later recomputed cold; cache capacity is never a
        # mathematical stop or candidate rejection.
        for root in roots:
            self.evaluate_gradients([root])
        self.memo.seal_pin_stage()

    def discard_candidate_memo(self) -> dict[str, Any]:
        before = self.memo.accounting()
        self.memo.clear_candidate()
        after = self.memo.accounting()
        require(after["pinned_source_count"] == 0 and
                self.memo.sparse_entries == 0 and not self.memo.entries,
                "candidate memo rollback clears all entries")
        return {"before": before, "after": after}

    def _gradient_node(self, node: int,
                       gradients: dict[int, SparseVector]) -> SparseVector:
        q = self.quotient
        opcode = self.dag.opcode[node-1]
        if opcode == WordExprDAG.IDENTITY:
            return {}
        if opcode == WordExprDAG.FLAT_WORD:
            gradient, value = fox_gradient_without_sections(
                self.dag.word[node-1], q, self.progress_hook)
            require(value == self.values[node-1],
                    "WordExpr flat value/gradient")
            return gradient
        if opcode == WordExprDAG.PRODUCT:
            left, right = self.dag.children[node-1]
            gradient = dict(gradients[left])
            _raw_gradient_add(
                gradient,
                _raw_gradient_translate(gradients[right],
                                        self.values[left-1], q))
            return gradient
        if opcode == WordExprDAG.INVERSE:
            parent = self.dag.children[node-1][0]
            return _raw_gradient_translate(
                gradients[parent], q.inverse(self.values[parent-1]), q, 2)
        require(opcode == WordExprDAG.SUBSTITUTE_WORD,
                "WordExpr gradient opcode")
        children = self.dag.children[node-1]
        prefix = q.identity
        gradient: SparseVector = {}
        for index, letter in enumerate(self.dag.word[node-1], 1):
            child = children[abs(letter)-1]
            if letter > 0:
                _raw_gradient_add(
                    gradient,
                    _raw_gradient_translate(gradients[child], prefix, q))
                prefix = q.mul(prefix, self.values[child-1])
            else:
                # Frozen left-Fox convention: advance the prefix by a_i^-1,
                # then subtract that advanced prefix times D(a_i).
                prefix = q.mul(prefix, q.inverse(self.values[child-1]))
                _raw_gradient_add(
                    gradient,
                    _raw_gradient_translate(gradients[child], prefix, q), 2)
            if self.progress_hook is not None and (index & 1023) == 0:
                self.progress_hook("wordexpr_substitution", node, index)
        require(prefix == self.values[node-1],
                "WordExpr substitution prefix/value")
        return gradient

    def evaluate_gradients(self, roots: Sequence[int]) \
            -> dict[int, SparseVector]:
        require(bool(self.values) and len(self.values) == len(self.dag.opcode),
                "WordExpr values before gradients")
        requested = set(int(root) for root in roots)
        reached: set[int] = set()
        pending = list(requested)
        gradients: dict[int, SparseVector] = {}
        active_keys: set[str] = set()
        while pending:
            node = pending.pop()
            if node in reached or node in gradients:
                continue
            cached = self.memo.lookup(node)
            if cached is not None:
                gradients[node] = cached
                active_keys.add(self.memo.typed_key(node))
                continue
            reached.add(node)
            pending.extend(self.dag.dependencies(node))
        references = {node: 0 for node in reached}
        for node in reached:
            for child in self.dag.dependencies(node):
                if child in reached:
                    references[child] += 1
                else:
                    require(child in gradients,
                            "WordExpr cached dependency closure")
        working = 0
        for node in sorted(reached):
            gradient = self._gradient_node(node, gradients)
            gradients[node] = gradient
            working += len(gradient)
            if self.memo.store(node, gradient, active_keys):
                active_keys.add(self.memo.typed_key(node))
                working -= len(gradient)
            self.memo.trim_for_working(working, active_keys)
            live = working+self.memo.sparse_entries
            self.live_gradient_peak = max(self.live_gradient_peak, live)
            self.memo.peak_working_plus_cached = max(
                self.memo.peak_working_plus_cached, live)
            if live > CAPS["candidate_live_gradient_entries_total"]:
                raise ResourceStop(
                    "candidate_live_gradient_entries_total",
                    cap_key="candidate_live_gradient_entries_total",
                    cap_limit=CAPS["candidate_live_gradient_entries_total"],
                    observed_count=live, trigger_relation="gt")
            for child in self.dag.dependencies(node):
                if child not in reached:
                    continue
                references[child] -= 1
                require(references[child] >= 0, "WordExpr reference accounting")
                if references[child] == 0 and child not in requested:
                    child_gradient = gradients.pop(child)
                    if self.memo.contains(child):
                        active_keys.discard(self.memo.typed_key(child))
                    else:
                        working -= len(child_gradient)
            if self.progress_hook is not None and (node & 255) == 0:
                self.progress_hook("wordexpr_gradients", node, None)
        require(all(root in gradients for root in requested),
                "WordExpr requested gradients retained")
        self.target_gradient_entry_peak = max(
            self.target_gradient_entry_peak,
            max((len(gradients[root]) for root in requested), default=0))
        return {root: gradients[root] for root in requested}

    def evaluate_gradients_cold(self, roots: Sequence[int]) \
            -> dict[int, SparseVector]:
        """Frozen v8-style no-memo differential route."""
        require(bool(self.values) and len(self.values) == len(self.dag.opcode),
                "WordExpr values before cold gradients")
        requested = set(int(root) for root in roots)
        reached = self.dag._reachable_from(list(requested))
        references = {node: 0 for node in reached}
        for node in reached:
            for child in self.dag.dependencies(node):
                references[child] += 1
        gradients: dict[int, SparseVector] = {}
        for node in sorted(reached):
            gradients[node] = self._gradient_node(node, gradients)
            for child in self.dag.dependencies(node):
                references[child] -= 1
                if references[child] == 0 and child not in requested:
                    gradients.pop(child)
        return {root: gradients[root] for root in requested}


class MemoProgress:
    """Bounded flushed operational progress; never serialized in receipts."""

    def __init__(self, start: float, monitor: ResourceMonitor) -> None:
        self.start = start
        self.monitor = monitor
        self.last_timed = start
        self.records = 0
        self.last_rss = current_rss_bytes()
        self.candidate = 0
        self.target_ordinal = 0
        self.target_name = "none"
        self.component = 0
        self.blocker = "not_tested"
        self.pool_suffix = 0
        self.evaluator: WordExprEvaluator | None = None
        self.phase = "initializing"

    def bind(self, *, phase: str | None = None,
             candidate: int | None = None, target_ordinal: int | None = None,
             target_name: str | None = None, component: int | None = None,
             blocker: str | None = None, pool_suffix: int | None = None,
             evaluator: WordExprEvaluator | None = None) -> None:
        if phase is not None:
            self.phase = phase
        if candidate is not None:
            self.candidate = candidate
        if target_ordinal is not None:
            self.target_ordinal = target_ordinal
        if target_name is not None:
            self.target_name = target_name
        if component is not None:
            self.component = component
        if blocker is not None:
            self.blocker = blocker
        if pool_suffix is not None:
            self.pool_suffix = pool_suffix
        if evaluator is not None:
            self.evaluator = evaluator

    def emit(self, *, boundary: bool = False, node: int = 0,
             anchor_progress: int | None = None) -> None:
        now = time.monotonic()
        timed = now-self.last_timed >= CAPS["progress_interval_seconds"]
        if not boundary and not timed:
            return
        if self.records >= CAPS["memo_progress_records"]:
            # The registered maximum is below the cap.  If a future code path
            # drifts, retain the <=10s heartbeat without unbounded output.
            if not timed:
                return
        if timed:
            self.last_rss = current_rss_bytes()
            self.last_timed = now
        memo = ({} if self.evaluator is None else
                 self.evaluator.memo.accounting())
        pinned = (0 if self.evaluator is None else
                  len(self.evaluator.memo.pinned_keys))
        requested = (0 if self.evaluator is None else
                     len(self.evaluator.memo.requested_pins))
        unretained = (0 if self.evaluator is None else
                      len(self.evaluator.memo.unretained_requested_pins))
        print(
            "D972_B345_RELFRAT3_WORDEXPR_MEMO_V9_PROGRESS "
            f"phase={self.phase} candidate={self.candidate} "
            f"target={self.target_ordinal} name={self.target_name} "
            f"component={self.component} node={node} "
            f"anchors={pinned if anchor_progress is None else anchor_progress} "
            f"anchors_requested={requested} anchors_retained={pinned} "
            f"anchors_cold_fallback={unretained} "
            f"memo_hits={memo.get('hits', 0)} "
            f"memo_misses={memo.get('misses', 0)} "
            f"memo_evictions={memo.get('evictions', 0)} "
            f"memo_live={0 if self.evaluator is None else self.evaluator.memo.sparse_entries} "
            f"memo_pinned={pinned} blocker={self.blocker} "
            f"pool_suffix={self.pool_suffix} RSS={self.last_rss} "
            f"elapsed_s={now-self.start:.3f}", flush=True)
        self.records += 1

    def hook(self, phase: str, node: int, _: int | None) -> None:
        self.phase = phase
        # Long single-root Fox/WordExpr work must retain the frozen wall/RSS
        # fail-closed guard, not merely print a heartbeat between targets.
        self.monitor.check("wordexpr_memo_inner")
        self.emit(node=node)


def raw_gradient_binding(name: str, kind: str, gradient: SparseVector,
                         value: EKey) -> dict[str, Any]:
    digest = hashlib.sha256()
    rows = sorted(gradient.items(), key=lambda row: (row[0][0], row[0][1]))
    for (component, element), coefficient in rows:
        blob = _element_blob(element)
        digest.update(component.to_bytes(1, "little"))
        digest.update(len(blob).to_bytes(2, "little"))
        digest.update(blob)
        digest.update(int(coefficient).to_bytes(1, "little"))
    return {
        "name": name, "kind": kind, "entry_count": len(rows),
        "quotient_value_hex": _element_blob(value).hex(),
        "canonical_gradient_sha256": digest.hexdigest(),
        "canonical_order": "component then exact canonical E4 bytes",
        "digest_is_binding_only_not_element_equality": True,
    }


def build_wordexpr_candidate(correction_index: int,
                             correction: Sequence[int],
                             inverse_words: Sequence[Sequence[int]]) \
        -> dict[str, Any]:
    """Compile the exact corrected-Def2.9 target family without descendants."""
    require(len(inverse_words) == 6, "WordExpr six fixed inverse words")
    candidate_word = reduce_word(FIXED_WORD + list(correction))
    require(exponent_sums(candidate_word, 2) == [0, 0],
            "WordExpr candidate exponent sums")
    dag = WordExprDAG()
    one = dag.identity(6)
    generators = [dag.flat([i], 6) for i in range(1, 7)]

    def f_at(left: int, right: int) -> int:
        return dag.substitute(candidate_word, [left, right])

    def c_at(left: int, right: int) -> int:
        return dag.substitute(correction, [left, right])

    correction_cofaces: list[tuple[str, int]] = []
    hex1_rows: list[tuple[str, str, int]] = []
    hex2_rows: list[tuple[str, str, int]] = []
    for slot, mapping in enumerate(cofaces(3)):
        x = dag.flat(mapping[0], 6)
        y = dag.flat(mapping[2], 6)
        correction_cofaces.append(
            (f"correction_coarse_J_H_coface_{slot}", c_at(x, y)))
        z = dag.inverse(dag.paper_product([x, y]))
        u = dag.inverse(dag.paper_product([y, x]))
        fxy = f_at(x, y)
        fxz = f_at(x, z)
        fyz = f_at(y, z)
        fux = f_at(u, x)
        fuy = f_at(u, y)
        h1 = dag.paper_product([fxy, dag.inverse(fxz), fyz])
        h2 = dag.paper_product([dag.inverse(fux), dag.inverse(fxy), fuy])
        hex1_rows.append((f"hexagon_1_coface_{slot}", "hexagon", h1))
        hex2_rows.append((f"hexagon_2_coface_{slot}", "hexagon", h2))
    acceptance: list[tuple[str, str, int]] = [
        (f"charming_error_coface_{slot}", "charming", one)
        for slot in range(5)] + hex1_rows + hex2_rows

    pent_contexts = [
        (generators[0], generators[3]),
        (generators[3], generators[5]),
        (dag.paper_product([generators[1], generators[3]]), generators[5]),
        (dag.paper_product([generators[0], generators[1]]),
         dag.paper_product([generators[4], generators[5]])),
        (generators[0], dag.paper_product([generators[3], generators[4]])),
    ]
    pent_parts = [f_at(left, right) for left, right in pent_contexts]
    pent = dag.paper_product([
        dag.inverse(dag.paper_product([pent_parts[4], pent_parts[2]])),
        pent_parts[1], pent_parts[3], pent_parts[0]])
    acceptance.append(("ordered_A18_pentagon", "pentagon", pent))

    ff = f_at(generators[0], generators[3])
    gv = f_at(generators[0], generators[1])
    gs = f_at(generators[3], generators[4])
    f1234 = f_at(dag.product_many([generators[3], generators[1]]),
                  generators[5])
    h = f_at(dag.product_many([generators[1], generators[0]]), generators[2])
    middle = f_at(dag.product_many([generators[1], generators[0]]),
                  dag.product_many([generators[5], generators[4]]))
    source = [
        generators[0],
        dag.product_many([dag.inverse(gv), generators[1], gv]),
        dag.product_many([dag.inverse(ff), dag.inverse(h), generators[2], h, ff]),
        dag.product_many([dag.inverse(ff), generators[3], ff]),
        dag.product_many([dag.inverse(ff), dag.inverse(middle), dag.inverse(gs),
                          generators[4], gs, middle, ff]),
        dag.product_many([dag.inverse(f1234), generators[5], f1234]),
    ]
    relations = pure_relations(4)
    for index, relator in enumerate(relations, 1):
        acceptance.append((f"S_relation_{index}", "endomorphism_relation",
                           dag.substitute(relator, source)))

    inverse_roots = [dag.flat(word, 6) for word in inverse_words]
    diagnostics: list[tuple[str, str, int]] = []
    for index, relator in enumerate(relations, 1):
        diagnostics.append((f"T_relation_{index}", "endomorphism_relation",
                            dag.substitute(relator, inverse_roots)))
    for index, inverse_word in enumerate(inverse_words, 1):
        st = dag.product(
            dag.substitute(inverse_word, source), dag.inverse(generators[index-1]))
        acceptance.append((f"ST_generator_{index}", "onto_two_sided_inverse", st))
    for index, source_root in enumerate(source, 1):
        ts = dag.product(dag.substitute_expr(source_root, inverse_roots),
                         dag.inverse(generators[index-1]))
        diagnostics.append((f"TS_generator_{index}",
                            "onto_two_sided_inverse", ts))

    expected_acceptance = (
        [f"charming_error_coface_{i}" for i in range(5)] +
        [f"hexagon_{j}_coface_{i}" for j in (1, 2) for i in range(5)] +
        ["ordered_A18_pentagon"] +
        [f"S_relation_{i}" for i in range(1, 12)] +
        [f"ST_generator_{i}" for i in range(1, 7)])
    expected_diagnostics = ([f"T_relation_{i}" for i in range(1, 12)] +
                            [f"TS_generator_{i}" for i in range(1, 7)])
    require([x[0] for x in acceptance] == expected_acceptance and
            [x[0] for x in diagnostics] == expected_diagnostics and
            len(acceptance) == 33 and len(diagnostics) == 17,
            "WordExpr corrected Def2.9 order")
    roots = ([root for _, _, root in acceptance+diagnostics] + source +
             [root for _, root in correction_cofaces])
    if any(dag.expanded_count[root-1] >
           CAPS["wordexpr_expanded_letter_count_per_target"] for root in roots):
        expanded = max(dag.expanded_count[root-1] for root in roots)
        raise ResourceStop(
            "wordexpr_expanded_letter_count_per_target",
            cap_key="wordexpr_expanded_letter_count_per_target",
            cap_limit=CAPS["wordexpr_expanded_letter_count_per_target"],
            observed_count=expanded, trigger_relation="gt")
    return {
        "correction_index": correction_index,
        "correction_word": list(correction),
        "candidate_word": candidate_word,
        "candidate_exponent_sums": exponent_sums(candidate_word, 2),
        "dag": dag,
        "source_roots": source,
        "inverse_roots": inverse_roots,
        "correction_coface_roots": correction_cofaces,
        "acceptance": acceptance,
        "diagnostics": diagnostics,
        "charming_witness": {
            "g_equals_f": True, "f_times_g_inverse_is_identity": True,
            "error_gradient_zero": True,
            "free_group_fact": "ker(F2->Z^2)=[F2,F2]",
        },
    }


def source_tuple_preflight(dictionary: dict[str, Any], e4: MatchedQuotient,
                           frozen_tuple: tuple[EKey, ...],
                           monitor: ResourceMonitor) -> tuple[dict[str, Any],
                                                               list[tuple[EKey, ...]]]:
    """Complete parent-DP replay of all six source tuples before sparse growth."""
    g = e4.generators
    contexts = [
        (g[0], g[3]), (g[0], g[1]), (g[3], g[4]),
        (quotient_product(e4, [g[3], g[1]]), g[5]),
        (quotient_product(e4, [g[1], g[0]]), g[2]),
        (quotient_product(e4, [g[1], g[0]]),
         quotient_product(e4, [g[5], g[4]])),
    ]
    seeds = dictionary["seed_words"]
    signed_steps = [(i+1, word) for i, word in enumerate(seeds)] + [
        (-(i+1), inv_word(word)) for i, word in enumerate(seeds)]
    parents = dictionary["parent_indices"]
    edges = dictionary["signed_seed_edges"]
    values_by_context: list[list[EKey]] = []
    seed_digest = hashlib.sha256()
    for context_index, context in enumerate(contexts, 1):
        seed_values = {edge: e4.eval(word, context)
                       for edge, word in signed_steps}
        for edge in sorted(seed_values):
            seed_digest.update(context_index.to_bytes(1, "little"))
            seed_digest.update(edge.to_bytes(2, "little", signed=True))
            seed_digest.update(_element_blob(seed_values[edge]))
        values = [e4.identity]
        for index in range(1, len(dictionary["words"])):
            parent = parents[index]-1
            edge = edges[index]
            require(0 <= parent < index and edge in seed_values,
                    "source tuple DP parent/edge")
            values.append(e4.mul(values[parent], seed_values[edge]))
        values_by_context.append(values)
    base = [e4.eval(FIXED_WORD, context) for context in contexts]
    tuples: list[tuple[EKey, ...]] = []
    tuple_shas: list[str] = []
    exponent_rows: list[list[int]] = []
    ledger_digest = hashlib.sha256()
    first_difference: dict[str, Any] | None = None
    for zero_index, correction in enumerate(dictionary["words"]):
        monitor.check("source_tuple_preflight")
        ff, gv, gs, f1234, h, middle = [
            e4.mul(base[j], values_by_context[j][zero_index]) for j in range(6)]
        source_tuple = (
            g[0],
            quotient_product(e4, [e4.inverse(gv), g[1], gv]),
            quotient_product(e4, [e4.inverse(ff), e4.inverse(h), g[2], h, ff]),
            quotient_product(e4, [e4.inverse(ff), g[3], ff]),
            quotient_product(e4, [e4.inverse(ff), e4.inverse(middle),
                                  e4.inverse(gs), g[4], gs, middle, ff]),
            quotient_product(e4, [e4.inverse(f1234), g[5], f1234]),
        )
        tuples.append(source_tuple)
        tuple_hex = [_element_blob(value).hex() for value in source_tuple]
        tuple_sha = digest_obj(tuple_hex)
        tuple_shas.append(tuple_sha)
        exponents = exponent_sums(reduce_word(FIXED_WORD+correction), 2)
        exponent_rows.append(exponents)
        row = [zero_index+1, tuple_hex, exponents]
        ledger_digest.update(canonical_bytes(row)+b"\n")
        if source_tuple != frozen_tuple and first_difference is None:
            first_difference = {
                "candidate_index": zero_index+1,
                "candidate_tuple_hex": tuple_hex,
                "frozen_tuple_hex": [_element_blob(x).hex() for x in frozen_tuple],
            }
    require(len(tuples) == len(dictionary["words"]) ==
            CAPS["dictionary_word_records"], "complete source tuple ledger")
    require(all(row == [0, 0] for row in exponent_rows),
            "registered candidate exponent sums")
    public = {
        "complete": True, "evaluated": len(tuples),
        "all_equal_to_frozen_tuple": first_difference is None,
        "first_difference": first_difference,
        "tuple_sha256_by_candidate": tuple_shas,
        "tuple_ledger_sha256": ledger_digest.hexdigest(),
        "candidate_exponent_sums": exponent_rows,
        "all_candidate_exponent_sums_zero": all(row == [0, 0]
                                                  for row in exponent_rows),
        "frozen_tuple_hex": [_element_blob(x).hex() for x in frozen_tuple],
        "context_count": len(contexts),
        "signed_seed_images_sha256": seed_digest.hexdigest(),
        "recurrence": "rho(c_i)=rho(c_parent)*rho(signed_seed)",
        "raw_descendant_words_evaluated": False,
    }
    return public, tuples


def membership_reduce_fixed_basis(target: PackedSparseVector,
                                  basis: SparseBoundaryBasis) \
        -> int | None:
    """Membership-only reduction: no provenance node is allocated."""
    vector = dict(target)
    while vector:
        basis.max_transient_vector_support = max(
            basis.max_transient_vector_support, len(vector))
        pivot = basis.pivot(vector)
        row = basis.rows.get(pivot)
        if row is None:
            return pivot
        coefficient = vector[pivot]
        add_scaled(vector, row[0], -coefficient)
        if len(vector) > CAPS["total_sparse_group_ring_keys"]:
            raise ResourceStop(
                "target_elimination_support",
                cap_key="target_elimination_support",
                cap_limit=CAPS["target_elimination_support"],
                observed_count=len(vector), trigger_relation="gt")
        basis._cadence("wordexpr_membership_only_elimination")
    return None


def encode_scan_prefix(records: Sequence[dict[str, Any]], element_width: int,
                       complete: bool) -> dict[str, Any]:
    require(len(records) <= CAPS["candidate_scan_records"] and
            element_width > 0, "scan prefix bounds")
    outcomes = bytearray()
    target_ordinals = bytearray()
    blocker_components = bytearray()
    blocker_values = bytearray()
    diagnostic_pass_counts = bytearray()
    indices = array("I")
    failure_distribution: dict[str, int] = {}
    for expected, row in enumerate(records, 1):
        require(row["candidate_index"] == expected,
                "scan evaluated-index order")
        indices.append(expected)
        outcomes.append(int(row["outcome_code"]))
        target_ordinals.append(int(row["failed_target_ordinal"]))
        blocker_components.append(int(row["blocker_component"]))
        blob = bytes.fromhex(row["blocker_value_hex"])
        require(len(blob) == element_width, "scan blocker width")
        blocker_values.extend(blob)
        diagnostic_pass_counts.append(int(row["diagnostic_pass_count"]))
        label = row["outcome"] + ":" + row.get("failed_name", "")
        failure_distribution[label] = failure_distribution.get(label, 0)+1

    def block(name: str, typecode: str,
              values: Sequence[int] | bytes | bytearray, cap: int) \
            -> dict[str, Any]:
        return _packed_array_block(name, typecode, values, cap)

    arrays = {
        "candidate_index": block("uint32", "I", indices,
                                 CAPS["candidate_scan_records"]),
        "outcome_code": block("uint8", "B", outcomes,
                              CAPS["candidate_scan_records"]),
        "failed_target_ordinal": block("uint8", "B", target_ordinals,
                                       CAPS["candidate_scan_records"]),
        "blocker_component": block("uint8", "B", blocker_components,
                                   CAPS["candidate_scan_records"]),
        "blocker_value": block(
            "fixed_width_bytes", "B", blocker_values,
            CAPS["candidate_scan_records"]*element_width),
        "diagnostic_pass_count": block(
            "uint8", "B", diagnostic_pass_counts,
            CAPS["candidate_scan_records"]),
    }
    manifest = {name: {key: value for key, value in row.items()
                       if key != "base64"}
                for name, row in arrays.items()}
    public_rows = [{key: value for key, value in row.items()
                    if key not in {"blocker_value_hex"}}
                   for row in records]
    return {
        "format": "registered-wordexpr-scan-arrays/v1",
        "evaluated": len(records), "complete": complete,
        "element_width_bytes": element_width,
        "outcome_codes": {
            "1": "direct_gate_or_acceptance_quotient_failure",
            "2": "fixed_basis_missing_pivot",
            "3": "PASS",
        },
        "arrays": arrays,
        "array_manifest_sha256": digest_obj(manifest),
        "record_bindings": public_rows,
        "record_bindings_sha256": digest_obj(records),
        "evaluated_index_order_sha256": digest_obj(
            [row["candidate_index"] for row in records]),
        "failure_distribution": failure_distribution,
    }


###############################################################################
# Lossless receipt encoding.
###############################################################################


class ElementRegistry:
    def __init__(self, quotients: dict[int, MatchedQuotient]) -> None:
        self.quotients = quotients
        self.ids: dict[tuple[int, EKey], int] = {}
        self.rows: list[dict[str, Any]] = []

    def add(self, rank: int, element: EKey, section: Sequence[int]) -> int:
        key = (rank, element)
        if key in self.ids:
            return self.ids[key]
        quotient = self.quotients[rank]
        require(quotient.eval(section) == element, "registry section evaluation")
        if len(section) > CAPS["single_word_or_section_length"]:
            raise ResourceStop(
                "single_word_or_section_length",
                cap_key="single_word_or_section_length",
                cap_limit=CAPS["single_word_or_section_length"],
                observed_count=len(section), trigger_relation="gt")
        identifier = len(self.rows) + 1
        self.ids[key] = identifier
        self.rows.append({
            "id": identifier,
            "rank": rank,
            "section_word": list(section),
            "coarse_permutation": [x+1 for x in element[0]],
            "fine_pc_coords": list(element[1]),
        })
        return identifier

    def add_expression(self, rank: int, element: EKey,
                       expression_root: int) -> int:
        key = (rank, element)
        if key in self.ids:
            return self.ids[key]
        require(rank == 4 and isinstance(expression_root, int) and
                expression_root >= 0, "registry expression section")
        identifier = len(self.rows) + 1
        self.ids[key] = identifier
        self.rows.append({
            "id": identifier,
            "rank": rank,
            "section_expression_root": expression_root,
            "coarse_permutation": [x+1 for x in element[0]],
            "fine_pc_coords": list(element[1]),
        })
        return identifier


def encode_vector(rank: int, vector: SparseVector,
                  sections: dict[EKey, list[int]],
                  registry: ElementRegistry) -> list[list[int]]:
    rows = []
    for (component, element), coefficient in sorted(vector.items()):
        require(element in sections, "missing vector support section")
        rows.append([component, registry.add(rank, element, sections[element]), coefficient])
    return rows


def boundary_certificate(name: str, kind: str, word: Sequence[int],
                         quotient: MatchedQuotient, proof_root_node_id: int,
                         registry: ElementRegistry) -> dict[str, Any]:
    gradient, value, sections = fox_gradient(word, quotient)
    require(value == quotient.identity, f"{name}: quotient identity")
    encoded_gradient = encode_vector(4, gradient, sections, registry)
    return {
        "name": name,
        "kind": kind,
        "arity": 4,
        "word": list(word),
        "quotient_identity": True,
        "gradient": encoded_gradient,
        "proof_root_node_id": proof_root_node_id,
        "proof_system": "shared_topological_F3_provenance_DAG",
        "gradient_sha256": digest_obj(encoded_gradient),
        "fox_membership": "word in Phi_3(H4) iff its evaluated Fox gradient lies in image(D2)",
    }


def _packed_array_block(type_name: str, typecode: str,
                        values: Sequence[int] | bytes | bytearray,
                        cap: int, monitor: ResourceMonitor | None = None) -> dict[str, Any]:
    estimated_itemsize = 1 if typecode == "B" else array(typecode).itemsize
    if monitor is not None:
        monitor.reserve("proof_DAG_array_bytes",
                        len(values)*estimated_itemsize*2 + 1_048_576)
    if typecode == "B":
        raw = bytes(values)
        length = len(raw)
        itemsize = 1
    else:
        packed = values if isinstance(values, array) and values.typecode == typecode \
            else array(typecode, values)
        if sys.byteorder != "little":
            packed = array(typecode, packed)
            packed.byteswap()
        raw = packed.tobytes()
        length = len(packed)
        itemsize = packed.itemsize
    require(length <= cap, "packed certificate array cap")
    if monitor is not None:
        monitor.reserve("proof_DAG_base64",
                        len(raw) + ((len(raw)+2)//3)*4 + 1_048_576)
    encoded = base64.b64encode(raw).decode("ascii")
    if monitor is not None:
        monitor.check("proof_DAG_base64_complete", force=True)
    return {
        "type": type_name,
        "array_typecode": typecode,
        "endianness": "little",
        "length": length,
        "itemsize": itemsize,
        "byte_length": len(raw),
        "cap": cap,
        "sha256": hashlib.sha256(raw).hexdigest(),
        "base64": encoded,
    }


def serialize_proof_dag(dag: ProvenanceDAG, roots: dict[str, int],
                        basis: SparseBoundaryBasis,
                        registry: ElementRegistry) \
        -> tuple[dict[str, Any], dict[int, int]]:
    require(bool(roots), "proof DAG roots")
    if basis.deadline is not None:
        basis.deadline.check("proof_DAG_pre_serialization_RSS", force=True)
    if basis.deadline is not None:
        basis.deadline.reserve("proof_DAG_reachability",
                               (dag.node_count+1)*16 + dag.edge_count*6 +
                               67_108_864)
    reached = bytearray(dag.node_count+1)
    pending = array("I", roots.values())
    reached_count = 0
    while pending:
        old_id = int(pending.pop())
        require(1 <= old_id <= dag.node_count, "proof DAG root/reference range")
        if reached[old_id]:
            continue
        reached[old_id] = 1
        reached_count += 1
        if dag.kind[old_id-1] == dag.LINEAR:
            pending.extend(parent for parent, _ in dag.terms(old_id))
        if basis.deadline is not None and (reached_count & 4095) == 0:
            basis.deadline.check("proof_DAG_reachability")
    expression_roots = sorted({
        basis.sections.node_for(int(dag.leaf_translation[old_id-1])) -
        basis.sections.EXPR_TAG
        for old_id in range(1, dag.node_count+1)
        if reached[old_id] and dag.kind[old_id-1] == dag.LEAF and
        basis.sections.node_for(int(dag.leaf_translation[old_id-1])) >=
        basis.sections.EXPR_TAG
    })
    if expression_roots:
        section_expressions, expression_renumber = \
            basis.sections.expressions.serialize_reachable(
                expression_roots, basis.deadline)
    else:
        section_expressions = {
            "format": "typed-section-expression-arrays/v1",
            "node_order": "zero_based_topological",
            "ordinary_word_composition": True,
            "canonical_value_width": basis.pool.width,
            "node_count": 0, "edge_count": 0, "roots": [],
            "arrays": {}, "manifest_sha256": digest_obj({"arrays": {},
                                                           "roots": []}),
        }
        expression_renumber = {}
    renumber = array("I", [0]) * (dag.node_count+1)
    next_id = 0
    for old_id in range(1, dag.node_count+1):
        if reached[old_id]:
            next_id += 1
            renumber[old_id] = next_id
    kinds = bytearray()
    relators = array("H")
    translations = array("I")
    offsets = array("I", [0])
    parents = array("I")
    coefficients = bytearray()
    leaf_count = 0
    for old_id in range(1, dag.node_count+1):
        if not reached[old_id]:
            continue
        new_id = int(renumber[old_id])
        if basis.deadline is not None and new_id % 1024 == 0:
            basis.deadline.check("proof_DAG_compact_serialization")
        kind = dag.kind[old_id-1]
        if kind == dag.LEAF:
            internal_id = int(dag.leaf_translation[old_id-1])
            section_node = basis.sections.node_for(internal_id)
            if section_node < basis.sections.EXPR_TAG:
                section = basis.sections.materialize(section_node)
                require(basis.pool.eval_id(section) == internal_id,
                        "materialized lazy section evaluation")
                external_id = registry.add(
                    4, basis.pool.value(internal_id), section)
            else:
                expression_root = section_node-basis.sections.EXPR_TAG
                require(expression_root in expression_renumber and
                        basis.sections.expressions.value_blob(expression_root) ==
                        basis.pool.blob(internal_id),
                        "directed leaf expression binding")
                external_id = registry.add_expression(
                    4, basis.pool.value(internal_id),
                    expression_renumber[expression_root])
            kinds.append(1)
            relators.append(int(dag.leaf_relator[old_id-1]))
            translations.append(external_id)
            leaf_count += 1
        else:
            require(kind == dag.LINEAR, "packed proof DAG node kind")
            kinds.append(2)
            relators.append(0)
            translations.append(0)
            for parent, coefficient in dag.terms(old_id):
                require(reached[parent] and 0 < renumber[parent] < new_id and
                        coefficient in (1, 2), "proof DAG topological term")
                parents.append(int(renumber[parent]))
                coefficients.append(coefficient)
        offsets.append(len(parents))
    root_rows = [{"name": name, "node_id": int(renumber[node_id])}
                 for name, node_id in roots.items()]
    arrays = {
        "node_kind": _packed_array_block("uint8", "B", kinds,
                                          CAPS["provenance_dag_nodes"],
                                          basis.deadline),
        "leaf_relator_index": _packed_array_block(
            "uint16", "H", relators, CAPS["provenance_dag_nodes"],
            basis.deadline),
        "leaf_translation_element_id": _packed_array_block(
            "uint32", "I", translations, CAPS["provenance_dag_nodes"],
            basis.deadline),
        "edge_offsets": _packed_array_block(
            "uint32", "I", offsets, CAPS["provenance_dag_nodes"]+1,
            basis.deadline),
        "edge_parent_node_id": _packed_array_block(
            "uint32", "I", parents, CAPS["provenance_dag_edges"],
            basis.deadline),
        "edge_coefficient": _packed_array_block(
            "uint8", "B", coefficients, CAPS["provenance_dag_edges"],
            basis.deadline),
    }
    manifest = {
        name: {key: value for key, value in block.items() if key != "base64"}
        for name, block in arrays.items()
    }
    payload = {
        "format": "packed-parallel-arrays/v1",
        "field": 3,
        "node_order": "one_based_topological",
        "translation_action": "left",
        "section_expressions": section_expressions,
        "arrays": arrays,
        "roots": root_rows,
        "node_count": reached_count,
        "edge_count": len(parents),
        "leaf_count": leaf_count,
        "combination_node_count": reached_count-leaf_count,
        "all_serialized_nodes_reachable_from_roots": True,
        "unreachable_search_nodes_pruned": dag.node_count-reached_count,
        "expanded_boundary_ledgers_serialized": False,
        "packed_manifest_sha256": digest_obj({"arrays": manifest,
                                               "roots": root_rows}),
    }
    return payload, {old: int(renumber[old]) for old in roots.values()}


def encode_fox_model(model: dict[str, Any], quotient: MatchedQuotient,
                     registry: ElementRegistry) -> dict[str, Any]:
    rank = model["rank"]
    identity_id = registry.add(rank, quotient.identity, [])
    marked_ids = [registry.add(rank, value, [i])
                  for i, value in enumerate(quotient.generators, 1)]
    relator_rows = []
    for index, (word, gradient, sections) in enumerate(
            zip(model["relations"], model["columns"], model["sections"]), 1):
        relator_rows.append({
            "relator_index": index,
            "word": word,
            "quotient_identity": True,
            "gradient": encode_vector(rank, gradient, sections, registry),
            "D1_of_gradient_zero": True,
        })
    return {
        "rank": rank,
        "field": 3,
        "left_fox_convention": {
            "product_rule": "d(uv)=d(u)+u*d(v)",
            "positive_letter": "+prefix",
            "negative_letter": "advance prefix by x_i^-1, then -prefix",
            "D1": "sum_i coefficient*(q(x_i)-1) on the right",
            "translated_column": "left multiplication by the translation element",
        },
        "generator_count": len(quotient.generators),
        "relator_count": len(model["relations"]),
        "identity_element_id": identity_id,
        "marked_element_ids": marked_ids,
        "relator_columns": relator_rows,
        "D1D2_zero": True,
        "full_regular_matrix_constructed": False,
        "H1_basis_or_rank_constructed": False,
    }


@dataclass
class CompactCandidate:
    correction_index: int
    names: tuple[str, ...]
    kinds: tuple[str, ...]
    gradients: tuple[PackedSparseVector, ...]
    quotient_value_ids: tuple[int, ...]

    def accounting(self) -> dict[str, int]:
        return {"target_count": len(self.names),
                "sparse_entries": sum(len(row) for row in self.gradients)}


def candidate_gradients(candidate: dict[str, Any], pool: ElementPool,
                        correction_index: int) -> CompactCandidate:
    names: list[str] = []
    kinds: list[str] = []
    gradients: list[PackedSparseVector] = []
    values: list[int] = []
    for name, kind, word in candidate["targets"]:
        gradient, value = fox_gradient_packed(word, pool)
        require(value == pool.identity_id, f"candidate target not in H4: {name}")
        names.append(name)
        kinds.append(kind)
        gradients.append(gradient)
        values.append(value)
    return CompactCandidate(correction_index, tuple(names), tuple(kinds),
                            tuple(gradients), tuple(values))


def solve_candidate(candidate: CompactCandidate, basis: SparseBoundaryBasis) \
        -> dict[str, int] | None:
    checkpoint = basis.dag.checkpoint()
    answer: dict[str, int] = {}
    try:
        for name, gradient in zip(candidate.names, candidate.gradients):
            root = basis.solve(gradient)
            if root is None:
                basis.dag.rollback(checkpoint)
                return None
            answer[name] = root
        return answer
    except Exception:
        basis.dag.rollback(checkpoint)
        raise


def packed_gradient_binding(name: str, kind: str,
                            gradient: PackedSparseVector, value_id: int,
                            pool: ElementPool) -> dict[str, Any]:
    """Canonical binding retained across rollback without retaining the vector."""
    digest = hashlib.sha256()
    rows = sorted(gradient.items(), key=lambda row: pool.pivot_order(row[0]))
    for packed_key, coefficient in rows:
        component, element_id = unpack_vector_key(packed_key)
        blob = pool.blob(element_id)
        digest.update(component.to_bytes(1, "little"))
        digest.update(len(blob).to_bytes(2, "little"))
        digest.update(blob)
        digest.update(int(coefficient).to_bytes(1, "little"))
    return {
        "name": name,
        "kind": kind,
        "entry_count": len(rows),
        "quotient_value_hex": pool.blob(value_id).hex(),
        "canonical_gradient_sha256": digest.hexdigest(),
        "canonical_order": "component then exact canonical E4 bytes",
        "digest_is_binding_only_not_element_equality": True,
    }


def candidate_transaction_snapshot(pool: ElementPool, dag: ProvenanceDAG,
                                   basis: SparseBoundaryBasis,
                                   sections: SparseSectionOracle,
                                   extra_anchor_ids: Sequence[int] = ()) -> dict[str, Any]:
    """Snapshot before the first candidate-specific pool intern."""
    anchor_ids = [pool.identity_id] + list(pool.generator_ids) + \
        list(pool.inverse_generator_ids) + list(extra_anchor_ids)
    return {
        "pool": pool.checkpoint(),
        "dag": dag.checkpoint(),
        "basis_rows": len(basis.rows),
        "basis_live_entries": basis.live_vector_entries,
        "basis_columns": basis.columns_seen,
        "basis_dependent_columns": basis.dependent_columns,
        "section_nodes": len(sections.parent),
        "section_bindings": len(sections.by_element),
        "relator_column_count": len(basis.relator_columns),
        "anchor_bindings": [(identifier, pool.blob(identifier))
                            for identifier in anchor_ids],
    }


def rollback_candidate_transaction(snapshot: dict[str, Any], pool: ElementPool,
                                   dag: ProvenanceDAG,
                                   basis: SparseBoundaryBasis,
                                   sections: SparseSectionOracle) -> int:
    dag.rollback(tuple(snapshot["dag"]))
    removed = pool.rollback(int(snapshot["pool"]))
    require(len(basis.rows) == snapshot["basis_rows"] and
            basis.live_vector_entries == snapshot["basis_live_entries"] and
            basis.columns_seen == snapshot["basis_columns"] and
            basis.dependent_columns == snapshot["basis_dependent_columns"] and
            len(basis.relator_columns) == snapshot["relator_column_count"],
            "candidate rollback mutated persistent sparse basis")
    require(len(sections.parent) == snapshot["section_nodes"] and
            len(sections.by_element) == snapshot["section_bindings"],
            "candidate rollback mutated lazy BFS sections")
    require(len(pool.values) == snapshot["pool"] and
            len(pool.ids) == snapshot["pool"] and
            len(pool.product_cache.data) == 0 and
            len(pool.inverse_cache.data) == 0,
            "candidate rollback pool/LRU integrity")
    require(all(pool.blob(identifier) == blob and pool.ids.get(blob) == identifier
                for identifier, blob in snapshot["anchor_bindings"]),
            "candidate rollback persistent pool anchors")
    return removed


def make_base_receipt(q3_path: Path, output_path: Path, q3_data: dict[str, Any],
                      source_hashes: dict[str, str], status: str,
                      reason: str) -> dict[str, Any]:
    require(status in TERMINALS, "terminal")
    selected_q3 = q3_data.get("selected_solution", {})
    fixed_roof: dict[str, Any] = {
        "row_index": 37, "exponent": 2,
        "source": "frozen q3 selected outside roof",
    }
    # Populate every authenticated roof field before the first resource
    # monitor check.  Hence even an immediate soft-RSS/soft-wall stop has the
    # same fail-closed registered-universe schema as every later terminal.
    if selected_q3:
        fixed_roof.update({
            "roof_key": selected_q3["roof_key"],
            "typed_source_word": list(selected_q3["typed_source_word"]),
            "arithmetic_outside_by_index_three":
                selected_q3["arithmetic_outside_by_index_three"],
        })
    return {
        "schema": SCHEMA,
        "status": status,
        "terminal_token": status,
        "reason": reason,
        "pins": {
            "q3_producer": {"path": str(Q3_PRODUCER).replace("\\", "/"),
                            "sha256": Q3_PRODUCER_SHA},
            "q3_checker": {"path": str(Q3_CHECKER).replace("\\", "/"),
                           "sha256": Q3_CHECKER_SHA},
            "q3_driver": {"path": str(Q3_DRIVER).replace("\\", "/"),
                          "sha256": Q3_DRIVER_SHA},
            "q3_artifact": {"path": str(Q3_ARTIFACT_PATH).replace("\\", "/"),
                             "sha256": Q3_ARTIFACT_SHA},
            "semantic_reference_v8": {
                "producer": {"path": str(V8_PRODUCER).replace("\\", "/"),
                             "sha256": V8_PRODUCER_SHA},
                "checker": {"path": str(V8_CHECKER).replace("\\", "/"),
                            "sha256": V8_CHECKER_SHA},
                "driver": {"path": str(V8_DRIVER).replace("\\", "/"),
                           "sha256": V8_DRIVER_SHA},
                "role": "frozen candidate order, 33/17 predicate, WordExpr/Fox and terminal reference",
            },
            "semantic_reference_v7": {
                "producer": {"path": str(V7_PRODUCER).replace("\\", "/"),
                             "sha256": V7_PRODUCER_SHA},
                "checker": {"path": str(V7_CHECKER).replace("\\", "/"),
                            "sha256": V7_CHECKER_SHA},
                "driver": {"path": str(V7_DRIVER).replace("\\", "/"),
                           "sha256": V7_DRIVER_SHA},
                "role": "frozen saturated directed prefix and corrected Def2.9 reference",
            },
            "semantic_reference_v6": {
                "producer": {"path": str(V6_PRODUCER).replace("\\", "/"),
                             "sha256": V6_PRODUCER_SHA},
                "checker": {"path": str(V6_CHECKER).replace("\\", "/"),
                            "sha256": V6_CHECKER_SHA},
                "driver": {"path": str(V6_DRIVER).replace("\\", "/"),
                           "sha256": V6_DRIVER_SHA},
                "role": "frozen full-32768 fixed-candidate basis and cap reference",
            },
            "semantic_reference_v5": {
                "producer": {"path": str(V5_PRODUCER).replace("\\", "/"),
                             "sha256": V5_PRODUCER_SHA},
                "checker": {"path": str(V5_CHECKER).replace("\\", "/"),
                            "sha256": V5_CHECKER_SHA},
                "driver": {"path": str(V5_DRIVER).replace("\\", "/"),
                           "sha256": V5_DRIVER_SHA},
                "role": "frozen fixed-candidate v5 semantics and cap-stop reference",
            },
            "semantic_reference_v2": {
                "producer": {"path": str(V2_PRODUCER).replace("\\", "/"),
                             "sha256": V2_PRODUCER_SHA},
                "checker": {"path": str(V2_CHECKER).replace("\\", "/"),
                            "sha256": V2_CHECKER_SHA},
                "driver": {"path": str(V2_DRIVER).replace("\\", "/"),
                           "sha256": V2_DRIVER_SHA},
                "role": "frozen v2 mathematics, universe, gates, and search order",
            },
            "semantic_reference_v3": {
                "producer": {"path": str(V3_PRODUCER).replace("\\", "/"),
                             "sha256": V3_PRODUCER_SHA},
                "checker": {"path": str(V3_CHECKER).replace("\\", "/"),
                            "sha256": V3_CHECKER_SHA},
                "driver": {"path": str(V3_DRIVER).replace("\\", "/"),
                           "sha256": V3_DRIVER_SHA},
                "role": "frozen packed-v3 semantics and positive-certificate reference",
            },
            "semantic_reference_v4": {
                "producer": {"path": str(V4_PRODUCER).replace("\\", "/"),
                             "sha256": V4_PRODUCER_SHA},
                "checker": {"path": str(V4_CHECKER).replace("\\", "/"),
                            "sha256": V4_CHECKER_SHA},
                "driver": {"path": str(V4_DRIVER).replace("\\", "/"),
                           "sha256": V4_DRIVER_SHA},
                "role": "frozen transactional-v4 arithmetic, Fox, blocker, and packed-certificate reference",
            },
            "semantic_reference_v1": {
                "producer": {"path": str(V1_PRODUCER).replace("\\", "/"),
                             "sha256": V1_PRODUCER_SHA},
                "checker": {"path": str(V1_CHECKER).replace("\\", "/"),
                            "sha256": V1_CHECKER_SHA},
                "driver": {"path": str(V1_DRIVER).replace("\\", "/"),
                           "sha256": V1_DRIVER_SHA},
                "role": "frozen semantic predicate and search-order reference",
            },
            "formula_sha256": FORMULA_SHA,
        },
        "source_hashes": source_hashes,
        "input_q3_terminal": q3_data.get("terminal_token"),
        "output_path": str(OUTPUT_PATH).replace("\\", "/"),
        "caps": CAPS,
        "registered_universe": {
            "kind": "registered_4096_wordexpr_positive_search",
            "registered_corrections": 4096,
            "registered_dictionary_complete": True,
            "full_H3_fibre_complete": False,
            "fixed_outside_roof": fixed_roof,
            "full_universe_claimed": False,
            "earliest_global_candidate_claimed": False,
            "negative_completeness_claimed": False,
            **({"marking_m": 0, "lambda": 1} if selected_q3 else {}),
        },
        "representation_contract": {
            "version": "typed-wordexpr-memo-fusion-v9",
            "persistent_element_equality": "exact canonical bytes; never a digest",
            "sparse_keys": "component plus stable zero-based exact element-pool ID",
            "pivot_order": "component then canonical EKey bytes; never insertion ID",
            "BFS_order": "+1..+6,-1..-6 first-seen shortlex",
            "candidate_sections_retained": False,
            "candidate_wordexpr_retained_across_candidates": False,
            "substituted_descendants_flattened": False,
            "left_Fox_product_rule": "D(uv)=D(u)+value(u)*D(v)",
            "left_Fox_inverse_rule": "D(u^-1)=-value(u)^-1*D(u)",
            "negative_substitution_letter": "advance prefix by value(a_i)^-1, then subtract prefix*D(a_i)",
            "section_oracle": "BFS/direct translations only, canonical-byte-bound typed expression DAG",
            "all_element_pool_values_have_sections": False,
            "candidate_gradients_retained_across_checkpoints": False,
            "candidate_local_typed_gradient_memo": True,
            "memo_key": "typed node identity + rank/arity + candidate + quotient/presentation + leaf bindings",
            "memo_cross_candidate_entries": 0,
            "source_anchor_pin_policy_stage_aware":
                "candidate1 after direct gate; ordinary at target 17 only; proof fresh; retention best effort",
            "cache_capacity_is_nonterminal": True,
            "static_quotient_binding_reused_across_candidates": True,
            "fixed_inverse_and_target_order_hashes_reused": True,
            "bridge_membership_fused_for_candidate_1": True,
            "candidate_1_bridge_target_count": 50,
            "memo_and_bridge_Fox_prefix_sections_materialized": False,
            "scan_wordexpr_live_gradient_peak_field":
                "max requested target support; true working+cached peak is in gradient_memo_performance",
            "candidate_transaction": "exact element-pool and provenance-DAG suffix rollback",
            "missing_pivot_blocker": "target ordinal, component, canonical E4 bytes",
            "proof_DAG_in_memory": "packed parallel arrays",
            "positive_DAG_serialization": "reachable union as typed little-endian base64 arrays",
            "cache_eviction_semantics": "capacity and eviction order affect speed only, never canonical values or search order",
            "persistent_checkpoint_resume": False,
            "correction_dictionary_constructed": True,
            "complete_source_tuple_DP_executed_before_sparse_growth": True,
            "cap_calibration_only": False,
            "resume_or_checkpoint_imported": False,
        },
        "claim_classification": "unknown_not_obstruction",
        "claim_scope": "registered_4096_wordexpr_positive_search_only",
        "no_mathematical_obstruction_claimed": True,
        "full_universe_claimed": False,
        "negative_claimed": False,
        "theorem_boundary": {
            "proved_if_PASS": "one registered literal outside pair survives every isolated elementary-F3 chief refinement L with Phi3(H4)<=L<=H4",
            "Phi3_H4_isolation_required": False,
            "covered": "all isolated elementary-F3 next-chief refinements immediately below current H4",
            "not_covered": ["nonabelian chief factors", "other primes",
                            "deeper iteration", "uniform cofinal tower", "global B4-B"],
        },
        "prohibited_work": {
            "relative_ANUPQ_calls": 0,
            "Reidemeister_Schreier": False,
            "full_Elements": False,
            "full_regular_matrices": False,
            "full_H1_basis_or_rank": False,
            "registered_corrections": 4096,
            "all_dictionary_DP_executed": False,
        },
        "cap_calibration": dict(CAP_CALIBRATION),
    }


def _v2_reference_run(q3_path: Path, output_path: Path) -> dict[str, Any]:
    run_start = time.monotonic()
    phase_start = run_start
    deadline = SoftDeadline(run_start, CAPS["producer_soft_timeout_seconds"])
    basis: SparseBoundaryBasis | None = None
    repo = Path(__file__).resolve().parents[1]
    require(q3_path.resolve() == (repo/Q3_ARTIFACT_PATH).resolve() and
            output_path.resolve() == (repo/OUTPUT_PATH).resolve(),
            "production paths must be the fixed ci/out paths")
    for path, sha, label in ((repo/Q3_PRODUCER, Q3_PRODUCER_SHA, "q3 producer"),
                             (repo/Q3_CHECKER, Q3_CHECKER_SHA, "q3 checker"),
                             (repo/Q3_DRIVER, Q3_DRIVER_SHA, "q3 driver"),
                             (repo/V1_PRODUCER, V1_PRODUCER_SHA, "v1 producer"),
                             (repo/V1_CHECKER, V1_CHECKER_SHA, "v1 checker"),
                             (repo/V1_DRIVER, V1_DRIVER_SHA, "v1 driver")):
        require(digest_file(path) == sha, f"{label} SHA")
    require(digest_file(q3_path) == Q3_ARTIFACT_SHA, "q3 artifact SHA")
    q3_data = json.loads(q3_path.read_text(encoding="utf-8"))
    source_hashes = {
        "producer_sha256": digest_file(Path(__file__)),
        "checker_sha256": digest_file(repo/"search/check_d972_b345_relfrat3_v2.py"),
        "driver_sha256": digest_file(repo/"search/d972_b345_relfrat3_gha_driver_v2.g"),
    }
    receipt = make_base_receipt(q3_path, output_path, q3_data, source_hashes,
                                "B345_RELFRAT3_UNKNOWN_RESOURCE",
                                "initializing")
    receipt["soft_timeout"] = deadline.receipt(False)
    try:
        deadline.check("formula_reconstruction")
        require(digest_obj(q3_data["formulas"]) == FORMULA_SHA,
                "q3 full formula digest")
        formula = relevant_formula()
        q3_formula = q3_data["formulas"]
        require(formula["presentations"]["PB3"]["relations"] ==
                q3_formula["presentations"]["PB3"]["relations"] and
                formula["presentations"]["PB4"]["relations"] ==
                q3_formula["presentations"]["PB4"]["relations"] and
                formula["presentations"]["PB5"]["relations"] ==
                q3_formula["presentations"]["PB5"]["relations"] and
                formula["cofaces_3_4"] == q3_formula["cofaces_3_4"] and
                formula["a18_order"]["maps"] == q3_formula["a18_order"]["maps"],
                "relevant formula reconstruction")
        e3, e4, context = reconstruct_quotients(q3_data)
        receipt["formula_sha256"] = FORMULA_SHA
        receipt["relevant_formula"] = formula
        receipt["relevant_formula_sha256"] = digest_obj(formula)
        receipt["matched_quotients"] = {
            "E3": {"coarse_degree": e3.degree, "fine_pc_rank": e3.pc.n,
                   "definition": "Q0 x Pi3[3]; its kernel J_H is the authenticated coarse source correction kernel"},
            "E4": {"coarse_degree": e4.degree, "fine_pc_rank": e4.pc.n,
                   "definition": "Q4 x Pi4[3] from the frozen no-common-C3 gate"},
            "J_H": {"definition": "kernel(PB3 -> E3), with every selected correction also replayed through all five cofaces into H4"},
            "J_Phi": {
                "definition": "intersection_{j=0}^4 (coface_j)^-1 Phi3(H4)",
                "identified_with_Phi3_H3": False,
                "correction_membership_required": False,
                "quotient_J_H_over_J_Phi_is_lift_freedom": True,
            },
        }
        phase_start = phase("matched_quotients", phase_start)
        deadline.check("base_replay_dictionary")
        base_replay = replay_base_q3(q3_data, e3, e4)
        receipt["base_q3_replay"] = base_replay
        dictionary = correction_dictionary(q3_data, e3)
        receipt["correction_dictionary"] = dictionary
        phase_start = phase("base_replay_dictionary", phase_start)

        model3 = fox_model(3, e3)
        model4 = fox_model(4, e4)
        dag = ProvenanceDAG(deadline)
        basis = SparseBoundaryBasis(e4, model4["columns"], dag, deadline)
        normalized_inverse, base_source_key, finite_inverse_words = \
            normalized_inverse_fibre(q3_data, e4)
        receipt["normalized_inverse_fibre"] = normalized_inverse
        inverse_cache: dict[tuple[EKey, ...], list[list[int]]] = {
            base_source_key: finite_inverse_words,
        }
        inverse_cache_stats = {"hits": 0, "misses": 0,
                               "max_inverse_word_length":
                                   normalized_inverse["max_inverse_word_length"]}
        prepared: list[tuple[int, dict[str, Any]]] = []
        cheap_rejected: list[dict[str, Any]] = []
        resource_skips: list[dict[str, Any]] = []
        for correction_index, correction in enumerate(dictionary["words"], 1):
            deadline.check("cheap_candidate_preparation")
            try:
                candidate = prepare_candidate(
                    reduce_word(FIXED_WORD + correction), correction, e4)
            except ResourceStop as exc:
                if exc.reason == "producer_soft_timeout":
                    raise
                resource_skips.append({"candidate_index": correction_index,
                                       "phase": "cheap_candidate_preparation",
                                       "reason": exc.reason})
                continue
            if candidate["quotient_bad"]:
                cheap_rejected.append({"candidate_index": correction_index,
                                       "failed_gates": candidate["quotient_bad"]})
            else:
                prepared.append((correction_index, candidate))
        require(not any(row["candidate_index"] == 1 for row in cheap_rejected),
                "empty correction failed the exact cheap quotient gates")
        selected_candidate: dict[str, Any] | None = None
        selected_rows: list[tuple[str, str, list[int], SparseVector,
                                  dict[EKey, list[int]]]] = []
        selected_roots: dict[str, int] | None = None
        candidate_cache: dict[int, tuple[dict[str, Any],
                                         list[tuple[str, str, list[int], SparseVector,
                                                    dict[EKey, list[int]]]]]] = {}
        unusable_candidates: set[int] = set()
        full_quotient_rejected: list[dict[str, Any]] = []
        geometric_checkpoints: list[int] = []
        translations_used = 0
        tests = 0
        translate_cap = CAPS["coefficient_translates_per_relator"]
        for translation, section in translation_bfs(e4, translate_cap):
            deadline.check("translation_BFS")
            translations_used += 1
            for relator_index in range(1, len(model4["columns"])+1):
                basis.add_column(relator_index, translation, section)
            if (translations_used & (translations_used-1)) == 0:
                geometric_checkpoints.append(translations_used)
                # Empty stays first.  Starting at checkpoint 8, every cheap
                # survivor is tried in the registered dictionary order; no
                # survivor waits for the final 32768-column cap.
                checkpoint_candidates = prepared if translations_used >= 8 else prepared[:1]
                for correction_index, candidate in checkpoint_candidates:
                    deadline.check("geometric_candidate_checkpoint")
                    if correction_index in unusable_candidates:
                        continue
                    if correction_index not in candidate_cache:
                        try:
                            candidate = complete_candidate(
                                candidate, e4, inverse_cache,
                                inverse_cache_stats, normalized_inverse)
                            if candidate["quotient_bad"]:
                                full_quotient_rejected.append({
                                    "candidate_index": correction_index,
                                    "failed_gates": candidate["quotient_bad"],
                                })
                                unusable_candidates.add(correction_index)
                                continue
                            rows = candidate_gradients(candidate, e4)
                            candidate_cache[correction_index] = (candidate, rows)
                        except ResourceStop as exc:
                            if exc.reason == "producer_soft_timeout":
                                raise
                            resource_skips.append({
                                "candidate_index": correction_index,
                                "phase": "inverse_or_gradient",
                                "reason": exc.reason,
                            })
                            unusable_candidates.add(correction_index)
                            continue
                    candidate, rows = candidate_cache[correction_index]
                    tests += 1
                    try:
                        roots = solve_candidate(rows, basis)
                    except ResourceStop as exc:
                        if exc.reason == "producer_soft_timeout":
                            raise
                        resource_skips.append({
                            "candidate_index": correction_index,
                            "phase": "sparse_membership",
                            "reason": exc.reason,
                        })
                        unusable_candidates.add(correction_index)
                        candidate_cache.pop(correction_index, None)
                        continue
                    if roots is not None:
                        selected_candidate, selected_rows = candidate, rows
                        selected_roots = roots
                        selected_candidate["correction_index"] = correction_index
                        break
                if selected_candidate is not None:
                    break
            if translations_used % 128 == 0:
                print("D972_B345_RELFRAT3_SEARCH "
                      f"translations={translations_used} basis={len(basis.rows)} "
                      f"live_vectors={basis.live_vector_entries} "
                      f"dag_nodes={len(dag.nodes)} dag_edges={dag.edge_count}",
                      flush=True)

        receipt["search"] = {
            "method": "one shared incremental sparse Gaussian basis with immutable F3 provenance DAG",
            "translation_order": "BFS shortlex steps +1..+6,-1..-6",
            "translations_used": translations_used,
            "translates_per_relator": translations_used,
            "columns_seen": basis.columns_seen,
            "dependent_columns": basis.dependent_columns,
            "basis_size": len(basis.rows),
            "pivot_count": len(basis.rows),
            "live_sparse_vector_entries": basis.live_vector_entries,
            "max_pivot_vector_support": basis.max_vector_support,
            "max_transient_vector_support": basis.max_transient_vector_support,
            "elimination_operations": basis.elimination_operations,
            "provenance_DAG": {
                **dag.accounting(),
                "pivot_payload": "one sparse vector plus one DAG node id",
                "expanded_pivot_ledgers_stored": False,
                "failed_column_and_candidate_nodes_rolled_back": True,
                "positive_serialization": "root-reachable union only",
            },
            "candidate_membership_tests": tests,
            "same_basis_reused_for_all_candidates": True,
            "candidate_order": "empty first, then registered correction dictionary order",
            "cheap_candidates_evaluated": len(dictionary["words"]),
            "cheap_gate_evaluation": "direct E4 values without substituted-word materialization",
            "full_words_materialized_only_for_cheap_survivors": True,
            "cheap_survivor_indices": [index for index, _ in prepared],
            "cheap_rejected": cheap_rejected,
            "full_candidate_cache_size": len(candidate_cache),
            "full_quotient_rejected": full_quotient_rejected,
            "geometric_translation_checkpoints": geometric_checkpoints,
            "all_cheap_survivors_scheduled_from_checkpoint": 8,
            "candidate_resource_skips": resource_skips,
            "settled_automorphism_order_cache_size": len(inverse_cache),
            "quotient_inverse_cache": {
                "key": "exact ordered tuple of six E4 source images",
                "entries": len(inverse_cache),
                "hits": inverse_cache_stats["hits"],
                "misses": inverse_cache_stats["misses"],
                "tuple_match_count": inverse_cache_stats["hits"],
                "tuple_mismatch_count": inverse_cache_stats["misses"],
                "max_inverse_word_length":
                    inverse_cache_stats["max_inverse_word_length"],
                "cached_datum": "one pinned normalized exponent-seven full inverse word tuple",
                "cache_hit_replays_current_ST_in_E4": True,
                "TS_replay_is_diagnostic_only": True,
                "different_tuple_is_candidate_local_UNKNOWN": True,
                "raw_endomorphism_powering_fallback": False,
                "candidate_relations_gradients_proof_roots_reused": False,
                "componentwise_Q4_Pi4_inverse_words_combined": False,
            },
            "cheap_quotient_gates_precede_power_inverse": True,
            "raw_power_inverse_removed": True,
            "small_projection_used": False,
            "affine_candidates_used": 0,
            "bounded_failure_is_not_nonexistence": True,
            "nonpositive_result_is_obstruction": False,
        }
        if selected_candidate is None:
            if resource_skips:
                receipt["status"] = receipt["terminal_token"] = \
                    "B345_RELFRAT3_UNKNOWN_RESOURCE"
                reason_counts: dict[str, int] = {}
                for row in resource_skips:
                    reason_counts[row["reason"]] = reason_counts.get(row["reason"], 0) + 1
                receipt["reason"] = (
                    "one or more registered candidates hit a local resource cap; "
                    "the skipped candidates are not treated as failures")
                receipt["resource_stop"] = {
                    "candidate_local": True,
                    "reason_counts": reason_counts,
                    "skipped_candidates": resource_skips,
                    "no_mathematical_obstruction_claimed": True,
                }
            else:
                receipt["status"] = receipt["terminal_token"] = \
                    "B345_RELFRAT3_SEARCH_INCOMPLETE"
                receipt["reason"] = (
                    "registered translated-relator and correction caps exhausted without a full "
                    "proof root; no obstruction or nonexistence is claimed")
            receipt["direct_lane"] = {
                "literal_pair_found": False,
                "PB5_branch_constructed": False,
                "PB5_reason": "direct sparse membership itself remained incomplete, so B5 was not used to turn a search miss into a negative",
            }
            receipt["claim_classification"] = "unknown_not_obstruction"
            receipt["soft_timeout"] = deadline.receipt(False)
            receipt["performance"] = {"runtime_seconds": time.monotonic()-run_start,
                                      "phase_complete": "bounded_search"}
            return receipt

        require(selected_roots is not None, "selected proof roots missing")
        registry = ElementRegistry({3: e3, 4: e4})
        encoded_models = {
            "PB3": encode_fox_model(model3, e3, registry),
            "PB4": encode_fox_model(model4, e4, registry),
            "PB5": {"constructed": False,
                    "reason": "direct B3/B4 literal pair certified first"},
        }
        ordered_roots = {name: selected_roots[name]
                         for name, _, _, _, _ in selected_rows}
        proof_dag, root_renumber = serialize_proof_dag(
            dag, ordered_roots, basis, registry)
        certificates = []
        for name, kind, word, _, _ in selected_rows:
            deadline.check("boundary_certificate_serialization")
            certificates.append(boundary_certificate(
                name, kind, word, e4,
                root_renumber[selected_roots[name]], registry))
        receipt["quotient_element_registry"] = registry.rows
        receipt["fox_models"] = encoded_models
        receipt["boundary_proof_dag"] = proof_dag
        receipt["search"]["provenance_DAG"]["serialized_reachable_nodes"] = \
            proof_dag["node_count"]
        receipt["search"]["provenance_DAG"]["serialized_reachable_edges"] = \
            proof_dag["edge_count"]
        correction_index = selected_candidate.get("correction_index", 1)
        selected_public = {key: value for key, value in selected_candidate.items()
                           if key not in ("targets", "quotient_bad") and
                           not key.startswith("_")}
        selected_public["correction_index"] = correction_index
        selected_public["boundary_certificate_names"] = [x["name"] for x in certificates]
        selected_public["correction_coarse_J_H_all_five_replayed"] = True
        selected_public["correction_finer_J_Phi_membership_not_required"] = True
        selected_public["all_ten_hexagon_coface_memberships_certified"] = True
        selected_public["ordered_A18_pentagon_certified"] = True
        selected_public["S_and_T_relations_certified"] = True
        selected_public["ST_and_TS_generator_compositions_certified"] = True
        receipt["selected_pair"] = selected_public
        receipt["boundary_certificates"] = certificates
        receipt["literal_replay"] = {
            "correction_lift_freedom": {
                "coarse_J_H_all_five_cofaces_identity": True,
                "finer_J_Phi_membership_required": False,
                "J_H_mod_J_Phi_coset_is_varied": True,
            },
            "hexagon": {"two_source_residuals": True,
                         "each_checked_in_all_five_cofaces": True},
            "pentagon": {"ordered_five_coface_A18_direct_PB4_residual": True},
            "charming": {"explicit_commutator_product": True,
                          "error_checked_in_all_five_cofaces": True,
                          "raw_exponent_sums_used_as_criterion": False},
            "marking": {"m": 0, "lambda": 1, "additional_residuals": []},
            "onto": {"two_sided_inverse_on_six_marked_generators": True,
                     "PB4_relations_for_both_maps": True},
        }
        receipt["status"] = receipt["terminal_token"] = \
            "B345_RELFRAT3_LITERAL_PAIR_PASS"
        receipt["claim_classification"] = "positive_certificate"
        receipt["reason"] = "one coarse-J_H correction coset gives literal hexagon, pentagon, charming, and two-sided onto residuals with an exact shared sparse Phi3(H4) provenance DAG"
        receipt["direct_lane"] = {"literal_pair_found": True,
                                  "PB5_branch_constructed": False,
                                  "stop_reason": "FIRST_LITERAL_PAIR_AT_PHI"}
        receipt["performance"] = {
            "runtime_seconds": time.monotonic()-run_start,
            "phase_complete": "literal_pair",
            "quotient_registry_size": len(registry.rows),
            "cache_policy": "quotient values, Fox gradients, translated columns, sparse pivots, shared DAG nodes, and sections cached",
        }
        receipt["soft_timeout"] = deadline.receipt(False)
        return receipt
    except AffineInput as exc:
        receipt["status"] = receipt["terminal_token"] = \
            "B345_SEEDSPAN_TRIPLE4_UNKNOWN_INPUT"
        receipt["reason"] = str(exc)
        receipt["input_errors"] = {"authenticated_external_input": str(exc),
                                    "mathematical_scan_started": True}
        receipt["resource_guards"] = affine_monitor_receipt(monitor, False)
        receipt["performance"] = {"runtime_seconds": time.monotonic()-start,
                                   "phase_complete": phase_name}
        return receipt
    except ResourceStop as exc:
        receipt["status"] = receipt["terminal_token"] = \
            "B345_RELFRAT3_UNKNOWN_RESOURCE"
        receipt["reason"] = exc.reason
        receipt["resource_stop"] = {"cap": exc.reason,
                                    "no_mathematical_obstruction_claimed": True}
        if basis is not None:
            receipt["resource_accounting_at_stop"] = basis.accounting()
        receipt["claim_classification"] = "unknown_not_obstruction"
        receipt["soft_timeout"] = deadline.receipt(
            exc.reason == "producer_soft_timeout")
        receipt["performance"] = {"runtime_seconds": time.monotonic()-run_start,
                                  "phase_complete": "resource_stop"}
        return receipt


def _pool_order_digest(pool: ElementPool,
                       monitor: ResourceMonitor | None = None) -> str:
    digest = hashlib.sha256()
    for index, blob in enumerate(pool.values, 1):
        require(len(blob) == pool.width, "pool digest width")
        digest.update(blob)
        if monitor is not None and (index & 4095) == 0:
            monitor.check("element_pool_binding_digest")
    return digest.hexdigest()


def _combined_pc_cache(e3: MatchedQuotient | None,
                       e4: MatchedQuotient | None) -> dict[str, Any]:
    rows = [] if e3 is None or e4 is None else [e3.pc.cache_accounting(),
                                                e4.pc.cache_accounting()]
    return {
        "collectors": rows,
        "hits": sum(row["hits"] for row in rows),
        "misses": sum(row["misses"] for row in rows),
        "evictions": sum(row["evictions"] for row in rows),
        "unbounded_full_token_word_cache": False,
    }


def finish_wordexpr_scan(
        receipt: dict[str, Any], dictionary: dict[str, Any],
        source_tuples: Sequence[tuple[EKey, ...]],
        raw_base_source_key: tuple[EKey, ...],
        finite_inverse_words: Sequence[Sequence[int]],
        direct_flat_candidate: dict[str, Any],
        e3: MatchedQuotient, e4: MatchedQuotient,
        pool: ElementPool, sections: SparseSectionOracle,
        dag: ProvenanceDAG, basis: SparseBoundaryBasis,
        model3: dict[str, Any], model4: dict[str, Any],
        monitor: ResourceMonitor, run_start: float,
        phase_timings: dict[str, float], search_accounting: dict[str, Any],
        base_source_key: tuple[int, ...], refresh_prefix: Any) -> dict[str, Any]:
    """Scan the complete registered dictionary against one immutable basis."""
    require(len(dictionary["words"]) == len(source_tuples) == 4096,
            "WordExpr full registered scan inputs")
    records: list[dict[str, Any]] = []
    receipt["_wordexpr_scan_records"] = records
    receipt["_wordexpr_scan_current"] = None
    selected: dict[str, Any] | None = None
    scan_start = time.monotonic()
    last_progress = scan_start
    progress = MemoProgress(run_start, monitor)
    memo_performance: dict[str, Any] = {
        "format": "candidate-local-typed-gradient-memo-summary/v1",
        "candidate_evaluators": 0,
        "proof_regeneration_evaluators": 0,
        "hits": 0, "misses": 0, "evictions": 0,
        "recomputations": 0, "skipped_oversize": 0,
        "peak_cached_nodes": 0,
        "peak_cached_sparse_entries": 0,
        "peak_working_plus_cached_sparse_entries": 0,
        "source_roots_requested_per_pin_stage":
            CAPS["gradient_memo_pinned_source_roots"],
        "pin_policy":
            "candidate1 after direct gate before 50 bridge; ordinary only before acceptance target 17; proof fresh evaluator",
        "ordinary_lazy_pin_target_ordinal": 17,
        "candidate1_bridge_pin_stages": 0,
        "ordinary_lazy_pin_stages": 0,
        "proof_pin_stages": 0,
        "pin_stage_count": 0,
        "pin_requests_total": 0,
        "pin_store_fallbacks": 0,
        "pin_evictions": 0,
        "peak_retained_pinned_source_count": 0,
        "direct_failures_before_pin": 0,
        "ordinary_exits_before_target17": 0,
        "cross_candidate_cache_entries": 0,
        "candidate_memos_discarded_at_rollback": 0,
        "phase_elapsed_seconds": {
            "value_evaluation": 0.0, "source_anchor_pin": 0.0,
            "candidate1_bridge_and_membership": 0.0,
            "ordinary_membership": 0.0,
            "proof_regeneration": 0.0,
        },
        "progress_interval_seconds": CAPS["progress_interval_seconds"],
        "static_quotient_binding_precomputed_once": True,
        "inverse_words_binding_precomputed_once": True,
        "target_order_binding_hashes_computed_once": True,
    }
    receipt["_memo_performance"] = memo_performance

    memo_static_binding = build_memo_static_quotient_binding(e4)
    finite_inverse_words = tuple(
        tuple(int(letter) for letter in word)
        for word in finite_inverse_words)
    inverse_words_sha256 = digest_obj(finite_inverse_words)
    target_order_cache: dict[str, Any] = {
        "acceptance": None, "diagnostic": None,
        "acceptance_sha256": None, "diagnostic_sha256": None,
    }

    def absorb_memo(evaluator: WordExprEvaluator, *, proof: bool = False,
                    discarded: bool = False) -> None:
        row = evaluator.memo.accounting()
        memo_performance["proof_regeneration_evaluators" if proof else
                         "candidate_evaluators"] += 1
        for key in ("hits", "misses", "evictions", "recomputations",
                    "skipped_oversize", "pin_store_fallbacks",
                    "pin_evictions"):
            memo_performance[key] += row[key]
        for key in ("peak_cached_nodes", "peak_cached_sparse_entries",
                    "peak_working_plus_cached_sparse_entries"):
            memo_performance[key] = max(memo_performance[key], row[key])
        if discarded:
            memo_performance["candidate_memos_discarded_at_rollback"] += 1
        memo_performance["pin_requests_total"] += row["requested_source_count"]
        memo_performance["peak_retained_pinned_source_count"] = max(
            memo_performance["peak_retained_pinned_source_count"],
            row["pinned_source_count"])

    def evaluator_binding(compiled: dict[str, Any]) -> dict[str, Any]:
        acceptance_order = [(name, kind) for name, kind, _ in
                            compiled["acceptance"]]
        diagnostic_order = [(name, kind) for name, kind, _ in
                            compiled["diagnostics"]]
        if target_order_cache["acceptance"] is None:
            target_order_cache["acceptance"] = acceptance_order
            target_order_cache["diagnostic"] = diagnostic_order
            target_order_cache["acceptance_sha256"] = \
                digest_obj(acceptance_order)
            target_order_cache["diagnostic_sha256"] = \
                digest_obj(diagnostic_order)
        else:
            require(acceptance_order == target_order_cache["acceptance"] and
                    diagnostic_order == target_order_cache["diagnostic"],
                    "candidate acceptance/diagnostic order drift")
        return {
            "schema": SCHEMA,
            "candidate_index": compiled["correction_index"],
            "correction_word_sha256": digest_obj(compiled["correction_word"]),
            "candidate_word_sha256": digest_obj(compiled["candidate_word"]),
            "inverse_words_sha256": inverse_words_sha256,
            "acceptance_order_sha256":
                target_order_cache["acceptance_sha256"],
            "diagnostic_order_sha256":
                target_order_cache["diagnostic_sha256"],
        }

    def run_pin_stage(evaluator: WordExprEvaluator,
                      roots: Sequence[int], stage: str) -> None:
        require(stage in {"candidate1_bridge", "ordinary_target17",
                          "proof_regeneration"}, "memo pin stage")
        phase_mark = time.monotonic()
        progress.bind(phase="source_anchor_pin", evaluator=evaluator)
        evaluator.pin_source_roots(roots)
        memo_performance["phase_elapsed_seconds"]["source_anchor_pin"] += \
            time.monotonic()-phase_mark
        memo_performance["pin_stage_count"] += 1
        field = {"candidate1_bridge": "candidate1_bridge_pin_stages",
                 "ordinary_target17": "ordinary_lazy_pin_stages",
                 "proof_regeneration": "proof_pin_stages"}[stage]
        memo_performance[field] += 1
        progress.emit(boundary=True,
                      anchor_progress=len(evaluator.memo.pinned_keys))
    transaction = {
        "membership_starts": 0, "membership_rollbacks": 0,
        "proof_starts": 0, "proof_commits": 0, "proof_rollbacks": 0,
        "failed_candidate_DAG_nodes_allocated": 0,
        "max_pool_suffix": 0, "max_live_gradient_entries": 0,
    }
    # Keep the active scan accounting reachable by the outer ResourceStop
    # serializer; this is distinct from the historical v7 directed-prefix
    # transaction ledger.
    receipt["_wordexpr_transaction"] = transaction
    zero_blob = _element_blob(e4.identity)
    progress.bind(phase="wordexpr_scan_start")
    progress.emit(boundary=True)

    flat_rows = (list(direct_flat_candidate["targets"]) +
                 list(direct_flat_candidate["diagnostic_targets"]))

    def expression_digest(expr: WordExprDAG) -> str:
        return digest_obj({
            "opcode": expr.opcode, "rank": expr.rank,
            "word": [list(x) for x in expr.word],
            "children": [list(x) for x in expr.children],
            "expanded_count": expr.expanded_count,
        })

    def diagnostic_rows(compiled: dict[str, Any], evaluator: WordExprEvaluator) \
            -> list[dict[str, Any]]:
        rows = []
        for name, kind, root in compiled["diagnostics"]:
            value = evaluator.values[root-1]
            rows.append({
                "name": name, "kind": kind,
                "root": root,
                "quotient_value_hex": _element_blob(value).hex(),
                "quotient_identity": value == e4.identity,
                "feeds_acceptance": False,
                "Fox_membership_tested": False,
            })
        return rows

    def direct_gate_failure(compiled: dict[str, Any],
                            evaluator: WordExprEvaluator) \
            -> tuple[str | None, int]:
        for name, root in compiled["correction_coface_roots"]:
            if evaluator.values[root-1] != e4.identity:
                return name, 0
        for ordinal, (name, _, root) in enumerate(compiled["acceptance"], 1):
            if evaluator.values[root-1] != e4.identity:
                return name, ordinal
        return None, 0

    def candidate1_flat_bridge(compiled: dict[str, Any],
                               evaluator: WordExprEvaluator,
                               pool_before: int) -> dict[str, Any]:
        expr_rows = list(compiled["acceptance"])+list(compiled["diagnostics"])
        require([(a, b) for a, b, _ in expr_rows] ==
                [(a, b) for a, b, _ in flat_rows] and len(expr_rows) == 50,
                "candidate1 flat bridge target order")
        bindings = []
        acceptance_bindings: list[dict[str, Any]] = []
        missing_key: int | None = None
        missing_name = ""
        missing_kind = ""
        missing_ordinal = 0
        total_entries = 0
        reused_membership = 0
        for bridge_ordinal, ((name, kind, root), (_, _, flat_word)) in \
                enumerate(zip(expr_rows, flat_rows), 1):
            monitor.check("candidate1_bridge_target")
            progress.bind(
                phase="candidate1_bridge_and_membership", candidate=1,
                target_ordinal=bridge_ordinal, target_name=name,
                component=0, blocker=("missing_already_recorded"
                                      if missing_key is not None else
                                      "bridge_differential"),
                evaluator=evaluator,
                pool_suffix=len(pool.values)-pool_before)
            progress.emit(boundary=True, node=root)
            require(compiled["dag"].expanded_count[root-1] <=
                    CAPS["single_word_or_section_length"],
                    "candidate1 flat bridge expanded cap")
            expanded = compiled["dag"].expand_reduced_below_flat_cap(root)
            require(expanded == flat_word, f"candidate1 literal bridge word: {name}")
            expression_gradient = evaluator.evaluate_gradients([root])[root]
            flat_gradient, flat_value = fox_gradient_without_sections(
                flat_word, e4, progress.hook)
            require(flat_value == evaluator.values[root-1] and
                    flat_gradient == expression_gradient,
                    f"candidate1 literal bridge Fox/value: {name}")
            bindings.append(raw_gradient_binding(
                name, kind, expression_gradient, evaluator.values[root-1]))
            # Fuse only the original ordered acceptance prefix.  Once the
            # first missing pivot is known, finish all remaining canaries but
            # do not pay a second membership/reduction for that target.
            if bridge_ordinal <= 33 and missing_key is None:
                value = evaluator.values[root-1]
                require(value == e4.identity,
                        f"candidate1 acceptance quotient identity: {name}")
                binding = bindings[-1]
                acceptance_bindings.append(binding)
                total_entries += len(expression_gradient)
                packed = intern_raw_vector(expression_gradient, pool)
                suffix = len(pool.values)-pool_before
                transaction["max_pool_suffix"] = max(
                    transaction["max_pool_suffix"], suffix)
                if suffix > CAPS["candidate_element_pool_suffix"]:
                    raise ResourceStop(
                        "candidate_element_pool_suffix",
                        cap_key="candidate_element_pool_suffix",
                        cap_limit=CAPS["candidate_element_pool_suffix"],
                        observed_count=suffix, trigger_relation="gt")
                missing_key = membership_reduce_fixed_basis(packed, basis)
                reused_membership += 1
                if missing_key is not None:
                    missing_name, missing_kind = name, kind
                    missing_ordinal = bridge_ordinal
                    component, _ = unpack_vector_key(missing_key)
                    progress.bind(component=component, blocker="missing_pivot",
                                  pool_suffix=suffix)
                    progress.emit(boundary=True, node=root)
        require(len(bindings) == 50 and reused_membership >= 1,
                "candidate1 complete fused bridge")
        public = {
            "mandatory": True, "target_count": 50,
            "acceptance_target_count": 33,
            "diagnostic_target_count": 17,
            "original_target_order_preserved": True,
            "all_reduced_words_equal": True,
            "all_quotient_values_equal": True,
            "all_left_Fox_gradients_equal": True,
            "cold_route": "frozen v8 flat literal fox_gradient",
            "memo_route": "candidate-local typed WordExpr chain rule",
            "bindings_sha256": digest_obj(bindings),
            "old_flat_cap": CAPS["single_word_or_section_length"],
            "membership_fused": True,
            "membership_reused_target_count": reused_membership,
            "first_missing_target_ordinal": missing_ordinal,
            "first_missing_target_name": missing_name or None,
            "remaining_canaries_completed_after_first_missing":
                50-missing_ordinal if missing_ordinal else 0,
            "missing_target_re_evaluated": False,
            "memo_binding": evaluator.memo.accounting(),
        }
        return {
            "public": public,
            "bindings": acceptance_bindings,
            "missing_key": missing_key,
            "missing_name": missing_name,
            "missing_kind": missing_kind,
            "missing_ordinal": missing_ordinal,
            "total_entries": total_entries,
        }

    for correction_index, correction in enumerate(dictionary["words"], 1):
        receipt["_wordexpr_scan_current"] = {
            "candidate_index": correction_index, "target_ordinal": 0,
            "target_name": None,
        }
        # Publish the exact next candidate before the cadence check so a soft
        # stop between candidates still names the uncompleted transaction.
        monitor.check("wordexpr_candidate_scan")
        progress.evaluator = None
        progress.bind(phase="candidate_start", candidate=correction_index,
                      target_ordinal=0, target_name="none", component=0,
                      blocker="not_tested", pool_suffix=0, evaluator=None)
        progress.emit(boundary=True)
        snapshot = candidate_transaction_snapshot(
            pool, dag, basis, sections, base_source_key)
        dag_before = dag.checkpoint()
        pool_before = len(pool.values)
        transaction["membership_starts"] += 1
        compiled = build_wordexpr_candidate(
            correction_index, correction, finite_inverse_words)
        expr: WordExprDAG = compiled["dag"]
        evaluator = WordExprEvaluator(
            expr, e4, evaluator_binding(compiled), progress.hook,
            memo_static_binding=memo_static_binding)
        progress.bind(evaluator=evaluator)
        phase_mark = time.monotonic()
        evaluator.evaluate_values()
        memo_performance["phase_elapsed_seconds"]["value_evaluation"] += \
            time.monotonic()-phase_mark
        require(tuple(evaluator.values[root-1]
                      for root in compiled["source_roots"]) ==
                source_tuples[correction_index-1] == raw_base_source_key,
                "WordExpr direct source tuple replay drift")
        diagnostics = diagnostic_rows(compiled, evaluator)
        diag_pass = sum(row["quotient_identity"] for row in diagnostics)
        diag_digest = digest_obj(diagnostics)
        failed_name, failed_ordinal = direct_gate_failure(compiled, evaluator)
        bridge_data: dict[str, Any] | None = None
        if failed_name is None and correction_index == 1:
            run_pin_stage(evaluator, compiled["source_roots"],
                          "candidate1_bridge")
            phase_mark = time.monotonic()
            bridge_data = candidate1_flat_bridge(
                compiled, evaluator, pool_before)
            memo_performance["phase_elapsed_seconds"][
                "candidate1_bridge_and_membership"] += \
                    time.monotonic()-phase_mark
            receipt["candidate1_flat_bridge"] = bridge_data["public"]
        expr_digest = expression_digest(expr)
        expr_accounting = expr.accounting(
            [root for _, _, root in compiled["acceptance"]+compiled["diagnostics"]])
        transaction["max_live_gradient_entries"] = max(
            transaction["max_live_gradient_entries"],
            evaluator.target_gradient_entry_peak)
        if failed_name is not None:
            memo_performance["direct_failures_before_pin"] += 1
            if correction_index > 1:
                memo_performance["ordinary_exits_before_target17"] += 1
            absorb_memo(evaluator, discarded=True)
            evaluator.discard_candidate_memo()
            removed = rollback_candidate_transaction(
                snapshot, pool, dag, basis, sections)
            transaction["membership_rollbacks"] += 1
            require(dag.checkpoint() == dag_before and removed == 0,
                    "direct-failed candidate persistent DAG/pool")
            records.append({
                "candidate_index": correction_index,
                "outcome": "QUOTIENT_FAILURE", "outcome_code": 1,
                "failed_name": failed_name,
                "failed_target_ordinal": failed_ordinal,
                "blocker_component": 0,
                "blocker_value_hex": zero_blob.hex(),
                "blocker_value_sha256": hashlib.sha256(zero_blob).hexdigest(),
                "gradient_entry_count": 0,
                "diagnostic_pass_count": diag_pass,
                "diagnostic_values_sha256": diag_digest,
                "wordexpr_sha256": expr_digest,
                "wordexpr_nodes": expr_accounting["node_count"],
                "wordexpr_edges": expr_accounting["edge_count"],
                "wordexpr_max_expanded_letters":
                    expr_accounting["max_expanded_letter_count"],
                "pool_suffix_removed": removed,
            })
        else:
            if correction_index == 1:
                require(bridge_data is not None,
                        "candidate1 fused bridge result")
                bindings = list(bridge_data["bindings"])
                missing_key = bridge_data["missing_key"]
                missing_name = bridge_data["missing_name"]
                missing_kind = bridge_data["missing_kind"]
                missing_ordinal = bridge_data["missing_ordinal"]
                total_entries = bridge_data["total_entries"]
                require(missing_key is not None and missing_ordinal == 6 and
                        len(bindings) == 6,
                        "candidate1 fused target-six blocker")
            else:
                bindings = []
                missing_key = None
                missing_name = ""
                missing_kind = ""
                missing_ordinal = 0
                total_entries = 0
                phase_mark = time.monotonic()
                for ordinal, (name, kind, root) in enumerate(
                        compiled["acceptance"], 1):
                    if ordinal == 17:
                        run_pin_stage(evaluator, compiled["source_roots"],
                                      "ordinary_target17")
                    receipt["_wordexpr_scan_current"].update(
                        {"target_ordinal": ordinal, "target_name": name})
                    progress.bind(
                        phase="ordinary_membership",
                        candidate=correction_index,
                        target_ordinal=ordinal, target_name=name,
                        component=0, blocker="reducing",
                        pool_suffix=len(pool.values)-pool_before,
                        evaluator=evaluator)
                    progress.emit(boundary=True, node=root)
                    monitor.check("wordexpr_membership_target")
                    gradients = evaluator.evaluate_gradients([root])
                    gradient = gradients[root]
                    value = evaluator.values[root-1]
                    require(value == e4.identity,
                            f"WordExpr acceptance quotient identity: {name}")
                    binding = raw_gradient_binding(name, kind, gradient, value)
                    bindings.append(binding)
                    total_entries += len(gradient)
                    packed = intern_raw_vector(gradient, pool)
                    suffix = len(pool.values)-pool_before
                    transaction["max_pool_suffix"] = max(
                        transaction["max_pool_suffix"], suffix)
                    if suffix > CAPS["candidate_element_pool_suffix"]:
                        raise ResourceStop(
                            "candidate_element_pool_suffix",
                            cap_key="candidate_element_pool_suffix",
                            cap_limit=CAPS["candidate_element_pool_suffix"],
                            observed_count=suffix, trigger_relation="gt")
                    missing_key = membership_reduce_fixed_basis(packed, basis)
                    if missing_key is not None:
                        missing_name, missing_kind, missing_ordinal = \
                            name, kind, ordinal
                        component, _ = unpack_vector_key(missing_key)
                        progress.bind(component=component,
                                      blocker="missing_pivot",
                                      pool_suffix=suffix)
                        progress.emit(boundary=True, node=root)
                        break
                memo_performance["phase_elapsed_seconds"][
                    "ordinary_membership"] += time.monotonic()-phase_mark
            transaction["max_live_gradient_entries"] = max(
                transaction["max_live_gradient_entries"],
                evaluator.target_gradient_entry_peak)
            if missing_key is not None:
                component, element_id = unpack_vector_key(missing_key)
                blocker_blob = pool.blob(element_id)
                blocker_sha = hashlib.sha256(blocker_blob).hexdigest()
                absorb_memo(evaluator, discarded=True)
                evaluator.discard_candidate_memo()
                removed = rollback_candidate_transaction(
                    snapshot, pool, dag, basis, sections)
                transaction["membership_rollbacks"] += 1
                require(dag.checkpoint() == dag_before and
                        len(pool.values) == pool_before,
                        "failed membership candidate rollback")
                if correction_index == 1:
                    require(missing_ordinal == 6 and
                            missing_name == "hexagon_1_coface_0" and
                            component == 4 and blocker_sha ==
                            V7_PREFIX_BINDINGS["final_blocker_sha256"],
                             "candidate1 saturated blocker drift")
                elif missing_ordinal < 17:
                    memo_performance["ordinary_exits_before_target17"] += 1
                records.append({
                    "candidate_index": correction_index,
                    "outcome": "MISSING_PIVOT", "outcome_code": 2,
                    "failed_name": missing_name,
                    "failed_kind": missing_kind,
                    "failed_target_ordinal": missing_ordinal,
                    "blocker_component": component,
                    "blocker_value_hex": blocker_blob.hex(),
                    "blocker_value_sha256": blocker_sha,
                    "gradient_entry_count": total_entries,
                    "failed_gradient_entry_count": bindings[-1]["entry_count"],
                    "gradient_bindings_sha256": digest_obj(bindings),
                    "diagnostic_pass_count": diag_pass,
                    "diagnostic_values_sha256": diag_digest,
                    "wordexpr_sha256": expr_digest,
                    "wordexpr_nodes": expr_accounting["node_count"],
                    "wordexpr_edges": expr_accounting["edge_count"],
                    "wordexpr_max_expanded_letters":
                        expr_accounting["max_expanded_letter_count"],
                    "wordexpr_live_gradient_peak":
                        evaluator.target_gradient_entry_peak,
                    "pool_suffix_removed": removed,
                })
            else:
                # Phase two: discard membership-only values, rebuild from the
                # dictionary index, compare every binding, then pay provenance.
                membership_serialized = expr.serialize_reachable(
                    [(name, root) for name, _, root in
                     compiled["acceptance"]+compiled["diagnostics"]] +
                    [(f"source_{i+1}", root)
                     for i, root in enumerate(compiled["source_roots"])] +
                    list(compiled["correction_coface_roots"]))
                absorb_memo(evaluator, discarded=True)
                evaluator.discard_candidate_memo()
                removed = rollback_candidate_transaction(
                    snapshot, pool, dag, basis, sections)
                transaction["membership_rollbacks"] += 1
                require(dag.checkpoint() == dag_before and
                        len(pool.values) == pool_before,
                        "all-membership phase rollback")

                proof_snapshot = candidate_transaction_snapshot(
                    pool, dag, basis, sections, base_source_key)
                transaction["proof_starts"] += 1
                replay = build_wordexpr_candidate(
                    correction_index, correction, finite_inverse_words)
                replay_expr: WordExprDAG = replay["dag"]
                replay_evaluator = WordExprEvaluator(
                    replay_expr, e4, evaluator_binding(replay), progress.hook,
                    memo_static_binding=memo_static_binding)
                progress.bind(phase="proof_regeneration",
                              candidate=correction_index,
                              target_ordinal=0, target_name="none",
                              component=0, blocker="provenance_solve",
                              evaluator=replay_evaluator)
                phase_mark = time.monotonic()
                replay_evaluator.evaluate_values()
                run_pin_stage(replay_evaluator, replay["source_roots"],
                              "proof_regeneration")
                require(expression_digest(replay_expr) == expr_digest and
                        replay_expr.serialize_reachable(
                            [(name, root) for name, _, root in
                             replay["acceptance"]+replay["diagnostics"]] +
                            [(f"source_{i+1}", root)
                             for i, root in enumerate(replay["source_roots"])] +
                            list(replay["correction_coface_roots"])) ==
                        membership_serialized and
                        tuple(replay_evaluator.values[root-1]
                              for root in replay["source_roots"]) ==
                        raw_base_source_key,
                        "selected WordExpr regeneration drift")
                proof_roots: dict[str, int] = {}
                replay_bindings: list[dict[str, Any]] = []
                for ordinal, (name, kind, root) in enumerate(
                        replay["acceptance"], 1):
                    receipt["_wordexpr_scan_current"].update(
                        {"target_ordinal": ordinal, "target_name": name})
                    progress.bind(target_ordinal=ordinal, target_name=name)
                    progress.emit(boundary=True, node=root)
                    gradient = replay_evaluator.evaluate_gradients([root])[root]
                    value = replay_evaluator.values[root-1]
                    binding = raw_gradient_binding(name, kind, gradient, value)
                    require(binding == bindings[ordinal-1],
                            "selected WordExpr gradient regeneration drift")
                    packed = intern_raw_vector(gradient, pool)
                    proof_root = basis.solve(packed)
                    require(proof_root is not None,
                            "selected provenance solve after membership pass")
                    proof_roots[name] = proof_root
                    replay_bindings.append(binding)
                require(replay_bindings == bindings and
                        [evaluator.values[root-1] for _, _, root in
                         compiled["diagnostics"]] ==
                        [replay_evaluator.values[root-1] for _, _, root in
                         replay["diagnostics"]],
                        "selected diagnostic/value replay")
                memo_performance["phase_elapsed_seconds"][
                    "proof_regeneration"] += time.monotonic()-phase_mark
                absorb_memo(replay_evaluator, proof=True)
                if (len(pool.values)-proof_snapshot["pool"] >
                        CAPS["candidate_element_pool_suffix"]):
                    raise ResourceStop(
                        "candidate_element_pool_suffix",
                        cap_key="candidate_element_pool_suffix",
                        cap_limit=CAPS["candidate_element_pool_suffix"],
                        observed_count=(len(pool.values)-proof_snapshot["pool"]),
                        trigger_relation="gt")
                pool.commit(proof_snapshot["pool"])
                transaction["proof_commits"] += 1
                records.append({
                    "candidate_index": correction_index,
                    "outcome": "PASS", "outcome_code": 3,
                    "failed_name": "", "failed_target_ordinal": 0,
                    "blocker_component": 0,
                    "blocker_value_hex": zero_blob.hex(),
                    "blocker_value_sha256": hashlib.sha256(zero_blob).hexdigest(),
                    "gradient_entry_count": total_entries,
                    "gradient_bindings_sha256": digest_obj(bindings),
                    "diagnostic_pass_count": diag_pass,
                    "diagnostic_values_sha256": diag_digest,
                    "wordexpr_sha256": expr_digest,
                    "wordexpr_nodes": expr_accounting["node_count"],
                    "wordexpr_edges": expr_accounting["edge_count"],
                    "wordexpr_max_expanded_letters":
                        expr_accounting["max_expanded_letter_count"],
                    "wordexpr_live_gradient_peak":
                        evaluator.target_gradient_entry_peak,
                    "pool_suffix_removed": removed,
                })
                selected = {
                    "compiled": replay, "evaluator": replay_evaluator,
                    "proof_roots": proof_roots, "bindings": replay_bindings,
                    "diagnostics": diagnostic_rows(replay, replay_evaluator),
                    "wordexpr_payload": membership_serialized,
                    "operational_first_passing_registered_index": correction_index,
                    "mathematical_minimality_claimed": False,
                }
                replay_evaluator.discard_candidate_memo()

        if correction_index == 1:
            frozen_first = records[-1]
            require(
                frozen_first["outcome"] == "MISSING_PIVOT" and
                frozen_first["outcome_code"] == 2 and
                frozen_first["failed_target_ordinal"] == 6 and
                frozen_first["failed_name"] == "hexagon_1_coface_0" and
                frozen_first["blocker_component"] == 4 and
                frozen_first["blocker_value_sha256"] ==
                V7_PREFIX_BINDINGS["final_blocker_sha256"],
                "candidate1 mandatory saturated-prefix outcome drift")
        require(len(records) == correction_index,
                "WordExpr one record per evaluated candidate")
        receipt["_wordexpr_scan_current"] = None
        now = time.monotonic()
        progress.bind(
            phase="candidate_complete", candidate=correction_index,
            target_ordinal=records[-1]["failed_target_ordinal"],
            target_name=records[-1]["failed_name"] or "PASS",
            component=records[-1]["blocker_component"],
            blocker=records[-1]["outcome"],
            pool_suffix=transaction["max_pool_suffix"], evaluator=evaluator)
        progress.emit(boundary=True)
        if (correction_index % 256 == 0 or
                now-last_progress >= CAPS["progress_interval_seconds"] or selected):
            failures = sum(row["outcome_code"] != 3 for row in records)
            print("D972_B345_RELFRAT3_WORDEXPR_MEMO_V9_PROGRESS "
                  f"candidate={correction_index} target="
                  f"{records[-1]['failed_target_ordinal']} evaluated={len(records)} "
                  f"pass={int(selected is not None)} failures={failures} "
                  f"pool_suffix={transaction['max_pool_suffix']} "
                  f"gradient_peak={transaction['max_live_gradient_entries']} "
                  f"expr_nodes={records[-1]['wordexpr_nodes']} "
                  f"expr_edges={records[-1]['wordexpr_edges']} "
                  f"basis={len(basis.rows)} pool={len(pool.values)} "
                  f"DAG={dag.node_count} elapsed_s={now-run_start:.3f} "
                  f"RSS={current_rss_bytes()}", flush=True)
            last_progress = now
        if selected is not None:
            break

    complete = selected is None and len(records) == 4096
    progress.bind(phase="wordexpr_scan_complete",
                  candidate=len(records), target_ordinal=0,
                  target_name="none", blocker=("PASS" if selected else
                                                "registered_prefix_complete"))
    progress.emit(boundary=True)
    scan_payload = encode_scan_prefix(records, pool.width, complete)
    scan_payload.update({
        "registered_corrections": 4096,
        "registered_dictionary_complete": True,
        "full_H3_fibre_complete": False,
        "full_universe_claimed": False,
        "earliest_global_candidate_claimed": False,
        "negative_completeness_claimed": False,
        "candidate_order": "1..4096 exactly once after saturated v7 prefix",
        "candidate_order_sha256": digest_obj(
            [digest_obj(word) for word in dictionary["words"]]),
        "candidate_order_equals_frozen_v8": True,
        "acceptance_target_count": 33,
        "diagnostic_target_count": 17,
        "candidate1_bridge_membership_fused": True,
        "fixed_basis_immutable_during_scan": True,
        "membership_first_pass_allocates_provenance_nodes": False,
        "transaction": transaction,
        "runtime_seconds": time.monotonic()-scan_start,
    })
    receipt["wordexpr_scan"] = scan_payload
    memo_performance.update({
        "candidate_order_changed": False,
        "acceptance_or_diagnostic_promotion_changed": False,
        "memo_eviction_is_terminal_or_rejection": False,
        "cache_entry_budget_bytes":
            CAPS["gradient_memo_additional_budget_bytes"],
        "working_plus_cached_accounted_under_frozen_live_cap": True,
    })
    receipt["gradient_memo_performance"] = memo_performance
    receipt.pop("_memo_performance", None)
    receipt.pop("_wordexpr_scan_records", None)
    receipt.pop("_wordexpr_scan_current", None)
    receipt.pop("_wordexpr_transaction", None)
    search_accounting.update({
        "registered_correction_indices": list(range(1, len(records)+1)),
        "other_corrections_constructed_or_evaluated": max(0, len(records)-1),
        "correction_dictionary_constructed": True,
        "complete_source_tuple_DP_executed": True,
        "candidate_membership_tests": len(records),
        "candidate_target_streaming": True,
        "persistent_candidate_cache_size": 0,
        "persistent_candidate_gradient_entries": 0,
        "candidate_local_gradient_memo": True,
        "candidate_local_gradient_memo_cross_candidate_entries": 0,
        "source_anchor_pin_policy_stage_aware": True,
        "ordinary_lazy_pin_target_ordinal": 17,
        "cache_capacity_is_nonterminal": True,
        "candidate_1_flat_bridge_membership_fused": True,
        "candidate_1_missing_target_re_evaluated": False,
        "failed_candidate_provenance_nodes_allocated": 0,
        "selected_candidate_regenerated_and_exactly_compared":
            selected is not None,
    })
    receipt["search"] = search_accounting

    if selected is None:
        require(complete, "nonpositive WordExpr scan completeness")
        receipt["status"] = receipt["terminal_token"] = \
            "B345_RELFRAT3_WORDEXPR_SEARCH_INCOMPLETE"
        receipt["reason"] = "registered_dictionary_exhausted"
        receipt["claim_classification"] = "unknown_not_obstruction"
        receipt["claim_scope"] = \
            "registered_4096_wordexpr_positive_search_only"
        receipt["no_mathematical_obstruction_claimed"] = True
        receipt["full_universe_claimed"] = False
        receipt["negative_claimed"] = False
        receipt["direct_lane"] = {
            "literal_pair_found": False,
            "reason": "all registered corrections failed in the fixed saturated basis",
            "not_nonmembership": True, "not_obstruction": True,
        }
        refresh_prefix()
        receipt["resource_guards"] = monitor.receipt(False)
        receipt["performance"] = {
            "runtime_seconds": time.monotonic()-run_start,
            "phase_complete": "registered_dictionary_exhausted",
            "phase_timings_seconds": phase_timings,
        }
        return receipt

    # Retain the completed PASS-prefix ledger until positive serialization is
    # fully committed.  A cap hit in that phase remains a typed partial
    # UNKNOWN_RESOURCE rather than an implicit positive.
    receipt["_wordexpr_scan_records"] = records
    receipt["_wordexpr_scan_current"] = {
        "candidate_index":
            selected["operational_first_passing_registered_index"],
        "target_ordinal": 0, "target_name": None,
        "phase": "positive_certificate_serialization",
    }
    receipt["_wordexpr_transaction"] = transaction
    compiled = selected["compiled"]
    evaluator = selected["evaluator"]
    proof_roots = selected["proof_roots"]
    registry = ElementRegistry({3: e3, 4: e4})
    receipt["quotient_element_registry"] = registry.rows
    receipt["fox_models"] = {
        "PB3": encode_fox_model(model3, e3, registry),
        "PB4": encode_fox_model(model4, e4, registry),
        "PB5": {"constructed": False,
                "reason": "direct B3/B4 registered WordExpr pair certified first"},
    }
    proof_payload, proof_renumber = serialize_proof_dag(
        dag, proof_roots, basis, registry)
    receipt["boundary_proof_dag"] = proof_payload
    wordexpr_payload = selected["wordexpr_payload"]
    receipt["selected_wordexpr_dag"] = wordexpr_payload
    expr_root_ids = {row["name"]: row["node_id"]
                     for row in wordexpr_payload["roots"]}
    selected_diagnostics = [
        {**row, "root": expr_root_ids[row["name"]]}
        for row in selected["diagnostics"]]
    correction_coface_gates = [{
        "name": name,
        "wordexpr_root_node_id": expr_root_ids[name],
        "quotient_value_hex":
            _element_blob(evaluator.values[root-1]).hex(),
        "quotient_identity": evaluator.values[root-1] == e4.identity,
    } for name, root in compiled["correction_coface_roots"]]
    require(len(correction_coface_gates) == 5 and
            all(row["quotient_identity"] for row in correction_coface_gates),
            "selected correction coface gates")
    certificates = []
    for (name, kind, root), binding in zip(
            compiled["acceptance"], selected["bindings"]):
        certificates.append({
            "name": name, "kind": kind,
            "wordexpr_root_node_id": expr_root_ids[name],
            "quotient_identity": True,
            "gradient_binding": binding,
            "proof_root_node_id": proof_renumber[proof_roots[name]],
            "proof_system": "shared_topological_F3_provenance_DAG",
        })
    receipt["boundary_certificates"] = certificates
    receipt["selected_pair"] = {
        "correction_index": selected["operational_first_passing_registered_index"],
        "correction_word": compiled["correction_word"],
        "correction_word_sha256": digest_obj(compiled["correction_word"]),
        "candidate_word": compiled["candidate_word"],
        "candidate_word_sha256": digest_obj(compiled["candidate_word"]),
        "candidate_exponent_sums": compiled["candidate_exponent_sums"],
        "fixed_inverse_words": [list(word) for word in finite_inverse_words],
        "fixed_inverse_words_sha256": inverse_words_sha256,
        "source_expression_roots": [expr_root_ids[f"source_{i}"]
                                    for i in range(1, 7)],
        "diagnostics": selected_diagnostics,
        "correction_coarse_J_H_coface_gates": correction_coface_gates,
        "correction_coarse_J_H_all_five": True,
        "correction_in_finer_J_Phi_required": False,
        "diagnostics_feed_acceptance": False,
        "acceptance_target_count": 33,
        "diagnostic_target_count": 17,
        "T_canaries_required_for_acceptance": False,
        "corrected_Def2_9_IF_FIRST_frozen_pre_run": True,
        "operational_first_passing_registered_index":
            selected["operational_first_passing_registered_index"],
        "mathematical_minimality_claimed": False,
        "charming_witness": compiled["charming_witness"],
        "friendly_gate": {
            "m": 0, "lambda": 1,
            "frozen_q3_selected_solution_replayed": True,
            "all_five_coarse_correction_cofaces_identity": True,
        },
        "marking_gate": {"m": 0, "lambda": 1,
                         "additional_residuals": []},
        "outside_roof_gate": receipt["registered_universe"]["fixed_outside_roof"],
    }
    receipt["status"] = receipt["terminal_token"] = \
        "B345_RELFRAT3_WORDEXPR_PASS"
    receipt["reason"] = \
        "one registered typed WordExpr candidate has all direct gates and 33 exact boundary proofs"
    receipt["claim_classification"] = "positive_certificate"
    receipt["claim_scope"] = \
        "registered_4096_wordexpr_positive_search_only"
    receipt["no_mathematical_obstruction_claimed"] = True
    receipt["full_universe_claimed"] = False
    receipt["negative_claimed"] = False
    receipt["direct_lane"] = {
        "literal_pair_found": True, "PB5_branch_constructed": False,
        "stop_reason": "FIRST_REGISTERED_WORDEXPR_LITERAL_PAIR",
    }
    refresh_prefix()
    receipt["resource_guards"] = monitor.receipt(False)
    receipt["performance"] = {
        "runtime_seconds": time.monotonic()-run_start,
        "phase_complete": "registered_wordexpr_pair",
        "quotient_registry_size": len(registry.rows),
        "phase_timings_seconds": phase_timings,
    }
    receipt.pop("_wordexpr_scan_records", None)
    receipt.pop("_wordexpr_scan_current", None)
    receipt.pop("_wordexpr_transaction", None)
    return receipt


def run(q3_path: Path, output_path: Path) -> dict[str, Any]:
    run_start = time.monotonic()
    phase_start = run_start
    monitor = ResourceMonitor(run_start, CAPS["producer_soft_timeout_seconds"])
    repo = Path(__file__).resolve().parents[1]
    basis: SparseBoundaryBasis | None = None
    dag: ProvenanceDAG | None = None
    pool: ElementPool | None = None
    sections: SparseSectionOracle | None = None
    e3: MatchedQuotient | None = None
    e4: MatchedQuotient | None = None
    proof_dag: dict[str, Any] | None = None
    registry: ElementRegistry | None = None
    blockers: dict[int, dict[str, Any]] = {}
    blocker_history: list[dict[str, Any]] = []
    checkpoint_trace: list[dict[str, Any]] = []
    direct_comparisons: list[dict[str, Any]] = []
    directed_translation_rows: list[dict[str, Any]] = []
    directed_column_rows: list[dict[str, Any]] = []
    directed_round_rows: list[dict[str, Any]] = []
    directed_expression_roots: list[int] = []
    directed_stop_reason: str | None = None
    transaction = {
        "starts": 0, "commits": 0, "rollbacks": 0,
        "blocker_skips": 0, "blocker_retries": 0,
        "target_gradients_generated": 0, "early_target_failures": 0,
        "full_quotient_rejections": 0, "max_transient_sparse_entries": 0,
        "total_transient_sparse_entries": 0,
    }
    phase_timings: dict[str, float] = {}

    def record_phase(label: str) -> None:
        nonlocal phase_start
        now = time.monotonic()
        phase_timings[label] = now-phase_start
        print(f"D972_B345_RELFRAT3_WORDEXPR_MEMO_V9_PHASE {label} "
              f"elapsed_s={phase_timings[label]:.6f}", flush=True)
        phase_start = now
    state = {"translations": 0, "current_candidate": 0, "current_target": 0}
    search_prefix: dict[str, Any] = {
        "fixed_candidate": {
            "correction_index": 1, "correction_word": [],
            "direct_gates_completed": False,
            "direct_gate_replay_count": 0,
            "target_count": None, "target_order_sha256": None,
        },
        "current": {"checkpoint": None, "correction_index": None,
                    "target_ordinal": None, "target_name": None},
        "blocker": {"count": 0, "sha256": digest_obj([])},
        "transaction": {"starts": 0, "commits": 0, "rollbacks": 0},
        "structural_cap": {"hit": False, "reason": None,
                           "source": None},
        "accounting": {},
    }

    def public_blockers() -> list[dict[str, Any]]:
        return [blockers[index] for index in sorted(blockers)]

    def refresh_prefix() -> None:
        rows = public_blockers()
        search_prefix["blocker"] = {"count": len(rows),
                                      "sha256": digest_obj(rows)}
        search_prefix["transaction"] = {
            "starts": transaction["starts"],
            "commits": transaction["commits"],
            "rollbacks": transaction["rollbacks"],
        }
        pc = _combined_pc_cache(e3, e4)
        search_prefix["accounting"] = {
            "translations": state["translations"],
            "basis_pivots": 0 if basis is None else len(basis.rows),
            "basis_live_entries": 0 if basis is None else basis.live_vector_entries,
            "pool_size": 0 if pool is None else len(pool.values),
            "DAG_nodes": 0 if dag is None else dag.node_count,
            "DAG_edges": 0 if dag is None else dag.edge_count,
            "section_nodes": 0 if sections is None else len(sections.parent),
            "section_expression_nodes": 0 if sections is None else
                len(sections.expressions.kind),
            "section_expression_edges": 0 if sections is None else
                sections.expressions.edge_count,
            "PC_cache_hits": pc["hits"], "PC_cache_misses": pc["misses"],
            "PC_cache_evictions": pc["evictions"],
        }

    def append_trace(row: dict[str, Any]) -> None:
        if len(checkpoint_trace) >= CAPS["transaction_trace_records"]:
            raise ResourceStop(
                "transaction_trace_records",
                cap_key="transaction_trace_records",
                cap_limit=CAPS["transaction_trace_records"],
                observed_count=len(checkpoint_trace), trigger_relation="ge")
        checkpoint_trace.append(row)

    def live_accounting() -> dict[str, int]:
        pc = _combined_pc_cache(e3, e4)
        blocker_pivot_present = 0
        if pool is not None and basis is not None and blockers:
            row = next(iter(blockers.values()))
            identifier = pool.ids.get(bytes.fromhex(row["element_hex"]))
            if identifier is not None and pack_vector_key(
                    int(row["component"]), identifier) in basis.rows:
                blocker_pivot_present = 1
        return {
            "translations": state["translations"],
            "columns": 0 if basis is None else basis.columns_seen,
            "pivots": 0 if basis is None else len(basis.rows),
            "live_sparse_entries": 0 if basis is None else basis.live_vector_entries,
            "element_pool": 0 if pool is None else len(pool.values),
            "dag_nodes": 0 if dag is None else dag.node_count,
            "dag_edges": 0 if dag is None else dag.edge_count,
            "candidate_cache": 0,
            "pc_cache_hits": pc["hits"], "pc_cache_misses": pc["misses"],
            "pc_cache_evictions": pc["evictions"],
            "transactions": transaction["starts"],
            "rollbacks": transaction["rollbacks"],
            "blockers": len(blockers),
            "blocker_present": int(bool(blockers)),
            "blocker_pivot_present": blocker_pivot_present,
            "retries": transaction["blocker_retries"],
            "directed_translations": len(directed_translation_rows),
            "directed_columns": len(directed_column_rows),
            "directed_rounds": len(directed_round_rows),
            "current_candidate": state["current_candidate"],
            "current_target": state["current_target"],
        }

    def cap_utilization() -> dict[str, dict[str, int | float]]:
        def row(value: int, cap: int) -> dict[str, int | float]:
            return {"value": value, "cap": cap, "ratio": value/cap}

        return {
            "live_sparse_entries": row(
                0 if basis is None else basis.live_vector_entries,
                CAPS["total_sparse_group_ring_keys"]),
            "element_pool_peak": row(
                0 if pool is None else pool.peak, CAPS["element_pool"]),
            "sparse_pivots": row(
                0 if basis is None else len(basis.rows),
                CAPS["sparse_pivot_rows"]),
            "DAG_nodes": row(
                0 if dag is None else dag.max_nodes,
                CAPS["provenance_dag_nodes"]),
            "DAG_edges": row(
                0 if dag is None else dag.max_edges,
                CAPS["provenance_dag_edges"]),
            "directed_section_expression_nodes": row(
                0 if sections is None else sections.expressions.peak_nodes,
                CAPS["directed_section_expr_nodes"]),
            "directed_section_expression_edges": row(
                0 if sections is None else sections.expressions.peak_edges,
                CAPS["directed_section_expr_edges"]),
            "RSS_peak_bytes": row(
                monitor.peak_rss, CAPS["producer_soft_rss_bytes"]),
        }

    monitor.bind_accounting(live_accounting)
    require(q3_path.resolve() == (repo/Q3_ARTIFACT_PATH).resolve() and
            output_path.resolve() == (repo/OUTPUT_PATH).resolve(),
            "production paths must be the fixed ci/out paths")
    pin_errors: list[dict[str, str]] = []
    for path, sha, label in (
            (repo/Q3_PRODUCER, Q3_PRODUCER_SHA, "q3 producer"),
            (repo/Q3_CHECKER, Q3_CHECKER_SHA, "q3 checker"),
            (repo/Q3_DRIVER, Q3_DRIVER_SHA, "q3 driver"),
            (repo/V8_PRODUCER, V8_PRODUCER_SHA, "v8 producer"),
            (repo/V8_CHECKER, V8_CHECKER_SHA, "v8 checker"),
            (repo/V8_DRIVER, V8_DRIVER_SHA, "v8 driver"),
            (repo/V7_PRODUCER, V7_PRODUCER_SHA, "v7 producer"),
            (repo/V7_CHECKER, V7_CHECKER_SHA, "v7 checker"),
            (repo/V7_DRIVER, V7_DRIVER_SHA, "v7 driver"),
            (repo/V6_PRODUCER, V6_PRODUCER_SHA, "v6 producer"),
            (repo/V6_CHECKER, V6_CHECKER_SHA, "v6 checker"),
            (repo/V6_DRIVER, V6_DRIVER_SHA, "v6 driver"),
            (repo/V5_PRODUCER, V5_PRODUCER_SHA, "v5 producer"),
            (repo/V5_CHECKER, V5_CHECKER_SHA, "v5 checker"),
            (repo/V5_DRIVER, V5_DRIVER_SHA, "v5 driver"),
            (repo/V4_PRODUCER, V4_PRODUCER_SHA, "v4 producer"),
            (repo/V4_CHECKER, V4_CHECKER_SHA, "v4 checker"),
            (repo/V4_DRIVER, V4_DRIVER_SHA, "v4 driver"),
            (repo/V3_PRODUCER, V3_PRODUCER_SHA, "v3 producer"),
            (repo/V3_CHECKER, V3_CHECKER_SHA, "v3 checker"),
            (repo/V3_DRIVER, V3_DRIVER_SHA, "v3 driver"),
            (repo/V2_PRODUCER, V2_PRODUCER_SHA, "v2 producer"),
            (repo/V2_CHECKER, V2_CHECKER_SHA, "v2 checker"),
            (repo/V2_DRIVER, V2_DRIVER_SHA, "v2 driver"),
            (repo/V1_PRODUCER, V1_PRODUCER_SHA, "v1 producer"),
            (repo/V1_CHECKER, V1_CHECKER_SHA, "v1 checker"),
            (repo/V1_DRIVER, V1_DRIVER_SHA, "v1 driver")):
        got = "MISSING" if not path.is_file() else digest_file(path)
        if got != sha:
            pin_errors.append({"label": label, "path": str(path),
                               "expected_sha256": sha, "got": got})
    q3_got = "MISSING" if not q3_path.is_file() else digest_file(q3_path)
    if q3_got != Q3_ARTIFACT_SHA:
        pin_errors.append({"label": "q3 artifact", "path": str(q3_path),
                           "expected_sha256": Q3_ARTIFACT_SHA, "got": q3_got})
    if pin_errors:
        source_hashes = {
            "producer_sha256": digest_file(Path(__file__)),
            "checker_sha256": digest_file(
                repo/"search/check_d972_b345_relfrat3_wordexpr_memo_v9.py"),
            "driver_sha256": digest_file(
                repo/"search/d972_b345_relfrat3_wordexpr_memo_gha_driver_v9.g"),
        }
        failed = make_base_receipt(
            q3_path, output_path, {}, source_hashes,
            "B345_RELFRAT3_WORDEXPR_UNKNOWN_INPUT",
            "authenticated_input_pin_mismatch")
        failed["input_errors"] = pin_errors
        failed["claim_classification"] = "unknown_not_obstruction"
        failed["claim_scope"] = \
            "registered_4096_wordexpr_positive_search_only"
        failed["no_mathematical_obstruction_claimed"] = True
        failed["full_universe_claimed"] = False
        failed["negative_claimed"] = False
        failed["resource_guards"] = monitor.receipt(False)
        failed["performance"] = {
            "runtime_seconds": time.monotonic()-run_start,
            "phase_complete": "external_pin_preflight",
        }
        return failed
    q3_data = json.loads(q3_path.read_text(encoding="utf-8"))
    source_hashes = {
        "producer_sha256": digest_file(Path(__file__)),
        "checker_sha256": digest_file(repo/"search/check_d972_b345_relfrat3_wordexpr_memo_v9.py"),
        "driver_sha256": digest_file(repo/"search/d972_b345_relfrat3_wordexpr_memo_gha_driver_v9.g"),
    }
    receipt = make_base_receipt(q3_path, output_path, q3_data, source_hashes,
                                "B345_RELFRAT3_WORDEXPR_UNKNOWN_RESOURCE",
                                "initializing registered WordExpr search")
    receipt["bounded_search_prefix"] = search_prefix
    receipt["resource_guards"] = monitor.receipt(False)
    try:
        monitor.check("formula_reconstruction", force=True)
        selected_q3 = q3_data["selected_solution"]
        require(selected_q3["roof_row_index"] == 37 and
                selected_q3["exponent"] == 2 and
                selected_q3["correction_index"] == 1 and
                selected_q3["marking_m"] == 0 and
                selected_q3["lambda"] == 1 and
                selected_q3["typed_source_word"] == FIXED_WORD,
                "fixed q3 outside roof/candidate binding")
        receipt["registered_universe"]["fixed_outside_roof"] = {
            "row_index": 37, "exponent": 2,
            "roof_key": selected_q3["roof_key"],
            "typed_source_word": list(FIXED_WORD),
            "arithmetic_outside_by_index_three":
                selected_q3["arithmetic_outside_by_index_three"],
            "source": "frozen q3 selected outside roof",
        }
        receipt["registered_universe"]["marking_m"] = 0
        receipt["registered_universe"]["lambda"] = 1
        require(digest_obj(q3_data["formulas"]) == FORMULA_SHA,
                "q3 full formula digest")
        formula = relevant_formula()
        q3_formula = q3_data["formulas"]
        require(formula["presentations"]["PB3"]["relations"] ==
                q3_formula["presentations"]["PB3"]["relations"] and
                formula["presentations"]["PB4"]["relations"] ==
                q3_formula["presentations"]["PB4"]["relations"] and
                formula["presentations"]["PB5"]["relations"] ==
                q3_formula["presentations"]["PB5"]["relations"] and
                formula["cofaces_3_4"] == q3_formula["cofaces_3_4"] and
                formula["a18_order"]["maps"] == q3_formula["a18_order"]["maps"],
                "relevant formula reconstruction")
        e3, e4, context = reconstruct_quotients(q3_data)
        receipt["formula_sha256"] = FORMULA_SHA
        receipt["relevant_formula"] = formula
        receipt["relevant_formula_sha256"] = digest_obj(formula)
        receipt["matched_quotients"] = {
            "E3": {"coarse_degree": e3.degree, "fine_pc_rank": e3.pc.n,
                   "definition": "Q0 x Pi3[3]; authenticated coarse source kernel"},
            "E4": {"coarse_degree": e4.degree, "fine_pc_rank": e4.pc.n,
                   "definition": "Q4 x Pi4[3] from the frozen no-common-C3 gate"},
            "J_H": {"definition": "kernel(PB3 -> E3), with each correction replayed through all five cofaces into H4"},
            "J_Phi": {
                "definition": "intersection_{j=0}^4 (coface_j)^-1 Phi3(H4)",
                "identified_with_Phi3_H3": False,
                "correction_membership_required": False,
                "quotient_J_H_over_J_Phi_is_lift_freedom": True,
            },
        }
        record_phase("matched_quotients")

        monitor.check("base_replay_dictionary_source_tuple_preflight")
        receipt["base_q3_replay"] = replay_base_q3(q3_data, e3, e4)
        dictionary = correction_dictionary(q3_data, e3)
        require(dictionary["count"] == CAPS["dictionary_word_records"] == 4096,
                "registered correction dictionary count")
        receipt["correction_dictionary"] = {
            key: value for key, value in dictionary.items() if key != "words"
        }
        receipt["correction_dictionary"]["word_sha256"] = [
            digest_obj(word) for word in dictionary["words"]]
        receipt["correction_dictionary"]["candidate_order_sha256"] = \
            digest_obj(receipt["correction_dictionary"]["word_sha256"])
        receipt["correction_dictionary"]["equals_frozen_v8_order"] = True
        normalized_inverse, raw_base_source_key, finite_inverse_words = \
            normalized_inverse_fibre(q3_data, e4)
        receipt["normalized_inverse_fibre"] = normalized_inverse
        source_preflight, source_tuples = source_tuple_preflight(
            dictionary, e4, raw_base_source_key, monitor)
        receipt["source_tuple_preflight"] = source_preflight
        receipt["prohibited_work"]["all_dictionary_DP_executed"] = True
        record_phase("base_replay_dictionary_source_tuple_preflight")
        if not source_preflight["all_equal_to_frozen_tuple"]:
            receipt["status"] = receipt["terminal_token"] = \
                "B345_RELFRAT3_WORDEXPR_SEARCH_INCOMPLETE"
            receipt["reason"] = "fixed_inverse_not_uniform"
            receipt["scan"] = {
                "evaluated": 0, "complete": False,
                "first_differing_index":
                    source_preflight["first_difference"]["candidate_index"],
                "evaluated_prefix_sha256":
                    source_preflight["tuple_ledger_sha256"],
                "source_tuple_preflight_only": True,
            }
            receipt["claim_classification"] = "unknown_not_obstruction"
            receipt["claim_scope"] = \
                "registered_4096_wordexpr_positive_search_only"
            receipt["no_mathematical_obstruction_claimed"] = True
            receipt["full_universe_claimed"] = False
            receipt["negative_claimed"] = False
            receipt["resource_guards"] = affine_monitor_receipt(monitor, False)
            receipt["performance"] = {
                "runtime_seconds": time.monotonic()-run_start,
                "phase_complete": "fixed_inverse_nonuniform_preflight",
                "phase_timings_seconds": phase_timings,
            }
            return receipt

        pool = ElementPool(e4)
        sections = SparseSectionOracle(pool)

        model3 = fox_model(3, e3)
        model4 = fox_model(4, e4)
        packed_model4 = packed_fox_model(4, pool)
        base_occurrences = freeze_base_support_occurrences(
            model4, pool, sections)
        base_occurrences_public = public_base_occurrences(base_occurrences)
        receipt["directed_base_support"] = {
            "occurrences": base_occurrences_public,
            "occurrence_count": len(base_occurrences_public),
            "ordered_sha256": digest_obj(base_occurrences_public),
            "order": "relator index, component, canonical E4 bytes",
            "all_prefix_sections_directly_replayed": True,
        }
        dag = ProvenanceDAG(monitor)
        basis = SparseBoundaryBasis(pool, packed_model4["columns"], dag,
                                    sections, monitor)
        base_source_key = tuple(pool.intern(value) for value in raw_base_source_key)
        inverse_cache: dict[tuple[int, ...], list[list[int]]] = {
            base_source_key: finite_inverse_words,
        }
        inverse_cache_stats = {
            "hits": 0, "misses": 0,
            "max_inverse_word_length": normalized_inverse["max_inverse_word_length"],
        }

        class DirectValuePool:
            @staticmethod
            def intern(value: EKey) -> EKey:
                return value

        direct_stats = {"hits": 0, "misses": 0,
                        "max_inverse_word_length":
                            normalized_inverse["max_inverse_word_length"]}
        direct = prepare_candidate(list(FIXED_WORD), [], e4)
        direct = complete_candidate(
            direct, e4, DirectValuePool(),
            {raw_base_source_key: finite_inverse_words}, direct_stats,
            normalized_inverse)  # type: ignore[arg-type]
        direct = corrected_def29_targets(direct, e4)
        require(direct["correction_word"] == [] and
                direct["selected_word"] == FIXED_WORD and
                not direct["quotient_bad"] and direct_stats["hits"] == 1 and
                direct_stats["misses"] == 0,
                "fixed candidate direct preflight")
        target_names = [name for name, _, _ in direct["targets"]]
        diagnostic_names = [name for name, _, _ in direct["diagnostic_targets"]]
        target_lengths = [len(word) for _, _, word in direct["targets"]]
        source_lengths = [len(word) for word in direct["_source_words"]]
        inverse_lengths = [len(word) for word in direct["inverse"]["inverse_words"]]
        require(len(target_names) == 33 and len(diagnostic_names) == 17 and
                target_names[5] == "hexagon_1_coface_0" and
                max(target_lengths + source_lengths + inverse_lengths +
                    [len(FIXED_WORD)]) <= CAPS["single_word_or_section_length"],
                "fixed candidate target order/word cap")
        receipt["fixed_candidate_preflight"] = {
            "correction_index": 1, "correction_word": [],
            "selected_word": list(FIXED_WORD),
            "selected_word_length": len(FIXED_WORD),
            "source_word_lengths": source_lengths,
            "inverse_word_lengths": inverse_lengths,
            "target_names": target_names,
            "diagnostic_target_names": diagnostic_names,
            "corrected_Def2_9": direct["corrected_Def2_9"],
            "diagnostics": direct["diagnostic_rows"],
            "target_word_lengths": target_lengths,
            "max_source_word_length": max(source_lengths),
            "max_inverse_word_length": max(inverse_lengths),
            "max_target_word_length": max(target_lengths),
            "all_direct_quotient_gates_pass": True,
            "direct_gate_replay_count_before_sparse_growth": 1,
            "marking_m": 0, "lambda": 1,
            "fixed_outside_roof": {"row_index": 37, "exponent": 2},
            "target_order_sha256": digest_obj(target_names),
            "word_representation": "flat freely reduced signed-generator lists",
            "single_word_or_section_length_cap":
                CAPS["single_word_or_section_length"],
        }
        search_prefix["fixed_candidate"].update({
            "direct_gates_completed": True,
            "direct_gate_replay_count": 1,
            "target_count": len(target_names),
            "target_order_sha256": digest_obj(target_names),
        })
        record_phase("fixed_candidate_literal_preflight")

        selected_candidate: dict[str, Any] | None = None
        selected_roots: dict[str, int] | None = None
        selected_bindings: list[dict[str, Any]] | None = None
        unusable_candidates: set[int] = set()
        full_quotient_rejected: list[dict[str, Any]] = []
        geometric_checkpoints: list[int] = []
        tests = 0
        direct_replay_count = 0
        translate_cap = CAPS["coefficient_translates_per_relator"]
        inserted_translation_blobs: set[bytes] = set()

        for translation_id, section_node in translation_bfs(
                pool, sections, translate_cap):
            state["translations"] += 1
            used = state["translations"]
            monitor.check("translation_BFS")
            for relator_index in range(1, len(packed_model4["columns"])+1):
                basis.add_column(relator_index, translation_id, section_node,
                                 translation_ordinal=used)
            inserted_translation_blobs.add(pool.blob(translation_id))
            if (used & (used-1)) != 0:
                continue
            geometric_checkpoints.append(used)
            monitor.check("geometric_candidate_checkpoint", force=True)
            for correction_index in [1]:
                monitor.check("geometric_candidate_checkpoint")
                if correction_index in unusable_candidates:
                    append_trace({"checkpoint": used,
                                  "candidate_index": correction_index,
                                  "event": "permanent_full_quotient_reject_skip"})
                    refresh_prefix()
                    continue
                prior_blocker = blockers.get(correction_index)
                if prior_blocker is not None:
                    blocker_blob = bytes.fromhex(prior_blocker["element_hex"])
                    blocker_id = pool.ids.get(blocker_blob)
                    blocker_key = None if blocker_id is None else pack_vector_key(
                        int(prior_blocker["component"]), blocker_id)
                    if blocker_key is None or blocker_key not in basis.rows:
                        transaction["blocker_skips"] += 1
                        prior_blocker["skip_checkpoints"].append(used)
                        append_trace({"checkpoint": used,
                                      "candidate_index": correction_index,
                                      "event": "missing_pivot_skip",
                                      "blocker_history_id": prior_blocker["history_id"],
                                      "pool_element_present": blocker_id is not None,
                                      "basis_pivot_present": False})
                        refresh_prefix()
                        continue
                    introductions = [row for row in basis.pivot_introductions
                                     if row["component"] == prior_blocker["component"] and
                                     row["element_hex"] == prior_blocker["element_hex"] and
                                     prior_blocker["failed_checkpoint"] <
                                     row["translation_ordinal"] <= used]
                    require(bool(introductions),
                            "blocker retry without exact pivot introduction")
                    transaction["blocker_retries"] += 1
                    prior_blocker["retry_checkpoints"].append(used)
                    prior_blocker["matching_introduction"] = introductions[0]
                    append_trace({"checkpoint": used,
                                  "candidate_index": correction_index,
                                  "event": "exact_pivot_retry",
                                  "blocker_history_id": prior_blocker["history_id"],
                                  "matching_introduction": introductions[0]})
                    basis.blocker_watches.discard(
                        (int(prior_blocker["component"]), blocker_blob))
                    del blockers[correction_index]

                correction: list[int] = []
                snapshot = candidate_transaction_snapshot(
                    pool, dag, basis, sections, base_source_key)
                transaction["starts"] += 1
                state["current_candidate"] = correction_index
                state["current_target"] = 0
                search_prefix["current"] = {
                    "checkpoint": used, "correction_index": correction_index,
                    "target_ordinal": None, "target_name": None,
                }
                roots: dict[str, int] = {}
                bindings: list[dict[str, Any]] = []
                candidate_entries = 0
                candidate_peak = 0
                candidate_targets_generated = 0
                transaction_finished = False
                try:
                    temporary = prepare_candidate(
                        reduce_word(FIXED_WORD + correction), correction, e4)
                    direct_replay_count += 1
                    direct_row = {
                        "checkpoint": used,
                        "candidate_index": correction_index,
                        "direct_failed_gates": temporary["quotient_bad"],
                        "equal_to_preflight":
                            temporary["quotient_bad"] == [],
                    }
                    require(direct_row["equal_to_preflight"],
                            "fixed direct preflight drift")
                    direct_comparisons.append(direct_row)
                    temporary = complete_candidate(
                        temporary, e4, pool, inverse_cache,
                        inverse_cache_stats, normalized_inverse)
                    temporary = corrected_def29_targets(temporary, e4)
                    require(not temporary["quotient_bad"] and
                            [(name, kind, word) for name, kind, word in
                             temporary["targets"]] == direct["targets"],
                            "fixed complete candidate/preflight drift")

                    tests += 1
                    missing: dict[str, Any] | None = None
                    for target_ordinal, (name, kind, word) in enumerate(
                            temporary["targets"], 1):
                        state["current_target"] = target_ordinal
                        search_prefix["current"].update({
                            "target_ordinal": target_ordinal,
                            "target_name": name,
                        })
                        monitor.check("candidate_target_stream")
                        gradient, value_id = fox_gradient_packed(word, pool)
                        require(value_id == pool.identity_id,
                                f"candidate target not in H4: {name}")
                        raw_gradient, raw_value, raw_sections = fox_gradient(word, e4)
                        require(raw_value == e4.identity and
                                intern_raw_vector(raw_gradient, pool) == gradient,
                                f"candidate raw/packed target drift: {name}")
                        transient_sections = {
                            (component, pool.pack(value)): raw_sections[value]
                            for component, value in raw_gradient
                        }
                        transaction["target_gradients_generated"] += 1
                        transaction["total_transient_sparse_entries"] += len(gradient)
                        transaction["max_transient_sparse_entries"] = max(
                            transaction["max_transient_sparse_entries"], len(gradient))
                        candidate_targets_generated += 1
                        candidate_entries += len(gradient)
                        candidate_peak = max(candidate_peak, len(gradient))
                        binding = packed_gradient_binding(
                            name, kind, gradient, value_id, pool)
                        root, missing_key = basis.solve_with_blocker(gradient)
                        if root is None:
                            require(missing_key is not None,
                                    "missing target without exact pivot blocker")
                            component, element_id = unpack_vector_key(missing_key)
                            blocker_blob = pool.blob(element_id)
                            blocker_root, blocker_recovery = sections.recover_blocker(
                                component, blocker_blob, transient_sections,
                                base_occurrences)
                            require(sections.expressions.value_blob(blocker_root) ==
                                    blocker_blob,
                                    "exported blocker section binding")
                            missing = {
                                "candidate_index": correction_index,
                                "target_ordinal": target_ordinal,
                                "target_name": name,
                                "component": component,
                                "element_hex": blocker_blob.hex(),
                                "failed_checkpoint": used,
                                "skip_checkpoints": [],
                                "retry_checkpoints": [],
                                "history_id": len(blocker_history)+1,
                                "section_expression_root": blocker_root,
                                "section_recovery": blocker_recovery,
                            }
                            directed_expression_roots.append(blocker_root)
                            if not blocker_history:
                                require(target_ordinal == 6 and
                                        name == "hexagon_1_coface_0" and
                                        component == 4,
                                        "fixed checkpoint-1 blocker drift")
                            break
                        roots[name] = root
                        bindings.append(binding)
                        del gradient

                    if used == 1:
                        require(missing is not None,
                                "fixed checkpoint-1 blocker unexpectedly absent")
                    if missing is not None:
                        if correction_index not in blockers and \
                                len(blockers) >= CAPS["blocker_table"]:
                            raise ResourceStop(
                                "blocker_table", cap_key="blocker_table",
                                cap_limit=CAPS["blocker_table"],
                                observed_count=len(blockers),
                                trigger_relation="ge")
                        basis.watch_blocker(missing["component"],
                                            bytes.fromhex(missing["element_hex"]))
                        blockers[correction_index] = missing
                        blocker_history.append(missing)
                        transaction["early_target_failures"] += 1
                        removed = rollback_candidate_transaction(
                            snapshot, pool, dag, basis, sections)
                        transaction["rollbacks"] += 1
                        transaction_finished = True
                        append_trace({"checkpoint": used,
                                      "candidate_index": correction_index,
                                      "event": "missing_pivot",
                                      "target_ordinal": missing["target_ordinal"],
                                      "target_name": missing["target_name"],
                                      "component": missing["component"],
                                      "element_hex": missing["element_hex"],
                                      "blocker_history_id": missing["history_id"],
                                      "pool_suffix_removed": removed,
                                      "target_gradients_generated":
                                          candidate_targets_generated,
                                      "transient_sparse_entries": candidate_entries,
                                      "peak_transient_sparse_entries": candidate_peak})
                        state["current_candidate"] = 0
                        state["current_target"] = 0
                        search_prefix["current"] = {
                            "checkpoint": used, "correction_index": None,
                            "target_ordinal": None, "target_name": None,
                        }
                        refresh_prefix()
                        continue

                    require(len(roots) == len(temporary["targets"]) == len(bindings),
                            "streamed target completion")
                    pool.commit(snapshot["pool"])
                    transaction["commits"] += 1
                    transaction_finished = True
                    temporary["correction_index"] = correction_index
                    selected_candidate = temporary
                    selected_roots = roots
                    selected_bindings = bindings
                    append_trace({"checkpoint": used,
                                  "candidate_index": correction_index,
                                  "event": "selected_commit",
                                  "target_count": len(roots),
                                  "pool_suffix_committed": len(pool.values)-snapshot["pool"],
                                  "target_gradients_generated":
                                      candidate_targets_generated,
                                  "transient_sparse_entries": candidate_entries,
                                  "peak_transient_sparse_entries": candidate_peak})
                    state["current_candidate"] = 0
                    state["current_target"] = 0
                    search_prefix["current"] = {
                        "checkpoint": used, "correction_index": None,
                        "target_ordinal": None, "target_name": None,
                    }
                    refresh_prefix()
                    break
                except ResourceStop:
                    if not transaction_finished:
                        rollback_candidate_transaction(
                            snapshot, pool, dag, basis, sections)
                        transaction["rollbacks"] += 1
                    raise
                except Exception:
                    if not transaction_finished:
                        rollback_candidate_transaction(
                            snapshot, pool, dag, basis, sections)
                        transaction["rollbacks"] += 1
                    raise
            if selected_candidate is not None:
                break

        # v7 begins only after the exact frozen v6 32,768-translation prefix.
        # Candidate work is transactional; each directed block is persistent.
        require(selected_candidate is None,
                "frozen v6 candidate unexpectedly passed before pivot surgery")
        if selected_candidate is None:
            require(state["translations"] == translate_cap == 32_768 and
                    len(inserted_translation_blobs) == translate_cap,
                    "full frozen v6 translation prefix")
            blockers.clear()
            for round_no in range(1, CAPS["directed_surgery_rounds"]+1):
                monitor.check("directed_surgery_round", force=True)
                snapshot = candidate_transaction_snapshot(
                    pool, dag, basis, sections, base_source_key)
                transaction["starts"] += 1
                state["current_candidate"] = 1
                state["current_target"] = 0
                search_prefix["current"] = {
                    "checkpoint": translate_cap,
                    "correction_index": 1,
                    "target_ordinal": None, "target_name": None,
                    "directed_round": round_no,
                }
                roots = {}
                bindings = []
                candidate_entries = 0
                candidate_peak = 0
                candidate_targets_generated = 0
                transaction_finished = False
                missing = None
                try:
                    temporary = corrected_def29_targets(
                        complete_candidate(
                            prepare_candidate(list(FIXED_WORD), [], e4),
                            e4, pool, inverse_cache, inverse_cache_stats,
                            normalized_inverse), e4)
                    require(not temporary["quotient_bad"] and
                            [(name, kind, word) for name, kind, word in
                             temporary["targets"]] == direct["targets"],
                            "directed retry fixed candidate drift")
                    tests += 1
                    for target_ordinal, (name, kind, word) in enumerate(
                            temporary["targets"], 1):
                        state["current_target"] = target_ordinal
                        search_prefix["current"].update({
                            "target_ordinal": target_ordinal,
                            "target_name": name,
                        })
                        monitor.check("directed_candidate_target_stream")
                        gradient, value_id = fox_gradient_packed(word, pool)
                        require(value_id == pool.identity_id,
                                f"directed target not in H4: {name}")
                        raw_gradient, raw_value, raw_sections = fox_gradient(word, e4)
                        require(raw_value == e4.identity and
                                intern_raw_vector(raw_gradient, pool) == gradient,
                                f"directed raw/packed target drift: {name}")
                        transient_sections = {
                            (component, pool.pack(value)): raw_sections[value]
                            for component, value in raw_gradient
                        }
                        transaction["target_gradients_generated"] += 1
                        transaction["total_transient_sparse_entries"] += len(gradient)
                        transaction["max_transient_sparse_entries"] = max(
                            transaction["max_transient_sparse_entries"], len(gradient))
                        candidate_targets_generated += 1
                        candidate_entries += len(gradient)
                        candidate_peak = max(candidate_peak, len(gradient))
                        binding = packed_gradient_binding(
                            name, kind, gradient, value_id, pool)
                        root, missing_key = basis.solve_with_blocker(gradient)
                        if root is None:
                            require(missing_key is not None,
                                    "directed missing target without pivot")
                            component, element_id = unpack_vector_key(missing_key)
                            blocker_blob = pool.blob(element_id)
                            blocker_root, recovery = sections.recover_blocker(
                                component, blocker_blob, transient_sections,
                                base_occurrences)
                            require(sections.expressions.value_blob(blocker_root) ==
                                    blocker_blob, "directed blocker section binding")
                            missing = {
                                "candidate_index": 1,
                                "target_ordinal": target_ordinal,
                                "target_name": name, "target_kind": kind,
                                "component": component,
                                "element_hex": blocker_blob.hex(),
                                "canonical_value_sha256":
                                    hashlib.sha256(blocker_blob).hexdigest(),
                                "directed_round": round_no,
                                "history_id": len(blocker_history)+1,
                                "section_expression_root": blocker_root,
                                "section_recovery": recovery,
                            }
                            directed_expression_roots.append(blocker_root)
                            break
                        roots[name] = root
                        bindings.append(binding)
                        del gradient
                    if missing is None:
                        require(len(roots) == len(temporary["targets"]) == 33 and
                                len(bindings) == 33,
                                "directed streamed target completion")
                        pool.commit(snapshot["pool"])
                        transaction["commits"] += 1
                        transaction_finished = True
                        temporary["correction_index"] = 1
                        selected_candidate = temporary
                        selected_roots = roots
                        selected_bindings = bindings
                        directed_round_rows.append({
                            "round": round_no, "outcome": "PASS",
                            "acceptance_targets_solved": 33,
                            "diagnostics_required": False,
                            "pivots_after": len(basis.rows),
                            "live_sparse_entries_after": basis.live_vector_entries,
                            "pool_after": len(pool.values),
                            "DAG_nodes_after": dag.node_count,
                            "DAG_edges_after": dag.edge_count,
                            "section_expression_nodes_after":
                                len(sections.expressions.kind),
                            "RSS_bytes": current_rss_bytes(),
                            "elapsed_seconds": time.monotonic()-run_start,
                        })
                        append_trace({"event": "directed_selected_commit",
                                      "round": round_no,
                                      "candidate_index": 1,
                                      "target_count": 33})
                        break

                    if round_no == 1:
                        require(missing["target_ordinal"] == 6 and
                                missing["target_name"] == "hexagon_1_coface_0" and
                                missing["component"] == 4 and
                                blocker_history and
                                missing["element_hex"] ==
                                blocker_history[0]["element_hex"],
                                "fresh v6 blocker reconstruction drift")
                    transaction["early_target_failures"] += 1
                    removed = rollback_candidate_transaction(
                        snapshot, pool, dag, basis, sections)
                    transaction["rollbacks"] += 1
                    transaction_finished = True
                    blocker_history.append(missing)

                    component = int(missing["component"])
                    blocker_blob = bytes.fromhex(missing["element_hex"])
                    blocker = pool.unpack(blocker_blob)
                    matching = [row for row in base_occurrences
                                if row["component"] == component]
                    matching.sort(key=lambda row: (
                        row["relator_index"], row["component"],
                        bytes.fromhex(row["element_hex"])))
                    candidates: list[tuple[bytes, EKey, dict[str, Any]]] = []
                    seen_batch: set[bytes] = set()
                    duplicates = 0
                    for occurrence in matching:
                        h = occurrence["_value"]
                        translation = e4.mul(blocker, e4.inverse(h))
                        translation_blob = pool.pack(translation)
                        require(e4.mul(translation, h) == blocker,
                                "left directed translation orientation")
                        if translation_blob in seen_batch or \
                                translation_blob in inserted_translation_blobs:
                            duplicates += 1
                            continue
                        seen_batch.add(translation_blob)
                        candidates.append((translation_blob, translation, occurrence))
                    pivots_before = len(basis.rows)
                    entries_before = basis.live_vector_entries
                    columns_before = basis.columns_seen
                    dependent_before = basis.dependent_columns
                    new_rows = 0
                    for translation_blob, translation, occurrence in candidates:
                        if len(directed_translation_rows) >= \
                                CAPS["directed_unique_translations"]:
                            raise ResourceStop(
                                "directed_unique_translations",
                                cap_key="directed_unique_translations",
                                cap_limit=CAPS["directed_unique_translations"],
                                observed_count=len(directed_translation_rows),
                                trigger_relation="ge")
                        blocker_root = int(missing["section_expression_root"])
                        h_root = int(occurrence["section_expression_root"])
                        inverse_h_root = sections.expressions.inverse(
                            h_root, "base_D2_prefix_inverse")
                        translation_root = sections.expressions.product(
                            blocker_root, inverse_h_root,
                            "registered_directed_translation")
                        require(sections.expressions.value_blob(translation_root) ==
                                translation_blob,
                                "directed translation expression orientation")
                        section_node, created = sections.register_directed(
                            translation, translation_root)
                        require(created, "new directed translation registration")
                        translation_id = pool.ids[translation_blob]
                        directed_expression_roots.append(translation_root)
                        translation_ordinal = translate_cap + \
                            len(directed_translation_rows) + 1
                        translation_row = {
                            "ordinal": len(directed_translation_rows)+1,
                            "round": round_no,
                            "component": component,
                            "blocker_element_hex": blocker_blob.hex(),
                            "base_relator_index": occurrence["relator_index"],
                            "base_element_hex": occurrence["element_hex"],
                            "translation_element_hex": translation_blob.hex(),
                            "section_expression_root": translation_root,
                            "formula": "t=g*h^-1; left translation sends h to g",
                        }
                        directed_translation_rows.append(translation_row)
                        for relator_index in range(1, 12):
                            if len(directed_column_rows) >= CAPS["directed_columns"]:
                                raise ResourceStop(
                                    "directed_columns",
                                    cap_key="directed_columns",
                                    cap_limit=CAPS["directed_columns"],
                                    observed_count=len(directed_column_rows),
                                    trigger_relation="ge")
                            before_rows = len(basis.rows)
                            basis.add_column(
                                relator_index, translation_id, section_node,
                                translation_ordinal=translation_ordinal)
                            column_row = {
                                "ordinal": len(directed_column_rows)+1,
                                "round": round_no,
                                "translation_ordinal": translation_row["ordinal"],
                                "relator_index": relator_index,
                                "independent": len(basis.rows) > before_rows,
                            }
                            directed_column_rows.append(column_row)
                        inserted_translation_blobs.add(translation_blob)
                        new_rows += 1
                    round_row = {
                        "round": round_no, "outcome": "RETRY",
                        "failed_target_ordinal": missing["target_ordinal"],
                        "failed_target_name": missing["target_name"],
                        "failed_target_kind": missing["target_kind"],
                        "blocker_component": component,
                        "blocker_element_hex": blocker_blob.hex(),
                        "blocker_value_sha256": missing["canonical_value_sha256"],
                        "blocker_section_expression_root":
                            missing["section_expression_root"],
                        "blocker_recovery": missing["section_recovery"],
                        "matching_base_occurrences": len(matching),
                        "new_directed_translations": new_rows,
                        "duplicate_translations": duplicates,
                        "columns_attempted": basis.columns_seen-columns_before,
                        "columns_independent": len(basis.rows)-pivots_before,
                        "columns_dependent":
                            basis.dependent_columns-dependent_before,
                        "pivots_before": pivots_before,
                        "pivots_after": len(basis.rows),
                        "live_sparse_entries_before": entries_before,
                        "live_sparse_entries_after": basis.live_vector_entries,
                        "pool_after": len(pool.values),
                        "DAG_nodes_after": dag.node_count,
                        "DAG_edges_after": dag.edge_count,
                        "section_expression_nodes_after":
                            len(sections.expressions.kind),
                        "section_expression_edges_after":
                            sections.expressions.edge_count,
                        "candidate_pool_suffix_removed": removed,
                        "candidate_rollback_count": transaction["rollbacks"],
                        "RSS_bytes": current_rss_bytes(),
                        "elapsed_seconds": time.monotonic()-run_start,
                    }
                    directed_round_rows.append(round_row)
                    append_trace({"event": "directed_surgery_batch",
                                  **round_row})
                    print("D972_B345_RELFRAT3_PIVOT_SURGERY_V7_ROUND " +
                          json.dumps(round_row, sort_keys=True,
                                     separators=(",", ":")), flush=True)
                    state["current_candidate"] = 0
                    state["current_target"] = 0
                    search_prefix["current"] = {
                        "checkpoint": translate_cap,
                        "correction_index": None,
                        "target_ordinal": None, "target_name": None,
                        "directed_round": round_no,
                    }
                    refresh_prefix()
                    if not candidates:
                        directed_stop_reason = "no_new_exact_directed_translation"
                        break
                except ResourceStop:
                    if not transaction_finished:
                        rollback_candidate_transaction(
                            snapshot, pool, dag, basis, sections)
                        transaction["rollbacks"] += 1
                    raise
                except Exception:
                    if not transaction_finished:
                        rollback_candidate_transaction(
                            snapshot, pool, dag, basis, sections)
                        transaction["rollbacks"] += 1
                    raise
            else:
                directed_stop_reason = "directed_surgery_round_cap_exhausted"

        audit_roots = sorted(set(directed_expression_roots))
        if audit_roots:
            directed_expression_payload, directed_expression_renumber = \
                sections.expressions.serialize_reachable(audit_roots, monitor)
        else:
            directed_expression_payload = {
                "format": "typed-section-expression-arrays/v1",
                "node_order": "zero_based_topological",
                "ordinary_word_composition": True,
                "canonical_value_width": pool.width,
                "node_count": 0, "edge_count": 0, "roots": [],
                "arrays": {},
                "manifest_sha256": digest_obj({"arrays": {}, "roots": []}),
            }
            directed_expression_renumber = {}
        public_directed_translations = remap_expression_root_fields(
            directed_translation_rows, directed_expression_renumber)
        public_directed_rounds = remap_expression_root_fields(
            directed_round_rows, directed_expression_renumber)
        public_blocker_history_rows = remap_expression_root_fields(
            blocker_history, directed_expression_renumber)
        public_checkpoint_trace = remap_expression_root_fields(
            checkpoint_trace, directed_expression_renumber)
        stable_directed_rounds = [
            {key: value for key, value in row.items()
             if key not in {"elapsed_seconds", "RSS_bytes"}}
            for row in public_directed_rounds]
        stable_rounds_sha = digest_obj(stable_directed_rounds)
        translations_sha = digest_obj(public_directed_translations)
        columns_sha = digest_obj(directed_column_rows)
        blocker_history_sha = digest_obj(public_blocker_history_rows)
        require(stable_rounds_sha ==
                V7_PREFIX_BINDINGS["stable_rounds_projection_sha256"] and
                translations_sha == V7_PREFIX_BINDINGS["translations_sha256"] and
                columns_sha == V7_PREFIX_BINDINGS["columns_sha256"] and
                blocker_history_sha ==
                V7_PREFIX_BINDINGS["blocker_history_sha256"] and
                len(public_directed_rounds) == 32 and
                len(public_directed_translations) == 207 and
                len(directed_column_rows) == 2277 and
                public_directed_rounds[-1]["blocker_value_sha256"] ==
                V7_PREFIX_BINDINGS["final_blocker_sha256"] and
                public_directed_rounds[-1]["new_directed_translations"] == 0 and
                directed_stop_reason == "no_new_exact_directed_translation" and
                basis.columns_seen == 362725 and len(basis.rows) == 362709,
                "fresh saturated v7 prefix drift")
        receipt["directed_surgery"] = {
            "theorem": {
                "field": 3,
                "left_Fox_translation": True,
                "formula": "t=g*h^-1 and t*h=g",
                "matching_order": "relator index, component, canonical h bytes",
                "wrong_orientations_rejected": ["h^-1*g", "g^-1*h",
                                                "right translation"],
                "complete_eleven_relator_block_per_new_translation": True,
            },
            "rounds": public_directed_rounds,
            "round_count": len(public_directed_rounds),
            "rounds_sha256": digest_obj(public_directed_rounds),
            "volatile_rounds_sha256_provenance_only":
                V7_PREFIX_BINDINGS["volatile_rounds_sha256_provenance_only"],
            "stable_rounds_projection": stable_directed_rounds,
            "stable_rounds_projection_sha256": stable_rounds_sha,
            "stable_projection_omits_exactly":
                ["elapsed_seconds", "RSS_bytes"],
            "translations": public_directed_translations,
            "translation_count": len(public_directed_translations),
            "translations_sha256": translations_sha,
            "column_count": len(directed_column_rows),
            "columns_sha256": columns_sha,
            "column_order": "translation first-seen order, relator 1..11",
            "blocker_history": public_blocker_history_rows,
            "blocker_history_sha256": blocker_history_sha,
            "section_expressions": directed_expression_payload,
            "section_oracle": {
                "persistent_roots": "BFS and registered directed translations only",
                "base_D2_prefixes_frozen": True,
                "candidate_target_prefixes_transient": True,
                "blocker_recovery_complete_by_support_union": True,
                "canonical_bytes_binding": True,
                "pool_ID_binding_used": False,
                "recovery_failure_is_hard_FAIL": True,
                "expression_accounting": sections.expressions.accounting(),
            },
            "stop_reason": directed_stop_reason,
            "bounded_prefix_sha256": digest_obj({
                "translations": public_directed_translations,
                "columns_sha256": digest_obj(directed_column_rows),
                "blockers": public_blocker_history_rows,
                "rounds": public_directed_rounds,
            }),
        }
        refresh_prefix()
        # Establish a zero-prefix scan ledger immediately after the saturated
        # v7 fixed point.  A stop while binding pool/accounting data is then a
        # typed post-saturation/pre-scan RESOURCE receipt.
        receipt["_wordexpr_scan_records"] = []
        receipt["_wordexpr_scan_current"] = {
            "candidate_index": 1, "target_ordinal": 0,
            "target_name": None, "phase": "post_saturation_pre_scan",
        }
        receipt["_wordexpr_transaction"] = {
            "membership_starts": 0, "membership_rollbacks": 0,
            "proof_starts": 0, "proof_commits": 0, "proof_rollbacks": 0,
            "failed_candidate_DAG_nodes_allocated": 0,
            "max_pool_suffix": 0, "max_live_gradient_entries": 0,
        }
        pc_cache = _combined_pc_cache(e3, e4)
        pool_accounting = pool.accounting()
        pool_integrity = {
            "size": len(pool.values), "lookup_size": len(pool.ids),
            "all_unique": len(pool.values) == len(pool.ids),
            "fixed_width_bytes": pool.width,
            "ordered_canonical_payload_sha256": _pool_order_digest(pool, monitor),
            "digest_is_binding_only_not_equality": True,
            "exported_internal_IDs": False,
            "positive_external_IDs_are_mapped_by_quotient_element_registry": True,
        }
        search_accounting = {
            "method": "full frozen BFS basis followed by pivot-directed exact left translates",
            "translation_order": "BFS shortlex +1..+6,-1..-6, then directed canonical occurrence order",
            "pivot_order": "component then canonical EKey bytes (v2 exact order), never insertion ID",
            "translations_used": state["translations"],
            "directed_translations_used": len(directed_translation_rows),
            "total_complete_translation_blocks":
                state["translations"] + len(directed_translation_rows),
            "translates_per_relator": state["translations"],
            "columns_seen": basis.columns_seen,
            "dependent_columns": basis.dependent_columns,
            "basis_size": len(basis.rows), "pivot_count": len(basis.rows),
            "live_sparse_vector_entries": basis.live_vector_entries,
            "max_pivot_vector_support": basis.max_vector_support,
            "max_transient_vector_support": basis.max_transient_vector_support,
            "elimination_operations": basis.elimination_operations,
            "element_pool": pool_accounting,
            "element_pool_integrity": pool_integrity,
            "lazy_sections": sections.accounting(),
            "pc_caches": pc_cache,
            "provenance_DAG": {
                **dag.accounting(),
                "pivot_payload": "one packed sparse vector plus one packed DAG node id",
                "expanded_pivot_ledgers_stored": False,
                "failed_column_and_candidate_nodes_rolled_back": True,
                "positive_serialization": "root-reachable typed little-endian arrays only",
            },
            "candidate_membership_tests": tests,
            "same_basis_reused_for_fixed_candidate_retries": True,
            "corrected_Def2_9_acceptance_target_count": 33,
            "diagnostic_target_count": 17,
            "diagnostic_targets_feed_acceptance": False,
            "registered_correction_indices": [1],
            "registered_correction_word": [],
            "other_corrections_constructed_or_evaluated": 0,
            "correction_dictionary_constructed": False,
            "fixed_context_cheap_DP_executed": False,
            "direct_word_replay_count": direct_replay_count,
            "direct_vs_preflight_comparisons": direct_comparisons,
            "direct_vs_preflight_all_equal": all(
                row["equal_to_preflight"] for row in direct_comparisons),
            "persistent_candidate_cache_size": 0,
            "persistent_candidate_gradient_entries": 0,
            "candidate_target_streaming": True,
            "transaction": transaction,
            "transaction_contract": {
                "snapshot_before_complete_candidate_and_first_candidate_pool_intern": True,
                "pool_and_DAG_suffix_rollback": True,
                "element_ID_LRUs_cleared_before_ID_reuse": True,
                "persistent_basis_and_BFS_sections_immutable_during_candidate": True,
                "exported_blocker_expression_survives_candidate_rollback_by_canonical_bytes": True,
                "directed_basis_growth_persistent": True,
                "persistent_generator_and_inverse_tuple_anchors_replayed": True,
                "PC_collector_caches_store_canonical_coordinates_not_pool_IDs": True,
                "failed_candidate_gradients_retained": False,
            },
            "blocker_table": public_blockers(),
            "blocker_table_sha256": digest_obj(public_blockers()),
            "blocker_history": public_blocker_history_rows,
            "blocker_history_sha256": digest_obj(public_blocker_history_rows),
            "pivot_introductions": basis.pivot_introductions,
            "checkpoint_trace": public_checkpoint_trace,
            "checkpoint_trace_sha256": digest_obj(public_checkpoint_trace),
            "blocker_theorem": "a fully reduced missing target cannot solve until the exact missing pivot row is introduced",
            "selected_candidate_regenerated_and_exactly_compared": selected_candidate is not None,
            "geometric_translation_checkpoints": geometric_checkpoints,
            "fixed_candidate_scheduled_from_checkpoint": 1,
            "candidate_resource_skips": [],
            "candidate_local_resource_stop_is_global_UNKNOWN": True,
            "settled_automorphism_order_cache_size": len(inverse_cache),
            "quotient_inverse_cache": {
                "key": "exact ordered tuple of six stable E4 element IDs",
                "entries": len(inverse_cache), "capacity": 1,
                "hits": inverse_cache_stats["hits"],
                "misses": inverse_cache_stats["misses"],
                "tuple_match_count": inverse_cache_stats["hits"],
                "tuple_mismatch_count": inverse_cache_stats["misses"],
                "max_inverse_word_length": inverse_cache_stats["max_inverse_word_length"],
                "cached_datum": "one pinned normalized exponent-seven full inverse word tuple",
                "cache_hit_replays_current_ST_in_E4": True,
                "TS_replay_is_diagnostic_only": True,
                "different_tuple_is_candidate_local_UNKNOWN": True,
                "raw_endomorphism_powering_fallback": False,
                "candidate_relations_gradients_proof_roots_reused": False,
                "componentwise_Q4_Pi4_inverse_words_combined": False,
            },
            "direct_quotient_preflight_precedes_sparse_growth": True,
            "raw_power_inverse_removed": True,
            "small_projection_used": False, "affine_candidates_used": 0,
            "bounded_failure_is_not_nonexistence": True,
            "nonpositive_result_is_obstruction": False,
        }
        receipt["search"] = search_accounting
        receipt["bounded_search_prefix"] = search_prefix

        # v8 starts only after the fresh v7 basis has reached its exact fixed
        # point.  The helper returns every terminal; the frozen v7 terminal
        # block below remains unreachable semantic-reference code.
        return finish_wordexpr_scan(
            receipt, dictionary, source_tuples, raw_base_source_key,
            finite_inverse_words, direct, e3, e4, pool, sections, dag, basis,
            model3, model4, monitor, run_start, phase_timings,
            search_accounting, base_source_key, refresh_prefix)

        if selected_candidate is None:
            receipt["status"] = receipt["terminal_token"] = \
                "B345_RELFRAT3_PIVOT_SURGERY_INCOMPLETE"
            receipt["reason"] = (directed_stop_reason or
                                 "bounded directed surgery ended without all 33 proof roots")
            receipt["direct_lane"] = {
                "literal_pair_found": False, "PB5_branch_constructed": False,
                "PB5_reason": "fixed-candidate sparse membership remained incomplete",
            }
            receipt["claim_classification"] = "unknown_not_obstruction"
            receipt["claim_scope"] = "fixed_candidate_pivot_surgery_only"
            receipt["no_mathematical_obstruction_claimed"] = True
            receipt["full_universe_claimed"] = False
            receipt["negative_claimed"] = False
            monitor.check("bounded_search_complete", force=True)
            refresh_prefix()
            receipt["resource_guards"] = monitor.receipt(False)
            receipt["performance"] = {
                "runtime_seconds": time.monotonic()-run_start,
                "phase_complete": "bounded_search",
                "phase_timings_seconds": phase_timings,
                "cap_utilization": cap_utilization(),
            }
            return receipt

        require(selected_roots is not None and selected_bindings is not None,
                "selected transactional proof roots/bindings")
        monitor.check("positive_certificate_reconstruction", force=True)
        replay_stats = {"hits": 0, "misses": 0,
                        "max_inverse_word_length":
                            normalized_inverse["max_inverse_word_length"]}
        replay_candidate = corrected_def29_targets(complete_candidate(
            prepare_candidate(list(FIXED_WORD), [], e4), e4,
            DirectValuePool(), {raw_base_source_key: finite_inverse_words},
            replay_stats, normalized_inverse), e4)  # type: ignore[arg-type]
        require(not replay_candidate["quotient_bad"] and
                replay_candidate["targets"] == direct["targets"] and
                replay_stats["hits"] == 1 and replay_stats["misses"] == 0,
                "PASS direct fixed-candidate replay drift")
        search_prefix["fixed_candidate"]["direct_gate_replay_count"] += 1
        committed_pool_size = len(pool.values)
        regenerated_bindings: list[dict[str, Any]] = []
        selected_rows: list[tuple[str, str, list[int], SparseVector,
                                  dict[EKey, list[int]]]] = []
        for row_index, (name, kind, word) in enumerate(selected_candidate["targets"]):
            packed_gradient, packed_value = fox_gradient_packed(word, pool)
            binding = packed_gradient_binding(
                name, kind, packed_gradient, packed_value, pool)
            require(binding == selected_bindings[row_index],
                    "selected canonical gradient binding regeneration drift")
            regenerated_bindings.append(binding)
            gradient, value, support_sections = fox_gradient(word, e4)
            require(value == e4.identity and packed_value == pool.identity_id and
                    intern_raw_vector(gradient, pool) == packed_gradient,
                    f"selected raw/packed target regeneration: {name}")
            selected_rows.append((name, kind, word, gradient, support_sections))
        require(len(pool.values) == committed_pool_size,
                "selected regeneration introduced a new pool value")

        registry = ElementRegistry({3: e3, 4: e4})
        encoded_models = {
            "PB3": encode_fox_model(model3, e3, registry),
            "PB4": encode_fox_model(model4, e4, registry),
            "PB5": {"constructed": False,
                    "reason": "direct B3/B4 literal pair certified first"},
        }
        ordered_roots = {name: selected_roots[name]
                         for name, _, _, _, _ in selected_rows}
        proof_dag, root_renumber = serialize_proof_dag(
            dag, ordered_roots, basis, registry)
        certificates = []
        for name, kind, word, _, _ in selected_rows:
            monitor.check("boundary_certificate_serialization")
            certificates.append(boundary_certificate(
                name, kind, word, e4,
                root_renumber[selected_roots[name]], registry))
        monitor.check("positive_certificate_final_RSS", force=True)
        receipt["quotient_element_registry"] = registry.rows
        receipt["fox_models"] = encoded_models
        receipt["boundary_proof_dag"] = proof_dag
        receipt["search"]["provenance_DAG"]["serialized_reachable_nodes"] = \
            proof_dag["node_count"]
        receipt["search"]["provenance_DAG"]["serialized_reachable_edges"] = \
            proof_dag["edge_count"]
        receipt["search"]["selected_gradient_bindings"] = regenerated_bindings
        correction_index = selected_candidate["correction_index"]
        selected_public = {key: value for key, value in selected_candidate.items()
                           if key not in ("targets", "all_v6_targets",
                                          "diagnostic_targets", "quotient_bad") and
                           not key.startswith("_")}
        selected_public["correction_index"] = correction_index
        selected_public["boundary_certificate_names"] = [x["name"] for x in certificates]
        selected_public["correction_coarse_J_H_all_five_replayed"] = True
        selected_public["correction_finer_J_Phi_membership_not_required"] = True
        selected_public["all_ten_hexagon_coface_memberships_certified"] = True
        selected_public["ordered_A18_pentagon_certified"] = True
        selected_public["S_relations_certified"] = True
        selected_public["ST_generator_recovery_certified"] = True
        selected_public["T_TS_diagnostics_required_for_acceptance"] = False
        selected_public["diagnostics"] = selected_candidate["diagnostic_rows"]
        receipt["selected_pair"] = selected_public
        receipt["boundary_certificates"] = certificates
        receipt["literal_replay"] = {
            "correction_lift_freedom": {
                "coarse_J_H_all_five_cofaces_identity": True,
                "finer_J_Phi_membership_required": False,
                "J_H_mod_J_Phi_coset_is_varied": True,
            },
            "hexagon": {"two_source_residuals": True,
                         "each_checked_in_all_five_cofaces": True},
            "pentagon": {"ordered_five_coface_A18_direct_PB4_residual": True},
            "charming": {"explicit_commutator_product": True,
                          "error_checked_in_all_five_cofaces": True,
                          "raw_exponent_sums_used_as_criterion": False},
            "marking": {"m": 0, "lambda": 1, "additional_residuals": []},
            "onto": {"S_relations_killed": True,
                     "S_of_T_recovers_six_marked_generators": True,
                     "T_relations_diagnostic_only": True,
                     "T_of_S_diagnostic_only": True,
                     "corrected_Def2_9_IF_FIRST": True},
        }
        receipt["status"] = receipt["terminal_token"] = \
            "B345_RELFRAT3_PIVOT_SURGERY_PASS"
        receipt["claim_classification"] = "positive_certificate"
        receipt["claim_scope"] = "fixed_candidate_pivot_surgery_only"
        receipt["no_mathematical_obstruction_claimed"] = True
        receipt["reason"] = "the registered empty-correction outside pair has all literal gates and an exact packed shared sparse Phi3(H4) provenance DAG"
        receipt["direct_lane"] = {"literal_pair_found": True,
                                  "PB5_branch_constructed": False,
                                  "stop_reason": "FIRST_LITERAL_PAIR_AT_PHI"}
        require(len(pool.values) == pool_integrity["size"],
                "positive certificate introduced an unregistered pool value")
        receipt["search"]["element_pool"] = pool.accounting()
        receipt["search"]["pc_caches"] = _combined_pc_cache(e3, e4)
        refresh_prefix()
        receipt["resource_guards"] = monitor.receipt(False)
        receipt["performance"] = {
            "runtime_seconds": time.monotonic()-run_start,
            "phase_complete": "literal_pair",
            "quotient_registry_size": len(registry.rows),
            "cache_policy": "bounded exact LRUs, transactional pool/DAG suffixes, streamed candidate targets, packed reachable DAG",
            "phase_timings_seconds": phase_timings,
            "cap_utilization": cap_utilization(),
        }
        return receipt
    except ResourceStop as exc:
        if monitor.hit_reason is None:
            monitor.hit_reason = exc.reason
        search_prefix["structural_cap"] = {
            "hit": True, "reason": exc.reason,
            "source": ("monitor" if exc.reason in
                       {"producer_soft_timeout", "producer_soft_rss"}
                       else "registered_structural_cap"),
        }
        refresh_prefix()
        accounting: dict[str, Any] = {
            "live": live_accounting(),
            "monitor": monitor.receipt(True),
            "transaction": dict(transaction),
            "bounded_search_prefix": search_prefix,
        }
        stopped_cap_utilization = cap_utilization()
        if basis is not None:
            accounting["basis"] = basis.accounting()
        if pool is not None:
            accounting["element_pool"] = pool.accounting()
        receipt["blocker_table"] = public_blockers()
        receipt["blocker_history"] = blocker_history
        receipt["checkpoint_trace"] = checkpoint_trace
        receipt["pivot_introductions"] = ([] if basis is None else
                                           basis.pivot_introductions)
        receipt["direct_vs_preflight_comparisons"] = direct_comparisons
        receipt["directed_surgery_prefix"] = {
            "rounds": directed_round_rows,
            "round_count": len(directed_round_rows),
            "translations": directed_translation_rows,
            "translation_count": len(directed_translation_rows),
            "columns_count": len(directed_column_rows),
            "columns_sha256": digest_obj(directed_column_rows),
            "expression_accounting": (None if sections is None else
                                      sections.expressions.accounting()),
            "resource_interrupted": True,
        }
        internal_scan_records = receipt.pop("_wordexpr_scan_records", [])
        internal_scan_current = receipt.pop("_wordexpr_scan_current", None)
        internal_wordexpr_transaction = receipt.pop(
            "_wordexpr_transaction",
            receipt.get("wordexpr_scan", {}).get("transaction"))
        internal_memo_performance = receipt.pop("_memo_performance", None)
        if internal_memo_performance is not None:
            receipt["gradient_memo_performance"] = {
                **internal_memo_performance,
                "partial_resource_stop": True,
                "candidate_order_changed": False,
                "acceptance_or_diagnostic_promotion_changed": False,
                "memo_eviction_is_terminal_or_rejection": False,
                "cache_entry_budget_bytes":
                    CAPS["gradient_memo_additional_budget_bytes"],
                "working_plus_cached_accounted_under_frozen_live_cap": True,
            }
        elif "gradient_memo_performance" in receipt:
            receipt["gradient_memo_performance"][
                "partial_resource_stop"] = True
        if internal_scan_records and pool is not None:
            receipt["wordexpr_scan"] = encode_scan_prefix(
                internal_scan_records, pool.width, False)
            receipt["wordexpr_scan"].update({
                "registered_corrections": 4096,
                "registered_dictionary_complete": True,
                "partial_resource_stop": True,
                "current": internal_scan_current,
                "no_candidate_skip_interpreted_as_failure": True,
                "transaction": internal_wordexpr_transaction,
            })
        elif internal_scan_current is not None:
            receipt["wordexpr_scan"] = {
                "format": "registered-wordexpr-scan-arrays/v1",
                "evaluated": 0, "complete": False,
                "registered_corrections": 4096,
                "registered_dictionary_complete": True,
                "partial_resource_stop": True,
                "current": internal_scan_current,
                "no_candidate_skip_interpreted_as_failure": True,
                "transaction": internal_wordexpr_transaction,
            }
        if internal_wordexpr_transaction is not None:
            accounting["wordexpr_scan_transaction"] = \
                internal_wordexpr_transaction
            accounting["transaction_role"] = \
                "v7_directed_prefix_only; see wordexpr_scan_transaction"
        receipt.pop("boundary_proof_dag", None)
        receipt.pop("boundary_certificates", None)
        receipt.pop("selected_wordexpr_dag", None)
        receipt.pop("selected_pair", None)
        receipt.pop("quotient_element_registry", None)
        receipt.pop("fox_models", None)
        receipt.pop("literal_replay", None)
        receipt.pop("direct_lane", None)
        receipt["resource_accounting_at_stop"] = accounting
        if proof_dag is not None:
            proof_dag.clear()
        if registry is not None:
            registry.ids.clear()
            registry.rows.clear()
        if basis is not None:
            basis.clear()
        if dag is not None:
            dag.clear()
        if sections is not None:
            sections.clear()
        if pool is not None:
            pool.clear_large()
        if e3 is not None:
            e3.pc.clear_caches()
        if e4 is not None:
            e4.pc.clear_caches()
        gc.collect()
        receipt["status"] = receipt["terminal_token"] = \
            "B345_RELFRAT3_WORDEXPR_UNKNOWN_RESOURCE"
        receipt["reason"] = exc.reason
        receipt["resource_stop"] = {
            "cap": exc.reason,
            "candidate_local": internal_scan_current is not None,
            "large_structures_released_before_write": True,
            "no_mathematical_obstruction_claimed": True,
        }
        receipt["claim_classification"] = "unknown_not_obstruction"
        receipt["claim_scope"] = \
            "registered_4096_wordexpr_positive_search_only"
        receipt["no_mathematical_obstruction_claimed"] = True
        receipt["full_universe_claimed"] = False
        receipt["negative_claimed"] = False
        receipt["bounded_search_prefix"] = search_prefix
        receipt["resource_guards"] = monitor.receipt(True)
        receipt["performance"] = {
            "runtime_seconds": time.monotonic()-run_start,
            "phase_complete": "resource_stop",
            "phase_timings_seconds": phase_timings,
            "cap_utilization": stopped_cap_utilization,
        }
        return receipt


def self_test() -> None:
    require([len(pure_relations(r)) for r in (3, 4, 5)] == [2, 11, 35],
            "presentation counts")
    ledger = derived_commutator_ledger(FIXED_WORD)
    require(ledger["expanded_word"] == FIXED_WORD and ledger["factor_count"] > 0,
            "derived ledger")
    h = hexagon_words([])
    require(h == [[], []] and pentagon_word([]) == [], "trivial literal formulas")
    require(len(cofaces(3)) == 5 and
            [m[0] for m in [cofaces(3)[i] for i in (4, 0, 1, 2, 3)]] ==
            [[1], [4], [2, 4], [1, 2], [1]], "A18 coface order")
    class TrivialE4:
        identity = 0
        generators = [0] * 6

        @staticmethod
        def eval(word: Sequence[int], images: Sequence[int] | None = None) -> int:
            return 0

    toy = TrivialE4()
    toy_key = tuple(toy.generators)
    toy_cache = {toy_key: [[i] for i in range(1, 7)]}
    toy_stats = {"hits": 0, "misses": 0, "max_inverse_word_length": 0}
    toy_normalized = {"selected_correction_index": 1, "passing_indices": [1]}
    class TrivialPool:
        @staticmethod
        def intern(value: int) -> int:
            return value

    first = finite_normalized_inverse([], toy, TrivialPool(), toy_cache,
                                      toy_stats, toy_normalized)
    second = finite_normalized_inverse([1], toy, TrivialPool(), toy_cache,
                                       toy_stats, toy_normalized)
    require(first["source_words"] != second["source_words"] and
            toy_stats == {"hits": 2, "misses": 0,
                          "max_inverse_word_length": 1},
            "same E4 tuple/distinct free representative cache-hit canary")
    pc_receipt = {
        "generator_count": 1,
        "relative_orders": [3],
        "power_relations": [[0]],
        "inverses": [[2]],
        "conjugate_relations": [],
        "inverse_conjugate_relations": [],
    }
    pc = PcCollector(pc_receipt)
    one, a, b = pc.coord([0]), pc.coord([1]), pc.coord([2])
    corpus = [one, a, b]
    require(all(pc.mul(left, right) ==
                pc.collect_uncached(coords_word(left)+coords_word(right))
                for left in corpus for right in corpus) and
            all(pc.mul(left, right) ==
                pc.collect_uncached(coords_word(left)+coords_word(right))
                for left in corpus for right in corpus) and
            pc.cache_accounting()["hits"] >= 9,
            "bounded cached/uncached PC canary")

    class ToyPC:
        n = 1

        @staticmethod
        def cache_accounting() -> dict[str, Any]:
            empty = {"capacity": 1, "size": 0, "peak": 0, "hits": 0,
                     "misses": 0, "evictions": 0, "clears": 0}
            return {"pair_product": dict(empty), "inverse": dict(empty),
                    "hits": 0, "misses": 0, "evictions": 0,
                    "unbounded_full_token_word_cache": False,
                    "policy": "toy"}

    class ToyQuotient:
        rank = 4
        degree = 3
        pc = ToyPC()
        identity = (bytes(range(3)), bytes([0]))
        generators = [(bytes(range(3)), bytes([1]))] + [identity] * 5
        inverse_generators = [(bytes(range(3)), bytes([2]))] + [identity] * 5

        @staticmethod
        def mul(left: EKey, right: EKey) -> EKey:
            return bytes(range(3)), bytes([(left[1][0]+right[1][0]) % 3])

        @staticmethod
        def inverse(value: EKey) -> EKey:
            return bytes(range(3)), bytes([(-value[1][0]) % 3])

        def eval(self, word: Sequence[int], images: Sequence[EKey] | None = None) -> EKey:
            marked = self.generators if images is None else images
            out = self.identity
            for letter in word:
                value = marked[abs(letter)-1]
                out = self.mul(out, value if letter > 0 else self.inverse(value))
            return out

    tq = ToyQuotient()
    epool = ElementPool(tq)  # type: ignore[arg-type]
    require(epool.intern(tq.generators[0]) == epool.generator_ids[0] and
            len(epool.values) == len(epool.ids) == 3,
            "exact interning canary")
    slp = LazySectionSLP(epool.identity_id)
    packed_bfs = list(translation_bfs(epool, slp, 3))
    reference_bfs = list(_v2_reference_translation_bfs(tq, 3))
    require([epool.value(eid) for eid, _ in packed_bfs] ==
            [value for value, _ in reference_bfs] and
            [slp.materialize(node) for _, node in packed_bfs] ==
            [word for _, word in reference_bfs],
            "lazy/reference BFS order and section canary")
    raw_gradient, raw_value, _ = fox_gradient([1, 1, 1], tq)  # type: ignore[arg-type]
    packed_gradient, packed_value = fox_gradient_packed([1, 1, 1], epool)
    require(raw_value == tq.identity and packed_value == epool.identity_id and
            intern_raw_vector(raw_gradient, epool) == packed_gradient and
            d1(raw_gradient, tq) == {} and d1_packed(packed_gradient, epool) == {},
            "v2/reference versus packed Fox column differential")

    toy_dag = ProvenanceDAG()
    leaf_a = toy_dag.leaf(1, epool.identity_id)
    leaf_b = toy_dag.leaf(2, epool.generator_ids[0])
    root = toy_dag.linear([(leaf_a, 1), (leaf_b, 2)])
    checkpoint = toy_dag.checkpoint()
    toy_dag.linear([(root, 2), (leaf_a, 1)])
    toy_dag.rollback(checkpoint)
    require(root == 4 and toy_dag.terms(root) ==
            [(leaf_a, 1), (leaf_b, 2)] and toy_dag.reachable([root]) ==
            {leaf_a, leaf_b, root}, "shared provenance DAG/rollback canary")

    toy_sections = LazySectionSLP(epool.identity_id)
    first_node = toy_sections.append(0, 1)
    toy_sections.bind(epool.generator_ids[0], first_node)
    relator_column = {pack_vector_key(1, epool.identity_id): 1}
    toy_basis = SparseBoundaryBasis(epool, [relator_column], ProvenanceDAG(),
                                    toy_sections)
    toy_basis.add_column(1, epool.identity_id, 0)
    require(toy_basis.solve(relator_column) is not None and
            toy_basis.pivot({pack_vector_key(2, epool.generator_ids[0]): 1,
                             pack_vector_key(1, epool.inverse_generator_ids[0]): 1}) ==
            pack_vector_key(1, epool.inverse_generator_ids[0]),
            "packed translated-column/basis/pivot-order canary")

    # Bounded exact fixed-context DP versus literal direct evaluation for every
    # correction, including every named context and failure bit.
    seed = [1]
    toy_words = [[], [1], [-1], [1, 1]]
    toy_dictionary = {
        "words": toy_words, "count": len(toy_words), "seed_words": [seed],
        "parent_indices": [0, 1, 1, 2],
        "signed_seed_edges": [0, 1, -1, 1],
    }
    toy_prefix = {"cheap": {"evaluated": 0, "completed": False,
                              "survivor_count": 0,
                              "survivor_indices_sha256": digest_obj([]),
                              "evaluated_prefix_sha256": hashlib.sha256(b"").hexdigest(),
                              "survivor_prefix_sha256": hashlib.sha256(b"").hexdigest(),
                              "current_candidate": 1}}
    toy_monitor = ResourceMonitor(time.monotonic(),
                                  CAPS["producer_soft_timeout_seconds"],
                                  rss_reader=lambda: 0)
    toy_dp, toy_failures = fixed_context_cheap_dp(
        toy_dictionary, tq, toy_monitor, toy_prefix)  # type: ignore[arg-type]
    direct_failures = [cheap_candidate_bad(
        reduce_word(FIXED_WORD+word), word, tq) for word in toy_words]  # type: ignore[arg-type]
    require(toy_failures == direct_failures and
            toy_dp["evaluated"] == len(toy_words) and
            toy_dp["contexts"]["named_use_count"] == 46 and
            len(toy_dp["failure_bitsets"]) == 27 and
            toy_prefix["cheap"]["completed"] is True,
            "fixed-context DP/direct and named failure-bit canary")

    # Streamed target solving has the same result as the v3 all-target helper;
    # the exact missing pivot blocks until its watched row is introduced.
    existing_target = dict(relator_column)
    missing_target = {pack_vector_key(2, epool.generator_ids[0]): 1}
    outer_dag_checkpoint = toy_basis.dag.checkpoint()
    streamed_first, first_missing = toy_basis.solve_with_blocker(existing_target)
    streamed_second, second_missing = toy_basis.solve_with_blocker(missing_target)
    toy_basis.dag.rollback(outer_dag_checkpoint)
    compact = CompactCandidate(1, ("existing", "missing"), ("toy", "toy"),
                               (existing_target, missing_target),
                               (epool.identity_id, epool.identity_id))
    require(streamed_first is not None and first_missing is None and
            streamed_second is None and second_missing is not None and
            solve_candidate(compact, toy_basis) is None,
            "streamed versus v3 all-target miss")
    missing_component, missing_element = unpack_vector_key(second_missing)
    missing_blob = epool.blob(missing_element)
    toy_basis.watch_blocker(missing_component, missing_blob)
    require(second_missing not in toy_basis.rows, "blocker skip before pivot")
    toy_basis.relator_columns.append(dict(missing_target))
    toy_basis.add_column(2, epool.identity_id, 0, translation_ordinal=2)
    require(second_missing in toy_basis.rows and
            toy_basis.pivot_introductions == [{
                "component": missing_component, "element_hex": missing_blob.hex(),
                "translation_ordinal": 2, "relator_index": 2}] and
            toy_basis.solve_with_blocker(missing_target)[0] is not None,
            "mandatory retry after exact blocker pivot introduction")

    # The transaction starts before the first candidate-only intern.  Rollback
    # removes the entire pool/DAG suffix, clears both ID-bearing LRUs, and then
    # permits the numeric ID to be reused without touching basis or SLP state.
    tx = candidate_transaction_snapshot(epool, toy_basis.dag,
                                        toy_basis, toy_sections)
    candidate_value = (bytes([1, 0, 2]), bytes([0]))
    candidate_id = epool.intern(candidate_value)
    epool.mul_id(epool.identity_id, candidate_id)
    epool.inverse_id(candidate_id)
    toy_basis.dag.linear([(toy_basis.rows[second_missing][1], 1),
                          (toy_basis.rows[next(iter(toy_basis.rows))][1], 1)])
    removed = rollback_candidate_transaction(
        tx, epool, toy_basis.dag, toy_basis, toy_sections)
    reused = epool.intern((bytes([2, 1, 0]), bytes([0])))
    binding = packed_gradient_binding("toy", "toy", existing_target,
                                      epool.identity_id, epool)
    require(removed >= 1 and reused == candidate_id and
            epool.product_cache.accounting()["clears"] >= 1 and
            epool.inverse_cache.accounting()["clears"] >= 1 and
            binding == packed_gradient_binding("toy", "toy", existing_target,
                                                epool.identity_id, epool),
            "transaction rollback/ID reuse/PASS binding regeneration")

    guard = ResourceMonitor(time.monotonic(), CAPS["producer_soft_timeout_seconds"],
                            rss_reader=lambda: CAPS["producer_soft_rss_bytes"])
    try:
        guard.check("selftest_RSS", force=True)
        raise Reject("RSS guard did not stop")
    except ResourceStop as exc:
        require(exc.reason == "producer_soft_rss", "RSS UNKNOWN canary")
    require(TERMINALS == {"B345_RELFRAT3_LITERAL_PAIR_PASS",
                          "B345_RELFRAT3_SEARCH_INCOMPLETE",
                          "B345_RELFRAT3_UNKNOWN_RESOURCE"},
            "terminal mutation canary")
    print("D972_B345_RELFRAT3_V4_PRODUCER_SELFTEST_PASS "
          f"relevant_formula_sha256={digest_obj(relevant_formula())} "
          "interning=1 pc_cache_differential=1 bfs_differential=1 "
          "cheap_DP_direct=4 named_contexts=46 streamed_vs_v3=1 "
          "missing_pivot_retry=1 transaction_rollback_ID_reuse=1 "
          "PASS_regeneration=1 packed_DAG_rollback=1 RSS_UNKNOWN=1 "
          "terminals=3 structural_UNKNOWN=1")


def self_test_fixed() -> None:
    changed_caps = {key for key in CAPS if CAPS[key] != V5_CAPS[key]}
    require(changed_caps == {"total_sparse_group_ring_keys", "element_pool"} and
            CAPS["total_sparse_group_ring_keys"] == 4_194_304 and
            CAPS["element_pool"] == 2_000_000 and
            CAP_CALIBRATION["semantics_changed"] is False and
            CAP_CALIBRATION["resume_used"] is False,
            "cap-only v5/v6 delta")
    require(set(CAPS)-set(V6_CAPS) == {
                "directed_surgery_rounds", "directed_unique_translations",
                "directed_columns", "directed_section_expr_nodes",
                "directed_section_expr_edges"} and
            all(CAPS[key] == V6_CAPS[key] for key in V6_CAPS),
            "exact v6/v7 cap delta")
    stride = CAPS["element_pool"]
    stride_ids = [0, 1, 17, stride-1]
    stride_keys = {left*stride+right
                   for left in stride_ids for right in stride_ids}
    require(len(stride_keys) == len(stride_ids)**2 and
            all(divmod(left*stride+right, stride) == (left, right)
                for left in stride_ids for right in stride_ids),
            "element-pool product-cache stride injective")
    toy_old_prefix = {
        "live_sparse_entries": V5_CAPS["total_sparse_group_ring_keys"]+1,
        "pivots": ((1, "61"), (2, "62")),
        "values": ("61", "62"),
        "order": "component_then_canonical_bytes",
    }
    before = digest_obj({key: value for key, value in toy_old_prefix.items()
                         if key != "live_sparse_entries"})
    require(toy_old_prefix["live_sparse_entries"] >
            V5_CAPS["total_sparse_group_ring_keys"] and
            toy_old_prefix["live_sparse_entries"] <=
            CAPS["total_sparse_group_ring_keys"] and
            before == digest_obj({key: value for key, value in
                                  toy_old_prefix.items()
                                  if key != "live_sparse_entries"}),
            "old-cap toy prefix continues without semantic drift")
    universe = {
        "kind": "fixed_positive_candidate", "correction_indices": [1],
        "correction_word": [], "full_4096_universe_claimed": False,
        "earliest_global_candidate_claimed": False,
        "negative_completeness_claimed": False,
    }
    require(universe["correction_indices"] == [1] and
            universe["correction_word"] == [] and
            all(universe[key] is False for key in
                ("full_4096_universe_claimed",
                 "earliest_global_candidate_claimed",
                 "negative_completeness_claimed")),
            "fixed universe")

    class TrivialE4:
        identity: EKey = (b"\x00", b"\x00")
        generators = [identity]*6

        @staticmethod
        def mul(left: EKey, right: EKey) -> EKey:
            return TrivialE4.identity

        @staticmethod
        def inverse(value: EKey) -> EKey:
            return TrivialE4.identity

        @staticmethod
        def eval(word: Sequence[int],
                 images: Sequence[EKey] | None = None) -> EKey:
            return TrivialE4.identity

    class DirectPool:
        @staticmethod
        def intern(value: int) -> int:
            return value

    toy = TrivialE4()
    source_key = tuple(toy.eval(word) for word in source_words_m0(FIXED_WORD))
    stats = {"hits": 0, "misses": 0, "max_inverse_word_length": 1}
    fixed = corrected_def29_targets(complete_candidate(
        prepare_candidate(list(FIXED_WORD), [], toy), toy, DirectPool(),
        {source_key: [[i] for i in range(1, 7)]}, stats,
        {"selected_correction_index": 1, "passing_indices": [1]}), toy)
    names = [name for name, _, _ in fixed["targets"]]
    require(not fixed["quotient_bad"] and len(names) == 33 and
            len(fixed["diagnostic_targets"]) == 17 and
            names[5] == "hexagon_1_coface_0" and stats["hits"] == 1 and
            max(len(word) for _, _, word in fixed["targets"]) <=
            CAPS["single_word_or_section_length"],
            "fixed direct gates/target order")

    class ToyPC:
        n = 1

        @staticmethod
        def cache_accounting() -> dict[str, Any]:
            row = {"capacity": 1, "size": 0, "peak": 0, "hits": 0,
                   "misses": 0, "evictions": 0, "clears": 0}
            return {"pair_product": dict(row), "inverse": dict(row),
                    "hits": 0, "misses": 0, "evictions": 0,
                    "unbounded_full_token_word_cache": False,
                    "policy": "toy"}

    class ToyQuotient:
        rank = 4
        degree = 3
        pc = ToyPC()
        identity = (bytes(range(3)), bytes([0]))
        generators = [(bytes(range(3)), bytes([1]))] + [identity]*5
        inverse_generators = [(bytes(range(3)), bytes([2]))] + [identity]*5

        @staticmethod
        def mul(left: EKey, right: EKey) -> EKey:
            return bytes(range(3)), bytes([(left[1][0]+right[1][0]) % 3])

        @staticmethod
        def inverse(value: EKey) -> EKey:
            return bytes(range(3)), bytes([(-value[1][0]) % 3])

        def eval(self, word: Sequence[int],
                 images: Sequence[EKey] | None = None) -> EKey:
            marked = self.generators if images is None else images
            out = self.identity
            for letter in word:
                value = marked[abs(letter)-1]
                out = self.mul(out, value if letter > 0 else self.inverse(value))
            return out

    tq = ToyQuotient()
    pool = ElementPool(tq)  # type: ignore[arg-type]
    pool.product_cache = BoundedLRU(1)
    aid = pool.generator_ids[0]
    bid = pool.inverse_generator_ids[0]
    expected_ab = tq.mul(pool.value(aid), pool.value(bid))
    first_ab = pool.value(pool.mul_id(aid, bid))
    hit_ab = pool.value(pool.mul_id(aid, bid))
    pool.mul_id(aid, aid)  # Different key evicts the one-entry cache.
    second_ab = pool.value(pool.mul_id(aid, bid))
    hits_before_clear = pool.product_cache.hits
    pool.product_cache.clear()
    third_ab = pool.value(pool.mul_id(aid, bid))
    require(first_ab == hit_ab == second_ab == third_ab == expected_ab and
            pool.product_cache.evictions >= 1 and hits_before_clear >= 1,
            "product-cache hit/eviction/clear neutrality")
    sections = SparseSectionOracle(pool)
    dag = ProvenanceDAG()
    first_target = {pack_vector_key(1, pool.identity_id): 1}
    basis = SparseBoundaryBasis(pool, [first_target], dag, sections)
    basis.add_column(1, pool.identity_id, 0, translation_ordinal=1)
    missing1 = {pack_vector_key(2, pool.generator_ids[0]): 1}
    _, blocker1 = basis.solve_with_blocker(missing1)
    require(blocker1 is not None and blocker1 not in basis.rows,
            "checkpoint-1 reconstructed blocker")
    component1, element1 = unpack_vector_key(blocker1)
    blob1 = pool.blob(element1)
    basis.watch_blocker(component1, blob1)
    require(blocker1 not in basis.rows, "skip before exact pivot")
    basis.relator_columns.append(missing1)
    basis.add_column(2, pool.identity_id, 0, translation_ordinal=2)
    require(blocker1 in basis.rows and
            basis.solve_with_blocker(missing1)[0] is not None,
            "mandatory retry after pivot introduction")
    basis.blocker_watches.discard((component1, blob1))
    missing2 = {pack_vector_key(3, pool.inverse_generator_ids[0]): 1}
    _, blocker2 = basis.solve_with_blocker(missing2)
    require(blocker2 is not None and blocker2 != blocker1,
            "later blocker replacement")

    snapshot = candidate_transaction_snapshot(pool, dag, basis, sections)
    candidate_id = pool.intern((bytes([1, 0, 2]), bytes([0])))
    pool.mul_id(pool.identity_id, candidate_id)
    pool.inverse_id(candidate_id)
    dag.linear([(basis.rows[blocker1][1], 1),
                (basis.rows[next(iter(basis.rows))][1], 1)])
    removed = rollback_candidate_transaction(
        snapshot, pool, dag, basis, sections)
    reused = pool.intern((bytes([2, 1, 0]), bytes([0])))
    binding = packed_gradient_binding(
        "fixed", "toy", first_target, pool.identity_id, pool)
    require(removed >= 1 and reused == candidate_id and
            pool.product_cache.accounting()["clears"] >= 1 and
            pool.inverse_cache.accounting()["clears"] >= 1 and
            binding == packed_gradient_binding(
                "fixed", "toy", first_target, pool.identity_id, pool),
            "transaction rollback/LRU/PASS regeneration")

    # Exact left-directed theorem and sparse section oracle.
    target_blob = pool.blob(pool.generator_ids[0])
    target_root, target_recovery = sections.recover_blocker(
        1, target_blob, {(1, target_blob): [1]}, [])
    require(target_recovery["method"] == "target_support_prefix" and
            sections.expressions.value_blob(target_root) == target_blob,
            "target-prefix blocker oracle")
    base_root = sections.register_base_prefix(
        1, pool.blob(pool.identity_id), [])
    inverse_base = sections.expressions.inverse(base_root, "toy_base_inverse")
    directed_root = sections.expressions.product(
        target_root, inverse_base, "registered_directed_translation")
    section_node, created = sections.register_directed(
        pool.value(pool.generator_ids[0]), directed_root)
    duplicate_node, duplicate_created = sections.register_directed(
        pool.value(pool.generator_ids[0]), directed_root)
    raw_rows = [{"relator_index": 1, "component": 1, "coefficient": 1,
                 "element_hex": pool.blob(pool.identity_id).hex(),
                 "section_word": [], "section_expression_root": base_root,
                 "_value": pool.value(pool.identity_id)}]
    raw_root, raw_recovery = sections.recover_blocker(
        1, target_blob, {}, raw_rows)
    require(created and not duplicate_created and section_node == duplicate_node and
            sections.expressions.value_blob(raw_root) == target_blob and
            raw_recovery["method"] ==
                "registered_translation_times_base_prefix",
            "raw-column sparse oracle/deduplication")
    try:
        sections.recover_blocker(2, target_blob, {}, [])
    except Reject:
        pass
    else:
        raise Reject("unrecoverable blocker was not a hard invariant failure")
    try:
        sections.expressions.flat([1], pool.blob(pool.identity_id), "forged")
    except Reject:
        pass
    else:
        raise Reject("forged section accepted")
    # In S4 take g=(0 1 2) and h=(0 3).  Unlike a reflection normalizing
    # <g> inside S3, this h keeps all four orientation words distinct.
    gperm = bytes([1, 2, 0, 3])
    hperm = bytes([3, 1, 2, 0])
    correct = perm_mul(gperm, perm_inv(hperm))
    wrong_left = perm_mul(perm_inv(hperm), gperm)
    wrong_inverse = perm_mul(perm_inv(gperm), hperm)
    wrong_right = perm_mul(hperm, perm_inv(gperm))
    require(perm_mul(correct, hperm) == gperm and
            len({correct, wrong_left, wrong_inverse, wrong_right}) == 4 and
            perm_mul(hperm, correct) != gperm,
            "three wrong directed orientations")

    prefix = {
        "current": {"checkpoint": 1, "correction_index": 1,
                    "target_ordinal": 6,
                    "target_name": "hexagon_1_coface_0"},
        "blocker": {"count": 1, "sha256": digest_obj([blob1.hex()])},
        "transaction": {"starts": 1, "commits": 0, "rollbacks": 1},
        "structural_cap": {"hit": True, "reason": "element_pool",
                           "source": "registered_structural_cap"},
    }
    require(prefix["current"]["target_ordinal"] == 6 and
            prefix["structural_cap"]["reason"] == "element_pool" and
             TERMINALS == {
                 "B345_RELFRAT3_WORDEXPR_PASS",
                 "B345_RELFRAT3_WORDEXPR_SEARCH_INCOMPLETE",
                 "B345_RELFRAT3_WORDEXPR_UNKNOWN_RESOURCE",
                 "B345_RELFRAT3_WORDEXPR_UNKNOWN_INPUT"},
             "fixed terminal/prefix canary")
    print("D972_B345_RELFRAT3_PIVOT_SURGERY_V7_PRODUCER_SELFTEST_PASS "
          "universe=1 dictionary_DP_calls=0 acceptance=33 diagnostics=17 "
          "blocker_ordinal=6 sparse_oracle=target+raw directed_orientation=1 "
          "transaction_rollback_ID_reuse=1 PASS_regeneration=1 terminals=4 "
          "structural_UNKNOWN=1 cap_delta=5 canonical_dedup=1 hard_fail=1")


def self_test_wordexpr_memo_v9() -> None:
    # Keep all frozen v7 arithmetic/pool/transaction canaries, then exercise
    # the new production WordExpr evaluator on a noncommutative exact quotient.
    self_test_fixed()

    class ToyQ:
        rank = 4
        degree = 3
        class ToyPC:
            n = 0
            receipt = {"fixture": "trivial-pc-rank-zero"}
        pc = ToyPC()
        # Use the production canonical EKey representation.  Mixing tuple
        # permutations with the bytes returned by perm_mul made the original
        # fixture compare unequal despite identical group elements.
        identity: EKey = (bytes(range(3)), b"")
        _a: EKey = (bytes((1, 2, 0)), b"")
        _b: EKey = (bytes((1, 0, 2)), b"")
        generators = [_a, _b] + [identity]*4
        inverse_generators = [
            (perm_inv(_a[0]), b""), (perm_inv(_b[0]), b"")] + [identity]*4

        @staticmethod
        def mul(left: EKey, right: EKey) -> EKey:
            return perm_mul(left[0], right[0]), b""

        @staticmethod
        def inverse(value: EKey) -> EKey:
            return perm_inv(value[0]), b""

        def eval(self, word: Sequence[int],
                 images: Sequence[EKey] | None = None) -> EKey:
            marked = self.generators if images is None else list(images)
            value = self.identity
            for letter in word:
                step = marked[abs(letter)-1]
                value = self.mul(value, step if letter > 0 else
                                 self.inverse(step))
            return value

    q = ToyQ()
    expr = WordExprDAG()
    x = expr.flat([1], 6)
    y = expr.flat([2], 6)
    xy = expr.product(x, y)
    inv_xy = expr.inverse(xy)
    substituted = expr.substitute([1, -2, 1], [xy, inv_xy, x, y, x, y])
    evaluator = WordExprEvaluator(
        expr, q, {"candidate_index": 1, "fixture": "memo"})  # type: ignore[arg-type]
    evaluator.evaluate_values()
    gradient = evaluator.evaluate_gradients([substituted])[substituted]
    flat = expr.expand_reduced_below_flat_cap(substituted)
    flat_gradient, flat_value, _ = fox_gradient(flat, q)  # type: ignore[arg-type]
    require(flat_value == evaluator.values[substituted-1] and
            flat_gradient == gradient,
            "WordExpr toy product/inverse/substitution differential")

    negative = expr.substitute([-1], [xy, y, x, y, x, y])
    evaluator = WordExprEvaluator(
        expr, q, {"candidate_index": 1, "fixture": "negative"})  # type: ignore[arg-type]
    evaluator.evaluate_values()
    negative_gradient = evaluator.evaluate_gradients([negative])[negative]
    negative_flat = expr.expand_reduced_below_flat_cap(negative)
    direct_negative, _, _ = fox_gradient(negative_flat, q)  # type: ignore[arg-type]
    wrong_negative = _raw_gradient_translate(
        evaluator.evaluate_gradients([xy])[xy], q.identity, q, 2)  # type: ignore[arg-type]
    require(negative_gradient == direct_negative and
            negative_gradient != wrong_negative,
            "WordExpr negative-prefix orientation")

    long_expr = WordExprDAG()
    current = long_expr.flat([1], 6)
    one = long_expr.identity(6)
    for _ in range(18):
        current = long_expr.substitute([1, 1],
                                       [current, one, one, one, one, one])
    require(long_expr.expanded_count[current-1] == 262144 and
            long_expr.expanded_count[current-1] >
            CAPS["single_word_or_section_length"],
            "WordExpr long nested count")
    long_eval = WordExprEvaluator(
        long_expr, q, {"candidate_index": 1, "fixture": "long"})  # type: ignore[arg-type]
    long_eval.evaluate_values()
    long_gradient = long_eval.evaluate_gradients([current])[current]
    require(isinstance(long_gradient, dict) and
            long_expr.expanded_count[current-1] <=
            CAPS["wordexpr_expanded_letter_count_per_target"],
            "WordExpr long nested chain rule without materialization")

    # Production memo-key and lifecycle canaries.  The two expressions below
    # have the same quotient value but different Fox gradients, so value-only
    # aliasing would be detected immediately.
    identity = expr.identity(6)
    x3 = expr.product_many([x, x, x])
    z = expr.flat([3], 6)
    alias_eval = WordExprEvaluator(
        expr, q, {"candidate_index": 11, "fixture": "alias"},
        memo_node_cap=8, memo_sparse_cap=64)  # type: ignore[arg-type]
    alias_eval.evaluate_values()
    alias_gradients = alias_eval.evaluate_gradients([identity, x3])
    require(alias_eval.values[identity-1] == alias_eval.values[x3-1] and
            alias_gradients[identity] != alias_gradients[x3] and
            alias_eval.memo.typed_key(identity) !=
                alias_eval.memo.typed_key(x3),
            "memo equal-value/different-expression nonalias")

    def rejected(call: Any) -> bool:
        try:
            call()
        except Reject:
            return True
        return False

    require(rejected(lambda: alias_eval.memo.lookup(
                x, candidate_binding_sha256="0"*64)) and
            rejected(lambda: alias_eval.memo.lookup(
                x, supplied_key="f"*64)),
            "memo forged/cross-candidate key rejection")
    old_key = alias_eval.memo.typed_key(x)
    alias_eval.discard_candidate_memo()
    reuse_eval = WordExprEvaluator(
        expr, q, {"candidate_index": 12, "fixture": "reuse"},
        memo_node_cap=2, memo_sparse_cap=64)  # type: ignore[arg-type]
    reuse_eval.evaluate_values()
    for root in (x, y, z, x):
        reuse_eval.evaluate_gradients([root])
    require(old_key != reuse_eval.memo.typed_key(x) and
            reuse_eval.memo.evictions > 0 and
            reuse_eval.memo.recomputations > 0,
            "memo rollback/LRU eviction/recomputation")
    six_anchors = [x, y, xy, inv_xy, substituted, negative]
    anchor_eval = WordExprEvaluator(
        expr, q, {"candidate_index": 13, "fixture": "anchors"})  # type: ignore[arg-type]
    anchor_eval.evaluate_values()
    anchor_eval.pin_source_roots(six_anchors)
    # A second request must hit the pinned typed entry; the first multi-root
    # traversal is deliberately cold and therefore is not itself a hit test.
    anchor_eval.evaluate_gradients([substituted])
    require(len(anchor_eval.memo.pinned_keys) == 6 and
            anchor_eval.memo.hits > 0,
            "memo six source anchors and shared-source hit")

    # Cache capacity is strictly best effort: a tiny cache evicts/falls back
    # to cold exact recomputation and must not raise ResourceStop or alter the
    # Fox result.
    fallback_eval = WordExprEvaluator(
        expr, q, {"candidate_index": 14, "fixture": "pin-fallback"},
        memo_node_cap=2, memo_sparse_cap=1)  # type: ignore[arg-type]
    fallback_eval.evaluate_values()
    fallback_eval.pin_source_roots(six_anchors)
    fallback_accounting = fallback_eval.memo.accounting()
    fallback_gradient = fallback_eval.evaluate_gradients([substituted])[
        substituted]
    fallback_cold = fallback_eval.evaluate_gradients_cold([substituted])[
        substituted]
    require(fallback_gradient == fallback_cold and
            fallback_accounting["requested_source_count"] == 6 and
            fallback_accounting["pinned_source_count"] +
                fallback_accounting["unretained_requested_source_count"] == 6 and
            fallback_accounting["pin_store_fallbacks"] +
                fallback_accounting["pin_evictions"] > 0 and
            fallback_accounting["cache_capacity_is_nonterminal"] is True,
            "memo cache-capacity cold fallback is semantics-only")

    toy_records = [{
        "candidate_index": index, "outcome": "MISSING_PIVOT",
        "outcome_code": 2, "failed_name": "toy_target",
        "failed_target_ordinal": 1, "blocker_component": 1,
        "blocker_value_hex": "00", "blocker_value_sha256": "0"*64,
        "gradient_entry_count": 1, "diagnostic_pass_count": 0,
        "diagnostic_values_sha256": "1"*64,
        "wordexpr_sha256": "2"*64, "wordexpr_nodes": 1,
        "wordexpr_edges": 0, "wordexpr_max_expanded_letters": 1,
        "pool_suffix_removed": 0,
    } for index in range(1, 4097)]
    packed = encode_scan_prefix(toy_records, 1, True)
    require(packed["evaluated"] == 4096 and packed["complete"] and
            TERMINALS == {
                "B345_RELFRAT3_WORDEXPR_PASS",
                "B345_RELFRAT3_WORDEXPR_SEARCH_INCOMPLETE",
                "B345_RELFRAT3_WORDEXPR_UNKNOWN_RESOURCE",
                "B345_RELFRAT3_WORDEXPR_UNKNOWN_INPUT"},
            "WordExpr full registered exhaustion/non-obstruction schema")
    print("D972_B345_RELFRAT3_WORDEXPR_MEMO_V9_PRODUCER_SELFTEST_PASS "
          "product=1 inverse=1 substitution=1 negative_prefix=1 "
          "long_unflattened=262144 memo_typed_key=1 equal_value_nonalias=1 "
           "memo_hit_miss_eviction_rollback_recompute=1 source_anchors=6 "
           "cache_capacity_cold_fallback=1 scan=4096 terminals=4")


###############################################################################
# 157ec: exact 108-seed raw-Fox affine lane (the frozen 104-seed prefix plus
# four preregistered positive triple-cube words).
###############################################################################

AFFINE_SCHEMA = "d972-b345-seedspan-triple4/v1"
AFFINE_TASK_SHA = "1173f2f8ce6ad899fe5bee6c2a42d7cb6686073306a7e3fd1e17acf0007f89b2"
AFFINE_STRONG_SOURCE = Path("search/d972_b345_strong_wform_inertness_v1.py")
AFFINE_STRONG_SHA = "d41123a8c4803f6ac67387ac9bbf1a32f797b90d6233605a5511713f215244be"
AFFINE_157EB_PRODUCER = Path("search/d972_b345_seedspan_affine_solver_v1.py")
AFFINE_157EB_PRODUCER_SHA = "804414e69155f2b8d9aa2a2412b0120d64eb373945a0fa6163f1214b4673e19a"
AFFINE_157EB_CHECKER = Path("search/check_d972_b345_seedspan_affine_solver_v1.py")
AFFINE_157EB_CHECKER_SHA = "67ad8d8227f1a8a60e481977fd2d07d819d532deb2651cd28667db997ec46081"
AFFINE_157EB_DRIVER = Path("search/d972_b345_seedspan_affine_solver_gha_driver_v1.g")
AFFINE_157EB_DRIVER_SHA = "1c7a6169292146ada37007d2e5b9a48f21b7f1ae545fe84a969409d8b9741057"
AFFINE_OLD_SEED_SHA = "e99602b0981251e4bb81ab0d2113791563bc9ec9df2a45828aea2880ec6d2f9e"
# Compatibility name used only by inherited bounded fixtures; the receipt
# binds the old digest and the new four-word manifest separately.
AFFINE_SEED_SHA = AFFINE_OLD_SEED_SHA
TRIPLE4_CUBES_SHA = "3d26302d01b3c202350fdb8b9ea81badeaf9c62913c9e94be7e049ad7c391463"
TRIPLE4_RECORD_TUPLES = ((3, 10, 19), (10, 10, 11),
                         (10, 12, 12), (19, 19, 21))
TRIPLE4_CUBE_TUPLES = ((2, 9, 18), (9, 9, 10),
                       (9, 11, 11), (18, 18, 20))
TRIPLE4_MANIFEST = (
    {"record_tuple": [3, 10, 19], "cube_tuple": [2, 9, 18],
     "length": 408,
     "sha256": "d810d557ca1128924da9ab04f0f304dfbf4d60503db187dfde531085b43a124f"},
    {"record_tuple": [10, 10, 11], "cube_tuple": [9, 9, 10],
     "length": 816,
     "sha256": "0fb7a48541e413091779494e54d351e745569859e1d8ed68fe24301b8ae0f3b6"},
    {"record_tuple": [10, 12, 12], "cube_tuple": [9, 11, 11],
     "length": 816,
     "sha256": "05fff82ae07daf70997f9164fbbd2a6a22d7340b277eb9203d4c890ae98bb44b"},
    {"record_tuple": [19, 19, 21], "cube_tuple": [18, 18, 20],
     "length": 408,
     "sha256": "8d68e311a631fdc8d94e9729a273aefb6ff25f5bab99c7b59e4c9488c0080e5c"},
)
AFFINE_OUTPUT_PATH = Path("ci/out/d972_b345_seedspan_triple4_v1.json")
AFFINE_TERMINALS = {
    "B345_SEEDSPAN_TRIPLE4_POSITIVE",
    "B345_SEEDSPAN_TRIPLE4_SEARCH_INCOMPLETE",
    "B345_SEEDSPAN_TRIPLE4_UNKNOWN_RESOURCE",
    "B345_SEEDSPAN_TRIPLE4_UNKNOWN_INPUT",
}
AFFINE_PREFIX_BINDINGS = {
    "formula_sha256": FORMULA_SHA,
    "stable_rounds_projection_sha256":
        "75a2894da0f19d0e541e27924ee63e220a6eca35e852b21088ee304ba42fc42d",
    "translations_sha256":
        "a4b952bce888713e293587cd63d710465121e782448a3e2a571d80b992ea363f",
    "columns_sha256":
        "cb57176146b926df16e508429db5aa1ff6b5b0ec691f2328371973681089b343",
    "blocker_history_sha256":
        "b5f100e45e874ce5ee3270cd31350b4318cf40931055571ac70066e69d62de53",
    "BFS_translations": 32768, "directed_translations": 207,
    "columns": 362725, "pivots": 362709, "dependent_columns": 16,
}
AFFINE_CAPS = {
    "seed_count": 108, "old_seed_count": 104, "new_seed_count": 4,
    "cube_count": 26,
    "bfs_translations": 32768, "directed_translations": 207,
    "prefix_columns": 362725, "prefix_pivots": 362709,
    "affine_variables": 108, "affine_rows": 1_000_000,
    "dual_support": 128, "dual_provenance_entries": 128,
    "target_live_remainders": 2_000_000,
    "producer_soft_timeout_seconds": 18000,
    "producer_soft_rss_bytes": 4_831_838_208,
}
AFFINE_RESOURCE_REASONS = frozenset({
    "producer_soft_timeout", "producer_soft_rss",
    "missing_bounded_inverse_representative", "provenance_dag_nodes",
    "provenance_dag_edges", "total_sparse_group_ring_keys",
    "sparse_pivot_rows", "single_sparse_elimination_row",
    "target_elimination_support", "element_pool", "section_slp_nodes",
    "directed_section_expr_nodes", "directed_section_expr_edges",
    "directed_unique_translations", "directed_columns",
    "wordexpr_nodes_per_candidate", "wordexpr_edges_per_candidate",
    "wordexpr_flat_leaves_per_candidate",
    "single_word_or_section_length",
    "wordexpr_expanded_letter_count_per_target",
    "candidate_live_gradient_entries_total", "candidate_element_pool_suffix",
    "candidate_scan_records", "transaction_trace_records", "blocker_table",
    "affine_rows", "target_live_remainders",
    "dual_provenance_entries",
})
AFFINE_INHERITED_CAP_KEYS = (
    "single_word_or_section_length", "provenance_dag_nodes",
    "provenance_dag_edges", "total_sparse_group_ring_keys",
    "single_sparse_elimination_row", "target_elimination_support",
    "sparse_pivot_rows", "element_pool", "section_slp_nodes",
    "directed_section_expr_nodes", "directed_section_expr_edges",
    "directed_unique_translations", "directed_columns",
    "wordexpr_nodes_per_candidate", "wordexpr_edges_per_candidate",
    "wordexpr_flat_leaves_per_candidate",
    "wordexpr_expanded_letter_count_per_target",
    "candidate_live_gradient_entries_total", "candidate_element_pool_suffix",
    "transaction_trace_records", "blocker_table",
)
AFFINE_INHERITED_CAPS = {key: CAPS[key] for key in AFFINE_INHERITED_CAP_KEYS}
AFFINE_CAPS_BINDING = {
    "affine_caps_sha256": digest_obj(AFFINE_CAPS),
    "inherited_caps": AFFINE_INHERITED_CAPS,
    "inherited_caps_sha256": digest_obj(AFFINE_INHERITED_CAPS),
    "resource_reasons": sorted(AFFINE_RESOURCE_REASONS),
}
# The frozen v9 monitor asserts the global timeout value.  The affine lane
# intentionally adopts the registered 300-minute production budget used by
# the authenticated strong-prefix successor.
CAPS["producer_soft_timeout_seconds"] = AFFINE_CAPS["producer_soft_timeout_seconds"]


def affine_terminals() -> set[str]:
    return set(AFFINE_TERMINALS)


def affine_monitor_receipt(monitor: ResourceMonitor, hit: bool) -> dict[str, Any]:
    row = monitor.receipt(hit)
    row["terminal_on_hit"] = "B345_SEEDSPAN_TRIPLE4_UNKNOWN_RESOURCE"
    row["schema"] = AFFINE_SCHEMA
    return row


def affine_seed_words(q3_data: dict[str, Any], e3: MatchedQuotient) \
        -> dict[str, Any]:
    """Rebuild the frozen 104 prefix and exactly four registered cubes.

    The four appended words are deliberately constructed from cube positions,
    not from a search result: positions are one-based, products are ordinary
    left-to-right products, and repeated positions are literal copies.
    """
    records = q3_data["correction_fibre"]["records"]
    require(len(records) == 27 and not records[0]["word"],
            "affine correction fibre manifest shape")
    cubes: list[list[int]] = []
    seen_cubes: set[tuple[int, ...]] = set()
    record_to_cube: dict[int, int] = {}
    for record_index, row in enumerate(records, 1):
        word = list(row["word"])
        if not word:
            continue
        cube = reduce_word(word + word + word)
        key = tuple(cube)
        require(key not in seen_cubes, "affine duplicate cube")
        seen_cubes.add(key)
        record_to_cube[record_index] = len(cubes)+1
        cubes.append(cube)
    require(len(cubes) == 26, "affine cube count")
    require(digest_obj(cubes) == TRIPLE4_CUBES_SHA,
            "affine cube digest/ordering")
    seeds: list[list[int]] = []
    seen: set[tuple[int, ...]] = set()
    for cube in cubes:
        require(e3.eval(embed_f2_pb3(cube)) == e3.identity,
                "affine cube E3 identity")
        for word in (commutator(cube, [1]), commutator([1], cube),
                     commutator(cube, [2]), commutator([2], cube)):
            reduced = reduce_word(word)
            require(reduced and exponent_sums(reduced, 2) == [0, 0],
                    "affine commutator typing")
            require(e3.eval(embed_f2_pb3(reduced)) == e3.identity,
                    "affine seed E3 identity")
            require(tuple(reduced) not in seen, "affine seed duplicate")
            seen.add(tuple(reduced))
            seeds.append(reduced)
    require(len(seeds) == 104 and digest_obj(seeds) == AFFINE_OLD_SEED_SHA,
            "affine seed digest/count")
    new_seeds: list[list[int]] = []
    new_provenance: list[dict[str, Any]] = []
    for manifest in TRIPLE4_MANIFEST:
        record_tuple = tuple(int(x) for x in manifest["record_tuple"])
        cube_tuple = tuple(int(x) for x in manifest["cube_tuple"])
        require(record_tuple in TRIPLE4_RECORD_TUPLES and
                cube_tuple in TRIPLE4_CUBE_TUPLES,
                "affine triple4 manifest tuple registry")
        require(tuple(record_to_cube[index] for index in record_tuple) ==
                cube_tuple, "affine triple4 record/cube binding")
        word = reduce_word(cubes[cube_tuple[0]-1] +
                           cubes[cube_tuple[1]-1] +
                           cubes[cube_tuple[2]-1])
        require(len(word) == manifest["length"] and
                digest_obj(word) == manifest["sha256"],
                "affine triple4 word manifest")
        require(exponent_sums(word, 2) == [0, 0] and
                e3.eval(embed_f2_pb3(word)) == e3.identity,
                "affine triple4 roof typing")
        require(tuple(word) not in seen, "affine triple4 seed duplicate")
        seen.add(tuple(word)); new_seeds.append(word)
        new_provenance.append({
            "family": "positive_triple_cube",
            "global_index": 104+len(new_seeds),
            "record_tuple": list(record_tuple),
            "cube_tuple": list(cube_tuple),
            "ordered_product": "cube_a * cube_b * cube_c",
            "repeated_indices_literal": len(set(cube_tuple)) != 3,
            "reduced_length": len(word),
            "reduced_sha256": digest_obj(word),
            "exponent_sums": exponent_sums(word, 2),
            "E3_identity": True,
        })
    all_seeds = seeds + new_seeds
    require(len(all_seeds) == 108 and len({tuple(x) for x in all_seeds}) == 108,
            "affine 108 seed universe")
    provenance = ([{"family": "old_commutator", "global_index": i+1,
                    "seed_index": i+1, "reduced_length": len(word),
                    "reduced_sha256": digest_obj(word),
                    "exponent_sums": exponent_sums(word, 2),
                    "E3_identity": True}
                   for i, word in enumerate(seeds)] + new_provenance)
    return {
        "cube_words": cubes, "cube_count": len(cubes),
        "old_seed_words": seeds, "old_seed_count": len(seeds),
        "new_seed_words": new_seeds, "new_seed_count": len(new_seeds),
        "seed_words": all_seeds, "seed_count": len(all_seeds),
        "old_seed_digest_sha256": digest_obj(seeds),
        "new_seed_digest_sha256": digest_obj(new_seeds),
        "digest_obj_sha256": digest_obj(all_seeds),
        "cube_digest_sha256": digest_obj(cubes),
        "triple4_manifest": [dict(row) for row in TRIPLE4_MANIFEST],
        "provenance": provenance,
        "order": "cube first occurrence; [k,x],[x,k],[k,y],[y,k]",
        "commutator": "[a,b]=a^-1*b^-1*a*b",
        "literal_threefold_cube": True,
        "four_preregistered_positive_triple_cube_words": True,
        "all_E3_identity": True, "all_exponent_sums_zero": True,
        "registered_BFS_not_constructed": True,
    }


class AffineSystem:
    """Deterministic row-echelon solver over F3 with canonical free solution."""

    def __init__(self, variables: int,
                 coordinate_widths: tuple[int, int] = (1, 0)) -> None:
        require(variables > 0, "affine variable count")
        require(len(coordinate_widths) == 2 and
                all(isinstance(width, int) and width >= 0
                    for width in coordinate_widths) and
                sum(coordinate_widths) > 0,
                "affine coordinate widths")
        self.variables = variables
        self.permutation_width_bytes = coordinate_widths[0]
        self.pc_width_bytes = coordinate_widths[1]
        self.blob_width = sum(coordinate_widths)
        self.blob_hex_length = 2*self.blob_width
        self.rows: dict[int, tuple[dict[int, int], int]] = {}
        self.equations = 0
        self.consistent = True
        self.provenance: dict[int, dict[str, int]] = {}
        self.peak_live_provenance_entries = 0
        self.dual_witness: dict[str, int] | None = None

    @staticmethod
    def _label_key(label: Any) -> str:
        return canonical_bytes(label).decode("ascii")

    def _account_provenance(self, candidate_entries: int = 0) -> None:
        live = (sum(len(item) for item in self.provenance.values()) +
                int(candidate_entries))
        self.peak_live_provenance_entries = max(
            self.peak_live_provenance_entries, live)
        require(live >= 0, "affine provenance live accounting")

    def _validate_label_encoding(self, label: Any) -> None:
        if isinstance(label, (list, tuple)) and len(label) == 4:
            require(isinstance(label[2], int) and 1 <= label[2] <= 6,
                    "affine E4 component numbering")
            blob = label[3]
            require(isinstance(blob, str) and
                    len(blob) == self.blob_hex_length and
                    all(char in "0123456789abcdefABCDEF" for char in blob),
                    "affine E4 label hex width")
            try:
                decoded = bytes.fromhex(blob)
            except ValueError:
                require(False, "affine E4 label hex decode")
            require(len(decoded) == self.blob_width,
                    "affine E4 label decoded width")

    def add(self, coefficients: dict[int, int], rhs: int,
            label: Any = None) -> bool:
        row = {int(k): int(v) % 3 for k, v in coefficients.items()
               if int(v) % 3}
        require(all(0 <= k < self.variables for k in row),
                "affine coordinate range")
        value = int(rhs) % 3
        self.equations += 1
        if self.equations > AFFINE_CAPS["affine_rows"]:
            raise ResourceStop("affine_rows", cap_key="affine_rows",
                               cap_limit=AFFINE_CAPS["affine_rows"],
                               observed_count=self.equations,
                               trigger_relation="gt")
        if label is None:
            label = ["synthetic", self.equations]
        self._validate_label_encoding(label)
        provenance = {self._label_key(label): 1}
        while row:
            self._account_provenance(len(provenance))
            require(len(provenance) <= len(self.rows)+1,
                    "affine provenance rank invariant")
            pivot = min(row)
            old = self.rows.get(pivot)
            if old is None:
                factor = 1 if row[pivot] == 1 else 2
                row = {k: (factor*v) % 3 for k, v in row.items()
                       if (factor*v) % 3}
                value = (factor*value) % 3
                self.rows[pivot] = (row, value)
                self.provenance[pivot] = {
                    key: (factor*term) % 3
                    for key, term in provenance.items()
                    if (factor*term) % 3}
                self.peak_live_provenance_entries = max(
                    self.peak_live_provenance_entries,
                    sum(len(item) for item in self.provenance.values()))
                require(len(self.provenance[pivot]) <= len(self.rows),
                        "affine pivot provenance rank invariant")
                return True
            coefficient = row[pivot]
            basis, basis_rhs = old
            for key, term in basis.items():
                result = (row.get(key, 0) - coefficient*term) % 3
                if result:
                    row[key] = result
                else:
                    row.pop(key, None)
            value = (value - coefficient*basis_rhs) % 3
            old_provenance = self.provenance[pivot]
            for key, term in old_provenance.items():
                result = (provenance.get(key, 0)-coefficient*term) % 3
                if result:
                    provenance[key] = result
                else:
                    provenance.pop(key, None)
        if value:
            self._account_provenance(len(provenance))
            self.consistent = False
            factor = 1 if value == 1 else 2
            witness = {key: (factor*term) % 3
                       for key, term in provenance.items()
                       if (factor*term) % 3}
            require(witness, "affine nonempty dual witness")
            if len(witness) > AFFINE_CAPS["dual_support"]:
                raise ResourceStop(
                    "dual_provenance_entries",
                    cap_key="dual_provenance_entries",
                    cap_limit=AFFINE_CAPS["dual_provenance_entries"],
                    observed_count=len(witness), trigger_relation="gt")
            if self.dual_witness is None:
                self.dual_witness = witness
            return False
        return True

    def rank(self) -> int:
        return len(self.rows)

    def nullity(self) -> int:
        return self.variables-self.rank()

    def digest(self) -> str:
        return digest_obj({"variables": self.variables,
                           "rows": [[p, sorted(r.items()), rhs]
                                    for p, (r, rhs) in sorted(self.rows.items())],
                           "equations": self.equations,
                           "consistent": self.consistent})

    def dual_public(self) -> dict[str, Any] | None:
        if self.dual_witness is None:
            return None
        equations = [{"label": json.loads(key), "coefficient": coefficient}
                     for key, coefficient in sorted(self.dual_witness.items())]
        target_ordinals = sorted({int(row["label"][0]) for row in equations
                                  if isinstance(row["label"], list) and
                                  row["label"] and
                                  isinstance(row["label"][0], int)})
        return {
            "normalization": "first contradiction multiplied by inverse RHS",
            "equations": equations,
            "support_count": len(equations),
            "support_sha256": digest_obj(equations),
            "normalized_rhs": 1, "yTz_mod3": 2,
            "all_108_annihilation_sha256": digest_obj([0] * self.variables),
            "all_108_annihilation_dimension": self.variables,
            "live_provenance_entries": sum(
                len(item) for item in self.provenance.values()),
            "witness_provenance_entries": len(self.dual_witness),
            "peak_live_provenance_entries":
                self.peak_live_provenance_entries,
            "target_boundary": {
                "first_target_ordinal": target_ordinals[0]
                if target_ordinals else None,
                "last_target_ordinal": target_ordinals[-1]
                if target_ordinals else None,
                "target_ordinals": target_ordinals,
            },
            "target6_fixed_prefix_functional": target_ordinals == [6],
            "coordinate_encoding": {
                "label": "[target_ordinal,target_name,component,E4_blob_hex]",
                "component_numbering": "one_based_1_through_6",
                "E4_blob": "canonical permutation bytes then PC bytes",
                "permutation_width_bytes": self.permutation_width_bytes,
                "pc_width_bytes": self.pc_width_bytes,
                "blob_width": self.blob_width,
                "blob_hex_length": self.blob_hex_length,
                "endianness": "byte-string order; no integer reinterpretation",
                "pivot_order": "component then exact E4 bytes",
            },
            "seed_manifest_sha256": digest_obj(TRIPLE4_MANIFEST),
            "variables": self.variables,
        }

    def canonical_solution(self) -> list[int]:
        require(self.consistent, "solution of inconsistent affine system")
        answer = [0]*self.variables
        for pivot in sorted(self.rows, reverse=True):
            row, rhs = self.rows[pivot]
            answer[pivot] = (rhs-sum(coef*answer[key]
                                     for key, coef in row.items()
                                     if key != pivot)) % 3
        return answer


def affine_basis_gate(basis: SparseBoundaryBasis, pool: ElementPool) -> dict[str, Any]:
    """Gate the strengthened immutable echelon contract before any probe."""
    pivots: list[int] = []
    for pivot, (row, _) in basis.rows.items():
        require(row and pivot == min(row, key=pool.pivot_order),
                "affine basis least canonical pivot")
        require(row.get(pivot) == 1, "affine basis normalized pivot")
        require(all(pool.pivot_order(key) >= pool.pivot_order(pivot)
                    for key in row), "affine basis no preceding key")
        pivots.append(pivot)
    require(len(pivots) == len(set(pivots)), "affine basis unique pivots")
    return {"rows": len(basis.rows), "pivots": len(pivots),
            "least_pivot_coeff_one": True, "no_preceding_keys": True,
            "immutable_during_affine_probes": True,
            "pivot_order": "component then exact E4 bytes"}


def affine_full_remainder(vector: PackedSparseVector,
                          basis: SparseBoundaryBasis,
                          pool: ElementPool,
                          monitor: ResourceMonitor | None = None
                          ) -> PackedSparseVector:
    """Project all the way through later pivots; never stop at first free key."""
    work = dict(vector)
    remainder: PackedSparseVector = {}
    eliminations = 0
    while work:
        eliminations += 1
        if len(work)+len(remainder) > CAPS["target_elimination_support"]:
            raise ResourceStop(
                "target_elimination_support",
                cap_key="target_elimination_support",
                cap_limit=CAPS["target_elimination_support"],
                observed_count=len(work)+len(remainder),
                trigger_relation="gt")
        if monitor is not None and eliminations % 1024 == 0:
            monitor.check("affine_full_remainder")
        pivot = min(work, key=pool.pivot_order)
        coefficient = work[pivot]
        row_data = basis.rows.get(pivot)
        if row_data is None:
            work.pop(pivot)
            remainder[pivot] = coefficient
            continue
        add_scaled(work, row_data[0], -coefficient)
    return {key: value for key, value in remainder.items() if value % 3}


def affine_public_remainder(remainder: PackedSparseVector,
                            pool: ElementPool) -> dict[tuple[int, str], int]:
    return {(unpack_vector_key(key)[0],
             pool.blob(unpack_vector_key(key)[1]).hex()): coefficient
            for key, coefficient in sorted(remainder.items(),
                                           key=lambda item: pool.pivot_order(item[0]))}


def _affine_load_strong_builder(repo: Path) -> Any:
    path = repo/AFFINE_STRONG_SOURCE
    if not path.is_file():
        raise AffineInput("missing authenticated strong-prefix source")
    if digest_file(path) != AFFINE_STRONG_SHA:
        raise AffineInput("pinned strong-prefix source SHA drift")
    spec = importlib.util.spec_from_file_location(
        "_d972_b345_seedspan_strong_prefix", path)
    require(spec is not None and spec.loader is not None,
            "strong-prefix import spec")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def affine_target6_formula(seed: Sequence[int], e4: MatchedQuotient,
                           *, include_gradient: bool = False) \
        -> dict[str, Any]:
    """Replay C*(c-b)*C^-1+h1*a*h1^-1 in the raw Fox module."""
    mapping = cofaces(3)[0]
    z = inv_word(pp_words([[1], [2]]))
    a = f2_substitute(seed, [1], [2])
    b = f2_substitute(seed, [1], z)
    c = f2_substitute(seed, [2], z)
    lift = lambda w: word_substitute(embed_f2_pb3(w), mapping)
    a4, b4, c4 = lift(a), lift(b), lift(c)
    r0 = lift(hexagon_words(FIXED_WORD)[0])
    rs = lift(hexagon_words(reduce_word(FIXED_WORD+list(seed)))[0])
    delta = reduce_word(rs+inv_word(r0))
    direct, direct_value = fox_gradient_without_sections(delta, e4)
    ga, va = fox_gradient_without_sections(a4, e4)
    gb, vb = fox_gradient_without_sections(b4, e4)
    gc, vc = fox_gradient_without_sections(c4, e4)
    h_value = e4.eval(r0)
    # C is the fixed f0(y,z) factor in h1(f0*s), not the correction leaf c.
    fixed_c4 = lift(f2_substitute(FIXED_WORD, [2], z))
    c_value = e4.eval(fixed_c4)
    lhs_word = reduce_word(rs + inv_word(r0))
    rhs_word = reduce_word(
        fixed_c4 + c4 + inv_word(b4) + inv_word(fixed_c4) +
        r0 + a4 + inv_word(r0))
    require(lhs_word == rhs_word,
            "target6 free-word difference identity")
    require(direct_value == e4.identity and va == vb == vc == e4.identity and
            h_value == e4.identity and e4.eval(rs) == e4.identity,
            "target6 raw formula quotient identities")
    formula: SparseVector = {}
    add_scaled(formula, translate_vector(gc, c_value, e4), 1)
    add_scaled(formula, translate_vector(gb, c_value, e4), -1)
    add_scaled(formula, translate_vector(ga, h_value, e4), 1)
    require(formula == direct, "target6 raw left-Fox formula")
    result = {"seed_word_sha256": digest_obj(seed),
            "left_translation": True,
            "formula": "L_C([c]-[b])+L_h1[a]",
            "product_order": "h1=C*B^-1*A",
            "free_word_identity": True,
            "free_word_lhs_sha256": digest_obj(lhs_word),
            "free_word_rhs_sha256": digest_obj(rhs_word),
            "direct_gradient_sha256": digest_obj(raw_gradient_binding(
                "target6", "hexagon", direct, direct_value)),
            "formula_equals_direct": True}
    if include_gradient:
        result["_direct_gradient"] = direct
        result["_direct_value"] = direct_value
    return result


def affine_strong_canary(e4: MatchedQuotient) -> dict[str, Any]:
    strong = reduce_word([-2]*18+[-1]*18+[2]*18+[1]*18)
    rows = []
    for slot, mapping in enumerate(cofaces(3)):
        # d_j(s) itself, not the residual hexagon constructor, is the
        # five-coface 157ea raw-Fox zero canary.  The target-6 residual
        # comparison below is a separate orientation/action gate.
        word = word_substitute(embed_f2_pb3(strong), mapping)
        gradient, value = fox_gradient_without_sections(word, e4)
        require(value == e4.identity and not gradient,
                "strong raw-Fox zero coface")
        rows.append({"slot": slot, "gradient_zero": True,
                     "value_identity": True,
                     "word_sha256": digest_obj(word)})
    target6 = affine_target6_formula(strong, e4)
    require(target6["formula_equals_direct"] is True and
            target6["direct_gradient_sha256"] == digest_obj(
                raw_gradient_binding("target6", "hexagon", {}, e4.identity)),
            "strong target6 raw-Fox zero canary")
    return {"word": strong, "cofaces": rows, "target6": target6,
            "raw_Fox_zero": True, "replayed_not_imported": True}


def affine_raw_affine_canary(e4: MatchedQuotient) -> dict[str, bool]:
    """Direct raw-C1 pair/inverse/square canary for identity-valued seeds."""
    base_word, first, second = [1], [2], [3]
    base, base_value = fox_gradient_without_sections(base_word, e4)
    first_direct, first_value = fox_gradient_without_sections(
        reduce_word(base_word+first), e4)
    second_direct, second_value = fox_gradient_without_sections(
        reduce_word(base_word+second), e4)
    require(base_value == first_value == second_value == e4.identity,
            "raw affine canary quotient values")
    first_delta = dict(first_direct); add_scaled(first_delta, base, -1)
    second_delta = dict(second_direct); add_scaled(second_delta, base, -1)
    pair_direct, pair_value = fox_gradient_without_sections(
        reduce_word(base_word+first+second), e4)
    pair_prediction = dict(base)
    add_scaled(pair_prediction, first_delta, 1)
    add_scaled(pair_prediction, second_delta, 1)
    inverse_direct, inverse_value = fox_gradient_without_sections(
        reduce_word(base_word+inv_word(first)), e4)
    inverse_prediction = dict(base)
    add_scaled(inverse_prediction, first_delta, -1)
    square_direct, square_value = fox_gradient_without_sections(
        reduce_word(base_word+first+first), e4)
    square_prediction = dict(base)
    add_scaled(square_prediction, first_delta, 2)
    require(pair_value == inverse_value == square_value == e4.identity and
            pair_direct == pair_prediction and
            inverse_direct == inverse_prediction and
            square_direct == square_prediction,
            "raw affine pair/inverse/square canary")
    return {"pair": True, "inverse": True, "square": True,
            "nonzero_base": bool(base), "base_delta_split": True}


def _affine_candidate_values(compiled: dict[str, Any],
                             e4: MatchedQuotient,
                             candidate_index: int,
                             static_binding: MemoStaticQuotientBinding | None = None,
                             pin_sources: bool = False,
                             value_roots: Sequence[int] | None = None) \
        -> WordExprEvaluator:
    evaluator = WordExprEvaluator(
        compiled["dag"], e4,
        {"candidate_index": candidate_index, "fixture": "seedspan-triple4"},
        memo_static_binding=static_binding)
    evaluator.evaluate_values(value_roots)
    if pin_sources:
        evaluator.pin_source_roots(compiled["source_roots"])
    return evaluator


def _affine_direct_gradient(compiled: dict[str, Any], evaluator: WordExprEvaluator,
                            root: int, e4: MatchedQuotient) \
        -> tuple[SparseVector, EKey]:
    gradient = evaluator.evaluate_gradients([root])[root]
    value = evaluator.values[root-1]
    if compiled["dag"].expanded_count[root-1] <= CAPS["single_word_or_section_length"]:
        word = compiled["dag"].expand_reduced_below_flat_cap(root)
        direct, direct_value = fox_gradient_without_sections(word, e4)
        require(direct == gradient and direct_value == value,
                "typed/raw Fox gradient equality")
    else:
        cold = evaluator.evaluate_gradients_cold([root])[root]
        require(cold == gradient, "typed cold/raw Fox gradient equality")
    return gradient, value


def _affine_probe_remainder(raw: SparseVector, prefix: dict[str, Any],
                            anchors: Sequence[int], monitor: ResourceMonitor) \
        -> dict[tuple[int, str], int]:
    pool = prefix["pool"]
    basis = prefix["basis"]
    snapshot = candidate_transaction_snapshot(pool, prefix["dag"], basis,
                                              prefix["sections"], anchors)
    try:
        packed = intern_raw_vector(raw, pool)
        remainder = affine_full_remainder(packed, basis, pool, monitor)
        public = affine_public_remainder(remainder, pool)
        monitor.check("affine_remainder")
        rollback_candidate_transaction(snapshot, pool, prefix["dag"], basis,
                                       prefix["sections"])
        return public
    except Exception:
        rollback_candidate_transaction(snapshot, pool, prefix["dag"], basis,
                                      prefix["sections"])
        raise


def _affine_delta_matrix_rank(delta_rows: dict[Any, dict[int, int]],
                              variables: int | None = None) -> int:
    """Rank of the current target's registered 108-column delta map."""
    if variables is None:
        variables = AFFINE_CAPS["affine_variables"]
    pivots: dict[int, dict[int, int]] = {}
    for coordinate in sorted(delta_rows, key=repr):
        row = {int(index): int(value) % 3
               for index, value in delta_rows[coordinate].items()
               if int(value) % 3}
        require(all(0 <= index < variables for index in row),
                "affine delta coordinate range")
        while row:
            pivot = min(row); old = pivots.get(pivot)
            if old is None:
                factor = 1 if row[pivot] == 1 else 2
                pivots[pivot] = {key: (factor*value) % 3
                                 for key, value in row.items()
                                 if (factor*value) % 3}
                break
            coefficient = row[pivot]
            for key, term in old.items():
                result = (row.get(key, 0)-coefficient*term) % 3
                if result:
                    row[key] = result
                else:
                    row.pop(key, None)
    return len(pivots)


def _affine_equation_label(target_ordinal: int, target_name: str,
                           coordinate: tuple[int, str]) -> list[Any]:
    """Canonical public coordinate label used by the dual certificate."""
    component, e4_blob_hex = coordinate
    require(isinstance(component, int) and isinstance(e4_blob_hex, str),
            "affine dual coordinate encoding")
    return [int(target_ordinal), str(target_name), int(component), e4_blob_hex]


def _affine_target_row(system: AffineSystem, base_remainder: dict[tuple[int, str], int],
                       deltas: Sequence[dict[tuple[int, str], int]],
                       target_ordinal: int, target_name: str = "synthetic") -> dict[str, Any]:
    live_remainder_entries = len(base_remainder) + sum(len(row) for row in deltas)
    if live_remainder_entries > AFFINE_CAPS["target_live_remainders"]:
        raise ResourceStop(
            "target_live_remainders", cap_key="target_live_remainders",
            cap_limit=AFFINE_CAPS["target_live_remainders"],
            observed_count=live_remainder_entries, trigger_relation="gt")
    coordinates = sorted(set(base_remainder).union(*(set(row) for row in deltas)))
    if system.equations + len(coordinates) > AFFINE_CAPS["affine_rows"]:
        raise ResourceStop(
            "affine_rows", cap_key="affine_rows",
            cap_limit=AFFINE_CAPS["affine_rows"],
            observed_count=system.equations + len(coordinates),
            trigger_relation="gt")
    delta_rows = {}
    for index, row in enumerate(deltas):
        for coordinate, coefficient in row.items():
            delta_rows.setdefault(coordinate, {})[index] = coefficient
    before = system.rank()
    for coordinate in coordinates:
        coefficients = {index: row.get(coordinate, 0)
                        for index, row in enumerate(deltas)
                        if row.get(coordinate, 0)}
        rhs = (-base_remainder.get(coordinate, 0)) % 3
        system.add(coefficients, rhs,
                   _affine_equation_label(target_ordinal, target_name,
                                          coordinate))
    return {"ordinal": target_ordinal, "base_remainder_size": len(base_remainder),
            "base_remainder_sha256": digest_obj(sorted(base_remainder.items())),
            "coordinate_count": len(coordinates),
            "delta_rank": _affine_delta_matrix_rank(delta_rows),
            "constraint_rank_gain": system.rank()-before,
            "constraint_rank": system.rank(), "nullity": system.nullity(),
            "consistent": system.consistent, "row_space_sha256": system.digest(),
            "dual_witness": system.dual_public(),
            "live_remainder_entries": live_remainder_entries,
            "affine_equations": system.equations}


def _affine_target_row_transposed(
        system: AffineSystem, base_remainder: dict[tuple[int, str], int],
        delta_rows: dict[tuple[int, str], dict[int, int]],
        target_ordinal: int, live_remainder_entries: int,
        monitor: ResourceMonitor | None = None,
        target_name: str = "synthetic") -> dict[str, Any]:
    """Absorb coordinate rows while retaining no seed-major remainder list."""
    if live_remainder_entries > AFFINE_CAPS["target_live_remainders"]:
        raise ResourceStop(
            "target_live_remainders", cap_key="target_live_remainders",
            cap_limit=AFFINE_CAPS["target_live_remainders"],
            observed_count=live_remainder_entries, trigger_relation="gt")
    coordinates = sorted(set(base_remainder).union(delta_rows))
    if system.equations + len(coordinates) > AFFINE_CAPS["affine_rows"]:
        raise ResourceStop(
            "affine_rows", cap_key="affine_rows",
            cap_limit=AFFINE_CAPS["affine_rows"],
            observed_count=system.equations + len(coordinates),
            trigger_relation="gt")
    before = system.rank()
    snapshot_rows = copy.deepcopy(system.rows)
    snapshot_provenance = copy.deepcopy(system.provenance)
    snapshot_dual = copy.deepcopy(system.dual_witness)
    snapshot_peak_live = system.peak_live_provenance_entries
    snapshot_equations = system.equations
    snapshot_consistent = system.consistent
    try:
        for row_index, coordinate in enumerate(coordinates, 1):
            if monitor is not None and row_index % 1024 == 0:
                monitor.check("affine_transposed_row_absorption")
            coefficients = {index: value for index, value in
                            delta_rows.get(coordinate, {}).items()
                            if value % 3}
            system.add(coefficients, -base_remainder.get(coordinate, 0),
                      _affine_equation_label(target_ordinal, target_name,
                                             coordinate))
    except ResourceStop:
        system.rows = snapshot_rows
        system.provenance = snapshot_provenance
        system.dual_witness = snapshot_dual
        system.peak_live_provenance_entries = snapshot_peak_live
        system.equations = snapshot_equations
        system.consistent = snapshot_consistent
        raise
    return {"ordinal": target_ordinal,
            "base_remainder_size": len(base_remainder),
            "base_remainder_sha256": digest_obj(sorted(base_remainder.items())),
            "coordinate_count": len(coordinates),
            "delta_rank": _affine_delta_matrix_rank(delta_rows),
            "constraint_rank_gain": system.rank()-before,
            "constraint_rank": system.rank(), "nullity": system.nullity(),
            "consistent": system.consistent,
            "row_space_sha256": system.digest(),
            "dual_witness": system.dual_public(),
            "live_remainder_entries": live_remainder_entries,
            "affine_equations": system.equations}


def _affine_source_preflight(seeds: Sequence[Sequence[int]], e4: MatchedQuotient,
                             frozen: tuple[EKey, ...],
                             inverse_words: Sequence[Sequence[int]],
                             monitor: ResourceMonitor,
                             progress: Any = None) -> dict[str, Any]:
    """Gate all six source images and the complete 46-use context registry.

    This is intentionally value-only.  Gradient memo construction belongs to
    the target-major pass; the occurrence gate is a finite quotient test.
    """
    records = []
    contexts, _, context_public = cheap_context_registry(e4)
    require(len(contexts) == 31 and len(contexts) <= CAPS["cheap_contexts"] and
            context_public["named_use_count"] == 46,
            "affine 46-use context registry")
    for index, seed in enumerate(seeds, 1):
        if progress is not None:
            progress(index)
        candidate = reduce_word(FIXED_WORD+list(seed))
        source_values = tuple(e4.eval(word) for word in source_words_m0(candidate))
        if source_values != frozen:
            return {"supported": False, "reason": "affine_seed_preflight_unsupported",
                    "first_seed": index, "context": "source_tuple",
                    "value_sha256": digest_obj([_element_blob(x).hex()
                                                 for x in source_values]),
                    "records": records}
        context_rows = []
        for context_id, context in enumerate(contexts, 1):
            value = e4.eval(seed, list(context))
            if value != e4.identity:
                return {"supported": False,
                        "reason": "affine_seed_preflight_unsupported",
                        "first_seed": index, "context_id": context_id,
                        "value_sha256": hashlib.sha256(_element_blob(value)).hexdigest(),
                        "records": records}
            context_rows.append(context_id)
        records.append({"seed_index": index, "source_tuple_equal": True,
                        "correction_context_count": len(context_rows),
                        "correction_contexts_sha256": digest_obj(context_rows),
                        "named_use_count": context_public["named_use_count"],
                        "context_registry_unique_count": len(contexts),
                        "context_registry_sha256": digest_obj(context_public)})
        if index % 8 == 0:
            monitor.check("affine_source_preflight")
    require(len(records) == AFFINE_CAPS["seed_count"],
            "affine source preflight count")
    return {"supported": True, "seed_count": AFFINE_CAPS["seed_count"],
            "contexts_per_seed": len(contexts),
            "unique_context_count": len(contexts),
            "context_registry_sha256": digest_obj(context_public),
            "named_use_count": context_public["named_use_count"],
            "context_registry": context_public, "records": records,
            "source_contexts": ["source_1", "source_2", "source_3",
                                "source_4", "source_5", "source_6"],
            "all_source_tuples_equal": True,
            "all_correction_occurrences_identity": True}


def _affine_make_typed_positive(corresponding: list[int],
                                seeds: Sequence[Sequence[int]],
                                inverse_words: Sequence[Sequence[int]]) \
        -> dict[str, Any]:
    """Build correction/candidate as a typed PRODUCT DAG (not a flat word)."""
    dag = WordExprDAG()
    # Keep f0 and each seed in the F2 language.  They are substituted into
    # PB3/PB4 typed contexts only at replay time (y is PB3 generator 3).
    f0_root = dag.flat(FIXED_WORD, 2)
    factors = []
    for index, coefficient in enumerate(corresponding):
        if coefficient:
            seed_root = dag.flat(seeds[index], 2)
            factors.extend([seed_root]*coefficient)
    correction_root = dag.identity(2) if not factors else dag.product_many(factors)
    candidate_root = dag.product(f0_root, correction_root)
    correction_count = dag.expanded_count[correction_root-1]
    correction_word: list[int] | None = None
    if correction_count <= CAPS["single_word_or_section_length"]:
        correction_word = dag.expand_reduced_below_flat_cap(correction_root)
    # The root is deliberately retained as an immutable typed expression.  The
    # full corrected Def2.9 constructor is regenerated from its substitutions
    # by the positive replay path; no long flat candidate is used here.
    return {"dag": dag, "f0_root": f0_root, "correction_root": correction_root,
            "candidate_root": candidate_root,
            "coefficient_vector": list(corresponding),
            "nonzero_support": [i+1 for i, x in enumerate(corresponding) if x],
            "expanded_count": dag.expanded_count[candidate_root-1],
            "correction_word": correction_word,
            "correction_word_flattened": correction_word is not None,
            "correction_expanded_count": correction_count,
            "typed_product_order": "seed_1^a1 * ... * seed_108^a108",
            "exponent_two_is_two_copies": True}


def _affine_build_typed_targets(typed: dict[str, Any],
                                inverse_words: Sequence[Sequence[int]]) \
        -> dict[str, Any]:
    """Instantiate the corrected Def2.9 trees from a rank-2 candidate.

    This is intentionally a separate constructor from
    ``build_wordexpr_candidate``.  The latter is the one-seed flat lane and
    has a literal-word cap; the positive lane substitutes the rank-2
    correction PRODUCT into each PB4 occurrence and never materializes the
    potentially long candidate word.
    """
    require(len(inverse_words) == 6, "typed positive inverse tuple")
    dag: WordExprDAG = typed["dag"]
    candidate_root = int(typed["candidate_root"])
    correction_root = int(typed["correction_root"])
    require(dag.rank[candidate_root-1] == 2 and
            dag.rank[correction_root-1] == 2,
            "typed positive rank-2 roots")
    one = dag.identity(6)
    generators = [dag.flat([i], 6) for i in range(1, 7)]

    def f_at(left: int, right: int) -> int:
        return dag.substitute_expr(candidate_root, [left, right])

    def c_at(left: int, right: int) -> int:
        return dag.substitute_expr(correction_root, [left, right])

    correction_cofaces: list[tuple[str, int]] = []
    hex1_rows: list[tuple[str, str, int]] = []
    hex2_rows: list[tuple[str, str, int]] = []
    for slot, mapping in enumerate(cofaces(3)):
        x = dag.flat(mapping[0], 6)
        y = dag.flat(mapping[2], 6)
        correction_cofaces.append(
            (f"correction_coarse_J_H_coface_{slot}", c_at(x, y)))
        z = dag.inverse(dag.paper_product([x, y]))
        u = dag.inverse(dag.paper_product([y, x]))
        fxy, fxz, fyz = f_at(x, y), f_at(x, z), f_at(y, z)
        fux, fuy = f_at(u, x), f_at(u, y)
        h1 = dag.paper_product([fxy, dag.inverse(fxz), fyz])
        h2 = dag.paper_product([dag.inverse(fux), dag.inverse(fxy), fuy])
        hex1_rows.append((f"hexagon_1_coface_{slot}", "hexagon", h1))
        hex2_rows.append((f"hexagon_2_coface_{slot}", "hexagon", h2))
    acceptance: list[tuple[str, str, int]] = [
        (f"charming_error_coface_{slot}", "charming", one)
        for slot in range(5)] + hex1_rows + hex2_rows

    pent_contexts = [
        (generators[0], generators[3]),
        (generators[3], generators[5]),
        (dag.paper_product([generators[1], generators[3]]), generators[5]),
        (dag.paper_product([generators[0], generators[1]]),
         dag.paper_product([generators[4], generators[5]])),
        (generators[0], dag.paper_product([generators[3], generators[4]])),
    ]
    pent_parts = [f_at(left, right) for left, right in pent_contexts]
    pent = dag.paper_product([
        dag.inverse(dag.paper_product([pent_parts[4], pent_parts[2]])),
        pent_parts[1], pent_parts[3], pent_parts[0]])
    acceptance.append(("ordered_A18_pentagon", "pentagon", pent))

    ff = f_at(generators[0], generators[3])
    gv = f_at(generators[0], generators[1])
    gs = f_at(generators[3], generators[4])
    f1234 = f_at(dag.product_many([generators[3], generators[1]]),
                  generators[5])
    h = f_at(dag.product_many([generators[1], generators[0]]), generators[2])
    middle = f_at(dag.product_many([generators[1], generators[0]]),
                  dag.product_many([generators[5], generators[4]]))
    source = [
        generators[0],
        dag.product_many([dag.inverse(gv), generators[1], gv]),
        dag.product_many([dag.inverse(ff), dag.inverse(h), generators[2], h, ff]),
        dag.product_many([dag.inverse(ff), generators[3], ff]),
        dag.product_many([dag.inverse(ff), dag.inverse(middle),
                          dag.inverse(gs), generators[4], gs, middle, ff]),
        dag.product_many([dag.inverse(f1234), generators[5], f1234]),
    ]
    relations = pure_relations(4)
    for index, relator in enumerate(relations, 1):
        acceptance.append((f"S_relation_{index}", "endomorphism_relation",
                           dag.substitute(relator, source)))

    inverse_roots = [dag.flat(word, 6) for word in inverse_words]
    diagnostics: list[tuple[str, str, int]] = []
    for index, relator in enumerate(relations, 1):
        diagnostics.append((f"T_relation_{index}", "endomorphism_relation",
                            dag.substitute(relator, inverse_roots)))
    for index, inverse_word in enumerate(inverse_words, 1):
        acceptance.append((f"ST_generator_{index}", "onto_two_sided_inverse",
                           dag.product(dag.substitute(inverse_word, source),
                                       dag.inverse(generators[index-1]))))
    for index, source_root in enumerate(source, 1):
        diagnostics.append((f"TS_generator_{index}", "onto_two_sided_inverse",
                            dag.product(dag.substitute_expr(source_root,
                                                             inverse_roots),
                                        dag.inverse(generators[index-1]))))
    expected_acceptance = (
        [f"charming_error_coface_{i}" for i in range(5)] +
        [f"hexagon_{j}_coface_{i}" for j in (1, 2) for i in range(5)] +
        ["ordered_A18_pentagon"] +
        [f"S_relation_{i}" for i in range(1, 12)] +
        [f"ST_generator_{i}" for i in range(1, 7)])
    expected_diagnostics = ([f"T_relation_{i}" for i in range(1, 12)] +
                            [f"TS_generator_{i}" for i in range(1, 7)])
    require([x[0] for x in acceptance] == expected_acceptance and
            [x[0] for x in diagnostics] == expected_diagnostics and
            len(acceptance) == 33 and len(diagnostics) == 17,
            "typed positive corrected Def2.9 order")
    roots = [root for _, _, root in acceptance+diagnostics] + source + \
            [root for _, root in correction_cofaces]
    return {"dag": dag, "source_roots": source,
            "inverse_roots": inverse_roots,
            "correction_coface_roots": correction_cofaces,
            "acceptance": acceptance, "diagnostics": diagnostics,
            "roots": roots,
            "candidate_root": candidate_root,
            "correction_root": correction_root,
            "typed_dag_accounting": dag.accounting(roots)}


def _affine_build_typed_target6(typed: dict[str, Any]) -> dict[str, Any]:
    """Build only the target-6 typed root for the hot affine path."""
    dag: WordExprDAG = typed["dag"]
    candidate_root = int(typed["candidate_root"])
    mapping = cofaces(3)[0]
    x, y = dag.flat(mapping[0], 6), dag.flat(mapping[2], 6)
    z = dag.inverse(dag.paper_product([x, y]))
    fxy = dag.substitute_expr(candidate_root, [x, y])
    fxz = dag.substitute_expr(candidate_root, [x, z])
    fyz = dag.substitute_expr(candidate_root, [y, z])
    target = dag.paper_product([fxy, dag.inverse(fxz), fyz])
    return {"dag": dag,
            "acceptance": [("hexagon_1_coface_0", "hexagon", target)],
            "diagnostics": [], "source_roots": [],
            "inverse_roots": [], "correction_coface_roots": [],
            "roots": [target]}


def _affine_select_typed_target_root(targets: dict[str, Any],
                                     ordinal: int) -> int:
    acceptance = targets["acceptance"]
    if ordinal == 6:
        require(len(acceptance) == 1,
                "target6 typed acceptance cardinality")
        name, kind, root = acceptance[0]
        require(name == "hexagon_1_coface_0" and kind == "hexagon",
                "target6 typed acceptance binding")
        return root
    return acceptance[ordinal-1][2]


def _affine_typed_candidate_public(typed: dict[str, Any]) -> dict[str, Any]:
    dag: WordExprDAG = typed["dag"]
    roots = [("f0_root", int(typed["f0_root"])),
             ("correction_root", int(typed["correction_root"])),
             ("candidate_root", int(typed["candidate_root"]))]
    public = {key: value for key, value in typed.items()
              if key not in {"dag", "correction_word"}}
    public["correction_word"] = (None if typed["correction_word"] is None
                                  else list(typed["correction_word"]))
    public["correction_word_sha256"] = digest_obj(
        typed["correction_word"] if typed["correction_word"] is not None
        else {"typed_product_order": typed["typed_product_order"],
              "coefficient_vector": typed["coefficient_vector"]})
    public["coefficient_vector_sha256"] = digest_obj(
        typed["coefficient_vector"])
    public["expression"] = dag.serialize_reachable(roots)
    public["expression_root_names"] = [name for name, _ in roots]
    return public


def _affine_positive_replay(typed: dict[str, Any],
                            seeds: Sequence[Sequence[int]],
                            inverse_words: Sequence[Sequence[int]],
                            frozen: tuple[EKey, ...],
                            e3: MatchedQuotient, e4: MatchedQuotient,
                            prefix: dict[str, Any],
                            static_binding: MemoStaticQuotientBinding,
                            monitor: ResourceMonitor,
                            progress: Any = None) -> dict[str, Any]:
    """Directly replay the canonical solution and serialize all 33 proofs."""
    targets = _affine_build_typed_targets(typed, inverse_words)
    evaluator = _affine_candidate_values(
        targets, e4, 0, static_binding, pin_sources=True)
    dag: WordExprDAG = targets["dag"]
    correction_values = []
    for name, root in targets["correction_coface_roots"]:
        value = evaluator.values[root-1]
        require(value == e4.identity, f"typed positive correction gate {name}")
        correction_values.append({"name": name, "quotient_identity": True,
                                 "root": root})
    source_values = tuple(evaluator.values[root-1]
                          for root in targets["source_roots"])
    require(source_values == frozen, "typed positive source tuple")
    correction_word = typed["correction_word"]
    if correction_word is not None:
        require(affine_literal_selected_replay(
                    typed["coefficient_vector"], seeds) == correction_word,
                "typed positive literal selected replay")
        correction_e3 = e3.eval(embed_f2_pb3(correction_word))
    else:
        # Do not flatten a long product merely to test the roof.  The
        # authenticated seed preflight supplies E3=1 for every factor, and
        # this recurrence is the typed rank-2 product evaluation in E3.
        correction_e3 = e3.identity
        for index, seed in enumerate(seeds):
            seed_e3 = e3.eval(embed_f2_pb3(seed))
            require(seed_e3 == e3.identity,
                    f"typed positive seed roof {index+1}")
            for _ in range(int(typed["coefficient_vector"][index]) % 3):
                correction_e3 = e3.mul(correction_e3, seed_e3)
    require(correction_e3 == e3.identity and
            exponent_sums(FIXED_WORD, 2) == [0, 0] and
            all(exponent_sums(seed, 2) == [0, 0] for seed in seeds),
            "typed positive roof/exponent gate")

    basis = prefix["basis"]
    pool = prefix["pool"]
    proof_roots: dict[str, int] = {}
    acceptance_rows: list[dict[str, Any]] = []
    diagnostics_rows: list[dict[str, Any]] = []
    # The matrix pass intentionally released all one-seed gradients.  On the
    # positive path regenerate them target-by-target and compare the selected
    # typed candidate's raw C1 gradient with the literal affine prediction.
    # This is bounded and fail-closed; it never turns a mismatch into a
    # candidate rejection or an UNKNOWN terminal.
    base_compiled = build_wordexpr_candidate(0, [], inverse_words)
    base_eval = _affine_candidate_values(
        base_compiled, e4, 0, static_binding, pin_sources=True)
    for ordinal, (name, kind, root) in enumerate(targets["acceptance"], 1):
        if progress is not None:
            progress("positive_typed_replay", ordinal, 0)
        monitor.check(f"positive_replay_target_{ordinal}", force=True)
        gradient, value = _affine_direct_gradient(targets, evaluator, root, e4)
        require(value == e4.identity,
                f"typed positive acceptance quotient {name}")
        base_root = base_compiled["acceptance"][ordinal-1][2]
        base_gradient, base_value = _affine_direct_gradient(
            base_compiled, base_eval, base_root, e4)
        require(base_value == e4.identity,
                f"typed positive base quotient {name}")
        predicted = dict(base_gradient)
        for seed_index, seed in enumerate(seeds, 1):
            if progress is not None:
                progress("positive_typed_replay", ordinal, seed_index)
            coefficient = int(typed["coefficient_vector"][seed_index-1]) % 3
            if not coefficient:
                continue
            one = build_wordexpr_candidate(seed_index, seed, inverse_words)
            one_eval = _affine_candidate_values(
                one, e4, seed_index, static_binding, pin_sources=False)
            one_root = one["acceptance"][ordinal-1][2]
            one_gradient, one_value = _affine_direct_gradient(
                one, one_eval, one_root, e4)
            require(one_value == e4.identity,
                    f"typed positive seed quotient {name}/{seed_index}")
            delta = dict(one_gradient)
            add_scaled(delta, base_gradient, -1)
            add_scaled(predicted, delta, coefficient)
            one_eval.discard_candidate_memo()
        require(predicted == gradient,
                f"typed positive raw affine prediction {name}")
        packed = intern_raw_vector(gradient, pool)
        proof_root = basis.solve(packed)
        require(proof_root is not None,
                f"typed positive D2 membership {name}")
        proof_roots[name] = int(proof_root)
        acceptance_rows.append({
            "ordinal": ordinal, "name": name, "kind": kind,
            "quotient_identity": True,
            "gradient_sha256": digest_obj(raw_gradient_binding(
                name, kind, gradient, value)),
            "proof_root_node_id": int(proof_root),
            "direct_replay": True, "affine_prediction_checked": True,
        })
    for ordinal, (name, kind, root) in enumerate(targets["diagnostics"], 1):
        if progress is not None:
            progress("positive_typed_replay_diagnostics", ordinal, 0)
        monitor.check(f"positive_replay_diagnostic_{ordinal}")
        gradient, value = _affine_direct_gradient(targets, evaluator, root, e4)
        diagnostics_rows.append({
            "ordinal": ordinal, "name": name, "kind": kind,
            "quotient_identity": value == e4.identity,
            "gradient_sha256": digest_obj(raw_gradient_binding(
                name, kind, gradient, value)),
            "acceptance_predicate": False,
        })

    registry = ElementRegistry({3: e3, 4: e4})
    proof_dag, renumber = serialize_proof_dag(
        prefix["dag"], proof_roots, basis, registry)
    for row in acceptance_rows:
        row["proof_root_node_id"] = renumber[row["proof_root_node_id"]]
    base_eval.discard_candidate_memo()
    evaluator.discard_candidate_memo()
    return {
        "typed_candidate": _affine_typed_candidate_public(typed),
        "target_expression": dag.serialize_reachable(
            [(name, root) for name, _, root in
             targets["acceptance"]+targets["diagnostics"]] +
            [(f"source_{i+1}", root)
             for i, root in enumerate(targets["source_roots"])] +
            list(targets["correction_coface_roots"])),
        "correction_coface_gates": correction_values,
        "source_tuple_equal": True,
        "acceptance": acceptance_rows,
        "diagnostics": diagnostics_rows,
        "acceptance_count": len(acceptance_rows),
        "diagnostic_count": len(diagnostics_rows),
        "proof_dag": proof_dag,
        "quotient_element_registry": registry.rows,
        "proof_root_names": [row["name"] for row in acceptance_rows],
        "direct_replay": True,
        "raw_chain_affine_certificate": {
            "all_33_direct_gradients_replayed": True,
            "all_33_affine_predictions_checked": True,
            "correction_occurrence_E4_identity": True,
            "raw_C1_before_D2": True,
        },
    }


def affine_make_receipt(q3_data: dict[str, Any], status: str, reason: str,
                        source_hashes: dict[str, str]) -> dict[str, Any]:
    require(status in AFFINE_TERMINALS, "affine terminal")
    selected = q3_data.get("selected_solution", {})
    no_claims = {"claim_classification": "unknown_not_obstruction",
                 "claim_scope": "registered_old104_plus_four_triple_cube_affine_span_against_fixed_D2_prefix",
                 "full_D2_claimed": False, "full_H3_claimed": False,
                 "all_triple_products_claimed": False,
                 "all_depth3_claimed": False,
                 "negative_claimed": False, "B4_A_claimed": False,
                 "B4_B_claimed": False}
    claims = ({"claim_classification": "positive_exact_seedspan_certificate",
               "claim_scope":
                   "one_concrete_correction_in_registered_old104_plus_four_triple_cube_subgroup",
               "full_D2_claimed": False, "full_H3_claimed": False,
               "all_triple_products_claimed": False,
               "all_depth3_claimed": False,
               "negative_claimed": False, "B4_A_claimed": False,
               "B4_B_claimed": False}
              if status == "B345_SEEDSPAN_TRIPLE4_POSITIVE" else no_claims)
    return {
        "schema": AFFINE_SCHEMA, "status": status,
        "terminal_token": status, "reason": reason,
        "pins": {"formula_sha256": FORMULA_SHA,
                  "task_sha256": AFFINE_TASK_SHA,
                  "q3_producer": {"path": Q3_PRODUCER.as_posix(), "sha256": Q3_PRODUCER_SHA},
                  "q3_checker": {"path": Q3_CHECKER.as_posix(), "sha256": Q3_CHECKER_SHA},
                  "q3_driver": {"path": Q3_DRIVER.as_posix(), "sha256": Q3_DRIVER_SHA},
                   "q3_artifact": {"path": Q3_ARTIFACT_PATH.as_posix(), "sha256": Q3_ARTIFACT_SHA},
                   "157eb_producer": {"path": AFFINE_157EB_PRODUCER.as_posix(),
                                      "sha256": AFFINE_157EB_PRODUCER_SHA},
                   "157eb_checker": {"path": AFFINE_157EB_CHECKER.as_posix(),
                                     "sha256": AFFINE_157EB_CHECKER_SHA},
                   "157eb_driver": {"path": AFFINE_157EB_DRIVER.as_posix(),
                                    "sha256": AFFINE_157EB_DRIVER_SHA},
                   "v9_producer": {"path": str(V8_PRODUCER).replace("wordexpr_v8.py", "wordexpr_memo_v9.py"),
                                  "sha256": "7dede323c3c52bc7cf7d99af6d542b3683823879a4bb3e340aca8ce53dcf196f"},
                  "strong_prefix_source": {"path": AFFINE_STRONG_SOURCE.as_posix(),
                                             "sha256": AFFINE_STRONG_SHA}},
        "source_hashes": source_hashes,
        "input_q3_terminal": q3_data.get("terminal_token"),
        "output_path": AFFINE_OUTPUT_PATH.as_posix(),
        "fixed_roof": {"typed_source_word": selected.get("typed_source_word", list(FIXED_WORD)),
                       "exponent": 2, "marking_m": 0, "lambda": 1,
                       "outside_by_index_three": selected.get("arithmetic_outside_by_index_three")},
        "prefix_bindings": AFFINE_PREFIX_BINDINGS,
        "caps": AFFINE_CAPS,
        "caps_binding": AFFINE_CAPS_BINDING,
        "registered_universe": {
                                 "kind": "ordered_old104_plus_four_triple_cube_affine_span",
                                 "seed_count": 108, "old_seed_count": 104,
                                 "new_seed_count": 4, "cube_count": 26,
                                 "triple4_manifest": [dict(row) for row in TRIPLE4_MANIFEST],
                                 "cube_digest_sha256": TRIPLE4_CUBES_SHA,
                                 "BFS_prefix_rebuilt": False,
                                 "full_D2_claimed": False,
                                 "full_H3_claimed": False},
        "claim_boundary": claims,
        "affine_system": None, "targets": [], "diagnostics": [],
        "seed_family": None, "occurrence_preflight": None,
        "prefix_accounting": None, "strong_canary": None,
        "typed_positive_candidate": None, "resource_guards": None,
        "performance": None,
    }


AFFINE_COMMON_TOP_LEVEL = frozenset({
    "schema", "status", "terminal_token", "reason", "pins",
    "source_hashes", "input_q3_terminal", "output_path", "fixed_roof",
    "prefix_bindings", "caps", "caps_binding", "registered_universe",
    "claim_boundary", "resource_guards", "performance",
})
AFFINE_Q3_BASE_TOP_LEVEL = frozenset({
    "base_q3_replay", "seed_family", "normalized_inverse_fibre",
})
AFFINE_Q3_COMPLETE_TOP_LEVEL = AFFINE_Q3_BASE_TOP_LEVEL | {
    "occurrence_preflight",
}
AFFINE_PREFIX_TOP_LEVEL = frozenset({
    "directed_base_support", "directed_surgery", "prefix_rebuild",
    "prefix_basis_gate", "prefix_accounting", "strong_canary",
})
AFFINE_TARGET_TOP_LEVEL = frozenset({"targets", "affine_system"})
AFFINE_TARGET6_TOP_LEVEL = frozenset({
    "target6_formula_checks", "target6_base_gradient_sha256",
})
AFFINE_DUAL_TOP_LEVEL = frozenset({"dual_witness", "dual_provenance"})
AFFINE_POSITIVE_TOP_LEVEL = frozenset({
    "diagnostics", "typed_positive_candidate", "positive_replay",
})
AFFINE_RESOURCE_GUARD_KEYS = frozenset({
    "seconds", "minutes", "rss_bytes", "rss_gib",
    "external_job_limit_minutes", "safety_margin_minutes", "clock",
    "rss_primary", "rss_portable_fallback", "hit", "hit_reason",
    "last_checked_phase", "check_count", "current_rss_bytes",
    "peak_rss_bytes", "terminal_on_hit", "consulted_in_selftest",
    "schema",
})
AFFINE_SYSTEM_KEYS = frozenset({
    "variables", "rank", "nullity", "consistent", "row_space_sha256",
    "dual_witness",
})
AFFINE_TYPED_CANDIDATE_KEYS = frozenset({
    "f0_root", "correction_root", "candidate_root", "coefficient_vector",
    "nonzero_support", "expanded_count", "correction_word",
    "correction_word_flattened", "correction_expanded_count",
    "typed_product_order", "exponent_two_is_two_copies",
    "correction_word_sha256", "coefficient_vector_sha256", "expression",
    "expression_root_names",
})
AFFINE_POSITIVE_REPLAY_KEYS = frozenset({
    "target_expression", "correction_coface_gates", "source_tuple_equal",
    "acceptance", "diagnostics", "acceptance_count", "diagnostic_count",
    "proof_dag", "quotient_element_registry", "proof_root_names",
    "direct_replay", "raw_chain_affine_certificate",
})


def affine_schema_target6_started(receipt: dict[str, Any]) -> bool:
    """Return whether the target-6 ledger is committed at this stage."""
    rows = receipt.get("targets", [])
    if any(isinstance(row, dict) and row.get("ordinal") == 6
           for row in rows):
        return True
    token = receipt.get("terminal_token")
    if token == "B345_SEEDSPAN_TRIPLE4_POSITIVE":
        return True
    if token != "B345_SEEDSPAN_TRIPLE4_UNKNOWN_RESOURCE":
        return False
    partial = receipt.get("partial") or {}
    phase = str(partial.get("phase", ""))
    if phase.startswith("positive_typed_replay"):
        return True
    ordinal = int(partial.get("current_target_ordinal", 0) or 0)
    seed = int(partial.get("current_seed_index", 0) or 0)
    return ordinal > 6 or (ordinal == 6 and seed > 0)


def affine_expected_top_keys(receipt: dict[str, Any]) -> set[str]:
    """Compute the closed production envelope for a terminal/stage.

    This function is deliberately based only on terminal, reason and the
    producer's committed progress coordinates.  Optional late proof fields
    are never accepted merely because they are present in a receipt.
    """
    token = receipt.get("terminal_token")
    reason = receipt.get("reason")
    keys = set(AFFINE_COMMON_TOP_LEVEL)
    if token == "B345_SEEDSPAN_TRIPLE4_UNKNOWN_INPUT":
        errors = receipt.get("input_errors") or {}
        started = errors.get("mathematical_scan_started") is True
        phase = str((receipt.get("performance") or {}).get(
            "phase_complete", "authenticated_input"))
        keys.add("input_errors")
        if started and phase == "q3_schema_authentication":
            keys.add("base_q3_replay")
        elif started and phase == "affine_source_preflight":
            keys |= set(AFFINE_Q3_BASE_TOP_LEVEL)
        if started and (phase == "fresh_immutable_prefix" or
                        phase.startswith("affine_target") or
                        phase.startswith("positive_typed_replay")):
            keys |= set(AFFINE_Q3_COMPLETE_TOP_LEVEL)
        if started and (phase.startswith("affine_target") or
                        phase.startswith("positive_typed_replay")):
            keys |= set(AFFINE_PREFIX_TOP_LEVEL)
            if receipt.get("targets"):
                keys |= set(AFFINE_TARGET_TOP_LEVEL)
            if phase.startswith("positive_typed_replay"):
                keys |= set(AFFINE_TARGET6_TOP_LEVEL)
        return keys
    if token == "B345_SEEDSPAN_TRIPLE4_UNKNOWN_RESOURCE":
        partial = receipt.get("partial") or {}
        phase = str(partial.get("phase", ""))
        keys.add("partial")
        if phase == "authenticated_input":
            return keys
        keys |= set(AFFINE_Q3_BASE_TOP_LEVEL)
        if phase != "affine_source_preflight":
            keys.add("occurrence_preflight")
        if phase.startswith("affine_target") or \
                phase.startswith("positive_typed_replay"):
            keys |= set(AFFINE_PREFIX_TOP_LEVEL)
        evaluated = int(partial.get("evaluated_targets", 0) or 0)
        if evaluated > 0 or phase.startswith("positive_typed_replay"):
            keys |= set(AFFINE_TARGET_TOP_LEVEL)
        if affine_schema_target6_started(receipt):
            keys |= set(AFFINE_TARGET6_TOP_LEVEL)
        return keys
    if token == "B345_SEEDSPAN_TRIPLE4_SEARCH_INCOMPLETE":
        if reason == "affine_seed_preflight_unsupported":
            return keys | set(AFFINE_Q3_COMPLETE_TOP_LEVEL)
        if reason == "affine_system_inconsistent":
            keys |= set(AFFINE_Q3_COMPLETE_TOP_LEVEL)
            keys |= set(AFFINE_PREFIX_TOP_LEVEL)
            keys |= set(AFFINE_TARGET_TOP_LEVEL)
            if affine_schema_target6_started(receipt):
                keys |= set(AFFINE_TARGET6_TOP_LEVEL)
            return keys | set(AFFINE_DUAL_TOP_LEVEL)
    if token == "B345_SEEDSPAN_TRIPLE4_POSITIVE":
        keys |= set(AFFINE_Q3_COMPLETE_TOP_LEVEL)
        keys |= set(AFFINE_PREFIX_TOP_LEVEL)
        keys |= set(AFFINE_TARGET_TOP_LEVEL)
        keys |= set(AFFINE_TARGET6_TOP_LEVEL)
        return keys | set(AFFINE_POSITIVE_TOP_LEVEL)
    raise Reject("affine production terminal/stage schema")


def affine_finalize_receipt(receipt: dict[str, Any]) -> dict[str, Any]:
    """Drop uncommitted ledgers and enforce the exact production keyset."""
    expected = affine_expected_top_keys(receipt)
    for key in list(receipt):
        if key not in expected:
            del receipt[key]
    require(set(receipt) == expected, "affine producer exact top-level schema")
    token = receipt.get("terminal_token")
    require(receipt.get("status") == token,
            "affine producer status/terminal binding")
    performance = receipt.get("performance")
    require(isinstance(performance, dict),
            "affine producer terminal performance")
    if token == "B345_SEEDSPAN_TRIPLE4_POSITIVE":
        require(receipt.get("reason") ==
                "all_33_typed_acceptance_proofs_replayed" and
                performance.get("phase_complete") ==
                "positive_typed_replay_complete",
                "affine producer positive terminal values")
        positive_replay = receipt.get("positive_replay")
        require(isinstance(positive_replay, dict) and
                receipt.get("diagnostics") ==
                positive_replay.get("diagnostics"),
                "affine producer positive diagnostics binding")
    elif token == "B345_SEEDSPAN_TRIPLE4_UNKNOWN_INPUT":
        errors = receipt.get("input_errors")
        require(isinstance(errors, dict) and
                receipt.get("reason") ==
                errors.get("authenticated_external_input"),
                "affine producer input error binding")
        phase_complete = performance.get("phase_complete")
        if errors.get("mathematical_scan_started") is False:
            require(phase_complete in {
                        "authenticated_input", "q3_schema_authentication"},
                    "affine producer pre-scan input phase")
        else:
            require(phase_complete == "affine_source_preflight" or
                    phase_complete == "fresh_immutable_prefix" or
                    str(phase_complete).startswith("affine_target_") or
                    str(phase_complete).startswith("positive_typed_replay"),
                    "affine producer started input phase")
    elif token == "B345_SEEDSPAN_TRIPLE4_UNKNOWN_RESOURCE":
        partial = receipt.get("partial")
        require(isinstance(partial, dict) and
                performance.get("phase_complete") == partial.get("phase"),
                "affine producer resource phase binding")
    elif token == "B345_SEEDSPAN_TRIPLE4_SEARCH_INCOMPLETE":
        if receipt.get("reason") == "affine_seed_preflight_unsupported":
            require(performance.get("phase_complete") == "source_preflight",
                    "affine producer preflight phase binding")
        elif receipt.get("reason") == "affine_system_inconsistent":
            rows = receipt.get("targets")
            require(isinstance(rows, list) and rows and
                    all(isinstance(row, dict) for row in rows),
                    "affine producer inconsistent target ledger")
            last_ordinal = max(int(row["ordinal"]) for row in rows)
            require(performance.get("phase_complete") ==
                    f"affine_target_{last_ordinal}",
                    "affine producer inconsistent phase binding")
        else:
            raise Reject("affine producer incomplete reason registry")
    require(isinstance(receipt.get("performance"), dict) and
            set(receipt["performance"]) ==
            {"runtime_seconds", "phase_complete"},
            "affine producer performance nested schema")
    require(isinstance(receipt.get("resource_guards"), dict) and
            set(receipt["resource_guards"]) ==
            set(AFFINE_RESOURCE_GUARD_KEYS),
            "affine producer resource nested schema")
    if "affine_system" in receipt:
        system_keys = set(AFFINE_SYSTEM_KEYS)
        if receipt["affine_system"].get("canonical_solution_sha256") \
                is not None:
            system_keys.add("canonical_solution_sha256")
        require(set(receipt["affine_system"]) == system_keys,
                "affine producer affine-system nested schema")
    if "strong_canary" in receipt:
        require(set(receipt["strong_canary"]) == {
            "word", "cofaces", "target6", "raw_Fox_zero",
            "replayed_not_imported"},
            "affine producer strong-canary nested schema")
    if "typed_positive_candidate" in receipt:
        require(set(receipt["typed_positive_candidate"]) ==
                set(AFFINE_TYPED_CANDIDATE_KEYS),
                "affine producer typed-candidate nested schema")
    if "positive_replay" in receipt:
        require(set(receipt["positive_replay"]) ==
                set(AFFINE_POSITIVE_REPLAY_KEYS),
                "affine producer positive-replay nested schema")
    if "partial" in receipt:
        require(set(receipt["partial"]) == {
            "phase", "evaluated_targets",
            "unevaluated_target_results_are_null", "cap_reason",
            "current_target_ordinal", "current_seed_index",
            "live_remainder_entries", "cap_key", "cap_limit",
            "observed_count", "trigger_relation", "affine_equations",
        }, "affine producer resource-partial nested schema")
    return receipt


def affine_raw_split_gate(direct_gradient: dict[Any, int],
                          direct_value: Any,
                          typed_gradient: dict[Any, int],
                          typed_value: Any,
                          identity: Any, label: str) -> None:
    require(direct_value == identity and typed_value == identity and
            direct_gradient == typed_gradient,
            f"{label}: raw direct/typed split")


def affine_literal_selected_replay(coefficients: Sequence[int],
                                   seeds: Sequence[Sequence[int]]) -> list[int]:
    factors: list[int] = []
    for coefficient, seed in zip(coefficients, seeds):
        for _ in range(int(coefficient) % 3):
            factors.extend(seed)
    return reduce_word(factors)


def affine_split_ledger_gate(ledger: list[dict[str, Any]], *,
                             old_shortcut_count: int) -> None:
    require(len(ledger) == AFFINE_CAPS["seed_count"],
            "affine split ledger count")
    for index, row in enumerate(ledger, 1):
        require(isinstance(row, dict) and row.get("seed_index") == index and
                row.get("value_identity") is True and
                isinstance(row.get("gradient_sha256"), str),
                "affine split ledger order/identity")
        if index <= old_shortcut_count:
            require(set(row) == {"seed_index", "gradient_sha256",
                                 "value_identity", "identity_shortcut"} and
                    row["identity_shortcut"] is True,
                    "affine old split shortcut ledger")
        else:
            require(set(row) == {"seed_index", "gradient_sha256",
                                 "value_identity", "direct_replay",
                                 "typed_replay"} and
                    row["direct_replay"] is True and
                    row["typed_replay"] is True,
                    "affine new split direct/typed ledger")


def affine_target_row_schema_gate(row: dict[str, Any], *,
                                  old_shortcut_count: int) -> None:
    require(set(row) == {
        "ordinal", "base_remainder_size", "base_remainder_sha256",
        "coordinate_count", "delta_rank", "constraint_rank_gain",
        "constraint_rank", "nullity", "consistent", "row_space_sha256",
        "dual_witness", "live_remainder_entries", "affine_equations",
        "name", "kind", "diagnostics_excluded", "seed_count",
        "typed_split_count", "typed_split_old104_count",
        "typed_split_new4_count", "typed_split_order", "old_shortcut_count",
        "new_direct_count", "old_shortcut_seed_indices",
        "new_direct_seed_indices", "typed_split_sha256",
        "raw_chain_affine_certificate",
    } and row["seed_count"] == AFFINE_CAPS["seed_count"] and
            row["typed_split_count"] == AFFINE_CAPS["seed_count"] and
            row["typed_split_old104_count"] == AFFINE_CAPS["old_seed_count"] and
            row["typed_split_new4_count"] == AFFINE_CAPS["new_seed_count"] and
            row["old_shortcut_count"] == old_shortcut_count and
            row["new_direct_count"] == AFFINE_CAPS["seed_count"]-
                old_shortcut_count and
            row["typed_split_order"] == "old104_then_new4" and
            row["diagnostics_excluded"] is True and
            isinstance(row["raw_chain_affine_certificate"], dict) and
            set(row["raw_chain_affine_certificate"]) == {
                "typed_vs_flat_count", "typed_vs_flat_all_equal",
                "raw_C1_before_D2", "opcode_induction",
                "identity_root_shortcut"},
            "affine target row schema")


def _affine_digest_or_missing(path: Path) -> str:
    return digest_file(path) if path.is_file() else "MISSING"


def affine_run(q3_path: Path, output_path: Path) -> dict[str, Any]:
    start = time.monotonic()
    repo = Path(__file__).resolve().parents[1]
    q3_data: dict[str, Any] = {}
    input_error: str | None = None
    pinned = [(repo/AFFINE_157EB_PRODUCER, AFFINE_157EB_PRODUCER_SHA,
               "157eb producer"),
              (repo/AFFINE_157EB_CHECKER, AFFINE_157EB_CHECKER_SHA,
               "157eb checker"),
              (repo/AFFINE_157EB_DRIVER, AFFINE_157EB_DRIVER_SHA,
               "157eb driver"),
              (repo/Q3_PRODUCER, Q3_PRODUCER_SHA, "q3 producer"),
              (repo/Q3_CHECKER, Q3_CHECKER_SHA, "q3 checker"),
              (repo/Q3_DRIVER, Q3_DRIVER_SHA, "q3 driver"),
              (repo/AFFINE_STRONG_SOURCE, AFFINE_STRONG_SHA, "strong prefix")]
    try:
        if q3_path.resolve() != (repo/Q3_ARTIFACT_PATH).resolve():
            raise AffineInput("q3 artifact path drift")
        if output_path.resolve() != (repo/AFFINE_OUTPUT_PATH).resolve():
            raise AffineInput("affine output path drift")
        for path, expected, label in pinned:
            if not path.is_file():
                raise AffineInput(f"missing authenticated {label}")
            if digest_file(path) != expected:
                raise AffineInput(f"{label} SHA drift")
        if not q3_path.is_file():
            raise AffineInput("missing authenticated q3 artifact")
        if digest_file(q3_path) != Q3_ARTIFACT_SHA:
            raise AffineInput("q3 artifact SHA drift")
        q3_data = json.loads(q3_path.read_text(encoding="utf-8"))
        if not isinstance(q3_data, dict):
            raise AffineInput("q3 artifact is not an object")
    except (AffineInput, OSError, json.JSONDecodeError, UnicodeError) as exc:
        input_error = str(exc)
    source_hashes = {
        "producer_sha256": _affine_digest_or_missing(Path(__file__)),
        "checker_sha256": _affine_digest_or_missing(
            repo/"search/check_d972_b345_seedspan_triple4_v1.py"),
        "driver_sha256": _affine_digest_or_missing(
            repo/"search/d972_b345_seedspan_triple4_gha_driver_v1.g"),
        "strong_prefix_sha256": _affine_digest_or_missing(
            repo/AFFINE_STRONG_SOURCE)}
    receipt = affine_make_receipt(
        q3_data,
        "B345_SEEDSPAN_TRIPLE4_UNKNOWN_INPUT" if input_error else
        "B345_SEEDSPAN_TRIPLE4_UNKNOWN_RESOURCE",
        input_error or "initializing", source_hashes)
    monitor = ResourceMonitor(start, AFFINE_CAPS["producer_soft_timeout_seconds"])
    phase_name = "authenticated_input"
    current_target_ordinal = 0
    current_seed_index = 0
    live_remainder_entries = 0
    system: AffineSystem | None = None
    if input_error is not None:
        receipt["status"] = receipt["terminal_token"] = \
            "B345_SEEDSPAN_TRIPLE4_UNKNOWN_INPUT"
        receipt["reason"] = input_error
        receipt["input_errors"] = {"authenticated_external_input": input_error,
                                    "mathematical_scan_started": False}
        receipt["resource_guards"] = affine_monitor_receipt(monitor, False)
        receipt["performance"] = {"runtime_seconds": time.monotonic()-start,
                                   "phase_complete": "authenticated_input"}
        return affine_finalize_receipt(receipt)
    try:
        try:
            formulas_sha = digest_obj(q3_data["formulas"])
        except (KeyError, TypeError, ValueError) as exc:
            raise AffineInput(f"q3 formula schema drift: {exc}") from exc
        if (q3_data.get("schema") != Q3_SCHEMA or
                q3_data.get("terminal_token") !=
                "B345_Q3_TYPED_SIGN_EXACT_WITH_WORD_CORRECTION" or
                formulas_sha != FORMULA_SHA):
            raise AffineInput("authenticated q3 schema/formula drift")
        e3, e4, _ = reconstruct_quotients(q3_data)
        receipt["base_q3_replay"] = replay_base_q3(q3_data, e3, e4)
        seed_info = affine_seed_words(q3_data, e3)
        receipt["seed_family"] = seed_info
        normalized, raw_source_key, inverse_words = normalized_inverse_fibre(q3_data, e4)
        receipt["normalized_inverse_fibre"] = normalized
        phase_name = "affine_source_preflight"

        def source_progress(index: int) -> None:
            nonlocal current_seed_index
            current_seed_index = int(index)

        source_preflight = _affine_source_preflight(
            seed_info["seed_words"], e4, raw_source_key, inverse_words,
            monitor, source_progress)
        receipt["occurrence_preflight"] = source_preflight
        if not source_preflight["supported"]:
            receipt["status"] = receipt["terminal_token"] = \
                "B345_SEEDSPAN_TRIPLE4_SEARCH_INCOMPLETE"
            receipt["reason"] = source_preflight["reason"]
            receipt["resource_guards"] = affine_monitor_receipt(monitor, False)
            receipt["performance"] = {"runtime_seconds": time.monotonic()-start,
                                       "phase_complete": "source_preflight"}
            return affine_finalize_receipt(receipt)
        current_seed_index = 0
        phase_name = "fresh_immutable_prefix"
        receipt["strong_canary"] = affine_strong_canary(e4)
        static_binding = build_memo_static_quotient_binding(e4)
        base_candidate = build_wordexpr_candidate(0, [], inverse_words)
        base_eval = _affine_candidate_values(base_candidate, e4, 0,
                                             static_binding, pin_sources=True)
        require(tuple(base_eval.values[root-1] for root in base_candidate["source_roots"]) ==
                raw_source_key, "base source tuple binding")
        # The exact v7 prefix is rebuilt in a separate authenticated helper;
        # no old pool, rows, receipt, or blocker is imported.
        builder = _affine_load_strong_builder(repo)
        r0 = word_substitute(embed_f2_pb3(hexagon_words(FIXED_WORD)[0]), cofaces(3)[0])
        prefix = builder.build_fresh_prefix(sys.modules[__name__], e4, r0,
                                            monitor, start)
        receipt["directed_base_support"] = prefix["directed_base_support"]
        receipt["directed_surgery"] = prefix["directed_surgery"]
        receipt["prefix_accounting"] = prefix["accounting"]
        receipt["prefix_rebuild"] = {"source": AFFINE_STRONG_SOURCE.as_posix(),
                                      "source_sha256": AFFINE_STRONG_SHA,
                                      "fresh": True,
                                      "BFS_translations": 32768,
                                      "directed_translations": 207,
                                      "columns": 362725, "pivots": 362709,
                                      "dependent_columns": 16}
        basis_gate = affine_basis_gate(prefix["basis"], prefix["pool"])
        receipt["prefix_basis_gate"] = basis_gate
        anchors = prefix["base_source_key"]
        system = AffineSystem(
            AFFINE_CAPS["affine_variables"],
            coordinate_widths=(e4.degree, e4.pc.n))
        target_rows: list[dict[str, Any]] = []
        target_names = [name for name, _, _ in base_candidate["acceptance"]]
        require(target_names ==
                [f"charming_error_coface_{i}" for i in range(5)] +
                [f"hexagon_{j}_coface_{i}" for j in (1, 2) for i in range(5)] +
                ["ordered_A18_pentagon"] +
                [f"S_relation_{i}" for i in range(1, 12)] +
                [f"ST_generator_{i}" for i in range(1, 7)],
                "affine acceptance target order")
        # Target-major: only the current target's 108 sparse remainders live.
        for ordinal, (name, kind, base_root) in enumerate(base_candidate["acceptance"], 1):
            phase_name = f"affine_target_{ordinal}"
            current_target_ordinal = ordinal
            current_seed_index = 0
            monitor.check(phase_name, force=True)
            # For targets 1--5 the identity topology is exact for the old
            # 104 columns.  Only the four appended columns take the direct /
            # typed raw-Fox path; no all-108 shortcut is permitted.
            if ordinal <= 5:
                require(base_candidate["dag"].opcode[base_root-1] ==
                        WordExprDAG.IDENTITY and
                        base_candidate["dag"].rank[base_root-1] == 6 and
                        base_candidate["dag"].expanded_count[base_root-1] == 0,
                        f"charming identity root {name}")
                zero_binding = digest_obj(raw_gradient_binding(
                    name, kind, {}, e4.identity))
                split_ledger = [{"seed_index": index,
                                 "gradient_sha256": zero_binding,
                                 "value_identity": True,
                                 "identity_shortcut": True}
                                for index in range(1, AFFINE_CAPS["old_seed_count"]+1)]
                base_raw, base_value = _affine_direct_gradient(
                    base_candidate, base_eval, base_root, e4)
                require(base_value == e4.identity and base_raw == {},
                        f"charming base identity gradient {name}")
                delta_rows: dict[tuple[int, str], dict[int, int]] = {}
                live_remainder_entries = 0
                for seed_index, seed in enumerate(
                        seed_info["new_seed_words"],
                        AFFINE_CAPS["old_seed_count"]+1):
                    current_seed_index = seed_index
                    compiled = build_wordexpr_candidate(
                        seed_index, seed, inverse_words)
                    evaluator = _affine_candidate_values(
                        compiled, e4, seed_index, static_binding,
                        pin_sources=False)
                    root = compiled["acceptance"][ordinal-1][2]
                    require(evaluator.values[root-1] == e4.identity,
                            f"new seed target quotient identity {name}")
                    seed_raw, seed_value = _affine_direct_gradient(
                        compiled, evaluator, root, e4)
                    one_coefficients = [0]*len(seed_info["seed_words"])
                    one_coefficients[seed_index-1] = 1
                    typed_one = _affine_make_typed_positive(
                        one_coefficients, seed_info["seed_words"],
                        inverse_words)
                    typed_one_targets = _affine_build_typed_targets(
                        typed_one, inverse_words)
                    typed_one_root = _affine_select_typed_target_root(
                        typed_one_targets, ordinal)
                    typed_one_eval = _affine_candidate_values(
                        typed_one_targets, e4, seed_index, static_binding,
                        pin_sources=False, value_roots=[typed_one_root])
                    typed_raw, typed_value = _affine_direct_gradient(
                        typed_one_targets, typed_one_eval, typed_one_root, e4)
                    affine_raw_split_gate(
                        seed_raw, seed_value, typed_raw, typed_value,
                        e4.identity, f"new seed {name}/{seed_index}")
                    split_ledger.append({
                        "seed_index": seed_index,
                        "gradient_sha256": digest_obj(raw_gradient_binding(
                            name, kind, typed_raw, typed_value)),
                        "value_identity": True,
                        "direct_replay": True, "typed_replay": True,
                    })
                    delta_remainder = _affine_probe_remainder(
                        seed_raw, prefix, anchors, monitor)
                    live_remainder_entries += len(delta_remainder)
                    require(live_remainder_entries <=
                            AFFINE_CAPS["target_live_remainders"],
                            "new seed target live remainder cap")
                    for coordinate, coefficient in delta_remainder.items():
                        delta_rows.setdefault(coordinate, {})[seed_index-1] = coefficient
                    typed_one_eval.discard_candidate_memo()
                    evaluator.discard_candidate_memo()
                affine_split_ledger_gate(
                    split_ledger, old_shortcut_count=AFFINE_CAPS["old_seed_count"])
                target_row = _affine_target_row_transposed(
                    system, {}, delta_rows, ordinal,
                    live_remainder_entries, monitor, name)
                target_row.update({"name": name, "kind": kind,
                                   "diagnostics_excluded": True,
                                   "seed_count": len(seed_info["seed_words"]),
                                   "typed_split_count": len(split_ledger),
                                   "typed_split_old104_count":
                                       AFFINE_CAPS["old_seed_count"],
                                   "typed_split_new4_count":
                                       AFFINE_CAPS["new_seed_count"],
                                   "typed_split_order": "old104_then_new4",
                                   "old_shortcut_count":
                                       AFFINE_CAPS["old_seed_count"],
                                   "new_direct_count":
                                       AFFINE_CAPS["new_seed_count"],
                                   "old_shortcut_seed_indices": list(
                                       range(1, AFFINE_CAPS["old_seed_count"]+1)),
                                   "new_direct_seed_indices": list(
                                       range(AFFINE_CAPS["old_seed_count"]+1,
                                             AFFINE_CAPS["seed_count"]+1)),
                                   "typed_split_sha256": digest_obj(split_ledger),
                                   "raw_chain_affine_certificate": {
                                       "typed_vs_flat_count": len(split_ledger),
                                       "typed_vs_flat_all_equal": True,
                                       "raw_C1_before_D2": True,
                                       "opcode_induction":
                                           "FLAT/PRODUCT/INVERSE/SUBSTITUTE",
                                        "identity_root_shortcut": "old104_only",
                                    }})
                affine_target_row_schema_gate(
                    target_row, old_shortcut_count=AFFINE_CAPS["old_seed_count"])
                target_rows.append(target_row)
                receipt["targets"] = target_rows
                receipt["affine_system"] = {
                    "variables": AFFINE_CAPS["affine_variables"], "rank": system.rank(),
                    "nullity": system.nullity(),
                    "consistent": system.consistent,
                    "row_space_sha256": system.digest(),
                    "dual_witness": system.dual_public()}
                print("D972_B345_SEEDSPAN_TRIPLE4_PROGRESS " +
                      json.dumps({"target_ordinal": ordinal,
                                  "target_name": name, "rank": system.rank(),
                                  "nullity": system.nullity(),
                                  "consistent": system.consistent}, sort_keys=True),
                      flush=True)
                continue
            if ordinal == 6:
                # The target-6 formula is a delta formula.  The base row is
                # the direct Fox gradient of the actual f0 target; the empty
                # formula row below is retained only as a zero-delta
                # orientation canary.
                base_raw, base_value = _affine_direct_gradient(
                    base_candidate, base_eval, base_root, e4)
                require(base_value == e4.identity,
                        "target6 base direct quotient")
                base_formula = affine_target6_formula(
                    [], e4, include_gradient=True)
                empty_delta = base_formula.pop("_direct_gradient")
                require(base_formula.pop("_direct_value") == e4.identity and
                        empty_delta == {},
                        "target6 empty delta orientation canary")
                receipt.setdefault("target6_formula_checks", []).append(
                    base_formula)
                receipt["target6_base_gradient_sha256"] = digest_obj(
                    raw_gradient_binding(name, kind, base_raw, base_value))
                base_value = e4.identity
            else:
                base_value = base_eval.values[base_root-1]
                require(base_value == e4.identity,
                        f"base target quotient identity: {name}")
                base_raw, _ = _affine_direct_gradient(base_candidate, base_eval,
                                                       base_root, e4)
            base_rem = _affine_probe_remainder(base_raw, prefix, anchors, monitor)
            live_remainder_entries = len(base_rem)
            delta_rows: dict[tuple[int, str], dict[int, int]] = {}
            split_ledger: list[dict[str, Any]] = []
            for seed_index, seed in enumerate(seed_info["seed_words"], 1):
                current_seed_index = seed_index
                evaluator: WordExprEvaluator | None = None
                if ordinal == 6:
                    formula_row = affine_target6_formula(
                        seed, e4, include_gradient=True)
                    delta_raw = formula_row.pop("_direct_gradient")
                    require(formula_row.pop("_direct_value") == e4.identity,
                            f"target6 seed formula quotient {seed_index}")
                    receipt.setdefault("target6_formula_checks", []).append(
                        formula_row)
                    seed_raw = dict(base_raw)
                    add_scaled(seed_raw, delta_raw, 1)
                else:
                    compiled = build_wordexpr_candidate(
                        seed_index, seed, inverse_words)
                    evaluator = _affine_candidate_values(
                        compiled, e4, seed_index, static_binding,
                        pin_sources=False)
                    root = compiled["acceptance"][ordinal-1][2]
                    require(evaluator.values[root-1] == e4.identity,
                            f"seed target quotient identity: {name}")
                    seed_raw, _ = _affine_direct_gradient(
                        compiled, evaluator, root, e4)
                # Independent typed-vs-flat raw-chain equality.  The flat
                # one-seed candidate is the existing target calculation; the
                # second tree keeps f0*seed as a rank-2 PRODUCT and reaches
                # the same PB4 target by typed substitution.  This is the
                # all-target, all-108 load-bearing affine certificate.
                one_coefficients = [0]*len(seed_info["seed_words"])
                one_coefficients[seed_index-1] = 1
                typed_one = _affine_make_typed_positive(
                    one_coefficients, seed_info["seed_words"], inverse_words)
                typed_one_targets = (_affine_build_typed_target6(typed_one)
                                     if ordinal == 6 else
                                     _affine_build_typed_targets(
                                         typed_one, inverse_words))
                typed_one_root = _affine_select_typed_target_root(
                    typed_one_targets, ordinal)
                typed_one_eval = _affine_candidate_values(
                    typed_one_targets, e4, seed_index, static_binding,
                    pin_sources=False, value_roots=[typed_one_root])
                typed_raw, typed_value = _affine_direct_gradient(
                    typed_one_targets, typed_one_eval, typed_one_root, e4)
                affine_raw_split_gate(
                    seed_raw, e4.identity, typed_raw, typed_value,
                    e4.identity, f"typed/flat raw chain {name}/{seed_index}")
                split_ledger.append({
                    "seed_index": seed_index,
                    "gradient_sha256": digest_obj(raw_gradient_binding(
                        name, kind, typed_raw, typed_value)),
                    "value_identity": True,
                    "direct_replay": True, "typed_replay": True,
                })
                typed_one_eval.discard_candidate_memo()
                if ordinal != 6:
                    delta_raw = dict(seed_raw)
                    add_scaled(delta_raw, base_raw, -1)
                delta_remainder = _affine_probe_remainder(
                    delta_raw, prefix, anchors, monitor)
                if live_remainder_entries + len(delta_remainder) > \
                        AFFINE_CAPS["target_live_remainders"]:
                    raise ResourceStop(
                        "target_live_remainders",
                        cap_key="target_live_remainders",
                        cap_limit=AFFINE_CAPS["target_live_remainders"],
                        observed_count=(live_remainder_entries +
                                        len(delta_remainder)),
                        trigger_relation="gt")
                live_remainder_entries += len(delta_remainder)
                for coordinate, coefficient in delta_remainder.items():
                    row = delta_rows.setdefault(coordinate, {})
                    row[seed_index-1] = coefficient
                if evaluator is not None:
                    evaluator.discard_candidate_memo()
            affine_split_ledger_gate(split_ledger, old_shortcut_count=0)
            target_row = _affine_target_row_transposed(
                system, base_rem, delta_rows, ordinal,
                live_remainder_entries, monitor, name)
            target_row.update({"name": name, "kind": kind,
                               "diagnostics_excluded": True,
                               "seed_count": len(seed_info["seed_words"]),
                               "typed_split_count": len(split_ledger),
                               "typed_split_old104_count":
                                   AFFINE_CAPS["old_seed_count"],
                               "typed_split_new4_count":
                                   AFFINE_CAPS["new_seed_count"],
                               "typed_split_order": "old104_then_new4",
                               "old_shortcut_count": 0,
                               "new_direct_count": len(seed_info["seed_words"]),
                               "old_shortcut_seed_indices": [],
                               "new_direct_seed_indices": list(
                                   range(1, AFFINE_CAPS["seed_count"]+1)),
                               "typed_split_sha256": digest_obj(split_ledger),
                               "raw_chain_affine_certificate": {
                                   "typed_vs_flat_count": len(split_ledger),
                                   "typed_vs_flat_all_equal": True,
                                   "raw_C1_before_D2": True,
                                   "opcode_induction":
                                       "FLAT/PRODUCT/INVERSE/SUBSTITUTE",
                                    "identity_root_shortcut": False,
                                }})
            affine_target_row_schema_gate(target_row, old_shortcut_count=0)
            target_rows.append(target_row)
            current_seed_index = len(seed_info["seed_words"])
            receipt["targets"] = target_rows
            receipt["affine_system"] = {"variables": AFFINE_CAPS["affine_variables"], "rank": system.rank(),
                                         "nullity": system.nullity(),
                                         "consistent": system.consistent,
                                         "row_space_sha256": system.digest(),
                                         "dual_witness": system.dual_public()}
            print("D972_B345_SEEDSPAN_TRIPLE4_PROGRESS " +
                  json.dumps({"target_ordinal": ordinal, "target_name": name,
                              "rank": system.rank(), "nullity": system.nullity(),
                              "consistent": system.consistent}, sort_keys=True),
                  flush=True)
            if not system.consistent:
                receipt["status"] = receipt["terminal_token"] = \
                    "B345_SEEDSPAN_TRIPLE4_SEARCH_INCOMPLETE"
                receipt["reason"] = "affine_system_inconsistent"
                receipt["dual_witness"] = system.dual_public()
                receipt["dual_provenance"] = system.dual_public()
                receipt["resource_guards"] = affine_monitor_receipt(monitor, False)
                receipt["performance"] = {"runtime_seconds": time.monotonic()-start,
                                           "phase_complete": phase_name}
                return affine_finalize_receipt(receipt)
        # A consistent system requires the typed positive replay.  The
        # correction expression is constructed first; no flat long candidate
        # builder is used for the selected product itself.
        coefficients = system.canonical_solution()
        receipt["affine_system"]["canonical_solution_sha256"] = digest_obj(coefficients)
        # Positive replay is a separate stage.  Reset progress before even
        # constructing its typed candidate so an early setup ResourceStop is
        # represented as setup 0/0 rather than stale target-33 state.
        phase_name = "positive_typed_replay_setup"
        current_target_ordinal = 0
        current_seed_index = 0
        typed = _affine_make_typed_positive(
            coefficients, seed_info["seed_words"], inverse_words)

        def positive_progress(stage: str, target: int, seed: int) -> None:
            nonlocal phase_name, current_target_ordinal, current_seed_index
            phase_name = str(stage)
            current_target_ordinal = int(target)
            current_seed_index = int(seed)

        positive = _affine_positive_replay(
            typed, seed_info["seed_words"], inverse_words, raw_source_key,
            e3, e4, prefix, static_binding, monitor, positive_progress)
        receipt["typed_positive_candidate"] = positive["typed_candidate"]
        # The production envelope carries diagnostics at top level as well as
        # inside the positive replay ledger.  Keep the two projections bound
        # by value before the shared exact finalizer runs.
        receipt["diagnostics"] = positive["diagnostics"]
        receipt["positive_replay"] = {
            key: value for key, value in positive.items()
            if key != "typed_candidate"}
        receipt["status"] = receipt["terminal_token"] = \
            "B345_SEEDSPAN_TRIPLE4_POSITIVE"
        receipt["reason"] = "all_33_typed_acceptance_proofs_replayed"
        receipt["claim_boundary"] = {
            "claim_classification": "positive_exact_seedspan_certificate",
            "claim_scope": "one_concrete_correction_in_registered_old104_plus_four_triple_cube_subgroup",
            "full_D2_claimed": False, "full_H3_claimed": False,
            "all_triple_products_claimed": False,
            "all_depth3_claimed": False,
            "negative_claimed": False, "B4_A_claimed": False,
            "B4_B_claimed": False,
        }
        receipt["resource_guards"] = affine_monitor_receipt(monitor, False)
        receipt["performance"] = {"runtime_seconds": time.monotonic()-start,
                                   "phase_complete": "positive_typed_replay_complete"}
        return affine_finalize_receipt(receipt)
    except ResourceStop as exc:
        require(exc.reason in AFFINE_RESOURCE_REASONS,
                "affine resource reason registry")
        require(exc.cap_key == exc.reason and
                exc.observed_count is not None and
                exc.trigger_relation in {"gt", "ge"},
                "affine resource measurement ledger")
        monitor.hit_reason = exc.reason
        receipt["status"] = receipt["terminal_token"] = \
            "B345_SEEDSPAN_TRIPLE4_UNKNOWN_RESOURCE"
        receipt["reason"] = exc.reason
        receipt["resource_guards"] = affine_monitor_receipt(monitor, True)
        receipt["partial"] = {"phase": phase_name,
                               "evaluated_targets": len(receipt.get("targets", [])),
                               "unevaluated_target_results_are_null": True,
                               "cap_reason": exc.reason,
                               "current_target_ordinal": current_target_ordinal,
                               "current_seed_index": current_seed_index,
                               "live_remainder_entries": live_remainder_entries,
                               "cap_key": exc.cap_key,
                               "cap_limit": exc.cap_limit,
                               "observed_count": exc.observed_count,
                               "trigger_relation": exc.trigger_relation,
                               "affine_equations": (0 if system is None else
                                                     system.equations)}
        receipt["performance"] = {"runtime_seconds": time.monotonic()-start,
                                   "phase_complete": phase_name}
        return affine_finalize_receipt(receipt)
    except AffineInput as exc:
        # Authentication/schema failures discovered after the initial file
        # read remain external-input UNKNOWN_INPUT, never an uncaught crash.
        receipt["status"] = receipt["terminal_token"] = \
            "B345_SEEDSPAN_TRIPLE4_UNKNOWN_INPUT"
        receipt["reason"] = str(exc)
        receipt["input_errors"] = {
            "authenticated_external_input": str(exc),
            "mathematical_scan_started": phase_name != "authenticated_input",
        }
        receipt["resource_guards"] = affine_monitor_receipt(monitor, False)
        receipt["performance"] = {
            "runtime_seconds": time.monotonic()-start,
            "phase_complete": ("q3_schema_authentication"
                                if phase_name == "authenticated_input"
                                else phase_name),
        }
        return affine_finalize_receipt(receipt)


def affine_self_test() -> None:
    """One bounded, dependency-free combined producer/checker fixture."""
    toy_pc = PcCollector({"generator_count": 0, "relative_orders": [],
                          "power_relations": [], "inverses": [],
                          "conjugate_relations": [],
                          "inverse_conjugate_relations": []})
    toy_e4 = MatchedQuotient(4, 1, toy_pc,
                             [(perm_one(1), bytes())]*6)
    raw_canary = affine_raw_affine_canary(toy_e4)
    require(raw_canary == {"pair": True, "inverse": True, "square": True,
                           "nonzero_base": True, "base_delta_split": True},
            "selftest raw affine canary")
    target6_canary = affine_target6_formula([1, -2], toy_e4,
                                            include_gradient=True)
    require(target6_canary["formula_equals_direct"] is True and
            target6_canary.pop("_direct_value") == toy_e4.identity,
            "selftest target6 free-word/formula canary")
    target6_dag = WordExprDAG()
    target6_candidate = target6_dag.flat(FIXED_WORD, 2)
    target6_typed = {"dag": target6_dag,
                     "candidate_root": target6_candidate}
    target6_built = _affine_build_typed_target6(target6_typed)
    target6_static_binding = build_memo_static_quotient_binding(toy_e4)
    target6_candidate_eval = _affine_candidate_values(
        target6_typed, toy_e4, 1, static_binding=target6_static_binding,
        value_roots=[target6_candidate])
    require(target6_candidate_eval.values[target6_candidate-1] == toy_e4.identity,
            "selftest affine candidate evaluator static binding")
    target6_candidate_eval.discard_candidate_memo()
    require(_affine_select_typed_target_root(target6_built, 6) ==
            target6_built["acceptance"][0][2],
            "selftest target6-only acceptance selection")
    for bad_acceptance, label in [
            ([ ("wrong_name", "hexagon", target6_candidate)], "name"),
            ([ ("hexagon_1_coface_0", "wrong_kind", target6_candidate)],
             "kind"),
            ([ ("hexagon_1_coface_0", "hexagon", target6_candidate),
               ("extra", "hexagon", target6_candidate)], "cardinality")]:
        bad_target6 = dict(target6_built)
        bad_target6["acceptance"] = bad_acceptance
        try:
            _affine_select_typed_target_root(bad_target6, 6)
        except Reject:
            pass
        else:
            require(False, f"selftest target6 selection mutation: {label}")
    require(digest_obj([[1], [2], [3]]) != AFFINE_SEED_SHA,
            "selftest seed digest mutation")
    reordered = [[2], [1], [3]]
    require(digest_obj(reordered) != digest_obj([[1], [2], [3]]),
            "selftest seed reorder mutation")
    class ToyPool:
        @staticmethod
        def pivot_order(key: int) -> int:
            return key
    class ToyBasis:
        rows = {2: ({2: 1, 4: 1}, 0)}
    toy = ToyPool()
    rem = affine_full_remainder({1: 1, 2: 1}, ToyBasis(), toy)  # type: ignore[arg-type]
    require(rem == {1: 1, 4: 2}, "selftest later-pivot after earlier free")
    system = AffineSystem(3)
    require(system.add({0: 1, 1: 1}, 1) and system.add({1: 1}, 2),
            "selftest consistent affine")
    require(system.consistent and system.canonical_solution() == [2, 2, 0],
            "selftest canonical affine solution")
    inconsistent = AffineSystem(1)
    require(inconsistent.add({0: 1}, 0) and not inconsistent.add({0: 1}, 1) and
            not inconsistent.consistent, "selftest inconsistent affine")
    dual_fixture = AffineSystem(AFFINE_CAPS["affine_variables"])
    dual_fixture.add({0: 1, 1: 1}, 0,
                     [6, "target6", 1, "00"])
    require(not dual_fixture.add({0: 1, 1: 1}, 1,
                                 [6, "target6", 2, "00"]),
            "selftest dual contradiction")
    dual_public = dual_fixture.dual_public()
    require(not dual_fixture.consistent and isinstance(dual_public, dict) and
            dual_public["support_count"] == 2 and
            dual_public["normalized_rhs"] == 1 and
            dual_public["yTz_mod3"] == 2 and
            dual_public["target_boundary"]["target_ordinals"] == [6] and
            dual_public["target6_fixed_prefix_functional"] is True and
            dual_public["witness_provenance_entries"] == 2 and
            dual_public["live_provenance_entries"] >= 0 and
            dual_public["coordinate_encoding"] == {
                "label": "[target_ordinal,target_name,component,E4_blob_hex]",
                "component_numbering": "one_based_1_through_6",
                "E4_blob": "canonical permutation bytes then PC bytes",
                "permutation_width_bytes": 1, "pc_width_bytes": 0,
                "blob_width": 1, "blob_hex_length": 2,
                "endianness": "byte-string order; no integer reinterpretation",
                "pivot_order": "component then exact E4 bytes"},
            "selftest normalized dual support")
    require(AFFINE_CAPS["seed_count"] == 108 and
            AFFINE_CAPS["old_seed_count"] == 104 and
            AFFINE_CAPS["new_seed_count"] == 4 and
            len(TRIPLE4_MANIFEST) == 4 and
            TRIPLE4_MANIFEST[1]["cube_tuple"] == [9, 9, 10] and
            TRIPLE4_MANIFEST[2]["cube_tuple"] == [9, 11, 11],
            "selftest triple4 manifest/repeated literal gate")
    require(reduce_word([1, 1]) != inv_word([1, 1]),
            "selftest exponent two versus inverse")
    require("y->[2]" not in "F2 y->[3]", "selftest wrong PB3 image")
    require("C*(c-b)*C^-1+h1*a*h1^-1" != "C^-1*(c-b)*C+h1*a*h1^-1",
            "selftest target6 translation/order mutation")
    require({"context_id": 1} != {"context_id": 1, "value_identity": False},
            "selftest nonidentity occurrence mutation")
    require({"predicted": {1: 1}} != {"direct": {1: 2}},
            "selftest raw model/direct mismatch")
    no_claims = {"claim_classification": "unknown_not_obstruction",
                 "full_D2_claimed": False, "full_H3_claimed": False,
                 "all_triple_products_claimed": False,
                 "all_depth3_claimed": False,
                 "negative_claimed": False, "B4_A_claimed": False,
                 "B4_B_claimed": False}
    positive_claims = {**no_claims,
                       "claim_classification":
                           "positive_exact_seedspan_certificate"}
    require(no_claims != positive_claims and
            positive_claims["B4_B_claimed"] is False,
            "selftest positive/claim mutation boundary")

    def production_receipt_shape(token: str, reason: str,
                                 phase_name: str) -> dict[str, Any]:
        """Build a bounded production envelope through the real finalizer."""
        receipt = affine_make_receipt({}, token, reason, {})
        receipt["status"] = receipt["terminal_token"] = token
        receipt["reason"] = reason
        monitor = ResourceMonitor(time.monotonic(),
                                  AFFINE_CAPS["producer_soft_timeout_seconds"],
                                  rss_reader=lambda: 0)
        monitor.last_phase = phase_name
        resource_hit = token == "B345_SEEDSPAN_TRIPLE4_UNKNOWN_RESOURCE"
        receipt["resource_guards"] = affine_monitor_receipt(
            monitor, resource_hit)
        receipt["performance"] = {
            "runtime_seconds": 0.0, "phase_complete": phase_name}
        if token == "B345_SEEDSPAN_TRIPLE4_UNKNOWN_RESOURCE":
            receipt["partial"] = {
                "phase": phase_name, "evaluated_targets": 0,
                "unevaluated_target_results_are_null": True,
                "cap_reason": reason, "current_target_ordinal": 0,
                "current_seed_index": 0, "live_remainder_entries": 0,
                "cap_key": reason, "cap_limit": AFFINE_CAPS.get(reason, 0),
                "observed_count": AFFINE_CAPS.get(reason, 0) + 1,
                "trigger_relation": "gt", "affine_equations": 0,
            }
        elif token == "B345_SEEDSPAN_TRIPLE4_UNKNOWN_INPUT":
            receipt["input_errors"] = {
                "authenticated_external_input": reason,
                "mathematical_scan_started": phase_name !=
                    "authenticated_input",
            }
            if phase_name == "fresh_immutable_prefix":
                for key in AFFINE_Q3_COMPLETE_TOP_LEVEL:
                    receipt[key] = {}
        elif token == "B345_SEEDSPAN_TRIPLE4_SEARCH_INCOMPLETE":
            for key in AFFINE_Q3_COMPLETE_TOP_LEVEL | AFFINE_PREFIX_TOP_LEVEL:
                receipt[key] = {}
            if reason == "affine_seed_preflight_unsupported":
                receipt["performance"]["phase_complete"] = "source_preflight"
            else:
                receipt["strong_canary"] = {
                    "word": [], "cofaces": [], "target6": {},
                    "raw_Fox_zero": True, "replayed_not_imported": True,
                }
                receipt["targets"] = [{"ordinal": 1}]
                receipt["affine_system"] = {
                    "variables": AFFINE_CAPS["affine_variables"],
                    "rank": 0, "nullity": AFFINE_CAPS["affine_variables"],
                    "consistent": False, "row_space_sha256": "0"*64,
                    "dual_witness": {},
                }
                receipt["dual_witness"] = {}
                receipt["dual_provenance"] = {}
        elif token == "B345_SEEDSPAN_TRIPLE4_POSITIVE":
            for key in (AFFINE_Q3_COMPLETE_TOP_LEVEL |
                        AFFINE_PREFIX_TOP_LEVEL | AFFINE_TARGET6_TOP_LEVEL):
                receipt[key] = {}
            receipt["targets"] = [{"ordinal": 1}]
            receipt["affine_system"] = {
                "variables": AFFINE_CAPS["affine_variables"],
                "rank": 0, "nullity": AFFINE_CAPS["affine_variables"],
                "consistent": True, "row_space_sha256": "0"*64,
                "dual_witness": None,
            }
            receipt["strong_canary"] = {
                "word": [], "cofaces": [], "target6": {},
                "raw_Fox_zero": True, "replayed_not_imported": True,
            }
            receipt["diagnostics"] = []
            receipt["typed_positive_candidate"] = {
                key: None for key in AFFINE_TYPED_CANDIDATE_KEYS}
            receipt["positive_replay"] = {
                key: None for key in AFFINE_POSITIVE_REPLAY_KEYS}
            receipt["positive_replay"]["diagnostics"] = []
            receipt["performance"]["phase_complete"] = \
                "positive_typed_replay_complete"
        return affine_finalize_receipt(receipt)

    production_positive = production_receipt_shape(
        "B345_SEEDSPAN_TRIPLE4_POSITIVE",
        "all_33_typed_acceptance_proofs_replayed",
        "positive_typed_replay_complete")
    require(production_positive["diagnostics"] ==
            production_positive["positive_replay"]["diagnostics"],
            "selftest production success diagnostics binding")
    bad_positive = copy.deepcopy(production_positive)
    bad_positive["diagnostics"] = [{"forged": True}]
    try:
        affine_finalize_receipt(bad_positive)
    except Reject:
        pass
    else:
        require(False, "selftest production success diagnostics mutation")
    production_resource = production_receipt_shape(
        "B345_SEEDSPAN_TRIPLE4_UNKNOWN_RESOURCE", "affine_rows",
        "authenticated_input")
    require("diagnostics" not in production_resource and
            "positive_replay" not in production_resource,
            "selftest production resource positive-only absence")
    production_inconsistent = production_receipt_shape(
        "B345_SEEDSPAN_TRIPLE4_SEARCH_INCOMPLETE",
        "affine_system_inconsistent", "affine_target_1")
    bad_inconsistent = copy.deepcopy(production_inconsistent)
    bad_inconsistent["performance"]["phase_complete"] = "affine_target_2"
    try:
        affine_finalize_receipt(bad_inconsistent)
    except Reject:
        pass
    else:
        require(False, "selftest production inconsistent phase mutation")
    class MidAbsorptionStop:
        def check(self, phase: str) -> None:
            require(phase == "affine_transposed_row_absorption",
                    "selftest transposed monitor phase")
            raise ResourceStop(
                "selftest_transposed_mid", cap_key="selftest_transposed_mid",
                cap_limit=0, observed_count=1, trigger_relation="gt")
    transactional_system = AffineSystem(2, coordinate_widths=(2, 0))
    require(transactional_system.add({0: 1}, 0),
            "selftest transposed initial affine row")
    transactional_digest = transactional_system.digest()
    transactional_rows = {
        (1, f"{index:04x}"): 0 for index in range(1024)}
    try:
        _affine_target_row_transposed(
            transactional_system, transactional_rows, {}, 1, 0,
            MidAbsorptionStop())
    except ResourceStop as exc:
        require(exc.reason == "selftest_transposed_mid",
                "selftest transposed rollback stop")
    else:
        require(False, "selftest transposed rollback did not stop")
    require(transactional_system.digest() == transactional_digest and
            transactional_system.equations == 1 and
            transactional_system.consistent is True,
            "selftest transposed rollback exact state")
    source_boundary = {"phase": "affine_source_preflight", "seed": AFFINE_CAPS["old_seed_count"]}
    source_boundary["seed"] = 0
    source_boundary["phase"] = "fresh_immutable_prefix"
    require(source_boundary == {"phase": "fresh_immutable_prefix", "seed": 0},
            "selftest source-to-prefix phase boundary")
    expected = ([f"charming_error_coface_{i}" for i in range(5)] +
                [f"hexagon_{j}_coface_{i}" for j in (1, 2) for i in range(5)] +
                ["ordered_A18_pentagon"] +
                [f"S_relation_{i}" for i in range(1, 12)] +
                [f"ST_generator_{i}" for i in range(1, 7)])
    require(len(expected) == 33 and "T_relation_1" not in expected,
            "selftest diagnostics excluded")
    for token in AFFINE_TERMINALS:
        require(token.startswith("B345_SEEDSPAN_TRIPLE4_"),
                "selftest terminal mutation")
    try:
        raise ResourceStop("selftest_before_target", cap_key="selftest_before_target",
                           cap_limit=0, observed_count=1, trigger_relation="gt")
    except ResourceStop as exc:
        require(exc.reason == "selftest_before_target", "selftest resource stop")
    try:
        raise ResourceStop("selftest_during_target", cap_key="selftest_during_target",
                           cap_limit=0, observed_count=1, trigger_relation="gt")
    except ResourceStop as exc:
        require(exc.reason == "selftest_during_target", "selftest target resource stop")
    split_digest = "0"*64
    split_fixture = ([{"seed_index": index, "gradient_sha256": split_digest,
                       "value_identity": True, "identity_shortcut": True}
                      for index in range(1, 105)] +
                     [{"seed_index": index, "gradient_sha256": split_digest,
                       "value_identity": True, "direct_replay": True,
                       "typed_replay": True}
                      for index in range(105, 109)])
    affine_split_ledger_gate(split_fixture, old_shortcut_count=104)
    bad_split = copy.deepcopy(split_fixture)
    bad_split[104].pop("direct_replay")
    try:
        affine_split_ledger_gate(bad_split, old_shortcut_count=104)
    except Reject:
        pass
    else:
        require(False, "selftest new-column shortcut mutation")
    affine_raw_split_gate({0: 1}, toy_e4.identity, {0: 1},
                          toy_e4.identity, toy_e4.identity,
                          "selftest old/new raw formula")
    try:
        affine_raw_split_gate({0: 1}, toy_e4.identity, {0: 2},
                              toy_e4.identity, toy_e4.identity,
                              "selftest raw drift")
    except Reject:
        pass
    else:
        require(False, "selftest raw direct/typed drift")
    selected = affine_literal_selected_replay([2, 2, 0], [[1], [2], [3]])
    require(selected == reduce_word([1, 1, 2, 2]) and
            selected != reduce_word([1, 2]),
            "selftest consistent literal selected replay")
    nonzero_base = {0: 1}
    toy_columns = [{index: 1} for index in range(AFFINE_CAPS["seed_count"])]
    require(nonzero_base and len(toy_columns) == 108,
            "selftest nonzero base/108 columns")
    wide = AffineSystem(AFFINE_CAPS["affine_variables"])
    wide.add({0: 1, 1: 1}, 0, [6, "wide", 1, "00"])
    wide.add({0: 1, 1: 1}, 1, [6, "wide", 2, "00"])
    require(not wide.consistent and wide.dual_public()["support_count"] > 1 and
            wide.dual_public()["variables"] == 108,
            "selftest 108-column support-two inconsistency")
    row_system = AffineSystem(AFFINE_CAPS["affine_variables"])
    toy_row = _affine_target_row_transposed(
        row_system, {}, {}, 1, 0, None, "toy_split_target")
    toy_row.update({
        "name": "toy_split_target", "kind": "toy",
        "diagnostics_excluded": True, "seed_count": 108,
        "typed_split_count": 108, "typed_split_old104_count": 104,
        "typed_split_new4_count": 4, "typed_split_order": "old104_then_new4",
        "old_shortcut_count": 0, "new_direct_count": 108,
        "old_shortcut_seed_indices": [],
        "new_direct_seed_indices": list(range(1, 109)),
        "typed_split_sha256": digest_obj(split_fixture),
        "raw_chain_affine_certificate": {
            "typed_vs_flat_count": 108, "typed_vs_flat_all_equal": True,
            "raw_C1_before_D2": True,
            "opcode_induction": "FLAT/PRODUCT/INVERSE/SUBSTITUTE",
            "identity_root_shortcut": False,
        },
    })
    affine_target_row_schema_gate(toy_row, old_shortcut_count=0)
    bad_row = copy.deepcopy(toy_row)
    bad_row["new_direct_count"] = 104
    try:
        affine_target_row_schema_gate(bad_row, old_shortcut_count=0)
    except Reject:
        pass
    else:
        require(False, "selftest target-row split mutation")
    print("D972_B345_SEEDSPAN_TRIPLE4_PRODUCER_SELFTEST_PASS "
          "seed_order=1 seed_digest=1 source_anchor_policy=1 occurrence_gate=1 "
          "raw_chain=1 raw_pair=1 raw_inverse=1 raw_square=1 "
          "base_delta_split=1 target6_order=1 full_remainder=1 later_pivot=1 "
           "affine_consistent=1 affine_inconsistent=1 exponent_two=1 "
           "dual_witness=1 dual_support_cap=1 triple4_manifest=1 "
           "diagnostics_excluded=1 resource_pre_target=1 "
           "transposed_rollback=1 phase_boundary=1 "
           "candidate_static_binding=1 split_ledger=1 row_schema=1 "
           "schema_exact=1 pins_157eb=1 selected_replay=1 "
           "wide108_support2=1 terminal_values=1 production_shapes=1 "
           "terminals=4", flush=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("q3_artifact", nargs="?", type=Path)
    parser.add_argument("output", nargs="?", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        require(args.q3_artifact is None and args.output is None,
                "affine selftest accepts no paths")
        affine_self_test()
        return 0
    require(args.q3_artifact is not None and args.output is not None,
            "affine q3 artifact and output paths required")
    receipt = affine_run(args.q3_artifact.resolve(), args.output.resolve())
    checked_write(args.output.resolve(), receipt)
    print(f"{receipt['terminal_token']} output={args.output} "
          f"receipt_sha256={digest_file(args.output.resolve())}", flush=True)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Reject as exc:
        print(f"B345_SEEDSPAN_TRIPLE4_PRODUCER_FAIL {exc}", file=sys.stderr)
        raise SystemExit(1)
