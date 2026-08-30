# Luna task 411 — R07 A0 compact pc/invariant owner v1

Role: Luna implementation and bounded fixtures only.  Do not do new
mathematics, run heavy local production, commit, push, dispatch GHA, edit a
workflow, or touch pre-existing files.

The mathematical contract is frozen in:

- `sol/proof_r07_a0_occurrence_quotient_invariant_span_v396.md`;
- `sol/proof_r07_compact_extension_presentation_a0_seed_reduction_v397.md`;
- v220 Deltas 270--271.

Implement that route directly.  Do not resume, copy, or reinterpret the old
1.66 GB adaptive checkpoint.

## 1. Required versioned outputs

Create only:

1. `search/d972_r07_a0_compact_pc_invariant_owner_v1.py`;
2. `crosscheck/check_d972_r07_a0_compact_pc_invariant_owner_v1.py`;
3. `search/d972_r07_a0_compact_pc_invariant_owner_gha_driver_v1.g`;
4. `sol/luna_reply_411_r07_a0_compact_pc_invariant_owner_v1.md`.

The producer may import/hash-pin frozen owners, but the checker must rebuild
the finite presentation and final membership from public input receipts with
helper code not shared with the producer.

## 2. Pinned mathematical inputs

Authenticate at least:

```text
ci/b345_157ee_artifacts_32359956713/
  d972_b345_joint_kernel_qstar_closure_v1.json
bytes  = 2166036
sha256 = 1c3ad7a7124cee152eb40968cf212c14641a9f8720063c85f70533864898d0df

ci/in/d972_r07_seven_context_roof_presentation_v1.json
bytes  = 31017244
sha256 = 82f7955580039f2a0271896c928515d26996f636d8e73231331da6a37f6b19f5

ci/in/d972_r07_seven_context_roof_presentation_v1.acceptance_v2.json
bytes  = 2722
sha256 = cc8c16c8ad8f2d094868f0897bcca2a98adba75c18bf7ff397f0da67fd233ea4
```

Also pin the exact task179/task176 physical all-seven evaluator and the
registered `g760` owner used by
`search/d972_r07_crel_occurrence_closure_v3.py`.  That file is a useful ABI
example for the eleven separately tagged occurrences and their four signed
actors; it is not authority for the new theorem and its verbose transition
receipt must not be copied.

## 3. Deterministic compact roof presentation

From the authenticated 243-state Gamma multiplication/transition data:

1. deterministically construct a subnormal pc sequence of length five with
   relative orders three;
2. choose each pc element's literal source representative from products of
   the authenticated 26 Q0-identity correction records;
3. collect and emit at most five power and ten conjugation relations;
4. collect the conjugates by marked `x` and `y`, emitting ten action
   relations (one orientation only, as proved in v397);
5. collect the 19 authenticated Q0 defects and emit their adjusted relations;
6. Tietze-substitute literal source words for all auxiliary pc generators.

Require `compact_relator_count <= 44`.  Each literal relator must replay to
the identity in the accepted task198 seven-block roof.

Prove presentation completeness mechanically without expanding the 357M roof:

- enumerate/check the pc normal forms and exact Gamma order 243;
- check the marked action table and all 19 defect endpoints;
- use the v397 finite-order bound with the already accepted Q0 order and roof
  bridge;
- stream all 6,441 old relator occurrence vectors into the invariant span of
  the compact roster as the expensive-direction equivalence oracle.  Do not
  retain all 6,441 rows or words in memory.

No search over pc presentations is allowed.  Use a deterministic composition
series / first admissible source representative and report its digest.

## 4. Exact A0 occurrence closure

Keep all eleven Fox occurrences separate until physical aggregation.  Build
the correction image exactly as v396:

```text
seed J(r), r in compact roster (<=44)
close retained rank-raising rows under x, x^-1, y, y^-1
aggregate only through the authenticated physical L_g
```

Build the complete typed boundary independently from its fifteen seeds:

- two PB3 presentation relations for H1;
- two PB3 presentation relations for H2;
- eleven PB4 presentation relations for P;
- close under all signed marked PB generators as specified by v396.

Decide the exact finite membership `-T in D + L_g(W)`.  On MEMBER, retain a
compact seed/action/product ancestry DAG and output a literal mod-three common
correction plus a typed boundary preimage.  Apply the frozen v156/v265
exactifying-relator rule and selected-support replay before using a positive
terminal; require exact integer exponent sums `(0,0)`.  On NONMEMBER, emit it
only after both compact closures are exhausted and the independent checker
reproduces the same separating functional.  Resource exhaustion is typed
`UNKNOWN_RESOURCE`, never NONMEMBER.

The two exponent rows are the v156 normalized lattice coordinates, not raw
exponent sums modulo three.  For every correction seed require

```text
epsilon(word) in 18 Z^2
normalized row = (epsilon_x/18, epsilon_y/18) mod 3.
```

The four conjugation actors copy these two coordinates unchanged; all PB
boundary rows and the target carry zero.  Raw `epsilon mod 3` is identically
zero on the joint kernel and is not an acceptance gate.  A MEMBER word has
exponent `(54A,54B)` and must be exactified using the authenticated v156
words `v0=r9*r12*r3^-2`, `u0=r9*v0^-8`, followed by direct replay of exact
integer exponent `(0,0)` and the unchanged all-seven boundary class.  The
governing correction is
`sol/proof_r07_a0_normalized_exponent_lattice_repair_v399.md`.

## 5. Speed and memory are simultaneous requirements

The production owner must not reduce memory merely by serializing the whole
calculation.

- One central reducer owns only compact sparse pivots and the minimal
  ancestry/action DAG.
- Create worker processes before loading any large reducer state, or use
  spawn-based workers whose payload is only immutable action tables plus a
  bounded batch of sparse frontier rows.  A worker must never inherit/copy the
  owner echelon, old checkpoint, full ancestry dictionary, or historical
  transition log.
- Parallelize the four signed actions and independent H1/H2/P boundary
  closures.  Central reduction remains deterministic in preregistered order.
- Store no per-failed-row reduction trace, no complete transition roster, no
  historical dual columns, no global conjugator roster, and no 6,441-row
  cache.  Positive ancestry is a hash-consed DAG; dependent candidates leave
  only counters/digests.
- Checkpoint after bounded rank/frontier batches with atomic replacement.  A
  checkpoint contains compact pivots, frontier cursor, action tables' hashes,
  and live ancestry nodes only.  Resume must be exact and progress logging
  must expose phase, seed ordinal, rank, frontier cursor, RSS and elapsed time.
- Put hard RSS checks on owner and workers separately.  The implementation
  design must keep total RSS under the GHA 5.7 GB contract without counting
  sampled parent-plus-child peaks as available memory.

### Narrow hot-path density/copy gate

This gate is mandatory but must remain small.  In the existing production
hot path, expose per phase: current/max row `nnz`, total pivot `nnz`, frontier
`nnz`, serialized worker-batch bytes, owner RSS, and each worker RSS.  Inspect
the actual task payload and process start method.  A worker must receive only
bounded sparse frontier rows and immutable action data, never the pivot map,
reducer, ancestry store, checkpoint, or a closure capturing them.

Fix only a confirmed/local issue: remove whole-row or whole-basis copies,
delete zero coefficients immediately after mod-three arithmetic, avoid
retaining dependent-row traces, and intern coordinate identifiers only if
string-key duplication is an observed or direct hot-path cost.  If rows stay
sparse and payloads are bounded, record that fact and do not redesign.
Do **not** add a profiling framework, database, alternate algebra backend,
custom allocator, GPU path, extra mutation campaign, or separate preliminary
phase.  These counters belong to the normal progress line and cannot delay
useful production.

The producer should begin useful production immediately; do not put SELFTEST,
SAT, mutation campaigns, or full legacy replay ahead of the compact closure.
The old 6,441 streaming oracle may run after a candidate/exhausted span exists
and must be resumable by row ordinal.

## 6. Bounded local gates

Run only compile/help/hash-pin/GAP-parse and a tiny synthetic finite-extension
fixture.  The fixture must show:

- Cayley presentation and compact pc presentation have the same normal
  closure in the tiny target;
- a compact seed action raises rank once and a duplicate does not;
- owner/worker payload excludes reducer/checkpoint state;
- checkpoint/resume reproduces rank, frontier and ancestry digest;
- one relator, one action endpoint, and one checkpoint node mutation are
  rejected.

Do not run the 243-state extraction, 6,441 replay, or actual A0 locally if it
is more than a bounded few seconds.  Report exact file bytes/SHA-256, commands,
gates, expected GHA command, progress markers, and a realistic memory/runtime
estimate.  If an existing ABI cannot supply one of the fifteen boundary seed
actions, return the exact missing field as a blocker; do not fall back to the
legacy adaptive search.
