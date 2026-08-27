# R07 positive augmented-saturation word selector v141

Author: Sol / 2026-08-27

Status: paper theorem and next-computation contract.  This note turns the
v129 actual-class equation into a positive-only, word-bearing finite
algorithm.  It also separates the boundary chain in v140 from the deeper
correction coefficient in v129; confusing those two objects changes the
literal source word.  The actual R07 augmented system has not yet been run.
No compatible cofinal lift, fake, or Ihara witness is declared here.

## 1. Two different quantities previously denoted by d

The finite all-seven certificate of v140 has the form

\[
 -T=d_{\rm bdry}+\mathscr V(a_0),
 \qquad d_{\rm bdry}\in D_{\rm PB3/PB4}.
\tag{1.1}
\]

Here \(d_{\rm bdry}\) is a relation-module boundary chain.  It certifies
that the residual is zero in the required quotient, but it is **not** a
source correction and must never be multiplied into the correction word.

After lifting the resulting leading coefficient \(a_0\) to a deeper
module, v129 instead forms

\[
 e=Ba_0-z\in JZ
\tag{1.2}
\]

and asks for

\[
 \boxed{e=Bd_{\rm sat}+\rho z,
 \qquad d_{\rm sat}\in JA,\quad \rho\in J.}
\tag{1.3}
\]

The element \(d_{\rm sat}\) is a genuine deeper **source correction
coefficient**.  It occurs in the final coefficient

\[
 a=(1+\rho)^{-1}(a_0-d_{\rm sat}).
\tag{1.4}
\]

Thus the safe implementation names are `d_boundary` and `d_saturation`;
they have different types and opposite word-materialization rules.

## 2. Finite word-bearing augmented column family

Let \(\Lambda\) be a finite-dimensional \(\mathbf F_3\)-algebra, let
\(J\triangleleft\Lambda\) be a two-sided nilpotent ideal, and let

\[
 B:A\longrightarrow Z
\tag{2.1}
\]

be a homomorphism of finite left \(\Lambda\)-modules.  Fix \(z,e\in Z\).
Choose:

1. a word-bearing \(\mathbf F_3\)-spanning roster
   \(a_1,\ldots,a_s\) of \(A\); and
2. an \(\mathbf F_3\)-basis \(\mu_1,\ldots,\mu_t\) of \(J\), with exact
   multiplication and action tables.

Then

\[
 JA=\operatorname{span}_{\mathbf F_3}
       \{\mu_i a_j:1\leq i\leq t,\ 1\leq j\leq s\}
\tag{2.2}
\]

and

\[
 Jz=\operatorname{span}_{\mathbf F_3}
       \{\mu_i z:1\leq i\leq t\}.
\tag{2.3}
\]

Consequently the augmented map

\[
 \Psi:JA\oplus J\longrightarrow Z,
 \qquad \Psi(d,\rho)=Bd+\rho z
\tag{2.4}
\]

has the finite typed column family

\[
 \mathcal C_{\rm sat}=
 \{B(\mu_i a_j)\}_{i,j}
 \ \sqcup\
 \{\mu_i z\}_i.
\tag{2.5}
\]

The disjoint tag in (2.5) is load-bearing.  A column in the first family
contributes to the correction coefficient \(d_{\rm sat}\); a column in the
second contributes to the scalar \(\rho\).  Equal vectors from the two
families may not be deduplicated without retaining both typed preimages.

For a context-changing edge with
\(K_A=\ker(A'\to A)\) not known to equal \(JA'\), replace the first roster
in (2.5) by any complete word-bearing finite spanning roster of \(K_A\).
The proof below is unchanged and decides membership in
\(B'(K_A)+Jz'\), the denominator of v129 (4.9).

## 3. Positive-only augmented selector

Starting with any authenticated independent prefix of (2.5), maintain an
exact echelon basis \(W_k\) and the remainder of \(e\).  If
\(e\notin W_k\), choose an exact dual row \(\lambda_k\) satisfying

\[
 \lambda_k(W_k)=0,
 \qquad \lambda_k(e)\ne0.
\tag{3.1}
\]

Probe the two typed families in a fair schedule.  A probe is positive only
after the **complete** vector in \(Z\) has been replayed and satisfies

\[
 \lambda_k(c)\ne0.
\tag{3.2}
\]

Retain its typed preimage and add it after an exact new-pivot check.

### Theorem 3.1 (POSITIVE AUGMENTED-SATURATION TERMINATION)

Assume

\[
 e\in B(JA)+Jz.
\tag{3.3}
\]

If the probes enumerate the finite family (2.5) fairly, the procedure above
terminates after finitely many rank increases and returns explicit
word-bearing \(d_{\rm sat}\in JA\) and explicit \(\rho\in J\) satisfying
(1.3).

#### Proof

Suppose \(e\notin W_k\) and take \(\lambda_k\) as in (3.1).  If
\(\lambda_k\) vanished on every column of (2.5), it would vanish on
\(B(JA)+Jz\), contradicting (3.3) and \(\lambda_k(e)\ne0\).  Hence some
typed column is positive.  Fairness reaches it, and (3.1)--(3.2) imply a
strict rank increase.  The ambient \(\mathbf F_3\)-space \(Z\) is finite
dimensional, so only finitely many such increases can occur.  Therefore a
later remainder is zero.

Coefficient recovery in the retained column order writes

\[
 e=\sum_{i,j}u_{ij}B(\mu_i a_j)
   +\sum_i v_i\mu_i z,
 \qquad u_{ij},v_i\in\mathbf F_3.
\tag{3.4}
\]

Put

\[
 d_{\rm sat}=\sum_{i,j}u_{ij}\mu_i a_j,
 \qquad \rho=\sum_i v_i\mu_i.
\tag{3.5}
\]

Equations (3.4)--(3.5) give (1.3).  Every \(a_j\) and every action
\(\mu_i a_j\) retained a source-word preimage, so the first coordinate is
word-bearing.  \(\square\)

If (3.3) is false, or a registered cap is reached before the active column,
the bounded algorithm returns `UNKNOWN_RESOURCE`.  A dual for the current
prefix is not a separator for the unvisited family.

## 4. From the positive certificate to one literal deeper word

Assume \(J^L=0\).  Given (1.3), put

\[
 U=(1+\rho)^{-1}=\sum_{m=0}^{L-1}(-\rho)^m,
 \qquad a=U(a_0-d_{\rm sat}).
\tag{4.1}
\]

No commutativity of \(\Lambda\) is needed: the finite geometric identity
for the single element \(\rho\) is two-sided.  By \(\Lambda\)-linearity,

\[
 B(a_0-d_{\rm sat})=(1+\rho)z
 \quad\Longrightarrow\quad Ba=z.
\tag{4.2}
\]

### Theorem 4.1 (WORD MATERIALIZATION)

Suppose the word-bearing model of \(A\) realizes addition by ordered word
product, negation by word inverse, and the action of each registered group
element by the registered translate/conjugate operation.  Then (4.1) can be
materialized as a finite ordinary source word.  The same word reduces to
the coarse word represented by \(a_0\), and direct replay gives residual
\(z\) at the deeper level.

#### Proof

Expand every coefficient of \(d_{\rm sat}\), \(\rho\), and the finitely
many powers in \(U\) in the fixed \(\mathbf F_3\)-basis of \(\Lambda\).
Replace coefficient 1 by the registered translated word and coefficient 2
by its inverse, preserving the frozen expansion order.  This gives an
ordinary word representing (4.1).  Because \(d_{\rm sat},\rho\in J\), one
has \(U\equiv1\pmod J\), so the word reduces to \(a_0\) at the coarse
level.  Equation (4.2) proves its deeper residual identity.  \(\square\)

For the fixed R07 Jennings step, \(J=I^9\) and \(I^{29}=0\), hence
\(J^4=0\) and the exact formula is

\[
 \boxed{a=(1-\rho+\rho^2-\rho^3)
              (a_0-d_{\rm sat}).}
\tag{4.3}
\]

The checker must reconstruct the ring products \(\rho^2,\rho^3\); it may
not treat the four displayed summands as unrelated correction columns.

## 5. Positive receipt and cofinal iteration

A successful augmented receipt needs only positive data:

1. the exact ring/ideal/module pins and the lifted actual error
   \(e=Ba_0-z\);
2. every retained typed column and its word/ring preimage;
3. each dual pairing and strict rank transition;
4. the recovered equality (1.3), separately typed as
   `d_saturation` and `rho`;
5. exact multiplication showing \((1+\rho)U=U(1+\rho)=1\);
6. literal word materialization of (4.1), coarse reduction to \(a_0\), and
   full deeper all-seven replay; and
7. all marking, exponent, formation, and nonabelian side gates belonging to
   that edge.

It need not certify that an earlier active column did not exist.  A bounded
miss has no negative mathematical content.

At each abelian edge of a fixed cofinal ladder, apply Theorem 3.1 to the
actual lifted error and Theorem 4.1 to the returned pair.  Each output
reduces to the preceding word, so v129 Theorem 5.1 makes the resulting
sequence automatically compatible.  This gives a uniform **algorithmic
form** of the relative lift selector; it does not prove that (3.3) holds at
every R07 edge.  Nonabelian chief edges still require their finite
accepted-set witnesses.

## 6. Immediate R07 execution order

1. Accept a task179 common word only after its independent all-seven replay.
2. Lift its word-bearing coefficient \(a_0\) into the fixed full Jennings
   context and compute the named error \(e\).
3. Enumerate the two typed families in (2.5) lazily and run Theorem 3.1.
4. On success, materialize (4.3) and replay the literal word, not merely its
   module vector.
5. Use the same positive augmented engine at later abelian refinement
   edges; record each actual-class failure as `UNKNOWN` unless a complete
   typed separator is independently proved.

This is the next consumer of a positive task179 output.  It removes the
need for a global orbit splitter and for separate depth-10/11/12 searches,
but it does not assume the missing actual-class membership.

```text
BOUNDARY d VS SATURATION d TYPE SEPARATION:   PAPER_PROOF
FINITE AUGMENTED COLUMN FAMILY:               PAPER_PROOF
POSITIVE-ONLY (d_saturation,rho) TERMINATION: PAPER_PROOF
FINITE ORDINARY-WORD MATERIALIZATION:         PAPER_PROOF
SEQUENTIAL ABELIAN-EDGE COMPATIBILITY:        PAPER_PROOF (v129 + v141)
TASK179 FIRST ALL-SEVEN COMMON WORD:           NOT YET COMPUTED
R07 FIRST AUGMENTED SATURATION PAIR:           NOT YET COMPUTED
ALL ABELIAN ACTUAL-CLASS MEMBERSHIPS:          OPEN
NONABELIAN ACCEPTED SETS:                      OPEN
COMPATIBLE COFINAL R07 LIFT:                   NOT CONSTRUCTED
FAKE / IHARA WITNESS:                          NOT DECLARED
```
