# R07 A0: affine truncated engine for both post-2016 rungs (v443)

Author: Sol / 2026-09-03

Status: candidate implementation theorem, conditional on the independent
audit of the v442 affine tables and on an accepted literal order-2016
correction.  It turns v441's abstract transversal/cocycle requirements into
closed coordinate operations.  It does not assert that any positive grade is
MEMBER and does not declare A0, COMMON, a cofinal lift, fake, or Ihara.
`verified=false`.

## 1. One truncated polynomial ring, not a larger group table

Let

\[
 T_{\le d}=\mathbf F_3[u_1,u_2,u_3]/
 (u_1^3,u_2^3,u_3^3,\text{monomials of total degree }>d),
 \qquad 0\leq d\leq6.                              \tag{1.1}
\]

For (v=(v_1,v_2,v_3)\in\mathbf F_3^3), put

\[
 E(v)=\prod_{i=1}^3(1+u_i)^{v_i}\in T_{\le d}.      \tag{1.2}
\]

All exponents in (1.2) are their representatives (0,1,2).  Since
((1+u_i)^3=1), (E(v+w)=E(v)E(w)).  A signed permutation matrix (M)
acts through the exact algebra automorphism

\[
 \phi_M(E(v))=E(Mv).                                \tag{1.3}
\]

In particular a negative column gives

\[
 u_i\longmapsto (1+u_{\sigma(i)})^{-1}-1
 =2u_{\sigma(i)}+u_{\sigma(i)}^2,                   \tag{1.4}
\]

not merely its linear term.  Equations (1.1)--(1.4), sparse coefficient
maps keyed by the 27 possible monomials, and quotient coordinates suffice
for every precision.  No multiplication table for a 54,432- or
1,469,664-element group is required.

## 2. Normal form for the split first rung

Write (P=PSL(2,8)), (A=\langle s_X,s_Y\rangle\cong C_2^2), and
(V=N/N^3\cong C_3^3).  With the v442 right-action convention, put

\[
 Q_1=P\times A,
 \qquad \widetilde Q_1=P\times(V\rtimes A)=Q_2.
\]

Let (S(a)) be the diagonal sign action of (a\in A), let
(sigma(p,a)=(p,0,a)), and put (n(v)=(1,v,0)).  Every element has the
unique **section-left, kernel-right** form

\[
 g=\sigma(q)\star n(v),\qquad q=(p,a)\in Q_1.       \tag{2.1}
\]

If (q'=(p',b)), the group law is

\[
 (\sigma(q)n(v))\star(\sigma(q')n(w))
 =\sigma(q\star q')n(S(b)v+w).                      \tag{2.2}
\]

Therefore the truncated group algebra has the canonical vector-space basis

\[
 [p,a]u^\alpha,qquad |\alpha|\leq d,               \tag{2.3}
\]

and its product is the closed formula

\[
 \boxed{
 ([p,a]f)\,([p',b]g)
 =[p\star p',a+b]\,\rho_b(f)g,}
 \qquad \rho_b(E(v))=E(S(b)v).                      \tag{2.4}
\]

This formula fixes the otherwise dangerous left/right ambiguity: the parity
of the **right** quotient coordinate acts on the kernel polynomial of the
left factor.

The marked lifts have kernel coordinates

\[
 v_X=(1,0,0),\qquad v_Y=(1,1,1),                    \tag{2.5}
\]

and hence

\[
 v_{X^{-1}}=(-1,0,0),\qquad
 v_{Y^{-1}}=(1,-1,1).                               \tag{2.6}
\]

Indeed, in section-left normal form

\[
 (q,v)^{-1}=(q^{-1},-S(a)v)                         \tag{2.7}
\]

when the (A)-part of (q) is (a).

## 3. Exact actor, occurrence, and prefix operators on the first rung

Let a source actor (ell) have normal coordinates
(sigma(q_\ell)n(v_\ell)), and let (a) be the (A)-part of a row
coordinate (q).  Left translation is

\[
 \boxed{
 L_\ell([q]f)=[q_\ell\star q]\,
 E(S(a)v_\ell)f.}                                   \tag{3.1}
\]

Thus actor closure is performed directly on the truncated coordinates; the
kernel factor is allowed to raise degree and is never replaced by its
constant or linear part.

For occurrence (j), let (alpha_j^P), (A_j), (M_j), and (c_j) be
the independently audited v442 data.  Then

\[
 \boxed{
 \alpha_j([p,a]f)
 = [\alpha_j^P(p),A_ja]\,E(c_j(a)\bmod3)\phi_{M_j}(f).}       \tag{3.2}
\]

The crossed law for (c_j) is essential to (3.2).  Treating the two listed
values (c_j(s_X),c_j(s_Y)) as an ordinarily additive map would be wrong.

Every fixed (g_{760}) prefix is just another instance of (3.1), after its
normal coordinates are obtained by repeated use of (2.4).  Hence the six
occurrence maps, four correlated source actors, and all physical prefix
operators share one arithmetic kernel.  They do not share one action after
physical aggregation; v441's occurrence-first order is unchanged.

## 4. Normal form for the nonsplit carry rung

For the second extension, the quotient coordinate is

\[
 q=(p,\bar r,a)\in
 Q_2=P\times(C_3^3\rtimes A),                       \tag{4.1}
\]

where (ar r\in\mathbf F_3^3).  Let
(d:\mathbf F_3^3\to\{0,1,2\}^3\subset(\mathbf Z/9)^3) be the fixed
digit section and let (K=3(\mathbf Z/9)^3\cong C_3^3).  Again choose
section-left, kernel-right normal form

\[
 \sigma(p,\bar r,a)n(k),qquad k\in K.              \tag{4.2}
\]

For (q'=(p',\bar s,b)), quotient multiplication and its carry are

\[
 q\star q'=(p\star p',S(b)\bar r+\bar s,a+b),       \tag{4.3}
\]

\[
 \omega(q,q')=
 \frac{S(b)d(\bar r)+d(\bar s)
 -d(S(b)\bar r+\bar s\bmod3)}{3}\pmod3.            \tag{4.4}
\]

The numerator is taken in integer coordinates before division.  The exact
truncated product is

\[
 \boxed{
 ([q]f)([q']g)
 =[q\star q']E(\omega(q,q'))\rho_b(f)g.}             \tag{4.5}
\]

If (ell=sigma(q_\ell)n(k_\ell)), its left action is consequently

\[
 \boxed{
 L_\ell([q]f)=[q_\ell\star q]
 E(S(a)k_\ell+\omega(q_\ell,q))f.}                 \tag{4.6}
\]

The marked positive actors have (k_X=k_Y=0).  With the digit section above,
the inverse actors have

\[
 k_{X^{-1}}=(2,0,0),\qquad k_{Y^{-1}}=(0,2,0).       \tag{4.7}
\]

These values are not guessed inverse signs; they are the carries in the
representatives (8=2+3\cdot2) in the affected coordinates.

For occurrence (j), define

\[
 \bar\alpha_j(p,\bar r,a)=
 (\alpha_j^P(p),M_j\bar r+c_j(a)\bmod3,A_ja),       \tag{4.8}
\]

and

\[
 \kappa_j(\bar r,a)=
 \frac{M_jd(\bar r)+c_j(a)
 -d(M_j\bar r+c_j(a)\bmod3)}{3}\pmod3.             \tag{4.9}
\]

Then the exact occurrence operator is

\[
 \boxed{
 \alpha_j([q]f)
 =[\bar\alpha_j(q)]E(\kappa_j(\bar r,a))\phi_{M_j}(f).}       \tag{4.10}
\]

Equations (4.3)--(4.10) are the complete second-rung multiplication,
actor, prefix and occurrence arithmetic.  No generic transversal lookup is
left.

## 5. Literal Fox rows use the same coordinate engine

For a word (w=z_1\cdots z_m) in (x^{\pm1},y^{\pm1}), keep its running
prefix in the appropriate normal form.  For a positive letter, add the
current prefix to that generator component and then multiply by the marked
generator.  For a negative letter, first multiply by the marked inverse and
then subtract the resulting prefix.  This is exactly the evaluator convention
used by the accepted coarse artifacts.

Apply this rule after each of the six registered substitutions, retain all
six tags, and apply the pinned PB3 normal map componentwise in the truncated
ring.  Only after actor closure is exhausted may the fixed signed H1/H2
aggregation and prefix translations be applied.  Normalized exponent remains
an additional lower coordinate computed integrally before reduction.

For a MEMBER update, every echelon operation carries a sparse formal
combination of literal `(seed, actor-path)` leaves.  Because every substituted
base relator is an identity in the marked finite group, the Fox product rule
for a product of selected conjugates reduces exactly to addition.  Thus the
literal correction is both the output certificate and the input to the next
precision; no separate word-recovery search is needed.

## 6. Exact first-rung sizes and a bounded first executable

Let

\[
 H_d=\sum_{i=0}^d[t^i](1+t+t^2)^3
 =(1,4,10,17,23,26,27)_d.                           \tag{6.1}
\]

For the first extension, precision (d+1) has

\[
 12\,|Q_1|H_d\quad\text{occurrence coordinates},
 \qquad4\,|Q_1|H_d\quad\text{physical coordinates}.             \tag{6.2}
\]

The exact cumulative sizes are:

```text
highest degree d       0       1        2        3        4        5        6
occurrence          24192   96768   241920   411264   556416   628992   653184
physical             8064   32256    80640   137088   185472   209664   217728
```

The new grade-one block alone is 72,576 occurrence and 24,192 physical
coordinates.  Consequently the first faithful executable should implement
only the (d=1) fibre test at precision two, while already using the generic
formulas (1.1)--(3.2).  It must:

1. consume an independently accepted order-2016 literal correction;
2. evaluate the original 44 seeds at precision two;
3. exhaust the four correlated actors in the full occurrence module;
4. aggregate afterwards and perform v441 lower-first/fibre elimination;
5. test the actual grade-one residual;
6. return either a full-grade dual or a coefficient-bearing literal update.

This is a finite exact test, but (6.2) is not a rank or runtime bound.  A
producer must emit progress and stop fail-closed on the registered resource
cap.  A positive literal replay can certify MEMBER without making an
independent checker rerun the discovery echelon; discovery ranks must then be
reported as telemetry, exactly as at the order-2016 floor.

## 7. The second-rung resource boundary

For the second extension replace (|Q_1|=2016) by (|Q_2|=54,432) in
(6.2).  In particular precision two has 2,612,736 occurrence and 870,912
physical coordinates, while precision seven reaches 17,635,968 and
5,878,656.  These numbers still require no group multiplication table, but
they make an external bounded run plausible for later grades.  The decision
between local execution and GHA is an implementation/runtime decision made
after the first-rung engine is measured; it is not part of this theorem.

## 8. Claim boundary

Conditional on v442's independent table audit, this paper closes the exact
coordinate arithmetic required by v441 for both extensions.  It does not
close any of the twelve image-fibre membership tests.

```text
ORDER-2016 LITERAL MEMBER:             EXTERNAL INPUT; AUDIT PENDING
Q1 -> Q2 TRUNCATED ARITHMETIC:         PAPER-EXPLICIT; AUDIT PENDING
Q2 -> Q0 TRUNCATED ARITHMETIC:         PAPER-EXPLICIT; AUDIT PENDING
Q1 -> Q2 GRADE 1:                      READY FOR BOUNDED IMPLEMENTATION AFTER AUDIT
REMAINING ELEVEN POSITIVE GRADES:      NOT RUN
FULL-Q0 / A0 / COMMON / COFINAL LIFT:  NOT DECIDED
FAKE / IHARA:                          NOT DECLARED
verified:                              false
```

`R07_A0_AFFINE_TRUNCATED_TWO_RUNG_ENGINE_V443_CANDIDATE`
