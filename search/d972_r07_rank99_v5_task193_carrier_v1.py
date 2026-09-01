#!/usr/bin/env python3
"""Positive-only rank-99 v5 discovery to the frozen Task193 carrier ABI."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import re
import stat
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "d972-r07-rank99-v5-task193-carrier/v1"
MARKER = "R07_RANK99_V5_TASK193_CARRIER_V1"
V5P = (
    "search/d972_r07_a0_dual_anchored_rank99_durable_discovery_v5.py",
    104031,
    "25c308ec11b9f36cc9779dfec46058a4956068969d664ee582a26f9cb0db7c09",
)
V5C = (
    "crosscheck/check_d972_r07_a0_dual_anchored_rank99_durable_discovery_v5.py",
    71589,
    "970ffe3a78687f3a27a222e089ae3d5e928bbfa048b9aef9f51fcf4c0b5d578d",
)
V5D = (
    "search/d972_r07_a0_dual_anchored_rank99_durable_discovery_gha_driver_v5.g",
    9425,
    "bed9105b36fef5e59120d954029ec507b16f393ab2859a7599867a19156b1b5d",
)
RANK51 = (
    "search/certs/d972_r07_a0_actual_tau_free_rank51_checkpoint_v1.json",
    10934,
    "a83959e4c9fcfa79093c712e82164d47c31b78c9fc00b512f7adac9413c481f4",
)
TASK451_P = (
    "search/d972_r07_a0_dual_anchored_active_batch_v1.py",
    13834,
    "ca7fb15e06dd04881146c38d63d93015a9e630fbc334cf15098cbd8a32f22f9b",
)
SOURCE_HEAD = "dd6d90b64e2bfba73d7f131f4da876235746f314"
RUN_ID = "33553895281"
FIXTURE_ARTIFACT = "496"
V5_PASS = "R07_A0_DUAL_ANCHORED_RANK99_DURABLE_DISCOVERY_V5_CHECKER_PASS terminal=COMMON_CANDIDATE"


def need(value: Any, message: str) -> None:
    if not value:
        raise RuntimeError(message)


def artifact_id(value: Any) -> str:
    need(isinstance(value, str) and re.fullmatch(r"[1-9][0-9]*", value) is not None,
         "artifact_id:positive_decimal")
    return value


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canon(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True).encode("ascii")


def digest(value: Any) -> str:
    return sha(canon(value))


def sealed(value: dict[str, Any]) -> dict[str, Any]:
    out = dict(value)
    out.pop("self_digest", None)
    out["self_digest"] = digest(out)
    return out


def checkseal(value: dict[str, Any], label: str) -> None:
    body = dict(value)
    got = body.pop("self_digest", None)
    need(isinstance(got, str) and got == digest(body), label + ":seal")


def pin(spec: tuple[str, int, str]) -> dict[str, Any]:
    raw = (ROOT / spec[0]).read_bytes()
    need(len(raw) == spec[1] and sha(raw) == spec[2], "pin:" + spec[0])
    return {"path": spec[0], "bytes": len(raw), "sha256": sha(raw)}


def load(spec: tuple[str, int, str], name: str) -> Any:
    pin(spec)
    path = ROOT / spec[0]
    module_spec = importlib.util.spec_from_file_location(name, path)
    need(module_spec is not None and module_spec.loader is not None,
         "loader:" + spec[0])
    module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(module)
    return module


def read_file(name: str, limit: int = 512 * 1024 * 1024) -> tuple[bytes, dict[str, Any]]:
    need(isinstance(name, str) and name == name.strip(), "input:path")
    path = Path(name)
    resolved = path.resolve() if path.is_absolute() else (ROOT / path).resolve()
    resolved.relative_to(ROOT.resolve())
    need(not path.is_symlink(), "input:symlink")
    fd = os.open(resolved, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
    chunks: list[bytes] = []
    h = hashlib.sha256()
    try:
        info = os.fstat(fd)
        need(stat.S_ISREG(info.st_mode) and 0 < info.st_size <= limit,
             "input:physical")
        while True:
            chunk = os.read(fd, 1 << 20)
            if not chunk:
                break
            h.update(chunk)
            chunks.append(chunk)
        need(sum(len(chunk) for chunk in chunks) == info.st_size,
             "input:short_read")
    finally:
        os.close(fd)
    raw = b"".join(chunks)
    identity = {"path": str(resolved.relative_to(ROOT)).replace("\\", "/"),
                "bytes": len(raw), "sha256": h.hexdigest()}
    return raw, identity


def read_json(name: str) -> tuple[dict[str, Any], dict[str, Any]]:
    raw, identity = read_file(name)
    value = json.loads(raw.decode("ascii"))
    need(isinstance(value, dict) and raw == canon(value) + b"\n",
         "input:canonical")
    return value, identity


def reduce_word(word: Any) -> list[int]:
    out: list[int] = []
    need(isinstance(word, list), "word:list")
    for letter in word:
        need(type(letter) is int and letter and abs(letter) <= 2,
             "word:letter")
        if out and out[-1] == -letter:
            out.pop()
        else:
            out.append(letter)
    return out


def gword(value: Any) -> list[int]:
    if isinstance(value, (list, tuple)):
        return list(value)
    if isinstance(value, dict) and isinstance(value.get("word"), (list, tuple)):
        return list(value["word"])
    if hasattr(value, "word"):
        return list(value.word)
    raise RuntimeError("g760:word_abi")


def bootstrap() -> tuple[Any, Any, Any, Any, Any, list[int]]:
    owner = load(TASK451_P, "rank99_carrier_task451_owner")
    v3 = owner.v3
    v1 = load(v3.b.V1, "rank99_carrier_rank_ladder")
    v4 = v1.load(v1.V4, "rank99_carrier_v4")
    model_bundle = v4.load_v1()
    v12 = model_bundle.load(model_bundle.V12, "rank99_carrier_v12")
    physical = model_bundle.load(model_bundle.P435, "rank99_carrier_p435")
    _, base, _, _, runtime, _, model, _, quotient, target = physical.bootstrap(v12)
    _, g760, model2 = base["direct_physical_owner"](runtime)
    need(model2.g == model.g, "g760:model_owner")
    return v12, runtime, model, quotient, target, gword(g760)


def legacy_digest(encoded: Any) -> str:
    previous: bytes | None = None
    h = hashlib.sha256()
    need(isinstance(encoded, list), "row:list")
    for key_hex, coefficient in encoded:
        key = bytes.fromhex(key_hex)
        need(previous is None or previous < key, "row:sparse_order")
        previous = key
        need(coefficient in (1, 2), "row:coefficient")
        h.update(len(key).to_bytes(4, "big"))
        h.update(key)
        h.update(bytes((coefficient,)))
    return h.hexdigest()


def validate_upstream(result: dict[str, Any], checkpoint: dict[str, Any],
                      result_id: dict[str, Any], checkpoint_id: dict[str, Any],
                      checker_log: bytes) -> dict[str, Any]:
    v5c = load(V5C, "rank99_carrier_v5_checker")
    need(result.get("schema") == v5c.SCHEMA and
         result.get("status") == result.get("terminal") == "COMMON_CANDIDATE" and
         result.get("reason") is None, "v5:positive_envelope")
    need(result.get("discovery_mode") == "COMMON" and
         result.get("candidate_marker") == v5c.PRODUCER_MARKER + "_COMMON_CANDIDATE" and
         result.get("current_dual_profile") is None and
         result.get("soft_flush_committed") is False and
         result.get("open_batch_discarded") is False and
         result.get("ready_written") is True and
         result.get("selector_entered") is True, "v5:common_boundary")
    need(result.get("claims") == {"A0": True, "COMMON": False,
                                  "NONMEMBER": False, "fake": False,
                                  "Ihara": False}, "v5:claims")
    terminal_replay = result.get("terminal_replay")
    need(isinstance(terminal_replay, dict) and
         terminal_replay.get("status") == "COMMON_CANDIDATE" and
         terminal_replay.get("strict_replay") is True, "v5:terminal_replay")
    durable = result.get("durable_state")
    need(isinstance(durable, dict) and
         all(durable.get(key) == checkpoint_id.get(key)
             for key in ("path", "bytes", "sha256")),
         "v5:checkpoint_identity")
    need(checkpoint.get("schema") == v5c.CP_SCHEMA and
         checkpoint.get("open_batch") is False and
         checkpoint.get("state_sha256") == durable.get("state_sha256"),
         "v5:checkpoint_shape")
    need(result.get("binding") == v5c.BINDING and result.get("pins") == v5c.pins(),
         "v5:binding_pins")
    result_body = dict(result)
    result_seal = result_body.pop("self_digest_sha256", None)
    need(isinstance(result_seal, str) and result_seal == digest(result_body),
         "v5-result:seal")
    need(V5_PASS.encode("ascii") in checker_log.splitlines(),
         "v5:checker_marker")
    verdict = v5c.check(result)
    need(verdict.get("status") == "PASS" and
         verdict.get("terminal") == "COMMON_CANDIDATE",
         "v5:checker_reject")
    return terminal_replay


def build(args: argparse.Namespace) -> dict[str, Any]:
    for spec in (V5P, V5C, V5D, RANK51, TASK451_P):
        pin(spec)
    need(args.v5_result and args.v5_checkpoint and args.v5_checker_log and
         args.source_head is not None and args.run_id is not None and
         args.artifact_id is not None, "production:explicit_inputs")
    artifact = artifact_id(args.artifact_id)
    need(args.source_head == SOURCE_HEAD, "production:source_head")
    need(str(args.run_id) == RUN_ID, "production:run_id")
    result, result_id = read_json(args.v5_result)
    checkpoint, checkpoint_id = read_json(args.v5_checkpoint)
    checker_log, log_id = read_file(args.v5_checker_log, 16 * 1024 * 1024)
    terminal_replay = validate_upstream(result, checkpoint, result_id,
                                        checkpoint_id, checker_log)
    v12, runtime, model, quotient, target, g760 = bootstrap()
    need(len(g760) == 760 and reduce_word(g760) == g760,
         "g760:literal")
    literal = reduce_word(terminal_replay.get("literal_word"))
    need(literal == terminal_replay.get("literal_word") and
         terminal_replay.get("exact_exponent_pair") == [0, 0] and
         v12.v3.exp_pair(literal) == (0, 0), "literal:exponent")
    states = runtime.states_direct(literal)
    need(len(states) == 10 and all(state.a == state.q.identity for state in states),
         "literal:joint_kernel")
    direct, replay = model.direct_column([], literal)
    corrected = reduce_word(g760 + literal)
    need(replay.get("corrected_word") == corrected and
         replay.get("conjugate_word") == literal and
         replay.get("eleven_occurrence_replay") is True and
         replay.get("direct_all_seven_replay") is True,
         "direct:replay")
    need(v12.enc_row(target) == terminal_replay.get("target_row"),
         "direct:target")
    correction = quotient.transform(direct)
    need(v12.enc_row(correction) == terminal_replay.get("correction_sum"),
         "direct:correction")
    ancestry = terminal_replay.get("selected_action_ancestry")
    need(isinstance(ancestry, list), "direct:ancestry")
    encoded = v12.enc_row(direct)
    carrier = {
        "g760": g760,
        "literal_word": literal,
        "correction_word": literal,
        "corrected_word": corrected,
        "direct_replay": {
            "replay": replay,
            "eleven_occurrence_replay": True,
            "direct_all_seven_replay": True,
            "right_g760_multiplication": True,
            "hexagons": True,
            "pentagon_printed_order": True,
            "exact_exponent_pair": [0, 0],
            "joint_kernel": True,
            "physical_row": encoded,
            "physical_row_sha256": legacy_digest(encoded),
            "quotient_value_blobs": replay.get("quotient_value_blobs"),
        },
        "selected_action_ancestry": ancestry,
        "selected_action_ancestry_sha256": sha(canon(ancestry)),
    }
    pins = {"producer": dict(zip(("path", "bytes", "sha256"), V5P)),
            "checker": dict(zip(("path", "bytes", "sha256"), V5C)),
            "driver": dict(zip(("path", "bytes", "sha256"), V5D)),
            "frozen_rank51": dict(zip(("path", "bytes", "sha256"), RANK51))}
    inputs = {"v5_result": result_id, "v5_checkpoint": checkpoint_id,
              "v5_checker_log": log_id, "source_head": args.source_head,
              "run_id": str(args.run_id), "artifact_id": artifact}
    return sealed({
        "schema": SCHEMA,
        "status": "ACCEPTED",
        "terminal": MARKER + "_ACCEPTED",
        "carrier": carrier,
        "inputs": inputs,
        "pins": pins,
        "upstream": {"schema": "d972-r07-a0-dual-anchored-rank99-durable-discovery/v5",
                      "binding": "0e0123e99309a768910e150d5bf4725295a0dc35eab7e15eac66538a3a37d56b",
                      "implementation_commit": SOURCE_HEAD,
                      "production_run_id": RUN_ID,
                      "production_artifact_id": artifact},
        "claims": {"carrier": True, "A2": False, "lift": False,
                   "fake": False, "Ihara": False},
    })


def fixture() -> dict[str, Any]:
    toy = {
        "result_identity": {"path": "r", "bytes": 1, "sha256": "a" * 64},
        "checkpoint_identity": {"path": "c", "bytes": 1, "sha256": "b" * 64},
        "v5_schema": "d972-r07-a0-dual-anchored-rank99-durable-discovery/v5",
        "v5_marker": "R07_A0_DUAL_ANCHORED_RANK99_DURABLE_DISCOVERY_V5_COMMON_CANDIDATE",
        "producer_marker": "R07_A0_DUAL_ANCHORED_RANK99_DURABLE_DISCOVERY_V5",
        "checker_marker": V5_PASS,
        "source_head": SOURCE_HEAD, "run_id": RUN_ID, "artifact_id": FIXTURE_ARTIFACT,
        "terminal_replay": {"literal_word": [1, 2]},
        "literal_word": [1, 2], "exponent": [0, 0],
        "physical_replay": True, "physical_digest": "d" * 64,
        "ancestry": [], "right_product": True, "carrier_seal": True,
    }

    def gate(value: dict[str, Any]) -> None:
        need(value["result_identity"]["path"] == "r" and
             value["checkpoint_identity"]["path"] == "c", "toy:identity")
        need(value["v5_schema"].endswith("/v5") and
             value["v5_marker"].endswith("_COMMON_CANDIDATE") and
             value["producer_marker"].endswith("_V5") and
             value["checker_marker"] == V5_PASS, "toy:markers")
        need(value["source_head"] == SOURCE_HEAD and
             value["run_id"] == RUN_ID and
             artifact_id(value["artifact_id"]) == FIXTURE_ARTIFACT,
             "toy:provenance")
        need(value["terminal_replay"]["literal_word"] == value["literal_word"] and
             value["exponent"] == [0, 0] and value["physical_replay"] is True and
             len(value["physical_digest"]) == 64 and value["ancestry"] == [] and
             value["right_product"] is True and value["carrier_seal"] is True,
             "toy:replay")

    gate(toy)
    labels = ["result_identity", "checkpoint_identity", "v5_schema", "v5_marker",
              "producer_marker", "checker_marker", "source_head", "run_id",
              "artifact_id", "terminal_replay", "literal_word", "exponent",
              "physical_replay", "physical_digest", "ancestry", "right_product",
              "carrier_seal"]
    rejected: list[str] = []
    for label in labels:
        mutated = json.loads(json.dumps(toy))
        mutated[label] = None
        try:
            gate(mutated)
        except (AttributeError, KeyError, RuntimeError, TypeError):
            rejected.append(label)
    need(len(rejected) == len(labels), "toy:mutation_coverage")
    artifact_rejections: list[str] = []
    for label, mutated_id in (("artifact_id_nonnumeric", "job-id"),
                              ("artifact_id_zero", "0"),
                              ("artifact_id_drift", "497")):
        mutated = json.loads(json.dumps(toy))
        mutated["artifact_id"] = mutated_id
        try:
            gate(mutated)
        except (AttributeError, KeyError, RuntimeError, TypeError):
            artifact_rejections.append(label)
    need(len(artifact_rejections) == 3, "toy:artifact_id_mutation_coverage")
    return {"status": "PASS", "actual_common": False,
            "production_terminal_emitted": False,
            "mutation_rejections": rejected,
            "artifact_id_mutation_rejections": artifact_rejections}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixture", action="store_true")
    parser.add_argument("--v5-result", "--result", dest="v5_result")
    parser.add_argument("--v5-checkpoint", "--checkpoint", dest="v5_checkpoint")
    parser.add_argument("--v5-checker-log", "--checker-log", dest="v5_checker_log")
    parser.add_argument("--source-head")
    parser.add_argument("--run-id")
    parser.add_argument("--artifact-id")
    parser.add_argument("--output", required=True)
    args = parser.parse_args(argv)
    if args.fixture:
        value = {"schema": SCHEMA, "status": "FIXTURE", "fixture": fixture()}
    else:
        try:
            value = build(args)
        except Exception as exc:
            value = {"schema": SCHEMA, "status": "UNKNOWN_INPUT",
                     "terminal": MARKER + "_UNKNOWN_INPUT", "reason": str(exc),
                     "actual_common": False,
                     "claims": {"carrier": False, "A2": False, "lift": False,
                                "fake": False, "Ihara": False}}
    Path(args.output).write_bytes(canon(value) + b"\n")
    print(MARKER + " status=" + value["status"] +
          (" actual_common=false" if args.fixture else ""), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
