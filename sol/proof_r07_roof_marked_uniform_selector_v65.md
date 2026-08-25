# Roof-marked uniform relative selector v65

Author: Sol / 2026-08-25

Status: paper-proof candidate; `verified=false`, `cross_checked=false`.
This note strengthens the constructive strategy, not the final existence
claim.  It proves that a uniform search should freeze only roof row 9 during
the B4 recursion; freezing the exact K2 point R07 at every step is an
unnecessary restriction.

## 1. The two marks

Let

$$
G=GT_3(K2)\xrightarrow{\rho}X,
\qquad |X|=972,
\tag{1.1}
$$

and let $a\in X$ be zero-based row 9.  V61 proves

$$
\operatorname{ord}(a)=9,
\qquad a^4=\operatorname{row}36,
\qquad a\notin A_{\rm ar}.
\tag{1.2}
$$

The last assertion follows already from the fact that row 36 is outside the
arithmetic subgroup $A_{\rm ar}$: if $a$ were arithmetic, then so would be
$a^4$.

For the word coordinate, write

$$
q_{K2}:\widehat F_2\longrightarrow Q_{K2},
\qquad
q_9:\widehat F_2\longrightarrow Q_9
\tag{1.3}
$$

for finite evaluation coordinates which, with $m=0$ fixed, record
respectively the complete K2 word datum and the coarser 972-roof datum.
Reduction gives a map $r:Q_{K2}\to Q_9$ with

$$
q_9=rq_{K2}.
\tag{1.4}
$$

These are word-evaluation homomorphisms into finite groups.  No assertion
that multiplication of $f$-coordinates is the GT group law is being made.

At depth $n$, take the accumulated joint B4 evaluation map from v64 and
adjoin one of the two marks.  Denote the resulting kernels by

$$
U_n^{K2}:=\ker\Psi_n^{K2},
\qquad
U_n^{\rm roof}:=\ker\Psi_n^{\rm roof}.
\tag{1.5}
$$

Equation (1.4) gives

$$
\boxed{U_n^{K2}\le U_n^{\rm roof}.}
\tag{1.6}
$$

Thus a correction which fixes exact R07 also fixes row 9, but a row-9
correction is allowed to move inside the K2 fibre.

## 2. Roof-marked product theorem

Let $f_0$ be an explicit word which is admissible through an initial B4
window and whose 972-roof is row 9.  Suppose recursively that

$$
c_n\in U_n^{\rm roof},
\qquad f_{n+1}=f_nc_n,
\tag{2.1}
$$

and that $f_{n+1}$ passes all equations and side gates through level $n+1$.

### Theorem 2.1 (ROOF-MARKED-NESTED-PRODUCT)

If (2.1) can be continued through every level of one nested cofinal B4
ladder, then

$$
\boxed{f_\infty=f_0c_0c_1c_2\cdots}
\tag{2.2}
$$

converges in $\widehat F_2$, the pair $(0,f_\infty)$ belongs to the original
profinite $\widehat{GT}$, and its 972-roof is row 9.  In particular it is an
Ihara non-surjectivity witness.

#### Proof

The accumulated kernels are nested.  For $m>n$,

$$
f_n^{-1}f_m=c_nc_{n+1}\cdots c_{m-1}\in U_n^{\rm roof}.
\tag{2.3}
$$

Hence the partial products are Cauchy and have the limit (2.2).  At every
fixed B4 level all later corrections are invisible, so the relations and
side gates stabilize.  Cofinality and continuity put the limit in
$\widehat{GT}$, exactly as in v64, Theorem 3.1.

The coordinate $q_9$ is included in every accumulated evaluation map.
Therefore every correction has trivial $q_9$ value and the limit retains
the row-9 roof of $f_0$.  Equation (1.2) says that this roof is outside the
arithmetic image, which proves the last assertion. $\square$

The witness conclusion does not require a subsequent exactification.  If an
exact K2 label is nevertheless desired, apply the compatible profinite GT
group power from v61/v62:

$$
z=(0,f_\infty)
\quad\longmapsto\quad
z^{4\mathbf e_3},
\qquad
\mathbf e_3=(1\in\mathbf Z_3,0\in\mathbf Z_\ell\ (\ell\ne3)).
\tag{2.4}
$$

Its K2 coordinate is R07.  Formula (2.4) is applied in the profinite GT
group law after the limit has been constructed; it is not naive word
concatenation of the $f$-coordinate.

## 3. The strictly larger finite correction problem

Let $H_{n+1}^{\rm roof}\to H_n^{\rm roof}$ and
$H_{n+1}^{K2}\to H_n^{K2}$ be the two accumulated finite joint images.
As in v64, the complete one-step value domains are

$$
D_{n+1,n}^{\rm roof}
=\ker(H_{n+1}^{\rm roof}\to H_n^{\rm roof}),
\qquad
D_{n+1,n}^{K2}
=\ker(H_{n+1}^{K2}\to H_n^{K2}).
\tag{3.1}
$$

Under the natural reduction of joint images, the exact-marked domain maps
into the roof-marked domain.  Equivalently, at the word level (1.6) gives

$$
\boxed{
\text{exact-K2 corrections}\subseteq
\text{row-9-preserving corrections}.}
\tag{3.2}
$$

The inclusion can be strict.  Consequently an empty exact-R07 correction
fibre for one chosen prefix is not an obstruction to the witness: another
correction may move the K2 component while preserving row 9 and all earlier
B4 equations.

The deterministic finite procedure is now:

1. retain all admissible row-9 states at depth $n$;
2. for each state enumerate the complete finite domain
   $D_{n+1,n}^{\rm roof}$;
3. evaluate the literal two hexagons, ordered pentagon, descent, charming,
   and onto gates;
4. retain all passing children, with a shortlex word representative in
   $F_2\cap U_n^{\rm roof}$.

This computes the complete finite frontier.  It is uniform and cannot lose
a witness by insisting on R07 too early.

## 4. The correct explicit relative-dihedral target

For a backtracking-free construction, let $E_n^{(9)}$ be a specified class
of admissible row-9 prefixes.  It is enough to construct formulas

$$
\kappa_{n+1}^{(9)}:E_n^{(9)}\longrightarrow U_n^{\rm roof}
\tag{4.1}
$$

such that

$$
f\,\kappa_{n+1}^{(9)}(f)\in E_{n+1}^{(9)}
\qquad(f\in E_n^{(9)}).
\tag{4.2}
$$

Starting with one $f_0\in E_0^{(9)}$, equations (4.1)--(4.2) and Theorem
2.1 give the desired explicit infinite product.  This is the precise
uniform relative-dihedral lift theorem still being sought.

The preceding closed formulas already define pieces of $\kappa^{(9)}$ on
formation-free, prime-to-three, lower-central, typed abelian, and peelable
$PSL(2,8)$ chief stages.  They may now use the larger kernel
$U_n^{\rm roof}$ rather than $U_n^{K2}$.  The unresolved assertion is that
one of the allowed formulas exists and preserves $E^{(9)}$ at every active
coupled B4 chief step.

Thus the explicit-lift programme has not been displaced by compactness.  Its
target has been sharpened:

$$
\boxed{
\text{preserve one coarse nonarithmetic row uniformly first;}
\quad\text{normalize to R07 only at the end}.}
\tag{4.3}
$$

## 5. Boundary

This note proves the relaxation (1.6), the roof-marked product theorem, and
the exact form (4.1)--(4.2) of a uniform selector.  It does not prove that
the next-step row-9 fibre is nonempty at every remaining coupled chief
stage.  Hence it does not yet declare the 972 witness.

## 6. Sources

- `sol/proof_r07_row9_power_bridge_v61.md`.
- `sol/proof_r07_one_bit_roof_fullness_v62.md`.
- `sol/proof_r07_uniform_nested_correction_product_v64.md`.
- `sol/proof_relative_dihedral_b3_and_b4_small_window_v3.md`.
- `sol/proof_relative_formation_residual_exact_correction_domain_v37.md`.
