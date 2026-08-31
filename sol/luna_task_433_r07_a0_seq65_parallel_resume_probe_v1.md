# Luna task 433 — A0 sequence-65 parallel continuation and positive probe

Implement the smallest mechanical successor to the completed task431 and
task432 runs.  Do not change the mathematics, the v12 producer/checker, any
workflow, v220, or any earlier versioned file.  This task creates one exact
continuation driver and one task432-style positive-only probe for the same
authenticated sequence-65 checkpoint.

## 1. Exact input and release

The parent independently downloaded and hashed run `33337628476`, artifact
`9741582127`.  Its accepted v12 output checkpoint is:

```text
phase                    occurrence_queue
checkpoint_seq           65
seed/parent/action       44 / 523 / 2092
occurrence rank/frontier 1655 / 1132
occurrence payload nnz   227591095
physical rank/payload    0 / 0
bytes                    461087575
sha256                   8918df4407e91a7b4ab1a29246a23ba5b0ed1a7b6011f4abf74775cc33d82705
```

It is permanently mirrored as an exact one-entry zip:

```text
url    https://github.com/tochiazuma0510-alt/shadow-atelier/releases/download/archive-gha-checkpoints/d972_r07_a0_pb34_direct_quotient_owner_v12_seq65.checkpoint.zip
bytes  178918944
sha256 b27a70ffe4095f9c9760c51694e7b56d68efb3e22d7df4ecaab4513f7328dbcc
entry  d972_r07_a0_pb34_direct_quotient_owner_v12_output.checkpoint
```

The zip was reopened independently: exactly one entry, uncompressed bytes
461087575, extracted SHA-256 equal to the checkpoint pin above.

## 2. Allowed outputs

Create only:

1. `search/d972_r07_a0_pb34_direct_quotient_owner_gha_driver_v13.g`
2. `search/d972_r07_a0_prefix_positive_probe_v2.py`
3. `search/d972_r07_a0_prefix_positive_probe_gha_driver_v2.g`
4. `sol/luna_reply_433_r07_a0_seq65_parallel_resume_probe_v1.md`

No download, checkpoint load, production run, commit, push, dispatch, release
operation, or workflow edit.  Run seconds-scale fixtures only.

## 3. Continuation driver v13

Reuse the audited task431 recovery-driver structure, but use the exact
one-entry release above and distinct v13 paths.  Byte-pin and invoke the
unchanged files:

```text
producer search/d972_r07_a0_pb34_direct_quotient_owner_v12.py
         51884 bytes
         3016b6a21d9fafbf037dbb5384dcca81f49e1fa44ae45a466ff16f1fd13948b3
checker  crosscheck/check_d972_r07_a0_pb34_direct_quotient_owner_v12.py
         13334 bytes
         e6a16f63725cd23bb1cd8469e2a0d93c7774c979079b7314b653b7ffa439f891
```

The recovery shell must reject an absent/extra/duplicate/path entry, use
same-directory temporary files and atomic moves, require ordinary regular
non-symlink zip/input/seal/receipt files, and install a fresh hash-bound
one-shot receipt only after either the fresh or pre-existing branch validates
all pins.  GAP must compare its exact one-line content.  Do not retain the old
six-entry roster and do not invoke the sequence-40 parent-phase repair: this
input is already canonical `occurrence_queue` and ordinary v12 `cp_read`
must accept it directly.

Invoke v12 with the recovered input, a distinct output checkpoint, 9000
seconds and 4800000000 RSS bytes.  Invoke the unchanged checker with both
input and output checkpoint paths.  Require unique producer/checker PASS
markers.  Require external preamble
`D972_R07_A0_PB34_V13_RUN:=true;;`.  Use only `ci/out` artifacts.

## 4. Positive probe v2

Make v2 an exact minimal diff from the audited task432 wrapper v1.  Change
only the sequence-65 input bytes/SHA and informational original rank/frontier
to `1655/1132`, plus versioned marker/name text required to distinguish v2.
Keep the pinned v12 import, `FalseTruthDeque`, global reset/final restoration,
no-checkpoint contract, top-level `COMMON_CANDIDATE|UNKNOWN` boundary,
resource normalization, six-action positive-only UNKNOWN, and all promotion
flags false.  Do not add a diagnostic pass or retain physical payload after
the decision.

Its v2 driver is the task432 audited recovery/marker structure adapted to the
same exact one-entry sequence-65 release and distinct v2 paths.  Invoke the
probe for 9000 seconds / 4800000000 RSS bytes, then the unchanged v12 checker
with input checkpoint only and no output checkpoint.  Require external
preamble `D972_R07_A0_PREFIX_POSITIVE_PROBE_V2_RUN:=true;;`.

## 5. Bounded gates

Run only:

- Python AST/fixture for v2 without repository bytecode;
- exact source diff/allowlist against probe v1;
- unchanged v12 producer fixture and checker self-test;
- static no-checkpoint-write gate for the probe;
- reconstructed GAP commands, one-entry roster, receipt and marker checks;
- exact bytes/SHA of all four outputs and `git diff --check`.

Report explicitly that a probe UNKNOWN is not a negative result, and that
neither path promotes COMMON, compatible lift, fake, or Ihara without the
registered strict replay.
