#!/usr/bin/env python3
"""Independently replay a KBMAG normal-form certificate bundle.

KBMAG normal forms are only candidates: an unlogged rewrite system does not
say which original relator was used to obtain a rule.  This checker therefore
accepts a *proof bundle*, not ``roof_bits`` alone.  Every derived rule has a
primitive proof from the original 158 relators, and every one of the 972
canonical norm words has an application trace ending at the advertised
normal form.  All words are signed words in the original six-generator F6
basis.  The checker intentionally has no GAP/KBMAG or producer import.

Bundle schema (``d972-b4-kbmag-vankampen-bundle/v1``)::

    {
      "relator_sha256": ..., "roof_norm_words_sha256": ...,
      "normal_form_source": {
        "kbmag_status": "ALL_972_EMPTY_CANDIDATE_NEEDS_REPLAY",
        "normal_form_basis": "F6",
        "normal_forms": [[...], ...],
        "normal_forms_sha256": ...,
        "artifact_sha256": ...
      },
      "rules": [{"id": 1, "lhs": [...], "rhs": [...],
        "proof_steps": [{"op": "cancel"|"delete_relator"|"insert_relator",
          ... , "after": [...]}]}],
      "rows": [{"index": 1, "rule_steps": [...],
                "normal_form": [...], "final": [...]}]
    }

The primitive operations are free cancellation and insertion/deletion of a
contiguous cyclic conjugate of one of the original relators (or its inverse).
The result is ``LOCAL_972_NORMS_REPLAY_CERTIFIED`` only when all 972 traces
independently end at the empty word and the supplied normal-form source also
says all 972 were empty.  This is a statement about the fixed F6/158-relator
presentation only.  It is deliberately not a global B4-B, PB4 survival,
cofinality, or Ihara statement; the global field remains
``GLOBAL_SURVIVAL_UNKNOWN`` until a separate typed refinement bridge is proved.
Missing/partial/opaque data is always ``UNKNOWN``.

Soundness invariant: if ``u ~= v`` means equality in the quotient by the
normal closure of the 158 relators, free reduction preserves the represented
element, ``cancel`` removes an inverse pair, and every relator variant is a
normal-closure identity (cyclic conjugate or inverse).  Thus insertion/deletion
preserves ``~=``; induction over a rule proof and then over a row trace proves
only the corresponding fixed-presentation equality.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RELATORS = ROOT / "ci" / "out" / "d972_b4_u_relators_v1.json"
DEFAULT_WORDS = ROOT / "search" / "certs" / "d972_b4_word_key_artifact_v1_20260816.json"

SCHEMA = "d972-b4-kbmag-vankampen-bundle/v1"
RELATOR_SCHEMA = "d972-b4-u-relators/v1"
WORD_SCHEMA = "d972-b4-word-key-artifact/v1"
TARGET_DIGEST = "9c77e6768feb7ffe7143abf18f753af70e81b8e9cc792910c30ae0075d3b1d62"
TUPLE_DIGEST = "32e78ca5b97cd8a6fa59a150dac77719c1b8cb527f0467570c4d284600465a91"
ROWS_DIGEST = "283bf9cc728ced084a3b276e4496fbbc69026589813a2f31caa0dcb7a3682930"
RELATOR_DIGEST = "12fc1146dce5179c2b5fc44a3ceed6356a6b2c4835a564b55e9a9cd679fccd2e"
NORM_DIGEST = "ecf0cc8425bc24bdf6a8a352c223398221c4b179e09ee9a0bfe3dc888861683e"
WORD_ARTIFACT_DIGEST = "564a921be8114bdeb963f679c121e8d9aa90e148c65e95e393874fcba843e9f9"
EMPTY_KBMAG_STATUS = "ALL_972_EMPTY_CANDIDATE_NEEDS_REPLAY"
HEX64 = re.compile(r"^[0-9a-f]{64}$")

RHO = (
    (-6, -5, -3),
    (3,),
    (5,),
    (-3, -2, -1),
    (-5, -4, -1),
    (1,),
)


def cjson(value: Any) -> bytes:
    return json.dumps(value, separators=(",", ":"), ensure_ascii=True).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(cjson(value)).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def is_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def word(value: Any, name: str, *, max_abs: int = 6) -> list[int]:
    require(isinstance(value, list), f"{name} must be a list")
    out: list[int] = []
    for letter in value:
        require(is_int(letter) and letter != 0 and abs(letter) <= max_abs,
                f"{name} has an invalid signed letter")
        out.append(letter)
    return out


def free_reduce(value: list[int]) -> list[int]:
    out: list[int] = []
    for letter in value:
        if out and out[-1] == -letter:
            out.pop()
        else:
            out.append(letter)
    return out


def inverse(value: list[int]) -> list[int]:
    return [-letter for letter in reversed(value)]


def relator_variant(relators: list[list[int]], relator_id: Any,
                    rotation: Any, inverted: Any) -> list[int]:
    require(is_int(relator_id) and 1 <= relator_id <= len(relators),
            "relator id out of range")
    require(is_int(rotation), "rotation must be an integer")
    base = relators[relator_id - 1]
    require(base and 0 <= rotation < len(base), "rotation out of range")
    rotated = base[rotation:] + base[:rotation]
    require(isinstance(inverted, bool), "inverse must be boolean")
    return inverse(rotated) if inverted else rotated


def exact_norm(f2_word: list[int]) -> list[int]:
    """Rebuild the fixed six-generator norm without importing a producer."""
    current = free_reduce([(1 if letter > 0 else -1) if abs(letter) == 1 else
                           (4 if letter > 0 else -4) for letter in f2_word])
    orbit: list[list[int]] = []
    for _ in range(5):
        orbit.append(current)
        expanded: list[int] = []
        for letter in current:
            image = list(RHO[abs(letter) - 1])
            expanded.extend(image if letter > 0 else inverse(image))
        current = free_reduce(expanded)
    out: list[int] = []
    for item in reversed(orbit):
        out = free_reduce(out + item)
    return out


def load_relators(path: Path) -> list[list[int]]:
    obj = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(obj, dict) and obj.get("schema") == RELATOR_SCHEMA,
            "relator schema drift")
    require(obj.get("count") == 158 and isinstance(obj.get("relators"), list),
            "relator count drift")
    relators = [word(item, "relator") for item in obj["relators"]]
    require(digest(relators) == RELATOR_DIGEST, "relator digest drift")
    require(obj.get("canonical_bytes_sha256") == RELATOR_DIGEST,
            "relator canonical digest drift")
    return relators


def load_words(path: Path) -> tuple[list[list[Any]], list[list[int]], str]:
    raw = path.read_bytes()
    obj = json.loads(raw.decode("utf-8"))
    require(isinstance(obj, dict) and obj.get("schema") == WORD_SCHEMA,
            "word artifact schema drift")
    require(obj.get("count") == 972 and obj.get("source_target_key_digest") == TARGET_DIGEST,
            "word artifact target/count drift")
    require(obj.get("frozen_tuple_sha256") == TUPLE_DIGEST,
            "word artifact tuple digest drift")
    rows = obj.get("rows")
    require(isinstance(rows, list) and len(rows) == 972, "word rows incomplete")
    normalized: list[list[Any]] = []
    for row_index, row_value in enumerate(rows):
        require(isinstance(row_value, list) and len(row_value) == 3,
                f"word row {row_index} shape drift")
        marker, key, raw_word = row_value
        require(is_int(marker), f"word row {row_index} marker drift")
        require(isinstance(key, list), f"word row {row_index} key drift")
        # The canonical artifact uses [] for the two empty F2 words.  The
        # historical empty-string spelling is normalized before the pinned
        # rows digest for defensive parsing, but the raw source SHA below
        # still rejects an old artifact; never pass a string to exact_norm.
        if raw_word == "":
            raw_word = []
        f2 = word(raw_word, f"word row {row_index}", max_abs=2)
        normalized.append([marker, key, f2])
    require(digest(normalized) == ROWS_DIGEST, "normalized rows digest drift")
    norms = [exact_norm(row[2]) for row in normalized]
    require(digest(norms) == NORM_DIGEST, "roof norm digest drift")
    raw_digest = hashlib.sha256(raw).hexdigest()
    # This is a source pin, not a substitute for the normalized rows digest.
    require(raw_digest == WORD_ARTIFACT_DIGEST, "word artifact source digest drift")
    return normalized, norms, raw_digest


def check_digest_field(value: Any, name: str) -> None:
    require(isinstance(value, str) and HEX64.fullmatch(value) is not None,
            f"{name} must be a lowercase SHA-256")


def replay_primitive(current: list[int], step: Any,
                     relators: list[list[int]], context: str) -> list[int]:
    require(isinstance(step, dict), f"{context}: primitive step is not an object")
    op = step.get("op")
    require(op in {"cancel", "delete_relator", "insert_relator"},
            f"{context}: unsupported primitive operation")
    position = step.get("position")
    require(is_int(position) and position >= 0, f"{context}: invalid position")
    candidate: list[int]
    if op == "cancel":
        require(position + 1 < len(current), f"{context}: cancel outside word")
        require(current[position + 1] == -current[position],
                f"{context}: cancel is not an inverse pair")
        candidate = current[:position] + current[position + 2:]
    else:
        token = relator_variant(relators, step.get("relator"),
                                step.get("rotation"), step.get("inverse"))
        if op == "delete_relator":
            require(current[position:position + len(token)] == token,
                    f"{context}: relator deletion does not match")
            candidate = current[:position] + current[position + len(token):]
        else:
            require(position <= len(current), f"{context}: insertion outside word")
            candidate = current[:position] + token + current[position:]
    result = free_reduce(candidate)
    require(result == word(step.get("after"), f"{context}.after"),
            f"{context}: forged after word")
    return result


def verify_rule(rule_value: Any, relators: list[list[int]]) -> tuple[int, list[int], list[int]]:
    require(isinstance(rule_value, dict), "rule is not an object")
    rule_id = rule_value.get("id")
    require(is_int(rule_id) and rule_id > 0, "rule id is invalid")
    lhs = word(rule_value.get("lhs"), f"rule {rule_id}.lhs")
    rhs = word(rule_value.get("rhs"), f"rule {rule_id}.rhs")
    require(lhs, f"rule {rule_id} has an empty lhs")
    steps = rule_value.get("proof_steps")
    require(isinstance(steps, list), f"rule {rule_id} proof_steps missing")
    current = list(lhs)
    for step_index, step in enumerate(steps):
        current = replay_primitive(current, step, relators,
                                   f"rule {rule_id} step {step_index}")
    # Equal words need no primitive proof; a nontrivial rule must have at
    # least one primitive step so an opaque KBMAG equation cannot slip in.
    require(current == rhs, f"rule {rule_id}: proof does not reach rhs")
    require(steps or lhs == rhs, f"rule {rule_id}: empty proof for nonidentity rule")
    return rule_id, lhs, rhs


def verify_source(source: Any) -> tuple[list[list[int]], str]:
    require(isinstance(source, dict), "normal_form_source missing")
    require(source.get("normal_form_basis") == "F6", "normal-form basis is not F6")
    status = source.get("kbmag_status")
    require(isinstance(status, str) and status, "KBMAG status missing")
    artifact_sha = source.get("artifact_sha256")
    check_digest_field(artifact_sha, "normal_form_source.artifact_sha256")
    forms = source.get("normal_forms")
    require(isinstance(forms, list) and len(forms) == 972,
            "normal-form list must contain all 972 rows")
    forms = [word(item, "normal form") for item in forms]
    require(source.get("normal_forms_sha256") == digest(forms),
            "normal-form digest mismatch")
    all_empty = all(not item for item in forms)
    require(source.get("all_empty") is all_empty, "normal-form all_empty mismatch")
    return forms, status


def verify_bundle(bundle: Any, relators: list[list[int]], norms: list[list[int]],
                  word_artifact_sha: str) -> dict[str, Any]:
    require(isinstance(bundle, dict) and bundle.get("schema") == SCHEMA,
            "bundle schema drift")
    require(bundle.get("relator_sha256") == RELATOR_DIGEST,
            "bundle relator digest drift")
    require(bundle.get("roof_norm_words_sha256") == NORM_DIGEST,
            "bundle norm digest drift")
    require(bundle.get("normalized_rows_sha256") == ROWS_DIGEST,
            "bundle rows digest drift")
    source = bundle.get("normal_form_source")
    normal_forms, kbmag_status = verify_source(source)
    rules_value = bundle.get("rules")
    require(isinstance(rules_value, list) and rules_value, "rule ledger missing")
    rules: dict[int, tuple[list[int], list[int]]] = {}
    for rule_value in rules_value:
        rule_id, lhs, rhs = verify_rule(rule_value, relators)
        require(rule_id not in rules, f"duplicate rule id {rule_id}")
        rules[rule_id] = (lhs, rhs)

    rows = bundle.get("rows")
    require(isinstance(rows, list) and len(rows) == 972, "row trace incomplete")
    seen: set[int] = set()
    used: set[int] = set()
    for expected_index, row_value in enumerate(rows, start=1):
        require(isinstance(row_value, dict), f"row {expected_index} is not an object")
        index = row_value.get("index")
        require(index == expected_index and index not in seen,
                f"row index ledger is not complete at {expected_index}")
        seen.add(index)
        current = list(norms[index - 1])
        advertised_nf = word(row_value.get("normal_form"),
                             f"row {index}.normal_form")
        require(advertised_nf == normal_forms[index - 1],
                f"row {index}: normal form disagrees with source")
        steps = row_value.get("rule_steps")
        require(isinstance(steps, list), f"row {index}: rule_steps missing")
        for step_index, step in enumerate(steps):
            require(isinstance(step, dict), f"row {index} step {step_index} is not an object")
            rule_id = step.get("rule")
            require(is_int(rule_id) and rule_id in rules,
                    f"row {index} step {step_index}: unknown rule")
            lhs, rhs = rules[rule_id]
            position = step.get("position")
            require(is_int(position) and 0 <= position <= len(current) - len(lhs),
                    f"row {index} step {step_index}: bad rule position")
            if "before" in step:
                require(word(step["before"], f"row {index} step {step_index}.before") == current,
                        f"row {index} step {step_index}: before mismatch")
            require(current[position:position + len(lhs)] == lhs,
                    f"row {index} step {step_index}: lhs does not match")
            current = free_reduce(current[:position] + rhs + current[position + len(lhs):])
            require(current == word(step.get("after"),
                                    f"row {index} step {step_index}.after"),
                    f"row {index} step {step_index}: forged after word")
            used.add(rule_id)
        require(current == advertised_nf, f"row {index}: trace does not reach normal form")
        if "final" in row_value:
            require(word(row_value["final"], f"row {index}.final") == current,
                    f"row {index}: final mismatch")
    require(seen == set(range(1, 973)), "row index set is incomplete")

    empty_forms = all(not item for item in normal_forms)
    if empty_forms and kbmag_status == EMPTY_KBMAG_STATUS:
        status = "LOCAL_972_NORMS_REPLAY_CERTIFIED"
        global_status = "GLOBAL_SURVIVAL_UNKNOWN"
    elif empty_forms:
        status = "UNKNOWN_KBMAG_STATUS_NOT_TERMINAL"
        global_status = "GLOBAL_SURVIVAL_UNKNOWN"
    else:
        status = "UNKNOWN_NONEMPTY_NORMAL_FORMS"
        global_status = "GLOBAL_SURVIVAL_UNKNOWN"
    return {
        "schema": "d972-b4-kbmag-vankampen-receipt/v1",
        "status": status,
        "global_b_status": global_status,
        "proof_level": "INDEPENDENT_FIXED_U_158_RELATOR_DAG_REPLAY_LOCAL",
        "bundle_schema": SCHEMA,
        "relator_sha256": RELATOR_DIGEST,
        "normalized_rows_sha256": ROWS_DIGEST,
        "roof_norm_words_sha256": NORM_DIGEST,
        "word_artifact_sha256": word_artifact_sha,
        "normal_form_source_artifact_sha256": source["artifact_sha256"],
        "kbmag_status": kbmag_status,
        "rule_count": len(rules),
        "used_rule_count": len(used),
        "row_count": len(rows),
        "normal_form_count": len(normal_forms),
        "normal_forms_empty": empty_forms,
        "terminal_claim": ("LOCAL ONLY: all 972 fixed-U original F6 norms have "
                           "independently replayed original-relator proof traces; "
                           "PB4/global survival bridge is not claimed"
                           if status == "LOCAL_972_NORMS_REPLAY_CERTIFIED"
                           else "NONE; missing/opaque/partial proof remains UNKNOWN"),
    }


def fixture() -> tuple[dict[str, Any], list[list[int]], list[list[int]]]:
    relators = [[1]]
    norms = [[1] for _ in range(972)]
    forms = [[] for _ in range(972)]
    rule = {
        "id": 1, "lhs": [1], "rhs": [],
        "proof_steps": [{"op": "delete_relator", "relator": 1,
                          "rotation": 0, "inverse": False,
                          "position": 0, "after": []}],
    }
    rows = [{"index": index, "normal_form": [], "rule_steps": [
        {"rule": 1, "position": 0, "after": []}], "final": []}
            for index in range(1, 973)]
    source = {"kbmag_status": EMPTY_KBMAG_STATUS, "normal_form_basis": "F6",
              "normal_forms": forms, "normal_forms_sha256": digest(forms),
              "artifact_sha256": "0" * 64, "all_empty": True}
    bundle = {"schema": SCHEMA, "relator_sha256": RELATOR_DIGEST,
              "roof_norm_words_sha256": NORM_DIGEST,
              "normalized_rows_sha256": ROWS_DIGEST,
              "normal_form_source": source, "rules": [rule], "rows": rows}
    return bundle, relators, norms


def selftest() -> None:
    bundle, relators, norms = fixture()
    receipt = verify_bundle(bundle, relators, norms, "0" * 64)
    require(receipt["status"] == "LOCAL_972_NORMS_REPLAY_CERTIFIED", "positive fixture failed")
    require(receipt["global_b_status"] == "GLOBAL_SURVIVAL_UNKNOWN",
            "local fixture overclaimed global survival")

    forged = json.loads(json.dumps(bundle))
    forged["rules"][0]["proof_steps"][0]["after"] = [1]
    try:
        verify_bundle(forged, relators, norms, "0" * 64)
    except ValueError:
        pass
    else:
        raise AssertionError("forged primitive after was accepted")

    forged = json.loads(json.dumps(bundle))
    forged["rows"][0]["rule_steps"][0]["after"] = [1]
    try:
        verify_bundle(forged, relators, norms, "0" * 64)
    except ValueError:
        pass
    else:
        raise AssertionError("forged application after was accepted")

    forged = json.loads(json.dumps(bundle))
    forged["rows"][0]["index"] = 2
    try:
        verify_bundle(forged, relators, norms, "0" * 64)
    except ValueError:
        pass
    else:
        raise AssertionError("partial/index-forged ledger was accepted")

    forged = json.loads(json.dumps(bundle))
    nonempty_forms = [[1] for _ in range(972)]
    forged["normal_form_source"]["normal_forms"] = nonempty_forms
    forged["normal_form_source"]["normal_forms_sha256"] = digest(nonempty_forms)
    forged["normal_form_source"]["all_empty"] = False
    for forged_row in forged["rows"]:
        forged_row["normal_form"] = [1]
        forged_row["rule_steps"] = []
        forged_row["final"] = [1]
    receipt = verify_bundle(forged, relators, norms, "0" * 64)
    require(receipt["status"] == "UNKNOWN_NONEMPTY_NORMAL_FORMS",
            "nonempty normal form was promoted")
    require(receipt["global_b_status"] == "GLOBAL_SURVIVAL_UNKNOWN",
            "nonempty fixture global status drift")
    print("SELFTEST_PASS schema=" + SCHEMA)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--bundle", type=Path)
    parser.add_argument("--relators", type=Path, default=DEFAULT_RELATORS)
    parser.add_argument("--word-artifact", type=Path, default=DEFAULT_WORDS)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    if args.selftest:
        selftest()
        return 0
    require(args.bundle is not None and args.output is not None,
            "--bundle and --output are required without --selftest")
    relators = load_relators(args.relators.resolve())
    _rows, norms, word_artifact_sha = load_words(args.word_artifact.resolve())
    bundle_bytes = args.bundle.resolve().read_bytes()
    bundle = json.loads(bundle_bytes.decode("utf-8"))
    receipt = verify_bundle(bundle, relators, norms, word_artifact_sha)
    receipt["bundle_sha256"] = hashlib.sha256(bundle_bytes).hexdigest()
    args.output.resolve().parent.mkdir(parents=True, exist_ok=True)
    args.output.resolve().write_text(json.dumps(receipt, sort_keys=True, indent=2) + "\n",
                                     encoding="utf-8")
    print(json.dumps({key: receipt[key] for key in
                      ("status", "global_b_status", "rule_count", "row_count")},
                     sort_keys=True))
    return 0 if receipt["status"] == "LOCAL_972_NORMS_REPLAY_CERTIFIED" else 2


if __name__ == "__main__":
    raise SystemExit(main())
