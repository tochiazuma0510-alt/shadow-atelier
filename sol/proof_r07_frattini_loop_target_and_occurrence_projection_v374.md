# R07 Frattini loop target and occurrence projection v374

Author: Sol / 2026-08-30

Status: corrected paper theorem after the rejected v373 draft and after
v145, v151, v153, v252, v370 and v372.  The Fox-path fibre retained by
v372 is canonically the endpoint obstruction in the next relative Frattini
quotient.  The theorem identifies the exact finite supported target at every
successor.  It also proves, through a formal action module, that the
task395 eleven-occurrence closure projects onto the image of the actual
first-successor affine correction map, conditional on the named physical
owners.  Actual membership at the first or all later successors remains
open.  No compatible lift, fake certificate or Ihara witness is declared.
verified=false.

## 1. A coarse Fox loop is the next endpoint

Fix one marked PB3 or PB4 block \(B\).  Write

\[
 K_{B,n+1}=\Phi _3(K_{B,n})
 =K_{B,n}^3[K_{B,n},K_{B,n}],
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

For the complete fixed presentation of \(P_B\), let

\[
 C_{2,B,n}\xrightarrow{D_{2,B,n}}C_{1,B,n}
 \xrightarrow{D_{1,B,n}}\mathbf F _3[E_{B,n}]
\tag{1.3}
\]

be the evaluated cellular complex and set

\[
 \mathcal R_{B,n}
 =C_{1,B,n}/\operatorname {im}D_{2,B,n}.
\tag{1.4}
\]

The marked presentation generators generate \(E_{B,n}\), so the image of
\(D_{1,B,n}\) is the augmentation ideal \(I(E_{B,n})\).  Thus there is a
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

For every \(w\in K_{B,n}\), the two classes

\[
 [\partial _{B,n}w]\in\ker\overline D_{1,B,n},
 \qquad
 wK_{B,n+1}\in\ker(E_{B,n+1}\to E_{B,n})
\tag{1.6}
\]

correspond under the canonical identifications with \(V_{B,n}\).  In
particular,

\[
 \boxed{
 [\partial _{B,n}w]=0
 \quad\Longleftrightarrow\quad
 w=1\text{ in }E_{B,n+1}.}
\tag{1.7}
\]

The identification is \(E_{B,n}\)-equivariant.  It is natural for every
registered homomorphism \(f:P_B\to P_{B'}\) which satisfies

\[
 f(K_{B,n})\subseteq K_{B',n}
\tag{1.8}
\]

and whose authenticated Fox chain map sends the complete boundary module
\(\operatorname {im}D_{2,B,n}\) into
\(\operatorname {im}D_{2,B',n}\).

#### Proof

The left class in (1.6) is, by the edge-path realization of cellular
homology, the image of \(w\) in

\[
 H_1(K_{B,n};\mathbf F _3)
 =K_{B,n}/K_{B,n}^3[K_{B,n},K_{B,n}].
\tag{1.9}
\]

By (1.1), the right class is the image of the same word in the same
quotient.  This proves (1.7).  Deck transformation of the covering realizes
conjugation by \(E_{B,n}\), giving equivariance.  Under (1.8), the group
map sends cubes and commutators into cubes and commutators.  The
authenticated chain-map condition makes passage modulo complete
\(D_2\)-boundaries well-defined, and Fox naturality makes the square
commute.  \(\square\)

The loop fibre which invalidated the endpoint-only v371 descent is therefore
not an auxiliary ambiguity.  It is exactly the next group-valued
obstruction.

## 2. The exact supported successor layer

We first record the blockwise form of the v153 argument without assuming
that the ambient presentation group is free.

### Lemma 2.1 (FINITE-GENERATED ALIGNED FORMATION FORMULA)

Let \(Q\) be finitely generated, let \(K\triangleleft Q\) have finite
index, and put

\[
 E_0=Q/K,\qquad R=R_S(E_0),\qquad P=q^{-1}(R).
\tag{2.1}
\]

Define

\[
 K_n=\Phi _3^n(K),\qquad P_n=\Phi _3^n(P),\qquad E_n=Q/K_n.
\tag{2.2}
\]

Then every \(E_n\) is finite and

\[
 \boxed{R_S(E_n)=P_n/K_n.}
\tag{2.3}
\]

Consequently

\[
 \boxed{
 (K_n/K_{n+1})\cap R_S(E_{n+1})
 =\frac{K_n\cap P_{n+1}}{K_{n+1}}.}
\tag{2.4}
\]

#### Proof

The finite-index groups \(K\) and \(P\) are finitely generated.  Hence
\(K/K_n\) and \(P/P_n\) are finite \(3\)-groups, so \(E_n\) is finite.
There is an extension

\[
 1\longrightarrow P/P_n\longrightarrow Q/P_n
 \longrightarrow Q/P\longrightarrow1.
\tag{2.5}
\]

The kernel is a finite \(3\)-group and
\(Q/P\cong E_0/R\) lies in the no-\(S\) formation.  Extension closure gives
\(Q/P_n\) in that formation, and therefore

\[
 R_S(E_n)\leq P_n/K_n.
\tag{2.6}
\]

Conversely let \(N\triangleleft Q\), \(K_n\leq N\), and
\(Q/N\) lie in the formation.  The quotient by \(N K\) shows from the
definition of \(R\) that \(P\leq N K\).  Thus the images of \(P\) and
\(K\) in \(Q/N\) coincide.  Epimorphisms commute with \(\Phi _3^n\), so
the images of \(P_n\) and \(K_n\) coincide.  The latter is trivial, hence
\(P_n\leq N\).  Intersecting all such \(N\) proves the reverse inclusion
in (2.6), hence (2.3).  Intersect (2.3) at level \(n+1\) with the
transition kernel \(K_n/K_{n+1}\) to obtain (2.4).  \(\square\)

Return to one block.  Let
\(N_{B,n+1}\triangleleft E_{B,n+1}\) be the supported subgroup required
at the fine level.  For a hexagon block set

\[
 N_{B,n+1}=R_S(E_{B,n+1}),
\tag{2.7}
\]

and for the pentagon block set

\[
 N_{P,n+1}
 =B_{P,n+1}\cap R_S(E_{P,n+1}),
\tag{2.8}
\]

where \(B_{P,n+1}\) is the registered image of the Brunnian subgroup.
Define

\[
 T_{B,n}=V_{B,n}\cap N_{B,n+1}.
\tag{2.9}
\]

### Proposition 2.2 (SUPPORTED LOOP LAYER)

Suppose a block residual word \(W\) is trivial in \(E_{B,n}\).  Its exact
obstruction to being trivial in \(E_{B,n+1}\) is

\[
 \beta _{B,n}=WK_{B,n+1}\in V_{B,n}.
\tag{2.10}
\]

If its fine endpoint lies in \(N_{B,n+1}\), then

\[
 \boxed{\beta _{B,n}\in T_{B,n},\qquad
 [\partial _{B,n}W]=\theta _{B,n}(\beta _{B,n}).}
\tag{2.11}
\]

#### Proof

Coarse triviality puts \(W\) in \(K_{B,n}\), while fine support puts its
class in \(N_{B,n+1}\).  This proves membership in the intersection (2.9).
The equality of classes is Theorem 1.1.  \(\square\)

Apply Lemma 2.1 with \(Q=P_B\), \(K=K_{B,0}\), and let \(P_B^S\) be the
inverse image of \(R_S(E_{B,0})\).  With
\(P_{B,n}^S=\Phi _3^n(P_B^S)\), it gives

\[
 \boxed{
 T_{B,n}^{S}
 =V_{B,n}\cap R_S(E_{B,n+1})
 =\frac{K_{B,n}\cap P_{B,n+1}^{S}}{K_{B,n+1}}.}
\tag{2.12}
\]

If, separately for this block, \(R_S(E_{B,0})\) is authenticated as
superperfect, v151 also gives at the first edge

\[
 \boxed{T_{B,0}^{S}=[R_S(E_{B,0}),V_{B,0}].}
\tag{2.13}
\]

Superperfectness of a joint context group is not silently substituted for
this blockwise hypothesis.

For the pentagon, retain the literal intersection

\[
 T_{P,n}^{\mathrm{loc}}
 =T_{P,n}^{S}\cap B_{P,n+1};
\tag{2.14}
\]

no image--intersection interchange is asserted.  Put

\[
 Z_n^{\mathrm{loc}}
 =T_{H1,n}^{S}\oplus T_{H2,n}^{S}
  \oplus T_{P,n}^{\mathrm{loc}}.
\tag{2.15}
\]

The localization statement below always includes the full v252 typing:

\[
 F=F_{\mathrm{arith}}u,\qquad u\in\Pi_S,\qquad
 F\in[\widehat F_2,\widehat F_2],
\tag{2.16}
\]

and the correction is in
\(\Pi_S\cap\ker q_0\cap[\widehat F_2,\widehat F_2]\).
Under (2.16), v252 and Proposition 2.2 put every residual already killed
through rung \(n\) into (2.15) at the next rung.

The coarse v372 module

\[
 \overline D_{1,B,n}^{-1}(I(R_S(E_{B,n})))
\tag{2.17}
\]

contains the whole loop fibre because every loop has coarse endpoint one.
The fine intersection (2.12), not (2.17) alone, distinguishes the supported
next endpoints.

## 3. The task395 closure has a canonical actual projection

At the first edge, retain the task395 raw separately tagged chain space
\(V_{\mathrm{raw}}\), the eleven v370 signed-prefix columns, and their
four-generator closure \(W_C\).  Let

\[
 \operatorname {Agg}:V_{\mathrm{raw}}\longrightarrow
 \mathcal R_{H1,0}\oplus\mathcal R_{H2,0}
 \oplus\mathcal R_{P,0}
\tag{3.1}
\]

sum occurrences in printed block order and quotient by the complete
PB3/PB4 boundary modules.

Let \(c_1,\ldots,c_r\) be the future authenticated task382 basis of
\(C_{\mathrm{rel}}\).  Every occurrence value \(\rho_o(c_i)\) is one in
the coarse endpoint group.  For its v370 column one has

\[
 D_{1,B(o),0}
 \bigl(\sigma_oP_o\,\delta(\rho_o(c_i))\bigr)
 =\sigma_oP_o(\rho_o(c_i)-1)=0.
\tag{3.2}
\]

The simultaneous actor in v370 is a left group action on the chain complex.
It commutes with \(D_1\).  Equation (3.2) therefore remains zero after every
simultaneous translate and every linear combination.  Hence

\[
 \boxed{
 \operatorname {Agg}(W_C)\subseteq
 \ker\overline D_{1,H1,0}\oplus
 \ker\overline D_{1,H2,0}\oplus
 \ker\overline D_{1,P,0}.}
\tag{3.3}
\]

The following map is consequently defined on all of \(W_C\), not merely on
its seed columns:

\[
 \lambda _0
 =(\theta _{H1,0}^{-1}\oplus\theta _{H2,0}^{-1}
       \oplus\theta _{P,0}^{-1})\operatorname {Agg}.
\tag{3.4}
\]

We now type its source comparison without identifying a group-algebra ideal
with the actual common-word layer.  Let \(\Delta_{\mathrm{act}}\) be the
finite simultaneous action group authenticated by task198/task382 and set

\[
 P_{\mathrm{reg}}
 =\bigoplus_{\substack{g\in\Delta_{\mathrm{act}}\\1\leq i\leq r}}
   \mathbf F _3 e_{g,i}.
\tag{3.5}
\]

Define two linear maps on its displayed basis:

\[
 \begin{aligned}
 m(e_{g,i})&={}^{g}c_i\in C_{\mathrm{rel}},\\
 \widehat b(e_{g,i})
   &=g\cdot\widehat B(c_i-1)\in W_C.
 \end{aligned}
\tag{3.6}
\]

The first map uses the actual conjugation action on the elementary-abelian
transition kernel.  The second uses the eleven occurrence actors of v370.
Task382 basis completeness gives

\[
 m(P_{\mathrm{reg}})=C_{\mathrm{rel}},
\tag{3.7}
\]

already from the terms with \(g=1\).  V370 generator closure gives

\[
 \widehat b(P_{\mathrm{reg}})=W_C.
\tag{3.8}
\]

Let

\[
 D_0^{\mathrm{act}}:C_{\mathrm{rel}}\longrightarrow
 V_{H1,0}\oplus V_{H2,0}\oplus V_{P,0}
\tag{3.9}
\]

be the exact first-successor affine change map of v99 for the same base,
multiplication convention and block order.

### Theorem 3.1 (FORMAL-ACTION COMMUTING SQUARE)

After authenticating the task198/task382 owner, complete boundaries,
prefixes, signs and simultaneous action, one has

\[
 \boxed{\lambda _0\widehat b=D_0^{\mathrm{act}}m
 \quad\text{on }P_{\mathrm{reg}}.}
\tag{3.10}
\]

Consequently

\[
 \boxed{\lambda _0(W_C)=\operatorname {im}D_0^{\mathrm{act}}.}
\tag{3.11}
\]

#### Proof

It is enough to evaluate \(e_{g,i}\).  V370 Lemma 1.1 identifies
\(\widehat B(c_i-1)\) with the literal first Fox difference of the two
hexagons and printed pentagon.  V370 Lemma 2.1 identifies its simultaneous
translate by \(g\) with the first difference produced by the actual
conjugate correction \({}^{g}c_i\), including the occurrence prefixes.
Aggregation and complete boundary quotient give the three coarse Fox-loop
classes.  Theorem 1.1 sends those classes to their three successor endpoint
changes.  By v99 exact affine linearization, that tuple is
\(D_0^{\mathrm{act}}({}^{g}c_i)\).  This proves (3.10) on every displayed
generator and hence everywhere.  Equations (3.7)--(3.8) then give both
inclusions in (3.11).  \(\square\)

### Proposition 3.2 (LEGAL IMAGE IS SUPPORTED)

Assume the base \(F_0\) and every registered correction
\({}^{g}c_i\) satisfy the full typing (2.16).  Then

\[
 \boxed{\operatorname {im}D_0^{\mathrm{act}}
 \subseteq Z_0^{\mathrm{loc}}.}
\tag{3.12}
\]

#### Proof

Fix a generator \({}^{g}c_i\).  In a block \(B\), form the literal
residual-change word

\[
 R_B(F_0\,{}^{g}c_i)\,R_B(F_0)^{-1}.
\tag{3.13}
\]

Both residuals have the same coarse endpoint, so (3.13) is coarse-trivial
and defines a class in \(V_{B,0}\).  Modulo the formation residual the
relative factors in \(F_0\) and in the correction disappear, while the
arithmetic word satisfies the relation.  Hence both residual endpoints,
and therefore their difference (3.13), lie in the fine formation residual.
For the pentagon, both source words are exact commutators, so BRUN-DEF puts
both pentagon residuals in the registered Brunnian image; their difference
also lies there.  Proposition 2.2 puts the three successor classes in
(2.15).  Taking spans proves (3.12).  \(\square\)

Equations (3.11)--(3.12) do not assert \(W_C=L/JL\).  They give the exact
smaller statement needed at the first successor: after aggregation,
complete-boundary quotient and \(\theta^{-1}\), task395 computes the image
of the actual affine correction map in the finite supported target.

## 4. Exact successor criterion and the all-rung boundary

Let \(F_n\) satisfy the two hexagons and pentagon through rung \(n\), with
the full typing (2.16), and let

\[
 \beta _n\in Z_n^{\mathrm{loc}}
\tag{4.1}
\]

be the three next endpoints.  Let \(C_n^{\mathrm{rel}}\) be the actual
one-common-word relative correction layer.  Every occurrence value of an
element of \(C_n^{\mathrm{rel}}\) lies in the corresponding \(K_{B,n}\).
Let

\[
 D_n:C_n^{\mathrm{rel}}\longrightarrow Z_n^{\mathrm{loc}}
\tag{4.2}
\]

be the exact affine map.

### Theorem 4.1 (ONE-SUCCESSOR NECESSARY AND SUFFICIENT TEST)

A legal correction \(c_n\) invisible through rung \(n\) extends \(F_n\)
through rung \(n+1\) if and only if

\[
 \boxed{D_n[c_n]=-\beta _n.}
\tag{4.3}
\]

If \(m>n\) and every occurrence value of a later correction lies in
\(K_{B,m}\), that later correction leaves (4.3) and all earlier equations
unchanged.

#### Proof

At the elementary-abelian transition, v99 gives the exact identity

\[
 \beta _n(F_nc_n)=\beta _n(F_n)+D_n[c_n].
\tag{4.4}
\]

Theorem 1.1 says that vanishing of this vector is equivalent to the three
literal relation words being trivial in the fine quotient.  This proves
(4.3).  For \(m>n\),

\[
 K_{B,m}\leq K_{B,n+1},
\tag{4.5}
\]

so the later correction has zero image in \(V_{B,n}\).  \(\square\)

This direct finite test needs no ordinary strict-\(L/JL\) theorem.  It does
not remove the quantifier over all successors.

For the compactness alternative, let \(X_n\) be the finite set of
equivalence classes of source words in the registered finite joint state at
level \(n\), retaining the roof, commutator, formation, Brunnian and literal
relation gates.  Reduction maps \(X_{n+1}\) into \(X_n\).  If
\(X_n\neq\varnothing\) for every \(n\), these finite levels form a finitely
branching tree with vertices at arbitrary depth.  Koenig's lemma gives one
compatible pro-\(3\) branch.  It removes the compatibility-choice problem;
it does not prove nonemptiness.

There remain two honest ways to close the pro-\(3\) tail:

1. prove (4.3) soluble at every rung, by a structural theorem or complete
   finite accepted sets, and apply compactness; or
2. prove one natural completed identity, such as the v191 universal
   word-pair boundary identity or the v369 completed based right inverse,
   which solves all rungs simultaneously.

## 5. Exact advance and remaining gates

The canonical statement joining v372 to the Frattini tower is

\[
 \boxed{
 [\partial _{B,n}W]
 =\theta _{B,n}(\beta _{B,n}),
 \qquad
 \theta _{B,n}^{-1}[\partial _{B,n}W]
 =\beta _{B,n}\in T_{B,n}.}
\tag{5.1}
\]

Thus task395 has a precise positive consumer: aggregate its eleven
occurrences, quotient by the complete PB boundaries, apply the loop-endpoint
identification, and compare the actual \(-\beta _0\) with the resulting
image.  Ordinary localized saturation is not part of that one-successor
decision.

One first-edge MEMBER still does not imply all-rung membership.  The
completed Newton route still needs its strict or weighted target and leading
onto certificate, or the pointed/universal identity route must succeed.
Physical task198/task382 ownership, actual numerical membership, every
non-\(3\) edge, settlement and the perfect-core gates remain mandatory.

~~~text
FOX LOOP / NEXT FRATTINI ENDPOINT SQUARE:            PAPER PROOF
BLOCKWISE ALIGNED FORMATION FORMULA:                 PAPER PROOF
PENTAGON BRUNNIAN INTERSECTION:                      EXACT DEFINITION
ALL OF W_C LIES IN THE THREE LOOP KERNELS:           PAPER PROOF
FORMAL ACTION SQUARE lambda_0 b = D_0^act m:          PAPER PROOF / ABI-CONDITIONAL
TASK395 PROJECTION = ACTUAL FIRST-SUCCESSOR IMAGE:   PAPER PROOF / ABI-CONDITIONAL
DIRECT ONE-SUCCESSOR TEST WITHOUT L/JL STRICTNESS:   PAPER PROOF
ACTUAL TASK395 CLOSURE AND FIRST MEMBERSHIP:         NOT COMPUTED
ALL-RUNG MEMBERSHIP OR NATURAL COMPLETED IDENTITY:   OPEN
COMPATIBLE RELATIVE PRO-3 LIFT:                      NOT CONSTRUCTED
MIXED-PRIME / PERFECT-CORE / SETTLEMENT:             OPEN
FAKE / IHARA WITNESS:                               NOT DECLARED
~~~

R07_FRATTINI_LOOP_TARGET_AND_OCCURRENCE_PROJECTION_V374_PAPER_GRADE
