# Luna task 175b: all-seven raw bridge implementation repair

Date: 2026-08-27
Role: Luna / static code repair only

## 1. STOP ruling

Task175 v1 is not dispatchable.  Its producer `run_preflight()` raises
`UNKNOWN_RESOURCE:runtime` unconditionally, the checker validates only a
contract-shaped static receipt, and the driver contains no executable
producer/checker run.  A list of intended checks is not an implementation.

Read task175 and all five v1 deliverables completely.  Implement the full
bounded reconstruction specified in task175 Sections 1--8.  Do not execute
Python, GAP, Node, git, or GHA locally.

## 2. Authorized files

Edit only the five existing, uncommitted task175 files:

```text
search/d972_r07_all_seven_raw_bridge_preflight_v1.py
crosscheck/check_d972_r07_all_seven_raw_bridge_preflight_v1.py
search/d972_r07_all_seven_raw_bridge_preflight_gha_driver_v1.g
search/certs/d972_r07_all_seven_raw_bridge_preflight_v1_20260827.json
sol/luna_reply_175_r07_all_seven_raw_bridge_preflight_v1.md
```

## 3. Producer must actually reconstruct

Replace the unconditional STOP path by a bounded executable preflight which
performs every task175 operation.  In particular it must:

1. authenticate all frozen inputs by exact bytes/SHA;
2. freshly reconstruct E3/E4 arithmetic and the v122 coarse/fine deletion
   and insertion maps, including all pc-generator and mark replays;
3. reconstruct and losslessly retain all 6,441 actual signed F2 relation
   words, not just their counts/token templates;
4. select the deterministic first nonempty row and directly prove its joint
   identity before using it as the canary correction;
5. reconstruct g760 and one corrected word, then evaluate literal H1, H2,
   five pentagon factors, the ordered product and all intermediate products;
6. compute all three direct changes and all three independent literal
   prefix/Fox changes, requiring exact equality;
7. construct the tagged sparse H1/H2/P target without cross-block merging;
8. construct and check the actual two PB3 and eleven PB4 D2 columns; and
9. run at least 110 actual conjugation canaries plus the same-context and
   actual-product additivity canaries.

Do not import mutable task169.  Use the frozen task172-v7 and task157ee/q3
sources and receipts.  Importing a predecessor API is allowed only after its
source is pinned and every load-bearing value is replayed here; public
booleans are not evidence.

The positive receipt must serialize actual rows, blobs, digests, counts,
maps, formula results, D1/D2 transcripts, canary provenance and mutation
results.  It may compact the 6,441 words losslessly, but a contract string or
count is insufficient.  Every partial exception maps to the specific
fail-closed terminal from task175; no READY token may survive an exception.

The checked-in static receipt remains an immutable
`UNKNOWN_RESOURCE:LOCAL_EXECUTION_GUARD` fixture.  Add `--output` so GHA writes
the executed receipt under `ci/out`; never overwrite the fixture.

## 4. Checker must independently recompute

The checker must have `--check --receipt --output` and a cheap fixture mode.
For a READY receipt it must independently reconstruct all objects listed in
task175 Section 6, without importing the producer or any producer helper.
It must decode/rebuild the complete roster, rerun all direct products and
Fox rows, reproduce all 110+ canaries, and compare every serialized digest
and transcript.

Implement every required destructive control as a real mutation passed
through the same full validator.  Merely listing mutation names, checking a
digest, or checking counts is a STOP.  Record exact attempted/rejected counts
and require equality.  The fixture mode may use small genuine groups/words,
but it must exercise the production algorithms.

For the static guard receipt, report only fixture/static consistency.  Never
label it cross-checked raw input.

## 5. Executable GHA driver

Replace the dormant contract with actual GAP `Exec` paths for:

- a cheap source/fixture selftest which does not run the 6,441-row replay;
- a production-preflight mode which runs exactly one producer and then one
  checker, serially, under one fail-closed timeout and `pipefail`.

The production mode must reject pre-existing driver-owned `ci/out` files,
pin producer/checker/static fixture and all high-value inputs by exact bytes
and SHA, require exact-one markers and exact-one terminal, parse/gate the
READY receipt and checker verdict, preserve complete logs on failure, write
hash/timing/sentinel files, and state the generic `gap-run.yml` variable
preamble.  No `0` byte wildcard, placeholder, or merely constructed shell
string may remain.

## 6. Report boundary

Update the reply after static finalization.  State plainly that no replay or
mutation has yet run and all values are UNKNOWN until GHA.  Report exact
source hashes, driver flags, estimated time/RSS and `GHA dispatched=false`.
Only use `R07_ALL_SEVEN_RAW_BRIDGE_PREFLIGHT_V1_STATIC_READY` when the
production path is actually present and all pins are final; otherwise retain
STOP.  Do not promote any correction, lift, fake, or Ihara claim.
