#!/usr/bin/env python3
"""Task982: read-only target history and one ordered F2 word, with mod54 readout.

The accepted numerical parents are premises. This consumer never resumes
them, never calls the continuation producer, and never imports its checker.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass, field
import hashlib
import json
import os
from pathlib import Path
import re
import signal
import stat
import struct
import sys
import tempfile
import time
from typing import Any, BinaryIO, Callable, Iterable

SCHEMA = "d972.r07.continuation-positive-word.v1"
GRAMMAR = "prior-only-ordered-F2-eight-ops-v1"
SOURCE_ROOT = Path(__file__).resolve().parent.parent
CHARACTERS = ((0, 0), (0, 1), (1, 0), (1, 1))
ACTORS = (1, -1, 2, -2)
OLD_OFFSETS, NEW_OFFSETS = (0, 505, 1008, 1511), (2014, 3523, 5035, 6547)
OLD_RANKS, NEW_RANKS = (505, 503, 503, 503), (1509, 1512, 1512, 1512)
P1_ROWS, LOWER_TRITS, PHYSICAL_TRITS, PHYSICAL_BYTES = 8059, 96776, 48384, 12096
REF_NAMESPACES = frozenset(("p1", "old-defect", "conn-lower", "conn-raw", "physical",
                          "raw-e", "tree", "normalizer", "target"))
OPS = frozenset(("Identity", "Letter", "Rel", "Act", "OrderedProduct", "Inverse", "IntegerPower", "Ref"))
ASSURANCE = {"candidate": True, "cross_checked": False, "verified": False}
DATA_PINS = {
    "scratchpad/a0_paper_words_v1.json": (115928, "90ba603368307e16b27b2bad9d84847c7bedc501fab811b8919d96e3c8936893"),
    "scratchpad/a0_v2_words.json": (106133, "fb191e30d269b5392acbebfce914905eeb0d10ed4292eac31bbbcb928ae62612"),
    "scratchpad/fuda1_a0_rmax_data.g": (4709, "625b4d11ca882c9419d9e0d78510bf323a117673722b8dd9ec7d7e85554267ba")}
RHO2_ARTIFACT = {"run": 33839962829, "attempt": 1, "head": "17a8439c766d92719d7ae7d35846ea444da598fa",
    "id": 9925190479, "name": "task640-fresh-rho2-v17-33839962829-1", "bytes": 6049643,
    "sha256": "sha256:01722bfda081e577195aa6ca9c0bba3425a50dcfd829eca6ac23e33cb5d79ca4"}
RHO2_FILES = {
    "task640-payload/manifest.json": (26047, "55c42f06e70b2150d324ed8649fe4af0e6db1bf0e87e315db570d1fa80f61488"),
    "task640-verdict.json": (418, "cdf0654738a10acf59844df3b9dda5ab8efdf2e387bba7d69b691a4ad46b2848"),
    "task640-payload/rho2.bin": (12096, "b41b9e69fc1257bb1542062a2496bc94bd3cbe6b01e03aba653dae2e4af17c2e"),
    "task640-payload/rho2-dense.bin": (48384, "abfafbc7521af43c75f1b5a73a6da5d37b90ec1648b649401d684a58cf16752e"),
    "task640-payload/lower-dense.bin": (32260, "c5657f998c12426cb1f2c1b4ae1e3a99ce4df9d61101eb33fba7921303bb4830"),
    "task640-payload/target-dense.bin": (80644, "122dca3cf3dc3299214f1ba4c2bc5b82dbe64e510f8aef482329316c2a935ea2"),
    "task640-payload/authenticated-roots.json": (255846, "af1b035e0eb0af6e593770affb52a52905609fd9c19e988b0b7e8cf69e7592c5")}
STARTED = time.monotonic()
DEADLINE: float | None = None
MEMORY_LIMIT_BYTES: int | None = None
STOP_REQUESTED = False
PHASE = "initialization"
OUTPUT_CREATED: Path | None = None


class ResourceStop(RuntimeError):
    pass


def require(condition: Any, message: str) -> None:
    if not condition:
        raise ValueError(message)


def plain_int(value: Any, low: int | None = None, high: int | None = None) -> bool:
    return type(value) is int and (low is None or value >= low) and (high is None or value <= high)


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":")) + "\n").encode("ascii")


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def digest_string(value: Any) -> bool:
    return isinstance(value, str) and re.fullmatch(r"[0-9a-f]{64}", value) is not None


def seal(kind: str, body: dict[str, Any]) -> dict[str, Any]:
    require("schema" not in body and "sha256" not in body, "reserved_seal_fields")
    unsigned = {"schema": SCHEMA + "." + kind, **body}
    return {**unsigned, "sha256": sha(canonical(unsigned))}


def check_seal(value: Any, schema: str | None = None) -> None:
    require(isinstance(value, dict) and digest_string(value.get("sha256")), "sealed_object")
    require(schema is None or value.get("schema") == schema, "sealed_schema")
    require(value["sha256"] == sha(canonical({key: item for key, item in value.items() if key != "sha256"})),
            "sealed_hash")


def check_resources(phase: str | None = None) -> None:
    global PHASE
    if phase is not None:
        PHASE = phase
    if STOP_REQUESTED or (DEADLINE is not None and time.monotonic() >= DEADLINE):
        raise ResourceStop(PHASE + ":deadline")
    if MEMORY_LIMIT_BYTES is not None and sys.platform != "win32":
        import resource
        used = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        used *= 1 if sys.platform == "darwin" else 1024
        if used >= MEMORY_LIMIT_BYTES:
            raise ResourceStop(PHASE + ":memory")


def request_stop(_signal: int, _frame: Any) -> None:
    global STOP_REQUESTED
    STOP_REQUESTED = True


def progress(phase: str, **fields: Any) -> None:
    check_resources(phase)
    print(json.dumps({"phase": phase, "elapsed_seconds": round(time.monotonic() - STARTED, 6), **fields},
                     sort_keys=True), file=sys.stderr, flush=True)


def relative_name(name: Any) -> str:
    require(isinstance(name, str) and name and "\\" not in name and "\x00" not in name and ":" not in name,
            "relative_posix_name")
    path = Path(name)
    require(not path.is_absolute() and all(part not in ("", ".", "..") for part in name.split("/")),
            "relative_path_parts")
    require(path.as_posix() == name, "canonical_relative_path")
    return name


def safe_file(root: Path, name: str) -> Path:
    relative_name(name)
    require(root.is_dir() and not root.is_symlink(), "parent_regular_directory")
    cursor = root
    for part in name.split("/"):
        cursor /= part
        require(not cursor.is_symlink(), "ancestor_symlink")
    require(root.resolve() in cursor.resolve().parents and cursor.is_file() and
            stat.S_ISREG(cursor.stat().st_mode), "contained_regular_file")
    return cursor


def file_pin(path: Path) -> dict[str, Any]:
    require(path.is_file() and not path.is_symlink(), "regular_file_pin")
    length, digest = 0, hashlib.sha256()
    with path.open("rb") as stream:
        while True:
            chunk = stream.read(1 << 20)
            if not chunk:
                break
            digest.update(chunk)
            length += len(chunk)
            check_resources("input-file-pin")
    return {"bytes": length, "sha256": digest.hexdigest()}


def read_json_file(path: Path, *, canonical_required: bool = True) -> Any:
    raw = path.read_bytes()
    value = json.loads(raw.decode("utf-8"))
    if canonical_required:
        require(canonical(value) == raw, "canonical_json:" + path.name)
    return value


def signrep(value: Any) -> int:
    require(plain_int(value, 0, 2), "F3_scalar")
    return (0, 1, -1)[value]


def signed_letters(value: Any) -> tuple[int, ...]:
    require(isinstance(value, (list, tuple)) and all(type(item) is int and item in ACTORS for item in value),
            "literal_signed_letters")
    return tuple(value)


def epsilon(word: Iterable[int]) -> tuple[int, int]:
    a, b = 0, 0
    for letter in word:
        require(type(letter) is int and letter in ACTORS, "exponent_signed_letter")
        if abs(letter) == 1:
            a += 1 if letter > 0 else -1
        else:
            b += 1 if letter > 0 else -1
    return a, b


def child_links(op: str, args: Any) -> list[dict[str, Any]]:
    require(op in OPS and isinstance(args, dict), "word_op_args")
    keys = {"Identity": set(), "Letter": {"letter"},
        "Rel": {"dictionary_sha256", "relator_id", "letters", "letters_sha256"},
        "Act": {"conjugator", "word", "orientation"}, "OrderedProduct": {"factors"},
        "Inverse": {"word"}, "IntegerPower": {"word", "exponent"},
        "Ref": {"namespace", "key", "scope_sha256", "word"}}
    require(set(args) == keys[op], "exact_word_args:" + op)
    if op == "Identity":
        return []
    if op == "Letter":
        require(type(args["letter"]) is int and args["letter"] in ACTORS, "word_letter")
        return []
    if op == "Rel":
        require(digest_string(args["dictionary_sha256"]) and digest_string(args["letters_sha256"]) and
                isinstance(args["relator_id"], str) and args["relator_id"], "word_relator_identity")
        signed_letters(args["letters"])
        require(args["letters_sha256"] == sha(canonical(args["letters"])), "word_relator_bytes")
        return []
    if op == "Act":
        require(args["orientation"] == "P*W*P^-1", "word_actor_orientation")
        return [args["conjugator"], args["word"]]
    if op == "OrderedProduct":
        require(isinstance(args["factors"], list), "word_ordered_factors")
        return args["factors"]
    if op == "IntegerPower":
        require(type(args["exponent"]) is int, "word_ordinary_integer_exponent")
    if op == "Ref":
        require(args["namespace"] in REF_NAMESPACES and isinstance(args["key"], str) and args["key"] and
                digest_string(args["scope_sha256"]), "word_typed_ref")
    return [args["word"]]


def node_residue(op: str, args: dict[str, Any], pairs: list[tuple[int, int]]) -> tuple[int, int]:
    if op == "Identity":
        return 0, 0
    if op == "Letter":
        pair = epsilon((args["letter"],))
    elif op == "Rel":
        pair = epsilon(args["letters"])
    elif op == "Act":
        pair = pairs[args["word"]["node"]]
    elif op == "OrderedProduct":
        a, b = 0, 0
        for child in args["factors"]:
            x, y = pairs[child["node"]]
            a, b = (a + x) % 54, (b + y) % 54
        pair = a, b
    elif op == "Inverse":
        x, y = pairs[args["word"]["node"]]
        pair = -x, -y
    elif op == "IntegerPower":
        x, y = pairs[args["word"]["node"]]
        factor = args["exponent"] % 54
        pair = factor * x, factor * y
    else:
        require(op == "Ref", "residue_word_op")
        pair = pairs[args["word"]["node"]]
    return pair[0] % 54, pair[1] % 54


@dataclass
class WordDAG:
    stream: BinaryIO
    dictionary_sha256: str
    relators: dict[str, tuple[int, ...]]
    receipt_count: Callable[[], int]
    hashes: list[str] = field(default_factory=list)
    pairs: list[tuple[int, int]] = field(default_factory=list)
    positions: list[tuple[int, int]] = field(default_factory=list)
    symbols: dict[tuple[str, str, str], int] = field(default_factory=dict)
    length: int = 0
    file_digest: Any = field(default_factory=hashlib.sha256)

    def link(self, node: int) -> dict[str, Any]:
        require(plain_int(node, 0, len(self.hashes) - 1), "existing_word_node")
        return {"node": node, "sha256": self.hashes[node]}

    def add(self, op: str, args: dict[str, Any], refs: Iterable[int] = ()) -> int:
        index = len(self.hashes)
        refs = list(refs)
        require(all(plain_int(item, 0, self.receipt_count() - 1) for item in refs), "word_receipt_reference")
        for child in child_links(op, args):
            require(isinstance(child, dict) and set(child) == {"node", "sha256"} and
                    plain_int(child["node"], 0, index - 1) and child["sha256"] == self.hashes[child["node"]],
                    "prior_only_child_id_hash")
        if op == "Rel":
            require(args["dictionary_sha256"] == self.dictionary_sha256 and args["relator_id"] in self.relators and
                    tuple(args["letters"]) == self.relators[args["relator_id"]], "exact_literal_dictionary_join")
        unsigned = {"id": index, "type": "F2-word", "op": op, "args": args, "receipt_refs": refs}
        record = {**unsigned, "node_sha256": sha(canonical(unsigned))}
        raw = canonical(record)
        require(self.stream.write(raw) == len(raw), "word_stream_full_write")
        self.hashes.append(record["node_sha256"])
        self.pairs.append(node_residue(op, args, self.pairs))
        self.positions.append((self.length, len(raw)))
        self.length += len(raw)
        self.file_digest.update(raw)
        if index % 256 == 0:
            check_resources("ordered-word")
        return index

    def identity(self, refs: Iterable[int] = ()) -> int:
        return self.add("Identity", {}, refs)

    def letter(self, value: int, refs: Iterable[int] = ()) -> int:
        return self.add("Letter", {"letter": value}, refs)

    def rel(self, key: str, refs: Iterable[int] = ()) -> int:
        require(key in self.relators, "known_literal_relator")
        letters = list(self.relators[key])
        return self.add("Rel", {"dictionary_sha256": self.dictionary_sha256, "relator_id": key,
            "letters": letters, "letters_sha256": sha(canonical(letters))}, refs)

    def product(self, factors: Iterable[int], refs: Iterable[int] = ()) -> int:
        return self.add("OrderedProduct", {"factors": [self.link(node) for node in factors]}, refs)

    def inverse(self, word: int, refs: Iterable[int] = ()) -> int:
        return self.add("Inverse", {"word": self.link(word)}, refs)

    def power(self, word: int, exponent: int, refs: Iterable[int] = ()) -> int:
        return self.add("IntegerPower", {"word": self.link(word), "exponent": exponent}, refs)

    def act(self, conjugator: int, word: int, refs: Iterable[int] = ()) -> int:
        return self.add("Act", {"conjugator": self.link(conjugator), "word": self.link(word),
                               "orientation": "P*W*P^-1"}, refs)

    def ref(self, namespace: str, key: str, scope: str, word: int, refs: Iterable[int] = ()) -> int:
        symbol = namespace, key, scope
        require(symbol not in self.symbols, "unique_symbol_first_DFS_postorder")
        node = self.add("Ref", {"namespace": namespace, "key": key, "scope_sha256": scope, "word": self.link(word)}, refs)
        self.symbols[symbol] = node
        return node

    def flush(self) -> dict[str, Any]:
        self.stream.flush()
        os.fsync(self.stream.fileno())
        return {"file": "ordered-word.jsonl", "bytes": self.length,
                "sha256": self.file_digest.hexdigest(), "nodes": len(self.hashes)}


PARENT_ROLES = ("state", "delta", "seed34", "packet", "refinement", "oracle", "e", "prepare",
                "block-0", "block-1", "block-2", "block-3", "p1", "task712", "continuation", "rho2")
FIXED_ARTIFACTS = json.loads(r'''{
  "state": {
    "run": 33891714539,
    "attempt": 1,
    "head": "7b7b9de20faaa3b8f26e331bb738b374f6f5708c",
    "id": 9944214057,
    "name": "d972-r07-grade2-physical-state-separator-v2-candidate-33891714539-1",
    "bytes": 107195261,
    "sha256": "sha256:2d91e2e94ab7eb235805eb0f7c04ff87edef3954460d686f047d8abcfa99c017",
    "workflow": ".github/workflows/d972-r07-grade2-physical-state-separator-v2.yml",
    "repository_id": 1312092366,
    "conclusion": "success"
  },
  "delta": {
    "run": 33946247365,
    "attempt": 1,
    "head": "7f6dfaddf4150449e62a9b3e85def472fcb41c01",
    "id": 9963533999,
    "name": "d972-r07-actual-seed30-materializer-v1-candidate-33946247365-1",
    "bytes": 915410,
    "sha256": "sha256:f9627416f0e920fa369f6bc6bb9bffa8c6b15674c0fb7ff37bbebaf77991ace6",
    "workflow": ".github/workflows/d972-r07-actual-seed30-materializer-v1.yml",
    "repository_id": 1312092366,
    "conclusion": "success"
  },
  "seed34": {
    "run": 33956437467,
    "attempt": 1,
    "head": "b9ae78b0950b186463849c3ec874f6474f359851",
    "id": 9966542166,
    "name": "d972-r07-actual-root-seed-materializer-v3-candidate-33956437467-1",
    "bytes": 984053,
    "sha256": "sha256:a4cb9f63a470636628d9ef02a5b5e55d90fe3b0a2c70f2012d32c9517d87defc",
    "workflow": ".github/workflows/d972-r07-actual-root-seed-materializer-v3.yml",
    "repository_id": 1312092366,
    "conclusion": "success"
  },
  "packet": {
    "run": 33964709359,
    "attempt": 1,
    "head": "fff114c41bd8748ad0e708919fe0820335c9cce8",
    "id": 9969090590,
    "name": "d972-r07-fixed-root-packet-loop-v2-candidate-33964709359-1",
    "bytes": 1855391,
    "sha256": "sha256:b15b07150d23a1a291fff387f23c8c13cf3ab5ada2b5f95f2a886b0bdf44a428",
    "workflow": ".github/workflows/d972-r07-fixed-root-packet-loop-v2.yml",
    "repository_id": 1312092366,
    "conclusion": "success"
  },
  "refinement": {
    "run": 33971897879,
    "attempt": 1,
    "head": "64475e1dfab1537a38d1b3131971bfed5fc3071c",
    "id": 9971466432,
    "name": "d972-r07-full-origin-checker-completion-v1-candidate-33971897879-1",
    "bytes": 51943596,
    "sha256": "sha256:0d4af3475ca62da1d7436246bd36109d380e0a463a713de1c1e3db69f90c9db8",
    "workflow": ".github/workflows/d972-r07-full-origin-checker-completion-v1.yml",
    "repository_id": 1312092366,
    "conclusion": "success"
  },
  "oracle": {
    "run": 33977701313,
    "attempt": 1,
    "head": "bbce98d8f95a845f36fe89c0f507b9360792666f",
    "id": 9972829869,
    "name": "d972-r07-section-cochain-checker-completion-v1-candidate-33977701313-1",
    "bytes": 2299772,
    "sha256": "sha256:1a5c8800af563493b95dd4166d20c2fe1b74449f5f7f15aa99278d9b1c1b878d",
    "workflow": ".github/workflows/d972-r07-section-cochain-checker-completion-v1.yml",
    "repository_id": 1312092366,
    "conclusion": "success"
  },
  "e": {
    "run": 33981657987,
    "attempt": 1,
    "head": "444c71c9e554ae8feb9c8ee54df57d3df19ed66f",
    "id": 9973974150,
    "name": "d972-r07-selected-cycle-materializer-v1-candidate-33981657987-1",
    "bytes": 2816692,
    "sha256": "sha256:884c039737cae9673c9e1d871c30713456c993b97f16a557e9c8c24078537f25",
    "workflow": ".github/workflows/d972-r07-selected-cycle-materializer-v1.yml",
    "repository_id": 1312092366,
    "conclusion": "success"
  },
  "p1": {
    "run": 33851744070,
    "attempt": 1,
    "head": "6673eb2ea15ca6022acc2ddc5a8a204a0380172f",
    "id": 9931437113,
    "name": "task809-canonical-p1-degree2-lift-v9-33851744070-1",
    "bytes": 641518300,
    "sha256": "sha256:6d6f2ec6eb7f1245b8e7d52645c710ecd519ae0cc442340237d1098c7fa63d5c",
    "workflow": ".github/workflows/d972-r07-canonical-p1-dag-degree2-lift-v9.yml",
    "repository_id": 1312092366,
    "conclusion": "success"
  },
  "task712": {
    "run": 33814194630,
    "attempt": 1,
    "head": "5ff2c5a30b604536df12acba8801828a5a7e5fe0",
    "id": 9915928157,
    "name": "d972-r07-grade2-maps-v4-33814194630-1",
    "bytes": 22404961,
    "sha256": "sha256:abedff074117bb779675021e9436c3a9973c577e247fe76a8314a2d4312ea858",
    "workflow": ".github/workflows/d972-r07-grade2-maps-v4.yml",
    "repository_id": 1312092366,
    "conclusion": "success"
  },
  "prepare": {
    "run": 33677346616,
    "attempt": 1,
    "head": "22c6dddb43d107c05e65f53ad898823ae8ebe276",
    "id": 9865061266,
    "name": "task554-grade1-v3-prepare-33677346616-1",
    "bytes": 204360988,
    "sha256": "sha256:da8bfec6a03cac65de40ba8c4f79cde687fd2629edb3c3965fd972ecf96cc2f4",
    "workflow": ".github/workflows/d972-r07-a0-first-rung-grade1-v3.yml",
    "repository_id": 1312092366,
    "conclusion": "failure"
  },
  "block-0": {
    "run": 33677346616,
    "attempt": 1,
    "head": "22c6dddb43d107c05e65f53ad898823ae8ebe276",
    "id": 9865238399,
    "name": "task554-grade1-v3-state-block-0-33677346616-1",
    "bytes": 81729645,
    "sha256": "sha256:2a8e63a4270bf4052c7fd8763d7828fc17dd6b94c88854bacde1e94082cd5838",
    "workflow": ".github/workflows/d972-r07-a0-first-rung-grade1-v3.yml",
    "repository_id": 1312092366,
    "conclusion": "failure"
  },
  "block-1": {
    "run": 33677346616,
    "attempt": 1,
    "head": "22c6dddb43d107c05e65f53ad898823ae8ebe276",
    "id": 9865242284,
    "name": "task554-grade1-v3-state-block-1-33677346616-1",
    "bytes": 82259824,
    "sha256": "sha256:849321b79f0e3ea3c9a3f9c9dad43de2b3aaa571163456abc702476e322714fb",
    "workflow": ".github/workflows/d972-r07-a0-first-rung-grade1-v3.yml",
    "repository_id": 1312092366,
    "conclusion": "failure"
  },
  "block-2": {
    "run": 33677346616,
    "attempt": 1,
    "head": "22c6dddb43d107c05e65f53ad898823ae8ebe276",
    "id": 9865193269,
    "name": "task554-grade1-v3-state-block-2-33677346616-1",
    "bytes": 82200189,
    "sha256": "sha256:d2cdf8245d58a384bebfd516135e07930fe26c21c2c1cab130dfa6c3c7f2854d",
    "workflow": ".github/workflows/d972-r07-a0-first-rung-grade1-v3.yml",
    "repository_id": 1312092366,
    "conclusion": "failure"
  },
  "block-3": {
    "run": 33677346616,
    "attempt": 1,
    "head": "22c6dddb43d107c05e65f53ad898823ae8ebe276",
    "id": 9865239848,
    "name": "task554-grade1-v3-state-block-3-33677346616-1",
    "bytes": 82266526,
    "sha256": "sha256:87547101ede2fb48619a069de958c08cbb3cb0ee6c0990090234005aacd05b92",
    "workflow": ".github/workflows/d972-r07-a0-first-rung-grade1-v3.yml",
    "repository_id": 1312092366,
    "conclusion": "failure"
  }
}''')
FIXED_ARTIFACTS["rho2"] = {**RHO2_ARTIFACT, "workflow":
    ".github/workflows/d972-r07-a0-fresh-precision2-endpoint-v17.yml",
    "repository_id": 1312092366, "conclusion": "success"}
OLD_STATE_SHA = "69fdcc8cd740f8ea11bd198aaf44bcf50d1c4980331f51aa7f792544b00f9d88"
P1_MANIFEST_SHA = "86e8b14cb0a60c86468ffb54a7bf14980366406a1e5bea17018fc6961f331feb"
P1_INSTRUCTIONS_PIN = (349055442, "8b549337786b1f3b970a7250f1c326724ef957369c213c55af5a3d52a96f38ae")
PREPARE_BODY_SHA = "1f191d88a0453360021ec57d253a7d16c9a66ac059ddaaadb6db3e2b9293c865"
BLOCK_BODY_SHAS = (
    "9ebcc7ad1141c20aeaff82eb4a83a9489dc492b30220547f23526b4fcdd8dc74",
    "d783bbe6c92c15a241eb78d0b25bca5e7c00f60799ce82f6df8b1d3ee7a202f6",
    "a6dcc904fc3e9daae008f72de7e83ffadcd39055d557621b9cdf06baea0e83ac",
    "642a4ec0ad6ad4ea659e84330e34006c767ca029203446cb64a17c151fefdb01")
PURE_WORDS = ((), (-2,) * 9, (-2, -2, 1, 1, 2, 1, 2, 1, 1),
              (-2, -2, -2, -1, -2, -1, -1, -1, -2, -1))
NORMALIZER_ROSTER_SHA = "dcb8ce42c8324b0ce2a5018007f3d664da5568ee73182758a9f358deba84bc2a"
NORMALIZER_WORDS = {
    "r_x": (1058, "82fa1ff07d5269e5228fb411b97321b61869791c49133aaa65161f44d16b6f2c"),
    "r_y": (466, "88657577db0338fd5c58f7edeec205c27ce5ff5ddba128b8af403167cb232ac0"),
    "c_x": (9522, "2935d479d5896360e71b66aa95bcb964cdb04d9716f27c06f492034b5ac98abb"),
    "c_y": (4194, "c1f3ebec1ef6c448b854b216f8473e674a67a3b5d3a3059888af016293a1a6dd")}
LOOP_SCHEMA = "d972.r07.complete-oracle-cegar-continuation.v1"
LOOP_FIXED_FILES = {
    "output/owner.json": (8612, "e356f7d614828b9c466c70e4e446ec561de73a758b4c6a2292fdd97be39ff77b"),
    "output/source.json": (2423, "c787d53c65c6392845e6f26c545e213b6b17d9b08dc07d694a1c4e33282f2651"),
    "output/start.json": (54707, "87bd9b89c593d68fba65b765bfe9f17bcc47d52cc9afce6f53f8c131a24f816b")}
LOOP_PRODUCER_SHA = "67d2302c3c4d571a4ccbe524098fe97808f05069bfd2ed822408bde3e256733c"
LOOP_CHECKER_SHA = "e985b4ca3922fc4f89fe7c313d969bf4dd2b525fb92b4ee3ce3920888e6821e3"
PRIMARY_MANIFESTS = {"state": "state/manifest.json", "delta": "output/manifest.json",
    "seed34": "output/manifest.json", "packet": "output/HEAD", "refinement": "output/HEAD",
    "oracle": "output/manifest.json", "e": "output/manifest.json", "p1": "manifest.json",
    "task712": "r07-grade2-maps-v4/manifest.json", "continuation": "output/HEAD",
    "rho2": "task640-payload/manifest.json", "prepare": "prepare." + PREPARE_BODY_SHA + ".json",
    **{f"block-{owner}": f"block-{owner}.{digest}.json" for owner, digest in enumerate(BLOCK_BODY_SHAS)}}


def pin_entry(value: Any) -> None:
    require(isinstance(value, dict) and set(value) == {"file", "bytes", "sha256"} and
            plain_int(value["bytes"], 0) and digest_string(value["sha256"]), "file_pin_entry")
    relative_name(value["file"])


def inventory(root: Path) -> tuple[list[dict[str, Any]], list[str]]:
    require(root.is_dir() and not root.is_symlink(), "inventory_root")
    files, directories = [], []
    for current, folders, names in os.walk(root, followlinks=False):
        current_path = Path(current)
        for folder in sorted(folders):
            path = current_path / folder
            require(path.is_dir() and not path.is_symlink(), "inventory_regular_directory")
            directories.append(relative_name(path.relative_to(root).as_posix()))
        for name in sorted(names):
            path = current_path / name
            require(stat.S_ISREG(path.stat().st_mode) and not path.is_symlink(), "inventory_regular_file")
            files.append({"file": relative_name(path.relative_to(root).as_posix()), **file_pin(path)})
    return sorted(files, key=lambda entry: entry["file"]), sorted(directories)


@dataclass
class Parents:
    roots: dict[str, Path]
    acceptance: dict[str, Any]
    acceptance_sha256: str
    roster: dict[str, dict[str, Any]]
    files: dict[str, dict[str, dict[str, Any]]]

    def path(self, role: str, name: str) -> Path:
        require(role in self.roots and name in self.files[role], "declared_parent_file:" + role + "/" + name)
        return safe_file(self.roots[role], name)

    def pin(self, role: str, name: str) -> dict[str, Any]:
        require(role in self.files and name in self.files[role], "parent_pin_roster")
        return self.files[role][name]

    def read(self, role: str, name: str, *, strict: bool = True) -> Any:
        return read_json_file(self.path(role, name), canonical_required=strict)

    def manifest_sha(self, role: str) -> str:
        return self.roster[role]["manifest"]["sha256"]

    def again(self) -> None:
        for role in PARENT_ROLES:
            files, directories = inventory(self.roots[role])
            require(files == self.roster[role]["files"] and directories == self.roster[role]["directories"],
                    "all_input_bytes_unchanged:" + role)
            progress("parent-unchanged", role=role, files=len(files))


def admit_parents(args: argparse.Namespace) -> Parents:
    require(len(args.block_root) == 4, "four_ordered_block_roots")
    roots = {role: Path(getattr(args, role.replace("-", "_") + "_root")).resolve()
             for role in PARENT_ROLES if not role.startswith("block-")}
    roots.update({f"block-{owner}": Path(value).resolve() for owner, value in enumerate(args.block_root)})
    output = Path(args.output).resolve()
    for role, root in roots.items():
        require(root.is_dir() and not root.is_symlink(), "actual_cli_parent:" + role)
        require(root != output and root not in output.parents and output not in root.parents,
                "output_parent_disjoint")
        for other, path in roots.items():
            if other != role:
                require(path != root and path not in root.parents and root not in path.parents, "parent_roots_disjoint")
    acceptance_path = Path(args.acceptance).resolve()
    accepted_raw = acceptance_path.read_bytes()
    accepted = json.loads(accepted_raw.decode("ascii"))
    require(canonical(accepted) == accepted_raw, "canonical_acceptance")
    check_seal(accepted, SCHEMA + ".acceptance")
    require(set(accepted) == {"schema", "sha256", "status", "parents", "selected", "consumer_sources",
                              "runtime", "candidate", "cross_checked", "verified"}, "exact_acceptance_keys")
    require(accepted["status"] == "PASS" and all(accepted[key] is value for key, value in ASSURANCE.items()),
            "root_observed_acceptance_only")
    require(isinstance(accepted["parents"], list) and
            [entry.get("role") for entry in accepted["parents"]] == list(PARENT_ROLES), "sixteen_ordered_parents")
    roster, files = {}, {}
    for item in accepted["parents"]:
        require(set(item) == {"role", "artifact", "manifest", "files", "directories"}, "exact_parent_entry")
        role, artifact = item["role"], item["artifact"]
        require(isinstance(artifact, dict) and set(artifact) == set(FIXED_ARTIFACTS["state"]),
                "complete_artifact_tuple")
        require(all(plain_int(artifact[key], 1) for key in ("run", "attempt", "id", "bytes")) and
                artifact["repository_id"] == 1312092366 and
                re.fullmatch(r"[0-9a-f]{40}", artifact["head"]) is not None and
                re.fullmatch(r"sha256:[0-9a-f]{64}", artifact["sha256"]) is not None and
                isinstance(artifact["name"], str) and artifact["name"], "actual_artifact_identity")
        if role == "continuation":
            require(artifact["conclusion"] == "success" and "-candidate-" in artifact["name"] and
                    artifact["workflow"] in (
                        ".github/workflows/d972-r07-complete-oracle-cegar-checker-completion-v1.yml",
                        ".github/workflows/d972-r07-complete-oracle-cegar-resume64-v1.yml",
                        ".github/workflows/d972-r07-complete-oracle-cegar-resume-next-v1.yml"),
                    "successful_observed_continuation")
        else:
            require(artifact == FIXED_ARTIFACTS[role], "fixed_artifact_tuple:" + role)
        pin_entry(item["manifest"])
        require(item["manifest"]["file"] == PRIMARY_MANIFESTS[role], "fixed_primary_parent_receipt")
        require(isinstance(item["files"], list) and isinstance(item["directories"], list), "parent_full_inventory")
        for entry in item["files"]:
            pin_entry(entry)
        require(item["files"] == sorted(item["files"], key=lambda entry: entry["file"]) and
                len({entry["file"] for entry in item["files"]}) == len(item["files"]), "unique_sorted_files")
        require(item["directories"] == sorted(set(item["directories"])), "unique_sorted_directories")
        for name in item["directories"]:
            relative_name(name)
        observed_files, observed_dirs = inventory(roots[role])
        require(observed_files == item["files"] and observed_dirs == item["directories"],
                "whole_input_bytes_roster:" + role)
        files[role] = {entry["file"]: entry for entry in observed_files}
        require(files[role].get(item["manifest"]["file"]) == item["manifest"], "parent_primary_receipt")
        roster[role] = item
        progress("parent-admitted", role=role, files=len(observed_files))
    parents = Parents(roots, accepted, sha(accepted_raw), roster, files)
    require("r07-grade2-maps-v4/manifest.json" in files["task712"] and
            "r07-grade2-maps-v4-receipt.json" in files["task712"] and
            "r07-grade2-maps-v4-checker.json" in files["task712"], "task712_envelope_all_receipts")
    for name, (size, digest) in RHO2_FILES.items():
        require(parents.pin("rho2", name) == {"file": name, "bytes": size, "sha256": digest}, "fresh_rho2_pin")
    for name, (size, digest) in DATA_PINS.items():
        require(file_pin(safe_file(SOURCE_ROOT, name)) == {"bytes": size, "sha256": digest}, "raw_dictionary_pin")
    sources = accepted["consumer_sources"]
    require(isinstance(sources, dict) and set(sources) == {"producer", "checker"}, "consumer_source_pair")
    wanted_sources = {"producer": "search/d972_r07_continuation_positive_word_readout_v1.py",
                      "checker": "search/check_d972_r07_continuation_same_word_eleven_slots_v1.py"}
    for role, entry in sources.items():
        pin_entry(entry)
        require(entry["file"] == wanted_sources[role] and
                file_pin(safe_file(SOURCE_ROOT, entry["file"])) == {key: entry[key] for key in ("bytes", "sha256")},
                "actual_consumer_source:" + role)
    import numpy as np
    require(accepted["runtime"] == {"python": sys.version, "numpy": np.__version__}, "full_runtime_identity")
    return parents


def json_pointer(value: Any, pointer: str) -> Any:
    require(isinstance(pointer, str) and (pointer == "" or pointer.startswith("/")), "RFC6901_pointer")
    for encoded in pointer.split("/")[1:]:
        require(re.search(r"~(?![01])", encoded) is None, "RFC6901_escape")
        key = encoded.replace("~1", "/").replace("~0", "~")
        if isinstance(value, list):
            require(re.fullmatch(r"0|[1-9][0-9]*", key) is not None and int(key) < len(value), "pointer_array_index")
            value = value[int(key)]
        else:
            require(isinstance(value, dict) and key in value, "pointer_object_key")
            value = value[key]
    return value


@dataclass
class Ancestors:
    parents: Parents
    entries: list[dict[str, Any]] = field(default_factory=list)
    unique: dict[tuple[Any, ...], int] = field(default_factory=dict)

    def add(self, namespace: str, role: str, name: str, *, offset: int | None = None,
            length: int | None = None, pointer: str | None = None, value: Any = None) -> int:
        require(namespace in REF_NAMESPACES and role in PARENT_ROLES, "ancestor_namespace_and_role")
        pin = self.parents.pin(role, name)
        if pointer is not None:
            require(offset is None and length is None, "JSON_pointer_or_positioned_record")
            if value is None:
                value = self.parents.read(role, name, strict=False)
            pointed = json_pointer(value, pointer)
            record_sha = sha(canonical(pointed))
        elif offset is not None:
            require(plain_int(offset, 0) and plain_int(length, 1) and offset + length <= pin["bytes"],
                    "positioned_parent_bounds")
            with self.parents.path(role, name).open("rb") as stream:
                stream.seek(offset)
                raw = stream.read(length)
            require(len(raw) == length, "positioned_parent_read")
            record_sha = sha(raw)
        else:
            require(length is None, "whole_parent_file_position")
            offset, length, record_sha = 0, pin["bytes"], pin["sha256"]
        key = namespace, role, name, offset, length, pointer, record_sha
        if key in self.unique:
            return self.unique[key]
        index = len(self.entries)
        self.entries.append({"id": index, "namespace": namespace, "parent_role": role,
            "parent_manifest_sha256": self.parents.manifest_sha(role), "file": name,
            "file_sha256": pin["sha256"], "offset": offset, "length": length,
            "record_sha256": record_sha, "json_pointer": pointer})
        self.unique[key] = index
        return index


def ordinary_inverse(word: Iterable[int]) -> tuple[int, ...]:
    return tuple(-letter for letter in reversed(tuple(word)))


def freely_reduce(word: Iterable[int]) -> tuple[int, ...]:
    stack: list[int] = []
    for letter in word:
        require(type(letter) is int and letter in ACTORS, "normalizer_letter")
        if stack and stack[-1] == -letter:
            stack.pop()
        else:
            stack.append(letter)
    return tuple(stack)


def literal_dictionary() -> dict[str, Any]:
    paper = read_json_file(safe_file(SOURCE_ROOT, "scratchpad/a0_paper_words_v1.json"), canonical_required=False)
    other = read_json_file(safe_file(SOURCE_ROOT, "scratchpad/a0_v2_words.json"), canonical_required=False)
    relators = paper["relators"]
    require(len(relators) == 44, "forty_four_literal_relators")
    q = [signed_letters(word) for word in other["raw_q0_relators"]]
    require(len(q) == 19 and sha(canonical(other["raw_q0_relators"])[:-1]) == NORMALIZER_ROSTER_SHA,
            "nineteen_raw_Q0_words")
    rx = freely_reduce(q[0] + ordinary_inverse(q[5]) * 2 + q[6] * 4 + q[8])
    ry = freely_reduce(ordinary_inverse(q[7]) + ordinary_inverse(q[3]))
    normalizers = {"r_x": rx, "r_y": ry, "c_x": freely_reduce(rx * 9), "c_y": freely_reduce(ry * 9)}
    for key, word in normalizers.items():
        count, digest = NORMALIZER_WORDS[key]
        require(len(word) == count and sha(canonical(list(word))[:-1]) == digest, "normalizer_literal_hash")
    require(epsilon(rx) == (2, 0) and epsilon(ry) == (0, 2), "normalizer_ordinary_exponents")
    dictionary = {f"r:{index + 1}": list(signed_letters(word)) for index, word in enumerate(relators)}
    dictionary.update({f"q:{index + 1}": list(word) for index, word in enumerate(q)})
    dictionary.update({f"pure:{index}": list(word) for index, word in enumerate(PURE_WORDS)})
    dictionary.update({f"normalizer:{key}": list(normalizers[key]) for key in ("r_x", "r_y")})
    return seal("literal-dictionary", {"relators": dictionary,
        "raw_sources": [{"file": name, "bytes": size, "sha256": digest} for name, (size, digest) in DATA_PINS.items()],
        "paper_relators_pointer": "/relators", "normalizer_relators_pointer": "/raw_q0_relators",
        "normalizer_raw_roster_sha256_without_LF": NORMALIZER_ROSTER_SHA,
        "normalizer_words": [{"name": key, "length": count, "word_sha256_without_LF": digest}
                             for key, (count, digest) in NORMALIZER_WORDS.items()],
        "normalizer_recipe": {"r_x": "free(q1*q6^-2*q7^4*q9)", "r_y": "free(q8^-1*q4^-1)"},
        "pure_order": [list(value) for value in CHARACTERS], "central_representative": "sr(0,1,2)=(0,1,-1)",
        "relator_normal_closure_claim": False, "eof": True})


def read_positioned(parents: Parents, role: str, name: str, offset: int, length: int, digest: str) -> Any:
    with parents.path(role, name).open("rb") as stream:
        stream.seek(offset)
        raw = stream.read(length)
    require(len(raw) == length and sha(raw) == digest and raw.endswith(b"\n"), "positioned_record_bytes")
    value = json.loads(raw.decode("ascii"))
    require(canonical(value) == raw, "positioned_canonical_record")
    return value


def rolling_record(record: Any, previous: str, field: str = "rolling_sha256") -> str:
    require(isinstance(record, dict) and digest_string(previous) and digest_string(record.get(field)),
            "rolling_record_type")
    unsigned = {key: value for key, value in record.items() if key != field}
    require(record[field] == sha(bytes.fromhex(previous) + canonical(unsigned)), "ordered_rolling_record")
    return record[field]


def authenticate_file_manifest(parents: Parents, role: str, name: str) -> Any:
    manifest = parents.read(role, name)
    check_seal(manifest)
    require(isinstance(manifest.get("files"), list), "manifest_file_roster")
    directory = name.rsplit("/", 1)[0]
    names = []
    for item in manifest["files"]:
        require(isinstance(item, dict) and {"file", "bytes", "sha256"} <= set(item), "manifest_payload_identity")
        relative_name(item["file"])
        require("/" not in item["file"], "manifest_direct_child")
        path = directory + "/" + item["file"]
        require(parents.pin(role, path) == {key: (path if key == "file" else item[key])
                                          for key in ("file", "bytes", "sha256")}, "manifest_actual_payload")
        names.append(item["file"])
    require(names == sorted(set(names)), "manifest_unique_sorted_files")
    actual = sorted(path.rsplit("/", 1)[1] for path in parents.files[role]
                    if path.startswith(directory + "/") and "/" not in path[len(directory) + 1:])
    extras = ["HEAD"] if role == "e" and name == "output/manifest.json" else []
    require(actual == sorted(names + ["manifest.json"] + extras), "manifest_directory_exact_EOF")
    return manifest


def read_selected_head(parents: Parents) -> tuple[Any, Any, Any, Any]:
    for name, (size, digest) in LOOP_FIXED_FILES.items():
        require(parents.pin("continuation", name) == {"file": name, "bytes": size, "sha256": digest},
                "same_frozen_continuation_owner_source_start")
    selected = parents.acceptance["selected"]
    keys = {"head", "result", "checker", "owner", "source", "start", "fixed",
            "completed_steps", "rank", "generation", "kind", "state_head",
            "target_remainder_sha256", "lambda_sha256", "terminal"}
    require(isinstance(selected, dict) and set(selected) == keys, "selected_acceptance_exact_fields")
    paths = {"head": "output/HEAD", "result": "output/result.json", "checker": "checker-result.json",
             "owner": "output/owner.json", "source": "output/source.json", "start": "output/start.json",
             "fixed": "output/fixed/manifest.json"}
    values = {}
    for key, name in paths.items():
        pin_entry(selected[key])
        require(selected[key] == parents.pin("continuation", name), "selected_actual_entry:" + key)
        values[key] = parents.read("continuation", name)
        check_seal(values[key])
    head, result, checked, start = (values[key] for key in ("head", "result", "checker", "start"))
    require(head["schema"] == LOOP_SCHEMA + ".head" and start["schema"] == LOOP_SCHEMA + ".start" and
            checked["schema"] == LOOP_SCHEMA + ".checker-result" and checked["status"] == "PASS",
            "whole_prefix_successful_receipt")
    require(values["source"]["producer_sha256"] == LOOP_PRODUCER_SHA and
            checked["checker_sha256"] == LOOP_CHECKER_SHA and
            values["source"]["python"] == parents.acceptance["runtime"]["python"] and
            values["source"]["numpy"] == parents.acceptance["runtime"]["numpy"], "frozen_P971_Cv2_and_runtime")
    require(start["rank"] == 1386 and start["generation"] == 8091 and start["completed_steps"] == 0 and
            start["external_e_attached"] is True and start["external_e_numerically_replayed"] is False,
            "external_E_once_in_start")
    completed = selected["completed_steps"]
    require(plain_int(completed, 0) and head["completed_steps"] == checked["completed_steps"] ==
            checked["prefix_steps_replayed"] == completed, "accepted_committed_count")
    require(head["rank"] == start["rank"] + completed and head["generation"] == start["generation"] + completed,
            "accepted_absolute_rank_generation")
    for key in ("rank", "generation", "kind", "state_head", "target_remainder_sha256", "lambda_sha256"):
        require(head[key] == checked[key] == selected[key], "selected_head_checker:" + key)
        require(result[key] == head[key], "selected_result_head:" + key)
    require(checked["terminal"] == selected["terminal"] == result["terminal"], "selected_terminal")
    for key, source in (("owner_sha256", "owner"), ("source_sha256", "source"), ("start_sha256", "start"),
                        ("fixed_manifest_sha256", "fixed")):
        expected = selected[source]["sha256"]
        require(head[key] == checked[key] == expected, "selected_parent_hash:" + key)
    require(checked["head_sha256"] == selected["head"]["sha256"] and
            checked["result_sha256"] == selected["result"]["sha256"], "whole_HEAD_result_hash")
    require(checked["all_new_committed_arrays_and_json_compared"] is True and
            checked["current_checkpoint_fully_compared"] is True and
            checked["full_four_character_scope"] is True and checked["all_four_B_summed_each_E"] is True and
            checked["section_equalities_each"] == 8059 and checked["chords_each"] == 54433 and
            checked["auxiliary_tests_each"] == 2 and checked["source_lower_trits_each_E"] == 96776 and
            checked["literal_modulus"] == 54, "accepted_full_prefix_scope")
    require(checked["python"] == parents.acceptance["runtime"]["python"] and
            checked["numpy"] == parents.acceptance["runtime"]["numpy"], "accepted_numerical_runtime")
    require(len(checked["steps"]) == completed and
            len(checked["snapshots"]) == completed + (head["current_snapshot_sha256"] is not None),
            "accepted_snapshot_cardinality")
    require(checked["current_snapshot_sha256"] == head["current_snapshot_sha256"] and
            checked["current_checkpoint_sha256"] == head["current_checkpoint_sha256"], "accepted_HEAD_cursor")
    validate_continuation_layout(parents, completed)
    return head, result, checked, start


def validate_continuation_layout(parents: Parents, completed: int) -> None:
    root = parents.roots["continuation"] / "output"
    top_files = {"owner.json", "source.json", "start.json", "HEAD", "result.json",
                 "resource-stop.json", "rejected.json"}
    top_dirs = {"fixed", "snapshots", "steps", "invocations"}
    pending = lambda name: re.fullmatch(r"\.[A-Za-z0-9_.-]+\.pending-[0-9a-f]{32}", name) is not None
    for path in root.iterdir():
        if path.name in top_files:
            require(path.is_file(), "HEAD_root_file_type")
        elif path.name in top_dirs:
            require(path.is_dir(), "HEAD_root_directory_type")
        else:
            require((path.is_file() and pending(path.name) and
                     any(path.name.startswith("." + name + ".pending-") for name in top_files)) or
                    (path.is_dir() and re.fullmatch(r"\.pending-fixed-[0-9a-f]{32}", path.name) is not None),
                    "only_named_root_tail")
    for folder, low, extra in (("snapshots", 0, 0), ("steps", 1, 1)):
        for path in (root / folder).iterdir():
            require(path.is_dir() and re.fullmatch(r"[0-9]{6}", path.name) is not None and
                    low <= int(path.name) <= completed + extra, "only_registered_numbered_tail")
    for path in (root / "invocations").iterdir():
        require(path.is_file() and (re.fullmatch(r"[0-9a-f]{32}\.json", path.name) is not None or pending(path.name)),
                "only_registered_invocation")
    # Successfully checked current/tail receipts remain authenticated premises.
    # This reader follows only steps 1..completed and never publishes their tails.


@dataclass
class TargetHistory:
    parents: Parents
    ancestors: Ancestors
    head: Any
    terminal: Any
    checked: Any
    start: Any
    pivots: list[dict[str, Any]] = field(default_factory=list)
    base_records: list[dict[str, Any]] = field(default_factory=list)
    lower_offers: list[int] = field(default_factory=list)
    named_parents: list[dict[str, Any]] = field(default_factory=list)
    current_state: str = OLD_STATE_SHA
    current_target: str = ""
    generation: int = 8059

    def instruction(self, pivot: dict[str, Any]) -> Any:
        entry = self.ancestors.entries[pivot["physical_recipe_ref"]]
        if entry["json_pointer"] is None:
            return read_positioned(self.parents, entry["parent_role"], entry["file"],
                                   entry["offset"], entry["length"], entry["record_sha256"])
        return json_pointer(self.parents.read(entry["parent_role"], entry["file"]), entry["json_pointer"])

    def add_row(self, role: str, name: str, offset: int, digest: str | None, lead: int) -> int:
        require(plain_int(lead, 0, PHYSICAL_TRITS - 1), "physical_lead")
        ref = self.ancestors.add("physical", role, name, offset=offset, length=PHYSICAL_BYTES)
        entry = self.ancestors.entries[ref]
        require(digest is None or entry["record_sha256"] == digest, "normalized_physical_row_hash")
        with self.parents.path(role, name).open("rb") as stream:
            stream.seek(offset)
            raw = stream.read(PHYSICAL_BYTES)
        require(len(raw) == PHYSICAL_BYTES and all(byte <= 80 for byte in raw) and
                (raw[lead // 4] // (3 ** (lead % 4))) % 3 == 1, "normalized_base3_packed_row_shape")
        return ref

    def add_delta(self, role: str, directory: str, raw_recipe: dict[str, Any], named_role: str,
                  *, legacy: bool = False, manifest_name: str | None = None) -> Any:
        instruction_name, result_name = directory + "/instruction.json", directory + "/result.json"
        instruction, result = self.parents.read(role, instruction_name), self.parents.read(role, result_name)
        check_seal(result)
        number = len(self.pivots)
        require(instruction["offer"] == self.generation and instruction["rank"] == number + 1 and
                instruction["generation"] == self.generation + 1 and
                instruction["physical_offset"] == number * PHYSICAL_BYTES, "delta_physical_global_identity")
        require(instruction["predecessor"] == self.current_state, "delta_instruction_predecessor")
        next_state = rolling_record(instruction, self.current_state)
        pivot = result["pivot"]
        require(pivot["scale"] == instruction["sigma"] and plain_int(instruction["sigma"], 1, 2) and
                pivot["lead"] == instruction["lead"], "delta_normalization_metadata")
        row_sha = pivot["normalized_sha256"]
        row_ref = self.add_row(role, directory + "/physical-normalized.bin", 0, row_sha, instruction["lead"])
        target = result["target"]
        target_scalar = target["scalar"]
        require(plain_int(target_scalar, 0, 2), "target_scalar_F3_not_bool")
        if legacy:
            check_seal(target)
            require(target["old_remainder_sha256"] == self.current_target and
                    target["rho2_sha256"] == RHO2_FILES["task640-payload/rho2.bin"][1] and
                    target["state_head"] == next_state and target["state_rank"] == number + 1,
                    "saved_legacy_target_identity")
            require(pivot["head_before"] == self.current_state and pivot["head_after"] == next_state and
                    pivot["rank_before"] == number and pivot["rank_after"] == number + 1 and
                    pivot["generation_before"] == self.generation and
                    pivot["generation_after"] == self.generation + 1 and
                    pivot["instruction_sha256"] == self.parents.pin(role, instruction_name)["sha256"],
                    "saved_legacy_pivot_identity")
            expected = [] if target_scalar == 0 else [number]
            require([item["pivot_id"] for item in target["new_reductions"]] == expected,
                    "legacy_single_target_delta")
            for item in target["new_reductions"]:
                require(item["scalar"] == target_scalar and item["row_sha256"] == row_sha and
                        item["offer"] == self.generation and item["lead"] == instruction["lead"] and
                        item["physical_offset"] == number * PHYSICAL_BYTES, "legacy_target_row_join")
        else:
            require(set(target) == {"parent_remainder_sha256", "remainder_sha256", "scalar"} and
                    target["parent_remainder_sha256"] == self.current_target and
                    instruction["target_scalar"] == target_scalar and
                    instruction["target_remainder_sha256"] == target["remainder_sha256"] and
                    instruction["physical_sha256"] == row_sha, "plain_single_target_delta")
            require(result["rank_before"] == number and result["rank_after"] == number + 1 and
                    result["generation_before"] == self.generation and
                    result["generation_after"] == self.generation + 1 and
                    result["parent_state_head"] == self.current_state and result["state_head"] == next_state,
                    "one_row_result_identity")
        target_name = directory + "/target-remainder.bin"
        require(self.parents.pin(role, target_name)["bytes"] == PHYSICAL_BYTES and
                self.parents.pin(role, target_name)["sha256"] == target["remainder_sha256"], "actual_target_payload")
        if role in ("e", "continuation"):
            require(result["target_derivation"] == {
                "mode": "derived", "original_rho2_packed_sha256": RHO2_FILES["task640-payload/rho2.bin"][1],
                "original_rho2_directly_read": False, "accepted_target_derivation_parents": self.named_parents,
                "identity": "parent_remainder - new_remainder = target.scalar * new_normalized_row",
                "new_delta": {"instruction_sha256": self.parents.pin(role, instruction_name)["sha256"],
                    "normalized_sha256": row_sha, "state_head": next_state, "target_sha256": sha(canonical(target))}},
                "E_explicit_original_rho2_and_last_target_delta")
        instruction_ref = self.ancestors.add("physical", role, instruction_name, pointer="", value=instruction)
        target_ref = self.ancestors.add("target", role, result_name, pointer="/target", value=result)
        self.pivots.append({"pivot_id": number, "offer": self.generation, "lead": instruction["lead"],
            "sigma": instruction["sigma"], "target_scalar": target_scalar, "literal_exponent": signrep(target_scalar),
            "physical_recipe_ref": instruction_ref, "row_ref": row_ref, "target_delta_ref": target_ref,
            "scope_sha256": self.parents.pin(role, instruction_name)["sha256"],
            "raw_recipe": raw_recipe, "state_head": next_state})
        manifest_name = manifest_name or directory + "/manifest.json"
        parent = {"role": named_role, "manifest_sha256": self.parents.pin(role, manifest_name)["sha256"],
            "result_sha256": self.parents.pin(role, result_name)["sha256"],
            "target_sha256": sha(canonical(target)), "state_head": next_state}
        if role in ("e", "continuation"):
            parent["instruction_sha256"] = self.parents.pin(role, instruction_name)["sha256"]
        self.named_parents.append(parent)
        self.current_state, self.current_target = next_state, target["remainder_sha256"]
        self.generation += 1
        return instruction, result

    def output(self) -> dict[str, Any]:
        last = self.pivots[-1]
        if last["raw_recipe"]["kind"] == "e":
            raw = last["raw_recipe"]
            prefix = raw["base"] + ("/physical" if raw["parent_role"] == "continuation" else "")
            residual_role, residual_name = raw["parent_role"], prefix + "/target-remainder.bin"
        else:
            raise ValueError("accepted_start_contains_external_E")
        residual = self.parents.path(residual_role, residual_name).read_bytes()
        require(sha(residual) == self.current_target and len(residual) == PHYSICAL_BYTES, "history_final_target")
        zero = not any(residual)
        if zero:
            require(self.head["kind"] == "LinearMembershipCandidate" and self.head["lambda_sha256"] is None and
                    self.terminal["terminal"] == "LINEAR_MEMBERSHIP_CANDIDATE", "positive_zero_HEAD_gate")
        else:
            require(self.head["kind"] == "Separator" and digest_string(self.head["lambda_sha256"]) and
                    self.terminal["terminal"] != "LINEAR_MEMBERSHIP_CANDIDATE", "nonzero_not_positive")
        return seal("target-history", {"accepted_head_sha256": self.parents.acceptance["selected"]["head"]["sha256"],
            "accepted_result_sha256": self.parents.acceptance["selected"]["result"]["sha256"],
            "accepted_checker_sha256": self.parents.acceptance["selected"]["checker"]["sha256"],
            "completed_steps": self.head["completed_steps"], "rank": len(self.pivots), "generation": self.generation,
            "state_head": self.current_state, "kind": self.head["kind"], "terminal": self.terminal["terminal"],
            "pivots": self.pivots, "base_offers": self.base_records, "lower_pivot_offers": self.lower_offers,
            "target_scalars": [item["target_scalar"] for item in self.pivots],
            "residual": {"parent_role": residual_role, **self.parents.pin(residual_role, residual_name),
                         "trits": PHYSICAL_TRITS, "zero": zero},
            "original_rho2_packed_sha256": RHO2_FILES["task640-payload/rho2.bin"][1],
            "target_derivation_mode": "DERIVED_FROM_ACCEPTED_NUMERICAL_PARENTS",
            "accepted_target_derivation_parents": self.named_parents,
            "identity": "rho2 = residual + insertion_order_sum(target_scalar * normalized_physical_row)",
            "positive_applicability": "LINEAR_ZERO_CANDIDATE" if zero else "NOT_APPLICABLE",
            "uncommitted_tail_appended": False, "old_numerical_replay": False, "eof": True, **ASSURANCE})


def read_base_target(history: TargetHistory) -> None:
    parents, ancestors = history.parents, history.ancestors
    result = parents.read("state", "output/result.json")
    target = result["target_reduction"]
    state_manifest = parents.read("state", "state/manifest.json")
    state_head = parents.read("state", "state/HEAD")
    require(state_head["generation"] == 8059 and state_head["rank"] == 1354 and state_head["eof"] is True and
            state_head["rolling_head"] == OLD_STATE_SHA and
            state_head["manifest_sha256"] == parents.pin("state", "state/manifest.json")["sha256"],
            "base_state_HEAD_manifest")
    require(target["state_generation"] == 8059 and target["state_rank"] == 1354 and
            target["state_head"] == OLD_STATE_SHA and target["rho2_sha256"] ==
            RHO2_FILES["task640-payload/rho2.bin"][1], "base_target_rho2_identity")
    coefficients = [0] * 1354
    previous_id = -1
    for item in target["reductions"]:
        number, scalar = item["pivot_id"], item["scalar"]
        require(plain_int(number, previous_id + 1, 1353) and plain_int(scalar, 1, 2), "base_target_ordered_reductions")
        coefficients[number], previous_id = scalar, number
    target_ref = ancestors.add("target", "state", "output/result.json", pointer="/target_reduction", value=result)
    previous_outer, previous_inner, offset = "0" * 64, "0" * 64, 0
    with parents.path("state", "state/instructions.jsonl").open("rb") as stream:
        for offer, raw in enumerate(stream):
            require(raw.endswith(b"\n"), "base_instruction_final_LF")
            record = json.loads(raw.decode("ascii"))
            require(canonical(record) == raw and record["offer"] == offer, "base_instruction_order")
            previous_outer = rolling_record(record, previous_outer)
            conn = record["source"]
            require(conn["offer"] == offer and conn["source"]["node"] == offer and
                    conn["kind"] in ("pivot", "connection"), "base_full_nested_Conn")
            previous_inner = rolling_record(conn, previous_inner)
            for pair in conn["reductions"]:
                require(isinstance(pair, list) and len(pair) == 2 and
                        plain_int(pair[0], 0, len(history.lower_offers) - 1) and plain_int(pair[1], 1, 2),
                        "Conn_prior_lower_reduction")
            lower_id = None
            if conn["kind"] == "pivot":
                require(record["kind"] == "skipped" and plain_int(conn["sigma"], 1, 2), "retained_skipped_lower_pivot")
                lower_id = len(history.lower_offers)
                history.lower_offers.append(offer)
            else:
                require(conn["sigma"] is None and conn["lower_zero"] is True, "Conn_raw_has_no_outer_sigma")
            location = {"offer": offer, "offset": offset, "length": len(raw), "sha256": sha(raw),
                        "physical_kind": record["kind"], "conn_kind": conn["kind"], "lower_pivot_id": lower_id,
                        "p1_source": conn["source"]}
            history.base_records.append(location)
            if record["kind"] == "physical_pivot":
                number = len(history.pivots)
                require(record["physical_offset"] == number * PHYSICAL_BYTES and record["rank"] == number + 1 and
                        plain_int(record["sigma"], 1, 2) and conn["kind"] == "connection", "base_pivot_identity")
                for pair in record["reductions"]:
                    require(isinstance(pair, list) and len(pair) == 2 and
                            plain_int(pair[0], 0, number - 1) and plain_int(pair[1], 1, 2), "base_prior_physical")
                instruction_ref = ancestors.add("physical", "state", "state/instructions.jsonl",
                                                offset=offset, length=len(raw))
                row_ref = history.add_row("state", "state/physical.bin", number * PHYSICAL_BYTES, None, record["lead"])
                history.pivots.append({"pivot_id": number, "offer": offer, "lead": record["lead"],
                    "sigma": record["sigma"], "target_scalar": coefficients[number],
                    "literal_exponent": signrep(coefficients[number]), "physical_recipe_ref": instruction_ref,
                    "row_ref": row_ref, "target_delta_ref": target_ref,
                    "scope_sha256": parents.pin("state", "state/manifest.json")["sha256"],
                    "raw_recipe": {"kind": "conn", "offer": offer}, "state_head": previous_outer})
            else:
                require(record["kind"] in ("skipped", "physical_dependent"), "known_base_physical_instruction")
            offset += len(raw)
            if (offer + 1) % 512 == 0:
                progress("base-record-closure", offers=offer + 1, pivots=len(history.pivots))
    pin = parents.pin("state", "state/instructions.jsonl")
    require(offset == pin["bytes"] and len(history.base_records) == 8059 and
            len(history.pivots) == 1354 and previous_outer == OLD_STATE_SHA, "base_entire_instruction_EOF")
    require(state_manifest["physical"]["bytes"] == parents.pin("state", "state/physical.bin")["bytes"] ==
            1354 * PHYSICAL_BYTES, "base_physical_store_EOF")
    for item in target["reductions"]:
        pivot = history.pivots[item["pivot_id"]]
        require(item["offer"] == pivot["offer"] and item["lead"] == pivot["lead"] and
                item["physical_sha256"] == ancestors.entries[pivot["row_ref"]]["record_sha256"],
                "base_target_normalized_row_join")
    remainder = bytes.fromhex(target["remainder"])
    require(len(remainder) == PHYSICAL_BYTES and sha(remainder) == target["remainder_sha256"], "base_remainder_bytes")
    history.current_target = target["remainder_sha256"]
    history.named_parents.append({"role": "base",
        "manifest_sha256": parents.pin("state", "state/manifest.json")["sha256"],
        "result_sha256": parents.pin("state", "output/result.json")["sha256"],
        "target_sha256": sha(canonical(target)), "state_head": OLD_STATE_SHA})


PHASE_ORDER = ("section", "cochain", "tree", "raw", "source", "primal", "p1", "B", "physical")


def phase_directory(snapshot: str, phase: str) -> str:
    require(phase in PHASE_ORDER, "known_snapshot_phase")
    return snapshot + ("/" if phase in PHASE_ORDER[:3] else "/e/") + phase


def e_recipe(role: str, snapshot: str | None = None) -> dict[str, Any]:
    require((role == "e" and snapshot is None) or (role == "continuation" and snapshot is not None), "typed_E_origin")
    flat = role == "e"
    base = "output" if flat else "output/snapshots/" + str(snapshot) + "/e"
    return {"kind": "e", "parent_role": role, "base": base,
        "key": "external-e" if flat else "loop/" + str(snapshot),
        "raw_file": base + ("/" if flat else "/raw/") + "raw-word.json",
        "primal_file": base + ("/" if flat else "/primal/") + "p1-reductions.json",
        "source_correction_file": base + ("/" if flat else "/p1/") + "source-correction.json",
        "p1_roots_file": base + ("/" if flat else "/p1/") + "p1-roots.json",
        "physical_literal_file": base + ("/" if flat else "/physical/") + "physical-literal.json",
        "B_file": None if flat else base + "/B/B.json",
        "geometry_role": "oracle" if flat else "continuation",
        "geometry_base": "output/geometry" if flat else "output/fixed",
        "witness_role": "oracle" if flat else "continuation",
        "witness_file": "output/tree/witness.json" if flat else
                        "output/snapshots/" + str(snapshot) + "/tree/witness.json"}


def loop_snapshot_directory(number: int) -> str:
    require(plain_int(number, 1), "positive_committed_step_number")
    return f"output/snapshots/{number - 1:06d}"


def read_loop_step(history: TargetHistory, number: int, previous_manifest: str | None) -> str:
    parents, ancestors = history.parents, history.ancestors
    directory = loop_snapshot_directory(number)
    step_file = f"output/steps/{number:06d}/manifest.json"
    step = parents.read("continuation", step_file)
    check_seal(step, LOOP_SCHEMA + ".step-manifest")
    snapshot = parents.read("continuation", directory + "/start.json")
    check_seal(snapshot, LOOP_SCHEMA + ".snapshot")
    snapshot_sha = parents.pin("continuation", directory + "/start.json")["sha256"]
    require(step["step"] == number and snapshot["step"] == number - 1 and
            snapshot["rank"] == len(history.pivots) and snapshot["generation"] == history.generation and
            snapshot["state_head"] == history.current_state and
            snapshot["target_remainder_sha256"] == history.current_target and
            snapshot["accepted_target_derivation_parents"] == history.named_parents,
            "saved_snapshot_before_append")
    require(step["snapshot_sha256"] == snapshot_sha and
            step["predecessor_step_manifest_sha256"] == previous_manifest and
            step["parent_state_head"] == history.current_state and step["phase_eof"] == list(PHASE_ORDER),
            "committed_step_snapshot_chain")
    for field in ("owner_sha256", "source_sha256", "start_sha256", "fixed_manifest_sha256"):
        require(step[field] == snapshot[field] == history.head[field], "same_owner_snapshot_binding")
    previous_phase = None
    require(set(step["phase_manifests"]) == set(PHASE_ORDER), "nine_committed_phases")
    for phase in PHASE_ORDER:
        path = phase_directory(directory, phase) + "/manifest.json"
        phase_value = authenticate_file_manifest(parents, "continuation", path)
        require(phase_value["schema"] == LOOP_SCHEMA + ".phase-manifest" and phase_value["phase"] == phase and
                phase_value["snapshot_sha256"] == snapshot_sha and
                phase_value["previous_phase_manifest_sha256"] == previous_phase, "ordered_typed_phase_chain")
        for field in ("owner_sha256", "source_sha256", "fixed_manifest_sha256"):
            require(phase_value[field] == history.head[field], "same_owner_phase")
        previous_phase = parents.pin("continuation", path)["sha256"]
        require(step["phase_manifests"][phase] == previous_phase, "step_exact_phase_file_hash")
    oracle_file = directory + "/oracle-manifest.json"
    oracle = parents.read("continuation", oracle_file)
    check_seal(oracle, LOOP_SCHEMA + ".oracle-manifest")
    require(oracle["snapshot_sha256"] == snapshot_sha and oracle["terminal"] == "VIOLATION_CANDIDATE" and
            oracle["stage_eof"] == list(PHASE_ORDER[:3]) and oracle["stage_manifests"] ==
            {phase: step["phase_manifests"][phase] for phase in PHASE_ORDER[:3]} and
            step["oracle_manifest_sha256"] == parents.pin("continuation", oracle_file)["sha256"] and
            oracle["witness_sha256"] == step["witness_sha256"] ==
            parents.pin("continuation", directory + "/tree/witness.json")["sha256"] and
            oracle["result_sha256"] == parents.pin("continuation", directory + "/oracle-result.json")["sha256"],
            "one_snapshot_complete_oracle_witness")
    instruction, result = history.add_delta("continuation", directory + "/e/physical",
        e_recipe("continuation", f"{number - 1:06d}"), f"loop-e-{number:06d}", manifest_name=step_file)
    for key in ("rank", "generation", "state_head", "target_remainder_sha256"):
        expected = instruction["rolling_sha256"] if key == "state_head" else instruction[key]
        require(step[key] == expected, "step_after_state:" + key)
    require(step["instruction_sha256"] == parents.pin("continuation", directory + "/e/physical/instruction.json")["sha256"] and
            step["result_sha256"] == parents.pin("continuation", directory + "/e/physical/result.json")["sha256"] and
            step["physical_normalized_sha256"] == instruction["physical_sha256"], "step_physical_payloads")
    saved_c = history.checked["steps"][number - 1]
    require(saved_c["step"] == number and saved_c["manifest_sha256"] ==
            parents.pin("continuation", step_file)["sha256"] and saved_c["state_head"] == step["state_head"] and
            saved_c["rank"] == step["rank"] and saved_c["generation"] == step["generation"] and
            saved_c["target_scalar"] == instruction["target_scalar"], "accepted_checker_exact_step")
    saved_snapshot = history.checked["snapshots"][number - 1]
    require(saved_snapshot["step"] == number - 1 and saved_snapshot["snapshot_sha256"] == snapshot_sha and
            saved_snapshot["phase_manifests"] == step["phase_manifests"] and
            saved_snapshot["oracle_manifest_sha256"] == step["oracle_manifest_sha256"],
            "accepted_checker_exact_snapshot")
    ancestors.add("target", "continuation", step_file)
    progress("committed-target-step", step=number, pivots=len(history.pivots))
    return parents.pin("continuation", step_file)["sha256"]


def read_target_history(parents: Parents, ancestors: Ancestors) -> TargetHistory:
    head, terminal, checked, start = read_selected_head(parents)
    history = TargetHistory(parents, ancestors, head, terminal, checked, start)
    read_base_target(history)
    for role, named in (("delta", "seed30"), ("seed34", "seed34")):
        authenticate_file_manifest(parents, role, "output/manifest.json")
        history.add_delta(role, "output", {"kind": "legacy-seed", "parent_role": role,
            "file": "output/result.json", "pointer": "/ancestry"}, named, legacy=True)
    previous = None
    for number in range(1, 4):
        directory = f"output/steps/{number:06d}"
        manifest = authenticate_file_manifest(parents, "packet", directory + "/manifest.json")
        require(manifest["step"] == number and manifest["parent_state_head"] == history.current_state and
                manifest["predecessor_step_manifest_sha256"] == previous, "accepted_packet_chain")
        instruction = parents.read("packet", directory + "/instruction.json")
        seed = instruction["selected"]["seed"]
        require(plain_int(seed, 0, 43), "bare_seed_zero_based")
        history.add_delta("packet", directory, {"kind": "packet-seed", "parent_role": "packet",
            "file": "output/packet/relations.json", "pointer": "/seeds/" + str(seed),
            "seed": seed, "character": instruction["selected"]["character"]}, f"packet-step-{number}")
        require(manifest["state_head"] == history.current_state and manifest["rank"] == len(history.pivots) and
                manifest["generation"] == history.generation, "packet_after_state")
        previous = parents.pin("packet", directory + "/manifest.json")["sha256"]
    require(len(history.pivots) == 1359, "accepted_fixed_packet_rank")
    previous = None
    ref_head = parents.read("refinement", "output/HEAD")
    require(ref_head["completed_steps"] == 26, "accepted_full_origin_count")
    for number in range(1, 27):
        directory = f"output/steps/{number:06d}"
        manifest = authenticate_file_manifest(parents, "refinement", directory + "/manifest.json")
        require(manifest["step"] == number and manifest["parent_state_head"] == history.current_state and
                manifest["predecessor_step_manifest_sha256"] == previous, "accepted_refinement_chain")
        materialization = parents.read("refinement", directory + "/materialization.json")
        check_seal(materialization)
        instruction, _ = history.add_delta("refinement", directory, {"kind": "refinement",
            "parent_role": "refinement", "file": directory + "/materialization.json", "pointer": ""},
            f"refinement-step-{number}")
        require(instruction["materialization_sha256"] == parents.pin("refinement", directory + "/materialization.json")["sha256"] and
                manifest["state_head"] == history.current_state, "refinement_materialization_join")
        previous = parents.pin("refinement", directory + "/manifest.json")["sha256"]
    require(len(history.pivots) == 1385 and ref_head["state_head"] == history.current_state and
            ref_head["target_remainder_sha256"] == history.current_target, "accepted_refinement_final_HEAD")
    e_manifest = authenticate_file_manifest(parents, "e", "output/manifest.json")
    _, e_result = history.add_delta("e", "output", e_recipe("e"), "external-e")
    e_head = parents.read("e", "output/HEAD")
    check_seal(e_head)
    require(e_head["manifest_sha256"] == parents.pin("e", "output/manifest.json")["sha256"] and
            e_manifest["result_sha256"] == parents.pin("e", "output/result.json")["sha256"] and
            e_head["state_head"] == e_manifest["state_head"] == history.current_state and
            e_head["rank"] == e_result["rank_after"] == len(history.pivots) and
            e_head["generation"] == e_result["generation_after"] == history.generation,
            "external_E_HEAD_separately_authenticated")
    require(len(history.pivots) == start["rank"] and history.generation == start["generation"] and
            history.current_state == start["state_head"] and history.current_target == start["target_remainder_sha256"] and
            history.named_parents == start["accepted_target_derivation_parents"], "exact_external_E_start_premise")
    require(start["lambda_rho2"]["original_rho2_packed_sha256"] == RHO2_FILES["task640-payload/rho2.bin"][1] and
            start["lambda_rho2"]["accepted_target_derivation_parents"] == history.named_parents, "original_rho2_named_chain")
    previous = None
    for number in range(1, head["completed_steps"] + 1):
        previous = read_loop_step(history, number, previous)
    require(previous == head["last_step_manifest_sha256"] and len(history.pivots) == head["rank"] and
            history.generation == head["generation"] and history.current_state == head["state_head"] and
            history.current_target == head["target_remainder_sha256"], "read_only_accepted_HEAD_exact_end")
    if head["kind"] == "Separator":
        require(terminal["lambda_rho2"]["accepted_target_derivation_parents"] == history.named_parents and
                terminal["lambda_rho2"]["original_rho2_packed_sha256"] == RHO2_FILES["task640-payload/rho2.bin"][1],
                "terminal_original_rho2_DERIVED_chain")
    history.output()
    return history


def p1_location(node: int) -> tuple[str, int, int, int]:
    require(plain_int(node, 0, P1_ROWS - 1), "global_P1_node")
    kind, offsets, ranks = ("old", OLD_OFFSETS, OLD_RANKS) if node < NEW_OFFSETS[0] else ("new", NEW_OFFSETS, NEW_RANKS)
    owner = next(owner for owner in range(4) if offsets[owner] <= node < offsets[owner] + ranks[owner])
    return kind, owner, node - offsets[owner], offsets[owner]


@dataclass
class LiteralParents:
    parents: Parents
    ancestors: Ancestors
    history: TargetHistory
    prepare_name: str
    prepare: dict[str, Any]
    blocks: list[dict[str, Any]]
    block_names: list[str]
    index: dict[str, Any]
    p1_manifest: dict[str, Any]
    dictionary: dict[str, Any]

    def body_record(self, node: int) -> tuple[dict[str, Any], str, str, str, dict[str, Any]]:
        kind, owner, local, _ = p1_location(node)
        if kind == "old":
            pointer = f"/old_blocks/{owner}/record/dag_nodes/{local}"
            return self.prepare["old_blocks"][owner]["record"]["dag_nodes"][local], "prepare", self.prepare_name, pointer, self.prepare
        pointer = f"/dag_nodes/{local}"
        return self.blocks[owner]["dag_nodes"][local], f"block-{owner}", self.block_names[owner], pointer, self.blocks[owner]

    def p1_record(self, node: int) -> Any:
        ref = self.index["references"][node]
        record = read_positioned(self.parents, "p1", self.p1_manifest["instruction"]["path"],
            ref["instruction_offset"], ref["instruction_length"], ref["instruction_sha256"])
        validate_p1_record(self, node, record, ref)
        return record

    def p1_refs(self, node: int, record: Any) -> list[int]:
        index = self.index["references"][node]
        body, role, name, pointer, container = self.body_record(node)
        record_ref = self.ancestors.add("p1", "p1", self.p1_manifest["instruction"]["path"],
            offset=index["instruction_offset"], length=index["instruction_length"])
        body_ref = self.ancestors.add("p1", role, name, pointer=pointer, value=container)
        row_ref = self.ancestors.add("p1", "p1", self.p1_manifest["cache"]["path"], offset=node * 36288, length=36288)
        require(self.ancestors.entries[row_ref]["record_sha256"] == index["row_sha256"], "P1_actual_cache_row")
        return [record_ref, body_ref, row_ref]


def validate_p1_record(literal: LiteralParents, node: int, record: Any, ref: Any) -> None:
    kind, owner, local, base = p1_location(node)
    body, _, _, _, _ = literal.body_record(node)
    require(record["node"] == ref["node"] == node and record["origin"] == body["origin"] and
            record["reductions"] == body["reductions"] and record["scale"] == body["scale"] == ref["scale"] and
            body["pivot"] == local and plain_int(record["scale"], 1, 2), "P1_canonical_Task554_recipe")
    require(sha(canonical(record["origin"])) == ref["origin_sha256"] and
            sha(canonical(record["reductions"])) == ref["reductions_sha256"] and
            record["literal_input_sha256"] == ref["literal_input_sha256"] and
            record["ancestry_sha256"] == ref["ancestry_sha256"] and record["predecessor"] == ref["predecessor"] and
            record["p1_sha256"] == ref["p1_sha256"], "P1_exact_index_fields")
    require(record["offset"] == node * 36288 and record["length"] == 36288 and
            record["row_receipt"] == {"offset": node * 36288, "length": 36288, "sha256": ref["row_sha256"]},
            "P1_cache_global_offset")
    reduction_rows = []
    for pair in record["reductions"]:
        require(isinstance(pair, list) and len(pair) == 2 and plain_int(pair[0], 0, local - 1) and
                plain_int(pair[1], 1, 2), "P1_owner_local_prior_reduction")
        reduction_rows.append(literal.index["references"][base + pair[0]]["row_sha256"])
    require(record["reduction_parent_sha256"] == reduction_rows, "P1_all_ordered_reduction_parent_rows")
    origin = record["origin"]
    if origin["kind"] == "actor":
        require(set(origin) == {"kind", "parent", "letter"} and plain_int(origin["parent"], 0, local - 1) and
                type(origin["letter"]) is int and origin["letter"] in ACTORS, "P1_actor_local_parent")
        require(record["literal_input_sha256"] == sha(canonical({"kind": "actor", "letter": origin["letter"],
                                                                 "actor_order": list(ACTORS)})), "P1_actor_literal")
    elif kind == "old":
        require(set(origin) == {"kind", "seed"} and origin["kind"] == "projected_seed" and
                plain_int(origin["seed"], 1, 44), "P1_one_based_projected_seed")
        word = literal.dictionary["relators"]["r:" + str(origin["seed"])]
        require(record["literal_input_sha256"] == sha(canonical({"kind": "projected_seed", "seed": origin["seed"],
                    "word": word, "character": list(CHARACTERS[owner])})), "P1_projected_seed_literal")
    else:
        require(set(origin) == {"kind", "origin"} and origin["kind"] == "defect" and
                plain_int(origin["origin"], 0, len(literal.prepare["defect_origins"]) - 1), "P1_old_defect_id")
        old = literal.prepare["defect_origins"][origin["origin"]]
        if old["kind"] == "seed":
            body_literal = {"kind": "seed", "seed": old["seed"],
                "word": literal.dictionary["relators"]["r:" + str(old["seed"])],
                "character": list(CHARACTERS[old["lower_character"]])}
        else:
            require(old["kind"] == "transition", "old_defect_transition")
            body_literal = {"kind": "transition", "pivot": old["pivot"], "letter": old["letter"],
                            "character": list(CHARACTERS[old["lower_character"]])}
        require(record["old_defect_literal_input_sha256"] == sha(canonical(body_literal)),
                "P1_same_old_defect_literal_parent")


def load_literal_parents(parents: Parents, ancestors: Ancestors, history: TargetHistory,
                         dictionary: Any) -> LiteralParents:
    prepare_name = "prepare." + PREPARE_BODY_SHA + ".json"
    head = parents.read("prepare", "prepare.HEAD", strict=False)
    require(head["body_sha256"] == PREPARE_BODY_SHA and parents.pin("prepare", prepare_name)["sha256"] ==
            PREPARE_BODY_SHA, "prepare_actual_body")
    body = parents.read("prepare", prepare_name, strict=False)
    prepare = {"old_blocks": body["old_blocks"], "defect_origins": body["defect_origins"]}
    del body
    for owner, old in enumerate(prepare["old_blocks"]):
        require(old["rank"] == OLD_RANKS[owner] and old["character_index"] == owner and
                old["record"]["actor_order"] == list(ACTORS) and
                len(old["record"]["dag_nodes"]) == OLD_RANKS[owner], "old_literal_block_identity")
    blocks, block_names = [], []
    for owner, digest in enumerate(BLOCK_BODY_SHAS):
        role, name = f"block-{owner}", f"block-{owner}.{digest}.json"
        head = parents.read(role, f"block-{owner}.HEAD", strict=False)
        require(head["body_sha256"] == digest and parents.pin(role, name)["sha256"] == digest, "new_actual_body")
        body = parents.read(role, name, strict=False)
        require(body["character_index"] == owner and body["rank"] == NEW_RANKS[owner] and
                body["actor_order"] == list(ACTORS) and len(body["dag_nodes"]) == NEW_RANKS[owner],
                "new_literal_block_identity")
        blocks.append({key: body[key] for key in ("dag_nodes", "origin_reductions", "actor_transitions", "basis_blob")})
        block_names.append(name)
        del body
        progress("literal-body-read", owner=owner)
    p1_manifest = parents.read("p1", "manifest.json", strict=False)
    require(parents.pin("p1", "manifest.json")["sha256"] == P1_MANIFEST_SHA and
            p1_manifest["rows"] == P1_ROWS and p1_manifest["actor_order"] == list(ACTORS), "accepted_P1_manifest")
    ip = p1_manifest["instruction"]
    require((ip["bytes"], ip["sha256"]) == P1_INSTRUCTIONS_PIN and ip["rows"] == P1_ROWS and ip["eof"] is True and
            ip["final_lf"] is True and parents.pin("p1", ip["path"]) ==
            {"file": ip["path"], "bytes": ip["bytes"], "sha256": ip["sha256"]}, "P1_instruction_whole_EOF")
    cp = p1_manifest["cache"]
    require(cp["rows"] == P1_ROWS and cp["bytes"] == 36288 * P1_ROWS and cp["eof"] is True and
            parents.pin("p1", cp["path"]) == {"file": cp["path"], "bytes": cp["bytes"], "sha256": cp["sha256"]},
            "P1_cache_whole_EOF")
    index = parents.read("continuation", "output/fixed/canonical-index.json")
    check_seal(index)
    require(index["rows"] == P1_ROWS and len(index["references"]) == P1_ROWS and
            index["p1_manifest_sha256"] == P1_MANIFEST_SHA and index["instruction_sha256"] == ip["sha256"] and
            index["cache_sha256"] == cp["sha256"], "fixed_canonical_index_same_P1")
    literal = LiteralParents(parents, ancestors, history, prepare_name, prepare, blocks, block_names, index,
                             p1_manifest, dictionary)
    offset, previous, count = 0, "0" * 64, 0
    with parents.path("p1", ip["path"]).open("rb") as stream:
        for node, raw in enumerate(stream):
            require(node < P1_ROWS and raw.endswith(b"\n"), "P1_full_instruction_stream")
            record = json.loads(raw.decode("ascii"))
            ref = index["references"][node]
            require(canonical(record) == raw and ref["instruction_offset"] == offset and
                    ref["instruction_length"] == len(raw) and ref["instruction_sha256"] == sha(raw) and
                    record["predecessor"] == previous, "P1_continuous_positioned_chain")
            previous = rolling_record(record, previous, "ancestry_sha256")
            validate_p1_record(literal, node, record, ref)
            source = history.base_records[node]["p1_source"]
            require(source == {"node": node, "instruction_sha256": ref["instruction_sha256"],
                "p1_sha256": ref["p1_sha256"], "cache_row_sha256": ref["row_sha256"],
                "predecessor": ref["predecessor"], "ancestry_sha256": ref["ancestry_sha256"]},
                "all_Conn_offers_same_P1")
            offset += len(raw)
            count += 1
            if count % 512 == 0:
                progress("literal-P1-full-index", rows=count)
    require(count == P1_ROWS and offset == ip["bytes"] and previous == ip["final_head"], "all_P1_literal_EOF")
    return literal


Symbol = tuple[str, str, str]


def check_four_B(b: Any, byte_count: int, by_character_sha: str, source_sha: str, witness_sha: str) -> None:
    check_seal(b)
    require(byte_count == 4 * PHYSICAL_BYTES and b["characters"] == [0, 1, 2, 3] and
            b["all_four_summed"] is True and b["eof"] is True and
            b["by_character_sha256"] == by_character_sha and b["source_correction_sha256"] == source_sha and
            b["witness_sha256"] == witness_sha, "E_saved_all_four_B_scope")


class TargetWordCompiler:
    def __init__(self, history: TargetHistory, literal: LiteralParents, dag: WordDAG):
        self.history, self.literal, self.dag = history, literal, dag
        self.parents, self.ancestors = history.parents, history.ancestors
        self.recipe_refs: dict[Symbol, list[int]] = {}
        self.raw_origins: dict[str, dict[str, Any]] = {}
        self.raw_data: dict[str, Any] = {}
        self.geometries: dict[str, Any] = {}
        self.raw_streams: list[dict[str, Any]] = []
        self.symbol_order: list[dict[str, Any]] = []
        self.normalizer_origin_refs: dict[str, list[int]] = {}

    def symbol(self, namespace: str, key: int | str, scope: str | None = None) -> Symbol:
        if scope is None:
            if namespace == "p1":
                scope = P1_MANIFEST_SHA
            elif namespace == "old-defect":
                scope = PREPARE_BODY_SHA
            elif namespace in ("conn-lower", "conn-raw"):
                scope = self.parents.pin("state", "state/manifest.json")["sha256"]
            elif namespace == "physical":
                scope = self.history.pivots[int(key)]["scope_sha256"]
            elif namespace == "normalizer":
                scope = self.dag.dictionary_sha256
            else:
                raise ValueError("explicit_symbol_scope")
        return namespace, str(key), scope

    def resolve(self, symbol: Symbol) -> int:
        if symbol in self.dag.symbols:
            return self.dag.symbols[symbol]
        active: set[Symbol] = set()
        stack: list[tuple[Symbol, Any]] = []
        current, sent = symbol, None
        while True:
            if current is not None:
                require(current not in active and current not in self.dag.symbols, "prior_only_symbol_DAG_no_cycle")
                active.add(current)
                self.recipe_refs[current] = []
                stack.append((current, self.build(current)))
                sent, current = None, None
            item, generator = stack[-1]
            try:
                dependency = generator.send(sent)
                require(isinstance(dependency, tuple) and len(dependency) == 3 and
                        dependency[0] in REF_NAMESPACES, "typed_symbol_dependency")
                if dependency in self.dag.symbols:
                    sent = self.dag.symbols[dependency]
                else:
                    current = dependency
            except StopIteration as finished:
                word = finished.value
                require(plain_int(word, 0, len(self.dag.hashes) - 1), "compiled_symbol_word")
                node = self.dag.ref(*item, word, self.recipe_refs[item])
                self.symbol_order.append({"namespace": item[0], "key": item[1], "scope_sha256": item[2],
                                          "node": node, "node_sha256": self.dag.hashes[node]})
                active.remove(item)
                stack.pop()
                if not stack:
                    return node
                sent, current = node, None
            check_resources("literal-DFS")

    def project(self, word: int, character: int, refs: Iterable[int] = ()) -> int:
        require(plain_int(character, 0, 3), "literal_character")
        factors = []
        for index, parity in enumerate(CHARACTERS):
            sign = -1 if sum(a * b for a, b in zip(CHARACTERS[character], parity)) % 2 else 1
            actor = self.dag.rel("pure:" + str(index), refs)
            factors.append(self.dag.power(self.dag.act(actor, word, refs), sign, refs))
        return self.dag.product(factors, refs)

    def build(self, symbol: Symbol) -> Any:
        namespace, key, _ = symbol
        if namespace == "p1":
            return (yield from self.build_p1(symbol, int(key)))
        if namespace == "old-defect":
            return (yield from self.build_defect(symbol, int(key)))
        if namespace in ("conn-lower", "conn-raw"):
            return (yield from self.build_conn(symbol, int(key), namespace == "conn-lower"))
        if namespace == "physical":
            return (yield from self.build_physical(symbol, int(key)))
        if namespace == "raw-e":
            return (yield from self.build_raw(symbol))
        if namespace == "tree":
            return (yield from self.build_tree(symbol, int(key)))
        if namespace == "normalizer":
            require(key in ("r_x", "r_y"), "fixed_normalizer_symbol")
            require(key in self.normalizer_origin_refs, "normalizer_actual_parent_origin")
            self.recipe_refs[symbol] = list(self.normalizer_origin_refs[key])
            return self.dag.rel("normalizer:" + key, self.recipe_refs[symbol])
        require(namespace == "target" and key == self.parents.acceptance["selected"]["head"]["sha256"],
                "one_target_HEAD_symbol")
        self.recipe_refs[symbol] = [self.ancestors.add("target", "continuation", "output/HEAD"),
                                   *(pivot["target_delta_ref"] for pivot in self.history.pivots)]
        factors = []
        for pivot in self.history.pivots:
            word = yield self.symbol("physical", pivot["pivot_id"])
            factors.append(self.dag.power(word, signrep(pivot["target_scalar"]), [pivot["target_delta_ref"]]))
        return self.dag.product(factors)

    def build_p1(self, symbol: Symbol, node: int) -> Any:
        record = self.literal.p1_record(node)
        refs = self.literal.p1_refs(node, record)
        self.recipe_refs[symbol] = refs
        kind, owner, local, base = p1_location(node)
        origin = record["origin"]
        if origin["kind"] == "actor":
            conjugator = self.dag.letter(origin["letter"], refs)
            parent = yield self.symbol("p1", base + origin["parent"])
            word = self.dag.act(conjugator, parent, refs)
        elif kind == "old":
            word = self.project(self.dag.rel("r:" + str(origin["seed"]), refs), owner, refs)
        else:
            defect = yield self.symbol("old-defect", origin["origin"])
            word = self.project(defect, owner, refs)
        factors = [word]
        for local_id, coefficient in record["reductions"]:
            parent = yield self.symbol("p1", base + local_id)
            factors.append(self.dag.power(parent, -signrep(coefficient), refs))
        return self.dag.power(self.dag.product(factors, refs), signrep(record["scale"]), refs)

    def build_defect(self, symbol: Symbol, number: int) -> Any:
        prepare = self.literal.prepare
        require(plain_int(number, 0, len(prepare["defect_origins"]) - 1), "old_defect_index")
        origin = prepare["defect_origins"][number]
        require(origin["id"] == number, "old_defect_registered_id")
        owner = origin["lower_character"]
        require(plain_int(owner, 0, 3), "old_defect_owner")
        old = prepare["old_blocks"][owner]["record"]
        refs = [self.ancestors.add("old-defect", "prepare", self.literal.prepare_name,
                                  pointer=f"/defect_origins/{number}", value=prepare)]
        if origin["kind"] == "seed":
            seed = origin["seed"]
            require(plain_int(seed, 1, 44), "old_defect_one_based_seed")
            expression = old["seed_reductions"][seed - 1]
            pointer = f"/old_blocks/{owner}/record/seed_reductions/{seed - 1}"
            word = self.project(self.dag.rel("r:" + str(seed), refs), owner, refs)
        else:
            require(origin["kind"] == "transition" and origin["letter"] in ACTORS and
                    plain_int(origin["pivot"], 0, OLD_RANKS[owner] - 1), "old_defect_actor")
            slot = ACTORS.index(origin["letter"])
            expression = old["actor_transitions"][origin["pivot"]][slot]
            pointer = f"/old_blocks/{owner}/record/actor_transitions/{origin['pivot']}/{slot}"
            actor = self.dag.letter(origin["letter"], refs)
            parent = yield self.symbol("p1", OLD_OFFSETS[owner] + origin["pivot"])
            word = self.dag.act(actor, parent, refs)
        refs.append(self.ancestors.add("old-defect", "prepare", self.literal.prepare_name, pointer=pointer, value=prepare))
        self.recipe_refs[symbol] = refs
        factors = [word]
        for local, coefficient in expression:
            require(plain_int(local, 0, OLD_RANKS[owner] - 1), "old_defect_reduction_owner")
            parent = yield self.symbol("p1", OLD_OFFSETS[owner] + local)
            factors.append(self.dag.power(parent, -signrep(coefficient), refs))
        return self.dag.product(factors, refs)

    def build_conn(self, symbol: Symbol, number: int, lower: bool) -> Any:
        offer = self.history.lower_offers[number] if lower else number
        require(plain_int(offer, 0, len(self.history.base_records) - 1), "Conn_offer_range")
        where = self.history.base_records[offer]
        record = read_positioned(self.parents, "state", "state/instructions.jsonl",
                                 where["offset"], where["length"], where["sha256"])
        conn = record["source"]
        require(conn["kind"] == ("pivot" if lower else "connection") and
                (not lower or where["lower_pivot_id"] == number), "typed_Conn_namespace")
        refs = [self.ancestors.add(symbol[0], "state", "state/instructions.jsonl",
                                  offset=where["offset"], length=where["length"])]
        self.recipe_refs[symbol] = refs
        word = yield self.symbol("p1", conn["source"]["node"])
        factors = [word]
        for lower_id, coefficient in conn["reductions"]:
            require(self.history.lower_offers[lower_id] < offer, "strict_prior_Conn_offer")
            parent = yield self.symbol("conn-lower", lower_id)
            factors.append(self.dag.power(parent, -signrep(coefficient), refs))
        value = self.dag.product(factors, refs)
        return self.dag.power(value, signrep(conn["sigma"]), refs) if lower else value


    def event_sources(self, *, seed: int | None = None, node: int | None = None,
                      actor: int | None = None) -> Iterable[tuple[Any, ...]]:
        prepare = self.literal.prepare
        if seed is not None:
            require(plain_int(seed, 0, 43), "literal_bare_seed_zero_based")
            origins = []
            for owner in range(4):
                old = prepare["old_blocks"][owner]
                matches = [index for index, item in enumerate(prepare["defect_origins"])
                           if item["kind"] == "seed" and item["lower_character"] == owner and item["seed"] == seed + 1]
                require(len(matches) == 1, "bare_seed_unique_old_origin")
                origin = matches[0]
                origins.append(origin)
                pointer = f"/old_blocks/{owner}/record/seed_reductions/{seed}"
                yield (old["record"]["seed_reductions"][seed], "prepare", self.literal.prepare_name,
                       pointer, prepare, owner, None, origin, OLD_OFFSETS[owner])
            for target in range(4):
                for owner in range(4):
                    origin = origins[owner]
                    yield (self.literal.blocks[target]["origin_reductions"][origin], f"block-{target}",
                           self.literal.block_names[target], f"/origin_reductions/{origin}", self.literal.blocks[target],
                           owner, target, origin, NEW_OFFSETS[target])
        else:
            require(node is not None and actor in ACTORS, "actor_event_origin")
            kind, owner, local, _ = p1_location(node)
            slot = ACTORS.index(actor)
            if kind == "old":
                matches = [index for index, item in enumerate(prepare["defect_origins"])
                           if item["kind"] == "transition" and item["lower_character"] == owner and
                           item["pivot"] == local and item["letter"] == actor]
                require(len(matches) == 1, "actor_unique_old_transition")
                origin = matches[0]
                yield (prepare["old_blocks"][owner]["record"]["actor_transitions"][local][slot], "prepare",
                       self.literal.prepare_name, f"/old_blocks/{owner}/record/actor_transitions/{local}/{slot}",
                       prepare, owner, None, origin, OLD_OFFSETS[owner])
                for target in range(4):
                    yield (self.literal.blocks[target]["origin_reductions"][origin], f"block-{target}",
                           self.literal.block_names[target], f"/origin_reductions/{origin}", self.literal.blocks[target],
                           owner, target, origin, NEW_OFFSETS[target])
            else:
                yield (self.literal.blocks[owner]["actor_transitions"][local][slot], f"block-{owner}",
                       self.literal.block_names[owner], f"/actor_transitions/{local}/{slot}", self.literal.blocks[owner],
                       owner, owner, None, NEW_OFFSETS[owner])

    def authenticate_events(self, events: Any, relation: Any, refs: list[int], *,
                            seed: int | None = None, node: int | None = None, actor: int | None = None) -> None:
        require(isinstance(events, list) and relation["raw_event_count"] == len(events), "raw_event_count")
        at, previous = 0, "0" * 64
        for expression, role, name, pointer, body, owner, target, origin, offset in self.event_sources(
                seed=seed, node=node, actor=actor):
            if expression:
                refs.append(self.ancestors.add("physical", role, name, pointer=pointer, value=body))
            for ordinal, pair in enumerate(expression):
                require(at < len(events) and isinstance(pair, list) and len(pair) == 2, "raw_event_expression_shape")
                local, coefficient = pair
                require(plain_int(local, 0, (OLD_RANKS[owner] if target is None else NEW_RANKS[target]) - 1) and
                        plain_int(coefficient, 1, 2), "raw_event_owner_local_coefficient")
                event = events[at]
                expected = {"event_id": at, "body_role": "prepare-old" if target is None else "new-block",
                    "task554_body_sha256": PREPARE_BODY_SHA if target is None else BLOCK_BODY_SHAS[target],
                    "source_character": owner, "target_character": target, "origin_id": origin,
                    "term_ordinal": ordinal, "local_index": local, "global_index": offset + local,
                    "coefficient": coefficient}
                require(all(event.get(key) == value for key, value in expected.items()), "ordered_raw_event_Task554_join")
                if "node" in event:
                    require(event["node"] == offset + local, "raw_actor_node_alias")
                if "seed" in event:
                    require(event["seed"] == seed, "raw_bare_seed_alias")
                previous = rolling_record(event, previous)
                at += 1
        require(at == len(events) and previous == relation["raw_event_final_head"], "all_ordered_events_EOF")

    def build_legacy_source(self, recipe: Any, refs: list[int]) -> Any:
        role, name, pointer = recipe["parent_role"], recipe["file"], recipe["pointer"]
        value = self.parents.read(role, name)
        refs.append(self.ancestors.add("physical", role, name, pointer=pointer, value=value))
        selected = json_pointer(value, pointer)
        if recipe["kind"] == "legacy-seed":
            relation = selected
            seed, character = relation["seed"], relation["character"]
            raw = value["raw_seed"]
            require(raw["seed"] == seed and raw["character"] == character and
                    raw["compact_word"] == self.literal.dictionary["relators"]["r:" + str(seed + 1)] and
                    raw["compact_word_sha256"] == sha(canonical(raw["compact_word"])), "legacy_actual_bare_seed_word")
            word = self.dag.rel("r:" + str(seed + 1), refs)
            actor_node, actor = None, None
        elif recipe["kind"] == "packet-seed":
            relation, seed, character = selected, recipe["seed"], recipe["character"]
            require(relation["seed"] == seed, "packet_zero_based_seed_relation")
            word = self.dag.rel("r:" + str(seed + 1), refs)
            actor_node, actor = None, None
        else:
            require(recipe["kind"] == "refinement", "legacy_materialization_kind")
            relation, selection = selected["relation"], selected["selection"]
            character = selection["character"]
            if selection["origin_kind"] == "seed":
                seed, actor_node, actor = selection["seed"], None, None
                require(selected["mode"] == "immutable-seed-packet" and relation["seed"] == seed, "refinement_seed_mode")
                word = self.dag.rel("r:" + str(seed + 1), refs)
            else:
                require(selection["origin_kind"] == "actor" and selected["mode"] == "complete-filtered-actor",
                        "refinement_actor_mode")
                seed, actor_node, actor = None, selection["basis_i"], selection["actor"]
                require(actor == ACTORS[selection["actor_slot"]] and relation["basis_i"] == actor_node and
                        relation["actor"] == actor and selected["literal"]["actor_conjugation"] == "t*W*t^-1",
                        "refinement_actual_literal_actor")
                conjugator = self.dag.letter(actor, refs)
                parent = yield self.symbol("p1", actor_node)
                word = self.dag.act(conjugator, parent, refs)
        check_seal(relation)
        events = relation["raw_events"]
        self.authenticate_events(events, relation, refs, seed=seed, node=actor_node, actor=actor)
        factors = [word]
        for event in events:
            parent = yield self.symbol("p1", event["global_index"])
            factors.append(self.dag.power(parent, -signrep(event["coefficient"]), refs))
        return self.project(self.dag.product(factors, refs), character, refs)

    def build_physical(self, symbol: Symbol, number: int) -> Any:
        require(plain_int(number, 0, len(self.history.pivots) - 1), "physical_insertion_ID")
        pivot = self.history.pivots[number]
        instruction = self.history.instruction(pivot)
        refs = [pivot["physical_recipe_ref"], pivot["row_ref"]]
        self.recipe_refs[symbol] = refs
        recipe = pivot["raw_recipe"]
        if recipe["kind"] == "conn":
            word = yield self.symbol("conn-raw", recipe["offer"])
            reductions = [{"pivot_id": pair[0], "scalar": pair[1]} for pair in instruction["reductions"]]
        elif recipe["kind"] == "e":
            word = yield from self.build_E_source(recipe, refs)
            reductions = instruction["physical_reductions"]
            literal = self.parents.read(recipe["parent_role"], recipe["physical_literal_file"])
            check_seal(literal)
            role = recipe["parent_role"]
            oracle_file = "output/manifest.json" if role == "e" else \
                          recipe["base"].rsplit("/e", 1)[0] + "/oracle-manifest.json"
            require(instruction["origin"] == {"kind": "v548-cycle",
                    "oracle_manifest_sha256": self.parents.pin(recipe["witness_role"], oracle_file)["sha256"],
                    "raw_word_sha256": self.parents.pin(role, recipe["raw_file"])["sha256"],
                    "witness_sha256": self.parents.pin(recipe["witness_role"], recipe["witness_file"])["sha256"]} and
                    instruction["p1_reductions_sha256"] == self.parents.pin(role, recipe["primal_file"])["sha256"] and
                    instruction["p1_roots_sha256"] == self.parents.pin(role, recipe["p1_roots_file"])["sha256"] and
                    instruction["source_correction_sha256"] == literal["source_correction_sha256"] ==
                    self.parents.pin(role, recipe["source_correction_file"])["sha256"], "E_same_source_and_literal_origin")
            require(literal["physical_factors"] ==
                    [{**item, "literal_exponent": -signrep(item["scalar"])} for item in reductions] and
                    literal["sigma"] == pivot["sigma"] and literal["literal_outer_exponent"] == signrep(pivot["sigma"]) and
                    literal["physical_normalized_sha256"] == self.ancestors.entries[pivot["row_ref"]]["record_sha256"] and
                    literal["source_lower_zero"] == "NOT_ASSERTED" and literal["physical_lower_zero"] is True and
                    literal["accepted_physical_head"] == instruction["predecessor"] and
                    instruction["physical_literal_sha256"] ==
                    self.parents.pin(recipe["parent_role"], recipe["physical_literal_file"])["sha256"],
                    "same_E_physical_literal_word")
            refs.append(self.ancestors.add("physical", recipe["parent_role"], recipe["physical_literal_file"]))
        else:
            word = yield from self.build_legacy_source(recipe, refs)
            reductions = instruction.get("physical_reductions", instruction.get("reductions"))
        require(isinstance(reductions, list), "saved_physical_reduction_order")
        factors = [word]
        previous_id = -1
        for item in reductions:
            parent_id, scalar = item["pivot_id"], item["scalar"]
            require(plain_int(parent_id, previous_id + 1, number - 1) and plain_int(scalar, 1, 2), "prior_physical_factors")
            parent_pivot = self.history.pivots[parent_id]
            for field in ("offer", "lead"):
                if field in item:
                    require(item[field] == parent_pivot[field], "physical_factor_" + field)
            if "physical_offset" in item:
                require(item["physical_offset"] == parent_id * PHYSICAL_BYTES, "physical_factor_global_offset")
            if "row_sha256" in item:
                require(item["row_sha256"] == self.ancestors.entries[parent_pivot["row_ref"]]["record_sha256"],
                        "physical_factor_saved_row")
            parent = yield self.symbol("physical", parent_id)
            factors.append(self.dag.power(parent, -signrep(scalar), refs))
            previous_id = parent_id
        return self.dag.power(self.dag.product(factors, refs), signrep(pivot["sigma"]), refs)

    def geometry(self, recipe: Any) -> Any:
        role, base = recipe["geometry_role"], recipe["geometry_base"]
        scope = self.parents.pin(role, base + "/manifest.json")["sha256"]
        if scope not in self.geometries:
            arrays = {}
            for name, count in (("parent.u32", 54432), ("parent-edge.u32", 54432), ("next-pos.u32", 108864)):
                raw = self.parents.path(role, base + "/" + name).read_bytes()
                require(len(raw) == 4 * count, "tree_u32_exact_EOF")
                arrays[name] = struct.unpack("<" + str(count) + "I", raw)
            require(arrays["parent.u32"][0] == arrays["parent-edge.u32"][0] == 0xffffffff,
                    "tree_root_u32_sentinel")
            self.geometries[scope] = {"role": role, "base": base, "arrays": arrays}
        return scope, self.geometries[scope]

    def tree_letters(self, geometry: Any, vertex: int) -> tuple[int, ...]:
        require(plain_int(vertex, 0, 54431), "tree_vertex")
        parents, edges, nexts = (geometry["arrays"][name] for name in ("parent.u32", "parent-edge.u32", "next-pos.u32"))
        letters, seen = [], set()
        while vertex:
            require(vertex not in seen, "tree_no_cycle")
            seen.add(vertex)
            parent, edge = parents[vertex], edges[vertex]
            require(parent < 54432 and edge < 108864 and edge // 2 == parent and nexts[edge] == vertex,
                    "actual_right_positive_tree_edge")
            letters.append(edge % 2 + 1)
            vertex = parent
        return tuple(reversed(letters))

    def build_tree(self, symbol: Symbol, vertex: int) -> Any:
        geometry = self.geometries[symbol[2]]
        role, base, arrays = geometry["role"], geometry["base"], geometry["arrays"]
        require(plain_int(vertex, 0, 54431), "tree_symbol_vertex")
        refs = [self.ancestors.add("tree", role, base + "/manifest.json"),
                *(self.ancestors.add("tree", role, base + "/" + name, offset=4 * vertex, length=4)
                  for name in ("parent.u32", "parent-edge.u32"))]
        self.recipe_refs[symbol] = refs
        if vertex == 0:
            require(arrays["parent.u32"][0] == arrays["parent-edge.u32"][0] == 0xffffffff, "same_tree_root_sentinel")
            return self.dag.identity(refs)
        parent, edge = arrays["parent.u32"][vertex], arrays["parent-edge.u32"][vertex]
        require(parent < 54432 and edge < 108864 and edge // 2 == parent and
                arrays["next-pos.u32"][edge] == vertex, "tree_Ref_exact_positive_step")
        refs.append(self.ancestors.add("tree", role, base + "/next-pos.u32", offset=4 * edge, length=4))
        word = yield self.symbol("tree", parent, symbol[2])
        letter = self.dag.letter(edge % 2 + 1, refs)
        return self.dag.product([word, letter], refs)

    def build_raw(self, symbol: Symbol) -> Any:
        key = symbol[1]
        prefix, node_id = key.rsplit("/", 1)
        data = self.raw_data[prefix]
        record = data["by_id"][node_id]
        ordinal = data["positions"][node_id]
        refs = [self.ancestors.add("raw-e", data["role"], data["name"], pointer=f"/nodes/{ordinal}", value=data["record"])]
        self.recipe_refs[symbol] = refs
        op = record["op"]
        dependency = lambda name: self.symbol("raw-e", prefix + "/" + name, symbol[2])
        if op == "Identity":
            return self.dag.identity(refs)
        if op == "Letter":
            return self.dag.letter(record["letter"], refs)
        if op == "Ref":
            if record["namespace"] == "oracle-tree":
                return (yield self.symbol("tree", record["key"], data["geometry_scope"]))
            require(record["namespace"] == "normalizer-v459" and record["key"] in ("r_x", "r_y"), "raw_fixed_normalizer")
            normalizer = self.symbol("normalizer", record["key"])
            refs.append(self.ancestors.add("raw-e", data["role"], data["name"],
                                           pointer="/normalizers", value=data["record"]))
            origin_ref = self.ancestors.add("normalizer", data["role"], data["name"],
                                             pointer="/normalizers", value=data["record"])
            self.normalizer_origin_refs.setdefault(record["key"], [origin_ref])
            return (yield normalizer)
        if op == "OrderedProduct":
            factors = []
            for child in record["factors"]:
                factors.append((yield dependency(child)))
            return self.dag.product(factors, refs)
        require(op in ("Inverse", "IntegerPower"), "raw_grammar_operation")
        word = yield dependency(record["node"])
        return self.dag.inverse(word, refs) if op == "Inverse" else self.dag.power(word, record["exponent"], refs)


    def load_raw(self, recipe: Any) -> Any:
        key, role, name = recipe["key"], recipe["parent_role"], recipe["raw_file"]
        if key in self.raw_data:
            return self.raw_data[key]
        record = self.parents.read(role, name)
        check_seal(record)
        witness = self.parents.read(recipe["witness_role"], recipe["witness_file"])
        check_seal(witness)
        geometry_scope, geometry = self.geometry(recipe)
        require(record["grammar"] == "ordered-slp-v1" and record["root"] == "raw-root" and
                record["geometry_manifest_sha256"] == geometry_scope and record["cycles"] == witness["cycles"] and
                record["witness_sha256"] == self.parents.pin(recipe["witness_role"], recipe["witness_file"])["sha256"],
                "raw_same_snapshot_witness_geometry")
        normalizers = record["normalizers"]
        require(normalizers["dictionary"] == {"file": "scratchpad/a0_v2_words.json",
                    "bytes": DATA_PINS["scratchpad/a0_v2_words.json"][0],
                    "sha256": DATA_PINS["scratchpad/a0_v2_words.json"][1]} and
                normalizers["raw_relators_sha256"] == NORMALIZER_ROSTER_SHA and
                normalizers["words"] == [{"name": n, "length": count, "word_sha256": digest}
                                         for n, (count, digest) in NORMALIZER_WORDS.items()],
                "raw_normalizer_same_dictionary")
        expected = [{"id": "identity", "op": "Identity"}, {"id": "x", "op": "Letter", "letter": 1},
                    {"id": "y", "op": "Letter", "letter": 2}]
        factors = []
        for index, cycle in enumerate(witness["cycles"]):
            require(set(cycle) == {"edge", "coefficient"} and plain_int(cycle["edge"], 0, 108863), "selected_cycle_edge")
            edge, suffix = cycle["edge"], str(index)
            tail, slot = divmod(edge, 2)
            head = geometry["arrays"]["next-pos.u32"][edge]
            expected.extend([
                {"id": "tail-" + suffix, "op": "Ref", "namespace": "oracle-tree", "key": tail},
                {"id": "head-" + suffix, "op": "Ref", "namespace": "oracle-tree", "key": head},
                {"id": "head-inverse-" + suffix, "op": "Inverse", "node": "head-" + suffix},
                {"id": "cycle-" + suffix, "op": "OrderedProduct",
                 "factors": ["tail-" + suffix, ("x", "y")[slot], "head-inverse-" + suffix]},
                {"id": "cycle-power-" + suffix, "op": "IntegerPower", "node": "cycle-" + suffix,
                 "exponent": signrep(cycle["coefficient"])}])
            factors.append("cycle-power-" + suffix)
        expected.extend([
            {"id": "w", "op": "OrderedProduct", "factors": factors},
            {"id": "r-x", "op": "Ref", "namespace": "normalizer-v459", "key": "r_x"},
            {"id": "r-y", "op": "Ref", "namespace": "normalizer-v459", "key": "r_y"},
            {"id": "r-x-cube", "op": "IntegerPower", "node": "r-x", "exponent": 3},
            {"id": "r-y-cube", "op": "IntegerPower", "node": "r-y", "exponent": 3},
            {"id": "r-x-inverse", "op": "Inverse", "node": "r-x"},
            {"id": "r-y-inverse", "op": "Inverse", "node": "r-y"},
            {"id": "commutator", "op": "OrderedProduct",
             "factors": ["r-x-inverse", "r-y-inverse", "r-x", "r-y"]}])
        require(record["nodes"][:len(expected)] == expected, "raw_exact_ordered_constructor")
        values, leaves = {}, {}
        def evaluate(node: Any) -> None:
            node_id, op = node["id"], node["op"]
            require(node_id not in values, "raw_unique_prior_ID")
            if op == "Identity":
                scalar, length = (0, 0, 0), 0
            elif op in ("Letter", "Ref"):
                if op == "Letter":
                    word = (node["letter"],)
                elif node["namespace"] == "oracle-tree":
                    word = self.tree_letters(geometry, node["key"])
                else:
                    word = tuple(self.literal.dictionary["relators"]["normalizer:" + node["key"]])
                a, b, omega = 0, 0, 0
                for letter in word:
                    if abs(letter) == 1:
                        increment = 1 if letter == 1 else -1
                        omega = (omega + increment * b) % 3
                        a += increment
                    else:
                        b += 1 if letter == 2 else -1
                scalar, length = (a, b, omega), len(word)
                leaves[node_id] = word
            elif op == "OrderedProduct":
                a, b, omega, length = 0, 0, 0, 0
                for child in node["factors"]:
                    require(child in values, "raw_prior_product")
                    (c, d, psi), size = values[child]
                    a, b, omega, length = a + c, b + d, (omega + psi + b * c) % 3, length + size
                scalar = a, b, omega
            else:
                require(op in ("Inverse", "IntegerPower") and node["node"] in values, "raw_prior_power")
                power = -1 if op == "Inverse" else node["exponent"]
                require(type(power) is int, "raw_ordinary_integer_power")
                (a, b, omega), size = values[node["node"]]
                scalar = power * a, power * b, (power * omega + power * (power - 1) // 2 * b * a) % 3
                length = abs(power) * size
            values[node_id] = scalar, length
        for node in expected:
            evaluate(node)
        a, b, omega = values["w"][0]
        if witness["kind"] == "chord":
            require(len(witness["cycles"]) == 6 and witness["eta"] == [0, 0] and a % 6 == b % 6 == 0,
                    "six_cycles_ordinary_integer_repair")
            tail = [
                {"id": "repair-x", "op": "IntegerPower", "node": "r-x-cube", "exponent": -a // 6},
                {"id": "repair-y", "op": "IntegerPower", "node": "r-y-cube", "exponent": -b // 6},
                {"id": "repair-central", "op": "IntegerPower", "node": "commutator", "exponent": signrep(omega)},
                {"id": "raw-root", "op": "OrderedProduct", "factors": ["w", "repair-x", "repair-y", "repair-central"]}]
        else:
            require(witness["kind"] == "auxiliary" and witness["cycles"] == [] and
                    plain_int(witness["coordinate"], 0, 1) and
                    witness["eta"] == ([1, 0] if witness["coordinate"] == 0 else [0, 1]), "auxiliary_eta_ninth_power")
            tail = [{"id": "raw-root", "op": "IntegerPower",
                     "node": ("r-x", "r-y")[witness["coordinate"]], "exponent": 9}]
        require(record["nodes"] == expected + tail, "raw_signed_repair_and_complete_constructor")
        for node in tail:
            evaluate(node)
        require(len(record["node_values"]) == len(values), "raw_all_node_value_receipts")
        for node, saved in zip(record["nodes"], record["node_values"]):
            scalar, length = values[node["id"]]
            require(saved["id"] == node["id"] and saved["exponent"] == list(scalar[:2]) and
                    saved["omega"] == scalar[2] and saved["length"] == length, "raw_same_word_integer_receipt")
        root_scalar, root_length = values["raw-root"]
        require(root_scalar[0] % 18 == root_scalar[1] % 18 == 0 and root_scalar[2] == 0 and
                record["eta"] == witness["eta"] ==
                [root_scalar[0] // 18 % 3, root_scalar[1] // 18 % 3], "raw_same_word_normalized_eta")
        require(record["word_bound"]["actual_slp_length"] == root_length <= record["word_bound"]["normalized"] and
                record["word_bound"]["unrepaired"] == values["w"][1], "raw_literal_word_bound")
        by_id = {node["id"]: node for node in record["nodes"]}
        digest, letters = hashlib.sha256(), 0
        stack = [("raw-root", False)]
        while stack:
            node_id, inverse = stack.pop()
            node = by_id[node_id]
            op = node["op"]
            if op in ("Letter", "Ref"):
                word = ordinary_inverse(leaves[node_id]) if inverse else leaves[node_id]
                for letter in word:
                    digest.update(bytes((letter & 255,)))
                    letters += 1
            elif op == "OrderedProduct":
                children = list(reversed(node["factors"])) if inverse else node["factors"]
                stack.extend((child, inverse) for child in reversed(children))
            elif op == "Inverse":
                stack.append((node["node"], not inverse))
            elif op == "IntegerPower":
                power = -node["exponent"] if inverse else node["exponent"]
                stack.extend((node["node"], power < 0) for _ in range(abs(power)))
            else:
                require(op == "Identity", "raw_stream_operation")
            require(letters <= root_length, "raw_exact_stream_length_bound")
            check_resources("raw-literal-stream")
        stream = {"encoding": "signed-byte:1=01,-1=ff,2=02,-2=fe", "letters": letters, "bytes": letters,
                  "sha256": digest.hexdigest(), "full_eof": True}
        require(letters == root_length and record["word_stream"] == stream, "same_raw_word_stream_EOF")
        value = {"role": role, "name": name, "record": record, "witness": witness, "values": values,
                 "geometry_scope": geometry_scope, "by_id": by_id,
                 "positions": {node["id"]: at for at, node in enumerate(record["nodes"])}}
        self.raw_data[key] = value
        self.raw_streams.append({"key": key, "parent_role": role, "raw_word_file": name,
            "raw_word_sha256": self.parents.pin(role, name)["sha256"], "witness_sha256": record["witness_sha256"],
            "geometry_manifest_sha256": geometry_scope, "word_stream": stream, "eta": record["eta"],
            "literal_root": "raw-root"})
        return value

    def build_E_source(self, recipe: Any, refs: list[int]) -> Any:
        data = self.load_raw(recipe)
        role, key = recipe["parent_role"], recipe["key"]
        raw_ref = self.ancestors.add("raw-e", role, recipe["raw_file"])
        refs.append(raw_ref)
        word = yield self.symbol("raw-e", key + "/raw-root", self.parents.pin(role, recipe["raw_file"])["sha256"])
        reductions = self.parents.read(role, recipe["primal_file"])
        corrected = self.parents.read(role, recipe["source_correction_file"])
        roots = self.parents.read(role, recipe["p1_roots_file"])
        for value in (reductions, corrected, roots):
            check_seal(value)
        refs.extend([self.ancestors.add("physical", role, recipe[name])
                     for name in ("primal_file", "source_correction_file", "p1_roots_file")])
        require(reductions["rows"] == P1_ROWS and reductions["eof"] is True and
                reductions["order"] == "old-global-ascending-embedded-original-lead;new-owner-major-ascending-original-lead" and
                corrected["operation"] == "ordered-product" and corrected["p1_factor_order"] == "event-ascending" and
                corrected["raw_word_sha256"] == self.parents.pin(role, recipe["raw_file"])["sha256"] and
                corrected["p1_roots_sha256"] == self.parents.pin(role, recipe["p1_roots_file"])["sha256"] and
                corrected["coefficients_sha256"] == reductions["coefficients_sha256"] and
                corrected["top_characters"] == [0, 1, 2, 3] and corrected["source_lower_equality"] is True and
                corrected["source_lower_zero"]["trits"] == LOWER_TRITS and reductions["lower_zero"]["trits"] == LOWER_TRITS,
                "same_E_source_P1_receipts")
        require(roots["p1_manifest_sha256"] == P1_MANIFEST_SHA and roots["canonical_index_sha256"] ==
                self.parents.pin("continuation", "output/fixed/canonical-index.json")["sha256"] and
                roots["all_references_authenticated"] is True, "E_actual_P1_roots")
        root_map = {entry["node"]: entry for entry in roots["roots"]}
        require(len(root_map) == len(roots["roots"]) and list(root_map) == sorted(root_map), "E_sorted_P1_root_receipts")
        require(len(corrected["p1_factors"]) == len(reductions["events"]), "E_P1_factor_cardinality")
        alpha = bytearray(P1_ROWS)
        factors, previous_order = [word], None
        for at, (event, factor) in enumerate(zip(reductions["events"], corrected["p1_factors"])):
            node, coefficient = event["node"], event["coefficient"]
            kind, owner, local, _ = p1_location(node)
            require(plain_int(coefficient, 1, 2) and alpha[node] == 0 and event["event"] == at and
                    event["kind"] == kind and event["owner"] == owner and event["local"] == local and
                    event["literal_exponent"] == -signrep(coefficient), "E_primal_same_ordered_node")
            body, _, _, _, _ = self.literal.body_record(node)
            original = body["lead"]
            embedded = (owner * 6048 + original if original < 6048 else 96768 + original - 6048) if kind == "old" else \
                       24192 + owner * 18144 + original
            order = (0, embedded) if kind == "old" else (1, owner, original)
            require(event["original_lead"] == original and event["embedded_lead"] == embedded and
                    (previous_order is None or previous_order < order), "E_primal_original_lead_order")
            previous_order = order
            if kind == "old":
                descriptors = (self.literal.prepare["old_blocks"][owner]["lower_basis_blob"],
                               self.literal.prepare["old_blocks"][owner]["lifted_grade_blob"])
                row_role, widths = "prepare", (1514, 18144)
            else:
                descriptors = (self.literal.blocks[owner]["basis_blob"],)
                row_role, widths = f"block-{owner}", (4536,)
            factor_refs = list(refs)
            for index, (descriptor, width) in enumerate(zip(descriptors, widths)):
                prefix = "row" if index == 0 else "companion"
                require(event[prefix + "_offset"] == local * width, "E_primal_blob_local_offset")
                row_ref = self.ancestors.add("p1", row_role, descriptor["file"], offset=local * width, length=width)
                require(self.ancestors.entries[row_ref]["record_sha256"] == event[prefix + "_sha256"],
                        "E_primal_actual_lower_row")
                factor_refs.append(row_ref)
            if kind == "new":
                require(event["companion_offset"] is None and event["companion_sha256"] is None, "new_primal_no_companion")
            reference = self.literal.index["references"][node]
            require(node in root_map and all(root_map[node][field] == value for field, value in reference.items()),
                    "E_selected_P1_full_reference")
            require(factor == {"event": at, "node": node, "coefficient": coefficient,
                               "literal_exponent": -signrep(coefficient), "p1_sha256": reference["p1_sha256"]},
                    "E_corrected_literal_factor_exact")
            alpha[node] = coefficient
            parent = yield self.symbol("p1", node)
            factors.append(self.dag.power(parent, -signrep(coefficient), factor_refs))
        require(set(root_map) == {node for node, coefficient in enumerate(alpha) if coefficient} and
                sha(bytes(alpha)) == reductions["coefficients_sha256"], "E_all_alpha_and_roots")
        alpha_name = recipe["base"] + ("/p1-coefficients.u8" if role == "e" else "/primal/p1-coefficients.u8")
        require(self.parents.path(role, alpha_name).read_bytes() == bytes(alpha), "E_actual_full_alpha_bytes")
        value = self.dag.product(factors, refs)
        residues = list(self.dag.pairs[value])
        require(residues == corrected["exponent_residue_mod54"] and all(x in (0, 18, 36) for x in residues) and
                corrected["normalized_pair"] == [x // 18 for x in residues] == [0, 0], "E_same_V_normalized_pair")
        by_character = recipe["base"] + ("/physical-by-character.bin" if role == "e" else "/B/physical-by-character.bin")
        require(self.parents.pin(role, by_character)["bytes"] == 4 * PHYSICAL_BYTES, "E_four_B_payload_shape")
        if recipe["B_file"] is not None:
            b = self.parents.read(role, recipe["B_file"])
            check_four_B(b, self.parents.pin(role, by_character)["bytes"],
                         self.parents.pin(role, by_character)["sha256"],
                         self.parents.pin(role, recipe["source_correction_file"])["sha256"],
                         data["record"]["witness_sha256"])
            refs.append(self.ancestors.add("physical", role, recipe["B_file"]))
        else:
            checked = self.parents.read("e", "checker-result.json")
            require(checked["status"] == "PASS" and checked["all_four_B_summed"] is True and
                    checked["all_arrays_and_json_compared"] is True, "external_E_four_B_accepted_premise")
        return value


SUCCESS_FILES = tuple(sorted(("source.json", "owner.json", "parent-roster.json", "fresh-rho2.json", "context.json",
    "literal-dictionary.json", "target-history.json", "ancestor-index.json", "ordered-word.jsonl",
    "word-manifest.json", "normalized-pair.json", "manifest.json", "result.json")))
SCOPE = {"source_lower_trits": 96776, "physical_lower_trits": 32260, "physical_top_trits": 48384,
    "p1_rows": 8059, "character_order": [0, 1, 2, 3], "unique_occurrences": 10,
    "occurrence_order": [0, 1, 2, 3, 0, 4, 5, 6, 7, 8, 9],
    "current_grade": "v478-(2.7)-PB4-dropped", "word_group": "F2",
    "actor_convention": "P*W*P^-1", "normalized_modulus": 54,
    "grade2_member": "NOT_DECIDED", "grade2_nonmember": "NOT_DECIDED", "full_A0": False}


def write_output(root: Path, name: str, raw: bytes) -> dict[str, Any]:
    require(name in SUCCESS_FILES and "/" not in name and not (root / name).exists(), "fresh_output_file")
    with (root / name).open("xb") as stream:
        require(stream.write(raw) == len(raw), "output_complete_write")
        stream.flush()
        os.fsync(stream.fileno())
    return {"file": name, "bytes": len(raw), "sha256": sha(raw)}


def output_metadata(parents: Parents, history: TargetHistory, dictionary: Any) -> dict[str, Any]:
    selected = parents.acceptance["selected"]
    roster = seal("parent-roster", {"acceptance_sha256": parents.acceptance_sha256,
        "parents": parents.acceptance["parents"], "all_files_and_directories_authenticated": True, **ASSURANCE})
    roster_sha = sha(canonical(roster))
    source = seal("source", {"acceptance_sha256": parents.acceptance_sha256,
        "consumer_sources": parents.acceptance["consumer_sources"],
        "raw_sources": [{"file": name, "bytes": size, "sha256": digest} for name, (size, digest) in DATA_PINS.items()],
        "runtime": parents.acceptance["runtime"], "accepted_continuation_source_sha256": selected["source"]["sha256"],
        "arithmetic_imports": [], "old_numerical_replay": False, **ASSURANCE})
    source_sha = sha(canonical(source))
    owner = seal("owner", {"acceptance_sha256": parents.acceptance_sha256,
        "accepted_owner_sha256": selected["owner"]["sha256"], "accepted_source_sha256": selected["source"]["sha256"],
        "accepted_head_sha256": selected["head"]["sha256"], "parent_roster_sha256": roster_sha,
        "source_sha256": source_sha, "scope": SCOPE, **ASSURANCE})
    fresh_manifest = parents.read("rho2", "task640-payload/manifest.json", strict=False)
    fresh_verdict = parents.read("rho2", "task640-verdict.json", strict=False)
    fresh = seal("fresh-rho2", {"artifact": FIXED_ARTIFACTS["rho2"],
        "files": [{"file": name, "bytes": size, "sha256": digest} for name, (size, digest) in RHO2_FILES.items()],
        "manifest_sha256": RHO2_FILES["task640-payload/manifest.json"][1],
        "packed_sha256": RHO2_FILES["task640-payload/rho2.bin"][1],
        "manifest": fresh_manifest, "verdict": fresh_verdict,
        "direct_payload_parent": True, "derived_target_identity_used_as_direct_bytes": False, **ASSURANCE})
    context = seal("context", {"accepted_owner_sha256": selected["owner"]["sha256"],
        "accepted_source_sha256": selected["source"]["sha256"],
        "fresh_rho2_manifest_sha256": RHO2_FILES["task640-payload/manifest.json"][1],
        "task712_manifest_sha256": parents.pin("task712", "r07-grade2-maps-v4/manifest.json")["sha256"],
        "p1_manifest_sha256": P1_MANIFEST_SHA, "prepare_body_sha256": PREPARE_BODY_SHA,
        "block_body_sha256": list(BLOCK_BODY_SHAS),
        "canonical_index_sha256": parents.pin("continuation", "output/fixed/canonical-index.json")["sha256"],
        "scope": SCOPE, "aggregation": "printed-v478-(2.7)-PB4-dropped",
        "same_word_all_occurrences_required": True, **ASSURANCE})
    return {"source.json": source, "owner.json": owner, "parent-roster.json": roster,
            "fresh-rho2.json": fresh, "context.json": context, "literal-dictionary.json": dictionary}


def compile_target_word(history: TargetHistory, literal: LiteralParents, output: Path,
                        dictionary_sha: str) -> dict[str, Any]:
    with (output / "ordered-word.jsonl").open("xb") as stream:
        dag = WordDAG(stream, dictionary_sha,
            {key: tuple(word) for key, word in literal.dictionary["relators"].items()},
            lambda: len(history.ancestors.entries))
        compiler = TargetWordCompiler(history, literal, dag)
        head_sha = history.parents.acceptance["selected"]["head"]["sha256"]
        root = compiler.resolve(compiler.symbol("target", head_sha, head_sha))
        require(root == len(dag.hashes) - 1, "single_final_target_root")
        file_receipt = dag.flush()
        result = {"nodes_file": file_receipt, "root_id": root, "root_sha256": dag.hashes[root],
            "root_residues": list(dag.pairs[root]), "raw_streams": compiler.raw_streams,
            "literal_dependency_closure": {"prior_only": True, "symbol_order": compiler.symbol_order,
                                           "all_used_edges_preserved": True},
            "input_receipts": len(history.ancestors.entries)}
    return result


def read_normalized_pair(output: Path, word_manifest: Any, dictionary: Any, ancestor_count: int) -> dict[str, Any]:
    require(word_manifest["grammar"] == GRAMMAR and word_manifest["nodes_file"]["file"] == "ordered-word.jsonl",
            "C_same_word_bundle")
    hashes, pairs, total, count = [], [], 0, 0
    digest = hashlib.sha256()
    with (output / "ordered-word.jsonl").open("rb") as stream:
        for node_id, raw in enumerate(stream):
            require(raw.endswith(b"\n"), "C_JSONL_final_LF")
            node = json.loads(raw.decode("ascii"))
            require(isinstance(node, dict) and set(node) == {"id", "type", "op", "args", "receipt_refs", "node_sha256"} and
                    canonical(node) == raw and type(node["id"]) is int and node["id"] == node_id and
                    node["type"] == "F2-word", "C_continuous_typed_word_nodes")
            require(node["node_sha256"] == sha(canonical({key: value for key, value in node.items()
                                                         if key != "node_sha256"})), "C_node_seal")
            require(isinstance(node["receipt_refs"], list) and
                    all(plain_int(item, 0, ancestor_count - 1) for item in node["receipt_refs"]), "C_all_input_receipt_refs")
            for child in child_links(node["op"], node["args"]):
                require(isinstance(child, dict) and set(child) == {"node", "sha256"} and
                        plain_int(child["node"], 0, node_id - 1) and child["sha256"] == hashes[child["node"]],
                        "C_prior_only_same_child_hash")
            if node["op"] == "Rel":
                args = node["args"]
                require(args["dictionary_sha256"] == word_manifest["literal_dictionary_sha256"] and
                        args["relator_id"] in dictionary["relators"] and
                        args["letters"] == dictionary["relators"][args["relator_id"]], "C_same_literal_dictionary")
            pairs.append(node_residue(node["op"], node["args"], pairs))
            hashes.append(node["node_sha256"])
            total += len(raw)
            count += 1
            digest.update(raw)
            if count % 512 == 0:
                check_resources("same-root-mod54")
    require(word_manifest["nodes_file"] == {"file": "ordered-word.jsonl", "bytes": total,
                "sha256": digest.hexdigest(), "nodes": count} and count > 0 and
            word_manifest["root_id"] == count - 1 and word_manifest["root_sha256"] == hashes[-1],
            "C_exact_word_manifest_root_and_EOF")
    residues = list(pairs[-1])
    require(all(plain_int(value, 0, 53) for value in residues), "integer_residue54_range")
    divisible = [value in (0, 18, 36) for value in residues]
    normalized = [value // 18 for value in residues] if all(divisible) else None
    return seal("normalized-pair", {"word_manifest_sha256": sha(canonical(word_manifest)),
        "same_root_id": word_manifest["root_id"], "same_root_sha256": word_manifest["root_sha256"],
        "modulus": 54, "residue_type": "integer-residue-0-to-53", "exponent_residues": residues,
        "divisible18": divisible, "normalized_pair": normalized, "eof": True})


def make_word_manifest(metadata: Any, history: TargetHistory, target: Any, ancestors: Any, bundle: Any) -> Any:
    return seal("word-manifest", {"grammar": GRAMMAR, "owner_sha256": sha(canonical(metadata["owner.json"])),
        "source_sha256": sha(canonical(metadata["source.json"])),
        "context_manifest_sha256": sha(canonical(metadata["context.json"])),
        "fresh_rho2_manifest_sha256": RHO2_FILES["task640-payload/manifest.json"][1],
        "parent_roster_sha256": sha(canonical(metadata["parent-roster.json"])),
        "accepted_head_sha256": history.parents.acceptance["selected"]["head"]["sha256"],
        "target_history_sha256": sha(canonical(target)), "ancestor_index_sha256": sha(canonical(ancestors)),
        "literal_dictionary_sha256": sha(canonical(metadata["literal-dictionary.json"])),
        "nodes_file": bundle["nodes_file"], "root_id": bundle["root_id"], "root_sha256": bundle["root_sha256"],
        "character_order": [0, 1, 2, 3], "actor_convention": "P*W*P^-1",
        "central_representative": "sr(0,1,2)=(0,1,-1)", "coefficient_rule": "saved-F3-to-signed-integer-once",
        "raw_streams": bundle["raw_streams"], "literal_dependency_closure": bundle["literal_dependency_closure"],
        "input_receipts": bundle["input_receipts"], "eof": True, **ASSURANCE})


def run_actual(args: argparse.Namespace) -> Any:
    global OUTPUT_CREATED
    output = Path(args.output).resolve()
    require(not output.exists(), "new_separate_readout_output")
    parents = admit_parents(args)
    ancestors = Ancestors(parents)
    history = read_target_history(parents, ancestors)
    dictionary = literal_dictionary()
    literal = load_literal_parents(parents, ancestors, history, dictionary)
    metadata = output_metadata(parents, history, dictionary)
    output.mkdir(parents=True, exist_ok=False)
    OUTPUT_CREATED = output
    output_files = []
    for name in ("source.json", "owner.json", "parent-roster.json", "fresh-rho2.json", "context.json", "literal-dictionary.json"):
        output_files.append(write_output(output, name, canonical(metadata[name])))
    bundle = compile_target_word(history, literal, output, sha(canonical(dictionary)))
    del literal
    target = history.output()
    ancestor_record = seal("ancestor-index", {"parent_roster_sha256": sha(canonical(metadata["parent-roster.json"])),
        "owner_sha256": sha(canonical(metadata["owner.json"])), "source_sha256": sha(canonical(metadata["source.json"])),
        "entries": ancestors.entries, "eof": True})
    word = make_word_manifest(metadata, history, target, ancestor_record, bundle)
    normalized = read_normalized_pair(output, word, dictionary, len(ancestors.entries))
    require(normalized["exponent_residues"] == bundle["root_residues"], "same_B_C_root_mod54")
    for name, value in (("target-history.json", target), ("ancestor-index.json", ancestor_record),
                        ("word-manifest.json", word), ("normalized-pair.json", normalized)):
        output_files.append(write_output(output, name, canonical(value)))
    output_files.append({key: bundle["nodes_file"][key] for key in ("file", "bytes", "sha256")})
    # The successful result is published only after every original input byte remains intact.
    parents.again()
    require(file_pin(Path(args.acceptance).resolve()) ==
            {"bytes": len(canonical(parents.acceptance)), "sha256": parents.acceptance_sha256},
            "acceptance_all_bytes_unchanged")
    for key, entry in parents.acceptance["consumer_sources"].items():
        require(file_pin(safe_file(SOURCE_ROOT, entry["file"])) ==
                {name: entry[name] for name in ("bytes", "sha256")}, "consumer_source_unchanged:" + key)
    for name, (size, digest) in DATA_PINS.items():
        require(file_pin(safe_file(SOURCE_ROOT, name)) == {"bytes": size, "sha256": digest}, "raw_source_unchanged")
    manifest = seal("manifest", {"owner_sha256": word["owner_sha256"], "source_sha256": word["source_sha256"],
        "accepted_head_sha256": word["accepted_head_sha256"], "word_manifest_sha256": sha(canonical(word)),
        "target_history_sha256": sha(canonical(target)), "normalized_pair_sha256": sha(canonical(normalized)),
        "root_id": word["root_id"], "root_sha256": word["root_sha256"], "file_roster": list(SUCCESS_FILES),
        "files": sorted(output_files, key=lambda entry: entry["file"]), "all_inputs_unchanged": True, **ASSURANCE})
    require(len(manifest["files"]) == 11, "eleven_payloads_two_outer_receipts")
    write_output(output, "manifest.json", canonical(manifest))
    zero, normalized_zero = target["residual"]["zero"], normalized["normalized_pair"] == [0, 0]
    result = seal("result", {"status": "PASS", "terminal": "POSITIVE_WORD_CANDIDATE" if zero else "NOT_APPLICABLE",
        "positive_applicability": target["positive_applicability"],
        "positive_readout": "PENDING_SAME_WORD_D_AND_SIDE_CONDITIONS" if zero and normalized_zero else "NOT_APPLICABLE",
        "manifest_sha256": sha(canonical(manifest)), "owner_sha256": word["owner_sha256"],
        "source_sha256": word["source_sha256"], "parent_roster_sha256": word["parent_roster_sha256"],
        "context_manifest_sha256": word["context_manifest_sha256"],
        "fresh_rho2_manifest_sha256": word["fresh_rho2_manifest_sha256"],
        "word_manifest_sha256": sha(canonical(word)), "target_history_sha256": sha(canonical(target)),
        "ancestor_index_sha256": sha(canonical(ancestor_record)), "normalized_pair_sha256": sha(canonical(normalized)),
        "accepted_head_sha256": word["accepted_head_sha256"],
        "accepted_checker_sha256": parents.acceptance["selected"]["checker"]["sha256"],
        "completed_steps": target["completed_steps"], "rank": target["rank"], "generation": target["generation"],
        "state_head": target["state_head"], "target_remainder_sha256": target["residual"]["sha256"],
        "residual_zero": zero, "normalized_pair": normalized["normalized_pair"], "normalized_zero": normalized_zero,
        "root_id": word["root_id"], "root_sha256": word["root_sha256"], "nodes": bundle["nodes_file"]["nodes"],
        "source_lower_zero": "NOT_ASSERTED_FOR_WHOLE_TARGET_WORD", "old_numerical_replays": 0,
        "same_word_B_C": True, "same_word_D": False, "eleven_slot_replay": False,
        "side_conditions": "PENDING", "grade2_member": "NOT_DECIDED", "grade2_nonmember": "NOT_DECIDED", "full_A0": False,
        "parent_inputs_unchanged": True, "eof": True,
        "resource_limits": {"max_seconds": args.max_seconds, "max_memory_mib": args.max_memory_mib},
        "elapsed_seconds": round(time.monotonic() - STARTED, 6), **ASSURANCE})
    write_output(output, "result.json", canonical(result))
    require(sorted(path.name for path in output.iterdir()) == list(SUCCESS_FILES), "exact_success_output_roster")
    return result


def selftest_rejection(name: str, action: Callable[[], Any], rejected: list[str]) -> None:
    try:
        action()
    except ValueError:
        rejected.append(name)
    else:
        raise AssertionError("selftest_expected_rejection:" + name)


def fixture_parents(root: Path, payloads: dict[str, dict[str, bytes]],
                    primary: dict[str, str]) -> Parents:
    """Metadata fixtures bypass admission; they never represent accepted arithmetic."""
    roots, roster, files = {}, {}, {}
    for role, entries in payloads.items():
        folder = root / role
        folder.mkdir(parents=True, exist_ok=False)
        for name, raw in entries.items():
            path = folder / relative_name(name)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(raw)
        roots[role] = folder
        observed, directories = inventory(folder)
        files[role] = {item["file"]: item for item in observed}
        roster[role] = {"role": role, "manifest": files[role][primary[role]], "files": observed,
                        "directories": directories}
    selected = {key: {"sha256": sha(key.encode("ascii"))} for key in ("head", "result", "checker")}
    return Parents(roots, {"selected": selected}, sha(b"metadata-fixture"), roster, files)


def replace_fixture(parents: Parents, role: str, name: str, raw: bytes) -> None:
    path = parents.path(role, name)
    path.write_bytes(raw)
    parents.files[role][name] = {"file": name, **file_pin(path)}


def selftest_word(root: Path) -> dict[str, Any]:
    root.mkdir()
    rejected: list[str] = []
    dictionary = {"relators": {"r:1": [1, 2]}}
    dictionary_sha = sha(canonical(dictionary))
    with (root / "ordered-word.jsonl").open("xb") as stream:
        dag = WordDAG(stream, dictionary_sha, {"r:1": (1, 2)}, lambda: 1)
        identity, x, y = dag.identity(), dag.letter(1), dag.letter(2)
        rel = dag.rel("r:1", [0])
        xy, yx = dag.product([x, y]), dag.product([y, x])
        require(dag.pairs[xy] == dag.pairs[yx] and dag.hashes[xy] != dag.hashes[yx],
                "selftest_order_is_not_exponent_equality")
        act = dag.act(x, rel, [0])
        internal = dag.power(act, signrep(2), [0])
        corrected = dag.product([internal, dag.power(rel, -signrep(2), [0])], [0])
        physical = dag.power(corrected, signrep(2), [0])
        first = dag.ref("p1", "0", dictionary_sha, rel, [0])
        second = dag.ref("physical", "0", dictionary_sha, physical, [0])
        require(first != second and dag.hashes[first] != dag.hashes[second], "selftest_typed_same_integer_ID")
        inverse = dag.inverse(x)
        target = dag.product([dag.power(x, 18), dag.power(y, -18), second,
                              dag.power(first, 0), x, inverse, identity])
        root_id = dag.ref("target", "fixture", dictionary_sha, target, [0])
        receipt = dag.flush()
        root_hash = dag.hashes[root_id]
    word = seal("word-manifest", {"grammar": GRAMMAR, "nodes_file": receipt, "root_id": root_id,
        "root_sha256": root_hash, "literal_dictionary_sha256": dictionary_sha})
    normalized = read_normalized_pair(root, word, dictionary, 1)
    require(normalized["exponent_residues"] == [18, 36] and normalized["normalized_pair"] == [1, 2] and
            normalized["same_root_sha256"] == root_hash, "selftest_negative18_mod54_same_root")
    original = (root / "ordered-word.jsonl").read_bytes()
    nodes = [json.loads(line) for line in original.splitlines()]
    def changed_node(index: int, action: Callable[[dict[str, Any]], None]) -> None:
        changed = json.loads(original.decode("ascii").splitlines()[index])
        action(changed)
        changed["node_sha256"] = sha(canonical({k: v for k, v in changed.items() if k != "node_sha256"}))
        lines = original.splitlines(keepends=True)
        lines[index] = canonical(changed)
        (root / "ordered-word.jsonl").write_bytes(b"".join(lines))
        read_normalized_pair(root, word, dictionary, 1)
    selftest_rejection("self-child-even-with-seal", lambda: changed_node(root_id, lambda n:
        n["args"].update(word={"node": root_id, "sha256": root_hash})), rejected)
    power_id = next(n["id"] for n in nodes if n["op"] == "IntegerPower")
    selftest_rejection("bool-is-not-integer-power", lambda: changed_node(power_id, lambda n:
        n["args"].update(exponent=True)), rejected)
    selftest_rejection("receipt-outside-closure", lambda: changed_node(root_id, lambda n:
        n.update(receipt_refs=[1])), rejected)
    product_id = next(n["id"] for n in nodes if n["op"] == "OrderedProduct" and len(n["args"]["factors"]) == 2)
    selftest_rejection("reordered-word-unchanged-root", lambda: changed_node(product_id, lambda n:
        n["args"]["factors"].reverse()), rejected)
    (root / "ordered-word.jsonl").write_bytes(original)
    wrong_root = {**word, "root_sha256": nodes[0]["node_sha256"]}
    selftest_rejection("other-root-same-bundle", lambda:
        read_normalized_pair(root, wrong_root, dictionary, 1), rejected)
    (root / "ordered-word.jsonl").write_bytes(original[:-1])
    selftest_rejection("JSONL-without-final-LF", lambda: read_normalized_pair(root, word, dictionary, 1), rejected)
    (root / "ordered-word.jsonl").write_bytes(original)
    selftest_rejection("bool-is-not-F3", lambda: signrep(True), rejected)
    selftest_rejection("relator-hash-LF-boundary", lambda: child_links("Rel", {
        "dictionary_sha256": dictionary_sha, "relator_id": "r:1", "letters": [1, 2],
        "letters_sha256": sha(canonical([1, 2])[:-1])}), rejected)
    require(read_normalized_pair(root, word, dictionary, 1) == normalized, "selftest_original_word_restored")
    return {"name": "ordered-word-same-root-mod54", "status": "PASS", "rejected_cases": rejected}


def selftest_history(root: Path) -> dict[str, Any]:
    rejected: list[str] = []
    row0 = bytes([27]) + bytes(PHYSICAL_BYTES - 1)
    row1 = bytes([9]) + bytes(PHYSICAL_BYTES - 1)
    row2 = bytes([0, 3]) + bytes(PHYSICAL_BYTES - 2)
    residual = bytes([1]) + bytes(PHYSICAL_BYTES - 1)
    target = {"parent_remainder_sha256": sha(residual), "remainder_sha256": sha(residual), "scalar": 0}
    instruction = {"schema": "fixture.instruction", "offer": 8059, "rank": 3, "generation": 8060,
        "physical_offset": 2 * PHYSICAL_BYTES, "predecessor": OLD_STATE_SHA, "sigma": 2, "lead": 5,
        "target_scalar": 0, "target_remainder_sha256": sha(residual), "physical_sha256": sha(row2)}
    instruction["rolling_sha256"] = sha(bytes.fromhex(OLD_STATE_SHA) + canonical(instruction))
    result = seal("fixture-result", {"pivot": {"scale": 2, "lead": 5, "normalized_sha256": sha(row2)},
        "target": target, "rank_before": 2, "rank_after": 3, "generation_before": 8059, "generation_after": 8060,
        "parent_state_head": OLD_STATE_SHA, "state_head": instruction["rolling_sha256"],
        "target_derivation": {"mode": "derived", "original_rho2_directly_read": False,
            "original_rho2_packed_sha256": RHO2_FILES["task640-payload/rho2.bin"][1],
            "accepted_target_derivation_parents": [],
            "identity": "parent_remainder - new_remainder = target.scalar * new_normalized_row",
            "new_delta": {"instruction_sha256": sha(canonical(instruction)), "normalized_sha256": sha(row2),
                "state_head": instruction["rolling_sha256"], "target_sha256": sha(canonical(target))}}})
    metadata = canonical(seal("metadata-fixture", {"not_numerical_certificate": True}))
    parents = fixture_parents(root, {
        "state": {"state/manifest.json": metadata, "state/physical.bin": row0 + row1},
        "e": {"output/manifest.json": metadata, "output/instruction.json": canonical(instruction),
              "output/result.json": canonical(result), "output/physical-normalized.bin": row2,
              "output/target-remainder.bin": residual},
        "continuation": {"output/HEAD": metadata}},
        {"state": "state/manifest.json", "e": "output/manifest.json", "continuation": "output/HEAD"})
    head = {"kind": "Separator", "lambda_sha256": sha(b"lambda"), "completed_steps": 0}
    def new_history() -> TargetHistory:
        h = TargetHistory(parents, Ancestors(parents), dict(head), {"terminal": "UNKNOWN_CAP"}, {}, {})
        h.current_target = sha(residual)
        h.pivots = [{"pivot_id": 0, "target_scalar": 1}, {"pivot_id": 1, "target_scalar": 2}]
        return h
    history = new_history()
    first = history.add_row("state", "state/physical.bin", 0, sha(row0), 3)
    second = history.add_row("state", "state/physical.bin", PHYSICAL_BYTES, sha(row1), 2)
    require(history.ancestors.entries[first]["offset"] == 0 and
            history.ancestors.entries[second]["offset"] == PHYSICAL_BYTES, "selftest_base3_four_trit_offsets")
    history.add_delta("e", "output", e_recipe("e"), "external-e")
    pivot = history.pivots[-1]
    require(pivot["pivot_id"] == 2 and pivot["target_scalar"] == pivot["literal_exponent"] == 0 and
            history.ancestors.entries[pivot["row_ref"]]["offset"] == 0 and len(history.pivots) == 3,
            "selftest_zero_target_retains_pivot_with_local_zero_offset")
    require(history.output()["positive_applicability"] == "NOT_APPLICABLE", "selftest_nonzero_readout_stays_available")
    def bad_instruction() -> None:
        bad = {**instruction, "physical_offset": 0}
        bad["rolling_sha256"] = sha(bytes.fromhex(OLD_STATE_SHA) +
            canonical({k: v for k, v in bad.items() if k != "rolling_sha256"}))
        replace_fixture(parents, "e", "output/instruction.json", canonical(bad))
        new_history().add_delta("e", "output", e_recipe("e"), "external-e")
    selftest_rejection("global-offset-is-not-delta-file-offset", bad_instruction, rejected)
    replace_fixture(parents, "e", "output/instruction.json", canonical(instruction))
    replace_fixture(parents, "e", "output/physical-normalized.bin", bytes([81]) + row2[1:])
    selftest_rejection("base3-byte-above80", lambda: new_history().add_row(
        "e", "output/physical-normalized.bin", 0, None, 5), rejected)
    replace_fixture(parents, "e", "output/physical-normalized.bin", row2)
    selftest_rejection("delta-global-offset-outside-single-row", lambda: new_history().add_row(
        "e", "output/physical-normalized.bin", 2 * PHYSICAL_BYTES, None, 5), rejected)
    bad_result = json.loads(canonical(result))
    bad_result["target"]["scalar"] = False
    bad_result["sha256"] = sha(canonical({k: v for k, v in bad_result.items() if k != "sha256"}))
    replace_fixture(parents, "e", "output/result.json", canonical(bad_result))
    selftest_rejection("bool-target-coefficient", lambda:
        new_history().add_delta("e", "output", e_recipe("e"), "external-e"), rejected)
    bad_result = json.loads(canonical(result))
    bad_result["target_derivation"]["new_delta"]["target_sha256"] = sha(b"wrong-delta")
    bad_result["sha256"] = sha(canonical({k: v for k, v in bad_result.items() if k != "sha256"}))
    replace_fixture(parents, "e", "output/result.json", canonical(bad_result))
    selftest_rejection("last-derived-delta-mismatch", lambda:
        new_history().add_delta("e", "output", e_recipe("e"), "external-e"), rejected)
    replace_fixture(parents, "e", "output/result.json", canonical(result))
    history.head.update(kind="LinearMembershipCandidate", lambda_sha256=None)
    history.terminal["terminal"] = "LINEAR_MEMBERSHIP_CANDIDATE"
    selftest_rejection("nonzero-residual-with-linear-null", history.output, rejected)
    replace_fixture(parents, "e", "output/target-remainder.bin", bytes(PHYSICAL_BYTES))
    history.current_target = sha(bytes(PHYSICAL_BYTES))
    require(history.output()["positive_applicability"] == "LINEAR_ZERO_CANDIDATE",
            "selftest_linear_zero_legal_null_metadata")
    require(loop_snapshot_directory(1) == "output/snapshots/000000" and
            e_recipe("continuation", "000000")["raw_file"] == "output/snapshots/000000/e/raw/raw-word.json",
            "selftest_step_one_uses_snapshot_zero")
    selftest_rejection("zero-committed-step", lambda: loop_snapshot_directory(0), rejected)
    selftest_rejection("bool-committed-step", lambda: loop_snapshot_directory(True), rejected)
    selftest_rejection("external-E-with-loop-snapshot", lambda: e_recipe("e", "000000"), rejected)
    out = parents.roots["continuation"] / "output"
    for name in ("fixed", "snapshots/000000", "snapshots/000001", "steps/000001", "steps/000002", "invocations"):
        (out / name).mkdir(parents=True, exist_ok=True)
    before = inventory(parents.roots["continuation"])
    validate_continuation_layout(parents, 1)
    require(inventory(parents.roots["continuation"]) == before, "selftest_readonly_tail_not_adopted")
    (out / "steps/000003").mkdir()
    selftest_rejection("unregistered-tail-past-head-plus-one", lambda:
        validate_continuation_layout(parents, 1), rejected)
    (out / "steps/000003").rmdir()
    require(p1_location(505)[:3] == ("old", 1, 0) and p1_location(2014)[:3] == ("new", 0, 0),
            "selftest_old_new_owner_local_boundary")
    selftest_rejection("bool-P1-ID", lambda: p1_location(True), rejected)
    return {"name": "target-history-positioned-readonly", "status": "PASS", "rejected_cases": rejected}


def raw_fixture_record(dictionary: Any, witness: Any, witness_sha: str, geometry_sha: str,
                       nexts: list[int], paths: dict[int, tuple[int, ...]]) -> Any:
    """Small literal fixture expanded only for canaries, never for the actual target."""
    nodes = [{"id": "identity", "op": "Identity"}, {"id": "x", "op": "Letter", "letter": 1},
             {"id": "y", "op": "Letter", "letter": 2}]
    factors = []
    for at, cycle in enumerate(witness["cycles"]):
        suffix, edge = str(at), cycle["edge"]
        nodes.extend([
            {"id": "tail-" + suffix, "op": "Ref", "namespace": "oracle-tree", "key": edge // 2},
            {"id": "head-" + suffix, "op": "Ref", "namespace": "oracle-tree", "key": nexts[edge]},
            {"id": "head-inverse-" + suffix, "op": "Inverse", "node": "head-" + suffix},
            {"id": "cycle-" + suffix, "op": "OrderedProduct",
             "factors": ["tail-" + suffix, ("x", "y")[edge % 2], "head-inverse-" + suffix]},
            {"id": "cycle-power-" + suffix, "op": "IntegerPower", "node": "cycle-" + suffix,
             "exponent": (0, 1, -1)[cycle["coefficient"]]}])
        factors.append("cycle-power-" + suffix)
    nodes.extend([
        {"id": "w", "op": "OrderedProduct", "factors": factors},
        {"id": "r-x", "op": "Ref", "namespace": "normalizer-v459", "key": "r_x"},
        {"id": "r-y", "op": "Ref", "namespace": "normalizer-v459", "key": "r_y"},
        {"id": "r-x-cube", "op": "IntegerPower", "node": "r-x", "exponent": 3},
        {"id": "r-y-cube", "op": "IntegerPower", "node": "r-y", "exponent": 3},
        {"id": "r-x-inverse", "op": "Inverse", "node": "r-x"},
        {"id": "r-y-inverse", "op": "Inverse", "node": "r-y"},
        {"id": "commutator", "op": "OrderedProduct",
         "factors": ["r-x-inverse", "r-y-inverse", "r-x", "r-y"]}])
    words: dict[str, tuple[int, ...]] = {}
    def expand(node: Any) -> tuple[int, ...]:
        op = node["op"]
        if op == "Identity":
            value = ()
        elif op == "Letter":
            value = (node["letter"],)
        elif op == "Ref":
            value = paths[node["key"]] if node["namespace"] == "oracle-tree" else \
                    tuple(dictionary["relators"]["normalizer:" + node["key"]])
        elif op == "OrderedProduct":
            value = tuple(letter for name in node["factors"] for letter in words[name])
        else:
            power = -1 if op == "Inverse" else node["exponent"]
            value = words[node["node"]]
            value = (tuple(-x for x in reversed(value)) if power < 0 else value) * abs(power)
        words[node["id"]] = value
        return value
    def small_readout(word: tuple[int, ...]) -> tuple[int, int, int]:
        a, b, omega = 0, 0, 0
        for letter in word:
            if abs(letter) == 1:
                step = 1 if letter == 1 else -1
                omega += b * step
                a += step
            else:
                b += 1 if letter == 2 else -1
        return a, b, omega % 3
    for node in nodes:
        expand(node)
    if witness["kind"] == "chord":
        a, b, omega = small_readout(words["w"])
        require((a, b, omega) == (0, 0, 2), "selftest_fixture_commutator_orientation")
        tail = [
            {"id": "repair-x", "op": "IntegerPower", "node": "r-x-cube", "exponent": 0},
            {"id": "repair-y", "op": "IntegerPower", "node": "r-y-cube", "exponent": 0},
            {"id": "repair-central", "op": "IntegerPower", "node": "commutator", "exponent": -1},
            {"id": "raw-root", "op": "OrderedProduct", "factors": ["w", "repair-x", "repair-y", "repair-central"]}]
    else:
        tail = [{"id": "raw-root", "op": "IntegerPower",
                 "node": ("r-x", "r-y")[witness["coordinate"]], "exponent": 9}]
    nodes.extend(tail)
    for node in tail:
        expand(node)
    values = []
    for node in nodes:
        a, b, omega = small_readout(words[node["id"]])
        values.append({"id": node["id"], "exponent": [a, b], "omega": omega, "length": len(words[node["id"]])})
    stream = bytes(letter & 255 for letter in words["raw-root"])
    return seal("raw-word", {"grammar": "ordered-slp-v1", "root": "raw-root", "nodes": nodes, "node_values": values,
        "witness_sha256": witness_sha, "geometry_manifest_sha256": geometry_sha,
        "cycles": witness["cycles"], "eta": witness["eta"],
        "normalizers": {"dictionary": {"file": "scratchpad/a0_v2_words.json",
            "bytes": DATA_PINS["scratchpad/a0_v2_words.json"][0], "sha256": DATA_PINS["scratchpad/a0_v2_words.json"][1]},
            "raw_relators_sha256": NORMALIZER_ROSTER_SHA,
            "words": [{"name": name, "length": size, "word_sha256": digest}
                      for name, (size, digest) in NORMALIZER_WORDS.items()]},
        "word_bound": {"actual_slp_length": len(stream), "normalized": len(stream), "unrepaired": len(words["w"])},
        "word_stream": {"encoding": "signed-byte:1=01,-1=ff,2=02,-2=fe",
                        "letters": len(stream), "bytes": len(stream), "sha256": sha(stream), "full_eof": True}})


def selftest_raw(root: Path) -> dict[str, Any]:
    rejected: list[str] = []
    dictionary = literal_dictionary()
    geometry = canonical(seal("metadata-fixture", {"not_numerical_certificate": True}))
    parents_array, edges, nexts = [0] * 54432, [0] * 54432, [0] * 108864
    parents_array[0] = edges[0] = 0xffffffff
    # A tiny positive tree and two non-tree edges yield xy(yx)^-1.
    paths = {0: (), 1: (1,), 2: (2,), 3: (1, 1), 4: (2, 2), 5: (1, 1, 1), 6: (1, 1, 2)}
    for vertex, parent, edge in ((1, 0, 0), (2, 0, 1), (3, 1, 2), (4, 2, 5), (5, 3, 6), (6, 3, 7)):
        parents_array[vertex], edges[vertex], nexts[edge] = parent, edge, vertex
    witness = seal("witness", {"kind": "chord",
        "cycles": [{"edge": edge, "coefficient": coefficient}
                   for edge, coefficient in zip((2, 3, 4, 5, 6, 7), (0, 1, 2, 0, 0, 0))], "eta": [0, 0]})
    raw = raw_fixture_record(dictionary, witness, sha(canonical(witness)), sha(geometry), nexts, paths)
    payloads = {"e": {"output/manifest.json": geometry, "output/raw-word.json": canonical(raw)},
        "oracle": {"output/manifest.json": geometry, "output/geometry/manifest.json": geometry,
            "output/tree/witness.json": canonical(witness),
            "output/geometry/parent.u32": struct.pack("<54432I", *parents_array),
            "output/geometry/parent-edge.u32": struct.pack("<54432I", *edges),
            "output/geometry/next-pos.u32": struct.pack("<108864I", *nexts)}}
    parents = fixture_parents(root, payloads, {"e": "output/manifest.json", "oracle": "output/manifest.json"})
    sequence = 0
    def probe(*, compile_word: bool = False) -> Any:
        nonlocal sequence
        sequence += 1
        with (root / ("word-" + str(sequence) + ".jsonl")).open("xb") as stream:
            ancestors = Ancestors(parents)
            history = TargetHistory(parents, ancestors, {}, {}, {}, {})
            literal = argparse.Namespace(dictionary=dictionary)
            dag = WordDAG(stream, sha(canonical(dictionary)),
                          {key: tuple(word) for key, word in dictionary["relators"].items()}, lambda: len(ancestors.entries))
            compiler = TargetWordCompiler(history, literal, dag)
            value = compiler.load_raw(e_recipe("e"))
            if not compile_word:
                return value
            root_id = compiler.resolve(compiler.symbol("raw-e", "external-e/raw-root",
                parents.pin("e", "output/raw-word.json")["sha256"]))
            dag.flush()
            require({"raw-e", "normalizer"}.issubset({entry["namespace"] for entry in ancestors.entries}),
                    "selftest_Ref_keeps_own_parent_origin")
            return list(dag.pairs[root_id]), ancestors.entries, compiler.symbol_order
    pair, entries, symbols = probe(compile_word=True)
    require(pair == [0, 0] and "tree" in {entry["namespace"] for entry in entries} and
            all(any(item["key"] == "external-e/cycle-power-" + str(at) for item in symbols) for at in range(6)),
            "selftest_raw_six_cycles_zero_edges_resolved")
    original = canonical(raw)
    def mutate_raw(action: Callable[[Any], None]) -> None:
        changed = json.loads(original)
        action(changed)
        changed["sha256"] = sha(canonical({k: v for k, v in changed.items() if k != "sha256"}))
        replace_fixture(parents, "e", "output/raw-word.json", canonical(changed))
        probe()
    def central_two(value: Any) -> None:
        next(item for item in value["nodes"] if item["id"] == "repair-central")["exponent"] = 2
    selftest_rejection("central-plus2-is-not-signed-minus1", lambda: mutate_raw(central_two), rejected)
    selftest_rejection("zero-cycle-edge-omitted", lambda: mutate_raw(lambda value:
        next(item for item in value["nodes"] if item["id"] == "w")["factors"].pop(0)), rejected)
    selftest_rejection("raw-root-factor-order", lambda: mutate_raw(lambda value:
        value["nodes"][-1]["factors"].reverse()), rejected)
    selftest_rejection("raw-other-witness-same-snapshot", lambda: mutate_raw(lambda value:
        value.update(witness_sha256=sha(b"other-witness"))), rejected)
    replace_fixture(parents, "e", "output/raw-word.json", original)
    bad_edges = list(edges)
    bad_edges[1] = 1
    replace_fixture(parents, "oracle", "output/geometry/parent-edge.u32", struct.pack("<54432I", *bad_edges))
    selftest_rejection("tree-edge-endpoint-mismatch", probe, rejected)
    replace_fixture(parents, "oracle", "output/geometry/parent-edge.u32", struct.pack("<54432I", *edges))
    for coordinate in (0, 1):
        auxiliary = seal("witness", {"kind": "auxiliary", "coordinate": coordinate, "cycles": [],
                                    "eta": [1, 0] if coordinate == 0 else [0, 1]})
        replace_fixture(parents, "oracle", "output/tree/witness.json", canonical(auxiliary))
        aux_raw = raw_fixture_record(dictionary, auxiliary, sha(canonical(auxiliary)), sha(geometry), nexts, paths)
        replace_fixture(parents, "e", "output/raw-word.json", canonical(aux_raw))
        pair, _, _ = probe(compile_word=True)
        require(pair == ([18, 0] if coordinate == 0 else [0, 18]), "selftest_aux9_same_raw_root_mod54")
        bad = json.loads(canonical(aux_raw))
        bad["nodes"][-1]["exponent"] = 3
        bad["sha256"] = sha(canonical({k: v for k, v in bad.items() if k != "sha256"}))
        replace_fixture(parents, "e", "output/raw-word.json", canonical(bad))
        selftest_rejection("auxiliary-cube-instead-of-nine-" + str(coordinate), probe, rejected)
    hashes = [sha(label) for label in (b"four-B", b"source", b"witness")]
    b = seal("B", {"characters": [0, 1, 2, 3], "all_four_summed": True, "eof": True,
        "by_character_sha256": hashes[0], "source_correction_sha256": hashes[1], "witness_sha256": hashes[2]})
    check_four_B(b, 4 * PHYSICAL_BYTES, *hashes)
    selftest_rejection("three-B-payloads", lambda: check_four_B(b, 3 * PHYSICAL_BYTES, *hashes), rejected)
    bad_b = seal("B", {**{k: v for k, v in b.items() if k not in ("schema", "sha256")}, "characters": [0]})
    selftest_rejection("selected-character-only-B", lambda: check_four_B(bad_b, 4 * PHYSICAL_BYTES, *hashes), rejected)
    selftest_rejection("B-other-witness", lambda: check_four_B(
        b, 4 * PHYSICAL_BYTES, hashes[0], hashes[1], sha(b"stale")), rejected)
    return {"name": "raw-cycle-auxiliary-four-B", "status": "PASS", "rejected_cases": rejected}


def selftest() -> Any:
    progress("new-boundary-selftests")
    with tempfile.TemporaryDirectory(prefix="r07-positive-word-selftest-") as temporary:
        root = Path(temporary)
        tests = [selftest_word(root / "word"), selftest_history(root / "history"), selftest_raw(root / "raw")]
    require(len(tests) == 3 and all(test["status"] == "PASS" and test["rejected_cases"] for test in tests),
            "three_new_interface_groups")
    return seal("selftest", {"status": "PASS", "tests": tests,
        "fixture_scope": "new-word-and-metadata-interfaces-only;not-accepted-numerical-certificates",
        "production_interfaces_used": ["WordDAG", "read_normalized_pair", "TargetHistory.add_row",
            "TargetHistory.add_delta", "TargetHistory.output", "loop_snapshot_directory",
            "validate_continuation_layout", "TargetWordCompiler.load_raw", "TargetWordCompiler.resolve", "check_four_B"],
        "old_success_suites_rerun": 0, "candidate": False, "cross_checked": False, "verified": False})


def diagnostic(args: argparse.Namespace, status: str, error: BaseException) -> Any:
    value = seal("diagnostic", {"status": status, "phase": PHASE, "reason": type(error).__name__ + ":" + str(error),
        "successful_bundle": False, "partial_output_only": OUTPUT_CREATED is not None,
        "resource_limits": {"max_seconds": args.max_seconds, "max_memory_mib": args.max_memory_mib},
        "elapsed_seconds": round(time.monotonic() - STARTED, 6),
        "grade2_member": "NOT_DECIDED", "grade2_nonmember": "NOT_DECIDED", "full_A0": False,
        "candidate": False, "cross_checked": False, "verified": False})
    if OUTPUT_CREATED is not None:
        name = "resource-stop.json" if status == "UNKNOWN_RESOURCE" else "rejected.json"
        with (OUTPUT_CREATED / name).open("xb") as stream:
            stream.write(canonical(value))
            stream.flush()
            os.fsync(stream.fileno())
    return value


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--selftest", action="store_true")
    for role in PARENT_ROLES:
        if not role.startswith("block-"):
            parser.add_argument("--" + role + "-root")
    parser.add_argument("--block-root", action="append", default=[])
    parser.add_argument("--acceptance")
    parser.add_argument("--output")
    parser.add_argument("--max-seconds", type=int)
    parser.add_argument("--max-memory-mib", type=int)
    args = parser.parse_args()
    if args.selftest:
        if args.max_seconds is None:
            args.max_seconds = 300
        if args.max_memory_mib is None:
            args.max_memory_mib = 1024
        if args.output or args.acceptance or args.block_root or any(
                getattr(args, role.replace("-", "_") + "_root") for role in PARENT_ROLES if not role.startswith("block-")):
            parser.error("--selftest takes only resource ceilings")
    else:
        missing = ["--" + role + "-root" for role in PARENT_ROLES if not role.startswith("block-") and
                   not getattr(args, role.replace("-", "_") + "_root")]
        missing += ["--" + name.replace("_", "-") for name in ("acceptance", "output", "max_seconds", "max_memory_mib")
                    if getattr(args, name) is None]
        if missing or len(args.block_root) != 4:
            parser.error("required: " + ", ".join(missing) + "; --block-root exactly four times in owner order")
    if not plain_int(args.max_seconds, 1) or not plain_int(args.max_memory_mib, 1):
        parser.error("resource ceilings must be positive integers")
    return args


def main() -> int:
    global STARTED, DEADLINE, MEMORY_LIMIT_BYTES, OUTPUT_CREATED
    args = parse_args()
    STARTED = time.monotonic()
    DEADLINE = STARTED + args.max_seconds
    MEMORY_LIMIT_BYTES = args.max_memory_mib * (1 << 20)
    OUTPUT_CREATED = None
    signal.signal(signal.SIGTERM, request_stop)
    signal.signal(signal.SIGINT, request_stop)
    try:
        if sys.platform != "win32":
            import resource
            _, hard = resource.getrlimit(resource.RLIMIT_AS)
            require(hard == resource.RLIM_INFINITY or MEMORY_LIMIT_BYTES <= hard, "memory_ceiling_above_process_limit")
            resource.setrlimit(resource.RLIMIT_AS, (MEMORY_LIMIT_BYTES, hard))
        value = selftest() if args.selftest else run_actual(args)
        status = 0
    except (ResourceStop, MemoryError, KeyboardInterrupt) as error:
        value, status = diagnostic(args, "UNKNOWN_RESOURCE", error), 3
    except Exception as error:
        value, status = diagnostic(args, "FAIL", error), 1
    sys.stdout.buffer.write(canonical(value))
    sys.stdout.buffer.flush()
    return status


if __name__ == "__main__":
    raise SystemExit(main())
