#!/usr/bin/env python3
"""Independent checker for the cached-v3 persistent boundary adapter."""
from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "d972-r07-normalized-exact-common-word-cached-parallel/v4"
SELF_SCHEMA = SCHEMA + "/selftest"
PRODUCTION_SCHEMA = SCHEMA + "/production"
FIXTURE_SCHEMA = SCHEMA + "/fixture/v4"
PASS_MARKER = "R07_NORMALIZED_EXACT_COMMON_WORD_CACHED_PARALLEL_V4_CHECKER_PASS"
TERMINAL_PREFIX = "R07_NORMALIZED_EXACT_COMMON_WORD_CACHED_PARALLEL_V4_CHECKER_TERMINAL"
PASS_TERMINAL = "PASS"
COMMON_TERMINAL = "R07_NORMALIZED_EXACT_CACHED_COLGEN_V3_COMMON_WORD"
WORKER_COUNTS = (2, 3, 4)
POOL_WORKER_COUNT = 4
CASE_NAMES = (
    "active_two_shards",
    "cancel_across_shards",
    "nontrivial_lex_winner",
    "no_active_key",
)
MUTATIONS = (
    "omitted_shard", "duplicated_shard", "overlapping_interval", "gap",
    "permuted_pair_order", "wrong_dual_digest", "wrong_descriptor_digest",
    "changed_coefficient", "changed_translation_key", "changed_contributor",
    "wrong_partial", "wrong_mod3_merge", "zero_kept_active", "wrong_lex_winner",
    "wrong_direct_scalar", "wrong_pair_count", "stale_epoch",
    "worker_failure_accepted", "incomplete_batch_checkpointed",
    "single_process_true", "worker_count_outside_range", "pid_replacement",
    "dishonest_rss",
)
FALSE_CLAIMS = {
    "common_word": False,
    "separator": False,
    "finite_common_word": False,
    "cofinal_lift": False,
    "fake": False,
    "ihara_witness": False,
}
ORDER_VERSION = "v3-descriptor-outer-support-insertion-expanded-pairs-v1"
F3_ENCODING = "integer-residue-mod-3-delete-zero"
WINNER_ORDER_VERSION = "(block,translation_blob,relator_index)"
RSS_POLICY = "parent_peak_bytes + sum(child_peak_bytes); unknown RSS stops"
SEMANTIC_FIELDS = (
    "schema", "status", "terminal", "fixture_digest", "parallel_boundary",
    "single_process", "driver_worker_count", "worker_counts", "case_names",
    "cases", "epochs", "pool", "monitor", "resource", "checkpoint_state",
    "claims",
)
SHARD_BODY_FIELDS = {
    "worker_id", "pid", "start", "stop", "count", "interval_digest",
    "epoch_digest", "pair_roster_digest", "partial", "contributors",
    "worker_failed", "rss_known", "rss_peak_bytes",
}
SHARD_FIELDS = SHARD_BODY_FIELDS | {"result_digest"}
RUN_BODY_FIELDS = {
    "worker_count", "epoch_digest", "pair_roster_digest", "pair_count",
    "cover", "shards", "completed_shard_count", "accumulator",
    "contributors", "selected_key", "selected_scalar", "direct_scalar",
    "batch_complete", "checkpoint_state", "physical",
}
RUN_FIELDS = RUN_BODY_FIELDS | {"merge_digest"}
V3_CHECKER_PIN = (
    "crosscheck/check_d972_r07_normalized_exact_common_word_cached_v3.py",
    154009,
    "dfc8cbbd96a1da45f15e01607ed343b66a78a7201f4a80952fba33aaeb361e10",
)
CHECKPOINT_ZIP = (
    "ci/in/d972_r07_normalized_exact_common_word_cached_v3_run33149728601_checkpoint.zip",
    5001811,
    "f3ac82a04907983d987cc2a42d06fe3b612ec2040555f40be81200969358f566",
)
CHECKPOINT_MANIFEST = (
    "ci/in/d972_r07_normalized_exact_common_word_cached_v3_run33149728601_checkpoint.manifest.json",
    1328,
    "6911dfe822662a17ae95c896f97573e553d15325631f1606bd0bf7f550e88302",
)
CHECKPOINT_MEMBER = "d972_r07_normalized_exact_common_word_cached_v3.json.checkpoint.json"
CHECKPOINT_RAW_BYTES = 86368039
CHECKPOINT_RAW_SHA = "c261aa967867a4870228eae467f46ee4afbfc236445890debd891bcef4a250ab"


class CheckError(RuntimeError):
    pass


def insist(condition, message):
    if not condition:
        raise CheckError(message)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True).encode("ascii")


def object_sha(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def blob(value):
    return canonical(value).decode("ascii")


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def f3(value):
    return int(value) % 3


def intervals(total, worker_count):
    insist(worker_count in WORKER_COUNTS and type(total) is int and
           total >= worker_count, "interval cardinality")
    return [[worker * total // worker_count,
             (worker + 1) * total // worker_count]
            for worker in range(worker_count)]


def interval_digest(pairs, start, stop):
    return object_sha({
        "start": start, "stop": stop,
        "pair_indices": [item["pair_index"] for item in pairs[start:stop]],
        "slice_digest": object_sha(pairs[start:stop]),
    })


def fixture_expected():
    return {
        "schema": FIXTURE_SCHEMA,
        "case_names": list(CASE_NAMES),
        "epoch_runs": 3,
        "worker_counts": list(WORKER_COUNTS),
        "mutation_names": list(MUTATIONS),
        "parallel_boundary": True,
        "single_process": False,
        "expanded_pair_sharding": True,
        "case_expectations": {
            "active_two_shards": {
                "selected_key": [1, "t01", 1],
                "selected_scalar": 1,
                "w2_crosses_cut": True,
                "typed_support_concentrated_under_descriptor": True,
            },
            "cancel_across_shards": {
                "selected_key": [2, "t01", 2],
                "selected_scalar": 1,
                "cancelled_key": [1, "t01", 1],
            },
            "nontrivial_lex_winner": {
                "selected_key": [1, "t01", 2],
                "selected_scalar": 1,
                "competing_key": [1, "t02", 1],
            },
            "no_active_key": {"selected_key": None, "selected_scalar": 0},
        },
        "claims": copy.deepcopy(FALSE_CLAIMS),
    }


def read_fixture(path_value):
    path = Path(path_value)
    insist(not path.is_absolute() and ".." not in path.parts and
           (path.as_posix().startswith("search/certs/") or
            path.as_posix().startswith("ci/in/")), "fixture path")
    value = json.loads((ROOT / path).read_text(encoding="ascii"))
    insist(value == fixture_expected(), "fixture contract")
    return value


def fixture_descriptors(name):
    def descriptor(index, block, relator, component, h, base=1):
        return {"descriptor_index": index, "block": block,
                "relator_index": relator, "component": component, "h": h,
                "base_coefficient": base}

    if name == "active_two_shards":
        descriptors = [descriptor(0, 1, 1, 1, 2),
                       descriptor(1, 1, 2, 2, 4),
                       descriptor(2, 2, 1, 3, 6),
                       descriptor(3, 2, 2, 4, 8)]
        dual = [{"block": 1, "component": 1, "g": value,
                 "lambda_coefficient": 1}
                for value in (3, 5, 7, 9, 11, 20, 15, 0)]
    elif name == "cancel_across_shards":
        descriptors = [descriptor(0, 1, 1, 1, 2, 1),
                       descriptor(1, 2, 2, 3, 5, 1),
                       descriptor(2, 1, 1, 2, 3, 2),
                       descriptor(3, 2, 2, 4, 6, 0)]
        dual = [{"block": 1, "component": 1, "g": 3,
                 "lambda_coefficient": 1},
                {"block": 1, "component": 2, "g": 4,
                 "lambda_coefficient": 1},
                {"block": 2, "component": 3, "g": 6,
                 "lambda_coefficient": 1},
                {"block": 2, "component": 4, "g": 7,
                 "lambda_coefficient": 1}]
    elif name == "nontrivial_lex_winner":
        descriptors = [descriptor(0, 1, 2, 1, 2),
                       descriptor(1, 1, 1, 2, 2),
                       descriptor(2, 2, 1, 3, 4),
                       descriptor(3, 2, 2, 4, 5)]
        dual = [{"block": 1, "component": 1, "g": 3,
                 "lambda_coefficient": 1},
                {"block": 1, "component": 2, "g": 4,
                 "lambda_coefficient": 1},
                {"block": 2, "component": 3, "g": 5,
                 "lambda_coefficient": 0},
                {"block": 2, "component": 4, "g": 6,
                 "lambda_coefficient": 0}]
    elif name == "no_active_key":
        descriptors = [descriptor(0, 1, 1, 1, 2, 1),
                       descriptor(1, 1, 1, 2, 3, 2),
                       descriptor(2, 2, 1, 3, 4, 1),
                       descriptor(3, 2, 1, 4, 5, 2)]
        dual = [{"block": 1, "component": 1, "g": 3,
                 "lambda_coefficient": 1},
                {"block": 1, "component": 2, "g": 4,
                 "lambda_coefficient": 1},
                {"block": 2, "component": 3, "g": 5,
                 "lambda_coefficient": 1},
                {"block": 2, "component": 4, "g": 6,
                 "lambda_coefficient": 1}]
    else:
        raise CheckError("unknown fixture case")
    return descriptors, dual


def fixture_pairs(descriptors, dual):
    support = {}
    for index, record in enumerate(dual):
        support.setdefault((record["block"], record["component"]), []).append(
            {"support_index": index, **record})
    pairs = []
    for descriptor in descriptors:
        for record in support.get((descriptor["block"], descriptor["component"]), []):
            pairs.append({
                "mode": "fixture", "pair_index": len(pairs),
                "descriptor_index": descriptor["descriptor_index"],
                "support_index": record["support_index"],
                "block": descriptor["block"],
                "relator_index": descriptor["relator_index"],
                "component": descriptor["component"], "h": descriptor["h"],
                "g": record["g"],
                "base_coefficient": descriptor["base_coefficient"],
                "lambda_coefficient": record["lambda_coefficient"],
            })
    insist(pairs and len(pairs) >= 4, "fixture pair roster")
    return pairs


def pair_key(pair):
    return [int(pair["block"]),
            f"t{(int(pair['g']) - int(pair['h'])) % 17:02d}",
            int(pair["relator_index"])]


def pair_contribution(pair):
    return f3(int(pair["base_coefficient"]) *
              int(pair["lambda_coefficient"]))


def contributor_record(pair):
    return {
        "pair_index": int(pair["pair_index"]),
        "component": int(pair["component"]),
        "g_hex": (pair["g_hex"] if "g_hex" in pair else
                   f"{int(pair['g']):02x}"),
        "h_hex": (pair["h_hex"] if "h_hex" in pair else
                   f"{int(pair['h']):02x}"),
        "lambda_coefficient": int(pair["lambda_coefficient"]),
        "base_coefficient": f3(pair["base_coefficient"]),
    }


def serial_projection(pairs):
    accumulator = {}
    contributors = {}
    for pair in pairs:
        key = blob(pair_key(pair))
        coefficient = pair_contribution(pair)
        if coefficient:
            total = (accumulator.get(key, 0) + coefficient) % 3
            if total:
                accumulator[key] = total
            else:
                accumulator.pop(key, None)
        contributors.setdefault(key, []).append(contributor_record(pair))
    accumulator = {key: accumulator[key] for key in sorted(accumulator)}
    contributors = {key: contributors[key] for key in sorted(contributors)}
    active = [json.loads(key) for key, value in accumulator.items() if value]
    selected = (min(active, key=lambda value: (value[0], value[1], value[2]))
                if active else None)
    selected_blob = blob(selected) if selected is not None else None
    scalar = accumulator.get(selected_blob, 0) if selected_blob else 0
    return {"accumulator": accumulator, "contributors": contributors,
            "selected_key": selected, "selected_scalar": scalar,
            "direct_scalar": scalar, "pair_count": len(pairs)}


def replay_shard(shard, pairs, epoch_digest, pair_roster_digest, start, stop):
    insist(isinstance(shard, dict) and set(shard) == SHARD_FIELDS,
           "shard shape")
    insist(type(shard["worker_id"]) is int and shard["worker_id"] >= 0 and
           type(shard["pid"]) is int and shard["pid"] > 0,
           "worker identity")
    insist(shard["worker_failed"] is False and shard["rss_known"] is True and
           type(shard["rss_peak_bytes"]) is int and
           shard["rss_peak_bytes"] > 0, "worker resource truth")
    expected = {"worker_id": shard["worker_id"], "pid": shard["pid"],
                "start": start, "stop": stop, "count": stop - start,
                "interval_digest": interval_digest(pairs, start, stop),
                "epoch_digest": epoch_digest,
                "pair_roster_digest": pair_roster_digest,
                "partial": {}, "contributors": {},
                "worker_failed": False, "rss_known": True,
                "rss_peak_bytes": shard["rss_peak_bytes"]}
    for pair in pairs[start:stop]:
        key = blob(pair_key(pair))
        coefficient = pair_contribution(pair)
        if coefficient:
            total = (expected["partial"].get(key, 0) + coefficient) % 3
            if total:
                expected["partial"][key] = total
            else:
                expected["partial"].pop(key, None)
        expected["contributors"].setdefault(key, []).append(
            contributor_record(pair))
    expected["partial"] = {key: expected["partial"][key]
                            for key in sorted(expected["partial"])}
    expected["contributors"] = {key: expected["contributors"][key]
                                 for key in sorted(expected["contributors"])}
    insist(shard == {**expected, "result_digest": object_sha(expected)},
           "independent shard replay")


def add_f3(left, right):
    result = dict(left)
    insist(isinstance(right, dict), "partial map")
    for key, value in right.items():
        insist(type(value) is int and value in (1, 2), "partial F3 value")
        total = (result.get(key, 0) + value) % 3
        if total:
            result[key] = total
        else:
            result.pop(key, None)
    return {key: result[key] for key in sorted(result)}


def validate_physical(physical, run, pool):
    fields = {
        "process_parallel", "single_process", "pool_worker_count",
        "requested_worker_count", "worker_pids", "stable_pid_roster",
        "pid_replacements", "parent_peak_rss_bytes", "child_peak_rss_bytes",
        "aggregate_peak_rss_bytes", "rss_known", "aggregate_rss_policy",
        "wall_before_launch_checked", "wall_after_return_checked",
        "elapsed_seconds",
    }
    insist(isinstance(physical, dict) and set(physical) == fields,
           "physical fields")
    workers = run["worker_count"]
    shard_pids = [shard["pid"] for shard in run["shards"]]
    insist(physical["process_parallel"] is True and
           physical["single_process"] is False and
           physical["pool_worker_count"] == pool["worker_count"] and
           physical["requested_worker_count"] == workers and
           physical["worker_pids"] == shard_pids and
           len(shard_pids) == workers and len(set(shard_pids)) == workers and
           physical["stable_pid_roster"] == pool["stable_pid_roster"] and
           set(shard_pids).issubset(set(pool["stable_pid_roster"])) and
           physical["pid_replacements"] == 0 and
           type(physical["parent_peak_rss_bytes"]) is int and
           physical["parent_peak_rss_bytes"] > 0 and
           isinstance(physical["child_peak_rss_bytes"], list) and
           len(physical["child_peak_rss_bytes"]) == workers and
           all(type(value) is int and value > 0
               for value in physical["child_peak_rss_bytes"]) and
           physical["aggregate_peak_rss_bytes"] ==
           physical["parent_peak_rss_bytes"] +
           sum(physical["child_peak_rss_bytes"]) and
           physical["rss_known"] is True and
           physical["aggregate_rss_policy"] == RSS_POLICY and
           physical["wall_before_launch_checked"] is True and
           physical["wall_after_return_checked"] is True and
           type(physical["elapsed_seconds"]) in (int, float) and
           physical["elapsed_seconds"] >= 0, "physical process truth")


def independent_run(run, pairs, identity, worker_count, pool):
    insist(isinstance(run, dict) and set(run) == RUN_FIELDS | {
        "epoch_identity", "descriptors", "dual", "serial",
        "local_winner_contributors", "pair_roster"}, "run fields")
    epoch_digest = object_sha(identity)
    pair_digest = object_sha(pairs)
    insist(run["worker_count"] == worker_count and
           run["epoch_digest"] == epoch_digest and
           run["pair_roster_digest"] == pair_digest and
           run["pair_count"] == len(pairs) and
           run["epoch_identity"] == identity and
           run["pair_roster"] == pairs and run["batch_complete"] is True and
           run["checkpoint_state"] is None, "run identity")
    cover = intervals(len(pairs), worker_count)
    insist(run["cover"] == cover and len(run["shards"]) == worker_count,
           "ordered shard cover")
    for worker, (shard, interval) in enumerate(zip(run["shards"], cover)):
        insist(shard["worker_id"] == worker, "worker order")
        replay_shard(shard, pairs, epoch_digest, pair_digest,
                     interval[0], interval[1])
    accumulator = {}
    contributors = {}
    for shard in run["shards"]:
        accumulator = add_f3(accumulator, shard["partial"])
        for key, records in shard["contributors"].items():
            contributors.setdefault(key, []).extend(copy.deepcopy(records))
    contributors = {key: contributors[key] for key in sorted(contributors)}
    serial = serial_projection(pairs)
    body = {
        "worker_count": worker_count, "epoch_digest": epoch_digest,
        "pair_roster_digest": pair_digest, "pair_count": len(pairs),
        "cover": cover, "shards": copy.deepcopy(run["shards"]),
        "completed_shard_count": worker_count, "accumulator": accumulator,
        "contributors": contributors, "selected_key": serial["selected_key"],
        "selected_scalar": serial["selected_scalar"],
        "direct_scalar": serial["direct_scalar"], "batch_complete": True,
        "checkpoint_state": None, "physical": copy.deepcopy(run["physical"]),
    }
    expected = {**body, "merge_digest": object_sha(body),
                "epoch_identity": copy.deepcopy(identity),
                "descriptors": copy.deepcopy(run["descriptors"]),
                "dual": copy.deepcopy(run["dual"]), "serial": serial,
                "local_winner_contributors": copy.deepcopy(
                    run["local_winner_contributors"]),
                "pair_roster": copy.deepcopy(pairs)}
    insist(run == expected, "independent map/reduce replay")
    validate_physical(run["physical"], run, pool)
    local = (contributors.get(blob(serial["selected_key"]), [])
             if serial["selected_key"] is not None else [])
    local = [{key: value for key, value in item.items()
              if key != "pair_index"} for item in local]
    insist(run["local_winner_contributors"] == local,
           "local winner contributor order")
    return serial


def audit_fixture_case(case, fixture, pool):
    insist(isinstance(case, dict) and set(case) == {
        "name", "descriptors", "dual", "pair_roster", "serial", "runs",
        "outcome"}, "case shape")
    name = case["name"]
    descriptors, dual = fixture_descriptors(name)
    pairs = fixture_pairs(descriptors, dual)
    insist(case["descriptors"] == descriptors and case["dual"] == dual and
           case["pair_roster"] == pairs, "case fixture binding")
    serial = serial_projection(pairs)
    insist(case["serial"] == serial and case["outcome"] ==
           fixture["case_expectations"][name], "case outcome")
    insist(isinstance(case["runs"], dict) and
           set(case["runs"]) == {str(worker) for worker in WORKER_COUNTS},
           "case worker roster")
    for worker_count in WORKER_COUNTS:
        identity = {
            "dual_digest": object_sha(dual),
            "descriptor_digest": object_sha(descriptors),
            "typed_support_digest": object_sha(dual),
            "pair_roster_digest": object_sha(pairs),
            "pair_count": len(pairs), "pair_order_version": ORDER_VERSION,
            "field": F3_ENCODING, "winner_order_version": WINNER_ORDER_VERSION,
        }
        run = case["runs"][str(worker_count)]
        insist(run["descriptors"] == descriptors and run["dual"] == dual,
               "run fixture binding")
        independent_run(run, pairs, identity, worker_count, pool)
    if name == "active_two_shards":
        insist(len({item["descriptor_index"] for item in pairs}) == 1,
               "support concentration")
        cut = intervals(len(pairs), 2)[0][1]
        indices = [item["pair_index"] for item in serial["contributors"].get(
            blob(serial["selected_key"]), [])]
        insist(any(index < cut for index in indices) and
               any(index >= cut for index in indices), "winner crosses cut")
    elif name == "cancel_across_shards":
        cancelled = blob(case["outcome"]["cancelled_key"])
        cut = intervals(len(pairs), 2)[0][1]
        indices = [item["pair_index"] for item in serial["contributors"].get(
            cancelled, [])]
        insist(cancelled not in serial["accumulator"] and
               any(index < cut for index in indices) and
               any(index >= cut for index in indices), "cross-shard cancel")
    elif name == "nontrivial_lex_winner":
        selected = case["outcome"]["selected_key"]
        competing = case["outcome"]["competing_key"]
        insist(blob(selected) in serial["accumulator"] and
               blob(competing) in serial["accumulator"] and
               selected[1] < competing[1] and selected[2] > competing[2],
               "v3 lex winner")
    else:
        insist(serial["accumulator"] == {} and serial["selected_key"] is None and
               serial["selected_scalar"] == serial["direct_scalar"] == 0,
               "empty active set")


def epoch_dual(index):
    coefficients = ((1, 1, 1, 1, 1, 1, 1, 1) if index == 1 else
                    (2, 2, 2, 2, 2, 2, 2, 2) if index == 2 else
                    (1, 2, 1, 2, 1, 2, 1, 2))
    return [{"block": 1, "component": 1, "g": value,
             "lambda_coefficient": coefficient}
            for value, coefficient in zip(
                (3, 5, 7, 9, 11, 13, 15, 0), coefficients)]


def epoch_identity(descriptors, dual):
    pairs = fixture_pairs(descriptors, dual)
    return {
        "dual_digest": object_sha(dual),
        "descriptor_digest": object_sha(descriptors),
        "typed_support_digest": object_sha(dual),
        "pair_roster_digest": object_sha(pairs), "pair_count": len(pairs),
        "pair_order_version": ORDER_VERSION, "field": F3_ENCODING,
        "winner_order_version": WINNER_ORDER_VERSION,
    }


def audit_epochs(epochs, driver_worker_count, pool):
    insist(isinstance(epochs, dict) and set(epochs) == {
        "runs", "state_isolated", "epoch_digests", "isolation_digest"},
           "epoch envelope")
    insist(isinstance(epochs["runs"], list) and
           [run.get("epoch_index") for run in epochs["runs"]] == [1, 2, 3] and
           len(epochs["epoch_digests"]) == 3 and
           len(set(epochs["epoch_digests"])) == 3 and
           epochs["state_isolated"] is True, "epoch roster")
    descriptors, _ = fixture_descriptors("active_two_shards")
    for index, record in enumerate(epochs["runs"], 1):
        insist(isinstance(record, dict) and set(record) == {
            "epoch_index", "dual", "serial", "parallel"}, "epoch record")
        dual = epoch_dual(index)
        pairs = fixture_pairs(descriptors, dual)
        identity = epoch_identity(descriptors, dual)
        insist(record["dual"] == dual and record["serial"] ==
               serial_projection(pairs), "epoch serial")
        insist(record["parallel"]["descriptors"] == descriptors and
               record["parallel"]["dual"] == dual, "epoch fixture binding")
        independent_run(record["parallel"], pairs, identity,
                         driver_worker_count, pool)
        insist(epochs["epoch_digests"][index - 1] == object_sha(identity),
               "epoch digest")
    insist(epochs["isolation_digest"] == object_sha({
        "runs": epochs["runs"], "state_isolated": epochs["state_isolated"]}),
           "epoch isolation digest")


def expected_monitor(cases, epochs):
    case_pairs = sum(case["runs"]["2"]["pair_count"] for case in cases)
    case_runs = sum(len(case["runs"]) for case in cases)
    epoch_pairs = sum(run["parallel"]["pair_count"] for run in epochs["runs"])
    return {
        "parallel_boundary": True, "single_process": False,
        "worker_counts_exercised": list(WORKER_COUNTS),
        "completed_batch_count": case_runs + len(epochs["runs"]),
        "completed_shard_count": 9 * len(cases) + sum(
            run["parallel"]["completed_shard_count"]
            for run in epochs["runs"]),
        "total_pair_count": case_pairs * 3 + epoch_pairs,
        "boundary_pairs": case_pairs * 3 + epoch_pairs,
        "worker_failures": 0, "aggregate_rss_policy": RSS_POLICY,
    }


def semantic_payload(receipt):
    return {field: copy.deepcopy(receipt[field]) for field in SEMANTIC_FIELDS
            if field in receipt}


def audit_seal(receipt):
    insist(isinstance(receipt, dict) and
           isinstance(receipt.get("self_digest_sha256"), str), "seal field")
    body = dict(receipt)
    claimed = body.pop("self_digest_sha256", None)
    insist(claimed == object_sha(body), "self seal")


def audit_selftest(receipt, fixture, independent_mutations=False):
    audit_seal(receipt)
    insist(set(receipt) == set(SEMANTIC_FIELDS) |
           {"input_digest", "mutation_controls", "self_digest_sha256"},
           "selftest envelope")
    insist(receipt["schema"] == SELF_SCHEMA and receipt["status"] == "PASS" and
           receipt["terminal"] == PASS_TERMINAL and
           receipt["fixture_digest"] == object_sha(fixture) and
           receipt["parallel_boundary"] is True and
           receipt["single_process"] is False and
           receipt["driver_worker_count"] in WORKER_COUNTS and
           receipt["worker_counts"] == list(WORKER_COUNTS) and
           receipt["case_names"] == list(CASE_NAMES) and
           receipt["claims"] == FALSE_CLAIMS and
           receipt["checkpoint_state"] is None, "selftest boundary")
    insist(receipt["input_digest"] == object_sha(semantic_payload(receipt)),
           "semantic digest")
    pool = receipt["pool"]
    insist(isinstance(pool, dict) and set(pool) == {
        "created_count", "close_count", "join_count", "worker_count",
        "stable_pid_roster", "epoch_count", "epoch_digests",
        "aggregate_rss_policy", "terminated"}, "pool shape")
    insist(pool["created_count"] == pool["close_count"] == pool["join_count"] == 1 and
           pool["worker_count"] == POOL_WORKER_COUNT and
           isinstance(pool["stable_pid_roster"], list) and
           len(pool["stable_pid_roster"]) == POOL_WORKER_COUNT and
           len(set(pool["stable_pid_roster"])) == POOL_WORKER_COUNT and
           all(type(pid) is int and pid > 0 for pid in pool["stable_pid_roster"]) and
           pool["aggregate_rss_policy"] == RSS_POLICY and
           pool["terminated"] is False, "persistent pool")
    cases = receipt["cases"]
    insist(isinstance(cases, list) and
           [case.get("name") for case in cases] == list(CASE_NAMES),
           "case roster")
    for case in cases:
        audit_fixture_case(case, fixture, pool)
    audit_epochs(receipt["epochs"], receipt["driver_worker_count"], pool)
    expected_pool_epochs = [case["runs"][str(worker)]["epoch_digest"]
                            for case in cases for worker in WORKER_COUNTS]
    expected_pool_epochs.extend(record["parallel"]["epoch_digest"]
                                for record in receipt["epochs"]["runs"])
    insist(pool["epoch_count"] == len(expected_pool_epochs) and
           pool["epoch_digests"] == expected_pool_epochs,
           "pool epoch transcript")
    insist(receipt["monitor"] == expected_monitor(cases, receipt["epochs"]),
           "monitor counters")
    resource_truth = receipt["resource"]
    insist(isinstance(resource_truth, dict) and set(resource_truth) == {
        "rss_known", "aggregate_rss_policy", "pool_created_once",
        "pool_closed_once", "parent_peak_rss_bytes"} and
           resource_truth["rss_known"] is True and
           resource_truth["aggregate_rss_policy"] == RSS_POLICY and
           resource_truth["pool_created_once"] is True and
           resource_truth["pool_closed_once"] is True and
           type(resource_truth["parent_peak_rss_bytes"]) is int and
           resource_truth["parent_peak_rss_bytes"] > 0, "resource truth")
    controls = receipt["mutation_controls"]
    insist(isinstance(controls, dict) and controls["names"] == list(MUTATIONS) and
           controls["attempted"] == len(MUTATIONS) and
           controls["rejected"] == len(MUTATIONS) and
           len(controls["effects"]) == len(MUTATIONS), "producer mutations")
    baseline = None
    for effect, name in zip(controls["effects"], MUTATIONS):
        insist(isinstance(effect, dict) and set(effect) == {
            "name", "baseline_digest", "mutant_digest", "rejected",
            "reason_digest"} and effect["name"] == name and
               effect["rejected"] is True and
               isinstance(effect["baseline_digest"], str) and
               isinstance(effect["mutant_digest"], str) and
               effect["mutant_digest"] != effect["baseline_digest"] and
               isinstance(effect["reason_digest"], str), "mutation effect shape")
        if baseline is None:
            baseline = effect["baseline_digest"]
        insist(effect["baseline_digest"] == baseline,
               "mutation baseline transcript")
    if independent_mutations:
        effects = independent_mutation_audit(receipt, fixture)
        insist(len(effects) == len(MUTATIONS) and
               all(effect["rejected"] is True for effect in effects),
               "independent mutation suite")
    return pool


def refresh_shard(shard):
    body = {field: copy.deepcopy(shard[field]) for field in SHARD_BODY_FIELDS}
    shard["result_digest"] = object_sha(body)


def refresh_run(run):
    body = {field: copy.deepcopy(run[field]) for field in RUN_BODY_FIELDS}
    run["merge_digest"] = object_sha(body)


def refresh_epochs(epochs):
    epochs["isolation_digest"] = object_sha({
        "runs": epochs["runs"], "state_isolated": epochs["state_isolated"]})


def mutate_independently(receipt, name):
    run = receipt["cases"][0]["runs"]["2"]
    if name == "omitted_shard":
        run["shards"].pop(); run["cover"].pop()
    elif name == "duplicated_shard":
        run["shards"].append(copy.deepcopy(run["shards"][0]))
        run["cover"].append(copy.deepcopy(run["cover"][0]))
    elif name == "overlapping_interval":
        run["shards"][1]["start"] = run["shards"][0]["stop"] - 1
    elif name == "gap":
        run["shards"][1]["start"] = run["shards"][0]["stop"] + 1
    elif name == "permuted_pair_order":
        pairs = run["pair_roster"]
        pairs[0], pairs[1] = pairs[1], pairs[0]
    elif name == "wrong_dual_digest":
        run["shards"][0]["epoch_digest"] = "wrong:" + run["epoch_digest"]
    elif name == "wrong_descriptor_digest":
        run["pair_roster_digest"] = "wrong:" + run["pair_roster_digest"]
    elif name == "changed_coefficient":
        run["pair_roster"][0]["base_coefficient"] = 2
    elif name == "changed_translation_key":
        run["pair_roster"][0]["h"] += 1
    elif name == "changed_contributor":
        key = sorted(run["shards"][0]["contributors"])[0]
        run["shards"][0]["contributors"][key][0]["base_coefficient"] = 2
    elif name == "wrong_partial":
        run["shards"][0]["partial"][blob([1, "t00", 1])] = 1
    elif name == "wrong_mod3_merge":
        key = sorted(run["accumulator"])[0]
        run["accumulator"][key] = (run["accumulator"][key] % 2) + 1
    elif name == "zero_kept_active":
        run["accumulator"][blob([9, "t00", 9])] = 0
    elif name == "wrong_lex_winner":
        lex = receipt["cases"][2]["runs"]["2"]
        lex["selected_key"] = [1, "t02", 1]
    elif name == "wrong_direct_scalar":
        run["direct_scalar"] = (run["direct_scalar"] + 1) % 3
    elif name == "wrong_pair_count":
        run["pair_count"] += 1
    elif name == "stale_epoch":
        receipt["epochs"]["runs"][1]["parallel"]["epoch_digest"] = \
            receipt["epochs"]["runs"][0]["parallel"]["epoch_digest"]
    elif name == "worker_failure_accepted":
        run["shards"][0]["worker_failed"] = True
    elif name == "incomplete_batch_checkpointed":
        run["batch_complete"] = False
        run["checkpoint_state"] = {"safe": True, "partial": True}
    elif name == "single_process_true":
        receipt["single_process"] = True
    elif name == "worker_count_outside_range":
        run["worker_count"] = 1
    elif name == "pid_replacement":
        run["physical"]["worker_pids"][0] += 1
    elif name == "dishonest_rss":
        run["physical"]["aggregate_peak_rss_bytes"] = 1
    else:
        raise CheckError("unknown mutation")


def reseal(receipt):
    receipt["input_digest"] = object_sha(semantic_payload(receipt))
    receipt.pop("self_digest_sha256", None)
    receipt["self_digest_sha256"] = object_sha(receipt)


def independent_mutation_audit(receipt, fixture):
    baseline = object_sha(semantic_payload(receipt))
    effects = []
    for name in MUTATIONS:
        mutant = copy.deepcopy(receipt)
        mutate_independently(mutant, name)
        reseal(mutant)
        changed = object_sha(semantic_payload(mutant))
        insist(changed != baseline, "checker mutation no-op:" + name)
        rejected = False
        reason = ""
        try:
            audit_selftest(mutant, fixture, independent_mutations=False)
        except (CheckError, KeyError, TypeError, ValueError) as error:
            rejected = True
            reason = type(error).__name__ + ":" + str(error)
        insist(rejected, "checker mutation survived:" + name)
        effects.append({"name": name, "baseline_digest": baseline,
                        "mutant_digest": changed, "rejected": True,
                        "reason_digest": digest(reason.encode("utf-8"))})
    return effects


def authenticate_v3_checker():
    rel, size, expected = V3_CHECKER_PIN
    path = ROOT / rel
    raw = path.read_bytes()
    insist(len(raw) == size and digest(raw) == expected,
           "v3 checker pin")
    spec = importlib.util.spec_from_file_location(
        "d972_cached_v3_helper_nonshared_v4", path)
    insist(spec is not None and spec.loader is not None, "v3 checker loader")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def audit_source_artifacts(source):
    insist(isinstance(source, dict) and set(source) == {
        "manifest", "zip_bytes", "zip_sha256", "member", "raw_bytes",
        "raw_sha256", "resume"}, "source artifact shape")
    insist(source["zip_bytes"] == CHECKPOINT_ZIP[1] and
           source["zip_sha256"] == CHECKPOINT_ZIP[2] and
           source["member"] == CHECKPOINT_MEMBER and
           source["raw_bytes"] == CHECKPOINT_RAW_BYTES and
           source["raw_sha256"] == CHECKPOINT_RAW_SHA, "source checkpoint pins")
    manifest = source["manifest"]
    insist(isinstance(manifest, dict) and
           manifest.get("zip", {}).get("member") == CHECKPOINT_MEMBER and
           manifest.get("zip", {}).get("bytes") == CHECKPOINT_ZIP[1] and
           manifest.get("zip", {}).get("sha256") == CHECKPOINT_ZIP[2] and
           manifest.get("raw_checkpoint", {}).get("bytes") == CHECKPOINT_RAW_BYTES and
           manifest.get("raw_checkpoint", {}).get("sha256") == CHECKPOINT_RAW_SHA,
           "manifest binding")
    resume = source["resume"]
    insist(isinstance(resume, dict) and set(resume) == {
        "path", "bytes", "sha256"} and isinstance(resume["path"], str) and
           not Path(resume["path"]).is_absolute() and
           ".." not in Path(resume["path"]).parts and
           (resume["path"] in (CHECKPOINT_ZIP[0], CHECKPOINT_MANIFEST[0]) or
            (resume["path"].startswith("ci/out/") and
             len(Path(resume["path"]).parts) == 3 and
             Path(resume["path"]).name.endswith(".checkpoint.json"))),
           "resume source identity")
    if resume["path"].startswith("ci/out/"):
        resume_path = ROOT / Path(resume["path"])
        insist(resume_path.is_file() and
               len(resume_path.read_bytes()) == resume["bytes"] and
               digest(resume_path.read_bytes()) == resume["sha256"],
               "resume sidecar source identity")
    else:
        insist(resume["bytes"] == CHECKPOINT_RAW_BYTES and
               resume["sha256"] == CHECKPOINT_RAW_SHA,
               "resume archive source identity")


def sidecar_for(receipt_path, reference):
    insist(isinstance(reference, dict) and set(reference) == {
        "path", "bytes", "sha256", "sealed", "adapter_safe",
        "epoch_restart_only"}, "checkpoint reference shape")
    path_value = Path(reference["path"])
    insist(not path_value.is_absolute() and ".." not in path_value.parts and
           len(path_value.parts) == 1, "checkpoint reference path")
    path = Path(receipt_path).parent / path_value
    insist(path.is_file(), "checkpoint sidecar missing")
    raw = path.read_bytes()
    insist(len(raw) == reference["bytes"] and
           digest(raw) == reference["sha256"] and
           reference["sealed"] is True and reference["adapter_safe"] is True and
           reference["epoch_restart_only"] is True, "checkpoint sidecar identity")
    return path, raw


def audit_production(receipt, receipt_path):
    audit_seal(receipt)
    fields = {
        "schema", "status", "terminal", "inner_terminal", "inner_receipt",
        "inner_receipt_digest", "inner_single_process",
        "inner_single_process_legacy_logical_only", "parallel_boundary",
        "single_process", "driver_worker_count", "pool", "epochs",
        "epoch_count", "epoch_digests", "minimum_three_distinct_epochs",
        "resource", "source_artifacts", "base_receipt_digest",
        "base_checkpoint_digest", "checkpoint_state", "claims",
        "input_digest", "self_digest_sha256",
    }
    insist(set(receipt) == fields, "production envelope")
    insist(receipt["schema"] == PRODUCTION_SCHEMA and
           receipt["driver_worker_count"] in WORKER_COUNTS and
           receipt["parallel_boundary"] is True and
           receipt["single_process"] is False and
           receipt["inner_single_process_legacy_logical_only"] is True and
           receipt["claims"] == FALSE_CLAIMS and
           receipt["input_digest"] == object_sha(semantic_payload(receipt)),
           "production boundary")
    terminal = receipt["terminal"]
    if receipt["inner_receipt"] is None:
        insist(receipt["status"] == "UNKNOWN_INPUT" and
               receipt["inner_terminal"] == terminal and
               receipt["inner_receipt_digest"] is None and
               receipt["source_artifacts"] is None and
               receipt["base_receipt_digest"] is None and
               receipt["base_checkpoint_digest"] is None and
               receipt["checkpoint_state"] is None and
               receipt["epochs"] == [] and receipt["epoch_count"] == 0 and
               receipt["epoch_digests"] == [] and
               receipt["minimum_three_distinct_epochs"] is False and
               receipt["pool"]["created_count"] == 0 and
               receipt["resource"]["pool_created_once"] is False,
               "sealed stop envelope")
        return
    inner = receipt["inner_receipt"]
    insist(isinstance(inner, dict) and
           receipt["inner_terminal"] == terminal and
           inner.get("terminal") == terminal and
           receipt["status"] == inner.get("status") and
           receipt["inner_receipt_digest"] == object_sha(inner) and
           receipt["base_receipt_digest"] == object_sha(inner),
           "inner receipt binding")
    helper = authenticate_v3_checker()
    try:
        helper.check_production(inner)
    except Exception as error:
        raise CheckError("pinned v3 checker:" + type(error).__name__) from error
    audit_source_artifacts(receipt["source_artifacts"])
    pool = receipt["pool"]
    insist(isinstance(pool, dict) and set(pool) == {
        "created_count", "close_count", "join_count", "worker_count",
        "stable_pid_roster", "epoch_count", "epoch_digests",
        "aggregate_rss_policy", "terminated"}, "production pool shape")
    epochs = receipt["epochs"]
    insist(isinstance(epochs, list) and receipt["epoch_count"] == len(epochs) and
           receipt["epoch_digests"] == [object_sha(item["epoch_identity"])
                                         for item in epochs] and
           len(set(receipt["epoch_digests"])) == len(epochs) and
           pool["epoch_count"] == len(epochs) and
           pool["epoch_digests"] == [object_sha(item["epoch_identity"])
                                      for item in epochs], "epoch summary")
    has_epochs = bool(epochs)
    insist(pool["worker_count"] == receipt["driver_worker_count"] and
           pool["aggregate_rss_policy"] == RSS_POLICY and
           pool["terminated"] is False and
           pool["created_count"] == pool["close_count"] == pool["join_count"] ==
           (1 if has_epochs else 0) and
           isinstance(pool["stable_pid_roster"], list) and
           (len(pool["stable_pid_roster"]) == pool["worker_count"] if has_epochs
            else pool["stable_pid_roster"] == []) and
           (len(set(pool["stable_pid_roster"])) == pool["worker_count"]
            if has_epochs else True),
           "production persistent pool")
    for item in epochs:
        insist(isinstance(item, dict) and set(item) == {
            "epoch_identity", "epoch_digest", "pair_count", "worker_count",
            "descriptor_count", "typed_support_count", "pair_roster_digest",
            "cover", "shard_metadata", "physical", "batch_complete",
            "selected_key",
            "selected_scalar", "direct_scalar", "local_winner_digest",
            "local_winner_contributors",
        }, "compact epoch record")
        identity = item["epoch_identity"]
        insist(isinstance(identity, dict) and
               item["epoch_digest"] == object_sha(identity) and
               item["worker_count"] == receipt["driver_worker_count"] and
               identity.get("pair_order_version") == ORDER_VERSION and
               identity.get("field") == F3_ENCODING and
               identity.get("winner_order_version") == WINNER_ORDER_VERSION and
               identity.get("descriptor_count") == 104 and
               item["descriptor_count"] == 104 and
               item["pair_count"] == identity.get("pair_count") and
               item["pair_roster_digest"] == identity.get("pair_roster_digest") and
               item["cover"] == intervals(item["pair_count"], item["worker_count"]) and
               item["batch_complete"] is True and
               item["typed_support_count"] > 0 and item["pair_count"] > 0 and
               item["direct_scalar"] == item["selected_scalar"] and
               item["local_winner_digest"] == object_sha({
                   "selected_key": item["selected_key"],
                   "contributors": item["local_winner_contributors"]}) and
               item["selected_scalar"] in (0, 1, 2) and
               isinstance(item["local_winner_contributors"], list),
               "epoch identity")
        shards = item["shard_metadata"]
        insist(isinstance(shards, list) and len(shards) == item["worker_count"],
               "compact shard roster")
        for worker, (shard, interval) in enumerate(zip(shards, item["cover"])):
            insist(isinstance(shard, dict) and set(shard) == {
                "worker_id", "pid", "start", "stop", "count",
                "epoch_digest", "pair_roster_digest", "interval_digest",
                "result_digest", "partial_digest", "contributors_digest",
                "rss_peak_bytes", "worker_failed", "rss_known"},
                "compact shard shape")
            insist(shard["worker_id"] == worker and
                   shard["start"] == interval[0] and
                   shard["stop"] == interval[1] and
                   shard["count"] == interval[1] - interval[0] and
                   shard["epoch_digest"] == item["epoch_digest"] and
                   shard["pair_roster_digest"] == item["pair_roster_digest"] and
                   shard["worker_failed"] is False and
                   shard["rss_known"] is True and
                   type(shard["pid"]) is int and shard["pid"] > 0 and
                   type(shard["rss_peak_bytes"]) is int and
                   shard["rss_peak_bytes"] > 0 and
                   isinstance(shard["partial_digest"], str) and
                   isinstance(shard["contributors_digest"], str) and
                   isinstance(shard["result_digest"], str),
                   "compact shard binding")
        validate_physical(item["physical"], {
            "worker_count": item["worker_count"],
            "shards": [{"pid": shard["pid"]} for shard in shards]}, pool)
        if item["selected_key"] is None:
            insist(item["selected_scalar"] == 0 and
                   item["local_winner_contributors"] == [],
                   "empty epoch winner")
        else:
            key = item["selected_key"]
            insist(isinstance(key, list) and len(key) == 3 and
                   type(key[0]) is int and type(key[1]) is str and
                   type(key[2]) is int and item["selected_scalar"] in (1, 2),
                   "epoch winner key")
            for record in item["local_winner_contributors"]:
                insist(isinstance(record, dict) and set(record) == {
                    "component", "g_hex", "h_hex", "lambda_coefficient",
                    "base_coefficient"}, "winner provenance shape")
            insist(item["local_winner_contributors"], "winner provenance")
    distinct = {item["epoch_identity"].get("dual_digest") for item in epochs}
    insist(receipt["minimum_three_distinct_epochs"] == len(distinct) >= 3,
           "distinct epoch flag")
    resource = receipt["resource"]
    insist(isinstance(resource, dict) and set(resource) == {
        "aggregate_rss_policy", "parent_peak_rss_bytes", "rss_known",
        "wall_checks", "pool_created_once", "pool_closed_once"} and
           resource["aggregate_rss_policy"] == RSS_POLICY and
           resource["rss_known"] is True and resource["wall_checks"] is True and
           resource["pool_created_once"] is has_epochs and
           resource["pool_closed_once"] is has_epochs, "production resource")
    if terminal == COMMON_TERMINAL:
        insist(receipt["checkpoint_state"] is None and
               not (Path(receipt_path).parent /
                    (Path(receipt_path).name + ".checkpoint.json")).exists(),
               "COMMON checkpoint firewall")
    elif terminal.startswith("UNKNOWN_RESOURCE"):
        reference = receipt["checkpoint_state"]
        path, raw = sidecar_for(receipt_path, reference)
        insist(receipt["base_checkpoint_digest"] == digest(raw),
               "resource checkpoint digest")
    else:
        insist(receipt["checkpoint_state"] is None, "unexpected checkpoint")


def write_fresh(path_value, value):
    path = Path(path_value)
    insist(not path.is_absolute() and path.as_posix().startswith("ci/out/") and
           ".." not in path.parts, "checker output path")
    target = ROOT / path
    insist(not target.exists(), "checker stale output")
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("xb") as stream:
        stream.write(canonical(value) + b"\n")


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("SELFTEST", "PRODUCTION"),
                        default="PRODUCTION")
    parser.add_argument("--fixture", default=(
        "search/certs/"
        "d972_r07_normalized_exact_common_word_cached_parallel_selftest_v1_20260828.json"))
    parser.add_argument("--receipt", required=True)
    parser.add_argument("--output")
    args = parser.parse_args(argv)
    try:
        receipt_path = Path(args.receipt)
        insist(not receipt_path.is_absolute() and
               receipt_path.as_posix().startswith("ci/out/") and
               ".." not in receipt_path.parts, "receipt path")
        receipt = json.loads((ROOT / receipt_path).read_text(encoding="ascii"))
        if args.mode == "SELFTEST":
            fixture = read_fixture(args.fixture)
            audit_selftest(receipt, fixture)
            effects = independent_mutation_audit(receipt, fixture)
            verdict = {
                "schema": SCHEMA + "/checker-selftest", "status": "PASS",
                "terminal": PASS_TERMINAL,
                "producer_digest": object_sha(receipt),
                "case_names": list(CASE_NAMES), "worker_counts": list(WORKER_COUNTS),
                "epoch_runs": 3, "state_isolated": True,
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
        audit_production(receipt, receipt_path)
        verdict = {
            "schema": SCHEMA + "/checker-production",
            "status": "PASS", "terminal": receipt["terminal"],
            "producer_digest": object_sha(receipt),
            "claims": copy.deepcopy(FALSE_CLAIMS),
        }
        verdict["self_digest_sha256"] = object_sha(verdict)
        if args.output:
            write_fresh(args.output, verdict)
        print(TERMINAL_PREFIX + " terminal=" + receipt["terminal"], flush=True)
        return 0
    except (CheckError, KeyError, TypeError, ValueError, OSError,
            UnicodeError, json.JSONDecodeError) as error:
        print(TERMINAL_PREFIX,
              "UNKNOWN_INPUT:checker_reject:" + type(error).__name__, flush=True)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
