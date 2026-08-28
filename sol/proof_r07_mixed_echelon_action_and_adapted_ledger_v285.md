# R07 mixed-echelon action and adapted-ledger theorem v285

Author: Sol / 2026-08-29

Status: paper-grade correctness refinement of v272--v274, v280, and v282.
It fixes the formal ancestry required when lazy boundary columns are inserted
after quotient-kernel rows, proves the complete source-action columns for
both MEMBER and rank-rise queries, and transports the v273 discrepancy ledger
through v280's area-adapted basis.  It does not accept the in-progress A4-v5
implementation, compute an actual A4 basis, or construct a compatible lift,
fake certificate, or Ihara witness.  `verified=false`.

## 1. The mixed-pivot problem

Retain v273's notation

\[
 \Psi:\mathcal L_D\twoheadrightarrow D\subseteq A
\tag{1.1}
\]

and an ordered quotient basis \(k_1,\ldots,k_t\).  A lazy oracle keeps a
numerical echelon for the changing space

\[
 U=B+\langle k_1,\ldots,k_t\rangle .
\tag{1.2}
\]

Boundary columns can be discovered after some \(k_i\) have already been
inserted.  Reducing a new raw boundary \(d=\Psi(Q_d)\) against the combined
echelon may subtract K pivots.  Its stored numerical pivot need therefore not
itself lie in \(D\), even though adjoining it enlarges (1.2) by exactly the
raw boundary column \(d\).

Consequently neither a label `B` nor a mutable pivot coefficient vector is
enough.  Every combined numerical pivot \(p_\alpha\) must carry a formal pair

\[
 \boxed{(Q_\alpha,C_\alpha)\in
 \mathcal L_D\times\mathbf F_3^t,
 \qquad
 p_\alpha=\Psi(Q_\alpha)+\sum_{i=1}^t C_{\alpha i}k_i.}
\tag{1.3}
\]

The K-coordinate vector is extended by zeros whenever a later K row is
appended.  This is a semantic equality in the raw ten-context module, not a
claim about how a pivot was originally discovered.

## 2. Formal row operations

Let a target reduce in the external subtraction convention as

\[
 r=v-\sum_\alpha\mu_\alpha p_\alpha.
\tag{2.1}
\]

Define

\[
 Q=\sum_\alpha\mu_\alpha Q_\alpha,
 \qquad
 c_i=\sum_\alpha\mu_\alpha C_{\alpha i}.
\tag{2.2}
\]

Then exact expansion of (1.3) gives

\[
 \boxed{r=v-\Psi(Q)-\sum_i c_i k_i.}
\tag{2.3}
\]

This converts any internal `remainder = input + coefficients*stored` ABI
once at its boundary; the exported \((Q,c)\) always has the meaning (2.3).

### Lemma 2.1 (FORMAL ECHELON UPDATE)

Suppose a numerical row operation replaces

\[
 p_\beta\longmapsto
 a p_\beta+\sum_\alpha b_\alpha p_\alpha.
\tag{2.4}
\]

Applying the same operation to its formal pair,

\[
 (Q_\beta,C_\beta)\longmapsto
 \left(aQ_\beta+\sum_\alpha b_\alpha Q_\alpha,
       aC_\beta+\sum_\alpha b_\alpha C_\alpha\right),
\tag{2.5}
\]

preserves (1.3).

#### Proof

Apply the linear map
\((Q,C)\mapsto\Psi(Q)+\sum_i C_i k_i\) to (2.5).  Its image is exactly
(2.4).  \(\square\)

Thus an append-only row echelon may leave older formals unchanged.  A reduced
row-echelon implementation which clears a new pivot from older rows must
apply every such clearing operation to the older formal pairs as well.

## 3. Boundary and K insertions

Suppose a selected raw boundary column \(d=\Psi(Q_d)\) reduces by (2.1) and
is normalized by \(s\in\mathbf F_3^\times\).  Its new combined pivot is

\[
 p_{\rm new}=s\left(d-\sum_\alpha\mu_\alpha p_\alpha\right).
\tag{3.1}
\]

It receives the formal pair

\[
 \boxed{
 Q_{\rm new}=s\left(Q_d-\sum_\alpha\mu_\alpha Q_\alpha\right),
 \qquad
 C_{{\rm new},i}=-s\sum_\alpha\mu_\alpha C_{\alpha i}.}
\tag{3.2}
\]

This pivot may have nonzero K coordinates.  The raw boundary roster still
adds \(d\), not \(p_{\rm new}\), and the equality

\[
 \langle U,p_{\rm new}\rangle=\langle U,d\rangle
\tag{3.3}
\]

shows that the numerical live space is unchanged by this distinction.

For a complete zero-correlation query, first expand its reduction by (2.2):

\[
 r=v-\Psi(Q)-\sum_{i<t}c_i k_i\ne0,
 \qquad k_t=s r.
\tag{3.4}

The newly inserted K pivot is the numerical row \(k_t\) itself and has the
formal pair

\[
 \boxed{(0,e_t).}
\tag{3.5}

Here \(e_t\) is the new standard basis vector.  Equations (3.2), (3.5), and
Lemma 2.1 inductively attach a valid formal pair to every combined pivot,
regardless of the interleaving of boundary and K discoveries.

### Theorem 3.1 (MIXED-ECHELON REPLAY)

At every lazy-oracle epoch, expanding the combined reduction through its
formal pairs produces the exact v273 external relation (2.3).  In particular:

1. a zero remainder is a genuine MEMBER relation in
   \(D+\langle k_1,\ldots,k_t\rangle\);
2. a K rank rise uses the exact \(Q,c,s\) required by v273's word and
   discrepancy recurrence; and
3. later boundary discoveries cannot change any already exported quotient
   relation.

#### Proof

The base echelon is empty.  Boundary insertion preserves (1.3) by (3.2), K
insertion preserves it by (3.5), and any further row operation preserves it
by Lemma 2.1.  Equation (2.3) then follows at every epoch.  The three claims
are respectively the cases \(r=0\), (3.4), and equality in the fixed raw
ledger/K grammar.  V273 Theorem 6.1 separately proves that later elements of
\(D\) cannot destroy earlier quotient independence. \(\square\)

## 4. Complete source-action columns

Fix the column convention in which the \(p\)-th column of \(M_a\) is the
coordinate vector of \(a\cdot k_p\) in the final ordered K basis.  Query the
action target \(v=a\cdot k_p\) through the same mixed oracle.

For a MEMBER result, (2.3) with \(r=0\) gives

\[
 a\cdot k_p\equiv\sum_{i\le t}c_i k_i\pmod D,
\tag{4.1}
\]

so its action column is \(c\).

For a rank rise, (3.4) gives

\[
 k_{t+1}=s\left(v-\Psi(Q)-\sum_{i\le t}c_i k_i\right).
\tag{4.2}

Since every nonzero scalar in \(\mathbf F_3\) is its own inverse,

\[
 \boxed{
 a\cdot k_p\equiv
 \sum_{i\le t}c_i k_i+s^{-1}k_{t+1}
 =\sum_{i\le t}c_i k_i+s k_{t+1}\pmod D.}
\tag{4.3}

Thus the rank-rise column is \(c+s e_{t+1}\), not merely \(e_{t+1}\).
Future K insertions only append zero coordinates to this already exact
column.

### Theorem 4.1 (QUEUE EXHAUSTION GIVES THE FULL ACTION MATRICES)

Assume every accepted K item is processed under
\(x,x^{-1},y,y^{-1}\), every query is certified by v272/v274 and Theorem
3.1, and the queue exhausts.  Padding the columns (4.1) and (4.3) to the final
basis size gives the complete four source-action matrices.  They satisfy

\[
 M_xM_{x^{-1}}=M_{x^{-1}}M_x=I,
 \qquad
 M_yM_{y^{-1}}=M_{y^{-1}}M_y=I.
\tag{4.4}

#### Proof

Every final basis item has exactly one processed record for each signed
actor.  Equations (4.1) and (4.3) give its actual quotient image, so the
columns define the restrictions of the four genuine source actions to K.
Queue exhaustion proves closure.  The two actor pairs are inverse on the
ambient quotient; applying either product to every basis vector gives the
corresponding equality in (4.4). \(\square\)

An executable certificate must replay
\(a\cdot k_p-\Psi(Q)\) against the claimed full column.  Matrix inverse laws
alone are insufficient because two mutually inverse but unrelated matrices
could otherwise pass.

## 5. Word and discrepancy DAG types

For a K word node retain

\[
 (W,k,E),\qquad \delta(W)=k+\Psi(E),\qquad\rho_0(W)=1.
\tag{5.1}

Product, inverse, and scalar-power nodes between K nodes use

\[
 (k,E)(k',E')=(k+k',E+E'),
 \quad (k,E)^{-1}=(-k,-E),
 \quad (k,E)^s=(sk,sE).
\tag{5.2}

For a signed source actor \(a\), conjugation is a distinct typed operation:

\[
 \boxed{a(W,k,E)a^{-1}=(aWa^{-1},a\cdot k,a\cdot E).}
\tag{5.3}

It is invalid to treat (5.3) as ordinary addition of three detached K
ledgers: the actor itself has nontrivial roof value.  Equivalently one may
implement the full semidirect ledger law, but a K-only persistent DAG must
have the explicit conjugation node (5.3).

Combining (5.3) with Theorem 3.1 and v273 (4.3)--(4.4) gives every new K item
an exact literal word and boundary ledger.  Hash-consing may share immutable
nodes, but acceptance expands or independently evaluates the selected
finite roster and checks (5.1) in all ten contexts.

## 6. Transport through the v280 adapted basis

Let each accepted A4 item satisfy

\[
 \delta(W_i)=k_i+\Psi(E_i).
\tag{6.1}

Use v280's recomputed least index \(j\), exponents \(a_i\), and
\(e=a_j^{-1}\).  Define

\[
 \begin{aligned}
 W_*&=\operatorname{red}(W_j^e),
 &k_*&=e k_j,
 &E_*&=eE_j,\\
 \widetilde W_i&=\operatorname{red}(W_iW_*^{-a_i}),
 &\widetilde k_i&=k_i-a_i k_*,
 &\widetilde E_i&=E_i-a_iE_*
 \quad(i\ne j).
 \end{aligned}
\tag{6.2}

Because all these words have trivial lower roof value, (6.1) and the
additive laws (5.2) give

\[
 \boxed{
 \delta(W_*)=k_*+\Psi(E_*),
 \qquad
 \delta(\widetilde W_i)=\widetilde k_i+Psi(\widetilde E_i).}
\tag{6.3}

Let old basis coordinates be ordered \(1,\ldots,t\), and new coordinates be
ordered by `*` followed by the old indices \(i\ne j\).  The change matrix
\(T\), defined by \(K'=KT\), has columns

\[
 T_{*}=e e_j,
 \qquad
 T_{\widetilde i}=e_i-a_i e e_j.
\tag{6.4}

Its inverse, defined by \(K=K'T^{-1}\), has columns

\[
 (T^{-1})_j=a_j e_*,
 \qquad
 (T^{-1})_i=e_{\widetilde i}+a_i e_*quad(i\ne j).
\tag{6.5}

Direct multiplication gives \(TT^{-1}=T^{-1}T=I\).  Hence a consumer can
check the adapted raw rows, literal words, discrepancy ledgers, and both
directions of the basis change without trusting an `adapted_basis=true`
field.

## 7. Independent checker and resource consequences

The producer and checker may use different pivot orders, so combined-pivot
labels need not agree.  Each side must nevertheless reconstruct its own
formal pairs and reduce every reported semantic object to the common raw
grammar:

1. translated boundary symbols \((i,j,t)\);
2. the chronological ordered K rows;
3. exact sparse rows in the ten-context module; and
4. literal K words with their v273 ledgers.

The checker then compares exact expanded equations, not producer pivot
coordinates.  Required destructive controls include changing one
mixed-pivot K coefficient, omitting one boundary formal during a late B
insertion, using \(e_{t+1}\) instead of (4.3), failing to pad an early action
column, treating conjugation as ledger addition, changing \(E_*\) or one
\(\widetilde E_i\), and corrupting either matrix in (6.4)--(6.5).

Formal pairs are sparse persistent objects.  Updating them under the same
row operations is linear in the touched support; it requires neither a full
boundary enumeration nor expanded-word commutation.  Checkpoints must store
the raw B/K rosters and enough deterministic state to rebuild and compare all
formals.  A checkpoint containing only numerical pivots or labels cannot
resume the certificate.

## 8. Fixed frontier

```text
DYNAMIC B-AFTER-K MIXED ECHELON FORMALS:       PAPER PROOF
MEMBER AND RANK-RISE ACTION COLUMNS:           PAPER PROOF
FOUR ACTION MATRICES AFTER QUEUE EXHAUSTION:   PAPER PROOF
TYPED CONJUGATION LEDGER:                      PAPER PROOF
V280 ADAPTED DISCREPANCY LEDGERS / T,T^-1:     PAPER PROOF
ACTUAL A4 CLOSURE / ORDERED BASIS / MATRICES:  NOT COMPUTED
ACTUAL A5 / A6 / COMPATIBLE LIFT:              NOT COMPUTED
FAKE / IHARA WITNESS:                          NONE
```

`R07_MIXED_ECHELON_ACTION_AND_ADAPTED_LEDGER_V285_PAPER_GRADE`
