# Luna task 236 - task226 third static repair v1

Date: 2026-08-28

Role: bounded mechanical implementation. Parent Sol owns mathematics,
acceptance, git, and GHA. Read Sections 1--11 completely before editing. Do
not run Python, Node, GAP, git, GHA, or network. Replace, rather than defend,
the rejected task233 paths.

## 1. Verdict and authorized scope

The task233 return is **REJECTED BEFORE EXECUTION**. It is not a SELFTEST or
Fox certificate. Repair only:

```text
search/d972_r07_actual_two_word_endpoint_specializer_v2.py
crosscheck/check_d972_r07_actual_two_word_endpoint_specializer_v2.py
search/d972_r07_actual_two_word_endpoint_specializer_gha_driver_v2.g
search/certs/d972_r07_actual_two_word_endpoint_specializer_selftest_v2_20260828.json
sol/luna_reply_226_r07_actual_two_word_endpoint_specializer_v2.md
```

Do not edit task227/task235, proofs, predecessors, workflows, or this
commission. Keep Python, GAP, and JSON ASCII-only. Task233 Sections 3--10
remain mandatory except where this commission makes the serialization more
explicit.

## 2. Exact defects found in the task233 return

1. Producer production calls `seal(t192)` and `seal(t198)` at line 314, but
   no `seal` function exists. Production cannot start.
2. Producer line 259 calls `endpoint(target,3)` and
   `endpoint(residual,3)` on chains containing H1, H2, and PB4/P terms. A
   single `d=3` cannot decode PB4 width-ten keys or components 4--6. H1 and
   H2 endpoints are also merged into one untagged dictionary.
3. `expected_endpoint` and global `eps` omit block tags, so equal PB3 group
   keys from H1 and H2 can cancel. The three endpoints must remain separate.
4. ABI `u0[i].terms` is filled from `o["u0"]`. Task233 requires the two
   summands: `terms=w_o` and `translated_terms=k_o(z0)w_o`; task227 computes
   translated minus terms. The current ABI would compute translated minus
   the already-subtracted difference.
5. The four required equalities are not serialized and compared block by
   block. `residual_one_minus_Rf` is a tautology because `eps` is defined as
   `endpoint(residual)` and then compared to the same expression.
6. Checker lines 127--132 rebuild only a Fox dictionary and ask whether it is
   a dict. They neither compare it with `d_occ/d_raw/B_a/e` nor apply D1.
7. Checker recomputes relation words from the static commutator substitution
   words in `literals.factors`, not from the actual substituted `rword_g` and
   `rword_f`. It therefore cannot check either actual word.
8. Checker accepts the producer's three identity Booleans. It does not
   reconstruct signed prefixes, direct/inverse P_o, xi_o, w_o, marked z0,
   u0, or bar-epsilon term by term.
9. Producer and checker mutations still route many unrelated names through
   one changed schema/ledger/sign field. They do not invoke the semantic gate
   named in each mutation.
10. SELFTEST terminal probes are prebuilt JSON labels, not executions of the
    malformed-input and resource-stop paths. Resource accounting has no wall
    time, RSS, serialized bytes, or group-operation increments.
11. Producer lacks exact input/output path guards and returns only a printed
    UNKNOWN on stale output. Checker can write a verdict without refusing all
    stale/aliased paths and reports `independent=true` even for UNKNOWN.
12. Checker requires each bar-epsilon list to be truthy. Zero is a legitimate
    sparse endpoint and must be compared exactly, not rejected or skipped.

## 3. Typed Fox algebra; never mix blocks

Use three separately typed chain and endpoint spaces:

```text
H1: component 0..2, Q3 key width 4
H2: component 0..2, Q3 key width 4
P:  component 0..5, Q4 key width 10.
```

All chain coordinates are `(block, component, key)`. All endpoint coordinates
are `(block, key)`. Implement D1 termwise as

```text
D1(block,q*e_i)=(block,q*G_i)-(block,q).
```

The decoder must select Q3 or Q4 from the block tag on every term. It is
forbidden to pass a mixed chain to a function with one global degree.

For each block B independently compute, serialize, and compare both sides of
all four task233 equalities:

```text
d_occ[B] = sum_o sigma_o P_o fox(rword_g[o]^-1)
d_raw[B] = -fox(R_B(g0))
d_occ[B] == d_raw[B]

B_a[B] = fox(R_B(f))-fox(R_B(g0))
e[B]   = d_occ[B]-B_a[B]
e[B]   == -fox(R_B(f))

D1(d_occ[B]) == 1-eval_Q(R_B(g0))
D1(e[B])     == 1-eval_Q(R_B(f)).
```

Retain block-tagged `one_minus_R_g`, `one_minus_R_f`, and every D1 image.
No identity may compare a value to the expression used to define it.

## 4. Actual two-word construction

Retain the exact literal ledger including `fox_prefix_occurrences`. For every
occurrence rebuild both

```text
rword_g[o]=subst(g0,L_o,R_o)
rword_f[o]=subst(f,L_o,R_o),  f=reduce(g0+a),
```

then signed `base_g[o]`, `base_f[o]`, and reverse-concatenated full block
words `R_B(g0)`, `R_B(f)`. Serialize these under unambiguous names; do not use
one `factors` field for both static substitution pairs and actual word
factors.

For every occurrence independently rebuild the signed prefix, orientation,
`P_o`, `xi_o=r_g^-1-1`, `w_o=sigma_o P_o xi_o`, `q_o(x)`, `q_o(y)`,
`q_o(z0)`, conjugated `k_o(z0)`, translated w, and u0 difference. Compare all
producer terms exactly.

## 5. Exact zero-safe ABI

The ABI schema remains `d972-r07-v216-specialization-abi/v1`. Its u0 field is
exactly eleven rows:

```text
{
  "ordinal": o,
  "terms":                 exact w_o terms,
  "translated_terms":      exact k_o(z0) w_o terms,
  "source_coefficient_terms": exact +translated/-original ancestry
}
```

The u0 difference is `translated_terms-terms`; it may additionally be stored
as `occurrence.u0`, but it must never replace `terms`. Compare empty lists as
empty lists. `bar_epsilon_1` is exactly a dictionary with H1/H2/P lists;
empty lists are allowed and checked.

Seal the ABI by removing its self-digest field and hashing the canonical
remainder. Add and use a real receipt `seal` routine in producer and checker.

## 6. Independent checker

The checker must use no producer import. Starting only from `g0`, `a`, the
literal ledger, and its own Q/Fox routines, reconstruct Sections 3--5. Decode
every producer sparse object with exact schema, width, coefficient, uniqueness,
and canonical ordering checks. Compare all of these, not only their types:

```text
11 rword_g/rword_f and Q values
11 signed prefixes and P_o
11 xi_o, w_o, translated w_o, u0 rows
3 R_B(g0), 3 R_B(f)
3 d_occ, d_raw, B_a, e
6 D1 images / one-minus-word endpoints
3 bar_epsilon_1 blocks
the complete stable ABI and its seal.
```

Delete acceptance based on producer identity Booleans. Booleans may be
reported only after exact reconstructed rows are equal. A check such as
`isinstance(fox(...),dict)` is never evidence.

The checker reconstruction digest must hash the complete independently
rebuilt ABI, not only the eleven-row ledger.

## 7. Exact predecessor authentication

Require the exact receipt paths used by the driver, canonical bytes, receipt
seals, schemas, and exact terminals from task233 Section 7. Define and call
the seal routine. Require the exact sidecar schemas, receipt/member path,
bytes, SHA, terminal equality, checker acceptance, and nonempty
run/head/artifact/checker fields. Reject path aliases, SELFTEST, UNKNOWN,
wrong sidecar schema, and receipt/sidecar mismatch before specialization.

The result and checker verdict bind both predecessor receipt/sidecar
identities and the ABI SHA. No invented member or manifest input is allowed.

## 8. Genuine mutation execution

For every registered name create a fresh mutation of the datum named by that
name and invoke the owning semantic reconstruction. Record

```text
name, changed_field, expected_gate, observed_reason, rejected=true.
```

At minimum, separately mutate g0, a/c_exact, f order, one actual rword_g, one
actual rword_f, one base word, one relation-word order, every literal ledger
field family, prefix occurrence/order, direct/inverse P_o, xi sign, each Fox
equality, D1 `qG-q`, Q3 and each Q4 bracket family, actor product/inverse,
marked conjugation, z0 cube, original u0 term, translated u0 term, u0
ancestry, ABI seal, each predecessor binding, output freshness, resource
terminal, and forbidden conclusion flags.

It is forbidden to reject unrelated names by changing ABI schema, one ledger
entry, one factor sign, or one conclusion flag. The checker runs its own
mutations and does not trust producer mutation records.

## 9. Production-shaped SELFTEST

Use nontrivial g0 and a with f different from g0. Require all eleven actual
substitutions, nonidentity signed prefixes, nonempty H1/H2/P Fox replay, and a
nontrivial marked action/u0. Directly assert:

```text
changing g0 changes rword_g;
changing a changes rword_f but leaves rword_g fixed;
all four equalities in every block;
the checker rebuild equals the complete producer ABI.
```

Actually call the malformed-input and forced-resource paths using distinct
fresh in-memory/test destinations and check their sealed UNKNOWN_INPUT and
UNKNOWN_RESOURCE envelopes. Preconstructed terminal labels do not count.

## 10. Resource, fresh output, and driver

Measure input bytes, word steps, group operations, sparse support, mutation
work, checker work, serialized bytes, elapsed wall time, and peak RSS when
available. Enforce wall time during work. Resource stop writes a fresh sealed
UNKNOWN_RESOURCE with phase/cap/value/limit; malformed input writes fresh
sealed UNKNOWN_INPUT. Require exact relative ci/in input paths and ci/out
output paths. Refuse, never overwrite, stale receipt/verdict/log/sentinel
outputs.

Update the serial GAP driver pins. Use exact anchored producer/checker
terminal comparisons. UNKNOWN is a typed run outcome with checker verdict
`accepted=false, independent=false`; only COMPLETE or exact SELFTEST replay
may be accepted.

## 11. Reply and v220 boundary

Replace the reply with an item-by-item honest report, final byte/SHA
identities, exact mutation roster, and `UNEXECUTED`. State:

```text
A2 paper contract:          1/3
A2 implementation SELFTEST: 0 until parent GHA producer+checker pass
A2 actual specialization:   0 until actual COMPLETE receipt+verdict
A3 and later:               untouched
```

No pointed multiplier, exact PB endpoint zero, compatible lift, fake, or
Ihara witness is constructed by this task.
