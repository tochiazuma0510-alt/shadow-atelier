#!/usr/bin/env python3
"""Independent checker for the R07 pre-A0 projected A3 receipt.

Only the pinned crosscheck task226/task227 engines are imported here.  Word,
class-two, ledger, Fox, projection, and mutation ownership code is local to
this checker so a producer receipt cannot supply its construction path.
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
VERDICT_SCHEMA = SCHEMA + "/verdict/v1"
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
SOURCE_PINS = {
    "task226_checker": ("crosscheck/check_d972_r07_actual_two_word_endpoint_specializer_v2.py",
                         35463,
                         "e49e4ee24b56e35f8c8120bad7579865e497d94f57b2af51664d562f50ffaa44"),
    "task227_checker": ("crosscheck/check_d972_r07_typed_single_seed_endpoint_consumer_v2.py",
                         34200,
                         "028e615bd71276c22cea2180b8ff59e53d8e9ee745c84a1912c862f217f2bb95"),
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

    def check(self, phase):
        elapsed = time.monotonic() - self.started
        self.used["wall_seconds"] = elapsed
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
    require(p0.get("schema") == SCHEMA + "/prereg/v1", "P0 schema")
    require(p0.get("caps") == CAPS, "P0 caps")
    require(p0.get("terminal_vocabulary") ==
            [MEMBER_TOP, NONMEMBER_TOP, UNKNOWN_INPUT, UNKNOWN_RESOURCE],
            "P0 terminal vocabulary")
    require(p0.get("central_rows") == EXPECTED_CENTRAL, "P0 central rows")
    require(p0.get("mutation_roster") == [
        "task198_raw_manifest_binding", "task198_ledger_sign",
        "task198_prefix", "g760_letter_digest", "computational_base_mode",
        "forbidden_task192_binding", "H1_central_row", "H2_central_row",
        "P_central_row", "projected_area_target", "ABI_seal_target",
        "forbidden_conclusion_flag"], "P0 mutation roster")
    for flag in FALSE_FLAGS:
        require(p0.get("false_conclusion_flags", {}).get(flag) is False,
                "P0 false conclusion flag:" + flag)
    require(p0["authority"]["task303"] == {
        "bytes": 6739,
        "path": "sol/proof_r07_pre_a0_computational_base_equivalence_v303.md",
        "sha256": "9868aa26d630138da9b8b963b0f3968e8c2ee698ba4461d596a2b6f155d25cf2"},
            "P0 v303 pin")
    require(p0["authority"]["task227_selftest_acceptance"] == {
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
        require(rel not in pins or pins[rel] == (size, sha),
                "conflicting authority pin:" + rel)
        pins[rel] = (size, sha)
    raw_by_path = {}
    for rel, (size, sha) in sorted(pins.items()):
        raw_by_path[rel] = read_bytes(rel, size, sha, meter,
                                      "authority:" + rel)
    return pins, raw_by_path


def make_ledger():
    blocks = ["H1", "H1", "H1", "H2", "H2", "H2", "P1", "P2", "P3", "P5", "P4"]
    types = ["E3"] * 6 + ["E4"] * 5
    ten = [0, 1, 2, 3, 0, 4, 5, 6, 7, 8, 9]
    contexts = [21, 22, 23, 24, 21, 25, 1, 27, 21, 26, 28]
    roles = ["hexagon_fxy", "hexagon_fxz", "hexagon_fyz", "hexagon_fux",
             "hexagon_fxy", "hexagon_fuy", "pentagon_b1", "pentagon_b2",
             "pentagon_b3", "pentagon_b5_inverse_slot", "pentagon_b4_inverse_slot"]
    signs = [1, -1, 1, -1, -1, 1, 1, 1, 1, -1, -1]
    orientations = ["direct", "inverse", "direct", "inverse", "inverse",
                    "direct", "direct", "direct", "direct", "inverse", "inverse"]
    prefixes = [[3, 2], [3], [], [6, 5], [6], [], [11, 10, 9, 8],
                [11, 10, 9], [11, 10], [11], []]
    names = ["H1_fxy", "H1_fxz", "H1_fyz", "H2_fux", "H2_fxy", "H2_fuy",
             "P_b1", "P_b2", "P_b3", "P_b5_inverse", "P_b4_inverse"]
    out = []
    for i, block in enumerate(blocks):
        out.append({"ordinal": i + 1, "block": block,
                    "block_index": 1 if block == "H1" else 2 if block == "H2" else i - 3,
                    "block_slot": i % 3 + 1 if block in ("H1", "H2") else 1,
                    "occurrence": names[i], "type": types[i], "ten_index": ten[i],
                    "context_id": contexts[i], "role": roles[i],
                    "factor_sign": signs[i], "orientation": orientations[i],
                    "fox_prefix_occurrences": prefixes[i]})
    return out


def authenticate_task198(p0, raw_by_path):
    authority = p0["authority"]["task198"]
    receipt_path, manifest_path = authority["receipt"]["path"], authority["acceptance_manifest"]["path"]
    receipt_raw, manifest_raw = raw_by_path[receipt_path], raw_by_path[manifest_path]
    receipt, manifest = json.loads(receipt_raw), json.loads(manifest_raw)
    require(receipt_raw == canonical(receipt) and manifest_raw == canonical(manifest),
            "task198 noncanonical input")
    receipt_seal = strip_seal(receipt, "self_digest_sha256")
    manifest_seal = strip_seal(manifest, "manifest_self_digest_sha256")
    require(receipt_seal == authority["receipt"]["self_digest_sha256"] and
            manifest_seal == authority["acceptance_manifest"]["manifest_self_digest_sha256"],
            "task198 self seals")
    require(receipt.get("schema") == "d972-r07-seven-context-roof-presentation/v1" and
            receipt.get("status") == "COMPLETE" and receipt.get("terminal") == T198_TERMINAL,
            "task198 receipt terminal")
    require(len(receipt_raw) == authority["receipt"]["bytes"] and
            digest_bytes(receipt_raw) == authority["receipt"]["sha256"],
            "task198 receipt raw binding")
    require(manifest.get("schema") == "d972-r07-seven-context-roof-presentation/v1/acceptance-manifest/v3" and
            manifest.get("accepted") is True and manifest.get("independent") is True and
            manifest.get("synthetic") is False and
            manifest.get("task198_source_identities") == authority["source_identities"],
            "task198 manifest binding")
    require(manifest.get("receipt", {}).get("sha256") == authority["receipt"]["sha256"] and
            manifest.get("receipt", {}).get("bytes") == authority["receipt"]["bytes"] and
            manifest.get("receipt", {}).get("self_digest_sha256") == receipt_seal,
            "task198 manifest receipt")
    require(manifest.get("producer", {}).get("run") == authority["producer"]["run"] and
            manifest.get("checker", {}).get("run") == authority["checker"]["run"] and
            manifest.get("producer", {}).get("artifact_id") == authority["producer"]["artifact_id"] and
            manifest.get("checker", {}).get("artifact_id") == authority["checker"]["artifact_id"] and
            manifest.get("producer", {}).get("head") == authority["producer"]["head"] and
            manifest.get("checker", {}).get("head") == authority["checker"]["head"] and
            manifest.get("producer", {}).get("zip_sha256") == authority["producer"]["zip_sha256"] and
            manifest.get("checker", {}).get("zip_sha256") == authority["checker"]["zip_sha256"] and
            manifest.get("producer", {}).get("terminal_line_sha256") == authority["producer"]["terminal_line_sha256"] and
            manifest.get("checker", {}).get("terminal_line_sha256") == authority["checker"]["terminal_line_sha256"],
            "task198 run/artifact binding")
    verdict_path = authority["checker_verdict"]["path"]
    verdict_raw, verdict = raw_by_path[verdict_path], json.loads(raw_by_path[verdict_path])
    require(verdict_raw == canonical(verdict) and len(verdict_raw) == authority["checker_verdict"]["bytes"] and
            digest_bytes(verdict_raw) == authority["checker_verdict"]["sha256"] and verdict == {
                "accepted": True, "independent": True,
                "receipt_terminal": T198_TERMINAL,
                "schema": "d972-r07-seven-context-roof-presentation/v1/crosscheck/v2"},
            "task198 checker verdict")
    producer_att = raw_by_path[authority["producer_attestation"]["path"]]
    checker_att = raw_by_path[authority["checker_attestation"]["path"]]
    require(digest_bytes(producer_att) == authority["producer_attestation"]["sha256"] and
            producer_att.decode("ascii") ==
            "R07_SEVEN_CONTEXT_ROOF_PRESENTATION_V1_PRODUCER_TERMINAL ROOF_BRIDGE_ISOMORPHISM\n" and
            digest_bytes(checker_att) == authority["checker_attestation"]["sha256"] and
            checker_att.decode("ascii") ==
            "R07_SEVEN_CONTEXT_ROOF_PRESENTATION_V1_CHECKER_PASS terminal=ROOF_BRIDGE_ISOMORPHISM rows=6441\n",
            "task198 attestations")
    rows = receipt.get("bridge", {}).get("occurrence_ledger")
    require(rows == make_ledger() and receipt["bridge"].get("ten_to_eleven") ==
            [0, 1, 2, 3, 0, 4, 5, 6, 7, 8, 9], "task198 ledger")
    require("section_cocycle" in receipt.get("evaluator", {}).get("entry_points", {}),
            "task198 evaluator ABI")
    require(digest_obj(rows) == receipt["bridge"].get("occurrence_ledger_sha256"),
            "task198 ledger digest")
    return rows, {"receipt_path": receipt_path, "receipt_bytes": len(receipt_raw),
                  "receipt_sha256": digest_bytes(receipt_raw),
                  "manifest_path": manifest_path, "manifest_bytes": len(manifest_raw),
                  "manifest_sha256": digest_bytes(manifest_raw),
                  "receipt_self_digest_sha256": receipt_seal,
                  "manifest_self_digest_sha256": manifest_seal}


def red(word):
    out = []
    for letter in word:
        require(type(letter) is int and letter != 0 and abs(letter) <= 6, "word letter")
        if out and out[-1] == -letter:
            out.pop()
        else:
            out.append(letter)
    return out


def winv(word):
    return [-letter for letter in reversed(word)]


def pp(left, right):
    return red(list(right) + list(left))


def commword(left, right):
    return red(winv(left) + winv(right) + list(left) + list(right))


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


def mul(left, right, degree):
    central = 1 if degree == 3 else 4
    na, za, nb, zb = left[:degree], left[degree:], right[:degree], right[degree:]
    z = [(za[i] + zb[i]) % 9 for i in range(central)]
    for i in range(degree):
        for j in range(i + 1, degree):
            q = bracket(i, j, degree)
            for k in range(central):
                z[k] = (z[k] - na[j] * nb[i] * q[k]) % 9
    return tuple((na[i] + nb[i]) % 9 for i in range(degree)) + tuple(z)


def inv(value, degree):
    central = 1 if degree == 3 else 4
    z = [(-x) % 9 for x in value[degree:]]
    for i in range(degree):
        for j in range(i + 1, degree):
            q = bracket(i, j, degree)
            for k in range(central):
                z[k] = (z[k] - value[i] * value[j] * q[k]) % 9
    return tuple((-x) % 9 for x in value[:degree]) + tuple(z)


def power(value, exponent, degree):
    out = (0,) * (degree + (1 if degree == 3 else 4))
    for _ in range(exponent % 9):
        out = mul(out, value, degree)
    return out


def eval_word(word, degree):
    width = degree + (1 if degree == 3 else 4)
    out = (0,) * width
    for letter in word:
        generator = [0] * width
        generator[abs(letter) - 1] = 1
        value = tuple(generator)
        out = mul(out, value if letter > 0 else inv(value, degree), degree)
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
            current = mul(current, generator, degree)
        else:
            current = mul(current, inv(generator, degree), degree)
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
        right = mul(key, generator, degree)
        out[right] = (out.get(right, 0) + coefficient) % 3
        out[key] = (out.get(key, 0) - coefficient) % 3
    return {key: coefficient for key, coefficient in out.items() if coefficient}


def jsg(value):
    return [{"key": list(key), "coefficient": coefficient}
            for key, coefficient in sorted(value.items())]


def literal_substitutions():
    x, y = [1], [3]
    z, u = winv(pp(x, y)), winv(pp(y, x))
    return {"PB3": {"x": x, "y": y, "z": z, "u": u,
                     "H1": [(x, y, 1), (x, z, -1), (y, z, 1)],
                     "H2": [(u, x, -1), (x, y, -1), (u, y, 1)]},
            "PB4": {"generators": [[1], [2], [3], [4], [5], [6]],
                    "b_display": [([4], [6], 1),
                                  (pp([1], [2]), pp([5], [6]), 1),
                                  ([1], [4], 1), (pp([2], [4]), [6], -1),
                                  ([1], pp([4], [5]), -1)]}}


def factor_data():
    sub = literal_substitutions()
    factors = sub["PB3"]["H1"] + sub["PB3"]["H2"] + sub["PB4"]["b_display"]
    return [(left, right) for left, right, _ in factors], [sign for _, _, sign in factors]


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


def target_from_fox(g760, rows, abi):
    pairs, signs = factor_data()
    raw_words = [red(subst(g760, left, right)) for left, right in pairs]
    signed_words = [word if signs[i] == 1 else winv(word)
                    for i, word in enumerate(raw_words)]
    targets, relations = {}, []
    for lo, hi, block, degree in ((0, 3, "H1", 3), (3, 6, "H2", 3),
                                  (6, 11, "P", 6)):
        relation = red([letter for index in reversed(range(lo, hi))
                        for letter in signed_words[index]])
        relations.append(relation)
        target = endpoint_block(tag(block, sparse_scale(fox(relation, degree), -1)),
                                block, degree)
        targets[block] = jsg(target)
        one = (0,) * (degree + (1 if degree == 3 else 4))
        require(target == sparse_add({one: 1}, {eval_word(relation, degree): -1}),
                "Fox endpoint identity:" + block)
    require(abi.get("bar_epsilon_1") == targets and
            abi.get("literals", {}).get("relation_words_g") == relations,
            "base target 1-R_B(g760)")
    return targets, {"relation_words_g": relations, "raw_rwords_g": raw_words,
                     "signed_rwords_g": signed_words}


def central_replay(rows, p0):
    pairs, _ = factor_data()
    expected = p0["central_rows"]
    products = {"H1": (0, 0, 0, 0), "H2": (0, 0, 0, 0), "P": (0,) * 10}
    sums = {"H1": [0], "H2": [0], "P": [0, 0, 0, 0]}
    records = []
    for index, row in enumerate(rows):
        degree = 3 if index < 6 else 6
        qx, qy = eval_word(pairs[index][0], degree), eval_word(pairs[index][1], degree)
        comm = mul(mul(mul(inv(qx, degree), inv(qy, degree), degree), qx, degree), qy, degree)
        z0 = power(comm, 3, degree)
        require(all(x == 0 for x in z0[:degree]), "central noncentral component")
        signed = tuple((row["factor_sign"] * x) % 9 for x in z0[degree:])
        block = "H1" if index < 3 else "H2" if index < 6 else "P"
        product_before = products[block]
        products[block] = mul(products[block], tuple([0] * degree + list(signed)), degree)
        sums[block] = [(a + b) % 9 for a, b in zip(sums[block], signed)]
        records.append({"ordinal": row["ordinal"], "block": block,
                        "factor_sign": row["factor_sign"], "q_o_x": list(qx),
                        "q_o_y": list(qy), "q_o_z0": list(z0),
                        "signed_central": list(signed),
                        "product_before": list(product_before),
                        "sum_after": list(sums[block]),
                        "product_after": list(products[block])})
    for block in ("H1", "H2", "P"):
        got_rows = [r["signed_central"] for r in records if r["block"] == block]
        require(got_rows == expected[block]["rows"] and sums[block] == expected[block]["sum"],
                "central rows/sum:" + block)
        require(list(products[block][3 if block != "P" else 6:]) == expected[block]["sum"] and
                products[block] == (0,) * len(products[block]), "central product:" + block)
    return {"rows": records, "blocks": {
        block: {"signed_rows": expected[block]["rows"], "sum": sums[block],
                "product": list(products[block])}
        for block in ("H1", "H2", "P")},
        "identity_checks": {block: products[block] == (0,) * len(products[block])
                             for block in ("H1", "H2", "P")}}


def make_projection(full_abi, package_rows, rows, targets, task198_meta):
    occurrences = full_abi["occurrences"]
    occurrence_rows = [{"ordinal": item["ordinal"], "p_o": item["p_o"],
                        "xi_o": item["xi_o"], "w_o": item["w_o"],
                        "u0_o": item["u0"]} for item in occurrences]
    quotient = {"modulus": 9, "q3_width": 4, "q4_width": 10,
                "actor_width": 3, "actor_convention": full_abi["actor_convention"],
                "PB3_brackets": package_rows.get("PB3_brackets"),
                "PB4_brackets": package_rows.get("PB4_brackets"),
                "marked_D1_action": "p_o conjugation followed by z0 action",
                "ten_to_eleven": full_abi["ten_to_eleven"]}
    body = {"schema": SCHEMA + "/projected-a3-interface/v1",
            "mode": "PRE_A0_COMPUTATIONAL_BASE_ONLY",
            "correction_word_constructed": False, "task192_consumed": False,
            "f_role": "BASE_REFERENCE_EQUAL_TO_G760",
            "authenticated_ledger": {"rows": rows, "sha256": digest_obj(rows),
                                      "task198_receipt_sha256": task198_meta["receipt_sha256"],
                                      "task198_manifest_sha256": task198_meta["manifest_sha256"]},
            "quotient_action_abi": quotient, "occurrence_rows": occurrence_rows,
            "combined_w": [{"ordinal": item["ordinal"], "terms": item["w_o"]}
                            for item in occurrences],
            "combined_u0": [{"ordinal": item["ordinal"], "terms": item["u0"]}
                             for item in occurrences],
            "target_blocks": targets, "target_role": "ONE_MINUS_R_B_G760",
            "projection_only": True,
            "full_package_fields_excluded": ["f", "rword_f", "B_a", "PB_chain_fields"]}
    body["canonical_digest_sha256"] = digest_obj(body)
    projected = copy.deepcopy(full_abi)
    projected.update({"projection_schema": body["schema"],
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
                      "f_role": "BASE_REFERENCE_EQUAL_TO_G760"})
    projected["self_digest_sha256"] = digest_obj(projected)
    return body, projected


def validate_base_reference(result, abi, g760):
    ref = result.get("base_reference", {})
    require(ref.get("mode") == "PRE_A0_COMPUTATIONAL_BASE_ONLY" and
            ref.get("correction_word_constructed") is False and
            ref.get("task192_consumed") is False and
            ref.get("f_role") == "BASE_REFERENCE_EQUAL_TO_G760" and
            ref.get("transfer_evidence") is False and
            ref.get("f_equals_g760") is True and ref.get("B_a_zero") is True,
            "base reference typing")
    fields = ref.get("full_package_fields", {})
    require(abi.get("literals_role") == "BASE_REFERENCE_ONLY" and
            abi.get("base_reference_field_types") == {
                "f": "BASE_REFERENCE_ONLY", "rword_f": "BASE_REFERENCE_ONLY",
                "B_a": "BASE_REFERENCE_ONLY", "PB_chain_fields": "BASE_REFERENCE_ONLY"},
            "base ABI field type map")
    for name in ("f", "a", "rword_f", "B_a", "PB_chain_fields"):
        require(fields.get(name, {}).get("type") == "BASE_REFERENCE_ONLY" and
                fields.get(name, {}).get("transfer_evidence") is False,
                "base reference field typing:" + name)
    require(fields["f"]["value"] == g760 and fields["a"]["value"] == [] and
            fields["rword_f"]["value"] == abi["literals"]["rword_f"] and
            fields["B_a"]["value"] == abi["literals"]["B_a"],
            "base reference field values")


def area_canary(engine, g760, rows, targets, meter):
    zword = red(commword([1], [2]) * 3)
    output = []
    for exponent in (0, 1, 2):
        representative = red(list(g760) + zword * exponent)
        abi = engine.reconstruct(representative, [], rows)
        require(abi["bar_epsilon_1"] == targets, "projected area target")
        meter.bump("area_builds", 1, "projected area representative")
        output.append({"t": exponent, "word_length": len(representative),
                       "word_sha256": word_digest(representative),
                       "bar_epsilon_1": abi["bar_epsilon_1"],
                       "label": "PROJECTED_AREA_REPRESENTATIVE_ONLY"})
    return {"zword": zword, "zword_sha256": word_digest(zword), "rows": output,
            "all_equal_base_target": True,
            "label": "PROJECTED_AREA_REPRESENTATIVE_ONLY"}


def mutation_fixture(rows, p0, task198_meta, g760, projected, targets, base_ref):
    return {"raw_manifest_binding": {"receipt_sha256": task198_meta["receipt_sha256"],
                                      "manifest_sha256": task198_meta["manifest_sha256"]},
            "ledger": copy.deepcopy(rows), "g760": list(g760),
            "base": copy.deepcopy(base_ref), "central": copy.deepcopy(p0["central_rows"]),
            "area_target": copy.deepcopy(targets), "abi": copy.deepcopy(projected),
            "flags": {flag: False for flag in FALSE_FLAGS}}


def cheap_validate(name, value, reference):
    if name == "task198_raw_manifest_binding" and value["raw_manifest_binding"] != reference["raw_manifest_binding"]:
        raise NarrowReject("task198 raw/manifest binding")
    if name in ("task198_ledger_sign", "task198_prefix") and value["ledger"] != reference["ledger"]:
        raise NarrowReject("task198 ledger " + name.rsplit("_", 1)[-1])
    if name == "g760_letter_digest" and word_digest(value["g760"]) != EXPECTED_G760_SHA256:
        raise NarrowReject("g760 digest")
    if name == "computational_base_mode" and value["base"]["mode"] != "PRE_A0_COMPUTATIONAL_BASE_ONLY":
        raise NarrowReject("computational-base mode")
    if name == "forbidden_task192_binding" and value["base"]["task192_consumed"] is not False:
        raise NarrowReject("task192 binding")
    if name in ("H1_central_row", "H2_central_row", "P_central_row") and value["central"] != reference["central"]:
        raise NarrowReject(name)
    if name == "projected_area_target" and value["area_target"] != reference["area_target"]:
        raise NarrowReject("projected area target")
    if name == "ABI_seal_target":
        abi = value["abi"]
        if abi.get("self_digest_sha256") != digest_obj({k: v for k, v in abi.items() if k != "self_digest_sha256"}):
            raise NarrowReject("ABI seal/target")
    if name == "forbidden_conclusion_flag" and any(value["flags"].get(flag) is not False for flag in FALSE_FLAGS):
        raise NarrowReject("forbidden conclusion flag")


def run_mutations(rows, p0, task198_meta, g760, projected, targets, base_ref, meter):
    roster = p0["mutation_roster"]
    reference = mutation_fixture(rows, p0, task198_meta, g760, projected, targets, base_ref)
    records = []
    for name in roster:
        mutant = copy.deepcopy(reference)
        if name == "task198_raw_manifest_binding": mutant["raw_manifest_binding"]["manifest_sha256"] = "0" * 64; owner = "raw_manifest_binding"
        elif name == "task198_ledger_sign": mutant["ledger"][0]["factor_sign"] *= -1; owner = "ledger"
        elif name == "task198_prefix": mutant["ledger"][0]["fox_prefix_occurrences"] = [2, 3]; owner = "ledger"
        elif name == "g760_letter_digest": mutant["g760"][0] *= -1; owner = "g760"
        elif name == "computational_base_mode": mutant["base"]["mode"] = "MUTATED_FORBIDDEN_MODE"; owner = "base"
        elif name == "forbidden_task192_binding": mutant["base"]["task192_consumed"] = True; owner = "base"
        elif name == "H1_central_row": mutant["central"]["H1"]["rows"][0][0] = 3; owner = "central"
        elif name == "H2_central_row": mutant["central"]["H2"]["rows"][0][0] = 6; owner = "central"
        elif name == "P_central_row": mutant["central"]["P"]["rows"][0][3] = 3; owner = "central"
        elif name == "projected_area_target": mutant["area_target"]["H1"] = []; owner = "area_target"
        elif name == "ABI_seal_target": mutant["abi"]["self_digest_sha256"] = "0" * 64; owner = "abi"
        elif name == "forbidden_conclusion_flag": mutant["flags"]["fake"] = True; owner = "flags"
        else: raise InputStop("unregistered mutation:" + name)
        before, after = digest_obj(reference[owner]), digest_obj(mutant[owner])
        require(before != after, "mutation owner unchanged:" + name)
        meter.bump("mutation_work", 1, "cheap mutation:" + name)
        try:
            cheap_validate(name, mutant, reference)
        except NarrowReject as exc:
            reason = str(exc)
            records.append({"name": name, "changed_field": owner,
                            "expected_gate": reason, "observed_reason": reason,
                            "before_sha256": before, "after_sha256": after,
                            "first_gate": reason, "rejected": True})
        else:
            raise MutationAccepted("accepted mutation:" + name)
    require([record["name"] for record in records] == roster and
            all(record["rejected"] for record in records), "cheap mutation matrix")
    return records


def load_engine(rel, size, sha, tag_name, meter):
    raw = read_bytes(rel, size, sha, meter, "import:" + tag_name)
    path = ROOT / safe_rel(rel)
    spec = importlib.util.spec_from_file_location("_d359_checker_" + tag_name, path)
    require(spec is not None and spec.loader is not None, "import specification:" + tag_name)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    meter.bump("dynamic_imports", 1, "dynamic import:" + tag_name)
    require(digest_bytes(raw) == sha, "post-import source drift:" + tag_name)
    return module


def read_receipt(path_text, meter):
    path = safe_rel(path_text, "ci/out/")
    raw = (ROOT / path).read_bytes()
    meter.bump("input_bytes", len(raw), "receipt input")
    try:
        value = json.loads(raw)
    except (ValueError, UnicodeError) as exc:
        raise InputStop("receipt JSON:" + str(exc))
    require(raw == canonical(value), "receipt noncanonical bytes")
    strip_seal(value, "self_digest_sha256")
    require(value.get("schema") == RECEIPT_SCHEMA, "receipt schema")
    return path.as_posix(), raw, value


def flags_false(value):
    return all(value.get(flag) is False for flag in
               ("boundary_membership", "pointed_mu1", "exact_pb_endpoint_zero",
                "cofinal_lift", "fake", "Ihara_witness"))


def write_verdict(path_text, value, meter):
    path = safe_rel(path_text, "ci/out/")
    path = ROOT / path
    require(not path.exists(), "stale verdict refused")
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = canonical(value)
    meter.bump("serialized_bytes", len(payload), "verdict serialization")
    with path.open("xb") as handle:
        handle.write(payload)


def verdict(value, receipt_path, receipt_raw, terminal, accepted, independent,
            p0, projected=None, central=None, gate=None, mutations=None,
            meter=None, reason=None):
    result = {"schema": VERDICT_SCHEMA, "terminal": terminal,
              "accepted": accepted, "independent": independent,
              "receipt_path": receipt_path, "receipt_bytes": len(receipt_raw),
              "receipt_sha256": digest_bytes(receipt_raw),
              "p0_path": P0_PATH, "p0_bytes": P0_BYTES,
              "p0_sha256": P0_SHA256,
              "p0_self_digest_sha256": p0.get("self_digest_sha256"),
              "source_identities": {rel: {"bytes": size, "sha256": sha}
                                    for rel, (size, sha) in sorted(
                                        authority_pins(p0).items())},
              "reconstructed_abi_sha256": digest_obj(projected) if projected is not None else None,
              "central_replay_sha256": digest_obj(central) if central is not None else None,
              "occurrence_rank": gate.get("rank") if gate else None,
              "block_rank": gate.get("block_rank") if gate else None,
              "task227_terminal": gate.get("terminal") if gate else None,
              "independent_result_sha256": digest_obj({"abi": projected, "central": central,
                                                        "gate": gate}) if gate is not None else None,
              "mutation_matrix_sha256": digest_obj(mutations) if mutations is not None else None,
              "reason": reason,
              "resource_meter": meter.snapshot() if meter is not None else None}
    result["self_digest_sha256"] = digest_obj(result)
    return result


def authority_pins(p0):
    pins = {}
    for rel, size, sha in iter_pins(p0["authority"]):
        require(rel not in pins or pins[rel] == (size, sha),
                "conflicting authority pin:" + rel)
        pins[rel] = (size, sha)
    return pins


def check_certificate(receipt_path, receipt_raw, receipt, p0, pins, rows,
                      task198_meta, meter):
    terminal = receipt.get("terminal")
    require(flags_false(receipt), "receipt forbidden conclusion flag")
    if terminal in (UNKNOWN_INPUT, UNKNOWN_RESOURCE):
        require(type(receipt.get("result")) is dict and
                receipt["result"].get("typed_unknown") == terminal,
                "typed unknown receipt")
        return terminal, None, None, None, None, None, task198_meta
    require(terminal in (MEMBER_TOP, NONMEMBER_TOP), "receipt terminal vocabulary")
    g616, g760 = construct_g760()
    t226 = load_engine("crosscheck/check_d972_r07_actual_two_word_endpoint_specializer_v2.py",
                       35463,
                       "e49e4ee24b56e35f8c8120bad7579865e497d94f57b2af51664d562f50ffaa44",
                       "task226", meter)
    t227 = load_engine("crosscheck/check_d972_r07_typed_single_seed_endpoint_consumer_v2.py",
                       34200,
                       "028e615bd71276c22cea2180b8ff59e53d8e9ee745c84a1912c862f217f2bb95",
                       "task227", meter)
    full_abi = t226.reconstruct(g760, [], rows)
    require(full_abi.get("ledger") == rows and full_abi.get("occurrence_ledger_sha256") == digest_obj(rows),
            "checker base ABI ledger")
    targets, trace = target_from_fox(g760, rows, full_abi)
    central = central_replay(rows, p0)
    # The independent engine exposes the same package data, but this checker
    # supplies the package group tables explicitly to the v303 projection.
    package_group = {"PB3_brackets": [[[0, 1], [1]], [[0, 2], [-1]], [[1, 2], [1]]],
                     "PB4_brackets": [[[0, 1], [1, 0, 0, 0]], [[0, 3], [-1, 0, 0, 0]],
                                       [[1, 3], [1, 0, 0, 0]], [[0, 2], [0, 1, 0, 0]],
                                       [[0, 4], [0, -1, 0, 0]], [[2, 4], [0, 1, 0, 0]],
                                       [[1, 2], [0, 0, 1, 0]], [[1, 5], [0, 0, -1, 0]],
                                       [[2, 5], [0, 0, 1, 0]], [[3, 4], [0, 0, 0, 1]],
                                       [[3, 5], [0, 0, 0, -1]], [[4, 5], [0, 0, 0, 1]]]}
    interface, projected = make_projection(full_abi, package_group, rows, targets, task198_meta)
    result = receipt.get("result")
    require(type(result) is dict and result.get("mode") == "PRE_A0_COMPUTATIONAL_BASE_ONLY" and
            result.get("correction_word_constructed") is False and
            result.get("task192_consumed") is False and
            result.get("f_role") == "BASE_REFERENCE_EQUAL_TO_G760",
            "receipt computational base typing")
    require(result.get("projected_a3_interface") == interface and
            result.get("specialization_v216_abi") == projected and
            digest_obj(result.get("projected_a3_interface")) == digest_obj(interface),
            "receipt projected interface binding")
    validate_base_reference(result, full_abi, g760)
    require(result.get("g616") == {"length": len(g616), "sha256": word_digest(g616)} and
            result.get("g760", {}).get("word") == g760 and
            result.get("g760", {}).get("length") == 760 and
            result.get("g760", {}).get("sha256") == word_digest(g760) and
            result.get("g760", {}).get("exponent_sums") == [0, 0],
            "receipt g760 binding")
    require(result.get("central_replay") == central and result.get("target_trace") == trace,
            "receipt central/target replay binding")
    areas = area_canary(t226, g760, rows, targets, meter)
    require(result.get("area_canary") == areas, "receipt area canary")
    base_ref = result.get("base_reference")
    mutations = run_mutations(rows, p0, task198_meta, g760, projected, targets,
                              base_ref, meter)
    require(result.get("mutation_controls", {}).get("attempted") == p0["mutation_roster"] and
            result.get("mutation_controls", {}).get("rejected") == mutations,
            "receipt mutation controls")
    gate = result.get("gate")
    internal = T227_MEMBER if terminal == MEMBER_TOP else T227_NONMEMBER
    require(result.get("task227_terminal") == internal and type(gate) is dict,
            "receipt task227 terminal")
    meter.check("independent task227 verifier before")
    require(t227.verify_gate(gate, projected, internal, "production") is True,
            "independent task227 verifier")
    meter.check("independent task227 verifier after")
    require(gate.get("terminal") == internal and
            gate.get("rank") == result.get("rank") and
            gate.get("block_rank") == result.get("block_rank") and
            gate.get("ideal_486") and len(gate["ideal_486"]) == 486 and
            gate.get("translate_729") and len(gate["translate_729"]) == 729,
            "gate roster preservation")
    require(receipt.get("resource_meter", {}).get("caps") == CAPS,
            "receipt resource caps")
    return terminal, projected, central, gate, mutations, areas, task198_meta


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("receipt")
    parser.add_argument("--verdict", required=True)
    args = parser.parse_args(argv)
    meter = Meter()
    receipt_path = safe_rel(args.receipt, "ci/out/").as_posix()
    receipt_raw = b""
    p0 = {"self_digest_sha256": None, "authority": {}}
    try:
        p0 = load_p0(meter)
        pins, raws = authenticate_authority(p0, meter)
        receipt_path, receipt_raw, receipt = read_receipt(args.receipt, meter)
        rows, task198_meta = authenticate_task198(p0, raws)
        raws.clear()  # release the single 31-MB accepted receipt byte copy
        terminal, projected, central, gate, mutations, areas, task198_meta = check_certificate(
            receipt_path, receipt_raw, receipt, p0, pins, rows, task198_meta, meter)
        output = verdict(receipt, receipt_path, receipt_raw, terminal,
                         terminal in (MEMBER_TOP, NONMEMBER_TOP),
                         terminal in (MEMBER_TOP, NONMEMBER_TOP), p0,
                         projected, central, gate, mutations, meter)
        write_verdict(args.verdict, output, meter)
        print("D359_CHECKER_TERMINAL " + terminal, flush=True)
        return 0
    except ResourceStop as exc:
        output = verdict({}, receipt_path, receipt_raw, UNKNOWN_RESOURCE, False,
                         False, p0, meter=meter, reason={"phase": exc.phase,
                         "cap": exc.cap, "value": exc.value, "limit": exc.limit})
        write_verdict(args.verdict, output, meter)
        print("D359_CHECKER_TERMINAL " + UNKNOWN_RESOURCE, flush=True)
        return 0
    except (InputStop, FileNotFoundError, KeyError, ValueError,
            UnicodeError, json.JSONDecodeError, MemoryError) as exc:
        output = verdict({}, receipt_path, receipt_raw, UNKNOWN_INPUT, False,
                         False, p0, meter=meter, reason=str(exc))
        write_verdict(args.verdict, output, meter)
        print("D359_CHECKER_TERMINAL " + UNKNOWN_INPUT, flush=True)
        return 0
    except RuntimeError as exc:
        if isinstance(exc, MutationAccepted):
            raise
        output = verdict({}, receipt_path, receipt_raw, UNKNOWN_INPUT, False,
                         False, p0, meter=meter,
                         reason="frozen-engine-rejection:" + str(exc))
        write_verdict(args.verdict, output, meter)
        print("D359_CHECKER_TERMINAL " + UNKNOWN_INPUT, flush=True)
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
