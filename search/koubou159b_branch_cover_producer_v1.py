"""Producer-side Phase-2 BRANCH-COVER audit (task 159b).

This file is deliberately self-contained.  It imports no search producer and
no crosscheck module.  It freezes the campaign inputs, reconstructs the
canonical 6 x 27 branch universe and its 144/18 and 8/10 partitions, and then
audits the q3 roof-power convention in the receipt's primitive permutation/pc
models.

The important terminal is partial: the receipt-level roster arithmetic is
closed, but the literal paper composition and the legacy q3 composition do
not define the same 27-element fibres in four of the five E4 contexts.  Thus
this producer must never be used to promote the 144 or 8 branches.  A new
paper-formula bulk run and a producer-nonsharing checker are still required.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
from pathlib import Path
from typing import Any, Callable, Iterable, Sequence


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "koubou159b-branch-cover-producer/v1"

# These are evidence pins, not an assertion that every file is a runtime input
# of this producer.  The ``lane`` field below separates the actual dependency
# chains and prevents the old M2 canary receipt from being paired with the new
# v3 source.
PINNED_FILES: tuple[tuple[str, int, str, str], ...] = (
    ("search/koubou158_L3_bulk162_v1_2.py", 12635,
     "21d83c9e48cbd3d81c585debad59cff2f974c54bed5b8a14cf064f87b3feab63", "bulk-source"),
    ("search/koubou158_L3_core_v1_2.py", 31192,
     "4366ebd1759fbd11a795b251101776836ef4ec2a28b7b947b93727208e199c63", "bulk-runtime"),
    ("search/certs/koubou158_L3_bulk162_v1_2_20260822.json", 45007,
     "6e51df539aa4cf793c7302514cf1f068e098c06ca751571890da09ba7fd13172", "bulk-receipt"),
    ("search/koubou158_prodrung_v1.py", 26567,
     "a0e1e47a76b9d6379e9f2b16334140ec0eaf1e0b4d70f4793ae4f676949015a1", "prodrung-source"),
    ("search/koubou158_prodrung_j5_resume_v1.py", 14421,
     "af56df3f5301437b13cf2113f75d0a2b15d0ce4b97a300f8ad4d5527c2b872c2", "prodrung-runtime"),
    ("search/certs/koubou158_prodrung_v1_20260822.json", 15391,
     "3160eec7281ecaaa38e4f869530b5fb7639620e7363c9abde5acb0990638cafe", "prodrung-receipt"),
    ("search/koubou158_M2_msweep_v3.py", 17512,
     "a6ab013cb541578a55485591c5b113bfabc822a1290f4337b26e7afad14ec59b", "m2-current-source"),
    ("search/koubou158_L3_core_v1_1.py", 24529,
     "ec93ed38527922de328603e01abd662743cfc03904ee21a924395fd0879d3d82", "m2-current-runtime"),
    ("search/koubou158_L3_core_completebfs_v1.py", 7432,
     "3aa5ce3beb4b8781506858ba2947ac7a17c4e70ee152dec9fd917fa451e33c13", "m2-current-runtime"),
    ("search/koubou158_m2_closedform_v2.py", 3645,
     "6525535ae7c50af54e6891a5e0608ee08ea50f692916dfb40ce5d75bfd463f2f", "m2-current-runtime"),
    ("search/koubou158_m2_closedform_v1.py", 3956,
     "7c5630bc4a6103f5fb5e002783f097a567ae290f0e913dd611ffa20a2c09c0dc", "m2-predecessor-source"),
    ("search/certs/koubou158_M2_msweep_v3_20260822.json", 33824,
     "7ff02c0eb9a49ed0105ceabba2aba92c476e04efbb77af9004b805c95f58abdd", "m2-predecessor-canary"),
    ("ci/b345_157en_artifacts_32458556448/d972_b345_q3_chief_v1.json", 231570,
     "3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72", "q3-runtime"),
    ("search/d972_b345_q3_chief_v1.g", 76867,
     "b95fc29b326c3d6a378249cdeb03595eed8d0211a7fe0358fc02447d70d5f755", "q3-source"),
    ("search/d972_b345_q3_gha_driver_v1.g", 5488,
     "c397cd837ff6814f7b7a8ca0604c6aed54fa0bc85bb577516ea1c6e7df83a831", "q3-driver"),
    ("search/check_d972_b345_q3_chief_v1.py", 89082,
     "ddb52ddae18327209692f0f6eb8b4f65cbdd446155be660a621de24274cc3f73", "q3-checker"),
    ("search/certs/d972_phase2b_nonsplit_v1_20260813.json", 15792,
     "648335000ff70f37d357c9c27ec5054cd4366b281c616f0391c4c7580cd4bcb9", "q3-source-input"),
    ("search/certs/d972_b4_word_key_artifact_v1_20260816.json", 176474,
     "564a921be8114bdeb963f679c121e8d9aa90e148c65e95e393874fcba843e9f9", "q3-runtime"),
    ("search/gaplib_common.g", 8793,
     "f80eeeae71c4e39f8b3d62d997d18635f5ea8fb339a6d0578e834300ea4d4911", "q3-source-input"),
    ("search/check_d972_b4_literal_row18_stage_v2.py", 71884,
     "bf85cfd142f6c640e96af77aa5f580caa206439329d17ed18ac342ac6acdcd19", "q3-row18-lineage"),
    ("search/d972_d972core_c2six_intersection_v2.g", 25799,
     "577de029a49e2db3a33cf3b4437c78548214f9635b1750185d48a5385c161f4c", "q3-row18-lineage"),
    ("search/d972_b4_literal_row18_stage_v2.g", 75920,
     "8f8b429b5725b244a214cc6a4cf59daa186e4ee2d4d6eee6df18e580d88ef2a1", "q3-row18-lineage"),
    ("ci/b345_157ee_artifacts_32359956713/d972_b345_joint_kernel_qstar_closure_v1.json", 2166036,
     "1c3ad7a7124cee152eb40968cf212c14641a9f8720063c85f70533864898d0df", "context-registry-runtime"),
    ("search/d972_b345_joint_kernel_qstar_closure_v1.py", 67945,
     "06ba6cf361957db3e339d48d14b3d4fbc689de9642e3f96273fbe8f3160e76dc", "context-registry-source"),
    ("search/check_d972_b345_joint_kernel_qstar_closure_v1.py", 47661,
     "9e721634d1f16be806e315eec263ec272bc023587f862703c094b7dd37c0111f", "context-registry-checker"),
    ("search/d972_b345_joint_kernel_qstar_closure_gha_driver_v1.g", 10906,
     "ad536c97644ba28e511ca7cb1f58192bddfecdfce6630fd76dde108589303ad4", "context-registry-driver"),
    ("crosscheck/check_koubou158_L3_bulk162_v1.py", 11487,
     "c97c0da5cac7b9e2300d7969c139f9ded1437d1f7492977690e57616741cd6bd", "bulk-old-nonseparated-checker"),
    ("crosscheck/verdicts/koubou158_L3_bulk162_crosscheck_v1_20260822.json", 32388,
     "eebc436b21090119be08b75126b0e3cf2dcd30ae0dc6395f3d0b0537e81880fb", "bulk-old-nonseparated-verdict"),
)

Q3_PATH = PINNED_FILES[12][0]
WORD_PATH = PINNED_FILES[17][0]
BULK_PATH = PINNED_FILES[2][0]
PRODRUNG_PATH = PINNED_FILES[5][0]
M2_CANARY_PATH = PINNED_FILES[11][0]
REGISTRY_PATH = PINNED_FILES[22][0]

EXPECTED_ROSTER = (
    "r0_c8", "r0_c13", "r0_c18", "r1_c2", "r1_c17", "r1_c23",
    "r2_c2", "r2_c15", "r2_c22", "r3_c2", "r3_c16", "r3_c21",
    "r4_c1", "r4_c16", "r4_c22", "r5_c3", "r5_c10", "r5_c26",
)
EXPECTED_DEAD8 = (
    "r0_c13", "r0_c18", "r1_c17", "r2_c15",
    "r3_c2", "r3_c21", "r4_c22", "r5_c10",
)
EXPECTED_LIVE10 = (
    "r0_c8", "r1_c2", "r1_c23", "r2_c2", "r2_c22",
    "r3_c16", "r4_c1", "r4_c16", "r5_c3", "r5_c26",
)
EXPECTED_ORBIT_ROWS_ONE_BASED = (1, 19, 37, 55, 73, 10, 28, 46, 64, 1)
OUTSIDE_EXPONENTS = (1, 2, 4, 5, 7, 8)


class Stop(RuntimeError):
    pass


def require(condition: Any, message: str) -> None:
    if not condition:
        raise Stop(message)


def canonical_bytes(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")


def digest_obj(obj: Any) -> str:
    return hashlib.sha256(canonical_bytes(obj)).hexdigest()


def digest_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def load_json(relative: str) -> Any:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def reduce_word(word: Iterable[int]) -> list[int]:
    out: list[int] = []
    for letter in word:
        require(isinstance(letter, int) and letter != 0, "invalid free letter")
        if out and out[-1] == -letter:
            out.pop()
        else:
            out.append(letter)
    return out


def inverse_word(word: Sequence[int]) -> list[int]:
    return reduce_word(-letter for letter in reversed(word))


def evaluate(word: Sequence[int], images: Sequence[Any], identity: Any,
             multiply: Callable[[Any, Any], Any], inverse: Callable[[Any], Any]) -> Any:
    out = identity
    for letter in word:
        require(1 <= abs(letter) <= len(images), "word image index")
        value = images[abs(letter) - 1]
        out = multiply(out, value if letter > 0 else inverse(value))
    return out


def substitute(word: Sequence[int], x_word: Sequence[int], y_word: Sequence[int]) -> list[int]:
    return evaluate(word, [list(x_word), list(y_word)], [],
                    lambda a, b: reduce_word(list(a) + list(b)), inverse_word)


def compose_paper_m0(left: Sequence[int], right: Sequence[int]) -> list[int]:
    # Formula (3.53): f1 E_(0,f1)(f2), E(y)=f1^-1 y f1.
    y_image = reduce_word(inverse_word(left) + [2] + list(left))
    return reduce_word(list(left) + substitute(right, [1], y_image))


def compose_legacy_m0(left: Sequence[int], right: Sequence[int]) -> list[int]:
    # Literal implementation in d972_b345_q3_chief_v1.g.
    y_image = reduce_word(list(left) + [2] + inverse_word(left))
    return reduce_word(substitute(right, [1], y_image) + list(left))


Perm = tuple[int, ...]


def perm_one(degree: int) -> Perm:
    return tuple(range(degree))


def perm_from_json(row: Sequence[int], degree: int) -> Perm:
    require(len(row) == degree, "permutation degree")
    out = tuple(int(x) - 1 for x in row)
    require(set(out) == set(range(degree)), "permutation bijection")
    return out


def perm_mul(a: Perm, b: Perm) -> Perm:
    # GAP right-action convention: i^(a*b)=(i^a)^b.
    require(len(a) == len(b), "permutation degree mismatch")
    return tuple(b[a[i]] for i in range(len(a)))


def perm_inv(a: Perm) -> Perm:
    out = [0] * len(a)
    for i, image in enumerate(a):
        out[image] = i
    return tuple(out)


def perm_order(a: Perm) -> int:
    seen = [False] * len(a)
    answer = 1
    for start in range(len(a)):
        if seen[start]:
            continue
        here, length = start, 0
        while not seen[here]:
            seen[here] = True
            here = a[here]
            length += 1
        answer = math.lcm(answer, length)
    return answer


class PcTable:
    """Small deterministic collector reconstructed only from receipt tables."""

    def __init__(self, receipt: dict[str, Any]) -> None:
        self.receipt = receipt
        self.n = int(receipt["generator_count"])
        self.orders = tuple(int(x) for x in receipt["relative_orders"])
        self.powers = tuple(tuple(int(x) for x in row) for row in receipt["power_relations"])
        self.inverses = tuple(tuple(int(x) for x in row) for row in receipt["inverses"])
        self.conjugates = {
            (int(row["i"]), int(row["j"])): tuple(int(x) for x in row["coords"])
            for row in receipt["conjugate_relations"]
        }
        require(len(self.orders) == self.n, "pc order width")
        require(len(self.powers) == self.n and len(self.inverses) == self.n, "pc table width")
        require(int(receipt["order_decimal"]) == math.prod(self.orders), "pc order product")
        require(all(len(row) == self.n for row in self.powers + self.inverses), "pc coordinate width")
        require(len(self.conjugates) == self.n * (self.n - 1) // 2, "pc conjugate table")
        self.cache: dict[tuple[int, ...], tuple[int, ...]] = {(): self.one()}

    def one(self) -> tuple[int, ...]:
        return (0,) * self.n

    def coords_word(self, coords: Sequence[int]) -> list[int]:
        out: list[int] = []
        for i, exponent in enumerate(coords, start=1):
            require(0 <= exponent < self.orders[i - 1], "pc exponent range")
            out.extend([i] * int(exponent))
        return out

    def collect(self, signed_word: Sequence[int]) -> tuple[int, ...]:
        key = tuple(int(x) for x in signed_word)
        if key in self.cache:
            return self.cache[key]
        tokens: list[int] = []
        for letter in key:
            require(1 <= abs(letter) <= self.n, "pc letter range")
            if letter > 0:
                tokens.append(letter)
            else:
                tokens.extend(self.coords_word(self.inverses[-letter - 1]))
        steps = 0
        cap = max(10000, 2000 * (1 + len(tokens)) * (1 + self.n))
        while True:
            changed = False
            for pos in range(len(tokens) - 1):
                a, b = tokens[pos], tokens[pos + 1]
                if a > b:
                    tokens[pos:pos + 2] = [b] + self.coords_word(self.conjugates[(a, b)])
                    changed = True
                    break
            if not changed:
                pos = 0
                while pos < len(tokens):
                    end = pos
                    while end < len(tokens) and tokens[end] == tokens[pos]:
                        end += 1
                    order = self.orders[tokens[pos] - 1]
                    if end - pos >= order:
                        tokens[pos:pos + order] = self.coords_word(self.powers[tokens[pos] - 1])
                        changed = True
                        break
                    pos = end
            if not changed:
                break
            steps += 1
            require(steps <= cap, "pc collection cap")
        row = [0] * self.n
        for letter in tokens:
            row[letter - 1] += 1
        answer = tuple(row)
        require(all(0 <= answer[i] < self.orders[i] for i in range(self.n)), "pc normal form")
        self.cache[key] = answer
        return answer

    def mul(self, a: Sequence[int], b: Sequence[int]) -> tuple[int, ...]:
        return self.collect(self.coords_word(a) + self.coords_word(b))

    def inverse(self, a: Sequence[int]) -> tuple[int, ...]:
        word: list[int] = []
        for i in range(self.n, 0, -1):
            for _ in range(int(a[i - 1])):
                word.extend(self.coords_word(self.inverses[i - 1]))
        return self.collect(word)

    def power(self, a: Sequence[int], exponent: int) -> tuple[int, ...]:
        require(exponent >= 0, "negative pc power")
        out, base, n = self.one(), tuple(a), exponent
        while n:
            if n & 1:
                out = self.mul(out, base)
            base = self.mul(base, base)
            n >>= 1
        return out

    def marked(self, word: Sequence[int]) -> tuple[int, ...]:
        marks = self.receipt["marked_generators"]
        images = [tuple(int(x) for x in row["coords"]) for row in marks]
        return evaluate(word, images, self.one(), self.mul, self.inverse)

    def order(self, value: Sequence[int]) -> int:
        for exponent in range(1, int(self.receipt["order_decimal"]) + 1):
            if self.power(value, exponent) == self.one():
                return exponent
        raise Stop("pc element order cap")


def model_images(model: dict[str, Any]) -> tuple[Perm, ...]:
    return tuple(perm_from_json(row, int(model["degree"])) for row in model["marked_permutations"])


def eval_perm(word: Sequence[int], model: dict[str, Any]) -> Perm:
    images = model_images(model)
    return evaluate(word, images, perm_one(int(model["degree"])), perm_mul, perm_inv)


def paper_product(values: Sequence[Any], identity: Any,
                  multiply: Callable[[Any, Any], Any]) -> Any:
    require(bool(values), "empty paper product")
    out = identity
    for value in reversed(values):
        out = multiply(out, value)
    return out


def numeric_branch_key(branch_id: str) -> tuple[int, int]:
    left, right = branch_id.split("_")
    return int(left[1:]), int(right[1:])


def pin_inventory() -> list[dict[str, Any]]:
    out = []
    for relative, expected_bytes, expected_sha, lane in PINNED_FILES:
        path = ROOT / relative
        require(path.is_file(), f"missing pinned file: {relative}")
        require(path.stat().st_size == expected_bytes, f"byte drift: {relative}")
        require(digest_file(path) == expected_sha, f"SHA drift: {relative}")
        out.append({"path": relative, "bytes": expected_bytes, "sha256": expected_sha, "lane": lane})
    return out


def branch_structure(bulk: dict[str, Any], prodrung: dict[str, Any]) -> dict[str, Any]:
    require(bulk["schema"] == "koubou158-L3-bulk162/v1.2", "bulk schema")
    rows = bulk["per_branch"]
    universe = {f"r{r}_c{c}" for r in range(6) for c in range(27)}
    row_ids = [row["branch_id"] for row in rows]
    require(len(rows) == len(set(row_ids)) == 162 and set(row_ids) == universe, "bulk cartesian universe")
    for row in rows:
        require(row["branch_id"] == f"r{row['roof_index']}_c{row['correction_index']}", "bulk branch fields")
        require(0 <= row["roof_index"] < 6 and 0 <= row["correction_index"] < 27, "zero-based branch")
    nonmember = {row["branch_id"] for row in rows if row["non_member_at_L3"]}
    member = universe - nonmember
    roster = tuple(sorted(member, key=numeric_branch_key))
    require(len(nonmember) == 144 and len(member) == 18, "bulk 144/18 counts")
    require(roster == EXPECTED_ROSTER, "canonical 18 roster")
    require(set(bulk["non_member_at_L3_branch_ids"]) == nonmember, "bulk nonmember summary")
    require(set(bulk["member_at_L3_branch_ids"]) == member, "bulk member summary")

    require(prodrung["schema"] == "koubou158-prodrung/v1", "prodrung schema")
    results = prodrung["branch_results"]
    require(set(results) == member, "prodrung covers exactly the 18")
    dead = {bid for bid, row in results.items() if row["non_member"] is True and row["j_star"] == 5}
    live = {bid for bid, row in results.items() if row["non_member"] is False and row["j_star"] is None}
    require(dead | live == member and not (dead & live), "prodrung 8/10 partition")
    require(tuple(sorted(dead, key=numeric_branch_key)) == EXPECTED_DEAD8, "prodrung dead 8")
    require(tuple(sorted(live, key=numeric_branch_key)) == EXPECTED_LIVE10, "prodrung live 10")
    expected_progress = ((2, 756, 555, 51, 606, 0, 18),
                         (3, 3456, 2672, 121, 2793, 0, 18),
                         (4, 11448, 9133, 191, 9324, 0, 18),
                         (5, 31320, 25352, 280, 25632, 8, 10))
    got_progress = tuple((row["j"], row["dim_Lambda_over_aj"], row["rank_D2bar_alone"],
                          row["rank_V"], row["rank_combined"],
                          row["n_branches_resolved_this_level"],
                          row["n_branches_still_undetermined_after"])
                         for row in prodrung["j_progression"])
    require(got_progress == expected_progress, "prodrung progression")
    return {
        "indexing": {
            "roof_index": "zero-based r=0..5; maps in order to q3 outside exponents 1,2,4,5,7,8",
            "correction_index": "zero-based c=0..26 into correction_fibre.records",
            "q3_row_index": "one-based GAP row number; not a branch correction index",
            "historical_selected_solution_correction_index": "one-based 1, hence branch c0",
        },
        "cartesian_universe": {"roof_count": 6, "correction_count": 27, "total": 162},
        "bulk_partition": {
            "nonmember_candidate_count": 144,
            "member_at_L3_count": 18,
            "disjoint": True,
            "union_is_cartesian_universe": True,
            "unique_member_roster": list(roster),
        },
        "prodrung_partition": {
            "j5_candidate_dead_count": 8,
            "j5_candidate_dead": list(EXPECTED_DEAD8),
            "undetermined_count": 10,
            "undetermined": list(EXPECTED_LIVE10),
            "disjoint": True,
            "union_is_unique_member_roster": True,
            "promotion_forbidden": "producer-only candidate records; no separated checker and formula gate blocked",
        },
        "j_progression": [
            {"j": j, "dimension": dim, "rank_D2": d2, "rank_V": v, "rank_combined": comb,
             "resolved": resolved, "undetermined": undetermined}
            for j, dim, d2, v, comb, resolved, undetermined in expected_progress
        ],
    }


def formula_audit(q3: dict[str, Any], words: dict[str, Any]) -> dict[str, Any]:
    require(q3["schema"] == "d972-b345-q-chief/v1", "q3 schema")
    require(words["schema"] == "d972-b4-word-key-artifact/v1" and words["count"] == 972, "word artifact")
    p_model, g_model = q3["coarse_models"]["P"], q3["coarse_models"]["G9"]
    cache: dict[tuple[Any, ...], tuple[int, list[int]]] = {}
    for row_index, row in enumerate(words["rows"], start=1):
        key = (row[0], eval_perm(row[2], p_model), eval_perm(row[2], g_model))
        require(key not in cache, "972 coarse key collision")
        cache[key] = (row_index, list(row[2]))
    require(len(cache) == 972, "coarse cache size")
    identity_key = (0, perm_one(int(p_model["degree"])), perm_one(int(g_model["degree"])))
    require(cache[identity_key][0] == 1, "identity row")
    base = list(words["rows"][18][2])
    base_key = (0, eval_perm(base, p_model), eval_perm(base, g_model))
    require(cache[base_key][0] == 19, "base row19")

    paths: dict[str, dict[str, list[Any]]] = {}
    for name, composer in (("paper", compose_paper_m0), ("legacy", compose_legacy_m0)):
        rows: list[int] = []
        raw_words: list[list[int]] = []
        canonical_words: list[list[int]] = []
        for exponent in range(10):
            if exponent == 0:
                row_index, canonical = cache[identity_key]
                raw = list(canonical)
            elif exponent == 1:
                row_index, canonical = 19, list(base)
                raw = list(base)
            else:
                raw = composer(base, canonical_words[-1])
                key = (0, eval_perm(raw, p_model), eval_perm(raw, g_model))
                require(key in cache, f"{name} coarse power missing")
                row_index, canonical = cache[key]
                canonical = list(canonical)
            rows.append(row_index)
            raw_words.append(raw)
            canonical_words.append(canonical)
        require(tuple(rows) == EXPECTED_ORBIT_ROWS_ONE_BASED, f"{name} orbit")
        paths[name] = {"rows": rows, "raw": raw_words, "canonical": canonical_words}

    # Pi3 fine model: this is exactly the layer at which the q3 receipt's own
    # fine_fibre_completeness check can make the formula defect look harmless.
    pc3 = PcTable(q3["groups"]["PB3"])
    marks3 = q3["groups"]["PB3"]["marked_generators"]
    f2_images3 = (tuple(marks3[0]["coords"]), tuple(marks3[2]["coords"]))
    eval3 = lambda word: evaluate(word, f2_images3, pc3.one(), pc3.mul, pc3.inverse)
    correction_words = [list(row["word"]) for row in q3["correction_fibre"]["records"]]
    corrections3 = [eval3(word) for word in correction_words]
    require(len(corrections3) == len(set(corrections3)) == 27, "Pi3 correction fibre")
    correction_set3 = set(corrections3)
    require(all(pc3.inverse(c) in correction_set3 for c in corrections3), "Pi3 correction inverses")
    require(all(pc3.mul(a, b) in correction_set3 for a in corrections3 for b in corrections3),
            "Pi3 correction closure")

    pi3_rows = []
    for exponent in range(10):
        values: dict[str, Any] = {}
        fibres: dict[str, set[Any]] = {}
        for name in ("paper", "legacy"):
            raw_value = eval3(paths[name]["raw"][exponent])
            canonical_value = eval3(paths[name]["canonical"][exponent])
            shift = pc3.mul(pc3.inverse(canonical_value), raw_value)
            require(shift in correction_set3, f"{name} Pi3 rebase shift")
            raw_fibre = {pc3.mul(raw_value, c) for c in corrections3}
            canonical_fibre = {pc3.mul(canonical_value, c) for c in corrections3}
            require(raw_fibre == canonical_fibre and len(raw_fibre) == 27, f"{name} Pi3 fibre")
            values[name] = {
                "raw_coords": list(raw_value), "canonical_coords": list(canonical_value),
                "rebase_shift_coords": list(shift),
                "rebase_shift_correction_index_zero_based": corrections3.index(shift),
                "raw_word_length": len(paths[name]["raw"][exponent]),
            }
            fibres[name] = raw_fibre
        require(fibres["paper"] == fibres["legacy"], "paper/legacy Pi3 fibre")
        pi3_rows.append({"exponent": exponent, **values, "paper_legacy_fibres_equal": True})

    center3 = pc3.marked([1, 2, 3])  # c=Delta_3^2=a12*a13*a23.
    require(pc3.order(center3) == 3, "Pi3 center order")
    require(center3 not in correction_set3, "center canary must not lie in correction subgroup")
    require(all(pc3.mul(center3, tuple(row["coords"])) == pc3.mul(tuple(row["coords"]), center3)
                for row in marks3), "Pi3 center commutation")

    # Full E4 = Q4 permutation x Pi4[3] pc model, in all five coface contexts.
    pc4 = PcTable(q3["groups"]["PB4"])
    q4 = q3["coarse_models"]["Q4"]
    q4_images = model_images(q4)
    pc4_images = tuple(tuple(row["coords"]) for row in q3["groups"]["PB4"]["marked_generators"])
    e4_marks = tuple(zip(q4_images, pc4_images))
    e4_one = (perm_one(int(q4["degree"])), pc4.one())

    def e4_mul(a: Any, b: Any) -> Any:
        return perm_mul(a[0], b[0]), pc4.mul(a[1], b[1])

    def e4_inv(a: Any) -> Any:
        return perm_inv(a[0]), pc4.inverse(a[1])

    pp = lambda values: paper_product(values, e4_one, e4_mul)
    g = e4_marks
    contexts = (
        (g[0], g[3]),
        (g[3], g[5]),
        (pp((g[1], g[3])), g[5]),
        (pp((g[0], g[1])), pp((g[4], g[5]))),
        (g[0], pp((g[3], g[4]))),
    )

    context_rows = []
    mismatch_contexts_by_outside: dict[str, list[int]] = {str(n): [] for n in OUTSIDE_EXPONENTS}
    canonical_mismatch_contexts_by_outside: dict[str, list[int]] = {str(n): [] for n in OUTSIDE_EXPONENTS}
    for context_index, pair in enumerate(contexts):
        eval4 = lambda word: evaluate(word, pair, e4_one, e4_mul, e4_inv)
        corrections4 = [eval4(word) for word in correction_words]
        require(len(set(corrections4)) == 27, "E4 context correction distinctness")
        paper_canonical_intersections = []
        legacy_canonical_intersections = []
        paper_legacy_intersections = []
        for exponent in range(10):
            named_fibres: dict[str, set[Any]] = {}
            for name in ("paper", "legacy"):
                raw_value = eval4(paths[name]["raw"][exponent])
                canonical_value = eval4(paths[name]["canonical"][exponent])
                named_fibres[name] = {e4_mul(raw_value, c) for c in corrections4}
                canonical_fibre = {e4_mul(canonical_value, c) for c in corrections4}
                intersection = len(named_fibres[name] & canonical_fibre)
                (paper_canonical_intersections if name == "paper" else
                 legacy_canonical_intersections).append(intersection)
                if name == "paper" and exponent in OUTSIDE_EXPONENTS and intersection != 27:
                    canonical_mismatch_contexts_by_outside[str(exponent)].append(context_index)
            intersection = len(named_fibres["paper"] & named_fibres["legacy"])
            paper_legacy_intersections.append(intersection)
            if exponent in OUTSIDE_EXPONENTS and intersection != 27:
                mismatch_contexts_by_outside[str(exponent)].append(context_index)
        context_rows.append({
            "context_index_zero_based": context_index,
            "correction_fibre_size": 27,
            "paper_raw_vs_canonical_intersection_by_exponent_0_to_9": paper_canonical_intersections,
            "legacy_raw_vs_canonical_intersection_by_exponent_0_to_9": legacy_canonical_intersections,
            "paper_raw_vs_legacy_raw_intersection_by_exponent_0_to_9": paper_legacy_intersections,
        })

    require(mismatch_contexts_by_outside == {
        "1": [], "2": [], "4": [0, 1, 2, 3], "5": [0, 1, 2, 3],
        "7": [0, 1, 2, 3], "8": []}, "paper/legacy E4 mismatch fingerprint")
    require(canonical_mismatch_contexts_by_outside == {
        "1": [], "2": [0, 1, 2, 3, 4], "4": [0, 1, 2, 3, 4],
        "5": [0, 1, 2, 3, 4], "7": [0, 1, 2, 3, 4],
        "8": [0, 1, 2, 3, 4]}, "paper/canonical E4 mismatch fingerprint")

    # Embedded PB3 center in PB4: [a12,a13,a23] = PB4 marked [1,2,4].
    center4 = evaluate([1, 2, 4], e4_marks, e4_one, e4_mul, e4_inv)
    center4_pc_order = pc4.order(center4[1])
    center4_perm_order = perm_order(center4[0])
    center4_full_order = math.lcm(center4_pc_order, center4_perm_order)
    require((center4_pc_order, center4_perm_order, center4_full_order) == (3, 18, 18),
            "embedded center kappa/full order canary")

    outside_roofs = [
        {"roof_index_zero_based": r, "exponent": exponent,
         "q3_row_index_one_based": EXPECTED_ORBIT_ROWS_ONE_BASED[exponent]}
        for r, exponent in enumerate(OUTSIDE_EXPONENTS)
    ]
    return {
        "paper_formula": "f1 E_(0,f1)(f2) = f1 * f2(x, f1^-1*y*f1), week1 formula (3.53)",
        "legacy_formula": "f2(x, f1*y*f1^-1) * f1, literal D972Q3GTComposeM0",
        "literal_formulae_equal": False,
        "coarse_972_cache_unique": True,
        "normalized_orbit_rows_one_based": list(EXPECTED_ORBIT_ROWS_ONE_BASED),
        "outside_roofs": outside_roofs,
        "pi3_fine_audit": {
            "correction_subgroup_order": 27,
            "paper_and_legacy_fibres_equal_at_all_exponents": True,
            "rows": pi3_rows,
            "center_c_coords": list(center3),
            "center_c_order_kappa": 3,
            "center_c_not_in_correction_subgroup": True,
            "warning": "Pi3-only fibre equality is insufficient for the E4 bulk predicate",
        },
        "e4_five_context_audit": {
            "embedded_center_pc_order_kappa": center4_pc_order,
            "embedded_center_q4_permutation_order": center4_perm_order,
            "embedded_center_full_e4_order": center4_full_order,
            "contexts": context_rows,
            "paper_vs_legacy_mismatch_contexts_by_outside_exponent": mismatch_contexts_by_outside,
            "paper_vs_canonical_mismatch_contexts_by_outside_exponent": canonical_mismatch_contexts_by_outside,
        },
        "verdict": {
            "status": "BLOCKED_E4_FIBRE_MISMATCH",
            "closed": "both conventions give the same coarse nine-row orbit and the same Pi3 27-fibres",
            "blocked": "paper/canonical and paper/legacy fibres differ in the E4 contexts used downstream",
            "required_repair": "regenerate all 162 branches from the literal paper formula with explicit zero-based rebasing, rerun bulk/prodrung, then use a producer-nonsharing checker",
        },
    }


def registry_and_primitives(q3: dict[str, Any], registry: dict[str, Any]) -> dict[str, Any]:
    require(registry["schema"] == "d972-b345-joint-kernel-qstar-closure/v1", "registry schema")
    block = registry["context_registry"]
    require(block["context_count"] == len(block["contexts"]) == 31, "31 context count")
    require(block["named_use_count"] == len(block["named_uses"]) == 46, "46 named-use count")
    require(digest_obj(block["contexts"]) == block["context_rows_sha256"], "context rows digest")
    require(digest_obj(block["named_uses"]) == block["named_use_mapping_sha256"], "named uses digest")
    pointers = {
        "/groups/PB3": q3["groups"]["PB3"],
        "/groups/PB4": q3["groups"]["PB4"],
        "/groups/PB5": q3["groups"]["PB5"],
        "/coarse_models/P": q3["coarse_models"]["P"],
        "/coarse_models/G9": q3["coarse_models"]["G9"],
        "/coarse_models/H9": q3["coarse_models"]["H9"],
        "/coarse_models/Q0": q3["coarse_models"]["Q0"],
        "/coarse_models/Q4": q3["coarse_models"]["Q4"],
        "/formulas/presentations/PB4/relations": q3["formulas"]["presentations"]["PB4"]["relations"],
        "/canonical_roof_powers/rows": q3["canonical_roof_powers"]["rows"],
        "/correction_fibre/records": q3["correction_fibre"]["records"],
    }
    return {
        "context_registry": {
            "context_count": 31,
            "context_rows_sha256": block["context_rows_sha256"],
            "named_use_count": 46,
            "named_use_mapping_sha256": block["named_use_mapping_sha256"],
            "scope": "registry artifact is a campaign legality input, not a runtime input of bulk162/prodrung",
        },
        "q3_embedded_primitive_tables": [
            {"json_pointer": pointer, "canonical_json_sha256": digest_obj(payload)}
            for pointer, payload in pointers.items()
        ],
        "pb5_boundary": "PB5 is summary_only in q3 chief; no PB5 Cayley table is present",
    }


def m2_lineage(m2_canary: dict[str, Any]) -> dict[str, Any]:
    require(m2_canary["schema"] == "koubou158-M2-msweep-v3-canary/v1", "M2 canary schema")
    require(m2_canary["status"] == "CANARY_ALL_FAIL_STOPPED", "M2 canary status")
    require(m2_canary["construction_source"].startswith("search/koubou158_m2_closedform_v1.py"),
            "M2 predecessor source")
    current_outputs = sorted(path.relative_to(ROOT).as_posix() for path in
                             (ROOT / "search/certs").glob("koubou158_M2_msweep_v3_measurement_*.json"))
    return {
        "predecessor_canary_schema": m2_canary["schema"],
        "predecessor_canary_status": m2_canary["status"],
        "predecessor_canary_construction_source": m2_canary["construction_source"],
        "current_v3_source": "search/koubou158_M2_msweep_v3.py",
        "current_v3_runtime_dependencies": [
            "search/koubou158_L3_core_v1_1.py",
            "search/koubou158_L3_core_completebfs_v1.py",
            "search/koubou158_m2_closedform_v2.py",
            Q3_PATH,
        ],
        "current_v3_measurement_files": current_outputs,
        "lineage_verdict": ("NO_CURRENT_V3_MEASUREMENT; 7ff02c... is predecessor closedform_v1 canary, "
                            "not output of current a6ab01... v3 source") if not current_outputs else
                           "CURRENT_V3_MEASUREMENT_PRESENT_SEPARATE_FROM_PREDECESSOR",
    }


def build_receipt() -> dict[str, Any]:
    inventory = pin_inventory()
    q3 = load_json(Q3_PATH)
    words = load_json(WORD_PATH)
    bulk = load_json(BULK_PATH)
    prodrung = load_json(PRODRUNG_PATH)
    m2_canary = load_json(M2_CANARY_PATH)
    registry = load_json(REGISTRY_PATH)
    structure = branch_structure(bulk, prodrung)
    formula = formula_audit(q3, words)
    auxiliary = registry_and_primitives(q3, registry)
    return {
        "schema": SCHEMA,
        "status": "STRUCTURAL_PASS_FORMULA_BLOCKED",
        "grade": "producer-only candidate; no independent checker; no branch promotion",
        "input_inventory": inventory,
        "inventory_sha256": digest_obj(inventory),
        "m2_lineage_separation": m2_lineage(m2_canary),
        "registry_and_primitives": auxiliary,
        "structural_branch_cover": structure,
        "kappa_formula_audit": formula,
        "gate5_accounting": {
            "closed": [
                "pinned evidence inventory",
                "canonical cert-defined 6x27 universe",
                "144/18 complement and canonical 18 unique roster",
                "prodrung 8/10 partition and j=2..5 rank receipts",
                "31-context registry counts/digests",
                "kappa sensitivity canaries (Pi3/Pi4 pc order 3; full E4 order 18)",
            ],
            "blocked": [
                "literal paper roof powers do not rebase to canonical 27-fibres in E4",
                "legacy and paper fibres differ for outside exponents 4,5,7 in contexts 0..3",
                "old bulk checker imports search-side producer helpers",
                "fresh paper-formula bulk/prodrung producer and nonsharing checker absent",
            ],
            "status": "PARTIAL_ONLY_DO_NOT_CLOSE_GATE5",
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", type=Path, help="compare a frozen receipt with a fresh reconstruction")
    parser.add_argument("--digest-only", action="store_true")
    args = parser.parse_args()
    receipt = build_receipt()
    blob = canonical_bytes(receipt)
    digest = hashlib.sha256(blob).hexdigest()
    if args.check is not None:
        frozen = json.loads(args.check.read_text(encoding="utf-8"))
        require(frozen == receipt, "frozen producer receipt differs")
        print(f"KOUBOU159B_BRANCH_COVER_PRODUCER_CHECK_PASS sha256={digest} "
              f"status={receipt['status']}")
    elif args.digest_only:
        print(digest)
    else:
        print(json.dumps(receipt, ensure_ascii=False, sort_keys=True, indent=2))
        print(f"KOUBOU159B_BRANCH_COVER_PRODUCER_PASS sha256={digest} "
              f"status={receipt['status']}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Stop as exc:
        print(f"KOUBOU159B_BRANCH_COVER_PRODUCER_STOP {exc}")
        raise SystemExit(1)
