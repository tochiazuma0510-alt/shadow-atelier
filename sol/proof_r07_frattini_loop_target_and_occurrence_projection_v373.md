# R07 Frattini loop target and occurrence projection v373

Author: Sol / 2026-08-30

Status: **REJECTED DRAFT; superseded by v374.**  The Fox-path
fibre retained by v372 is canonically the endpoint obstruction in the next
relative Frattini quotient.  This identifies the exact finite localized
target at every successor and gives a canonical projection of the task395
eleven-occurrence closure onto the actual first-successor correction image.
It does not prove that the actual defect belongs to that image at the first
or every later successor.  No compatible lift, fake certificate or Ihara
witness is declared.  verified=false.  Independent audit found an unproved
extension of the loop projection from seed columns to all of \(W_C\), an
undefined algebraic source in (3.3), and subsidiary typing/naturality gaps.
Nothing in this draft is promoted.

## 1. A coarse Fox loop is the next endpoint

Fix one marked PB3 or PB4 block (B).  Write

\[
 K_{B,n+1}=\Phi _3(K_{B,n})=K_{B,n}^3[K_{B,n},K_{B,n}],
 \qquad
 E_{B,n}=P_B/K_{B,n},
\tag{1.1}
\]

and put

\[
 V_{B,n}=K_{B,n}/K_{B,n+1}
 =H_1(K_{B,n};\mathbf F _3).
\tag{1.2}
\]

For the complete fixed presentation of (P_B), let

\[
 C_{2,B,n}\xrightarrow{D_{2,B,n}}C_{1,B,n}
 \xrightarrow{D_{1,B,n}}\mathbf F _3[E_{B,n}]
\tag{1.3}
\]

be the evaluated cellular complex and set

\[
 \mathcal R_{B,n}=C_{1,B,n}/\operatorname {im}D_{2,B,n}.
\tag{1.4}
\]

Since the marked presentation generators generate (E_{B,n}), the image of
(D_{1,B,n}) is its augmentation ideal (I(E_{B,n})).  Hence there is a
canonical exact sequence

\[
 \boxed{
 0\longrightarrow V_{B,n}
 \xrightarrow{\theta _{B,n}}\mathcal R_{B,n}
 \xrightarrow{\overline D_{1,B,n}}I(E_{B,n})
 \longrightarrow0.}
\tag{1.5}
\]

Here \(\theta _{B,n}\) sends the class of \(w\in K_{B,n}\) to the class of
its evaluated Fox path.  This is v145 Lemma 2.1, with the non-loop part of
the cellular one-chain retained as in v372.

### Theorem 1.1 (LOOP--SUCCESSOR ENDPOINT IDENTIFICATION)

For every (w\in K_{B,n}), the two classes

\[
 [\partial _{B,n}w]\in\ker\overline D_{1,B,n},
 \qquad
 wK_{B,n+1}\in\ker(E_{B,n+1}\to E_{B,n})
\tag{1.6}
\]

correspond under the canonical identifications with (V_{B,n}).  In
particular,

\[
 \boxed{
 [\partial _{B,n}w]=0
 \quad\Longleftrightarrow\quad
 w=1\text{ in }E_{B,n+1}.}
\tag{1.7}
\]

The identification is (E_{B,n})-equivariant and commutes with every marked
coface, deletion and refinement map.

#### Proof

The left class in (1.6) is, by the edge-path realization of cellular
homology, the image of (w) in

\[
 H_1(K_{B,n};\mathbf F _3)
 =K_{B,n}/K_{B,n}^3[K_{B,n},K_{B,n}].
\tag{1.8}
\]

By (1.1), the right class is the image of the same word in the same quotient.
This proves (1.7).  Deck transformation of the covering realizes conjugation
by (E_{B,n}), so the identification is equivariant.  Fox paths, cubes and
commutators are functorial under the registered homomorphisms, proving the
last assertion.  \(\square\)

Thus the loop fibre which invalidated the endpoint-only v371 descent is not
an auxiliary ambiguity.  It is exactly the next group-valued obstruction.

## 2. The exact localized successor layer

Let (N_{B,n+1}\triangleleft E_{B,n+1}) be the supported subgroup required
at the fine level.  For the two hexagon blocks take

\[
 N_{B,n+1}=R_S(E_{B,n+1}),
\tag{2.1}
\]

and for the pentagon block take

\[
 N_{P,n+1}=B_{P,n+1}\cap R_S(E_{P,n+1}),
\tag{2.2}
\]

where (B_{P,n+1}) is the registered image of the Brunnian subgroup.  Define
the finite local successor layer

\[
 T_{B,n}=V_{B,n}\cap N_{B,n+1}.
\tag{2.3}
\]

### Proposition 2.1 (SUPPORTED LOOP LAYER)

Suppose a block residual word (W) is trivial in (E_{B,n}).  Its exact
obstruction to being trivial in (E_{B,n+1}) is an element

\[
 \beta _{B,n}=WK_{B,n+1}\in V_{B,n}.
\tag{2.4}
\]

If the fine endpoint of (W) is required by the relative arithmetic and
commutator typing to lie in (N_{B,n+1}), then

\[
 \boxed{\beta _{B,n}\in T_{B,n}.}
\tag{2.5}
\]

Conversely, the Fox-loop class of \(W\) at level \(n\) is
\(\theta _{B,n}(\beta _{B,n})\).  Therefore \(T_{B,n}\), rather than the
whole coarse loop fibre, is the exact supported target for the next
successor.

#### Proof

Triviality at level (n) puts (W) in (K_{B,n}), so (2.4) follows from
(1.2).  Fine support puts the same endpoint in (N_{B,n+1}), proving
(2.5).  The final assertion is Theorem 1.1.  \(\square\)

The distinction between coarse and fine support is load-bearing.  The v372
module

\[
 \overline D_{1,B,n}^{-1}(I(N_{B,n}))
\tag{2.6}
\]

contains all of (ker\overline D_{1,B,n}), because every loop has coarse
endpoint one.  It consequently cannot by itself separate the supported and
unsupported next endpoints.  The fine subgroup in (2.3) supplies precisely
that missing leading-layer condition.

For an aligned formation tower, v153 makes (2.3) explicit.  Let (P_B^S)
be the inverse image in (P_B) of (R_S(E_{B,0})), and put

\[
 P_{B,n}^S=\Phi _3^n(P_B^S).
\tag{2.7}
\]

Then

\[
 R_S(E_{B,n+1})=P_{B,n+1}^S/K_{B,n+1}
\tag{2.8}
\]

and hence

\[
 \boxed{
 T_{B,n}^{S}
 =\frac{K_{B,n}\cap P_{B,n+1}^S}{K_{B,n+1}}.}
\tag{2.9}
\]

At the first authenticated superperfect (PSL(2,8)) edge, v151 gives the
equivalent action formula

\[
 \boxed{T_{B,0}^{S}=[R_S(E_{B,0}),V_{B,0}].}
\tag{2.10}
\]

For the pentagon one intersects (2.9) with
(V_{P,n}\cap B_{P,n+1}); no image--intersection interchange is assumed.

Put

\[
 Z_n^{\rm loc}=
 T_{H1,n}^{S}\oplus T_{H2,n}^{S}\oplus
 \bigl(T_{P,n}^{S}\cap B_{P,n+1}\bigr).
\tag{2.11}
\]

Every exact relative/commutator residual which has already been killed
through rung (n) has its next obstruction in (2.11), by v252 and
Proposition 2.1.

## 3. Canonical projection of the eleven-occurrence closure

At the first edge, retain the task370 raw separately tagged chain space
(V_{\rm raw}), its eleven signed prefix columns, and its four-generator
closure (W_C\).  Let

\[
 \operatorname {Agg}:V_{\rm raw}\longrightarrow
 \mathcal R_{H1,0}\oplus\mathcal R_{H2,0}\oplus\mathcal R_{P,0}
\tag{3.1}
\]

sum the occurrences in printed block order and quotient by the complete
PB3/PB4 boundary modules.  A task382 seed is roof-trivial in every retained
context, so every aggregated seed column has endpoint boundary zero.
Theorem 1.1 therefore defines the canonical loop projection

\[
 \lambda _0=
 (\theta _{H1,0}^{-1}\oplus\theta _{H2,0}^{-1}
       \oplus\theta _{P,0}^{-1})\operatorname {Agg}
 :W_C\longrightarrow
 V_{H1,0}\oplus V_{H2,0}\oplus V_{P,0}.
\tag{3.2}
\]

No inverse is applied outside the three loop kernels.

### Theorem 3.1 (OCCURRENCE CLOSURE PROJECTS TO THE ACTUAL SUCCESSOR IMAGE)

After the task198/task382 owner, complete boundary modules, signs, prefixes
and simultaneous action are physically authenticated, let

\[
 D_0:C_{\rm rel}^{\rm alg}\longrightarrow
 V_{H1,0}\oplus V_{H2,0}\oplus V_{P,0}
\tag{3.3}
\]

be the exact first-successor affine correction map on the group-algebra span
of the registered relative seeds.  Then

\[
 \boxed{\lambda _0(W_C)=\operatorname {im}D_0.}
\tag{3.4}
\]

Moreover the image of every legally typed column lies in
(Z_0^{\rm loc}).

#### Proof

V370 Lemma 1.1 identifies each seed column before aggregation with the
literal first Fox difference of the two hexagons and printed pentagon.
Aggregation and quotient by the complete boundary modules therefore give
the three coarse Fox-loop classes of that first difference.  Theorem 1.1
identifies those loop classes with the three successor endpoints, which are
exactly the affine map (3.3) of v99.  V370 Lemma 2.1 shows that simultaneous
translation on (W_C) agrees with the common group-algebra action, and v370
Theorem 3.1 says the exhausted closure is the image of the full registered
seed ideal.  These statements prove (3.4).  Relative/commutator typing and
Proposition 2.1 give the last assertion.  \(\square\)

Equation (3.4) is deliberately not the assertion
(W_C=L/JL).  It gives a smaller and exact statement: after the displayed
projection, task395 computes the actual first-successor correction image.
Consequently the first finite decision can be made directly in the target
(2.11), without choosing a path for an endpoint and without first proving
ordinary (J)-adic saturation of the completed localized module.

## 4. Exact successor criterion and the all-rung boundary

Let (F_n) satisfy the two hexagons and pentagon through rung (n), and let

\[
 \beta _n\in Z_n^{\rm loc}
\tag{4.1}
\]

be the three next endpoints, equivalently the three coarse Fox-loop classes.
Let (C_n^{\rm rel}) be the actual one-common-word relative correction layer
and let

\[
 D_n:C_n^{\rm rel}\longrightarrow Z_n^{\rm loc}
\tag{4.2}
\]

be the exact affine map.

### Theorem 4.1 (ONE-SUCCESSOR NECESSARY AND SUFFICIENT TEST)

A legal correction (c_n) which is invisible through rung (n) extends
(F_n) through rung (n+1) if and only if

\[
 \boxed{D_n[c_n]=-\beta _n.}
\tag{4.3}
\]

Every later correction from (C_m^{\rm rel}), (m>n), leaves (4.3) and
all earlier equations unchanged.

#### Proof

At the elementary-abelian transition, v99 gives the exact affine identity

\[
 \beta _n(F_nc_n)=\beta _n(F_n)+D_n[c_n].
\tag{4.4}
\]

Theorem 1.1 says that vanishing of this vector is equivalent to the three
literal relation words being trivial at the fine level.  This proves (4.3).
For (m>n), the correction lies in the next kernel below (K_{B,n+1}), so
its image in (V_{B,n}) is zero.  \(\square\)

This theorem gives a direct rung-by-rung route which does not use the
ordinary strict-(L/JL) hypothesis of v319.  It does not remove the
quantifier over all rungs.  A positive first-edge membership proves only one
successor.

For completeness, let (X_n) be the finite set of all registered relative
words at level (n) satisfying the roof, commutator, formation, Brunnian and
literal relation gates through that level.  Reduction maps (X_{n+1}) into
(X_n).  If (X_n\ne\varnothing) for every (n), the resulting finitely
branching tree has vertices at every depth, so Koenig compactness gives one
compatible pro-(3) branch.  This removes compatibility of separately found
finite solutions; it does not prove their nonemptiness.

There are therefore two honest ways to close the remaining pro-(3) tail:

1. prove (4.3) soluble at every rung, structurally or by complete finite
   accepted sets, and apply compactness; or
2. produce one natural completed identity, such as the v191 universal
   word-pair boundary identity or the v369 completed based right inverse,
   which proves all the equations simultaneously.

## 5. Exact advance and remaining gates

The path-bearing state of v372 and the all-rung formation formula of v153
now meet at a canonical finite object:

\[
 \boxed{
 \text{coarse Fox loop}
 \;=\;
 \text{next Frattini endpoint}
 \;\in\;
 Z_n^{\rm loc}.}
\tag{5.1}
\]

This removes an unnecessary path section and removes ordinary localized
saturation from the **direct one-successor decision**.  It also gives the
precise post-task395 consumer: aggregate, quotient by complete boundaries,
apply the loop--endpoint identification, and compare the actual
(-\beta _0) with the resulting image.

It does not turn one first-edge MEMBER into an all-rung theorem.  The
completed Newton route still needs either its strict/weighted target and
leading onto certificate, or a pointed/universal identity.  Physical
task198/task382 ownership and actual numerical membership remain mandatory.

```text
FOX LOOP = NEXT FRATTINI ENDPOINT:                  PAPER PROOF
FORMATION-SUPPORTED SUCCESSOR LAYER (2.9):          PAPER PROOF / v153
PENTAGON BRUNNIAN INTERSECTION:                     EXACT DEFINITION
TASK395 RAW CLOSURE -> ACTUAL D_0 IMAGE:             PAPER PROOF / ABI-CONDITIONAL
DIRECT ONE-SUCCESSOR TEST WITHOUT L/JL SATURATION:   PAPER PROOF
ACTUAL TASK395 CLOSURE AND FIRST MEMBERSHIP:         NOT COMPUTED
ALL-RUNG MEMBERSHIP OR NATURAL COMPLETED IDENTITY:   OPEN
COMPATIBLE RELATIVE PRO-3 LIFT:                     NOT CONSTRUCTED
MIXED-PRIME / PERFECT-CORE / SETTLEMENT:             OPEN
FAKE / IHARA WITNESS:                               NOT DECLARED
```

`R07_FRATTINI_LOOP_TARGET_AND_OCCURRENCE_PROJECTION_V373_PAPER_GRADE`
