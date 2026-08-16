"""Independent checker for the raw A.18 p=3 Schreier lane.

The checker rebuilds the five literal substitutions, the 158-relator
presentation, the regular C2^5 Schreier basis, and the unconditional
PENT-FORM' D-tilde words.  It does not import the GAP producer.  A finite
quotient defect is reported as a replayed candidate, never as a global claim.
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
DTILDE_RS_SHA = "418e88934210e726de0e7e1f375bac2e6151f465be84f913884c58129217259c"
RAW_RS_SHA = "db25c0268cdc774ef3205c9c1d1cf62cd013e6daaf73cf959e7972af5b3082bb"
RHO = ((-6, -5, -3), (3,), (5,), (-3, -2, -1), (-5, -4, -1), (1,))
GEN_BITS = (1, 2, 4, 8, 16, 31)
MAPS = (
    ("123", (1,), (4,)),
    ("234", (4,), (6,)),
    ("12,3,4", (2, 4), (6,)),
    ("1,23,4", (1, 2), (5, 6)),
    ("1,2,34", (1,), (4, 5)),
)
SCHEMA = "d972-b4-u-a18-anupq/v1"
FINAL = "D972_B4_U_A18_ANUPQ_V1_FINAL"


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


def rho_word(word: list[int]) -> list[int]:
    out: list[int] = []
    for letter in word:
        require(isinstance(letter, int) and letter != 0 and abs(letter) <= 6,
                "rho alphabet drift")
        image = list(RHO[abs(letter) - 1])
        out.extend(inverse_word(image) if letter < 0 else image)
    return free_reduce(out)


def marked_substitute(word: list[int], first: list[int], second: list[int]) -> list[int]:
    out: list[int] = []
    for letter in word:
        require(isinstance(letter, int) and letter != 0 and abs(letter) in (1, 4),
                "marked F2 alphabet drift")
        image = first if abs(letter) == 1 else second
        out.extend(inverse_word(image) if letter < 0 else image)
    return free_reduce(out)


def exact_dtilde(f2: list[int]) -> list[int]:
    marked = []
    for letter in f2:
        require(abs(letter) in (1, 2), "roof F2 alphabet drift")
        marked.append((1 if letter > 0 else -1) if abs(letter) == 1
                      else (4 if letter > 0 else -4))
    x15, x45 = [-3, -2, -1], [-6, -5, -3]
    return free_reduce(
        inverse_word(marked_substitute(marked, x45, [6])) +
        inverse_word(marked_substitute(marked, [1], x15)) +
        marked_substitute(marked, [4], [6]) +
        marked_substitute(marked, x45, x15) +
        marked_substitute(marked, [1], [4]))


def load_inputs(input_path: Path, words_path: Path) -> tuple[list[list[int]], list[list[int]], list[list[int]]]:
    source_bytes = input_path.read_bytes()
    require(file_sha(input_path) == SOURCE_SHA, "canonical input SHA drift")
    source = json.loads(source_bytes.decode("utf-8"))
    require(source.get("schema") == "d972-b4-p2-magnus-input/v2" and
            source.get("relator_count") == 158 and
            len(source.get("all_relators", [])) == 158 and
            tuple(tuple(x) for x in source.get("rho_words", [])) == RHO and
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

    words_bytes = words_path.read_bytes()
    require(file_sha(words_path) == WORDS_SHA, "word artifact SHA drift")
    words = json.loads(words_bytes.decode("utf-8"))
    require(words.get("schema") == "d972-b4-word-key-artifact/v1" and
            words.get("count") == 972 and len(words.get("rows", [])) == 972,
            "word artifact contract drift")
    f2_rows: list[list[int]] = []
    for row in words["rows"]:
        require(isinstance(row, list) and len(row) == 3, "word row shape drift")
        value = row[2]
        if value == "":
            value = []
        require(isinstance(value, list), "word row empty-list type drift")
        f2_rows.append([int(x) for x in value])
    dtilde = [exact_dtilde(row) for row in f2_rows]
    require(digest(dtilde) == DTILDE_SHA, "Dtilde digest drift")
    return relators, presentation, dtilde


def transversal(mask: int) -> list[int]:
    return [i + 1 for i in range(5) if mask & (1 << i)]


def toggle(mask: int, bit: int) -> int:
    return 31 - mask if bit == 31 else mask ^ bit


def build_rs(relators: list[list[int]]) -> tuple[list[list[int]], dict[tuple[int, int], int], list[list[int]]]:
    pair_id: dict[tuple[int, int], int] = {}
    pair_words: list[list[int]] = []
    for mask in range(32):
        for gen, bit in enumerate(GEN_BITS, 1):
            word = free_reduce(transversal(mask) + [gen] +
                               inverse_word(transversal(toggle(mask, bit))))
            if word:
                pair_id[(mask, gen)] = len(pair_words) + 1
                pair_words.append(word)
            else:
                pair_id[(mask, gen)] = 0
    require(len(pair_words) == 161, "Schreier generator count drift")

    def rewrite(word: list[int], start: int) -> list[int]:
        mask, out = start, []
        for letter in word:
            gen, bit = abs(letter), GEN_BITS[abs(letter) - 1]
            if letter > 0:
                ident = pair_id[(mask, gen)]
                if ident:
                    out.append(ident)
                mask = toggle(mask, bit)
            else:
                mask = toggle(mask, bit)
                ident = pair_id[(mask, gen)]
                if ident:
                    out.append(-ident)
        require(mask == start, "word leaves C2^5")
        return free_reduce(out)

    rows: list[list[int]] = []
    for start in range(32):
        for relator in relators:
            row = rewrite(relator, start)
            if row:
                rows.append(row)
    require(len(rows) == 5056, f"Schreier relator count drift: {len(rows)}")
    return rows, pair_id, [transversal(mask) for mask in range(32)]


def rewrite_norms(norms: list[list[int]], pair_id: dict[tuple[int, int], int]) -> list[list[int]]:
    result: list[list[int]] = []
    for word in norms:
        mask, out = 0, []
        for letter in word:
            gen, bit = abs(letter), GEN_BITS[abs(letter) - 1]
            if letter > 0:
                ident = pair_id[(mask, gen)]
                if ident:
                    out.append(ident)
                mask = toggle(mask, bit)
            else:
                mask = toggle(mask, bit)
                ident = pair_id[(mask, gen)]
                if ident:
                    out.append(-ident)
        require(mask == 0, "Dtilde leaves C2^5")
        result.append(free_reduce(out))
    return result


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
        require(checked[pair[0] - 1] == 1 and all(checked[i] == 0 for i in range(pair[0] - 1)),
                "conjugate tail drift")
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


def pc_inverse_generator(index: int, orders: list[int], power: list[list[int]], memo: dict[int, list[int]]) -> list[int]:
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
    _relators, presentation, dtilde = load_inputs(input_path, words_path)
    raw_rows, pair_id, transversal_rows = build_rs(presentation)
    norm_rows = rewrite_norms(dtilde, pair_id)
    require(digest(raw_rows) == RAW_RS_SHA, "raw RS digest drift")
    require(digest(norm_rows) == DTILDE_RS_SHA, "Dtilde RS digest drift")
    receipt_bytes = receipt_path.read_bytes()
    receipt = json.loads(receipt_bytes.decode("utf-8"))
    require(receipt.get("schema") == SCHEMA, "receipt schema drift")
    require(receipt.get("final_marker") == FINAL, "final marker drift")
    require(receipt.get("source_sha256") == SOURCE_SHA and
            receipt.get("word_artifact_sha256") == WORDS_SHA and
            receipt.get("relator_sha256") == RELATOR_SHA and
            receipt.get("a18_rows_sha256") == A18_ROWS_SHA and
            receipt.get("presentation_sha256") == PRESENTATION_SHA and
            receipt.get("dtilde_sha256") == DTILDE_SHA and
            receipt.get("raw_rs_sha256") == RAW_RS_SHA and
            receipt.get("dtilde_rs_sha256") == DTILDE_RS_SHA,
            "receipt digest binding drift")
    require(receipt.get("terminal_claim") is False and
            receipt.get("normal_closure_status") == "NOT_RUN_BOUNDED",
            "receipt scope drift")
    expected_basis = {
        "basis_id": "regular_c2^5_mask_transversal_v1",
        "coset_count": 32,
        "original_generator_count": 6,
        "rs_generator_count": 161,
        "rs_relator_count": 5056,
        "gen_bits": list(GEN_BITS),
        "transversal": transversal_rows,
    }
    require(receipt.get("basis_contract") == expected_basis, "basis contract drift")
    require(receipt.get("a18_map_count") == 5 and receipt.get("a18_row_count") == 140 and
            receipt.get("norm_count") == 972 and receipt.get("quotient_prime") == 3 and
            receipt.get("p_quotient_bound") == 4096, "count contract drift")
    status = receipt.get("status")
    if status == "A18_ANUPQ_SELFTEST_PASS":
        return {"status": status, "classes": 0, "defects": []}
    require(status in {"UNKNOWN_P3_BOUNDED", "B4_A_CANDIDATE_P3"}, "top status drift")
    classes = receipt.get("classes")
    require(isinstance(classes, list) and classes, "class ledger absent")
    require(receipt.get("completed_classes") == [row.get("class") for row in classes],
            "completed class drift")
    defects: list[dict[str, Any]] = []
    for row in classes:
        require(row.get("status") in {"ALLPASS", "DEFECT", "UNKNOWN_RESOURCE"},
                "class status drift")
        if row["status"] == "UNKNOWN_RESOURCE":
            continue
        orders = row.get("pcgs_relative_orders")
        images = row.get("quotient_generator_images")
        require(isinstance(orders, list) and orders and all(isinstance(x, int) and x > 0 for x in orders),
                "PC orders drift")
        require(row.get("order") == math.prod(orders), "PC order drift")
        require(isinstance(images, list) and len(images) == 161 and
                all(isinstance(x, list) and len(x) == len(orders) for x in images),
                "image basis drift")
        require(all(0 <= x < orders[j] for image in images for j, x in enumerate(image)),
                "image coordinate drift")
        power, conjugates = pc_contract(orders, row.get("pcgs_power_relations"),
                                        row.get("pcgs_conjugate_relations"))
        zero = [0] * len(orders)
        for index, relator in enumerate(raw_rows):
            require(pc_eval(relator, images, orders, power, conjugates) == zero,
                    f"quotient fails relator {index}")
        computed: list[tuple[int, list[int]]] = []
        for index, word in enumerate(norm_rows, 1):
            value = pc_eval(word, images, orders, power, conjugates)
            if value != zero:
                computed.append((index, value))
        require(row.get("bad_count") == len(computed), "bad-count drift")
        first = row.get("first_defect")
        if row["status"] == "DEFECT":
            require(computed and isinstance(first, dict) and
                    first.get("index") == computed[0][0] and
                    first.get("image") == computed[0][1] and
                    first.get("norm_rs") == norm_rows[computed[0][0] - 1],
                    "first defect drift")
            defects.append({"class": row["class"], "index": first["index"],
                            "image": first["image"]})
        else:
            require(first is None and not computed, "all-pass class has defect")
    if defects:
        require(status == "B4_A_CANDIDATE_P3", "defect top status drift")
        out_status = "B4_A_CANDIDATE_P3_REPLAY_CROSSCHECKED"
    else:
        require(status == "UNKNOWN_P3_BOUNDED", "all-pass top status drift")
        out_status = "UNKNOWN_P3_ALLPASS_OR_RESOURCE"
    return {"status": out_status, "classes": len(classes), "defects": defects,
            "receipt_sha256": file_sha(receipt_path)}


def selftest(input_path: Path, words_path: Path) -> None:
    relators, presentation, dtilde = load_inputs(input_path, words_path)
    raw, pair_id, _ = build_rs(presentation)
    norm_rows = rewrite_norms(dtilde, pair_id)
    require(len(raw) == 5056 and len(norm_rows) == 972, "selftest count drift")
    require(digest(raw) == RAW_RS_SHA and digest(norm_rows) == DTILDE_RS_SHA,
            "selftest digest drift")
    tampered = list(norm_rows[0]) + [1]
    require(tampered != norm_rows[0], "negative fixture setup failed")
    print("D972_B4_U_A18_ANUPQ_CHECKER_SELFTEST_PASS")


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
    result = verify(args.receipt, args.input, args.words)
    print(json.dumps({"schema": "d972-b4-u-a18-anupq-check/v1", **result},
                     ensure_ascii=True, indent=2, sort_keys=True))
    print("D972_B4_U_A18_ANUPQ_CHECKER_FINAL")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
