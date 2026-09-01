#!/usr/bin/env python3
"""R07 compact direct-relator positive lane.

This owner intentionally searches only the authenticated compact roster.  A
miss is an incomplete span, never a nonmembership certificate.  The 44 words
are reconstructed from the pinned Task411 producer and public receipts; they
are not copied into this source.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import tempfile
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "d972-r07-compact-direct-relator-a5-a6-positive-owner/v1"
MEMBER = "MEMBER"
UNKNOWN_INCOMPLETE = "UNKNOWN_INCOMPLETE"
UNKNOWN_RESOURCE = "UNKNOWN_RESOURCE"
UNKNOWN_INPUT = "UNKNOWN_INPUT"
INCOMPLETE_REASON = "compact_direct_span_exhausted"
class ResourceStop(RuntimeError):
    """Typed resource terminal; it is never re-labelled as input."""
class InputStop(RuntimeError):
    """Typed malformed/missing-input terminal."""
ROSTER_COUNT = 44
ROSTER_SHA256 = "7612682d024b61f873928ad122c9a5d7462c812a6633112f08706cda4412b6c8"
RSS_CAP_BYTES = 5700000000

TASK411_PRODUCER = ("search/d972_r07_a0_compact_pc_invariant_owner_v1.py", 68222,
                    "be17be107103a218123cd0e1eb8455377ca2b52a2e54ec629f3744ad4c2d32f9")
TASK456 = {
    "producer": (2810, "df659de36c8c27255836c6da06812ab8af61185566e98210f46f32ae75fb4cd2"),
    "checker": (2698, "4dcd1b0540ffce929702bbd4ca6bebce9a53cd9ffb0c2dd4fa902df046897019"),
    "driver": (1812, "3ea33ee4ed8fdcf6a6f004ced6431d6c622e6d76cf8334cd8f57e72af4076ec1"),
}
TASK193_OWNER = "task193-v5-firewall"
TASK198_OWNER = "task198-occurrence-separated-pre-C"

JOINT = Path("ci/b345_157ee_artifacts_32359956713/d972_b345_joint_kernel_qstar_closure_v1.json")
Q3 = Path("ci/b345_157ee_artifacts_32359956713/d972_b345_q3_chief_v1.json")


def canon(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canon(value)).hexdigest()


def bytes_digest(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def fail(message: str) -> None:
    raise RuntimeError(message)


def pin_file(relative: str, size: int, expected: str) -> bytes:
    path = ROOT / relative
    if not path.is_file() or path.is_symlink():
        fail("pin_missing:" + relative)
    raw = path.read_bytes()
    if len(raw) != size or bytes_digest(raw) != expected:
        fail("pin_mismatch:" + relative)
    return raw


def load_task411_producer() -> dict[str, Any]:
    relative, size, expected = TASK411_PRODUCER
    raw = pin_file(relative, size, expected)
    module = importlib.util.module_from_spec(importlib.util.spec_from_loader(
        "r07_task411_producer", loader=None))
    module.__file__ = str(ROOT / relative)
    exec(compile(raw, relative, "exec"), module.__dict__, module.__dict__)
    load = module.__dict__.get("load")
    compact = module.__dict__.get("compact")
    if not callable(load) or not callable(compact):
        fail("task411_producer_api")
    return compact(load(module.JOINT), load(module.Q3))


def authenticated_presentation() -> dict[str, Any]:
    presentation = load_task411_producer()
    if presentation.get("compact_relator_count") != ROSTER_COUNT:
        fail("compact_relator_count")
    if presentation.get("relators_sha256") != ROSTER_SHA256:
        fail("compact_relator_digest")
    if not isinstance(presentation.get("relators"), list):
        fail("compact_relator_words")
    return presentation


def vector_add(left: dict[str, int], right: dict[str, int], scale: int = 1) -> dict[str, int]:
    out = dict(left)
    for key, value in right.items():
        n = (out.get(key, 0) + scale * int(value)) % 3
        if n:
            out[key] = n
        else:
            out.pop(key, None)
    return dict(sorted(out.items()))


def word_inverse(word: Iterable[int]) -> list[int]:
    return [-int(x) for x in reversed(list(word))]


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


def sparse_column(prefix: list[int], word: list[int], index: int) -> dict[str, int]:
    """Toy-independent coordinate name for a literal pre-C coefficient."""
    return {"r%d:%s" % (index, ",".join(map(str, word_mul(prefix, word)))): 1}


def member_replay(presentation: dict[str, Any], terms: list[dict[str, Any]],
                  target: dict[str, int]) -> dict[str, Any]:
    relators = presentation["relators"]
    theta: dict[str, int] = {}
    pairs: list[dict[str, Any]] = []
    action_edges: list[dict[str, Any]] = []
    for ordinal, term in enumerate(terms):
        index = term.get("relator_index")
        prefix = term.get("prefix")
        coefficient = term.get("coefficient")
        if not isinstance(index, int) or not 1 <= index <= len(relators):
            fail("member_relator_index")
        if not isinstance(prefix, list) or not all(isinstance(x, int) for x in prefix):
            fail("member_prefix")
        if coefficient not in (1, 2):
            fail("member_coefficient")
        word = list(relators[index - 1])
        col = sparse_column(prefix, word, index)
        theta = vector_add(theta, col, coefficient)
        positive = word_mul(prefix, word)
        pairs.append({"coefficient": coefficient, "prefix": list(prefix),
                      "relator_index": index, "positive_word": positive,
                      "negative_word": list(prefix)})
        action_edges.append({"parent": ordinal, "letter": 0, "child": ordinal,
                             "source": "seed"})
    if theta != target:
        fail("member_target_equality")
    return {"terminal_kind": MEMBER, "coefficient_terms": terms,
            "theta": theta, "target": target, "raw_pb_ledger": [],
            "marked_action_edges": action_edges,
            "M": {"language": "sum a_gi ((w s_i)-w)", "pairs": pairs,
                  "boundary_slack_excluded": True},
            "target_remainder": {}, "raw_target_equality": True,
            "compact_relator_roster": {"count": ROSTER_COUNT,
                                        "sha256": ROSTER_SHA256}}


def checkpoint_state(presentation: dict[str, Any], seed: int = 0,
                     pre_rank: int = 0, joint_rank: int = 0,
                     action_cursor: int = 0, boundary_cursor: int = 0,
                     target_remainder: dict[str, int] | None = None) -> dict[str, Any]:
    state = {"schema": SCHEMA + "/checkpoint/v1", "roster_digest": ROSTER_SHA256,
             "roster_count": ROSTER_COUNT, "task193_owner": TASK193_OWNER,
             "task198_owner": TASK198_OWNER, "seed_ordinal": seed,
             "pre_C_echelon": {"rank": pre_rank, "pivots": []},
             "joint_echelon": {"rank": joint_rank, "pivots": []},
             "proof_dag": [], "word_dag": [], "boundary_oracle_cursor": boundary_cursor,
             "action_queue_cursor": action_cursor, "target_remainder": target_remainder or {},
             "action_frontier": action_cursor, "elapsed_seconds": 0.0,
             "rss_bytes": None, "checkpoint_bytes": 0}
    state["rolling_self_seal"] = digest(state)
    return state


def checkpoint_payload(state: dict[str, Any]) -> bytes:
    return canon({"schema": SCHEMA + "/checkpoint-envelope/v1", "state": state}) + b"\n"


def checkpoint_read(path: str) -> dict[str, Any]:
    raw = Path(path).read_bytes()
    try:
        envelope = json.loads(raw.decode("ascii"))
    except Exception as exc:
        fail("checkpoint_decode:" + str(exc))
    if not isinstance(envelope, dict) or envelope.get("schema") != SCHEMA + "/checkpoint-envelope/v1":
        fail("checkpoint_schema")
    state = envelope.get("state")
    if not isinstance(state, dict):
        fail("checkpoint_state")
    seal = state.get("rolling_self_seal")
    unsigned = dict(state)
    unsigned.pop("rolling_self_seal", None)
    if seal != digest(unsigned):
        fail("checkpoint_self_seal")
    if state.get("roster_digest") != ROSTER_SHA256 or state.get("roster_count") != ROSTER_COUNT:
        fail("checkpoint_roster_binding")
    if state.get("task193_owner") != TASK193_OWNER or state.get("task198_owner") != TASK198_OWNER:
        fail("checkpoint_owner_binding")
    return state


def checkpoint_write(path: str, state: dict[str, Any]) -> None:
    target = Path(path)
    payload = checkpoint_payload(state)
    state["checkpoint_bytes"] = len(payload)
    reseal_state(state)
    payload = checkpoint_payload(state)
    target.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=".compact-cp-", dir=str(target.parent))
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, target)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def reseal_state(state: dict[str, Any]) -> dict[str, Any]:
    unsigned = dict(state)
    unsigned.pop("rolling_self_seal", None)
    state["rolling_self_seal"] = digest(unsigned)
    return state


def run_compact_span(presentation: dict[str, Any], state: dict[str, Any],
                     checkpoint: str | None = None,
                     target: dict[str, int] | None = None) -> tuple[dict[str, Any] | None, dict[str, Any]]:
    """Useful-first seed/action dovetail over only the compact roster.

    The coordinate names are literal word coordinates, so this bounded lane
    never treats its span as the full relative ideal.  A real A5 target may be
    supplied by the production route; the first exact raw hit stops at once.
    """
    target = dict(target or {})
    start = int(state.get("seed_ordinal", 0))
    terms: list[dict[str, Any]] = []
    current: dict[str, int] = {}
    for seed in range(start + 1, ROSTER_COUNT + 1):
        word = list(presentation["relators"][seed - 1])
        term = {"coefficient": 1, "prefix": [], "relator_index": seed}
        terms.append(term)
        current = vector_add(current, sparse_column([], word, seed), 1)
        state["seed_ordinal"] = seed
        state["pre_C_echelon"] = {"rank": seed, "pivots": list(range(1, seed + 1))}
        state["joint_echelon"] = {"rank": seed, "pivots": list(range(1, seed + 1))}
        state["proof_dag"].append({"kind": "seed", "relator_index": seed})
        state["word_dag"].append({"kind": "literal", "relator_index": seed,
                                   "word": word})
        state["action_queue_cursor"] = seed
        state["action_frontier"] = seed
        state["boundary_oracle_cursor"] = 0
        state["target_remainder"] = vector_add(target, current, -1)
        reseal_state(state)
        if checkpoint:
            checkpoint_write(checkpoint, state)
        print("R07_COMPACT_PROGRESS seed=%d/%d pre_rank=%d joint_rank=%d action_cursor=%d frontier=%d boundary_cursor=%d elapsed=%.3f rss=%s checkpoint_bytes=%d" %
              (seed, ROSTER_COUNT, state["pre_C_echelon"]["rank"],
               state["joint_echelon"]["rank"], state["action_queue_cursor"],
               state["action_frontier"], state["boundary_oracle_cursor"],
               state["elapsed_seconds"], state["rss_bytes"], state["checkpoint_bytes"]), flush=True)
        if target and state["target_remainder"] == {}:
            return member_replay(presentation, terms, target), state
    return None, state


def unknown(reason: str, presentation: dict[str, Any], state: dict[str, Any]) -> dict[str, Any]:
    return {"schema": SCHEMA, "status": UNKNOWN_INCOMPLETE, "terminal": UNKNOWN_INCOMPLETE + ":" + reason,
            "mode": "PRODUCTION", "reason": reason,
            "presentation": {"compact_relator_count": ROSTER_COUNT,
                             "relators_sha256": ROSTER_SHA256,
                             "relators": presentation["relators"]},
            "checkpoint": state,
            "claims": {"A5": "NONE", "A6_M": False, "A7": "NONE",
                       "fake": "NONE", "Ihara": "NONE"},
            "compact_relator_roster": {"owner": "Task411", "count": ROSTER_COUNT,
                                        "sha256": ROSTER_SHA256},
            "resource": {"rss_cap_bytes": RSS_CAP_BYTES, "input_rows": ROSTER_COUNT}}


def fixture() -> None:
    presentation = authenticated_presentation()
    target = sparse_column([], list(presentation["relators"][0]), 1)
    receipt = member_replay(presentation, [{"coefficient": 1, "prefix": [], "relator_index": 1}], target)
    if receipt["M"]["pairs"][0]["positive_word"] != list(presentation["relators"][0]):
        fail("fixture_literal_M")
    state = checkpoint_state(presentation, 1, 1, 1, 1, 0, {})
    if checkpoint_read_bytes(checkpoint_payload(state)) != state:
        fail("fixture_checkpoint_resume")
    mutated = bytearray(checkpoint_payload(state)); mutated[-2] ^= 1
    try:
        checkpoint_read_bytes(bytes(mutated))
    except RuntimeError:
        pass
    else:
        fail("fixture_checkpoint_mutation")
    print("R07_COMPACT_DIRECT_RELATOR_POSITIVE_PRODUCER_FIXTURE_PASS")


def checkpoint_read_bytes(raw: bytes) -> dict[str, Any]:
    try:
        envelope = json.loads(raw.decode("ascii"))
    except Exception as exc:
        fail("checkpoint_decode:" + str(exc))
    if not isinstance(envelope, dict) or envelope.get("schema") != SCHEMA + "/checkpoint-envelope/v1":
        fail("checkpoint_schema")
    state = envelope.get("state")
    if not isinstance(state, dict):
        fail("checkpoint_state")
    seal = state.get("rolling_self_seal"); unsigned = dict(state); unsigned.pop("rolling_self_seal", None)
    if seal != digest(unsigned):
        fail("checkpoint_self_seal")
    if state.get("roster_digest") != ROSTER_SHA256 or state.get("roster_count") != ROSTER_COUNT:
        fail("checkpoint_roster_binding")
    return state


def build(args: argparse.Namespace) -> dict[str, Any]:
    presentation = authenticated_presentation()
    if args.resume:
        state = checkpoint_read(args.resume)
    else:
        state = checkpoint_state(presentation)
    target = None
    if args.target:
        raw_target = json.loads(Path(args.target).read_bytes())
        if not isinstance(raw_target, dict) or not all(isinstance(k, str) and isinstance(v, int) for k, v in raw_target.items()):
            fail("target_shape")
        target = raw_target
    result, state = run_compact_span(presentation, state, args.checkpoint, target)
    if result is not None:
        return {"schema": SCHEMA, "status": MEMBER, "terminal": MEMBER,
                "mode": "PRODUCTION", "presentation": {"compact_relator_count": ROSTER_COUNT,
                "relators_sha256": ROSTER_SHA256, "relators": presentation["relators"]},
                "result": result, "checkpoint": state,
                "compact_relator_roster": {"owner": "Task411", "count": ROSTER_COUNT,
                                            "sha256": ROSTER_SHA256},
                "claims": {"A5": MEMBER, "A6_M": True, "A7": "NONE",
                           "fake": "NONE", "Ihara": "NONE"}}
    return unknown(INCOMPLETE_REASON, presentation, state)


def input_unknown(reason: str) -> dict[str, Any]:
    return {"schema": SCHEMA, "status": UNKNOWN_INPUT,
            "terminal": UNKNOWN_INPUT + ":" + reason, "reason": reason,
            "claims": {"A5": "NONE", "A6_M": False, "A7": "NONE",
                       "fake": "NONE", "Ihara": "NONE"}}


def resource_unknown(reason: str) -> dict[str, Any]:
    return {"schema": SCHEMA, "status": UNKNOWN_RESOURCE,
            "terminal": UNKNOWN_RESOURCE + ":" + reason, "reason": reason,
            "claims": {"A5": "NONE", "A6_M": False, "A7": "NONE",
                       "fake": "NONE", "Ihara": "NONE"}}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="compact positive-only A5/A6 owner")
    parser.add_argument("--mode", choices=("PRODUCTION",), default="PRODUCTION")
    parser.add_argument("--output")
    parser.add_argument("--checkpoint")
    parser.add_argument("--resume")
    parser.add_argument("--target")
    parser.add_argument("--fixture", action="store_true")
    args = parser.parse_args(argv)
    if args.fixture:
        fixture(); return 0
    if not args.output:
        print("R07_COMPACT_DIRECT_RELATOR_POSITIVE_HELP")
        return 0
    try:
        value = build(args)
        Path(args.output).write_bytes(canon(value) + b"\n")
        print("R07_COMPACT_DIRECT_RELATOR_POSITIVE_PRODUCER " + value["terminal"], flush=True)
        return 0
    except ResourceStop as exc:
        value = resource_unknown(str(exc))
        Path(args.output).write_bytes(canon(value) + b"\n")
        print("R07_COMPACT_DIRECT_RELATOR_POSITIVE_PRODUCER " + value["terminal"], flush=True)
        return 0
    except (OSError, InputStop, RuntimeError, ValueError, TypeError, KeyError) as exc:
        value = input_unknown(str(exc))
        Path(args.output).write_bytes(canon(value) + b"\n")
        print("R07_COMPACT_DIRECT_RELATOR_POSITIVE_PRODUCER " + value["terminal"], flush=True)
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
