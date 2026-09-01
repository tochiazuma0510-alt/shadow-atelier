# Luna task 467 -- recovered rank-99 checker-only replay

Role: Luna mechanical implementation only.  Do not run A0 production, dispatch
GHA, edit workflows, commit, push, or touch files outside the three outputs
below.

The Task451 producer completed three closed batches before its resource stop.
The following checker failure was a Python name-binding defect, not a
mathematical rejection:

```text
UnboundLocalError: cannot access local variable 'formulas'
```

This task repairs only that defect and makes an authenticated checker-only GHA
driver.  It must not rerun the producer.

## 1. Required outputs

Create only:

1. `crosscheck/check_d972_r07_a0_dual_anchored_active_batch_recovered_v2.py`;
2. `search/d972_r07_a0_dual_anchored_active_batch_recovered_checker_only_gha_driver_v1.g`;
3. `sol/luna_reply_467_r07_rank99_recovered_checker_only.md`.

## 2. Exact production and artifact binding

Bind the recovered production to:

```text
run_id       33512607989
artifact_id  9808605601
artifact     gap-run-out
head_sha     3316809e483223ec571ca7d6976dc1317c892441
original artifact digest
sha256:fb6b6b776b8b288952196f400a0d32d57fd2a5ddb9780a7718e55cffee8bafe1
```

The six extracted original files and exact pins are:

```text
d972_r07_a0_dual_anchored_active_batch_v1.json
173930 5079ddfbffbfc00cac6b2672cbef80f7eb2cce069a2dba87aa04e7cbc420c29a
d972_r07_a0_dual_anchored_active_batch_v1_checker.log
5595 83378497196b198ef257c4918eedf103baa3532ec71675f2a15d4a5a65db3e91
d972_r07_a0_dual_anchored_active_batch_v1_output.checkpoint
173082 bc435660b299f9d72cb2ac10f9765da4ff7f3a16a75242264451c391f20bd358
d972_r07_a0_dual_anchored_active_batch_v1_producer.log
3898 ef366c147651cf011c16e676878a267dd5d85494d949ff02228f43c6004307af
driver.g
125 28802be0e11aad96494eaa266baed0c5b7aa9d85add29bf04a7d7d6db67f67c8
run.log
9493 075f3db302e3f7ee98d826cbe8b67fcbcf9355472b18322ccb29fb78a510af2a
```

The exact contents have also been archived permanently at:

```text
release tag  archive-gha-checkpoints
asset        artifact_9808605601_gap-run-out.rank99.zip
bytes        27959
sha256       d707cf2553fae24863362d581ba4c09709c629a977ff772d95877dd18fdd5f48
URL          https://github.com/tochiazuma0510-alt/shadow-atelier/releases/download/archive-gha-checkpoints/artifact_9808605601_gap-run-out.rank99.zip
```

The result says `UNKNOWN_RESOURCE:tau_free_candidate:time_limit`, not a
negative.  Its sealed durable checkpoint has three closed batches

```text
rank 51 -> 67 -> 83 -> 99
accepted_count 8 -> 24 -> 40 -> 56
round 12
```

and checkpoint inner state seal
`f2de40c3b16053464b8cf7d397f8fd05ca4439a46ca7e45df93e60bbc11a312d`.

## 3. Minimal checker repair

Use the exact accepted Task451 checker as source owner:

```text
crosscheck/check_d972_r07_a0_dual_anchored_active_batch_v1.py
13725 5c2f76b825bd920245d0200f29ff860ba93a32663ef5db9567bc499a86f7ff8a
```

Preserve its artifact schema, dependency pins, frozen rank-51 replay, batch
semantics, resource allowlist, and every mathematical gate.  Make only the
following semantic repair in `replay`:

```text
model,formulas,adj=compiled
```

must use a non-shadowing local such as

```text
model,compiled_formulas,adj=compiled
```

and pass that renamed local to `selector`.  The global function `formulas`
must therefore remain callable at the preceding line.  Version the checker
docstring/marker as recovered v2, but continue to consume the immutable v1
production artifact.  Add a bounded regression assertion which actually
calls the global formula builder through a toy/non-production replay hook, or
an equivalent static bytecode/name-binding gate; a string-presence test alone
is insufficient.

Do not weaken checkpoint-path, outer/inner seal, prefix, scalar, literal row,
exponent, selector, pivot, post-batch dual, profile, or RESOURCE checks.

## 4. Checker-only GHA driver

Require external preamble

```text
D972_R07_A0_DUAL_ANCHORED_ACTIVE_BATCH_RECOVERED_CHECKER_ONLY_V1_RUN:=true;;
```

The driver must exact-pin itself's checker, the release URL/bytes/SHA, and all
six extracted files.  It must run no producer and exactly one checker process.
Use `curl --fail --location` and SHA-256 before unzip.  Extract into a dedicated
subdirectory under `ci/out`; do not overwrite the workflow's current
`ci/out/driver.g` or `ci/out/run.log` with the historical names in the zip.

The immutable v1 result names its checkpoint as
`ci/out/d972_r07_a0_dual_anchored_active_batch_v1_output.checkpoint`.  Satisfy
that without editing the result: create a dedicated checker working directory,
copy only the already hash-checked checkpoint into that working directory's
`ci/out/`, change cwd there, and invoke the checker by an exact repository
path.  Hash-check the copy as well.  Bound the checker process by 6,600 wall
seconds and 4,800,000,000 RSS bytes using the already accepted resource wrapper
ABI; propagate timeout/OOM/nonzero exit through `set -euo pipefail` and require
exactly one recovered-v2 PASS marker.

The produced GHA artifact must retain the downloaded zip, all six extracted
historical files, checker log, and a small receipt binding the production run,
release asset, invoked commit, checker pin, exit code, and PASS marker.

## 5. Bounded local gates

Run only repo-external-cache compile/load/help checks, the repaired checker
self-test/regression gate, ASCII/final-newline checks, and static driver scans:

- no producer command or producer import as main;
- one checker process;
- exact release and six-file pins;
- collision-safe extraction path;
- 6,600-second and 4.8-GB bounds;
- pipefail/nonzero propagation and exact PASS count.

Do not perform the actual semantic replay locally.  Report exact generated
pins and state explicitly that rank 99 remains structurally authenticated but
not cross-checked until the checker-only GHA run passes.
