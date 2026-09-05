# Task943 -- selected-seed one-pivot release review

Verdict: **PASS for the frozen sources below. No outstanding necessary fix.**
`cross_checked=false; verified=false`.

Read the full Tasks 940/943, the complete new producer/checker actual paths
and public constructors, and Task940's handoff. This is static release
review, not a numerical replay. Accepted parent derivations and source-core
lineages remain premises. Root owns workflow review and GHA execution.

## F1. Exact freeze

Read-only file-size and SHA256 observations agree with the workers' freezes:

```text
search/d972_r07_actual_root_seed_materializer_v3.py
bytes: 86643
SHA256: 36cc620bdc1b772a4eb4067f7e5b490dab851fb41213c5cd8a5487855207a332

search/check_d972_r07_actual_root_seed_materializer_v3.py
bytes: 64626
SHA256: eca60918eb943edddc321054f04b8547b3e88e5f7421f4de1e09ea04d7ca2701
```

The draft checker launch-receipt mismatch was raised during review and is
resolved in this freeze: both public constructors serialize `launch.json`.
The completed checker compares independently reconstructed payloads,
instruction, result and manifest bytes, not merely candidate-owned hashes.

## F2. Current selected authority stays attached to the actual row

The pinned run 33954712636/1 authority and chronological first-nonzero stream
select character 0 / seed34 / value 1 at generation 8060, rank 1355. The code does
not reuse seed30's selected support or old root. Ordered Task554 events
include all four old source contributions and every source/target new-block
contribution; count/head are checked before coefficient collection. All
raw-event P1 roots, including cancelled numeric terms, remain referenced.

Both actual paths join the selected raw row's packed hash, support and
direct pairing to the current scalar receipt before subtraction. They
reconstruct the complete P1 subtraction, require all 96776 lower coordinates
zero, then compare the full defect projector to the plain selected slice.
Task712 B, its transpose, the actual current lambda, q and the nonzero
physical pairing are joined. The checker also checks the current saved P1
value fold against the selected scalar.

## F3. Split state, single append and target continuation are correct

The reader uses the immutable 1354 old rows followed by the authenticated
normalized seed30 pivot. Reduction follows insertion order, not numerical
lead order. Literal reductions reference the old instruction roots and the
saved seed30 instruction root through the current base-plus-delta parent.
The new nonzero remainder is normalized with its honest scale and appends
exactly one pivot: rank 1355 to 1356, generation 8060 to 8061. No concatenated
replacement parent state is emitted.

Only the new pivot is applied to the saved current target remainder. The
old target derivation and completed seed30 elimination remain parent
references. In the Separator branch, both implementations directly test the
FINAL functional against all 1354 old rows, the seed30 pivot and the new
pivot, plus the saved current and updated target remainders. The 1356-row
receipt matches that actual sweep; it is not inferred solely from the
intermediate reverse equations. The rho2 pairing is explicitly inherited
through the accepted target derivation, not claimed directly replayed.

## F4. Scope and obvious resource traps

No new producer arithmetic is imported by the checker. Its own accepted
checker lineage and fixed delta reader are explicit. The actual paths keep
one parsed Task554 body at a time, use buffered instruction scans, and
numerically replay only selected P1 support. No historical closure, scalar
orbit, original-target reconstruction or historical selftest is invoked.
The changed-interface canaries include a bad final row; they were inspected,
not executed here. No obvious new resource trap was found.

`ConnectionMemberCandidate` remains a candidate, with exact exponent and
full witness replay explicitly unfinished. Neither this append nor the
seed-only authority is promoted to orbit completeness, grade2/full A0 or a
cofinal result. No third engine, paper oracle or historical rerun is a new
release gate. Root's already planned serial canaries and actual paired GHA
run remain the execution step; this auditor made no commit or dispatch.
