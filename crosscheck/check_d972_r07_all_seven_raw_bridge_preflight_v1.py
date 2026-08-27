"""Helper-independent checker for the task-175 all-seven raw bridge.

The checker treats pinned files as data only.  It does not import or execute a
producer or predecessor Python module: PC/permutation arithmetic, word
algebra, the joint roster, Fox/D1/D2, and semantic mutations are local here.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any, Iterable, Sequence

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "search/certs/d972_r07_all_seven_raw_bridge_preflight_v1_20260827.json"
Q3_REL = "ci/b345_157ee_artifacts_32359956713/d972_b345_q3_chief_v1.json"
JOINT_REL = "ci/b345_157ee_artifacts_32359956713/d972_b345_joint_kernel_qstar_closure_v1.json"
CAP = 6441
READY = "R07_ALL_SEVEN_RAW_BRIDGE_PREFLIGHT_READY"
UNKNOWN_CONTEXT = "UNKNOWN_INPUT:E3_CONTEXT_KERNEL_BRIDGE"
UNKNOWN_PB3 = "UNKNOWN_INPUT:PB3_PRESENTATION_PIN"
UNKNOWN_RAW = "UNKNOWN_INPUT:RAW_FORMULA"
UNKNOWN_FOX = "UNKNOWN_INPUT:FOX_CANARY"
ALLOWED = {READY, UNKNOWN_CONTEXT, UNKNOWN_PB3, UNKNOWN_RAW, UNKNOWN_FOX,
           "UNKNOWN_RESOURCE:LOCAL_EXECUTION_GUARD", "UNKNOWN_RESOURCE:runtime"}
MUTATION_NAMES = [
    "correction_left_right", "corrected_base_sign", "H2_u_z",
    "inverse_fox_prefix", "negative_pentagon_factor_4",
    "negative_pentagon_factor_5", "negative_pentagon_order",
    "coface_slot_1_3_swap", "E3_E4_rank_swap", "E3_E4_blob_swap",
    "context_name_only_dedup", "dropped_block_tag",
    "fourth_third_deletion_swap", "fine_insertion_index_4_3_swap",
    "derived_u_order", "derived_z_order", "one_actual_roster_letter",
    "actual_product_additivity_term", "raw_base_target_stacked_confusion",
    "terminal_marker",
]
LEGACY_FIXTURE_MUTATION_NAMES = [
    name for name in MUTATION_NAMES if name != "raw_base_target_stacked_confusion"]

# Authentication pins are data pins.  No source loader exists in this file.
PINS = {
    "task175b": ("sol/luna_task_175b_r07_all_seven_raw_bridge_implementation_repair.md", 5136,
                 "a41f2446fd1c9f0bd60a7189db682784f4e69e24e8958f7c4505cd1eb9741836"),
    "task175": ("sol/luna_task_175_r07_all_seven_raw_bridge_preflight_v1.md", 8584,
                "5d0d8e006c6a752e5a525b188c9d95ba0c858aa69147432e639fe3e735ffefee"),
    "inventory173": ("sol/luna_reply_173_r07_all_seven_raw_bridge_inventory_v1.md", 24283,
                     "189a642fc8654f163b0b7964b75043ea393cac31a0b56b84ae0fddf2f73c3695"),
    "pb3_v121": ("sol/proof_pb3_two_relator_presentation_equality_v121.md", 5762,
                 "efd51ee51d496543e359704349877523a9d5d4aea686aee97e33c00dd6b84bd5"),
    "bridge_v122": ("sol/proof_r07_e3_context_kernel_retraction_bridge_v122.md", 7939,
                    "daadae2bed6a91ded8d3f1abec4d2fb6d379b80706f6387fa12abfd8f29e1348"),
    "checkpoint_v123": ("sol/audit_r07_all_seven_bridge_checkpoint_v123.md", 5017,
                        "272aabc882599031c4da0472f8f2340043b32571e8e05ecaa58fc5ad1c6a31ac"),
    "pb4_v108": ("sol/proof_pb4_eleven_relator_presentation_equality_v108.md", 6742,
                 "4a228f2b055fae7657ac5ca5b2e242eb05afcb04f6fb75ae79e9e776b3bca42f"),
    "v172_producer": ("search/d972_r07_full_e4_joint_orbit_preflight_v7.py", 21918,
                      "92701bb1ed84de9b9aa0fb8a986197f76b86e1f42af83ee18319700be0647eed"),
    "v172_checker": ("crosscheck/check_d972_r07_full_e4_orbit_preflight_v7.py", 12423,
                     "e3917ec05b95b8996e3a5cec1cc2bfde51c3ed8c6972175fd9be9e1178205c23"),
    "v172_cert": ("search/certs/d972_r07_full_e4_orbit_preflight_v7_20260827.json", 45246709,
                  "86c6f3a72a3f852a1be7c5323bf72c7ad987377fd5483b6e32528fe263e290ff"),
    "q3_receipt": (Q3_REL, 231570,
                   "3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72"),
    "157ee_receipt": ("ci/b345_157ee_artifacts_32359956713/d972_b345_joint_kernel_qstar_closure_v1.json", 2166036,
                      "1c3ad7a7124cee152eb40968cf212c14641a9f8720063c85f70533864898d0df"),
    "g760_source": ("search/check_d972_r07_616_to_760_commutator_affine_rhs_v3.py", 33409,
                    "f8c7fc7f5b5bbfffa0cf147a59313981c5a4b2c6c00504a9f773029097fdde5f"),
    "joint_source": ("search/d972_b345_joint_kernel_qstar_closure_v1.py", 67945,
                     "06ba6cf361957db3e339d48d14b3d4fbc689de9642e3f96273fbe8f3160e76dc"),
    "pb4_source": ("search/d972_b345_target6_dual_colgen_v2.py", 444497,
                   "b361dc5e7b025bb7efe3507b145e5480c6c67dfecc2e712134a8d521585e73c7"),
    "old_source": ("search/d972_b345_triple_cube_raw_lambda_census_v1.py", 126942,
                   "d4a290984ae8a93b6959f06d20c1de037b2814707778fba03c59ac87b2f736db"),
}

W2 = (1,1,1,1,-2,-2,-2,-2,-1,2,-1,-1,-2,-2,1,1,2,1,1,-2,1,1,2,1,1,2,1,1,-2,1,1,-2,1,1,2,2,-1,-1,-2,-1)
W3 = (1,1,1,1,-2,-2,-2,-2,-1,2,-1,-1,-2,-1,-1,2,-1,-1,-2,-2,1,1,2,1,2,2,1,2,2,-1,2,2,1,2,1,1,2,2,-1,-1,-2,-1,-1,2,-1,-1,-2,-2,-2,-1,-2,-2,1,2,1,1,-2,1)
P_RELATORS = [
    [-2,-2,1,1,2,1,2,1,1], [1,-2,-2,-2,-2,1,-2,-2,-2,-2],
    [-1,2,-1,-2,-1,-1,-2,-2,-1,-1,-2],
    [2,1,1,2,-1,2,-1,-1,2,-1,-1,2,-1],
    [-1,-2,-1,-1,-2,1,2,1,1,1,-2,-1,-1,-1],]
G9_RELATORS = [
    [1,2,2,-1,2,2], [2,-1,-1,-2,-1,-1], [2]*18, [1]*18,
    [2,1]+[-2]*8+[1,2,1]+[-2]*8+[1],
    [1,2,1,2,-1,-2,-1,-2,-1,-2,1,2,-1,-1,-1,-1,2,1,2,1,2,1,2,1,2,1,2,1,2,-1,2,1,1,1,1,2,-1,-2],
    [-1,-1,-1,2,1,2,-1,-2,-1,-2,-1,-2,-1,-2,-1,2,1,2,1,-2,-1,-1,-1,-2,1,-2,-1,-2,-1,-2,-1,-2,-1,-2,-1,-2,1,-2,1,-2],
    [1,-2,-1,-2,1,2,1,2,1,2,1,2,1,-2,-1,-2,1,1,1,1,1,1,-2,-1,-2,1,2,1,2,1,2,1,2,1,-2,-1,-2,1,1,1,1,1],]
SPLIT_WORDS = [
    [1,-2,1,1,2,-1,-2,-2,1,-2,-1,-1,-2,-1,-1,-2,-2,1,-2,-2],
    [-1,-1,-2,-1,-1,2,1,2,1,1,2,1,2,2],
    [1,2,2,-1,2,2,1,1,2,1,1,2,-1,2,2,1,-2,-1,-1,2,-1],
    [-2,-2,-1,-2,-1,-1,-2,-1,-2,1,1,2,1,1,2],]
COMPLETE_RELATORS_SHA = "dcb8ce42c8324b0ce2a5018007f3d664da5568ee73182758a9f358deba84bc2a"


class Stop(RuntimeError):
    def __init__(self, terminal: str, detail: str):
        super().__init__(detail)
        self.terminal, self.detail = terminal, detail


def fail(terminal: str, detail: str) -> None:
    raise Stop(terminal, detail)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def digest_obj(value: Any) -> str:
    return sha(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("ascii"))


def pin_inputs() -> dict[str, Any]:
    result = {}
    for name, (rel, expected_bytes, expected_sha) in PINS.items():
        path = ROOT / rel
        if not path.is_file():
            fail("UNKNOWN_RESOURCE:pin_missing", rel)
        raw = path.read_bytes()
        if len(raw) != expected_bytes:
            fail("UNKNOWN_RESOURCE:pin_bytes", rel)
        if sha(raw) != expected_sha:
            fail("UNKNOWN_RESOURCE:pin_sha", rel)
        result[name] = {"path": rel, "bytes": len(raw), "sha256": expected_sha}
    return result


def read_json(rel: str) -> dict[str, Any]:
    try:
        value = json.loads((ROOT / rel).read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        fail("UNKNOWN_RESOURCE:json", rel + ":" + str(exc))
    if not isinstance(value, dict):
        fail("UNKNOWN_RESOURCE:json", rel + ":not-object")
    return value


# ---- free words, paper convention, and the independently frozen g760 -----

def reduce_word(word: Iterable[int]) -> tuple[int, ...]:
    out = []
    for value in word:
        if type(value) is not int or value == 0 or abs(value) > 10:
            fail(UNKNOWN_RAW, "signed word alphabet")
        if out and out[-1] == -value:
            out.pop()
        else:
            out.append(value)
    return tuple(out)


def inverse(word: Sequence[int]) -> tuple[int, ...]:
    return reduce_word(-int(value) for value in reversed(word))


def paper_product(*displayed: Sequence[int]) -> tuple[int, ...]:
    if not displayed:
        fail(UNKNOWN_RAW, "empty paper product")
    return reduce_word(value for factor in reversed(displayed) for value in factor)


def substitute(word: Sequence[int], images: Sequence[Sequence[int]]) -> tuple[int, ...]:
    out = ()
    for value in word:
        index = abs(int(value))
        if not 1 <= index <= len(images):
            fail(UNKNOWN_RAW, "substitution index")
        image = images[index - 1]
        out = reduce_word(out + (tuple(image) if value > 0 else inverse(image)))
    return out


def f2_substitute(word: Sequence[int], left: Sequence[int], right: Sequence[int]) -> tuple[int, ...]:
    return substitute(word, (left, right))


def exponent_sums(word: Sequence[int], width: int = 2) -> list[int]:
    return [sum(1 if value == index else -1 if value == -index else 0 for value in word)
            for index in range(1, width + 1)]


def commutator(left: Sequence[int], right: Sequence[int]) -> tuple[int, ...]:
    return reduce_word(inverse(left) + inverse(right) + tuple(left) + tuple(right))


def construct_g760() -> tuple[int, ...]:
    parent = reduce_word(tuple(W2) + reduce_word(inverse(W3) + tuple(W2)) * 8)
    roof = (1,) * 108 + (-2,) * 36
    word = reduce_word(parent + inverse(roof))
    if len(parent) != 616 or digest_obj(list(parent)) != "3680e8bcbac37747467175454b082485b2ae296f1fb05244435d8f44979d4e90":
        fail(UNKNOWN_RAW, "g760 parent")
    if len(word) != 760 or digest_obj(list(word)) != "518f09820b8d7baee6b58ebf366cebf7b02a9a945cd1350cf8c701a4e6bc2b4d":
        fail(UNKNOWN_RAW, "g760 word")
    if exponent_sums(word) != [0, 0]:
        fail(UNKNOWN_RAW, "g760 exponent sums")
    return word


# -------------------- permutation / PC / quotient arithmetic --------------

Perm = bytes
Pc = bytes
Element = tuple[Perm, Pc]


def permutation(row: Sequence[int], degree: int) -> Perm:
    if len(row) != degree:
        fail(UNKNOWN_CONTEXT, "permutation degree")
    value = bytes(int(item) - 1 for item in row)
    if set(value) != set(range(degree)):
        fail(UNKNOWN_CONTEXT, "permutation bijection")
    return value


def perm_one(degree: int) -> Perm:
    return bytes(range(degree))


def perm_mul(left: Perm, right: Perm) -> Perm:
    if len(left) != len(right):
        fail(UNKNOWN_CONTEXT, "permutation product degree")
    return bytes(right[left[index]] for index in range(len(left)))


def perm_inv(value: Perm) -> Perm:
    out = [0] * len(value)
    for index, image in enumerate(value):
        out[image] = index
    return bytes(out)


def perm_eval(word: Sequence[int], generators: Sequence[Perm]) -> Perm:
    out = perm_one(len(generators[0]))
    inverses = [perm_inv(value) for value in generators]
    for letter in word:
        index = abs(int(letter)) - 1
        if not 0 <= index < len(generators):
            fail(UNKNOWN_CONTEXT, "permutation word index")
        out = perm_mul(out, generators[index] if letter > 0 else inverses[index])
    return out


def coords_word(coords: Sequence[int]) -> list[int]:
    return [index for index, exponent in enumerate(coords, 1) for _ in range(int(exponent))]


class PcCollector:
    def __init__(self, spec: dict[str, Any]):
        self.n = int(spec["generator_count"])
        self.orders = [int(x) for x in spec["relative_orders"]]
        if len(self.orders) != self.n or any(x != 3 for x in self.orders):
            fail(UNKNOWN_CONTEXT, "PC relative orders")
        self.powers = [self._coord(row) for row in spec["power_relations"]]
        self.inverses = [self._coord(row) for row in spec["inverses"]]
        self.conjugates = {(int(row["i"]), int(row["j"])): self._coord(row["coords"])
                           for row in spec["conjugate_relations"]}
        self.inverse_conjugates = {(int(row["i"]), int(row["j"])): self._coord(row["coords"])
                                   for row in spec["inverse_conjugate_relations"]}
        expected = self.n * (self.n - 1) // 2
        if len(self.conjugates) != expected or set(self.conjugates) != set(self.inverse_conjugates):
            fail(UNKNOWN_CONTEXT, "PC conjugate table")
        self.product_cache: dict[bytes, Pc] = {}
        self.inverse_cache: dict[Pc, Pc] = {}

    def _coord(self, row: Sequence[int]) -> Pc:
        if len(row) != self.n or any(type(x) is not int or not 0 <= x < 3 for x in row):
            fail(UNKNOWN_CONTEXT, "PC coordinate")
        return bytes(int(x) for x in row)

    def one(self) -> Pc:
        return bytes(self.n)

    def unit(self, index: int) -> Pc:
        if not 1 <= index <= self.n:
            fail(UNKNOWN_CONTEXT, "PC unit index")
        row = [0] * self.n
        row[index - 1] = 1
        return bytes(row)

    def collect(self, word: Sequence[int]) -> Pc:
        tokens = []
        for letter in word:
            index = abs(int(letter))
            if not 1 <= index <= self.n:
                fail(UNKNOWN_CONTEXT, "PC word index")
            tokens.extend([index] if letter > 0 else coords_word(self.inverses[index - 1]))
        steps = 0
        cap = max(10000, 1000 * (1 + len(tokens)) * (1 + self.n))
        while True:
            changed = False
            for pos in range(len(tokens) - 1):
                a, b = tokens[pos], tokens[pos + 1]
                if a > b:
                    if (a, b) not in self.conjugates:
                        fail(UNKNOWN_CONTEXT, "PC rewrite pair")
                    tokens[pos:pos + 2] = [b] + coords_word(self.conjugates[(a, b)])
                    changed = True
                    break
            if not changed:
                pos = 0
                while pos < len(tokens):
                    end = pos
                    while end < len(tokens) and tokens[end] == tokens[pos]:
                        end += 1
                    if end - pos >= 3:
                        tokens[pos:pos + 3] = coords_word(self.powers[tokens[pos] - 1])
                        changed = True
                        break
                    pos = end
            if not changed:
                break
            steps += 1
            if steps > cap:
                fail("UNKNOWN_RESOURCE:pc_collection", "rewrite cap")
        out = [0] * self.n
        last = 0
        for token in tokens:
            if token < last or not 1 <= token <= self.n:
                fail(UNKNOWN_CONTEXT, "PC normal form")
            out[token - 1] += 1
            if out[token - 1] >= 3:
                fail(UNKNOWN_CONTEXT, "PC power normal form")
            last = token
        return bytes(out)

    def mul(self, left: Pc, right: Pc) -> Pc:
        if len(left) != self.n or len(right) != self.n:
            fail(UNKNOWN_CONTEXT, "PC product width")
        key = left + right
        value = self.product_cache.get(key)
        if value is None:
            value = self.collect(coords_word(left) + coords_word(right))
            if len(self.product_cache) < 131072:
                self.product_cache[key] = value
        return value

    def inverse(self, value: Pc) -> Pc:
        if len(value) != self.n:
            fail(UNKNOWN_CONTEXT, "PC inverse width")
        cached = self.inverse_cache.get(value)
        if cached is not None:
            return cached
        word = []
        for index in range(self.n, 0, -1):
            for _ in range(value[index - 1]):
                word.extend(coords_word(self.inverses[index - 1]))
        answer = self.collect(word)
        if len(self.inverse_cache) < 65536:
            self.inverse_cache[value] = answer
        return answer

    def eval(self, word: Sequence[int], images: Sequence[Pc]) -> Pc:
        out = self.one()
        for letter in word:
            index = abs(int(letter)) - 1
            if not 0 <= index < len(images):
                fail(UNKNOWN_CONTEXT, "PC evaluation index")
            value = images[index]
            out = self.mul(out, value if letter > 0 else self.inverse(value))
        return out


class Quotient:
    def __init__(self, rank: int, degree: int, pc: PcCollector, generators: list[Element]):
        self.rank, self.degree, self.pc = rank, degree, pc
        self.generators = generators
        if len(generators) != rank * (rank - 1) // 2:
            fail(UNKNOWN_CONTEXT, "matched marked width")
        self.identity: Element = (perm_one(degree), pc.one())
        self.inverse_generators = [self.inverse(value) for value in generators]

    def mul(self, left: Element, right: Element) -> Element:
        return perm_mul(left[0], right[0]), self.pc.mul(left[1], right[1])

    def inverse(self, value: Element) -> Element:
        return perm_inv(value[0]), self.pc.inverse(value[1])

    def eval(self, word: Sequence[int], images: Sequence[Element] | None = None) -> Element:
        marked = self.generators if images is None else images
        out = self.identity
        for letter in word:
            index = abs(int(letter)) - 1
            if not 0 <= index < len(marked):
                fail(UNKNOWN_CONTEXT, "quotient word index")
            value = marked[index]
            out = self.mul(out, value if letter > 0 else self.inverse(value))
        return out


def element_blob(value: Element) -> bytes:
    return value[0] + value[1]


# --------- pure braid presentations and literal coface reconstruction ------

def pair_list(rank: int) -> list[list[int]]:
    return [[i, j] for i in range(1, rank) for j in range(i + 1, rank + 1)]


def pair_index(rank: int, pair: Sequence[int]) -> int:
    try:
        return pair_list(rank).index([int(pair[0]), int(pair[1])]) + 1
    except ValueError:
        fail(UNKNOWN_RAW, "pair index")


def artin_step(rank: int, letter: int) -> list[list[int]]:
    i = abs(int(letter))
    if not 1 <= i < rank:
        fail(UNKNOWN_RAW, "Artin index")
    images = [[j] for j in range(1, rank + 1)]
    if letter > 0:
        images[i - 1], images[i] = [i, i + 1, -i], [i]
    else:
        images[i - 1], images[i] = [i + 1], [-(i + 1), i, i + 1]
    return images


def artin_images(rank: int, braid: Sequence[int]) -> list[tuple[int, ...]]:
    images = [[j] for j in range(1, rank + 1)]
    for letter in braid:
        images = [list(substitute(word, artin_step(rank, letter))) for word in images]
    return [tuple(word) for word in images]


def aij_braid(i: int, j: int) -> list[int]:
    return list(range(j - 1, i, -1)) + [i, i] + [-k for k in range(i + 1, j)]


def pure_relations(rank: int) -> list[tuple[int, ...]]:
    if rank == 2:
        return []
    old_pairs = pair_list(rank - 1)
    old_map = [[pair_index(rank, pair)] for pair in old_pairs]
    relations = [substitute(word, old_map) for word in pure_relations(rank - 1)]
    kernel = [[pair_index(rank, [k, rank])] for k in range(1, rank)]
    for i, j in old_pairs:
        g = pair_index(rank, [i, j])
        action = artin_images(rank - 1, aij_braid(i, j))
        for k in range(1, rank):
            h = pair_index(rank, [k, rank])
            relations.append(reduce_word((-g, h, g) + inverse(substitute(action[k - 1], kernel))))
    return relations


def coface_generator(rank: int, slot: int, pair: Sequence[int]) -> list[int]:
    i, j = pair
    if slot == 0:
        return [pair_index(rank + 1, [i + 1, j + 1])]
    if slot == rank + 1:
        return [pair_index(rank + 1, [i, j])]
    if not 1 <= slot <= rank:
        fail(UNKNOWN_CONTEXT, "coface slot")
    if i == slot:
        return [pair_index(rank + 1, [slot, j + 1]), pair_index(rank + 1, [slot + 1, j + 1])]
    if j == slot:
        return [pair_index(rank + 1, [i, slot]), pair_index(rank + 1, [i, slot + 1])]
    return [pair_index(rank + 1, [i + int(i > slot), j + int(j > slot)])]


def cofaces(rank: int) -> list[list[list[int]]]:
    return [[coface_generator(rank, slot, pair) for pair in pair_list(rank)]
            for slot in range(rank + 2)]


def build_quotients(q3: dict[str, Any]) -> tuple[Quotient, Quotient, list[list[list[int]]]]:
    if q3.get("schema") != "d972-b345-q-chief/v1" or q3.get("terminal_token") != "B345_Q3_TYPED_SIGN_EXACT_WITH_WORD_CORRECTION":
        fail(UNKNOWN_CONTEXT, "q3 terminal")
    pc3 = PcCollector(q3["groups"]["PB3"])
    pc4 = PcCollector(q3["groups"]["PB4"])
    p3 = [pc3._coord(row["coords"]) for row in q3["groups"]["PB3"]["marked_generators"]]
    p4 = [pc4._coord(row["coords"]) for row in q3["groups"]["PB4"]["marked_generators"]]
    q0_model, q4_model = q3["coarse_models"]["Q0"], q3["coarse_models"]["Q4"]
    q0 = [permutation(row, int(q0_model["degree"])) for row in q0_model["marked_permutations"]]
    q4 = [permutation(row, int(q4_model["degree"])) for row in q4_model["marked_permutations"]]
    if len(q0) != 2 or len(q4) != 6:
        fail(UNKNOWN_CONTEXT, "coarse marked width")
    e3 = Quotient(3, int(q0_model["degree"]), pc3,
                  [(q0[0], p3[0]), (perm_mul(q0[1], q0[0]), p3[1]), (q0[1], p3[2])])
    e4 = Quotient(4, int(q4_model["degree"]), pc4, list(zip(q4, p4)))
    rel3, rel4 = pure_relations(3), pure_relations(4)
    if len(rel3) != 2 or len(rel4) != 11:
        fail(UNKNOWN_CONTEXT, "pure relation cardinality")
    if any(e3.eval(row) != e3.identity for row in rel3):
        fail(UNKNOWN_PB3, "PB3 presentation replay")
    if any(e4.eval(row) != e4.identity for row in rel4):
        fail(UNKNOWN_FOX, "PB4 presentation replay")
    maps = cofaces(3)
    if maps != q3.get("formulas", {}).get("cofaces_3_4"):
        fail(UNKNOWN_CONTEXT, "coface data drift")
    return e3, e4, maps


# ------------------------- v122 context/retraction ------------------------

def product_elements(quotient: Quotient, values: Sequence[Element]) -> Element:
    out = quotient.identity
    for value in values:
        out = quotient.mul(out, value)
    return out


def paper_product_elements(quotient: Quotient, values: Sequence[Element]) -> Element:
    """Evaluate displayed factors in the paper (right-to-left) order."""
    return product_elements(quotient, list(reversed(values)))


def eval_f2(quotient: Quotient, word: Sequence[int]) -> Element:
    return quotient.eval(substitute(word, ([1], [3]))) if quotient.rank == 3 else quotient.eval(word)


def context_registry(e4: Quotient, maps: list[list[list[int]]]) -> tuple[list[tuple[Element, Element]], dict[str, int], dict[str, Any]]:
    contexts, exact, aliases, named = [], {}, {}, []
    def add(name: str, left: Element, right: Element) -> None:
        if name in aliases:
            fail(UNKNOWN_CONTEXT, "duplicate context name")
        pair = (left, right)
        context_id = exact.get(pair)
        if context_id is None:
            context_id = len(contexts) + 1
            exact[pair] = context_id
            contexts.append(pair)
        aliases[name] = context_id
        named.append({"name": name, "context_id": context_id})
    for slot, mapping in enumerate(maps):
        x, y = e4.eval(mapping[0]), e4.eval(mapping[2])
        z, u = e4.inverse(paper_product_elements(e4, [x, y])), e4.inverse(paper_product_elements(e4, [y, x]))
        for name, left, right in ((f"correction_coface_{slot}", x, y),
            (f"hexagon_1_fxy_{slot}", x, y), (f"hexagon_1_fxz_{slot}", x, z),
            (f"hexagon_1_fyz_{slot}", y, z), (f"hexagon_2_fux_{slot}", u, x),
            (f"hexagon_2_fxy_{slot}", x, y), (f"hexagon_2_fuy_{slot}", u, y)):
            add(name, left, right)
    g = e4.generators
    pent = [(g[0], g[3]), (g[3], g[5]),
            (paper_product_elements(e4, [g[1], g[3]]), g[5]),
            (paper_product_elements(e4, [g[0], g[1]]), paper_product_elements(e4, [g[4], g[5]])),
            (g[0], paper_product_elements(e4, [g[3], g[4]]))]
    for index, (left, right) in enumerate(pent):
        add(f"pentagon_part_{index}", left, right)
    source = [("source_ff", g[0], g[3]), ("source_g", g[0], g[1]),
              ("source_gs", g[3], g[4]), ("source_f1234", product_elements(e4, [g[3], g[1]]), g[5]),
              ("source_h", product_elements(e4, [g[1], g[0]]), g[2]),
              ("source_middle", product_elements(e4, [g[1], g[0]]), product_elements(e4, [g[5], g[4]]))]
    for name, left, right in source:
        add(name, left, right)
    rows = [{"context_id": index, "left_hex": element_blob(pair[0]).hex(),
             "right_hex": element_blob(pair[1]).hex()} for index, pair in enumerate(contexts, 1)]
    public = {"context_count": len(contexts), "contexts": rows, "named_uses": named,
              "named_use_count": len(named), "named_use_mapping_sha256": digest_obj(named),
              "context_rows_sha256": digest_obj(rows), "deduplication": "exact E4 pair equality"}
    if len(contexts) != 31 or len(named) != 46:
        fail(UNKNOWN_CONTEXT, "context registry cardinality")
    return contexts, aliases, public


def restrict_coarse(perm: Perm) -> Perm:
    first = [int(perm[index]) - 27 for index in range(27, 36)]
    second = [int(perm[index]) - 117 + 9 for index in range(117, 144)]
    if sorted(first) != list(range(9)) or sorted(second) != list(range(9, 36)):
        fail(UNKNOWN_CONTEXT, "coarse fourth block projection")
    return bytes(first + second)


def reconstruct_retraction(e3: Quotient, e4: Quotient, contexts: list[tuple[Element, Element]], aliases: dict[str, int], mutation: str | None = None) -> dict[str, Any]:
    expected = [e3.generators[0][0], e3.generators[1][0], perm_one(36), e3.generators[2][0], perm_one(36), perm_one(36)]
    coarse = [restrict_coarse(value[0]) for value in e4.generators]
    if coarse != expected:
        fail(UNKNOWN_CONTEXT, "coarse marked image")
    steps = [value[1] for value in e4.generators]
    targets = [e3.generators[0][1], e3.generators[1][1], e3.pc.one(), e3.generators[2][1], e3.pc.one(), e3.pc.one()]
    all_steps = steps + [e4.pc.inverse(value) for value in steps]
    all_targets = targets + [e3.pc.inverse(value) for value in targets]
    table: dict[Pc, Pc] = {e4.pc.one(): e3.pc.one()}
    queue = [e4.pc.one()]
    head = 0
    while head < len(queue):
        source = queue[head]; head += 1
        for step, target in zip(all_steps, all_targets):
            nxt, image = e4.pc.mul(source, step), e3.pc.mul(table[source], target)
            if nxt in table and table[nxt] != image:
                fail(UNKNOWN_CONTEXT, "fine map conflict")
            if nxt not in table:
                table[nxt] = image; queue.append(nxt)
            if len(table) > 59049:
                fail(UNKNOWN_CONTEXT, "fine map cap")
    if len(table) != 59049 or len(set(table.values())) != 81:
        fail(UNKNOWN_CONTEXT, "fine map order")
    def d_element(value: Element) -> Element:
        if value[1] not in table:
            fail(UNKNOWN_CONTEXT, "fine map element")
        return restrict_coarse(value[0]), table[value[1]]
    insertion, deletion = [[1], [2], [4]], [[1], [2], [], [3], [], []]
    if mutation == "fourth_third_deletion_swap":
        deletion = [[1], [2], [], [], [3], []]
    if mutation == "fine_insertion_index_4_3_swap":
        insertion = [[1], [2], [3]]
    marks = []
    for mark, image in enumerate(insertion, 1):
        inserted = e4.eval(image); deleted_word = substitute(image, deletion)
        deleted, expected_mark, mapped = e3.eval(deleted_word), e3.eval([mark]), d_element(inserted)
        if deleted != expected_mark or mapped != expected_mark:
            fail(UNKNOWN_CONTEXT, "d_E i_E marked generator")
        marks.append({"mark": mark, "inserted_blob": element_blob(inserted).hex(),
                      "deleted_blob": element_blob(deleted).hex(), "formal_deleted_blob": element_blob(deleted).hex(),
                      "d_element_blob": element_blob(mapped).hex(), "expected_blob": element_blob(expected_mark).hex()})
    preimages = []
    for index in range(1, e3.pc.n + 1):
        expected_pc = e3.pc.unit(index)
        source = next((source for source, image in table.items() if image == expected_pc), None)
        if source is None:
            fail(UNKNOWN_CONTEXT, "fine PB3 PC generator image")
        preimages.append({"index": index, "input": source.hex(), "output": expected_pc.hex()})
    required = {21: "hexagon_1_fxy_4", 22: "hexagon_1_fxz_4", 23: "hexagon_1_fyz_4", 24: "hexagon_2_fux_4", 25: "hexagon_2_fuy_4"}
    if aliases.get("hexagon_2_fxy_4") != 21:
        fail(UNKNOWN_CONTEXT, "registry alias 21")
    xword, yword = [1], [2]
    zword, uword = inverse(paper_product(xword, yword)), inverse(paper_product(yword, xword))
    expected_pairs = [(xword, yword), (xword, zword), (yword, zword), (uword, xword), (uword, yword)]
    registry = []
    for registry_id, alias in required.items():
        if aliases.get(alias) != registry_id or registry_id > len(contexts):
            fail(UNKNOWN_CONTEXT, "registry bridge alias")
        left4, right4 = contexts[registry_id - 1]
        left3, right3 = d_element(left4), d_element(right4)
        expected_left, expected_right = eval_f2(e3, expected_pairs[registry_id - 21][0]), eval_f2(e3, expected_pairs[registry_id - 21][1])
        if left3 != expected_left or right3 != expected_right:
            fail(UNKNOWN_CONTEXT, "registry deletion blob")
        registry.append({"registry_id": registry_id, "input_left": element_blob(left4).hex(),
                         "input_right": element_blob(right4).hex(), "output_left": element_blob(left3).hex(),
                         "output_right": element_blob(right3).hex(), "expected_left": element_blob(expected_left).hex(),
                         "expected_right": element_blob(expected_right).hex()})
    return {"insertion_pb4_indices": insertion, "deletion_pb4_to_pb3": deletion, "marks": marks,
            "pc_generator_blobs": [e3.pc.unit(i).hex() for i in range(1, e3.pc.n + 1)],
            "pc_generator_preimages": preimages, "d_E_i_E_marks": True,
            "coarse_marked_images": [list(value) for value in coarse], "fine_domain_order": len(table),
            "fine_image_order": len(set(table.values())), "registry_replay": registry,
            "coarse_projection": {"P_block": "fourth", "G9_block": "fourth",
                                  "input_blobs": [row["inserted_blob"] for row in marks],
                                  "output_blobs": [row["deleted_blob"] for row in marks]}}


# ---------------- literal formulas, left Fox, D1, and D2 ------------------

def hexagon_words(word: Sequence[int]) -> tuple[tuple[int, ...], tuple[int, ...]]:
    x, y = (1,), (2,); z, u = inverse(paper_product(x, y)), inverse(paper_product(y, x))
    fxy, fxz, fyz = f2_substitute(word, x, y), f2_substitute(word, x, z), f2_substitute(word, y, z)
    fux, fuy = f2_substitute(word, u, x), f2_substitute(word, u, y)
    return paper_product(fxy, inverse(fxz), fyz), paper_product(inverse(fux), inverse(fxy), fuy)


def embed_pb3(word: Sequence[int]) -> tuple[int, ...]:
    return substitute(word, ([1], [3]))


def pentagon_context_words() -> list[tuple[tuple[int, ...], tuple[int, ...]]]:
    g = [(index,) for index in range(1, 7)]
    return [(g[0], g[3]), (g[3], g[5]), (paper_product(g[1], g[3]), g[5]),
            (paper_product(g[0], g[1]), paper_product(g[4], g[5])),
            (g[0], paper_product(g[3], g[4]))]


def pentagon_word(word: Sequence[int]) -> tuple[int, ...]:
    parts = [f2_substitute(word, left, right) for left, right in pentagon_context_words()]
    # Fresh literal constructor for the printed word
    # b1*b2*b3*b5^-1*b4^-1.  The natural inventory order is
    # (b3,b1,b5,b2,b4), hence indices (1,3,0,2,4) and signs (+++--).
    return paper_product(parts[1], parts[3], parts[0], inverse(parts[2]), inverse(parts[4]))


def add_term(target: dict[tuple[int, Element], int], key: tuple[int, Element], value: int) -> None:
    coefficient = int(value) % 3
    if not coefficient:
        return
    result = (target.get(key, 0) + coefficient) % 3
    if result:
        target[key] = result
    else:
        target.pop(key, None)


def add_scaled(target: dict[Any, int], source: dict[Any, int], scale: int) -> None:
    for key, value in source.items():
        result = (target.get(key, 0) + int(scale) * int(value)) % 3
        if result:
            target[key] = result
        else:
            target.pop(key, None)


def fox(quotient: Quotient, word: Sequence[int]) -> tuple[dict[tuple[int, Element], int], Element]:
    prefix = quotient.identity; gradient = {}
    for letter in word:
        index = abs(int(letter))
        if not 1 <= index <= len(quotient.generators):
            fail(UNKNOWN_FOX, "Fox component")
        if letter > 0:
            add_term(gradient, (index, prefix), 1)
            prefix = quotient.mul(prefix, quotient.generators[index - 1])
        else:
            prefix = quotient.mul(prefix, quotient.inverse_generators[index - 1])
            add_term(gradient, (index, prefix), 2)
    return gradient, prefix


def d1(vector: dict[tuple[int, Element], int], quotient: Quotient) -> dict[Element, int]:
    result = {}
    for (component, value), coefficient in vector.items():
        add_scaled(result, {quotient.mul(value, quotient.generators[component - 1]): 1, value: 2}, coefficient)
    return result


def translate(vector: dict[tuple[int, Element], int], translation: Element, quotient: Quotient) -> dict[tuple[int, Element], int]:
    result = {}
    for (component, value), coefficient in vector.items():
        add_term(result, (component, quotient.mul(translation, value)), coefficient)
    return result


def serial_row(vector: dict[tuple[int, Element], int]) -> list[list[Any]]:
    rows = [[int(component), element_blob(value).hex(), int(coefficient) % 3]
            for (component, value), coefficient in vector.items() if int(coefficient) % 3]
    return sorted(rows, key=lambda row: (row[0], bytes.fromhex(row[1])))


def raw_difference(quotient: Quotient, base: Sequence[int], corrected: Sequence[int], embed: Any = None):
    left, right = tuple(base) if embed is None else embed(base), tuple(corrected) if embed is None else embed(corrected)
    bg, bv = fox(quotient, left)
    cg, cv = fox(quotient, right)
    if bv != quotient.identity or cv != quotient.identity:
        fail(UNKNOWN_RAW, "raw relation quotient value")
    result = dict(cg); add_scaled(result, bg, -1)
    return result, bv, cv


def product_gradient(quotient: Quotient, factors: Sequence[Sequence[int]], embed: Any = None, reverse_translation: bool = False):
    prefix, result = quotient.identity, {}
    for factor in reversed(factors):
        word = tuple(factor) if embed is None else embed(factor)
        gradient, value = fox(quotient, word)
        transport = quotient.inverse(prefix) if reverse_translation else prefix
        add_scaled(result, translate(gradient, transport, quotient), 1)
        prefix = quotient.mul(prefix, value)
    return result, prefix


def prefix_difference(quotient: Quotient, base: Sequence[Sequence[int]], corrected: Sequence[Sequence[int]], embed: Any = None, reverse_translation: bool = False):
    bg, bv = product_gradient(quotient, base, embed, reverse_translation)
    cg, cv = product_gradient(quotient, corrected, embed, reverse_translation)
    result = dict(cg); add_scaled(result, bg, -1)
    return result, bv, cv


def complete_relators() -> list[tuple[int, ...]]:
    p_rows = [f2_substitute(row, SPLIT_WORDS[0], SPLIT_WORDS[1]) for row in P_RELATORS]
    g_rows = [f2_substitute(row, SPLIT_WORDS[2], SPLIT_WORDS[3]) for row in G9_RELATORS]
    rows = p_rows + g_rows + [commutator(a, b) for a in SPLIT_WORDS[:2] for b in SPLIT_WORDS[2:]]
    rows += [reduce_word((1,) + inverse(reduce_word(SPLIT_WORDS[0] + SPLIT_WORDS[2]))),
             reduce_word((2,) + inverse(reduce_word(SPLIT_WORDS[1] + SPLIT_WORDS[3])))]
    if (len(rows) != 19 or
            digest_obj([list(row) for row in rows]) != COMPLETE_RELATORS_SHA):
        fail(UNKNOWN_RAW, "Q0 relator count")
    return rows


def build_d2(e3: Quotient, e4: Quotient):
    pb3, pb4 = [], []
    for relator in pure_relations(3):
        gradient, value = fox(e3, relator)
        if value != e3.identity or d1(gradient, e3):
            fail(UNKNOWN_PB3, "PB3 D2 value/D1")
        pb3.append(serial_row(gradient))
    for relator in pure_relations(4):
        gradient, value = fox(e4, relator)
        if value != e4.identity or d1(gradient, e4):
            fail(UNKNOWN_FOX, "PB4 D2 value/D1")
        pb4.append(serial_row(gradient))
    return pb3, pb4, [digest_obj(row) for row in pb3], [digest_obj(row) for row in pb4]


# --------------------- 243-state joint roster ------------------------------

class Joint:
    def __init__(self, e3: Quotient, e4: Quotient, contexts: list[tuple[Element, Element]], records: list[tuple[int, ...]]):
        self.e3, self.e4, self.contexts, self.records = e3, e4, contexts, records
        self.identity = (e3.identity, tuple(e4.identity for _ in contexts))
        self.generators = [self.eval(word) for word in records]
        self.states, self.ids = [self.identity], {self.key(self.identity): 0}
        self.parents, self.parent_generators = [None], [None]
        state_id = 0
        while state_id < len(self.states):
            state = self.states[state_id]
            for generator_id, generator in enumerate(self.generators):
                value = self.mul(state, generator); key = self.key(value)
                if key not in self.ids:
                    self.ids[key] = len(self.states); self.states.append(value)
                    self.parents.append(state_id); self.parent_generators.append(generator_id)
            state_id += 1
            if len(self.states) > 243:
                fail(UNKNOWN_RAW, "joint state cap")
        if len(self.states) != 243:
            fail(UNKNOWN_RAW, "joint state count")
        self.transitions = [[self.ids[self.key(self.mul(state, generator))] for generator in self.generators]
                            for state in self.states]

    def key(self, state):
        return (element_blob(state[0]),) + tuple(element_blob(value) for value in state[1])

    def mul(self, left, right):
        return (self.e3.mul(left[0], right[0]), tuple(self.e4.mul(left[1][i], right[1][i]) for i in range(len(self.contexts))))

    def inverse(self, value):
        return self.e3.inverse(value[0]), tuple(self.e4.inverse(item) for item in value[1])

    def eval(self, word):
        return eval_f2(self.e3, word), tuple(self.e4.eval(word, (left, right)) for left, right in self.contexts)

    def section_factors(self, state_id: int) -> list[int]:
        result = []
        while state_id:
            generator, parent = self.parent_generators[state_id], self.parents[state_id]
            if generator is None or parent is None:
                fail(UNKNOWN_RAW, "joint section parent")
            result.append(generator); state_id = parent
        result.reverse(); return result

    def section_word(self, state_id: int) -> tuple[int, ...]:
        out = ()
        for generator in self.section_factors(state_id):
            out = reduce_word(out + self.records[generator])
        return out


def token_word(records, token):
    kind, index, sign = token
    word = tuple(records[index]) if kind == "record" else (index + 1,)
    return word if sign > 0 else inverse(word)


def materialize_tokens(records, tokens):
    out = ()
    for token in tokens:
        out = reduce_word(out + token_word(records, token))
    return out


def load_records(q3, joint_receipt: dict[str, Any] | None = None):
    records = [tuple(int(value) for value in row.get("word", [])) for row in q3["correction_fibre"]["records"] if row.get("word")]
    if len(records) != 26 or any(not word for word in records):
        fail(UNKNOWN_RAW, "correction record count")
    words_digest = digest_obj([list(word) for word in records])
    if words_digest != "08d11c68dcbacc1b81e5e2732eedcbc41df82a16c8a0f97dfbbb13d6accee24f":
        fail(UNKNOWN_RAW, "correction record digest")
    if joint_receipt is not None:
        manifest = joint_receipt.get("record_manifest", {})
        q0 = joint_receipt.get("q0_presentation", {})
        action = joint_receipt.get("action_relations", {})
        gamma = joint_receipt.get("gamma", {})
        if (joint_receipt.get("schema") != "d972-b345-joint-kernel-qstar-closure/v1" or
                joint_receipt.get("terminal_token") != "B345_JOINT_KERNEL_QSTAR_CLOSED" or
                manifest.get("record_count") != 26 or
                manifest.get("words_sha256") != words_digest or
                q0.get("complete_relator_count") != 19 or
                q0.get("complete_relators_sha256") != COMPLETE_RELATORS_SHA or
                action.get("row_count") != 104 or gamma.get("order") != 243):
            fail(UNKNOWN_RAW, "157ee record/q0 receipt")
    return records


def build_roster(joint: Joint):
    rows = []
    for state_id, transitions in enumerate(joint.transitions):
        section = joint.section_word(state_id)
        for generator_id, target in enumerate(transitions):
            rows.append({"layer": "gamma_edge", "ordinal": state_id * 26 + generator_id + 1,
                         "word": list(reduce_word(section + joint.records[generator_id] + inverse(joint.section_word(target))))})
    for record in range(26):
        for letter in range(2):
            value = joint.eval([letter + 1]); generator = joint.generators[record]
            for orientation in (1, -1):
                if orientation == 1:
                    conjugate = joint.mul(joint.mul(joint.inverse(value), generator), value)
                    tokens = [("letter", letter, -1), ("record", record, 1), ("letter", letter, 1)]
                else:
                    conjugate = joint.mul(joint.mul(value, generator), joint.inverse(value))
                    tokens = [("letter", letter, 1), ("record", record, 1), ("letter", letter, -1)]
                target = joint.ids[joint.key(conjugate)]
                tokens += [("record", index, -1) for index in reversed(joint.section_factors(target))]
                rows.append({"layer": "xy_action", "ordinal": record * 4 + letter * 2 + (1 if orientation == 1 else 2),
                             "word": list(materialize_tokens(joint.records, tokens))})
    for ordinal, relator in enumerate(complete_relators(), 1):
        target = joint.ids[joint.key(joint.eval(relator))]
        rows.append({"layer": "q0_relator", "ordinal": ordinal,
                     "word": list(reduce_word(relator + inverse(joint.section_word(target))))})
    # The expanded roster is lossless: a free-reduced relation may be the
    # empty word.  Nonempty is required only for the selected correction and
    # the actual Fox-canary samples below.
    if len(rows) != CAP:
        fail(UNKNOWN_RAW, "roster count")
    # Materialization is not accepted on section provenance alone: replay the
    # complete signed word roster in the local joint quotient.
    if any(joint.eval(row["word"]) != joint.identity for row in rows):
        fail(UNKNOWN_RAW, "roster joint evaluation")
    return rows


def roster_digest(rows):
    return digest_obj([[row["layer"], row["ordinal"], row["word"]] for row in rows])


def roster_provenance(joint: Joint, row: dict[str, Any]) -> dict[str, Any]:
    """Decode the deterministic row ordinal into its source witness."""
    layer, ordinal = row["layer"], int(row["ordinal"])
    if layer == "gamma_edge":
        state_id, generator_id = divmod(ordinal - 1, 26)
        target = joint.transitions[state_id][generator_id]
        return {"layer": layer, "state_id": state_id,
                "generator_id": generator_id, "record_index": generator_id,
                "section_source_factors": joint.section_factors(state_id),
                "section_target_factors": joint.section_factors(target)}
    if layer == "xy_action":
        record_index, rem = divmod(ordinal - 1, 4)
        letter_index, orientation_bit = divmod(rem, 2)
        return {"layer": layer, "record_index": record_index,
                "letter_index": letter_index,
                "orientation": 1 if orientation_bit == 0 else -1}
    if layer == "q0_relator":
        return {"layer": layer, "relator_index": ordinal - 1}
    fail(UNKNOWN_RAW, "roster provenance layer")


# ---------------- all eleven slots and actual word-bearing canaries --------

def slot_specs(e3: Quotient, e4: Quotient):
    x, y = (1,), (2,); z, u = inverse(paper_product(x, y)), inverse(paper_product(y, x))
    slots = [("H1", "H1_fxy", 1, e3, x, y, 1, embed_pb3), ("H1", "H1_fxz", 1, e3, x, z, -1, embed_pb3),
             ("H1", "H1_fyz", 1, e3, y, z, 1, embed_pb3), ("H2", "H2_fux", 2, e3, u, x, -1, embed_pb3),
             ("H2", "H2_fxy", 2, e3, x, y, -1, embed_pb3), ("H2", "H2_fuy", 2, e3, u, y, 1, embed_pb3)]
    # The literal pentagon factors are stored in natural context order
    # (b3,b1,b5,b2,b4), but the five printed occurrences are b1,b2,b3,
    # b5^-1,b4^-1.  Keep this occurrence order in every canary transcript.
    for index in (1, 3, 0, 2, 4):
        left, right = pentagon_context_words()[index]
        label = {0: "b3", 1: "b1", 2: "b5", 3: "b2", 4: "b4"}[index]
        slots.append(("P", "P_" + label + ("_inverse" if index in (2, 4) else ""), 3, e4, left, right, -1 if index in (2, 4) else 1, None))
    return [{"block": block, "name": name, "block_tag": tag, "quotient": quotient, "left": tuple(left), "right": tuple(right), "factor_sign": sign, "embed": embed}
            for block, name, tag, quotient, left, right, sign, embed in slots]


def canaries(e3: Quotient, e4: Quotient, rows, mutation: str | None = None):
    specs, selected = slot_specs(e3, e4), [row for layer, count in (("gamma_edge", 4), ("xy_action", 3), ("q0_relator", 3)) for row in [x for x in rows if x["layer"] == layer and x.get("word")][:count]]
    if len(selected) != 10:
        fail(UNKNOWN_FOX, "canary layer selection")
    conjugators = [(1,), (-1,), (2,), (-2,), (1, 2), (-2, -1), (1, 1, 2, -1), (2, 1, -2, -1), (1, -2, 1)]
    transcript = []
    for slot_index, spec in enumerate(specs):
        q = spec["quotient"]
        lift = spec["embed"] or (lambda word: tuple(word))
        for local_index, row in enumerate(selected):
            relation = lift(f2_substitute(row["word"], spec["left"], spec["right"]))
            if spec["factor_sign"] < 0:
                relation = inverse(relation)
            conjugator = conjugators[(slot_index * 10 + local_index) % len(conjugators)]
            qword = lift(f2_substitute(conjugator, spec["left"], spec["right"]))
            conjugated = reduce_word(qword + relation + inverse(qword))
            direct, direct_value = fox(q, conjugated); base, base_value = fox(q, relation)
            predicted = translate(base, q.eval(qword), q)
            if direct_value != q.identity or base_value != q.identity or direct != predicted:
                fail(UNKNOWN_FOX, "slot conjugation mismatch")
            transcript.append({"slot": slot_index + 1, "slot_name": spec["name"], "block": spec["block"], "block_tag": spec["block_tag"], "factor_sign": spec["factor_sign"],
                "layer": row["layer"], "ordinal": row["ordinal"], "u": list(conjugator), "u_length": len(conjugator), "r_word": list(row["word"]), "r_length": len(row["word"]),
                "relation_word": list(relation), "conjugated_word": list(conjugated), "direct": serial_row(direct), "predicted": serial_row(predicted)})
    if len(transcript) != 110:
        fail(UNKNOWN_FOX, "canary count")
    slot_counts = {str(index): sum(item["slot"] == index for item in transcript) for index in range(1, 12)}
    layer_counts = {layer: sum(item["layer"] == layer for item in transcript) for layer in ("gamma_edge", "xy_action", "q0_relator")}
    if any(value < 10 for value in slot_counts.values()) or any(value == 0 for value in layer_counts.values()):
        fail(UNKNOWN_FOX, "canary strata")
    same_context = []
    base_relation = tuple(selected[0]["word"])
    for krow in rows:
        if len(same_context) >= 2:
            break
        kernel = tuple(krow["word"]); u = (1,); v = reduce_word(u + kernel)
        c1, c2 = reduce_word(u + base_relation + inverse(u)), reduce_word(v + base_relation + inverse(v))
        if v == u or c1 == c2:
            continue
        tagged1, tagged2, equal = [], [], True
        for spec in specs:
            q = spec["quotient"]; lift = spec["embed"] or (lambda word: tuple(word))
            uv = q.eval(lift(f2_substitute(u, spec["left"], spec["right"])))
            vv = q.eval(lift(f2_substitute(v, spec["left"], spec["right"])))
            equal &= uv == vv
            g1, _ = fox(q, lift(f2_substitute(c1, spec["left"], spec["right"])))
            g2, _ = fox(q, lift(f2_substitute(c2, spec["left"], spec["right"])))
            tagged1.extend([[spec["block_tag"], *entry] for entry in serial_row(g1)])
            tagged2.extend([[spec["block_tag"], *entry] for entry in serial_row(g2)])
        if equal and sorted(tagged1) == sorted(tagged2):
            same_context.append({"r_layer": selected[0]["layer"], "r_ordinal": selected[0]["ordinal"], "r_word": list(base_relation), "k_layer": krow["layer"], "k_ordinal": krow["ordinal"], "k_word": list(kernel), "u": list(u), "v": list(v), "conjugate_u": list(c1), "conjugate_v": list(c2), "conjugates_differ": True, "complete_context_equal": True, "tagged_row_sha256": digest_obj([sorted(tagged1), sorted(tagged2)])})
    if len(same_context) < 2:
        fail(UNKNOWN_FOX, "same complete context quota")
    spec = specs[0]; lift = spec["embed"] or (lambda word: tuple(word))
    a = lift(f2_substitute(selected[1]["word"], spec["left"], spec["right"]))
    q, b = spec["quotient"], lift(f2_substitute(selected[2]["word"], spec["left"], spec["right"]))
    ga, va = fox(q, a); gb, vb = fox(q, b); gab, vab = fox(q, a + b)
    predicted_add = dict(ga); add_scaled(predicted_add, translate(gb, va, q), 1)
    if mutation == "actual_product_additivity_term":
        # This is deliberately a mutation of the evaluated product column,
        # before the direct-vs-product identity is checked.
        before = dict(gab)
        add_term(gab, (1, q.identity), 1)
        if gab == before:
            fail(UNKNOWN_FOX, "additivity mutation cancelled")
    if va != q.identity or vb != q.identity or vab != q.identity or gab != predicted_add:
        fail(UNKNOWN_FOX, "actual-product additivity")
    additivity = {"status": "PASS", "slot": spec["name"], "layer_a": selected[1]["layer"], "ordinal_a": selected[1]["ordinal"], "layer_b": selected[2]["layer"], "ordinal_b": selected[2]["ordinal"], "word_a": list(a), "word_b": list(b), "product_word": list(a + b), "direct": serial_row(gab), "predicted": serial_row(predicted_add), "equal": True}
    digest = digest_obj([{"slot": item["slot"], "layer": item["layer"], "ordinal": item["ordinal"], "direct": item["direct"], "predicted": item["predicted"]} for item in transcript])
    return {"status": "PASS", "pairs": len(transcript), "required": 110, "slot_counts": slot_counts, "layer_counts": layer_counts, "transcript": transcript, "row_digest_sha256": digest, "same_context_pairs": len(same_context), "same_context": same_context, "actual_product_additivity": additivity,
            "convention": {"formula": "left Fox; q*r*q^-1", "left_translation": True, "all_eleven_slots": True, "nonempty_conjugators": True, "inverse_slots": ["H1_fxz", "H2_fux", "H2_fxy", "P_b5_inverse", "P_b4_inverse"]}}


# ----------------------- complete checker reconstruction -------------------

def reconstruct(cert: dict[str, Any], mutation: str | None = None):
    q3 = read_json(Q3_REL)
    # The 157ee receipt is authenticated as immutable data and supplies the
    # record/q0/action cardinality witness.  No code is loaded from it.
    joint_receipt = read_json(JOINT_REL)
    if mutation == "E3_E4_rank_swap":
        # Change a load-bearing collector rank before any derived object is
        # built.  The local collector must reject the inconsistent schema.
        q3 = copy.deepcopy(q3)
        q3["groups"]["PB3"]["generator_count"] = 10
    elif mutation == "E3_E4_blob_swap":
        # Swap two marked PC blobs and replay all downstream presentations and
        # maps; this is not a receipt/digest-only mutation.
        q3 = copy.deepcopy(q3)
        marked = q3["groups"]["PB3"]["marked_generators"]
        marked[0]["coords"], marked[1]["coords"] = marked[1]["coords"], marked[0]["coords"]
    e3, e4, maps = build_quotients(q3)
    if mutation == "coface_slot_1_3_swap":
        maps[1], maps[3] = maps[3], maps[1]
    contexts, aliases, context_public = context_registry(e4, maps)
    if mutation == "context_name_only_dedup":
        # A name-only registry loses one exact pair but leaves old aliases;
        # the subsequent bridge replay must reject the stale registry IDs.
        contexts = contexts[:-1]
        if len(contexts) != context_public["context_count"]:
            fail(UNKNOWN_CONTEXT, "name-only context deduplication")
    retraction = reconstruct_retraction(e3, e4, contexts, aliases, mutation)
    records, joint = load_records(q3, joint_receipt), None
    joint = Joint(e3, e4, contexts, records); rows = build_roster(joint); g = construct_g760()
    if mutation == "actual_roster_letter":
        target = next((row for row in sorted(
            rows, key=lambda row: (row["layer"], row["ordinal"], row["word"]))
                       if row.get("word")), None)
        if target is None:
            fail(UNKNOWN_RAW, "roster mutation empty")
        target["word"][0] = -int(target["word"][0])
    ordered = sorted(rows, key=lambda row: (row["layer"], row["ordinal"], row["word"]))
    correction_row = next((row for row in ordered if row.get("word")), None)
    if correction_row is None:
        fail(UNKNOWN_RAW, "registered canary empty roster")
    correction = tuple(correction_row["word"])
    if joint.eval(correction) != joint.identity:
        fail(UNKNOWN_RAW, "registered canary joint identity")
    # The canonical correction is always retained.  The mutation changes the
    # load-bearing side of the corrected-word product itself; it must not
    # smuggle g into the registered correction and then multiply twice.
    f1 = (reduce_word(correction + g) if mutation == "correction_left_right"
          else reduce_word(g + correction)); x, y = (1,), (2,)
    z = inverse(paper_product(x, y)); u = inverse(paper_product(y, x))
    if mutation == "derived_u_order":
        u = inverse(paper_product(x, y))
    if mutation == "derived_z_order":
        z = inverse(paper_product(y, x))
    hbase, hcorr = hexagon_words(g), hexagon_words(f1)
    h1_base, h2_base, h1_corr, h2_corr = embed_pb3(hbase[0]), embed_pb3(hbase[1]), embed_pb3(hcorr[0]), embed_pb3(hcorr[1])
    source_pairs = [(x, y), (x, z), (y, z), (u, x), (u, y)]
    source_blobs = [{"left_blob": element_blob(eval_f2(e3, left)).hex(), "right_blob": element_blob(eval_f2(e3, right)).hex()} for left, right in source_pairs]
    if any(e3.eval(word) != e3.identity for word in (h1_corr, h2_corr)):
        fail(UNKNOWN_CONTEXT, "source H1/H2 identity")
    factor_contexts = pentagon_context_words(); factor_words_base = [f2_substitute(g, left, right) for left, right in factor_contexts]; factor_words_corr = [f2_substitute(f1, left, right) for left, right in factor_contexts]
    factor_values_base, factor_values_corr = [e4.eval(word) for word in factor_words_base], [e4.eval(word) for word in factor_words_corr]
    indices, signs = [1, 3, 0, 2, 4], [1, 1, 1, -1, -1]
    if mutation == "negative_pentagon_order": indices = [1, 3, 0, 4, 2]
    if mutation == "negative_pentagon_factor_4": signs = [1, 1, 1, 1, -1]
    if mutation == "negative_pentagon_factor_5": signs = [1, 1, 1, -1, 1]
    ordered_values = [value if sign > 0 else e4.inverse(value) for value, sign in ((factor_values_corr[index], sign) for index, sign in zip(indices, signs))]
    multiplication_order = list(reversed(ordered_values))
    product, intermediates = multiplication_order[0], []
    for value in multiplication_order[1:]:
        product = e4.mul(product, value)
        intermediates.append(element_blob(product).hex())
    direct_p = e4.eval(pentagon_word(f1))
    if product != direct_p or direct_p != e4.identity:
        fail(UNKNOWN_RAW, "pentagon factor replay")
    base_values = [factor_values_base[index] if sign > 0 else e4.inverse(factor_values_base[index]) for index, sign in zip([1, 3, 0, 2, 4], [1, 1, 1, -1, -1])]
    base_multiplication_order = list(reversed(base_values))
    base_product, base_intermediates = base_multiplication_order[0], []
    for value in base_multiplication_order[1:]:
        base_product = e4.mul(base_product, value)
        base_intermediates.append(element_blob(base_product).hex())
    if mutation == "corrected_base_sign":
        # Swap the actual base/corrected arguments before Fox evaluation; a
        # post-serialization sign flip would be only a receipt mutation.
        h1_direct, h1_bv, h1_cv = raw_difference(e3, h1_corr, h1_base)
        canonical_h1, _, _ = raw_difference(e3, h1_base, h1_corr)
        if h1_direct == canonical_h1:
            fail(UNKNOWN_RAW, "corrected/base sign mutation cancelled")
    else:
        h1_direct, h1_bv, h1_cv = raw_difference(e3, h1_base, h1_corr)
    h2_direct, h2_bv, h2_cv = raw_difference(e3, h2_base, h2_corr); p_direct, p_bv, p_cv = raw_difference(e4, pentagon_word(g), pentagon_word(f1))
    h1_base_target, _ = fox(e3, h1_base)
    h2_base_target, _ = fox(e3, h2_base)
    p_base_target, _ = fox(e4, pentagon_word(g))
    h2_u = z if mutation == "H2_u_z" else u
    fxy, fxz, fyz = f2_substitute(g, x, y), f2_substitute(g, x, z), f2_substitute(g, y, z); fxy1, fxz1, fyz1 = f2_substitute(f1, x, y), f2_substitute(f1, x, z), f2_substitute(f1, y, z); fux, fuy = f2_substitute(g, h2_u, x), f2_substitute(g, h2_u, y); fux1, fuy1 = f2_substitute(f1, h2_u, x), f2_substitute(f1, h2_u, y)
    h1_prefix, h1_prefix_bv, h1_prefix_cv = prefix_difference(e3, [fxy, inverse(fxz), fyz], [fxy1, inverse(fxz1), fyz1], embed_pb3, mutation == "inverse_fox_prefix"); h2_prefix, h2_prefix_bv, h2_prefix_cv = prefix_difference(e3, [inverse(fux), inverse(fxy), fuy], [inverse(fux1), inverse(fxy1), fuy1], embed_pb3)
    p_prefix, p_prefix_bv, p_prefix_cv = prefix_difference(e4, [factor_words_base[1], factor_words_base[3], factor_words_base[0], inverse(factor_words_base[2]), inverse(factor_words_base[4])], [factor_words_corr[1], factor_words_corr[3], factor_words_corr[0], inverse(factor_words_corr[2]), inverse(factor_words_corr[4])])
    h1_base_prefix, h1_base_prefix_value = product_gradient(
        e3, [fxy, inverse(fxz), fyz], embed_pb3)
    h2_base_prefix, h2_base_prefix_value = product_gradient(
        e3, [inverse(fux), inverse(fxy), fuy], embed_pb3)
    p_base_prefix, p_base_prefix_value = product_gradient(
        e4, [factor_words_base[1], factor_words_base[3], factor_words_base[0],
             inverse(factor_words_base[2]), inverse(factor_words_base[4])])
    if mutation == "inverse_fox_prefix":
        canonical_prefix, _, _ = prefix_difference(e3, [fxy, inverse(fxz), fyz], [fxy1, inverse(fxz1), fyz1], embed_pb3)
        if h1_prefix == canonical_prefix:
            fail(UNKNOWN_FOX, "inverse prefix mutation cancelled")
    if mutation == "H2_u_z":
        canonical_fux, canonical_fuy = f2_substitute(g, u, x), f2_substitute(g, u, y)
        canonical_fux1, canonical_fuy1 = f2_substitute(f1, u, x), f2_substitute(f1, u, y)
        canonical_h2, _, _ = prefix_difference(e3, [inverse(canonical_fux), inverse(fxy), canonical_fuy], [inverse(canonical_fux1), inverse(fxy1), canonical_fuy1], embed_pb3)
        if h2_prefix == canonical_h2:
            fail(UNKNOWN_FOX, "H2 u/z mutation cancelled")
    if (h1_prefix_bv != e3.eval(h1_base) or h1_prefix_cv != e3.eval(h1_corr) or
            h2_prefix_bv != e3.eval(h2_base) or h2_prefix_cv != e3.eval(h2_corr) or
            p_prefix_bv != e4.eval(pentagon_word(g)) or p_prefix_cv != e4.eval(pentagon_word(f1)) or
            h1_base_prefix_value != e3.eval(h1_base) or
            h2_base_prefix_value != e3.eval(h2_base) or
            p_base_prefix_value != e4.eval(pentagon_word(g))):
        fail(UNKNOWN_RAW, "prefix quotient value")
    for label, direct, prefix in (("H1", h1_direct, h1_prefix),
                                  ("H2", h2_direct, h2_prefix),
                                  ("P", p_direct, p_prefix)):
        if serial_row(direct) != serial_row(prefix):
            fail(UNKNOWN_RAW, "direct/prefix formula " + label)
    canonical_base_targets = {"H1": h1_base_target, "H2": h2_base_target,
                              "P": p_base_target}
    base_prefix_targets = {"H1": h1_base_prefix, "H2": h2_base_prefix,
                           "P": p_base_prefix}
    if mutation == "raw_base_target_stacked_confusion":
        confused = {"H1": h1_direct, "H2": h2_direct, "P": p_direct}
        if all(serial_row(confused[label]) == serial_row(canonical_base_targets[label])
               for label in canonical_base_targets):
            fail(UNKNOWN_RAW, "base-target/canary mutation cancelled")
        canonical_base_targets = confused
    for label in ("H1", "H2", "P"):
        if serial_row(canonical_base_targets[label]) != serial_row(base_prefix_targets[label]):
            fail(UNKNOWN_RAW, "base target direct/prefix " + label)
    pb3_rows, pb4_rows, pb3_digests, pb4_digests = build_d2(e3, e4); fox_replay = canaries(e3, e4, rows, mutation)
    block_tags = [1, 2, 3]
    if mutation == "dropped_block_tag":
        block_tags[0] = 0
    stacked = sorted([[tag, component, blob, coefficient] for tag, row in zip(block_tags, (h1_direct, h2_direct, p_direct)) for component, blob, coefficient in serial_row(row)], key=lambda row: (row[0], row[1], bytes.fromhex(row[2])))
    return {"q3": q3, "e3": e3, "e4": e4, "contexts": contexts, "aliases": aliases, "context_public": context_public, "retraction": retraction, "records": records, "joint": joint, "roster": rows, "g760": g, "correction": correction, "correction_provenance": roster_provenance(joint, correction_row), "f1": f1, "source_pairs": source_pairs, "source_blobs": source_blobs, "factor_values": factor_values_corr, "factor_values_base": factor_values_base, "factor_words": factor_words_corr, "factor_words_base": factor_words_base, "literal_words": {"H1_base": list(h1_base), "H2_base": list(h2_base), "H1_corrected": list(h1_corr), "H2_corrected": list(h2_corr), "P_base": list(pentagon_word(g)), "P_corrected": list(pentagon_word(f1)), "factor_words_base": [list(word) for word in factor_words_base], "factor_words_corrected": [list(word) for word in factor_words_corr]}, "ordered_indices": indices, "ordered_signs": signs, "ordered_intermediates": intermediates, "base_intermediates": base_intermediates, "ordered_blob": element_blob(product).hex(), "base_ordered_blob": element_blob(base_product).hex(), "direct_p_blob": element_blob(direct_p).hex(), "base_direct_p_blob": element_blob(e4.eval(pentagon_word(g))).hex(), "raw_base_targets": {label: {"row": serial_row(canonical_base_targets[label]), "sha256": digest_obj(serial_row(canonical_base_targets[label]))} for label in ("H1", "H2", "P")}, "raw": {"H1": h1_direct, "H2": h2_direct, "P": p_direct}, "prefix": {"H1": h1_prefix, "H2": h2_prefix, "P": p_prefix}, "raw_values": {"H1": (h1_bv, h1_cv), "H2": (h2_bv, h2_cv), "P": (p_bv, p_cv)}, "pb3_rows": pb3_rows, "pb4_rows": pb4_rows, "pb3_digests": pb3_digests, "pb4_digests": pb4_digests, "fox": fox_replay, "stacked": stacked}


def compare_ready(cert, obj):
    if cert.get("status") != "READY" or cert.get("terminal") != READY: fail(UNKNOWN_RAW, "READY envelope")
    if (cert.get("g760", {}).get("length") != 760 or
            cert.get("g760", {}).get("word") != list(obj["g760"]) or
            cert.get("g760", {}).get("sha256") != digest_obj(list(obj["g760"]))):
        fail(UNKNOWN_RAW, "g760 serialization")
    ordered = sorted(obj["roster"], key=lambda row: (row["layer"], row["ordinal"], row["word"])); correction = cert.get("correction", {})
    correction_row = next((row for row in ordered if row.get("word")), None)
    if correction_row is None:
        fail(UNKNOWN_RAW, "correction roster witness empty")
    if (correction.get("layer"), correction.get("ordinal"), tuple(correction.get("word", []))) != (correction_row["layer"], correction_row["ordinal"], obj["correction"]): fail(UNKNOWN_RAW, "correction roster witness")
    if correction.get("length") != len(obj["correction"]) or correction.get("sha256") != digest_obj(list(obj["correction"])) or correction.get("final") is not False: fail(UNKNOWN_RAW, "correction digest/role")
    if correction.get("provenance") != obj["correction_provenance"]:
        fail(UNKNOWN_RAW, "correction provenance")
    if not isinstance(cert.get("roster"), list) or cert.get("roster") != obj["roster"]:
        fail(UNKNOWN_RAW, "complete roster words")
    relation = cert.get("relation_roster", {});
    if (relation.get("count") != CAP or
            relation.get("layers") != {"gamma_edge": 6318, "xy_action": 104, "q0_relator": 19} or
            relation.get("roster_sha256") != roster_digest(obj["roster"]) or
            relation.get("lossless_words") is not True):
        fail(UNKNOWN_RAW, "roster contract")
    if cert.get("roster_contract", {}).get("nonempty_scope") != "deterministic correction witness and Fox canary samples only":
        fail(UNKNOWN_RAW, "roster nonempty scope")
    registered = cert.get("registered_canary", {})
    if (registered.get("status") != "PASS" or
            registered.get("direct_joint_identity") is not True or
            registered.get("layer") != correction_row["layer"] or
            registered.get("ordinal") != correction_row["ordinal"] or
            registered.get("word") != list(obj["correction"]) or
            registered.get("provenance") != obj["correction_provenance"]):
        fail(UNKNOWN_RAW, "registered canary")
    corrected = cert.get("corrected_word", {})
    if (corrected.get("word") != list(obj["f1"]) or
            corrected.get("length") != len(obj["f1"]) or
            corrected.get("sha256") != digest_obj(list(obj["f1"])) or
            corrected.get("formula") != "reduce(g760+c)"):
        fail(UNKNOWN_RAW, "corrected word")
    contexts = cert.get("contexts", {});
    if (contexts.get("aliases") != len(obj["aliases"]) or
            contexts.get("alias_map") != obj["aliases"] or
            contexts.get("named_uses") != obj["context_public"]["named_uses"] or
            contexts.get("registry_rows") != obj["context_public"]["contexts"] or
            contexts.get("registry_rows_sha256") != obj["context_public"]["context_rows_sha256"] or
            contexts.get("source_pairs") != obj["source_blobs"] or
            contexts.get("bridge_ids") != [21,22,23,24,25] or
            contexts.get("d_E_i_E_marks") is not True):
        fail(UNKNOWN_CONTEXT, "context envelope")
    stored_map, fresh_map = contexts.get("map_replay", {}), obj["retraction"]
    if stored_map != fresh_map:
        fail(UNKNOWN_CONTEXT, "map replay")
    raw_records = cert.get("raw_changes", {})
    for block in ("H1", "H2", "P"):
        if block not in raw_records: fail(UNKNOWN_RAW, "raw block " + block)
        direct, prefix = serial_row(obj["raw"][block]), serial_row(obj["prefix"][block])
        if raw_records[block].get("direct", {}).get("row") != direct or raw_records[block].get("prefix", {}).get("row") != prefix: fail(UNKNOWN_RAW, "raw rows " + block)
        if raw_records[block].get("direct", {}).get("sha256") != digest_obj(direct) or raw_records[block].get("prefix", {}).get("sha256") != digest_obj(prefix): fail(UNKNOWN_RAW, "raw digest " + block)
        if cert.get("raw_base_targets", {}).get(block) != obj["raw_base_targets"][block]:
            fail(UNKNOWN_RAW, "raw base target " + block)
    for block, (base, corrected) in obj["raw_values"].items():
        stored = cert.get("raw_values", {}).get(block, {})
        if stored.get("base") != element_blob(base).hex() or stored.get("corrected") != element_blob(corrected).hex(): fail(UNKNOWN_RAW, "raw value " + block)
    pent = cert.get("pentagon", {})
    if pent.get("factor_blobs") != [element_blob(value).hex() for value in obj["factor_values"]] or pent.get("base_factor_blobs") != [element_blob(value).hex() for value in obj["factor_values_base"]]: fail(UNKNOWN_RAW, "pentagon factors")
    for key, expected in (("ordered_intermediate_blobs", obj["ordered_intermediates"]), ("base_ordered_intermediate_blobs", obj["base_intermediates"]), ("ordered_value_blob", obj["ordered_blob"]), ("base_ordered_value_blob", obj["base_ordered_blob"]), ("direct_word_value_blob", obj["direct_p_blob"]), ("base_direct_word_value_blob", obj["base_direct_p_blob"])):
        if pent.get(key) != expected: fail(UNKNOWN_RAW, "pentagon " + key)
    if pent.get("ordered_factor_indices") != [1,3,0,2,4] or pent.get("ordered_factor_signs") != [1,1,1,-1,-1] or pent.get("direct_word_replay") is not True: fail(UNKNOWN_RAW, "pentagon order")
    for label, expected_rows, stored in (("pb3", obj["pb3_rows"], cert.get("pb3", {})), ("pb4", obj["pb4_rows"], cert.get("pb4", {}))):
        exact_by = "v121" if label == "pb3" else "v108"
        relator_values = [element_blob((obj["e3"] if label == "pb3" else obj["e4"]).eval(rel)).hex()
                          for rel in pure_relations(3 if label == "pb3" else 4)]
        if (stored.get("count") != len(expected_rows) or
                stored.get("rows") != expected_rows or
                stored.get("row_digests") != obj[label + "_digests"] or
                stored.get("relator_value_blobs") != relator_values or
                stored.get("d1_zero") is not True or
                stored.get("all_value_identity") is not True or
                stored.get("exact_by") != exact_by):
            fail(UNKNOWN_PB3 if label == "pb3" else UNKNOWN_FOX, label + " D2")
    literals = cert.get("literal_words", {})
    expected_literals = {
        "H1_base": list(obj["literal_words"]["H1_base"]),
        "H2_base": list(obj["literal_words"]["H2_base"]),
        "H1_corrected": list(obj["literal_words"]["H1_corrected"]),
        "H2_corrected": list(obj["literal_words"]["H2_corrected"]),
        "P_base": list(obj["literal_words"]["P_base"]),
        "P_corrected": list(obj["literal_words"]["P_corrected"]),
        "factor_words_base": obj["literal_words"]["factor_words_base"],
        "factor_words_corrected": obj["literal_words"]["factor_words_corrected"],
    }
    if literals != expected_literals: fail(UNKNOWN_RAW, "literal words")
    stack = cert.get("stacked_target", {})
    if (stack.get("row") != obj["stacked"] or stack.get("block_tags") != [1,2,3] or
            stack.get("key") != "(block_tag,component,exact_element_blob)" or
            stack.get("cross_block_cancellation") is not False or
            stack.get("row_sha256") != digest_obj(obj["stacked"])):
        fail(UNKNOWN_RAW, "stacked target")
    fx = cert.get("fox_replay", {})
    if fx.get("status") != "PASS" or fx.get("pairs", 0) < 110 or fx.get("slot_counts") != {str(i): 10 for i in range(1,12)} or any(fx.get("layer_counts", {}).get(layer, 0) == 0 for layer in ("gamma_edge", "xy_action", "q0_relator")): fail(UNKNOWN_FOX, "Fox quota")
    if fx.get("transcript") != obj["fox"]["transcript"] or fx.get("same_context") != obj["fox"]["same_context"] or fx.get("actual_product_additivity") != obj["fox"]["actual_product_additivity"] or fx.get("row_digest_sha256") != obj["fox"]["row_digest_sha256"]: fail(UNKNOWN_FOX, "Fox transcript")
    if cert.get("mutation_contract") != MUTATION_NAMES:
        fail(UNKNOWN_FOX, "mutation contract")
    muts = cert.get("mutation_results", {});
    if (muts.get("status") != "PASS" or
            muts.get("attempted") != len(MUTATION_NAMES) or
            muts.get("rejected") != len(MUTATION_NAMES) or
            len(muts.get("rows", [])) != len(MUTATION_NAMES) or
            [row.get("id") for row in muts.get("rows", [])] != MUTATION_NAMES or
            not all(row.get("caught") is True for row in muts.get("rows", []))):
        fail(UNKNOWN_FOX, "mutation envelope")
    if any(value is not False for value in cert.get("boundaries", {}).values()): fail(UNKNOWN_RAW, "claim boundary")


def mutation_suite(cert, canonical):
    names = list(MUTATION_NAMES)
    result = []
    for name in names:
        caught = False
        try:
            if name == "terminal_marker":
                # This sole envelope control checks terminal fail-closure;
                # every data mutation below enters reconstruct().
                candidate = copy.deepcopy(cert); candidate["terminal"] = "UNKNOWN_RESOURCE:runtime"; compare_ready(candidate, canonical)
            else:
                variant = {
                    "correction_left_right": "correction_left_right",
                    "corrected_base_sign": "corrected_base_sign",
                    "H2_u_z": "H2_u_z",
                    "inverse_fox_prefix": "inverse_fox_prefix",
                    "negative_pentagon_factor_4": "negative_pentagon_factor_4",
                    "negative_pentagon_factor_5": "negative_pentagon_factor_5",
                    "negative_pentagon_order": "negative_pentagon_order",
                    "coface_slot_1_3_swap": "coface_slot_1_3_swap",
                    "E3_E4_rank_swap": "E3_E4_rank_swap",
                    "E3_E4_blob_swap": "E3_E4_blob_swap",
                    "context_name_only_dedup": "context_name_only_dedup",
                    "dropped_block_tag": "dropped_block_tag",
                    "fourth_third_deletion_swap": "fourth_third_deletion_swap",
                    "fine_insertion_index_4_3_swap": "fine_insertion_index_4_3_swap",
                    "derived_u_order": "derived_u_order",
                    "derived_z_order": "derived_z_order",
                    "one_actual_roster_letter": "actual_roster_letter",
                    "actual_product_additivity_term": "actual_product_additivity_term",
                    "raw_base_target_stacked_confusion": "raw_base_target_stacked_confusion",
                }.get(name)
                if variant is None:
                    fail(UNKNOWN_FOX, "unmapped semantic mutation " + name)
                compare_ready(cert, reconstruct(cert, mutation=variant))
        except (Stop, KeyError, TypeError, ValueError, IndexError):
            caught = True
        if not caught: fail(UNKNOWN_FOX, "mutation accepted " + name)
        result.append({"id": name, "caught": True})
    return result


def validate_static(cert):
    if cert.get("schema") != "d972-r07-all-seven-raw-bridge-preflight/v1": fail(UNKNOWN_RAW, "schema")
    terminal = cert.get("terminal")
    if terminal not in ALLOWED: fail(UNKNOWN_RAW, "terminal")
    expected_pins = {name: {"path": rel, "bytes": expected_bytes,
                            "sha256": expected_sha}
                     for name, (rel, expected_bytes, expected_sha) in PINS.items()}
    if cert.get("pins") != expected_pins:
        fail("UNKNOWN_RESOURCE", "pins")
    if (cert.get("roster_contract", {}).get("total") != CAP or
            cert.get("roster_contract", {}).get("layers") != {"gamma_edge":6318,"q0_relator":19,"xy_action":104} or
            cert.get("roster_contract", {}).get("nonempty_scope") != "deterministic correction witness and Fox canary samples only"):
        fail(UNKNOWN_RAW, "roster contract")
    if cert.get("all_seven_contract", {}).get("occurrences", {}).get("total") != 11: fail(UNKNOWN_RAW, "occurrence contract")
    if cert.get("fox_contract", {}).get("actual_pairs_minimum") != 110: fail(UNKNOWN_FOX, "Fox contract")
    mutation_contract = cert.get("mutation_contract")
    if (mutation_contract != MUTATION_NAMES and not
            (terminal == "UNKNOWN_RESOURCE:LOCAL_EXECUTION_GUARD" and
             mutation_contract == LEGACY_FIXTURE_MUTATION_NAMES)):
        fail(UNKNOWN_FOX, "mutation contract")
    if any(value is not False for value in cert.get("boundaries", {}).values()): fail(UNKNOWN_RAW, "boundary")
    if terminal == "UNKNOWN_RESOURCE:LOCAL_EXECUTION_GUARD" and cert.get("status") != "UNKNOWN_RESOURCE": fail("UNKNOWN_RESOURCE", "fixture status")
    return {"terminal": terminal, "pins": len(PINS), "independent_reconstruction": "NOT_EXECUTED_BY_LOCAL_GUARD"}


def fixture_replay():
    # A genuinely tiny local quotient exercises the same collector, quotient,
    # Fox, translation, D1, and sparse serialization paths as production.
    word = reduce_word((1, 2, -2))
    if word != (1,) or inverse(inverse(word)) != word or paper_product((1,), (2,)) != (2, 1):
        fail(UNKNOWN_RAW, "fixture algebra")
    spec = {"generator_count": 1, "relative_orders": [3],
            "power_relations": [[0]], "inverses": [[2]],
            "conjugate_relations": [], "inverse_conjugate_relations": []}
    pc = PcCollector(spec)
    toy = Quotient(2, 1, pc, [(perm_one(1), pc.unit(1))])
    relation = (1, 1, 1)
    gradient, value = fox(toy, relation)
    if value != toy.identity or d1(gradient, toy) != {}:
        fail(UNKNOWN_FOX, "fixture Fox/D1")
    translated = translate(gradient, toy.eval((1,)), toy)
    if d1(translated, toy) != {} or not serial_row(translated):
        fail(UNKNOWN_FOX, "fixture translation/serialization")
    # The non-identity two-letter word is a real semantic rejection, not a
    # receipt mutation; it exercises the fixture's quotient validator path.
    if toy.eval((1, 1)) == toy.identity:
        fail(UNKNOWN_FOX, "fixture mutation accepted")
    return {"terminal": "FIXTURE_PASS", "fixture": True,
            "mutation_path": "semantic_local_toy", "fox_d1": True,
            "serialized_components": len(serial_row(translated))}


def validate_ready(cert):
    validate_static(cert); canonical = reconstruct(cert); compare_ready(cert, canonical); mutations = mutation_suite(cert, canonical)
    if cert.get("mutation_results", {}).get("rows") != mutations:
        fail(UNKNOWN_FOX, "mutation replay receipt")
    return {"terminal": READY, "pins": len(PINS), "fresh_roster": len(canonical["roster"]), "fresh_contexts": len(canonical["contexts"]), "fresh_aliases": len(canonical["aliases"]), "fresh_pb3_columns": len(canonical["pb3_rows"]), "fresh_pb4_columns": len(canonical["pb4_rows"]), "fresh_fox_pairs": canonical["fox"]["pairs"], "semantic_mutations_rejected": len(mutations), "semantic_mutation_gate": "FULL_RECONSTRUCTION_AND_VALIDATOR"}


def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--check", action="store_true"); parser.add_argument("--receipt", type=Path, default=CERT); parser.add_argument("--output", type=Path); parser.add_argument("--fixture", action="store_true"); args = parser.parse_args()
    marker = "D175_CHECK_PASS" if args.check else "D175_STATIC_CHECK_PASS"
    try:
        pins = pin_inputs(); cert = json.loads(args.receipt.read_text(encoding="utf-8"))
        if args.fixture:
            validate_static(cert)
            result = fixture_replay()
        else:
            result = validate_ready(cert) if args.check and cert.get("terminal") == READY else validate_static(cert)
        result["pins_authenticated"] = len(pins)
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True); args.output.write_text(marker + "\nterminal=" + result["terminal"] + "\n" + json.dumps(result, sort_keys=True) + "\n", encoding="utf-8")
        print(marker); print("terminal=" + result["terminal"]); print(json.dumps(result, sort_keys=True)); return 0
    except Stop as exc:
        print("D175_CHECK_FAIL"); print("terminal=" + exc.terminal); print("detail=" + exc.detail); return 1
    except (OSError, UnicodeError, json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        print("D175_CHECK_FAIL"); print("terminal=UNKNOWN_RESOURCE:checker_exception"); print("detail=" + str(exc)); return 1


if __name__ == "__main__":
    raise SystemExit(main())
