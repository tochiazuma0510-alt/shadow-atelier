"""157el: completed-anchor accounting type repair for the v2 receipt.

The frozen v3 checker supplies the exact three-key prefix repair and delegates
all mathematics to the frozen v2 checker.  This wrapper changes only the bad
completed-anchor wire: checker-native six-key replay accounting remains the
semantic replay certificate, while the producer's eleven-key public ledger is
passed to the unchanged public anchor validator.
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
TASK = Path("sol/luna_task_157el_b345_lexfirst_block_checker_accounting_v4.md")
TASK_SHA = "755861e724fbd66f88b59b9ad9808703f26e2c8016394cb49c0c9cb09ce1f88a"
TASK_BYTES = 16945

V2_PRODUCER = Path("search/d972_b345_lexfirst_block_target6_v2.py")
V2_PRODUCER_SHA = \
    "ad9a145f1d432afffc4dd3443dafb7d621708543730150636118d1332d83ce8a"
V2_PRODUCER_BYTES = 148824
V2_CHECKER = Path("search/check_d972_b345_lexfirst_block_target6_v2.py")
V2_CHECKER_SHA = \
    "fb28b8b4c7b42f5d83dd1f5c762136812d36731c427a003aae8a8fb0c36a66ba"
V2_CHECKER_BYTES = 130007
V3_CHECKER = Path("search/check_d972_b345_lexfirst_block_target6_v3.py")
V3_CHECKER_SHA = \
    "bc0c1c4dfe2e4bc6ea8fd6c18e3af245d20e0959408649dd61d23f969cba9845"
V3_CHECKER_BYTES = 14032
V3_DRIVER = Path("search/d972_b345_lexfirst_block_target6_gha_driver_v3.g")
V3_DRIVER_SHA = \
    "2637e08c67e48bd0fca41e3b79a68be68344488734123d4043725d5c82971908"
V3_DRIVER_BYTES = 13805
V3_TASK = Path("sol/luna_task_157ek_b345_lexfirst_block_checker_projection_v3.md")
V3_TASK_SHA = \
    "af5bfe5182e66010fb8893a68ad9f02dda87389171ea425c4122c3fad8addb7c"
V3_TASK_BYTES = 13686
V3_REPLY = Path("sol/luna_reply_157ek_b345_lexfirst_block_checker_projection_v3.md")
V3_REPLY_SHA = \
    "accf8cf58f511ebca7b30a1409be02a742a454762220df6c1ea9d9c69eb327b0"
V3_REPLY_BYTES = 8603
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
V3_MODULE_NAME = "_d972_157el_frozen_157ek_checker_v3"
ORIGINAL_ANCHOR_ATTR = "_d972_157el_original_validate_anchor_public"
ORIGINAL_CORE_ATTR = "_d972_157el_original_validate_completed_core"
SEMANTIC_ACCOUNTING_FIELDS = frozenset({
    "columns", "pivots", "dependent", "live_sparse_entries",
    "pool_size", "pool_order_sha256",
})
MATHEMATICAL_ACCOUNTING_FIELDS = (
    "columns", "pivots", "dependent", "live_sparse_entries")
PUBLIC_ACCOUNTING_FIELDS = frozenset({
    *SEMANTIC_ACCOUNTING_FIELDS,
    "DAG_nodes", "DAG_edges", "section_bindings",
    "section_expression_nodes", "section_expression_edges",
})
PUBLIC_ONLY_FIELDS = (
    "DAG_nodes", "DAG_edges", "section_bindings",
    "section_expression_nodes", "section_expression_edges",
)

FROZEN_INPUTS = {
    "157el_task": (TASK, TASK_SHA, TASK_BYTES),
    "157ej_v2_producer": (V2_PRODUCER, V2_PRODUCER_SHA, V2_PRODUCER_BYTES),
    "157ej_v2_checker": (V2_CHECKER, V2_CHECKER_SHA, V2_CHECKER_BYTES),
    "157ek_v3_checker": (V3_CHECKER, V3_CHECKER_SHA, V3_CHECKER_BYTES),
    "157ek_v3_driver": (V3_DRIVER, V3_DRIVER_SHA, V3_DRIVER_BYTES),
    "157ek_v3_task": (V3_TASK, V3_TASK_SHA, V3_TASK_BYTES),
    "157ek_v3_reply": (V3_REPLY, V3_REPLY_SHA, V3_REPLY_BYTES),
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
                sha_file(full) == digest, "157el checker pin: "+label)


def load_v3_checker() -> Any:
    authenticate_wrapper()
    existing = sys.modules.get(V3_MODULE_NAME)
    if existing is not None:
        require(Path(existing.__file__).resolve() == (ROOT/V3_CHECKER).resolve(),
                "157el loaded v3 checker path")
        return existing
    spec = importlib.util.spec_from_file_location(V3_MODULE_NAME, ROOT/V3_CHECKER)
    require(spec is not None and spec.loader is not None,
            "157el v3 checker import spec")
    module = importlib.util.module_from_spec(spec)
    sys.modules[V3_MODULE_NAME] = module
    try:
        spec.loader.exec_module(module)
    except Exception:
        sys.modules.pop(V3_MODULE_NAME, None)
        raise
    require(module.SCHEMA == SCHEMA and module.OUTPUT == OUTPUT and
            module.TASK == V3_TASK and module.TASK_SHA == V3_TASK_SHA and
            module.TASK_BYTES == V3_TASK_BYTES and
            module.V2_PRODUCER_SHA == V2_PRODUCER_SHA and
            module.V2_CHECKER_SHA == V2_CHECKER_SHA,
            "157el frozen v3 checker public contract")
    module.authenticate_wrapper()
    return module


def _semantic_accounting_projection(block: dict[str, Any]) \
        -> dict[str, dict[str, int]]:
    require(isinstance(block, dict) and
            isinstance(block.get("pre_accounting"), dict) and
            isinstance(block.get("post_accounting"), dict),
            "157el checker semantic accounting container")
    result: dict[str, dict[str, int]] = {}
    for label in ("pre_accounting", "post_accounting"):
        row = block[label]
        require(set(row) == set(SEMANTIC_ACCOUNTING_FIELDS) and
                all(isinstance(row[name], int) and row[name] >= 0 for name in
                    MATHEMATICAL_ACCOUNTING_FIELDS+("pool_size",)) and
                (row["pool_order_sha256"] is None or
                 isinstance(row["pool_order_sha256"], str) and
                 len(row["pool_order_sha256"]) == 64),
                "157el checker semantic accounting type")
        result[label] = {name: int(row[name])
                         for name in MATHEMATICAL_ACCOUNTING_FIELDS}
    return result


def validate_completed_anchor_split(
        v2: Any, replayed: dict[str, Any], public_block: dict[str, Any],
        public_anchor: dict[str, Any], live_basis_entries: int,
        full_public_validator: Callable[..., bool], *,
        trace: dict[str, int] | None = None) -> None:
    """Production-shared separation of semantic and public accounting."""
    replay_semantic = _semantic_accounting_projection(replayed)
    require(isinstance(public_block, dict) and
            set(public_block["pre_accounting"]) == set(PUBLIC_ACCOUNTING_FIELDS)
            and set(public_block["post_accounting"]) ==
                set(PUBLIC_ACCOUNTING_FIELDS),
            "157el producer public accounting type")
    public_semantic = {
        label: v2._accounting_semantic(public_block[label])
        for label in ("pre_accounting", "post_accounting")}
    require(replay_semantic == public_semantic,
            "157el replay/public semantic accounting equality")
    require(isinstance(live_basis_entries, int) and live_basis_entries >= 0 and
            replayed["post_accounting"]["live_sparse_entries"] ==
                live_basis_entries,
            "157el replayed basis live-entry binding")
    require(full_public_validator(public_block, public_anchor,
                                  live_basis_entries) is True,
            "157el unchanged full public anchor validator reached")
    if trace is not None:
        trace["completed_anchor_production_wrapper"] = \
            trace.get("completed_anchor_production_wrapper", 0)+1


def install_accounting_repair(v2: Any, *,
                              trace: dict[str, int] | None = None) -> None:
    source = inspect.getsource(v2.check_receipt)
    bad_call = "_validate_anchor_public(replayed, data[\"post_block_anchor\"],"
    live_call = "live_basis_entries=basis.live_entries"
    core_call = "_validate_completed_core(data, replay_completed_block,"
    require(source.count(bad_call) == 1 and source.count(live_call) == 1 and
            source.count(core_call) == 1 and
            source.index(bad_call) < source.index(live_call) <
                source.index(core_call),
            "157el frozen completed-anchor source-shape recurrence")
    if not hasattr(v2, ORIGINAL_ANCHOR_ATTR):
        setattr(v2, ORIGINAL_ANCHOR_ATTR, v2._validate_anchor_public)
    if not hasattr(v2, ORIGINAL_CORE_ATTR):
        setattr(v2, ORIGINAL_CORE_ATTR, v2._validate_completed_core)
    original_anchor = getattr(v2, ORIGINAL_ANCHOR_ATTR)
    original_core = getattr(v2, ORIGINAL_CORE_ATTR)

    def strict_public_validator(public_block: dict[str, Any],
                                public_anchor: dict[str, Any],
                                live_basis_entries: int) -> bool:
        original_anchor(public_block, public_anchor, frozen=True,
                        live_basis_entries=live_basis_entries)
        return True

    def repaired_core(data: dict[str, Any],
                      replay_block: Callable[[], dict[str, Any]],
                      bad_validate_anchor: Callable[[dict[str, Any]], None],
                      replay_target: Callable[[], tuple[Any, dict[Any, int]]],
                      validate_selected: Callable[[Any, dict[Any, int]], None],
                      validate_dual: Callable[[Any], None], *,
                      trace: dict[str, int] | None = None) -> None:
        require(callable(bad_validate_anchor),
                "157el frozen bad callback remains source-authenticated")

        def repaired_anchor(replayed: dict[str, Any]) -> None:
            require("translation_block" in data and
                    "post_block_anchor" in data,
                    "157el completed core public receipt arguments")
            captured: list[tuple[dict[str, Any], dict[str, Any], bool, int]] = []
            prior = v2._validate_anchor_public

            def capture(block: dict[str, Any], anchor: dict[str, Any], *,
                        frozen: bool,
                        live_basis_entries: int | None = None) -> None:
                require(live_basis_entries is not None,
                        "157el captured independent live-entry count")
                captured.append((block, anchor, frozen, live_basis_entries))

            v2._validate_anchor_public = capture
            try:
                # Execute the frozen closure exactly once, but intercept its
                # known bad six-as-eleven call before the strict validator.
                bad_validate_anchor(replayed)
            finally:
                v2._validate_anchor_public = prior
            require(len(captured) == 1 and captured[0][0] is replayed and
                    captured[0][1] == data["post_block_anchor"] and
                    captured[0][2] is True,
                    "157el frozen callback argument capture")
            live_basis_entries = captured[0][3]
            validate_completed_anchor_split(
                v2, replayed, data["translation_block"],
                data["post_block_anchor"], live_basis_entries,
                strict_public_validator, trace=trace_outer)

        original_core(data, replay_block, repaired_anchor, replay_target,
                      validate_selected, validate_dual, trace=trace)

    trace_outer = trace
    v2._validate_completed_core = repaired_core
    require(v2._validate_completed_core is repaired_core,
            "157el production completed-core repair installed")


def check_receipt(q3_path: Path, receipt_path: Path,
                  *, seconds: float = 18_000.0) -> dict[str, Any]:
    v3 = load_v3_checker()
    v2 = v3.load_v2_checker()
    v3.install_projection_repair(v2)
    install_accounting_repair(v2)
    return v3.check_receipt(q3_path, receipt_path, seconds=seconds)


def _expect_failure(action: Callable[[], Any], label: str) -> None:
    try:
        action()
    except (KeyError, RuntimeError, TypeError, ValueError):
        return
    raise RuntimeError("157el mutation accepted: "+label)


def _frozen_fixture_pair(v2: Any) \
        -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], int]:
    public, anchor = v2._fixture_block({})
    gain = int(public["rank_gain"]); live = 3_090_400
    pre = copy.deepcopy(public["pre_accounting"])
    post = copy.deepcopy(public["post_accounting"])
    pre.update({"columns": 362725, "pivots": 362709, "dependent": 16,
                "live_sparse_entries": 3_090_367, "pool_size": 976408,
                "DAG_nodes": 673296, "DAG_edges": 494688,
                "section_bindings": 1, "section_expression_nodes": 287,
                "section_expression_edges": 435})
    post.update({"columns": 362736, "pivots": 362709+gain,
                 "dependent": 16+(11-gain),
                 "live_sparse_entries": live, "pool_size": 976500,
                 "DAG_nodes": 673307, "DAG_edges": 494699,
                 "section_bindings": 2, "section_expression_nodes": 288,
                 "section_expression_edges": 436})
    public["pre_accounting"] = pre; public["post_accounting"] = post
    counts = {name: post[name] for name in MATHEMATICAL_ACCOUNTING_FIELDS}
    anchor.update({"basis_columns": post["columns"],
        "basis_pivots": post["pivots"], "basis_dependent": post["dependent"],
        "basis_live_sparse_entries": live, "pool_size": post["pool_size"],
        "DAG_nodes": post["DAG_nodes"], "DAG_edges": post["DAG_edges"],
        "section_bindings": post["section_bindings"],
        "anchor_semantic_sha256": v2.sha_obj({"basis_counts": counts,
            "translation_hex": v2.FIRST_T_HEX,
            "columns_sha256": public["raw_columns_sha256"]})})
    replayed = copy.deepcopy(public)
    for label in ("pre_accounting", "post_accounting"):
        replayed[label] = {name: public[label][name]
                           for name in SEMANTIC_ACCOUNTING_FIELDS}
    return replayed, public, anchor, live


def self_test() -> None:
    v3 = load_v3_checker()
    # Retain v2/v3 result/resource/input, projection, lifecycle, value-root,
    # phase, proof, and 24-mutation fixtures verbatim.
    v3.self_test()
    v2 = v3.load_v2_checker()
    v3.install_projection_repair(v2)
    replayed, public, anchor, live = _frozen_fixture_pair(v2)
    original = getattr(v2, ORIGINAL_ANCHOR_ATTR,
                       v2._validate_anchor_public)

    _expect_failure(lambda: original(replayed, anchor, frozen=True,
                                     live_basis_entries=live),
                    "semantic ledger as public")
    _expect_failure(lambda: _semantic_accounting_projection(public),
                    "public ledger as semantic")

    trace: dict[str, int] = {}
    core_trace: dict[str, int] = {}
    receipt = {"translation_block": public, "post_block_anchor": anchor,
        "affine_system": {"consistent": False},
        "terminal_token": "B345_E4_D2_LEXBLOCK_TARGET6_INCONSISTENT",
        "normalized_dual": {"fixture": True}}
    install_accounting_repair(v2, trace=trace)

    class FixtureSystem:
        consistent = False

    branch_trace = {"dual": 0}

    def bad_callback(block: dict[str, Any]) -> None:
        v2._validate_anchor_public(block, anchor, frozen=True,
                                   live_basis_entries=live)

    def validate_dual(_: Any) -> None:
        branch_trace["dual"] += 1

    v2._validate_completed_core(
        receipt, lambda: replayed, bad_callback,
        lambda: (FixtureSystem(), {}), lambda *_: None, validate_dual,
        trace=core_trace)

    public_omissions = 0
    for name in PUBLIC_ONLY_FIELDS:
        bad_public = copy.deepcopy(public)
        del bad_public["post_accounting"][name]
        _expect_failure(lambda bad_public=bad_public:
            validate_completed_anchor_split(v2, replayed, bad_public, anchor,
                live, lambda block, row, count: (
                    original(block, row, frozen=True,
                             live_basis_entries=count) is None)),
            "public-only omission "+name)
        public_omissions += 1

    public_mutations = 0
    mutations: list[tuple[dict[str, Any], dict[str, Any],
                          dict[str, Any], str]] = []
    bad = copy.deepcopy(public); bad["post_accounting"]["section_bindings"] = \
        bad["pre_accounting"]["section_bindings"]
    mutations.append((copy.deepcopy(replayed), bad, copy.deepcopy(anchor),
                      "section increment"))
    bad = copy.deepcopy(public); bad["post_accounting"]["columns"] -= 1
    bad_replayed = copy.deepcopy(replayed)
    bad_replayed["post_accounting"]["columns"] -= 1
    mutations.append((bad_replayed, bad, copy.deepcopy(anchor),
                      "column increment"))
    bad = copy.deepcopy(public); bad["rank_gain"] += 1
    mutations.append((copy.deepcopy(replayed), bad, copy.deepcopy(anchor),
                      "rank gain"))
    bad = copy.deepcopy(public); bad["post_accounting"]["dependent"] += 1
    bad_replayed = copy.deepcopy(replayed)
    bad_replayed["post_accounting"]["dependent"] += 1
    mutations.append((bad_replayed, bad, copy.deepcopy(anchor),
                      "dependent increment"))
    bad_anchor = copy.deepcopy(anchor); bad_anchor["DAG_nodes"] += 1
    mutations.append((copy.deepcopy(replayed), copy.deepcopy(public),
                      bad_anchor, "anchor binding"))
    bad_anchor = copy.deepcopy(anchor)
    bad_anchor["anchor_semantic_sha256"] = "00"*32
    mutations.append((copy.deepcopy(replayed), copy.deepcopy(public),
                      bad_anchor, "anchor digest"))
    for bad_replayed, bad_public, bad_anchor, label in mutations:
        _expect_failure(lambda bad_replayed=bad_replayed,
                        bad_public=bad_public, bad_anchor=bad_anchor:
            validate_completed_anchor_split(v2, bad_replayed, bad_public,
                bad_anchor, live, lambda block, row, count: (
                    original(block, row, frozen=True,
                             live_basis_entries=count) is None)), label)
        public_mutations += 1

    _expect_failure(lambda: validate_completed_anchor_split(
        v2, replayed, public, anchor, live+1,
        lambda block, row, count: (
            original(block, row, frozen=True,
                     live_basis_entries=count) is None)),
        "replayed live entries")
    semantic_shape_mutations = 0
    bad_replayed = copy.deepcopy(replayed)
    del bad_replayed["pre_accounting"]["pool_size"]
    _expect_failure(lambda: validate_completed_anchor_split(
        v2, bad_replayed, public, anchor, live,
        lambda *_: True), "semantic key omission")
    semantic_shape_mutations += 1
    bad_replayed = copy.deepcopy(replayed)
    bad_replayed["post_accounting"]["DAG_nodes"] = 1
    _expect_failure(lambda: validate_completed_anchor_split(
        v2, bad_replayed, public, anchor, live,
        lambda *_: True), "semantic key addition")
    semantic_shape_mutations += 1

    _expect_failure(lambda: validate_completed_anchor_split(
        v2, replayed, public, anchor, live,
        lambda *_: None), "deleted eleven-key validator")
    require(trace == {"completed_anchor_production_wrapper": 1} and
            core_trace == {"completed_core": 1} and
            branch_trace == {"dual": 1} and
            public_omissions == 5 and public_mutations == 6 and
            semantic_shape_mutations == 2,
            "157el exact accounting fixture counters")
    print("D972_B345_LEXBLOCK_TARGET6_V4_CHECKER_SELFTEST_PASS "
          "semantic_public_accounting_split=1 "
          "semantic_ledger_as_public_rejected=1 "
          "public_ledger_as_semantic_rejected=1 "
          "public_only_omissions_rejected=5 "
          "public_relation_mutations_rejected=6 "
          "semantic_shape_mutations_rejected=2 "
          "replayed_live_entries_bound=1 "
          "completed_anchor_production_wrapper=1 "
          "eleven_key_validator_retained=1 "
          "completed_anchor_source_recurrence=1 "
          "inherited_v3_projection=1", flush=True)


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
    print("D972_B345_LEXBLOCK_TARGET6_V4_CHECKER_PASS "
          f"terminal={data['terminal_token']} receipt={args.receipt}",
          flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
