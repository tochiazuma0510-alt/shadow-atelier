"""Independent checker for the direct raw-A.18 p=2/p=5 harness.

This checker rebuilds the canonical 158-relator presentation and all 972
D-tilde words without importing the GAP producer.  A receipt is accepted
only when its six-generator PC image kills every raw relator and the declared
D-tilde defect count is reproduced.  Directness matters: the quotient is of
F6/N_A itself, so no Schreier-kernel core argument is silently assumed.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
from typing import Any

SOURCE_SHA = "c61b2b77131127aca83a8d7c56b7fdadd2d519b040ea4d91093622c813c2b4a9"
WORDS_SHA = "564a921be8114bdeb963f679c121e8d9aa90e148c65e95e393874fcba843e9f9"
RELATOR_SHA = "12fc1146dce5179c2b5fc44a3ceed6356a6b2c4835a564b55e9a9cd679fccd2e"
A18_ROWS_SHA = "1f0cacaa20ab8474245f30568469de807b5877b2ca7dd0d6668c9b8956750722"
PRESENTATION_SHA = "783d7d80f472fbf6abc8a2f58454048de361e95774c76ce1c511982bb44eb305"
DTILDE_SHA = "32cdc85b315817e939feca628bc15235a55664157ca1e272815a53f1de4631ef"
SCHEMA = "d972-b4-u-a18-direct-p/v1"
FINAL = "D972_B4_U_A18_DIRECT_P_V1_FINAL"
RHO = ((-6, -5, -3), (3,), (5,), (-3, -2, -1), (-5, -4, -1), (1,))
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


def cjson(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=True, separators=(",", ":")).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(cjson(value)).hexdigest()


def file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def free_reduce(word: list[int]) -> list[int]:
    out: list[int] = []
    for letter in word:
        require(isinstance(letter, int) and letter != 0, "signed word drift")
        if out and out[-1] == -letter:
            out.pop()
        else:
            out.append(letter)
    return out


def inverse_word(word: list[int]) -> list[int]:
    return [-x for x in reversed(word)]


def marked_substitute(word: list[int], first: list[int], second: list[int]) -> list[int]:
    out: list[int] = []
    for letter in word:
        require(abs(letter) in (1, 4), "marked F2 alphabet drift")
        image = first if abs(letter) == 1 else second
        out.extend(inverse_word(image) if letter < 0 else image)
    return free_reduce(out)


def exact_dtilde(f2: list[int]) -> list[int]:
    marked = []
    for letter in f2:
        require(abs(letter) in (1, 2), "roof F2 alphabet drift")
        marked.append((1 if letter > 0 else -1) if abs(letter) == 1 else
                      (4 if letter > 0 else -4))
    x15, x45 = [-3, -2, -1], [-6, -5, -3]
    return free_reduce(
        inverse_word(marked_substitute(marked, x45, [6])) +
        inverse_word(marked_substitute(marked, [1], x15)) +
        marked_substitute(marked, [4], [6]) +
        marked_substitute(marked, x45, x15) +
        marked_substitute(marked, [1], [4]))


def load_inputs(input_path: Path, words_path: Path) -> tuple[list[list[int]], list[list[int]]]:
    source_bytes = input_path.read_bytes()
    require(file_sha(input_path) == SOURCE_SHA, "canonical input SHA drift")
    source = json.loads(source_bytes.decode("utf-8"))
    require(source.get("schema") == "d972-b4-p2-magnus-input/v2" and
            source.get("relator_count") == 158 and
            len(source.get("all_relators", [])) == 158 and
            tuple(tuple(x) for x in source.get("rho_words", [])) == RHO and
            source.get("rho_words_source") == "universal_v2_canonical" and
            source.get("all_relators_sha256") == RELATOR_SHA,
            "canonical input contract drift")
    relators = [[int(x) for x in row] for row in source["all_relators"]]
    require(digest(relators) == RELATOR_SHA, "relator digest drift")
    seeds = relators[18:46]
    a18: list[list[int]] = []
    for _name, first, second in MAPS:
        a18.extend(marked_substitute(row, list(first), list(second)) for row in seeds)
    require(digest(a18) == A18_ROWS_SHA, "A18 row digest drift")
    presentation = relators[:18] + a18
    require(digest(presentation) == PRESENTATION_SHA, "presentation digest drift")
    words = json.loads(words_path.read_text(encoding="utf-8"))
    require(file_sha(words_path) == WORDS_SHA and words.get("count") == 972 and
            words.get("schema") == "d972-b4-word-key-artifact/v1" and
            len(words.get("rows", [])) == 972, "word artifact contract drift")
    f2_rows: list[list[int]] = []
    for row in words["rows"]:
        require(isinstance(row, list) and len(row) == 3, "word row shape drift")
        value = row[2] if row[2] != "" else []
        require(isinstance(value, list), "word row empty-list type drift")
        f2_rows.append([int(x) for x in value])
    dtilde = [exact_dtilde(row) for row in f2_rows]
    require(digest(dtilde) == DTILDE_SHA, "Dtilde digest drift")
    return presentation, dtilde


def coords_to_word(coords: list[int]) -> list[int]:
    result: list[int] = []
    for index, exponent in enumerate(coords, 1):
        result.extend([index] * exponent)
    return result


def pc_contract(orders: list[int], power: Any, conjugates: Any) -> tuple[list[list[int]], dict[tuple[int, int], list[int]]]:
    require(isinstance(power, list) and len(power) == len(orders), "power shape drift")
    powers: list[list[int]] = []
    for row in power:
        require(isinstance(row, list) and len(row) == len(orders), "power vector drift")
        checked = [int(x) for x in row]
        require(all(0 <= x < orders[i] for i, x in enumerate(checked)), "power coordinate drift")
        powers.append(checked)
    expected = {(i, j) for i in range(2, len(orders) + 1) for j in range(1, i)}
    got: dict[tuple[int, int], list[int]] = {}
    require(isinstance(conjugates, list), "conjugate shape drift")
    for row in conjugates:
        require(isinstance(row, list) and len(row) == 3, "conjugate row drift")
        pair = (int(row[0]), int(row[1]))
        require(pair in expected and pair not in got, "conjugate index drift")
        vector = row[2]
        require(isinstance(vector, list) and len(vector) == len(orders), "conjugate vector drift")
        checked = [int(x) for x in vector]
        require(all(0 <= x < orders[i] for i, x in enumerate(checked)), "conjugate coordinate drift")
        require(checked[pair[0] - 1] == 1 and
                all(checked[i] == 0 for i in range(pair[0] - 1)), "conjugate tail drift")
        got[pair] = checked
    require(set(got) == expected, "conjugate coverage drift")
    return powers, got


def pc_normalize(sequence: list[int], orders: list[int], power: list[list[int]],
                 conjugates: dict[tuple[int, int], list[int]]) -> list[int]:
    for _ in range(1_000_000):
        changed = False
        for pos in range(len(sequence) - 1):
            left, right = sequence[pos:pos + 2]
            if left > right:
                sequence[pos:pos + 2] = [right] + coords_to_word(conjugates[(left, right)])
                changed = True
                break
        if changed:
            continue
        for pos, generator in enumerate(sequence):
            order = orders[generator - 1]
            run = 0
            while pos + run < len(sequence) and sequence[pos + run] == generator:
                run += 1
            if run >= order:
                sequence[pos:pos + order] = coords_to_word(power[generator - 1])
                changed = True
                break
        if not changed:
            result = [0] * len(orders)
            for generator in sequence:
                result[generator - 1] += 1
            require(all(result[i] < orders[i] for i in range(len(orders))), "PC normal form drift")
            return result
    raise ValueError("PC collection did not terminate")


def pc_inverse_generator(index: int, orders: list[int], power: list[list[int]],
                         memo: dict[int, list[int]]) -> list[int]:
    if index in memo:
        return memo[index]
    tail = coords_to_word(power[index])
    result = [index + 1] * (orders[index] - 1)
    for generator in reversed(tail):
        result.extend(pc_inverse_generator(generator - 1, orders, power, memo))
    memo[index] = result
    return result


def pc_eval(word: list[int], images: list[list[int]], orders: list[int],
            power: list[list[int]], conjugates: dict[tuple[int, int], list[int]]) -> list[int]:
    sequence: list[int] = []
    memo: dict[int, list[int]] = {}
    for letter in word:
        image = images[abs(letter) - 1]
        if letter > 0:
            sequence.extend(coords_to_word(image))
        else:
            for generator in reversed(coords_to_word(image)):
                sequence.extend(pc_inverse_generator(generator - 1, orders, power, memo))
    return pc_normalize(sequence, orders, power, conjugates)


def verify(receipt_path: Path, input_path: Path, words_path: Path) -> dict[str, Any]:
    presentation, dtilde = load_inputs(input_path, words_path)
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    require(receipt.get("schema") == SCHEMA and receipt.get("final_marker") == FINAL,
            "receipt identity drift")
    require(receipt.get("terminal_claim") is False and receipt.get("ambient_presentation") is True and
            receipt.get("normal_closure_status") == "NOT_NEEDED_DIRECT_AMBIENT",
            "direct ambient scope drift")
    require(receipt.get("source_sha256") == SOURCE_SHA and
            receipt.get("word_artifact_sha256") == WORDS_SHA and
            receipt.get("relator_sha256") == RELATOR_SHA and
            receipt.get("a18_rows_sha256") == A18_ROWS_SHA and
            receipt.get("presentation_sha256") == PRESENTATION_SHA and
            receipt.get("dtilde_sha256") == DTILDE_SHA,
            "receipt digest binding drift")
    require(receipt.get("raw_relator_count") == 158 and receipt.get("dtilde_count") == 972,
            "count contract drift")
    require(receipt.get("generator_order") == [1, 2, 3, 4, 5, 6],
            "generator order drift")
    require(receipt.get("raw_relators") == presentation and receipt.get("dtilde_words") == dtilde,
            "lossless word ledger drift")
    prime = receipt.get("prime")
    require(prime in (2, 5), "prime drift")
    allowed = set(range(1, 5 if prime == 2 else 4))
    requested = receipt.get("requested_classes")
    require(isinstance(requested, list) and requested and set(requested) <= allowed and
            len(set(requested)) == len(requested), "class preregistration drift")
    classes = receipt.get("classes")
    require(isinstance(classes, list) and receipt.get("completed_classes") ==
            [row.get("class") for row in classes], "class ledger drift")
    defects: list[dict[str, Any]] = []
    for row in classes:
        require(row.get("class") in requested, "unexpected class result")
        if row.get("status") == "UNKNOWN_RESOURCE":
            continue
        require(row.get("status") in {"ALLPASS", "DEFECT"}, "class status drift")
        orders = row.get("pcgs_relative_orders")
        images = row.get("quotient_generator_images")
        require(isinstance(orders, list) and all(isinstance(x, int) and x > 0 for x in orders),
                "PC orders drift")
        require(row.get("order") == math.prod(orders), "PC order drift")
        require(isinstance(images, list) and len(images) == 6 and
                all(isinstance(x, list) and len(x) == len(orders) for x in images),
                "six-image ledger drift")
        require(all(0 <= x < orders[j] for image in images for j, x in enumerate(image)),
                "image coordinate drift")
        power, conjugates = pc_contract(orders, row.get("pcgs_power_relations"),
                                        row.get("pcgs_conjugate_relations"))
        zero = [0] * len(orders)
        raw_bad: list[int] = []
        for index, relator in enumerate(presentation, 1):
            value = pc_eval(relator, images, orders, power, conjugates)
            if value != zero:
                raw_bad.append(index)
        require(row.get("raw_relator_bad_count") == len(raw_bad) == 0,
                "quotient fails raw relator")
        computed: list[tuple[int, list[int]]] = []
        for index, word in enumerate(dtilde, 1):
            value = pc_eval(word, images, orders, power, conjugates)
            if value != zero:
                computed.append((index, value))
        require(row.get("dtilde_bad_count") == len(computed), "Dtilde bad-count drift")
        first = row.get("first_defect")
        if computed:
            require(row.get("status") == "DEFECT" and isinstance(first, dict) and
                    first.get("index") == computed[0][0] and first.get("word") == dtilde[computed[0][0] - 1] and
                    first.get("image") == computed[0][1], "first defect drift")
            defects.append({"class": row["class"], "index": first["index"], "image": first["image"]})
        else:
            require(row.get("status") == "ALLPASS" and first is None, "all-pass status drift")
    expected_status = "DIRECT_FINITE_OBSTRUCTION_CANDIDATE" if defects else "UNKNOWN_DIRECT_P_BOUNDED"
    require(receipt.get("status") == expected_status, "top status drift")
    return {"status": expected_status, "prime": prime, "classes": len(classes),
            "defects": defects, "receipt_sha256": file_sha(receipt_path)}


def selftest(input_path: Path, words_path: Path) -> None:
    presentation, dtilde = load_inputs(input_path, words_path)
    require(len(presentation) == 158 and len(dtilde) == 972, "count drift")
    require(presentation[0] != presentation[1] or dtilde[0] == [], "fixture setup drift")
    print("D972_B4_U_A18_DIRECT_P_CHECKER_SELFTEST_PASS")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt", type=Path)
    parser.add_argument("--input", type=Path,
                        default=Path("search/certs/d972_b4_p2_magnus_input_v2_20260816.json"))
    parser.add_argument("--words", type=Path,
                        default=Path("search/certs/d972_b4_word_key_artifact_v1_20260816.json"))
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args()
    if args.selftest:
        selftest(args.input, args.words)
        return 0
    require(args.receipt is not None, "--receipt is required")
    print(json.dumps({"schema": "d972-b4-u-a18-direct-p-check/v1",
                      **verify(args.receipt, args.input, args.words)},
                     ensure_ascii=True, indent=2, sort_keys=True))
    print("D972_B4_U_A18_DIRECT_P_CHECKER_FINAL")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
