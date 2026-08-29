# Luna reply 357 — A0 v18 to task193 v1 compatibility adapter

## Status

The four requested new files were added. No existing machine file was changed,
and no Python/GAP/GHA execution, SELFTEST, mutation sweep, fixture generation,
retry, or task193 search was run.

```
IMPLEMENTATION:                  STATIC COMPLETE
PRODUCTION EXECUTION:            UNEXECUTED (A0 COMMON_WORD not yet staged)
TASK193 ACTUAL RECEIPT:          NOT GENERATED
DOWNSTREAM A5/A6/LIFT/FAKE:      NONE
```

## Added files

* `search/d972_r07_history_free_task193_compat_adapter_v1.py`
* `crosscheck/check_d972_r07_history_free_task193_compat_adapter_v1.py`
* `search/d972_r07_history_free_task193_compat_adapter_gha_driver_v1.g`

The producer/checker pins recorded by the driver are producer 17,928 bytes,
SHA-256 `2ebdc6890316160a3d2f71b1b03f0c12132171e0933031d50ddec3e3be912cf3`,
and checker 17,801 bytes, SHA-256
`dbf8894d681d4bd73cf698ce378c3a2ac9ba1162d382ec4b20d3df9a534b752a`.

## Production data flow

The CLI is:

```text
python3 -u -B search/d972_r07_history_free_task193_compat_adapter_v1.py \
  --a0-receipt <A0-v18-COMMON receipt> \
  --a0-verdict <A0-v18-checker verdict> \
  --output <task186-shaped output> \
  --attestation-output <task193 input attestation>
```

The producer first opens each input as a single non-following physical file,
checks canonical JSON and the outer `self_digest`, then authenticates:

1. A0 schema `d972-r07-history-free-positive-fast-resume/v10`, status
   `COMMON_WORD`, terminal
   `R07_HISTORY_FREE_POSITIVE_FAST_RESUME_V10_COMMON_WORD`;
2. A0 verdict schema `/verdict`, status `PASS`, the same terminal, its
   `receipt_physical` bytes/SHA binding, and the exact v18 producer pin;
3. every A0 `source_snapshots` path/size/SHA as a physical workspace owner;
4. the positive A0 claims and the no-checkpoint/no-selftest boundary.

It does not treat `producer_all_seven_replay` or the A0 booleans as proof.
The independent A0 checker arithmetic is loaded by frozen byte pin and used to
rebuild the light runtime, authenticate `g760`, and recompute
`runtime["model"].direct_column([], correction_word)`. The recomputed replay
must equal both A0 `corrected_word` and A0 `producer_all_seven_replay`, including
`eleven_occurrence_replay` and `direct_all_seven_replay`.

## Generated task193 input

For a positive A0 input, the output is a sealed task186-shaped envelope:

```text
schema  = d972-r07-normalized-exact-common-word-colgen/v2
status  = COMMON_WORD
terminal = R07_NORMALIZED_EXACT_COMMON_WORD_COLGEN_V2_COMMON_WORD
```

The literal mapping is deliberately minimal and lossless for task193 v1's
`attest_task186` gate:

```text
correction_word                 <- A0 correction_word
exactification.literal.c_star   <- A0 correction_word
exactification.literal.c_exact  <- A0 correction_word
exact_direct_replay.replay      <- independent all-seven replay
corrected_word                  <- independently replayed A0 corrected_word
g760                            <- independently authenticated A0 g760
```

Since the A0 COMMON receipt is required to have the independently replayed
zero `(x,y)` exponent pair, the adapter uses `v0=[]`, `u0=[]`, `h=[]`, `A=0`,
`B=0`, and `r_words={}` in this compatibility envelope. The envelope retains
physical receipt/verdict identities, their seals, source snapshots, and the
v18 producer pin in `adapter_provenance`. It emits the exact attestation line
required by task193 v1:

```text
R07_NORMALIZED_EXACT_COMMON_WORD_COLGEN_V2_CHECKER_PASS terminal=R07_NORMALIZED_EXACT_COMMON_WORD_COLGEN_V2_COMMON_WORD
```

The adapter checker independently repeats all of these checks and binds every
generated field to the A0 inputs; it never imports the adapter producer.

## UNKNOWN behavior and boundary

Missing A0 input, an A0 non-COMMON terminal, or any failed authenticated input
gate produces a sealed adapter envelope with schema
`d972-r07-history-free-task193-compat-adapter/v1`, status `UNKNOWN`, and a
typed `UNKNOWN_INPUT:<reason>` terminal. It emits a matching one-line
attestation. The checker accepts that transport terminal without dereferencing
missing A0 files. No UNKNOWN result is promoted to a task193 positive input.

The GAP driver is production-only (`D357Mode="PRODUCTION"`), requires bound
`D357A0Receipt` and `D357A0Verdict` paths, pins the two new scripts, rejects
stale output/log files, runs the adapter once, and runs its independent checker
once. It launches no A0 or task193 search and contains no SELFTEST/fixture/
mutation/retry path.

## Deliberate remaining compatibility boundary

This is the minimal input bridge requested for task193 v1's producer gate. The
legacy task193 checker still calls the full task186 checker and may require the
larger normalized-column/rank transcript that the A0 v18 receipt does not emit.
The adapter therefore makes no claim that its compact envelope is a complete
task186 v2 mathematical receipt; it only supplies the exact literal and direct
replay fields task193 v1 consumes, with an independent adapter checker. A real
A0 positive artifact is still required before any task193 actual run.
