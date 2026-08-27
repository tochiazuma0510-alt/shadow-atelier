# Luna task 179 — R07 positive-only common-word column generation v1

Commissioner: Sol / 2026-08-27

Role: Luna implementation and GHA computation.  The mathematics is fixed by
v110, v139, and v140.  This is the first actual R07 positive search, not
another toy moment implementation.  The producer may stop early only on a
fully replayed common word; an unsuccessful bounded scan is resource-unknown
and is never a separator.

## 1. Objective

Build a fail-closed producer, helper-nonshared positive-certificate checker,
ASCII GAP/GHA driver, immutable noncommutative SELFTEST fixture, and Luna
reply for

\[
 (-T_{H1},-T_{H2},-T_P,0,0)
 \in D_{\rm all}+\operatorname{span}
 \{V_{\delta,r}:\delta\in\Delta_{\rm all},
 r\in\mathcal R_\Omega\}.
\]

The production path must actually reconstruct the R07 target, boundary
columns, linked sections, and correction columns.  It must run a resumable
positive-only column-generation loop.  If membership is reached, return one
literal right-correction word and replay both hexagons plus the frozen
five-factor pentagon.  If a cap is reached first, return a versioned
rank/basis checkpoint and typed `UNKNOWN_RESOURCE`; do not emit a dual
separator.

## 2. Governing proof and fixed source identities

Pin and implement exactly:

```text
sol/proof_r07_witness_first_fibre_dovetail_selector_v139.md
  bytes=8310
  sha256=62e2160348db38eca1570b2ca6eb8934b885569f4e8cfb276a91b98c9b983920
sol/proof_r07_positive_only_common_word_colgen_v140.md
  bytes=10073
  sha256=6d388a74c75d55d215b0035496c451aa9de5bbc7a8248c277e76021092b8562b
sol/proof_r07_cubic_moment_resource_cap_erratum_v138.md
  bytes=6371
  sha256=9dc94b6de5120e54f3b5a5324fb58a24646ad5917b3bd85c36162af29aa86456
```

V138 is relevant only to resource honesty.  No task179 PASS may use the
withdrawn v136 constants `1536`, `9893376`, or unconditional signed-64
safety.  This positive route does not need a complete cubic moment.

Pin the repaired task175 runtime bundle exactly:

```text
search/d972_r07_all_seven_raw_bridge_preflight_v1.py
  bytes=57132
  sha256=ef0df11b4aa4efe3fc7b5136e7348c0920609ec9974e2fc918c7bd795deb28ca
crosscheck/check_d972_r07_all_seven_raw_bridge_preflight_v1.py
  bytes=79414
  sha256=4b6cd61050bbdfa23c4bb1e0b62b151fb93dec12a64e912b17fc6d320601c228
search/d972_r07_all_seven_raw_bridge_preflight_gha_driver_v1.g
  bytes=14797
  sha256=e4fa11d9b1f2ab7f0f0eb6c35c9a15bfa3c1fa5b3db37fefb67cd516273b4b2d
```

Pin the repaired task176 runtime bundle exactly:

```text
search/d972_r07_all_seven_extension_section_census_v1.py
  bytes=63872
  sha256=5cf5617bebc932833dd34105bd85b2536e8c332137dce0f6ea176ebd82e09bd3
crosscheck/check_d972_r07_all_seven_extension_section_census_v1.py
  bytes=82983
  sha256=892b9b2e086acf2dc9cb69e01b8c5ebb579050ae1622dd2ed4b66c83887a69a8
search/d972_r07_all_seven_extension_section_census_gha_driver_v1.g
  bytes=15817
  sha256=9d854d02b1c8c1fdcdda5855f16a85b1d8f51998c6a9a4a660c0313138a9839f
```

Also pin v108, v110, v121, v122, v125, the task157ee q3/joint receipts,
the current full-D2 positive-correlation engine, and every imported arithmetic
source by exact path/bytes/SHA.  Discover their current identities by static
read/hash and record them in the reply; do not use a placeholder pin.

The parent is separately running task175 production `33042556905` and
task176 production `33043237638`.  Those runs are audit gates, but task179
must reconstruct every source datum it uses from the pinned files.  Do not
assume that a prior large artifact is present in a fresh GHA checkout.

## 3. Correct target and additivity convention

Reconstruct task175 production data through its real authenticated path.
The target is

```text
(-raw_base_targets.H1, -raw_base_targets.H2,
 -raw_base_targets.P, 0, 0)
```

over F3, with the H1/H2/P block tags retained.  The task175 field
`stacked_target` is a canary correction-change row and is forbidden as the
base target.

Use the registered right convention `corrected_word=reduce(g760+correction)`.
For a retained correction column
`w=u r u^-1`, coefficient 1 contributes `w`, coefficient 2 contributes
`w^-1`, and coefficient 0 contributes nothing.  The order is the frozen
basis-column order.  PB3/PB4 boundary chains certify quotient equality but
must never be multiplied into the source correction word.  Replay v140
Theorem 2.1 directly.

## 4. Production reconstruction

The producer may import pinned task175/task176 arithmetic, but it must bind
their exact APIs and representations explicitly.  In particular retain the
task176 packed joint serializer; never call the frozen
`value[0] + value[1]` serializer on a tuple/bytes element.

Reconstruct:

1. the E3/E4 marked groups, v135 noncontiguous fourth-strand deletion, and
   all ten typed contexts;
2. the complete 6,441 word-bearing normal-generator roster;
3. the three raw base targets and literal PB3/PB4 base gradients;
4. the 243 Gamma states and their source words;
5. the 1,469,664-state Q0 positive shortlex section with parent/letter words;
6. singleton `A_S`, `L_S`, `Gamma_S^0`, adjusted L lifts, and word-bearing
   target-section lookup required by v139; and
7. sparse typed column operations over F3, including the two exponent rows.

Do not materialize or deduplicate all 357,128,352 linked Delta values.  The
Q0 section may use an outside-repository fixed-width/mmap store.  A complete
task176 JSON serialization is optional; the search may consume the live
fixed-width section and retain only digests plus selected word paths.

## 5. Initial basis and positive boundary oracle

Start from a deterministic authenticated independent subset of PB3/PB4
boundary columns and a small deterministic set of actual correction columns.
The subset need not already equal full D2 because a positive receipt remains
sound in every subspace.

For each nonzero target remainder, construct an exact sparse dual lambda with
`lambda(current_basis)=0` and `lambda(target)!=0`.  Probe PB3 and PB4 first.
Reuse or port the authenticated support-times-occurrence full-D2 correlation
method: accumulate the complete scalar for one translation before deciding
ACTIVE, materialize the complete typed boundary column only after a nonzero
scalar is found, and add it only after a new-pivot check.  A bounded prefix is
allowed, but exhaustion of that prefix is only `UNKNOWN_RESOURCE` unless the
correction oracle later returns a positive column.

Do not import the old target6 functional, target, fixed prefix, or negative
claim.  Only its generic marked-group translation/correlation arithmetic may
be reused after rebinding the current all-seven dual and raw PB3/PB4 rows.

## 6. Positive correction oracle

For each current dual and every one of the 6,441 rows, reconstruct the full
eleven-occurrence scalar formula

\[
 F_r(\delta)=K_r+\sum_i\sum_{t\in T_{r,i}}
 c_{r,i}(t)1_{\pi_i(\delta)=t}.
\]

Merge equal `(coordinate,target)` constraints in F3 and delete zero sums
before traversal.  The 110 task175 pairs are canaries, not the full weighted
table.

Run this fixed positive schedule:

1. canonical task176 section representative for every nonempty support
   target fibre, in `(row,coordinate,target)` order;
2. round-robin kernel-roster prefixes of lengths `1,2,4,8,...` for every
   live fibre, retaining one linked Gamma state across all ten contexts;
3. interleave the canonical global `(q,gamma)` source roster whenever
   `K_r != 0`; and
4. stop at the first direct full-eleven-term nonzero scalar.

Materialize `u_delta r u_delta^-1`, replay all ten context values from the
same literal source word, build the complete H1/H2/P/exponent column, verify
the nonzero dual pairing, and require a rank increase.  One occurrence being
nonzero is not enough; the merged full sum is authoritative.

The implementation may add a deterministic batch of ACTIVE columns per dual
for speed, but every member must independently have a new pivot against the
growing basis and retain complete word provenance.

## 7. Loop, checkpoint, and terminals

After every rank increase, reduce the target and emit an atomic checkpoint
record containing:

- exact input/basis/target hashes and rank;
- the reduced target and current dual;
- every retained column's family, source word or boundary translation,
  sparse row digest, coefficient ancestry, pivot, and rank transition;
- completed and pending boundary/fibre/global prefixes; and
- wall/RSS/disk/row/word counters with registered limits.

Within one GHA job, continue from the in-memory checkpoint until the common
word is found or a registered cap is reached.  The final artifact must contain
the latest checkpoint even on UNKNOWN so a later versioned resume can bind it.

Allowed production terminals are exactly:

```text
R07_POSITIVE_COMMON_WORD_COLGEN_COMMON_WORD
UNKNOWN_RESOURCE:<registered phase and cap>
UNKNOWN_INPUT:<authenticated missing or malformed input>
```

No separator terminal exists in v1.  A completed finite prefix, a zero old
functional, a timeout, or a moment not computed is never a negative result.
Programming exceptions are hard nonzero STOPs and must not be converted to
typed UNKNOWN.

## 8. Positive terminal and independent checker

On membership, recover the sparse coefficients and form the literal word
from Section 3.  Retain the boundary coefficient chains separately.  The
producer must directly check:

1. the sparse column identity equals the exact target;
2. every selected correction factor is in the joint kernel;
3. both exponent sums of the product are zero modulo three;
4. `corrected_word=reduce(g760+correction)`;
5. H1 and H2 reduce through their exact PB3 chains;
6. all five coface values occur in the frozen order and their noncommutative
   product reduces through the exact PB4 chain; and
7. every selected source word, conjugate, inverse-for-coefficient-2, and
   context value replays literally.

The checker must not import the producer or share its Gaussian, weighted
formula, fibre-selector, word, or Fox helpers.  It need not repeat the
producer's unsuccessful search prefixes.  By v140 Section 4 it independently
rebuilds each retained column, every rank transition, the final sparse
identity, correction word, joint-kernel/exponent checks, and all seven direct
relations.  This distinction is load-bearing: search completeness is needed
for a separator, not for a printed positive witness.

On UNKNOWN, the checker authenticates pins, checkpoint integrity, counters,
and the absence of every positive/negative claim.  It does not turn the
checkpoint into evidence of nonmembership.

## 9. SELFTEST and mutations

Use a finite noncommutative linked extension with two relation blocks and an
ordered three-or-more-factor product.  Exercise the real sparse dual,
boundary ACTIVE, support-fibre section, kernel-prefix dovetail, `K!=0` global
fallback, rank increase, coefficient-2 inverse, common-word materialization,
checkpoint, and positive checker paths.

At minimum reject, through the normal positive validator:

1. one context value from a different Gamma state;
2. left/right conjugation swap;
3. one omitted Fox occurrence;
4. one same-target coefficient before full merging;
5. one scalar taken from a single occurrence instead of the full sum;
6. an already dependent added column;
7. a changed pivot or rank transition;
8. target/canary confusion;
9. coefficient `1 <-> 2` without word inversion;
10. inserting a boundary chain into the correction word;
11. one PB3/PB4 block-tag swap;
12. one pentagon factor order/sign change;
13. one changed checkpoint pending-prefix cursor;
14. a fabricated separator/zero-correlation claim; and
15. a programming exception relabelled as UNKNOWN.

The producer and checker should use different finite-group representations
where practical.  Whole-dictionary equality is not a semantic mutation
oracle.

## 10. Files and execution discipline

Create only:

- `search/d972_r07_positive_common_word_colgen_v1.py`
- `crosscheck/check_d972_r07_positive_common_word_colgen_v1.py`
- `search/d972_r07_positive_common_word_colgen_gha_driver_v1.g`
- `search/certs/d972_r07_positive_common_word_colgen_selftest_v1_20260827.json`
- `sol/luna_reply_179_r07_positive_common_word_colgen_v1.md`

Do not edit task175, task176, task177, task178, proofs, workflows, or any
predecessor.  Do not run Python, Node, GAP, git, or GHA locally.  Parent alone
audits, commits, pushes, and dispatches.  The driver must be ASCII-only,
single-job serial, reject stale artifacts and line-wrapped sentinels, bind all
source identities, and fit under the normal six-hour GHA ceiling.

Implement the actual production path now.  It is acceptable for the first
bounded production run to end at an honest resumable UNKNOWN checkpoint; it
is not acceptable to leave production as an unconditional prerequisite seal
or unimplemented stub.

## 11. Claim boundary

A `COMMON_WORD` receipt proves only the finite universal B4 all-seven word of
v110/v140.  It is the input to v129's intrinsic `(d,rho)` saturation solve.
It is not yet a compatible cofinal lift, fake, or Ihara witness.  UNKNOWN has
no mathematical negative content.
