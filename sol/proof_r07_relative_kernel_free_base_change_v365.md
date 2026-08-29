# R07 relative-kernel-free base-change criterion (v365)

Author: Sol / 2026-08-30

Status: paper theorem refining v361--v364.  At an elementary-abelian
relative Frattini edge, full projectivity over the crossed action algebra is
not needed to kill the kernel base-change defects.  Freeness after restriction
to the relative kernel, together with leading surjectivity, gives an explicit
finite relative-kernel-linear section and kills both defects at every relative
depth.  The actual R07 packaged source and target modules and their leading
ranks still have to be authenticated.  No compatible lift, fake certificate
or Ihara witness is declared.  `verified=false`.

## 1. Induced relative quotients

Let \(k=\mathbf F_p\), and let

\[
 1\longrightarrow K\longrightarrow\Delta _1
 \longrightarrow\Delta _0\longrightarrow1,
 \qquad K\cong(C_p)^t.
\tag{1.1}
\]

Put

\[
 R=k[K],\qquad \mathfrak a=\ker(R\to k),\qquad
 \Lambda=k[\Delta _1],\qquad
 J=\ker(\Lambda\to k[\Delta _0]).
\tag{1.2}
\]

V364 proves

\[
 J^r=\mathfrak a^r\Lambda,
 \qquad J^{(p-1)t+1}=0.
\tag{1.3}
\]

### Lemma 1.1 (RELATIVE SHAPIRO QUOTIENT)

For every \(r\geq1\), as right \(\Lambda\)-modules,

\[
 \boxed{
 \Lambda/J^r\cong (R/\mathfrak a^r)\otimes_R\Lambda.}
\tag{1.4}
\]

Consequently, for every left \(\Lambda\)-module \(N\),

\[
 \boxed{
 \operatorname {Tor}^{\Lambda}_i(\Lambda/J^r,N)
 \cong
 \operatorname {Tor}^{R}_i(R/\mathfrak a^r,N)}
 \qquad(i\geq0),
\tag{1.5}
\]

where the right side uses the restricted \(R\)-action on \(N\).

#### Proof

Choose right-coset representatives for \(K\) in \(\Delta _1\).  They make
\(\Lambda\) free as a left \(R\)-module, and reduction of the coefficient
of every representative modulo \(\mathfrak a^r\) identifies the two sides
of (1.4).  The kernel is \(\mathfrak a^r\Lambda=J^r\).

If \(P_\bullet\to R/\mathfrak a^r\) is a projective right
\(R\)-resolution, then
\(P_\bullet\otimes_R\Lambda\) is a projective right
\(\Lambda\)-resolution of (1.4).  Associativity gives

\[
 (P_\bullet\otimes_R\Lambda)\otimes_\Lambda N
 \cong P_\bullet\otimes_R N,
\]

and homology gives (1.5). \(\square\)

At \(r=1\), equation (1.5) is the concrete group-homology identity

\[
 \operatorname {Tor}^{\Lambda}_1(\Lambda/J,N)
 \cong H_1(K,N).
\tag{1.6}
\]

## 2. The exact defect is relative-kernel homology

Let

\[
 f:M\longrightarrow N
\tag{2.1}
\]

be a \(\Lambda\)-linear map, put \(L=\ker f\), and assume that the leading
map

\[
 \bar f:M/JM\longrightarrow N/JN
\tag{2.2}
\]

is onto.

### Lemma 2.1 (LEADING ONTO IS ACTUALLY ONTO)

The map \(f\) is onto.  In particular, every v361 lifting defect vanishes:

\[
 \boxed{T_r(f)=0\qquad(r\geq1).}
\tag{2.3}
\]

#### Proof

For \(C=\operatorname {coker}f\), (2.2) says \(C=JC\).  Iteration and
(1.3) give \(C=J^{(p-1)t+1}C=0\), so \(f\) is onto.  Then

\[
 f(J^rM)=J^rf(M)=J^rN,
\]

which is exactly (2.3). \(\square\)

Assume henceforth that the restriction of \(M\) to \(R=k[K]\) is free.
Applying \((\Lambda/J^r)\otimes_\Lambda-\) to
\(0\to L\to M\to N\to0\), Lemma 1.1 makes the preceding Tor term for
\(M\) zero.  The kernel of
\(L/J^rL\to M/J^rM\) is v361's \(S_r(f)\).  Hence:

### Theorem 2.2 (RELATIVE HOMOLOGY DEFECT FORMULA)

For every \(r\geq1\),

\[
 \boxed{
 S_r(f)\cong
 \operatorname {Tor}^{R}_1(R/\mathfrak a^r,N).}
\tag{2.4}
\]

In particular,

\[
 \boxed{S_1(f)\cong H_1(K,N).}
\tag{2.5}

Thus the four ambient intersections in a direct v361 calculation may be
replaced, when the source is relative-kernel-free, by one standard Tor or
group-homology calculation on the actual codomain.

## 3. One leading test kills every depth

The algebra

\[
 R\cong
 k[T_1,\ldots,T_t]/(T_1^p,\ldots,T_t^p)
\tag{3.1}
\]

is local Artinian with maximal ideal \(\mathfrak a\).  For a finite
\(R\)-module \(N\), the following are equivalent:

\[
 \boxed{
 H_1(K,N)=0
 \quad\Longleftrightarrow\quad
 N\text{ is projective over }R
 \quad\Longleftrightarrow\quad
 N\text{ is free over }R.}
\tag{3.2}

Indeed, take a minimal finite free resolution \(F_\bullet\to N\) over the
local algebra \(R\).  Every differential has entries in
\(\mathfrak a\), so tensoring with \(k=R/\mathfrak a\) makes all
differentials zero and
\(\operatorname {Tor}^R_1(k,N)\cong F_1\otimes_Rk\).  Its vanishing and
Nakayama give \(F_1=0\), so \(F_0\to N\) is an isomorphism and \(N\) is
free.  The reverse implication is immediate.

Combining (2.3)--(3.2) gives the exact finite dichotomy.

### Theorem 3.1 (RELATIVE-KERNEL-FREE BASE CHANGE)

Suppose \(M\) and \(N\) are finite free after restriction to \(R=k[K]\)
and \(\bar f\) is onto.  Then

\[
 \boxed{
 S_r(f)=T_r(f)=0\qquad\text{for every }r\geq1.}
\tag{3.3}
\]

Equivalently, all natural maps

\[
 \boxed{
 (\ker f)/J^r(\ker f)
 \;\xrightarrow{\sim}\;
 \ker\bigl(M/J^rM\to N/J^rN\bigr)}
\tag{3.4}
\]

are isomorphisms.

There is also an explicit finite section at the exact strength needed for
(3.3).  Choose an \(R\)-basis \(e_1,\ldots,e_q\) of \(N\), lift its
leading classes through \(\bar f\), and extend the chosen preimages to an
\(R\)-linear map \(s_0:N\to M\).  Put \(E=fs_0-1_N\).  Then

\[
 E(N)\subseteq\mathfrak aN,
 \qquad E^{(p-1)t+1}=0,
\]

and

\[
 \boxed{
 s=s_0\sum_{i=0}^{(p-1)t}(-E)^i,
 \qquad fs=1_N.}
\tag{3.5}

The section is \(R\)-linear; it need not be \(\Lambda\)-linear.  That is
enough because \(J^rM=\mathfrak a^rM\): the resulting
\(R\)-module decomposition
\(M=L\oplus s(N)\) proves
\(L\cap J^rM=J^rL\), while Lemma 2.1 already proves the \(T_r\) equality.

Conversely, assume \(\bar f\) is onto, \(M\) is \(R\)-free, and \(N\) is
finite over \(R\) (automatic when \(M\) is finite).  Equations (2.5) and
(3.2) show that the single equality \(S_1(f)=0\) forces \(N\) to be
\(R\)-free and hence forces all the equalities (3.3).  There is no separate
higher-depth saturation test.

## 4. Exact R07 consequence

For an R07 elementary-abelian edge, \(p=3\), so the section polynomial in
(3.5) has degree at most \(2t\).  Every raw coordinate module
\(\Lambda^q\) is automatically free over \(R=\mathbf F_3[K]\), because
\(\Lambda\) is free over \(R\) on a coset transversal.  Therefore:

1. if the physically packaged source and codomain of \(G\) are finite sums
   of the full-action raw coordinate module, the source and codomain type
   gates in v361 are automatic; leading surjectivity of \(\bar G\) alone
   kills \(S_r(G),T_r(G)\) at every depth;
2. the same statement applies to \(H\) whenever its exact source and
   codomain are retained as raw full-action coordinate modules; and
3. if either codomain is instead an image, quotient or localized submodule,
   full \(\Lambda\)-projectivity is still unnecessary.  Provided the actual
   source remains \(R\)-free and the leading map is onto, one tests the much
   weaker exact condition \(H_1(K,N)=0\), or directly supplies an
   \(R\)-basis.  A nonzero class is the genuine v361 saturation defect; an
   incomplete search is UNKNOWN.

This replaces v364's sufficient full-action-projectivity gate by a necessary
and sufficient relative-kernel test when the source is relative-kernel-free.
It does not establish the physical packaging or either leading rank.  Those
are the remaining post-A4 finite owner calculations.

```text
RELATIVE SHAPIRO QUOTIENT/TOR FORMULA:             PAPER PROOF
LEADING ONTO => ACTUAL ONTO AND ALL T_r=0:         PAPER PROOF
S_r = Tor_1 OVER F_p[K] FOR K-FREE SOURCE:         PAPER PROOF
S_1=0 IFF FINITE CODOMAIN IS K-FREE:               PAPER PROOF
K-FREE SOURCE/CODOMAIN + LEADING ONTO => ALL DEPTH: PAPER PROOF
R07 FINITE SECTION DEGREE <= 2t:                   PAPER PROOF
ACTUAL G/H RAW-MODULE PACKAGING:                   NOT AUTHENTICATED
ACTUAL bar-G / bar-H LEADING ONTO:                 NOT COMPUTED
COMPATIBLE LIFT / FAKE / IHARA WITNESS:            NOT CONSTRUCTED
```

`R07_RELATIVE_KERNEL_FREE_BASE_CHANGE_V365_PAPER_GRADE`
