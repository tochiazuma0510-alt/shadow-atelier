#!/usr/bin/env python3
"""Non-sharing checker for arbitrary finite permutation images of U_M.

Input is JSON produced by a finite-image worker.  It contains six generator
images of U_M in ``h_images``, six signed free-rho words in ``rho_words``, all
158 U_M relators, and either ``roof_words`` (the exact 972 rows) or one
``witness_word``.  Roof words are F2 words and are evaluated at U generators
1 and 4: j(x)=X12 and j(y)=X23.  No producer module is imported.

Every receipt also identifies its position in the exhaustive
``GQuotients(...:findall:=true)`` batch with ``epi_index`` and ``epi_count``;
an all-pass result from one epi is never promoted to a terminal verdict.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import tempfile
from typing import Iterable, Sequence

Perm = tuple[int, ...]
FROZEN_TARGET_DIGEST = "9c77e6768feb7ffe7143abf18f753af70e81b8e9cc792910c30ae0075d3b1d62"
FROZEN_TUPLE_DIGEST = "32e78ca5b97cd8a6fa59a150dac77719c1b8cb527f0467570c4d284600465a91"
# Canonical JSON digest of Concatenation(K05 relators, five rho-orbit
# copies of the 28 marked Q0 relators), serialized as compact JSON arrays.
FROZEN_RELATOR_DIGEST = "12fc1146dce5179c2b5fc44a3ceed6356a6b2c4835a564b55e9a9cd679fccd2e"
# GAP's diagnostic HexSHA256(String(signed_relators)) was independently
# observed as 28fd032503ce7cdef186592ceeb959f40253644ebc12006ff98b300cdf7a67f.
# It is intentionally not the pin: GAP String inserts spaces and uses its
# pretty-printer delimiters, whereas this checker hashes compact JSON arrays.
# Canonical rows digest of the independently checked GHA word/key artifact.
FROZEN_WORD_KEY_ARTIFACT_DIGEST = (
    "283bf9cc728ced084a3b276e4496fbbc69026589813a2f31caa0dcb7a3682930"
)
# The archive is deliberately a separately versioned input, not a producer
# field.  A missing archive or digest mismatch keeps every terminal path
# closed.
WORD_KEY_ARTIFACT_PATH = (Path(__file__).resolve().parent / "certs" /
                          "d972_b4_word_key_artifact_v1_20260816.json")
TARGETS = {
    "S3": 6, "S4": 24, "D10": 10, "D14": 14, "D18": 18,
    "D22": 22, "D26": 26, "A5": 60,
}
BATCH_TARGETS = ("S3", "S4", "D10", "D14", "D18", "D22", "D26", "A5")


def compose(p: Perm, q: Perm) -> Perm:
    return tuple(q[p[i] - 1] for i in range(len(p)))


def inv(p: Perm) -> Perm:
    out = [0] * len(p)
    for i, x in enumerate(p, 1):
        out[x - 1] = i
    return tuple(out)


def perm(value: Sequence[int]) -> Perm:
    p = tuple(int(x) for x in value)
    if sorted(p) != list(range(1, len(p) + 1)):
        raise ValueError(f"not a permutation: {value!r}")
    return p


def eval_word(word: Iterable[int], images: Sequence[Perm]) -> Perm:
    out: Perm = tuple(range(1, len(images[0]) + 1))
    for raw in word:
        n = int(raw)
        if n == 0 or abs(n) > len(images):
            raise ValueError(f"word generator out of range: {n}")
        g = images[abs(n) - 1]
        out = compose(out, inv(g) if n < 0 else g)
    return out


def closure(gens: Sequence[Perm]) -> set[Perm]:
    one: Perm = tuple(range(1, len(gens[0]) + 1))
    seen = {one}
    todo = [one]
    while todo:
        a = todo.pop()
        for g in gens:
            for b in (compose(a, g), compose(g, a)):
                if b not in seen:
                    seen.add(b)
                    todo.append(b)
    return seen


def require(ok: bool, msg: str) -> None:
    if not ok:
        raise ValueError(msg)


def verify_pinned_fields(receipt: dict[str, object]) -> None:
    """Reject producer-controlled digest substitutions before any verdict."""
    require(receipt.get("target_key_digest") == FROZEN_TARGET_DIGEST,
            "receipt target-key digest is not pinned")
    require(receipt.get("all_relators_sha256") == FROZEN_RELATOR_DIGEST,
            "receipt relator digest is not pinned")
    require(FROZEN_WORD_KEY_ARTIFACT_DIGEST != "" and
            receipt.get("word_key_artifact_sha256") == FROZEN_WORD_KEY_ARTIFACT_DIGEST,
            "independent word-key artifact is not pinned")


def canonical_words(words: Sequence[Sequence[int]]) -> str:
    return json.dumps(words, separators=(",", ":"), ensure_ascii=False)


def target_key_digest(keys: Sequence[str]) -> str:
    return hashlib.sha256(("\n".join(sorted(keys)) + "\n").encode()).hexdigest()


def artifact_key_string(key: Sequence[object]) -> str:
    """Serialize nested artifact [m, [[a,e]x3], can4] to flat receipt key.

    The frozen tuple digest intentionally retains the nested orderkey shape,
    while receipt target keys use the historical flat six-coordinate can9
    string.  Keeping this conversion here prevents a shape-only binding bug.
    """
    require(isinstance(key, list) and len(key) == 3,
            "word-key artifact key shape")
    m, can9, can4 = key
    require(isinstance(m, int) and isinstance(can9, list) and len(can9) == 3,
            "word-key artifact D9 shape")
    require(isinstance(can4, list) and len(can4) == 9,
            "word-key artifact PSL shape")
    flat: list[str] = []
    for pair in can9:
        require(isinstance(pair, list) and len(pair) == 2 and
                all(isinstance(x, int) for x in pair),
                "word-key artifact D9 coordinate")
        flat.extend((str(pair[0]), str(pair[1])))
    require(all(isinstance(x, int) for x in can4),
            "word-key artifact PSL coordinate")
    return "(" + str(m) + ";" + ",".join(flat) + ";" + ",".join(map(str, can4)) + ")"


def load_word_key_artifact() -> set[tuple[str, tuple[int, ...]]]:
    """Load and authenticate the archived independent word/key table."""
    require(FROZEN_WORD_KEY_ARTIFACT_DIGEST != "",
            "independent word-key artifact is not pinned")
    require(WORD_KEY_ARTIFACT_PATH.is_file(),
            "archived independent word-key artifact is missing")
    obj = json.loads(WORD_KEY_ARTIFACT_PATH.read_text(encoding="utf-8"))
    require(obj.get("schema") == "d972-b4-word-key-artifact/v1",
            "word-key artifact schema drift")
    rows = obj.get("rows")
    require(isinstance(rows, list) and len(rows) == 972,
            "word-key artifact row count")
    require(obj.get("count") == 972,
            "word-key artifact count metadata")
    require(obj.get("source_target_key_digest") == FROZEN_TARGET_DIGEST,
            "word-key artifact source target digest")
    require(obj.get("frozen_tuple_sha256") == FROZEN_TUPLE_DIGEST,
            "word-key artifact frozen tuple digest")
    canonical = json.dumps(rows, separators=(",", ":"), ensure_ascii=True)
    got = hashlib.sha256(canonical.encode()).hexdigest()
    require(got == obj.get("canonical_bytes_sha256"),
            "word-key artifact declared digest mismatch")
    require(got == FROZEN_WORD_KEY_ARTIFACT_DIGEST,
            "word-key artifact archive digest mismatch")
    pairs: set[tuple[str, tuple[int, ...]]] = set()
    for row in rows:
        require(isinstance(row, list) and len(row) == 3,
                "word-key artifact row shape")
        m, key, word = row
        require(isinstance(m, int) and isinstance(key, list) and
                isinstance(word, list), "word-key artifact row types")
        require(len(key) == 3 and key[0] == m and
                all(isinstance(x, int) and x != 0 for x in word),
                "word-key artifact row binding shape")
        pair = (artifact_key_string(key), tuple(int(x) for x in word))
        require(pair not in pairs, "duplicate word/key artifact pair")
        pairs.add(pair)
    return pairs


def verify_word_key_binding(words: Sequence[Sequence[int]],
                            keys: Sequence[str],
                            artifact_pairs: set[tuple[str, tuple[int, ...]]]) -> None:
    """Require exact receipt (target-key, signed-word) correspondence."""
    require(len(words) == 972 and len(keys) == 972,
            "word/key receipt binding count")
    receipt_pairs = {(str(k), tuple(int(x) for x in w))
                     for k, w in zip(keys, words)}
    require(len(receipt_pairs) == 972,
            "receipt contains duplicate target-key/word pairs")
    require(receipt_pairs == artifact_pairs,
            "receipt roof words are not the archived exact target correspondence")


def selftest() -> None:
    global WORD_KEY_ARTIFACT_PATH, FROZEN_WORD_KEY_ARTIFACT_DIGEST
    s = (2, 1, 3)
    one = (1, 2, 3)
    require(eval_word([-1], [s]) == s, "negative-letter selftest")
    require(eval_word([1, -1], [s]) == one, "inverse selftest")
    rho = [[2], [3], [4], [5], [1], [6]]
    hs = [s, one, one, one, one, s]
    rows = [hs]
    for _ in range(4):
        rows.append([eval_word(w, rows[-1]) for w in rho])
    require([eval_word(w, rows[-1]) for w in rho] == hs, "rho^5 selftest")
    key0 = "(0;0,0,0,0,0,0;1,2,3,4,5,6,7,8,9)"
    require(artifact_key_string([0, [[0, 0], [0, 0], [0, 0]],
                                 list(range(1, 10))]) == key0,
            "word-key GAP key serialization selftest")
    pair0 = {(key0, (1, -2))}
    try:
        verify_word_key_binding([[1, -2]], [key0], pair0)
    except ValueError:
        pass
    else:
        raise ValueError("short word-key binding selftest was accepted")

    # The pinned archive is a separate load-bearing input.  Confirm the
    # actual archive is present and that a producer-declared digest cannot
    # authorize a tampered row.
    archive_pairs = load_word_key_artifact()
    require(len(archive_pairs) == 972, "word-key archive selftest count")
    require(sum(1 for _, word in archive_pairs if len(word) == 0) == 2,
            "word-key archive identity-row selftest")
    archive_obj = json.loads(WORD_KEY_ARTIFACT_PATH.read_text(encoding="utf-8"))
    tampered_rows = json.loads(json.dumps(archive_obj["rows"], separators=(",", ":")))
    tampered_rows[0][2] = [1]
    tampered_obj = dict(archive_obj)
    tampered_obj["rows"] = tampered_rows
    tampered_obj["canonical_bytes_sha256"] = hashlib.sha256(
        json.dumps(tampered_rows, separators=(",", ":"), ensure_ascii=True).encode()
    ).hexdigest()
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False,
                                     encoding="utf-8") as handle:
        tampered_path = Path(handle.name)
        json.dump(tampered_obj, handle, separators=(",", ":"))
    original_archive_path = WORD_KEY_ARTIFACT_PATH
    WORD_KEY_ARTIFACT_PATH = tampered_path
    try:
        try:
            load_word_key_artifact()
        except ValueError:
            pass
        else:
            raise ValueError("tampered word-key archive was accepted")
    finally:
        WORD_KEY_ARTIFACT_PATH = original_archive_path
        try:
            tampered_path.unlink()
        except OSError:
            pass

    old_pin = FROZEN_WORD_KEY_ARTIFACT_DIGEST
    FROZEN_WORD_KEY_ARTIFACT_DIGEST = "test-word-key-artifact"
    base = {"target_key_digest": FROZEN_TARGET_DIGEST,
            "all_relators_sha256": FROZEN_RELATOR_DIGEST,
            "word_key_artifact_sha256": FROZEN_WORD_KEY_ARTIFACT_DIGEST}
    verify_pinned_fields(base)
    for field in tuple(base):
        bad = dict(base)
        bad[field] = "tampered"
        try:
            verify_pinned_fields(bad)
        except ValueError:
            pass
        else:
            raise ValueError(f"tamper selftest accepted {field}")
    FROZEN_WORD_KEY_ARTIFACT_DIGEST = old_pin


def main() -> int:
    selftest()
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    digest = hashlib.sha256(args.input.read_bytes()).hexdigest()
    try:
        r = json.loads(args.input.read_text(encoding="utf-8"))
        require(r.get("schema") == "d972-b4-finite-image/v2", "schema drift")
        verify_pinned_fields(r)
        name = str(r.get("target", ""))
        epi_count = int(r["epi_count"])
        epi_index = int(r["epi_index"])
        require(epi_count > 0 and 1 <= epi_index <= epi_count, "epi batch position gate")
        h = [perm(x) for x in r["h_images"]]
        require(len(h) == 6, "six U_M images required")
        degree = len(h[0])
        require(all(len(x) == degree for x in h), "permutation degree drift")
        if name in TARGETS:
            require(r.get("target_order") == TARGETS[name], "target order mismatch")
        if r.get("target_order") is not None:
            require(len(closure(h)) == int(r["target_order"]), "epi generation gate")

        rho = [[int(x) for x in w] for w in r["rho_words"]]
        rels = [[int(x) for x in w] for w in r["all_relators"]]
        require(len(rho) == 6 and len(rels) == 158, "rho/158-relator count gate")
        rel_digest = hashlib.sha256(canonical_words(rels).encode()).hexdigest()
        require(rel_digest == FROZEN_RELATOR_DIGEST, "frozen relator digest mismatch")
        require(r.get("all_relators_sha256") == FROZEN_RELATOR_DIGEST,
                "receipt relator digest is not pinned")
        hpow: list[list[Perm]] = [h]
        for _ in range(4):
            hpow.append([eval_word(w, hpow[-1]) for w in rho])
        next_h = [eval_word(w, hpow[-1]) for w in rho]
        require(next_h == h, "rho^5 image gate")
        one: Perm = tuple(range(1, degree + 1))
        bad = [i for i, w in enumerate(rels) if any(eval_word(w, row) != one for row in hpow)]
        require(not bad, f"relator image failure: {bad[:8]}")

        keys = r.get("target_keys")
        require(isinstance(keys, list) and len(keys) == 972, "frozen key count")
        got = target_key_digest([str(x) for x in keys])
        require(got == FROZEN_TARGET_DIGEST, "frozen target-key digest mismatch")
        require(r.get("target_key_digest") == FROZEN_TARGET_DIGEST,
                "receipt target-key digest is not pinned")
        # A list of keys plus a producer-supplied list of words is not enough:
        # the load-bearing word/key correspondence needs a separately pinned,
        # independently generated artifact.  The archive and its digest are
        # checked before either witness or full-roof terminal path.
        require(FROZEN_WORD_KEY_ARTIFACT_DIGEST != "" and
                r.get("word_key_artifact_sha256") == FROZEN_WORD_KEY_ARTIFACT_DIGEST,
                "independent word-key artifact is not pinned")

        rows = r.get("roof_words")
        if rows is None and r.get("roof_rows") is not None:
            rows = [x["word"] if isinstance(x, dict) else x for x in r["roof_rows"]]
        if rows is not None:
            words = [[int(x) for x in w] for w in rows]
            require(len(words) == 972, "exact 972 roof words required")
            require(r.get("roof_words_sha256") is not None, "roof word digest required")
            require(hashlib.sha256(canonical_words(words).encode()).hexdigest() == r["roof_words_sha256"], "roof word digest")
            verify_word_key_binding(words, [str(x) for x in keys],
                                    load_word_key_artifact())
        else:
            words = None

        result: dict[str, object] = {
            "schema": "d972-b4-finite-image-independent-check/v2",
            "producer_receipt_sha256": digest,
            "target": name,
            "target_order": r.get("target_order"),
            "epi_index": epi_index,
            "epi_count": epi_count,
            "degree": degree,
            "relator_count": len(rels),
            "rho5": True,
            "relators": "all_pass",
        }
        if words is not None:
            bits: list[bool] = []
            first = None
            for i, word in enumerate(words, 1):
                # Critical convention: F2 y maps to U generator 4, not 2.
                factors = [eval_word(word, [row[0], row[3]]) for row in hpow]
                defect = one
                for factor in reversed(factors):
                    defect = compose(defect, factor)
                ok = defect == one
                bits.append(ok)
                if not ok and first is None:
                    first = {"index": i, "word": word, "defect": list(defect)}
            fails = len(bits) - sum(bits)
            result.update({"roof_count": 972, "pass_count": sum(bits), "fail_count": fails,
                           "first_fail": first,
                           "status": "B4_A_SIDE_CROSSCHECKED" if fails else "UNKNOWN_ALLPASS_CONTINUE"})
        else:
            require(1 <= int(r["witness_index"]) <= 972, "witness index")
            word = [int(x) for x in r["witness_word"]]
            witness_key = str(keys[int(r["witness_index"]) - 1])
            if r.get("witness_key") is not None:
                require(str(r["witness_key"]) == witness_key, "witness key mismatch")
            artifact_pairs = load_word_key_artifact()
            require((witness_key, tuple(word)) in artifact_pairs,
                    "witness word/key is not archived exact correspondence")
            factors = [eval_word(word, [row[0], row[3]]) for row in hpow]
            defect = one
            for factor in reversed(factors):
                defect = compose(defect, factor)
            require(defect != one, "witness defect is trivial")
            if r.get("expected_defect") is not None:
                require(list(defect) == [int(x) for x in r["expected_defect"]], "defect mismatch")
            result.update({"witness_word": word, "defect": list(defect),
                           "status": "B4_A_SIDE_CROSSCHECKED"})
    except (KeyError, TypeError, ValueError) as exc:
        result = {"schema": "d972-b4-finite-image-independent-check/v2",
                  "status": "REJECTED", "reason": str(exc)}
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps(result, sort_keys=True))
        return 1
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))
    return 0 if result["status"] == "B4_A_SIDE_CROSSCHECKED" else 2


if __name__ == "__main__":
    raise SystemExit(main())
