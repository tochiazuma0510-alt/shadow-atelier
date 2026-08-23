#!/usr/bin/env python3
"""Independent phase-2 branch-accounting checker for Sol campaign 159b.

This checker uses only Python's standard library and imports no search/producer
module.  It deliberately separates three statements:

* VERSION-PIN and registry bytes are intact;
* the reported 162 = 144 + 18 and 18 = 8 + 10 accountings are exact;
* the mathematical non-membership decisions and the nonzero-roof kappa
  formula are *not* independently certified by those receipts alone.

The raw q3 models are nevertheless sufficient to reconstruct a deterministic
literal target-6 word/gradient canary for every (roof, correction) pair.  The
bulk/prodrung receipts contain no matching per-branch word or gradient digest,
so these reconstructed canaries are emitted as an unbound handoff, not used to
promote the eight reported j=5 outcomes.
"""

from __future__ import annotations

import argparse
import base64
import copy
import hashlib
import itertools
import json
import re
import sys
from pathlib import Path
from typing import Any, Iterable, Sequence


PIN_REL = "search/certs/sol159b_version_pin_v1_20260823.json"
PIN_BYTES = 6259
PIN_SHA256 = "d9a92f265ae21fabc79a944670dae136e5e9c06260e0b9d2c11f6acfde62ca36"

Q3_REL = "ci/b345_157en_artifacts_32458556448/d972_b345_q3_chief_v1.json"
Q3_BYTES = 231570
Q3_SHA256 = "3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72"

BULK_REL = "search/certs/koubou158_L3_bulk162_v1_2_20260822.json"
BULK_BYTES = 45007
BULK_SHA256 = "6e51df539aa4cf793c7302514cf1f068e098c06ca751571890da09ba7fd13172"

PROD_REL = "search/certs/koubou158_prodrung_v1_20260822.json"
PROD_RESUME_SOURCE_REL = "search/koubou158_prodrung_j5_resume_v1.py"
M2_RUNTIME_CORE_REL = "search/koubou158_L3_core_v1_1.py"
M2_RUNTIME_BFS_REL = "search/koubou158_L3_core_completebfs_v1.py"
PROD_BYTES = 15391
PROD_SHA256 = "3160eec7281ecaaa38e4f869530b5fb7639620e7363c9abde5acb0990638cafe"

REGISTRY_REL = (
    "ci/b345_157ee_artifacts_32359956713/"
    "d972_b345_joint_kernel_qstar_closure_v1.json"
)
TARGET_REL = (
    "ci/b345_157en_artifacts_32458556448/"
    "d972_b345_target6_dual_colgen_v2.json"
)

EXPECTED_L3_INCONCLUSIVE = (
    "r0_c8", "r0_c13", "r0_c18",
    "r1_c2", "r1_c17", "r1_c23",
    "r2_c2", "r2_c15", "r2_c22",
    "r3_c2", "r3_c16", "r3_c21",
    "r4_c1", "r4_c16", "r4_c22",
    "r5_c3", "r5_c10", "r5_c26",
)
EXPECTED_J5_REPORTED_DEAD = (
    "r0_c13", "r0_c18", "r1_c17", "r2_c15",
    "r3_c2", "r3_c21", "r4_c22", "r5_c10",
)
EXPECTED_J5_UNDECIDED = (
    "r0_c8", "r1_c2", "r1_c23", "r2_c2", "r2_c22",
    "r3_c16", "r4_c1", "r4_c16", "r5_c3", "r5_c26",
)
BRANCH_RE = re.compile(r"^r([0-5])_c(0|[1-9]|1[0-9]|2[0-6])$")


class CheckError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise CheckError(message)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def digest_obj(value: Any) -> str:
    return sha256_bytes(canonical_bytes(value))


def _reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        if key in out:
            raise CheckError(f"duplicate JSON key: {key!r}")
        out[key] = value
    return out


def _reject_constant(value: str) -> None:
    raise CheckError(f"non-finite JSON constant: {value}")


def load_json_exact(
    path: Path, *, expected_bytes: int | None = None,
    expected_sha256: str | None = None, display_path: str | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    raw = path.read_bytes()
    actual_sha = sha256_bytes(raw)
    if expected_bytes is not None:
        require(len(raw) == expected_bytes, f"byte count mismatch: {path}")
    if expected_sha256 is not None:
        require(actual_sha == expected_sha256, f"SHA256 mismatch: {path}")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise CheckError(f"not UTF-8: {path}") from exc
    try:
        value = json.loads(
            text,
            object_pairs_hook=_reject_duplicate_keys,
            parse_constant=_reject_constant,
        )
    except (json.JSONDecodeError, TypeError) as exc:
        raise CheckError(f"invalid JSON: {path}: {exc}") from exc
    require(isinstance(value, dict), f"top-level JSON is not an object: {path}")
    return value, {
        "path": display_path if display_path is not None else path.as_posix(),
        "bytes": len(raw),
        "sha256": actual_sha,
    }


def validate_word(word: Any, alphabet: set[int], label: str) -> tuple[int, ...]:
    require(isinstance(word, list), f"{label}: word is not a list")
    require(all(type(x) is int and x in alphabet for x in word),
            f"{label}: illegal letter")
    return tuple(word)


def inverse_word(word: Sequence[int]) -> tuple[int, ...]:
    return tuple(-x for x in reversed(word))


def reduce_word(word: Iterable[int]) -> tuple[int, ...]:
    stack: list[int] = []
    for letter in word:
        if stack and stack[-1] == -letter:
            stack.pop()
        else:
            stack.append(letter)
    return tuple(stack)


def substitute_f2(
    word: Sequence[int], left: Sequence[int], right: Sequence[int]
) -> tuple[int, ...]:
    roots = {
        1: tuple(left), -1: inverse_word(left),
        2: tuple(right), -2: inverse_word(right),
    }
    return reduce_word(itertools.chain.from_iterable(roots[x] for x in word))


class PermModel:
    """One-based permutation rows with the pinned multiplication b[a[i]]."""

    def __init__(self, marked: Any, degree: int, label: str):
        require(isinstance(marked, list) and marked, f"{label}: no generators")
        self.degree = degree
        self.identity = tuple(range(1, degree + 1))
        self.marked: list[tuple[int, ...]] = []
        for pos, row in enumerate(marked):
            require(isinstance(row, list) and len(row) == degree,
                    f"{label}: bad permutation width at {pos}")
            perm = tuple(row)
            require(set(perm) == set(self.identity),
                    f"{label}: invalid permutation at {pos}")
            self.marked.append(perm)

    @staticmethod
    def mul(a: Sequence[int], b: Sequence[int]) -> tuple[int, ...]:
        return tuple(b[x - 1] for x in a)

    def inv(self, a: Sequence[int]) -> tuple[int, ...]:
        out = [0] * self.degree
        for source, target in enumerate(a, start=1):
            out[target - 1] = source
        return tuple(out)

    def eval(self, word: Sequence[int], roots: Sequence[int] | None = None) -> tuple[int, ...]:
        if roots is None:
            roots = tuple(range(1, len(self.marked) + 1))
        current = self.identity
        for letter in word:
            root = roots[abs(letter) - 1]
            gen = self.marked[root - 1]
            if letter < 0:
                gen = self.inv(gen)
            current = self.mul(current, gen)
        return current


class PcModel:
    """Independent collector for the class-2 exponent-3 pc data in q3."""

    def __init__(self, record: dict[str, Any], label: str):
        self.label = label
        self.n = record.get("generator_count")
        require(type(self.n) is int and self.n > 0, f"{label}: generator_count")
        orders = record.get("relative_orders")
        require(orders == [3] * self.n, f"{label}: expected exponent-three pcgs")
        powers = record.get("power_relations")
        require(powers == [[0] * self.n for _ in range(self.n)],
                f"{label}: nontrivial power relation unsupported")
        inverses = record.get("inverses")
        require(isinstance(inverses, list) and len(inverses) == self.n,
                f"{label}: inverse table")
        self.inverses = [self._coords(row, "inverse") for row in inverses]
        self.conj: dict[tuple[int, int], tuple[int, ...]] = {}
        rows = record.get("conjugate_relations")
        require(isinstance(rows, list) and len(rows) == self.n * (self.n - 1) // 2,
                f"{label}: conjugate table size")
        for row in rows:
            i, j = row.get("i"), row.get("j")
            require(type(i) is int and type(j) is int and 1 <= j < i <= self.n,
                    f"{label}: conjugate indices")
            coords = self._coords(row.get("coords"), "conjugate")
            require(all(coords[k] == 0 for k in range(i - 1)) and coords[i - 1] == 1,
                    f"{label}: non-triangular conjugate row {(i, j)}")
            self.conj[(i, j)] = coords
        require(len(self.conj) == len(rows), f"{label}: duplicate conjugate row")
        self.inverse_conj = {
            (row["i"], row["j"]): self._coords(row["coords"], "inverse conjugate")
            for row in record.get("inverse_conjugate_relations", [])
        }
        require(set(self.inverse_conj) == set(self.conj),
                f"{label}: inverse-conjugate table coverage")
        marked = record.get("marked_generators")
        require(isinstance(marked, list) and marked, f"{label}: marked generators")
        self.marked: list[tuple[int, ...]] = []
        self.marked_inverse: list[tuple[int, ...]] = []
        for row in marked:
            self.marked.append(self._coords(row.get("coords"), "marked"))
            self.marked_inverse.append(
                self._coords(row.get("inverse_coords"), "marked inverse")
            )
        self.identity = (0,) * self.n

    def _coords(self, value: Any, kind: str) -> tuple[int, ...]:
        require(isinstance(value, list) and len(value) == self.n,
                f"{self.label}: {kind} width")
        require(all(type(x) is int and 0 <= x < 3 for x in value),
                f"{self.label}: {kind} coordinate")
        return tuple(value)

    @staticmethod
    def expand(coords: Sequence[int]) -> list[int]:
        return [i for i, exponent in enumerate(coords, start=1) for _ in range(exponent)]

    def collect(self, letters: Sequence[int]) -> tuple[int, ...]:
        require(all(type(x) is int and 1 <= x <= self.n for x in letters),
                f"{self.label}: pc letter outside range")
        word = list(letters)
        steps = 0
        while True:
            inversion = next(
                (k for k in range(len(word) - 1) if word[k] > word[k + 1]),
                None,
            )
            if inversion is None:
                counts = [0] * self.n
                for letter in word:
                    counts[letter - 1] = (counts[letter - 1] + 1) % 3
                return tuple(counts)
            i, j = word[inversion], word[inversion + 1]
            word[inversion:inversion + 2] = [j] + self.expand(self.conj[(i, j)])
            steps += 1
            require(steps <= 2_000_000, f"{self.label}: collector did not terminate")

    def mul(self, a: Sequence[int], b: Sequence[int]) -> tuple[int, ...]:
        return self.collect(self.expand(a) + self.expand(b))

    def inv(self, a: Sequence[int]) -> tuple[int, ...]:
        current = self.identity
        for i in range(self.n, 0, -1):
            for _ in range(a[i - 1]):
                current = self.mul(current, self.inverses[i - 1])
        return current

    def eval_pc_word(self, word: Sequence[int]) -> tuple[int, ...]:
        current = self.identity
        for letter in word:
            coords = ((0,) * (abs(letter) - 1) + (1,) +
                      (0,) * (self.n - abs(letter)))
            if letter < 0:
                coords = self.inverses[abs(letter) - 1]
            current = self.mul(current, coords)
        return current

    def eval_marked(
        self, word: Sequence[int], roots: Sequence[int] | None = None
    ) -> tuple[int, ...]:
        if roots is None:
            roots = tuple(range(1, len(self.marked) + 1))
        current = self.identity
        for letter in word:
            root = roots[abs(letter) - 1]
            coords = self.marked[root - 1]
            if letter < 0:
                coords = self.marked_inverse[root - 1]
            current = self.mul(current, coords)
        return current

    def calibrate(self, record: dict[str, Any]) -> dict[str, int]:
        for i in range(1, self.n + 1):
            require(self.eval_pc_word([i, -i]) == self.identity,
                    f"{self.label}: inverse calibration {i}")
            require(self.eval_pc_word([i, i, i]) == self.identity,
                    f"{self.label}: power calibration {i}")
        for (i, j), expected in self.conj.items():
            require(self.eval_pc_word([-j, i, j]) == expected,
                    f"{self.label}: conjugate orientation {(i, j)}")
            require(self.eval_pc_word([j, i, -j]) == self.inverse_conj[(i, j)],
                    f"{self.label}: inverse conjugate orientation {(i, j)}")
        relations = record.get("original_relations")
        images = record.get("original_relator_images")
        require(isinstance(relations, list) and isinstance(images, list) and
                len(relations) == len(images), f"{self.label}: original relations")
        for ordinal, (word, expected) in enumerate(zip(relations, images)):
            require(self.eval_marked(word) == tuple(expected) == self.identity,
                    f"{self.label}: original relator {ordinal}")
        return {
            "inverse_rows": self.n,
            "conjugate_rows": len(self.conj),
            "original_relators": len(relations),
        }


def parse_branch_id(branch_id: Any) -> tuple[int, int]:
    require(isinstance(branch_id, str), "branch id is not a string")
    match = BRANCH_RE.fullmatch(branch_id)
    require(match is not None, f"noncanonical branch id: {branch_id!r}")
    return int(match.group(1)), int(match.group(2))


def universe_ids() -> tuple[str, ...]:
    return tuple(f"r{r}_c{c}" for r in range(6) for c in range(27))


def validate_pin_structure(pin: dict[str, Any]) -> None:
    require(pin.get("schema") == "sol159b-version-pin/v1", "pin schema")
    require(pin.get("status") == "VERSION_PIN_READY", "pin status")
    require(pin.get("branch") == "koubou158/m2-msweep-v5-gha", "pin branch")
    require("[fire]" not in pin["branch"], "forbidden branch marker")
    indexing = pin.get("indexing")
    require(isinstance(indexing, dict) and indexing.get("canonical") == "zero-based",
            "pin zero-based convention")
    require(indexing.get("branch_id_formula") ==
            "r{roof_index}_c{correction_index}", "pin branch formula")
    boundary = pin.get("claim_boundary")
    require(isinstance(boundary, dict) and boundary.get("mathematical_grade") == "UNKNOWN",
            "pin mathematical boundary")
    for key in (
        "bulk162_v1_2_orphan_lane_mathematically_accepted",
        "prodrung_mathematically_accepted", "M2_v3_mathematically_accepted",
        "type_M_claimed", "key_bijection_claimed", "M1_prime_claimed",
        "branch_cover_claimed",
    ):
        require(boundary.get(key) is False, f"pin boundary drift: {key}")


def validate_pin_files(repo: Path, pin: dict[str, Any]) -> dict[str, Any]:
    validate_pin_structure(pin)
    files = pin.get("files")
    require(isinstance(files, list) and len(files) == 18, "pin file count")
    seen: set[str] = set()
    checked: list[dict[str, Any]] = []
    for row in files:
        require(isinstance(row, dict), "pin file row")
        rel = row.get("path")
        require(isinstance(rel, str) and rel not in seen, "pin file path uniqueness")
        require(not Path(rel).is_absolute() and ".." not in Path(rel).parts,
                f"unsafe pin path: {rel}")
        seen.add(rel)
        raw = (repo / rel).read_bytes()
        actual = sha256_bytes(raw)
        require(len(raw) == row.get("bytes"), f"pin byte mismatch: {rel}")
        require(actual == row.get("sha256"), f"pin SHA mismatch: {rel}")
        checked.append({"path": rel, "bytes": len(raw), "sha256": actual})
    require({
        Q3_REL, BULK_REL, PROD_REL, PROD_RESUME_SOURCE_REL,
        M2_RUNTIME_CORE_REL, M2_RUNTIME_BFS_REL, REGISTRY_REL, TARGET_REL,
    }.issubset(seen),
            "pin lacks a required branch-cover input")
    return {
        "file_count": len(checked),
        "files_digest": digest_obj(checked),
        "load_bearing_prodrung_resume_source_pinned": True,
        "m2_v3_runtime_dependencies_pinned": [
            M2_RUNTIME_CORE_REL,
            M2_RUNTIME_BFS_REL,
        ],
        "manifest_expansion_reason": (
            "pin the two current M2 v3 runtime dependencies in addition to "
            "the previously pinned prodrung j5 resume source"
        ),
    }


def validate_registry(registry: dict[str, Any], pin: dict[str, Any]) -> dict[str, Any]:
    require(registry.get("schema") ==
            "d972-b345-joint-kernel-qstar-closure/v1", "registry schema")
    public = registry.get("context_registry")
    require(isinstance(public, dict), "context registry object")
    contexts = public.get("contexts")
    uses = public.get("named_uses")
    require(isinstance(contexts, list) and len(contexts) == 31,
            "context registry cardinality")
    require(isinstance(uses, list) and len(uses) == 46,
            "named-use cardinality")
    require(public.get("context_count") == 31 and public.get("named_use_count") == 46,
            "registry reported cardinalities")
    require([row.get("context_id") for row in contexts] == list(range(1, 32)),
            "context IDs are not one-based 1..31")
    for row in contexts:
        require(set(row) == {"context_id", "left_hex", "right_hex"},
                "context row schema")
        for field in ("left_hex", "right_hex"):
            try:
                blob = bytes.fromhex(row[field])
            except (TypeError, ValueError) as exc:
                raise CheckError(f"bad context blob: {field}") from exc
            require(len(blob) == 154, "context E4 blob width")
    names: set[str] = set()
    for row in uses:
        require(set(row) == {"context_id", "name"}, "named-use row schema")
        require(row["context_id"] in range(1, 32), "named-use context reference")
        require(isinstance(row["name"], str) and row["name"] not in names,
                "named-use name uniqueness")
        names.add(row["name"])
    contexts_sha = digest_obj(contexts)
    uses_sha = digest_obj(uses)
    require(contexts_sha == public.get("context_rows_sha256"),
            "context rows digest")
    require(uses_sha == public.get("named_use_mapping_sha256"),
            "named uses digest")

    gamma = registry.get("gamma")
    require(isinstance(gamma, dict) and
            gamma.get("canonical_state_key") == "E3 blob then 31 E4 blobs",
            "gamma state-key convention")
    packed = gamma.get("canonical_states")
    require(isinstance(packed, dict), "packed state table")
    widths = packed.get("factor_widths_bytes")
    require(widths == [40] + [154] * 31, "packed state factor widths")
    require(packed.get("row_width_bytes") == sum(widths), "packed row width")
    require(packed.get("state_count") == gamma.get("order") == 243,
            "packed state count")
    try:
        raw = base64.b64decode(packed.get("base64"), validate=True)
    except Exception as exc:  # binascii.Error and type errors are fail-closed
        raise CheckError("invalid packed state base64") from exc
    require(len(raw) == packed.get("byte_length") == 243 * sum(widths),
            "packed state byte length")
    require(sha256_bytes(raw) == packed.get("sha256"), "packed state byte SHA")
    rows: list[list[str]] = []
    offset = 0
    for _ in range(243):
        row: list[str] = []
        for width in widths:
            row.append(raw[offset:offset + width].hex())
            offset += width
        rows.append(row)
    state_rows_sha = digest_obj(rows)
    require(state_rows_sha == gamma.get("state_rows_sha256"),
            "packed state rows digest")

    manifest_registry = pin.get("registry_pin")
    require(isinstance(manifest_registry, dict), "manifest registry pin")
    require(manifest_registry.get("path") == REGISTRY_REL, "manifest registry path")
    require(manifest_registry.get("schema") == registry.get("schema"),
            "manifest registry schema")
    require(manifest_registry.get("context_count") == len(contexts) and
            manifest_registry.get("named_use_count") == len(uses),
            "manifest registry counts")
    require(manifest_registry.get("context_rows_sha256") == contexts_sha and
            manifest_registry.get("named_use_mapping_sha256") == uses_sha and
            manifest_registry.get("state_rows_sha256") == state_rows_sha,
            "manifest registry digest projection")
    return {
        "context_count": len(contexts),
        "named_use_count": len(uses),
        "context_rows_sha256": contexts_sha,
        "named_use_mapping_sha256": uses_sha,
        "state_count": 243,
        "state_rows_sha256": state_rows_sha,
        "packed_bytes_sha256": packed["sha256"],
    }


def validate_q3(q3: dict[str, Any]) -> dict[str, Any]:
    require(q3.get("schema") == "d972-b345-q-chief/v1", "q3 schema")
    require(q3.get("status") == q3.get("terminal_token") ==
            "B345_Q3_TYPED_SIGN_EXACT_WITH_WORD_CORRECTION", "q3 terminal")
    fibre = q3.get("correction_fibre")
    require(isinstance(fibre, dict), "q3 correction fibre")
    cert = fibre.get("certificate")
    records = fibre.get("records")
    require(isinstance(cert, dict) and isinstance(records, list) and len(records) == 27,
            "q3 correction records")
    require(cert.get("order") == cert.get("enumerated_count") == 27 and
            cert.get("all_q3_coordinates_unique") is True,
            "q3 correction enumeration certificate")
    expected_coords = list(itertools.product(range(3), repeat=3))
    for c, (record, expected) in enumerate(zip(records, expected_coords)):
        require(record.get("q_coords") == list(expected), f"q3 c{c} coordinate order")
        ambient = record.get("ambient_Pi3_coords")
        require(isinstance(ambient, list) and len(ambient) == 4 and
                all(type(x) is int and 0 <= x < 3 for x in ambient),
                f"q3 c{c} ambient coordinates")
        require(record["q_coords"] == [ambient[0], ambient[2], ambient[3]],
                f"q3 c{c} coordinate projection")
        perm = record.get("q_permutation")
        require(isinstance(perm, list) and set(perm) == set(range(1, 10)),
                f"q3 c{c} q permutation")
        validate_word(record.get("word"), {-2, -1, 1, 2}, f"q3 c{c}")
    require(records[0]["word"] == [] and records[0]["q_coords"] == [0, 0, 0],
            "canonical c0 is not the empty correction")

    roof = q3.get("canonical_roof_powers")
    require(isinstance(roof, dict), "q3 roof object")
    rows = roof.get("rows")
    exponents = [1, 2, 4, 5, 7, 8]
    require(isinstance(rows, list) and len(rows) == 6, "q3 roof row count")
    require(roof.get("outside_residues_complete_mod9") == exponents,
            "q3 outside residues")
    require([row.get("exponent") for row in rows] == exponents,
            "q3 zero-based roof order")
    require(len({row.get("row_index") for row in rows}) == 6, "q3 roof row uniqueness")
    for r, row in enumerate(rows):
        word = validate_word(row.get("word"), {-2, -1, 1, 2}, f"q3 r{r}")
        require(row.get("canonical_word_length") == len(word),
                f"q3 r{r} canonical length")
        require(row.get("q3_canonical_fibre_size") == 27 and
                row.get("q3_step_fibre_rebased") is True,
                f"q3 r{r} fibre size/rebase")
        shift = row.get("q3_shift_correction_index")
        require(type(shift) is int and 1 <= shift <= 27,
                f"q3 r{r} historical shift index")
        require(records[shift - 1]["q_coords"] == row.get("q3_shift_coords"),
                f"q3 r{r} one-based shift reference")
    return {
        "correction_count": len(records),
        "roof_count": len(rows),
        "roof_exponents": exponents,
        "zero_based_branch_axes": True,
        "historical_shift_index_is_one_based_and_separate": True,
    }


def validate_bulk(bulk: dict[str, Any]) -> dict[str, Any]:
    require(bulk.get("schema") == "koubou158-L3-bulk162/v1.2", "bulk schema")
    require(bulk.get("n_branches_total") == 162, "bulk total")
    entries = bulk.get("per_branch")
    universe = universe_ids()
    require(isinstance(entries, list) and len(entries) == 162, "bulk per_branch size")
    require([row.get("branch_id") for row in entries] == list(universe),
            "bulk branch order/uniqueness")
    reported_nonmember: list[str] = []
    reported_member: list[str] = []
    branch_row_fields = {
        "branch_id", "roof_index", "correction_index",
        "non_member_at_L3", "separator",
    }
    for ordinal, row in enumerate(entries):
        require(isinstance(row, dict) and set(row) == branch_row_fields,
                f"bulk branch row schema at ordinal {ordinal}")
        branch_id = row.get("branch_id")
        r, c = parse_branch_id(branch_id)
        require(ordinal == 27 * r + c, f"bulk zero-based ordinal: {branch_id}")
        require(row.get("roof_index") == r and row.get("correction_index") == c,
                f"bulk index fields: {branch_id}")
        flag = row.get("non_member_at_L3")
        require(type(flag) is bool, f"bulk outcome type: {branch_id}")
        separator = row.get("separator")
        if flag:
            require(isinstance(separator, dict) and
                    type(separator.get("support")) is int and separator["support"] > 0,
                    f"bulk separator: {branch_id}")
            reported_nonmember.append(branch_id)
        else:
            require(separator is None, f"bulk member has separator: {branch_id}")
            reported_member.append(branch_id)
    require(len(reported_nonmember) == bulk.get("n_non_member_at_L3") == 144,
            "bulk 144 count")
    require(len(reported_member) == bulk.get("n_member_at_L3") == 18,
            "bulk 18 count")
    # The top-level receipt projections use JSON-string order, while the
    # per-branch table is in numeric (roof, correction) order.  Check the
    # declared projection exactly without confusing lexical and numeric order.
    require(sorted(reported_nonmember) == bulk.get("non_member_at_L3_branch_ids"),
            "bulk nonmember list projection")
    require(sorted(reported_member) == bulk.get("member_at_L3_branch_ids"),
            "bulk member list projection")
    require(tuple(reported_member) == EXPECTED_L3_INCONCLUSIVE,
            "bulk accepted 18-roster mismatch")
    require(set(reported_nonmember).isdisjoint(reported_member) and
            set(reported_nonmember) | set(reported_member) == set(universe),
            "bulk 144/18 is not an exact partition")
    return {
        "universe_count": 162,
        "reported_nonmember_count": 144,
        "l3_inconclusive_count": 18,
        "l3_inconclusive": list(reported_member),
        "partition_exact": True,
        "branch_row_fields": sorted(branch_row_fields),
    }


def validate_prodrung(prod: dict[str, Any], l3_roster: Sequence[str]) -> dict[str, Any]:
    require(prod.get("schema") == "koubou158-prodrung/v1", "prodrung schema")
    results = prod.get("branch_results")
    require(isinstance(results, dict), "prodrung branch_results")
    require(set(results) == set(l3_roster) and len(results) == 18,
            "prodrung domain is not exactly the L3 roster")
    dead: list[str] = []
    undecided: list[str] = []
    branch_row_fields = {"branch_id", "j_star", "non_member", "separator"}
    for branch_id in l3_roster:
        row = results[branch_id]
        require(isinstance(row, dict) and set(row) == branch_row_fields and
                row.get("branch_id") == branch_id,
                f"prodrung nested branch id: {branch_id}")
        flag = row.get("non_member")
        require(type(flag) is bool, f"prodrung outcome type: {branch_id}")
        if flag:
            require(row.get("j_star") == 5 and isinstance(row.get("separator"), dict),
                    f"prodrung reported-dead receipt: {branch_id}")
            dead.append(branch_id)
        else:
            require(row.get("j_star") is None and row.get("separator") is None,
                    f"prodrung undecided receipt: {branch_id}")
            undecided.append(branch_id)
    require(tuple(dead) == EXPECTED_J5_REPORTED_DEAD,
            "prodrung accepted 8-roster mismatch")
    require(tuple(undecided) == EXPECTED_J5_UNDECIDED,
            "prodrung accepted 10-roster mismatch")
    require(len(dead) == prod.get("n_branches_dead") == 8 and
            len(undecided) == prod.get("n_branches_undetermined") == 10,
            "prodrung 8/10 counts")
    require(prod.get("all_18_dead") is False, "prodrung all_18_dead drift")
    require(set(dead).isdisjoint(undecided) and
            set(dead) | set(undecided) == set(l3_roster),
            "prodrung 8/10 is not an exact partition")
    progression = prod.get("j_progression")
    require(isinstance(progression, list) and [row.get("j") for row in progression] ==
            [2, 3, 4, 5], "prodrung j progression")
    require(progression[-1].get("n_branches_resolved_this_level") == 8 and
            progression[-1].get("n_branches_still_undetermined_after") == 10,
            "prodrung final progression counts")
    return {
        "domain_count": 18,
        "reported_j5_dead_count": 8,
        "reported_j5_dead": dead,
        "undecided_count": 10,
        "undecided": undecided,
        "partition_exact": True,
        "distinct_branch_count": 18,
        "stage_record_count_L3_plus_j5_undecided": 28,
        "twenty_eight_is_not_a_branch_count": True,
        "branch_row_fields": sorted(branch_row_fields),
    }


def validate_cross_provenance(
    bulk: dict[str, Any], prod: dict[str, Any]
) -> dict[str, Any]:
    b = bulk.get("input_provenance", {}).get("q3_chief_receipt")
    p = prod.get("input_provenance", {}).get("q3_chief_receipt")
    for label, row in (("bulk", b), ("prodrung", p)):
        require(isinstance(row, dict), f"{label} q3 provenance")
        require(row.get("bytes") == Q3_BYTES and row.get("sha256") == Q3_SHA256,
                f"{label} q3 provenance binding")
        require(Path(row.get("path", "")).name == "d972_b345_q3_chief_v1.json",
                f"{label} q3 provenance basename")
    return {"same_q3_bytes_sha256": Q3_SHA256, "same_q3_bound": True}


def state_key(perm: Sequence[int], coords: Sequence[int]) -> bytes:
    return bytes([x - 1 for x in perm] + list(coords))


def fox_gradient(
    word: Sequence[int], perm: PermModel, pc: PcModel
) -> tuple[dict[tuple[int, bytes], int], tuple[int, ...], tuple[int, ...]]:
    p = perm.identity
    c = pc.identity
    out: dict[tuple[int, bytes], int] = {}
    for letter in word:
        component = abs(letter)
        if letter > 0:
            key = (component, state_key(p, c))
            out[key] = (out.get(key, 0) + 1) % 3
            p = perm.mul(p, perm.marked[component - 1])
            c = pc.mul(c, pc.marked[component - 1])
        else:
            p = perm.mul(p, perm.inv(perm.marked[component - 1]))
            c = pc.mul(c, pc.marked_inverse[component - 1])
            key = (component, state_key(p, c))
            out[key] = (out.get(key, 0) + 2) % 3
    out = {key: value for key, value in out.items() if value}
    return out, p, c


def gradient_receipt(gradient: dict[tuple[int, bytes], int]) -> dict[str, Any]:
    rows = [[component, key.hex(), coefficient]
            for (component, key), coefficient in sorted(gradient.items())]
    return {"support": len(rows), "independent_rows_sha256": digest_obj(rows)}


def reconstruct_branch_canaries(
    q3: dict[str, Any], registry: dict[str, Any], target: dict[str, Any]
) -> dict[str, Any]:
    pb3_record = q3["groups"]["PB3"]
    pb4_record = q3["groups"]["PB4"]
    pb3 = PcModel(pb3_record, "Pi3[3]")
    pb4 = PcModel(pb4_record, "Pi4[3]")
    pc_calibration = {
        "PB3": pb3.calibrate(pb3_record),
        "PB4": pb4.calibrate(pb4_record),
    }
    q0_raw = q3["coarse_models"]["Q0"]
    q4_raw = q3["coarse_models"]["Q4"]
    q0 = PermModel(q0_raw["marked_permutations"], q0_raw["degree"], "Q0")
    q4 = PermModel(q4_raw["marked_permutations"], q4_raw["degree"], "Q4")

    corrections = q3["correction_fibre"]["records"]
    correction_pb3 = []
    correction_q0_identity = 0
    for c, record in enumerate(corrections):
        word = tuple(record["word"])
        coords = pb3.eval_marked(word, roots=(1, 3))
        require(coords == tuple(record["ambient_Pi3_coords"]),
                f"independent PB3 correction replay c{c}")
        correction_pb3.append(list(coords))
        if q0.eval(word) == q0.identity:
            correction_q0_identity += 1
    require(correction_q0_identity == 27,
            "independent Q0 correction-identity replay")

    roots = ((4,), (6,), (-4, -6))
    binding_rows: list[dict[str, Any]] = []
    q4_identity_count = 0
    pi4_identity_count = 0
    e4_identity_count = 0
    for r, roof in enumerate(q3["canonical_roof_powers"]["rows"]):
        for c, correction in enumerate(corrections):
            branch_id = f"r{r}_c{c}"
            candidate = reduce_word(tuple(roof["word"]) + tuple(correction["word"]))
            a = substitute_f2(candidate, roots[0], roots[1])
            b = substitute_f2(candidate, roots[0], roots[2])
            cword = substitute_f2(candidate, roots[1], roots[2])
            h1 = reduce_word(cword + inverse_word(b) + a)
            q4_value = q4.eval(h1)
            pi4_value = pb4.eval_marked(h1)
            q4_identity = q4_value == q4.identity
            pi4_identity = pi4_value == pb4.identity
            q4_identity_count += int(q4_identity)
            pi4_identity_count += int(pi4_identity)
            e4_identity_count += int(q4_identity and pi4_identity)
            gradient, final_perm, final_pc = fox_gradient(h1, q4, pb4)
            require(final_perm == q4_value and final_pc == pi4_value,
                    f"Fox/value replay mismatch: {branch_id}")
            raw_binding = {
                "branch_id": branch_id,
                "roof_index_zero_based": r,
                "correction_index_zero_based": c,
                "roof_exponent": roof["exponent"],
                "roof_row_index_historical_one_based": roof["row_index"],
                "roof_word": roof["word"],
                "correction_q_coords": correction["q_coords"],
                "correction_word": correction["word"],
            }
            binding_rows.append({
                "branch_id": branch_id,
                "raw_input_binding_sha256": digest_obj(raw_binding),
                "candidate_word_length": len(candidate),
                "candidate_word_sha256": digest_obj(list(candidate)),
                "h1_word_length": len(h1),
                "h1_word_sha256": digest_obj(list(h1)),
                "q4_identity": q4_identity,
                "pi4_identity": pi4_identity,
                **gradient_receipt(gradient),
            })

    # The only cross-blob target canary is the historical base r1_c0.
    base = binding_rows[27]
    base_word = q3["canonical_roof_powers"]["rows"][1]["word"]
    require(q3["selected_solution"]["exponent"] == 2 and
            q3["selected_solution"]["roof_row_index"] == 37 and
            q3["selected_solution"]["typed_source_word"] == base_word and
            q3["selected_solution"]["correction_word"] == [],
            "q3 r1_c0 selected-solution binding")
    require(registry["base_q3_replay"]["fixed_word"] == base_word and
            registry["base_q3_replay"]["roof_exponent"] == 2,
            "registry r1_c0 base binding")
    target6 = target.get("initial_target", {}).get("target6")
    require(isinstance(target6, dict) and target6.get("name") ==
            "hexagon_1_coface_0" and target6.get("ordinal") == 6,
            "target6 base row")
    formulas = target6.get("formula_checks")
    require(isinstance(formulas, list) and len(formulas) == 109,
            "target6 formula-check count")
    require(formulas[0].get("product_order") == "h1=C*B^-1*A" and
            formulas[0].get("formula") == "L_C([c]-[b])+L_h1[a]" and
            formulas[0].get("free_word_identity") is True,
            "target6 product/formula canary")
    expected_support = target6.get("base_gradient", {}).get("entry_count")
    require(expected_support == registry["base_target6"]["raw_gradient_support"] == 72,
            "cross-receipt base-gradient support")
    require(base["support"] == 72 and base["q4_identity"] and base["pi4_identity"],
            "independent r1_c0 h1/Fox support canary")

    return {
        "pc_model_calibration": pc_calibration,
        "correction_pb3_coords_sha256": digest_obj(correction_pb3),
        "correction_q0_identity_count": correction_q0_identity,
        "branch_binding_count": len(binding_rows),
        "branch_binding_rows_sha256": digest_obj(binding_rows),
        "q4_h1_identity_count": q4_identity_count,
        "pi4_h1_identity_count": pi4_identity_count,
        "e4_h1_identity_count": e4_identity_count,
        "base_r1_c0": base,
        "literal_reconstruction": {
            "candidate_formula": "free_reduce(roof_word || correction_word)",
            "roots": {"x0": [4], "y0": [6], "z0": [-4, -6]},
            "product_order": "h1=C*B^-1*A",
            "fox_convention": (
                "positive uses prefix before multiplication; negative uses inverse "
                "prefix after multiplication; coefficients modulo 3"
            ),
        },
        "semantic_binding": {
            "base_r1_c0_cross_blob_canary": "PASS",
            "all_162_literal_canaries_reconstructed": True,
            "bulk_per_branch_target_digest_present": False,
            "prodrung_per_branch_target_digest_present": False,
            "nonzero_kappa_formula_independently_certified": False,
            "reason": (
                "bulk/prodrung publish only branch indices and outcome/separator "
                "summaries; they publish neither candidate/h1 words nor per-branch "
                "raw-gradient digests.  Therefore the independently reconstructed "
                "162 target canaries cannot be matched to the targets actually "
                "rank/solved by those producers."
            ),
        },
    }


def run_mutation_tests(
    pin: dict[str, Any], q3: dict[str, Any], bulk: dict[str, Any],
    prod: dict[str, Any], registry: dict[str, Any],
) -> list[str]:
    tests: list[tuple[str, Any]] = []

    bad = copy.deepcopy(pin)
    bad["indexing"]["canonical"] = "one-based"
    tests.append(("one_based_manifest", lambda b=bad: validate_pin_structure(b)))

    bad = copy.deepcopy(q3)
    bad["correction_fibre"]["records"][1]["q_coords"] = [0, 0, 0]
    tests.append(("duplicate_q3_coordinate", lambda b=bad: validate_q3(b)))

    bad = copy.deepcopy(bulk)
    bad["per_branch"][1]["branch_id"] = "r0_c0"
    tests.append(("duplicate_branch", lambda b=bad: validate_bulk(b)))

    bad = copy.deepcopy(bulk)
    bad["per_branch"][27]["roof_index"] = 2
    tests.append(("one_based_roof_drift", lambda b=bad: validate_bulk(b)))

    bad = copy.deepcopy(prod)
    del bad["branch_results"][EXPECTED_L3_INCONCLUSIVE[0]]
    tests.append((
        "missing_prodrung_branch",
        lambda b=bad: validate_prodrung(b, EXPECTED_L3_INCONCLUSIVE),
    ))

    bad = copy.deepcopy(prod)
    row = bad["branch_results"][EXPECTED_J5_UNDECIDED[0]]
    row["non_member"], row["j_star"], row["separator"] = True, 5, {"support": 1}
    tests.append((
        "eight_ten_partition_drift",
        lambda b=bad: validate_prodrung(b, EXPECTED_L3_INCONCLUSIVE),
    ))

    bad = copy.deepcopy(registry)
    bad["context_registry"]["named_uses"][0]["context_id"] = 32
    tests.append(("invalid_context_reference", lambda b=bad: validate_registry(b, pin)))

    passed: list[str] = []
    for label, thunk in tests:
        try:
            thunk()
        except CheckError:
            passed.append(label)
        else:
            raise CheckError(f"mutation was not rejected: {label}")
    return passed


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path,
                        default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    repo = args.repo.resolve()

    pin, pin_meta = load_json_exact(
        repo / PIN_REL, expected_bytes=PIN_BYTES, expected_sha256=PIN_SHA256,
        display_path=PIN_REL,
    )
    pin_files = validate_pin_files(repo, pin)
    q3, q3_meta = load_json_exact(
        repo / Q3_REL, expected_bytes=Q3_BYTES, expected_sha256=Q3_SHA256,
        display_path=Q3_REL,
    )
    bulk, bulk_meta = load_json_exact(
        repo / BULK_REL, expected_bytes=BULK_BYTES, expected_sha256=BULK_SHA256,
        display_path=BULK_REL,
    )
    prod, prod_meta = load_json_exact(
        repo / PROD_REL, expected_bytes=PROD_BYTES, expected_sha256=PROD_SHA256,
        display_path=PROD_REL,
    )
    file_index = {row["path"]: row for row in pin["files"]}
    registry_row = file_index[REGISTRY_REL]
    target_row = file_index[TARGET_REL]
    registry, registry_meta = load_json_exact(
        repo / REGISTRY_REL,
        expected_bytes=registry_row["bytes"],
        expected_sha256=registry_row["sha256"],
        display_path=REGISTRY_REL,
    )
    target, target_meta = load_json_exact(
        repo / TARGET_REL,
        expected_bytes=target_row["bytes"],
        expected_sha256=target_row["sha256"],
        display_path=TARGET_REL,
    )

    pin_check = validate_pin_files(repo, pin)
    registry_check = validate_registry(registry, pin)
    q3_check = validate_q3(q3)
    bulk_check = validate_bulk(bulk)
    prodrung_check = validate_prodrung(prod, bulk_check["l3_inconclusive"])
    provenance_check = validate_cross_provenance(bulk, prod)
    canaries = reconstruct_branch_canaries(q3, registry, target)
    mutations = (
        run_mutation_tests(pin, q3, bulk, prod, registry)
        if args.self_test else []
    )

    script_path = Path(__file__).resolve()
    script_raw = script_path.read_bytes()
    verdict = {
        "schema": "koubou159b-branch-cover-crosscheck/v1",
        "status": "ACCOUNTING_PASS_KAPPA_UNKNOWN",
        "grade": "cross-checked accounting; mathematical branch outcomes UNKNOWN",
        "checked_date": "2026-08-23",
        "checker": {
            "path": script_path.relative_to(repo).as_posix(),
            "bytes": len(script_raw),
            "sha256": sha256_bytes(script_raw),
            "producer_modules_imported": [],
            "standard_library_only": True,
        },
        "inputs": [pin_meta, q3_meta, bulk_meta, prod_meta, registry_meta, target_meta],
        "version_pin": {**pin_check, "manifest_sha256": pin_meta["sha256"]},
        "registry": registry_check,
        "q3_axes": q3_check,
        "cross_provenance": provenance_check,
        "bulk_partition": bulk_check,
        "prodrung_partition": prodrung_check,
        "independent_literal_canaries": canaries,
        "nonzero_kappa_audit": {
            "status": "STOP_UNKNOWN_MISSING_TYPED_BINDING",
            "independently_certified": False,
            "requested_formula": (
                "kappa_M([(m,f)])=(m mod M_ord, f mod M_F2)"
            ),
            "first_missing_datum": (
                "a versioned typed 648-row table binding each outside source-roof "
                "element/key to its kappa_M image, zero-based branch_id, and "
                "source-target digest"
            ),
            "receipt_level_additional_gap": (
                "bulk/prodrung branch rows contain no candidate-word, h1-word, "
                "or raw-gradient digest, so the independently reconstructed 162 "
                "literal targets cannot be matched to producer rank/solve inputs"
            ),
            "bulk_branch_row_fields": bulk_check["branch_row_fields"],
            "prodrung_branch_row_fields": prodrung_check["branch_row_fields"],
        },
        "mutation_tests": {"executed": bool(args.self_test), "rejected": mutations},
        "claim_boundary": {
            "supported": [
                "the version-pin manifest and every listed file match bytes/SHA256",
                "the 31-context/46-name registry and packed state table replay",
                "the unique zero-based branch universe has 162 entries",
                "the receipts report the exact partition 162=144+18",
                "the prodrung receipt domain is exactly those 18 and reports 18=8+10",
                "the 10 are a subset of the 18; 28 is only a duplicated stage-record count",
                "r1_c0 independently replays the literal h1 value and Fox support-72 canary",
            ],
            "not_supported": [
                "independent rank/solve verification of the 144 or the reported eight",
                "promotion of the reported eight to final dead branches",
                "the nonzero-roof kappa formula as used by the bulk/prodrung producers",
                "a mapping from the 162 branch universe to all 648 outside roof elements",
                "TYPE-M, KEY-BIJ, M1-prime, lift existence/nonexistence, fake/witness type",
            ],
            "mathematical_status": "UNKNOWN",
        },
        "terminal_token": "KOUBOU159B_BRANCH_ACCOUNTING_PASS_KAPPA_UNKNOWN",
    }
    encoded = json.dumps(verdict, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(encoded, encoding="utf-8", newline="\n")
    else:
        sys.stdout.write(encoded)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (CheckError, FileNotFoundError, PermissionError) as exc:
        print(f"KOUBOU159B_BRANCH_CROSSCHECK_FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
