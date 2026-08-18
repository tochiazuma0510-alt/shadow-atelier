# Luna task 157cx — semantics-preserving row18 producer acceleration

## Scope and non-regression boundary

The active terminal GHA run is `32090719159` at commit
`9832127ee234b5d978a8ae4a794b293b8e0abdc4`.  It remains authoritative and
must not be cancelled.  It has spent about 40 minutes in the exact producer.
This task prepares a faster same-gate contingency while that immutable run
continues.

Do not reopen or re-audit any mathematics.  In particular, do not change the
fixed zero-based row 18, its arithmetic-outside status, the literal A.18
relations, the C2^24 basis, the B4 action certificate, settlement, the frozen
cofinal compactness theorem, or the terminal implication to B4-B.  This task
may change evaluation order and cache repeated values only.  Every accepted
solution and every terminal status must be exactly the same as in the current
producer.

Do not run GAP, a heavy Python computation, Git, or GitHub Actions locally.
You may perform lightweight source syntax/static checks only.  Parent Sol is
the sole Git/GHA broker.

## Authorized files

Modify only:

- `search/d972_b4_literal_row18_stage_v1.g`
- `.github/workflows/d972-b4-literal-row18-stage-v1.yml`
- `sol/luna_reply_157cu_literal_row18_stage_impl.md`

Create only:

- `sol/luna_reply_157cx_row18_exact_acceleration.md`

Do not touch the independent checker; it must replay the accelerated
producer receipt unchanged.

## Required repair

1. Add flushed, deterministic phase markers with `Runtime()` around at least:
   core reconstruction, fp/Artin action, literal A.18 relation closure, each
   power's 64-correction fibre, and settlement.  Markers are diagnostics only
   and must not enter the mathematical receipt or terminal decision.
2. In the two-power × 64-correction loop, preserve exhaustive enumeration but
   evaluate the cheap exact gates first.  Cache the candidate evaluations in
   E and G9.  Call the two expensive `Size(Group(...))` onto checks only if
   all already-computed necessary gates (transport, exact roof, charming,
   hexagons, pentagon/relation coefficient) pass.  A candidate skipped by
   this short circuit must be recorded logically as `onto_E=false` and
   `onto_G9=false`, and cannot enter the solution list.
3. Do not weaken either onto gate, the lossless relation correction, or the
   final settlement quotient/bijectivity checks.  Do not stop at the first
   solution: the existing exhaustive solution count and preferred exponent-1
   selection remain unchanged.
4. Cache repeated word evaluations where this is mechanically safe, without
   changing word order, GAP multiplication convention, or GT composition.
5. Keep the 100-minute process bound and 110-minute job bound.  Update only
   the producer SHA pin in the workflow (and any exact reply hash accounting
   forced by that change); all frozen input and checker pins remain unchanged.
6. State explicitly in the reply why the short circuit is logically
   equivalent, list every modified evaluation site, give final SHA-256 values,
   and finish with exactly one marker:

   - `ROW18_EXACT_ACCELERATION_READY_FOR_GHA`, or
   - `ROW18_EXACT_ACCELERATION_BLOCKED`.

The goal is lower wall time for the identical terminal finite gate, not a new
theorem and not a weaker candidate search.
