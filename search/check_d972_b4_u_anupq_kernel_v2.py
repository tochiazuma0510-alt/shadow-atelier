#!/usr/bin/env python3
"""Independent receipt checker for the canonical raw161 ANUPQ lane.

This checker does not import or execute the GAP producer.  It reconstructs the
regular C2^5 transversal, all 5056 ordinary RS relators, and all 972 exact
norm rows from the pinned artifacts.  A p-quotient receipt is accepted only if
its basis/digest contract and any reported first image agree with that replay.
An all-pass or resource-limited p=3 run remains UNKNOWN.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
from typing import Any


SOURCE_SHA = "c61b2b77131127aca83a8d7c56b7fdadd2d519b040ea4d91093622c813c2b4a9"
RELATOR_SHA = "12fc1146dce5179c2b5fc44a3ceed6356a6b2c4835a564b55e9a9cd679fccd2e"
WORDS_SHA = "564a921be8114bdeb963f679c121e8d9aa90e148c65e95e393874fcba843e9f9"
NORM_SHA = "ecf0cc8425bc24bdf6a8a352c223398221c4b179e09ee9a0bfe3dc888861683e"
RAW_RS_SHA = "29c65a6cf9d0308e25ca462c752d7b540a6856e7d99d5d1d016919240b575c0e"
NORM_RS_SHA = "f7134e15e92c80a5ceeede38e94314539815a665ba7d279443208de1696041f8"
RHO = ((-6, -5, -3), (3,), (5,), (-3, -2, -1), (-5, -4, -1), (1,))
GEN_BITS = (1, 2, 4, 8, 16, 31)


def cjson(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=True, separators=(",", ":")).encode("ascii")


def sha(value: Any) -> str:
    return hashlib.sha256(cjson(value)).hexdigest()


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def free_reduce(word: list[int]) -> list[int]:
    out: list[int] = []
    for letter in word:
        if out and out[-1] == -letter:
            out.pop()
        else:
            out.append(letter)
    return out


def inverse_word(word: list[int]) -> list[int]:
    return [-x for x in reversed(word)]


def transversal() -> list[list[int]]:
    return [[i + 1 for i in range(5) if mask & (1 << i)] for mask in range(32)]


def build_raw_rs(relators: list[list[int]]) -> tuple[list[list[int]], dict[tuple[int, int], int]]:
    reps = transversal()
    pair_id: dict[tuple[int, int], int] = {}
    next_id = 0
    for mask in range(32):
        for gen, bit in enumerate(GEN_BITS, 1):
            raw = reps[mask] + [gen] + inverse_word(reps[mask ^ bit])
            reduced = free_reduce(raw)
            if reduced:
                next_id += 1
                pair_id[(mask, gen)] = next_id
            else:
                pair_id[(mask, gen)] = 0
    if next_id != 161:
        raise ValueError(f"raw Schreier generator count drift: {next_id}")

    def rewrite(word: list[int], start: int) -> list[int]:
        mask = start
        out: list[int] = []
        for letter in word:
            gen = abs(letter)
            bit = GEN_BITS[gen - 1]
            if letter > 0:
                ident = pair_id[(mask, gen)]
                if ident:
                    out.append(ident)
                mask ^= bit
            else:
                mask ^= bit
                ident = pair_id[(mask, gen)]
                if ident:
                    out.append(-ident)
        if mask != start:
            raise ValueError("relator does not close in C2^5")
        return free_reduce(out)

    result: list[list[int]] = []
    for start in range(32):
        for relator in relators:
            row = rewrite(relator, start)
            if row:
                result.append(row)
    if len(result) != 5056:
        raise ValueError(f"raw Schreier relator count drift: {len(result)}")
    return result, pair_id


def rho_word(word: list[int]) -> list[int]:
    out: list[int] = []
    for letter in word:
        image = list(RHO[abs(letter) - 1])
        if letter < 0:
            image = inverse_word(image)
        out.extend(image)
    return free_reduce(out)


def exact_norm(f2_word: list[int]) -> list[int]:
    jword: list[int] = []
    for letter in f2_word:
        if abs(letter) == 1:
            jword.append(1 if letter > 0 else -1)
        elif abs(letter) == 2:
            jword.append(4 if letter > 0 else -4)
        else:
            raise ValueError("F2 norm row alphabet drift")
    orbit: list[list[int]] = []
    current = free_reduce(jword)
    for _ in range(5):
        orbit.append(current)
        current = rho_word(current)
    result: list[int] = []
    for current in reversed(orbit):
        result = free_reduce(result + current)
    return result


def load_inputs(input_path: Path, words_path: Path) -> tuple[list[list[int]], list[list[int]]]:
    input_bytes = input_path.read_bytes()
    if sha_bytes(input_bytes) != SOURCE_SHA:
        raise ValueError("canonical input SHA drift")
    source = json.loads(input_bytes.decode("utf-8"))
    if (source.get("schema") != "d972-b4-p2-magnus-input/v2" or
            len(source.get("all_relators", [])) != 158 or
            tuple(tuple(x) for x in source.get("rho_words", [])) != RHO or
            source.get("all_relators_sha256") != RELATOR_SHA):
        raise ValueError("canonical input contract drift")
    relators = [[int(x) for x in word] for word in source["all_relators"]]
    if sha(relators) != RELATOR_SHA:
        raise ValueError("relator digest drift")

    words_bytes = words_path.read_bytes()
    if sha_bytes(words_bytes) != WORDS_SHA:
        raise ValueError("word artifact SHA drift")
    words = json.loads(words_bytes.decode("utf-8"))
    if (words.get("schema") != "d972-b4-word-key-artifact/v1" or
            words.get("count") != 972 or
            words.get("canonical_bytes_sha256") != sha(words["rows"])):
        raise ValueError("word artifact contract drift")
    f2_rows: list[list[int]] = []
    for row in words["rows"]:
        if not isinstance(row, list) or len(row) != 3:
            raise ValueError("word row shape drift")
        f2_rows.append([int(x) for x in row[2]])
    norms = [exact_norm(row) for row in f2_rows]
    if sha(norms) != NORM_SHA:
        raise ValueError("original norm digest drift")
    return relators, norms


def _coords_to_word(coords: list[int]) -> list[int]:
    word: list[int] = []
    for index, exponent in enumerate(coords, 1):
        word.extend([index] * exponent)
    return word


def _pc_contract(
    orders: list[int],
    power: Any,
    conjugates: Any,
) -> tuple[list[list[int]], dict[tuple[int, int], list[int]]]:
    dimension = len(orders)
    if (not isinstance(power, list) or len(power) != dimension or
            not isinstance(conjugates, list)):
        raise ValueError("pc presentation relation shape drift")

    def checked_vector(value: Any, label: str) -> list[int]:
        if (not isinstance(value, list) or len(value) != dimension or
                any(not isinstance(x, int) or not 0 <= x < orders[i]
                    for i, x in enumerate(value))):
            raise ValueError(f"{label} coordinate drift")
        return [int(x) for x in value]

    power_rows = [checked_vector(row, "power") for row in power]
    for index, row in enumerate(power_rows):
        if any(row[i] != 0 for i in range(index + 1)):
            raise ValueError("power relation is not a pc tail")

    expected_pairs = {(i, j) for i in range(2, dimension + 1)
                      for j in range(1, i)}
    conjugate_rows: dict[tuple[int, int], list[int]] = {}
    for row in conjugates:
        if (not isinstance(row, list) or len(row) != 3 or
                not isinstance(row[0], int) or not isinstance(row[1], int)):
            raise ValueError("conjugate relation shape drift")
        pair = (row[0], row[1])
        if pair in conjugate_rows or pair not in expected_pairs:
            raise ValueError("conjugate relation index drift")
        vector = checked_vector(row[2], "conjugate")
        if any(vector[i] != 0 for i in range(pair[0] - 1)):
            raise ValueError("conjugate relation is not a pc tail")
        if vector[pair[0] - 1] != 1:
            raise ValueError("conjugate relation leading coordinate drift")
        conjugate_rows[pair] = vector
    if set(conjugate_rows) != expected_pairs:
        raise ValueError("conjugate relation coverage drift")
    return power_rows, conjugate_rows


def _pc_normalize(
    word: list[int],
    orders: list[int],
    power: list[list[int]],
    conjugates: dict[tuple[int, int], list[int]],
) -> list[int]:
    """Collect a positive PC word using the receipt's defining relations."""

    dimension = len(orders)
    sequence = list(word)
    if any(not isinstance(x, int) or not 1 <= x <= dimension for x in sequence):
        raise ValueError("pc word alphabet drift")

    # The canonical PC sequence has increasing generator indices.  Each
    # out-of-order pair g_i g_j (i>j) is replaced by
    # g_j (g_i ^ g_j), and each full relative-order power by its tail.
    for _ in range(1_000_000):
        changed = False
        for position in range(len(sequence) - 1):
            left, right = sequence[position:position + 2]
            if left > right:
                tail = _coords_to_word(conjugates[(left, right)])
                sequence[position:position + 2] = [right] + tail
                changed = True
                break
        if changed:
            continue
        for position, generator in enumerate(sequence):
            index = generator - 1
            order = orders[index]
            run = 0
            while position + run < len(sequence) and sequence[position + run] == generator:
                run += 1
            if run >= order:
                tail = _coords_to_word(power[index])
                sequence[position:position + order] = tail
                changed = True
                break
        if not changed:
            result = [0] * dimension
            for generator in sequence:
                result[generator - 1] += 1
            if any(result[i] >= orders[i] for i in range(dimension)):
                raise ValueError("pc normal form still exceeds relative order")
            return result
    raise ValueError("pc collection did not terminate")


def _pc_inverse_generator(
    index: int,
    orders: list[int],
    power: list[list[int]],
    memo: dict[int, list[int]],
) -> list[int]:
    if index in memo:
        return memo[index]
    # g_i^-1 = g_i^(r_i-1) (g_i^r_i)^-1; the power tail only uses
    # later generators, so this recursion is well-founded for a PCGS.
    tail = _coords_to_word(power[index])
    inverse_tail: list[int] = []
    for generator in reversed(tail):
        inverse_tail.extend(_pc_inverse_generator(
            generator - 1, orders, power, memo))
    result = [index + 1] * (orders[index] - 1) + inverse_tail
    memo[index] = result
    return result


def _pc_inverse_word(
    word: list[int],
    orders: list[int],
    power: list[list[int]],
    memo: dict[int, list[int]],
) -> list[int]:
    result: list[int] = []
    for generator in reversed(word):
        result.extend(_pc_inverse_generator(generator - 1, orders, power, memo))
    return result


def _pc_evaluate(
    word: list[int],
    images: list[list[int]],
    orders: list[int],
    power: list[list[int]],
    conjugates: dict[tuple[int, int], list[int]],
) -> list[int]:
    sequence: list[int] = []
    inverse_memo: dict[int, list[int]] = {}
    for letter in word:
        image = images[abs(letter) - 1]
        image_word = _coords_to_word(image)
        if letter > 0:
            sequence.extend(image_word)
        else:
            sequence.extend(_pc_inverse_word(
                image_word, orders, power, inverse_memo))
    return _pc_normalize(sequence, orders, power, conjugates)


def _pc_is_abelian_pcgs(
    orders: list[int],
    conjugates: dict[tuple[int, int], list[int]],
) -> bool:
    """Strictly recognize a PCGS whose defining conjugates are trivial.

    _pc_contract has already checked coverage, tails, and coordinate bounds.
    Here every relation g_i^g_j = g_i is required literally (the unit vector,
    not merely a zero tail in a selected coordinate).  Only this gate permits
    the additive evaluator below; every other presentation uses the general
    collector.
    """
    dimension = len(orders)
    expected = {(i, j) for i in range(2, dimension + 1)
                for j in range(1, i)}
    if set(conjugates) != expected:
        return False
    for (left, _right), vector in conjugates.items():
        if len(vector) != dimension:
            return False
        if any(value != (1 if index == left - 1 else 0)
               for index, value in enumerate(vector)):
            return False
    return True


def _pc_evaluate_abelian_modular(
    word: list[int],
    images: list[list[int]],
    orders: list[int],
    power: list[list[int]],
) -> list[int]:
    """Evaluate an abelian PC word by additive vectors and power carries.

    The image of a word is first summed in the PC coordinate lattice.  For
    each generator in PC order, divmod applies its relative-order relation
    and carries the quotient through the (strictly later) power tail.  This is
    exact for the abelian gate above, including C9^10 presentations whose
    relative orders are all 3 but whose first ten power rows are nonzero.
    """
    dimension = len(orders)
    vector = [0] * dimension
    for letter in word:
        image = images[abs(letter) - 1]
        sign = 1 if letter > 0 else -1
        for index, coordinate in enumerate(image):
            vector[index] += sign * coordinate
    for index, order in enumerate(orders):
        quotient, remainder = divmod(vector[index], order)
        vector[index] = remainder
        if quotient:
            for tail_index, coordinate in enumerate(power[index]):
                vector[tail_index] += quotient * coordinate
    if any(not 0 <= vector[index] < orders[index]
           for index in range(dimension)):
        raise ValueError("abelian modular vector normalization drift")
    return vector


def verify(receipt_path: Path, input_path: Path, words_path: Path) -> dict[str, Any]:
    relators, norms = load_inputs(input_path, words_path)
    raw_rows, pair_id = build_raw_rs(relators)
    norm_rows: list[list[int]] = []
    for norm in norms:
        mask = 0
        out: list[int] = []
        for letter in norm:
            gen = abs(letter)
            bit = GEN_BITS[gen - 1]
            if letter > 0:
                ident = pair_id[(mask, gen)]
                if ident:
                    out.append(ident)
                mask ^= bit
            else:
                mask ^= bit
                ident = pair_id[(mask, gen)]
                if ident:
                    out.append(-ident)
        if mask != 0:
            raise ValueError("norm leaves the kernel quotient")
        norm_rows.append(free_reduce(out))
    if sha(raw_rows) != RAW_RS_SHA or sha(norm_rows) != NORM_RS_SHA:
        raise ValueError("canonical raw Schreier digest drift")

    receipt_bytes = receipt_path.read_bytes()
    receipt = json.loads(receipt_bytes.decode("utf-8"))
    if receipt.get("schema") != "d972-b4-u-anupq-kernel/v2":
        raise ValueError("receipt schema drift")
    basis = receipt.get("basis_contract", {})
    expected_basis = {
        "basis_id": "regular_c2^5_mask_transversal_v1",
        "coset_count": 32,
        "original_generator_count": 6,
        "rs_generator_count": 161,
        "rs_relator_count": 5056,
        "gen_bits": list(GEN_BITS),
        "transversal": transversal(),
    }
    if basis != expected_basis:
        raise ValueError("raw Schreier basis contract drift")
    expected_digests = {
        "source_sha256": SOURCE_SHA,
        "relator_sha256": RELATOR_SHA,
        "word_artifact_sha256": WORDS_SHA,
        "norm_original_sha256": NORM_SHA,
        "raw_rs_relators_sha256": sha(raw_rows),
        "norm_rs_sha256": sha(norm_rows),
    }
    for key, value in expected_digests.items():
        if receipt.get(key) != value:
            raise ValueError(f"receipt {key} drift")
    if receipt.get("norm_count") != 972:
        raise ValueError("receipt norm count drift")
    if receipt.get("quotient_prime") != 3 or receipt.get("p_quotient_bound") != 4096:
        raise ValueError("p-quotient contract drift")

    classes = receipt.get("classes")
    if not isinstance(classes, list) or not classes:
        raise ValueError("receipt class rows absent")
    requested_classes = receipt.get("requested_classes")
    completed_classes = receipt.get("completed_classes")
    actual_classes = [row.get("class") for row in classes]
    if (not isinstance(requested_classes, list) or
            not requested_classes or
            not isinstance(completed_classes, list) or
            completed_classes != actual_classes or
            any(value not in requested_classes for value in completed_classes)):
        raise ValueError("requested class contract drift")
    defects: list[dict[str, Any]] = []
    abelian_modular_vector_classes = 0
    for row in classes:
        if not isinstance(row, dict) or row.get("status") not in {
            "ALLPASS", "DEFECT", "UNKNOWN_RESOURCE"
        }:
            raise ValueError("receipt class status drift")
        if row["status"] == "UNKNOWN_RESOURCE":
            continue
        images = row.get("quotient_generator_images")
        orders = row.get("pcgs_relative_orders")
        if not isinstance(images, list) or len(images) != 161:
            raise ValueError("quotient generator image basis drift")
        if not isinstance(orders, list) or not all(isinstance(x, int) and x > 0 for x in orders):
            raise ValueError("pcgs order receipt drift")
        if not isinstance(row.get("order"), int) or row["order"] != math.prod(orders):
            raise ValueError("finite quotient order receipt drift")
        for image in images:
            if not isinstance(image, list) or len(image) != len(orders):
                raise ValueError("quotient image vector drift")
            if any(not isinstance(x, int) or not 0 <= x < orders[i]
                   for i, x in enumerate(image)):
                raise ValueError("quotient image coordinate drift")
        power, conjugates = _pc_contract(
            orders, row.get("pcgs_power_relations"),
            row.get("pcgs_conjugate_relations"))
        zero = [0] * len(orders)
        abelian_modular = _pc_is_abelian_pcgs(orders, conjugates)
        if abelian_modular:
            abelian_modular_vector_classes += 1

        def evaluate(word: list[int]) -> list[int]:
            if abelian_modular:
                return _pc_evaluate_abelian_modular(word, images, orders, power)
            return _pc_evaluate(word, images, orders, power, conjugates)

        for index, relator in enumerate(raw_rows):
            if evaluate(relator) != zero:
                raise ValueError(f"quotient map fails RS relator {index}")
        computed_defects: list[tuple[int, list[int]]] = []
        for index, norm_row in enumerate(norm_rows):
            image = evaluate(norm_row)
            if image != zero:
                computed_defects.append((index + 1, image))
        if row.get("bad_count") != len(computed_defects):
            raise ValueError("quotient norm bad-count drift")
        if not isinstance(row.get("bad_count"), int) or row["bad_count"] < 0:
            raise ValueError("bad count drift")
        first = row.get("first_defect")
        if row["status"] == "DEFECT":
            if (not computed_defects or not isinstance(first, dict) or
                    first.get("index") != computed_defects[0][0] or
                    first.get("image") != computed_defects[0][1] or
                    not 1 <= first.get("index", 0) <= 972):
                raise ValueError("first defect receipt drift")
            index = first["index"] - 1
            if first.get("norm_rs") != norm_rows[index]:
                raise ValueError("first defect norm basis drift")
            image = first.get("image")
            if (not isinstance(image, list) or len(image) != len(orders) or
                    any(not isinstance(x, int) or not 0 <= x < orders[i]
                        for i, x in enumerate(image)) or
                    not any(int(x) != 0 for x in image)):
                raise ValueError("first defect image is not nonidentity")
            defects.append({"class": row["class"], "index": first["index"],
                            "image": image})
        elif first is not None or computed_defects:
            raise ValueError("all-pass class unexpectedly carries defect")

    top = receipt.get("status")
    if defects:
        if top != "B4_A_CANDIDATE_P3":
            raise ValueError("defect receipt is not marked candidate")
        status = "B4_A_CANDIDATE_P3_REPLAY_BASIS_CROSSCHECKED"
    else:
        if top not in {"UNKNOWN_P3_BOUNDED", "UNKNOWN_RESOURCE"}:
            raise ValueError("all-pass/resource receipt has terminal status")
        status = "UNKNOWN_P3_ALLPASS_OR_RESOURCE"
    return {
        "schema": "d972-b4-u-anupq-kernel-check/v2",
        "status": status,
        "raw_rs_generators": 161,
        "raw_rs_relators": 5056,
        "norm_count": 972,
        "checked_classes": len(classes),
        "raw_rs_relators_replayed": True,
        "norms_replayed": True,
        "finite_quotient_classes_replayed": sum(
            row.get("status") != "UNKNOWN_RESOURCE" for row in classes),
        "abelian_modular_vector_classes": abelian_modular_vector_classes,
        "defects": defects,
        "receipt_sha256": sha_bytes(receipt_bytes),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt", type=Path, required=True)
    parser.add_argument("--input", type=Path,
                        default=Path("search/certs/d972_b4_p2_magnus_input_v2_20260816.json"))
    parser.add_argument("--words", type=Path,
                        default=Path("search/certs/d972_b4_word_key_artifact_v1_20260816.json"))
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = verify(args.receipt.resolve(), args.input.resolve(), args.words.resolve())
    encoded = json.dumps(result, sort_keys=True, indent=2) + "\n"
    print(encoded, end="")
    if args.output:
        args.output.resolve().write_text(encoded, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
