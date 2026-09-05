# Task938 -- rank1355 root-seed checker and workflow handoff

## F1. Static implementation complete; execution reserved to root

Implemented the Task937/938 scope after reading full Task936/reply936 and
Task937. The new checker and workflow are frozen below. No local Python,
GAP, numerical run, network, credential, git, or GHA dispatch was performed.
Synthetic tests and the actual producer/checker comparison remain unrun.
No new root/scalar result is claimed in this handoff.

Only these authorized Task938 files were edited:

- search/check_d972_r07_rank1355_root_seed_scalars_v1.py
- .github/workflows/d972-r07-rank1355-root-seed-scalars-v1.yml
- this reply

No known static execution blocker remains. Root retains the short
actual-path review, source commit, single dispatch, and run/commit record.

## F2. Frozen sources

| File | Bytes | SHA256 |
|---|---:|---|
| search/check_d972_r07_rank1355_root_seed_scalars_v1.py | 36236 | f3c7ca2586a3734334b7d9823316601d18ab1d36561c72aa2c23c2aedfca0e62 |
| .github/workflows/d972-r07-rank1355-root-seed-scalars-v1.yml | 19792 | 6c099182ac39fbef556529f14f804f33e54ed783a1b0b068f8d3b7a04e01f1fc |

The workflow pins the sibling's producer
search/d972_r07_rank1355_root_seed_scalars_v1.py to 31578 bytes/SHA256
973ccd1d5d0f8fa5a28294589ff655620745f0cc988c09abe8a6178593e185bb.
These byte counts/digests were read with Get-Item/Get-FileHash, not a
numerical execution. LF/BOM and Python syntax gates are wired for GHA.

The checker hashes its accepted checker-v2 and checker-v15 dependencies
before importing checker-v2. It does not import or execute the new producer
or its arithmetic. Its dependencies remain:

- check_d972_r07_actual_grade2_root_scalar_batch_v2.py:
  e0237d100c7fd3e8826ce6ab8896fa8aecf6c7e04da23a603a3d9305ea9eebb6
- check_d972_r07_targeted_grade2_owner_generated_join_v15.py:
  8f718811c518f8d3e1d09de497b955d18c221e983391721068cc35be0000a662

The launch discloses both accepted producer/checker lineages; the workflow
authenticates all six new/dependency source files. Independence is qualified
by those disclosed accepted lineages, not claimed as a third actor engine.

## F3. Actual checker path and output contract

The fixed new parent is run33946247365/1, artifact9963533999,
head7f6dfaddf4150449e62a9b3e85def472fcb41c01, archive915410 bytes,
sha256:f9627416f0e920fa369f6bc6bb9bffa8c6b15674c0fb7ff37bbebaf77991ace6.
The delta manifest/result/instruction/checker/source receipt are each
size/SHA-pinned, joined and authenticated. The manifest authenticates all
delta payloads and its exact output roster. It binds the executed seed30
materializer/checker v1 sources, not the unused buffered v2 successor.

The old small state receipts are pinned, then old physical.bin is streamed
once with the new lambda. The checker requires all 1354 old row dots and
the new normalized-pivot dot to vanish, and the new saved target-remainder
dot to equal 1. Old state, delta and rho2 derivations remain premises; no
old instruction/Conn history replay, target solve, rho2 staging or state
copy is performed.

All four fresh q_a=B_a^*lambda are reconstructed using the accepted checker
B-table/adjoint lineage. Every RawDual explicitly binds generation8060,
rank1355 authority, new head
36feb776736c6587ce9f64d6f5acb883385074a7cc2eed4c2ce7eb8675e71342
and lambda SHA
f83bbaa503b8a4d5056f0779085ee4eced542eb1d78d3e35fa9df1c281960565.
No old root assertion, old-head fallback or old contracted value is used.

One buffered P1 cache pass computes four fresh 8059-entry uint8 vectors;
instruction bytes are hashed in one buffered pass, not replayed. Direct
raw seed evaluations call the accepted checker with actual_pin=False.
The 4x44 accumulator subtracts the complete global P1 seed relation:
all four prepare seed expressions and all four source seed origins in
each new target block. The five pinned Task554 bodies are loaded serially
and each full body and last expression are released before the next load.
The checker contracts each stored expression vectorially; the producer's
new per-term arithmetic is not reused. Per-seed event chains bind stored
term order, multiplicity, source/target character and local/global index.
No actor-origin/lower-dot or orbit arithmetic is called.

The independently reconstructed flat candidate has exactly 20 files:
launch.json, result.json, scalars.jsonl, manifest.json, and for each a=0..3,
q-aA-root.bin, p1-values-aA.bin, direct-seeds-aA.bin, seed-scalars-aA.bin
(replace A by a). Character receipts are embedded in result.json. Every
file's exact bytes, all nested receipts, full manifest/roster and the entire
176-record character-major stream are compared with the independently
computed expectation. Candidate self-seals never serve as arithmetic
authority.

The terminal is ROOT_SEED_VIOLATION with the first nonzero's complete
provenance, or ROOT_SEEDS_ZERO for exactly this 176-root-seed scope.
The latter is not full-grade EOF or nonexistence. Both paths retain
actor_origins_executed=0, orbit_rows_executed=0 and
materialization_performed=false. A selected next seed still needs its
separately authorized materialization. The legacy formula identifier
contains "actor-lower-adjoint", but this adapter executes only v541's raw
seed-minus-complete-P1 seed clauses, not that identifier's actor clauses.

## F4. Exact CLI and workflow

Common fixed-parent arguments, with block roots ordered 0,1,2,3:

```text
--delta-root NEW_DELTA --state-root TASK904 --prepare-root PREPARE
--block-root B0 --block-root B1 --block-root B2 --block-root B3
--p1-root P1 --task712-root TASK712
```

Producer: python -B -u search/d972_r07_rank1355_root_seed_scalars_v1.py
with those arguments and --output-root FRESH_OUTPUT.

Checker: python -B -u search/check_d972_r07_rank1355_root_seed_scalars_v1.py
with those arguments and --candidate-root FRESH_OUTPUT.

The workflow authenticates the unchanged exact P1, five Task554, Task712
and old physical-separator tuples plus the one new delta tuple; it then
downloads those nine artifacts and resolves roots without parent copies.
No old scalar/diagnostics or rho2 download and no seed30 v2 rerun remain.

Execution order is serial: source pins/syntax, producer --selftest,
checker --selftest, actual producer, actual checker. The checker has five
bounded synthetic canaries: dynamic four-root projections, coherently
resealed stale-head rejection, stored duplicate terms/global offset,
176-seed ordering/first hit, and ROOT_SEEDS_ZERO-only scope. They have not
been executed locally. Actual phases/counts flush to visible stderr and
bounded diagnostics; both numerical steps have a 40-minute cap and the
job has a 90-minute cap.

Candidate upload requires checker PASS and is named
d972-r07-rank1355-root-seed-scalars-v1-candidate-RUN-ATTEMPT.
Diagnostics upload uses if:always() and retains source/parent API receipts,
selftests, progress/error logs, summaries and any bounded candidate output,
but never the large parent state/cache copies. workflow_dispatch is
available; the work-branch push marker is
[r07-rank1355-root-seed-scalars-v1-run]. Root alone may dispatch.

No A0, grade2 membership/nonmembership, COMMON, COFINAL, FAKE or IHARA claim
is authorized. verified=false and cross_checked=false throughout. No
new run ID or commit SHA exists from this worker; root records those after
its authorized launch.
