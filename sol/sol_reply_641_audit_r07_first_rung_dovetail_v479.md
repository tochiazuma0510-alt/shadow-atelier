# Sol(max) Task641 reply: first-rung witness/presentation dovetail v479

## Verdict

`PASS`

V479 correctly separates two objects which had previously been packaged
together: the complete, target-independent transition presentation
\(\mathcal P_d\), and the result-dependent selected word \(C_d\).  A
targeted MEMBER ancestry is enough for the latter and for a fresh replay of
the next residual, but it is not evidence that the former has been
exhausted.  Conversely, \(\mathcal P_d\) determines the complete next legal
image but cannot determine the residual of an unspecified representative.

The conjugate-Fox identity and complete eleven-endpoint signature are
degree-independent over the one fixed first-rung quotient.  V479's grade
2--6 width table is exact, its source and physical auxiliary counts remain
correctly typed, and Theorem 5.1 has the right two-parent join.  I found no
source/physical type promotion, old/lower ancestry shortcut,
occurrence-after-aggregation action, hidden target dependency, or
cross-quotient endpoint reuse in the stated scope.

This is a paper scheduling result.  It computes no residual and no MEMBER
terminal.  `verified=false`.

## 1. Exact inputs

The Task641 instruction is 2,895 bytes with SHA-256
`96ec442c428488c5f1378b6f674c1e19c37823ae5bd57dddf0435758efc3e25c`.
The candidate itself authenticates exactly as 12,280 bytes with SHA-256
`df6850c9e7c86a83ade26c37064a7deb38ec3c8d7907b1eec6ff0d5268b22986`.

I recomputed every parent identity in v479's table:

| parent | bytes | recomputed SHA-256 |
|---|---:|---|
| v444 | 9,953 | `705afdc595f21f64356b70469a8444708b8a8c8e6306c218e942863a560ef645` |
| v449 | 1,408 | `0237572f8ee949cdac8129cb9a9dae8c833b00baee2647c0deed194449577ff9` |
| Task555 | 14,309 | `8dcdfbb4825c65bff9698311b735e830c27d39f98405bcfb01af3411d97a2e45` |
| v465 | 9,801 | `b779fca02449a1e4465bf0a29f7da8388f4c2e32c28a6f959e8c50189f2c7693` |
| v469 | 8,865 | `bae6864e6f00f65bfd3ff18a4c5676d5afe190ad0f2c6ffaf83cd9683d3f26f6` |
| v470 | 8,731 | `b56aa15ee87b4831cc999525233cfadbe8e62cd25c0503c0c98fce3106fb2b7a` |
| v471 | 8,819 | `38d271514baf838953b6003f954be60c689771f0fd1c9fec14de1dfc55daf99f` |
| v474 | 12,755 | `a0ae668799de33d79b5e80ca2a6b7b50224770528b1201d8fb999506757c08c9` |
| v478 | 5,131 | `a7e5df7f14d35b7dc971127e187fbc16abe00b3b5190fac341666b94bbf1e72b` |
| Task639 | 10,104 | `b48fe4bfb43aedb76c9109e2ca73e7a9de323687c69c64807e74f3ad62db0a1b` |

All ten pins pass.  I also read the incorporated v477 statement and the
load-bearing v441/v451 statements used in Theorem 5.1 and the present
grade-one instantiation.  No implementation, production computation, GHA,
or git operation was used.

## 2. The two genuine dependency branches

V444's theorem starts from an exhausted basis of the complete legal
occurrence module, all 44 seed reductions, and all four actor transitions
for every basis row.  Lifting those equalities produces the seed and
transition defects, and exhausting their legal actor closure gives

\[
 U_d=\operatorname{span}(\widetilde B_{d-1})
       \oplus H^{[d]},\qquad
 H^{[d]}=H^{\mathrm{v444}}_{d-1}.
\]

Every datum on the right is fixed by \(\mathcal P_{d-1}\), the seed roster,
the four source actors, the occurrence maps and the filtered quotient.  No
target, residual, selected coefficient, or chosen correction occurs.  The
new seed reductions and the four transitions of the new defect-basis rows
are obtained from the same exhausted closure, so this produces the complete
\(\mathcal P_d\), not merely a basis useful for one target.  V449 applies
Task555's required index repair exactly.

The other branch begins with an accepted selected MEMBER ancestry.  V474's
MEMBER terminal is existential: every row used in the successful span has
authenticated connection/defect/orbit ancestry, and back-substitution gives
one exact literal instruction tree.  It need not have exhausted unused
primal orbit rows.  After the v465/v469 gates require zero complete physical
lower/auxiliary image and the exact grade-\(d\) row, that tree supplies
\(\Delta C_d\) and the noncommutative root

\[
 C_d=\operatorname{Compose}(C_{d-1},\Delta C_d).
\]

Evaluating this exact chosen word one grade higher determines
\(\rho_{d+1}\).  V465 Corollary 2.3 shows why its exact representative is
load-bearing: a different word with the same grade-\(d\) class may change
the next residual.  Completion of unused rows of \(\mathcal P_d\), however,
cannot change that replay and is not an input to it.

Thus, after the grade-\(d\) MEMBER result, the actual dependency graph is

```text
accepted P_(d-1)  ---> complete target-independent P_d ----+
accepted C_d      ---> fresh replay rho_(d+1) -------------+--> grade-(d+1) join
```

The two arrows may execute concurrently.  The join may not omit either
output: without \(\mathcal P_d\) a targeted span may miss legal correction
rows, while without the replayed \(\rho_{d+1}\) it may decide the residual
of a different representative.  This proves precisely the dependency claim
of Theorem 5.1.

## 3. Source/physical and ordering audit

The possible mixed-ancestry counterexample is blocked.  V465's pure source
grade theorem applies only to origins already known to lie in \(F^d\).
V469 instead treats a lower-killed old connection by two direct physical
equalities: its full lower/auxiliary row is zero and its grade row equals the
stored offer.  V479 uses the latter licence for the selected word and does
not infer source-filtration membership from physical cancellation.

Likewise, a v474 targeted MEMBER row is not promoted to an exhausted source
presentation.  Its ancestry proves that the selected row is legal; it says
nothing about all unselected seed/transition orbits.  V479 explicitly
requires those closures in the separate presentation block.

The endpoint formula is applied occurrence by occurrence before physical
aggregation.  The complete signature retains six typed E3 slots and five
typed E4 slots, including the repeated coordinate-zero slots as distinct.
The first-six operation is only the typed restriction
\(E_3^6\times E_4^5\to E_3^6\), after all eleven endpoint gates and the
direct all-seven canary.  Prefixes and signs remain outside the unsigned
signature and act in the v477/v478 occurrence-first order.  No common actor
on an aggregated row is introduced.

## 4. Degree-independent Fox/signature theorem and trie boundary

For any group homomorphism used in one registered occurrence, endpoint one
gives the exact group-algebra identities

\[
 D(Pr_sP^{-1})=\eta_j\theta_j(P)D(r_s),\qquad
 D(Pr_s^{-1}P^{-1})=-\eta_j\theta_j(P)D(r_s).
\]

They precede truncation, so the proof does not depend on which one of the
degrees 0--6 is retained.  Grouping a finite sum by equality of the complete
typed value

\[
 \Sigma_{11}(P)=(\eta_j\theta_j(P))_{j=1}^{11}
      \in E_3^6\times E_4^5
\]

is therefore exact at every degree of the fixed first-rung group algebra.
What changes with \(d\) is the selected word/leaf map and the truncated seed
rows, not the algebraic lemma.

An accepted prefix trie is only a derived evaluator.  Adding new paths and
mod-three coalescing equal `(seed,path)` or `(seed,signature)` keys neither
deletes nor identifies any edge of the ordered source DAG.  Reuse of an old
path endpoint is licensed only because the eleven occurrence maps and the
first-rung quotient are unchanged.  At a changed quotient or refinement,
the endpoint-one gates, signatures, trie evaluations and seed rows require a
fresh receipt; v479 supplies no second-rung or cofinal reuse theorem.

### Task640 compositional-acceptance decision

There is **no mathematical need** for both Task640 executables to duplicate
the already accepted, roughly thousand-line Task625 graph-to-leaf traversal.
The following finite compositional contract is sufficient:

1. bind the exact Task625 manifest, source graph/ancestry, three roots and
   `R07LEAF1` bytes, the exact parent-checker executable, its uploaded
   verdict, and the Task639 acceptance reply;
2. in the workflow, hash the exact parent checker, rerun it against the exact
   Task554/Task595 parents, and require byte equality with the uploaded
   verdict before either consumer runs;
3. have the Task640 producer and its independent checker each stream-parse
   `R07LEAF1` themselves, including its ancestry binding, strict key order,
   coefficient and letter syntax, free reduction, record lengths and exact
   EOF;
4. have both independently reconstruct the registered prior
   \(C_{<1}\), preserve `C_1=Compose(C_<1,C_T)`, check every current endpoint
   gate/all-seven canary, and independently recompute the trie/signatures,
   lower and top dense rows, target difference and packing; and
5. fail closed on any parent hash, root, leaf, checker, verdict or Task639
   mismatch.

Under those gates, Task639 plus the rerun parent checker is the accepted
proof of the exact `C_T` graph-to-`R07LEAF1` equation.  Re-proving that same
parent equation inside each child is redundant, just as re-running any other
accepted parent theorem inside every consumer would be.  The shortcut covers
only that authenticated equation: it does not waive reconstruction of the
2,622-term prior root, any endpoint/dense arithmetic, or producer/checker
independence downstream.

The source graph remains bound as the authoritative noncommutative witness;
the leaf stream is used only as its accepted evaluation projection.  Hence
this compositional acceptance is not source-witness replacement, graph
pruning, refinement naturality, cofinality, or permission to reuse a
current-quotient endpoint receipt elsewhere.

## 5. Independent width recomputation

From

\[
(h_0,\ldots,h_6)=(1,3,6,7,6,3,1)
\]

the cumulative values are
\(H_0,\ldots,H_6=(1,4,10,17,23,26,27)\).  Substitution into v479 (4.2)
gives:

| fresh grade \(e\) | \(h_e\) | \(H_e\) | \(H_{e-1}\) | source through \(e\) | physical lower/auxiliary | physical top | packed top bytes |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 2 | 6 | 10 | 4 | 241,928 | 32,260 | 48,384 | 12,096 |
| 3 | 7 | 17 | 10 | 411,272 | 80,644 | 56,448 | 14,112 |
| 4 | 6 | 23 | 17 | 556,424 | 137,092 | 48,384 | 12,096 |
| 5 | 3 | 26 | 23 | 629,000 | 185,476 | 24,192 | 6,048 |
| 6 | 1 | 27 | 26 | 653,192 | 209,668 | 8,064 | 2,016 |

Every entry agrees.  The arithmetic is

```text
source through e         = 24,192 H_e + 8
physical lower/auxiliary =  8,064 H_(e-1) + 4
physical top             =  8,064 h_e
packed top bytes         =  2,016 h_e
```

The `+8` are the registered source auxiliaries; the `+4` are the distinct
physical lower auxiliaries.  Neither is multiplied by a Hilbert
multiplicity.  The five pentagon endpoints are retained typed source/all-
seven receipts, not extra rows in the present PB4-dropped physical target.
The displayed numbers are coordinate widths, not ranks, closure sizes, RSS,
or evidence of MEMBER.

## 6. Present instantiation and claim boundary

Task639 accepts exactly the grade-one selected `C_T` graph/leaf parent.  It
contains no rho2 and retains `next_degree2_residual=null`,
`cross_checked=false` internally as its self-promotion guard, and
`verified=false`.  Task640 exists only as an implementation commission; no
Task640 reply or successful output is present.  V479 accurately says that
the consumer is in progress and is merely intended to emit the fresh
48,384-trit rho2 after its 32,260-coordinate lower/auxiliary gate.

The prepare/four-block material and v451 determine the independent
grade-two presentation-side input.  V474 becomes a legal targeted decision
only after the accepted rho2 and complete presentation-side product meet at
the join.  It has not run.  Even a later v474 MEMBER would supply one
selected `C_2`, not a complete \(\mathcal P_2\); that completion remains the
other branch needed before grade three.

Accordingly:

```text
Task639 selected grade-one SLP parent:    ACCEPTED
Task640 fresh-rho2 consumer:              IN PROGRESS / NO RESULT
rho2:                                    NOT YET ACCEPTED
grade two and grades three--six:          NOT DECIDED
complete first rung / order 54,432:       NOT DECIDED
second rung / full Q0 / cofinal lift:     NOT DECIDED
COMMON / FAKE / IHARA:                    NOT DECLARED
verified:                                 false
```

The v220 ledger therefore does not change: the first rung remains **1/6
cross-checked**, and A0 remains **0/1 actual**.  No numerator is increased.

`R07_FIRST_RUNG_WITNESS_PRESENTATION_DOVETAIL_V479_AUDIT_PASS`
