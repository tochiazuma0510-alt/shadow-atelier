# R07 joint-kernel coefficient intersection v107

Author: Sol / 2026-08-27

Status: paper proof and executable reduction design.  It converts the
28-coordinate C-13 overapproximation of v106 into the coefficient image of
the already cross-checked finite **joint value kernel** from task 157ee.  No
new full computation has been run.  The result is still a projected
target6/presentation certificate, not a literal A.18 lift.  `verified=false`.

## 1. Two kernels which must be separated

Let (F=F(x,y)).  The fresh g760 target6 calculation uses the three
(Pi_4[3])-contexts

\[
 \omega_3:F\longrightarrow \Delta_3,
 \qquad K_3=\ker\omega_3,
\tag{1.1}
\]

where (|\Delta_3|=27).  Its frozen Schreier basis is

\[
 s_1,\ldots,s_{28},
 \qquad K_3\cong F_{28}.
\tag{1.2}
\]

This is the source of the 28 rows in v106.  It is an overapproximation because
an actual registered correction must be invisible not only in these three
projected contexts, but in the complete joint value gate.

The cross-checked task-157ee universe supplies the marked joint image

\[
 \Omega:F\longrightarrow G_{\rm joint}
 \leq Q_0\times E_3\times E_4^{31},
 \qquad K_{\rm joint}=\ker\Omega.
\tag{1.3}
\]

The three maps in (1.1) are projections of the 31-context data in (1.3),
followed by (E_4\twoheadrightarrow\Pi_4[3]).  Hence there is a surjection

\[
 p:G_{\rm joint}\twoheadrightarrow\Delta_3,
 \qquad p\Omega=\omega_3.
\tag{1.4}
\]

Put

\[
 Q=\ker p.
\tag{1.5}
\]

Restriction of (Omega) gives an exact sequence

\[
 \boxed{1\longrightarrow K_{\rm joint}
 \longrightarrow K_3\xrightarrow{\rho}Q\longrightarrow1.}
\tag{1.6}
\]

Surjectivity is immediate: if (q=\Omega(w)\in\ker p), then
(omega_3(w)=1), so (w\in K_3).  The kernel is (1.3).

If a later audit shows that the registered legal language has an additional
finite value gate not contained in (1.3), append that gate to (Omega).  The
proof below is unchanged.  In particular, a separate exponent-sum-mod-3 gate
can be appended as a factor ((\mathbf F_3)^2); it must not be silently
assumed to be encoded by (1.3).

## 2. The 31-context image is a linear subspace of the 28 coefficients

Let

\[
 \operatorname{ab}_3:K_3\longrightarrow
 H_1(K_3;\mathbf F_3)\cong\mathbf F_3^{28}
\tag{2.1}
\]

use the ordered basis (1.2), and define

\[
 B_{\rm joint}=\operatorname{ab}_3(K_{\rm joint})
 \subseteq\mathbf F_3^{28}.
\tag{2.2}
\]

### Theorem 2.1 (JOINT-KERNEL HOMOLOGY FILTER)

The subspace (2.2) is exactly

\[
 \boxed{
 B_{\rm joint}=\ker\!\left(
 H_1(K_3;\mathbf F_3)\longrightarrow H_1(Q;\mathbf F_3)
 \right).}
\tag{2.3}
\]

#### Proof

For any group (H),

\[
 H_1(H;\mathbf F_3)=H/(H^3[H,H]).
\tag{2.4}
\]

Apply this to the surjection (ho:K_3\twoheadrightarrow Q).  The kernel of
the induced map in (2.3) is

\[
 \frac{K_{\rm joint}K_3^3[K_3,K_3]}
      {K_3^3[K_3,K_3]},
\tag{2.5}
\]

which is precisely the image of (K_{\rm joint}) under
(operatorname{ab}_3).  This is (2.2).  (square)

Thus the genuine 31-context restriction does not require an unbounded word
search.  It is at most a (28\)-column linear calculation.

## 3. Computing the subspace from the existing exact presentation

Task 157ee did more than enumerate samples.  Its terminal
`B345_JOINT_KERNEL_QSTAR_CLOSED` supplied a complete finite presentation of
the marked joint image through:

1. all (6,318) Cayley-edge relations of the 243-state normal kernel;
2. all (104) (x/y)-action relations; and
3. the (19) complete (Q_0)-factor relations, whose defects normally
   generate that 243-state kernel.

The cross-checked full receipt is

```text
run       32359956713
receipt   ci/b345_157ee_artifacts_32359956713/
          d972_b345_joint_kernel_qstar_closure_v1.json
SHA-256   1c3ad7a7124cee152eb40968cf212c14641a9f8720063c85f70533864898d0df
```

Let (mathcal Rsubset F) be the defining relation words reconstructed from
those three layers, and let (T) be the frozen 27-element Schreier
transversal for (K_3\backslash F).  For (t\in T) and (r\in\mathcal R),
rewrite

\[
 R_{t,r}=\operatorname{Sch}_{K_3}(t r t^{-1})
\tag{3.1}
\]

as a word in (s_1,\ldots,s_{28}).  Every (R_{t,r}) belongs to
(K_{\rm joint}).

### Proposition 3.1 (FINITE ROW-SPAN FORMULA)

\[
 \boxed{
 B_{\rm joint}
 =\operatorname{span}_{\mathbf F_3}
 \{\operatorname{exp}_3(R_{t,r}):t\in T, r\in\mathcal R\}.}
\tag{3.2}
\]

#### Proof

The normal closure of (mathcal R) in (F) is (K_{\rm joint}), because
(mathcal R) presents (G_{\rm joint}).  Since (F) is the union of the
27 cosets (K_3t), its normal closure is, inside (K_3), normally generated
by the (t r t^{-1}).  Passing to the abelian exponent-3 quotient of (K_3)
kills conjugation and cubes.  Therefore their Schreier exponent rows span
exactly the image (2.2).  (square)

Only 28 pivots can survive.  The implementation should retain the
lexicographically first independent input rows together with their complete
relation words.  It need not retain a provenance vector with one coordinate
for every relation row.

## 4. Intersecting the g760 affine family with the joint kernel

Retain the notation of v106:

\[
 \mathcal A_j=
 \left\{a\in\mathbf F_3^{28}:
 t_j-\sum_i a_i\ell_{j,i}\in D_j\right\}.
\tag{4.1}
\]

The correct successor to the overapproximation certificate is

\[
 \boxed{\mathcal A_j^{\rm joint}
       =\mathcal A_j\cap B_{\rm joint}.}
\tag{4.2}
\]

Choose a (28\times d) matrix (U) whose columns are the retained basis of
(B_{\rm joint}).  Then (4.2) is computed without enumerating words by the
single affine system

\[
 L_jUz=q_j(t_j),
 \qquad z\in\mathbf F_3^d.
\tag{4.3}
\]

If (4.3) has a displayed solution (z), put (a=Uz).  For every column of
(U), retain an actual relation word (R_k\in K_{\rm joint}) having that
column as its Schreier exponent row.  Then

\[
 \boxed{c(z)=R_1^{z_1}\cdots R_d^{z_d}\in K_{\rm joint}}
\tag{4.4}
\]

is an explicit 31-context-invisible correction word.

The target6 map (Sigma_g:K_3\to V_j) is a homomorphism to an additive
(mathbf F_3)-space.  It therefore factors through (2.1), and direct word
replay must give

\[
 \Sigma_g(c(z))
 =\sum_i a_i\Sigma_g(s_i),
 \qquad
 t_j-\Sigma_g(c(z))\in D_j.
\tag{4.5}
\]

This is stronger than materializing the naive word
(prod_i s_i^{a_i}).  That naive word has the right mod-3 coefficient but
need not lie in (K_{\rm joint}).  Formula (4.4) lies there by construction.

## 5. Compatibility in Jennings depth

The subspace (B_{\rm joint}) is independent of (j), while v106 gives
(mathcal A_{j+1}\subseteq\mathcal A_j).  Hence

\[
 \boxed{
 \mathcal A_{j+1}^{\rm joint}
 \subseteq\mathcal A_j^{\rm joint}.}
\tag{5.1}
\]

All these sets lie in the same finite (mathbf F_3^{28}).  Consequently, if
they are nonempty at every Jennings depth of this fixed quotient, they
stabilize and have nonempty intersection.  Solving at the terminal nilpotent
depth returns one coefficient valid at every shallower Jennings truncation.

This is fixed-quotient compatibility only.  It is not the HT5 base-change
compatibility required by the pro-relative-dihedral theorem v82.

## 6. Exact promotion boundary

A nonempty (4.2), together with (4.4)--(4.5), would prove:

```text
one explicit g760 target6 correction
through the registered Q0/E3/31-E4 joint value gate
in the Pi4[3] Jennings quotient, modulo the registered D2 presentation image.
```

It would **not yet** prove a literal B4/A.18 lift.  Positive promotion still
requires all of the following, none of which is supplied by Theorem 2.1:

1. any legal-language gate not already contained in the pinned joint map;
2. removal of the positive-direction loss in (E_4\twoheadrightarrow\Pi_4[3]),
   or an exact blockwise reconstruction of the full (E_4) class;
3. the positive presentation comparison for (D_2) (C-12 proved the quotient
   direction needed for NO; equality with the true PB4 relation image remains
   a separate gate);
4. simultaneous replay of both hexagons and all five printed-order A.18
   cofaces for the same word; and
5. HT1--HT5 at every later abelian edge plus nonempty accepted sets at every
   nonabelian edge.

Thus (4.2) is the next honest positive gate: it closes the largest presently
visible gap between the 28-row overapproximation and the registered common
value-kernel, while preserving the distinction between a target6 certificate
and a cofinal lift.

## 7. Executable next step

After task 168 returns (mathcal A_9), the bounded successor is:

```text
J1  reconstruct the task-157ee defining relation words and their pins;
J2  rewrite their 27 transversal conjugates in the frozen 28 Schreier basis;
J3  row-reduce the resulting 28-column matrix and retain word-bearing pivots;
J4  solve A_9 intersect B_joint;
J5  materialize c(z) from relation words and replay all 31 values and target6;
J6  report the remaining projection/D2/literal-A18 gates without promotion.
```

No full-D2 closure is repeated in J1--J5: task 168's authenticated completed-j
checkpoint is consumed as an input.

```text
JOINT-KERNEL HOMOLOGY FILTER:                 PAPER_PROOF
FINITE 28-COLUMN PRESENTATION REDUCTION:      PAPER_PROOF
B_joint FOR THE PINNED 157ee UNIVERSE:         NOT YET COMPUTED
A_9:                                          WAITING FOR TASK 168 / GHA
A_9 INTERSECT B_joint:                        UNKNOWN
EXPLICIT 31-CONTEXT CORRECTION WORD:           NOT YET CONSTRUCTED
LITERAL A18 / COFINAL LIFT / IHARA WITNESS:    NOT DECLARED
```
