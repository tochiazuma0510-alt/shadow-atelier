# Luna reply 174: target6 context-image census v1 (task174c repair)

Date: 2026-08-27

## 1. Disposition

The three task174c STOP gates are repaired in the five authorized task174
files.  This was static implementation only: no Python, GAP, Node, git, or GHA
command was run.  Therefore no selftest, census, or independent-checker PASS
is claimed, and no numerical census result is promoted.

`GHA dispatched=false`.

## 2. Final files

```text
bytes  SHA-256                                                           path
57948  c7307c0ed21a4cee0798256fefc3f6b0044b1618d76bc76369ccf7e78c4bbaea  search/d972_r07_target6_context_image_census_v1.py
85390  821a8ee9369c5d879285b4a5e17ac16051d7a1b1e648709d5e6575059970be0b  crosscheck/check_d972_r07_target6_context_image_census_v1.py
24666  0d62e6cb7637d8108aaef3a8fa5d8a922b2899bede7e7528f6a6cbf96d2c0fb2  search/d972_r07_target6_context_image_census_gha_driver_v1.g
 5971  f96115087a4ddeb26552d7be9caadfda62bfcacc2972b1258d0859df567e4c7d  search/certs/d972_r07_target6_context_image_census_preflight_v1_20260827.json
```

The canonical one-line ASCII fixture has internal self-digest
`af1832d86981c16e24cb95d03852e808352198bc15d7cea705a0e16fa28e25d8`.
A read-only PowerShell/.NET calculation removed exactly the canonical
`self_digest_sha256` member and reproduced that digest.  Its source record is
the exact producer pin above.  This was a text/hash audit, not producer
execution.

## 3. Repair A: terminal-typed cap gates

The old `D174ReceiptAudit` globally required exactly one
`state_cap=2000000` and one `soft_deadline_seconds=9000`.  An honest
COMPLETE or UNKNOWN_RESOURCE receipt has those values in both
`registered_caps` and `resource`, so the old gate rejected it.

The driver now binds the complete canonical `registered_caps` object as one
typed path and separately binds the terminal's resource path:

- COMPLETE requires each scalar exactly twice, the registered object exactly
  once, the closing resource-cap suffix exactly once, and the typed
  `phase=complete/reason=null` suffix exactly once.
- UNKNOWN_RESOURCE requires the same registered/resource multiplicities and
  the replayable-prefix flag.
- INPUT_STOP requires each scalar exactly once, no resource-cap suffix,
  `resource:null` exactly once, and byte equality with the immutable fixture.

COMPLETE and UNKNOWN_RESOURCE also have exact top-level
`status,terminal` anchors.  The exactly-one allowed-terminal gate, receipt /
verdict agreement, mode and Python-binding gates, source pins, claim
boundaries, timing ledger, hash ledger, process markers, and final sentinel
remain fail-closed.

## 4. Repair B: production validator selftests

The checker now has one `validate_receipt_chain` used by runtime and
selftest.  It always enters `validate_envelope` and then exactly one of
`validate_complete`, `validate_resource`, or `validate_input`.  The old
standalone `validate_toy_snapshot` validator is gone.

The bounded fixture writer emits the real receipt schema and real packed
formats: 154-byte E4 coordinates, 462-byte triple states, discovery rows,
parents, actual parent letters, four signed transitions, all coordinate and
pair image/kernel rows, and 30-byte Delta3 rows.  Its finite construction is a
nonabelian linked `H_27 x C_2`, with code-level expected coordinate image
orders `54,27,2`, coordinate kernel orders `1,2,27`, three pair image
orders `54,54,54`, and quotient `H_27` of order 27.  These are fixture
construction assertions and were not executed in this commission.

The implemented bounded baselines all use the production chain:

1. COMPLETE with cap 64;
2. honest cap-before-novel UNKNOWN_RESOURCE with cap 8 and nonempty pending
   frontier;
3. the exact immutable INPUT_STOP fixture (the task's input-unknown lane).

Twenty resealed mutations also use that chain: generator order; one marked
triple coordinate; one packed state byte; one signed transition; one parent
letter; all three coordinate IDs; all three pair IDs; one kernel bitset; one
Delta3 row; one state count; the UNKNOWN_RESOURCE pending-frontier digest; and
five forbidden result terminals.  Packed-byte mutations are recompressed and
rehash-bound before validation, so they cannot be rejected merely for stale
compression metadata.

The driver expects exactly one checker selftest marker,
`"mutation_count":20`, and the new fixture marker
`"linked_image_order":54`.  These are unexecuted marker gates, not results.

## 5. Repair C: cursor-bound pending frontier

Producer enumeration receipts now separately bind:

- discovery prefix count and discovery-order digest;
- seen-state count and canonical sorted-set digest;
- the exact positive pending frontier at the cursor.

The frontier hash domain is
`D174-PENDING-POSITIVE-FRONTIER-V1`.  Its hash input is the canonical cursor
and positive-generator-order header followed deterministically by

```text
<u32 state_id, u8 generator_index, u8 letter, 462-byte literal state key>
```

for every unprocessed positive-generator task.  The receipt carries the
definition, domain, cursor, positive order, record width, task count, and
SHA-256.  COMPLETE binds the empty closed frontier; UNKNOWN_RESOURCE binds
the exact remaining work.

The checker has a separately written reconstruction routine and compares the
entire frontier object while also replaying the prefix, parent table, and
typed cap/deadline cursor.  Its dedicated frontier mutation starts from the
nonempty UNKNOWN_RESOURCE fixture and enters `validate_resource`.

## 6. Dependency and static audit

The existing 25 predecessor pins were retained.  Static PowerShell parsing
found 25 rows in the producer and 25 in the checker, with zero literal
differences.  All 25 current files matched their registered bytes/SHA-256.
A separate parse found the same 25 predecessor triples in the GAP driver,
again with zero differences.

The mutable task169 implementation is not imported or pinned.  The producer's
only `task169` string is the comment explicitly stating its absence.
The frozen lineage remains task157ee/q3 E4 arithmetic and receipt, task168
core/Delta3, and task172-v7.  The task174 and task174b pins remain:

```text
6765  b0ed2024d0dddb99e6a9407eca4ca732dc8f5791052d6a01b09c0b7126375ec4  sol/luna_task_174_r07_target6_context_image_census_v1.md
6294  0a17d240740e403706ffe234778dbd0eb1bb9ab78a0e588e4173943ebf8bb7d7  sol/luna_task_174b_r07_target6_context_image_census_repair.md
```

Final read-only scans found:

- LF endings and zero non-ASCII bytes in producer, checker, driver, and
  fixture; the `.g` file is ASCII-only;
- no `PLACEHOLDER`, `TODO`, `TBD`, or `INSERT_SHA` token in those four
  runtime files;
- one literal driver token for each allowed terminal;
- two driver references to the pending-frontier domain, for COMPLETE and
  UNKNOWN_RESOURCE;
- one checker definition each of `validate_complete`,
  `validate_resource`, and `validate_input`, all reached through
  `validate_receipt_chain`;
- final producer, fixture, checker, and driver pin values mutually agree.

These were static reads, hashes, and schema scans.  Python syntax, GAP parse,
selftests, and mathematical execution remain unrun by explicit instruction.

## 7. Exact dispatch inputs (not run)

Bounded serial selftest:

```gap
D972_R07_TARGET6_CONTEXT_IMAGE_CENSUS_V1_SELFTEST:=true;;
D972_R07_TARGET6_CONTEXT_IMAGE_CENSUS_V1_USE_PYTHON3:=true;;
Read("search/d972_r07_target6_context_image_census_gha_driver_v1.g");
```

Full GHA lane, only after the bounded selftest succeeds:

```gap
D972_R07_TARGET6_CONTEXT_IMAGE_CENSUS_V1_RUN:=true;;
D972_R07_TARGET6_CONTEXT_IMAGE_CENSUS_V1_USE_PYTHON3:=true;;
Read("search/d972_r07_target6_context_image_census_gha_driver_v1.g");
```

The exact mathematical commands assembled by the driver are:

```text
python3 -u -B search/d972_r07_target6_context_image_census_v1.py --run-census --output ci/out/d972_r07_target6_context_image_census_v1.json
python3 -u -B crosscheck/check_d972_r07_target6_context_image_census_v1.py --receipt ci/out/d972_r07_target6_context_image_census_v1.json --verdict ci/out/d972_r07_target6_context_image_census_crosscheck_v1.json
```

They are strictly serial: producer first, checker only after an exit-zero
producer receipt.  Each outer timeout is 10,200 s; the soft deadline is
9,000 s; the total workflow envelope is 21,600 s; the required upload margin
is 1,200 s.  No subprocess concurrency was added.

UNKNOWN_RESOURCE remains UNKNOWN and can receive only a bounded-prefix grade.
INPUT_STOP remains input-only.  COMPLETE becomes cross-checked only if the
independent checker actually succeeds.

simultaneous context image census only

linked Delta_E is not replaced by E4^3

complete fibres enable but do not execute v118 correlation

no target6 solution / cofinal lift / fake / Ihara witness declared

R07_TARGET6_CONTEXT_IMAGE_CENSUS_V1_STATIC_REPAIRED_UNEXECUTED

## 8. Parent static audit and GHA selftest dispatch

The parent Sol session and an independent read-only Luna re-audit both
accepted the repaired static bundle.  The parent separately recomputed all
five deliverable identities and all 25 literal predecessor pins; no drift was
found.  This is still only a static acceptance, not a selftest or census
result.

The parent committed and pushed the exact five task-174 files, then dispatched
only the bounded selftest lane:

```text
GHA run id:       33031593759
workflow:         gap-run.yml
branch:           sol/r07-explicit-lift-20260825
commit SHA:       eec4db7cbac28e6727d56e0e4bf49356a02e7cc6
script:           search/d972_r07_target6_context_image_census_gha_driver_v1.g
preamble:         D972_R07_TARGET6_CONTEXT_IMAGE_CENSUS_V1_SELFTEST:=true;; D972_R07_TARGET6_CONTEXT_IMAGE_CENSUS_V1_USE_PYTHON3:=true;;
optional packages: false
dispatch status:  in_progress
```

The full census has not been dispatched.  It remains gated on this selftest
returning the exact producer/checker/driver PASS markers.

## 9. Parent GHA execution update

The bounded selftest completed successfully:

```text
selftest run id:  33031593759
commit SHA:       eec4db7cbac28e6727d56e0e4bf49356a02e7cc6
conclusion:       success
driver terminal:  R07_TARGET6_CONTEXT_IMAGE_CENSUS_V1_GHA_DRIVER_PASS
mode:             selftest
```

This executes only the bounded producer fixture, the checker production
validator chain, its 20 registered destructive controls, and the driver
gates.  It does not execute the target6 census.

After that success, the parent dispatched the serial full census:

```text
full run id:      33031673980
workflow:         gap-run.yml
branch:           sol/r07-explicit-lift-20260825
commit SHA:       1892452db0a35096e5b037ed5aafb869d2306ed0
script:           search/d972_r07_target6_context_image_census_gha_driver_v1.g
preamble:         D972_R07_TARGET6_CONTEXT_IMAGE_CENSUS_V1_RUN:=true;; D972_R07_TARGET6_CONTEXT_IMAGE_CENSUS_V1_USE_PYTHON3:=true;;
optional packages: false
dispatch status:  in_progress
```

No order, projection, target6 solution, lift, fake, or Ihara claim is made
while that run is in progress.  A resource terminal will remain a bounded
UNKNOWN rather than being promoted to an order statement.

## 10. Full-run terminal and exact bounded result

Full run `33031673980` completed successfully at the workflow/driver level
and returned the typed resource terminal

```text
R07_TARGET6_CONTEXT_IMAGE_CENSUS_UNKNOWN_RESOURCE
grade = CROSS_CHECKED_BOUNDED_PREFIX_UNKNOWN
resource reason = state_cap
```

The producer stopped before inserting the next novel state at the registered
2,000,000-state cap.  The helper-nonshared checker independently replayed the
exact bounded prefix, including the next attempted novel state and the
cursor-bound pending-frontier digest.  The authenticated bounded fields are:

```text
seen_state_count       2,000,000
cursor.state_id        1,171,439
cursor.generator_index 1
next_positive_letter   2
frontier_count         828,561
pending_task_count     1,657,121
producer elapsed       101 seconds
checker elapsed        88 seconds
```

The exact executed artifacts are:

```text
83048714  329b583175cf3e35fdc52f424f9f1d0efbb9adde6cf35247b8d93a3c1d4c5668  d972_r07_target6_context_image_census_v1.json
     845  3332ff2ce5ab036e4216490deb7c89530198a3c0a61bbcee33fd9cfc003b2275  d972_r07_target6_context_image_census_crosscheck_v1.json
     314  03052ed637e71b305aca31dc6931779c1f998a2817fb07aa5c34f38b513d9127  d972_r07_target6_context_image_census_timing_v1.txt
```

Because the checker also confirms that the cap-triggering attempted state is
not among the two million retained literal keys, this receipt gives the
cross-checked lower bound

```text
|Delta_E| >= 2,000,001
6441*|Delta_E| >= 12,882,006,441
```

It gives no exact order and no coordinate/pair projection census.  In
particular, direct `6441*|Delta_E|` streaming is now ruled out as the next
reasonable route for this pinned context.  The extension-section / support-
fibre reduction of v120/v125 is the appropriate successor; merely increasing
the BFS cap is not promoted.

No target6 solution, all-seven solution, correction, cofinal lift, fake, or
Ihara witness follows from this bounded-prefix result.

R07_TARGET6_CONTEXT_IMAGE_CENSUS_V1_CROSS_CHECKED_BOUNDED_PREFIX_UNKNOWN
