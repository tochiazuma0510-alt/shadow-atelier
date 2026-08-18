# Luna reply 157cx — semantics-preserving row-18 acceleration

## Result

The contingency producer is ready for a parent-brokered GHA run.  The active
run `32090719159` was neither cancelled nor altered.  No mathematical gate,
receipt field, terminal status, correction fibre, or settlement check was
changed.  I did not run GAP, Git, GitHub Actions, or a heavy local Python job.

## Exact equivalence of the short circuit

For a fixed candidate, let

```text
C = transport
    AND exact roof
    AND charming
    AND all E/P/G9 hexagons
    AND literal-pentagon relation coefficient exists.
```

The old acceptance predicate was exactly
`C AND onto_E AND onto_G9`.  The accelerated producer first computes every
component of `C`.  If `C` is false it records the two local onto predicates as
`false`; the old conjunction was already false, so that candidate could not
have entered the solution list.  If `C` is true, it evaluates the same two
exact predicates

```text
Size(Group(x, PaperProd([f^-1,y,f]))) = Size(target)
```

with the same generators, multiplication convention, and target group as
before.  Memoization is keyed by the exact GAP group element `f`, in separate
fixed-context caches for `E` and `G9`; a cache hit therefore returns the same
Boolean predicate.  Thus the accepted candidate set is identical.

Both exponent records and every one of their 64 correction values are still
visited.  Gauge-column construction is still performed for every applicable
basis correction before the onto short circuit.  There is no early exit, the
lossless relation correction block is unchanged, total solution counts are
unchanged, and the existing exponent-1-first selection and exact settlement
block are unchanged.  Skipped onto computations have no receipt field for a
rejected candidate, so the receipt schema and independent checker contract are
unchanged.

## Modified evaluation sites

Only the following producer sites changed.

1. `D972LRPhaseBegin`/`D972LRPhaseEnd` now emit deterministic labelled
   `Runtime()` lines through `WriteLine(OutputTextUser(),...)`.  GAP 4.16's
   `OutputTextUser` delivers each character immediately, so these are flushed
   diagnostics.  Begin/end pairs surround `core_reconstruction`,
   `fp_artin_action`, `literal_a18_relation_closure`, each dynamically named
   `power_1_correction_fibre`/`power_2_correction_fibre`, and `settlement`.
   None is inserted into `D972LRReceipt`.
2. `D972LRHexCached` receives the already evaluated `f(x,y)`.  The retained
   `D972LRHex` wrapper has the old semantics.  The three base-hexagon calls and
   the three per-candidate hexagon calls use the cached value; the remaining
   four substitutions and both ordered paper products are unchanged.
3. At each power, the source word is evaluated once in `E`, `P`, and `G9` and
   those exact values are reused by the base hexagons and roof comparison.
4. At each correction value, the candidate word is evaluated once in `E`,
   `P`, and `G9`.  These values are reused by the roof test, hexagons, and onto
   tests.  Pentagon evaluations, masks, coefficient solving, and gauge-column
   construction remain in their original exhaustive order.
5. The fixed target orders `Size(E)` and `Size(G9)` are computed once.
   `D972LROntoCached` contains the single exact onto `Size(Group(...))` site.
   Both onto variables are initialized to `false` and this helper is called
   only inside `if D972LRPreOntoOK then`, after all necessary gates listed in
   `C` have been computed.
6. The workflow change is exactly the producer SHA pin.  The checker and every
   frozen-input pin are byte-for-byte unchanged, as are the `100m` process and
   110-minute job bounds.

The independent checker file was not modified.

## Static audit

Lightweight source assertions confirmed all five required phase regions, both
power records, the literal `[0..63]` loop, absence of an early `break`, the
pre-gate/false-initialization/conditional-onto/final-acceptance ordering, the
single exact onto expression, exponent-1 preference, and the single solution
accumulation site.  All non-producer workflow pins and all three immutable
40-hex action references were rechecked.  PyYAML `BaseLoader` accepted the
workflow, and the 100/110-minute bounds were rechecked.

## Final SHA-256 values

```text
search/d972_b4_literal_row18_stage_v1.g
  18a9ce2fce470cf27b1fd822ab1863a92abb7b9c3e2aaf0bf5144bc4d154f326

search/check_d972_b4_literal_row18_stage_v1.py  (unchanged)
  1c9b9fb4f2c1e331323ec0cd8cf6e46bcac9fd2957780493f02ea3991c4d7649

.github/workflows/d972-b4-literal-row18-stage-v1.yml
  b5f0d6ba799874c3c4133e37a62f6d1eb8473d99906169e28be3aeafd3aafb11
```

`sol/luna_reply_157cu_literal_row18_stage_impl.md` was updated to carry these
new bundle hashes and the evaluation-order note.

ROW18_EXACT_ACCELERATION_READY_FOR_GHA
