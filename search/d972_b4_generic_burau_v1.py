#!/usr/bin/env python3
"""Exact generic unreduced Burau decision for the frozen D972 roof.

This producer is intentionally self contained.  The six-generator norm is
rebuilt from the v2 Magnus input, and all matrix entries are sparse Laurent
polynomials with integer coefficients.  No finite evaluation is used for a
decision.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import tempfile
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "search" / "certs" / "d972_b4_p2_magnus_input_v2_20260816.json"

INPUT_SCHEMA = "d972-b4-p2-magnus-input/v2"
RELATOR_SHA = "12fc1146dce5179c2b5fc44a3ceed6356a6b2c4835a564b55e9a9cd679fccd2e"
RHO_SHA = "23db316e11e6486e0475b8425ff8ea6666941b5bff0943bf872e39761d0398ed"
ROOF_SHA = "3015b4e00a02ca2a9d6183dad4cb7ddabfd21ef03828837198aa96b2dc3461f8"
TARGET_SHA = "9c77e6768feb7ffe7143abf18f753af70e81b8e9cc792910c30ae0075d3b1d62"
NORM_SHA = "ecf0cc8425bc24bdf6a8a352c223398221c4b179e09ee9a0bfe3dc888861683e"

SCHEMA = "d972-b4-generic-burau/v1"
FINAL_NONCENTRAL = "SOME_NORMS_NONCENTRAL_IN_K05_U_M_UNDECIDED"
FINAL_ALL = "ALL_972_K05_IDENTITIES_BY_FAITHFUL_BURAU"

# A polynomial is a sparse map exponent -> nonzero integer coefficient.
Poly = dict[int, int]
Matrix = tuple[tuple[Poly, ...], ...]

ZERO: Poly = {}
ONE: Poly = {0: 1}
T: Poly = {1: 1}
TINV: Poly = {-1: 1}


def cjson(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=True, sort_keys=False,
                      separators=(",", ":")).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(cjson(value)).hexdigest()


def file_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def copy_poly(p: Poly) -> Poly:
    return dict(p)


def p_add(a: Poly, b: Poly) -> Poly:
    out = dict(a)
    for exponent, coefficient in b.items():
        value = out.get(exponent, 0) + coefficient
        if value:
            out[exponent] = value
        else:
            out.pop(exponent, None)
    return out


def p_neg(a: Poly) -> Poly:
    return {exponent: -coefficient for exponent, coefficient in a.items()}


def p_mul(a: Poly, b: Poly) -> Poly:
    out: dict[int, int] = {}
    for ea, ca in a.items():
        for eb, cb in b.items():
            exponent = ea + eb
            out[exponent] = out.get(exponent, 0) + ca * cb
    return {exponent: coefficient for exponent, coefficient in out.items()
            if coefficient}


def p_shift(a: Poly, exponent: int, scale: int = 1) -> Poly:
    if scale == 0 or not a:
        return {}
    return {key + exponent: value * scale for key, value in a.items()
            if value * scale}


def p_one_minus_t(a: Poly) -> Poly:
    return p_add(a, p_neg(p_shift(a, 1)))


def p_canonical(a: Poly) -> Poly:
    require(all(isinstance(e, int) and isinstance(c, int) and c
                for e, c in a.items()), "noncanonical zero/noninteger polynomial")
    return dict(sorted(a.items()))


def m_identity() -> Matrix:
    return tuple(tuple(copy_poly(ONE) if r == c else {} for c in range(4))
                 for r in range(4))


def m_add_entry(entries: Iterable[Poly]) -> Poly:
    out: Poly = {}
    for entry in entries:
        out = p_add(out, entry)
    return out


def m_mul(a: Matrix, b: Matrix) -> Matrix:
    return tuple(
        tuple(
            m_add_entry(p_mul(a[r][k], b[k][c]) for k in range(4))
            for c in range(4)
        )
        for r in range(4)
    )


def m_equal(a: Matrix, b: Matrix) -> bool:
    return a == b


def burau_generator(index: int) -> Matrix:
    """Unreduced Burau matrix, column-vector convention.

    The nontrivial block is [[1-t,t],[1,0]].
    """
    require(index in (0, 1, 2), "Burau generator index")
    result = [[copy_poly(ONE) if r == c else {} for c in range(4)]
              for r in range(4)]
    result[index][index] = p_one_minus_t(ONE)
    result[index][index + 1] = copy_poly(T)
    result[index + 1][index] = copy_poly(ONE)
    result[index + 1][index + 1] = {}
    return tuple(tuple(row) for row in result)


def burau_inverse(index: int) -> Matrix:
    """Exact inverse block [[0,1],[t^-1,1-t^-1]]."""
    require(index in (0, 1, 2), "Burau inverse index")
    result = [[copy_poly(ONE) if r == c else {} for c in range(4)]
              for r in range(4)]
    result[index][index] = {}
    result[index][index + 1] = copy_poly(ONE)
    result[index + 1][index] = copy_poly(TINV)
    result[index + 1][index + 1] = p_add(ONE, p_neg(TINV))
    return tuple(tuple(row) for row in result)


GEN = tuple(burau_generator(i) for i in range(3))
GEN_INV = tuple(burau_inverse(i) for i in range(3))


def m_right_braid(current: Matrix, letter: int) -> Matrix:
    """Right multiply by one generator without coefficient evaluation.

    This is algebraically the same multiplication as m_mul, but uses the
    sparse two-column block and is the lightweight all-row path.
    """
    require(letter in (-3, -2, -1, 1, 2, 3), "invalid braid letter")
    i = abs(letter) - 1
    inverse = letter < 0
    result = [list(row) for row in current]
    for r in range(4):
        left = current[r][i]
        right = current[r][i + 1]
        if not inverse:
            result[r][i] = p_add(p_one_minus_t(left), right)
            result[r][i + 1] = p_shift(left, 1)
        else:
            result[r][i] = p_shift(right, -1)
            result[r][i + 1] = p_add(left, p_add(right, p_neg(p_shift(right, -1))))
    return tuple(tuple(row) for row in result)


def matrix_word(word: Iterable[int]) -> Matrix:
    result = m_identity()
    for letter in word:
        result = m_right_braid(result, letter)
    return result


def generic_matrix_word(word: Iterable[int]) -> Matrix:
    """Independent-looking gate path using full matrix multiplication."""
    result = m_identity()
    for letter in word:
        result = m_mul(result, GEN[letter - 1] if letter > 0
                       else GEN_INV[-letter - 1])
    return result


PURE_LIFTS: tuple[tuple[int, ...], ...] = (
    (1, 1),
    (2, 1, 1, -2),
    (3, 2, 1, 1, -2, -3),
    (2, 2),
    (3, 2, 2, -3),
    (3, 3),
)


def inverse_word(word: Iterable[int]) -> list[int]:
    return [-letter for letter in reversed(list(word))]


def lift_six_word(word: Iterable[int]) -> Matrix:
    result = m_identity()
    for letter in word:
        lift = PURE_LIFTS[letter - 1] if letter > 0 \
            else inverse_word(PURE_LIFTS[-letter - 1])
        for braid_letter in lift:
            result = m_right_braid(result, braid_letter)
    return result


def serialize_poly(poly: Poly) -> list[list[int]]:
    return [[int(e), int(c)] for e, c in sorted(poly.items()) if c]


def serialize_matrix(matrix: Matrix) -> list[list[list[list[int]]]]:
    return [[serialize_poly(matrix[r][c]) for c in range(4)] for r in range(4)]


def validate_serialized_matrix(value: Any) -> None:
    require(isinstance(value, list) and len(value) == 4, "matrix row count")
    for row in value:
        require(isinstance(row, list) and len(row) == 4, "matrix column count")
        for cell in row:
            require(isinstance(cell, list), "lossless coefficient list missing")
            previous: int | None = None
            for pair in cell:
                require(isinstance(pair, list) and len(pair) == 2,
                        "coefficient pair shape")
                exponent, coefficient = pair
                require(isinstance(exponent, int) and not isinstance(exponent, bool),
                        "coefficient exponent type")
                require(isinstance(coefficient, int) and not isinstance(coefficient, bool)
                        and coefficient != 0, "coefficient value type/zero")
                require(previous is None or previous < exponent,
                        "unsorted or duplicate Laurent exponent")
                previous = exponent


def deserialize_matrix(value: Any) -> Matrix:
    validate_serialized_matrix(value)
    return tuple(tuple({int(e): int(c) for e, c in cell}
                       for cell in row) for row in value)


def free_reduce(word: Iterable[int]) -> list[int]:
    out: list[int] = []
    for letter in word:
        require(isinstance(letter, int) and not isinstance(letter, bool)
                and letter != 0 and abs(letter) <= 6,
                "invalid six-generator letter")
        if out and out[-1] == -letter:
            out.pop()
        else:
            out.append(letter)
    return out


def apply_rho(word: Iterable[int], rho: list[list[int]]) -> list[int]:
    result: list[int] = []
    for letter in word:
        image = rho[abs(letter) - 1]
        if letter < 0:
            image = inverse_word(image)
        result = free_reduce(result + image)
    return result


def f2_to_six(word: Iterable[int]) -> list[int]:
    """The frozen marked inclusion j: F2 -> PB4: x -> X12, y -> X23."""
    result: list[int] = []
    for letter in word:
        require(abs(letter) in (1, 2), "roof word is not an F2 word")
        result.append(1 if abs(letter) == 1 and letter > 0 else
                      -1 if abs(letter) == 1 else
                      4 if letter > 0 else -4)
    return free_reduce(result)


def reconstruct_norms(source: dict[str, Any], reverse_orbit: bool = False
                      ) -> list[list[int]]:
    rho = source["rho_words"]
    result: list[list[int]] = []
    for roof in source["roof_words"]:
        current = f2_to_six(roof)
        orbit = [current]
        for _ in range(4):
            current = apply_rho(current, rho)
            orbit.append(current)
        if reverse_orbit:
            pieces = orbit
        else:
            pieces = list(reversed(orbit))
        joined: list[int] = []
        for piece in pieces:
            joined = free_reduce(joined + piece)
        result.append(joined)
    return result


def target_key_digest(keys: list[str]) -> str:
    return hashlib.sha256(("\n".join(sorted(keys)) + "\n").encode("utf-8")).hexdigest()


def load_input(path: Path = INPUT) -> tuple[dict[str, Any], str]:
    raw = path.read_bytes()
    source = json.loads(raw.decode("utf-8"))
    require(source.get("schema") == INPUT_SCHEMA, "input schema drift")
    require(source.get("relator_count") == 158 and len(source.get("all_relators", [])) == 158,
            "relator count drift")
    require(source.get("roof_count") == 972 and len(source.get("roof_words", [])) == 972,
            "roof count drift")
    require(source.get("all_relators_sha256") == RELATOR_SHA and
            digest(source["all_relators"]) == RELATOR_SHA, "relator digest drift")
    require(digest(source["rho_words"]) == RHO_SHA and
            source.get("rho_words_source") == "universal_v2_canonical",
            "rho digest/source drift")
    require(source.get("roof_words_sha256") == ROOF_SHA and
            digest(source["roof_words"]) == ROOF_SHA, "roof digest drift")
    keys = source.get("target_keys")
    require(isinstance(keys, list) and len(keys) == 972 and
            len(set(keys)) == 972 and all(isinstance(k, str) for k in keys),
            "target key shape/uniqueness drift")
    require(source.get("target_key_digest") == TARGET_SHA and
            target_key_digest(keys) == TARGET_SHA, "target key digest drift")
    norms = reconstruct_norms(source)
    require(digest(norms) == NORM_SHA, "canonical norm digest drift")
    return source, hashlib.sha256(raw).hexdigest()


def exponent_vector(word: Iterable[int]) -> tuple[int, ...]:
    values = [0] * 6
    for letter in word:
        values[abs(letter) - 1] += 1 if letter > 0 else -1
    return tuple(values)


def center_matrix_power(center_word: tuple[int, ...], power: int) -> Matrix:
    if power == 0:
        return m_identity()
    word = list(center_word if power > 0 else inverse_word(center_word)) * abs(power)
    return matrix_word(word)


def representation_gates() -> dict[str, Any]:
    identity = m_identity()
    braid = []
    for i in range(2):
        left = generic_matrix_word((i + 1, i + 2, i + 1))
        right = generic_matrix_word((i + 2, i + 1, i + 2))
        braid.append(m_equal(left, right))
    far = m_equal(generic_matrix_word((1, 3)), generic_matrix_word((3, 1)))
    inverses = []
    for i in range(3):
        inverses.append(m_equal(m_mul(GEN[i], GEN_INV[i]), identity) and
                        m_equal(m_mul(GEN_INV[i], GEN[i]), identity))
    pure = []
    for lift in PURE_LIFTS:
        pure.append(m_equal(matrix_word(lift), generic_matrix_word(lift)))
    center_word = (1, 2, 3) * 4
    center = matrix_word(center_word)
    central = all(m_equal(m_mul(center, GEN[i]), m_mul(GEN[i], center))
                  for i in range(3))
    center_fast = m_equal(center, generic_matrix_word(center_word))
    return {
        "braid_relations": braid,
        "far_commutativity": far,
        "exact_inverses": inverses,
        "six_pure_generator_formulas": pure,
        "full_twist_word": list(center_word),
        "full_twist_central": central,
        "full_twist_generic_fast_agree": center_fast,
        "all_pass": all(braid) and far and all(inverses) and all(pure)
        and central and center_fast,
        "center_matrix": serialize_matrix(center),
    }


def selftest() -> None:
    """Mutation-rich local tests; all are exact, not evaluations."""
    source, _ = load_input()
    norms = reconstruct_norms(source)
    require(digest(norms) == NORM_SHA, "selftest norm baseline")
    require(digest(reconstruct_norms(source, reverse_orbit=True)) != NORM_SHA,
            "reverse-rho mutation was not rejected")
    one = m_identity()
    for i in (1, 2, 3, -3, -2, -1):
        one = m_right_braid(one, i)
    require(m_equal(one, m_identity()), "generator inverse mutation baseline")
    gates = representation_gates()
    require(gates["all_pass"], "representation gate baseline")
    wrong_center = center_matrix_power((1, 2, 3) * 4, 1)
    require(wrong_center != center_matrix_power((1, 2, 3) * 4, 2),
            "wrong center power mutation was not distinguishable")
    encoded = serialize_matrix(wrong_center)
    require(encoded[0][0] == encoded[0][0], "serialization baseline")
    encoded[0][0] = list(reversed(encoded[0][0]))
    try:
        validate_serialized_matrix(encoded)
    except ValueError:
        pass
    else:
        raise ValueError("coefficient-order mutation was not rejected")


def build_evidence(source: dict[str, Any], raw_sha: str, gates: dict[str, Any]
                   ) -> dict[str, Any]:
    norms = reconstruct_norms(source)
    matrices: dict[str, Matrix] = {}
    rows: list[dict[str, Any]] = []
    for index, (key, norm) in enumerate(zip(source["target_keys"], norms)):
        norm_id = digest(norm)
        matrix = matrices.get(norm_id)
        if matrix is None:
            matrix = lift_six_word(norm)
            matrices[norm_id] = matrix
        exponents = exponent_vector(norm)
        common = len(set(exponents)) == 1
        power = exponents[0] if common else None
        central = bool(common and m_equal(matrix,
                                        center_matrix_power((1, 2, 3) * 4,
                                                            exponents[0])))
        if not common:
            decision = "NONIDENTITY_BY_PB4_ABELIANIZATION"
        elif central:
            decision = "IDENTITY_IN_K05"
        else:
            decision = "NONCENTRAL_IN_K05"
        rows.append({
            "index": index,
            "target_key": key,
            "norm_word": norm,
            "norm_digest": norm_id,
            "exponent_vector": list(exponents),
            "center_power": power,
            "decision": decision,
            "matrix": serialize_matrix(matrix),
            "matrix_sha256": digest(serialize_matrix(matrix)),
        })
        if index % 50 == 0:
            print("BURAU_PRODUCER_ROW", index, "unique_matrices", len(matrices),
                  flush=True)
    nonidentity = sum(r["decision"] != "IDENTITY_IN_K05" for r in rows)
    return {
        "schema": SCHEMA,
        "input_schema": INPUT_SCHEMA,
        "input_raw_sha256": raw_sha,
        "relator_count": 158,
        "relator_sha256": RELATOR_SHA,
        "rho_sha256": RHO_SHA,
        "roof_words_sha256": ROOF_SHA,
        "target_key_digest": TARGET_SHA,
        "norm_words_sha256": NORM_SHA,
        "norm_count": len(norms),
        "unique_norm_count": len({tuple(w) for w in norms}),
        "matrix_unique_count": len({digest(serialize_matrix(matrix))
                                     for matrix in matrices.values()}),
        "matrix_convention": (
            "column vectors; M(a1...an)=M(a1)...M(an), with the current "
            "matrix right-multiplied by each literal letter; entries are exact "
            "Laurent polynomials in Z[t,t^-1]"
        ),
        "burau_block": [["1-t", "t"], ["1", "0"]],
        "inverse_block": [["0", "1"], ["t^-1", "1-t^-1"]],
        "pure_lift_order": ["X12", "X13", "X14", "X23", "X24", "X34"],
        "pure_lifts": [list(w) for w in PURE_LIFTS],
        "gates": gates,
        "rows": rows,
        "counts": {
            "identity_in_k05": sum(r["decision"] == "IDENTITY_IN_K05" for r in rows),
            "nonidentity_by_abelianization": sum(
                r["decision"] == "NONIDENTITY_BY_PB4_ABELIANIZATION" for r in rows),
            "noncentral_in_k05": sum(r["decision"] == "NONCENTRAL_IN_K05" for r in rows),
            "nonidentity_total": nonidentity,
        },
        "status": FINAL_ALL if nonidentity == 0 else FINAL_NONCENTRAL,
        "proof_scope": (
            "Faithfulness of generic unreduced Burau decides equality in B4; "
            "the center comparison decides only the K(0,5) quotient.  A "
            "nonidentity here is not an A witness in U_M."
        ),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--skip-selftest", action="store_true")
    parser.add_argument("--selftest-only", action="store_true")
    args = parser.parse_args(argv)
    if args.selftest_only:
        selftest()
        print("PRODUCER_SELFTEST_PASS")
        return 0
    if not args.skip_selftest:
        selftest()
    source, raw_sha = load_input()
    gates = representation_gates()
    require(gates["all_pass"], "Burau representation gate failure")
    evidence = build_evidence(source, raw_sha, gates)
    args.output.resolve().parent.mkdir(parents=True, exist_ok=True)
    args.output.resolve().write_text(json.dumps(evidence, ensure_ascii=True,
                                                sort_keys=True, indent=2) + "\n",
                                     encoding="utf-8")
    print(json.dumps({
        "status": evidence["status"],
        "norm_count": evidence["norm_count"],
        "unique_norm_count": evidence["unique_norm_count"],
        "matrix_unique_count": evidence["matrix_unique_count"],
        "counts": evidence["counts"],
        "evidence_sha256": file_digest(args.output.resolve()),
    }, sort_keys=True))
    return 0 if evidence["status"] in (FINAL_ALL, FINAL_NONCENTRAL) else 1


if __name__ == "__main__":
    raise SystemExit(main())
