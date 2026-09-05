#!/usr/bin/env python3
"""Independent checker for the repaired R07 actual root-scalar batch v2.

This file intentionally has no import of the producer.  It owns its cache
projection, v541 raw seed and actor adjoints, packed lower contractions,
relation walk, scalar replay, and output-roster comparison; only the already
audited checker-v15 arithmetic is reused.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import tempfile
from pathlib import Path
from typing import Any, Iterable

import numpy as np

try:
    import check_d972_r07_targeted_grade2_owner_generated_join_v15 as ARITH
except ModuleNotFoundError:  # pragma: no cover
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import check_d972_r07_targeted_grade2_owner_generated_join_v15 as ARITH


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "d972.r07.actual-grade2.root-scalar-batch.v2"
V541_FORMULA_ID = "r07.v541.formulas-2.1-2.2-4.1.raw-seed-plus-actor-lower-adjoint"
ARITH_PATH = PROJECT_ROOT / "search" / "check_d972_r07_targeted_grade2_owner_generated_join_v15.py"
ARITH_SHA256 = "8f718811c518f8d3e1d09de497b955d18c221e983391721068cc35be0000a662"
PRODUCER_ARITH_PATH = PROJECT_ROOT / "search" / "d972_r07_targeted_grade2_owner_generated_join_v15.py"
PRODUCER_ARITH_SHA256 = "76546bef263ad260f24632c0da46cfb913ee48759e0533d591c507d072037632"
P1_RUN = 33851744070; P1_ATTEMPT = 1
P1_HEAD = "6673eb2ea15ca6022acc2ddc5a8a204a0380172f"
P1_ARTIFACT = 9931437113
P1_ARTIFACT_NAME = "task809-canonical-p1-degree2-lift-v9-33851744070-1"
P1_ARCHIVE_BYTES = 641518300
P1_ARCHIVE_SHA256 = "sha256:6d6f2ec6eb7f1245b8e7d52645c710ecd519ae0cc442340237d1098c7fa63d5c"
P1_MANIFEST_BYTES = 17472
P1_MANIFEST_SHA256 = "86e8b14cb0a60c86468ffb54a7bf14980366406a1e5bea17018fc6961f331feb"
P1_CACHE_BYTES = 292444992
P1_CACHE_SHA256 = "b88edb9b12753cdb7a3629403f8ac14206595e03525fa2a201b6b00b985c1abf"
P1_INSTRUCTION_BYTES = 349055442
P1_INSTRUCTION_SHA256 = "8b549337786b1f3b970a7250f1c326724ef957369c213c55af5a3d52a96f38ae"
P1_ROWS = 8059; P1_ROW_TRITS = 145152; P1_ROW_BYTES = 36288
SOURCE_WIDTH = 36288; SLICE_BYTES = 9072
SOURCE0C = 6048; SOURCE1C = 18144
LOWER_WIDTH = 96776; LOWER_PACKED_BYTES = LOWER_WIDTH // 4
OLD_LOWER_WIDTH = 6056; OLD_GRADE_WIDTH = 72576; NEW_BASIS_WIDTH = 18144
PHYSICAL_WIDTH = 48384; PHYSICAL_PACKED_BYTES = 12096
ACTORS = (1, -1, 2, -2); CHARACTERS = ((0, 0), (0, 1), (1, 0), (1, 1))
OLD_RANKS = (505, 503, 503, 503); NEW_RANKS = (1509, 1512, 1512, 1512)
ORIGIN_RANGES = ((0, 2064), (2064, 4120), (4120, 6176), (6176, 8232))
SCALAR_ORIGINS = 32280; TASK554_ORIGINS = 8232; POW3 = (1, 3, 9, 27)

SEPARATOR_RUN = 33891714539; SEPARATOR_ATTEMPT = 1
SEPARATOR_HEAD = "7b7b9de20faaa3b8f26e331bb738b374f6f5708c"
SEPARATOR_ARTIFACT = 9944214057
SEPARATOR_ARTIFACT_NAME = "d972-r07-grade2-physical-state-separator-v2-candidate-33891714539-1"
SEPARATOR_ARCHIVE_BYTES = 107195261
SEPARATOR_ARCHIVE_SHA256 = "sha256:2d91e2e94ab7eb235805eb0f7c04ff87edef3954460d686f047d8abcfa99c017"
SEPARATOR_MANIFEST_SHA256 = "d11d551c2b1a127bd900c013cbc684eef698372660ff733b10f82bb4793f227b"
SEPARATOR_PHYSICAL_BYTES = 16377984
SEPARATOR_PHYSICAL_SHA256 = "1246ae0c23c7dcbfc2a1c2f73075f38968a4ab7b2e5c8fc006f0f8aafae2d57e"
SEPARATOR_LAMBDA_SHA256 = "7522ee1f00f386b229ea46bc0f2b9fdf2854cf03c262f40a2f60dd9ced0102ed"
SEPARATOR_TERMINAL_SHA256 = "098d5961cddc187d01c08e22f9f40ce55a7a02e8a1b1d088eca8c804957098cf"
SEPARATOR_RESULT_SHA256 = "d23892a4319a6d7eaa3d09af17a84e59cb6b0a1635f527fb77dc1038ae749968"
SEPARATOR_CHECKER_SHA256 = "2cad883205a5a1dc6e8795567004e071c3a7868351cf1d801727a695b43aa433"
SEPARATOR_GENERATION = 8059; SEPARATOR_RANK = 1354
SEPARATOR_STATE_HEAD = "69fdcc8cd740f8ea11bd198aaf44bcf50d1c4980331f51aa7f792544b00f9d88"

TASK554_RUN = 33677346616; TASK554_ATTEMPT = 1
TASK554_HEAD = "22c6dddb43d107c05e65f53ad898823ae8ebe276"
TASK554_BODY_DIGESTS = (
    "1f191d88a0453360021ec57d253a7d16c9a66ac059ddaaadb6db3e2b9293c865",
    "9ebcc7ad1141c20aeaff82eb4a83a9489dc492b30220547f23526b4fcdd8dc74",
    "d783bbe6c92c15a241eb78d0b25bca5e7c00f60799ce82f6df8b1d3ee7a202f6",
    "a6dcc904fc3e9daae008f72de7e83ffadcd39055d557621b9cdf06baea0e83ac",
    "642a4ec0ad6ad4ea659e84330e34006c767ca029203446cb64a17c151fefdb01",
)
TASK554_ARTIFACTS = (
    (9865061266, "task554-grade1-v3-prepare-33677346616-1", 204360988,
     "sha256:da8bfec6a03cac65de40ba8c4f79cde687fd2629edb3c3965fd972ecf96cc2f4"),
    (9865238399, "task554-grade1-v3-state-block-0-33677346616-1", 81729645,
     "sha256:2a8e63a4270bf4052c7fd8763d7828fc17dd6b94c88854bacde1e94082cd5838"),
    (9865242284, "task554-grade1-v3-state-block-1-33677346616-1", 82259824,
     "sha256:849321b79f0e3ea3c9a3f9c9dad43de2b3aaa571163456abc702476e322714fb"),
    (9865193269, "task554-grade1-v3-state-block-2-33677346616-1", 82200189,
     "sha256:d2cdf8245d58a384bebfd516135e07930fe26c21c2c1cab130dfa6c3c7f2854d"),
    (9865239848, "task554-grade1-v3-state-block-3-33677346616-1", 82266526,
     "sha256:87547101ede2fb48619a069de958c08cbb3cb0ee6c0990090234005aacd05b92"),
)
PACK_ENCODING = "base3-four-trits-per-byte"
OLD_BLOB_PINS = (
    (
        {"file": "old-0-lower-basis.46beeda1dfca7a228eafc9fbf030eb3ccd87c5009c380bae39efa4d17dda7837.bin",
         "bytes": 764570, "sha256": "46beeda1dfca7a228eafc9fbf030eb3ccd87c5009c380bae39efa4d17dda7837",
         "rows": 505, "width": 6056, "encoding": PACK_ENCODING},
        {"file": "old-0-lifted-grade.08632b4f3c0a8b0163926d48b406a58417038e427c902da56391c57963b4ab2b.bin",
         "bytes": 9162720, "sha256": "08632b4f3c0a8b0163926d48b406a58417038e427c902da56391c57963b4ab2b",
         "rows": 505, "width": 72576, "encoding": PACK_ENCODING},
    ),
    (
        {"file": "old-1-lower-basis.8a37de95859793ef3c8321d18de09590c28ec5adbc9025e70f819426a8d89333.bin",
         "bytes": 761542, "sha256": "8a37de95859793ef3c8321d18de09590c28ec5adbc9025e70f819426a8d89333",
         "rows": 503, "width": 6056, "encoding": PACK_ENCODING},
        {"file": "old-1-lifted-grade.14ea8ee3833f11250d18beac102b3e8b8d759ca13e0f8230069ece5f395cf364.bin",
         "bytes": 9126432, "sha256": "14ea8ee3833f11250d18beac102b3e8b8d759ca13e0f8230069ece5f395cf364",
         "rows": 503, "width": 72576, "encoding": PACK_ENCODING},
    ),
    (
        {"file": "old-2-lower-basis.ee6ee8c731be47024b9f6656a31100139ddc4ca685c568427d8fe90b172a60b4.bin",
         "bytes": 761542, "sha256": "ee6ee8c731be47024b9f6656a31100139ddc4ca685c568427d8fe90b172a60b4",
         "rows": 503, "width": 6056, "encoding": PACK_ENCODING},
        {"file": "old-2-lifted-grade.0609799f1bf4ba0fd534592c71ed22bee9c69b558930a4eddd745adf386076c4.bin",
         "bytes": 9126432, "sha256": "0609799f1bf4ba0fd534592c71ed22bee9c69b558930a4eddd745adf386076c4",
         "rows": 503, "width": 72576, "encoding": PACK_ENCODING},
    ),
    (
        {"file": "old-3-lower-basis.3b9be2ac16be5a4394c164f759a6e4414b65c597ee77d42830e33aeaa5fb0b48.bin",
         "bytes": 761542, "sha256": "3b9be2ac16be5a4394c164f759a6e4414b65c597ee77d42830e33aeaa5fb0b48",
         "rows": 503, "width": 6056, "encoding": PACK_ENCODING},
        {"file": "old-3-lifted-grade.7a3f436f4f2e324f0784f40efb975c31a24d845c350b0819f61b727aead3bec5.bin",
         "bytes": 9126432, "sha256": "7a3f436f4f2e324f0784f40efb975c31a24d845c350b0819f61b727aead3bec5",
         "rows": 503, "width": 72576, "encoding": PACK_ENCODING},
    ),
)
NEW_BLOB_PINS = (
    {"file": "block-0-basis.cc7e38114afc58e3aba10fa340a6ebd4f9a7a4752d5bb5fb9408ea8d84021e39.bin",
     "bytes": 6844824, "sha256": "cc7e38114afc58e3aba10fa340a6ebd4f9a7a4752d5bb5fb9408ea8d84021e39",
     "rows": 1509, "width": 18144, "encoding": PACK_ENCODING},
    {"file": "block-1-basis.0223f72b7d2cb8a72f2ff99b8812fea977ed761c8505dab52ad3fba284b93461.bin",
     "bytes": 6858432, "sha256": "0223f72b7d2cb8a72f2ff99b8812fea977ed761c8505dab52ad3fba284b93461",
     "rows": 1512, "width": 18144, "encoding": PACK_ENCODING},
    {"file": "block-2-basis.602f23081aa609973860eac24d2f65104a9530c8ddf356d60a9d0378921b99f6.bin",
     "bytes": 6858432, "sha256": "602f23081aa609973860eac24d2f65104a9530c8ddf356d60a9d0378921b99f6",
     "rows": 1512, "width": 18144, "encoding": PACK_ENCODING},
    {"file": "block-3-basis.4ed4de15c00290f60e5fd2d57dd94db3103be92c602d92481f2835d9d96db0b9.bin",
     "bytes": 6858432, "sha256": "4ed4de15c00290f60e5fd2d57dd94db3103be92c602d92481f2835d9d96db0b9",
     "rows": 1512, "width": 18144, "encoding": PACK_ENCODING},
)
LOWER_BLOB_BYTES = 67011332
LOWER_BLOB_PIN_SHA256 = hashlib.sha256((json.dumps(
    {"old": OLD_BLOB_PINS, "new": NEW_BLOB_PINS}, sort_keys=True,
    separators=(",", ":"), ensure_ascii=True) + "\n").encode("ascii")).hexdigest()
SEED2_RAW_PACKED_SHA256 = "e67d0a0b21aaf41fd1617811b45cd51191a0087c7d04fcc33dda5a58f4fcfca6"
SEED2_PROJECTED_PACKED_SHA256 = "7f151eec27ff74d68b13759ad3719913dcf26c3434274aa0e95868d5a4e45983"
SEED2_DIFFERENCE_PACKED_SHA256 = "f57b13d028ca786c3bab7c88dbef463a63f8558093c18c9c4b626d9f87c5ed60"
SEED2_P1_A0_SHA256 = (
    "a65a5bbf2467c28635d159752d41de9c503a85f8c2597bdead3e27f13b767e5f",
    "e9932ae482477843988c591fb44cad9640d85240a132eb8ee0b6032873eca8fb",
    "0c8e4fe89b60fa9d48a07297ddcbc7e4b71a907e12d1d8386cc870d3d89911b2",
    "09b391d1f2098bf581748225a418c200aa2cd2d8cfbe7b6ea40cac5cbfea9d42",
)
SEED2_REDUCTION = ((2, 2), (505, 2), (1008, 2), (1511, 2))
TASK712_PARENT = {"run_id": 33814194630, "run_attempt": 1, "artifact_id": 9915928157,
                  "artifact_digest": "sha256:abedff074117bb779675021e9436c3a9973c577e247fe76a8314a2d4312ea858"}
EXPECTED_ROOT = {
    0: (2742, 3, 2, "af62027aa99fbd1a4b7b53c6b380b4e7fa7403915ea91f9d51d7cb2198c7e053"),
    1: (0, None, None, "8f23754a0b5b965d1b0e2e5a9b043586911a3f8283a36412c739dad14c500838"),
    2: (0, None, None, "8f23754a0b5b965d1b0e2e5a9b043586911a3f8283a36412c739dad14c500838"),
    3: (0, None, None, "8f23754a0b5b965d1b0e2e5a9b043586911a3f8283a36412c739dad14c500838"),
}
EXPECTED_CHILD = {
    0: ("aa54bbed30791f3f771c5fb8d74e38329564101cbcd805db20e1e232595e7033",
        "1b98282910ed00d253cad00cbc389b9c85c6b84be9b8da0418ece4f8b0218cd8",
        "f98650b321a16e846539698d98710a544fd1953656afcaecbee995523f0def2b",
        "2245611c3efcef71758e281950ca4b23ba96d0991880cdb92ecafa0fac7aa8b4"),
    1: ("8f23754a0b5b965d1b0e2e5a9b043586911a3f8283a36412c739dad14c500838",) * 4,
    2: ("8f23754a0b5b965d1b0e2e5a9b043586911a3f8283a36412c739dad14c500838",) * 4,
    3: ("8f23754a0b5b965d1b0e2e5a9b043586911a3f8283a36412c739dad14c500838",) * 4,
}


def require(condition: bool, reason: str) -> None:
    if not condition:
        raise RuntimeError(reason)


def plain_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def sealed_object(value: Any) -> bool:
    if not isinstance(value, dict) or not isinstance(value.get("sha256"), str):
        return False
    body = dict(value); seal = body.pop("sha256")
    return seal == sha(canonical(body))


def canonical(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"),
                       ensure_ascii=True) + "\n").encode("ascii")


def safe_path(root: Path, name: str) -> Path:
    require(isinstance(name, str) and name and not Path(name).is_absolute(), "relative_path")
    path = (root / name).resolve(); require(root.resolve() in path.parents, "path_escape")
    require(not path.is_symlink() and path.is_file(), "unsafe_file")
    return path


def file_hash(path: Path, expected: int | None = None, cap: int = 1 << 30) -> tuple[int, str]:
    size = path.stat().st_size; require(size <= cap, "file_cap")
    if expected is not None: require(size == expected, "file_size")
    h = hashlib.sha256(); total = 0
    with path.open("rb") as stream:
        while True:
            block = stream.read(1 << 20)
            if not block: break
            h.update(block); total += len(block)
    require(total == size, "file_read_size"); return size, h.hexdigest()


def read_json(path: Path, expected_size: int | None = None,
              expected_hash: str | None = None, cap: int = 1 << 28) -> tuple[Any, bytes]:
    size, actual = file_hash(path, expected_size, cap); raw = path.read_bytes()
    require(len(raw) == size and (expected_hash is None or actual == expected_hash), "json_digest")
    value = json.loads(raw.decode("ascii")); require(canonical(value) == raw, "json_canonical")
    return value, raw


def read_json_stream(path: Path, expected_size: int, expected_hash: str,
                     cap: int = 1 << 28) -> Any:
    """Authenticate a large fixed body without a duplicate raw-byte copy."""
    size, actual = file_hash(path, expected_size, cap)
    require(size == expected_size and actual == expected_hash, "checker_json_stream_digest")
    try:
        with path.open("rb") as stream:
            value = json.load(stream)
    except (OSError, UnicodeError, ValueError) as exc:
        raise RuntimeError("checker_json_stream_decode") from exc
    require(isinstance(value, dict), "checker_json_stream_object")
    return value


def receipt(root: Path, item: dict[str, Any], cap: int = 1 << 30) -> bytes:
    require(isinstance(item, dict) and set(item) == {"file", "bytes", "sha256"}, "receipt_shape")
    path = safe_path(root, item["file"]); size, actual = file_hash(path, item["bytes"], cap)
    require(actual == item["sha256"], "receipt_digest"); return path.read_bytes()


def verify_source() -> None:
    _, actual = file_hash(ARITH_PATH); require(actual == ARITH_SHA256, "checker_source_pin")


def sparse_projection(packed: bytes, offset: int, entries: Iterable[tuple[int, int]]) -> int:
    total = 0
    for index, coefficient in entries:
        require(0 <= index < SOURCE_WIDTH and coefficient in (1, 2), "sparse_entry")
        total += coefficient * ((packed[offset + index // 4] // POW3[index % 4]) % 3)
    return total % 3


def check_table_transpose(forward: Iterable[Iterable[int]],
                          adjoint: Iterable[Iterable[int]]) -> None:
    """Independent table-level transpose check used after envelope parsing."""
    expected = sorted((int(destination), int(source), int(coefficient))
                      for source, destination, coefficient in forward)
    require(list(adjoint) == expected, "checker_task712_transpose")


def vectorized_projection_chunk(packed_rows: np.ndarray, byte_offset: int,
                                projections: list[tuple[np.ndarray, np.ndarray, np.ndarray]]) -> np.ndarray:
    """Independent bounded implementation of the sparse packed projection."""
    rows = np.asarray(packed_rows, dtype=np.uint8)
    require(rows.ndim == 2 and rows.shape[1] == P1_ROW_BYTES and
            0 <= byte_offset <= P1_ROW_BYTES - SLICE_BYTES, "checker_projection_chunk_shape")
    result = np.zeros((rows.shape[0], len(projections)), dtype=np.uint8)
    for slot, (byte_index, digit_slot, coefficient) in enumerate(projections):
        if not len(byte_index):
            continue
        selected = rows[:, byte_offset + byte_index]
        powers = np.asarray([POW3[i] for i in digit_slot], dtype=np.uint8)
        digits = (selected // powers) % 3
        result[:, slot] = (np.sum(digits.astype(np.uint32) * coefficient,
                                  axis=1, dtype=np.uint32) % 3).astype(np.uint8)
    return result


def checker_source_context() -> tuple[Any, dict[str, Any]]:
    words = ARITH._load_words()
    return ARITH._CheckerSeedContext(words), words


def checker_raw_seed_direct(context: Any, words: dict[str, Any], q: np.ndarray,
                            character: int, *, actual_pin: bool = False) -> dict[str, Any]:
    """Independently derive v541 (2.1), never calling the old projector API."""
    vector = np.asarray(q, dtype=np.uint8).reshape(-1)
    require(vector.size == SOURCE_WIDTH and not np.any(vector > 2) and
            plain_int(character) and 0 <= character < 4,
            "checker_raw_seed_shape")
    values: list[int] = []
    row_hashes: list[str] = []
    supports: list[int] = []
    combined = hashlib.sha256()
    for seed_index, relator in enumerate(words["relators"]):
        full = ARITH._checker_seed_evaluate_seed(
            context, tuple(int(letter) for letter in relator))
        row = full[2][character].copy()
        packed = ARITH.pack_trits(row)
        combined.update(packed)
        row_hashes.append(sha(packed))
        supports.append(int(np.count_nonzero(row)))
        values.append(ARITH.dot_mod3(row, vector))
    require(len(values) == 44, "checker_raw_seed_eof")
    if actual_pin:
        require(character == 0 and row_hashes[2] == SEED2_RAW_PACKED_SHA256 and
                supports[2] == 568 and values[2] == 0,
                "checker_actual_seed2_raw")
    direct_raw = bytes(values)
    body = {
        "schema": SCHEMA + ".raw-seed-direct.v541",
        "formula_id": V541_FORMULA_ID,
        "character": character,
        "q_packed_sha256": sha(ARITH.pack_trits(vector)),
        "row_count": 44,
        "row_trits": SOURCE_WIDTH,
        "row_packed_bytes": SLICE_BYTES,
        "raw_row_packed_sha256": row_hashes,
        "raw_row_support": supports,
        "raw_rows_packed_sha256": combined.hexdigest(),
        "raw_direct_values_sha256": sha(direct_raw),
    }
    return {"values": values,
            "receipt": {**body, "sha256": sha(canonical(body))}}


def checker_actor_tags(context: Any, actor: int) -> tuple[Any, ...]:
    require(actor in ACTORS, "checker_actor_tag_letter")
    output = []
    for pair in ARITH.SEED_OO:
        word = ARITH._checker_seed_substitute((actor,), *pair)
        output.append(ARITH._checker_seed_affine_eval(word, context.images))
    return tuple(output)


def _checker_polynomial_pull(factor: np.ndarray, q_rows: np.ndarray,
                             alpha_indices: tuple[int, ...]) -> np.ndarray:
    require(factor.shape == (10,) and q_rows.shape == (6, 504),
            "checker_polynomial_pull_shape")
    pulled = np.zeros((len(alpha_indices), 504), dtype=np.uint8)
    nonzero = [int(index) for index in np.flatnonzero(factor)]
    for row_index, alpha in enumerate(alpha_indices):
        total = np.zeros(504, dtype=np.uint16)
        for gamma in nonzero:
            beta = ARITH.SEED_DEGREE2_PRODUCT[gamma][alpha]
            if 4 <= beta <= 9:
                total += int(factor[gamma]) * q_rows[beta - 4].astype(np.uint16)
        pulled[row_index] = np.asarray(total % 3, dtype=np.uint8)
    return pulled


def checker_actor_adjoint(context: Any, q: np.ndarray, character: int,
                          actor: int) -> tuple[np.ndarray, np.ndarray]:
    vector = np.asarray(q, dtype=np.uint8).reshape(-1)
    require(vector.size == SOURCE_WIDTH and not np.any(vector > 2) and
            plain_int(character) and 0 <= character < 4 and actor in ACTORS,
            "checker_actor_adjoint_shape")
    lower0 = np.zeros((4, SOURCE0C), dtype=np.uint8)
    lower1 = np.zeros((4, SOURCE1C), dtype=np.uint8)
    top = np.zeros(SOURCE_WIDTH, dtype=np.uint8)
    label_a = CHARACTERS[character]
    for tag, affine in enumerate(checker_actor_tags(context, actor)):
        translate = context.pmap(affine[0])
        shift = (affine[1], affine[2])
        transported_a = context.transport[tag][label_a]
        for component in range(2):
            q_start = ((tag * 2 + component) * 6) * 504
            translated_q = vector[q_start:q_start + 3024].reshape(6, 504)[:, translate]
            for parity in CHARACTERS:
                factor = ARITH._checker_seed_e_poly(
                    ARITH._checker_seed_sign_kernel(parity, affine[3]))
                low_pull = _checker_polynomial_pull(factor, translated_q,
                                                    (0, 1, 2, 3))
                high_pull = _checker_polynomial_pull(
                    factor, translated_q, (4, 5, 6, 7, 8, 9))
                out_parity = (parity[0] ^ shift[0], parity[1] ^ shift[1])
                out_sign = ARITH._checker_seed_cv(transported_a, out_parity)
                for source_index, source_label in enumerate(CHARACTERS):
                    in_sign = ARITH._checker_seed_cv(
                        context.transport[tag][source_label], parity)
                    coefficient = (out_sign * in_sign) % 3
                    begin0 = ARITH._checker_seed_lower_coord(tag, component, 0)
                    lower0[source_index, begin0:begin0 + 504] = np.asarray(
                        (lower0[source_index, begin0:begin0 + 504].astype(np.uint16) +
                         coefficient * low_pull[0].astype(np.uint16)) % 3,
                        dtype=np.uint8)
                    for monomial in range(3):
                        begin1 = ARITH._checker_seed_grade1_coord(
                            tag, component, monomial, 0)
                        lower1[source_index, begin1:begin1 + 504] = np.asarray(
                            (lower1[source_index, begin1:begin1 + 504].astype(np.uint16) +
                             coefficient * low_pull[monomial + 1].astype(np.uint16)) % 3,
                            dtype=np.uint8)
                    if source_index == character:
                        for monomial in range(6):
                            begin2 = ((tag * 2 + component) * 6 + monomial) * 504
                            top[begin2:begin2 + 504] = np.asarray(
                                (top[begin2:begin2 + 504].astype(np.uint16) +
                                 coefficient * high_pull[monomial].astype(np.uint16)) % 3,
                                dtype=np.uint8)
    lower = np.concatenate((lower0.reshape(-1), lower1.reshape(-1),
                            np.zeros(8, dtype=np.uint8)))
    require(lower.shape == (LOWER_WIDTH,) and top.shape == (SOURCE_WIDTH,),
            "checker_actor_adjoint_output")
    return lower, top


def checker_actor_adjoints(context: Any, q: np.ndarray, character: int,
                           homogeneous: list[np.ndarray]) -> tuple[list[np.ndarray], dict[str, Any]]:
    require(len(homogeneous) == 4, "checker_actor_child_count")
    covectors: list[np.ndarray] = []
    covector_rows: list[dict[str, Any]] = []
    top_hashes: list[str] = []
    for slot in range(4):
        actor = ACTORS[slot]
        lower, top = checker_actor_adjoint(context, q, character, actor)
        require(np.array_equal(top, np.asarray(homogeneous[slot], dtype=np.uint8)),
                "checker_task712_top_adjoint")
        packed = ARITH.pack_trits(lower)
        covectors.append(lower)
        covector_rows.append({"actor": actor, "trits": LOWER_WIDTH,
                              "packed_bytes": LOWER_PACKED_BYTES,
                              "support": int(np.count_nonzero(lower)),
                              "packed_sha256": sha(packed)})
        top_hashes.append(sha(ARITH.pack_trits(top)))
    body = {"schema": SCHEMA + ".actor-lower-covectors.v541",
            "formula_id": V541_FORMULA_ID, "character": character,
            "actor_order": list(ACTORS), "auxiliary_entries_zero": True,
            "covectors": covector_rows,
            "task712_top_adjoint_packed_sha256": top_hashes,
            "task712_pure_top_match": True}
    return covectors, {**body, "sha256": sha(canonical(body))}


def _checker_blob_file_receipt(value: dict[str, Any]) -> dict[str, Any]:
    return {key: value[key] for key in ("file", "bytes", "sha256")}


def _checker_blob_descriptor(value: Any, expected: dict[str, Any],
                             reason: str) -> None:
    require(isinstance(value, dict) and set(value) ==
            {"file", "bytes", "sha256", "rows", "width", "encoding"} and
            value == expected and value["encoding"] == PACK_ENCODING and
            value["width"] % 4 == 0 and
            value["bytes"] == value["rows"] * (value["width"] // 4) and
            value["file"].endswith("." + value["sha256"] + ".bin"), reason)


_CHECKER_PACKED_DOT = np.empty((81, 81), dtype=np.uint8)
for _checker_left in range(81):
    for _checker_right in range(81):
        _digits_left = [(_checker_left // (3 ** index)) % 3 for index in range(4)]
        _digits_right = [(_checker_right // (3 ** index)) % 3 for index in range(4)]
        _CHECKER_PACKED_DOT[_checker_left, _checker_right] = sum(
            x * y for x, y in zip(_digits_left, _digits_right)) % 3


def checker_stream_dots(root: Path, descriptor: dict[str, Any],
                        covectors: list[np.ndarray], *, body_sha256: str,
                        role: str) -> tuple[np.ndarray, dict[str, Any]]:
    width = int(descriptor["width"]); count = int(descriptor["rows"])
    require(width > 0 and width % 4 == 0 and count >= 0 and covectors,
            "checker_stream_dimensions")
    packed_vectors: list[np.ndarray] = []
    for covector in covectors:
        dense = np.asarray(covector, dtype=np.uint8).reshape(-1)
        require(dense.size == width and not np.any(dense > 2),
                "checker_stream_covector")
        encoded = np.frombuffer(ARITH.pack_trits(dense), dtype=np.uint8)
        require(encoded.size == width // 4 and not np.any(encoded > 80),
                "checker_stream_covector_packed")
        packed_vectors.append(encoded)
    path = safe_path(root, descriptor["file"])
    row_bytes = width // 4
    batch = max(1, min(193, (7 << 20) // max(row_bytes, 1)))
    answer = np.zeros((count, len(covectors)), dtype=np.uint8)
    digest_state = hashlib.sha256(); cursor = 0; byte_count = 0
    with path.open("rb") as stream:
        while cursor != count:
            take = min(batch, count - cursor)
            block = stream.read(take * row_bytes)
            require(len(block) == take * row_bytes, "checker_stream_eof")
            digest_state.update(block); byte_count += len(block)
            packed_rows = np.frombuffer(block, dtype=np.uint8).reshape(take, row_bytes)
            require(not np.any(packed_rows > 80), "checker_stream_invalid_byte")
            for column, packed_vector in enumerate(packed_vectors):
                partial = _CHECKER_PACKED_DOT[packed_rows, packed_vector]
                answer[cursor:cursor + take, column] = np.asarray(
                    np.sum(partial, axis=1, dtype=np.uint32) % 3,
                    dtype=np.uint8)
            cursor += take
        require(stream.read(1) == b"", "checker_stream_trailing")
    require(byte_count == descriptor["bytes"] and
            digest_state.hexdigest() == descriptor["sha256"],
            "checker_stream_receipt")
    return answer, {"role": role, "task554_body_sha256": body_sha256,
                    "descriptor": descriptor, "padding_trits": 0}


def checker_old_slices(covectors: list[np.ndarray], character: int) -> tuple[list[np.ndarray], list[np.ndarray]]:
    lower_slices: list[np.ndarray] = []
    grade_slices: list[np.ndarray] = []
    for item in covectors:
        flat = np.asarray(item, dtype=np.uint8).reshape(-1)
        require(flat.size == LOWER_WIDTH, "checker_old_slice_width")
        d0 = flat[:4 * SOURCE0C].reshape(4, SOURCE0C)
        d1 = flat[4 * SOURCE0C:4 * SOURCE0C + 4 * SOURCE1C]
        lower_slices.append(np.concatenate((d0[character], flat[-8:])))
        grade_slices.append(d1.copy())
    return lower_slices, grade_slices


def checker_new_slices(covectors: list[np.ndarray], character: int) -> list[np.ndarray]:
    begin = 4 * SOURCE0C + character * SOURCE1C
    answer = []
    for item in covectors:
        flat = np.asarray(item, dtype=np.uint8).reshape(-1)
        require(flat.size == LOWER_WIDTH, "checker_new_slice_width")
        answer.append(flat[begin:begin + SOURCE1C].copy())
    return answer


def relation_source_sha256() -> str:
    """Digest the fixed coefficient source without serializing every term."""
    old_offsets = [0]
    for rank in OLD_RANKS[:-1]:
        old_offsets.append(old_offsets[-1] + rank)
    new_offsets = [sum(OLD_RANKS)]
    for rank in NEW_RANKS[:-1]:
        new_offsets.append(new_offsets[-1] + rank)
    return sha(canonical({
        "schema": SCHEMA + ".relation-stream", "body_sha256": list(TASK554_BODY_DIGESTS),
        "old_ranks": list(OLD_RANKS), "new_ranks": list(NEW_RANKS),
        "old_offsets": old_offsets, "new_offsets": new_offsets,
        "actor_order": list(ACTORS), "seed_count": 44,
        "origin_count": TASK554_ORIGINS, "relation_count": SCALAR_ORIGINS,
        "evaluator_version": "filtered-direct-blockwise-scalar-v2",
        "formula_id": V541_FORMULA_ID,
        "lower_blob_pin_sha256": LOWER_BLOB_PIN_SHA256,
        "source_pin": "task554-v3-body-and-lower-blob-pins"}))


def _expr(value: Any, bound: int, reason: str) -> None:
    require(isinstance(value, list), reason + ":list"); seen: set[int] = set()
    for pair in value:
        require(isinstance(pair, list) and len(pair) == 2 and plain_int(pair[0]) and
                plain_int(pair[1]) and 0 <= pair[0] < bound and pair[1] in (1, 2),
                reason + ":entry")
        require(pair[0] not in seen, reason + ":duplicate")
        seen.add(pair[0])


def _body(value: Any, index: int) -> None:
    require(isinstance(value, dict), "checker_task554_body")
    if index == -1:
        olds = value.get("old_blocks"); origins = value.get("defect_origins")
        require(isinstance(olds, list) and len(olds) == 4 and isinstance(origins, list) and
                len(origins) == TASK554_ORIGINS and isinstance(value.get("packets"), list) and
                len(value["packets"]) == 4, "checker_prepare_shape")
        cursor = 0
        for character, old in enumerate(olds):
            rank = OLD_RANKS[character]; record = old.get("record")
            require(old.get("character_index") == character and
                    old.get("character") == list(CHARACTERS[character]) and old.get("rank") == rank and
                    isinstance(record, dict) and record.get("character") == list(CHARACTERS[character]) and
                    record.get("rank") == rank and record.get("attempts") == 44 + 4 * rank and
                    record.get("actor_order") == list(ACTORS) and record.get("queue_exhausted") is True and
                    len(record.get("seed_reductions", [])) == 44 and len(record.get("dag_nodes", [])) == rank and
                    len(record.get("actor_transitions", [])) == rank, "checker_old_shape")
            for expression in record["seed_reductions"]: _expr(expression, rank, "checker_seed")
            for row in record["actor_transitions"]:
                require(isinstance(row, list) and len(row) == 4, "checker_old_actor")
                for expression in row: _expr(expression, rank, "checker_actor")
            for pivot, node in enumerate(record["dag_nodes"]):
                require(node.get("pivot") == pivot and node.get("scale") in (1, 2), "checker_old_node")
                _expr(node.get("reductions"), rank, "checker_old_reduction")
            require(old.get("defect_origin_range") == list(ORIGIN_RANGES[character]) and
                    ORIGIN_RANGES[character][0] == cursor, "checker_origin_range")
            cursor += 44 + 4 * rank
        require(cursor == len(origins), "checker_origin_count")
    else:
        rank = NEW_RANKS[index]
        require(value.get("phase") == "block" and value.get("character_index") == index and
                value.get("character") == list(CHARACTERS[index]) and value.get("rank") == rank and
                value.get("origin_count") == TASK554_ORIGINS and value.get("attempts") == TASK554_ORIGINS + 4 * rank and
                value.get("actor_order") == list(ACTORS) and value.get("queue_exhausted") is True,
                "checker_new_metadata")
        reductions = value.get("origin_reductions"); transitions = value.get("actor_transitions")
        nodes = value.get("dag_nodes"); leads = value.get("pivot_leads")
        require(isinstance(reductions, list) and len(reductions) == TASK554_ORIGINS and
                isinstance(transitions, list) and len(transitions) == rank and
                isinstance(nodes, list) and len(nodes) == rank and isinstance(leads, list) and
                len(leads) == rank and len(set(leads)) == rank, "checker_new_lists")
        for expression in reductions: _expr(expression, rank, "checker_origin_reduction")
        for row in transitions:
            require(isinstance(row, list) and len(row) == 4, "checker_new_actor")
            for expression in row: _expr(expression, rank, "checker_transition")
        for pivot, node in enumerate(nodes):
            require(node.get("pivot") == pivot and node.get("lead") == leads[pivot] and
                    node.get("scale") in (1, 2), "checker_new_node")
            _expr(node.get("reductions"), rank, "checker_new_reduction")
        require(value.get("dag_sha256") == sha(canonical(nodes)), "checker_dag_digest")


def state_descriptor(value: Any, index: int) -> dict[str, Any]:
    require(isinstance(value, dict) and set(value) == {"root", "head", "body", "files"},
            "checker_state_descriptor")
    root = Path(value["root"]).absolute(); require(root.is_dir(), "checker_state_root")
    stem = "prepare" if index == -1 else "block-" + str(index)
    body_hash = TASK554_BODY_DIGESTS[0 if index == -1 else index + 1]
    head = value["head"]; body = value["body"]
    require(head == {"file": stem + ".HEAD", "bytes": head["bytes"], "sha256": head["sha256"]} and
            body["file"] == stem + "." + body_hash + ".json" and body["sha256"] == body_hash and
            isinstance(value["files"], list), "checker_body_receipt")
    hvalue, _ = read_json(safe_path(root, head["file"]), head["bytes"], head["sha256"], 1 << 20)
    bpath = safe_path(root, body["file"])
    bvalue = read_json_stream(bpath, body["bytes"], body["sha256"], 1 << 28)
    require(hvalue == {
        "body_sha256": body_hash, "parent_sha256": None if index == -1 else TASK554_BODY_DIGESTS[0],
        "schema": "d972.r07.a0.first-rung-grade1.v3.state.head", "stem": stem},
        "checker_head_join")
    require(bvalue.get("schema") == "d972.r07.a0.first-rung-grade1.v3.state" and
            bvalue.get("phase") == ("prepare" if index == -1 else "block") and
            bvalue.get("parent_sha256") == (None if index == -1 else TASK554_BODY_DIGESTS[0]),
            "checker_body_join")
    _body(bvalue, index)
    descriptors = []
    if index == -1:
        for character, old in enumerate(bvalue["old_blocks"]):
            for slot, key in enumerate(("lower_basis_blob", "lifted_grade_blob")):
                descriptor = old.get(key)
                _checker_blob_descriptor(descriptor, OLD_BLOB_PINS[character][slot],
                                         "checker_old_blob_descriptor")
                descriptors.append(descriptor)
    else:
        descriptor = bvalue.get("basis_blob")
        _checker_blob_descriptor(descriptor, NEW_BLOB_PINS[index],
                                 "checker_new_blob_descriptor")
        descriptors.append(descriptor)
    require(value["files"] == [head, body] +
            [_checker_blob_file_receipt(item) for item in descriptors],
            "checker_body_lower_roster")
    return {"root": root, "body": bvalue, "body_sha256": body_hash}


def validate_task554(value: Any) -> dict[str, Any]:
    require(isinstance(value, dict) and set(value) ==
            {"schema", "source_run", "source_attempt", "source_head", "artifacts", "prepare", "blocks"} and
            value["schema"] == SCHEMA + ".task554-parent.v1" and value["source_run"] == TASK554_RUN and
            value["source_attempt"] == TASK554_ATTEMPT and value["source_head"] == TASK554_HEAD and
            value["artifacts"] == [{"id": x[0], "name": x[1], "bytes": x[2], "sha256": x[3]}
                                    for x in TASK554_ARTIFACTS] and len(value["blocks"]) == 4,
            "checker_task554_parent")
    for item in [value["prepare"], *value["blocks"]]:
        require(isinstance(item, dict) and set(item) == {"root", "head", "body", "files"},
                "checker_task554_descriptor")
    return value


def validate_p1(value: Any) -> dict[str, Any]:
    require(isinstance(value, dict) and set(value) ==
            {"root", "manifest", "files", "run", "attempt", "head", "artifact", "artifact_name",
             "archive_bytes", "archive_sha256"} and value["run"] == P1_RUN and
            value["attempt"] == P1_ATTEMPT and value["head"] == P1_HEAD and
            value["artifact"] == P1_ARTIFACT and value["artifact_name"] == P1_ARTIFACT_NAME and
            value["archive_bytes"] == P1_ARCHIVE_BYTES and value["archive_sha256"] == P1_ARCHIVE_SHA256,
            "checker_p1_parent")
    root = Path(value["root"]).absolute(); require(root.is_dir(), "checker_p1_root")
    manifest, raw = read_json(safe_path(root, value["manifest"]["file"]), P1_MANIFEST_BYTES,
                              P1_MANIFEST_SHA256, 1 << 20)
    require(value["manifest"] == {"file": "manifest.json", "bytes": P1_MANIFEST_BYTES,
                                   "sha256": P1_MANIFEST_SHA256} and
            manifest.get("schema") == "d972.r07.canonical-p1-dag-degree2-lift.v8" and
            manifest.get("status") == "CANONICAL_P1_DAG_DEGREE2_LIFT_CANDIDATE" and
            manifest.get("rows") == P1_ROWS and manifest.get("row_trits") == P1_ROW_TRITS and
            manifest.get("row_bytes") == P1_ROW_BYTES and
            manifest.get("global_order") == [0, 505, 1008, 1511, 2014, 3523, 5035, 6547, 8059] and
            manifest.get("actor_order") == list(ACTORS) and
            manifest.get("character_order") == [list(x) for x in CHARACTERS] and
            manifest.get("independent_checker") is False and
            all(manifest.get(k) is False for k in ("A0", "COMMON", "COFINAL", "FAKE", "IHARA", "verified")),
            "checker_p1_manifest")
    cache = manifest.get("cache"); instruction = manifest.get("instruction")
    require(cache == {"path": "degree2.cache.bin", "rows": P1_ROWS, "bytes": P1_CACHE_BYTES,
                      "sha256": P1_CACHE_SHA256, "final_lf": False, "eof": True} and
            instruction == {"path": "instructions.jsonl", "rows": P1_ROWS, "bytes": P1_INSTRUCTION_BYTES,
                            "sha256": P1_INSTRUCTION_SHA256, "final_lf": True, "eof": True,
                            "final_head": manifest.get("ancestry_sha256")} and
            value["files"] == [{"file": "degree2.cache.bin", "bytes": P1_CACHE_BYTES,
                                 "sha256": P1_CACHE_SHA256},
                                {"file": "instructions.jsonl", "bytes": P1_INSTRUCTION_BYTES,
                                 "sha256": P1_INSTRUCTION_SHA256}],
            "checker_p1_receipts")
    require({p.name for p in root.iterdir()} == {"manifest.json", "degree2.cache.bin", "instructions.jsonl"},
            "checker_p1_roster")
    return {"root": root, "manifest": manifest, "manifest_sha256": sha(raw),
            "cache": cache, "instruction": instruction}


def validate_separator(value: Any) -> dict[str, Any]:
    require(isinstance(value, dict) and set(value) ==
            {"schema", "root", "artifact", "manifest", "physical", "lambda", "internal"} and
            value["schema"] == SCHEMA + ".separator-parent.v1" and value["artifact"] == {
                "run": SEPARATOR_RUN, "attempt": SEPARATOR_ATTEMPT, "head": SEPARATOR_HEAD,
                "id": SEPARATOR_ARTIFACT, "name": SEPARATOR_ARTIFACT_NAME,
                "bytes": SEPARATOR_ARCHIVE_BYTES, "sha256": SEPARATOR_ARCHIVE_SHA256},
            "checker_separator_identity")
    root = Path(value["root"]).absolute(); require(root.is_dir(), "checker_separator_root")
    manifest, raw = read_json(safe_path(root, value["manifest"]["file"]), None,
                              SEPARATOR_MANIFEST_SHA256, 1 << 20)
    require(value["manifest"]["sha256"] == SEPARATOR_MANIFEST_SHA256 and
            manifest.get("generation") == SEPARATOR_GENERATION and manifest.get("rank") == SEPARATOR_RANK and
            manifest.get("instructions", {}).get("final_head") == SEPARATOR_STATE_HEAD and
            manifest.get("candidate_roster") == ["physical.bin", "physical-p1-coeff.bin",
                                                   "instructions.jsonl", "manifest.json", "HEAD"],
            "checker_separator_manifest")
    lam_raw = receipt(root, value["lambda"], PHYSICAL_PACKED_BYTES)
    require(sha(lam_raw) == SEPARATOR_LAMBDA_SHA256, "checker_separator_lambda")
    lam = ARITH.unpack_trits(lam_raw, PHYSICAL_WIDTH); physical = value["physical"]
    require(physical == {"file": "state/physical.bin", "bytes": SEPARATOR_PHYSICAL_BYTES,
                         "sha256": SEPARATOR_PHYSICAL_SHA256, "rows": SEPARATOR_RANK},
            "checker_physical_receipt")
    path = safe_path(root, physical["file"]); h = hashlib.sha256()
    with path.open("rb") as stream:
        for _ in range(SEPARATOR_RANK):
            packed = stream.read(PHYSICAL_PACKED_BYTES)
            require(len(packed) == PHYSICAL_PACKED_BYTES, "checker_physical_eof")
            row = ARITH.unpack_trits(packed, PHYSICAL_WIDTH)
            require(ARITH.dot_mod3(lam, row) == 0, "checker_separator_dot"); h.update(packed)
        require(stream.read(1) == b"", "checker_physical_trailing")
    require(h.hexdigest() == SEPARATOR_PHYSICAL_SHA256, "checker_physical_digest")
    for item, wanted in ((value["internal"]["terminal"], SEPARATOR_TERMINAL_SHA256),
                         (value["internal"]["result"], SEPARATOR_RESULT_SHA256),
                         (value["internal"]["checker"], SEPARATOR_CHECKER_SHA256)):
        require(sha(receipt(root, item, 1 << 24)) == wanted, "checker_internal_receipt")
    return {"root": root, "manifest": manifest, "manifest_sha256": sha(raw),
            "lambda": lam, "lambda_sha256": sha(lam_raw), "generation": SEPARATOR_GENERATION}


def validate_launch(path: Path) -> tuple[dict[str, Any], bytes]:
    launch, raw = read_json(path, cap=1 << 24)
    claims = launch_claims()
    require(isinstance(launch, dict) and set(launch) ==
            {"schema", "fixture_only", "mode", "characters", "actors", "p1_parent", "task554_parent",
             "task712_parents", "separator_parent", "out", "claims", "source_pin"} and
            launch["schema"] == SCHEMA + ".launch.v1" and launch["fixture_only"] is False and
            launch["mode"] == "actual" and launch["characters"] == [list(x) for x in CHARACTERS] and
            launch["actors"] == list(ACTORS) and launch["claims"] == claims,
            "checker_launch_shape")
    verify_source(); require(launch["source_pin"] == {
        "producer": {"path": PRODUCER_ARITH_PATH.as_posix(), "sha256": PRODUCER_ARITH_SHA256},
        "checker": {"path": ARITH_PATH.as_posix(), "sha256": ARITH_SHA256}},
                             "checker_launch_source")
    separator = validate_separator(launch["separator_parent"]); p1 = validate_p1(launch["p1_parent"])
    task554 = validate_task554(launch["task554_parent"])
    parents = launch["task712_parents"]
    require(isinstance(parents, list) and len(parents) == 4, "checker_task712_parent_list")
    for item in parents:
        require(set(item) == set(TASK712_PARENT) | {"root"} and
                {key: item[key] for key in TASK712_PARENT} == TASK712_PARENT, "checker_task712_pin")
    return ({"launch": launch, "launch_raw": raw, "launch_sha256": sha(raw),
             "separator": separator, "p1": p1, "task554": task554, "task712": parents}, raw)


def covectors(separator: dict[str, Any], parents: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[list[np.ndarray]]]:
    tables: list[dict[str, Any]] = []; vectors: list[list[np.ndarray]] = []
    for character in range(4):
        table = ARITH.read_task712_envelope(parents[character], character); tables.append(table)
        for key in ("B", *ACTORS):
            check_table_transpose(table["forward"][key], table["adjoint"][key])
        root = ARITH.sparse_adjoint(table["forward"]["B"], SOURCE_WIDTH, PHYSICAL_WIDTH,
                                    separator["lambda"])
        children = [ARITH.sparse_adjoint(table["forward"][actor], SOURCE_WIDTH, SOURCE_WIDTH, root)
                    for actor in ACTORS]
        vectors.append([root] + children)
        nz = np.flatnonzero(root); packed = ARITH.pack_trits(root)
        wanted = EXPECTED_ROOT[character]
        require((int(len(nz)), int(nz[0]) if len(nz) else None,
                 int(root[nz[0]]) if len(nz) else None, sha(packed)) == wanted, "checker_root_pin")
        for slot, child in enumerate(children):
            require(sha(ARITH.pack_trits(child)) == EXPECTED_CHILD[character][slot], "checker_child_pin")
    return tables, vectors


def _shift(expression: Any, bound: int, offset: int) -> list[list[int]]:
    _expr(expression, bound, "checker_relation_expression")
    return [[offset + int(i), int(c)] for i, c in expression]


def _subtract(accumulator: Any, expression: Any, values: np.ndarray, bound: int,
              offset: int, relation_hash: Any, label: dict[str, Any]) -> int:
    # state_descriptor already checked authenticated unique local terms and
    # coefficients; preserve source order without allocating a normalized copy.
    terms = expression; result = int(accumulator)
    for index, coefficient in terms:
        result = (result - int(coefficient) * int(values[offset + index])) % 3
    return result


def accumulate_scalars(parent: dict[str, Any], character: int, direct: list[int],
                       values: list[np.ndarray], lower_covectors: list[np.ndarray]) -> dict[str, Any]:
    """Checker-owned direct accumulator; no nested relation tree is retained."""
    prepare = state_descriptor(parent["prepare"], -1); olds = prepare["body"]["old_blocks"]
    old_offsets: list[int] = []; cursor = 0
    for rank in OLD_RANKS: old_offsets.append(cursor); cursor += rank
    new_offsets: list[int] = []; cursor = sum(OLD_RANKS)
    for rank in NEW_RANKS: new_offsets.append(cursor); cursor += rank
    require(cursor == P1_ROWS and len(direct) == 44, "checker_accumulator_offsets")
    seeds = np.asarray(direct, dtype=np.uint8).copy()
    actor_values = np.column_stack([np.asarray(item, dtype=np.uint8) for item in values[1:]])
    require(actor_values.shape == (P1_ROWS, 4) and len(lower_covectors) == 4,
            "checker_accumulator_shape")
    lower_values = np.zeros((P1_ROWS, 4), dtype=np.uint8)
    lower_blob_receipts: list[dict[str, Any]] = []
    for source, old in enumerate(olds):
        slices0, slices1 = checker_old_slices(lower_covectors, source)
        part0, rec0 = checker_stream_dots(
            prepare["root"], old["lower_basis_blob"], slices0,
            body_sha256=prepare["body_sha256"], role=f"old-{source}-lower")
        part1, rec1 = checker_stream_dots(
            prepare["root"], old["lifted_grade_blob"], slices1,
            body_sha256=prepare["body_sha256"], role=f"old-{source}-grade")
        offset = old_offsets[source]; stop = offset + OLD_RANKS[source]
        lower_values[offset:stop] = np.asarray(
            (part0.astype(np.uint16) + part1.astype(np.uint16)) % 3, dtype=np.uint8)
        actor_values[offset:stop] = np.asarray(
            (actor_values[offset:stop].astype(np.uint16) +
             lower_values[offset:stop].astype(np.uint16)) % 3, dtype=np.uint8)
        lower_blob_receipts.extend((rec0, rec1))
        del part0, part1, slices0, slices1
    # Bind only the fixed Task554 coefficient family here.  q/character
    # values belong to the scalar result, not this common relation receipt.
    relation_hash = relation_source_sha256()
    for seed in range(44):
        for source, old in enumerate(olds):
            seeds[seed] = _subtract(seeds[seed], old["record"]["seed_reductions"][seed],
                                    values[0], OLD_RANKS[source], old_offsets[source], relation_hash,
                                    {"kind": "seed-old", "source": source, "seed": seed})
    for source, old in enumerate(olds):
        for pivot in range(OLD_RANKS[source]):
            global_row = old_offsets[source] + pivot
            for slot in range(4):
                actor_values[global_row, slot] = _subtract(
                    actor_values[global_row, slot], old["record"]["actor_transitions"][pivot][slot],
                    values[0], OLD_RANKS[source], old_offsets[source], relation_hash,
                    {"kind": "actor-old", "basis_i": global_row, "slot": slot})
    for target in range(4):
        checked = state_descriptor(parent["blocks"][target], target); body = checked["body"]
        rank = NEW_RANKS[target]; offset = new_offsets[target]; reductions = body["origin_reductions"]
        lower_part, lower_receipt = checker_stream_dots(
            checked["root"], body["basis_blob"], checker_new_slices(lower_covectors, target),
            body_sha256=checked["body_sha256"], role=f"new-{target}-grade")
        lower_values[offset:offset + rank] = lower_part
        actor_values[offset:offset + rank] = np.asarray(
            (actor_values[offset:offset + rank].astype(np.uint16) +
             lower_part.astype(np.uint16)) % 3, dtype=np.uint8)
        lower_blob_receipts.append(lower_receipt)
        del lower_part
        for seed in range(44):
            for source in range(4):
                seeds[seed] = _subtract(
                    seeds[seed], reductions[ORIGIN_RANGES[source][0] + seed], values[0], rank,
                    new_offsets[target], relation_hash, {"kind": "seed-new", "target": target,
                                     "source": source, "seed": seed})
        for source in range(4):
            for pivot in range(OLD_RANKS[source]):
                global_row = old_offsets[source] + pivot
                for slot in range(4):
                    origin = ORIGIN_RANGES[source][0] + 44 + 4 * pivot + slot
                    actor_values[global_row, slot] = _subtract(
                        actor_values[global_row, slot], reductions[origin], values[0], rank,
                        new_offsets[target], relation_hash, {"kind": "actor-new-old", "target": target,
                                         "basis_i": global_row, "slot": slot})
        for local, row in enumerate(body["actor_transitions"]):
            global_row = offset + local
            for slot in range(4):
                actor_values[global_row, slot] = _subtract(
                    actor_values[global_row, slot], row[slot], values[0], rank,
                    new_offsets[target], relation_hash,
                    {"kind": "actor-new", "target": target, "basis_i": global_row, "slot": slot})
        del reductions, body, checked
    del prepare, olds
    return {"seed_values": seeds, "actor_values": actor_values,
            "lower_values": lower_values, "lower_blob_receipts": lower_blob_receipts,
            "relation_sha256": relation_hash, "origins": SCALAR_ORIGINS,
            "accumulator_count": SCALAR_ORIGINS}


def make_raw(character: int, table: dict[str, Any], separator: dict[str, Any],
             vector: np.ndarray) -> dict[str, Any]:
    packed = ARITH.pack_trits(vector)
    body = {"schema": ARITH.LIVE_SCHEMA + ".RawDual", "separator_generation": separator["generation"],
            "separator_s_head_sha256": SEPARATOR_STATE_HEAD, "lambda_sha256": separator["lambda_sha256"],
            "character": character, "B_adj_table_identity": table["identity"]["adjoint:B"],
            "word_node": {"kind": "root", "character": character, "actors": []},
            # This is the root node; actor identities belong to future edges.
            "actor_table_identities_along_w": [],
            "raw_q_packed_sha256": sha(packed), "raw_q_packed_offset": 0,
            "raw_q_packed_length": len(packed), "raw_predecessor_sha256": None}
    return {**body, "sha256": sha(canonical(body))}


def p1_values(p1: dict[str, Any], vectors: list[list[np.ndarray]]) -> dict[str, Any]:
    values = [[np.zeros(P1_ROWS, dtype=np.uint8) for _ in range(5)] for _ in range(4)]
    instruction_path = safe_path(p1["root"], p1["instruction"]["path"])
    _, instruction_sha = file_hash(instruction_path, P1_INSTRUCTION_BYTES, 1 << 30)
    require(instruction_sha == P1_INSTRUCTION_SHA256, "checker_instruction_hash")
    active = [bool(np.count_nonzero(group[0])) for group in vectors]
    require(active == [True, False, False, False], "checker_active_root_pin")
    projections: list[list[tuple[np.ndarray, np.ndarray, np.ndarray]]] = []
    for character in range(4):
        group: list[tuple[np.ndarray, np.ndarray, np.ndarray]] = []
        for vector in vectors[character]:
            pairs = [(int(i), int(vector[i])) for i in np.flatnonzero(vector)]
            if pairs:
                byte_index = np.asarray([i // 4 for i, _ in pairs], dtype=np.int64)
                digit_slot = np.asarray([i % 4 for i, _ in pairs], dtype=np.int64)
                coefficient = np.asarray([c for _, c in pairs], dtype=np.uint32)
            else:
                byte_index = np.asarray([], dtype=np.int64)
                digit_slot = np.asarray([], dtype=np.int64)
                coefficient = np.asarray([], dtype=np.uint32)
            group.append((byte_index, digit_slot, coefficient))
        projections.append(group)
    cache_path = safe_path(p1["root"], p1["cache"]["path"]); cache_hash = hashlib.sha256()
    buffer = bytearray(P1_ROW_BYTES * 256)
    cursor = 0
    with cache_path.open("rb") as stream:
        while cursor < P1_ROWS:
            count_rows = min(256, P1_ROWS - cursor)
            byte_count = count_rows * P1_ROW_BYTES
            require(stream.readinto(memoryview(buffer)[:byte_count]) == byte_count,
                    "checker_cache_eof")
            raw_chunk = memoryview(buffer)[:byte_count]; cache_hash.update(raw_chunk)
            packed_rows = np.frombuffer(raw_chunk, dtype=np.uint8).reshape(count_rows, P1_ROW_BYTES)
            for character in range(4):
                if not active[character]:
                    continue
                projected = vectorized_projection_chunk(
                    packed_rows, character * SLICE_BYTES, projections[character])
                for slot in range(5):
                    values[character][slot][cursor:cursor + count_rows] = projected[:, slot]
            cursor += count_rows
        require(stream.read(1) == b"", "checker_cache_trailing")
    require(cache_hash.hexdigest() == P1_CACHE_SHA256, "checker_cache_hash")
    return {"values": values, "manifest_sha256": p1["manifest_sha256"],
            "cache_sha256": cache_hash.hexdigest(), "instruction_sha256": instruction_sha,
            "value_sha256": [sha(v.tobytes()) for group in values for v in group],
            "rows": P1_ROWS, "cache_passes": 1, "instruction_passes": 1,
            "active_characters": [0], "active_pairings": 5}


def _scan_accumulated(raw: dict[str, Any], accum: dict[str, Any],
                      p1: dict[str, Any]) -> dict[str, Any]:
    """Independent scalar-order replay over the direct accumulator."""
    ARITH.validate_raw_dual(raw)
    seeds = accum["seed_values"]; actors = accum["actor_values"]
    require(len(seeds) == 44 and actors.shape == (P1_ROWS, 4),
            "checker_accumulator_scan_shape")
    chain = b"\0" * 32; origin = 0

    def emit(kind: str, descriptor: dict[str, Any], scalar: int) -> dict[str, Any] | None:
        nonlocal chain, origin
        record = {"origin_id": origin, "origin_kind": kind, **descriptor,
                  "scalar": int(scalar)}
        chain = hashlib.sha256(chain + canonical(record)).digest(); origin += 1
        if scalar:
            return _sealed("Violation", {
                "raw_dual_sha256": raw["sha256"], "character": raw["character"],
                "word_node_sha256": sha(canonical(raw["word_node"])), **record,
                "scalar_prefix_digest": chain.hex(),
                "p1_manifest_sha256": p1["manifest_sha256"],
                "global_relation_stream_sha256": accum["relation_sha256"],
                "value_vector_sha256": [sha(value.tobytes()) for value in p1["values"]],
                "filtered_direct_receipt_sha256": accum["filtered_direct_receipt_sha256"]})
        return None

    for seed in range(44):
        hit = emit("seed", {"seed": seed}, int(seeds[seed]))
        if hit is not None:
            return hit
    for basis_i in range(P1_ROWS):
        for slot, actor in enumerate(ACTORS):
            hit = emit("actor", {"basis_i": basis_i, "actor": actor},
                       int(actors[basis_i, slot]))
            if hit is not None:
                return hit
    require(origin == SCALAR_ORIGINS, "checker_accumulator_origin_eof")
    return _sealed("ScalarEOF", {
        "raw_dual_sha256": raw["sha256"], "p1_manifest_sha256": p1["manifest_sha256"],
        "global_relation_stream_sha256": accum["relation_sha256"],
        "origins": SCALAR_ORIGINS, "seed_pairings": 44,
        "actor_pairings": 4 * P1_ROWS, "next_origin": SCALAR_ORIGINS,
        "coefficient_stream_eof": True, "p1_cache_pass_eof": True,
        "value_vector_sha256": [sha(value.tobytes()) for value in p1["values"]],
        "rolling_scalar_head": chain.hex(),
        "filtered_direct_receipt_sha256": accum["filtered_direct_receipt_sha256"]})


def _sealed(kind: str, body: dict[str, Any]) -> dict[str, Any]:
    result = {"schema": ARITH.LIVE_SCHEMA + "." + kind, **body}
    result["sha256"] = sha(canonical(result)); return result


def _expected_character(character: int, table: dict[str, Any], vectors: list[np.ndarray],
                        separator: dict[str, Any], p1: dict[str, Any], task554: dict[str, Any],
                        values: list[np.ndarray], *,
                        context_bundle: tuple[Any, dict[str, Any]] | None = None,
                        payloads: dict[str, bytes] | None = None) -> dict[str, Any]:
    root = vectors[0]; packed = ARITH.pack_trits(root); nz = np.flatnonzero(root)
    children = [{"actor": actor, "support": int(np.count_nonzero(vector)),
                 "packed_sha256": sha(ARITH.pack_trits(vector))}
                for actor, vector in zip(ACTORS, vectors[1:])]
    base = {"character": character, "character_label": list(CHARACTERS[character]),
            "v541_formula_id": V541_FORMULA_ID,
            "root_support": int(np.count_nonzero(root)), "root_packed_sha256": sha(packed),
            "children": children, "task712_table_identities": table["identity"],
            "raw_dual": make_raw(character, table, separator, root), "root_packed_bytes": len(packed)}
    ARITH.validate_raw_dual(base["raw_dual"])
    if not len(nz):
        unsigned = {"schema": SCHEMA + ".RootZero", **base, "root_scalar": "zero"}
        unsigned["sha256"] = sha(canonical(unsigned)); return unsigned
    context, words = context_bundle if context_bundle is not None else checker_source_context()
    raw_seeds = checker_raw_seed_direct(context, words, root, character,
                                         actual_pin=(character == 0))
    lower_covectors, covector_receipt = checker_actor_adjoints(
        context, root, character, vectors[1:])
    accumulator = accumulate_scalars(task554, character, raw_seeds["values"],
                                     [values[slot] for slot in range(5)], lower_covectors)
    if character == 0:
        require(int(accumulator["seed_values"][2]) == 0, "checker_actual_seed2_corrected_scalar")
    lower_receipts = accumulator["lower_blob_receipts"]
    require(len(lower_receipts) == 12 and
            sum(item["descriptor"]["bytes"] for item in lower_receipts) == LOWER_BLOB_BYTES,
            "checker_lower_blob_complete_receipt")
    lower_body = {"schema": SCHEMA + ".lower-blob-stream.v1",
                  "pin_sha256": LOWER_BLOB_PIN_SHA256, "total_bytes": LOWER_BLOB_BYTES,
                  "receipts": lower_receipts, "all_packed_bytes_at_most_80": True,
                  "padding_trits": 0}
    lower_receipt = {**lower_body, "sha256": sha(canonical(lower_body))}
    repaired_payloads = [(f"seed-scalars-a{character}.bin", accumulator["seed_values"].tobytes())]
    repaired_payloads.extend((f"actor-lower-a{character}-t{slot}.bin",
                              accumulator["lower_values"][:, slot].tobytes()) for slot in range(4))
    saved_arrays = [{"file": name, "bytes": len(data), "sha256": sha(data)}
                    for name, data in repaired_payloads]
    if payloads is not None:
        for name, data in repaired_payloads:
            require(name not in payloads, "checker_repaired_payload_unique")
            payloads[name] = data
    complete_direct = np.asarray(
        (np.column_stack(values[1:]).astype(np.uint16) +
         accumulator["lower_values"].astype(np.uint16)) % 3, dtype=np.uint8)
    filtered_body = {
        "schema": SCHEMA + ".filtered-direct.v541", "formula_id": V541_FORMULA_ID,
        "character": character,
        "seed_direct_receipt_sha256": raw_seeds["receipt"]["sha256"],
        "seed_direct_receipt": raw_seeds["receipt"],
        "actor_covector_receipt_sha256": covector_receipt["sha256"],
        "actor_covector_receipt": covector_receipt,
        "lower_blob_receipt_sha256": lower_receipt["sha256"],
        "lower_blob_receipt": lower_receipt, "actor_order": list(ACTORS),
        "actor_top_value_sha256": [sha(item.tobytes()) for item in values[1:]],
        "actor_lower_value_sha256": [sha(accumulator["lower_values"][:, slot].tobytes())
                                     for slot in range(4)],
        "actor_complete_direct_value_sha256": [sha(complete_direct[:, slot].tobytes())
                                               for slot in range(4)],
        "corrected_seed_scalars_sha256": saved_arrays[0]["sha256"],
        "actual_seed2_corrected_scalar": int(accumulator["seed_values"][2]) if character == 0 else None,
        "saved_arrays": saved_arrays,
        "actor_direct_includes_lower_to_top": True,
        "seed_direct_is_raw_character_slice": True,
        "projected_direct_seed_routine_called": False}
    filtered = {**filtered_body, "sha256": sha(canonical(filtered_body))}
    base["v541_formula_id"] = V541_FORMULA_ID
    base["filtered_direct"] = filtered
    accumulator["filtered_direct_receipt_sha256"] = filtered["sha256"]
    base["relation_stream_sha256"] = accumulator["relation_sha256"]
    scalar = _scan_accumulated(base["raw_dual"], accumulator,
                                {"manifest_sha256": p1["manifest_sha256"], "values": values})
    base["scalar"] = scalar; base["scalar_schema"] = scalar["schema"]
    if scalar["schema"].endswith("ScalarEOF"):
        lead = int(nz[0]); scale = 1 if int(root[lead]) == 1 else 2
        normalized = ((scale * root.astype(np.uint16)) % 3).astype(np.uint8)
        normalized_packed = ARITH.pack_trits(normalized); normalized_sha = sha(normalized_packed)
        remainder_sha = sha(packed)
        next_head = ARITH._dual_next_state_head(
            "0" * 64, 0, lead, normalized_sha, base["raw_dual"]["sha256"],
            remainder_sha, 1)
        base["normalized_root_state"] = {
            "lead": lead, "scale": scale, "raw_lead": lead,
            "raw_lead_scalar": int(root[lead]), "raw_packed_sha256": sha(packed),
            "raw_q_file": f"q-a{character}-root.bin", "raw_q_file_bytes": len(packed),
            "raw_q_file_sha256": sha(packed), "raw_dual_sha256": base["raw_dual"]["sha256"],
            "remainder_sha256": remainder_sha, "normalized_packed_sha256": normalized_sha,
            "packed_sha256": normalized_sha, "normalized_pivot_sha256": normalized_sha,
            "normalized_packed_bytes": len(normalized_packed),
            "prior_state_head_sha256": "0" * 64, "prior_pivot_coefficients": [],
            "rank_before": 0, "insertion_id": 0, "dual_rank_after": 1,
            "next_state_head_sha256": next_head, "rolling_head": next_head,
            "normalized_from_raw_q": True,
            "future_orbit_declared_bound": 504, "future_orbit_rows_executed": 0,
            "remaining_independent_after_root": 503}
    result = {"schema": SCHEMA + (".RootViolation" if scalar["schema"].endswith("Violation") else ".RootScalarEOF"),
              **base}; result["sha256"] = sha(canonical(result)); return result


def launch_claims() -> dict[str, Any]:
    return {"ROOT_SCALAR_BATCH_CANDIDATE": True, "COMPLETE_DUAL_ORBITS": False,
            "GRADE2_MEMBER": "NOT_DECIDED", "GRADE2_NONMEMBER": "NOT_DECIDED",
            "A0": "NOT_DECLARED", "COMMON": "NOT_DECLARED", "COFINAL_LIFT": "NOT_DECLARED",
            "FAKE": "NOT_DECLARED", "IHARA": "NOT_DECLARED", "verified": False}


def terminal_claims() -> dict[str, Any]:
    return {"ROOT_SCALAR_BATCH_CANDIDATE": True, "COMPLETE_DUAL_ORBITS": False,
            "GRADE2_MEMBER": "NOT_DECIDED", "GRADE2_NONMEMBER": "NOT_DECIDED",
            "A0": "NOT_DECLARED", "COMMON": "NOT_DECLARED", "COFINAL_LIFT": "NOT_DECLARED",
            "FAKE": "NOT_DECLARED", "IHARA": "NOT_DECLARED", "verified": False}


def terminal_kind(records: list[dict[str, Any]]) -> str:
    require(isinstance(records, list) and len(records) == 4,
            "checker_terminal_record_count")
    return ("RootViolationBatch" if any(
        item.get("schema", "").endswith("RootViolation") for item in records)
            else "AllFourRootEOF")


def validate_scalar_record(actual: Any, expected: Any) -> None:
    require(actual == expected and sealed_object(actual),
            "checker_scalar_record_exact")


def validate_character_record(actual: Any, expected: Any) -> None:
    require(isinstance(actual, dict) and isinstance(expected, dict),
            "checker_character_record_shape")
    if "scalar" in expected:
        validate_scalar_record(actual.get("scalar"), expected["scalar"])
    require(actual == expected and sealed_object(actual),
            "checker_character_record_exact")


def validate_output_objects(terminal: Any, result: Any, manifest: Any,
                            expected_terminal: Any, expected_result: Any,
                            expected_manifest: Any) -> None:
    """Exact sealed-object join used by production output checking."""
    require(terminal == expected_terminal and sealed_object(terminal),
            "checker_terminal_exact")
    require(result == expected_result and sealed_object(result),
            "checker_result_exact")
    require(manifest == expected_manifest and sealed_object(manifest),
            "checker_manifest_exact")


def check_output(base: dict[str, Any], tables: list[dict[str, Any]], vectors: list[list[np.ndarray]],
                 values: dict[str, Any]) -> dict[str, Any]:
    out = Path(base["launch"]["out"]).absolute(); require(out.is_dir(), "checker_output_root")
    manifest, manifest_raw = read_json(out / "manifest.json", cap=1 << 24)
    files = manifest.get("files"); require(isinstance(files, list), "checker_output_manifest_files")
    actual = sorted(p.name for p in out.iterdir() if p.is_file())
    require(manifest.get("file_roster") == actual and len(actual) == len(set(actual)) and
            "manifest.json" in actual and "result.json" in actual and "terminal.json" in actual,
            "checker_output_roster")
    by_name = {item.get("file"): item for item in files if isinstance(item, dict)}
    require(len(by_name) == len(files), "checker_output_receipt_unique")
    for item in files: receipt(out, item, 1 << 28)
    terminal, terminal_raw = read_json(out / "terminal.json", cap=1 << 24)
    result, result_raw = read_json(out / "result.json", cap=1 << 24)
    expected_chars: list[dict[str, Any]] = []
    expected_records: list[dict[str, Any]] = []
    expected_result_files: list[dict[str, Any]] = []
    source_bundle = checker_source_context()
    for character in range(4):
        child_receipts = []
        for slot, wanted in enumerate(EXPECTED_CHILD[character]):
            item = {"file": f"q-a{character}-t{slot}", "bytes": SLICE_BYTES,
                    "sha256": wanted}
            # The producer's file name includes the .bin suffix; retain the
            # exact receipt in the sealed result order below.
            item["file"] += ".bin"
            child_receipts.append(item)
            child_raw = receipt(out, item, 1 << 20)
            require(child_raw == ARITH.pack_trits(vectors[character][slot + 1]),
                    "checker_child_file")
        root_item = {"file": f"q-a{character}-root.bin", "bytes": SLICE_BYTES,
                     "sha256": EXPECTED_ROOT[character][3]}
        root_raw = receipt(out, root_item, 1 << 20)
        require(root_raw == ARITH.pack_trits(vectors[character][0]), "checker_root_file")
        expected_payloads: dict[str, bytes] = {}
        expected = _expected_character(character, tables[character], vectors[character], base["separator"],
                                       base["p1"], base["task554"], values["values"][character],
                                       context_bundle=source_bundle, payloads=expected_payloads)
        repaired_receipts = expected.get("filtered_direct", {}).get("saved_arrays", [])
        require(set(expected_payloads) == {item["file"] for item in repaired_receipts},
                "checker_repaired_payload_roster")
        for item in repaired_receipts:
            require(receipt(out, item, 1 << 20) == expected_payloads[item["file"]],
                    "checker_repaired_payload_exact")
        actual_path = out / f"character-a{character}.json"; got, got_raw = read_json(actual_path, cap=1 << 24)
        validate_character_record(got, expected)
        expected_chars.append({"character": character, "schema": expected["schema"], "sha256": expected["sha256"]})
        expected_records.append(expected)
        expected_result_files.extend(child_receipts + [root_item] + repaired_receipts + [
            {"file": f"character-a{character}.json", "bytes": len(got_raw),
             "sha256": sha(got_raw)}])
        if expected["schema"].endswith("RootScalarEOF"):
            state_name = f"root-state-a{character}.json"
            state_value, state_raw = read_json(out / state_name, cap=1 << 20)
            require(state_value == expected["normalized_root_state"], "checker_root_state_replay")
            require(sha(state_raw) == sha(canonical(state_value)), "checker_root_state_canonical")
            expected_result_files.append({"file": state_name, "bytes": len(state_raw),
                                          "sha256": sha(state_raw)})
    terminal_value = terminal_kind(expected_records)
    expected_terminal_body = {
        "schema": SCHEMA + ".terminal", "terminal": terminal_value,
        "character_order": [list(x) for x in CHARACTERS], "actor_order": list(ACTORS),
        "characters": expected_chars, "p1_cache_passes": 1, "p1_rows": P1_ROWS,
        "global_relation_declared_count": SCALAR_ORIGINS,
        "future_active_orbit_declared_bound": 504, "future_orbit_rows_executed": 0,
        "v541_formula_id": V541_FORMULA_ID,
        **terminal_claims()}
    expected_terminal = {**expected_terminal_body,
                        "sha256": sha(canonical(expected_terminal_body))}
    expected_terminal_receipt = {"file": "terminal.json", "bytes": len(terminal_raw),
                                 "sha256": sha(terminal_raw)}
    expected_result_files.append(expected_terminal_receipt)
    expected_result_body = {
        "schema": SCHEMA + ".result", "launch_sha256": base["launch_sha256"],
        "separator_manifest_sha256": base["separator"]["manifest_sha256"],
        "p1_manifest_sha256": base["p1"]["manifest_sha256"],
        "task712_manifest_sha256": [item["manifest_sha256"] for item in tables],
        "global_relation_stream_sha256": expected_records[0].get("relation_stream_sha256"),
        "v541_formula_id": V541_FORMULA_ID,
        "filtered_direct_receipt_sha256": [item.get("filtered_direct", {}).get("sha256")
                                          for item in expected_records],
        "cache_passes": 1, "instruction_passes": 1, "rows": P1_ROWS,
        "characters": [item["sha256"] for item in expected_chars],
        "terminal_sha256": expected_terminal["sha256"], "files": expected_result_files,
        "claims": base["launch"]["claims"]}
    expected_result = {**expected_result_body,
                       "sha256": sha(canonical(expected_result_body))}
    expected_result_raw = canonical(expected_result)
    expected_result_receipt = {"file": "result.json", "bytes": len(expected_result_raw),
                               "sha256": sha(expected_result_raw)}
    expected_manifest_files = sorted(expected_result_files + [expected_result_receipt],
                                     key=lambda item: item["file"])
    expected_manifest_body = {
        "schema": SCHEMA + ".output-manifest", "terminal": terminal_value,
        "file_roster": sorted([item["file"] for item in expected_manifest_files] +
                               ["manifest.json"]),
        "files": expected_manifest_files, "result": expected_result_receipt,
        "candidate": True, "verified": False}
    expected_manifest = {**expected_manifest_body,
                         "sha256": sha(canonical(expected_manifest_body))}
    expected_names = {item["file"] for item in expected_result_files} | {"result.json", "manifest.json"}
    require(set(actual) == expected_names, "checker_output_exact_roster")
    validate_output_objects(terminal, result, manifest, expected_terminal,
                            expected_result, expected_manifest)
    return {"status": "PASS", "terminal": terminal["terminal"], "rows": P1_ROWS,
            "root_characters": 4, "cache_passes": 1,
            "relation_origin_declared_count": SCALAR_ORIGINS,
            "future_orbit_rows_executed": 0, "v541_formula_id": V541_FORMULA_ID,
            "complete_dual_orbits": False, "verified": False}


def _expect_reject(action: Any, reason: str) -> None:
    try:
        action()
    except Exception:
        return
    raise RuntimeError(reason)


def selftest() -> dict[str, Any]:
    rng = np.random.default_rng(9081)
    dense = rng.integers(0, 3, P1_ROW_TRITS, dtype=np.uint8)
    packed = ARITH.pack_trits(dense)
    vectors = [rng.integers(0, 3, SOURCE_WIDTH, dtype=np.uint8) for _ in range(20)]
    sparse_ok = []
    for offset in range(4):
        for vector in vectors[offset:offset + 4]:
            entries = [(int(i), int(vector[i])) for i in np.flatnonzero(vector)]
            sparse_ok.append(sparse_projection(packed, offset * SLICE_BYTES, entries) ==
                             ARITH.dot_mod3(ARITH.unpack_trits(
                                 packed[offset * SLICE_BYTES:(offset + 1) * SLICE_BYTES], SOURCE_WIDTH), vector))
    require(all(sparse_ok), "selftest_sparse")

    # Compare the checker vectorized five-value call with five independent
    # scalar projections; this is not the same expression twice.
    one_row = np.frombuffer(packed, dtype=np.uint8).reshape(1, P1_ROW_BYTES)
    chunk_projections = []
    for character in range(4):
        group = []
        for slot in range(5):
            indices = np.flatnonzero(vectors[5 * character + slot])
            group.append((np.asarray([i // 4 for i in indices], dtype=np.int64),
                          np.asarray([i % 4 for i in indices], dtype=np.int64),
                          np.asarray([int(vectors[5 * character + slot][i])
                                      for i in indices], dtype=np.int64)))
        chunk_projections.append(group)
    simultaneous = [vectorized_projection_chunk(one_row, character * SLICE_BYTES,
                                                 chunk_projections[character])[0].tolist()
                    for character in range(4)]
    separate = [[sparse_projection(packed, character * SLICE_BYTES,
                                   [(int(i), int(vectors[5 * character + slot][i]))
                                    for i in np.flatnonzero(vectors[5 * character + slot])])
                 for slot in range(5)] for character in range(4)]
    require(simultaneous == separate, "selftest_batch_equivalence")

    # Exercise the exact vectorized chunk path, including a short final chunk,
    # against independently unpacked dense rows at all four offsets.
    tiny_dense = rng.integers(0, 3, size=(3, P1_ROW_TRITS), dtype=np.uint8)
    tiny_rows = np.vstack([np.frombuffer(ARITH.pack_trits(item), dtype=np.uint8)
                           for item in tiny_dense])
    for character in range(4):
        got = vectorized_projection_chunk(tiny_rows, character * SLICE_BYTES,
                                           chunk_projections[character])
        expected = np.asarray([[ARITH.dot_mod3(
            ARITH.unpack_trits(bytes(tiny_rows[row])[character * SLICE_BYTES:
                                                    (character + 1) * SLICE_BYTES], SOURCE_WIDTH),
            vectors[5 * character + slot]) for slot in range(5)] for row in range(3)], dtype=np.uint8)
        require(np.array_equal(got, expected), "checker_vectorized_chunk_dense")

    table_control = False
    with tempfile.TemporaryDirectory(prefix="d972-r07-task913-checker-table-") as temp:
        table_root = Path(temp)
        forward_entries = [(0, 0, 1), (1, 0, 2), (3, 2, 1)]
        adjoint_entries = sorted((d, s, c) for s, d, c in forward_entries)

        def table_file(name: str, entries: list[tuple[int, int, int]]) -> tuple[Path, dict[str, Any]]:
            body = b"".join(ARITH._table_line(item) for item in entries)
            marker = {"body_bytes": len(body), "body_sha256": sha(body),
                      "count": len(entries), "eof": True}
            raw = body + canonical(marker); path = table_root / name
            path.write_bytes(raw)
            return path, {"bytes": len(raw), "sha256": sha(raw),
                          "source_width": SOURCE_WIDTH, "destination_width": SOURCE_WIDTH,
                          "entry_count": len(entries), "body_bytes": len(body),
                          "body_sha256": sha(body), "eof": True}

        _, forward_receipt = table_file("forward.jsonl", forward_entries)
        _, adjoint_receipt = table_file("adjoint.jsonl", adjoint_entries)
        forward = ARITH._read_table(table_root / "forward.jsonl", forward_receipt)
        adjoint = ARITH._read_table(table_root / "adjoint.jsonl", adjoint_receipt)
        check_table_transpose(forward, adjoint); table_control = True
        bad_entries = list(adjoint_entries); bad_entries[-1] = (2, 3, 2)
        _, bad_receipt = table_file("bad-adjoint.jsonl", bad_entries)
        bad_adjoint = ARITH._read_table(table_root / "bad-adjoint.jsonl", bad_receipt)
        _expect_reject(lambda: check_table_transpose(forward, bad_adjoint),
                       "checker_task712_transpose_control")

    separator_control = False
    separator_names = ("SEPARATOR_RUN", "SEPARATOR_ATTEMPT", "SEPARATOR_HEAD",
                       "SEPARATOR_ARTIFACT", "SEPARATOR_ARTIFACT_NAME",
                       "SEPARATOR_ARCHIVE_BYTES", "SEPARATOR_ARCHIVE_SHA256",
                       "SEPARATOR_MANIFEST_SHA256", "SEPARATOR_PHYSICAL_BYTES",
                       "SEPARATOR_PHYSICAL_SHA256", "SEPARATOR_LAMBDA_SHA256",
                       "SEPARATOR_TERMINAL_SHA256", "SEPARATOR_RESULT_SHA256",
                       "SEPARATOR_CHECKER_SHA256", "SEPARATOR_GENERATION",
                       "SEPARATOR_RANK", "SEPARATOR_STATE_HEAD")
    saved_separator = {name: globals()[name] for name in separator_names}
    try:
        zero_physical = bytes(PHYSICAL_PACKED_BYTES); state_head = "b" * 64
        manifest_body = {"generation": 1, "rank": 1,
                         "instructions": {"final_head": state_head},
                         "candidate_roster": ["physical.bin", "physical-p1-coeff.bin",
                                              "instructions.jsonl", "manifest.json", "HEAD"]}
        manifest_raw = canonical(manifest_body)
        internal_raw = {"terminal": b"terminal", "result": b"result", "checker": b"checker"}
        globals().update({"SEPARATOR_RUN": 1, "SEPARATOR_ATTEMPT": 1,
                          "SEPARATOR_HEAD": "h" * 40, "SEPARATOR_ARTIFACT": 2,
                          "SEPARATOR_ARTIFACT_NAME": "tiny-separator", "SEPARATOR_ARCHIVE_BYTES": 3,
                          "SEPARATOR_ARCHIVE_SHA256": "sha256:" + "a" * 64,
                          "SEPARATOR_MANIFEST_SHA256": sha(manifest_raw),
                          "SEPARATOR_PHYSICAL_BYTES": len(zero_physical),
                          "SEPARATOR_PHYSICAL_SHA256": sha(zero_physical),
                          "SEPARATOR_LAMBDA_SHA256": sha(zero_physical),
                          "SEPARATOR_TERMINAL_SHA256": sha(internal_raw["terminal"]),
                          "SEPARATOR_RESULT_SHA256": sha(internal_raw["result"]),
                          "SEPARATOR_CHECKER_SHA256": sha(internal_raw["checker"]),
                          "SEPARATOR_GENERATION": 1, "SEPARATOR_RANK": 1,
                          "SEPARATOR_STATE_HEAD": state_head})
        with tempfile.TemporaryDirectory(prefix="d972-r07-task913-checker-separator-") as temp:
            root = Path(temp); (root / "state").mkdir(); (root / "output").mkdir()
            (root / "manifest.json").write_bytes(manifest_raw)
            (root / "state" / "physical.bin").write_bytes(zero_physical)
            (root / "output" / "lambda.bin").write_bytes(zero_physical)
            for name, raw in internal_raw.items(): (root / "output" / (name + ".bin")).write_bytes(raw)
            parent = {"schema": SCHEMA + ".separator-parent.v1", "root": str(root),
                      "artifact": {"run": 1, "attempt": 1, "head": "h" * 40, "id": 2,
                                   "name": "tiny-separator", "bytes": 3,
                                   "sha256": "sha256:" + "a" * 64},
                      "manifest": {"file": "manifest.json", "bytes": len(manifest_raw),
                                   "sha256": sha(manifest_raw)},
                      "physical": {"file": "state/physical.bin", "bytes": len(zero_physical),
                                   "sha256": sha(zero_physical), "rows": 1},
                      "lambda": {"file": "output/lambda.bin", "bytes": len(zero_physical),
                                 "sha256": sha(zero_physical)},
                      "internal": {key: {"file": "output/" + key + ".bin", "bytes": len(raw),
                                          "sha256": sha(raw)} for key, raw in internal_raw.items()}}
            validate_separator(parent); separator_control = True
            bad = json.loads(json.dumps(parent)); bad["internal"]["terminal"]["sha256"] = "0" * 64
            _expect_reject(lambda: validate_separator(bad), "selftest_separator_mutation_control")
    finally:
        globals().update(saved_separator)

    p1_control = False
    p1_names = ("P1_RUN", "P1_ATTEMPT", "P1_HEAD", "P1_ARTIFACT", "P1_ARTIFACT_NAME",
                "P1_ARCHIVE_BYTES", "P1_ARCHIVE_SHA256", "P1_MANIFEST_BYTES",
                "P1_MANIFEST_SHA256", "P1_CACHE_BYTES", "P1_CACHE_SHA256",
                "P1_INSTRUCTION_BYTES", "P1_INSTRUCTION_SHA256", "P1_ROWS")
    saved_p1 = {name: globals()[name] for name in p1_names}
    try:
        cache_raw = bytes(P1_ROW_BYTES); instruction_raw = b"x"; ancestry = "c" * 64
        globals().update({"P1_RUN": 1, "P1_ATTEMPT": 1, "P1_HEAD": "p" * 40,
                          "P1_ARTIFACT": 2, "P1_ARTIFACT_NAME": "tiny-p1", "P1_ARCHIVE_BYTES": 3,
                          "P1_ARCHIVE_SHA256": "sha256:" + "d" * 64, "P1_CACHE_BYTES": len(cache_raw),
                          "P1_CACHE_SHA256": sha(cache_raw), "P1_INSTRUCTION_BYTES": len(instruction_raw),
                          "P1_INSTRUCTION_SHA256": sha(instruction_raw), "P1_ROWS": 1})
        manifest = {"schema": "d972.r07.canonical-p1-dag-degree2-lift.v8",
                    "status": "CANONICAL_P1_DAG_DEGREE2_LIFT_CANDIDATE", "rows": 1,
                    "row_trits": P1_ROW_TRITS, "row_bytes": P1_ROW_BYTES,
                    "global_order": [0, 505, 1008, 1511, 2014, 3523, 5035, 6547, 8059],
                    "actor_order": list(ACTORS), "character_order": [list(x) for x in CHARACTERS],
                    "independent_checker": False, "A0": False, "COMMON": False,
                    "COFINAL": False, "FAKE": False, "IHARA": False, "verified": False,
                    "ancestry_sha256": ancestry,
                    "cache": {"path": "degree2.cache.bin", "rows": 1, "bytes": len(cache_raw),
                              "sha256": sha(cache_raw), "final_lf": False, "eof": True},
                    "instruction": {"path": "instructions.jsonl", "rows": 1,
                                    "bytes": len(instruction_raw), "sha256": sha(instruction_raw),
                                    "final_lf": True, "eof": True, "final_head": ancestry}}
        manifest_raw = canonical(manifest)
        globals()["P1_MANIFEST_BYTES"] = len(manifest_raw); globals()["P1_MANIFEST_SHA256"] = sha(manifest_raw)
        with tempfile.TemporaryDirectory(prefix="d972-r07-task913-checker-p1-") as temp:
            root = Path(temp); (root / "manifest.json").write_bytes(manifest_raw)
            (root / "degree2.cache.bin").write_bytes(cache_raw)
            (root / "instructions.jsonl").write_bytes(instruction_raw)
            parent = {"root": str(root), "manifest": {"file": "manifest.json",
                       "bytes": len(manifest_raw), "sha256": sha(manifest_raw)},
                      "files": [{"file": "degree2.cache.bin", "bytes": len(cache_raw),
                                 "sha256": sha(cache_raw)},
                                {"file": "instructions.jsonl", "bytes": len(instruction_raw),
                                 "sha256": sha(instruction_raw)}],
                      "run": 1, "attempt": 1, "head": "p" * 40, "artifact": 2,
                      "artifact_name": "tiny-p1", "archive_bytes": 3,
                      "archive_sha256": "sha256:" + "d" * 64}
            checked = validate_p1(parent)
            tiny_vectors = [[np.zeros(SOURCE_WIDTH, dtype=np.uint8) for _ in range(5)] for _ in range(4)]
            tiny_vectors[0][0][0] = 1
            p1_values(checked, tiny_vectors)
            bad_manifest = json.loads(json.dumps(parent)); bad_manifest["manifest"]["sha256"] = "0" * 64
            _expect_reject(lambda: validate_p1(bad_manifest), "selftest_p1_manifest_control")
            (root / "degree2.cache.bin").write_bytes(cache_raw[:-1])
            _expect_reject(lambda: p1_values(checked, tiny_vectors), "selftest_p1_truncation_control")
        p1_control = True
    finally:
        globals().update(saved_p1)

    tiny_accumulator_control = False
    accumulator_names = ("P1_ROWS", "OLD_RANKS", "NEW_RANKS", "ORIGIN_RANGES",
                         "TASK554_ORIGINS", "SCALAR_ORIGINS", "TASK554_BODY_DIGESTS",
                         "OLD_BLOB_PINS", "NEW_BLOB_PINS")
    saved_accumulator = {name: globals()[name] for name in accumulator_names}
    try:
        globals().update({"P1_ROWS": 3, "OLD_RANKS": (1, 0, 0, 0),
                          "NEW_RANKS": (0, 1, 1, 0),
                          "ORIGIN_RANGES": ((0, 48), (48, 92), (92, 136), (136, 180)),
                          "TASK554_ORIGINS": 180, "SCALAR_ORIGINS": 56})

        def tiny_old(character: int, rank: int, start: int) -> dict[str, Any]:
            seed_terms = [[[0, 1]] for _ in range(44)] if rank else [[] for _ in range(44)]
            actor_terms = [[[[0, 1 if slot % 2 == 0 else 2]] for slot in range(4)]] if rank else []
            nodes = [{"pivot": 0, "scale": 1, "reductions": [[0, 1]]}] if rank else []
            record = {"rank": rank, "character": list(CHARACTERS[character]),
                      "attempts": 44 + 4 * rank, "actor_order": list(ACTORS),
                      "queue_exhausted": True, "seed_reductions": seed_terms,
                      "dag_nodes": nodes, "actor_transitions": actor_terms}
            return {"character_index": character, "character": list(CHARACTERS[character]),
                    "rank": rank, "record": record, "defect_origin_range": [start, start + 44 + 4 * rank]}

        tiny_payloads: dict[str, bytes] = {}
        tiny_dense_lower = np.zeros((3, LOWER_WIDTH), dtype=np.uint8)
        tiny_covectors = [rng.integers(0, 3, LOWER_WIDTH, dtype=np.uint8) for _ in range(4)]
        for item in tiny_covectors:
            item[-8:] = 0
        tiny_covectors[0].fill(0)
        tiny_covectors[0][4 * SOURCE0C + SOURCE1C + 17] = 1

        def tiny_blob(stem: str, rows: np.ndarray, width: int) -> dict[str, Any]:
            raw = b"".join(ARITH.pack_trits(row) for row in rows)
            digest = sha(raw); name = stem + "." + digest + ".bin"
            tiny_payloads[name] = raw
            return {"file": name, "bytes": len(raw), "sha256": digest,
                    "rows": len(rows), "width": width, "encoding": PACK_ENCODING}

        old_blocks = []; cursor = 0; tiny_old_pins = []
        for character, rank in enumerate(OLD_RANKS):
            item = tiny_old(character, rank, cursor); cursor += 44 + 4 * rank
            low = rng.integers(0, 3, size=(rank, OLD_LOWER_WIDTH), dtype=np.uint8)
            grade = np.zeros((rank, OLD_GRADE_WIDTH), dtype=np.uint8)
            if rank:
                grade[0, 7] = 1
                grade[0, SOURCE1C + 17] = 1
                grade[0, 2 * SOURCE1C + 41] = 2
                tiny_dense_lower[0, :SOURCE0C] = low[0, :SOURCE0C]
                tiny_dense_lower[0, 4 * SOURCE0C:4 * SOURCE0C + 4 * SOURCE1C] = grade[0]
                tiny_dense_lower[0, -8:] = low[0, -8:]
            low_desc = tiny_blob(f"old-{character}-lower-basis", low, OLD_LOWER_WIDTH)
            grade_desc = tiny_blob(f"old-{character}-lifted-grade", grade, OLD_GRADE_WIDTH)
            item["lower_basis_blob"] = low_desc; item["lifted_grade_blob"] = grade_desc
            tiny_old_pins.append((low_desc, grade_desc)); old_blocks.append(item)
        globals()["OLD_BLOB_PINS"] = tuple(tiny_old_pins)
        tiny_new_pins = []
        for character, rank in enumerate(NEW_RANKS):
            rows = rng.integers(0, 3, size=(rank, NEW_BASIS_WIDTH), dtype=np.uint8)
            if rank:
                global_row = 1 + sum(NEW_RANKS[:character])
                begin = 4 * SOURCE0C + character * SOURCE1C
                tiny_dense_lower[global_row, begin:begin + SOURCE1C] = rows[0]
            tiny_new_pins.append(tiny_blob(f"block-{character}-basis", rows, NEW_BASIS_WIDTH))
        globals()["NEW_BLOB_PINS"] = tuple(tiny_new_pins)
        expected_lower = np.asarray([[ARITH.dot_mod3(row, covector) for covector in tiny_covectors]
                                     for row in tiny_dense_lower], dtype=np.uint8)
        require(int(expected_lower[0, 0]) == 1, "checker_tiny_nonzero_cross_character_control")
        prepare = {"schema": "d972.r07.a0.first-rung-grade1.v3.state", "phase": "prepare",
                   "parent_sha256": None, "old_blocks": old_blocks,
                   "defect_origins": [0] * TASK554_ORIGINS, "packets": [[], [], [], []]}
        prepare_raw = canonical(prepare); prepare_hash = sha(prepare_raw); block_bodies = []
        for character, rank in enumerate(NEW_RANKS):
            if rank:
                reductions = [[[0, 1 if index % 2 == 0 else 2]] for index in range(TASK554_ORIGINS)]
                transitions = [[[[0, 1]], [[0, 2]], [[0, 1]], [[0, 2]]]]
                nodes = [{"pivot": 0, "lead": 0, "scale": 1, "reductions": [[0, 1]]}]
                leads = [0]
            else:
                reductions = [[] for _ in range(TASK554_ORIGINS)]; transitions = []; nodes = []; leads = []
            block_bodies.append({"schema": "d972.r07.a0.first-rung-grade1.v3.state", "phase": "block",
                                 "parent_sha256": prepare_hash, "character_index": character,
                                 "character": list(CHARACTERS[character]), "rank": rank,
                                 "origin_count": TASK554_ORIGINS, "attempts": TASK554_ORIGINS + 4 * rank,
                                 "actor_order": list(ACTORS), "queue_exhausted": True,
                                 "origin_reductions": reductions, "actor_transitions": transitions,
                                 "dag_nodes": nodes, "pivot_leads": leads,
                                 "dag_sha256": sha(canonical(nodes)),
                                 "basis_blob": NEW_BLOB_PINS[character]})
        body_values = [prepare] + block_bodies; body_raws = [canonical(value) for value in body_values]
        body_hashes = tuple(sha(raw) for raw in body_raws); globals()["TASK554_BODY_DIGESTS"] = body_hashes

        def write_state(root: Path, index: int, body_raw: bytes, body_hash: str) -> dict[str, Any]:
            stem = "prepare" if index == -1 else "block-" + str(index)
            head_value = {"body_sha256": body_hash,
                          "parent_sha256": None if index == -1 else body_hashes[0],
                          "schema": "d972.r07.a0.first-rung-grade1.v3.state.head", "stem": stem}
            head_raw = canonical(head_value); (root / (stem + ".HEAD")).write_bytes(head_raw)
            body_name = stem + "." + body_hash + ".json"; (root / body_name).write_bytes(body_raw)
            head_desc = {"file": stem + ".HEAD", "bytes": len(head_raw), "sha256": sha(head_raw)}
            body_desc = {"file": body_name, "bytes": len(body_raw), "sha256": body_hash}
            blobs = ([item for pair in OLD_BLOB_PINS for item in pair] if index == -1
                     else [NEW_BLOB_PINS[index]])
            for item in blobs:
                (root / item["file"]).write_bytes(tiny_payloads[item["file"]])
            return {"root": str(root), "head": head_desc, "body": body_desc,
                    "files": [head_desc, body_desc] +
                    [_checker_blob_file_receipt(item) for item in blobs]}

        with tempfile.TemporaryDirectory(prefix="d972-r07-task913-checker-accumulator-") as temp:
            root = Path(temp); descriptors = [write_state(root, -1, body_raws[0], body_hashes[0])]
            descriptors.extend(write_state(root, index, body_raws[index + 1], body_hashes[index + 1])
                               for index in range(4))
            values = [np.asarray(item, dtype=np.uint8) for item in (
                [1, 2, 0], [0, 1, 2], [2, 0, 1], [1, 1, 0], [2, 2, 1])]
            direct = [index % 3 for index in range(44)]
            got = accumulate_scalars({"prepare": descriptors[0], "blocks": descriptors[1:]},
                                     0, direct, values, tiny_covectors)
            expected_seeds = np.asarray(direct, dtype=np.uint8)
            expected_actors = np.asarray(
                (np.column_stack(values[1:]).astype(np.uint16) +
                 expected_lower.astype(np.uint16)) % 3, dtype=np.uint8)

            def direct_sub(accumulator: int, expression: list[list[int]], bound: int,
                           offset: int) -> int:
                _expr(expression, bound, "checker_selftest_direct_relation")
                return (int(accumulator) - sum(int(coef) * int(values[0][offset + int(index)])
                                               for index, coef in expression)) % 3

            old_offsets = [0, 1, 1, 1]; new_offsets = [1, 1, 2, 3]
            for seed in range(44):
                for source, old in enumerate(old_blocks):
                    expected_seeds[seed] = direct_sub(expected_seeds[seed],
                        old["record"]["seed_reductions"][seed], OLD_RANKS[source], old_offsets[source])
            for source, old in enumerate(old_blocks):
                for pivot in range(OLD_RANKS[source]):
                    global_row = old_offsets[source] + pivot
                    for slot in range(4):
                        expected_actors[global_row, slot] = direct_sub(
                            expected_actors[global_row, slot], old["record"]["actor_transitions"][pivot][slot],
                            OLD_RANKS[source], old_offsets[source])
            for target, body in enumerate(block_bodies):
                rank = NEW_RANKS[target]; offset = new_offsets[target]
                for seed in range(44):
                    for source in range(4):
                        expected_seeds[seed] = direct_sub(
                            expected_seeds[seed], body["origin_reductions"][ORIGIN_RANGES[source][0] + seed],
                            rank, offset)
                for source, old in enumerate(old_blocks):
                    for pivot in range(OLD_RANKS[source]):
                        for slot in range(4):
                            origin = ORIGIN_RANGES[source][0] + 44 + 4 * pivot + slot
                            expected_actors[old_offsets[source] + pivot, slot] = direct_sub(
                                expected_actors[old_offsets[source] + pivot, slot],
                                body["origin_reductions"][origin], rank, offset)
                for local, row_value in enumerate(body["actor_transitions"]):
                    for slot in range(4):
                        expected_actors[offset + local, slot] = direct_sub(
                            expected_actors[offset + local, slot], row_value[slot], rank, offset)
            require(np.array_equal(got["seed_values"], expected_seeds) and
                    np.array_equal(got["actor_values"], expected_actors) and
                    np.array_equal(got["lower_values"], expected_lower) and
                    len(got["lower_blob_receipts"]) == 12 and
                    got["accumulator_count"] == 56, "checker_two_block_accumulator")
            tiny_accumulator_control = True
    finally:
        globals().update(saved_accumulator)

    fake = {"schema": ARITH.LIVE_SCHEMA + ".RawDual", "separator_generation": 0,
            "separator_s_head_sha256": "0" * 64, "lambda_sha256": "0" * 64,
            "character": 0, "B_adj_table_identity": "B:x", "word_node": {"kind": "root"},
            "actor_table_identities_along_w": [], "raw_q_packed_sha256": "0" * 64,
            "raw_q_packed_offset": 0, "raw_q_packed_length": SOURCE_WIDTH // 4,
            "raw_predecessor_sha256": None}
    fake["sha256"] = sha(canonical({k: v for k, v in fake.items() if k != "sha256"}))
    scan_values = [np.zeros(P1_ROWS, dtype=np.uint8) for _ in range(5)]
    scan_cache = {"manifest_sha256": "2" * 64, "values": scan_values}
    eof_accumulator = {"seed_values": np.zeros(44, dtype=np.uint8),
                       "actor_values": np.zeros((P1_ROWS, 4), dtype=np.uint8),
                       "relation_sha256": "3" * 64, "filtered_direct_receipt_sha256": "5" * 64}
    eof_record = _scan_accumulated(fake, eof_accumulator, scan_cache)
    require(eof_record["schema"].endswith("ScalarEOF") and eof_record["origins"] == SCALAR_ORIGINS and
            sealed_object(eof_record), "checker_full_scalar_eof")
    seed_accumulator = {"seed_values": np.zeros(44, dtype=np.uint8),
                        "actor_values": np.zeros((P1_ROWS, 4), dtype=np.uint8),
                        "relation_sha256": "3" * 64, "filtered_direct_receipt_sha256": "5" * 64}
    seed_accumulator["seed_values"][0] = 1
    seed_record = _scan_accumulated(fake, seed_accumulator, scan_cache)
    require(seed_record["schema"].endswith("Violation") and seed_record["origin_id"] == 0 and
            seed_record["origin_kind"] == "seed" and seed_record["seed"] == 0,
            "checker_seed_first")
    actor_accumulator = {"seed_values": np.zeros(44, dtype=np.uint8),
                         "actor_values": np.zeros((P1_ROWS, 4), dtype=np.uint8),
                         "relation_sha256": "3" * 64, "filtered_direct_receipt_sha256": "5" * 64}
    actor_accumulator["actor_values"][0, 0] = 1
    actor_record = _scan_accumulated(fake, actor_accumulator, scan_cache)
    require(actor_record["schema"].endswith("Violation") and actor_record["origin_id"] == 44 and
            actor_record["origin_kind"] == "actor" and actor_record["basis_i"] == 0 and
            actor_record["actor"] == ACTORS[0], "checker_actor_first")

    zero_table = {"identity": {"adjoint:B": "B:tiny"}}
    zero_separator = {"generation": 0, "lambda_sha256": "0" * 64}
    zero_vectors = [[np.zeros(SOURCE_WIDTH, dtype=np.uint8) for _ in range(5)] for _ in range(4)]
    zero_records = [_expected_character(character, zero_table, zero_vectors[character], zero_separator,
                                        {}, {}, zero_vectors[character]) for character in range(4)]
    require(all(item["schema"].endswith("RootZero") for item in zero_records), "checker_zero_root")
    require(terminal_kind(zero_records) == "AllFourRootEOF", "checker_all_four_root_eof")

    # Task554 preserves insertion order.  Syntax validation therefore accepts
    # unsorted, unique terms and rejects only malformed/duplicate entries.
    _expr([[2, 2], [0, 1]], 3, "checker_relation_unsorted")
    for bad_expression, label in (
            ([[2, 2], [2, 1]], "checker_relation_duplicate"),
            ([[3, 1]], "checker_relation_out_of_range"),
            ([[0, 0]], "checker_relation_coefficient")):
        _expect_reject(lambda bad=bad_expression: _expr(
            bad, 3, "checker_relation_invalid"), label)

    # The exact Task554 body receipt still authenticates term order.  A
    # semantically equivalent reordering is rejected at that boundary, rather
    # than by the expression syntax validator above.
    relation_order_control = False
    with tempfile.TemporaryDirectory(prefix="d972-r07-task917-body-") as temp:
        body_path = Path(temp) / "task554-body.json"
        body = {"schema": "task554-order-fixture", "origin_reductions": [[2, 2], [0, 1]]}
        body_raw = canonical(body); body_sha = sha(body_raw)
        body_path.write_bytes(body_raw)
        read_json_stream(body_path, len(body_raw), body_sha)
        reordered_raw = canonical({"schema": body["schema"],
                                   "origin_reductions": [[0, 1], [2, 2]]})
        require(len(reordered_raw) == len(body_raw), "checker_relation_order_fixture_size")
        body_path.write_bytes(reordered_raw)
        _expect_reject(lambda: read_json_stream(body_path, len(body_raw), body_sha),
                       "checker_task554_body_order_digest_control")
        relation_order_control = True

    # The same exact-record validator used by check_output must reject
    # coherently resealed relation, child and scalar-prefix changes.
    character_expected = {"schema": SCHEMA + ".RootScalarEOF", "character": 0,
                          "children": [{"actor": ACTORS[0], "packed_sha256": "a" * 64}],
                          "relation_stream_sha256": "b" * 64, "scalar": eof_record}
    character_expected["sha256"] = sha(canonical(character_expected))
    validate_character_record(character_expected, character_expected)
    bad_relation = json.loads(json.dumps(character_expected)); bad_relation["relation_stream_sha256"] = "c" * 64
    bad_relation["sha256"] = sha(canonical({k: v for k, v in bad_relation.items() if k != "sha256"}))
    _expect_reject(lambda: validate_character_record(bad_relation, character_expected),
                   "checker_relation_reseal_control")
    bad_child = json.loads(json.dumps(character_expected)); bad_child["children"][0]["packed_sha256"] = "d" * 64
    bad_child["sha256"] = sha(canonical({k: v for k, v in bad_child.items() if k != "sha256"}))
    _expect_reject(lambda: validate_character_record(bad_child, character_expected),
                   "checker_child_reseal_control")
    bad_prefix = json.loads(json.dumps(character_expected)); bad_prefix["scalar"]["rolling_scalar_head"] = "e" * 64
    bad_prefix["scalar"]["sha256"] = sha(canonical({k: v for k, v in bad_prefix["scalar"].items() if k != "sha256"}))
    bad_prefix["sha256"] = sha(canonical({k: v for k, v in bad_prefix.items() if k != "sha256"}))
    _expect_reject(lambda: validate_character_record(bad_prefix, character_expected),
                   "checker_prefix_reseal_control")

    # Exercise the exact terminal/result/manifest join helper with a
    # coherently resealed upper claim and each authenticated parent join.
    terminal_body = {"schema": SCHEMA + ".terminal", "terminal": "AllFourRootEOF",
                     "claim": "candidate", "verified": False}
    expected_terminal = {**terminal_body, "sha256": sha(canonical(terminal_body))}
    result_body = {"schema": SCHEMA + ".result", "launch_sha256": "1" * 64,
                   "separator_manifest_sha256": "2" * 64, "p1_manifest_sha256": "3" * 64,
                   "task712_manifest_sha256": ["4" * 64] * 4}
    expected_result = {**result_body, "sha256": sha(canonical(result_body))}
    manifest_body = {"schema": SCHEMA + ".output-manifest", "terminal": "AllFourRootEOF",
                     "candidate": True, "verified": False}
    expected_manifest = {**manifest_body, "sha256": sha(canonical(manifest_body))}
    validate_output_objects(expected_terminal, expected_result, expected_manifest,
                            expected_terminal, expected_result, expected_manifest)
    bad_terminal = dict(expected_terminal); bad_terminal["claim"] = "GRADE2_MEMBER";
    bad_terminal["sha256"] = sha(canonical({k: v for k, v in bad_terminal.items() if k != "sha256"}))
    _expect_reject(lambda: validate_output_objects(bad_terminal, expected_result, expected_manifest,
                                                   expected_terminal, expected_result, expected_manifest),
                   "checker_terminal_claim_control")
    for field, altered in (("launch_sha256", "9" * 64),
                           ("separator_manifest_sha256", "8" * 64),
                           ("p1_manifest_sha256", "7" * 64),
                           ("task712_manifest_sha256", ["6" * 64] * 4)):
        bad_result = dict(expected_result); bad_result[field] = altered
        bad_result["sha256"] = sha(canonical({k: v for k, v in bad_result.items() if k != "sha256"}))
        _expect_reject(lambda bad_result=bad_result: validate_output_objects(
            expected_terminal, bad_result, expected_manifest,
            expected_terminal, expected_result, expected_manifest),
            "checker_result_join_control")
    bad_manifest = dict(expected_manifest); bad_manifest["terminal"] = "RootViolationBatch"
    bad_manifest["sha256"] = sha(canonical({k: v for k, v in bad_manifest.items() if k != "sha256"}))
    _expect_reject(lambda: validate_output_objects(expected_terminal, expected_result, bad_manifest,
                                                   expected_terminal, expected_result, expected_manifest),
                   "checker_manifest_join_control")

    # Exercise the actual canonical launch handoff.  The parent validators are
    # replaced only inside this bounded test so no real parent is opened; the
    # launch file itself still goes through validate_launch and its exact
    # source/claim/shape checks.
    launch_handoff_control = False
    saved_validators = (validate_separator, validate_p1, validate_task554)
    try:
        globals()["validate_separator"] = lambda value: {}
        globals()["validate_p1"] = lambda value: {}
        globals()["validate_task554"] = lambda value: {}
        with tempfile.TemporaryDirectory(prefix="d972-r07-task915-launch-") as temp:
            root = Path(temp)
            task712 = [dict(TASK712_PARENT, root=str(root / ("task712-" + str(index))))
                       for index in range(4)]
            launch = {"schema": SCHEMA + ".launch.v1", "fixture_only": False, "mode": "actual",
                      "characters": [list(item) for item in CHARACTERS], "actors": list(ACTORS),
                      "p1_parent": {}, "task554_parent": {}, "task712_parents": task712,
                      "separator_parent": {}, "out": str(root / "out"), "claims": launch_claims(),
                      "source_pin": {"producer": {"path": PRODUCER_ARITH_PATH.as_posix(),
                                                    "sha256": PRODUCER_ARITH_SHA256},
                                     "checker": {"path": ARITH_PATH.as_posix(),
                                                 "sha256": ARITH_SHA256}}}
            launch_path = root / "launch.json"; launch_raw = canonical(launch)
            launch_path.write_bytes(launch_raw)
            checked, authenticated_raw = validate_launch(launch_path)
            require(authenticated_raw == launch_raw and
                    checked["launch_sha256"] == sha(authenticated_raw),
                    "selftest_launch_sha_handoff")
            launch_handoff_control = True
    finally:
        globals().update({"validate_separator": saved_validators[0],
                          "validate_p1": saved_validators[1],
                          "validate_task554": saved_validators[2]})

    return {"schema": SCHEMA + ".checker-selftest", "status": "PASS", "sparse_offsets": 4,
            "simultaneous_values": 20, "vectorized_chunk_dense_crosscheck": True,
            "offset_four_slot_control": tiny_accumulator_control,
            "two_block_accumulator": tiny_accumulator_control,
            "full_scalar_eof_32280": True, "seed_first_violation": 0,
            "actor_first_violation": "basis_i/actor", "all_four_root_eof": True,
            "zero_root": True, "separator_mutation_rejected": separator_control,
            "task712_transpose_mutation_rejected": table_control,
            "p1_truncation_digest_mutation_rejected": p1_control,
            "task554_relation_order_mutation_rejected": relation_order_control,
            "result_q_child_scalar_prefix_resealing_rejected": True,
            "terminal_claim_and_parent_join_rejected": True,
            "launch_sha256_handoff": launch_handoff_control,
            "dense_all_row_matrix": False, "verified": False}


def checker_v541_selftest(context: Any, words: dict[str, Any]) -> dict[str, Any]:
    """Small full-action comparisons for the repaired filtered scalar only."""
    rng = np.random.default_rng(541922)
    mixed = (rng.integers(0, 3, (4, SOURCE0C), dtype=np.uint8),
             rng.integers(0, 3, (4, SOURCE1C), dtype=np.uint8),
             rng.integers(0, 3, (4, SOURCE_WIDTH), dtype=np.uint8),
             rng.integers(0, 3, 8, dtype=np.uint8))
    flat_lower = np.concatenate((mixed[0].reshape(-1), mixed[1].reshape(-1), mixed[3]))
    q = rng.integers(0, 3, SOURCE_WIDTH, dtype=np.uint8)
    controls = 0; chosen = None
    for character in range(4):
        for actor in ACTORS:
            lower, top = checker_actor_adjoint(context, q, character, actor)
            acted = ARITH._checker_seed_act(context, mixed, checker_actor_tags(context, actor))
            actual = ARITH.dot_mod3(q, acted[2][character])
            expected = (ARITH.dot_mod3(lower, flat_lower) +
                        ARITH.dot_mod3(top, mixed[2][character])) % 3
            require(actual == expected, "checker_v541_full_mixed_adjoint")
            require(not np.any(lower[-8:]), "checker_v541_auxiliary_zero")
            controls += 1
            if chosen is None and character == 0 and np.count_nonzero(lower):
                chosen = (actor, lower, top)
    require(chosen is not None, "checker_v541_nonzero_lower_exists")
    actor, lower, top = chosen
    index = int(np.flatnonzero(lower)[0])
    unit = np.zeros(LOWER_WIDTH, dtype=np.uint8); unit[index] = 1
    lower_only = (unit[:4 * SOURCE0C].reshape(4, SOURCE0C),
                  unit[4 * SOURCE0C:4 * SOURCE0C + 4 * SOURCE1C].reshape(4, SOURCE1C),
                  np.zeros((4, SOURCE_WIDTH), dtype=np.uint8), unit[-8:])
    known = ARITH._checker_seed_act(context, lower_only, checker_actor_tags(context, actor))
    known_scalar = ARITH.dot_mod3(q, known[2][0])
    require(known_scalar == int(lower[index]) and known_scalar != 0,
            "checker_v541_known_nonzero_lower")
    pure_top = (np.zeros_like(mixed[0]), np.zeros_like(mixed[1]),
                mixed[2].copy(), np.zeros(8, dtype=np.uint8))
    pure_acted = ARITH._checker_seed_act(context, pure_top, checker_actor_tags(context, actor))
    require(ARITH.dot_mod3(q, pure_acted[2][0]) == ARITH.dot_mod3(top, mixed[2][0]),
            "checker_v541_full_pure_top_adjoint")
    # A two-row reconstruction tests the complete FULL-defect subtraction.
    row = (lower_only[0], lower_only[1], mixed[2], lower_only[3])
    acted = ARITH._checker_seed_act(context, row, checker_actor_tags(context, actor))
    reconstructed = (2 * mixed[2][0].astype(np.int16) +
                     mixed[2][1].astype(np.int16)) % 3
    full_defect_top = np.asarray((acted[2][0].astype(np.int16) - reconstructed) % 3,
                                dtype=np.uint8)
    scalar = (ARITH.dot_mod3(top, row[2][0]) + ARITH.dot_mod3(lower, unit) -
              2 * ARITH.dot_mod3(q, mixed[2][0]) -
              ARITH.dot_mod3(q, mixed[2][1])) % 3
    require(scalar == ARITH.dot_mod3(q, full_defect_top),
            "checker_v541_full_defect_scalar")
    require((scalar - known_scalar) % 3 != scalar,
            "checker_v541_omitted_lower_negative_control")
    seed = ARITH._checker_seed_evaluate_seed(
        context, tuple(int(letter) for letter in words["relators"][2]))
    projected = ARITH._checker_seed_full_project(context, seed, CHARACTERS[0])
    delta = np.asarray((seed[2][0].astype(np.int16) -
                        projected[2][0].astype(np.int16)) % 3, dtype=np.uint8)
    require(sha(ARITH.pack_trits(seed[2][0])) == SEED2_RAW_PACKED_SHA256 and
            sha(ARITH.pack_trits(delta)) == SEED2_DIFFERENCE_PACKED_SHA256,
            "checker_v541_seed2_row_identity")
    delta_index = int(np.flatnonzero(delta)[0])
    seed_q = np.zeros(SOURCE_WIDTH, dtype=np.uint8); seed_q[delta_index] = 1
    raw_direct = checker_raw_seed_direct(context, words, seed_q, 0)
    reconstruction = ARITH.dot_mod3(seed_q, seed[2][0])
    correct_seed_scalar = (raw_direct["values"][2] - reconstruction) % 3
    wrong_seed_scalar = (ARITH.dot_mod3(seed_q, projected[2][0]) - reconstruction) % 3
    require(correct_seed_scalar == 0 and wrong_seed_scalar != 0,
            "checker_v541_one_sided_projector_negative_control")
    filtered = {"schema": SCHEMA + ".filtered-direct.v541", "formula_id": V541_FORMULA_ID,
                "actor_direct_includes_lower_to_top": True,
                "saved_arrays": [{"file": "seed-scalars-a0.bin", "bytes": 44,
                                  "sha256": sha(bytes(44))}]}
    filtered["sha256"] = sha(canonical(filtered))
    record = {"schema": SCHEMA + ".RootViolation", "filtered_direct": filtered}
    record["sha256"] = sha(canonical(record))
    validate_character_record(record, record)
    forged = json.loads(json.dumps(record))
    forged["filtered_direct"]["actor_direct_includes_lower_to_top"] = False
    forged["filtered_direct"]["sha256"] = sha(canonical(
        {key: value for key, value in forged["filtered_direct"].items() if key != "sha256"}))
    forged["sha256"] = sha(canonical({key: value for key, value in forged.items() if key != "sha256"}))
    _expect_reject(lambda: validate_character_record(forged, record),
                   "checker_v541_resealed_filtered_control")
    return {"status": "PASS", "formula_id": V541_FORMULA_ID,
            "mixed_full_actor_comparisons": controls, "known_lower_scalar": known_scalar,
            "lower_only_and_pure_top": True, "full_defect_scalar": True,
            "omitted_lower_rejected": True, "one_sided_projector_rejected": True,
            "repaired_receipt_resealing_rejected": True, "verified": False}


def checker_actual_canary(path: Path, context: Any, words: dict[str, Any]) -> dict[str, Any]:
    """Use actual q and four P1 slices, never the all-row scalar production pass."""
    base, _ = validate_launch(path)
    tables, vectors = covectors(base["separator"], base["task712"])
    q = vectors[0][0]
    raw = ARITH._checker_seed_evaluate_seed(
        context, tuple(int(letter) for letter in words["relators"][2]))
    projected = ARITH._checker_seed_full_project(context, raw, CHARACTERS[0])
    difference = np.asarray((raw[2][0].astype(np.int16) -
                             projected[2][0].astype(np.int16)) % 3, dtype=np.uint8)
    packed_rows = [ARITH.pack_trits(item) for item in (raw[2][0], projected[2][0], difference)]
    require([sha(item) for item in packed_rows] ==
            [SEED2_RAW_PACKED_SHA256, SEED2_PROJECTED_PACKED_SHA256,
             SEED2_DIFFERENCE_PACKED_SHA256], "checker_canary_seed2_packed_pins")
    pairings = [ARITH.dot_mod3(q, item) for item in (raw[2][0], projected[2][0], difference)]
    require(pairings == [0, 1, 2], "checker_canary_seed2_pairings")
    cache = safe_path(base["p1"]["root"], base["p1"]["cache"]["path"])
    require(cache.stat().st_size == P1_CACHE_BYTES, "checker_canary_p1_cache_size")
    reconstructed = 0
    with cache.open("rb") as stream:
        for (node, coefficient), wanted_sha in zip(SEED2_REDUCTION, SEED2_P1_A0_SHA256):
            stream.seek(node * P1_ROW_BYTES)
            packed = stream.read(SLICE_BYTES)
            require(len(packed) == SLICE_BYTES and sha(packed) == wanted_sha,
                    "checker_canary_p1_selected_slice")
            reconstructed = (reconstructed + coefficient *
                             ARITH.dot_mod3(q, ARITH.unpack_trits(packed, SOURCE_WIDTH))) % 3
    require((pairings[0] - reconstructed) % 3 == 0,
            "checker_canary_actual_seed2_corrected")
    _, covector_receipt = checker_actor_adjoints(context, q, 0, vectors[0][1:])
    return {"schema": SCHEMA + ".actual-canary.v541", "status": "PASS",
            "formula_id": V541_FORMULA_ID, "seed": 2,
            "raw_projected_difference_pairings": pairings,
            "corrected_seed_scalar": 0, "p1_selected_slices": 4,
            "task712_pure_top_match": True,
            "actor_covector_receipt_sha256": covector_receipt["sha256"],
            "all_row_scalar_scan_executed": False, "verified": False}


def parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__); group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--selftest", action="store_true"); group.add_argument("--check-launch", type=Path)
    parser.add_argument("--actual-canary-launch", type=Path)
    return parser


def check_actual(path: Path) -> dict[str, Any]:
    base, _ = validate_launch(path); tables, vectors = covectors(base["separator"], base["task712"])
    values = p1_values(base["p1"], vectors)
    return check_output(base, tables, vectors, values)


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        if args.selftest:
            result = selftest()
            context, words = checker_source_context()
            result["v541"] = checker_v541_selftest(context, words)
            if args.actual_canary_launch is not None:
                result["actual_canary"] = checker_actual_canary(args.actual_canary_launch, context, words)
            print(json.dumps(result, sort_keys=True)); return 0
        require(args.actual_canary_launch is None, "checker_canary_requires_selftest")
        print(json.dumps(check_actual(args.check_launch), sort_keys=True)); return 0
    except Exception as exc:
        print(json.dumps({"status": "REJECTED", "error": str(exc), "verified": False}, sort_keys=True),
              file=sys.stderr); return 1


if __name__ == "__main__":
    raise SystemExit(main())
