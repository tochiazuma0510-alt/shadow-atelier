# Task 549 independent audit — order-2016 literal MEMBER

## Verdict

The frozen 3,936-term literal payload is a direct legal preimage of the
registered order-2016 target.  This establishes the order-2016 floor as
**cross-checked MEMBER** without rebuilding the discovery closure.  The
reported closure rank, image rank, and attempt counts remain producer
telemetry.  The official checker's mutation test and complete-pin claims are
also weaker than advertised, but neither defect invalidates the independently
replayed direct preimage.

No Lean proof was supplied, so the result is not verified.

## 1. Frozen inputs and execution record

All four candidate outputs matched the task freeze before execution:

```text
bytes    sha256                                                            path
26235    6201ae0b5c1d648529ac648a574c5096b8088fe341423724556860d9d3f23fba  search/d972_r07_a0_c2fourier_joint_floor_v1.py
8539     abd8279e14b673ad1e1b197a9a29bb1ecefe5546762a81d314d50ccf89d90dd0  search/check_d972_r07_a0_c2fourier_joint_floor_v1.py
3954347  e55b7dfa5a0876054b05259f115266c0b2651431f1f2670efe85e9b34c94222b  search/certs/d972_r07_a0_c2fourier_joint_floor_v1.json
2896     70d5e6a0a4ddc2fd612c789ff2f986b14fa777b4c03657b1824e0e55a29f8de1  sol/luna_reply_542_r07_a0_c2fourier_joint_floor_v1.md
```

The direct replay used these additional machine inputs:

```text
115928   90ba603368307e16b27b2bad9d84847c7bedc501fab811b8919d96e3c8936893  scratchpad/a0_paper_words_v1.json
4709     625b4d11ca882c9419d9e0d78510bf323a117673722b8dd9ec7d7e85554267ba  scratchpad/fuda1_a0_rmax_data.g
9701     29efa11882ba76798ab0e9ca39c86476429d7066c4b203200e40d182af0c15f2  search/certs/d972_r07_a0_psl504_member_payload_lift_v2.json
10452    806c0e7015866edc917a9c07c8a3c340a6a5a29c75b751f25b91b534155936b2  sol/proof_r07_compact_extension_presentation_a0_seed_reduction_v397.md
```

The other prescribed audit inputs were unchanged:

```text
8337   5036b46264ef2486284add30b97ce44c57cf73e4186338676bfbebbd50134b2b  sol/luna_task_542_r07_a0_c2fourier_joint_floor_v1.md
9111   b18e27ac79f870a6bb5c104a12e85a95daf8644e080153305ce8447e3736f122  sol/proof_r07_a0_c2fourier_joint_lift_v439.md
21385  3114977ca62727296bf4c3980e405e920169a9c10b4bfdfa80f15990aac3a31d  sol/sol_reply_540_audit_r07_a0_c2fourier_next_rung_v1.md
11696  5cb52ffd02d2cd5c89e08080931065123a7208f7d5a2878acddb5d9ac2958fbb  sol/proof_r07_a0_relative_fibre_echelon_lift_v441.md
14931  7875fa2641355c8d6d09248b23c9fa9c766f48db751d34b90826ab609b457eb3  sol/sol_reply_544_audit_r07_a0_relative_fibre_echelon_v1.md
12520  680771157c6e0f4ec06f5f111c213c9d4ac11603268f70205df442501c6cf1b9  sol/sol_reply_543_audit_r07_a0_psl504_payload_lift_v1.md
3379   8e38008973a1f30df422aaa6a17ed0c862c48fafde112064e7d322a7720154e0  sol/luna_reply_545_r07_a0_psl504_payload_canonical_repair_v1.md
```

After the parent released the single Python slot, I ran exactly:

```powershell
python -u search/check_d972_r07_a0_c2fourier_joint_floor_v1.py
python -u "$env:TEMP\task549_independent_literal_replay.py" "C:\Users\81905\Desktop\shadow-atelier"
```

The frozen official checker exited 0 and reported runtime
`295.2751729488373 s`, 3,936 literal terms, Q0 support 511,576, the expected
Q0 digest, and zero Q1 projection.  The independent replay exited 0 and
reported runtime `15.311848878860474 s`.  Its temporary source was 21,017
bytes with SHA-256
`cf9a2dadc727ec17e60a6e2d3f9e7d2d4d8a9cbc9a04e9b3c98f6787c69bc50d`.
It imported neither repository program nor any shared helper.  It used byte
permutations, lexicographically sorted PSL states, and precomputed 264
seed-occurrence Fox rows, rather than the official checker's full-term word
rescan.

## 2. Finite marked group, transports, and target

The first nine points generate a group of order 504.  With

```text
x -> (q_x,1,0),   y -> (q_y,0,1),
```

the independently enumerated marked direct product has exactly 2,016
elements.  The three degree-9 block parities are

```text
x: (0,1,1)    y: (1,0,1),
```

so the registered `A=C2^2` basis is recovered rather than assumed.

In the six stored tag positions, the independently derived substitution
matrices (columns are the images of `x,y`) are

```text
[[1,0],[0,1]], [[1,1],[0,1]], [[0,1],[1,1]],
[[1,1],[1,0]], [[1,0],[0,1]], [[1,0],[1,1]].
```

Computing each inverse over F2 gives the following source-to-target character
labels:

```text
(0,1): (0,1),(0,1),(1,0),(1,1),(0,1),(1,1)
(1,0): (1,0),(1,1),(1,1),(0,1),(1,0),(1,0)
(1,1): (1,1),(1,0),(0,1),(1,0),(1,1),(0,1)
```

All six substituted PSL pairs generate order 504, and all matrices are
invertible.  The certified pure-A words evaluate to the four elements
`(1,a)` and attain independently enumerated shortest lengths

```text
(0,0): 0    (1,0): 9    (0,1): 9    (1,1): 10.
```

For comparison, the independent reverse-order BFS found the equally short
representatives

```text
(0,0): []
(0,1): [-2,-2,-2,-2,-2,-2,-2,-2,-2]
(1,0): [-2,-2,1,1,2,1,2,1,1]
(1,1): [-2,-2,-2,-1,-2,-1,-1,-1,-2,-1].
```

The word convention is
`(p*q)[i]=q[p[i]]`: words are evaluated left to right, positive Fox letters
are recorded at the old prefix, negative letters at the new prefix, and all
physical shifts act on the left.  For tag order
`(fxy,fxz,fyz,fux,fxy,fuy)`, the independently derived block/sign/shift
table is

```text
H1: +1, -g_yz, +g_yz
H2: -(g_uy*g_xy^-1), -g_uy, +g_uy.
```

Equivalently, the six signs are `(+,-,+,-,-,+)` and the six shifts are
`(1,g_yz,g_yz,g_uy*g_xy^-1,g_uy,g_uy)`.  All six occurrence values of the
fixed `g760` prefix, and hence all six shifts, have A-part `(0,0)`.  Thus the
fixed-prefix character scalar is 1 in this particular candidate; the signed
scalar row is `(1,2,1,2,2,1)` for each nontrivial character.  The common
source-actor scalar identity
`lambda_o(alpha_o(a))=lambda(a)` was checked for both marked basis actors and
all four characters.  Three complete word-level samples independently agreed
with the prefix-derived aggregation, fixing the left/right order
non-vacuously.

The two base words were reconstructed literally as

```text
H1(g)=f_yz(g) f_xz(g)^-1 f_xy(g)
H2(g)=f_uy(g) f_xy(g)^-1 f_ux(g)^-1.
```

Both evaluate to the identity in Q1 and Q0.  The audited target is exactly
the negative of their two PB3 normal images.  In the audit-local full-Q1
coordinate order its regular part has support 365 and SHA-256
`857d69ee766169bb1628f34d72b6ad0d4292a61092b19e472d359c72eb1b07b8`
over the compact sparse encoding `[[index,value],...]`.

## 3. Literal direct preimage

The compact roster contains 44 words, with word 44 empty, and has the
independently recomputed compact-JSON digest

```text
7612682d024b61f873928ad122c9a5d7462c812a6633112f08706cda4412b6c8.
```

Every exponent pair is integrally divisible by 18.  All 264 substituted seed
endpoints (`44*6`) are identities in Q1; the independent replay also checked
the same 264 endpoints in Q0.

The full payload has exactly 3,936 distinct `(seed,conjugator-word)` entries,
all seed indices in `1..44`, all letters in `{x^+-1,y^+-1}`, word lengths
0 through 13, and coefficients only 1 or 2:

```text
coefficient 1: 1962
coefficient 2: 1974
full literal digest:
3b902c612b2297c1144743620ac578f62d2c19e1f61cb76dfcdd18028dc2dd9e
```

The replay checked all `3936*6=23,616` coefficient-bearing conjugates as
Q1 identities and, independently, as Q0 identities.  Each is literally
`d r_i d^-1` for one of the registered legal compact relators.  Coefficient
2 is `-1` in F3 and may be realised by the inverse factor (or two copies).
Since all factors are identities in Q1, the Fox product rule is additive.
Thus the ordered product of these literal factors is a genuine legal source
element, not merely an echelon existence vector.

Its exact signed six-occurrence regular aggregate equals the full target.
The four independently Fourier-projected target/correction sectors agree;
their audit-local support/digest receipts are

```text
character  support  sha256
(0,0)      310      5109b55bda7d52b12ef61a6ecda8a9558dc4ad97ad33a1ece0cffd7f74e156cb
(0,1)      317      b4390c79dfb43ab79e8604d76544bb29b4711c61cba580d5b52e4372ea51950f
(1,0)      308      75529a020a05cca8b3c81aeda75c94339ac94f168cdac04e2fe206bfd90865f9
(1,1)      306      3d9c1f07fa98d4a24b20d681844aa9265e4f9d93817610eee5ec9526795c59cf
```

The trivial source projection is exactly the pinned Task541/v2 PSL504
payload as a `(seed,PSL-state)` source-module map; after combining it has 388
nonzero entries, consistently with the canonical repair recorded by
Task545.  The 2,247-term nontrivial list has zero trivial projection.  For
each of the three nontrivial characters, the full payload projection equals
the corresponding projection of that 2,247-term new correction.  This
separately checks that the trivial payload was not substituted for, or mixed
with, a nontrivial sector.

## 4. PB3 augmentation and normalized exponents

The independent PB3 normal calculation retained the scalar augmentation
coordinate omitted from the 6,048 regular nontrivial ambient.  The two target
augmentations and the two literal aggregate augmentations are both exactly

```text
(0,0).
```

The base `g760`, `H1(g760)`, and `H2(g760)` have exact exponent pair `(0,0)`.
Using integer division by 18 only after checking divisibility term by term,
the 3,936-term correction has normalized exponent pair

```text
(0,0).
```

Therefore no extra coordinate is merely asserted: the regular Q1 target,
both PB3 augmentation coordinates, and both normalized-exponent coordinates
all have the required values.

## 5. Q0 residual

Starting from the same literal terms in the pinned degree-36 marking, the
independent occurrence-first Fox replay reconstructed

```text
T_Q0 - A_g^Q0(z1)
support                         511576
coefficient 1                  255518
coefficient 2                  256058
sha256                          19e8f27d5c655f8043d82ebc9546b57940b4b842bf6b569da994cb7f8ec89dd9
full projection support in Q1  0.
```

The official checker independently returned the same body receipt.  This is
a materialised nonzero higher residual, not a Q0 solution or obstruction.

## 6. Checker semantics, pins, and mutations

The producer's direct-seed checks, literal replay, and Q0 lift use the correct
action order.  I found no lost ancestry in the persisted final literal list,
no aggregation-before-transport in the producer, and no hard-coded value on
which the direct preimage proof depends.

The official checker does hard-pin its producer plus the raw words, degree-36
marking, v439/Task540 theorem, v397/Task411 compact authority, and Task541/v2
payload.  It does not validate every entry of the certificate's broader
`frozen_hashes` map, nor does it recompute the roster digest, character
transport table, or residual coefficient distribution.  Those current
values were independently rebound above.

The official checker also does **not** reconstruct the 1,509-rank occurrence
closure.  Its line-71 rank/attempt assertions are fixed-field comparisons.
This is acceptable for the positive direct-preimage conclusion, but it does
not cross-check discovery ranks, queue exhaustion, or NONMEMBER capability.

Its reported `3/3 PASS` mutation suite is not an actual acceptance-path test.
The local `valid()` Boolean used for mutations is separate from `main()`;
there is no marked-group/character mutation, it checks only `A0_COMMON` among
the downstream flags, and `main()` itself does not reject arbitrary changed
downstream flags or transport-table fields.  Consequently the official
mutation receipt is not accepted as a fail-closed checker claim.

The independent replay used one common acceptance predicate and rejected:

```text
literal coefficient mutation       PASS (rejected)
character-transport datum mutation PASS (rejected)
downstream verified=true mutation  PASS (rejected)
```

All current downstream flags were also read directly and are false.

## 7. Claim boundary

1. **Finite group/transport/target:** cross-checked as stated above.
2. **Legal literal preimage/exact target:** cross-checked; this directly proves
   order-2016 MEMBER.
3. **PB3 augmentation/normalized exponents:** cross-checked at `(0,0)` and
   `(0,0)` respectively.
4. **Q0 residual/zero Q1 projection:** cross-checked with the exact receipt in
   Section 5.
5. **Mutation/frozen pins:** current data pass an independent fail-closed
   suite; the official checker's own mutation and comprehensive-pin claims
   remain defective.
6. **Rank/exhaustion:** producer telemetry only: seed rank 54, exhausted rank
   1509, action attempts 6036, row-insertion attempts 6168, physical image
   rank 1254.  No independent closure reconstruction was performed.
7. **Downstream boundary:** no order-54,432 positive grade, full-Q0, A0,
   COMMON, compatible cofinal lift, fake, or Ihara conclusion follows.  No
   NONMEMBER/completeness capability of this positive-only shortcut was
   established.

ORDER_2016_LITERAL_MEMBER_PASS_WITH_TELEMETRY_LIMIT
verified=false
