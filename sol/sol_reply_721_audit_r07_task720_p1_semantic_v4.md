# Sol Task721 — Task720 P1 semantic producer v4 release audit

```text
VERDICT=PASS_P1_SEMANTIC_V4_SAFE_FOR_GHA
SAFE_TO_DISPATCH_GHA=yes
verified=false
```

The commissioned Task714 blockers and Task720 digest correction are closed.
This verdict authorizes only the real five-artifact semantic replay on GHA; it
does not promote any P1 equality, independent check, A0, lift, fake, or Ihara
claim before that replay succeeds.

## Frozen receipts

| path | bytes | LF | final LF | SHA-256 |
|---|---:|---:|---|---|
| `search/d972_r07_grade2_p1_componentwise_semantic_replay_v4.py` | 41259 | 381 | yes | `ff50d0ad50e080a15075bb52365987d9e389bf59e5e39666002b710947287a17` |
| `search/d972_r07_a0_first_rung_grade1_v4.py` | 144552 | 3326 | yes | `1fb4b29691f448782e7f7f2e2282e7067282bc619fb34b7214089c5a73e24dc4` |
| `search/d972_r07_grade2_specific_owner_prejoin_v1.py` | 47995 | 545 | yes | `38fcbe3757d1b14fd19f4f557f763c1f5f6a2e8da47e0e061707cf28c5064d73` |
| `sol/luna_task_720_r07_p1_semantic_equality_digest_repair_v4.md` | 2122 | 56 | yes | `1530533abd876edacbababf1b80f3f1282f3a3fe5889480b3a6ee2240f6873e3` |
| `sol/luna_reply_720_r07_p1_semantic_equality_digest_repair_v4.md` | 2324 | 55 | yes | `3e835d8430f92dbe12c39fab46a32f3eab81203ac430db9d4094bd61df8f77e1` |

The v4 producer exactly matches the parent-remeasured receipt.

## Narrow findings

### Equality records and corrected aggregate — PASS

The four ordered record/lower/lifted triples at lines 26--30 match Task715
literally.  Applying the source's own `canonical()` to
`list(EQUALITY_RECORDS)` independently returned exactly:

```text
99da0c4a42a0c747cde28cd91797d7c655d797c27f8f78a7423142bf56bc5dbf
```

Production prepare validates the four literals and recomputes this digest
before receipt emission (line 166).  Production join reaches
`validate_prepare_receipt`, which independently recomputes the received list
and then requires the receipt field to equal the same fixed digest (line 237).
A coordinated valid-hex record mutation with its aggregate recomputed rejects
at `equality_record_pin`; exact records with a different valid-hex aggregate
reject at `equality_digest_pin`.  No free digest literal remains.

### Indexed block DAG pins — PASS

The four Task715 DAG literals are fixed in index order at line 32.  Block
replay first reconstructs and hashes the complete DAG, compares it to the
authenticated block body, and then requires the indexed pin at lines 199--200.
Join requires the same indexed literal at line 250.  A different but valid
64-hex digest rejects at `block_dag_digest`.

### CLI phase exclusion — PASS

`validate_cli` requires exactly one of selftest, prepare, block, or join and
requires `--index` iff block is selected.  `main` invokes it before phase work.
No phase, two phases, block without index, selftest+index, prepare+index, and
join+index all reject through this production validator.  The three requested
CLI commands each exited 1 with `index_phase` before touching their dummy
paths.

### Regression and semantic boundary — PASS

The v4-versus-v3 diff is five insertions and four deletions: the one corrected
aggregate literal, two production recomputation checks, one added mutation,
and its selftest reporting field.  There is no arithmetic or claim change.
The v4-versus-v2 delta retains every Task711 repair: safe-root and registered
loader, authenticated packet ranges and final EOF, full Q1 endpoint/Walsh
identity, structural three-value envelope and safe root, one cached block
context, deque FIFO, complete four-actor rows, strict nested receipt types and
false flags, and the exact count equation
`8232 + 32928 + 24180 = 65340`.

The accepting bounded five-receipt fixture passed the same
`validate_join_receipts` used by production join.  I found no deterministic
exception on this perfect typed input and no commissioned mutation accepted
without a hash collision.

All prepare, block, and terminal receipts retain
`independent_checker=false`, `precision2=false`, `A0=false`, `COMMON=false`,
`COMPATIBLE_LIFT=false`, `FAKE=false`, `IHARA=false`, and `verified=false`.

## Bounded execution

```text
python -m py_compile search/d972_r07_grade2_p1_componentwise_semantic_replay_v4.py
exit 0

python -B search/d972_r07_grade2_p1_componentwise_semantic_replay_v4.py --selftest
exit 0
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

An additional direct bounded import reproduced the producer digest and exact
equality digest, accepted the unmodified complete receipt fixture, and rejected
the coordinated equality, wrong aggregate, valid-hex DAG, empty/two-phase,
forbidden-index, and missing-index cases at their named production gates.

No real artifact, GHA, implementation edit, workflow action, or git operation
was performed.

```text
REAL_TASK554_REPLAY=DEFERRED_TO_GHA
verified=false
```

The reply's exact byte/LF/final-LF/SHA-256 receipt is supplied externally after
sealing because embedding its own digest would change its preimage.
