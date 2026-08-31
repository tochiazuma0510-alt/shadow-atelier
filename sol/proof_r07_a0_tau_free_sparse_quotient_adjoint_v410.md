# R07 A0 tau-free sparse quotient adjoint (v410)

Author: Sol / 2026-08-31

Status: paper implementation theorem refining v409.  It proves that, when
the current physical quotient dual has zero coefficient on the three global
`tau` keys, its exact adjoint under the v401/v402 normal map can be generated
from a bounded local reverse neighbourhood.  No E3, E4, Q0, or Delta roster
is enumerated.  The theorem deliberately does not dispose of a nonzero
`tau` dual; that branch remains an explicit measured gate.  No A0 terminal,
compatible lift, fake, or Ihara witness is asserted.  `verified=false`.

## 1. Separate the Tietze map from the central normal map

For one physical block write

\[
 C_{\rm old}\xrightarrow{J_{\rm T}}C_{\rm new}
 \xrightarrow{N}Y.
\tag{1.1}
\]

For PB3, (C_{\rm new}=\mathbf F_3[H]^3) has two noncentral
coordinates and one central coordinate.  For PB4 it has five noncentral
coordinates and one central coordinate.  Thus put

\[
 n=2\quad(PB3),\qquad n=5\quad(PB4).
\tag{1.2}

The sparse maps (J_{\rm T}) are v401 (2.2) and v402 (2.2).  They are
left-module maps: every output of one old singleton is a fixed finite list
of right-shifted new singletons, so

\[
 J_{\rm T}L_t=L_tJ_{\rm T}.
\tag{1.3}

The map (N) is the orbitwise `contract` map of the accepted v12 owner.  Fix
the actual order-three central element (z), the actual transversal function

\[
 h=r(h)z^{j(h)},\qquad j(h)\in\{0,1,2\},
\tag{1.4}

and the new noncentral marked images (s_1,\ldots,s_n).  PB3 may use the
least-serialization transversal and PB4 the authenticated kappa transversal;
the argument below does not require either one to split multiplicatively.

## 2. One raw singleton has radius-one output support

Consider a new-coordinate singleton (e_c(h)), and write
(h=r z^j) as in (1.4).

- If (c=n) is the central coordinate, (N(e_n(h))) has localized support
  only at the orbit representative (r), plus possibly the global `tau`
  coordinate.
- If (0\leq c<n), the orbit sum has localized support at (r).  The
  triangular correction to the central coordinate has localized support only
  at

  \[
    r\quad\hbox{and}\quad r(hs_c),
  \tag{2.1}
  \]

  again plus possibly `tau`.

This is read directly from v401 (3.3)--(3.8) and v402 (4.4)--(4.7): the two
elimination coefficients are attached to (h) and (hs_c), and there is no
second edge.  It is also exactly the `contract` control flow in v12; newly
created representatives have zero noncentral input and therefore cannot
start another update.

## 3. Complete reverse neighbourhood of one localized dual key

Let a localized quotient dual key have orbit representative (r).  Define

\[
 \begin{split}
 \mathcal P(r)= {}&
 \{e_n(rz^j):0\leq j<3\}\\
 &\cup\{e_c(rz^j):0\leq c<n,\ 0\leq j<3\}\\
 &\cup\{e_c(rz^j s_c^{-1}):0\leq c<n,\ 0\leq j<3\}.
 \end{split}
\tag{3.1}

The last line is evaluated in the actual finite group and then put back into
the actual transversal form.  Hence it includes all central cocycle shifts,
including the nonsplit PB3 transversal.

### Lemma 3.1 (LOCAL ADJOINT SUPPORT)

Let (y_r^*) be any localized quotient coordinate functional at (r),
including a noncentral orbit sum or either `u0/u1` coordinate, but excluding
the global `tau` functional.  Then

\[
 \operatorname{supp}(N^*y_r^*)\subseteq\mathcal P(r).
\tag{3.2}

In particular

\[
 |\mathcal P(r)|\leq3+6n=
 \begin{cases}
 15,&PB3,\\
 33,&PB4.
 \end{cases}
\tag{3.3}

#### Proof

If a central singleton pairs with (y_r^*N), Section 2 forces its orbit
representative to be (r), giving the first line of (3.1).  If a
noncentral singleton (e_c(h)) pairs, Section 2 says either (r(h)=r),
giving the second line, or (r(hs_c)=r).  In the latter case
(hs_c=rz^j) for one (j), hence (h=rz^js_c^{-1}), giving the third
line.  These exhaust the radius-one output support.  Counting the three
central states and two three-state lists for each of (n) components proves
(3.3). \(\square\)

The set (3.1) is an overestimate for noncentral output labels, but using the
uniform bound avoids a label-specific completeness bug.

## 4. Sparse construction of the full tau-free adjoint

Let

\[
 \lambda=\sum_{(r,\ell)}a_{r,\ell}y_{r,\ell}^*
\tag{4.1}

be a sparse quotient dual with zero coefficient on the global `tau` key.
Take the union of (3.1) over its localized support.  For every raw singleton
(e) in that union, evaluate the already authenticated direct normal map
once and set

\[
 \mu(e)=\langle\lambda,N(e)\rangle.
\tag{4.2}

Delete zero values.

### Theorem 4.1 (TAU-FREE SPARSE ADJOINT)

The functional (\mu) constructed by (4.2) is exactly

\[
 \boxed{\mu=N^*\lambda.}
\tag{4.3}

If (s_3) and (s_4) are the localized PB3 and PB4 dual support counts,
the number of candidate singleton evaluations is at most

\[
 \boxed{15s_3+33s_4}
\tag{4.4}

before duplicate deletion.

#### Proof

Linearity reduces the claim to one supported quotient key.  Lemma 3.1 says
its adjoint is zero outside the enumerated reverse neighbourhood, while
(4.2) gives its exact coefficient on every point inside.  Summing the
supported keys proves (4.3).  Equation (4.4) is (3.3) summed over the sparse
support. \(\square\)

Normalized exponent dual keys pass through unchanged and contribute the
constant (K_i) of v409.  They are not included in (4.4).

## 5. Compile the weighted formula without an old-coordinate adjoint

For each compact seed and occurrence, apply (J_{\rm T}) once to its
untranslated raw Fox gradient.  By (1.3), source conjugation then left
translates this finite new-coordinate row.  Pair its support
((c,h)) with the support ((c,g)) of (N^*\lambda).  With the frozen
occurrence prefix (P_o), the unique linked-coordinate target is

\[
 \pi_{j(o)}(\delta)=P_o^{-1}g h^{-1}
\tag{5.1}

when (h) is the unprefixed Tietze-row key.  Equivalently, using the
already-prefix-translated key gives v409 (3.5).  Merge all eleven occurrences
before deleting zero coefficients.

### Corollary 5.1 (ENUMERATION-FREE FORMULA COMPILER)

For a tau-free physical dual, the complete v409 formula for all at-most-44
compact seeds can be compiled using only:

1. at most (15s_3+33s_4) actual singleton normal-map evaluations;
2. the finite Tietze-expanded supports of the 44-by-eleven base gradients;
3. actual group multiplication/inversion for (5.1); and
4. the normalized exponent constant.

No actor BFS, E3/E4 scan, Q0 scan, Delta scan, or full boundary correlation
occurs before the v142/v143 fibre selector itself.

Every proposed ACTIVE state is still checked by a fresh literal conjugate,
all eleven raw occurrences, the physical normal map, and the direct quotient
dual scalar.  Thus the sparse compiler affects discovery speed, not the
positive trusted base.

## 6. The exact remaining gate

There are three global `tau` keys, one in each physical block.  Their adjoints
need not be localized by Lemma 3.1.  Therefore the production order is:

1. build the first actual physical dual from the 44 identity compact columns
   and the exact v404 action oracle;
2. print its three `tau` coefficients;
3. if all are zero, apply Theorem 4.1 and immediately compute the 44 actual
   `(K,target_count,W)` records;
4. if any is nonzero, retain a fail-closed `NONZERO_TAU_GATE` and derive a
   separate symbolic/global-tau correlation.  Do not materialize a dense raw
   vector and do not call the dual zero.

```text
TAU-FREE Q_ph^* SUPPORT:              <= 15*s3 + 33*s4
ACTUAL GROUP/TRANSVERSAL ENUMERATION:  NONE
PB3 NONSPLIT COCYCLE:                  INCLUDED BY ACTUAL PREDECESSORS
44 WEIGHTED FORMULAE AFTER TAU=0:      FINITE LOCAL COMPILATION
NONZERO GLOBAL TAU:                    SEPARATE MEASURED GATE
ACTUAL FIRST DUAL TAU PROFILE:         NOT YET RUN
ACTUAL A0 MEMBER/NONMEMBER:            NOT YET COMPUTED
```

`R07_A0_TAU_FREE_SPARSE_QUOTIENT_ADJOINT_V410_PAPER_GRADE`
