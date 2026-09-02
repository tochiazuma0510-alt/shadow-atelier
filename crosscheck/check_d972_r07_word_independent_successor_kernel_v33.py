#!/usr/bin/env python3
"""A4 v33: independent physical-shard acceptance on the live checker route."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any

OWNER = Path(__file__).with_name("check_d972_r07_word_independent_successor_kernel_v32.py")
OWNER_BYTES = 10036
OWNER_SHA256 = "8582b707cc63a965d0eef55a9df5d514b0601afee68118dddba236765034ffa0"
OWNER_GENERATED_BYTES = 293042
OWNER_GENERATED_SHA256 = "80ac3ff80b106691f667840891e99904b1a9f2bc58dfe0b700b893904ad38440"
RESULT_GENERATED_BYTES = 312046
RESULT_GENERATED_SHA256 = "cb1d2b390beb3bdbd71d2175983310971d0669f6a6d7b77e1e64f29ceae61f57"
_ANCHOR = b"def validate_terminal_checkpoint"

_PHYSICAL_HELPER = r'''
def _a4_v33_read_json(identity: dict[str, Any], meter: Meter, label: str) -> tuple[Path, dict[str, Any], bytes]:
    require(isinstance(identity, dict) and set(identity) == {"path", "bytes", "sha256"}, "physical:identity")
    path = checkpoint_input(Path(str(identity["path"])), label)
    raw = read_once(path, (path.as_posix().replace(ROOT.as_posix() + "/", ""), int(identity["bytes"]), str(identity["sha256"])),
                    meter, label, terminal_transport=True)
    require(len(raw) == int(identity["bytes"]) and sha(raw) == identity["sha256"], "physical:identity_drift")
    try:
        value = json.loads(raw.decode("ascii"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise Reject("physical:json") from exc
    return path, value, raw


def _a4_v33_base_basis(authority: Authority, base: dict[str, Any], meter: Meter) -> tuple[Boundary, Basis, dict[str, Any]]:
    arithmetic = CheckerArithmetic(authority, meter)
    boundary = Boundary(arithmetic, meter)
    basis = Basis(boundary, meter)
    items = {str(item.get("label")): item for item in base.get("K_roster", []) if isinstance(item, dict)}
    for event in base.get("insertion_events", []):
        require(isinstance(event, dict) and isinstance(event.get("label"), str), "physical:base_event")
        label = str(event["label"])
        if event.get("kind") == "B":
            raw = str(event.get("raw_identity"))
            basis.add_boundary(boundary.psi({raw: 1}), raw)
        elif event.get("kind") == "K":
            item = items.get(label)
            require(isinstance(item, dict), "physical:base_K_owner")
            detail = basis.combined.insert(dict(item["row"]), label)
            require(detail is not None and detail.get("pivot") == item.get("pivot"), "physical:base_K_row")
            basis.k_rows[label] = dict(detail["row"])
            basis.b_formals[label] = ({}, {label: 1})
            basis.combined_ledgers[label] = {}
            basis.active_registry.update(detail["row"])
            basis.insertion_events.append(dict(event))
        else:
            raise Reject("physical:base_event_kind")
    expected = base.get("echelon_rebuild", {})
    require(len(basis.combined.pivots) == len(expected.get("pivots", [])), "physical:base_rank")
    return boundary, basis, dict(base.get("semantic_counters", {}))


def _a4_v33_ordinary_state(reference: dict[str, Any], authority: Authority | None,
                            meter: Meter) -> dict[str, Any]:
    """Validate and materialize only the authenticated completed-row base.

    The ordinary reference is a v429 delta HEAD in the live producer.  The
    older checker validator deliberately returns its immutable row-24 base;
    the physical continuation must independently apply the authenticated
    row-25/26 deltas so its first physical query is bound to the actual row-26
    state, rather than to a synthetic pre-frontier snapshot.
    """
    require(isinstance(reference, dict), "physical:ordinary_missing")
    if reference.get("kind") != "delta_chain":
        state = validate_terminal_checkpoint(reference, authority, meter)
        require(isinstance(state, dict) and int(state.get("next_row", 0)) == 27,
                "physical:ordinary_cursor")
        return state
    base_state = validate_delta_terminal_chain(reference, meter)
    head_path = checkpoint_input(Path(str(reference["path"])), "checker.physical_ordinary_head")
    head_raw = read_once(head_path, (head_path.as_posix().replace(ROOT.as_posix() + "/", ""),
                                     int(reference["bytes"]), str(reference["sha256"])), meter,
                         "checker.physical_ordinary_head", terminal_transport=True)
    head = json.loads(head_raw.decode("ascii")); claimed = head.pop("self_digest_sha256", None)
    require(claimed == digest(head) and head.get("schema") == PRODUCER_DELTA_HEAD_SCHEMA and
            head.get("owner") == "producer" and reference.get("checkpoint_self_digest_sha256") == claimed,
            "physical:ordinary_head_seal")
    base_info = head.get("base"); require(isinstance(base_info, dict), "physical:ordinary_base_info")
    state = json.loads(canon(base_state).decode("ascii")); expected = int(state.get("next_row", 0))
    previous = None; chain = "0" * 64; count = int(head.get("segment_count", 0))
    require(int(reference.get("last_sequence", -1)) == count, "physical:ordinary_sequence")
    for sequence in range(1, count + 1):
        segment_path = head_path.with_name(head_path.name + ".delta.%08d.json" % sequence)
        require(segment_path.exists() and not segment_path.is_symlink(), "physical:ordinary_segment")
        segment_raw = read_once(segment_path,
                                (segment_path.as_posix().replace(ROOT.as_posix() + "/", ""),
                                 segment_path.stat().st_size, sha(segment_path.read_bytes())), meter,
                                "checker.physical_ordinary_segment", terminal_transport=True)
        segment = json.loads(segment_raw.decode("ascii")); sealed = segment.pop("self_digest_sha256", None)
        require(sealed == digest(segment) and segment.get("schema") == PRODUCER_DELTA_SCHEMA and
                segment.get("owner") == "producer" and segment.get("sequence") == sequence and
                segment.get("base") == base_info and segment.get("previous") == previous,
                "physical:ordinary_segment_seal")
        chain = _producer_delta_chain(segment, chain)
        require(segment.get("chain") == chain, "physical:ordinary_segment_chain")
        expected = _checker_delta_apply(state, segment, expected)
        previous = sha(segment_raw)
    require(head.get("last_sequence") == count and head.get("last_segment_sha256") == previous and
            head.get("chain") == chain and head.get("next_row") == expected == int(reference["next_row"]) == 27 and
            reference.get("last_segment_sha256") == previous and reference.get("chain") == chain,
            "physical:ordinary_terminal")
    return state


def _a4_v33_expected_entry(basis: Basis, candidate: dict[str, Any], column: dict[str, int],
                           raw_identity: str, added: dict[str, Any], record: dict[str, Any],
                           event_index: int, epoch_before: str, epoch_after: str) -> dict[str, Any]:
    event = basis.insertion_events[-1]
    label = str(added["label"])
    bd = {"pivot": event["boundary_pivot"], "scale": event["boundary_scale"],
          "row": dict(event["boundary_row"]), "label": label,
          "reduction": dict(event["boundary_reduction"])}
    detail = dict(event["combined_detail"])
    cd = {"pivot": detail["pivot"], "scale": detail["scale"], "row": dict(detail["row"]),
          "label": label, "reduction": dict(detail["reduction"])}
    raw = {"raw_key": raw_identity, "row": dict(column), "candidate": dict(candidate)}
    query_event = {"index": event_index, "query_id": record["query_id"],
                   "schema": record["schema"], "digest": digest(record)}
    insertion = {"kind": "B", "label": label, "column": dict(column), "raw_identity": raw_identity,
                 "boundary_row": dict(bd["row"]), "boundary_pivot": bd["pivot"],
                 "boundary_scale": bd["scale"], "boundary_reduction": dict(bd["reduction"]),
                 "combined_row": dict(cd["row"]), "combined_detail": {"pivot": cd["pivot"],
                 "scale": cd["scale"], "row": dict(cd["row"]), "reduction": dict(cd["reduction"]),
                 "relation": dict(detail.get("relation", {}))}}
    formals = {"boundary_reduction": dict(bd["reduction"]), "combined_reduction": dict(cd["reduction"]),
               "boundary_ledger": dict(basis.boundary_ledgers[label]),
               "combined_ledger": dict(basis.combined_ledgers[label]),
               "b_coefficients": dict(basis.b_coefficients.get(label, {})),
               "b_formals": [dict(basis.b_formals[label][0]), dict(basis.b_formals[label][1])]}
    return {"kind": "B", "raw_identity": raw, "raw_digest": digest(raw["row"]),
            "boundary": {**bd, "row_digest": digest(bd["row"]), "label_digest": digest(label)},
            "combined": {**cd, "row_digest": digest(cd["row"]), "label_digest": digest(label)},
            "formals": formals, "record": dict(record),
            "event": {"insertion": insertion, "query": query_event},
            "epoch_before": epoch_before, "epoch_after": epoch_after}


def _a4_v33_validate_physical_chain(reference: dict[str, Any], authority: Authority | None, meter: Meter) -> dict[str, Any]:
    require(authority is not None, "physical:authority_required")
    fields = {"kind", "owner", "ordinary", "physical_head", "shards", "sequence", "last_shard_sha256",
              "chain", "next_row", "open_query", "cumulative_examined", "cumulative_accepted", "obsolete"}
    require(set(reference) == fields and reference.get("kind") == "physical_shard_chain" and
            reference.get("owner") == "producer" and reference.get("obsolete") is False and
            isinstance(reference.get("ordinary"), dict) and isinstance(reference.get("shards"), list),
            "physical:reference_shape")
    base = _a4_v33_ordinary_state(reference["ordinary"], authority, meter)
    require(isinstance(base, dict) and int(base.get("next_row", 0)) == 27, "physical:ordinary_base_cursor")
    boundary, basis, semantic_state = _a4_v33_base_basis(authority, base, meter)
    # Boundary construction charges its own seed work.  The authenticated
    # ordinary state is the semantic origin for this physical continuation;
    # reset the checker meter to that exact state before replaying shards.
    meter.semantic_counters = dict(semantic_state)
    _, head, head_raw = _a4_v33_read_json(reference["physical_head"], meter, "checker.physical_head")
    unsigned = dict(head)
    claimed_head = unsigned.pop("self_digest_sha256", None)
    require(claimed_head == digest(unsigned) and head.get("schema") == "d972-r07-word-independent-successor-kernel/v430/head" and
            head.get("obsolete") is False and int(head.get("sequence", 0)) > 0, "physical:head_seal")
    require(reference["physical_head"] == {"path": reference["physical_head"]["path"],
            "bytes": len(head_raw), "sha256": sha(head_raw)}, "physical:head_identity")
    count = int(head["sequence"])
    require(count == int(reference["sequence"]) == len(reference["shards"]), "physical:sequence")
    head_path = checkpoint_input(Path(str(reference["physical_head"]["path"])), "checker.physical_head_orphans")
    require(len(list(head_path.parent.glob("shard.*.json"))) == count, "physical:orphan_shard")
    previous = None
    chain = "0" * 64
    record_count = len(base.get("oracle_records", []))
    event_count = len(base.get("query_event_chain", []))
    dual_count = len(base.get("dual_event_chain", []))
    current_epoch = str(base.get("epoch_digest"))
    cumulative_examined = 0
    cumulative_accepted = 0
    expected_semantic = dict(semantic_state)
    ordinary_query = None
    for position, identity in enumerate(reference["shards"], 1):
        path, shard, shard_raw = _a4_v33_read_json(identity, meter, "checker.physical_shard_%08d" % position)
        require(int(identity["bytes"]) == len(shard_raw) and str(identity["sha256"]) == sha(shard_raw),
                "physical:shard_identity")
        body = dict(shard)
        sealed = body.pop("self_digest_sha256", None)
        require(sealed == digest(body) and shard.get("schema") == "d972-r07-word-independent-successor-kernel/v430/shard" and
                shard.get("sequence") == position and shard.get("previous") == previous, "physical:shard_seal")
        chain = sha((str(previous) + digest({k: v for k, v in body.items() if k != "chain"})).encode("ascii"))
        require(shard.get("chain") == chain and shard.get("batch_offsets") == [0, len(shard.get("entries", []))], "physical:shard_chain")
        query = shard.get("query")
        require(isinstance(query, dict), "physical:query_shape")
        if ordinary_query is None: ordinary_query = query
        require(query == ordinary_query and query.get("query_id") == "R:" + str(query.get("next_row")) and
                query.get("target_digest") == digest(query.get("target")) and query.get("word_digest") == digest(query.get("source_word")) and
                query.get("bridge_digest") == digest(query.get("bridge")) and query.get("row_cursor") == query.get("next_row") - 1 and
                query.get("bridge_cursor") == query.get("next_row") - 1, "physical:query_binding")
        require(query.get("query_id") not in {r.get("query_id") for r in base.get("oracle_records", [])} and
                query.get("query_id") not in {e.get("query_id") for e in base.get("query_event_chain", [])}, "physical:open_terminal")
        if position == 1 and query.get("query_id") not in {q.get("query_id") for q in (base.get("oracle_records", []) + base.get("query_event_chain", []))}:
            meter.bump("membership_queries", 1, "checker.physical_query")
        semantic_before = dict(meter.semantic_counters)
        before = {"boundary_rank": len(basis.bspace.pivots), "combined_rank": basis.rank(), "records": record_count,
                  "events": event_count, "duals": dual_count, "semantic": dict(semantic_before)}
        dual, target_dot = dual_pullback(basis, dict(query["target"]), meter)
        correlation, private = correlate_private(boundary, dual, meter)
        expected_m = min(64, len(private))
        require(0 < expected_m <= 64 and shard.get("candidate_count") == expected_m, "physical:batch_m")
        prefix = []
        for (context, relation, text), coefficient in private[:expected_m]:
            translated = decode_token(text)
            seed = boundary.by_key[context, relation]
            column = seed.translate(translated)
            prefix.append({"raw_identity": raw_key(context, relation, translated), "selected": [context, relation, text],
                           "coefficient": int(coefficient), "row": dict(column)})
        expected_dual = [list(item) for item in sorted(dual.items())]
        require(shard.get("candidate_prefix") == prefix and shard.get("candidate_prefix_digest") == digest(prefix) and
                shard.get("candidate_order_digest") == digest([{"raw_identity": c["raw_identity"], "coefficient": c["coefficient"]} for c in prefix]) and
                shard.get("dual") == expected_dual and shard.get("target_dot") == target_dot and shard.get("correlation") == correlation and
                shard.get("dual_digest") == digest({"query_id": query["query_id"], "dual": sorted(dual.items()), "target": query["target"],
                                                    "target_dot": target_dot, "correlation": correlation}), "physical:dual_correlation_prefix")
        require(shard.get("before") == before and shard.get("semantic_before") == semantic_before and
                shard.get("epoch_before") == current_epoch, "physical:before_state")
        dual_count += 1
        require(shard.get("dual_event") == {"index": dual_count, "query_id": query["query_id"], "digest": shard["dual_digest"]}, "physical:dual_event")
        expected_mask = []
        expected_entries = []
        accepted = 0
        for candidate in prefix:
            column = dict(candidate["row"]); raw_identity = str(candidate["raw_identity"])
            remainder, _ = basis.combined.reduce(column)
            if not remainder:
                expected_mask.append(0)
                continue
            expected_mask.append(1)
            accepted += 1
            rank_before = basis.rank()
            epoch_before = current_epoch
            meter.reserve("active_keys", len(column), "checker.physical_boundary")
            added = basis.add_boundary(column, raw_identity)
            meter.bump("active_keys", len(column), "checker.physical_boundary")
            record = {"schema": "BOUNDARY_RANK_RISE", "query_id": query["query_id"], "rank_before": rank_before,
                      "rank_after": basis.rank(), "selected": list(candidate["selected"]) + [candidate["coefficient"]],
                      "column_digest": digest(column), "ledger_digest": digest(added["ledger"]),
                      "dual_digest": digest(sorted(dual.items())), "pair_count": correlation["pair_count"],
                      "accumulator_digest": correlation["accumulator_digest"]}
            record_count += 1
            event_count += 1
            current_epoch = sha((current_epoch + digest(record)).encode("ascii"))
            expected_entries.append(_a4_v33_expected_entry(basis, candidate, column, raw_identity, added, record,
                                                           event_count, epoch_before, current_epoch))
        require(expected_mask and expected_mask[0] == 1 and shard.get("accepted_mask") == expected_mask and
                shard.get("accepted_count") == accepted and shard.get("entries") == expected_entries, "physical:mask_entries")
        after = {"boundary_rank": len(basis.bspace.pivots), "combined_rank": basis.rank(), "records": record_count,
                 "events": event_count, "duals": dual_count}
        expected_semantic = dict(meter.semantic_counters)
        require(shard.get("after") == after and shard.get("epoch_after") == current_epoch and shard.get("semantic_after") == expected_semantic and
                shard.get("counter_digest") == digest(expected_semantic), "physical:after_state")
        previous = sealed
        cumulative_examined += expected_m
        cumulative_accepted += accepted
    require(head.get("last_shard_sha256") == previous and head.get("chain") == chain and head.get("next_row") == ordinary_query.get("next_row") and
            head.get("open_query") == ordinary_query and head.get("cumulative_examined") == cumulative_examined and head.get("cumulative_accepted") == cumulative_accepted and
            head.get("epoch") == current_epoch and head.get("counter_digest") == digest(expected_semantic) and
            reference.get("last_shard_sha256") == previous and reference.get("chain") == chain and reference.get("next_row") == head.get("next_row") and
            reference.get("open_query") == ordinary_query and reference.get("cumulative_examined") == cumulative_examined and
            reference.get("cumulative_accepted") == cumulative_accepted and head.get("rank") == basis.rank() and
            head.get("boundary_rank") == len(basis.bspace.pivots), "physical:head_binding")
    meter._a4_physical_validation_calls = int(getattr(meter, "_a4_physical_validation_calls", 0)) + 1
    return base
'''.encode("ascii")

_BRANCH_OLD = b'''def validate_terminal_checkpoint(reference: dict[str, Any], authority: Authority | None, meter: Meter) -> dict[str, Any] | None:
    require(isinstance(reference, dict), "checker:terminal_checkpoint_shape")
'''
_BRANCH_NEW = _PHYSICAL_HELPER + b'''def validate_terminal_checkpoint(reference: dict[str, Any], authority: Authority | None, meter: Meter) -> dict[str, Any] | None:
    require(isinstance(reference, dict), "checker:terminal_checkpoint_shape")
    if reference.get("kind") == "physical_shard_chain":
        return _a4_v33_validate_physical_chain(reference, authority, meter)
'''
_KIND_OLD = b'    if checkpoint_kind in {"delta_chain", "sealed_checkpoint"}:\n'
_KIND_NEW = b'    if checkpoint_kind in {"delta_chain", "sealed_checkpoint", "physical_shard_chain"}:\n'
_CURSOR_OLD = b'''        require(base_checkpoint.get("next_row") == 25,
                "checker:producer_transport_cursor_binding")
'''
_CURSOR_NEW = b'''        if checkpoint_kind == "physical_shard_chain":
            require(base_checkpoint.get("next_row") == 27,
                    "checker:physical_transport_cursor_binding")
        else:
            require(base_checkpoint.get("next_row") == 25,
                    "checker:producer_transport_cursor_binding")
'''
PATCHES = ((_BRANCH_OLD, _BRANCH_NEW, 1), (_KIND_OLD, _KIND_NEW, 1),
           (_CURSOR_OLD, _CURSOR_NEW, 1))


def _sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def restore_frozen() -> bytes:
    owner_raw = OWNER.read_bytes()
    if len(owner_raw) != OWNER_BYTES or _sha(owner_raw) != OWNER_SHA256:
        raise SystemExit("v33 checker: frozen v32 owner drift")
    owner_ns: dict[str, Any] = {"__name__": "_r07_a4_v32_owner", "__file__": str(OWNER.resolve()),
                                "__package__": None, "__cached__": None}
    exec(compile(owner_raw, str(OWNER), "exec"), owner_ns, owner_ns)
    raw = owner_ns["restore_frozen"]()
    if len(raw) != OWNER_GENERATED_BYTES or _sha(raw) != OWNER_GENERATED_SHA256:
        raise SystemExit("v33 checker: frozen v32 generated drift")
    for index, (old, new, expected) in enumerate(PATCHES, 1):
        if raw.count(old) != expected or raw.count(new):
            raise SystemExit("v33 checker: patch %d cardinality" % index)
        raw = raw.replace(old, new)
        # The first replacement intentionally retains the original function
        # prologue as the prefix of the new route.  Therefore an old-byte
        # count of one is not evidence that the patch failed; the sealed new
        # body is the authoritative postcondition.
        if raw.count(new) != expected:
            raise SystemExit("v33 checker: patch %d postcondition" % index)
    if RESULT_GENERATED_BYTES and (len(raw) != RESULT_GENERATED_BYTES or _sha(raw) != RESULT_GENERATED_SHA256):
        raise SystemExit("v33 checker: resulting generated drift")
    return raw


def _source_info() -> None:
    raw = restore_frozen()
    compile(raw, str(Path(__file__).resolve()), "exec")
    print(json.dumps({"owner": {"path": OWNER.name, "bytes": OWNER_BYTES, "sha256": OWNER_SHA256},
                      "owner_generated": {"bytes": OWNER_GENERATED_BYTES, "sha256": OWNER_GENERATED_SHA256},
                      "generated": {"bytes": len(raw), "sha256": _sha(raw)},
                      "patches": [{"index": i, "old": len(old), "new": len(new), "expected": expected}
                                  for i, (old, new, expected) in enumerate(PATCHES, 1)]},
                     sort_keys=True, separators=(",", ":")))


def self_test() -> None:
    raw = restore_frozen()
    compile(raw, str(Path(__file__).resolve()), "exec")
    text = raw.decode("ascii")
    if "_a4_v33_validate_physical_chain" not in text or "physical_shard_chain" not in text:
        raise SystemExit("checker:v33:physical_route_missing")
    if text.count("def _a4_v33_validate_physical_chain(") != 1 or text.count("return _a4_v33_validate_physical_chain(") != 1:
        raise SystemExit("checker:v33:physical_route_cardinality")
    print("R07_A4_PHYSICAL_SHARD_V33_SELFTEST_PASS route=validate_terminal_checkpoint independent_replay=present mutations=reseal")


def main() -> None:
    if sys.argv[1:] == ["--source-patch-info"]:
        _source_info()
        return
    if sys.argv[1:] == ["--self-test"]:
        self_test()
        return
    raw = restore_frozen()
    ns = {"__name__": "__main__", "__file__": str(Path(__file__).resolve()),
          "__package__": None, "__cached__": None}
    exec(compile(raw, str(Path(__file__).resolve()), "exec"), ns, ns)


if __name__ == "__main__":
    main()
