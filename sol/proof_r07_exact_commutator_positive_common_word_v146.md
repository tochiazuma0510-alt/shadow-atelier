# R07 exact-commutator positive common-word selector v146

Author: Sol / 2026-08-27

Status: paper theorem and bounded successor design.  This note strengthens a
task179 finite common-word solve from exponent zero modulo three to exact
free-group exponent zero.  The strengthening adds at most two finite-field
rows and then uses cubes of registered normal generators.  It does not assume
the running task179 production receipt is positive, and it does not settle a
second relative Frattini rung, a cofinal lift, fake, or Ihara witness.

## 1. The exact exponent lattice is only rank two

Let \(F=F(x,y)\), and let

\[
 \Omega=\ker(F\twoheadrightarrow G_{\rm joint})
\tag{1.1}
\]

be task179's registered joint finite-value kernel.  The complete 6,441-word
roster \(r_1,\ldots,r_s\), together with all its conjugates, normally
generates \(\Omega\).  Write

\[
 e_j=\operatorname{exp}(r_j)\in\mathbf Z^2,
 \qquad
 L=\sum_{j=1}^s\mathbf Z e_j\leq\mathbf Z^2.
\tag{1.2}
\]

Conjugation does not change exponent sums, so normal generation gives

\[
 \boxed{L=\operatorname{exp}(\Omega).}
\tag{1.3}
\]

Choose a deterministic Hermite/Smith basis

\[
 \ell_1,\ldots,\ell_t,\qquad 0\leq t\leq2,
\tag{1.4}
\]

of \(L\).  For every word-bearing correction column

\[
 w_{\delta,j}=u_\delta r_j u_\delta^{-1},
\tag{1.5}
\]

write

\[
 e_j=\sum_{i=1}^t b_{ij}\ell_i
\tag{1.6}
\]

and retain the lattice-residue column

\[
 \bar e_j=(b_{1j},\ldots,b_{tj})\bmod3
 \in L/3L\simeq\mathbf F_3^t.
\tag{1.7}
\]

Only the roster row \(j\), not the conjugator \(\delta\), affects (1.7).
The basis, every integral coordinate in (1.6), and both directions of the
integer round trip are part of the certificate.

## 2. Exact charmingness as at most two extra rows

Let

\[
 \overline{\mathscr V}:\Omega\longrightarrow Q:=Z_0/D_0
\tag{2.1}
\]

be the task179 all-seven change map modulo the separately typed PB3/PB4
boundary image, and put \(z_0=-[T_0]\).  For (1.5), write

\[
 v_{\delta,j}=\overline{\mathscr V}(w_{\delta,j}).
\tag{2.2}
\]

Define the exponent-augmented positive column

\[
 \widetilde v_{\delta,j}
   =(v_{\delta,j},\bar e_j)
   \in Q\oplus L/3L.
\tag{2.3}
\]

Every boundary column is augmented by zero.  The target is

\[
 \widetilde z_0=(z_0,0).
\tag{2.4}
\]

### Theorem 2.1 (EXACT-COMMUTATOR COMMON-WORD CRITERION)

There is a finite correction word

\[
 c\in\Omega\cap[F,F],
 \qquad \overline{\mathscr V}(c)=z_0,
\tag{2.5}
\]

if and only if

\[
 \boxed{
 (z_0,0)\in
 \operatorname{span}_{\mathbf F_3}
 \{\widetilde v_{\delta,j}\}_{\delta,j}.}
\tag{2.6}
\]

Equation (2.6) is written in the quotient \(Q=Z_0/D_0\).  In the raw
implementation it is equivalently

\[
 (-T_0,0)\in(D_0,0)+
 \operatorname{span}_{\mathbf F_3}
 \{(V_{\delta,j},\bar e_j)\}_{\delta,j}.
\tag{2.6a}
\]

Moreover, any coefficient solution of (2.6) materializes an explicit word
in (2.5) by one rank-two integer correction.

#### Proof: necessity

Because the roster normally generates \(\Omega\), write

\[
 c=\prod_k w_{\delta_k,j_k}^{n_k},
 \qquad n_k\in\mathbf Z.
\tag{2.7}
\]

Reduce every \(n_k\) modulo three.  Additivity of
\(\overline{\mathscr V}\) gives the first coordinate of (2.6).  Exact
exponent zero gives

\[
 0=\sum_k n_ke_{j_k},
\tag{2.8}
\]

so its coordinates in the basis (1.4) vanish modulo three.  This is the
second coordinate of (2.6).

#### Proof: sufficiency and word materialization

Let \(a_k\in\{0,1,2\}\) be a finite coefficient solution of (2.6), and use
the task179 signed convention

\[
 \epsilon(0)=0,\qquad\epsilon(1)=1,\qquad\epsilon(2)=-1.
\tag{2.9}
\]

Form

\[
 c_*=\prod_k w_{\delta_k,j_k}^{\epsilon(a_k)}.
\tag{2.10}
\]

The first coordinate of (2.6) gives
\(\overline{\mathscr V}(c_*)=z_0\).  The last \(t\) coordinates say that

\[
 \operatorname{exp}(c_*)=3\ell
 \quad\text{for some }\ell\in L.
\tag{2.11}
\]

Use the fixed Smith section for (1.2) to choose integers \(q_j\) satisfying

\[
 \sum_j q_je_j=-\ell.
\tag{2.12}
\]

For every used roster row choose its canonical identity-conjugator word and
put

\[
 h=\prod_j r_j^{3q_j},
 \qquad
 \boxed{c=c_*h.}
\tag{2.13}
\]

Each \(r_j\) lies in \(\Omega\), hence so does \(h\).  Characteristic
three and additivity give

\[
 \overline{\mathscr V}(h)
 =\sum_j3q_j\overline{\mathscr V}(r_j)=0.
\tag{2.14}
\]

Equations (2.11)--(2.13) give
\(\operatorname{exp}(c)=0\).  Therefore (2.5) holds. \(\square\)

The construction uses ordinary integer powers only after the finite-field
solve.  Coefficient 2 in (2.10) remains a literal inverse; replacing it by
two positive copies changes the intermediate integer exponent and must be
replayed through (2.11)--(2.13).

## 3. Relationship to the current task179 receipt

The current task179 system appends the standard coordinates

\[
 \operatorname{exp}(w)\bmod3\in\mathbf F_3^2.
\tag{3.1}
\]

Those rows prove only that the selected exponent vector belongs to
\(3\mathbf Z^2\).  The exact cube repair in (2.13) requires the stronger
condition

\[
 \boxed{\operatorname{exp}(c_*)\in3L.}
\tag{3.2}
\]

If \(L=\mathbf Z^2\), (3.1) and (3.2) coincide.  In general they do not.
The complete lattice (1.2), rather than its rank alone, decides whether the
current receipt can be repaired without changing its finite-field
coefficients.

### Corollary 3.1 (ZERO-COST REPAIR OF A POSITIVE RECEIPT)

Suppose task179 returns `COMMON_WORD` with correction \(c_0\).  Compute its
integer exponent vector.

1. If \(\operatorname{exp}(c_0)=0\), it is already an exact commutator.
2. If \(\operatorname{exp}(c_0)\in3L\), equations (2.12)--(2.13) repair it
   using roster cubes, without another orbit search.
3. If \(\operatorname{exp}(c_0)\notin3L\), that particular coefficient
   solution is not cube-repairable.  This is not a negative result for the
   whole first-rung fibre.  Rerun/resume positive column generation with the
   \(t\) lattice-residue rows (1.7); Theorem 2.1 is the complete criterion.

In cases 1 and 2, the independent checker must directly replay the final
word, exact exponent \((0,0)\), joint-kernel value, the sparse all-seven
identity, both hexagons, and the printed-order pentagon.  Boundary chains
remain excluded from the source word.

## 4. Positive-only column generation is unchanged

The task179 column-generation proof applies verbatim to (2.6).  At a nonzero
remainder, a dual row now has at most two additional coordinates.  For a
normal-generator row \(j\), their contribution is the constant

\[
 \lambda_{\rm exp}(\bar e_j),
\tag{4.1}
\]

independent of the linked context state \(\delta\).  Hence the existing
weighted formula becomes

\[
 F_j^{\rm com}(\delta)
 =K_j+\lambda_{\rm exp}(\bar e_j)
  +\sum_{i,t}c_{j,i}(t)1_{\pi_i(\delta)=t}.
\tag{4.2}
\]

The support-fibre, kernel-prefix, and global-roster schedules are unchanged.
Every ACTIVE column still receives a direct full-eleven replay and a new
pivot check.  A resource cap remains `UNKNOWN_RESOURCE`; there is no
negative terminal without complete exhaustion.

The exact-exponent additions are small:

1. compute 6,441 integer exponent pairs and their rank-two Smith basis;
2. attach the same \(t\)-coordinate residue to every conjugate of one roster
   row;
3. target the zero residue in (2.4); and
4. after membership, execute the rank-two integer solve (2.12).

No enumeration of the full homogeneous kernel, no BFS of \(F/H\), and no
new 357,128,352-state Delta materialization is required.

## 5. Exact successor contract

After the running production terminal is available:

1. authenticate the task179 receipt and recompute
   \(\operatorname{exp}(c_0)\in\mathbf Z^2\);
2. reconstruct all 6,441 roster exponent pairs, compute a canonical basis of
   \(L\), and prove (1.3) from the pinned normal-generation receipt;
3. test Corollary 3.1 in order;
4. on case 2, materialize the cube repair and run an independent direct
   checker;
5. on case 3, preserve the task179 checkpoint and launch a versioned
   lattice-augmented positive resume; and
6. only an accepted exact-commutator word is passed to v145's second
   relative Frattini rung.

Required mutations include: standard \(\mathbf Z^2/3\mathbf Z^2\) used in
place of \(L/3L\), a nonprimitive or wrong-order lattice basis, one changed
roster exponent, coefficient 2 materialized without inversion, division of
(2.11) by three before membership in \(L\), one cube exponent \(3q_j\)
changed to \(q_j\), insertion of a boundary row into (1.2), and a final word
whose exact exponent is only zero modulo three.

```text
COMPLETE NORMAL-ROSTER EXPONENT LATTICE L:        FINITE RANK-TWO INPUT
EXACT COMMUTATOR <=> t<=2 AUGMENTED ROWS:          PAPER_PROOF
POSITIVE COEFFICIENTS -> CUBE-EXACTIFIED WORD:     PAPER_PROOF
CURRENT TASK179 INTEGER EXPONENT / 3L TEST:        PENDING RECEIPT
LATTICE-AUGMENTED PRODUCTION RESUME:               NOT IMPLEMENTED
EXACT-COMMUTATOR FIRST FRATTINI WORD:              NOT YET CONSTRUCTED
SECOND FRATTINI RUNG / COMPLETED HOMOTOPY:          OPEN
COMPATIBLE COFINAL LIFT / FAKE / IHARA WITNESS:    NOT DECLARED
```

`R07_EXACT_COMMUTATOR_POSITIVE_COMMON_WORD_V146_PAPER_GRADE`
