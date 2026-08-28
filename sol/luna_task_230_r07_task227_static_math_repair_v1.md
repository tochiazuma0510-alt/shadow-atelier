# Luna task 230 - task227 static mathematics repair v1

Date: 2026-08-28

Role: bounded mechanical repair after parent Sol's fail-closed static audit.
Sol owns the mathematics, acceptance, git, and GHA.  Do not run Python, Node,
GAP, git, GHA, or network.  Read Sections 1--10 in full.  Report by replacing
the provisional claims in
`sol/luna_reply_227_r07_typed_single_seed_consumer_v2.md`.

## 1. Verdict, dependency, and authorized scope

The first task227 implementation is **REJECTED BEFORE EXECUTION**.  It also
depends on the rejected first task226 ABI.  Repair in place only:

```text
search/d972_r07_typed_single_seed_endpoint_consumer_v2.py
crosscheck/check_d972_r07_typed_single_seed_endpoint_consumer_v2.py
search/d972_r07_typed_single_seed_endpoint_consumer_gha_driver_v2.g
search/certs/d972_r07_typed_single_seed_endpoint_consumer_selftest_v2_20260828.json
sol/luna_reply_227_r07_typed_single_seed_consumer_v2.md
```

Do not edit task226, task229, v216, v220, or a workflow.  The final production
parser remains dependency-blocked until repaired task226 fixes its ABI; build
the schema-independent group/action/echelon/certificate engine now and name
any exact remaining ABI dependency in the reply.

## 2. Repair the Q3/Q4 arithmetic completely

The current `qmul` concatenates the two degree-one tuples instead of adding
them, so it returns width 7/16 rather than 4/10.  Replace it by coordinatewise
degree-one addition modulo 9 followed by the central cross term.  Use the
complete canonical tables from task229:

```text
PB3: (+c123,-c123,+c123) on
      (A12,A13),(A12,A23),(A13,A23).

PB4:
[A12,A13]=+c123  [A12,A23]=-c123  [A13,A23]=+c123
[A12,A14]=+c124  [A12,A24]=-c124  [A14,A24]=+c124
[A13,A14]=+c134  [A13,A34]=-c134  [A14,A34]=+c134
[A23,A24]=+c234  [A23,A34]=-c234  [A24,A34]=+c234.
```

All coordinates, including degree one, are modulo 9.  Producer and checker
independently test width, identity, inverse, selected associativity triples,
commutators, and ninth powers.  They must remain helper-nonshared.

## 3. Repair actor cosets and marked actions

For the Heisenberg actor use `h=[x,y]=(0,0,1)`, `z0=h^3=(0,0,3)`, and

```text
R0={(0,0,0),(0,0,3),(0,0,6)}.
```

Form cosets with `(0,0,3*j)`, require 243 disjoint three-element cosets and
their 729-element union.  The current producer's `(0,0,j)` cosets are wrong.

Every occurrence action, including queue generators, is

```text
(g odot v)_o = k_o(g) v_o,
k_o(g)=p_o q_o(g) p_o^-1.
```

The current queue translates by bare `q_o(x)`/`q_o(y)` and is invalid.  Use
the conjugated `k_o` for `x`, `x^-1`, `y`, and `y^-1`.  For a canonical actor
`(a,b,r)=x^a y^b h^r`, evaluate `q_o(g)` from `q_o_x,q_o_y` and the same
normal-form order; test that this is a homomorphism on a deterministic actor
roster.

## 4. Recompute and compare the actual seed

First recompute each `w_o=sigma_o p_o xi_o`.  Then construct

```text
z0_word=(x^-1 y^-1 x y)^3,
u0_o = p_o q_o(z0) p_o^-1 w_o - w_o.
```

The first task227 code retained only the translated term and omitted `-w`.
The repaired consumer must compare its complete eleven-coordinate `u0` term
by term with repaired task226's serialized `u0` and its ancestry.  A zero
seed is valid.  Reject any mismatch before orbit closure.

## 5. Orbit basis with genuine group-algebra ancestry

Represent a coefficient in `F3[D1]` as a sparse map from actor triples to
coefficients.  Start the seed row with coefficient `1`.  If a queue row is
`lambda odot u0`, translating by `g` changes the ancestry to
`(g lambda) odot u0`; left-translate every actor key and preserve all linear
coefficients.  Echelon row operations must apply identically to row and
ancestry.

Path-name dictionaries such as `{"path:x":1}` are not coefficient ancestry
and must disappear.  For every retained basis row, directly replay its
stored `lambda` on `u0` and require equality.  Queue exhaustion under all four
marked generators is mandatory.  A 487th independent row contradicts the
v216 rank theorem and is a typed input/arithmetic failure, not a certified
nonmember.

## 6. Recover the member coefficient, not just membership

After occurrence closure, apply `C` to every retained row and build a second
echelon whose ancestry is in occurrence-basis row IDs.  Reduce the target
while tracking coefficients.  On zero remainder recover

```text
target = sum_i c_i C(row_i),
lambda = sum_i c_i lambda_i,
kappa  = lambda (z0-1) in F3[D1].
```

Retain and directly replay all three equalities:

```text
sum_i c_i row_i = lambda odot u0,
lambda odot u0  = kappa odot w,
C(kappa odot w) = bar_epsilon_1.
```

Reduce `kappa` in `F3[D1/R0]` by collecting actor coefficients with the same
`(a,b,r mod 3)` coset and require zero.  The first implementation returned
the seed's per-occurrence ancestry instead of a target solution; that is not
a member certificate.

## 7. Construct a general separating dual

When the target remainder is nonzero, solve the complete finite linear system

```text
phi(block_basis_row)=0 for every row,
phi(target)=1.
```

Use sparse Gaussian elimination or nullspace construction over F3.  Do not
restrict to a single coordinate absent from every basis row: a nonmember can
share all support coordinates with the span.  Retain `phi`, its coordinate
roster, direct annihilation of every producer block-basis row, and nonzero
target pairing.  Also test it against all 729 directly constructed
`C(g odot u0)` rows.

## 8. Independent 486/729 checker

The checker must actually construct, not merely count, the canonical 243
transversal elements `t=x^a y^b h^r` with `0<=a,b<9`, `0<=r<3`, and the 486
ideal coefficients

```text
t(z0-1),  t(z0-1)^2.
```

Act every coefficient on `w`.  Compare the resulting occurrence span with
the producer occurrence span in both directions by reducing every basis row
against the other basis.  Do the same after `C`.  Separately construct all
729 actor translates of `u0`; use them to replay a positive member equality
or a negative dual.  Ranks and supplied digests alone are insufficient.

The checker independently authenticates the task226 package, rebuilds Q3/Q4
arithmetic, `w`, `u0`, marked actions, `C`, both spans, the recovered group-
ring coefficient or dual, quotient-zero, and terminal.  It must not accept
SELFTEST by checking only advertised counters.

## 9. Production-shaped SELFTEST and real mutations

Use the immutable eleven tags, H1/H2/P combined blocks, widths 4/10, repeated
E3 slot, distinct E3/E4 C21 types, actual sign/orientation roster, nontrivial
distinct substitutions, and conjugated actions.  Construct:

1. nonzero `u0`, at least two rank increases, and a dependent queue row;
2. a nonzero member target chosen from a retained nontrivial coefficient;
3. a nonmember target sharing support coordinates with the span when the
   fixture dimension permits, with the general dual above; and
4. zero-`u0` member and nonmember edge cases.

The present `attempted==rejected` lists are prose, not mutation tests.  For
each registered mutation, make one concrete change, invoke the relevant
independent validator, and record the observed rejection reason.  Preserve
the existing roster and add separate controls for tuple-concatenation in
`qmul`, all PB triple brackets, wrong `(0,0,j)` cosets, missing `p_o`
conjugation on queue generators, missing `-w`, fake path ancestry, false
member coefficient, coordinate-only dual, unconstructed 486 rows, and
unconstructed 729 rows.  Every control is attempted exactly once.

## 10. Provenance, resource terminals, report, and v220 boundary

Adapt the production sidecar parser to the final task226 schema once task229
has stabilized it.  Do not require nonexistent receipt fields, and do not
treat a nonempty attestation byte string as authentication.  Exact canonical
sidecars must bind run/head/artifact/member bytes+SHA and independent checker
acceptance.  Resource and input stops must write the expected fresh receipt;
measure wall and RSS rather than merely listing caps.

Update driver pins only after final bytes are known.  The reply enumerates
every defect and repair, exact identities, actual mutation count, and any
remaining task226 ABI dependency.  It must state:

```text
A3 actual package:       0/1 until accepted actual task226 input
A3 orbit closure:        0/1 until complete actual queue/486 equality
A3 membership-or-dual:   0/1 until accepted actual terminal
SELFTEST infrastructure: does not increment A3
A4 and later:            untouched
```

No pointed multiplier, exact PB endpoint zero, compatible lift, fake, or
Ihara witness may be claimed.
