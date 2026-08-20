"""157eh: versioned outer-scoped monitor repair for the 157eg lane.

All mathematical helpers come from the exact frozen v1 producer.  This file
owns only authentication, monitor scoping, the v2 receipt envelope, and the
versioned entry points.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import sys
import tempfile
import time
from collections import defaultdict
from pathlib import Path
from typing import Any, Callable, Sequence

try:
    import resource
except ImportError:  # pragma: no cover - Windows fixture path
    resource = None  # type: ignore[assignment]


ROOT = Path(__file__).resolve().parents[1]
TASK = Path("sol/luna_task_157eh_b345_full_d2_monitor_scope_repair.md")
TASK_SHA = "5d8da27e3997b261c004bb2fb4a40e9416bed39536816ab2fca9f3a9935c095e"
TASK_BYTES = 15015
SCHEMA = "d972-b345-full-d2-dual-correlation/v2"
OUTPUT = Path("ci/out/d972_b345_full_d2_dual_correlation_v2.json")

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

REPAIR_INPUTS = {
    "157eh_task": (TASK, TASK_SHA, TASK_BYTES),
    "157eg_producer": (V1_PRODUCER, V1_PRODUCER_SHA, V1_PRODUCER_BYTES),
    "157eg_checker": (V1_CHECKER, V1_CHECKER_SHA, V1_CHECKER_BYTES),
    "157eg_driver": (V1_DRIVER, V1_DRIVER_SHA, V1_DRIVER_BYTES),
    "157eg_task": (V1_TASK, V1_TASK_SHA, V1_TASK_BYTES),
    "157eg_reply": (V1_REPLY, V1_REPLY_SHA, V1_REPLY_BYTES),
}

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
    return {name: {"path": path.as_posix(), "sha256": digest, "bytes": size}
            for name, (path, digest, size) in REPAIR_INPUTS.items()}


def authenticate_static() -> None:
    for name, (path, digest, size) in REPAIR_INPUTS.items():
        full = ROOT/path
        if not full.is_file() or full.stat().st_size != size or \
                sha_file(full) != digest:
            raise RuntimeError(f"157eh authenticated pin drift: {name}")


_V1_RUNTIME: Any | None = None


def load_v1() -> Any:
    global _V1_RUNTIME
    authenticate_static()
    if _V1_RUNTIME is not None:
        return _V1_RUNTIME
    spec = importlib.util.spec_from_file_location(
        "_d972_157eh_frozen_157eg_producer", ROOT/V1_PRODUCER)
    require(spec is not None and spec.loader is not None, "157eg producer spec")
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
            "157eg frozen local caps")
    _V1_RUNTIME = module
    return module


def current_rss() -> int:
    try:
        with open("/proc/self/status", "r", encoding="ascii") as stream:
            for line in stream:
                if line.startswith("VmRSS:"):
                    return int(line.split()[1])*1024
    except (OSError, ValueError, IndexError):
        pass
    if resource is None:
        return 0
    value = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    return value if sys.platform == "darwin" else value*1024


class ScopedResource(RuntimeError):
    def __init__(self, key: str, limit: int, observed: int, relation: str,
                 outer: str, current: dict[str, Any], *,
                 cap_source: str = "local", inner: str | None = None,
                 callback_api: str | None = None) -> None:
        super().__init__(key)
        require(relation in {"gt", "ge"}, "v2 resource comparator")
        require(cap_source in {"local", "upstream"}, "v2 cap source")
        if cap_source == "local":
            require(key in LOCAL_CAPS and LOCAL_CAPS[key] == int(limit),
                    "v2 local resource cap")
        if inner is None:
            require(callback_api is None, "v2 absent inner callback")
        else:
            require(outer in MONITOR_REGISTRY_FROZEN and
                    inner in MONITOR_REGISTRY_FROZEN[outer] and
                    callback_api in {"check", "reserve"},
                    "v2 resource callback pair")
        self.key = key
        self.limit = int(limit)
        self.observed = int(observed)
        self.relation = relation
        self.phase = outer
        self.current = current
        self.cap_source = cap_source
        self.inner = inner
        self.callback_api = callback_api

    def public(self) -> dict[str, Any]:
        return {"cap_reason": self.key, "cap_key": self.key,
            "cap_source": self.cap_source, "cap_limit": self.limit,
            "observed_count": self.observed, "comparator": self.relation,
            "phase": self.phase, "current": self.current}

    def diagnostic(self) -> dict[str, str] | None:
        if self.inner is None:
            return None
        return {"outer": self.phase, "inner": self.inner,
                "api": str(self.callback_api)}


class Monitor:
    """One clock/RSS/check state; imported callbacks require BoundMonitor."""

    def __init__(self, seconds: float = 18_000.0) -> None:
        require(0 < seconds <= LOCAL_CAPS["common_math_soft_deadline_seconds"],
                "v2 common producer deadline")
        self.started = time.monotonic()
        self.deadline = self.started+float(seconds)
        self.initial_seconds = float(seconds)
        self.checks = 0
        self.peak_rss_bytes = 0
        self.hit_reason: str | None = None
        self.callback_counts: dict[tuple[str, str, str], int] = defaultdict(int)
        self.last_callback: tuple[str, str, str] | None = None

    def bind(self, outer: str) -> "BoundMonitor":
        return BoundMonitor(self, outer)

    def _pair(self, outer: str, inner: str, api: str) -> None:
        require(outer in MONITOR_REGISTRY_FROZEN and
                inner in MONITOR_REGISTRY_FROZEN[outer] and
                api in {"check", "reserve"}, "v2 exact monitor pair")
        self.callback_counts[(outer, inner, api)] += 1
        self.last_callback = (outer, inner, api)

    def _sample(self, outer: str, inner: str, api: str,
                force: bool = False) -> None:
        self._pair(outer, inner, api)
        self.checks += 1
        if not force and self.checks & 63:
            return
        rss = current_rss()
        self.peak_rss_bytes = max(self.peak_rss_bytes, rss)
        if rss >= LOCAL_CAPS["producer_soft_rss_bytes"]:
            self.hit_reason = "producer_soft_rss_bytes"
            raise ScopedResource(self.hit_reason, LOCAL_CAPS[self.hit_reason],
                rss, "ge", outer, {}, inner=inner, callback_api=api)
        if time.monotonic() >= self.deadline:
            self.hit_reason = "common_math_soft_deadline_seconds"
            elapsed = max(LOCAL_CAPS[self.hit_reason],
                          int(time.monotonic()-self.started))
            raise ScopedResource(self.hit_reason, LOCAL_CAPS[self.hit_reason],
                elapsed, "ge", outer, {}, inner=inner, callback_api=api)

    def _reserve(self, outer: str, inner: str, additional_bytes: int) -> None:
        require(isinstance(additional_bytes, int) and additional_bytes >= 0,
                "v2 RSS reservation")
        self._pair(outer, inner, "reserve")
        rss = current_rss()
        self.peak_rss_bytes = max(self.peak_rss_bytes, rss)
        attempted = rss+additional_bytes
        if attempted >= LOCAL_CAPS["producer_soft_rss_bytes"]:
            self.hit_reason = "producer_soft_rss_bytes"
            raise ScopedResource(self.hit_reason, LOCAL_CAPS[self.hit_reason],
                attempted, "ge", outer, {}, inner=inner,
                callback_api="reserve")
        self.checks += 1
        if time.monotonic() >= self.deadline:
            self.hit_reason = "common_math_soft_deadline_seconds"
            elapsed = max(LOCAL_CAPS[self.hit_reason],
                          int(time.monotonic()-self.started))
            raise ScopedResource(self.hit_reason, LOCAL_CAPS[self.hit_reason],
                elapsed, "ge", outer, {}, inner=inner,
                callback_api="reserve")

    def check(self, outer: str, *, force: bool = False, **_: Any) -> None:
        require(outer in MONITOR_REGISTRY_FROZEN and
                MONITOR_REGISTRY_FROZEN[outer] == frozenset({outer}),
                "v2 explicit owned outer")
        self._sample(outer, outer, "check", force)

    def public(self) -> dict[str, Any]:
        return {"initial_remaining_seconds": self.initial_seconds,
            "elapsed_seconds": time.monotonic()-self.started,
            "remaining_seconds": max(0.0, self.deadline-time.monotonic()),
            "checks": self.checks, "peak_rss_bytes": self.peak_rss_bytes,
            "hit_reason": self.hit_reason}


class BoundMonitor:
    """Immutable exact outer scope over a single Monitor state."""

    __slots__ = ("_base", "_outer", "_allowed", "_sealed")

    def __init__(self, base: Monitor, outer: str) -> None:
        require(type(base) is Monitor and outer in MONITOR_REGISTRY_FROZEN,
                "v2 bound monitor construction")
        object.__setattr__(self, "_base", base)
        object.__setattr__(self, "_outer", outer)
        object.__setattr__(self, "_allowed", MONITOR_REGISTRY_FROZEN[outer])
        object.__setattr__(self, "_sealed", True)

    def __setattr__(self, name: str, value: Any) -> None:
        if getattr(self, "_sealed", False):
            raise AttributeError("v2 bound monitor is immutable")
        object.__setattr__(self, name, value)

    @property
    def started(self) -> float:
        return self._base.started

    @property
    def deadline(self) -> float:
        return self._base.deadline

    @property
    def outer(self) -> str:
        return self._outer

    def check(self, inner: str, force: bool = False, **_: Any) -> None:
        require(inner in self._allowed, "v2 bound monitor inner")
        self._base._sample(self._outer, inner, "check", force)

    def reserve(self, inner: str, additional_bytes: int) -> None:
        require(inner in self._allowed, "v2 bound monitor reserve inner")
        self._base._reserve(self._outer, inner, additional_bytes)


def monitor_scope_record(detached: bool,
                         diagnostic: dict[str, str] | None = None) \
        -> dict[str, Any]:
    return {"contract": "one-base-clock-and-immutable-outer-adapters/v2",
        "registry": MONITOR_REGISTRY,
        "registry_sha256": MONITOR_REGISTRY_SHA,
        "registered_pair_count": sum(map(len, MONITOR_REGISTRY.values())),
        "repair_inputs": repair_input_rows(),
        "fresh_adapter_detached_after_prefix": bool(detached),
        "resource_callback": diagnostic,
        "receipt_serialization_is_not_monitor_pair": True,
        "inner_string_never_selects_outer": True,
        "deadline_or_RSS_epoch_reset": False}


def project_v1(receipt: dict[str, Any], v1: Any) -> dict[str, Any]:
    projected = json.loads(json.dumps(receipt))
    require("monitor_scope" in projected, "v2 monitor scope field")
    del projected["monitor_scope"]
    projected["schema"] = v1.SCHEMA
    projected["task_sha256"] = v1.TASK_SHA
    return projected


def validate_monitor_scope(receipt: dict[str, Any]) -> None:
    scope = receipt["monitor_scope"]
    require(set(scope) == {"contract", "registry", "registry_sha256",
            "registered_pair_count", "repair_inputs",
            "fresh_adapter_detached_after_prefix", "resource_callback",
            "receipt_serialization_is_not_monitor_pair",
            "inner_string_never_selects_outer", "deadline_or_RSS_epoch_reset"} and
            scope["contract"] ==
                "one-base-clock-and-immutable-outer-adapters/v2" and
            scope["registry"] == MONITOR_REGISTRY and
            scope["registry_sha256"] == MONITOR_REGISTRY_SHA and
            scope["registered_pair_count"] ==
                sum(map(len, MONITOR_REGISTRY.values())) and
            scope["repair_inputs"] == repair_input_rows() and
            scope["receipt_serialization_is_not_monitor_pair"] is True and
            scope["inner_string_never_selects_outer"] is True and
            scope["deadline_or_RSS_epoch_reset"] is False and
            scope["fresh_adapter_detached_after_prefix"] is
                bool(receipt["prefix"]), "v2 exact monitor scope")
    diagnostic = scope["resource_callback"]
    resource = receipt["resource_guards"]["resource"]
    monitor_resource = (receipt["terminal_token"] ==
        "B345_E4_FULL_D2_UNKNOWN_RESOURCE" and isinstance(resource, dict) and
        resource.get("cap_source") == "local" and resource.get("cap_key") in
        {"common_math_soft_deadline_seconds", "producer_soft_rss_bytes"})
    if monitor_resource:
        require(isinstance(diagnostic, dict) and set(diagnostic) ==
                {"outer", "inner", "api"} and
                diagnostic["outer"] == receipt["phase"] and
                diagnostic["outer"] in MONITOR_REGISTRY_FROZEN and
                diagnostic["inner"] in
                    MONITOR_REGISTRY_FROZEN[diagnostic["outer"]] and
                diagnostic["api"] in {"check", "reserve"},
                "v2 monitor resource diagnostic")
    else:
        require(diagnostic is None, "v2 nonmonitor resource diagnostic")


def validate_receipt_schema(receipt: dict[str, Any], v1: Any, *,
                            fixture: bool = False) -> None:
    require(receipt.get("schema") == SCHEMA and
            receipt.get("task_sha256") == TASK_SHA and
            set(receipt) == set(v1.TOP_KEYS) | {"monitor_scope"},
            "v2 receipt envelope")
    validate_monitor_scope(receipt)
    v1.validate_receipt_schema(project_v1(receipt, v1), fixture=fixture)


def promote_v2(receipt: dict[str, Any], detached: bool = False,
               diagnostic: dict[str, str] | None = None) -> dict[str, Any]:
    receipt["schema"] = SCHEMA
    receipt["task_sha256"] = TASK_SHA
    receipt["monitor_scope"] = monitor_scope_record(detached, diagnostic)
    return receipt


def empty_receipt(v1: Any, monitor: Monitor,
                  upstream: dict[str, int]) -> dict[str, Any]:
    return promote_v2(v1.empty_receipt(monitor, upstream))


def convert_upstream(exc: Any, v1: Any, ed: Any, outer: str) -> ScopedResource:
    registry = v1.upstream_caps(ed)
    key = str(getattr(exc, "cap_key", ""))
    reason = str(getattr(exc, "reason", ""))
    limit = int(getattr(exc, "cap_limit", -1))
    observed = int(getattr(exc, "observed_count", -1))
    relation = str(getattr(exc, "trigger_relation", "gt"))
    require(key in registry and registry[key] == limit and reason == key,
            "v2 closed inherited resource")
    return ScopedResource(key, limit, observed, relation, outer, {},
                          cap_source="upstream")


def detach_prefix_monitors(prefix: dict[str, Any],
                           fresh: BoundMonitor) -> None:
    require(prefix["dag"].deadline is fresh and
            prefix["basis"].deadline is fresh,
            "v2 fresh adapter retained at prefix return")
    prefix["dag"].deadline = None
    prefix["basis"].deadline = None
    require(prefix["dag"].deadline is None and
            prefix["basis"].deadline is None,
            "v2 prefix monitor detach")


def require_prefix_detached(prefix: dict[str, Any]) -> None:
    require(prefix["dag"].deadline is None and
            prefix["basis"].deadline is None,
            "v2 later prefix monitor remains detached")


def run(q3_path: Path, *, seconds: float = 18_000.0,
        v1_module: Any | None = None) -> dict[str, Any]:
    authenticate_static()
    monitor = Monitor(seconds)
    v1 = load_v1() if v1_module is None else v1_module
    phase_started = time.monotonic()
    phases: dict[str, float] = {}
    phase = "authenticated_input"
    ed: Any = None
    old: Any = None
    prefix: dict[str, Any] | None = None
    upstream: dict[str, int] = {}
    receipt = empty_receipt(v1, monitor, upstream)

    def close_phase(label: str) -> None:
        nonlocal phase_started
        now = time.monotonic()
        phases[label] = now-phase_started
        phase_started = now
        print(f"D972_B345_FULL_D2_DUAL_CORRELATION_V2_PHASE {label} "
              f"elapsed_s={phases[label]:.6f}", flush=True)

    try:
        ed = v1.load_ed()
        upstream = v1.upstream_caps(ed)
        receipt = empty_receipt(v1, monitor, upstream)
        if q3_path.resolve() != (ROOT/v1.Q3_PATH).resolve() or \
                not q3_path.is_file() or sha_file(q3_path) != v1.Q3_SHA:
            raise v1.InputFailure("q3 artifact path/SHA drift")
        try:
            q3, old = ed.authenticated_input(q3_path)
        except ed.AffineInput as exc:
            raise v1.InputFailure(str(exc)) from exc
        e3, e4, _ = old.reconstruct_quotients(q3)
        receipt["base_q3_replay"] = old.replay_base_q3(q3, e3, e4)
        normalized, raw_source_key, inverse_words = \
            old.normalized_inverse_fibre(q3, e4)
        receipt["normalized_inverse_fibre"] = normalized
        require(e4.degree == 144 and e4.pc.n == 10, "v2 E4 width 154")
        # This owned boundary accounts for the stage.  The first non-forced
        # check cannot raise, so v1's intentionally unchanged RESOURCE stage
        # projection remains exact; the immediately following fresh forced
        # check samples the same absolute clock/RSS state.
        monitor.check("authenticated_input")
        close_phase("authenticated_input")

        phase = "fresh_immutable_prefix"
        fresh = monitor.bind(phase)
        fresh.check(phase, force=True)
        try:
            prefix, dependent = ed.build_instrumented_prefix(
                old, e4, fresh, raw_source_key)
        except ScopedResource:
            raise
        except (old.ResourceStop, ed.ResourceStop) as exc:
            raise convert_upstream(exc, v1, ed, phase) from exc
        detach_prefix_monitors(prefix, fresh)
        pool = prefix["pool"]
        require(len(pool.values) == v1.PREFIX_POOL_CHECKPOINT and
                tuple(prefix["raw_source_tuple"]) == tuple(raw_source_key) and
                tuple(pool.value(i) for i in prefix["base_source_key"]) ==
                    tuple(raw_source_key), "v2 prefix pool/source anchors")
        receipt["directed_base_support"] = prefix["directed_base_support"]
        receipt["directed_surgery"] = prefix["directed_surgery"]
        require(prefix["directed_surgery"]["stable_rounds_projection_sha256"] ==
                    v1.PREFIX_STABLE_SHA and
                prefix["directed_surgery"]["translations_sha256"] ==
                    v1.PREFIX_TRANSLATIONS_SHA and
                prefix["directed_surgery"]["columns_sha256"] ==
                    v1.PREFIX_COLUMNS_SHA and
                prefix["directed_surgery"]["blocker_history_sha256"] ==
                    v1.PREFIX_BLOCKERS_SHA, "v2 fresh directed prefix")
        receipt["prefix"] = {"counts": v1.PREFIX_COUNTS,
            "accounting": prefix["accounting"],
            "basis_gate": old.affine_basis_gate(prefix["basis"], pool),
            "prefix_pool_checkpoint": len(pool.values),
            "dependent_events": dependent,
            "dependent_event_count": len(dependent),
            "dependent_event_sha256": v1.sha_obj(dependent),
            "fresh_not_imported": True, "source_sha256": ed.STRONG_SHA}
        close_phase(phase)

        phase = "raw_lambda_oracle"
        require_prefix_detached(prefix)
        raw_monitor = monitor.bind(phase)
        raw_monitor.check(phase, force=True)
        try:
            qstar = ed.validate_qstar_label(ed.QSTAR_LABEL, 154)
            oracle = ed.RawLambdaOracle(old, prefix, qstar, raw_monitor)
        except ScopedResource:
            raise
        except (old.ResourceStop, ed.ResourceStop) as exc:
            raise convert_upstream(exc, v1, ed, phase) from exc
        pivot_zero = []
        for pivot in sorted(prefix["basis"].rows, key=pool.pivot_order):
            row_data = prefix["basis"].rows[pivot]
            row = row_data[0] if isinstance(row_data, tuple) else row_data
            pivot_zero.append(oracle.packed(row))
        require(pivot_zero == [0]*v1.PREFIX_COUNTS["pivots"],
                "v2 lambda pivots zero")
        dependent_zero = []
        for event in dependent:
            packed: dict[int, int] = {}
            for component, value_hex, coefficient in event["raw_column"]:
                identifier = pool.ids.get(bytes.fromhex(value_hex))
                require(identifier is not None, "v2 dependent pool key")
                packed[old.pack_vector_key(component, identifier)] = coefficient
            require(oracle.packed(packed) == 0, "v2 lambda dependent zero")
            dependent_zero.append(0)
        r0 = old.word_substitute(old.embed_f2_pb3(
            old.hexagon_words(old.FIXED_WORD)[0]), old.cofaces(3)[0])
        r0_raw, r0_value, _ = old.fox_gradient(r0, e4)
        require(r0_value == e4.identity and oracle.sparse(r0_raw) == 2,
                "v2 base target6 lambda")
        oracle.public.update({"pivot_annihilation_count": len(pivot_zero),
            "pivot_annihilation_sha256": v1.sha_obj(pivot_zero),
            "dependent_annihilation_count": len(dependent_zero),
            "dependent_annihilation_sha256": v1.sha_obj(dependent_zero),
            "base_target6_lambda": 2,
            "base_target6_name": "hexagon_1_coface_0"})
        receipt["lambda_oracle"] = oracle.public
        support = v1.lambda_support(oracle, 154)
        receipt["lambda_support"] = support
        close_phase(phase)

        phase = "base_columns"
        require_prefix_detached(prefix)
        monitor.check(phase, force=True)
        bundle = v1.rebuild_base_bundle(old, prefix, e4)
        receipt["base_columns"] = bundle["public"]
        close_phase(phase)

        phase = "dual_correlation"
        require_prefix_detached(prefix)
        monitor.check(phase, force=True)
        before = v1.state_snapshot(prefix)
        mul, inverse = v1.uncached_ops(old, e4)
        corr = v1.exact_correlation(support["rows"],
            bundle["private_occurrences"], width=154, unpack=pool.unpack,
            mul=mul, inverse=inverse, pack=pool.pack, monitor=monitor)
        canaries = v1.correlation_canaries(corr, support["rows"],
            bundle["private_occurrences"], width=154, identity=e4.identity,
            unpack=pool.unpack, mul=mul, pack=pool.pack)
        after = v1.state_snapshot(prefix)
        require(before == after, "v2 correlation persistent neutrality")
        receipt["state_no_mutation"] = {"before": v1.public_snapshot(before),
            "after": v1.public_snapshot(after), "exact_equal": True,
            "helper_signature_excludes_pool_basis_DAG_sections": True,
            "pool_ID_reuse_or_intern_calls": 0, "E4_cache_path_used": False}
        receipt["direct_canaries"] = canaries
        receipt["correlation"] = corr["public"]
        close_phase(phase)

        phase = "section_witness"
        require_prefix_detached(prefix)
        section_monitor = monitor.bind(phase)
        section_monitor.check(phase, force=True)
        try:
            witness = v1.make_section_witness(old, e4, prefix,
                bundle["private_occurrences"], corr, section_monitor)
        except ScopedResource:
            raise
        except (old.ResourceStop, ed.ResourceStop) as exc:
            raise convert_upstream(exc, v1, ed, phase) from exc
        require_prefix_detached(prefix)
        receipt["section_witness"] = witness
        active = corr["public"]["active_count"] > 0
        receipt["terminal_token"] = receipt["status"] = (
            "B345_E4_FULL_D2_ACTIVE_TRANSLATION" if active else
            "B345_E4_FULL_D2_QSTAR_SEPARATOR")
        receipt["reason"] = ("complete_correlation_has_nonzero_translation"
                             if active else
                             "complete_correlation_all_translates_zero")
        receipt["claim"] = ("first_active_full_D2_translation_exported_not_a_lift"
                            if active else
                            "qstar_separates_base_target6_from_full_D2_for_pinned_E4_roof")
        receipt["phase"] = "complete"
        close_phase(phase)
    except v1.InputFailure as exc:
        if not upstream and ed is not None:
            upstream = v1.upstream_caps(ed)
        receipt = empty_receipt(v1, monitor, upstream)
        receipt["terminal_token"] = receipt["status"] = \
            "B345_E4_FULL_D2_UNKNOWN_INPUT"
        receipt["reason"] = "authenticated_input_failure"
        receipt["claim"] = "none"
        receipt["phase"] = "authenticated_input"
        receipt["input_errors"] = [str(exc)]
    except (ScopedResource, v1.CorrelationResource) as exc:
        monitor.hit_reason = exc.key
        receipt["terminal_token"] = receipt["status"] = \
            "B345_E4_FULL_D2_UNKNOWN_RESOURCE"
        receipt["reason"] = exc.key
        receipt["claim"] = "none"
        receipt["phase"] = exc.phase
        receipt["correlation"] = {}
        receipt["section_witness"] = {}
        receipt["direct_canaries"] = {}
        receipt["state_no_mutation"] = {}
        receipt["resource_guards"] = {"resource_hit": True,
            "resource": exc.public(), "atomic_partial": True}
        receipt["partial"] = {"phase": exc.phase, "current": exc.current,
            "correlation_published": False, "mathematical_claim": "none",
            "rollback_required": False, "reason": exc.key}
        diagnostic = exc.diagnostic() if isinstance(exc, ScopedResource) else None
        receipt["monitor_scope"] = monitor_scope_record(
            bool(receipt["prefix"]), diagnostic)
    receipt["performance"].update(monitor.public())
    receipt["performance"]["phase_seconds"] = phases
    if receipt["monitor_scope"]["resource_callback"] is None:
        receipt["monitor_scope"] = monitor_scope_record(bool(receipt["prefix"]))
    validate_receipt_schema(receipt, v1)
    return receipt


def write_checked(path: Path, receipt: dict[str, Any], v1: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    for _ in range(8):
        raw = (json.dumps(receipt, sort_keys=True,
            separators=(",", ":"))+"\n").encode("utf-8")
        size = len(raw)
        if receipt["performance"]["receipt_bytes"] == size:
            break
        receipt["performance"]["receipt_bytes"] = size
    raw = (json.dumps(receipt, sort_keys=True,
        separators=(",", ":"))+"\n").encode("utf-8")
    require(len(raw) == receipt["performance"]["receipt_bytes"],
            "v2 receipt byte fixed point")
    if len(raw) > v1.CAPS["packed_receipt_bytes"]:
        raise ScopedResource("packed_receipt_bytes",
            v1.CAPS["packed_receipt_bytes"], len(raw), "gt",
            "receipt_serialization", {})
    temporary = path.with_suffix(path.suffix+".tmp")
    temporary.write_bytes(raw)
    require(temporary.read_bytes() == raw, "v2 receipt temp readback")
    os.replace(temporary, path)
    require(path.read_bytes() == raw, "v2 receipt final readback")


def finalize_serialization_resource(receipt: dict[str, Any],
                                    exc: ScopedResource, v1: Any,
                                    *, fixture: bool = False) -> None:
    require(exc.key == "packed_receipt_bytes" and exc.inner is None and
            exc.phase == "receipt_serialization", "v2 serialization selector")
    receipt["terminal_token"] = receipt["status"] = \
        "B345_E4_FULL_D2_UNKNOWN_RESOURCE"
    receipt["reason"] = exc.key
    receipt["claim"] = "none"
    receipt["phase"] = exc.phase
    for name in ("correlation", "section_witness", "direct_canaries",
                 "state_no_mutation"):
        receipt[name] = {}
    receipt["resource_guards"] = {"resource_hit": True,
        "resource": exc.public(), "atomic_partial": True}
    receipt["partial"] = {"phase": exc.phase, "current": {},
        "correlation_published": False, "mathematical_claim": "none",
        "rollback_required": False, "reason": exc.key}
    receipt["performance"]["hit_reason"] = exc.key
    receipt["monitor_scope"] = monitor_scope_record(bool(receipt["prefix"]))
    validate_receipt_schema(receipt, v1, fixture=fixture)


def write_with_resource_fallback(path: Path, receipt: dict[str, Any], v1: Any,
                                 *, fixture: bool = False) -> bool:
    try:
        write_checked(path, receipt, v1)
        return False
    except ScopedResource as exc:
        finalize_serialization_resource(receipt, exc, v1, fixture=fixture)
        write_checked(path, receipt, v1)
        return True


def expect_failure(action: Callable[[], Any], label: str) -> None:
    try:
        action()
    except (RuntimeError, ValueError, AttributeError):
        return
    raise RuntimeError(f"v2 selftest mutation accepted: {label}")


def _perm_mul(left: bytes, right: bytes) -> bytes:
    return bytes(left[right[i]] for i in range(len(left)))


def _perm_inv(value: bytes) -> bytes:
    out = bytearray(len(value))
    for index, image in enumerate(value):
        out[image] = index
    return bytes(out)


def _toy_old_state(old: Any, fresh: BoundMonitor) -> tuple[Any, Any, Any, int]:
    one = bytes((0, 1, 2))
    r = bytes((1, 2, 0))
    s = bytes((1, 0, 2))

    class ToyPC:
        n = 0

    class ToyQ:
        degree = 3
        rank = 6
        def __init__(self) -> None:
            self.pc = ToyPC()
            self.identity = (one, b"")
            self.generators = [(r, b""), (s, b"")] + [self.identity]*4
            self.inverse_generators = [self.inverse(x) for x in self.generators]
        @staticmethod
        def mul(a: Any, b: Any) -> Any:
            return _perm_mul(a[0], b[0]), b""
        @staticmethod
        def inverse(a: Any) -> Any:
            return _perm_inv(a[0]), b""
        def eval(self, word: Sequence[int], images: Sequence[Any] | None = None) -> Any:
            marked = self.generators if images is None else images
            value = self.identity
            for letter in word:
                step = marked[abs(letter)-1]
                value = self.mul(value, step if letter > 0 else self.inverse(step))
            return value

    pool = old.ElementPool(ToyQ())
    sections = old.SparseSectionOracle(pool)
    dag = old.ProvenanceDAG(fresh)
    key = old.pack_vector_key(1, pool.identity_id)
    basis = old.SparseBoundaryBasis(pool, [{key: 1}], dag, sections, fresh)
    return pool, sections, basis, key


def loaded_ed_fixture_module(v1: Any) -> Any:
    """Reuse the module intentionally loaded by frozen v1.self_test()."""
    name = "_d972_157eg_pinned_157ed_producer"
    module = sys.modules.get(name)
    expected = (ROOT/v1.ED_PRODUCER).resolve()
    module_file = None if module is None else Path(module.__file__).resolve()
    require(module is not None and module_file == expected and
            expected.is_file() and expected.stat().st_size == 126_942 and
            sha_file(expected) == v1.ED_PRODUCER_SHA and
            callable(getattr(module, "load_pinned_module", None)) and
            getattr(module, "OLD_PRODUCER", None) is not None and
            getattr(module, "OLD_PRODUCER_SHA", None) is not None,
            "v2 fixture reuses exact loaded 157ed producer")
    return module


def self_test() -> None:
    authenticate_static()
    v1 = load_v1()
    v1.self_test()

    all_inner = sorted({inner for rows in MONITOR_REGISTRY.values()
                        for inner in rows})
    base = Monitor(30)
    for outer, rows in MONITOR_REGISTRY.items():
        adapter = base.bind(outer)
        for inner in rows:
            adapter.check(inner)
        for inner in all_inner:
            if inner not in rows:
                expect_failure(lambda adapter=adapter, inner=inner:
                    adapter.check(inner), f"cross pair {outer}/{inner}")
    for dormant in ("affine_remainder", "provenance_dag_growth",
                    "fixed_context_cheap_DP", "proof_DAG_invented"):
        expect_failure(lambda dormant=dormant:
            base.bind("fresh_immutable_prefix").check(dormant), dormant)
    for prefix_only in ("packed_provenance_dag_growth",
                        "packed_pivot_column_elimination",
                        "packed_target_sparse_elimination",
                        "strong_wform_fresh_BFS"):
        expect_failure(lambda prefix_only=prefix_only:
            base.bind("section_witness").check(prefix_only),
            "section prefix-only "+prefix_only)

    shared = Monitor(30)
    fresh = shared.bind("fresh_immutable_prefix")
    section = shared.bind("section_witness")
    started = shared.started
    deadline = shared.deadline
    fresh.check("proof_DAG_array_bytes", force=True)
    section.check("proof_DAG_array_bytes", force=True)
    require(fresh.started == section.started == started and
            fresh.deadline == section.deadline == deadline and
            shared.checks == 2 and shared.last_callback ==
                ("section_witness", "proof_DAG_array_bytes", "check"),
            "v2 shared adapter state")
    expect_failure(lambda:setattr(fresh, "started", started+1),
                   "adapter epoch reset")
    expect_failure(lambda:setattr(section, "deadline", deadline+1),
                   "adapter deadline extension")

    for outer in ("fresh_immutable_prefix", "section_witness"):
        forced = Monitor(30)
        adapter = forced.bind(outer)
        try:
            adapter.reserve("proof_DAG_array_bytes",
                            LOCAL_CAPS["producer_soft_rss_bytes"])
        except ScopedResource as exc:
            require(exc.phase == outer and exc.inner ==
                    "proof_DAG_array_bytes" and exc.callback_api == "reserve",
                    "v2 reserve pinned outer")
        else:
            raise RuntimeError("v2 reserve resource fixture did not stop")
    forced = Monitor(30)
    adapter = forced.bind("section_witness")
    forced.deadline = time.monotonic()-1
    try:
        adapter.check("proof_DAG_base64_complete", force=True)
    except ScopedResource as exc:
        require(exc.phase == "section_witness" and
                exc.inner == "proof_DAG_base64_complete" and
                exc.callback_api == "check", "v2 check pinned outer")
    else:
        raise RuntimeError("v2 deadline fixture did not stop")

    ed = loaded_ed_fixture_module(v1)
    old = ed.load_pinned_module(ed.OLD_PRODUCER, ed.OLD_PRODUCER_SHA,
                                "_d972_157eh_monitor_fixture_old")
    dag_base = Monitor(30)
    dag_base.checks = 63
    dag_fresh = dag_base.bind("fresh_immutable_prefix")
    dag = old.ProvenanceDAG(dag_fresh)
    for _ in range(1023):
        dag.leaf(1, 0)
    require(dag.node_count == 1024 and dag_base.callback_counts[
            ("fresh_immutable_prefix", "packed_provenance_dag_growth",
             "check")] == 1 and dag_base.checks == 64,
            "v2 actual 1024-node provenance callback")

    reducer_base = Monitor(30)
    reducer_fresh = reducer_base.bind("fresh_immutable_prefix")
    pool, sections, basis, key = _toy_old_state(old, reducer_fresh)
    basis.add_column(1, pool.identity_id,
                     sections.node_for(pool.identity_id))
    basis.elimination_operations = 1023
    basis.add_column(1, pool.identity_id,
                     sections.node_for(pool.identity_id))
    basis.elimination_operations = 1023
    root, missing = basis.solve_with_blocker({key: 1})
    require(root is not None and missing is None and
            reducer_base.callback_counts[("fresh_immutable_prefix",
                "packed_pivot_column_elimination", "check")] == 1 and
            reducer_base.callback_counts[("fresh_immutable_prefix",
                "packed_target_sparse_elimination", "check")] == 1,
            "v2 actual packed reducer callbacks")

    expression = sections.expressions
    g = expression.generator(1, "v2_monitor_g")
    inverse_g = expression.inverse(g, "v2_monitor_inverse_g")
    product = expression.product(g, inverse_g, "v2_monitor_product")
    fresh_serial = Monitor(30).bind("fresh_immutable_prefix")
    section_serial = Monitor(30).bind("section_witness")
    expression.serialize_reachable([product], fresh_serial)
    expression.serialize_reachable([product], section_serial)
    for adapter in (fresh_serial, section_serial):
        counts = adapter._base.callback_counts
        for inner, api in (("proof_DAG_array_bytes", "reserve"),
                           ("proof_DAG_base64", "reserve"),
                           ("proof_DAG_base64_complete", "check")):
            require(counts[(adapter.outer, inner, api)] > 0,
                    "v2 actual section serializer callback")

    detach_prefix = {"dag": dag, "basis": basis}
    dag.deadline = reducer_fresh
    basis.deadline = reducer_fresh
    expect_failure(lambda:detach_prefix_monitors(
        detach_prefix, dag_fresh), "stale mismatched prefix adapter")
    dag.deadline = reducer_fresh
    basis.deadline = reducer_fresh
    detach_prefix_monitors(detach_prefix, reducer_fresh)
    before_checks = reducer_base.checks
    basis.elimination_operations = 1023
    basis._cadence("packed_target_sparse_elimination")
    require_prefix_detached(detach_prefix)
    require(reducer_base.checks == before_checks,
            "v2 detached helper cannot callback")

    fixture = promote_v2(v1.empty_receipt(Monitor(30), {}))
    fixture["pins"] = {}
    fixture["terminal_token"] = fixture["status"] = \
        "B345_E4_FULL_D2_UNKNOWN_INPUT"
    fixture["reason"] = "authenticated_input_failure"
    fixture["claim"] = "none"
    fixture["phase"] = "authenticated_input"
    fixture["input_errors"] = ["toy"]
    validate_receipt_schema(fixture, v1, fixture=True)
    bad = json.loads(json.dumps(fixture))
    bad["monitor_scope"]["registry"]["fresh_immutable_prefix"].append(
        "packed_unknown")
    expect_failure(lambda:validate_receipt_schema(bad, v1, fixture=True),
                   "monitor registry mutation")
    bad = json.loads(json.dumps(fixture))
    bad["monitor_scope"]["registry_sha256"] = "0"*64
    expect_failure(lambda:validate_receipt_schema(bad, v1, fixture=True),
                   "monitor digest mutation")
    bad = json.loads(json.dumps(fixture))
    bad["monitor_scope"]["fresh_adapter_detached_after_prefix"] = True
    expect_failure(lambda:validate_receipt_schema(bad, v1, fixture=True),
                   "monitor detached-state mutation")

    print("D972_B345_FULL_D2_DUAL_CORRELATION_V2_PRODUCER_SELFTEST_PASS "
          "registry_pairs=18 shared_clock=1 reserve=1 outer_resources=2 "
          "actual_dag_1024=1 packed_reducers=2 proof_serializers=2 detach=1 "
          "v1_fixture=1", flush=True)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--q3", type=Path, default=ROOT/
                        "ci/out/d972_b345_q3_chief_v1.json")
    parser.add_argument("--output", type=Path, default=ROOT/OUTPUT)
    parser.add_argument("--seconds", type=float, default=18_000.0)
    args = parser.parse_args(argv)
    if args.self_test:
        self_test()
        return 0
    receipt = run(args.q3, seconds=args.seconds)
    v1 = load_v1()
    write_with_resource_fallback(args.output, receipt, v1)
    print("D972_B345_FULL_D2_DUAL_CORRELATION_V2_PRODUCER_PASS "
          f"terminal={receipt['terminal_token']} output={args.output}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
