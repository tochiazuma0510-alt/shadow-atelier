# R07 all-seven bridge checkpoint v123

Author: Sol / 2026-08-27

## Verdict

The corrected task-173 static inventory is accepted.  Its two mathematical
STOP gates are now closed:

```text
PB3-PRES-EQ                         COMPLETE by v121
E3-CONTEXT-KERNEL-BRIDGE            COMPLETE by v122
executable E3 retraction replay     bounded implementation duty
all-seven raw preflight             GO
all-seven orbit/stacked solve       NOT RUN
literal common correction           NOT CONSTRUCTED
cofinal lift / fake / Ihara witness NOT DECLARED
```

This checkpoint supersedes the task-173 statement that the two named gates
are open.  It does not alter task 173's word formulas, occurrence inventory,
typing rules, canary requirements, or claim boundaries.

## 1. Accepted inventory

Task 173 correctly fixes the all-seven target as one common correction word
used in:

1. the first source-E3 hexagon;
2. the second source-E3 hexagon;
3. all five ordered E4 pentagon occurrences.

The resulting sparse target has three noninterchangeable blocks, H1/E3,
H2/E3, and P/E4.  Context equality never permits cancellation across block
tags.  The pentagon order remains

\[
b_1b_2b_3b_5^{-1}b_4^{-1}.
\tag{1.1}
\]

The corrected shelf table also properly treats task-172 v2 as historical and
task-172 v7/v119 as the current, narrowly promoted target6 raw bridge.

## 2. Closure of the presentation gate

`sol/proof_pb3_two_relator_presentation_equality_v121.md` proves that the two
frozen relators present the marked group \(P_3\).  It gives both:

- the explicit Tietze form
  \(\langle b,c,t\mid[b,t],[c,t]\rangle=F_2\times\mathbb Z\); and
- an independent split-presentation proof through the exact PB4 eleven-row
  presentation v108.

Therefore the two PB3 Fox columns and every left translate form the true
presentation \(D_2\) image.  The all-seven successor must pin v121 and may
mark this gate exact; it must still reconstruct and check the two raw columns.

## 3. Closure of the source-context gate

`sol/proof_r07_e3_context_kernel_retraction_bridge_v122.md` uses the actual
endpoint coface 4 and fourth-strand deletion.  On the two matched factors it
constructs

\[
d_E:Q_4\times\Pi_4[3]\longrightarrow Q_0\times\Pi_3[3]=E_3,
\qquad d_Ei_E=1.
\tag{3.1}
\]

The task-157ee joint registry already includes the coface-4 images of all five
source pairs at IDs 21--25.  Applying \(d_E\) proves that its registered joint
kernel is contained in all five source-E3 evaluation kernels.  No new joint
group with four redundant E3 factors is mathematically necessary.

The selected q=3 JSON omitted the map bundle on its positive branch.  Hence
the successor must reconstruct (3.1), validate it on marked generators, and
map blobs 21--25 back to their E3 blobs.  This is a fail-closed executable
input check, not a remaining theorem choice.

## 4. Frozen forward path

The next steps are fixed in this order:

1. build and independently check the bounded all-seven raw preflight from
   task 173, with v121/v122 as pinned theorems;
2. compute the actual all-seven orbit image and solve the one stacked affine
   membership problem;
3. materialize one word-bearing common correction and replay H1, H2, and the
   ordered pentagon directly for the same corrected word;
4. only then promote an explicit q=3 finite-stage lift;
5. use the adaptive one-path theorem v117 and the later-stage lifting
   mechanism to address a cofinal compatible family.

A target6-only solution, a quotient-value correction without a word, or a
zero in a projected module does not skip any step above.

## 5. Parallel finite computations

Task 169's first local preflight stopped after 618,272 ms at
`ResourceStop: relation_roster_wall_seconds_cap`; it produced no artifact and
no rank.  Its transition-cache successor is untested and must not be described
as a result.  After source audit it belongs on GHA, not another long local
Python run.

Task 174 is the separate target6 context-image census.  It can sharpen the
finite image and kernel sizes, but it neither replaces the all-seven stack nor
closes a cofinal theorem.

## 6. No-backtracking ledger

```text
v108  PB4 eleven-relator presentation equality       CLOSED
v119  target6 raw bridge, bounded narrow promotion    CLOSED FOR SUCCESSOR USE
v120  extension-section context census reduction      CLOSED AS THEOREM
v121  PB3 two-relator presentation equality           CLOSED
v122  source-E3 context-kernel containment             CLOSED AS THEOREM
169   joint coefficient intersection preflight         RESOURCE STOP, NO RESULT
174   target6 context-image census                      STATIC, NOT EXECUTED
175   all-seven raw bridge preflight                    NEXT IMPLEMENTATION
```

No later audit should reopen v108, v121, or the mathematical containment in
v122 unless it supplies a specific counterexample to a displayed marked map
or equation.  Executable serialization failures remain `UNKNOWN_INPUT` and
must be repaired without downgrading the proved group-theoretic statements.
