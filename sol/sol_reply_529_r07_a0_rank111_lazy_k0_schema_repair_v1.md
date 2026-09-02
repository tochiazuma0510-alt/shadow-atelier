# Sol reply 529 -- minimal schema repair for the rank111 lazy K=0 successor

## Verdict

`READY_FOR_REAUDIT`

The two Task528 blockers are repaired in exactly these four new versioned
outputs:

- `search/d972_r07_a0_actual_tau_free_lazy_k0_seed_v6.py`
- `crosscheck/check_d972_r07_a0_actual_tau_free_lazy_k0_seed_v10.py`
- `search/d972_r07_a0_actual_tau_free_lazy_k0_rank111_resume_gha_driver_v14.g`
- this reply

V5/v9/v13 and Task525 were not overwritten.  No full replay, production, GHA,
workflow, git, release, or v220 mutation was performed.

Exact executable fingerprints are:

| output | bytes | SHA-256 |
|---|---:|---|
| producer v6 | 42434 | `43f5dac842fd4025d714b99a1e16f63ecf7cc2a35c53d8f106748a4d06a13b1c` |
| checker v10 | 33455 | `36db2a4e5eafb9a2c6a23d0ec9d280f22503b033fcf098f1c2ee19f32db5dd78` |
| driver v14 | 8692 | `c46fedb85495128a6e1f5e84c13ffc55d95cb2ece7b565050ba5777cfc868bd4` |

The independently matching v6 schema binding is
`c76189ad8f5b43eefea62f92ff1942e097be57802babe2622ee6c1bf13fb6050`.

## Repair A -- authenticated round chain

Both owners now require exact `type(value) is int` for every new record round.
A shared chain gate starts at legacy round 73, requires the first v6 round to
be greater than 73, and requires every later v6 round to be strictly greater
than its predecessor.  Gaps remain allowed.  Checkpoint and result rounds are
exact integers and must be at least the authenticated last v6 record round, or
at least 73 when there is no v6 record.

The producer applies this gate when validating or constructing a checkpoint,
before each new production commit, and before replaying sealed v6 records.
Replay names the already chain-authenticated round and requires the regenerated
record to contain that same value; it no longer merely converts or silently
accepts an untrusted stored value.  The checker applies the same rule at the
checkpoint/result boundary and again on entry to its live `replay_new` path.

Resealed first-new rounds 1 and 73, duplicate and decreasing later rounds, and
a float round were all rejected.  The checker self-test reaches `replay_new`
for these mutations before any expensive physical setup.

## Repair B -- exact integer schema

V6 and v10 reject every JSON boolean or float recursively inside a new v6
record, then explicitly require exact integers for:

- round, old/new rank, scalar, record version and direct scalar;
- correction seed index, every delta letter, exact exponent pair, K,
  formula scalar, N coefficients and normalized exponent quotients;
- every required coordinate; fibre, coordinate, kernel, q0-id and gamma-id
  cursor fields; checked-fibre count; and every selector counter;
- action-source `family_index` and `scalar`.

The same exact boundary covers new checkpoint accepted count, rank and round,
completed/attempt counters, known progress integers, result cardinalities and
round, and durable-state byte/count/rank metadata.  Counter addition no longer
normalizes untrusted values through `int(...)`.  Result
`elapsed_seconds` remains a legitimate float and is deliberately outside the
recursive record/checkpoint integer gate.

All pre-existing digest, selector, formula, direct-pair, row/fresh,
exponent/N/E, remainder, pivot, add/update and claims checks are retained.  V10
still does not import v6 or a producer selector validator.

## Bounded evidence

All writable fixtures were repository-external.  The bounded commands and
markers were:

```text
python -m py_compile <v6> <v10>                         TASK529_PY_COMPILE_PASS
python -B <v6> --mode FIXTURE --output <TEMP>           status=FIXTURE
python -B <v10> --self-test                             V10_CHECKER_SELFTEST_PASS
.\gap.ps1 <ReadAsFunction harness for v14>              V14_GAP_PARSE_PASS
captured GAP D527Cmd | bash -n                          TASK529_GENERATED_D527CMD_BASH_N_PASS
```

The producer fixture rejected the exact-integer mutations
`bool_scalar,float_direct_scalar,float_exponent,float_N,bool_counter,float_cursor`
and the round mutations
`first_1,first_73,duplicate,decreasing,noninteger`.  V10 rejected the same
sets through `replay_new`, retained the four earlier
`K!=0,second_insert,direct_scalar,epsilon` rejections, and reported
`producer_selector_imported=false`.  A separate action-record fixture accepted
the valid integer record and rejected boolean `family_index` and float action
scalar in both owners.

A repository-external harness used the exact authenticated 68-source legacy
prefix, built a valid sealed v6 baseline, then recomputed the public v6 state
seal after every mutation.  Both producer and checker rejected all 16 cases:

```text
round_first_1, round_first_73, round_duplicate, round_decreasing,
round_noninteger, scalar_bool, direct_float, exponent_float, N_float,
counter_bool, cursor_float, cp_count_bool, cp_rank_float, cp_round_bool,
cp_counter_float, cp_progress_bool

TASK529_RESEALED_CHECKPOINT_MUTATIONS_PASS 16 owners=2
```

Mechanical AST/source comparison gave
`TASK529_MATH_SELECTOR_BYTE_CONFINEMENT_PASS`: producer
`formula_for_seed`, `formula_scalar`, `kernel_digest`, `support_states` and
checker `formula_for_seed`, `formula_scalar`, `support_states`,
`kernel_digest`, `public_source`, `first_action`, `replay_correction`,
`reason_type` are byte-identical to v5/v9.  Producer `direct_correction` and
`select_one` are identical after the required record-version 5-to-6 token
normalization.  Thus no task445 state, K0 formula, support schedule, physical
admission, update, resource or claims mathematics changed.

The mechanical diff sizes were `201/44` added/deleted lines for v5-to-v6,
`167/41` for v9-to-v10, and `36/36` for v13-to-v14.  The Python changes classify
as schema/marker aliases, exact numeric/round gates and their bounded fixtures.
The GAP changes classify solely as fresh v14 paths/preamble/markers and exact
v6/v10 byte/SHA pins.

V13-to-v14 transport confinement independently matched the permanent release,
run/job/head/API identity, complete ordered eight-member manifest, member-5
pin, stale gates, two-process shape and all resource limits.  V14 retains
`ulimit -v 5200000`, producer `7500/7200/4800000000/64`, checker `3600`, one
exact checker marker, and no production SELFTEST.  Its embedded producer and
checker pins match the final files.

## Limitations

This commission deliberately did not rerun the expensive task445/rank111
physical setup or claim a new row.  Task528 already passed that unchanged
mathematical/physical route; this repair is confined to its two schema
blockers.  Bounded tool output remains candidate evidence rather than Lean
verification.  K!=0 and every previously unsupported branch remain
claims-false `UNKNOWN_RESOURCE`; no numerator or mathematical conclusion is
changed.

`READY_FOR_REAUDIT`
