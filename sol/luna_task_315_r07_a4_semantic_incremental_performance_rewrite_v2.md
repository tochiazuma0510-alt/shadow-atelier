# Luna task 315 — R07 A4 semantic, incremental, performance rewrite v2

From: Sol / 2026-08-28

Role: Luna implementation only.  This is a bounded versioned rewrite after
the independent Sol(max) task313 `REJECT`.  Read
`sol/sol_reply_313_r07_a4_correctness_performance_code_audit_v1.md` in full
before editing.  Every F1--F13 and every performance finding there is
load-bearing; this commission does not authorize weakening a gate.

Do not run actual A4, do not run a large local Python/GAP job, do not edit a
workflow, v220, a predecessor, or any existing v1 path.  The independently
accepted task198 authority is not staged yet, so production must fail closed
with a typed static-blocked terminal.  A bounded single-process syntax check
is permitted, but leave semantic execution to a later independent audit and
GHA SELFTEST.

## 1. Write exactly five new files

1. `search/d972_r07_word_independent_successor_kernel_v2.py`
2. `crosscheck/check_d972_r07_word_independent_successor_kernel_v2.py`
3. `search/d972_r07_word_independent_successor_kernel_gha_driver_v2.g`
4. `search/certs/d972_r07_word_independent_successor_kernel_selftest_v2_20260828.json`
5. `sol/luna_reply_315_r07_a4_semantic_incremental_performance_rewrite_v2.md`

Do not modify the v1 bundle.  The v2 driver must pin exact byte lengths and
SHA-256 values of the v2 producer, checker, and fixture.  The `.g` file must
be ASCII-only.

## 2. Preserve the mathematical contract

The producer must implement the v188/v231 word-independent successor kernel
using the complete task198 6,441-row presentation, the v189 ten typed
coordinates, the task232 literal context substitutions, the four marked
roof actions, a complete invariant closure, and the v247 word-bearing basis
anchor.  It must retain the exact distinction between five E3 and five E4
typed coordinates, including the two different `C21` coordinates.

The only positive production terminal is

```text
R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V2_PASS
```

and it is reachable only after every certificate gate below.  A positive
status must be `COMPLETE`; the `terminal` field must be passed explicitly and
must equal the token above.  Do not broaden an allowlist to accept a generic
`COMPLETE` terminal.

## 3. Task198 authority and literal roster

Implement one exact canonical acceptance-manifest schema which binds:

- producer run, checker run, immutable head(s), artifact id, ZIP digest,
  member bytes/SHA, and receipt self-digest;
- both exact producer/checker terminal-line digests;
- exact current task198 producer/checker/driver source identities; and
- the accepted receipt basename.

The four production authority paths must be exact resolved descendants of
`ROOT/ci/in` with registered basenames.  Reject `..`, symlink/alias escape,
absolute substitutions, or mere textual `ci/in/` prefixes.  Apply the same
resolved-containment discipline to outputs and checkpoints.

Until the real manifest and its exact driver pin are staged, production must
return

```text
STATIC_BLOCKED:TASK198_AUTHORITY_NOT_STAGED
```

with every A4 milestone and every lift/fake/Ihara flag false.  The SELFTEST
fixture may contain a tiny synthetic authority object, visibly marked
`synthetic=true`; it is not accepted production authority.

For a real receipt validate canonical bytes and the exact layer-local roster:

```text
Gamma_Cayley ordinals = 1..6318
action ordinals       = 1..104
Q0_lift ordinals      = 1..19
```

Do not reinterpret these as global 1..6441 ordinals.  Bind and replay all
seven chunk seals, `normal_generation_proof`, exact normal-closure fields,
bridge image/kernel orders, ten-to-eleven insertion, seven blocks, eleven
occurrences, four marked inverse replays, typed-ledger/row/replay digests,
and the complete v188 evaluator ABI, widths, coordinate digest, and canaries.

## 4. Lightweight runtime is mandatory

Neither v2 program may call `p179.build_runtime`, task176
`enumerate_q0_sections`, `scan_memberships`, `prove_L`, or any equivalent
full-Q0/global-roster builder.  It may not construct the 1,469,664 Q0 states,
2,939,328 edges, the raw section store, or a second task175 6,441-row roster.

Build only the local authenticated ingredients needed by A4:

- PB3/PB4 blob multiplication, inverse, action, and codecs;
- the ten task232 context substitutions and boundary-source rows;
- the four marked generator actions; and
- the task198 receipt's already authenticated 6,441 literal rows.

Cache the forty marked actor values once in each process.  Bucket a sparse
row by typed coordinate so an action does not rescan the whole row ten times.
Producer and checker each parse the 31 MB task198 input once; the independent
checker must still reconstruct all 6,441 defects once, because that is
necessary independent work.  Do not duplicate the task198 presentation in
the A4 output; retain an exact authority reference plus A4-specific records.

## 5. One live incremental coefficient echelon

Replace every rebuild-per-membership path by one live coefficient-carrying
total `B+K` echelon per implementation.  Insert a certified boundary or K row
once and reduce all later candidates against the retained state.  Keep a
separate live boundary-only echelon for boundary membership/certificates.

Every pivot row must retain fully scaled ancestry to stable raw labels:

```text
B:<raw translated-boundary record index>
K:<raw accepted-kernel record index>
```

Row addition, scaling, swap, insertion, and reduction must update those
coefficients exactly over F3.  Before accepting any returned coefficient
map, replay its sparse sum against the raw labelled rows.  The producer must
export boundary and K ancestry all the way to raw labels; private pivot IDs
are forbidden.

The checker must implement a different coefficient-carrying echelon.  It
must compare producer and checker elements/spans through an explicit
producer-to-checker change-of-basis modulo independently rebuilt boundaries.
Never compare coordinate dictionaries belonging to different bases.

The report must give an exact count of insertions, reductions, and rank
raises and a static complexity bound for the live algorithm.  There must be
no loop which reconstructs all retained B+K rows for each of 6,441 queries.

## 6. Word ancestry and v247 anchor

Use a persistent ancestry DAG or equivalent sharing representation.  Do not
copy/flatten inherited term lists at every action.  Give the conjugator list
one explicit composition convention and replay it against the stored literal
`conjugated_word`, including a depth-two noncommuting canary.

For every exported basis row require a direct ten-context source-word
evaluation, and prove

```text
direct_defect(source_word) - stored_basis_row
```

by a boundary-only raw-label coefficient receipt.  Compute the H2(9)
projection and the least-index v247 `k_z` anchor only after that binding.
Replay every projected exponent, inverse scalar, powered source word, coarse
identity, successor value, and ten-context value independently.

All ancestry, word, support, receipt, and serialized-output sizes need live
caps.  Word materialization must stream or decode the shared DAG with a cap;
unmetered flattening is forbidden.

## 7. Complete checker replay

The checker must independently reconstruct and replay, not shape-check:

- every producer initial source word, ten chains, and defect row;
- every raw translated boundary row and every exported boundary coefficient;
- every accepted K row, membership ancestry, source word, and basis binding;
- every negative dual: normalization, annihilation of all retained B/K rows,
  zero boundary correlation, and nonzero target pairing;
- all four producer action matrices and action/closure equations;
- the full producer-to-checker basis change and equal invariant span; and
- every v247 anchor field and literal word replay.

Replace the v1 vector tautologies by direct word/group or authenticated
structural replays.  A checker Boolean copied from the producer is never a
proof.

## 8. Terminals, exact-one driver, and nonpositive envelopes

The driver must delete/reject stale outputs before work and require exactly
one complete producer line, exactly one complete checker line, exact terminal
equality, nonempty sealed receipt/verdict, and exactly one final sentinel.
Do not use `tail -n 1` or a `grep` whose count is ignored.

For every `UNKNOWN_INPUT`, `UNKNOWN_RESOURCE`, or `STATIC_BLOCKED` envelope,
both implementations must require a typed reason, status/terminal agreement,
zero A4 milestones, and all downstream lift/fake/Ihara flags false.  A
resource terminal must contain the exact live cap, observed value, phase, and
last replayable state.  If genuine checkpoint restoration is not implemented,
name it `RANK_ZERO_RESTART`; do not advertise resume.

## 9. Live resource accounting

Wire every declared cap to executed work in both implementations:

- total wall time and RSS, including authentication, matrix tail, ancestry,
  sealing, and output;
- input, checkpoint, and serialized bytes;
- relator evaluations, boundary records, membership reductions, accepted
  ranks, queue actions, actor applications, dual correlations;
- ancestry nodes/decoded words and maximum decoded word length; and
- checker work.

Check wall/RSS inside every long loop and before/after serialization.  Do not
serialize the full output twice merely to hash and then write it; use one
bounded canonical byte object or a streaming scheme.  Remove the quadratic
pairwise F3 tautology loop and document the actual remaining dense-matrix
bound.

## 10. Production-shaped SELFTEST ownership

The SELFTEST must run the same authentication, live echelon, queue, ancestry,
resource, terminal, and checker owner functions as production on a small
fixture.  Include at least one positive closure with a depth-two
noncommuting action, one NONMEMBER dual, one alternate checker basis, and one
typed resource stop.

Use a fixed explicit mutation roster covering at least these distinct owners:

1. per-layer ordinal;
2. authority run/head/member binding;
3. canonical input bytes;
4. resolved-path traversal;
5. normal-generation proof;
6. bridge/typed occurrence ledger;
7. evaluator ABI/canary;
8. raw boundary coefficient;
9. live echelon inherited scale;
10. producer/checker basis change;
11. conjugator order;
12. source-word/basis-row boundary difference;
13. negative dual;
14. action matrix;
15. projected H2 exponent;
16. `k_z` inverse scalar/powered word;
17. live resource cap;
18. positive status/terminal;
19. nonpositive false-progress flag; and
20. duplicate producer/checker/final marker.

Each mutation must canonically change its owned object, reach the intended
semantic gate, be independently rejected, and be counted individually.

## 11. Reply and fixed accounting

The reply must list exact bytes/SHA-256 for all five files except its own
self-referential SHA, the static call/count/complexity bounds, every removed
full-space path, the fixed mutation roster and its expected owner, and any
syntax command actually run.  End with:

```text
TASK315/V2 IMPLEMENTATION:                    COMPLETE or BLOCKED
TASK313 F1--F13 REPAIR COVERAGE:              itemized
FULL Q0 / GLOBAL ROSTER RECONSTRUCTION:       FORBIDDEN / ABSENT
MEMBERSHIP ECHELON:                           LIVE INCREMENTAL
ACTUAL TASK198 AUTHORITY:                     NOT STAGED
EXECUTION:                                    UNEXECUTED
ACTUAL A4:                                    0/3
LIFT / FAKE / IHARA:                          NONE
```

`TASK315_R07_A4_SEMANTIC_INCREMENTAL_PERFORMANCE_REWRITE_V2_COMMISSION`
