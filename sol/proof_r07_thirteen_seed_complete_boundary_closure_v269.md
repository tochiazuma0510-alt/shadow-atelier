# R07 thirteen-seed complete boundary closure v269

Author: Sol / 2026-08-29

Status: paper/interface theorem after v163, v188, v267, and v268.  It proves
that A4's complete translated PB3/PB4 boundary space can be constructed once
by a rank-bounded marked-action queue from the thirteen authenticated base
boundaries.  The independent checker may retain v163's support-inversion dual
algorithm, giving two different completeness proofs.  No actual boundary
rank, A4 kernel, anchor, lift, fake, or Ihara witness is declared.
`verified=false`.

## 1. Typed base boundaries

For each of the two hexagon PB3 blocks and the printed PB4 blocks, retain the
authenticated base boundary rows of v163.  Write the complete typed roster as

\[
 \mathcal B_0=\{d_{b,j}\},\qquad |\mathcal B_0|=2+11=13.
\tag{1.1}
\]

Each row is supported in its own block/component coordinate space.  Equal
group bytes in different types remain different coordinates.  If \(Q_b\) is
the marked finite quotient acting on block \(b\), the complete boundary
space is

\[
 D=\operatorname{span}_{\mathbf F_3}
       \{q\cdot d_{b,j}:q\in Q_b,\ d_{b,j}\in\mathcal B_0\}.
\tag{1.2}
\]

The marked images of the two source letters generate every \(Q_b\).  On the
direct sum of typed blocks, a source letter acts componentwise through its
corresponding marked value.  Since each seed is block-supported, applying one
common source word to it realizes the arbitrary translate by that word's
image in its own \(Q_b\); no diagonal restriction is introduced.

## 2. Complete invariant closure

Let \(D_{\rm q}\) be the following queue closure in the actual typed sparse
row space.

1. Insert the thirteen rows of \(\mathcal B_0\) into one coefficient-bearing
   echelon.
2. Whenever an insertion raises rank, retain its raw base/parent/action
   ancestry and enqueue the normalized row.
3. Apply \(x,x^{-1},y,y^{-1}\) to every dequeued row, reduce against the live
   echelon, and enqueue only a rank raise.
4. Stop only when the queue is empty.

### Theorem 2.1 (THIRTEEN-SEED BOUNDARY CLOSURE)

\[
 \boxed{D_{\rm q}=D.}
\tag{2.1}
\]

If the terminal boundary rank is \(b\), there are exactly \(b\) rank-raising
rows and at most \(4b\) translated action candidates after the thirteen
initial insertions.  No enumeration of any \(Q_b\) is required.

#### Proof

Every inserted row is obtained from a base boundary by a marked source-word
action and linear combination, so it belongs to (1.2).  Thus
\(D_{\rm q}\subseteq D\).

At queue exhaustion, \(D_{\rm q}\) contains every base row and is stable
under the marked generators and inverses.  Hence it is stable under every
word in \(x^{\pm1},y^{\pm1}\).  Their images exhaust each \(Q_b\), so it
contains every translate in (1.2), proving the reverse inclusion.  Every
accepted queue row strictly raises rank in a finite-dimensional space, which
gives termination and the stated counts. \(\square\)

The retained parent/action chain and base-row coefficient vector give an
explicit translated PB3/PB4 boundary preimage for every member of the final
echelon.  All row operations must be applied to that immutable raw ancestry,
as in the task322 correction.

## 3. Exact quotient and independent decision

After Theorem 2.1 finishes, every A4 presentation defect and every translated
K row can be reduced against one fixed complete boundary basis.  Therefore:

- a zero remainder carries an explicit boundary preimage;
- a nonzero target outside the span carries an echelon dual annihilating the
  complete basis; and
- no per-row scan of translated boundaries or dynamic group-state roster is
  necessary.

A helper-nonshared checker can prove completeness by the different v163
support-inversion identity.  Given a dual \(\lambda\), it processes every
base-boundary occurrence and matching dual-support entry, reconstructs the
unique translation \(q=gh^{-1}\), and either finds an active column or proves
that \(\lambda\) annihilates every translate.  Iterating only on strict rank
rises reconstructs the complete checker boundary span.  Two-way containment
of the producer queue basis and checker column-generation basis proves equal
quotients without comparing coordinates from unrelated echelons.

This division is algorithmically independent:

```text
producer:  thirteen seeds -> marked invariant rank closure
checker:   dual support inversion -> active translated columns
```

Both paths retain exact block tags, multiplication convention, and literal
translation ancestry.  A cap before queue exhaustion or complete dual
correlation is `UNKNOWN_RESOURCE`, never NONMEMBER.

## 4. A4 consequence

The task328 actual consumer may replace a repeated lazy boundary query by one
precomputation of (2.1), then use the resulting coefficient-bearing basis for
all 6,441 initial rows, K action rows, basis-change proofs, word-boundary
differences, and the v247 anchor.  Together with v268, its fixed initial work
has the form

\[
 \text{288 primitive word DAG}
 \;\longrightarrow\;
 \text{6,441 defect rows}
 \;\longrightarrow\;
 \text{13-seed boundary closure}
 \;\longrightarrow\;
 K\text{ closure modulo }D.
\tag{4.1}
\]

The order of the middle two independent computations may be exchanged, but a
K row is not certified modulo boundaries until the boundary closure is
complete.  No full Q0 section table, quotient-state enumeration, or repeated
support correlation belongs in the producer hot path.

```text
COMPLETE BOUNDARY BASE SEEDS:                    13 (v163)
INVARIANT CLOSURE EQUALS ALL TRANSLATES:         PAPER PROOF
PRODUCER ACTION CANDIDATES AFTER INITIAL SEEDS:  <= 4b
INDEPENDENT SUPPORT-INVERSION CHECKER:            PAPER PROOF (v163)
ACTUAL BOUNDARY RANK b:                           NOT COMPUTED
ACTUAL K / A4 ANCHOR:                             NOT COMPUTED
LIFT / FAKE / IHARA:                             NONE
```

`R07_THIRTEEN_SEED_COMPLETE_BOUNDARY_CLOSURE_V269_PAPER_GRADE`

