#!/usr/bin/env python3
"""Exact truncated noncommutative Magnus quotients for the B4 U_M input.

For d >= 1 let

    T_d = F_2 <X_1,...,X_6> / (all monomials of length d+1).

The assignment x_i |-> 1+X_i sends every free-group generator to a unit;
the inverse is 1+X_i+...+X_i^d.  For each signed U_M relator r this
program computes E(r)-1 and closes the resulting rows under *both* left and
right multiplication by every monomial.  Row reduction is therefore the
actual two-sided ideal I_d, rather than a class-2 coordinate approximation.
The finite unit group of T_d/I_d is a genuine finite 2-group image of U_M.

This producer is deliberately receipt-oriented.  It never labels an
all-pass result as a nonexistence proof.  A nonzero roof residue is a
candidate witness until the independent checker verifies the lossless
receipt, the exact word/key artifact, every relator, and rho^5.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import os
import tempfile
from pathlib import Path
from typing import Iterable, Iterator, Sequence


NGEN = 6
RELATOR_COUNT = 158
ROOF_COUNT = 972
TARGET_KEY_DIGEST = (
    "9c77e6768feb7ffe7143abf18f753af70e81b8e9cc792910c30ae0075d3b1d62"
)
CANONICAL_RHO = [[-6, -5, -3], [3], [5], [-3, -2, -1], [-5, -4, -1], [1]]
TUPLE_DIGEST = (
    "32e78ca5b97cd8a6fa59a150dac77719c1b8cb527f0467570c4d284600465a91"
)


def canonical_json(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=True, separators=(",", ":")).encode("ascii")


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def file_sha(path: Path) -> str:
    return sha_bytes(path.read_bytes())


def monomials(d: int) -> list[tuple[int, ...]]:
    """The fixed lossless monomial order: length, then lexicographic."""
    out: list[tuple[int, ...]] = [()]
    for length in range(1, d + 1):
        out.extend(itertools.product(range(NGEN), repeat=length))
    return out


def append_bits(poly: int, generator: int, append_index: Sequence[int]) -> int:
    """Right-multiply a polynomial by X_generator, truncating at degree d."""
    out = 0
    bits = poly
    while bits:
        low = bits & -bits
        old = low.bit_length() - 1
        new = append_index[old]
        if new >= 0:
            out ^= 1 << new
        bits ^= low
    return out


def eval_word(word: Iterable[int], d: int, append_maps: Sequence[Sequence[int]]) -> int:
    """Evaluate a signed free word as a bitset polynomial over F_2."""
    one = 1  # monomial () is index zero in the fixed order
    poly = one
    for raw in word:
        letter = int(raw)
        if letter == 0 or abs(letter) > NGEN:
            raise ValueError(f"invalid signed generator {letter}")
        g = abs(letter) - 1
        if letter > 0:
            # (1+X_g), including the constant term.  Omitting it is unsound.
            poly ^= append_bits(poly, g, append_maps[g])
        else:
            # (1+X_g)^(-1)=sum_{k=0}^d X_g^k in characteristic two.
            total = poly
            power = poly
            for _ in range(d):
                power = append_bits(power, g, append_maps[g])
                total ^= power
            poly = total
    return poly


def rho_substitute(word: Sequence[int], rho: Sequence[Sequence[int]]) -> list[int]:
    out: list[int] = []
    for raw in word:
        n = int(raw)
        if n == 0 or abs(n) > NGEN:
            raise ValueError(f"invalid rho input letter {n}")
        image = list(rho[abs(n) - 1])
        if n > 0:
            out.extend(image)
        else:
            out.extend(-x for x in reversed(image))
    return out


def rho_power(word: Sequence[int], rho: Sequence[Sequence[int]], power: int) -> list[int]:
    out = list(word)
    for _ in range(power):
        out = rho_substitute(out, rho)
    return out


def norm_word(word: Sequence[int], rho: Sequence[Sequence[int]]) -> list[int]:
    # The requested order is rho^4(f) ... rho(f) f.
    out: list[int] = []
    for power in reversed(range(5)):
        out.extend(rho_power(word, rho, power))
    return out


def signed_roof(word: Sequence[int]) -> list[int]:
    """P2 F2 letters u,v become U_M generators 1,4."""
    out: list[int] = []
    for raw in word:
        n = int(raw)
        if n in (1, -1):
            out.append(n)
        elif n == 2:
            out.append(4)
        elif n == -2:
            out.append(-4)
        else:
            raise ValueError(f"roof word is not a signed F2 word: {n}")
    return out


def set_bits(poly: int) -> Iterator[int]:
    while poly:
        low = poly & -poly
        yield low.bit_length() - 1
        poly ^= low


def shifted_row(poly: int, left: tuple[int, ...], right: tuple[int, ...],
                mons: Sequence[tuple[int, ...]], index: dict[tuple[int, ...], int],
                d: int) -> int:
    out = 0
    for mid in set_bits(poly):
        mon = left + mons[mid] + right
        if len(mon) <= d:
            out ^= 1 << index[mon]
    return out


def add_high_basis(basis: dict[int, int], row: int) -> None:
    """Insert one row into a deterministic highest-pivot F2 echelon basis."""
    while row:
        pivot = row.bit_length() - 1
        old = basis.get(pivot)
        if old is None:
            basis[pivot] = row
            return
        row ^= old


def reduce_high_basis(basis: dict[int, int], row: int) -> int:
    while row:
        old = basis.get(row.bit_length() - 1)
        if old is None:
            return row
        row ^= old
    return 0


def ideal_basis(rel_polys: Sequence[int], d: int, mons: Sequence[tuple[int, ...]],
                index: dict[tuple[int, ...], int],
                append_maps: Sequence[Sequence[int]]) -> dict[int, int]:
    """Build the full two-sided ideal span, not merely relator rows."""
    by_length: list[list[tuple[int, ...]]] = [
        [m for m in mons if len(m) == n] for n in range(d + 1)
    ]
    basis: dict[int, int] = {}
    for relation in rel_polys:
        if relation == 0:
            continue
        min_degree = min(len(mons[i]) for i in set_bits(relation))
        for total in range(d - min_degree + 1):
            for left_length in range(total + 1):
                right_length = total - left_length
                for left in by_length[left_length]:
                    for right in by_length[right_length]:
                        row = shifted_row(relation, left, right, mons, index, d)
                        if row:
                            add_high_basis(basis, row)
    return basis


def target_digest(keys: Sequence[str]) -> str:
    return sha_bytes(("\n".join(sorted(map(str, keys))) + "\n").encode("utf-8"))


def flat_artifact_key(key: object) -> str:
    if not isinstance(key, list) or len(key) != 3:
        raise ValueError("word/key artifact key shape")
    m, can9, can4 = key
    if not isinstance(m, int) or not isinstance(can9, list) or len(can9) != 3:
        raise ValueError("word/key artifact D9 shape")
    if not isinstance(can4, list) or len(can4) != 9:
        raise ValueError("word/key artifact PSL shape")
    flat: list[str] = []
    for pair in can9:
        if not isinstance(pair, list) or len(pair) != 2:
            raise ValueError("word/key artifact D9 coordinate shape")
        if any(not isinstance(x, int) for x in pair):
            raise ValueError("word/key artifact D9 coordinate type")
        flat.extend(str(x) for x in pair)
    if any(not isinstance(x, int) for x in can4):
        raise ValueError("word/key artifact PSL coordinate type")
    return "(" + str(m) + ";" + ",".join(flat) + ";" + ",".join(map(str, can4)) + ")"


def load_word_key_pairs(path: Path) -> tuple[set[tuple[str, tuple[int, ...]]], dict[str, object]]:
    """Authenticate the independently produced exact roof word/key table."""
    obj = json.loads(path.read_text(encoding="utf-8"))
    if obj.get("schema") != "d972-b4-word-key-artifact/v1":
        raise ValueError("word/key artifact schema drift")
    rows = obj.get("rows")
    if obj.get("count") != ROOF_COUNT or not isinstance(rows, list) or len(rows) != ROOF_COUNT:
        raise ValueError("word/key artifact count gate")
    if obj.get("source_target_key_digest") != TARGET_KEY_DIGEST:
        raise ValueError("word/key artifact target digest drift")
    if obj.get("frozen_tuple_sha256") != TUPLE_DIGEST:
        raise ValueError("word/key artifact tuple digest drift")
    actual = sha_bytes(canonical_json(rows))
    if obj.get("canonical_bytes_sha256") != actual:
        raise ValueError("word/key artifact canonical digest mismatch")
    pairs: set[tuple[str, tuple[int, ...]]] = set()
    keys: set[str] = set()
    legacy_empty_rows: list[int] = []
    for row_index, row in enumerate(rows, 1):
        if not isinstance(row, list) or len(row) != 3:
            raise ValueError("word/key artifact row shape")
        m, key, word = row
        if not isinstance(m, int) or not isinstance(key, list):
            raise ValueError("word/key artifact row types")
        # GAP's IsString([]) ambiguity in the archived v1 receipt serialized
        # exactly the identity word as "".  Normalize only that value, retain
        # the raw file hash, and expose the defect in the receipt metadata.
        if isinstance(word, str) and word == "":
            legacy_empty_rows.append(row_index)
            word = []
        if not isinstance(word, list):
            raise ValueError("word/key artifact row word type")
        if key[0] != m or any(not isinstance(x, int) or x == 0 for x in word):
            raise ValueError("word/key artifact row binding shape")
        flat = flat_artifact_key(key)
        pair = (flat, tuple(int(x) for x in word))
        if pair in pairs:
            raise ValueError("duplicate word/key artifact pair")
        pairs.add(pair)
        keys.add(flat)
    if len(keys) != ROOF_COUNT or target_digest(sorted(keys)) != TARGET_KEY_DIGEST:
        raise ValueError("word/key artifact key set drift")
    return pairs, {"sha256": file_sha(path), "canonical_sha256": actual, "keys": keys,
                   "legacy_empty_rows": legacy_empty_rows}


def evaluate_degree(obj: dict[str, object], d: int, artifact_pairs: set[tuple[str, tuple[int, ...]]] | None,
                    artifact_meta: dict[str, object] | None) -> dict[str, object]:
    rels = [[int(x) for x in w] for w in obj["all_relators"]]  # type: ignore[index]
    rho = [[int(x) for x in w] for w in obj["rho_words"]]  # type: ignore[index]
    roof_base = [[int(x) for x in w] for w in obj["roof_words"]]  # type: ignore[index]
    keys = [str(x) for x in obj["target_keys"]]  # type: ignore[index]
    mons = monomials(d)
    index = {m: i for i, m in enumerate(mons)}
    append_maps: list[list[int]] = []
    for g in range(NGEN):
        amap = [-1] * len(mons)
        for i, mon in enumerate(mons):
            if len(mon) < d:
                amap[i] = index[mon + (g,)]
        append_maps.append(amap)

    rel_polys = [eval_word(w, d, append_maps) ^ 1 for w in rels]
    basis = ideal_basis(rel_polys, d, mons, index, append_maps)
    relator_bad = [i + 1 for i, p in enumerate(rel_polys)
                   if reduce_high_basis(basis, p) != 0]
    rho5_bad: list[int] = []
    for g in range(1, NGEN + 1):
        p = eval_word(rho_power([g], rho, 5) + [-g], d, append_maps) ^ 1
        if reduce_high_basis(basis, p) != 0:
            rho5_bad.append(g)

    rows: list[dict[str, object]] = []
    failures: list[dict[str, object]] = []
    binding_bad = False
    for i, raw in enumerate(roof_base, 1):
        sw = signed_roof(raw)
        word = norm_word(sw, rho)
        residue = reduce_high_basis(basis, eval_word(word, d, append_maps) ^ 1)
        pair_key: str | None = None
        if artifact_pairs is not None:
            # Key and word together are the exact binding; words alone can
            # repeat in different m-fibres (including two identity rows).
            requested_pair = (keys[i - 1], tuple(int(x) for x in raw))
            if requested_pair not in artifact_pairs:
                binding_bad = True
            else:
                pair_key = requested_pair[0]
        row: dict[str, object] = {
            "index": i,
            "input_target_key": keys[i - 1] if i <= len(keys) else None,
            "target_key": pair_key,
            "residue_hex": format(residue, "x"),
        }
        rows.append(row)
        if residue:
            failure = dict(row)
            failure["norm_word"] = word
            failures.append(failure)

    if artifact_pairs is not None:
        # P2 roof words are encoded in the U_M alphabet (1,4), while the
        # artifact is the natural marked F2 alphabet (1,2).  Compare after
        # converting each input word back to its F2 letters.
        input_pairs: set[tuple[str, tuple[int, ...]]] = {
            (key, tuple(int(x) for x in raw)) for raw, key in zip(roof_base, keys)
        }
        # Words need not be unique across the two m-fibres (the identity word
        # is a concrete example), so compare exact key/word pairs rather than
        # imposing a false word-uniqueness gate.
        if input_pairs != set(artifact_pairs) or len(input_pairs) != ROOF_COUNT:
            binding_bad = True

    if failures and not relator_bad and not rho5_bad:
        status = "DEFECT_CANDIDATE" if not binding_bad else "DEFECT_UNBOUND"
    elif failures:
        status = "UNKNOWN_GATE_FAIL"
    elif binding_bad:
        status = "ALLPASS_UNBOUND"
    else:
        status = "ALLPASS_UNKNOWN"
    return {
        "degree": d,
        "monomial_count": len(mons),
        "ideal_rank": len(basis),
        "quotient_dimension": len(mons) - len(basis),
        "relator_bad": relator_bad,
        "rho5_bad_generators": rho5_bad,
        "roof_count": len(rows),
        "roof_defect_count": len(failures),
        "first_defect": failures[0] if failures else None,
        "rows": rows,
        "ideal_basis_hex": [format(basis[p], "x") for p in sorted(basis)],
        "ideal_basis_pivots": sorted(basis),
        "artifact_binding": {
            "available": artifact_pairs is not None,
            "status": ("PASS_LEGACY_EMPTY_NORMALIZED"
                       if artifact_pairs is not None and artifact_meta and artifact_meta.get("legacy_empty_rows")
                       else "PASS" if artifact_pairs is not None and not binding_bad else "FAIL_OR_MISSING"),
            "artifact_sha256": artifact_meta.get("sha256") if artifact_meta else None,
            "legacy_empty_rows": artifact_meta.get("legacy_empty_rows", []) if artifact_meta else [],
        },
        "status": status,
        "method": "F2 noncommutative truncated algebra; complete two-sided monomial ideal",
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--degree", type=int, action="append", default=None)
    parser.add_argument("--input", type=Path,
                        default=Path("ci/out/d972_b4_p2_magnus_input_v1.json"))
    parser.add_argument("--artifact", type=Path,
                        default=Path("ci/out/d972_b4_word_key_artifact_v1.json"))
    parser.add_argument("--output", type=Path,
                        default=Path(tempfile.gettempdir()) / "d972_b4_magnus_ideal_v2_receipt.json")
    args = parser.parse_args(argv)
    degrees = sorted(set(args.degree or [2, 3, 4, 5]))
    if any(d < 1 or d > 5 for d in degrees):
        raise ValueError("degree must be in 1..5")
    obj = json.loads(args.input.read_text(encoding="utf-8"))
    if obj.get("schema") not in {"d972-b4-p2-magnus-input/v1",
                                  "d972-b4-p2-magnus-input/v2"}:
        raise ValueError("Magnus input schema drift")
    if len(obj.get("all_relators", [])) != RELATOR_COUNT or len(obj.get("roof_words", [])) != ROOF_COUNT:
        raise ValueError("exact relator/roof count gate failed")
    if obj.get("target_key_digest") != TARGET_KEY_DIGEST:
        raise ValueError("frozen target-key digest gate failed")
    if obj.get("rho_words") != CANONICAL_RHO:
        raise ValueError("legacy rho map rejected; require universal_v2 canonical rho")
    if ("rho_words_source" in obj and
            obj.get("rho_words_source") != "universal_v2_canonical"):
        raise ValueError("rho_words_source is not universal_v2_canonical")
    rel_digest = sha_bytes(canonical_json(obj["all_relators"]))
    if obj.get("all_relators_sha256") != rel_digest:
        raise ValueError("relator digest metadata mismatch")
    roof_digest = sha_bytes(canonical_json(obj["roof_words"]))
    if obj.get("roof_words_sha256") != roof_digest:
        raise ValueError("roof digest metadata mismatch")
    artifact_pairs: set[tuple[str, tuple[int, ...]]] | None = None
    artifact_meta: dict[str, object] | None = None
    artifact_error: str | None = None
    if args.artifact.is_file():
        try:
            artifact_pairs, artifact_meta = load_word_key_pairs(args.artifact)
        except (OSError, TypeError, ValueError, json.JSONDecodeError) as exc:
            artifact_error = str(exc)
    result: dict[str, object] = {
        "schema": "d972-b4-magnus-ideal/v2",
        "status": "CANDIDATE_RECEIPT",
        "input_path": str(args.input),
        "input_sha256": file_sha(args.input),
        "input_digests": {
            "all_relators_sha256": obj.get("all_relators_sha256"),
            "target_key_digest": obj.get("target_key_digest"),
            "roof_words_sha256": obj.get("roof_words_sha256"),
        },
        "artifact": {"path": str(args.artifact), "error": artifact_error,
                     "sha256": artifact_meta.get("sha256") if artifact_meta else None},
        "model": {
            "field": "F2", "generators": NGEN, "truncation": "all monomials of degree > d",
            "inverse": "(1+X_i)^-1=sum_{k=0}^d X_i^k",
            "ideal": "two-sided span of u*(E(r)-1)*v for all monomials u,v",
            "finite_unit_group": "subgroup of units of finite-dimensional F2 algebra",
        },
        "degrees": {},
    }
    for d in degrees:
        row = evaluate_degree(obj, d, artifact_pairs, artifact_meta)
        result["degrees"][str(d)] = row  # type: ignore[index]
        print(json.dumps({k: row[k] for k in (
            "degree", "status", "monomial_count", "ideal_rank", "roof_defect_count",
            "relator_bad", "rho5_bad_generators")}, sort_keys=True))
    statuses = [x["status"] for x in result["degrees"].values()]  # type: ignore[union-attr]
    if any(x == "DEFECT_CANDIDATE" for x in statuses):
        result["status"] = "DEFECT_CANDIDATE_NEEDS_INDEPENDENT_CHECK"
    elif any(x == "DEFECT_UNBOUND" for x in statuses):
        result["status"] = "DEFECT_BUT_WORD_KEY_UNBOUND"
    elif all(x == "ALLPASS_UNKNOWN" for x in statuses):
        result["status"] = "ALLPASS_GRADING_UNKNOWN"
    else:
        result["status"] = "CANDIDATE_RECEIPT"
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=True, sort_keys=True, indent=2) + "\n",
                           encoding="utf-8")
    print(json.dumps({"status": result["status"], "output": str(args.output)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
