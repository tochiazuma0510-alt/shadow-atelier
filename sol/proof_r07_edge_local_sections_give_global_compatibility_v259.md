# R07 edge-local word sections give global compatibility v259

Author: Sol / 2026-08-28

Status: paper synthesis after v98, v117, v247, and v252.  It removes a
spurious compatibility requirement from the explicit-lift frontier: the
finite word-bearing relative-ideal sections used at distinct edges need not
commute with reduction.  Edge-kernel typing of the selected correction words
already makes the accumulated partial words compatible.  The theorem does
not prove that the actual residual is a MEMBER at every edge, and declares no
compatible R07 lift, fake certificate, or Ihara witness.  `verified=false`.

## 1. Nested evaluation tower

Let (F=F(x,y)), and fix a nested cofinal family of finite evaluation kernels

\[
 F\ge N_0\ge N_1\ge N_2\ge\cdots,
 \qquad X_n=F/N_n.
\tag{1.1}
\]

All marked B3/B4 contexts and side coordinates at depth (n) are included in
the single finite quotient (X_n).  Let (Phi_n(f)) be the complete literal
relation residual of a source word (f), including the two hexagons, printed
pentagon, and every side coordinate imposed at that depth.

Suppose a partial word (f_n) has

\[
 Phi_n(f_n)=1.
\tag{1.2}
\]

An edge-local correction is a word (c_nin N_n) such that

\[
 Phi_{n+1}(f_nc_n)=1.
\tag{1.3}
\]

No section of (X_{n+1}	woheadrightarrow X_n) is part of this definition.

## 2. Compatibility is supplied by kernel typing

### Theorem 2.1 (EDGE-LOCAL SECTION COMPATIBILITY)

Assume that for every (n), after (f_n) has been chosen, a finite
word-bearing solver returns a correction (c_n) satisfying (1.3) and
(c_nin N_n).  Define

\[
 f_{n+1}=f_nc_n.
\tag{2.1}
\]

Then:

1. for every (m\le n), (f_{n+1}) and (f_n) have the same value in
   (X_m);
2. the values (([f_n]_{X_n})_n) form a compatible inverse-system point;
3. the ordered product

   \[
    f_\infty=f_0c_0c_1c_2\cdots
   \tag{2.2}
   \]

   converges in the completion defined by (1.1); and
4. if (1.2)--(1.3) include all registered nonlinear and side gates, then the
   limit satisfies every one of them.

The finite linear or set-theoretic sections used by the solver at different
edges need not be compatible with one another.

#### Proof

Because (c_nin N_n), its image in (X_n), and hence in every (X_m) with
(m\le n), is the identity.  Equation (2.1) therefore preserves every
previous value.  This proves assertions 1 and 2.

For fixed (m), all factors (c_n) with (n\ge m) lie in
(N_n\le N_m).  Hence the partial products in (2.2) are eventually constant
in (X_m).  They are therefore Cauchy for the profinite topology and define
the compatible limit in assertion 3.  Every registered relation or side map
is continuous and is already trivial at each sufficiently deep finite
quotient by (1.3), proving assertion 4.  No comparison between the internal
sections used to construct (c_n) and (c_{n+1}) occurs in the argument.
\(square)

This is the group-word form of the adaptive convergence theorem v117.  Its
point here is the application to the noncanonical sections of v247.

## 3. Why the v247 word-bearing section has the required type

At one elementary-abelian relative edge, v247 chooses a transversal and
word-bearing lifts and sends a projected basis vector to

\[
 t(r-1)\longmapsto s(t)(\sigma(r)-1).
\tag{3.1}
\]

In source words, every summand is a pair

\[
 U-V,
 \qquad [U]_{X_n}=[V]_{X_n}.
\tag{3.2}
\]

The ordered materialization of a coefficient (bin\mathbf F_3) uses the
exponent (0,1,-1) and the kernel word (UV^{-1}), with the retained
conjugating prefix.  Equation (3.2) gives

\[
 UV^{-1}in N_n.
\tag{3.3}
\]

Normality of (N_n) puts every conjugate and their ordered product in
(N_n).  Thus every positive A5/A6 ancestry built from the v247 section
automatically meets the kernel premise of Theorem 2.1.

Different transversals or word-bearing lifts at the next edge may change the
literal word (c_{n+1}).  They cannot change the fact that it belongs to
(N_{n+1}\le N_n), which is the only compatibility property used by (2.2).

## 4. Canonical explicit selector once membership is known

At each finite abelian edge the actual correction matrix and target are
finite.  Fix the registered row/column order and reduced-echelon convention.
If the target is a MEMBER, choose the lexicographically first normalized
ancestry and materialize it by (3.2)--(3.3).  At a finite nonabelian edge,
choose the shortlex-first word in the complete accepted set.

### Corollary 4.1 (NO EXTRA COHERENT-SECTION GATE)

If every encountered abelian actual residual is a MEMBER of its registered
joint common-word image, every nonabelian accepted set is nonempty, and each
selected word passes the registered side gates, then the preceding finite
rules compute one explicit compatible inverse-limit word.  One does not also
need a natural transformation between the edgewise v247 sections.

#### Proof

Every finite rule terminates because its matrix or accepted set is finite.
Section 3 gives (c_n\in N_n), and Theorem 2.1 applies. \(square)

This does **not** turn one successful first edge into all-edge success.  It
separates the two statements:

\[
\begin{array}{ll}
\text{compatibility of already selected edge corrections}
 &\text{automatic from }c_n\in N_n,\\
\text{existence of a legal selected correction at every edge}
 &\text{the remaining mathematical problem.}
\end{array}
\tag{4.1}
\]

For the current R07 branch, v252 identifies the latter as the quantified
joint-image membership of the deeper formation/Brunnian-localized residual,
together with nonempty perfect-core accepted sets.

## 5. Corrected frontier

The line in v247 saying that coherent all-rung sections remain a later gate
must now be read narrowly.  A *natural linear section on the whole abstract
module* is still unconstructed and would give a stronger closed homotopy.
It is not necessary for one based explicit lift.  Edge-local word-bearing
sections plus based MEMBER choices suffice.

```text
EDGE-LOCAL WORD SECTIONS PRESERVE ALL COARSER VALUES: PAPER PROOF
ORDERED V247 ANCESTRY LIES IN THE EDGE KERNEL:         PAPER PROOF
SELECTED EDGE WORDS AUTOMATICALLY FORM A THREAD:       PAPER PROOF
NATURAL MODULE-WIDE SECTION/HOMOTOPY:                  NOT REQUIRED FOR ONE BASED LIFT
ALL-EDGE ACTUAL ABELIAN MEMBERSHIP:                    OPEN
NONABELIAN ACCEPTED-SET NONEMPTINESS:                  OPEN
ACTUAL A0--A7 POSITIVE PACKAGE:                        NOT YET COMPLETE
COMPATIBLE R07 LIFT / FAKE / IHARA:                    NOT CONSTRUCTED
```

`R07_EDGE_LOCAL_SECTIONS_GIVE_GLOBAL_COMPATIBILITY_V259_PAPER_GRADE`
