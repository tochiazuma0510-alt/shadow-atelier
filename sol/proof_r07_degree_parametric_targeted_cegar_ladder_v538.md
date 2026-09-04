# R07 degree-parametric targeted CEGAR ladder v538

Author: root Sol / 2026-09-04

Status: conditional paper theorem extending the finite logic of v474/v535/v536
from grade two to every remaining grade of the first `C3^3` rung.  It proves
that no new search architecture or old-orbit restart is needed after a MEMBER;
it does not force any residual to be a MEMBER and does not run an artifact.
`verified=false`.

## 1. Grade-dependent spaces and fixed parents

Let

```text
(h_0,h_1,...,h_6) = (1,3,6,7,6,3,1),
H_d = h_0+...+h_d.
```

For a grade `d` with `1 <= d <= 6`, put

```text
V_(a,d) = k^(6048 h_d)       (one source-character pure grade),
P_d     = k^(8064 h_d)       (joint physical top grade),
L_d     = k^(8064 H_(d-1)+4) (all lower and auxiliary coordinates),
```

over `k=F3`.  Thus for the currently pending and later grades the exact
dimensions are

| `d` | `dim V_(a,d)` | `dim P_d` | `dim L_d` |
|---:|---:|---:|---:|
| 2 | 36,288 | 48,384 | 32,260 |
| 3 | 42,336 | 56,448 | 80,644 |
| 4 | 36,288 | 48,384 | 137,092 |
| 5 | 18,144 | 24,192 | 185,476 |
| 6 | 6,048 | 8,064 | 209,668 |

These are coordinate dimensions, not ranks or memory predictions.

Assume that precision `d-1` has two separately authenticated parents:

1. a complete target-independent transition presentation `P_(d-1)` in the
   sense of v444/v449, with ordered basis, all 44 seed reductions, all four
   actor transitions and literal ancestry; and
2. an accepted literal root `C_(d-1)` solving through grade `d-1`, whose
   independent one-higher evaluation gives the actual residual
   `rho_d in P_d` and zero in `L_d` as in v479.

Neither parent may be reconstructed from the other.  In particular, the
selected ancestry of one earlier MEMBER is not a complete transition
presentation.

## 2. Uniform typed image formula

Re-evaluate the ordered basis of `P_(d-1)` one precision higher.  If its
offers are indexed by a finite set `E_d`, their lower/top components define

```text
ell_d : k^(E_d) -> L_d,
g_d   : k^(E_d) -> P_d.
```

Run lower-first elimination once.  For every dependent offer retain the
canonical kernel vector `k_i in ker ell_d`, its prior reductions and scales,
and define the ordered connection list

```text
Conn_d = (g_d(k_i))_i.
```

The usual unused-offer-coordinate argument gives

```text
span(Conn_d) = g_d(ker ell_d).                         (2.1)
```

V444/v449 form the pure grade transition defects from the 44 lifted seed
relations and four lifted transitions of each old basis row.  Project each
complete zero-lower defect into the four fixed character blocks.  For each
character `a`, let `D_(a,d)` be this finite ordered defect roster, let

```text
T_(a,t,d) : V_(a,d) -> V_(a,d),  t=(1,-1,2,-2),
B_(a,d)   : V_(a,d) -> P_d
```

be the exact associated-grade actor and physical maps, and put

```text
H_(a,d) = span{T_(a,w,d) q : q in D_(a,d), actor words w}.
```

The formulas of v443 construct these maps from the same 27-monomial
truncated algebra; changing `d` changes only the homogeneous monomial roster
and the target offsets.  It does not license reuse of grade-two table bytes.

### Proposition 2.1 (degree-parametric image decomposition)

The complete legal grade-`d` physical correction image is

```text
M_d = span(Conn_d) + sum_a B_(a,d)(H_(a,d)) <= P_d.    (2.2)
```

#### Proof

V444/v449 say that the complete precision-`d` occurrence image is the direct
sum of the lifted old presentation and the actor closure of precisely the
seed/transition defects above.  V441 applies physical aggregation only after
that source closure.  Lower-first elimination of the lifted-old part exposes
exactly `g_d(ker ell_d)` by (2.1), while a pure-grade defect has zero lower
coordinates and contributes exactly through `B_(a,d)`.  Every legal row is
in one of these two families, and every displayed family is legal.  This
proves (2.2).  QED.

## 3. The same targeted decision at every grade

Initialize a one-way physical echelon `S_(d,0)` by streaming `Conn_d` once.
At generation `n`, reduce `rho_d` by the current echelon.

- A zero remainder is a MEMBER transcript immediately.
- For a nonzero remainder, v536 Lemma 2.1 constructs the canonical separator
  `lambda` by choosing its least nonzero free coordinate and reverse-solving
  the physical pivots.  Thus no generic nullspace solve is needed at any
  grade.

For each character start at `B_(a,d)^* lambda`, close under the four exact
adjoints, and pair every accepted raw representative with the whole ordered
roster `D_(a,d)`.  A nonzero pairing names the explicit primal row

```text
B_(a,d) T_(a,w,d) q,
```

whose stored actor tuple is replayed in the primal order fixed by v518.  Add
that row to `S`, abandon the old separator, and repeat.  Only four exhausted
dual-orbit/defect scans for one unchanged separator may return NONMEMBER.

### Theorem 3.1 (finite grade-d terminal)

Under independent authentication of both parents, all forward/adjoint maps,
connection rows, separators, scalar pairings, materialized rows and physical
pivots, and absent a resource stop, this state machine returns exactly one of

```text
MEMBER:    rho_d in M_d, with complete literal ancestry;
NONMEMBER: rho_d notin M_d, with a separator killing M_d.
```

It constructs at most

```text
dim(P_d) - rank(S_(d,0)) + 1                           (3.1)
```

separators.

#### Proof

The v536 strict-rise proof is dimension-free.  Every violation row belongs
to (2.2) and pairs nontrivially with a functional killing the current span,
so it is a new pivot.  This can happen at most the codimension in (3.1).
A zero target remainder gives membership.  At exhausted EOF, the dual-orbit
criterion kills the second summand of (2.2), while initialization already
contains the first; normalization on `rho_d` proves nonmembership.  QED.

The safe durable objects are likewise degree-independent: connection EOF,
one physical pivot, one raw-dual/DualPivot insertion, one complete scalar
terminal, and one character EOF.  A cap elsewhere is `UNKNOWN_RESOURCE`, not
a terminal.

## 4. MEMBER handoff without a primal restart

On MEMBER, reverse physical substitution expands every selected pivot either
through its lower-dependent lifted-old ancestry or through its named
defect/actor ancestry.  Replace every coefficient two by literal inverse and
retain the fixed noncommutative product order.  The same proof as v518 gives
an ordered literal update `Delta C_d` with zero lower/auxiliary value and top
value `rho_d`.  Direct evaluation then defines

```text
C_d = Compose(C_(d-1), Delta C_d).                     (4.1)
```

Two tasks may now run concurrently:

1. evaluate (4.1) one precision higher to obtain the fresh `rho_(d+1)`; and
2. complete and persist the target-independent transition presentation
   `P_d` using v444's lifted basis plus exhausted transition-defect basis.

The first uses only selected word ancestry; the second must retain every seed
and actor transition.  When both finish, they are exactly the two parents of
Section 1 for grade `d+1`.  No historical actor word is rediscovered, because
v444 transports the old presentation and closes only its new defects.

### Corollary 4.1 (remaining first-rung ladder)

Once the grade-one word and complete transition-presentation parents pass
their named acceptance gates, an accepted grade-two MEMBER followed by
accepted MEMBER terminals at grades three, four, five and six produces one
literal `C_6` whose residual lies in `I^7=0`.  Hence it solves the registered
target exactly at the order-54,432 first-rung quotient.  The present complete
P1 cache is still a candidate parent until its required independent joins;
this corollary does not promote it by prose.

This is five actual finite membership decisions, not a theorem that one
successful grade automatically makes the next four successful.  NONMEMBER at
any grade stops this witness branch; a resource stop remains UNKNOWN.

## 5. Reusable implementation ABI and exact boundary

A degree-parametric implementation may share code for:

1. monomial enumeration and the v443 truncated-ring operators;
2. lower-first connection construction;
3. the v536 target reduction and reverse separator;
4. raw-dual versus normalized-DualPivot state;
5. scalar scanning and on-demand primal materialization; and
6. literal reverse substitution and the two-parent successor handoff.

It must version and authenticate separately for each grade: dimensions,
monomial order, old presentation, defect roster, sparse map tables, target
root/residual, pivot stores and EOFs.  A grade-two byte artifact cannot be
relabeled as a later-grade artifact merely because grades two and four have
equal ambient widths.

The first-rung conclusion still does not finish the nonsplit
order-54,432-to-1,469,664 rung.  That rung uses v443's carry formulas and its
own six actual membership tests.  Nor does this theorem establish the
physical-kernel cover/jet-saturation needed by v504/v537.

```text
GRADE-PARAMETRIC IMAGE/DUAL/CEGAR THEOREM:  PAPER-CLOSED, CONDITIONAL
GENERIC REVERSE SEPARATOR AT GRADES 2--6:   PAPER-CLOSED
OLD PRIMAL ORBIT RESTART AFTER MEMBER:      NOT REQUIRED
GRADE 2 ACTUAL TERMINAL:                    OPEN J1--J4
GRADES 3--6 ACTUAL TERMINALS:               OPEN
ORDER 54,432 FIRST-RUNG MEMBER:             OPEN
SECOND RUNG / FULL A0 / COMMON:             OPEN
COFINAL LIFT / FAKE / IHARA:                NOT DECLARED
verified=false
```

`R07_DEGREE_PARAMETRIC_TARGETED_CEGAR_LADDER_V538_CANDIDATE`
