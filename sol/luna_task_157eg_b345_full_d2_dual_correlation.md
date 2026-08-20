# 157eg — B345 full-D2 dual correlation census

## Role and authorized scope

Luna implements one versioned, exact dual-correlation lane.  Create only:

1. `search/d972_b345_full_d2_dual_correlation_v1.py`
2. `search/check_d972_b345_full_d2_dual_correlation_v1.py`
3. `search/d972_b345_full_d2_dual_correlation_gha_driver_v1.g`
4. `sol/luna_reply_157eg_b345_full_d2_dual_correlation.md`

Do not edit a workflow, q3, 157ed--157ef, or any other source.  The driver is
ASCII only.  Temporary diagnostics stay outside the repository.  Run one
bounded combined self-test before freeze; a corrective rerun must record its
exact fixture-only reason.  Do not run the full mathematics locally.

This is deliberately a small successor.  Do not add a correction search,
another word-depth census, or an iterative basis-growth loop.

## Frozen predecessors and run evidence

Hard-authenticate these exact files before doing mathematics:

- 157ee producer
  `search/d972_b345_joint_kernel_qstar_closure_v1.py`, SHA-256
  `06ba6cf361957db3e339d48d14b3d4fbc689de9642e3f96273fbe8f3160e76dc`,
  67945 bytes.
- repaired 157ef checker
  `search/check_d972_b345_joint_kernel_qstar_closure_v2.py`, SHA-256
  `5c3b03af26a47f00fbfbd8484e17c591c5399ac708e566506d726d5dbd03ba88`,
  5942 bytes.
- repaired 157ef driver
  `search/d972_b345_joint_kernel_qstar_closure_gha_driver_v2.g`, SHA-256
  `8ff80ba97f3801daf28ad61b19d2f0a01572a5720c13578f11c56bf0d7ad26e7`,
  3912 bytes.
- 157ed producer
  `search/d972_b345_triple_cube_raw_lambda_census_v1.py`, SHA-256
  `d4a290984ae8a93b6959f06d20c1de037b2814707778fba03c59ac87b2f736db`,
  126942 bytes.
- 157ed checker
  `search/check_d972_b345_triple_cube_raw_lambda_census_v1.py`, SHA-256
  `677aa1b69e4415da9629c34fcf0e469ad974cf3c888be7e768635bac50f672ce`,
  97363 bytes.
- 157ed driver
  `search/d972_b345_triple_cube_raw_lambda_census_gha_driver_v1.g`, SHA-256
  `29a31752d42bd3f5a0e7f27ca38495bdd54c9cc694d12ddf9fe637e8749975e9`,
  10223 bytes.
- frozen prefix implementation
  `search/d972_b345_seedspan_triple4_v1.py`, SHA-256
  `fe18fc31fdf3f9416ebb829112ccbd514c27e6a8d30fe24691842865277a0b29`,
  535219 bytes.
- 157ee task SHA-256
  `64a32c0b7e3d4efc41ddb8e0e7036282b0b5430d9ab46bbfe125b588478a95d4`.
- 157ef task SHA-256
  `e626802b32e9577e35f5543b252830abdc4461b409972c9f5536ea29d8bb14ed`.
- q3 artifact SHA-256
  `3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72`.

The cross-checked predecessor is GHA run `32359956713`, commit
`1696e7b44792b97c51a435d4160259462963c52d`, artifact ID `9403505687`,
archive digest
`9fe43b570dd135c4f26c910dff983e0e58492bb3250beb4cbe01d7e8bcca1192`,
and receipt SHA-256
`1c3ad7a7124cee152eb40968cf212c14641a9f8720063c85f70533864898d0df`.
This evidence is provenance only: do not import its receipt, basis, pool,
lambda table, or GAP state.

Fresh reconstruction must reproduce:

```
E4 blob width                 154 bytes (degree 144 + PC rank 10)
prefix BFS translations       32768
prefix directed translations  207
prefix D2 columns              362725
prefix pivots                  362709
dependent columns              16
live sparse entries            3090367
row-tail visits                2727658
prefix pool checkpoint         976408
raw-lambda semantic entries    362710
lambda(base target 6)          2
```

The 11 unshifted PB4 D2 columns have exactly 76 nonzero occurrences, ordered
by relator, component, and canonical E4 bytes, with relator support sizes

```
[8,6,8,6,4,8,12,6,4,8,6]
```

and component totals `[10,12,18,10,12,14]`.  Their public occurrence digest is
`3eacd6dc77d62c1799a55923d3c8d5313a37ceab8e78b58b07b45925a28f131d`.

## A. Exact mathematical question

Let

```
C1 = F3[E4]^6,
Bfull = span{ L_t D2_j : t in E4, 1 <= j <= 11 }.
```

The fresh reverse-pivot functional `lambda:C1->F3` annihilates the registered
362725-column prefix and has value 2 on the base target-6 gradient `z`.
The predecessor explicitly did **not** claim that lambda annihilates `Bfull`.

For a base column

```
D2_j = sum_(c,h) a(j,c,h) e_(c,h),
```

the actual left action used by the frozen code is

```
L_t e_(c,h) = e_(c,t*h),
F_j(t) = lambda(L_t D2_j)
       = sum_(c,h) a(j,c,h) lambda(c,t*h).
```

If `F_j(t)` is nonzero, at least one summand has `g=t*h` in the nonzero
support of lambda, hence necessarily

```
t = g*h^-1
```

for a same-component lambda support coordinate `(c,g)` and base occurrence
`(j,c,h)`.  Conversely, accumulating all such pairs computes every `F_j(t)`
exactly, including cancellations.  Therefore this finite support correlation
is exhaustive over the entire (very large) E4 without enumerating E4.

Type clarification after T-61: the acting group in this D2 chain module is the
pinned PB4 quotient **E4**, not the joint F2 correction quotient called `J` in
157ee/T-61.  The 11 unshifted PB4 relator columns are, by definition, the 11
orbit representatives whose E4-left translates generate `Bfull`.  Hence no
extra `prefix_generates_module`/FC-44 assumption is needed.  Do not replace
this exact correlation by a coinvariant `(x-1),(y-1)` shortcut: one direction
of that shortcut was explicitly left unaudited in T-61.  The support argument
above evaluates all E4 translates directly and is the load-bearing theorem.

## B. Fresh prefix, lambda support, and base columns

Producer imports the pinned 157ed producer only through an authenticated
module loader.  Checker imports the pinned 157ed checker and independently
rebuilds E3/E4, the prefix, base columns, and reverse-pivot lambda.  They must
not import one another's pool IDs, rows, support table, or correlation map.

Build lambda once in reverse canonical pivot order.  Publish and independently
check its nonzero support as canonical rows

```
[component_u8, exact_154_byte_blob_hex, coefficient_in_{1,2}]
```

sorted by `(component, blob)`, with count and digest.  The nonzero count is a
measurement, not a hardcoded acceptance value.  All zero-valued pivot-table
entries remain covered by the predecessor semantic digest.  Candidate queries
must never intern new pool elements.

Independently rebuild all 11 base columns from the PB4 relators.  Require the
76-occurrence count, the per-relator and per-component counts above, the
ordered public digest, quotient identity, and `D1*D2=0` for every column.

Actual helper-shape warning: the frozen `build_fresh_prefix` return contains
private `model4`, `pool`, and `sections`, plus the **public**
`directed_base_support`; it does not contain a private `base_occurrences`
field.  Reconstruct internal occurrences from `model4` with
`freeze_base_support_occurrences(model4,pool,sections)` (which must reuse the
already registered canonical roots), and exact-compare its public projection.
Reading `prefix["base_occurrences"]` is a dispatch-stopping shape bug.

## C. Exhaustive correlation algorithm

Precompute the inverse of each of the 76 base E4 values once.  For each
same-component pair

```
(lambda row (c,g,l), base row (j,c,h,a))
```

compute directly in E4, without pool interning,

```
t = g*h^-1
corr[j, canonical_blob(t)] += a*l mod 3.
```

Delete zero totals only after all contributions to a key have been added.
The remaining map is exactly the nonzero set of `F_j(t)`.  Freeze public order
as `(translation blob lexicographically, relator index)` and define the first
active entry in that order.  Record:

- nonzero lambda support count and per-component counts;
- exact pair-attempt count
  `sum_c lambda_support_count[c] * base_occurrence_count[c]`;
- distinct `(j,t)` candidate count before zero deletion;
- cancellation-to-zero count and nonzero active count;
- scalar distribution in F3;
- canonical packed digest of every nonzero `(t,j,scalar)` row;
- the canonical first active row, if any.

Use fixed-width packed bytes `(translation_blob_154 | relator_u8 | scalar_u8)`
for the semantic digest.  Hashes never replace exact equality.

Hard direct canaries:

1. identity translation: correlation value equals termwise direct lambda on
   the unshifted raw column;
2. first active entry, when present: explicitly evaluate the entire translated
   raw column term by term and require the same scalar;
3. at least four deterministic candidate translations, including a
   cancellation-to-zero row when one exists;
4. replacing `g*h^-1` by `h^-1*g`, `g^-1*h`, or right translation must be
   rejected by the shared production helper on a noncommutative toy fixture;
5. correlation must leave pool cardinality, IDs, basis rows, DAG, section
   registry, and caches semantically unchanged.

Caps:

```
pair attempts                 8388608
distinct (j,t) candidates     2000000
packed active rows             2000000
```

Cap exhaustion is atomic `UNKNOWN_RESOURCE`, never a separator or active
claim.  Process relators incrementally if useful, but semantic order/digest is
organization-independent.

## D. First-active section witness

If an active row exists, retain the lexicographically first contributing pair
`(c,g,l;j,c,h,a)` and verify `t=g*h^-1`; also recompute the complete scalar so
the single pair is never mistaken for the total.

For a fixed public `(t,j)` row, "lexicographically first" means the exact tuple
`(component, g_blob, h_blob, lambda_coefficient, base_coefficient)`, with blobs
compared as raw 154-byte strings.  It must not depend on dictionary insertion,
pool IDs, or the producer/checker loop organization.

Construct an exact section expression for `g` by the sparse-oracle theorem:

1. first try the base target-6 Fox prefix map (this covers qstar support);
2. otherwise scan all same-component base occurrences `h0` in canonical order,
   set `u=g*h0^-1`, and choose the first `u` in the registered BFS/directed
   translation-section table; then `w_g = w_u * w_h0`;
3. set `w_t = w_g * inverse(w_h)`.

Use a typed PRODUCT/INVERSE section DAG bound to canonical blobs, not a long
flat word and never a transient pool ID.  Directly evaluate `w_g` and `w_t`
in E4.  Recovery failure is a hard invariant failure, not `UNKNOWN_INPUT`.
Checker reconstructs the sparse recovery search independently.

Legacy API trap: the pinned seedspan predecessor's
`SectionExpressionDAG.materialize()` still contains the formerly unreachable
name `inverse_word` instead of `inv_word`.  ACTIVE makes an INVERSE node live,
so calling that inherited method would deterministically crash.  Do not edit
the predecessor and do not call this method for the witness.  Materialize or
stream-replay the reachable typed DAG in the new producer/checker with their
own explicit inverse/reduction helper, cap and value gates.  The ACTIVE
production-path self-test must execute an actual INVERSE node.

The target-6 prefix map is rebuilt fresh from the literal base target-6 Fox
replay after the prefix is complete; it is not imported from the transient
map used by the earlier prefix probe.  Re-running
`freeze_base_support_occurrences(model4,pool,sections)` must reuse and gate the
already registered `base_prefix_roots`, not allocate a second semantic set.

This witness identifies the next complete 11-relator translation block.  This
lane does not add that block and does not claim a lift.

## E. Terminals and exact claim boundaries

Four terminals only:

1. `B345_E4_FULL_D2_QSTAR_SEPARATOR`
   iff the complete correlation has `active_count=0`.  It certifies that
   lambda annihilates every E4-left translate of all 11 base D2 columns while
   `lambda(z)=2`, so the base target-6 class is outside the **full D2 image for
   this pinned E4 roof**.  Combined with the cross-checked 157ee theorem, every
   correction in its exact joint kernel K retains this obstruction.
2. `B345_E4_FULL_D2_ACTIVE_TRANSLATION`
   iff the complete correlation has a nonzero row.  It exports the canonical
   first active translated boundary column and its section witness.  This only
   says the present lambda is not a full-D2 separator; it is not a lift and not
   target-6 membership.
3. `B345_E4_FULL_D2_UNKNOWN_RESOURCE` for registered resource limits only.
4. `B345_E4_FULL_D2_UNKNOWN_INPUT` for authenticated external pin/schema/input
   failures only.

Even the separator terminal is scoped to the pinned E4 roof and 157ee joint
kernel.  Never claim alternate-roof exhaustion, full-H3 correction exhaustion,
global lift nonexistence, or B4-A/B.

## F. Receipt and checker

Use exact terminal/phase top-level and nested keysets.  Bind at least:

- all task/source/q3/predecessor hashes and the cross-checked run provenance;
- fresh prefix, pool checkpoint, base 76-occurrence ledger, and raw-lambda
  semantic reconstruction;
- canonical nonzero lambda support count/per-component counts/digest;
- pair/candidate/cancellation/active counts and scalar distribution;
- organization-independent packed correlation digest and first active row;
- direct canaries, pool-no-mutation accounting, and section DAG/witness when
  active;
- theorem-boundary booleans, phase timings, RSS/wall accounting, cap registry,
  actual observed counts, comparator, and atomic partial prefix.

The checker reconstructs all mathematical objects and the complete correlation
from q3 and pinned sources.  It may use a different iteration organization but
must obtain the same exact canonical rows and digest.  It must reject extra
keys, terminal/reason drift, public/private helper-shape drift, wrong blob
width/component numbering, and a producer-only section witness.

## G. Self-test, driver, and runtime

The combined self-test must enter the same production correlation, terminal,
schema, and section-recovery helpers on a small nonabelian group.  It must
cover both an ACTIVE fixture and a no-active exhaustive separator fixture, a
true cancellation row, the three orientation mutations, a public projection
without private fields, pool-cardinality neutrality, cap/phase/reason schema,
and section-expression value replay.

The driver pins final producer/checker/task/predecessor hashes, runs q3 in the
same isolated child pattern, uses pipefail+tee, exact-one markers, and one
shared 18000-second producer+checker deadline under the 330-minute job.  Run
GHA self-test first and dispatch full only at that exact commit after it passes.

Expected normal cost is prefix-dominated: producer about 6--10 minutes,
checker 6--10 minutes, same-job about 12--22 minutes, RSS about 0.8--1.4 GiB.
If the measured lambda support makes the registered correlation caps relevant,
return honest `UNKNOWN_RESOURCE`; do not widen caps or enumerate E4.

## H. Mandatory recurrent-failure guard

The reply must contain an explicit PASS or N/A-with-reason line for every item:

1. **Frozen snapshot:** verify every pin by SHA/bytes both before editing and
   at freeze; never audit a changing live file or overwrite a predecessor.
2. **Actual data shape:** trace helper return keys/types through call sites;
   never read a private field from a public projection.  Add exact-keyset and
   shape-mutation canaries in producer and checker.
3. **Production-path self-test:** use the actual selector/helper/finalizer/
   schema/terminal entry, not a fixture-only early return.
4. **Producer/checker state order:** compare pool anchors, intern order,
   snapshot/rollback, ID reuse, and basis commit positions.  Checker probes
   are transactional and cannot pollute persistent schedules.
5. **RESOURCE contract:** exact stage-aware keysets, closed reason/cap
   registries, actual observed count and gt/ge comparator, exact phase/current
   coordinates, and atomic rollback are mirrored in P/C.
6. **Driver/pins:** final P/C/task hashes, no placeholders or stale paths,
   markers exactly once, pipefail/tee, shared deadline, GHA self-test before
   full on the same commit.
7. **Performance:** immutable hashes/contexts are computed once outside hot
   loops; no per-candidate full DAG/target rebuild, full sparse materialization,
   or unbounded cache; inner loops have wall/RSS cadence and registered caps.
8. **Claim boundary:** producer-only is not cross-checked; prefix/roof/kernel
   scopes and UNKNOWN are explicit; no promotion to full-H3/global no-lift.

Any failure of this checklist is a dispatch STOP, not a reason to weaken the
checker or expand runtime/resource limits.
