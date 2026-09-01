#!/usr/bin/env python3
"""Independent positive-only replay for the compact direct-relator lane."""
from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "d972-r07-compact-direct-relator-a5-a6-positive-owner/v1"
MEMBER = "MEMBER"
UNKNOWN_INCOMPLETE = "UNKNOWN_INCOMPLETE"
ROSTER_COUNT = 44
ROSTER_SHA256 = "7612682d024b61f873928ad122c9a5d7462c812a6633112f08706cda4412b6c8"
TASK411_CHECKER = ("crosscheck/check_d972_r07_a0_compact_pc_invariant_owner_v1.py", 44831,
                   "7c1aea086ce264ad6f51983554a3a371ac481d07a2ec5f5d9a96ee270af6dfcf")
TASK456 = {
    "producer": (2810, "df659de36c8c27255836c6da06812ab8af61185566e98210f46f32ae75fb4cd2"),
    "checker": (2698, "4dcd1b0540ffce929702bbd4ca6bebce9a53cd9ffb0c2dd4fa902df046897019"),
    "driver": (1812, "3ea33ee4ed8fdcf6a6f004ced6431d6c622e6d76cf8334cd8f57e72af4076ec1"),
}
TASK193_OWNER = "task193-v5-firewall"
TASK198_OWNER = "task198-occurrence-separated-pre-C"


def canon(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canon(value)).hexdigest()


def fail(message: str) -> None:
    raise RuntimeError(message)


def pin_file(relative: str, size: int, expected: str) -> bytes:
    path = ROOT / relative
    if not path.is_file() or path.is_symlink():
        fail("pin_missing:" + relative)
    raw = path.read_bytes()
    if len(raw) != size or hashlib.sha256(raw).hexdigest() != expected:
        fail("pin_mismatch:" + relative)
    return raw


def task411_presentation() -> dict[str, Any]:
    relative, size, expected = TASK411_CHECKER
    raw = pin_file(relative, size, expected)
    module = importlib.util.module_from_spec(importlib.util.spec_from_loader(
        "r07_task411_checker", loader=None))
    module.__file__ = str(ROOT / relative)
    exec(compile(raw, relative, "exec"), module.__dict__, module.__dict__)
    load_data = module.__dict__.get("load_data")
    load_source = module.__dict__.get("load_source")
    rebuild = module.__dict__.get("rebuild_presentation")
    if not callable(load_data) or not callable(load_source) or not callable(rebuild):
        fail("task411_checker_api")
    joint, q3 = load_data(module.JOINT), load_data(module.Q3)
    raw_owner = load_source("raw")
    presentation = rebuild(joint, q3, raw_owner)
    if presentation.get("compact_relator_count") != ROSTER_COUNT:
        fail("compact_relator_count")
    if presentation.get("relators_sha256") != ROSTER_SHA256:
        fail("compact_relator_digest")
    return presentation


def word_mul(*parts: Iterable[int]) -> list[int]:
    out: list[int] = []
    for part in parts:
        for letter in part:
            letter = int(letter)
            if out and out[-1] == -letter:
                out.pop()
            else:
                out.append(letter)
    return out


def column(prefix: list[int], word: list[int], index: int) -> dict[str, int]:
    return {"r%d:%s" % (index, ",".join(map(str, word_mul(prefix, word)))): 1}


def add(left: dict[str, int], right: dict[str, int], scale: int = 1) -> dict[str, int]:
    out = dict(left)
    for key, value in right.items():
        n = (out.get(key, 0) + scale * int(value)) % 3
        if n:
            out[key] = n
        else:
            out.pop(key, None)
    return dict(sorted(out.items()))


def check_member(output: dict[str, Any], presentation: dict[str, Any]) -> None:
    result = output.get("result")
    if not isinstance(result, dict) or result.get("terminal_kind") != MEMBER:
        fail("member_result")
    binding = output.get("compact_relator_roster")
    if binding != {"owner": "Task411", "count": ROSTER_COUNT, "sha256": ROSTER_SHA256}:
        fail("roster_owner_binding")
    terms = result.get("coefficient_terms")
    target = result.get("target")
    if not isinstance(terms, list) or not isinstance(target, dict):
        fail("member_terms_target")
    theta: dict[str, int] = {}
    expected_pairs: list[dict[str, Any]] = []
    for ordinal, term in enumerate(terms):
        if not isinstance(term, dict):
            fail("term_shape")
        index, prefix, coefficient = term.get("relator_index"), term.get("prefix"), term.get("coefficient")
        if not isinstance(index, int) or not 1 <= index <= ROSTER_COUNT:
            fail("term_index")
        if not isinstance(prefix, list) or not all(isinstance(x, int) for x in prefix):
            fail("term_prefix")
        if coefficient not in (1, 2):
            fail("term_coefficient")
        word = list(presentation["relators"][index - 1])
        theta = add(theta, column(prefix, word, index), coefficient)
        expected_pairs.append({"coefficient": coefficient, "prefix": list(prefix),
                               "relator_index": index,
                               "positive_word": word_mul(prefix, word),
                               "negative_word": list(prefix)})
    if theta != target or result.get("theta") != theta or result.get("target_remainder") != {}:
        fail("target_equality")
    if result.get("raw_target_equality") is not True:
        fail("raw_target_equality")
    edges = result.get("marked_action_edges")
    if not isinstance(edges, list) or len(edges) != len(terms):
        fail("action_edges")
    for ordinal, edge in enumerate(edges):
        if edge != {"parent": ordinal, "letter": 0, "child": ordinal, "source": "seed"}:
            fail("action_edge_replay")
    if result.get("raw_pb_ledger") != []:
        fail("pb_ledger_replay")
    M = result.get("M")
    if not isinstance(M, dict) or M.get("language") != "sum a_gi ((w s_i)-w)" or M.get("boundary_slack_excluded") is not True:
        fail("M_shape")
    if M.get("pairs") != expected_pairs:
        fail("literal_M_replay")


def check_checkpoint(state: Any) -> None:
    if not isinstance(state, dict):
        fail("checkpoint_state")
    if state.get("schema") != SCHEMA + "/checkpoint/v1":
        fail("checkpoint_schema")
    unsigned = dict(state)
    seal = unsigned.pop("rolling_self_seal", None)
    if seal != digest(unsigned):
        fail("checkpoint_self_seal")
    required = {"roster_digest": ROSTER_SHA256, "roster_count": ROSTER_COUNT,
                "task193_owner": TASK193_OWNER, "task198_owner": TASK198_OWNER}
    if any(state.get(key) != value for key, value in required.items()):
        fail("checkpoint_binding")
    for key in ("pre_C_echelon", "joint_echelon", "proof_dag", "word_dag",
                "boundary_oracle_cursor", "action_queue_cursor", "target_remainder"):
        if key not in state:
            fail("checkpoint_field:" + key)


def fixture() -> None:
    presentation = task411_presentation()
    target = column([], list(presentation["relators"][0]), 1)
    fake = {"schema": SCHEMA, "status": MEMBER, "terminal": MEMBER,
            "compact_relator_roster": {"owner": "Task411", "count": ROSTER_COUNT,
                                        "sha256": ROSTER_SHA256},
            "result": {"terminal_kind": MEMBER, "coefficient_terms":
                        [{"coefficient": 1, "prefix": [], "relator_index": 1}],
                        "theta": target, "target": target, "target_remainder": {},
                        "raw_target_equality": True, "raw_pb_ledger": [],
                        "marked_action_edges": [{"parent": 0, "letter": 0, "child": 0, "source": "seed"}],
                        "M": {"language": "sum a_gi ((w s_i)-w)",
                               "boundary_slack_excluded": True,
                               "pairs": [{"coefficient": 1, "prefix": [], "relator_index": 1,
                                           "positive_word": list(presentation["relators"][0]),
                                           "negative_word": []}]}}}
    check_member(fake, presentation)
    unknown = {"status": "UNKNOWN_INCOMPLETE", "terminal": "UNKNOWN_INCOMPLETE:" + "compact_direct_span_exhausted"}
    if unknown["status"] != unknown["terminal"].split(":", 1)[0]:
        fail("unknown_mapping")
    def reject_terminal(value: dict[str, Any]) -> None:
        if value.get("status") != MEMBER or value.get("terminal") != MEMBER:
            raise RuntimeError("no_unknown_acceptance")
    for old in ({"status": "NONMEMBER", "terminal": "NONMEMBER"}, unknown):
        try:
            reject_terminal(old)
        except RuntimeError:
            pass
        else:
            fail("old_nonmember_fixture")
    # Every mutable owner is checked by the same replay path used for a
    # receipt: literal seed word, marked action edge, raw PB ledger, and M.
    mutations = []
    mutated = copy.deepcopy(fake); mutated["result"]["coefficient_terms"][0]["relator_index"] = 2; mutations.append(mutated)
    mutated = copy.deepcopy(fake); mutated["result"]["marked_action_edges"][0]["letter"] = 1; mutations.append(mutated)
    mutated = copy.deepcopy(fake); mutated["result"]["raw_pb_ledger"] = [{"block": 1}]; mutations.append(mutated)
    mutated = copy.deepcopy(fake); mutated["result"]["M"]["pairs"][0]["positive_word"] = []; mutations.append(mutated)
    for candidate in mutations:
        try:
            check_member(candidate, presentation)
        except RuntimeError:
            pass
        else:
            fail("mutation_accepted")
    state = {"schema": SCHEMA + "/checkpoint/v1", "roster_digest": ROSTER_SHA256,
             "roster_count": ROSTER_COUNT, "task193_owner": TASK193_OWNER,
             "task198_owner": TASK198_OWNER, "pre_C_echelon": {"rank": 1, "pivots": []},
             "joint_echelon": {"rank": 1, "pivots": []}, "proof_dag": [], "word_dag": [],
             "boundary_oracle_cursor": 0, "action_queue_cursor": 1,
             "target_remainder": {}, "rolling_self_seal": ""}
    unsigned = dict(state); unsigned.pop("rolling_self_seal"); state["rolling_self_seal"] = digest(unsigned)
    check_checkpoint(state)
    mutated = dict(state); mutated["action_queue_cursor"] = 2
    try:
        check_checkpoint(mutated)
    except RuntimeError:
        pass
    else:
        fail("checkpoint_mutation")
    print("R07_COMPACT_DIRECT_RELATOR_POSITIVE_CHECKER_FIXTURE_PASS")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="independent compact positive replay")
    parser.add_argument("--producer")
    parser.add_argument("--fixture", action="store_true")
    args = parser.parse_args(argv)
    try:
        if args.fixture:
            fixture(); return 0
        if not args.producer:
            fail("producer_required")
        output = json.loads(Path(args.producer).read_bytes())
        if not isinstance(output, dict) or output.get("schema") != SCHEMA:
            fail("schema")
        if output.get("status") != MEMBER or output.get("terminal") != MEMBER:
            fail("no_unknown_acceptance")
        presentation = task411_presentation()
        supplied = output.get("presentation")
        if not isinstance(supplied, dict) or supplied.get("compact_relator_count") != ROSTER_COUNT or supplied.get("relators_sha256") != ROSTER_SHA256 or supplied.get("relators") != presentation["relators"]:
            fail("presentation_replay")
        check_member(output, presentation)
        check_checkpoint(output.get("checkpoint"))
        claims = output.get("claims", {})
        if claims.get("A5") != MEMBER or claims.get("A6_M") is not True or claims.get("A7") != "NONE" or claims.get("fake") != "NONE" or claims.get("Ihara") != "NONE":
            fail("claims")
        print("R07_COMPACT_DIRECT_RELATOR_POSITIVE_CHECKER_PASS")
        return 0
    except (OSError, RuntimeError, ValueError, TypeError, KeyError, json.JSONDecodeError) as exc:
        print("R07_COMPACT_DIRECT_RELATOR_POSITIVE_CHECKER_FAIL:" + str(exc))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
