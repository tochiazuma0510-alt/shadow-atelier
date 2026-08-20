"""157ek: exact three-field prefix projection repair for the v2 checker.

The mathematical checker is the frozen v2 checker.  This versioned wrapper
authenticates it, installs the sole projection repair at the production global
used by ``check_receipt``, and otherwise delegates without changing the v2
receipt schema, output, predicate, replay, deadlines, or terminal meanings.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import inspect
import sys
from pathlib import Path
from typing import Any, Callable, Sequence


ROOT = Path(__file__).resolve().parents[1]
TASK = Path("sol/luna_task_157ek_b345_lexfirst_block_checker_projection_v3.md")
TASK_SHA = "af5bfe5182e66010fb8893a68ad9f02dda87389171ea425c4122c3fad8addb7c"
TASK_BYTES = 13686

V2_PRODUCER = Path("search/d972_b345_lexfirst_block_target6_v2.py")
V2_PRODUCER_SHA = \
    "ad9a145f1d432afffc4dd3443dafb7d621708543730150636118d1332d83ce8a"
V2_PRODUCER_BYTES = 148824
V2_CHECKER = Path("search/check_d972_b345_lexfirst_block_target6_v2.py")
V2_CHECKER_SHA = \
    "fb28b8b4c7b42f5d83dd1f5c762136812d36731c427a003aae8a8fb0c36a66ba"
V2_CHECKER_BYTES = 130007
V2_DRIVER = Path("search/d972_b345_lexfirst_block_target6_gha_driver_v2.g")
V2_DRIVER_SHA = \
    "48f5717b9be1d6f6087cdf2864d20d41df2475f5d0d87b43c2bd1deefab01394"
V2_DRIVER_BYTES = 13597
V2_TASK = Path("sol/luna_task_157ej_b345_lexfirst_block_target6_v2.md")
V2_TASK_SHA = \
    "1d6f14ef9f799a43fc344daa38606281dbcf0b2fe47d86db0b44df382762f290"
V2_TASK_BYTES = 14667
V2_REPLY = Path("sol/luna_reply_157ej_b345_lexfirst_block_target6_v2.md")
V2_REPLY_SHA = \
    "f00a3f56e140663002e85a488f78b37ade796126928d475f30bb57e951020428"
V2_REPLY_BYTES = 8676

SCHEMA = "d972-b345-lexfirst-block-target6/v2"
OUTPUT = Path("ci/out/d972_b345_lexfirst_block_target6_v2.json")
PREFIX_FIELDS = frozenset({
    "directed_base_support", "directed_surgery", "prefix"})
PREFIX_PUBLIC_FIELDS = (
    "counts", "accounting", "basis_gate", "prefix_pool_checkpoint",
    "dependent_events", "dependent_event_count", "dependent_event_sha256",
    "fresh_not_imported", "source_sha256",
)
V2_MODULE_NAME = "_d972_157ek_frozen_157ej_checker_v2"

FROZEN_INPUTS = {
    "157ek_task": (TASK, TASK_SHA, TASK_BYTES),
    "157ej_v2_producer": (V2_PRODUCER, V2_PRODUCER_SHA, V2_PRODUCER_BYTES),
    "157ej_v2_checker": (V2_CHECKER, V2_CHECKER_SHA, V2_CHECKER_BYTES),
    "157ej_v2_driver": (V2_DRIVER, V2_DRIVER_SHA, V2_DRIVER_BYTES),
    "157ej_v2_task": (V2_TASK, V2_TASK_SHA, V2_TASK_BYTES),
    "157ej_v2_reply": (V2_REPLY, V2_REPLY_SHA, V2_REPLY_BYTES),
}


def require(condition: Any, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def authenticate_wrapper() -> None:
    for label, (path, digest, size) in FROZEN_INPUTS.items():
        full = ROOT/path
        require(full.is_file() and full.stat().st_size == size and
                sha_file(full) == digest, "157ek checker pin: "+label)


def load_v2_checker() -> Any:
    authenticate_wrapper()
    existing = sys.modules.get(V2_MODULE_NAME)
    if existing is not None:
        require(Path(existing.__file__).resolve() == (ROOT/V2_CHECKER).resolve(),
                "157ek loaded v2 checker path")
        return existing
    spec = importlib.util.spec_from_file_location(V2_MODULE_NAME, ROOT/V2_CHECKER)
    require(spec is not None and spec.loader is not None,
            "157ek v2 checker import spec")
    module = importlib.util.module_from_spec(spec)
    sys.modules[V2_MODULE_NAME] = module
    try:
        spec.loader.exec_module(module)
    except Exception:
        sys.modules.pop(V2_MODULE_NAME, None)
        raise
    require(module.SCHEMA == SCHEMA and module.OUTPUT == OUTPUT and
            module.TASK == V2_TASK and module.TASK_SHA == V2_TASK_SHA and
            module.TASK_BYTES == V2_TASK_BYTES and
            module.CURRENT_PRODUCER == V2_PRODUCER and
            module.CURRENT_PRODUCER_SHA == V2_PRODUCER_SHA and
            module.CURRENT_PRODUCER_BYTES == V2_PRODUCER_BYTES and
            set(module.PREFIX_FIELDS) == set(PREFIX_FIELDS),
            "157ek frozen v2 checker public contract")
    # This authenticates every q3/157ec/157ed/157eh/v1 pin owned by v2.
    module.authenticate()
    return module


def validate_prefix_projection(data: dict[str, Any],
                               projected: dict[str, Any]) -> dict[str, Any]:
    """Validate the exact semantic projection consumed by inherited replay."""
    require(isinstance(data, dict) and isinstance(projected, dict),
            "157ek prefix projection mappings")
    for name in PREFIX_FIELDS:
        require(name in data, "157ek prefix projection missing input: "+name)
    require(set(projected) == set(PREFIX_FIELDS),
            "157ek prefix projection exact top-level keys")
    require(isinstance(data["directed_base_support"], dict) and
            bool(data["directed_base_support"]),
            "157ek directed-base-support nonempty mapping")
    require(isinstance(data["directed_surgery"], dict) and
            bool(data["directed_surgery"]),
            "157ek directed-surgery nonempty mapping")
    require(projected["directed_base_support"] ==
                data["directed_base_support"],
            "157ek directed-base-support exact projection")
    require(projected["directed_surgery"] == data["directed_surgery"],
            "157ek directed-surgery exact projection")
    require(isinstance(data["prefix"], dict) and
            all(name in data["prefix"] for name in PREFIX_PUBLIC_FIELDS),
            "157ek prefix projection required nested inputs")
    require(isinstance(projected["prefix"], dict) and
            tuple(projected["prefix"].keys()) == PREFIX_PUBLIC_FIELDS and
            set(projected["prefix"]) == set(PREFIX_PUBLIC_FIELDS),
            "157ek prefix projection exact nested keys")
    require(all(projected["prefix"][name] == data["prefix"][name]
                for name in PREFIX_PUBLIC_FIELDS),
            "157ek prefix exact projected values")
    return projected


def production_prefix_projection(data: dict[str, Any]) -> dict[str, Any]:
    """The sole repaired helper installed at v2's production failing locus."""
    require(isinstance(data, dict), "157ek prefix projection receipt mapping")
    for name in PREFIX_FIELDS:
        require(name in data, "157ek prefix projection missing input: "+name)
    prefix = data["prefix"]
    require(isinstance(prefix, dict), "157ek prefix projection nested mapping")
    for name in PREFIX_PUBLIC_FIELDS:
        require(name in prefix,
                "157ek prefix projection missing nested input: "+name)
    projected = {
        "directed_base_support": data["directed_base_support"],
        "directed_surgery": data["directed_surgery"],
        "prefix": {name: prefix[name] for name in PREFIX_PUBLIC_FIELDS},
    }
    return validate_prefix_projection(data, projected)


def install_projection_repair(v2: Any) -> None:
    """Bind the production global resolved by frozen ``check_receipt``."""
    source = inspect.getsource(v2.check_receipt)
    projection_call = "projected = _project_prefix(data)"
    replay_call = "pool, basis, events = ed.replay_prefix("
    require(source.count(projection_call) == 1 and
            source.count(replay_call) == 1 and
            source.index(projection_call) < source.index(replay_call) and
            "old, projected, e4, normalized, base_key" in source,
            "157ek production projection/replay source-shape recurrence")
    v2._project_prefix = production_prefix_projection
    require(v2._project_prefix is production_prefix_projection,
            "157ek production projector installation")


def check_receipt(q3_path: Path, receipt_path: Path,
                  *, seconds: float = 18_000.0) -> dict[str, Any]:
    v2 = load_v2_checker()
    install_projection_repair(v2)
    return v2.check_receipt(q3_path, receipt_path, seconds=seconds)


def _expect_failure(action: Callable[[], Any], label: str) -> None:
    try:
        action()
    except (KeyError, RuntimeError, TypeError, ValueError):
        return
    raise RuntimeError("157ek mutation accepted: "+label)


def _fixture_receipt_prefix() -> dict[str, Any]:
    return {
        "directed_base_support": {
            "occurrences": [{"relator": 1, "component": 1,
                              "element_hex": "0102"}],
            "occurrence_count": 1,
            "ordered_sha256": "11"*32,
            "order": "relator index, component, canonical E4 bytes",
            "all_prefix_sections_directly_replayed": True,
        },
        "directed_surgery": {
            "translation_count": 1, "translations_sha256": "22"*32},
        "prefix": {name: {"field": name} for name in PREFIX_PUBLIC_FIELDS},
    }


def _fixture_replay(v2: Any, data: dict[str, Any]) -> dict[str, int]:
    """Record the positional production replay ABI and consume all fields."""
    calls: list[tuple[Any, ...]] = []

    class Recorder:
        @staticmethod
        def replay_prefix(*args: Any) -> tuple[None, None, None]:
            calls.append(args)
            require(len(args) == 5, "157ek replay positional arity")
            payload = args[1]
            validate_prefix_projection(data, payload)
            require(payload["directed_base_support"]["occurrence_count"] == 1
                    and payload["directed_surgery"]["translation_count"] == 1
                    and payload["prefix"]["counts"] == {"field": "counts"},
                    "157ek fake replay consumes all three fields")
            return None, None, None

    old = object(); e4 = object(); normalized = {"fixture": True}
    base_key = (object(),)
    projected = v2._project_prefix(data)
    result = Recorder.replay_prefix(old, projected, e4, normalized, base_key)
    require(result == (None, None, None) and len(calls) == 1 and
            calls[0][0] is old and calls[0][1] is projected and
            calls[0][2] is e4 and calls[0][3] is normalized and
            calls[0][4] is base_key,
            "157ek unchanged replay positional arguments")
    return {"prefix_projection_three_keys": 1,
            "directed_base_support_consumed": 1,
            "production_wrapper_entry": 1}


def self_test() -> None:
    v2 = load_v2_checker()
    # Keep all completed/result/resource/input, lifecycle, proof, and 24
    # mutation fixtures from the frozen checker live in this version.
    v2.self_test()
    install_projection_repair(v2)
    data = _fixture_receipt_prefix()
    projected = v2._project_prefix(data)
    require(tuple(projected) ==
            ("directed_base_support", "directed_surgery", "prefix"),
            "157ek canonical projected order")
    counters = _fixture_replay(v2, data)

    omissions = 0
    for name in ("directed_base_support", "directed_surgery", "prefix"):
        bad = copy.deepcopy(data); del bad[name]
        _expect_failure(lambda bad=bad: v2._project_prefix(bad),
                        "missing input "+name)
        omissions += 1

    incident = copy.deepcopy(projected); del incident["directed_base_support"]
    _expect_failure(lambda: validate_prefix_projection(data, incident),
                    "incident two-key projected shape")
    extra = copy.deepcopy(projected); extra["unexpected"] = True
    _expect_failure(lambda: validate_prefix_projection(data, extra),
                    "extra projected key")

    support_mutations = 0
    for replacement in ({}, {"stale": True},
            {**copy.deepcopy(data["directed_base_support"]),
             "occurrence_count": 2}):
        bad = copy.deepcopy(projected)
        bad["directed_base_support"] = replacement
        _expect_failure(lambda bad=bad: validate_prefix_projection(data, bad),
                        "directed-base-support value mutation")
        support_mutations += 1

    bad = copy.deepcopy(projected); del bad["prefix"]["source_sha256"]
    _expect_failure(lambda: validate_prefix_projection(data, bad),
                    "nested prefix omission")
    bad = copy.deepcopy(projected); bad["prefix"]["unexpected"] = 1
    _expect_failure(lambda: validate_prefix_projection(data, bad),
                    "nested prefix extra")

    require(counters == {"prefix_projection_three_keys": 1,
                         "directed_base_support_consumed": 1,
                         "production_wrapper_entry": 1} and
            omissions == 3 and support_mutations == 3,
            "157ek exact projection fixture counters")
    print("D972_B345_LEXBLOCK_TARGET6_V3_CHECKER_SELFTEST_PASS "
          "prefix_projection_three_keys=1 "
          "directed_base_support_consumed=1 "
          "prefix_projection_omissions_rejected=3 "
          "prefix_projection_extra_rejected=1 "
          "prefix_projection_support_mutations_rejected=3 "
          "prefix_projection_nested_mutations_rejected=2 "
          "production_wrapper_entry=1 source_shape_recurrence=1 "
          "inherited_v2_checker=1", flush=True)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--q3", type=Path,
                        default=ROOT/"ci/out/d972_b345_q3_chief_v1.json")
    parser.add_argument("--receipt", type=Path, default=ROOT/OUTPUT)
    parser.add_argument("--seconds", type=float, default=18_000.0)
    args = parser.parse_args(argv)
    if args.self_test:
        self_test()
        return 0
    data = check_receipt(args.q3, args.receipt, seconds=args.seconds)
    print("D972_B345_LEXBLOCK_TARGET6_V3_CHECKER_PASS "
          f"terminal={data['terminal_token']} receipt={args.receipt}",
          flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
