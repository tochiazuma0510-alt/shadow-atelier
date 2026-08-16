#!/usr/bin/env python3
"""Independent receipt and raw-RS checker for the B4 exact-K lane.

The GAP producer is allowed to be the only implementation of KBMAG's
rewriting system.  This checker independently rebuilds the canonical
161-generator/5056-relator Schreier words and all 972 norm words, checks the
producer's complete boolean ledgers, and recomputes K_ab by integer Smith
normal form.  It never turns an UNKNOWN producer state into A or B.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

from sympy import Matrix, ZZ
from sympy.matrices.normalforms import smith_normal_form


INPUT = Path("search/certs/d972_b4_p2_magnus_input_v2_20260816.json")
WORDS = Path("search/certs/d972_b4_word_key_artifact_v1_20260816.json")
SOURCE_SHA = "c61b2b77131127aca83a8d7c56b7fdadd2d519b040ea4d91093622c813c2b4a9"
V1_SHA = "a3972236122dac32e74c6c8527d8dec8c8adc61e7f4dabb107af7660bc039dac"
RELATOR_SHA = "12fc1146dce5179c2b5fc44a3ceed6356a6b2c4835a564b55e9a9cd679fccd2e"
NORM_SHA = "ecf0cc8425bc24bdf6a8a352c223398221c4b179e09ee9a0bfe3dc888861683e"
RHO_SHA = "23db316e11e6486e0475b8425ff8ea6666941b5bff0943bf872e39761d0398ed"
RS_CONSTRUCTOR_SHA = "ae605e53f0a6823b6362ffe9e063cb9b4ea824ff1a28992c17da8706feb62576"
WORDS_SHA = "564a921be8114bdeb963f679c121e8d9aa90e148c65e95e393874fcba843e9f9"
WORDS_CANONICAL_SHA = "283bf9cc728ced084a3b276e4496fbbc69026589813a2f31caa0dcb7a3682930"
RAW_RS_SHA = "29c65a6cf9d0308e25ca462c752d7b540a6856e7d99d5d1d016919240b575c0e"
NORM_RS_SHA = "f7134e15e92c80a5ceeede38e94314539815a665ba7d279443208de1696041f8"
RHO = [[-6, -5, -3], [3], [5], [-3, -2, -1], [-5, -4, -1], [1]]
GEN_BITS = [1, 2, 4, 8, 16, 31]
AB = [9] * 10
KERNEL_ORDER = 9**10
U_ORDER = 32 * KERNEL_ORDER
REPLAY_NAME = "d972_b4_u_metabelian_kbmag_replay_v1.json"


def compact(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def digest(value: object) -> str:
    return hashlib.sha256(compact(value).encode("utf-8")).hexdigest()


def file_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def free_reduce(word: list[int]) -> list[int]:
    out: list[int] = []
    for letter in word:
        if out and out[-1] == -letter:
            out.pop()
        else:
            out.append(letter)
    return out


def inverse(word: list[int]) -> list[int]:
    return [-x for x in reversed(word)]


def toggle(mask: int, bit: int) -> int:
    return 31 - mask if bit == 31 else mask ^ bit


def transversal(mask: int) -> list[int]:
    return [bit + 1 for bit in range(5) if mask & (1 << bit)]


def rs_rewrite(word: list[int], start: int, pair_id: list[list[int]]) -> list[int]:
    mask = start
    out: list[int] = []
    for letter in word:
        gen = abs(letter)
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
    if mask != start:
        raise ValueError("Schreier word does not close")
    return free_reduce(out)


def build_raw_rs(relators: list[list[int]]) -> tuple[list[list[int]], list[list[int]]]:
    pair_id = [[0] * 6 for _ in range(32)]
    pair_words: list[list[int]] = []
    reps = [transversal(mask) for mask in range(32)]
    for mask in range(32):
        for gen in range(1, 7):
            raw = reps[mask] + [gen] + inverse(reps[toggle(mask, GEN_BITS[gen - 1])])
            word = free_reduce(raw)
            if word:
                pair_words.append(word)
                pair_id[mask][gen - 1] = len(pair_words)
    if len(pair_words) != 161:
        raise ValueError(f"raw Schreier generator count drift: {len(pair_words)}")
    raw_relators: list[list[int]] = []
    for start in range(32):
        for relator in relators:
            word = rs_rewrite(relator, start, pair_id)
            if word:
                raw_relators.append(word)
    if len(raw_relators) != 5056:
        raise ValueError(f"raw Schreier relator count drift: {len(raw_relators)}")
    return pair_words, raw_relators


def rho_map(word: list[int]) -> list[int]:
    out: list[int] = []
    for letter in word:
        image = RHO[abs(letter) - 1]
        out.extend(image if letter > 0 else inverse(image))
    return free_reduce(out)


def exact_norm(f2word: list[int]) -> list[int]:
    base: list[int] = []
    for letter in f2word:
        if abs(letter) == 1:
            base.append(1 if letter > 0 else -1)
        elif abs(letter) == 2:
            base.append(4 if letter > 0 else -4)
        else:
            raise ValueError("F2 alphabet drift")
    base = free_reduce(base)
    orbit: list[list[int]] = []
    value = base
    for _ in range(5):
        orbit.append(value)
        value = rho_map(value)
    result: list[int] = []
    for value in reversed(orbit):
        result = free_reduce(result + value)
    return result


def normalize_word_rows(rows: object) -> tuple[list[list[object]], list[int]]:
    if not isinstance(rows, list) or len(rows) != 972:
        raise ValueError("word artifact row count drift")
    normalized: list[list[object]] = []
    legacy: list[int] = []
    for index, row in enumerate(rows):
        if not isinstance(row, list) or len(row) != 3:
            raise ValueError(f"word artifact row {index} shape drift")
        m, key, word = row
        if not isinstance(m, int) or isinstance(m, bool) or not isinstance(key, list):
            raise ValueError(f"word artifact row {index} key shape drift")
        if word == "":
            if index not in (0, 891):
                raise ValueError(f"unexpected legacy empty row {index}")
            legacy.append(index)
            word = []
        if not isinstance(word, list):
            raise ValueError(f"word artifact row {index} word type drift")
        if any(not isinstance(letter, int) or isinstance(letter, bool) or letter == 0
               for letter in word):
            raise ValueError(f"word artifact row {index} signed-letter drift")
        normalized.append([m, key, list(word)])
    return normalized, legacy


def load_canonical() -> tuple[list[list[int]], list[list[int]], list[list[int]]]:
    if file_digest(INPUT) != SOURCE_SHA:
        raise ValueError("canonical input SHA drift")
    source = json.loads(INPUT.read_text(encoding="utf-8"))
    if source.get("schema") != "d972-b4-p2-magnus-input/v2":
        raise ValueError("canonical input schema drift")
    relators = source.get("all_relators")
    if not isinstance(relators, list) or len(relators) != 158:
        raise ValueError("canonical relator count drift")
    if source.get("rho_words") != RHO or source.get("all_relators_sha256") != RELATOR_SHA:
        raise ValueError("canonical rho/relator digest drift")
    if digest(relators) != RELATOR_SHA:
        raise ValueError("canonical relator bytes drift")
    if file_digest(WORDS) != WORDS_SHA:
        raise ValueError("word artifact SHA drift")
    artifact = json.loads(WORDS.read_text(encoding="utf-8"))
    rows = artifact.get("rows")
    if artifact.get("schema") != "d972-b4-word-key-artifact/v1" or artifact.get("count") != 972:
        raise ValueError("word artifact schema/count drift")
    normalized, _legacy = normalize_word_rows(rows)
    if artifact.get("canonical_bytes_sha256") != WORDS_CANONICAL_SHA:
        raise ValueError("word artifact canonical digest pin drift")
    if artifact.get("canonical_bytes_sha256") != digest(normalized):
        raise ValueError("word artifact canonical digest drift")
    pair_words, raw_relators = build_raw_rs(relators)
    if digest(raw_relators) != RAW_RS_SHA:
        raise ValueError("raw RS relator digest drift")
    norm_original = [exact_norm(row[2]) for row in normalized]
    if digest(norm_original) != NORM_SHA:
        raise ValueError("norm original digest drift")
    pair_id = _pair_id(pair_words)
    norm_rows = [rs_rewrite(word, 0, pair_id) for word in norm_original]
    if digest(norm_rows) != NORM_RS_SHA:
        raise ValueError("norm RS digest drift")
    return pair_words, raw_relators, norm_rows


def _pair_id(pair_words: list[list[int]]) -> list[list[int]]:
    """Recover the canonical pair-id matrix from mask-major pair words."""
    pair_id = [[0] * 6 for _ in range(32)]
    index = 0
    reps = [transversal(mask) for mask in range(32)]
    for mask in range(32):
        for gen in range(1, 7):
            word = free_reduce(reps[mask] + [gen] + inverse(reps[toggle(mask, GEN_BITS[gen - 1])]))
            if word:
                index += 1
                if pair_words[index - 1] != word:
                    raise ValueError("Schreier pair-word drift")
                pair_id[mask][gen - 1] = index
    if index != len(pair_words):
        raise ValueError("Schreier pair-word length drift")
    return pair_id


def resolve_replay_path(receipt_path: Path, explicit: Path | None) -> Path:
    """Require the same-job replay beside the v3 receipt, or an explicit path."""
    replay_path = explicit if explicit is not None else receipt_path.with_name(REPLAY_NAME)
    if not replay_path.is_file():
        raise ValueError(
            f"same-job replay receipt missing: {replay_path}; pass --replay explicitly"
        )
    return replay_path


def _expected_replay_status(comm: list[bool], norms: list[bool]) -> str:
    if sum(comm) != 12880:
        return "UNKNOWN_K_NONABELIAN_REPLAYED"
    if sum(norms) < 972:
        return "B4_A_CANDIDATE_METABELIAN_REPLAYED"
    return "B4_B_TERMINAL_CANDIDATE_METABELIAN_REPLAYED"


def validate_replay_binding(
    receipt: dict,
    replay_raw: bytes,
    replay: object,
    comm: list[bool],
    norms: list[bool],
) -> None:
    """Check the outer -> replay -> inner receipt chain and replay ledgers."""
    if receipt.get("post_replay_requested") is not True:
        raise ValueError("same-job replay was not requested")
    if not isinstance(replay, dict):
        raise ValueError("same-job replay receipt is not an object")
    replay_sha = hashlib.sha256(replay_raw).hexdigest()
    if receipt.get("replay_receipt_sha256") != replay_sha:
        raise ValueError("outer replay receipt SHA mismatch")
    inner_sha = receipt.get("inner_receipt_sha256")
    if not isinstance(inner_sha, str) or len(inner_sha) != 64:
        raise ValueError("outer inner receipt SHA missing")
    if replay.get("producer_receipt_sha256") != inner_sha:
        raise ValueError("replay is not bound to the v1 inner receipt")
    if replay.get("schema") != "d972-b4-u-metabelian-kbmag-replay/v1":
        raise ValueError("same-job replay schema drift")
    if replay.get("status") != _expected_replay_status(comm, norms):
        raise ValueError("same-job replay status drift")
    for field, expected in (
        ("source_sha256", SOURCE_SHA),
        ("rs_constructor_sha256", RS_CONSTRUCTOR_SHA),
        ("rho_words_sha256", RHO_SHA),
        ("relator_sha256", RELATOR_SHA),
        ("norm_original_sha256", NORM_SHA),
    ):
        if replay.get(field) != expected or receipt.get(field) != expected:
            raise ValueError(f"same-job replay binding drift: {field}")
    if replay.get("norm_count") != 972 or replay.get("commutator_count") != 12880:
        raise ValueError("same-job replay ledger count drift")
    if (
        replay.get("gpgenmult_rechecked") is not True
        or replay.get("gpcheckmult_rechecked") is not True
        or replay.get("gpaxioms_rechecked") is not True
        or replay.get("automata_replayed") is not True
    ):
        raise ValueError("same-job replay GAP/FSA gate not satisfied")
    for field in ("commutator_ledger_sha256", "norm_ledger_sha256"):
        if replay.get(field) != receipt.get(field):
            raise ValueError(f"same-job replay ledger binding drift: {field}")
    if replay.get("commutator_ledger_sha256") != digest(comm):
        raise ValueError("same-job replay commutator ledger digest mismatch")
    if replay.get("norm_ledger_sha256") != digest(norms):
        raise ValueError("same-job replay norm ledger digest mismatch")
    if replay.get("commutator_empty_count") != sum(comm):
        raise ValueError("same-job replay commutator count mismatch")
    if replay.get("norm_empty_count") != sum(norms):
        raise ValueError("same-job replay norm count mismatch")
    if replay.get("proof_level") != "DIRECT_GPAxioms_FSA_REPLAY_PENDING_LEAN":
        raise ValueError("same-job replay proof-level drift")


def _checked_snf_diagonal(diagonal: list[int], width: int = 161) -> tuple[int, list[int]]:
    """Reject free factors before interpreting the non-unit SNF entries."""
    if len(diagonal) != width:
        raise ValueError(f"SNF diagonal width drift: {len(diagonal)} != {width}")
    rank = sum(value != 0 for value in diagonal)
    if rank != width or any(value == 0 for value in diagonal):
        raise ValueError(f"SNF rank is not full: rank={rank} width={width}")
    return rank, sorted(abs(value) for value in diagonal if abs(value) > 1)


def snf_invariants(raw_relators: list[list[int]]) -> tuple[int, list[int]]:
    matrix_rows: list[list[int]] = []
    for word in raw_relators:
        row = [0] * 161
        for letter in word:
            row[abs(letter) - 1] += 1 if letter > 0 else -1
        matrix_rows.append(row)
    smith = smith_normal_form(Matrix(matrix_rows), domain=ZZ)
    diagonal = [int(smith[i, i]) for i in range(min(smith.shape))]
    return _checked_snf_diagonal(diagonal)


def validate(
    receipt_path: Path, output_path: Path, replay_path: Path | None = None
) -> dict:
    _, raw_relators, norm_rows = load_canonical()
    receipt_raw = receipt_path.read_bytes()
    receipt = json.loads(receipt_raw.decode("utf-8"))
    if receipt.get("schema") != "d972-b4-u-metabelian-kbmag/v2":
        raise ValueError("receipt schema drift")
    if receipt.get("producer_v1_sha256") != V1_SHA:
        raise ValueError("producer v1 digest drift")
    if receipt.get("source_sha256") != SOURCE_SHA or receipt.get("relator_sha256") != RELATOR_SHA:
        raise ValueError("receipt source digest drift")
    if (
        receipt.get("rs_constructor_sha256") != RS_CONSTRUCTOR_SHA
        or receipt.get("rho_words_sha256") != RHO_SHA
    ):
        raise ValueError("receipt constructor/rho digest drift")
    if receipt.get("norm_original_sha256") != NORM_SHA:
        raise ValueError("receipt norm digest drift")
    if receipt.get("word_artifact_sha256") != WORDS_SHA or \
            receipt.get("word_artifact_canonical_sha256") != WORDS_CANONICAL_SHA:
        raise ValueError("receipt word artifact digest drift")
    if receipt.get("raw_rs_relators_sha256") != RAW_RS_SHA or receipt.get("norm_rs_sha256") != NORM_RS_SHA:
        raise ValueError("receipt RS digest drift")
    if receipt.get("raw_rs_generator_count") != 161 or receipt.get("raw_rs_relator_count") != 5056:
        raise ValueError("receipt raw RS count drift")
    if receipt.get("norm_count") != 972 or receipt.get("commutator_count") != 12880:
        raise ValueError("receipt ledger count drift")
    if (receipt.get("large") is not False or
            receipt.get("filestore") is not False or
            receipt.get("diff1") is not False):
        raise ValueError("receipt is not the large=false lane")
    if (receipt.get("automatic_success") is not True or
            receipt.get("gpgenmult_rechecked") is not True or
            receipt.get("gpcheckmult_rechecked") is not True or
            receipt.get("gpaxioms_rechecked") is not True):
        raise ValueError("AutomaticStructure/GpGenMult/GpCheckMult/GpAxioms gate not satisfied")
    comm = receipt.get("commutator_ledger")
    norms = receipt.get("norm_ledger")
    if not isinstance(comm, list) or len(comm) != 12880 or any(type(x) is not bool for x in comm):
        raise ValueError("commutator ledger shape drift")
    if not isinstance(norms, list) or len(norms) != 972 or any(type(x) is not bool for x in norms):
        raise ValueError("norm ledger shape drift")
    if digest(comm) != receipt.get("commutator_ledger_sha256"):
        raise ValueError("commutator ledger digest mismatch")
    if digest(norms) != receipt.get("norm_ledger_sha256"):
        raise ValueError("norm ledger digest mismatch")
    if receipt.get("commutator_empty_count") != sum(comm):
        raise ValueError("commutator empty count mismatch")
    if receipt.get("norm_empty_count") != sum(norms):
        raise ValueError("norm empty count mismatch")

    replay_file = resolve_replay_path(receipt_path, replay_path)
    replay_raw = replay_file.read_bytes()
    replay = json.loads(replay_raw.decode("utf-8"))
    validate_replay_binding(receipt, replay_raw, replay, comm, norms)

    # Ensure the producer's claimed K_ab is independently reproduced from the
    # canonical raw relators, rather than accepted from its JSON field.
    snf_rank, invariants = snf_invariants(raw_relators)
    if invariants != AB or receipt.get("abelian_invariants") != AB:
        raise ValueError(f"K_ab SNF mismatch: {invariants}")
    if snf_rank != 161 or receipt.get("snf_rank") != 161:
        raise ValueError(f"K_ab SNF rank mismatch: {snf_rank}")

    status = receipt.get("status")
    if status == "B4_B_FINITE_ORDER_TERMINAL":
        if not all(comm) or not all(norms):
            raise ValueError("B4-B status without all-empty ledgers")
        if receipt.get("kernel_index") != 32 or receipt.get("kernel_order") != KERNEL_ORDER:
            raise ValueError("B4-B kernel order mismatch")
        if receipt.get("u_order") != U_ORDER:
            raise ValueError("B4-B U order mismatch")
    elif status == "B4_A_TERMINAL":
        if all(norms):
            raise ValueError("B4-A status without a norm defect")
        first = receipt.get("first_norm_defect")
        if not isinstance(first, list) or not first or first[0] != norms.index(False) + 1:
            raise ValueError("B4-A first defect mismatch")
    else:
        raise ValueError(f"nonterminal status: {status}")

    result = {
        "schema": "d972-b4-u-metabelian-kbmag-check/v2",
        "status": status,
        "proof_level": "INDEPENDENT_RAW_RS_LEDGER_AND_SNF_CROSSCHECK",
        "producer_receipt_sha256": hashlib.sha256(receipt_raw).hexdigest(),
        "replay_receipt_sha256": hashlib.sha256(replay_raw).hexdigest(),
        "inner_receipt_sha256": receipt["inner_receipt_sha256"],
        "replay_status": replay["status"],
        "post_replay_requested": True,
        "source_sha256": SOURCE_SHA,
        "raw_rs_relators_sha256": RAW_RS_SHA,
        "norm_rs_sha256": NORM_RS_SHA,
        "automatic_success": True,
        "gpgenmult_rechecked": True,
        "gpcheckmult_rechecked": True,
        "gpaxioms_rechecked": True,
        "commutator_count": len(comm),
        "commutator_empty_count": sum(comm),
        "norm_count": len(norms),
        "norm_empty_count": sum(norms),
        "abelian_invariants": AB,
        "snf_rank": snf_rank,
        "kernel_index": 32,
        "kernel_order": KERNEL_ORDER,
        "u_order": U_ORDER,
        "independent_raw_rs_replay": True,
        "independent_snf_match": True,
        "independent_replay_binding": True,
    }
    output_path.write_text(compact(result) + "\n", encoding="utf-8")
    print("B4_U_METABELIAN_V2_CHECK", f"status={status}",
          f"comm={sum(comm)}/12880", f"norm={sum(norms)}/972",
          f"u_order={U_ORDER}", f"output={output_path}")
    return result


def selftest() -> None:
    """Light fail-closed tests; no canonical SNF or 5056-row load is done."""
    assert free_reduce([1, -1, 2, 2, -2]) == [2]
    assert toggle(0, 1) == 1
    assert toggle(1, 1) == 0
    assert toggle(0, 31) == 31
    assert toggle(31, 31) == 0
    fixture = [
        [0, [[0, 0]], ""],
        [1, [[1, 0]], [1, -1]],
    ] + [[2, [[2, 0]], []] for _ in range(970)]
    fixture[891][2] = ""
    rows, legacy = normalize_word_rows(fixture)
    assert legacy == [0, 891]
    assert rows[0][2] == [] and rows[1][2] == [1, -1]

    rank, invariants = _checked_snf_diagonal([1] * 151 + [9] * 10)
    assert rank == 161 and invariants == AB

    def must_reject(thunk, label: str) -> None:
        try:
            thunk()
        except (OSError, TypeError, ValueError, KeyError, IndexError):
            return
        raise AssertionError(f"negative selftest accepted: {label}")

    must_reject(
        lambda: resolve_replay_path(Path("d972_missing_receipt.json"), None),
        "missing replay receipt",
    )
    must_reject(
        lambda: _checked_snf_diagonal([1] * 160 + [0]),
        "zero SNF diagonal",
    )
    forged_raw = b"{}\n"
    forged_outer = {
        "post_replay_requested": True,
        "replay_receipt_sha256": hashlib.sha256(forged_raw).hexdigest(),
        "inner_receipt_sha256": "1" * 64,
    }
    forged_replay = {
        "schema": "d972-b4-u-metabelian-kbmag-replay/v1",
        "producer_receipt_sha256": "2" * 64,
    }
    must_reject(
        lambda: validate_replay_binding(
            forged_outer, forged_raw, forged_replay, [True] * 12880, [True] * 972
        ),
        "forged replay inner binding",
    )
    print(
        "B4_U_METABELIAN_V2_SELFTEST_PASS",
        "snf_rank=161 missing_replay=BLOCKED zero_diagonal=BLOCKED forged_replay=BLOCKED",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("receipt", type=Path, nargs="?")
    parser.add_argument("--output", type=Path)
    parser.add_argument(
        "--replay",
        type=Path,
        help=f"same-job replay receipt (default: sibling {REPLAY_NAME})",
    )
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args()
    if args.selftest:
        selftest()
        return 0
    if args.receipt is None or args.output is None:
        parser.error("receipt and --output are required unless --selftest is used")
    try:
        validate(args.receipt, args.output, args.replay)
    except (OSError, TypeError, ValueError, KeyError, IndexError) as exc:
        print(f"B4_U_METABELIAN_V2_CHECK_ERROR {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
