#!/usr/bin/env python3
"""Checker-only v10 successor for the registered WordExpr/Fox memo-v9 lane.

No producer helper is imported.  The checker rebuilds the presentations,
cofaces, matched quotient arithmetic, Fox gradients, every shared-DAG leaf
and operation, and every accepted literal residual.  The v9 producer and
receipt schema remain byte-for-byte frozen; v10 repairs only the independent
replay pool schedule used to compare the lossless scan accounting.
"""

from __future__ import annotations

import argparse
import base64
import copy
import hashlib
import json
import math
import sys
import time
from array import array
from collections import OrderedDict, deque
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Sequence


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
V9_PRODUCER = Path("search/d972_b345_relfrat3_wordexpr_memo_v9.py")
V9_CHECKER = Path("search/check_d972_b345_relfrat3_wordexpr_memo_v9.py")
V9_DRIVER = Path("search/d972_b345_relfrat3_wordexpr_memo_gha_driver_v9.g")
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
TERMINALS = {
    "B345_RELFRAT3_WORDEXPR_PASS",
    "B345_RELFRAT3_WORDEXPR_SEARCH_INCOMPLETE",
    "B345_RELFRAT3_WORDEXPR_UNKNOWN_RESOURCE",
    "B345_RELFRAT3_WORDEXPR_UNKNOWN_INPUT",
}
V7_PREFIX_BINDINGS = {
    "stable_rounds_projection_sha256":
        "75a2894da0f19d0e541e27924ee63e220a6eca35e852b21088ee304ba42fc42d",
    "volatile_rounds_sha256_provenance_only":
        "e1c11cd5a436229c8730d5174b9a6981a508901a6e44d5362219e03d74557391",
    "translations_sha256":
        "a4b952bce888713e293587cd63d710465121e782448a3e2a571d80b992ea363f",
    "columns_sha256":
        "cb57176146b926df16e508429db5aa1ff6b5b0ec691f2328371973681089b343",
    "blocker_history_sha256":
        "b5f100e45e874ce5ee3270cd31350b4318cf40931055571ac70066e69d62de53",
    "final_blocker_sha256":
        "0cd653ee0966ccc83d270802bbb5d00b61731f28e27eec1918bb5ea282e00903",
}
RESOURCE_REASONS = {
    "producer_soft_timeout", "producer_soft_rss", "blocker_table",
    "element_pool", "missing_bounded_inverse_representative",
    "provenance_dag_edges", "provenance_dag_nodes", "section_slp_nodes",
    "single_sparse_elimination_row", "single_word_or_section_length",
    "sparse_pivot_rows", "target_elimination_support",
    "total_sparse_group_ring_keys", "transaction_trace_records",
    "directed_unique_translations", "directed_columns",
    "directed_section_expr_nodes", "directed_section_expr_edges",
    "wordexpr_nodes_per_candidate", "wordexpr_edges_per_candidate",
    "wordexpr_flat_leaves_per_candidate",
    "wordexpr_expanded_letter_count_per_target",
    "candidate_live_gradient_entries_total",
    "candidate_element_pool_suffix", "candidate_scan_records",
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
        self.cap_limit = (checker_resource_cap_limit(self.cap_key)
                          if cap_limit is None else int(cap_limit))
        self.observed_count = (None if observed_count is None
                               else int(observed_count))
        self.trigger_relation = trigger_relation


CHECKER_STARTED: float | None = None
CHECKER_CHECKS = 0


def checker_deadline(phase: str, force: bool = False) -> None:
    """Independent affine checker soft wall, matching the producer cap."""
    global CHECKER_CHECKS
    if CHECKER_STARTED is None:
        return
    CHECKER_CHECKS += 1
    if force or (CHECKER_CHECKS & 255) == 0:
        seconds = (AFFINE_CAPS["producer_soft_timeout_seconds"]
                   if "AFFINE_CAPS" in globals() else 7200)
        require(time.monotonic()-CHECKER_STARTED < seconds,
                f"checker soft replay bound: {phase}")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise Reject(message)


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


def current_rss_bytes() -> int:
    status = Path("/proc/self/status")
    if not status.exists():
        return 0
    for line in status.read_text(encoding="ascii").splitlines():
        if line.startswith("VmRSS:"):
            fields = line.split()
            require(len(fields) >= 3 and fields[2] == "kB", "checker VmRSS")
            return int(fields[1])*1024
    return 0


def reduce_word(word: Iterable[int]) -> list[int]:
    out: list[int] = []
    for x in word:
        require(isinstance(x, int) and x != 0, "signed word letter")
        if out and out[-1] == -x:
            out.pop()
        else:
            out.append(x)
        require(len(out) <= CAPS["single_word_or_section_length"], "word cap")
    return out


def inv_word(word: Sequence[int]) -> list[int]:
    return reduce_word(-x for x in reversed(word))


def substitute(word: Sequence[int], images: Sequence[Sequence[int]]) -> list[int]:
    out: list[int] = []
    for x in word:
        require(1 <= abs(x) <= len(images), "substitution index")
        out = reduce_word(out +
                          list(images[x-1] if x > 0 else inv_word(images[-x-1])))
    return out


def pp(words: Sequence[Sequence[int]]) -> list[int]:
    require(bool(words), "empty paper product")
    return reduce_word(x for word in reversed(words) for x in word)


def commutator(a: Sequence[int], b: Sequence[int]) -> list[int]:
    return reduce_word(inv_word(a) + inv_word(b) + list(a) + list(b))


def exponent_sums(word: Sequence[int], width: int) -> list[int]:
    return [sum(1 if x > 0 else -1 for x in word if abs(x) == i)
            for i in range(1, width+1)]


def replay_derived_ledger(word: Sequence[int], block: dict[str, Any]) -> None:
    require(block["convention"] == "[a,b]=a^-1*b^-1*a*b", "commutator convention")
    expanded: list[int] = []
    for row in block["factors"]:
        expanded = reduce_word(expanded + commutator(row["left"], row["right"]))
    require(expanded == reduce_word(word) == block["expanded_word"] and
            len(block["factors"]) == block["factor_count"] and
            exponent_sums(word, 2) == [0, 0], "commutator-product witness")


###############################################################################
# Independent presentation and literal-formula reconstruction.
###############################################################################


def pairs(rank: int) -> list[list[int]]:
    return [[i, j] for i in range(1, rank) for j in range(i+1, rank+1)]


def pair_index(rank: int, pair: Sequence[int]) -> int:
    require(list(pair) in pairs(rank), "pair index")
    return pairs(rank).index(list(pair)) + 1


def artin_step(rank: int, letter: int) -> list[list[int]]:
    i = abs(letter)
    require(1 <= i < rank, "Artin letter")
    rows = [[j] for j in range(1, rank+1)]
    if letter > 0:
        rows[i-1], rows[i] = [i, i+1, -i], [i]
    else:
        rows[i-1], rows[i] = [i+1], [-(i+1), i, i+1]
    return rows


def artin_images(rank: int, word: Sequence[int]) -> list[list[int]]:
    rows = [[i] for i in range(1, rank+1)]
    for letter in word:
        rows = [substitute(row, artin_step(rank, letter)) for row in rows]
    return rows


def aij(i: int, j: int) -> list[int]:
    return list(range(j-1, i, -1)) + [i, i] + [-k for k in range(i+1, j)]


def pure_relations(rank: int) -> list[list[int]]:
    if rank == 2:
        return []
    old_pairs = pairs(rank-1)
    old_map = [[pair_index(rank, p)] for p in old_pairs]
    answer = [substitute(word, old_map) for word in pure_relations(rank-1)]
    kernel = [[pair_index(rank, [k, rank])] for k in range(1, rank)]
    for i, j in old_pairs:
        g = pair_index(rank, [i, j])
        action = artin_images(rank-1, aij(i, j))
        for k in range(1, rank):
            h = pair_index(rank, [k, rank])
            answer.append(reduce_word([-g, h, g] +
                                      inv_word(substitute(action[k-1], kernel))))
    return answer


def coface_generator(rank: int, slot: int, pair: Sequence[int]) -> list[int]:
    i, j = pair
    if slot == 0:
        return [pair_index(rank+1, [i+1, j+1])]
    if slot == rank+1:
        return [pair_index(rank+1, [i, j])]
    if i == slot:
        return [pair_index(rank+1, [slot, j+1]),
                pair_index(rank+1, [slot+1, j+1])]
    if j == slot:
        return [pair_index(rank+1, [i, slot]),
                pair_index(rank+1, [i, slot+1])]
    require(1 <= slot <= rank, "coface slot")
    return [pair_index(rank+1, [i+(i > slot), j+(j > slot)])]


def cofaces(rank: int) -> list[list[list[int]]]:
    return [[coface_generator(rank, s, p) for p in pairs(rank)]
            for s in range(rank+2)]


def formula_subset() -> dict[str, Any]:
    c34 = cofaces(3)
    return {
        "convention": {
            "pair_order": "lexicographic_i_then_j",
            "word_product": "left_to_right",
            "paper_product": "displayed_factors_multiplied_right_to_left",
            "coface_slots": "0=left endpoint,1..r=strand doubling,r+1=right endpoint",
        },
        "presentations": {f"PB{r}": {"pairs": pairs(r),
                                      "relations": pure_relations(r)}
                          for r in (3, 4, 5)},
        "cofaces_3_4": c34,
        "a18_order": {
            "names": ["phi_123", "phi_234", "phi_12_3_4",
                      "phi_1_23_4", "phi_1_2_34"],
            "slots": [4, 0, 1, 2, 3],
            "maps": [c34[i] for i in (4, 0, 1, 2, 3)],
        },
    }


def f2_sub(word: Sequence[int], x: Sequence[int], y: Sequence[int]) -> list[int]:
    return substitute(word, [x, y])


def hexagon_words(f: Sequence[int]) -> list[list[int]]:
    x, y = [1], [2]
    z, u = inv_word(pp([x, y])), inv_word(pp([y, x]))
    fxy, fxz, fyz = f2_sub(f, x, y), f2_sub(f, x, z), f2_sub(f, y, z)
    fux, fuy = f2_sub(f, u, x), f2_sub(f, u, y)
    return [pp([fxy, inv_word(fxz), fyz]),
            pp([inv_word(fux), inv_word(fxy), fuy])]


def embed_f2(word: Sequence[int]) -> list[int]:
    return substitute(word, [[1], [3]])


def pentagon_word(f: Sequence[int]) -> list[int]:
    g = [[i] for i in range(1, 7)]
    contexts = [[g[0], g[3]], [g[3], g[5]],
                [pp([g[1], g[3]]), g[5]],
                [pp([g[0], g[1]]), pp([g[4], g[5]])],
                [g[0], pp([g[3], g[4]])]]
    values = [f2_sub(f, x, y) for x, y in contexts]
    return pp([inv_word(pp([values[4], values[2]])),
               values[1], values[3], values[0]])


def source_words(f: Sequence[int]) -> list[list[int]]:
    ff, g, gs = substitute(f, [[1], [4]]), substitute(f, [[1], [2]]), \
        substitute(f, [[4], [5]])
    f1234 = substitute(f, [[4, 2], [6]])
    h = substitute(f, [[2, 1], [3]])
    middle = substitute(f, [[2, 1], [6, 5]])
    return [[1], reduce_word(inv_word(g)+[2]+g),
            reduce_word(inv_word(ff)+inv_word(h)+[3]+h+ff),
            reduce_word(inv_word(ff)+[4]+ff),
            reduce_word(inv_word(ff)+inv_word(middle)+inv_word(gs)+[5]+gs+middle+ff),
            reduce_word(inv_word(f1234)+[6]+f1234)]


###############################################################################
# Receipt-only finite arithmetic, implemented independently.
###############################################################################


Perm = tuple[int, ...]
Pc = tuple[int, ...]
Element = tuple[Perm, Pc]
VKey = tuple[int, Element]
Vector = dict[VKey, int]


def row_perm(row: Sequence[int], degree: int) -> Perm:
    require(len(row) == degree, "permutation width")
    value = tuple(x-1 for x in row)
    require(set(value) == set(range(degree)), "permutation bijection")
    return value


def p_one(degree: int) -> Perm:
    return tuple(range(degree))


def p_mul(a: Perm, b: Perm) -> Perm:
    require(len(a) == len(b), "permutation degrees")
    return tuple(b[a[i]] for i in range(len(a)))


def p_inv(a: Perm) -> Perm:
    out = [0]*len(a)
    for i, image in enumerate(a):
        out[image] = i
    return tuple(out)


def p_order(a: Perm) -> int:
    seen = [False]*len(a)
    answer = 1
    for i in range(len(a)):
        if seen[i]:
            continue
        j, length = i, 0
        while not seen[j]:
            seen[j] = True
            j = a[j]
            length += 1
        answer = math.lcm(answer, length)
    return answer


def pc_word(coords: Sequence[int]) -> list[int]:
    return [i for i, exponent in enumerate(coords, 1) for _ in range(exponent)]


@dataclass
class Collector:
    data: dict[str, Any]

    def __post_init__(self) -> None:
        self.n = self.data["generator_count"]
        self.orders = list(self.data["relative_orders"])
        require(len(self.orders) == self.n <= 175 and all(x == 3 for x in self.orders),
                "collector rank/orders")
        self.powers = [self.coord(x) for x in self.data["power_relations"]]
        self.inverses = [self.coord(x) for x in self.data["inverses"]]
        self.conjugates = {(x["i"], x["j"]): self.coord(x["coords"])
                           for x in self.data["conjugate_relations"]}
        self.inv_conjugates = {(x["i"], x["j"]): self.coord(x["coords"])
                               for x in self.data["inverse_conjugate_relations"]}
        require(len(self.conjugates) == self.n*(self.n-1)//2 and
                set(self.conjugates) == set(self.inv_conjugates), "collector tables")
        self.pair_cache: OrderedDict[tuple[Pc, Pc], Pc] = OrderedDict()
        self.inverse_cache: OrderedDict[Pc, Pc] = OrderedDict()

    def coord(self, row: Sequence[int]) -> Pc:
        require(len(row) == self.n and all(isinstance(x, int) and 0 <= x < 3
                                           for x in row), "collector coordinate")
        return tuple(row)

    def identity(self) -> Pc:
        return (0,)*self.n

    def collect(self, signed: Sequence[int]) -> Pc:
        tokens: list[int] = []
        for x in signed:
            require(1 <= abs(x) <= self.n, "collector signed index")
            tokens.extend([x] if x > 0 else pc_word(self.inverses[-x-1]))
        cap = max(10000, 1000*(1+len(tokens))*(1+self.n))
        count = 0
        while True:
            changed = False
            for i in range(len(tokens)-1):
                if tokens[i] > tokens[i+1]:
                    a, b = tokens[i], tokens[i+1]
                    tokens[i:i+2] = [b] + pc_word(self.conjugates[(a, b)])
                    changed = True
                    break
            if not changed:
                i = 0
                while i < len(tokens):
                    j = i
                    while j < len(tokens) and tokens[j] == tokens[i]:
                        j += 1
                    if j-i >= 3:
                        tokens[i:i+3] = pc_word(self.powers[tokens[i]-1])
                        changed = True
                        break
                    i = j
            if not changed:
                break
            count += 1
            require(count <= cap, "collector rewrite cap")
        row = [0]*self.n
        last = 0
        for x in tokens:
            require(x >= last, "collector order")
            row[x-1] += 1
            require(row[x-1] < 3, "collector power")
            last = x
        return tuple(row)

    def mul(self, a: Pc, b: Pc) -> Pc:
        key = (a, b)
        if key in self.pair_cache:
            self.pair_cache.move_to_end(key)
            return self.pair_cache[key]
        answer = self.collect(pc_word(a)+pc_word(b))
        if len(self.pair_cache) >= CAPS["pc_pair_product_cache"]:
            self.pair_cache.popitem(last=False)
        self.pair_cache[key] = answer
        return answer

    def inverse(self, a: Pc) -> Pc:
        if a in self.inverse_cache:
            self.inverse_cache.move_to_end(a)
            return self.inverse_cache[a]
        word: list[int] = []
        for i in range(self.n, 0, -1):
            for _ in range(a[i-1]):
                word.extend(pc_word(self.inverses[i-1]))
        answer = self.collect(word)
        if len(self.inverse_cache) >= CAPS["pc_inverse_cache"]:
            self.inverse_cache.popitem(last=False)
        self.inverse_cache[a] = answer
        return answer

    def eval(self, word: Sequence[int], images: Sequence[Pc]) -> Pc:
        out = self.identity()
        for x in word:
            value = images[abs(x)-1]
            out = self.mul(out, value if x > 0 else self.inverse(value))
        return out


@dataclass
class Quotient:
    rank: int
    degree: int
    collector: Collector
    generators: list[Element]

    def __post_init__(self) -> None:
        self.identity = (p_one(self.degree), self.collector.identity())
        self.inverse_generators = [self.inverse(x) for x in self.generators]

    def mul(self, a: Element, b: Element) -> Element:
        return p_mul(a[0], b[0]), self.collector.mul(a[1], b[1])

    def inverse(self, a: Element) -> Element:
        return p_inv(a[0]), self.collector.inverse(a[1])

    def eval(self, word: Sequence[int], images: Sequence[Element] | None = None) -> Element:
        marked = self.generators if images is None else images
        out = self.identity
        for x in word:
            value = marked[abs(x)-1]
            out = self.mul(out, value if x > 0 else self.inverse(value))
        return out


def reconstruct(data: dict[str, Any]) -> tuple[Quotient, Quotient]:
    c3, c4 = Collector(data["groups"]["PB3"]), Collector(data["groups"]["PB4"])
    fine3 = [c3.coord(x["coords"]) for x in data["groups"]["PB3"]["marked_generators"]]
    fine4 = [c4.coord(x["coords"]) for x in data["groups"]["PB4"]["marked_generators"]]
    q0r, q4r = data["coarse_models"]["Q0"], data["coarse_models"]["Q4"]
    q0 = [row_perm(x, q0r["degree"]) for x in q0r["marked_permutations"]]
    q4 = [row_perm(x, q4r["degree"]) for x in q4r["marked_permutations"]]
    z = p_inv(p_mul(q0[1], q0[0]))
    e3 = Quotient(3, q0r["degree"], c3,
                  [(q0[0], fine3[0]), (z, fine3[1]), (q0[1], fine3[2])])
    e4 = Quotient(4, q4r["degree"], c4, list(zip(q4, fine4)))
    require(all(e3.eval(r) == e3.identity for r in pure_relations(3)) and
            all(e4.eval(r) == e4.identity for r in pure_relations(4)),
            "matched presentation replay")
    return e3, e4


def add(vector: dict[Any, int], key: Any, coefficient: int) -> None:
    value = (vector.get(key, 0)+coefficient) % 3
    if value:
        vector[key] = value
    else:
        vector.pop(key, None)


def add_scaled(target: dict[Any, int], source: dict[Any, int], scalar: int) -> None:
    for key, coefficient in source.items():
        add(target, key, scalar*coefficient)


def fox(word: Sequence[int], quotient: Quotient) -> tuple[Vector, Element]:
    prefix = quotient.identity
    out: Vector = {}
    for x in word:
        i = abs(x)
        if x > 0:
            add(out, (i, prefix), 1)
            prefix = quotient.mul(prefix, quotient.generators[i-1])
        else:
            prefix = quotient.mul(prefix, quotient.inverse_generators[i-1])
            add(out, (i, prefix), 2)
    return out, prefix


def boundary1(vector: Vector, quotient: Quotient) -> dict[Element, int]:
    out: dict[Element, int] = {}
    for (i, value), coefficient in vector.items():
        add(out, quotient.mul(value, quotient.generators[i-1]), coefficient)
        add(out, value, -coefficient)
    return out


def translate(vector: Vector, value: Element, quotient: Quotient) -> Vector:
    return {(i, quotient.mul(value, g)): coefficient
            for (i, g), coefficient in vector.items()}


def encode(vector: Vector, rank: int,
           element_to_id: dict[tuple[int, Element], int]) -> list[list[int]]:
    return [[i, element_to_id[(rank, value)], coefficient]
            for (i, value), coefficient in sorted(vector.items())]


def perm_eval(word: Sequence[int], images: Sequence[Perm]) -> Perm:
    out = p_one(len(images[0]))
    for x in word:
        value = images[abs(x)-1]
        out = p_mul(out, value if x > 0 else p_inv(value))
    return out


def enumerate_small(identity: Any, generators: Sequence[Any], mul: Any,
                    inverse: Any, cap: int) -> set[Any]:
    steps = list(generators)+[inverse(x) for x in generators]
    seen, queue = {identity}, [identity]
    while queue:
        a = queue.pop()
        for g in steps:
            b = mul(a, g)
            if b not in seen:
                seen.add(b)
                require(len(seen) <= cap, "small group cap")
                queue.append(b)
    return seen


def paper_conj(value: Any, y: Any, mul: Any, inverse: Any) -> Any:
    return mul(mul(value, y), inverse(value))


def validate_base_replay(receipt: dict[str, Any], q3: dict[str, Any],
                         e3: Quotient, e4: Quotient) -> None:
    block = receipt["base_q3_replay"]
    selected = q3["selected_solution"]
    require(q3["schema"] == Q3_SCHEMA and q3["terminal_token"] ==
            "B345_Q3_TYPED_SIGN_EXACT_WITH_WORD_CORRECTION" and
            selected["typed_source_word"] == FIXED_WORD and
            selected["correction_word"] == [] and selected["exponent"] == 2,
            "frozen q3 witness")
    require(block["fixed_word"] == FIXED_WORD and block["roof_exponent"] == 2 and
            block["roof_order"] == 9 and block["marking_m"] == 0 and
            block["lambda"] == 1 and block["replayed_not_copied"] is True,
            "base replay metadata")
    hexes = hexagon_words(FIXED_WORD)
    pent = pentagon_word(FIXED_WORD)
    require(block["hexagon_residual_words_F2"] == hexes and
            all(e3.eval(embed_f2(w)) == e3.identity for w in hexes),
            "base hexagon")
    require(block["pentagon_residual_word_PB4"] == pent and
            e4.eval(pent) == e4.identity, "base pentagon")
    replay_derived_ledger(FIXED_WORD, block["derived_membership"])
    q0_value = perm_eval(FIXED_WORD, [e3.generators[0][0], e3.generators[2][0]])
    require(p_order(q0_value) == 9, "base roof order")
    models = q3["coarse_models"]
    p = [row_perm(x, models["P"]["degree"]) for x in models["P"]["marked_permutations"]]
    g = [row_perm(x, models["G9"]["degree"]) for x in models["G9"]["marked_permutations"]]
    fp, fg = perm_eval(FIXED_WORD, p), perm_eval(FIXED_WORD, g)
    p_onto = len(enumerate_small(p_one(9), [p[0], paper_conj(fp, p[1], p_mul, p_inv)],
                                 p_mul, p_inv, 504)) == 504
    g_onto = len(enumerate_small(p_one(27), [g[0], paper_conj(fg, g[1], p_mul, p_inv)],
                                 p_mul, p_inv, 2916)) == 2916
    b = [e3.generators[0][1], e3.generators[2][1]]
    fb = e3.collector.eval(FIXED_WORD, b)
    b_onto = len(enumerate_small(e3.collector.identity(),
                                 [b[0], paper_conj(fb, b[1],
                                                   e3.collector.mul,
                                                   e3.collector.inverse)],
                                 e3.collector.mul, e3.collector.inverse, 27)) == 27
    require(block["onto_small_factors"] == {"P_order_504": p_onto,
                                             "G9_order_2916": g_onto,
                                             "B2_order_27": b_onto} and
            p_onto and g_onto and b_onto, "base onto factors")
    require(block["settled_source_words"] == source_words(FIXED_WORD),
            "base settlement source")


def rebuild_dictionary(q3: dict[str, Any], e3: Quotient) -> dict[str, Any]:
    base = [reduce_word(row["word"]*3) for row in q3["correction_fibre"]["records"]
            if row["word"]]
    base = list(dict.fromkeys(tuple(x) for x in base))
    seeds: list[list[int]] = []
    for raw in base:
        k = list(raw)
        require(e3.eval(embed_f2(k)) == e3.identity, "dictionary cube H3")
        for gen in ([1], [2]):
            for word in (commutator(k, gen), commutator(gen, k)):
                if word and word not in seeds:
                    require(exponent_sums(word, 2) == [0, 0] and
                            e3.eval(embed_f2(word)) == e3.identity,
                            "dictionary seed H3")
                    seeds.append(word)
    words: list[list[int]] = [[]]
    parent_indices = [0]
    signed_seed_edges = [0]
    seen = {()}
    queue: deque[int] = deque([1])
    steps = [(index+1, word) for index, word in enumerate(seeds)] + [
        (-(index+1), inv_word(word)) for index, word in enumerate(seeds)]
    require(all(e3.eval(embed_f2(word)) == e3.identity for word in seeds),
            "dictionary seed E3 kernel")
    while queue and len(words) < CAPS["candidate_correction_dictionary"]:
        parent_index = queue.popleft()
        prefix = words[parent_index-1]
        for signed_edge, step in steps:
            word = reduce_word(prefix+step)
            if tuple(word) not in seen:
                require(exponent_sums(word, 2) == [0, 0],
                        "dictionary free-derived invariant")
                seen.add(tuple(word))
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
    provenance = {"parent_indices": parent_indices,
                  "signed_seed_edges": signed_seed_edges,
                  "word_sha256": [digest_obj(word) for word in words]}
    return {"order": "identity, then breadth-first products of authenticated H3 commutator seeds and inverses",
            "source": "commutators with cubes of the frozen 27-word coarse-trivial exponent-three fibre",
            "words": words, "count": len(words),
            "cap": CAPS["candidate_correction_dictionary"],
            "all_words_in_H3": True, "all_words_in_coarse_J_H": True,
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
            "provenance_sha256": digest_obj(provenance)}


def q_product(q: Quotient, values: Sequence[Element]) -> Element:
    out = q.identity
    for value in values:
        out = q.mul(out, value)
    return out


def q_paper_product(q: Quotient, values: Sequence[Element]) -> Element:
    return q_product(q, list(reversed(values)))


def element_blob(value: Element) -> bytes:
    return bytes(value[0]) + bytes(value[1])


def direct_cheap_failures(candidate: Sequence[int], correction: Sequence[int],
                          e4: Quotient) -> list[str]:
    coarse: list[str] = []
    first: list[str] = []
    second: list[str] = []
    for slot, mapping in enumerate(cofaces(3)):
        x, y = e4.eval(mapping[0]), e4.eval(mapping[2])
        if e4.eval(correction, [x, y]) != e4.identity:
            coarse.append(f"correction_coarse_J_H_coface_{slot}")
        z = e4.inverse(q_paper_product(e4, [x, y]))
        u = e4.inverse(q_paper_product(e4, [y, x]))
        fxy = e4.eval(candidate, [x, y])
        fxz = e4.eval(candidate, [x, z])
        fyz = e4.eval(candidate, [y, z])
        fux = e4.eval(candidate, [u, x])
        fuy = e4.eval(candidate, [u, y])
        if q_paper_product(e4, [fxy, e4.inverse(fxz), fyz]) != e4.identity:
            first.append(f"hexagon_1_coface_{slot}")
        if q_paper_product(e4, [e4.inverse(fux), e4.inverse(fxy), fuy]) != \
                e4.identity:
            second.append(f"hexagon_2_coface_{slot}")
    bad = coarse + first + second
    g = e4.generators
    contexts = [
        [g[0], g[3]], [g[3], g[5]],
        [q_paper_product(e4, [g[1], g[3]]), g[5]],
        [q_paper_product(e4, [g[0], g[1]]),
         q_paper_product(e4, [g[4], g[5]])],
        [g[0], q_paper_product(e4, [g[3], g[4]])],
    ]
    parts = [e4.eval(candidate, context) for context in contexts]
    pent = q_paper_product(
        e4, [e4.inverse(q_paper_product(e4, [parts[4], parts[2]])),
             parts[1], parts[3], parts[0]])
    if pent != e4.identity:
        bad.append("ordered_A18_pentagon")
    source = source_words(candidate)
    for index, relation in enumerate(pure_relations(4), 1):
        if e4.eval(substitute(relation, source)) != e4.identity:
            bad.append(f"S_relation_{index}")
    return bad


def independent_context_registry(e4: Quotient) \
        -> tuple[list[tuple[Element, Element]], dict[str, int], dict[str, Any]]:
    contexts: list[tuple[Element, Element]] = []
    exact: dict[tuple[Element, Element], int] = {}
    named: list[dict[str, Any]] = []
    by_name: dict[str, int] = {}

    def register(name: str, left: Element, right: Element) -> None:
        require(name not in by_name, "duplicate independent context name")
        pair = (left, right)
        context_id = exact.get(pair)
        if context_id is None:
            context_id = len(contexts)+1
            exact[pair] = context_id
            contexts.append(pair)
        by_name[name] = context_id
        named.append({"name": name, "context_id": context_id})

    for slot, mapping in enumerate(cofaces(3)):
        x, y = e4.eval(mapping[0]), e4.eval(mapping[2])
        z = e4.inverse(q_paper_product(e4, [x, y]))
        u = e4.inverse(q_paper_product(e4, [y, x]))
        register(f"correction_coface_{slot}", x, y)
        register(f"hexagon_1_fxy_{slot}", x, y)
        register(f"hexagon_1_fxz_{slot}", x, z)
        register(f"hexagon_1_fyz_{slot}", y, z)
        register(f"hexagon_2_fux_{slot}", u, x)
        register(f"hexagon_2_fxy_{slot}", x, y)
        register(f"hexagon_2_fuy_{slot}", u, y)
    g = e4.generators
    pentagon = [
        (g[0], g[3]), (g[3], g[5]),
        (q_paper_product(e4, [g[1], g[3]]), g[5]),
        (q_paper_product(e4, [g[0], g[1]]),
         q_paper_product(e4, [g[4], g[5]])),
        (g[0], q_paper_product(e4, [g[3], g[4]])),
    ]
    for index, pair in enumerate(pentagon):
        register(f"pentagon_part_{index}", *pair)
    source_contexts = [
        ("source_ff", g[0], g[3]),
        ("source_g", g[0], g[1]),
        ("source_gs", g[3], g[4]),
        ("source_f1234", q_product(e4, [g[3], g[1]]), g[5]),
        ("source_h", q_product(e4, [g[1], g[0]]), g[2]),
        ("source_middle", q_product(e4, [g[1], g[0]]),
         q_product(e4, [g[5], g[4]])),
    ]
    for name, left, right in source_contexts:
        register(name, left, right)
    require(len(contexts) <= CAPS["cheap_contexts"], "context registry cap")
    rows = [{"context_id": index, "left_hex": element_blob(pair[0]).hex(),
             "right_hex": element_blob(pair[1]).hex()}
            for index, pair in enumerate(contexts, 1)]
    public = {"context_count": len(contexts), "contexts": rows,
              "named_uses": named, "named_use_count": len(named),
              "named_use_mapping_sha256": digest_obj(named),
              "context_rows_sha256": digest_obj(rows),
              "deduplication": "exact E4 pair equality"}
    return contexts, by_name, public


def independent_dp_failures(index: int,
                            correction_values: list[list[Element]],
                            base_values: list[Element], by_name: dict[str, int],
                            e4: Quotient) -> list[str]:
    def correction(name: str) -> Element:
        return correction_values[by_name[name]-1][index]

    def candidate(name: str) -> Element:
        context = by_name[name]-1
        return e4.mul(base_values[context], correction_values[context][index])

    coarse: list[str] = []
    first: list[str] = []
    second: list[str] = []
    for slot in range(5):
        if correction(f"correction_coface_{slot}") != e4.identity:
            coarse.append(f"correction_coarse_J_H_coface_{slot}")
        fxy = candidate(f"hexagon_1_fxy_{slot}")
        fxz = candidate(f"hexagon_1_fxz_{slot}")
        fyz = candidate(f"hexagon_1_fyz_{slot}")
        fux = candidate(f"hexagon_2_fux_{slot}")
        fxy2 = candidate(f"hexagon_2_fxy_{slot}")
        fuy = candidate(f"hexagon_2_fuy_{slot}")
        if q_paper_product(e4, [fxy, e4.inverse(fxz), fyz]) != e4.identity:
            first.append(f"hexagon_1_coface_{slot}")
        if q_paper_product(e4, [e4.inverse(fux), e4.inverse(fxy2), fuy]) != \
                e4.identity:
            second.append(f"hexagon_2_coface_{slot}")
    bad = coarse + first + second
    parts = [candidate(f"pentagon_part_{i}") for i in range(5)]
    pent = q_paper_product(
        e4, [e4.inverse(q_paper_product(e4, [parts[4], parts[2]])),
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
        g[0], q_product(e4, [e4.inverse(gv), g[1], gv]),
        q_product(e4, [e4.inverse(ff), e4.inverse(h), g[2], h, ff]),
        q_product(e4, [e4.inverse(ff), g[3], ff]),
        q_product(e4, [e4.inverse(ff), e4.inverse(middle), e4.inverse(gs),
                       g[4], gs, middle, ff]),
        q_product(e4, [e4.inverse(f1234), g[5], f1234]),
    ]
    for relator_index, relation in enumerate(pure_relations(4), 1):
        if e4.eval(relation, source) != e4.identity:
            bad.append(f"S_relation_{relator_index}")
    return bad


def rebuild_fixed_context_dp(dictionary: dict[str, Any], e4: Quotient) \
        -> tuple[dict[str, Any], list[list[str]]]:
    contexts, by_name, context_public = independent_context_registry(e4)
    seeds = dictionary["seed_words"]
    signed = [(index+1, word) for index, word in enumerate(seeds)] + [
        (-(index+1), inv_word(word)) for index, word in enumerate(seeds)]
    seed_images: list[dict[int, Element]] = []
    seed_digest = hashlib.sha256()
    for context_index, pair in enumerate(contexts, 1):
        row: dict[int, Element] = {}
        for edge, word in signed:
            value = e4.eval(word, list(pair))
            row[edge] = value
            seed_digest.update(context_index.to_bytes(2, "little"))
            seed_digest.update(edge.to_bytes(2, "little", signed=True))
            seed_digest.update(element_blob(value))
        seed_images.append(row)
    correction_values: list[list[Element]] = []
    propagated = hashlib.sha256()
    for context_index in range(len(contexts)):
        values = [e4.identity]
        propagated.update(element_blob(e4.identity))
        for word_index in range(1, dictionary["count"]):
            parent = dictionary["parent_indices"][word_index]-1
            edge = dictionary["signed_seed_edges"][word_index]
            require(0 <= parent < word_index and edge in seed_images[context_index],
                    "independent DP parent/edge")
            value = e4.mul(values[parent], seed_images[context_index][edge])
            values.append(value)
            propagated.update(element_blob(value))
        correction_values.append(values)
    base_values = [e4.eval(FIXED_WORD, list(pair)) for pair in contexts]
    failures: list[list[str]] = []
    survivors: list[int] = []
    gate_names = [f"correction_coarse_J_H_coface_{i}" for i in range(5)] + \
        [f"hexagon_1_coface_{i}" for i in range(5)] + \
        [f"hexagon_2_coface_{i}" for i in range(5)] + \
        ["ordered_A18_pentagon"] + [f"S_relation_{i}" for i in range(1, 12)]
    gate_bits = {name: bytearray((dictionary["count"]+7)//8)
                 for name in gate_names}
    gate_counts = {name: 0 for name in gate_names}
    evaluated_prefix = hashlib.sha256()
    survivor_prefix = hashlib.sha256()
    for index in range(dictionary["count"]):
        bad = independent_dp_failures(index, correction_values, base_values,
                                      by_name, e4)
        failures.append(bad)
        if not bad:
            survivors.append(index+1)
            survivor_prefix.update((index+1).to_bytes(4, "little"))
        evaluated_prefix.update(canonical_bytes([index+1, bad]) + b"\n")
        for name in bad:
            gate_bits[name][index//8] |= 1 << (index % 8)
            gate_counts[name] += 1
    bitsets = []
    for name in gate_names:
        raw = bytes(gate_bits[name])
        bitsets.append({"gate": name, "failure_count": gate_counts[name],
                        "byte_length": len(raw),
                        "sha256": hashlib.sha256(raw).hexdigest(),
                        "base64": base64.b64encode(raw).decode("ascii")})
    semantic = {
        "complete": True, "evaluated": dictionary["count"],
        "current_candidate": None, "contexts": context_public,
        "signed_seed_count": len(signed),
        "signed_seed_images_sha256": seed_digest.hexdigest(),
        "propagated_correction_values_sha256": propagated.hexdigest(),
        "recurrence": "rho(c_i)=rho(c_parent)*rho(signed_seed)",
        "free_reduction_value_invariant": True,
        "failure_bitsets": bitsets,
        "failure_lists_sha256": digest_obj([[i+1, row]
                                             for i, row in enumerate(failures)]),
        "survivor_count": len(survivors), "survivor_indices": survivors,
        "survivor_indices_sha256": digest_obj(survivors),
        "evaluated_prefix_sha256": evaluated_prefix.hexdigest(),
        "survivor_prefix_sha256": survivor_prefix.hexdigest(),
        "per_gate_failure_counts": gate_counts,
        "direct_word_replay_required_for_full_lane": True,
    }
    return semantic, failures


def two_sided_residuals(source: Sequence[Sequence[int]],
                        inverse: Sequence[Sequence[int]]) \
        -> tuple[list[list[int]], list[list[int]]]:
    st = [reduce_word(substitute(inverse[i], source)+[-(i+1)]) for i in range(6)]
    ts = [reduce_word(substitute(source[i], inverse)+[-(i+1)]) for i in range(6)]
    return st, ts


def rebuild_normalized_inverse_fibre(q3: dict[str, Any], e4: Quotient) \
        -> tuple[dict[str, Any], tuple[Element, ...], list[list[int]]]:
    block = q3["canonical_roof_powers"]
    rows = block["rows"]
    require([row["exponent"] for row in rows] == [1, 2, 4, 5, 7, 8] and
            block["canonicalized_each_step"] is True and
            block["literal_power_words_retained"] is False,
            "normalized q3 power receipt")
    row7s = [row for row in rows if row["exponent"] == 7]
    row2s = [row for row in rows if row["exponent"] == 2]
    require(len(row7s) == len(row2s) == 1, "normalized exponent-two/seven rows")
    row7 = row7s[0]
    correction = q3["correction_fibre"]
    records = correction["records"]
    require(len(records) == 27 and correction["certificate"]["order"] == 27 and
            correction["certificate"]["enumerated_count"] == 27 and
            correction["certificate"]["all_words_coarse_identity"] is True,
            "normalized inverse correction fibre")
    selected_q3 = q3["selected_solution"]
    selected_index = selected_q3["correction_index"]
    require(selected_q3["exponent"] == 2 and 1 <= selected_index <= 27 and
            reduce_word(row2s[0]["word"] + records[selected_index-1]["word"]) ==
            FIXED_WORD,
            "fixed exponent-two tuple/canonical fibre binding")
    base_source = source_words(FIXED_WORD)
    base_key = tuple(e4.eval(word) for word in base_source)
    tested: list[int] = []
    passing: list[int] = []
    candidates: dict[int, tuple[list[int], list[list[int]]]] = {}
    for index, record in enumerate(records, 1):
        candidate = reduce_word(row7["word"] + record["word"])
        inverse = source_words(candidate)
        st, ts = two_sided_residuals(base_source, inverse)
        tested.append(index)
        if all(e4.eval(word) == e4.identity for word in st+ts):
            passing.append(index)
            candidates[index] = (candidate, inverse)
    require(tested == list(range(1, 28)) and passing,
            "normalized exponent-seven fibre has no E4 two-sided inverse")
    selected = passing[0]
    selected_candidate, selected_inverse = candidates[selected]
    maximum = max(map(len, selected_inverse))
    require(maximum <= CAPS["single_word_or_section_length"],
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
        "max_inverse_word_length": maximum,
        "raw_endomorphism_powering_used": False,
        "componentwise_Q4_Pi4_inverse_words_combined": False,
    }
    return public, base_key, selected_inverse


def rebuild_inverse(f: Sequence[int], e4: Quotient,
                    claimed: dict[str, Any], normalized: dict[str, Any],
                    base_key: tuple[Element, ...]) -> dict[str, Any]:
    source = source_words(f)
    require(tuple(e4.eval(word) for word in source) == base_key,
            "selected candidate lacks the bounded normalized inverse key")
    inverse = normalized["selected_inverse_words"]
    st, ts = two_sided_residuals(source, inverse)
    expected = {
        "normalized_exponent": 7,
        "normalized_roof_order": 9,
        "source_words": source,
        "inverse_words": inverse,
        "ST_residuals": st,
        "TS_residuals": ts,
        "construction": "finite normalized exponent-seven inverse from the pinned complete 27-fibre",
        "max_inverse_word_length": max(map(len, inverse)),
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
    require(claimed == expected and
            all(e4.eval(word) == e4.identity for word in st),
            "finite normalized inverse receipt")
    return expected


def expected_targets(selected: dict[str, Any], e4: Quotient,
                     normalized: dict[str, Any],
                     base_key: tuple[Element, ...]) \
        -> list[tuple[str, str, list[int]]]:
    f, correction = selected["selected_word"], selected["correction_word"]
    require(f == reduce_word(FIXED_WORD+correction), "selected word/correction")
    replay_derived_ledger(f, selected["derived_witness"])
    error = reduce_word(f+inv_word(selected["derived_witness"]["expanded_word"]))
    require(selected["charming_error_word"] == error, "charming error word")
    c34 = cofaces(3)
    coarse_jh = [substitute(embed_f2(correction), mapping) for mapping in c34]
    require(selected["correction_coarse_J_H_coface_words"] == coarse_jh and
            selected["correction_coarse_J_H_all_five"] is True and
            selected["correction_coarse_J_H_all_five_replayed"] is True and
            selected["correction_in_finer_J_Phi_required"] is False and
            selected["correction_finer_J_Phi_membership_not_required"] is True and
            selected["correction_J_Phi_coset_is_lift_freedom"] is True and
            "kernel" in selected["J_H_definition"] and
            "intersection" in selected["J_Phi_definition"] and
            selected["J_Phi_not_identified_with_Phi3_H3"] is True and
            all(e4.eval(word) == e4.identity for word in coarse_jh),
            "coarse J_H correction/finer J_Phi lift freedom")
    charm = [substitute(embed_f2(error), mapping) for mapping in c34]
    hexes = hexagon_words(f)
    require(selected["hexagon_words_F2"] == hexes and
            selected["pentagon_word_PB4"] == pentagon_word(f),
            "selected literal words")
    targets: list[tuple[str, str, list[int]]] = []
    targets += [(f"charming_error_coface_{i}", "charming", word)
                for i, word in enumerate(charm)]
    for hindex, h in enumerate(hexes, 1):
        for slot, mapping in enumerate(c34):
            targets.append((f"hexagon_{hindex}_coface_{slot}", "hexagon",
                            substitute(embed_f2(h), mapping)))
    targets.append(("ordered_A18_pentagon", "pentagon", pentagon_word(f)))
    inverse = rebuild_inverse(f, e4, selected["inverse"], normalized, base_key)
    for index, relator in enumerate(pure_relations(4), 1):
        targets.append((f"S_relation_{index}", "endomorphism_relation",
                        substitute(relator, inverse["source_words"])))
        targets.append((f"T_relation_{index}", "endomorphism_relation",
                        substitute(relator, inverse["inverse_words"])))
    targets += [(f"ST_generator_{i+1}", "onto_two_sided_inverse", word)
                for i, word in enumerate(inverse["ST_residuals"])]
    targets += [(f"TS_generator_{i+1}", "onto_two_sided_inverse", word)
                for i, word in enumerate(inverse["TS_residuals"])]
    # This helper reconstructs the historical interleaved 50-word list so
    # the selected-pair metadata can be audited.  Def. 2.9 acceptance in v7
    # is only the 33 S/ST-side rows; T/TS rows are diagnostics and may be
    # nonidentity without suppressing a PASS.
    require(all(e4.eval(word) == e4.identity
                for name, _, word in targets
                if not name.startswith("T_relation_") and
                   not name.startswith("TS_generator_")),
            "expected acceptance target outside H4")
    return targets


def validate_registry(rows: Sequence[dict[str, Any]],
                      quotients: dict[int, Quotient],
                      expression_values: Sequence[Element] | None = None) \
        -> tuple[dict[int, Element], dict[tuple[int, Element], int]]:
    by_id: dict[int, Element] = {}
    reverse: dict[tuple[int, Element], int] = {}
    for expected_id, row in enumerate(rows, 1):
        flat = "section_word" in row
        expression = "section_expression_root" in row
        expected_keys = ({"id", "rank", "section_word",
                          "coarse_permutation", "fine_pc_coords"} if flat else
                         {"id", "rank", "section_expression_root",
                          "coarse_permutation", "fine_pc_coords"})
        require(set(row) == expected_keys and flat != expression and
                row["id"] == expected_id and row["rank"] in quotients and
                (not flat or isinstance(row["section_word"], list) and
                 len(row["section_word"]) <=
                 CAPS["single_word_or_section_length"]),
                "element registry id/rank/section kind")
        quotient = quotients[row["rank"]]
        value = (row_perm(row["coarse_permutation"], quotient.degree),
                 quotient.collector.coord(row["fine_pc_coords"]))
        if flat:
            require(quotient.eval(row["section_word"]) == value,
                    "element registry flat section")
        else:
            root = row["section_expression_root"]
            require(row["rank"] == 4 and expression_values is not None and
                    isinstance(root, int) and 0 <= root < len(expression_values) and
                    expression_values[root] == value,
                    "element registry expression section")
        require((row["rank"], value) not in reverse, "duplicate registry element")
        by_id[expected_id] = value
        reverse[(row["rank"], value)] = expected_id
    return by_id, reverse


def validate_fox_models(block: dict[str, Any], e3: Quotient, e4: Quotient,
                        reverse: dict[tuple[int, Element], int]) \
        -> dict[int, list[Vector]]:
    models: dict[int, list[Vector]] = {}
    for name, rank, quotient in (("PB3", 3, e3), ("PB4", 4, e4)):
        row = block[name]
        require(row["rank"] == rank and row["field"] == 3 and
                row["generator_count"] == len(pairs(rank)) and
                row["relator_count"] == len(pure_relations(rank)) and
                row["D1D2_zero"] is True and
                row["full_regular_matrix_constructed"] is False and
                row["H1_basis_or_rank_constructed"] is False,
                f"{name} Fox metadata")
        require(row["identity_element_id"] == reverse[(rank, quotient.identity)] and
                row["marked_element_ids"] ==
                [reverse[(rank, x)] for x in quotient.generators],
                f"{name} marked registry")
        convention = row["left_fox_convention"]
        require(convention == {
            "product_rule": "d(uv)=d(u)+u*d(v)",
            "positive_letter": "+prefix",
            "negative_letter": "advance prefix by x_i^-1, then -prefix",
            "D1": "sum_i coefficient*(q(x_i)-1) on the right",
            "translated_column": "left multiplication by the translation element",
        }, f"{name} Fox convention")
        columns: list[Vector] = []
        for index, (relator, claimed) in enumerate(
                zip(pure_relations(rank), row["relator_columns"]), 1):
            gradient, value = fox(relator, quotient)
            require(value == quotient.identity and boundary1(gradient, quotient) == {},
                    f"{name} D1D2 reconstruction")
            require(claimed["relator_index"] == index and claimed["word"] == relator and
                    claimed["quotient_identity"] is True and
                    claimed["D1_of_gradient_zero"] is True and
                    claimed["gradient"] == encode(gradient, rank, reverse),
                    f"{name} relator column {index}")
            columns.append(gradient)
        models[rank] = columns
    require(block["PB5"] in (
                {"constructed": False,
                 "reason": "direct B3/B4 literal pair certified first"},
                {"constructed": False,
                 "reason": "direct B3/B4 registered WordExpr pair certified first"}),
            "PB5 positive-first bypass")
    return models


def _decode_packed_array(block: dict[str, Any], expected_type: str,
                         typecode: str, cap: int) -> Sequence[int]:
    require(set(block) == {"type", "array_typecode", "endianness", "length",
                           "itemsize", "byte_length", "cap", "sha256", "base64"} and
            block["type"] == expected_type and
            block["array_typecode"] == typecode and
            block["endianness"] == "little" and block["cap"] == cap and
            isinstance(block["length"], int) and 0 <= block["length"] <= cap and
            isinstance(block["base64"], str), "packed array schema")
    try:
        raw = base64.b64decode(block["base64"], validate=True)
    except Exception as exc:
        raise Reject("packed array base64") from exc
    require(base64.b64encode(raw).decode("ascii") == block["base64"] and
            hashlib.sha256(raw).hexdigest() == block["sha256"] and
            block["byte_length"] == len(raw), "packed array bytes/SHA")
    if typecode == "B":
        require(block["itemsize"] == 1 and len(raw) == block["length"],
                "packed uint8 length")
        return raw
    values = array(typecode)
    require(block["itemsize"] == values.itemsize and
            len(raw) == block["length"]*values.itemsize,
            "packed integer byte length")
    values.frombytes(raw)
    if sys.byteorder != "little":
        values.byteswap()
    return values


def decode_section_expressions(block: dict[str, Any], quotient: Quotient) \
        -> list[Element]:
    require(set(block) == {"format", "node_order",
                           "ordinary_word_composition",
                           "canonical_value_width", "node_count",
                           "edge_count", "roots", "arrays",
                           "manifest_sha256"} and
            block["format"] == "typed-section-expression-arrays/v1" and
            block["node_order"] == "zero_based_topological" and
            block["ordinary_word_composition"] is True and
            block["canonical_value_width"] ==
                quotient.degree+quotient.collector.n and
            isinstance(block["node_count"], int) and
            0 <= block["node_count"] <= CAPS["directed_section_expr_nodes"] and
            isinstance(block["edge_count"], int) and
            0 <= block["edge_count"] <= CAPS["directed_section_expr_edges"],
            "section expression header")
    n = block["node_count"]
    if n == 0:
        require(block["arrays"] == {} and block["roots"] == [] and
                block["edge_count"] == 0 and block["manifest_sha256"] ==
                digest_obj({"arrays": {}, "roots": []}),
                "empty section expressions")
        return []
    arrays = block["arrays"]
    require(set(arrays) == {"kind", "signed_generator", "left", "right",
                            "flat_offsets", "flat_letters",
                            "canonical_values"},
            "section expression arrays")
    kinds = _decode_packed_array(arrays["kind"], "uint8", "B",
                                 CAPS["directed_section_expr_nodes"])
    signed = _decode_packed_array(arrays["signed_generator"], "int8", "b",
                                  CAPS["directed_section_expr_nodes"])
    left = _decode_packed_array(arrays["left"], "uint32", "I",
                                CAPS["directed_section_expr_nodes"])
    right = _decode_packed_array(arrays["right"], "uint32", "I",
                                 CAPS["directed_section_expr_nodes"])
    offsets = _decode_packed_array(
        arrays["flat_offsets"], "uint32", "I",
        CAPS["directed_section_expr_nodes"]+1)
    letters = _decode_packed_array(
        arrays["flat_letters"], "int16", "h",
        CAPS["directed_section_expr_nodes"] *
        CAPS["single_word_or_section_length"])
    values_raw = _decode_packed_array(
        arrays["canonical_values"], "uint8", "B",
        CAPS["directed_section_expr_nodes"] *
        (quotient.degree+quotient.collector.n))
    width = quotient.degree+quotient.collector.n
    require(len(kinds) == len(signed) == len(left) == len(right) == n and
            len(offsets) == n+1 and offsets[0] == 0 and offsets[-1] ==
            len(letters) and all(offsets[i] <= offsets[i+1]
                                 for i in range(n)) and
            len(values_raw) == n*width and
            sum(1 if kind == 3 else 2 if kind == 2 else 0
                for kind in kinds) == block["edge_count"],
            "section expression dimensions")
    manifest = {name: {key: value for key, value in row.items()
                       if key != "base64"} for name, row in arrays.items()}
    require(block["manifest_sha256"] == digest_obj({"arrays": manifest,
                                                     "roots": block["roots"]}),
            "section expression manifest")
    roots = block["roots"]
    require(isinstance(roots, list) and len(set(roots)) == len(roots) and
            all(isinstance(root, int) and 0 <= root < n for root in roots),
            "section expression roots")
    values: list[Element] = []
    for index in range(n):
        blob = bytes(values_raw[index*width:(index+1)*width])
        recorded: Element = (tuple(blob[:quotient.degree]),
                             tuple(blob[quotient.degree:]))
        kind = kinds[index]
        if kind == 0:
            require(signed[index] == 0 and offsets[index] == offsets[index+1],
                    "section identity payload")
            computed = quotient.identity
        elif kind == 1:
            letter = int(signed[index])
            require(1 <= abs(letter) <= 6 and
                    offsets[index] == offsets[index+1],
                    "section generator payload")
            value = quotient.generators[abs(letter)-1]
            computed = value if letter > 0 else quotient.inverse(value)
        elif kind == 4:
            word = [int(x) for x in letters[offsets[index]:offsets[index+1]]]
            require(len(word) <= CAPS["single_word_or_section_length"] and
                    all(1 <= abs(x) <= 6 for x in word),
                    "section flat word")
            computed = quotient.eval(word)
        elif kind == 3:
            parent = int(left[index])
            require(parent < index and offsets[index] == offsets[index+1],
                    "section inverse topology")
            computed = quotient.inverse(values[parent])
        else:
            require(kind == 2 and int(left[index]) < index and
                    int(right[index]) < index and
                    offsets[index] == offsets[index+1],
                    "section product topology")
            computed = quotient.mul(values[int(left[index])],
                                    values[int(right[index])])
        require(computed == recorded, "section expression canonical binding")
        values.append(recorded)
    reached: set[int] = set()
    pending = list(roots)
    while pending:
        node = pending.pop()
        if node in reached:
            continue
        reached.add(node)
        if kinds[node] == 3:
            pending.append(int(left[node]))
        elif kinds[node] == 2:
            pending.extend((int(left[node]), int(right[node])))
    require(len(reached) == n,
            "section expression unreachable serialized node")
    return values


def evaluate_proof_dag(block: dict[str, Any], expected_names: Sequence[str],
                       leaf_resolver: Any) \
        -> tuple[dict[str, Vector], dict[str, int]]:
    expected_keys = {
        "format", "field", "node_order", "translation_action",
        "section_expressions", "arrays",
        "roots", "node_count", "edge_count", "leaf_count",
        "combination_node_count", "all_serialized_nodes_reachable_from_roots",
        "unreachable_search_nodes_pruned", "expanded_boundary_ledgers_serialized",
        "packed_manifest_sha256",
    }
    require(set(block) == expected_keys and
            block["format"] == "packed-parallel-arrays/v1" and
            block["field"] == 3 and
            block["node_order"] == "one_based_topological" and
            block["translation_action"] == "left" and
            isinstance(block["node_count"], int) and
            1 <= block["node_count"] <= CAPS["provenance_dag_nodes"] and
            isinstance(block["edge_count"], int) and
            0 <= block["edge_count"] <= CAPS["provenance_dag_edges"] and
            isinstance(block["unreachable_search_nodes_pruned"], int) and
            block["unreachable_search_nodes_pruned"] >= 0 and
            block["all_serialized_nodes_reachable_from_roots"] is True and
            block["expanded_boundary_ledgers_serialized"] is False,
            "packed proof DAG header")
    arrays = block["arrays"]
    require(set(arrays) == {"node_kind", "leaf_relator_index",
                            "leaf_translation_element_id", "edge_offsets",
                            "edge_parent_node_id", "edge_coefficient"},
            "packed proof DAG arrays")
    n, e = block["node_count"], block["edge_count"]
    kinds = _decode_packed_array(arrays["node_kind"], "uint8", "B",
                                 CAPS["provenance_dag_nodes"])
    relators = _decode_packed_array(arrays["leaf_relator_index"], "uint16", "H",
                                    CAPS["provenance_dag_nodes"])
    translations = _decode_packed_array(
        arrays["leaf_translation_element_id"], "uint32", "I",
        CAPS["provenance_dag_nodes"])
    offsets = _decode_packed_array(arrays["edge_offsets"], "uint32", "I",
                                   CAPS["provenance_dag_nodes"]+1)
    edge_parents = _decode_packed_array(
        arrays["edge_parent_node_id"], "uint32", "I",
        CAPS["provenance_dag_edges"])
    edge_coefficients = _decode_packed_array(
        arrays["edge_coefficient"], "uint8", "B", CAPS["provenance_dag_edges"])
    require(len(kinds) == len(relators) == len(translations) == n and
            len(offsets) == n+1 and len(edge_parents) ==
            len(edge_coefficients) == e and offsets[0] == 0 and offsets[-1] == e and
            all(offsets[i] <= offsets[i+1] for i in range(n)),
            "packed proof DAG dimensions")
    manifest = {
        name: {key: value for key, value in row.items() if key != "base64"}
        for name, row in arrays.items()
    }
    require(block["packed_manifest_sha256"] ==
            digest_obj({"arrays": manifest, "roots": block["roots"]}),
            "packed proof DAG manifest")

    roots = block["roots"]
    require(isinstance(roots, list) and
            [row.get("name") for row in roots] == list(expected_names) and
            all(set(row) == {"name", "node_id"} and
                isinstance(row["node_id"], int) and 1 <= row["node_id"] <= n
                for row in roots), "packed proof DAG roots/order")
    root_ids = {row["name"]: row["node_id"] for row in roots}
    require(len(root_ids) == len(roots), "packed proof DAG duplicate root")

    # First structural pass: exact backward references and future-use counts.
    use_count = array("I", [0]) * (n+1)
    leaf_count = 0
    for index in range(n):
        checker_deadline("packed proof DAG", force=(index == 0))
        node_id = index+1
        start, stop = int(offsets[index]), int(offsets[index+1])
        if kinds[index] == 1:
            require(start == stop and relators[index] >= 1 and
                    translations[index] >= 1, "packed proof DAG leaf fields")
            leaf_count += 1
        else:
            require(kinds[index] == 2 and relators[index] == 0 and
                    translations[index] == 0 and (stop > start or node_id == 1),
                    "packed proof DAG linear fields")
            seen: set[int] = set()
            for position in range(start, stop):
                parent = int(edge_parents[position])
                coefficient = int(edge_coefficients[position])
                require(1 <= parent < node_id and parent not in seen and
                        coefficient in (1, 2),
                        "packed proof DAG backward reference/coefficient")
                seen.add(parent)
                use_count[parent] += 1
    for node_id in root_ids.values():
        use_count[node_id] += 1
    require(block["leaf_count"] == leaf_count and
            block["combination_node_count"] == n-leaf_count,
            "packed proof DAG accounting")

    # Independent root reachability uses a byte bitmap, never a Python set of
    # millions of IDs.
    reached = bytearray(n+1)
    pending = array("I", root_ids.values())
    reached_count = 0
    while pending:
        node_id = int(pending.pop())
        if reached[node_id]:
            continue
        reached[node_id] = 1
        reached_count += 1
        start, stop = int(offsets[node_id-1]), int(offsets[node_id])
        pending.extend(int(edge_parents[position])
                       for position in range(start, stop))
    require(reached_count == n and all(reached[1:]),
            "packed proof DAG unreachable node")

    # Streaming topological replay.  A parent vector is released immediately
    # after its last edge use; only root holds survive to the end.
    live: dict[int, Vector] = {}
    live_entries = 0
    peak_live_entries = 0
    peak_live_nodes = 0
    replay_start = time.monotonic()
    last_progress = replay_start
    for index in range(n):
        node_id = index+1
        start, stop = int(offsets[index]), int(offsets[index+1])
        if kinds[index] == 1:
            vector = leaf_resolver({
                "relator_index": int(relators[index]),
                "translation_element_id": int(translations[index]),
                "translation_action": "left",
            })
        else:
            vector = {}
            for position in range(start, stop):
                parent = int(edge_parents[position])
                require(parent in live, "packed proof DAG released parent")
                add_scaled(vector, live[parent], int(edge_coefficients[position]))
            for position in range(start, stop):
                parent = int(edge_parents[position])
                require(use_count[parent] > 0, "packed proof DAG use count")
                use_count[parent] -= 1
                if use_count[parent] == 0:
                    live_entries -= len(live[parent])
                    del live[parent]
        require(use_count[node_id] > 0, "packed proof DAG unreferenced inserted node")
        live[node_id] = vector
        live_entries += len(vector)
        peak_live_entries = max(peak_live_entries, live_entries)
        peak_live_nodes = max(peak_live_nodes, len(live))
        now = time.monotonic()
        if (node_id & 4095) == 0 or now-last_progress >= \
                CAPS["progress_interval_seconds"]:
            rss = current_rss_bytes()
            require(rss == 0 or rss < CAPS["producer_soft_rss_bytes"],
                    "checker packed DAG RSS guard")
            print("D972_B345_RELFRAT3_PIVOT_SURGERY_V7_CHECKER_PROGRESS "
                  f"phase=packed_DAG_replay elapsed={now-replay_start:.3f} "
                  f"nodes={node_id} live_nodes={len(live)} "
                  f"live_sparse_entries={live_entries} peak_live_nodes={peak_live_nodes} "
                  f"peak_live_sparse_entries={peak_live_entries} current_rss={rss}",
                  flush=True)
            last_progress = now
    require(all(node_id in live for node_id in root_ids.values()),
            "packed proof DAG root lifetime")
    result = {name: live[node_id] for name, node_id in root_ids.items()}
    require(peak_live_nodes <= n and peak_live_entries >= 0,
            "packed proof DAG streaming accounting")
    return result, root_ids


def validate_certificates(certificates: Sequence[dict[str, Any]],
                          dag_block: dict[str, Any],
                          targets: Sequence[tuple[str, str, list[int]]],
                          e4: Quotient, pb4_columns: Sequence[Vector],
                          by_id: dict[int, Element],
                          reverse: dict[tuple[int, Element], int]) -> set[int]:
    names = [x[0] for x in targets]
    require([x["name"] for x in certificates] == names,
            "boundary certificate order/names")
    referenced: set[int] = set()

    def resolve_leaf(node: dict[str, Any]) -> Vector:
        relator = node["relator_index"]
        translation_id = node["translation_element_id"]
        require(isinstance(relator, int) and 1 <= relator <= len(pb4_columns) and
                translation_id in by_id and
                reverse.get((4, by_id[translation_id])) == translation_id,
                "proof DAG leaf typing")
        referenced.add(translation_id)
        return translate(pb4_columns[relator-1], by_id[translation_id], e4)

    root_vectors, root_ids = evaluate_proof_dag(dag_block, names, resolve_leaf)
    certificate_keys = {
        "name", "kind", "arity", "word", "quotient_identity", "gradient",
        "proof_root_node_id", "proof_system", "gradient_sha256", "fox_membership",
    }
    for cert, (name, kind, word) in zip(certificates, targets):
        require(set(cert) == certificate_keys and
                cert["name"] == name and cert["kind"] == kind and
                cert["arity"] == 4 and cert["word"] == word and
                cert["quotient_identity"] is True and
                cert["proof_root_node_id"] == root_ids[name] and
                cert["proof_system"] == "shared_topological_F3_provenance_DAG",
                f"{name}: typed DAG certificate header")
        gradient, value = fox(word, e4)
        require(value == e4.identity and boundary1(gradient, e4) == {},
                f"{name}: Fox cycle")
        expected_gradient = encode(gradient, 4, reverse)
        require(cert["gradient"] == expected_gradient and
                cert["gradient_sha256"] == digest_obj(expected_gradient) and
                root_vectors[name] == gradient,
                f"{name}: DAG root/gradient")
    return referenced


def validate_terminal(data: dict[str, Any]) -> None:
    token = data.get("terminal_token")
    require(token in TERMINALS and data.get("status") == token, "terminal/status")
    if token == "B345_RELFRAT3_LITERAL_PAIR_PASS":
        require(data.get("claim_classification") == "positive_certificate",
                "positive claim classification")
        require(data["direct_lane"] == {"literal_pair_found": True,
                                        "PB5_branch_constructed": False,
                                        "stop_reason": "FIRST_LITERAL_PAIR_AT_PHI"},
                "positive direct lane")
        require(bool(data.get("selected_pair")) and
                bool(data.get("boundary_certificates")) and
                bool(data.get("boundary_proof_dag")),
                "positive without pair/certificates")
    elif token == "B345_RELFRAT3_SEARCH_INCOMPLETE":
        search = data["search"]
        require(data.get("claim_classification") == "unknown_not_obstruction" and
                data["direct_lane"]["literal_pair_found"] is False and
                data["direct_lane"]["PB5_branch_constructed"] is False and
                search["translates_per_relator"] ==
                CAPS["coefficient_translates_per_relator"] and
                search["candidate_resource_skips"] == [] and
                search["bounded_failure_is_not_nonexistence"] is True and
                search["nonpositive_result_is_obstruction"] is False and
                "no obstruction or nonexistence" in data["reason"],
                "bounded search terminal")
        require("selected_pair" not in data and
                "boundary_certificates" not in data and
                "boundary_proof_dag" not in data,
                "search miss promoted to a pair")
    elif token == "B345_RELFRAT3_UNKNOWN_RESOURCE":
        require(data.get("claim_classification") == "unknown_not_obstruction" and
                data["resource_stop"]["no_mathematical_obstruction_claimed"] is True and
                "selected_pair" not in data and
                "boundary_certificates" not in data and
                "boundary_proof_dag" not in data,
                "resource stop promotion")
        require(isinstance(data["resource_stop"].get("candidate_local"), bool) and
                data["resource_stop"]["cap"] == data["reason"],
                "resource stop exact reason")


def validate_resource_guards(data: dict[str, Any]) -> None:
    block = data["resource_guards"]
    require(set(block) == {
                "seconds", "minutes", "rss_bytes", "rss_gib",
                "external_job_limit_minutes", "safety_margin_minutes", "clock",
                "rss_primary", "rss_portable_fallback", "hit", "hit_reason",
                "last_checked_phase", "check_count", "current_rss_bytes",
                "peak_rss_bytes", "terminal_on_hit", "consulted_in_selftest",
            } and
            block["seconds"] == CAPS["producer_soft_timeout_seconds"] == 18_000 and
            block["minutes"] == 300 and
            block["rss_bytes"] == CAPS["producer_soft_rss_bytes"] and
            block["rss_gib"] == 4.5 and
            block["external_job_limit_minutes"] == 330 and
            block["safety_margin_minutes"] == 30 and
            block["clock"] == "time.monotonic" and
            block["rss_primary"] == "/proc/self/status VmRSS" and
            isinstance(block["rss_portable_fallback"], str) and
            isinstance(block["hit"], bool) and
            (block["hit_reason"] is None or
             isinstance(block["hit_reason"], str) and block["hit_reason"]) and
            isinstance(block["last_checked_phase"], str) and
            block["last_checked_phase"] and
            isinstance(block["check_count"], int) and block["check_count"] >= 0 and
            isinstance(block["current_rss_bytes"], int) and
            isinstance(block["peak_rss_bytes"], int) and
            0 <= block["current_rss_bytes"] <= block["peak_rss_bytes"] and
            block["terminal_on_hit"] == "B345_RELFRAT3_UNKNOWN_RESOURCE" and
            block["consulted_in_selftest"] is False,
            "resource guard contract")
    actual_stop = data["terminal_token"] == "B345_RELFRAT3_UNKNOWN_RESOURCE"
    require(block["hit"] is actual_stop and
            (not actual_stop and block["hit_reason"] is None or
             actual_stop and block["hit_reason"] == data["resource_stop"]["cap"]),
            "resource guard hit/terminal equivalence")


def validate_lru_accounting(row: dict[str, Any], capacity: int) -> None:
    require(set(row) == {"capacity", "size", "peak", "hits", "misses",
                         "evictions", "clears"} and row["capacity"] == capacity and
            all(isinstance(row[key], int) and row[key] >= 0
                for key in ("size", "peak", "hits", "misses", "evictions",
                            "clears")) and
            row["size"] <= row["peak"] <= capacity,
            "bounded LRU accounting")


def _validate_receipt_v3_reference(data: dict[str, Any], q3: dict[str, Any],
                                   q3_path: Path, repo: Path) -> None:
    required_top = {"schema", "status", "terminal_token", "reason", "pins",
                    "source_hashes", "input_q3_terminal", "output_path", "caps",
                    "representation_contract", "claim_classification",
                    "theorem_boundary", "prohibited_work", "resource_guards",
                    "performance"}
    optional_top = {"formula_sha256", "relevant_formula",
                    "relevant_formula_sha256", "matched_quotients",
                    "base_q3_replay", "correction_dictionary",
                    "normalized_inverse_fibre", "search", "direct_lane",
                    "resource_stop", "resource_accounting_at_stop",
                    "quotient_element_registry", "fox_models",
                    "boundary_proof_dag", "selected_pair",
                    "boundary_certificates", "literal_replay"}
    require(required_top <= set(data) and set(data) <= required_top | optional_top,
            "v3 top-level schema/key layout")
    require(data.get("schema") == SCHEMA and data.get("caps") == CAPS,
            "schema/caps")
    require(data["input_q3_terminal"] == q3.get("terminal_token") and
            data["output_path"] == str(OUTPUT_PATH).replace("\\", "/"),
            "input/output binding")
    validate_terminal(data)
    validate_resource_guards(data)
    pins = data["pins"]
    for key, path, sha in (("q3_producer", Q3_PRODUCER, Q3_PRODUCER_SHA),
                           ("q3_checker", Q3_CHECKER, Q3_CHECKER_SHA),
                           ("q3_driver", Q3_DRIVER, Q3_DRIVER_SHA)):
        require(pins[key] == {"path": str(path).replace("\\", "/"),
                              "sha256": sha} and digest_file(repo/path) == sha,
                f"pin {key}")
    require(pins["q3_artifact"] == {"path": str(Q3_ARTIFACT_PATH).replace("\\", "/"),
                                    "sha256": Q3_ARTIFACT_SHA} and
            digest_file(q3_path) == Q3_ARTIFACT_SHA and
            pins["formula_sha256"] == FORMULA_SHA and
            digest_obj(q3["formulas"]) == FORMULA_SHA,
            "artifact/formula pins")
    semantic_v2 = pins["semantic_reference_v2"]
    require(semantic_v2 == {
                "producer": {"path": str(V2_PRODUCER).replace("\\", "/"),
                             "sha256": V2_PRODUCER_SHA},
                "checker": {"path": str(V2_CHECKER).replace("\\", "/"),
                            "sha256": V2_CHECKER_SHA},
                "driver": {"path": str(V2_DRIVER).replace("\\", "/"),
                           "sha256": V2_DRIVER_SHA},
                "role": "frozen v2 mathematics, universe, gates, and search order",
            } and digest_file(repo/V2_PRODUCER) == V2_PRODUCER_SHA and
            digest_file(repo/V2_CHECKER) == V2_CHECKER_SHA and
            digest_file(repo/V2_DRIVER) == V2_DRIVER_SHA,
            "frozen v2 semantic reference")
    semantic = pins["semantic_reference_v1"]
    require(semantic == {
                "producer": {"path": str(V1_PRODUCER).replace("\\", "/"),
                             "sha256": V1_PRODUCER_SHA},
                "checker": {"path": str(V1_CHECKER).replace("\\", "/"),
                            "sha256": V1_CHECKER_SHA},
                "driver": {"path": str(V1_DRIVER).replace("\\", "/"),
                           "sha256": V1_DRIVER_SHA},
                "role": "frozen semantic predicate and search-order reference",
            } and
            digest_file(repo/V1_PRODUCER) == V1_PRODUCER_SHA and
            digest_file(repo/V1_CHECKER) == V1_CHECKER_SHA and
            digest_file(repo/V1_DRIVER) == V1_DRIVER_SHA,
            "frozen v1 semantic reference")
    local_sources = {
        "producer_sha256": digest_file(repo/"search/d972_b345_relfrat3_v3.py"),
        "checker_sha256": digest_file(Path(__file__)),
        "driver_sha256": digest_file(repo/"search/d972_b345_relfrat3_gha_driver_v3.g"),
    }
    require(data["source_hashes"] == local_sources, "new source SHA binding")
    require(data["representation_contract"] == {
                "version": "packed-v3",
                "persistent_element_equality": "exact canonical bytes; never a digest",
                "sparse_keys": "component plus stable zero-based exact element-pool ID",
                "pivot_order": "component then canonical EKey bytes; never insertion ID",
                "BFS_order": "+1..+6,-1..-6 first-seen shortlex",
                "candidate_sections_retained": False,
                "proof_DAG_in_memory": "packed parallel arrays",
                "positive_DAG_serialization": "reachable union as typed little-endian base64 arrays",
                "cache_eviction_semantics": "capacity and eviction order affect speed only, never canonical values or search order",
                "persistent_checkpoint_resume": False,
            }, "v3 representation contract")
    theorem = data["theorem_boundary"]
    require(theorem["Phi3_H4_isolation_required"] is False and
            set(theorem["not_covered"]) == {"nonabelian chief factors", "other primes",
                                              "deeper iteration", "uniform cofinal tower",
                                              "global B4-B"}, "theorem boundary")
    prohibited = data["prohibited_work"]
    require(prohibited == {"relative_ANUPQ_calls": 0,
                            "Reidemeister_Schreier": False,
                            "full_Elements": False,
                            "full_regular_matrices": False,
                            "full_H1_basis_or_rank": False}, "prohibited-work receipt")
    if data["terminal_token"] == "B345_RELFRAT3_UNKNOWN_RESOURCE" and \
            data["resource_stop"].get("candidate_local") is False:
        stop = data["resource_stop"]
        require(stop.get("cap") in {
                    "producer_soft_timeout", "producer_soft_rss",
                    "single_word_or_section_length", "element_pool",
                    "compact_candidate_cache", "compact_candidate_sparse_entries",
                    "section_slp_nodes", "total_sparse_group_ring_keys",
                    "single_sparse_elimination_row", "target_elimination_support",
                    "sparse_pivot_rows", "provenance_dag_nodes",
                    "provenance_dag_edges",
                } and data["reason"] == stop["cap"] and
                stop.get("large_structures_released_before_write") is True and
                stop.get("no_mathematical_obstruction_claimed") is True,
                "global resource-only receipt")
        accounting = data["resource_accounting_at_stop"]
        require(set(accounting) >= {"live", "monitor", "candidate_cache_size",
                                   "candidate_sparse_entries"} and
                accounting["candidate_cache_size"] <=
                4_096 and
                accounting["candidate_sparse_entries"] <=
                1_000_000 and
                accounting["live"]["element_pool"] <= CAPS["element_pool"] and
                accounting["live"]["dag_nodes"] <= CAPS["provenance_dag_nodes"] and
                accounting["live"]["dag_edges"] <= CAPS["provenance_dag_edges"],
                "global resource accounting")
    if "search" not in data:
        stop = data["resource_stop"]
        require(data["terminal_token"] == "B345_RELFRAT3_UNKNOWN_RESOURCE" and
                stop.get("candidate_local") is not True and
                stop.get("cap") in {
                    "producer_soft_timeout", "producer_soft_rss",
                    "single_word_or_section_length", "element_pool",
                    "compact_candidate_cache", "compact_candidate_sparse_entries",
                    "section_slp_nodes",
                    "total_sparse_group_ring_keys", "single_sparse_elimination_row",
                    "target_elimination_support", "sparse_pivot_rows",
                    "provenance_dag_nodes", "provenance_dag_edges",
                } and data["reason"] == stop["cap"] and
                stop.get("large_structures_released_before_write") is True and
                stop.get("no_mathematical_obstruction_claimed") is True,
                "global resource-only receipt")
        if "resource_accounting_at_stop" in data:
            accounting = data["resource_accounting_at_stop"]
            require(set(accounting) >= {"live", "monitor", "candidate_cache_size",
                                       "candidate_sparse_entries"} and
                    accounting["candidate_cache_size"] <=
                    4_096 and
                    accounting["candidate_sparse_entries"] <=
                    1_000_000 and
                    accounting["live"]["element_pool"] <= CAPS["element_pool"] and
                    accounting["live"]["dag_nodes"] <= CAPS["provenance_dag_nodes"] and
                    accounting["live"]["dag_edges"] <= CAPS["provenance_dag_edges"],
                    "resource-stop accounting")
        return
    formula = formula_subset()
    require(data.get("formula_sha256") == FORMULA_SHA and
            data.get("relevant_formula") == formula and
            data.get("relevant_formula_sha256") == digest_obj(formula),
            "relevant formula")
    e3, e4 = reconstruct(q3)
    matched = data["matched_quotients"]
    require(matched["E3"]["coarse_degree"] == e3.degree and
            matched["E4"]["coarse_degree"] == e4.degree and
            "kernel" in matched["J_H"]["definition"] and
            matched["J_Phi"]["identified_with_Phi3_H3"] is False and
            matched["J_Phi"]["correction_membership_required"] is False and
            matched["J_Phi"]["quotient_J_H_over_J_Phi_is_lift_freedom"] is True and
            "intersection" in matched["J_Phi"]["definition"],
            "matched J_H/J_Phi typing")
    validate_base_replay(data, q3, e3, e4)
    require(data["correction_dictionary"] == rebuild_dictionary(q3, e3),
            "correction dictionary/order")
    normalized_inverse, normalized_base_key, _ = \
        rebuild_normalized_inverse_fibre(q3, e4)
    require(data["normalized_inverse_fibre"] == normalized_inverse,
            "normalized exponent-seven inverse fibre")
    # Frozen v2 accounting contract retained as a nonexecuting source-level
    # differential reference; v3's exact packed contract is checked below.
    if False and "search" in data:
        search = data["search"]
        survivor_indices = search["cheap_survivor_indices"]
        rejected_indices = [row["candidate_index"] for row in
                            search["cheap_rejected"]]
        prep_resource_indices = [row["candidate_index"] for row in
                                 search["candidate_resource_skips"]
                                 if row["phase"] == "cheap_candidate_preparation"]
        inverse_cache = search["quotient_inverse_cache"]
        missing_inverse_skips = [row for row in search["candidate_resource_skips"]
                                 if row["reason"] ==
                                 "missing_bounded_inverse_representative"]
        dag_accounting = search["provenance_DAG"]
        dag_accounting_keys = {
            "live_nodes", "live_edges", "peak_nodes", "peak_edges",
            "pivot_payload", "expanded_pivot_ledgers_stored",
            "failed_column_and_candidate_nodes_rolled_back",
            "positive_serialization",
        }
        if data["terminal_token"] == "B345_RELFRAT3_LITERAL_PAIR_PASS":
            dag_accounting_keys |= {
                "serialized_reachable_nodes", "serialized_reachable_edges",
            }
        require(search["method"] ==
                "one shared incremental sparse Gaussian basis with immutable F3 provenance DAG" and
                set(dag_accounting) == dag_accounting_keys and
                search["basis_size"] == search["pivot_count"] and
                0 <= search["pivot_count"] <= CAPS["sparse_pivot_rows"] and
                0 <= search["live_sparse_vector_entries"] <=
                CAPS["total_sparse_group_ring_keys"] and
                0 <= search["max_pivot_vector_support"] <=
                CAPS["total_sparse_group_ring_keys"] and
                0 <= search["max_transient_vector_support"] <=
                CAPS["total_sparse_group_ring_keys"] and
                isinstance(search["elimination_operations"], int) and
                search["elimination_operations"] >= 0 and
                1 <= dag_accounting["live_nodes"] <=
                dag_accounting["peak_nodes"] <= CAPS["provenance_dag_nodes"] and
                0 <= dag_accounting["live_edges"] <=
                dag_accounting["peak_edges"] <= CAPS["provenance_dag_edges"] and
                dag_accounting["pivot_payload"] ==
                "one sparse vector plus one DAG node id" and
                dag_accounting["expanded_pivot_ledgers_stored"] is False and
                dag_accounting["failed_column_and_candidate_nodes_rolled_back"] is True and
                dag_accounting["positive_serialization"] ==
                "root-reachable union only" and
                "live_sparse_entries" not in search and
                "max_ledger_support" not in search and
                search["cheap_quotient_gates_precede_power_inverse"] is True and
                search["raw_power_inverse_removed"] is True and
                search["same_basis_reused_for_all_candidates"] is True and
                search["candidate_order"] ==
                "empty first, then registered correction dictionary order" and
                search["cheap_candidates_evaluated"] ==
                data["correction_dictionary"]["count"] and
                search["cheap_gate_evaluation"] ==
                "direct E4 values without substituted-word materialization" and
                search["full_words_materialized_only_for_cheap_survivors"] is True and
                survivor_indices == sorted(set(survivor_indices)) and
                rejected_indices == sorted(set(rejected_indices)) and
                prep_resource_indices == sorted(set(prep_resource_indices)) and
                set(survivor_indices).isdisjoint(rejected_indices) and
                set(survivor_indices).isdisjoint(prep_resource_indices) and
                set(rejected_indices).isdisjoint(prep_resource_indices) and
                set(survivor_indices + rejected_indices + prep_resource_indices) ==
                set(range(1, data["correction_dictionary"]["count"]+1)) and
                search["all_cheap_survivors_scheduled_from_checkpoint"] == 8 and
                all(x > 0 and (x & (x-1)) == 0
                    for x in search["geometric_translation_checkpoints"]) and
                search["settled_automorphism_order_cache_size"] == 1 and
                inverse_cache == {
                    "key": "exact ordered tuple of six E4 source images",
                    "entries": 1,
                    "hits": inverse_cache["hits"],
                    "misses": inverse_cache["misses"],
                    "tuple_match_count": inverse_cache["hits"],
                    "tuple_mismatch_count": inverse_cache["misses"],
                    "max_inverse_word_length":
                        normalized_inverse["max_inverse_word_length"],
                    "cached_datum": "one pinned normalized exponent-seven full inverse word tuple",
                    "cache_hit_replays_current_ST_in_E4": True,
                    "TS_replay_is_diagnostic_only": True,
                    "different_tuple_is_candidate_local_UNKNOWN": True,
                    "raw_endomorphism_powering_fallback": False,
                    "candidate_relations_gradients_proof_roots_reused": False,
                    "componentwise_Q4_Pi4_inverse_words_combined": False,
                } and
                isinstance(inverse_cache["hits"], int) and
                isinstance(inverse_cache["misses"], int) and
                inverse_cache["hits"] >= 0 and inverse_cache["misses"] >= 0 and
                inverse_cache["misses"] == len(missing_inverse_skips) and
                search["nonpositive_result_is_obstruction"] is False,
                "search cache/performance contract")
    if "search" in data:
        search = data["search"]
        survivor_indices = search["cheap_survivor_indices"]
        rejected_indices = [row["candidate_index"] for row in search["cheap_rejected"]]
        prep_resource_indices = [row["candidate_index"] for row in
                                 search["candidate_resource_skips"]
                                 if row["phase"] == "cheap_candidate_preparation"]
        require(survivor_indices == sorted(set(survivor_indices)) and
                rejected_indices == sorted(set(rejected_indices)) and
                prep_resource_indices == sorted(set(prep_resource_indices)) and
                set(survivor_indices).isdisjoint(rejected_indices) and
                set(survivor_indices).isdisjoint(prep_resource_indices) and
                set(rejected_indices).isdisjoint(prep_resource_indices) and
                set(survivor_indices + rejected_indices + prep_resource_indices) ==
                set(range(1, data["correction_dictionary"]["count"]+1)),
                "packed cheap candidate partition/order")
        dag_accounting = search["provenance_DAG"]
        expected_dag_keys = {
            "live_nodes", "live_edges", "peak_nodes", "peak_edges",
            "packed_arrays", "node_payload_bytes", "edge_payload_bytes",
            "pivot_payload", "expanded_pivot_ledgers_stored",
            "failed_column_and_candidate_nodes_rolled_back", "positive_serialization",
        }
        if data["terminal_token"] == "B345_RELFRAT3_LITERAL_PAIR_PASS":
            expected_dag_keys |= {"serialized_reachable_nodes",
                                  "serialized_reachable_edges"}
        require(set(dag_accounting) == expected_dag_keys and
                dag_accounting["packed_arrays"] is True and
                1 <= dag_accounting["live_nodes"] <= dag_accounting["peak_nodes"] <=
                CAPS["provenance_dag_nodes"] and
                0 <= dag_accounting["live_edges"] <= dag_accounting["peak_edges"] <=
                CAPS["provenance_dag_edges"] and
                dag_accounting["node_payload_bytes"] >= 0 and
                dag_accounting["edge_payload_bytes"] >= 0 and
                dag_accounting["pivot_payload"] ==
                "one packed sparse vector plus one packed DAG node id" and
                dag_accounting["expanded_pivot_ledgers_stored"] is False and
                dag_accounting["failed_column_and_candidate_nodes_rolled_back"] is True and
                dag_accounting["positive_serialization"] ==
                "root-reachable typed little-endian arrays only",
                "packed DAG accounting")
        element_pool = search["element_pool"]
        pool_integrity = search["element_pool_integrity"]
        require(element_pool["capacity"] == CAPS["element_pool"] and
                1 <= element_pool["size"] <= element_pool["peak"] <=
                CAPS["element_pool"] and
                element_pool["packed_width_bytes"] ==
                e4.degree+e4.collector.n and
                element_pool["packed_payload_bytes"] ==
                element_pool["size"]*element_pool["packed_width_bytes"] and
                isinstance(element_pool["hits"], int) and element_pool["hits"] >= 0 and
                isinstance(element_pool["misses"], int) and
                element_pool["misses"] >= element_pool["size"] and
                element_pool["exact_equality"] ==
                "canonical permutation bytes concatenated with PC-coordinate bytes" and
                element_pool["canonical_order"] ==
                "lexicographic canonical packed bytes, identical to EKey=(permutation,PC) tuple order" and
                element_pool["digest_used_as_equality"] is False,
                "exact element pool")
        for name, capacity in (("product_cache", CAPS["element_product_cache"]),
                               ("inverse_cache", CAPS["element_inverse_cache"])):
            row = element_pool[name]
            validate_lru_accounting(row, capacity)
        require(pool_integrity["size"] == pool_integrity["lookup_size"] ==
                element_pool["size"] and pool_integrity["all_unique"] is True and
                pool_integrity["fixed_width_bytes"] == element_pool["packed_width_bytes"] and
                isinstance(pool_integrity["ordered_canonical_payload_sha256"], str) and
                len(pool_integrity["ordered_canonical_payload_sha256"]) == 64 and
                all(ch in "0123456789abcdef" for ch in
                    pool_integrity["ordered_canonical_payload_sha256"]) and
                pool_integrity["digest_is_binding_only_not_equality"] is True and
                pool_integrity["exported_internal_IDs"] is False and
                pool_integrity["positive_external_IDs_are_mapped_by_quotient_element_registry"] is True,
                "element pool uniqueness/canonical encoding receipt")
        lazy = search["lazy_sections"]
        require(lazy["capacity"] == CAPS["section_slp_nodes"] and
                1 <= lazy["live_nodes"] <= lazy["peak_nodes"] <=
                CAPS["section_slp_nodes"] and
                search["translations_used"] <= lazy["bound_elements"] <=
                CAPS["coefficient_translates_per_relator"] and
                lazy["representation"] ==
                "parent element-section node plus signed generator letter",
                "lazy section accounting")
        pc = search["pc_caches"]
        require(pc["unbounded_full_token_word_cache"] is False and
                len(pc["collectors"]) == 2 and
                pc["hits"] == sum(row["hits"] for row in pc["collectors"]) and
                pc["misses"] == sum(row["misses"] for row in pc["collectors"]) and
                pc["evictions"] == sum(row["evictions"] for row in pc["collectors"]),
                "PC cache aggregate")
        for collector in pc["collectors"]:
            validate_lru_accounting(collector["pair_product"],
                                    CAPS["pc_pair_product_cache"])
            validate_lru_accounting(collector["inverse"],
                                    CAPS["pc_inverse_cache"])
            require(collector["unbounded_full_token_word_cache"] is False and
                    collector["policy"] ==
                    "bounded exact pair-product and inverse LRU; no full-word cache" and
                    collector["pair_product"]["capacity"] ==
                    CAPS["pc_pair_product_cache"] and
                    collector["inverse"]["capacity"] == CAPS["pc_inverse_cache"] and
                    0 <= collector["pair_product"]["size"] <=
                    collector["pair_product"]["peak"] <=
                    CAPS["pc_pair_product_cache"] and
                    0 <= collector["inverse"]["size"] <=
                    collector["inverse"]["peak"] <= CAPS["pc_inverse_cache"] and
                    collector["hits"] == collector["pair_product"]["hits"]+
                    collector["inverse"]["hits"] and
                    collector["misses"] == collector["pair_product"]["misses"]+
                    collector["inverse"]["misses"] and
                    collector["evictions"] == collector["pair_product"]["evictions"]+
                    collector["inverse"]["evictions"], "bounded PC collector")
        checkpoints: list[int] = []
        value = 1
        while value <= search["translations_used"]:
            checkpoints.append(value)
            value *= 2
        inverse_cache = search["quotient_inverse_cache"]
        missing_inverse_skips = [row for row in search["candidate_resource_skips"]
                                 if row["reason"] ==
                                 "missing_bounded_inverse_representative"]
        require(search["method"] ==
                "one shared incremental sparse Gaussian basis with packed exact IDs and packed provenance DAG" and
                search["translation_order"] == "BFS shortlex steps +1..+6,-1..-6" and
                search["pivot_order"] ==
                "component then canonical EKey bytes (v2 exact order), never insertion ID" and
                1 <= search["translations_used"] <=
                CAPS["coefficient_translates_per_relator"] and
                search["translates_per_relator"] == search["translations_used"] and
                search["columns_seen"] == 11*search["translations_used"] and
                search["basis_size"] == search["pivot_count"] and
                0 <= search["pivot_count"] <= CAPS["sparse_pivot_rows"] and
                0 <= search["live_sparse_vector_entries"] <=
                CAPS["total_sparse_group_ring_keys"] and
                search["same_basis_reused_for_all_candidates"] is True and
                search["candidate_order"] ==
                "empty first, then registered correction dictionary order" and
                search["cheap_candidates_evaluated"] == 4096 and
                search["cheap_gate_evaluation"] ==
                "direct E4 values without substituted-word retention" and
                search["full_words_materialized_only_transiently_for_cheap_survivors"] is True and
                search["candidate_section_maps_retained"] is False and
                search["compact_candidate_cache_size"] <=
                search["compact_candidate_cache_cap"] == 4_096 and
                search["compact_candidate_sparse_entries"] <=
                search["compact_candidate_sparse_entries_cap"] ==
                1_000_000 and
                search["compact_candidate_cache_payload"] ==
                "names,kinds,packed gradients,quotient value IDs,correction index" and
                isinstance(search["selected_candidate_regenerated_and_exactly_compared"], bool) and
                (data["terminal_token"] != "B345_RELFRAT3_LITERAL_PAIR_PASS" or
                 search["selected_candidate_regenerated_and_exactly_compared"] is True) and
                search["geometric_translation_checkpoints"] == checkpoints and
                search["all_cheap_survivors_scheduled_from_checkpoint"] == 8 and
                search["settled_automorphism_order_cache_size"] == 1 and
                inverse_cache["key"] ==
                "exact ordered tuple of six stable E4 element IDs" and
                inverse_cache["entries"] == inverse_cache["capacity"] == 1 and
                inverse_cache["tuple_match_count"] == inverse_cache["hits"] and
                inverse_cache["tuple_mismatch_count"] == inverse_cache["misses"] and
                inverse_cache["misses"] == len(missing_inverse_skips) and
                inverse_cache["max_inverse_word_length"] ==
                normalized_inverse["max_inverse_word_length"] and
                inverse_cache["raw_endomorphism_powering_fallback"] is False and
                search["cheap_quotient_gates_precede_power_inverse"] is True and
                search["raw_power_inverse_removed"] is True and
                search["bounded_failure_is_not_nonexistence"] is True and
                search["nonpositive_result_is_obstruction"] is False,
                "packed search/cache contract")

    if data["terminal_token"] != "B345_RELFRAT3_LITERAL_PAIR_PASS":
        require("serialized_reachable_nodes" not in
                data["search"]["provenance_DAG"] and
                "serialized_reachable_edges" not in
                data["search"]["provenance_DAG"],
                "nonpositive serialized proof DAG")
        return
    require(data["search"]["provenance_DAG"]["serialized_reachable_nodes"] ==
            data["boundary_proof_dag"]["node_count"] and
            data["search"]["provenance_DAG"]["serialized_reachable_edges"] ==
            data["boundary_proof_dag"]["edge_count"],
            "serialized proof DAG accounting")
    selected = data["selected_pair"]
    dictionary = data["correction_dictionary"]
    index = selected["correction_index"]
    require(1 <= index <= len(dictionary["words"]) and
            selected["correction_word"] == dictionary["words"][index-1] and
            index in data["search"]["cheap_survivor_indices"] and
            index not in {row["candidate_index"] for row in
                          data["search"]["full_quotient_rejected"]} and
            index not in {row["candidate_index"] for row in
                          data["search"]["candidate_resource_skips"]},
            "selected correction/order")
    targets = expected_targets(selected, e4, normalized_inverse,
                               normalized_base_key)
    require(selected["boundary_certificate_names"] == [x[0] for x in targets] and
            all(selected[x] is True for x in
                ("correction_coarse_J_H_all_five_replayed",
                 "correction_finer_J_Phi_membership_not_required",
                 "all_ten_hexagon_coface_memberships_certified",
                 "ordered_A18_pentagon_certified",
                 "S_and_T_relations_certified",
                 "ST_and_TS_generator_compositions_certified")),
            "selected completeness flags")
    by_id, reverse = validate_registry(data["quotient_element_registry"], {3: e3, 4: e4})
    models = validate_fox_models(data["fox_models"], e3, e4, reverse)
    validate_certificates(data["boundary_certificates"],
                          data["boundary_proof_dag"], targets, e4,
                          models[4], by_id, reverse)
    replay = data["literal_replay"]
    require(replay["correction_lift_freedom"] == {
                "coarse_J_H_all_five_cofaces_identity": True,
                "finer_J_Phi_membership_required": False,
                "J_H_mod_J_Phi_coset_is_varied": True,
            } and
            replay["hexagon"]["each_checked_in_all_five_cofaces"] is True and
            replay["pentagon"]["ordered_five_coface_A18_direct_PB4_residual"] is True and
            replay["charming"]["explicit_commutator_product"] is True and
            replay["charming"]["raw_exponent_sums_used_as_criterion"] is False and
            replay["onto"]["two_sided_inverse_on_six_marked_generators"] is True,
            "literal replay flags")


def require_sha256(value: Any, label: str) -> None:
    require(isinstance(value, str) and len(value) == 64 and
            all(ch in "0123456789abcdef" for ch in value), label)


def independent_gradient_binding(name: str, kind: str, gradient: Vector,
                                 value: Element) -> dict[str, Any]:
    digest = hashlib.sha256()
    for (component, element), coefficient in sorted(gradient.items()):
        blob = element_blob(element)
        digest.update(component.to_bytes(1, "little"))
        digest.update(len(blob).to_bytes(2, "little"))
        digest.update(blob)
        digest.update(int(coefficient).to_bytes(1, "little"))
    return {"name": name, "kind": kind, "entry_count": len(gradient),
            "quotient_value_hex": element_blob(value).hex(),
            "canonical_gradient_sha256": digest.hexdigest(),
            "canonical_order": "component then exact canonical E4 bytes",
            "digest_is_binding_only_not_element_equality": True}


def validate_search_prefix(prefix: dict[str, Any],
                           failures: list[list[str]] | None,
                           dictionary_count: int | None) -> None:
    require(set(prefix) == {"cheap", "current", "blocker", "transaction",
                            "structural_cap", "accounting"},
            "bounded prefix keys")
    cheap = prefix["cheap"]
    require(set(cheap) == {"evaluated", "completed", "survivor_count",
                           "survivor_indices_sha256",
                           "evaluated_prefix_sha256", "survivor_prefix_sha256",
                           "current_candidate"} and
            isinstance(cheap["evaluated"], int) and 0 <= cheap["evaluated"] <= 4096 and
            isinstance(cheap["completed"], bool) and
            isinstance(cheap["survivor_count"], int) and
            0 <= cheap["survivor_count"] <= cheap["evaluated"],
            "bounded cheap prefix")
    for key in ("survivor_indices_sha256", "evaluated_prefix_sha256",
                "survivor_prefix_sha256"):
        require_sha256(cheap[key], f"cheap prefix {key}")
    expected_current = None if cheap["completed"] else cheap["evaluated"]+1
    require(cheap["current_candidate"] == expected_current and
            (not cheap["completed"] or dictionary_count is not None and
             cheap["evaluated"] == dictionary_count),
            "cheap evaluated/current prefix")
    if failures is not None:
        count = cheap["evaluated"]
        survivors = [index+1 for index, row in enumerate(failures[:count]) if not row]
        evaluated_digest = hashlib.sha256()
        survivor_digest = hashlib.sha256()
        for index, row in enumerate(failures[:count], 1):
            evaluated_digest.update(canonical_bytes([index, row])+b"\n")
            if not row:
                survivor_digest.update(index.to_bytes(4, "little"))
        require(cheap["survivor_count"] == len(survivors) and
                cheap["survivor_indices_sha256"] == digest_obj(survivors) and
                cheap["evaluated_prefix_sha256"] == evaluated_digest.hexdigest() and
                cheap["survivor_prefix_sha256"] == survivor_digest.hexdigest(),
                "independent cheap evaluated prefix")
    else:
        require(cheap["evaluated"] == cheap["survivor_count"] == 0 and
                cheap["survivor_indices_sha256"] == digest_obj([]) and
                cheap["evaluated_prefix_sha256"] == hashlib.sha256(b"").hexdigest() and
                cheap["survivor_prefix_sha256"] == hashlib.sha256(b"").hexdigest(),
                "pre-dictionary empty cheap prefix")
    current = prefix["current"]
    require(set(current) == {"checkpoint", "correction_index", "target_ordinal",
                             "target_name"} and
            (current["checkpoint"] is None or
             isinstance(current["checkpoint"], int) and current["checkpoint"] > 0) and
            (current["correction_index"] is None or
             isinstance(current["correction_index"], int) and
             1 <= current["correction_index"] <= 4096) and
            (current["target_ordinal"] is None or
             isinstance(current["target_ordinal"], int) and
             current["target_ordinal"] > 0) and
            (current["target_name"] is None or
             isinstance(current["target_name"], str) and current["target_name"]),
            "current candidate prefix")
    blocker = prefix["blocker"]
    require(set(blocker) == {"count", "sha256"} and
            isinstance(blocker["count"], int) and
            0 <= blocker["count"] <= CAPS["blocker_table"],
            "blocker prefix")
    require_sha256(blocker["sha256"], "blocker prefix SHA")
    transaction = prefix["transaction"]
    require(set(transaction) == {"starts", "commits", "rollbacks"} and
            all(isinstance(transaction[key], int) and transaction[key] >= 0
                for key in transaction) and
            transaction["commits"] <= 1 and
            transaction["rollbacks"] <= transaction["starts"],
            "transaction prefix")
    structural = prefix["structural_cap"]
    require(set(structural) == {"hit", "reason", "source"} and
            isinstance(structural["hit"], bool) and
            (not structural["hit"] and structural["reason"] is None and
             structural["source"] is None or
             structural["hit"] and isinstance(structural["reason"], str) and
             structural["reason"] and structural["source"] in
             {"monitor", "registered_structural_cap"}),
            "structural cap prefix")
    accounting = prefix["accounting"]
    require(set(accounting) == {"translations", "basis_pivots",
                                "basis_live_entries", "pool_size", "DAG_nodes",
                                "DAG_edges", "section_nodes", "PC_cache_hits",
                                "PC_cache_misses", "PC_cache_evictions"} and
            all(isinstance(value, int) and value >= 0
                for value in accounting.values()),
            "bounded accounting prefix")


def validate_blocker_trace(search: dict[str, Any], element_width: int) -> None:
    table = search["blocker_table"]
    history = search["blocker_history"]
    introductions = search["pivot_introductions"]
    trace = search["checkpoint_trace"]
    require(len(table) <= CAPS["blocker_table"] and
            len(trace) <= CAPS["transaction_trace_records"] and
            table == sorted(table, key=lambda row: row["candidate_index"]) and
            len({row["candidate_index"] for row in table}) == len(table) and
            search["blocker_table_sha256"] == digest_obj(table) and
            search["blocker_history_sha256"] == digest_obj(history) and
            search["checkpoint_trace_sha256"] == digest_obj(trace),
            "blocker table/history/trace bindings")
    by_history: dict[int, dict[str, Any]] = {}
    for expected_id, row in enumerate(history, 1):
        require(row["history_id"] == expected_id and
                1 <= row["candidate_index"] <= 4096 and
                row["target_ordinal"] >= 1 and
                isinstance(row["target_name"], str) and row["target_name"] and
                1 <= row["component"] <= 6,
                "blocker history row")
        raw_element = bytes.fromhex(row["element_hex"])
        require(len(raw_element) == element_width and
                all(isinstance(x, int) and x > row["failed_checkpoint"]
                    for x in row["skip_checkpoints"]+row["retry_checkpoints"]),
                "blocker checkpoint lists")
        by_history[expected_id] = row
    for intro in introductions:
        require(set(intro) == {"component", "element_hex", "translation_ordinal",
                               "relator_index"} and
                1 <= intro["component"] <= 6 and intro["translation_ordinal"] >= 1 and
                1 <= intro["relator_index"] <= 11 and
                any(row["component"] == intro["component"] and
                    row["element_hex"] == intro["element_hex"] for row in history),
                "watched pivot introduction")
    active: dict[int, dict[str, Any]] = {}
    for row in trace:
        require(isinstance(row.get("checkpoint"), int) and row["checkpoint"] >= 1 and
                1 <= row.get("candidate_index", 0) <= 4096,
                "checkpoint trace row")
        event = row["event"]
        if event == "missing_pivot":
            source = by_history[row["blocker_history_id"]]
            require(source["candidate_index"] == row["candidate_index"] and
                    source["failed_checkpoint"] == row["checkpoint"] and
                    source["target_ordinal"] == row["target_ordinal"] and
                    source["target_name"] == row["target_name"] and
                    source["component"] == row["component"] and
                    source["element_hex"] == row["element_hex"],
                    "missing-pivot trace/history")
            active[row["candidate_index"]] = source
        elif event == "missing_pivot_skip":
            source = active.get(row["candidate_index"])
            require(source is by_history[row["blocker_history_id"]] and
                    row["checkpoint"] in source["skip_checkpoints"] and
                    isinstance(row["pool_element_present"], bool) and
                    row["basis_pivot_present"] is False,
                    "missing-pivot skip theorem")
        elif event == "exact_pivot_retry":
            source = active.get(row["candidate_index"])
            intro = row["matching_introduction"]
            require(source is by_history[row["blocker_history_id"]] and
                    row["checkpoint"] in source["retry_checkpoints"] and
                    source.get("matching_introduction") == intro and
                    intro in introductions and
                    source["failed_checkpoint"] < intro["translation_ordinal"] <=
                    row["checkpoint"] and intro["component"] == source["component"] and
                    intro["element_hex"] == source["element_hex"],
                    "mandatory exact-pivot retry")
            del active[row["candidate_index"]]
        elif event in {"full_quotient_reject", "selected_commit",
                       "permanent_full_quotient_reject_skip"}:
            pass
        else:
            raise Reject(f"unknown checkpoint trace event: {event}")
    require([active[index] for index in sorted(active)] == table,
            "final blocker table replay")


def validate_transaction_search(data: dict[str, Any], search: dict[str, Any],
                                dictionary: dict[str, Any], e4: Quotient,
                                expected_dp: dict[str, Any],
                                dp_failures: list[list[str]],
                                normalized_inverse: dict[str, Any]) -> None:
    actual_dp = search["fixed_context_cheap_DP"]
    require(actual_dp == data["fixed_context_cheap_DP"], "cheap DP duplicate binding")
    semantic_actual = {key: value for key, value in actual_dp.items()
                       if key not in {"runtime_seconds", "PC_cache_delta"}}
    require(semantic_actual == expected_dp and
            isinstance(actual_dp["runtime_seconds"], (int, float)) and
            actual_dp["runtime_seconds"] >= 0 and
            set(actual_dp["PC_cache_delta"]) == {"hits", "misses", "evictions"} and
            all(isinstance(value, int) for value in actual_dp["PC_cache_delta"].values()),
            "independent fixed-context DP")
    require(search["cheap_survivor_indices"] == expected_dp["survivor_indices"] and
            search["cheap_candidates_evaluated"] == dictionary["count"] == 4096,
            "cheap survivor universe")
    comparisons = search["direct_vs_DP_comparisons"]
    require(search["direct_word_replay_count"] == len(comparisons) and
            search["direct_vs_DP_all_equal"] is True,
            "direct replay count")
    for row in comparisons:
        index = row["candidate_index"]
        correction = dictionary["words"][index-1]
        direct = direct_cheap_failures(reduce_word(FIXED_WORD+correction),
                                       correction, e4)
        require(row == {"checkpoint": row["checkpoint"],
                        "candidate_index": index,
                        "DP_failed_gates": dp_failures[index-1],
                        "direct_failed_gates": direct,
                        "equal": True} and
                row["checkpoint"] > 0 and
                (row["checkpoint"] & (row["checkpoint"]-1)) == 0 and
                direct == dp_failures[index-1],
                "direct-versus-DP replay")
    validate_blocker_trace(search, e4.degree+e4.collector.n)
    transaction = search["transaction"]
    require(search["transaction_contract"] == {
                "snapshot_before_complete_candidate_and_first_candidate_pool_intern": True,
                "pool_and_DAG_suffix_rollback": True,
                "element_ID_LRUs_cleared_before_ID_reuse": True,
                "persistent_basis_and_lazy_sections_immutable_during_candidate": True,
                "persistent_generator_and_inverse_tuple_anchors_replayed": True,
                "PC_collector_caches_store_canonical_coordinates_not_pool_IDs": True,
                "failed_candidate_gradients_retained": False,
            }, "transaction implementation contract")
    require(set(transaction) == {"starts", "commits", "rollbacks",
                                 "blocker_skips", "blocker_retries",
                                 "target_gradients_generated",
                                 "early_target_failures",
                                 "full_quotient_rejections",
                                 "max_transient_sparse_entries",
                                 "total_transient_sparse_entries"} and
            all(isinstance(value, int) and value >= 0
                for value in transaction.values()),
            "transaction accounting keys")
    outcomes = [row for row in search["checkpoint_trace"]
                if row["event"] in {"missing_pivot", "full_quotient_reject",
                                    "selected_commit"}]
    require([(row["checkpoint"], row["candidate_index"]) for row in comparisons] ==
            [(row["checkpoint"], row["candidate_index"]) for row in outcomes] and
            transaction["starts"] == len(outcomes) == len(comparisons) and
            transaction["rollbacks"] ==
            sum(row["event"] != "selected_commit" for row in outcomes) and
            transaction["commits"] ==
            sum(row["event"] == "selected_commit" for row in outcomes) and
            transaction["early_target_failures"] ==
            sum(row["event"] == "missing_pivot" for row in outcomes) and
            transaction["full_quotient_rejections"] ==
            len(search["full_quotient_rejected"]) and
            transaction["target_gradients_generated"] ==
            sum(row["target_gradients_generated"] for row in outcomes) and
            transaction["total_transient_sparse_entries"] ==
            sum(row["transient_sparse_entries"] for row in outcomes) and
            transaction["max_transient_sparse_entries"] ==
            max([0]+[row["peak_transient_sparse_entries"] for row in outcomes]) and
            transaction["blocker_skips"] ==
            sum(row["event"] == "missing_pivot_skip"
                for row in search["checkpoint_trace"]) and
            transaction["blocker_retries"] ==
            sum(row["event"] == "exact_pivot_retry"
                for row in search["checkpoint_trace"]) and
            transaction["max_transient_sparse_entries"] <=
            transaction["total_transient_sparse_entries"],
            "transaction trace totals")
    checkpoints: list[int] = []
    value = 1
    while value <= search["translations_used"]:
        checkpoints.append(value)
        value *= 2
    require(search["method"] ==
            "shared incremental sparse basis plus candidate-local transactional target streaming" and
            search["translation_order"] == "BFS shortlex steps +1..+6,-1..-6" and
            search["pivot_order"] ==
            "component then canonical EKey bytes (v2 exact order), never insertion ID" and
            search["candidate_order"] ==
            "checkpoint-major; registered correction order within each checkpoint" and
            search["geometric_translation_checkpoints"] == checkpoints and
            search["all_cheap_survivors_scheduled_from_checkpoint"] == 8 and
            search["persistent_candidate_cache_size"] == 0 and
            search["persistent_candidate_gradient_entries"] == 0 ==
            CAPS["persistent_candidate_gradient_entries"] and
            search["candidate_target_streaming"] is True and
            search["candidate_resource_skips"] == [] and
            search["candidate_local_resource_stop_is_global_UNKNOWN"] is True and
            search["same_basis_reused_for_all_candidates"] is True and
            search["columns_seen"] == 11*search["translations_used"] and
            search["basis_size"] == search["pivot_count"] and
            0 <= search["pivot_count"] <= CAPS["sparse_pivot_rows"] and
            0 <= search["live_sparse_vector_entries"] <=
            CAPS["total_sparse_group_ring_keys"] and
            search["selected_candidate_regenerated_and_exactly_compared"] is
            (data["terminal_token"] == "B345_RELFRAT3_LITERAL_PAIR_PASS") and
            search["bounded_failure_is_not_nonexistence"] is True and
            search["nonpositive_result_is_obstruction"] is False,
            "transactional search contract")
    inverse = search["quotient_inverse_cache"]
    require(search["settled_automorphism_order_cache_size"] == 1 and
            inverse["key"] == "exact ordered tuple of six stable E4 element IDs" and
            inverse["entries"] == inverse["capacity"] == 1 and
            inverse["tuple_match_count"] == inverse["hits"] and
            inverse["tuple_mismatch_count"] == inverse["misses"] and
            inverse["max_inverse_word_length"] ==
            normalized_inverse["max_inverse_word_length"] and
            inverse["raw_endomorphism_powering_fallback"] is False,
            "normalized inverse cache")


def validate_receipt(data: dict[str, Any], q3: dict[str, Any], q3_path: Path,
                     repo: Path) -> None:
    required_top = {"schema", "status", "terminal_token", "reason", "pins",
                    "source_hashes", "input_q3_terminal", "output_path", "caps",
                    "representation_contract", "claim_classification",
                    "theorem_boundary", "prohibited_work", "resource_guards",
                    "performance", "bounded_search_prefix"}
    optional_top = {"formula_sha256", "relevant_formula",
                    "relevant_formula_sha256", "matched_quotients",
                    "base_q3_replay", "correction_dictionary",
                    "normalized_inverse_fibre", "fixed_context_cheap_DP",
                    "search", "direct_lane", "resource_stop",
                    "resource_accounting_at_stop", "quotient_element_registry",
                    "fox_models", "boundary_proof_dag", "selected_pair",
                    "boundary_certificates", "literal_replay", "blocker_table",
                    "blocker_history", "checkpoint_trace",
                    "direct_vs_DP_comparisons"}
    require(required_top <= set(data) and set(data) <= required_top | optional_top,
            "v4 top-level schema/key layout")
    require(data["schema"] == SCHEMA and data["caps"] == CAPS and
            data["input_q3_terminal"] == q3.get("terminal_token") and
            data["output_path"] == str(OUTPUT_PATH).replace("\\", "/"),
            "v4 schema/caps/input/output")
    validate_terminal(data)
    validate_resource_guards(data)
    pins = data["pins"]
    for key, path, sha in (("q3_producer", Q3_PRODUCER, Q3_PRODUCER_SHA),
                           ("q3_checker", Q3_CHECKER, Q3_CHECKER_SHA),
                           ("q3_driver", Q3_DRIVER, Q3_DRIVER_SHA)):
        require(pins[key] == {"path": str(path).replace("\\", "/"),
                              "sha256": sha} and digest_file(repo/path) == sha,
                f"pin {key}")
    require(pins["q3_artifact"] == {
                "path": str(Q3_ARTIFACT_PATH).replace("\\", "/"),
                "sha256": Q3_ARTIFACT_SHA} and
            digest_file(q3_path) == Q3_ARTIFACT_SHA and
            pins["formula_sha256"] == FORMULA_SHA and
            digest_obj(q3["formulas"]) == FORMULA_SHA,
            "q3 artifact/formula pins")
    for key, producer, producer_sha, checker, checker_sha, driver, driver_sha, role in (
            ("semantic_reference_v3", V3_PRODUCER, V3_PRODUCER_SHA,
             V3_CHECKER, V3_CHECKER_SHA, V3_DRIVER, V3_DRIVER_SHA,
             "frozen packed-v3 semantics and positive-certificate reference"),
            ("semantic_reference_v2", V2_PRODUCER, V2_PRODUCER_SHA,
             V2_CHECKER, V2_CHECKER_SHA, V2_DRIVER, V2_DRIVER_SHA,
             "frozen v2 mathematics, universe, gates, and search order"),
            ("semantic_reference_v1", V1_PRODUCER, V1_PRODUCER_SHA,
             V1_CHECKER, V1_CHECKER_SHA, V1_DRIVER, V1_DRIVER_SHA,
             "frozen semantic predicate and search-order reference")):
        expected = {"producer": {"path": str(producer).replace("\\", "/"),
                                  "sha256": producer_sha},
                    "checker": {"path": str(checker).replace("\\", "/"),
                                 "sha256": checker_sha},
                    "driver": {"path": str(driver).replace("\\", "/"),
                                "sha256": driver_sha}, "role": role}
        require(pins[key] == expected and digest_file(repo/producer) == producer_sha and
                digest_file(repo/checker) == checker_sha and
                digest_file(repo/driver) == driver_sha, f"{key} pin")
    local_sources = {
        "producer_sha256": digest_file(repo/"search/d972_b345_relfrat3_v4.py"),
        "checker_sha256": digest_file(Path(__file__)),
        "driver_sha256": digest_file(repo/"search/d972_b345_relfrat3_gha_driver_v4.g"),
    }
    require(data["source_hashes"] == local_sources, "v4 source SHA binding")
    representation = data["representation_contract"]
    require(representation == {
                "version": "transactional-packed-v4",
                "persistent_element_equality": "exact canonical bytes; never a digest",
                "sparse_keys": "component plus stable zero-based exact element-pool ID",
                "pivot_order": "component then canonical EKey bytes; never insertion ID",
                "BFS_order": "+1..+6,-1..-6 first-seen shortlex",
                "candidate_sections_retained": False,
                "candidate_gradients_retained_across_checkpoints": False,
                "candidate_transaction": "exact element-pool and provenance-DAG suffix rollback",
                "missing_pivot_blocker": "target ordinal, component, canonical E4 bytes",
                "proof_DAG_in_memory": "packed parallel arrays",
                "positive_DAG_serialization": "reachable union as typed little-endian base64 arrays",
                "cache_eviction_semantics": "capacity and eviction order affect speed only, never canonical values or search order",
                "persistent_checkpoint_resume": False,
            }, "v4 representation contract")
    require(data["prohibited_work"] == {"relative_ANUPQ_calls": 0,
                                          "Reidemeister_Schreier": False,
                                          "full_Elements": False,
                                          "full_regular_matrices": False,
                                          "full_H1_basis_or_rank": False},
            "prohibited-work receipt")
    theorem = data["theorem_boundary"]
    require(theorem["Phi3_H4_isolation_required"] is False and
            "global B4-B" in theorem["not_covered"], "theorem boundary")

    dictionary: dict[str, Any] | None = None
    e3: Quotient | None = None
    e4: Quotient | None = None
    expected_dp: dict[str, Any] | None = None
    dp_failures: list[list[str]] | None = None
    if "correction_dictionary" in data:
        e3, e4 = reconstruct(q3)
        formula = formula_subset()
        require(data["formula_sha256"] == FORMULA_SHA and
                data["relevant_formula"] == formula and
                data["relevant_formula_sha256"] == digest_obj(formula),
                "relevant formula")
        validate_base_replay(data, q3, e3, e4)
        dictionary = rebuild_dictionary(q3, e3)
        require(data["correction_dictionary"] == dictionary,
                "dictionary provenance/order")
        expected_dp, dp_failures = rebuild_fixed_context_dp(dictionary, e4)
    validate_search_prefix(data["bounded_search_prefix"], dp_failures,
                           None if dictionary is None else dictionary["count"])

    if data["terminal_token"] == "B345_RELFRAT3_UNKNOWN_RESOURCE":
        stop = data["resource_stop"]
        require(stop["cap"] in RESOURCE_REASONS and stop["cap"] == data["reason"] and
                stop["large_structures_released_before_write"] is True and
                stop["no_mathematical_obstruction_claimed"] is True and
                data["bounded_search_prefix"]["structural_cap"] == {
                    "hit": True, "reason": stop["cap"],
                    "source": ("monitor" if stop["cap"] in
                               {"producer_soft_timeout", "producer_soft_rss"}
                               else "registered_structural_cap")},
                "resource terminal/prefix")
        accounting = data["resource_accounting_at_stop"]
        require(set(accounting) >= {"live", "monitor", "transaction",
                                    "bounded_search_prefix"} and
                accounting["bounded_search_prefix"] ==
                data["bounded_search_prefix"] and
                accounting["live"]["element_pool"] <= CAPS["element_pool"] and
                accounting["live"]["dag_nodes"] <= CAPS["provenance_dag_nodes"] and
                accounting["live"]["dag_edges"] <= CAPS["provenance_dag_edges"] and
                data["bounded_search_prefix"]["blocker"] == {
                    "count": len(data["blocker_table"]),
                    "sha256": digest_obj(data["blocker_table"])},
                "resource bounded accounting")
        return

    require(dictionary is not None and e3 is not None and e4 is not None and
            expected_dp is not None and dp_failures is not None and
            data["fixed_context_cheap_DP"]["complete"] is True,
            "complete-search DP prerequisites")
    normalized_inverse, normalized_base_key, _ = \
        rebuild_normalized_inverse_fibre(q3, e4)
    require(data["normalized_inverse_fibre"] == normalized_inverse,
            "normalized inverse fibre")
    search = data["search"]
    validate_transaction_search(data, search, dictionary, e4, expected_dp,
                                dp_failures, normalized_inverse)
    prefix = data["bounded_search_prefix"]
    require(prefix["cheap"]["completed"] is True and
            prefix["blocker"] == {"count": len(search["blocker_table"]),
                                   "sha256": digest_obj(search["blocker_table"])} and
            prefix["transaction"] == {
                "starts": search["transaction"]["starts"],
                "commits": search["transaction"]["commits"],
                "rollbacks": search["transaction"]["rollbacks"]} and
            prefix["structural_cap"] == {"hit": False, "reason": None,
                                          "source": None},
            "complete terminal prefix binding")
    dag_accounting = search["provenance_DAG"]
    expected_dag_keys = {"live_nodes", "live_edges", "peak_nodes", "peak_edges",
                         "packed_arrays", "node_payload_bytes", "edge_payload_bytes",
                         "pivot_payload", "expanded_pivot_ledgers_stored",
                         "failed_column_and_candidate_nodes_rolled_back",
                         "positive_serialization"}
    if data["terminal_token"] == "B345_RELFRAT3_LITERAL_PAIR_PASS":
        expected_dag_keys |= {"serialized_reachable_nodes", "serialized_reachable_edges"}
    require(set(dag_accounting) == expected_dag_keys and
            dag_accounting["packed_arrays"] is True and
            1 <= dag_accounting["live_nodes"] <= dag_accounting["peak_nodes"] <=
            CAPS["provenance_dag_nodes"] and
            0 <= dag_accounting["live_edges"] <= dag_accounting["peak_edges"] <=
            CAPS["provenance_dag_edges"] and
            dag_accounting["failed_column_and_candidate_nodes_rolled_back"] is True,
            "packed DAG accounting")
    pool = search["element_pool"]
    require(pool["capacity"] == CAPS["element_pool"] and
            1 <= pool["size"] <= pool["peak"] <= CAPS["element_pool"] and
            pool["packed_width_bytes"] == e4.degree+e4.collector.n and
            pool["packed_payload_bytes"] == pool["size"]*pool["packed_width_bytes"] and
            pool["transaction_rollbacks"] == search["transaction"]["rollbacks"] and
            pool["transaction_commits"] == search["transaction"]["commits"] and
            pool["rollback_lru_clears"] == 2*pool["transaction_rollbacks"] and
            pool["rollback_suffix_removed"] >= pool["max_rollback_suffix"] >= 0,
            "transactional element pool")
    validate_lru_accounting(pool["product_cache"], CAPS["element_product_cache"])
    validate_lru_accounting(pool["inverse_cache"], CAPS["element_inverse_cache"])
    integrity = search["element_pool_integrity"]
    require(integrity["size"] == integrity["lookup_size"] == pool["size"] and
            integrity["all_unique"] is True and
            integrity["fixed_width_bytes"] == pool["packed_width_bytes"],
            "pool integrity")
    require_sha256(integrity["ordered_canonical_payload_sha256"],
                   "pool binding SHA")
    lazy = search["lazy_sections"]
    require(lazy["capacity"] == CAPS["section_slp_nodes"] and
            1 <= lazy["live_nodes"] <= lazy["peak_nodes"] <= CAPS["section_slp_nodes"] and
            search["translations_used"] <= lazy["bound_elements"] <=
            CAPS["coefficient_translates_per_relator"], "lazy BFS sections")
    pc = search["pc_caches"]
    require(pc["unbounded_full_token_word_cache"] is False and
            len(pc["collectors"]) == 2 and
            pc["hits"] == sum(row["hits"] for row in pc["collectors"]) and
            pc["misses"] == sum(row["misses"] for row in pc["collectors"]) and
            pc["evictions"] == sum(row["evictions"] for row in pc["collectors"]),
            "PC cache aggregate")
    for collector in pc["collectors"]:
        validate_lru_accounting(collector["pair_product"], CAPS["pc_pair_product_cache"])
        validate_lru_accounting(collector["inverse"], CAPS["pc_inverse_cache"])

    if data["terminal_token"] != "B345_RELFRAT3_LITERAL_PAIR_PASS":
        require(search["translations_used"] == CAPS["coefficient_translates_per_relator"] and
                "serialized_reachable_nodes" not in dag_accounting and
                search["transaction"]["commits"] == 0,
                "exhausted incomplete search")
        return
    require(dag_accounting["serialized_reachable_nodes"] ==
            data["boundary_proof_dag"]["node_count"] and
            dag_accounting["serialized_reachable_edges"] ==
            data["boundary_proof_dag"]["edge_count"] and
            search["transaction"]["commits"] == 1,
            "positive DAG/commit")
    selected = data["selected_pair"]
    index = selected["correction_index"]
    require(1 <= index <= dictionary["count"] and
            selected["correction_word"] == dictionary["words"][index-1] and
            index in expected_dp["survivor_indices"] and
            index not in {row["candidate_index"]
                          for row in search["full_quotient_rejected"]},
            "selected correction/order")
    targets = expected_targets(selected, e4, normalized_inverse, normalized_base_key)
    require(selected["boundary_certificate_names"] == [row[0] for row in targets],
            "selected target names")
    by_id, reverse = validate_registry(data["quotient_element_registry"], {3: e3, 4: e4})
    models = validate_fox_models(data["fox_models"], e3, e4, reverse)
    validate_certificates(data["boundary_certificates"], data["boundary_proof_dag"],
                          targets, e4, models[4], by_id, reverse)
    bindings = []
    for name, kind, word in targets:
        gradient, value = fox(word, e4)
        bindings.append(independent_gradient_binding(name, kind, gradient, value))
    require(search["selected_gradient_bindings"] == bindings,
            "selected canonical gradient regeneration")
    replay = data["literal_replay"]
    require(replay["correction_lift_freedom"]["coarse_J_H_all_five_cofaces_identity"] is True and
            replay["hexagon"]["each_checked_in_all_five_cofaces"] is True and
            replay["pentagon"]["ordered_five_coface_A18_direct_PB4_residual"] is True and
            replay["charming"]["explicit_commutator_product"] is True and
            replay["onto"]["two_sided_inverse_on_six_marked_generators"] is True,
            "positive literal replay")


def fixed_target_split(e4: Quotient, normalized: dict[str, Any]) \
        -> tuple[list[tuple[str, str, list[int]]],
                 list[tuple[str, str, list[int]]]]:
    f: list[int] = list(FIXED_WORD)
    c34 = cofaces(3)
    targets: list[tuple[str, str, list[int]]] = [
        (f"charming_error_coface_{i}", "charming", []) for i in range(5)]
    for hindex, residual in enumerate(hexagon_words(f), 1):
        source = embed_f2(residual)
        for slot, mapping in enumerate(c34):
            targets.append((f"hexagon_{hindex}_coface_{slot}", "hexagon",
                            substitute(source, mapping)))
    targets.append(("ordered_A18_pentagon", "pentagon", pentagon_word(f)))
    source_words_fixed = source_words(f)
    inverse_words = normalized["selected_inverse_words"]
    st, ts = two_sided_residuals(source_words_fixed, inverse_words)
    for index, relator in enumerate(pure_relations(4), 1):
        targets.append((f"S_relation_{index}", "endomorphism_relation",
                        substitute(relator, source_words_fixed)))
        targets.append((f"T_relation_{index}", "endomorphism_relation",
                        substitute(relator, inverse_words)))
    targets += [(f"ST_generator_{i+1}", "onto_two_sided_inverse", word)
                for i, word in enumerate(st)]
    targets += [(f"TS_generator_{i+1}", "onto_two_sided_inverse", word)
                for i, word in enumerate(ts)]
    acceptance = [row for row in targets
                  if not row[0].startswith("T_relation_") and
                  not row[0].startswith("TS_generator_")]
    diagnostics = [row for row in targets
                   if row[0].startswith("T_relation_") or
                   row[0].startswith("TS_generator_")]
    require(len(targets) == 50 and len(acceptance) == 33 and
            len(diagnostics) == 17 and
            acceptance[5][0] == "hexagon_1_coface_0" and
            all(e4.eval(word) == e4.identity for _, _, word in acceptance),
            "corrected fixed target order/acceptance quotient identities")
    return acceptance, diagnostics


def fixed_targets(e4: Quotient, normalized: dict[str, Any]) \
        -> list[tuple[str, str, list[int]]]:
    return fixed_target_split(e4, normalized)[0]


class ReplayPool:
    """Independent canonical-byte interning for the v7 sparse replay."""

    def __init__(self, quotient: Quotient) -> None:
        self.q = quotient
        self.width = quotient.degree + quotient.collector.n
        self.values: list[bytes] = []
        self.ids: dict[bytes, int] = {}
        self.product: OrderedDict[tuple[int, int], int] = OrderedDict()
        self.inverses: OrderedDict[int, int] = OrderedDict()
        self.identity = self.intern(quotient.identity)
        self.generators = [self.intern(value) for value in quotient.generators]
        self.inverse_generators = [self.inverse_id(value)
                                   for value in self.generators]

    def pack(self, value: Element) -> bytes:
        blob = bytes(value[0]) + bytes(value[1])
        require(len(blob) == self.width, "checker replay element width")
        return blob

    def unpack(self, blob: bytes) -> Element:
        require(isinstance(blob, bytes) and len(blob) == self.width,
                "checker replay canonical element")
        return (tuple(blob[:self.q.degree]),
                tuple(blob[self.q.degree:]))

    def intern(self, value: Element) -> int:
        blob = self.pack(value)
        old = self.ids.get(blob)
        if old is not None:
            return old
        require(len(self.values) < CAPS["element_pool"],
                "checker replay element pool cap")
        identifier = len(self.values)
        self.values.append(blob)
        self.ids[blob] = identifier
        return identifier

    def value(self, identifier: int) -> Element:
        require(0 <= identifier < len(self.values), "checker replay element id")
        return self.unpack(self.values[identifier])

    def mul_id(self, left: int, right: int) -> int:
        key = (left, right)
        old = self.product.get(key)
        if old is not None:
            self.product.move_to_end(key)
            return old
        answer = self.intern(self.q.mul(self.value(left), self.value(right)))
        if len(self.product) >= CAPS["element_product_cache"]:
            self.product.popitem(last=False)
        self.product[key] = answer
        return answer

    def inverse_id(self, value: int) -> int:
        old = self.inverses.get(value)
        if old is not None:
            self.inverses.move_to_end(value)
            return old
        answer = self.intern(self.q.inverse(self.value(value)))
        if len(self.inverses) >= CAPS["element_inverse_cache"]:
            self.inverses.popitem(last=False)
        self.inverses[value] = answer
        return answer

    def pivot_order(self, key: int) -> tuple[int, bytes]:
        component, identifier = replay_unpack_key(key)
        return component, self.values[identifier]

    def checkpoint(self) -> int:
        return len(self.values)

    def rollback(self, checkpoint: int) -> int:
        require(0 <= checkpoint <= len(self.values),
                "checker replay pool checkpoint")
        removed = len(self.values)-checkpoint
        for identifier in range(len(self.values)-1, checkpoint-1, -1):
            blob = self.values[identifier]
            require(self.ids.get(blob) == identifier,
                    "checker replay pool rollback exact binding")
            del self.ids[blob]
        del self.values[checkpoint:]
        self.product.clear()
        self.inverses.clear()
        require(len(self.ids) == len(self.values) == checkpoint,
                "checker replay pool rollback uniqueness/checkpoint")
        return removed


def seed_replay_source_anchors(
        pool: ReplayPool, frozen_source_tuple: Sequence[Element]) \
        -> tuple[int, ...]:
    """Mirror the producer's six persistent source-value interns exactly."""
    require(len(frozen_source_tuple) == 6,
            "checker replay frozen source anchor count")
    return tuple(pool.intern(value) for value in frozen_source_tuple)


def transactional_replay_probe(pool: ReplayPool, probe: Any) -> Any:
    """Run a read-only target probe and discard every transient pool value."""
    require(callable(probe), "checker replay transactional probe callable")
    checkpoint = pool.checkpoint()
    try:
        return probe()
    finally:
        pool.rollback(checkpoint)


def replay_pack_key(component: int, identifier: int) -> int:
    require(1 <= component <= 6 and 0 <= identifier < CAPS["element_pool"],
            "checker packed key")
    return identifier*8 + component-1


def replay_unpack_key(key: int) -> tuple[int, int]:
    require(isinstance(key, int) and key >= 0 and key % 8 < 6,
            "checker packed key decode")
    return key % 8 + 1, key//8


def replay_add(vector: dict[int, int], key: int, coefficient: int) -> None:
    value = (vector.get(key, 0)+coefficient) % 3
    if value:
        vector[key] = value
    else:
        vector.pop(key, None)


def replay_add_scaled(target: dict[int, int], source: dict[int, int],
                      coefficient: int) -> None:
    for key, value in source.items():
        replay_add(target, key, coefficient*value)


def replay_fox_packed(word: Sequence[int], pool: ReplayPool) \
        -> tuple[dict[int, int], int]:
    prefix = pool.identity
    gradient: dict[int, int] = {}
    for letter in word:
        component = abs(letter)
        if letter > 0:
            replay_add(gradient, replay_pack_key(component, prefix), 1)
            prefix = pool.mul_id(prefix, pool.generators[component-1])
        else:
            prefix = pool.mul_id(prefix,
                                 pool.inverse_generators[component-1])
            replay_add(gradient, replay_pack_key(component, prefix), 2)
    return gradient, prefix


def fox_with_sections(word: Sequence[int], quotient: Quotient) \
        -> tuple[Vector, Element, dict[Element, list[int]]]:
    prefix = quotient.identity
    prefix_word: list[int] = []
    gradient: Vector = {}
    sections: dict[Element, list[int]] = {prefix: []}
    for letter in word:
        component = abs(letter)
        if letter > 0:
            add(gradient, (component, prefix), 1)
            sections.setdefault(prefix, list(prefix_word))
            prefix = quotient.mul(prefix, quotient.generators[component-1])
            prefix_word = reduce_word(prefix_word + [letter])
        else:
            prefix = quotient.mul(prefix,
                                  quotient.inverse_generators[component-1])
            prefix_word = reduce_word(prefix_word + [letter])
            add(gradient, (component, prefix), 2)
            sections.setdefault(prefix, list(prefix_word))
    return gradient, prefix, sections


class ReplayBasis:
    def __init__(self, pool: ReplayPool,
                 columns: list[dict[int, int]]) -> None:
        self.pool = pool
        self.columns = columns
        self.rows: dict[int, dict[int, int]] = {}
        self.columns_seen = 0
        self.dependent = 0
        self.live_entries = 0

    def pivot(self, vector: dict[int, int]) -> int:
        return min(vector, key=self.pool.pivot_order)

    def add_column(self, relator: int, translation: int) -> bool:
        vector: dict[int, int] = {}
        for key, coefficient in self.columns[relator-1].items():
            component, element = replay_unpack_key(key)
            replay_add(vector, replay_pack_key(
                component, self.pool.mul_id(translation, element)), coefficient)
        while vector:
            pivot = self.pivot(vector)
            old = self.rows.get(pivot)
            if old is None:
                factor = 1 if vector[pivot] == 1 else 2
                if factor == 2:
                    vector = {key: (2*value) % 3
                              for key, value in vector.items()}
                require(self.live_entries + len(vector) <=
                        CAPS["total_sparse_group_ring_keys"],
                        "checker replay sparse cap")
                require(len(self.rows) < CAPS["sparse_pivot_rows"],
                        "checker replay pivot cap")
                self.rows[pivot] = vector
                self.live_entries += len(vector)
                self.columns_seen += 1
                return True
            coefficient = vector[pivot]
            replay_add_scaled(vector, old, -coefficient)
        self.columns_seen += 1
        self.dependent += 1
        return False

    def solve(self, target: dict[int, int]) -> int | None:
        vector = dict(target)
        while vector:
            pivot = self.pivot(vector)
            old = self.rows.get(pivot)
            if old is None:
                return pivot
            replay_add_scaled(vector, old, -vector[pivot])
        return None


def replay_translation_bfs(pool: ReplayPool, cap: int) -> Iterable[int]:
    steps = pool.generators + pool.inverse_generators
    seen = {pool.identity}
    queue: deque[int] = deque([pool.identity])
    while queue and len(seen) <= cap:
        value = queue.popleft()
        yield value
        if len(seen) == cap:
            continue
        for step in steps:
            child = pool.mul_id(value, step)
            if child not in seen:
                seen.add(child)
                queue.append(child)
                if len(seen) == cap:
                    break


def checker_base_occurrences(e4: Quotient) \
        -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    public: list[dict[str, Any]] = []
    private: list[dict[str, Any]] = []
    width = e4.degree+e4.collector.n
    for relator_index, relator in enumerate(pure_relations(4), 1):
        gradient, value, sections = fox_with_sections(relator, e4)
        require(value == e4.identity and boundary1(gradient, e4) == {},
                "checker base D2 replay")
        ordered = sorted(gradient.items(), key=lambda item: (
            item[0][0], bytes(item[0][1][0])+bytes(item[0][1][1])))
        for (component, element), coefficient in ordered:
            blob = bytes(element[0])+bytes(element[1])
            require(len(blob) == width and element in sections,
                    "checker base support section")
            row = {
                "relator_index": relator_index,
                "component": component, "coefficient": coefficient,
                "element_hex": blob.hex(),
                "section_word": sections[element],
            }
            public.append(row)
            private.append({**row, "_value": element})
    return public, private


###############################################################################
# Independent typed WordExpr and left-Fox replay for the v8 scan.
###############################################################################


class CheckWordExpr:
    """Checker-owned exact expression DAG; no producer helper is imported."""

    NAMES = {1: "IDENTITY", 2: "FLAT_WORD", 3: "PRODUCT",
             4: "INVERSE", 5: "SUBSTITUTE_WORD"}

    def __init__(self) -> None:
        self.op: list[int] = []
        self.rank: list[int] = []
        self.words: list[tuple[int, ...]] = []
        self.children: list[tuple[int, ...]] = []
        self.counts: list[int] = []
        self.index: dict[tuple[Any, ...], int] = {}
        self.edges = 0
        self.flat_leaves = 0
        self.sub_cache: dict[tuple[int, tuple[int, ...]], int] = {}

    def add(self, op: int, rank: int, word: Sequence[int],
            children: Sequence[int], count: int) -> int:
        word_t, children_t = tuple(map(int, word)), tuple(map(int, children))
        key = (op, rank, word_t, children_t)
        if key in self.index:
            return self.index[key]
        require(op in self.NAMES and rank > 0 and count >= 0 and
                len(self.op) < CAPS["wordexpr_nodes_per_candidate"] and
                self.edges+len(children_t) <=
                    CAPS["wordexpr_edges_per_candidate"] and
                all(1 <= child <= len(self.op) for child in children_t),
                "checker WordExpr node/cap/topology")
        node = len(self.op)+1
        self.op.append(op); self.rank.append(rank); self.words.append(word_t)
        self.children.append(children_t); self.counts.append(count)
        self.index[key] = node; self.edges += len(children_t)
        if op == 2:
            self.flat_leaves += 1
            require(self.flat_leaves <=
                    CAPS["wordexpr_flat_leaves_per_candidate"],
                    "checker WordExpr flat-leaf cap")
        return node

    def identity(self, rank: int = 6) -> int:
        return self.add(1, rank, (), (), 0)

    def flat(self, word: Sequence[int], rank: int = 6) -> int:
        raw = tuple(map(int, word))
        require(len(raw) <= CAPS["single_word_or_section_length"] and
                all(letter and abs(letter) <= rank for letter in raw),
                "checker WordExpr flat leaf")
        return self.add(2, rank, raw, (), len(raw))

    def product(self, left: int, right: int) -> int:
        require(self.rank[left-1] == self.rank[right-1],
                "checker WordExpr product rank")
        return self.add(3, self.rank[left-1], (), (left, right),
                        self.counts[left-1]+self.counts[right-1])

    def product_many(self, roots: Sequence[int]) -> int:
        roots = list(roots)
        require(bool(roots), "checker WordExpr product list")
        def balanced(lo: int, hi: int) -> int:
            if hi-lo == 1:
                return roots[lo]
            mid = (lo+hi)//2
            return self.product(balanced(lo, mid), balanced(mid, hi))
        return balanced(0, len(roots))

    def paper(self, roots: Sequence[int]) -> int:
        return self.product_many(list(reversed(list(roots))))

    def inverse(self, parent: int) -> int:
        return self.add(4, self.rank[parent-1], (), (parent,),
                        self.counts[parent-1])

    def substitution(self, outer: Sequence[int], images: Sequence[int]) -> int:
        images_t = tuple(map(int, images)); outer_t = tuple(map(int, outer))
        require(bool(images_t) and
                all(self.rank[x-1] == self.rank[images_t[0]-1]
                    for x in images_t) and
                all(letter and abs(letter) <= len(images_t)
                    for letter in outer_t) and
                len(outer_t) <= CAPS["single_word_or_section_length"],
                "checker WordExpr substitution typing")
        count = sum(self.counts[images_t[abs(letter)-1]-1]
                    for letter in outer_t)
        return self.add(5, self.rank[images_t[0]-1], outer_t, images_t, count)

    def substitute_expr(self, root: int, images: Sequence[int]) -> int:
        images_t = tuple(map(int, images)); key = (root, images_t)
        if key in self.sub_cache:
            return self.sub_cache[key]
        require(self.rank[root-1] == len(images_t),
                "checker recursive substitution rank")
        op = self.op[root-1]
        if op == 1:
            answer = self.identity(self.rank[images_t[0]-1])
        elif op == 2:
            answer = self.substitution(self.words[root-1], images_t)
        elif op == 3:
            left, right = self.children[root-1]
            answer = self.product(self.substitute_expr(left, images_t),
                                  self.substitute_expr(right, images_t))
        elif op == 4:
            answer = self.inverse(self.substitute_expr(
                self.children[root-1][0], images_t))
        else:
            require(op == 5, "checker recursive substitution opcode")
            transformed = [self.substitute_expr(child, images_t)
                           for child in self.children[root-1]]
            answer = self.substitution(self.words[root-1], transformed)
        self.sub_cache[key] = answer
        return answer

    def reachable(self, roots: Sequence[int]) -> set[int]:
        seen: set[int] = set(); pending = list(roots)
        while pending:
            node = pending.pop()
            if node in seen:
                continue
            require(1 <= node <= len(self.op), "checker WordExpr root")
            seen.add(node); pending.extend(self.children[node-1])
        return seen

    def expand_reduced(self, root: int) -> list[int]:
        require(self.counts[root-1] <= CAPS["single_word_or_section_length"],
                "checker WordExpr flat bridge cap")
        reached = self.reachable([root]); memo: dict[int, list[int]] = {}
        for node in sorted(reached):
            op = self.op[node-1]
            if op == 1:
                value: list[int] = []
            elif op == 2:
                value = reduce_word(self.words[node-1])
            elif op == 3:
                left, right = self.children[node-1]
                value = reduce_word(memo[left]+memo[right])
            elif op == 4:
                value = inv_word(memo[self.children[node-1][0]])
            else:
                require(op == 5, "checker WordExpr flat expansion opcode")
                value = substitute(self.words[node-1],
                                   [memo[x] for x in self.children[node-1]])
            require(len(value) <= CAPS["single_word_or_section_length"],
                    "checker WordExpr reduced bridge cap")
            memo[node] = value
        return memo[root]

    def serialize(self, named_roots: Sequence[tuple[str, int]]) \
            -> dict[str, Any]:
        reached = self.reachable([root for _, root in named_roots])
        ordered = sorted(reached); renumber = {old: i+1
                                              for i, old in enumerate(ordered)}
        nodes = [{"node_id": renumber[old],
                  "opcode": self.NAMES[self.op[old-1]],
                  "rank": self.rank[old-1],
                  "flat_word": list(self.words[old-1]),
                  "children": [renumber[x] for x in self.children[old-1]],
                  "expanded_letter_count": self.counts[old-1]}
                 for old in ordered]
        roots = [{"name": name, "node_id": renumber[root]}
                 for name, root in named_roots]
        return {"format": "typed-wordexpr-dag/v1",
                "node_order": "one_based_topological", "nodes": nodes,
                "roots": roots, "node_count": len(nodes),
                "edge_count": sum(len(row["children"]) for row in nodes),
                "ordinary_product": True,
                "free_reduction_semantic_bridge":
                    "recursive expansion then free reduction equals the literal word; D(xx^-1)=0",
                "manifest_sha256": digest_obj({"nodes": nodes,
                                                 "roots": roots})}

    def accounting(self, roots: Sequence[int]) -> dict[str, Any]:
        counts = {name: 0 for name in self.NAMES.values()}
        for op in self.op:
            counts[self.NAMES[op]] += 1
        return {"node_count": len(self.op), "edge_count": self.edges,
                "flat_leaf_count": self.flat_leaves,
                "opcode_counts": counts, "root_count": len(roots),
                "max_expanded_letter_count": max(
                    (self.counts[root-1] for root in roots), default=0),
                "association": "fixed recursively balanced ordinary PRODUCT",
                "hash_consing": "full opcode/rank/word/child payload equality",
                "digest_is_binding_only": True}


class CheckWordExprEvaluator:
    def __init__(self, dag: CheckWordExpr, quotient: Quotient) -> None:
        self.dag, self.q = dag, quotient
        self.values: list[Element] = []
        self.live_peak = 0
        self.target_gradient_entry_peak = 0

    def evaluate_values(self, roots: Sequence[int] | None = None) -> list[Element]:
        reached = (set(range(1, len(self.dag.op)+1)) if roots is None
                   else self.dag.reachable(list(roots)))
        values: list[Element] = [self.q.identity] * len(self.dag.op)
        for node, op in enumerate(self.dag.op, 1):
            checker_deadline("WordExpr values")
            if node not in reached:
                continue
            if self.dag.rank[node-1] != len(self.q.generators):
                require(self.dag.rank[node-1] == 2 and op in {1, 2, 3, 4, 5},
                        "checker non-PB4 typed node")
                values[node-1] = self.q.identity
                continue
            if op == 1:
                value = self.q.identity
            elif op == 2:
                value = self.q.eval(self.dag.words[node-1])
            elif op == 3:
                left, right = self.dag.children[node-1]
                value = self.q.mul(values[left-1], values[right-1])
            elif op == 4:
                value = self.q.inverse(values[self.dag.children[node-1][0]-1])
            else:
                require(op == 5, "checker WordExpr value opcode")
                value = self.q.identity
                for letter in self.dag.words[node-1]:
                    child = self.dag.children[node-1][abs(letter)-1]
                    factor = values[child-1]
                    value = self.q.mul(value, factor if letter > 0 else
                                       self.q.inverse(factor))
            values[node-1] = value
        self.values = values
        return values

    def gradients(self, roots: Sequence[int]) -> dict[int, Vector]:
        require(len(self.values) == len(self.dag.op),
                "checker WordExpr values first")
        requested = set(map(int, roots)); reached = self.dag.reachable(roots)
        uses = {node: 0 for node in reached}
        for node in reached:
            for child in self.dag.children[node-1]:
                uses[child] += 1
        live: dict[int, Vector] = {}; live_entries = 0
        for node in sorted(reached):
            checker_deadline("WordExpr gradients")
            op = self.dag.op[node-1]
            if op == 1:
                gradient: Vector = {}
            elif op == 2:
                gradient, value = fox(self.dag.words[node-1], self.q)
                require(value == self.values[node-1],
                        "checker WordExpr flat Fox value")
            elif op == 3:
                left, right = self.dag.children[node-1]
                gradient = dict(live[left])
                add_scaled(gradient, translate(live[right],
                                               self.values[left-1], self.q), 1)
            elif op == 4:
                parent = self.dag.children[node-1][0]
                gradient = translate(live[parent],
                                     self.q.inverse(self.values[parent-1]),
                                     self.q)
                gradient = {key: (2*coefficient) % 3
                            for key, coefficient in gradient.items()
                            if coefficient % 3}
            else:
                require(op == 5, "checker WordExpr Fox opcode")
                gradient = {}; prefix = self.q.identity
                for letter in self.dag.words[node-1]:
                    child = self.dag.children[node-1][abs(letter)-1]
                    if letter > 0:
                        add_scaled(gradient, translate(live[child], prefix,
                                                       self.q), 1)
                        prefix = self.q.mul(prefix, self.values[child-1])
                    else:
                        prefix = self.q.mul(
                            prefix, self.q.inverse(self.values[child-1]))
                        add_scaled(gradient, translate(live[child], prefix,
                                                       self.q), 2)
                require(prefix == self.values[node-1],
                        "checker WordExpr negative-prefix/value")
            live[node] = gradient; live_entries += len(gradient)
            self.live_peak = max(self.live_peak, live_entries)
            require(self.live_peak <=
                    CAPS["candidate_live_gradient_entries_total"],
                    "checker WordExpr live-gradient cap")
            for child in self.dag.children[node-1]:
                uses[child] -= 1
                if uses[child] == 0 and child not in requested:
                    live_entries -= len(live.pop(child))
        self.target_gradient_entry_peak = max(
            self.target_gradient_entry_peak,
            max((len(live[root]) for root in requested), default=0))
        return {root: live[root] for root in requested}


def check_gradient_binding(name: str, kind: str, gradient: Vector,
                           value: Element) -> dict[str, Any]:
    digest = hashlib.sha256()
    for (component, element), coefficient in sorted(
            gradient.items(), key=lambda row: (row[0][0], row[0][1])):
        blob = element_blob(element)
        digest.update(component.to_bytes(1, "little"))
        digest.update(len(blob).to_bytes(2, "little"))
        digest.update(blob)
        digest.update(int(coefficient).to_bytes(1, "little"))
    return {"name": name, "kind": kind, "entry_count": len(gradient),
            "quotient_value_hex": element_blob(value).hex(),
            "canonical_gradient_sha256": digest.hexdigest(),
            "canonical_order": "component then exact canonical E4 bytes",
            "digest_is_binding_only_not_element_equality": True}


def build_check_wordexpr(index: int, correction: Sequence[int],
                         inverse_words: Sequence[Sequence[int]]) \
        -> dict[str, Any]:
    require(len(inverse_words) == 6, "checker WordExpr inverse tuple")
    candidate = reduce_word(FIXED_WORD+list(correction))
    require(exponent_sums(candidate, 2) == [0, 0],
            "checker candidate exponent sums")
    dag = CheckWordExpr(); one = dag.identity(6)
    generators = [dag.flat([i], 6) for i in range(1, 7)]

    def f_at(left: int, right: int) -> int:
        return dag.substitution(candidate, [left, right])

    def c_at(left: int, right: int) -> int:
        return dag.substitution(correction, [left, right])

    correction_roots: list[tuple[str, int]] = []
    hex1: list[tuple[str, str, int]] = []
    hex2: list[tuple[str, str, int]] = []
    for slot, mapping in enumerate(cofaces(3)):
        x, y = dag.flat(mapping[0], 6), dag.flat(mapping[2], 6)
        correction_roots.append(
            (f"correction_coarse_J_H_coface_{slot}", c_at(x, y)))
        z = dag.inverse(dag.paper([x, y]))
        u = dag.inverse(dag.paper([y, x]))
        fxy, fxz, fyz = f_at(x, y), f_at(x, z), f_at(y, z)
        fux, fuy = f_at(u, x), f_at(u, y)
        hex1.append((f"hexagon_1_coface_{slot}", "hexagon",
                     dag.paper([fxy, dag.inverse(fxz), fyz])))
        hex2.append((f"hexagon_2_coface_{slot}", "hexagon",
                     dag.paper([dag.inverse(fux), dag.inverse(fxy), fuy])))
    acceptance: list[tuple[str, str, int]] = [
        (f"charming_error_coface_{slot}", "charming", one)
        for slot in range(5)] + hex1 + hex2
    pent_contexts = [
        (generators[0], generators[3]),
        (generators[3], generators[5]),
        (dag.paper([generators[1], generators[3]]), generators[5]),
        (dag.paper([generators[0], generators[1]]),
         dag.paper([generators[4], generators[5]])),
        (generators[0], dag.paper([generators[3], generators[4]])),
    ]
    pent_parts = [f_at(left, right) for left, right in pent_contexts]
    pent = dag.paper([
        dag.inverse(dag.paper([pent_parts[4], pent_parts[2]])),
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
    for ordinal, relator in enumerate(relations, 1):
        acceptance.append((f"S_relation_{ordinal}",
                           "endomorphism_relation",
                           dag.substitution(relator, source)))
    inverse_roots = [dag.flat(word, 6) for word in inverse_words]
    diagnostics: list[tuple[str, str, int]] = []
    for ordinal, relator in enumerate(relations, 1):
        diagnostics.append((f"T_relation_{ordinal}",
                            "endomorphism_relation",
                            dag.substitution(relator, inverse_roots)))
    for ordinal, inverse_word in enumerate(inverse_words, 1):
        acceptance.append((f"ST_generator_{ordinal}",
                           "onto_two_sided_inverse",
                           dag.product(dag.substitution(inverse_word, source),
                                       dag.inverse(generators[ordinal-1]))))
    for ordinal, source_root in enumerate(source, 1):
        diagnostics.append((f"TS_generator_{ordinal}",
                            "onto_two_sided_inverse",
                            dag.product(dag.substitute_expr(
                                source_root, inverse_roots),
                                dag.inverse(generators[ordinal-1]))))
    expected_a = ([f"charming_error_coface_{i}" for i in range(5)] +
                  [f"hexagon_{j}_coface_{i}" for j in (1, 2)
                   for i in range(5)] + ["ordered_A18_pentagon"] +
                  [f"S_relation_{i}" for i in range(1, 12)] +
                  [f"ST_generator_{i}" for i in range(1, 7)])
    expected_d = ([f"T_relation_{i}" for i in range(1, 12)] +
                  [f"TS_generator_{i}" for i in range(1, 7)])
    require([x[0] for x in acceptance] == expected_a and
            [x[0] for x in diagnostics] == expected_d and
            all(dag.counts[root-1] <=
                CAPS["wordexpr_expanded_letter_count_per_target"]
                for root in ([row[2] for row in acceptance+diagnostics] +
                              source + [row[1] for row in correction_roots])),
            "checker corrected Def2.9 order/count cap")
    return {"correction_index": index, "correction_word": list(correction),
            "candidate_word": candidate,
            "candidate_exponent_sums": exponent_sums(candidate, 2),
            "dag": dag, "source_roots": source,
            "inverse_roots": inverse_roots,
            "correction_coface_roots": correction_roots,
            "acceptance": acceptance, "diagnostics": diagnostics,
            "charming_witness": {
                "g_equals_f": True, "f_times_g_inverse_is_identity": True,
                "error_gradient_zero": True,
                "free_group_fact": "ker(F2->Z^2)=[F2,F2]"}}


def checker_make_typed_positive(coefficients: Sequence[int],
                                seeds: Sequence[Sequence[int]]) \
        -> dict[str, Any]:
    dag = CheckWordExpr()
    f0_root = dag.flat(FIXED_WORD, 2)
    factors: list[int] = []
    for index, coefficient in enumerate(coefficients):
        for _ in range(int(coefficient) % 3):
            factors.append(dag.flat(seeds[index], 2))
    correction_root = dag.identity(2) if not factors else dag.product_many(factors)
    candidate_root = dag.product(f0_root, correction_root)
    correction_count = dag.counts[correction_root-1]
    correction_word = None
    if correction_count <= CAPS["single_word_or_section_length"]:
        correction_word = dag.expand_reduced(correction_root)
    return {"dag": dag, "f0_root": f0_root,
            "correction_root": correction_root,
            "candidate_root": candidate_root,
            "coefficient_vector": list(map(int, coefficients)),
            "nonzero_support": [i+1 for i, x in enumerate(coefficients)
                                if int(x) % 3],
            "expanded_count": dag.counts[candidate_root-1],
            "correction_expanded_count": correction_count,
            "correction_word": correction_word,
            "correction_word_flattened": correction_word is not None,
            "typed_product_order": "seed_1^a1 * ... * seed_104^a104",
            "exponent_two_is_two_copies": True}


def checker_build_typed_targets(typed: dict[str, Any],
                                inverse_words: Sequence[Sequence[int]]) \
        -> dict[str, Any]:
    require(len(inverse_words) == 6, "checker typed inverse tuple")
    dag: CheckWordExpr = typed["dag"]
    candidate_root, correction_root = (int(typed["candidate_root"]),
                                       int(typed["correction_root"]))
    require(dag.rank[candidate_root-1] == dag.rank[correction_root-1] == 2,
            "checker typed rank-2 roots")
    one = dag.identity(6)
    generators = [dag.flat([i], 6) for i in range(1, 7)]

    def f_at(left: int, right: int) -> int:
        return dag.substitute_expr(candidate_root, [left, right])

    def c_at(left: int, right: int) -> int:
        return dag.substitute_expr(correction_root, [left, right])

    correction_roots: list[tuple[str, int]] = []
    hex1: list[tuple[str, str, int]] = []
    hex2: list[tuple[str, str, int]] = []
    for slot, mapping in enumerate(cofaces(3)):
        x, y = dag.flat(mapping[0], 6), dag.flat(mapping[2], 6)
        correction_roots.append(
            (f"correction_coarse_J_H_coface_{slot}", c_at(x, y)))
        z = dag.inverse(dag.paper([x, y]))
        u = dag.inverse(dag.paper([y, x]))
        fxy, fxz, fyz = f_at(x, y), f_at(x, z), f_at(y, z)
        fux, fuy = f_at(u, x), f_at(u, y)
        hex1.append((f"hexagon_1_coface_{slot}", "hexagon",
                     dag.paper([fxy, dag.inverse(fxz), fyz])))
        hex2.append((f"hexagon_2_coface_{slot}", "hexagon",
                     dag.paper([dag.inverse(fux), dag.inverse(fxy), fuy])))
    acceptance: list[tuple[str, str, int]] = [
        (f"charming_error_coface_{slot}", "charming", one)
        for slot in range(5)] + hex1 + hex2
    pent_contexts = [
        (generators[0], generators[3]),
        (generators[3], generators[5]),
        (dag.paper([generators[1], generators[3]]), generators[5]),
        (dag.paper([generators[0], generators[1]]),
         dag.paper([generators[4], generators[5]])),
        (generators[0], dag.paper([generators[3], generators[4]])),
    ]
    pent_parts = [f_at(left, right) for left, right in pent_contexts]
    acceptance.append(("ordered_A18_pentagon", "pentagon", dag.paper([
        dag.inverse(dag.paper([pent_parts[4], pent_parts[2]])),
        pent_parts[1], pent_parts[3], pent_parts[0]])))
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
    for ordinal, relator in enumerate(relations, 1):
        acceptance.append((f"S_relation_{ordinal}", "endomorphism_relation",
                           dag.substitution(relator, source)))
    inverse_roots = [dag.flat(word, 6) for word in inverse_words]
    diagnostics: list[tuple[str, str, int]] = []
    for ordinal, relator in enumerate(relations, 1):
        diagnostics.append((f"T_relation_{ordinal}", "endomorphism_relation",
                            dag.substitution(relator, inverse_roots)))
    for ordinal, inverse_word in enumerate(inverse_words, 1):
        acceptance.append((f"ST_generator_{ordinal}", "onto_two_sided_inverse",
                           dag.product(dag.substitution(inverse_word, source),
                                       dag.inverse(generators[ordinal-1]))))
    for ordinal, source_root in enumerate(source, 1):
        diagnostics.append((f"TS_generator_{ordinal}", "onto_two_sided_inverse",
                            dag.product(dag.substitute_expr(source_root,
                                                             inverse_roots),
                                        dag.inverse(generators[ordinal-1]))))
    expected_a = ([f"charming_error_coface_{i}" for i in range(5)] +
                  [f"hexagon_{j}_coface_{i}" for j in (1, 2)
                   for i in range(5)] + ["ordered_A18_pentagon"] +
                  [f"S_relation_{i}" for i in range(1, 12)] +
                  [f"ST_generator_{i}" for i in range(1, 7)])
    expected_d = ([f"T_relation_{i}" for i in range(1, 12)] +
                  [f"TS_generator_{i}" for i in range(1, 7)])
    require([x[0] for x in acceptance] == expected_a and
            [x[0] for x in diagnostics] == expected_d and
            len(acceptance) == 33 and len(diagnostics) == 17,
            "checker typed Def2.9 order")
    roots = ([root for _, _, root in acceptance+diagnostics] + source +
             [root for _, root in correction_roots])
    return {"dag": dag, "source_roots": source,
            "inverse_roots": inverse_roots,
            "correction_coface_roots": correction_roots,
            "acceptance": acceptance, "diagnostics": diagnostics,
            "roots": roots}


def checker_build_typed_target6(typed: dict[str, Any]) -> dict[str, Any]:
    """Build only the target-6 typed root for the checker hot path."""
    dag: CheckWordExpr = typed["dag"]
    candidate_root = int(typed["candidate_root"])
    mapping = cofaces(3)[0]
    x, y = dag.flat(mapping[0], 6), dag.flat(mapping[2], 6)
    z = dag.inverse(dag.paper([x, y]))
    fxy = dag.substitute_expr(candidate_root, [x, y])
    fxz = dag.substitute_expr(candidate_root, [x, z])
    fyz = dag.substitute_expr(candidate_root, [y, z])
    target = dag.paper([fxy, dag.inverse(fxz), fyz])
    return {"dag": dag,
            "acceptance": [("hexagon_1_coface_0", "hexagon", target)],
            "diagnostics": [], "source_roots": [],
            "inverse_roots": [], "correction_coface_roots": [],
            "roots": [target]}


def checker_select_typed_target_root(targets: dict[str, Any],
                                     ordinal: int) -> int:
    acceptance = targets["acceptance"]
    if ordinal == 6:
        require(len(acceptance) == 1,
                "checker target6 typed acceptance cardinality")
        name, kind, root = acceptance[0]
        require(name == "hexagon_1_coface_0" and kind == "hexagon",
                "checker target6 typed acceptance binding")
        return root
    return acceptance[ordinal-1][2]


def checker_validate_selected_proof_payload(
        proof: dict[str, Any], expected_names: Sequence[str],
        leaf_resolver: Any,
        expected_vectors: dict[str, Vector] | None = None
        ) -> tuple[dict[str, Vector], dict[str, int]]:
    """Shared lossless selected-proof replay entry.

    Production positive replay and the bounded injected fixture both enter
    through this exact DAG decoder/replayer.  The fixture may provide a small
    quotient and leaf resolver, but it cannot replace topology, reachability,
    coefficient, root-order, or streaming replay checks.
    """
    require(callable(leaf_resolver), "selected proof leaf resolver")
    vectors, roots = evaluate_proof_dag(proof, expected_names, leaf_resolver)
    if expected_vectors is not None:
        require(vectors == expected_vectors,
                "selected proof expected vector binding")
    return vectors, roots


def checker_validate_positive_replay(data: dict[str, Any],
                                     coefficients: Sequence[int],
                                     seeds: Sequence[Sequence[int]],
                                     inverse_words: Sequence[Sequence[int]],
                                     frozen: tuple[Element, ...],
                                     e3: Quotient, e4: Quotient,
                                     pool: ReplayPool, basis: ReplayBasis) -> None:
    typed = checker_make_typed_positive(coefficients, seeds)
    typed_targets = checker_build_typed_targets(typed, inverse_words)
    evaluator = CheckWordExprEvaluator(typed_targets["dag"], e4)
    evaluator.evaluate_values()
    for name, root in typed_targets["correction_coface_roots"]:
        require(evaluator.values[root-1] == e4.identity,
                f"checker positive correction gate {name}")
    source_values = tuple(evaluator.values[root-1]
                          for root in typed_targets["source_roots"])
    require(source_values == frozen, "checker positive source tuple")
    for index, seed in enumerate(seeds):
        require(e3.eval(embed_f2(seed)) == e3.identity and
                exponent_sums(seed, 2) == [0, 0],
                f"checker positive seed roof {index+1}")
    correction_word = typed["correction_word"]
    if correction_word is not None:
        require(e3.eval(embed_f2(correction_word)) == e3.identity,
                "checker positive correction roof")
    else:
        correction_e3 = e3.identity
        for index, seed in enumerate(seeds):
            seed_e3 = e3.eval(embed_f2(seed))
            for _ in range(int(coefficients[index]) % 3):
                correction_e3 = e3.mul(correction_e3, seed_e3)
        require(correction_e3 == e3.identity,
                "checker positive typed correction roof")
    require(exponent_sums(FIXED_WORD, 2) == [0, 0],
            "checker positive fixed exponent")

    named = ([(name, root) for name, _, root in
              typed_targets["acceptance"]+typed_targets["diagnostics"]] +
             [(f"source_{i+1}", root)
              for i, root in enumerate(typed_targets["source_roots"])] +
             list(typed_targets["correction_coface_roots"]))
    expected_expression = typed_targets["dag"].serialize(named)
    positive = data.get("positive_replay")
    require(isinstance(positive, dict) and
            positive.get("target_expression") == expected_expression and
            positive.get("acceptance_count") == 33 and
            positive.get("diagnostic_count") == 17 and
            positive.get("direct_replay") is True and
            positive.get("raw_chain_affine_certificate") == {
                "all_33_direct_gradients_replayed": True,
                "all_33_affine_predictions_checked": True,
                "correction_occurrence_E4_identity": True,
                "raw_C1_before_D2": True,
            }, "checker positive replay header/expression")
    acceptance_rows = positive["acceptance"]
    diagnostics_rows = positive["diagnostics"]
    require(len(acceptance_rows) == 33 and len(diagnostics_rows) == 17,
            "checker positive replay row counts")

    def replay_gradient(root: int, name: str) -> tuple[Vector, Element]:
        value = evaluator.values[root-1]
        gradient = evaluator.gradients([root])[root]
        if typed_targets["dag"].counts[root-1] <= \
                CAPS["single_word_or_section_length"]:
            direct, direct_value = fox(
                typed_targets["dag"].expand_reduced(root), e4)
            require(direct == gradient and direct_value == value,
                    f"checker positive typed/flat {name}")
        else:
            cold = CheckWordExprEvaluator(typed_targets["dag"], e4)
            cold.evaluate_values()
            require(cold.gradients([root])[root] == gradient and
                    cold.values[root-1] == value,
                    f"checker positive typed/cold {name}")
        return gradient, value

    expected_names = [name for name, _, _ in typed_targets["acceptance"]]
    require([row.get("name") for row in acceptance_rows] == expected_names,
            "checker positive acceptance order")
    for row, (name, kind, root) in zip(acceptance_rows,
                                       typed_targets["acceptance"]):
        gradient, value = replay_gradient(root, name)
        binding_sha = digest_obj(check_gradient_binding(name, kind,
                                                        gradient, value))
        require(row == {
            "ordinal": row["ordinal"], "name": name, "kind": kind,
            "quotient_identity": True,
            "gradient_sha256": binding_sha,
            "proof_root_node_id": row["proof_root_node_id"],
            "direct_replay": True, "affine_prediction_checked": True,
        } and row["ordinal"] == typed_targets["acceptance"].index(
            (name, kind, root))+1,
                f"checker positive acceptance binding {name}")
    expected_diag_names = [name for name, _, _ in typed_targets["diagnostics"]]
    require([row.get("name") for row in diagnostics_rows] == expected_diag_names,
            "checker positive diagnostics order")
    for row, (name, kind, root) in zip(diagnostics_rows,
                                       typed_targets["diagnostics"]):
        gradient, value = replay_gradient(root, name)
        require(row == {
            "ordinal": row["ordinal"], "name": name, "kind": kind,
            "quotient_identity": value == e4.identity,
            "gradient_sha256": digest_obj(check_gradient_binding(
                name, kind, gradient, value)),
            "acceptance_predicate": False,
        } and row["ordinal"] == typed_targets["diagnostics"].index(
            (name, kind, root))+1,
                f"checker positive diagnostic binding {name}")

    proof = positive.get("proof_dag")
    registry_rows = positive.get("quotient_element_registry")
    require(isinstance(proof, dict) and isinstance(registry_rows, list),
            "checker positive proof payload")
    section_values = decode_section_expressions(proof["section_expressions"], e4)
    by_id, reverse = validate_registry(registry_rows, {4: e4}, section_values)

    def leaf_resolver(node: dict[str, Any]) -> Vector:
        relator = node["relator_index"]
        translation_id = node["translation_element_id"]
        require(1 <= relator <= len(basis.columns) and
                translation_id in by_id and
                reverse.get((4, by_id[translation_id])) == translation_id,
                "checker positive proof leaf typing")
        packed = basis.columns[relator-1]
        raw: Vector = {}
        for key, coefficient in packed.items():
            component, identifier = replay_unpack_key(key)
            add(raw, (component, pool.value(identifier)), coefficient)
        return translate(raw, by_id[translation_id], e4)

    proof_vectors, proof_roots = checker_validate_selected_proof_payload(
        proof, expected_names, leaf_resolver)
    for row, (name, kind, root) in zip(acceptance_rows,
                                       typed_targets["acceptance"]):
        gradient, value = replay_gradient(root, name)
        require(row["proof_root_node_id"] == proof_roots[name] and
                proof_vectors[name] == gradient and value == e4.identity,
                f"checker positive serialized proof {name}")
    require(positive.get("proof_root_names") == expected_names,
            "checker positive proof root names")


def checker_source_tuple_preflight(dictionary: dict[str, Any], e4: Quotient,
                                   frozen: tuple[Element, ...]) \
        -> tuple[dict[str, Any], list[tuple[Element, ...]]]:
    g = e4.generators
    contexts = [(g[0], g[3]), (g[0], g[1]), (g[3], g[4]),
                (q_product(e4, [g[3], g[1]]), g[5]),
                (q_product(e4, [g[1], g[0]]), g[2]),
                (q_product(e4, [g[1], g[0]]),
                 q_product(e4, [g[5], g[4]]))]
    seeds = dictionary["seed_words"]
    signed = [(i+1, word) for i, word in enumerate(seeds)] + [
        (-(i+1), inv_word(word)) for i, word in enumerate(seeds)]
    tables: list[list[Element]] = []; seed_sha = hashlib.sha256()
    for context_index, context in enumerate(contexts, 1):
        step = {edge: e4.eval(word, context) for edge, word in signed}
        for edge in sorted(step):
            seed_sha.update(context_index.to_bytes(1, "little"))
            seed_sha.update(edge.to_bytes(2, "little", signed=True))
            seed_sha.update(element_blob(step[edge]))
        values = [e4.identity]
        for index in range(1, dictionary["count"]):
            parent = dictionary["parent_indices"][index]-1
            edge = dictionary["signed_seed_edges"][index]
            require(0 <= parent < index and edge in step,
                    "checker source DP parent")
            values.append(e4.mul(values[parent], step[edge]))
        tables.append(values)
    base = [e4.eval(FIXED_WORD, context) for context in contexts]
    tuples: list[tuple[Element, ...]] = []; tuple_sha = []
    exponents: list[list[int]] = []; ledger = hashlib.sha256()
    first: dict[str, Any] | None = None
    for index, correction in enumerate(dictionary["words"], 1):
        checker_deadline("source tuple preflight")
        ff, gv, gs, f1234, h, middle = [
            e4.mul(base[j], tables[j][index-1]) for j in range(6)]
        current = (
            g[0], q_product(e4, [e4.inverse(gv), g[1], gv]),
            q_product(e4, [e4.inverse(ff), e4.inverse(h), g[2], h, ff]),
            q_product(e4, [e4.inverse(ff), g[3], ff]),
            q_product(e4, [e4.inverse(ff), e4.inverse(middle), e4.inverse(gs),
                            g[4], gs, middle, ff]),
            q_product(e4, [e4.inverse(f1234), g[5], f1234]))
        tuples.append(current)
        row_hex = [element_blob(value).hex() for value in current]
        tuple_sha.append(digest_obj(row_hex))
        exp = exponent_sums(reduce_word(FIXED_WORD+correction), 2)
        exponents.append(exp); ledger.update(canonical_bytes(
            [index, row_hex, exp])+b"\n")
        if current != frozen and first is None:
            first = {"candidate_index": index, "candidate_tuple_hex": row_hex,
                     "frozen_tuple_hex": [element_blob(x).hex()
                                           for x in frozen]}
    require(len(tuples) == CAPS["dictionary_word_records"] and
            all(row == [0, 0] for row in exponents),
            "checker complete source tuple/exponent ledger")
    return ({"complete": True, "evaluated": len(tuples),
             "all_equal_to_frozen_tuple": first is None,
             "first_difference": first,
             "tuple_sha256_by_candidate": tuple_sha,
             "tuple_ledger_sha256": ledger.hexdigest(),
             "candidate_exponent_sums": exponents,
             "all_candidate_exponent_sums_zero": True,
             "frozen_tuple_hex": [element_blob(x).hex() for x in frozen],
             "context_count": 6,
             "signed_seed_images_sha256": seed_sha.hexdigest(),
             "recurrence": "rho(c_i)=rho(c_parent)*rho(signed_seed)",
             "raw_descendant_words_evaluated": False}, tuples)


def check_expr_digest(dag: CheckWordExpr) -> str:
    return digest_obj({"opcode": dag.op, "rank": dag.rank,
                       "word": [list(row) for row in dag.words],
                       "children": [list(row) for row in dag.children],
                       "expanded_count": dag.counts})


def check_expr_diagnostics(compiled: dict[str, Any],
                           evaluator: CheckWordExprEvaluator,
                           remap: dict[str, int] | None = None) \
        -> list[dict[str, Any]]:
    rows = []
    for name, kind, root in compiled["diagnostics"]:
        value = evaluator.values[root-1]
        rows.append({"name": name, "kind": kind,
                     "root": root if remap is None else remap[name],
                     "quotient_value_hex": element_blob(value).hex(),
                     "quotient_identity": value == evaluator.q.identity,
                     "feeds_acceptance": False,
                     "Fox_membership_tested": False})
    return rows


def check_direct_failure(compiled: dict[str, Any],
                         evaluator: CheckWordExprEvaluator) \
        -> tuple[str | None, int]:
    for name, root in compiled["correction_coface_roots"]:
        if evaluator.values[root-1] != evaluator.q.identity:
            return name, 0
    for ordinal, (name, _, root) in enumerate(compiled["acceptance"], 1):
        if evaluator.values[root-1] != evaluator.q.identity:
            return name, ordinal
    return None, 0


def check_flat_bridge(compiled: dict[str, Any],
                      evaluator: CheckWordExprEvaluator,
                      e4: Quotient,
                      normalized: dict[str, Any]) -> dict[str, Any]:
    flat_a, flat_d = fixed_target_split(e4, normalized)
    flat = flat_a+flat_d
    expr_rows = compiled["acceptance"]+compiled["diagnostics"]
    require([(x[0], x[1]) for x in expr_rows] ==
            [(x[0], x[1]) for x in flat] and len(flat) == 50,
            "checker candidate1 flat bridge order")
    bindings = []
    for (name, kind, root), (_, _, word) in zip(expr_rows, flat):
        require(compiled["dag"].expand_reduced(root) == word,
                f"checker candidate1 flat literal {name}")
        gradient = evaluator.gradients([root])[root]
        direct_gradient, direct_value = fox(word, e4)
        require(direct_value == evaluator.values[root-1] and
                direct_gradient == gradient,
                f"checker candidate1 flat Fox {name}")
        bindings.append(check_gradient_binding(
            name, kind, gradient, evaluator.values[root-1]))
    return {"mandatory": True, "target_count": 50,
            "acceptance_target_count": 33,
            "diagnostic_target_count": 17,
            "original_target_order_preserved": True,
            "all_reduced_words_equal": True,
            "all_quotient_values_equal": True,
            "all_left_Fox_gradients_equal": True,
            "cold_route": "frozen v8 flat literal fox_gradient",
            "memo_route": "candidate-local typed WordExpr chain rule",
            "bindings_sha256": digest_obj(bindings),
            "old_flat_cap": CAPS["single_word_or_section_length"]}


def validate_memo_accounting(row: Any, *, require_pins: bool) -> None:
    require(isinstance(row, dict) and set(row) == {
                "format", "candidate_binding_sha256",
                "quotient_binding_sha256", "presentation_sha256",
                "leaf_bindings_sha256",
                "key_binds_rank_arity_candidate_quotient_leafs",
                "equal_group_value_is_not_a_cache_key",
                "cross_candidate_sharing", "pool_or_proof_identifiers_stored",
                "node_cap", "sparse_entry_cap",
                "estimated_bytes_per_sparse_entry",
                "additional_budget_bytes", "hits", "misses", "evictions",
                "skipped_oversize", "recomputations", "peak_cached_nodes",
                "peak_cached_sparse_entries",
                "peak_working_plus_cached_sparse_entries",
                "pinned_source_count", "requested_source_count",
                "unretained_requested_source_count",
                "pin_store_fallbacks", "pin_evictions",
                "cache_capacity_is_nonterminal",
                "rollbacks", "discarded_nodes",
                "discarded_sparse_entries",
                "eviction_changes_performance_only"} and
            row["format"] == "candidate-local-typed-gradient-memo/v1" and
            all(isinstance(row[key], str) and len(row[key]) == 64
                for key in ("candidate_binding_sha256",
                            "quotient_binding_sha256", "presentation_sha256",
                            "leaf_bindings_sha256")) and
            row["key_binds_rank_arity_candidate_quotient_leafs"] is True and
            row["equal_group_value_is_not_a_cache_key"] is True and
            row["cross_candidate_sharing"] is False and
            row["pool_or_proof_identifiers_stored"] is False and
            row["node_cap"] == CAPS["gradient_memo_nodes"] and
            row["sparse_entry_cap"] == CAPS["gradient_memo_sparse_entries"] and
            row["estimated_bytes_per_sparse_entry"] ==
                CAPS["gradient_memo_estimated_bytes_per_sparse_entry"] and
            row["additional_budget_bytes"] ==
                CAPS["gradient_memo_additional_budget_bytes"] and
            all(isinstance(row[key], int) and row[key] >= 0 for key in
                ("hits", "misses", "evictions", "skipped_oversize",
                 "recomputations", "peak_cached_nodes",
                 "peak_cached_sparse_entries",
                 "peak_working_plus_cached_sparse_entries",
                 "requested_source_count",
                 "unretained_requested_source_count",
                 "pin_store_fallbacks", "pin_evictions", "rollbacks",
                 "discarded_nodes", "discarded_sparse_entries")) and
            row["peak_cached_nodes"] <= CAPS["gradient_memo_nodes"] and
            row["peak_cached_sparse_entries"] <=
                CAPS["gradient_memo_sparse_entries"] and
            row["peak_working_plus_cached_sparse_entries"] <=
                CAPS["candidate_live_gradient_entries_total"] and
            isinstance(row["pinned_source_count"], int) and
            0 <= row["pinned_source_count"] <= 6 and
            row["requested_source_count"] == (6 if require_pins else 0) and
            row["pinned_source_count"] +
                row["unretained_requested_source_count"] ==
                row["requested_source_count"] and
            row["cache_capacity_is_nonterminal"] is True and
            row["eviction_changes_performance_only"] is True,
            "checker typed memo accounting")


def validate_candidate1_bridge(actual: Any, expected: dict[str, Any],
                               compiled: dict[str, Any], e4: Quotient,
                               inverse_words: Sequence[Sequence[int]]) -> None:
    require(isinstance(actual, dict) and set(actual) == set(expected) | {
                "membership_fused", "membership_reused_target_count",
                "first_missing_target_ordinal", "first_missing_target_name",
                "remaining_canaries_completed_after_first_missing",
                "missing_target_re_evaluated", "memo_binding"} and
            all(actual[key] == value for key, value in expected.items()) and
            actual["membership_fused"] is True and
            actual["membership_reused_target_count"] == 6 and
            actual["first_missing_target_ordinal"] == 6 and
            actual["first_missing_target_name"] == "hexagon_1_coface_0" and
            actual["remaining_canaries_completed_after_first_missing"] == 44 and
            actual["missing_target_re_evaluated"] is False,
            "checker candidate1 bridge/fusion metadata")
    validate_memo_accounting(actual["memo_binding"], require_pins=True)
    memo = actual["memo_binding"]
    candidate_binding = {
        "schema": SCHEMA,
        "candidate_index": compiled["correction_index"],
        "correction_word_sha256": digest_obj(compiled["correction_word"]),
        "candidate_word_sha256": digest_obj(compiled["candidate_word"]),
        "inverse_words_sha256": digest_obj(inverse_words),
        "acceptance_order_sha256": digest_obj(
            [(name, kind) for name, kind, _ in compiled["acceptance"]]),
        "diagnostic_order_sha256": digest_obj(
            [(name, kind) for name, kind, _ in compiled["diagnostics"]]),
    }
    presentation_sha = digest_obj(e4.collector.data)
    leaf_sha = digest_obj([element_blob(value).hex()
                           for value in e4.generators])
    quotient_sha = digest_obj({
        "rank": e4.rank, "degree": e4.degree,
        "pc_rank": e4.collector.n,
        "presentation_sha256": presentation_sha,
        "leaf_bindings_sha256": leaf_sha})
    require(memo["candidate_binding_sha256"] == digest_obj(candidate_binding) and
            memo["presentation_sha256"] == presentation_sha and
            memo["leaf_bindings_sha256"] == leaf_sha and
            memo["quotient_binding_sha256"] == quotient_sha,
            "checker independent memo typed binding")


def validate_gradient_memo_performance(data: dict[str, Any], *,
                                       evaluated: int, pass_count: int,
                                       partial: bool,
                                       records: Sequence[dict[str, Any]] = ()) \
        -> None:
    row = data.get("gradient_memo_performance")
    require(isinstance(row, dict), "checker memo performance receipt")
    keys = {
        "format", "candidate_evaluators", "proof_regeneration_evaluators",
        "hits", "misses", "evictions", "recomputations",
        "skipped_oversize", "peak_cached_nodes",
        "peak_cached_sparse_entries",
        "peak_working_plus_cached_sparse_entries",
        "source_roots_requested_per_pin_stage", "pin_policy",
        "ordinary_lazy_pin_target_ordinal",
        "candidate1_bridge_pin_stages", "ordinary_lazy_pin_stages",
        "proof_pin_stages", "pin_stage_count", "pin_requests_total",
        "pin_store_fallbacks", "pin_evictions",
        "peak_retained_pinned_source_count", "direct_failures_before_pin",
        "ordinary_exits_before_target17", "cross_candidate_cache_entries",
        "candidate_memos_discarded_at_rollback", "phase_elapsed_seconds",
        "progress_interval_seconds", "candidate_order_changed",
        "acceptance_or_diagnostic_promotion_changed",
        "memo_eviction_is_terminal_or_rejection", "cache_entry_budget_bytes",
        "working_plus_cached_accounted_under_frozen_live_cap",
        "static_quotient_binding_precomputed_once",
        "inverse_words_binding_precomputed_once",
        "target_order_binding_hashes_computed_once"}
    if partial:
        keys.add("partial_resource_stop")
    require(set(row) == keys and
            row["format"] ==
                "candidate-local-typed-gradient-memo-summary/v1" and
            row["source_roots_requested_per_pin_stage"] == 6 and
            row["pin_policy"] ==
                "candidate1 after direct gate before 50 bridge; ordinary only before acceptance target 17; proof fresh evaluator" and
            row["ordinary_lazy_pin_target_ordinal"] == 17 and
            row["cross_candidate_cache_entries"] == 0 and
            row["candidate_order_changed"] is False and
            row["acceptance_or_diagnostic_promotion_changed"] is False and
            row["memo_eviction_is_terminal_or_rejection"] is False and
            row["cache_entry_budget_bytes"] ==
                CAPS["gradient_memo_additional_budget_bytes"] <= 512_000_000 and
            row["working_plus_cached_accounted_under_frozen_live_cap"] is True and
            row["static_quotient_binding_precomputed_once"] is True and
            row["inverse_words_binding_precomputed_once"] is True and
            row["target_order_binding_hashes_computed_once"] is True and
            row["progress_interval_seconds"] == 10 and
            all(isinstance(row[key], int) and row[key] >= 0 for key in
                ("candidate_evaluators", "proof_regeneration_evaluators",
                 "hits", "misses", "evictions", "recomputations",
                 "skipped_oversize", "peak_cached_nodes",
                 "peak_cached_sparse_entries",
                  "peak_working_plus_cached_sparse_entries",
                  "candidate_memos_discarded_at_rollback",
                  "candidate1_bridge_pin_stages",
                  "ordinary_lazy_pin_stages", "proof_pin_stages",
                  "pin_stage_count", "pin_requests_total",
                  "pin_store_fallbacks", "pin_evictions",
                  "peak_retained_pinned_source_count",
                  "direct_failures_before_pin",
                  "ordinary_exits_before_target17")) and
            row["peak_cached_nodes"] <= CAPS["gradient_memo_nodes"] and
            row["peak_cached_sparse_entries"] <=
                CAPS["gradient_memo_sparse_entries"] and
            row["peak_working_plus_cached_sparse_entries"] <=
                CAPS["candidate_live_gradient_entries_total"] and
            row["peak_retained_pinned_source_count"] <= 6 and
            row["pin_stage_count"] ==
                row["candidate1_bridge_pin_stages"] +
                row["ordinary_lazy_pin_stages"] + row["proof_pin_stages"] and
            row["pin_requests_total"] <= 6*row["pin_stage_count"],
            "checker memo performance contract")
    phases = row["phase_elapsed_seconds"]
    require(set(phases) == {"value_evaluation", "source_anchor_pin",
                            "candidate1_bridge_and_membership",
                            "ordinary_membership", "proof_regeneration"} and
            all(isinstance(value, (int, float)) and value >= 0
                for value in phases.values()),
            "checker memo phase timings")
    if partial:
        require(row["partial_resource_stop"] is True and
                # A cap can fire after the current membership evaluator or
                # prospective-PASS proof evaluator has been absorbed but
                # before its scan record is committed.  The one open
                # transaction is diagnostic, never an accepted candidate.
                row["candidate_evaluators"] <= evaluated+1 and
                row["proof_regeneration_evaluators"] <= pass_count+1 and
                row["candidate_memos_discarded_at_rollback"] <= evaluated+1,
                "checker partial memo accounting")
    else:
        require(len(records) == evaluated, "checker memo completed records")
        candidate1_pin = (1 if records and
                          records[0]["outcome_code"] != 1 else 0)
        ordinary_pin = sum(
            row["candidate_index"] > 1 and
            (row["outcome_code"] == 3 or
             (row["outcome_code"] == 2 and
              row["failed_target_ordinal"] >= 17))
            for row in records)
        direct_failures = sum(row["outcome_code"] == 1 for row in records)
        ordinary_early = sum(
            row["candidate_index"] > 1 and
            (row["outcome_code"] == 1 or
             (row["outcome_code"] == 2 and
              row["failed_target_ordinal"] < 17))
            for row in records)
        require(row["candidate_evaluators"] == evaluated and
                row["proof_regeneration_evaluators"] == pass_count and
                row["candidate_memos_discarded_at_rollback"] == evaluated and
                row["candidate1_bridge_pin_stages"] == candidate1_pin and
                row["ordinary_lazy_pin_stages"] == ordinary_pin and
                row["proof_pin_stages"] == pass_count and
                row["pin_requests_total"] == 6*row["pin_stage_count"] and
                row["direct_failures_before_pin"] == direct_failures and
                row["ordinary_exits_before_target17"] == ordinary_early,
                "checker completed memo accounting")


def pack_check_gradient(gradient: Vector, pool: ReplayPool) \
        -> dict[int, int]:
    out: dict[int, int] = {}
    for (component, element), coefficient in gradient.items():
        replay_add(out, replay_pack_key(component, pool.intern(element)),
                   coefficient)
    return out


def decode_wordexpr_scan(block: dict[str, Any], width: int) \
        -> dict[str, Any]:
    require(block["format"] == "registered-wordexpr-scan-arrays/v1" and
            isinstance(block["evaluated"], int) and
            0 <= block["evaluated"] <= CAPS["candidate_scan_records"] and
            block["element_width_bytes"] == width and
            block["outcome_codes"] == {
                "1": "direct_gate_or_acceptance_quotient_failure",
                "2": "fixed_basis_missing_pivot", "3": "PASS"},
            "checker scan header")
    arrays = block["arrays"]
    require(set(arrays) == {"candidate_index", "outcome_code",
                            "failed_target_ordinal", "blocker_component",
                            "blocker_value", "diagnostic_pass_count"},
            "checker scan arrays")
    n = block["evaluated"]
    indices = _decode_packed_array(arrays["candidate_index"], "uint32", "I",
                                   CAPS["candidate_scan_records"])
    outcomes = _decode_packed_array(arrays["outcome_code"], "uint8", "B",
                                    CAPS["candidate_scan_records"])
    ordinals = _decode_packed_array(arrays["failed_target_ordinal"],
                                    "uint8", "B",
                                    CAPS["candidate_scan_records"])
    components = _decode_packed_array(arrays["blocker_component"],
                                      "uint8", "B",
                                      CAPS["candidate_scan_records"])
    values = _decode_packed_array(
        arrays["blocker_value"], "fixed_width_bytes", "B",
        CAPS["candidate_scan_records"]*width)
    diag_counts = _decode_packed_array(arrays["diagnostic_pass_count"],
                                       "uint8", "B",
                                       CAPS["candidate_scan_records"])
    require(len(indices) == len(outcomes) == len(ordinals) ==
            len(components) == len(diag_counts) == n and
            len(values) == n*width and list(indices) == list(range(1, n+1)) and
            all(code in (1, 2, 3) for code in outcomes),
            "checker scan dimensions/order")
    manifest = {name: {key: value for key, value in row.items()
                       if key != "base64"} for name, row in arrays.items()}
    require(block["array_manifest_sha256"] == digest_obj(manifest) and
            block["evaluated_index_order_sha256"] ==
                digest_obj(list(range(1, n+1))) and
            isinstance(block["record_bindings"], list) and
            len(block["record_bindings"]) == n,
            "checker scan manifest/bindings")
    return {"indices": list(indices), "outcomes": list(outcomes),
            "ordinals": list(ordinals), "components": list(components),
            "values": bytes(values), "diag_counts": list(diag_counts)}


def replay_pivot_surgery(data: dict[str, Any], e4: Quotient,
                         targets: list[tuple[str, str, list[int]]],
                         frozen_source_tuple: Sequence[Element]) \
        -> tuple[ReplayPool, ReplayBasis]:
    """Independent full v6 prefix plus exact v7 directed-column replay."""
    directed = data["directed_surgery"]
    base_public, base_private = checker_base_occurrences(e4)
    require(data["directed_base_support"] == {
                "occurrences": base_public,
                "occurrence_count": len(base_public),
                "ordered_sha256": digest_obj(base_public),
                "order": "relator index, component, canonical E4 bytes",
                "all_prefix_sections_directly_replayed": True},
            "directed base support receipt")
    expression_values = decode_section_expressions(
        directed["section_expressions"], e4)

    pool = ReplayPool(e4)
    packed_columns: list[dict[int, int]] = []
    for relator in pure_relations(4):
        column, value = replay_fox_packed(relator, pool)
        require(value == pool.identity, "checker packed base relator")
        packed_columns.append(column)
    basis = ReplayBasis(pool, packed_columns)
    # Producer v9 constructs its base basis first, then persistently interns
    # these six values before either the 32,768-translation BFS or any target
    # probe.  IDs and candidate-local rollback counts are part of the receipt,
    # so the independent replay must use that exact schedule.
    seed_replay_source_anchors(pool, frozen_source_tuple)
    inserted: set[bytes] = set()

    def unscoped_first_missing() -> dict[str, Any] | None:
        for ordinal, (name, kind, word) in enumerate(targets, 1):
            gradient, value = replay_fox_packed(word, pool)
            require(value == pool.identity,
                    f"checker acceptance quotient identity: {name}")
            blocker_key = basis.solve(gradient)
            if blocker_key is not None:
                component, identifier = replay_unpack_key(blocker_key)
                blob = pool.values[identifier]
                return {"target_ordinal": ordinal, "target_name": name,
                        "target_kind": kind, "component": component,
                        "element_hex": blob.hex(),
                        "value": pool.unpack(blob)}
        return None

    def first_missing() -> dict[str, Any] | None:
        # Every corresponding producer probe is enclosed in a candidate
        # transaction.  Copying the immutable blob/value into the result and
        # rolling the pool back keeps the persistent BFS/directed prefix and
        # the later scan checkpoints byte-for-byte aligned.
        return transactional_replay_probe(pool, unscoped_first_missing)

    first_at_one: dict[str, Any] | None = None
    for ordinal, translation in enumerate(replay_translation_bfs(
            pool, CAPS["coefficient_translates_per_relator"]), 1):
        checker_deadline("fresh 32768 translation basis")
        for relator in range(1, 12):
            basis.add_column(relator, translation)
        inserted.add(pool.values[translation])
        if ordinal == 1:
            first_at_one = first_missing()
        if ordinal % 4096 == 0:
            print("B345_RELFRAT3_PIVOT_SURGERY_CHECKER_PREFIX "
                  f"translations={ordinal} pivots={len(basis.rows)}", flush=True)
    require(first_at_one is not None and
            first_at_one["target_ordinal"] == 6 and
            first_at_one["target_name"] == "hexagon_1_coface_0" and
            first_at_one["component"] == 4,
            "checker fresh checkpoint-1 blocker")

    translation_rows = directed["translations"]
    require(isinstance(translation_rows, list) and
            directed["translation_count"] == len(translation_rows) <=
            CAPS["directed_unique_translations"] and
            directed["translations_sha256"] == digest_obj(translation_rows),
            "directed translation ledger")
    rows_by_round: dict[int, list[dict[str, Any]]] = {}
    for expected_ordinal, row in enumerate(translation_rows, 1):
        require(row["ordinal"] == expected_ordinal and
                isinstance(row["round"], int) and row["round"] >= 1 and
                row["formula"] == "t=g*h^-1; left translation sends h to g" and
                isinstance(row["section_expression_root"], int) and
                0 <= row["section_expression_root"] < len(expression_values),
                "directed translation row schema")
        value_blob = bytes(expression_values[row["section_expression_root"]][0]) + \
            bytes(expression_values[row["section_expression_root"]][1])
        require(value_blob.hex() == row["translation_element_hex"],
                "directed translation section expression")
        rows_by_round.setdefault(row["round"], []).append(row)

    computed_columns: list[dict[str, Any]] = []
    rounds = directed["rounds"]
    require(isinstance(rounds, list) and
            directed["round_count"] == len(rounds) <=
            CAPS["directed_surgery_rounds"] and
            directed["rounds_sha256"] == digest_obj(rounds),
            "directed round ledger")
    passed = False
    for expected_round, claimed in enumerate(rounds, 1):
        checker_deadline("directed saturation replay", force=True)
        require(claimed["round"] == expected_round,
                "directed round order")
        missing = first_missing()
        if missing is None:
            require(claimed["outcome"] == "PASS" and
                    claimed["acceptance_targets_solved"] == 33 and
                    claimed["diagnostics_required"] is False and
                    expected_round == len(rounds),
                    "directed PASS round")
            passed = True
            break
        require(claimed["outcome"] == "RETRY" and
                claimed["failed_target_ordinal"] == missing["target_ordinal"] and
                claimed["failed_target_name"] == missing["target_name"] and
                claimed["failed_target_kind"] == missing["target_kind"] and
                claimed["blocker_component"] == missing["component"] and
                claimed["blocker_element_hex"] == missing["element_hex"] and
                claimed["blocker_value_sha256"] == hashlib.sha256(
                    bytes.fromhex(missing["element_hex"])).hexdigest() and
                isinstance(claimed["blocker_section_expression_root"], int) and
                0 <= claimed["blocker_section_expression_root"] <
                len(expression_values),
                "directed blocker replay")
        blocker_expr = expression_values[
            claimed["blocker_section_expression_root"]]
        require((bytes(blocker_expr[0])+bytes(blocker_expr[1])).hex() ==
                missing["element_hex"], "blocker section expression binding")
        recovery = claimed["blocker_recovery"]
        target_word = targets[missing["target_ordinal"]-1][2]
        raw_target, raw_value, raw_sections = fox_with_sections(target_word, e4)
        require(raw_value == e4.identity, "blocker recovery target quotient")
        if recovery["method"] == "target_support_prefix":
            require(recovery == {
                        "method": "target_support_prefix",
                        "component": missing["component"],
                        "element_hex": missing["element_hex"]} and
                    (missing["component"], missing["value"]) in raw_target and
                    missing["value"] in raw_sections,
                    "target-support blocker recovery")
        else:
            require(recovery["method"] ==
                    "registered_translation_times_base_prefix",
                    "raw-column blocker recovery method")
            source_rows = [row for row in base_private
                           if row["component"] == missing["component"] and
                           row["relator_index"] == recovery["relator_index"] and
                           row["element_hex"] == recovery["base_element_hex"]]
            require(len(source_rows) == 1, "blocker recovery base occurrence")
            h0 = source_rows[0]["_value"]
            t0 = e4.mul(missing["value"], e4.inverse(h0))
            t0_blob = bytes(t0[0])+bytes(t0[1])
            require(recovery == {
                        "method": "registered_translation_times_base_prefix",
                        "component": missing["component"],
                        "element_hex": missing["element_hex"],
                        "relator_index": source_rows[0]["relator_index"],
                        "base_element_hex": source_rows[0]["element_hex"],
                        "registered_translation_hex": t0_blob.hex()} and
                    t0_blob in inserted and e4.mul(t0, h0) == missing["value"],
                    "registered-translation blocker recovery")
        component = missing["component"]
        matching = [row for row in base_private
                    if row["component"] == component]
        matching.sort(key=lambda row: (row["relator_index"], row["component"],
                                       bytes.fromhex(row["element_hex"])))
        candidates: list[tuple[bytes, Element, dict[str, Any]]] = []
        seen_batch: set[bytes] = set()
        duplicate_count = 0
        for occurrence in matching:
            h = occurrence["_value"]
            translation = e4.mul(missing["value"], e4.inverse(h))
            blob = bytes(translation[0])+bytes(translation[1])
            require(e4.mul(translation, h) == missing["value"],
                    "checker left orientation")
            if blob in seen_batch or blob in inserted:
                duplicate_count += 1
                continue
            seen_batch.add(blob)
            candidates.append((blob, translation, occurrence))
        claimed_translations = rows_by_round.get(expected_round, [])
        require(len(claimed_translations) == len(candidates) and
                claimed["matching_base_occurrences"] == len(matching) and
                claimed["new_directed_translations"] == len(candidates) and
                claimed["duplicate_translations"] == duplicate_count,
                "directed canonical batch size")
        pivots_before = len(basis.rows)
        entries_before = basis.live_entries
        dependent_before = basis.dependent
        for claimed_translation, (blob, translation, occurrence) in zip(
                claimed_translations, candidates):
            require(claimed_translation["round"] == expected_round and
                    claimed_translation["component"] == component and
                    claimed_translation["blocker_element_hex"] ==
                        missing["element_hex"] and
                    claimed_translation["base_relator_index"] ==
                        occurrence["relator_index"] and
                    claimed_translation["base_element_hex"] ==
                        occurrence["element_hex"] and
                    claimed_translation["translation_element_hex"] == blob.hex(),
                    "directed translation formula/order")
            identifier = pool.intern(translation)
            for relator in range(1, 12):
                before = len(basis.rows)
                basis.add_column(relator, identifier)
                computed_columns.append({
                    "ordinal": len(computed_columns)+1,
                    "round": expected_round,
                    "translation_ordinal": claimed_translation["ordinal"],
                    "relator_index": relator,
                    "independent": len(basis.rows) > before,
                })
            inserted.add(blob)
        require(claimed["columns_attempted"] == 11*len(candidates) and
                claimed["columns_independent"] == len(basis.rows)-pivots_before and
                claimed["columns_dependent"] == basis.dependent-dependent_before and
                claimed["pivots_before"] == pivots_before and
                claimed["pivots_after"] == len(basis.rows) and
                claimed["live_sparse_entries_before"] == entries_before and
                claimed["live_sparse_entries_after"] == basis.live_entries,
                "directed elimination accounting")
        if not candidates:
            require(expected_round == len(rounds) and
                    directed["stop_reason"] ==
                    "no_new_exact_directed_translation",
                    "directed no-progress terminal")
            break

    if passed:
        require(directed["stop_reason"] is None,
                "directed PASS stop reason")
    elif rounds and rounds[-1]["outcome"] == "RETRY" and \
            rounds[-1]["new_directed_translations"] > 0:
        require(len(rounds) == CAPS["directed_surgery_rounds"] and
                directed["stop_reason"] ==
                    "directed_surgery_round_cap_exhausted",
                "directed round-cap terminal")

    require(directed["column_count"] == len(computed_columns) <=
            CAPS["directed_columns"] and
            directed["columns_sha256"] == digest_obj(computed_columns) and
            directed["column_order"] ==
                "translation first-seen order, relator 1..11",
            "directed column digest/order")
    theorem = directed["theorem"]
    require(theorem == {
                "field": 3, "left_Fox_translation": True,
                "formula": "t=g*h^-1 and t*h=g",
                "matching_order":
                    "relator index, component, canonical h bytes",
                "wrong_orientations_rejected":
                    ["h^-1*g", "g^-1*h", "right translation"],
                "complete_eleven_relator_block_per_new_translation": True},
            "directed theorem receipt")
    history = directed["blocker_history"]
    require(isinstance(history, list) and history and
            directed["blocker_history_sha256"] == digest_obj(history) and
            all(isinstance(row.get("section_expression_root"), int) and
                0 <= row["section_expression_root"] < len(expression_values) and
                (bytes(expression_values[row["section_expression_root"]][0])+
                 bytes(expression_values[row["section_expression_root"]][1])).hex()
                    == row["element_hex"] for row in history),
            "directed blocker history section bindings")
    referenced_expression_roots = {
        row["section_expression_root"] for row in translation_rows}
    referenced_expression_roots.update(
        row["section_expression_root"] for row in history)
    referenced_expression_roots.update(
        row["blocker_section_expression_root"] for row in rounds
        if row["outcome"] == "RETRY")
    require(referenced_expression_roots ==
            set(directed["section_expressions"]["roots"]),
            "directed section expression root coverage")
    oracle = directed["section_oracle"]
    require(oracle["persistent_roots"] ==
                "BFS and registered directed translations only" and
            oracle["base_D2_prefixes_frozen"] is True and
            oracle["candidate_target_prefixes_transient"] is True and
            oracle["blocker_recovery_complete_by_support_union"] is True and
            oracle["canonical_bytes_binding"] is True and
            oracle["pool_ID_binding_used"] is False and
            oracle["recovery_failure_is_hard_FAIL"] is True and
            oracle["expression_accounting"]["live_nodes"] <=
                CAPS["directed_section_expr_nodes"] and
            oracle["expression_accounting"]["live_edges"] <=
                CAPS["directed_section_expr_edges"],
            "sparse section oracle contract")
    require(directed["bounded_prefix_sha256"] == digest_obj({
                "translations": translation_rows,
                "columns_sha256": digest_obj(computed_columns),
                "blockers": history,
                "rounds": rounds}),
            "directed bounded prefix digest")
    stable_rounds = [
        {key: value for key, value in row.items()
         if key not in {"elapsed_seconds", "RSS_bytes"}}
        for row in rounds]
    require(not passed and directed["stop_reason"] ==
            "no_new_exact_directed_translation" and
            directed["stable_projection_omits_exactly"] ==
                ["elapsed_seconds", "RSS_bytes"] and
            directed["stable_rounds_projection"] == stable_rounds and
            directed["stable_rounds_projection_sha256"] ==
                digest_obj(stable_rounds) ==
                V7_PREFIX_BINDINGS["stable_rounds_projection_sha256"] and
            directed["volatile_rounds_sha256_provenance_only"] ==
                V7_PREFIX_BINDINGS["volatile_rounds_sha256_provenance_only"] and
            directed["translations_sha256"] ==
                V7_PREFIX_BINDINGS["translations_sha256"] and
            directed["columns_sha256"] ==
                V7_PREFIX_BINDINGS["columns_sha256"] and
            directed["blocker_history_sha256"] ==
                V7_PREFIX_BINDINGS["blocker_history_sha256"] and
            len(rounds) == 32 and len(translation_rows) == 207 and
            len(computed_columns) == 2277 and
            rounds[-1]["blocker_value_sha256"] ==
                V7_PREFIX_BINDINGS["final_blocker_sha256"] and
            rounds[-1]["new_directed_translations"] == 0 and
            basis.columns_seen == 362725 and len(basis.rows) == 362709,
            "fresh saturated v7 prefix stable binding")
    return pool, basis


def bounded_record_difference(actual: Any, expected: list[dict[str, Any]]) \
        -> dict[str, Any] | None:
    """Return only the first scan-row mismatch, never a 4096-row dump."""
    if not isinstance(actual, list):
        return {"candidate_index": None, "field": "record_bindings_type",
                "expected": "list", "actual": type(actual).__name__}
    if len(actual) != len(expected):
        return {"candidate_index": None, "field": "record_bindings_length",
                "expected": len(expected), "actual": len(actual)}

    def bounded(value: Any) -> Any:
        if value is None or isinstance(value, (bool, int, float)):
            return value
        if isinstance(value, str) and len(value) <= 96:
            return value
        return {"type": type(value).__name__, "sha256": digest_obj(value)}

    for ordinal, (got, want) in enumerate(zip(actual, expected), 1):
        if got == want:
            continue
        if not isinstance(got, dict):
            return {"candidate_index": ordinal, "field": "record_type",
                    "expected": "dict", "actual": type(got).__name__}
        keys = sorted(set(got) | set(want))
        for key in keys:
            if key not in got:
                return {"candidate_index": ordinal, "field": key,
                        "expected": bounded(want[key]), "actual": "<missing>"}
            if key not in want:
                return {"candidate_index": ordinal, "field": key,
                        "expected": "<absent>", "actual": bounded(got[key])}
            if got[key] != want[key]:
                return {"candidate_index": ordinal, "field": key,
                        "expected": bounded(want[key]),
                        "actual": bounded(got[key])}
        return {"candidate_index": ordinal, "field": "unknown_row_drift"}
    return None


def validate_wordexpr_scan(block: dict[str, Any], dictionary: dict[str, Any],
                           tuples: Sequence[tuple[Element, ...]],
                           frozen_tuple: tuple[Element, ...],
                           inverse_words: Sequence[Sequence[int]],
                           normalized: dict[str, Any], e4: Quotient,
                           pool: ReplayPool, basis: ReplayBasis,
                           candidate1_bridge: Any = None,
                           partial_resource: bool = False,
                           validation_setup: dict[str, Any] | None = None) \
        -> tuple[list[dict[str, Any]], dict[str, Any] | None]:
    # `validation_setup` replaces only the authenticated q3/fresh-basis
    # provider in the bounded self-test.  Both production and the sealed
    # provider enter this same decoder, replay loop, transaction validator,
    # and selected-candidate return path.
    if validation_setup is None:
        candidate_builder = build_check_wordexpr
        bridge_validator = check_flat_bridge
        candidate1_expected = {
            "outcome": "MISSING_PIVOT",
            "failed_target_ordinal": 6,
            "failed_name": "hexagon_1_coface_0",
            "blocker_component": 4,
            "blocker_value_sha256":
                V7_PREFIX_BINDINGS["final_blocker_sha256"],
        }
    else:
        require(set(validation_setup) == {
                    "candidate_builder", "bridge_validator",
                    "candidate1_expected", "trace"},
                "checker injected scan setup")
        candidate_builder = validation_setup["candidate_builder"]
        bridge_validator = validation_setup["bridge_validator"]
        candidate1_expected = validation_setup["candidate1_expected"]
        require(callable(candidate_builder) and callable(bridge_validator) and
                isinstance(candidate1_expected, dict) and
                isinstance(validation_setup["trace"], dict),
                "checker injected scan setup types")
        validation_setup["trace"]["scan_validator_entries"] = \
            validation_setup["trace"].get("scan_validator_entries", 0)+1
    decoded = decode_wordexpr_scan(block, pool.width)
    n = decoded["indices"][-1] if decoded["indices"] else 0
    base_keys = {"format", "evaluated", "complete", "element_width_bytes",
                 "outcome_codes", "arrays", "array_manifest_sha256",
                 "record_bindings", "record_bindings_sha256",
                 "evaluated_index_order_sha256", "failure_distribution"}
    if partial_resource:
        extra_keys = {"registered_corrections",
                      "registered_dictionary_complete",
                      "partial_resource_stop", "current",
                      "no_candidate_skip_interpreted_as_failure",
                      "transaction"}
        current = block.get("current")
        current_names = ([f"charming_error_coface_{i}" for i in range(5)] +
                         [f"hexagon_{j}_coface_{i}" for j in (1, 2)
                          for i in range(5)] + ["ordered_A18_pentagon"] +
                         [f"S_relation_{i}" for i in range(1, 12)] +
                         [f"ST_generator_{i}" for i in range(1, 7)])
        require(set(block) == base_keys | extra_keys and
                block["complete"] is False and
                block["partial_resource_stop"] is True and
                block["no_candidate_skip_interpreted_as_failure"] is True and
                isinstance(current, dict) and
                ((set(current) == {"candidate_index", "target_ordinal",
                                    "target_name"} and
                  current.get("candidate_index") == n+1) or
                 (set(current) == {"candidate_index", "target_ordinal",
                                    "target_name", "phase"} and n > 0 and
                  current.get("candidate_index") == n and
                  current.get("phase") ==
                    "positive_certificate_serialization")) and
                0 <= current.get("target_ordinal", -1) <= 33 and
                ((current["target_ordinal"] == 0 and
                  current.get("target_name") is None) or
                 (current["target_ordinal"] > 0 and
                  current.get("target_name") ==
                    current_names[current["target_ordinal"]-1])),
                "checker partial scan exact schema/current")
    else:
        extra_keys = {"registered_corrections",
                      "registered_dictionary_complete",
                      "full_H3_fibre_complete", "full_universe_claimed",
                      "earliest_global_candidate_claimed",
                      "negative_completeness_claimed", "candidate_order",
                      "candidate_order_sha256",
                      "candidate_order_equals_frozen_v8",
                      "acceptance_target_count", "diagnostic_target_count",
                      "candidate1_bridge_membership_fused",
                      "fixed_basis_immutable_during_scan",
                      "membership_first_pass_allocates_provenance_nodes",
                      "transaction", "runtime_seconds"}
        require(set(block) == base_keys | extra_keys and
                block["full_H3_fibre_complete"] is False and
                block["full_universe_claimed"] is False and
                block["earliest_global_candidate_claimed"] is False and
                block["negative_completeness_claimed"] is False and
                block["candidate_order"] ==
                    "1..4096 exactly once after saturated v7 prefix" and
                block["candidate_order_sha256"] ==
                    digest_obj([digest_obj(word)
                                for word in dictionary["words"]]) and
                block["candidate_order_equals_frozen_v8"] is True and
                block["acceptance_target_count"] == 33 and
                block["diagnostic_target_count"] == 17 and
                block["candidate1_bridge_membership_fused"] is True and
                block["fixed_basis_immutable_during_scan"] is True and
                block["membership_first_pass_allocates_provenance_nodes"] is
                    False and
                isinstance(block["runtime_seconds"], (int, float)) and
                block["runtime_seconds"] >= 0,
                "checker completed scan exact schema/claim boundary")
    require(block["registered_corrections"] == 4096 and
            block["registered_dictionary_complete"] is True,
            "checker scan registered universe")
    expected_records: list[dict[str, Any]] = []
    selected: dict[str, Any] | None = None
    zero_blob = element_blob(e4.identity)
    max_suffix = 0; max_live = 0

    for index in range(1, n+1):
        checker_deadline("registered WordExpr scan", force=(index == 1))
        checkpoint = pool.checkpoint()
        compiled = candidate_builder(index, dictionary["words"][index-1],
                                     inverse_words)
        dag: CheckWordExpr = compiled["dag"]
        evaluator = CheckWordExprEvaluator(dag, e4)
        evaluator.evaluate_values()
        require(tuple(evaluator.values[root-1]
                      for root in compiled["source_roots"]) ==
                tuples[index-1] == frozen_tuple,
                "checker direct source tuple expression replay")
        diagnostics = check_expr_diagnostics(compiled, evaluator)
        diag_pass = sum(row["quotient_identity"] for row in diagnostics)
        diag_sha = digest_obj(diagnostics)
        if index == 1:
            validate_candidate1_bridge(
                candidate1_bridge,
                bridge_validator(compiled, evaluator, e4, normalized),
                compiled, e4, inverse_words)
        failure_name, failure_ordinal = check_direct_failure(
            compiled, evaluator)
        roots = [root for _, _, root in
                 compiled["acceptance"]+compiled["diagnostics"]]
        accounting = dag.accounting(roots)
        expression_sha = check_expr_digest(dag)
        if failure_name is not None:
            removed = pool.rollback(checkpoint)
            record = {
                "candidate_index": index, "outcome": "QUOTIENT_FAILURE",
                "outcome_code": 1, "failed_name": failure_name,
                "failed_target_ordinal": failure_ordinal,
                "blocker_component": 0,
                "blocker_value_hex": zero_blob.hex(),
                "blocker_value_sha256": hashlib.sha256(zero_blob).hexdigest(),
                "gradient_entry_count": 0,
                "diagnostic_pass_count": diag_pass,
                "diagnostic_values_sha256": diag_sha,
                "wordexpr_sha256": expression_sha,
                "wordexpr_nodes": accounting["node_count"],
                "wordexpr_edges": accounting["edge_count"],
                "wordexpr_max_expanded_letters":
                    accounting["max_expanded_letter_count"],
                "pool_suffix_removed": removed,
            }
        else:
            bindings: list[dict[str, Any]] = []
            missing: int | None = None; failed_name = ""; failed_kind = ""
            failed_ordinal = 0; entries = 0
            for ordinal, (name, kind, root) in enumerate(
                    compiled["acceptance"], 1):
                gradient = evaluator.gradients([root])[root]
                value = evaluator.values[root-1]
                require(value == e4.identity,
                        "checker acceptance identity after direct gate")
                binding = check_gradient_binding(name, kind, gradient, value)
                bindings.append(binding); entries += len(gradient)
                packed = pack_check_gradient(gradient, pool)
                max_suffix = max(max_suffix, len(pool.values)-checkpoint)
                require(len(pool.values)-checkpoint <=
                        CAPS["candidate_element_pool_suffix"],
                        "checker candidate pool suffix cap")
                missing = basis.solve(packed)
                if missing is not None:
                    failed_name, failed_kind, failed_ordinal = name, kind, ordinal
                    break
            max_live = max(max_live, evaluator.target_gradient_entry_peak)
            if missing is not None:
                component, identifier = replay_unpack_key(missing)
                blocker = pool.values[identifier]
                removed = pool.rollback(checkpoint)
                record = {
                    "candidate_index": index, "outcome": "MISSING_PIVOT",
                    "outcome_code": 2, "failed_name": failed_name,
                    "failed_kind": failed_kind,
                    "failed_target_ordinal": failed_ordinal,
                    "blocker_component": component,
                    "blocker_value_hex": blocker.hex(),
                    "blocker_value_sha256": hashlib.sha256(blocker).hexdigest(),
                    "gradient_entry_count": entries,
                    "failed_gradient_entry_count": bindings[-1]["entry_count"],
                    "gradient_bindings_sha256": digest_obj(bindings),
                    "diagnostic_pass_count": diag_pass,
                    "diagnostic_values_sha256": diag_sha,
                    "wordexpr_sha256": expression_sha,
                    "wordexpr_nodes": accounting["node_count"],
                    "wordexpr_edges": accounting["edge_count"],
                    "wordexpr_max_expanded_letters":
                        accounting["max_expanded_letter_count"],
                    "wordexpr_live_gradient_peak":
                        evaluator.target_gradient_entry_peak,
                    "pool_suffix_removed": removed,
                }
            else:
                # Producer rolls back the membership-only phase and then
                # regenerates solely to allocate a selected proof.  The scan
                # record is completely determined before that allocation.
                removed = pool.rollback(checkpoint)
                record = {
                    "candidate_index": index, "outcome": "PASS",
                    "outcome_code": 3, "failed_name": "",
                    "failed_target_ordinal": 0, "blocker_component": 0,
                    "blocker_value_hex": zero_blob.hex(),
                    "blocker_value_sha256": hashlib.sha256(zero_blob).hexdigest(),
                    "gradient_entry_count": entries,
                    "gradient_bindings_sha256": digest_obj(bindings),
                    "diagnostic_pass_count": diag_pass,
                    "diagnostic_values_sha256": diag_sha,
                    "wordexpr_sha256": expression_sha,
                    "wordexpr_nodes": accounting["node_count"],
                    "wordexpr_edges": accounting["edge_count"],
                    "wordexpr_max_expanded_letters":
                        accounting["max_expanded_letter_count"],
                    "wordexpr_live_gradient_peak":
                        evaluator.target_gradient_entry_peak,
                    "pool_suffix_removed": removed,
                }
                selected = {"compiled": compiled, "evaluator": evaluator,
                            "bindings": bindings}
        expected_records.append(record)
        if index == 1:
            require(all(record.get(key) == value for key, value in
                        candidate1_expected.items()),
                    "checker candidate1 saturated blocker drift")
        require(decoded["outcomes"][index-1] == record["outcome_code"] and
                decoded["ordinals"][index-1] ==
                    record["failed_target_ordinal"] and
                decoded["components"][index-1] ==
                    record["blocker_component"] and
                decoded["values"][(index-1)*pool.width:index*pool.width] ==
                    bytes.fromhex(record["blocker_value_hex"]) and
                decoded["diag_counts"][index-1] ==
                    record["diagnostic_pass_count"],
                "checker scan packed outcome replay")
        if selected is not None:
            require(index == n, "checker scan continued after PASS")
            break

    public = [{key: value for key, value in row.items()
               if key != "blocker_value_hex"} for row in expected_records]
    distribution: dict[str, int] = {}
    for row in expected_records:
        label = row["outcome"]+":"+row.get("failed_name", "")
        distribution[label] = distribution.get(label, 0)+1
    difference = bounded_record_difference(block["record_bindings"], public)
    require(difference is None,
            "checker scan record_bindings first_difference=" +
            json.dumps(difference, sort_keys=True, separators=(",", ":")))
    require(block["record_bindings_sha256"] == digest_obj(expected_records),
            "checker scan record_bindings_sha256")
    require(block["failure_distribution"] == distribution,
            "checker scan failure_distribution")
    require(block["complete"] ==
            (selected is None and n == 4096 and not partial_resource),
            "checker scan completion equivalence")
    tx = block["transaction"]
    pass_count = sum(row["outcome_code"] == 3 for row in expected_records)
    exact_tx = {
        "membership_starts": n, "membership_rollbacks": n,
        "proof_starts": pass_count, "proof_commits": pass_count,
        "proof_rollbacks": 0, "failed_candidate_DAG_nodes_allocated": 0,
        "max_pool_suffix": max_suffix,
        "max_live_gradient_entries": max_live}
    if partial_resource:
        require(set(tx) == set(exact_tx) and
                tx["membership_starts"] in {n, n+1} and
                n <= tx["membership_rollbacks"] <= tx["membership_starts"] and
                tx["proof_starts"] >= tx["proof_commits"] >= pass_count and
                tx["proof_rollbacks"] >= 0 and
                tx["failed_candidate_DAG_nodes_allocated"] == 0 and
                tx["max_pool_suffix"] >= max_suffix and
                tx["max_live_gradient_entries"] >= max_live,
                "checker partial scan transaction accounting")
    else:
        require(tx == exact_tx, "checker scan transaction accounting")
    return expected_records, selected


def validate_selected_wordexpr(data: dict[str, Any],
                               selected: dict[str, Any],
                               inverse_words: Sequence[Sequence[int]],
                               e3: Quotient, e4: Quotient, *,
                               validation_setup: dict[str, Any] | None = None) \
        -> None:
    # This is the single production selected-proof entry.  The sealed test
    # may inject only the expensive registry/model leaf provider; it still
    # traverses the production typed-DAG, 33/17, source-root, certificate,
    # packed-proof, and scan-binding checks below.
    if validation_setup is not None:
        require(set(validation_setup) == {
                    "leaf_resolver", "expected_registry",
                    "expected_fox_models", "trace"} and
                callable(validation_setup["leaf_resolver"]) and
                isinstance(validation_setup["trace"], dict),
                "checker injected selected setup")
        validation_setup["trace"]["selected_validator_entries"] = \
            validation_setup["trace"].get("selected_validator_entries", 0)+1
    compiled = selected["compiled"]
    evaluator: CheckWordExprEvaluator = selected["evaluator"]
    named = ([(name, root) for name, _, root in
              compiled["acceptance"]+compiled["diagnostics"]] +
             [(f"source_{i+1}", root)
              for i, root in enumerate(compiled["source_roots"])] +
             list(compiled["correction_coface_roots"]))
    expected_expr = compiled["dag"].serialize(named)
    require(data["selected_wordexpr_dag"] == expected_expr,
            "checker selected WordExpr table rebuild")
    root_ids = {row["name"]: row["node_id"]
                for row in expected_expr["roots"]}
    pair = data["selected_pair"]
    require(set(pair) == {
                "correction_index", "correction_word",
                "correction_word_sha256", "candidate_word",
                "candidate_word_sha256", "candidate_exponent_sums",
                "fixed_inverse_words", "fixed_inverse_words_sha256",
                "source_expression_roots", "diagnostics",
                "correction_coarse_J_H_coface_gates",
                "correction_coarse_J_H_all_five",
                "correction_in_finer_J_Phi_required",
                "diagnostics_feed_acceptance", "acceptance_target_count",
                "diagnostic_target_count",
                "T_canaries_required_for_acceptance",
                "corrected_Def2_9_IF_FIRST_frozen_pre_run",
                "operational_first_passing_registered_index",
                "mathematical_minimality_claimed", "charming_witness",
                "friendly_gate", "marking_gate", "outside_roof_gate"} and
            pair["correction_index"] == compiled["correction_index"] and
            pair["correction_word"] == compiled["correction_word"] and
            pair["correction_word_sha256"] ==
                digest_obj(compiled["correction_word"]) and
            pair["candidate_word"] == compiled["candidate_word"] and
            pair["candidate_word_sha256"] ==
                digest_obj(compiled["candidate_word"]) and
            pair["candidate_exponent_sums"] == [0, 0] and
            pair["fixed_inverse_words"] == [list(x) for x in inverse_words] and
            pair["fixed_inverse_words_sha256"] == digest_obj(inverse_words) and
            pair["source_expression_roots"] ==
                [root_ids[f"source_{i}"] for i in range(1, 7)] and
            pair["diagnostics"] == check_expr_diagnostics(
                compiled, evaluator, root_ids) and
            pair["acceptance_target_count"] == 33 and
            pair["diagnostic_target_count"] == 17 and
            pair["T_canaries_required_for_acceptance"] is False and
            pair["corrected_Def2_9_IF_FIRST_frozen_pre_run"] is True and
            pair["diagnostics_feed_acceptance"] is False and
            pair["mathematical_minimality_claimed"] is False and
            pair["charming_witness"] == compiled["charming_witness"],
            "checker selected pair expression/direct metadata")
    correction = []
    for name, root in compiled["correction_coface_roots"]:
        value = evaluator.values[root-1]
        correction.append({
            "name": name, "wordexpr_root_node_id": root_ids[name],
            "quotient_value_hex": element_blob(value).hex(),
            "quotient_identity": value == e4.identity})
    require(pair["correction_coarse_J_H_coface_gates"] == correction and
            pair["correction_coarse_J_H_all_five"] is True and
            pair["correction_in_finer_J_Phi_required"] is False and
            all(row["quotient_identity"] for row in correction) and
            pair["friendly_gate"] == {
                "m": 0, "lambda": 1,
                "frozen_q3_selected_solution_replayed": True,
                "all_five_coarse_correction_cofaces_identity": True} and
            pair["marking_gate"] == {"m": 0, "lambda": 1,
                                      "additional_residuals": []} and
            pair["outside_roof_gate"] ==
                data["registered_universe"]["fixed_outside_roof"],
            "checker selected coface/friendly/marking/outside gates")

    proof = data["boundary_proof_dag"]
    section_values = decode_section_expressions(proof["section_expressions"], e4)
    if validation_setup is None:
        by_id, reverse = validate_registry(data["quotient_element_registry"],
                                           {3: e3, 4: e4}, section_values)
        models = validate_fox_models(data["fox_models"], e3, e4, reverse)

        def proof_leaf(node: dict[str, Any]) -> Vector:
            relator = node["relator_index"]
            translation_id = node["translation_element_id"]
            require(1 <= relator <= len(models[4]) and
                    translation_id in by_id and
                    reverse.get((4, by_id[translation_id])) == translation_id,
                    "checker selected proof leaf typing")
            referenced.add(translation_id)
            return translate(models[4][relator-1], by_id[translation_id], e4)
    else:
        require(data["quotient_element_registry"] ==
                    validation_setup["expected_registry"] and
                data["fox_models"] ==
                    validation_setup["expected_fox_models"] and
                section_values == [],
                "checker injected selected dependency binding")
        proof_leaf = validation_setup["leaf_resolver"]
    names = [name for name, _, _ in compiled["acceptance"]]
    referenced: set[int] = set()
    if validation_setup is not None:
        validation_setup["trace"]["proof_validator_entries"] = \
            validation_setup["trace"].get("proof_validator_entries", 0)+1
    proof_vectors, proof_roots = evaluate_proof_dag(
        proof, names, proof_leaf)
    certificates = data["boundary_certificates"]
    require([row["name"] for row in certificates] == names and
            len(certificates) == 33, "checker selected certificate order")
    expected_bindings = []
    for cert, (name, kind, root) in zip(certificates,
                                        compiled["acceptance"]):
        gradient = evaluator.gradients([root])[root]
        value = evaluator.values[root-1]
        binding = check_gradient_binding(name, kind, gradient, value)
        expected_bindings.append(binding)
        require(set(cert) == {"name", "kind", "wordexpr_root_node_id",
                              "quotient_identity", "gradient_binding",
                              "proof_root_node_id", "proof_system"} and
                cert == {"name": name, "kind": kind,
                         "wordexpr_root_node_id": root_ids[name],
                         "quotient_identity": True,
                         "gradient_binding": binding,
                         "proof_root_node_id": proof_roots[name],
                         "proof_system":
                             "shared_topological_F3_provenance_DAG"} and
                value == e4.identity and boundary1(gradient, e4) == {} and
                proof_vectors[name] == gradient,
                f"checker selected boundary proof {name}")
    require(expected_bindings == selected["bindings"] and
            data["wordexpr_scan"]["record_bindings"][-1]
                ["gradient_bindings_sha256"] == digest_obj(expected_bindings),
            "checker selected gradient binding regeneration")


def validate_v8_scan_selected_core(
        data: dict[str, Any], dictionary: dict[str, Any],
        tuples: Sequence[tuple[Element, ...]],
        frozen_tuple: tuple[Element, ...],
        inverse_words: Sequence[Sequence[int]], normalized: dict[str, Any],
        e3: Quotient, e4: Quotient, pool: ReplayPool, basis: ReplayBasis, *,
        scan_setup: dict[str, Any] | None = None,
        selected_setup: dict[str, Any] | None = None) -> None:
    """Shared production scan/selected-proof validation core.

    Production supplies the authenticated q3 and freshly replayed v7 basis.
    The bounded self-test may inject those expensive dependencies, but cannot
    replace this function, the packed scan decoder, or the selected proof
    validator it invokes.
    """
    token = data["terminal_token"]
    block = data.get("wordexpr_scan")
    require(isinstance(block, dict), "v8 scan receipt")
    partial = token == "B345_RELFRAT3_WORDEXPR_UNKNOWN_RESOURCE"
    if block.get("evaluated") == 0 and partial and "arrays" not in block:
        current0 = block.get("current")
        tx0 = block.get("transaction")
        current_names0 = ([f"charming_error_coface_{i}" for i in range(5)] +
                          [f"hexagon_{j}_coface_{i}" for j in (1, 2)
                           for i in range(5)] + ["ordered_A18_pentagon"] +
                          [f"S_relation_{i}" for i in range(1, 12)] +
                          [f"ST_generator_{i}" for i in range(1, 7)])
        require(set(block) == {"format", "evaluated", "complete",
                               "registered_corrections",
                               "registered_dictionary_complete",
                               "partial_resource_stop", "current",
                               "no_candidate_skip_interpreted_as_failure",
                               "transaction"} and
                block["format"] == "registered-wordexpr-scan-arrays/v1" and
                block["complete"] is False and
                block["registered_corrections"] == 4096 and
                block["registered_dictionary_complete"] is True and
                block["partial_resource_stop"] is True and
                block["no_candidate_skip_interpreted_as_failure"] is True and
                isinstance(current0, dict) and
                set(current0) == {"candidate_index", "target_ordinal",
                                  "target_name"} and
                current0["candidate_index"] == 1 and
                0 <= current0["target_ordinal"] <= 33 and
                ((current0["target_ordinal"] == 0 and
                  current0["target_name"] is None) or
                 (current0["target_ordinal"] > 0 and
                  current0["target_name"] ==
                    current_names0[current0["target_ordinal"]-1])) and
                isinstance(tx0, dict) and
                set(tx0) == {"membership_starts", "membership_rollbacks",
                             "proof_starts", "proof_commits",
                             "proof_rollbacks",
                             "failed_candidate_DAG_nodes_allocated",
                             "max_pool_suffix",
                             "max_live_gradient_entries"} and
                tx0["membership_starts"] == 1 and
                tx0["membership_rollbacks"] == 0 and
                tx0["proof_starts"] == tx0["proof_commits"] ==
                    tx0["proof_rollbacks"] == 0 and
                tx0["failed_candidate_DAG_nodes_allocated"] == 0,
                "v8 zero-prefix resource scan")
        if "gradient_memo_performance" in data:
            validate_gradient_memo_performance(
                data, evaluated=0, pass_count=0, partial=True, records=())
        return
    require(data["candidate1_flat_bridge"]["mandatory"] is True,
            "v8 candidate1 bridge receipt")
    records, selected = validate_wordexpr_scan(
        block, dictionary, tuples, frozen_tuple, inverse_words,
        normalized, e4, pool, basis, data["candidate1_flat_bridge"], partial,
        scan_setup)
    validate_gradient_memo_performance(
        data, evaluated=len(records),
        pass_count=sum(row["outcome_code"] == 3 for row in records),
        partial=partial, records=records)
    if partial:
        require(data["reason"] in RESOURCE_REASONS and
                data["resource_stop"]["cap"] == data["reason"] and
                data["resource_stop"]["no_mathematical_obstruction_claimed"]
                    is True and
                block["complete"] is False and
                block["partial_resource_stop"] is True,
                "v8 partial resource terminal")
        return
    search = data["search"]
    evaluated = len(records)
    require(search["registered_correction_indices"] ==
                list(range(1, evaluated+1)) and
            search["other_corrections_constructed_or_evaluated"] ==
                max(0, evaluated-1) and
            search["correction_dictionary_constructed"] is True and
            search["complete_source_tuple_DP_executed"] is True and
            search["candidate_membership_tests"] == evaluated and
            search["candidate_target_streaming"] is True and
            search["persistent_candidate_cache_size"] == 0 and
            search["persistent_candidate_gradient_entries"] == 0 and
            search["candidate_local_gradient_memo"] is True and
            search["candidate_local_gradient_memo_cross_candidate_entries"] == 0 and
            search["source_anchor_pin_policy_stage_aware"] is True and
            search["ordinary_lazy_pin_target_ordinal"] == 17 and
            search["cache_capacity_is_nonterminal"] is True and
            search["candidate_1_flat_bridge_membership_fused"] is True and
            search["candidate_1_missing_target_re_evaluated"] is False and
            search["failed_candidate_provenance_nodes_allocated"] == 0 and
            search["selected_candidate_regenerated_and_exactly_compared"] ==
                (selected is not None),
            "v8 completed scan search-accounting binding")
    if selected is None:
        require(token == "B345_RELFRAT3_WORDEXPR_SEARCH_INCOMPLETE" and
                data["reason"] == "registered_dictionary_exhausted" and
                len(records) == 4096 and block["complete"] is True and
                data["direct_lane"] == {
                    "literal_pair_found": False,
                    "reason":
                        "all registered corrections failed in the fixed saturated basis",
                    "not_nonmembership": True, "not_obstruction": True},
                "v8 registered exhaustion terminal")
        return
    require(token == "B345_RELFRAT3_WORDEXPR_PASS" and
            block["complete"] is False and records[-1]["outcome"] == "PASS" and
            data["selected_pair"]["operational_first_passing_registered_index"] ==
                selected["compiled"]["correction_index"],
            "v8 positive scan terminal")
    validate_selected_wordexpr(
        data, selected, inverse_words, e3, e4,
        validation_setup=selected_setup)


def validate_v8_claims(data: dict[str, Any]) -> None:
    token = data.get("terminal_token")
    require(token in TERMINALS and data.get("status") == token and
            data.get("claim_scope") ==
                "registered_4096_wordexpr_positive_search_only" and
            data.get("no_mathematical_obstruction_claimed") is True and
            data.get("full_universe_claimed") is False and
            data.get("negative_claimed") is False,
            "v8 terminal and claim boundary")
    if token == "B345_RELFRAT3_WORDEXPR_PASS":
        require(data.get("claim_classification") == "positive_certificate" and
                data.get("direct_lane") == {
                    "literal_pair_found": True,
                    "PB5_branch_constructed": False,
                    "stop_reason": "FIRST_REGISTERED_WORDEXPR_LITERAL_PAIR"} and
                all(key in data for key in
                    ("selected_pair", "selected_wordexpr_dag",
                     "boundary_certificates", "boundary_proof_dag")),
                "v8 positive terminal schema")
    else:
        require(data.get("claim_classification") ==
                    "unknown_not_obstruction" and
                all(key not in data for key in
                    ("selected_pair", "selected_wordexpr_dag",
                     "boundary_certificates", "boundary_proof_dag")),
                "v8 nonpositive claim/proof boundary")


def validate_v8_pins(data: dict[str, Any], q3_path: Path, repo: Path,
                     allow_input_mismatch: bool) -> None:
    pins = data["pins"]
    require(set(pins) == {"q3_producer", "q3_checker", "q3_driver",
                          "q3_artifact", "formula_sha256",
                          "semantic_reference_v1", "semantic_reference_v2",
                          "semantic_reference_v3", "semantic_reference_v4",
                          "semantic_reference_v5", "semantic_reference_v6",
                          "semantic_reference_v7",
                          "semantic_reference_v8"}, "v9 pin key set")
    base = (("q3_producer", Q3_PRODUCER, Q3_PRODUCER_SHA),
            ("q3_checker", Q3_CHECKER, Q3_CHECKER_SHA),
            ("q3_driver", Q3_DRIVER, Q3_DRIVER_SHA))
    mismatches: list[tuple[str, str, str]] = []
    for key, path, sha in base:
        require(pins[key] == {"path": str(path).replace("\\", "/"),
                              "sha256": sha}, f"v8 {key} receipt pin")
        got = "MISSING" if not (repo/path).is_file() else digest_file(repo/path)
        if got != sha:
            mismatches.append((key, sha, got))
    require(pins["q3_artifact"] == {
                "path": str(Q3_ARTIFACT_PATH).replace("\\", "/"),
                "sha256": Q3_ARTIFACT_SHA} and
            pins["formula_sha256"] == FORMULA_SHA,
            "v8 q3 artifact/formula receipt pins")
    got_q3 = "MISSING" if not q3_path.is_file() else digest_file(q3_path)
    if got_q3 != Q3_ARTIFACT_SHA:
        mismatches.append(("q3 artifact", Q3_ARTIFACT_SHA, got_q3))
    references = (
        ("semantic_reference_v8", V8_PRODUCER, V8_PRODUCER_SHA,
         V8_CHECKER, V8_CHECKER_SHA, V8_DRIVER, V8_DRIVER_SHA,
         "frozen candidate order, 33/17 predicate, WordExpr/Fox and terminal reference"),
        ("semantic_reference_v7", V7_PRODUCER, V7_PRODUCER_SHA,
         V7_CHECKER, V7_CHECKER_SHA, V7_DRIVER, V7_DRIVER_SHA,
         "frozen saturated directed prefix and corrected Def2.9 reference"),
        ("semantic_reference_v6", V6_PRODUCER, V6_PRODUCER_SHA,
         V6_CHECKER, V6_CHECKER_SHA, V6_DRIVER, V6_DRIVER_SHA,
         "frozen full-32768 fixed-candidate basis and cap reference"),
        ("semantic_reference_v5", V5_PRODUCER, V5_PRODUCER_SHA,
         V5_CHECKER, V5_CHECKER_SHA, V5_DRIVER, V5_DRIVER_SHA,
         "frozen fixed-candidate v5 semantics and cap-stop reference"),
        ("semantic_reference_v4", V4_PRODUCER, V4_PRODUCER_SHA,
         V4_CHECKER, V4_CHECKER_SHA, V4_DRIVER, V4_DRIVER_SHA,
         "frozen transactional-v4 arithmetic, Fox, blocker, and packed-certificate reference"),
        ("semantic_reference_v3", V3_PRODUCER, V3_PRODUCER_SHA,
         V3_CHECKER, V3_CHECKER_SHA, V3_DRIVER, V3_DRIVER_SHA,
         "frozen packed-v3 semantics and positive-certificate reference"),
        ("semantic_reference_v2", V2_PRODUCER, V2_PRODUCER_SHA,
         V2_CHECKER, V2_CHECKER_SHA, V2_DRIVER, V2_DRIVER_SHA,
         "frozen v2 mathematics, universe, gates, and search order"),
        ("semantic_reference_v1", V1_PRODUCER, V1_PRODUCER_SHA,
         V1_CHECKER, V1_CHECKER_SHA, V1_DRIVER, V1_DRIVER_SHA,
         "frozen semantic predicate and search-order reference"))
    for key, producer, psha, checker, csha, driver, dsha, role in references:
        require(pins[key] == {
                    "producer": {"path": str(producer).replace("\\", "/"),
                                 "sha256": psha},
                    "checker": {"path": str(checker).replace("\\", "/"),
                                "sha256": csha},
                    "driver": {"path": str(driver).replace("\\", "/"),
                               "sha256": dsha}, "role": role},
                f"v8 {key} receipt")
        for label, path, sha in ((f"{key} producer", producer, psha),
                                 (f"{key} checker", checker, csha),
                                 (f"{key} driver", driver, dsha)):
            got = "MISSING" if not (repo/path).is_file() else digest_file(repo/path)
            if got != sha:
                mismatches.append((label, sha, got))
    require((not mismatches) or allow_input_mismatch,
            "v8 authenticated dependency pin mismatch")
    if allow_input_mismatch:
        reported = {(row["label"], row["expected_sha256"], row["got"])
                    for row in data.get("input_errors", [])}
        require(set(mismatches) <= reported and bool(reported),
                "v8 UNKNOWN_INPUT mismatch ledger")


def validate_v8_receipt(data: dict[str, Any], q3: dict[str, Any],
                        q3_path: Path, repo: Path, *,
                        sealed_selftest: bool = False) -> None:
    # The sealed flag may inject only the expensive authenticated-q3/fresh-v7
    # setup.  It does not select a receipt schema or validator: the receipt
    # below must have the production v8 envelope and later enters the same scan
    # decoder and selected proof core as main().
    injected_setup = q3.get("_sealed_validation_context") \
        if sealed_selftest else None
    if sealed_selftest:
        require(isinstance(injected_setup, dict),
                "v8 sealed dependency provider")
        injected_setup["trace"]["envelope_validator_entries"] = \
            injected_setup["trace"].get("envelope_validator_entries", 0)+1
    base_keys = {"schema", "status", "terminal_token", "reason", "pins",
                 "source_hashes", "input_q3_terminal", "output_path", "caps",
                 "registered_universe", "representation_contract",
                 "claim_classification", "claim_scope",
                 "no_mathematical_obstruction_claimed",
                 "full_universe_claimed", "negative_claimed",
                 "theorem_boundary", "prohibited_work", "cap_calibration",
                 "resource_guards", "performance"}
    allowed = base_keys | {
        "input_errors", "bounded_search_prefix", "formula_sha256",
        "relevant_formula", "relevant_formula_sha256", "matched_quotients",
        "base_q3_replay", "correction_dictionary",
        "normalized_inverse_fibre", "source_tuple_preflight", "scan",
        "fixed_candidate_preflight", "directed_base_support",
        "directed_surgery", "directed_surgery_prefix", "blocker_table",
        "blocker_history", "checkpoint_trace", "pivot_introductions",
        "direct_vs_preflight_comparisons", "search", "candidate1_flat_bridge",
        "wordexpr_scan", "direct_lane", "resource_stop",
        "resource_accounting_at_stop", "quotient_element_registry",
        "fox_models", "boundary_proof_dag", "selected_wordexpr_dag",
        "selected_pair", "boundary_certificates", "literal_replay"}
    allowed.add("gradient_memo_performance")
    require(base_keys <= set(data) and set(data) <= allowed,
            "v8 exact top-level layout")
    require(data.get("schema") == SCHEMA and data.get("caps") == CAPS and
            data.get("output_path") == str(OUTPUT_PATH).replace("\\", "/") and
            data.get("input_q3_terminal") == q3.get("terminal_token") and
            data.get("cap_calibration") == CAP_CALIBRATION,
            "v8 schema/caps/input/output")
    validate_v8_claims(data)
    token = data["terminal_token"]
    is_input = token == "B345_RELFRAT3_WORDEXPR_UNKNOWN_INPUT"
    if injected_setup is None:
        validate_v8_pins(data, q3_path, repo, is_input)
    else:
        require(data["pins"] == injected_setup["expected_pins"],
                "v8 sealed external dependency injection")
    source = data["source_hashes"]
    require(source == {
                "producer_sha256": digest_file(repo/V9_PRODUCER),
                "checker_sha256": digest_file(repo/V9_CHECKER),
                "driver_sha256": digest_file(repo/V9_DRIVER)},
            "v8 source hash binding")
    guard = data["resource_guards"]
    require(guard["seconds"] == guard["minutes"]*60 == 7200 and
            guard["rss_bytes"] == CAPS["producer_soft_rss_bytes"] and
            guard["external_job_limit_minutes"] == 330 and
            guard["terminal_on_hit"] ==
                "B345_RELFRAT3_WORDEXPR_UNKNOWN_RESOURCE" and
            guard["hit"] ==
                (token == "B345_RELFRAT3_WORDEXPR_UNKNOWN_RESOURCE"),
            "v8 resource guard contract")
    if is_input:
        require(data["reason"] == "authenticated_input_pin_mismatch" and
                "input_errors" in data, "v8 UNKNOWN_INPUT reason")
        return

    if injected_setup is None:
        require(digest_file(q3_path) == Q3_ARTIFACT_SHA and
                digest_obj(q3["formulas"]) == FORMULA_SHA,
                "v8 authenticated q3/formula")
    else:
        require(q3.get("_sealed_setup_kind") ==
                    "external-q3-and-fresh-v7-only" and
                injected_setup.get("trace") is q3.get("_sealed_trace"),
                "v8 sealed setup scope")
    selected_q3 = q3["selected_solution"]
    require(selected_q3["roof_row_index"] == 37 and
            selected_q3["exponent"] == 2 and
            selected_q3["correction_index"] == 1 and
            selected_q3["marking_m"] == 0 and
            selected_q3["lambda"] == 1 and
            selected_q3["typed_source_word"] == FIXED_WORD and
            data["registered_universe"] == {
                "kind": "registered_4096_wordexpr_positive_search",
                "registered_corrections": 4096,
                "registered_dictionary_complete": True,
                "full_H3_fibre_complete": False,
                "fixed_outside_roof": {
                    "row_index": 37, "exponent": 2,
                    "roof_key": selected_q3["roof_key"],
                    "typed_source_word": list(FIXED_WORD),
                    "arithmetic_outside_by_index_three":
                        selected_q3["arithmetic_outside_by_index_three"],
                    "source": "frozen q3 selected outside roof"},
                "full_universe_claimed": False,
                "earliest_global_candidate_claimed": False,
                "negative_completeness_claimed": False,
                "marking_m": 0, "lambda": 1},
            "v8 exact registered universe/outside roof")
    require(data["representation_contract"] == {
                "version": "typed-wordexpr-memo-fusion-v9",
                "persistent_element_equality":
                    "exact canonical bytes; never a digest",
                "sparse_keys":
                    "component plus stable zero-based exact element-pool ID",
                "pivot_order":
                    "component then canonical EKey bytes; never insertion ID",
                "BFS_order": "+1..+6,-1..-6 first-seen shortlex",
                "candidate_sections_retained": False,
                "candidate_wordexpr_retained_across_candidates": False,
                "substituted_descendants_flattened": False,
                "left_Fox_product_rule": "D(uv)=D(u)+value(u)*D(v)",
                "left_Fox_inverse_rule": "D(u^-1)=-value(u)^-1*D(u)",
                "negative_substitution_letter":
                    "advance prefix by value(a_i)^-1, then subtract prefix*D(a_i)",
                "section_oracle":
                    "BFS/direct translations only, canonical-byte-bound typed expression DAG",
                "all_element_pool_values_have_sections": False,
                "candidate_gradients_retained_across_checkpoints": False,
                "candidate_local_typed_gradient_memo": True,
                "memo_key":
                    "typed node identity + rank/arity + candidate + quotient/presentation + leaf bindings",
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
                "candidate_transaction":
                    "exact element-pool and provenance-DAG suffix rollback",
                "missing_pivot_blocker":
                    "target ordinal, component, canonical E4 bytes",
                "proof_DAG_in_memory": "packed parallel arrays",
                "positive_DAG_serialization":
                    "reachable union as typed little-endian base64 arrays",
                "cache_eviction_semantics":
                    "capacity and eviction order affect speed only, never canonical values or search order",
                "persistent_checkpoint_resume": False,
                "correction_dictionary_constructed": True,
                "complete_source_tuple_DP_executed_before_sparse_growth": True,
                "cap_calibration_only": False,
                "resume_or_checkpoint_imported": False},
            "v8 representation contract")
    require(data["theorem_boundary"] == {
                "proved_if_PASS":
                    "one registered literal outside pair survives every isolated elementary-F3 chief refinement L with Phi3(H4)<=L<=H4",
                "Phi3_H4_isolation_required": False,
                "covered":
                    "all isolated elementary-F3 next-chief refinements immediately below current H4",
                "not_covered": ["nonabelian chief factors", "other primes",
                                "deeper iteration", "uniform cofinal tower",
                                "global B4-B"]} and
            data["prohibited_work"] == {
                "relative_ANUPQ_calls": 0, "Reidemeister_Schreier": False,
                "full_Elements": False, "full_regular_matrices": False,
                "full_H1_basis_or_rank": False,
                "registered_corrections": 4096,
                "all_dictionary_DP_executed":
                    ("source_tuple_preflight" in data)},
            "v8 exact theorem/prohibited-work boundary")
    if injected_setup is not None:
        required_setup = {
            "expected_pins", "trace", "e3", "e4", "dictionary",
            "dictionary_receipt", "normalized", "frozen_tuple",
            "inverse_words", "preflight", "tuples", "pool", "basis",
            "scan_setup", "selected_setup"}
        injected_setup["trace"]["source_preflight_validator_entries"] = \
            injected_setup["trace"].get(
                "source_preflight_validator_entries", 0)+1
        require(set(injected_setup) == required_setup and
                data.get("correction_dictionary") ==
                    injected_setup["dictionary_receipt"] and
                data.get("normalized_inverse_fibre") ==
                    injected_setup["normalized"] and
                data.get("source_tuple_preflight") ==
                    injected_setup["preflight"] and
                injected_setup["preflight"]["complete"] is True and
                injected_setup["preflight"]["evaluated"] == 4096,
                "v8 sealed production source/preflight setup")
        if not injected_setup["preflight"]["all_equal_to_frozen_tuple"]:
            first = injected_setup["preflight"]["first_difference"]
            require(token ==
                        "B345_RELFRAT3_WORDEXPR_SEARCH_INCOMPLETE" and
                    data["reason"] == "fixed_inverse_not_uniform" and
                    isinstance(first, dict) and
                    data.get("scan") == {
                        "evaluated": 0, "complete": False,
                        "first_differing_index": first["candidate_index"],
                        "evaluated_prefix_sha256":
                            injected_setup["preflight"]
                                ["tuple_ledger_sha256"],
                        "source_tuple_preflight_only": True},
                    "v8 sealed shared source-nonuniform terminal")
            return
        require(len(injected_setup["tuples"]) == 4096 and
                all(row == injected_setup["frozen_tuple"]
                    for row in injected_setup["tuples"]),
                "v8 sealed uniform source tuple provider")
        validate_v8_scan_selected_core(
            data, injected_setup["dictionary"], injected_setup["tuples"],
            injected_setup["frozen_tuple"],
            injected_setup["inverse_words"], injected_setup["normalized"],
            injected_setup["e3"], injected_setup["e4"],
            injected_setup["pool"], injected_setup["basis"],
            scan_setup=injected_setup["scan_setup"],
            selected_setup=injected_setup["selected_setup"])
        return
    if (token == "B345_RELFRAT3_WORDEXPR_UNKNOWN_RESOURCE" and
            "source_tuple_preflight" not in data):
        stop = data["resource_stop"]
        require(data["reason"] in RESOURCE_REASONS and
                stop["cap"] == data["reason"] and
                stop["no_mathematical_obstruction_claimed"] is True and
                data["bounded_search_prefix"]["structural_cap"]["hit"] is True and
                data["bounded_search_prefix"]["structural_cap"]["reason"] ==
                    data["reason"] and
                all(key not in data for key in
                    ("candidate1_flat_bridge", "wordexpr_scan",
                     "selected_pair", "boundary_proof_dag")),
                "v8 early progressive UNKNOWN_RESOURCE schema")
        if "formula_sha256" in data:
            formula = formula_subset()
            require(data["formula_sha256"] == FORMULA_SHA and
                    data["relevant_formula"] == formula and
                    data["relevant_formula_sha256"] == digest_obj(formula),
                    "v8 early completed formula phase")
        if "matched_quotients" in data:
            e3_early, e4_early = reconstruct(q3)
            require(data["matched_quotients"] == {
                        "E3": {"coarse_degree": e3_early.degree,
                               "fine_pc_rank": e3_early.collector.n,
                               "definition":
                                   "Q0 x Pi3[3]; authenticated coarse source kernel"},
                        "E4": {"coarse_degree": e4_early.degree,
                               "fine_pc_rank": e4_early.collector.n,
                               "definition":
                                   "Q4 x Pi4[3] from the frozen no-common-C3 gate"},
                        "J_H": {"definition":
                            "kernel(PB3 -> E3), with each correction replayed through all five cofaces into H4"},
                        "J_Phi": {
                            "definition":
                                "intersection_{j=0}^4 (coface_j)^-1 Phi3(H4)",
                            "identified_with_Phi3_H3": False,
                            "correction_membership_required": False,
                            "quotient_J_H_over_J_Phi_is_lift_freedom": True}},
                    "v8 early matched quotient phase")
        if "base_q3_replay" in data:
            e3_early, e4_early = reconstruct(q3)
            validate_base_replay(data, q3, e3_early, e4_early)
            if "correction_dictionary" in data:
                dictionary_early = rebuild_dictionary(q3, e3_early)
                public_early = {key: value for key, value in
                                dictionary_early.items() if key != "words"}
                public_early["word_sha256"] = [digest_obj(word)
                                                for word in
                                                dictionary_early["words"]]
                public_early["candidate_order_sha256"] = \
                    digest_obj(public_early["word_sha256"])
                public_early["equals_frozen_v8_order"] = True
                require(data["correction_dictionary"] == public_early,
                        "v8 early completed dictionary phase")
            if "normalized_inverse_fibre" in data:
                normalized_early, _, _ = rebuild_normalized_inverse_fibre(
                    q3, e4_early)
                require(data["normalized_inverse_fibre"] == normalized_early,
                        "v8 early completed inverse phase")
        return
    e3, e4 = reconstruct(q3)
    formula = formula_subset()
    require(data["formula_sha256"] == FORMULA_SHA and
            data["relevant_formula"] == formula and
            data["relevant_formula_sha256"] == digest_obj(formula),
            "v8 formula reconstruction")
    validate_base_replay(data, q3, e3, e4)
    dictionary = rebuild_dictionary(q3, e3)
    public_dictionary = {key: value for key, value in dictionary.items()
                         if key != "words"}
    public_dictionary["word_sha256"] = [digest_obj(word)
                                        for word in dictionary["words"]]
    public_dictionary["candidate_order_sha256"] = \
        digest_obj(public_dictionary["word_sha256"])
    public_dictionary["equals_frozen_v8_order"] = True
    require(data["correction_dictionary"] == public_dictionary and
            dictionary["count"] == 4096,
            "v8 dictionary reconstruction")
    normalized, frozen_tuple, inverse_words = \
        rebuild_normalized_inverse_fibre(q3, e4)
    require(data["normalized_inverse_fibre"] == normalized,
            "v8 normalized inverse reconstruction")
    preflight, tuples = checker_source_tuple_preflight(
        dictionary, e4, frozen_tuple)
    require(data["source_tuple_preflight"] == preflight,
            "v8 complete source tuple preflight")
    if not preflight["all_equal_to_frozen_tuple"]:
        require(token == "B345_RELFRAT3_WORDEXPR_SEARCH_INCOMPLETE" and
                data["reason"] == "fixed_inverse_not_uniform" and
                data["scan"] == {
                    "evaluated": 0, "complete": False,
                    "first_differing_index":
                        preflight["first_difference"]["candidate_index"],
                    "evaluated_prefix_sha256":
                        preflight["tuple_ledger_sha256"],
                    "source_tuple_preflight_only": True},
                "v8 fixed-inverse nonuniform terminal")
        return

    if (token == "B345_RELFRAT3_WORDEXPR_UNKNOWN_RESOURCE" and
            "directed_surgery" not in data):
        stop = data["resource_stop"]
        prefix = data["directed_surgery_prefix"]
        bounded = data["bounded_search_prefix"]
        require(data["reason"] in RESOURCE_REASONS and
                stop["cap"] == data["reason"] and
                stop["no_mathematical_obstruction_claimed"] is True and
                prefix["resource_interrupted"] is True and
                prefix["round_count"] == len(prefix["rounds"]) and
                prefix["translation_count"] == len(prefix["translations"]) and
                prefix["columns_count"] >= 0 and
                isinstance(prefix["columns_sha256"], str) and
                len(prefix["columns_sha256"]) == 64,
                "v8 pre-saturation resource receipt")
        require(bounded["structural_cap"] == {
                    "hit": True, "reason": data["reason"],
                    "source": ("monitor" if data["reason"] in
                               {"producer_soft_timeout", "producer_soft_rss"}
                               else "registered_structural_cap")} and
                "wordexpr_scan" not in data and
                all(key not in data for key in
                    ("candidate1_flat_bridge", "selected_pair",
                     "boundary_proof_dag")),
                "v8 pre-saturation resource boundary")
        # The interrupted prefix is not promoted to a mathematical result;
        # every deterministic completed ledger remains bound in the receipt.
        return

    targets, diagnostics = fixed_target_split(e4, normalized)
    target_names = [row[0] for row in targets]
    diagnostic_names = [row[0] for row in diagnostics]
    diagnostic_rows = []
    for name, kind, word in diagnostics:
        value = e4.eval(word)
        diagnostic_rows.append({
            "name": name, "kind": kind, "word": word,
            "quotient_value_hex": element_blob(value).hex(),
            "quotient_identity": value == e4.identity,
            "Fox_membership_eligible": value == e4.identity,
            "Fox_membership_tested": False, "feeds_acceptance": False})
    source_lengths = [len(word) for word in source_words(FIXED_WORD)]
    inverse_lengths = [len(word) for word in inverse_words]
    target_lengths = [len(word) for _, _, word in targets]
    corrected = {"acceptance_target_count": 33,
                 "diagnostic_target_count": 17,
                 "acceptance_target_names": target_names,
                 "diagnostic_target_names": diagnostic_names,
                 "T_canaries_required_for_acceptance": False,
                 "corrected_Def2_9_IF_FIRST_frozen_pre_run": True,
                 "diagnostic_quotient_pass_count": sum(
                     row["quotient_identity"] for row in diagnostic_rows),
                 "diagnostic_false_allowed_on_PASS": True}
    require(data["fixed_candidate_preflight"] == {
                "correction_index": 1, "correction_word": [],
                "selected_word": list(FIXED_WORD),
                "selected_word_length": len(FIXED_WORD),
                "source_word_lengths": source_lengths,
                "inverse_word_lengths": inverse_lengths,
                "target_names": target_names,
                "diagnostic_target_names": diagnostic_names,
                "corrected_Def2_9": corrected,
                "diagnostics": diagnostic_rows,
                "target_word_lengths": target_lengths,
                "max_source_word_length": max(source_lengths),
                "max_inverse_word_length": max(inverse_lengths),
                "max_target_word_length": max(target_lengths),
                "all_direct_quotient_gates_pass": True,
                "direct_gate_replay_count_before_sparse_growth": 1,
                "marking_m": 0, "lambda": 1,
                "fixed_outside_roof": {"row_index": 37, "exponent": 2},
                "target_order_sha256": digest_obj(target_names),
                "word_representation":
                    "flat freely reduced signed-generator lists",
                "single_word_or_section_length_cap":
                    CAPS["single_word_or_section_length"]},
            "v8 fixed candidate preflight")
    pool, basis = replay_pivot_surgery(data, e4, targets, frozen_tuple)
    if (token == "B345_RELFRAT3_WORDEXPR_UNKNOWN_RESOURCE" and
            "candidate1_flat_bridge" not in data):
        block0 = data.get("wordexpr_scan", {})
        current0 = block0.get("current")
        tx0 = block0.get("transaction")
        tx_keys = {"membership_starts", "membership_rollbacks",
                   "proof_starts", "proof_commits", "proof_rollbacks",
                   "failed_candidate_DAG_nodes_allocated",
                   "max_pool_suffix", "max_live_gradient_entries"}
        post_saturation = (
            current0 == {"candidate_index": 1, "target_ordinal": 0,
                         "target_name": None,
                         "phase": "post_saturation_pre_scan"} and
            isinstance(tx0, dict) and set(tx0) == tx_keys and
            all(value == 0 for value in tx0.values()))
        candidate1_prebridge = (
            isinstance(current0, dict) and
            set(current0) == {"candidate_index", "target_ordinal",
                              "target_name"} and
            current0["candidate_index"] == 1 and
            current0["target_ordinal"] == 0 and
            current0["target_name"] is None and
            isinstance(tx0, dict) and set(tx0) == tx_keys and
            tx0["membership_starts"] in {0, 1} and
            tx0["membership_rollbacks"] == 0 and
            tx0["proof_starts"] == tx0["proof_commits"] ==
                tx0["proof_rollbacks"] == 0 and
            tx0["failed_candidate_DAG_nodes_allocated"] == 0)
        require(set(block0) == {"format", "evaluated", "complete",
                                "registered_corrections",
                                "registered_dictionary_complete",
                                "partial_resource_stop", "current",
                                "no_candidate_skip_interpreted_as_failure",
                                "transaction"} and
                block0.get("format") ==
                    "registered-wordexpr-scan-arrays/v1" and
                block0.get("evaluated") == 0 and
                block0.get("complete") is False and
                block0.get("registered_corrections") == 4096 and
                block0.get("registered_dictionary_complete") is True and
                block0.get("partial_resource_stop") is True and
                block0.get("no_candidate_skip_interpreted_as_failure") is True and
                (post_saturation or candidate1_prebridge),
                "v8 post-prefix pre-bridge resource receipt")
        return
    validate_v8_scan_selected_core(
        data, dictionary, tuples, frozen_tuple, inverse_words, normalized,
        e3, e4, pool, basis)


def validate_fixed_prefix(prefix: dict[str, Any], target_names: list[str]) -> None:
    require(set(prefix) == {"fixed_candidate", "current", "blocker",
                            "transaction", "structural_cap", "accounting"},
            "fixed bounded-prefix keys")
    fixed = prefix["fixed_candidate"]
    require(set(fixed) == {"correction_index", "correction_word",
                           "direct_gates_completed", "direct_gate_replay_count",
                           "target_count", "target_order_sha256"} and
            fixed["correction_index"] == 1 and fixed["correction_word"] == [] and
            fixed["direct_gates_completed"] is True and
            fixed["direct_gate_replay_count"] in {1, 2} and
            fixed["target_count"] == len(target_names) == 33 and
            fixed["target_order_sha256"] == digest_obj(target_names),
            "fixed prefix candidate binding")
    current = prefix["current"]
    require(set(current) in ({"checkpoint", "correction_index",
                              "target_ordinal", "target_name"},
                             {"checkpoint", "correction_index",
                              "target_ordinal", "target_name",
                              "directed_round"}) and
            (current["checkpoint"] is None or
             isinstance(current["checkpoint"], int) and current["checkpoint"] > 0) and
            current["correction_index"] in {None, 1} and
            (current["target_ordinal"] is None or
             isinstance(current["target_ordinal"], int) and
             1 <= current["target_ordinal"] <= len(target_names)) and
            (current["target_name"] is None or
             current["target_ordinal"] is not None and
             current["target_name"] == target_names[current["target_ordinal"]-1]),
            "fixed current prefix")
    blocker = prefix["blocker"]
    require(set(blocker) == {"count", "sha256"} and
            blocker["count"] in {0, 1}, "fixed blocker prefix")
    require_sha256(blocker["sha256"], "fixed blocker prefix SHA")
    tx = prefix["transaction"]
    require(set(tx) == {"starts", "commits", "rollbacks"} and
            all(isinstance(x, int) and x >= 0 for x in tx.values()) and
            tx["commits"] in {0, 1} and tx["rollbacks"] <= tx["starts"],
            "fixed transaction prefix")
    structural = prefix["structural_cap"]
    require(set(structural) == {"hit", "reason", "source"} and
            (structural == {"hit": False, "reason": None, "source": None} or
             structural["hit"] is True and
             structural["source"] in {"monitor", "registered_structural_cap"} and
             structural["reason"] in RESOURCE_REASONS),
            "fixed structural prefix")
    accounting = prefix["accounting"]
    require(set(accounting) == {"translations", "basis_pivots",
                                "basis_live_entries", "pool_size", "DAG_nodes",
                                "DAG_edges", "section_nodes",
                                "section_expression_nodes",
                                "section_expression_edges", "PC_cache_hits",
                                "PC_cache_misses", "PC_cache_evictions"} and
            all(isinstance(value, int) and value >= 0
                for value in accounting.values()),
            "fixed prefix accounting")


def validate_fixed_trace(search: dict[str, Any], width: int) -> None:
    history = [row for row in search["blocker_history"]
               if "failed_checkpoint" in row]
    trace = [row for row in search["checkpoint_trace"]
             if "candidate_index" in row and
             row.get("event") != "directed_surgery_batch"]
    require(all(isinstance(row.get("element_hex"), str) and
                len(bytes.fromhex(row["element_hex"])) == width
                for row in history), "fixed blocker canonical width")
    require(history and history[0]["candidate_index"] == 1 and
            history[0]["failed_checkpoint"] == 1 and
            history[0]["target_ordinal"] == 6 and
            history[0]["target_name"] == "hexagon_1_coface_0" and
            history[0]["component"] == 4 and
            all(row["candidate_index"] == 1 for row in history) and
            all(row["candidate_index"] == 1 for row in trace),
            "reconstructed first fixed blocker")
    checkpoints = search["geometric_translation_checkpoints"]
    for row in history:
        retry = row["retry_checkpoints"][0] if row["retry_checkpoints"] else None
        expected_skips = [cp for cp in checkpoints
                          if row["failed_checkpoint"] < cp and
                          (retry is None or cp < retry)]
        require(row["skip_checkpoints"] == expected_skips and
                len(row["retry_checkpoints"]) <= 1,
                "complete fixed blocker skip schedule")
        if retry is not None:
            intro = row["matching_introduction"]
            expected_retry = next(cp for cp in checkpoints
                                  if cp >= intro["translation_ordinal"])
            require(retry == expected_retry,
                    "retry is first checkpoint after exact pivot")


def validate_fixed_claim_boundary(data: dict[str, Any]) -> None:
    """Bind the deliberately narrow, positive-only interpretation."""
    universe = data["registered_universe"]
    require(universe["kind"] == "fixed_positive_candidate" and
            universe["correction_indices"] == [1] and
            universe["correction_word"] == [] and
            universe["full_4096_universe_claimed"] is False and
            universe["earliest_global_candidate_claimed"] is False and
            universe["negative_completeness_claimed"] is False,
            "fixed positive-only universe/claim boundary")
    token = data["terminal_token"]
    if token != "B345_RELFRAT3_PIVOT_SURGERY_PASS":
        require(data["claim_classification"] == "unknown_not_obstruction" and
                data["claim_scope"] == "fixed_candidate_pivot_surgery_only" and
                data["no_mathematical_obstruction_claimed"] is True and
                data["full_universe_claimed"] is False and
                data["negative_claimed"] is False,
                "fixed nonpositive claim boundary")


def validate_cap_utilization(block: dict[str, Any], *, live: int,
                             pool_peak: int, pivots: int, dag_nodes: int,
                             dag_edges: int, rss_peak: int,
                             expression_nodes: int = 0,
                             expression_edges: int = 0) -> None:
    expected_values = {
        "live_sparse_entries": (live, CAPS["total_sparse_group_ring_keys"]),
        "element_pool_peak": (pool_peak, CAPS["element_pool"]),
        "sparse_pivots": (pivots, CAPS["sparse_pivot_rows"]),
        "DAG_nodes": (dag_nodes, CAPS["provenance_dag_nodes"]),
        "DAG_edges": (dag_edges, CAPS["provenance_dag_edges"]),
        "directed_section_expression_nodes": (
            expression_nodes, CAPS["directed_section_expr_nodes"]),
        "directed_section_expression_edges": (
            expression_edges, CAPS["directed_section_expr_edges"]),
        "RSS_peak_bytes": (rss_peak, CAPS["producer_soft_rss_bytes"]),
    }
    require(set(block) == set(expected_values), "cap utilization keys")
    for key, (value, cap) in expected_values.items():
        require(block[key] == {"value": value, "cap": cap,
                               "ratio": value/cap},
                f"cap utilization {key}")


def validate_cap_calibration(record: dict[str, Any]) -> None:
    require(record == CAP_CALIBRATION,
            "exact fixed-candidate v6 cap-calibration record")


def validate_fixed_receipt(data: dict[str, Any], q3: dict[str, Any],
                           q3_path: Path, repo: Path) -> None:
    required = {"schema", "status", "terminal_token", "reason", "pins",
                "source_hashes", "input_q3_terminal", "output_path", "caps",
                "registered_universe", "representation_contract",
                "claim_classification", "claim_scope",
                "no_mathematical_obstruction_claimed", "full_universe_claimed",
                "negative_claimed", "theorem_boundary",
                "prohibited_work", "resource_guards", "performance",
                "cap_calibration",
                "bounded_search_prefix", "formula_sha256", "relevant_formula",
                "relevant_formula_sha256", "matched_quotients",
                "base_q3_replay", "normalized_inverse_fibre",
                "fixed_candidate_preflight"}
    optional = {"search", "direct_lane", "resource_stop",
                "resource_accounting_at_stop", "quotient_element_registry",
                "fox_models", "boundary_proof_dag", "selected_pair",
                "boundary_certificates", "literal_replay", "blocker_table",
                "blocker_history", "checkpoint_trace", "pivot_introductions",
                "direct_vs_preflight_comparisons", "directed_surgery_prefix",
                "directed_base_support", "directed_surgery"}
    require(required <= set(data) and set(data) <= required | optional,
            "fixed v6 top-level layout")
    require(data["schema"] == SCHEMA and data["caps"] == CAPS and
            data["output_path"] == str(OUTPUT_PATH).replace("\\", "/") and
            data["input_q3_terminal"] == q3.get("terminal_token"),
            "fixed schema/caps/input/output")
    require(set(CAPS)-set(V6_CAPS) == {
                "directed_surgery_rounds", "directed_unique_translations",
                "directed_columns", "directed_section_expr_nodes",
                "directed_section_expr_edges"} and
            all(CAPS[key] == V6_CAPS[key] for key in V6_CAPS),
            "independent exact v6/v7 cap delta")
    validate_cap_calibration(data["cap_calibration"])
    token = data["terminal_token"]
    require(token in TERMINALS and data["status"] == token and
            data["claim_scope"] == "fixed_candidate_pivot_surgery_only" and
            data["no_mathematical_obstruction_claimed"] is True,
            "fixed terminal/scope")
    validate_fixed_claim_boundary(data)
    is_pass = token == "B345_RELFRAT3_PIVOT_SURGERY_PASS"
    is_incomplete = token == "B345_RELFRAT3_PIVOT_SURGERY_INCOMPLETE"
    is_unknown = token == "B345_RELFRAT3_PIVOT_SURGERY_UNKNOWN_RESOURCE"
    is_unknown_input = token == "B345_RELFRAT3_PIVOT_SURGERY_UNKNOWN_INPUT"
    require(data["claim_classification"] ==
            ("positive_certificate" if is_pass else "unknown_not_obstruction"),
            "fixed claim classification")
    if not is_pass:
        require("selected_pair" not in data and
                "boundary_certificates" not in data and
                "boundary_proof_dag" not in data,
                "nonpositive promoted to certificate")

    pins = data["pins"]
    require(set(pins) == {"q3_producer", "q3_checker", "q3_driver",
                          "q3_artifact", "formula_sha256",
                          "semantic_reference_v1", "semantic_reference_v2",
                          "semantic_reference_v3", "semantic_reference_v4",
                          "semantic_reference_v5", "semantic_reference_v6"},
            "fixed v7 pin key set")
    for key, path, sha in (("q3_producer", Q3_PRODUCER, Q3_PRODUCER_SHA),
                           ("q3_checker", Q3_CHECKER, Q3_CHECKER_SHA),
                           ("q3_driver", Q3_DRIVER, Q3_DRIVER_SHA)):
        require(pins[key] == {"path": str(path).replace("\\", "/"),
                              "sha256": sha} and digest_file(repo/path) == sha,
                f"fixed pin {key}")
    require(pins["q3_artifact"] == {
                "path": str(Q3_ARTIFACT_PATH).replace("\\", "/"),
                "sha256": Q3_ARTIFACT_SHA} and
            digest_file(q3_path) == Q3_ARTIFACT_SHA and
            pins["formula_sha256"] == FORMULA_SHA and
            digest_obj(q3["formulas"]) == FORMULA_SHA,
            "fixed q3/formula pins")
    references = (
        ("semantic_reference_v6", V6_PRODUCER, V6_PRODUCER_SHA,
         V6_CHECKER, V6_CHECKER_SHA, V6_DRIVER, V6_DRIVER_SHA,
         "frozen full-32768 fixed-candidate basis and cap reference"),
        ("semantic_reference_v5", V5_PRODUCER, V5_PRODUCER_SHA,
         V5_CHECKER, V5_CHECKER_SHA, V5_DRIVER, V5_DRIVER_SHA,
         "frozen fixed-candidate v5 semantics and cap-stop reference"),
        ("semantic_reference_v4", V4_PRODUCER, V4_PRODUCER_SHA,
         V4_CHECKER, V4_CHECKER_SHA, V4_DRIVER, V4_DRIVER_SHA,
         "frozen transactional-v4 arithmetic, Fox, blocker, and packed-certificate reference"),
        ("semantic_reference_v3", V3_PRODUCER, V3_PRODUCER_SHA,
         V3_CHECKER, V3_CHECKER_SHA, V3_DRIVER, V3_DRIVER_SHA,
         "frozen packed-v3 semantics and positive-certificate reference"),
        ("semantic_reference_v2", V2_PRODUCER, V2_PRODUCER_SHA,
         V2_CHECKER, V2_CHECKER_SHA, V2_DRIVER, V2_DRIVER_SHA,
         "frozen v2 mathematics, universe, gates, and search order"),
        ("semantic_reference_v1", V1_PRODUCER, V1_PRODUCER_SHA,
         V1_CHECKER, V1_CHECKER_SHA, V1_DRIVER, V1_DRIVER_SHA,
         "frozen semantic predicate and search-order reference"),
    )
    for key, producer, psha, checker, csha, driver, dsha, role in references:
        require(pins[key] == {
                    "producer": {"path": str(producer).replace("\\", "/"),
                                 "sha256": psha},
                    "checker": {"path": str(checker).replace("\\", "/"),
                                "sha256": csha},
                    "driver": {"path": str(driver).replace("\\", "/"),
                               "sha256": dsha}, "role": role} and
                digest_file(repo/producer) == psha and
                digest_file(repo/checker) == csha and
                digest_file(repo/driver) == dsha, f"fixed {key}")
    require(data["source_hashes"] == {
                "producer_sha256": digest_file(
                    repo/"search/d972_b345_relfrat3_pivot_surgery_v7.py"),
                "checker_sha256": digest_file(Path(__file__)),
                "driver_sha256": digest_file(
                    repo/"search/d972_b345_relfrat3_pivot_surgery_gha_driver_v7.g")},
            "fixed source hashes")
    require(data["representation_contract"] == {
                "version": "pivot-directed-sparse-section-oracle-v7",
                "persistent_element_equality": "exact canonical bytes; never a digest",
                "sparse_keys": "component plus stable zero-based exact element-pool ID",
                "pivot_order": "component then canonical EKey bytes; never insertion ID",
                "BFS_order": "+1..+6,-1..-6 first-seen shortlex",
                "candidate_sections_retained": False,
                "section_oracle": "BFS/direct translations only, canonical-byte-bound typed expression DAG",
                "all_element_pool_values_have_sections": False,
                "candidate_gradients_retained_across_checkpoints": False,
                "candidate_transaction": "exact element-pool and provenance-DAG suffix rollback",
                "missing_pivot_blocker": "target ordinal, component, canonical E4 bytes",
                "proof_DAG_in_memory": "packed parallel arrays",
                "positive_DAG_serialization": "reachable union as typed little-endian base64 arrays",
                "cache_eviction_semantics": "capacity and eviction order affect speed only, never canonical values or search order",
                "persistent_checkpoint_resume": False,
                "correction_dictionary_constructed": False,
                "fixed_context_cheap_DP_executed": False,
                "cap_calibration_only": False,
                "resume_or_checkpoint_imported": False,
            } and
            data["prohibited_work"]["omitted_corrections_evaluated"] == 0 and
            data["prohibited_work"]["all_dictionary_DP_executed"] is False,
            "fixed no-dictionary/DP contract")

    selected_q3 = q3["selected_solution"]
    require(selected_q3["roof_row_index"] == 37 and
            selected_q3["exponent"] == 2 and
            selected_q3["correction_index"] == 1 and
            selected_q3["marking_m"] == 0 and selected_q3["lambda"] == 1 and
            selected_q3["typed_source_word"] == FIXED_WORD,
            "fixed q3 selected roof")
    expected_universe = {
        "kind": "fixed_positive_candidate", "correction_indices": [1],
        "correction_word": [],
        "fixed_outside_roof": {
            "row_index": 37, "exponent": 2,
            "roof_key": selected_q3["roof_key"],
            "typed_source_word": list(FIXED_WORD),
            "arithmetic_outside_by_index_three":
                selected_q3["arithmetic_outside_by_index_three"],
            "source": "frozen q3 selected outside roof"},
        "full_4096_universe_claimed": False,
        "earliest_global_candidate_claimed": False,
        "negative_completeness_claimed": False,
        "marking_m": 0, "lambda": 1,
    }
    require(data["registered_universe"] == expected_universe,
            "fixed registered universe")

    e3, e4 = reconstruct(q3)
    formula = formula_subset()
    require(data["formula_sha256"] == FORMULA_SHA and
            data["relevant_formula"] == formula and
            data["relevant_formula_sha256"] == digest_obj(formula),
            "fixed formula reconstruction")
    validate_base_replay(data, q3, e3, e4)
    normalized, base_key, _ = rebuild_normalized_inverse_fibre(q3, e4)
    require(data["normalized_inverse_fibre"] == normalized,
            "fixed normalized inverse")
    targets, diagnostics = fixed_target_split(e4, normalized)
    target_names = [row[0] for row in targets]
    diagnostic_names = [row[0] for row in diagnostics]
    diagnostic_rows = []
    for name, kind, word in diagnostics:
        value = e4.eval(word)
        diagnostic_rows.append({
            "name": name, "kind": kind, "word": word,
            "quotient_value_hex": (bytes(value[0])+bytes(value[1])).hex(),
            "quotient_identity": value == e4.identity,
            "Fox_membership_eligible": value == e4.identity,
            "Fox_membership_tested": False,
            "feeds_acceptance": False,
        })
    corrected = {
        "acceptance_target_count": 33, "diagnostic_target_count": 17,
        "acceptance_target_names": target_names,
        "diagnostic_target_names": diagnostic_names,
        "T_canaries_required_for_acceptance": False,
        "corrected_Def2_9_IF_FIRST_frozen_pre_run": True,
        "diagnostic_quotient_pass_count": sum(
            row["quotient_identity"] for row in diagnostic_rows),
        "diagnostic_false_allowed_on_PASS": True,
    }
    source_lengths = [len(word) for word in source_words(FIXED_WORD)]
    inverse_lengths = [len(word) for word in normalized["selected_inverse_words"]]
    target_lengths = [len(row[2]) for row in targets]
    require(data["fixed_candidate_preflight"] == {
                "correction_index": 1, "correction_word": [],
                "selected_word": list(FIXED_WORD),
                "selected_word_length": len(FIXED_WORD),
                "source_word_lengths": source_lengths,
                "inverse_word_lengths": inverse_lengths,
                "target_names": target_names,
                "diagnostic_target_names": diagnostic_names,
                "corrected_Def2_9": corrected,
                "diagnostics": diagnostic_rows,
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
                    CAPS["single_word_or_section_length"]},
            "fixed literal preflight")
    validate_fixed_prefix(data["bounded_search_prefix"], target_names)

    guard = data["resource_guards"]
    require(guard["seconds"] == 18_000 and guard["minutes"] == 300 and
            guard["rss_bytes"] == CAPS["producer_soft_rss_bytes"] and
            guard["terminal_on_hit"] ==
                "B345_RELFRAT3_PIVOT_SURGERY_UNKNOWN_RESOURCE" and
            guard["hit"] is is_unknown and
            (not is_unknown and guard["hit_reason"] is None or
             is_unknown and guard["hit_reason"] == data["resource_stop"]["cap"]),
            "fixed resource guard")
    require(isinstance(data["performance"].get("phase_timings_seconds"), dict),
            "fixed phase timings")

    if is_unknown:
        stop = data["resource_stop"]
        require(stop["cap"] in RESOURCE_REASONS and stop["cap"] == data["reason"] and
                stop["large_structures_released_before_write"] is True and
                stop["no_mathematical_obstruction_claimed"] is True and
                data["bounded_search_prefix"]["structural_cap"]["reason"] == stop["cap"],
                "fixed UNKNOWN resource")
        rows = {"blocker_table": data["blocker_table"],
                "blocker_history": data["blocker_history"],
                "pivot_introductions": data["pivot_introductions"],
                "checkpoint_trace": data["checkpoint_trace"],
                "blocker_table_sha256": digest_obj(data["blocker_table"]),
                "blocker_history_sha256": digest_obj(data["blocker_history"]),
                "checkpoint_trace_sha256": digest_obj(data["checkpoint_trace"]),
                "geometric_translation_checkpoints": [
                    1 << i for i in range(16)
                    if (1 << i) <= data["bounded_search_prefix"]["accounting"]["translations"]]}
        if rows["blocker_history"]:
            validate_fixed_trace(rows, e4.degree+e4.collector.n)
        stopped = data["resource_accounting_at_stop"]
        require(stopped["bounded_search_prefix"] ==
                data["bounded_search_prefix"], "fixed UNKNOWN prefix binding")
        basis_stop = stopped["basis"]
        validate_cap_utilization(
            data["performance"]["cap_utilization"],
            live=basis_stop["live_sparse_vector_entries"],
            pool_peak=stopped["element_pool"]["peak"],
            pivots=basis_stop["pivot_count"],
            dag_nodes=basis_stop["dag"]["peak_nodes"],
            dag_edges=basis_stop["dag"]["peak_edges"],
            rss_peak=guard["peak_rss_bytes"],
            expression_nodes=basis_stop["lazy_sections"]
                ["expressions"]["peak_nodes"],
            expression_edges=basis_stop["lazy_sections"]
                ["expressions"]["peak_edges"])
        return

    search = data["search"]
    require(search["registered_correction_indices"] == [1] and
            search["registered_correction_word"] == [] and
            search["other_corrections_constructed_or_evaluated"] == 0 and
            search["correction_dictionary_constructed"] is False and
            search["fixed_context_cheap_DP_executed"] is False and
            search["persistent_candidate_cache_size"] == 0 and
            search["persistent_candidate_gradient_entries"] == 0 and
            search["same_basis_reused_for_fixed_candidate_retries"] is True and
            search["corrected_Def2_9_acceptance_target_count"] == 33 and
            search["diagnostic_target_count"] == 17 and
            search["diagnostic_targets_feed_acceptance"] is False and
            search["fixed_candidate_scheduled_from_checkpoint"] == 1 and
            search["candidate_resource_skips"] == [] and
            search["direct_vs_preflight_all_equal"] is True and
            search["translations_used"] == 32_768 and
            search["directed_translations_used"] ==
                data["directed_surgery"]["translation_count"] and
            search["total_complete_translation_blocks"] ==
                search["translations_used"]+
                search["directed_translations_used"] and
            search["columns_seen"] ==
                11*search["total_complete_translation_blocks"] and
            search["geometric_translation_checkpoints"] == [
                1 << i for i in range(16)
                if (1 << i) <= search["translations_used"]],
            "fixed search contract")
    inverse_cache = search["quotient_inverse_cache"]
    require(set(inverse_cache) == {
                "key", "entries", "capacity", "hits", "misses",
                "tuple_match_count", "tuple_mismatch_count",
                "max_inverse_word_length", "cached_datum",
                "cache_hit_replays_current_ST_in_E4",
                "TS_replay_is_diagnostic_only",
                "different_tuple_is_candidate_local_UNKNOWN",
                "raw_endomorphism_powering_fallback",
                "candidate_relations_gradients_proof_roots_reused",
                "componentwise_Q4_Pi4_inverse_words_combined"} and
            search["settled_automorphism_order_cache_size"] == 1 and
            inverse_cache["key"] ==
                "exact ordered tuple of six stable E4 element IDs" and
            inverse_cache["entries"] == inverse_cache["capacity"] == 1 and
            inverse_cache["hits"] == inverse_cache["tuple_match_count"] >= 1 and
            inverse_cache["misses"] ==
                inverse_cache["tuple_mismatch_count"] == 0 and
            inverse_cache["max_inverse_word_length"] ==
                normalized["max_inverse_word_length"] and
            inverse_cache["cached_datum"] ==
                "one pinned normalized exponent-seven full inverse word tuple" and
            inverse_cache["cache_hit_replays_current_ST_in_E4"] is True and
            inverse_cache["TS_replay_is_diagnostic_only"] is True and
            inverse_cache["different_tuple_is_candidate_local_UNKNOWN"] is True and
            inverse_cache["raw_endomorphism_powering_fallback"] is False and
            inverse_cache["candidate_relations_gradients_proof_roots_reused"] is False and
            inverse_cache["componentwise_Q4_Pi4_inverse_words_combined"] is False,
            "corrected normalized inverse cache contract")
    validate_fixed_trace(search, e4.degree+e4.collector.n)
    comparisons = search["direct_vs_preflight_comparisons"]
    outcomes = [row for row in search["checkpoint_trace"]
                if row["event"] in {"missing_pivot", "selected_commit"}]
    require(search["direct_word_replay_count"] == len(comparisons) and
            [(row["checkpoint"], row["candidate_index"]) for row in comparisons] ==
            [(row["checkpoint"], row["candidate_index"]) for row in outcomes] and
            all(row == {"checkpoint": row["checkpoint"], "candidate_index": 1,
                        "direct_failed_gates": [],
                        "equal_to_preflight": True}
                for row in comparisons),
            "fixed direct replay schedule")
    tx = search["transaction"]
    surgery_rounds = data["directed_surgery"]["rounds"]
    require(tx["starts"] == len(outcomes)+len(surgery_rounds) and
            tx["rollbacks"] == sum(row["event"] == "missing_pivot"
                                    for row in outcomes)+
                sum(row["outcome"] == "RETRY" for row in surgery_rounds) and
            tx["commits"] == sum(row["event"] == "selected_commit"
                                  for row in outcomes)+
                sum(row["outcome"] == "PASS" for row in surgery_rounds) and
            tx["blocker_skips"] == sum(row["event"] == "missing_pivot_skip"
                                       for row in search["checkpoint_trace"]) and
            tx["blocker_retries"] == sum(row["event"] == "exact_pivot_retry"
                                         for row in search["checkpoint_trace"]),
            "fixed transaction accounting")
    pool = search["element_pool"]
    require(pool["transaction_rollbacks"] == tx["rollbacks"] and
            pool["transaction_commits"] == tx["commits"] and
            pool["rollback_lru_clears"] == 2*tx["rollbacks"],
            "fixed pool transactions")
    validate_lru_accounting(pool["product_cache"], CAPS["element_product_cache"])
    validate_lru_accounting(pool["inverse_cache"], CAPS["element_inverse_cache"])
    validate_cap_utilization(
        data["performance"]["cap_utilization"],
        live=search["live_sparse_vector_entries"], pool_peak=pool["peak"],
        pivots=search["pivot_count"],
        dag_nodes=search["provenance_DAG"]["peak_nodes"],
        dag_edges=search["provenance_DAG"]["peak_edges"],
        rss_peak=guard["peak_rss_bytes"],
        expression_nodes=search["lazy_sections"]
            ["expressions"]["peak_nodes"],
        expression_edges=search["lazy_sections"]
            ["expressions"]["peak_edges"])
    replay_pivot_surgery(data, e4, targets, base_key)

    if is_incomplete:
        require(search["translations_used"] ==
                CAPS["coefficient_translates_per_relator"] and
                tx["commits"] == 0 and
                data["direct_lane"]["literal_pair_found"] is False,
                "fixed INCOMPLETE terminal")
        return

    require(is_pass and tx["commits"] == 1 and
            data["bounded_search_prefix"]["fixed_candidate"]
                ["direct_gate_replay_count"] == 2 and
            data["direct_lane"] == {"literal_pair_found": True,
                                      "PB5_branch_constructed": False,
                                      "stop_reason": "FIRST_LITERAL_PAIR_AT_PHI"},
            "fixed PASS terminal")
    selected = data["selected_pair"]
    require(selected["correction_index"] == 1 and
            selected["correction_word"] == [] and
            selected["selected_word"] == FIXED_WORD and
            selected["boundary_certificate_names"] == target_names,
            "fixed selected pair")
    expected_all = expected_targets(selected, e4, normalized, base_key)
    expected_acceptance = [row for row in expected_all
                           if not row[0].startswith("T_relation_") and
                           not row[0].startswith("TS_generator_")]
    expected_diagnostics = [row for row in expected_all
                            if row[0].startswith("T_relation_") or
                            row[0].startswith("TS_generator_")]
    require(expected_acceptance == targets and
            expected_diagnostics == diagnostics and
            selected["diagnostics"] == diagnostic_rows,
            "fixed selected 33/17 target regeneration")
    proof_expression_values = decode_section_expressions(
        data["boundary_proof_dag"]["section_expressions"], e4)
    by_id, reverse = validate_registry(data["quotient_element_registry"],
                                       {3: e3, 4: e4},
                                       proof_expression_values)
    models = validate_fox_models(data["fox_models"], e3, e4, reverse)
    validate_certificates(data["boundary_certificates"],
                          data["boundary_proof_dag"], targets, e4,
                          models[4], by_id, reverse)
    bindings = [independent_gradient_binding(name, kind, *fox(word, e4))
                for name, kind, word in targets]
    require(search["selected_gradient_bindings"] == bindings,
            "fixed PASS gradient bindings")
    require(data["literal_replay"]["onto"] == {
                "S_relations_killed": True,
                "S_of_T_recovers_six_marked_generators": True,
                "T_relations_diagnostic_only": True,
                "T_of_S_diagnostic_only": True,
                "corrected_Def2_9_IF_FIRST": True},
            "corrected Def2.9 PASS replay")


def expect_reject(action: Any, label: str) -> None:
    try:
        action()
    except (Reject, KeyError, IndexError, TypeError, ValueError):
        return
    raise AssertionError(f"mutation accepted: {label}")


def self_test() -> None:
    require([len(pure_relations(r)) for r in (3, 4, 5)] == [2, 11, 35],
            "selftest presentation")
    # Independent negative-letter Fox orientation canary in C3.
    cyclic = {"generator_count": 1, "relative_orders": [3],
              "power_relations": [[0]], "inverses": [[2]],
              "conjugate_relations": [], "inverse_conjugate_relations": []}
    pc = Collector(cyclic)
    # Collector intentionally has no producer-style unit helper; construct it directly.
    quotient = Quotient(2, 1, pc, [(p_one(1), (1,))])
    gradient, value = fox([-1], quotient)
    require(value == (p_one(1), (2,)) and list(gradient.values()) == [2],
            "negative Fox orientation")
    cube, cube_value = fox([1, 1, 1], quotient)
    require(cube_value == quotient.identity and boundary1(cube, quotient) == {},
            "C3 Fox cycle")
    mutated = dict(cube)
    first = next(iter(mutated))
    mutated[first] = 2 if mutated[first] == 1 else 1
    expect_reject(lambda: require(mutated == cube, "support coefficient"),
                  "Fox coefficient")
    fake = {"terminal_token": "B345_RELFRAT3_LITERAL_PAIR_PASS",
            "status": "B345_RELFRAT3_LITERAL_PAIR_PASS", "direct_lane": {}}
    expect_reject(lambda: validate_terminal(fake), "false positive terminal")
    unsupported = {"terminal_token": "B345_RELFRAT3_MISSING_MATCHED_CHAIN",
                   "status": "B345_RELFRAT3_MISSING_MATCHED_CHAIN"}
    expect_reject(lambda: validate_terminal(unsupported),
                  "unsupported missing-matched-chain terminal")
    projected = {"terminal_token": "B345_RELFRAT3_PROJECTED_OBSTRUCTION",
                 "status": "B345_RELFRAT3_PROJECTED_OBSTRUCTION",
                 "projection_certificate": {"independently_replayed": True}}
    expect_reject(lambda: validate_terminal(projected),
                  "unsupported projected-obstruction terminal")
    altered = formula_subset()
    altered = json.loads(json.dumps(altered))
    altered["cofaces_3_4"][1][0].reverse()
    expect_reject(lambda: require(altered == formula_subset(), "coface"),
                  "coface orientation")
    cache_row = {"capacity": 8, "size": 2, "peak": 3,
                 "hits": 5, "misses": 7, "evictions": 1, "clears": 2}
    validate_lru_accounting(cache_row, 8)
    bad_cache = dict(cache_row); bad_cache["peak"] = 9
    expect_reject(lambda: validate_lru_accounting(bad_cache, 8),
                  "LRU peak cap")
    bad_cache = dict(cache_row); bad_cache["capacity"] = 9
    expect_reject(lambda: validate_lru_accounting(bad_cache, 8),
                  "LRU capacity drift")

    # Independent bounded fixed-context recurrence versus literal evaluation.
    q4 = Quotient(4, 1, pc, [(p_one(1), (1,))] +
                  [(p_one(1), (0,)) for _ in range(5)])
    toy_dictionary = {
        "words": [[], [1], [-1], [1, 1]], "count": 4,
        "seed_words": [[1]], "parent_indices": [0, 1, 1, 2],
        "signed_seed_edges": [0, 1, -1, 1],
    }
    toy_dp, toy_failures = rebuild_fixed_context_dp(toy_dictionary, q4)
    toy_direct = [direct_cheap_failures(reduce_word(FIXED_WORD+word), word, q4)
                  for word in toy_dictionary["words"]]
    require(toy_failures == toy_direct and
            toy_dp["contexts"]["named_use_count"] == 46 and
            len(toy_dp["failure_bitsets"]) == 27,
            "independent fixed-context DP/direct")
    toy_prefix = {
        "cheap": {"evaluated": 4, "completed": True,
                  "survivor_count": toy_dp["survivor_count"],
                  "survivor_indices_sha256": toy_dp["survivor_indices_sha256"],
                  "evaluated_prefix_sha256": toy_dp["evaluated_prefix_sha256"],
                  "survivor_prefix_sha256": toy_dp["survivor_prefix_sha256"],
                  "current_candidate": None},
        "current": {"checkpoint": 4, "correction_index": None,
                    "target_ordinal": None, "target_name": None},
        "blocker": {"count": 0, "sha256": digest_obj([])},
        "transaction": {"starts": 0, "commits": 0, "rollbacks": 0},
        "structural_cap": {"hit": True, "reason": "toy_cap",
                           "source": "registered_structural_cap"},
        "accounting": {"translations": 4, "basis_pivots": 1,
                       "basis_live_entries": 1, "pool_size": 3,
                       "DAG_nodes": 2, "DAG_edges": 0, "section_nodes": 3,
                       "PC_cache_hits": 0, "PC_cache_misses": 0,
                       "PC_cache_evictions": 0},
    }
    validate_search_prefix(toy_prefix, toy_failures, 4)
    bad_prefix = json.loads(json.dumps(toy_prefix))
    bad_prefix["cheap"]["evaluated_prefix_sha256"] = "0"*64
    expect_reject(lambda: validate_search_prefix(bad_prefix, toy_failures, 4),
                  "cheap prefix digest mutation")

    blob = element_blob(q4.identity).hex()
    intro = {"component": 2, "element_hex": blob,
             "translation_ordinal": 3, "relator_index": 1}
    blocker = {"candidate_index": 2, "target_ordinal": 1,
               "target_name": "toy", "component": 2,
               "element_hex": blob, "failed_checkpoint": 1,
               "skip_checkpoints": [2], "retry_checkpoints": [4],
               "history_id": 1, "matching_introduction": intro}
    trace = [
        {"checkpoint": 1, "candidate_index": 2, "event": "missing_pivot",
         "target_ordinal": 1, "target_name": "toy", "component": 2,
         "element_hex": blob, "blocker_history_id": 1,
         "pool_suffix_removed": 1},
        {"checkpoint": 2, "candidate_index": 2, "event": "missing_pivot_skip",
         "blocker_history_id": 1, "pool_element_present": False,
         "basis_pivot_present": False},
        {"checkpoint": 4, "candidate_index": 2, "event": "exact_pivot_retry",
         "blocker_history_id": 1, "matching_introduction": intro},
    ]
    blocker_search = {"blocker_table": [],
                      "blocker_table_sha256": digest_obj([]),
                      "blocker_history": [blocker],
                      "blocker_history_sha256": digest_obj([blocker]),
                      "pivot_introductions": [intro],
                      "checkpoint_trace": trace,
                      "checkpoint_trace_sha256": digest_obj(trace)}
    validate_blocker_trace(blocker_search, len(bytes.fromhex(blob)))
    bad_blocker = json.loads(json.dumps(blocker_search))
    bad_blocker["checkpoint_trace"][2]["matching_introduction"][
        "translation_ordinal"] = 5
    bad_blocker["checkpoint_trace_sha256"] = digest_obj(
        bad_blocker["checkpoint_trace"])
    expect_reject(lambda: validate_blocker_trace(
        bad_blocker, len(bytes.fromhex(blob))), "retry before exact pivot")

    def seal_array(type_name: str, typecode: str, values: Sequence[int],
                   cap: int) -> dict[str, Any]:
        if typecode == "B":
            raw, itemsize = bytes(values), 1
        else:
            packed = array(typecode, values)
            if sys.byteorder != "little":
                packed.byteswap()
            raw, itemsize = packed.tobytes(), packed.itemsize
        return {"type": type_name, "array_typecode": typecode,
                "endianness": "little", "length": len(values),
                "itemsize": itemsize, "byte_length": len(raw), "cap": cap,
                "sha256": hashlib.sha256(raw).hexdigest(),
                "base64": base64.b64encode(raw).decode("ascii")}

    def seal_toy(kinds: Sequence[int] = (1, 1, 2),
                 relators: Sequence[int] = (1, 2, 0),
                 translations: Sequence[int] = (11, 12, 0),
                 offsets: Sequence[int] = (0, 0, 0, 2),
                 parents: Sequence[int] = (1, 2),
                 coefficients: Sequence[int] = (1, 2),
                 roots: Sequence[dict[str, Any]] =
                 ({"name": "toy_root", "node_id": 3},)) -> dict[str, Any]:
        arrays = {
            "node_kind": seal_array("uint8", "B", kinds,
                                      CAPS["provenance_dag_nodes"]),
            "leaf_relator_index": seal_array("uint16", "H", relators,
                                               CAPS["provenance_dag_nodes"]),
            "leaf_translation_element_id": seal_array(
                "uint32", "I", translations, CAPS["provenance_dag_nodes"]),
            "edge_offsets": seal_array("uint32", "I", offsets,
                                         CAPS["provenance_dag_nodes"]+1),
            "edge_parent_node_id": seal_array(
                "uint32", "I", parents, CAPS["provenance_dag_edges"]),
            "edge_coefficient": seal_array(
                "uint8", "B", coefficients, CAPS["provenance_dag_edges"]),
        }
        root_rows = [dict(row) for row in roots]
        manifest = {name: {key: value for key, value in row.items()
                           if key != "base64"} for name, row in arrays.items()}
        leaf_count = sum(1 for value in kinds if value == 1)
        return {
            "format": "packed-parallel-arrays/v1", "field": 3,
            "node_order": "one_based_topological", "translation_action": "left",
            "arrays": arrays, "roots": root_rows, "node_count": len(kinds),
            "edge_count": len(parents), "leaf_count": leaf_count,
            "combination_node_count": len(kinds)-leaf_count,
            "all_serialized_nodes_reachable_from_roots": True,
            "unreachable_search_nodes_pruned": 7,
            "expanded_boundary_ledgers_serialized": False,
            "packed_manifest_sha256": digest_obj({"arrays": manifest,
                                                   "roots": root_rows}),
        }

    key_a: VKey = (1, ((0,), (0,)))
    key_b: VKey = (2, ((1,), (1,)))
    leaf_values = {(1, 11): {key_a: 1}, (2, 12): {key_b: 1}}
    expected_toy = {key_a: 1, key_b: 2}

    def audit_toy(block: dict[str, Any]) -> None:
        roots, _ = evaluate_proof_dag(
            block, ["toy_root"],
            lambda node: leaf_values[(node["relator_index"],
                                      node["translation_element_id"])])
        require(roots["toy_root"] == expected_toy, "toy DAG root")

    toy = seal_toy()
    audit_toy(toy)
    orientation = json.loads(json.dumps(toy))
    orientation["translation_action"] = "right"
    expect_reject(lambda: audit_toy(orientation), "packed DAG orientation")
    expect_reject(lambda: audit_toy(seal_toy(coefficients=(1, 1))),
                  "packed DAG coefficient")
    expect_reject(lambda: audit_toy(seal_toy(relators=(2, 2, 0))),
                  "packed DAG wrong leaf")
    expect_reject(lambda: audit_toy(seal_toy(parents=(3, 2))),
                  "packed DAG forward reference")
    expect_reject(lambda: audit_toy(seal_toy(
        kinds=(1, 1, 2, 1), relators=(1, 2, 0, 1),
        translations=(11, 12, 0, 11), offsets=(0, 0, 0, 2, 2))),
        "packed DAG unreachable node")
    expect_reject(lambda: audit_toy(seal_toy(
        roots=({"name": "toy_root", "node_id": 1},))),
        "packed DAG root mutation")
    bad_sha = json.loads(json.dumps(toy))
    bad_sha["arrays"]["node_kind"]["sha256"] = "0"*64
    expect_reject(lambda: audit_toy(bad_sha), "packed array SHA")
    bad_id = json.loads(json.dumps(toy))
    bad_id["arrays"]["leaf_translation_element_id"]["base64"] = "@@@="
    expect_reject(lambda: audit_toy(bad_id), "packed malformed base64")
    bad_cap = json.loads(json.dumps(toy))
    bad_cap["arrays"]["edge_parent_node_id"]["cap"] -= 1
    expect_reject(lambda: audit_toy(bad_cap), "packed array cap drift")
    print("D972_B345_RELFRAT3_V4_CHECKER_SELFTEST_PASS "
          "mutations=19 fox_orientation_canaries=2 packed_DAG_canaries=10 "
          "cheap_DP_direct=4 named_contexts=46 prefix_UNKNOWN=1 "
          "blocker_skip_retry=1 streaming_parent_release=1")


def _legacy_self_test_fixed_v6_unreachable() -> None:
    """One bounded test of only the fixed-candidate v6 cap successor."""
    changed_caps = {key for key in CAPS if CAPS[key] != V5_CAPS[key]}
    require(changed_caps == {"total_sparse_group_ring_keys", "element_pool"} and
            all(CAPS[key] == V5_CAPS[key] for key in set(CAPS)-changed_caps),
            "checker cap-only v5/v6 delta")
    validate_cap_calibration(dict(CAP_CALIBRATION))
    for key in ("new_sparse_cap", "new_pool_cap", "resume_used",
                "semantics_changed", "source_receipt_sha256"):
        bad = dict(CAP_CALIBRATION)
        bad[key] = (not bad[key] if isinstance(bad[key], bool) else
                    0 if isinstance(bad[key], int) else "0"*64)
        expect_reject(lambda bad=bad: validate_cap_calibration(bad),
                      f"cap calibration {key}")
    stride = CAPS["element_pool"]
    ids = [0, 1, 29, stride-1]
    keys = [left*stride+right for left in ids for right in ids]
    require(len(set(keys)) == len(keys) and
            all(divmod(key, stride) == pair for key, pair in
                zip(keys, ((left, right) for left in ids for right in ids))),
            "checker pool pair-key stride")
    old_prefix_live = V5_CAPS["total_sparse_group_ring_keys"]+1
    require(old_prefix_live > V5_CAPS["total_sparse_group_ring_keys"] and
            old_prefix_live <= CAPS["total_sparse_group_ring_keys"],
            "checker old-cap prefix continuation")
    utilization = {
        "live_sparse_entries": {"value": old_prefix_live,
            "cap": CAPS["total_sparse_group_ring_keys"],
            "ratio": old_prefix_live/CAPS["total_sparse_group_ring_keys"]},
        "element_pool_peak": {"value": 7, "cap": CAPS["element_pool"],
            "ratio": 7/CAPS["element_pool"]},
        "sparse_pivots": {"value": 3, "cap": CAPS["sparse_pivot_rows"],
            "ratio": 3/CAPS["sparse_pivot_rows"]},
        "DAG_nodes": {"value": 4, "cap": CAPS["provenance_dag_nodes"],
            "ratio": 4/CAPS["provenance_dag_nodes"]},
        "DAG_edges": {"value": 2, "cap": CAPS["provenance_dag_edges"],
            "ratio": 2/CAPS["provenance_dag_edges"]},
        "directed_section_expression_nodes": {
            "value": 0, "cap": CAPS["directed_section_expr_nodes"],
            "ratio": 0.0},
        "directed_section_expression_edges": {
            "value": 0, "cap": CAPS["directed_section_expr_edges"],
            "ratio": 0.0},
        "RSS_peak_bytes": {"value": 11, "cap": CAPS["producer_soft_rss_bytes"],
            "ratio": 11/CAPS["producer_soft_rss_bytes"]},
    }
    validate_cap_utilization(utilization, live=old_prefix_live, pool_peak=7,
                             pivots=3, dag_nodes=4, dag_edges=2, rss_peak=11)
    bad_utilization = json.loads(json.dumps(utilization))
    bad_utilization["live_sparse_entries"]["ratio"] = 1.0
    expect_reject(lambda: validate_cap_utilization(
        bad_utilization, live=old_prefix_live, pool_peak=7, pivots=3,
        dag_nodes=4, dag_edges=2, rss_peak=11), "cap utilization ratio")
    class TrivialQ:
        identity = 0

        @staticmethod
        def eval(word: Sequence[int]) -> int:
            return 0

    normalized = {"selected_inverse_words": [[i] for i in range(1, 7)]}
    targets = fixed_targets(TrivialQ(), normalized)  # type: ignore[arg-type]
    names = [name for name, _, _ in targets]
    require(len(targets) == 50 and names[5] == "hexagon_1_coface_0" and
            fixed_targets(TrivialQ(), normalized) == targets,
            "fixed direct target order/PASS regeneration")

    universe = {
        "kind": "fixed_positive_candidate", "correction_indices": [1],
        "correction_word": [], "fixed_outside_roof": {},
        "full_4096_universe_claimed": False,
        "earliest_global_candidate_claimed": False,
        "negative_completeness_claimed": False,
    }
    claim = {
        "registered_universe": universe,
        "terminal_token": "B345_RELFRAT3_PIVOT_SURGERY_UNKNOWN_RESOURCE",
        "claim_classification": "unknown_not_obstruction",
        "claim_scope": "fixed_candidate_pivot_surgery_only",
        "no_mathematical_obstruction_claimed": True,
    }
    validate_fixed_claim_boundary(claim)
    for key in ("full_4096_universe_claimed",
                "earliest_global_candidate_claimed",
                "negative_completeness_claimed"):
        bad = json.loads(json.dumps(claim))
        bad["registered_universe"][key] = True
        expect_reject(lambda bad=bad: validate_fixed_claim_boundary(bad), key)
    for key, value in (("claim_classification", "obstruction"),
                       ("claim_scope", "global_B4-B"),
                       ("no_mathematical_obstruction_claimed", False)):
        bad = json.loads(json.dumps(claim)); bad[key] = value
        expect_reject(lambda bad=bad: validate_fixed_claim_boundary(bad), key)

    prefix = {
        "fixed_candidate": {
            "correction_index": 1, "correction_word": [],
            "direct_gates_completed": True, "direct_gate_replay_count": 1,
            "target_count": 50, "target_order_sha256": digest_obj(names),
        },
        "current": {"checkpoint": 8, "correction_index": None,
                    "target_ordinal": None, "target_name": None},
        "blocker": {"count": 1, "sha256": digest_obj(["fixed"])},
        "transaction": {"starts": 2, "commits": 0, "rollbacks": 2},
        "structural_cap": {"hit": True, "reason": "element_pool",
                           "source": "registered_structural_cap"},
        "accounting": {"translations": 8, "basis_pivots": 2,
                       "basis_live_entries": 2, "pool_size": 7,
                       "DAG_nodes": 2, "DAG_edges": 1, "section_nodes": 8,
                       "PC_cache_hits": 1, "PC_cache_misses": 1,
                       "PC_cache_evictions": 0},
    }
    validate_fixed_prefix(prefix, names)
    bad_prefix = json.loads(json.dumps(prefix))
    bad_prefix["fixed_candidate"]["correction_word"] = [1]
    expect_reject(lambda: validate_fixed_prefix(bad_prefix, names),
                  "fixed correction mutation")

    first = {"candidate_index": 1, "target_ordinal": 6,
             "target_name": "hexagon_1_coface_0", "component": 4,
             "element_hex": "00", "failed_checkpoint": 1,
             "skip_checkpoints": [2], "retry_checkpoints": [4],
             "history_id": 1,
             "matching_introduction": {"component": 4, "element_hex": "00",
                                        "translation_ordinal": 3,
                                        "relator_index": 1}}
    second = {"candidate_index": 1, "target_ordinal": 7,
              "target_name": "hexagon_1_coface_1", "component": 5,
              "element_hex": "01", "failed_checkpoint": 4,
              "skip_checkpoints": [8], "retry_checkpoints": [],
              "history_id": 2}
    trace = [
        {"checkpoint": 1, "candidate_index": 1, "event": "missing_pivot",
         "target_ordinal": 6, "target_name": "hexagon_1_coface_0",
         "component": 4, "element_hex": "00", "blocker_history_id": 1,
         "pool_suffix_removed": 1},
        {"checkpoint": 2, "candidate_index": 1,
         "event": "missing_pivot_skip", "blocker_history_id": 1,
         "pool_element_present": False, "basis_pivot_present": False},
        {"checkpoint": 4, "candidate_index": 1,
         "event": "exact_pivot_retry", "blocker_history_id": 1,
         "matching_introduction": first["matching_introduction"]},
        {"checkpoint": 4, "candidate_index": 1, "event": "missing_pivot",
         "target_ordinal": 7, "target_name": "hexagon_1_coface_1",
         "component": 5, "element_hex": "01", "blocker_history_id": 2,
         "pool_suffix_removed": 2},
        {"checkpoint": 8, "candidate_index": 1,
         "event": "missing_pivot_skip", "blocker_history_id": 2,
         "pool_element_present": True, "basis_pivot_present": False},
    ]
    search = {
        "blocker_table": [second], "blocker_history": [first, second],
        "pivot_introductions": [first["matching_introduction"]],
        "checkpoint_trace": trace,
        "blocker_table_sha256": digest_obj([second]),
        "blocker_history_sha256": digest_obj([first, second]),
        "checkpoint_trace_sha256": digest_obj(trace),
        "geometric_translation_checkpoints": [1, 2, 4, 8],
    }
    validate_fixed_trace(search, 1)
    bad_trace = json.loads(json.dumps(search))
    bad_trace["blocker_history"][0]["target_ordinal"] = 5
    bad_trace["blocker_history_sha256"] = digest_obj(bad_trace["blocker_history"])
    expect_reject(lambda: validate_fixed_trace(bad_trace, 1),
                  "checkpoint-1 blocker imported/drifted")

    def seal_array(type_name: str, typecode: str, values: Sequence[int],
                   cap: int) -> dict[str, Any]:
        if typecode == "B":
            raw, itemsize = bytes(values), 1
        else:
            packed = array(typecode, values)
            if sys.byteorder != "little":
                packed.byteswap()
            raw, itemsize = packed.tobytes(), packed.itemsize
        return {"type": type_name, "array_typecode": typecode,
                "endianness": "little", "length": len(values),
                "itemsize": itemsize, "byte_length": len(raw), "cap": cap,
                "sha256": hashlib.sha256(raw).hexdigest(),
                "base64": base64.b64encode(raw).decode("ascii")}

    def packed_toy(coefficients: Sequence[int] = (1, 2)) -> dict[str, Any]:
        arrays = {
            "node_kind": seal_array("uint8", "B", (1, 1, 2),
                                      CAPS["provenance_dag_nodes"]),
            "leaf_relator_index": seal_array("uint16", "H", (1, 2, 0),
                                               CAPS["provenance_dag_nodes"]),
            "leaf_translation_element_id": seal_array(
                "uint32", "I", (11, 12, 0), CAPS["provenance_dag_nodes"]),
            "edge_offsets": seal_array("uint32", "I", (0, 0, 0, 2),
                                         CAPS["provenance_dag_nodes"]+1),
            "edge_parent_node_id": seal_array(
                "uint32", "I", (1, 2), CAPS["provenance_dag_edges"]),
            "edge_coefficient": seal_array(
                "uint8", "B", coefficients, CAPS["provenance_dag_edges"]),
        }
        roots = [{"name": "fixed_root", "node_id": 3}]
        manifest = {name: {key: value for key, value in row.items()
                           if key != "base64"} for name, row in arrays.items()}
        return {"format": "packed-parallel-arrays/v1", "field": 3,
                "node_order": "one_based_topological",
                "translation_action": "left", "arrays": arrays,
                "roots": roots, "node_count": 3, "edge_count": 2,
                "leaf_count": 2, "combination_node_count": 1,
                "all_serialized_nodes_reachable_from_roots": True,
                "unreachable_search_nodes_pruned": 0,
                "expanded_boundary_ledgers_serialized": False,
                "packed_manifest_sha256": digest_obj(
                    {"arrays": manifest, "roots": roots})}

    key_a: VKey = (1, ((0,), (0,)))
    key_b: VKey = (2, ((1,), (1,)))
    leaves = {(1, 11): {key_a: 1}, (2, 12): {key_b: 1}}
    def audit_packed(block: dict[str, Any]) -> None:
        roots, _ = evaluate_proof_dag(
            block, ["fixed_root"],
            lambda node: leaves[(node["relator_index"],
                                 node["translation_element_id"])])
        require(roots["fixed_root"] == {key_a: 1, key_b: 2},
                "packed PASS streaming replay")

    audit_packed(packed_toy())
    expect_reject(lambda: audit_packed(packed_toy((1, 1))),
        "packed coefficient mutation")
    require(TERMINALS == {
                "B345_RELFRAT3_PIVOT_SURGERY_PASS",
                "B345_RELFRAT3_PIVOT_SURGERY_INCOMPLETE",
                "B345_RELFRAT3_PIVOT_SURGERY_UNKNOWN_RESOURCE"},
            "fixed terminal set")
    print("D972_B345_RELFRAT3_PIVOT_SURGERY_V7_CHECKER_SELFTEST_PASS "
          "universe=1 dictionary_DP_calls=0 targets=50 blocker_ordinal=6 "
          "skip_retry_replace=1 prefix_UNKNOWN=1 packed_DAG_replay=1 "
          "claim_mutations=6 terminals=3 cap_delta=2 "
          "cap_mutations=6 stride_injective=1 old_cap_continue=1")


def self_test_pool_schedule() -> None:
    """Exercise the exact persistent-anchor/transient-probe helpers."""
    pc_receipt = {
        "generator_count": 1, "relative_orders": [3],
        "power_relations": [[0]], "inverses": [[2]],
        "conjugate_relations": [], "inverse_conjugate_relations": [],
    }
    collector = Collector(pc_receipt)
    identity = (p_one(4), collector.identity())
    g = ((1, 2, 0, 3), collector.identity())
    h = ((3, 1, 2, 0), collector.identity())
    q = Quotient(4, 4, collector,
                 [g, h, identity, identity, identity, identity])
    schedule_pool = ReplayPool(q)
    permutations: list[Perm] = []
    permutation_seen = {p_one(4)}
    permutation_queue: deque[Perm] = deque([p_one(4)])
    while permutation_queue:
        value = permutation_queue.popleft()
        permutations.append(value)
        for step in (g[0], h[0]):
            child = p_mul(value, step)
            if child not in permutation_seen:
                permutation_seen.add(child)
                permutation_queue.append(child)
    candidates: list[Element] = []
    for permutation in permutations:
        for pc_value in (0, 1, 2):
            candidate = (permutation, (pc_value,))
            blob = schedule_pool.pack(candidate)
            if candidate != q.identity and blob not in schedule_pool.ids:
                candidates.append(candidate)
    require(len(candidates) >= 8, "pool-schedule nontrivial toy supply")
    anchors = tuple(candidates[:6])
    anchor_start = schedule_pool.checkpoint()
    anchor_ids = seed_replay_source_anchors(schedule_pool, anchors)
    require(len(set(anchor_ids)) == 6 and
            schedule_pool.checkpoint() == anchor_start+6 and
            [schedule_pool.values[i] for i in anchor_ids] ==
                [schedule_pool.pack(value) for value in anchors],
            "six ordered persistent source anchors")
    expect_reject(lambda: seed_replay_source_anchors(
        ReplayPool(q), anchors[:5]), "source anchor count mutation")

    probe_values = tuple(candidates[6:8])
    probe_start = schedule_pool.checkpoint()

    def polluting_probe() -> list[bytes]:
        identifiers = [schedule_pool.intern(value) for value in probe_values]
        return [bytes(schedule_pool.values[i]) for i in identifiers]

    copied_probe = transactional_replay_probe(schedule_pool, polluting_probe)
    require(copied_probe == [schedule_pool.pack(value) for value in probe_values] and
            schedule_pool.checkpoint() == probe_start and
            all(schedule_pool.pack(value) not in schedule_pool.ids
                for value in probe_values),
            "target probe pool suffix rollback")
    polluted_pool = ReplayPool(q)
    seed_replay_source_anchors(polluted_pool, anchors)
    polluted_start = polluted_pool.checkpoint()
    for value in probe_values:
        polluted_pool.intern(value)
    require(polluted_pool.checkpoint() > polluted_start,
            "omitted probe rollback canary")


def self_test_v7() -> None:
    """Single bounded differential test for the v7-only contracts."""
    require(set(CAPS)-set(V6_CAPS) == {
                "directed_surgery_rounds", "directed_unique_translations",
                "directed_columns", "directed_section_expr_nodes",
                "directed_section_expr_edges"}, "v6/v7 cap delta")
    pc_receipt = {
        "generator_count": 1, "relative_orders": [3],
        "power_relations": [[0]], "inverses": [[2]],
        "conjugate_relations": [], "inverse_conjugate_relations": [],
    }
    collector = Collector(pc_receipt)
    identity = (p_one(4), collector.identity())
    # S4: g=(0 1 2), h=(0 3).  The four orientation words below are
    # pairwise distinct; an S3 reflection would normalize <g> and degenerate
    # the right-orientation mutation.
    g = ((1, 2, 0, 3), collector.identity())
    h = ((3, 1, 2, 0), collector.identity())
    q = Quotient(4, 4, collector,
                 [g, h, identity, identity, identity, identity])
    pool = ReplayPool(q)
    gid, hid = pool.intern(g), pool.intern(h)
    component = 1
    base = {replay_pack_key(component, hid): 1}
    basis = ReplayBasis(pool, [base])
    target = {replay_pack_key(component, gid): 1}
    require(basis.solve(target) == replay_pack_key(component, gid),
            "toy initial blocker")
    translation = q.mul(g, q.inverse(h))
    tid = pool.intern(translation)
    require(q.mul(translation, h) == g, "toy directed orientation")
    wrong = (q.mul(q.inverse(h), g), q.mul(q.inverse(g), h),
             q.mul(h, q.inverse(g)))
    require(len({translation, *wrong}) == 4 and
            q.mul(h, translation) != g,
            "three wrong orientations")
    basis.add_column(1, tid)
    require(basis.solve(target) is None, "directed column creates blocker key")
    before = len(basis.rows)
    basis.add_column(1, tid)
    require(len(basis.rows) == before and basis.dependent == 1,
            "duplicate directed column neutrality")

    self_test_pool_schedule()

    def seal_array(type_name: str, typecode: str, values: Sequence[int],
                   cap: int) -> dict[str, Any]:
        if typecode == "B":
            raw, itemsize = bytes(values), 1
        else:
            packed = array(typecode, values)
            if sys.byteorder != "little":
                packed.byteswap()
            raw, itemsize = packed.tobytes(), packed.itemsize
        return {"type": type_name, "array_typecode": typecode,
                "endianness": "little", "length": len(values),
                "itemsize": itemsize, "byte_length": len(raw), "cap": cap,
                "sha256": hashlib.sha256(raw).hexdigest(),
                "base64": base64.b64encode(raw).decode("ascii")}

    h_inv = q.inverse(h)
    values = [h, g, h_inv, translation]
    raw_values = b"".join(bytes(value[0])+bytes(value[1]) for value in values)
    expr_arrays = {
        "kind": seal_array("uint8", "B", [4, 4, 3, 2],
                            CAPS["directed_section_expr_nodes"]),
        "signed_generator": seal_array("int8", "b", [0, 0, 0, 0],
                                        CAPS["directed_section_expr_nodes"]),
        "left": seal_array("uint32", "I", [0, 0, 0, 1],
                            CAPS["directed_section_expr_nodes"]),
        "right": seal_array("uint32", "I", [0, 0, 0, 2],
                             CAPS["directed_section_expr_nodes"]),
        "flat_offsets": seal_array("uint32", "I", [0, 1, 2, 2, 2],
                                    CAPS["directed_section_expr_nodes"]+1),
        "flat_letters": seal_array(
            "int16", "h", [2, 1], CAPS["directed_section_expr_nodes"] *
            CAPS["single_word_or_section_length"]),
        "canonical_values": seal_array(
            "uint8", "B", list(raw_values),
            CAPS["directed_section_expr_nodes"] *
            (q.degree+q.collector.n)),
    }
    expr_manifest = {name: {key: value for key, value in row.items()
                            if key != "base64"}
                     for name, row in expr_arrays.items()}
    expr = {"format": "typed-section-expression-arrays/v1",
            "node_order": "zero_based_topological",
            "ordinary_word_composition": True,
            "canonical_value_width": q.degree+q.collector.n,
            "node_count": 4, "edge_count": 3, "roots": [3],
            "arrays": expr_arrays,
            "manifest_sha256": digest_obj({"arrays": expr_manifest,
                                             "roots": [3]})}
    decoded = decode_section_expressions(expr, q)
    require(decoded[3] == translation, "section product/inverse replay")
    forged = json.loads(json.dumps(expr))
    forged_values = bytearray(raw_values)
    # Mutate the permutation payload of the final PRODUCT node.  Its trailing
    # PC coordinate is zero in this toy, so replacing only the last byte by
    # zero would be a vacuous mutation.
    forged_values[3*(q.degree+q.collector.n)] ^= 1
    forged["arrays"]["canonical_values"] = seal_array(
        "uint8", "B", list(forged_values),
        CAPS["directed_section_expr_nodes"]*(q.degree+q.collector.n))
    forged_manifest = {name: {key: value for key, value in row.items()
                              if key != "base64"}
                       for name, row in forged["arrays"].items()}
    forged["manifest_sha256"] = digest_obj({"arrays": forged_manifest,
                                             "roots": [3]})
    expect_reject(lambda: decode_section_expressions(forged, q),
                  "forged section canonical value")

    empty_expr = {
        "format": "typed-section-expression-arrays/v1",
        "node_order": "zero_based_topological",
        "ordinary_word_composition": True,
        "canonical_value_width": q.degree+q.collector.n,
        "node_count": 0, "edge_count": 0, "roots": [], "arrays": {},
        "manifest_sha256": digest_obj({"arrays": {}, "roots": []}),
    }

    def one_leaf_proof(translation_id: int) -> dict[str, Any]:
        arrays = {
            "node_kind": seal_array(
                "uint8", "B", [1], CAPS["provenance_dag_nodes"]),
            "leaf_relator_index": seal_array(
                "uint16", "H", [1], CAPS["provenance_dag_nodes"]),
            "leaf_translation_element_id": seal_array(
                "uint32", "I", [translation_id],
                CAPS["provenance_dag_nodes"]),
            "edge_offsets": seal_array(
                "uint32", "I", [0, 0], CAPS["provenance_dag_nodes"]+1),
            "edge_parent_node_id": seal_array(
                "uint32", "I", [], CAPS["provenance_dag_edges"]),
            "edge_coefficient": seal_array(
                "uint8", "B", [], CAPS["provenance_dag_edges"]),
        }
        roots = [{"name": "directed_leaf", "node_id": 1}]
        manifest = {name: {key: value for key, value in row.items()
                           if key != "base64"}
                    for name, row in arrays.items()}
        return {
            "format": "packed-parallel-arrays/v1", "field": 3,
            "node_order": "one_based_topological",
            "translation_action": "left",
            "section_expressions": empty_expr,
            "arrays": arrays, "roots": roots, "node_count": 1,
            "edge_count": 0, "leaf_count": 1,
            "combination_node_count": 0,
            "all_serialized_nodes_reachable_from_roots": True,
            "unreachable_search_nodes_pruned": 0,
            "expanded_boundary_ledgers_serialized": False,
            "packed_manifest_sha256": digest_obj(
                {"arrays": manifest, "roots": roots}),
        }

    leaf_vector = {(1, g): 1}

    def resolve_directed_leaf(node: dict[str, Any]) -> Vector:
        require(node == {"relator_index": 1,
                         "translation_element_id": 7,
                         "translation_action": "left"},
                "directed leaf provenance")
        return dict(leaf_vector)

    proof_roots, _ = evaluate_proof_dag(
        one_leaf_proof(7), ["directed_leaf"], resolve_directed_leaf)
    require(proof_roots["directed_leaf"] == leaf_vector,
            "packed directed leaf replay")
    expect_reject(lambda: evaluate_proof_dag(
        one_leaf_proof(8), ["directed_leaf"], resolve_directed_leaf),
        "packed directed leaf provenance mutation")

    class TrivialQ:
        identity = 0

        @staticmethod
        def eval(word: Sequence[int]) -> int:
            return 0

    normalized = {"selected_inverse_words": [[i] for i in range(1, 7)]}
    acceptance, diagnostics = fixed_target_split(
        TrivialQ(), normalized)  # type: ignore[arg-type]
    require(len(acceptance) == 33 and len(diagnostics) == 17 and
            all(not row[0].startswith(("T_relation_", "TS_generator_"))
                for row in acceptance), "corrected 33/17 split")
    diagnostic_false = [{"name": row[0], "quotient_identity": False}
                        for row in diagnostics]
    require(len(acceptance) == 33 and not any(
        row["quotient_identity"] for row in diagnostic_false),
        "false diagnostics do not alter acceptance")
    expect_reject(lambda: require(
        [row[0] for row in acceptance][:-1] ==
        [row[0] for row in acceptance], "S/ST mutation"),
        "acceptance mutation")

    claim = {
        "terminal_token": "B345_RELFRAT3_PIVOT_SURGERY_INCOMPLETE",
        "registered_universe": {
            "kind": "fixed_positive_candidate", "correction_indices": [1],
            "correction_word": [], "full_4096_universe_claimed": False,
            "earliest_global_candidate_claimed": False,
            "negative_completeness_claimed": False},
        "claim_classification": "unknown_not_obstruction",
        "claim_scope": "fixed_candidate_pivot_surgery_only",
        "no_mathematical_obstruction_claimed": True,
        "full_universe_claimed": False, "negative_claimed": False,
    }
    validate_fixed_claim_boundary(claim)
    for token in ("B345_RELFRAT3_PIVOT_SURGERY_INCOMPLETE",
                  "B345_RELFRAT3_PIVOT_SURGERY_UNKNOWN_RESOURCE",
                  "B345_RELFRAT3_PIVOT_SURGERY_UNKNOWN_INPUT"):
        fixture = json.loads(json.dumps(claim))
        fixture["terminal_token"] = token
        validate_fixed_claim_boundary(fixture)
    require(TERMINALS == {
                "B345_RELFRAT3_PIVOT_SURGERY_PASS",
                "B345_RELFRAT3_PIVOT_SURGERY_INCOMPLETE",
                "B345_RELFRAT3_PIVOT_SURGERY_UNKNOWN_RESOURCE",
                "B345_RELFRAT3_PIVOT_SURGERY_UNKNOWN_INPUT"},
            "v7 terminal fixtures")
    # Persistent basis survives a candidate-local scratch rollback.
    scratch = dict(target); scratch.clear()
    require(len(basis.rows) == before and basis.solve(target) is None,
            "candidate rollback versus persistent directed basis")
    # A directed column can fail to create a needed pivot; that is INCOMPLETE.
    smaller = ReplayBasis(pool, [{replay_pack_key(1, pool.identity): 1,
                                  replay_pack_key(1, gid): 1}])
    smaller.add_column(1, pool.identity)
    require(smaller.solve(target) is not None,
            "new-smaller-pivot remains incomplete")
    print("D972_B345_RELFRAT3_PIVOT_SURGERY_V7_CHECKER_SELFTEST_PASS "
          "left_orientation=1 wrong_orientations=3 dedup=1 rollback=1 "
          "smaller_pivot_incomplete=1 sparse_oracle=1 terminals=4 "
          "acceptance=33 diagnostics=17 expression_mutation=1 "
          "source_anchors=6 probe_rollback=1")


def self_test_fixed() -> None:
    """Bounded differential test through the production v8 validation core."""
    self_test_pool_schedule()
    pc_receipt = {
        "generator_count": 1, "relative_orders": [3],
        "power_relations": [[0]], "inverses": [[2]],
        "conjugate_relations": [], "inverse_conjugate_relations": [],
    }
    collector = Collector(pc_receipt)
    identity = (p_one(4), collector.identity())
    # g is a 3-cycle and h does not commute with it.  This simultaneously
    # makes x^3 a nonzero Fox boundary with identity quotient value and keeps
    # the orientation canaries nondegenerate.
    g = ((1, 2, 0, 3), collector.identity())
    h = ((3, 1, 2, 0), collector.identity())
    quotient = Quotient(4, 4, collector,
                        [g, h, identity, identity, identity, identity])
    acceptance_names = ([f"charming_error_coface_{i}" for i in range(5)] +
                        [f"hexagon_{j}_coface_{i}" for j in (1, 2)
                         for i in range(5)] + ["ordered_A18_pentagon"] +
                        [f"S_relation_{i}" for i in range(1, 12)] +
                        [f"ST_generator_{i}" for i in range(1, 7)])
    diagnostic_names = ([f"T_relation_{i}" for i in range(1, 12)] +
                        [f"TS_generator_{i}" for i in range(1, 7)])
    require(len(acceptance_names) == 33 and len(diagnostic_names) == 17 and
            acceptance_names[5] == "hexagon_1_coface_0",
            "v8 shared-core corrected target order")

    def toy_builder(index: int, correction: Sequence[int],
                    inverse_words: Sequence[Sequence[int]]) -> dict[str, Any]:
        require(index in {1, 2} and list(correction) == [] and
                len(inverse_words) == 6,
                "v8 shared-core toy candidate provider")
        dag = CheckWordExpr(); one = dag.identity(6)
        x, y = dag.flat([1], 6), dag.flat([2], 6)
        cube = dag.flat([1, 1, 1], 6)
        xy = dag.product(x, y); inv_xy = dag.inverse(xy)
        orientation = dag.substitution([1, -2, 1],
                                       [xy, inv_xy, x, y, x, y])
        # Retain a real typed substitution root in every receipt.  It is a
        # source root and therefore passes through the production serializer
        # and source-root comparison, while its inverse product is zero.
        zero_orientation = dag.product(orientation,
                                       dag.inverse(orientation))
        acceptance = []
        for ordinal, name in enumerate(acceptance_names, 1):
            root = cube if index == 1 and ordinal == 6 else zero_orientation
            kind = ("charming" if ordinal <= 5 else
                    "hexagon" if ordinal <= 15 else
                    "pentagon" if ordinal == 16 else
                    "endomorphism_relation" if ordinal <= 27 else
                    "onto_two_sided_inverse")
            acceptance.append((name, kind, root))
        diagnostics = [(name, "diagnostic", x)
                       for name in diagnostic_names]
        source_roots = [one, one, one, one, one, one]
        correction_roots = [
            (f"correction_coarse_J_H_coface_{slot}", one)
            for slot in range(5)]
        return {
            "correction_index": index, "correction_word": [],
            "candidate_word": [], "candidate_exponent_sums": [0, 0],
            "dag": dag, "source_roots": source_roots,
            "inverse_roots": [one]*6,
            "correction_coface_roots": correction_roots,
            "acceptance": acceptance, "diagnostics": diagnostics,
            "orientation_root": orientation,
            "charming_witness": {
                "g_equals_f": True,
                "f_times_g_inverse_is_identity": True,
                "error_gradient_zero": True,
                "free_group_fact": "ker(F2->Z^2)=[F2,F2]"},
        }

    inverse_words = [[] for _ in range(6)]
    bridge_compiled_for_binding = toy_builder(1, [], inverse_words)
    bridge_candidate_binding = {
        "schema": SCHEMA, "candidate_index": 1,
        "correction_word_sha256": digest_obj([]),
        "candidate_word_sha256": digest_obj([]),
        "inverse_words_sha256": digest_obj(inverse_words),
        "acceptance_order_sha256": digest_obj(
            [(name, kind) for name, kind, _ in
             bridge_compiled_for_binding["acceptance"]]),
        "diagnostic_order_sha256": digest_obj(
            [(name, kind) for name, kind, _ in
             bridge_compiled_for_binding["diagnostics"]]),
    }
    toy_presentation_sha = digest_obj(quotient.collector.data)
    toy_leaf_sha = digest_obj([element_blob(value).hex()
                               for value in quotient.generators])
    toy_quotient_sha = digest_obj({
        "rank": quotient.rank, "degree": quotient.degree,
        "pc_rank": quotient.collector.n,
        "presentation_sha256": toy_presentation_sha,
        "leaf_bindings_sha256": toy_leaf_sha})
    toy_memo_accounting = {
        "format": "candidate-local-typed-gradient-memo/v1",
        "candidate_binding_sha256": digest_obj(bridge_candidate_binding),
        "quotient_binding_sha256": toy_quotient_sha,
        "presentation_sha256": toy_presentation_sha,
        "leaf_bindings_sha256": toy_leaf_sha,
        "key_binds_rank_arity_candidate_quotient_leafs": True,
        "equal_group_value_is_not_a_cache_key": True,
        "cross_candidate_sharing": False,
        "pool_or_proof_identifiers_stored": False,
        "node_cap": CAPS["gradient_memo_nodes"],
        "sparse_entry_cap": CAPS["gradient_memo_sparse_entries"],
        "estimated_bytes_per_sparse_entry":
            CAPS["gradient_memo_estimated_bytes_per_sparse_entry"],
        "additional_budget_bytes":
            CAPS["gradient_memo_additional_budget_bytes"],
        "hits": 7, "misses": 11, "evictions": 1,
        "skipped_oversize": 0, "recomputations": 1,
        "peak_cached_nodes": 6, "peak_cached_sparse_entries": 12,
        "peak_working_plus_cached_sparse_entries": 15,
        "pinned_source_count": 6, "requested_source_count": 6,
        "unretained_requested_source_count": 0,
        "pin_store_fallbacks": 0, "pin_evictions": 0,
        "cache_capacity_is_nonterminal": True, "rollbacks": 0,
        "discarded_nodes": 0, "discarded_sparse_entries": 0,
        "eviction_changes_performance_only": True,
    }
    bridge = {
        "mandatory": True, "target_count": 50,
        "acceptance_target_count": 33, "diagnostic_target_count": 17,
        "original_target_order_preserved": True,
        "all_reduced_words_equal": True,
        "all_quotient_values_equal": True,
        "all_left_Fox_gradients_equal": True,
        "cold_route": "frozen v8 flat literal fox_gradient",
        "memo_route": "candidate-local typed WordExpr chain rule",
        "bindings_sha256": digest_obj(["sealed-shared-core"]),
        "old_flat_cap": CAPS["single_word_or_section_length"],
        "membership_fused": True,
        "membership_reused_target_count": 6,
        "first_missing_target_ordinal": 6,
        "first_missing_target_name": "hexagon_1_coface_0",
        "remaining_canaries_completed_after_first_missing": 44,
        "missing_target_re_evaluated": False,
        "memo_binding": toy_memo_accounting,
    }

    def bridge_validator(compiled: dict[str, Any],
                         evaluator: CheckWordExprEvaluator,
                         e4: Quotient, normalized: dict[str, Any]) \
            -> dict[str, Any]:
        require(compiled["correction_index"] == 1 and e4 is quotient and
                evaluator.q is quotient and
                normalized == {"selected_inverse_words": inverse_words},
                "v8 shared-core flat bridge provider")
        return {key: value for key, value in bridge.items() if key not in {
            "membership_fused", "membership_reused_target_count",
            "first_missing_target_ordinal", "first_missing_target_name",
            "remaining_canaries_completed_after_first_missing",
            "missing_target_re_evaluated", "memo_binding"}}

    # Build the exact two-record packed receipt independently of the validator:
    # candidate 1 has the registered target-6 missing pivot, candidate 2 PASSes.
    # ReplayBasis and its pool must be identical objects.
    fixture_pool = ReplayPool(quotient)
    fixture_basis = ReplayBasis(fixture_pool, [])
    fixture_records: list[dict[str, Any]] = []
    max_suffix = 0; max_live = 0
    for index in (1, 2):
        checkpoint = fixture_pool.checkpoint()
        compiled = toy_builder(index, [], inverse_words)
        evaluator = CheckWordExprEvaluator(compiled["dag"], quotient)
        evaluator.evaluate_values()
        diagnostics = check_expr_diagnostics(compiled, evaluator)
        diag_pass = sum(row["quotient_identity"] for row in diagnostics)
        diag_sha = digest_obj(diagnostics)
        bindings: list[dict[str, Any]] = []
        missing = None; failed_name = ""; failed_kind = ""; failed_ordinal = 0
        entries = 0
        for ordinal, (name, kind, root) in enumerate(
                compiled["acceptance"], 1):
            value = evaluator.values[root-1]
            require(value == quotient.identity,
                    "v8 shared-core toy acceptance quotient")
            gradient = evaluator.gradients([root])[root]
            bindings.append(check_gradient_binding(name, kind, gradient, value))
            entries += len(gradient)
            packed = pack_check_gradient(gradient, fixture_pool)
            missing = fixture_basis.solve(packed)
            max_suffix = max(max_suffix,
                             len(fixture_pool.values)-checkpoint)
            if missing is not None:
                failed_name, failed_kind, failed_ordinal = name, kind, ordinal
                break
        max_live = max(max_live, evaluator.target_gradient_entry_peak)
        roots = [root for _, _, root in
                 compiled["acceptance"]+compiled["diagnostics"]]
        accounting = compiled["dag"].accounting(roots)
        expression_sha = check_expr_digest(compiled["dag"])
        if missing is not None:
            component, identifier = replay_unpack_key(missing)
            blocker = fixture_pool.values[identifier]
            removed = fixture_pool.rollback(checkpoint)
            record = {
                "candidate_index": index, "outcome": "MISSING_PIVOT",
                "outcome_code": 2, "failed_name": failed_name,
                "failed_kind": failed_kind,
                "failed_target_ordinal": failed_ordinal,
                "blocker_component": component,
                "blocker_value_hex": blocker.hex(),
                "blocker_value_sha256": hashlib.sha256(blocker).hexdigest(),
                "gradient_entry_count": entries,
                "failed_gradient_entry_count": bindings[-1]["entry_count"],
                "gradient_bindings_sha256": digest_obj(bindings),
                "diagnostic_pass_count": diag_pass,
                "diagnostic_values_sha256": diag_sha,
                "wordexpr_sha256": expression_sha,
                "wordexpr_nodes": accounting["node_count"],
                "wordexpr_edges": accounting["edge_count"],
                "wordexpr_max_expanded_letters":
                    accounting["max_expanded_letter_count"],
                "wordexpr_live_gradient_peak":
                    evaluator.target_gradient_entry_peak,
                "pool_suffix_removed": removed,
            }
        else:
            removed = fixture_pool.rollback(checkpoint)
            record = {
                "candidate_index": index, "outcome": "PASS",
                "outcome_code": 3, "failed_name": "",
                "failed_target_ordinal": 0, "blocker_component": 0,
                "blocker_value_hex": element_blob(quotient.identity).hex(),
                "blocker_value_sha256": hashlib.sha256(
                    element_blob(quotient.identity)).hexdigest(),
                "gradient_entry_count": entries,
                "gradient_bindings_sha256": digest_obj(bindings),
                "diagnostic_pass_count": diag_pass,
                "diagnostic_values_sha256": diag_sha,
                "wordexpr_sha256": expression_sha,
                "wordexpr_nodes": accounting["node_count"],
                "wordexpr_edges": accounting["edge_count"],
                "wordexpr_max_expanded_letters":
                    accounting["max_expanded_letter_count"],
                "wordexpr_live_gradient_peak":
                    evaluator.target_gradient_entry_peak,
                "pool_suffix_removed": removed,
            }
        fixture_records.append(record)
    require(fixture_records[0]["failed_target_ordinal"] == 6 and
            fixture_records[1]["outcome"] == "PASS",
            "v8 shared-core fixture scan order")

    def seal_array(type_name: str, typecode: str, values: Sequence[int],
                   cap: int) -> dict[str, Any]:
        if typecode == "B":
            raw, itemsize = bytes(values), 1
        else:
            packed = array(typecode, values)
            if sys.byteorder != "little":
                packed.byteswap()
            raw, itemsize = packed.tobytes(), packed.itemsize
        return {"type": type_name, "array_typecode": typecode,
                "endianness": "little", "length": len(values),
                "itemsize": itemsize, "byte_length": len(raw), "cap": cap,
                "sha256": hashlib.sha256(raw).hexdigest(),
                "base64": base64.b64encode(raw).decode("ascii")}

    width = fixture_pool.width
    arrays = {
        "candidate_index": seal_array("uint32", "I", [1, 2],
                                        CAPS["candidate_scan_records"]),
        "outcome_code": seal_array("uint8", "B",
                                     [row["outcome_code"]
                                      for row in fixture_records],
                                     CAPS["candidate_scan_records"]),
        "failed_target_ordinal": seal_array(
            "uint8", "B", [row["failed_target_ordinal"]
                            for row in fixture_records],
            CAPS["candidate_scan_records"]),
        "blocker_component": seal_array(
            "uint8", "B", [row["blocker_component"]
                            for row in fixture_records],
            CAPS["candidate_scan_records"]),
        "blocker_value": seal_array(
            "fixed_width_bytes", "B",
            list(b"".join(bytes.fromhex(row["blocker_value_hex"])
                          for row in fixture_records)),
            CAPS["candidate_scan_records"]*width),
        "diagnostic_pass_count": seal_array(
            "uint8", "B", [row["diagnostic_pass_count"]
                            for row in fixture_records],
            CAPS["candidate_scan_records"]),
    }
    manifest = {name: {key: value for key, value in row.items()
                       if key != "base64"} for name, row in arrays.items()}
    public_records = [{key: value for key, value in row.items()
                       if key != "blocker_value_hex"}
                      for row in fixture_records]
    distribution: dict[str, int] = {}
    for row in fixture_records:
        label = row["outcome"]+":"+row.get("failed_name", "")
        distribution[label] = distribution.get(label, 0)+1
    scan = {
        "format": "registered-wordexpr-scan-arrays/v1", "evaluated": 2,
        "complete": False, "element_width_bytes": width,
        "outcome_codes": {
            "1": "direct_gate_or_acceptance_quotient_failure",
            "2": "fixed_basis_missing_pivot", "3": "PASS"},
        "arrays": arrays, "array_manifest_sha256": digest_obj(manifest),
        "record_bindings": public_records,
        "record_bindings_sha256": digest_obj(fixture_records),
        "evaluated_index_order_sha256": digest_obj([1, 2]),
        "failure_distribution": distribution,
        "registered_corrections": 4096,
        "registered_dictionary_complete": True,
        "full_H3_fibre_complete": False, "full_universe_claimed": False,
        "earliest_global_candidate_claimed": False,
        "negative_completeness_claimed": False,
        "candidate_order": "1..4096 exactly once after saturated v7 prefix",
        "candidate_order_sha256": digest_obj(
            [digest_obj([]) for _ in range(4096)]),
        "candidate_order_equals_frozen_v8": True,
        "acceptance_target_count": 33, "diagnostic_target_count": 17,
        "candidate1_bridge_membership_fused": True,
        "fixed_basis_immutable_during_scan": True,
        "membership_first_pass_allocates_provenance_nodes": False,
        "transaction": {
            "membership_starts": 2, "membership_rollbacks": 2,
            "proof_starts": 1, "proof_commits": 1, "proof_rollbacks": 0,
            "failed_candidate_DAG_nodes_allocated": 0,
            "max_pool_suffix": max_suffix,
            "max_live_gradient_entries": max_live},
        "runtime_seconds": 0.0,
    }

    compiled = toy_builder(2, [], inverse_words)
    evaluator = CheckWordExprEvaluator(compiled["dag"], quotient)
    evaluator.evaluate_values()
    selected_bindings = [check_gradient_binding(name, kind,
        evaluator.gradients([root])[root], evaluator.values[root-1])
        for name, kind, root in compiled["acceptance"]]
    named = ([(name, root) for name, _, root in
              compiled["acceptance"]+compiled["diagnostics"]] +
             [(f"source_{i+1}", root)
              for i, root in enumerate(compiled["source_roots"])] +
             list(compiled["correction_coface_roots"]))
    payload = compiled["dag"].serialize(named)
    root_ids = {row["name"]: row["node_id"] for row in payload["roots"]}
    correction_gates = []
    for name, root in compiled["correction_coface_roots"]:
        value = evaluator.values[root-1]
        correction_gates.append({
            "name": name, "wordexpr_root_node_id": root_ids[name],
            "quotient_value_hex": element_blob(value).hex(),
            "quotient_identity": True})

    empty_sections = {
        "format": "typed-section-expression-arrays/v1",
        "node_order": "zero_based_topological",
        "ordinary_word_composition": True,
        "canonical_value_width": quotient.degree+quotient.collector.n,
        "node_count": 0, "edge_count": 0, "roots": [], "arrays": {},
        "manifest_sha256": digest_obj({"arrays": {}, "roots": []}),
    }
    proof_arrays = {
        "node_kind": seal_array("uint8", "B", [2],
                                  CAPS["provenance_dag_nodes"]),
        "leaf_relator_index": seal_array("uint16", "H", [0],
                                           CAPS["provenance_dag_nodes"]),
        "leaf_translation_element_id": seal_array(
            "uint32", "I", [0], CAPS["provenance_dag_nodes"]),
        "edge_offsets": seal_array("uint32", "I", [0, 0],
                                     CAPS["provenance_dag_nodes"]+1),
        "edge_parent_node_id": seal_array("uint32", "I", [],
                                            CAPS["provenance_dag_edges"]),
        "edge_coefficient": seal_array("uint8", "B", [],
                                         CAPS["provenance_dag_edges"]),
    }
    proof_roots = [{"name": name, "node_id": 1}
                   for name in acceptance_names]
    proof_manifest = {name: {key: value for key, value in row.items()
                             if key != "base64"}
                      for name, row in proof_arrays.items()}
    proof = {
        "format": "packed-parallel-arrays/v1", "field": 3,
        "node_order": "one_based_topological", "translation_action": "left",
        "section_expressions": empty_sections, "arrays": proof_arrays,
        "roots": proof_roots, "node_count": 1, "edge_count": 0,
        "leaf_count": 0, "combination_node_count": 1,
        "all_serialized_nodes_reachable_from_roots": True,
        "unreachable_search_nodes_pruned": 0,
        "expanded_boundary_ledgers_serialized": False,
        "packed_manifest_sha256": digest_obj(
            {"arrays": proof_manifest, "roots": proof_roots}),
    }
    certificates = [{
        "name": name, "kind": kind,
        "wordexpr_root_node_id": root_ids[name],
        "quotient_identity": True, "gradient_binding": binding,
        "proof_root_node_id": 1,
        "proof_system": "shared_topological_F3_provenance_DAG"}
        for (name, kind, _), binding in
        zip(compiled["acceptance"], selected_bindings)]

    frozen_tuple = tuple(identity for _ in range(6))
    source_hex = [element_blob(value).hex() for value in frozen_tuple]
    source_ledger = hashlib.sha256()
    tuple_sha = digest_obj(source_hex)
    for index in range(1, 4097):
        source_ledger.update(canonical_bytes([index, source_hex, [0, 0]])+b"\n")
    preflight = {
        "complete": True, "evaluated": 4096,
        "all_equal_to_frozen_tuple": True, "first_difference": None,
        "tuple_sha256_by_candidate": [tuple_sha]*4096,
        "tuple_ledger_sha256": source_ledger.hexdigest(),
        "candidate_exponent_sums": [[0, 0] for _ in range(4096)],
        "all_candidate_exponent_sums_zero": True,
        "frozen_tuple_hex": source_hex, "context_count": 6,
        "signed_seed_images_sha256": digest_obj("sealed-source-provider"),
        "recurrence": "rho(c_i)=rho(c_parent)*rho(signed_seed)",
        "raw_descendant_words_evaluated": False,
    }
    dictionary = {"words": [[] for _ in range(4096)], "count": 4096}
    dictionary_receipt = {
        "count": 4096, "registered_dictionary_complete": True,
        "word_sha256": [digest_obj([]) for _ in range(4096)],
        "candidate_order_sha256": digest_obj(
            [digest_obj([]) for _ in range(4096)]),
        "equals_frozen_v8_order": True,
        "order": "identity then authenticated signed-seed BFS"}
    normalized = {"selected_inverse_words": inverse_words}
    trace: dict[str, int] = {}
    expected_canary = {
        key: fixture_records[0][key] for key in
        ("outcome", "failed_target_ordinal", "failed_name",
         "blocker_component", "blocker_value_sha256")}
    scan_setup = {
        "candidate_builder": toy_builder,
        "bridge_validator": bridge_validator,
        "candidate1_expected": expected_canary, "trace": trace}

    def no_leaf(_: dict[str, Any]) -> Vector:
        raise Reject("v8 sealed zero proof unexpectedly requested a leaf")

    selected_setup = {
        "leaf_resolver": no_leaf, "expected_registry": [],
        "expected_fox_models": {}, "trace": trace}
    setup_pool = ReplayPool(quotient)
    setup_basis = ReplayBasis(setup_pool, [])
    expected_pins = {"sealed_dependency_provider":
                     "external-q3-and-fresh-v7-only"}
    fixed_roof = {
        "row_index": 37, "exponent": 2, "roof_key": "sealed-row37",
        "typed_source_word": list(FIXED_WORD),
        "arithmetic_outside_by_index_three": True,
        "source": "frozen q3 selected outside roof"}
    representation = {
        "version": "typed-wordexpr-memo-fusion-v9",
        "persistent_element_equality":
            "exact canonical bytes; never a digest",
        "sparse_keys":
            "component plus stable zero-based exact element-pool ID",
        "pivot_order": "component then canonical EKey bytes; never insertion ID",
        "BFS_order": "+1..+6,-1..-6 first-seen shortlex",
        "candidate_sections_retained": False,
        "candidate_wordexpr_retained_across_candidates": False,
        "substituted_descendants_flattened": False,
        "left_Fox_product_rule": "D(uv)=D(u)+value(u)*D(v)",
        "left_Fox_inverse_rule": "D(u^-1)=-value(u)^-1*D(u)",
        "negative_substitution_letter":
            "advance prefix by value(a_i)^-1, then subtract prefix*D(a_i)",
        "section_oracle":
            "BFS/direct translations only, canonical-byte-bound typed expression DAG",
        "all_element_pool_values_have_sections": False,
        "candidate_gradients_retained_across_checkpoints": False,
        "candidate_local_typed_gradient_memo": True,
        "memo_key":
            "typed node identity + rank/arity + candidate + quotient/presentation + leaf bindings",
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
        "candidate_transaction":
            "exact element-pool and provenance-DAG suffix rollback",
        "missing_pivot_blocker":
            "target ordinal, component, canonical E4 bytes",
        "proof_DAG_in_memory": "packed parallel arrays",
        "positive_DAG_serialization":
            "reachable union as typed little-endian base64 arrays",
        "cache_eviction_semantics":
            "capacity and eviction order affect speed only, never canonical values or search order",
        "persistent_checkpoint_resume": False,
        "correction_dictionary_constructed": True,
        "complete_source_tuple_DP_executed_before_sparse_growth": True,
        "cap_calibration_only": False,
        "resume_or_checkpoint_imported": False}
    theorem = {
        "proved_if_PASS":
            "one registered literal outside pair survives every isolated elementary-F3 chief refinement L with Phi3(H4)<=L<=H4",
        "Phi3_H4_isolation_required": False,
        "covered":
            "all isolated elementary-F3 next-chief refinements immediately below current H4",
        "not_covered": ["nonabelian chief factors", "other primes",
                        "deeper iteration", "uniform cofinal tower",
                        "global B4-B"]}
    memo_summary = {
        "format": "candidate-local-typed-gradient-memo-summary/v1",
        "candidate_evaluators": 2,
        "proof_regeneration_evaluators": 1,
        "hits": 9, "misses": 21, "evictions": 1,
        "recomputations": 1, "skipped_oversize": 0,
        "peak_cached_nodes": 8, "peak_cached_sparse_entries": 12,
        "peak_working_plus_cached_sparse_entries": 15,
        "source_roots_requested_per_pin_stage": 6,
        "pin_policy":
            "candidate1 after direct gate before 50 bridge; ordinary only before acceptance target 17; proof fresh evaluator",
        "ordinary_lazy_pin_target_ordinal": 17,
        "candidate1_bridge_pin_stages": 1,
        "ordinary_lazy_pin_stages": 1,
        "proof_pin_stages": 1,
        "pin_stage_count": 3, "pin_requests_total": 18,
        "pin_store_fallbacks": 0, "pin_evictions": 0,
        "peak_retained_pinned_source_count": 6,
        "direct_failures_before_pin": 0,
        "ordinary_exits_before_target17": 0,
        "cross_candidate_cache_entries": 0,
        "candidate_memos_discarded_at_rollback": 2,
        "phase_elapsed_seconds": {
            "value_evaluation": 0.1, "source_anchor_pin": 0.1,
            "candidate1_bridge_and_membership": 0.1,
            "ordinary_membership": 0.1, "proof_regeneration": 0.1},
        "progress_interval_seconds": 10,
        "static_quotient_binding_precomputed_once": True,
        "inverse_words_binding_precomputed_once": True,
        "target_order_binding_hashes_computed_once": True,
        "candidate_order_changed": False,
        "acceptance_or_diagnostic_promotion_changed": False,
        "memo_eviction_is_terminal_or_rejection": False,
        "cache_entry_budget_bytes":
            CAPS["gradient_memo_additional_budget_bytes"],
        "working_plus_cached_accounted_under_frozen_live_cap": True,
    }

    repo = Path(__file__).resolve().parents[1]
    selected_pair = {
        "correction_index": 2, "correction_word": [],
        "correction_word_sha256": digest_obj([]), "candidate_word": [],
        "candidate_word_sha256": digest_obj([]),
        "candidate_exponent_sums": [0, 0],
        "fixed_inverse_words": inverse_words,
        "fixed_inverse_words_sha256": digest_obj(inverse_words),
        "source_expression_roots":
            [root_ids[f"source_{i}"] for i in range(1, 7)],
        "diagnostics": check_expr_diagnostics(compiled, evaluator, root_ids),
        "correction_coarse_J_H_coface_gates": correction_gates,
        "correction_coarse_J_H_all_five": True,
        "correction_in_finer_J_Phi_required": False,
        "diagnostics_feed_acceptance": False,
        "acceptance_target_count": 33, "diagnostic_target_count": 17,
        "T_canaries_required_for_acceptance": False,
        "corrected_Def2_9_IF_FIRST_frozen_pre_run": True,
        "operational_first_passing_registered_index": 2,
        "mathematical_minimality_claimed": False,
        "charming_witness": compiled["charming_witness"],
        "friendly_gate": {
            "m": 0, "lambda": 1,
            "frozen_q3_selected_solution_replayed": True,
            "all_five_coarse_correction_cofaces_identity": True},
        "marking_gate": {"m": 0, "lambda": 1,
                           "additional_residuals": []},
        "outside_roof_gate": fixed_roof}
    common = {
        "schema": SCHEMA, "status": "B345_RELFRAT3_WORDEXPR_PASS",
        "terminal_token": "B345_RELFRAT3_WORDEXPR_PASS",
        "reason": "sealed_shared_production_core_positive",
        "pins": expected_pins,
        "source_hashes": {
            "producer_sha256": digest_file(repo/V9_PRODUCER),
            "checker_sha256": digest_file(repo/V9_CHECKER),
            "driver_sha256": digest_file(repo/V9_DRIVER)},
        "input_q3_terminal": "sealed_q3_setup",
        "output_path": str(OUTPUT_PATH).replace("\\", "/"),
        "caps": CAPS, "cap_calibration": CAP_CALIBRATION,
        "resource_guards": {
            "minutes": 120, "seconds": 7200,
            "rss_bytes": CAPS["producer_soft_rss_bytes"],
            "external_job_limit_minutes": 330,
            "terminal_on_hit": "B345_RELFRAT3_WORDEXPR_UNKNOWN_RESOURCE",
            "hit": False},
        "performance": {"sealed_shared_core": True},
        "registered_universe": {
            "kind": "registered_4096_wordexpr_positive_search",
            "registered_corrections": 4096,
            "registered_dictionary_complete": True,
            "full_H3_fibre_complete": False,
            "fixed_outside_roof": fixed_roof,
            "full_universe_claimed": False,
            "earliest_global_candidate_claimed": False,
            "negative_completeness_claimed": False,
            "marking_m": 0, "lambda": 1},
        "representation_contract": representation,
        "claim_classification": "positive_certificate",
        "claim_scope": "registered_4096_wordexpr_positive_search_only",
        "no_mathematical_obstruction_claimed": True,
        "full_universe_claimed": False, "negative_claimed": False,
        "theorem_boundary": theorem,
        "prohibited_work": {
            "relative_ANUPQ_calls": 0, "Reidemeister_Schreier": False,
            "full_Elements": False, "full_regular_matrices": False,
            "full_H1_basis_or_rank": False, "registered_corrections": 4096,
            "all_dictionary_DP_executed": True},
        "correction_dictionary": dictionary_receipt,
        "normalized_inverse_fibre": normalized,
        "source_tuple_preflight": preflight,
        "candidate1_flat_bridge": bridge,
        "gradient_memo_performance": memo_summary,
        "wordexpr_scan": scan,
        "search": {
            "registered_correction_indices": [1, 2],
            "other_corrections_constructed_or_evaluated": 1,
            "correction_dictionary_constructed": True,
            "complete_source_tuple_DP_executed": True,
            "candidate_membership_tests": 2,
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
            "selected_candidate_regenerated_and_exactly_compared": True},
        "direct_lane": {"literal_pair_found": True,
                         "PB5_branch_constructed": False,
                         "stop_reason":
                             "FIRST_REGISTERED_WORDEXPR_LITERAL_PAIR"},
        "selected_wordexpr_dag": payload,
        "selected_pair": selected_pair,
        "boundary_certificates": certificates,
        "boundary_proof_dag": proof,
        "quotient_element_registry": [], "fox_models": {},
    }
    context = {
        "expected_pins": expected_pins, "trace": trace,
        "e3": quotient, "e4": quotient, "dictionary": dictionary,
        "dictionary_receipt": dictionary_receipt,
        "normalized": normalized, "frozen_tuple": frozen_tuple,
        "inverse_words": inverse_words, "preflight": preflight,
        "tuples": [frozen_tuple for _ in range(4096)],
        "pool": setup_pool, "basis": setup_basis,
        "scan_setup": scan_setup, "selected_setup": selected_setup}
    toy_q3 = {
        "terminal_token": "sealed_q3_setup",
        "selected_solution": {
            "roof_row_index": 37, "exponent": 2, "correction_index": 1,
            "marking_m": 0, "lambda": 1, "typed_source_word": FIXED_WORD,
            "roof_key": "sealed-row37",
            "arithmetic_outside_by_index_three": True},
        "_sealed_setup_kind": "external-q3-and-fresh-v7-only",
        "_sealed_trace": trace, "_sealed_validation_context": context}
    validate_v8_receipt(common, toy_q3, Path("."), repo,
                        sealed_selftest=True)
    require(trace == {
                "envelope_validator_entries": 1,
                "source_preflight_validator_entries": 1,
                "scan_validator_entries": 1,
                "selected_validator_entries": 1,
                "proof_validator_entries": 1},
            "v8 sealed receipt traverses full shared production core")

    # These positive mutations all re-enter the production scan and selected
    # proof functions.  The trace counters prove that no fixture-only early
    # return accepted or rejected them.
    mutation_paths = [
        ("opcode", lambda x: x["selected_wordexpr_dag"]["nodes"][0].update(
            {"opcode": "PRODUCT"}), "selected"),
        ("rank", lambda x: x["selected_wordexpr_dag"]["nodes"][0].update(
            {"rank": 5}), "selected"),
        ("child", lambda x: x["selected_wordexpr_dag"]["nodes"][-1].update(
            {"children": []}), "selected"),
        ("flat leaf", lambda x: x["selected_wordexpr_dag"]["nodes"][1].update(
            {"flat_word": [2]}), "selected"),
        ("gradient", lambda x: x["boundary_certificates"][0]
            ["gradient_binding"].update(
                {"canonical_gradient_sha256": "0"*64}), "selected"),
        ("proof", lambda x: x["boundary_proof_dag"].update(
            {"translation_action": "right"}), "proof"),
        ("S relation", lambda x: x["boundary_certificates"][16].update(
            {"name": "S_relation_mutated"}), "selected"),
        ("ST recovery", lambda x: x["boundary_certificates"][-1].update(
            {"name": "ST_generator_mutated"}), "selected"),
        ("source tuple", lambda x: x["source_tuple_preflight"].update(
            {"all_equal_to_frozen_tuple": False}), "preflight"),
        ("diagnostic claim", lambda x: x["selected_pair"].update(
            {"diagnostics_feed_acceptance": True}), "selected"),
        ("memo forged candidate key", lambda x: x["candidate1_flat_bridge"]
            ["memo_binding"].update(
                {"candidate_binding_sha256": "0"*64}), "scan"),
        ("memo cache terminalization", lambda x: x["candidate1_flat_bridge"]
            ["memo_binding"].update(
                {"cache_capacity_is_nonterminal": False}), "scan"),
        ("memo lazy pin stage", lambda x: x["gradient_memo_performance"].update(
            {"ordinary_lazy_pin_target_ordinal": 16}), "scan"),
        ("dropped bridge canary", lambda x: x["candidate1_flat_bridge"].update(
            {"target_count": 49}), "scan"),
        ("candidate order", lambda x: x["wordexpr_scan"].update(
            {"candidate_order": "2..4096,1"}), "scan"),
        ("acceptance demotion", lambda x: x["wordexpr_scan"].update(
            {"acceptance_target_count": 32}), "scan"),
        ("global claim", lambda x: x.update({"negative_claimed": True}),
         "envelope"),
    ]
    shared_positive_mutations = 0
    for label, mutate, expected_entry in mutation_paths:
        bad = copy.deepcopy(common); mutate(bad)
        before = dict(trace)
        expect_reject(lambda bad=bad: validate_v8_receipt(
            bad, toy_q3, Path("."), repo, sealed_selftest=True), label)
        require(trace["envelope_validator_entries"] >
                    before.get("envelope_validator_entries", 0),
                f"v8 mutation envelope entry: {label}")
        if expected_entry in {"preflight", "scan", "selected", "proof"}:
            require(trace["source_preflight_validator_entries"] >
                        before.get("source_preflight_validator_entries", 0),
                    f"v8 mutation source core entry: {label}")
        if expected_entry in {"scan", "selected", "proof"}:
            require(trace["scan_validator_entries"] >
                        before.get("scan_validator_entries", 0) and
                    (expected_entry == "scan" or
                     trace["selected_validator_entries"] >
                        before.get("selected_validator_entries", 0)),
                    f"v9 mutation scan/selected core entry: {label}")
        if expected_entry in {"selected", "proof"}:
            shared_positive_mutations += 1
        if expected_entry == "proof":
            require(trace["proof_validator_entries"] >
                        before.get("proof_validator_entries", 0),
                    "v8 proof mutation production core entry")

    def nonpositive_base(token: str, reason: str) -> dict[str, Any]:
        row = copy.deepcopy(common)
        for key in ("direct_lane", "selected_wordexpr_dag", "selected_pair",
                    "boundary_certificates", "boundary_proof_dag",
                    "quotient_element_registry", "fox_models", "search",
                    "candidate1_flat_bridge", "wordexpr_scan",
                    "gradient_memo_performance"):
            row.pop(key, None)
        row["status"] = row["terminal_token"] = token
        row["reason"] = reason
        row["claim_classification"] = "unknown_not_obstruction"
        row["resource_guards"]["hit"] = \
            token == "B345_RELFRAT3_WORDEXPR_UNKNOWN_RESOURCE"
        return row

    def injected_q3(ctx: dict[str, Any], local_trace: dict[str, int]) \
            -> dict[str, Any]:
        row = dict(toy_q3)
        row["_sealed_trace"] = local_trace
        row["_sealed_validation_context"] = ctx
        return row

    # SEARCH_INCOMPLETE reason 1: same production preflight branch, with a
    # lossless first tuple difference and zero sparse scan.
    nonuniform_trace: dict[str, int] = {}
    nonuniform_preflight = copy.deepcopy(preflight)
    nonuniform_preflight["all_equal_to_frozen_tuple"] = False
    nonuniform_preflight["first_difference"] = {
        "candidate_index": 2,
        "candidate_tuple_hex": source_hex[:-1] +
            [element_blob(g).hex()],
        "frozen_tuple_hex": source_hex}
    nonuniform = nonpositive_base(
        "B345_RELFRAT3_WORDEXPR_SEARCH_INCOMPLETE",
        "fixed_inverse_not_uniform")
    nonuniform["source_tuple_preflight"] = nonuniform_preflight
    nonuniform["scan"] = {
        "evaluated": 0, "complete": False,
        "first_differing_index": 2,
        "evaluated_prefix_sha256":
            nonuniform_preflight["tuple_ledger_sha256"],
        "source_tuple_preflight_only": True}
    nonuniform_context = dict(context)
    nonuniform_context.update({
        "trace": nonuniform_trace, "preflight": nonuniform_preflight,
        "scan_setup": {**scan_setup, "trace": nonuniform_trace},
        "selected_setup": {**selected_setup, "trace": nonuniform_trace}})
    validate_v8_receipt(
        nonuniform, injected_q3(nonuniform_context, nonuniform_trace),
        Path("."), repo, sealed_selftest=True)

    # SEARCH_INCOMPLETE reason 2: production packed scan decoder and replay
    # exhaust all 4096 registered entries with a cheap quotient failure.
    def exhaustion_builder(index: int, correction: Sequence[int],
                           invs: Sequence[Sequence[int]]) -> dict[str, Any]:
        require(1 <= index <= 4096 and list(correction) == [] and
                len(invs) == 6, "v8 exhaustion provider")
        dag = CheckWordExpr(); one = dag.identity(6); x = dag.flat([1], 6)
        acceptance = []
        for ordinal, name in enumerate(acceptance_names, 1):
            kind = ("charming" if ordinal <= 5 else
                    "hexagon" if ordinal <= 15 else
                    "pentagon" if ordinal == 16 else
                    "endomorphism_relation" if ordinal <= 27 else
                    "onto_two_sided_inverse")
            acceptance.append((name, kind, x if ordinal == 1 else one))
        return {
            "correction_index": index, "correction_word": [],
            "candidate_word": [], "candidate_exponent_sums": [0, 0],
            "dag": dag, "source_roots": [one]*6,
            "inverse_roots": [one]*6,
            "correction_coface_roots": [
                (f"correction_coarse_J_H_coface_{slot}", one)
                for slot in range(5)],
            "acceptance": acceptance,
            "diagnostics": [(name, "diagnostic", x)
                            for name in diagnostic_names],
            "charming_witness": {
                "g_equals_f": True,
                "f_times_g_inverse_is_identity": True,
                "error_gradient_zero": True,
                "free_group_fact": "ker(F2->Z^2)=[F2,F2]"}}

    exhaustion_compiled = exhaustion_builder(1, [], inverse_words)
    exhaustion_eval = CheckWordExprEvaluator(
        exhaustion_compiled["dag"], quotient)
    exhaustion_eval.evaluate_values()
    exhaustion_diag = check_expr_diagnostics(
        exhaustion_compiled, exhaustion_eval)
    exhaustion_roots = [root for _, _, root in
                        exhaustion_compiled["acceptance"]+
                        exhaustion_compiled["diagnostics"]]
    exhaustion_accounting = exhaustion_compiled["dag"].accounting(
        exhaustion_roots)
    zero_blob = element_blob(quotient.identity)
    exhaustion_record = {
        "candidate_index": 0, "outcome": "QUOTIENT_FAILURE",
        "outcome_code": 1,
        "failed_name": "charming_error_coface_0",
        "failed_target_ordinal": 1, "blocker_component": 0,
        "blocker_value_hex": zero_blob.hex(),
        "blocker_value_sha256": hashlib.sha256(zero_blob).hexdigest(),
        "gradient_entry_count": 0,
        "diagnostic_pass_count": sum(
            row["quotient_identity"] for row in exhaustion_diag),
        "diagnostic_values_sha256": digest_obj(exhaustion_diag),
        "wordexpr_sha256": check_expr_digest(exhaustion_compiled["dag"]),
        "wordexpr_nodes": exhaustion_accounting["node_count"],
        "wordexpr_edges": exhaustion_accounting["edge_count"],
        "wordexpr_max_expanded_letters":
            exhaustion_accounting["max_expanded_letter_count"],
        "pool_suffix_removed": 0}
    exhaustion_records = []
    for index in range(1, 4097):
        row = dict(exhaustion_record); row["candidate_index"] = index
        exhaustion_records.append(row)
    exhaustion_arrays = {
        "candidate_index": seal_array(
            "uint32", "I", list(range(1, 4097)),
            CAPS["candidate_scan_records"]),
        "outcome_code": seal_array(
            "uint8", "B", [1]*4096, CAPS["candidate_scan_records"]),
        "failed_target_ordinal": seal_array(
            "uint8", "B", [1]*4096, CAPS["candidate_scan_records"]),
        "blocker_component": seal_array(
            "uint8", "B", [0]*4096, CAPS["candidate_scan_records"]),
        "blocker_value": seal_array(
            "fixed_width_bytes", "B", list(zero_blob*4096),
            CAPS["candidate_scan_records"]*width),
        "diagnostic_pass_count": seal_array(
            "uint8", "B", [exhaustion_record["diagnostic_pass_count"]]*4096,
            CAPS["candidate_scan_records"]),
    }
    exhaustion_manifest = {
        name: {key: value for key, value in row.items() if key != "base64"}
        for name, row in exhaustion_arrays.items()}
    exhaustion_public = [{key: value for key, value in row.items()
                          if key != "blocker_value_hex"}
                         for row in exhaustion_records]
    exhaustion_scan = {
        "format": "registered-wordexpr-scan-arrays/v1", "evaluated": 4096,
        "complete": True, "element_width_bytes": width,
        "outcome_codes": {
            "1": "direct_gate_or_acceptance_quotient_failure",
            "2": "fixed_basis_missing_pivot", "3": "PASS"},
        "arrays": exhaustion_arrays,
        "array_manifest_sha256": digest_obj(exhaustion_manifest),
        "record_bindings": exhaustion_public,
        "record_bindings_sha256": digest_obj(exhaustion_records),
        "evaluated_index_order_sha256": digest_obj(list(range(1, 4097))),
        "failure_distribution": {
            "QUOTIENT_FAILURE:charming_error_coface_0": 4096},
        "registered_corrections": 4096,
        "registered_dictionary_complete": True,
        "full_H3_fibre_complete": False, "full_universe_claimed": False,
        "earliest_global_candidate_claimed": False,
        "negative_completeness_claimed": False,
        "candidate_order": "1..4096 exactly once after saturated v7 prefix",
        "candidate_order_sha256": digest_obj(
            [digest_obj([]) for _ in range(4096)]),
        "candidate_order_equals_frozen_v8": True,
        "acceptance_target_count": 33, "diagnostic_target_count": 17,
        "candidate1_bridge_membership_fused": True,
        "fixed_basis_immutable_during_scan": True,
        "membership_first_pass_allocates_provenance_nodes": False,
        "transaction": {
            "membership_starts": 4096, "membership_rollbacks": 4096,
            "proof_starts": 0, "proof_commits": 0, "proof_rollbacks": 0,
            "failed_candidate_DAG_nodes_allocated": 0,
            "max_pool_suffix": 0, "max_live_gradient_entries": 0},
        "runtime_seconds": 0.0}
    exhaustion = nonpositive_base(
        "B345_RELFRAT3_WORDEXPR_SEARCH_INCOMPLETE",
        "registered_dictionary_exhausted")
    exhaustion["candidate1_flat_bridge"] = bridge
    exhaustion["gradient_memo_performance"] = {
        **memo_summary, "candidate_evaluators": 4096,
        "proof_regeneration_evaluators": 0,
        "candidate_memos_discarded_at_rollback": 4096,
        "candidate1_bridge_pin_stages": 0,
        "ordinary_lazy_pin_stages": 0, "proof_pin_stages": 0,
        "pin_stage_count": 0, "pin_requests_total": 0,
        "peak_retained_pinned_source_count": 0,
        "direct_failures_before_pin": 4096,
        "ordinary_exits_before_target17": 4095}
    exhaustion["wordexpr_scan"] = exhaustion_scan
    exhaustion["search"] = {
        "registered_correction_indices": list(range(1, 4097)),
        "other_corrections_constructed_or_evaluated": 4095,
        "correction_dictionary_constructed": True,
        "complete_source_tuple_DP_executed": True,
        "candidate_membership_tests": 4096,
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
        "selected_candidate_regenerated_and_exactly_compared": False}
    exhaustion["direct_lane"] = {
        "literal_pair_found": False,
        "reason": "all registered corrections failed in the fixed saturated basis",
        "not_nonmembership": True, "not_obstruction": True}
    exhaustion_trace: dict[str, int] = {}
    exhaustion_pool = ReplayPool(quotient)
    exhaustion_context = dict(context)
    exhaustion_context.update({
        "trace": exhaustion_trace,
        "pool": exhaustion_pool, "basis": ReplayBasis(exhaustion_pool, []),
        "scan_setup": {
            "candidate_builder": exhaustion_builder,
            "bridge_validator": bridge_validator,
            "candidate1_expected": {
                key: exhaustion_records[0][key] for key in
                ("outcome", "failed_target_ordinal", "failed_name",
                 "blocker_component", "blocker_value_sha256")},
            "trace": exhaustion_trace},
        "selected_setup": {**selected_setup, "trace": exhaustion_trace}})
    validate_v8_receipt(
        exhaustion, injected_q3(exhaustion_context, exhaustion_trace),
        Path("."), repo, sealed_selftest=True)

    # A bounded RESOURCE prefix and authenticated INPUT stop also use the
    # production envelope/claim validator.  No positive proof fields survive.
    resource = nonpositive_base(
        "B345_RELFRAT3_WORDEXPR_UNKNOWN_RESOURCE",
        "producer_soft_timeout")
    resource["candidate1_flat_bridge"] = bridge
    resource["gradient_memo_performance"] = {
        **memo_summary,
        "candidate_evaluators": 0,
        "proof_regeneration_evaluators": 0,
        "candidate_memos_discarded_at_rollback": 0,
        "candidate1_bridge_pin_stages": 0,
        "ordinary_lazy_pin_stages": 0, "proof_pin_stages": 0,
        "pin_stage_count": 0, "pin_requests_total": 0,
        "peak_retained_pinned_source_count": 0,
        "direct_failures_before_pin": 0,
        "ordinary_exits_before_target17": 0,
        "partial_resource_stop": True}
    resource["wordexpr_scan"] = {
        "format": "registered-wordexpr-scan-arrays/v1", "evaluated": 0,
        "complete": False, "registered_corrections": 4096,
        "registered_dictionary_complete": True,
        "partial_resource_stop": True,
        "current": {"candidate_index": 1, "target_ordinal": 0,
                    "target_name": None},
        "no_candidate_skip_interpreted_as_failure": True,
        "transaction": {
            "membership_starts": 1, "membership_rollbacks": 0,
            "proof_starts": 0, "proof_commits": 0, "proof_rollbacks": 0,
            "failed_candidate_DAG_nodes_allocated": 0,
            "max_pool_suffix": 0, "max_live_gradient_entries": 0}}
    resource["resource_stop"] = {
        "cap": "producer_soft_timeout",
        "no_mathematical_obstruction_claimed": True}
    resource_trace: dict[str, int] = {}
    resource_context = dict(context)
    resource_context.update({
        "trace": resource_trace,
        "scan_setup": {**scan_setup, "trace": resource_trace},
        "selected_setup": {**selected_setup, "trace": resource_trace}})
    validate_v8_receipt(
        resource, injected_q3(resource_context, resource_trace),
        Path("."), repo, sealed_selftest=True)

    input_stop = nonpositive_base(
        "B345_RELFRAT3_WORDEXPR_UNKNOWN_INPUT",
        "authenticated_input_pin_mismatch")
    input_stop["input_errors"] = [{
        "label": "sealed external pin", "expected_sha256": "0"*64,
        "got": "MISSING"}]
    validate_v8_receipt(input_stop, toy_q3, Path("."), repo,
                        sealed_selftest=True)
    hard = copy.deepcopy(common)
    hard["status"] = hard["terminal_token"] = "UNSUPPORTED_HARD_FAIL_TOKEN"
    expect_reject(lambda: validate_v8_receipt(
        hard, toy_q3, Path("."), repo, sealed_selftest=True),
        "unsupported hard-fail terminal")

    # Product/inverse/substitution and negative-prefix orientation are checked
    # independently against direct flattened Fox below the flat cap.
    orientation_compiled = toy_builder(2, [], inverse_words)
    orientation_dag = orientation_compiled["dag"]
    orientation_root = orientation_compiled["orientation_root"]
    orientation_eval = CheckWordExprEvaluator(orientation_dag, quotient)
    orientation_eval.evaluate_values()
    orientation_gradient = orientation_eval.gradients(
        [orientation_root])[orientation_root]
    flat_orientation = orientation_dag.expand_reduced(orientation_root)
    direct_gradient, direct_value = fox(flat_orientation, quotient)
    require(orientation_gradient == direct_gradient and
            orientation_eval.values[orientation_root-1] == direct_value,
            "v8 shared-core orientation direct differential")
    alias_compiled = toy_builder(1, [], inverse_words)
    alias_eval = CheckWordExprEvaluator(alias_compiled["dag"], quotient)
    alias_eval.evaluate_values()
    identity_root = alias_compiled["acceptance"][0][2]
    cube_root = alias_compiled["acceptance"][5][2]
    alias_gradients = alias_eval.gradients([identity_root, cube_root])
    require(alias_eval.values[identity_root-1] ==
                alias_eval.values[cube_root-1] == quotient.identity and
            alias_gradients[identity_root] != alias_gradients[cube_root] and
            identity_root != cube_root,
            "v9 equal-value/different-expression Fox nonalias")
    long_dag = CheckWordExpr(); current = long_dag.flat([1], 6)
    one = long_dag.identity(6)
    for _ in range(18):
        current = long_dag.substitution(
            [1, 1], [current, one, one, one, one, one])
    long_eval = CheckWordExprEvaluator(long_dag, quotient)
    long_eval.evaluate_values()
    require(long_dag.counts[current-1] == 262144 and
            isinstance(long_eval.gradients([current])[current], dict),
            "v8 shared-core long unflattened expression")

    print("D972_B345_RELFRAT3_WORDEXPR_MEMO_V10_CHECKER_SELFTEST_PASS "
          f"envelope_entries={trace['envelope_validator_entries']} "
          f"source_preflight_entries={trace['source_preflight_validator_entries']} "
          f"scan_entries={trace['scan_validator_entries']} "
          f"selected_entries={trace['selected_validator_entries']} "
          f"proof_entries={trace['proof_validator_entries']} "
          f"positive_mutations_shared_core={shared_positive_mutations} "
          "product=1 inverse=1 substitution=1 negative_prefix=1 "
          "memo_forged_key=1 cross_candidate_binding=1 equal_value_nonalias=1 "
          "long_unflattened=262144 source_tuples=4096 rollback_ID_reuse=1 "
          "source_anchors=6 probe_rollback=1 acceptance=33 diagnostics=17 "
          "mutations=17 terminal_fixtures=5")


###############################################################################
# 157eb independent checker: 104-seed affine receipt.
###############################################################################

AFFINE_SCHEMA = "d972-b345-seedspan-affine/v1"
AFFINE_OUTPUT_PATH = Path("ci/out/d972_b345_seedspan_affine_v1.json")
AFFINE_TASK_SHA = "d38a8a7647cca720f73650c616803b1d8d499338783e2c4ebe20fed3b91035f2"
AFFINE_SEED_SHA = "e99602b0981251e4bb81ab0d2113791563bc9ec9df2a45828aea2880ec6d2f9e"
AFFINE_STRONG_SOURCE = Path("search/d972_b345_strong_wform_inertness_v1.py")
AFFINE_STRONG_SHA = "d41123a8c4803f6ac67387ac9bbf1a32f797b90d6233605a5511713f215244be"
AFFINE_TERMINALS = {
    "B345_SEEDSPAN_AFFINE_POSITIVE",
    "B345_SEEDSPAN_AFFINE_SEARCH_INCOMPLETE",
    "B345_SEEDSPAN_AFFINE_UNKNOWN_RESOURCE",
    "B345_SEEDSPAN_AFFINE_UNKNOWN_INPUT",
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
    "seed_count": 104, "cube_count": 26,
    "bfs_translations": 32768, "directed_translations": 207,
    "prefix_columns": 362725, "prefix_pivots": 362709,
    "affine_variables": 104, "affine_rows": 1_000_000,
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
# Keep the inherited monitor's global literal synchronized with this lane's
# registered 300-minute budget; checker deadline/resource receipts use the
# same value as the producer.
CAPS["producer_soft_timeout_seconds"] = AFFINE_CAPS["producer_soft_timeout_seconds"]

AFFINE_V9_PRODUCER_SHA = (
    "7dede323c3c52bc7cf7d99af6d542b3683823879a4bb3e340aca8ce53dcf196f")
AFFINE_EXPECTED_PINS = {
    "formula_sha256": FORMULA_SHA,
    "task_sha256": AFFINE_TASK_SHA,
    "q3_producer": {"path": Q3_PRODUCER.as_posix(),
                     "sha256": Q3_PRODUCER_SHA},
    "q3_checker": {"path": Q3_CHECKER.as_posix(),
                    "sha256": Q3_CHECKER_SHA},
    "q3_driver": {"path": Q3_DRIVER.as_posix(),
                   "sha256": Q3_DRIVER_SHA},
    "q3_artifact": {"path": Q3_ARTIFACT_PATH.as_posix(),
                     "sha256": Q3_ARTIFACT_SHA},
    "v9_producer": {"path": V9_PRODUCER.as_posix(),
                     "sha256": AFFINE_V9_PRODUCER_SHA},
    "strong_prefix_source": {"path": AFFINE_STRONG_SOURCE.as_posix(),
                              "sha256": AFFINE_STRONG_SHA},
}

AFFINE_ALLOWED_TOP_LEVEL = {
    "schema", "status", "terminal_token", "reason", "pins",
    "source_hashes", "input_q3_terminal", "output_path", "fixed_roof",
    "prefix_bindings", "caps", "caps_binding", "registered_universe",
    "claim_boundary", "affine_system", "targets", "diagnostics",
    "seed_family", "normalized_inverse_fibre", "occurrence_preflight",
    "prefix_accounting", "strong_canary", "typed_positive_candidate",
    "resource_guards", "performance", "base_q3_replay",
    "directed_base_support", "directed_surgery", "prefix_rebuild",
    "prefix_basis_gate", "target6_formula_checks",
    "target6_base_gradient_sha256", "positive_replay", "input_errors",
    "partial", "core_validation",
}


def checker_resource_cap_limit(reason: str) -> int:
    if reason == "producer_soft_timeout":
        return int(AFFINE_CAPS["producer_soft_timeout_seconds"])
    if reason == "producer_soft_rss":
        return int(AFFINE_CAPS["producer_soft_rss_bytes"])
    return int(AFFINE_CAPS.get(reason, CAPS.get(reason, 0)))


def checker_resource_observation_valid(partial: dict[str, Any]) -> bool:
    """Validate the measured value using the producer's exact comparator."""
    relation = partial.get("trigger_relation")
    observed = partial.get("observed_count")
    limit = partial.get("cap_limit")
    if relation == "gt":
        return isinstance(observed, int) and observed > limit
    if relation == "ge":
        return isinstance(observed, int) and observed >= limit
    return False


def checker_resource_partial_state(partial: dict[str, Any]) -> None:
    """Check progress coordinates carried by a partial resource receipt."""
    phase = partial["phase"]
    target = partial["current_target_ordinal"]
    seed = partial["current_seed_index"]
    if phase == "authenticated_input":
        require(target == 0 and seed == 0,
                "authenticated-input resource progress")
    elif phase == "fresh_immutable_prefix":
        require(target == 0 and seed == 0,
                "prefix resource progress")
    elif phase == "affine_source_preflight":
        require(target == 0 and 1 <= seed <= AFFINE_CAPS["seed_count"],
                "source-preflight resource seed progress")
    elif phase == "positive_typed_replay_setup":
        require(target == 0 and seed == 0,
                "positive-replay setup resource progress")
    elif phase.startswith("affine_target_"):
        require(target >= 1 and target <= 33 and
                phase == f"affine_target_{target}" and
                0 <= seed <= AFFINE_CAPS["seed_count"],
                "target resource progress")
    elif phase == "positive_typed_replay_diagnostics":
        require(1 <= target <= 17 and 0 <= seed <= AFFINE_CAPS["seed_count"],
                "positive-replay diagnostic progress")
    elif phase == "positive_typed_replay":
        require(1 <= target <= 33 and 0 <= seed <= AFFINE_CAPS["seed_count"],
                "positive-replay resource progress")
    else:
        raise Reject("unknown resource progress phase")


def checker_context_registry(e4: Quotient) -> tuple[list[tuple[Element, Element]], dict[str, Any]]:
    contexts: list[tuple[Element, Element]] = []
    exact: dict[tuple[Element, Element], int] = {}
    named: list[dict[str, Any]] = []

    def add(name: str, left: Element, right: Element) -> None:
        pair = (left, right); ident = exact.get(pair)
        if ident is None:
            ident = len(contexts)+1; exact[pair] = ident; contexts.append(pair)
        named.append({"name": name, "context_id": ident})

    for slot, mapping in enumerate(cofaces(3)):
        x, y = e4.eval(mapping[0]), e4.eval(mapping[2])
        z = e4.inverse(q_paper_product(e4, [x, y]))
        u = e4.inverse(q_paper_product(e4, [y, x]))
        add(f"correction_coface_{slot}", x, y)
        add(f"hexagon_1_fxy_{slot}", x, y)
        add(f"hexagon_1_fxz_{slot}", x, z)
        add(f"hexagon_1_fyz_{slot}", y, z)
        add(f"hexagon_2_fux_{slot}", u, x)
        add(f"hexagon_2_fxy_{slot}", x, y)
        add(f"hexagon_2_fuy_{slot}", u, y)
    g = e4.generators
    pent = [(g[0], g[3]), (g[3], g[5]),
            (q_paper_product(e4, [g[1], g[3]]), g[5]),
            (q_paper_product(e4, [g[0], g[1]]),
             q_paper_product(e4, [g[4], g[5]])),
            (g[0], q_paper_product(e4, [g[3], g[4]]))]
    for i, pair in enumerate(pent): add(f"pentagon_part_{i}", *pair)
    source = [("source_ff", g[0], g[3]), ("source_g", g[0], g[1]),
              ("source_gs", g[3], g[4]),
              ("source_f1234", q_product(e4, [g[3], g[1]]), g[5]),
              ("source_h", q_product(e4, [g[1], g[0]]), g[2]),
              ("source_middle", q_product(e4, [g[1], g[0]]),
               q_product(e4, [g[5], g[4]]))]
    for name, left, right in source: add(name, left, right)
    require(len(contexts) <= 64 and len(named) == 46,
            "checker context registry cap")
    rows = [{"context_id": i+1, "left_hex": element_blob(pair[0]).hex(),
             "right_hex": element_blob(pair[1]).hex()}
            for i, pair in enumerate(contexts)]
    public = {"context_count": len(contexts), "contexts": rows,
              "named_uses": named, "named_use_count": len(named),
              "named_use_mapping_sha256": digest_obj(named),
              "context_rows_sha256": digest_obj(rows),
              "deduplication": "exact E4 pair equality"}
    return contexts, public


def checker_rebuild_occurrence_preflight(
        seeds: Sequence[Sequence[int]], e4: Quotient,
        frozen: tuple[Element, ...]) -> dict[str, Any]:
    contexts, context_public = checker_context_registry(e4)
    records: list[dict[str, Any]] = []
    for index, seed in enumerate(seeds, 1):
        candidate = reduce_word(FIXED_WORD+list(seed))
        source_values = tuple(e4.eval(word) for word in source_words(candidate))
        if source_values != frozen:
            return {"supported": False,
                    "reason": "affine_seed_preflight_unsupported",
                    "first_seed": index, "context": "source_tuple",
                    "value_sha256": digest_obj([
                        element_blob(value).hex() for value in source_values]),
                    "records": records}
        context_rows: list[int] = []
        for context_id, context in enumerate(contexts, 1):
            if ((index-1)*len(contexts) + context_id) & 255 == 0:
                checker_deadline("affine source preflight", force=True)
            value = e4.eval(seed, list(context))
            if value != e4.identity:
                return {"supported": False,
                        "reason": "affine_seed_preflight_unsupported",
                        "first_seed": index, "context_id": context_id,
                        "value_sha256": hashlib.sha256(
                            element_blob(value)).hexdigest(),
                        "records": records}
            context_rows.append(context_id)
        records.append({"seed_index": index, "source_tuple_equal": True,
                        "correction_context_count": len(context_rows),
                        "correction_contexts_sha256": digest_obj(context_rows),
                        "named_use_count": context_public["named_use_count"]})
    return {"supported": True, "seed_count": len(seeds),
            "contexts_per_seed": len(contexts),
            "named_use_count": context_public["named_use_count"],
            "context_registry": context_public, "records": records,
            "source_contexts": ["source_1", "source_2", "source_3",
                                "source_4", "source_5", "source_6"],
            "all_source_tuples_equal": True,
            "all_correction_occurrences_identity": True}


def affine_checker_seed_words(q3: dict[str, Any], e3: Quotient) -> dict[str, Any]:
    cubes: list[list[int]] = []
    seen_cubes: set[tuple[int, ...]] = set()
    for row in q3["correction_fibre"]["records"]:
        if not row["word"]:
            continue
        cube = reduce_word(list(row["word"])*3)
        if tuple(cube) not in seen_cubes:
            seen_cubes.add(tuple(cube)); cubes.append(cube)
    require(len(cubes) == 26, "checker affine cube count")
    seeds: list[list[int]] = []
    seen: set[tuple[int, ...]] = set()
    for cube in cubes:
        require(e3.eval(embed_f2(cube)) == e3.identity,
                "checker affine cube identity")
        for word in (commutator(cube, [1]), commutator([1], cube),
                     commutator(cube, [2]), commutator([2], cube)):
            word = reduce_word(word)
            require(word and exponent_sums(word, 2) == [0, 0] and
                    e3.eval(embed_f2(word)) == e3.identity and
                    tuple(word) not in seen, "checker affine seed typing/order")
            seen.add(tuple(word)); seeds.append(word)
    require(len(seeds) == 104 and digest_obj(seeds) == AFFINE_SEED_SHA,
            "checker affine seed digest")
    return {"cube_words": cubes, "seed_words": seeds,
            "cube_count": 26, "seed_count": 104,
            "digest_obj_sha256": digest_obj(seeds),
            "order": "cube first occurrence; [k,x],[x,k],[k,y],[y,k]",
            "commutator": "[a,b]=a^-1*b^-1*a*b",
            "literal_threefold_cube": True,
            "all_E3_identity": True,
            "all_exponent_sums_zero": True,
            "registered_BFS_not_constructed": True}


class CheckerAffineSystem:
    def __init__(self, variables: int) -> None:
        self.variables = variables; self.rows: dict[int, tuple[dict[int, int], int]] = {}
        self.equations = 0; self.consistent = True

    def add(self, coefficients: dict[int, int], rhs: int) -> bool:
        row = {int(k): int(v) % 3 for k, v in coefficients.items()
               if int(v) % 3}; value = int(rhs) % 3; self.equations += 1
        if self.equations > AFFINE_CAPS["affine_rows"]:
            raise ResourceStop("affine_rows", cap_key="affine_rows",
                               cap_limit=AFFINE_CAPS["affine_rows"],
                               observed_count=self.equations,
                               trigger_relation="gt")
        require(all(0 <= k < self.variables for k in row),
                "checker affine coordinate range")
        while row:
            pivot = min(row); old = self.rows.get(pivot)
            if old is None:
                factor = 1 if row[pivot] == 1 else 2
                self.rows[pivot] = ({k: (factor*v) % 3 for k, v in row.items()
                                     if (factor*v) % 3}, (factor*value) % 3)
                return True
            coefficient = row[pivot]; basis, basis_rhs = old
            for key, term in basis.items():
                result = (row.get(key, 0)-coefficient*term) % 3
                if result: row[key] = result
                else: row.pop(key, None)
            value = (value-coefficient*basis_rhs) % 3
        if value: self.consistent = False
        return not value

    def digest(self) -> str:
        return digest_obj({"variables": self.variables,
                           "rows": [[p, sorted(row.items()), rhs]
                                    for p, (row, rhs) in sorted(self.rows.items())],
                           "equations": self.equations,
                           "consistent": self.consistent})

    def rank(self) -> int:
        return len(self.rows)

    def nullity(self) -> int:
        return self.variables-self.rank()

    def canonical_solution(self) -> list[int]:
        require(self.consistent, "checker solution of inconsistent affine system")
        answer = [0]*self.variables
        for pivot in sorted(self.rows, reverse=True):
            row, rhs = self.rows[pivot]
            answer[pivot] = (rhs-sum(coef*answer[key]
                                     for key, coef in row.items()
                                     if key != pivot)) % 3
        return answer


def checker_basis_gate(pool: ReplayPool, basis: ReplayBasis) -> dict[str, Any]:
    pivots = []
    for pivot, row in basis.rows.items():
        require(row and pivot == min(row, key=pool.pivot_order) and
                row.get(pivot) == 1 and
                all(pool.pivot_order(key) >= pool.pivot_order(pivot)
                    for key in row), "checker immutable prefix pivot gate")
        pivots.append(pivot)
    require(len(pivots) == len(set(pivots)), "checker unique pivots")
    return {"rows": len(pivots), "pivots": len(pivots),
            "least_pivot_coeff_one": True, "no_preceding_keys": True,
            "immutable_during_affine_probes": True,
            "pivot_order": "component then exact E4 bytes"}


def checker_full_remainder(vector: dict[int, int], basis: ReplayBasis,
                           pool: ReplayPool) -> dict[tuple[int, str], int]:
    work = dict(vector); remainder: dict[int, int] = {}
    eliminations = 0
    while work:
        eliminations += 1
        require(len(work)+len(remainder) <=
                CAPS["target_elimination_support"],
                "checker target elimination support cap")
        if eliminations % 1024 == 0:
            checker_deadline("checker full remainder", force=True)
        pivot = min(work, key=pool.pivot_order); coefficient = work.pop(pivot)
        row = basis.rows.get(pivot)
        if row is None:
            remainder[pivot] = coefficient; continue
        # The popped pivot must not be reintroduced by a normalized basis
        # row that contains its own pivot coordinate.  Put it back for the
        # cancellation, then let the row operation remove it exactly.
        work[pivot] = coefficient
        replay_add_scaled(work, row, -coefficient)
    return {(replay_unpack_key(key)[0],
             pool.values[replay_unpack_key(key)[1]].hex()): coefficient
            for key, coefficient in remainder.items() if coefficient % 3}


def checker_probe_remainder(gradient: Vector, pool: ReplayPool,
                            basis: ReplayBasis) -> dict[tuple[int, str], int]:
    checkpoint = pool.checkpoint()
    try:
        packed = pack_check_gradient(gradient, pool)
        return checker_full_remainder(packed, basis, pool)
    finally:
        pool.rollback(checkpoint)


def checker_delta_matrix_rank(delta_rows: dict[Any, dict[int, int]],
                              variables: int = 104) -> int:
    """Independent rank of the current target's 104-column delta map."""
    pivots: dict[int, dict[int, int]] = {}
    for coordinate in sorted(delta_rows, key=repr):
        row = {int(index): int(value) % 3
               for index, value in delta_rows[coordinate].items()
               if int(value) % 3}
        require(all(0 <= index < variables for index in row),
                "checker delta coordinate range")
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


def checker_target_row_transposed(
        system: CheckerAffineSystem,
        base_remainder: dict[tuple[int, str], int],
        delta_rows: dict[tuple[int, str], dict[int, int]],
        target_ordinal: int, live_remainder_entries: int) -> dict[str, Any]:
    require(live_remainder_entries <= AFFINE_CAPS["target_live_remainders"],
            "checker target live remainder cap")
    coordinates = sorted(set(base_remainder).union(delta_rows))
    require(system.equations + len(coordinates) <= AFFINE_CAPS["affine_rows"],
            "checker affine row cap preflight")
    before = system.rank()
    for row_index, coordinate in enumerate(coordinates, 1):
        if row_index & 1023 == 0:
            checker_deadline("affine transposed row absorption", force=True)
        coefficients = {index: value for index, value in
                        delta_rows.get(coordinate, {}).items() if value % 3}
        system.add(coefficients, -base_remainder.get(coordinate, 0))
    return {"ordinal": target_ordinal,
            "base_remainder_size": len(base_remainder),
            "base_remainder_sha256": digest_obj(sorted(base_remainder.items())),
            "coordinate_count": len(coordinates),
            "delta_rank": checker_delta_matrix_rank(delta_rows),
            "constraint_rank_gain": system.rank()-before,
            "constraint_rank": system.rank(),
            "nullity": 104-system.rank(),
            "consistent": system.consistent,
            "row_space_sha256": system.digest(),
            "live_remainder_entries": live_remainder_entries,
            "affine_equations": system.equations}


def checker_raw_model_direct_gate(predicted: Any, direct: Any,
                                  label: str) -> None:
    """Shared raw-C1 model/direct equality gate.

    The producer may use a direct target-specific formula, but the checker
    always compares its result with an independently replayed raw Fox value
    at this boundary.  Keeping this as a small common gate also lets the
    bounded self-test inject a tiny quotient without replacing the gate.
    """
    require(predicted == direct, f"{label}: raw model/direct mismatch")


def checker_target6_formula(seed: Sequence[int], e4: Quotient,
                            *, include_gradient: bool = False) -> Any:
    mapping = cofaces(3)[0]; z = inv_word(pp([[1], [2]]))
    lift = lambda word: substitute(embed_f2(word), mapping)
    a, b, c = (lift(f2_sub(seed, [1], [2])),
               lift(f2_sub(seed, [1], z)), lift(f2_sub(seed, [2], z)))
    r0 = lift(hexagon_words(FIXED_WORD)[0])
    rs = lift(hexagon_words(reduce_word(FIXED_WORD+list(seed)))[0])
    direct, value = fox(reduce_word(rs+inv_word(r0)), e4)
    fixed_c = lift(f2_sub(FIXED_WORD, [2], z))
    ga, va = fox(a, e4); gb, vb = fox(b, e4); gc, vc = fox(c, e4)
    h = e4.eval(r0); cv = e4.eval(fixed_c)
    lhs_word = reduce_word(rs + inv_word(r0))
    rhs_word = reduce_word(
        fixed_c + c + inv_word(b) + inv_word(fixed_c) +
        r0 + a + inv_word(r0))
    require(lhs_word == rhs_word,
            "checker target6 free-word difference identity")
    require(value == e4.identity and va == vb == vc == e4.identity and
            h == e4.identity and e4.eval(rs) == e4.identity,
            "checker target6 quotient formula gate")
    formula: Vector = {}
    add_scaled(formula, translate(gc, cv, e4), 1)
    add_scaled(formula, translate(gb, cv, e4), -1)
    add_scaled(formula, translate(ga, h, e4), 1)
    checker_raw_model_direct_gate(formula, direct, "checker target6")
    if include_gradient:
        return {"formula_equals_direct": True,
                "direct_gradient": direct, "direct_value": value,
                "free_word_lhs_sha256": digest_obj(lhs_word),
                "free_word_rhs_sha256": digest_obj(rhs_word)}
    return True


def checker_target6_public_from_detail(seed: Sequence[int], detail: dict[str, Any]) \
        -> dict[str, Any]:
    binding = check_gradient_binding("target6", "hexagon",
                                     detail["direct_gradient"],
                                     detail["direct_value"])
    return {"seed_word_sha256": digest_obj(seed),
            "left_translation": True,
            "formula": "L_C([c]-[b])+L_h1[a]",
            "product_order": "h1=C*B^-1*A",
            "free_word_identity": True,
            "free_word_lhs_sha256": detail["free_word_lhs_sha256"],
            "free_word_rhs_sha256": detail["free_word_rhs_sha256"],
            "direct_gradient_sha256": digest_obj(binding),
            "formula_equals_direct": detail["formula_equals_direct"]}


def checker_target6_public(seed: Sequence[int], e4: Quotient) -> dict[str, Any]:
    return checker_target6_public_from_detail(
        seed, checker_target6_formula(seed, e4, include_gradient=True))


def checker_strong_canary(e4: Quotient) -> dict[str, Any]:
    """Recompute the 157ea raw-Fox canary; never trust a receipt boolean."""
    strong = reduce_word([-2]*18+[-1]*18+[2]*18+[1]*18)
    rows: list[dict[str, Any]] = []
    for slot, mapping in enumerate(cofaces(3)):
        # The five canary rows are d_j(s) themselves.  The target-6
        # hexagon-difference formula is checked independently below.
        word = substitute(embed_f2(strong), mapping)
        gradient, value = fox(word, e4)
        require(value == e4.identity and not gradient,
                f"checker strong raw-Fox coface {slot}")
        rows.append({"slot": slot, "gradient_zero": True,
                     "value_identity": True,
                     "word_sha256": digest_obj(word)})
    target6 = checker_target6_public(strong, e4)
    require(target6["formula_equals_direct"] is True,
            "checker strong target6 formula/direct")
    return {"word": strong, "cofaces": rows,
            "target6": target6,
            "raw_Fox_zero": True, "replayed_not_imported": True}


def checker_raw_affine_canary(e4: Quotient) -> dict[str, bool]:
    """Independent raw-C1 pair/inverse/square canary."""
    base_word, first, second = [1], [2], [3]
    base, base_value = fox(base_word, e4)
    first_direct, first_value = fox(reduce_word(base_word+first), e4)
    second_direct, second_value = fox(reduce_word(base_word+second), e4)
    require(base_value == first_value == second_value == e4.identity,
            "checker raw affine canary quotient values")
    first_delta = dict(first_direct); add_scaled(first_delta, base, -1)
    second_delta = dict(second_direct); add_scaled(second_delta, base, -1)
    pair_direct, pair_value = fox(reduce_word(base_word+first+second), e4)
    pair_prediction = dict(base)
    add_scaled(pair_prediction, first_delta, 1)
    add_scaled(pair_prediction, second_delta, 1)
    inverse_direct, inverse_value = fox(
        reduce_word(base_word+inv_word(first)), e4)
    inverse_prediction = dict(base)
    add_scaled(inverse_prediction, first_delta, -1)
    square_direct, square_value = fox(
        reduce_word(base_word+first+first), e4)
    square_prediction = dict(base)
    add_scaled(square_prediction, first_delta, 2)
    require(pair_value == inverse_value == square_value == e4.identity and
            pair_direct == pair_prediction and
            inverse_direct == inverse_prediction and
            square_direct == square_prediction,
            "checker raw affine pair/inverse/square canary")
    return {"pair": True, "inverse": True, "square": True,
            "nonzero_base": bool(base), "base_delta_split": True}


def checker_affine_common_envelope(data: dict[str, Any]) \
        -> dict[str, Any] | None:
    """Shared affine receipt envelope/partial-schema validator.

    The full production path performs additional authenticated reconstruction
    below this boundary.  This envelope is deliberately shared with the
    injected bounded fixture, so terminal and claim mutations cannot be
    accepted by a fixture-only shortcut.
    """
    require(set(data) <= AFFINE_ALLOWED_TOP_LEVEL,
            "affine common closed top-level schema")
    require(data.get("schema") == AFFINE_SCHEMA and
            data.get("terminal_token") in AFFINE_TERMINALS and
            data.get("status") == data.get("terminal_token"),
            "affine common schema/terminal")
    token = data["terminal_token"]
    no_claims = {"claim_classification": "unknown_not_obstruction",
                 "claim_scope":
                     "registered_104_seed_affine_span_against_fixed_D2_prefix",
                 "full_D2_claimed": False, "full_H3_claimed": False,
                 "negative_claimed": False, "B4_A_claimed": False,
                 "B4_B_claimed": False}
    positive_claims = {
        "claim_classification": "positive_exact_seedspan_certificate",
        "claim_scope":
            "one_concrete_correction_in_registered_104_seed_subgroup",
        "full_D2_claimed": False, "full_H3_claimed": False,
        "negative_claimed": False, "B4_A_claimed": False,
        "B4_B_claimed": False,
    }
    require(data.get("claim_boundary") ==
            (positive_claims if token ==
             "B345_SEEDSPAN_AFFINE_POSITIVE" else no_claims),
            "affine common claim boundary")
    require(data.get("pins") == AFFINE_EXPECTED_PINS,
            "affine common exact pin binding")
    require(data.get("caps") == AFFINE_CAPS,
            "affine common cap binding")
    require(data.get("caps_binding") == AFFINE_CAPS_BINDING,
            "affine common cap projection binding")
    if token == "B345_SEEDSPAN_AFFINE_UNKNOWN_INPUT":
        errors = data.get("input_errors")
        require(isinstance(errors, dict) and
                isinstance(errors.get("authenticated_external_input"), str) and
                errors.get("mathematical_scan_started") in {False, True},
                "affine common UNKNOWN_INPUT ledger")
        return None
    partial = data.get("partial") if token == \
        "B345_SEEDSPAN_AFFINE_UNKNOWN_RESOURCE" else None
    if token != "B345_SEEDSPAN_AFFINE_UNKNOWN_RESOURCE":
        require("partial" not in data or data.get("partial") is None,
                "affine common unexpected partial")
    if partial is not None:
        require(set(partial) == {
                    "phase", "evaluated_targets",
                    "unevaluated_target_results_are_null", "cap_reason",
                    "current_target_ordinal", "current_seed_index",
                    "live_remainder_entries", "cap_key", "cap_limit",
                    "observed_count", "trigger_relation", "affine_equations"} and
                isinstance(partial["phase"], str) and partial["phase"] and
                isinstance(partial["evaluated_targets"], int) and
                0 <= partial["evaluated_targets"] <= 33 and
                partial["unevaluated_target_results_are_null"] is True and
                isinstance(partial["cap_reason"], str) and
                partial["cap_reason"] in AFFINE_RESOURCE_REASONS and
                partial["cap_key"] == partial["cap_reason"] and
                isinstance(partial["cap_limit"], int) and
                partial["cap_limit"] == checker_resource_cap_limit(
                     partial["cap_reason"]) and
                partial["trigger_relation"] in {"gt", "ge"} and
                checker_resource_observation_valid(partial) and
                isinstance(partial["current_target_ordinal"], int) and
                0 <= partial["current_target_ordinal"] <= 33 and
                isinstance(partial["current_seed_index"], int) and
                0 <= partial["current_seed_index"] <= 104 and
                isinstance(partial["live_remainder_entries"], int) and
                0 <= partial["live_remainder_entries"] <=
                    AFFINE_CAPS["target_live_remainders"] and
                isinstance(partial["affine_equations"], int) and
                 0 <= partial["affine_equations"] <= AFFINE_CAPS["affine_rows"],
                 "affine common partial schema")
        checker_resource_partial_state(partial)
        guards = data.get("resource_guards")
        require(isinstance(guards, dict) and guards.get("hit") is True and
                guards.get("hit_reason") == partial["cap_reason"] and
                guards.get("terminal_on_hit") ==
                    "B345_SEEDSPAN_AFFINE_UNKNOWN_RESOURCE",
                "affine common resource guard binding")
    return partial


def checker_affine_injected_core(data: dict[str, Any],
                                 provider: dict[str, Any],
                                 partial: dict[str, Any] | None) -> None:
    """Run the shared production gates against a bounded injected fixture.

    Only the expensive quotient/prefix construction is injected.  Echelon,
    full remainder, affine elimination, raw model/direct comparison, proof
    topology, and terminal envelope remain the production implementations.
    """
    if data.get("terminal_token") == "B345_SEEDSPAN_AFFINE_UNKNOWN_INPUT":
        checker_affine_unknown_input_gate(
            data, Path("."), Path(__file__).resolve().parents[1])
        return
    checker_affine_metadata_gate(
        data, provider["metadata_q3"], Path(__file__).resolve().parents[1],
        partial)
    if partial is not None:
        require(data.get("core_validation") is None,
                "resource fixture must not promote core block")
        return
    require(data["terminal_token"] == "B345_SEEDSPAN_AFFINE_POSITIVE" and
            set(provider) == {"pool", "basis", "remainder_vector",
                              "affine_variables", "affine_equations",
                              "raw_predicted", "raw_direct", "proof",
                              "proof_names", "proof_vectors", "leaf",
                              "input_gates", "seed_words", "seed_digest",
                              "occurrence_values", "target6_binding",
                              "exponent_two_is_two_copies",
                              "diagnostics_excluded", "base_delta_canary",
                              "context_quotient", "context_public",
                              "context_orientation", "metadata_q3"},
            "affine injected provider contract")
    block = data.get("core_validation")
    require(isinstance(block, dict) and set(block) == {
                "remainder", "echelon", "affine", "raw_model_direct",
                "selected_proof", "input_gates", "seed_binding",
                "occurrence_values", "target6_binding", "acceptance",
                "diagnostics_excluded", "base_delta_canary",
                "context_public", "context_orientation"},
            "affine common core block")
    require(block["input_gates"] == provider["input_gates"] and
            provider["input_gates"] == {
                "f2_to_pb3": {"x": [1], "y": [3]},
                "f2_to_pb4": {"x": [1], "y": [3]}},
            "affine common F2/PB input binding")
    computed_contexts, computed_context_public = checker_context_registry(
        provider["context_quotient"])
    require(computed_context_public == provider["context_public"] and
            block["context_public"] == computed_context_public,
            "affine common context registry binding")
    context_generators = provider["context_quotient"].generators
    ordinary = q_product(provider["context_quotient"],
                         [context_generators[0], context_generators[1]])
    paper = q_paper_product(provider["context_quotient"],
                             [context_generators[0], context_generators[1]])
    expected_orientation = {
        "ordinary": element_blob(ordinary).hex(),
        "paper": element_blob(paper).hex(),
        "different": ordinary != paper,
    }
    require(expected_orientation["different"] is True and
            provider["context_orientation"] == expected_orientation and
            block["context_orientation"] == expected_orientation,
            "affine common context product orientation")
    require(block["seed_binding"] == {
                "words": provider["seed_words"],
                "digest_sha256": provider["seed_digest"],
                "order": "authenticated_small_fixture",
                "exponent_two_is_two_copies":
                    provider["exponent_two_is_two_copies"]} and
            provider["seed_digest"] == digest_obj(provider["seed_words"]),
            "affine common seed binding")
    require(block["occurrence_values"] == provider["occurrence_values"] and
            all(provider["occurrence_values"].values()),
            "affine common occurrence E4 binding")
    require(block["target6_binding"] == provider["target6_binding"] and
            provider["target6_binding"] == {
                "formula": "L_C([c]-[b])+L_h1[a]",
                "product_order": "h1=C*B^-1*A",
                "translation": "left"},
            "affine common target6 orientation binding")
    require(block["acceptance"] == {"count": 33,
                                    "diagnostics_excluded": True} and
            provider["diagnostics_excluded"] is True and
            block["diagnostics_excluded"] is True,
            "affine common acceptance/diagnostic boundary")
    pool = provider["pool"]; basis = provider["basis"]
    gate = checker_basis_gate(pool, basis)
    require(block["echelon"] == gate, "affine common echelon binding")
    remainder = checker_full_remainder(provider["remainder_vector"],
                                       basis, pool)
    remainder_public = sorted([[component, blob, coefficient]
                               for (component, blob), coefficient
                               in remainder.items()])
    require(block["remainder"] == {
                "entries": remainder_public,
                "sha256": digest_obj(remainder_public)},
            "affine common full remainder binding")
    system = CheckerAffineSystem(provider["affine_variables"])
    for coefficients, rhs in provider["affine_equations"]:
        system.add(dict(coefficients), rhs)
    affine_public = {"variables": system.variables, "rank": system.rank(),
                     "nullity": system.nullity(),
                     "consistent": system.consistent,
                     "canonical_solution": system.canonical_solution(),
                     "row_space_sha256": system.digest()}
    require(block["affine"] == affine_public,
            "affine common F3 system binding")
    checker_raw_model_direct_gate(provider["raw_predicted"],
                                  provider["raw_direct"],
                                  "affine common raw model")
    require(block["raw_model_direct"] == {
                "predicted": provider["raw_predicted"],
                "direct": provider["raw_direct"],
                "equal": True}, "affine common raw binding")
    canary = provider["base_delta_canary"]
    combined = dict(canary["base"])
    add_scaled(combined, canary["delta"], 1)
    require(combined == canary["direct"] and canary["base"] != {},
            "affine common nonzero base plus delta canary")
    require(block["base_delta_canary"] == canary,
            "affine common base/delta canary binding")
    selected = block["selected_proof"]
    require(isinstance(selected, dict) and set(selected) == {
                "proof", "names", "root_ids", "vectors"} and
            selected["names"] == provider["proof_names"] and
            selected["proof"] == provider["proof"],
            "affine common selected proof payload")
    leaf = provider["leaf"]

    def leaf_resolver(node: dict[str, Any]) -> Vector:
        require(node == leaf, "affine injected proof leaf binding")
        return {}

    vectors, roots = checker_validate_selected_proof_payload(
        selected["proof"], provider["proof_names"], leaf_resolver,
        provider["proof_vectors"])
    require(selected["root_ids"] == roots and selected["vectors"] == vectors,
            "affine common selected proof result")


def checker_affine_metadata_gate(data: dict[str, Any], q3: dict[str, Any],
                                 repo: Path,
                                 partial: dict[str, Any] | None) -> None:
    """Close the receipt's authenticated and load-bearing metadata surface."""
    require(set(data) <= AFFINE_ALLOWED_TOP_LEVEL,
            "affine closed top-level schema")
    require(data.get("pins") == AFFINE_EXPECTED_PINS,
            "affine exact authenticated pins")
    for key, expected in AFFINE_EXPECTED_PINS.items():
        if key == "q3_artifact" or not isinstance(expected, dict):
            continue
        pinned_path = repo/Path(expected["path"])
        require(pinned_path.is_file() and digest_file(pinned_path) ==
                expected["sha256"],
                f"affine authenticated pin drift: {key}")
    expected_source_hashes = {
        "producer_sha256": digest_file(
            repo/"search/d972_b345_seedspan_affine_solver_v1.py"),
        "checker_sha256": digest_file(Path(__file__).resolve()),
        "driver_sha256": digest_file(
            repo/"search/d972_b345_seedspan_affine_solver_gha_driver_v1.g"),
        "strong_prefix_sha256": digest_file(repo/AFFINE_STRONG_SOURCE),
    }
    require(data.get("source_hashes") == expected_source_hashes,
            "affine source hash receipt binding")
    require(data.get("input_q3_terminal") == q3.get("terminal_token") and
            data.get("output_path") == AFFINE_OUTPUT_PATH.as_posix(),
            "affine q3/output metadata binding")
    selected = q3.get("selected_solution")
    require(isinstance(selected, dict), "affine q3 selected roof metadata")
    expected_roof = {
        "typed_source_word": selected.get("typed_source_word"),
        "exponent": 2, "marking_m": 0, "lambda": 1,
        "outside_by_index_three":
            selected.get("arithmetic_outside_by_index_three"),
    }
    require(data.get("fixed_roof") == expected_roof,
            "affine fixed roof metadata binding")
    require(data.get("prefix_bindings") == AFFINE_PREFIX_BINDINGS,
            "affine prefix metadata binding")
    expected_universe = {
        "kind": "ordered_104_seed_affine_span", "seed_count": 104,
        "cube_count": 26, "BFS_prefix_rebuilt": False,
        "full_D2_claimed": False, "full_H3_claimed": False,
    }
    require(data.get("registered_universe") == expected_universe,
            "affine registered universe metadata binding")
    expected_rebuild = {
        "source": AFFINE_STRONG_SOURCE.as_posix(),
        "source_sha256": AFFINE_STRONG_SHA, "fresh": True,
        "BFS_translations": 32768, "directed_translations": 207,
        "columns": 362725, "pivots": 362709, "dependent_columns": 16,
    }
    expected_basis = {
        "rows": 362709, "pivots": 362709,
        "least_pivot_coeff_one": True, "no_preceding_keys": True,
        "immutable_during_affine_probes": True,
        "pivot_order": "component then exact E4 bytes",
    }
    has_rebuild = "prefix_rebuild" in data or "prefix_basis_gate" in data
    if has_rebuild:
        require(data.get("prefix_rebuild") == expected_rebuild and
                data.get("prefix_basis_gate") == expected_basis and
                "prefix_rebuild" in data and "prefix_basis_gate" in data,
                "affine prefix rebuild/basis metadata binding")
    else:
        early = (partial is not None and partial["phase"] in {
            "authenticated_input", "affine_source_preflight",
            "fresh_immutable_prefix"}) or (
                data["terminal_token"] ==
                "B345_SEEDSPAN_AFFINE_SEARCH_INCOMPLETE" and
                data["reason"] == "affine_seed_preflight_unsupported")
        require(early, "affine missing prefix metadata stage")


def checker_affine_unknown_input_gate(data: dict[str, Any],
                                      q3_path: Path,
                                      repo: Path) -> None:
    """Validate the pre-mathematical UNKNOWN_INPUT envelope fail-closed.

    At this stage q3 may be absent or malformed, so no selected-roof or
    presentation replay is attempted.  The authenticated dependency pins,
    source projection, fixed paths, closed schema, and untouched scan ledgers
    are still mandatory.
    """
    require(set(data) <= AFFINE_ALLOWED_TOP_LEVEL and
            "core_validation" not in data,
            "affine UNKNOWN_INPUT closed top-level schema")
    require(data.get("schema") == AFFINE_SCHEMA and
            data.get("status") == "B345_SEEDSPAN_AFFINE_UNKNOWN_INPUT" and
            data.get("terminal_token") == data.get("status"),
            "affine UNKNOWN_INPUT terminal")
    require(data.get("pins") == AFFINE_EXPECTED_PINS,
            "affine UNKNOWN_INPUT exact pins")
    expected_source_hashes = {
        "producer_sha256": digest_file(
            repo/"search/d972_b345_seedspan_affine_solver_v1.py"),
        "checker_sha256": digest_file(Path(__file__).resolve()),
        "driver_sha256": digest_file(
            repo/"search/d972_b345_seedspan_affine_solver_gha_driver_v1.g"),
        "strong_prefix_sha256": digest_file(repo/AFFINE_STRONG_SOURCE),
    }
    require(data.get("source_hashes") == expected_source_hashes,
            "affine UNKNOWN_INPUT source projection")
    if q3_path.resolve() == (repo/Q3_ARTIFACT_PATH).resolve() and \
            q3_path.is_file():
        require(digest_file(q3_path) == Q3_ARTIFACT_SHA,
                "affine UNKNOWN_INPUT q3 artifact drift")
    require(data.get("input_q3_terminal") is None or
            isinstance(data.get("input_q3_terminal"), str),
            "affine UNKNOWN_INPUT q3 stage field")
    require(data.get("output_path") == AFFINE_OUTPUT_PATH.as_posix() and
            data.get("prefix_bindings") == AFFINE_PREFIX_BINDINGS and
            data.get("caps") == AFFINE_CAPS and
            data.get("caps_binding") == AFFINE_CAPS_BINDING,
            "affine UNKNOWN_INPUT fixed metadata")
    require(data.get("registered_universe") == {
                "kind": "ordered_104_seed_affine_span", "seed_count": 104,
                "cube_count": 26, "BFS_prefix_rebuilt": False,
                "full_D2_claimed": False, "full_H3_claimed": False},
            "affine UNKNOWN_INPUT universe")
    roof = data.get("fixed_roof")
    require(isinstance(roof, dict) and set(roof) == {
                "typed_source_word", "exponent", "marking_m", "lambda",
                "outside_by_index_three"} and
            isinstance(roof["typed_source_word"], list) and
            roof["exponent"] == 2 and roof["marking_m"] == 0 and
            roof["lambda"] == 1 and
            (roof["outside_by_index_three"] is None or
             isinstance(roof["outside_by_index_three"], bool)),
            "affine UNKNOWN_INPUT roof shape")
    for key, expected in {
            "affine_system": None, "targets": [], "diagnostics": [],
            "seed_family": None, "normalized_inverse_fibre": None,
            "occurrence_preflight": None, "prefix_accounting": None,
            "strong_canary": None, "typed_positive_candidate": None,
            "partial": None}.items():
        require(data.get(key) == expected,
                f"affine UNKNOWN_INPUT untouched ledger: {key}")
    errors = data.get("input_errors")
    require(isinstance(errors, dict) and set(errors) == {
                "authenticated_external_input", "mathematical_scan_started"} and
            isinstance(errors["authenticated_external_input"], str) and
            isinstance(errors["mathematical_scan_started"], bool),
            "affine UNKNOWN_INPUT error ledger")
    guards = data.get("resource_guards")
    require(isinstance(guards, dict) and guards.get("hit") is False and
            guards.get("hit_reason") is None,
            "affine UNKNOWN_INPUT resource guard")
    require(isinstance(data.get("performance"), dict) and
            data["performance"].get("phase_complete") in {
                "authenticated_input", "q3_schema_authentication"},
            "affine UNKNOWN_INPUT performance stage")


def checker_affine_validate(data: dict[str, Any], q3: dict[str, Any],
                            q3_path: Path, artifact: Path, repo: Path,
                            *, injected_provider: dict[str, Any] | None = None
                            ) -> None:
    common_partial = checker_affine_common_envelope(data)
    if injected_provider is not None:
        checker_affine_injected_core(data, injected_provider, common_partial)
        return
    require(data.get("schema") == AFFINE_SCHEMA and
            data.get("terminal_token") in AFFINE_TERMINALS and
            data.get("status") == data.get("terminal_token"),
            "affine receipt schema/terminal")
    token = data["terminal_token"]
    claims = data.get("claim_boundary")
    no_claims = {"claim_classification": "unknown_not_obstruction",
                 "claim_scope": "registered_104_seed_affine_span_against_fixed_D2_prefix",
                 "full_D2_claimed": False, "full_H3_claimed": False,
                 "negative_claimed": False, "B4_A_claimed": False,
                 "B4_B_claimed": False}
    positive_claims = {
        "claim_classification": "positive_exact_seedspan_certificate",
        "claim_scope": "one_concrete_correction_in_registered_104_seed_subgroup",
        "full_D2_claimed": False, "full_H3_claimed": False,
        "negative_claimed": False, "B4_A_claimed": False,
        "B4_B_claimed": False,
    }
    require(claims == (positive_claims if
                       token == "B345_SEEDSPAN_AFFINE_POSITIVE" else
                       no_claims), "affine claim boundary")
    if token == "B345_SEEDSPAN_AFFINE_UNKNOWN_INPUT":
        checker_affine_unknown_input_gate(data, q3_path, repo)
        return
    resource_partial = data.get("partial") if token == \
        "B345_SEEDSPAN_AFFINE_UNKNOWN_RESOURCE" else None
    require(q3_path.resolve() == (repo/Q3_ARTIFACT_PATH).resolve() and
            q3_path.is_file() and digest_file(q3_path) == Q3_ARTIFACT_SHA,
            "affine authenticated q3 artifact pin")
    checker_affine_metadata_gate(data, q3, repo, resource_partial)
    if resource_partial is not None:
        require(set(resource_partial) == {
                    "phase", "evaluated_targets",
                    "unevaluated_target_results_are_null", "cap_reason",
                    "current_target_ordinal", "current_seed_index",
                    "live_remainder_entries", "cap_key", "cap_limit",
                    "observed_count", "trigger_relation", "affine_equations"} and
                isinstance(resource_partial["phase"], str) and
                isinstance(resource_partial["evaluated_targets"], int) and
                resource_partial["evaluated_targets"] >= 0 and
                resource_partial["unevaluated_target_results_are_null"] is True and
                isinstance(resource_partial["cap_reason"], str) and
                resource_partial["cap_key"] == resource_partial["cap_reason"] and
                resource_partial["cap_limit"] == checker_resource_cap_limit(
                     resource_partial["cap_reason"]) and
                resource_partial["trigger_relation"] in {"gt", "ge"} and
                checker_resource_observation_valid(resource_partial) and
                isinstance(resource_partial["current_target_ordinal"], int) and
                0 <= resource_partial["current_target_ordinal"] <= 33 and
                isinstance(resource_partial["current_seed_index"], int) and
                0 <= resource_partial["current_seed_index"] <= 104 and
                isinstance(resource_partial["live_remainder_entries"], int) and
                0 <= resource_partial["live_remainder_entries"] <=
                    AFFINE_CAPS["target_live_remainders"] and
                isinstance(resource_partial["affine_equations"], int) and
                 0 <= resource_partial["affine_equations"] <=
                     AFFINE_CAPS["affine_rows"],
                 "affine resource partial ledger")
        checker_resource_partial_state(resource_partial)
        guards = data.get("resource_guards")
        require(isinstance(guards, dict) and guards.get("hit") is True and
                guards.get("hit_reason") == resource_partial["cap_reason"] and
                guards.get("terminal_on_hit") ==
                    "B345_SEEDSPAN_AFFINE_UNKNOWN_RESOURCE",
                "affine resource guard/reason binding")
    require(data["pins"] == AFFINE_EXPECTED_PINS,
            "affine pin receipt")
    require(data.get("caps") == AFFINE_CAPS,
            "affine cap receipt")
    e3, e4 = reconstruct(q3)
    validate_base_replay(data, q3, e3, e4)
    seed_info = affine_checker_seed_words(q3, e3)
    require(data["seed_family"] == seed_info, "independent seed family replay")
    normalized, frozen, inverse_words = rebuild_normalized_inverse_fibre(q3, e4)
    require(data["normalized_inverse_fibre"] == normalized,
            "independent normalized inverse replay")
    contexts, context_public = checker_context_registry(e4)
    require(context_public["named_use_count"] == 46,
            "checker context registry count")
    if resource_partial is not None and data.get("occurrence_preflight") is None:
        if resource_partial["phase"] in {
                "authenticated_input", "affine_source_preflight",
                "fresh_immutable_prefix"}:
            require(resource_partial["evaluated_targets"] == 0 and
                    resource_partial["current_target_ordinal"] == 0 and
                    resource_partial["affine_equations"] == 0,
                    "affine source-preflight resource phase")
        else:
            target_phase = resource_partial["phase"].startswith(
                "affine_target_")
            positive_phase = resource_partial["phase"].startswith(
                "positive_typed_replay")
            require((target_phase or positive_phase) and
                    (not target_phase or
                     resource_partial["evaluated_targets"] ==
                         resource_partial["current_target_ordinal"]-1) and
                    (not positive_phase or
                     resource_partial["evaluated_targets"] == 0) and
                    resource_partial["affine_equations"] == 0,
                    "affine staged resource phase")
        return
    expected_preflight = checker_rebuild_occurrence_preflight(
        seed_info["seed_words"], e4, frozen)
    require(data["occurrence_preflight"] == expected_preflight,
            "affine occurrence preflight independent replay")
    if not expected_preflight["supported"]:
        require(data["terminal_token"] ==
                "B345_SEEDSPAN_AFFINE_SEARCH_INCOMPLETE" and
                data["reason"] == "affine_seed_preflight_unsupported",
                "affine unsupported preflight terminal")
        return
    if resource_partial is not None and data.get("strong_canary") is None:
        require(resource_partial["evaluated_targets"] == 0 and
                data.get("prefix_accounting") is None and
                resource_partial["current_target_ordinal"] == 0,
                "affine pre-prefix resource phase")
        return
    strong = checker_strong_canary(e4)
    require(data["strong_canary"]["raw_Fox_zero"] is True and
            data["strong_canary"]["word"] == strong["word"] and
            data["strong_canary"]["cofaces"] == strong["cofaces"] and
            data["strong_canary"]["target6"] == strong["target6"],
            "affine strong canary receipt/replay")
    # Build the 105 exact target-6 formula rows once.  The same detail ledger
    # supplies the raw delta gradients in the target-major absorption below;
    # this avoids replaying each four-Fox formula twice.
    target6_details: list[dict[str, Any]] = []
    target6_seeds = [[]] + list(seed_info["seed_words"])
    for detail_index, seed in enumerate(target6_seeds):
        if detail_index % 4 == 0:
            checker_deadline("affine target6 formula ledger", force=True)
        target6_details.append(
            checker_target6_formula(seed, e4, include_gradient=True))
    expected_target6_rows: list[dict[str, Any]] = []
    for detail_index, seed in enumerate(target6_seeds):
        if detail_index % 4 == 0:
            checker_deadline("affine target6 row ledger", force=True)
        expected_target6_rows.append(
            checker_target6_public_from_detail(seed,
                                               target6_details[detail_index]))
    actual_target6_rows = data.get("target6_formula_checks")
    if resource_partial is None or resource_partial["evaluated_targets"] >= 6:
        require(actual_target6_rows == expected_target6_rows,
                "affine target6 exact formula ledger")
    elif actual_target6_rows is None:
        require(resource_partial["evaluated_targets"] < 6,
                "affine target6 absent partial ledger")
    else:
        require(isinstance(actual_target6_rows, list) and
                actual_target6_rows == expected_target6_rows[
                    :len(actual_target6_rows)],
                "affine target6 partial formula ledger")
    if resource_partial is not None and data.get("prefix_accounting") is None:
        require(resource_partial["evaluated_targets"] == 0 and
                resource_partial["current_target_ordinal"] == 0,
                "affine prefix-build resource phase")
        return
    r0 = substitute(embed_f2(hexagon_words(FIXED_WORD)[0]), cofaces(3)[0])
    prefix_targets = [(f"charming_error_coface_{i}", "charming", [])
                      for i in range(5)] + [("hexagon_1_coface_0", "hexagon", r0)]
    pool, basis = replay_pivot_surgery(data, e4, prefix_targets, frozen)
    gate = checker_basis_gate(pool, basis)
    require(data.get("prefix_basis_gate") == gate,
            "checker prefix basis gate receipt binding")
    require(gate["rows"] == 362709 and basis.columns_seen == 362725 and
            basis.dependent == 16, "checker prefix counts/gate")
    targets, diagnostics = fixed_target_split(e4, normalized)
    require(len(targets) == 33 and len(diagnostics) == 17,
            "checker target split")
    base_compiled = build_check_wordexpr(0, [], inverse_words)
    base_eval = CheckWordExprEvaluator(base_compiled["dag"], e4)
    base_eval.evaluate_values()
    system = CheckerAffineSystem(104); rows: list[dict[str, Any]] = []
    for ordinal, (name, kind, root) in enumerate(base_compiled["acceptance"], 1):
        if resource_partial is not None and ordinal > \
                resource_partial["evaluated_targets"]:
            break
        if ordinal <= 5:
            require(base_compiled["dag"].op[root-1] == 1 and
                    base_compiled["dag"].rank[root-1] == 6 and
                    base_compiled["dag"].counts[root-1] == 0,
                    f"checker charming identity root {name}")
            zero_binding = digest_obj(check_gradient_binding(
                name, kind, {}, e4.identity))
            split_ledger = [{"seed_index": index,
                             "gradient_sha256": zero_binding,
                             "value_identity": True}
                            for index in range(1, 105)]
            target_row = {"ordinal": ordinal, "name": name, "kind": kind,
                          "base_remainder_size": 0,
                          "base_remainder_sha256": digest_obj([]),
                          "coordinate_count": 0, "delta_rank": 0,
                          "constraint_rank_gain": 0,
                          "constraint_rank": system.rank(),
                          "nullity": 104-system.rank(),
                          "consistent": system.consistent,
                          "row_space_sha256": system.digest(),
                          "live_remainder_entries": 0,
                          "affine_equations": system.equations,
                          "diagnostics_excluded": True, "seed_count": 104,
                          "typed_split_count": 104,
                          "typed_split_sha256": digest_obj(split_ledger),
                          "raw_chain_affine_certificate": {
                              "typed_vs_flat_count": 104,
                              "typed_vs_flat_all_equal": True,
                              "raw_C1_before_D2": True,
                              "opcode_induction":
                                  "FLAT/PRODUCT/INVERSE/SUBSTITUTE",
                              "identity_root_shortcut": True,
                          }}
            rows.append(target_row)
            continue
        require(base_eval.values[root-1] == e4.identity,
                f"checker base target identity {name}")
        if ordinal == 6:
            # The target-6 formula is a delta formula.  Obtain the base
            # gradient from the actual f0 target and retain the empty formula
            # row only as a zero-delta orientation canary.
            base_gradient = base_eval.gradients([root])[root]
            base_formula = target6_details[0]
            empty_delta = base_formula["direct_gradient"]
            require(base_formula["direct_value"] == e4.identity and
                    base_formula["formula_equals_direct"] is True and
                    empty_delta == {},
                    "checker target6 empty delta orientation canary")
            require(data.get("target6_base_gradient_sha256") ==
                    digest_obj(check_gradient_binding(
                        name, kind, base_gradient, e4.identity)),
                    "checker target6 base gradient binding")
        else:
            base_gradient = base_eval.gradients([root])[root]
        base_remainder = checker_probe_remainder(base_gradient, pool, basis)
        delta_rows: dict[tuple[int, str], dict[int, int]] = {}
        live_remainder_entries = len(base_remainder)
        split_ledger: list[dict[str, Any]] = []
        for index, seed in enumerate(seed_info["seed_words"], 1):
            if index & 15 == 0:
                checker_deadline("affine target seed", force=True)
            if ordinal == 6:
                formula_row = target6_details[index]
                delta_gradient = formula_row["direct_gradient"]
                require(formula_row["direct_value"] == e4.identity and
                        formula_row["formula_equals_direct"] is True,
                        f"checker target6 seed formula {index}")
                seed_gradient = dict(base_gradient)
                add_scaled(seed_gradient, delta_gradient, 1)
            else:
                compiled = build_check_wordexpr(index, seed, inverse_words)
                evaluator = CheckWordExprEvaluator(compiled["dag"], e4)
                evaluator.evaluate_values()
                seed_root = compiled["acceptance"][ordinal-1][2]
                require(evaluator.values[seed_root-1] == e4.identity,
                        f"checker seed target identity {name}")
                seed_gradient = evaluator.gradients([seed_root])[seed_root]
                if compiled["dag"].counts[seed_root-1] <= \
                        CAPS["single_word_or_section_length"]:
                    direct, direct_value = fox(
                        compiled["dag"].expand_reduced(seed_root), e4)
                    require(direct == seed_gradient and
                            direct_value == e4.identity,
                            f"checker direct gradient {name}")
                else:
                    # Long typed roots are independently replayed cold; forcing
                    # flat expansion here would change the registered lane.
                    cold_eval = CheckWordExprEvaluator(compiled["dag"], e4)
                    cold_eval.evaluate_values()
                    cold_gradient = cold_eval.gradients([seed_root])[seed_root]
                    require(cold_gradient == seed_gradient and
                            cold_eval.values[seed_root-1] == e4.identity,
                            f"checker typed cold gradient {name}")
            one_coefficients = [0]*len(seed_info["seed_words"])
            one_coefficients[index-1] = 1
            typed_one = checker_make_typed_positive(
                one_coefficients, seed_info["seed_words"])
            typed_one_targets = (checker_build_typed_target6(typed_one)
                                 if ordinal == 6 else
                                 checker_build_typed_targets(
                                     typed_one, inverse_words))
            typed_one_eval = CheckWordExprEvaluator(
                typed_one_targets["dag"], e4)
            typed_one_root = checker_select_typed_target_root(
                typed_one_targets, ordinal)
            typed_one_eval.evaluate_values([typed_one_root])
            typed_raw = typed_one_eval.gradients([typed_one_root])[typed_one_root]
            require(typed_one_eval.values[typed_one_root-1] == e4.identity and
                    typed_raw == seed_gradient,
                    f"checker typed/flat raw chain split {name}/{index}")
            split_ledger.append({
                "seed_index": index,
                "gradient_sha256": digest_obj(check_gradient_binding(
                    name, kind, typed_raw,
                    typed_one_eval.values[typed_one_root-1])),
                "value_identity": True,
            })
            if ordinal == 6:
                delta = delta_gradient
            else:
                delta = dict(seed_gradient)
                add_scaled(delta, base_gradient, -1)
            delta_remainder = checker_probe_remainder(delta, pool, basis)
            require(live_remainder_entries + len(delta_remainder) <=
                    AFFINE_CAPS["target_live_remainders"],
                    "checker target live remainder cap")
            live_remainder_entries += len(delta_remainder)
            for coordinate, coefficient in delta_remainder.items():
                delta_rows.setdefault(coordinate, {})[index-1] = coefficient
        row = checker_target_row_transposed(
            system, base_remainder, delta_rows, ordinal,
            live_remainder_entries)
        row.update({"name": name, "kind": kind,
               "diagnostics_excluded": True, "seed_count": 104,
               "typed_split_count": len(split_ledger),
               "typed_split_sha256": digest_obj(split_ledger),
               "raw_chain_affine_certificate": {
                   "typed_vs_flat_count": len(split_ledger),
                   "typed_vs_flat_all_equal": True,
                   "raw_C1_before_D2": True,
                   "opcode_induction":
                       "FLAT/PRODUCT/INVERSE/SUBSTITUTE",
               }})
        rows.append(row)
        if not system.consistent:
            break
    require(data["targets"] == rows, "checker target-major affine rows")
    if resource_partial is not None:
        # A resource stop during the typed positive replay is not a target
        # prefix stop.  All 33 affine rows and the consistent system have
        # already been completed; only the positive proof replay is partial.
        # Validate that completed prefix independently before inspecting the
        # replay-stage coordinates.
        positive_phase = resource_partial["phase"]
        if positive_phase.startswith("positive_typed_replay"):
            require(resource_partial["evaluated_targets"] == 33 and
                    len(rows) == 33 and system.consistent and
                    resource_partial["affine_equations"] == system.equations and
                    data["reason"] == resource_partial["cap_reason"],
                    "checker positive replay completed affine prefix")
            partial_system = data.get("affine_system")
            canonical = system.canonical_solution()
            require(isinstance(partial_system, dict) and
                    partial_system.get("variables") == 104 and
                    partial_system.get("rank") == system.rank() and
                    partial_system.get("nullity") == 104-system.rank() and
                    partial_system.get("consistent") is True and
                    partial_system.get("row_space_sha256") == system.digest() and
                    partial_system.get("canonical_solution_sha256") ==
                        digest_obj(canonical),
                    "checker positive replay canonical system")
            require(data.get("diagnostics") == [] and
                    data.get("typed_positive_candidate") is None and
                    data.get("positive_replay") is None,
                    "checker positive replay partial proof boundary")
            if positive_phase == "positive_typed_replay_setup":
                require(resource_partial["current_target_ordinal"] == 0 and
                        resource_partial["current_seed_index"] == 0,
                        "checker positive replay setup progress")
            elif positive_phase == "positive_typed_replay":
                require(1 <= resource_partial["current_target_ordinal"] <= 33 and
                        0 <= resource_partial["current_seed_index"] <=
                            AFFINE_CAPS["seed_count"],
                        "checker positive acceptance progress")
            elif positive_phase == "positive_typed_replay_diagnostics":
                require(1 <= resource_partial["current_target_ordinal"] <= 17 and
                        0 <= resource_partial["current_seed_index"] <=
                            AFFINE_CAPS["seed_count"],
                        "checker positive diagnostic progress")
            else:
                raise Reject("checker positive replay phase")
            return
        require(len(rows) == resource_partial["evaluated_targets"] and
                data["reason"] == resource_partial["cap_reason"],
                "checker resource target prefix length/reason")
        require(resource_partial["current_target_ordinal"] in {
                    len(rows), len(rows)+1} and
                resource_partial["affine_equations"] == system.equations,
                "checker resource current target/equation binding")
        if not rows:
            require(data.get("affine_system") is None,
                    "checker pre-target resource affine system")
        else:
            partial_system = data.get("affine_system")
            require(isinstance(partial_system, dict) and
                    partial_system.get("variables") == 104 and
                    partial_system.get("rank") == system.rank() and
                    partial_system.get("nullity") == 104-system.rank() and
                    partial_system.get("consistent") is system.consistent and
                    partial_system.get("row_space_sha256") == system.digest(),
                    "checker partial affine system")
        return
    expected_system = data["affine_system"]
    require(expected_system["variables"] == 104 and
            expected_system["rank"] == system.rank() and
            expected_system["nullity"] == 104-system.rank() and
            expected_system["consistent"] is system.consistent and
            expected_system["row_space_sha256"] == system.digest(),
            "checker affine system binding")
    if data["terminal_token"] == "B345_SEEDSPAN_AFFINE_POSITIVE":
        candidate = data.get("typed_positive_candidate")
        require(isinstance(candidate, dict) and
                candidate.get("coefficient_vector") ==
                    system.canonical_solution() and
                candidate.get("coefficient_vector_sha256",
                              digest_obj(candidate["coefficient_vector"])) ==
                    digest_obj(candidate["coefficient_vector"]),
                "checker positive canonical coefficient vector")
        checker_validate_positive_replay(
            data, candidate["coefficient_vector"],
            seed_info["seed_words"], inverse_words, frozen, e3, e4,
            pool, basis)
    elif data["terminal_token"] == "B345_SEEDSPAN_AFFINE_SEARCH_INCOMPLETE":
        require(data["reason"] in {"affine_seed_preflight_unsupported",
                                    "affine_system_inconsistent"},
                "checker incomplete reason")
        if data["reason"] == "affine_system_inconsistent":
            require(not system.consistent, "checker inconsistency terminal")
    elif data["terminal_token"] == "B345_SEEDSPAN_AFFINE_UNKNOWN_RESOURCE":
        require(isinstance(data.get("partial"), dict),
                "checker resource partial schema")


def affine_checker_self_test() -> None:
    require(AFFINE_CAPS["producer_soft_timeout_seconds"] == 18_000 and
            AFFINE_CAPS["producer_soft_rss_bytes"] == 4_831_838_208,
            "checker affine deadline/RSS binding")
    # This is intentionally a small injected quotient/presentation.  It
    # enters checker_affine_validate through the same envelope and shared
    # gates used by the production artifact; only the expensive q3/prefix
    # construction is replaced by the provider below.
    def packed(type_name: str, typecode: str,
               values: Sequence[int], cap: int) -> dict[str, Any]:
        raw_array = array(typecode, [int(x) for x in values])
        if sys.byteorder != "little":
            raw_array.byteswap()
        raw = raw_array.tobytes()
        return {"type": type_name, "array_typecode": typecode,
                "endianness": "little", "length": len(values),
                "itemsize": raw_array.itemsize, "byte_length": len(raw),
                "cap": cap, "sha256": hashlib.sha256(raw).hexdigest(),
                "base64": base64.b64encode(raw).decode("ascii")}

    collector = Collector({"generator_count": 0, "relative_orders": [],
                           "power_relations": [], "inverses": [],
                           "conjugate_relations": [],
                           "inverse_conjugate_relations": []})
    identity = ((0,), ())
    toy_quotient = Quotient(4, 1, collector, [identity]*6)
    raw_canary = checker_raw_affine_canary(toy_quotient)
    require(raw_canary == {"pair": True, "inverse": True, "square": True,
                           "nonzero_base": True, "base_delta_split": True},
            "checker selftest raw affine canary")
    target6_canary = checker_target6_formula([1, -2], toy_quotient,
                                             include_gradient=True)
    require(target6_canary["formula_equals_direct"] is True and
            target6_canary["direct_value"] == toy_quotient.identity,
            "checker selftest target6 free-word/formula canary")
    target6_dag = CheckWordExpr()
    target6_candidate = target6_dag.flat(FIXED_WORD, 2)
    target6_built = checker_build_typed_target6(
        {"dag": target6_dag, "candidate_root": target6_candidate})
    require(checker_select_typed_target_root(target6_built, 6) ==
            target6_built["acceptance"][0][2],
            "checker selftest target6-only acceptance selection")
    for bad_acceptance, label in [
            ([ ("wrong_name", "hexagon", target6_candidate)], "name"),
            ([ ("hexagon_1_coface_0", "wrong_kind", target6_candidate)],
             "kind"),
            ([ ("hexagon_1_coface_0", "hexagon", target6_candidate),
               ("extra", "hexagon", target6_candidate)], "cardinality")]:
        bad_target6 = dict(target6_built)
        bad_target6["acceptance"] = bad_acceptance
        expect_reject(lambda bad=bad_target6:
                      checker_select_typed_target_root(bad, 6),
                      f"checker target6 selection mutation: {label}")
    context_quotient = Quotient(
        4, 3, collector,
        [((1, 2, 0), collector.identity()),
         ((1, 0, 2), collector.identity()),
         ((0, 1, 2), collector.identity()),
         ((0, 1, 2), collector.identity()),
         ((0, 1, 2), collector.identity()),
         ((0, 1, 2), collector.identity())])
    _, context_public = checker_context_registry(context_quotient)
    context_generators = context_quotient.generators
    context_ordinary = q_product(context_quotient,
                                  [context_generators[0], context_generators[1]])
    context_paper = q_paper_product(context_quotient,
                                    [context_generators[0], context_generators[1]])
    context_orientation = {
        "ordinary": element_blob(context_ordinary).hex(),
        "paper": element_blob(context_paper).hex(),
        "different": context_ordinary != context_paper,
    }
    pool = ReplayPool(toy_quotient)
    key0 = replay_pack_key(1, pool.identity)
    key1 = replay_pack_key(2, pool.identity)
    key2 = replay_pack_key(3, pool.identity)
    basis = ReplayBasis(pool, [{}])
    basis.rows = {key1: {key1: 1, key2: 1}}
    basis.columns_seen = 1
    remainder_vector = {key0: 1, key1: 1, key2: 1}
    gate = checker_basis_gate(pool, basis)
    remainder = checker_full_remainder(remainder_vector, basis, pool)
    remainder_public = sorted([[component, blob, coefficient]
                               for (component, blob), coefficient
                               in remainder.items()])
    affine_equations = [({0: 1, 1: 1}, 1), ({1: 1}, 2)]
    affine_system = CheckerAffineSystem(2)
    for coefficients, rhs in affine_equations:
        affine_system.add(coefficients, rhs)

    section_expressions = {
        "format": "typed-section-expression-arrays/v1",
        "node_order": "zero_based_topological",
        "ordinary_word_composition": True,
        "canonical_value_width": 1, "node_count": 0, "edge_count": 0,
        "roots": [], "arrays": {},
        "manifest_sha256": digest_obj({"arrays": {}, "roots": []}),
    }
    proof_arrays = {
        "node_kind": packed("uint8", "B", [1], CAPS["provenance_dag_nodes"]),
        "leaf_relator_index": packed(
            "uint16", "H", [1], CAPS["provenance_dag_nodes"]),
        "leaf_translation_element_id": packed(
            "uint32", "I", [1], CAPS["provenance_dag_nodes"]),
        "edge_offsets": packed(
            "uint32", "I", [0, 0], CAPS["provenance_dag_nodes"]+1),
        "edge_parent_node_id": packed(
            "uint32", "I", [], CAPS["provenance_dag_edges"]),
        "edge_coefficient": packed(
            "uint8", "B", [], CAPS["provenance_dag_edges"]),
    }
    proof_roots = [{"name": "toy_selected", "node_id": 1}]
    proof_manifest = {
        name: {key: value for key, value in row.items()
               if key != "base64"}
        for name, row in proof_arrays.items()}
    proof = {
        "format": "packed-parallel-arrays/v1", "field": 3,
        "node_order": "one_based_topological",
        "translation_action": "left",
        "section_expressions": section_expressions,
        "arrays": proof_arrays, "roots": proof_roots,
        "node_count": 1, "edge_count": 0, "leaf_count": 1,
        "combination_node_count": 0,
        "all_serialized_nodes_reachable_from_roots": True,
        "unreachable_search_nodes_pruned": 0,
        "expanded_boundary_ledgers_serialized": False,
        "packed_manifest_sha256": digest_obj(
            {"arrays": proof_manifest, "roots": proof_roots}),
    }
    leaf = {"relator_index": 1, "translation_element_id": 1,
            "translation_action": "left"}
    toy_q3 = {
        "terminal_token": "toy_q3",
        "selected_solution": {
            "typed_source_word": [1],
            "arithmetic_outside_by_index_three": True,
        },
    }
    selftest_repo = Path(__file__).resolve().parents[1]
    provider = {
        "pool": pool, "basis": basis,
        "remainder_vector": remainder_vector,
        "affine_variables": 2, "affine_equations": affine_equations,
        "raw_predicted": {"gradient": [[1, 0]]},
        "raw_direct": {"gradient": [[1, 0]]},
        "proof": proof, "proof_names": ["toy_selected"],
        "proof_vectors": {"toy_selected": {}}, "leaf": leaf,
        "input_gates": {"f2_to_pb3": {"x": [1], "y": [3]},
                         "f2_to_pb4": {"x": [1], "y": [3]}},
        "seed_words": [[1, -2], [2, -1]],
        "seed_digest": digest_obj([[1, -2], [2, -1]]),
        "occurrence_values": {"context_1": True, "context_2": True},
        "target6_binding": {
            "formula": "L_C([c]-[b])+L_h1[a]",
            "product_order": "h1=C*B^-1*A", "translation": "left"},
        "exponent_two_is_two_copies": True,
        "diagnostics_excluded": True,
        "base_delta_canary": {"base": {0: 1}, "delta": {0: 2},
                              "direct": {}},
        "context_quotient": context_quotient,
        "context_public": context_public,
        "context_orientation": context_orientation,
        "metadata_q3": toy_q3,
    }
    no_claims = {"claim_classification": "unknown_not_obstruction",
                 "claim_scope":
                     "registered_104_seed_affine_span_against_fixed_D2_prefix",
                 "full_D2_claimed": False, "full_H3_claimed": False,
                 "negative_claimed": False, "B4_A_claimed": False,
                 "B4_B_claimed": False}
    positive_claims = {**no_claims,
                       "claim_classification":
                           "positive_exact_seedspan_certificate",
                       "claim_scope":
                           "one_concrete_correction_in_registered_104_seed_subgroup"}
    metadata_rebuild = {
        "source": AFFINE_STRONG_SOURCE.as_posix(),
        "source_sha256": AFFINE_STRONG_SHA, "fresh": True,
        "BFS_translations": 32768, "directed_translations": 207,
        "columns": 362725, "pivots": 362709, "dependent_columns": 16,
    }
    metadata_basis = {
        "rows": 362709, "pivots": 362709,
        "least_pivot_coeff_one": True, "no_preceding_keys": True,
        "immutable_during_affine_probes": True,
        "pivot_order": "component then exact E4 bytes",
    }
    metadata_universe = {
        "kind": "ordered_104_seed_affine_span", "seed_count": 104,
        "cube_count": 26, "BFS_prefix_rebuilt": False,
        "full_D2_claimed": False, "full_H3_claimed": False,
    }
    metadata_fixed_roof = {
        "typed_source_word": [1], "exponent": 2,
        "marking_m": 0, "lambda": 1,
        "outside_by_index_three": True,
    }
    metadata_source_hashes = {
        "producer_sha256": digest_file(
            selftest_repo/"search/d972_b345_seedspan_affine_solver_v1.py"),
        "checker_sha256": digest_file(Path(__file__).resolve()),
        "driver_sha256": digest_file(
            selftest_repo/"search/d972_b345_seedspan_affine_solver_gha_driver_v1.g"),
        "strong_prefix_sha256": digest_file(
            selftest_repo/AFFINE_STRONG_SOURCE),
    }
    base = {
        "schema": AFFINE_SCHEMA,
        "status": "B345_SEEDSPAN_AFFINE_POSITIVE",
        "terminal_token": "B345_SEEDSPAN_AFFINE_POSITIVE",
        "reason": "selftest_shared_core_control",
        "pins": AFFINE_EXPECTED_PINS,
        "caps": AFFINE_CAPS, "caps_binding": AFFINE_CAPS_BINDING,
        "claim_boundary": positive_claims,
        "source_hashes": metadata_source_hashes,
        "input_q3_terminal": "toy_q3",
        "output_path": AFFINE_OUTPUT_PATH.as_posix(),
        "fixed_roof": metadata_fixed_roof,
        "prefix_bindings": AFFINE_PREFIX_BINDINGS,
        "registered_universe": metadata_universe,
        "prefix_rebuild": metadata_rebuild,
        "prefix_basis_gate": metadata_basis,
    }
    core = {
        "remainder": {"entries": remainder_public,
                       "sha256": digest_obj(remainder_public)},
        "echelon": gate,
        "affine": {"variables": affine_system.variables,
                    "rank": affine_system.rank(),
                    "nullity": affine_system.nullity(),
                    "consistent": affine_system.consistent,
                    "canonical_solution": affine_system.canonical_solution(),
                    "row_space_sha256": affine_system.digest()},
        "raw_model_direct": {"predicted": provider["raw_predicted"],
                              "direct": provider["raw_direct"], "equal": True},
        "selected_proof": {"proof": proof, "names": ["toy_selected"],
                            "root_ids": {"toy_selected": 1},
                            "vectors": {"toy_selected": {}}},
        "input_gates": provider["input_gates"],
        "seed_binding": {"words": provider["seed_words"],
                          "digest_sha256": provider["seed_digest"],
                          "order": "authenticated_small_fixture",
                          "exponent_two_is_two_copies": True},
        "occurrence_values": provider["occurrence_values"],
        "target6_binding": provider["target6_binding"],
        "acceptance": {"count": 33, "diagnostics_excluded": True},
        "diagnostics_excluded": True,
        "base_delta_canary": provider["base_delta_canary"],
        "context_public": context_public,
        "context_orientation": context_orientation,
    }
    control = {**base, "core_validation": core}
    invoke = lambda receipt, dep=provider: checker_affine_validate(
        receipt, toy_q3, Path("."), Path("."), selftest_repo,
        injected_provider=dep)
    invoke(control)

    def reject_receipt(label: str, mutate: Any,
                       dep: dict[str, Any] = provider) -> None:
        bad = copy.deepcopy(control)
        mutate(bad)
        expect_reject(lambda: invoke(bad, dep),
                      f"checker shared-core mutation: {label}")

    reject_receipt("wrong F2-to-PB3 y image",
                   lambda x: x["core_validation"]["input_gates"][
                       "f2_to_pb3"]["y"].__setitem__(0, 2))
    reject_receipt("seed reorder/digest",
                   lambda x: x["core_validation"]["seed_binding"][
                       "words"].reverse())
    reject_receipt("seed sign/duplicate",
                   lambda x: x["core_validation"]["seed_binding"][
                       "words"].__setitem__(1, [1, -2]))
    reject_receipt("nonidentity occurrence context",
                   lambda x: x["core_validation"]["occurrence_values"].
                   __setitem__("context_2", False))
    reject_receipt("C/B inverse/A order",
                   lambda x: x["core_validation"]["target6_binding"].
                   __setitem__("product_order", "A*B^-1*C"))
    reject_receipt("right translation",
                   lambda x: x["core_validation"]["target6_binding"].
                   __setitem__("translation", "right"))
    reject_receipt("context ordinary/paper orientation",
                   lambda x: x["core_validation"]["context_orientation"].
                   __setitem__("ordinary",
                               x["core_validation"]["context_orientation"][
                                   "paper"]))
    reject_receipt("first-free reducer",
                   lambda x: x["core_validation"]["remainder"][
                       "entries"].clear())
    reject_receipt("later-pivot elimination",
                   lambda x: x["core_validation"]["echelon"].update(
                       {"no_preceding_keys": False}))
    reject_receipt("consistent affine system",
                   lambda x: x["core_validation"]["affine"].update(
                       {"canonical_solution": [0, 0]}))
    reject_receipt("inconsistent affine system",
                   lambda x: x["core_validation"]["affine"].update(
                       {"consistent": False}))
    reject_receipt("exponent two versus inverse",
                   lambda x: x["core_validation"]["seed_binding"].update(
                       {"exponent_two_is_two_copies": False}))
    reject_receipt("raw model/direct mismatch",
                   lambda x: x["core_validation"]["raw_model_direct"].
                   update({"direct": {"gradient": [[1, 2]]}, "equal": True}))
    reject_receipt("nonzero base/delta arithmetic",
                   lambda x: x["core_validation"]["base_delta_canary"].
                   update({"direct": {0: 1}}))
    reject_receipt("cap projection drift",
                   lambda x: x.update({"caps_binding": {
                       **AFFINE_CAPS_BINDING,
                       "affine_caps_sha256": "0"*64}}))
    reject_receipt("authenticated pin projection drift",
                   lambda x: x["pins"].pop("q3_checker"))
    reject_receipt("closed top-level drift",
                   lambda x: x.update({"unexpected_load_bearing_field": True}))
    reject_receipt("diagnostic promotion",
                   lambda x: x["core_validation"]["diagnostics_excluded"]
                   .__class__ and x["core_validation"].update({
                       "acceptance": {"count": 33,
                                      "diagnostics_excluded": False},
                       "diagnostics_excluded": False}))
    bad_provider = copy.deepcopy(provider)
    bad_provider["proof"]["translation_action"] = "right"
    bad_proof = copy.deepcopy(control)
    bad_proof["core_validation"]["selected_proof"]["proof"] = \
        bad_provider["proof"]
    expect_reject(lambda: invoke(bad_proof, bad_provider),
                  "checker shared-core mutation: selected proof")
    reject_receipt("terminal status", lambda x: x.update(
        {"status": "B345_SEEDSPAN_AFFINE_SEARCH_INCOMPLETE"}))
    reject_receipt("terminal claim", lambda x: x.update(
        {"claim_boundary": no_claims}))
    reject_receipt("terminal incomplete", lambda x: x.update(
        {"status": "B345_SEEDSPAN_AFFINE_SEARCH_INCOMPLETE",
         "terminal_token": "B345_SEEDSPAN_AFFINE_SEARCH_INCOMPLETE"}))
    reject_receipt("terminal unknown input", lambda x: x.update(
        {"status": "B345_SEEDSPAN_AFFINE_UNKNOWN_INPUT",
         "terminal_token": "B345_SEEDSPAN_AFFINE_UNKNOWN_INPUT"}))

    unknown = copy.deepcopy(base)
    unknown.update({
        "status": "B345_SEEDSPAN_AFFINE_UNKNOWN_INPUT",
        "terminal_token": "B345_SEEDSPAN_AFFINE_UNKNOWN_INPUT",
        "reason": "selftest authenticated q3 schema drift",
        "claim_boundary": no_claims,
        "input_q3_terminal": None,
        "fixed_roof": {
            "typed_source_word": list(FIXED_WORD), "exponent": 2,
            "marking_m": 0, "lambda": 1,
            "outside_by_index_three": None,
        },
        "affine_system": None, "targets": [], "diagnostics": [],
        "seed_family": None, "normalized_inverse_fibre": None,
        "occurrence_preflight": None, "prefix_accounting": None,
        "strong_canary": None, "typed_positive_candidate": None,
        "partial": None,
        "input_errors": {
            "authenticated_external_input":
                "selftest authenticated q3 schema drift",
            "mathematical_scan_started": False,
        },
        "resource_guards": {
            "hit": False, "hit_reason": None,
            "terminal_on_hit": "B345_RELFRAT3_WORDEXPR_UNKNOWN_RESOURCE",
        },
        "performance": {"runtime_seconds": 0.0,
                         "phase_complete": "authenticated_input"},
    })
    invoke(unknown)
    unknown_pin = copy.deepcopy(unknown)
    unknown_pin["pins"]["q3_driver"]["sha256"] = "0"*64
    expect_reject(lambda: invoke(unknown_pin),
                  "checker UNKNOWN_INPUT pin mutation")

    def resource_receipt(phase: str, evaluated: int,
                         target: int, seed: int,
                         reason: str = "affine_rows",
                         relation: str = "gt") -> dict[str, Any]:
        limit = checker_resource_cap_limit(reason)
        observed = limit + 1 if relation == "gt" else limit
        partial = {"phase": phase, "evaluated_targets": evaluated,
                   "unevaluated_target_results_are_null": True,
                   "cap_reason": reason, "current_target_ordinal": target,
                   "current_seed_index": seed, "live_remainder_entries": 0,
                   "cap_key": reason,
                   "cap_limit": limit, "observed_count": observed,
                   "trigger_relation": relation,
                   "affine_equations": 0}
        return {**base, "status": "B345_SEEDSPAN_AFFINE_UNKNOWN_RESOURCE",
                "terminal_token": "B345_SEEDSPAN_AFFINE_UNKNOWN_RESOURCE",
                "reason": reason, "claim_boundary": no_claims,
                "partial": partial,
                "resource_guards": {
                    "hit": True, "hit_reason": reason,
                    "terminal_on_hit":
                        "B345_SEEDSPAN_AFFINE_UNKNOWN_RESOURCE"}}

    invoke(resource_receipt("authenticated_input", 0, 0, 0))
    invoke(resource_receipt("affine_source_preflight", 0, 0, 7))
    invoke(resource_receipt("affine_target_1", 0, 1, 0))
    invoke(resource_receipt("positive_typed_replay", 0, 3, 5,
                            "element_pool", "ge"))
    positive_acceptance = resource_receipt("positive_typed_replay", 33, 1, 4)
    checker_resource_partial_state(positive_acceptance["partial"])
    positive_diagnostics = resource_receipt(
        "positive_typed_replay_diagnostics", 33, 17, 4)
    checker_resource_partial_state(positive_diagnostics["partial"])
    positive_diag_bad = copy.deepcopy(positive_diagnostics)
    positive_diag_bad["partial"]["current_target_ordinal"] = 18
    expect_reject(
        lambda: checker_resource_partial_state(positive_diag_bad["partial"]),
        "checker positive diagnostic range mutation")
    ge_boundary = resource_receipt("authenticated_input", 0, 0, 0,
                                   "element_pool", "ge")
    invoke(ge_boundary)
    ge_bad = copy.deepcopy(ge_boundary)
    ge_bad["partial"]["observed_count"] -= 1
    expect_reject(lambda: invoke(ge_bad),
                  "checker resource ge boundary mutation")
    resource_bad = resource_receipt("affine_target_1", 0, 1, 0)
    resource_bad["partial"]["cap_reason"] = "wrong_cap"
    expect_reject(lambda: invoke(resource_bad),
                  "checker shared-core resource partial mutation")
    print("D972_B345_SEEDSPAN_AFFINE_CHECKER_SELFTEST_PASS "
          "shared_core=1 provider_boundary=1 seed_order=1 seed_digest=1 "
          "raw_chain=1 raw_pair=1 raw_inverse=1 raw_square=1 "
          "base_delta_split=1 context_registry=1 target6_order=1 "
          "full_remainder=1 later_pivot=1 "
          "affine_consistent=1 affine_inconsistent=1 selected_proof=1 "
           "diagnostics_excluded=1 terminals=4 resource_phases=4 "
           "gt_ge=1 source_seed=1 positive_phase=1 positive_ranges=1 "
           "prefix_counts=1 deadline=1")


def main() -> int:
    global CHECKER_STARTED, CHECKER_CHECKS
    parser = argparse.ArgumentParser()
    parser.add_argument("q3_artifact", nargs="?", type=Path)
    parser.add_argument("artifact", nargs="?", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        require(args.q3_artifact is None and args.artifact is None,
                "affine checker selftest paths")
        affine_checker_self_test()
        return 0
    require(args.q3_artifact is not None and args.artifact is not None,
            "affine checker paths")
    q3_path, artifact = args.q3_artifact.resolve(), args.artifact.resolve()
    repo = Path(__file__).resolve().parents[1]
    require(q3_path == (repo/Q3_ARTIFACT_PATH).resolve() and
            artifact == (repo/AFFINE_OUTPUT_PATH).resolve(),
            "affine checker fixed paths")
    q3 = json.loads(q3_path.read_text(encoding="utf-8"))
    data = json.loads(artifact.read_text(encoding="utf-8"))
    CHECKER_STARTED = time.monotonic(); CHECKER_CHECKS = 0
    checker_affine_validate(data, q3, q3_path, artifact, repo)
    checker_deadline("affine checker completion", force=True)
    print(f"D972_B345_SEEDSPAN_AFFINE_CHECK_PASS terminal={data['terminal_token']} "
          f"artifact_sha256={digest_file(artifact)}", flush=True)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Reject as exc:
        print(f"B345_SEEDSPAN_AFFINE_CHECK_FAIL {exc}", file=sys.stderr)
        raise SystemExit(1)
