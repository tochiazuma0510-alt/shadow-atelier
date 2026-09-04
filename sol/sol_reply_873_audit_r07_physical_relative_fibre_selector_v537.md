# Task 873 Sol(max) hostile audit — physical relative-fibre selector v537

## Ruling

`PASS_WITH_EXPLICIT_NARROW_REPAIRS`.

The physical one-edge theorem, the fixed-word target construction, and the
recursive selector are mathematically sound.  V537 is a legitimate direct
physical alternative to v526; it never proves, and does not need to pretend to
prove, v526's unaggregated kernel equality.  There is one narrow type bridge to
make explicit before citing Section 6 as v504 (6.1): identify the inverse-limit
owner `X` with v504's completed source `P`, or exhibit the compatible quotient
map from the redundant `X` presentation to `P`, and identify the finite maps
`B_n` with the quotients of v504's `B_(n,w0)`.  As written, the last step changes
from v537's `B(X)` to v504's `B(P)` only by prose.

This is a conditional paper ruling only.  No actual A4 cover, A0 member, lift,
fake, Ihara statement, `cross_checked` promotion, or verification is obtained.

## 1. Exact one-edge criterion

All maps in Theorem 2.1 are correctly typed:

```text
X' --B'--> L'
 |rX       |rL
 v         v
X  --B-->  L,

rL B' = B rX,     rX surjective.
```

Commutativity gives `B'(ker rX) <= ker rL`.  If equality holds, take any
compatible targets `z' in L'`, `z=rL(z')`, and any coarse solution `x` with
`Bx=z`.  Surjectivity of `rX` gives `s in X'` with `rX(s)=x`, and

```text
d := z' - B's  in ker rL.
```

The kernel equality gives `c in ker rX` with `B'c=d`; hence `s+c` is a fine
solution reducing to `x`.  Conversely, for arbitrary `d in ker rL`, use the
compatible target pair `(z',z)=(d,0)`.  The coarse zero fibre is nonempty, so
surjectivity of that fibre reduction gives `c in ker rX` with `B'c=d`.
Together with the automatic inclusion this proves equality.

No surjectivity of `rL` is needed.  Empty coarse fibres make the corresponding
surjectivity assertion vacuous, while the converse deliberately uses the
nonempty zero fibre.  No fine fibre is assumed nonempty.  V537 also correctly
states that for one prescribed target/coarse solution only the resulting
defect membership in `B'(ker rX)` is necessary and sufficient; full kernel
coverage is the uniform all-fibre gate.

## 2. The fixed-word target family

Defining

```text
z_n := Phi_n(w0)
```

from one fixed literal word does construct a compatible target family if the
stated structural naturality holds.  Reducing that same word, its prefix DAG,
all eleven typed occurrence maps, normalized coordinates, and the outer
physical evaluator gives

```text
rL_n Phi_(n+1)(w0) = Phi_n(w0).
```

This implication uses no coarse MEMBER.  The coarse MEMBER supplies only an
`x_0` with `B_0 x_0=z_0`; it neither chooses nor reconstructs any `z_(n+1)`.
V537 correctly leaves the generator-level evaluator/reduction replay as an
actual open receipt rather than treating endpoint equality as naturality.

## 3. Relation to v526 and the bridge to v504

The two routes have different target kernels:

- v526 covers the kernel of reduction in its eleven-slot unaggregated target
  and subsequently needs an aggregation/evaluation bridge;
- v537 asks directly for the kernel of reduction in the complete physical
  target `L_n` and lifts the physical fibre itself.

Thus physical equality does not imply v526's unaggregated equality, but it is
a valid alternative when `X_n` is the one common v504 legal instruction owner
and `L_n` is the complete physical owner, not a selected window.  Since the
desired conclusion is already physical, no inverse to aggregation and no
post-aggregation reconstruction is used.

One displayed owner bridge is still required.  In the redundant-presentation
form, let `q_n:X_n -> P_n` impose exactly v504's pre-registered linear source
relations and require

```text
q_n rX_n = rP_n q_(n+1),
B_n = B_(n,w0)^504 q_n,
Phi_n(w0) = the n-th quotient of Phi^504(w0).
```

The induced `q:lim X_n -> P` must be the v504 completed-source identification
(or simply declare `P=lim X_n` when the redundant presentation is retained).
Then the recursively constructed `x=(x_n)` gives

```text
p=q(x) in P,     B_(w0)^504 p = Phi^504(w0),
```

which is exactly v504 (6.1).  This is the smallest repair: replace the bare
phrase `Phi(w0) in B(X)` in v537 Section 6 by this typed factorization into
`Phi(w0) in B(P)`.  It does not reinstate v526's unaggregated bridge.

Even after that repair, the actual premises openly left pending by v537 remain
load-bearing: a complete coarse A0 literal member, actual all-edge physical
kernel columns and source sections, the fixed-word naturality receipt, and all
independent hypotheses of v504.

## 4. Selector and inverse-limit materialization

For a fixed basis `(b_j)` of `ker rL` and selected columns

```text
C_j in ker rX,     B'C_j=b_j,
```

the map `h(sum d_j b_j)=sum d_j C_j` satisfies `rX h=0` and
`B'h=id_(ker rL)`.  Consequently

```text
sigma(x) + h(z' - B'sigma(x))
```

has the advertised image and reduction.  This linear formula itself is not a
literal-word theorem.  V537 does not conflate the two: its Section 5 separately
requires a word/DAG-bearing section and columns, fixed product order, literal
inverse for coefficient `2`, and structural reduction of the fine materialized
word to the prescribed coarse word.

With those receipts at each ladder edge, the recursive word at level `n+1`
reduces to the already chosen word at level `n`; hence the limit has one common
word ancestry.  All eleven values are evaluations of that one owner record.
There is no occurrencewise gluing.  Nor is fine-fibre nonemptiness assumed:
Theorem 2.1 constructs a fine point from the coarse point.  A failed/capped
column search remains `UNKNOWN`, as v537 states.

## 5. Exact grade-two boundary and indispensable v518 replay

The repaired grade distinction is correct.  Even after acceptance, v535 plus
v518 supplies only the grade-two truncated instance of (4.1).  V504 requires
the complete first-rung path-bearing A0 membership through grades three to six
(or one accepted full-A0 transcript).  The packed 48,384-coordinate equality
alone is not the needed literal premise.

The indispensable v518 replay is its full Theorem 5.1 chain, not merely its
final physical row:

1. authenticate the Task554 parents and all 8,059 canonical P1 instruction
   and cache records, including distinct precision-one/degree-two rows,
   origins, ordered reductions, scales, bytes, and EOF;
2. replay the fixed projector order
   `((0,0),(0,1),(1,0),(1,1))` and the forward literal recurrences (1.3) and
   (2.2), with coefficient `2` materialized as inverse;
3. replay the nonreversed actor nesting (3.2), including a noncommuting
   two-letter check;
4. replay the connection, orbit, pivot-reduction, and back-substitution
   formulas (4.1)--(4.4) with exactly the same ordered coefficients and scales;
5. independently evaluate one and the same ordered `Delta C_2` word in all
   eleven typed slots and then perform the printed PB/hexagon/A.18 aggregation,
   obtaining zero lower/auxiliary value and top value `rho2`; and
6. replay both normalized-exponent coordinates and every required side and
   localization gate.

The six source tags in the P1 cache are not the eleven physical occurrences.
The latter require the separate same-word evaluations above.  This replay
establishes only the stated grade-two literal premise and not
`PHYSICAL-JET-SATURATION` or the missing grades.

## 6. What A4 v10 actually targets

The advertised v10 object is
`d972-r07-word-independent-successor-kernel/.../physical-bridge-seed-v1`.
Its report describes a typed sealed origin seed, origin/base/local/terminal
history bodies, a local shard, and independently built fixture
`K/kernel/closure` objects.  Its bounded positive test exercises reader,
authority, resource, comparison, and scale-two plumbing.  It does not exhibit:

- the complete v537 spaces `X',X,L',L` and both reductions;
- a basis of `ker rL` in the complete physical target;
- surjectivity of `rX` and the commuting physical square; or
- one literal source-kernel column over every such target-kernel basis row.

Moreover, `resource_K_construction=0`, the production archive was not opened,
the GAP driver was not run, and the reported frontier is only `A4=1/3 THROUGH
ROW26`.  Therefore the prepared computation targets a differently typed
successor-kernel/physical-bridge-seed object.  Without an explicit typed map
and the equations above, it is not evidence even for a definite subset of
v537's physical kernel cover.  It may later feed that receipt, but the actual
cover remains open.

## 7. Honest v220 mapping and status

The safe v220 implication is exactly:

```text
complete first-rung literal A0 member in the exact v504 owner
+ fixed-word structural target naturality
+ surjective source reductions and commuting physical squares
+ all-edge complete physical relative-kernel basis covers
+ word-bearing sections/columns and the explicit X-to-P bridge above
    => Phi(w0) in B(P).

Phi(w0) in B(P)
+ v504 compactness/strictness/separation
+ actual PHYSICAL-JET-SATURATION
+ side, Cauchy, and continuity gates
    => the conditional v504 Newton conclusion.
```

Nothing currently authorizes replacing the first line by the grade-two
member, replacing the physical cover by A4 v10, or promoting the final
conclusion.

```text
FIXED-WORD PHYSICAL TARGET FAMILY:            PAPER-CLOSED, CONDITIONAL
PHYSICAL KERNEL COVER <=> ALL-FIBRE LIFTING:  PAPER-CLOSED
EXPLICIT ONE-EDGE SELECTOR:                   PAPER-CLOSED, CONDITIONAL
X-TO-v504-P / B_(w0) TYPED BRIDGE:            NARROW PAPER REPAIR REQUIRED
ACTUAL A4 PHYSICAL BASIS COVER:               OPEN
ACTUAL FIXED-WORD REDUCTION RECEIPT:          OPEN
ACTUAL COMPLETE FIRST-RUNG A0 MEMBER:         OPEN
ACTUAL PHYSICAL-JET-SATURATION:               OPEN
COMPATIBLE R07 LIFT / FAKE / IHARA:           NOT DECLARED
cross_checked=false
verified=false
```

VERDICT=PASS_WITH_EXPLICIT_NARROW_REPAIRS
verified=false
