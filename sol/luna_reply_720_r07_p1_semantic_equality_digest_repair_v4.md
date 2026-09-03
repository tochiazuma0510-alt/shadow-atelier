# Task720 result — P1 semantic producer v4 equality-digest repair

Status: `READY_FOR_SOL_P1_SEMANTIC_V4_AUDIT`; `verified=false`.

Only the new v4 producer and this reply were created.  v3, the independent
checker, workflows, v220, and all earlier files remain unchanged.  No real
Task554 artifact replay, GHA, git, or parallel computation was performed.

## Exact semantic diff from v3

1. `EQUALITY_SHA` is corrected from the erroneous `42d64690...` literal to
   `99da0c4a42a0c747cde28cd91797d7c655d797c27f8f78a7423142bf56bc5dbf`.
2. Production `replay_prepare` requires
   `sha(canonical(equality)) == EQUALITY_SHA` before emitting its receipt.
3. Production `validate_prepare_receipt`, used by join, independently requires
   `sha(canonical(equality_receipts)) == EQUALITY_SHA`, then requires the
   received aggregate field to equal the same exact pin.
4. The existing coordinated record-plus-recomputed-digest mutation remains
   live and rejecting.  A second live mutation keeps all four exact records
   but supplies a different valid-hex aggregate; it also rejects.

No arithmetic, schema, count, ancestry, DAG pin, CLI phase, claim flag, packet
range, block kernel, or memory behavior changed.

## Bounded commands and results

```text
python -m py_compile search/d972_r07_grade2_p1_componentwise_semantic_replay_v4.py
PASS

python -B search/d972_r07_grade2_p1_componentwise_semantic_replay_v4.py --selftest
status=PASS
fixture_accept=2
rejections=34
coordinated_equality_mutation=REJECT
noncanonical_equality_aggregate=REJECT
valid_hex_dag_mutation=REJECT
live_entry_points=exact_root,prepare_packet_range,block_envelope,actor_row,
  block_replay_kernel,projector_identity,join_receipt_validator,cli_validator

--selftest --index 0: exit 1, index_phase
--prepare-replay fixture --index 0: exit 1, index_phase
--join-receipts a b c d e --index 0: exit 1, index_phase
```

`REAL_TASK554_REPLAY=DEFERRED_TO_GHA`; `verified=false`.

## Exact output receipt

| file | bytes | LF | final LF | SHA-256 |
|---|---:|---:|---|---|
| `search/d972_r07_grade2_p1_componentwise_semantic_replay_v4.py` | 41259 | 381 | true | `ff50d0ad50e080a15075bb52365987d9e389bf59e5e39666002b710947287a17` |

The reply's exact final receipt is supplied externally after sealing because
embedding its own digest would change the preimage.
