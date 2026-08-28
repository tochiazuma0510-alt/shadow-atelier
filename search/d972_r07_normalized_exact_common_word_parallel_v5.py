#!/usr/bin/env python3
"""Task303 v5: fixed-dual process-parallel boundary-kernel SELFTEST."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import multiprocessing
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "d972-r07-normalized-exact-common-word-parallel/v5"
SELF_SCHEMA = SCHEMA + "/selftest"
PRODUCTION_SCHEMA = SCHEMA + "/production-stop"
FIXTURE_SCHEMA = SCHEMA + "/fixture/v3"
SELFTEST_MARKER = "R07_NORMALIZED_EXACT_COMMON_WORD_PARALLEL_V5_SELFTEST_PASS"
TERMINAL_PREFIX = "R07_NORMALIZED_EXACT_COMMON_WORD_PARALLEL_V5_PRODUCER_TERMINAL"
PASS_TERMINAL = "PASS"
UNKNOWN_ADAPTER = "UNKNOWN_INPUT:resume_adapter_not_commissioned"
UNKNOWN_RESUME = "UNKNOWN_INPUT:authenticated_resume_absent"
UNKNOWN_WORKER = "UNKNOWN_RESOURCE:parallel_worker_failure"
WORKER_COUNTS = (2, 3, 4)
CASE_NAMES = (
    "active_two_shards",
    "cancel_across_shards",
    "nontrivial_lex_winner",
    "no_active_key",
)
MUTATIONS = (
    "omitted_shard",
    "duplicated_shard",
    "overlapping_interval",
    "gap",
    "permuted_pair_order",
    "wrong_dual_digest",
    "wrong_descriptor_digest",
    "changed_coefficient",
    "changed_translation_key",
    "changed_contributor",
    "wrong_mod3_merge",
    "zero_kept_active",
    "wrong_lex_winner",
    "wrong_direct_scalar",
    "wrong_pair_count",
    "stale_epoch",
    "worker_failure_accepted",
    "incomplete_batch_checkpointed",
    "single_process_true",
    "worker_count_outside_range",
)
FALSE_CLAIMS = {
    "common_word": False,
    "separator": False,
    "finite_common_word": False,
    "cofinal_lift": False,
    "fake": False,
    "ihara_witness": False,
}
SHARD_BODY_FIELDS = {
    "start",
    "stop",
    "count",
    "interval_digest",
    "dual_digest",
    "descriptor_digest",
    "partial",
    "contributors",
    "worker_failed",
}
SHARD_FIELDS = SHARD_BODY_FIELDS | {"result_digest"}
RUN_BODY_FIELDS = {
    "worker_count",
    "dual_digest",
    "descriptor_digest",
    "cover",
    "shards",
    "completed_shard_count",
    "pair_count",
    "accumulator",
    "contributors",
    "selected_key",
    "selected_scalar",
    "direct_scalar",
    "batch_complete",
    "checkpoint_state",
}
RUN_FIELDS = RUN_BODY_FIELDS | {"merge_digest"}
SEMANTIC_DIGEST_FIELDS = (
    "schema",
    "status",
    "terminal",
    "fixture_digest",
    "parallel_boundary",
    "single_process",
    "driver_worker_count",
    "worker_counts",
    "case_names",
    "cases",
    "epochs",
    "monitor",
    "checkpoint_state",
    "claims",
)


class SemanticError(RuntimeError):
    pass


class InputStop(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise SemanticError(message)


def canonical(value):
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode("ascii")


def digest_obj(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def f3(value):
    return int(value) % 3


def key_blob(value):
    return canonical(value).decode("ascii")


def boundary_key(descriptor):
    return [
        descriptor["block"],
        descriptor["relator_index"],
        descriptor["translation_blob"],
    ]


def dual_map(dual):
    require(isinstance(dual, list) and dual, "dual roster")
    answer = {}
    for record in dual:
        require(isinstance(record, list) and len(record) == 2, "dual record")
        key, value = record
        require(
            isinstance(key, list)
            and len(key) == 2
            and isinstance(key[0], str)
            and type(key[1]) is int,
            "dual key",
        )
        require(type(value) is int and value in (0, 1, 2), "dual value")
        blob = key_blob(key)
        require(blob not in answer, "duplicate dual key")
        answer[blob] = value
    require(dual == sorted(dual, key=lambda item: key_blob(item[0])), "dual order")
    return answer


def validate_descriptors(descriptors, dual):
    mapping = dual_map(dual)
    require(isinstance(descriptors, list) and descriptors, "descriptor roster")
    expected_fields = {
        "pair_index",
        "block",
        "relator_index",
        "translation_blob",
        "dual_key",
        "coefficient",
    }
    for index, descriptor in enumerate(descriptors):
        require(
            isinstance(descriptor, dict) and set(descriptor) == expected_fields,
            "descriptor shape",
        )
        require(
            type(descriptor["pair_index"]) is int
            and descriptor["pair_index"] == index,
            "descriptor pair order",
        )
        require(
            type(descriptor["block"]) is int and descriptor["block"] > 0,
            "descriptor block",
        )
        require(
            type(descriptor["relator_index"]) is int
            and descriptor["relator_index"] > 0,
            "descriptor relator",
        )
        require(
            isinstance(descriptor["translation_blob"], str)
            and descriptor["translation_blob"],
            "descriptor translation",
        )
        require(
            key_blob(descriptor["dual_key"]) in mapping,
            "descriptor dual key",
        )
        require(
            type(descriptor["coefficient"]) is int
            and descriptor["coefficient"] in (0, 1, 2),
            "descriptor coefficient",
        )
    return mapping


def frozen_dual_digest(dual):
    dual_map(dual)
    return digest_obj(dual)


def full_descriptor_digest(descriptors, dual):
    validate_descriptors(descriptors, dual)
    return digest_obj(descriptors)


def intervals(total, worker_count):
    require(worker_count in WORKER_COUNTS, "worker range")
    require(type(total) is int and total >= worker_count, "descriptor cardinality")
    return [
        [worker * total // worker_count, (worker + 1) * total // worker_count]
        for worker in range(worker_count)
    ]


def interval_digest(descriptors, start, stop):
    return digest_obj(
        {
            "start": start,
            "stop": stop,
            "pair_indices": [
                descriptor["pair_index"] for descriptor in descriptors[start:stop]
            ],
            "slice_digest": digest_obj(descriptors[start:stop]),
        }
    )


def add_f3(left, right):
    result = dict(left)
    for blob, value in right.items():
        require(type(value) is int and value in (1, 2), "partial F3 value")
        combined = (result.get(blob, 0) + value) % 3
        if combined:
            result[blob] = combined
        else:
            result.pop(blob, None)
    return {blob: result[blob] for blob in sorted(result)}


def slice_accumulator(dual, descriptors, start, stop):
    mapping = validate_descriptors(descriptors, dual)
    partial = {}
    contributors = {}
    for descriptor in descriptors[start:stop]:
        coefficient = f3(
            descriptor["coefficient"] * mapping[key_blob(descriptor["dual_key"])]
        )
        if not coefficient:
            continue
        blob = key_blob(boundary_key(descriptor))
        combined = (partial.get(blob, 0) + coefficient) % 3
        if combined:
            partial[blob] = combined
        else:
            partial.pop(blob, None)
        contributors.setdefault(blob, []).append(
            {
                "pair_index": descriptor["pair_index"],
                "dual_key": copy.deepcopy(descriptor["dual_key"]),
                "coefficient": coefficient,
            }
        )
    return (
        {blob: partial[blob] for blob in sorted(partial)},
        {blob: contributors[blob] for blob in sorted(contributors)},
    )


def shard_record(dual, descriptors, start, stop):
    partial, contributors = slice_accumulator(dual, descriptors, start, stop)
    body = {
        "start": start,
        "stop": stop,
        "count": stop - start,
        "interval_digest": interval_digest(descriptors, start, stop),
        "dual_digest": frozen_dual_digest(dual),
        "descriptor_digest": full_descriptor_digest(descriptors, dual),
        "partial": partial,
        "contributors": contributors,
        "worker_failed": False,
    }
    return {**body, "result_digest": digest_obj(body)}


def worker_entry(task):
    dual, descriptors, start, stop = task
    return shard_record(dual, descriptors, start, stop)


def validate_shard(shard, dual, descriptors, start, stop):
    require(isinstance(shard, dict) and set(shard) == SHARD_FIELDS, "shard shape")
    require(shard.get("worker_failed") is False, "worker failure")
    expected = shard_record(dual, descriptors, start, stop)
    require(shard == expected, "shard direct replay")


def select_active(accumulator):
    active = [json.loads(blob) for blob, value in accumulator.items() if value]
    return (
        min(active, key=lambda item: (item[0], item[2], item[1]))
        if active
        else None
    )


def direct_scalar(dual, descriptors, selected_key):
    if selected_key is None:
        return 0
    mapping = validate_descriptors(descriptors, dual)
    total = 0
    for descriptor in descriptors:
        if boundary_key(descriptor) == selected_key:
            total += (
                descriptor["coefficient"]
                * mapping[key_blob(descriptor["dual_key"])]
            )
    return total % 3


def serial_oracle(dual, descriptors):
    partial, contributors = slice_accumulator(dual, descriptors, 0, len(descriptors))
    selected = select_active(partial)
    scalar = partial.get(key_blob(selected), 0) if selected is not None else 0
    replayed = direct_scalar(dual, descriptors, selected)
    require(scalar == replayed, "serial direct scalar")
    return {
        "accumulator": partial,
        "contributors": contributors,
        "selected_key": selected,
        "selected_scalar": scalar,
        "direct_scalar": replayed,
        "pair_count": len(descriptors),
    }


def merge_shards(dual, descriptors, worker_count, shards):
    expected_cover = intervals(len(descriptors), worker_count)
    require(isinstance(shards, list) and len(shards) == worker_count, "shard count")
    observed_cover = [
        [shard.get("start"), shard.get("stop")]
        if isinstance(shard, dict)
        else [None, None]
        for shard in shards
    ]
    require(observed_cover == expected_cover, "ordered exact shard cover")
    accumulator = {}
    contributors = {}
    returned_count = 0
    for shard, (start, stop) in zip(shards, expected_cover):
        validate_shard(shard, dual, descriptors, start, stop)
        returned_count += shard["count"]
        accumulator = add_f3(accumulator, shard["partial"])
        for blob, records in shard["contributors"].items():
            contributors.setdefault(blob, []).extend(copy.deepcopy(records))
    contributors = {
        blob: contributors[blob] for blob in sorted(contributors)
    }
    require(returned_count == len(descriptors), "returned pair count")
    selected = select_active(accumulator)
    scalar = (
        accumulator.get(key_blob(selected), 0) if selected is not None else 0
    )
    replayed = direct_scalar(dual, descriptors, selected)
    require(
        (selected is None and scalar == replayed == 0)
        or (selected is not None and scalar == replayed and scalar in (1, 2)),
        "merged direct scalar",
    )
    body = {
        "worker_count": worker_count,
        "dual_digest": frozen_dual_digest(dual),
        "descriptor_digest": full_descriptor_digest(descriptors, dual),
        "cover": expected_cover,
        "shards": copy.deepcopy(shards),
        "completed_shard_count": worker_count,
        "pair_count": returned_count,
        "accumulator": accumulator,
        "contributors": contributors,
        "selected_key": selected,
        "selected_scalar": scalar,
        "direct_scalar": replayed,
        "batch_complete": True,
        "checkpoint_state": None,
    }
    run = {**body, "merge_digest": digest_obj(body)}
    require(run_projection(run) == serial_oracle(dual, descriptors), "serial parity")
    return run


def run_projection(run):
    return {
        field: copy.deepcopy(run[field])
        for field in (
            "accumulator",
            "contributors",
            "selected_key",
            "selected_scalar",
            "direct_scalar",
            "pair_count",
        )
    }


def validate_run(run, dual, descriptors, worker_count):
    require(isinstance(run, dict) and set(run) == RUN_FIELDS, "run shape")
    require(run.get("worker_count") == worker_count, "run worker count")
    require(run.get("batch_complete") is True, "incomplete batch")
    require(run.get("checkpoint_state") is None, "partial checkpoint state")
    expected = merge_shards(dual, descriptors, worker_count, run.get("shards"))
    require(run == expected, "run direct replay")


def parallel_run(dual, descriptors, worker_count):
    validate_descriptors(descriptors, dual)
    cover = intervals(len(descriptors), worker_count)
    context = multiprocessing.get_context("fork")
    tasks = [
        (copy.deepcopy(dual), copy.deepcopy(descriptors), start, stop)
        for start, stop in cover
    ]
    with context.Pool(worker_count) as pool:
        shards = pool.map(worker_entry, tasks)
    return merge_shards(dual, descriptors, worker_count, shards)


def make_descriptor(index, block, relator, translation, coefficient):
    return {
        "pair_index": index,
        "block": block,
        "relator_index": relator,
        "translation_blob": translation,
        "dual_key": ["D", index % 4],
        "coefficient": coefficient,
    }


def make_case(specification):
    return [
        make_descriptor(index, *values)
        for index, values in enumerate(specification)
    ]


def baseline_dual(value=1):
    return [[["D", index], value] for index in range(4)]


def case_descriptors():
    return {
        "active_two_shards": make_case(
            [
                (1, 1, "a", 1),
                (1, 2, "a", 1),
                (1, 1, "a", 2),
                (2, 1, "z", 1),
                (2, 1, "z", 2),
                (1, 2, "a", 1),
                (1, 1, "b", 1),
                (1, 1, "b", 2),
            ]
        ),
        "cancel_across_shards": make_case(
            [
                (1, 1, "a", 1),
                (1, 1, "a", 2),
                (1, 2, "a", 1),
                (2, 1, "z", 0),
                (2, 1, "z", 0),
                (1, 2, "a", 2),
                (2, 2, "c", 1),
                (2, 2, "d", 0),
            ]
        ),
        "nontrivial_lex_winner": make_case(
            [
                (1, 2, "a", 1),
                (1, 1, "b", 1),
                (2, 1, "a", 1),
                (2, 1, "a", 2),
                (2, 2, "z", 0),
                (2, 2, "z", 0),
                (3, 1, "a", 0),
                (3, 2, "a", 0),
            ]
        ),
        "no_active_key": make_case(
            [
                (1, 1, "a", 1),
                (1, 2, "b", 2),
                (2, 1, "a", 1),
                (2, 2, "c", 2),
                (1, 1, "a", 2),
                (1, 2, "b", 1),
                (2, 1, "a", 2),
                (2, 2, "c", 1),
            ]
        ),
    }


def expected_fixture():
    return {
        "schema": FIXTURE_SCHEMA,
        "case_names": list(CASE_NAMES),
        "epoch_runs": 2,
        "worker_counts": list(WORKER_COUNTS),
        "mutation_names": list(MUTATIONS),
        "parallel_boundary": True,
        "single_process": False,
        "case_expectations": {
            "active_two_shards": {
                "selected_key": [1, 2, "a"],
                "selected_scalar": 2,
                "w2_crosses_cut": True,
            },
            "cancel_across_shards": {
                "selected_key": [2, 2, "c"],
                "selected_scalar": 1,
                "cancelled_key": [1, 2, "a"],
            },
            "nontrivial_lex_winner": {
                "selected_key": [1, 2, "a"],
                "selected_scalar": 1,
                "competing_key": [1, 1, "b"],
            },
            "no_active_key": {
                "selected_key": None,
                "selected_scalar": 0,
            },
        },
        "claims": copy.deepcopy(FALSE_CLAIMS),
    }


def load_fixture(path_value):
    path = Path(path_value)
    require(
        not path.is_absolute()
        and ".." not in path.parts
        and (
            path.as_posix().startswith("search/certs/")
            or path.as_posix().startswith("ci/in/")
        ),
        "fixture path",
    )
    fixture = json.loads((ROOT / path).read_text(encoding="ascii"))
    require(fixture == expected_fixture(), "fixture contract")
    return fixture


def contributor_indices(serial, selected_key):
    return [
        record["pair_index"]
        for record in serial["contributors"].get(key_blob(selected_key), [])
    ]


def validate_case_outcome(name, serial, outcome, descriptors):
    require(
        outcome.get("selected_key") == serial["selected_key"]
        and outcome.get("selected_scalar") == serial["selected_scalar"],
        "outcome/serial binding",
    )
    if name == "active_two_shards":
        expected = expected_fixture()["case_expectations"][name]
        require(outcome == expected, "active outcome")
        cut = intervals(len(descriptors), 2)[0][1]
        indices = contributor_indices(serial, expected["selected_key"])
        require(
            any(index < cut for index in indices)
            and any(index >= cut for index in indices),
            "selected key does not cross w2 cut",
        )
    elif name == "cancel_across_shards":
        expected = expected_fixture()["case_expectations"][name]
        require(outcome == expected, "cancellation outcome")
        cancelled_blob = key_blob(expected["cancelled_key"])
        cut = intervals(len(descriptors), 2)[0][1]
        indices = [
            record["pair_index"]
            for record in serial["contributors"].get(cancelled_blob, [])
        ]
        require(
            cancelled_blob not in serial["accumulator"]
            and any(index < cut for index in indices)
            and any(index >= cut for index in indices),
            "cross-shard cancellation",
        )
    elif name == "nontrivial_lex_winner":
        expected = expected_fixture()["case_expectations"][name]
        require(outcome == expected, "lex outcome")
        require(
            key_blob(expected["selected_key"]) in serial["accumulator"]
            and key_blob(expected["competing_key"]) in serial["accumulator"]
            and expected["selected_key"][1] > expected["competing_key"][1]
            and expected["selected_key"][2] < expected["competing_key"][2],
            "nontrivial v3 lex order",
        )
    elif name == "no_active_key":
        expected = expected_fixture()["case_expectations"][name]
        require(
            outcome == expected
            and serial["accumulator"] == {}
            and serial["selected_key"] is None
            and serial["selected_scalar"] == 0,
            "no-active outcome",
        )
    else:
        raise SemanticError("unknown case")


def build_cases():
    cases = []
    dual = baseline_dual(1)
    descriptors_by_name = case_descriptors()
    for name in CASE_NAMES:
        descriptors = descriptors_by_name[name]
        serial = serial_oracle(dual, descriptors)
        outcome = copy.deepcopy(expected_fixture()["case_expectations"][name])
        validate_case_outcome(name, serial, outcome, descriptors)
        runs = {
            str(worker_count): parallel_run(dual, descriptors, worker_count)
            for worker_count in WORKER_COUNTS
        }
        cases.append(
            {
                "name": name,
                "dual": copy.deepcopy(dual),
                "descriptors": descriptors,
                "serial": serial,
                "runs": runs,
                "outcome": outcome,
            }
        )
    return cases


def epoch_isolation_digest(runs, state_isolated):
    return digest_obj({"runs": runs, "state_isolated": state_isolated})


def build_epochs(driver_worker_count):
    descriptors = case_descriptors()["active_two_shards"]
    runs = []
    for epoch_index, dual in (
        (1, baseline_dual(1)),
        (2, baseline_dual(2)),
    ):
        runs.append(
            {
                "epoch_index": epoch_index,
                "dual": dual,
                "serial": serial_oracle(dual, descriptors),
                "parallel": parallel_run(dual, descriptors, driver_worker_count),
            }
        )
    state_isolated = (
        runs[0]["dual"] != runs[1]["dual"]
        and runs[0]["serial"] != runs[1]["serial"]
        and run_projection(runs[0]["parallel"]) == runs[0]["serial"]
        and run_projection(runs[1]["parallel"]) == runs[1]["serial"]
        and all(
            shard["dual_digest"] == frozen_dual_digest(runs[1]["dual"])
            for shard in runs[1]["parallel"]["shards"]
        )
    )
    return {
        "runs": runs,
        "state_isolated": state_isolated,
        "isolation_digest": epoch_isolation_digest(runs, state_isolated),
    }


def semantic_payload(receipt):
    return {field: copy.deepcopy(receipt[field]) for field in SEMANTIC_DIGEST_FIELDS}


def rebind_receipt(receipt):
    receipt["input_digest"] = digest_obj(semantic_payload(receipt))
    receipt.pop("self_digest_sha256", None)
    receipt["self_digest_sha256"] = digest_obj(receipt)


def check_receipt_seal(receipt):
    require(isinstance(receipt, dict), "receipt object")
    body = dict(receipt)
    claimed = body.pop("self_digest_sha256", None)
    require(isinstance(claimed, str) and claimed == digest_obj(body), "receipt seal")


def expected_monitor(driver_worker_count):
    return {
        "parallel_boundary": True,
        "single_process": False,
        "driver_worker_count": driver_worker_count,
        "worker_counts_exercised": list(WORKER_COUNTS),
        "completed_batch_count": 14,
        "completed_shard_count": 36 + 2 * driver_worker_count,
        "total_pair_count": 112,
        "boundary_pairs": 112,
        "worker_failures": 0,
        "aggregate_rss_policy": (
            "SELFTEST_ONLY_NO_RSS_CLAIM_PRODUCTION_ADAPTER_ABSENT"
        ),
    }


def validate_cases(cases):
    require(
        isinstance(cases, list)
        and [case.get("name") for case in cases] == list(CASE_NAMES),
        "case names",
    )
    for case in cases:
        require(
            isinstance(case, dict)
            and set(case)
            == {"name", "dual", "descriptors", "serial", "runs", "outcome"},
            "case shape",
        )
        name = case["name"]
        dual = case["dual"]
        descriptors = case["descriptors"]
        require(case["serial"] == serial_oracle(dual, descriptors), "serial oracle")
        require(
            isinstance(case["runs"], dict)
            and set(case["runs"]) == {str(value) for value in WORKER_COUNTS},
            "worker run roster",
        )
        for worker_count in WORKER_COUNTS:
            validate_run(
                case["runs"][str(worker_count)],
                dual,
                descriptors,
                worker_count,
            )
        validate_case_outcome(name, case["serial"], case["outcome"], descriptors)


def validate_epochs(epochs, driver_worker_count):
    require(
        isinstance(epochs, dict)
        and set(epochs) == {"runs", "state_isolated", "isolation_digest"},
        "epoch envelope",
    )
    runs = epochs["runs"]
    require(isinstance(runs, list) and len(runs) == 2, "two epoch runs")
    descriptors = case_descriptors()["active_two_shards"]
    require(
        [run.get("epoch_index") for run in runs] == [1, 2],
        "epoch ordering",
    )
    for run in runs:
        require(
            isinstance(run, dict)
            and set(run) == {"epoch_index", "dual", "serial", "parallel"},
            "epoch run shape",
        )
        require(
            run["serial"] == serial_oracle(run["dual"], descriptors),
            "epoch serial oracle",
        )
        validate_run(
            run["parallel"], run["dual"], descriptors, driver_worker_count
        )
        require(
            run_projection(run["parallel"]) == run["serial"],
            "epoch parallel parity",
        )
    require(
        runs[0]["dual"] != runs[1]["dual"]
        and runs[0]["serial"] != runs[1]["serial"],
        "different frozen epochs",
    )
    require(epochs["state_isolated"] is True, "epoch isolation flag")
    require(
        epochs["isolation_digest"]
        == epoch_isolation_digest(runs, epochs["state_isolated"]),
        "epoch isolation digest",
    )
    require(
        all(
            shard["dual_digest"] == frozen_dual_digest(runs[1]["dual"])
            for shard in runs[1]["parallel"]["shards"]
        ),
        "stale epoch shard",
    )


def validate_semantics(receipt):
    check_receipt_seal(receipt)
    require(
        set(receipt)
        == set(SEMANTIC_DIGEST_FIELDS)
        | {"input_digest", "mutation_controls", "self_digest_sha256"},
        "selftest receipt shape",
    )
    require(
        receipt.get("schema") == SELF_SCHEMA
        and receipt.get("status") == "PASS"
        and receipt.get("terminal") == PASS_TERMINAL,
        "selftest envelope",
    )
    require(
        receipt.get("fixture_digest") == digest_obj(expected_fixture()),
        "fixture digest",
    )
    require(
        receipt.get("parallel_boundary") is True
        and receipt.get("single_process") is False,
        "parallel process flags",
    )
    driver_worker_count = receipt.get("driver_worker_count")
    require(driver_worker_count in WORKER_COUNTS, "driver worker count")
    require(
        receipt.get("worker_counts") == list(WORKER_COUNTS)
        and receipt.get("case_names") == list(CASE_NAMES),
        "public rosters",
    )
    require(
        receipt.get("input_digest") == digest_obj(semantic_payload(receipt)),
        "semantic input digest",
    )
    validate_cases(receipt.get("cases"))
    validate_epochs(receipt.get("epochs"), driver_worker_count)
    require(
        receipt.get("monitor") == expected_monitor(driver_worker_count),
        "monitor truth",
    )
    require(receipt.get("checkpoint_state") is None, "selftest checkpoint state")
    require(receipt.get("claims") == FALSE_CLAIMS, "false claims")
    require(isinstance(receipt.get("mutation_controls"), dict), "mutation placeholder")


def refresh_shard_digest(shard):
    body = {field: copy.deepcopy(shard[field]) for field in SHARD_BODY_FIELDS}
    shard["result_digest"] = digest_obj(body)


def refresh_run_digest(run):
    body = {field: copy.deepcopy(run[field]) for field in RUN_BODY_FIELDS}
    run["merge_digest"] = digest_obj(body)


def refresh_epoch_digest(epochs):
    epochs["isolation_digest"] = epoch_isolation_digest(
        epochs["runs"], epochs["state_isolated"]
    )


def first_run(receipt):
    return receipt["cases"][0]["runs"]["2"]


def apply_mutation(receipt, name):
    run = first_run(receipt)
    descriptors = receipt["cases"][0]["descriptors"]
    if name == "omitted_shard":
        run["shards"].pop()
        run["cover"].pop()
        run["completed_shard_count"] -= 1
        refresh_run_digest(run)
    elif name == "duplicated_shard":
        run["shards"].append(copy.deepcopy(run["shards"][0]))
        run["cover"].append(copy.deepcopy(run["cover"][0]))
        run["completed_shard_count"] += 1
        refresh_run_digest(run)
    elif name == "overlapping_interval":
        shard = run["shards"][1]
        shard["start"] = run["shards"][0]["stop"] - 1
        shard["count"] = shard["stop"] - shard["start"]
        shard["interval_digest"] = interval_digest(
            descriptors, shard["start"], shard["stop"]
        )
        run["cover"][1] = [shard["start"], shard["stop"]]
        refresh_shard_digest(shard)
        refresh_run_digest(run)
    elif name == "gap":
        shard = run["shards"][1]
        shard["start"] = run["shards"][0]["stop"] + 1
        shard["count"] = shard["stop"] - shard["start"]
        shard["interval_digest"] = interval_digest(
            descriptors, shard["start"], shard["stop"]
        )
        run["cover"][1] = [shard["start"], shard["stop"]]
        refresh_shard_digest(shard)
        refresh_run_digest(run)
    elif name == "permuted_pair_order":
        descriptors[0], descriptors[1] = descriptors[1], descriptors[0]
    elif name == "wrong_dual_digest":
        shard = run["shards"][0]
        shard["dual_digest"] = "wrong:" + shard["dual_digest"]
        refresh_shard_digest(shard)
        refresh_run_digest(run)
    elif name == "wrong_descriptor_digest":
        shard = run["shards"][0]
        shard["descriptor_digest"] = "wrong:" + shard["descriptor_digest"]
        refresh_shard_digest(shard)
        refresh_run_digest(run)
    elif name == "changed_coefficient":
        descriptor = descriptors[0]
        descriptor["coefficient"] = (descriptor["coefficient"] + 1) % 3
    elif name == "changed_translation_key":
        descriptors[0]["translation_blob"] += "-mutated"
    elif name == "changed_contributor":
        shard = run["shards"][0]
        blob = sorted(shard["contributors"])[0]
        record = shard["contributors"][blob][0]
        record["coefficient"] = (record["coefficient"] % 2) + 1
        refresh_shard_digest(shard)
        refresh_run_digest(run)
    elif name == "wrong_mod3_merge":
        blob = key_blob(run["selected_key"])
        run["accumulator"][blob] = (run["accumulator"][blob] % 2) + 1
        refresh_run_digest(run)
    elif name == "zero_kept_active":
        zero_blob = key_blob([9, 9, "zero"])
        shard = run["shards"][0]
        shard["partial"][zero_blob] = 0
        run["accumulator"][zero_blob] = 0
        refresh_shard_digest(shard)
        refresh_run_digest(run)
    elif name == "wrong_lex_winner":
        lex_run = receipt["cases"][2]["runs"]["2"]
        competitor = [1, 1, "b"]
        lex_run["selected_key"] = competitor
        lex_run["selected_scalar"] = lex_run["accumulator"][key_blob(competitor)]
        lex_run["direct_scalar"] = lex_run["selected_scalar"]
        refresh_run_digest(lex_run)
    elif name == "wrong_direct_scalar":
        run["direct_scalar"] = (run["direct_scalar"] + 1) % 3
        refresh_run_digest(run)
    elif name == "wrong_pair_count":
        shard = run["shards"][0]
        shard["count"] += 1
        run["pair_count"] += 1
        refresh_shard_digest(shard)
        refresh_run_digest(run)
    elif name == "stale_epoch":
        receipt["epochs"]["runs"][1]["epoch_index"] = 1
        refresh_epoch_digest(receipt["epochs"])
    elif name == "worker_failure_accepted":
        shard = run["shards"][0]
        shard["worker_failed"] = True
        refresh_shard_digest(shard)
        refresh_run_digest(run)
    elif name == "incomplete_batch_checkpointed":
        run["batch_complete"] = False
        run["checkpoint_state"] = {
            "safe": True,
            "partial_accumulator_serialized": True,
        }
        refresh_run_digest(run)
    elif name == "single_process_true":
        receipt["single_process"] = True
    elif name == "worker_count_outside_range":
        run["worker_count"] = 1
        refresh_run_digest(run)
    else:
        raise SemanticError("unknown mutation")


def mutation_effect_digest(receipt):
    return digest_obj(semantic_payload(receipt))


def run_mutations(baseline):
    baseline_effect = mutation_effect_digest(baseline)
    effects = []
    for name in MUTATIONS:
        mutant = copy.deepcopy(baseline)
        apply_mutation(mutant, name)
        rebind_receipt(mutant)
        mutant_effect = mutation_effect_digest(mutant)
        require(mutant_effect != baseline_effect, "mutation no-op: " + name)
        rejected = False
        reason = ""
        try:
            validate_semantics(mutant)
        except (SemanticError, KeyError, TypeError, ValueError) as error:
            rejected = True
            reason = type(error).__name__ + ":" + str(error)
        require(rejected, "mutation survived: " + name)
        effects.append(
            {
                "name": name,
                "baseline_digest": baseline_effect,
                "mutant_digest": mutant_effect,
                "rejected": True,
                "reason_digest": hashlib.sha256(reason.encode("utf-8")).hexdigest(),
            }
        )
    return effects


def validate_final(receipt):
    validate_semantics(receipt)
    controls = receipt["mutation_controls"]
    require(
        isinstance(controls, dict)
        and set(controls) == {"names", "attempted", "rejected", "effects"},
        "mutation summary shape",
    )
    require(
        controls["names"] == list(MUTATIONS)
        and controls["attempted"] == len(MUTATIONS)
        and controls["rejected"] == len(MUTATIONS)
        and isinstance(controls["effects"], list)
        and len(controls["effects"]) == len(MUTATIONS),
        "mutation summary",
    )
    for name, effect in zip(MUTATIONS, controls["effects"]):
        require(
            isinstance(effect, dict)
            and set(effect)
            == {
                "name",
                "baseline_digest",
                "mutant_digest",
                "rejected",
                "reason_digest",
            }
            and effect["name"] == name
            and effect["rejected"] is True
            and effect["baseline_digest"] != effect["mutant_digest"],
            "mutation effect record",
        )


def selftest(driver_worker_count, fixture_path):
    require(driver_worker_count in WORKER_COUNTS, "driver worker range")
    fixture = load_fixture(fixture_path)
    cases = build_cases()
    epochs = build_epochs(driver_worker_count)
    receipt = {
        "schema": SELF_SCHEMA,
        "status": "PASS",
        "terminal": PASS_TERMINAL,
        "fixture_digest": digest_obj(fixture),
        "parallel_boundary": True,
        "single_process": False,
        "driver_worker_count": driver_worker_count,
        "worker_counts": list(WORKER_COUNTS),
        "case_names": list(CASE_NAMES),
        "cases": cases,
        "epochs": epochs,
        "monitor": expected_monitor(driver_worker_count),
        "checkpoint_state": None,
        "claims": copy.deepcopy(FALSE_CLAIMS),
        "mutation_controls": {
            "names": list(MUTATIONS),
            "attempted": 0,
            "rejected": 0,
            "effects": [],
        },
    }
    rebind_receipt(receipt)
    validate_semantics(receipt)
    effects = run_mutations(receipt)
    receipt["mutation_controls"] = {
        "names": list(MUTATIONS),
        "attempted": len(effects),
        "rejected": sum(1 for effect in effects if effect["rejected"]),
        "effects": effects,
    }
    rebind_receipt(receipt)
    validate_final(receipt)
    return receipt


def sealed_production_stop(terminal, reason, worker_count, resume_path):
    receipt = {
        "schema": PRODUCTION_SCHEMA,
        "status": "UNKNOWN_INPUT",
        "terminal": terminal,
        "reason": reason,
        "resume_path": resume_path,
        "adapter_commissioned": False,
        "parallel_boundary": True,
        "single_process": False,
        "worker_count": worker_count,
        "claims": copy.deepcopy(FALSE_CLAIMS),
    }
    receipt["self_digest_sha256"] = digest_obj(receipt)
    return receipt


def production(resume_value, worker_count):
    require(worker_count in WORKER_COUNTS, "production worker range")
    path = Path(resume_value)
    if (
        not resume_value
        or path.is_absolute()
        or ".." in path.parts
        or not path.as_posix().startswith("ci/in/")
        or not (ROOT / path).is_file()
    ):
        return sealed_production_stop(
            UNKNOWN_RESUME,
            "authenticated resume input was not supplied",
            worker_count,
            resume_value,
        )
    return sealed_production_stop(
        UNKNOWN_ADAPTER,
        "parallel v3-resume adapter requires a separate commission",
        worker_count,
        path.as_posix(),
    )


def write_fresh_output(path_value, receipt):
    path = Path(path_value)
    if (
        path.is_absolute()
        or not path.as_posix().startswith("ci/out/")
        or ".." in path.parts
    ):
        raise InputStop("output path")
    target = ROOT / path
    if target.exists():
        raise InputStop("stale output")
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("xb") as stream:
        stream.write(canonical(receipt) + b"\n")


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode", choices=("SELFTEST", "PRODUCTION"), default="PRODUCTION"
    )
    parser.add_argument(
        "--fixture",
        default=(
            "search/certs/"
            "d972_r07_normalized_exact_common_word_parallel_selftest_v5_20260828.json"
        ),
    )
    parser.add_argument("--resume", default="")
    parser.add_argument("--boundary-workers", type=int, default=2)
    parser.add_argument("--seconds", type=int, default=19800)
    parser.add_argument("--boundary-pairs", type=int, default=8000000)
    parser.add_argument("--fibre-scans", type=int, default=80000000)
    parser.add_argument("--candidate-words", type=int, default=2000000)
    parser.add_argument("--retained-columns", type=int, default=250000)
    parser.add_argument("--checkpoint-bytes", type=int, default=4000000000)
    parser.add_argument("--rss-bytes", type=int, default=5700000000)
    parser.add_argument("--oracle-rounds", type=int, default=1)
    parser.add_argument("--output", required=True)
    args = parser.parse_args(argv)
    result = None
    return_code = 0
    try:
        if args.boundary_workers not in WORKER_COUNTS:
            raise InputStop("boundary worker range 2..4")
        if args.mode == "SELFTEST":
            result = selftest(args.boundary_workers, args.fixture)
        else:
            result = production(args.resume, args.boundary_workers)
    except (SemanticError, InputStop, OSError, UnicodeError, json.JSONDecodeError) as error:
        terminal = UNKNOWN_RESUME
        result = sealed_production_stop(
            terminal,
            type(error).__name__ + ":" + str(error),
            args.boundary_workers,
            args.resume,
        )
        return_code = 2
    except Exception as error:
        result = sealed_production_stop(
            UNKNOWN_WORKER,
            type(error).__name__ + ":" + str(error),
            args.boundary_workers,
            args.resume,
        )
        return_code = 2
    try:
        write_fresh_output(args.output, result)
    except (InputStop, OSError):
        print(TERMINAL_PREFIX, UNKNOWN_RESUME, flush=True)
        return 2
    if (
        args.mode == "SELFTEST"
        and return_code == 0
        and result.get("terminal") == PASS_TERMINAL
    ):
        print(SELFTEST_MARKER, flush=True)
    print(TERMINAL_PREFIX, result["terminal"], flush=True)
    return return_code


if __name__ == "__main__":
    raise SystemExit(main())
