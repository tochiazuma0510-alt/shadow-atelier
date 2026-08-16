#!/usr/bin/env python3
"""Independent checker for the exact 6-to-5 simplified-presentation receipt.

The checker does not import the GAP producer.  It authenticates the canonical
input, rebuilds all 972 F6 rho-norms, checks the pinned 5-generator/141-
relator transport fields and word digests, and deliberately leaves KBMAG
all-pass as UNKNOWN because a GAP rewriting-system proof is not replayed by
this Python checker.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = ROOT / "search" / "certs" / "d972_b4_p2_magnus_input_v2_20260816.json"
DEFAULT_WORDS = ROOT / "search" / "certs" / "d972_b4_word_key_artifact_v1_20260816.json"
SOURCE_SHA = "c61b2b77131127aca83a8d7c56b7fdadd2d519b040ea4d91093622c813c2b4a9"
RELATOR_SHA = "12fc1146dce5179c2b5fc44a3ceed6356a6b2c4835a564b55e9a9cd679fccd2e"
RHO = ((-6, -5, -3), (3,), (5,), (-3, -2, -1), (-5, -4, -1), (1,))
NORM_SHA = "ecf0cc8425bc24bdf6a8a352c223398221c4b179e09ee9a0bfe3dc888861683e"
WORDS_SHA = "564a921be8114bdeb963f679c121e8d9aa90e148c65e95e393874fcba843e9f9"
TARGET_SHA = "9c77e6768feb7ffe7143abf18f753af70e81b8e9cc792910c30ae0075d3b1d62"
TUPLE_SHA = "32e78ca5b97cd8a6fa59a150dac77719c1b8cb527f0467570c4d284600465a91"


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


def load_norms(source: Path, words: Path) -> tuple[list[list[int]], str]:
    source_raw = source.read_bytes()
    if hashlib.sha256(source_raw).hexdigest() != SOURCE_SHA:
        raise ValueError("source SHA drift")
    source_obj = json.loads(source_raw.decode("utf-8"))
    if (source_obj.get("schema") != "d972-b4-p2-magnus-input/v2" or
            source_obj.get("rho_words") != [list(x) for x in RHO] or
            source_obj.get("all_relators_sha256") != RELATOR_SHA or
            len(source_obj.get("all_relators", [])) != 158):
        raise ValueError("source canonical gate failed")
    words_raw = words.read_bytes()
    if hashlib.sha256(words_raw).hexdigest() != WORDS_SHA:
        raise ValueError("word artifact SHA drift")
    obj = json.loads(words_raw.decode("utf-8"))
    if (obj.get("schema") != "d972-b4-word-key-artifact/v1" or
            obj.get("count") != 972 or
            obj.get("source_target_key_digest") != TARGET_SHA or
            obj.get("frozen_tuple_sha256") != TUPLE_SHA):
        raise ValueError("word artifact canonical gate failed")
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
        raise ValueError("normalized word artifact digest drift")
    norms = [exact_norm(row[2]) for row in normalized]
    if digest(norms) != NORM_SHA:
        raise ValueError("exact norm digest drift")
    return norms, hashlib.sha256(words_raw).hexdigest()


def require_words(rows: Any, count: int, width: int, name: str) -> list[list[int]]:
    if not isinstance(rows, list) or len(rows) != count:
        raise ValueError(name + " count drift")
    out: list[list[int]] = []
    for row in rows:
        if not isinstance(row, list) or any(not isinstance(x, int) or x == 0 or abs(x) > width for x in row):
            raise ValueError(name + " signed-word drift")
        out.append(list(row))
    return out


def substitute(word: list[int], images: list[list[int]], source_width: int) -> list[int]:
    """Free-reduced image under a signed generator map, independently of GAP."""
    out: list[int] = []
    for x in word:
        if x == 0 or abs(x) > source_width:
            raise ValueError("transport source-letter drift")
        image = list(images[abs(x) - 1])
        if x < 0:
            image = [-y for y in reversed(image)]
        out = reduce_word(out + image)
    return out


def verify(receipt: dict[str, Any], norms: list[list[int]], raw_words_sha: str) -> dict[str, Any]:
    if receipt.get("schema") != "d972-b4-u-simplified-transport/v1":
        raise ValueError("receipt schema drift")
    for key, value in (("source_sha256", SOURCE_SHA), ("relator_sha256", RELATOR_SHA),
                       ("word_artifact_sha256", WORDS_SHA), ("roof_norm_sha256", NORM_SHA)):
        if receipt.get(key) != value:
            raise ValueError(key + " pin drift")
    if receipt.get("simple_generator_count") != 5 or receipt.get("simple_relator_count") != 141:
        raise ValueError("simplified shape drift")
    simple_rels = require_words(receipt.get("simple_relators"), 141, 5, "simple relators")
    simple_norms = require_words(receipt.get("simple_norm_words"), 972, 5, "simple norms")
    if digest(simple_rels) != receipt.get("simple_relators_sha256"):
        raise ValueError("simple relator digest drift")
    if digest(simple_norms) != receipt.get("simple_norms_sha256"):
        raise ValueError("simple norm digest drift")
    map_u_to_s = require_words(receipt.get("original_to_simple_words"), 6, 5, "U-to-simple map")
    map_s_to_u = require_words(receipt.get("simple_to_original_words"), 5, 6, "simple-to-U map")
    if digest([map_u_to_s, map_s_to_u]) != receipt.get("transport_maps_sha256"):
        raise ValueError("transport map digest drift")
    replayed_norms = [substitute(norm, map_u_to_s, 6) for norm in norms]
    if replayed_norms != simple_norms:
        raise ValueError("transported norm words do not replay from canonical F6 norms")
    if receipt.get("roof_count") != 972 or receipt.get("word_artifact_sha256") != raw_words_sha:
        raise ValueError("transport norm count/artifact drift")
    # The producer's inverse-map identity checks are load-bearing GAP facts;
    # retain them as explicit receipt booleans when present, but never infer
    # a global B result from the opaque simplifier or KBMAG all-pass.
    status = str(receipt.get("status"))
    if status == "CONFLUENT_ALLPASS_CANDIDATE":
        final = "UNKNOWN_KBMAG_ALLPASS_TRANSPORT_CROSSCHECKED"
    elif status in {"NOT_RUN", "NO_TERMINAL_KBMAG_RESULT", "TRANSPORT_READY"}:
        final = "TRANSPORT_CROSSCHECKED_UNKNOWN"
    else:
        final = "TRANSPORT_CROSSCHECKED_UNKNOWN"
    bits = receipt.get("kbmag_roof_bits")
    if bits is not None and (not isinstance(bits, list) or len(bits) not in (0, 972) or
                             any(not isinstance(x, bool) for x in bits)):
        raise ValueError("KBMAG bit ledger drift")
    return {"schema": "d972-b4-u-simplified-transport-independent-check/v1",
            "status": final, "simple_generator_count": 5,
            "simple_relator_count": 141, "norm_count": 972,
            "transport_words_replayed": True, "transport_map_substitution_checked": True,
            "kbmag_allpass_terminal": False}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--words", type=Path, default=DEFAULT_WORDS)
    args = parser.parse_args(argv)
    norms, raw_words_sha = load_norms(args.source.resolve(), args.words.resolve())
    receipt_raw = args.receipt.resolve().read_bytes()
    result = verify(json.loads(receipt_raw.decode("utf-8")), norms, raw_words_sha)
    result["producer_receipt_sha256"] = hashlib.sha256(receipt_raw).hexdigest()
    args.output.resolve().parent.mkdir(parents=True, exist_ok=True)
    args.output.resolve().write_text(json.dumps(result, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
