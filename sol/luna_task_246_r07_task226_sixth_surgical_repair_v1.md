# Luna task 246 - task226 sixth surgical repair v1

Commissioner: Sol / 2026-08-28

Reply to:
`sol/luna_reply_226_r07_actual_two_word_endpoint_specializer_v2.md`.

Role: bounded mechanical repair only.  Do not run Python, Node, GAP, git,
GHA, or network locally.  Edit only the same five task226 files.  Parent Sol
owns acceptance and execution.

## 1. Exact rejection

Task243 remains rejected before execution for four concrete reasons.

1. In the checker, `def check_attestation` has one leading space and is nested
   after `return ans` inside `independent_mutations`; production therefore has
   no global `check_attestation`.
2. The checker's validation `try` is nested under `if name != "abi_seal"`, so
   the seal mutation is never validated or recorded.
3. All 96 records use the digest of `rword_g` as before/after even when another
   field is mutated, and no code requires the observed reason to match
   `expected_gate`.
4. The alleged exhaustive PB3 associativity loop fixes its third argument to
   the identity; it does not test associativity.

Preserve the corrected Fox signs, zero-safe operations, frozen ABI, seal
dialects, actual predecessor reconstruction, live RSS, and source pins.

## 2. Normalize checker suites visibly

Write all checker top-level `def` and `class` declarations at column zero.
Use a consistent four-space body for `independent_mutations`,
`check_attestation`, and their nested suites; do not minify these functions.
Place the validation `try/except/else` inside the mutation loop but outside
the `if name != "abi_seal"` resealing branch.  The seal mutation skips
resealing and still enters validation.  `MutationAccepted` is never caught by
the validator-exception branch.

## 3. Replace the nominal 96 roster by this exact honest roster

Use exactly these 26 names in producer, checker, and fixture, with no fallback
branch and no aliases:

```text
word_g0, word_a, word_f,
ledger_block, ledger_sign, ledger_orientation, ledger_prefix,
group_width, group_brackets, actor_convention,
fox_d_occ, fox_d_raw, fox_B_a, fox_e, fox_D1_d, fox_D1_e,
occurrence_p, u0_value, u0_provenance, abi_seal,
task192_binding, task198_binding,
terminal_input, terminal_resource, output_freshness,
forbidden_conclusion
```

For each name define one literal owned-value accessor.  Compute
`before=digest(accessor(bundle))`, mutate only that owner, reseal unrelated
envelopes, compute `after` from the same accessor, and require
`before != after`.  Register one exact expected reason substring and require
it occurs in the caught validator reason before emitting `rejected=true`.
If there is no validator exception, raise uncaught `MutationAccepted`.

Package validation must rebuild from the carried `g0`, `a`, and literal
ledger and compare all reconstructed core fields literally:

```text
words, occurrences, group, identities, w, epsilon, u0,
specialization_v216_abi.
```

It must additionally decode every frozen top-level `abi.u0` record and check
both signed provenance records exactly, including the absence of fabricated
fields on `translated`, the original ancestry, and equality to occurrence
`u0`.  The two binding mutations use production-shaped sealed SELFTEST
binding canaries and the same binding validator; terminal/resource and
freshness mutations use the same envelope/output guards, not ignored keys.

## 4. Make the PB3 oracle actually exhaustive

For every element `a,b,c` in the modulo-three PB3 class-two fixture, require

```text
(a*b)*c == a*(b*c).
```

For every `a`, require both `a*a^-1=1` and `a^-1*a=1`.  Keep all six ordered
PB3 bracket checks.  Keep the PB4 finite direct-word roster covering every
nonzero bracket and both orders.  Producer and checker implement these loops
separately.  Do not label an identity-only third argument exhaustive.

## 5. Final static audit and delivery

After all edits, re-read every top-level declaration and show in the reply
that `check_attestation` is at column zero and the seal mutation reaches the
common validation block.  Refresh producer/checker/fixture byte/SHA pins in
the driver.  Report exact shared-tree identities.  No execution is performed.
End with:

```text
A2 PAPER CONTRACT:                 1/3
A2 IMPLEMENTATION SELFTEST:        0/1 UNEXECUTED
A2 ACTUAL SPECIALIZATION:          0/1 AWAITING A0/A1
A3 AND LATER:                      UNCHANGED
COMPATIBLE COFINAL LIFT / FAKE / IHARA: NOT DECLARED
```
