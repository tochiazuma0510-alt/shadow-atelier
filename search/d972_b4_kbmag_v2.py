#!/usr/bin/env python3
"""Construct the exact six-generator B4 norm words for KBMAG v2.

The old KBMAG lane reduced a two-generator F2 word directly in the six
generator U_M alphabet.  That is not the pentagon norm: the canonical map is
``j(x)=U1, j(y)=U4`` and the word must be multiplied in the order
``rho^4(j(f)) ... rho(j(f)) j(f)``.  This helper rebuilds that word list from
the corrected 972-row artifact without importing GAP or the old producer.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


TARGET_KEY_DIGEST = (
    "9c77e6768feb7ffe7143abf18f753af70e81b8e9cc792910c30ae0075d3b1d62"
)
FROZEN_TUPLE_DIGEST = (
    "32e78ca5b97cd8a6fa59a150dac77719c1b8cb527f0467570c4d284600465a91"
)
RELATOR_DIGEST = (
    "12fc1146dce5179c2b5fc44a3ceed6356a6b2c4835a564b55e9a9cd679fccd2e"
)
ROOF_NORM_DIGEST = (
    "ecf0cc8425bc24bdf6a8a352c223398221c4b179e09ee9a0bfe3dc888861683e"
)

# rho on the six K(0,5) free generators, in the same order as the universal
# GAP source.  Each list is a reduced signed free word.
RHO_FREE_IMAGES: tuple[tuple[int, ...], ...] = (
    (-6, -5, -3),
    (3,),
    (5,),
    (-3, -2, -1),
    (-5, -4, -1),
    (1,),
)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, separators=(",", ":"), ensure_ascii=True
    ).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def reduce_free(word: list[int] | tuple[int, ...]) -> list[int]:
    out: list[int] = []
    for letter in word:
        if letter == 0 or abs(letter) > 6:
            raise ValueError(f"invalid F6 letter {letter}")
        if out and out[-1] == -letter:
            out.pop()
        else:
            out.append(letter)
    return out


def rho_word(word: list[int] | tuple[int, ...]) -> list[int]:
    expanded: list[int] = []
    for letter in word:
        image = list(RHO_FREE_IMAGES[abs(letter) - 1])
        if letter < 0:
            image = [-x for x in reversed(image)]
        expanded.extend(image)
    return reduce_free(expanded)


def map_j(word: list[int]) -> list[int]:
    """Map a signed F2 word through j(x)=U1, j(y)=U4."""

    mapped: list[int] = []
    for letter in word:
        if abs(letter) not in (1, 2):
            raise ValueError(f"roof row is not a signed F2 word: {letter}")
        mapped.append((1 if letter > 0 else -1) if abs(letter) == 1
                      else (4 if letter > 0 else -4))
    return reduce_free(mapped)


def norm_word(word: list[int]) -> list[int]:
    """Return rho^4(j(word))*...*rho(j(word))*j(word)."""

    orbit: list[list[int]] = []
    current = map_j(word)
    for _ in range(5):
        orbit.append(current)
        current = rho_word(current)
    result: list[int] = []
    for current in reversed(orbit):
        result = reduce_free(result + current)
    return result


def load_rows(path: Path) -> tuple[list[list[Any]], list[int], str]:
    with path.open(encoding="utf-8") as handle:
        obj = json.load(handle)
    if not isinstance(obj, dict):
        raise ValueError("word artifact root is not an object")
    if obj.get("schema") != "d972-b4-word-key-artifact/v1":
        raise ValueError("word artifact schema drift")
    if obj.get("count") != 972:
        raise ValueError("word artifact count drift")
    if obj.get("source_target_key_digest") != TARGET_KEY_DIGEST:
        raise ValueError("word artifact target digest drift")
    if obj.get("frozen_tuple_sha256") != FROZEN_TUPLE_DIGEST:
        raise ValueError("word artifact tuple digest drift")
    rows = obj.get("rows")
    if not isinstance(rows, list) or len(rows) != 972:
        raise ValueError("word artifact row count drift")
    raw_digest = digest(rows)
    if obj.get("canonical_bytes_sha256") != raw_digest:
        raise ValueError("word artifact canonical digest does not bind rows")
    normalized: list[list[Any]] = []
    legacy: list[int] = []
    for index, row in enumerate(rows):
        if not isinstance(row, list) or len(row) != 3:
            raise ValueError(f"word row {index} shape drift")
        m, key, word = row
        if word == "":
            if index not in (0, 891):
                raise ValueError(f"unexpected legacy empty row {index}")
            legacy.append(index)
            word = []
        if not isinstance(m, int) or not isinstance(key, list):
            raise ValueError(f"word row {index} metadata drift")
        if not isinstance(word, list) or any(
            not isinstance(letter, int) or letter == 0 for letter in word
        ):
            raise ValueError(f"word row {index} signed-word drift")
        normalized.append([m, key, list(word)])
    return normalized, legacy, raw_digest


def build_receipt(path: Path) -> dict[str, Any]:
    rows, legacy, raw_digest = load_rows(path)
    words = [norm_word(row[2]) for row in rows]
    norm_digest = digest(words)
    if norm_digest != ROOF_NORM_DIGEST:
        raise ValueError(f"roof norm digest drift: {norm_digest}")
    return {
        "schema": "d972-b4-kbmag-input/v2",
        "status": "ROOF_NORMS_CONSTRUCTED",
        "word_artifact": str(path.resolve()),
        "word_artifact_raw_rows_sha256": raw_digest,
        "word_artifact_legacy_empty_rows": legacy,
        "row_count": len(words),
        "j_map": {"f2_1": 1, "f2_2": 4},
        "rho_order": [4, 3, 2, 1, 0],
        "rho_free_images": [list(x) for x in RHO_FREE_IMAGES],
        "roof_norm_words_sha256": norm_digest,
        "roof_norm_word_lengths": [len(word) for word in words],
        "relator_digest": RELATOR_DIGEST,
        "target_key_digest": TARGET_KEY_DIGEST,
        "frozen_tuple_digest": FROZEN_TUPLE_DIGEST,
        "source_note": (
            "This is the six-generator pentagon norm, not a direct reduction "
            "of the two-generator F2 representative."
        ),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    receipt = build_receipt(args.artifact.resolve())
    encoded = json.dumps(receipt, sort_keys=True, indent=2) + "\n"
    print(encoded, end="")
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
