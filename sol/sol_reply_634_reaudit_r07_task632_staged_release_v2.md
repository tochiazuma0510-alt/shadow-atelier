# Sol(max) Task634 reply: final static re-audit of Task632 staged release v2

## Verdict

`PASS`.

Task632 closes exactly the four finite Task631 repairs R1--R4.  I found no
concrete launch-blocking regression in the finite boundary registered by the
Task634 mail.  The exact quartet below is safe for the parent to commit, push,
and launch through the pinned GHA workflow.

This is a static/code verdict only.  No production route or GHA job was run,
and no payload or mathematical result was produced.  `verified=false`.

## Exact input binding

All mandatory parents and all four final release inputs were read completely.
The byte streams used for this verdict are:

| input | bytes | SHA-256 |
|---|---:|---|
| Task634 mail | 3,642 | `9e52fd30c2a5f736e68b486fdd3edd097af5c06188c6a9f7be79ecdd978d7d69` |
| Task631 reply | 13,862 | `88ddf2e7a96f5ec4f6a7a0d2b9060e5eda894a1800654ee8be2d9647293ba91d` |
| repaired theorem v475 | 8,253 | `757ffab5aa011643efa3df4b133dc03d423895d57a003ed6830a47528388148e` |
| Task629 reply | 4,103 | `581a6242bb2f584d04c298594a361695bc91271ab0a9791677273c941c3dea90` |
| final v2 producer | 75,000 | `ce036c4a1a92d16a78cb8da8c16dee282a6a981889f821e6df82eaecdd8fba0a` |
| final v2 checker | 104,392 | `8c3dd039368f63d62ef79694a196f73d0b626134df39673c5e48c98c7c8787f9` |
| final v2 workflow | 6,077 | `d5f724eb163faf68e0555ec4e5e32dcf05b2d3df1749da89b8762ff5078e6109` |
| Task632 Luna reply | 7,796 | `6ef38b64baee05ed26a57b8cfbf7e2c80baaa11079ea0775ad9aed5b392d8ab8` |

The four final sizes and hashes match the Task634 authentication table
exactly.  The workflow's producer, checker, Task632-reply, v3-producer, and
v475 pins match their current byte streams.

## R1--R4 decision

### R1. One checked outgoing batch per active node: PASS

Both executables retain the complete streaming prevalidation over every
static edge.  In the later propagation pass, a nonempty node first constructs
one local tuple of checked outgoing descriptors, then iterates every exact
path over that tuple.  The tuple is explicitly deleted after the node.  No
whole-graph Python edge cache is introduced; the added retention is only the
current reached node's outgoing batch.

In both implementations `state_edge_traversals` is incremented inside the
path-by-edge loop.  Thus a node with `N` exact paths and degree `d` contributes
`N*d`, independently of the two provider calls (one global validation call
and one active-node call).  It still counts state-edge pairs with path
multiplicity, not provider invocations.

The shipped two-path fixture gives two provider calls for its common node and
four total state-edge traversals.  My additional three-path/two-edge serial
probe gave, independently in producer and checker:

```text
provider calls for every active node = 2
expanded states                    = 6
state-edge traversals              = 9 = 3 ingress + 3*2 outgoing
leaf keys                          = 6 exact (seed, tuple) keys
```

### R2. Direct exact-tuple terminal accumulator: PASS

Producer internal node buckets continue to use compact path IDs.  Its literal
insertion now forms the terminal key directly as
`(int(seed), paths[path_id])`; the second component is the already interned
exact freely reduced tuple.  Cancellation occurs in that dictionary, and the
same dictionary is returned and serialized.  The former full
`(seed,path_id)` dictionary followed by a terminal `leaf_map` comprehension is
absent.  Sorting, coefficients, leaf counts, and compact leaf bytes are
unchanged.

### R3. One tuple formation for each canonical product: PASS

On the producer path, the native list returned by the pinned
`v3.floor.wm(left,right)` is passed directly to the validating interner, which
performs its sole tuple construction.  An already built-in-integer tuple is
validated and reused without reconstruction.

The checker independently retains `word_mul`, which constructs its canonical
tuple once.  Only that return value enters the narrowly scoped
`remember_product` path; it requires an actual tuple with built-in integer
letters, checks the alphabet, free reduction, and path-length cap, registers
the exact tuple, and reuses it.  Raw roots and raw edge suffixes still go
through the full normalization and validation path.  Typed-root checks and
the independent checker boundary remain in place.  Neither implementation
coalesces words by endpoint, signature, hash alone, seed alone, or transient
path ID.

### R4. Manifest-inclusive durable cap: PASS

The producer now canonicalizes `manifest` exactly once, computes

```text
sum(exact receipt-file bytes) + len(the exact manifest_raw byte string),
```

rejects a strict excess as `UNKNOWN_RESOURCE:durable_cap` before writing or
publishing, writes that same `manifest_raw`, and reports the inclusive total
as `payload_bytes` in `payload-sealed` telemetry and its terminal JSON.  An
exact-cap total is accepted; adding one manifest byte is rejected.

The checker first authenticates every receipt's actual length and digest,
then independently recomputes the same receipt sum plus the raw canonical
`manifest.json` length, applies the cap, and reports the inclusive total in
its terminal telemetry.  There is no manifest self-reference.

On producer cap failure the process-specific staging directory is discarded;
`os.replace` remains after all receipts, the manifest construction, and the
inclusive cap gate.  Hence an exhausted cap cannot publish a partial payload.

## Concrete regression boundary

No R1--R4-induced regression was found in the registered boundary:

- The Task554 source is still `33677346616/1`; the Task595 candidate is still
  `33707397894/1` at commit
  `93f746ad1b649796e1bc28e00ff34993498929ee`.  The lower-first route still
  gates the exact 8,059 logical offers, 2,014/6,398 offer counts,
  1,661/5,044 ranks, 3,317 MEMBER coefficients, zero remainder, authenticated
  basis, and reconstructed basis equation.
- The executable order remains decreasing `G`, decreasing `L`, four
  decreasing `B` stages, canonical `D`, four decreasing `O` stages, then
  leaves.  The `G,L,B,D,O` constructors retain the accepted v475 signs and
  scales, left-to-right `red(Pq)`, strict reduction and actor-parent
  inequalities, ancestry bindings, and typed roots.
- Exact tuple equality remains authoritative throughout the staged
  calculation.  Producer interning is injective on tuples, while the checker
  keeps its separate tuple set and separately encoded complete leaf stream.
- The checker still performs the later standalone full reroute of all 8,059
  objects, including the all-zero old-lower offers, authenticates every
  physical row/edge cursor, requires terminal cursor exhaustion, and checks
  the MEMBER equation independently.
- Atomic publication is retained.  Producer cap failures and checker
  computational-resource failures retain `UNKNOWN_RESOURCE` semantics; an
  over-cap purported payload is rejected by the checker's receipt gate.
  Manifest and roots still require
  `direct_occurrence_replay=false`, `next_degree2_residual=null`, and
  `cross_checked=verified=A0=COMMON=FAKE=IHARA=false`.
- The workflow uses six immutable 40-hex action pins, runs producer then
  checker serially, promotes payload/verdict only after checker success, and
  always uploads logs.  The inert marker, 60-minute job boundary,
  `ulimit -v 8388608`, 7-GiB RSS/durable caps, exact parent IDs, and v475 pin
  are retained.

## Bounded gates

Only bounded serial fixtures and read-only inspection were used; the real
route was not invoked.

```text
Python 3.13.14
python -m py_compile producer checker                         PASS
python -B producer --selftest                                PASS
  staged fixtures=9; expanded=13; traversals=13; max-live=3
  resource caps rejected=5; provider calls=2; R1/R2/R3/R4 gates PASS
python -B checker --selftest                                 PASS
  staged fixtures=9; expanded=13; traversals=13; max-live=3
  resource caps rejected=5; provider calls=2; projection/R1/R3/R4 PASS
YAML parse / exact hash pins / immutable action pins / EOF    PASS
independent three-path/two-edge scheduler probe               PASS
```

## Residual risk and claim boundary

The real numbers of exact paths, accumulated states, traversals, leaves, wall
time, and peak memory remain result-dependent.  This static PASS does not
prove that the production payload fits the fixed limits.  If it does not, the
honest result remains `UNKNOWN_RESOURCE`, not a mathematical negative result.

No production result, A0, COMMON, cofinal lift, fake witness, Ihara
counterexample, or Lean verification follows from this PASS.  It also does
not promote the release to `cross-checked` or `verified`.

```text
TASK631 R1 EDGE-BATCH REUSE:             PASS
TASK631 R2 DIRECT EXACT-TUPLE LEAVES:    PASS
TASK631 R3 SINGLE PRODUCT TUPLE:         PASS
TASK631 R4 MANIFEST-INCLUSIVE DURABLE:   PASS
FINITE REGRESSION BOUNDARY:              PASS
PARENT COMMIT/PUSH/GHA LAUNCH:           AUTHORIZED FOR EXACT QUARTET
verified:                                false
OVERALL:                                 PASS
```

`R07_TASK632_STAGED_RELEASE_V2_FINAL_STATIC_PASS`
