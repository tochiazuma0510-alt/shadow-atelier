# Luna task 351 - task176 recovery-v2 and A0/v10 exact selected semantics

Role: Luna, bounded provenance repair and implementation only.  Read every
numbered section and every prerequisite first to last.  Do not run Python,
Node, GAP, GHA, a workflow, git, or network.  Read-only PowerShell byte/hash/
schema checks and repository-external temporary canonicalization are allowed.
Use `apply_patch` for every repository file.  Preserve every existing v1--v9
file, especially the sealed but semantically inconsistent recovery-v1 owner.
This task authorizes exactly the six new outputs in Section 2 and no
SELFTEST/PRODUCTION execution.

Task350 correctly returned `BLOCKED / UNEXECUTED`.  Its first stop is a
two-hex-digit transcription error in recovery-v1, not a drift of the accepted
task176 receipt: the physical receipt, reply348, accepted task176 reply, and
verdict all record
`f8f0ce249ff547d3e1235bd4b9760daa2b34b23771bf7da47b48dbd5cbbfae1d`,
whereas recovery-v1 alone says `...b34f...`.  Repair this by a versioned
provenance owner; never overwrite or silently ignore v1.

## 1. Binding prerequisites

Read in full, in order:

1. `sol/luna_task_348_r07_task176_checker_verdict_recovery.md`,
   `sol/luna_reply_348_r07_task176_checker_verdict_recovery.md`, the recovered
   verdict, receipt manifest, receipt, and recovery-v1 manifest;
2. `sol/luna_task_350_r07_task349_a0_v9_selected_section_dag_native.md` and
   all five v9 outputs, including the full blocked reply;
3. updated v287 and v288;
4. tasks342/349 and task347's audit, then v265/v275--v279/v284;
5. every q3/E4/joint/old/task176 physical source pinned by v9.

All task350 requirements survive unless this mail explicitly sharpens them.
No positive, negative, separator, lift, fake, cofinal, or Ihara claim is
authorized.

## 2. Sole permitted outputs

Create only:

- `ci/in/d972_r07_all_seven_extension_section_census_crosscheck_v1.recovery.manifest.v2.json`;
- `search/d972_r07_history_free_positive_fast_resume_v10.py`;
- `crosscheck/check_d972_r07_history_free_positive_fast_resume_v10.py`;
- `search/d972_r07_history_free_positive_fast_resume_gha_driver_v10.g`;
- `search/certs/d972_r07_history_free_positive_fast_resume_selftest_v10_20260829.json`;
- `sol/luna_reply_351_r07_task350_recovery_v2_a0_v10.md`.

Return `IMPLEMENTED / UNEXECUTED` only if recovery-v2 and every literal v10
static path are complete.  Otherwise return `BLOCKED / UNEXECUTED` with the
first exact owner/API.  A fresh Sol(max) full code-and-performance PASS is
still required before execution.

## 3. Versioned recovery-v2 owner

First establish by read-only physical checks:

- receipt: 13,649,089 bytes, physical SHA-256
  `715441d8ecb1b4bb39a51cf3df15f04d6179ee6adeafa5b925485dbbe91f7f41`,
  self digest `f8f0ce249ff547d3e1235bd4b9760daa2b34b23771bf7da47b48dbd5cbbfae1d`;
- recovered verdict: 757 bytes, SHA-256
  `e6a45a34353ce1fb54c99b4f9cbc8b106f34bfc751dd50044f2a79da72cad5e5`,
  self digest `e9d42ea064e7caaa9a333f7e2a8aec42f709bf1565e9fc9a8950ef92e18ce473`;
- recovery-v1: 2,035 bytes, SHA-256
  `41d2cb72614ce7e2d5b2d7a9000e861414da1c749876b3d51f1ccf2ca63390a8`,
  self digest `f8c6c0faf2588cd58d8a2aec75a2a1f9950ea67769dd913fbd796d018098f581`;
- receipt manifest, producer/checker sources, hashes-file identity, accepted
  task176 reply, run/head/artifact/archive/member identities exactly as
  task348/reply348 record them.

Create one canonical one-line JSON v2 manifest with final LF and a self digest
computed by deleting only its top-level `self_digest_sha256` before canonical
serialization.  It must copy every still-correct v1 field, change the schema
suffix to `/v2`, correct only `accepted_receipt.self_digest_sha256`, and add:

```text
supersedes: exact path/bytes/SHA/self-digest of recovery-v1
correction: exact JSON pointer, old value, new value,
            reason="transcription mismatch against physical accepted receipt and reply348"
mathematical_grade_change: false
execution: UNEXECUTED
```

The v2 file is a provenance correction, not a new task176 computation or
acceptance.  Re-read it, reproduce its self digest, and report exact bytes and
physical SHA.  V10 producer/checker/driver pin v2 and explicitly reject using
v1 as the final authority, while still authenticating v1 as the superseded
owner named by v2.

## 4. Exact Q0 selected replay

Retain v9's bounded strict decoding but implement the semantics, not byte
comparison only.

1. Decode the one-based u32 parent and u8 letter entries.  The sole root is
   `(parent,letter)=(0,0)`; every other entry has an earlier nonzero parent and
   letter exactly 1 or 2.  Recover `qword` by reversing the selected walk.
2. Independently decode the two 36-byte Q0 marked permutations from the q3
   owner, evaluate `qword`, and require exact equality with the selected
   36-byte canonical-roster record.
3. Parse task176's ten x/y marked-generator rows, with exact widths 40 for
   coordinates 0--4 and 154 for 5--9.  Starting from the independently built
   typed identities, multiply along `qword` with locally implemented
   E3/E4 operations and require the selected ten section blobs.

The checker must not call task176 source code or any A0 producer helper.
Pinned general low-level E3/E4 group primitives may be used only through an
independently instantiated checker implementation; task176's composite
`enumerate_q0_sections`, `q0_section_word`, coordinate evaluator, fibre, A-map,
and kernel helpers are forbidden.

## 5. Exact Gamma selected replay

`Gamma.record_words` has exactly 26 generator records, not 243 state words.
For a selected one-based `gid`, walk the u16 parent/u8 parent-record owners.
The sole root is `(0,0)`; every other state has an earlier nonzero parent and
record in 1--26.  Reverse the walk, concatenate the indexed record words with
the pinned free reduction, and call the result `gword`.

Evaluate `gword` independently in all ten typed coordinates.  Concatenate
five 40-byte and five 154-byte blobs and require exact equality with the
selected 970-byte task176 Gamma record.  V10 producer provenance exports this
as `gamma_projected_ten_state_hex`.  A full JointGroup state, if retained for
diagnostics, is separately named `gamma_full_state_hex`; the checker never
equates it with or substitutes it for the 970-byte owner.

The selected base word is `red(gword + qword)`, in that order.  Independently
multiply the ten Gamma and Q0 section blobs and compare the resulting source
word, ten-coordinate row, producer provenance, and correction formula.

## 6. Exact K-nonzero schedule

For an authenticated cursor `c`, require

```text
0 <= c < 1,469,664 * 243
qid = c // 243 + 1
gid = c % 243 + 1
```

Apply Sections 4--5 to those exact ids.  Recompute the weighted formula,
`K`, `W`, schedule kind and bound (`W+1` or the typed resource fallback),
ten-coordinate product, formula scalar, direct H1/H2/P column and active-dual
pairing.  A qid/gid range, copied state hex, or cursor arithmetic alone is not
acceptance.

## 7. Exact K-zero one-coordinate fibre

For the selected support target `(j,t)`:

1. stream all 1,469,664 chronological Q0 parent records once, carrying only
   coordinate `j`; retain the one-coordinate typed state needed for parent
   random access and a coarse-key-to-qid inverse; reject duplicate coarse
   keys and compare exact task176 singleton bucket count/digest metadata;
2. reconstruct all 243 Gamma ten-state records and build the first-gid map of
   distinct coordinate-`j` values, independently matching
   `A_families[Sj].literal_elements` rather than importing it;
3. for each distinct Gamma value `a`, compute `a^-1 * t`, look up its unique
   Q0 coarse section, require full typed-blob equality and `a*s_j(q)=t`, and
   prove the claimed `(qid,gid)` is the lexicographically least retained base
   pair;
4. authenticate `word_generators[Sj]`, independently replay every listed
   word, rebuild the full ten-coordinate kernel BFS, require the accepted
   exact order 1, 3, or 9, and bind the claimed `kernel_cursor`; and
5. form `red(kernel_word + gword + qword)`, in that order, replay its ten
   coordinates, selected target, formula scalar, direct column and pairing.

Materialize no other Q0 coordinate inverse.  One selected-coordinate state
array and inverse are allowed and must be byte/RSS/counter-capped before
allocation.  All 243 Gamma states and the at-most-nine kernel states are
bounded.  The producer's fibre list, leastness Boolean, A map, kernel order,
state hex, and heavy digest are never authorities.

## 8. Old-row and heavy identity binding

Bind every selected `o:NNNN` to the physically opened old raw checkpoint
record, not the A0 receipt.  Derive the selected heavy identity from the exact
opened task176 receipt/verdict/manifests/recovery-v2, q3/E4/joint owners,
decoded raw owner hashes, selected coordinate/inverse digest, Gamma roster,
kernel BFS, current dual and cursor.  Compare the producer's correction word,
coefficient-two inverse, eleven occurrences, direct H1/H2/P row, scalar and
final finite sparse equality only after this reconstruction.

Add ordinary-validator physical mutations for recovery-v1 substitution,
recovery-v2 corrected field/self seal, Q0 parent/letter/roster/q3 mark, one
coordinate mark, Gamma parent/record/word/970-byte state, full-vs-projected
Gamma substitution, qid/gid/cursor, K-zero coarse key/full blob/least base,
kernel generator/order/cursor/word, product order, heavy identity and final
row.  No mutation-name branch or miniature substitute is allowed.

## 9. Preserve and re-audit v9 DAG/checkpoint repairs

Retain only repairs supported by literal v10 source.  Recheck that:

- actual rank rises store node ids and never flat expressions;
- checkpoint and restore store solution/remainder node ids and fixed bounded
  canaries, not the complete expanded formal solution;
- restore injects stored chronological normalized rows and node ids into
  rebuilt echelons without recomputing every old actual provenance;
- expansion calls/support, unique DAG nodes, DAG literal-support allocation,
  sparse operations and serialized bytes have separate caps/counters;
- the one output checkpoint sidecar is pre-sized/capped before canonical
  allocation/write and atomically replaced, with no phase-versioned siblings;
- UNKNOWN reads at most that one sidecar and does not load task176 or the
  86 MB raw owner; and
- no unbounded read, duplicate target/dual build, repeated large canon/hash,
  unnecessary worker pass, linear pivot lookup, all-coordinate Q0 index, or
  hidden SELFTEST remains.

Any v9 reply assertion contradicted by source is a v10 blocker.  Do not carry
forward stale `v7` error labels or line references.

## 10. Driver and reply contract

The ASCII driver pins all six v10/recovery outputs and every authority.  It
stages recovery-v2 and its superseded v1 owner, has disjoint SELFTEST/fresh/
authenticated-resume routes, exact timeouts 10,800/7,200 plus 3,600 artifact
reserve inside 21,600 seconds, one output sidecar, atomic receipts/verdict,
and last-write sentinel.  No sleep, retry, polling, nested pool, local run, or
workflow edit.

Report exact bytes/SHA for the five machine outputs, recovery-v2 self digest,
the complete import/process/physical-owner graph, line-numbered static traces
for Sections 3--9, formula counts separately from `UNEXECUTED` measurements,
and the first exact blocker if any.  End exactly with:

```text
RECOVERY-V2:                    COMPLETE or BLOCKED
IMPLEMENTATION:                 IMPLEMENTED or BLOCKED
SELFTEST / PRODUCTION:          UNEXECUTED
FROZEN INPUTS:                  PASS or BLOCKED
FRESH SEARCH ROUTE:             STATICALLY REACHABLE or BLOCKED
AUTHENTICATED RESUME ROUTE:     STATICALLY REACHABLE or BLOCKED
ACTUAL A0 COMMON + CHECKER:     0/1
SEPARATOR / NEGATIVE CLAIM:     FORBIDDEN
LIFT / FAKE / IHARA:            NONE
```

`TASK351_R07_TASK350_RECOVERY_V2_A0_V10`
