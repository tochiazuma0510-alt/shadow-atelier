# R07 return-Reynolds reduction for the actual orbit splitter v112

Author: Sol / 2026-08-27

Status: exact paper lemma over \(\mathbf F_3\).  It proves that return parity,
and more generally any registered prime-to-three context symmetry, creates no
additional leading-layer obstruction after actual orbit membership is known.
It does not prove that the stacked g760 defect is in the correction image, it
does not contract the three-primary context radical, and it does not declare
a cofinal lift, fake, or Ihara witness.

## 1. Question isolated by v111

Use the v111 leading-layer datum

\[
 B:A\longrightarrow Z
\tag{1.1}
\]

over \(k=\mathbf F_3\).  Both modules carry the same registered context
action and \(B\) is equivariant.  For an actual leading defect \(z\), v111
Proposition 4.1 asks for a preimage \(a\) satisfying not only \(Ba=z\), but
also every context relation which annihilates \(z\).

The return involution is one such relation.  The purpose of this note is to
show that its relation can always be imposed by a closed formula.  Therefore
the previously detected return-even field-outer class is evidence against a
pure \(1-\theta\) correction formula, but is not by itself evidence against
an actual full-orbit lift.

## 2. Return parity is automatically enforceable

Let \(\theta^2=1\) act linearly on \(A\) and \(Z\), and assume

\[
 B\theta=\theta B.
\tag{2.1}
\]

Since \(2\) is invertible in \(k\), put

\[
 e_+=\frac{1+\theta}{2},
 \qquad
 e_-=\frac{1-\theta}{2}.
\tag{2.2}
\]

These are orthogonal idempotents with sum one.

### Lemma 2.1 (RETURN-REYNOLDS PREIMAGE)

Let \(\varepsilon\in\{+1,-1\}\).  If

\[
 \theta z=\varepsilon z,
 \qquad Ba=z,
\tag{2.3}
\]

then

\[
 \boxed{a_\varepsilon=e_\varepsilon a}
\tag{2.4}
\]

satisfies

\[
 \boxed{Ba_\varepsilon=z,
 \qquad \theta a_\varepsilon=\varepsilon a_\varepsilon.}
\tag{2.5}
\]

#### Proof

Equivariance gives

\[
 Ba_\varepsilon=Be_\varepsilon a
 =e_\varepsilon Ba=e_\varepsilon z=z.
\]

The second identity follows from
\(\theta e_\varepsilon=\varepsilon e_\varepsilon\).  \(\square\)

At the value level, (2.4) is word-bearing whenever the registered correction
domain is return-stable: coefficients in \(\mathbf F_3\) are represented by
the corresponding products and inverses of a correction and its returned
word.  Preservation of nonlinear side gates remains a separate replay
obligation.

### Corollary 2.2 (NO RETURN-PARITY OBSTRUCTION)

On either return eigenspace,

\[
 z\in\operatorname{im}B
 \quad\Longleftrightarrow\quad
 z\in B(A^\varepsilon).
\tag{2.6}
\]

Thus the return-even survivor cannot be killed by the odd operator
\(1-\theta\), but any actual full-orbit preimage of it can be chosen
return-even by (2.4).

## 3. Prime-to-three context symmetries

The preceding formula is the order-two case of a standard finite averaging
argument, recorded here because its explicit direction matters for the
word-bearing selector.

Let a finite group \(H\) of order prime to three act on \(A\) and \(Z\), and
let \(B\) be \(H\)-equivariant.  Let \(W\subseteq Z\) be an \(H\)-submodule
contained in \(\operatorname{im}B\).  Choose any \(k\)-linear right inverse

\[
 s_0:W\longrightarrow B^{-1}(W),
 \qquad Bs_0=1_W.
\tag{3.1}
\]

Define

\[
 \boxed{
 s_H(w)=\frac1{|H|}\sum_{h\in H}h^{-1}s_0(hw).}
\tag{3.2}
\]

### Theorem 3.1 (PRIME-TO-THREE REYNOLDS SPLITTER)

The map \(s_H\) is an \(k[H]\)-linear right inverse to \(B\) on \(W\).

#### Proof

First,

\[
 Bs_H(w)=\frac1{|H|}\sum_{h\in H}h^{-1}Bs_0(hw)
 =\frac1{|H|}\sum_{h\in H}h^{-1}hw=w.
\tag{3.3}
\]

For \(g\in H\), substitute \(k=hg\):

\[
 s_H(gw)
 =\frac1{|H|}\sum_{h\in H}h^{-1}s_0(hgw)
 =g\frac1{|H|}\sum_{k\in H}k^{-1}s_0(kw)
 =g s_H(w).
\tag{3.4}
\]

Hence \(s_H\) is equivariant and is a right inverse.  \(\square\)

In particular, for \(W=k[H]z\), the single membership
\(z\in\operatorname{im}B\) implies \(W\subseteq\operatorname{im}B\), and
(3.2) supplies the annihilator-compatible splitter on the whole \(H\)-orbit.

## 4. Semisimple leading quotient

Suppose the registered context group has a typed decomposition

\[
 \Delta=P\rtimes H,
 \qquad P\text{ a }3\text{-group},
 \qquad 3\nmid |H|,
\tag{4.1}
\]

and take

\[
 \Lambda=k[\Delta],
 \qquad \mathfrak a=I(P)\Lambda.
\tag{4.2}
\]

Then

\[
 \Lambda/\mathfrak a\cong k[H]
\tag{4.3}
\]

is semisimple.  Therefore every leading-layer surjection onto an
\(H\)-submodule splits, explicitly by (3.2).  For the cyclic actual module
\(\overline Z_z=(\Lambda/\mathfrak a)z\), this gives

\[
 \boxed{
 z\in\operatorname{im}\overline B
 \Longrightarrow
 \text{v111 condition (4.5) has a solution}.}
\tag{4.4}
\]

The implication (4.4) may be used for R07 only after the actual diagonal
context image and the ideal \(\mathfrak a\) have been authenticated and
(4.1) has been checked.  The notation \(O_3(\Delta)\) alone is insufficient:
the quotient can still have order divisible by three.

## 5. What remains genuinely three-primary

The Reynolds formulas remove only relations coming from invertible group
orders.  They do not average over a nontrivial three-subgroup.  Accordingly,
the actual splitter problem separates as

\[
 \boxed{
 \begin{array}{c}
 \text{return / registered }3'\text{-symmetry}\;:\;
 \text{closed Reynolds formula},\\[2mm]
 \text{three-primary context radical}\;:\;
 \text{actual membership, relation lifting, and naturality still required}.
 \end{array}}
\tag{5.1}
\]

If task 172 authenticates only the return action, Lemma 2.1 is the available
conclusion.  If it authenticates the stronger semidirect-product hypothesis
(4.1), Theorem 3.1 turns leading membership into the complete leading
splitter.  In either case, promotion through all radical depths still needs
the filtration-raising lift required by v111 Theorem 3.1.  Maschke averaging
does not prove that lift, all-edge side-gate admissibility, or nonabelian
accepted-set nonemptiness.

## 6. Updated boundary

```text
RETURN +/- REYNOLDS PREIMAGE:                 PAPER_PROOF
REGISTERED 3'-CONTEXT REYNOLDS SPLITTER:      PAPER_PROOF
CURRENT DELTA = P semidirect H TYPING:        NOT YET AUTHENTICATED
STACKED g760 LEADING MEMBERSHIP:              NOT YET COMPUTED
THREE-PRIMARY RADICAL HOMOTOPY:               OPEN (v111 criterion)
ALL-EDGE NATURALITY / SIDE GATES:             OPEN
NONABELIAN ACCEPTED-SET NONEMPTINESS:         OPEN
COMPATIBLE COFINAL R07 LIFT:                  NOT CONSTRUCTED
FAKE / IHARA WITNESS:                         NOT DECLARED
```
