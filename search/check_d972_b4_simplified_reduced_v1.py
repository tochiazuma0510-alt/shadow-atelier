#!/usr/bin/env python3
"""Independent checker for the nonconfluent KBMAG reduced-form ledger.

This checker rebuilds the canonical F6 norms, validates the supplied
transport receipt and substitution, then authenticates the 972 reduced words
and their counts/hashes.  It deliberately does not treat KBMAG rules as a
proof: the receipt records that completion exposed no derivation ancestry.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "search" / "certs" / "d972_b4_p2_magnus_input_v2_20260816.json"
WORDS = ROOT / "search" / "certs" / "d972_b4_word_key_artifact_v1_20260816.json"
SOURCE_SHA = "c61b2b77131127aca83a8d7c56b7fdadd2d519b040ea4d91093622c813c2b4a9"
RELATOR_SHA = "12fc1146dce5179c2b5fc44a3ceed6356a6b2c4835a564b55e9a9cd679fccd2e"
RHO = ((-6, -5, -3), (3,), (5,), (-3, -2, -1), (-5, -4, -1), (1,))
NORM_SHA = "ecf0cc8425bc24bdf6a8a352c223398221c4b179e09ee9a0bfe3dc888861683e"
WORDS_SHA = "564a921be8114bdeb963f679c121e8d9aa90e148c65e95e393874fcba843e9f9"
TARGET_SHA = "9c77e6768feb7ffe7143abf18f753af70e81b8e9cc792910c30ae0075d3b1d62"
TUPLE_SHA = "32e78ca5b97cd8a6fa59a150dac77719c1b8cb527f0467570c4d284600465a91"
TRANSPORT_SHA = "535d033019140e76cb9d3d7452b3e551c156f50ce74728b76bf6238d81806323"
SIMPLE_REL_SHA = "6d614c32365753d62477cad8803420ffa58bcca0b5d18b0e5eadaaf6bf81b35a"
SIMPLE_NORM_SHA = "127f029a2bafc7f8adf249b8c5f37cda594b105d3e1b567ba00400771cdca63e"


def digest(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, separators=(",", ":"), ensure_ascii=True).encode()).hexdigest()


def reduce_word(word: list[int]) -> list[int]:
    out: list[int] = []
    for x in word:
        if x == 0 or abs(x) > 6:
            raise ValueError("F6 letter drift")
        if out and out[-1] == -x:
            out.pop()
        else:
            out.append(x)
    return out


def rho_word(word: list[int]) -> list[int]:
    out: list[int] = []
    for x in word:
        image = list(RHO[abs(x) - 1])
        if x < 0:
            image = [-y for y in reversed(image)]
        out.extend(image)
    return reduce_word(out)


def exact_norm(word: list[int]) -> list[int]:
    current = reduce_word([(1 if x > 0 else -1) if abs(x) == 1 else
                           (4 if x > 0 else -4) for x in word])
    orbit: list[list[int]] = []
    for _ in range(5):
        orbit.append(current)
        current = rho_word(current)
    out: list[int] = []
    for current in reversed(orbit):
        out = reduce_word(out + current)
    return out


def require_words(value: Any, count: int, width: int, name: str,
                  allow_empty: bool = True) -> list[list[int]]:
    if not isinstance(value, list) or len(value) != count:
        raise ValueError(f"{name} count drift")
    out: list[list[int]] = []
    for row in value:
        if not isinstance(row, list) or (not allow_empty and not row):
            raise ValueError(f"{name} shape drift")
        if any(not isinstance(x, int) or x == 0 or abs(x) > width for x in row):
            raise ValueError(f"{name} signed-word drift")
        out.append(list(row))
    return out


def substitute(word: list[int], images: list[list[int]], source_width: int) -> list[int]:
    out: list[int] = []
    for x in word:
        if x == 0 or abs(x) > source_width:
            raise ValueError("transport source-letter drift")
        image = list(images[abs(x) - 1])
        if x < 0:
            image = [-y for y in reversed(image)]
        for y in image:
            if out and out[-1] == -y:
                out.pop()
            else:
                out.append(y)
    return out


def canonical_norms() -> list[list[int]]:
    source_raw = SOURCE.read_bytes()
    if hashlib.sha256(source_raw).hexdigest() != SOURCE_SHA:
        raise ValueError("source SHA drift")
    source_obj = json.loads(source_raw.decode())
    if (source_obj.get("schema") != "d972-b4-p2-magnus-input/v2" or
            source_obj.get("rho_words") != [list(x) for x in RHO] or
            source_obj.get("all_relators_sha256") != RELATOR_SHA or
            len(source_obj.get("all_relators", [])) != 158):
        raise ValueError("canonical source gate failed")
    words_raw = WORDS.read_bytes()
    if hashlib.sha256(words_raw).hexdigest() != WORDS_SHA:
        raise ValueError("word artifact SHA drift")
    obj = json.loads(words_raw.decode())
    if (obj.get("schema") != "d972-b4-word-key-artifact/v1" or
            obj.get("count") != 972 or obj.get("source_target_key_digest") != TARGET_SHA or
            obj.get("frozen_tuple_sha256") != TUPLE_SHA):
        raise ValueError("word artifact gate failed")
    rows = obj.get("rows")
    if not isinstance(rows, list) or len(rows) != 972:
        raise ValueError("word row count drift")
    normalized: list[list[Any]] = []
    for i, row in enumerate(rows):
        if not isinstance(row, list) or len(row) != 3:
            raise ValueError("word row shape drift")
        m, key, word = row
        if word == "":
            if i not in (0, 891):
                raise ValueError("legacy empty row drift")
            word = []
        if not isinstance(word, list):
            raise ValueError("word row type drift")
        normalized.append([m, key, [int(x) for x in word]])
    if digest(normalized) != obj.get("canonical_bytes_sha256"):
        raise ValueError("normalized artifact digest drift")
    norms = [exact_norm(row[2]) for row in normalized]
    if digest(norms) != NORM_SHA:
        raise ValueError("exact norm digest drift")
    return norms


def verify(transport_path: Path, reduced: dict[str, Any], norms: list[list[int]]) -> dict[str, Any]:
    transport_raw = transport_path.read_bytes()
    if hashlib.sha256(transport_raw).hexdigest() != TRANSPORT_SHA:
        raise ValueError("transport receipt SHA drift")
    transport = json.loads(transport_raw.decode())
    if (transport.get("schema") != "d972-b4-u-simplified-transport/v1" or
            transport.get("source_sha256") != SOURCE_SHA or
            transport.get("relator_sha256") != RELATOR_SHA or
            transport.get("roof_norm_sha256") != NORM_SHA or
            transport.get("simple_relators_sha256") != SIMPLE_REL_SHA or
            transport.get("simple_norms_sha256") != SIMPLE_NORM_SHA):
        raise ValueError("transport pin drift")
    simple_rels = require_words(transport.get("simple_relators"), 141, 5, "simple relators")
    simple_norms = require_words(transport.get("simple_norm_words"), 972, 5, "simple norms")
    if digest(simple_rels) != SIMPLE_REL_SHA or digest(simple_norms) != SIMPLE_NORM_SHA:
        raise ValueError("transport word digest drift")
    maps = require_words(transport.get("original_to_simple_words"), 6, 5, "U-to-simple map")
    if [substitute(norm, maps, 6) for norm in norms] != simple_norms:
        raise ValueError("canonical norms do not replay to transport words")
    if reduced.get("schema") != "d972-b4-simplified-reduced/v1":
        raise ValueError("reduced receipt schema drift")
    for key, value in (("source_sha256", SOURCE_SHA), ("relator_sha256", RELATOR_SHA),
                       ("roof_norm_sha256", NORM_SHA), ("simple_relators_sha256", SIMPLE_REL_SHA),
                       ("simple_norms_sha256", SIMPLE_NORM_SHA),
                       ("transport_receipt_sha256", TRANSPORT_SHA)):
        if reduced.get(key) != value:
            raise ValueError(f"reduced {key} pin drift")
    reduced_words = require_words(reduced.get("reduced_norm_words"), 972, 5, "reduced norms")
    unique_words = reduced.get("reduced_unique_words")
    if not isinstance(unique_words, list) or reduced.get("unique_norm_count") != len(unique_words):
        raise ValueError("reduced unique count drift")
    if {tuple(x) for x in unique_words} != {tuple(x) for x in reduced_words}:
        raise ValueError("reduced unique ledger drift")
    if digest(reduced_words) != reduced.get("reduced_norm_words_sha256"):
        raise ValueError("reduced norm digest drift")
    if digest(unique_words) != reduced.get("reduced_unique_words_sha256"):
        raise ValueError("reduced unique digest drift")
    empty_count = sum(not row for row in reduced_words)
    if reduced.get("empty_count") != empty_count:
        raise ValueError("empty count drift")
    status = str(reduced.get("status"))
    if status == "ALL_EMPTY_REWRITE_CANDIDATE":
        final = "UNKNOWN_ALL_EMPTY_KBMAG_NO_ANCESTRY"
    elif status == "NONZERO_REDUCED_WORDS":
        final = "UNKNOWN_NONZERO_REDUCED_WORDS"
    else:
        final = "UNKNOWN_KBMAG_NOT_NORMAL_STOP"
    return {"schema": "d972-b4-simplified-reduced-independent-check/v1",
            "status": final, "norm_count": 972,
            "unique_norm_count": len(unique_words), "empty_count": empty_count,
            "transport_words_replayed": True, "kbmag_rule_ancestry_replayed": False,
            "terminal_claim": False}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt", type=Path, required=True)
    parser.add_argument("--transport", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = verify(args.transport.resolve(), json.loads(args.receipt.resolve().read_text()), canonical_norms())
    raw = args.receipt.resolve().read_bytes()
    result["reduced_receipt_sha256"] = hashlib.sha256(raw).hexdigest()
    args.output.resolve().parent.mkdir(parents=True, exist_ok=True)
    args.output.resolve().write_text(json.dumps(result, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
