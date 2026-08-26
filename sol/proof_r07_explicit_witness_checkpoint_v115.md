# R07 explicit-lift-to-witness checkpoint v115

Author: Sol / 2026-08-27

Status: non-repeating frontier after v105--v114.  This note fixes what is
proved, what the running computations decide, and the shortest remaining
route from g760 to an explicit cofinal lift.  It supersedes no negative or
positive machine receipt.  No fake or Ihara witness is declared.

## 1. Fixed objects

The current explicit base is

\[
 \boxed{g_{760}=w_2(w_3^{-1}w_2)^8y^{36}x^{-108}}
\tag{1.1}
\]

with freely reduced length \(760\), exponent sums \((0,0)\), and signed-word
SHA-256

```text
518f09820b8d7baee6b58ebf366cebf7b02a9a945cd1350cf8c701a4e6bc2b4d
```

It is the fixed descendant of the explicit first lift

\[
 f_1=y^\nu x^{-\nu}w_1(m_1=0).
\tag{1.2}
\]

The correction convention is right multiplication.  If \(\beta\) is the
base defect and \(D(c)\) is corrected minus base, the equation is

\[
 \boxed{\beta+D(c)=0.}
\tag{1.3}
\]

No later implementation may silently reverse this sign.

## 2. What j=9 through j=12 seek

Let \(P=\Pi_4[3]\), \(\Lambda=\mathbf F_3[P]\), and \(I=I(P)\) be the
augmentation ideal.  At Jennings depth \(j\), the target6 calculation works
in

\[
 \Lambda/I^j.
\tag{2.1}
\]

Increasing \(j\) retains more radical layers.  Thus \(j=9,10,11,12\) are
four increasingly fine necessary tests for the **same fixed g760 first
hexagon defect**.  They are not searches for four different words and are not
four GT relations.

At each depth the producer asks whether

\[
 t_j\in
 \operatorname{im}D_{2,j}^{\rm full}
 +\operatorname{span}(L_{j,1},\ldots,L_{j,28}),
\tag{2.2}
\]

where the 28 rows are the registered C-13 legal overapproximation.  If (2.2)
fails, the pinned g760 lane dies already in that quotient.  If it holds, one
must retain the complete affine coefficient family

\[
 \mathcal A_j=
 \{a\in\mathbf F_3^{28}:
 t_j-L_j a\in\operatorname{im}D_{2,j}^{\rm full}\}.
\tag{2.3}
\]

A Boolean `nonmember=false` reports only (2.2).  It does not identify a legal
word and is not an A.18 lift.

The immutable GHA evidence currently fixes:

```text
j=9: 11/11 D2 relators complete; rank 19,621; nonmember=false
j=10: relators 1..7 complete; rank 29,143; no terminal decision
j=11: not started
j=12: not started
```

Run `32972580814` and v105 are the source of these numbers.  Because its
artifact was not uploaded, the integrated coefficient extraction must
recompute j=9 once; it must not recompute j=9 a second time inside the same
future invocation.

## 3. Fixed paper results which are not to be reopened

1. V98 constructs compatible ordinary-word spellings from compatible
   correction values in the accumulated kernels.
2. V99 proves the structural affine linearization, literal closedness, and
   residual/Jacobian base-change statements formerly called structural HT1,
   HT2, and HT5.
3. V108 proves that the frozen eleven-relator PB4 presentation boundary is
   the true PB4 boundary.  It does **not** assert
   \(\ker D_1=\operatorname{im}D_2\).
4. V109 proves the exact full-context orbit-image criterion for target6.
5. V110 stacks both hexagons and the five ordered A.18 coface evaluations and
   proves the one-common-word criterion.  Five cofaces form one
   noncommutative pentagon equation.
6. V111 proves the filtered Neumann formula

   \[
   h=s\sigma\sum_{r\geq0}(1-B\sigma)^r
   \tag{3.1}
   \]

   once a filtration-raising actual-class splitter is supplied.  It also
   proves the cyclic annihilator test

   \[
   Ba=z,\qquad\operatorname{Ann}(z)a=0.
   \tag{3.2}
   \]

7. V112 removes return parity and every authenticated prime-to-three context
   symmetry by Reynolds averaging.  A return-even survivor defeats the pure
   \(1-\theta\) formula but is not itself a lift obstruction.
8. V113 compresses the remaining three-primary stabilizer equations to norm
   orbit columns, while retaining every extra linear annihilator relation.
9. V114 proves the modular norm-transfer warning: fixed-context Jennings
   lifting and growing-context cofinal naturality are distinct.  If a
   persistent nonzero invariant class crosses a quotient with nontrivial
   three-kernel, a fully equivariant natural splitter is too strong; a based
   actual-class selector is then required.

These are paper proofs.  They are not Lean-verified, and none asserts the
missing R07 membership calculation.

## 4. The two running bridges

### 4.1 Task 169: legal coefficient to actual registered word

For each completed \(\mathcal A_j\), task 169 computes the word-bearing
subspace

\[
 B_{\rm legal,value}
 =B_{\rm joint}\cap\ker(\operatorname{exp}_3)
\tag{4.1}
\]

coming from the exact registered joint kernel

\[
 \ker(F_2\to Q_0\times E_3\times E_4^{31}).
\tag{4.2}
\]

It then computes

\[
 \mathcal A_j^{\rm joint}
 =\mathcal A_j\cap B_{\rm legal,value}
\tag{4.3}
\]

and, if nonempty, materializes an actual signed \(F_2\) correction word.  The
full affine family and its kernel basis must be retained; a lexicographic
point alone is insufficient for the later seven-evaluation intersection.

### 4.2 Task 172: full-E4 orbit input authentication

Task 172 repairs the rejected task-171 preflight.  It must bind the actual
full-E4 operations, all 26 record words, the complete
\(6318+104+19\) relation roster, the three target6 contexts, and the eleven
raw PB4 presentation rows.  Its semidirect-product toy must compare a genuine
normal-relator orbit image with a genuine cocycle image; self-comparison and
hard-coded mutations are forbidden.

Neither task is a mathematical lift.  Together they make the first honest
full-E4 word-bearing orbit solve executable.

## 5. Shortest decision path after the bridges

The next parent GHA invocation must run serially and return, in order:

1. authenticated j=9 full-D2 completion;
2. the complete \(\mathcal A_9\), not only membership;
3. the task-169 intersection \(\mathcal A_9^{\rm joint}\); and
4. an actual word with direct value, exponent, projected-Sigma, and D2 replay
   if that intersection is nonempty.

If the intersection is empty, the result is negative only for this pinned
base, projected target6, and registered exact joint-value domain.  If it is
nonempty, its word-bearing coefficient provenance is used to seed and audit
the authenticated full-E4 target6 orbit system; the projected 28-coordinate
family is not silently identified with the full-E4 orbit domain.  A positive
full-E4 target6 result then enters the v110 stack:

\[
 (H_1,H_2,P_{A18})
\tag{5.1}
\]

with one coefficient vector and one correction word for all blocks.

Depths 10--12 remain useful stronger fatal screens, but they need not delay
the higher-information actual-domain/full-E4 positive branch once j=9 has
returned a word-bearing family.  If that branch fails for a convention or
typing reason rather than by a sound empty certificate, resume j=10 from its
recorded relator-8 frontier instead of rerunning j=9 blindly.

For a positive stacked result, the receipt must additionally compute the
actual context orbit of the stacked defect \(z\), its stabilizer, and its full
annihilator.  It must solve

\[
 \boxed{Ba=z,\qquad\operatorname{Ann}(z)a=0}
\tag{5.2}
\]

using v112--v113 compression.  This is the first finite candidate for the
return-even homotopy \(h_{\rm orb}\), not merely one corrected word.

## 6. From a stacked word to a cofinal witness

Even after (5.2), four genuinely different gates remain.

1. **Fixed-context radical lift.**  Show the lifted splitter raises Jennings
   filtration and apply (3.1) through the terminating fixed \(P\)-radical.
2. **Context-changing transitions.**  Apply the v114 receipt.  Use an
   equivariant selector only when its transfer is legal; otherwise construct
   a based actual-class selector in the v98 accumulated kernel.
3. **All side gates.**  Replay marking, exact commutator, relative formation,
   charmingness, descent, onto, and settlement on the materialized words.
4. **Nonabelian chief edges.**  Prove every accepted set encountered by the
   matched ladder is nonempty and interleave those corrections with the
   abelian recursion.

Only after these four gates does the convergent profinite product give one
compatible cofinal R07 lift.  Only after its roof value is tied to a named
nonarithmetic element may it be promoted to a fake/Ihara witness.

## 7. Frozen ledger

```text
EXPLICIT g760 BASE:                           FIXED
j=9 PROJECTED TARGET6 FATAL SCREEN:           SURVIVED (candidate producer)
j=9 ACTUAL AFFINE COEFFICIENT FAMILY:         AWAITING INTEGRATED GHA
REGISTERED JOINT-VALUE WORD INTERSECTION:     TASK 169 RUNNING
FULL-E4 ORBIT PREFLIGHT:                      TASK 172 RUNNING
TRUE PB4 PRESENTATION BOUNDARY:               PAPER_PROOF (v108)
ONE-WORD ALL-SEVEN ORBIT CRITERION:           PAPER_PROOF (v110)
FILTERED ACTUAL-CLASS HOMOTOPY FORMULA:       PAPER_PROOF (v111)
RETURN / 3'-SYMMETRY REDUCTION:               PAPER_PROOF (v112)
3-PRIMARY STABILIZER COMPRESSION:             PAPER_PROOF (v113)
COFINAL NORM-TRANSFER BOUNDARY:               PAPER_PROOF (v114)
FULL-E4 TARGET6 WORD:                         NOT YET CONSTRUCTED
ALL-SEVEN COMMON CORRECTION WORD:             NOT YET CONSTRUCTED
ACTUAL h_orb:                                 NOT YET CONSTRUCTED
ALL-EDGE SIDE GATES / NONABELIAN NONEMPTY:    OPEN
COMPATIBLE COFINAL R07 LIFT:                  NOT CONSTRUCTED
FAKE / IHARA WITNESS:                         NOT DECLARED
```
