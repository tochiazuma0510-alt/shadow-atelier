#!/usr/bin/env python3
"""Independent F6 checker for the bounded B4 IdRel logged lane.

The checker intentionally shares no GAP helper.  It reloads the frozen
six-generator presentation and 972 roof words, recomputes the exact norm
words, expands every signed IdRel log in the free group, and checks

    product(rel_i ** conjugator) + reduced == original

by integer-word free reduction.  A valid UNKNOWN receipt is not promoted to
an A or B conclusion.  Exit status is 0 for an independently accepted
terminal receipt, 2
for a well-formed but nonterminal/partial receipt, and 1 for a bad receipt.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Iterable, Sequence

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "search/certs/d972_b4_p2_magnus_input_v2_20260816.json"
DEFAULT_WORDS = ROOT / "search/certs/d972_b4_word_key_artifact_v1_20260816.json"

RELATOR_SHA = "12fc1146dce5179c2b5fc44a3ceed6356a6b2c4835a564b55e9a9cd679fccd2e"
ROOF_SHA = "3015b4e00a02ca2a9d6183dad4cb7ddabfd21ef03828837198aa96b2dc3461f8"
TARGET_SHA = "9c77e6768feb7ffe7143abf18f753af70e81b8e9cc792910c30ae0075d3b1d62"
NORM_SHA = "ecf0cc8425bc24bdf6a8a352c223398221c4b179e09ee9a0bfe3dc888861683e"
WORD_CANONICAL_SHA = "283bf9cc728ced084a3b276e4496fbbc69026589813a2f31caa0dcb7a3682930"

Word = list[int]


def compact(value: Any) -> bytes:
    return json.dumps(value, separators=(",", ":"), ensure_ascii=True).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(compact(value)).hexdigest()


def free_reduce(word: Iterable[int]) -> Word:
    out: Word = []
    for letter in word:
        if out and out[-1] == -letter:
            out.pop()
        else:
            out.append(letter)
    return out


def inverse(word: Sequence[int]) -> Word:
    return [-x for x in reversed(word)]


def validate_signed_word(word: Any, alphabet: int, where: str) -> Word:
    if not isinstance(word, list) or any(
        not isinstance(x, int) or isinstance(x, bool) or x == 0 or abs(x) > alphabet
        for x in word
    ):
        raise ValueError(f"{where}: signed-word shape drift")
    return list(word)


def rho_substitute(word: Sequence[int], rho: Sequence[Sequence[int]]) -> Word:
    out: Word = []
    for letter in word:
        image = list(rho[abs(letter) - 1])
        out = free_reduce(out + (inverse(image) if letter < 0 else image))
    return out


def exact_norm(f2word: Sequence[int], rho: Sequence[Sequence[int]]) -> Word:
    mapped: Word = []
    for letter in f2word:
        if abs(letter) == 1:
            mapped.append(1 if letter > 0 else -1)
        elif abs(letter) == 2:
            mapped.append(4 if letter > 0 else -4)
        else:
            raise ValueError("F2 norm alphabet drift")
    mapped = free_reduce(mapped)
    orbit: list[Word] = []
    current = mapped
    for _ in range(5):
        orbit.append(current)
        current = rho_substitute(current, rho)
    out: Word = []
    for item in reversed(orbit):
        out = free_reduce(out + item)
    return out


def load_frozen(input_path: Path, words_path: Path) -> tuple[list[Word], list[Word], list[int], dict[str, Any]]:
    source = json.loads(input_path.read_text(encoding="utf-8"))
    if source.get("schema") != "d972-b4-p2-magnus-input/v2":
        raise ValueError("input schema drift")
    relators_raw = source.get("all_relators")
    roofs_raw = source.get("roof_words")
    rho = source.get("rho_words")
    if not isinstance(relators_raw, list) or len(relators_raw) != 158:
        raise ValueError("relator count drift")
    if not isinstance(roofs_raw, list) or len(roofs_raw) != 972:
        raise ValueError("roof count drift")
    if not isinstance(rho, list) or len(rho) != 6:
        raise ValueError("rho count drift")
    relators = [validate_signed_word(w, 6, f"relator[{i}]") for i, w in enumerate(relators_raw)]
    roofs = [validate_signed_word(w, 2, f"roof[{i}]") for i, w in enumerate(roofs_raw)]
    rho_words = [validate_signed_word(w, 6, f"rho[{i}]") for i, w in enumerate(rho)]
    if source.get("all_relators_sha256") != RELATOR_SHA or digest(relators) != RELATOR_SHA:
        raise ValueError("relator digest drift")
    if source.get("roof_words_sha256") != ROOF_SHA or digest(roofs) != ROOF_SHA:
        raise ValueError("roof digest drift")
    if source.get("target_key_digest") != TARGET_SHA:
        raise ValueError("target-key digest drift")
    keys = source.get("target_keys")
    if not isinstance(keys, list) or len(keys) != 972:
        raise ValueError("target-key row count drift")
    target_bytes = ("\n".join(sorted(str(x) for x in keys)) + "\n").encode()
    if hashlib.sha256(target_bytes).hexdigest() != TARGET_SHA:
        raise ValueError("target-key rows digest drift")

    word_obj = json.loads(words_path.read_text(encoding="utf-8"))
    if word_obj.get("schema") != "d972-b4-word-key-artifact/v1":
        raise ValueError("word artifact schema drift")
    if word_obj.get("count") != 972 or word_obj.get("source_target_key_digest") != TARGET_SHA:
        raise ValueError("word artifact count/source drift")
    if word_obj.get("canonical_bytes_sha256") != WORD_CANONICAL_SHA:
        raise ValueError("word artifact canonical digest drift")
    rows = word_obj.get("rows")
    if not isinstance(rows, list) or len(rows) != 972:
        raise ValueError("word artifact row count drift")
    artifact_roofs: list[Word] = []
    for i, row in enumerate(rows):
        if not isinstance(row, list) or len(row) != 3:
            raise ValueError(f"word artifact row {i}: shape drift")
        artifact_roofs.append(validate_signed_word(row[2], 2, f"word row[{i}].f2"))
    if artifact_roofs != roofs:
        raise ValueError("word artifact and canonical roof windows disagree")

    norms = [exact_norm(w, rho_words) for w in roofs]
    if digest(norms) != NORM_SHA:
        raise ValueError("exact norm digest drift")
    unique: list[Word] = []
    duplicate_map: list[int] = []
    positions: dict[tuple[int, ...], int] = {}
    for word in norms:
        key = tuple(word)
        if key not in positions:
            positions[key] = len(unique) + 1
            unique.append(word)
        duplicate_map.append(positions[key])
    if len(unique) != 486 or len(duplicate_map) != 972:
        raise ValueError("unique norm count drift")
    return relators, unique, duplicate_map, source


def proof_word(relators: Sequence[Word], reduced: Sequence[int], log: Any) -> Word:
    if not isinstance(log, list):
        raise ValueError("log is not a list")
    out: Word = []
    for j, entry in enumerate(log):
        if not isinstance(entry, list) or len(entry) != 2:
            raise ValueError(f"log entry {j}: shape drift")
        index, conjugator = entry
        if not isinstance(index, int) or isinstance(index, bool) or index == 0 or abs(index) > len(relators):
            raise ValueError(f"log entry {j}: relator index drift")
        conjugator = validate_signed_word(conjugator, 6, f"log entry {j}.conjugator")
        relator = relators[abs(index) - 1]
        if index < 0:
            relator = inverse(relator)
        # GAP's group exponent convention is c^-1 r c.
        out = free_reduce(out + inverse(conjugator) + relator + conjugator)
    return free_reduce(out + validate_signed_word(reduced, 6, "reduced"))


def verify_duplicate_map(receipt: dict[str, Any], canonical_unique: Sequence[Word], canonical_map: Sequence[int]) -> None:
    if receipt.get("generator_count") != 6 or receipt.get("relator_count") != 158:
        raise ValueError("presentation size drift")
    if receipt.get("norm_count") != 972 or receipt.get("unique_norm_count") != 486:
        raise ValueError("norm count drift")
    got = receipt.get("duplicate_map")
    if got != list(canonical_map):
        raise ValueError("duplicate map is not the frozen complete 972-row map")
    for value in got:
        if not isinstance(value, int) or not 1 <= value <= len(canonical_unique):
            raise ValueError("duplicate map index drift")


def _positive_cap(value: Any, name: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
        raise ValueError(f"{name} cap drift")
    return value


def _validate_filter_audit(value: Any, where: str) -> None:
    if not isinstance(value, list):
        raise ValueError(f"{where}: filter audit missing")
    for i, item in enumerate(value):
        if not isinstance(item, dict):
            raise ValueError(f"{where}: filter audit row {i} shape drift")
        if not isinstance(item.get("stage"), int) or isinstance(item.get("stage"), bool) or item["stage"] < 0:
            raise ValueError(f"{where}: filter audit stage drift")
        if item.get("phase") not in ("initial", "onepass", "rewrite"):
            raise ValueError(f"{where}: filter audit phase drift")
        count = item.get("invalid_count")
        if not isinstance(count, int) or isinstance(count, bool) or count < 0:
            raise ValueError(f"{where}: filter audit count drift")
        digest_value = item.get("invalid_digest")
        if (
            not isinstance(digest_value, str)
            or len(digest_value) != 64
            or any(c not in "0123456789abcdef" for c in digest_value)
        ):
            raise ValueError(f"{where}: filter audit digest drift")


def verify_stage(
    stage: dict[str, Any],
    relators: Sequence[Word],
    unique: Sequence[Word],
    expected_caps: dict[str, Any] | None = None,
) -> tuple[int, bool]:
    if stage.get("schema") != "d972-b4-u-idrel-direct-logged-stage/v1":
        raise ValueError("stage schema drift")
    if stage.get("generator_count") != 6 or stage.get("relator_count") != 158:
        raise ValueError("stage presentation size drift")
    if stage.get("relator_sha256") != RELATOR_SHA or stage.get("norm_sha256") != NORM_SHA:
        raise ValueError("stage source digest drift")
    _validate_filter_audit(stage.get("filter_audit"), "stage")
    max_rules = _positive_cap(stage.get("max_rules"), "max_rules")
    max_log_length = _positive_cap(stage.get("max_log_length"), "max_log_length")
    max_conjugator_length = _positive_cap(
        stage.get("max_conjugator_length"), "max_conjugator_length"
    )
    max_log_letters = _positive_cap(stage.get("max_log_letters"), "max_log_letters")
    max_reduced_length = _positive_cap(stage.get("max_reduced_length"), "max_reduced_length")
    if expected_caps is not None:
        for name, value in (
            ("max_rules", max_rules),
            ("max_log_length", max_log_length),
            ("max_conjugator_length", max_conjugator_length),
            ("max_log_letters", max_log_letters),
            ("max_reduced_length", max_reduced_length),
        ):
            if expected_caps.get(name) != value:
                raise ValueError(f"stage/receipt {name} cap mismatch")
    rule_count = stage.get("rule_count")
    if not isinstance(rule_count, int) or isinstance(rule_count, bool) or not 0 <= rule_count <= max_rules:
        raise ValueError("stage rule-count cap drift")
    rows = stage.get("rows")
    if not isinstance(rows, list):
        raise ValueError("stage rows missing")
    completed = stage.get("completed_unique_count")
    if completed != len(rows) or completed > len(unique):
        raise ValueError("stage completed count drift")
    seen: set[int] = set()
    all_identity = completed == len(unique)
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError("stage row is not an object")
        index = row.get("unique_index")
        if not isinstance(index, int) or not 1 <= index <= len(unique) or index in seen:
            raise ValueError("stage unique index drift")
        seen.add(index)
        original = validate_signed_word(row.get("original"), 6, f"stage row {index}.original")
        reduced = validate_signed_word(row.get("reduced"), 6, f"stage row {index}.reduced")
        if original != unique[index - 1]:
            raise ValueError(f"stage row {index}: original norm mismatch")
        log = row.get("log")
        if not isinstance(log, list) or len(log) > max_log_length:
            raise ValueError(f"stage row {index}: log-length cap drift")
        total_log_letters = 0
        for entry_no, entry in enumerate(log):
            if not isinstance(entry, list) or len(entry) != 2:
                raise ValueError(f"stage row {index}: log entry {entry_no} shape drift")
            conjugator = validate_signed_word(
                entry[1], 6, f"stage row {index}.log[{entry_no}].conjugator"
            )
            if len(conjugator) > max_conjugator_length:
                raise ValueError(f"stage row {index}: conjugator-length cap drift")
            total_log_letters += len(conjugator)
        if total_log_letters > max_log_letters:
            raise ValueError(f"stage row {index}: total log-letter cap drift")
        checked = proof_word(relators, reduced, log)
        if checked != original:
            raise ValueError(f"stage row {index}: F6 proof equation fails")
        if row.get("log_length") != len(log):
            raise ValueError(f"stage row {index}: log length field drift")
        if row.get("total_log_letters") != total_log_letters:
            raise ValueError(f"stage row {index}: total log-letter field drift")
        if len(reduced) > max_reduced_length:
            raise ValueError(f"stage row {index}: reduced-length cap drift")
        identity = len(reduced) == 0
        if row.get("identity") is not identity:
            raise ValueError(f"stage row {index}: identity field drift")
        all_identity = all_identity and identity
    if completed != len(unique):
        all_identity = False
    if stage.get("status") == "COMPLETE" and completed != len(unique):
        raise ValueError("COMPLETE stage is partial")
    return completed, all_identity


def resolve_artifact(receipt_path: Path, name: str) -> Path:
    path = Path(name)
    if path.exists():
        return path
    sibling = receipt_path.parent / path
    if sibling.exists():
        return sibling
    # GHA artifact download often flattens absolute producer paths.  Keep
    # the receipt's basename as a deterministic fallback, never a recursive
    # search through unrelated worktree files.
    flattened = receipt_path.parent / Path(name).name
    if flattened.exists():
        return flattened
    return sibling


def verify_receipt(receipt_path: Path, input_path: Path, words_path: Path) -> tuple[str, dict[str, Any]]:
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    if receipt.get("schema") != "d972-b4-u-idrel-direct-logged/v1":
        raise ValueError("receipt schema drift")
    relators, unique, duplicate_map, source = load_frozen(input_path, words_path)
    if hashlib.sha256(input_path.read_bytes()).hexdigest() != receipt.get("source_sha256"):
        raise ValueError("receipt/input source SHA mismatch")
    word_file_sha = hashlib.sha256(words_path.read_bytes()).hexdigest()
    if word_file_sha != receipt.get("word_artifact_sha256"):
        raise ValueError("receipt/word artifact SHA mismatch")
    if receipt.get("relator_sha256") != RELATOR_SHA or receipt.get("roof_word_sha256") != ROOF_SHA:
        raise ValueError("receipt source digest drift")
    if receipt.get("target_key_sha256") != TARGET_SHA or receipt.get("norm_sha256") != NORM_SHA:
        raise ValueError("receipt norm digest drift")
    verify_duplicate_map(receipt, unique, duplicate_map)
    caps = receipt.get("caps")
    if not isinstance(caps, dict):
        raise ValueError("receipt caps missing")
    if not isinstance(caps.get("max_passes"), int) or isinstance(caps.get("max_passes"), bool) or caps["max_passes"] < 0:
        raise ValueError("receipt max_passes cap drift")
    for name in (
        "max_rules",
        "max_log_length",
        "max_conjugator_length",
        "max_log_letters",
        "max_reduced_length",
        "max_wall_ms",
    ):
        _positive_cap(caps.get(name), name)
    _validate_filter_audit(receipt.get("filter_audit"), "receipt")
    artifacts = receipt.get("stage_artifacts")
    if not isinstance(artifacts, list) or not artifacts:
        raise ValueError("stage artifact list missing")
    terminal_stage = False
    stage_summaries: list[dict[str, Any]] = []
    for meta in artifacts:
        if not isinstance(meta, dict) or not isinstance(meta.get("artifact"), str):
            raise ValueError("stage metadata drift")
        path = resolve_artifact(receipt_path, meta["artifact"])
        if not path.exists():
            raise ValueError(f"stage artifact missing: {path}")
        stage = json.loads(path.read_text(encoding="utf-8"))
        if stage.get("stage") != meta.get("stage") or stage.get("status") != meta.get("status"):
            raise ValueError("stage metadata/contents disagree")
        completed, all_identity = verify_stage(stage, relators, unique, caps)
        stage_summaries.append({"stage": stage["stage"], "completed": completed,
                                "status": stage["status"], "all_identity": all_identity})
        terminal_stage = terminal_stage or (stage.get("status") == "COMPLETE" and all_identity)
    status = receipt.get("status")
    if status == "B4_B_DIRECT_LOGGED_TERMINAL":
        if not terminal_stage:
            raise ValueError("terminal status without a complete all-identity stage")
        result = "B4_B_DIRECT_LOGGED_TERMINAL"
    else:
        # A reduced nonidentity is deliberately only a bounded UNKNOWN.
        if status == "B4_A" or (isinstance(status, str) and status.startswith("B4_A")):
            raise ValueError("IdRel lane cannot label a bounded nonidentity as A")
        result = "UNKNOWN_VALID_RECEIPT"
    return result, {"receipt": str(receipt_path), "status": status, "stages": stage_summaries}


def verify_toy() -> None:
    """Small noncanonical certificate test, including a conjugated relator."""
    relators = [[1, 1]]
    original = [-2, 1, 1, 2]  # relator [1,1] conjugated by generator 2
    reduced: Word = []
    log = [[1, [2]]]
    if proof_word(relators, reduced, log) != original:
        raise AssertionError("toy valid log rejected")
    bad = [[1, [1]]]
    if proof_word(relators, reduced, bad) == original:
        raise AssertionError("toy conjugator mutation accepted")
    print(json.dumps({"status": "TOY_F6_SELFTEST_PASS", "checks": 2}, sort_keys=True))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt", type=Path)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--words", type=Path, default=DEFAULT_WORDS)
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args()
    try:
        if args.selftest:
            verify_toy()
            return 0
        if args.receipt is None:
            parser.error("--receipt is required unless --selftest is used")
        result, detail = verify_receipt(args.receipt.resolve(), args.input.resolve(), args.words.resolve())
        print(json.dumps({"status": result, **detail}, sort_keys=True))
        return 0 if result == "B4_B_DIRECT_LOGGED_TERMINAL" else 2
    except (OSError, ValueError, json.JSONDecodeError, AssertionError) as exc:
        print(json.dumps({"status": "CHECKER_REJECT", "error": str(exc)}, sort_keys=True))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
