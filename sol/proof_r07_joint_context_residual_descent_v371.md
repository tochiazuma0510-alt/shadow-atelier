# R07 joint-context residual descent v371

Author: Sol / 2026-08-30

Status: **REJECTED** by independent audit on 2026-08-30 and superseded by
v372.  Its endpoint-only \(\kappa\) is not well-defined because two retained
paths with one finite quotient endpoint can differ by the nonzero active
class \(H_1(K_n;\mathbf F_3)\).  The text below is retained as a failed
candidate and makes no theorem claim.

The attempted factorization after v173, v357, v369 and the frozen
task198 ten-to-eleven ledger claimed that continuous descent of the exact
H1/H2/printed-pentagon residual is automatic once the registered joint image
is physically identified with those same context substitutions.  Combining
that factorization with v33/v37 and
\(\mathscr Q_C\subseteq\vartheta(K_0)\) also proves that every reachable lane
residual stays in the formation/Brunnian localized target.  The physical ABI
identification, strictness, leading onto and the intrinsic nonlinear depth
estimate are not proved here.  No compatible lift, fake certificate or Ihara
witness is declared.  `verified=false`.

## 1. The absolute finite residual is a word map on the joint tuple

Work on the registered exponent-zero (\(m=0\)) R07 lane.  At retained level
\(n\), let

\[
 \rho_{j,n}:F_2\longrightarrow Q_{j,n},
 \qquad 0\leq j<10,
\tag{1.1}
\]

be the ten physical task198 substitutions, with each value retained in its
registered PB3 or PB4 type.  The eleven literal factors use the frozen map

\[
 t=(0,1,2,3,0,4,5,6,7,8,9)
\tag{1.2}
\]

and the signs

\[
 \sigma=(+,-,+,-,-,+,+,+,+,-,-).
\tag{1.3}
\]

Thus the repeated `fxy` context is one joint coordinate used in two
different printed factors; it is not an eleventh independently selectable
context.  Assume the physical joint image is

\[
 \Delta_n=\operatorname{im}\left(
 F_2\xrightarrow{(\rho_{0,n},\ldots,\rho_{9,n})}
 \prod_{j=0}^9Q_{j,n}\right),
\tag{1.4}
\]

including the registered occurrence-to-block embeddings.  For
\(d=(d_0,\ldots,d_9)\in\Delta_n\), take the signed values

\[
 f_{o,n}(d)=d_{t(o)}^{\sigma_o}.
\tag{1.5}
\]

For each occurrence let

\[
 \jmath_{o,n}:Q_{t(o),n}\longrightarrow G_{B(o),n},
 \qquad B(o)\in\{H1,H2,P\},
\tag{1.6}
\]

be its registered PB3/PB4 embedding.  Multiplication in the frozen printed
order, separately over occurrences 1--3, 4--6 and 7--11, first defines the
group-valued word map

\[
 \widetilde\psi^{\rm grp}_n(d)=
 \left(
  \prod_{o=1}^{3}\jmath_{o,n}(d_{t(o)})^{\sigma_o},
  \prod_{o=4}^{6}\jmath_{o,n}(d_{t(o)})^{\sigma_o},
  \prod_{o=7}^{11}\jmath_{o,n}(d_{t(o)})^{\sigma_o}
 \right).
\tag{1.7}
\]

The residual targets used by v169/v252 are additive Fox-path quotients.  For
each block \(B\), fix the canonical map

\[
 \kappa_{B,n}:G_{B,n}\longrightarrow R_{B,n}:=
 C_{1,B,n}/\operatorname{im}D_{2,B,n}.
\tag{1.8}
\]

Here \(\kappa_{B,n}(g)\) is the class of any retained Cayley path from the
identity vertex to \(g\).  Two choices differ by a one-cycle and hence by a
complete PB boundary, so the class is well-defined.  Moreover
\(\kappa_{B,n}(1)=0\), and exactness of the Cayley presentation complex gives
\(\kappa_{B,n}(g)=0\) only when \(g=1\).  The fixed marked presentation maps
make the \(\kappa_{B,n}\) commute with matched reduction.  Now put

\[
 \psi_n=(\kappa_{H1,n},\kappa_{H2,n},\kappa_{P,n})
          \circ\widetilde\psi^{\rm grp}_n:
 \Delta_n\longrightarrow
 R_{H1,n}\times R_{H2,n}\times R_{P,n}=:R_n.
\tag{1.9}
\]

Thus (1.5)--(1.9) retain all task198 occurrence data: the two uses of
coordinate zero, the two inverse hexagon slots, the two inverse pentagon
slots, and the H1/H2/P block tags.  Neither map need be a homomorphism;
\(\widetilde\psi^{\rm grp}_n\) is a finite noncommutative word map and
\(\psi_n\) is that exact word map followed by the physical residual encoder.

### Lemma 1.1 (FINITE JOINT-IMAGE FACTORIZATION)

For every source word \(F\in F_2\),

\[
 \psi_n\bigl((\rho_{j,n}(F))_{j=0}^9\bigr)=\Phi_n(F),
\tag{1.10}
\]

where the right side is the exact two-hexagon/printed-pentagon residual at
level \(n\), encoded in the lossless path quotients (1.8).  Thus
\(\Phi_n(F)=0\) if and only if all three literal group residuals are the
identity.  Hence two source words with the same joint tuple have the same
exact residual at that level.

#### Proof

Before applying \(\kappa\), the three frozen products are, literally,

\[
 \begin{aligned}
 H1(F)&=F(x,y)F(x,z)^{-1}F(y,z),\\
 H2(F)&=F(u,x)^{-1}F(x,y)^{-1}F(u,y),
 \end{aligned}
\tag{1.11}
\]

and the printed pentagon is the frozen five-factor product with factor order
and signs \((+,+,+,-,-)\).  Substituting the ten coordinates of \(F\) into
(1.7) therefore reproduces all eleven factors in their three blocks.  Applying
the three canonical path classes is exactly the v169/v252 residual
\(\Phi_n(F)\), which proves (1.10).  No linear approximation, source lift, or
representative of a joint tuple occurs in the calculation. \(\square\)

Fix now one reachable base word \(F_*\), and put

\[
 w_{0,n}=(\rho_{j,n}(F_*))_{j=0}^9\in\Delta_n.
\tag{1.12}
\]

For a correction tuple \(c\in\Delta_n\), the based residual map is

\[
 \phi_{F_*,n}(c):=\psi_n(w_{0,n}c).
\tag{1.13}
\]

If \(c=(\rho_{j,n}(u))_j\) for a source correction \(u\), then

\[
 \phi_{F_*,n}(c)=\Phi_n(F_*u),
\tag{1.14}
\]

because every substitution is a homomorphism.  This based formula is the
nonlinear counterpart of v370's chain formula: v370 differentiates the
group-word part of (1.13) at the identity correction, while (1.13) retains
the complete finite word products and then records their exact path classes.

## 2. Matched refinement gives a continuous inverse-limit map

Assume the context maps, their PB3/PB4 target embeddings, and the three
printed products commute with every matched refinement.  Then (1.4) gives
the registered surjections

\[
 \Delta_{n+1}\twoheadrightarrow\Delta_n,
 \qquad
 \Delta_\infty=\varprojlim_n\Delta_n.
\tag{2.1}
\]

Give \(R_n\) the matched three-block reduction maps and put
\(R_\infty=\varprojlim_nR_n\).

### Theorem 2.1 (CONTINUOUS RESIDUAL DESCENT)

The finite maps \(\psi_n\) commute with reduction and induce one continuous
map

\[
 \psi_\infty:\Delta_\infty\longrightarrow R_\infty.
\tag{2.2}
\]

Its pullback along the simultaneous source map
\(\vartheta:\widehat F_2\to\Delta_\infty\) is the exact completed R07
residual.

#### Proof

Every entry of (1.7) is obtained by projection to a fixed coordinate,
followed by the registered occurrence embedding, multiplication, and
inversion.  Quotient homomorphisms commute with all these operations.  The
marked presentation maps also carry a retained path to its reduced path and
complete boundaries to complete boundaries, so the canonical encoders
\(\kappa_{B,n}\) commute with reduction.  Thus (1.9) commutes with matched
reduction, and the compatible family defines (2.2).
Each finite target is discrete and every finite projection of
\(\psi_\infty\) factors through one finite coordinate, so the inverse-limit
map is continuous.  Equation (1.10) at every level proves the absolute
pullback assertion.  Restricting it to
\(\vartheta^{-1}(w_0\mathscr Q_C)\) gives the exact based-lane pullback used
below. \(\square\)

Let \(\mathscr Q_C\leq\Delta_\infty\) be v369's closed relative seed group,
let \(w_0=\vartheta(F_*)\), and let \(w_0\mathscr Q_C\) be the reachable lane
torsor.  Right translation identifies \(\mathscr Q_C\) homeomorphically with
this torsor, but no section back to \(\widehat F_2\) is asserted.

### Corollary 2.2 (LOCALIZED LANE DESCENT)

Suppose the physical localized target is a closed inverse-limit subspace
\(L\leq R_\infty\), and every reachable exact residual on
\(w_0\mathscr Q_C\) belongs to \(L\).  Then the corestriction

\[
 \Phi_{\rm lane}:=
 \left.\psi_\infty\right|_{w_0\mathscr Q_C}:
 w_0\mathscr Q_C\longrightarrow L
\tag{2.3}
\]

is continuous, and its source pullback is the actual localized residual.
Thus the residual-descent hypothesis in v369 Theorem 4.1 follows from the
finite physical context identification (1.4), matched refinement, and
localized stability; it is not an additional all-depth selector.

#### Proof

Restrict (2.2) to the closed torsor and corestrict it to \(L\).  The stated
membership makes the corestriction well-defined.  Continuity and the
pullback identity follow from Theorem 2.1. \(\square\)

### Proposition 2.3 (ACTUAL R07 LANE IS DOUBLY LOCALIZED)

Put

\[
 K_0=\Pi_S\cap\ker q_0
\tag{2.4}
\]

and assume the authenticated base typing

\[
 F_*=F_{\rm arith}u_*,
 \qquad u_*\in\Pi_S,
 \qquad F_*\in[\widehat F_2,\widehat F_2].
\tag{2.5}
\]

Let \(\mathscr Q_C\) be v369's group, so
\(\mathscr Q_C\subseteq\vartheta(K_0)\).  For \(B=H1,H2\), let

\[
 \mathcal L_{B,n}:=
 \left\langle
  \kappa_{B,n}\bigl(R_S(G_{B,n})\bigr)
 \right\rangle_{\Lambda_{B,n}}
 \subseteq R_{B,n},
\tag{2.6}
\]

where \(\Lambda_{B,n}\) is the registered block deck algebra.  In the
pentagon block put

\[
 \mathcal L_{P,n}:=
 \left\langle
  \kappa_{P,n}\bigl(B_{P,n}\cap R_S(G_{P,n})\bigr)
 \right\rangle_{\Lambda_{P,n}}
 \subseteq R_{P,n}.
\tag{2.7}
\]

At every finite level define

\[
 L_n=
 \mathcal L_{H1,n}\times\mathcal L_{H2,n}\times\mathcal L_{P,n},
\tag{2.8}
\]

and let \(L_{\rm loc}\) be the closed subspace of \(R_\infty\) whose finite
coordinates belong to the corresponding \(L_n\).  Formation residuals are
characteristic, Brunnian deletion kernels and the block deck actions commute
with matched quotient maps, and hence the \(L_n\) form a compatible system
of localized submodules.  Then

\[
 \boxed{\psi_\infty(w_0\mathscr Q_C)\subseteq L_{\rm loc}.}
\tag{2.9}
\]

Consequently (2.3), with \(L=L_{\rm loc}\), is an actual continuous
localized lane residual.  No continuous section
\(\mathscr Q_C\to K_0\) is needed.

#### Proof

Take \(q\in\mathscr Q_C\).  Since
\(\mathscr Q_C\subseteq\vartheta(K_0)\), choose \(k\in K_0\) with
\(\vartheta(k)=q\).  Since
\(K_0\leq\Pi_S\leq[\widehat F_2,\widehat F_2]\), we have

\[
 F_*k=F_{\rm arith}(u_*k),
 \qquad u_*k\in\Pi_S,
 \qquad F_*k\in[\widehat F_2,\widehat F_2].
\tag{2.10}
\]

V33 Lemma 1.1, equivalently v37's exact formation-domain theorem, puts the
two hexagon residuals and the pentagon residual of \(F_*k\) in their
respective \(S\)-formation residuals.  BRUN-DEF puts the pentagon residual
in \(B_{P,n}\), because (2.10) is a commutator word.  Thus its group-valued
finite residual has its two hexagon coordinates in the formation residuals
and its pentagon coordinate in their Brunnian/formation intersection.
Applying the three \(\kappa_{B,n}\) places its additive residual class in
(2.8) for every \(n\).  Theorem 2.1 identifies these classes with the
coordinates of \(\psi_\infty(w_0q)\), proving (2.9).

The argument depends only on \(q\), not on the chosen preimage \(k\):
different preimages have the same joint tuple and Lemma 1.1 gives the same
residual.  Corollary 2.2 now supplies the continuous corestriction.
\(\square\)

Proposition 2.3 proves localization as a closed codomain statement.  It does
not identify the ambient filtration
\(L_{\rm loc}\cap J^dR_\infty\) with the intrinsic filtration
\(J^dL_{\rm loc}\).  That distinct saturation issue is exactly v321's
remaining gate.

## 3. Exact physical authentication gate

The theorem turns residual descent into the following finite ABI checks:

1. the registered \(\Delta_n\) uses the exact ten substitutions, types, and
   ten-to-eleven repetition (1.1)--(1.4);
2. H1, H2 and printed P use the same eleven signs, occurrence-to-block
   embeddings, and printed factor order;
3. matched transition maps commute with those substitutions and embeddings;
4. the exact residual package and localized module \(L\) use the same finite
   target coordinates; and
5. the authenticated base and correction typing matches (2.4)--(2.8), so
   Proposition 2.3 applies.

Items 1--4 are equality/replay checks against the frozen task198/v169
owners.  Item 5 is a typing replay against v33/v37 and v369, not a new
all-depth membership computation.  This paper does not prove intrinsic
strictness of \(L_{\rm loc}\), leading surjectivity of the seed Jacobian, or
the one-depth affine/nonlinear law.

```text
FINITE EXACT RESIDUAL FACTORS THROUGH JOINT TUPLE: PAPER PROOF
MATCHED INVERSE-LIMIT CONTINUITY:                  PAPER PROOF
TASK198/v169 JOINT-TUPLE ABI EQUALITY:             OPEN AUTHENTICATION
REACHABLE RESIDUALS STAY IN LOCALIZED L:           PAPER PROOF / ABI TYPING
STRICT L/JL / LEADING ONTO:                        OPEN
ONE-DEPTH AFFINE / NONLINEAR GAIN:                 OPEN
COMPATIBLE LIFT / FAKE / IHARA WITNESS:            NOT CONSTRUCTED
```

`R07_JOINT_CONTEXT_RESIDUAL_DESCENT_V371_PAPER_GRADE`
