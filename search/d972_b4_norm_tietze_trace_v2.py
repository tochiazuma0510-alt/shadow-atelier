#!/usr/bin/env python3
"""Canonical, proof-producing RS/Tietze transport lane (v2).

This is a versioned replacement for ``d972_b4_norm_tietze_trace_v1.py``.
It reads the pinned canonical input directly, builds the ordinary
Reidemeister--Schreier presentation (161 generators/5056 relators), and then
performs only explicit one-occurrence Tietze substitutions.  Generator IDs are
kept stable during the trace; a final, recorded dense relabelling produces a
presentation suitable for KBMAG when the active generator count is <=127.

The producer is intentionally not a proof by itself.  The companion checker
reconstructs the RS words and replays every primitive, including all 972 norm
test words and both cumulative generator maps.  A non-empty final presentation
or an all-pass finite run is UNKNOWN; only a checker-accepted all-empty norm
ledger can be promoted to a per-word identity certificate.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "search" / "certs" / "d972_b4_p2_magnus_input_v2_20260816.json"
DEFAULT_WORDS = ROOT / "search" / "certs" / "d972_b4_word_key_artifact_v1_20260816.json"

SCHEMA = "d972-b4-norm-tietze-trace/v2"
SOURCE_SHA = "c61b2b77131127aca83a8d7c56b7fdadd2d519b040ea4d91093622c813c2b4a9"
RELATOR_SHA = "12fc1146dce5179c2b5fc44a3ceed6356a6b2c4835a564b55e9a9cd679fccd2e"
WORD_ARTIFACT_SHA = "564a921be8114bdeb963f679c121e8d9aa90e148c65e95e393874fcba843e9f9"
ROWS_SHA = "283bf9cc728ced084a3b276e4496fbbc69026589813a2f31caa0dcb7a3682930"
NORM_SHA = "ecf0cc8425bc24bdf6a8a352c223398221c4b179e09ee9a0bfe3dc888861683e"
TARGET_SHA = "9c77e6768feb7ffe7143abf18f753af70e81b8e9cc792910c30ae0075d3b1d62"
TUPLE_SHA = "32e78ca5b97cd8a6fa59a150dac77719c1b8cb527f0467570c4d284600465a91"
PAIR_WORDS_SHA = "2be7ef40bbe19177a9777774e3685c4b5f564466a1f65fc55d5466b6dc34ca7e"
RS_WORDS_SHA = "29c65a6cf9d0308e25ca462c752d7b540a6856e7d99d5d1d016919240b575c0e"
NORM_RS_SHA = "f7134e15e92c80a5ceeede38e94314539815a665ba7d279443208de1696041f8"
BASIS_ID = "f2^5-positive-transversal-mask-order-v1"

GEN_BITS = (1, 2, 4, 8, 16, 31)
RHO = ((-6, -5, -3), (3,), (5,), (-3, -2, -1), (-5, -4, -1), (1,))
RAW_GENERATORS = 161
RS_RELATORS = 5056
NORM_COUNT = 972


def cjson(value: Any) -> bytes:
    return json.dumps(value, separators=(",", ":"), ensure_ascii=True).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(cjson(value)).hexdigest()


def reduce_word(word: list[int]) -> list[int]:
    out: list[int] = []
    for letter in word:
        if out and out[-1] == -letter:
            out.pop()
        else:
            out.append(letter)
    return out


def inverse_word(word: list[int]) -> list[int]:
    return [-x for x in reversed(word)]


def canonical_words(words: list[list[int]]) -> list[list[int]]:
    return sorted(reduce_word(list(word)) for word in words if word)


def rho_word(word: list[int]) -> list[int]:
    out: list[int] = []
    for letter in word:
        image = list(RHO[abs(letter) - 1])
        if letter < 0:
            image = inverse_word(image)
        out.extend(image)
    return reduce_word(out)


def exact_norm(f2_word: list[int]) -> list[int]:
    current = reduce_word([
        (1 if letter > 0 else -1) if abs(letter) == 1
        else (4 if letter > 0 else -4)
        for letter in f2_word
    ])
    orbit: list[list[int]] = []
    for _ in range(5):
        orbit.append(current)
        current = rho_word(current)
    out: list[int] = []
    for item in reversed(orbit):
        out = reduce_word(out + item)
    return out


def load_relators(path: Path) -> list[list[int]]:
    raw = path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != SOURCE_SHA:
        raise ValueError("canonical input SHA drift")
    obj = json.loads(raw.decode("utf-8"))
    if obj.get("schema") != "d972-b4-p2-magnus-input/v2":
        raise ValueError("canonical input schema drift")
    relators = obj.get("all_relators")
    if not isinstance(relators, list) or len(relators) != 158:
        raise ValueError("canonical relator count drift")
    relators = [[int(x) for x in word] for word in relators]
    if obj.get("all_relators_sha256") != RELATOR_SHA or digest(relators) != RELATOR_SHA:
        raise ValueError("canonical relator digest drift")
    if obj.get("rho_words") != [list(x) for x in RHO]:
        raise ValueError("canonical rho drift")
    if any(not word or any(x == 0 or abs(x) > 6 for x in word) for word in relators):
        raise ValueError("canonical signed relator alphabet drift")
    return relators


def load_norms(path: Path) -> tuple[list[list[int]], list[list[int]], str]:
    raw = path.read_bytes()
    raw_sha = hashlib.sha256(raw).hexdigest()
    if raw_sha != WORD_ARTIFACT_SHA:
        raise ValueError("word artifact SHA drift")
    obj = json.loads(raw.decode("utf-8"))
    if obj.get("schema") != "d972-b4-word-key-artifact/v1" or obj.get("count") != NORM_COUNT:
        raise ValueError("word artifact schema/count drift")
    if obj.get("source_target_key_digest") != TARGET_SHA or obj.get("frozen_tuple_sha256") != TUPLE_SHA:
        raise ValueError("word artifact target pin drift")
    rows = obj.get("rows")
    if not isinstance(rows, list) or len(rows) != NORM_COUNT:
        raise ValueError("word artifact row count drift")
    normalized: list[list[int]] = []
    for index, row in enumerate(rows):
        if not isinstance(row, list) or len(row) != 3:
            raise ValueError("word artifact row shape drift")
        m, key, word = row
        # The committed canonical artifact has already repaired the two GAP
        # empty-list/string rows.  Accepting strings here would reopen that
        # ambiguity, so fail closed.
        if not isinstance(m, int) or not isinstance(key, list) or not isinstance(word, list):
            raise ValueError(f"word artifact row type drift at {index}")
        if any(not isinstance(x, int) or x == 0 or abs(x) > 2 for x in word):
            raise ValueError(f"word artifact F2 alphabet drift at {index}")
        normalized.append([m, key, [int(x) for x in word]])
    if obj.get("canonical_bytes_sha256") != ROWS_SHA or digest(normalized) != ROWS_SHA:
        raise ValueError("word artifact row digest drift")
    norms = [exact_norm(row[2]) for row in normalized]
    if digest(norms) != NORM_SHA:
        raise ValueError("exact norm digest drift")
    return normalized, norms, raw_sha


def transversal() -> list[list[int]]:
    return [[i + 1 for i in range(5) if mask & (1 << i)] for mask in range(32)]


def build_rs(relators: list[list[int]]) -> tuple[list[list[int]], list[list[int]], dict[tuple[int, int], int | None]]:
    reps = transversal()
    pair_id: dict[tuple[int, int], int | None] = {}
    pair_words: list[list[int]] = []
    for mask in range(32):
        for gen, bit in enumerate(GEN_BITS, 1):
            word = reduce_word(reps[mask] + [gen] + inverse_word(reps[mask ^ bit]))
            if word:
                pair_id[(mask, gen)] = len(pair_words) + 1
                pair_words.append(word)
            else:
                pair_id[(mask, gen)] = None

    rs_rels: list[list[int]] = []
    for start in range(32):
        for relator in relators:
            mask = start
            rewritten: list[int] = []
            for letter in relator:
                gen = abs(letter)
                bit = GEN_BITS[gen - 1]
                if letter > 0:
                    ident = pair_id[(mask, gen)]
                    if ident is not None:
                        rewritten.append(ident)
                    mask ^= bit
                else:
                    mask ^= bit
                    ident = pair_id[(mask, gen)]
                    if ident is not None:
                        rewritten.append(-ident)
            if mask != start:
                raise ValueError("RS relator endpoint drift")
            rewritten = reduce_word(rewritten)
            if rewritten:
                rs_rels.append(rewritten)
    if len(pair_words) != RAW_GENERATORS or len(rs_rels) != RS_RELATORS:
        raise ValueError("RS dimension drift")
    return pair_words, rs_rels, pair_id


def rewrite_rs(word: list[int], pair_id: dict[tuple[int, int], int | None]) -> list[int]:
    mask = 0
    out: list[int] = []
    for letter in word:
        gen = abs(letter)
        bit = GEN_BITS[gen - 1]
        if letter > 0:
            ident = pair_id[(mask, gen)]
            if ident is not None:
                out.append(ident)
            mask ^= bit
        else:
            mask ^= bit
            ident = pair_id[(mask, gen)]
            if ident is not None:
                out.append(-ident)
    if mask != 0:
        raise ValueError("RS norm endpoint drift")
    return reduce_word(out)


def substitute_word(word: list[int], pivot_letter: int, replacement: list[int]) -> list[int]:
    inverse_replacement = inverse_word(replacement)
    out: list[int] = []
    for letter in word:
        if letter == pivot_letter:
            out.extend(inverse_replacement)
        elif letter == -pivot_letter:
            out.extend(replacement)
        else:
            out.append(letter)
    return reduce_word(out)


def substitute_words(words: list[list[int]], pivot_letter: int, replacement: list[int]) -> list[list[int]]:
    out: list[list[int]] = []
    for word in words:
        reduced = substitute_word(word, pivot_letter, replacement)
        if reduced:
            out.append(reduced)
    return out


def substitute_preserve(words: list[list[int]], pivot_letter: int, replacement: list[int]) -> list[list[int]]:
    return [substitute_word(word, pivot_letter, replacement) for word in words]


def choose_event(words: list[list[int]], active: set[int]) -> tuple[int, int, list[int], int] | None:
    best: tuple[tuple[int, int, int, int], tuple[int, int, list[int], int]] | None = None
    for relator_index, word in enumerate(words):
        counts = Counter(abs(x) for x in word)
        for position, letter in enumerate(word):
            pivot = abs(letter)
            if pivot not in active or counts[pivot] != 1:
                continue
            candidate = ((len(word), pivot, position, relator_index),
                         (relator_index, position, list(word), letter))
            if best is None or candidate[0] < best[0]:
                best = candidate
    return None if best is None else best[1]


def validate_map(map_words: list[list[int]], active: set[int], width: int) -> None:
    if not isinstance(map_words, list) or len(map_words) != width:
        raise ValueError("generator map width drift")
    for word in map_words:
        if not isinstance(word, list) or any(not isinstance(x, int) or x == 0 or abs(x) not in active for x in word):
            raise ValueError("generator map alphabet drift")


def run_trace(rs_rels: list[list[int]], norm_rs: list[list[int]], max_steps: int) -> dict[str, Any]:
    if max_steps < 0 or max_steps > RAW_GENERATORS:
        raise ValueError("max_steps outside bounded lane")
    words = [reduce_word(list(word)) for word in rs_rels if word]
    targets = [reduce_word(list(word)) for word in norm_rs]
    active = set(range(1, RAW_GENERATORS + 1))
    old_to_new = [[i] for i in range(1, RAW_GENERATORS + 1)]
    new_to_old = [[i] for i in range(1, RAW_GENERATORS + 1)]
    events: list[dict[str, Any]] = []
    initial_digest = digest(canonical_words(words))
    for step in range(1, max_steps + 1):
        selected = choose_event(words, active)
        if selected is None:
            break
        relator_index, position, defining, pivot_letter = selected
        pivot = abs(pivot_letter)
        if sum(abs(x) == pivot for x in defining) != 1:
            raise ValueError("internal pivot uniqueness failure")
        before_digest = digest(canonical_words(words))
        before_count = len(canonical_words(words))
        before_active = sorted(active)
        before_norm_digest = digest(targets)
        before_norm_empty = sum(not word for word in targets)
        tail_head = defining[position + 1 :] + defining[:position]
        replacement = list(tail_head)
        positive_substitution = inverse_word(replacement) if pivot_letter > 0 else replacement
        negative_substitution = replacement if pivot_letter > 0 else inverse_word(replacement)
        words = substitute_words(words, pivot_letter, replacement)
        targets = substitute_preserve(targets, pivot_letter, replacement)
        old_to_new = substitute_preserve(old_to_new, pivot_letter, replacement)
        active.remove(pivot)
        new_to_old[pivot - 1] = []
        after_digest = digest(canonical_words(words))
        after_count = len(canonical_words(words))
        after_norm_digest = digest(targets)
        after_norm_empty = sum(not word for word in targets)
        events.append({
            "step": step,
            "pivot": pivot,
            "pivot_letter": pivot_letter,
            "defining_relator_index": relator_index,
            "defining_relator": defining,
            "pivot_position": position,
            "replacement_word": replacement,
            "positive_substitution": positive_substitution,
            "negative_substitution": negative_substitution,
            "before_active_generators": before_active,
            "after_active_generators": sorted(active),
            "before_generator_count": len(before_active),
            "after_generator_count": len(active),
            "before_relator_count": before_count,
            "after_relator_count": after_count,
            "before_presentation_sha256": before_digest,
            "after_presentation_sha256": after_digest,
            "before_norm_words_sha256": before_norm_digest,
            "after_norm_words_sha256": after_norm_digest,
            "before_norm_empty_count": before_norm_empty,
            "after_norm_empty_count": after_norm_empty,
            # Store value snapshots.  In particular, ``new_to_old`` is
            # updated in place at the next step; retaining the live list
            # would silently rewrite every earlier event and invalidate
            # independent replay.
            "old_to_new": [list(row) for row in old_to_new],
            "new_to_old": [list(row) for row in new_to_old],
        })
    status = "UNKNOWN_STAGE_LIMIT" if len(events) == max_steps and active else "UNKNOWN_NO_ONE_OCCURRENCE_ELIMINATION"
    if not active:
        status = "COMPLETE_KERNEL_TRIVIAL"
    final_active = sorted(active)
    dense_map = {old: index for index, old in enumerate(final_active, 1)}

    def dense_word(word: list[int]) -> list[int]:
        out: list[int] = []
        for letter in word:
            ident = dense_map.get(abs(letter))
            if ident is None:
                raise ValueError("final word refers to eliminated generator")
            out.append(ident if letter > 0 else -ident)
        return out

    final_relators = [dense_word(word) for word in words]
    final_norm_words = [dense_word(word) for word in targets]
    final_old_to_dense = [dense_word(word) if word else [] for word in old_to_new]
    final_new_to_old = [new_to_old[old - 1] for old in final_active]
    all_norms_empty = all(not word for word in final_norm_words)
    if all_norms_empty:
        status = "B4_B_NORMS_CERTIFIED_PENDING_REPLAY"
    return {
        "status": status,
        "events": events,
        "initial_presentation_sha256": initial_digest,
        "final_active_generators": final_active,
        "final_generator_count": len(final_active),
        "final_dense_map": [[old, dense_map[old]] for old in final_active],
        "final_old_to_dense": final_old_to_dense,
        "final_dense_to_old": final_new_to_old,
        "final_relators": final_relators,
        "final_relators_sha256": digest(canonical_words(final_relators)),
        "final_norm_words": final_norm_words,
        "final_norm_words_sha256": digest(final_norm_words),
        "final_norm_empty_count": sum(not word for word in final_norm_words),
        "all_norms_empty": all_norms_empty,
        "active_generator_count": len(active),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--word-artifact", type=Path, default=DEFAULT_WORDS)
    parser.add_argument("--max-steps", type=int, default=34)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args(argv)
    if args.selftest:
        fixture = run_trace([[1, 2], [1, 1]], [[2], [-1]], 1)
        if fixture["status"] != "UNKNOWN_STAGE_LIMIT" or fixture["final_generator_count"] != 160:
            raise AssertionError("producer selftest stage contract drift")
        if len(fixture["events"]) != 1 or fixture["events"][0]["pivot"] != 1:
            raise AssertionError("producer selftest primitive drift")
        if len(fixture["final_old_to_dense"]) != RAW_GENERATORS or \
           len(fixture["final_dense_to_old"]) != 160:
            raise AssertionError("producer selftest dense-map drift")
        # Exercise two successive eliminations: the first event must retain
        # its own inverse-map snapshot after the second event mutates the
        # live map.  This is the regression that a JSON receipt must expose
        # rather than silently aliasing mutable Python lists.
        snapshots = run_trace([[1], [2]], [[1], [2]], 2)
        if snapshots["events"][0]["new_to_old"][:2] != [[], [2]] or \
           snapshots["events"][1]["new_to_old"][:2] != [[], []] or \
           len(snapshots["events"][0]["new_to_old"]) != RAW_GENERATORS:
            raise AssertionError("producer selftest map snapshot drift")
        print("D972_NORM_TZ_V2_PRODUCER_SELFTEST_PASS")
        return 0
    if args.output is None:
        parser.error("--output is required unless --selftest is supplied")
    relators = load_relators(args.input.resolve())
    rows, norms, word_sha = load_norms(args.word_artifact.resolve())
    pair_words, rs_rels, pair_id = build_rs(relators)
    norm_rs = [rewrite_rs(word, pair_id) for word in norms]
    if len(norm_rs) != NORM_COUNT:
        raise ValueError("norm RS count drift")
    if digest(pair_words) != PAIR_WORDS_SHA or digest(rs_rels) != RS_WORDS_SHA:
        raise ValueError("raw RS basis digest drift")
    if digest(norm_rs) != NORM_RS_SHA:
        raise ValueError("norm RS basis digest drift")
    result = run_trace(rs_rels, norm_rs, args.max_steps)
    result.update({
        "schema": SCHEMA,
        "basis_id": BASIS_ID,
        "gen_bits": list(GEN_BITS),
        "source_sha256": SOURCE_SHA,
        "relator_sha256": RELATOR_SHA,
        "word_artifact_sha256": word_sha,
        "normalized_rows_sha256": ROWS_SHA,
        "roof_norm_words_sha256": NORM_SHA,
        "original_relator_count": len(relators),
        "rs_generator_count": len(pair_words),
        "rs_relator_count": len(rs_rels),
        "rs_pair_words": pair_words,
        "rs_pair_words_sha256": digest(pair_words),
        "rs_relators": rs_rels,
        "rs_relators_sha256": digest(rs_rels),
        "norm_count": len(norms),
        "norm_rs_words": norm_rs,
        "norm_rs_words_sha256": digest(norm_rs),
        "max_steps": args.max_steps,
        "dense_target_max_generators": 127,
        "proof_level": "ELEMENTARY_TZ_NORM_AND_MAP_REPLAY_REQUIRED",
        "finite_quotient_claim": "NONE_UNLESS_ALL_NORMS_REPLAY_EMPTY",
    })
    args.output.resolve().parent.mkdir(parents=True, exist_ok=True)
    args.output.resolve().write_text(json.dumps(result, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": result["status"],
        "rs_generators": result["rs_generator_count"],
        "rs_relators": result["rs_relator_count"],
        "steps": len(result["events"]),
        "final_generators": result["final_generator_count"],
        "norm_empty": result["final_norm_empty_count"],
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
