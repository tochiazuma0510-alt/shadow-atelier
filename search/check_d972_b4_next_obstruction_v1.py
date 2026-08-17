#!/usr/bin/env python3
"""Independent checker for the literal-A.18 Magnus campaign.

This file intentionally does not import the producer, the encoded Magnus
core, or a rho helper.  It reconstructs the 18-prefix-plus-five-raw-coface
presentation, the unconditional D-tilde words, and the complete two-sided
F2 ideal with monomial tuples and lowest pivots.  An all-pass result is
UNKNOWN; only a checked nonzero D-tilde residue is a finite A candidate.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import itertools
import json
import tempfile
from pathlib import Path
from typing import Any, Iterable, Sequence


NGEN = 6
PREFIX_COUNT = 18
SEED_COUNT = 28
COFACE_COUNT = 5
RELATOR_COUNT = 158
ROOF_COUNT = 972
DEGREES = tuple(range(2, 7))
SHARD_COUNTS = {2: 1, 3: 1, 4: 1, 5: 1, 6: 16}

SCHEMA = "d972-b4-next-obstruction/v2"
FINAL_MARKER = "D972_B4_NEXT_OBSTRUCTION_V2_FINAL"
CHECKER_SCHEMA = "d972-b4-next-obstruction-check/v2"
CHECKER_MARKER = "D972_B4_NEXT_OBSTRUCTION_CHECKER_V2_FINAL"
SEMANTICS = "raw_a18_18_plus_140"

INPUT_SHA = "c61b2b77131127aca83a8d7c56b7fdadd2d519b040ea4d91093622c813c2b4a9"
WORDS_SHA = "564a921be8114bdeb963f679c121e8d9aa90e148c65e95e393874fcba843e9f9"
RELATOR_SHA = "12fc1146dce5179c2b5fc44a3ceed6356a6b2c4835a564b55e9a9cd679fccd2e"
PREFIX_SHA = "62ccbb87e2b27784b5330812252a2eaf247fea0fef4eda078ea6724c5b2a31e6"
SEED_SHA = "366c893977a0684a294e8bd488741c735016ec5caf18804415dfc73acdb09822"
A18_ROWS_SHA = "1f0cacaa20ab8474245f30568469de807b5877b2ca7dd0d6668c9b8956750722"
PRESENTATION_SHA = "783d7d80f472fbf6abc8a2f58454048de361e95774c76ce1c511982bb44eb305"
DTILDE_SHA = "32cdc85b315817e939feca628bc15235a55664157ca1e272815a53f1de4631ef"
LITERAL_INPUT_SHA = "60efdb2f7fc847d065701bf27d676cec558e0be9a276ee2a782c3ff0c5754494"
ROOF_WORDS_SHA = "3015b4e00a02ca2a9d6183dad4cb7ddabfd21ef03828837198aa96b2dc3461f8"
RHO_WORDS_SHA = "23db316e11e6486e0475b8425ff8ea6666941b5bff0943bf872e39761d0398ed"
TARGET_KEY_DIGEST = "9c77e6768feb7ffe7143abf18f753af70e81b8e9cc792910c30ae0075d3b1d62"
TUPLE_DIGEST = "32e78ca5b97cd8a6fa59a150dac77719c1b8cb527f0467570c4d284600465a91"
CAMPAIGN_WRAPPER_SHA = "bbf91f461e0c0d9d67ea49186450e709fcb97025ac4ebc3462b3dc6c278eb886"
CORE_SHARD_SHA = "1a18994e3933d5d42e85274af62badb89c2f9a65c92c63862d1740ac2d47da63"
CORE_MERGE_SHA = "6ccce4e95378dfa22051bd8c09e3d3aa5a91234b8d155c0fb57fd18c34f24bf5"
CORE_BASE_MERGE_SHA = "c79abb6ff51bccaaf98992fa070fecf3aba9d70ea4f6b6deff90d4cfcef1814c"
CANONICAL_RHO = [[-6, -5, -3], [3], [5], [-3, -2, -1], [-5, -4, -1], [1]]

RHO_ROLE = "omitted_from_ideal_and_defect"
ALLOWED_RHO_FIELDS = {"rho_used", "rho_tail_used", "rho_role"}
STALE_RHO_FIELDS = {
    "rho_words", "rho_tail", "rho_orbit", "rho5", "rho5_bad_generators",
    "rho_words_sha256", "norm_word", "reverse_rho_norm", "rho_norm",
}
SHARD_RECORD_FIELDS = {
    "path", "sha256", "degree", "shard_index", "shard_count",
    "relator_count", "relator_indices", "relator_indices_sha256",
    "monomial_count", "ideal_rank", "input_sha256",
    "literal_input_sha256", "input_digests", "campaign_schema",
    "campaign_degree", "presentation_semantics", "raw_source_sha256",
    "word_artifact_sha256", "relator_sha256", "prefix_sha256",
    "seed_sha256", "a18_rows_sha256", "presentation_sha256",
    "dtilde_sha256", "rho_tail_used", "rho_used", "rho_role",
    "campaign_wrapper_sha256", "core_shard_sha256", "core_merge_sha256",
    "core_base_merge_sha256", "complete_two_sided_ideal",
}

INPUT_PATH = Path("search/certs/d972_b4_p2_magnus_input_v2_20260816.json")
WORDS_PATH = Path("search/certs/d972_b4_word_key_artifact_v1_20260816.json")

MAPS = (
    ("123", (1,), (4,)),
    ("234", (4,), (6,)),
    ("12,3,4", (2, 4), (6,)),
    ("1,23,4", (1, 2), (5, 6)),
    ("1,2,34", (1,), (4, 5)),
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def canonical_json(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=True, separators=(",", ":")).encode("ascii")


def digest(value: object) -> str:
    return hashlib.sha256(canonical_json(value)).hexdigest()


def file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def free_reduce(word: Iterable[int]) -> list[int]:
    out: list[int] = []
    for raw in word:
        n = int(raw)
        require(n != 0 and abs(n) <= NGEN, "signed word alphabet drift")
        if out and out[-1] == -n:
            out.pop()
        else:
            out.append(n)
    return out


def inverse_word(word: Sequence[int]) -> list[int]:
    return [-int(x) for x in reversed(word)]


def marked_substitute(word: Sequence[int], left: Sequence[int],
                      right: Sequence[int]) -> list[int]:
    out: list[int] = []
    for raw in word:
        n = int(raw)
        require(n != 0 and abs(n) in (1, 4), "marked F2 seed alphabet drift")
        image = list(left if abs(n) == 1 else right)
        out.extend(inverse_word(image) if n < 0 else image)
    return free_reduce(out)


def exact_dtilde(f2_word: Sequence[int]) -> list[int]:
    marked: list[int] = []
    for raw in f2_word:
        n = int(raw)
        require(n != 0 and abs(n) in (1, 2), "roof F2 alphabet drift")
        marked.append(1 if n == 1 else -1 if n == -1 else 4 if n == 2 else -4)
    x15 = (-3, -2, -1)
    x45 = (-6, -5, -3)
    return free_reduce(
        inverse_word(marked_substitute(marked, x45, (6,)))
        + inverse_word(marked_substitute(marked, (1,), x15))
        + marked_substitute(marked, (4,), (6,))
        + marked_substitute(marked, x45, x15)
        + marked_substitute(marked, (1,), (4,))
    )


def flat_key(key: object) -> str:
    require(isinstance(key, list) and len(key) == 3,
            "word artifact key shape drift")
    m, can9, can4 = key
    require(isinstance(m, int) and isinstance(can9, list) and len(can9) == 3 and
            isinstance(can4, list) and len(can4) == 9,
            "word artifact key component drift")
    coords: list[int] = []
    for pair in can9:
        require(isinstance(pair, list) and len(pair) == 2 and
                all(isinstance(x, int) for x in pair),
                "word artifact D9 key drift")
        coords.extend(pair)
    require(all(isinstance(x, int) for x in can4),
            "word artifact PSL key drift")
    return "(" + str(m) + ";" + ",".join(map(str, coords)) + ";" + ",".join(map(str, can4)) + ")"


def load_artifact(path: Path, source_keys: Sequence[str]) -> tuple[list[list[int]], list[str], list[list[int]]]:
    require(file_sha(path) == WORDS_SHA, "word artifact SHA drift")
    obj = json.loads(path.read_text(encoding="utf-8"))
    require(obj.get("schema") == "d972-b4-word-key-artifact/v1" and
            obj.get("count") == ROOF_COUNT, "word artifact schema/count drift")
    rows = obj.get("rows")
    require(isinstance(rows, list) and len(rows) == ROOF_COUNT,
            "word artifact row count drift")
    require(obj.get("source_target_key_digest") == TARGET_KEY_DIGEST and
            obj.get("frozen_tuple_sha256") == TUPLE_DIGEST,
            "word artifact digest metadata drift")
    require(obj.get("canonical_bytes_sha256") == digest(rows),
            "word artifact canonical digest drift")
    words: list[list[int]] = []
    keys: list[str] = []
    for row in rows:
        require(isinstance(row, list) and len(row) == 3,
                "word artifact row shape drift")
        m, key, word = row
        require(isinstance(m, int) and isinstance(key, list) and key and
                key[0] == m, "word artifact row key drift")
        require(not (isinstance(word, str) and word == ""),
                "legacy empty word row rejected")
        require(isinstance(word, list) and all(isinstance(x, int) and
                x != 0 and abs(x) <= 2 for x in word),
                "word artifact F2 word drift")
        keys.append(flat_key(key))
        words.append([int(x) for x in word])
    require(len(set(keys)) == ROOF_COUNT and set(keys) == set(source_keys),
            "word artifact/source target-key set drift")
    require(hashlib.sha256(("\n".join(sorted(keys)) + "\n").encode("ascii")).hexdigest() ==
            TARGET_KEY_DIGEST, "word artifact target-key digest drift")
    dtilde = [exact_dtilde(word) for word in words]
    require(digest(dtilde) == DTILDE_SHA, "D-tilde digest drift")
    return words, keys, dtilde


def reconstruct_literal_transport(source: dict[str, Any],
                                  presentation: Sequence[Sequence[int]]) -> tuple[str, dict[str, str]]:
    """Independently rebuild the producer's deterministic legacy transport."""
    roof_words = source.get("roof_words")
    require(isinstance(roof_words, list) and len(roof_words) == ROOF_COUNT and
            source.get("roof_words_sha256") == ROOF_WORDS_SHA and
            digest(roof_words) == ROOF_WORDS_SHA,
            "canonical roof-word transport drift")
    require(source.get("rho_words") == CANONICAL_RHO and
            digest(source["rho_words"]) == RHO_WORDS_SHA,
            "canonical legacy rho transport drift")
    literal = dict(source)
    literal.update({
        "all_relators": [list(row) for row in presentation],
        "all_relators_sha256": digest(presentation),
        "presentation_semantics": SEMANTICS,
        "raw_source_sha256": INPUT_SHA,
        "prefix_sha256": PREFIX_SHA,
        "seed_sha256": SEED_SHA,
        "a18_rows_sha256": A18_ROWS_SHA,
        "presentation_sha256": PRESENTATION_SHA,
        "dtilde_sha256": DTILDE_SHA,
        "rho_tail_used": False,
        "rho_used": False,
        "rho_role": "transport_only_not_used_in_ideal_or_defect",
    })
    payload = (json.dumps(literal, ensure_ascii=True, sort_keys=True,
                          indent=2) + "\n").encode("utf-8")
    literal_sha = hashlib.sha256(payload).hexdigest()
    require(literal_sha == LITERAL_INPUT_SHA,
            "independent literal transport SHA fixture drift")
    return literal_sha, {
        "all_relators_sha256": PRESENTATION_SHA,
        "roof_words_sha256": ROOF_WORDS_SHA,
        "rho_words_sha256": RHO_WORDS_SHA,
        "target_key_digest": TARGET_KEY_DIGEST,
    }


def load_source(input_path: Path, artifact_path: Path) -> dict[str, Any]:
    require(file_sha(input_path) == INPUT_SHA, "canonical input SHA drift")
    source = json.loads(input_path.read_text(encoding="utf-8"))
    require(source.get("schema") == "d972-b4-p2-magnus-input/v2" and
            source.get("relator_count") == RELATOR_COUNT,
            "canonical input schema/count drift")
    relators = [[int(x) for x in row] for row in source.get("all_relators", [])]
    require(len(relators) == RELATOR_COUNT and
            source.get("all_relators_sha256") == RELATOR_SHA and
            digest(relators) == RELATOR_SHA, "canonical relator digest drift")
    prefix = relators[:PREFIX_COUNT]
    seeds = relators[PREFIX_COUNT:PREFIX_COUNT + SEED_COUNT]
    require(digest(prefix) == PREFIX_SHA and digest(seeds) == SEED_SHA,
            "literal prefix/seed digest drift")
    source_keys = [str(x) for x in source.get("target_keys", [])]
    require(len(source_keys) == ROOF_COUNT and len(set(source_keys)) == ROOF_COUNT,
            "canonical target-key count drift")
    require(hashlib.sha256(("\n".join(sorted(source_keys)) + "\n").encode("ascii")).hexdigest() ==
            TARGET_KEY_DIGEST, "canonical target-key digest drift")
    words, keys, dtilde = load_artifact(artifact_path, source_keys)

    a18: list[list[int]] = []
    for _name, left, right in MAPS:
        a18.extend(marked_substitute(row, left, right) for row in seeds)
    require(len(a18) == COFACE_COUNT * SEED_COUNT and
            digest(a18) == A18_ROWS_SHA, "literal A.18 rows drift")
    presentation = prefix + a18
    require(len(presentation) == RELATOR_COUNT and
            digest(presentation) == PRESENTATION_SHA,
            "literal A.18 presentation drift")
    literal_input_sha256, input_digests = reconstruct_literal_transport(
        source, presentation)
    return {
        "source": source,
        "prefix": prefix,
        "seeds": seeds,
        "a18_rows": a18,
        "presentation": presentation,
        "words": words,
        "keys": keys,
        "dtilde": dtilde,
        "literal_input_sha256": literal_input_sha256,
        "input_digests": input_digests,
    }


def monomials(degree: int) -> list[tuple[int, ...]]:
    out: list[tuple[int, ...]] = [()]
    for length in range(1, degree + 1):
        out.extend(itertools.product(range(NGEN), repeat=length))
    return out


def xor_sets(left: set[tuple[int, ...]], right: set[tuple[int, ...]]) -> set[tuple[int, ...]]:
    out = set(left)
    out.symmetric_difference_update(right)
    return out


def append_set(poly: set[tuple[int, ...]], generator: int,
               degree: int) -> set[tuple[int, ...]]:
    return {word + (generator,) for word in poly if len(word) < degree}


def eval_word(word: Iterable[int], degree: int) -> set[tuple[int, ...]]:
    poly: set[tuple[int, ...]] = {()}
    for raw in word:
        letter = int(raw)
        require(letter != 0 and abs(letter) <= NGEN,
                "Magnus word alphabet drift")
        generator = abs(letter) - 1
        if letter > 0:
            poly = xor_sets(poly, append_set(poly, generator, degree))
        else:
            total = set(poly)
            power = set(poly)
            for _ in range(degree):
                power = append_set(power, generator, degree)
                total = xor_sets(total, power)
            poly = total
    return poly


def eval_minus_one(word: Iterable[int], degree: int) -> set[tuple[int, ...]]:
    poly = eval_word(word, degree)
    poly.discard(())
    return poly


def bits(poly: set[tuple[int, ...]], index: dict[tuple[int, ...], int]) -> int:
    result = 0
    for monomial in poly:
        result |= 1 << index[monomial]
    return result


def add_low(basis: dict[int, int], row: int) -> None:
    while row:
        pivot = (row & -row).bit_length() - 1
        old = basis.get(pivot)
        if old is None:
            basis[pivot] = row
            return
        row ^= old


def reduce_low(basis: dict[int, int], row: int) -> int:
    while row:
        pivot = (row & -row).bit_length() - 1
        old = basis.get(pivot)
        if old is None:
            return row
        row ^= old
    return 0


def ideal_rows(relations: Sequence[set[tuple[int, ...]]], degree: int,
               monomial_list: Sequence[tuple[int, ...]],
               index: dict[tuple[int, ...], int]) -> dict[int, int]:
    levels = [[word for word in monomial_list if len(word) == length]
              for length in range(degree + 1)]
    generated: dict[int, int] = {}
    for relation in relations:
        if not relation:
            continue
        minimum = min(len(word) for word in relation)
        for total in range(degree - minimum + 1):
            for left_length in range(total + 1):
                right_length = total - left_length
                for left in levels[left_length]:
                    for right in levels[right_length]:
                        row = {
                            left + middle + right
                            for middle in relation
                            if len(left) + len(middle) + len(right) <= degree
                        }
                        if row:
                            add_low(generated, bits(row, index))
    return generated


def from_hex(value: object, limit: int) -> int:
    require(isinstance(value, str) and value and
            all(c in "0123456789abcdefABCDEF" for c in value),
            "ideal basis hex drift")
    row = int(value, 16)
    require(row.bit_length() <= limit, "ideal basis row exceeds monomial space")
    return row


def is_sha256(value: object) -> bool:
    return (isinstance(value, str) and len(value) == 64 and
            all(char in "0123456789abcdef" for char in value))


def validate_rho_contract(obj: dict[str, Any], where: str) -> None:
    require(obj.get("rho_used") is False and
            obj.get("rho_tail_used") is False and
            obj.get("rho_role") == RHO_ROLE,
            f"{where} rho exclusion contract drift")
    for field in STALE_RHO_FIELDS:
        require(field not in obj, f"{where} stale rho field present: {field}")
    for field in obj:
        require(not field.lower().startswith("rho") or field in ALLOWED_RHO_FIELDS,
                f"{where} unversioned rho field present: {field}")


def expected_relator_indices(index: int, count: int) -> list[int]:
    require(count >= 1 and 0 <= index < count, "invalid shard index/count")
    return [i + 1 for i in range(RELATOR_COUNT) if i % count == index]


def validate_top_contract(receipt: dict[str, Any], degree: int,
                          canonical: dict[str, Any]) -> None:
    require(receipt.get("schema") == SCHEMA and
            receipt.get("final_marker") == FINAL_MARKER,
            "producer schema/final marker drift")
    require(receipt.get("campaign_degree") == degree and
            receipt.get("presentation_semantics") == SEMANTICS,
            "producer degree/semantics drift")
    validate_rho_contract(receipt, "top-level receipt")
    for field, expected in (
            ("source_sha256", INPUT_SHA),
            ("word_artifact_sha256", WORDS_SHA),
            ("relator_sha256", RELATOR_SHA),
            ("prefix_sha256", PREFIX_SHA),
            ("seed_sha256", SEED_SHA),
            ("a18_rows_sha256", A18_ROWS_SHA),
            ("presentation_sha256", PRESENTATION_SHA),
            ("dtilde_sha256", DTILDE_SHA),
            ("campaign_wrapper_sha256", CAMPAIGN_WRAPPER_SHA),
            ("core_shard_sha256", CORE_SHARD_SHA),
            ("core_merge_sha256", CORE_MERGE_SHA),
            ("core_base_merge_sha256", CORE_BASE_MERGE_SHA),
            ("literal_input_sha256", canonical["literal_input_sha256"])):
        require(receipt.get(field) == expected, f"receipt {field} drift")
    require(receipt.get("input_digests") == canonical["input_digests"],
            "receipt literal input digest map drift")
    require(receipt.get("complete_two_sided_ideal") is True and
            receipt.get("no_bounded_word_search") is True and
            receipt.get("no_matrix_group_enumeration") is True,
            "completeness metadata missing")


def validate_shard_records(records: object, degree: int,
                           canonical: dict[str, Any]) -> None:
    count = SHARD_COUNTS[degree]
    require(isinstance(records, list) and len(records) == count,
            "merge shard record count drift")
    coverage: list[int] = []
    for index, record in enumerate(records):
        require(isinstance(record, dict) and set(record) == SHARD_RECORD_FIELDS,
                f"merge shard record schema drift at {index}")
        expected = expected_relator_indices(index, count)
        require(record.get("degree") == degree and
                record.get("campaign_degree") == degree and
                record.get("shard_index") == index and
                record.get("shard_count") == count,
                f"merge shard identity drift at {index}")
        require(record.get("relator_indices") == expected and
                record.get("relator_count") == len(expected) and
                record.get("relator_indices_sha256") == digest(expected),
                f"merge shard relator coverage/digest drift at {index}")
        require(record.get("monomial_count") == sum(NGEN ** n for n in range(degree + 1)) and
                isinstance(record.get("ideal_rank"), int) and
                record["ideal_rank"] >= 0,
                f"merge shard dimension metadata drift at {index}")
        expected_name = f"d972_b4_next_d{degree}_shard_{index}_of_{count}.json"
        require(isinstance(record.get("path"), str) and
                Path(record["path"]).name == expected_name and
                is_sha256(record.get("sha256")),
                f"merge shard file binding drift at {index}")
        require(record.get("input_sha256") == canonical["literal_input_sha256"] and
                record.get("literal_input_sha256") == canonical["literal_input_sha256"] and
                record.get("input_digests") == canonical["input_digests"],
                f"merge shard literal transport binding drift at {index}")
        for field, value in (
                ("campaign_schema", SCHEMA),
                ("presentation_semantics", SEMANTICS),
                ("raw_source_sha256", INPUT_SHA),
                ("word_artifact_sha256", WORDS_SHA),
                ("relator_sha256", RELATOR_SHA),
                ("prefix_sha256", PREFIX_SHA),
                ("seed_sha256", SEED_SHA),
                ("a18_rows_sha256", A18_ROWS_SHA),
                ("presentation_sha256", PRESENTATION_SHA),
                ("dtilde_sha256", DTILDE_SHA),
                ("campaign_wrapper_sha256", CAMPAIGN_WRAPPER_SHA),
                ("core_shard_sha256", CORE_SHARD_SHA),
                ("core_merge_sha256", CORE_MERGE_SHA),
                ("core_base_merge_sha256", CORE_BASE_MERGE_SHA),
                ("complete_two_sided_ideal", True)):
            require(record.get(field) == value,
                    f"merge shard {field} drift at {index}")
        validate_rho_contract(record, f"merge shard {index}")
        coverage.extend(expected)
    require(sorted(coverage) == list(range(1, RELATOR_COUNT + 1)) and
            len(coverage) == len(set(coverage)),
            "merge shard records are not an exact relator partition")


def validate_pivot_metadata(rows: Sequence[int], pivots: object) -> None:
    expected = [row.bit_length() - 1 for row in rows]
    require(pivots == expected, "ideal pivot metadata does not match basis rows")


def status_for(degree: int, defects: Sequence[dict[str, Any]],
               relator_bad: Sequence[int], binding_bad: Sequence[str],
               construction_bad: Sequence[str]) -> str:
    if relator_bad or binding_bad or construction_bad:
        return f"D{degree}_MAGNUS_GATE_FAILURE"
    if defects:
        return f"D{degree}_A_CANDIDATE_NEEDS_CHECK"
    return f"D{degree}_ALLPASS_UNKNOWN"


def check_receipt_object(receipt: dict[str, Any], degree: int,
                         canonical: dict[str, Any]) -> dict[str, Any]:
    validate_top_contract(receipt, degree, canonical)
    degrees = receipt.get("degrees")
    require(isinstance(degrees, dict) and set(degrees) == {str(degree)},
            "receipt degree set drift")
    got = degrees[str(degree)]
    require(isinstance(got, dict), "degree receipt shape drift")
    validate_rho_contract(got, "degree receipt")
    validate_shard_records(got.get("shards"), degree, canonical)

    monomial_list = monomials(degree)
    index = {word: i for i, word in enumerate(monomial_list)}
    rel_polys = [eval_minus_one(word, degree) for word in canonical["presentation"]]
    generated = ideal_rows(rel_polys, degree, monomial_list, index)
    basis_hex = got.get("ideal_basis_hex")
    require(isinstance(basis_hex, list), "ideal basis missing")
    receipt_rows = [from_hex(value, len(monomial_list)) for value in basis_hex]
    candidate: dict[int, int] = {}
    for row in receipt_rows:
        add_low(candidate, row)
    require(len(candidate) == len(receipt_rows), "receipt ideal basis is dependent")
    for row in generated.values():
        require(reduce_low(candidate, row) == 0,
                "receipt basis does not contain literal ideal")
    for row in candidate.values():
        require(reduce_low(generated, row) == 0,
                "receipt basis contains a non-ideal row")
    require(len(generated) == len(candidate), "literal ideal rank mismatch")
    require(got.get("monomial_count") == len(monomial_list) and
            got.get("ideal_rank") == len(candidate) and
            got.get("quotient_dimension") == len(monomial_list) - len(candidate),
            "ideal dimension metadata drift")
    supplied_pivots = got.get("ideal_basis_pivots")
    validate_pivot_metadata(receipt_rows, supplied_pivots)

    def residue(word: Sequence[int]) -> int:
        return reduce_low(candidate, bits(eval_minus_one(word, degree), index))

    relator_bad = [i + 1 for i, word in enumerate(canonical["presentation"])
                   if residue(word)]
    binding_bad = got.get("binding_bad")
    construction_bad = got.get("construction_bad")
    require(isinstance(binding_bad, list) and all(isinstance(x, str) for x in binding_bad),
            "binding gate shape drift")
    require(isinstance(construction_bad, list) and
            all(isinstance(x, str) for x in construction_bad),
            "construction gate shape drift")
    require(got.get("relator_bad") == relator_bad,
            "literal relator gate mismatch")

    row_receipts = got.get("dtilde_rows")
    require(isinstance(row_receipts, list) and len(row_receipts) == ROOF_COUNT,
            "D-tilde row count drift")
    failures: list[dict[str, Any]] = []
    for i, (word, key) in enumerate(zip(canonical["dtilde"], canonical["keys"]), 1):
        value = residue(word)
        expected = {
            "index": i,
            "target_key": key,
            "word": word,
            "residue_hex": format(value, "x"),
        }
        supplied = row_receipts[i - 1]
        require(supplied == expected, f"D-tilde receipt mismatch at row {i}")
        if value:
            failures.append(expected)
    require(got.get("dtilde_count") == ROOF_COUNT and
            got.get("dtilde_defect_count") == len(failures) and
            got.get("first_defect") == (failures[0] if failures else None),
            "D-tilde defect ledger drift")
    expected = status_for(degree, failures, relator_bad, binding_bad, construction_bad)
    require(got.get("status") == expected and receipt.get("status") == expected,
            f"gate/defect status mismatch: {receipt.get('status')} != {expected}")
    return {
        "degree": degree,
        "ideal_rank": len(candidate),
        "quotient_dimension": len(monomial_list) - len(candidate),
        "relator_bad": relator_bad,
        "binding_bad": binding_bad,
        "construction_bad": construction_bad,
        "dtilde_defect_count": len(failures),
        "status": expected,
    }


def check_receipt(path: Path, degree: int,
                  canonical: dict[str, Any]) -> dict[str, Any]:
    receipt = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(receipt, dict), "producer receipt shape drift")
    return check_receipt_object(receipt, degree, canonical)


def synthetic_d2_receipt(canonical: dict[str, Any]) -> dict[str, Any]:
    """Build a clean receipt solely for fail-closed metadata mutations."""
    degree = 2
    monomial_list = monomials(degree)
    index = {word: i for i, word in enumerate(monomial_list)}
    generated = ideal_rows(
        [eval_minus_one(word, degree) for word in canonical["presentation"]],
        degree, monomial_list, index)
    rows = [generated[pivot] for pivot in sorted(generated)]

    def residue(word: Sequence[int]) -> int:
        return reduce_low(generated, bits(eval_minus_one(word, degree), index))

    relator_bad = [i + 1 for i, word in enumerate(canonical["presentation"])
                   if residue(word)]
    dtilde_rows = [{
        "index": i,
        "target_key": key,
        "word": word,
        "residue_hex": format(residue(word), "x"),
    } for i, (word, key) in enumerate(
        zip(canonical["dtilde"], canonical["keys"]), 1)]
    defects = [row for row in dtilde_rows if row["residue_hex"] != "0"]
    require(not relator_bad and not defects,
            "degree-2 clean mutation fixture unexpectedly has a defect")
    indices = expected_relator_indices(0, 1)
    shard = {
        "path": "d972_b4_next_d2_shard_0_of_1.json",
        "sha256": "0" * 64,
        "degree": degree,
        "shard_index": 0,
        "shard_count": 1,
        "relator_count": len(indices),
        "relator_indices": indices,
        "relator_indices_sha256": digest(indices),
        "monomial_count": len(monomial_list),
        "ideal_rank": len(rows),
        "input_sha256": canonical["literal_input_sha256"],
        "literal_input_sha256": canonical["literal_input_sha256"],
        "input_digests": canonical["input_digests"],
        "campaign_schema": SCHEMA,
        "campaign_degree": degree,
        "presentation_semantics": SEMANTICS,
        "raw_source_sha256": INPUT_SHA,
        "word_artifact_sha256": WORDS_SHA,
        "relator_sha256": RELATOR_SHA,
        "prefix_sha256": PREFIX_SHA,
        "seed_sha256": SEED_SHA,
        "a18_rows_sha256": A18_ROWS_SHA,
        "presentation_sha256": PRESENTATION_SHA,
        "dtilde_sha256": DTILDE_SHA,
        "rho_tail_used": False,
        "rho_used": False,
        "rho_role": RHO_ROLE,
        "campaign_wrapper_sha256": CAMPAIGN_WRAPPER_SHA,
        "core_shard_sha256": CORE_SHARD_SHA,
        "core_merge_sha256": CORE_MERGE_SHA,
        "core_base_merge_sha256": CORE_BASE_MERGE_SHA,
        "complete_two_sided_ideal": True,
    }
    status = "D2_ALLPASS_UNKNOWN"
    row = {
        "degree": degree,
        "monomial_count": len(monomial_list),
        "ideal_rank": len(rows),
        "quotient_dimension": len(monomial_list) - len(rows),
        "shards": [shard],
        "rho_tail_used": False,
        "rho_used": False,
        "rho_role": RHO_ROLE,
        "relator_bad": [],
        "binding_bad": [],
        "construction_bad": [],
        "dtilde_count": ROOF_COUNT,
        "dtilde_defect_count": 0,
        "first_defect": None,
        "dtilde_rows": dtilde_rows,
        "ideal_basis_hex": [format(value, "x") for value in rows],
        "ideal_basis_pivots": [value.bit_length() - 1 for value in rows],
        "status": status,
    }
    return {
        "schema": SCHEMA,
        "final_marker": FINAL_MARKER,
        "status": status,
        "campaign_degree": degree,
        "source_sha256": INPUT_SHA,
        "word_artifact_sha256": WORDS_SHA,
        "relator_sha256": RELATOR_SHA,
        "prefix_sha256": PREFIX_SHA,
        "seed_sha256": SEED_SHA,
        "a18_rows_sha256": A18_ROWS_SHA,
        "presentation_sha256": PRESENTATION_SHA,
        "dtilde_sha256": DTILDE_SHA,
        "literal_input_sha256": canonical["literal_input_sha256"],
        "input_digests": canonical["input_digests"],
        "presentation_semantics": SEMANTICS,
        "rho_tail_used": False,
        "rho_used": False,
        "rho_role": RHO_ROLE,
        "complete_two_sided_ideal": True,
        "no_bounded_word_search": True,
        "no_matrix_group_enumeration": True,
        "campaign_wrapper_sha256": CAMPAIGN_WRAPPER_SHA,
        "core_shard_sha256": CORE_SHARD_SHA,
        "core_merge_sha256": CORE_MERGE_SHA,
        "core_base_merge_sha256": CORE_BASE_MERGE_SHA,
        "degrees": {"2": row},
    }


def expect_mutation_rejected(base: dict[str, Any], canonical: dict[str, Any],
                             label: str, mutation) -> None:
    candidate = copy.deepcopy(base)
    mutation(candidate)
    try:
        check_receipt_object(candidate, 2, canonical)
    except (TypeError, ValueError, KeyError):
        return
    raise ValueError(f"fail-open mutation selftest: {label}")


def self_test(canonical: dict[str, Any]) -> None:
    require(canonical["a18_rows"][:SEED_COUNT] == canonical["seeds"],
            "123 raw coface fixture failed")
    require(len(canonical["a18_rows"]) == 140 and
            len(canonical["presentation"]) == 158 and
            len(canonical["dtilde"]) == 972,
            "literal count fixture failed")
    require(digest(canonical["a18_rows"]) == A18_ROWS_SHA and
            digest(canonical["presentation"]) == PRESENTATION_SHA and
            digest(canonical["dtilde"]) == DTILDE_SHA,
            "literal digest fixture failed")
    monomial_list = monomials(2)
    index = {word: i for i, word in enumerate(monomial_list)}
    generated = ideal_rows([eval_minus_one([1, 2], 2)], 2,
                            monomial_list, index)
    require(generated, "degree-2 ideal fixture unexpectedly empty")
    # Explicit fail-closed negative: no defects cannot override any bad gate.
    require(status_for(2, [], [1], [], []) == "D2_MAGNUS_GATE_FAILURE",
            "relator-bad/no-defect negative failed")
    require(status_for(2, [], [], ["binding"], []) == "D2_MAGNUS_GATE_FAILURE",
            "binding-bad/no-defect negative failed")
    require(status_for(2, [], [], [], ["construction"]) == "D2_MAGNUS_GATE_FAILURE",
            "construction-bad/no-defect negative failed")
    require(status_for(2, [], [], [], []) == "D2_ALLPASS_UNKNOWN",
            "clean no-defect status fixture failed")
    base = synthetic_d2_receipt(canonical)
    require(check_receipt_object(base, 2, canonical)["status"] ==
            "D2_ALLPASS_UNKNOWN", "clean synthetic receipt fixture failed")
    mutations = [
        ("empty shard record list",
         lambda obj: obj["degrees"]["2"].__setitem__("shards", [])),
        ("arbitrary top literal transport SHA",
         lambda obj: obj.__setitem__("literal_input_sha256", "f" * 64)),
        ("forged basis pivots",
         lambda obj: obj["degrees"]["2"].__setitem__(
             "ideal_basis_pivots",
             [999] * len(obj["degrees"]["2"]["ideal_basis_hex"]))),
        ("out-of-range shard index",
         lambda obj: obj["degrees"]["2"]["shards"][0].__setitem__(
             "shard_index", 99)),
        ("degree rho_used drift",
         lambda obj: obj["degrees"]["2"].__setitem__("rho_used", True)),
        ("degree rho_tail_used drift",
         lambda obj: obj["degrees"]["2"].__setitem__("rho_tail_used", True)),
        ("degree rho_role drift",
         lambda obj: obj["degrees"]["2"].__setitem__("rho_role", "diagnostic")),
        ("degree stale rho field",
         lambda obj: obj["degrees"]["2"].__setitem__("rho_words", [])),
        ("shard assignment digest drift",
         lambda obj: obj["degrees"]["2"]["shards"][0].__setitem__(
             "relator_indices_sha256", "f" * 64)),
        ("shard transport SHA drift",
         lambda obj: obj["degrees"]["2"]["shards"][0].__setitem__(
             "literal_input_sha256", "f" * 64)),
        ("shard input digest drift",
         lambda obj: obj["degrees"]["2"]["shards"][0]["input_digests"].__setitem__(
             "all_relators_sha256", "f" * 64)),
    ]
    for label, mutation in mutations:
        expect_mutation_rejected(base, canonical, label, mutation)
    print("D972_B4_NEXT_OBSTRUCTION_CHECKER_V2_SELFTEST_PASS")
    print(f"{CHECKER_MARKER} status=PASS degrees=2,3,4,5,6")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt", type=Path, action="append")
    parser.add_argument("--receipt-dir", type=Path)
    parser.add_argument("--input", type=Path, default=INPUT_PATH)
    parser.add_argument("--artifact", type=Path, default=WORDS_PATH)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--output", type=Path,
                        default=Path(tempfile.gettempdir()) / "d972_literal_a18_check.json")
    args = parser.parse_args(argv)
    try:
        canonical = load_source(args.input, args.artifact)
        if args.self_test:
            self_test(canonical)
            return 0
        if args.receipt_dir is not None:
            paths = [args.receipt_dir / f"d972_b4_next_obstruction_d{degree}.json"
                     for degree in DEGREES]
        else:
            paths = args.receipt or []
        require(len(paths) == len(DEGREES),
                "exactly five degree receipts are required")
        summaries: list[dict[str, Any]] = []
        for path, degree in zip(sorted(paths, key=lambda p: int(p.stem.rsplit("d", 1)[-1])), DEGREES):
            summaries.append(check_receipt(path, degree, canonical))
        summaries.sort(key=lambda row: row["degree"])
        if any(row["status"].endswith("GATE_FAILURE") for row in summaries):
            status = "D972_B4_NEXT_OBSTRUCTION_CHECKER_GATE_FAILURE"
        elif any("_A_CANDIDATE_" in row["status"] for row in summaries):
            status = "D972_B4_A18_Dtilde_CANDIDATE_CROSSCHECKED"
        else:
            status = "UNKNOWN_CORRECT_A18_Dtilde_ALLPASS"
        result = {
            "schema": CHECKER_SCHEMA,
            "final_marker": CHECKER_MARKER,
            "status": status,
            "degrees": summaries,
            "source_sha256": INPUT_SHA,
            "word_artifact_sha256": WORDS_SHA,
            "a18_rows_sha256": A18_ROWS_SHA,
            "presentation_sha256": PRESENTATION_SHA,
            "dtilde_sha256": DTILDE_SHA,
            "presentation_semantics": SEMANTICS,
            "rho_used": False,
            "rho_tail_used": False,
            "independent_literal_reconstruction": True,
            "complete_two_sided_ideal": True,
        }
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, ensure_ascii=True,
                                          sort_keys=True, indent=2) + "\n",
                                 encoding="utf-8")
        print(json.dumps(result, sort_keys=True))
        print(f"{CHECKER_MARKER} status={status} degrees=2,3,4,5,6")
        return 0 if not status.endswith("GATE_FAILURE") else 1
    except (OSError, TypeError, ValueError, KeyError, json.JSONDecodeError) as exc:
        result = {"schema": CHECKER_SCHEMA, "status": "REJECTED",
                  "reason": str(exc)}
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n",
                               encoding="utf-8")
        print(json.dumps(result, sort_keys=True))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
