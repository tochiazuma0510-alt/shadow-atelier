# R07 lazy-kernel boundary-discrepancy theorem v273

Author: Sol / 2026-08-29

Status: load-bearing word-certificate refinement of v272.  The lazy quotient
algorithm and its support-inversion completeness remain unchanged.  This note
adds the boundary-discrepancy state which must accompany every retained K
word.  Without it, a later conjugation or normalized linear combination need
not replay the stored quotient representative.  No actual A4 rank, K basis,
anchor, lift, fake, or Ihara witness is declared.  `verified=false`.

## 1. The missing state in a word-bearing quotient basis

Let

\[
 A=\bigoplus_{i=0}^{9}A_i,
 \qquad D=\bigoplus_{i=0}^{9}D_i\subseteq A
\tag{1.1}
\]

be the ten-tagged raw Fox module and its full translated presentation-boundary
subspace.  The actual first-successor kernel is represented in the quotient
\(A/D\).  A sparse echelon is free to retain a normalized representative
\(k\in A\), but a literal source word \(W\) realizing its quotient class
generally satisfies only

\[
 \delta(W)=k+e,
 \qquad e\in D,
\tag{1.2}
\]

where \(\delta\) is the raw ten-context affine/Fox defect.

The term \(e\) is zero for an initial presentation word before quotient
reduction.  It need not remain zero after subtracting discovered boundary
columns, combining prior K rows, or normalizing.  Consequently a K basis item
must be the triple

\[
 (k,W,E),\qquad \delta(W)=k+\Psi(E),
\tag{1.3}
\]

where \(E\) is an explicit raw boundary ledger and \(\Psi(E)\in D\) is its
evaluated sparse row.  Keeping only \((k,W)\), or assuming every prior word
has raw defect exactly \(k\), loses a load-bearing term.

## 2. A canonical raw boundary ledger

For coordinate \(i\), base presentation relator \(j\), and marked quotient
element \(t\in E_i\), introduce the formal symbol

\[
 [i,j,t]_D,
 \qquad
 \Psi([i,j,t]_D)=t d_{i,j}.
\tag{2.1}
\]

The ledger space \(\mathcal L_D\) consists of finite F3-linear combinations
of these symbols, collected under the complete canonical key \((i,j,t)\).
Equation (2.1) gives a surjection

\[
 \Psi:\mathcal L_D\twoheadrightarrow D.
\tag{2.2}
\]

Injectivity is neither asserted nor needed: different translated relations
may be linearly dependent.  The certificate always checks the evaluated row.

Every discovered boundary pivot must retain its coefficient vector in this
raw ledger, not merely coefficients in a mutable pivot basis.  Thus a
boundary combination returned by reduction expands deterministically to one
element of \(\mathcal L_D\).

For a source letter \(a\in\{x^{\pm1},y^{\pm1}\}\), let \(A_i(a)\in E_i\)
be its actual context value.  Define

\[
 a\cdot[i,j,t]_D=[i,j,A_i(a)t]_D.
\tag{2.3}
\]

Then \(\Psi(a\cdot E)=a\cdot\Psi(E)\).  This is well-defined because every
\(D_i\) is invariant under the full marked group, hence under the source
context image.  Equation (2.3) uses actual group multiplication and retains
the coordinate and relator tags.

## 3. Fixed reduction-sign convention

Let \(k_1,\ldots,k_{t-1}\) be the previously retained quotient-basis rows,
and let a candidate be represented by a sparse row \(v\in A\).  Write the
complete reduction result in the following external convention:

\[
 r=v-\Psi(Q)-\sum_{\ell<t}c_\ell k_\ell,
 \qquad Q\in\mathcal L_D,quad c_\ell\in\mathbf F_3.
\tag{3.1}
\]

This equation is the certificate contract even if an internal echelon uses
`remainder = input + coefficients*raw`.  Such an implementation must convert
its coefficients once to (3.1) before exporting them.  It may not change the
meaning of the same coefficient array between accepted and dependent rows.

If \(r=0\), (3.1) is the MEMBER replay.  If a complete lazy dual proves
nonmembership modulo \(D+\langle k_1,\ldots,k_{t-1}\rangle\), then \(r\ne0\).
Let \(s\in\{1,2\}\) normalize its chosen pivot and set

\[
 k_t=s r.
\tag{3.2}
\]

All row, raw-boundary, and prior-K coefficients are multiplied by the same
\(s\).

## 4. Exact word and boundary-discrepancy recurrence

Assume the candidate carries a literal roof-kernel word \(W_v\) and ledger
\(E_v\) satisfying

\[
 \delta(W_v)=v+\Psi(E_v).
\tag{4.1}
\]

Assume inductively

\[
 \delta(W_\ell)=k_\ell+\Psi(E_\ell)
 \quad(\ell<t).
\tag{4.2}
\]

Use increasing \(\ell\), literal exponents in \(\{0,1,2\}\), free reduction,
and the registered product convention to define

\[
 W_t=
 \operatorname{red}
 \left(W_v\prod_{\ell<t}W_\ell^{-c_\ell}\right)^s.
\tag{4.3}
\]

Define the new boundary ledger by

\[
 \boxed{
 E_t=s\left(E_v+Q-\sum_{\ell<t}c_\ell E_\ell\right).}
\tag{4.4}
\]

### Theorem 4.1 (BOUNDARY-DISCREPANCY REPLAY)

Equations (3.1)--(4.4) imply

\[
 \boxed{\delta(W_t)=k_t+\Psi(E_t).}
\tag{4.5}
\]

#### Proof

All words in (4.1)--(4.3) have trivial roof value.  Hence the affine/Fox
product and inverse laws reduce on them to addition and negation, and literal
power \(s\) multiplies the defect by \(s\).  Therefore

\[
\begin{aligned}
 \delta(W_t)
 &=s\left(v+\Psi(E_v)
       -\sum_{\ell<t}c_\ell(k_\ell+\Psi(E_\ell))\right)\\
 &=s\left(r+\Psi(Q)+\Psi(E_v)
       -\sum_{\ell<t}c_\ell\Psi(E_\ell)\right)\\
 &=k_t+\Psi\left(
       s(E_v+Q-\sum_{\ell<t}c_\ell E_\ell)\right),
\end{aligned}
\]

which is (4.5). \(\square\)

The terms \(E_v\) and \(-\sum c_\ell E_\ell\) are mandatory.  The shorter
formula which keeps only the freshly subtracted boundary combination \(Q\)
is valid only when the candidate and every used prior K word have zero
discrepancy, which is not an invariant of quotient reduction.

## 5. Initial and conjugated candidates

For an authenticated initial presentation relator \(R_j\), set

\[
 v=\delta(R_j),\qquad W_v=R_j,qquad E_v=0.
\tag{5.1}
\]

For a source-action candidate obtained from basis item \((k_p,W_p,E_p)\),
let \(a\in\{x^{\pm1},y^{\pm1}\}\) and use the literal outer-first conjugate

\[
 v=a\cdot k_p,qquad
 W_v=aW_pa^{-1},qquad
 E_v=a\cdot E_p.
\tag{5.2}
\]

Because \(W_p\) has identity roof value, the affine conjugation law gives

\[
 \delta(aW_pa^{-1})
 =\rho_0(a)\cdot\delta(W_p)
 =a\cdot k_p+\Psi(a\cdot E_p),
\tag{5.3}
\]

so (4.1) holds.  Thus (4.4) propagates a valid discrepancy ledger through
every initial and action-generated rank raise.

## 6. Persistent lazy-boundary and K invariants

Let \(B\le D\) be the span of boundary columns discovered so far and
\(L_t=\langle k_1,\ldots,k_t\rangle\).  The v272 query loop maintains:

1. every B pivot lies in D and carries a raw ledger replay;
2. \(B+L_t\) carries a coefficient replay in its immutable raw roster;
3. the classes of \(k_1,\ldots,k_t\) are linearly independent in \(A/D\);
4. every K item satisfies (1.3); and
5. every dependent target has an explicit expression in \(D+L_t\).

### Theorem 6.1 (CHRONOLOGICAL LAZY K CORRECTNESS)

The invariants above survive every active-boundary insertion, MEMBER query,
and accepted K query.  Boundary columns discovered by later queries cannot
invalidate an earlier K rank raise.

#### Proof

For an active-boundary round, the current dual \(\lambda\) annihilates
\(B+L_t\) and pairs nontrivially with the chosen boundary column \(d\).
Hence \(d\notin B+L_t\); inserting it strictly raises the live total rank and
its raw ledger proves (1).

A MEMBER equation is exactly (3.1) with zero remainder, proving (5).  For an
accepted K query, the final support-inversion zero correlation proves that
the dual annihilates the whole D, not merely B.  It also annihilates \(L_t\)
and pairs nontrivially with the target.  The new class is therefore
independent modulo D, proving (3).  Equations (3.2)--(4.5) prove (4), while
coefficient-bearing elimination preserves (2).

For the last assertion, retain the dual which accepted \(k_j\).  It
annihilates all of D and all earlier K rows but not \(k_j\).  Any boundary
column found later still lies in D, so it is also annihilated.  Thus no later
growth of B can create a dependence of \(k_j\) modulo D and its predecessors.
\(\square\)

Together with source-queue exhaustion, Theorem 6.1 supplies the hypothesis
of v231 Theorem 2.1.  The discrepancy ledger does not change K; it supplies
the missing literal-word proof of every quotient representative.

## 7. Checker and anchor consequences

For every accepted K item, both implementations must perform four separate
checks:

1. flat-evaluate \(W_t\) in all ten actual affine contexts;
2. evaluate the retained representative \(k_t\);
3. independently expand and evaluate \(E_t\) from raw translated boundary
   symbols; and
4. require the exact equality (4.5), coordinate and coefficient wise.

A digest, a mutable B-pivot coefficient vector, or membership of the
difference in the *currently discovered* B is insufficient.  The ledger is
in the full raw translated-relation grammar and remains meaningful if B later
changes.

The v247 projection is applied to the literal word \(W_t\), not to the chosen
raw representative alone.  Once (4.5) is accepted, the raw boundary term
vanishes in the actual successor quotient, so the word and representative
give the same K element.  The least nonzero H2(9) projection and powered-word
anchor then proceed exactly as in v247.

## 8. Resource and mutation obligations

Ledger coefficients may be stored as persistent sparse maps or immutable DAG
nodes.  Every node has a finite raw-symbol expansion, and direct expansion is
required for each accepted K item or in independently replayable bounded
chunks.  Resource accounting must charge source action on ledgers, scalar
combination, duplicate-key collection, expansion, and the equality (4.5).
A resource stop before the equality is only `UNKNOWN_RESOURCE`.

At least the following distinct mutations are load-bearing:

- omit or alter the candidate ledger \(E_v\);
- omit or alter one prior-K term \(-c_\ell E_\ell\);
- flip the reduction-boundary sign of Q;
- use the unnormalized rather than scaled ledger;
- reverse the source action in (5.2);
- change one raw boundary tag/translation; and
- replay only modulo discovered B instead of exact equality in A.

Each must reach the actual discrepancy validator on producer and checker
sides.

## 9. Supersession and fixed frontier

V272 Theorems 2.1, 3.1, and 5.1 remain valid.  Its informal word construction
in Section 5 is superseded wherever it omits the recursively accumulated
boundary discrepancy.  Equations (3.1), (4.3), and (4.4) above are the binding
coefficient and word certificate.

```text
LAZY FULL-D QUOTIENT DECISION:                 PAPER PROOF / v272
CHRONOLOGICAL K INDEPENDENCE MODULO FULL D:    PAPER PROOF
RAW BOUNDARY-DISCREPANCY RECURRENCE:           PAPER PROOF
WORD-BEARING SOURCE-ACTION CLOSURE:            PAPER PROOF
ACTUAL A4 K / DISCREPANCY LEDGERS / ANCHOR:    NOT COMPUTED
COMPATIBLE COFINAL LIFT / FAKE / IHARA:         NONE
```

`R07_LAZY_KERNEL_BOUNDARY_DISCREPANCY_V273_PAPER_GRADE`
