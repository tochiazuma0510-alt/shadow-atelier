"""Helper-nonshared checker for the v146 exact-commutator successor."""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
from pathlib import Path
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "d972-r07-exact-commutator-common-word/v1"
SELFTEST_SCHEMA = "d972-r07-exact-commutator-common-word-selftest-output/v1"
FIXTURE = ROOT / "search/certs/d972_r07_exact_commutator_common_word_selftest_v1_20260827.json"
FIXTURE_BYTES = 307
FIXTURE_SHA256 = "ab45ef8d467c92b70d1716f8d4053d99f0dd35479b57898d12887a703393eec2"
TERMINAL = "R07_EXACT_COMMUTATOR_COMMON_WORD"
HANDOFF = "LATTICE_AUGMENTED_RESUME_REQUIRED"
PINS = {
    "proof145": ("sol/proof_r07_task179_relative_frattini_successor_v145.md", 13819, "b08f140838b78424cafa9528eafbcab9442f94cf92ce2cb42e15fc88ed489a51"),
    "proof146": ("sol/proof_r07_exact_commutator_positive_common_word_v146.md", 9065, "a167df351d55e82781cb60cd2b4dbfdf5cd2ea4f50251643a6e0b83332557cee"),
    "task179_producer": ("search/d972_r07_positive_common_word_colgen_v1.py", 119396, "448123e3ccba4324f4d19a09eeb6a2ba217d611ef5053d4cfa27e61ac69a2512"),
    "task179_checker": ("crosscheck/check_d972_r07_positive_common_word_colgen_v1.py", 70020, "473bad89f9656dd67f4313398b5bdbb253a3495e1e20855d90781b4875309f2d"),
    "task179_driver": ("search/d972_r07_positive_common_word_colgen_gha_driver_v1.g", 12872, "fbab67e85de604f157f8bd93f53d64e7265121508aa948c1e01341e78d1b5a11"),
    "task175_producer": ("search/d972_r07_all_seven_raw_bridge_preflight_v1.py", 60306, "1e0a65f5182157bb928638c2c9a71d475b3b788a6694ee4ded09f5a0ffd38cfa"),
    "task175_checker": ("crosscheck/check_d972_r07_all_seven_raw_bridge_preflight_v1.py", 85848, "c55ec99a9a920cd5d0ef92db7d5f2ad841dda7b0f1dcc59a5dc45e469ed6f7cc"),
    "task175_driver": ("search/d972_r07_all_seven_raw_bridge_preflight_gha_driver_v1.g", 21580, "dbe147f98774fde50dee86de7306f9e18243ac1becef0ec7516765bcb2e08765"),
    "task176_producer": ("search/d972_r07_all_seven_extension_section_census_v1.py", 66109, "878cf1d8d44e74a993309ed1c613c9fc57eb62fd2da48a30fd8797ff4b19af3b"),
    "task176_checker": ("crosscheck/check_d972_r07_all_seven_extension_section_census_v1.py", 84980, "4e6b97aa315fdccb4250de21e99dd78302477b90fd420215de6c6bea7d1fa695"),
    "task176_driver": ("search/d972_r07_all_seven_extension_section_census_gha_driver_v1.g", 15929, "1c6dc7f10d9b27092c2441a274ff74726d8899599ac10c2b8cc47cb59da02995"),
    "q3_receipt": ("ci/b345_157ee_artifacts_32359956713/d972_b345_q3_chief_v1.json", 231570, "3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72"),
    "joint_receipt": ("ci/b345_157ee_artifacts_32359956713/d972_b345_joint_kernel_qstar_closure_v1.json", 2166036, "1c3ad7a7124cee152eb40968cf212c14641a9f8720063c85f70533864898d0df"),
    "joint_source": ("search/d972_b345_joint_kernel_qstar_closure_v1.py", 67945, "06ba6cf361957db3e339d48d14b3d4fbc689de9642e3f96273fbe8f3160e76dc"),
}


def canonical(x: Any) -> bytes:
    return json.dumps(x, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("ascii")


def digest(x: Any) -> str: return hashlib.sha256(canonical(x)).hexdigest()
def file_digest(path: Path) -> str: return hashlib.sha256(path.read_bytes()).hexdigest()
def need(ok: bool, message: str) -> None:
    if not ok: raise RuntimeError(message)


def egcd(a: int, b: int) -> tuple[int, int, int]:
    if b == 0: return abs(a), (1 if a >= 0 else -1), 0
    g, x, y = egcd(b, a % b); return g, y, x - (a // b) * y


class CheckerLattice:
    """Independent HNF/SNF data path; no producer import or helper reuse."""
    def __init__(self, vectors: list[tuple[int, int]], names: list[str]):
        self.vectors, self.names = vectors, names; self.rank = 0
        self.basis: list[tuple[int, int]] = []; self.combos: list[list[int]] = []
        self.coords: list[list[int]] = []; self.invariants: list[int] = []
        self.build()

    def build(self) -> None:
        import math
        nz = [v for v in self.vectors if v != (0, 0)]
        if not nz: self.finish(); return
        g0 = math.gcd(abs(nz[0][0]), abs(nz[0][1])); p = (nz[0][0] // g0, nz[0][1] // g0)
        if p[0] < 0 or (p[0] == 0 and p[1] < 0): p = (-p[0], -p[1])
        if all(x * p[1] == y * p[0] for x, y in self.vectors):
            scalars = [(x // p[0] if p[0] else y // p[1]) for x, y in self.vectors]
            h = 0; combo = [0] * len(self.vectors)
            for i, z in enumerate(scalars):
                h, u, v = egcd(h, z); combo = [u * q for q in combo]; combo[i] += v
            if h < 0: h = -h; combo = [-q for q in combo]
            self.rank, self.basis, self.combos = 1, [(h * p[0], h * p[1])], [combo]
            self.finish(); return
        gx = 0; bx = [0] * len(self.vectors)
        for i, (x, _y) in enumerate(self.vectors):
            gx, u, v = egcd(gx, x); bx = [u * q for q in bx]; bx[i] += v
        if gx < 0: gx = -gx; bx = [-q for q in bx]
        py = sum(q * v[1] for q, v in zip(bx, self.vectors)); vals = [v[1] - (v[0] // gx) * py for v in self.vectors]
        t = 0; by = [0] * len(self.vectors)
        for i, z in enumerate(vals):
            t, u, v = egcd(t, z); by = [u * q for q in by]
            wi = [(1 if j == i else 0) - (self.vectors[i][0] // gx) * bx[j] for j in range(len(self.vectors))]
            by = [q + v * w for q, w in zip(by, wi)]
        if t < 0: t = -t; by = [-q for q in by]
        shift, rem = divmod(py, t); p2 = (gx, rem); bx2 = [q - shift * z for q, z in zip(bx, by)]
        self.rank, self.basis, self.combos = 2, [p2, (0, t)], [bx2, by]; self.finish()

    def finish(self) -> None:
        import math
        for x, y in self.vectors:
            if self.rank == 0: c = []
            elif self.rank == 1:
                a, b = self.basis[0]; q = x // a if a else y // b; need((x, y) == (q * a, q * b), "checker rank1 coordinate"); c = [q]
            else:
                a, s = self.basis[0]; t = self.basis[1][1]; m = x // a; n = (y - m * s) // t
                need((x, y) == (m * a, m * s + n * t), "checker rank2 coordinate"); c = [m, n]
            self.coords.append(c)
        vals = [abs(z) for v in self.vectors for z in v if z]
        self.invariants = [] if self.rank == 0 else ([abs(self.basis[0][0] or self.basis[0][1])] if self.rank == 1 else [math.gcd(*vals), abs(self.basis[0][0] * self.basis[1][1]) // math.gcd(*vals)])
        for k, combo in enumerate(self.combos):
            need(tuple(sum(q * v[i] for q, v in zip(combo, self.vectors)) for i in (0, 1)) == self.basis[k], "checker basis combination")

    def solve(self, target: tuple[int, int]) -> list[int] | None:
        if self.rank == 0: return [] if target == (0, 0) else None
        if self.rank == 1:
            a, b = self.basis[0]; q = target[0] // a if a else target[1] // b
            if target != (q * a, q * b): return None
            return [q * combo[0] for combo in self.combos[0]]
        a, s = self.basis[0]; t = self.basis[1][1]; m = target[0] // a; n = (target[1] - m * s) // t
        if target != (m * a, m * s + n * t): return None
        return [m * c[0] + n * c[1] for c in self.coords]

    def public(self) -> dict[str, Any]:
        return {"rank": self.rank, "basis": [list(v) for v in self.basis], "basis_combinations": self.combos,
                "coordinates": self.coords, "invariant_factors": self.invariants,
                "roster_pairs": [list(v) for v in self.vectors], "roster_names": self.names,
                "normal_generation_pin": {"proof146_sha256": PINS["proof146"][2],
                    "complete_roster_count": len(self.vectors),
                "normal_generation_theorem": "v146_equation_1.3"}}


def lattice_family_selftest() -> int:
    families = [[(0, 0)], [(2, 0), (4, 0)], [(2, 0), (0, 2)], [(2, 0), (1, 2)]]
    tested = 0
    import itertools
    for vectors in families:
        lattice = CheckerLattice(vectors, [str(i) for i in range(len(vectors))])
        for x in range(-4, 5):
            for y in range(-4, 5):
                brute = any(sum(c * v[0] for c, v in zip(coeff, vectors)) == x and
                            sum(c * v[1] for c, v in zip(coeff, vectors)) == y
                            for coeff in itertools.product(range(-8, 9), repeat=len(vectors)))
                need((lattice.solve((x, y)) is not None) == brute, "checker lattice brute membership")
                tested += 1
    return tested


def reduce_word(word: list[int]) -> list[int]:
    out: list[int] = []
    for letter in word:
        if out and out[-1] == -letter:
            out.pop()
        else:
            out.append(letter)
    return out


def power_word(word: list[int], power: int) -> list[int]:
    if power < 0:
        word = [-letter for letter in reversed(word)]
        power = -power
    return reduce_word(word * power)


def exponent(word: list[int]) -> list[int]:
    return [sum(1 if x == 1 else -1 if x == -1 else 0 for x in word), sum(1 if x == 2 else -1 if x == -2 else 0 for x in word)]


def pmul(left: list[int] | tuple[int, ...], right: list[int] | tuple[int, ...]) -> tuple[int, ...]:
    return tuple(left[right[i]] for i in range(len(left)))


def pinv(value: list[int] | tuple[int, ...]) -> tuple[int, ...]:
    out = [0] * len(value)
    for i, image in enumerate(value): out[image] = i
    return tuple(out)


def peval(word: list[int], generators: list[list[int]]) -> tuple[int, ...]:
    value = tuple(range(len(generators[0])))
    for letter in word:
        g = generators[abs(letter) - 1]
        value = pmul(value, g if letter > 0 else pinv(g))
    return value


def authenticate_fixture() -> dict[str, Any]:
    raw = FIXTURE.read_bytes(); need(len(raw) == FIXTURE_BYTES and file_digest(FIXTURE) == FIXTURE_SHA256, "checker fixture pin"); return json.loads(raw.decode("ascii"))


def authenticate_pins() -> None:
    for rel, size, expected in PINS.values():
        path = ROOT / rel; need(path.is_file(), "checker missing pin " + rel)
        raw = path.read_bytes(); need(len(raw) == size and hashlib.sha256(raw).hexdigest() == expected, "checker pin drift " + rel)


def validate_selftest(fixture: dict[str, Any], cert: dict[str, Any]) -> None:
    need(cert.get("schema") == SELFTEST_SCHEMA and cert.get("terminal") == TERMINAL and cert.get("status") == "PASS", "checker selftest envelope")
    vectors = [tuple(exponent(x["word"])) for x in fixture["normal_roster"]]
    lattice = CheckerLattice(vectors, [x["name"] for x in fixture["normal_roster"]])
    need(cert.get("fixture_sha256") == file_digest(FIXTURE) and cert.get("lattice") == lattice.public() and cert.get("generators") == fixture["generators"], "checker lattice/generator receipt")
    c = cert.get("cases", {})
    need(c.get("e0_zero") == [0, 0] and c.get("e0_in_3L") == [6, 0] and c.get("e0_in_3L_q") == [-1, 0, 0] and c.get("e0_in_3L_cube_tail") == [-1] * 6 and c.get("e0_in_3L_exact") == [] and c.get("e0_not_in_3L") == [3, 0] and c.get("e0_not_in_3L_handoff") == HANDOFF, "checker cases")
    up = cert.get("checkpoint_upgrade", {})
    need(up == {"old_rank": 2, "new_rank": 4,
               "discarded_old_state": ["dual", "boundary_cursor", "correction_cursor"],
               "initialized_new_state": ["dual", "boundary_cursor", "correction_cursor"]}, "checker checkpoint")
    identity = tuple(range(len(cert["generators"][0])))
    computed_joint = peval(c.get("e0_in_3L_exact"), cert["generators"]) == identity
    computed_relation = peval(fixture["toy_words"]["zero"], cert["generators"]) == identity
    cube_words = [power_word(row["word"], 3 * q) for row, q in zip(fixture["normal_roster"], c["e0_in_3L_q"])]
    computed_cube_tail = reduce_word([letter for word in cube_words for letter in word])
    computed_cube_change = all(value % 3 == 0 for word in cube_words for value in exponent(word))
    computed_exact = reduce_word(c["e0_in_3L"] + c["e0_in_3L_cube_tail"])
    computed_boundary_zero = all(value == 0 for value in cert.get("boundary_tail", []))
    computed_boundary_absence = cert.get("boundary_source_words") == []
    need(cert.get("active_constant") == 2 and cert.get("coefficient_2_inverse") == [2, 1, -2, -1] and cert.get("boundary_tail") == [0, 0] and cert.get("boundary_tail_zero") is computed_boundary_zero and cert.get("lattice_family_tests") == 324 and c["e0_in_3L_cube_tail"] == computed_cube_tail and cert.get("cube_tail_all_seven_change_zero") is computed_cube_change and cert.get("exact_exponent") == list(exponent(computed_exact)) and cert.get("joint_identity") is computed_joint and cert.get("hexagons") is computed_relation and cert.get("pentagon_printed_order") is computed_relation, "checker direct replay")
    need(cert.get("boundary_chains_not_inserted") is computed_boundary_absence, "checker boundary provenance")
    need(all(cert.get("claims", {}).get(x) is False for x in ("fake", "cofinal", "ihara", "second_rung")), "checker claim boundary")


def mutation_suite(fixture: dict[str, Any], cert: dict[str, Any]) -> int:
    actions = [
        lambda x: x["lattice"]["basis"].__setitem__(0, [1, 0]), lambda x: x["lattice"].__setitem__("rank", 1),
        lambda x: x["lattice"]["roster_pairs"].__setitem__(0, [4, 0]), lambda x: x["lattice"].__setitem__("normal_generation_pin", "sampled"),
        lambda x: x["cases"].__setitem__("e0_in_3L_q", [0, 0, 0]), lambda x: x["boundary_tail"].__setitem__(0, 1),
        lambda x: x["checkpoint_upgrade"]["discarded_old_state"].append("old_dual"), lambda x: x.__setitem__("active_constant", 1),
        lambda x: x.__setitem__("coefficient_2_inverse", []), lambda x: x["cases"].__setitem__("e0_in_3L_q", [1, 0, 0]),
        lambda x: x["cases"].__setitem__("e0_in_3L_cube_tail", [1]), lambda x: x.__setitem__("cube_tail_all_seven_change_zero", False),
        lambda x: x["exact_exponent"].__setitem__(0, 3), lambda x: x["boundary_source_words"].append([1]),
        lambda x: x["claims"].__setitem__("fake", True), lambda x: x.__setitem__("terminal", "UNKNOWN_RESOURCE:TypeError"),
        lambda x: x["cases"].__setitem__("e0_not_in_3L_handoff", TERMINAL),
    ]
    rejected = 0
    for action in actions:
        candidate = copy.deepcopy(cert); action(candidate)
        try: validate_selftest(fixture, candidate)
        except Exception: rejected += 1
        else: raise RuntimeError("checker mutation accepted")
    need(rejected == 17, "checker seventeen mutations"); return rejected


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(); p.add_argument("--mode", choices=("SELFTEST", "PRODUCTION"), required=True); p.add_argument("--receipt", type=Path, required=True); p.add_argument("--verdict", type=Path, required=True); a = p.parse_args(argv)
    authenticate_pins()
    receipt = json.loads(a.receipt.read_text(encoding="ascii"))
    if a.mode == "SELFTEST":
        fixture = authenticate_fixture(); validate_selftest(fixture, receipt); mutation_suite(fixture, receipt); marker = "R07_EXACT_COMMUTATOR_COMMON_WORD_V1_CHECKER_SELFTEST_PASS mutations=17"; result = {"status": "PASS", "terminal": TERMINAL, "mutations": 17}
    else:
        # Production replay is deliberately unavailable in this delivery.  In
        # particular, never promote asserted exact_exponent/direct_replay
        # fields from a producer receipt into a checker verdict.
        raise RuntimeError("STATIC_STOP: independent production replay is not implemented")
    a.verdict.parent.mkdir(parents=True, exist_ok=True); a.verdict.write_bytes(canonical(result) + b"\n"); print(marker, flush=True); return 0


if __name__ == "__main__":
    try: raise SystemExit(main())
    except Exception as exc: print("R07_EXACT_COMMUTATOR_COMMON_WORD_V1_CHECKER_STOP " + type(exc).__name__ + ":" + str(exc), file=sys.stderr); raise
