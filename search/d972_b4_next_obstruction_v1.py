#!/usr/bin/env python3
"""Exact literal-A.18 Magnus campaign for degrees 2 through 6.

This wrapper deliberately does not use the old rho-orbit tail as a quotient
ideal.  It reconstructs the 18 K(0,5) prefix rows and the five literal raw
A.18 coface images of the 28 seed rows, then feeds that presentation to the
audited encoded Magnus algebra.  The defect is the unconditional five-coface
D-tilde word, not the reverse rho norm.

The independent checker reconstructs the same maps, ideal, and defect without
importing this module or any of its helper routines.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
import tempfile
import time
from pathlib import Path
from typing import Any, Iterable, Sequence


ROOT = Path(__file__).resolve().parents[1]
CORE_SHARD_PATH = ROOT / "search" / "d972_b4_magnus_ideal_shard_v2.py"
CORE_MERGE_PATH = ROOT / "search" / "d972_b4_magnus_ideal_merge_v3.py"
CORE_BASE_MERGE_PATH = ROOT / "search" / "d972_b4_magnus_ideal_merge_v2.py"
INPUT_PATH = ROOT / "search" / "certs" / "d972_b4_p2_magnus_input_v2_20260816.json"
WORDS_PATH = ROOT / "search" / "certs" / "d972_b4_word_key_artifact_v1_20260816.json"

NGEN = 6
PREFIX_COUNT = 18
SEED_COUNT = 28
COFACE_COUNT = 5
RELATOR_COUNT = 158
ROOF_COUNT = 972
DEGREES = tuple(range(2, 7))
SHARD_COUNTS = {2: 1, 3: 1, 4: 1, 5: 1, 6: 16}

SCHEMA = "d972-b4-next-obstruction/v2"
FINAL_MARKER = "D972_B4_NEXT_OBSTRUCTION_V2_FINAL"
SEMANTICS = "raw_a18_18_plus_140"

INPUT_SHA = "c61b2b77131127aca83a8d7c56b7fdadd2d519b040ea4d91093622c813c2b4a9"
WORDS_SHA = "564a921be8114bdeb963f679c121e8d9aa90e148c65e95e393874fcba843e9f9"
RELATOR_SHA = "12fc1146dce5179c2b5fc44a3ceed6356a6b2c4835a564b55e9a9cd679fccd2e"
PREFIX_SHA = "62ccbb87e2b27784b5330812252a2eaf247fea0fef4eda078ea6724c5b2a31e6"
SEED_SHA = "366c893977a0684a294e8bd488741c735016ec5caf18804415dfc73acdb09822"
A18_ROWS_SHA = "1f0cacaa20ab8474245f30568469de807b5877b2ca7dd0d6668c9b8956750722"
PRESENTATION_SHA = "783d7d80f472fbf6abc8a2f58454048de361e95774c76ce1c511982bb44eb305"
DTILDE_SHA = "32cdc85b315817e939feca628bc15235a55664157ca1e272815a53f1de4631ef"
LITERAL_INPUT_SHA = "60efdb2f7fc847d065701bf27d676cec558e0be9a276ee2a782c3ff0c5754494"
TARGET_KEY_DIGEST = "9c77e6768feb7ffe7143abf18f753af70e81b8e9cc792910c30ae0075d3b1d62"
TUPLE_DIGEST = "32e78ca5b97cd8a6fa59a150dac77719c1b8cb527f0467570c4d284600465a91"
CANONICAL_RHO = [[-6, -5, -3], [3], [5], [-3, -2, -1], [-5, -4, -1], [1]]

CORE_SHARD_SHA = "1a18994e3933d5d42e85274af62badb89c2f9a65c92c63862d1740ac2d47da63"
CORE_MERGE_SHA = "6ccce4e95378dfa22051bd8c09e3d3aa5a91234b8d155c0fb57fd18c34f24bf5"
CORE_BASE_MERGE_SHA = "c79abb6ff51bccaaf98992fa070fecf3aba9d70ea4f6b6deff90d4cfcef1814c"

MAPS = (
    ("123", (1,), (4,)),
    ("234", (4,), (6,)),
    ("12,3,4", (2, 4), (6,)),
    ("1,23,4", (1, 2), (5, 6)),
    ("1,2,34", (1,), (4, 5)),
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def canonical_json(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=True, separators=(",", ":")).encode("ascii")


def digest(value: object) -> str:
    return hashlib.sha256(canonical_json(value)).hexdigest()


def file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def free_reduce(word: Iterable[int]) -> list[int]:
    out: list[int] = []
    for raw in word:
        n = int(raw)
        require(n != 0 and abs(n) <= NGEN, "signed word alphabet drift")
        if out and out[-1] == -n:
            out.pop()
        else:
            out.append(n)
    return out


def inverse_word(word: Sequence[int]) -> list[int]:
    return [-int(x) for x in reversed(word)]


def marked_substitute(word: Sequence[int], left: Sequence[int],
                      right: Sequence[int]) -> list[int]:
    out: list[int] = []
    for raw in word:
        n = int(raw)
        require(n != 0 and abs(n) in (1, 4), "marked F2 seed alphabet drift")
        image = list(left if abs(n) == 1 else right)
        out.extend(inverse_word(image) if n < 0 else image)
    return free_reduce(out)


def exact_dtilde(f2_word: Sequence[int]) -> list[int]:
    """Build the unconditional five-coface defect D-tilde(f)."""
    marked = []
    for raw in f2_word:
        n = int(raw)
        require(n != 0 and abs(n) in (1, 2), "roof F2 alphabet drift")
        marked.append(1 if n == 1 else -1 if n == -1 else 4 if n == 2 else -4)
    x15 = (-3, -2, -1)
    x45 = (-6, -5, -3)
    return free_reduce(
        inverse_word(marked_substitute(marked, x45, (6,)))
        + inverse_word(marked_substitute(marked, (1,), x15))
        + marked_substitute(marked, (4,), (6,))
        + marked_substitute(marked, x45, x15)
        + marked_substitute(marked, (1,), (4,))
    )


def flat_key(key: object) -> str:
    require(isinstance(key, list) and len(key) == 3,
            "word artifact key shape drift")
    m, can9, can4 = key
    require(isinstance(m, int) and isinstance(can9, list) and len(can9) == 3 and
            isinstance(can4, list) and len(can4) == 9,
            "word artifact key component drift")
    coords: list[int] = []
    for pair in can9:
        require(isinstance(pair, list) and len(pair) == 2 and
                all(isinstance(x, int) for x in pair),
                "word artifact D9 key drift")
        coords.extend(pair)
    require(all(isinstance(x, int) for x in can4),
            "word artifact PSL key drift")
    return "(" + str(m) + ";" + ",".join(map(str, coords)) + ";" + ",".join(map(str, can4)) + ")"


def load_word_artifact(path: Path) -> tuple[list[list[int]], list[str], list[list[int]]]:
    require(file_sha(path) == WORDS_SHA, "word artifact SHA drift")
    obj = json.loads(path.read_text(encoding="utf-8"))
    require(obj.get("schema") == "d972-b4-word-key-artifact/v1" and
            obj.get("count") == ROOF_COUNT, "word artifact schema/count drift")
    rows = obj.get("rows")
    require(isinstance(rows, list) and len(rows) == ROOF_COUNT,
            "word artifact row count drift")
    require(obj.get("source_target_key_digest") == TARGET_KEY_DIGEST,
            "word artifact target digest drift")
    require(obj.get("frozen_tuple_sha256") == TUPLE_DIGEST,
            "word artifact tuple digest drift")
    require(obj.get("canonical_bytes_sha256") == digest(rows),
            "word artifact canonical digest drift")
    words: list[list[int]] = []
    keys: list[str] = []
    for row in rows:
        require(isinstance(row, list) and len(row) == 3,
                "word artifact row shape drift")
        m, key, word = row
        require(isinstance(m, int) and isinstance(key, list) and
                key and key[0] == m, "word artifact key drift")
        require(not (isinstance(word, str) and word == ""),
                "legacy empty word row rejected")
        require(isinstance(word, list) and all(isinstance(x, int) and
                x != 0 and abs(x) <= 2 for x in word),
                "word artifact F2 word drift")
        keys.append(flat_key(key))
        words.append([int(x) for x in word])
    require(len(set(keys)) == ROOF_COUNT, "word artifact key uniqueness drift")
    require(hashlib.sha256(("\n".join(sorted(keys)) + "\n").encode("ascii")).hexdigest() == TARGET_KEY_DIGEST,
            "word artifact key-set digest drift")
    dtilde = [exact_dtilde(word) for word in words]
    require(digest(dtilde) == DTILDE_SHA, "D-tilde digest drift")
    return words, keys, dtilde


def build_literal(source_path: Path, words_path: Path, output: Path) -> dict[str, Any]:
    require(file_sha(source_path) == INPUT_SHA, "canonical input SHA drift")
    source = json.loads(source_path.read_text(encoding="utf-8"))
    require(source.get("schema") == "d972-b4-p2-magnus-input/v2" and
            source.get("relator_count") == RELATOR_COUNT,
            "canonical input schema/count drift")
    relators = [[int(x) for x in row] for row in source.get("all_relators", [])]
    require(len(relators) == RELATOR_COUNT and
            source.get("all_relators_sha256") == RELATOR_SHA and
            digest(relators) == RELATOR_SHA, "canonical relator digest drift")
    prefix = relators[:PREFIX_COUNT]
    seeds = relators[PREFIX_COUNT:PREFIX_COUNT + SEED_COUNT]
    require(len(prefix) == PREFIX_COUNT and len(seeds) == SEED_COUNT,
            "literal prefix/seed count drift")
    require(digest(prefix) == PREFIX_SHA and digest(seeds) == SEED_SHA,
            "literal prefix/seed digest drift")
    words, keys, dtilde = load_word_artifact(words_path)
    source_keys = [str(x) for x in source.get("target_keys", [])]
    require(len(source_keys) == ROOF_COUNT and len(set(source_keys)) == ROOF_COUNT and
            set(source_keys) == set(keys), "word artifact/source key set drift")
    a18: list[list[int]] = []
    for _name, left, right in MAPS:
        a18.extend(marked_substitute(row, left, right) for row in seeds)
    require(len(a18) == COFACE_COUNT * SEED_COUNT and
            digest(a18) == A18_ROWS_SHA, "literal A.18 rows drift")
    presentation = prefix + a18
    require(len(presentation) == RELATOR_COUNT and
            digest(presentation) == PRESENTATION_SHA,
            "literal A.18 presentation drift")

    # The encoded shard core requires the canonical rho field for its legacy
    # input parser.  It is retained only in this temporary transport object;
    # the actual relator list, ideal, and defect below never use it.
    literal = dict(source)
    literal.update({
        "all_relators": presentation,
        "all_relators_sha256": digest(presentation),
        "presentation_semantics": SEMANTICS,
        "raw_source_sha256": INPUT_SHA,
        "prefix_sha256": PREFIX_SHA,
        "seed_sha256": SEED_SHA,
        "a18_rows_sha256": A18_ROWS_SHA,
        "presentation_sha256": PRESENTATION_SHA,
        "dtilde_sha256": DTILDE_SHA,
        "rho_tail_used": False,
        "rho_used": False,
        "rho_role": "transport_only_not_used_in_ideal_or_defect",
    })
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(literal, ensure_ascii=True, sort_keys=True,
                                 indent=2) + "\n", encoding="utf-8", newline="\n")
    require(file_sha(output) == LITERAL_INPUT_SHA,
            "deterministic literal transport SHA drift")
    return {
        "literal_path": output,
        "literal_input_sha256": file_sha(output),
        "source": source,
        "prefix": prefix,
        "seeds": seeds,
        "a18_rows": a18,
        "presentation": presentation,
        "words": words,
        "keys": keys,
        "dtilde": dtilde,
    }


def import_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_cores():
    require(file_sha(CORE_SHARD_PATH) == CORE_SHARD_SHA,
            "Magnus shard core SHA drift")
    require(file_sha(CORE_MERGE_PATH) == CORE_MERGE_SHA,
            "Magnus merge core SHA drift")
    require(file_sha(CORE_BASE_MERGE_PATH) == CORE_BASE_MERGE_SHA,
            "Magnus base merge core SHA drift")
    shard = import_module(CORE_SHARD_PATH, "d972_literal_a18_shard_core")
    merge = import_module(CORE_MERGE_PATH, "d972_literal_a18_merge_core")
    require(shard.NGEN == NGEN and shard.RELATOR_COUNT == RELATOR_COUNT,
            "Magnus core constant drift")
    require(shard.monomial_count(2) == 43 and
            shard.monomial_count(6) == 55987, "Magnus monomial count drift")
    return shard, merge


def annotate(path: Path, meta: dict[str, Any]) -> None:
    obj = json.loads(path.read_text(encoding="utf-8"))
    obj.update(meta)
    path.write_text(json.dumps(obj, ensure_ascii=True, sort_keys=True,
                               indent=2) + "\n", encoding="utf-8")


def campaign_meta(info: dict[str, Any], degree: int) -> dict[str, Any]:
    return {
        "campaign_schema": SCHEMA,
        "campaign_degree": degree,
        "presentation_semantics": SEMANTICS,
        "raw_source_sha256": INPUT_SHA,
        "word_artifact_sha256": WORDS_SHA,
        "relator_sha256": RELATOR_SHA,
        "prefix_sha256": PREFIX_SHA,
        "seed_sha256": SEED_SHA,
        "a18_rows_sha256": A18_ROWS_SHA,
        "presentation_sha256": PRESENTATION_SHA,
        "dtilde_sha256": DTILDE_SHA,
        "literal_input_sha256": info["literal_input_sha256"],
        "rho_tail_used": False,
        "rho_used": False,
        "rho_role": "omitted_from_ideal_and_defect",
        "campaign_wrapper_sha256": file_sha(Path(__file__).resolve()),
        "core_shard_sha256": CORE_SHARD_SHA,
        "core_merge_sha256": CORE_MERGE_SHA,
        "core_base_merge_sha256": CORE_BASE_MERGE_SHA,
        "complete_two_sided_ideal": True,
        "no_bounded_word_search": True,
        "no_matrix_group_enumeration": True,
    }


def run_shard(args: argparse.Namespace) -> int:
    require(args.degree in DEGREES, "degree must be 2..6")
    require(args.output is not None and args.shard_index is not None and
            args.shard_count is not None, "shard arguments are incomplete")
    require(args.shard_count == SHARD_COUNTS[args.degree] and
            0 <= args.shard_index < args.shard_count,
            "campaign shard index/count drift")
    with tempfile.TemporaryDirectory(prefix="d972_literal_a18_") as td:
        literal = build_literal(args.input, args.artifact,
                                Path(td) / "literal_input.json")
        shard, _merge = load_cores()
        code = shard.main([
            "--degree", str(args.degree),
            "--shard-index", str(args.shard_index),
            "--shard-count", str(args.shard_count),
            "--input", str(literal["literal_path"]),
            "--output", str(args.output),
        ])
        require(code == 0, "Magnus shard core returned nonzero")
        annotate(args.output, campaign_meta(literal, args.degree))
    print(f"{FINAL_MARKER} phase=SHARD status=PASS degree={args.degree} output={args.output}",
          flush=True)
    return 0


def discover_shards(directory: Path, degree: int, count: int, pattern: str) -> list[Path]:
    expected = [directory / pattern.format(degree=degree, index=i, count=count)
                for i in range(count)]
    require(all(path.is_file() for path in expected),
            f"shard directory is incomplete: {expected}")
    require(set(directory.glob(pattern.format(degree=degree, index="*", count=count))) == set(expected),
            "shard directory contains unexpected files")
    return expected


def expected_relator_indices(index: int, count: int) -> list[int]:
    require(count >= 1 and 0 <= index < count, "invalid shard index/count")
    return [i + 1 for i in range(RELATOR_COUNT) if i % count == index]


def bind_shard_records(paths: Sequence[Path], core_records: Sequence[dict[str, Any]],
                       degree: int, count: int, info: dict[str, Any],
                       input_digests: dict[str, str]) -> list[dict[str, Any]]:
    """Promote the core's terse records to a closed campaign receipt."""
    require(count == SHARD_COUNTS[degree] and len(paths) == count and
            len(core_records) == count, "campaign shard record count drift")
    by_index = {record.get("shard_index"): record for record in core_records}
    require(set(by_index) == set(range(count)), "core shard index coverage drift")
    meta = campaign_meta(info, degree)
    records: list[dict[str, Any]] = []
    coverage: list[int] = []
    for index, path in enumerate(paths):
        obj = json.loads(path.read_text(encoding="utf-8"))
        expected = expected_relator_indices(index, count)
        expected_digest = digest(expected)
        require(obj.get("schema") == "d972-b4-magnus-ideal-shard/v2" and
                obj.get("degree") == degree and
                obj.get("shard_index") == index and
                obj.get("shard_count") == count,
                f"shard identity drift: {path}")
        require(obj.get("relator_indices") == expected and
                obj.get("relator_indices_sha256") == expected_digest,
                f"shard relator coverage drift: {path}")
        require(obj.get("input_sha256") == info["literal_input_sha256"] and
                obj.get("input_digests") == input_digests,
                f"shard literal transport binding drift: {path}")
        require(obj.get("monomial_count") == sum(NGEN ** n for n in range(degree + 1)) and
                isinstance(obj.get("ideal_rank"), int) and obj["ideal_rank"] >= 0,
                f"shard dimension metadata drift: {path}")
        for field, value in meta.items():
            require(obj.get(field) == value,
                    f"shard campaign binding drift for {field}: {path}")
        core = by_index[index]
        shard_sha = file_sha(path)
        require(core == {
            "path": str(path),
            "sha256": shard_sha,
            "shard_index": index,
            "shard_count": count,
            "relator_count": len(expected),
            "ideal_rank": obj["ideal_rank"],
        }, f"core shard record drift: {path}")
        records.append({
            "path": str(path),
            "sha256": shard_sha,
            "degree": degree,
            "shard_index": index,
            "shard_count": count,
            "relator_count": len(expected),
            "relator_indices": expected,
            "relator_indices_sha256": expected_digest,
            "monomial_count": obj["monomial_count"],
            "ideal_rank": obj["ideal_rank"],
            "input_sha256": info["literal_input_sha256"],
            "literal_input_sha256": info["literal_input_sha256"],
            "input_digests": dict(input_digests),
            "campaign_schema": SCHEMA,
            "campaign_degree": degree,
            "presentation_semantics": SEMANTICS,
            "raw_source_sha256": INPUT_SHA,
            "word_artifact_sha256": WORDS_SHA,
            "relator_sha256": RELATOR_SHA,
            "prefix_sha256": PREFIX_SHA,
            "seed_sha256": SEED_SHA,
            "a18_rows_sha256": A18_ROWS_SHA,
            "presentation_sha256": PRESENTATION_SHA,
            "dtilde_sha256": DTILDE_SHA,
            "rho_tail_used": False,
            "rho_used": False,
            "rho_role": "omitted_from_ideal_and_defect",
            "campaign_wrapper_sha256": meta["campaign_wrapper_sha256"],
            "core_shard_sha256": CORE_SHARD_SHA,
            "core_merge_sha256": CORE_MERGE_SHA,
            "core_base_merge_sha256": CORE_BASE_MERGE_SHA,
            "complete_two_sided_ideal": True,
        })
        coverage.extend(expected)
    require(sorted(coverage) == list(range(1, RELATOR_COUNT + 1)) and
            len(coverage) == len(set(coverage)),
            "campaign shard relator coverage is not an exact partition")
    return records


def status_for(degree: int, defects: Sequence[dict[str, Any]],
               relator_bad: Sequence[int], binding_bad: Sequence[str],
               construction_bad: Sequence[str]) -> str:
    if relator_bad or binding_bad or construction_bad:
        return f"D{degree}_MAGNUS_GATE_FAILURE"
    if defects:
        return f"D{degree}_A_CANDIDATE_NEEDS_CHECK"
    return f"D{degree}_ALLPASS_UNKNOWN"


def evaluate_literal(merge, basis: dict[int, int], degree: int,
                     info: dict[str, Any], shard_records: list[dict[str, Any]]) -> dict[str, Any]:
    evaluator, quotient_dimension, _nonpivots = merge.MERGE.quotient_evaluator(basis, degree)

    def residue(word: Sequence[int]) -> int:
        return evaluator(word) ^ 1

    relator_bad = [index + 1 for index, word in
                   enumerate(info["presentation"]) if residue(word)]
    dtilde_rows: list[dict[str, Any]] = []
    for index, (word, key) in enumerate(zip(info["dtilde"], info["keys"]), 1):
        value = residue(word)
        dtilde_rows.append({
            "index": index,
            "target_key": key,
            "word": word,
            "residue_hex": format(value, "x"),
        })
    defects = [row for row in dtilde_rows if row["residue_hex"] != "0"]
    binding_bad: list[str] = []
    construction_bad: list[str] = []
    status = status_for(degree, defects, relator_bad, binding_bad, construction_bad)
    return {
        "degree": degree,
        "monomial_count": merge.MERGE.SHARD.monomial_count(degree),
        "ideal_rank": len(basis),
        "quotient_dimension": quotient_dimension,
        "shards": shard_records,
        "rho_tail_used": False,
        "rho_used": False,
        "rho_role": "omitted_from_ideal_and_defect",
        "relator_bad": relator_bad,
        "binding_bad": binding_bad,
        "construction_bad": construction_bad,
        "dtilde_count": len(dtilde_rows),
        "dtilde_defect_count": len(defects),
        "first_defect": defects[0] if defects else None,
        "dtilde_rows": dtilde_rows,
        "ideal_basis_hex": [format(basis[p], "x") for p in sorted(basis)],
        "ideal_basis_pivots": sorted(basis),
        "status": status,
    }


def run_merge(args: argparse.Namespace) -> int:
    require(args.degree in DEGREES, "degree must be 2..6")
    require(args.output is not None and args.shard_dir is not None and
            args.shard_count is not None, "merge arguments are incomplete")
    require(args.shard_count == SHARD_COUNTS[args.degree],
            "campaign shard count drift")
    with tempfile.TemporaryDirectory(prefix="d972_literal_a18_") as td:
        info = build_literal(args.input, args.artifact,
                             Path(td) / "literal_input.json")
        _shard, merge = load_cores()
        paths = discover_shards(args.shard_dir, args.degree, args.shard_count, args.pattern)
        obj, literal_sha, digests = merge.MERGE.load_input(info["literal_path"])
        require(literal_sha == info["literal_input_sha256"],
                "literal transport SHA drift")
        basis, core_records = merge.stream_load_shards(paths, args.degree,
                                                        literal_sha, digests)
        records = bind_shard_records(paths, core_records, args.degree,
                                     args.shard_count, info, digests)
        row = evaluate_literal(merge, basis, args.degree, info, records)
        result: dict[str, Any] = {
            "schema": SCHEMA,
            "final_marker": FINAL_MARKER,
            "status": row["status"],
            "campaign_degree": args.degree,
            "source_sha256": INPUT_SHA,
            "word_artifact_sha256": WORDS_SHA,
            "relator_sha256": RELATOR_SHA,
            "prefix_sha256": PREFIX_SHA,
            "seed_sha256": SEED_SHA,
            "a18_rows_sha256": A18_ROWS_SHA,
            "presentation_sha256": PRESENTATION_SHA,
            "dtilde_sha256": DTILDE_SHA,
            "literal_input_sha256": literal_sha,
            "input_digests": digests,
            "presentation_semantics": SEMANTICS,
            "rho_tail_used": False,
            "rho_used": False,
            "rho_role": "omitted_from_ideal_and_defect",
            "complete_two_sided_ideal": True,
            "no_bounded_word_search": True,
            "no_matrix_group_enumeration": True,
            "campaign_wrapper_sha256": file_sha(Path(__file__).resolve()),
            "core_shard_sha256": CORE_SHARD_SHA,
            "core_merge_sha256": CORE_MERGE_SHA,
            "core_base_merge_sha256": CORE_BASE_MERGE_SHA,
            "ideal_model": (
                "F2 noncommutative Magnus truncation; literal A.18 ideal = "
                "18 K(0,5) relators plus five raw coface images of 28 seeds"
            ),
            "defect_model": "unconditional five-coface Dtilde(f), not rho norm",
            "degrees": {str(args.degree): row},
            "elapsed_seconds": 0,
        }
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, ensure_ascii=True,
                                           sort_keys=True, indent=2) + "\n",
                                encoding="utf-8")
    print(f"{FINAL_MARKER} phase=MERGE status={row['status']} degree={args.degree} output={args.output}",
          flush=True)
    return 0


def self_test() -> None:
    with tempfile.TemporaryDirectory(prefix="d972_literal_a18_selftest_") as td:
        info = build_literal(INPUT_PATH, WORDS_PATH, Path(td) / "literal.json")
        require(info["a18_rows"][:SEED_COUNT] == info["seeds"],
                "123 coface reconstruction fixture failed")
        require(len(info["a18_rows"]) == 140 and len(info["dtilde"]) == 972,
                "literal row count fixture failed")
        require(digest(info["a18_rows"]) == A18_ROWS_SHA and
                digest(info["presentation"]) == PRESENTATION_SHA and
                digest(info["dtilde"]) == DTILDE_SHA,
                "literal digest fixture failed")
        shard, _merge = load_cores()
        require(shard.monomial_count(2) == 43 and
                shard.monomial_count(6) == 55987,
                "Magnus degree calibration fixture failed")
        require(status_for(2, [], [], ["synthetic-binding"], []) ==
                "D2_MAGNUS_GATE_FAILURE",
                "no-defects/bad-gate negative fixture failed")
        for degree, count in SHARD_COUNTS.items():
            coverage = [item for index in range(count)
                        for item in expected_relator_indices(index, count)]
            require(sorted(coverage) == list(range(1, RELATOR_COUNT + 1)) and
                    len(coverage) == len(set(coverage)),
                    f"degree-{degree} exact shard partition fixture failed")
    print("D972_B4_NEXT_OBSTRUCTION_V2_SELFTEST_PASS")
    print(f"{FINAL_MARKER} phase=SELFTEST status=PASS degrees=2,3,4,5,6")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("self-test", "shard", "merge"),
                        default="self-test")
    parser.add_argument("--degree", type=int, default=6)
    parser.add_argument("--input", type=Path, default=INPUT_PATH)
    parser.add_argument("--artifact", type=Path, default=WORDS_PATH)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--shard-index", type=int)
    parser.add_argument("--shard-count", type=int)
    parser.add_argument("--shard-dir", type=Path)
    parser.add_argument("--pattern", default="d972_b4_next_d{degree}_shard_{index}_of_{count}.json")
    args = parser.parse_args(argv)
    if args.mode == "self-test":
        self_test()
        return 0
    try:
        if args.mode == "shard":
            return run_shard(args)
        return run_merge(args)
    except Exception as exc:
        print(f"{FINAL_MARKER} status=ERROR error={type(exc).__name__}:{exc}",
              file=sys.stderr, flush=True)
        raise


if __name__ == "__main__":
    raise SystemExit(main())
