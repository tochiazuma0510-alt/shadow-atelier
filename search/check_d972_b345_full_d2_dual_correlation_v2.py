"""Independent v2 monitor-scope checker for the frozen 157eg predicate."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
import tempfile
import time
from pathlib import Path
from typing import Any, Callable, Sequence


ROOT = Path(__file__).resolve().parents[1]
TASK = Path("sol/luna_task_157eh_b345_full_d2_monitor_scope_repair.md")
TASK_SHA = "5d8da27e3997b261c004bb2fb4a40e9416bed39536816ab2fca9f3a9935c095e"
TASK_BYTES = 15015
SCHEMA = "d972-b345-full-d2-dual-correlation/v2"
OUTPUT = Path("ci/out/d972_b345_full_d2_dual_correlation_v2.json")
Q3_PATH = Path("ci/out/d972_b345_q3_chief_v1.json")

PRODUCER = Path("search/d972_b345_full_d2_dual_correlation_v2.py")
PRODUCER_SHA = "6557bcfea70c0846158951fafe3d6ef8790479a5c7010db896ed76540dd5ae5f"
PRODUCER_BYTES = 42449
V1_PRODUCER = Path("search/d972_b345_full_d2_dual_correlation_v1.py")
V1_PRODUCER_SHA = "6903b745be2c005c573d7a368beb826d5f411f0f4a353eeedf3a8cccbc9fde52"
V1_PRODUCER_BYTES = 78832
V1_CHECKER = Path("search/check_d972_b345_full_d2_dual_correlation_v1.py")
V1_CHECKER_SHA = "311dc9413012542e489c9b2b7cd38e6008b81b6b8854e5e49d8d56285a457358"
V1_CHECKER_BYTES = 66571
V1_DRIVER = Path("search/d972_b345_full_d2_dual_correlation_gha_driver_v1.g")
V1_DRIVER_SHA = "c0a0626f4ea15616bfef3b5916740c23c86a0f87760a98b0ff3d8da923db65b4"
V1_DRIVER_BYTES = 11980
V1_TASK = Path("sol/luna_task_157eg_b345_full_d2_dual_correlation.md")
V1_TASK_SHA = "22b649c178ea1a821a5d67973b39c58f6a7395b6bc6a407a36a493f9ce19720e"
V1_TASK_BYTES = 16187
V1_REPLY = Path("sol/luna_reply_157eg_b345_full_d2_dual_correlation.md")
V1_REPLY_SHA = "12a1e5feafebe97d694b15c09063a50fac7a471d0528c0f210373c18c9a0445f"
V1_REPLY_BYTES = 9795

PIN_SPECS = {
    "157eh_task": (TASK, TASK_SHA, TASK_BYTES),
    "157eh_producer": (PRODUCER, PRODUCER_SHA, PRODUCER_BYTES),
    "157eg_producer": (V1_PRODUCER, V1_PRODUCER_SHA, V1_PRODUCER_BYTES),
    "157eg_checker": (V1_CHECKER, V1_CHECKER_SHA, V1_CHECKER_BYTES),
    "157eg_driver": (V1_DRIVER, V1_DRIVER_SHA, V1_DRIVER_BYTES),
    "157eg_task": (V1_TASK, V1_TASK_SHA, V1_TASK_BYTES),
    "157eg_reply": (V1_REPLY, V1_REPLY_SHA, V1_REPLY_BYTES),
}

REPAIR_INPUT_LABELS = (
    "157eh_task", "157eg_producer", "157eg_checker", "157eg_driver",
    "157eg_task", "157eg_reply",
)

# Independent literal: never import this table from the producer or receipt.
_REGISTRY_SOURCE = {
    "authenticated_input": {"authenticated_input"},
    "fresh_immutable_prefix": {
        "fresh_immutable_prefix", "strong_wform_fresh_BFS",
        "strong_wform_directed_round", "packed_provenance_dag_growth",
        "packed_pivot_column_elimination", "packed_target_sparse_elimination",
        "proof_DAG_array_bytes", "proof_DAG_base64",
        "proof_DAG_base64_complete",
    },
    "raw_lambda_oracle": {"raw_lambda_oracle", "raw_lambda_reverse_dp"},
    "base_columns": {"base_columns"},
    "dual_correlation": {"dual_correlation"},
    "section_witness": {
        "section_witness", "proof_DAG_array_bytes", "proof_DAG_base64",
        "proof_DAG_base64_complete",
    },
}
MONITOR_REGISTRY = {
    outer: sorted(_REGISTRY_SOURCE[outer]) for outer in sorted(_REGISTRY_SOURCE)
}
MONITOR_REGISTRY_FROZEN = {
    outer: frozenset(rows) for outer, rows in _REGISTRY_SOURCE.items()
}

LOCAL_CAPS = {
    "common_math_soft_deadline_seconds": 18_000,
    "producer_soft_rss_bytes": 4_831_838_208,
    "packed_receipt_bytes": 268_435_456,
}

CHECKER_STARTED: float | None = None
CHECKER_DEADLINE: float | None = None
CHECKER_CHECKS = 0


def require(condition: Any, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha_obj(value: Any) -> str:
    return sha_bytes(json.dumps(value, sort_keys=True,
        separators=(",", ":")).encode("utf-8"))


MONITOR_REGISTRY_SHA = sha_obj(MONITOR_REGISTRY)


def sha_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def repair_input_rows() -> dict[str, dict[str, Any]]:
    return {name: {"path": PIN_SPECS[name][0].as_posix(),
                   "sha256": PIN_SPECS[name][1],
                   "bytes": PIN_SPECS[name][2]}
            for name in REPAIR_INPUT_LABELS}


def authenticate() -> None:
    for name, (path, digest, size) in PIN_SPECS.items():
        full = ROOT/path
        require(full.is_file() and full.stat().st_size == size and
                sha_file(full) == digest, f"157eh checker pin: {name}")


_V1_CHECKER_RUNTIME: Any | None = None


def load_v1_checker() -> Any:
    global _V1_CHECKER_RUNTIME
    authenticate()
    if _V1_CHECKER_RUNTIME is not None:
        return _V1_CHECKER_RUNTIME
    spec = importlib.util.spec_from_file_location(
        "_d972_157eh_frozen_157eg_checker", ROOT/V1_CHECKER)
    require(spec is not None and spec.loader is not None,
            "157eh frozen checker spec")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    try:
        spec.loader.exec_module(module)
    except BaseException:
        sys.modules.pop(spec.name, None)
        raise
    require(module.SCHEMA == "d972-b345-full-d2-dual-correlation/v1" and
            module.CAPS["common_math_soft_deadline_seconds"] ==
                LOCAL_CAPS["common_math_soft_deadline_seconds"] and
            module.CAPS["producer_soft_rss_bytes"] ==
                LOCAL_CAPS["producer_soft_rss_bytes"] and
            module.CAPS["packed_receipt_bytes"] ==
                LOCAL_CAPS["packed_receipt_bytes"],
            "157eh frozen checker caps")
    _V1_CHECKER_RUNTIME = module
    return module


def project_v1(data: dict[str, Any], v1: Any) -> dict[str, Any]:
    projected = json.loads(json.dumps(data))
    require("monitor_scope" in projected, "checker v2 scope field")
    del projected["monitor_scope"]
    projected["schema"] = v1.SCHEMA
    projected["task_sha256"] = v1.TASK_SHA
    return projected


def canonical_receipt_bytes(data: dict[str, Any]) -> bytes:
    for _ in range(16):
        raw = (json.dumps(data, sort_keys=True,
            separators=(",", ":"))+"\n").encode("utf-8")
        if data["performance"]["receipt_bytes"] == len(raw):
            return raw
        data["performance"]["receipt_bytes"] = len(raw)
    raise RuntimeError("checker projected receipt byte fixed point")


def validate_pair(outer: str, inner: str) -> None:
    require(outer in MONITOR_REGISTRY_FROZEN and
            inner in MONITOR_REGISTRY_FROZEN[outer],
            "checker exact outer/inner monitor pair")


def validate_monitor_scope(data: dict[str, Any]) -> None:
    scope = data["monitor_scope"]
    require(set(scope) == {"contract", "registry", "registry_sha256",
            "registered_pair_count", "repair_inputs",
            "fresh_adapter_detached_after_prefix", "resource_callback",
            "receipt_serialization_is_not_monitor_pair",
            "inner_string_never_selects_outer", "deadline_or_RSS_epoch_reset"}
            and scope["contract"] ==
                "one-base-clock-and-immutable-outer-adapters/v2"
            and scope["registry"] == MONITOR_REGISTRY
            and scope["registry_sha256"] == MONITOR_REGISTRY_SHA
            and scope["registered_pair_count"] ==
                sum(map(len, MONITOR_REGISTRY.values()))
            and scope["repair_inputs"] == repair_input_rows()
            and scope["receipt_serialization_is_not_monitor_pair"] is True
            and scope["inner_string_never_selects_outer"] is True
            and scope["deadline_or_RSS_epoch_reset"] is False
            and scope["fresh_adapter_detached_after_prefix"] is
                bool(data["prefix"]), "checker exact monitor-scope envelope")
    diagnostic = scope["resource_callback"]
    resource = data["resource_guards"]["resource"]
    monitor_resource = (data["terminal_token"] ==
        "B345_E4_FULL_D2_UNKNOWN_RESOURCE" and isinstance(resource, dict) and
        resource.get("cap_source") == "local" and resource.get("cap_key") in
        {"common_math_soft_deadline_seconds", "producer_soft_rss_bytes"})
    if monitor_resource:
        require(isinstance(diagnostic, dict) and set(diagnostic) ==
                {"outer", "inner", "api"} and
                diagnostic["outer"] == data["phase"] == resource["phase"] and
                diagnostic["api"] in {"check", "reserve"},
                "checker monitor resource diagnostic")
        validate_pair(diagnostic["outer"], diagnostic["inner"])
    else:
        require(diagnostic is None, "checker nonmonitor resource diagnostic")


def validate_v2_envelope(data: dict[str, Any], v1: Any, *,
                         fixture: bool = False,
                         expected_upstream: dict[str, int] | None = None) -> None:
    require(set(data) == set(v1.TOP_KEYS) | {"monitor_scope"} and
            data.get("schema") == SCHEMA and
            data.get("task_sha256") == TASK_SHA,
            "checker v2 exact top-level envelope")
    validate_monitor_scope(data)
    v1.validate_envelope(project_v1(data, v1), fixture=fixture,
                         expected_upstream=expected_upstream)


def tick(phase: str, force: bool = False) -> None:
    global CHECKER_CHECKS
    CHECKER_CHECKS += 1
    if not force and CHECKER_CHECKS & 63:
        return
    require(CHECKER_DEADLINE is not None and
            time.monotonic() < CHECKER_DEADLINE,
            f"157eh checker soft deadline: {phase}")


def bind_v1_deadline(v1: Any) -> None:
    require(CHECKER_STARTED is not None and CHECKER_DEADLINE is not None and
            0.0 < CHECKER_DEADLINE-time.monotonic() <= 18_000.0,
            "157eh checker common remaining budget")
    v1.CHECKER_STARTED = CHECKER_STARTED
    v1.CHECKER_DEADLINE = CHECKER_DEADLINE
    v1.CHECKER_CHECKS = CHECKER_CHECKS


def check_receipt(q3_path: Path, receipt_path: Path) -> dict[str, Any]:
    v1 = load_v1_checker()
    raw = receipt_path.read_bytes()
    data = json.loads(raw.decode("utf-8"))
    require(raw == (json.dumps(data, sort_keys=True,
            separators=(",", ":"))+"\n").encode("utf-8"),
            "checker v2 canonical JSON")
    validate_v2_envelope(data, v1,
        expected_upstream=data["upstream_caps"]["registry"])
    require(data["performance"]["receipt_bytes"] == len(raw) and
            len(raw) <= LOCAL_CAPS["packed_receipt_bytes"],
            "checker v2 receipt bytes")
    # The frozen checker reconstructs its own upstream registry and all
    # mathematical predicates.  It receives only the v1 projection in a
    # repository-external temporary file.
    projected = project_v1(data, v1)
    projected_raw = canonical_receipt_bytes(projected)
    before_sha = sha_obj(data)
    tick("v2 projection", True)
    bind_v1_deadline(v1)
    with tempfile.TemporaryDirectory(prefix="shadow-atelier-157eh-") as tmp:
        projected_path = Path(tmp)/"d972_b345_full_d2_v1_projection.json"
        projected_path.write_bytes(projected_raw)
        require(projected_path.read_bytes() == projected_raw,
                "checker projected receipt readback")
        checked = v1.check_receipt(q3_path, projected_path)
    require(checked == projected and sha_obj(data) == before_sha and
            v1.CHECKER_DEADLINE == CHECKER_DEADLINE,
            "checker frozen predicate projection/no mutation/deadline")
    tick("v2 complete", True)
    return data


def expect_failure(action: Callable[[], Any], label: str) -> None:
    try:
        action()
    except (RuntimeError, ValueError, AttributeError):
        return
    raise RuntimeError(f"v2 checker mutation accepted: {label}")


class AuditMonitor:
    """Independent bounded adapter model using the checker-owned registry."""

    def __init__(self) -> None:
        self.started = time.monotonic()
        self.deadline = self.started+30.0
        self.checks = 0
        self.peak_rss_bytes = 0
        self.hit_reason: str | None = None
        self.events: list[tuple[str, str, str]] = []

    def bind(self, outer: str) -> "AuditBound":
        return AuditBound(self, outer)

    def event(self, outer: str, inner: str, api: str) -> None:
        validate_pair(outer, inner)
        require(api in {"check", "reserve"}, "checker adapter API")
        self.checks += 1
        self.events.append((outer, inner, api))


class AuditBound:
    __slots__ = ("_base", "_outer", "_sealed")

    def __init__(self, base: AuditMonitor, outer: str) -> None:
        require(type(base) is AuditMonitor and outer in
                MONITOR_REGISTRY_FROZEN, "checker bound adapter construction")
        object.__setattr__(self, "_base", base)
        object.__setattr__(self, "_outer", outer)
        object.__setattr__(self, "_sealed", True)

    def __setattr__(self, name: str, value: Any) -> None:
        if getattr(self, "_sealed", False):
            raise AttributeError("checker bound adapter immutable")
        object.__setattr__(self, name, value)

    @property
    def started(self) -> float:
        return self._base.started

    @property
    def deadline(self) -> float:
        return self._base.deadline

    def check(self, inner: str, force: bool = False, **_: Any) -> None:
        del force
        self._base.event(self._outer, inner, "check")

    def reserve(self, inner: str, additional_bytes: int) -> None:
        require(isinstance(additional_bytes, int) and additional_bytes >= 0,
                "checker adapter reserve")
        self._base.event(self._outer, inner, "reserve")


def promote_fixture(old_data: dict[str, Any], *, detached: bool,
                    diagnostic: dict[str, str] | None = None) -> dict[str, Any]:
    data = json.loads(json.dumps(old_data))
    data["schema"] = SCHEMA
    data["task_sha256"] = TASK_SHA
    data["monitor_scope"] = {
        "contract": "one-base-clock-and-immutable-outer-adapters/v2",
        "registry": MONITOR_REGISTRY,
        "registry_sha256": MONITOR_REGISTRY_SHA,
        "registered_pair_count": sum(map(len, MONITOR_REGISTRY.values())),
        "repair_inputs": repair_input_rows(),
        "fresh_adapter_detached_after_prefix": detached,
        "resource_callback": diagnostic,
        "receipt_serialization_is_not_monitor_pair": True,
        "inner_string_never_selects_outer": True,
        "deadline_or_RSS_epoch_reset": False,
    }
    return data


def unknown_fixture(v1: Any) -> dict[str, Any]:
    data = v1.fixture_envelope({}, False)
    data["terminal_token"] = data["status"] = \
        "B345_E4_FULL_D2_UNKNOWN_INPUT"
    data["reason"] = "authenticated_input_failure"
    data["claim"] = "none"
    data["phase"] = "authenticated_input"
    data["input_errors"] = ["toy"]
    for name in ("base_q3_replay", "normalized_inverse_fibre",
                 "directed_base_support", "directed_surgery", "prefix",
                 "lambda_oracle", "lambda_support", "base_columns",
                 "correlation", "direct_canaries", "state_no_mutation",
                 "section_witness"):
        data[name] = {}
    data["performance"]["phase_seconds"] = {}
    return promote_fixture(data, detached=False)


def monitor_resource_fixture(v1: Any, outer: str, inner: str, api: str,
                             key: str) -> dict[str, Any]:
    data = v1.fixture_envelope({}, False)
    data["terminal_token"] = data["status"] = \
        "B345_E4_FULL_D2_UNKNOWN_RESOURCE"
    data["reason"] = key
    data["claim"] = "none"
    data["phase"] = outer
    completed = {"fresh_immutable_prefix": 2, "raw_lambda_oracle": 5,
        "base_columns": 7, "dual_correlation": 8, "section_witness": 8}
    math_fields = ("base_q3_replay", "normalized_inverse_fibre",
        "directed_base_support", "directed_surgery", "prefix",
        "lambda_oracle", "lambda_support", "base_columns", "correlation",
        "direct_canaries", "state_no_mutation", "section_witness")
    for index, name in enumerate(math_fields):
        data[name] = {"toy": True} if index < completed[outer] else {}
    row = {"cap_reason": key, "cap_key": key, "cap_source": "local",
        "cap_limit": LOCAL_CAPS[key], "observed_count": LOCAL_CAPS[key],
        "comparator": "ge", "phase": outer, "current": {}}
    data["resource_guards"] = {"resource_hit": True, "resource": row,
        "atomic_partial": True}
    data["partial"] = {"phase": outer, "current": {},
        "correlation_published": False, "mathematical_claim": "none",
        "rollback_required": False, "reason": key}
    data["input_errors"] = []
    data["performance"]["hit_reason"] = key
    timed = v1.TIMED_PHASES[:{
        "fresh_immutable_prefix": 1, "raw_lambda_oracle": 2,
        "base_columns": 3, "dual_correlation": 4,
        "section_witness": 5}[outer]]
    data["performance"]["phase_seconds"] = {name: 0.0 for name in timed}
    return promote_fixture(data, detached=bool(data["prefix"]),
        diagnostic={"outer": outer, "inner": inner, "api": api})


def self_test() -> None:
    v1 = load_v1_checker()
    v1.self_test()

    audit = AuditMonitor()
    all_inner = sorted({inner for rows in MONITOR_REGISTRY.values()
                        for inner in rows})
    for outer, rows in MONITOR_REGISTRY.items():
        adapter = audit.bind(outer)
        for inner in rows:
            adapter.check(inner)
        for inner in all_inner:
            if inner not in rows:
                expect_failure(lambda adapter=adapter, inner=inner:
                    adapter.check(inner), f"cross pair {outer}/{inner}")
    fresh = audit.bind("fresh_immutable_prefix")
    section = audit.bind("section_witness")
    started, deadline = audit.started, audit.deadline
    fresh.reserve("proof_DAG_array_bytes", 1)
    section.check("proof_DAG_array_bytes", force=True)
    require(fresh.started == section.started == started and
            fresh.deadline == section.deadline == deadline and
            audit.events[-2:] == [
                ("fresh_immutable_prefix", "proof_DAG_array_bytes", "reserve"),
                ("section_witness", "proof_DAG_array_bytes", "check")],
            "checker shared explicit outer adapters")
    expect_failure(lambda:setattr(fresh, "_outer", "section_witness"),
                   "checker adapter outer mutation")
    for dormant in ("affine_remainder", "provenance_dag_growth",
                    "fixed_context_cheap_DP", "proof_DAG_invented"):
        expect_failure(lambda dormant=dormant:
            fresh.check(dormant), "checker dormant "+dormant)

    unknown = unknown_fixture(v1)
    validate_v2_envelope(unknown, v1, fixture=True)
    fresh_resource = monitor_resource_fixture(v1,
        "fresh_immutable_prefix", "proof_DAG_array_bytes", "reserve",
        "producer_soft_rss_bytes")
    validate_v2_envelope(fresh_resource, v1, fixture=True)
    section_resource = monitor_resource_fixture(v1,
        "section_witness", "proof_DAG_array_bytes", "check",
        "common_math_soft_deadline_seconds")
    validate_v2_envelope(section_resource, v1, fixture=True)

    mutations: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
        ("registry", lambda row: row["monitor_scope"]["registry"][
            "fresh_immutable_prefix"].append("packed_unknown")),
        ("digest", lambda row: row["monitor_scope"].__setitem__(
            "registry_sha256", "0"*64)),
        ("pair count", lambda row: row["monitor_scope"].__setitem__(
            "registered_pair_count", 17)),
        ("stale detach", lambda row: row["monitor_scope"].__setitem__(
            "fresh_adapter_detached_after_prefix", True)),
    ]
    for label, mutate in mutations:
        bad = json.loads(json.dumps(unknown))
        mutate(bad)
        expect_failure(lambda bad=bad:validate_v2_envelope(
            bad, v1, fixture=True), label)
    for label, field, value in (
        ("outer diagnostic", "outer", "fresh_immutable_prefix"),
        ("inner diagnostic", "inner", "packed_pivot_column_elimination"),
        ("API diagnostic", "api", "invented"),
    ):
        bad = json.loads(json.dumps(section_resource))
        bad["monitor_scope"]["resource_callback"][field] = value
        expect_failure(lambda bad=bad:validate_v2_envelope(
            bad, v1, fixture=True), label)
    bad = json.loads(json.dumps(unknown))
    bad["monitor_scope"]["resource_callback"] = {
        "outer": "fresh_immutable_prefix", "inner":
            "packed_provenance_dag_growth", "api": "check"}
    expect_failure(lambda:validate_v2_envelope(bad, v1, fixture=True),
                   "diagnostic on nonresource terminal")

    print("D972_B345_FULL_D2_DUAL_CORRELATION_V2_CHECKER_SELFTEST_PASS "
          "registry_pairs=18 cross_rejections=1 shared_clock=1 check_reserve=1 "
          "duplicate_inner_two_outers=1 outer_inner_mutations=3 stale_detach=1 "
          "v1_production_core=1", flush=True)


def main(argv: Sequence[str] | None = None) -> int:
    global CHECKER_STARTED, CHECKER_DEADLINE, CHECKER_CHECKS
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--q3", type=Path, default=ROOT/Q3_PATH)
    parser.add_argument("--receipt", type=Path, default=ROOT/OUTPUT)
    parser.add_argument("--seconds", type=float, default=18_000.0)
    args = parser.parse_args(argv)
    require(0.0 < args.seconds <= 18_000.0,
            "157eh checker deadline input")
    CHECKER_STARTED = time.monotonic()
    CHECKER_DEADLINE = CHECKER_STARTED+args.seconds
    CHECKER_CHECKS = 0
    if args.self_test:
        self_test()
        return 0
    result = check_receipt(args.q3, args.receipt)
    print("D972_B345_FULL_D2_DUAL_CORRELATION_V2_CHECKER_PASS "
          f"terminal={result['terminal_token']}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
