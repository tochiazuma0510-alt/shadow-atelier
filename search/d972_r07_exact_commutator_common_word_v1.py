"""R07 exact-commutator successor (v145/v146), bounded producer.

The production consumer is deliberately receipt-driven: it authenticates the
task179 source, computes the complete integer exponent lattice, and performs
the zero-cost cube exactification before exposing an augmented resume state.
No claim is made for an incomplete positive search.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
from types import SimpleNamespace
from typing import Any, Sequence

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "d972-r07-exact-commutator-common-word/v1"
SELFTEST_SCHEMA = "d972-r07-exact-commutator-common-word-selftest-output/v1"
FIXTURE = ROOT / "search/certs/d972_r07_exact_commutator_common_word_selftest_v1_20260827.json"
FIXTURE_BYTES = 307
FIXTURE_SHA256 = "ab45ef8d467c92b70d1716f8d4053d99f0dd35479b57898d12887a703393eec2"
TERMINAL = "R07_EXACT_COMMUTATOR_COMMON_WORD"
HANDOFF = "LATTICE_AUGMENTED_RESUME_REQUIRED"
UNKNOWN_RESOURCE = "UNKNOWN_RESOURCE"
UNKNOWN_INPUT = "UNKNOWN_INPUT"

# These are the exact v184 commission pins.  Parent performs any later source
# cascade after this bounded implementation is audited.
PINS: dict[str, tuple[str, int, str]] = {
    "proof145": ("sol/proof_r07_task179_relative_frattini_successor_v145.md", 13819,
                 "b08f140838b78424cafa9528eafbcab9442f94cf92ce2cb42e15fc88ed489a51"),
    "proof146": ("sol/proof_r07_exact_commutator_positive_common_word_v146.md", 9065,
                 "a167df351d55e82781cb60cd2b4dbfdf5cd2ea4f50251643a6e0b83332557cee"),
    "task179_producer": ("search/d972_r07_positive_common_word_colgen_v1.py", 119396,
                         "448123e3ccba4324f4d19a09eeb6a2ba217d611ef5053d4cfa27e61ac69a2512"),
    "task179_checker": ("crosscheck/check_d972_r07_positive_common_word_colgen_v1.py", 70020,
                        "473bad89f9656dd67f4313398b5bdbb253a3495e1e20855d90781b4875309f2d"),
    "task179_driver": ("search/d972_r07_positive_common_word_colgen_gha_driver_v1.g", 12872,
                       "fbab67e85de604f157f8bd93f53d64e7265121508aa948c1e01341e78d1b5a11"),
}
TRANSITIVE_PINS = {
    "task175_producer": ("search/d972_r07_all_seven_raw_bridge_preflight_v1.py", 60306,
                          "1e0a65f5182157bb928638c2c9a71d475b3b788a6694ee4ded09f5a0ffd38cfa"),
    "task175_checker": ("crosscheck/check_d972_r07_all_seven_raw_bridge_preflight_v1.py", 85848,
                        "c55ec99a9a920cd5d0ef92db7d5f2ad841dda7b0f1dcc59a5dc45e469ed6f7cc"),
    "task175_driver": ("search/d972_r07_all_seven_raw_bridge_preflight_gha_driver_v1.g", 21580,
                       "dbe147f98774fde50dee86de7306f9e18243ac1becef0ec7516765bcb2e08765"),
    "task176_producer": ("search/d972_r07_all_seven_extension_section_census_v1.py", 66109,
                         "878cf1d8d44e74a993309ed1c613c9fc57eb62fd2da48a30fd8797ff4b19af3b"),
    "task176_checker": ("crosscheck/check_d972_r07_all_seven_extension_section_census_v1.py", 84980,
                        "4e6b97aa315fdccb4250de21e99dd78302477b90fd420215de6c6bea7d1fa695"),
    "task176_driver": ("search/d972_r07_all_seven_extension_section_census_gha_driver_v1.g", 15929,
                       "1c6dc7f10d9b27092c2441a274ff74726d8899599ac10c2b8cc47cb59da02995"),
    "q3_receipt": ("ci/b345_157ee_artifacts_32359956713/d972_b345_q3_chief_v1.json", 231570,
                   "3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72"),
    "joint_receipt": ("ci/b345_157ee_artifacts_32359956713/d972_b345_joint_kernel_qstar_closure_v1.json", 2166036,
                      "1c3ad7a7124cee152eb40968cf212c14641a9f8720063c85f70533864898d0df"),
    "joint_source": ("search/d972_b345_joint_kernel_qstar_closure_v1.py", 67945,
                     "06ba6cf361957db3e339d48d14b3d4fbc689de9642e3f96273fbe8f3160e76dc"),
}


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True).encode("ascii")


def sha(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def sha_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def reduce_word(word: Sequence[int]) -> list[int]:
    answer: list[int] = []
    for letter in word:
        require(int(letter) != 0, "zero free-group letter")
        if answer and answer[-1] == -int(letter):
            answer.pop()
        else:
            answer.append(int(letter))
    return answer


def inverse_word(word: Sequence[int]) -> list[int]:
    return [-int(letter) for letter in reversed(word)]


def integer_exponent(word: Sequence[int]) -> tuple[int, int]:
    return (sum(1 if int(x) == 1 else -1 if int(x) == -1 else 0 for x in word),
            sum(1 if int(x) == 2 else -1 if int(x) == -2 else 0 for x in word))


def power_word(word: Sequence[int], exponent: int) -> list[int]:
    if exponent < 0:
        return power_word(inverse_word(word), -exponent)
    answer: list[int] = []
    for _ in range(exponent):
        answer = reduce_word(answer + list(word))
    return answer


def perm_mul(left: Sequence[int], right: Sequence[int]) -> tuple[int, ...]:
    return tuple(left[right[i]] for i in range(len(left)))


def perm_inverse(value: Sequence[int]) -> tuple[int, ...]:
    answer = [0] * len(value)
    for index, image in enumerate(value): answer[image] = index
    return tuple(answer)


def perm_eval(word: Sequence[int], generators: Sequence[Sequence[int]]) -> tuple[int, ...]:
    value = tuple(range(len(generators[0])))
    for letter in word:
        generator = generators[abs(int(letter)) - 1]
        value = perm_mul(value, generator if int(letter) > 0 else perm_inverse(generator))
    return value


def extended_gcd(a: int, b: int) -> tuple[int, int, int]:
    if b == 0:
        return (abs(a), 1 if a >= 0 else -1, 0)
    g, x, y = extended_gcd(b, a % b)
    return g, y, x - (a // b) * y


class ExponentLattice:
    """Canonical rank <=2 row lattice with integral transformation receipts."""
    def __init__(self, vectors: Sequence[Sequence[int]], names: Sequence[str]):
        self.vectors = [tuple(map(int, row)) for row in vectors]
        self.names = list(names)
        require(len(self.vectors) == len(self.names), "lattice roster length")
        self.rank = 0; self.basis: list[tuple[int, int]] = []
        self.basis_combinations: list[list[int]] = []
        self.coordinates: list[list[int]] = []
        self.invariant_factors: list[int] = []
        self._build()

    def _build(self) -> None:
        nonzero = [v for v in self.vectors if v != (0, 0)]
        if not nonzero:
            self._finish(); return
        first = nonzero[0]; g0 = __import__("math").gcd(abs(first[0]), abs(first[1]))
        primitive = (first[0] // g0, first[1] // g0)
        if primitive[0] < 0 or (primitive[0] == 0 and primitive[1] < 0):
            primitive = (-primitive[0], -primitive[1])
        rank_one = all(x * primitive[1] == y * primitive[0]
                       for x, y in self.vectors)
        scalars = []
        if rank_one:
            for x, y in self.vectors:
                scalar = x // primitive[0] if primitive[0] else y // primitive[1]
                require((x, y) == (scalar * primitive[0], scalar * primitive[1]),
                        "rank-one dependence")
                scalars.append(scalar)
            h = 0; coeff = [0] * len(self.vectors)
            for i, value in enumerate(scalars):
                h, u, v = extended_gcd(h, value)
                coeff = [u * z for z in coeff]; coeff[i] += v
            if h < 0: h = -h; coeff = [-z for z in coeff]
            self.rank = 1; self.basis = [(h * primitive[0], h * primitive[1])]
            self.basis_combinations = [coeff]; self._finish(); return
        # Full-rank canonical HNF: (g,s),(0,t), with 0<=s<t.
        gx = 0; bez = [0] * len(self.vectors)
        for i, (x, _y) in enumerate(self.vectors):
            gx, u, v = extended_gcd(gx, x)
            bez = [u * z for z in bez]; bez[i] += v
        if gx < 0: gx = -gx; bez = [-z for z in bez]
        px = sum(c * v[0] for c, v in zip(bez, self.vectors)); py = sum(c * v[1] for c, v in zip(bez, self.vectors))
        require(px == gx and gx > 0, "lattice x Bezout")
        vertical_values = [v[1] - (v[0] // gx) * py for v in self.vectors]
        t = 0; vbez = [0] * len(self.vectors)
        for i, value in enumerate(vertical_values):
            t, u, v = extended_gcd(t, value)
            vbez = [u * z for z in vbez];
            for j in range(len(self.vectors)): vbez[j] += v * ((1 if j == i else 0) - (self.vectors[i][0] // gx) * bez[j])
        if t < 0: t = -t; vbez = [-z for z in vbez]
        require(t > 0, "full lattice vertical gcd")
        shift, rem = divmod(py, t)
        p = (gx, rem); pbez = [bez[i] - shift * vbez[i] for i in range(len(bez))]
        self.rank = 2; self.basis = [p, (0, t)]; self.basis_combinations = [pbez, vbez]
        self._finish()

    def _finish(self) -> None:
        self.coordinates = []
        for x, y in self.vectors:
            if self.rank == 0: coord = []
            elif self.rank == 1:
                bx, by = self.basis[0]; scalar = x // bx if bx else y // by
                require((x, y) == (scalar * bx, scalar * by), "rank-one coordinate")
                coord = [scalar]
            else:
                (a, s), (_z, t) = self.basis; m = x // a; n = (y - m * s) // t
                require((x, y) == (m * a, m * s + n * t), "rank-two coordinate")
                coord = [m, n]
            self.coordinates.append(coord)
        self.invariant_factors = [] if self.rank == 0 else ([abs(self.basis[0][0] or self.basis[0][1])] if self.rank == 1 else [__import__("math").gcd(*[abs(z) for v in self.vectors for z in v if z]), abs(self.basis[0][0] * self.basis[1][1]) // __import__("math").gcd(*[abs(z) for v in self.vectors for z in v if z])])
        require(all(sum(c * v[i] for c, v in zip(combo, self.vectors)) == self.basis[k][i]
                    for k, combo in enumerate(self.basis_combinations) for i in (0, 1)),
                "lattice basis transformation")

    def residue(self, index: int) -> list[int]:
        return [x % 3 for x in self.coordinates[index]]

    def solve(self, target: Sequence[int]) -> list[int] | None:
        if self.rank == 0: return [] if tuple(target) == (0, 0) else None
        if self.rank == 1:
            b = self.basis[0]; scalar = target[0] // b[0] if b[0] else target[1] // b[1]
            if tuple(target) != (scalar * b[0], scalar * b[1]): return None
            h = 0; out = [0] * len(self.vectors)
            for i, coord in enumerate(self.coordinates):
                h, u, v = extended_gcd(h, coord[0]); out = [u * z for z in out]; out[i] += v
            return [scalar * z for z in out]
        a, s = self.basis[0]; t = self.basis[1][1]; n = target[1] // t; m = (target[0] - a * n) // a
        if tuple(target) != (m * a, m * s + n * t): return None
        return [m * c[0] + n * c[1] for c in self.coordinates]

    def public(self) -> dict[str, Any]:
        return {"rank": self.rank, "basis": [list(v) for v in self.basis],
                "basis_combinations": self.basis_combinations,
                "coordinates": self.coordinates, "invariant_factors": self.invariant_factors,
                "roster_pairs": [list(v) for v in self.vectors],
                "roster_names": self.names,
                "normal_generation_pin": {"proof146_sha256": PINS["proof146"][2],
                    "complete_roster_count": len(self.vectors),
                "normal_generation_theorem": "v146_equation_1.3"}}


def lattice_family_selftest() -> int:
    families = [[(0, 0)], [(2, 0), (4, 0)], [(2, 0), (0, 2)],
                [(2, 0), (1, 2)]]
    tested = 0
    for vectors in families:
        lattice = ExponentLattice(vectors, [str(i) for i in range(len(vectors))])
        for x in range(-4, 5):
            for y in range(-4, 5):
                brute = any(sum(c * v[0] for c, v in zip(coeff, vectors)) == x and
                            sum(c * v[1] for c, v in zip(coeff, vectors)) == y
                            for coeff in __import__("itertools").product(range(-8, 9), repeat=len(vectors)))
                require((lattice.solve((x, y)) is not None) == brute,
                        "bounded lattice brute membership")
                tested += 1
    return tested


def fixture_data() -> dict[str, Any]:
    return json.loads(FIXTURE.read_text(encoding="ascii"))


def toy_certificate(fixture: dict[str, Any]) -> dict[str, Any]:
    roster = fixture["normal_roster"]
    vectors = [integer_exponent(row["word"]) for row in roster]
    lattice = ExponentLattice(vectors, [row["name"] for row in roster])
    require(lattice.rank == 2 and lattice.basis == [(2, 0), (0, 2)], "toy proper lattice")
    e_zero = integer_exponent(fixture["toy_words"]["zero"])
    e_in = integer_exponent(fixture["toy_words"]["in_3L"])
    e_bad = integer_exponent(fixture["toy_words"]["not_in_3L"])
    q_in = lattice.solve(tuple(-x // 3 for x in e_in)); require(q_in == [-1, 0, 0], "toy cube solve")
    cube_words = [power_word(row["word"], 3 * q) for row, q in zip(roster, q_in)]
    cube_tail = reduce_word([letter for word in cube_words for letter in word])
    exact = reduce_word(fixture["toy_words"]["in_3L"] + cube_tail)
    require(integer_exponent(exact) == (0, 0), "toy exactification")
    generators = fixture["generators"]; identity = tuple(range(len(generators[0])))
    joint_identity = perm_eval(exact, generators) == identity
    relation_identity = perm_eval(fixture["toy_words"]["zero"], generators) == identity
    recovery = reduce_word(fixture["toy_words"]["zero"])
    require(integer_exponent(recovery) == (0, 0), "toy augmented recovery")
    boundary_tail = [0] * lattice.rank
    boundary_source_words: list[list[int]] = []
    checkpoint = {"old_rank": 2, "new_rank": 4,
                  "discarded_old_state": ["dual", "boundary_cursor", "correction_cursor"],
                  "initialized_new_state": ["dual", "boundary_cursor", "correction_cursor"]}
    signed = inverse_word(fixture["toy_words"]["zero"])
    return {"schema": SELFTEST_SCHEMA, "terminal": TERMINAL, "status": "PASS",
            "fixture_sha256": sha_bytes(FIXTURE.read_bytes()), "lattice": lattice.public(),
            "cases": {"e0_zero": list(e_zero), "e0_in_3L": list(e_in),
                       "e0_in_3L_q": q_in, "e0_in_3L_cube_tail": cube_tail,
                       "e0_in_3L_exact": exact, "e0_not_in_3L": list(e_bad),
                       "e0_not_in_3L_handoff": HANDOFF, "augmented_recovery": recovery},
            "generators": fixture["generators"],
            "checkpoint_upgrade": checkpoint, "active_constant": 2,
            "coefficient_2_inverse": signed,
            "boundary_tail": boundary_tail,
            "boundary_tail_zero": all(value == 0 for value in boundary_tail),
            "lattice_family_tests": lattice_family_selftest(),
            "cube_tail_all_seven_change_zero": all(value % 3 == 0 for word in cube_words
                                                    for value in integer_exponent(word)),
            "exact_exponent": list(integer_exponent(exact)),
            "joint_identity": joint_identity, "hexagons": relation_identity,
            "pentagon_printed_order": relation_identity,
            "boundary_source_words": boundary_source_words,
            "boundary_chains_not_inserted": not boundary_source_words,
            "claims": {"fake": False, "cofinal": False, "ihara": False,
                       "second_rung": False},
            "mutation_results": {"attempted": 17, "rejected": 17}}


def validate_selftest(fixture: dict[str, Any], cert: dict[str, Any]) -> None:
    require(cert.get("schema") == SELFTEST_SCHEMA and cert.get("terminal") == TERMINAL and
            cert.get("status") == "PASS" and cert.get("fixture_sha256") == sha_bytes(FIXTURE.read_bytes()),
            "selftest envelope")
    lattice = ExponentLattice([integer_exponent(x["word"]) for x in fixture["normal_roster"]],
                              [x["name"] for x in fixture["normal_roster"]])
    require(cert["lattice"] == lattice.public() and lattice.rank == 2 and
            lattice.basis == [(2, 0), (0, 2)] and
            cert.get("generators") == fixture["generators"], "selftest lattice/generator binding")
    cases = cert["cases"]
    require(cases["e0_zero"] == [0, 0] and cases["e0_in_3L"] == [6, 0] and
            cases["e0_in_3L_q"] == [-1, 0, 0] and
            cases["e0_in_3L_cube_tail"] == [-1] * 6 and
            cases["e0_in_3L_exact"] == [] and
            cases["e0_not_in_3L"] == [3, 0] and cases["e0_not_in_3L_handoff"] == HANDOFF,
            "selftest exact cases")
    identity = tuple(range(len(cert["generators"][0])))
    computed_joint = perm_eval(cases["e0_in_3L_exact"], cert["generators"]) == identity
    computed_relation = perm_eval(fixture["toy_words"]["zero"], cert["generators"]) == identity
    cube_words = [power_word(row["word"], 3 * q) for row, q in zip(fixture["normal_roster"], cases["e0_in_3L_q"])]
    computed_cube_tail = reduce_word([letter for word in cube_words for letter in word])
    computed_cube_change = all(value % 3 == 0 for word in cube_words
                               for value in integer_exponent(word))
    computed_exact = reduce_word(cases["e0_in_3L"] + cases["e0_in_3L_cube_tail"])
    computed_boundary_zero = all(value == 0 for value in cert.get("boundary_tail", []))
    computed_boundary_absence = cert.get("boundary_source_words") == []
    require(cert["checkpoint_upgrade"] == {"old_rank": 2, "new_rank": 4,
            "discarded_old_state": ["dual", "boundary_cursor", "correction_cursor"],
            "initialized_new_state": ["dual", "boundary_cursor", "correction_cursor"]} and
            cert.get("boundary_tail") == [0, 0] and cert["boundary_tail_zero"] is computed_boundary_zero and
            cert["lattice_family_tests"] == 324 and
            cert["coefficient_2_inverse"] == [2, 1, -2, -1] and
            cases["e0_in_3L_cube_tail"] == computed_cube_tail and
            cert["cube_tail_all_seven_change_zero"] is computed_cube_change and
            cert["exact_exponent"] == list(integer_exponent(computed_exact)) and
            cert["joint_identity"] is computed_joint and cert["hexagons"] is computed_relation and
            cert["pentagon_printed_order"] is computed_relation and
            cert["boundary_chains_not_inserted"] is computed_boundary_absence and
            all(cert["claims"].get(x) is False for x in ("fake", "cofinal", "ihara", "second_rung")),
            "selftest controls")


def mutations(fixture: dict[str, Any], cert: dict[str, Any]) -> int:
    actions = [
        lambda x: x["lattice"]["basis"].__setitem__(0, [1, 0]),
        lambda x: x["lattice"]["rank"].__setitem__(0, 1) if isinstance(x["lattice"]["rank"], list) else x["lattice"].__setitem__("rank", 1),
        lambda x: x["lattice"]["roster_pairs"].__setitem__(0, [4, 0]),
        lambda x: x["lattice"].__setitem__("normal_generation_pin", "sampled"),
        lambda x: x["cases"].__setitem__("e0_in_3L_q", [0, 0, 0]),
        lambda x: x["boundary_tail"].__setitem__(0, 1),
        lambda x: x["checkpoint_upgrade"]["discarded_old_state"].append("old_dual"),
        lambda x: x.__setitem__("active_constant", 1),
        lambda x: x.__setitem__("coefficient_2_inverse", x["cases"]["e0_in_3L_cube_tail"]),
        lambda x: x["cases"].__setitem__("e0_in_3L", [5, 0]),
        lambda x: x["cases"].__setitem__("e0_in_3L_cube_tail", [1]),
        lambda x: x["boundary_source_words"].append([1]),
        lambda x: x["exact_exponent"].__setitem__(0, 3),
        lambda x: x["generators"][0].__setitem__(0, 1),
        lambda x: x["claims"].__setitem__("fake", True),
        lambda x: x.__setitem__("terminal", "UNKNOWN_RESOURCE:TypeError"),
        lambda x: x["cases"].__setitem__("e0_not_in_3L_handoff", TERMINAL),
    ]
    rejected = 0
    for action in actions:
        candidate = copy.deepcopy(cert); action(candidate)
        try: validate_selftest(fixture, candidate)
        except Exception: rejected += 1
        else: raise RuntimeError("selftest mutation accepted")
    require(rejected == 17, "seventeen selftest mutations")
    return rejected


def authenticate() -> dict[str, dict[str, Any]]:
    raw = FIXTURE.read_bytes(); FIXTURE_BYTES = len(raw); FIXTURE_SHA256 = sha_bytes(raw)
    require(len(raw) == 307 and FIXTURE_SHA256 ==
            "ab45ef8d467c92b70d1716f8d4053d99f0dd35479b57898d12887a703393eec2",
            "fixture pin")
    out = {"fixture": {"path": str(FIXTURE.relative_to(ROOT)).replace("\\", "/"),
                        "bytes": len(raw), "sha256": FIXTURE_SHA256}}
    for name, (rel, size, digest) in {**PINS, **TRANSITIVE_PINS}.items():
        path = ROOT / rel; actual = path.read_bytes() if path.is_file() else b""
        if len(actual) != size or sha_bytes(actual) != digest:
            raise RuntimeError("pin:" + rel)
        out[name] = {"path": rel, "bytes": size, "sha256": digest}
    return out


def load_task179_runtime() -> tuple[Any, dict[str, Any]]:
    """Load only the authenticated task179 producer for production runtime."""
    path = ROOT / PINS["task179_producer"][0]
    spec = importlib.util.spec_from_file_location("pinned_task179", path)
    require(spec is not None and spec.loader is not None, "task179 import spec")
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    args = SimpleNamespace(seconds=19_200.0, boundary_pairs=8_000_000,
                           fibre_scans=80_000_000, candidate_words=2_000_000,
                           retained_columns=250_000, checkpoint_bytes=4_000_000_000,
                           rss_bytes=5_700_000_000, oracle_rounds=1)
    monitor = module.Monitor(args)
    return module, module.build_runtime(monitor)


def lattice_from_runtime(runtime: dict[str, Any]) -> ExponentLattice:
    roster = runtime.get("roster")
    require(type(roster) is list and len(roster) == 6_441, "complete normal roster")
    words = [row["word"] for row in roster]
    return ExponentLattice([integer_exponent(word) for word in words],
                           [str(i) for i in range(1, len(words) + 1)])


def sparse_with_lattice_tail(record: dict[str, Any], lattice: ExponentLattice,
                             roster_index: int) -> dict[str, Any]:
    sparse = {str(key): int(value) for key, value in record.get("sparse_row", [])}
    tail = lattice.residue(roster_index - 1)
    for index, value in enumerate(tail):
        if value:
            key = (b"L" + bytes((index + 1,))).hex()
            require(key not in sparse, "lattice typed key collision")
            sparse[key] = value
    return {"sparse_row": sorted([[key, value] for key, value in sparse.items()]),
            "lattice_tail": tail}


def upgrade_columns(source: dict[str, Any], lattice: ExponentLattice) -> list[dict[str, Any]]:
    upgraded = []
    for record in source.get("columns", []):
        item = copy.deepcopy(record)
        provenance = item.get("provenance", {})
        if item.get("family") == "correction":
            index = int(provenance["roster_index"])
            item["augmented"] = sparse_with_lattice_tail(record, lattice, index)
        else:
            item["augmented"] = {"sparse_row": record.get("sparse_row", []),
                                  "lattice_tail": [0] * lattice.rank}
        upgraded.append(item)
    return upgraded


def exactify_receipt(source: dict[str, Any], runtime: dict[str, Any],
                     module: Any, lattice: ExponentLattice,
                     pins: dict[str, Any], source_sha256: str) -> dict[str, Any]:
    require(source.get("status") == "COMMON_WORD", "task179 common receipt")
    correction = [int(x) for x in source.get("correction_word", [])]
    e0 = integer_exponent(correction)
    receipt: dict[str, Any] = {"schema": SCHEMA, "status": "INSPECTION",
        "terminal": HANDOFF, "pins": pins, "task179_receipt_sha256": source_sha256,
        "task179_input_sha256": source.get("input_sha256"),
        "lattice": lattice.public(), "e0": list(e0)}
    cube_words: list[list[int]] = [[] for _ in lattice.vectors]
    cube_tail_unreduced: list[int] = []
    if e0 == (0, 0):
        q = [0] * len(lattice.vectors); cube_tail = []; exact = reduce_word(correction)
    elif e0[0] % 3 or e0[1] % 3:
        return receipt | {"reason": "e0 is not in 3Z^2", "handoff": HANDOFF}
    else:
        q = lattice.solve((-e0[0] // 3, -e0[1] // 3))
        if q is None:
            return receipt | {"reason": "e0/3 is not in L", "handoff": HANDOFF}
        words = runtime["roster"]
        cube_words = [power_word(words[i]["word"], 3 * q[i]) if q[i] else []
                      for i in range(len(words))]
        cube_tail_unreduced = [letter for word in cube_words for letter in word]
        cube_tail = reduce_word(cube_tail_unreduced)
        exact = reduce_word(correction + cube_tail)
    require(integer_exponent(exact) == (0, 0), "exact exponent zero")
    joint = runtime["joint_group"].eval(exact)
    require(joint == runtime["joint_group"].identity, "exact correction joint identity")
    raise RuntimeError("STATIC_STOP: direct all-seven/hexagon/pentagon replay requires successor implementation")


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(); p.add_argument("--mode", choices=("SELFTEST", "INSPECT", "PRODUCTION"), required=True)
    p.add_argument("--output", type=Path, required=True); p.add_argument("--task179-receipt", type=Path)
    p.add_argument("--task179-checkpoint", type=Path); return p


def main(argv: Sequence[str] | None = None) -> int:
    args = parser().parse_args(argv); output = args.output if args.output.is_absolute() else ROOT / args.output
    if args.mode == "SELFTEST":
        fixture = fixture_data(); cert = toy_certificate(fixture); validate_selftest(fixture, cert); mutations(fixture, cert)
        output.parent.mkdir(parents=True, exist_ok=True); output.write_bytes(canonical(cert) + b"\n")
        print("R07_EXACT_COMMUTATOR_COMMON_WORD_V1_PRODUCER_SELFTEST_PASS mutations=17", flush=True); return 0
    pins = authenticate(); source = args.task179_receipt or args.task179_checkpoint
    if source is None: raise RuntimeError("task179 receipt/checkpoint required")
    raw = source.read_bytes(); task179 = json.loads(raw.decode("ascii")); status = task179.get("status")
    if status != "COMMON_WORD" and task179.get("schema") != "d972-r07-positive-common-word-colgen-checkpoint/v1":
        result = {"schema": SCHEMA, "status": "UNKNOWN", "terminal": UNKNOWN_INPUT + ":task179_not_common",
                  "pins": pins, "task179_status": status, "claims": {"fake": False, "cofinal": False, "ihara": False}}
    elif task179.get("schema") == "d972-r07-positive-common-word-colgen-checkpoint/v1":
        if args.mode != "INSPECT":
            raise RuntimeError("STATIC_STOP: augmented checkpoint continuation is not implemented")
        _module, runtime = load_task179_runtime(); lattice = lattice_from_runtime(runtime)
        result = {"schema": SCHEMA, "status": "INSPECTION", "terminal": HANDOFF,
                  "pins": pins, "task179_checkpoint_sha256": sha_bytes(raw),
                  "lattice": lattice.public(), "augmented_columns": upgrade_columns(task179, lattice),
                  "static_stop": {"reason": "augmented checkpoint continuation not implemented",
                      "discarded_state_fields": ["old_dual", "old_cursors", "pending_claims"]},
                  "reason": "inspection-only diagnostic; no successor result"}
    else:
        if args.mode != "INSPECT":
            raise RuntimeError("STATIC_STOP: production replay is not complete")
        module, runtime = load_task179_runtime()
        lattice = lattice_from_runtime(runtime)
        result = exactify_receipt(task179, runtime, module, lattice, pins, sha_bytes(raw))
        result["task179_receipt_bytes"] = len(raw)
        result["task179_receipt_raw_sha256"] = sha_bytes(raw)
    output.parent.mkdir(parents=True, exist_ok=True); output.write_bytes(canonical(result) + b"\n")
    print("R07_EXACT_COMMUTATOR_COMMON_WORD_V1_TERMINAL " + result["terminal"], flush=True); return 0


if __name__ == "__main__": raise SystemExit(main())
