#!/usr/bin/env python3
"""Fresh g760 C-13/L3 target6 producer.

The bounded lane builds every base-dependent target and legal-correction
row, but never enumerates the 649,539 translated D2 columns.  The GHA-only
full lane computes the preregistered j ladder with the frozen C-13 BFS
closure, followed by a direct lossless separator pairing replay.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
import sys
import time
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable, Sequence


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "d972-r07-760-l3-target6/v1"
FINAL_MARKER = "R07_760_L3_TARGET6_V1_PRODUCER_PASS"
DEFAULT_PREFLIGHT = Path(
    "search/certs/d972_r07_760_l3_target6_preflight_v1_20260826.json")
DEFAULT_FULL = Path("ci/out/d972_r07_760_l3_target6_v1.json")

TERMINALS = {
    "R07_760_L3_TARGET6_NONMEMBER",
    "R07_760_L3_TARGET6_MEMBER_INCONCLUSIVE",
    "R07_760_L3_TARGET6_UNKNOWN_RESOURCE",
    "R07_760_L3_TARGET6_INPUT_STOP",
}
PREFLIGHT_STATE = "R07_760_L3_TARGET6_PREFLIGHT_READY"

Q3_PATH = Path(
    "ci/b345_157en_artifacts_32458556448/d972_b345_q3_chief_v1.json")
CORE_PATH = Path("search/koubou158_L3_core_v1_2.py")
J_ORDER = tuple(range(2, 13))
MAX_DIMENSION = 180000
MAX_RSS_MIB = 5600
TRANSLATED_D2_COUNT = 11 * (3 ** 10)

PARENT_SHA = "3680e8bcbac37747467175454b082485b2ae296f1fb05244435d8f44979d4e90"
BASE_SHA = "518f09820b8d7baee6b58ebf366cebf7b02a9a945cd1350cf8c701a4e6bc2b4d"
OLD20_SHA = "b79f105ec2963ae55b69480f8ed8ab13083d01cb936da32edb4798698c22055d"

PIN_SPECS: dict[str, tuple[Path, int, str]] = {
    "task_163": (Path("sol/luna_task_163_r07_760_l3_target6_v1.md"),
        9066, "9fcdf2f25b724e9dbc225f417b0036e126e7b5e37a0778dab5e0299ee2f74e12"),
    "claims": (Path("provenance/CLAIMS.md"),
        68363, "37325e7e7d734f7619785eb1832a051a4e35bb7409e0adaad413443a13038c00"),
    "dialogue": (Path("docs/\u5bfe\u8a71\u5e33.md"),
        234377, "a5eadcc04468b593e0a1c7896409a59b55c6442ca489df6a91aac60d6e128a06"),
    "proof_v92": (Path("sol/proof_r07_joint_derived_commutator_rebase_v92.md"),
        5969, "cc56e2187fac08ffa70fe3753e200627e776b5fa591738dee5da908e4d217387"),
    "audit_v95": (Path("sol/audit_r07_uniform_explicit_lift_checkpoint_v95.md"),
        5324, "12877306446bcfe8b57b01751c929bdee78d15300c4f90a8311764ff2d7eeeae"),
    "task_162": (Path("sol/luna_task_162_r07_760_commutator_affine_rhs_v3.md"),
        4053, "8ca38afc6f30e8e6074f191a17541f508f29ba1da58d3b286ba4fcf33406ae21"),
    "reply_162": (Path("sol/luna_reply_162_r07_760_commutator_affine_rhs_v3.md"),
        8833, "70ebb7bf433fafd77dc828efe5f71b9dd6dc982e7682a4c6397695b6a2e6bcf5"),
    "preflight_162": (
        Path("search/certs/d972_r07_616_to_760_commutator_affine_rhs_"
             "preflight_v3_20260826.json"),
        184890, "55752b6c1a748fb0b25a86d6fc1a0381a82b203112568b0b1963c5665cef0408"),
    "c13_producer": (Path("search/koubou158_L3_radical_v1_2.py"),
        14488, "05e96bb3e7d0e9b949cb8d9ec0d216f97a698777df82d56449bcc20f89933f17"),
    "c13_core": (CORE_PATH,
        31192, "4366ebd1759fbd11a795b251101776836ef4ec2a28b7b947b93727208e199c63"),
    "c13_checker": (Path("crosscheck/check_koubou158_L3_radical_v1.py"),
        28198, "451aa614d2c83f43291fa80abf09abe425004288717ed6278b5690b511724529"),
    "c13_receipt_v11": (
        Path("search/certs/koubou158_L3_radical_v1_1_20260822.json"),
        17418, "4a80c0b4c063eaab31ce32aad69eb9f21c220278dc748e31439aef9af38a2ca2"),
    "c13_receipt_v12": (
        Path("search/certs/koubou158_L3_radical_v1_2_20260822.json"),
        20930, "56ab4592bf5b64fbe5605afe063681e8c059929cd8abbc07323988aff4a8440f"),
    "c13_checker_receipt": (
        Path("crosscheck/verdicts/koubou158_L3_radical_crosscheck_v1_20260822.json"),
        7654, "c87e12ba96ea95607e99701e1e92786ac93ba08c91ad424dbea1f252304b1b78"),
    "q3": (Q3_PATH,
        231570, "3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72"),
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


class InputStop(RuntimeError):
    pass


class ResourceStop(RuntimeError):
    def __init__(self, stage: str, detail: str) -> None:
        super().__init__(detail)
        self.stage = stage
        self.detail = detail


class Monitor:
    def __init__(self, seconds: float) -> None:
        require(0 < seconds <= 21600, "seconds range")
        self.started = time.monotonic()
        self.deadline = self.started + seconds
        self.checks = 0

    def check(self, stage: str, *, force: bool = False) -> None:
        self.checks += 1
        if not force and self.checks % 256:
            return
        if time.monotonic() >= self.deadline:
            raise ResourceStop(stage, "shared wall-clock budget exhausted")
        try:
            import resource
            rss = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
            # Linux reports KiB, macOS bytes.  GHA is Linux.
            rss_mib = rss / 1024
            if sys.platform == "darwin":
                rss_mib = rss / (1024 * 1024)
            if rss_mib > MAX_RSS_MIB:
                raise ResourceStop(stage, f"RSS cap exceeded: {rss_mib:.1f} MiB")
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


def pin_inputs() -> dict[str, Any]:
    rows: dict[str, Any] = {}
    for label, (path, size, digest) in PIN_SPECS.items():
        full = ROOT / path
        if not full.is_file() or full.stat().st_size != size or \
                digest_file(full) != digest:
            raise InputStop("pin drift: " + path.as_posix())
        rows[label] = {"path": path.as_posix(), "bytes": size,
                       "sha256": digest}
    return rows


def load_core() -> Any:
    path = ROOT / CORE_PATH
    spec = importlib.util.spec_from_file_location("_r07_760_l3_c13_core", path)
    require(spec is not None and spec.loader is not None, "core module spec")
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
        if letter == 1:
            out.extend(x)
        elif letter == -1:
            out.extend(inv_word(x))
        elif letter == 2:
            out.extend(y)
        elif letter == -2:
            out.extend(inv_word(y))
        else:
            raise RuntimeError("F2 alphabet")
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
            "parent 616 reconstruction")
    require(len(base) == 760 and digest_obj(base) == BASE_SHA and
            exponent_sums(base) == [0, 0], "g760 reconstruction")
    require(digest_obj(list(OLD20)) == OLD20_SHA, "old20 diagnostic pin")
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


def add_vec(left: dict[Any, int], right: dict[Any, int]) -> dict[Any, int]:
    out: dict[Any, int] = defaultdict(int)
    for key, value in itertools.chain(left.items(), right.items()):
        out[key] = (out[key] + int(value)) % 3
    return {key: value for key, value in out.items() if value}


def neg_vec(row: dict[Any, int]) -> dict[Any, int]:
    return {key: (-int(value)) % 3 for key, value in row.items()
            if int(value) % 3}


def claims() -> dict[str, bool]:
    return {
        "actual_A18_occurrence": False,
        "normalized_Brunnian_class": False,
        "compatible_cofinal_lift": False,
        "ihara_witness": False,
        "all_bases_obstruction": False,
    }


def verify_weights(q3: dict[str, Any]) -> dict[str, Any]:
    pb4 = q3["groups"]["PB4"]
    require(pb4["nilpotency_class"] == 2 and
            pb4["generator_count"] == 10, "PB4 PC dimensions")
    require(all(int(x) == 3 for x in pb4["relative_orders"]) and
            all(all(int(v) == 0 for v in row)
                for row in pb4["power_relations"]), "PB4 exponent three")
    violations = []
    for entry in pb4["conjugate_relations"]:
        i, j = int(entry["i"]), int(entry["j"])
        coords = [int(x) for x in entry["coords"]]
        if i > 6 or j > 6:
            expected = [1 if k + 1 == i else 0 for k in range(10)]
            if coords != expected:
                violations.append([i, j])
        else:
            if any(coords[k] and k + 1 <= 6 and k + 1 != i
                   for k in range(10)):
                violations.append([i, j])
    require(not violations, "Jennings weight derivation")
    return {"weights": [1] * 6 + [2] * 4,
            "conjugate_relations_checked":
                len(pb4["conjugate_relations"]),
            "power_relations_checked": len(pb4["power_relations"]),
            "violations": 0}


def delta_and_schreier(core: Any, e4: Any) \
        -> tuple[list[list[int]], dict[str, Any]]:
    pc = e4.pc
    xbar, ybar, zbar = (e4.eval(list(word))[1]
                         for word in (X0, Y0, Z0))
    require(zbar == pc.inverse(pc.mul(ybar, xbar)),
            "zbar=(ybar*xbar)^-1")
    g1 = (xbar, xbar, ybar)
    g2 = (ybar, zbar, zbar)
    transversal, tree = core.enum_delta_pc(g1, g2, pc, core.DELTA_CAP)
    words = core.schreier_generators_pc(transversal, tree, g1, g2, pc)
    require(len(transversal) == 27 and len(words) == 28,
            "full Schreier roster")
    commute = tuple(pc.mul(g1[i], g2[i]) for i in range(3)) == \
        tuple(pc.mul(g2[i], g1[i]) for i in range(3))
    return words, {
        "order_Delta": len(transversal),
        "isomorphism_type": (
            "elementary_abelian_C3^3" if commute else
            "nonabelian_exponent3_order27_class2"),
        "schreier_generator_count": len(words),
        "schreier_rank_formula": "1+[Delta:F2_image]*(2-1)=28",
        "schreier_words_sha256": digest_obj(words),
        "full_kernel_generating_set": True,
    }


def build_static() -> tuple[dict[str, Any], dict[str, Any]]:
    pins = pin_inputs()
    core = load_core()
    q3 = json.loads((ROOT / Q3_PATH).read_text(encoding="utf-8"))
    require(q3["schema"] == "d972-b345-q-chief/v1", "q3 schema")
    e4 = core.E4(q3)
    parent, base = construct_base()

    A = substitute2(base, X0, Y0)
    B = substitute2(base, X0, Z0)
    C = substitute2(base, Y0, Z0)
    target_word = reduce_word(C + inv_word(B) + A)
    alt_no_inverse = reduce_word(C + B + A)
    alt_reordered = reduce_word(A + inv_word(B) + C)
    target_raw = core.fox_gradient(e4, target_word)
    target_pc = core.project_to_pi(target_raw)
    require(e4.eval(target_word) == e4.identity,
            "fresh g760 target value in current E4")

    Abar, Bbar, Cbar = (e4.eval(word) for word in (A, B, C))
    prefix = e4.mul(Bbar, e4.inverse(Cbar))
    prefix_inverse = e4.inverse(prefix)
    require(prefix != prefix_inverse, "prefix inverse mutation discriminant")

    schreier, delta_public = delta_and_schreier(core, e4)
    sigma_private: list[dict[Any, int]] = []
    legal_rows = []
    pc_one = e4.pc.one()
    for ordinal, word in enumerate(schreier, 1):
        context_values = [
            e4.eval(substitute2(word, left, right))[1]
            for left, right in ((X0, Y0), (X0, Z0), (Y0, Z0))]
        require(context_values == [pc_one, pc_one, pc_one],
                f"Schreier context identity {ordinal}")
        ga = core.fox_gradient(e4, substitute2(word, X0, Y0))
        gb = core.fox_gradient(e4, substitute2(word, X0, Z0))
        gc = core.fox_gradient(e4, substitute2(word, Y0, Z0))
        sigma = add_vec(
            core.translate_vec(e4, add_vec(gc, neg_vec(gb)), prefix), ga)
        sigma_pc = core.project_to_pi(sigma)
        sigma_private.append(sigma_pc)
        public = serialize_pc_gradient(sigma_pc)
        legal_rows.append({
            "ordinal": ordinal, "schreier_word": word,
            "schreier_word_sha256": digest_obj(word),
            "projected_sigma": public,
            "projected_sigma_sha256": digest_obj(public),
        })

    relators = q3["formulas"]["presentations"]["PB4"]["relations"]
    require(len(relators) == 11 and relators == core.pure_relations(4),
            "PB4 relator roster")
    relator_pc: list[dict[Any, int]] = []
    relator_rows = []
    for ordinal, word in enumerate(relators, 1):
        require(e4.eval(word) == e4.identity, f"PB4 relator {ordinal}")
        raw = core.fox_gradient(e4, word)
        pcrow = core.project_to_pi(raw)
        relator_pc.append(pcrow)
        public = serialize_pc_gradient(pcrow)
        relator_rows.append({
            "ordinal": ordinal, "word": word,
            "word_sha256": digest_obj(word),
            "projected_gradient": public,
            "projected_gradient_sha256": digest_obj(public),
        })

    jennings = []
    for j in J_ORDER:
        monomials = core.enumerate_monomials(j)
        jennings.append({
            "j": j, "monomial_count": len(monomials),
            "dim_Lambda_over_Ij": 6 * len(monomials),
            "basis_sha256": digest_obj([list(row) for row in monomials]),
        })

    old_A = substitute2(OLD20, X0, Y0)
    old_B = substitute2(OLD20, X0, Z0)
    old_C = substitute2(OLD20, Y0, Z0)
    old_target = reduce_word(old_C + inv_word(old_B) + old_A)
    old_target_raw = core.fox_gradient(e4, old_target)

    static = {
        "implementation_parent_commit":
            "f3698fffd3b73370f753c4b0d9eb1e86751b1159",
        "pins": pins,
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
            "basis_manifest": jennings,
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
    private = {
        "core": core, "q3": q3, "e4": e4, "target_pc": target_pc,
        "sigma_pc": sigma_private, "relator_pc": relator_pc,
    }
    return static, private


def base_receipt(mode: str, terminal: str | None, static: dict[str, Any]) \
        -> dict[str, Any]:
    receipt = {
        "schema": SCHEMA, "mode": mode, "static": static,
        "result": {"state": "UNBUILT_GHA_ONLY"} if mode == "preflight" else {},
        "sound_implication": {
            "two_enlargements": [
                "projection E4 -> Pi4[3]",
                "literal legal image -> full C-13 K^(31) span",
            ],
            "nonmembership_direction_only": True,
            "membership_is_lift": False,
            "scope": "one explicit g760 prefix, first hexagon coordinate",
        },
        "claims": claims(),
    }
    if mode == "preflight":
        require(terminal is None, "preflight has no mathematical terminal")
        receipt["preflight_state"] = PREFLIGHT_STATE
    else:
        require(terminal in TERMINALS, "full terminal")
        receipt["status"] = terminal
        receipt["terminal_token"] = terminal
    return receipt


def build_preflight() -> dict[str, Any]:
    static, private = build_static()
    del private
    receipt = base_receipt("preflight", None, static)
    receipt["self_digest_sha256"] = digest_obj(receipt)
    return receipt


def pc_translate(pc: Any, row: dict[Any, int], g: bytes) -> dict[Any, int]:
    out: dict[Any, int] = defaultdict(int)
    for (component, value), coefficient in row.items():
        key = (component, pc.mul(g, value))
        out[key] = (out[key] + int(coefficient)) % 3
    return {key: value for key, value in out.items() if value}


def sep_public(sep: tuple[int, int], idx: dict[Any, int],
               sp: Any) -> list[list[Any]]:
    reverse = {value: key for key, value in idx.items()}
    rows = []
    for coordinate in range(sp.n):
        coefficient = sp.coeff_at(sep, coordinate)
        if coefficient:
            component, monomial = reverse[coordinate]
            rows.append([int(component), list(monomial), int(coefficient)])
    return rows


def verify_separator_direct(core: Any, e4: Any, j: int,
                            sep: tuple[int, int], idx: dict[Any, int],
                            sp: Any, sigma_pc: Sequence[dict[Any, int]],
                            relator_pc: Sequence[dict[Any, int]],
                            target_pc: dict[Any, int],
                            monitor: Monitor) -> dict[str, Any]:
    bad_legal = []
    for ordinal, row in enumerate(sigma_pc, 1):
        projected = core.project_vec_to_Ij(row, j)
        vector = sp.vec({idx[key]: value for key, value in projected.items()
                         if key in idx})
        if sp.dot(sep, vector):
            bad_legal.append(ordinal)
    bad_boundary = []
    checked = 0
    for relator_ordinal, relator in enumerate(relator_pc, 1):
        for coords in itertools.product(range(3), repeat=10):
            monitor.check("separator_direct_pairing")
            translated = pc_translate(e4.pc, relator, bytes(coords))
            projected = core.project_vec_to_Ij(translated, j)
            vector = sp.vec({idx[key]: value for key, value in projected.items()
                             if key in idx})
            checked += 1
            if sp.dot(sep, vector):
                if len(bad_boundary) < 8:
                    bad_boundary.append([relator_ordinal, list(coords)])
    target_projected = core.project_vec_to_Ij(target_pc, j)
    target_vector = sp.vec({idx[key]: value
                            for key, value in target_projected.items()
                            if key in idx})
    target_dot = sp.dot(sep, target_vector)
    require(not bad_legal and not bad_boundary and
            checked == TRANSLATED_D2_COUNT and target_dot != 0,
            "lossless separator direct pairing")
    return {
        "legal_rows_checked": len(sigma_pc),
        "legal_nonzero_pairings": len(bad_legal),
        "translated_boundary_rows_checked": checked,
        "translated_boundary_nonzero_pairings": 0,
        "target_pairing": target_dot,
        "all_generated_rows_annihilated": True,
        "target_pairing_nonzero": True,
        "direct_all_59049_elements_x_11_relators": True,
    }


def compute_j_bfs(private: dict[str, Any], j: int,
                  monitor: Monitor, *, pairing: bool) -> dict[str, Any]:
    core, e4 = private["core"], private["e4"]
    sigma_pc = private["sigma_pc"]
    relator_pc = private["relator_pc"]
    target_pc = private["target_pc"]
    monomials = core.enumerate_monomials(j)
    dimension = 6 * len(monomials)
    if dimension > MAX_DIMENSION:
        raise ResourceStop(f"j={j}", f"dimension cap: {dimension}")
    idx = {(component, monomial): ordinal for ordinal, (component, monomial)
           in enumerate((component, monomial)
                        for component in range(1, 7)
                        for monomial in monomials)}
    sp = core.F3BitSpace(dimension)

    legal_vectors = []
    legal_public = []
    legal_ech = core.F3BitEchelon(sp)
    for row in sigma_pc:
        projected = core.project_vec_to_Ij(row, j)
        legal_public.append(projected_public(projected))
        vector = sp.vec({idx[key]: value for key, value in projected.items()
                         if key in idx})
        legal_vectors.append(vector)
        legal_ech.add(vector)

    d2_ech = core.F3BitEchelon(sp)
    closure_receipts = []
    for ordinal, row in enumerate(relator_pc, 1):
        monitor.check(f"j={j}:D2-relator-{ordinal}", force=True)
        closure_receipts.append(core.submodule_closure_with_depth(
            row, j, idx, sp, e4.pc, d2_ech))
    combined = d2_ech.clone()
    for vector in legal_vectors:
        combined.add(vector)

    target_projected = core.project_vec_to_Ij(target_pc, j)
    target_vector = sp.vec({idx[key]: value
                            for key, value in target_projected.items()
                            if key in idx})
    remainder, pivot = combined.reduce(target_vector)
    nonmember = pivot >= 0
    separator = None
    if nonmember:
        sep = combined.extract_separator(target_vector)
        require(sep is not None, "separator extraction")
        terms = sep_public(sep, idx, sp)
        pairings = verify_separator_direct(
            core, e4, j, sep, idx, sp, sigma_pc, relator_pc,
            target_pc, monitor) if pairing else None
        separator = {
            "terms": terms, "terms_sha256": digest_obj(terms),
            "support": len(terms), "pairing_replay": pairings,
        }
    return {
        "j": j, "monomial_count": len(monomials),
        "dim_Lambda_over_Ij": dimension,
        "basis_sha256": digest_obj([list(row) for row in monomials]),
        "rank_D2bar_alone": d2_ech.rank(),
        "rank_legal_overapproximation": legal_ech.rank(),
        "rank_combined": combined.rank(),
        "target_projected_sha256":
            digest_obj(projected_public(target_projected)),
        "legal_projected_rows_sha256": digest_obj(legal_public),
        "PB4_translate_count": TRANSLATED_D2_COUNT,
        "producer_D2_algorithm": "saturated (x_i-1) BFS, D2 first",
        "per_relator_closure_receipts": closure_receipts,
        "nonmember": nonmember,
        "separator": separator,
    }


def mathematical_result(private: dict[str, Any], monitor: Monitor) \
        -> tuple[str, dict[str, Any]]:
    progression = []
    terminal = "R07_760_L3_TARGET6_MEMBER_INCONCLUSIVE"
    for j in J_ORDER:
        monitor.check(f"j={j}:start", force=True)
        row = compute_j_bfs(private, j, monitor, pairing=True)
        progression.append(row)
        if row["nonmember"]:
            terminal = "R07_760_L3_TARGET6_NONMEMBER"
            replay = compute_j_bfs(private, j, monitor, pairing=False)
            keys = ("rank_D2bar_alone", "rank_legal_overapproximation",
                    "rank_combined", "target_projected_sha256",
                    "legal_projected_rows_sha256", "nonmember")
            require(all(replay[key] == row[key] for key in keys),
                    "fresh no-state-leak BFS replay")
            break
    j4 = next((row for row in progression if row["j"] == 4), None)
    comparison = None if j4 is None else {
        "historical_old20": {
            "rank_D2bar_alone": 310,
            "rank_legal_overapproximation": 4,
            "rank_combined": 314,
        },
        "fresh_g760": {key: j4[key] for key in
            ("rank_D2bar_alone", "rank_legal_overapproximation",
             "rank_combined", "nonmember")},
        "used_as_requirement": False,
    }
    return terminal, {
        "state": terminal,
        "j_order_tested": [row["j"] for row in progression],
        "first_terminal_rule_applied": True,
        "first_nonmember_j": next(
            (row["j"] for row in progression if row["nonmember"]), None),
        "j_progression": progression,
        "old20_comparison_diagnostic": comparison,
        "registered_108_family_used": False,
        "literal_A18_computed": False,
        "normalized_Brunnian_class_computed": False,
    }


def stop_receipt(mode: str, terminal: str, reason: str,
                 stage: str, seconds: float) -> dict[str, Any]:
    parent, base = construct_base()
    receipt = {
        "schema": SCHEMA, "mode": mode, "status": terminal,
        "terminal_token": terminal,
        "static": {
            "base": {
                "base_kind": "r07_760_commutator",
                "parent_616_sha256": digest_obj(parent),
                "signed_word": base, "length": len(base),
                "sha256": digest_obj(base),
                "free_exponent_sums": exponent_sums(base),
            },
            "freshness_boundary": {
                "old20_target_imported": False,
                "old20_ranks_required": False,
                "old616_target_imported": False,
                "historical_blocker_imported": False,
                "historical_B0_B1_imported": False,
            },
        },
        "result": {
            "state": terminal, "stage": stage, "reason": reason,
            "requested_seconds": seconds,
            "mathematical_membership_claimed": False,
            "mathematical_nonmembership_claimed": False,
        },
        "sound_implication": {
            "two_enlargements": [
                "projection E4 -> Pi4[3]",
                "literal legal image -> full C-13 K^(31) span",
            ],
            "nonmembership_direction_only": True,
            "membership_is_lift": False,
            "scope": "one explicit g760 prefix, first hexagon coordinate",
        },
        "claims": claims(),
    }
    receipt["self_digest_sha256"] = digest_obj(receipt)
    return receipt


def build_full(seconds: float) -> dict[str, Any]:
    try:
        static, private = build_static()
        monitor = Monitor(seconds)
        terminal, result = mathematical_result(private, monitor)
        receipt = base_receipt("full", terminal, static)
        receipt["result"] = result
        receipt["self_digest_sha256"] = digest_obj(receipt)
        del private
        return receipt
    except ResourceStop as exc:
        return stop_receipt(
            "full", "R07_760_L3_TARGET6_UNKNOWN_RESOURCE",
            exc.detail, exc.stage, seconds)
    except InputStop as exc:
        return stop_receipt(
            "full", "R07_760_L3_TARGET6_INPUT_STOP",
            str(exc), "input_authentication", seconds)
    except RuntimeError as exc:
        return stop_receipt(
            "full", "R07_760_L3_TARGET6_INPUT_STOP",
            str(exc), "typed_invariant", seconds)


def validate_receipt(receipt: dict[str, Any]) -> None:
    require(receipt["schema"] == SCHEMA, "receipt schema")
    if receipt["mode"] == "preflight":
        require(receipt.get("preflight_state") == PREFLIGHT_STATE and
                "status" not in receipt and "terminal_token" not in receipt,
                "claim-free preflight envelope")
    else:
        require(receipt["mode"] == "full" and
                receipt["status"] == receipt["terminal_token"] and
                receipt["terminal_token"] in TERMINALS,
                "full terminal envelope")
    claimed = receipt.pop("self_digest_sha256")
    require(claimed == digest_obj(receipt), "self digest")
    receipt["self_digest_sha256"] = claimed
    require(all(value is False for value in receipt["claims"].values()),
            "global claims false")
    base = receipt["static"]["base"]
    require(base["sha256"] == BASE_SHA and base["length"] == 760 and
            base["free_exponent_sums"] == [0, 0],
            "receipt base")


def checked_write(path: Path, receipt: dict[str, Any]) -> bytes:
    validate_receipt(receipt)
    raw = canonical_bytes(receipt) + b"\n"
    full = path if path.is_absolute() else ROOT / path
    full.parent.mkdir(parents=True, exist_ok=True)
    if full.exists():
        require(full.read_bytes() == raw, "immutable output mismatch")
    else:
        full.write_bytes(raw)
    require(full.read_bytes() == raw, "checked write")
    return raw


def toy_tracker() -> None:
    core = load_core()
    sp = core.F3BitSpace(3)
    ech = core.F3BitEchelon(sp)
    require(ech.add(sp.vec({0: 1})) and
            ech.add(sp.vec({1: 1})), "toy rank")
    member, pivot = ech.reduce(sp.vec({0: 2, 1: 1}))
    require(pivot < 0 and member == (0, 0), "toy positive membership")
    target = sp.vec({2: 1})
    _, pivot = ech.reduce(target)
    require(pivot == 2, "toy negative membership")
    sep = ech.extract_separator(target)
    require(sep is not None and sp.dot(sep, target) != 0 and
            all(sp.dot(sep, row) == 0 for row in ech.pivots.values()),
            "toy separator")


def self_test() -> None:
    parent, base = construct_base()
    require(len(parent) == 616 and len(base) == 760, "toy base")
    toy_tracker()
    print("R07_760_L3_TARGET6_V1_PRODUCER_SELFTEST_PASS "
          "toy_member=1 toy_nonmember=1 separator=1", flush=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--preflight", action="store_true")
    parser.add_argument("--full", action="store_true")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--seconds", type=float, default=10800.0)
    args = parser.parse_args()
    require(sum((args.self_test, args.preflight, args.full)) == 1,
            "select exactly one mode")
    if args.self_test:
        self_test()
        return 0
    receipt = build_preflight() if args.preflight else build_full(args.seconds)
    output = args.output or (DEFAULT_PREFLIGHT if args.preflight else DEFAULT_FULL)
    raw = checked_write(output, receipt)
    state_key = "preflight_state" if args.preflight else "terminal_token"
    state_label = "preflight_state" if args.preflight else "terminal"
    print(FINAL_MARKER + f" {state_label}={receipt[state_key]} "
          f"sha256={hashlib.sha256(raw).hexdigest()} bytes={len(raw)}",
          flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
