#!/usr/bin/env python3
"""Independent direct-enumeration checker for the fresh g760 L3 gate.

This file imports neither the new producer nor any koubou158 L3 producer,
core, or result certificate.  It uses only the older frozen seedspan
arithmetic to reconstruct E4 from the authenticated q3 receipt, writes its
own target/Sigma expression path, and enumerates all 59,049 PC elements
for each of the eleven PB4 relators.
"""

from __future__ import annotations

import argparse
import copy
import functools
import hashlib
import importlib.util
import itertools
import json
import sys
import time
from collections import defaultdict, deque
from pathlib import Path
from typing import Any, Iterable, Sequence


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "d972-r07-760-l3-target6/v1"
FINAL_MARKER = "R07_760_L3_TARGET6_V1_CHECKER_PASS"
DEFAULT_RECEIPT = Path(
    "search/certs/d972_r07_760_l3_target6_preflight_v1_20260826.json")
Q3_PATH = Path(
    "ci/b345_157en_artifacts_32458556448/d972_b345_q3_chief_v1.json")
SEEDSPAN_PATH = Path("search/d972_b345_seedspan_triple4_v1.py")
J_ORDER = tuple(range(2, 13))
TRANSLATED_D2_COUNT = 11 * (3 ** 10)
MAX_DIMENSION = 180000
MAX_RSS_MIB = 5600

PARENT_SHA = "3680e8bcbac37747467175454b082485b2ae296f1fb05244435d8f44979d4e90"
BASE_SHA = "518f09820b8d7baee6b58ebf366cebf7b02a9a945cd1350cf8c701a4e6bc2b4d"
OLD20_SHA = "b79f105ec2963ae55b69480f8ed8ab13083d01cb936da32edb4798698c22055d"
PREFLIGHT_STATE = "R07_760_L3_TARGET6_PREFLIGHT_READY"

PIN_SPECS = {
    "task": (Path("sol/luna_task_163_r07_760_l3_target6_v1.md"),
        9066, "9fcdf2f25b724e9dbc225f417b0036e126e7b5e37a0778dab5e0299ee2f74e12"),
    "q3": (Q3_PATH, 231570,
        "3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72"),
    "seedspan": (SEEDSPAN_PATH, 535219,
        "fe18fc31fdf3f9416ebb829112ccbd514c27e6a8d30fe24691842865277a0b29"),
}

W2 = (
    1, 1, 1, 1, -2, -2, -2, -2, -1, 2, -1, -1, -2, -2, 1, 1,
    2, 1, 1, -2, 1, 1, 2, 1, 1, 2, 1, 1, -2, 1, 1, -2, 1, 1,
    2, 2, -1, -1, -2, -1,
)
W3 = (
    1, 1, 1, 1, -2, -2, -2, -2, -1, 2, -1, -1, -2, -1, -1, 2,
    -1, -1, -2, -2, 1, 1, 2, 1, 2, 2, 1, 2, 2, -1, 2, 2, 1, 2,
    1, 1, 2, 2, -1, -1, -2, -1, -1, 2, -1, -1, -2, -2, -2, -1,
    -2, -2, 1, 2, 1, 1, -2, 1,
)
OLD20 = (
    -2, -2, -1, -1, 2, 2, 1, -2, -1, -1,
    2, 2, 2, -1, -2, -2, 1, 1, 1, 1,
)
X0, Y0, Z0 = (4,), (6,), (-4, -6)
WEIGHTS = (1, 1, 1, 1, 1, 1, 2, 2, 2, 2)
BINOM = {0: (1, 0, 0), 1: (1, 1, 0), 2: (1, 2, 1)}


class ResourceStop(RuntimeError):
    pass


class Monitor:
    def __init__(self, seconds: float) -> None:
        require(0 < seconds <= 21600, "checker seconds")
        self.deadline = time.monotonic() + seconds
        self.checks = 0

    def check(self, stage: str, *, force: bool = False) -> None:
        self.checks += 1
        if not force and self.checks % 256:
            return
        if time.monotonic() >= self.deadline:
            raise ResourceStop("checker deadline: " + stage)
        try:
            import resource
            rss = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
            rss_mib = rss / 1024
            if sys.platform == "darwin":
                rss_mib = rss / (1024 * 1024)
            if rss_mib > MAX_RSS_MIB:
                raise ResourceStop(
                    f"checker RSS cap: {rss_mib:.1f} MiB at {stage}")
        except ImportError:
            pass


def require(condition: Any, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True).encode("ascii")


def digest_obj(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def digest_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def authenticate() -> None:
    for label, (path, size, digest) in PIN_SPECS.items():
        full = ROOT / path
        require(full.is_file() and full.stat().st_size == size and
                digest_file(full) == digest, "checker pin: " + label)


def load_seedspan() -> Any:
    spec = importlib.util.spec_from_file_location(
        "_r07_760_l3_seedspan_independent", ROOT / SEEDSPAN_PATH)
    require(spec is not None and spec.loader is not None,
            "seedspan module spec")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    try:
        spec.loader.exec_module(module)
    except BaseException:
        sys.modules.pop(spec.name, None)
        raise
    return module


def reduce_word(word: Iterable[int]) -> list[int]:
    out: list[int] = []
    for value in word:
        letter = int(value)
        require(letter != 0, "zero word letter")
        if out and out[-1] == -letter:
            out.pop()
        else:
            out.append(letter)
    return out


def inv_word(word: Sequence[int]) -> list[int]:
    return reduce_word(-int(x) for x in reversed(word))


def substitute2(word: Sequence[int], x: Sequence[int],
                y: Sequence[int]) -> list[int]:
    out: list[int] = []
    for letter in word:
        choices = {1: x, -1: inv_word(x), 2: y, -2: inv_word(y)}
        require(letter in choices, "F2 alphabet")
        out.extend(choices[letter])
        out = reduce_word(out)
    return out


def exponent_sums(word: Sequence[int]) -> list[int]:
    return [sum(1 if x == i else -1 if x == -i else 0 for x in word)
            for i in (1, 2)]


def construct_base() -> tuple[list[int], list[int]]:
    w2, w3 = list(W2), list(W3)
    parent = reduce_word(w2 + (inv_word(w3) + w2) * 8)
    base = reduce_word(parent + [2] * 36 + [-1] * 108)
    require(len(parent) == 616 and digest_obj(parent) == PARENT_SHA,
            "checker parent")
    require(len(base) == 760 and digest_obj(base) == BASE_SHA and
            exponent_sums(base) == [0, 0], "checker base")
    require(digest_obj(list(OLD20)) == OLD20_SHA, "checker old20")
    return parent, base


def element_blob(value: Any) -> bytes:
    return bytes(value[0]) + bytes(value[1])


def serialize_e4_gradient(row: dict[Any, int]) -> list[list[Any]]:
    return [[int(component), element_blob(value).hex(), int(coefficient) % 3]
            for (component, value), coefficient in sorted(
                row.items(), key=lambda item:
                    (int(item[0][0]), element_blob(item[0][1])))
            if int(coefficient) % 3]


def serialize_pc_gradient(row: dict[Any, int]) -> list[list[Any]]:
    return [[int(component), bytes(value).hex(), int(coefficient) % 3]
            for (component, value), coefficient in sorted(
                row.items(), key=lambda item:
                    (int(item[0][0]), bytes(item[0][1])))
            if int(coefficient) % 3]


def projected_public(row: dict[Any, int]) -> list[list[Any]]:
    return [[int(component), list(monomial), int(coefficient) % 3]
            for (component, monomial), coefficient in sorted(
                row.items(), key=lambda item: (item[0][0], item[0][1]))
            if int(coefficient) % 3]


def fox_gradient(e4: Any, word: Sequence[int]) -> dict[Any, int]:
    out: dict[Any, int] = defaultdict(int)
    prefix = e4.identity
    for letter in word:
        component = abs(int(letter))
        generator = e4.generators[component - 1]
        if letter > 0:
            out[(component, prefix)] += 1
            prefix = e4.mul(prefix, generator)
        else:
            prefix = e4.mul(prefix, e4.inverse(generator))
            out[(component, prefix)] -= 1
    return {key: value % 3 for key, value in out.items() if value % 3}


def collapse_to_pc(row: dict[Any, int]) -> dict[Any, int]:
    out: dict[Any, int] = defaultdict(int)
    for (component, value), coefficient in row.items():
        key = (component, value[1])
        out[key] = (out[key] + int(coefficient)) % 3
    return {key: value for key, value in out.items() if value}


def add_vec(left: dict[Any, int], right: dict[Any, int]) -> dict[Any, int]:
    out: dict[Any, int] = defaultdict(int)
    for key, value in itertools.chain(left.items(), right.items()):
        out[key] = (out[key] + int(value)) % 3
    return {key: value for key, value in out.items() if value}


def neg_vec(row: dict[Any, int]) -> dict[Any, int]:
    return {key: (-int(value)) % 3 for key, value in row.items()
            if int(value) % 3}


def translate_e4(e4: Any, row: dict[Any, int], g: Any) -> dict[Any, int]:
    out: dict[Any, int] = defaultdict(int)
    for (component, value), coefficient in row.items():
        key = (component, e4.mul(g, value))
        out[key] = (out[key] + int(coefficient)) % 3
    return {key: value for key, value in out.items() if value}


def pc_translate(pc: Any, row: dict[Any, int], g: bytes) -> dict[Any, int]:
    out: dict[Any, int] = defaultdict(int)
    for (component, value), coefficient in row.items():
        key = (component, pc.mul(g, value))
        out[key] = (out[key] + int(coefficient)) % 3
    return {key: value for key, value in out.items() if value}


def verify_weights(q3: dict[str, Any]) -> dict[str, Any]:
    pb4 = q3["groups"]["PB4"]
    require(pb4["nilpotency_class"] == 2 and
            pb4["generator_count"] == 10, "checker PC dimensions")
    require(all(int(x) == 3 for x in pb4["relative_orders"]) and
            all(all(int(v) == 0 for v in row)
                for row in pb4["power_relations"]), "checker exponent")
    violations = []
    for entry in pb4["conjugate_relations"]:
        i, j = int(entry["i"]), int(entry["j"])
        coords = [int(x) for x in entry["coords"]]
        if i > 6 or j > 6:
            if coords != [1 if k + 1 == i else 0 for k in range(10)]:
                violations.append([i, j])
        elif any(coords[k] and k + 1 <= 6 and k + 1 != i
                 for k in range(10)):
            violations.append([i, j])
    require(not violations, "checker Jennings weights")
    return {"weights": [1] * 6 + [2] * 4,
            "conjugate_relations_checked":
                len(pb4["conjugate_relations"]),
            "power_relations_checked": len(pb4["power_relations"]),
            "violations": 0}


def delta_and_schreier(e4: Any) \
        -> tuple[list[list[int]], dict[str, Any]]:
    pc = e4.pc
    xbar, ybar, zbar = (e4.eval(list(word))[1]
                         for word in (X0, Y0, Z0))
    require(zbar == pc.inverse(pc.mul(ybar, xbar)),
            "checker zbar identity")
    generators = {
        1: (xbar, xbar, ybar),
        2: (ybar, zbar, zbar),
    }
    identity = (pc.one(), pc.one(), pc.one())
    transversal = {identity: []}
    order = [identity]
    tree = set()
    queue = deque([identity])
    while queue:
        current = queue.popleft()
        for letter in (1, 2):
            nxt = tuple(pc.mul(current[i], generators[letter][i])
                        for i in range(3))
            if nxt not in transversal:
                require(len(order) < 40, "checker Delta cap")
                transversal[nxt] = transversal[current] + [letter]
                order.append(nxt)
                tree.add((current, letter))
                queue.append(nxt)
    words = []
    for current in order:
        for letter in (1, 2):
            if (current, letter) in tree:
                continue
            nxt = tuple(pc.mul(current[i], generators[letter][i])
                        for i in range(3))
            words.append(reduce_word(
                transversal[current] + [letter] + inv_word(transversal[nxt])))
    require(len(order) == 27 and len(words) == 28,
            "checker Schreier roster")
    g1, g2 = generators[1], generators[2]
    commute = tuple(pc.mul(g1[i], g2[i]) for i in range(3)) == \
        tuple(pc.mul(g2[i], g1[i]) for i in range(3))
    return words, {
        "order_Delta": len(order),
        "isomorphism_type": (
            "elementary_abelian_C3^3" if commute else
            "nonabelian_exponent3_order27_class2"),
        "schreier_generator_count": len(words),
        "schreier_rank_formula": "1+[Delta:F2_image]*(2-1)=28",
        "schreier_words_sha256": digest_obj(words),
        "full_kernel_generating_set": True,
    }


def monomials(j: int) -> list[tuple[int, ...]]:
    return sorted(tuple(row) for row in itertools.product(range(3), repeat=10)
                  if sum(a * w for a, w in zip(row, WEIGHTS)) < j)


def build_static_independent() -> tuple[dict[str, Any], dict[str, Any]]:
    authenticate()
    ss = load_seedspan()
    q3 = json.loads((ROOT / Q3_PATH).read_text(encoding="utf-8"))
    require(q3["schema"] == "d972-b345-q-chief/v1", "checker q3 schema")
    _, e4, _ = ss.reconstruct_quotients(q3)
    parent, base = construct_base()

    A = substitute2(base, X0, Y0)
    B = substitute2(base, X0, Z0)
    C = substitute2(base, Y0, Z0)
    target_word = reduce_word(C + inv_word(B) + A)
    alt_no_inverse = reduce_word(C + B + A)
    alt_reordered = reduce_word(A + inv_word(B) + C)
    target_raw = fox_gradient(e4, target_word)
    target_pc = collapse_to_pc(target_raw)
    require(e4.eval(target_word) == e4.identity,
            "checker target E4 value")
    Abar, Bbar, Cbar = (e4.eval(word) for word in (A, B, C))
    prefix = e4.mul(Bbar, e4.inverse(Cbar))
    prefix_inverse = e4.inverse(prefix)
    require(prefix != prefix_inverse, "checker prefix discriminant")

    schreier, delta_public = delta_and_schreier(e4)
    pc_one = e4.pc.one()
    sigma_pc = []
    legal_rows = []
    for ordinal, word in enumerate(schreier, 1):
        values = [
            e4.eval(substitute2(word, left, right))[1]
            for left, right in ((X0, Y0), (X0, Z0), (Y0, Z0))]
        require(values == [pc_one, pc_one, pc_one],
                f"checker context identity {ordinal}")
        ga = fox_gradient(e4, substitute2(word, X0, Y0))
        gb = fox_gradient(e4, substitute2(word, X0, Z0))
        gc = fox_gradient(e4, substitute2(word, Y0, Z0))
        sigma = add_vec(
            translate_e4(e4, add_vec(gc, neg_vec(gb)), prefix), ga)
        pcrow = collapse_to_pc(sigma)
        sigma_pc.append(pcrow)
        public = serialize_pc_gradient(pcrow)
        legal_rows.append({
            "ordinal": ordinal, "schreier_word": word,
            "schreier_word_sha256": digest_obj(word),
            "projected_sigma": public,
            "projected_sigma_sha256": digest_obj(public),
        })

    derived_relators = ss.pure_relations(4)
    receipt_relators = q3["formulas"]["presentations"]["PB4"]["relations"]
    require(derived_relators == receipt_relators and
            len(derived_relators) == 11,
            "checker independently derived PB4 roster")
    relator_pc = []
    relator_rows = []
    for ordinal, word in enumerate(derived_relators, 1):
        require(e4.eval(word) == e4.identity,
                f"checker relator {ordinal}")
        pcrow = collapse_to_pc(fox_gradient(e4, word))
        relator_pc.append(pcrow)
        public = serialize_pc_gradient(pcrow)
        relator_rows.append({
            "ordinal": ordinal, "word": word,
            "word_sha256": digest_obj(word),
            "projected_gradient": public,
            "projected_gradient_sha256": digest_obj(public),
        })

    basis_manifest = []
    for j in J_ORDER:
        basis = monomials(j)
        basis_manifest.append({
            "j": j, "monomial_count": len(basis),
            "dim_Lambda_over_Ij": 6 * len(basis),
            "basis_sha256": digest_obj([list(row) for row in basis]),
        })

    old_A = substitute2(OLD20, X0, Y0)
    old_B = substitute2(OLD20, X0, Z0)
    old_C = substitute2(OLD20, Y0, Z0)
    old_target = reduce_word(old_C + inv_word(old_B) + old_A)
    old_target_raw = fox_gradient(e4, old_target)

    public = {
        "implementation_parent_commit":
            "f3698fffd3b73370f753c4b0d9eb1e86751b1159",
        "base": {
            "base_kind": "r07_760_commutator",
            "construction": "w2*(w3^-1*w2)^8*y^36*x^-108",
            "parent_616_word": parent,
            "parent_616_sha256": digest_obj(parent),
            "signed_word": base, "length": len(base),
            "sha256": digest_obj(base),
            "free_exponent_sums": exponent_sums(base),
        },
        "target6": {
            "name": "hexagon_1_coface_0",
            "formula": "C*B^-1*A",
            "X0": list(X0), "Y0": list(Y0), "Z0": list(Z0),
            "A_word_sha256": digest_obj(A),
            "B_word_sha256": digest_obj(B),
            "C_word_sha256": digest_obj(C),
            "word": target_word, "word_length": len(target_word),
            "word_sha256": digest_obj(target_word),
            "alternative_CBA_sha256": digest_obj(alt_no_inverse),
            "alternative_ABinvC_sha256": digest_obj(alt_reordered),
            "raw_E4_gradient": serialize_e4_gradient(target_raw),
            "raw_E4_gradient_sha256":
                digest_obj(serialize_e4_gradient(target_raw)),
            "projected_L3_gradient": serialize_pc_gradient(target_pc),
            "projected_L3_gradient_sha256":
                digest_obj(serialize_pc_gradient(target_pc)),
            "value_identity_in_current_E4": True,
        },
        "prefix_action": {
            "formula": "fbar_xz*fbar_yz^-1",
            "value_hex": element_blob(prefix).hex(),
            "value_sha256": digest_obj(element_blob(prefix).hex()),
            "inverse_value_hex": element_blob(prefix_inverse).hex(),
            "inverse_is_distinct": True,
            "fresh_from_g760": True,
        },
        "legal_overapproximation": {
            "Delta": delta_public,
            "rows": legal_rows, "row_count": len(legal_rows),
            "rows_sha256": digest_obj(legal_rows),
            "all_84_context_values_identity_in_Pi4_3": True,
            "Sigma_homomorphism_on_K":
                "paper one-line: cbar=1 makes Sigma(cd)=Sigma(c)+Sigma(d)",
            "H1_span_equals_full_K_image": True,
            "literal_legal_image_subset_full_K_span": True,
            "overapproximation_safe_direction": "NONMEMBERSHIP_ONLY",
        },
        "PB4_D2": {
            "relation_count": len(relator_rows),
            "relators": relator_rows,
            "relators_sha256": digest_obj(relator_rows),
            "full_translate_count": TRANSLATED_D2_COUNT,
            "base_independent_but_freshly_authenticated": True,
        },
        "Jennings": {
            "weights": verify_weights(q3),
            "j_order": list(J_ORDER), "first_terminal_rule": True,
            "basis_manifest": basis_manifest,
            "projection_enlargement":
                "E4 -> Pi4[3], safe only for NONMEMBERSHIP",
        },
        "historical_old20_diagnostic_only": {
            "signed_word_sha256": digest_obj(list(OLD20)),
            "target_word_sha256": digest_obj(old_target),
            "raw_E4_gradient_sha256":
                digest_obj(serialize_e4_gradient(old_target_raw)),
            "historical_j4_ranks": {
                "D2bar_alone": 310, "V": 4, "combined": 314},
            "imported_as_answer": False,
        },
        "freshness_boundary": {
            "old20_target_imported": False,
            "old20_ranks_required": False,
            "old616_target_imported": False,
            "historical_blocker_imported": False,
            "historical_B0_B1_imported": False,
            "registered_108_family_used": False,
            "literal_five_coface_A18_built": False,
        },
    }
    private = {"e4": e4, "target_pc": target_pc,
               "sigma_pc": sigma_pc, "relator_pc": relator_pc}
    return public, private


class SparseTracker:
    def __init__(self, pivots: dict[int, dict[int, int]] | None = None) -> None:
        self.pivots = copy.deepcopy(pivots) if pivots is not None else {}

    def clone(self) -> "SparseTracker":
        return SparseTracker(self.pivots)

    def reduce(self, vector: dict[int, int]) -> dict[int, int]:
        row = {int(k): int(v) % 3 for k, v in vector.items() if int(v) % 3}
        while row:
            pivot = min(row)
            basis = self.pivots.get(pivot)
            if basis is None:
                break
            coefficient = row[pivot]
            for key, value in basis.items():
                new = (row.get(key, 0) - coefficient * value) % 3
                if new:
                    row[key] = new
                else:
                    row.pop(key, None)
        return row

    def add(self, vector: dict[int, int]) -> bool:
        row = self.reduce(vector)
        if not row:
            return False
        pivot = min(row)
        scalar = row[pivot]
        self.pivots[pivot] = {
            key: (value * scalar) % 3 for key, value in row.items()}
        return True

    @property
    def rank(self) -> int:
        return len(self.pivots)

    def separator(self, target: dict[int, int]) -> dict[int, int] | None:
        remainder = self.reduce(target)
        if not remainder:
            return None
        coordinate = min(remainder)
        phi = {coordinate: 1}
        # Pivot insertion order is streaming-dependent and need not be
        # monotone.  A row at pivot p only uses coordinates > p, so dual
        # back-substitution must follow numeric pivot order, descending.
        for pivot in sorted(self.pivots, reverse=True):
            row = self.pivots[pivot]
            value = -sum(coefficient * phi.get(key, 0)
                         for key, coefficient in row.items()
                         if key != pivot)
            value %= 3
            if value:
                phi[pivot] = value
        return phi


def dot(phi: dict[int, int], row: dict[int, int]) -> int:
    return sum(int(value) * phi.get(key, 0)
               for key, value in row.items()) % 3


def projection_factory(j: int) -> tuple[
        list[tuple[int, ...]], dict[tuple[int, ...], int], Any]:
    basis = monomials(j)
    if 6 * len(basis) > MAX_DIMENSION:
        raise ResourceStop(f"checker dimension cap at j={j}")
    index = {row: ordinal for ordinal, row in enumerate(basis)}

    @functools.lru_cache(maxsize=8192)
    def expand(pcvec: bytes) -> tuple[tuple[int, int], ...]:
        out: dict[int, int] = defaultdict(int)
        ranges = [range(int(a) + 1) for a in pcvec]
        for exponent in itertools.product(*ranges):
            ordinal = index.get(tuple(exponent))
            if ordinal is None:
                continue
            coefficient = 1
            for a, e in zip(pcvec, exponent):
                coefficient = coefficient * BINOM[int(a)][int(e)] % 3
            if coefficient:
                out[ordinal] = (out[ordinal] + coefficient) % 3
        return tuple((key, value) for key, value in sorted(out.items())
                     if value)

    def project(row: dict[Any, int]) -> dict[int, int]:
        out: dict[int, int] = defaultdict(int)
        width = len(basis)
        for (component, pcvec), coefficient in row.items():
            offset = (int(component) - 1) * width
            for ordinal, scalar in expand(bytes(pcvec)):
                key = offset + ordinal
                out[key] = (
                    out[key] + int(coefficient) * int(scalar)) % 3
        return {key: value for key, value in out.items() if value}

    return basis, index, project


def indexed_to_public(row: dict[int, int],
                      basis: Sequence[tuple[int, ...]]) -> list[list[Any]]:
    width = len(basis)
    answer = []
    for coordinate, coefficient in sorted(row.items()):
        component = coordinate // width + 1
        monomial = basis[coordinate % width]
        answer.append([component, list(monomial), int(coefficient) % 3])
    return answer


def enumerate_translated_rows(e4: Any, relators: Sequence[dict[Any, int]],
                              project: Any, monitor: Monitor,
                              stage: str) -> Iterable[dict[int, int]]:
    for relator in relators:
        for coords in itertools.product(range(3), repeat=10):
            monitor.check(stage)
            yield project(pc_translate(e4.pc, relator, bytes(coords)))


def verify_phi_stream(e4: Any, phi: dict[int, int],
                      legal: Sequence[dict[int, int]],
                      relators: Sequence[dict[Any, int]],
                      target: dict[int, int], project: Any,
                      monitor: Monitor, stage: str) -> dict[str, Any]:
    bad_legal = sum(dot(phi, row) != 0 for row in legal)
    bad_boundary = 0
    count = 0
    for row in enumerate_translated_rows(
            e4, relators, project, monitor, stage):
        count += 1
        if dot(phi, row):
            bad_boundary += 1
    target_dot = dot(phi, target)
    require(bad_legal == 0 and bad_boundary == 0 and
            count == TRANSLATED_D2_COUNT and target_dot != 0,
            "checker lossless separator pairing")
    return {
        "legal_rows_checked": len(legal),
        "legal_nonzero_pairings": 0,
        "translated_boundary_rows_checked": count,
        "translated_boundary_nonzero_pairings": 0,
        "target_pairing": target_dot,
        "all_generated_rows_annihilated": True,
        "target_pairing_nonzero": True,
        "direct_all_59049_elements_x_11_relators": True,
    }


def direct_j(private: dict[str, Any], j: int,
             monitor: Monitor) -> dict[str, Any]:
    e4 = private["e4"]
    basis, _, project = projection_factory(j)
    legal_rows = [project(row) for row in private["sigma_pc"]]
    legal_tracker = SparseTracker()
    combined = SparseTracker()
    for row in legal_rows:
        legal_tracker.add(row)
        combined.add(row)
    d2 = SparseTracker()
    count = 0
    for row in enumerate_translated_rows(
            e4, private["relator_pc"], project, monitor,
            f"checker j={j} direct rank"):
        count += 1
        d2.add(row)
        combined.add(row)
    require(count == TRANSLATED_D2_COUNT, "checker translated count")
    target = project(private["target_pc"])
    phi = combined.separator(target)
    nonmember = phi is not None
    own_separator = None
    if phi is not None:
        terms = indexed_to_public(phi, basis)
        pairing = verify_phi_stream(
            e4, phi, legal_rows, private["relator_pc"], target,
            project, monitor, f"checker j={j} own separator")
        own_separator = {
            "terms": terms, "terms_sha256": digest_obj(terms),
            "support": len(terms), "pairing_replay": pairing,
        }
    legal_public = [
        indexed_to_public(row, basis) for row in legal_rows]
    return {
        "semantic": {
            "j": j, "monomial_count": len(basis),
            "dim_Lambda_over_Ij": 6 * len(basis),
            "basis_sha256": digest_obj([list(row) for row in basis]),
            "rank_D2bar_alone": d2.rank,
            "rank_legal_overapproximation": legal_tracker.rank,
            "rank_combined": combined.rank,
            "target_projected_sha256":
                digest_obj(indexed_to_public(target, basis)),
            "legal_projected_rows_sha256": digest_obj(legal_public),
            "PB4_translate_count": count,
            "nonmember": nonmember,
        },
        "basis": basis, "project": project,
        "legal_rows": legal_rows, "target": target,
        "own_separator": own_separator,
    }


def independent_full(private: dict[str, Any], seconds: float) \
        -> dict[str, Any]:
    monitor = Monitor(seconds)
    progression = []
    rows = {}
    first = None
    for j in J_ORDER:
        monitor.check(f"checker j={j} start", force=True)
        row = direct_j(private, j, monitor)
        progression.append(row["semantic"])
        rows[j] = row
        if row["semantic"]["nonmember"]:
            first = j
            break
    terminal = ("R07_760_L3_TARGET6_NONMEMBER" if first is not None else
                "R07_760_L3_TARGET6_MEMBER_INCONCLUSIVE")
    return {"terminal": terminal, "first_nonmember_j": first,
            "progression": progression, "rows": rows,
            "monitor": monitor}


def verify_envelope(data: dict[str, Any], raw: bytes) -> None:
    require(raw == canonical_bytes(data) + b"\n", "canonical receipt")
    require(data["schema"] == SCHEMA, "checker schema")
    claimed = data.pop("self_digest_sha256")
    require(claimed == digest_obj(data), "checker self digest")
    data["self_digest_sha256"] = claimed
    require(all(value is False for value in data["claims"].values()),
            "checker global claims")


def authenticate_receipt_pins(rows: dict[str, Any]) -> None:
    require(type(rows) is dict and rows, "receipt pin manifest")
    for label, row in rows.items():
        path = ROOT / row["path"]
        require(path.is_file() and path.stat().st_size == int(row["bytes"]) and
                digest_file(path) == row["sha256"],
                "receipt pin replay: " + label)


def compare_static(observed: dict[str, Any],
                   expected: dict[str, Any]) -> None:
    authenticate_receipt_pins(observed["pins"])
    projected = {key: value for key, value in observed.items()
                 if key != "pins"}
    require(projected == expected, "independent static mismatch")


def parse_phi(terms: Sequence[Sequence[Any]],
              basis: Sequence[tuple[int, ...]]) -> dict[int, int]:
    width = len(basis)
    index = {row: ordinal for ordinal, row in enumerate(basis)}
    phi: dict[int, int] = {}
    for component, monomial, coefficient in terms:
        key_tuple = tuple(int(x) for x in monomial)
        require(1 <= int(component) <= 6 and key_tuple in index and
                int(coefficient) in (1, 2), "producer separator term")
        coordinate = (int(component) - 1) * width + index[key_tuple]
        require(coordinate not in phi, "producer separator duplicate")
        phi[coordinate] = int(coefficient)
    require(phi, "producer separator nonempty")
    return phi


def compare_full(data: dict[str, Any], independent: dict[str, Any],
                 expected_static: dict[str, Any],
                 private: dict[str, Any], mutations: bool) -> int:
    compare_static(data["static"], expected_static)
    require(data["terminal_token"] == independent["terminal"] and
            data["result"]["state"] == independent["terminal"] and
            data["result"]["first_nonmember_j"] ==
                independent["first_nonmember_j"],
            "checker terminal agreement")
    observed_rows = data["result"]["j_progression"]
    require(len(observed_rows) == len(independent["progression"]),
            "checker progression length")
    semantic_keys = {
        "j", "monomial_count", "dim_Lambda_over_Ij", "basis_sha256",
        "rank_D2bar_alone", "rank_legal_overapproximation",
        "rank_combined", "target_projected_sha256",
        "legal_projected_rows_sha256", "PB4_translate_count", "nonmember",
    }
    for observed, expected in zip(
            observed_rows, independent["progression"]):
        require({key: observed[key] for key in semantic_keys} == expected,
                f"checker rank/target mismatch j={expected['j']}")
        require(observed["producer_D2_algorithm"] ==
                "saturated (x_i-1) BFS, D2 first" and
                len(observed["per_relator_closure_receipts"]) == 11,
                "checker producer algorithm receipt")

    count = 0
    if independent["first_nonmember_j"] is not None:
        j = independent["first_nonmember_j"]
        row = independent["rows"][j]
        producer_sep = observed_rows[-1]["separator"]
        phi = parse_phi(producer_sep["terms"], row["basis"])
        require(producer_sep["terms_sha256"] ==
                digest_obj(producer_sep["terms"]) and
                producer_sep["support"] == len(phi),
                "producer separator serialization")
        pairing = verify_phi_stream(
            private["e4"], phi, row["legal_rows"],
            private["relator_pc"], row["target"], row["project"],
            independent["monitor"], "checker producer separator")
        require(producer_sep["pairing_replay"] == pairing,
                "producer separator full replay")
        if mutations:
            require(dot({}, row["target"]) == 0,
                    "forged zero separator must annihilate target")
            witness_row = next(
                (value for value in row["legal_rows"] if value), None)
            if witness_row is None:
                witness_row = next(enumerate_translated_rows(
                    private["e4"], private["relator_pc"], row["project"],
                    independent["monitor"], "checker mutation witness"))
            coordinate = min(witness_row)
            forged = dict(phi)
            forged[coordinate] = (forged.get(coordinate, 0) + 1) % 3
            if forged.get(coordinate) == 0:
                forged.pop(coordinate)
            require(dot(forged, witness_row) != 0,
                    "forged row-missing separator detected")
            count += 2
    require(data["result"]["registered_108_family_used"] is False and
            data["result"]["literal_A18_computed"] is False and
            data["result"]["normalized_Brunnian_class_computed"] is False,
            "checker result boundary")
    return count


def validate_stop(data: dict[str, Any]) -> None:
    require(data["mode"] == "full" and data["terminal_token"] in {
        "R07_760_L3_TARGET6_UNKNOWN_RESOURCE",
        "R07_760_L3_TARGET6_INPUT_STOP"} and
        data["status"] == data["terminal_token"],
        "checker stop terminal")
    base = data["static"]["base"]
    require(base["sha256"] == BASE_SHA and base["length"] == 760 and
            base["free_exponent_sums"] == [0, 0],
            "checker stop base")
    freshness = data["static"]["freshness_boundary"]
    require(all(value is False for value in freshness.values()),
            "checker stop freshness")
    result = data["result"]
    require(result["state"] == data["terminal_token"] and
            type(result["stage"]) is str and result["stage"] and
            type(result["reason"]) is str and result["reason"] and
            result["mathematical_membership_claimed"] is False and
            result["mathematical_nonmembership_claimed"] is False,
            "checker claim-free stop")


def toy_separator_tests() -> int:
    tracker = SparseTracker()
    tracker.add({0: 1}); tracker.add({1: 1})
    require(not tracker.reduce({0: 2, 1: 1}), "toy member")
    target = {2: 1}
    phi = tracker.separator(target)
    require(phi is not None and dot(phi, target) != 0 and
            all(dot(phi, row) == 0 for row in tracker.pivots.values()),
            "toy nonmember")
    require(dot({}, target) == 0, "toy forged target-zero")
    forged = dict(phi); forged[0] = 1
    require(dot(forged, tracker.pivots[0]) != 0,
            "toy forged missed row")

    # Destructive canary for insertion-order back-substitution.  These
    # pivots are inserted as 2,0,1.  The former reversed-insertion loop
    # visits 1,0,2 and fails to annihilate the pivot-1 row.
    unordered = SparseTracker()
    require(unordered.add({2: 1, 3: 1}) and
            unordered.add({0: 1, 1: 1}) and
            unordered.add({1: 1, 2: 1}) and
            list(unordered.pivots) == [2, 0, 1],
            "nonmonotone pivot insertion canary")
    unordered_phi = unordered.separator({3: 1})
    require(unordered_phi is not None and
            dot(unordered_phi, {3: 1}) != 0 and
            all(dot(unordered_phi, row) == 0
                for row in unordered.pivots.values()),
            "numeric reverse-pivot separator")
    old_bad = {3: 1}
    for pivot in reversed(list(unordered.pivots)):
        row = unordered.pivots[pivot]
        value = -sum(coefficient * old_bad.get(key, 0)
                     for key, coefficient in row.items() if key != pivot)
        if value % 3:
            old_bad[pivot] = value % 3
    require(any(dot(old_bad, row) != 0
                for row in unordered.pivots.values()),
            "insertion-order mutation rejected")
    return 3


def mutation_suite(data: dict[str, Any],
                   expected: dict[str, Any]) -> int:
    mutations = []

    def add(label: str, mutate: Any) -> None:
        bad = copy.deepcopy(data)
        mutate(bad)
        try:
            compare_static(bad["static"], expected)
        except RuntimeError:
            mutations.append(label)
            return
        raise RuntimeError("mutation survived: " + label)

    add("tail_sign", lambda d: d["static"]["base"]["signed_word"]
        .__setitem__(-1, 1))
    add("base_sha", lambda d: d["static"]["base"]
        .update({"sha256": "0" * 64}))
    add("target_order", lambda d: d["static"]["target6"]
        .update({"formula": "C*B*A"}))
    add("prefix_inverse", lambda d: d["static"]["prefix_action"]
        .update({"value_hex": d["static"]["prefix_action"]["inverse_value_hex"]}))
    add("PB4_coefficient", lambda d: d["static"]["PB4_D2"]["relators"][0]
        ["projected_gradient"][0].__setitem__(
            2, 3 - d["static"]["PB4_D2"]["relators"][0]
                ["projected_gradient"][0][2]))
    add("Jennings_coordinate", lambda d: d["static"]["Jennings"]
        ["basis_manifest"][0].update({"basis_sha256": "1" * 64}))
    add("legal_row_omitted", lambda d: d["static"]
        ["legal_overapproximation"]["rows"].pop())
    add("historical_substitution", lambda d: d["static"]["target6"].update({
        "word_sha256": d["static"]["historical_old20_diagnostic_only"]
            ["target_word_sha256"]}))
    count = len(mutations) + toy_separator_tests()
    require(len(mutations) == 8 and count == 11,
            "mutation count")
    return count


def check(path: Path, *, full: bool, mutations: bool,
          seconds: float) -> dict[str, Any]:
    raw = path.read_bytes()
    data = json.loads(raw.decode("ascii"))
    verify_envelope(data, raw)
    if data.get("terminal_token") in {
            "R07_760_L3_TARGET6_UNKNOWN_RESOURCE",
            "R07_760_L3_TARGET6_INPUT_STOP"}:
        validate_stop(data)
        count = toy_separator_tests() if mutations else 0
        print(FINAL_MARKER + f" terminal={data['terminal_token']} "
              f"mutations={count} full_replay=false "
              f"receipt_sha256={hashlib.sha256(raw).hexdigest()}", flush=True)
        return data

    expected_static, private = build_static_independent()
    if full:
        require(data["mode"] == "full", "checker full mode")
        independent = independent_full(private, seconds)
        count = compare_full(
            data, independent, expected_static, private, mutations)
        full_replay = True
    else:
        require(data["mode"] == "preflight" and
                data.get("preflight_state") == PREFLIGHT_STATE and
                "terminal_token" not in data and "status" not in data,
                "checker preflight mode")
        compare_static(data["static"], expected_static)
        count = mutation_suite(data, expected_static) if mutations else 0
        full_replay = False
    state_key = "terminal_token" if full else "preflight_state"
    state_label = "terminal" if full else "preflight_state"
    print(FINAL_MARKER + f" {state_label}={data[state_key]} "
          f"mutations={count} full_replay={str(full_replay).lower()} "
          f"receipt_sha256={hashlib.sha256(raw).hexdigest()}", flush=True)
    return data


def self_test() -> None:
    construct_base()
    count = toy_separator_tests()
    require(count == 3, "checker toy mutation count")
    print("R07_760_L3_TARGET6_V1_CHECKER_SELFTEST_PASS "
          "toy_member=1 toy_nonmember=1 separator_mutations=3", flush=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--receipt", type=Path, default=DEFAULT_RECEIPT)
    parser.add_argument("--full", action="store_true")
    parser.add_argument("--mutations", action="store_true")
    parser.add_argument("--seconds", type=float, default=10800.0)
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return 0
    path = args.receipt if args.receipt.is_absolute() else ROOT / args.receipt
    check(path, full=args.full, mutations=args.mutations,
          seconds=args.seconds)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
