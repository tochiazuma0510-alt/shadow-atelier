#!/usr/bin/env python3
"""Independent task303 checker for the fixed-dual parallel v5 SELFTEST."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "d972-r07-normalized-exact-common-word-parallel/v5"
SELF_SCHEMA = SCHEMA + "/selftest"
PRODUCTION_SCHEMA = SCHEMA + "/production-stop"
FIXTURE_SCHEMA = SCHEMA + "/fixture/v3"
PASS_MARKER = "R07_NORMALIZED_EXACT_COMMON_WORD_PARALLEL_V5_CHECKER_PASS"
TERMINAL_PREFIX = "R07_NORMALIZED_EXACT_COMMON_WORD_PARALLEL_V5_CHECKER_TERMINAL"
PASS_TERMINAL = "PASS"
UNKNOWN_ADAPTER = "UNKNOWN_INPUT:resume_adapter_not_commissioned"
UNKNOWN_RESUME = "UNKNOWN_INPUT:authenticated_resume_absent"
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


class CheckError(RuntimeError):
    pass


def insist(condition, message):
    if not condition:
        raise CheckError(message)


def encoded(value):
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode("ascii")


def object_sha(value):
    return hashlib.sha256(encoded(value)).hexdigest()


def blob(value):
    return encoded(value).decode("ascii")


def public_boundary_key(descriptor):
    return [
        descriptor["block"],
        descriptor["relator_index"],
        descriptor["translation_blob"],
    ]


def inspect_dual(dual):
    insist(isinstance(dual, list) and dual, "dual list")
    mapping = {}
    for item in dual:
        insist(isinstance(item, list) and len(item) == 2, "dual item")
        coordinate, value = item
        insist(
            isinstance(coordinate, list)
            and len(coordinate) == 2
            and isinstance(coordinate[0], str)
            and type(coordinate[1]) is int,
            "dual coordinate",
        )
        insist(type(value) is int and value in (0, 1, 2), "dual coefficient")
        coordinate_blob = blob(coordinate)
        insist(coordinate_blob not in mapping, "dual duplicate")
        mapping[coordinate_blob] = value
    insist(
        dual == sorted(dual, key=lambda record: blob(record[0])),
        "dual canonical order",
    )
    return mapping


def inspect_descriptors(descriptors, dual):
    dual_values = inspect_dual(dual)
    fields = {
        "pair_index",
        "block",
        "relator_index",
        "translation_blob",
        "dual_key",
        "coefficient",
    }
    insist(isinstance(descriptors, list) and descriptors, "descriptors")
    for index, descriptor in enumerate(descriptors):
        insist(
            isinstance(descriptor, dict) and set(descriptor) == fields,
            "descriptor fields",
        )
        insist(
            type(descriptor["pair_index"]) is int
            and descriptor["pair_index"] == index,
            "descriptor ordering",
        )
        insist(
            type(descriptor["block"]) is int and descriptor["block"] > 0,
            "descriptor block",
        )
        insist(
            type(descriptor["relator_index"]) is int
            and descriptor["relator_index"] > 0,
            "descriptor relator",
        )
        insist(
            isinstance(descriptor["translation_blob"], str)
            and descriptor["translation_blob"],
            "descriptor translation",
        )
        insist(blob(descriptor["dual_key"]) in dual_values, "descriptor dual")
        insist(
            type(descriptor["coefficient"]) is int
            and descriptor["coefficient"] in (0, 1, 2),
            "descriptor coefficient",
        )
    return dual_values


def independent_intervals(total, worker_count):
    insist(worker_count in WORKER_COUNTS, "worker range")
    insist(type(total) is int and total >= worker_count, "pair cardinality")
    boundaries = []
    for worker in range(worker_count):
        boundaries.append(
            [worker * total // worker_count, (worker + 1) * total // worker_count]
        )
    return boundaries


def independent_interval_digest(descriptors, start, stop):
    payload = {
        "start": start,
        "stop": stop,
        "pair_indices": [
            descriptors[index]["pair_index"] for index in range(start, stop)
        ],
        "slice_digest": object_sha(descriptors[start:stop]),
    }
    return object_sha(payload)


def replay_slice(dual, descriptors, start, stop):
    values = inspect_descriptors(descriptors, dual)
    totals = {}
    contributors = {}
    for index in range(start, stop):
        descriptor = descriptors[index]
        coefficient = (
            descriptor["coefficient"] * values[blob(descriptor["dual_key"])]
        ) % 3
        if coefficient == 0:
            continue
        boundary_blob = blob(public_boundary_key(descriptor))
        new_total = (totals.get(boundary_blob, 0) + coefficient) % 3
        if new_total == 0:
            totals.pop(boundary_blob, None)
        else:
            totals[boundary_blob] = new_total
        contributors.setdefault(boundary_blob, []).append(
            {
                "pair_index": descriptor["pair_index"],
                "dual_key": copy.deepcopy(descriptor["dual_key"]),
                "coefficient": coefficient,
            }
        )
    return (
        {key: totals[key] for key in sorted(totals)},
        {key: contributors[key] for key in sorted(contributors)},
    )


def expected_shard(dual, descriptors, start, stop):
    partial, contributors = replay_slice(dual, descriptors, start, stop)
    body = {
        "start": start,
        "stop": stop,
        "count": stop - start,
        "interval_digest": independent_interval_digest(
            descriptors, start, stop
        ),
        "dual_digest": object_sha(dual),
        "descriptor_digest": object_sha(descriptors),
        "partial": partial,
        "contributors": contributors,
        "worker_failed": False,
    }
    return {**body, "result_digest": object_sha(body)}


def replay_shard(shard, dual, descriptors, start, stop):
    insist(isinstance(shard, dict) and set(shard) == SHARD_FIELDS, "shard shape")
    insist(shard.get("worker_failed") is False, "worker failure flag")
    insist(
        shard == expected_shard(dual, descriptors, start, stop),
        "independent shard replay",
    )


def independent_serial(descriptors, dual):
    values = inspect_descriptors(descriptors, dual)
    accumulator = {}
    contributors = {}
    for descriptor in descriptors:
        coefficient = (
            descriptor["coefficient"] * values[blob(descriptor["dual_key"])]
        ) % 3
        if coefficient == 0:
            continue
        boundary_blob = blob(public_boundary_key(descriptor))
        total = (accumulator.get(boundary_blob, 0) + coefficient) % 3
        if total:
            accumulator[boundary_blob] = total
        else:
            accumulator.pop(boundary_blob, None)
        contributors.setdefault(boundary_blob, []).append(
            {
                "pair_index": descriptor["pair_index"],
                "dual_key": copy.deepcopy(descriptor["dual_key"]),
                "coefficient": coefficient,
            }
        )
    accumulator = {key: accumulator[key] for key in sorted(accumulator)}
    contributors = {key: contributors[key] for key in sorted(contributors)}
    active = [json.loads(key) for key, value in accumulator.items() if value]
    selected = (
        min(active, key=lambda item: (item[0], item[2], item[1]))
        if active
        else None
    )
    selected_scalar = (
        accumulator.get(blob(selected), 0) if selected is not None else 0
    )
    direct_scalar = 0
    if selected is not None:
        for descriptor in descriptors:
            if public_boundary_key(descriptor) == selected:
                direct_scalar += (
                    descriptor["coefficient"]
                    * values[blob(descriptor["dual_key"])]
                )
        direct_scalar %= 3
    insist(selected_scalar == direct_scalar, "independent direct scalar")
    return {
        "accumulator": accumulator,
        "contributors": contributors,
        "selected_key": selected,
        "selected_scalar": selected_scalar,
        "direct_scalar": direct_scalar,
        "pair_count": len(descriptors),
    }


def combine_partials(left, right):
    combined = dict(left)
    for key, value in right.items():
        insist(type(value) is int and value in (1, 2), "partial value")
        total = (combined.get(key, 0) + value) % 3
        if total:
            combined[key] = total
        else:
            combined.pop(key, None)
    return {key: combined[key] for key in sorted(combined)}


def independent_run(dual, descriptors, worker_count, shards):
    cover = independent_intervals(len(descriptors), worker_count)
    insist(isinstance(shards, list) and len(shards) == worker_count, "shard roster")
    observed = [
        [shard.get("start"), shard.get("stop")]
        if isinstance(shard, dict)
        else [None, None]
        for shard in shards
    ]
    insist(observed == cover, "ordered shard cover")
    accumulator = {}
    contributors = {}
    pair_count = 0
    for shard, interval in zip(shards, cover):
        replay_shard(shard, dual, descriptors, interval[0], interval[1])
        pair_count += shard["count"]
        accumulator = combine_partials(accumulator, shard["partial"])
        for key, records in shard["contributors"].items():
            contributors.setdefault(key, []).extend(copy.deepcopy(records))
    contributors = {key: contributors[key] for key in sorted(contributors)}
    insist(pair_count == len(descriptors), "pair total")
    serial = independent_serial(descriptors, dual)
    body = {
        "worker_count": worker_count,
        "dual_digest": object_sha(dual),
        "descriptor_digest": object_sha(descriptors),
        "cover": cover,
        "shards": copy.deepcopy(shards),
        "completed_shard_count": worker_count,
        "pair_count": pair_count,
        "accumulator": accumulator,
        "contributors": contributors,
        "selected_key": serial["selected_key"],
        "selected_scalar": serial["selected_scalar"],
        "direct_scalar": serial["direct_scalar"],
        "batch_complete": True,
        "checkpoint_state": None,
    }
    result = {**body, "merge_digest": object_sha(body)}
    insist(
        {
            key: result[key]
            for key in (
                "accumulator",
                "contributors",
                "selected_key",
                "selected_scalar",
                "direct_scalar",
                "pair_count",
            )
        }
        == serial,
        "independent serial parity",
    )
    return result


def audit_run(run, dual, descriptors, worker_count):
    insist(isinstance(run, dict) and set(run) == RUN_FIELDS, "run fields")
    insist(run.get("worker_count") == worker_count, "worker metadata")
    insist(run.get("batch_complete") is True, "incomplete batch")
    insist(run.get("checkpoint_state") is None, "checkpointed partial")
    expected = independent_run(
        dual, descriptors, worker_count, run.get("shards")
    )
    insist(run == expected, "independent run replay")


def fixture_contract():
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


def read_fixture(path_value):
    path = Path(path_value)
    insist(
        not path.is_absolute()
        and ".." not in path.parts
        and (
            path.as_posix().startswith("search/certs/")
            or path.as_posix().startswith("ci/in/")
        ),
        "fixture path",
    )
    fixture = json.loads((ROOT / path).read_text(encoding="ascii"))
    insist(fixture == fixture_contract(), "fixture contents")
    return fixture


def selected_contributor_indices(serial, selected_key):
    return [
        record["pair_index"]
        for record in serial["contributors"].get(blob(selected_key), [])
    ]


def audit_outcome(name, case, expected):
    serial = case["serial"]
    descriptors = case["descriptors"]
    insist(case["outcome"] == expected, "case outcome")
    insist(
        expected.get("selected_key") == serial["selected_key"]
        and expected.get("selected_scalar") == serial["selected_scalar"],
        "outcome/serial binding",
    )
    if name == "active_two_shards":
        cut = independent_intervals(len(descriptors), 2)[0][1]
        indices = selected_contributor_indices(serial, expected["selected_key"])
        insist(
            any(index < cut for index in indices)
            and any(index >= cut for index in indices),
            "two-shard selected contributor",
        )
    elif name == "cancel_across_shards":
        cancelled_blob = blob(expected["cancelled_key"])
        cut = independent_intervals(len(descriptors), 2)[0][1]
        indices = [
            record["pair_index"]
            for record in serial["contributors"].get(cancelled_blob, [])
        ]
        insist(
            cancelled_blob not in serial["accumulator"]
            and any(index < cut for index in indices)
            and any(index >= cut for index in indices),
            "cross-shard cancellation",
        )
    elif name == "nontrivial_lex_winner":
        insist(
            blob(expected["selected_key"]) in serial["accumulator"]
            and blob(expected["competing_key"]) in serial["accumulator"]
            and expected["selected_key"][1] > expected["competing_key"][1]
            and expected["selected_key"][2] < expected["competing_key"][2],
            "v3 lex winner",
        )
    elif name == "no_active_key":
        insist(
            serial["accumulator"] == {}
            and serial["selected_key"] is None
            and serial["selected_scalar"] == serial["direct_scalar"] == 0,
            "no active key",
        )
    else:
        raise CheckError("unexpected case name")


def audit_cases(cases, fixture):
    insist(
        isinstance(cases, list)
        and [case.get("name") for case in cases] == list(CASE_NAMES),
        "case roster",
    )
    for case in cases:
        insist(
            isinstance(case, dict)
            and set(case)
            == {"name", "dual", "descriptors", "serial", "runs", "outcome"},
            "case object",
        )
        name = case["name"]
        dual = case["dual"]
        descriptors = case["descriptors"]
        insist(
            case["serial"] == independent_serial(descriptors, dual),
            "independent serial case",
        )
        insist(
            isinstance(case["runs"], dict)
            and set(case["runs"]) == {str(value) for value in WORKER_COUNTS},
            "all worker counts",
        )
        for worker_count in WORKER_COUNTS:
            run = case["runs"][str(worker_count)]
            audit_run(run, dual, descriptors, worker_count)
            for shard in run["shards"]:
                insist(shard["worker_failed"] is False, "all-worker failure check")
        audit_outcome(
            name, case, fixture["case_expectations"][name]
        )


def epoch_digest(runs, isolated):
    return object_sha({"runs": runs, "state_isolated": isolated})


def audit_epochs(epochs, driver_worker_count, descriptors):
    insist(
        isinstance(epochs, dict)
        and set(epochs) == {"runs", "state_isolated", "isolation_digest"},
        "epoch envelope",
    )
    runs = epochs["runs"]
    insist(isinstance(runs, list) and len(runs) == 2, "epoch count")
    insist(
        [run.get("epoch_index") for run in runs] == [1, 2],
        "epoch ordering",
    )
    for run in runs:
        insist(
            isinstance(run, dict)
            and set(run) == {"epoch_index", "dual", "serial", "parallel"},
            "epoch record",
        )
        serial = independent_serial(descriptors, run["dual"])
        insist(run["serial"] == serial, "epoch serial")
        audit_run(
            run["parallel"], run["dual"], descriptors, driver_worker_count
        )
    insist(
        runs[0]["dual"] != runs[1]["dual"]
        and runs[0]["serial"] != runs[1]["serial"],
        "different epochs",
    )
    insist(epochs["state_isolated"] is True, "isolation flag")
    insist(
        epochs["isolation_digest"]
        == epoch_digest(runs, epochs["state_isolated"]),
        "isolation digest",
    )
    second_digest = object_sha(runs[1]["dual"])
    insist(
        all(
            shard["dual_digest"] == second_digest
            for shard in runs[1]["parallel"]["shards"]
        ),
        "stale epoch",
    )


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


def semantic_payload(receipt):
    return {field: copy.deepcopy(receipt[field]) for field in SEMANTIC_DIGEST_FIELDS}


def reseal(receipt):
    receipt["input_digest"] = object_sha(semantic_payload(receipt))
    receipt.pop("self_digest_sha256", None)
    receipt["self_digest_sha256"] = object_sha(receipt)


def audit_seal(receipt):
    insist(isinstance(receipt, dict), "receipt object")
    body = dict(receipt)
    claimed = body.pop("self_digest_sha256", None)
    insist(isinstance(claimed, str) and claimed == object_sha(body), "receipt seal")


def audit_semantics(receipt, fixture):
    audit_seal(receipt)
    insist(
        set(receipt)
        == set(SEMANTIC_DIGEST_FIELDS)
        | {"input_digest", "mutation_controls", "self_digest_sha256"},
        "selftest receipt shape",
    )
    insist(
        receipt.get("schema") == SELF_SCHEMA
        and receipt.get("status") == "PASS"
        and receipt.get("terminal") == PASS_TERMINAL,
        "selftest envelope",
    )
    insist(
        receipt.get("fixture_digest") == object_sha(fixture),
        "fixture binding",
    )
    insist(
        receipt.get("parallel_boundary") is True
        and receipt.get("single_process") is False,
        "parallel flags",
    )
    driver_worker_count = receipt.get("driver_worker_count")
    insist(driver_worker_count in WORKER_COUNTS, "driver worker count")
    insist(
        receipt.get("worker_counts") == list(WORKER_COUNTS)
        and receipt.get("case_names") == list(CASE_NAMES),
        "declared rosters",
    )
    insist(
        receipt.get("input_digest") == object_sha(semantic_payload(receipt)),
        "semantic digest",
    )
    audit_cases(receipt.get("cases"), fixture)
    audit_epochs(
        receipt.get("epochs"),
        driver_worker_count,
        receipt["cases"][0]["descriptors"],
    )
    insist(
        receipt.get("monitor") == expected_monitor(driver_worker_count),
        "monitor metadata",
    )
    insist(receipt.get("checkpoint_state") is None, "selftest checkpoint")
    insist(receipt.get("claims") == FALSE_CLAIMS, "claims boundary")
    insist(isinstance(receipt.get("mutation_controls"), dict), "mutation field")


def refresh_shard(shard):
    body = {field: copy.deepcopy(shard[field]) for field in SHARD_BODY_FIELDS}
    shard["result_digest"] = object_sha(body)


def refresh_run(run):
    body = {field: copy.deepcopy(run[field]) for field in RUN_BODY_FIELDS}
    run["merge_digest"] = object_sha(body)


def refresh_epochs(epochs):
    epochs["isolation_digest"] = epoch_digest(
        epochs["runs"], epochs["state_isolated"]
    )


def mutate_independently(receipt, name):
    run = receipt["cases"][0]["runs"]["2"]
    descriptors = receipt["cases"][0]["descriptors"]
    if name == "omitted_shard":
        run["shards"].pop()
        run["cover"].pop()
        run["completed_shard_count"] -= 1
        refresh_run(run)
    elif name == "duplicated_shard":
        run["shards"].append(copy.deepcopy(run["shards"][0]))
        run["cover"].append(copy.deepcopy(run["cover"][0]))
        run["completed_shard_count"] += 1
        refresh_run(run)
    elif name == "overlapping_interval":
        shard = run["shards"][1]
        shard["start"] = run["shards"][0]["stop"] - 1
        shard["count"] = shard["stop"] - shard["start"]
        shard["interval_digest"] = independent_interval_digest(
            descriptors, shard["start"], shard["stop"]
        )
        run["cover"][1] = [shard["start"], shard["stop"]]
        refresh_shard(shard)
        refresh_run(run)
    elif name == "gap":
        shard = run["shards"][1]
        shard["start"] = run["shards"][0]["stop"] + 1
        shard["count"] = shard["stop"] - shard["start"]
        shard["interval_digest"] = independent_interval_digest(
            descriptors, shard["start"], shard["stop"]
        )
        run["cover"][1] = [shard["start"], shard["stop"]]
        refresh_shard(shard)
        refresh_run(run)
    elif name == "permuted_pair_order":
        descriptors[0], descriptors[1] = descriptors[1], descriptors[0]
    elif name == "wrong_dual_digest":
        shard = run["shards"][0]
        shard["dual_digest"] = "checker-wrong:" + shard["dual_digest"]
        refresh_shard(shard)
        refresh_run(run)
    elif name == "wrong_descriptor_digest":
        shard = run["shards"][0]
        shard["descriptor_digest"] = "checker-wrong:" + shard["descriptor_digest"]
        refresh_shard(shard)
        refresh_run(run)
    elif name == "changed_coefficient":
        descriptors[0]["coefficient"] = (
            descriptors[0]["coefficient"] + 1
        ) % 3
    elif name == "changed_translation_key":
        descriptors[0]["translation_blob"] += "-checker-mutated"
    elif name == "changed_contributor":
        shard = run["shards"][0]
        contributor_key = sorted(shard["contributors"])[0]
        contributor = shard["contributors"][contributor_key][0]
        contributor["coefficient"] = (contributor["coefficient"] % 2) + 1
        refresh_shard(shard)
        refresh_run(run)
    elif name == "wrong_mod3_merge":
        selected_blob = blob(run["selected_key"])
        run["accumulator"][selected_blob] = (
            run["accumulator"][selected_blob] % 2
        ) + 1
        refresh_run(run)
    elif name == "zero_kept_active":
        zero_blob = blob([9, 9, "zero-checker"])
        shard = run["shards"][0]
        shard["partial"][zero_blob] = 0
        run["accumulator"][zero_blob] = 0
        refresh_shard(shard)
        refresh_run(run)
    elif name == "wrong_lex_winner":
        lex_run = receipt["cases"][2]["runs"]["2"]
        competitor = [1, 1, "b"]
        lex_run["selected_key"] = competitor
        lex_run["selected_scalar"] = lex_run["accumulator"][blob(competitor)]
        lex_run["direct_scalar"] = lex_run["selected_scalar"]
        refresh_run(lex_run)
    elif name == "wrong_direct_scalar":
        run["direct_scalar"] = (run["direct_scalar"] + 1) % 3
        refresh_run(run)
    elif name == "wrong_pair_count":
        shard = run["shards"][0]
        shard["count"] += 1
        run["pair_count"] += 1
        refresh_shard(shard)
        refresh_run(run)
    elif name == "stale_epoch":
        receipt["epochs"]["runs"][1]["epoch_index"] = 1
        refresh_epochs(receipt["epochs"])
    elif name == "worker_failure_accepted":
        shard = run["shards"][0]
        shard["worker_failed"] = True
        refresh_shard(shard)
        refresh_run(run)
    elif name == "incomplete_batch_checkpointed":
        run["batch_complete"] = False
        run["checkpoint_state"] = {
            "safe": True,
            "partial_accumulator_serialized": True,
        }
        refresh_run(run)
    elif name == "single_process_true":
        receipt["single_process"] = True
    elif name == "worker_count_outside_range":
        run["worker_count"] = 1
        refresh_run(run)
    else:
        raise CheckError("unknown mutation")


def effect_digest(receipt):
    return object_sha(semantic_payload(receipt))


def independent_mutation_audit(receipt, fixture):
    baseline = effect_digest(receipt)
    effects = []
    for name in MUTATIONS:
        mutant = copy.deepcopy(receipt)
        mutate_independently(mutant, name)
        reseal(mutant)
        changed = effect_digest(mutant)
        insist(changed != baseline, "checker mutation no-op: " + name)
        rejected = False
        reason = ""
        try:
            audit_semantics(mutant, fixture)
        except (CheckError, KeyError, TypeError, ValueError) as error:
            rejected = True
            reason = type(error).__name__ + ":" + str(error)
        insist(rejected, "checker mutation survived: " + name)
        effects.append(
            {
                "name": name,
                "baseline_digest": baseline,
                "mutant_digest": changed,
                "rejected": True,
                "reason_digest": hashlib.sha256(reason.encode("utf-8")).hexdigest(),
            }
        )
    return effects


def audit_production_stop(receipt):
    audit_seal(receipt)
    insist(
        isinstance(receipt, dict)
        and set(receipt)
        == {
            "schema",
            "status",
            "terminal",
            "reason",
            "resume_path",
            "adapter_commissioned",
            "parallel_boundary",
            "single_process",
            "worker_count",
            "claims",
            "self_digest_sha256",
        },
        "production stop shape",
    )
    insist(
        receipt["schema"] == PRODUCTION_SCHEMA
        and receipt["status"] == "UNKNOWN_INPUT"
        and receipt["terminal"] in (UNKNOWN_ADAPTER, UNKNOWN_RESUME),
        "production stop terminal",
    )
    insist(
        receipt["adapter_commissioned"] is False
        and receipt["parallel_boundary"] is True
        and receipt["single_process"] is False
        and receipt["worker_count"] in WORKER_COUNTS
        and receipt["claims"] == FALSE_CLAIMS,
        "production stop boundary",
    )
    if receipt["terminal"] == UNKNOWN_ADAPTER:
        resume = Path(receipt["resume_path"])
        insist(
            not resume.is_absolute()
            and resume.as_posix().startswith("ci/in/")
            and ".." not in resume.parts,
            "production resume identity",
        )


def write_fresh(path_value, value):
    path = Path(path_value)
    insist(
        not path.is_absolute()
        and path.as_posix().startswith("ci/out/")
        and ".." not in path.parts,
        "checker output path",
    )
    target = ROOT / path
    insist(not target.exists(), "checker stale output")
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("xb") as stream:
        stream.write(encoded(value) + b"\n")


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
    parser.add_argument("--receipt", required=True)
    parser.add_argument("--output")
    args = parser.parse_args(argv)
    try:
        receipt_path = Path(args.receipt)
        insist(
            not receipt_path.is_absolute()
            and receipt_path.as_posix().startswith("ci/out/")
            and ".." not in receipt_path.parts,
            "receipt path",
        )
        receipt = json.loads((ROOT / receipt_path).read_text(encoding="ascii"))
        if args.mode == "SELFTEST":
            fixture = read_fixture(args.fixture)
            audit_semantics(receipt, fixture)
            effects = independent_mutation_audit(receipt, fixture)
            insist(
                len(effects) == len(MUTATIONS)
                and all(effect["rejected"] is True for effect in effects),
                "independent mutation count",
            )
            verdict = {
                "schema": SCHEMA + "/checker-selftest",
                "status": "PASS",
                "terminal": PASS_TERMINAL,
                "producer_digest": object_sha(receipt),
                "case_names": list(CASE_NAMES),
                "worker_counts": list(WORKER_COUNTS),
                "epoch_runs": 2,
                "state_isolated": True,
                "mutation_attempted": len(effects),
                "mutation_rejected": len(effects),
                "mutation_effects": effects,
                "claims": copy.deepcopy(FALSE_CLAIMS),
            }
            verdict["self_digest_sha256"] = object_sha(verdict)
            if args.output:
                write_fresh(args.output, verdict)
            print(PASS_MARKER, flush=True)
            print(TERMINAL_PREFIX, PASS_TERMINAL, flush=True)
            return 0
        audit_production_stop(receipt)
        verdict = {
            "schema": SCHEMA + "/checker-production-stop",
            "status": "PASS",
            "terminal": receipt["terminal"],
            "producer_digest": object_sha(receipt),
            "claims": copy.deepcopy(FALSE_CLAIMS),
        }
        verdict["self_digest_sha256"] = object_sha(verdict)
        if args.output:
            write_fresh(args.output, verdict)
        print(TERMINAL_PREFIX, receipt["terminal"], flush=True)
        return 0
    except (
        CheckError,
        KeyError,
        TypeError,
        ValueError,
        OSError,
        UnicodeError,
        json.JSONDecodeError,
    ) as error:
        print(
            TERMINAL_PREFIX,
            "UNKNOWN_INPUT:checker_reject:" + type(error).__name__,
            flush=True,
        )
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
