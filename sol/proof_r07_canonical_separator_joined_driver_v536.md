# R07 canonical separator and joined grade-two driver (v536)

Author: root Sol / 2026-09-04

Status: exact finite driver theorem joining the accepted boundaries of
v474, v530, v533--v535.  The main new point is that a separator does not
require a fresh generic linear solve: it is obtained by one target reduction
and reverse substitution through the current physical echelon.  The complete
connection list is inserted once at initialization and is never rescanned in
later separator generations.  This note does not run the actual artifacts or
decide grade two, A0, COMMON, a compatible lift, fake, or Ihara.
`verified=false`.

## 1. Physical-echelon convention

Work over `k=F3` and put `P=k^48384`.  A physical state consists of ordered
normalized rows

```text
s_0,...,s_(r-1) in P,   lead(s_i)=p_i,   s_i[p_i]=1,
```

where an offered row is reduced by the accepted rows in their insertion
order.  Consequently

```text
s_i[p_j]=0 for every j<i.                              (1.1)
```

The pivot coordinates need not be numerically increasing.  Each pivot keeps
its raw origin, prior-pivot coefficients, normalization scale, and rolling
state head.  This is the same one-way echelon convention used by v530/v534;
no reduced-row-echelon rewrite is required.

For a vector `v`, let `red_S(v)` mean reduction by `s_0,...,s_(r-1)` in this
order.  It records the coefficients and returns a remainder `u` satisfying

```text
u[p_i]=0 for all i,       v-u in span(S).              (1.2)
```

## 2. Canonical separator without a generic solve

### Lemma 2.1 (reverse-substitution separator)

Let `u=red_S(rho2)`.  If `u` is nonzero, let `f` be its least nonzero
coordinate.  Then `f` is not a pivot coordinate.  There is a canonical
functional `lambda_S` with

```text
lambda_S(S)=0,              lambda_S(rho2)=1.          (2.1)
```

It is constructed as follows.

1. Set every nonpivot coordinate of `lambda_S` to zero except
   `lambda_S[f]=u[f]^-1`.
2. For `i=r-1,...,0`, set

   ```text
   lambda_S[p_i] = - sum_(j != p_i) s_i[j] lambda_S[j].  (2.2)
   ```

If `u=0`, the recorded reduction coefficients are already a MEMBER
expression of `rho2` in `S`.

#### Proof

Equation (1.2) shows that a nonzero coordinate of `u` cannot be a pivot.
When (2.2) is evaluated for row `i`, all nonpivot values are fixed and all
later-pivot values have already been fixed.  By (1.1), no earlier-pivot
value occurs in row `s_i`.  Thus (2.2) is well-defined and makes
`<lambda_S,s_i>=0`; reverse induction proves that `lambda_S` kills all of
`S`.  Since `rho2-u` lies in `S`,

```text
<lambda_S,rho2> = <lambda_S,u>
                  = u[f]^-1 u[f] = 1.
```

If `u=0`, (1.2) directly supplies the claimed membership expression. QED.

The construction is deterministic after fixing coordinate order and pivot
insertion order.  It costs one physical reduction plus one reverse pass over
the stored pivot rows.  It neither builds a `48384 x 48384` matrix nor calls
a general nullspace solver.  Its checker independently repeats the same
reduction and reverse substitution and compares all 48,384 values in (2.1).

## 3. Insert the complete connection image only once

Let the accepted v530 physical-connection artifact contain every dependent
lower offer in the fixed P1 order, with companion

```text
c_i=g(k_i),       span{c_i}=g(ker ell).                (3.1)
```

Stream these connection rows once into an initially empty physical echelon,
retaining their complete v530 coefficient/P1 ancestry.  Physically dependent
connections need not become pivots, but their reductions remain in the
initialization transcript.  Call the resulting span `S_0`.  Then

```text
S_0 = span(Conn) <= M2.                                (3.2)
```

Every later state is obtained by inserting only accepted v534 violation
rows, so `S_n` continues to contain all of `Conn`.  Hence every separator
from Lemma 2.1 automatically kills every connection.  The connection phase
of v474 needs one authenticated initialization EOF, not a new 8,059-offer
scan for every separator generation.

This optimization does not omit a generator: the remaining part of v474
Proposition 1.1 is exactly the four actor-closed defect images tested by the
dual-orbit/scalar loop.

## 4. Exact joined state machine

The finite driver has the following states.

```text
INIT_CONN
  stream the complete v530 connection artifact into S_0;
  require its terminal EOF and ancestry joins.

TARGET_REDUCE(n)
  u_n := red_(S_n)(rho2).
  if u_n=0, return MEMBER with physical back-substitution;
  otherwise construct lambda_n by Lemma 2.1.

DUAL(n,a)
  for a in the fixed four-character order, start
      q_(a,empty)=B_a^*(lambda_n),
  and close raw representatives under the four adjoints in actor order
      (1,-1,2,-2).
  Raw word nodes and normalized DualPivots remain distinct as in v534.

SCALAR(n,a,raw_q)
  invoke the accepted v533 owner on exactly that RawDual.
  ScalarEOF advances the dual FIFO.  A dependent adjoint child does not need
  a defect scan; accepted raw representatives form a basis of the dual orbit.

VIOLATION(n,a,raw_q,o)
  invoke the v531/v534 materializer, check both nonzero pairings, and offer
  its raw physical row to S_n.  Require a genuine new physical pivot, commit
  S_(n+1), discard the incomplete certificate for lambda_n, and return to
  TARGET_REDUCE(n+1).

NONMEMBER
  allowed only after INIT_CONN EOF and four complete dual FIFO/child/scalar
  EOF transcripts for one unchanged separator generation n.
```

The dual closure need not be retained after a violation because the next
separator is different.  Safe durable boundaries are: one physical-pivot
commit, one accepted RawDual/DualPivot commit, one completed scalar terminal,
or one complete character EOF.  A stop elsewhere rolls back to the preceding
boundary and returns `UNKNOWN_RESOURCE`.

## 5. Correctness and finite termination

### Theorem 5.1 (literal MEMBER or exact NONMEMBER)

Assume the endpoint `rho2`, complete P1, Task554, Task712, v530 connection,
v533 scalar, and v531/v534 materialization inputs pass their named
independent checkers, and no resource cap interrupts the loop.  Then the
state machine in Section 4 returns exactly one of:

```text
MEMBER:    rho2 in M2, with a complete v518 literal ancestry;
NONMEMBER: rho2 notin M2, with a separator killing M2.
```

It constructs at most

```text
48384-rank(S_0)+1                                      (5.1)
```

separators.

#### Proof

By (3.2), `S_0<=M2`.  Every violation row is a row
`B_a T_(a,w)d_(a,o)` of `M2`.  V534 proves that its pairing with the current
separator is nonzero; since that separator kills `S_n`, the row is outside
`S_n` and raises physical rank exactly once.  Thus there are at most
`48384-rank(S_0)` violation generations.

At TARGET_REDUCE, a zero remainder is equivalent to `rho2 in S_n`; reverse
physical substitution followed by the v530 or v534 origin expansion is the
v518 literal MEMBER ancestry.  Otherwise Lemma 2.1 supplies a separator with
the exact normalization required by v474.  If all four dual closures end in
complete scalar EOF, v474 Theorem 2.1 kills every actor-closed defect image;
Section 3 already puts all connections inside `S_n`.  Hence the separator
kills `M2` but takes value one on `rho2`, proving NONMEMBER.  The two outcomes
are disjoint. QED.

## 6. Minimal durable receipts and implementation boundary

The implementation needs only the following new driver-owned objects.

1. `PhysicalStateHEAD`: generation, rank, ordered normalized packed rows,
   raw-origin/reduction stream, current rolling head, and the complete v530
   initialization EOF receipt.
2. `TargetReduction`: the exact rho2 parent, ordered pivot coefficients,
   packed remainder and its first nonzero free coordinate (or zero/MEMBER).
3. `Separator`: the same state generation/head, target-remainder digest,
   packed lambda, reverse-substitution transcript, and the two equalities in
   (2.1).
4. Per-character `RawDual`/`DualPivot` FIFO state and v533 scalar terminal.
5. On violation, the v534 `RawMaterialization` and `PhysicalPivot` pair;
   on terminal EOF, four complete character receipts bound to one unchanged
   separator.

The initial connection rows and all later physical pivots share one file-
backed physical-echelon owner.  Packed pivot rows may be read into one
reusable 12,096-byte buffer.  No full defect matrix, full physical generator
matrix, or generic separator matrix is part of this driver.

The implementation order is therefore:

```text
accepted physical v4 -> build S_0 once
accepted rho2 parent -> TargetReduction/Separator
accepted scalar owner + materializer -> one joined generation
repeat generations until MEMBER/NONMEMBER/UNKNOWN_RESOURCE.
```

```text
CANONICAL SEPARATOR:                 PAPER-CLOSED
PER-GENERATION CONNECTION RESCAN:   NOT REQUIRED
JOINED FINITE DRIVER:                PAPER-CLOSED
ACTUAL DRIVER IMPLEMENTATION/RUN:   OPEN
GRADE2 MEMBER/NONMEMBER:             NOT DECIDED
A0/COMMON/COFINAL/FAKE/IHARA:        NOT DECLARED
verified=false
```

`R07_CANONICAL_SEPARATOR_JOINED_DRIVER_V536_CANDIDATE`
