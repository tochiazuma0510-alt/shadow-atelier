#!/usr/bin/env python3
"""R07 pre-A0 single-target A3 producer.

This wrapper owns the g760 reconstruction, the v302 replay and the v303
projection.  The two frozen engines are loaded by digest under private names;
no new helper is imported by the production route.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import time
from pathlib import Path

try:
    import resource
except ImportError:  # pragma: no cover - Windows runner
    resource = None

ROOT = Path(__file__).resolve().parents[1]
P0_PATH = "ci/in/d972_r07_pre_a0_single_target_a3_v1.prereg.v1.json"
P0_BYTES = 6691
P0_SHA256 = "f8092796af77da3ea137908b1cca48db6563c412d937147bc341be29cc49489f"
SCHEMA = "d972-r07-pre-a0-single-target-a3/v1"
RECEIPT_SCHEMA = SCHEMA + "/receipt/v1"
UNKNOWN_INPUT = "UNKNOWN_INPUT"
UNKNOWN_RESOURCE = "UNKNOWN_RESOURCE"
MEMBER_TOP = "R07_PRE_A0_A3_PROJECTED_MEMBER"
NONMEMBER_TOP = "R07_PRE_A0_A3_PROJECTED_NONMEMBER_DUAL"
T227_MEMBER = "PROJECTED_MEMBER_SEED"
T227_NONMEMBER = "PROJECTED_NONMEMBER_DUAL"
T198_TERMINAL = "ROOF_BRIDGE_ISOMORPHISM"
FALSE_FLAGS = ("actual_a3_numerator", "boundary_membership", "cofinal_lift",
               "exact_pb_endpoint_zero", "fake", "Ihara_witness",
               "pointed_mu1", "task192_consumed")
CAPS = {
    "actor_operations": 2000000, "area_builds": 3,
    "authority_bytes": 400000000, "base_abi_builds": 1,
    "block_rank_increases": 486, "block_rows": 100000,
    "checker_roster": 729, "closure_actions": 2000000,
    "closure_runs": 1, "dual_work": 1000000, "dynamic_imports": 2,
    "input_bytes": 500000000, "mutation_work": 100,
    "occurrence_rank_increases": 486, "occurrence_support": 2000000,
    "orbit_actions": 2000000, "rss_bytes": 6442450944,
    "serialized_bytes": 2000000000, "wall_seconds": 21600,
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
EXPECTED_G616_SHA256 = "3680e8bcbac37747467175454b082485b2ae296f1fb05244435d8f44979d4e90"
EXPECTED_G760_SHA256 = "518f09820b8d7baee6b58ebf366cebf7b02a9a945cd1350cf8c701a4e6bc2b4d"
EXPECTED_CENTRAL = {
    "H1": {"rows": [[6], [6], [6]], "sum": [0]},
    "H2": {"rows": [[3], [3], [3]], "sum": [0]},
    "P": {"rows": [[0, 0, 0, 6], [0, 6, 6, 0], [6, 0, 0, 0],
                       [0, 0, 3, 3], [3, 3, 0, 0]], "sum": [0, 0, 0, 0]},
}
LEDGER = [
    {"ordinal": 1, "block": "H1", "block_index": 1, "block_slot": 1,
     "occurrence": "H1_fxy", "type": "E3", "ten_index": 0,
     "context_id": 21, "role": "hexagon_fxy", "factor_sign": 1,
     "orientation": "direct", "fox_prefix_occurrences": [3, 2]},
    {"ordinal": 2, "block": "H1", "block_index": 1, "block_slot": 2,
     "occurrence": "H1_fxz", "type": "E3", "ten_index": 1,
     "context_id": 22, "role": "hexagon_fxz", "factor_sign": -1,
     "orientation": "inverse", "fox_prefix_occurrences": [3]},
    {"ordinal": 3, "block": "H1", "block_index": 1, "block_slot": 3,
     "occurrence": "H1_fyz", "type": "E3", "ten_index": 2,
     "context_id": 23, "role": "hexagon_fyz", "factor_sign": 1,
     "orientation": "direct", "fox_prefix_occurrences": []},
    {"ordinal": 4, "block": "H2", "block_index": 2, "block_slot": 1,
     "occurrence": "H2_fux", "type": "E3", "ten_index": 3,
     "context_id": 24, "role": "hexagon_fux", "factor_sign": -1,
     "orientation": "inverse", "fox_prefix_occurrences": [6, 5]},
    {"ordinal": 5, "block": "H2", "block_index": 2, "block_slot": 2,
     "occurrence": "H2_fxy", "type": "E3", "ten_index": 0,
     "context_id": 21, "role": "hexagon_fxy", "factor_sign": -1,
     "orientation": "inverse", "fox_prefix_occurrences": [6]},
    {"ordinal": 6, "block": "H2", "block_index": 2, "block_slot": 3,
     "occurrence": "H2_fuy", "type": "E3", "ten_index": 4,
     "context_id": 25, "role": "hexagon_fuy", "factor_sign": 1,
     "orientation": "direct", "fox_prefix_occurrences": []},
    {"ordinal": 7, "block": "P1", "block_index": 3, "block_slot": 1,
     "occurrence": "P_b1", "type": "E4", "ten_index": 5,
     "context_id": 1, "role": "pentagon_b1", "factor_sign": 1,
     "orientation": "direct", "fox_prefix_occurrences": [11, 10, 9, 8]},
    {"ordinal": 8, "block": "P2", "block_index": 4, "block_slot": 1,
     "occurrence": "P_b2", "type": "E4", "ten_index": 6,
     "context_id": 27, "role": "pentagon_b2", "factor_sign": 1,
     "orientation": "direct", "fox_prefix_occurrences": [11, 10, 9]},
    {"ordinal": 9, "block": "P3", "block_index": 5, "block_slot": 1,
     "occurrence": "P_b3", "type": "E4", "ten_index": 7,
     "context_id": 21, "role": "pentagon_b3", "factor_sign": 1,
     "orientation": "direct", "fox_prefix_occurrences": [11, 10]},
    {"ordinal": 10, "block": "P5", "block_index": 6, "block_slot": 1,
     "occurrence": "P_b5_inverse", "type": "E4", "ten_index": 8,
     "context_id": 26, "role": "pentagon_b5_inverse_slot", "factor_sign": -1,
     "orientation": "inverse", "fox_prefix_occurrences": [11]},
    {"ordinal": 11, "block": "P4", "block_index": 7, "block_slot": 1,
     "occurrence": "P_b4_inverse", "type": "E4", "ten_index": 9,
     "context_id": 28, "role": "pentagon_b4_inverse_slot", "factor_sign": -1,
     "orientation": "inverse", "fox_prefix_occurrences": []},
]
SOURCE_PINS = {
    "task226_producer": ("search/d972_r07_actual_two_word_endpoint_specializer_v2.py", 40556,
                          "a1532740a7343bd8166c17947f6bd95203a4abdaaafd8e0d9607d3cdf202e6fb"),
    "task227_producer": ("search/d972_r07_typed_single_seed_endpoint_consumer_v2.py", 47135,
                          "755ba97e55266bcdb51796cc1a89a562efa782db48475d0e3479e82e325cde8e"),
}


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True).encode("ascii")


def digest_obj(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def digest_bytes(value):
    return hashlib.sha256(value).hexdigest()


class InputStop(RuntimeError):
    pass


class MutationAccepted(RuntimeError):
    pass


class NarrowReject(RuntimeError):
    pass


class ResourceStop(RuntimeError):
    def __init__(self, phase, cap, value, limit):
        super().__init__(f"phase={phase}:cap={cap}:value={value}:limit={limit}")
        self.phase, self.cap, self.value, self.limit = phase, cap, value, limit


def require(ok, message):
    if ok is not True:
        raise InputStop(message)


class Meter:
    def __init__(self):
        self.started = time.monotonic()
        self.caps = dict(CAPS)
        self.used = {key: 0 for key in self.caps}

    def bump(self, key, amount, phase):
        if key not in self.caps:
            raise InputStop("unregistered resource counter:" + key)
        self.used[key] += amount
        elapsed = time.monotonic() - self.started
        self.used["wall_seconds"] = elapsed
        if self.used[key] > self.caps[key]:
            raise ResourceStop(phase, key, self.used[key], self.caps[key])
        if elapsed > self.caps["wall_seconds"]:
            raise ResourceStop(phase, "wall_seconds", elapsed,
                               self.caps["wall_seconds"])

    def snapshot(self):
        rss = None
        if resource is not None:
            rss = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1024)
            self.used["rss_bytes"] = rss
            if rss > self.caps["rss_bytes"]:
                raise ResourceStop("rss measurement", "rss_bytes", rss,
                                   self.caps["rss_bytes"])
        return {"caps": dict(self.caps), "used": dict(self.used),
                "peak_rss_bytes": rss}


def safe_rel(text, prefix=None):
    value = str(text)
    path = Path(value)
    normalized = value.replace("\\", "/")
    require(not path.is_absolute() and ".." not in path.parts and
            normalized == path.as_posix(), "path alias")
    if prefix is not None:
        require(normalized.startswith(prefix), "path prefix")
    return path


def read_bytes(rel, expected_bytes, expected_sha, meter, phase,
               authority=True):
    path = safe_rel(rel)
    raw = (ROOT / path).read_bytes()
    meter.bump("input_bytes", len(raw), phase)
    if authority:
        meter.bump("authority_bytes", len(raw), phase)
    require(len(raw) == expected_bytes, phase + ":byte length")
    require(digest_bytes(raw) == expected_sha, phase + ":SHA-256")
    return raw


def strip_seal(value, field):
    require(type(value) is dict and type(value.get(field)) is str,
            "missing " + field)
    body = dict(value)
    claimed = body.pop(field)
    require(claimed == digest_obj(body), field + " mismatch")
    return claimed


def iter_pins(value):
    if isinstance(value, dict):
        if (type(value.get("path")) is str and type(value.get("bytes")) is int
                and type(value.get("sha256")) is str):
            yield value["path"], value["bytes"], value["sha256"]
        for child in value.values():
            yield from iter_pins(child)
    elif isinstance(value, list):
        for child in value:
            yield from iter_pins(child)


def load_p0(meter):
    raw = read_bytes(P0_PATH, P0_BYTES, P0_SHA256, meter, "P0")
    try:
        p0 = json.loads(raw)
    except (ValueError, UnicodeError) as exc:
        raise InputStop("P0 JSON:" + str(exc))
    require(raw == canonical(p0), "P0 noncanonical bytes")
    strip_seal(p0, "self_digest_sha256")
    require(p0["schema"] == SCHEMA + "/prereg/v1", "P0 schema")
    require(p0["caps"] == CAPS, "P0 caps")
    require(p0["terminal_vocabulary"] ==
            [MEMBER_TOP, NONMEMBER_TOP, UNKNOWN_INPUT, UNKNOWN_RESOURCE],
            "P0 terminal vocabulary")
    require(p0["central_rows"] == EXPECTED_CENTRAL, "P0 central rows")
    require(p0["mutation_roster"] == [
        "task198_raw_manifest_binding", "task198_ledger_sign",
        "task198_prefix", "g760_letter_digest", "computational_base_mode",
        "forbidden_task192_binding", "H1_central_row", "H2_central_row",
        "P_central_row", "projected_area_target", "ABI_seal_target",
        "forbidden_conclusion_flag"], "P0 mutation roster")
    for flag in FALSE_FLAGS:
        require(p0["false_conclusion_flags"].get(flag) is False,
                "P0 false conclusion flag:" + flag)
    require(p0["authority"]["task303"]["sha256"] ==
            "9868aa26d630138da9b8b963b0f3968e8c2ee698ba4461d596a2b6f155d25cf2",
            "P0 v303 pin")
    acc = p0["authority"]["task227_selftest_acceptance"]
    require(acc == {
        "run": "33153010409",
        "head": "d1e34bb450bdee48633f64b251db5b14580ce798",
        "artifact_id": "9678665435",
        "archive_sha256": "cf67587fe34dd33d8bef1d79e57b942cccb54c03ca4de189b04c0daf97199549",
        "receipt_bytes": 4636766,
        "receipt_sha256": "dd642ad26b336c9ee5c399798b83867465cb9023c4ec08a02af3fa2eeb723df8",
        "verdict_bytes": 615,
        "verdict_sha256": "3ea0e5e59662c3014364adcf11d3ec40d8e52d70a36c20d6529c7e00236238ea",
        "terminal": "R07_TYPED_SINGLE_SEED_ENDPOINT_CONSUMER_V2_SELFTEST_PASS",
        "cases": ["MEMBER", "MEMBER", "NONMEMBER", "MEMBER", "NONMEMBER"],
        "ideal_rows": 486, "translates": 729, "mutation_count": 24,
        "edge_control_count": 3}, "P0 task227 SELFTEST acceptance")
    return p0


def authenticate_authority(p0, meter):
    pins = {}
    for rel, size, sha in iter_pins(p0["authority"]):
        prior = pins.get(rel)
        require(prior is None or prior == (size, sha),
                "conflicting authority pin:" + rel)
        pins[rel] = (size, sha)
    raw_by_path = {}
    for rel, (size, sha) in sorted(pins.items()):
        raw_by_path[rel] = read_bytes(rel, size, sha, meter,
                                      "authority:" + rel)
    return pins, raw_by_path


def local_ledger():
    return copy.deepcopy(LEDGER)


def authenticate_task198(p0, pins, raw_by_path):
    authority = p0["authority"]["task198"]
    receipt_path = authority["receipt"]["path"]
    manifest_path = authority["acceptance_manifest"]["path"]
    receipt_raw = raw_by_path[receipt_path]
    manifest_raw = raw_by_path[manifest_path]
    receipt = json.loads(receipt_raw)
    manifest = json.loads(manifest_raw)
    require(receipt_raw == canonical(receipt), "task198 noncanonical receipt")
    require(manifest_raw == canonical(manifest), "task198 noncanonical manifest")
    receipt_seal = strip_seal(receipt, "self_digest_sha256")
    manifest_seal = strip_seal(manifest, "manifest_self_digest_sha256")
    require(receipt_seal == authority["receipt"]["self_digest_sha256"],
            "task198 receipt self seal binding")
    require(manifest_seal == authority["acceptance_manifest"]["manifest_self_digest_sha256"],
            "task198 manifest self seal binding")
    require(receipt.get("schema") == "d972-r07-seven-context-roof-presentation/v1" and
            receipt.get("status") == "COMPLETE" and
            receipt.get("terminal") == T198_TERMINAL, "task198 receipt terminal")
    require(digest_bytes(receipt_raw) == authority["receipt"]["sha256"] and
            len(receipt_raw) == authority["receipt"]["bytes"],
            "task198 receipt raw binding")
    require(manifest.get("schema") ==
            "d972-r07-seven-context-roof-presentation/v1/acceptance-manifest/v3" and
            manifest.get("accepted") is True and manifest.get("synthetic") is False and
            manifest.get("independent") is True and
            manifest.get("manifest_self_digest_sha256") == manifest_seal,
            "task198 acceptance manifest")
    require(manifest.get("receipt", {}).get("sha256") == authority["receipt"]["sha256"] and
            manifest.get("receipt", {}).get("bytes") == authority["receipt"]["bytes"] and
            manifest.get("receipt", {}).get("self_digest_sha256") == receipt_seal,
            "task198 manifest receipt binding")
    require(manifest.get("task198_source_identities") == authority["source_identities"],
            "task198 source identity binding")
    require(manifest.get("producer", {}).get("run") == authority["producer"]["run"] and
            manifest.get("checker", {}).get("run") == authority["checker"]["run"] and
            manifest.get("producer", {}).get("terminal_line_sha256") ==
            authority["producer"]["terminal_line_sha256"] and
            manifest.get("checker", {}).get("terminal_line_sha256") ==
            authority["checker"]["terminal_line_sha256"],
            "task198 run/head/terminal binding")
    require(manifest.get("producer", {}).get("artifact_id") == authority["producer"]["artifact_id"] and
            manifest.get("checker", {}).get("artifact_id") == authority["checker"]["artifact_id"] and
            manifest.get("producer", {}).get("head") == authority["producer"]["head"] and
            manifest.get("checker", {}).get("head") == authority["checker"]["head"] and
            manifest.get("producer", {}).get("zip_sha256") == authority["producer"]["zip_sha256"] and
            manifest.get("checker", {}).get("zip_sha256") == authority["checker"]["zip_sha256"],
            "task198 artifact/head/archive binding")
    verdict_path = authority["checker_verdict"]["path"]
    verdict_raw = raw_by_path[verdict_path]
    verdict = json.loads(verdict_raw)
    require(verdict_raw == canonical(verdict), "task198 verdict noncanonical")
    require(digest_bytes(verdict_raw) == authority["checker_verdict"]["sha256"] and
            len(verdict_raw) == authority["checker_verdict"]["bytes"],
            "task198 verdict raw binding")
    require(verdict == {"accepted": True, "independent": True,
                        "receipt_terminal": T198_TERMINAL,
                        "schema": "d972-r07-seven-context-roof-presentation/v1/crosscheck/v2"},
            "task198 checker verdict")
    producer_att = raw_by_path[authority["producer_attestation"]["path"]]
    checker_att = raw_by_path[authority["checker_attestation"]["path"]]
    require(digest_bytes(producer_att) == authority["producer_attestation"]["sha256"] and
            len(producer_att) == authority["producer_attestation"]["bytes"] and
            producer_att.decode("ascii") ==
            "R07_SEVEN_CONTEXT_ROOF_PRESENTATION_V1_PRODUCER_TERMINAL ROOF_BRIDGE_ISOMORPHISM\n",
            "task198 producer attestation")
    require(digest_bytes(checker_att) == authority["checker_attestation"]["sha256"] and
            len(checker_att) == authority["checker_attestation"]["bytes"] and
            checker_att.decode("ascii") ==
            "R07_SEVEN_CONTEXT_ROOF_PRESENTATION_V1_CHECKER_PASS terminal=ROOF_BRIDGE_ISOMORPHISM rows=6441\n",
            "task198 checker attestation")
    bridge = receipt.get("bridge", {})
    rows = bridge.get("occurrence_ledger")
    require(rows == local_ledger(), "task198 occurrence ledger")
    require(bridge.get("ten_to_eleven") == [0, 1, 2, 3, 0, 4, 5, 6, 7, 8, 9],
            "task198 insertion map")
    require("section_cocycle" in receipt.get("evaluator", {}).get("entry_points", {}),
            "task198 evaluator ABI")
    require(digest_obj(rows) == bridge.get("occurrence_ledger_sha256"),
            "task198 ledger digest")
    return rows, {
        "receipt_path": receipt_path, "receipt_bytes": len(receipt_raw),
        "receipt_sha256": digest_bytes(receipt_raw),
        "manifest_path": manifest_path, "manifest_bytes": len(manifest_raw),
        "manifest_sha256": digest_bytes(manifest_raw),
        "receipt_self_digest_sha256": receipt_seal,
        "manifest_self_digest_sha256": manifest_seal,
    }


def red(word):
    out = []
    for letter in word:
        require(type(letter) is int and letter != 0 and abs(letter) <= 6,
                "word letter")
        if out and out[-1] == -letter:
            out.pop()
        else:
            out.append(letter)
    return out


def winv(word):
    return [-letter for letter in reversed(word)]


def commword(left, right):
    return red(winv(left) + winv(right) + list(left) + list(right))


def pp(left, right):
    return red(list(right) + list(left))


def subst(word, left, right):
    out = []
    for letter in word:
        image = left if abs(letter) == 1 else right
        out.extend(image if letter > 0 else winv(image))
    return red(out)


PB3_BRACKETS = {(0, 1): (1,), (0, 2): (-1,), (1, 2): (1,)}
PB4_BRACKETS = {
    (0, 1): (1, 0, 0, 0), (0, 3): (-1, 0, 0, 0),
    (1, 3): (1, 0, 0, 0), (0, 2): (0, 1, 0, 0),
    (0, 4): (0, -1, 0, 0), (2, 4): (0, 1, 0, 0),
    (1, 2): (0, 0, 1, 0), (1, 5): (0, 0, -1, 0),
    (2, 5): (0, 0, 1, 0), (3, 4): (0, 0, 0, 1),
    (3, 5): (0, 0, 0, -1), (4, 5): (0, 0, 0, 1),
}


def bracket(i, j, degree):
    table = PB3_BRACKETS if degree == 3 else PB4_BRACKETS
    width = 1 if degree == 3 else 4
    if i == j:
        return (0,) * width
    if i > j:
        return tuple((-x) % 9 for x in bracket(j, i, degree))
    return tuple(x % 9 for x in table.get((i, j), (0,) * width))


def cmul(left, right, degree):
    central = 1 if degree == 3 else 4
    na, za, nb, zb = left[:degree], left[degree:], right[:degree], right[degree:]
    z = [(za[i] + zb[i]) % 9 for i in range(central)]
    for i in range(degree):
        for j in range(i + 1, degree):
            q = bracket(i, j, degree)
            for k in range(central):
                z[k] = (z[k] - na[j] * nb[i] * q[k]) % 9
    return tuple((na[i] + nb[i]) % 9 for i in range(degree)) + tuple(z)


def cinv(value, degree):
    central = 1 if degree == 3 else 4
    z = [(-x) % 9 for x in value[degree:]]
    for i in range(degree):
        for j in range(i + 1, degree):
            q = bracket(i, j, degree)
            for k in range(central):
                z[k] = (z[k] - value[i] * value[j] * q[k]) % 9
    return tuple((-x) % 9 for x in value[:degree]) + tuple(z)


def cpow(value, exponent, degree):
    out = (0,) * (degree + (1 if degree == 3 else 4))
    for _ in range(exponent % 9):
        out = cmul(out, value, degree)
    return out


def ceval(word, degree):
    width = degree + (1 if degree == 3 else 4)
    out = (0,) * width
    for letter in word:
        generator = [0] * width
        generator[abs(letter) - 1] = 1
        value = tuple(generator)
        out = cmul(out, value if letter > 0 else cinv(value, degree), degree)
    return out


def sparse_add(left, right, scale=1):
    out = dict(left)
    for key, value in right.items():
        out[key] = (out.get(key, 0) + scale * value) % 3
        if out[key] == 0:
            del out[key]
    return out


def sparse_scale(value, scale):
    return {key: (scale * coefficient) % 3 for key, coefficient in value.items()
            if (scale * coefficient) % 3}


def tag(block, value):
    return {(block, component, key): coefficient
            for (component, key), coefficient in value.items()}


def fox(word, degree):
    width = degree + (1 if degree == 3 else 4)
    current = (0,) * width
    out = {}
    for letter in word:
        generator = [0] * width
        generator[abs(letter) - 1] = 1
        generator = tuple(generator)
        if letter > 0:
            key = (abs(letter) - 1, current)
            out[key] = (out.get(key, 0) + 1) % 3
            current = cmul(current, generator, degree)
        else:
            current = cmul(current, cinv(generator, degree), degree)
            key = (abs(letter) - 1, current)
            out[key] = (out.get(key, 0) - 1) % 3
    return {key: coefficient for key, coefficient in out.items() if coefficient}


def endpoint_block(chain, wanted, degree):
    width = degree + (1 if degree == 3 else 4)
    out = {}
    for (block, component, key), coefficient in chain.items():
        if block != wanted:
            continue
        generator = [0] * width
        generator[component] = 1
        generator = tuple(generator)
        right = cmul(key, generator, degree)
        out[right] = (out.get(right, 0) + coefficient) % 3
        out[key] = (out.get(key, 0) - coefficient) % 3
    return {key: coefficient for key, coefficient in out.items() if coefficient}


def jsg(value):
    return [{"key": list(key), "coefficient": coefficient}
            for key, coefficient in sorted(value.items())]


def literal_substitutions():
    x, y = [1], [3]
    z, u = winv(pp(x, y)), winv(pp(y, x))
    return {
        "PB3": {"x": x, "y": y, "z": z, "u": u,
                "H1": [(x, y, 1), (x, z, -1), (y, z, 1)],
                "H2": [(u, x, -1), (x, y, -1), (u, y, 1)]},
        "PB4": {"generators": [[1], [2], [3], [4], [5], [6]],
                "b_display": [([4], [6], 1),
                              (pp([1], [2]), pp([5], [6]), 1),
                              ([1], [4], 1),
                              (pp([2], [4]), [6], -1),
                              ([1], pp([4], [5]), -1)]},
    }


def factor_data():
    sub = literal_substitutions()
    factors = sub["PB3"]["H1"] + sub["PB3"]["H2"] + sub["PB4"]["b_display"]
    return sub, [(left, right) for left, right, _ in factors], [sign for _, _, sign in factors]


def word_digest(word):
    return digest_obj(list(word))


def construct_g760():
    g616 = red(list(W2) + (winv(list(W3)) + list(W2)) * 8)
    require(len(g616) == 616 and word_digest(g616) == EXPECTED_G616_SHA256,
            "g616 length/digest")
    g760 = red(g616 + [2] * 36 + [-1] * 108)
    require(len(g760) == 760 and word_digest(g760) == EXPECTED_G760_SHA256,
            "g760 length/digest")
    require([sum(1 if x == i else -1 if x == -i else 0 for x in g760)
             for i in (1, 2)] == [0, 0], "g760 exponent sums")
    return g616, g760


def base_checks(pkg, rows, g760):
    words = pkg.get("words", {})
    require(words.get("g0") == g760 and words.get("a") == [] and
            words.get("f") == g760 and words.get("f_equals_reduce_g0_plus_a") is True,
            "computational base word typing")
    abi = pkg.get("specialization_v216_abi", {})
    require(abi.get("ledger") == rows and abi.get("ten_to_eleven") ==
            [0, 1, 2, 3, 0, 4, 5, 6, 7, 8, 9], "base ledger typing")
    literals = abi.get("literals", {})
    require(abi.get("literals_role") in (None, "BASE_REFERENCE_ONLY"),
            "base literals role")
    require(literals.get("rword_f") == literals.get("rword_g") and
            literals.get("relation_factors_f") == literals.get("relation_factors_g") and
            literals.get("relation_words_f") == literals.get("relation_words_g"),
            "base rword_f typing")
    for key in ("B_a",):
        require(all(literals.get(key, {}).get(block) == []
                    for block in ("H1", "H2", "P")), "base B_a zero")
    for index, occurrence in enumerate(abi.get("occurrences", [])):
        require(occurrence.get("rword_f") == occurrence.get("rword_g") and
                occurrence.get("r_f") == occurrence.get("r_g"),
                "base occurrence rword_f")
    require(words["f"] == g760, "base f role")
    return abi


def target_from_fox(g760, rows, abi):
    sub, pairs, signs = factor_data()
    raw_words = [red(subst(g760, left, right)) for left, right in pairs]
    signed_words = [word if signs[i] == 1 else winv(word)
                    for i, word in enumerate(raw_words)]
    targets = {}
    relation_words = []
    for lo, hi, block, degree in ((0, 3, "H1", 3), (3, 6, "H2", 3),
                                  (6, 11, "P", 6)):
        relation = red([letter for index in reversed(range(lo, hi))
                        for letter in signed_words[index]])
        relation_words.append(relation)
        chain = tag(block, sparse_scale(fox(relation, degree), -1))
        target = endpoint_block(chain, block, degree)
        targets[block] = jsg(target)
        one = (0,) * (degree + (1 if degree == 3 else 4))
        direct = sparse_add({one: 1}, {ceval(relation, degree): -1})
        require(target == direct, "Fox endpoint identity:" + block)
    require(abi.get("bar_epsilon_1") == targets, "base target 1-R_B(g760)")
    require(abi.get("literals", {}).get("relation_words_g") == relation_words,
            "base relation words")
    return targets, {"relation_words_g": relation_words,
                     "raw_rwords_g": raw_words, "signed_rwords_g": signed_words}


def central_replay(rows, p0):
    sub, pairs, _ = factor_data()
    expected = p0["central_rows"]
    records = []
    products = {"H1": (0, 0, 0, 0), "H2": (0, 0, 0, 0),
                "P": (0,) * 10}
    sums = {"H1": [0], "H2": [0], "P": [0, 0, 0, 0]}
    for index, row in enumerate(rows):
        degree = 3 if index < 6 else 6
        qx, qy = ceval(pairs[index][0], degree), ceval(pairs[index][1], degree)
        comm = cmul(cmul(cmul(cinv(qx, degree), cinv(qy, degree), degree),
                         qx, degree), qy, degree)
        z0 = cpow(comm, 3, degree)
        require(all(value == 0 for value in z0[:degree]),
                "central q_o(z0) noncentral")
        signed = tuple((row["factor_sign"] * value) % 9
                       for value in z0[degree:])
        block = "H1" if index < 3 else "H2" if index < 6 else "P"
        signed_element = tuple([0] * degree + list(signed))
        product_before = products[block]
        products[block] = cmul(products[block], signed_element, degree)
        sums[block] = [(a + b) % 9 for a, b in zip(sums[block], signed)]
        records.append({"ordinal": row["ordinal"], "block": block,
                        "factor_sign": row["factor_sign"],
                        "q_o_x": list(qx), "q_o_y": list(qy),
                        "q_o_z0": list(z0), "signed_central": list(signed),
                        "product_before": list(product_before),
                        "sum_after": list(sums[block]),
                        "product_after": list(products[block])})
    for block in ("H1", "H2", "P"):
        require(sums[block] == expected[block]["sum"],
                "central sum:" + block)
        require(list(products[block][(3 if block != "P" else 6):]) ==
                expected[block]["sum"], "central product:" + block)
        block_rows = [r["signed_central"] for r in records
                      if r["block"] == block]
        require(block_rows == expected[block]["rows"],
                "central rows:" + block)
    return {"rows": records, "blocks": {
        block: {"signed_rows": expected[block]["rows"],
                "sum": sums[block], "product": list(products[block])}
        for block in ("H1", "H2", "P")},
        "identity_checks": {block: products[block] ==
                             (0,) * len(products[block])
                             for block in ("H1", "H2", "P")}}


def make_projection(full_abi, group, rows, targets, task198_meta):
    occurrences = full_abi["occurrences"]
    occurrence_rows = [{"ordinal": item["ordinal"], "p_o": item["p_o"],
                        "xi_o": item["xi_o"], "w_o": item["w_o"],
                        "u0_o": item["u0"]} for item in occurrences]
    quotient = {
        "modulus": 9,
        "q3_width": 4,
        "q4_width": 10,
        "actor_width": 3,
        "actor_convention": full_abi["actor_convention"],
        "PB3_brackets": group.get("PB3_brackets"),
        "PB4_brackets": group.get("PB4_brackets"),
        "marked_D1_action": "p_o conjugation followed by z0 action",
        "ten_to_eleven": full_abi["ten_to_eleven"],
    }
    body = {
        "schema": SCHEMA + "/projected-a3-interface/v1",
        "mode": "PRE_A0_COMPUTATIONAL_BASE_ONLY",
        "correction_word_constructed": False,
        "task192_consumed": False,
        "f_role": "BASE_REFERENCE_EQUAL_TO_G760",
        "authenticated_ledger": {"rows": rows,
                                  "sha256": digest_obj(rows),
                                  "task198_receipt_sha256": task198_meta["receipt_sha256"],
                                  "task198_manifest_sha256": task198_meta["manifest_sha256"]},
        "quotient_action_abi": quotient,
        "occurrence_rows": occurrence_rows,
        "combined_w": [{"ordinal": item["ordinal"], "terms": item["w_o"]}
                        for item in occurrences],
        "combined_u0": [{"ordinal": item["ordinal"], "terms": item["u0"]}
                         for item in occurrences],
        "target_blocks": targets,
        "target_role": "ONE_MINUS_R_B_G760",
        "projection_only": True,
        "full_package_fields_excluded": ["f", "rword_f", "B_a", "PB_chain_fields"],
    }
    body["canonical_digest_sha256"] = digest_obj(body)
    interface = body
    projected = copy.deepcopy(full_abi)
    projected.update({
        "projection_schema": body["schema"],
        "projection_role": "LOAD_BEARING_A3_ONLY",
        "projected_a3_interface_digest_sha256": body["canonical_digest_sha256"],
        "literals_role": "BASE_REFERENCE_ONLY",
        "base_reference_only": True,
        "base_reference_field_types": {"f": "BASE_REFERENCE_ONLY",
                                       "rword_f": "BASE_REFERENCE_ONLY",
                                       "B_a": "BASE_REFERENCE_ONLY",
                                       "PB_chain_fields": "BASE_REFERENCE_ONLY"},
        "mode": "PRE_A0_COMPUTATIONAL_BASE_ONLY",
        "correction_word_constructed": False,
        "task192_consumed": False,
        "f_role": "BASE_REFERENCE_EQUAL_TO_G760",
    })
    projected["self_digest_sha256"] = digest_obj(projected)
    return interface, projected


def base_reference(pkg, abi, g760):
    literals = abi["literals"]
    pb_fields = {key: literals.get(key) for key in
                 ("e", "one_minus_R_g", "one_minus_R_f", "D1_d_occ", "D1_e",
                  "minus_fox_Rg", "minus_fox_Rf")}
    return {
        "mode": "PRE_A0_COMPUTATIONAL_BASE_ONLY",
        "correction_word_constructed": False,
        "task192_consumed": False,
        "f_role": "BASE_REFERENCE_EQUAL_TO_G760",
        "transfer_evidence": False,
        "full_package_fields": {
            "f": {"type": "BASE_REFERENCE_ONLY", "value": list(g760),
                   "transfer_evidence": False},
            "a": {"type": "BASE_REFERENCE_ONLY", "value": [],
                   "transfer_evidence": False},
            "rword_f": {"type": "BASE_REFERENCE_ONLY",
                        "value": literals["rword_f"], "transfer_evidence": False},
            "B_a": {"type": "BASE_REFERENCE_ONLY",
                    "value": literals["B_a"], "transfer_evidence": False},
            "PB_chain_fields": {"type": "BASE_REFERENCE_ONLY",
                                "value": pb_fields, "transfer_evidence": False},
        },
        "f_equals_g760": pkg["words"]["f"] == g760,
        "B_a_zero": all(literals["B_a"].get(block) == []
                         for block in ("H1", "H2", "P")),
    }


def area_canary(engine, g760, rows, base_targets, meter):
    zword = red(commword([1], [2]) * 3)
    out = []
    for exponent in (0, 1, 2):
        representative = red(list(g760) + zword * exponent)
        package = engine.specialize(representative, [], rows)
        target = package["specialization_v216_abi"]["bar_epsilon_1"]
        require(target == base_targets, "projected area target")
        meter.bump("area_builds", 1, "projected area representative")
        out.append({"t": exponent, "word_length": len(representative),
                    "word_sha256": word_digest(representative),
                    "bar_epsilon_1": target,
                    "label": "PROJECTED_AREA_REPRESENTATIVE_ONLY"})
    return {"zword": zword, "zword_sha256": word_digest(zword), "rows": out,
            "all_equal_base_target": True,
            "label": "PROJECTED_AREA_REPRESENTATIVE_ONLY"}


def resource_canary(phase):
    value = {"schema": "d972-r07-typed-single-seed-endpoint-consumer/v2/resource-canary/v1",
             "terminal": UNKNOWN_RESOURCE, "phase": phase,
             "cap": "serialized_bytes", "value": 0, "limit": 2000000000}
    value["self_digest_sha256"] = digest_obj(value)
    return value


def mutation_fixture(rows, p0, task198_meta, g760, projected, targets, base_ref):
    return {"raw_manifest_binding": {
        "receipt_sha256": task198_meta["receipt_sha256"],
        "manifest_sha256": task198_meta["manifest_sha256"]},
        "ledger": copy.deepcopy(rows), "g760": list(g760),
        "base": copy.deepcopy(base_ref), "central": copy.deepcopy(p0["central_rows"]),
        "area_target": copy.deepcopy(targets), "abi": copy.deepcopy(projected),
        "flags": {flag: False for flag in FALSE_FLAGS}}


def cheap_validate(name, value, reference):
    if name == "task198_raw_manifest_binding":
        if value["raw_manifest_binding"] != reference["raw_manifest_binding"]:
            raise NarrowReject("task198 raw/manifest binding")
    elif name in ("task198_ledger_sign", "task198_prefix"):
        if value["ledger"] != reference["ledger"]:
            raise NarrowReject("task198 ledger " + name.rsplit("_", 1)[-1])
    elif name == "g760_letter_digest":
        if word_digest(value["g760"]) != EXPECTED_G760_SHA256:
            raise NarrowReject("g760 digest")
    elif name == "computational_base_mode":
        if value["base"]["mode"] != "PRE_A0_COMPUTATIONAL_BASE_ONLY":
            raise NarrowReject("computational-base mode")
    elif name == "forbidden_task192_binding":
        if value["base"]["task192_consumed"] is not False:
            raise NarrowReject("task192 binding")
    elif name in ("H1_central_row", "H2_central_row", "P_central_row"):
        if value["central"] != reference["central"]:
            raise NarrowReject(name)
    elif name == "projected_area_target":
        if value["area_target"] != reference["area_target"]:
            raise NarrowReject("projected area target")
    elif name == "ABI_seal_target":
        abi = value["abi"]
        if abi.get("self_digest_sha256") != digest_obj(
                {key: item for key, item in abi.items()
                 if key != "self_digest_sha256"}):
            raise NarrowReject("ABI seal/target")
    elif name == "forbidden_conclusion_flag":
        if any(value["flags"].get(flag) is not False for flag in FALSE_FLAGS):
            raise NarrowReject("forbidden conclusion flag")
    else:
        raise InputStop("unregistered mutation:" + name)


def run_mutations(rows, p0, task198_meta, g760, projected, targets, base_ref, meter):
    roster = p0["mutation_roster"]
    reference = mutation_fixture(rows, p0, task198_meta, g760, projected,
                                 targets, base_ref)
    records = []
    for name in roster:
        mutant = copy.deepcopy(reference)
        if name == "task198_raw_manifest_binding":
            mutant["raw_manifest_binding"]["manifest_sha256"] = "0" * 64
            owner = "raw_manifest_binding"
        elif name == "task198_ledger_sign":
            mutant["ledger"][0]["factor_sign"] *= -1
            owner = "ledger"
        elif name == "task198_prefix":
            mutant["ledger"][0]["fox_prefix_occurrences"] = [2, 3]
            owner = "ledger"
        elif name == "g760_letter_digest":
            mutant["g760"][0] *= -1
            owner = "g760"
        elif name == "computational_base_mode":
            mutant["base"]["mode"] = "MUTATED_FORBIDDEN_MODE"
            owner = "base"
        elif name == "forbidden_task192_binding":
            mutant["base"]["task192_consumed"] = True
            owner = "base"
        elif name == "H1_central_row":
            mutant["central"]["H1"]["rows"][0][0] = 3
            owner = "central"
        elif name == "H2_central_row":
            mutant["central"]["H2"]["rows"][0][0] = 6
            owner = "central"
        elif name == "P_central_row":
            mutant["central"]["P"]["rows"][0][3] = 3
            owner = "central"
        elif name == "projected_area_target":
            mutant["area_target"]["H1"] = []
            owner = "area_target"
        elif name == "ABI_seal_target":
            mutant["abi"]["self_digest_sha256"] = "0" * 64
            owner = "abi"
        elif name == "forbidden_conclusion_flag":
            mutant["flags"]["fake"] = True
            owner = "flags"
        else:
            raise InputStop("unregistered mutation:" + name)
        before = digest_obj(reference[owner])
        after = digest_obj(mutant[owner])
        require(before != after, "mutation owner unchanged:" + name)
        meter.bump("mutation_work", 1, "cheap mutation:" + name)
        try:
            cheap_validate(name, mutant, reference)
        except NarrowReject as exc:
            reason = str(exc)
            records.append({"name": name, "changed_field": owner,
                            "expected_gate": reason,
                            "observed_reason": reason,
                            "before_sha256": before, "after_sha256": after,
                            "first_gate": reason, "rejected": True})
        else:
            raise MutationAccepted("accepted mutation:" + name)
    require([record["name"] for record in records] == roster and
            all(record["rejected"] for record in records),
            "cheap mutation matrix")
    return records


def load_engine(rel, size, sha, tag_name, meter):
    raw = read_bytes(rel, size, sha, meter, "import:" + tag_name)
    path = ROOT / safe_rel(rel)
    module_name = "_d359_producer_" + tag_name
    spec = importlib.util.spec_from_file_location(module_name, path)
    require(spec is not None and spec.loader is not None,
            "import specification:" + tag_name)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    meter.bump("dynamic_imports", 1, "dynamic import:" + tag_name)
    require(digest_bytes(raw) == sha, "post-import source drift:" + tag_name)
    return module


def envelope(terminal, result, meter):
    value = {"schema": RECEIPT_SCHEMA, "terminal": terminal, "result": result,
             "boundary_membership": False, "pointed_mu1": False,
             "exact_pb_endpoint_zero": False, "cofinal_lift": False,
             "fake": False, "Ihara_witness": False}
    value["resource_meter"] = meter.snapshot()
    value["self_digest_sha256"] = digest_obj(value)
    return value


def write_fresh(path_text, value, meter):
    path = safe_rel(path_text, "ci/out/")
    path = ROOT / path
    if path.exists():
        raise InputStop("stale output refused")
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = canonical(value)
    meter.bump("serialized_bytes", len(payload), "receipt serialization")
    with path.open("xb") as handle:
        handle.write(payload)


def production(output):
    meter = Meter()
    try:
        p0 = load_p0(meter)
        pins, raw_by_path = authenticate_authority(p0, meter)
        rows, task198_meta = authenticate_task198(p0, pins, raw_by_path)
        raw_by_path.clear()  # release the single 31-MB receipt byte copy
        g616, g760 = construct_g760()
        t226 = load_engine(*SOURCE_PINS["task226_producer"], "task226", meter)
        t227 = load_engine(*SOURCE_PINS["task227_producer"], "task227", meter)
        package = t226.specialize(g760, [], rows)
        meter.bump("base_abi_builds", 1, "computational base ABI")
        full_abi = base_checks(package, rows, g760)
        targets, target_trace = target_from_fox(g760, rows, full_abi)
        central = central_replay(rows, p0)
        interface, projected = make_projection(full_abi, package["group"], rows,
                                               targets, task198_meta)
        base_ref = base_reference(package, full_abi, g760)
        mutations = run_mutations(rows, p0, task198_meta, g760, projected,
                                  targets, base_ref, meter)
        areas = area_canary(t226, g760, rows, targets, meter)
        meter.bump("closure_runs", 1, "single projected closure")
        meter.bump("closure_actions", 1, "single projected closure")
        run = t227.closure(projected, meter, structural=None)
        internal_terminal = T227_MEMBER if run.get("member") else T227_NONMEMBER
        top_terminal = MEMBER_TOP if run.get("member") else NONMEMBER_TOP
        gate = t227.encode_gate(run)
        gate["terminal"] = internal_terminal
        gate["phase"] = "production"
        gate["resource"] = resource_canary("production")
        gate["boundary_membership"] = False
        gate["pointed_mu1"] = False
        gate["exact_pb_endpoint_zero"] = False
        gate["cofinal_lift"] = False
        gate["fake"] = False
        gate["Ihara_witness"] = False
        result = {
            "mode": "PRE_A0_COMPUTATIONAL_BASE_ONLY",
            "correction_word_constructed": False,
            "task192_consumed": False,
            "f_role": "BASE_REFERENCE_EQUAL_TO_G760",
            "g616": {"length": len(g616), "sha256": word_digest(g616)},
            "g760": {"word": g760, "length": len(g760),
                     "sha256": word_digest(g760), "exponent_sums": [0, 0]},
            "base_reference": base_ref,
            "projected_a3_interface": interface,
            "specialization_v216_abi": projected,
            "central_replay": central,
            "target_trace": target_trace,
            "area_canary": areas,
            "mutation_controls": {"attempted": p0["mutation_roster"],
                                   "rejected": mutations},
            "gate": gate,
            "task227_terminal": internal_terminal,
            "rank": run.get("rank"), "block_rank": run.get("block_rank"),
            "ideal_486_count": len(run.get("ideal_486", [])),
            "translate_729_count": len(run.get("translate_729", [])),
            "authority": {"pins": pins, "p0_sha256": P0_SHA256,
                          "p0_self_digest_sha256": p0["self_digest_sha256"],
                          "task198": task198_meta,
                          "task227_selftest": p0["authority"]["task227_selftest_acceptance"]},
            "false_conclusion_flags": {flag: False for flag in FALSE_FLAGS},
        }
        receipt = envelope(top_terminal, result, meter)
        write_fresh(output, receipt, meter)
        print("D359_PRODUCER_TERMINAL " + top_terminal, flush=True)
        return 0
    except ResourceStop as exc:
        result = {"phase": exc.phase, "cap": exc.cap, "value": exc.value,
                  "limit": exc.limit, "typed_unknown": UNKNOWN_RESOURCE}
        receipt = envelope(UNKNOWN_RESOURCE, result, meter)
        write_fresh(output, receipt, meter)
        print("D359_PRODUCER_TERMINAL " + UNKNOWN_RESOURCE, flush=True)
        return 0
    except (InputStop, FileNotFoundError, KeyError, ValueError,
            UnicodeError, json.JSONDecodeError, MemoryError) as exc:
        result = {"phase": "input-or-resource-authentication",
                  "reason": str(exc), "typed_unknown": UNKNOWN_INPUT}
        receipt = envelope(UNKNOWN_INPUT, result, meter)
        write_fresh(output, receipt, meter)
        print("D359_PRODUCER_TERMINAL " + UNKNOWN_INPUT, flush=True)
        return 0
    except RuntimeError as exc:
        if isinstance(exc, MutationAccepted):
            raise
        result = {"phase": "frozen-engine-rejection",
                  "reason": str(exc), "typed_unknown": UNKNOWN_INPUT}
        receipt = envelope(UNKNOWN_INPUT, result, meter)
        write_fresh(output, receipt, meter)
        print("D359_PRODUCER_TERMINAL " + UNKNOWN_INPUT, flush=True)
        return 0


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="ci/out/d972_r07_pre_a0_single_target_a3_v1.json")
    args = parser.parse_args(argv)
    safe_rel(args.output, "ci/out/")
    return production(args.output)


if __name__ == "__main__":
    raise SystemExit(main())
