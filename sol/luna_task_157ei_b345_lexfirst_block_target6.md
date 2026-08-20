# Luna task 157ei — lex-first full relator block and target-6 column generation

## 0. Role, authorized files, and non-goals

Implement one versioned, positive-information column-generation step after the
cross-checked 157eh ACTIVE result.  Luna may create or edit only these four
files:

1. `search/d972_b345_lexfirst_block_target6_v1.py`
2. `search/check_d972_b345_lexfirst_block_target6_v1.py`
3. `search/d972_b345_lexfirst_block_target6_gha_driver_v1.g`
4. `sol/luna_reply_157ei_b345_lexfirst_block_target6.md`

Do not edit the frozen q3, 157ec, 157eg, or 157eh bundles, workflows, claims
ledger, dialogue book, or any other worktree file.  Temporary selftest output
belongs outside the repository.  Do not run a full production scan, GAP, GHA,
or Git; the parent session owns those actions.  A bounded combined selftest is
required before the final static freeze.

This task adds exactly one E4 translation block and asks exactly one affine
question, target 6.  It does **not** add every old ACTIVE row, iterate column
generation, scan targets 7--33, produce a typed GT lift, exhaust the full D2
image, exhaust H3 corrections or roofs, or prove B4-A/B.

Use schema `d972-b345-lexfirst-block-target6/v1` and output
`ci/out/d972_b345_lexfirst_block_target6_v1.json`.

## A. Frozen inputs and authenticated evidence

Hard-authenticate paths, byte lengths where listed, and SHA-256 values before
mathematical work.  Missing or drifting external inputs are UNKNOWN_INPUT;
internal theorem, orientation, helper-shape, or arithmetic drift is a hard
failure, never UNKNOWN_INPUT.

### A.1 q3 roof

```text
search/d972_b345_q3_chief_v1.g
  b95fc29b326c3d6a378249cdeb03595eed8d0211a7fe0358fc02447d70d5f755
search/check_d972_b345_q3_chief_v1.py
  ddb52ddae18327209692f0f6eb8b4f65cbdd446155be660a621de24274cc3f73
search/d972_b345_q3_gha_driver_v1.g
  c397cd837ff6814f7b7a8ca0604c6aed54fa0bc85bb577516ea1c6e7df83a831
ci/out/d972_b345_q3_chief_v1.json
  3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72
```

The driver must generate and independently check this q3 artifact in the same
job.  Do not trust an unpinned pre-existing output.

### A.2 frozen 157ec affine theorem and 108-seed universe

```text
search/d972_b345_seedspan_triple4_v1.py
  fe18fc31fdf3f9416ebb829112ccbd514c27e6a8d30fe24691842865277a0b29 / 535219
search/check_d972_b345_seedspan_triple4_v1.py
  ef5125e3b7e328ce8aa8cfd4c36d0937e28f44a480188fcd4ed01a37eb80b981 / 574347
search/d972_b345_seedspan_triple4_gha_driver_v1.g
  a9c88540c1abdb21dc214d4d4e6461c1431dc407f93542c49e0e65a14788fca4 / 9041
sol/luna_task_157ec_b345_seedspan_triple4.md
  1173f2f8ce6ad899fe5bee6c2a42d7cb6686073306a7e3fd1e17acf0007f89b2 / 14751
```

Cross-checked run `32326652060` produced artifact SHA-256
`d556a3e579390ae09ea005d1de94b0d2f88b5ed5f9c5d230034b316afe45fc8d`.
It found target-6 rank 54/nullity 54 and an inconsistency against the old
prefix.  This is evidence and a stable comparison gate, not a remainder or
dual that may be imported into the new calculation.

The ordered variables remain exactly the old 104 seeds followed by the four
preregistered triple-cube seeds
`(3,10,19),(10,10,11),(10,12,12),(19,19,21)`.  Bind the complete 108-word
manifest, all exact word/quotient/context digests, and the old result's
target-6 raw-gradient ledger.  Rebuild raw gradients in this task; do not reuse
the old 33687-coordinate remainder, its row echelon state, or its dual.

### A.3 frozen 157eh ACTIVE result

```text
search/d972_b345_full_d2_dual_correlation_v2.py
  6557bcfea70c0846158951fafe3d6ef8790479a5c7010db896ed76540dd5ae5f / 42449
search/check_d972_b345_full_d2_dual_correlation_v2.py
  881719f18b302afcb5ee25fd22e36ef7d6b50ee38a3562f208a2adb2a6e74060 / 21933
search/d972_b345_full_d2_dual_correlation_gha_driver_v2.g
  5b76b267a36526f4f2d9e325b4b92e36c7b241f6f9d75abec7e08c3c9ff74cde / 13253
sol/luna_task_157eh_b345_full_d2_monitor_scope_repair.md
  5d8da27e3997b261c004bb2fb4a40e9416bed39536816ab2fca9f3a9935c095e / 15015
```

Cross-checked run `32374248796`, exact head
`9e1da3ca55133ae17fe6349bf64e7695fdda14f6`, produced receipt SHA-256
`7c9de4d4aa5dc0facf94cec9c4b2b71d81c1b8cc590e84aa574cace18c1cb7d5`.
The independently checked stable facts are:

```text
old prefix columns/pivots/dependent       362725 / 362709 / 16
old prefix BFS/directed blocks             32768 / 207
old prefix live sparse entries                  3090367
old pool checkpoint                              976408
base-column occurrence count                           76
base occurrence SHA  3eacd6dc77d62c1799a55923d3c8d5313a37ceab8e78b58b07b45925a28f131d
lambda support                                  78 = [43,9,11,15,0,0]
correlation attempts/candidates/cancel/active   886 / 724 / 156 / 568
active scalar distribution                         1:284, 2:284
active packed SHA     8f69ef922a646c0306f2c9ebcf0c8f03531c84b057e29ad4e580a508911c6551
first active relator/scalar                           9 / 1
first-active t-word length/SHA  24 / 04813137f271cba21b5fdab6b733f0a0ac8ca9daa6b23323e5de55d2b7edba36
g-word length/SHA               22 / 5e1880d33973be6d67c31110827daf4db55cddf533c4e88354e0c26fbb74a448
section expression manifest SHA aae5341e2f0586069548360b7441d7ebd4fc9550dd752171a8f59ffa3804b073
first-active translation blob
  0001030608070402050d0a0b0e1011090c0f16131417191a1215181b1c1d1e1f2021222328272625242c2b2a293534333231302f2e2d3c3d3e363738393a3b41403f4746454443424d4c4b4a4948504f4e5951525354555657585b5c5d5e5f6061625a6867666564636b6a696c74737271706f6e6d75767778797a7b7c7d7e7f808182838485868788898a8b8c8d8e8f00000200000000000000
```

Independently reconstruct the exact first-active translation and its canonical
contributing-pair fields; do not depend on access to the old temporary
artifact.  Do not compare a truncated display string.  Require the exact
154-byte blob above,
`t=g*h^-1`, left action `L_t e_(c,h)=e_(c,t*h)`, relator 9, scalar 1, exact
section word, and complete correlation digest above.

Run IDs, elapsed time, RSS, job IDs, local paths, object identities, cache
counters, and log timestamps are provenance-only.  They must not enter a
stable mathematical digest.  Stable projections may remove only an exact
named volatile-field set; never recursively discard arbitrary fields.

## B. Load-bearing one-block theorem

Let

```text
C1 = F3[E4]^6,
B0 = span of the frozen 362725 prefix columns,
c_j = L_t D2_j  (1 <= j <= 11),
B1 = B0 + span{c_1,...,c_11},
```

where `t` is the canonical lexicographically first ACTIVE translation from
157eh.  The old functional `q*` satisfies

```text
q*(B0)=0,  q*(c_9)=1.
```

Therefore `c_9` is not in `B0` and

```text
1 <= dim(B1/B0) <= 11.
```

This is the exact progress theorem.  Add the complete block in relator order
`1,2,...,11`.  In that order an earlier column may make relator 9 dependent;
do **not** require relator 9 itself to be the inserted pivot.  Require only the
cumulative rank gain to lie in `1..11`, together with the direct pre-insertion
gate `q*(c_9)=1`.

Adding all 568 old ACTIVE `(t,j)` rows is forbidden in v1.  They are active for
the old dual only, do not exhaust full D2, and would require a new all-section
oracle.  If the one-block system remains inconsistent, the correct next
column-generation step is to correlate the **new** dual, not to bulk-add every
column selected by the obsolete dual.

## C. Production algorithm and exact order

### C.1 Rebuild and pre-mutation gates

1. Authenticate all inputs and rebuild E3/E4 and the exact 108-seed manifest.
2. Run the same typed source/context preflight as 157ec.  The five charming
   source identities and every target-6 direct-vs-typed Fox formula are hard
   gates.  The source universe and candidate order must not change.
3. Fresh-rebuild the frozen prefix in the exact old order.  Require every
   stable count/digest in A.3.  No old pool, basis, DAG, section table, normal
   form, or receipt object may be imported.
4. Before any persistent mutation, reconstruct the old reverse-pivot `q*`, all
   11 base columns, and the complete 886-pair correlation.  Require the full
   stable result from A.3, not merely the first row.  Snapshot and require
   pool/basis/DAG/section semantic neutrality across this correlation.
5. Independently recover and direct-evaluate the exact typed PRODUCT/INVERSE
   section for `g` and `t`; never call the inherited broken `inverse_word`
   materializer.  The public binding is by canonical blobs and word/SLP
   digests, never transient pool IDs.

### C.2 Persistent complete block

After the old-correlation snapshot is closed, intern or look up `t` and bind
its exact section in the persistent section oracle.  `t` may already occur in
the element pool without having a registered translation section, so do not
assert that the pool grows by one.  If a section is already registered, require
exact canonical value and word equality.  Public/checker equality never uses
the resulting ID.

Set translation ordinal 32976 and add exactly the 11 translated relator
columns in ascending relator order.  Use the actual frozen packed-basis API and
the same left action as the correlation.  For every raw translated column:

- recompute it term by term from the unshifted base column;
- require exact canonical sparse equality with direct left translation;
- require quotient identity and `D1*D2=0`;
- record a canonical semantic digest ordered by relator, component, and exact
  154-byte E4 blob;
- record dependent/independent outcome and, for an independent row, the
  canonical pivot label and reduced-row digest, but no pool or DAG ID.

Normal completion must have

```text
post columns       = 362736
post pivots        = 362709 + rank_gain
post dependent     = 16 + (11-rank_gain)
1 <= rank_gain <= 11.
```

The rank gain is recomputed from pre/post basis rank and independently from the
11 raw columns modulo B0.  A digest alone is never equality.  Preserve the
post-block pool, section, basis, and DAG as the immutable anchor for every
target remainder transaction.  Candidate rollback snapshots must be taken
**after** this anchor and must explicitly retain `t`, its section, all 11
columns, and all new pivots.

If a registered resource stop occurs during this persistent block, emit an
atomic RESOURCE terminal with exact attempted/completed relator prefix,
rank-gain-so-far, and pre/post counts.  Do not continue target work and do not
pretend that a candidate-transaction rollback can undo persistent basis rows.
No mathematical terminal may be promoted from a partial block.

### C.3 Fresh target-6 affine system

The sole target is ordinal 6, `hexagon_1_coface_0`.  Recompute from raw C1:

```text
z       = target-6 Fox gradient of the base candidate f0,
delta_i = target-6 gradient(f0 * seed_i) - z,  1 <= i <= 108.
```

Use the frozen 157ec noncommutative target-6 formula and independently compare
it with direct typed WordExpr/Fox evaluation for the base and every seed.
Never use `formula([])=0` as the base gradient.  Targets 1--5 may be replayed
only as zero-gradient canaries; they are not additional questions in this
task.

Reduce `z` and every `delta_i` freshly against B1, with each temporary pool/DAG
suffix rolled back to the post-block anchor.  Do not reuse a B0 remainder,
old support-one dual, or pool ID.  Public coordinates are one-based component
plus exact canonical 154-byte blob in component/blob order.

Solve over F3, in seed order 1..108,

```text
A a = b,       b = -z_bar,
equivalently   z_bar + sum_i a_i delta_i_bar = 0 in C1/B1.
```

Continue absorbing all target-6 coordinates after the first contradiction so
rank, nullity, row-space digest, and dual refer to the complete 108-variable
system.  A normalized inconsistent dual must satisfy

```text
y A = 0,  y b = 1,  hence y z_bar = 2.
```

Bind its exact semantic support/provenance and support cap.  This quotient dual
is a handoff for a later fresh reverse-pivot correlation; v1 must not run that
next correlation or call it a full-D2 separator.

If the system is consistent, compute the canonical solution in variable order,
construct the exact ordered literal/typed product (coefficient 0/1/2 means zero,
one, or two copies of that registered seed), and directly replay the selected
target-6 Fox gradient.  Produce an exact packed D2 proof against B1, serialize
only the reachable proof DAG, and independently check that the proof expands
to `z + sum_i a_i delta_i`.  A target-6 consistency bit without this selected
direct replay and proof is not a mathematical terminal.

## D. Terminals and claim boundary

Exactly four terminal tokens are allowed:

1. `B345_E4_D2_LEXBLOCK_TARGET6_CONSISTENT`
   - iff the complete block is committed, the complete 108-variable system is
     consistent, and the canonical selected target-6 proof is directly
     replayed;
   - exact claim: one concrete correction in the registered 108-seed affine
     family has target-6 boundary in B1, hence in full D2 for this pinned E4
     roof;
   - it is **not** evidence that targets 7--33, all literal gates, settlement,
     or a typed lift pass.
2. `B345_E4_D2_LEXBLOCK_TARGET6_INCONSISTENT`
   - iff the complete block is committed and the complete target-6 system is
     inconsistent with a checked normalized dual;
   - exact claim: no coefficient vector in the registered 108-seed affine
     family solves target 6 modulo B1;
   - because `B1` is only a subspace of full D2, this is not a full-D2
     obstruction, nonexistence result, or reason to skip a later block.
3. `B345_E4_D2_LEXBLOCK_TARGET6_UNKNOWN_RESOURCE`
   - registered wall/RSS/size/count caps only; no mathematical claim.
4. `B345_E4_D2_LEXBLOCK_TARGET6_UNKNOWN_INPUT`
   - authenticated external path/pin/schema/input failures only; no
     mathematical claim.

Every receipt must set, with exact booleans:

```text
single_lexfirst_translation_block_only = true
complete_11_relator_block = true              # only after normal block completion
all_old_active_rows_added = false
full_D2_claimed = false
full_H3_claimed = false
targets_7_through_33_checked = false
typed_lift_claimed = false
negative_claimed = false
B4_A_claimed = false
B4_B_claimed = false
```

For CONSISTENT, `target6_membership_in_full_D2_for_selected_correction=true` is
allowed because B1 is a proved subspace of full D2.  No wider positive flag is
allowed.  For INCONSISTENT that flag is false/absent.

## E. Receipt, provenance, and exact schema

Use exact top-level and nested keysets per terminal/reason/phase.  Validators
must compare equality of key sets, not subset unions.  At minimum bind:

- schema/task/source/checker/driver/q3/157ec/157eh pins and stable run evidence;
- exact 108-seed manifest and typed source preflight;
- fresh B0 prefix counts and stable digests;
- old qstar oracle, 76 base occurrences, complete correlation counts/digest,
  first-active row, contributing pair, and state-neutrality snapshot;
- exact section-expression and direct word replay for `g` and `t`;
- the ordered 11-column raw/reduced ledger, translation-block digest,
  pre/post accounting, rank gain, and post-block anchor digest;
- target-6 base/delta direct-vs-typed ledger, 109 fresh remainder digests,
  coordinate/equation counts, rank/nullity/consistency, row-space digest;
- exactly one of normalized dual/provenance or canonical solution plus selected
  direct proof;
- one absolute performance/resource envelope and stage-complete marker.

RESOURCE has exact stage-aware partial shapes for authentication, fresh prefix,
old dual/correlation, section recovery, block insertion, target base, seed
`i`, affine absorption, and selected proof.  A partial record names exact
completed counts and makes every unevaluated result null/absent; it never
contains a consistency or obstruction claim.  Require `reason==cap_key`, exact
limit/observed values, and exact `gt`/`ge` semantics.  UNKNOWN_INPUT cannot
carry prefix/block/affine/proof fields.  Non-consistent terminals cannot carry
selected-proof fields.

Receipt serialization is outside the mathematical monitor but has its own
checked-write byte cap and exact readback.  A serialization overflow falls
back to the canonical RESOURCE schema; it must not publish a partial positive
file or a stale prior receipt.

## F. Independent checker

The checker must not call the producer's predicate, finalizer, block builder,
affine solver, or receipt validator.  Producer may authenticate/use the frozen
157ec/157eh producer-side arithmetic; checker uses the corresponding frozen
checker-side implementations and independently reconstructs:

1. q3, E3/E4, all 108 words and source/context gates;
2. B0 and its exact stable counts/digests;
3. qstar, all base occurrences, the complete correlation, canonical first
   ACTIVE row, contributor, and typed section;
4. all 11 translated columns and B1 in the fixed insertion order;
5. all 109 target-6 raw/reduced vectors and the complete affine system;
6. the inconsistent dual or consistent selected proof.

The two languages/processes may allocate different pool IDs and may have
different harmless cache schedules.  All cross-language bindings use canonical
`(component,154-byte blob)` values and semantic packed rows.  Add a bounded
fixture that deliberately pre-interns irrelevant values in only one side and
still produces the same public result.  Also reject any receipt that exposes
or relies on transient pool/DAG/section IDs.

## G. Monitor and resource contract

Use one base monotonic clock and one RSS epoch from process start.  Adapters
never reset either.  Preserve the exact 157eh fresh-prefix outer/inner registry
and identity/detach gates.  After the old correlation, attach new exact
outer-phase adapters to the post-prefix DAG/basis only for the block insertion
and target/proof work; detach and identity-check them at the documented
boundaries.  Trace the actual pinned helper call tree and publish one closed
outer/inner pair table plus canonical digest.  No `startswith`, wildcard,
inner-to-outer inference, or catch-all phase is allowed.  Unknown callbacks are
hard failures.

Inherit the frozen structural caps and at least:

```text
translation blocks selected/committed       exactly 1
relator columns attempted on normal path    exactly 11
affine variables                            exactly 108
affine rows                                 1000000
target live remainders                      2000000
dual provenance/support                     at least 128, with exact gt gate
common soft wall                            18000 seconds
soft RSS                                    4831838208 bytes
packed receipt                              268435456 bytes
```

Do not silently raise an inherited cap.  If the normalized dual needs more
than the registered support bound, return RESOURCE after preserving the full
completed-system partial ledger, not INCONSISTENT.  The GHA job budget remains
330 minutes.

## H. Combined production-path selftest

One bounded combined selftest must traverse the same production block,
target-6 solve, terminal finalizer, receipt schema, and independent checker
validator.  It must include both consistent and inconsistent noncommutative
fixtures and all four terminal envelopes.  At minimum reject mutations for:

- selecting a first row before completing/cancelling the full correlation;
- `h^-1*g`, right action, wrong inverse, relator/scalar/blob drift;
- adding only relator 9, omitting/duplicating/reordering a block column;
- requiring relator 9 itself, rather than the whole block, to be independent;
- importing an old B0 remainder/dual after B1 is installed;
- taking rollback anchors before the persistent t/11-column block;
- using `formula([])=0` as the base target-6 gradient or reversing `b=-z`;
- stopping affine absorption at the first contradictory coordinate;
- pool-ID-dependent public equality or producer/checker allocation coupling;
- support/provenance, proof-root, coefficient-order, or reachable-DAG drift;
- stale success fields in INCONSISTENT/RESOURCE/INPUT receipts;
- wrong reason/phase/cap relation, mid-block partial-count drift, receipt
  overflow, stale output, source/task/driver pin drift;
- a fixture-only early return that bypasses the production helper/finalizer;
- a missing monitor callback, stale adapter after detach, clock/RSS reset;
- including elapsed/RSS/object/cache fields in a stable mathematical digest;
- unescaped driver command quoting or accepting a producer marker without the
  independent checker marker.

The selftest log must expose markers proving that the real block insertion,
target reducer, consistent proof, inconsistent dual, four exact schemas,
independent pool schedule, monitor callbacks, and checked-write fallback were
entered.  Syntax compilation alone is not sufficient.

## I. Driver and stale-pass discipline

The thin GAP driver pins the final producer/checker/task hashes, invokes the
same-job q3 child and q3 checker, removes every stale output/sentinel/log before
work, runs producer and checker with pipefail/tee semantics and one shared
absolute deadline, and accepts exactly one of the four registered terminal
tokens plus exactly one checker PASS marker.  A shell/GAP/Python syntax error,
missing output, duplicate terminal, checker failure, stale sentinel, or hash
drift is a failed job.  Upload the receipt and bounded logs only after all
markers pass.

## J. Runtime expectation and decision tree

Source/run evidence:

- 157ec producer reached the complete old prefix near 268 seconds and the
  complete 108-column target-6 inconsistency at 530.737 seconds; its GHA Run
  GAP step (producer plus checker) took about 17m57s and peak producer RSS was
  744943616 bytes.
- 157eh producer completed prefix, reverse dual, correlation, and witness in
  about 284 seconds; the whole producer/checker step took about ten minutes and
  peak producer RSS was about 766 MB.
- eleven new columns are only 0.0031% of the old 362725-column prefix.  The
  target-6 109-vector reduction remains the dominant incremental cost.

Expected INCONSISTENT branch: producer 9--13 minutes, checker 9--15 minutes,
full job 20--32 minutes.  A CONSISTENT branch with selected proof may take
roughly 27--55 minutes total.  Pessimistic but non-resource range is 45--90
minutes; the 300-minute soft wall and 330-minute job budget remain fail-closed.
Expected RSS is below 1 GiB, with a conservative under-2-GiB band before the
existing 4.5-GiB soft cap.

Interpret outcomes exactly:

- CONSISTENT -> hand off the concrete target-6 coefficient/proof to a later
  targets-7--33 lane; do not call it a lift.
- INCONSISTENT -> hand off the new normalized quotient dual to a later fresh
  full-correlation step; do not bulk-add the old 568 ACTIVE rows.
- RESOURCE/INPUT -> repair only the registered resource/transport/input issue;
  do not infer mathematics.

## K. Reply and freeze

The reply must list final paths, hashes, byte lengths, authenticated pins,
selftest command/log outside the repo, exact PASS markers, terminal meanings,
runtime estimate, and `git status --short` evidence.  End with exactly:

```text
READY_FOR_GHA
```
