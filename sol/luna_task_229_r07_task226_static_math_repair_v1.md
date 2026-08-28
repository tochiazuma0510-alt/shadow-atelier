# Luna task 229 - task226 static mathematics repair v1

Date: 2026-08-28

Role: bounded mechanical repair after parent Sol's fail-closed static audit.
Sol owns the mathematics, acceptance, git, and GHA.  Do not run Python, Node,
GAP, git, GHA, or network.  Read this file from Section 1 through Section 9
before editing.  Report by replacing the provisional claims in
`sol/luna_reply_226_r07_actual_two_word_endpoint_specializer_v2.md` with an
honest repair report and an explicit statement that the repaired code remains
unexecuted.

## 1. Verdict and authorized scope

The first task226 implementation is **REJECTED BEFORE EXECUTION**.  None of
its producer/checker flags, recorded mutation lists, or advertised group
facts may be treated as evidence.  Repair in place only these five files:

```text
search/d972_r07_actual_two_word_endpoint_specializer_v2.py
crosscheck/check_d972_r07_actual_two_word_endpoint_specializer_v2.py
search/d972_r07_actual_two_word_endpoint_specializer_gha_driver_v2.g
search/certs/d972_r07_actual_two_word_endpoint_specializer_selftest_v2_20260828.json
sol/luna_reply_226_r07_actual_two_word_endpoint_specializer_v2.md
```

Do not edit v225, v220, any predecessor, task227, or a workflow.  The `.py`,
`.g`, and JSON files remain ASCII-only.

## 2. Canonical class-two arithmetic

Repair producer and checker independently; the checker must not import or
copy helper code from the producer.

For a key `(a,z)` every degree-one and central coordinate is reduced modulo
9 after multiplication.  Inversion must use a mutable temporary or a direct
tuple constructor; the current tuple assignment is invalid.  Seal and test

```text
(a,z)(b,w)=(a+b,z+w-sum_{i<j} a_j b_i B_ij),
(a,z)^-1=(-a,-z-sum_{i<j} a_i a_j B_ij)
```

with all coordinates modulo 9.

Use lexicographic degree-one orders

```text
PB3: A12,A13,A23
PB4: A12,A13,A14,A23,A24,A34
```

and central orders `c123` and `c123,c124,c134,c234`.  The complete nonzero
PB4 upper-triangular bracket table is exactly:

```text
[A12,A13]=+c123  [A12,A23]=-c123  [A13,A23]=+c123
[A12,A14]=+c124  [A12,A24]=-c124  [A14,A24]=+c124
[A13,A14]=+c134  [A13,A34]=-c134  [A14,A34]=+c134
[A23,A24]=+c234  [A23,A34]=-c234  [A24,A34]=+c234
```

All other brackets of distinct degree-one generators are zero and the lower
triangle is determined by skew-symmetry.  PB3 is the first line only, hence
its signs in order `(A12,A13),(A12,A23),(A13,A23)` are `+,-,+`.

In SELFTEST check identity, inverse, selected associativity triples, generator
commutators, ninth powers, coordinate width, and word evaluation.  A boolean
written into a receipt without recomputation is not a test.

## 3. Actor and the correct 243 cosets

Retain the three-coordinate Heisenberg actor and exhaust all 729 elements.
With `h=[x,y]=(0,0,1)` in the frozen convention, use

```text
z0=h^3=(0,0,3),   R0=<z0>={(0,0,0),(0,0,3),(0,0,6)}.
```

The 243 transversals may use central coordinate `0,1,2`, but each coset must
be formed with the powers `(0,0,3*j)`, not `(0,0,j)`.  Require 243 disjoint
three-element cosets whose union is all 729 actors.

## 4. No synthetic production ledger or substitutions

Delete the unconditional use of `toy_records()` and `occurrence_maps()` in
the specialization path.  SELFTEST may use a toy word pair, but it must use
the same following literal A.18 constructors and immutable eleven-row ledger
as production.

The exact task198 ledger has one-based prefix ordinals

```text
[3,2], [3], [], [6,5], [6], [],
[11,10,9,8], [11,10,9], [11,10], [11], []
```

with blocks

```text
H1,H1,H1,H2,H2,H2,P1,P2,P3,P5,P4
```

and signs

```text
+,-,+,-,-,+,+,+,+,-,-.
```

Production must compare every relevant field of the received task198 ledger
to this literal roster, including ordinal, block, type, ten index, context id,
role, sign, orientation, and prefix list.  Do not merely check length or a
digest supplied by the same receipt.  The combined ABI block is `H1`, `H2`,
or `P`; `P1/P2/P3/P5/P4` are occurrence labels, not five combined endpoints.

Use the exact static substitutions of the authenticated task179 constructor.
Paper products concatenate displayed factors from right to left.

```text
PB3 x=A12, y=A23
z = inverse(PP(x,y));  u = inverse(PP(y,x))
H1: (x,y)+, (x,z)-, (y,z)+
H2: (u,x)-, (x,y)-, (u,y)+

PB4 generator order: A12,A13,A14,A23,A24,A34
b1=(A23,A34)       +
b2=(PP(A12,A13),PP(A24,A34)) +
b3=(A12,A23)       +
b5=(PP(A13,A23),A34) inverse slot
b4=(A12,PP(A23,A24)) inverse slot
```

Here the displayed b-order is the immutable task179 occurrence order
`natural_index 1,3,0,2,4`.  Reconstruct the three full relation words with
the same right-to-left paper-product constructor.  Do not search for a row
whose literal block is the nonexistent string `P`.

## 5. Signed prefixes and both independent Fox identities

For each prefix ordinal, multiply the **signed** base factor
`r_j` for sign `+1` and `r_j^-1` for sign `-1`, in the exact listed order.
Then use v225 exactly:

```text
r_o  = rho_o(g0)                       (unsigned)
Q_o  = product of named signed factors
P_o  = Q_o*r_o for a direct slot, Q_o for an inverse slot
xi_o = r_o^-1 - 1
w_o  = sigma_o * P_o * xi_o
```

The first implementation multiplied unsigned factors and used zero-based toy
prefixes; both behaviours must disappear.

Implement a literal left Fox gradient over sparse pairs `(component,Q-key)`.
For each of `H1,H2,P`, recompute rather than assert:

```text
sum_o sigma_o P_o delta(r_o^-1) = -delta R_B(g0)
D1 of that chain                   = 1-R_B(g0)
epsilon_B                          = 1-R_B(f)
epsilon_B                          = D1[d_B-(delta R_B(f)-delta R_B(g0))].
```

The checker reconstructs all four equalities independently.  The certificate
must expose computed equality results and enough sparse data to replay them;
hardcoded `True` identities are forbidden.

## 6. Correct marked action and u0

Construct the source word

```text
comm=[x,y]=x^-1 y^-1 x y,
z0_word=comm*comm*comm.
```

For occurrence `o`, evaluate `q_o(z0)` through the exact substitution and set

```text
k_o = p_o q_o(z0) p_o^-1,
(z0 odot w)_o = k_o * w_o,
u0_o = (z0 odot w)_o - w_o.
```

Retain both translated and subtracted sparse terms and their source-word,
substitution, `p_o`, and coefficient ancestry.  The old code used `x^3`,
cancelled `P*P^-1` on the wrong side, and omitted the `-w` term; none of that
may remain.  Output `q_o(x)` and `q_o(y)` separately so task227 can reconstruct
the whole actor map, but do not claim a v216 membership result.

## 7. Actual input schema and fail-closed provenance

The task192 positive receipt itself supplies `g760`,
`exactification.literal.c_exact`, and
`exact_direct_replay.replay.corrected_word`.  Require its exact cached-v3
schema/terminal/seal and

```text
corrected_word == reduce(g760+c_exact),
right_g760_multiplication == true,
exact_direct_replay.replay.direct_all_seven_replay == true.
```

Do not require nonexistent receipt fields such as a top-level `artifact`,
`member`, or `manifest`.  Authenticate run/head/artifact/member/checker facts
from separately staged canonical sidecars with a versioned exact schema and
cross-equality of member path/bytes/SHA to the receipt bytes.  Likewise, the
task198 receipt has no `bridge.source_ancestry`; require the actual fields it
does expose: schema, positive terminal, seal, exact `bridge` ledger and
insertion, and `evaluator.entry_points` including `section_cocycle`.  Use a
separate canonical task198 attestation for immutable run/head/artifact/member
and checker acceptance.  Reject a missing, noncanonical, mismatched, SELFTEST,
or nonpositive sidecar as typed `UNKNOWN_INPUT` before specialization.

The parent will stage the sidecars only after task192 and task198 production
acceptance.  SELFTEST must not fabricate a PRODUCTION acceptance.

## 8. Real mutation execution and independent checker

The existing `attempted`/`rejected` lists are only prose and are rejected.
For every registered mutation, create exactly one changed package or input in
SELFTEST, run the relevant producer/checker validator, require an exception or
negative verdict, and retain mutation name plus observed rejection reason.
The checker must independently execute the controls; it may not accept the
producer's mutation counts as evidence.  Cover all 37 names already
registered, plus separate controls for the corrected PB3 middle sign, every
PB4 triple family, modulo-9 degree reduction, actual one-based prefix roster,
pentagon combined-block mapping, commutator-cube word, and the missing `-w`
term.  Report the new exact attempted/rejected count only after static
construction; parent execution is still required for acceptance.

The checker must independently rebuild group arithmetic, literal
substitutions, relation factors, prefixes, Fox chains, endpoints, marked
action, and `u0`.  Width checks and false-claim flags alone are insufficient.

## 9. Driver, resource stops, report, and v220 boundary

Keep the driver serial and fail-closed.  Ensure every typed resource stop and
input stop writes the expected fresh receipt, and that producer/checker exact
terminals are compared.  Pin the repaired four files only after their final
bytes are known.  Do not preserve obsolete identities from the rejected
version.

The reply must enumerate each defect above and its concrete repair, exact new
file identities, exact sidecar schemas and missing production inputs, computed
mutation roster, and an explicit unexecuted status.  Its v220 mapping remains:

```text
A2 paper contract:          1/3
A2 implementation SELFTEST: 0 until parent GHA producer+checker acceptance
A2 actual specialization:   0 until both actual receipts and checker pass
A3 and later:               untouched
```

No compatible lift, fake certificate, or Ihara witness may be claimed.
