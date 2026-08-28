#!/usr/bin/env python3
"""R07 A4 word-independent compressed first-successor kernel.

This module is deliberately self contained.  Production consumes only a
positive, independently accepted task198 roof presentation.  SELFTEST uses a
small typed affine extension and exercises the same boundary, ancestry, and
invariant-closure interfaces.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import inspect
import json
import os
import sys
import time
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "d972-r07-word-independent-successor-kernel/v1"
SELFTEST_SCHEMA = "d972-r07-word-independent-successor-kernel-selftest/v1"
ISO = "R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V1_PASS"
UNKNOWN_INPUT = "UNKNOWN_INPUT"
UNKNOWN_RESOURCE = "UNKNOWN_RESOURCE"
Q0_ORDER = 1469664
PRESENTATION_ROWS = 6441
CONTEXT_IDS = (21, 22, 23, 24, 25, 1, 27, 21, 26, 28)
CONTEXT_TYPES = ("E3", "E3", "E3", "E3", "E3", "E4", "E4", "E4", "E4", "E4")
CONTEXT_TAGS = ("E3-C21", "E3-C22", "E3-C23", "E3-C24", "E3-C25",
                "E4-C1", "E4-C27", "E4-C21", "E4-C26", "E4-C28")
CONTEXT_SOURCES = (
    ("x", "y"), ("x", "z"), ("y", "z"), ("u", "x"), ("u", "y"),
    ("A23", "A34"), ("PP(A12,A13)", "PP(A24,A34)"),
    ("A12", "A23"), ("PP(A13,A23)", "A34"),
    ("A12", "PP(A23,A24)"),
)
CONTEXT_LEDGER = tuple({"index": i, "context_id": CONTEXT_IDS[i],
                        "type": CONTEXT_TYPES[i], "tag": CONTEXT_TAGS[i],
                        "source": list(CONTEXT_SOURCES[i])}
                       for i in range(10))
RESOURCE_CAPS = {"wall_seconds": 14400, "rss_bytes": 8000000000,
                 "input_bytes": 500000000, "relator_evaluations": 6441,
                 "affine_oracle_rounds": 1000000, "boundary_columns": 1000000,
                 "membership_queries": 1000000, "accepted_rank": 100000,
                 "queue_actions": 1000000, "ancestry_words": 1000000,
                 "ancestry_nodes": 1000000, "dual_correlations": 1000000,
                 "checker_work": 1000000, "checkpoint_bytes": 100000000,
                 "serialized_bytes": 2000000000}
MUTATIONS = (
    "task198_bytes", "task198_schema", "task198_terminal", "task198_run",
    "task198_head", "task198_artifact", "task198_member", "checker_acceptance",
    "projected_coordinate", "selected_index", "inverse_scalar", "word_exponent",
    "delta0_identity", "d1_z0_target", "k_z_source_word",
    "presentation_word", "presentation_complete", "context_type", "context_id",
    "source_substitution", "e3_c21_e4_c21_merge", "repeated_e3_insertion",
    "paper_product_order", "affine_multiplication", "affine_inverse",
    "crossed_derivation_order", "roof_reduction", "raw_coordinate", "block_tag",
    "omitted_boundary", "boundary_coefficient", "false_positive_membership",
    "false_negative_dual", "k_row_coefficient", "pivot", "ancestry_word",
    "omitted_relator", "omitted_generator_translate", "early_queue_terminal",
    "generator_action", "generator_inverse", "order_three", "commutator",
    "rank", "order", "nilpotence_bound", "delta1_bfs", "task192_word",
    "selftest_production", "traversal_stale", "resource_stop_completion",
    "false_d1", "false_e1", "false_mu1", "false_lift", "false_fake", "false_ihara",
)

PROOF_PINS = (
    ("sol/proof_r07_task179_relative_frattini_successor_v145.md", 13819, "b08f140838b78424cafa9528eafbcab9442f94cf92ce2cb42e15fc88ed489a51"),
    ("sol/proof_r07_recursive_relative_magnus_frattini_compiler_v168.md", 13829, "0f491cf9a4a43ac165eb70c60d37142053bde47eac965b2497d1d6abaa370cb3"),
    ("sol/proof_r07_compressed_diagonal_successor_relation_module_v188.md", 11314, "6512e810011105f83f845e9a41f63ee51fe278371f2cee6cc241e8022a41e822"),
    ("sol/proof_r07_ten_occurrence_seven_block_action_bridge_v189.md", 8814, "f3d2fdf9f1fec28c1f308fe7ee74e796cec465fd40dbd73f5e7dc478327da302"),
    ("sol/proof_r07_existing_6441_roof_presentation_v190.md", 9793, "562a1ac9db7c1b0a460a5383deff5858de073704f648d524566bd7d18a05e5e1"),
    ("sol/proof_r07_word_independent_successor_and_direct_pair_compiler_v231.md", 9622, "10582c0de99579d297a6d2bed3dd8c313fab85784cb9fd9b0b12e9859556906e"),
    ("sol/luna_task_232_r07_word_independent_successor_kernel_v1.md", 10486, "3e9f22192657343f7d205faef0eef7996af0ff5e720ec9f6fbab769d85d708a2"),
    ("sol/luna_task_244_r07_task232_second_actual_kernel_repair_v1.md", 7117, "474a9590972c1ec9ebbb4f6b6563ffce306e721393c77cd3b57b9c72f644a2b1"),
    ("sol/luna_task_244b_r07_task232_projection_anchor_erratum_v1.md", 1806, "c75c005bfd12eda46c5cd47cfc47ff9bf1eb46c2381db2b782211936f7d0cc67"),
    ("sol/proof_r07_a4_anchored_relative_ideal_lift_v247.md", 12104, "84ff184d6f2a55c7f59874ab7fc6433be1826f34694d5f5228477affef896a53"),
    ("sol/luna_task_252_r07_task232_builtin_h2_projection_repair_v1.md", 2825, "b3b088367bf4f2a36034858e1becd8a274a5ceef55d9fdac08c984afc3906b62"),
)
TASK198_PINS = (
    ("search/d972_r07_seven_context_roof_presentation_v1.py", 137169, "6b2645b80f97256a659af81e856c086cca724b36e2a22ae70335b29ffa95d44c"),
    ("crosscheck/check_d972_r07_seven_context_roof_presentation_v1.py", 153420, "46c566925375cd87a7d95d1949715523c0fff8a2b857e9aa563e9ee094011af5"),
    ("search/certs/d972_r07_seven_context_roof_presentation_selftest_v1_20260828.json", 1605, "fb31f6a0be2f2f5b530c6fe99796476ea16edb72fe7ddc192323995f2ae55ce7"),
)
TASK198_EXTERNAL_FIELDS = {
    "artifact_id", "zip_sha256", "run", "head", "member",
    "member_bytes", "member_sha256",
}
TASK176_EXTERNAL = {
    "artifact_id": "9635036013",
    "zip_sha256": "250e25c992cbe8562f59fb808a8b0d86a7b54fdb750a57f2b1cd1c6cd0c89912",
    "run": "33044121344",
    "head": "0533e42019c9f67f6cec3d1566152db17b903836",
    "member": "d972_r07_all_seven_extension_section_census_v1.json",
    "member_bytes": 13649089,
    "member_sha256": "715441d8ecb1b4bb39a51cf3df15f04d6179ee6adeafa5b925485dbbe91f7f41",
}
TASK179_PIN = ("search/d972_r07_positive_common_word_colgen_v1.py", 123870,
               "47116826e1b94750fa5eaa0c577586aeaec23a476c5f004fc0d5ea83892845c7")


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def input_require(condition: bool, message: str) -> None:
    if not condition:
        raise InputStop(message)


class InputStop(RuntimeError):
    pass


class ResourceStop(RuntimeError):
    pass


class ResourceMeter:
    """One invocation-wide monotone meter; exhaustion is never success."""
    def __init__(self, caps: dict[str, int] | None = None) -> None:
        self.caps = dict(caps or RESOURCE_CAPS)
        self.counters = {key: 0 for key in self.caps}
        self.started = time.monotonic()

    def bump(self, name: str, amount: int = 1, phase: str = "") -> None:
        self.counters[name] = self.counters.get(name, 0) + int(amount)
        limit = self.caps.get(name)
        if limit is not None and self.counters[name] > limit:
            raise ResourceStop("phase=%s:cap=%s:value=%s:limit=%s" %
                               (phase, name, self.counters[name], limit))
        if time.monotonic() - self.started > self.caps.get("wall_seconds", 14400):
            raise ResourceStop("phase=%s:cap=wall_seconds:value=%s:limit=%s" %
                               (phase, int(time.monotonic() - self.started),
                               self.caps.get("wall_seconds", 14400)))

    def merge_snapshot(self, snapshot: dict[str, Any]) -> None:
        """Bind the pinned-runtime meter into the invocation envelope."""
        counters = snapshot.get("counters", {})
        for name, value in counters.items():
            self.counters[name] = max(int(self.counters.get(name, 0)), int(value))
        if "rss_bytes" in snapshot:
            self.counters["rss_bytes"] = max(int(self.counters.get("rss_bytes", 0)),
                                               int(snapshot["rss_bytes"]))
        self.counters["wall_seconds"] = max(
            float(self.counters.get("wall_seconds", 0)),
            float(snapshot.get("elapsed_seconds", 0)))


def mod3(row: dict[str, int]) -> dict[str, int]:
    return {k: v % 3 for k, v in row.items() if v % 3}


def row_add(a: dict[str, int], b: dict[str, int], scale: int = 1) -> dict[str, int]:
    out = dict(a)
    for key, value in b.items():
        z = (out.get(key, 0) + scale * value) % 3
        if z:
            out[key] = z
        else:
            out.pop(key, None)
    return out


def row_scale(a: dict[str, int], scale: int) -> dict[str, int]:
    return mod3({k: scale * v for k, v in a.items()})


H2_MODULUS = 9
H2_IDENTITY = (0, 0, 0)


def h2_mul(left: tuple[int, int, int], right: tuple[int, int, int]) -> tuple[int, int, int]:
    """The frozen H2(9) normal-form multiplication from task252."""
    a, b, r = left; ap, bp, rp = right
    return ((a + ap) % 9, (b + bp) % 9, (r + rp - b * ap) % 9)


def h2_inv(value: tuple[int, int, int]) -> tuple[int, int, int]:
    a, b, r = value
    return ((-a) % 9, (-b) % 9, (-r - a * b) % 9)


def free_reduce_word(word: Iterable[int]) -> list[int]:
    stack: list[int] = []
    for letter in word:
        letter = int(letter)
        if stack and stack[-1] == -letter:
            stack.pop()
        else:
            stack.append(letter)
    return stack


def h2_signed_word(word: Iterable[int]) -> tuple[int, int, int]:
    value = H2_IDENTITY
    generators = {1: (1, 0, 0), 2: (0, 1, 0)}
    for letter in word:
        base = generators[abs(int(letter))]
        value = h2_mul(value, base if letter > 0 else h2_inv(base))
    return value


def word_from_ancestry(terms: Iterable[dict[str, Any]]) -> list[int]:
    """Replay a K basis ancestry as a literal product of source words."""
    answer: list[int] = []
    for term in terms:
        word = term.get("conjugated_word", term.get("source_word"))
        require(type(word) is list and word, "word-bearing ancestry")
        coefficient = int(term.get("coefficient", 1)) % 3
        for _ in range(coefficient):
            answer.extend(int(letter) for letter in word)
    return free_reduce_word(answer)


class Echelon:
    """Exact F3 echelon retaining coefficients and source ancestry."""
    def __init__(self) -> None:
        self.rows: dict[str, dict[str, int]] = {}
        self.ancestry: dict[str, dict[str, int]] = {}
        self.pivots: list[str] = []

    def reduce(self, source: dict[str, int]) -> tuple[dict[str, int], dict[str, int]]:
        row = mod3(source)
        coeff: dict[str, int] = {}
        for pivot in self.pivots:
            z = row.get(pivot, 0)
            if z:
                row = row_add(row, self.rows[pivot], -z)
                for key, value in self.ancestry[pivot].items():
                    # The reduced row is source minus z times the pivot row;
                    # ancestry follows that same subtraction and later pivot
                    # scaling, so literal replay is exact.
                    q = (coeff.get(key, 0) - z * value) % 3
                    if q: coeff[key] = q
                    else: coeff.pop(key, None)
        return row, coeff

    def insert(self, source: dict[str, int], source_id: str) -> tuple[str, dict[str, int]] | None:
        row, coeff = self.reduce(source)
        if not row:
            return None
        pivot = min(row)
        scale = 1 if row[pivot] == 1 else 2
        self.rows[pivot] = row_scale(row, scale)
        ancestry = {key: (scale * value) % 3 for key, value in coeff.items()
                    if (scale * value) % 3}
        ancestry[source_id] = (ancestry.get(source_id, 0) + scale) % 3
        self.ancestry[pivot] = {k: v for k, v in ancestry.items() if v}
        self.pivots.append(pivot)
        self.pivots.sort()
        return pivot, self.ancestry[pivot]

    def dual(self, target: dict[str, int]) -> dict[str, int]:
        remainder, _ = self.reduce(target)
        require(remainder, "dual requested for member")
        functional = {min(remainder): 1}
        for pivot in reversed(self.pivots):
            z = (-sum(v * functional.get(k, 0) for k, v in self.rows[pivot].items() if k != pivot)) % 3
            if z: functional[pivot] = z
            else: functional.pop(pivot, None)
        require(all(sum(a * functional.get(k, 0) for k, a in row.items()) % 3 == 0 for row in self.rows.values()), "dual boundary correlation")
        require(sum(a * functional.get(k, 0) for k, a in target.items()) % 3 != 0, "dual target correlation")
        return functional


def complete_membership(candidate: dict[str, int], boundary: Iterable[dict[str, int]], rows: Iterable[dict[str, int]]) -> dict[str, Any]:
    echelon = Echelon()
    for i, row in enumerate(boundary):
        echelon.insert(row, "B:" + str(i))
    for i, row in enumerate(rows):
        echelon.insert(row, "K:" + str(i))
    remainder, coefficients = echelon.reduce(candidate)
    if not remainder:
        return {"member": True,
                "boundary_coefficients": {k: v for k, v in coefficients.items() if k.startswith("B:")},
                "k_coefficients": {k: v for k, v in coefficients.items() if k.startswith("K:")},
                "replay": True,
                "pivots": list(echelon.pivots)}
    return {"member": False, "dual": echelon.dual(candidate),
            "pivots": list(echelon.pivots)}


class AffinePair:
    """Typed successor pair: (translation, roof value).

    The callback is an authenticated roof action.  Keeping this primitive in
    the consumer ABI prevents accidental use of the full ambient affine
    product and makes multiplication/inverse order explicit.
    """
    def __init__(self, translation: dict[str, int], roof: Any,
                 action: Any, roof_mul: Any, roof_inv: Any) -> None:
        self.translation = mod3(translation)
        self.roof = roof
        self.action = action
        self.roof_mul = roof_mul
        self.roof_inv = roof_inv

    def mul(self, other: "AffinePair") -> "AffinePair":
        require(self.action is other.action, "typed affine action")
        moved = self.action(self.roof, other.translation)
        return AffinePair(row_add(self.translation, moved),
                          self.roof_mul(self.roof, other.roof),
                          self.action, self.roof_mul, self.roof_inv)

    def inverse(self) -> "AffinePair":
        return AffinePair(self.action(self.roof_inv(self.roof),
                                      row_scale(self.translation, -1)),
                          self.roof_inv(self.roof), self.action,
                          self.roof_mul, self.roof_inv)

    def reduction(self) -> dict[str, Any]:
        return {"roof": self.roof, "translation": self.translation}


def crossed_derivation(word: Iterable[int], prefixes: Iterable[Any],
                       component: str) -> dict[str, int]:
    """Build a signed left-Fox chain from an exact prefix stream."""
    row: dict[str, int] = {}
    for index, (letter, prefix) in enumerate(zip(word, prefixes)):
        sign = 1 if int(letter) > 0 else -1
        key = component + ":" + str(index) + ":" + repr(prefix)
        row[key] = (row.get(key, 0) + sign) % 3
    return mod3(row)


def word_reduce(word: Iterable[int]) -> tuple[int, ...]:
    out: list[int] = []
    for letter in word:
        letter = int(letter)
        if out and out[-1] == -letter:
            out.pop()
        else:
            out.append(letter)
    return tuple(out)


def word_inverse(word: Iterable[int]) -> tuple[int, ...]:
    return tuple(-x for x in reversed(tuple(word)))


def word_product(*words: Iterable[int]) -> tuple[int, ...]:
    result: tuple[int, ...] = ()
    for word in words:
        result = word_reduce(result + tuple(word))
    return result


def pp(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    # Paper convention is right-to-left: PP(A,B)=B+A.
    return word_product(right, left)


def exact_contexts() -> list[dict[str, Any]]:
    x, y = (1,), (3,)
    z = word_inverse(pp(x, y))
    u = word_inverse(pp(y, x))
    return [
        {"type": "E3", "context_id": 21, "source": (x, y)},
        {"type": "E3", "context_id": 22, "source": (x, z)},
        {"type": "E3", "context_id": 23, "source": (y, z)},
        {"type": "E3", "context_id": 24, "source": (u, x)},
        {"type": "E3", "context_id": 25, "source": (u, y)},
        {"type": "E4", "context_id": 1, "source": ((4,), (6,))},
        {"type": "E4", "context_id": 27, "source": (pp((1,), (2,)), pp((5,), (6,)))},
        {"type": "E4", "context_id": 21, "source": ((1,), (4,))},
        {"type": "E4", "context_id": 26, "source": (pp((2,), (4,)), (6,))},
        {"type": "E4", "context_id": 28, "source": ((1,), pp((4,), (5,)))},
    ]


def build_typed_successors() -> list[dict[str, Any]]:
    """Return the ten literal source substitutions used by the successor."""
    x, y = (1,), (3,)
    z = word_inverse(pp(x, y))
    u = word_inverse(pp(y, x))
    values = [(x, y), (x, z), (y, z), (u, x), (u, y),
              ((4,), (6,)), (pp((1,), (2,)), pp((5,), (6,))),
              ((1,), (4,)), (pp((2,), (4,)), (6,)),
              ((1,), pp((4,), (5,)))]
    answer = []
    for index, descriptor in enumerate(CONTEXT_LEDGER):
        answer.append({"index": index, "type": descriptor["type"],
                       "context_id": descriptor["context_id"],
                       "source_substitution": CONTEXT_SOURCES[index],
                       "source_words": values[index]})
    require(answer[0]["source_substitution"] == ("x", "y") and
            answer[7]["source_substitution"] == ("A12", "A23") and
            answer[0]["type"] == "E3" and answer[7]["type"] == "E4",
            "ten literal typed substitutions")
    return answer


def toy_action(row: dict[str, int], letter: int, tag_count: int = 10) -> dict[str, int]:
    """Noncentral typed action; tags intentionally prevent blob merging."""
    out: dict[str, int] = {}
    for key, value in row.items():
        tag, coordinate = key.split(":")
        i = int(coordinate)
        if int(tag) >= tag_count:
            out[key] = (out.get(key, 0) + value) % 3
            continue
        # x swaps the two coordinates; y is a shear.  Inverses are distinct.
        j = (1 - i) if abs(letter) == 1 else i
        if abs(letter) == 2 and i == 1:
            out[f"{tag}:{j}"] = (out.get(f"{tag}:{j}", 0) + value) % 3
            out[f"{tag}:0"] = (out.get(f"{tag}:0", 0) + (1 if letter > 0 else 2) * value) % 3
        else:
            out[f"{tag}:{j}"] = (out.get(f"{tag}:{j}", 0) + value) % 3
    return mod3(out)


def toy_affine_checks() -> dict[str, Any]:
    def action(roof: tuple[int, ...], row: dict[str, int]) -> dict[str, int]:
        return toy_action(row, roof[-1])

    def roof_mul(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
        return word_reduce(left + right)

    def roof_inv(value: tuple[int, ...]) -> tuple[int, ...]:
        return word_inverse(value)

    left = AffinePair({"0:0": 1}, (1,), action, roof_mul, roof_inv)
    right = AffinePair({"0:1": 1}, (2,), action, roof_mul, roof_inv)
    product = left.mul(right)
    inverse = left.inverse()
    identity = left.mul(inverse)
    require(product.roof == (1, 2) and identity.roof == () and
            identity.translation == {}, "marked affine multiplication/inverse")
    require(crossed_derivation((1, -2), ((1,), (1, 2)), "R"),
            "crossed derivation signed order")
    return {"multiplication": True, "inverse": True, "reduction": True,
            "crossed_derivation": True, "kernel_exponent": 3}


def toy_defect(seed: int) -> dict[str, int]:
    # Ten typed blocks, each retaining its own raw affine/Fox coordinate.
    # Two independent coordinates are load-bearing; later rows are redundant.
    if seed % 3 == 0:
        return {f"{i}:0": 1 for i in range(10)}
    if seed % 3 == 1:
        return {f"{i}:1": 1 for i in range(10)}
    return {f"{i}:0": 2 for i in range(10)}


def ancestry_value(terms: list[dict[str, Any]], seeds: list[dict[str, int]]) -> dict[str, int]:
    result: dict[str, int] = {}
    for term in terms:
        value = dict(seeds[int(term["seed"])])
        for letter in term.get("conjugator", []):
            value = toy_action(value, int(letter))
        result = row_add(result, value, int(term.get("coefficient", 1)))
    return result


def run_toy() -> dict[str, Any]:
    arithmetic = toy_affine_checks()
    contexts = exact_contexts()
    successors = build_typed_successors()
    require(len(contexts) == 10 and contexts[0]["type"] == "E3" and contexts[7]["type"] == "E4", "typed context roster")
    require(contexts[0]["context_id"] == contexts[7]["context_id"] == 21, "E3-C21/E4-C21 must remain distinct")
    seeds = [toy_defect(i) for i in range(6)]
    toy_seed_words = [[1], [2], [1, 2], [2, 1], [-1], [-2]]
    # Complete translated boundaries overlap the defect support.  The first
    # two rows are a nontrivial redundant equality; this is not a sampled
    # boundary list and exercises quotient membership on shared coordinates.
    boundary = [{"0:0": 1, "0:1": 1}, {"0:0": 2, "0:1": 2},
                {"1:0": 1}]
    basis = Echelon()
    records: list[dict[str, Any]] = []
    queue: list[int] = []
    basis_terms: list[list[dict[str, Any]]] = []
    for index, seed in enumerate(seeds):
        result = basis.insert(seed, "R:" + str(index))
        if result:
            pivot, ancestry = result
            terms = [{"seed": index, "conjugator": [], "source_word": toy_seed_words[index],
                      "coefficient": 1}]
            basis_terms.append(terms)
            queue.append(len(basis_terms) - 1)
            records.append({"kind": "relator", "index": index, "pivot": pivot,
                            "ancestry": terms, "coefficients": ancestry})
    cursor = 0
    while cursor < len(queue):
        basis_index = queue[cursor]
        cursor += 1
        source = basis.rows[basis.pivots[basis_index]]
        for letter in (1, -1, 2, -2):
            translated = toy_action(source, letter)
            reduced, _ = basis.reduce(translated)
            if reduced:
                result = basis.insert(translated, "T:" + str(basis_index) + ":" + str(letter))
                if result:
                    pivot, ancestry = result
                    terms = []
                    for term in basis_terms[basis_index]:
                        prior_word = list(term.get("source_word", toy_seed_words[term["seed"]]))
                        terms.append({"seed": term["seed"],
                                      "conjugator": [letter] + list(term.get("conjugator", [])),
                                      "source_word": [letter] + prior_word + [-letter],
                                      "coefficient": term.get("coefficient", 1)})
                    basis_terms.append(terms)
                    queue.append(len(basis_terms) - 1)
                    records.append({"kind": "translate", "basis": basis_index,
                                    "letter": letter, "pivot": pivot,
                                    "ancestry": terms, "coefficients": ancestry})
    rank = len(basis.pivots)
    require(rank >= 2, "toy successor rank")
    require(cursor == len(queue), "queue exhaustion")
    # Initial defects and all four translates have exact membership receipts.
    membership = []
    for index, seed in enumerate(seeds):
        membership.append(complete_membership(seed, boundary, list(basis.rows.values())))
        require(membership[-1]["member"], "initial defect containment")
    translates = []
    for i, pivot in enumerate(basis.pivots):
        for letter in (1, -1, 2, -2):
            receipt = complete_membership(toy_action(basis.rows[pivot], letter), boundary, list(basis.rows.values()))
            require(receipt["member"], "translate containment")
            translates.append(receipt)
    # Literal ancestry and elementary-abelian replay.
    for i, terms in enumerate(basis_terms):
        require(ancestry_value(terms, seeds) == basis.rows[basis.pivots[i]], "ancestry replay")
        require(toy_action(basis.rows[basis.pivots[i]], 1) != toy_action(basis.rows[basis.pivots[i]], 2), "noncentral action")
        require(row_add(basis.rows[basis.pivots[i]], basis.rows[basis.pivots[i]], 2) == {}, "order-three replay")
    for a in basis.rows.values():
        for b in basis.rows.values():
            require(row_add(row_add(a, b), a, 2) == b, "pairwise commutation replay")
    # Two syntactically different accepted bases have equal spans.
    alternate = Echelon()
    for row in list(basis.rows.values())[::-1]:
        alternate.insert(row, "A")
    for row in basis.rows.values():
        require(complete_membership(row, boundary, list(alternate.rows.values()))["member"], "alternate span forward")
    for row in alternate.rows.values():
        require(complete_membership(row, boundary, list(basis.rows.values()))["member"], "alternate span reverse")
    negative = complete_membership({"outside": 1}, boundary, list(basis.rows.values()))
    require(negative["member"] is False and negative.get("dual"), "negative dual")
    action_matrices: dict[str, dict[str, dict[str, int]]] = {str(letter): {}
                                                              for letter in (1, -1, 2, -2)}
    for i, pivot in enumerate(basis.pivots):
        for letter in (1, -1, 2, -2):
            moved_receipt = complete_membership(
                toy_action(basis.rows[pivot], letter), boundary,
                list(basis.rows.values()))
            require(moved_receipt["member"], "toy action matrix membership")
            action_matrices[str(letter)][str(i)] = dict(
                moved_receipt.get("k_coefficients", {}))
    toy_basis_word = ([-1, -2, 1, 2] * 6)
    toy_anchor_word = free_reduce_word(toy_basis_word * 2)
    require(h2_signed_word(toy_basis_word) == (0, 0, 6) and
            h2_signed_word(toy_anchor_word) == (0, 0, 3),
            "toy H2 exponent-two anchor")
    toy_basis_receipts = [
        {"index": 0, "source_word": toy_basis_word, "d1_value": [0, 0, 6],
         "projected_exponent": 2,
         "roof_values": [{"context": i, "roof_identity": True, "chain": {}}
                         for i in range(10)], "delta0_identity": True,
         "delta1_k_membership": True,
         "membership": {"member": True, "k_coefficients": {"K:0": 1}},
         "replay": True},
        {"index": 1, "source_word": [1, -1], "d1_value": [0, 0, 0],
         "projected_exponent": 0,
         "roof_values": [{"context": i, "roof_identity": True, "chain": {}}
                         for i in range(10)], "delta0_identity": True,
         "delta1_k_membership": True,
         "membership": {"member": True, "k_coefficients": {"K:1": 1}},
         "replay": True},
    ]
    return {"rank": rank, "basis": [{"pivot": p, "row": basis.rows[p], "ancestry": basis_terms[i]} for i, p in enumerate(basis.pivots)],
            "initial_membership": membership, "translate_membership": translates,
            "boundary": boundary, "queue_actions": len(records), "contexts": CONTEXT_LEDGER,
            "successors": successors, "roof_reductions": [True for _ in successors],
            "successor_digest": digest([item["source_words"] for item in successors]),
            "affine_checks": arithmetic,
            "order": 3 ** rank, "nilpotence_bound": 2 * rank + 1,
            "basis_digest": digest([basis.rows[p] for p in basis.pivots]),
            "alternate_rank": len(alternate.pivots), "negative_dual": negative["dual"],
            "boundary_digest": digest(boundary), "action_matrices": action_matrices,
            "inverse_products": {"1-1": True, "-11": True,
                                 "2-2": True, "-22": True},
            "order_three": True, "pairwise_commutation": True,
            "alternate_span_forward": True, "alternate_span_reverse": True,
            "task198_binding": {"schema": "d972-r07-seven-context-roof-presentation/v1",
                                "terminal": "ROOF_BRIDGE_ISOMORPHISM", "run": "fixture-run",
                                "head": "fixture-head", "artifact": "fixture-artifact",
                                "member": True, "checker": True, "delta1_bfs": "unused",
                                "task192_word": "unused"},
            "resource_terminal": {"terminal": "UNKNOWN_RESOURCE", "rank_zero": True},
            "projection_anchor": {"projected_coordinate": [2, 0], "selected_index": 0,
                                   "inverse_scalar": 2, "word_exponent": 2,
                                   "source_word": toy_anchor_word, "delta0_identity": True,
                                   "delta1_k_membership": True, "d1_z0": [0, 0, 3],
                                   "basis_coefficients": {"0": 2},
                                   "roof_values": [{"context": i, "roof_identity": True,
                                                    "chain": {}} for i in range(10)],
                                   "membership": {"member": True,
                                                  "k_coefficients": {"K:0": 2}},
                                   "replay": True},
            "basis_projections": [item["projected_exponent"] for item in toy_basis_receipts],
            "basis_d1_values": [item["d1_value"] for item in toy_basis_receipts],
            "basis_receipts": toy_basis_receipts,
            "forbidden_downstream": {"d1": False, "e1": False, "mu1": False,
                                      "lift": False, "fake": False, "Ihara_witness": False}}


def pivot_scale_ancestry_selftest() -> dict[str, Any]:
    """Exercise a nontrivial reduction whose new pivot normalizes by two."""
    echelon = Echelon()
    first = {"a": 1}
    second = {"a": 2, "b": 2}
    require(echelon.insert(first, "S1") is not None, "ancestry first insert")
    inserted = echelon.insert(second, "S2")
    require(inserted is not None and inserted[0] == "b" and
            echelon.ancestry["b"] == {"S1": 2, "S2": 2},
            "pivot scale ancestry coefficients")
    replay = row_scale(row_add(second, first), 2)
    require(replay == echelon.rows["b"], "pivot scale ancestry replay")
    return {"first_reduction": True, "pivot": "b", "scale": 2,
            "source_keys": ["S1", "S2"], "replayed": True}


def semantic_mutation_replay(certificate: dict[str, Any]) -> int:
    """Apply each registered mutation to a load-bearing certificate object."""
    def validate(value: dict[str, Any]) -> None:
        require(value["rank"] >= 2 and value["order"] == 3 ** value["rank"], "mutation rank/order")
        require(value["nilpotence_bound"] == 2 * value["rank"] + 1, "mutation nilpotence")
        require([(row.get("index"), row.get("type"), row.get("context_id"), row.get("tag"))
                 for row in value["contexts"]] ==
                [(row["index"], row["type"], row["context_id"], row["tag"])
                 for row in CONTEXT_LEDGER], "mutation typed contexts")
        require(value["task198_binding"].get("schema") ==
                "d972-r07-seven-context-roof-presentation/v1" and
                value["task198_binding"].get("terminal") == "ROOF_BRIDGE_ISOMORPHISM" and
                all(value["task198_binding"].get(key) for key in
                    ("run", "head", "artifact", "member", "checker", "delta1_bfs", "task192_word")) and
                value["task198_binding"].get("delta1_bfs") == "unused" and
                value["task198_binding"].get("task192_word") == "unused",
                "mutation task198 binding")
        require(all(item.get("source_words") for item in value["successors"]) and
                value["successor_digest"] == digest([item["source_words"] for item in value["successors"]]),
                "mutation source substitutions")
        require(len(value["successors"]) == 10 and
                value["roof_reductions"] == [True] * 10, "mutation roof")
        require(value["affine_checks"]["multiplication"] is True and value["affine_checks"]["inverse"] is True and
                value["affine_checks"]["crossed_derivation"] is True, "mutation affine")
        require(value["queue_actions"] > 0 and len(value["basis"]) == value["rank"], "mutation queue/basis")
        require(all(item.get("row") for item in value["basis"]) and
                all(item.get("pivot") and item["pivot"] in item["row"]
                    for item in value["basis"]),
                "mutation basis rows")
        require(value["basis_digest"] == digest([item["row"] for item in value["basis"]]),
                "mutation basis digest")
        require(value["boundary"] and
                any(set(row) & set(value["basis"][0]["row"]) for row in value["boundary"]),
                "mutation complete boundary overlap")
        require(value["boundary_digest"] == digest(value["boundary"]),
                "mutation boundary transcript")
        require(all(item.get("ancestry") and
                    all(term.get("source_word") for term in item["ancestry"])
                    for item in value["basis"]), "mutation ancestry")
        require(all(item.get("member") is True for item in value["initial_membership"] + value["translate_membership"]), "mutation membership")
        require(len(value["initial_membership"]) == 6 and
                len(value["translate_membership"]) == 4 * value["rank"],
                "mutation completeness replay")
        require(value["alternate_rank"] == value["rank"] and
                value["alternate_span_forward"] is True and
                value["alternate_span_reverse"] is True, "mutation alternate span")
        require(value["action_matrices"] and
                all(len(value["action_matrices"][str(letter)]) == value["rank"]
                    for letter in (1, -1, 2, -2)) and
                all(value["inverse_products"].values()) and
                value["order_three"] is True and
                value["pairwise_commutation"] is True, "mutation action matrices")
        anchor = value.get("projection_anchor", {})
        receipts = value.get("basis_receipts", [])
        require(len(receipts) == value["rank"] and
                all(type(item.get("source_word")) is list and item.get("source_word") and
                    all(type(letter) is int and letter in (-2, -1, 1, 2)
                        for letter in item["source_word"]) and
                    (d1 := h2_signed_word(item["source_word"])) ==
                    tuple(item.get("d1_value", [])) and
                    d1[0:2] == (0, 0) and d1[2] in (0, 3, 6) and
                    item.get("projected_exponent") == (d1[2] // 3) % 3 and
                    len(item.get("roof_values", [])) == 10 and
                    all(roof.get("roof_identity") is True
                        for roof in item["roof_values"]) and
                    item.get("delta0_identity") is True and
                    item.get("delta1_k_membership") is True and
                    item.get("membership", {}).get("member") is True and
                    item.get("replay") is True
                    for item in receipts) and
                value.get("basis_projections") ==
                [item["projected_exponent"] for item in receipts] and
                value.get("basis_d1_values") ==
                [item["d1_value"] for item in receipts],
                "mutation reconstructed projection receipts")
        projection = value["basis_projections"]
        require(any(projection), "mutation projection nonzero")
        selected = next(i for i, exponent in enumerate(projection) if exponent)
        scalar = 1 if projection[selected] == 1 else 2
        require(anchor.get("projected_coordinate") == projection and
                anchor.get("selected_index") == selected and
                anchor.get("inverse_scalar") == scalar and
                anchor.get("word_exponent") == scalar and
                type(anchor.get("source_word")) is list and
                h2_signed_word(anchor["source_word"]) == (0, 0, 3) and
                anchor.get("source_word") ==
                free_reduce_word(receipts[selected]["source_word"] * scalar) and
                anchor.get("delta0_identity") is True and
                anchor.get("delta1_k_membership") is True and
                anchor.get("d1_z0") == [0, 0, 3] and
                anchor.get("basis_coefficients") == {str(selected): scalar} and
                len(anchor.get("roof_values", [])) == 10 and
                all(roof.get("roof_identity") is True
                    for roof in anchor["roof_values"]) and
                anchor.get("membership", {}).get("member") is True and
                anchor.get("replay") is True, "mutation projection anchor")
        require(value["negative_dual"], "mutation complete dual")
        require(value["task198_binding"].get("member") is True and
                value["task198_binding"].get("checker") is True and
                value["resource_terminal"].get("rank_zero") is True and
                all(flag is False for flag in value["forbidden_downstream"].values()),
                "mutation external/resource/downstream")

    rejected = 0
    for name in MUTATIONS:
        mutant = copy.deepcopy(certificate)
        if name == "task198_bytes": mutant["task198_binding"]["artifact"] = ""
        elif name == "task198_schema": mutant["task198_binding"]["schema"] = "bad"
        elif name == "task198_terminal": mutant["task198_binding"]["terminal"] = "UNKNOWN"
        elif name == "task198_run": mutant["task198_binding"]["run"] = ""
        elif name == "task198_head": mutant["task198_binding"]["head"] = ""
        elif name == "task198_artifact": mutant["task198_binding"]["artifact"] = ""
        elif name == "task198_member": mutant["task198_binding"]["member"] = False
        elif name == "checker_acceptance": mutant["task198_binding"]["checker"] = False
        elif name == "projected_coordinate": mutant["projection_anchor"]["projected_coordinate"] = [1, 0]
        elif name == "selected_index": mutant["projection_anchor"]["selected_index"] = -1
        elif name == "inverse_scalar": mutant["projection_anchor"]["inverse_scalar"] = 0
        elif name == "word_exponent": mutant["projection_anchor"]["word_exponent"] = 0
        elif name == "delta0_identity": mutant["projection_anchor"]["delta0_identity"] = False
        elif name == "d1_z0_target": mutant["projection_anchor"]["d1_z0"] = [0, 0, 2]
        elif name == "k_z_source_word": mutant["projection_anchor"]["source_word"] = []
        elif name == "presentation_word": mutant["basis"][0]["ancestry"][0]["source_word"] = []
        elif name == "presentation_complete": mutant["initial_membership"][0]["member"] = False
        elif name == "context_type": mutant["contexts"][0]["type"] = "E4"
        elif name == "context_id": mutant["contexts"][0]["context_id"] = 0
        elif name == "source_substitution": mutant["successors"][0]["source_words"] = []
        elif name == "e3_c21_e4_c21_merge": mutant["contexts"][7]["tag"] = "E3-C21"
        elif name == "repeated_e3_insertion": mutant["contexts"] = mutant["contexts"][:-1]
        elif name == "paper_product_order": mutant["successors"][0]["source_words"] = list(reversed(mutant["successors"][0]["source_words"]))
        elif name in ("affine_multiplication", "affine_inverse", "crossed_derivation_order"):
            mutant["affine_checks"][name.replace("_order", "")] = False
        elif name == "roof_reduction": mutant["roof_reductions"][0] = False
        elif name == "raw_coordinate": mutant["basis"][0]["row"] = {}
        elif name == "block_tag": mutant["contexts"][0]["tag"] = "bad"
        elif name == "omitted_boundary": mutant["boundary"] = []
        elif name == "boundary_coefficient": mutant["boundary"][0]["0:0"] = 2
        elif name == "false_positive_membership": mutant["initial_membership"][0]["member"] = False
        elif name == "false_negative_dual": mutant["negative_dual"] = {}
        elif name == "k_row_coefficient": mutant["basis"][0]["row"]["0:0"] = 2
        elif name == "pivot": mutant["basis"][0]["pivot"] = "bad"
        elif name == "ancestry_word": mutant["basis"][0]["ancestry"] = []
        elif name == "omitted_relator": mutant["initial_membership"].pop()
        elif name == "omitted_generator_translate": mutant["translate_membership"].pop()
        elif name == "early_queue_terminal": mutant["queue_actions"] = 0
        elif name == "generator_action": mutant["action_matrices"]["1"] = {}
        elif name == "generator_inverse": mutant["inverse_products"]["1-1"] = False
        elif name == "order_three": mutant["order_three"] = False
        elif name == "commutator": mutant["pairwise_commutation"] = False
        elif name in ("rank", "order", "nilpotence_bound"): mutant[name] = 0
        elif name == "delta1_bfs": mutant["task198_binding"]["delta1_bfs"] = "bad"
        elif name == "task192_word": mutant["task198_binding"]["task192_word"] = "bad"
        elif name == "selftest_production": mutant["task198_binding"]["member"] = False
        elif name == "traversal_stale": mutant["alternate_span_forward"] = False
        elif name == "resource_stop_completion": mutant["resource_terminal"]["rank_zero"] = False
        elif name == "false_ihara":
            mutant["forbidden_downstream"]["Ihara_witness"] = True
        elif name.startswith("false_"):
            mutant["forbidden_downstream"][name[6:]] = True
        try:
            validate(mutant)
        except RuntimeError:
            rejected += 1
    validate(certificate)
    require(rejected == len(MUTATIONS), "semantic mutation rejection")
    return rejected


def selftest(fixture: dict[str, Any] | None = None) -> dict[str, Any]:
    toy = run_toy()
    ancestry = pivot_scale_ancestry_selftest()
    rejected = semantic_mutation_replay(toy)
    if fixture is not None:
        expected = fixture.get("expected", {})
        input_require(expected.get("min_rank", 2) <= toy["rank"], "fixture rank")
        input_require(expected.get("contexts", 10) == len(toy["contexts"]), "fixture contexts")
    return {"schema": SELFTEST_SCHEMA, "status": "PASS", "terminal": ISO,
            "toy": toy, "mutation_controls": {"attempted": len(MUTATIONS),
            "rejected": rejected, "names": list(MUTATIONS),
            "pivot_scale_ancestry": ancestry}}


def checked_pin(path: str, size: int, expected: str) -> dict[str, Any]:
    candidate = ROOT / path
    input_require(candidate.is_file(), "missing pin:" + path)
    raw = candidate.read_bytes()
    input_require(len(raw) == size and hashlib.sha256(raw).hexdigest() == expected, "pin:" + path)
    return {"path": path, "bytes": len(raw), "sha256": expected}


def guarded(path: str, label: str) -> Path:
    p = Path(path)
    input_require(not p.is_absolute() and p.as_posix().startswith("ci/in/"), label + ":GUARDED_PATH")
    return ROOT / p


def authenticate_task198(path: str, manifest_path: str, producer_attestation: str,
                         checker_attestation: str) -> dict[str, Any]:
    receipt_path = guarded(path, "TASK198_RECEIPT")
    manifest_file = guarded(manifest_path, "TASK198_MANIFEST")
    producer_file = guarded(producer_attestation, "TASK198_PRODUCER_ATTESTATION")
    checker_file = guarded(checker_attestation, "TASK198_CHECKER_ATTESTATION")
    for pin in TASK198_PINS:
        checked_pin(*pin)
    for source in PROOF_PINS:
        checked_pin(*source)
    for f in (receipt_path, manifest_file, producer_file, checker_file):
        input_require(f.is_file() and f.stat().st_size > 0, "missing task198 input:" + f.as_posix())
    raw = receipt_path.read_bytes()
    try:
        receipt = json.loads(raw.decode("ascii"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise InputStop("TASK198_RECEIPT_JSON") from exc
    input_require(type(receipt) is dict and receipt.get("schema") == "d972-r07-seven-context-roof-presentation/v1", "TASK198_SCHEMA")
    body = dict(receipt)
    claimed = body.pop("self_digest_sha256", None)
    input_require(type(claimed) is str and claimed == digest(body), "TASK198_SELF_DIGEST")
    input_require(receipt.get("status") == "COMPLETE" and receipt.get("terminal") == "ROOF_BRIDGE_ISOMORPHISM", "TASK198_TERMINAL")
    delta0 = receipt.get("Delta0")
    presentation = delta0.get("presentation", {}) if type(delta0) is dict else {}
    input_require(type(presentation) is dict and presentation.get("row_count") == PRESENTATION_ROWS and
                  type(presentation.get("rows")) is list and
                  len(presentation["rows"]) == PRESENTATION_ROWS,
                  "TASK198_PRESENTATION")
    for ordinal, row in enumerate(presentation["rows"], 1):
        input_require(type(row) is dict and type(row.get("word")) is list and
                      all(type(letter) is int and letter in (-2, -1, 1, 2)
                          for letter in row["word"]) and
                      type(row.get("layer")) is str and
                      type(row.get("ordinal")) is int and row["ordinal"] == ordinal,
                      "TASK198_LITERAL_PRESENTATION_ROW")
    input_require(presentation.get("normal_closure_exact") is True and
                  delta0.get("normal_closure_exact") is True and
                  delta0.get("marked_generators") == {"x": [1], "y": [2]} and
                  type(delta0.get("order")) is int and delta0["order"] == 357128352,
                  "TASK198_COMPLETE_PRESENTATION")
    input_require(type(presentation.get("rows_sha256")) is str and
                  presentation["rows_sha256"] == digest(presentation["rows"]),
                  "TASK198_PRESENTATION_DIGEST")
    layers = {name: sum(row.get("layer") == name for row in presentation["rows"])
              for name in ("Gamma_Cayley", "action", "Q0_lift")}
    input_require(layers == {"Gamma_Cayley": 6318, "action": 104, "Q0_lift": 19},
                  "TASK198_PRESENTATION_LAYERS")
    chunks = presentation.get("chunks")
    expected_chunks = []
    for start in range(0, PRESENTATION_ROWS, 1024):
        part = presentation["rows"][start:start + 1024]
        expected_chunks.append({"start": start, "end": start + len(part),
                                "sealed": bool(part), "prefix_complete": True,
                                "sha256": digest(part)})
    input_require(type(chunks) is list and chunks == expected_chunks and
                  presentation.get("resume_cursor") == PRESENTATION_ROWS,
                  "TASK198_PRESENTATION_CHUNKS")
    input_require(type(receipt.get("bridge")) is dict and
                  receipt["bridge"].get("branch") == "ROOF_BRIDGE_ISOMORPHISM" and
                  receipt["bridge"].get("kernel_order") == 1,
                  "TASK198_BRIDGE_LEDGER")
    evaluator = receipt.get("evaluator")
    input_require(type(evaluator) is dict and
                  evaluator.get("schema") == "d972-r07-v188-roof-consumer-action-abi/v1" and
                  set(evaluator.get("entry_points", {})) ==
                  {"eval", "multiply", "inverse", "source_section", "action", "section_cocycle"},
                  "TASK198_EVALUATOR_ABI")
    manifest_raw = manifest_file.read_bytes()
    try:
        manifest = json.loads(manifest_raw.decode("ascii"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise InputStop("TASK198_MANIFEST_JSON") from exc
    receipt_sha = hashlib.sha256(raw).hexdigest()
    input_require(type(manifest) is dict and
                  manifest_raw == canonical(manifest) and
                  set(manifest) == TASK198_EXTERNAL_FIELDS and
                  manifest.get("member") == Path(path).name and
                  manifest.get("member_bytes") == len(raw) and
                  manifest.get("member_sha256") == receipt_sha and
                  type(manifest.get("artifact_id")) is str and manifest["artifact_id"] and
                  type(manifest.get("run")) is str and manifest["run"] and
                  type(manifest.get("head")) is str and len(manifest["head"]) == 40 and
                  all(ch in "0123456789abcdef" for ch in manifest["head"]) and
                  type(manifest.get("zip_sha256")) is str and
                  len(manifest["zip_sha256"]) == 64 and
                  all(ch in "0123456789abcdef" for ch in manifest["zip_sha256"]),
                  "TASK198_MANIFEST_BINDING")
    source_input = receipt.get("input")
    task176_input = source_input.get("task176", {}) if type(source_input) is dict else {}
    input_require(type(task176_input) is dict and
                  all(task176_input.get(key) == value for key, value in TASK176_EXTERNAL.items()),
                  "TASK198_EMBEDDED_EXTERNAL_BINDING")
    producer_line = producer_file.read_text(encoding="ascii").splitlines()
    checker_line = checker_file.read_text(encoding="ascii").splitlines()
    input_require(len(producer_line) == 1 and producer_line[0] == "R07_SEVEN_CONTEXT_ROOF_PRESENTATION_V1_PRODUCER_TERMINAL ROOF_BRIDGE_ISOMORPHISM", "TASK198_PRODUCER_ATTESTATION")
    input_require(len(checker_line) == 1 and checker_line[0] == "R07_SEVEN_CONTEXT_ROOF_PRESENTATION_V1_CHECKER_PASS terminal=ROOF_BRIDGE_ISOMORPHISM rows=6441", "TASK198_CHECKER_ATTESTATION")
    return {"receipt_path": path, "receipt_bytes": len(raw), "receipt_sha256": receipt_sha,
            "manifest_path": manifest_path, "producer_attestation": producer_attestation,
            "checker_attestation": checker_attestation, "presentation_rows": PRESENTATION_ROWS,
            "contexts": CONTEXT_LEDGER, "Delta0": delta0, "presentation": presentation,
            "bridge": receipt["bridge"], "evaluator": evaluator,
            "input": source_input, "external_manifest": manifest,
            "resource": receipt.get("resource"),
            "grade": "CROSS_CHECKED"}


class Task179Monitor:
    """Adapter exposing the pinned task179 monitor ABI on one global meter."""
    def __init__(self, args: argparse.Namespace) -> None:
        self.meter = ResourceMeter()
        self.started = time.monotonic()
        self.phase = "task232"
        self.limits = {"wall_seconds": float(getattr(args, "seconds", 14400)),
                       "rss_bytes": int(getattr(args, "rss_bytes", 8000000000)),
                       "boundary_pairs": int(getattr(args, "boundary_pairs", 1000000)),
                       "fibre_scans": int(getattr(args, "fibre_scans", 1000000)),
                       "candidate_words": int(getattr(args, "candidate_words", 1000000)),
                       "retained_columns": int(getattr(args, "retained_columns", 100000)),
                       "checkpoint_bytes": int(getattr(args, "checkpoint_bytes", 100000000)),
                       "oracle_rounds": int(getattr(args, "oracle_rounds", 1000000)),
                       "global_roster": Q0_ORDER * 243}
        self.counters = {key: 0 for key in ("boundary_pairs", "fibre_scans",
                                             "candidate_words", "retained_columns",
                                             "checkpoint_bytes", "oracle_rounds",
                                             "global_roster")}

    def check(self, phase: str) -> None:
        self.phase = phase
        elapsed = time.monotonic() - self.started
        if elapsed > self.limits["wall_seconds"]:
            raise ResourceStop("phase=%s:cap=wall_seconds:value=%s:limit=%s" %
                               (phase, int(elapsed),
                                self.limits["wall_seconds"]))
        rss = self.rss()
        if rss and rss > self.limits["rss_bytes"]:
            raise ResourceStop("phase=%s:cap=rss_bytes:value=%s:limit=%s" %
                               (phase, rss, self.limits["rss_bytes"]))

    @staticmethod
    def rss() -> int:
        try:
            import resource
            value = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
            return value if sys.platform == "darwin" else value * 1024
        except (ImportError, AttributeError):
            return 0

    def bump(self, name: str, amount: int = 1, phase: str | None = None) -> None:
        self.phase = phase or self.phase
        self.counters[name] = self.counters.get(name, 0) + int(amount)
        if name in self.limits and self.counters[name] > self.limits[name]:
            raise ResourceStop("phase=%s:cap=%s:value=%s:limit=%s" %
                               (self.phase, name, self.counters[name], self.limits[name]))
        if self.counters[name] % 4096 == 0:
            self.check(self.phase)

    def public(self) -> dict[str, Any]:
        return {"phase": self.phase, "elapsed_seconds": time.monotonic() - self.started,
                "rss_bytes": self.rss(),
                "limits": self.limits, "counters": self.counters,
                "single_process": True}


def load_pinned_module(path: str, size: int, expected: str, name: str) -> Any:
    raw_path = ROOT / path
    input_require(raw_path.is_file(), "missing pinned arithmetic:" + path)
    raw = raw_path.read_bytes()
    input_require(len(raw) == size and hashlib.sha256(raw).hexdigest() == expected,
                  "pinned arithmetic identity:" + path)
    spec = importlib.util.spec_from_file_location(name, raw_path)
    input_require(spec is not None and spec.loader is not None, "arithmetic loader")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def task232_contexts(old: Any) -> list[dict[str, Any]]:
    """Frozen ten substitutions in the right-to-left paper-product order."""
    x, y = [1], [3]
    pp = old.pp_words
    z = old.inv_word(pp([x, y]))
    u = old.inv_word(pp([y, x]))
    e3 = [(x, y), (x, z), (y, z), (u, x), (u, y)]
    e4 = [([4], [6]), (pp([[1], [2]]), pp([[5], [6]])),
          ([1], [4]), (pp([[2], [4]]), [6]),
          ([1], pp([[4], [5]]))]
    answer = []
    for i, (left, right) in enumerate(e3 + e4):
        answer.append({"index": i, "type": "E3" if i < 5 else "E4",
                       "context_id": CONTEXT_IDS[i], "tag": CONTEXT_TAGS[i],
                       "left": list(left), "right": list(right),
                       "block": 1 if i < 5 else 3})
    input_require([(x["type"], x["context_id"]) for x in answer] ==
                  list(zip(CONTEXT_TYPES, CONTEXT_IDS)), "task232 context ledger")
    input_require(answer[0]["left"] == [1] and answer[0]["right"] == [3] and
                  answer[7]["left"] == [1] and answer[7]["right"] == [4],
                  "task232 exact source substitutions")
    return answer


def context_successor_value(p179: Any, runtime: dict[str, Any],
                            context: dict[str, Any], source_word: list[int]) -> dict[str, Any]:
    value = context_affine_value(p179, runtime, context, source_word)
    p179.require(value["roof_identity"], "nontrivial roof reduction")
    return value


def context_affine_value(p179: Any, runtime: dict[str, Any],
                         context: dict[str, Any], source_word: list[int]) -> dict[str, Any]:
    old = runtime["old"]
    quotient = runtime["e3"] if context["type"] == "E3" else runtime["e4"]
    pb_word = old.f2_substitute(source_word, context["left"], context["right"])
    gradient, roof_value = old.fox_gradient_without_sections(pb_word, quotient)
    raw: dict[str, int] = {}
    for (component, value), coefficient in gradient.items():
        blob = p179.element_blob(runtime, value).hex()
        key = "%d:%d:%s" % (context["index"], int(component), blob)
        raw[key] = (raw.get(key, 0) + int(coefficient)) % 3
    raw = {key: value for key, value in raw.items() if value}
    return {"context": context["index"], "type": context["type"],
            "context_id": context["context_id"], "source_word": list(source_word),
            "substituted_word": list(pb_word),
            "roof_identity": roof_value == quotient.identity,
            "base_blob": p179.element_blob(runtime, roof_value).hex(),
            "chain": raw}


class ActualBoundaryOracle:
    """Lazy complete translated-boundary oracle over the ten tagged blocks."""
    def __init__(self, p179: Any, runtime: dict[str, Any], monitor: Task179Monitor):
        self.p179, self.runtime, self.monitor = p179, runtime, monitor
        self.boundary = Echelon()
        self.boundary_records: list[dict[str, Any]] = []
        self.k_rows: list[dict[str, int]] = []

    @staticmethod
    def split_key(key: str) -> tuple[int, int, bytes]:
        coord, component, blob = key.split(":", 2)
        return int(coord), int(component), bytes.fromhex(blob)

    def project(self, dual: dict[str, int], coordinate: int) -> dict[bytes, int]:
        block = 1 if coordinate < 5 else 3
        answer: dict[bytes, int] = {}
        for key, coefficient in dual.items():
            coord, component, blob = self.split_key(key)
            if coord == coordinate:
                pkey = self.p179.row_key(block, component, blob)
                answer[pkey] = (answer.get(pkey, 0) + coefficient) % 3
        return {key: value for key, value in answer.items() if value}

    def lift_row(self, row: dict[bytes, int], coordinate: int) -> dict[str, int]:
        answer: dict[str, int] = {}
        for key, coefficient in row.items():
            block, component, blob = self.p179.decode_row_key(key)
            own = "%d:%d:%s" % (coordinate, component, blob.hex())
            answer[own] = (answer.get(own, 0) + coefficient) % 3
        return {key: value for key, value in answer.items() if value}

    def find_active_boundary(self, dual: dict[str, int]) -> dict[str, Any] | None:
        for coordinate in range(10):
            projected = self.project(dual, coordinate)
            if not projected:
                continue
            active = self.p179.boundary_oracle(self.runtime, projected, self.monitor)
            if active is not None:
                row = self.lift_row(active["row"], coordinate)
                return {"row": row, "coordinate": coordinate,
                        "provenance": active["provenance"]}
        return None

    def query(self, candidate: dict[str, int], query_id: str) -> dict[str, Any]:
        while True:
            self.monitor.bump("oracle_rounds", 1, "complete_boundary_membership")
            total = Echelon()
            for pivot in self.boundary.pivots:
                total.insert(self.boundary.rows[pivot], "B:" + pivot)
            for index, row in enumerate(self.k_rows):
                total.insert(row, "K:" + str(index))
            remainder, coefficients = total.reduce(candidate)
            if not remainder:
                boundary_coefficients = {k: v for k, v in coefficients.items() if k.startswith("B:")}
                k_coefficients = {k: v for k, v in coefficients.items() if k.startswith("K:")}
                return {"member": True, "boundary_coefficients": boundary_coefficients,
                        "k_coefficients": k_coefficients, "replay": True,
                        "pivots": list(total.pivots)}
            dual = total.dual(candidate)
            active = self.find_active_boundary(dual)
            if active is not None:
                row = active["row"]
                inserted = self.boundary.insert(row, "B:%d" % len(self.boundary_records))
                self.monitor.bump("retained_columns", 1, "translated_boundary_insert")
                self.boundary_records.append({"query": query_id,
                                              "coordinate": active["coordinate"],
                                              "row": row, "inserted": inserted is not None,
                                              "provenance": active["provenance"],
                                              "dual": dual})
                continue
            pairing = sum(int(a) * int(dual.get(k, 0)) for k, a in candidate.items()) % 3
            require(pairing != 0, "complete negative dual pairing")
            pivot = min(remainder)
            scale = 1 if remainder[pivot] == 1 else 2
            ancestry = {key: (scale * value) % 3
                        for key, value in coefficients.items()
                        if (scale * value) % 3}
            ancestry[query_id] = scale
            return {"member": False, "dual": dual, "pairing": pairing,
                    "remainder": remainder, "normalized": row_scale(remainder, scale),
                    "normalization_scale": scale, "reduction_coefficients": coefficients,
                    "boundary_coefficients": {k: v for k, v in ancestry.items()
                                               if k.startswith("B:")},
                    "k_coefficients": {k: v for k, v in ancestry.items()
                                        if k.startswith("K:")},
                    "normalized_ancestry": ancestry,
                    "full_zero_correlation": True, "replay": True,
                    "pivots": list(total.pivots)}


def actual_action(p179: Any, runtime: dict[str, Any], contexts: list[dict[str, Any]],
                  row: dict[str, int], letter: int) -> dict[str, int]:
    """Conjugate a tagged kernel row by a marked source generator."""
    answer: dict[str, int] = {}
    for coordinate in range(10):
        context = contexts[coordinate]
        actor = context_affine_value(p179, runtime, context, [1 if abs(letter) == 1 else 2])
        quotient = runtime["e3"] if context["type"] == "E3" else runtime["e4"]
        actor_value = p179.unpack_element(runtime, bytes.fromhex(actor["base_blob"]), context["block"])
        if letter < 0:
            actor_value = quotient.inverse(actor_value)
        for key, coefficient in row.items():
            coord, component, blob = ActualBoundaryOracle.split_key(key)
            if coord != coordinate:
                continue
            value = p179.unpack_element(runtime, blob, context["block"])
            moved = quotient.mul(actor_value, value)
            moved_key = "%d:%d:%s" % (coord, component,
                                       p179.element_blob(runtime, moved).hex())
            answer[moved_key] = (answer.get(moved_key, 0) + coefficient) % 3
    return {key: value for key, value in answer.items() if value}


def actual_defect(p179: Any, runtime: dict[str, Any], contexts: list[dict[str, Any]],
                  source_word: list[int], monitor: Task179Monitor) -> tuple[dict[str, int], list[dict[str, Any]]]:
    row: dict[str, int] = {}
    values: list[dict[str, Any]] = []
    for context in contexts:
        monitor.bump("candidate_words", 1, "ten_typed_successor_evaluation")
        value = context_successor_value(p179, runtime, context, source_word)
        values.append(value)
        row = row_add(row, value["chain"])
    return row, values


def evaluate_roof_trivial_source(p179: Any, runtime: dict[str, Any],
                                 contexts: list[dict[str, Any]],
                                 oracle: ActualBoundaryOracle,
                                 source_word: list[int],
                                 monitor: Task179Monitor) -> dict[str, Any]:
    """Exported word-bearing evaluator for a supplied roof-trivial source."""
    defect, values = actual_defect(p179, runtime, contexts, source_word, monitor)
    require(all(value["roof_identity"] for value in values),
            "evaluator requires ten roof identities")
    membership = oracle.query(defect, "EVAL:" + digest(source_word))
    return {"schema": SCHEMA + "/evaluator/v1", "source_word": list(source_word),
            "successor_values": values, "defect": defect,
            "membership": membership,
            "basis_coordinates": membership.get("k_coefficients", {}),
            "complete_boundary_receipt": membership}


def combine_term_ancestry(coefficients: dict[str, int], terms: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    answer: list[dict[str, Any]] = []
    for source_id, coefficient in sorted(coefficients.items()):
        for term in terms.get(source_id, []):
            item = dict(term)
            item["coefficient"] = (int(item.get("coefficient", 1)) * int(coefficient)) % 3
            if item["coefficient"]:
                answer.append(item)
    return answer


def boundary_value_from_coefficients(oracle: ActualBoundaryOracle,
                                     coefficients: dict[str, int]) -> dict[str, int]:
    """Materialize the complete retained-boundary part of a reduction."""
    answer: dict[str, int] = {}
    for source_id, coefficient in sorted(coefficients.items()):
        if not source_id.startswith("B:") or not coefficient:
            continue
        pivot = source_id[2:]
        require(pivot in oracle.boundary.rows, "boundary ancestry pivot")
        answer = row_add(answer, oracle.boundary.rows[pivot], int(coefficient))
    return answer


def expanded_boundary_value(oracle: ActualBoundaryOracle,
                            coefficients: dict[str, int],
                            prior: dict[str, dict[str, int]]) -> dict[str, int]:
    answer = boundary_value_from_coefficients(oracle, coefficients)
    for source_id, coefficient in sorted(coefficients.items()):
        if source_id.startswith("K:") and coefficient:
            answer = row_add(answer, prior.get(source_id, {}), int(coefficient))
    return answer


def build_actual_kernel(p179: Any, runtime: dict[str, Any], authenticated: dict[str, Any],
                        args: argparse.Namespace,
                        monitor: Task179Monitor | None = None) -> dict[str, Any]:
    monitor = monitor or Task179Monitor(args)
    contexts = task232_contexts(runtime["old"])
    oracle = ActualBoundaryOracle(p179, runtime, monitor)
    rows = authenticated["presentation"]["rows"]
    k_terms: dict[str, list[dict[str, Any]]] = {}
    k_boundary_values: dict[str, dict[str, int]] = {}
    basis_rows: list[dict[str, Any]] = []
    queue: list[int] = []
    relation_receipts: list[dict[str, Any]] = []
    for ordinal, presentation_row in enumerate(rows, 1):
        monitor.bump("candidate_words", 1, "presentation_relator")
        source_word = [int(x) for x in presentation_row["word"]]
        defect, values = actual_defect(p179, runtime, contexts, source_word, monitor)
        query = oracle.query(defect, "R:%d" % ordinal)
        relation_receipts.append({"ordinal": ordinal, "source_word": source_word,
                                  "values": values, "defect": defect, "membership": query})
        if query["member"]:
            continue
        source_id = "K:%d" % len(basis_rows)
        query = oracle.query(defect, source_id)
        require(query["member"] is False, "defect changed during insertion")
        normalized = query["normalized"]
        oracle.k_rows.append(normalized)
        terms = [{"relator": ordinal, "conjugator": [],
                  "source_word": list(source_word),
                  "coefficient": query["normalization_scale"]}]
        coefficients = dict(query["normalized_ancestry"])
        coefficients.pop(source_id, None)
        terms.extend(combine_term_ancestry(coefficients, k_terms))
        boundary_value = expanded_boundary_value(oracle, coefficients, k_boundary_values)
        require(boundary_value == row_add(normalized,
                                          row_scale(defect, -query["normalization_scale"])),
                "initial boundary reduction replay")
        k_terms[source_id] = terms
        k_boundary_values[source_id] = boundary_value
        basis_rows.append({"source_id": source_id, "row": normalized,
                           "raw_defect": defect, "membership": query,
                           "ancestry": terms, "boundary_value": boundary_value,
                           "boundary_coefficients": {k: v for k, v in coefficients.items()
                                                       if k.startswith("B:")},
                           "prior_k_coefficients": {k: v for k, v in coefficients.items()
                                                     if k.startswith("K:")},
                           "literal_source_word": source_word, "source_word": source_word,
                           "delta1_value": normalized, "delta0_identity": all(
                               item.get("roof_identity") is True for item in values),
                           "values": values})
        queue.append(len(basis_rows) - 1)
        monitor.bump("accepted_rank", 1, "kernel_rank_raise")
    cursor = 0
    while cursor < len(queue):
        basis_index = queue[cursor]
        cursor += 1
        source = basis_rows[basis_index]["row"]
        for letter in (1, -1, 2, -2):
            monitor.bump("candidate_words", 1, "generator_translate")
            translated = actual_action(p179, runtime, contexts, source, letter)
            source_id = "T:%d:%d" % (basis_index, letter)
            query = oracle.query(translated, source_id)
            if query["member"]:
                continue
            normalized = query["normalized"]
            oracle.k_rows.append(normalized)
            terms = []
            for term in basis_rows[basis_index]["ancestry"]:
                item = dict(term)
                item["conjugator"] = [letter] + list(item.get("conjugator", []))
                item["conjugated_word"] = ([letter] +
                                            list(item.get("conjugated_word",
                                                          item.get("source_word", []))) +
                                            [-letter])
                item["coefficient"] = (int(item.get("coefficient", 1)) *
                                        int(query["normalization_scale"])) % 3
                terms.append(item)
            coefficients = dict(query["normalized_ancestry"])
            coefficients.pop(source_id, None)
            terms.extend(combine_term_ancestry(coefficients, k_terms))
            source_word = word_from_ancestry(terms)
            base_boundary = row_scale(actual_action(
                p179, runtime, contexts,
                basis_rows[basis_index].get("boundary_value", {}), letter),
                query["normalization_scale"])
            boundary_value = row_add(base_boundary,
                                     expanded_boundary_value(oracle, coefficients,
                                                            k_boundary_values))
            require(boundary_value == row_add(normalized,
                                              row_scale(translated,
                                                        -query["normalization_scale"])),
                    "translate boundary reduction replay")
            k_terms[source_id] = terms
            k_boundary_values[source_id] = boundary_value
            basis_rows.append({"source_id": source_id, "row": normalized,
                               "raw_defect": translated, "membership": query,
                               "ancestry": terms, "boundary_value": boundary_value,
                               "boundary_coefficients": {k: v for k, v in coefficients.items()
                                                           if k.startswith("B:")},
                               "prior_k_coefficients": {k: v for k, v in coefficients.items()
                                                         if k.startswith("K:")},
                               "literal_source_word": None, "source_word": source_word,
                               "word_ancestry": terms, "delta1_value": normalized,
                               "delta0_identity": True, "values": None})
            queue.append(len(basis_rows) - 1)
            monitor.bump("accepted_rank", 1, "kernel_rank_raise")
    require(cursor == len(queue), "actual queue exhaustion")
    initial_replay_receipts = []
    for relation in relation_receipts:
        replay = oracle.query(relation["defect"], "replay:R:%d" % relation["ordinal"])
        require(replay["member"] is True, "initial defect terminal containment")
        initial_replay_receipts.append({"ordinal": relation["ordinal"],
                                       "row": relation["defect"],
                                       "membership": replay})
    translate_receipts = []
    for index, basis in enumerate(basis_rows):
        for letter in (1, -1, 2, -2):
            moved = actual_action(p179, runtime, contexts, basis["row"], letter)
            replay = oracle.query(moved, "replay:T:%d:%d" % (index, letter))
            require(replay["member"] is True, "translate terminal containment")
            translate_receipts.append({"basis": index, "letter": letter,
                                       "row": moved, "membership": replay})
    action_matrices: dict[str, dict[str, dict[str, int]]] = {str(letter): {}
                                                              for letter in (1, -1, 2, -2)}
    for receipt in translate_receipts:
        action_matrices[str(receipt["letter"])] [str(receipt["basis"])] = dict(
            receipt["membership"].get("k_coefficients", {}))
    rank = len(basis_rows)
    for letter in action_matrices:
        require(len(action_matrices[letter]) == rank,
                "complete source-generator action matrix")

    def compose(left: dict[str, dict[str, int]],
                right: dict[str, dict[str, int]]) -> dict[str, dict[str, int]]:
        answer: dict[str, dict[str, int]] = {}
        for source in range(rank):
            column: dict[str, int] = {}
            for middle, coefficient in right[str(source)].items():
                for target, value in left.get(middle[2:], {}).items():
                    column[target] = (column.get(target, 0) +
                                      int(coefficient) * int(value)) % 3
            answer[str(source)] = {k: v for k, v in column.items() if v}
        return answer

    inverse_products: dict[str, bool] = {}
    for positive, negative in (("1", "-1"), ("2", "-2")):
        identity = {str(i): {"K:" + str(i): 1} for i in range(rank)}
        require(compose(action_matrices[positive], action_matrices[negative]) == identity and
                compose(action_matrices[negative], action_matrices[positive]) == identity,
                "inverse source-generator action matrices")
        inverse_products[positive + negative] = True
        inverse_products[negative + positive] = True
    require(all(row_add(row, row, 2) == {} for row in (item["row"] for item in basis_rows)),
            "source-word order three")
    require(all(row_add(row_add(a, b), a, 2) == b
                for a in (item["row"] for item in basis_rows)
                for b in (item["row"] for item in basis_rows)),
            "source-word pairwise commutation")
    require(all(ancestry_value_actual(p179, runtime, contexts, item["ancestry"], relation_receipts,
                                      item.get("boundary_value", {})) == item["row"]
                 for item in basis_rows), "literal ancestry replay")
    return {"rank": rank, "basis": basis_rows, "queue_actions": len(queue),
            "queue_cursor": cursor, "initial_defects": relation_receipts,
            "initial_replay_receipts": initial_replay_receipts,
            "translate_receipts": translate_receipts,
            "action_matrices": action_matrices,
            "inverse_products": inverse_products,
            "order_three": True, "pairwise_commutation": True,
            "boundary_records": oracle.boundary_records,
            "boundary_rank": len(oracle.boundary.pivots),
            "order": 3 ** rank, "nilpotence_bound": 2 * rank + 1,
            "basis_digest": digest([item["row"] for item in basis_rows]),
            "evaluator": {"schema": SCHEMA + "/evaluator/v1",
                          "entry_point": "evaluate_roof_trivial_source",
                          "source_encoding": "literal strict signed F2 word",
                          "returns": ["successor_values", "basis_coordinates",
                                      "complete_boundary_receipt"]},
            "contexts": contexts, "resource": monitor.public(),
            "_oracle": oracle, "_contexts": contexts,
            "complete": True}


def evaluate_k_z(p179: Any, runtime: dict[str, Any], kernel: dict[str, Any],
                 contexts: list[dict[str, Any]], monitor: Task179Monitor) -> dict[str, Any]:
    """Construct the v247 anchor using the built-in H2(9) quotient."""
    oracle = kernel.get("_oracle")
    input_require(isinstance(oracle, ActualBoundaryOracle), "A4_BOUNDARY_ORACLE_NOT_PROVIDED")
    projections: list[int] = []
    basis_receipts: list[dict[str, Any]] = []
    for index, basis in enumerate(kernel.get("basis", [])):
        source_word = basis.get("source_word")
        input_require(type(source_word) is list and source_word,
                      "A4_BASIS_SOURCE_WORD_NOT_PROVIDED")
        d1_value = h2_signed_word(source_word)
        input_require(d1_value[0:2] == (0, 0) and d1_value[2] in (0, 3, 6),
                      "A4_BASIS_D1_NOT_CENTRAL")
        exponent = (d1_value[2] // 3) % 3
        defect, roof_values = actual_defect(p179, runtime, contexts, source_word, monitor)
        membership = oracle.query(defect, "A4:K:%d" % index)
        input_require(membership.get("member") is True,
                      "A4_BASIS_K_MEMBERSHIP")
        projections.append(exponent)
        basis_receipts.append({"index": index, "source_word": list(source_word),
                               "d1_value": list(d1_value), "projected_exponent": exponent,
                               "roof_values": roof_values,
                               "delta0_identity": all(item.get("roof_identity") is True
                                                       for item in roof_values),
                               "delta1_k_membership": True,
                               "membership": membership, "replay": True})
    active = [i for i, exponent in enumerate(projections) if exponent]
    input_require(bool(active), "A4_D1_PROJECTION_ZERO")
    selected = active[0]
    scalar = 1 if projections[selected] == 1 else 2
    selected_word = basis_receipts[selected]["source_word"]
    source_word = free_reduce_word(selected_word * scalar)
    d1_value = h2_signed_word(source_word)
    input_require(d1_value == (0, 0, 3), "A4_SELECTED_D1_TARGET")
    selected_defect, roof_values = actual_defect(p179, runtime, contexts, source_word, monitor)
    selected_membership = oracle.query(selected_defect, "A4:K:z")
    input_require(selected_membership.get("member") is True,
                  "A4_SELECTED_K_MEMBERSHIP")
    input_require(all(item.get("roof_identity") is True for item in roof_values),
                  "A4_SELECTED_DELTA0_IDENTITY")
    return {"basis_projections": projections, "basis_d1_values": [item["d1_value"]
                       for item in basis_receipts], "basis_receipts": basis_receipts,
            "projected_coordinate": projections, "selected_index": selected,
            "inverse_scalar": scalar, "word_exponent": scalar,
            "source_word": source_word, "roof_values": roof_values,
            "delta0_identity": True, "delta1_k_membership": True,
            "d1_z0": list(d1_value), "basis_coefficients": {str(selected): scalar},
            "membership": selected_membership, "replay": True}


def load_checkpoint(path_text: str | None) -> dict[str, Any] | None:
    if not path_text:
        return None
    path = Path(path_text)
    input_require(not path.is_absolute() and path.as_posix().startswith("ci/in/"),
                  "RESUME_GUARDED_PATH")
    obj = json.loads((ROOT / path).read_text(encoding="ascii"))
    body = dict(obj); claimed = body.pop("self_digest_sha256", None)
    input_require(obj.get("schema") == SCHEMA + "/checkpoint/v1" and
                  obj.get("sealed") is True and claimed == digest(body),
                  "RESUME_CHECKPOINT_SEAL")
    return obj


def ancestry_value_actual(p179: Any, runtime: dict[str, Any], contexts: list[dict[str, Any]],
                          terms: list[dict[str, Any]], receipts: list[dict[str, Any]],
                          boundary_value: dict[str, int] | None = None) -> dict[str, int]:
    answer: dict[str, int] = {}
    by_relator = {int(item["ordinal"]): item["defect"] for item in receipts}
    for term in terms:
        value = dict(by_relator[int(term["relator"])])
        for letter in term.get("conjugator", []):
            value = actual_action(p179, runtime, contexts, value, int(letter))
        answer = row_add(answer, value, int(term.get("coefficient", 1)))
    return row_add(answer, boundary_value or {})


def production(args: argparse.Namespace) -> dict[str, Any]:
    started = time.monotonic()
    meter = ResourceMeter()
    try:
        resume = load_checkpoint(getattr(args, "resume", None))
        task198 = authenticate_task198(args.task198_receipt, args.task198_manifest,
                                       args.task198_producer_attestation,
                                       args.task198_checker_attestation)
    except InputStop as exc:
        return envelope(UNKNOWN_INPUT, str(exc), {"phase": "task198_authentication"}, started, meter)
    successor_monitor: Task179Monitor | None = None
    try:
        p179 = load_pinned_module(*TASK179_PIN, "d232_task179")
        input_require(hasattr(p179, "build_runtime") and
                      hasattr(p179, "boundary_oracle") and
                      hasattr(p179, "translated_boundary"),
                      "TASK179_AFFINE_API")
        successor_monitor = Task179Monitor(args)
        runtime = p179.build_runtime(successor_monitor)
        input_require(hasattr(runtime.get("old"), "fox_gradient_without_sections") and
                      hasattr(runtime.get("old"), "f2_substitute"),
                      "TASK179_FOX_SUBSTITUTION_API")
        kernel = build_actual_kernel(p179, runtime, task198, args, successor_monitor)
        kernel["k_z_receipt"] = evaluate_k_z(p179, runtime, kernel,
                                              kernel.pop("_contexts"), successor_monitor)
        kernel["boundary_records"] = kernel["_oracle"].boundary_records
        kernel["boundary_rank"] = len(kernel["_oracle"].boundary.pivots)
        kernel.pop("_oracle", None)
        kernel["resource"] = successor_monitor.public()
        meter.merge_snapshot(kernel["resource"])
        if resume is not None:
            input_require(resume.get("rank_zero_replay") is True and
                          type(resume.get("accepted_rows")) is list and
                          type(resume.get("oracle_transcript")) is list,
                          "RESUME_REPLAY_STATE")
        input_require(kernel["complete"] and kernel["queue_cursor"] == kernel["queue_actions"],
                      "A4_QUEUE_NOT_EXHAUSTED")
        result = {"task198": task198, "kernel": kernel,
                  "presentation_rows": PRESENTATION_ROWS, "word_bearing": True,
                  "complete_presentation": True,
                  "A4_presentation_input": 1, "A4_invariant_closure": 1,
                  "A4_word_bearing_K": 1,
                  "forbidden_downstream": {"d1": False, "e1": False,
                  "pointed_multiplier": False, "endpoint": False,
                  "lift": False, "fake": False, "Ihara_witness": False}}
        return envelope("COMPLETE", ISO, result, started, meter)
    except ResourceStop as exc:
        if successor_monitor is not None:
            meter.merge_snapshot(successor_monitor.public())
        checkpoint = None
        if getattr(args, "checkpoint", None):
            cp = Path(args.checkpoint)
            input_require(not cp.is_absolute() and cp.as_posix().startswith("ci/out/"), "CHECKPOINT_PATH")
            payload = {"schema": SCHEMA + "/checkpoint/v1", "sealed": True,
                       "resource_stop": str(exc), "input_identity": task198,
                       "rank_zero_replay": True, "accepted_rows": [],
                       "queue_cursor": 0, "oracle_transcript": [],
                       "caps": vars(args)}
            payload["self_digest_sha256"] = digest(payload)
            out = ROOT / cp; out.parent.mkdir(parents=True, exist_ok=True)
            out.write_bytes(canonical(payload)); checkpoint = {"path": cp.as_posix(), "sealed": True}
        return envelope(UNKNOWN_RESOURCE, str(exc),
                        {"phase": "successor_kernel", "resource_stop": True,
                         "checkpoint": checkpoint}, started, meter)
    except (InputStop, RuntimeError, OSError, ValueError) as exc:
        if successor_monitor is not None:
            meter.merge_snapshot(successor_monitor.public())
        return envelope(UNKNOWN_INPUT, str(exc),
                        {"phase": "successor_kernel"}, started, meter)


def envelope(status: str, reason: str, result: Any, started: float,
             meter: ResourceMeter | None = None,
             terminal: str | None = None) -> dict[str, Any]:
    counters = {} if meter is None else dict(meter.counters)
    counters.setdefault("wall_seconds", time.monotonic() - started)
    counters.setdefault("rss_bytes", 0)
    value = {"schema": SCHEMA, "status": status, "terminal": terminal or status,
             "reason": reason, "result": result,
             "resource": counters,
             "A4_presentation_input": 0, "A4_invariant_closure": 0,
             "A4_word_bearing_K": 0, "d1": False, "e1": False,
             "pointed_multiplier": False, "endpoint": False, "lift": False,
             "fake": False, "Ihara_witness": False}
    value["self_digest_sha256"] = digest(value)
    return value


def load_json(path: str) -> dict[str, Any]:
    raw = Path(path).read_bytes()
    obj = json.loads(raw.decode("ascii"))
    input_require(type(obj) is dict, "fixture object")
    return obj


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--fixture")
    parser.add_argument("--output")
    parser.add_argument("--task198-receipt", default="ci/in/d972_r07_seven_context_roof_presentation_v1.json")
    parser.add_argument("--task198-manifest", default="ci/in/d972_r07_seven_context_roof_presentation_v1.manifest.json")
    parser.add_argument("--task198-producer-attestation", default="ci/in/d972_r07_seven_context_roof_presentation_v1.producer.attestation.txt")
    parser.add_argument("--task198-checker-attestation", default="ci/in/d972_r07_seven_context_roof_presentation_v1.checker.attestation.txt")
    parser.add_argument("--seconds", type=int, default=14400)
    parser.add_argument("--rss-bytes", type=int, default=8000000000)
    parser.add_argument("--boundary-pairs", type=int, default=1000000)
    parser.add_argument("--fibre-scans", type=int, default=1000000)
    parser.add_argument("--candidate-words", type=int, default=1000000)
    parser.add_argument("--retained-columns", type=int, default=100000)
    parser.add_argument("--checkpoint-bytes", type=int, default=100000000)
    parser.add_argument("--oracle-rounds", type=int, default=1000000)
    parser.add_argument("--checkpoint")
    parser.add_argument("--resume")
    args = parser.parse_args(argv)
    try:
        if args.selftest:
            fixture = load_json(args.fixture) if args.fixture else None
            result = selftest(fixture)
            if args.output:
                output = Path(args.output)
                input_require(not output.is_absolute() and output.as_posix().startswith("ci/out/"), "SELFTEST_OUTPUT_PATH")
                output = ROOT / output
                input_require(not output.exists(), "SELFTEST_STALE_OUTPUT")
                output.parent.mkdir(parents=True, exist_ok=True)
                output.write_bytes(canonical(result))
            print("R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V1_PRODUCER_SELFTEST_PASS")
            return 0
        result = production(args)
        if args.output:
            output = Path(args.output)
            input_require(not output.is_absolute() and output.as_posix().startswith("ci/out/"), "OUTPUT_PATH")
            output = ROOT / output
            input_require(not output.exists(), "OUTPUT_STALE")
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_bytes(canonical(result))
        print("R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V1_PRODUCER_TERMINAL " + result["terminal"])
        return 0
    except (InputStop, RuntimeError, OSError, json.JSONDecodeError) as exc:
        print("R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V1_PRODUCER_NONPOSITIVE reason=" + str(exc))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
