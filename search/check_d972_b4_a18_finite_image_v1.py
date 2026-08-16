"""Independent checker for raw-A.18 finite-image receipts.

This checker deliberately does not import a GAP producer.  It rebuilds the
five literal A.18 substitutions, the 18+140 presentation, and the 972
unconditional D-tilde words from the two pinned artifacts.  A receipt is
accepted only when its six marked K(0,5) generator images are a complete
permutation-group epimorphism and every raw presentation relator is replayed
to one.  A nontrivial D-tilde image is a finite-image candidate only; an
all-pass finite search is UNKNOWN.

The generator order in a receipt is
    (x45, x14, x24, x15, x25, x12).
No rho-tail, rho orbit, or self-asserted B4 label is part of this schema.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, Iterable


SOURCE_SHA = "c61b2b77131127aca83a8d7c56b7fdadd2d519b040ea4d91093622c813c2b4a9"
WORDS_SHA = "564a921be8114bdeb963f679c121e8d9aa90e148c65e95e393874fcba843e9f9"
RELATOR_SHA = "12fc1146dce5179c2b5fc44a3ceed6356a6b2c4835a564b55e9a9cd679fccd2e"
A18_ROWS_SHA = "1f0cacaa20ab8474245f30568469de807b5877b2ca7dd0d6668c9b8956750722"
PRESENTATION_SHA = "783d7d80f472fbf6abc8a2f58454048de361e95774c76ce1c511982bb44eb305"
DTILDE_SHA = "32cdc85b315817e939feca628bc15235a55664157ca1e272815a53f1de4631ef"

INPUT_PATH = Path("search/certs/d972_b4_p2_magnus_input_v2_20260816.json")
WORDS_PATH = Path("search/certs/d972_b4_word_key_artifact_v1_20260816.json")
SCHEMA = "d972-b4-a18-finite-image/v1"
SEMANTICS = "raw_a18_18_plus_140"
GENERATOR_ORDER = ("x45", "x14", "x24", "x15", "x25", "x12")
FINAL_MARKER = "D972_B4_A18_FINITE_IMAGE_V1_FINAL"

# Fixed target shelf.  The order is independently checked from the six
# permutation images, so a label cannot turn an arbitrary subgroup into an
# accepted target.  The two PSL/PGL 8 entries are useful small-degree shelves;
# the remaining entries mirror the existing finite-group shelves.
TARGET_ORDERS = {
    "S3": 6,
    "S4": 24,
    "A4": 12,
    "A5": 60,
    "D10": 10,
    "D14": 14,
    "D18": 18,
    "D22": 22,
    "D26": 26,
    "PSL2_7": 168,
    "PGL2_7": 336,
    "PSL2_8": 504,
    "PGL2_8": 504,
    "PSL2_11": 660,
    "SL2_11": 1320,
    "PGL2_11": 1320,
    "PSL2_13": 1092,
    "SL2_13": 2184,
    "M11": 7920,
    "PSL3_3": 5616,
}

# PackageGT's N19 shelf entry is retained as an explicit audit fixture, but
# it is a PB4 tuple.  It must not be silently presented as a K(0,5) image:
# the PB4 centre is nontrivial.  The producer reports this as rejected before
# evaluating raw A.18.  The tuples are in paper order
# (g12,g23,g13,g14,g24,g34).
PACKAGEGT_N19_PB4 = (
    ((3, 1, 2, 6, 4, 5, 7, 8, 9)),
    ((4, 7, 3, 9, 5, 2, 6, 8, 1)),
    ((7, 2, 6, 4, 1, 9, 5, 8, 3)),
    ((1, 6, 8, 4, 3, 7, 2, 5, 9)),
    ((8, 2, 4, 7, 5, 1, 3, 6, 9)),
    ((2, 3, 1, 4, 5, 6, 9, 7, 8)),
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def cjson(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=True, separators=(",", ":")).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(cjson(value)).hexdigest()


def file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def free_reduce(word: Iterable[int]) -> list[int]:
    out: list[int] = []
    for letter in word:
        require(isinstance(letter, int) and not isinstance(letter, bool) and letter != 0,
                "signed word drift")
        if out and out[-1] == -letter:
            out.pop()
        else:
            out.append(letter)
    return out


def inverse_word(word: Iterable[int]) -> list[int]:
    return [-x for x in reversed(list(word))]


MAPS = (
    ("123", (1,), (4,)),
    ("234", (4,), (6,)),
    ("12,3,4", (2, 4), (6,)),
    ("1,23,4", (1, 2), (5, 6)),
    ("1,2,34", (1,), (4, 5)),
)


def marked_substitute(word: list[int], first: tuple[int, ...], second: tuple[int, ...]) -> list[int]:
    out: list[int] = []
    for letter in word:
        require(isinstance(letter, int) and abs(letter) in (1, 4),
                "marked F2 alphabet drift")
        image = first if abs(letter) == 1 else second
        out.extend(inverse_word(image) if letter < 0 else image)
    return free_reduce(out)


def exact_dtilde(f2: list[int]) -> list[int]:
    marked: list[int] = []
    for letter in f2:
        require(isinstance(letter, int) and abs(letter) in (1, 2),
                "roof F2 alphabet drift")
        if abs(letter) == 1:
            marked.append(1 if letter > 0 else -1)
        else:
            marked.append(4 if letter > 0 else -4)
    x15, x45 = [-3, -2, -1], [-6, -5, -3]
    return free_reduce(
        inverse_word(marked_substitute(marked, tuple(x45), (6,)))
        + inverse_word(marked_substitute(marked, (1,), tuple(x15)))
        + marked_substitute(marked, (4,), (6,))
        + marked_substitute(marked, tuple(x45), tuple(x15))
        + marked_substitute(marked, (1,), (4,))
    )


def load_inputs(input_path: Path, words_path: Path) -> tuple[list[list[int]], list[list[int]], list[list[int]]]:
    require(file_sha(input_path) == SOURCE_SHA, "canonical source SHA drift")
    source = json.loads(input_path.read_text(encoding="utf-8"))
    require(source.get("schema") == "d972-b4-p2-magnus-input/v2" and
            source.get("relator_count") == 158 and
            len(source.get("all_relators", [])) == 158 and
            source.get("all_relators_sha256") == RELATOR_SHA,
            "canonical raw-A.18 source contract drift")
    relators = [[int(x) for x in row] for row in source["all_relators"]]
    require(digest(relators) == RELATOR_SHA, "raw relator digest drift")
    seeds = relators[18:46]
    a18: list[list[int]] = []
    for _name, first, second in MAPS:
        a18.extend(marked_substitute(row, first, second) for row in seeds)
    require(len(a18) == 140 and digest(a18) == A18_ROWS_SHA, "raw A.18 rows drift")
    presentation = relators[:18] + a18
    require(len(presentation) == 158 and digest(presentation) == PRESENTATION_SHA,
            "raw A.18 presentation drift")

    require(file_sha(words_path) == WORDS_SHA, "word artifact SHA drift")
    words = json.loads(words_path.read_text(encoding="utf-8"))
    require(words.get("schema") == "d972-b4-word-key-artifact/v1" and
            words.get("count") == 972 and len(words.get("rows", [])) == 972,
            "word artifact contract drift")
    f2_rows: list[list[int]] = []
    for row in words["rows"]:
        require(isinstance(row, list) and len(row) == 3, "word row shape drift")
        value = [] if row[2] == "" else row[2]
        require(isinstance(value, list), "word row empty-list type drift")
        f2_rows.append([int(x) for x in value])
    dtilde = [exact_dtilde(row) for row in f2_rows]
    require(len(dtilde) == 972 and digest(dtilde) == DTILDE_SHA, "D-tilde digest drift")
    return relators, presentation, dtilde


def perm_identity(degree: int) -> tuple[int, ...]:
    return tuple(range(1, degree + 1))


def perm_inverse(p: tuple[int, ...]) -> tuple[int, ...]:
    result = [0] * len(p)
    for index, image in enumerate(p, 1):
        result[image - 1] = index
    return tuple(result)


def perm_mul(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    # GAP's permutation convention is right action: (i^(left*right))
    # equals (i^left)^right.
    return tuple(right[left[index] - 1] for index in range(len(left)))


def validate_images(raw: Any) -> tuple[tuple[int, ...], ...]:
    require(isinstance(raw, list) and len(raw) == 6, "generator image count drift")
    require(all(isinstance(row, list) for row in raw), "generator image row drift")
    degree = len(raw[0])
    require(degree >= 1 and all(len(row) == degree for row in raw),
            "generator image degree drift")
    expected = set(range(1, degree + 1))
    images: list[tuple[int, ...]] = []
    for row in raw:
        require(set(row) == expected and all(isinstance(x, int) for x in row),
                "generator image is not a permutation")
        images.append(tuple(row))
    return tuple(images)


def eval_word(word: list[int], images: tuple[tuple[int, ...], ...]) -> tuple[int, ...]:
    result = perm_identity(len(images[0]))
    for letter in word:
        require(0 < abs(letter) <= 6, "presentation alphabet drift")
        image = images[abs(letter) - 1]
        if letter < 0:
            image = perm_inverse(image)
        result = perm_mul(result, image)
    return result


def generated_order(images: tuple[tuple[int, ...], ...]) -> int:
    identity = perm_identity(len(images[0]))
    generators = list(images) + [perm_inverse(p) for p in images]
    seen = {identity}
    frontier = [identity]
    while frontier:
        current = frontier.pop()
        for generator in generators:
            product = perm_mul(current, generator)
            if product not in seen:
                seen.add(product)
                frontier.append(product)
    return len(seen)


def image_vector(p: tuple[int, ...]) -> list[int]:
    return list(p)


def reject_old_rho(receipt: dict[str, Any]) -> None:
    forbidden = ("rho_words", "rho_tail", "rho_orbit", "rho5", "rho_words_sha256")
    require(not any(key in receipt for key in forbidden),
            "old rho-tail receipt is forbidden for raw A.18")
    require(receipt.get("presentation_semantics") == SEMANTICS,
            "raw A.18 presentation semantics gate failed")
    require(receipt.get("rho_tail_used") is False,
            "rho-tail use must be explicitly false")


def check_receipt(receipt_path: Path, input_path: Path = INPUT_PATH,
                  words_path: Path = WORDS_PATH) -> dict[str, Any]:
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    require(isinstance(receipt, dict), "receipt must be an object")
    require(receipt.get("schema") == SCHEMA, "receipt schema drift")
    require(receipt.get("status") == "B4_A_CANDIDATE_RAW_A18_FINITE_IMAGE",
            "receipt status is not a raw-A.18 finite candidate")
    reject_old_rho(receipt)
    for key, expected in (
        ("source_sha256", SOURCE_SHA),
        ("word_artifact_sha256", WORDS_SHA),
        ("relator_sha256", RELATOR_SHA),
        ("a18_rows_sha256", A18_ROWS_SHA),
        ("presentation_sha256", PRESENTATION_SHA),
        ("dtilde_sha256", DTILDE_SHA),
    ):
        require(receipt.get(key) == expected, f"receipt {key} drift")
    require(receipt.get("generator_order") == list(GENERATOR_ORDER),
            "generator order drift")
    require(receipt.get("raw_relator_count") == 158 and
            receipt.get("raw_relator_bad_count") == 0 and
            receipt.get("dtilde_count") == 972,
            "receipt ledger count drift")
    require(isinstance(receipt.get("epi_index"), int) and
            isinstance(receipt.get("epi_count"), int) and
            receipt["epi_index"] >= 1 and receipt["epi_count"] >= receipt["epi_index"],
            "receipt epimorphism index drift")
    target = receipt.get("target_label")
    require(target in TARGET_ORDERS, "target is outside the fixed finite shelf")
    require(receipt.get("target_order") == TARGET_ORDERS[target], "target order drift")
    images = validate_images(receipt.get("generator_images"))
    degree = len(images[0])
    require(receipt.get("target_degree") == degree, "target degree drift")
    require(receipt.get("surjective") is True, "receipt is not an asserted epimorphism")
    require(generated_order(images) == TARGET_ORDERS[target],
            "six images do not generate the claimed target order")

    _relators, presentation, dtilde = load_inputs(input_path, words_path)
    one = perm_identity(degree)
    raw_bad: list[dict[str, Any]] = []
    for index, word in enumerate(presentation, 1):
        image = eval_word(word, images)
        if image != one:
            raw_bad.append({"index": index, "word": word, "image": image_vector(image)})
    require(not raw_bad, f"raw A.18 relator failure at {raw_bad[0]['index'] if raw_bad else '?'}")
    defects: list[dict[str, Any]] = []
    for index, word in enumerate(dtilde, 1):
        image = eval_word(word, images)
        if image != one:
            defects.append({"index": index, "word": word, "image": image_vector(image)})
    declared_bad = receipt.get("raw_relator_bad_count")
    require(declared_bad == 0, "receipt self-reported raw relator defect")
    declared_dtilde = receipt.get("dtilde_defect_count")
    require(isinstance(declared_dtilde, int) and declared_dtilde == len(defects),
            "receipt D-tilde defect count drift")
    require(defects, "candidate receipt has no independently replayed D-tilde defect")
    declared_first = receipt.get("first_defect")
    require(isinstance(declared_first, dict) and
            declared_first.get("index") == defects[0]["index"] and
            declared_first.get("word") == defects[0]["word"] and
            declared_first.get("image") == defects[0]["image"],
            "receipt first-defect witness drift")
    status = ("B4_A_CANDIDATE_RAW_A18_FINITE_IMAGE_CROSSCHECKED"
              if defects else "UNKNOWN_RAW_A18_FINITE_IMAGE_ALLPASS")
    return {
        "schema": SCHEMA,
        "status": status,
        "presentation_semantics": SEMANTICS,
        "target_label": target,
        "target_order": TARGET_ORDERS[target],
        "target_degree": degree,
        "raw_relator_count": len(presentation),
        "raw_relator_bad_count": len(raw_bad),
        "dtilde_count": len(dtilde),
        "dtilde_defect_count": len(defects),
        "first_defect": defects[0] if defects else None,
        "receipt_sha256": file_sha(receipt_path),
    }


def packagegt_n19_center() -> tuple[int, ...]:
    # Paper-order PB4 tuple; this is deliberately not a K05 evaluation.
    product = perm_identity(9)
    for index in (3, 4, 5, 0, 2, 1):  # g14,g24,g34,g12,g13,g23
        product = perm_mul(product, PACKAGEGT_N19_PB4[index])
    return product


def selftest() -> None:
    relators, presentation, dtilde = load_inputs(INPUT_PATH, WORDS_PATH)
    require(len(relators) == 158 and len(presentation) == 158 and len(dtilde) == 972,
            "selftest input counts")
    require(packagegt_n19_center() != perm_identity(9),
            "PackageGT N19 centre gate unexpectedly vanished")
    identity = [[1]] * 6
    images = validate_images(identity)
    require(generated_order(images) == 1 and eval_word([], images) == (1,),
            "permutation evaluator selftest")
    forged = {
        "schema": SCHEMA,
        "presentation_semantics": SEMANTICS,
        "rho_tail_used": False,
        "source_sha256": SOURCE_SHA,
        "word_artifact_sha256": WORDS_SHA,
        "relator_sha256": RELATOR_SHA,
        "a18_rows_sha256": A18_ROWS_SHA,
        "presentation_sha256": PRESENTATION_SHA,
        "dtilde_sha256": DTILDE_SHA,
        "generator_order": list(GENERATOR_ORDER),
        "target_label": "A5",
        "target_order": 60,
        "target_degree": 1,
        "generator_images": identity,
        "surjective": True,
    }
    try:
        target = forged["target_label"]
        require(generated_order(validate_images(forged["generator_images"])) == TARGET_ORDERS[target],
                "forged target unexpectedly accepted")
    except ValueError:
        pass
    else:
        raise AssertionError("forged target selftest did not fail closed")
    old = dict(forged)
    old["rho_words"] = []
    try:
        reject_old_rho(old)
    except ValueError:
        pass
    else:
        raise AssertionError("rho-tail selftest did not fail closed")
    print("D972_B4_A18_FINITE_IMAGE_V1_SELFTEST_PASS")
    print(f"D972_B4_A18_FINITE_IMAGE_V1_FINAL_MARKER status=PASS presentation={PRESENTATION_SHA} dtilde={DTILDE_SHA}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt", type=Path)
    parser.add_argument("--input", type=Path, default=INPUT_PATH)
    parser.add_argument("--words", type=Path, default=WORDS_PATH)
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.selftest:
        selftest()
        return 0
    require(args.receipt is not None, "--receipt is required unless --selftest is used")
    result = check_receipt(args.receipt, args.input, args.words)
    encoded = json.dumps(result, ensure_ascii=True, sort_keys=True, separators=(",", ":"))
    if args.output:
        args.output.write_text(encoded + "\n", encoding="utf-8")
    print(encoded)
    print(f"{FINAL_MARKER} status={result['status']} target={result['target_label']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
