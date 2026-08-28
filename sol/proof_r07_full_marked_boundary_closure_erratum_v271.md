# R07 full-marked boundary closure erratum v271

Author: Sol / 2026-08-29

Status: paper/type correction to v269 and v270.  V270 correctly replaces the
untagged count 13 by 65 A4 boundary seeds, but its proof still uses the wrong
acting group: the two source-context images need not generate the full marked
PB3/PB4 quotient whose presentation boundaries are being divided out.  The
complete producer closure must use the full marked PB generators separately
in every tagged coordinate.  No actual boundary rank, A4 kernel, anchor,
lift, fake, or Ihara witness is declared.  `verified=false`.

## 1. Source action and boundary translation are different actions

For the ten A4 coordinates let

\[
 M=\bigoplus_{i=0}^{9}M_i,
 \qquad
 D=\bigoplus_{i=0}^{9}D_i,
 \qquad
 D_i=\operatorname{span}_{\mathbf F_3}
       \{q\,d_{i,j}:q\in E_i\}.
\tag{1.1}
\]

Here (E_i=E_3) for (i<5), (E_i=E_4) for (i\ge5), and the (d_{i,j})
are the two PB3 or eleven PB4 presentation-boundary rows in the independently
tagged (i)-th summand.  Thus the seed count from v270 remains

\[
 5\cdot2+5\cdot11=65.
\tag{1.2}
\]

Let (X_i,Y_i\in E_i) be the two values of the source letters in context
(i), and put (H_i=\langle X_i,Y_i\rangle\).  Closing the seeds only under
the common source actions (x^{\pm1},y^{\pm1}) constructs at most

\[
 D_i^{\rm src}=\operatorname{span}_{\mathbf F_3}
   \{h\,d_{i,j}:h\in H_i\},
\tag{1.3}
\]

not (1.1).  The equality (D_i^{\rm src}=D_i) requires an additional
surjectivity theorem (H_i=E_i), which v269/v270 did not prove and which is
false for the actual E4 contexts.

This does not change the source-word invariant closure of the eventual
kernel (K): (K) is an (F(x,y))-module and is still closed under the four
source actions.  Only the presentation-boundary subspace (D) requires the
full marked PB action.

## 2. Actual countercheck to the missing surjectivity premise

The cross-checked task176 production run `33044121344` computes the ten
singleton context-image orders from the literal context pairs.  Its accepted
receipt has

\[
 |H_i|=
 \begin{cases}
 39,680,928,&i=0,\ldots,4,\\
 357,128,352,&i=5,6,7,\\
 119,042,784,&i=8,9.
 \end{cases}
\tag{2.1}
\]

The same pinned q3 authority gives the coarse marked PB4 quotient

\[
 |Q_4|=583,152,628,325,845,597,028,352.
\tag{2.2}
\]

The marked (E_4) projects onto this (Q_4), whereas every number in the E4
part of (2.1) is smaller than (2.2).  Hence none of the five actual E4
context pairs generates the full marked (E_4).  In particular the reverse
inclusion step in v269 Theorem 2.1 and v270 Theorem 2.1 cannot be repaired by
the corrected seed count alone.

Equation (2.1) is used only as a countercheck.  The corrected theorem below
does not depend on enumerating (H_i), (E_i), or any quotient state roster.

## 3. Correct coordinatewise marked-generator closure

Let

\[
 S_i=
 \begin{cases}
 \{A_{12}^{\pm1},A_{13}^{\pm1},A_{23}^{\pm1}\},&i<5,\\
 \{A_{12}^{\pm1},A_{13}^{\pm1},A_{14}^{\pm1},
   A_{23}^{\pm1},A_{24}^{\pm1},A_{34}^{\pm1}\},&i\ge5.
 \end{cases}
\tag{3.1}
\]

Run ten tagged queue closures.  For coordinate (i), insert its two or
eleven base rows into a coefficient-bearing echelon.  Whenever an insertion
strictly raises rank, retain its immutable seed/parent/action ancestry,
enqueue the normalized row, and apply every left-translation in (S_i) to
that row.  Stop only when every queue is empty.  Rows and accumulator keys
retain the coordinate tag throughout.

### Theorem 3.1 (FULL-MARKED COMPLETE BOUNDARY CLOSURE)

The direct sum of the ten terminal queue spaces is exactly (D) in (1.1).

#### Proof

Every seed is a presentation-boundary row in its tagged summand.  Every
operation in (3.1) is left translation by an element of the same marked
quotient, and row reduction takes only linear combinations.  Hence every
queue space is contained in (D_i).

Conversely, queue exhaustion makes the (i)-th space invariant under all
marked PB generators and their inverses.  Those marked generators generate
(E_i) by the definition of the matched quotient.  Therefore the terminal
space contains (q d_{i,j}) for every (q\in E_i) and every base relation
(j).  It contains (D_i), proving equality coordinate by coordinate and
then after taking the tagged direct sum.  Every accepted row strictly raises
rank in a finite-dimensional row space, so all queues terminate. \(\square\)

Let

\[
 b_3=\sum_{i=0}^{4}\dim D_i,
 \qquad
 b_4=\sum_{i=5}^{9}\dim D_i,
 \qquad b=b_3+b_4.
\tag{3.2}
\]

There are exactly (b) rank raises.  With the deliberately explicit signed
generator roster, the number of post-seed action candidates is at most

\[
 6b_3+12b_4\le12b,
\tag{3.3}
\]

and total insertion attempts are at most

\[
 65+6b_3+12b_4.
\tag{3.4}
\]

The ten closures may share one sparse-echelon implementation, because the
coordinate tag makes their pivots disjoint, but they must retain ten logical
queues/actions.  Applying ninety coordinate actions to every mixed row is a
correct but needless (90b) implementation.

## 4. Independent complete checker

The v163 support-inversion checker remains valid after the v270 tag repair
and needs no group enumeration.  For every tagged base occurrence
((i,j,c,h,\alpha)) and matching dual-support element (g), it forms

\[
 t=gh^{-1},\qquad th=g,
\tag{4.1}
\]

and accumulates under the complete key ((i,j,t)).  Because (g,h\in E_i),
the reconstructed (t) is automatically in (E_i).  A nonzero accumulator
returns an active full-translation column; complete zero correlation proves
annihilation of every generator of (D_i).  Iterating on strict rank rises
therefore reconstructs the same (D) by an algorithm different from the
producer's marked-generator queues.

Two-way span containment between these two coefficient-bearing bases is the
appropriate completeness certificate.  Source-action closure compared only
with itself is not.

## 5. Required affine evaluator type

The fast v268 word DAG is sound only when its cached node value is the actual
left-Fox affine value, not merely the roof group value.  For a PB word (w)
write

\[
 \mathcal A(w)=(\bar w,\partial w).
\tag{5.1}
\]

With left translation on sparse Fox rows, concatenation and inversion are

\[
 (a,u)(b,v)=(ab,u+a\cdot v),
 \qquad
 (a,u)^{-1}=(a^{-1},-a^{-1}\cdot u).
\tag{5.2}
\]

Thus each of the forty signed context actors must be the affine evaluation
of the corresponding substituted PB word.  Trie/DAG recurrence uses (5.2),
and a bounded direct call to `fox_gradient_without_sections` must agree on
every primitive word and every newly materialized K/anchor word.  A tuple of
roof values, a hash-shaped row, or bridge-ledger signs cannot replace this
affine chain.

## 6. Supersession and fixed frontier

V269 and v270 are superseded wherever they assert that the 65 A4 seeds close
to all presentation boundaries under only
(x,x^{-1},y,y^{-1}), or quote the bounds (4b) and (65+4b).  V270's seed
counts 65 and 15 and its coordinate-aware support-inversion correction remain
valid.  Task332 and task328/v3 are not eligible for execution if they retain
the source-action boundary closure.

```text
A4 TAGGED BASE BOUNDARY SEEDS:                  65
PRODUCER COMPLETE ACTIONS:                      PB3 +/-3, PB4 +/-6 per tag
POST-SEED ACTION CANDIDATES:                    <= 6*b3 + 12*b4
INDEPENDENT SUPPORT-INVERSION CHECKER:          RETAINED
SOURCE x/y ACTION FOR K CLOSURE:                RETAINED, NOT USED FOR D
ACTUAL A4 BOUNDARY RANK / K / ANCHOR:           NOT COMPUTED
LIFT / FAKE / IHARA:                            NONE
```

`R07_FULL_MARKED_BOUNDARY_CLOSURE_ERRATUM_V271_PAPER_GRADE`
