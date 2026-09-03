# R07: typed physical replay of the canonical selected SLP (v469)

Author: Sol / 2026-09-03

Status: candidate paper repair of v468 after independent Task607
`PASS_AFTER_REPAIR`. This note replaces only v468 Theorem 4.2 and checker
item 5. It does not change the canonical graph, roots, exact source word,
adjoint evaluation or refinement naturality. No actual selected payload,
grade-two result, A0, COMMON, cofinal lift, fake or Ihara conclusion is
asserted. `verified=false`.

## 1. Source grades and physical grades are different types

Retain all definitions and Theorems 4.1 and 4.3 of v468. For a pure source
node already known to lie in \(F^1\), v465 Theorem 2.1 still gives

\[
 [\mathcal W_j]_1=b_j\quad\text{in }F^1/F^2.        \tag{1.1}
\]

Equation (1.1) is not assigned to an old/lower-derived node merely because
its physical lower image vanishes. In particular, this note makes no
assertion that such a node lies in \(F^1\), in a relative source kernel, or
in any source associated grade.

At the current marked quotient, let

\[
 \mathcal E^{\rm phys}_{<1},\qquad
 \mathcal E^{\rm phys}_{1}                         \tag{1.2}
\]

be the complete registered physical interpreters. The first contains every
normalized-exponent, PB3 augmentation, boundary and auxiliary coordinate;
the second is the coupled grade-one physical row. They are evaluated
occurrence by occurrence with the registered substitutions, prefixes,
inverse conventions and signs.

Their linear use below is conditional on an executable endpoint gate. Every
reached literal seed, actor application and composed SLP node is evaluated in
the current marked quotient, and the required identity endpoints are checked
before Fox additivity is invoked. This is the current-quotient hypothesis of
v467, not a source-filtration conclusion.

## 2. The three physical node identities

The selected graph carries three different kinds of physical identity.

### 2.1 Selected lower pivots

For every reached physical-lower pivot \(k\), let \(\ell_k\) be its
normalized complete lower row and let \(g_k\) be its equally scaled stored
grade companion. Direct replay of its exact SLP \(L_k\) must prove

\[
 \mathcal E^{\rm phys}_{<1}(L_k)=\ell_k,\qquad
 \mathcal E^{\rm phys}_{1}(L_k)=g_k.                \tag{2.1}
\]

Neither side of the first equality is generally zero. Its normalized scale
must be applied to both equalities.

### 2.2 Old-connection grade origins

Suppose an old physical origin \(O_j\) was reduced against lower pivots by
the exact ordered list \(((k,c_k))\). Its canonical origin SLP is

\[
 Z_j=\operatorname{Prod}\left(
       O_j,\bigl(\operatorname{Pow}(L_k,-c_k)\bigr)^{\longrightarrow}
      \right).                                      \tag{2.2}
\]

Direct replay of the old row, (2.1), and the exact lower-reducer order must
prove

\[
 \mathcal E^{\rm phys}_{<1}(Z_j)=0,\qquad
 \mathcal E^{\rm phys}_{1}(Z_j)=z_j.                \tag{2.3}
\]

Here \(z_j\) is the lower-killed, unnormalized grade companion actually
offered to the grade owner. This is the precise mixed lower-first licence.

### 2.3 Physical-grade pivots

For a block origin, direct aggregation supplies a lower-zero origin \(Z_j\)
and its offered grade row \(z_j\). For an old connection use (2.3). If the
accepted grade record is

\[
 b_j=\sigma_j\left(z_j-
       \sum_{(p,q)\in E_j}^{\longrightarrow}q b_p\right),       \tag{2.4}
\]

the canonical word rule of v468 defines

\[
 W_j=\operatorname{Pow}\left(
       \operatorname{Prod}\left(
         Z_j,\bigl(\operatorname{Pow}(W_p,-q)\bigr)^{
           \longrightarrow}_{(p,q)\in E_j}
       \right),\sigma_j\right).                    \tag{2.5}
\]

The required typed conclusion is

\[
 \boxed{
 \mathcal E^{\rm phys}_{<1}(W_j)=0,\qquad
 \mathcal E^{\rm phys}_{1}(W_j)=b_j.}               \tag{2.6}
\]

It is a physical equality, not the source equality (1.1).

## 3. Repaired selected-root theorem

### Theorem 3.1 (current physical correctness)

Assume:

1. the canonical selected graph and roots satisfy v468;
2. all current marked endpoints needed for v467 additivity replay to one;
3. every reached source block/old expression is bound to its authenticated
   literal ancestry;
4. every reached lower pivot passes (2.1); and
5. every reached physical-grade pivot passes (2.3)--(2.6).

For the exact Task595 root order

\[
 C_T=\operatorname{Prod}
   \bigl(\operatorname{Pow}(W_{j_i},a_i)\bigr)_{i=1}^{3317},
                                                               \tag{3.1}
\]

one has

\[
 \mathcal E^{\rm phys}_{<1}(C_T)=0,\qquad
 \mathcal E^{\rm phys}_{1}(C_T)
       =\sum_{i=1}^{3317}a_i b_{j_i}.              \tag{3.2}
\]

If the authenticated MEMBER equation identifies the right side of (3.2)
with the grade-one residual, and the separately authenticated prior root
\(C_{<1}\) replays to the target through precision zero, then

\[
 C_1=\operatorname{Compose}(C_{<1},C_T)             \tag{3.3}
\]

replays to the complete target through precision one.

#### Proof

First prove (2.1) for the reached lower nodes by induction over their accepted
order, applying each recorded origin, ordered reduction and scale to the
complete pair \((\ell,g)\). Equation (2.3) is then the exact lower reduction
which created the offered old companion. Starting from block origins and
(2.3), induct on the physical-grade pivot id in (2.4). Current endpoint one
and the Fox product/inverse laws of v467 make both physical interpreters
additive on these exact words, so (2.5) gives (2.6).

Applying the same laws in the untouched root order (3.1) gives (3.2). The
MEMBER equation and the direct prior-root replay then give (3.3). At no point
is an old/lower word assigned a class in \(F^1/F^2\). \(\square\)

### Corollary 3.2 (fresh residual licence)

Only after the endpoint gates and the complete equality in Theorem 3.1 may
the consumer define

\[
 \rho_2=\operatorname{gr}_2
   \bigl(T_{\le2}-\mathcal E^{\rm phys}_{\le2}(C_1)\bigr).      \tag{3.4}
\]

V467's quotient-specific adjoint pass may evaluate the right side without a
flat word, while the canonical noncommutative graph and root (3.3) remain
unchanged. Equation (3.4) proves neither source relative-kernel membership
nor success of the grade-two MEMBER test.

## 4. Repaired authoritative transcript check

Replace v468 checker item 5 by the following selected-only deterministic
replay.

1. Recreate each reached physical source origin from the authenticated old
   lower/lift blobs or character-block basis row and the exact registered
   aggregation.
2. For every reached physical-lower pivot, compare its exported logical
   origin, scale, coefficient values and complete ordered edge interval with
   the deterministic lower route. Reconstruct both \(\ell_k\) and \(g_k\)
   and check (2.1).
3. For every reached physical-grade pivot, compare the same four fields with
   the deterministic grade route. For an old connection, apply its exported
   lower interval and require (2.3); then reconstruct (2.5), require (2.6),
   and compare the packed row byte for byte with the authenticated Task595
   basis row at the original pivot id.
4. For every reached block/old node and every reached non-DAG defect, compare
   its original id, origin, scale, exact ordered reductions, character signs
   and referenced `seed_reductions` or single `actor_transitions` expression
   with the sealed source record.
5. Only after these local comparisons, check the exact 3317-term MEMBER
   reconstruction and zero remainder.

The checker may route all 8059 logical inputs and retain data only for the
selected set, or may replay the selected recurrences from authenticated
earlier rows. It need not export unselected source nodes or materialize a
flat word. A mutation of local edge order must fail even when it leaves the
abelian terminal basis unchanged.

The derived adjoint flow and its coalesced literal leaf map are not evidence
for items 1--4. They are checked only after the canonical parent graph has
passed.

## 5. Exact boundary

```text
PURE SOURCE NODE GRADE CLASS:                  AS IN V465, WITH SOURCE PREMISE
MIXED OLD/LOWER NODE SOURCE GRADE CLASS:       NOT ASSERTED
SELECTED LOWER ROW + COMPANION REPLAY:         PAPER-CLOSED UNDER EXACT INPUTS
SELECTED PHYSICAL-GRADE RECURRENCE:            PAPER-CLOSED UNDER ENDPOINT GATES
COMPLETE CURRENT PRECISION-ONE ROOT:           PAPER-CLOSED UNDER MEMBER REPLAY
CANONICAL LOCAL ORDER AUTHENTICATION:          REQUIRED BY SELECTED REROUTE
FRESH GRADE-TWO RESIDUAL:                      AUTHORIZED ONLY AFTER THESE GATES
SOURCE RELATIVE-KERNEL / ALL-EDGE SURJECTIVITY: NOT PROVED
ACTUAL SLP / GRADE TWO / A0 / COMMON:          NOT DECLARED
COFINAL LIFT / FAKE / IHARA:                   NOT DECLARED
verified:                                      false
```

`R07_CANONICAL_SELECTED_SLP_PHYSICAL_REPLAY_V469_CANDIDATE`
