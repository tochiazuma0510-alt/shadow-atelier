# Luna reply Task632: finite Task625 static/performance repair

## Verdict

`READY_FOR_SOL_MAX_STATIC_REAUDIT`

Only Task631 repairs R1--R4 were applied to the unreleased Task625 v2
quartet.  The completed Task631 reply was read in full and authenticated as
13,862 bytes, 279 lines, SHA-256
`88ddf2e7a96f5ec4f6a7a0d2b9060e5eda894a1800654ee8be2d9647293ba91d`.
No production route, GHA workflow, or git operation was run.

## R1: one active-node edge batch

The producer and checker retain the complete constant-memory streaming pass
that validates every static edge.  During coefficient propagation, each
nonzero node now calls its local edge provider once, validates and materializes
only that node's checked outgoing tuple, reuses it for all exact paths in the
node accumulator, and deletes it immediately afterward.  There is no global
Python edge cache; added live storage is `O(maximum reached-node degree)`.

A two-path common-node fixture measures the provider directly.  The common
node has one provider call during whole-graph prevalidation and one during its
coefficient pass, hence exactly two calls despite its two exact paths.  Its
single constructor edge is still traversed once per path.  The complete toy
graph therefore records four `state_edge_traversals`, preserving v475's
state-edge-pair definition rather than conflating it with provider calls.

## R2: one exact-tuple leaf accumulator

Producer node maps still use compact transient path IDs.  At a literal edge,
however, the terminal accumulator is now keyed immediately by
`(seed, paths[path_id])`, reusing the interned exact tuple.  That same
dictionary is returned and streamed into `literal-leaves.bin`; the former
terminal comprehension that duplicated the full leaf dictionary is absent.

Cancellation, leaf counts, exact-tuple authority, canonical sorting, binary
header/record format, and emitted bytes are unchanged.  A selftest-only source
gate bounds the scheduler body and rejects reintroduction of the old
`(seed,path_id) -> leaf_map` terminal clone pattern.

## R3: one tuple formation per canonical product

On the producer production path, the pinned `v3.floor.wm(left,right)` result
is passed as its native reduced list directly to the validating interner.  The
interner performs the sole tuple formation, then enforces path length,
alphabet, and free-reduction gates.  The fixture authenticates that the pinned
reducer returns list `[2]` for the boundary-cancelling product and retains the
generic canonical-tuple identity check.

The independent checker keeps raw roots and raw edge suffixes on the full
canonicalization and validation route.  Only the tuple returned by its own
local `word_mul` enters the narrowly scoped `remember_product` route; that
tuple is scanned for built-in integer letters, alphabet, free reduction, and
length, entered into the exact-path set, and reused without another tuple
allocation.  A captured-product fixture requires object identity at the
resulting leaf.  Additional raw list, nonreduced-word, and invalid-letter
fixtures confirm that this optimization does not weaken external gates.

Neither executable coalesces by quotient endpoint, signature, hash alone, or
seed alone.

## R4: manifest-inclusive durable boundary

The producer now canonicalizes the manifest exactly once, computes

```text
sum(all receipt file bytes) + len(the exact manifest.json bytes),
```

and applies `UNKNOWN_RESOURCE:durable_cap` before writing/publishing when the
inclusive total exceeds 7 GiB.  The same serialized manifest bytes used for
the size test are written.  No self-referential size field was added.
`payload-sealed` telemetry and the producer terminal JSON report the inclusive
total.

The checker independently recomputes `receipt bytes + manifest_raw bytes`,
applies the same cap, and reports that inclusive value in terminal checker
telemetry.  Producer and checker fixtures both accept a total exactly at the
cap and reject the addition of one manifest byte across it.  Producer failure
continues to remove its process-specific staging directory, so no partial
payload is published.

## Retained Task625/Task622 invariants

The four repairs do not alter:

- exact Task554 source `33677346616/1`, Task595 candidate
  `33707397894/1`, or candidate commit
  `93f746ad1b649796e1bc28e00ff34993498929ee`;
- the lower-first 8,059-offer route, offer counts 2,014/6,398, ranks
  1,661/5,044, 3,317 MEMBER coefficients, zero remainder, and Task595 basis
  equation;
- packed zero-copy physical receipts, all-zero old-lower cursor coverage,
  selected-lower-only preliminary replay, or the later full independent
  8,059-object reroute and cursor exhaustion;
- the v475 `G,L,B,D,O` order, strict reduction/actor-parent gates, signs,
  scales, left-to-right `red(Pq)`, source ancestry, typed roots, and exact
  compact leaf codec/comparison;
- deterministic staged statistic comparison, including
  `expanded_states=sum_v |supp(A_v)|` and multiplicity-counted
  `state_edge_traversals`; or
- the 60-minute workflow, 8-GiB VM, 7-GiB RSS/durable caps, immutable actions,
  exact parents, serial producer/checker, success-only payload gate, always
  log upload, v475 pin, and inert
  `[fire-grade1-selected-slp-staged-v2]` marker.

All manifest/root gates remain
`direct_occurrence_replay=false`, `next_degree2_residual=null`, and
`cross_checked=verified=A0=COMMON=FAKE=IHARA=false`.

## Bounded serial gates

Bytecode cache was outside the repository.  The real route was not invoked.

```text
python -m py_compile producer checker
=> exit 0

python search/d972_r07_a0_grade1_selected_slp_v2.py --selftest
=> PASS
   staged fixtures=9; expanded=13; state-edge traversals=13;
   maximum live=3; resource caps rejected=5;
   two-path provider calls=2;
   canonical tuple reuse/raw word gates/terminal clone absence/
   v3 list-to-interner/manifest-inclusive cap = PASS

python search/check_d972_r07_a0_grade1_selected_slp_v2.py --selftest
=> PASS
   all retained cursor/compact-leaf/claim fixtures PASS;
   staged fixtures=9; expanded=13; state-edge traversals=13;
   maximum live=3; resource caps rejected=5;
   statistics projection and all R1/R3/R4 gates = PASS
```

YAML parsing, immutable workflow contract, exact pin checks, stale-token scan,
and trailing-whitespace/EOF checks pass.

## Final files

| file | bytes | lines | SHA-256 |
|---|---:|---:|---|
| `search/d972_r07_a0_grade1_selected_slp_v2.py` | 75,000 | 2,121 | `ce036c4a1a92d16a78cb8da8c16dee282a6a981889f821e6df82eaecdd8fba0a` |
| `search/check_d972_r07_a0_grade1_selected_slp_v2.py` | 104,392 | 2,934 | `8c3dd039368f63d62ef79694a196f73d0b626134df39673c5e48c98c7c8787f9` |
| `.github/workflows/d972-r07-a0-grade1-selected-slp-v2.yml` | final bytes/lines/SHA-256 returned out of band after reply pinning |
| `sol/luna_reply_632_r07_task625_static_performance_repair.md` | final bytes/lines/SHA-256 returned out of band after close |

The workflow pins this reply; embedding the reply's own final digest would
change both files.  Their exact final values are returned together in the
completion handoff.  The historical Task625 reply and all v1/theorem/audit
files were not edited.

## Remaining risk and claim boundary

The real support sizes, interned-path population, state-edge traversals, leaf
count, wall time, and peak memory remain result-dependent.  R1--R4 remove the
identified avoidable work/copy and close the durable-boundary mismatch; they
do not prove that the real payload fits the fixed limits.  Any future resource
terminal remains `UNKNOWN_RESOURCE`, not NONMEMBER.

Production, A0, COMMON, a cofinal lift, fake witness, Ihara counterexample,
and Lean verification were neither run nor established.  No payload or
cross-check numerator was produced.

`R07_TASK625_STATIC_PERFORMANCE_REPAIR_NOT_RUN`
