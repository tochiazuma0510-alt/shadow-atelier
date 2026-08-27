# R07 universal-boundary endpoint reduction v193

Author: Sol / 2026-08-28

Status: paper theorem and a strict reduction of the post-v191 promotion
gate.  In the occurrence-resolved seven-block Fox complex, the universal
boundary equation is equivalent to one finite endpoint identity.  Thus a
separate blind search for a boundary chain is not a mathematical gate: once
the endpoint is zero, a finite boundary chain exists and can be extracted
from relator decompositions.  The actual task192 word, pointed multiplier,
and endpoint have not yet been computed.  No compatible R07 lift, fake
certificate, or Ihara witness is declared.

## 1. The occurrence-resolved presentation complex

Put \(k=\mathbf F_3\).  For each of the seven typed occurrence blocks

\[
 b\in\{H1,H2,P1,P2,P3,P5,P4\},
\tag{1.1}
\]

let

\[
 G_b=\langle X_b\mid R_b\rangle
\tag{1.2}
\]

be the fixed presented PB3 or PB4 context group used by v175.  Repeated
occurrences use separate tagged copies of the same presentation module.
In particular, the H1/1 and H2/2 copies of the same E3 map remain separate
occurrences here, while v189 supplies their common acting value.  The E3
and E4 occurrences both labelled `C21` remain different typed copies.

Use the left Fox convention

\[
 C_{2,b}=k[G_b]^{R_b},\qquad
 C_{1,b}=k[G_b]^{X_b},\qquad
 C_{0,b}=k[G_b],
\tag{1.3}
\]

\[
 D_{2,b}[r]=\delta_b(r),\qquad
 D_{1,b}(g[x])=g(x-1).
\tag{1.4}
\]

Thus

\[
 D_{1,b}\delta_b(w)=\bar w-1.
\tag{1.5}
\]

Put

\[
 \widetilde C_i=\bigoplus_b C_{i,b},\qquad
 \widetilde D_i=\bigoplus_b D_{i,b}.
\tag{1.6}
\]

All printed hexagon signs, the pentagon order
\((b_1,b_2,b_3,b_5^{-1},b_4^{-1})\), and all prefix transports are absorbed
in the literal tagged rows \(\widetilde d,\widetilde e\in\widetilde C_1\).
No occurrence is summed away before (1.6).

This occurrence-resolved qualification is load-bearing.  The theorem below
must not be applied after collapsing the five pentagon occurrences or the
two hexagons to an untagged total, because such a collapse can create cycles
which do not lift componentwise.

## 2. Exactness at Fox degree one

### Lemma 2.1 (COMPLETE PRESENTATION BOUNDARIES ARE ALL ONE-CYCLES)

For every block \(b\),

\[
 \boxed{\ker D_{1,b}=\operatorname{im}D_{2,b}.}
\tag{2.1}
\]

Consequently

\[
 \boxed{\ker\widetilde D_1=\operatorname{im}\widetilde D_2.}
\tag{2.2}
\]

Every finite-support element of the kernel has a finite-support preimage.

#### Proof

The cellular chain complex (1.3)--(1.4) is the degree-two part of the
cellular complex of the universal cover of the presentation two-complex of
\(G_b\).  The universal cover is simply connected, so its first homology is
zero.  Therefore

\[
 H_1=\ker D_{1,b}/\operatorname{im}D_{2,b}=0,
\]

which is (2.1).  This uses neither asphericity nor exactness at \(C_{2,b}\).
Taking the finite direct sum gives (2.2).  Cellular chain groups use direct
sums, so every chain, including a preimage, has finite support. \(\square\)

Completeness of the two PB3 and eleven PB4 presentation-relator rosters is
essential.  A sampled boundary orbit does not satisfy Lemma 2.1.

## 3. The universal boundary equation is an endpoint equation

Let \(\mathcal G\) be the common source group of v191 and let

\[
 M=\sum_{i=1}^t a_i(U_i-V_i),\qquad
 a_i\in k,\qquad \pi(U_i)=\pi(V_i),
\tag{3.1}
\]

be any finite roof-fibre word-pair polynomial.  Its action on block \(b\)
is through the fixed context homomorphism
\(\rho_b:\mathcal G\to G_b\).  Define

\[
 z(M)=\widetilde e-M\widetilde d\in\widetilde C_1
\tag{3.2}
\]

and its endpoint

\[
 \eta(M)=\widetilde D_1z(M)\in\widetilde C_0.
\tag{3.3}
\]

### Theorem 3.1 (UNIVERSAL BOUNDARY--ENDPOINT EQUIVALENCE)

For the literal occurrence-resolved v191 rows,

\[
 \boxed{
 \exists q\in\widetilde C_2:\
 \widetilde e-M\widetilde d=\widetilde D_2q
 \quad\Longleftrightarrow\quad
 \eta(M)=0.}
\tag{3.4}
\]

When these conditions hold, \(q\) can be chosen with finite support.

#### Proof

The forward implication follows from
\(\widetilde D_1\widetilde D_2=0\).  Conversely, \(\eta(M)=0\) says that
\(z(M)\in\ker\widetilde D_1\).  Lemma 2.1 gives
\(z(M)\in\operatorname{im}\widetilde D_2\), including the finite-support
assertion. \(\square\)

Thus the `universal boundary chain q` in v191 is not a second independent
existence problem.  The only existence gate is the endpoint identity
\(\eta(M)=0\); after it passes, extraction of \(q\) is certificate
production.

### Corollary 3.2 (FINITE ENDPOINT FORMULA)

The block-\(b\) component is

\[
 \boxed{
 \eta_b(M)=D_{1,b}\widetilde e_b-
 \sum_i a_i\bigl(\rho_b(U_i)-\rho_b(V_i)\bigr)
 D_{1,b}\widetilde d_b.}
\tag{3.5}
\]

In particular, it is a finite-support element of \(k[G_b]\).  If a tagged
row is a single Fox path,

\[
 \widetilde d_b=\delta_b(W_{d,b}),\qquad
 \widetilde e_b=\delta_b(W_{e,b}),
\tag{3.6}
\]

then

\[
 \eta_b(M)=
 (\overline W_{e,b}-1)-
 \sum_i a_i\bigl(\rho_b(U_i)-\rho_b(V_i)\bigr)
 (\overline W_{d,b}-1).
\tag{3.7}
\]

For a signed or prefix-transported row, (3.5), rather than an informal
simplification of (3.7), is authoritative.

#### Proof

The Fox endpoint map is equivariant for left translation:
\(D_{1,b}(gc)=gD_{1,b}(c)\).  Expand (3.1)--(3.3) without commuting any
factor.  Equation (1.5) gives the last assertion. \(\square\)

## 4. Exact decision and constructive extraction

Equation (3.5) can be decided without constructing a translated boundary
span.  Normalize every group word in its fixed PB3/PB4 presentation, collect
equal normal forms, and reduce coefficients modulo three.  Then:

1. if one collected coefficient is nonzero, it is a complete obstruction
   to the exact candidate \(M\); no boundary chain for that candidate can
   exist;
2. if all seven tagged endpoint components vanish, Theorem 3.1 proves that
   a finite \(q\) exists; and
3. the result is about the exact retained source representatives.  Replacing
   one \(U_i\) or \(V_i\) by a word with the same first-successor value can
   change (3.5).

The zero case can be made fully constructive.  View a finite one-cycle in
the Cayley graph of \(G_b\) and split it, over \(k\), into finitely many
based loops.  For each loop word \(w\), retain a relator decomposition in
the free group,

\[
 w=\prod_j s_jr_{i_j}^{\epsilon_j}s_j^{-1},
 \qquad \epsilon_j\in\{1,-1\}.
\tag{4.1}
\]

Fox differentiation in \(G_b\) gives

\[
 \delta_b(w)=
 \sum_j\epsilon_j\,\overline{s_j}\,\delta_b(r_{i_j}),
\tag{4.2}
\]

where a negative exponent is read modulo three.  The coefficients on the
right are the desired entries of \(q_b\).  Summing the seven tagged
components produces \(q\).

An authenticated proof-producing normal-form routine may output (4.1)
directly.  Even without one, enumeration of products of conjugates of the
finite relator roster terminates after endpoint equality has established
that each loop lies in the normal closure.  This is a termination statement,
not a practical wall-time bound; production must remain fail-closed on a
resource stop.

### Corollary 4.1 (NO UNIVERSAL COLUMN GENERATION AFTER A POINTED PASS)

After v188/v191 compile the actual \(M_1\), the promotion procedure is:

1. evaluate the seven finite endpoint expressions (3.5);
2. reject the exact representative choice if any endpoint is nonzero;
3. on zero, extract relator decompositions and hence \(q\) by (4.1)--(4.2);
4. independently replay the literal chain equality; and
5. apply v191 Theorem 2.1 and v174's ordered Neumann correction.

No full universal boundary-orbit echelon and no blind search radius for
\(q\) belongs between Steps 1 and 3.

## 5. Consequence for the current R07 chain

Let task192/task193/v188 return a pointed ancestry and let v191 compile

\[
 M_1=\sum_i a_i(U_i-V_i).
\tag{5.1}
\]

The relative pro-3 promotion gate is now precisely

\[
 \boxed{\eta(M_1)=0\text{ in the seven tagged PB group algebras}.}
\tag{5.2}
\]

If (5.2) holds, Theorem 3.1 supplies the hypothesis previously called the
universal boundary gate, and the same finite word-pair polynomial has the
required image at every matched relative pro-3 rung.  If (5.2) fails, the
nonzero normalized endpoint identifies the exact block, group element, and
coefficient which a same-first-shadow representative variation must repair.
It does not negate the finite pointed solution itself.

The proof removes one large linear search but does not make the actual
endpoint automatically zero.  It also does not discharge formation,
prime-to-three, nonlinear word, onto, settlement, or perfect-core gates.

## 6. Certificate contract

A positive endpoint certificate must retain:

1. the exact \(M_1\), all source words, coefficients, and roof/successor
   values from v191;
2. the v189 seven-block/ten-coordinate occurrence ledger;
3. the complete fixed PB3/PB4 presentations and all two/eleven relators;
4. every unreduced term of (3.5), canonical word normal forms, collection
   buckets, and zero coefficients after collection;
5. the loop decomposition and every conjugate-relator factor in (4.1);
6. the derived boundary chain \(q\) and a direct replay of
   \(z(M_1)=\widetilde D_2q\); and
7. destructive rejection after changing one context tag, source word,
   left factor order, endpoint coefficient, relator sign, or boundary
   coefficient.

The independent checker must reconstruct endpoints and relator
decompositions without importing the producer's normal-form or collection
helpers.  A hash is an identity pin, not an equality oracle.

```text
COMPLETE PRESENTATION FOX EXACTNESS AT C1:          PAPER_PROOF
UNIVERSAL BOUNDARY IFF SEVEN ENDPOINTS VANISH:      PAPER_PROOF
FINITE-SUPPORT q AFTER ENDPOINT ZERO:               PAPER_PROOF
BLIND UNIVERSAL BOUNDARY COLUMN GENERATION:         REMOVED
ACTUAL FIRST-SHADOW MULTIPLIER mu1:                 NOT COMPUTED
ACTUAL WORD-PAIR POLYNOMIAL M1:                     NOT COMPILED
ACTUAL SEVEN-BLOCK ENDPOINT eta(M1):                NOT COMPUTED
EXPLICIT RELATOR-DECOMPOSITION CHAIN q:              NOT COMPILED
RELATIVE PRO-3 COMPATIBLE R07 LIFT:                 NOT CONSTRUCTED
PRIME-TO-3 / PERFECT-CORE GATES:                    OPEN
FAKE / IHARA WITNESS:                               NOT DECLARED
```

`R07_UNIVERSAL_BOUNDARY_ENDPOINT_REDUCTION_V193_PAPER_GRADE`
