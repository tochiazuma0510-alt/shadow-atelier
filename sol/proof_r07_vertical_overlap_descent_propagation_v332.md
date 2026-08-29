# R07 vertical propagation by horizontal overlap descent (v332)

Author: Sol / 2026-08-29

Status: paper theorem combining v314/v316 with the horizontal exact sequence
of v331.  Between two matched refinements, every genuinely new common-source
identity is assembled from genuinely new cumulative Goursat overlap scores.
If no overlap score is born upstairs, one finite MEMBER target propagates to
the next refinement automatically; uniform overlap descent propagates it
through the whole cofinal tower.  The actual R07 overlap-descent equalities
have not been computed.  No compatible lift, fake certificate or Ihara
witness is declared.  `verified=false`.

## 1. Two compatible Goursat chains

Let (n) and (n+1) be consecutive matched finite refinements.  At each
level retain an ordered cumulative chain

\[
 H_{i,r}=H_{i-1,r}\times_{D_{i,r}}G_{i,r},
 \qquad r\in\{n,n+1\},
\tag{1.1}
\]

and surjective reduction maps

\[
 \rho^H_i:H_{i,n+1}\twoheadrightarrow H_{i,n},
 \quad
 \rho^G_i:G_{i,n+1}\twoheadrightarrow G_{i,n},
 \quad
 \rho^D_i:D_{i,n+1}\twoheadrightarrow D_{i,n}.
\tag{1.2}
\]

Assume the Goursat squares commute:

\[
 \rho^D_i\alpha_{i,n+1}=\alpha_{i,n}\rho^H_{i-1},
 \qquad
 \rho^D_i\beta_{i,n+1}=\beta_{i,n}\rho^G_i.
\tag{1.3}
\]

Let (U_{j,r}\le k[G_{j,r}]),
(Q_{j,r}=k[G_{j,r}]/U_{j,r}), and
(W_{j,r}=U_{j,r}^\perp\).  Require the local quotients to reduce naturally,
so pullback of functions gives injections

\[
 (\rho^G_j)^*:W_{j,n}\hookrightarrow W_{j,n+1}.
\tag{1.4}
\]

The resulting coordinatewise pullback is denoted simply by

\[
 \rho_i^*:\bigoplus_{j\le i}W_{j,n}
   \hookrightarrow\bigoplus_{j\le i}W_{j,n+1}.
\tag{1.5}
\]

Let (mathcal I_{i,r}) and (mathcal P_{i,r}) be respectively v331's
cumulative identity and overlap-score spaces at level (r).

## 2. Naturality of the horizontal exact sequence

### Lemma 2.1 (OVERLAP PULLBACK)

Pullback by (ho_i^D) sends

\[
 (\rho_i^D)^*:\mathcal P_{i,n}hookrightarrow
                 \mathcal P_{i,n+1}.
\tag{2.1}
\]

Moreover the v331 short exact sequences form a commutative diagram

\[
\begin{array}{ccccccccc}
0&\to&\mathcal I_{i-1,n}&\to&\mathcal I_{i,n}&\to&
 \mathcal P_{i,n}&\to&0\\
 &&\downarrow\rho_{i-1}^*&&\downarrow\rho_i^*&&
 \downarrow(\rho_i^D)^*&&\\
0&\to&\mathcal I_{i-1,n+1}&\to&\mathcal I_{i,n+1}&\to&
 \mathcal P_{i,n+1}&\to&0.
\end{array}
\tag{2.2}
\]

#### Proof

Let (psi\in\mathcal P_{i,n}).  By definition,
(alpha_{i,n}^*\psi) is a sum of admissible lower local scores and
(eta_{i,n}^*\psi\in W_{i,n}).  Pull those scores through (1.4), and use
the two commuting identities (1.3).  They show that
((\rho_i^D)^*\psi) satisfies both defining conditions for
(mathcal P_{i,n+1}).  Surjectivity of (ho_i^D) makes pullback
injective.

Pullback of a zero additive score remains zero on the upper joint image, so
it sends (mathcal I_{i,n}) into (mathcal I_{i,n+1}).  V331's quotient
score attached to the pulled identity is exactly
((\rho_i^D)^*\psi), again by (1.3).  This proves every square in (2.2).
(\square\)

## 3. Every new identity is an extension of new overlap scores

Define the vertical novelty spaces

\[
 \mathcal C_{i,n}
 =\mathcal I_{i,n+1}/\rho_i^*\mathcal I_{i,n},
\tag{3.1}
\]

\[
 \mathcal E_{i,n}
 =\mathcal P_{i,n+1}/(\rho_i^D)^*\mathcal P_{i,n}.
\tag{3.2}
\]

### Theorem 3.1 (NOVEL-IDENTITY EXACT SEQUENCE)

For (i\ge2), there is a short exact sequence

\[
 \boxed{
 0\longrightarrow\mathcal C_{i-1,n}
 \longrightarrow\mathcal C_{i,n}
 \longrightarrow\mathcal E_{i,n}
 \longrightarrow0.}
\tag{3.3}
\]

In particular,

\[
 \boxed{
 \dim\mathcal C_{m,n}
   =\sum_{i=2}^m\dim\mathcal E_{i,n}.}
\tag{3.4}
\]

#### Proof

All vertical maps in (2.2) are injective.  Quotient the lower exact row from
the upper row.  The induced sequence is exact: explicitly, an upper identity
whose overlap class descends can be adjusted by a pulled lower identity with
the same overlap score; the difference lies in the preceding upper identity
space.  It is trivial modulo pulled identities exactly when that preceding
class descends.  Conversely every novel overlap class has an upper identity
lift by v331 Theorem 2.1.  This proves (3.3).

At (i=1), both identity spaces vanish, so
(mathcal C_{1,n}=0).  Taking dimensions in (3.3) and iterating gives
(3.4).  \(\square\)

Thus v316's possible new vertical dual obstruction is horizontally graded by
the concrete overlap novelties (mathcal E_{i,n}).  A monolithic upper
identity basis is unnecessary.

## 4. Exact one-step propagation of an actual target

Let

\[
 a_r=(a_{1,r},\ldots,a_{m,r})
 \in\bigoplus_jQ_{j,r}
\tag{4.1}
\]

be compatible target classes:

\[
 (\rho_j^G)_*a_{j,n+1}=a_{j,n}.
\tag{4.2}
\]

Assume (a_n) is MEMBER in the level-(n) common-source marginal image.
Then it annihilates every identity in (mathcal I_{m,n}).  Consequently the
pairing of (a_{n+1}) with an upper identity depends only on its novelty
class in (mathcal C_{m,n}), since for every lower identity (phi),

\[
 \langle\rho_m^*\phi,a_{n+1}\rangle
   =\langle\phi,a_n\rangle=0.
\tag{4.3}
\]

### Theorem 4.1 (TARGET-SPECIFIC SUCCESSOR GATE)

Under the preceding hypotheses,

\[
 \boxed{
 a_{n+1}\text{ is MEMBER}
 \quad\Longleftrightarrow\quad
 \langle c,a_{n+1}\rangle=0
 \text{ for every }c\in\mathcal C_{m,n}.}
\tag{4.4}
\]

It is enough to test identity lifts of bases of the overlap novelty spaces
(mathcal E_{i,n}), together with the inherited novelty basis from
(mathcal C_{i-1,n}).

#### Proof

By v329 finite duality, the upper target is MEMBER exactly when it annihilates
all of (mathcal I_{m,n+1}).  The pulled lower subspace already pairs to
zero by (4.3), so this is equivalent to vanishing on the quotient
(mathcal C_{m,n}).  The final assertion follows recursively from (3.3).
(\square\)

A nonzero pairing with one named lifted overlap novelty is a complete
successor obstruction.  If all pairings vanish, finite primal elimination
recovers the upper coefficient; no arbitrary choice of a compatible lift is
assumed.

## 5. When one successful level propagates through every refinement

### Corollary 5.1 (NO-NEW-OVERLAP PROPAGATION)

If, at one refinement edge,

\[
 \boxed{
 \mathcal P_{i,n+1}
  =(\rho_i^D)^*\mathcal P_{i,n}
 \quad\text{for every }i\ge2,}
\tag{5.1}
\]

then

\[
 \mathcal I_{m,n+1}=\rho_m^*\mathcal I_{m,n},
\tag{5.2}
\]

and every compatible level-(n) MEMBER target is MEMBER at level (n+1).

#### Proof

Condition (5.1) says every (mathcal E_{i,n}=0).  Equations (3.3)--(3.4)
give (mathcal C_{m,n}=0), and Theorem 4.1 gives target propagation.
(\square\)

### Corollary 5.2 (ONE LEVEL TO THE COFINAL LINEAR LIFT)

Suppose (5.1) holds at every edge of a matched cofinal tower and the target
classes reduce compatibly.  Then one MEMBER target at the initial registered
level is MEMBER at every later level.  V313's finite-fibre compactness gives
one compatible completed common-source coefficient.

If, in addition, bases and right inverses for the overlap systems commute
with reduction, v314/v322/v324 construct the coefficient recursively rather
than only obtaining it by compactness.

#### Proof

Iterate Corollary 5.1.  Every finite solution set is nonempty and maps into
the preceding one.  V313 applies to the resulting inverse system of finite
nonempty sets.  Natural right inverses give the stronger explicit recursion.
(\square\)

This is the precise form in which one successful stage can imply all stages.
The hypothesis is not merely equality of local group orders or dimensions:
it is equality of the complete authenticated overlap-score subspaces under
pullback.  When it fails, Theorem 4.1 still leaves only the novel quotient
classes, not the whole upper dual, to test against the actual target.

## 6. R07 application and certificate boundary

At every R07 matched edge, an acceptable overlap-descent certificate contains:

1. the compatible finite joint groups and cumulative Goursat quotient maps;
2. both complete overlap-score bases, generated from v323 and v330;
3. direct pullback of every lower basis row;
4. two-way span containment proving (5.1), or a basis of the quotient
   (mathcal E_{i,n});
5. for a target-specific pass, identity lifts of every novel basis and their
   zero target pairings; and
6. on MEMBER, independently replayed v324--v325 primal ancestry.

Rank equality alone does not prove (5.1).  A bounded sample of score rows does
not prove completeness.  Natural cofinal selection requires map-level replay,
not coincident dimensions at adjacent levels.

The theorem closes only the linear common-source endpoint propagation.  It
does not establish the actual overlap equalities, the nonlinear weighted or
retract step, formation, settlement, perfect-core compatibility, or the final
R07 side gates.

```text
NEW VERTICAL IDENTITIES FROM OVERLAP NOVELTIES:     EXACT SEQUENCE
TARGET-SPECIFIC NEXT-LEVEL GATE:                    COMPLETE FINITE DUAL
NO NEW OVERLAP SCORES => MEMBER PROPAGATION:        PAPER PROOF
ALL EDGES STABLE => ONE LEVEL TO COFINAL LINEAR:    PAPER PROOF
ACTUAL R07 OVERLAP DESCENT / NOVEL PAIRINGS:        NOT COMPUTED
NATURAL PRIMAL RIGHT INVERSES:                      NOT CONSTRUCTED
NONLINEAR / FORMATION / PERFECT-CORE GATES:         OPEN
COMPATIBLE FULL LIFT / FAKE / IHARA WITNESS:        NOT CONSTRUCTED
```

`R07_VERTICAL_OVERLAP_DESCENT_PROPAGATION_V332_PAPER_GRADE`
