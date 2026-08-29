#!/usr/bin/env python3
"""Task384/v5 independent checker for the R07 pre-A0 projected A3 receipt.

Only the pinned crosscheck task226/task227 engines are imported here.  Word,
class-two, ledger, Fox, projection, and mutation ownership code is local to
this checker so a producer receipt cannot supply its construction path.
"""
from __future__ import annotations

import argparse
import copy
import ctypes
import errno
import hashlib
import importlib.util
import json
import os
import signal
import stat
import sys
import time
from pathlib import Path
from types import MappingProxyType

try:
    import resource
except ImportError:  # pragma: no cover - Windows runner
    resource = None

ROOT = Path(__file__).resolve().parents[1]
P0_PATH = "ci/in/d972_r07_pre_a0_single_target_a3_v4.prereg.v1.json"
P0_BYTES = 16417
P0_SHA256 = "14ea6de8efac73e71854f6566a9202eb89164ab6b7b5940954e87b3af21ee8ae"
P0_SELF_SHA256 = "f1991fa0c232e1d7ea95a211498b4d1741c2104b22271fb90ec1a7ee3af98be7"
SCHEMA = "d972-r07-pre-a0-single-target-a3/v4"
RECEIPT_SCHEMA = "d972-r07-pre-a0-single-target-a3/v5/receipt/v1"
VERDICT_SCHEMA = "d972-r07-pre-a0-single-target-a3/v5/verdict/v1"
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
    "authority_bytes": 40000000, "base_abi_builds": 1,
    "block_rank_increases": 486, "block_rows": 100000,
    "checker_roster": 729, "closure_runs": 1, "dual_work": 1000000,
    "dynamic_imports": 7, "evaluator_builds": 1,
    "evaluator_calls": 64, "evaluator_operations": 1000000,
    "evaluator_support": 11,
    "independent_verify_calls": 1, "input_bytes": 60000000,
    "mutation_work": 100,
    "occurrence_rank_increases": 486,
    "orbit_actions": 2000000, "rss_bytes": 4294967296,
    "serialization_peak_bytes": 57327680,
    "serialized_bytes": 20000000, "wall_seconds": 1800,
}
NORMAL_OUTPUT_MAX = 1_000_000
EMERGENCY_OUTPUT_MAX = 65_536
PRODUCER_RECEIPT_MAX = 19_000_000
CANONICAL_CHUNK = 65_536
BASE_BUILD_RESERVE = 1
AREA_BUILD_RESERVE = 1
CONSUMER_MARKER = "V303_OMITTED_NOT_CONSUMED"
ACTOR_CONVENTION = (
    "x^a y^b h^r; [x,y]=x^-1 y^-1 x y=(0,0,1), product "
    "r+r'-b*a', inverse (-a,-b,-r-a*b) mod 9, z0=(0,0,3)"
)
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
    "e4_arithmetic": ("search/d972_b345_seedspan_triple4_v1.py", 535219,
                       "fe18fc31fdf3f9416ebb829112ccbd514c27e6a8d30fe24691842865277a0b29"),
    "e4_arithmetic_checker": ("search/check_d972_b345_seedspan_triple4_v1.py",
                               574347,
                               "ef5125e3b7e328ce8aa8cfd4c36d0937e28f44a480188fcd4ed01a37eb80b981"),
    "joint_checker": ("search/check_d972_b345_joint_kernel_qstar_closure_v1.py",
                      47661,
                      "9e721634d1f16be806e315eec263ec272bc023587f862703c094b7dd37c0111f"),
    "task176_producer": ("search/d972_r07_all_seven_extension_section_census_v1.py",
                         66109,
                         "878cf1d8d44e74a993309ed1c613c9fc57eb62fd2da48a30fd8797ff4b19af3b"),
    "task198_checker": ("crosscheck/check_d972_r07_seven_context_roof_presentation_v1.py",
                        157253,
                        "001277d44dbbc2acd7e03c6ecb6c6419df84996ae188cbb4be7b18f7cfb56ca1"),
    "task226_checker": ("crosscheck/check_d972_r07_actual_two_word_endpoint_specializer_v2.py",
                         35463,
                         "e49e4ee24b56e35f8c8120bad7579865e497d94f57b2af51664d562f50ffaa44"),
    "task227_checker": ("crosscheck/check_d972_r07_typed_single_seed_endpoint_consumer_v2.py",
                         34200,
                         "028e615bd71276c22cea2180b8ff59e53d8e9ee745c84a1912c862f217f2bb95"),
}
PRODUCER_RESOURCE_FORMULAS = {
    "authority": {"formula": "16417+33121619", "bytes": 33138036,
                  "cap": 40000000, "owner_count": 23},
    "input": {"formula": "16417+33121619+2*894133",
              "bytes": 34926302, "cap": 60000000,
              "authenticated_source_import_bytes": 894133,
              "loader_extra_physical_reads": 0},
    "output": {"receipt_max_bytes": 19000000,
               "serialized_cap": CAPS["serialized_bytes"]},
    "allocation": {
        "formula": "3*19000000+65536",
        "normal_serialization_peak_bound_bytes": 57065536,
        "normal_plus_emergency_charged_bound_bytes": 57327680,
        "rlimit_as_bytes": CAPS["rss_bytes"]},
    "wall": {"internal_seconds": 1800, "external_each_seconds": 2100,
             "serial_external_seconds": 4200,
             "workflow_seconds": 21600,
             "inequalities": "1800<2100;2*2100=4200<21600"},
    "task227_frozen_dependency": {
        "internal_span_comparison_calls": 12,
        "wrapper_reversed_span_calls": 0},
}
CHECKER_RESOURCE_FORMULAS = {
    "authority": {"formula": "16417+33121619", "bytes": 33138036,
                  "cap": 40000000, "owner_count": 23},
    "input_before_receipt": {
        "formula": "16417+33121619+2*1450252",
        "bytes": 36038540, "cap": 60000000,
        "authenticated_source_import_bytes": 1450252,
        "loader_extra_physical_reads": 0},
    "input_with_max_receipt": {
        "formula": "36038540+19000000", "bytes": 55038540,
        "cap": 60000000},
    "output": {"verdict_max_bytes": NORMAL_OUTPUT_MAX,
               "serialized_cap": CAPS["serialized_bytes"]},
    "allocation": {"q0_private_bytes": 7348320,
                   "q0_private_construction_peak_bytes": 14696640,
                   "verdict_serialization_peak_bound_bytes": 3065536,
                   "rlimit_as_bytes": CAPS["rss_bytes"]},
    "wall": {"internal_seconds": 1800, "external_each_seconds": 2100,
             "serial_external_seconds": 4200,
             "workflow_seconds": 21600,
             "inequalities": "1800<2100;2*2100=4200<21600"},
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


class StaleOutput(InputStop):
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
        self.reserved = {key: 0 for key in self.caps}
        self.rss_samples = []
        self.hard_limit = None
        self.reserve("serialized_bytes", EMERGENCY_OUTPUT_MAX,
                     "emergency output reserve")

    def elapsed(self):
        return time.monotonic() - self.started

    def check(self, phase):
        elapsed = self.elapsed()
        self.used["wall_seconds"] = elapsed
        if elapsed > self.caps["wall_seconds"]:
            raise ResourceStop(phase, "wall_seconds", elapsed,
                               self.caps["wall_seconds"])

    def reserve(self, key, amount, phase):
        if key not in self.caps or type(amount) is not int or amount < 0:
            raise InputStop("invalid resource reservation:" + key)
        wanted = self.used[key] + self.reserved[key] + amount
        if wanted > self.caps[key]:
            raise ResourceStop(phase, key, wanted, self.caps[key])
        self.reserved[key] += amount
        self.check(phase)

    def consume(self, key, reserved_amount, actual_amount, phase):
        if (key not in self.caps or type(reserved_amount) is not int or
                type(actual_amount) is not int or actual_amount < 0 or
                reserved_amount < actual_amount or
                self.reserved[key] < reserved_amount):
            raise InputStop("invalid reserved resource consumption:" + key)
        self.reserved[key] -= reserved_amount
        self.used[key] += actual_amount
        if self.used[key] > self.caps[key]:
            raise ResourceStop(phase, key, self.used[key], self.caps[key])
        self.check(phase)

    def release(self, key, amount):
        if (key not in self.caps or type(amount) is not int or amount < 0 or
                self.reserved[key] < amount):
            raise InputStop("invalid resource release:" + key)
        self.reserved[key] -= amount

    def bump(self, key, amount, phase):
        if key not in self.caps:
            raise InputStop("unregistered resource counter:" + key)
        self.reserve(key, amount, phase)
        self.consume(key, amount, amount, phase)

    def sample_rss(self, phase):
        require(resource is not None, "Linux resource API unavailable")
        rss = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1024)
        self.rss_samples.append({"phase": phase, "peak_rss_bytes": rss})
        self.used["rss_bytes"] = max(self.used["rss_bytes"], rss)
        if rss > self.caps["rss_bytes"]:
            raise ResourceStop(phase, "rss_bytes", rss,
                               self.caps["rss_bytes"])
        self.check(phase)
        return rss

    def public(self, serialized_override=None, wall_override=None):
        used = dict(self.used)
        used["wall_seconds"] = (self.elapsed() if wall_override is None
                                else wall_override)
        if serialized_override is not None:
            used["serialized_bytes"] = serialized_override
        return {"caps": dict(self.caps), "used": used,
                "rss_samples": list(self.rss_samples),
                "rss_sampling_is_not_an_in_call_interrupt": True,
                "hard_address_space": copy.deepcopy(self.hard_limit),
                "opaque_task227_verifier_calls":
                    self.used["independent_verify_calls"]}


class WallDeadline:
    def __init__(self, meter, phase):
        self.meter = meter
        self.phase = phase
        self.old_handler = None
        self.old_timer = None
        self.entered = None

    def _expired(self, _signum, _frame):
        raise ResourceStop(self.phase, "wall_seconds", self.meter.elapsed(),
                           self.meter.caps["wall_seconds"])

    def __enter__(self):
        self.meter.check(self.phase + ":before")
        remaining = self.meter.caps["wall_seconds"] - self.meter.elapsed()
        if remaining <= 0:
            raise ResourceStop(self.phase, "wall_seconds", self.meter.elapsed(),
                               self.meter.caps["wall_seconds"])
        self.old_handler = signal.getsignal(signal.SIGALRM)
        self.old_timer = signal.getitimer(signal.ITIMER_REAL)
        self.entered = time.monotonic()
        armed = remaining
        if self.old_timer[0] > 0.0:
            armed = min(armed, self.old_timer[0])
        signal.signal(signal.SIGALRM, self._expired)
        signal.setitimer(signal.ITIMER_REAL, armed)
        return self

    def __exit__(self, exc_type, exc, tb):
        signal.setitimer(signal.ITIMER_REAL, 0.0)
        signal.signal(signal.SIGALRM, self.old_handler)
        if self.old_timer != (0.0, 0.0):
            restored = self.old_timer[0] - (time.monotonic() - self.entered)
            if restored <= 0.0:
                raise ResourceStop(self.phase + ":prior timer expired",
                                   "wall_seconds", self.meter.elapsed(),
                                   self.meter.caps["wall_seconds"])
            signal.setitimer(signal.ITIMER_REAL, restored, self.old_timer[1])
        return False


def install_linux_hard_limits(meter):
    require(sys.platform.startswith("linux") and resource is not None,
            "required Linux hard-cap APIs unavailable")
    for name in ("RLIMIT_AS", "getrlimit", "setrlimit"):
        require(hasattr(resource, name), "required Linux RLIMIT_AS unavailable")
    for name in ("setitimer", "getitimer", "ITIMER_REAL", "SIGALRM"):
        require(hasattr(signal, name), "required Linux wall timer unavailable")
    libc = ctypes.CDLL(None, use_errno=True)
    require(hasattr(libc, "renameat2"),
            "required Linux renameat2 no-overwrite API unavailable")
    _soft, hard = resource.getrlimit(resource.RLIMIT_AS)
    target = meter.caps["rss_bytes"]
    if hard != resource.RLIM_INFINITY:
        target = min(target, hard)
    require(type(target) is int and target > 0,
            "invalid RLIMIT_AS hard ceiling")
    resource.setrlimit(resource.RLIMIT_AS, (target, target))
    installed_soft, installed_hard = resource.getrlimit(resource.RLIMIT_AS)
    require(installed_soft == target and installed_hard == target,
            "RLIMIT_AS hard ceiling readback")
    meter.hard_limit = {"api": "resource.RLIMIT_AS", "hard_bytes": target,
                        "requested_bytes": meter.caps["rss_bytes"]}
    meter.sample_rss("hard limits installed")


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
    require(type(expected_bytes) is int and expected_bytes >= 0 and
            type(expected_sha) is str and len(expected_sha) == 64 and
            all(character in "0123456789abcdef" for character in expected_sha),
            phase + ":pin shape")
    path = safe_rel(rel)
    absolute = ROOT / path
    try:
        info = absolute.lstat()
    except OSError as exc:
        raise InputStop(phase + ":stat:" + str(exc))
    require(stat.S_ISREG(info.st_mode) and not absolute.is_symlink(),
            phase + ":regular file")
    require(info.st_size == expected_bytes, phase + ":stat byte length")
    meter.reserve("input_bytes", expected_bytes, phase + ":read reserve")
    if authority:
        meter.reserve("authority_bytes", expected_bytes,
                      phase + ":authority reserve")
    try:
        raw = absolute.read_bytes()
    except OSError as exc:
        meter.release("input_bytes", expected_bytes)
        if authority:
            meter.release("authority_bytes", expected_bytes)
        raise InputStop(phase + ":read:" + str(exc))
    meter.consume("input_bytes", expected_bytes, len(raw), phase)
    if authority:
        meter.consume("authority_bytes", expected_bytes, len(raw), phase)
    require(len(raw) == expected_bytes, phase + ":byte length")
    require(digest_bytes(raw) == expected_sha, phase + ":SHA-256")
    return raw


def iter_canonical_chunks(value):
    encoder = json.JSONEncoder(sort_keys=True, separators=(",", ":"),
                               ensure_ascii=True, allow_nan=False)
    for piece in encoder.iterencode(value):
        for offset in range(0, len(piece), CANONICAL_CHUNK):
            yield piece[offset:offset + CANONICAL_CHUNK].encode("ascii")


def streaming_canonical(value, expected_raw=None):
    position = 0
    hasher = hashlib.sha256()
    view = memoryview(expected_raw) if expected_raw is not None else None
    for chunk in iter_canonical_chunks(value):
        end = position + len(chunk)
        if view is not None and bytes(view[position:end]) != chunk:
            raise InputStop("streaming canonical byte mismatch")
        hasher.update(chunk)
        position = end
    if view is not None and position != len(view):
        raise InputStop("streaming canonical byte length mismatch")
    if view is not None:
        view.release()
    return position, hasher.hexdigest()


def streaming_seal(value, field, expected, label):
    require(type(value) is dict and type(value.get(field)) is str,
            label + ":missing seal")
    body = dict(value)
    claimed = body.pop(field)
    _, actual = streaming_canonical(body)
    require(claimed == expected and actual == expected,
            label + ":self seal binding")
    return claimed


def strip_seal(value, field):
    require(type(value) is dict and type(value.get(field)) is str,
            "missing " + field)
    body = dict(value)
    claimed = body.pop(field)
    require(claimed == digest_obj(body), field + " mismatch")
    return claimed


def collect_authority_pins(p0):
    records = []

    def walk(value):
        if isinstance(value, dict):
            if "path" in value:
                require(type(value.get("path")) is str and
                        type(value.get("bytes")) is int and
                        value["bytes"] >= 0 and
                        type(value.get("sha256")) is str and
                        len(value["sha256"]) == 64 and
                        all(c in "0123456789abcdef"
                            for c in value["sha256"]),
                        "malformed ordinary authority owner")
                rel = safe_rel(value["path"]).as_posix()
                require(rel == value["path"], "authority owner path alias")
                records.append((rel, value["bytes"], value["sha256"]))
                return
            for child in value.values():
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)

    walk(p0["authority"])
    paths = [record[0] for record in records]
    inventory = p0["authority_inventory"]
    require(len(paths) == len(set(paths)), "duplicate authority owner path")
    require(sorted(paths) == inventory["owner_paths"] and
            len(records) == inventory["unique_owner_count"] and
            sum(record[1] for record in records) ==
                inventory["unique_owner_bytes"],
            "authority owner inventory missing/extra/count/bytes")
    require(P0_PATH not in paths and
            not any(path.endswith("single_target_a3_v5.py") or
                    path.endswith("single_target_a3_gha_driver_v5.g")
                    for path in paths),
            "authority graph cycle")
    return records


def load_p0(meter):
    require(len(P0_SHA256) == 64 and len(P0_SELF_SHA256) == 64,
            "P0 pin length")
    raw = read_bytes(P0_PATH, P0_BYTES, P0_SHA256, meter, "P0")
    try:
        p0 = json.loads(raw)
    except (ValueError, UnicodeError) as exc:
        raise InputStop("P0 JSON:" + str(exc))
    require(raw == canonical(p0), "P0 noncanonical bytes")
    require(strip_seal(p0, "self_digest_sha256") == P0_SELF_SHA256,
            "P0 self seal pin")
    require(p0.get("schema") == SCHEMA + "/prereg/v1", "P0 schema")
    require(p0.get("caps") == CAPS, "P0 caps")
    require(p0.get("terminal_vocabulary") ==
            [MEMBER_TOP, NONMEMBER_TOP, UNKNOWN_INPUT, UNKNOWN_RESOURCE],
            "P0 terminal vocabulary")
    require(p0.get("central_rows") == EXPECTED_CENTRAL, "P0 central rows")
    require(digest_obj(p0["authority"]["task198"]["evaluator_contract"]) ==
            p0["authority"]["task198"]["evaluator_contract_sha256"] ==
            "4fc38881ffee293f0820d3639230dd44a2af9b9ed126dfb21dc5831290ff08b8",
            "P0 evaluator contract digest")
    require(p0["consumer_abi"]["compatibility_presence_only_fields"] ==
            {"rword_f": CONSUMER_MARKER, "rword_g": CONSUMER_MARKER},
            "P0 consumer compatibility markers")
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
    ancestry = p0["authority"]["g760_ancestry"]
    require(type(ancestry) is list and len(ancestry) == 2 and
            {item["path"] for item in ancestry} == {
                "search/d972_r07_760_l3_target6_v1.py",
                "search/check_d972_r07_616_to_760_commutator_affine_rhs_v3.py"},
            "P0 complete g760 ancestry owners")
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
    records = collect_authority_pins(p0)
    pins = {rel: (size, sha) for rel, size, sha in records}
    for rel, size, sha in SOURCE_PINS.values():
        require(pins.get(rel) == (size, sha),
                "source pin absent from P0 authority:" + rel)
    retained = {
        p0["authority"]["task198"][name]["path"]
        for name in ("receipt", "acceptance_manifest", "producer_attestation",
                     "checker_attestation", "checker_verdict")
    }
    retained.add(p0["authority"]["task198_evaluator_support"]
                 ["q3_receipt"]["path"])
    raw_by_path = {}
    for rel, (size, sha) in sorted(pins.items()):
        raw = read_bytes(rel, size, sha, meter, "authority:" + rel)
        if rel in retained:
            raw_by_path[rel] = raw
        else:
            del raw
    meter.sample_rss("authority physical pins")
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


def _without_path(value):
    return {key: copy.deepcopy(item) for key, item in value.items()
            if key != "path"}


def _roof_value(value, widths):
    return (type(value) is list and len(value) == len(widths) and
            all(type(item) is str and len(item) == 2 * width and
                all(character in "0123456789abcdef" for character in item)
                for item, width in zip(value, widths)))


def _validate_evaluator_canaries(canaries, widths):
    expected = {"nonsplit_y_y_section_cocycle", "source_2_2", "x", "y",
                "x_inverse", "xy", "xy_section_cocycle", "x_action_y"}
    require(type(canaries) is dict and set(canaries) == expected and
            canaries["nonsplit_y_y_section_cocycle"] is None,
            "task198 evaluator canary roster")
    for name, word in (("x", [1]), ("y", [2]), ("x_inverse", [-1]),
                       ("xy", [1, 2])):
        item = canaries[name]
        require(type(item) is dict and set(item) == {"word", "value"} and
                item["word"] == word and _roof_value(item["value"], widths),
                "task198 evaluator canary:" + name)
    source = canaries["source_2_2"]
    require(type(source) is dict and set(source) == {
        "gamma_state_id", "gamma_word", "q0_state_id", "q0_word",
        "source_word", "value"} and source["gamma_state_id"] == 2 and
        source["q0_state_id"] == 2 and source["q0_word"] == [1] and
        all(type(word) is list and all(type(letter) is int and letter != 0
            for letter in word) for word in
            (source["gamma_word"], source["source_word"])) and
        _roof_value(source["value"], widths),
        "task198 evaluator source-section canary")
    action = canaries["x_action_y"]
    require(type(action) is dict and set(action) ==
            {"actor_word", "input", "value"} and
            action["actor_word"] == [1] and
            _roof_value(action["input"], widths) and
            _roof_value(action["value"], widths),
            "task198 evaluator action canary")
    cocycle = canaries["xy_section_cocycle"]
    require(type(cocycle) is dict and set(cocycle) ==
            {"left", "right", "product", "value"} and
            cocycle["left"] == [1] and cocycle["right"] == [2] and
            cocycle["product"] == [1, 2] and
            _roof_value(cocycle["value"], widths),
            "task198 evaluator cocycle canary")


def freeze_snapshot(value):
    """Recursively freeze a compact checker-authenticated JSON value."""
    if type(value) is dict:
        return MappingProxyType({key: freeze_snapshot(value[key])
                                 for key in sorted(value)})
    if type(value) is list:
        return tuple(freeze_snapshot(item) for item in value)
    return value


def thaw_snapshot(value):
    if isinstance(value, MappingProxyType):
        return {key: thaw_snapshot(item) for key, item in value.items()}
    if type(value) is tuple:
        return [thaw_snapshot(item) for item in value]
    return value


def validate_task198_binding_snapshot(p0, raw_by_path, snapshot):
    """Checker-local ordinary validator for the real small binding owners."""
    frozen = thaw_snapshot(snapshot)
    authority = p0["authority"]["task198"]
    manifest_owner = frozen["manifest_owner"]
    manifest_raw = raw_by_path[manifest_owner["path"]]
    try:
        manifest = json.loads(manifest_raw)
    except (ValueError, UnicodeError) as exc:
        raise InputStop("task198 manifest JSON:" + str(exc))
    streaming_canonical(manifest, manifest_raw)
    require(set(manifest) == {"accepted", "accepted_receipt_basename",
            "checker", "checker_attestation", "checker_verdict",
            "independent", "manifest_self_digest_sha256", "producer",
            "producer_attestation", "receipt", "schema", "synthetic",
            "task198_source_identities"} and manifest["accepted"] is True and
            manifest["independent"] is True and manifest["synthetic"] is False and
            manifest["schema"] ==
            "d972-r07-seven-context-roof-presentation/v1/acceptance-manifest/v3",
            "task198 acceptance manifest")
    require(manifest["receipt"] == frozen["receipt_manifest_binding"],
            "task198 raw/manifest binding")
    manifest_seal = streaming_seal(
        manifest, "manifest_self_digest_sha256",
        manifest_owner["manifest_self_digest_sha256"], "task198 manifest")
    require(len(manifest_raw) == manifest_owner["bytes"] and
            digest_bytes(manifest_raw) == manifest_owner["sha256"] and
            manifest_seal == manifest_owner["manifest_self_digest_sha256"],
            "task198 manifest raw binding")
    expected_contract = frozen["manifest_contract"]
    require(authority["manifest_contract"] == expected_contract and
            all(manifest[key] == value for key, value in
                expected_contract.items()),
            "task198 complete member/attestation/verdict manifest binding")
    member = frozen["member"]
    require(Path(frozen["receipt_path"]).name ==
            frozen["accepted_receipt_basename"] and
            manifest["producer"]["member"] == member and
            manifest["checker"]["member"] == member and
            manifest["producer"]["terminal_line_sha256"] ==
                frozen["producer_attestation"]["owner"]["sha256"] and
            manifest["checker"]["terminal_line_sha256"] ==
                frozen["checker_attestation"]["owner"]["sha256"],
            "task198 receipt/member/attestation cross-links")
    require(manifest["task198_source_identities"] ==
            frozen["source_identities"], "task198 source identity binding")
    acceptance = frozen["acceptance"]
    require(p0["authority"]["task198_acceptance"] == acceptance and
            acceptance == {
                "checker_terminal": T198_TERMINAL,
                "head": manifest["checker"]["head"],
                "producer_terminal": T198_TERMINAL,
                "run": manifest["producer"]["run"],
                "zip_sha256": manifest["producer"]["zip_sha256"]} and
            manifest["producer"]["run"] == manifest["checker"]["run"] and
            manifest["producer"]["head"] == manifest["checker"]["head"] and
            manifest["producer"]["artifact_id"] ==
                manifest["checker"]["artifact_id"] and
            manifest["producer"]["zip_sha256"] ==
                manifest["checker"]["zip_sha256"],
            "task198 run/head/artifact/zip links")
    verdict_snapshot = frozen["checker_verdict"]
    verdict_owner = verdict_snapshot["owner"]
    verdict_raw = raw_by_path[verdict_owner["path"]]
    verdict = json.loads(verdict_raw)
    streaming_canonical(verdict, verdict_raw)
    require(Path(verdict_owner["path"]).name == verdict_owner["basename"] and
            len(verdict_raw) == verdict_owner["bytes"] and
            digest_bytes(verdict_raw) == verdict_owner["sha256"] and
            verdict == verdict_snapshot["content"],
            "task198 checker verdict complete metadata")
    for key in ("producer_attestation", "checker_attestation"):
        attestation = frozen[key]
        owner = attestation["owner"]
        raw = raw_by_path[owner["path"]]
        require(Path(owner["path"]).name == owner["basename"] and
                len(raw) == owner["bytes"] and
                digest_bytes(raw) == owner["sha256"] and
                raw.decode("ascii") == attestation["text"],
                "task198 " + key.replace("_", " ") +
                " complete metadata")
    return True


def authenticate_task198(p0, pins, raw_by_path):
    authority = p0["authority"]["task198"]
    receipt_path = authority["receipt"]["path"]
    manifest_path = authority["acceptance_manifest"]["path"]
    receipt_raw = raw_by_path[receipt_path]
    manifest_raw = raw_by_path[manifest_path]
    try:
        receipt = json.loads(receipt_raw)
        manifest = json.loads(manifest_raw)
    except (ValueError, UnicodeError) as exc:
        raise InputStop("task198 JSON:" + str(exc))
    streaming_canonical(receipt, receipt_raw)
    streaming_canonical(manifest, manifest_raw)
    receipt_seal = streaming_seal(
        receipt, "self_digest_sha256",
        authority["receipt"]["self_digest_sha256"], "task198 receipt")
    manifest_seal = streaming_seal(
        manifest, "manifest_self_digest_sha256",
        authority["acceptance_manifest"]["manifest_self_digest_sha256"],
        "task198 manifest")
    require(receipt.get("schema") ==
            "d972-r07-seven-context-roof-presentation/v1" and
            receipt.get("status") == "COMPLETE" and
            receipt.get("terminal") == T198_TERMINAL,
            "task198 receipt terminal")
    require(len(receipt_raw) == authority["receipt"]["bytes"] and
            pins[receipt_path] == (authority["receipt"]["bytes"],
                                   authority["receipt"]["sha256"]),
            "task198 receipt raw binding")
    require(set(manifest) == {"accepted", "accepted_receipt_basename",
            "checker", "checker_attestation", "checker_verdict",
            "independent", "manifest_self_digest_sha256", "producer",
            "producer_attestation", "receipt", "schema", "synthetic",
            "task198_source_identities"} and manifest["accepted"] is True and
            manifest["independent"] is True and manifest["synthetic"] is False and
            manifest["schema"] ==
            "d972-r07-seven-context-roof-presentation/v1/acceptance-manifest/v3",
            "task198 acceptance manifest")
    expected_manifest_contract = {
        "accepted_receipt_basename": authority["accepted_receipt_basename"],
        "checker": authority["checker"],
        "checker_attestation": _without_path(authority["checker_attestation"]),
        "checker_verdict": _without_path(authority["checker_verdict"]),
        "producer": authority["producer"],
        "producer_attestation": _without_path(authority["producer_attestation"]),
    }
    require(authority["manifest_contract"] == expected_manifest_contract and
            all(manifest[key] == value for key, value in
                expected_manifest_contract.items()),
            "task198 complete member/attestation/verdict manifest binding")
    expected_member = {
        "basename": authority["accepted_receipt_basename"],
        "bytes": authority["receipt"]["bytes"],
        "sha256": authority["receipt"]["sha256"],
    }
    require(Path(receipt_path).name == authority["accepted_receipt_basename"] and
            manifest["producer"]["member"] == expected_member and
            manifest["checker"]["member"] == expected_member and
            manifest["producer"]["terminal_line_sha256"] ==
                authority["producer_attestation"]["sha256"] and
            manifest["checker"]["terminal_line_sha256"] ==
                authority["checker_attestation"]["sha256"],
            "task198 receipt/member/attestation cross-links")
    raw_manifest_binding = manifest["receipt"] == {
        "basename": authority["accepted_receipt_basename"],
        "bytes": authority["receipt"]["bytes"],
        "self_digest_sha256": receipt_seal,
        "sha256": authority["receipt"]["sha256"]}
    require(manifest["task198_source_identities"] ==
            authority["source_identities"],
            "task198 source identity binding")
    acceptance = p0["authority"]["task198_acceptance"]
    require(acceptance == {
        "checker_terminal": T198_TERMINAL,
        "head": manifest["checker"]["head"],
        "producer_terminal": T198_TERMINAL,
        "run": manifest["producer"]["run"],
        "zip_sha256": manifest["producer"]["zip_sha256"]} and
        manifest["producer"]["run"] == manifest["checker"]["run"] and
        manifest["producer"]["head"] == manifest["checker"]["head"] and
        manifest["producer"]["artifact_id"] == manifest["checker"]["artifact_id"] and
        manifest["producer"]["zip_sha256"] == manifest["checker"]["zip_sha256"],
            "task198 run/head/artifact/zip links")
    verdict_raw = raw_by_path[authority["checker_verdict"]["path"]]
    verdict = json.loads(verdict_raw)
    streaming_canonical(verdict, verdict_raw)
    expected_verdict = {key: authority["checker_verdict"][key] for key in
                        ("accepted", "independent", "receipt_terminal", "schema")}
    require(Path(authority["checker_verdict"]["path"]).name ==
            authority["checker_verdict"]["basename"] and
            len(verdict_raw) == authority["checker_verdict"]["bytes"] and
            digest_bytes(verdict_raw) == authority["checker_verdict"]["sha256"] and
            verdict == expected_verdict and verdict["accepted"] is True and
            verdict["independent"] is True and verdict["receipt_terminal"] ==
            T198_TERMINAL, "task198 checker verdict complete metadata")
    producer_att = raw_by_path[authority["producer_attestation"]["path"]]
    checker_att = raw_by_path[authority["checker_attestation"]["path"]]
    require(Path(authority["producer_attestation"]["path"]).name ==
            authority["producer_attestation"]["basename"] and
            len(producer_att) == authority["producer_attestation"]["bytes"] and
            digest_bytes(producer_att) == authority["producer_attestation"]["sha256"] and
            producer_att.decode("ascii") ==
            "R07_SEVEN_CONTEXT_ROOF_PRESENTATION_V1_PRODUCER_TERMINAL ROOF_BRIDGE_ISOMORPHISM\n",
            "task198 producer attestation complete metadata")
    require(Path(authority["checker_attestation"]["path"]).name ==
            authority["checker_attestation"]["basename"] and
            len(checker_att) == authority["checker_attestation"]["bytes"] and
            digest_bytes(checker_att) == authority["checker_attestation"]["sha256"] and
            checker_att.decode("ascii") ==
            "R07_SEVEN_CONTEXT_ROOF_PRESENTATION_V1_CHECKER_PASS terminal=ROOF_BRIDGE_ISOMORPHISM rows=6441\n",
            "task198 checker attestation complete metadata")
    bridge = receipt.get("bridge", {})
    rows = bridge.get("occurrence_ledger")
    expected_evaluator = authority["evaluator_contract"]
    require(rows == make_ledger() == expected_evaluator["occurrence_ledger"],
            "task198 literal eleven-row ledger")
    require(bridge.get("ten_to_eleven") ==
            [0, 1, 2, 3, 0, 4, 5, 6, 7, 8, 9] and
            digest_obj(rows) == bridge.get("occurrence_ledger_sha256") ==
            "040ab853535db8aad06fba295adf8b59bb1cd77435e7c64a1edcc34cdacb4cd7",
            "task198 insertion/ledger digest")
    evaluator = receipt.get("evaluator")
    require(type(evaluator) is dict and set(evaluator) == {
        "canaries", "context_maps", "coordinate_ledger_sha256",
        "coordinate_widths", "encoding", "entry_points",
        "joint_coordinate_image", "module", "registry_callable",
        "relator_rows_sha256", "runtime_constructor", "schema", "semantics"},
        "task198 evaluator exact keyset")
    evaluator_core = dict(evaluator)
    canaries = evaluator_core.pop("canaries")
    require(evaluator_core.pop("context_maps") is None and
            evaluator_core.pop("joint_coordinate_image") is None,
            "task198 evaluator production-null maps")
    expected_core = dict(expected_evaluator)
    expected_core.pop("occurrence_ledger")
    require(evaluator_core == expected_core and
            digest_obj(expected_evaluator) == authority["evaluator_contract_sha256"],
            "task198 complete evaluator ABI")
    _validate_evaluator_canaries(canaries, expected_evaluator["coordinate_widths"])
    require(raw_manifest_binding, "task198 raw/manifest binding")
    rows_out = copy.deepcopy(rows)
    evaluator_out = copy.deepcopy(expected_evaluator)
    meta = {"receipt_path": receipt_path, "receipt_bytes": len(receipt_raw),
            "receipt_sha256": pins[receipt_path][1],
            "manifest_path": manifest_path, "manifest_bytes": len(manifest_raw),
            "manifest_sha256": pins[manifest_path][1],
            "receipt_self_digest_sha256": receipt_seal,
            "manifest_self_digest_sha256": manifest_seal,
            "accepted_receipt_basename": authority["accepted_receipt_basename"],
            "manifest_contract": copy.deepcopy(expected_manifest_contract),
            "evaluator_contract_sha256": authority["evaluator_contract_sha256"],
            "evaluator_canaries_sha256": digest_obj(canaries),
            "evaluator_canaries": copy.deepcopy(canaries)}
    expected_verdict = {key: authority["checker_verdict"][key] for key in
                        ("accepted", "independent", "receipt_terminal",
                         "schema")}
    snapshot = freeze_snapshot({
        "receipt_path": receipt_path,
        "accepted_receipt_basename": authority["accepted_receipt_basename"],
        "receipt_manifest_binding": {
            "basename": authority["accepted_receipt_basename"],
            "bytes": authority["receipt"]["bytes"],
            "self_digest_sha256": receipt_seal,
            "sha256": pins[receipt_path][1]},
        "manifest_owner": {
            "path": manifest_path,
            "bytes": authority["acceptance_manifest"]["bytes"],
            "sha256": pins[manifest_path][1],
            "manifest_self_digest_sha256": manifest_seal},
        "manifest_contract": copy.deepcopy(expected_manifest_contract),
        "member": expected_member,
        "producer_attestation": {
            "owner": copy.deepcopy(authority["producer_attestation"]),
            "text":
                "R07_SEVEN_CONTEXT_ROOF_PRESENTATION_V1_PRODUCER_TERMINAL ROOF_BRIDGE_ISOMORPHISM\n"},
        "checker_attestation": {
            "owner": copy.deepcopy(authority["checker_attestation"]),
            "text":
                "R07_SEVEN_CONTEXT_ROOF_PRESENTATION_V1_CHECKER_PASS terminal=ROOF_BRIDGE_ISOMORPHISM rows=6441\n"},
        "checker_verdict": {
            "owner": copy.deepcopy(authority["checker_verdict"]),
            "content": expected_verdict},
        "source_identities": copy.deepcopy(authority["source_identities"]),
        "acceptance": copy.deepcopy(acceptance),
        "decoded_result": {
            "occurrence_ledger": rows_out,
            "evaluator_contract": evaluator_out,
            "evaluator_canaries": copy.deepcopy(canaries)},
    })
    require(validate_task198_binding_snapshot(
        p0, raw_by_path, snapshot) is True,
        "task198 authenticated binding snapshot")
    decoded = thaw_snapshot(snapshot)["decoded_result"]
    del receipt, manifest, verdict, evaluator, evaluator_core, canaries
    return (decoded["occurrence_ledger"], decoded["evaluator_contract"], meta,
            snapshot)


def run_raw_authority_mutation(p0, raw_by_path, snapshot, meter):
    """Mutate one real small owner and re-enter its ordinary validator."""
    name = "task198_raw_manifest_binding"
    manifest_owner = p0["authority"]["task198"]["acceptance_manifest"]
    path = manifest_owner["path"]
    manifest = json.loads(raw_by_path[path])
    before = digest_bytes(raw_by_path[path])
    manifest["receipt"]["sha256"] = "0" * 64
    body = dict(manifest)
    body.pop("manifest_self_digest_sha256")
    manifest["manifest_self_digest_sha256"] = digest_obj(body)
    mutant_raw = canonical(manifest)
    mutant_raws = dict(raw_by_path)
    mutant_raws[path] = mutant_raw
    after = digest_bytes(mutant_raw)
    require(before != after, "mutation owner unchanged:" + name)
    meter.bump("mutation_work", 1,
               "checker ordinary authority mutation:" + name)
    observed = None
    try:
        validate_task198_binding_snapshot(p0, mutant_raws, snapshot)
    except InputStop as exc:
        if str(exc) == "task198 raw/manifest binding":
            observed = str(exc)
        else:
            raise
    if observed is None:
        raise MutationAccepted("accepted mutation:" + name)
    expected = p0["mutation_expected_reasons"][name]
    require(observed == expected, "mutation wrong first reason:" + name)
    return {"name": name, "changed_field": "task198_manifest_raw_owner",
            "expected_gate": expected, "observed_reason": observed,
            "before_sha256": before, "after_sha256": after,
            "first_gate": observed, "ordinary_validator":
                "validate_task198_binding_snapshot", "rejected": True}


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


def base_checks(abi, rows, g760):
    require(type(abi) is dict and type(abi.get("self_digest_sha256")) is str,
            "base ABI seal presence")
    streaming_seal(abi, "self_digest_sha256", abi["self_digest_sha256"],
                   "task226 independent BASE_REFERENCE_ONLY ABI")
    require(abi.get("ledger") == rows and abi.get("ten_to_eleven") ==
            [0, 1, 2, 3, 0, 4, 5, 6, 7, 8, 9] and
            abi.get("actor_convention") == ACTOR_CONVENTION,
            "checker base ledger/actor typing")
    literals = abi.get("literals", {})
    require(literals.get("rword_f") == literals.get("rword_g") and
            literals.get("relation_factors_f") ==
                literals.get("relation_factors_g") and
            literals.get("relation_words_f") == literals.get("relation_words_g") and
            all(literals.get("B_a", {}).get(block) == []
                for block in ("H1", "H2", "P")),
            "checker empty-correction full base typing")
    require(len(abi.get("occurrences", [])) == 11 and
            all(item.get("rword_f") == item.get("rword_g") and
                item.get("r_f") == item.get("r_g")
                for item in abi["occurrences"]),
            "checker base occurrence rword typing")
    return abi


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


INTERFACE_OCCURRENCE_FIELDS = {
    "ordinal", "block", "block_index", "block_slot", "occurrence", "type",
    "ten_index", "context_id", "role", "factor_sign", "orientation",
    "fox_prefix_occurrences", "combined_block", "q_degree", "key_width",
    "p_o", "q_o(x)", "q_o(y)", "xi_o", "w_o", "translated", "u0",
    "ancestry",
}


def seal_fresh(value, label):
    require(type(value) is dict, label + ":object")
    value.pop("self_digest_sha256", None)
    _, seal = streaming_canonical(value)
    value["self_digest_sha256"] = seal
    streaming_seal(value, "self_digest_sha256", seal, label)
    return seal


def contains_forbidden_key(value, forbidden):
    if isinstance(value, dict):
        return any(key in forbidden or contains_forbidden_key(child, forbidden)
                   for key, child in value.items())
    if isinstance(value, list):
        return any(contains_forbidden_key(child, forbidden) for child in value)
    return False


def quotient_codec():
    return {
        "actor": {"coordinates": ["a", "b", "r"], "modulus": 9,
                  "width": 3, "convention": ACTOR_CONVENTION},
        "field": {"coefficient_encoding": [1, 2], "name": "F3",
                  "zero_terms_omitted": True},
        "q3": {"degree_one_width": 3, "central_width": 1,
               "key_width": 4,
               "brackets": [[list(key), list(value)]
                            for key, value in PB3_BRACKETS.items()]},
        "q4": {"degree_one_width": 6, "central_width": 4,
               "key_width": 10,
               "brackets": [[list(key), list(value)]
                            for key, value in PB4_BRACKETS.items()]},
        "sparse_coordinate_encoding":
            "canonical list of {key:[0..8]^width,coefficient:1|2}",
        "orbit_action": "left multiplication by p_o*q_o(actor)*p_o^-1",
    }


def _consumer_body(interface, p0):
    marker = p0["consumer_abi"]["compatibility_presence_only_fields"]
    occurrences = []
    for item in interface["occurrences"]:
        row = {key: copy.deepcopy(item[key])
               for key in p0["consumer_abi"]["occurrence_fields"]}
        row["rword_g"] = marker["rword_g"]
        row["rword_f"] = marker["rword_f"]
        occurrences.append(row)
    return {"schema": p0["consumer_abi"]["schema"],
            "modulus": interface["modulus"],
            "occurrences": occurrences,
            "bar_epsilon_1": copy.deepcopy(interface["target_blocks"]),
            "u0": copy.deepcopy(interface["combined_u0"]),
            "ten_to_eleven": copy.deepcopy(interface["ten_to_eleven"])}


def validate_projection(interface, consumer, p0):
    forbidden = {"literals", "rword_f", "B_a", "exact_PB_chain_fields",
                 "task192_ancestry"}
    require(interface.get("schema") ==
            SCHEMA + "/projected_a3_interface_v2" and
            interface.get("projection_mode") ==
            "V303_PRE_A0_COMPUTATIONAL_BASE_PROJECTION" and
            interface.get("mode") == "PRE_A0_COMPUTATIONAL_BASE_ONLY" and
            interface.get("task192_consumed") is False and
            interface.get("correction_word_constructed") is False and
            not contains_forbidden_key(interface, forbidden),
            "checker projected interface allowlist")
    require(len(interface.get("occurrences", [])) == 11 and
            all(set(item) == INTERFACE_OCCURRENCE_FIELDS
                for item in interface["occurrences"]),
            "checker projected interface occurrence allowlist")
    streaming_seal(interface, "self_digest_sha256",
                   interface.get("self_digest_sha256"),
                   "checker projected interface baseline")
    expected_body = _consumer_body(interface, p0)
    streaming_seal(consumer, "self_digest_sha256",
                   consumer.get("self_digest_sha256"),
                   "checker task227 consumer ABI baseline")
    actual_body = dict(consumer)
    actual_body.pop("self_digest_sha256")
    require(actual_body == expected_body and
            set(actual_body) == set(p0["projection_allowlist"]) and
            all(set(item) == set(p0["consumer_abi"]["occurrence_fields"]) |
                {"rword_g", "rword_f"} for item in consumer["occurrences"]),
            "checker task227 consumer ABI derived only from projection")
    return True


def make_projection(full_abi, rows, targets, task198_meta, evaluator_trace, p0):
    occurrences = []
    for row, item in zip(rows, full_abi["occurrences"]):
        projected = {key: copy.deepcopy(row[key]) for key in row}
        for key in ("combined_block", "q_degree", "key_width", "p_o",
                    "q_o(x)", "q_o(y)", "xi_o", "w_o", "translated",
                    "u0", "ancestry"):
            projected[key] = copy.deepcopy(item[key])
        require(set(projected) == INTERFACE_OCCURRENCE_FIELDS,
                "checker projected occurrence field roster")
        occurrences.append(projected)
    interface = {
        "schema": SCHEMA + "/projected_a3_interface_v2",
        "projection_mode": "V303_PRE_A0_COMPUTATIONAL_BASE_PROJECTION",
        "mode": "PRE_A0_COMPUTATIONAL_BASE_ONLY",
        "correction_word_constructed": False, "task192_consumed": False,
        "f_role": "BASE_REFERENCE_EQUAL_TO_G760", "projection_only": True,
        "modulus": 9,
        "ten_to_eleven": copy.deepcopy(full_abi["ten_to_eleven"]),
        "authenticated_ledger": {
            "rows": copy.deepcopy(rows), "sha256": digest_obj(rows),
            "task198_receipt_sha256": task198_meta["receipt_sha256"],
            "task198_manifest_sha256": task198_meta["manifest_sha256"],
            "task198_evaluator_contract_sha256":
                task198_meta["evaluator_contract_sha256"],
            "task198_evaluator_occurrence_values_sha256":
                evaluator_trace["occurrence_values_sha256"],
            "task198_evaluator_direct_values_sha256":
                digest_obj(evaluator_trace["direct_values"])},
        "group_field_coordinate_codecs": quotient_codec(),
        "actor_orbit_convention": ACTOR_CONVENTION,
        "occurrences": occurrences,
        "combined_w": [{"ordinal": item["ordinal"],
                         "terms": copy.deepcopy(item["w_o"])}
                        for item in occurrences],
        "combined_u0": copy.deepcopy(full_abi["u0"]),
        "target_blocks": copy.deepcopy(targets),
        "target_role": "ONE_MINUS_R_B_G760",
        "full_package_fields_excluded": copy.deepcopy(
            p0["consumer_abi"]["excluded_fields"])}
    interface_seal = seal_fresh(interface, "checker projected interface")
    consumer = _consumer_body(interface, p0)
    consumer_seal = seal_fresh(consumer, "checker task227 consumer ABI")
    validate_projection(interface, consumer, p0)
    return interface, consumer, {
        "projected_interface_body_sha256": interface_seal,
        "projected_interface_sealed_sha256": digest_obj(interface),
        "task227_consumer_abi_body_sha256": consumer_seal,
        "task227_consumer_abi_sealed_sha256": digest_obj(consumer),
        "old_seal_removed_before_each_reseal": True,
        "baseline_validated_before_mutation": True}


def base_reference(abi, g760):
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
        "package_role": "BASE_REFERENCE_ONLY",
        "full_task226_abi_body_sha256": abi["self_digest_sha256"],
        "full_task226_abi_sealed_sha256": digest_obj(abi),
        "full_package_fields": {
            "f": {"type": "BASE_REFERENCE_ONLY", "value": list(g760),
                  "transfer_evidence": False},
            "a": {"type": "BASE_REFERENCE_ONLY", "value": [],
                  "transfer_evidence": False},
            "rword_f": {"type": "BASE_REFERENCE_ONLY",
                        "value": literals["rword_f"],
                        "transfer_evidence": False},
            "B_a": {"type": "BASE_REFERENCE_ONLY", "value": literals["B_a"],
                    "transfer_evidence": False},
            "PB_chain_fields": {"type": "BASE_REFERENCE_ONLY",
                                "value": pb_fields,
                                "transfer_evidence": False}},
        "f_equals_g760": True,
        "B_a_zero": all(literals["B_a"].get(block) == []
                         for block in ("H1", "H2", "P")),
    }


EVALUATOR_BUILD_OPERATIONS = 26 + 243 * 26 + 59_049 * 6 + 243 * 10
Q0_SECTION_ORDER = 1_469_664


class EvaluatorBudget:
    """Checker-local meter adapter for accepted independent evaluator APIs."""
    def __init__(self, meter):
        self.meter = meter

    def check(self, phase):
        self.meter.check("checker task198 evaluator:" + phase)

    def bump(self, key, amount, phase):
        require(key == "gamma_operations",
                "unexpected checker evaluator dependency counter:" + key)
        self.meter.bump("evaluator_operations", amount,
                        "checker task198 evaluator:" + phase)


def build_checker_evaluator_runtime(arithmetic, checker_arithmetic, joint,
                                    p176, q3_raw, meter):
    meter.reserve("evaluator_builds", 1,
                  "checker task198 evaluator build reserve")
    meter.reserve("evaluator_operations", EVALUATOR_BUILD_OPERATIONS,
                  "checker evaluator known build work reserve")
    budget = EvaluatorBudget(meter)
    try:
        with WallDeadline(meter, "checker task198 evaluator runtime build"):
            q3 = json.loads(q3_raw)
            require(q3.get("schema") == "d972-b345-q-chief/v1" and
                    q3.get("terminal_token") ==
                        "B345_Q3_TYPED_SIGN_EXACT_WITH_WORD_CORRECTION",
                    "checker evaluator q3 terminal")
            probe = [1, -2, 1, 2]
            require(arithmetic.embed_f2_pb3(probe) ==
                    checker_arithmetic.embed_f2(probe),
                    "checker independent arithmetic orientation")
            e3, e4, _ = arithmetic.reconstruct_quotients(q3)
            contexts, _, context_public = arithmetic.cheap_context_registry(e4)
            require(len(contexts) == 31 and
                    len(context_public["named_uses"]) == 46,
                    "checker evaluator context registry")
            words = [list(row["word"])
                     for row in q3["correction_fibre"]["records"]
                     if row.get("word")]
            require(len(words) == 26, "checker evaluator correction words")
            group = joint.JointGroup(checker_arithmetic, e3, e4,
                                     contexts, words)
            require(len(group.states) == 243 and
                    len(group.transitions) == 243,
                    "checker independent evaluator Gamma order")
            fine, _ = p176.build_fine_deletion(e3, e4, budget)
            q0_marked = [p176.canonical_packed_permutation(
                arithmetic.perm_from_row(row, 36), 36,
                "checker v5 evaluator Q0 mark")
                for row in q3["coarse_models"]["Q0"]["marked_permutations"]]
            delete, _ = p176.make_deleter(arithmetic, e3, e4, fine,
                                          q0_marked)
            runtime = {"p176": p176, "old": arithmetic, "e3": e3,
                       "e4": e4, "contexts": contexts, "delete": delete}
            rebuilt = {"group": group, "words": words}
            parent_raw = bytearray(4 * Q0_SECTION_ORDER)
            parent_raw[4:8] = (1).to_bytes(4, "little")
            letters = bytearray(Q0_SECTION_ORDER)
            letters[1] = 1
            q0_private = {"parent_raw": bytes(parent_raw),
                          "letters": bytes(letters)}
            del parent_raw, letters
    except BaseException:
        meter.release("evaluator_builds", 1)
        meter.release("evaluator_operations", EVALUATOR_BUILD_OPERATIONS)
        raise
    meter.consume("evaluator_operations", EVALUATOR_BUILD_OPERATIONS,
                  EVALUATOR_BUILD_OPERATIONS,
                  "checker evaluator known build work")
    meter.consume("evaluator_builds", 1, 1,
                  "checker task198 evaluator build")
    meter.sample_rss("checker task198 evaluator runtime boundary")
    return runtime, rebuilt, q0_private, budget


def evaluator_exercise(contract, rows, g760, central, targets, task198_meta,
                       task198, runtime, rebuilt, q0_private, budget, meter):
    require(contract["occurrence_ledger"] == rows and
            contract["encoding"] == {
                "roof_value": "ten lowercase hex typed coordinate blobs",
                "source_word": "strict signed F2 list",
                "state_ids": "one-based Gamma and Q0 ids"} and
            contract["semantics"] == {
                "action": "actor*value*actor_inverse",
                "multiplication": "left_then_right",
                "section_cocycle": "s_left*s_right*s_product_inverse"},
            "checker task198 evaluator contract reconstruction binding")
    require(all(type(letter) is int and letter != 0 and abs(letter) <= 2
                for letter in g760), "checker evaluator source-word encoding")
    widths = contract["coordinate_widths"]
    require(len(widths) == 10 and all(widths[row["ten_index"]] ==
            (40 if row["type"] == "E3" else 154) for row in rows),
            "checker evaluator typed coordinate widths")
    entries = contract["entry_points"]
    require(set(entries) == {"action", "eval", "inverse", "multiply",
            "section_cocycle", "source_section"} and
            all(central["identity_checks"].values()) and
            set(targets) == {"H1", "H2", "P"},
            "checker evaluator ordinary base/central exercise")
    functions = {
        "eval": task198.checker_eval,
        "multiply": task198.checker_multiply,
        "inverse": task198.checker_inverse,
        "source_section": task198.checker_source_section,
        "action": task198.checker_action,
        "section_cocycle": task198.checker_section_cocycle,
    }
    require(all(callable(value) for value in functions.values()),
            "checker accepted independent evaluator functions")
    direct_counts = {name: 0 for name in sorted(functions)}

    def invoke(name, *args):
        meter.bump("evaluator_calls", 1,
                   "checker accepted task198 direct call:" + name)
        direct_counts[name] += 1
        if name == "source_section":
            return functions[name](runtime, rebuilt, q0_private,
                                   *args, budget)
        return functions[name](runtime, *args, budget)

    g760_value = invoke("eval", g760)
    x = invoke("eval", [1])
    y = invoke("eval", [2])
    xy = invoke("multiply", x, y)
    x_inverse = invoke("inverse", x)
    g760_inverse = invoke("inverse", g760_value)
    source = invoke("source_section", 2, 2)
    action = invoke("action", [1], y)
    cocycle = invoke("section_cocycle", [1], [2], [1, 2])
    canaries = task198_meta["evaluator_canaries"]
    require(x == canaries["x"]["value"] and
            y == canaries["y"]["value"] and
            xy == canaries["xy"]["value"] and
            x_inverse == canaries["x_inverse"]["value"] and
            source == canaries["source_2_2"] and
            action == canaries["x_action_y"]["value"] and
            cocycle == canaries["xy_section_cocycle"]["value"],
            "checker independent evaluator direct canaries")
    require(all(_roof_value(value, widths) for value in
                (g760_value, x, y, xy, x_inverse, g760_inverse,
                 source["value"], action, cocycle)),
            "checker independent evaluator typed values")
    occurrence_values = []
    for row in rows:
        value = (g760_value if row["factor_sign"] == 1
                 else g760_inverse)[row["ten_index"]]
        width = widths[row["ten_index"]]
        require(len(value) == 2 * width and
                row["orientation"] ==
                    ("direct" if row["factor_sign"] == 1 else "inverse"),
                "checker occurrence evaluator binding")
        occurrence_values.append({
            "ordinal": row["ordinal"], "occurrence": row["occurrence"],
            "ten_index": row["ten_index"], "factor_sign": row["factor_sign"],
            "orientation": row["orientation"], "width_bytes": width,
            "value": value})
    meter.bump("evaluator_support", len(occurrence_values),
               "checker eleven occurrence bindings")
    require(direct_counts == {"action": 1, "eval": 3, "inverse": 2,
            "multiply": 1, "section_cocycle": 1, "source_section": 1},
            "checker exact direct evaluator calls")
    shared = {"contract_sha256": digest_obj(contract),
            "decoded_callable_bindings": copy.deepcopy(entries),
            "source_word_sha256": word_digest(g760),
            "typed_coordinate_widths": list(widths),
            "ledger_sha256": digest_obj(rows),
            "ordinary_base_target_sha256": digest_obj(targets),
            "ordinary_central_replay_sha256": digest_obj(central),
            "direct_call_counts": direct_counts,
            "actual_transitive_call_counts": {
                "action": 1, "eval": 6, "inverse": 3, "multiply": 4,
                "section_cocycle": 1, "source_section": 1},
            "direct_values": {
                "g760": g760_value, "x": x, "y": y, "xy": xy,
                "x_inverse": x_inverse, "g760_inverse": g760_inverse,
                "source_2_2": source, "x_action_y": action,
                "xy_section_cocycle": cocycle},
            "occurrence_values": occurrence_values,
            "occurrence_values_sha256": digest_obj(occurrence_values),
            "accepted_canaries_sha256":
                task198_meta["evaluator_canaries_sha256"],
            "evaluator_build_operations_formula":
                "26+243*26+59049*6+243*10",
            "evaluator_build_operations": EVALUATOR_BUILD_OPERATIONS,
            "multiplication_convention_exercised":
                contract["semantics"]["multiplication"],
            "action_convention_exercised": contract["semantics"]["action"],
            "cocycle_convention_authenticated":
                contract["semantics"]["section_cocycle"]}
    independent = {
        "implementation":
            "crosscheck/check_d972_r07_seven_context_roof_presentation_v1.py",
        "direct_call_counts": direct_counts,
        "actual_transitive_call_counts": {
            "action": 1, "eval": 8, "inverse": 3, "multiply": 4,
            "section_cocycle": 1, "source_section": 1},
        "direct_values": copy.deepcopy(shared["direct_values"]),
        "direct_values_sha256": digest_obj(shared["direct_values"]),
        "occurrence_values_sha256": digest_obj(occurrence_values),
        "q0_private_bytes": 5 * Q0_SECTION_ORDER,
        "producer_trace_reconstructed_sha256": digest_obj(shared),
    }
    return shared, independent


def area_canary(engine, g760, rows, targets, meter):
    zword = red(commword([1], [2]) * 3)
    output = []
    for exponent in (0, 1, 2):
        representative = red(list(g760) + zword * exponent)
        meter.reserve("area_builds", AREA_BUILD_RESERVE,
                      "checker projected area build reserve")
        try:
            with WallDeadline(meter, "checker projected area build"):
                abi = engine.reconstruct(representative, [], rows)
        except BaseException:
            meter.release("area_builds", AREA_BUILD_RESERVE)
            raise
        meter.consume("area_builds", AREA_BUILD_RESERVE, 1,
                      "checker projected area build")
        require(abi["bar_epsilon_1"] == targets, "projected area target")
        output.append({"t": exponent, "word_length": len(representative),
                       "word_sha256": word_digest(representative),
                       "bar_epsilon_1": abi["bar_epsilon_1"],
                       "label": "PROJECTED_AREA_REPRESENTATIVE_ONLY"})
        del abi
        meter.sample_rss("checker projected area boundary:" + str(exponent))
    return {"zword": zword, "zword_sha256": word_digest(zword), "rows": output,
            "all_equal_base_target": True,
            "label": "PROJECTED_AREA_REPRESENTATIVE_ONLY"}


def mutation_fixture(rows, g760, interface, consumer, central, areas,
                     base_ref, target_constructor_owner):
    return {"ledger": rows, "g760": g760,
            "base": base_ref, "central": central,
            "areas": areas,
            "target_constructor_owner": target_constructor_owner,
            "interface": interface,
            "consumer": consumer,
            "flags": {flag: False for flag in FALSE_FLAGS}}

def validate_ledger_owner(value):
    if type(value) is not list or len(value) != 11:
        raise NarrowReject("task198 ledger roster")
    for actual, expected in zip(value, make_ledger()):
        if actual.get("factor_sign") != expected["factor_sign"]:
            raise NarrowReject("task198 ledger sign")
        if actual.get("fox_prefix_occurrences") != expected["fox_prefix_occurrences"]:
            raise NarrowReject("task198 ledger prefix")
    if value != make_ledger():
        raise NarrowReject("task198 ledger roster")
    return True


def validate_g760_owner(value):
    if (type(value) is not list or len(value) != 760 or
            word_digest(value) != EXPECTED_G760_SHA256):
        raise NarrowReject("g760 digest")
    return True


def validate_base_owner(value):
    if value.get("mode") != "PRE_A0_COMPUTATIONAL_BASE_ONLY":
        raise NarrowReject("computational-base mode")
    if value.get("task192_consumed") is not False:
        raise NarrowReject("task192 binding")
    return True


def validate_false_flags(value):
    if (type(value) is not dict or
            any(value.get(flag) is not False for flag in FALSE_FLAGS)):
        raise NarrowReject("forbidden conclusion flag")
    return True


def run_mutations(rows, p0, g760, interface, consumer,
                  central, areas, base_ref, target_constructor_owner,
                  raw_authority_record, meter):
    roster = p0["mutation_roster"]
    reference = mutation_fixture(rows, g760, interface, consumer, central,
                                 areas, base_ref,
                                 target_constructor_owner)
    require(validate_ledger_owner(reference["ledger"]) is True and
            validate_g760_owner(reference["g760"]) is True and
            validate_base_owner(reference["base"]) is True and
            validate_projection(reference["interface"],
                                reference["consumer"], p0) is True and
            validate_false_flags(reference["flags"]) is True and
            all(reference["central"]["identity_checks"].values()) and
            reference["areas"]["all_equal_base_target"] is True,
            "checker untouched ordinary mutation baseline")
    records = [raw_authority_record]
    for name in roster[1:]:
        route = None
        if name == "task198_ledger_sign":
            owner = "ledger"
            mutant_owner = list(reference[owner])
            mutant_owner[0] = dict(mutant_owner[0])
            mutant_owner[0]["factor_sign"] *= -1
            before_value = reference[owner]
            route = lambda: validate_ledger_owner(mutant_owner)
        elif name == "task198_prefix":
            owner = "ledger"
            mutant_owner = list(reference[owner])
            mutant_owner[0] = dict(mutant_owner[0])
            mutant_owner[0]["fox_prefix_occurrences"] = [2, 3]
            before_value = reference[owner]
            route = lambda: validate_ledger_owner(mutant_owner)
        elif name == "g760_letter_digest":
            owner = "g760"
            mutant_owner = list(reference[owner])
            mutant_owner[0] *= -1
            before_value = reference[owner]
            route = lambda: validate_g760_owner(mutant_owner)
        elif name == "computational_base_mode":
            owner = "base"
            mutant_owner = dict(reference[owner])
            mutant_owner["mode"] = "MUTATED_FORBIDDEN_MODE"
            before_value = reference[owner]
            route = lambda: validate_base_owner(mutant_owner)
        elif name == "forbidden_task192_binding":
            owner = "base"
            mutant_owner = dict(reference[owner])
            mutant_owner["task192_consumed"] = True
            before_value = reference[owner]
            route = lambda: validate_base_owner(mutant_owner)
        elif name == "H1_central_row":
            owner = "central"
            mutant_owner = dict(p0["central_rows"])
            block_owner = dict(mutant_owner["H1"])
            block_rows = list(block_owner["rows"])
            block_rows[0] = list(block_rows[0])
            block_rows[0][0] = 3
            block_owner["rows"] = block_rows
            mutant_owner["H1"] = block_owner
            mutant_p0 = {"central_rows": mutant_owner}
            before_value = p0["central_rows"]
            route = lambda: central_replay(rows, mutant_p0)
        elif name == "H2_central_row":
            owner = "central"
            mutant_owner = dict(p0["central_rows"])
            block_owner = dict(mutant_owner["H2"])
            block_rows = list(block_owner["rows"])
            block_rows[0] = list(block_rows[0])
            block_rows[0][0] = 6
            block_owner["rows"] = block_rows
            mutant_owner["H2"] = block_owner
            mutant_p0 = {"central_rows": mutant_owner}
            before_value = p0["central_rows"]
            route = lambda: central_replay(rows, mutant_p0)
        elif name == "P_central_row":
            owner = "central"
            mutant_owner = dict(p0["central_rows"])
            block_owner = dict(mutant_owner["P"])
            block_rows = list(block_owner["rows"])
            block_rows[0] = list(block_rows[0])
            block_rows[0][3] = 3
            block_owner["rows"] = block_rows
            mutant_owner["P"] = block_owner
            mutant_p0 = {"central_rows": mutant_owner}
            before_value = p0["central_rows"]
            route = lambda: central_replay(rows, mutant_p0)
        elif name == "projected_area_target":
            owner = "target_constructor_owner"
            before_value = {
                "bar_epsilon_1": reference[owner]["bar_epsilon_1"],
                "literals": {"relation_words_g":
                    reference[owner]["literals"]["relation_words_g"]}}
            mutant_owner = {
                "bar_epsilon_1": dict(reference[owner]["bar_epsilon_1"]),
                "literals": {"relation_words_g":
                    reference[owner]["literals"]["relation_words_g"]}}
            mutant_owner["bar_epsilon_1"]["H1"] = []
            route = lambda: target_from_fox(
                g760, rows, mutant_owner)
        elif name == "ABI_seal_target":
            owner = "consumer"
            before_value = reference[owner]
            mutant_owner = dict(reference[owner])
            mutant_bar = dict(mutant_owner["bar_epsilon_1"])
            mutant_bar["H1"] = []
            mutant_owner["bar_epsilon_1"] = mutant_bar
            seal_fresh(mutant_owner, "checker mutated consumer ABI")
            route = lambda: validate_projection(
                reference["interface"], mutant_owner, p0)
        elif name == "forbidden_conclusion_flag":
            owner = "flags"
            before_value = reference[owner]
            mutant_owner = dict(reference[owner])
            mutant_owner["fake"] = True
            route = lambda: validate_false_flags(mutant_owner)
        else:
            raise InputStop("unregistered mutation:" + name)
        before, after = digest_obj(before_value), digest_obj(mutant_owner)
        require(before != after, "mutation owner unchanged:" + name)
        meter.bump("mutation_work", 1, "checker ordinary mutation:" + name)
        observed = None
        try:
            route()
        except NarrowReject as exc:
            observed = str(exc)
        except InputStop as exc:
            reason_map = {
                "central rows/sum:H1": "H1_central_row",
                "central rows/sum:H2": "H2_central_row",
                "central rows/sum:P": "P_central_row",
                "base target 1-R_B(g760)": "projected area target",
                "task227 consumer ABI derived only from projection":
                    "ABI seal/target"}
            if str(exc) in reason_map:
                observed = reason_map[str(exc)]
            else:
                raise
        if observed is None:
            raise MutationAccepted("accepted mutation:" + name)
        expected = p0["mutation_expected_reasons"][name]
        if observed != expected:
            raise InputStop("mutation wrong first reason:" + name + ":" + observed)
        records.append({"name": name, "changed_field": owner,
                        "expected_gate": expected, "observed_reason": observed,
                        "before_sha256": before, "after_sha256": after,
                        "first_gate": observed,
                        "ordinary_validator": {
                            "task198_ledger_sign": "validate_ledger_owner",
                            "task198_prefix": "validate_ledger_owner",
                            "g760_letter_digest": "validate_g760_owner",
                            "computational_base_mode": "validate_base_owner",
                            "forbidden_task192_binding": "validate_base_owner",
                            "H1_central_row": "central_replay",
                            "H2_central_row": "central_replay",
                            "P_central_row": "central_replay",
                            "projected_area_target": "target_from_fox",
                            "ABI_seal_target": "validate_projection",
                            "forbidden_conclusion_flag": "validate_false_flags",
                        }[name],
                        "rejected": True})
    require([record["name"] for record in records] == roster and
            all(record["rejected"] for record in records),
            "checker ordinary mutation matrix")
    return records


def load_engine(rel, size, sha, tag_name, meter):
    raw = read_bytes(rel, size, sha, meter, "import:" + tag_name,
                     authority=False)
    path = ROOT / safe_rel(rel)
    spec = importlib.util.spec_from_file_location("_task384_v5_checker_" + tag_name, path)
    require(spec is not None and spec.loader is not None, "import specification:" + tag_name)
    module = importlib.util.module_from_spec(spec)
    module_name = "_task384_v5_checker_" + tag_name
    require(module_name not in sys.modules,
            "fresh checker dynamic module name:" + tag_name)
    sys.modules[module_name] = module
    meter.reserve("dynamic_imports", 1, "dynamic import reserve:" + tag_name)
    try:
        with WallDeadline(meter, "dynamic import:" + tag_name):
            code = compile(raw, str(path), "exec", dont_inherit=True)
            exec(code, module.__dict__)
    except BaseException:
        sys.modules.pop(module_name, None)
        meter.release("dynamic_imports", 1)
        raise
    meter.consume("dynamic_imports", 1, 1, "dynamic import:" + tag_name)
    post = read_bytes(rel, size, sha, meter, "post-import:" + tag_name,
                      authority=False)
    del raw, post
    meter.sample_rss("checker dynamic import boundary:" + tag_name)
    return module


def read_receipt(path_text, expected_sha, meter):
    path = safe_rel(path_text, "ci/out/")
    require(type(expected_sha) is str and len(expected_sha) == 64 and
            all(character in "0123456789abcdef" for character in expected_sha),
            "receipt SHA pin length/encoding")
    absolute = ROOT / path
    try:
        info = absolute.lstat()
    except OSError as exc:
        raise InputStop("production receipt stat:" + str(exc))
    require(stat.S_ISREG(info.st_mode) and not absolute.is_symlink() and
            0 < info.st_size <= PRODUCER_RECEIPT_MAX,
            "production receipt stat envelope")
    meter.reserve("input_bytes", info.st_size, "production receipt read reserve")
    try:
        raw = absolute.read_bytes()
    except OSError as exc:
        meter.release("input_bytes", info.st_size)
        raise InputStop("production receipt read:" + str(exc))
    meter.consume("input_bytes", info.st_size, len(raw), "production receipt input")
    authenticated_sha = digest_bytes(raw)
    require(len(raw) == info.st_size and authenticated_sha == expected_sha,
            "production receipt physical SHA binding")
    try:
        value = json.loads(raw)
    except (ValueError, UnicodeError) as exc:
        raise InputStop("receipt JSON:" + str(exc))
    streaming_canonical(value, raw)
    streaming_seal(value, "self_digest_sha256",
                   value.get("self_digest_sha256"), "production receipt")
    require(value.get("schema") == RECEIPT_SCHEMA, "receipt schema")
    return path.as_posix(), raw, value, authenticated_sha


def flags_false(value):
    return all(value.get(flag) is False for flag in FALSE_FLAGS)


def seal_fixed_point(value, meter, reserve_amount, phase, pre_reserved=False):
    if not pre_reserved:
        meter.reserve("serialized_bytes", reserve_amount,
                      phase + ":maximum reserve")
    base = meter.used["serialized_bytes"]
    transient_bound = 3 * reserve_amount + CANONICAL_CHUNK
    meter.bump("serialization_peak_bytes", transient_bound,
               phase + ":old/new/encoded transient bound")
    frozen_wall = meter.elapsed()
    guess = base + 1
    raw = None
    try:
        for _ in range(16):
            value.pop("self_digest_sha256", None)
            value["resource_meter"] = meter.public(
                serialized_override=guess, wall_override=frozen_wall)
            _, seal = streaming_canonical(value)
            value["self_digest_sha256"] = seal
            raw = canonical(value)
            require(0 < len(raw) <= reserve_amount,
                    phase + ":serialized maximum")
            next_guess = base + len(raw)
            if next_guess == guess:
                meter.consume("serialized_bytes", reserve_amount, len(raw), phase)
                require(meter.used["serialized_bytes"] == guess,
                        phase + ":fixed-point telemetry")
                return raw
            guess = next_guess
        raise InputStop(phase + ":serialization fixed point")
    except BaseException:
        if meter.reserved["serialized_bytes"] >= reserve_amount:
            meter.release("serialized_bytes", reserve_amount)
        raise


def prepare_output(path_text):
    relative = safe_rel(path_text, "ci/out/")
    require(relative.parent == Path("ci/out"),
            "verdict must be a direct child of trusted ci/out")
    target = ROOT / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    require(target.parent.is_dir() and not target.parent.is_symlink(),
            "verdict parent envelope")
    if target.exists() or target.is_symlink():
        raise StaleOutput("stale final verdict refused")
    prefix = "." + target.name + ".tmp."
    if any(item.name.startswith(prefix) for item in target.parent.iterdir()):
        raise StaleOutput("stale verdict temp alias refused")
    return target


def open_output_parent():
    flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | \
        getattr(os, "O_NOFOLLOW", 0)
    root_fd = os.open(ROOT, flags)
    ci_fd = -1
    try:
        ci_fd = os.open("ci", flags, dir_fd=root_fd)
        return os.open("out", flags, dir_fd=ci_fd)
    finally:
        if ci_fd >= 0:
            os.close(ci_fd)
        os.close(root_fd)


def atomic_publish(target, raw):
    prefix = "." + target.name + ".tmp."
    temporary_name = prefix + str(os.getpid()) + "." + str(time.time_ns())
    target_name = target.name
    descriptor = -1
    directory = -1
    renamed = False
    try:
        directory = open_output_parent()
        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
        flags |= getattr(os, "O_NOFOLLOW", 0)
        descriptor = os.open(temporary_name, flags, 0o600,
                             dir_fd=directory)
        view = memoryview(raw)
        offset = 0
        while offset < len(view):
            written = os.write(descriptor, view[offset:])
            if written <= 0:
                raise OSError(errno.EIO, "short verdict write")
            offset += written
        view.release()
        os.fsync(descriptor)
        os.close(descriptor)
        descriptor = -1
        libc = ctypes.CDLL(None, use_errno=True)
        renameat2 = libc.renameat2
        renameat2.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int,
                              ctypes.c_char_p, ctypes.c_uint]
        renameat2.restype = ctypes.c_int
        result = renameat2(directory, os.fsencode(temporary_name), directory,
                           os.fsencode(target_name), 1)
        if result != 0:
            error = ctypes.get_errno()
            if error == errno.EEXIST:
                raise StaleOutput("no-overwrite verdict publication refused")
            raise OSError(error, os.strerror(error))
        renamed = True
        os.fsync(directory)
        os.close(directory)
        directory = -1
    except BaseException as exc:
        rollback_error = None
        if descriptor >= 0:
            try:
                os.close(descriptor)
            except OSError as cleanup:
                rollback_error = cleanup
        if directory >= 0:
            try:
                try:
                    os.unlink(target_name if renamed else temporary_name,
                              dir_fd=directory)
                except FileNotFoundError:
                    pass
            except OSError as cleanup:
                rollback_error = cleanup
            try:
                os.fsync(directory)
            except OSError as cleanup:
                rollback_error = cleanup
            try:
                os.close(directory)
            except OSError as cleanup:
                rollback_error = cleanup
        if rollback_error is not None:
            raise ResourceStop("failure-atomic verdict publication rollback",
                               "serialized_bytes", len(raw),
                               CAPS["serialized_bytes"]) from rollback_error
        if isinstance(exc, (InputStop, ResourceStop, StaleOutput)):
            raise
        raise ResourceStop("failure-atomic verdict publication",
                           "serialized_bytes", len(raw),
                           CAPS["serialized_bytes"])


def release_normal_output_reserve(meter):
    normal = min(NORMAL_OUTPUT_MAX,
                 max(0, meter.reserved["serialized_bytes"] -
                     EMERGENCY_OUTPUT_MAX))
    if normal:
        meter.release("serialized_bytes", normal)


def verdict_document(receipt_path, receipt_raw, receipt_sha256,
                     pinned_receipt_sha256, terminal, accepted, p0,
                     pins, receipt=None, context=None, gate=None,
                     mutations=None, reconstructed_result_sha256=None,
                     reason=None):
    require(type(receipt_raw) is bytes, "verdict receipt byte type")
    if receipt_raw:
        require(type(pinned_receipt_sha256) is str and
                len(pinned_receipt_sha256) == 64 and
                all(character in "0123456789abcdef"
                    for character in pinned_receipt_sha256) and
                type(receipt_sha256) is str and
                len(receipt_sha256) == 64 and
                all(character in "0123456789abcdef"
                    for character in receipt_sha256) and
                receipt_sha256 == pinned_receipt_sha256,
                "verdict authenticated receipt SHA transport")
    else:
        require(receipt_sha256 is None,
                "empty verdict receipt SHA transport")
    projection = None if context is None else context["seal_trace"]
    central = None if context is None else context["central"]
    value = {"schema": VERDICT_SCHEMA, "status": terminal,
             "terminal": terminal, "accepted": accepted,
             "independent": accepted,
             "receipt_path": receipt_path,
             "receipt_bytes": len(receipt_raw),
             "receipt_sha256": receipt_sha256 if receipt_raw else None,
             "receipt_self_digest_sha256": receipt.get("self_digest_sha256")
                if receipt is not None else None,
             "receipt_result_sha256": reconstructed_result_sha256,
             "p0": {"path": P0_PATH, "bytes": P0_BYTES,
                    "sha256": P0_SHA256,
                    "self_digest_sha256": P0_SELF_SHA256},
             "source_identities": {rel: {"bytes": size, "sha256": sha}
                                   for rel, (size, sha) in sorted(pins.items())},
             "task198_authority_sha256": None if context is None else
                streaming_canonical(context["task198_meta"])[1],
             "independent_task198_evaluator": None if context is None else
                context["independent_evaluator"],
             "projected_interface_body_sha256": None if projection is None else
                projection["projected_interface_body_sha256"],
             "projected_interface_sealed_sha256": None if projection is None else
                projection["projected_interface_sealed_sha256"],
             "task227_consumer_abi_body_sha256": None if projection is None else
                projection["task227_consumer_abi_body_sha256"],
             "task227_consumer_abi_sealed_sha256": None if projection is None else
                projection["task227_consumer_abi_sealed_sha256"],
             "central_replay_sha256": None if central is None else digest_obj(central),
             "occurrence_rank": gate.get("rank") if gate else None,
             "block_rank": gate.get("block_rank") if gate else None,
             "task227_terminal": gate.get("terminal") if gate else None,
             "independently_reconstructed_result_sha256":
                reconstructed_result_sha256,
             "mutation_matrix_sha256": digest_obj(mutations)
                if mutations is not None else None,
             "post_call_exact_counts": None if gate is None else
                {"ideal_rows": len(gate.get("ideal_486", [])),
                 "translates": len(gate.get("translate_729", [])),
                 "independent_verify_calls": 1,
                 "frozen_internal_span_comparison_calls": 12,
                 "wrapper_reversed_span_calls": 0},
             "resource_formulas": None if context is None else
                copy.deepcopy(CHECKER_RESOURCE_FORMULAS),
             "reason": reason}
    value.update({flag: False for flag in FALSE_FLAGS})
    return value


def emergency_unknown(receipt_path, receipt_raw, receipt_sha256,
                      pinned_receipt_sha256, terminal, exc, meter, p0, pins):
    reason = str(exc)[:512]
    detail = {"typed_unknown": terminal, "reason": reason}
    if terminal == UNKNOWN_RESOURCE:
        detail.update({"phase": getattr(exc, "phase", "memory allocation"),
                       "cap": getattr(exc, "cap", "RLIMIT_AS"),
                       "value": getattr(exc, "value", "MemoryError"),
                       "limit": getattr(exc, "limit", CAPS["rss_bytes"])})
    return verdict_document(
        receipt_path, receipt_raw, receipt_sha256, pinned_receipt_sha256,
        terminal, False, p0, pins, reason=detail)


def reconstruct_context(p0, pins, rows, evaluator_contract, task198_meta,
                        q3_raw, raw_authority_record, meter):
    g616, g760 = construct_g760()
    require(validate_ledger_owner(rows) is True,
            "checker ordinary task198 ledger baseline")
    validate_g760_owner(g760)
    arithmetic = load_engine(*SOURCE_PINS["e4_arithmetic"],
                             "task198_arithmetic", meter)
    checker_arithmetic = load_engine(*SOURCE_PINS["e4_arithmetic_checker"],
                                     "task198_checker_arithmetic", meter)
    joint = load_engine(*SOURCE_PINS["joint_checker"],
                        "task198_checker_joint", meter)
    p176 = load_engine(*SOURCE_PINS["task176_producer"],
                       "task198_task176", meter)
    t198 = load_engine(*SOURCE_PINS["task198_checker"],
                       "task198_checker_evaluator", meter)
    evaluator_runtime, rebuilt, q0_private, evaluator_budget = \
        build_checker_evaluator_runtime(
            arithmetic, checker_arithmetic, joint, p176, q3_raw, meter)
    t226 = load_engine(*SOURCE_PINS["task226_checker"], "task226", meter)
    t227 = load_engine(*SOURCE_PINS["task227_checker"], "task227", meter)
    meter.reserve("base_abi_builds", BASE_BUILD_RESERVE,
                  "checker computational base ABI reserve")
    try:
        with WallDeadline(meter, "checker computational base ABI"):
            full_abi = t226.reconstruct(g760, [], rows)
    except BaseException:
        meter.release("base_abi_builds", BASE_BUILD_RESERVE)
        raise
    meter.consume("base_abi_builds", BASE_BUILD_RESERVE, 1,
                  "checker computational base ABI")
    meter.sample_rss("checker computational base boundary")
    base_checks(full_abi, rows, g760)
    targets, trace = target_from_fox(g760, rows, full_abi)
    central = central_replay(rows, p0)
    with WallDeadline(meter, "checker accepted evaluator six operations"):
        evaluator_trace, independent_evaluator = evaluator_exercise(
            evaluator_contract, rows, g760, central, targets, task198_meta,
            t198, evaluator_runtime, rebuilt, q0_private, evaluator_budget,
            meter)
    interface, consumer, seal_trace = make_projection(
        full_abi, rows, targets, task198_meta, evaluator_trace, p0)
    base_ref = base_reference(full_abi, g760)
    validate_base_owner(base_ref)
    validate_false_flags({flag: False for flag in FALSE_FLAGS})
    areas = area_canary(t226, g760, rows, targets, meter)
    mutations = run_mutations(rows, p0, g760, interface,
                              consumer, central, areas, base_ref,
                              full_abi,
                              raw_authority_record, meter)
    meter.sample_rss("checker projection and mutation boundary")
    return {"g616": g616, "g760": g760, "t227": t227,
            "targets": targets, "target_trace": trace, "central": central,
            "evaluator_trace": evaluator_trace, "interface": interface,
            "independent_evaluator": independent_evaluator,
            "consumer": consumer, "seal_trace": seal_trace,
            "base_reference": base_ref, "areas": areas,
            "mutations": mutations, "task198_meta": task198_meta,
            "pins": pins}


def check_certificate(receipt_path, receipt_raw, receipt, p0, context, meter):
    terminal = receipt.get("terminal")
    require(flags_false(receipt) and receipt.get("status") == terminal,
            "receipt forbidden conclusion/status flag")
    if terminal in (UNKNOWN_INPUT, UNKNOWN_RESOURCE):
        require(type(receipt.get("result")) is dict and
                receipt["result"].get("typed_unknown") == terminal,
                "typed unknown receipt")
        return terminal, None, None
    require(terminal in (MEMBER_TOP, NONMEMBER_TOP) and
            receipt.get("accepted") is True,
            "receipt accepting terminal vocabulary")
    g616, g760 = context["g616"], context["g760"]
    result = receipt.get("result")
    require(type(result) is dict and result.get("mode") == "PRE_A0_COMPUTATIONAL_BASE_ONLY" and
            result.get("correction_word_constructed") is False and
            result.get("task192_consumed") is False and
            result.get("f_role") == "BASE_REFERENCE_EQUAL_TO_G760",
            "receipt computational base typing")
    require(result.get("projected_a3_interface_v2") == context["interface"] and
            result.get("task227_consumer_abi") == context["consumer"] and
            result.get("projection_seal_trace") == context["seal_trace"],
            "receipt v303-only projection/consumer binding")
    require(result.get("base_reference") == context["base_reference"],
            "receipt BASE_REFERENCE_ONLY package binding")
    require(result.get("g616") == {"length": len(g616), "sha256": word_digest(g616)} and
            result.get("g760", {}).get("word") == g760 and
            result.get("g760", {}).get("length") == 760 and
            result.get("g760", {}).get("sha256") == word_digest(g760) and
            result.get("g760", {}).get("exponent_sums") == [0, 0],
            "receipt g760 binding")
    require(result.get("central_replay") == context["central"] and
            result.get("target_trace") == context["target_trace"] and
            result.get("task198_evaluator_exercise") == context["evaluator_trace"],
            "receipt central/target replay binding")
    require(result.get("area_canary") == context["areas"],
            "receipt area canary")
    mutations = context["mutations"]
    require(result.get("mutation_controls", {}).get("attempted") == p0["mutation_roster"] and
            result.get("mutation_controls", {}).get("baseline") == "PASS" and
            result.get("mutation_controls", {}).get("rejected") == mutations,
            "receipt mutation controls")
    require(result.get("false_conclusion_flags") ==
            p0["false_conclusion_flags"] and
            all(result["false_conclusion_flags"].get(flag) is False
                for flag in FALSE_FLAGS),
            "receipt complete false conclusion flags")
    expected_pins = {rel: {"bytes": size, "sha256": sha}
                     for rel, (size, sha) in sorted(context["pins"].items())}
    require(result.get("authority", {}).get("pins") == expected_pins and
            result["authority"].get("p0") == {
                "path": P0_PATH, "bytes": P0_BYTES, "sha256": P0_SHA256,
                "self_digest_sha256": P0_SELF_SHA256} and
            result["authority"].get("task198") == context["task198_meta"] and
            result["authority"].get("task227_selftest") ==
                p0["authority"]["task227_selftest_acceptance"],
            "receipt complete authority cross-binding")
    gate = result.get("gate")
    internal = T227_MEMBER if terminal == MEMBER_TOP else T227_NONMEMBER
    require(result.get("task227_terminal") == internal and type(gate) is dict,
            "receipt task227 terminal")
    require(all(gate.get(flag) is False for flag in FALSE_FLAGS),
            "gate complete false conclusion flags")
    meter.reserve("independent_verify_calls", 1,
                  "independent task227 verifier reserve")
    try:
        with WallDeadline(meter, "independent task227 verifier"):
            verified = context["t227"].verify_gate(
                gate, context["consumer"], internal, "production")
    except BaseException:
        meter.release("independent_verify_calls", 1)
        raise
    meter.consume("independent_verify_calls", 1, 1,
                  "independent task227 verifier")
    require(verified is True, "independent task227 verifier")
    meter.sample_rss("independent task227 verifier boundary")
    require(type(gate.get("rank")) is int and 0 <= gate["rank"] <= 486 and
            type(gate.get("block_rank")) is int and
            0 <= gate["block_rank"] <= 486 and
            gate.get("terminal") == internal and
            gate.get("rank") == result.get("rank") and
            gate.get("block_rank") == result.get("block_rank") and
            gate.get("ideal_486") and len(gate["ideal_486"]) == 486 and
            gate.get("translate_729") and len(gate["translate_729"]) == 729,
            "gate roster preservation")
    meter.bump("checker_roster", 729, "post-verifier exact translate roster")
    meter.bump("block_rows", 486, "post-verifier exact ideal roster")
    meter.bump("occurrence_rank_increases", gate["rank"],
               "post-verifier occurrence rank")
    meter.bump("block_rank_increases", gate["block_rank"],
               "post-verifier block rank")
    resource_meter = receipt.get("resource_meter", {})
    require(resource_meter.get("caps") == CAPS and
            resource_meter.get("used", {}).get("serialized_bytes") ==
                len(receipt_raw) and len(receipt_raw) > 0 and
            resource_meter.get("used", {}).get("closure_runs") == 1 and
            resource_meter.get("used", {}).get("base_abi_builds") == 1 and
            resource_meter.get("used", {}).get("area_builds") == 3 and
            resource_meter.get("used", {}).get("dynamic_imports") == 6 and
            resource_meter.get("used", {}).get("evaluator_builds") == 1 and
            resource_meter.get("used", {}).get("evaluator_calls") == 9 and
            resource_meter.get("used", {}).get("evaluator_support") == 11 and
            resource_meter.get("used", {}).get("serialization_peak_bytes") ==
                3 * PRODUCER_RECEIPT_MAX + CANONICAL_CHUNK,
            "receipt sealed nonzero resource telemetry")
    require(result.get("post_call_exact_counts") ==
            {"ideal_rows": 486, "translates": 729, "closure_calls": 1} and
            result.get("ideal_486_count") == 486 and
            result.get("translate_729_count") == 729,
            "receipt post-call exact counts")
    expected_result = {
        "mode": "PRE_A0_COMPUTATIONAL_BASE_ONLY",
        "correction_word_constructed": False,
        "task192_consumed": False,
        "f_role": "BASE_REFERENCE_EQUAL_TO_G760",
        "g616": {"length": len(g616), "sha256": word_digest(g616)},
        "g760": {"word": g760, "length": 760,
                 "sha256": word_digest(g760), "exponent_sums": [0, 0]},
        "base_reference": context["base_reference"],
        "projected_a3_interface_v2": context["interface"],
        "task227_consumer_abi": context["consumer"],
        "projection_seal_trace": context["seal_trace"],
        "central_replay": context["central"],
        "target_trace": context["target_trace"],
        "task198_evaluator_exercise": context["evaluator_trace"],
        "area_canary": context["areas"],
        "mutation_controls": {"baseline": "PASS",
                              "attempted": p0["mutation_roster"],
                              "rejected": mutations},
        "gate": gate,
        "task227_terminal": internal,
        "rank": gate["rank"], "block_rank": gate["block_rank"],
        "ideal_486_count": 486, "translate_729_count": 729,
        "post_call_exact_counts": {"ideal_rows": 486, "translates": 729,
                                   "closure_calls": 1},
        "resource_formulas": copy.deepcopy(PRODUCER_RESOURCE_FORMULAS),
        "authority": {
            "pins": expected_pins,
            "p0": {"path": P0_PATH, "bytes": P0_BYTES,
                   "sha256": P0_SHA256,
                   "self_digest_sha256": P0_SELF_SHA256},
            "task198": context["task198_meta"],
            "task227_selftest":
                p0["authority"]["task227_selftest_acceptance"]},
        "false_conclusion_flags": {flag: False for flag in FALSE_FLAGS},
    }
    require(result == expected_result, "receipt exact reconstructed result")
    _, reconstructed_sha = streaming_canonical(expected_result)
    return terminal, gate, reconstructed_sha


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("receipt")
    parser.add_argument("--verdict", required=True)
    parser.add_argument("--receipt-sha256", required=True)
    args = parser.parse_args(argv)
    meter = Meter()
    receipt_path = str(args.receipt)[:512]
    receipt_raw = b""
    receipt_sha256 = None
    p0 = {"self_digest_sha256": None, "authority": {}}
    pins = {}
    try:
        receipt_path = safe_rel(args.receipt, "ci/out/").as_posix()
        install_linux_hard_limits(meter)
        with WallDeadline(meter, "complete v5 checker route"):
            target = prepare_output(args.verdict)
            p0 = load_p0(meter)
            with WallDeadline(
                    meter,
                    "checker complete authority physical authentication"):
                pins, raws = authenticate_authority(p0, meter)
            with WallDeadline(
                    meter, "checker task198 complete authority validation"):
                rows, evaluator_contract, task198_meta, task198_snapshot = \
                    authenticate_task198(p0, pins, raws)
            q3_path = p0["authority"]["task198_evaluator_support"] \
                ["q3_receipt"]["path"]
            q3_raw = raws.pop(q3_path)
            with WallDeadline(
                    meter, "checker task198 ordinary authority mutation"):
                raw_authority_record = run_raw_authority_mutation(
                    p0, raws, task198_snapshot, meter)
            del task198_snapshot
            raws.clear()
            del raws
            meter.sample_rss(
                "checker task198 raw released after ordinary authority mutation")
            context = reconstruct_context(p0, pins, rows, evaluator_contract,
                                          task198_meta, q3_raw,
                                          raw_authority_record, meter)
            del q3_raw
            del evaluator_contract
            with WallDeadline(meter, "production receipt physical validation"):
                receipt_path, receipt_raw, receipt, receipt_sha256 = read_receipt(
                    args.receipt, args.receipt_sha256, meter)
            meter.sample_rss("production receipt parse boundary")
            with WallDeadline(meter, "complete independent certificate check"):
                terminal, gate, reconstructed_sha = check_certificate(
                    receipt_path, receipt_raw, receipt, p0, context, meter)
            accepted = terminal in (MEMBER_TOP, NONMEMBER_TOP)
            meter.reserve("serialized_bytes", NORMAL_OUTPUT_MAX,
                          "verdict output maximum before construction")
            output = verdict_document(
                receipt_path, receipt_raw, receipt_sha256,
                args.receipt_sha256, terminal, accepted, p0, pins,
                receipt=receipt, context=context, gate=gate,
                mutations=context["mutations"],
                reconstructed_result_sha256=reconstructed_sha)
            raw = seal_fixed_point(output, meter, NORMAL_OUTPUT_MAX,
                                   "verdict serialization", pre_reserved=True)
            atomic_publish(target, raw)
        print("D363_CHECKER_TERMINAL " + terminal, flush=True)
        return 0 if accepted else 2
    except StaleOutput as exc:
        print("D363_CHECKER_DIAGNOSTIC stale-output:" + str(exc),
              file=sys.stderr, flush=True)
        return 3
    except MutationAccepted as exc:
        print("D363_CHECKER_DIAGNOSTIC " + str(exc), file=sys.stderr,
              flush=True)
        return 4
    except MemoryError as exc:
        terminal = UNKNOWN_RESOURCE
        failure = exc
    except ResourceStop as exc:
        terminal = UNKNOWN_RESOURCE
        failure = exc
    except (InputStop, FileNotFoundError, KeyError, ValueError, UnicodeError,
            json.JSONDecodeError, OSError, RuntimeError) as exc:
        terminal = UNKNOWN_INPUT
        failure = exc
    try:
        release_normal_output_reserve(meter)
        with WallDeadline(meter, "complete v5 checker emergency publication"):
            target = prepare_output(args.verdict)
            unknown = emergency_unknown(
                receipt_path, receipt_raw, receipt_sha256,
                args.receipt_sha256, terminal, failure, meter, p0, pins)
            raw = seal_fixed_point(unknown, meter, EMERGENCY_OUTPUT_MAX,
                                   "emergency UNKNOWN verdict serialization",
                                   pre_reserved=True)
            atomic_publish(target, raw)
        print("D363_CHECKER_TERMINAL " + terminal, flush=True)
        return 2
    except BaseException as emergency:
        print("D363_CHECKER_DIAGNOSTIC emergency-publication-failed:" +
              str(emergency), file=sys.stderr, flush=True)
        return 5


if __name__ == "__main__":
    raise SystemExit(main())
