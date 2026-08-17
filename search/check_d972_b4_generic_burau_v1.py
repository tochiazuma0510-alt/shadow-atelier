#!/usr/bin/env python3
"""Independent exact checker for d972_b4_generic_burau_v1.py.

The producer is not imported.  This checker has a separate Laurent-polynomial
representation (sorted coefficient tuples), rebuilds the frozen norms, and
recomputes every row matrix before accepting any aggregate.
"""

from __future__ import annotations

import argparse
import hashlib
import json
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
ARTIFACT_SCHEMA = "d972-b4-generic-burau/v1"
ALL_STATUS = "ALL_972_K05_IDENTITIES_BY_FAITHFUL_BURAU"
NONCENTRAL_STATUS = "SOME_NORMS_NONCENTRAL_IN_K05_U_M_UNDECIDED"

# A different exact representation from the producer: sorted (exponent,coef)
# tuples, rather than mutable dictionaries.
Poly = tuple[tuple[int, int], ...]
Matrix = tuple[tuple[Poly, ...], ...]
EMPTY: Poly = ()
UNIT: Poly = ((0, 1),)


def must(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def canonical_json(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=True, sort_keys=False,
                      separators=(",", ":")).encode("ascii")


def sha(value: Any) -> str:
    return hashlib.sha256(canonical_json(value)).hexdigest()


def file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def p_from_map(values: dict[int, int]) -> Poly:
    return tuple(sorted((int(e), int(c)) for e, c in values.items() if c))


def p_to_map(poly: Poly) -> dict[int, int]:
    return {e: c for e, c in poly}


def p_add(a: Poly, b: Poly) -> Poly:
    values = p_to_map(a)
    for exponent, coefficient in b:
        values[exponent] = values.get(exponent, 0) + coefficient
        if values[exponent] == 0:
            del values[exponent]
    return p_from_map(values)


def p_neg(a: Poly) -> Poly:
    return tuple((e, -c) for e, c in a)


def p_shift(a: Poly, amount: int, scalar: int = 1) -> Poly:
    return tuple((e + amount, c * scalar) for e, c in a if c * scalar)


def p_mul(a: Poly, b: Poly) -> Poly:
    values: dict[int, int] = {}
    for exponent_a, coefficient_a in a:
        for exponent_b, coefficient_b in b:
            exponent = exponent_a + exponent_b
            values[exponent] = values.get(exponent, 0) + coefficient_a * coefficient_b
    return p_from_map(values)


def one_minus_t(a: Poly) -> Poly:
    return p_add(a, p_neg(p_shift(a, 1)))


def eye() -> Matrix:
    return tuple(tuple(UNIT if r == c else EMPTY for c in range(4))
                 for r in range(4))


def full_product(left: Matrix, right: Matrix) -> Matrix:
    rows: list[tuple[Poly, ...]] = []
    for r in range(4):
        row: list[Poly] = []
        for c in range(4):
            entry = EMPTY
            for k in range(4):
                entry = p_add(entry, p_mul(left[r][k], right[k][c]))
            row.append(entry)
        rows.append(tuple(row))
    return tuple(rows)


def generator(which: int, inverse: bool = False) -> Matrix:
    must(0 <= which < 3, "generator index")
    a = [[UNIT if r == c else EMPTY for c in range(4)] for r in range(4)]
    if not inverse:
        a[which][which] = one_minus_t(UNIT)
        a[which][which + 1] = ((1, 1),)
        a[which + 1][which] = UNIT
        a[which + 1][which + 1] = EMPTY
    else:
        a[which][which] = EMPTY
        a[which][which + 1] = UNIT
        a[which + 1][which] = ((-1, 1),)
        a[which + 1][which + 1] = p_add(UNIT, p_neg(((-1, 1),)))
    return tuple(tuple(row) for row in a)


G = tuple(generator(i) for i in range(3))
GI = tuple(generator(i, True) for i in range(3))


def append_letter(matrix: Matrix, letter: int) -> Matrix:
    """Exact two-column right multiplication, with tuple polynomials."""
    must(letter and abs(letter) <= 3, "bad braid letter")
    i = abs(letter) - 1
    inv = letter < 0
    mutable = [list(row) for row in matrix]
    for r in range(4):
        a, b = matrix[r][i], matrix[r][i + 1]
        if inv:
            mutable[r][i] = p_shift(b, -1)
            mutable[r][i + 1] = p_add(a, p_add(b, p_neg(p_shift(b, -1))))
        else:
            mutable[r][i] = p_add(one_minus_t(a), b)
            mutable[r][i + 1] = p_shift(a, 1)
    return tuple(tuple(row) for row in mutable)


def word_matrix(word: Iterable[int]) -> Matrix:
    result = eye()
    for letter in word:
        result = append_letter(result, letter)
    return result


def generic_word_matrix(word: Iterable[int]) -> Matrix:
    result = eye()
    for letter in word:
        result = full_product(result, G[letter - 1] if letter > 0
                              else GI[-letter - 1])
    return result


PURE = (
    (1, 1),
    (2, 1, 1, -2),
    (3, 2, 1, 1, -2, -3),
    (2, 2),
    (3, 2, 2, -3),
    (3, 3),
)


def inverse_word(word: Iterable[int]) -> list[int]:
    return [-x for x in reversed(tuple(word))]


def six_matrix(word: Iterable[int]) -> Matrix:
    result = eye()
    for letter in word:
        braid_word = PURE[letter - 1] if letter > 0 else inverse_word(PURE[-letter - 1])
        for braid_letter in braid_word:
            result = append_letter(result, braid_letter)
    return result


def matrix_power_of_center(power: int) -> Matrix:
    if power == 0:
        return eye()
    base = (1, 2, 3) * 4
    if power < 0:
        base = tuple(inverse_word(base))
    result = eye()
    for _ in range(abs(power)):
        for letter in base:
            result = append_letter(result, letter)
    return result


def free_reduce(word: Iterable[int]) -> list[int]:
    stack: list[int] = []
    for letter in word:
        must(isinstance(letter, int) and not isinstance(letter, bool)
             and letter != 0 and abs(letter) <= 6, "six-word letter")
        if stack and stack[-1] == -letter:
            stack.pop()
        else:
            stack.append(letter)
    return stack


def rho_apply(word: Iterable[int], rho: list[list[int]]) -> list[int]:
    stack: list[int] = []
    for letter in word:
        image = rho[abs(letter) - 1]
        if letter < 0:
            image = inverse_word(image)
        for image_letter in image:
            if stack and stack[-1] == -image_letter:
                stack.pop()
            else:
                stack.append(image_letter)
    return stack


def marked_f2(word: Iterable[int]) -> list[int]:
    output: list[int] = []
    for letter in word:
        must(abs(letter) in (1, 2), "roof F2 alphabet")
        if abs(letter) == 1:
            output.append(1 if letter > 0 else -1)
        else:
            output.append(4 if letter > 0 else -4)
    return free_reduce(output)


def rebuild_norms(source: dict[str, Any], reverse: bool = False) -> list[list[int]]:
    rho = source["rho_words"]
    norms: list[list[int]] = []
    for raw in source["roof_words"]:
        current = marked_f2(raw)
        orbit = [current]
        for _ in range(4):
            current = rho_apply(current, rho)
            orbit.append(current)
        order = orbit if reverse else tuple(reversed(orbit))
        joined: list[int] = []
        for part in order:
            joined = free_reduce(joined + part)
        norms.append(joined)
    return norms


def key_digest(keys: list[str]) -> str:
    return hashlib.sha256(("\n".join(sorted(keys)) + "\n").encode()).hexdigest()


def load_source() -> tuple[dict[str, Any], str]:
    raw = INPUT.read_bytes()
    source = json.loads(raw.decode("utf-8"))
    must(source.get("schema") == INPUT_SCHEMA, "source schema")
    must(source.get("relator_count") == 158 and len(source["all_relators"]) == 158,
         "source relator count")
    must(source.get("roof_count") == 972 and len(source["roof_words"]) == 972,
         "source roof count")
    must(source.get("all_relators_sha256") == RELATOR_SHA and
         sha(source["all_relators"]) == RELATOR_SHA, "source relator digest")
    must(source.get("rho_words_source") == "universal_v2_canonical" and
         sha(source["rho_words"]) == RHO_SHA, "source rho digest")
    must(source.get("roof_words_sha256") == ROOF_SHA and
         sha(source["roof_words"]) == ROOF_SHA, "source roof digest")
    keys = source["target_keys"]
    must(isinstance(keys, list) and len(keys) == 972 and len(set(keys)) == 972,
         "source key set")
    must(source.get("target_key_digest") == TARGET_SHA and
         key_digest(keys) == TARGET_SHA, "source target digest")
    norms = rebuild_norms(source)
    must(sha(norms) == NORM_SHA, "source norm digest")
    return source, hashlib.sha256(raw).hexdigest()


def exponents(word: Iterable[int]) -> tuple[int, ...]:
    out = [0] * 6
    for letter in word:
        out[abs(letter) - 1] += 1 if letter > 0 else -1
    return tuple(out)


def encode_poly(poly: Poly) -> list[list[int]]:
    return [[e, c] for e, c in poly]


def encode_matrix(matrix: Matrix) -> list[list[list[list[int]]]]:
    return [[encode_poly(matrix[r][c]) for c in range(4)] for r in range(4)]


def parse_matrix(raw: Any) -> Matrix:
    must(isinstance(raw, list) and len(raw) == 4,
         "lossless matrix must have four rows")
    rows: list[tuple[Poly, ...]] = []
    for row in raw:
        must(isinstance(row, list) and len(row) == 4,
             "lossless matrix must have four columns")
        cells: list[Poly] = []
        for cell in row:
            must(isinstance(cell, list), "evaluation-only matrix rejected")
            pairs: list[tuple[int, int]] = []
            last: int | None = None
            for pair in cell:
                must(isinstance(pair, list) and len(pair) == 2,
                     "coefficient pair shape")
                e, c = pair
                must(isinstance(e, int) and not isinstance(e, bool) and
                     isinstance(c, int) and not isinstance(c, bool) and c != 0,
                     "coefficient pair type")
                must(last is None or last < e, "duplicate/unsorted coefficient")
                last = e
                pairs.append((e, c))
            cells.append(tuple(pairs))
        rows.append(tuple(cells))
    return tuple(rows)


def representation_gates() -> dict[str, Any]:
    identity = eye()
    braid = [generic_word_matrix((i, i + 1, i)) ==
             generic_word_matrix((i + 1, i, i + 1)) for i in (1, 2)]
    far = generic_word_matrix((1, 3)) == generic_word_matrix((3, 1))
    inverse = [full_product(G[i], GI[i]) == identity and
               full_product(GI[i], G[i]) == identity for i in range(3)]
    pure = [word_matrix(word) == generic_word_matrix(word) for word in PURE]
    center_word = (1, 2, 3) * 4
    center = word_matrix(center_word)
    central = all(full_product(center, G[i]) == full_product(G[i], center)
                  for i in range(3))
    fast_agree = center == generic_word_matrix(center_word)
    return {
        "braid_relations": braid,
        "far_commutativity": far,
        "exact_inverses": inverse,
        "six_pure_generator_formulas": pure,
        "full_twist_word": list(center_word),
        "full_twist_central": central,
        "full_twist_generic_fast_agree": fast_agree,
        "all_pass": all(braid) and far and all(inverse) and all(pure)
        and central and fast_agree,
        "center_matrix": encode_matrix(center),
    }


def check_row_cover(rows: Any) -> None:
    must(isinstance(rows, list) and len(rows) == 972, "row omission/duplication")
    indices = [row.get("index") if isinstance(row, dict) else None for row in rows]
    must(indices == list(range(972)), "row index omission/duplication/order")


def expected_decision(matrix: Matrix, vector: tuple[int, ...]) -> tuple[str, int | None]:
    if len(set(vector)) != 1:
        return "NONIDENTITY_BY_PB4_ABELIANIZATION", None
    power = vector[0]
    if matrix == matrix_power_of_center(power):
        return "IDENTITY_IN_K05", power
    return "NONCENTRAL_IN_K05", power


def verify_counts(artifact: dict[str, Any], rows: list[dict[str, Any]]) -> None:
    expected = {
        "identity_in_k05": sum(r["decision"] == "IDENTITY_IN_K05" for r in rows),
        "nonidentity_by_abelianization": sum(
            r["decision"] == "NONIDENTITY_BY_PB4_ABELIANIZATION" for r in rows),
        "noncentral_in_k05": sum(r["decision"] == "NONCENTRAL_IN_K05" for r in rows),
    }
    expected["nonidentity_total"] = (expected["nonidentity_by_abelianization"] +
                                      expected["noncentral_in_k05"])
    must(artifact.get("counts") == {**expected}, "forged aggregate counts")
    status = ALL_STATUS if expected["nonidentity_total"] == 0 else NONCENTRAL_STATUS
    must(artifact.get("status") == status, "forged aggregate status")


def verify_artifact(artifact: dict[str, Any], source: dict[str, Any],
                    raw_sha: str, expected_norms: list[list[int]],
                    expected_gates: dict[str, Any]) -> dict[str, Any]:
    must(artifact.get("schema") == ARTIFACT_SCHEMA, "artifact schema")
    must(artifact.get("input_schema") == INPUT_SCHEMA and
         artifact.get("input_raw_sha256") == raw_sha, "artifact input binding")
    must(artifact.get("relator_count") == 158 and
         artifact.get("relator_sha256") == RELATOR_SHA and
         artifact.get("rho_sha256") == RHO_SHA and
         artifact.get("roof_words_sha256") == ROOF_SHA and
         artifact.get("target_key_digest") == TARGET_SHA and
         artifact.get("norm_words_sha256") == NORM_SHA, "artifact digest binding")
    must(artifact.get("matrix_convention") == (
        "column vectors; M(a1...an)=M(a1)...M(an), with the current "
        "matrix right-multiplied by each literal letter; entries are exact "
        "Laurent polynomials in Z[t,t^-1]"), "matrix convention drift")
    must(artifact.get("pure_lifts") == [list(x) for x in PURE], "pure lift drift")
    must(artifact.get("gates") == expected_gates, "unreplayed/forged gate summary")
    must(expected_gates["all_pass"], "representation gates fail")
    rows = artifact.get("rows")
    check_row_cover(rows)
    must(artifact.get("norm_count") == 972 and
         artifact.get("unique_norm_count") == len({tuple(x) for x in expected_norms}),
         "norm aggregate drift")
    matrix_cache: dict[tuple[int, ...], Matrix] = {}
    canonical_matrices: dict[str, Matrix] = {}
    checked: list[dict[str, Any]] = []
    for index, row in enumerate(rows):
        must(isinstance(row, dict), "row object shape")
        must(row.get("target_key") == source["target_keys"][index], "row key binding")
        norm = expected_norms[index]
        must(row.get("norm_word") == norm, "lossless norm binding")
        norm_digest = sha(norm)
        must(row.get("norm_digest") == norm_digest, "norm digest row binding")
        vector = exponents(norm)
        must(row.get("exponent_vector") == list(vector), "exponent vector binding")
        # An evaluation-only receipt has no admissible fallback: every row
        # must carry all 16 exact coefficient lists.
        must("matrix" in row and "evaluations" not in row,
             "evaluation-only evidence rejected")
        supplied = parse_matrix(row["matrix"])
        expected = matrix_cache.get(tuple(norm))
        if expected is None:
            expected = six_matrix(norm)
            matrix_cache[tuple(norm)] = expected
        must(supplied == expected, "exact Laurent matrix mismatch")
        encoded = encode_matrix(expected)
        must(row.get("matrix_sha256") == sha(encoded), "matrix digest mismatch")
        decision, power = expected_decision(expected, vector)
        must(row.get("center_power") == power and row.get("decision") == decision,
             "row decision/center-power mismatch")
        canonical_matrices[row["matrix_sha256"]] = expected
        checked.append({"decision": decision, "matrix": expected,
                        "target_key": row["target_key"]})
        if index % 50 == 0:
            print("BURAU_CHECKER_ROW", index, "unique_matrices",
                  len(canonical_matrices), flush=True)
    must(artifact.get("matrix_unique_count") == len(canonical_matrices),
         "matrix unique aggregate drift")
    verify_counts(artifact, rows)
    return {
        "rows_checked": len(checked),
        "unique_norms_checked": len(matrix_cache),
        "unique_matrices_checked": len(canonical_matrices),
        "counts": artifact["counts"],
        "status": artifact["status"],
    }


def expect_failure(callback: Any, label: str) -> None:
    try:
        callback()
    except (AssertionError, ValueError, KeyError, TypeError):
        return
    raise ValueError("mutation was accepted: " + label)


def selftest() -> None:
    source, _ = load_source()
    norms = rebuild_norms(source)
    must(sha(norms) == NORM_SHA, "checker norm baseline")
    must(sha(rebuild_norms(source, reverse=True)) != NORM_SHA,
         "reversed rho orbit mutation")
    gates = representation_gates()
    must(gates["all_pass"], "checker gate baseline")
    # Omitted and duplicated rows are rejected before any matrix result is used.
    sample = [{"index": i} for i in range(972)]
    expect_failure(lambda: check_row_cover(sample[:-1]), "omitted row")
    sample[17] = {"index": 16}
    expect_failure(lambda: check_row_cover(sample), "duplicated row")
    # An evaluation-only object cannot pass the exact coefficient parser.
    expect_failure(lambda: parse_matrix([[4.0]]), "evaluation-only matrix")
    # Exact center powers are distinct; using the wrong power cannot be hidden
    # by an evaluation at a single parameter.
    c1 = matrix_power_of_center(1)
    c2 = matrix_power_of_center(2)
    must(c1 != c2 and c1 != eye(), "wrong center power mutation")
    fake = {"decision": "IDENTITY_IN_K05", "center_power": 2}
    expected, power = expected_decision(c1, (1, 1, 1, 1, 1, 1))
    must((fake["decision"], fake["center_power"]) != (expected, power),
         "wrong center power was not detectable")
    # Forged aggregates are checked against row-level recomputation.
    fake_artifact = {"counts": {"identity_in_k05": 1}}
    expect_failure(lambda: verify_counts(fake_artifact, [{"decision": "NONCENTRAL_IN_K05"}]),
                   "forged aggregate")
    # Coefficient order and duplicate exponents are rejected losslessly.
    bad = [[[[0, 1], [0, 2]] for _ in range(4)] for _ in range(4)]
    expect_failure(lambda: parse_matrix(bad), "duplicate coefficient exponent")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--evidence", type=Path, required=True)
    parser.add_argument("--skip-selftest", action="store_true")
    parser.add_argument("--selftest-only", action="store_true")
    args = parser.parse_args(argv)
    if args.selftest_only:
        selftest()
        print("CHECKER_SELFTEST_PASS")
        return 0
    if not args.skip_selftest:
        selftest()
    source, raw_sha = load_source()
    norms = rebuild_norms(source)
    gates = representation_gates()
    artifact = json.loads(args.evidence.resolve().read_text(encoding="utf-8"))
    result = verify_artifact(artifact, source, raw_sha, norms, gates)
    result["evidence_sha256"] = file_sha(args.evidence.resolve())
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
