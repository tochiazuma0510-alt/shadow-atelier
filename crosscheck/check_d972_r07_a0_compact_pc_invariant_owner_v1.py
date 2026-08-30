#!/usr/bin/env python3
"""Independent checker for the compact A0 presentation and v400 quotient.

The producer is data only: this module never imports it.  For conclusive A0
results the checker restores the frozen checker arithmetic with a minimal,
SHA-pinned roof authority, reconstructs the shared B3/B4 boundary quotients,
closes the 44 compact occurrence seeds under all four F2 actors, and then
checks a literal MEMBER preimage or a canonical NONMEMBER functional.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import struct
import types
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Iterable, Sequence


ROOT = Path(__file__).resolve().parents[1]
JOINT = Path("ci/b345_157ee_artifacts_32359956713/d972_b345_joint_kernel_qstar_closure_v1.json")
Q3 = Path("ci/b345_157ee_artifacts_32359956713/d972_b345_q3_chief_v1.json")
ROOF = Path("ci/in/d972_r07_seven_context_roof_presentation_v1.json")
ACCEPTANCE = Path("ci/in/d972_r07_seven_context_roof_presentation_v1.acceptance_v2.json")

DATA_PINS = {
    str(JOINT): (2166036, "1c3ad7a7124cee152eb40968cf212c14641a9f8720063c85f70533864898d0df"),
    str(Q3): (231570, "3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72"),
    str(ROOF): (31017244, "82f7955580039f2a0271896c928515d26996f636d8e73231331da6a37f6b19f5"),
    str(ACCEPTANCE): (2722, "cc8c16c8ad8f2d094868f0897bcca2a98adba75c18bf7ff397f0da67fd233ea4"),
}
SOURCE_PINS = {
    "bootstrap": ("crosscheck/check_d972_r07_zero_base_a5_a6_compiler_v4.py", 45942,
                  "cc88aeed18c4f14481971595ab22070720f68ce3fbe48f1057ecd89b610178aa"),
    "occurrence": ("crosscheck/check_d972_r07_crel_occurrence_closure_v2.py", 33839,
                   "a88fc4c7777a1fdc9d5ce9365807cd7caed58b2ef0b6d7e0d75a979de4ace26c"),
    "raw": ("crosscheck/check_d972_r07_all_seven_raw_bridge_preflight_v1.py", 88503,
            "0b45c3daa1db6cad63d434170c65d0dbfa928efc51543b881dc0aa2e3a0f1fce"),
}
G760_SHA256 = "518f09820b8d7baee6b58ebf366cebf7b02a9a945cd1350cf8c701a4e6bc2b4d"
SCHEMA = "d972-r07-a0-compact-pc-invariant-owner/v1"
ACTION_LETTERS = (1, -1, 2, -2)
LEGACY_ROWS = 6441
MAX_FRONTIER = 200000


def canon(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canon(value)).hexdigest()


def digest_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def require(condition: bool, message: str) -> None:
    if condition is not True:
        raise RuntimeError(message)


def pinned_bytes(relative: str | Path, size: int, sha256: str) -> bytes:
    path = ROOT / relative
    require(path.is_file() and not path.is_symlink(), "pin_missing:" + str(relative))
    raw = path.read_bytes()
    require(len(raw) == size and digest_bytes(raw) == sha256, "pin_mismatch:" + str(relative))
    return raw


def load_data(relative: Path) -> dict[str, Any]:
    raw = pinned_bytes(relative, *DATA_PINS[str(relative)])
    try:
        value = json.loads(raw.decode("ascii"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise RuntimeError("json:" + str(relative)) from exc
    require(type(value) is dict, "object:" + str(relative))
    return value


def load_source(label: str) -> types.ModuleType:
    relative, size, sha256 = SOURCE_PINS[label]
    raw = pinned_bytes(relative, size, sha256)
    module = types.ModuleType("r07_a0_checker_" + label)
    module.__file__ = str(ROOT / relative)
    module.__package__ = None
    exec(compile(raw, relative, "exec"), module.__dict__, module.__dict__)
    return module


def acceptance_ok(value: dict[str, Any]) -> bool:
    verdict = value.get("checker_verdict", {})
    member = value.get("receipt", {})
    return (value.get("accepted") is True and value.get("independent") is True and
            value.get("accepted_receipt_basename") == ROOF.name and
            member.get("bytes") == DATA_PINS[str(ROOF)][0] and
            member.get("sha256") == DATA_PINS[str(ROOF)][1] and
            verdict.get("accepted") is True and verdict.get("independent") is True and
            verdict.get("receipt_terminal") == "ROOF_BRIDGE_ISOMORPHISM")


def unpack(field: dict[str, Any], encoding: str) -> list[int]:
    try:
        raw = base64.b64decode(field["base64"], validate=True)
    except Exception as exc:
        raise RuntimeError("packed_base64") from exc
    require(field.get("encoding") == encoding and digest_bytes(raw) == field.get("sha256"),
            "packed")
    if encoding == "u16-le":
        require(len(raw) % 2 == 0, "packed_u16_width")
        answer = [struct.unpack_from("<H", raw, index)[0]
                  for index in range(0, len(raw), 2)]
    else:
        answer = list(raw)
    require(len(answer) == field.get("count") and digest(answer) == field.get("decoded_sha256"),
            "decoded")
    return answer


def reduce_word(word: Iterable[int]) -> list[int]:
    answer: list[int] = []
    for raw in word:
        letter = int(raw)
        require(type(raw) is int and letter in ACTION_LETTERS, "word_letter")
        if answer and answer[-1] == -letter:
            answer.pop()
        else:
            answer.append(letter)
    return answer


def inverse_word(word: Sequence[int]) -> list[int]:
    return [-int(letter) for letter in reversed(word)]


def multiply_words(*parts: Sequence[int]) -> list[int]:
    return reduce_word(letter for part in parts for letter in part)


class Gamma:
    def __init__(self, joint: dict[str, Any], q3: dict[str, Any]):
        public = joint["gamma"]
        self.width, self.order = 26, 243
        transitions = unpack(public["transitions"], "u16-le")
        require(len(transitions) == self.width * self.order, "gamma_transitions")
        self.transitions = [[value - 1 for value in transitions[index * self.width:(index + 1) * self.width]]
                            for index in range(self.order)]
        parents = unpack(public["section_parent_states"], "u16-le")
        generators = unpack(public["section_parent_generators"], "u8")
        self.parents = [value - 1 for value in parents]
        self.parent_generators = [value - 1 for value in generators]
        self.sections = []
        for start in range(self.order):
            state, section = start, []
            while state:
                section.append(self.parent_generators[state])
                state = self.parents[state]
            self.sections.append(section[::-1])
        self.inverses = []
        for left in range(self.order):
            hits = [right for right in range(self.order)
                    if self.mul(left, right) == 0 and self.mul(right, left) == 0]
            require(len(hits) == 1, "gamma_inverse")
            self.inverses.append(hits[0])
        self.words = [list(record["word"])
                      for record in q3["correction_fibre"]["records"][1:]]
        require(len(self.words) == self.width and
                digest(self.words) == joint["record_manifest"]["words_sha256"],
                "gamma_words")

    def mul(self, left: int, right: int) -> int:
        for generator in self.sections[right]:
            left = self.transitions[left][generator]
        return left

    def closure(self, generators: list[int]) -> set[int]:
        generators = list(dict.fromkeys(generators + [self.inverses[x] for x in generators]))
        seen, queue = {0}, [0]
        while queue:
            left = queue.pop()
            for right in generators:
                value = self.mul(left, right)
                if value not in seen:
                    seen.add(value)
                    queue.append(value)
        return seen

    def normal(self, left: set[int], right: set[int]) -> bool:
        return all(self.mul(self.mul(self.inverses[x], y), x) in left
                   for x in right for y in left)

    def chain(self) -> list[int]:
        generators: list[int] = []
        subgroups = [{0}]
        for level in range(1, 6):
            for value in range(1, self.order):
                if value in subgroups[-1]:
                    continue
                candidate = self.closure(generators + [value])
                if len(candidate) == 3 ** level and self.normal(subgroups[-1], candidate):
                    generators.append(value)
                    subgroups.append(candidate)
                    break
            else:
                raise RuntimeError("gamma_chain")
        return generators

    def normal_forms(self, generators: list[int]) -> dict[int, tuple[int, ...]]:
        answer: dict[int, tuple[int, ...]] = {}

        def visit(index: int, state: int, exponents: tuple[int, ...]) -> None:
            if index == 5:
                answer[state] = exponents
                return
            for exponent in range(3):
                visit(index + 1, state, exponents + (exponent,))
                state = self.mul(state, generators[index])

        visit(0, 0, ())
        require(len(answer) == self.order, "gamma_normal_forms")
        return answer

    def source(self, state: int) -> list[int]:
        answer: list[int] = []
        for generator in self.sections[state]:
            answer = multiply_words(answer, self.words[generator])
        return answer


def q0_relators(raw: Any) -> list[list[int]]:
    def substitute(word: Sequence[int], left: Sequence[int], right: Sequence[int]) -> list[int]:
        answer: list[int] = []
        for letter in word:
            answer = multiply_words(answer,
                                    left if letter == 1 else inverse_word(left) if letter == -1
                                    else right if letter == 2 else inverse_word(right))
        return answer

    split = [list(word) for word in raw.SPLIT_WORDS]
    first = [substitute(row, split[0], split[1]) for row in raw.P_RELATORS]
    second = [substitute(row, split[2], split[3]) for row in raw.G9_RELATORS]
    cross = [multiply_words(inverse_word(left), inverse_word(right), left, right)
             for left in split[:2] for right in split[2:]]
    cross += [multiply_words([1], inverse_word(multiply_words(split[0], split[2]))),
              multiply_words([2], inverse_word(multiply_words(split[1], split[3])))]
    answer = first + second + cross
    require(digest(answer) == "dcb8ce42c8324b0ce2a5018007f3d664da5568ee73182758a9f358deba84bc2a",
            "q0_relators")
    return answer


def rebuild_presentation(joint: dict[str, Any], q3: dict[str, Any], raw: Any) -> dict[str, Any]:
    gamma = Gamma(joint, q3)
    generators = gamma.chain()
    normal_forms = gamma.normal_forms(generators)
    sources = [gamma.source(state) for state in generators]

    def normal_word(state: int) -> list[int]:
        answer: list[int] = []
        for index, exponent in enumerate(normal_forms[state]):
            answer = multiply_words(answer, sources[index] * exponent)
        return answer

    relators: list[list[int]] = []
    for index, state in enumerate(generators):
        relators.append(multiply_words(sources[index], sources[index], sources[index],
                                       inverse_word(normal_word(gamma.mul(gamma.mul(state, state), state)))))
    for upper in range(1, 5):
        for lower in range(upper):
            state = gamma.mul(gamma.mul(gamma.inverses[generators[upper]], generators[lower]),
                              generators[upper])
            relators.append(multiply_words(inverse_word(sources[upper]), sources[lower],
                                           sources[upper], inverse_word(normal_word(state))))
    action_rows = joint["action_relations"]["rows"]
    for state, source in zip(generators, sources):
        for letter_index, letter in ((0, [1]), (1, [2])):
            target = 0
            for record in gamma.sections[state]:
                row = next(item for item in action_rows
                           if item[0] == record + 1 and item[1] == letter_index + 1 and item[2] == 1)
                target = gamma.mul(target, row[3] - 1)
            relators.append(multiply_words(inverse_word(letter), source, letter,
                                           inverse_word(normal_word(target))))
    raw_q0 = q0_relators(raw)
    registered = [multiply_words(word, inverse_word(gamma.source(
        joint["q0_relations"]["rows"][index][2] - 1)))
                  for index, word in enumerate(raw_q0)]
    require(digest(registered) == "bf24506f259414c3d375d5291c3014f1478b9b4ea73d389c07b7d10b07c82dc5" and
            [len(registered[index - 1]) for index in (3, 9, 12)] == [190, 344, 902],
            "registered_q0")
    for index, word in enumerate(raw_q0):
        relators.append(multiply_words(word, inverse_word(normal_word(
            joint["q0_relations"]["rows"][index][2] - 1))))
    require(len(relators) == 44, "compact_relator_count")
    return {"pc_generators": generators, "compact_relator_count": len(relators),
            "relators_sha256": digest(relators), "pc_state_normal_form_count": len(normal_forms),
            "relators": relators, "registered_q0_relators_sha256": digest(registered)}


def sparse_add(left: dict[Any, int], right: dict[Any, int], scale: int = 1) -> dict[Any, int]:
    answer = dict(left)
    for key, raw in right.items():
        value = (answer.get(key, 0) + int(scale) * int(raw)) % 3
        if value:
            answer[key] = value
        else:
            answer.pop(key, None)
    return answer


def pairing(functional: dict[Any, int], row: dict[Any, int]) -> int:
    return sum(int(value) * int(functional.get(key, 0))
               for key, value in row.items()) % 3


class RowSpace:
    """Canonical sparse F3 echelon with an independently replayable dual."""
    def __init__(self) -> None:
        self.rows: dict[Any, dict[Any, int]] = {}
        self.order: list[Any] = []

    def reduce(self, source: dict[Any, int]) -> dict[Any, int]:
        row = {key: int(value) % 3 for key, value in source.items() if int(value) % 3}
        for pivot in sorted(self.rows):
            coefficient = row.get(pivot, 0)
            if coefficient:
                for key, value in self.rows[pivot].items():
                    updated = (row.get(key, 0) - coefficient * int(value)) % 3
                    if updated:
                        row[key] = updated
                    else:
                        row.pop(key, None)
        return row

    def insert(self, source: dict[Any, int]) -> tuple[bool, dict[Any, int]]:
        row = self.reduce(source)
        if not row:
            return False, {}
        pivot = min(row)
        scale = 1 if row[pivot] == 1 else 2
        row = {key: scale * int(value) % 3 for key, value in row.items()
               if scale * int(value) % 3}
        require(pivot not in self.rows, "echelon_duplicate_pivot")
        self.rows[pivot] = row
        self.order.append(pivot)
        require(len(self.rows) <= MAX_FRONTIER, "echelon_rank_cap")
        return True, row

    def basis(self) -> list[dict[Any, int]]:
        return [self.rows[pivot] for pivot in sorted(self.rows)]

    def dual(self, target: dict[Any, int]) -> tuple[dict[Any, int], int]:
        remainder = self.reduce(target)
        require(bool(remainder), "dual_member")
        free = min(remainder)
        functional: dict[Any, int] = {free: 1}
        for pivot in sorted(self.rows, reverse=True):
            value = pairing(functional, self.rows[pivot])
            if value:
                functional[pivot] = (-value) % 3
            else:
                functional.pop(pivot, None)
        target_pair = pairing(functional, target)
        require(target_pair != 0 and all(pairing(functional, row) == 0
                                         for row in self.rows.values()), "dual_replay")
        return functional, target_pair

    def __len__(self) -> int:
        return len(self.rows)


def physical_key(block: int, component: int, blob: bytes) -> bytes:
    return b"R" + bytes((int(block), int(component))) + len(blob).to_bytes(2, "big") + blob


def validate_physical_key(key: bytes) -> None:
    require(type(key) is bytes, "physical_key_type")
    if key[:1] == b"N":
        require(len(key) == 2 and key[1] in (1, 2), "normalization_key")
        return
    require(len(key) >= 5 and key[:1] == b"R" and key[1] in (1, 2, 3), "row_key_tag")
    width = int.from_bytes(key[3:5], "big")
    require(len(key) == 5 + width, "row_key_width")
    require((key[1] in (1, 2) and key[2] in (1, 2, 3) and width == 40) or
            (key[1] == 3 and key[2] in (1, 2, 3, 4, 5, 6) and width == 154),
            "row_key_domain")


def public_sparse(row: dict[bytes, int]) -> list[list[Any]]:
    for key in row:
        validate_physical_key(key)
    return [[key.hex(), int(value) % 3]
            for key, value in sorted(row.items()) if int(value) % 3]


def parse_public_sparse(value: Any, label: str) -> dict[bytes, int]:
    require(type(value) is list, label + "_shape")
    answer: dict[bytes, int] = {}
    prior: bytes | None = None
    for item in value:
        require(type(item) is list and len(item) == 2 and type(item[0]) is str and
                type(item[1]) is int and item[1] in (1, 2), label + "_item")
        try:
            key = bytes.fromhex(item[0])
        except ValueError as exc:
            raise RuntimeError(label + "_hex") from exc
        validate_physical_key(key)
        require(prior is None or prior < key, label + "_canonical_order")
        answer[key] = item[1]
        prior = key
    require(public_sparse(answer) == value, label + "_canonical")
    return answer


def element_from_blob(blob: bytes, block: int) -> tuple[bytes, bytes]:
    cut, total = (36, 40) if block in (1, 2) else (144, 154)
    require(len(blob) == total, "element_blob_width")
    return blob[:cut], blob[cut:]


def validate_ledger(helper: Any, roof: dict[str, Any]) -> list[dict[str, Any]]:
    bridge = roof.get("bridge", {})
    ledger = bridge.get("occurrence_ledger")
    require(type(ledger) is list and len(ledger) == 11 and
            bridge.get("ten_to_eleven") == [0, 1, 2, 3, 0, 4, 5, 6, 7, 8, 9] and
            bridge.get("eleven_delete_duplicate") == [0, 1, 2, 3, 5, 6, 7, 8, 9, 10] and
            bridge.get("seven_blocks") == [[0, 1, 2], [3, 0, 4], [5], [6], [7], [8], [9]] and
            bridge.get("occurrence_ledger_sha256") == digest(ledger), "occurrence_ledger")
    layout = getattr(helper, "CHECKER_BRIDGE_OWNER_LAYOUT", None)
    require(type(layout) in (list, tuple) and len(layout) == 11, "checker_layout")
    answer = []
    for index, original in enumerate(ledger):
        require(type(original) is dict and int(original.get("ordinal", 0)) == index + 1,
                "ledger_ordinal")
        actual = (original.get("block"), int(original.get("block_index", 0)),
                  int(original.get("block_slot", 0)), original.get("occurrence"),
                  original.get("type"), int(original.get("ten_index", -1)),
                  int(original.get("context_id", 0)), original.get("role"),
                  int(original.get("factor_sign", 0)), original.get("orientation"),
                  tuple(original.get("fox_prefix_occurrences", ())))
        require(actual == tuple(layout[index]), "ledger_layout:" + str(index + 1))
        answer.append(dict(original))
    return answer


class CachedDirect:
    def __init__(self, word: Sequence[int], states: list[Any]):
        self.word = tuple(word)
        self.states = states

    def direct(self, word: Sequence[int], index: int) -> Any:
        require(tuple(word) == self.word and 0 <= int(index) < 10, "cached_direct")
        return self.states[int(index)]


def runtime_environment(roof: dict[str, Any], q3: dict[str, Any], raw: Any) -> dict[str, Any]:
    bootstrap = load_source("bootstrap")
    occurrence = load_source("occurrence")
    helper = bootstrap.load_helper()
    meter = helper.Meter(dict(helper.CAPS))
    authority = SimpleNamespace(receipt=roof)
    arithmetic = helper.CheckerArithmetic(authority, meter)
    ledger = validate_ledger(helper, roof)
    e3, e4, _maps = raw.build_quotients(q3)
    for checker_q, independent_q, label in ((arithmetic.e3, e3, "E3"),
                                             (arithmetic.e4, e4, "E4")):
        require(len(checker_q.generators) == len(independent_q.generators) and
                all(helper.element_blob(left) == raw.element_blob(right)
                    for left, right in zip(checker_q.generators, independent_q.generators)),
                "quotient_binding:" + label)
    g760 = tuple(raw.construct_g760())
    require(len(g760) == 760 and digest(list(g760)) == G760_SHA256, "g760_binding")
    base_states = [arithmetic.direct(g760, index) for index in range(10)]
    for index, context in enumerate(arithmetic.contexts):
        quotient = e3 if context["type"] == "E3" else e4
        expected = quotient.eval(raw.f2_substitute(g760, context["left"], context["right"]))
        require(helper.element_blob(base_states[index].a) == raw.element_blob(expected),
                "g760_context_binding:" + str(index))
    actor_cache: dict[tuple[int, int], tuple[Any, Any]] = {}
    for item in ledger:
        ordinal, index = int(item["ordinal"]), int(item["ten_index"])
        quotient, prefix = base_states[index].q, base_states[index].q.identity
        for prior_ordinal in item.get("fox_prefix_occurrences", ()):
            prior = ledger[int(prior_ordinal) - 1]
            state = base_states[int(prior["ten_index"])]
            prefix = quotient.mul(prefix, state.a if int(prior["factor_sign"]) > 0
                                  else quotient.inverse(state.a))
        current = base_states[index]
        transport = quotient.mul(prefix, current.a) if int(item["factor_sign"]) > 0 else prefix
        for letter in ACTION_LETTERS:
            actor = arithmetic.actors[index, letter].a
            actor_cache[ordinal, letter] = (
                quotient, quotient.mul(quotient.mul(transport, actor), quotient.inverse(transport)))
    occurrence.PHYSICAL_G = list(g760)
    occurrence.BASE_STATES = base_states
    occurrence.ACTOR_CACHE = actor_cache
    return {"helper": helper, "occurrence": occurrence, "raw": raw,
            "arithmetic": arithmetic, "meter": meter, "ledger": ledger,
            "e3": e3, "e4": e4, "g760": g760}


def exponent_pair(word: Sequence[int]) -> tuple[int, int]:
    return (sum(1 if letter == 1 else -1 if letter == -1 else 0 for letter in word),
            sum(1 if letter == 2 else -1 if letter == -2 else 0 for letter in word))


def augmented_occurrence(env: dict[str, Any], word: Sequence[int], label: str) -> dict[str, int]:
    normalized = reduce_word(word)
    states = [env["arithmetic"].direct(normalized, index) for index in range(10)]
    require(all(state.a == state.q.identity for state in states), label + "_joint_identity")
    row = dict(env["occurrence"].term_vector(CachedDirect(normalized, states),
                                               normalized, env["ledger"]))
    left, right = exponent_pair(normalized)
    require(left % 18 == 0 and right % 18 == 0, label + "_exponent_lattice")
    for index, value in ((1, left // 18), (2, right // 18)):
        coefficient = value % 3
        if coefficient:
            row["N:" + str(index)] = coefficient
    return {key: int(value) % 3 for key, value in row.items() if int(value) % 3}


def parse_occurrence(row: dict[str, int], ledger: list[dict[str, Any]]) -> dict[tuple[Any, ...], int]:
    answer: dict[tuple[Any, ...], int] = {}
    for text, raw_value in row.items():
        value = int(raw_value) % 3
        if not value:
            continue
        if text.startswith("N:"):
            index = int(text.split(":", 1)[1])
            require(index in (1, 2), "occurrence_normalization_index")
            key = ("N", index)
        else:
            parts = text.split(":", 2)
            require(len(parts) == 3 and parts[0].startswith("o"), "occurrence_key")
            ordinal, component = int(parts[0][1:]), int(parts[1])
            require(1 <= ordinal <= len(ledger), "occurrence_ordinal")
            try:
                blob = bytes.fromhex(parts[2])
            except ValueError as exc:
                raise RuntimeError("occurrence_blob") from exc
            block = 1 if ledger[ordinal - 1]["type"] == "E3" else 3
            element_from_blob(blob, block)
            key = ("O", ordinal, component, blob)
        answer[key] = (answer.get(key, 0) + value) % 3
        if not answer[key]:
            answer.pop(key)
    return answer


def occurrence_strings(row: dict[tuple[Any, ...], int]) -> dict[str, int]:
    answer: dict[str, int] = {}
    for key, value in row.items():
        if key[0] == "N":
            text = "N:" + str(key[1])
        else:
            require(key[0] == "O" and len(key) == 4, "occurrence_internal_key")
            text = "o%d:%d:%s" % (key[1], key[2], key[3].hex())
        answer[text] = int(value) % 3
    return {key: value for key, value in answer.items() if value}


def quotient_occurrence(row: dict[tuple[Any, ...], int], ledger: list[dict[str, Any]],
                        b3: RowSpace, b4: RowSpace) -> dict[tuple[Any, ...], int]:
    answer = {key: int(value) % 3 for key, value in row.items()
              if key[0] == "N" and int(value) % 3}
    groups: dict[int, dict[tuple[int, tuple[bytes, bytes]], int]] = {}
    for key, raw_value in row.items():
        if key[0] != "O":
            continue
        ordinal, component, blob = int(key[1]), int(key[2]), key[3]
        block = 1 if ledger[ordinal - 1]["type"] == "E3" else 3
        element = element_from_blob(blob, block)
        group = groups.setdefault(ordinal, {})
        group[component, element] = (group.get((component, element), 0) + int(raw_value)) % 3
        if not group[component, element]:
            group.pop((component, element))
    for ordinal, group in groups.items():
        space = b3 if ledger[ordinal - 1]["type"] == "E3" else b4
        for (component, element), value in space.reduce(group).items():
            blob = element[0] + element[1]
            answer[("O", ordinal, int(component), blob)] = int(value) % 3
    return {key: value for key, value in answer.items() if value}


def act_occurrence(env: dict[str, Any], row: dict[tuple[Any, ...], int], letter: int,
                   b3: RowSpace, b4: RowSpace) -> dict[tuple[Any, ...], int]:
    public = occurrence_strings(row)
    ordinary = {key: value for key, value in public.items() if not key.startswith("N:")}
    moved = env["occurrence"].apply_actor(ordinary, int(letter), env["ledger"])
    for index in (1, 2):
        key = "N:" + str(index)
        if key in public:
            moved[key] = public[key]
    return quotient_occurrence(parse_occurrence(moved, env["ledger"]), env["ledger"], b3, b4)


def aggregate_occurrence(env: dict[str, Any], row: dict[tuple[Any, ...], int]) -> dict[bytes, int]:
    public = occurrence_strings(row)
    ordinary = {key: value for key, value in public.items() if not key.startswith("N:")}
    answer = dict(env["occurrence"].aggregate_tagged(ordinary, env["ledger"]))
    for index in (1, 2):
        value = int(public.get("N:" + str(index), 0)) % 3
        if value:
            answer[b"N" + bytes((index,))] = value
    for key in answer:
        validate_physical_key(key)
    return {key: int(value) % 3 for key, value in answer.items() if int(value) % 3}


def close_boundary(raw: Any, quotient: Any, degree: int, meter: Any) -> RowSpace:
    relations = raw.pure_relations(degree)
    require(len(relations) == (2 if degree == 3 else 11), "boundary_seed_count")
    space, frontier = RowSpace(), []
    for relation in relations:
        row, value = raw.fox(quotient, relation)
        require(value == quotient.identity, "boundary_seed_value")
        rise, reduced = space.insert(row)
        if rise:
            frontier.append(reduced)
    letters = tuple(range(1, len(quotient.generators) + 1))
    cursor = 0
    while cursor < len(frontier):
        row = frontier[cursor]
        cursor += 1
        require(len(frontier) <= MAX_FRONTIER, "boundary_frontier_cap")
        if cursor == 1 or cursor % 32 == 0:
            meter.check("checker.boundary_closure")
            print("R07_A0_CHECKER_PROGRESS phase=boundary_B%d rank=%d cursor=%d frontier=%d" %
                  (degree, len(space), cursor, len(frontier)), flush=True)
        for letter in letters + tuple(-value for value in letters):
            moved = raw.translate(row, quotient.eval((letter,)), quotient)
            rise, reduced = space.insert(moved)
            if rise:
                frontier.append(reduced)
    return space


def serialize_gradient(raw: Any, row: dict[Any, int], block: int) -> dict[bytes, int]:
    answer: dict[bytes, int] = {}
    for (component, element), raw_value in row.items():
        key = physical_key(block, int(component), raw.element_blob(element))
        value = (answer.get(key, 0) + int(raw_value)) % 3
        if value:
            answer[key] = value
        else:
            answer.pop(key, None)
    return answer


def target_row(env: dict[str, Any]) -> dict[bytes, int]:
    raw, g760 = env["raw"], env["g760"]
    first, second = raw.hexagon_words(g760)
    entries = ((1, env["e3"], raw.embed_pb3(first)),
               (2, env["e3"], raw.embed_pb3(second)),
               (3, env["e4"], raw.pentagon_word(g760)))
    answer: dict[bytes, int] = {}
    for block, quotient, word in entries:
        gradient, value = raw.fox(quotient, word)
        require(value == quotient.identity, "target_quotient_identity")
        answer = sparse_add(answer, serialize_gradient(raw, gradient, block), -1)
    return answer


def independent_closure(relators: list[list[int]], roof: dict[str, Any],
                        q3: dict[str, Any], raw: Any) -> dict[str, Any]:
    require(len(relators) == 44, "closure_seed_count")
    env = runtime_environment(roof, q3, raw)
    b3 = close_boundary(raw, env["e3"], 3, env["meter"])
    b4 = close_boundary(raw, env["e4"], 4, env["meter"])

    boundary = RowSpace()
    boundary_rows: list[dict[bytes, int]] = []
    for block, source in ((1, b3), (2, b3), (3, b4)):
        for row in source.basis():
            rise, reduced = boundary.insert(serialize_gradient(raw, row, block))
            require(rise, "physical_boundary_rank")
            boundary_rows.append(reduced)

    occurrence = RowSpace()
    frontier: list[dict[tuple[Any, ...], int]] = []
    for ordinal, word in enumerate(relators, 1):
        raw_row = augmented_occurrence(env, word, "compact_seed_" + str(ordinal))
        seed = quotient_occurrence(parse_occurrence(raw_row, env["ledger"]),
                                   env["ledger"], b3, b4)
        rise, reduced = occurrence.insert(seed)
        if rise:
            frontier.append(reduced)
    cursor = 0
    while cursor < len(frontier):
        row = frontier[cursor]
        cursor += 1
        require(len(frontier) <= MAX_FRONTIER, "occurrence_frontier_cap")
        if cursor == 1 or cursor % 32 == 0:
            env["meter"].check("checker.occurrence_closure")
            print("R07_A0_CHECKER_PROGRESS phase=occurrence rank=%d cursor=%d frontier=%d" %
                  (len(occurrence), cursor, len(frontier)), flush=True)
        for letter in ACTION_LETTERS:
            moved = act_occurrence(env, row, letter, b3, b4)
            rise, reduced = occurrence.insert(moved)
            if rise:
                frontier.append(reduced)

    correction = RowSpace()
    correction_rows: list[dict[bytes, int]] = []
    for ordinal, pivot in enumerate(occurrence.order, 1):
        physical = aggregate_occurrence(env, occurrence.rows[pivot])
        physical = boundary.reduce(physical)
        rise, reduced = correction.insert(physical)
        if rise:
            correction_rows.append(reduced)
        if ordinal == 1 or ordinal % 64 == 0:
            print("R07_A0_CHECKER_PROGRESS phase=physical_correction rank=%d cursor=%d total=%d" %
                  (len(correction), ordinal, len(occurrence.order)), flush=True)

    combined = RowSpace()
    for row in boundary_rows + correction_rows:
        rise, _reduced = combined.insert(row)
        require(rise, "combined_retained_rank")
    target = target_row(env)
    remainder = combined.reduce(target)
    return {"env": env, "b3": b3, "b4": b4, "boundary": boundary,
            "boundary_rows": boundary_rows, "occurrence": occurrence,
            "correction": correction, "correction_rows": correction_rows,
            "combined": combined, "target": target, "remainder": remainder,
            "boundary_rank": len(boundary), "occurrence_rank": len(occurrence),
            "correction_rank": len(correction), "frontier_count": len(frontier)}


def check_summary(a0: dict[str, Any], closure: dict[str, Any]) -> None:
    remainder_public = public_sparse(closure["remainder"])
    require(a0.get("boundary_rank") == closure["boundary_rank"] and
            a0.get("occurrence_rank") == closure["occurrence_rank"] and
            a0.get("remainder_nnz") == len(closure["remainder"]) and
            a0.get("remainder_sha256") == digest(remainder_public), "a0_summary")
    require(a0.get("normalized_exponent_coordinates_included") is True and
            a0.get("seed_direct_replay_checked") is True, "a0_replay_contract")


def typed_boundary_row(env: dict[str, Any], item: dict[str, Any]) -> dict[bytes, int]:
    required = {"block", "base_relator_index", "translation_word", "coefficient"}
    require(set(item) in (required, required | {"translation_element_hex"}) and
            type(item["block"]) is int and item["block"] in (1, 2, 3) and
            type(item["base_relator_index"]) is int and
            type(item["translation_word"]) is list and
            type(item["coefficient"]) is int and item["coefficient"] in (1, 2),
            "typed_boundary_term")
    block = item["block"]
    quotient = env["e3"] if block in (1, 2) else env["e4"]
    width = 3 if block in (1, 2) else 6
    word = item["translation_word"]
    require(all(type(letter) is int and letter != 0 and abs(letter) <= width
                for letter in word),
            "typed_boundary_translation_word")
    translation = quotient.eval(word)
    if "translation_element_hex" in item:
        require(type(item["translation_element_hex"]) is str, "typed_boundary_element_hex")
        try:
            claimed = bytes.fromhex(item["translation_element_hex"])
        except ValueError as exc:
            raise RuntimeError("typed_boundary_element_hex") from exc
        require(claimed == env["raw"].element_blob(translation),
                "typed_boundary_element_binding")
    relations = env["raw"].pure_relations(3 if block in (1, 2) else 4)
    index = item["base_relator_index"]
    require(1 <= index <= len(relations), "typed_boundary_relation_index")
    require(quotient.mul(translation, quotient.inverse(translation)) == quotient.identity and
            quotient.mul(quotient.inverse(translation), translation) == quotient.identity,
            "typed_boundary_translation_element")
    source, value = env["raw"].fox(quotient, relations[index - 1])
    require(value == quotient.identity, "typed_boundary_source_value")
    moved = env["raw"].translate(source, translation, quotient)
    return serialize_gradient(env["raw"], moved, block)


def check_member(a0: dict[str, Any], closure: dict[str, Any]) -> None:
    require(a0.get("member") is True and a0.get("positive_certificate") is True and
            not closure["remainder"], "member_terminal")
    check_summary(a0, closure)
    word = a0.get("literal_correction")
    require(type(word) is list and all(type(letter) is int and letter in ACTION_LETTERS
                                       for letter in word), "member_literal")
    require(exponent_pair(word) == (0, 0) and a0.get("exact_exponent_pair") == [0, 0],
            "member_exponent_replay")
    raw_occurrence = augmented_occurrence(closure["env"], word, "member_literal")
    require(not any(key.startswith("N:") for key in raw_occurrence), "member_normalization_zero")
    occurrence = parse_occurrence(raw_occurrence, closure["env"]["ledger"])
    physical = aggregate_occurrence(closure["env"], occurrence)
    residual = sparse_add(closure["target"], physical, -1)

    certificate = a0.get("typed_boundary_preimage")
    require(type(certificate) is list, "typed_boundary_preimage_shape")
    order = []
    replay: dict[bytes, int] = {}
    for item in certificate:
        require(type(item) is dict, "typed_boundary_preimage_item")
        word = item.get("translation_word")
        key = (item.get("block"), item.get("base_relator_index"),
               tuple(word) if type(word) is list else ())
        order.append(key)
        replay = sparse_add(replay, typed_boundary_row(closure["env"], item),
                            int(item["coefficient"]))
    require(order == sorted(order) and len(order) == len(set(order)),
            "typed_boundary_preimage_canonical")
    require(replay == residual, "typed_boundary_preimage_replay")


def replay_legacy_oracle(closure: dict[str, Any], roof: dict[str, Any]) -> None:
    rows = roof.get("Delta0", {}).get("presentation", {}).get("rows")
    require(type(rows) is list and len(rows) == LEGACY_ROWS, "legacy_oracle_roster_count")
    env = closure["env"]
    for ordinal, item in enumerate(rows, 1):
        if ordinal == 1 or ordinal % 64 == 0:
            env["meter"].check("checker.legacy_oracle")
            print("R07_A0_CHECKER_PROGRESS phase=legacy_oracle cursor=%d total=%d" %
                  (ordinal, LEGACY_ROWS), flush=True)
        require(type(item) is dict and type(item.get("word")) is list, "legacy_oracle_row")
        raw_row = augmented_occurrence(env, item["word"], "legacy_seed_" + str(ordinal))
        seed = quotient_occurrence(parse_occurrence(raw_row, env["ledger"]),
                                   env["ledger"], closure["b3"], closure["b4"])
        require(not closure["occurrence"].reduce(seed),
                "legacy_seed_outside_compact_span:" + str(ordinal))
        rows[ordinal - 1] = None


def check_nonmember(a0: dict[str, Any], closure: dict[str, Any], roof: dict[str, Any]) -> None:
    require(a0.get("member") is False and bool(closure["remainder"]), "nonmember_terminal")
    check_summary(a0, closure)
    replay_legacy_oracle(closure, roof)
    functional, target_pair = closure["combined"].dual(closure["target"])
    require(all(pairing(functional, row) == 0 for row in closure["boundary_rows"]),
            "separator_boundary_pair")
    require(all(pairing(functional, row) == 0 for row in closure["correction_rows"]),
            "separator_correction_pair")
    require(pairing(functional, closure["target"]) == target_pair != 0,
            "separator_target_pair")
    expected = public_sparse(functional)
    claimed = parse_public_sparse(a0.get("separator"), "separator")
    require(claimed == functional and a0.get("separator") == expected and
            a0.get("separator_sha256") == digest(expected) and
            a0.get("target_pair") == target_pair, "separator_binding")
    require(a0.get("legacy_oracle_exhausted") is True, "legacy_oracle_claim")


def fixture() -> None:
    raw = load_source("raw")
    word = tuple(raw.construct_g760())
    require(len(word) == 760 and digest(list(word)) == G760_SHA256, "fixture_g760")
    bootstrap = load_source("bootstrap")
    helper = bootstrap.load_helper()
    occurrence = load_source("occurrence")
    require(callable(getattr(helper, "CheckerArithmetic", None)) and
            callable(getattr(occurrence, "term_vector", None)) and
            callable(getattr(occurrence, "apply_actor", None)) and
            callable(getattr(occurrence, "aggregate_tagged", None)),
            "fixture_independent_api")
    space = RowSpace()
    first = {b"a": 1, b"c": 2}
    second = {b"b": 1, b"c": 1}
    require(space.insert(first)[0] and space.insert(second)[0], "fixture_rank")
    target = {b"c": 1}
    functional, value = space.dual(target)
    require(value != 0 and pairing(functional, first) == 0 and
            pairing(functional, second) == 0, "fixture_dual")
    physical = {physical_key(1, 1, bytes(40)): 1,
                b"N" + bytes((1,)): 2}
    public = public_sparse(physical)
    require(parse_public_sparse(public, "fixture_sparse") == physical and
            digest(public) == digest([[key.hex(), value]
                                      for key, value in sorted(physical.items())]),
            "fixture_public_sparse")
    mutated = [list(item) for item in public]
    mutated[0][1] = 2 if mutated[0][1] == 1 else 1
    require(digest(mutated) != digest(public), "fixture_mutation")


def validate_presentation(output: dict[str, Any], expected: dict[str, Any]) -> None:
    presentation = output.get("presentation", {})
    require(presentation.get("compact_relator_count") == 44 and
            presentation.get("pc_generators") == expected["pc_generators"] and
            presentation.get("relators") == expected["relators"] and
            presentation.get("relators_sha256") == expected["relators_sha256"] and
            presentation.get("registered_q0_relators_sha256") ==
            expected["registered_q0_relators_sha256"] and
            presentation.get("pc_state_normal_form_count") == 243,
            "presentation_mismatch")


def validate_envelope(output: dict[str, Any], acceptance: dict[str, Any]) -> dict[str, Any]:
    require(output.get("schema") == SCHEMA, "schema")
    roof_input = output.get("roof_input", {})
    require(roof_input.get("bytes") == DATA_PINS[str(ROOF)][0] and
            roof_input.get("sha256") == DATA_PINS[str(ROOF)][1] and
            roof_input.get("authenticated") is True, "roof_input")
    accepted = output.get("acceptance_v2", {})
    require(acceptance_ok(acceptance) and accepted.get("bytes") == DATA_PINS[str(ACCEPTANCE)][0] and
            accepted.get("sha256") == DATA_PINS[str(ACCEPTANCE)][1] and
            accepted.get("authenticated") is True, "acceptance_pin")
    a0 = output.get("a0")
    require(type(a0) is dict and a0.get("status") in
            ("UNKNOWN_INPUT", "UNKNOWN_RESOURCE", "MEMBER", "NONMEMBER"), "a0_terminal")
    require(output.get("status") == a0.get("status") and
            output.get("terminal") == output.get("status"), "top_terminal_propagation")
    expected_claim = a0.get("status") == "MEMBER" and a0.get("positive_certificate") is True
    require(output.get("claim_boundary", {}).get("A0_membership") is expected_claim, "overclaim")
    memory = output.get("memory_contract", {})
    require(memory.get("worker_inherits_reducer") is False and
            memory.get("worker_inherits_checkpoint") is False and
            memory.get("worker_inherits_ancestry") is False and
            memory.get("dependent_traces_retained") is False, "memory_contract")
    return a0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--producer")
    parser.add_argument("--fixture", action="store_true")
    args = parser.parse_args()
    try:
        if args.fixture:
            fixture()
            print("R07_A0_COMPACT_PC_CHECKER_FIXTURE_PASS")
            return 0
        require(type(args.producer) is str and bool(args.producer), "producer_required")
        output = json.loads(Path(args.producer).read_bytes())
        require(type(output) is dict, "producer_object")
        joint, q3 = load_data(JOINT), load_data(Q3)
        acceptance = load_data(ACCEPTANCE)
        raw = load_source("raw")
        expected = rebuild_presentation(joint, q3, raw)
        validate_presentation(output, expected)
        a0 = validate_envelope(output, acceptance)
        status = a0["status"]
        if status in ("UNKNOWN_INPUT", "UNKNOWN_RESOURCE"):
            require(type(a0.get("reason")) is str and bool(a0["reason"]) and
                    a0.get("member") is not True and a0.get("positive_certificate") is not True,
                    "a0_unknown_shape")
        else:
            roof = load_data(ROOF)
            closure = independent_closure(expected["relators"], roof, q3, raw)
            if status == "MEMBER":
                check_member(a0, closure)
            else:
                check_nonmember(a0, closure, roof)
        print("R07_A0_COMPACT_PC_CHECKER_PASS relators=44 sha=" +
              expected["relators_sha256"])
        return 0
    except Exception as exc:
        print("R07_A0_COMPACT_PC_CHECKER_FAIL:" + str(exc))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
