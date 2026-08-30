# R07 A0 partial-boundary occurrence selector (v405)

Author: Sol / 2026-08-30

Status: paper theorem combining v396, v400--v404.  It replaces the bounded
shortlex conjugator search by an exact finite invariant closure while still
avoiding both PB3 closures and the five central PB4 closures.  This is a
production selector theorem, not an executed A0 terminal.  No common word,
compatible lift, fake, or Ihara witness is reported.  `verified=false`.

## 1. Quotient only the occurrence boundaries which already have closed maps

Let \(\mathcal O\) be the eleven separately tagged correction occurrences:
six PB3 occurrences and five PB4 occurrences.  Before physical aggregation
write

\[
 U=\bigoplus_{o\in\mathcal O}C_o\oplus k^2,
 \qquad k=\mathbf F_3,
\tag{1.1}
\]

where the final summand is v399's normalized exponent pair.

For a PB3 occurrence let \(B_o=D_3\), the full two-family relation boundary
of v401.  For a PB4 occurrence let

\[
 B_o=D_{\rm cen},
\tag{1.2}
\]

the span of only the five central commutator families of v402.  Put

\[
 B_{\rm par}=\bigoplus_oB_o\oplus0.
\tag{1.3}
\]

Every \(B_o\) is a full left-translation span of its chosen relator rows.
Therefore all four occurrencewise source actors preserve it.  The quotient

\[
 \bar U=U/B_{\rm par}
\tag{1.4}
\]

has an explicit sparse realization:

\[
 \bar U=
 \left(\bigoplus_{o\ {m PB3}}Y_{3,o}\right)
 \oplus
 \left(\bigoplus_{o\ {m PB4}}Y^{\rm cen}_{4,o}\right)
 \oplus k^2,
\tag{1.5}
\]

using v401's \(Q_3\) and v402's \(Q_4^{\rm cen}\).  No global boundary
echelon occurs in (1.5).

If \(w_o(a)\) is the frozen prefix-conjugated actor for
\(a\in\{x,x^{-1},y,y^{-1}\}\), its exact quotient action is

\[
 \bar\rho_o(a)=Q_oL_{w_o(a)}\iota_o,
\tag{1.6}
\]

where \(\iota_o\) is any fixed sparse section of the corresponding normal
map.  This is independent of the section because \(B_o\) is left invariant.
The two exponent coordinates have the trivial action.  Equation (1.6), not
a common action after aggregation, is the registered semilinear actor.

## 2. Exact 44-seed correction closure

Let \(r_1,\ldots,r_{44}\) be the accepted compact presentation roster and
let \(\widehat J_g(r_i)\in U\) be its full prefix-transported, occurrence-
tagged Fox row with normalized exponent pair.  By v397 these relators
normally generate the same correction kernel as the historical 6,441-row
roster.  Put

\[
 \bar W=\operatorname{span}_k
 \{\bar\rho(a)\,\overline{\widehat J_g(r_i)}:
 i=1,\ldots,44,\ a\in F(x,y)\}\le\bar U.
\tag{2.1}
\]

### Theorem 2.1 (PARTIAL-QUOTIENT CORRECTION CLOSURE)

The following queue terminates with basis exactly \(\bar W\).

1. Insert the 44 quotient seed rows.
2. Whenever a candidate strictly raises the occurrence-quotient rank, retain
   it and enqueue its four images under (1.6).
3. Discard a dependent candidate and do not enqueue it.

If \(r=\dim_k\bar W\), the queue makes at most

\[
 \boxed{44+4r}
\tag{2.2}
\]

insertion attempts.

#### Proof

This is the invariant-span argument of v396 in the invariant quotient
(1.4).  The output span contains all seeds and is invariant after the queue
exhausts, so it contains (2.1).  Every queued row is obtained from a seed by
the four actors and linear elimination, hence lies in (2.1), giving the
reverse containment.  If a candidate \(u\) is dependent on retained basis
rows \(b_i\), then linearity gives

\[
 \bar\rho(a)u=\sum_i c_i\bar\rho(a)b_i.
\tag{2.3}
\]

Thus discarding \(u\)'s descendants loses no direction.  Only the four
children of each of the \(r\) accepted pivots are attempted, proving (2.2).
\(\square\)

Every pivot remains word-bearing.  A seed is `LEAF(i)`, an actor child is
`CONJUGATE(letter,parent)`, coefficient two is `INVERSE`, and elimination
ancestry is an ordered `PRODUCT`.  Expanding a pivot DAG therefore produces
an actual finite product of conjugates of the 44 literal relators.  No
arbitrary conjugator-length cap remains.

## 3. Aggregate only after occurrence closure

Let \(L_g:U\to Z\) be the frozen signed-prefix physical aggregation and let

\[
 D_{\rm par}=D_3^{(1)}\oplus D_3^{(2)}\oplus D_{\rm cen}^{(4)}\oplus0
 \le Z.
\tag{3.1}
\]

The v400 argument applies verbatim to the smaller boundary (1.3): every
occurrence summand is inserted with a sign and a fixed left translate, so

\[
 L_g(B_{\rm par})\subseteq D_{\rm par}.
\tag{3.2}
\]

Hence there is an induced linear map

\[
 \bar L_g:\bar U\longrightarrow
 \bar Z:=Z/D_{\rm par}
 \cong Y_3^{(1)}\oplus Y_3^{(2)}
       \oplus Y_4^{\rm cen}\oplus k^2.
\tag{3.3}
\]

The quotient correction image is exactly

\[
 \boxed{(D_{\rm par}+L_gJ(\Omega))/D_{\rm par}
       =\bar L_g(\bar W).}
\tag{3.4}
\]

Operationally, each retained occurrence pivot is first acted on and reduced
with all eleven tags separate.  Only then is its pivot representative
summed into the two PB3 and one PB4 physical blocks.  A physically dependent
aggregate must not suppress the pivot's occurrence-level descendants; the
queue decision is made solely in \(\bar U\).

## 4. The only remaining physical boundary is the six-action space

Inside \(\bar Z\), both PB3 boundary summands and the five central PB4
families have vanished.  The remaining boundary is

\[
 \widetilde D_0=(0,0,D_0,0),
\tag{4.1}
\]

where \(D_0\le k[H_0]^5\) is generated by the six action rows of v404.
Let \(\bar T\) be the target normal form.  The exact A0 equation is now

\[
 \boxed{-\bar T\in\bar L_g(\bar W)+\widetilde D_0.}
\tag{4.2}
\]

After the queue of Theorem 2.1 is exhausted, insert the physical aggregates
of its pivot basis into one sparse physical echelon.  For a nonzero target
remainder choose a separating dual \(\lambda\).  V404 computes every
nonzero pairing with \(\widetilde D_0\) by the six support accumulators

\[
 t=gh^{-1}.
\tag{4.3}
\]

An active accumulator supplies a rank-raising boundary row.  Recompute the
dual and repeat.  If the target becomes zero, (4.2) is positive.  If all six
accumulators are empty while the target pairing remains nonzero, v404 proves
that \(\lambda\) annihilates all of \(\widetilde D_0\); since \(\bar W\) was
already exhausted, this is an exact negative separator for (4.2), not a
prefix heuristic.

### Theorem 4.1 (COMPLETE FINITE A0 SELECTOR)

The occurrence queue of Theorem 2.1 followed by the v404 physical boundary
oracle decides the A0 equation (4.2) after finitely many strict rank rises.
It neither enumerates a joint conjugator group nor materializes any of the
seven eliminated boundary closures.

#### Proof

Theorem 2.1 and (3.4) exhaust the complete correction image.  V404 either
adds a row outside the present physical span or certifies that the current
dual annihilates the entire remaining boundary (4.1).  The ambient spaces
are finite-dimensional, so only finitely many additions occur.  Zero gives
membership; a nonzero dual after an empty exact boundary oracle annihilates
both summands in (4.2) and separates the target. \(\square\)

## 5. Positive certificate and checkpoint boundary

On a positive terminal, physical echelon ancestry selects:

- occurrence pivots, each with a literal compact-relator instruction DAG;
- finitely many of the six PB4 action rows and their \(H_0\) translations;
- zero PB3 and zero central-PB4 live rows; and
- the exact normalized exponent pair.

Expand only the selected correction DAG, perform v399 exactification, and
run v403's joint-kernel, integer exponent, fresh unquotiented Fox,
quotient-normal, selected-action and survivor replay.  These gates yield an
exact common word.  Eliminated-boundary ancestry is unnecessary by v403's
kernel theorem.

A resumable checkpoint must contain two distinct owners:

1. the complete occurrence echelon, queue/frontier, source DAG and its
   44-seed/four-actor cursor; and
2. the physical echelon with correction-pivot references, selected
   six-action rows, order and ancestry.

Saving only the physical rank or a shortlex conjugator cursor is not a
continuation of this selector.

## 6. Fixed consequence

The bounded length-six schedule of task413/task419 is no longer the preferred
or mathematically complete correction route.  It is replaced by the exact
44-seed invariant queue (2.2).  The route now has no unregistered search
universe:

```text
PB3 OCCURRENCE BOUNDARIES:                 CLOSED NORMAL MAPS
FIVE CENTRAL PB4 OCCURRENCE FAMILIES:      CLOSED NORMAL MAP
COMPACT CORRECTION CONJUGATORS:            EXACT 44+4r INVARIANT QUEUE
REMAINING SIX PB4 PHYSICAL FAMILIES:        EXACT v404 SUPPORT ORACLE
FINITE A0 MEMBER/NONMEMBER SELECTOR:        PAPER THEOREM
ACTUAL A0 COMMON WORD:                     NOT COMPUTED
COMPATIBLE LIFT / FAKE / IHARA WITNESS:    NONE
```

`R07_A0_PARTIAL_BOUNDARY_OCCURRENCE_SELECTOR_V405_PAPER_GRADE`
