#!/usr/bin/env python3
"""Independent direct-enumeration checker for g760 L3 resume v2.

This file imports neither v1 nor v2 producer.  It uses the older frozen
seedspan arithmetic to reconstruct E4 from the authenticated q3 receipt,
writes its own target/Sigma expression path, and enumerates all 59,049 PC
elements for each of the eleven PB4 relators at every freshly completed j.
"""

from __future__ import annotations

import argparse
import copy
import functools
import hashlib
import importlib.util
import itertools
import json
import sys
import time
from collections import defaultdict, deque
from pathlib import Path
from typing import Any, Iterable, Sequence


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "d972-r07-760-l3-target6-resume/v2"
CHECKPOINT_SCHEMA = "d972-r07-760-l3-target6-resume-checkpoint/v2"
FINAL_MARKER = "R07_760_L3_TARGET6_RESUME_V2_CHECKER_PASS"
DEFAULT_RECEIPT = Path(
    "search/certs/d972_r07_760_l3_target6_resume_"
    "preflight_v2_20260826.json")
Q3_PATH = Path(
    "ci/b345_157en_artifacts_32458556448/d972_b345_q3_chief_v1.json")
SEEDSPAN_PATH = Path("search/d972_b345_seedspan_triple4_v1.py")
V1_PATH = Path("search/d972_r07_760_l3_target6_v1.py")
V1_PREFLIGHT_PATH = Path(
    "search/certs/d972_r07_760_l3_target6_preflight_v1_20260826.json")
TASK_PATH = Path("sol/luna_task_164_r07_760_l3_target6_resume_v2.md")
PRIOR_RECEIPT_PATH = Path(
    "search/certs/d972_r07_760_l3_target6_prior_"
    "run32901384400_v1_20260826.json")
PRIOR_LOG_PATH = Path(
    "search/certs/d972_r07_760_l3_target6_prior_"
    "run32901384400_producer_v1_20260826.log")
J_ORDER = tuple(range(2, 13))
FRESH_J_ORDER = (9, 10, 11, 12)
INHERITED_PREFIX = (2, 3, 4, 5, 6, 7, 8)
START_J = 9
TRANSLATED_D2_COUNT = 11 * (3 ** 10)
MAX_DIMENSION = 180000
MAX_RSS_MIB = 5600

PARENT_SHA = "3680e8bcbac37747467175454b082485b2ae296f1fb05244435d8f44979d4e90"
BASE_SHA = "518f09820b8d7baee6b58ebf366cebf7b02a9a945cd1350cf8c701a4e6bc2b4d"
OLD20_SHA = "b79f105ec2963ae55b69480f8ed8ab13083d01cb936da32edb4798698c22055d"
PREFLIGHT_STATE = "R07_760_L3_TARGET6_RESUME_V2_PREFLIGHT_READY"
CHECKPOINT_STATE = "R07_760_L3_TARGET6_RESUME_V2_CHECKPOINT_READY"
PRIOR_RUN_ID = 32901384400
PRIOR_HEAD_SHA = "c1e7eb8fcd08676d5a6efad82add2c1c832a22c0"
PRIOR_RECEIPT_BYTES = 3239
PRIOR_RECEIPT_SHA = (
    "1c739559eee368ba676c694960be21db94d6bc2292a6136d89b97bedfef3e15b")
PRIOR_LOG_BYTES = 164
PRIOR_LOG_SHA = (
    "fc3901c29f958e216e17ba175be4857ee26cc140f3f809f0e29833b636ccd436")
V1_BYTES = 53284
V1_SHA = "7048e73a02e76df5d49fd359c52d5be70ae99d70aa95ebe74b28c4a18f130fde"
TASK_BYTES = 5292
TASK_SHA = "761359bda0fc14543ab9266ec61139006403525d828811bb2af5d27d34ccfc9d"

PIN_SPECS = {
    "task_164": (TASK_PATH, TASK_BYTES, TASK_SHA),
    "v1_producer_data_only": (V1_PATH, V1_BYTES, V1_SHA),
    "v1_preflight": (V1_PREFLIGHT_PATH, 663780,
        "4d305a1af415ffb5acf1d029a69c1b720961fce88dc86575d8fde2d504a787ab"),
    "prior_receipt": (PRIOR_RECEIPT_PATH, PRIOR_RECEIPT_BYTES,
        PRIOR_RECEIPT_SHA),
    "prior_producer_log": (PRIOR_LOG_PATH, PRIOR_LOG_BYTES, PRIOR_LOG_SHA),
    "q3": (Q3_PATH, 231570,
        "3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72"),
    "seedspan": (SEEDSPAN_PATH, 535219,
        "fe18fc31fdf3f9416ebb829112ccbd514c27e6a8d30fe24691842865277a0b29"),
}

PRODUCER_V2_PIN_SPECS = {
    "task_164": (TASK_PATH, TASK_BYTES, TASK_SHA),
    "v1_producer": (V1_PATH, V1_BYTES, V1_SHA),
    "prior_receipt": (PRIOR_RECEIPT_PATH, PRIOR_RECEIPT_BYTES,
        PRIOR_RECEIPT_SHA),
    "prior_producer_log": (PRIOR_LOG_PATH, PRIOR_LOG_BYTES, PRIOR_LOG_SHA),
}

HISTORICAL_C13_AUDIT_ONLY = {
    "search/koubou158_L3_radical_v1_2.py": {
        "bytes": 14488,
        "sha256": "05e96bb3e7d0e9b949cb8d9ec0d216f97a698777df82d56449bcc20f89933f17",
    },
    "search/koubou158_L3_core_v1_2.py": {
        "bytes": 31192,
        "sha256": "4366ebd1759fbd11a795b251101776836ef4ec2a28b7b947b93727208e199c63",
    },
    "crosscheck/check_koubou158_L3_radical_v1.py": {
        "bytes": 28198,
        "sha256": "451aa614d2c83f43291fa80abf09abe425004288717ed6278b5690b511724529",
    },
    "search/certs/koubou158_L3_radical_v1_1_20260822.json": {
        "bytes": 17418,
        "sha256": "4a80c0b4c063eaab31ce32aad69eb9f21c220278dc748e31439aef9af38a2ca2",
    },
    "search/certs/koubou158_L3_radical_v1_2_20260822.json": {
        "bytes": 20930,
        "sha256": "56ab4592bf5b64fbe5605afe063681e8c059929cd8abbc07323988aff4a8440f",
    },
    "crosscheck/verdicts/koubou158_L3_radical_crosscheck_v1_20260822.json": {
        "bytes": 7654,
        "sha256": "c87e12ba96ea95607e99701e1e92786ac93ba08c91ad424dbea1f252304b1b78",
    },
}

W2 = (
    1, 1, 1, 1, -2, -2, -2, -2, -1, 2, -1, -1, -2, -2, 1, 1,
    2, 1, 1, -2, 1, 1, 2, 1, 1, 2, 1, 1, -2, 1, 1, -2, 1, 1,
    2, 2, -1, -1, -2, -1,
)
W3 = (
    1, 1, 1, 1, -2, -2, -2, -2, -1, 2, -1, -1, -2, -1, -1, 2,
    -1, -1, -2, -2, 1, 1, 2, 1, 2, 2, 1, 2, 2, -1, 2, 2, 1, 2,
    1, 1, 2, 2, -1, -1, -2, -1, -1, 2, -1, -1, -2, -2, -2, -1,
    -2, -2, 1, 2, 1, 1, -2, 1,
)
OLD20 = (
    -2, -2, -1, -1, 2, 2, 1, -2, -1, -1,
    2, 2, 2, -1, -2, -2, 1, 1, 1, 1,
)
X0, Y0, Z0 = (4,), (6,), (-4, -6)
WEIGHTS = (1, 1, 1, 1, 1, 1, 2, 2, 2, 2)
BINOM = {0: (1, 0, 0), 1: (1, 1, 0), 2: (1, 2, 1)}


class ResourceStop(RuntimeError):
    pass


class Monitor:
    def __init__(self, seconds: float) -> None:
        require(0 < seconds <= 21600, "checker seconds")
        self.deadline = time.monotonic() + seconds
        self.checks = 0

    def check(self, stage: str, *, force: bool = False) -> None:
        self.checks += 1
        if not force and self.checks % 256:
            return
        if time.monotonic() >= self.deadline:
            raise ResourceStop("checker deadline: " + stage)
        try:
            import resource
            rss = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
            rss_mib = rss / 1024
            if sys.platform == "darwin":
                rss_mib = rss / (1024 * 1024)
            if rss_mib > MAX_RSS_MIB:
                raise ResourceStop(
                    f"checker RSS cap: {rss_mib:.1f} MiB at {stage}")
        except ImportError:
            pass


def require(condition: Any, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True).encode("ascii")


def digest_obj(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def digest_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def authenticate() -> None:
    for label, (path, size, digest) in PIN_SPECS.items():
        full = ROOT / path
        require(full.is_file() and full.stat().st_size == size and
                digest_file(full) == digest, "checker pin: " + label)


def claims() -> dict[str, bool]:
    return {
        "actual_A18_occurrence": False,
        "normalized_Brunnian_class": False,
        "compatible_cofinal_lift": False,
        "ihara_witness": False,
        "all_bases_obstruction": False,
    }


def verify_self_digest(data: dict[str, Any], label: str) -> None:
    require(type(data) is dict and type(data.get("self_digest_sha256")) is str,
            label + " self digest field")
    work = copy.deepcopy(data)
    claimed = work.pop("self_digest_sha256")
    require(claimed == digest_obj(work), label + " self digest")


def producer_v2_pin_manifest() -> dict[str, Any]:
    return {
        label: {"path": path.as_posix(), "bytes": size, "sha256": digest}
        for label, (path, size, digest) in PRODUCER_V2_PIN_SPECS.items()
    }


def authenticate_manifest(rows: dict[str, Any], label: str) -> None:
    require(type(rows) is dict and rows, label + " manifest")
    for name, row in rows.items():
        require(type(row) is dict and type(row.get("path")) is str and
                type(row.get("bytes")) is int and
                type(row.get("sha256")) is str,
                label + " row " + str(name))
        path = ROOT / row["path"]
        require(path.is_file() and path.stat().st_size == row["bytes"] and
                digest_file(path) == row["sha256"],
                label + " pin " + str(name))


def expected_v1_pin_manifest() -> dict[str, Any]:
    raw = (ROOT / V1_PREFLIGHT_PATH).read_bytes()
    data = json.loads(raw.decode("ascii"))
    require(raw == canonical_bytes(data) + b"\n", "v1 preflight canonical")
    verify_self_digest(data, "v1 preflight")
    require(data.get("schema") == "d972-r07-760-l3-target6/v1" and
            data.get("mode") == "preflight" and
            data.get("preflight_state") ==
                "R07_760_L3_TARGET6_PREFLIGHT_READY",
            "v1 preflight envelope")
    rows = data["static"]["pins"]
    authenticate_manifest(rows, "v1 pin")
    return rows


def authenticate_prior() -> dict[str, Any]:
    receipt_raw = (ROOT / PRIOR_RECEIPT_PATH).read_bytes()
    log_raw = (ROOT / PRIOR_LOG_PATH).read_bytes()
    require(len(receipt_raw) == PRIOR_RECEIPT_BYTES and
            hashlib.sha256(receipt_raw).hexdigest() == PRIOR_RECEIPT_SHA,
            "checker prior receipt bytes")
    require(len(log_raw) == PRIOR_LOG_BYTES and
            hashlib.sha256(log_raw).hexdigest() == PRIOR_LOG_SHA,
            "checker prior log bytes")
    data = json.loads(receipt_raw.decode("ascii"))
    require(receipt_raw == canonical_bytes(data) + b"\n",
            "checker prior canonical")
    verify_self_digest(data, "checker prior receipt")
    result = data.get("result", {})
    base = data.get("static", {}).get("base", {})
    require(data.get("schema") == "d972-r07-760-l3-target6/v1" and
            data.get("mode") == "full" and
            data.get("status") ==
                "R07_760_L3_TARGET6_UNKNOWN_RESOURCE" and
            data.get("terminal_token") ==
                "R07_760_L3_TARGET6_UNKNOWN_RESOURCE" and
            result.get("state") ==
                "R07_760_L3_TARGET6_UNKNOWN_RESOURCE" and
            result.get("requested_seconds") == 10200.0 and
            result.get("stage") == "j=9:D2-relator-7" and
            result.get("mathematical_membership_claimed") is False and
            result.get("mathematical_nonmembership_claimed") is False and
            base.get("base_kind") == "r07_760_commutator" and
            base.get("sha256") == BASE_SHA and base.get("length") == 760 and
            base.get("free_exponent_sums") == [0, 0],
            "checker prior exact stop")
    require(data.get("claims") == claims(), "checker prior false claims")
    expected_log = (
        "R07_760_L3_TARGET6_V1_PRODUCER_PASS "
        "terminal=R07_760_L3_TARGET6_UNKNOWN_RESOURCE "
        f"sha256={PRIOR_RECEIPT_SHA} bytes={PRIOR_RECEIPT_BYTES}\n"
    ).encode("ascii")
    require(log_raw == expected_log, "checker prior log marker")
    binding = {
        "run_id": PRIOR_RUN_ID,
        "head_sha": PRIOR_HEAD_SHA,
        "evidence_grade": "producer_control_flow_candidate_only",
        "inherited_candidate_prefix": list(INHERITED_PREFIX),
        "next_j": START_J,
        "unfinished_j_state_serialized": False,
        "prior_receipt": {
            "path": PRIOR_RECEIPT_PATH.as_posix(),
            "bytes": PRIOR_RECEIPT_BYTES,
            "sha256": PRIOR_RECEIPT_SHA,
            "self_digest_sha256": data["self_digest_sha256"],
            "terminal": data["terminal_token"],
            "stage": result["stage"],
            "requested_seconds": result["requested_seconds"],
        },
        "prior_producer_log": {
            "path": PRIOR_LOG_PATH.as_posix(),
            "bytes": PRIOR_LOG_BYTES,
            "sha256": PRIOR_LOG_SHA,
        },
        "v1_producer": {
            "path": V1_PATH.as_posix(), "bytes": V1_BYTES,
            "sha256": V1_SHA,
        },
    }
    binding["binding_sha256"] = digest_obj(binding)
    return binding


def load_seedspan() -> Any:
    spec = importlib.util.spec_from_file_location(
        "_r07_760_l3_seedspan_independent", ROOT / SEEDSPAN_PATH)
    require(spec is not None and spec.loader is not None,
            "seedspan module spec")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    try:
        spec.loader.exec_module(module)
    except BaseException:
        sys.modules.pop(spec.name, None)
        raise
    return module


def reduce_word(word: Iterable[int]) -> list[int]:
    out: list[int] = []
    for value in word:
        letter = int(value)
        require(letter != 0, "zero word letter")
        if out and out[-1] == -letter:
            out.pop()
        else:
            out.append(letter)
    return out


def inv_word(word: Sequence[int]) -> list[int]:
    return reduce_word(-int(x) for x in reversed(word))


def substitute2(word: Sequence[int], x: Sequence[int],
                y: Sequence[int]) -> list[int]:
    out: list[int] = []
    for letter in word:
        choices = {1: x, -1: inv_word(x), 2: y, -2: inv_word(y)}
        require(letter in choices, "F2 alphabet")
        out.extend(choices[letter])
        out = reduce_word(out)
    return out


def exponent_sums(word: Sequence[int]) -> list[int]:
    return [sum(1 if x == i else -1 if x == -i else 0 for x in word)
            for i in (1, 2)]


def construct_base() -> tuple[list[int], list[int]]:
    w2, w3 = list(W2), list(W3)
    parent = reduce_word(w2 + (inv_word(w3) + w2) * 8)
    base = reduce_word(parent + [2] * 36 + [-1] * 108)
    require(len(parent) == 616 and digest_obj(parent) == PARENT_SHA,
            "checker parent")
    require(len(base) == 760 and digest_obj(base) == BASE_SHA and
            exponent_sums(base) == [0, 0], "checker base")
    require(digest_obj(list(OLD20)) == OLD20_SHA, "checker old20")
    return parent, base


def element_blob(value: Any) -> bytes:
    return bytes(value[0]) + bytes(value[1])


def serialize_e4_gradient(row: dict[Any, int]) -> list[list[Any]]:
    return [[int(component), element_blob(value).hex(), int(coefficient) % 3]
            for (component, value), coefficient in sorted(
                row.items(), key=lambda item:
                    (int(item[0][0]), element_blob(item[0][1])))
            if int(coefficient) % 3]


def serialize_pc_gradient(row: dict[Any, int]) -> list[list[Any]]:
    return [[int(component), bytes(value).hex(), int(coefficient) % 3]
            for (component, value), coefficient in sorted(
                row.items(), key=lambda item:
                    (int(item[0][0]), bytes(item[0][1])))
            if int(coefficient) % 3]


def projected_public(row: dict[Any, int]) -> list[list[Any]]:
    return [[int(component), list(monomial), int(coefficient) % 3]
            for (component, monomial), coefficient in sorted(
                row.items(), key=lambda item: (item[0][0], item[0][1]))
            if int(coefficient) % 3]


def fox_gradient(e4: Any, word: Sequence[int]) -> dict[Any, int]:
    out: dict[Any, int] = defaultdict(int)
    prefix = e4.identity
    for letter in word:
        component = abs(int(letter))
        generator = e4.generators[component - 1]
        if letter > 0:
            out[(component, prefix)] += 1
            prefix = e4.mul(prefix, generator)
        else:
            prefix = e4.mul(prefix, e4.inverse(generator))
            out[(component, prefix)] -= 1
    return {key: value % 3 for key, value in out.items() if value % 3}


def collapse_to_pc(row: dict[Any, int]) -> dict[Any, int]:
    out: dict[Any, int] = defaultdict(int)
    for (component, value), coefficient in row.items():
        key = (component, value[1])
        out[key] = (out[key] + int(coefficient)) % 3
    return {key: value for key, value in out.items() if value}


def add_vec(left: dict[Any, int], right: dict[Any, int]) -> dict[Any, int]:
    out: dict[Any, int] = defaultdict(int)
    for key, value in itertools.chain(left.items(), right.items()):
        out[key] = (out[key] + int(value)) % 3
    return {key: value for key, value in out.items() if value}


def neg_vec(row: dict[Any, int]) -> dict[Any, int]:
    return {key: (-int(value)) % 3 for key, value in row.items()
            if int(value) % 3}


def translate_e4(e4: Any, row: dict[Any, int], g: Any) -> dict[Any, int]:
    out: dict[Any, int] = defaultdict(int)
    for (component, value), coefficient in row.items():
        key = (component, e4.mul(g, value))
        out[key] = (out[key] + int(coefficient)) % 3
    return {key: value for key, value in out.items() if value}


def pc_translate(pc: Any, row: dict[Any, int], g: bytes) -> dict[Any, int]:
    out: dict[Any, int] = defaultdict(int)
    for (component, value), coefficient in row.items():
        key = (component, pc.mul(g, value))
        out[key] = (out[key] + int(coefficient)) % 3
    return {key: value for key, value in out.items() if value}


def verify_weights(q3: dict[str, Any]) -> dict[str, Any]:
    pb4 = q3["groups"]["PB4"]
    require(pb4["nilpotency_class"] == 2 and
            pb4["generator_count"] == 10, "checker PC dimensions")
    require(all(int(x) == 3 for x in pb4["relative_orders"]) and
            all(all(int(v) == 0 for v in row)
                for row in pb4["power_relations"]), "checker exponent")
    violations = []
    for entry in pb4["conjugate_relations"]:
        i, j = int(entry["i"]), int(entry["j"])
        coords = [int(x) for x in entry["coords"]]
        if i > 6 or j > 6:
            if coords != [1 if k + 1 == i else 0 for k in range(10)]:
                violations.append([i, j])
        elif any(coords[k] and k + 1 <= 6 and k + 1 != i
                 for k in range(10)):
            violations.append([i, j])
    require(not violations, "checker Jennings weights")
    return {"weights": [1] * 6 + [2] * 4,
            "conjugate_relations_checked":
                len(pb4["conjugate_relations"]),
            "power_relations_checked": len(pb4["power_relations"]),
            "violations": 0}


def delta_and_schreier(e4: Any) \
        -> tuple[list[list[int]], dict[str, Any]]:
    pc = e4.pc
    xbar, ybar, zbar = (e4.eval(list(word))[1]
                         for word in (X0, Y0, Z0))
    require(zbar == pc.inverse(pc.mul(ybar, xbar)),
            "checker zbar identity")
    generators = {
        1: (xbar, xbar, ybar),
        2: (ybar, zbar, zbar),
    }
    identity = (pc.one(), pc.one(), pc.one())
    transversal = {identity: []}
    order = [identity]
    tree = set()
    queue = deque([identity])
    while queue:
        current = queue.popleft()
        for letter in (1, 2):
            nxt = tuple(pc.mul(current[i], generators[letter][i])
                        for i in range(3))
            if nxt not in transversal:
                require(len(order) < 40, "checker Delta cap")
                transversal[nxt] = transversal[current] + [letter]
                order.append(nxt)
                tree.add((current, letter))
                queue.append(nxt)
    words = []
    for current in order:
        for letter in (1, 2):
            if (current, letter) in tree:
                continue
            nxt = tuple(pc.mul(current[i], generators[letter][i])
                        for i in range(3))
            words.append(reduce_word(
                transversal[current] + [letter] + inv_word(transversal[nxt])))
    require(len(order) == 27 and len(words) == 28,
            "checker Schreier roster")
    g1, g2 = generators[1], generators[2]
    commute = tuple(pc.mul(g1[i], g2[i]) for i in range(3)) == \
        tuple(pc.mul(g2[i], g1[i]) for i in range(3))
    return words, {
        "order_Delta": len(order),
        "isomorphism_type": (
            "elementary_abelian_C3^3" if commute else
            "nonabelian_exponent3_order27_class2"),
        "schreier_generator_count": len(words),
        "schreier_rank_formula": "1+[Delta:F2_image]*(2-1)=28",
        "schreier_words_sha256": digest_obj(words),
        "full_kernel_generating_set": True,
    }


def monomials(j: int) -> list[tuple[int, ...]]:
    return sorted(tuple(row) for row in itertools.product(range(3), repeat=10)
                  if sum(a * w for a, w in zip(row, WEIGHTS)) < j)


def build_static_independent() -> tuple[dict[str, Any], dict[str, Any]]:
    authenticate()
    ss = load_seedspan()
    q3 = json.loads((ROOT / Q3_PATH).read_text(encoding="utf-8"))
    require(q3["schema"] == "d972-b345-q-chief/v1", "checker q3 schema")
    _, e4, _ = ss.reconstruct_quotients(q3)
    parent, base = construct_base()

    A = substitute2(base, X0, Y0)
    B = substitute2(base, X0, Z0)
    C = substitute2(base, Y0, Z0)
    target_word = reduce_word(C + inv_word(B) + A)
    alt_no_inverse = reduce_word(C + B + A)
    alt_reordered = reduce_word(A + inv_word(B) + C)
    target_raw = fox_gradient(e4, target_word)
    target_pc = collapse_to_pc(target_raw)
    require(e4.eval(target_word) == e4.identity,
            "checker target E4 value")
    Abar, Bbar, Cbar = (e4.eval(word) for word in (A, B, C))
    prefix = e4.mul(Bbar, e4.inverse(Cbar))
    prefix_inverse = e4.inverse(prefix)
    require(prefix != prefix_inverse, "checker prefix discriminant")

    schreier, delta_public = delta_and_schreier(e4)
    pc_one = e4.pc.one()
    sigma_pc = []
    legal_rows = []
    for ordinal, word in enumerate(schreier, 1):
        values = [
            e4.eval(substitute2(word, left, right))[1]
            for left, right in ((X0, Y0), (X0, Z0), (Y0, Z0))]
        require(values == [pc_one, pc_one, pc_one],
                f"checker context identity {ordinal}")
        ga = fox_gradient(e4, substitute2(word, X0, Y0))
        gb = fox_gradient(e4, substitute2(word, X0, Z0))
        gc = fox_gradient(e4, substitute2(word, Y0, Z0))
        sigma = add_vec(
            translate_e4(e4, add_vec(gc, neg_vec(gb)), prefix), ga)
        pcrow = collapse_to_pc(sigma)
        sigma_pc.append(pcrow)
        public = serialize_pc_gradient(pcrow)
        legal_rows.append({
            "ordinal": ordinal, "schreier_word": word,
            "schreier_word_sha256": digest_obj(word),
            "projected_sigma": public,
            "projected_sigma_sha256": digest_obj(public),
        })

    derived_relators = ss.pure_relations(4)
    receipt_relators = q3["formulas"]["presentations"]["PB4"]["relations"]
    require(derived_relators == receipt_relators and
            len(derived_relators) == 11,
            "checker independently derived PB4 roster")
    relator_pc = []
    relator_rows = []
    for ordinal, word in enumerate(derived_relators, 1):
        require(e4.eval(word) == e4.identity,
                f"checker relator {ordinal}")
        pcrow = collapse_to_pc(fox_gradient(e4, word))
        relator_pc.append(pcrow)
        public = serialize_pc_gradient(pcrow)
        relator_rows.append({
            "ordinal": ordinal, "word": word,
            "word_sha256": digest_obj(word),
            "projected_gradient": public,
            "projected_gradient_sha256": digest_obj(public),
        })

    basis_manifest = []
    for j in J_ORDER:
        basis = monomials(j)
        basis_manifest.append({
            "j": j, "monomial_count": len(basis),
            "dim_Lambda_over_Ij": 6 * len(basis),
            "basis_sha256": digest_obj([list(row) for row in basis]),
        })

    old_A = substitute2(OLD20, X0, Y0)
    old_B = substitute2(OLD20, X0, Z0)
    old_C = substitute2(OLD20, Y0, Z0)
    old_target = reduce_word(old_C + inv_word(old_B) + old_A)
    old_target_raw = fox_gradient(e4, old_target)

    public = {
        "implementation_parent_commit":
            "f3698fffd3b73370f753c4b0d9eb1e86751b1159",
        "runtime_packaging": {
            "self_contained_producer_core": True,
            "imports_HEAD_absent_koubou158_runtime_files": False,
            "runtime_pins_are_prospective_HEAD_files_only": True,
        },
        "historical_C13_audit_only": {
            path: {**row, "runtime_pin": False,
                   "present_in_packaging_HEAD": False}
            for path, row in HISTORICAL_C13_AUDIT_ONLY.items()
        },
        "base": {
            "base_kind": "r07_760_commutator",
            "construction": "w2*(w3^-1*w2)^8*y^36*x^-108",
            "parent_616_word": parent,
            "parent_616_sha256": digest_obj(parent),
            "signed_word": base, "length": len(base),
            "sha256": digest_obj(base),
            "free_exponent_sums": exponent_sums(base),
        },
        "target6": {
            "name": "hexagon_1_coface_0",
            "formula": "C*B^-1*A",
            "X0": list(X0), "Y0": list(Y0), "Z0": list(Z0),
            "A_word_sha256": digest_obj(A),
            "B_word_sha256": digest_obj(B),
            "C_word_sha256": digest_obj(C),
            "word": target_word, "word_length": len(target_word),
            "word_sha256": digest_obj(target_word),
            "alternative_CBA_sha256": digest_obj(alt_no_inverse),
            "alternative_ABinvC_sha256": digest_obj(alt_reordered),
            "raw_E4_gradient": serialize_e4_gradient(target_raw),
            "raw_E4_gradient_sha256":
                digest_obj(serialize_e4_gradient(target_raw)),
            "projected_L3_gradient": serialize_pc_gradient(target_pc),
            "projected_L3_gradient_sha256":
                digest_obj(serialize_pc_gradient(target_pc)),
            "value_identity_in_current_E4": True,
        },
        "prefix_action": {
            "formula": "fbar_xz*fbar_yz^-1",
            "value_hex": element_blob(prefix).hex(),
            "value_sha256": digest_obj(element_blob(prefix).hex()),
            "inverse_value_hex": element_blob(prefix_inverse).hex(),
            "inverse_is_distinct": True,
            "fresh_from_g760": True,
        },
        "legal_overapproximation": {
            "Delta": delta_public,
            "rows": legal_rows, "row_count": len(legal_rows),
            "rows_sha256": digest_obj(legal_rows),
            "all_84_context_values_identity_in_Pi4_3": True,
            "Sigma_homomorphism_on_K":
                "paper one-line: cbar=1 makes Sigma(cd)=Sigma(c)+Sigma(d)",
            "H1_span_equals_full_K_image": True,
            "literal_legal_image_subset_full_K_span": True,
            "overapproximation_safe_direction": "NONMEMBERSHIP_ONLY",
        },
        "PB4_D2": {
            "relation_count": len(relator_rows),
            "relators": relator_rows,
            "relators_sha256": digest_obj(relator_rows),
            "full_translate_count": TRANSLATED_D2_COUNT,
            "base_independent_but_freshly_authenticated": True,
        },
        "Jennings": {
            "weights": verify_weights(q3),
            "j_order": list(J_ORDER), "first_terminal_rule": True,
            "basis_manifest": basis_manifest,
            "projection_enlargement":
                "E4 -> Pi4[3], safe only for NONMEMBERSHIP",
        },
        "historical_old20_diagnostic_only": {
            "signed_word_sha256": digest_obj(list(OLD20)),
            "target_word_sha256": digest_obj(old_target),
            "raw_E4_gradient_sha256":
                digest_obj(serialize_e4_gradient(old_target_raw)),
            "historical_j4_ranks": {
                "D2bar_alone": 310, "V": 4, "combined": 314},
            "imported_as_answer": False,
        },
        "freshness_boundary": {
            "old20_target_imported": False,
            "old20_ranks_required": False,
            "old616_target_imported": False,
            "historical_blocker_imported": False,
            "historical_B0_B1_imported": False,
            "registered_108_family_used": False,
            "literal_five_coface_A18_built": False,
        },
    }
    private = {"e4": e4, "target_pc": target_pc,
               "sigma_pc": sigma_pc, "relator_pc": relator_pc}
    return public, private


def summarize_static_independent(public: dict[str, Any],
                                 prior: dict[str, Any]) -> dict[str, Any]:
    v1_pins = expected_v1_pin_manifest()
    v2_pins = producer_v2_pin_manifest()
    base = public["base"]
    target = public["target6"]
    legal = public["legal_overapproximation"]
    d2 = public["PB4_D2"]
    jennings = public["Jennings"]
    summary = {
        "full_v1_static_rebuilt": True,
        "v1_static_without_pins_sha256": digest_obj(public),
        "v1_pin_manifest_sha256": digest_obj(v1_pins),
        "v1_pin_manifest": v1_pins,
        "v2_pin_manifest_sha256": digest_obj(v2_pins),
        "v2_pin_manifest": v2_pins,
        "prior_binding_sha256": prior["binding_sha256"],
        "base": {
            "base_kind": base["base_kind"],
            "parent_616_sha256": base["parent_616_sha256"],
            "length": base["length"], "sha256": base["sha256"],
            "free_exponent_sums": base["free_exponent_sums"],
        },
        "target6": {
            key: target[key] for key in (
                "name", "formula", "word_length", "word_sha256",
                "raw_E4_gradient_sha256", "projected_L3_gradient_sha256",
                "value_identity_in_current_E4")
        },
        "prefix_action": {
            key: public["prefix_action"][key] for key in (
                "formula", "value_sha256", "inverse_is_distinct",
                "fresh_from_g760")
        },
        "legal_overapproximation": {
            "row_count": legal["row_count"],
            "rows_sha256": legal["rows_sha256"],
            "overapproximation_safe_direction":
                legal["overapproximation_safe_direction"],
        },
        "PB4_D2": {
            "relation_count": d2["relation_count"],
            "relators_sha256": d2["relators_sha256"],
            "full_translate_count": d2["full_translate_count"],
        },
        "Jennings": {
            "weights": jennings["weights"],
            "full_j_order": jennings["j_order"],
            "fresh_j_order": list(FRESH_J_ORDER),
            "first_terminal_rule": jennings["first_terminal_rule"],
            "basis_manifest": [row for row in jennings["basis_manifest"]
                               if row["j"] in FRESH_J_ORDER],
        },
        "freshness_boundary": public["freshness_boundary"],
    }
    summary["binding_sha256"] = digest_obj(summary)
    return summary


class SparseTracker:
    def __init__(self, pivots: dict[int, dict[int, int]] | None = None) -> None:
        self.pivots = copy.deepcopy(pivots) if pivots is not None else {}

    def clone(self) -> "SparseTracker":
        return SparseTracker(self.pivots)

    def reduce(self, vector: dict[int, int]) -> dict[int, int]:
        row = {int(k): int(v) % 3 for k, v in vector.items() if int(v) % 3}
        while row:
            pivot = min(row)
            basis = self.pivots.get(pivot)
            if basis is None:
                break
            coefficient = row[pivot]
            for key, value in basis.items():
                new = (row.get(key, 0) - coefficient * value) % 3
                if new:
                    row[key] = new
                else:
                    row.pop(key, None)
        return row

    def add(self, vector: dict[int, int]) -> bool:
        row = self.reduce(vector)
        if not row:
            return False
        pivot = min(row)
        scalar = row[pivot]
        self.pivots[pivot] = {
            key: (value * scalar) % 3 for key, value in row.items()}
        return True

    @property
    def rank(self) -> int:
        return len(self.pivots)

    def separator(self, target: dict[int, int]) -> dict[int, int] | None:
        remainder = self.reduce(target)
        if not remainder:
            return None
        coordinate = min(remainder)
        phi = {coordinate: 1}
        # Pivot insertion order is streaming-dependent and need not be
        # monotone.  A row at pivot p only uses coordinates > p, so dual
        # back-substitution must follow numeric pivot order, descending.
        for pivot in sorted(self.pivots, reverse=True):
            row = self.pivots[pivot]
            value = -sum(coefficient * phi.get(key, 0)
                         for key, coefficient in row.items()
                         if key != pivot)
            value %= 3
            if value:
                phi[pivot] = value
        return phi


def dot(phi: dict[int, int], row: dict[int, int]) -> int:
    return sum(int(value) * phi.get(key, 0)
               for key, value in row.items()) % 3


def projection_factory(j: int) -> tuple[
        list[tuple[int, ...]], dict[tuple[int, ...], int], Any]:
    basis = monomials(j)
    if 6 * len(basis) > MAX_DIMENSION:
        raise ResourceStop(f"checker dimension cap at j={j}")
    index = {row: ordinal for ordinal, row in enumerate(basis)}

    @functools.lru_cache(maxsize=8192)
    def expand(pcvec: bytes) -> tuple[tuple[int, int], ...]:
        out: dict[int, int] = defaultdict(int)
        ranges = [range(int(a) + 1) for a in pcvec]
        for exponent in itertools.product(*ranges):
            ordinal = index.get(tuple(exponent))
            if ordinal is None:
                continue
            coefficient = 1
            for a, e in zip(pcvec, exponent):
                coefficient = coefficient * BINOM[int(a)][int(e)] % 3
            if coefficient:
                out[ordinal] = (out[ordinal] + coefficient) % 3
        return tuple((key, value) for key, value in sorted(out.items())
                     if value)

    def project(row: dict[Any, int]) -> dict[int, int]:
        out: dict[int, int] = defaultdict(int)
        width = len(basis)
        for (component, pcvec), coefficient in row.items():
            offset = (int(component) - 1) * width
            for ordinal, scalar in expand(bytes(pcvec)):
                key = offset + ordinal
                out[key] = (
                    out[key] + int(coefficient) * int(scalar)) % 3
        return {key: value for key, value in out.items() if value}

    return basis, index, project


def indexed_to_public(row: dict[int, int],
                      basis: Sequence[tuple[int, ...]]) -> list[list[Any]]:
    width = len(basis)
    answer = []
    for coordinate, coefficient in sorted(row.items()):
        component = coordinate // width + 1
        monomial = basis[coordinate % width]
        answer.append([component, list(monomial), int(coefficient) % 3])
    return answer


def enumerate_translated_rows(e4: Any, relators: Sequence[dict[Any, int]],
                              project: Any, monitor: Monitor,
                              stage: str) -> Iterable[dict[int, int]]:
    for relator in relators:
        for coords in itertools.product(range(3), repeat=10):
            monitor.check(stage)
            yield project(pc_translate(e4.pc, relator, bytes(coords)))


def verify_phi_stream(e4: Any, phi: dict[int, int],
                      legal: Sequence[dict[int, int]],
                      relators: Sequence[dict[Any, int]],
                      target: dict[int, int], project: Any,
                      monitor: Monitor, stage: str) -> dict[str, Any]:
    bad_legal = sum(dot(phi, row) != 0 for row in legal)
    bad_boundary = 0
    count = 0
    for row in enumerate_translated_rows(
            e4, relators, project, monitor, stage):
        count += 1
        if dot(phi, row):
            bad_boundary += 1
    target_dot = dot(phi, target)
    require(bad_legal == 0 and bad_boundary == 0 and
            count == TRANSLATED_D2_COUNT and target_dot != 0,
            "checker lossless separator pairing")
    return {
        "legal_rows_checked": len(legal),
        "legal_nonzero_pairings": 0,
        "translated_boundary_rows_checked": count,
        "translated_boundary_nonzero_pairings": 0,
        "target_pairing": target_dot,
        "all_generated_rows_annihilated": True,
        "target_pairing_nonzero": True,
        "direct_all_59049_elements_x_11_relators": True,
    }


def direct_j(private: dict[str, Any], j: int,
             monitor: Monitor) -> dict[str, Any]:
    e4 = private["e4"]
    basis, _, project = projection_factory(j)
    legal_rows = [project(row) for row in private["sigma_pc"]]
    legal_tracker = SparseTracker()
    combined = SparseTracker()
    for row in legal_rows:
        legal_tracker.add(row)
        combined.add(row)
    d2 = SparseTracker()
    count = 0
    for row in enumerate_translated_rows(
            e4, private["relator_pc"], project, monitor,
            f"checker j={j} direct rank"):
        count += 1
        d2.add(row)
        combined.add(row)
    require(count == TRANSLATED_D2_COUNT, "checker translated count")
    target = project(private["target_pc"])
    phi = combined.separator(target)
    nonmember = phi is not None
    own_separator = None
    if phi is not None:
        terms = indexed_to_public(phi, basis)
        pairing = verify_phi_stream(
            e4, phi, legal_rows, private["relator_pc"], target,
            project, monitor, f"checker j={j} own separator")
        own_separator = {
            "terms": terms, "terms_sha256": digest_obj(terms),
            "support": len(terms), "pairing_replay": pairing,
        }
    legal_public = [
        indexed_to_public(row, basis) for row in legal_rows]
    return {
        "semantic": {
            "j": j, "monomial_count": len(basis),
            "dim_Lambda_over_Ij": 6 * len(basis),
            "basis_sha256": digest_obj([list(row) for row in basis]),
            "rank_D2bar_alone": d2.rank,
            "rank_legal_overapproximation": legal_tracker.rank,
            "rank_combined": combined.rank,
            "target_projected_sha256":
                digest_obj(indexed_to_public(target, basis)),
            "legal_projected_rows_sha256": digest_obj(legal_public),
            "PB4_translate_count": count,
            "nonmember": nonmember,
        },
        "basis": basis, "project": project,
        "legal_rows": legal_rows, "target": target,
        "own_separator": own_separator,
    }


def independent_fresh(private: dict[str, Any], observed_js: Sequence[int],
                      seconds: float) -> dict[str, Any]:
    require(list(observed_js) == list(FRESH_J_ORDER[:len(observed_js)]),
            "checker exact fresh prefix")
    monitor = Monitor(seconds)
    progression = []
    rows = {}
    first = None
    for j in observed_js:
        monitor.check(f"checker j={j} start", force=True)
        row = direct_j(private, j, monitor)
        progression.append(row["semantic"])
        rows[j] = row
        if row["semantic"]["nonmember"]:
            first = j
            break
    require(len(progression) == len(observed_js),
            "checker observed prefix stops at first nonmember")
    return {"first_nonmember_j": first, "progression": progression,
            "rows": rows, "monitor": monitor,
            "translated_rows": len(observed_js) * TRANSLATED_D2_COUNT}


def verify_envelope(data: dict[str, Any], raw: bytes) -> None:
    require(raw == canonical_bytes(data) + b"\n", "canonical v2 receipt")
    verify_self_digest(data, "v2 receipt")
    require(data.get("schema") == SCHEMA and data.get("claims") == claims(),
            "v2 receipt envelope")


def checkpoint_filename(j: int) -> str:
    require(j in FRESH_J_ORDER, "checker checkpoint j")
    return f"d972_r07_760_l3_target6_resume_v2_j{j}.json"


def resolve_receipt_path(path: str) -> Path:
    candidate = Path(path)
    return candidate if candidate.is_absolute() else ROOT / candidate


def validate_public_row(row: dict[str, Any],
                        summary: dict[str, Any]) -> None:
    require(type(row) is dict and type(row.get("j")) is int and
            row["j"] in FRESH_J_ORDER, "checker row j")
    manifest = {int(item["j"]): item
                for item in summary["Jennings"]["basis_manifest"]}
    expected = manifest[row["j"]]
    require(row.get("monomial_count") == expected["monomial_count"] and
            row.get("dim_Lambda_over_Ij") ==
                expected["dim_Lambda_over_Ij"] and
            row.get("basis_sha256") == expected["basis_sha256"],
            "checker row basis")
    dimension = int(row["dim_Lambda_over_Ij"])
    ranks = [row.get("rank_D2bar_alone"),
             row.get("rank_legal_overapproximation"),
             row.get("rank_combined")]
    require(all(type(value) is int and 0 <= value <= dimension
                for value in ranks) and
            ranks[0] <= ranks[2] and ranks[1] <= ranks[2],
            "checker row ranks")
    require(type(row.get("target_projected_sha256")) is str and
            len(row["target_projected_sha256"]) == 64 and
            type(row.get("legal_projected_rows_sha256")) is str and
            len(row["legal_projected_rows_sha256"]) == 64 and
            row.get("PB4_translate_count") == TRANSLATED_D2_COUNT and
            row.get("producer_D2_algorithm") ==
                "saturated (x_i-1) BFS, D2 first" and
            type(row.get("per_relator_closure_receipts")) is list and
            len(row["per_relator_closure_receipts"]) == 11 and
            type(row.get("nonmember")) is bool,
            "checker row algorithm")
    separator = row.get("separator")
    if row["nonmember"]:
        require(type(separator) is dict and
                separator.get("terms_sha256") ==
                    digest_obj(separator.get("terms")) and
                separator.get("support") == len(separator.get("terms", [])),
                "checker row separator")
        replay = separator.get("pairing_replay")
        require(type(replay) is dict and
                replay.get("translated_boundary_rows_checked") ==
                    TRANSLATED_D2_COUNT and
                replay.get("translated_boundary_nonzero_pairings") == 0 and
                replay.get("all_generated_rows_annihilated") is True and
                replay.get("target_pairing_nonzero") is True and
                replay.get("direct_all_59049_elements_x_11_relators") is True,
                "checker row producer pairing")
    else:
        require(separator is None, "checker member row separator absent")


def validate_checkpoint_data(data: dict[str, Any],
                             summary: dict[str, Any],
                             prior: dict[str, Any]) -> None:
    verify_self_digest(data, "v2 checkpoint")
    require(data.get("schema") == CHECKPOINT_SCHEMA and
            data.get("mode") == "checkpoint" and
            data.get("checkpoint_state") == CHECKPOINT_STATE and
            data.get("grade") == "CANDIDATE" and
            data.get("claims") == claims(),
            "checker checkpoint envelope")
    require(data.get("inherited_candidate_prefix") ==
                list(INHERITED_PREFIX) and
            data.get("inherited_prefix_grade") ==
                "producer_control_flow_candidate_only" and
            data.get("start_j") == START_J and
            data.get("static_binding") == summary and
            data.get("prior_run_binding") == prior and
            data.get("unfinished_j_inferred") is False and
            data.get("relator_level_state_serialized") is False,
            "checker checkpoint fixed contract")
    progression = data.get("fresh_j_progression")
    require(type(progression) is list and progression,
            "checker checkpoint progression")
    completed = [row.get("j") for row in progression]
    require(completed == data.get("completed_j_prefix") and
            completed == list(FRESH_J_ORDER[:len(completed)]),
            "checker checkpoint prefix")
    for row in progression:
        validate_public_row(row, summary)
    nonmembers = [row["j"] for row in progression if row["nonmember"]]
    require(len(nonmembers) <= 1 and
            (not nonmembers or nonmembers == [completed[-1]]) and
            data.get("first_nonmember_j") ==
                (nonmembers[0] if nonmembers else None),
            "checker checkpoint first terminal")
    expected_next = None if nonmembers or completed[-1] == FRESH_J_ORDER[-1] \
        else completed[-1] + 1
    require(data.get("next_j") == expected_next and
            data.get("current_j_row_sha256") ==
                digest_obj(progression[-1]),
            "checker checkpoint next/current")


def validate_checkpoint_manifest(data: dict[str, Any],
                                 summary: dict[str, Any],
                                 prior: dict[str, Any]) -> int:
    result = data["result"]
    progression = result["j_progression"]
    manifest = result["checkpoint_manifest"]
    require(type(progression) is list and type(manifest) is list and
            len(progression) == len(manifest),
            "checker checkpoint manifest length")
    expected_previous = None
    for index, (row, record) in enumerate(zip(progression, manifest)):
        j = FRESH_J_ORDER[index]
        require(row.get("j") == j and type(record) is dict and
                record.get("j") == j and
                record.get("filename") == checkpoint_filename(j) and
                type(record.get("path")) is str and
                type(record.get("bytes")) is int and
                type(record.get("sha256")) is str,
                "checker checkpoint manifest row")
        path = resolve_receipt_path(record["path"])
        require(path.is_file() and path.name == record["filename"] and
                path.stat().st_size == record["bytes"] and
                digest_file(path) == record["sha256"],
                "checker checkpoint file binding")
        raw = path.read_bytes()
        checkpoint = json.loads(raw.decode("ascii"))
        require(raw == canonical_bytes(checkpoint) + b"\n",
                "checker checkpoint canonical")
        validate_checkpoint_data(checkpoint, summary, prior)
        require(checkpoint["fresh_j_progression"] ==
                    progression[:index + 1] and
                checkpoint["prior_checkpoint"] == expected_previous,
                "checker cumulative checkpoint chain")
        expected_previous = record
    return len(manifest)


def parse_phi(terms: Sequence[Sequence[Any]],
              basis: Sequence[tuple[int, ...]]) -> dict[int, int]:
    width = len(basis)
    index = {row: ordinal for ordinal, row in enumerate(basis)}
    phi: dict[int, int] = {}
    for component, monomial, coefficient in terms:
        key_tuple = tuple(int(x) for x in monomial)
        require(1 <= int(component) <= 6 and key_tuple in index and
                int(coefficient) in (1, 2), "producer separator term")
        coordinate = (int(component) - 1) * width + index[key_tuple]
        require(coordinate not in phi, "producer separator duplicate")
        phi[coordinate] = int(coefficient)
    require(phi, "producer separator nonempty")
    return phi


def compare_row_semantics(observed_rows: Sequence[dict[str, Any]],
                          independent: dict[str, Any],
                          private: dict[str, Any],
                          mutations: bool) -> int:
    semantic_keys = {
        "j", "monomial_count", "dim_Lambda_over_Ij", "basis_sha256",
        "rank_D2bar_alone", "rank_legal_overapproximation",
        "rank_combined", "target_projected_sha256",
        "legal_projected_rows_sha256", "PB4_translate_count", "nonmember",
    }
    require(len(observed_rows) == len(independent["progression"]),
            "checker fresh progression length")
    for observed, expected in zip(
            observed_rows, independent["progression"]):
        require({key: observed[key] for key in semantic_keys} == expected,
                f"checker fresh row mismatch j={expected['j']}")
        require(observed["producer_D2_algorithm"] ==
                "saturated (x_i-1) BFS, D2 first" and
                len(observed["per_relator_closure_receipts"]) == 11,
                "checker producer BFS roster")

    mutation_count = 0
    first = independent["first_nonmember_j"]
    if first is not None:
        require(observed_rows[-1]["j"] == first,
                "checker first nonmember last")
        row = independent["rows"][first]
        producer_sep = observed_rows[-1]["separator"]
        phi = parse_phi(producer_sep["terms"], row["basis"])
        require(producer_sep["terms_sha256"] ==
                    digest_obj(producer_sep["terms"]) and
                producer_sep["support"] == len(phi),
                "checker producer separator serialization")
        pairing = verify_phi_stream(
            private["e4"], phi, row["legal_rows"],
            private["relator_pc"], row["target"], row["project"],
            independent["monitor"], "checker producer separator")
        require(producer_sep["pairing_replay"] == pairing,
                "checker producer separator direct replay")
        if mutations:
            require(dot({}, row["target"]) == 0,
                    "checker forged zero separator")
            witness = next((value for value in row["legal_rows"] if value),
                           None)
            if witness is None:
                witness = next(enumerate_translated_rows(
                    private["e4"], private["relator_pc"], row["project"],
                    independent["monitor"], "checker mutation witness"))
            coordinate = min(witness)
            forged = dict(phi)
            forged[coordinate] = (forged.get(coordinate, 0) + 1) % 3
            if forged.get(coordinate) == 0:
                forged.pop(coordinate)
            require(dot(forged, witness) != 0,
                    "checker forged separator rejected")
            mutation_count = 2
    return mutation_count


def validate_common_result(data: dict[str, Any],
                           summary: dict[str, Any],
                           prior: dict[str, Any]) -> None:
    require(data.get("grade") == "CANDIDATE" and
            data.get("static_binding") == summary and
            data.get("prior_run_binding") == prior and
            data.get("v2_pins") == producer_v2_pin_manifest(),
            "checker v2 static/prior/pins")
    authenticate_manifest(data["v2_pins"], "producer v2")
    result = data["result"]
    require(result.get("inherited_candidate_prefix") ==
                list(INHERITED_PREFIX) and
            result.get("inherited_prefix_grade") ==
                "producer_control_flow_candidate_only" and
            result.get("start_j") == START_J and
            result.get("fresh_j_order") == list(FRESH_J_ORDER) and
            result.get("fresh_j_order_tested") ==
                [row.get("j") for row in result.get("j_progression", [])] and
            result.get("unfinished_j_inferred") is False and
            result.get("relator_level_state_serialized") is False and
            result.get("mathematical_membership_claimed") is False and
            result.get("mathematical_nonmembership_claimed") is False and
            result.get("actual_A18_lift_claimed") is False and
            result.get("registered_108_family_used") is False and
            result.get("literal_A18_computed") is False and
            result.get("normalized_Brunnian_class_computed") is False,
            "checker result scope boundary")


def compare_full(data: dict[str, Any], expected_summary: dict[str, Any],
                 prior: dict[str, Any], private: dict[str, Any],
                 mutations: bool, seconds: float) -> dict[str, Any]:
    require(data.get("mode") == "full" and
            data.get("terminal_token") in {
                "R07_760_L3_TARGET6_NONMEMBER",
                "R07_760_L3_TARGET6_MEMBER_INCONCLUSIVE",
                "R07_760_L3_TARGET6_UNKNOWN_RESOURCE",
                "R07_760_L3_TARGET6_INPUT_STOP"} and
            data.get("status") == data.get("terminal_token") and
            data.get("result", {}).get("state") == data.get("terminal_token"),
            "checker full terminal")
    validate_common_result(data, expected_summary, prior)
    checkpoint_count = validate_checkpoint_manifest(
        data, expected_summary, prior)
    result = data["result"]
    observed_rows = result["j_progression"]
    observed_js = [row["j"] for row in observed_rows]
    require(observed_js == list(FRESH_J_ORDER[:len(observed_js)]),
            "checker fresh j exact prefix")
    independent = independent_fresh(private, observed_js, seconds)
    mutation_count = compare_row_semantics(
        observed_rows, independent, private, mutations)
    require(result.get("first_nonmember_j") ==
                independent["first_nonmember_j"],
            "checker first nonmember agreement")

    terminal = data["terminal_token"]
    if terminal == "R07_760_L3_TARGET6_NONMEMBER":
        require(independent["first_nonmember_j"] is not None and
                observed_js[-1] == independent["first_nonmember_j"],
                "checker NONMEMBER terminal")
    elif terminal == "R07_760_L3_TARGET6_MEMBER_INCONCLUSIVE":
        require(observed_js == list(FRESH_J_ORDER) and
                independent["first_nonmember_j"] is None,
                "checker MEMBER_INCONCLUSIVE terminal")
    else:
        require(type(result.get("stage")) is str and result["stage"] and
                type(result.get("reason")) is str and result["reason"] and
                type(result.get("requested_seconds")) in (int, float),
                "checker claim-free stop fields")
    return {
        "checkpoint_count": checkpoint_count,
        "fresh_rows": len(observed_rows),
        "translated_rows": independent["translated_rows"],
        "mutations": mutation_count,
        "full_replay": bool(observed_rows),
    }


def validate_preflight_core(data: dict[str, Any],
                            summary: dict[str, Any],
                            prior: dict[str, Any]) -> None:
    require(data.get("mode") == "preflight" and
            data.get("preflight_state") == PREFLIGHT_STATE and
            "terminal_token" not in data and "status" not in data and
            data.get("grade") == "CANDIDATE" and
            data.get("static_binding") == summary and
            data.get("prior_run_binding") == prior and
            data.get("v2_pins") == producer_v2_pin_manifest() and
            data.get("resume_contract", {}).get(
                "inherited_candidate_prefix") == list(INHERITED_PREFIX) and
            data["resume_contract"].get("start_j") == START_J and
            data["resume_contract"].get("fresh_j_order") ==
                list(FRESH_J_ORDER) and
            data["resume_contract"].get(
                "interrupted_j_recomputed_from_relator_1") is True and
            data["resume_contract"].get("member_is_actual_A18_lift") is False,
            "checker preflight contract")
    authenticate_manifest(summary["v1_pin_manifest"], "preflight v1")
    authenticate_manifest(summary["v2_pin_manifest"], "preflight v2")
    contract = data.get("checkpoint_contract", {})
    require(contract.get("schema") == CHECKPOINT_SCHEMA and
            contract.get("checkpoint_state") == CHECKPOINT_STATE and
            contract.get("j_values") == list(FRESH_J_ORDER) and
            contract.get("cumulative_public_rows") is True and
            contract.get("prior_checkpoint_sha_and_bytes") is True and
            contract.get("canonical_self_digest") is True and
            contract.get("relator_level_state_serialized") is False,
            "checker checkpoint schema contract")


def toy_separator_tests() -> int:
    tracker = SparseTracker()
    tracker.add({0: 1}); tracker.add({1: 1})
    require(not tracker.reduce({0: 2, 1: 1}), "toy member")
    target = {2: 1}
    phi = tracker.separator(target)
    require(phi is not None and dot(phi, target) != 0 and
            all(dot(phi, row) == 0 for row in tracker.pivots.values()),
            "toy nonmember")
    require(dot({}, target) == 0, "toy forged target-zero")
    forged = dict(phi); forged[0] = 1
    require(dot(forged, tracker.pivots[0]) != 0,
            "toy forged missed row")

    unordered = SparseTracker()
    require(unordered.add({2: 1, 3: 1}) and
            unordered.add({0: 1, 1: 1}) and
            unordered.add({1: 1, 2: 1}) and
            list(unordered.pivots) == [2, 0, 1],
            "nonmonotone pivot insertion canary")
    unordered_phi = unordered.separator({3: 1})
    require(unordered_phi is not None and
            dot(unordered_phi, {3: 1}) != 0 and
            all(dot(unordered_phi, row) == 0
                for row in unordered.pivots.values()),
            "numeric reverse-pivot separator")
    old_bad = {3: 1}
    for pivot in reversed(list(unordered.pivots)):
        row = unordered.pivots[pivot]
        value = -sum(coefficient * old_bad.get(key, 0)
                     for key, coefficient in row.items() if key != pivot)
        if value % 3:
            old_bad[pivot] = value % 3
    require(any(dot(old_bad, row) != 0
                for row in unordered.pivots.values()),
            "insertion-order mutation rejected")
    return 3


def toy_checkpoint_tests() -> int:
    prior = {"binding_sha256": "a" * 64}
    summary = {"Jennings": {"basis_manifest": [{
        "j": 9, "monomial_count": 1,
        "dim_Lambda_over_Ij": 6, "basis_sha256": "b" * 64,
    }]}}
    row = {
        "j": 9, "monomial_count": 1, "dim_Lambda_over_Ij": 6,
        "basis_sha256": "b" * 64, "rank_D2bar_alone": 1,
        "rank_legal_overapproximation": 1, "rank_combined": 2,
        "target_projected_sha256": "c" * 64,
        "legal_projected_rows_sha256": "d" * 64,
        "PB4_translate_count": TRANSLATED_D2_COUNT,
        "producer_D2_algorithm": "saturated (x_i-1) BFS, D2 first",
        "per_relator_closure_receipts": [{} for _ in range(11)],
        "nonmember": False, "separator": None,
    }
    good = {
        "schema": CHECKPOINT_SCHEMA, "mode": "checkpoint",
        "checkpoint_state": CHECKPOINT_STATE, "grade": "CANDIDATE",
        "inherited_candidate_prefix": list(INHERITED_PREFIX),
        "inherited_prefix_grade": "producer_control_flow_candidate_only",
        "start_j": START_J, "completed_j_prefix": [9], "next_j": 10,
        "first_nonmember_j": None, "fresh_j_progression": [row],
        "current_j_row_sha256": digest_obj(row), "prior_checkpoint": None,
        "static_binding": summary, "prior_run_binding": prior,
        "unfinished_j_inferred": False,
        "relator_level_state_serialized": False, "claims": claims(),
    }
    good["self_digest_sha256"] = digest_obj(good)
    validate_checkpoint_data(good, summary, prior)
    labels = []
    for label, mutate in (
        ("skip_prefix", lambda d: d.update({"completed_j_prefix": [10]})),
        ("wrong_next", lambda d: d.update({"next_j": 11})),
        ("row_basis", lambda d: d["fresh_j_progression"][0].update(
            {"basis_sha256": "0" * 64})),
        ("prior_binding", lambda d: d["prior_run_binding"].update(
            {"binding_sha256": "0" * 64})),
        ("claim_flip", lambda d: d["claims"].update(
            {"ihara_witness": True})),
        ("self_digest", lambda d: d.update(
            {"self_digest_sha256": "0" * 64})),
    ):
        bad = copy.deepcopy(good)
        mutate(bad)
        try:
            validate_checkpoint_data(bad, summary, prior)
        except RuntimeError:
            labels.append(label)
            continue
        raise RuntimeError("checker checkpoint mutation survived: " + label)
    require(len(labels) == 6, "checker checkpoint mutation count")
    return len(labels)


def preflight_mutation_suite(data: dict[str, Any],
                             summary: dict[str, Any],
                             prior: dict[str, Any]) -> int:
    labels = []

    def reject(label: str, mutate: Any) -> None:
        bad = copy.deepcopy(data)
        mutate(bad)
        try:
            verify_envelope(bad, canonical_bytes(bad) + b"\n")
            validate_preflight_core(bad, summary, prior)
        except RuntimeError:
            labels.append(label)
            return
        raise RuntimeError("preflight mutation survived: " + label)

    reject("prior_run", lambda d: d["prior_run_binding"].update(
        {"run_id": 0}))
    reject("inherited_prefix", lambda d: d["resume_contract"].update(
        {"inherited_candidate_prefix": [2, 3]}))
    reject("start_j", lambda d: d["resume_contract"].update({"start_j": 8}))
    reject("fresh_order", lambda d: d["resume_contract"].update(
        {"fresh_j_order": [9, 11]}))
    reject("member_lift", lambda d: d["resume_contract"].update(
        {"member_is_actual_A18_lift": True}))
    reject("base_sha", lambda d: d["static_binding"]["base"].update(
        {"sha256": "0" * 64}))
    reject("checkpoint_schema", lambda d: d["checkpoint_contract"].update(
        {"schema": "wrong"}))
    reject("claim_flip", lambda d: d["claims"].update(
        {"ihara_witness": True}))
    require(len(labels) == 8, "preflight mutation count")
    return len(labels) + toy_separator_tests() + toy_checkpoint_tests()


def check(path: Path, *, full: bool, mutations: bool,
          seconds: float) -> dict[str, Any]:
    raw = path.read_bytes()
    data = json.loads(raw.decode("ascii"))
    verify_envelope(data, raw)
    authenticate()
    prior = authenticate_prior()
    public, private = build_static_independent()
    summary = summarize_static_independent(public, prior)
    if full:
        result = compare_full(
            data, summary, prior, private, mutations, seconds)
        terminal = data["terminal_token"]
        print(
            FINAL_MARKER + f" terminal={terminal} "
            f"grade=CROSS_CHECKED_FRESH_ONLY "
            f"inherited_prefix_cross_checked=false "
            f"fresh_rows={result['fresh_rows']} "
            f"translated_rows={result['translated_rows']} "
            f"checkpoints={result['checkpoint_count']} "
            f"mutations={result['mutations']} "
            f"full_replay={str(result['full_replay']).lower()} "
            f"receipt_sha256={hashlib.sha256(raw).hexdigest()}",
            flush=True)
    else:
        validate_preflight_core(data, summary, prior)
        count = preflight_mutation_suite(
            data, summary, prior) if mutations else 0
        print(
            FINAL_MARKER + f" preflight_state={PREFLIGHT_STATE} "
            f"mutations={count} full_replay=false "
            f"receipt_sha256={hashlib.sha256(raw).hexdigest()}",
            flush=True)
    return data


def self_test() -> None:
    authenticate()
    prior = authenticate_prior()
    construct_base()
    separator_count = toy_separator_tests()
    checkpoint_count = toy_checkpoint_tests()
    require(prior["next_j"] == START_J and separator_count == 3 and
            checkpoint_count == 6, "checker selftest contract")
    print(
        "R07_760_L3_TARGET6_RESUME_V2_CHECKER_SELFTEST_PASS "
        "imports_producer=false prior_artifacts=2 "
        f"separator_mutations={separator_count} "
        f"checkpoint_mutations={checkpoint_count}",
        flush=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--receipt", type=Path, default=DEFAULT_RECEIPT)
    parser.add_argument("--full", action="store_true")
    parser.add_argument("--mutations", action="store_true")
    parser.add_argument("--seconds", type=float, default=21000.0)
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return 0
    path = args.receipt if args.receipt.is_absolute() else ROOT / args.receipt
    check(path, full=args.full, mutations=args.mutations,
          seconds=args.seconds)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
