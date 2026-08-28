# R07 recomputed A4 anchor and area-adapted A5 basis v280

Author: Sol / 2026-08-29

Status: paper theorem and binding consumer refinement of v216, v242, and
v247.  An A5 consumer must not accept a separately asserted A4 anchor or the
Booleans `rho0_replay`, `rho1_in_kernel`, and `q_z0_replay`.  It can derive
the unique deterministic anchor from the accepted ordered word-bearing A4
basis, replay it through the actual maps, and simultaneously change that
basis to an area-adapted word-bearing basis.  In the adapted A5 joint closure
exactly one seed can have a nonzero matching exponent-nine endpoint.  No
actual A4 package, A5 MEMBER, compatible lift, fake certificate, or Ihara
witness is declared.  `verified=false`.

## 1. Frozen first-edge data and the trust boundary

Let

\[
 F(x,y)\mathrel{\mathop{\twoheadrightarrow}^{\rho _1}}\Delta _1
 \mathrel{\mathop{\twoheadrightarrow}^{\pi}}\Delta _0,
 \qquad K=\ker\pi
\tag{1.1}
\]

be the first relative Frattini edge.  Its kernel is an elementary-abelian
three-group.  Retain the matching quotient

\[
 q:\Delta _1\twoheadrightarrow D_1\cong\mathcal H_2(9),
 \qquad q(K)=R_0=\langle z_0\rangle\cong C_3 .
\tag{1.2}
\]

An accepted A4 package supplies an ordered word-bearing basis

\[
 (u_1,k_1),\ldots,(u_t,k_t),
 \qquad \rho _1(u_i)=k_i,
 \qquad K=\langle k_1,\ldots,k_t\rangle_{\mathbf F_3}.
\tag{1.3}
\]

The downstream trust boundary is the complete accepted A4 producer/checker
object bound byte-for-byte to the same task198 roof and maps.  It is not a
standalone dictionary containing an anchor word and success flags.  The A5
consumer independently parses and evaluates every literal word in (1.3),
checks

\[
 \rho _1(u_i)=k_i,
 \qquad \rho _0(u_i)=\pi(k_i)=1,
\tag{1.4}
\]

and computes its (D_1)-image.  Completeness and independence of the basis
remain the accepted A4 theorem; the word values and all data used below are
recomputed by the consumer and its independent checker.

Since (q(k_i)\in R_0), there is a unique

\[
 a_i\in\mathbf F_3
 \quad\text{such that}\quad q(k_i)=z_0^{a_i}.
\tag{1.5}
\]

The consumer obtains (a_i) by literal comparison with
(1,z_0,z_0^2).  A supplied exponent field is ignored as evidence and is
checked only against this result.  If one of the three comparisons fails,
the input is mistyped.  If all (a_i) vanish, (1.2)--(1.3) are inconsistent,
so this is also `UNKNOWN_INPUT`, not an A3 or A5 NONMEMBER terminal.

## 2. Recomputed deterministic anchor

Let

\[
 j=\min\{i:a_i\ne0\},
 \qquad e=a_j^{-1}\in\mathbf F_3^\times,
 \qquad u_*=\operatorname{red}(u_j^e),
 \qquad k_*=k_j^e .
\tag{2.1}
\]

Here `red` is deterministic free reduction and (e\in\{1,2\}).  Neither
(j), (e), (u_*), nor (k_*) is accepted from an anchor subreceipt; all
four are recomputed from (1.3)--(1.5).

### Theorem 2.1 (BOOLEAN-FREE A4 ANCHOR REPLAY)

The recomputed word satisfies

\[
 \boxed{
 \rho _1(u_*)=k_*\in K,
 \qquad \rho _0(u_*)=1,
 \qquad q(k_*)=z_0.}
\tag{2.2}
\]

These assertions admit direct finite replay and require no trusted Boolean.

#### Proof

Evaluation of a literal power gives
(ho _1(u_*)=\rho _1(u_j)^e=k_j^e=k_*).  Since (K) is a subgroup,
(k_*\in K), and (1.4) gives (ho _0(u_*)=1).  Finally,

\[
 q(k_*)=q(k_j)^e=z_0^{a_je}=z_0.
\tag{2.3}
\]

Every equality is evaluated in the pinned finite representations. \(\square\)

Thus the fields `anchor_receipt_identity`, `least_index`,
`projected_exponent`, `inverse_scalar`, `literal_word`, `rho1_in_kernel`,
`rho0_replay`, and `q_z0_replay` may be exported for readability, but none
may control acceptance.  They are derived fields which must equal the
consumer's result.

## 3. Simultaneous area-adapted word basis

For each (i\ne j), retain the original order and define

\[
 \widetilde u_i
 =\operatorname{red}(u_i u_*^{-a_i}),
 \qquad
 \widetilde k_i=k_i k_*^{-a_i}.
\tag{3.1}
\]

Order the new family as (u_*), followed by the
(widetilde u_i) for (i\ne j) in their old order.

### Theorem 3.1 (WORD-BEARING AREA-ADAPTED BASIS)

The family

\[
 \boxed{k_*,\ (\widetilde k_i)_{i\ne j}}
\tag{3.2}
\]

is a basis of (K), carries the literal words in (2.1) and (3.1), and
satisfies

\[
 \boxed{q(k_*)=z_0,
 \qquad q(\widetilde k_i)=1\quad(i\ne j).}
\tag{3.3}
\]

#### Proof

Write (K) additively over (mathbf F_3).  The first replacement is the
nonzero scaling (k_j\mapsto e k_j=k_*).  Every other replacement is the
shear

\[
 k_i\mapsto k_i-a_i k_*.
\tag{3.4}
\]

Scaling by (e\ne0) and these shears form an invertible change of basis, so
(3.2) is a basis.  Literal evaluation of (3.1) gives its displayed group
element.  Equations (1.5) and (2.2) give

\[
 q(\widetilde k_i)=z_0^{a_i}z_0^{-a_i}=1.
\tag{3.5}
\]

The first equality in (3.3) is Theorem 2.1. \(\square\)

The complete consumer certificate records the invertible basis-change
matrix and replays both directions.  Merely reporting equal ranks is not
enough.  It also evaluates every word in (2.1) and (3.1) in (Delta _1),
(Delta _0), and (D_1).

## 4. Exact reduction of the A5 joint input

Put (A=\mathbf F_3[\Delta _1]) and

\[
 I=\ker(A\to\mathbf F_3[\Delta _0]).
\tag{4.1}
\]

Because (3.2) generates (K), the standard relative-ideal identity gives

\[
 \boxed{
 I=A(k_*-1)+\sum_{i\ne j}A(\widetilde k_i-1).}
\tag{4.2}
\]

Retain v214's eleven-occurrence vector (w\in\widehat E_1), the actual
pointed row (d_1\in Z_1^{\rm full}), and the occurrence action before the
non-equivariant block map (C).  Define

\[
 v_*=igl((k_*-1)d_1,(k_*-1)\mathbin\odot w\bigr),
 \qquad
 v_i=igl((\widetilde k_i-1)d_1,
            (\widetilde k_i-1)\mathbin\odot w\bigr).
\tag{4.3}
\]

### Theorem 4.1 (ONE ENDPOINT-BEARING A5 SEED)

One has

\[
 \boxed{
 (k_*-1)\mathbin\odot w=(z_0-1)\mathbin\odot w,
 \qquad
 (\widetilde k_i-1)\mathbin\odot w=0.}
\tag{4.4}
\]

Moreover the invariant span of the seeds in (4.3) is exactly

\[
 \boxed{
 \{(\theta d_1,\theta\mathbin\odot w):\theta\in I\}.}
\tag{4.5}
\]

Thus exactly one initial seed can carry a nonzero matching exponent-nine
endpoint; all other seeds contribute only to the pointed coordinate.  This
changes neither the A5 membership space nor its MEMBER/NONMEMBER answer.

#### Proof

The occurrence action factors through (q).  Equations (2.2) and (3.3)
therefore give (4.4).  Equation (4.2), linearity, associativity of the two
actions, and closure under the marked generators give both containments in
(4.5), exactly as in v214 Theorem 4.1 and v242 Theorem 3.1.  The change of
basis is invertible, so it changes only the generating presentation of the
same relative ideal. \(\square\)

The producer may use the adapted seeds.  A structurally independent checker
may instead reconstruct the original A4 basis seeds and compare the complete
occurrence-level spans in both directions.  This avoids sharing the adapted
basis as an unexamined oracle.

## 5. Local construction of the corrected A3+A4 base point

Let an accepted A3 package return canonical coefficients

\[
 \lambda=\sum_{g\in D_1}\lambda_g g,
 \qquad \lambda_g\in\mathbf F_3,
 \qquad \kappa_D=\lambda(z_0-1).
\tag{5.1}
\]

For every nonzero coefficient, the consumer derives the normal-form section

\[
 g=x^ay^bh^r,qquad
 s(g)=x^ay^bh^r
\tag{5.2}
\]

from the authenticated (D_1) key.  It does not accept a producer-supplied
pair list.  It constructs locally

\[
 \boxed{
 \widetilde\kappa_0
 =\sum_{\lambda_g\ne0}\lambda_g
   \bigl(\operatorname{red}(s(g)u_*)-s(g)\bigr).}
\tag{5.3}
\]

### Theorem 5.1 (SELF-CONSTRUCTED ROOF-FIBRE BASE POINT)

Every pair in (5.3) has equal (Delta _0)-endpoints, and its image in
(mathbf F_3[D_1]) is (g(z_0-1)).  Consequently

\[
 \boxed{
 \kappa_0:=\rho_{1,*}(\widetilde\kappa_0)\in I,
 \qquad q_*(\kappa_0)=\kappa_D.}
\tag{5.4}
\]

If the accepted A3 package proves
(C(\kappa_D\mathbin\odot w)=\bar\epsilon_1), then

\[
 \boxed{C(\kappa_0\mathbin\odot w)=\bar\epsilon_1.}
\tag{5.5}
\]

#### Proof

Theorem 2.1 gives (ho_0(u_*)=1), so the two endpoints in each pair have
the same (Delta _0)-value.  It also gives (q(\rho_1(u_*))=z_0); the
normal-form section maps to (g).  This proves the pairwise assertions and
(5.4).  The source-independent endpoint theorem v214 (2.7) says that the
matching occurrence action depends only on the (D_1)-image, which proves
(5.5). \(\square\)

The A5 receipt exports the locally created ordered pairs and both endpoint
evaluations.  The independent checker rebuilds them from the A3 coefficient
map and A4 words.  A pre-existing `base_pairs` array, a formula string, or
the absence of the substring `[x,y]^3` is never evidence.

## 6. Minimal executable consumer and cost

An honest A5 input adapter performs, in order:

1. authenticate the exact accepted A4 producer/checker pair and common
   roof/tower identities;
2. independently evaluate all ordered A4 basis words as in (1.4);
3. compute every (a_i) by (1.5), choose (2.1), and replay (2.2);
4. construct the adapted basis (3.1), replay its invertible two-way change
   and all values in (3.3);
5. authenticate the A3 coefficient map and derive each section (5.2);
6. construct (5.3) locally and replay every pair through (ho_0,ho_1,q);
7. build the A5 seeds (4.3), close their joint action, and decide the v242
   slice; and
8. on MEMBER, expand the retained ancestry into the same locally replayed
   pair language for A6.

Before joint closure, the added algebra is (O(t+s)) group operations plus
literal evaluation, where (t=\dim_{\mathbf F_3}K) and
(s=|\operatorname{supp}\lambda|).  It enumerates neither all 729 elements
of (D_1) nor a second relative-ideal roster.  The adapted basis reduces the
number of endpoint-bearing initial seeds from (t) to one; it does not omit
the other (t-1) pointed seeds.

The following are fatal input errors, not mathematical negative terminals:

- an unaccepted or digest-mismatched A4 package;
- any literal-word evaluation mismatch;
- an image (q(k_i)\notin\{1,z_0,z_0^2\});
- all recomputed (a_i=0);
- a supplied least index, scalar, anchor word, or basis change differing from
  the recomputed value;
- a copied replay Boolean;
- a supplied rather than locally reconstructed base-pair roster; or
- failure of any pair endpoint or projection replay.

## 7. Fixed frontier

```text
A4 ORDERED BASIS -> DETERMINISTIC ANCHOR:          PAPER PROOF
ANCHOR ACCEPTANCE FROM COPIED BOOLEANS:            REJECTED
A4 BASIS -> AREA-ADAPTED WORD BASIS:               PAPER PROOF
ENDPOINT-BEARING A5 INITIAL SEEDS:                 EXACTLY ONE POSSIBLE
A3+A4 BASE PAIRS CONSTRUCTED BY A5 CONSUMER:       PAPER PROOF
EXTRA PRE-CLOSURE COST:                            O(t + support(lambda))
ACTUAL ACCEPTED A4 BASIS / ANCHOR:                 NOT COMPUTED
ACTUAL A5 JOINT CLOSURE / MEMBER:                  NOT COMPUTED
ACTUAL A6 WORD-PAIR / THREE EXACT PB ENDPOINTS:    NOT COMPUTED
COMPATIBLE COFINAL LIFT / FAKE / IHARA WITNESS:   NOT CONSTRUCTED
```

`R07_RECOMPUTED_ANCHOR_AND_ADAPTED_A5_BASIS_V280_PAPER_GRADE`
