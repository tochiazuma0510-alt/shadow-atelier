# Sol(max) Task633 reply: audit of the eleven-endpoint/six-row restriction v476

## Verdict

`PASS_AFTER_REPAIR`.

The proposed mathematical resolution is correct: the actual source ledger
has eleven typed endpoint slots, while the present v437/v451 physical target
is the PB4-dropped two-hexagon projection and therefore uses precisely H
ordinals 1--6.  Restriction is coordinate selection, not an algebraic map
from five E4/P Fox rows to six E3/H Fox rows.  Grouping by the finer complete
eleven-endpoint signature preserves every six-row sum, and v476 correctly
keeps the five P endpoints without declaring their derivatives zero.

One finite repair is nevertheless required in v476 before it can be
paper-closed: repair the corrupted and mistyped occurrence-module display
(2.1), distinguishing the full group-ring ambient, the through-degree-two
truncated module, and its degree-two grade.  The final Task630 reply already
supplies the exact executable elaboration of the leaf/root and prefix gates;
those are retained implications, not additional defects in v476.

This is a local typing/serialization repair.  No new adapter, closure, or
mathematical framework is needed.  No implementation, production, GHA, git,
or full route was run.  `verified=false`.

## Exact input binding

Every requested paper/reply was read completely.  The designated portions of
the actual v12f table and recurrence were inspected directly.

| input | bytes | LF | SHA-256 |
|---|---:|---:|---|
| Task633 | 2,277 | 44 | `6eec6ecc2f570a82f1393961ab71c477bf5ceca44d5e52169e945ddcc79cae66` |
| v476 | 8,882 | 233 | `c6d788fbf246d7d858a6856c1f82c7c7a89c783a879edf2985457ee8beb6c5cd` |
| v437 | 9,007 | 265 | `4671e1f46e5489355b850e7f2c04d73d36d96d7eca1feadde199b56ae273e3d6` |
| v445 | 9,670 | 248 | `98d073c896cae8304252327ea285b876f8868b6c2d00e8ba3c00465ea86612e7` |
| v446 | 9,262 | 253 | `389ceee1250b892ec4845753af23f4455e619e2d72782931645d8b8176764756` |
| v451 | 8,050 | 229 | `3ec2d1351e16bf0fcde3abe8da346b8765b26c30796ff48e415c46ac51d933b4` |
| v470 | 8,731 | 225 | `b56aa15ee87b4831cc999525233cfadbe8e62cd25c0503c0c98fce3106fb2b7a` |
| v471 | 8,819 | 220 | `38d271514baf838953b6003f954be60c689771f0fd1c9fec14de1dfc55daf99f` |
| Task613 reply | 9,923 | 219 | `04acf864fd2fd95c13880510feb5087588f3f3970418f47ed44614f5bc74f75b` |
| actual v12f owner | 343,155 | 6,472 | `22d2ebda554cfacc78393dda7f43a9a6550e7f134dd8f44f87ab0f62241bbbbb` |
| final Task630 reply | 32,029 | 677 | `d64122daa3b6396e494d8309eb98ecadebad2062a173a80fca2ab88baacd7dd1` |

The v476 bytes and digest match Task633 exactly.  The final Task630 reply
appeared before this audit completed and was then reread from its first byte
through its final marker.

## 1. Actual eleven-context ledger: PASS

With the actual paper-product convention

```text
PP(w1,...,wk) = red(wk ... w1),
z = PP(x,y)^-1 = [-1,-2],
u = PP(y,x)^-1 = [-2,-1],
```

the v12f `raw_specs` table is exactly:

| ord | label | type | coordinate | left | right | sign |
|---:|---|---|---:|---|---|---:|
| 1 | `H1_fxy` | E3 | 0 | `[1]` | `[2]` | +1 |
| 2 | `H1_fxz` | E3 | 1 | `[1]` | `[-1,-2]` | -1 |
| 3 | `H1_fyz` | E3 | 2 | `[2]` | `[-1,-2]` | +1 |
| 4 | `H2_fux` | E3 | 3 | `[-2,-1]` | `[1]` | -1 |
| 5 | `H2_fxy` | E3 | 0 | `[1]` | `[2]` | -1 |
| 6 | `H2_fuy` | E3 | 4 | `[-2,-1]` | `[2]` | +1 |
| 7 | `P_b1` | E4 | 5 | `[4]` | `[6]` | +1 |
| 8 | `P_b2` | E4 | 6 | `[2,1]` | `[6,5]` | +1 |
| 9 | `P_b3` | E4 | 7 | `[1]` | `[4]` | +1 |
| 10 | `P_b5_inverse` | E4 | 8 | `[4,2]` | `[6]` | -1 |
| 11 | `P_b4_inverse` | E4 | 9 | `[1]` | `[5,4]` | -1 |

Thus v476's label order, quotient types, signs, and coordinate list

```text
(0,1,2,3,0,4,5,6,7,8,9)
```

are exact.  Ordinals 1 and 5 intentionally materialize the same underlying
endpoint coordinate twice, but their H1/H2 block, sign, and prefix roles are
different.  The P order is the signed factor order
`b1,b2,b3,b5^-1,b4^-1`, not natural-name order.

After the registered PB3 lift, H ordinals 1--6 are exactly Task565's ordered
six substitutions

```text
([1],[3]), ([1],[-1,-3]), ([3],[-1,-3]),
([-3,-1],[1]), ([1],[3]), ([-3,-1],[3]).
```

No `% 6`, label sort, coordinate-0 deduplication, or E3/E4 byte alias is
type-correct.

## 2. Six-row target and dimensions: PASS after R1

V437 (4.4) is explicitly the necessary projection which retains the two
hexagon gradients and normalized exponents and drops the PB4 block.  V445,
v446, and v451 carry the same six occurrence tags into the first-rung
filtered/graded computation.  They do not add five pentagon Fox rows to the
current target.

Let

\[
 G_2=I^2/I^3
 =\bigoplus_{\lambda\in\widehat A,\,\alpha\in\mathcal B_2}
   k[P]e_\lambda u^\alpha,
 \qquad \dim G_2=4\cdot6\cdot504=12{,}096.
\]

The operative degree-two occurrence and physical modules therefore have

\[
 \dim\!\left(\bigoplus_{h=1}^{6}G_2^{\oplus2}\right)
 =6\cdot2\cdot12{,}096=145{,}152,
\]

\[
 \dim(G_2^{\oplus4})
 =2\text{ hexagons}\cdot2\text{ components}\cdot12{,}096
 =48{,}384.
\]

The complete physical lower/auxiliary width is independently

```text
degree 0:  4*4*504       =  8,064
degree 1:  4*4*3*504     = 24,192
auxiliary:                           4
total:                         32,260.
```

The top packing is consequently exactly `48,384/4 = 12,096` bytes under the
registered four-trits-per-byte format.  These agree with v451 and Task630.

### R1: repair display (2.1), both serialization and type

V476 byte offset 2,471 is the forbidden control byte `0x08`; the source is
effectively `0x08igoplus`, not `\bigoplus`.  Merely replacing that byte by a
backslash would leave the display ambiguous: literal
`direct-sum_h k[Q_2]^2` is the full group-ring occurrence ambient and has
dimension

```text
6*2*|Q2| = 6*2*54,432 = 653,184,
```

not the stored current degree-two source width 145,152.  The through-degree-
two truncated occurrence source has width

```text
24,192 + 72,576 + 145,152 = 241,920
```

before its eight source auxiliaries.

Replace (2.1) by the explicit typed chain

\[
 \mathcal O_{H,\le2}
 =\bigoplus_{h\in H_6}
   \left(k[Q_1]\otimes T_{\le2}\right)^{\oplus2},
 \qquad
 \operatorname{gr}_2\mathcal O_{H,\le2}
 =\bigoplus_{h\in H_6}G_2^{\oplus2}.
\]

If the author wishes also to mention the natural full Fox ambient
`direct-sum_h k[Q2]^2`, it must be displayed separately together with the
registered truncation/grade projection into the two modules above.  It may
not be called the operative v445/v446/v451 stored source.  This single
replacement also removes the control byte.

## 3. Eleven-to-six operation: PASS

The map used in Theorem 3.1 is

\[
 \pi_H:E3^6\times E4^5\longrightarrow E3^6,
 \qquad(g_1,\ldots,g_{11})\mapsto(g_1,\ldots,g_6).
\]

This is a restriction of a heterogeneous endpoint tuple.  It is not a
homomorphism on occurrence Fox modules and requires no map (E4\to E3).
After this restriction, only the six H seed derivatives, signs, and prefixes
enter the v451 physical map.  Therefore the typing is exact once R1 names the
graded codomain correctly.

A concrete forbidden countermodel is supplied by two paths with equal six H
endpoints but different P endpoints.  They have the same current H action
but can have different P Fox rows.  Any proposed `11 -> 6` algebraic adapter
which aliases the P slots would identify data that the full all-seven
interpreter distinguishes.  Coordinate restriction does not.

## 4. Finer signature grouping: PASS

For fixed seed (s), the exact leaf formula is

\[
 D_h(C_1)=\sum_P\mu_{s,P}E_h(P)D_h(r_s),
 \qquad E_h(P)=\eta_h\theta_h(P).
\]

The fibres of the complete signature

\[
 \Sigma_{11}(P)=(E_1(P),\ldots,E_{11}(P))
\]

refine the fibres of its first-six restriction.  Summing over the finer
fibres and then forgetting coordinates 7--11 is just a partition of the same
finite sum.  It neither loses nor duplicates a coefficient.  This remains
true when two paths have the same H signature and unequal P signatures: the
two finer buckets receive the same H multiplier and their coefficients add
in the final H row.  A bounded two-bucket coefficient `1+2=0 mod 3` probe
confirmed the same cancellation before and after restriction.

The grouping remains per seed.  Endpoint equality never identifies
different relators, source words, DAG edges, or refinement endpoints.

## 5. P endpoints and projection boundary: PASS

V476 explicitly retains P ordinals 7--11 in every endpoint gate,
path-to-signature assignment, and reusable signature receipt.  It excludes
their Fox rows only because the registered target map drops PB4.  It does
not state that their derivatives or their changes are zero.  A future
P-retaining/B4 target must supply its own typed physical module and cannot
reinterpret the 48,384-trit H residual as a full all-seven residual.

Accordingly, success in all six projected first-rung grades remains only the
registered necessary branch.  It is not full A0 and does not discharge PB4
or compatibility.

## 6. Exact leaf/root interface: PASS

The source-level identity is ordered and noncommutative:

```text
C_T  = OrderedProduct(the 3,317 selected GradeNodeRef powers)
C_<1 = RegisteredPriorProduct(prepare.canonical_solution.terms in stored order)
C_1  = Compose(C_<1,C_T), meaning prior followed by update.
```

At endpoint one, Fox evaluation of this ordered product is additive, but that
does not commute or identify the source words.

The final Task630 reply supplies the required executable disambiguation of
v476's combined mathematical notation:

1. independently traverse the 3,317 selected roots to obtain
   `mu_T(s,P)` and byte-compare precisely that map with `R07LEAF1`;
2. separately traverse the stored prior terms, without sorting, to obtain
   `mu_<1(s,P)`; and
3. authenticate the three root objects and all eleven endpoint-one gates
   before forming the evaluation-only sum
   `mu_1 = mu_<1 + mu_T (mod 3)`.

Only `mu_1` is used in Theorem 3.1 for `C_1`; it must not be compared with the
`C_T`-only binary stream.  The canonical `Compose` source root remains
authoritative after this evaluation-level addition.  V476 says that the
source graph *and prior root* supply the complete map and separately requires
all three roots; it neither says that the Task625 leaf stream contains the
prior root nor contradicts the Task630 split.  Therefore no further v476
repair is needed here.

## 7. Prefix, sign, and parent contract: PASS

The v12f reverse-block construction confirms the exact occurrence prefixes.
For signed base factors (q_j=\eta_j(\theta_j(g)^{\epsilon_j})), they are

```text
H1: q3 q2 q1 = 1;       U1=1,       U2=q3,       U3=q3
H2: q6 q5 q4 = 1;       U4=q6 q5,   U5=q6,       U6=q6
P:  q11 q10 q9 q8 q7=1; U7=1, U8=q11 q10 q9 q8,
                         U9=q11 q10 q9, U10=q11, U11=1.
```

The path signature itself is unsigned:

\[
 E_j(P)=\eta_j\theta_j(P),
\]

and one leaf occurrence is

\[
 \epsilon_j L_{U_j}L_{E_j(P)}D_{\eta_j\theta_j}(r_s).
\]

Thus the actor endpoint acts first on the seed row, the fixed prefix acts
second, and the occurrence sign is applied exactly once.  In the prefix trie,
an appended source letter is right multiplication,

\[
 E_j(P\ell)=E_j(P)\,\eta_j\theta_j(\ell),
\]

so no source word is reversed.

The final Task630 reply, read as the requested companion input at exact
SHA-256
`d64122daa3b6396e494d8309eb98ecadebad2062a173a80fca2ab88baacd7dd1`
supplies the following executable gates behind v476's concise instruction to
seal the actual prefixes:

- reconstruct every (U_j), block identity, PP reversal, PB3 lift, and typed
  E3/E4 endpoint from the pinned v12f table;
- keep sign and prefix out of the endpoint-signature key and apply them in
  the order above; and
- for every nonzero exact complete-root `(s,P)` key, compare the eleven-row
  occurrence result entrywise with the direct H1/H2/pentagon Fox difference
  for `g P r_s P^-1`.

The direct all-seven canary authenticates inversion, word orientation, and
prefix placement.  Its P calculation is an authentication receipt; it still
does not inject P rows into the projected H target.  Producer and checker
must construct this arithmetic independently.  A resource stop before the
comparison is `UNKNOWN_RESOURCE`, never an empty row or negative result.
V476 requires separately pinned or independently constructed tables and does
not conflict with any of these gates, so duplicating the complete Task630
checklist in v476 is not a load-bearing repair.

## 8. Task565 binding and remaining actual inputs

Task565's six substitution/affine tables still require a concrete entrywise
receipt.  V476 correctly requires, rather than assumes, equality with
ordinals 1--6.  The future gate must compare at least:

```text
ordered post-lift substitution pairs;
E3 marked generator images and quotient type;
six kernel matrices and generally nonzero crossed cochains;
signs (1,2,1,2,2,1) in F3;
destination blocks (H1,H1,H1,H2,H2,H2);
prefix shifts (1,g_yz,g_yz,g_uy*g_xy^-1,g_uy,g_uy);
PB3 normal/boundary map and filtration commutation.
```

This is a six-to-six identity test.  It is not supplied by matching counts or
labels, and the current Task565 candidate is not itself an accepted result.

After R1, the mathematical contract is complete, but these actual values
remain external and must keep a consumer inert until available:

- a finally accepted successful Task625 producer/checker quartet, immutable
  run/artifact/manifest and all fifteen payload receipts;
- its result-dependent graph, reached-seed, exact-leaf, `L/U/G`, scheduler,
  and root digests;
- the accepted Task565/v451 table and PB4-drop/filtration receipts, with an
  independently implemented consumer checker;
- the exact through-degree-two target and all parent hashes; and
- the dense 32,260-coordinate zero comparison and freshly recomputed
  48,384-trit/12,096-byte residual receipts.

Task595/Task625 grade-one membership does not supply any of the last target
or residual data.  The fresh residual is only an input to the later v474
grade-two decision.

## Bounded adversarial probes

Only symbolic/in-memory checks were made:

```text
actual H pairs == Task565/floor.OO             PASS
coordinates                                     (0,1,2,3,0,4,5,6,7,8,9)
signs                                           (+,-,+,-,-,+,+,+,+,-,-)
P signed-factor order                          b1,b2,b3,b5^-1,b4^-1
degree-two source / physical widths            145,152 / 48,384
physical lower/auxiliary width                 32,260
full k[Q2]^2 six-row ambient                   653,184
through-degree-two occurrence source           241,920
same-H/different-P finer-bucket cancellation   preserved
v476 forbidden control bytes                   one: 0x08 at offset 2,471
```

These probes are sufficient to expose R1 and to test the proposed restriction
on a path pair which a full signature separates.  They are not production
evaluation or evidence that the missing result-dependent parents exist.

## Claim boundary and handoff

```text
ACTUAL ELEVEN ENDPOINT TABLE:                 PASS
ORDINALS 1--6 == TASK565 H TABLE:             PASS ON STATIC TABLE; ACTUAL RECEIPT REQUIRED
11-ENDPOINT -> 6-ROW OPERATION:               TYPED COORDINATE RESTRICTION
FINER SIGNATURE PRESERVES H SUM:              PASS
P FOX CONTRIBUTION ZERO:                     NOT ASSERTED
32,260 LOWER / 48,384 TOP DIMENSIONS:         PASS AFTER R1 NOTATION REPAIR
COMPLETE ROOT / TASK625 LEAF INTERFACE:       PASS (TASK630 ELABORATION RETAINED)
PREFIX / SIGN / WORD ORDER:                   PASS (TASK630 CANARY RETAINED)
TASK625 SUCCESS PAYLOAD / FRESH RHO2:         NOT PRESENT
GRADE TWO / COMPLETE FIRST RUNG:              NOT DECIDED
FULL PB4 / A0 / COMMON / COFINAL LIFT:        NOT DECIDED
FAKE / IHARA:                                 NOT DECLARED
verified:                                     false
OVERALL:                                      PASS_AFTER_REPAIR
```

Executable work may begin only from a repaired, re-audited successor and must
remain non-runnable against guessed Task625 values.  No production launch is
authorized by this paper verdict.

`R07_ELEVEN_ENDPOINT_SIX_ROW_V476_PASS_AFTER_REPAIR`
