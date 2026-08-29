#!/usr/bin/env python3
"""Task384/v5 R07 pre-A0 single-target A3 producer.

This wrapper owns the g760 reconstruction, the v302 replay and the v303
projection.  The two frozen engines are loaded by digest under private names;
no new helper is imported by the production route.
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
NORMAL_OUTPUT_MAX = 19_000_000
EMERGENCY_OUTPUT_MAX = 65_536
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
    "e4_arithmetic": ("search/d972_b345_seedspan_triple4_v1.py", 535219,
                       "fe18fc31fdf3f9416ebb829112ccbd514c27e6a8d30fe24691842865277a0b29"),
    "joint_producer": ("search/d972_b345_joint_kernel_qstar_closure_v1.py", 67945,
                       "06ba6cf361957db3e339d48d14b3d4fbc689de9642e3f96273fbe8f3160e76dc"),
    "task176_producer": ("search/d972_r07_all_seven_extension_section_census_v1.py",
                         66109,
                         "878cf1d8d44e74a993309ed1c613c9fc57eb62fd2da48a30fd8797ff4b19af3b"),
    "task198_producer": ("search/d972_r07_seven_context_roof_presentation_v1.py",
                         137169,
                         "6b2645b80f97256a659af81e856c086cca724b36e2a22ae70335b29ffa95d44c"),
    "task226_producer": ("search/d972_r07_actual_two_word_endpoint_specializer_v2.py", 40556,
                          "a1532740a7343bd8166c17947f6bd95203a4abdaaafd8e0d9607d3cdf202e6fb"),
    "task227_producer": ("search/d972_r07_typed_single_seed_endpoint_consumer_v2.py", 47135,
                          "755ba97e55266bcdb51796cc1a89a562efa782db48475d0e3479e82e325cde8e"),
}
RESOURCE_FORMULAS = {
    "authority": {"formula": "16417+33121619", "bytes": 33138036,
                  "cap": 40000000, "owner_count": 23},
    "input": {"formula": "16417+33121619+2*894133",
              "bytes": 34926302, "cap": 60000000,
              "authenticated_source_import_bytes": 894133,
              "loader_extra_physical_reads": 0},
    "output": {"receipt_max_bytes": NORMAL_OUTPUT_MAX,
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
        self.frozen_alias_events = 0
        self.hard_limit = None
        self.reserve("serialized_bytes", EMERGENCY_OUTPUT_MAX,
                     "emergency output reserve")

    def elapsed(self):
        return time.monotonic() - self.started

    def check_wall(self, phase):
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
        self.check_wall(phase)

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
        self.check_wall(phase)

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
        self.check_wall(phase)
        return rss

    def note_frozen_orbit_alias(self, amount):
        self.frozen_alias_events += amount

    def public(self, serialized_override=None, wall_override=None):
        used = dict(self.used)
        used["wall_seconds"] = (self.elapsed() if wall_override is None
                                else wall_override)
        if serialized_override is not None:
            used["serialized_bytes"] = serialized_override
        return {
            "caps": dict(self.caps),
            "used": used,
            "rss_samples": list(self.rss_samples),
            "rss_sampling_is_not_an_in_call_interrupt": True,
            "hard_address_space": copy.deepcopy(self.hard_limit),
            "frozen_task227_orbit_alias_events_not_double_charged":
                self.frozen_alias_events,
        }


class ClosureBudget:
    """Adapter for task227's frozen duplicate qmul counter calls."""
    def __init__(self, meter):
        self.meter = meter
        self.used = meter.used
        self.alias_credit = 0

    def bump(self, key, amount, phase):
        if key == "actor_operations":
            self.meter.bump(key, amount, phase)
            self.alias_credit += amount
        elif key == "orbit_actions":
            require(self.alias_credit >= amount,
                    "frozen task227 orbit alias without actor event")
            self.alias_credit -= amount
            self.meter.note_frozen_orbit_alias(amount)
        else:
            self.meter.bump(key, amount, phase)


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
        self.meter.check_wall(self.phase + ":before")
        remaining = self.meter.caps["wall_seconds"] - self.meter.elapsed()
        if remaining <= 0:
            raise ResourceStop(self.phase, "wall_seconds",
                               self.meter.elapsed(),
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
    soft, hard = resource.getrlimit(resource.RLIMIT_AS)
    infinity = resource.RLIM_INFINITY
    target = meter.caps["rss_bytes"]
    if hard != infinity:
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
    require(p0["schema"] == SCHEMA + "/prereg/v1", "P0 schema")
    require(p0["caps"] == CAPS, "P0 caps")
    require(p0["terminal_vocabulary"] ==
            [MEMBER_TOP, NONMEMBER_TOP, UNKNOWN_INPUT, UNKNOWN_RESOURCE],
            "P0 terminal vocabulary")
    require(p0["central_rows"] == EXPECTED_CENTRAL, "P0 central rows")
    require(digest_obj(p0["authority"]["task198"]["evaluator_contract"]) ==
            p0["authority"]["task198"]["evaluator_contract_sha256"] ==
            "4fc38881ffee293f0820d3639230dd44a2af9b9ed126dfb21dc5831290ff08b8",
            "P0 evaluator contract digest")
    require(p0["consumer_abi"]["compatibility_presence_only_fields"] ==
            {"rword_f": CONSUMER_MARKER, "rword_g": CONSUMER_MARKER},
            "P0 consumer compatibility markers")
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
    ancestry = p0["authority"]["g760_ancestry"]
    require(type(ancestry) is list and len(ancestry) == 2 and
            {item["path"] for item in ancestry} == {
                "search/d972_r07_760_l3_target6_v1.py",
                "search/check_d972_r07_616_to_760_commutator_affine_rhs_v3.py"},
            "P0 complete g760 ancestry owners")
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


def local_ledger():
    return copy.deepcopy(LEDGER)


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
    """Recursively freeze a compact authenticated JSON value."""
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
    """Ordinary small-owner validator shared by baseline and mutation."""
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
            "task198_source_identities"} and
            manifest["schema"] ==
            "d972-r07-seven-context-roof-presentation/v1/acceptance-manifest/v3" and
            manifest["accepted"] is True and manifest["independent"] is True and
            manifest["synthetic"] is False,
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
            "task198_source_identities"} and
            manifest["schema"] ==
            "d972-r07-seven-context-roof-presentation/v1/acceptance-manifest/v3" and
            manifest["accepted"] is True and manifest["independent"] is True and
            manifest["synthetic"] is False,
            "task198 acceptance manifest")
    expected_manifest_contract = {
        "accepted_receipt_basename": authority["accepted_receipt_basename"],
        "checker": authority["checker"],
        "checker_attestation": _without_path(authority["checker_attestation"]),
        "checker_verdict": _without_path(authority["checker_verdict"]),
        "producer": authority["producer"],
        "producer_attestation": _without_path(authority["producer_attestation"]),
    }
    require(authority["manifest_contract"] == expected_manifest_contract,
            "P0 task198 manifest semantic contract")
    require(all(manifest[key] == value for key, value in
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
        manifest["producer"]["artifact_id"] ==
            manifest["checker"]["artifact_id"] and
        manifest["producer"]["zip_sha256"] ==
            manifest["checker"]["zip_sha256"],
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
            verdict["independent"] is True and
            verdict["receipt_terminal"] == T198_TERMINAL,
            "task198 checker verdict complete metadata")
    producer_att = raw_by_path[authority["producer_attestation"]["path"]]
    checker_att = raw_by_path[authority["checker_attestation"]["path"]]
    require(Path(authority["producer_attestation"]["path"]).name ==
            authority["producer_attestation"]["basename"] and
            len(producer_att) == authority["producer_attestation"]["bytes"] and
            digest_bytes(producer_att) ==
                authority["producer_attestation"]["sha256"] and
            producer_att.decode("ascii") ==
            "R07_SEVEN_CONTEXT_ROOF_PRESENTATION_V1_PRODUCER_TERMINAL ROOF_BRIDGE_ISOMORPHISM\n",
            "task198 producer attestation complete metadata")
    require(Path(authority["checker_attestation"]["path"]).name ==
            authority["checker_attestation"]["basename"] and
            len(checker_att) == authority["checker_attestation"]["bytes"] and
            digest_bytes(checker_att) ==
                authority["checker_attestation"]["sha256"] and
            checker_att.decode("ascii") ==
            "R07_SEVEN_CONTEXT_ROOF_PRESENTATION_V1_CHECKER_PASS terminal=ROOF_BRIDGE_ISOMORPHISM rows=6441\n",
            "task198 checker attestation complete metadata")
    bridge = receipt.get("bridge", {})
    rows = bridge.get("occurrence_ledger")
    expected_evaluator = authority["evaluator_contract"]
    require(rows == local_ledger() == expected_evaluator["occurrence_ledger"],
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
            digest_obj(expected_evaluator) ==
                authority["evaluator_contract_sha256"],
            "task198 complete evaluator ABI")
    _validate_evaluator_canaries(canaries,
                                 expected_evaluator["coordinate_widths"])
    require(raw_manifest_binding, "task198 raw/manifest binding")
    rows_out = copy.deepcopy(rows)
    evaluator_out = copy.deepcopy(expected_evaluator)
    manifest_snapshot = copy.deepcopy(expected_manifest_contract)
    meta = {
        "receipt_path": receipt_path, "receipt_bytes": len(receipt_raw),
        "receipt_sha256": pins[receipt_path][1],
        "manifest_path": manifest_path, "manifest_bytes": len(manifest_raw),
        "manifest_sha256": pins[manifest_path][1],
        "receipt_self_digest_sha256": receipt_seal,
        "manifest_self_digest_sha256": manifest_seal,
        "accepted_receipt_basename": authority["accepted_receipt_basename"],
        "manifest_contract": manifest_snapshot,
        "evaluator_contract_sha256": authority["evaluator_contract_sha256"],
        "evaluator_canaries_sha256": digest_obj(canaries),
        "evaluator_canaries": copy.deepcopy(canaries),
    }
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
        "manifest_contract": manifest_snapshot,
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
    meter.bump("mutation_work", 1, "ordinary authority mutation:" + name)
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
    require(type(abi.get("self_digest_sha256")) is str,
            "base ABI seal presence")
    streaming_seal(abi, "self_digest_sha256", abi["self_digest_sha256"],
                   "task226 BASE_REFERENCE_ONLY ABI")
    require(abi.get("ledger") == rows and abi.get("ten_to_eleven") ==
            [0, 1, 2, 3, 0, 4, 5, 6, 7, 8, 9] and
            abi.get("actor_convention") == ACTOR_CONVENTION,
            "base ledger/actor typing")
    literals = abi.get("literals", {})
    require(literals.get("rword_f") == literals.get("rword_g") and
            literals.get("relation_factors_f") == literals.get("relation_factors_g") and
            literals.get("relation_words_f") == literals.get("relation_words_g"),
            "base rword_f typing")
    for key in ("B_a",):
        require(all(literals.get(key, {}).get(block) == []
                    for block in ("H1", "H2", "P")), "base B_a zero")
    require(len(abi.get("occurrences", [])) == 11,
            "base occurrence count")
    for occurrence in abi["occurrences"]:
        require(occurrence.get("rword_f") == occurrence.get("rword_g") and
                occurrence.get("r_f") == occurrence.get("r_g"),
                "base occurrence rword_f")
    require(words["f"] == g760, "base f role")
    return abi


EVALUATOR_BUILD_OPERATIONS = 26 + 243 * 26 + 59_049 * 6 + 243 * 10


class EvaluatorBudget:
    """Meter adapter for the accepted task176/task198 evaluator APIs."""
    def __init__(self, meter):
        self.meter = meter

    def check(self, phase):
        self.meter.check_wall("task198 evaluator:" + phase)

    def bump(self, key, amount, phase):
        require(key == "gamma_operations",
                "unexpected evaluator dependency counter:" + key)
        self.meter.bump("evaluator_operations", amount,
                        "task198 evaluator:" + phase)


def build_task198_runtime(arithmetic, joint, p176, q3_raw, meter):
    meter.reserve("evaluator_builds", 1, "task198 evaluator build reserve")
    meter.reserve("evaluator_operations", EVALUATOR_BUILD_OPERATIONS,
                  "task198 evaluator known build work reserve")
    budget = EvaluatorBudget(meter)
    try:
        with WallDeadline(meter, "task198 evaluator runtime build"):
            q3 = json.loads(q3_raw)
            require(q3.get("schema") == "d972-b345-q-chief/v1" and
                    q3.get("terminal_token") ==
                        "B345_Q3_TYPED_SIGN_EXACT_WITH_WORD_CORRECTION",
                    "task198 evaluator q3 terminal")
            e3, e4, _ = arithmetic.reconstruct_quotients(q3)
            contexts, _, context_public = arithmetic.cheap_context_registry(e4)
            require(len(contexts) == 31 and
                    len(context_public["named_uses"]) == 46,
                    "task198 evaluator context registry")
            words = [list(row["word"])
                     for row in q3["correction_fibre"]["records"]
                     if row.get("word")]
            require(len(words) == 26, "task198 evaluator correction words")

            class PackedJointGroup(joint.JointGroup):
                def blob(self, value):
                    return p176.packed_joint_blob(
                        value, "v5 task198 evaluator Gamma element")

            gamma = PackedJointGroup(arithmetic, e3, e4, contexts, words)
            require(len(gamma.states) == 243 and
                    len(gamma.transitions) == 243,
                    "task198 evaluator Gamma order")
            fine, _ = p176.build_fine_deletion(e3, e4, budget)
            q0_marked = [p176.canonical_packed_permutation(
                arithmetic.perm_from_row(row, 36), 36,
                "v5 task198 evaluator Q0 mark")
                for row in q3["coarse_models"]["Q0"]["marked_permutations"]]
            delete, _ = p176.make_deleter(arithmetic, e3, e4, fine,
                                          q0_marked)
            projected = [p176.projection(state, delete)
                         for state in gamma.states]
            require(len(projected) == 243 and
                    all([len(p176.blob(arithmetic, value)) for value in row] ==
                        p176.COORDINATE_WIDTHS for row in projected),
                    "task198 evaluator projected widths")
            xrow = p176.eval_word_coordinates(
                arithmetic, e3, e4, contexts, delete, [1])
            stores = []
            for index, (value, width) in enumerate(zip(
                    xrow, p176.COORDINATE_WIDTHS)):
                raw = p176.blob(arithmetic, value)
                require(len(raw) == width,
                        "task198 evaluator Q0 support width")
                stores.append(bytearray(width) + bytearray(raw))
            runtime = {
                "p176": p176, "old": arithmetic, "e3": e3, "e4": e4,
                "contexts": contexts, "delete": delete, "gamma": gamma,
                "projected": projected, "parents": [0, 0],
                "letters": bytes([0, 1]), "stores": stores,
                "abi_budget": budget,
            }
    except BaseException:
        meter.release("evaluator_builds", 1)
        meter.release("evaluator_operations", EVALUATOR_BUILD_OPERATIONS)
        raise
    meter.consume("evaluator_operations", EVALUATOR_BUILD_OPERATIONS,
                  EVALUATOR_BUILD_OPERATIONS,
                  "task198 evaluator known build work")
    meter.consume("evaluator_builds", 1, 1, "task198 evaluator build")
    meter.sample_rss("task198 evaluator runtime boundary")
    return runtime


def evaluator_exercise(contract, rows, g760, central, targets, task198_meta,
                       task198, runtime, meter):
    require(contract["occurrence_ledger"] == rows and
            contract["encoding"] == {
                "roof_value": "ten lowercase hex typed coordinate blobs",
                "source_word": "strict signed F2 list",
                "state_ids": "one-based Gamma and Q0 ids"} and
            contract["semantics"] == {
                "action": "actor*value*actor_inverse",
                "multiplication": "left_then_right",
                "section_cocycle": "s_left*s_right*s_product_inverse"},
            "task198 evaluator contract reconstruction binding")
    require(all(type(letter) is int and letter != 0 and abs(letter) <= 2
                for letter in g760), "task198 evaluator source-word encoding")
    widths = contract["coordinate_widths"]
    require(len(widths) == 10 and all(widths[row["ten_index"]] ==
            (40 if row["type"] == "E3" else 154) for row in rows),
            "task198 evaluator typed coordinate widths")
    entries = contract["entry_points"]
    require(set(entries) == {"action", "eval", "inverse", "multiply",
            "section_cocycle", "source_section"},
            "task198 evaluator six-callable exercise roster")
    registry = task198.v188_consumer_action_abi()
    require(set(registry) == set(entries) and
            all(callable(registry[name]) and
                registry[name].__name__ == entries[name]["callable"]
                for name in entries),
            "task198 accepted live evaluator registry")
    require(all(central["identity_checks"].values()) and
            set(targets) == {"H1", "H2", "P"},
            "task198 evaluator ordinary base/central exercise")

    direct_counts = {name: 0 for name in sorted(registry)}

    def invoke(name, *args):
        meter.bump("evaluator_calls", 1,
                   "accepted task198 direct call:" + name)
        direct_counts[name] += 1
        return registry[name](runtime, *args)

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
            "task198 accepted evaluator direct canaries")
    require(all(_roof_value(value, widths) for value in
                (g760_value, x, y, xy, x_inverse, g760_inverse,
                 source["value"], action, cocycle)),
            "task198 accepted evaluator direct typed values")
    occurrence_values = []
    for row in rows:
        value = (g760_value if row["factor_sign"] == 1
                 else g760_inverse)[row["ten_index"]]
        width = widths[row["ten_index"]]
        require(len(value) == 2 * width and
                row["orientation"] ==
                    ("direct" if row["factor_sign"] == 1 else "inverse"),
                "task198 occurrence evaluator binding")
        occurrence_values.append({
            "ordinal": row["ordinal"], "occurrence": row["occurrence"],
            "ten_index": row["ten_index"], "factor_sign": row["factor_sign"],
            "orientation": row["orientation"], "width_bytes": width,
            "value": value})
    meter.bump("evaluator_support", len(occurrence_values),
               "task198 eleven occurrence bindings")
    require(direct_counts == {"action": 1, "eval": 3, "inverse": 2,
            "multiply": 1, "section_cocycle": 1, "source_section": 1},
            "task198 exact direct evaluator calls")
    return {
        "contract_sha256": digest_obj(contract),
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
        "accepted_canaries_sha256": task198_meta["evaluator_canaries_sha256"],
        "evaluator_build_operations_formula":
            "26+243*26+59049*6+243*10",
        "evaluator_build_operations": EVALUATOR_BUILD_OPERATIONS,
        "multiplication_convention_exercised": contract["semantics"]["multiplication"],
        "action_convention_exercised": contract["semantics"]["action"],
        "cocycle_convention_authenticated": contract["semantics"]["section_cocycle"],
    }


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
    return {
        "schema": p0["consumer_abi"]["schema"],
        "modulus": interface["modulus"],
        "occurrences": occurrences,
        "bar_epsilon_1": copy.deepcopy(interface["target_blocks"]),
        "u0": copy.deepcopy(interface["combined_u0"]),
        "ten_to_eleven": copy.deepcopy(interface["ten_to_eleven"]),
    }


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
            "projected interface allowlist")
    require(len(interface.get("occurrences", [])) == 11 and
            all(set(item) == INTERFACE_OCCURRENCE_FIELDS
                for item in interface["occurrences"]),
            "projected interface occurrence allowlist")
    interface_seal = interface.get("self_digest_sha256")
    streaming_seal(interface, "self_digest_sha256", interface_seal,
                   "projected interface baseline")
    expected_body = _consumer_body(interface, p0)
    consumer_seal = consumer.get("self_digest_sha256")
    streaming_seal(consumer, "self_digest_sha256", consumer_seal,
                   "task227 consumer ABI baseline")
    actual_body = dict(consumer)
    actual_body.pop("self_digest_sha256")
    require(actual_body == expected_body and
            set(actual_body) == set(p0["projection_allowlist"]) and
            all(set(item) == set(p0["consumer_abi"]["occurrence_fields"]) |
                {"rword_g", "rword_f"} for item in consumer["occurrences"]),
            "task227 consumer ABI derived only from projection")
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
                "projected occurrence field roster")
        occurrences.append(projected)
    interface = {
        "schema": SCHEMA + "/projected_a3_interface_v2",
        "projection_mode": "V303_PRE_A0_COMPUTATIONAL_BASE_PROJECTION",
        "mode": "PRE_A0_COMPUTATIONAL_BASE_ONLY",
        "correction_word_constructed": False,
        "task192_consumed": False,
        "f_role": "BASE_REFERENCE_EQUAL_TO_G760",
        "projection_only": True,
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
            p0["consumer_abi"]["excluded_fields"]),
    }
    interface_seal = seal_fresh(interface, "projected interface")
    consumer = _consumer_body(interface, p0)
    consumer_seal = seal_fresh(consumer, "task227 consumer ABI")
    validate_projection(interface, consumer, p0)
    return interface, consumer, {
        "projected_interface_body_sha256": interface_seal,
        "projected_interface_sealed_sha256": digest_obj(interface),
        "task227_consumer_abi_body_sha256": consumer_seal,
        "task227_consumer_abi_sealed_sha256": digest_obj(consumer),
        "old_seal_removed_before_each_reseal": True,
        "baseline_validated_before_mutation": True,
    }


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
        "package_role": "BASE_REFERENCE_ONLY",
        "full_task226_abi_body_sha256": abi["self_digest_sha256"],
        "full_task226_abi_sealed_sha256": digest_obj(abi),
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
        meter.reserve("area_builds", AREA_BUILD_RESERVE,
                      "projected area build reserve")
        try:
            with WallDeadline(meter, "projected area build"):
                package = engine.specialize(representative, [], rows)
        except BaseException:
            meter.release("area_builds", AREA_BUILD_RESERVE)
            raise
        meter.consume("area_builds", AREA_BUILD_RESERVE, 1,
                      "projected area build")
        target = package["specialization_v216_abi"]["bar_epsilon_1"]
        require(target == base_targets, "projected area target")
        out.append({"t": exponent, "word_length": len(representative),
                    "word_sha256": word_digest(representative),
                    "bar_epsilon_1": target,
                    "label": "PROJECTED_AREA_REPRESENTATIVE_ONLY"})
        del package
        meter.sample_rss("projected area build boundary:" + str(exponent))
    return {"zword": zword, "zword_sha256": word_digest(zword), "rows": out,
            "all_equal_base_target": True,
            "label": "PROJECTED_AREA_REPRESENTATIVE_ONLY"}


def resource_canary(phase):
    value = {"schema": "d972-r07-typed-single-seed-endpoint-consumer/v2/resource-canary/v1",
             "terminal": UNKNOWN_RESOURCE, "phase": phase,
             "cap": "serialized_bytes", "value": 0, "limit": 2000000000}
    value["self_digest_sha256"] = digest_obj(value)
    return value


def mutation_fixture(rows, g760, interface, consumer, central, areas,
                     base_ref, target_constructor_owner):
    return {
        "ledger": rows, "g760": g760,
        "base": base_ref, "central": central,
        "areas": areas,
        "target_constructor_owner": target_constructor_owner,
        "interface": interface, "consumer": consumer,
        "flags": {flag: False for flag in FALSE_FLAGS},
    }

def validate_ledger_owner(value):
    if type(value) is not list or len(value) != 11:
        raise NarrowReject("task198 ledger roster")
    for actual, expected in zip(value, local_ledger()):
        if actual.get("factor_sign") != expected["factor_sign"]:
            raise NarrowReject("task198 ledger sign")
        if actual.get("fox_prefix_occurrences") != expected["fox_prefix_occurrences"]:
            raise NarrowReject("task198 ledger prefix")
    if value != local_ledger():
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
            "untouched ordinary mutation baseline")
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
            seal_fresh(mutant_owner, "mutated task227 consumer ABI")
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
        before = digest_obj(before_value)
        after = digest_obj(mutant_owner)
        require(before != after, "mutation owner unchanged:" + name)
        meter.bump("mutation_work", 1, "ordinary mutation:" + name)
        observed = None
        try:
            route()
        except NarrowReject as exc:
            observed = str(exc)
        except InputStop as exc:
            central_reason = {
                "central rows:H1": "H1_central_row",
                "central rows:H2": "H2_central_row",
                "central rows:P": "P_central_row",
                "base target 1-R_B(g760)": "projected area target",
                "task227 consumer ABI derived only from projection":
                    "ABI seal/target"}
            if str(exc) in central_reason:
                observed = central_reason[str(exc)]
            else:
                raise
        if observed is None:
            raise MutationAccepted("accepted mutation:" + name)
        expected = p0["mutation_expected_reasons"][name]
        if observed != expected:
            raise InputStop("mutation wrong first reason:" + name + ":" + observed)
        records.append({"name": name, "changed_field": owner,
                        "expected_gate": expected,
                        "observed_reason": observed,
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
            "ordinary mutation matrix")
    return records


def load_engine(rel, size, sha, tag_name, meter):
    raw = read_bytes(rel, size, sha, meter, "import:" + tag_name,
                     authority=False)
    path = ROOT / safe_rel(rel)
    module_name = "_task384_v5_producer_" + tag_name
    spec = importlib.util.spec_from_file_location(module_name, path)
    require(spec is not None and spec.loader is not None,
            "import specification:" + tag_name)
    module = importlib.util.module_from_spec(spec)
    require(module_name not in sys.modules,
            "fresh dynamic module name:" + tag_name)
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
    meter.sample_rss("dynamic import boundary:" + tag_name)
    return module


def envelope(terminal, result):
    value = {"schema": RECEIPT_SCHEMA, "status": terminal,
             "terminal": terminal,
             "accepted": terminal in (MEMBER_TOP, NONMEMBER_TOP),
             "result": result}
    value.update({flag: False for flag in FALSE_FLAGS})
    return value


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
            "output must be a direct child of trusted ci/out")
    target = ROOT / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    require(target.parent.is_dir() and not target.parent.is_symlink(),
            "output parent envelope")
    if target.exists() or target.is_symlink():
        raise StaleOutput("stale final output refused")
    prefix = "." + target.name + ".tmp."
    if any(item.name.startswith(prefix) for item in target.parent.iterdir()):
        raise StaleOutput("stale output temp alias refused")
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
                raise OSError(errno.EIO, "short output write")
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
                raise StaleOutput("no-overwrite publication refused")
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
            raise ResourceStop("failure-atomic publication rollback",
                               "serialized_bytes", len(raw),
                               CAPS["serialized_bytes"]) from rollback_error
        if isinstance(exc, (InputStop, ResourceStop, StaleOutput)):
            raise
        raise ResourceStop("failure-atomic publication", "serialized_bytes",
                           len(raw), CAPS["serialized_bytes"])


def release_normal_output_reserve(meter):
    normal = min(NORMAL_OUTPUT_MAX,
                 max(0, meter.reserved["serialized_bytes"] -
                     EMERGENCY_OUTPUT_MAX))
    if normal:
        meter.release("serialized_bytes", normal)


def emergency_unknown(terminal, exc, meter):
    reason = str(exc)[:512]
    if terminal == UNKNOWN_RESOURCE:
        result = {"typed_unknown": terminal,
                  "phase": getattr(exc, "phase", "memory allocation"),
                  "cap": getattr(exc, "cap", "RLIMIT_AS"),
                  "value": getattr(exc, "value", "MemoryError"),
                  "limit": getattr(exc, "limit", CAPS["rss_bytes"]),
                  "reason": reason}
    else:
        result = {"typed_unknown": terminal,
                  "phase": "input/authentication", "reason": reason}
    result["false_conclusion_flags"] = {flag: False for flag in FALSE_FLAGS}
    return envelope(terminal, result)


def production(p0, meter):
    with WallDeadline(meter, "complete authority physical authentication"):
        pins, raw_by_path = authenticate_authority(p0, meter)
    with WallDeadline(meter, "task198 complete authority validation"):
        rows, evaluator_contract, task198_meta, task198_snapshot = \
            authenticate_task198(p0, pins, raw_by_path)
    q3_path = p0["authority"]["task198_evaluator_support"]["q3_receipt"]["path"]
    q3_raw = raw_by_path.pop(q3_path)
    with WallDeadline(meter, "task198 ordinary authority mutation"):
        raw_authority_record = run_raw_authority_mutation(
            p0, raw_by_path, task198_snapshot, meter)
    del task198_snapshot
    raw_by_path.clear()
    del raw_by_path
    meter.sample_rss("task198 raw released after ordinary authority mutation")
    arithmetic = load_engine(*SOURCE_PINS["e4_arithmetic"],
                             "task198_arithmetic", meter)
    joint = load_engine(*SOURCE_PINS["joint_producer"],
                        "task198_joint", meter)
    p176 = load_engine(*SOURCE_PINS["task176_producer"],
                       "task198_task176", meter)
    t198 = load_engine(*SOURCE_PINS["task198_producer"],
                       "task198_evaluator", meter)
    evaluator_runtime = build_task198_runtime(
        arithmetic, joint, p176, q3_raw, meter)
    require(validate_ledger_owner(rows) is True,
            "ordinary task198 ledger baseline")
    g616, g760 = construct_g760()
    validate_g760_owner(g760)
    t226 = load_engine(*SOURCE_PINS["task226_producer"], "task226", meter)
    t227 = load_engine(*SOURCE_PINS["task227_producer"], "task227", meter)
    meter.reserve("base_abi_builds", BASE_BUILD_RESERVE,
                  "computational base ABI reserve")
    try:
        with WallDeadline(meter, "computational base ABI"):
            package = t226.specialize(g760, [], rows)
    except BaseException:
        meter.release("base_abi_builds", BASE_BUILD_RESERVE)
        raise
    meter.consume("base_abi_builds", BASE_BUILD_RESERVE, 1,
                  "computational base ABI")
    meter.sample_rss("computational base ABI boundary")
    full_abi = base_checks(package, rows, g760)
    targets, target_trace = target_from_fox(g760, rows, full_abi)
    central = central_replay(rows, p0)
    with WallDeadline(meter, "accepted task198 six-operation exercise"):
        evaluator_trace = evaluator_exercise(
            evaluator_contract, rows, g760, central, targets, task198_meta,
            t198, evaluator_runtime, meter)
    interface, consumer, seal_trace = make_projection(
        full_abi, rows, targets, task198_meta, evaluator_trace, p0)
    base_ref = base_reference(package, full_abi, g760)
    validate_base_owner(base_ref)
    validate_false_flags({flag: False for flag in FALSE_FLAGS})
    areas = area_canary(t226, g760, rows, targets, meter)
    mutations = run_mutations(rows, p0, g760, interface,
                              consumer, central, areas, base_ref,
                              full_abi,
                              raw_authority_record, meter)
    del package, full_abi, evaluator_contract, evaluator_runtime, q3_raw
    meter.sample_rss("projection and mutation boundary")
    meter.reserve("closure_runs", 1, "single projected closure reserve")
    closure_budget = ClosureBudget(meter)
    try:
        with WallDeadline(meter, "single projected task227 closure"):
            run = t227.closure(consumer, closure_budget, structural=None)
    except BaseException:
        meter.release("closure_runs", 1)
        raise
    meter.consume("closure_runs", 1, 1, "single projected task227 closure")
    meter.sample_rss("task227 closure boundary")
    require(type(run.get("member")) is bool, "task227 terminal Boolean")
    require(len(run.get("ideal_486", [])) == 486 and
            len(run.get("translate_729", [])) == 729,
            "task227 exact 486/729 post-call counts")
    internal_terminal = T227_MEMBER if run["member"] else T227_NONMEMBER
    top_terminal = MEMBER_TOP if run["member"] else NONMEMBER_TOP
    meter.reserve("serialized_bytes", NORMAL_OUTPUT_MAX,
                  "output maximum before gate materialization")
    with WallDeadline(meter, "task227 accepting gate materialization"):
        gate = t227.encode_gate(run)
    gate.update({"terminal": internal_terminal, "phase": "production",
                 "resource": resource_canary("production")})
    gate.update({flag: False for flag in FALSE_FLAGS})
    result = {
        "mode": "PRE_A0_COMPUTATIONAL_BASE_ONLY",
        "correction_word_constructed": False,
        "task192_consumed": False,
        "f_role": "BASE_REFERENCE_EQUAL_TO_G760",
        "g616": {"length": len(g616), "sha256": word_digest(g616)},
        "g760": {"word": g760, "length": len(g760),
                 "sha256": word_digest(g760), "exponent_sums": [0, 0]},
        "base_reference": base_ref,
        "projected_a3_interface_v2": interface,
        "task227_consumer_abi": consumer,
        "projection_seal_trace": seal_trace,
        "central_replay": central,
        "target_trace": target_trace,
        "task198_evaluator_exercise": evaluator_trace,
        "area_canary": areas,
        "mutation_controls": {"baseline": "PASS",
                               "attempted": p0["mutation_roster"],
                               "rejected": mutations},
        "gate": gate,
        "task227_terminal": internal_terminal,
        "rank": run.get("rank"), "block_rank": run.get("block_rank"),
        "ideal_486_count": len(run["ideal_486"]),
        "translate_729_count": len(run["translate_729"]),
        "post_call_exact_counts": {"ideal_rows": 486, "translates": 729,
                                   "closure_calls": 1},
        "resource_formulas": copy.deepcopy(RESOURCE_FORMULAS),
        "authority": {
            "pins": {rel: {"bytes": size, "sha256": sha}
                     for rel, (size, sha) in sorted(pins.items())},
            "p0": {"path": P0_PATH, "bytes": P0_BYTES,
                   "sha256": P0_SHA256,
                   "self_digest_sha256": P0_SELF_SHA256},
            "task198": task198_meta,
            "task227_selftest":
                p0["authority"]["task227_selftest_acceptance"]},
        "false_conclusion_flags": {flag: False for flag in FALSE_FLAGS},
    }
    del run
    meter.sample_rss("pre-serialization boundary")
    return top_terminal, envelope(top_terminal, result)


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--output",
                        default="ci/out/d972_r07_pre_a0_single_target_a3_v5.json")
    args = parser.parse_args(argv)
    meter = Meter()
    try:
        install_linux_hard_limits(meter)
        with WallDeadline(meter, "complete v5 producer route"):
            target = prepare_output(args.output)
            p0 = load_p0(meter)
            terminal, receipt = production(p0, meter)
            raw = seal_fixed_point(receipt, meter, NORMAL_OUTPUT_MAX,
                                   "receipt serialization", pre_reserved=True)
            atomic_publish(target, raw)
        print("D363_PRODUCER_TERMINAL " + terminal, flush=True)
        return 0
    except StaleOutput as exc:
        print("D363_PRODUCER_DIAGNOSTIC stale-output:" + str(exc),
              file=sys.stderr, flush=True)
        return 3
    except MutationAccepted as exc:
        print("D363_PRODUCER_DIAGNOSTIC " + str(exc), file=sys.stderr,
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
        with WallDeadline(meter, "complete v5 producer emergency publication"):
            target = prepare_output(args.output)
            unknown = emergency_unknown(terminal, failure, meter)
            raw = seal_fixed_point(unknown, meter, EMERGENCY_OUTPUT_MAX,
                                   "emergency UNKNOWN serialization",
                                   pre_reserved=True)
            atomic_publish(target, raw)
        print("D363_PRODUCER_TERMINAL " + terminal, flush=True)
        return 2
    except BaseException as emergency:
        print("D363_PRODUCER_DIAGNOSTIC emergency-publication-failed:" +
              str(emergency), file=sys.stderr, flush=True)
        return 5


if __name__ == "__main__":
    raise SystemExit(main())
