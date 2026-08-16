#!/usr/bin/env python3
"""Independent checker for the fixed-basis B4 norm/Tietze trace.

This checker intentionally does not import the producer.  It reconstructs the
canonical six-generator input, the regular ``C2^5`` transversal, all 161
Schreier generators, 5056 relators, and all 972 exact norm words.  It then
replays the producer schema ``d972-b4-norm-tietze-trace/v2`` one elementary
Tietze step at a time.

The accepted trace is a *step-34 dense-input receipt*, not a finite-group
proof.  Every defining row, signed substitution, active-generator set,
presentation digest, norm digest, stable old-generator map, final dense map,
and final relator/norm list is checked.  A partial ledger, a finite all-pass
experiment, or a malformed alphabet is rejected rather than promoted.

Checker output schema:
``d972-b4-norm-tietze-dense-check/v1``.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "search" / "certs" / "d972_b4_p2_magnus_input_v2_20260816.json"
DEFAULT_WORDS = ROOT / "search" / "certs" / "d972_b4_word_key_artifact_v1_20260816.json"

TRACE_SCHEMA = "d972-b4-norm-tietze-trace/v2"
CHECK_SCHEMA = "d972-b4-norm-tietze-dense-check/v1"
SOURCE_SHA = "c61b2b77131127aca83a8d7c56b7fdadd2d519b040ea4d91093622c813c2b4a9"
RELATOR_SHA = "12fc1146dce5179c2b5fc44a3ceed6356a6b2c4835a564b55e9a9cd679fccd2e"
WORD_ARTIFACT_SHA = "564a921be8114bdeb963f679c121e8d9aa90e148c65e95e393874fcba843e9f9"
ROWS_SHA = "283bf9cc728ced084a3b276e4496fbbc69026589813a2f31caa0dcb7a3682930"
NORM_SHA = "ecf0cc8425bc24bdf6a8a352c223398221c4b179e09ee9a0bfe3dc888861683e"
TARGET_SHA = "9c77e6768feb7ffe7143abf18f753af70e81b8e9cc792910c30ae0075d3b1d62"
TUPLE_SHA = "32e78ca5b97cd8a6fa59a150dac77719c1b8cb527f0467570c4d284600465a91"
RAW_RS_SHA = "29c65a6cf9d0308e25ca462c752d7b540a6856e7d99d5d1d016919240b575c0e"
NORM_RS_SHA = "f7134e15e92c80a5ceeede38e94314539815a665ba7d279443208de1696041f8"

GEN_BITS = (1, 2, 4, 8, 16, 31)
RHO = ((-6, -5, -3), (3,), (5,), (-3, -2, -1), (-5, -4, -1), (1,))
RAW_GENERATORS = 161
RAW_RELATORS = 5056
RELATOR_INPUT_COUNT = 158
NORM_COUNT = 972
TRACE_STEPS = 34
DENSE_LIMIT = 127


def cjson(value: Any) -> bytes:
    """The canonical compact JSON byte encoding used by the artifacts."""

    return json.dumps(value, separators=(",", ":"), ensure_ascii=True).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(cjson(value)).hexdigest()


def file_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def strict_int(value: object, message: str) -> int:
    require(type(value) is int, message)
    return int(value)


def reduce_word(word: list[int]) -> list[int]:
    out: list[int] = []
    for letter in word:
        if out and out[-1] == -letter:
            out.pop()
        else:
            out.append(letter)
    return out


def inverse_word(word: list[int]) -> list[int]:
    return [-letter for letter in reversed(word)]


def canonical_words(words: list[list[int]]) -> list[list[int]]:
    return sorted(reduce_word(list(word)) for word in words if word)


def validate_signed_word(word: object, width: int | None, label: str,
                         *, allow_empty: bool = True) -> list[int]:
    require(isinstance(word, list), f"{label}: word is not a list")
    if not allow_empty:
        require(bool(word), f"{label}: empty word")
    result: list[int] = []
    for index, letter in enumerate(word):
        value = strict_int(letter, f"{label}[{index}]: non-integer letter")
        require(value != 0, f"{label}[{index}]: zero letter")
        if width is not None:
            require(abs(value) <= width, f"{label}[{index}]: alphabet drift")
        result.append(value)
    return result


def validate_word_list(words: object, width: int | None, label: str,
                       *, allow_empty_rows: bool = True) -> list[list[int]]:
    require(isinstance(words, list), f"{label}: not a list")
    return [validate_signed_word(word, width, f"{label}[{i}]",
                                 allow_empty=allow_empty_rows)
            for i, word in enumerate(words)]


def rho_word(word: list[int]) -> list[int]:
    out: list[int] = []
    for letter in word:
        require(1 <= abs(letter) <= 6, "rho input alphabet drift")
        image = list(RHO[abs(letter) - 1])
        if letter < 0:
            image = inverse_word(image)
        out.extend(image)
    return reduce_word(out)


def exact_norm(f2_word: list[int]) -> list[int]:
    base: list[int] = []
    for index, letter in enumerate(f2_word):
        require(type(letter) is int and letter != 0,
                f"F2 word letter {index} is not signed integer")
        if abs(letter) == 1:
            base.append(1 if letter > 0 else -1)
        elif abs(letter) == 2:
            base.append(4 if letter > 0 else -4)
        else:
            raise ValueError("F2 alphabet drift")
    current = reduce_word(base)
    orbit: list[list[int]] = []
    for _ in range(5):
        orbit.append(current)
        current = rho_word(current)
    result: list[int] = []
    for item in reversed(orbit):
        result = reduce_word(result + item)
    return result


def load_canonical(input_path: Path, words_path: Path) -> tuple[
        list[list[int]], list[list[int]], list[list[int]], list[list[int]], str]:
    """Load and pin source, raw RS presentation, and exact norm rows."""

    source_raw = input_path.read_bytes()
    require(hashlib.sha256(source_raw).hexdigest() == SOURCE_SHA,
            "canonical input SHA drift")
    source = json.loads(source_raw.decode("utf-8"))
    require(source.get("schema") == "d972-b4-p2-magnus-input/v2",
            "canonical input schema drift")
    raw_relators_obj = source.get("all_relators")
    require(isinstance(raw_relators_obj, list) and
            len(raw_relators_obj) == RELATOR_INPUT_COUNT,
            "canonical relator count drift")
    require(source.get("rho_words") == [list(row) for row in RHO],
            "canonical rho drift")
    require(source.get("all_relators_sha256") == RELATOR_SHA,
            "canonical relator pin drift")
    relators: list[list[int]] = []
    for row_index, word in enumerate(raw_relators_obj):
        row = validate_signed_word(word, 6, f"canonical relator {row_index}",
                                   allow_empty=False)
        relators.append(row)
    require(digest(relators) == RELATOR_SHA, "canonical relator digest drift")

    words_raw = words_path.read_bytes()
    words_sha = hashlib.sha256(words_raw).hexdigest()
    require(words_sha == WORD_ARTIFACT_SHA, "word artifact SHA drift")
    artifact = json.loads(words_raw.decode("utf-8"))
    require(artifact.get("schema") == "d972-b4-word-key-artifact/v1" and
            artifact.get("count") == NORM_COUNT,
            "word artifact schema/count drift")
    require(artifact.get("source_target_key_digest") == TARGET_SHA and
            artifact.get("frozen_tuple_sha256") == TUPLE_SHA,
            "word artifact target pin drift")
    rows_obj = artifact.get("rows")
    require(isinstance(rows_obj, list) and len(rows_obj) == NORM_COUNT,
            "word row count drift")
    normalized: list[list[Any]] = []
    for row_index, row_obj in enumerate(rows_obj):
        require(isinstance(row_obj, list) and len(row_obj) == 3,
                f"word row {row_index} shape drift")
        mode, key, f2_word_obj = row_obj
        require(type(mode) is int and isinstance(key, list),
                f"word row {row_index} metadata drift")
        f2_word = validate_signed_word(f2_word_obj, 2,
                                       f"word row {row_index} F2 word")
        require(all(abs(letter) <= 2 for letter in f2_word),
                f"word row {row_index} F2 alphabet drift")
        normalized.append([mode, key, f2_word])
    require(artifact.get("canonical_bytes_sha256") == ROWS_SHA and
            digest(normalized) == ROWS_SHA,
            "word row digest drift")
    norms = [exact_norm(row[2]) for row in normalized]
    require(digest(norms) == NORM_SHA, "exact norm digest drift")

    pair_words, raw_rs, pair_id = build_raw_rs(relators)
    require(digest(raw_rs) == RAW_RS_SHA, "raw RS digest drift")
    norm_rs: list[list[int]] = []
    for row_index, word in enumerate(norms):
        rewritten = rewrite_rs(word, 0, pair_id)
        require(all(abs(letter) <= RAW_GENERATORS for letter in rewritten),
                f"norm RS row {row_index} alphabet drift")
        norm_rs.append(rewritten)
    require(len(norm_rs) == NORM_COUNT and digest(norm_rs) == NORM_RS_SHA,
            "norm RS digest drift")
    return pair_words, raw_rs, norms, norm_rs, words_sha


def transversal(mask: int) -> list[int]:
    return [bit + 1 for bit in range(5) if mask & (1 << bit)]


def toggle(mask: int, bit: int) -> int:
    # The sixth quotient image is the all-ones mask; XOR is still the exact
    # C2^5 transition, including bit=31.
    require(0 <= mask < 32 and bit in GEN_BITS, "quotient mask drift")
    return mask ^ bit


def build_raw_rs(relators: list[list[int]]) -> tuple[
        list[list[int]], list[list[int]], list[list[int]]]:
    pair_id = [[0] * 6 for _ in range(32)]
    pair_words: list[list[int]] = []
    reps = [transversal(mask) for mask in range(32)]
    for mask in range(32):
        for gen, bit in enumerate(GEN_BITS, 1):
            raw = reps[mask] + [gen] + inverse_word(reps[toggle(mask, bit)])
            word = reduce_word(raw)
            if word:
                pair_words.append(word)
                pair_id[mask][gen - 1] = len(pair_words)
    require(len(pair_words) == RAW_GENERATORS, "raw RS generator count drift")

    raw_rs: list[list[int]] = []
    for start in range(32):
        for relator_index, relator in enumerate(relators):
            mask = start
            rewritten: list[int] = []
            for letter in relator:
                gen = abs(letter)
                require(1 <= gen <= 6, "raw relator alphabet drift")
                bit = GEN_BITS[gen - 1]
                if letter > 0:
                    ident = pair_id[mask][gen - 1]
                    if ident:
                        rewritten.append(ident)
                    mask = toggle(mask, bit)
                else:
                    mask = toggle(mask, bit)
                    ident = pair_id[mask][gen - 1]
                    if ident:
                        rewritten.append(-ident)
            require(mask == start,
                    f"RS relator endpoint drift at {start}/{relator_index}")
            rewritten = reduce_word(rewritten)
            if rewritten:
                raw_rs.append(rewritten)
    require(len(raw_rs) == RAW_RELATORS, "raw RS relator count drift")
    return pair_words, raw_rs, pair_id


def rewrite_rs(word: list[int], start: int,
               pair_id: list[list[int]]) -> list[int]:
    mask = start
    out: list[int] = []
    for letter in word:
        gen = abs(letter)
        require(1 <= gen <= 6, "RS word alphabet drift")
        bit = GEN_BITS[gen - 1]
        if letter > 0:
            ident = pair_id[mask][gen - 1]
            if ident:
                out.append(ident)
            mask = toggle(mask, bit)
        else:
            mask = toggle(mask, bit)
            ident = pair_id[mask][gen - 1]
            if ident:
                out.append(-ident)
    require(mask == start, "RS word endpoint drift")
    return reduce_word(out)


def substitute_word(word: list[int], pivot_letter: int,
                    replacement: list[int]) -> list[int]:
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


def substitute_words(words: list[list[int]], pivot_letter: int,
                     replacement: list[int]) -> list[list[int]]:
    result: list[list[int]] = []
    for word in words:
        reduced = substitute_word(word, pivot_letter, replacement)
        if reduced:
            result.append(reduced)
    return result


def substitute_preserve(words: list[list[int]], pivot_letter: int,
                        replacement: list[int]) -> list[list[int]]:
    return [substitute_word(word, pivot_letter, replacement) for word in words]


def choose_event(words: list[list[int]], active: set[int]) -> tuple[
        int, int, list[int], int] | None:
    best: tuple[tuple[int, int, int, int], tuple[int, int, list[int], int]] | None = None
    for relator_index, word in enumerate(words):
        counts = Counter(abs(letter) for letter in word)
        for position, letter in enumerate(word):
            pivot = abs(letter)
            if pivot not in active or counts[pivot] != 1:
                continue
            key = (len(word), pivot, position, relator_index)
            candidate = (relator_index, position, list(word), letter)
            if best is None or key < best[0]:
                best = (key, candidate)
    return None if best is None else best[1]


def validate_stable_map(map_words: object, active: set[int], width: int,
                        label: str) -> list[list[int]]:
    require(isinstance(map_words, list) and len(map_words) == width,
            f"{label}: width drift")
    result: list[list[int]] = []
    for index, word in enumerate(map_words):
        row = validate_signed_word(word, width, f"{label}[{index}]")
        require(all(abs(letter) in active for letter in row),
                f"{label}[{index}]: eliminated generator reference")
        result.append(row)
    return result


def same_field(event: dict[str, Any], key: str, expected: Any) -> None:
    require(key in event, f"trace event missing {key}")
    require(event[key] == expected, f"trace event {key} mismatch")


def replay_events(events_obj: object, initial_words: list[list[int]],
                  initial_norms: list[list[int]], width: int,
                  required_steps: int | None) -> dict[str, Any]:
    """Replay every elementary event and return the independently computed state."""

    require(isinstance(events_obj, list), "trace events are not a list")
    words = [reduce_word(list(word)) for word in initial_words if word]
    targets = [reduce_word(list(word)) for word in initial_norms]
    active = set(range(1, width + 1))
    old_to_new = [[index] for index in range(1, width + 1)]
    new_to_old = [[index] for index in range(1, width + 1)]
    initial_digest = digest(canonical_words(words))

    for event_index, event_obj in enumerate(events_obj):
        require(isinstance(event_obj, dict), f"event {event_index} is not an object")
        event = event_obj
        expected_step = event_index + 1
        same_field(event, "step", expected_step)
        selected = choose_event(words, active)
        require(selected is not None, f"event {expected_step}: no legal event")
        relator_index, position, defining, pivot_letter = selected
        pivot = abs(pivot_letter)
        same_field(event, "defining_relator_index", relator_index)
        same_field(event, "pivot_position", position)
        same_field(event, "defining_relator", defining)
        same_field(event, "pivot_letter", pivot_letter)
        same_field(event, "pivot", pivot)
        require(sum(abs(letter) == pivot for letter in defining) == 1,
                f"event {expected_step}: pivot is not unique")
        require(pivot in active, f"event {expected_step}: inactive pivot")

        replacement = defining[position + 1:] + defining[:position]
        positive_substitution = (inverse_word(replacement)
                                 if pivot_letter > 0 else replacement)
        negative_substitution = (replacement
                                 if pivot_letter > 0
                                 else inverse_word(replacement))
        same_field(event, "replacement_word", replacement)
        same_field(event, "positive_substitution", positive_substitution)
        same_field(event, "negative_substitution", negative_substitution)
        require(all(abs(letter) in active for letter in replacement),
                f"event {expected_step}: replacement alphabet drift")
        # This is the explicit defining-row-removal gate.  It catches a
        # forged defining index even if the aggregate presentation digest is
        # forged along with it.
        require(substitute_word(defining, pivot_letter, replacement) == [],
                f"event {expected_step}: defining row was not removed")

        before_active = sorted(active)
        before_presentation = canonical_words(words)
        before_norm_empty = sum(not word for word in targets)
        same_field(event, "before_active_generators", before_active)
        same_field(event, "before_generator_count", len(before_active))
        same_field(event, "before_relator_count", len(before_presentation))
        same_field(event, "before_presentation_sha256", digest(before_presentation))
        same_field(event, "before_norm_words_sha256", digest(targets))
        same_field(event, "before_norm_empty_count", before_norm_empty)

        next_words = substitute_words(words, pivot_letter, replacement)
        next_targets = substitute_preserve(targets, pivot_letter, replacement)
        next_old_to_new = substitute_preserve(old_to_new, pivot_letter, replacement)
        next_active = active - {pivot}
        next_new_to_old = [list(row) for row in new_to_old]
        next_new_to_old[pivot - 1] = []
        after_active = sorted(next_active)
        after_presentation = canonical_words(next_words)
        after_norm_empty = sum(not word for word in next_targets)
        same_field(event, "after_active_generators", after_active)
        same_field(event, "after_generator_count", len(after_active))
        same_field(event, "after_relator_count", len(after_presentation))
        same_field(event, "after_presentation_sha256", digest(after_presentation))
        same_field(event, "after_norm_words_sha256", digest(next_targets))
        same_field(event, "after_norm_empty_count", after_norm_empty)
        event_old_to_new = validate_stable_map(event.get("old_to_new"),
                                               next_active, width,
                                               f"event {expected_step} old_to_new")
        event_new_to_old = validate_stable_map(event.get("new_to_old"),
                                               set(range(1, width + 1)), width,
                                               f"event {expected_step} new_to_old")
        same_field(event, "old_to_new", next_old_to_new)
        same_field(event, "new_to_old", next_new_to_old)
        require(event_old_to_new == next_old_to_new,
                f"event {expected_step}: old_to_new mismatch")
        require(event_new_to_old == next_new_to_old,
                f"event {expected_step}: new_to_old mismatch")

        words, targets = next_words, next_targets
        active = next_active
        old_to_new, new_to_old = next_old_to_new, next_new_to_old

    if required_steps is not None:
        require(len(events_obj) == required_steps,
                f"partial elimination ledger: {len(events_obj)} != {required_steps}")
    return {
        "words": words,
        "targets": targets,
        "active": active,
        "old_to_new": old_to_new,
        "new_to_old": new_to_old,
        "initial_presentation_sha256": initial_digest,
    }


def dense_word(word: list[int], dense: dict[int, int], label: str) -> list[int]:
    result: list[int] = []
    for index, letter in enumerate(word):
        mapped = dense.get(abs(letter))
        require(mapped is not None,
                f"{label}[{index}]: eliminated generator in final word")
        result.append(mapped if letter > 0 else -mapped)
    return result


def check_final_artifact(receipt: dict[str, Any], replay: dict[str, Any],
                         width: int) -> dict[str, Any]:
    active = sorted(replay["active"])
    require(active == receipt.get("final_active_generators"),
            "final active-generator list mismatch")
    require(receipt.get("final_generator_count") == len(active),
            "final generator count mismatch")
    require(len(active) <= DENSE_LIMIT,
            f"final generator count exceeds dense target: {len(active)}")
    dense = {old: index for index, old in enumerate(active, 1)}
    dense_pairs = [[old, dense[old]] for old in active]
    same_field(receipt, "final_dense_map", dense_pairs)
    require(receipt.get("dense_target_max_generators") == DENSE_LIMIT,
            "dense target bound drift")

    final_relators = [dense_word(word, dense, "final_relator")
                      for word in replay["words"]]
    final_norms = [dense_word(word, dense, "final_norm")
                   for word in replay["targets"]]
    same_field(receipt, "final_relators", final_relators)
    same_field(receipt, "final_norm_words", final_norms)
    same_field(receipt, "final_relators_sha256", digest(canonical_words(final_relators)))
    same_field(receipt, "final_norm_words_sha256", digest(final_norms))
    same_field(receipt, "final_norm_empty_count", sum(not word for word in final_norms))
    same_field(receipt, "all_norms_empty", all(not word for word in final_norms))

    old_to_dense_words = [dense_word(word, dense, "old_to_dense") if word else []
                          for word in replay["old_to_new"]]
    dense_to_old_words = [list(replay["new_to_old"][old - 1]) for old in active]
    dense_inverse_pairs = [[index, old] for index, old in enumerate(active, 1)]
    require(len(old_to_dense_words) == width and
            len(dense_to_old_words) == len(active),
            "dense old/new map width drift")
    dense_map_sha = digest([dense_pairs, dense_inverse_pairs])
    optional_old = receipt.get("final_old_to_dense")
    if optional_old is not None:
        require(optional_old == old_to_dense_words, "final old_to_dense mismatch")
    optional_new = receipt.get("final_new_to_old")
    if optional_new is not None:
        require(optional_new == dense_to_old_words, "final new_to_old mismatch")
    optional_sha = receipt.get("dense_map_sha256")
    if optional_sha is not None:
        require(optional_sha == dense_map_sha, "dense map digest mismatch")
    return {
        "final_relators": final_relators,
        "final_norm_words": final_norms,
        "final_relators_sha256": digest(canonical_words(final_relators)),
        "final_norm_words_sha256": digest(final_norms),
        "final_norm_empty_count": sum(not word for word in final_norms),
        "all_norms_empty": all(not word for word in final_norms),
        "dense_old_to_new": dense_pairs,
        "dense_new_to_old": dense_inverse_pairs,
        "dense_new_to_old_words": dense_to_old_words,
        "dense_old_to_dense_words": old_to_dense_words,
        "dense_map_sha256": dense_map_sha,
    }


def expected_status(active: set[int], all_norms_empty: bool,
                    step_count: int) -> str:
    if not active:
        return "COMPLETE_KERNEL_TRIVIAL"
    if all_norms_empty:
        return "B4_B_NORMS_CERTIFIED_PENDING_REPLAY"
    if step_count == TRACE_STEPS:
        return "UNKNOWN_STAGE_LIMIT"
    return "UNKNOWN_NO_ONE_OCCURRENCE_ELIMINATION"


def validate_receipt(receipt_path: Path, input_path: Path,
                     words_path: Path) -> dict[str, Any]:
    pair_words, raw_rs, _norms, norm_rs, words_sha = load_canonical(
        input_path, words_path)
    receipt_raw = receipt_path.read_bytes()
    receipt_obj = json.loads(receipt_raw.decode("utf-8"))
    require(isinstance(receipt_obj, dict), "trace receipt is not an object")
    receipt: dict[str, Any] = receipt_obj
    require(receipt.get("schema") == TRACE_SCHEMA, "trace schema drift")
    for field, expected in (
        ("source_sha256", SOURCE_SHA),
        ("relator_sha256", RELATOR_SHA),
        ("word_artifact_sha256", words_sha),
        ("normalized_rows_sha256", ROWS_SHA),
        ("roof_norm_words_sha256", NORM_SHA),
        ("rs_relators_sha256", RAW_RS_SHA),
        ("norm_rs_words_sha256", NORM_RS_SHA),
    ):
        require(receipt.get(field) == expected, f"trace {field} drift")
    for field, expected in (
        ("original_relator_count", RELATOR_INPUT_COUNT),
        ("rs_generator_count", RAW_GENERATORS),
        ("rs_relator_count", RAW_RELATORS),
        ("norm_count", NORM_COUNT),
        ("max_steps", TRACE_STEPS),
        ("dense_target_max_generators", DENSE_LIMIT),
    ):
        require(receipt.get(field) == expected, f"trace {field} drift")
    require(receipt.get("proof_level") ==
            "ELEMENTARY_TZ_NORM_AND_MAP_REPLAY_REQUIRED",
            "trace proof-level drift")
    require(receipt.get("finite_quotient_claim") ==
            "NONE_UNLESS_ALL_NORMS_REPLAY_EMPTY",
            "trace finite-claim drift")

    receipt_pairs = validate_word_list(receipt.get("rs_pair_words"), RAW_GENERATORS,
                                       "receipt rs_pair_words", allow_empty_rows=False)
    require(receipt_pairs == pair_words, "receipt Schreier pair words mismatch")
    receipt_rs = validate_word_list(receipt.get("rs_relators"), RAW_GENERATORS,
                                    "receipt rs_relators", allow_empty_rows=False)
    require(receipt_rs == raw_rs, "receipt raw RS relators mismatch")
    receipt_norm_rs = validate_word_list(receipt.get("norm_rs_words"), RAW_GENERATORS,
                                         "receipt norm_rs_words")
    require(receipt_norm_rs == norm_rs, "receipt norm RS words mismatch")
    require(receipt.get("rs_pair_words_sha256") == digest(pair_words),
            "receipt Schreier pair digest mismatch")
    require(receipt.get("rs_relators_sha256") == digest(raw_rs) == RAW_RS_SHA,
            "receipt raw RS digest mismatch")
    require(receipt.get("norm_rs_words_sha256") == digest(norm_rs) == NORM_RS_SHA,
            "receipt norm RS digest mismatch")

    events_obj = receipt.get("events")
    replay = replay_events(events_obj, raw_rs, norm_rs, RAW_GENERATORS,
                           TRACE_STEPS)
    dense = check_final_artifact(receipt, replay, RAW_GENERATORS)
    status = expected_status(replay["active"], dense["all_norms_empty"],
                             len(events_obj))
    require(receipt.get("status") == status, "trace status drift")
    same_field(receipt, "initial_presentation_sha256",
               replay["initial_presentation_sha256"])
    same_field(receipt, "active_generator_count", len(replay["active"]))

    result = {
        "schema": CHECK_SCHEMA,
        "status": status,
        "proof_level": "INDEPENDENT_FIXED_BASIS_TZ_AND_DENSE_REPLAY",
        "producer_receipt_sha256": hashlib.sha256(receipt_raw).hexdigest(),
        "source_sha256": SOURCE_SHA,
        "relator_sha256": RELATOR_SHA,
        "word_artifact_sha256": words_sha,
        "normalized_rows_sha256": ROWS_SHA,
        "roof_norm_words_sha256": NORM_SHA,
        "raw_rs_relators_sha256": RAW_RS_SHA,
        "norm_rs_words_sha256": NORM_RS_SHA,
        "raw_rs_generator_count": RAW_GENERATORS,
        "raw_rs_relator_count": RAW_RELATORS,
        "norm_count": NORM_COUNT,
        "steps_replayed": len(events_obj),
        "final_generator_count": len(replay["active"]),
        "final_relators_sha256": dense["final_relators_sha256"],
        "final_norm_words_sha256": dense["final_norm_words_sha256"],
        "final_norm_empty_count": dense["final_norm_empty_count"],
        "all_norms_empty": dense["all_norms_empty"],
        "dense_old_to_new": dense["dense_old_to_new"],
        "dense_new_to_old": dense["dense_new_to_old"],
        "dense_new_to_old_words": dense["dense_new_to_old_words"],
        "dense_old_to_dense_words": dense["dense_old_to_dense_words"],
        "dense_map_sha256": dense["dense_map_sha256"],
        "independent_raw_rs_replay": True,
        "independent_norm_replay": True,
        "independent_tietze_replay": True,
        "independent_dense_map_replay": True,
        "terminal_claim": "NONE; KBMAG/AutomaticStructure replay still required",
    }
    return result


def _fixture_event(words: list[list[int]], norms: list[list[int]],
                   width: int) -> dict[str, Any]:
    """Construct one honest synthetic event for negative selftests only."""

    active = set(range(1, width + 1))
    selected = choose_event(words, active)
    require(selected is not None, "fixture has no event")
    relator_index, position, defining, pivot_letter = selected
    pivot = abs(pivot_letter)
    replacement = defining[position + 1:] + defining[:position]
    before_active = sorted(active)
    before_presentation = canonical_words(words)
    before_maps = [[index] for index in range(1, width + 1)]
    before_inverse = [[index] for index in range(1, width + 1)]
    next_words = substitute_words(words, pivot_letter, replacement)
    next_norms = substitute_preserve(norms, pivot_letter, replacement)
    next_maps = substitute_preserve(before_maps, pivot_letter, replacement)
    next_active = active - {pivot}
    next_inverse = [list(row) for row in before_inverse]
    next_inverse[pivot - 1] = []
    return {
        "step": 1,
        "pivot": pivot,
        "pivot_letter": pivot_letter,
        "defining_relator_index": relator_index,
        "defining_relator": defining,
        "pivot_position": position,
        "replacement_word": replacement,
        "positive_substitution": (inverse_word(replacement)
                                   if pivot_letter > 0 else replacement),
        "negative_substitution": (replacement
                                   if pivot_letter > 0
                                   else inverse_word(replacement)),
        "before_active_generators": before_active,
        "after_active_generators": sorted(next_active),
        "before_generator_count": len(before_active),
        "after_generator_count": len(next_active),
        "before_relator_count": len(before_presentation),
        "after_relator_count": len(canonical_words(next_words)),
        "before_presentation_sha256": digest(before_presentation),
        "after_presentation_sha256": digest(canonical_words(next_words)),
        "before_norm_words_sha256": digest(norms),
        "after_norm_words_sha256": digest(next_norms),
        "before_norm_empty_count": sum(not word for word in norms),
        "after_norm_empty_count": sum(not word for word in next_norms),
        "old_to_new": next_maps,
        "new_to_old": next_inverse,
    }


def selftest() -> None:
    """Run only tiny fixtures; never load the canonical 5056-row input."""

    require(reduce_word([1, -1, 2, 2, -2]) == [2], "selftest reduction")
    require(toggle(0, 31) == 31 and toggle(31, 31) == 0,
            "selftest quotient toggle")
    fixture_words = [[1, 2], [2, -1]]
    fixture_norms = [[1], [-1]]
    good_event = _fixture_event(fixture_words, fixture_norms, 2)
    replay_events([good_event], fixture_words, fixture_norms, 2, 1)

    def must_reject(thunk: Any, label: str) -> None:
        try:
            thunk()
        except (ValueError, TypeError, KeyError, IndexError):
            return
        raise AssertionError(f"negative selftest accepted: {label}")

    forged_step = json.loads(json.dumps(good_event))
    forged_step["pivot"] = 2
    must_reject(lambda: replay_events([forged_step], fixture_words,
                                      fixture_norms, 2, 1), "forged step")

    forged_map = json.loads(json.dumps(good_event))
    forged_map["old_to_new"][0] = [2, 2]
    must_reject(lambda: replay_events([forged_map], fixture_words,
                                      fixture_norms, 2, 1), "forged map")

    forged_digest = json.loads(json.dumps(good_event))
    forged_digest["after_norm_words_sha256"] = "0" * 64
    must_reject(lambda: replay_events([forged_digest], fixture_words,
                                      fixture_norms, 2, 1), "forged digest")

    must_reject(lambda: validate_signed_word([1, 3], 2, "fixture F2"),
                "forged alphabet")
    must_reject(lambda: replay_events([], fixture_words, fixture_norms, 2, 1),
                "partial ledger")

    replay = replay_events([good_event], fixture_words, fixture_norms, 2, 1)
    dense = {2: 1}
    forged_final = {
        "final_active_generators": [2],
        "final_generator_count": 1,
        "final_dense_map": [[2, 1]],
        "dense_target_max_generators": 127,
        "final_relators": [[1]],
        "final_norm_words": [[-1], [1]],
        "final_relators_sha256": digest([[1]]),
        "final_norm_words_sha256": digest([[-1], [1]]),
        "final_norm_empty_count": 0,
        "all_norms_empty": False,
    }
    # A final artifact with the wrong relator digest/contents must not be
    # accepted merely because its dense map is plausible.
    must_reject(lambda: check_final_artifact(forged_final, replay, 2),
                "forged final artifact")
    print("D972_B4_NORM_TIETZE_DENSE_SELFTEST_PASS",
          "step=BLOCKED map=BLOCKED digest=BLOCKED alphabet=BLOCKED partial=BLOCKED")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("trace", type=Path, nargs="?")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--word-artifact", type=Path, default=DEFAULT_WORDS)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args(argv)
    if args.selftest:
        selftest()
        return 0
    if args.trace is None or args.output is None:
        parser.error("trace and --output are required unless --selftest is used")
    try:
        result = validate_receipt(args.trace.resolve(), args.input.resolve(),
                                  args.word_artifact.resolve())
        output_path = args.output.resolve()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n",
                                encoding="utf-8")
        print("D972_B4_NORM_TIETZE_DENSE_CHECK",
              f"status={result['status']}",
              f"steps={result['steps_replayed']}",
              f"final_generators={result['final_generator_count']}",
              f"norm_empty={result['final_norm_empty_count']}/{NORM_COUNT}",
              f"output={output_path}")
        return 0
    except (OSError, TypeError, ValueError, KeyError, IndexError,
            json.JSONDecodeError) as exc:
        print(f"D972_B4_NORM_TIETZE_DENSE_CHECK_ERROR {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
