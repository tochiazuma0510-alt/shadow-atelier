#!/usr/bin/env python3
"""Independent checker for the exact B4 KBMAG-v2 norm input.

This checker intentionally does not import `d972_b4_kbmag_v2.py`, GAP, or the
old KBMAG lane.  It reconstructs j and the rho orbit itself, binds the
corrected 972-row digest, and rejects receipts that omit the six-generator
norm digest or use the old direct-F2 map.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


TARGET_DIGEST = (
    "9c77e6768feb7ffe7143abf18f753af70e81b8e9cc792910c30ae0075d3b1d62"
)
TUPLE_DIGEST = (
    "32e78ca5b97cd8a6fa59a150dac77719c1b8cb527f0467570c4d284600465a91"
)
RELATOR_DIGEST = (
    "12fc1146dce5179c2b5fc44a3ceed6356a6b2c4835a564b55e9a9cd679fccd2e"
)
NORMALIZED_ROWS_DIGEST = (
    "283bf9cc728ced084a3b276e4496fbbc69026589813a2f31caa0dcb7a3682930"
)
NORM_DIGEST = (
    "ecf0cc8425bc24bdf6a8a352c223398221c4b179e09ee9a0bfe3dc888861683e"
)
RHO = (
    (-6, -5, -3), (3,), (5,), (-3, -2, -1), (-5, -4, -1), (1,)
)


def cjson(value: Any) -> bytes:
    return json.dumps(value, separators=(",", ":"),
                      ensure_ascii=True).encode("ascii")


def sha(value: Any) -> str:
    return hashlib.sha256(cjson(value)).hexdigest()


def free_reduce(word: list[int]) -> list[int]:
    out: list[int] = []
    for letter in word:
        if letter == 0 or abs(letter) > 6:
            raise ValueError("not an F6 signed word")
        if out and out[-1] == -letter:
            out.pop()
        else:
            out.append(letter)
    return out


def apply_rho(word: list[int]) -> list[int]:
    expanded: list[int] = []
    for letter in word:
        image = list(RHO[abs(letter) - 1])
        if letter < 0:
            image = [-x for x in reversed(image)]
        expanded.extend(image)
    return free_reduce(expanded)


def exact_norm(f2_word: list[int]) -> list[int]:
    jword: list[int] = []
    for letter in f2_word:
        if abs(letter) == 1:
            jword.append(1 if letter > 0 else -1)
        elif abs(letter) == 2:
            jword.append(4 if letter > 0 else -4)
        else:
            raise ValueError("F2 word has a non-F2 letter")
    jword = free_reduce(jword)
    orbit: list[list[int]] = []
    current = jword
    for _ in range(5):
        orbit.append(current)
        current = apply_rho(current)
    output: list[int] = []
    for current in reversed(orbit):
        output = free_reduce(output + current)
    return output


def load_rows(path: Path) -> tuple[list[list[Any]], list[int]]:
    with path.open(encoding="utf-8") as handle:
        obj = json.load(handle)
    if obj.get("schema") != "d972-b4-word-key-artifact/v1":
        raise ValueError("word artifact schema drift")
    if obj.get("count") != 972 or obj.get("source_target_key_digest") != TARGET_DIGEST:
        raise ValueError("word artifact count/target drift")
    if obj.get("frozen_tuple_sha256") != TUPLE_DIGEST:
        raise ValueError("word artifact tuple drift")
    rows = obj.get("rows")
    if not isinstance(rows, list) or len(rows) != 972:
        raise ValueError("word artifact rows drift")
    if obj.get("canonical_bytes_sha256") != sha(rows):
        raise ValueError("word artifact canonical binding drift")
    normalized: list[list[Any]] = []
    legacy: list[int] = []
    for index, row in enumerate(rows):
        if not isinstance(row, list) or len(row) != 3:
            raise ValueError(f"word row {index} shape drift")
        m, key, word = row
        if word == "":
            if index not in (0, 891):
                raise ValueError(f"unexpected empty row {index}")
            legacy.append(index)
            word = []
        if not isinstance(m, int) or not isinstance(key, list) or not isinstance(word, list):
            raise ValueError(f"word row {index} type drift")
        if any(not isinstance(letter, int) or letter == 0 for letter in word):
            raise ValueError(f"word row {index} signed-letter drift")
        normalized.append([m, key, list(word)])
    if legacy:
        # The final artifact must be regenerated with [] rather than "".
        # Exploratory input is allowed here only so that its normalized bytes
        # are checked against the same frozen universe.
        pass
    if sha(normalized) != NORMALIZED_ROWS_DIGEST:
        raise ValueError("corrected 972-row digest drift")
    return normalized, legacy


def check_receipt(path: Path, expected_norm_digest: str) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        receipt = json.load(handle)
    if receipt.get("schema") != "d972-b4-kbmag-input/v2":
        raise ValueError("input receipt schema drift")
    if receipt.get("status") != "ROOF_NORMS_CONSTRUCTED":
        raise ValueError("input receipt is not a norm-construction receipt")
    if receipt.get("row_count") != 972:
        raise ValueError("input receipt row count drift")
    if receipt.get("j_map") != {"f2_1": 1, "f2_2": 4}:
        raise ValueError("input receipt j map is not X12/X23")
    if receipt.get("rho_order") != [4, 3, 2, 1, 0]:
        raise ValueError("input receipt norm order drift")
    if receipt.get("roof_norm_words_sha256") != expected_norm_digest:
        raise ValueError("input receipt norm digest drift")
    if receipt.get("relator_digest") != RELATOR_DIGEST:
        raise ValueError("input receipt relator digest drift")
    return {
        "receipt_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "receipt_schema": receipt["schema"],
        "receipt_norm_digest": expected_norm_digest,
    }


def check_gap_source(path: Path) -> dict[str, Any]:
    source = path.read_text(encoding="utf-8")
    required = {
        "exact_norm_constructor": "D972KBV2NormWord:=function(sw)",
        "canonical_j_x": "D972KBV2FreeGens[1]",
        "canonical_j_y": "D972KBV2FreeGens[4]",
        "rho_free_substitution": "D972KBV2RhoFree",
        "reverse_norm_order": "for t in Reversed([1..5])",
        "norm_digest_gate": "ecf0cc8425bc24bdf6a8a352c223398221c4b179e09ee9a0bfe3dc888861683e",
        "six_generator_reduction": "D972KBV2SignedToU(normWords[ii])",
    }
    missing = [name for name, marker in required.items() if marker not in source]
    if missing:
        raise ValueError("KBMAG v2 source markers missing: " + ",".join(missing))
    return {
        "source_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "markers": {name: True for name in required},
        "old_direct_f2_mapper_absent": "D972KBToUWord" not in source,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact", type=Path, required=True)
    parser.add_argument("--receipt", type=Path)
    parser.add_argument("--gap-source", type=Path,
                        default=Path(__file__).resolve().parent /
                        "d972_b4_kbmag_v2.g")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    rows, legacy = load_rows(args.artifact.resolve())
    norms = [exact_norm(row[2]) for row in rows]
    norm_digest = sha(norms)
    if norm_digest != NORM_DIGEST:
        raise SystemExit(f"norm digest mismatch: {norm_digest}")
    result: dict[str, Any] = {
        "schema": "d972-b4-kbmag-independent-check/v2",
        "status": "ROOF_NORM_CROSSCHECKED_NO_KBMAG_RUN",
        "row_count": len(rows),
        "legacy_empty_row_indices": legacy,
        "normalized_rows_sha256": sha(rows),
        "target_key_digest": TARGET_DIGEST,
        "frozen_tuple_digest": TUPLE_DIGEST,
        "relator_digest": RELATOR_DIGEST,
        "j_map": {"f2_1": 1, "f2_2": 4},
        "rho_order": [4, 3, 2, 1, 0],
        "roof_norm_words_sha256": norm_digest,
        "roof_norm_lengths_sha256": sha([len(word) for word in norms]),
        "global_b_status": "UNKNOWN",
    }
    result["gap_source"] = check_gap_source(args.gap_source.resolve())
    if args.receipt:
        result["input_receipt"] = check_receipt(args.receipt.resolve(), norm_digest)
        result["status"] = "ROOF_NORM_CROSSCHECKED_RECEIPT_BOUND"
    encoded = json.dumps(result, sort_keys=True, indent=2) + "\n"
    print(encoded, end="")
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
