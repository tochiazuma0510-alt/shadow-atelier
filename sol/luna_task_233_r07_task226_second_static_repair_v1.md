# Luna task 233 - task226 second static repair v1

Date: 2026-08-28

Role: bounded mechanical implementation.  Parent Sol owns all mathematics,
acceptance, git, and GHA.  Read Sections 1--11 in full before editing.  Do not
run Python, Node, GAP, git, GHA, or network.  Replace the existing task226
reply with an honest unexecuted repair report.

## 1. Verdict and authorized scope

The task229 revision is **REJECTED BEFORE EXECUTION**.  Its advertised Fox
identities, mutation results, ABI, and checker are not evidence.  Repair only:

```text
search/d972_r07_actual_two_word_endpoint_specializer_v2.py
crosscheck/check_d972_r07_actual_two_word_endpoint_specializer_v2.py
search/d972_r07_actual_two_word_endpoint_specializer_gha_driver_v2.g
search/certs/d972_r07_actual_two_word_endpoint_specializer_selftest_v2_20260828.json
sol/luna_reply_226_r07_actual_two_word_endpoint_specializer_v2.md
```

Do not edit any proof, predecessor, workflow, task227 file, or this
commission.  Keep Python, GAP, and JSON ASCII-only.

## 2. Exact defects found by parent Sol

Repair every item; do not merely change a receipt Boolean.

1. `ledger()` is not the task198 ledger.  It drops `block_index`,
   `block_slot`, and `occurrence`, and renames `fox_prefix_occurrences` to
   `prefix_occurrences`; production equality must therefore stop even on the
   genuine task198 receipt.
2. `relation_factors()` returns the fixed commutator words of the static
   substitutions.  A.18 requires the supplied word `g0`, and separately
   `f=g0*a`, substituted into each of the eleven pairs.  The present output is
   independent of both actual words.
3. Each `r=ceval(g0)` ignores its occurrence substitution, so the eleven
   `r_o` are false.  The corrected word `f` is never used in a Fox chain.
4. Full block words are concatenated in occurrence order although the frozen
   paper product is right-to-left.  The exact internal word is the reverse
   concatenation of the displayed signed factors.
5. H1 and H2 chains are accumulated without block tags, allowing unrelated
   coordinates to merge.
6. `endpoint()` maps `(component,q)` to `q-1`.  The left Fox boundary is
   `q*G_component-q`; the identity term is not used except when `q=1`.
7. The three reported identities are consequently neither v225 (1.2)--(1.5)
   nor independent.  In particular the existing residual algebra is a
   tautological combination of one wrong word.
8. The actor multiplication is a different normal-form convention from v216.
   Use `x^a y^b h^r` throughout, with product central coordinate
   `r+r'-b*a'` and inverse `(-a,-b,-r-a*b)` modulo nine.
9. Producer and checker mutations mostly flip one unrelated identity Boolean.
   They do not exercise the named gates.  The checker only asks whether a Fox
   routine returned a dict and trusts most producer sparse data.
10. The sidecar parser accepts the wrong sidecar schema, noncanonical bytes,
    and member metadata not bound to the receipt.  The task198 positive
    terminal is not pinned exactly.
11. The resource meter is a list of caps with zero usage; there is no typed
    resource accounting.  Direct invocation can overwrite a stale receipt.

## 3. Literal eleven substitutions and actual word evaluation

Use the exact full dictionaries from task198 `OCCURRENCE_LEDGER`, including
all fields and the key `fox_prefix_occurrences`.  Compare the received list
to that literal list, field for field.  Add only a derived `combined_block`
to the output ABI; never replace the received ledger.

Retain the v225/task229 substitution pairs.  Implement a free-word
substitution

```text
subst(w,L,R):  1 -> L, -1 -> L^-1, 2 -> R, -2 -> R^-1
```

followed by free reduction.  For each occurrence `o`, compute both

```text
rword_g[o] = subst(g0,L_o,R_o)
rword_f[o] = subst(f, L_o,R_o)
r_g[o]     = eval_Q(rword_g[o])
r_f[o]     = eval_Q(rword_f[o]).
```

For PB3 the pairs are `(x,y),(x,z),(y,z),(u,x),(x,y),(u,y)`, with
`x=A12`, `y=A23`, `z=inverse(PP(x,y))`, and
`u=inverse(PP(y,x))`.  For PB4 use displayed order
`b1,b2,b3,b5,b4`, namely the context IDs `1,27,21,26,28`.  `PP(A,B)` is the
right-to-left word `B+A`.

For either input word `s`, define the signed factor

```text
base_s[o] = rword_s[o]                  if sigma_o=+1
            inverse(rword_s[o])         if sigma_o=-1.
```

The full word for one block is

```text
R_B(s) = paper_product(base_s[o] in displayed occurrence order)
       = reverse-concatenate(base_s[o]).
```

Retain all source words, reduced words, evaluated Q keys, and SHA-256 values.
SELFTEST must assert that changing `g0` changes at least one `rword_g`, and
changing `a` changes at least one `rword_f` while leaving `rword_g` fixed.

## 4. Exact left Fox chains and the four v225 equalities

Represent a chain coordinate as `(block,component,Q-key)`.  For a generator
`G_i`, implement

```text
D1(q*e_i) = q*G_i - q.
```

Recompute all of the following as sparse term equalities for each block, and
emit both sides, not just Booleans:

```text
d_B_occ = sum_o sigma_o * P_o * fox(inverse(rword_g[o]))
d_B_raw = -fox(R_B(g0))
d_B_occ == d_B_raw

Ba_B    = fox(R_B(f)) - fox(R_B(g0))
e_B     = d_B_occ - Ba_B
e_B     == -fox(R_B(f))

D1(d_B) == 1-eval_Q(R_B(g0))
D1(e_B) == 1-eval_Q(R_B(f)).
```

Here `Q_o` is the product, in the listed order, of the signed `base_g[j]`
named by the one-based `fox_prefix_occurrences`; and

```text
P_o = Q_o*r_g[o]  for a direct/+ slot
      Q_o          for an inverse/- slot.
```

Build `xi_o=r_g[o]^-1-1`, and require the boundary of the full occurrence
chain `sigma_o P_o fox(r_g[o]^-1)` to equal the sparse `w_o` defined below.
The checker independently reconstructs the source substitutions, both full
words, every Fox chain, every boundary, and compares every serialized term.
It may not accept producer identity flags or merely check return types.

## 5. Q3/Q4, actor, marked maps, w, epsilon, and u0

Retain the complete v225 class-two formulas and all 3/12 bracket entries.
Use the actor normal form fixed in Section 2.  In both implementations test
identity, inverse, selected nontrivial associativity, all generator
commutators, ninth powers, coordinate widths, all 729 actor states, and the
243 disjoint cosets of `<(0,0,3)>`.

For each occurrence emit

```text
q_o(x)=eval_Q(L_o), q_o(y)=eval_Q(R_o)
p_o=eval_Q(P_o)
xi_o = r_g[o]^-1-1
w_o  = sigma_o * p_o * xi_o.
```

The residual target is exactly

```text
bar_epsilon_1[B] = D1(e_B) = 1-eval_Q(R_B(f)).
```

For `h=[x,y]=x^-1 y^-1 x y` and `z0=h^3`, evaluate `q_o(z0)` from the
emitted `q_o(x),q_o(y)` and set

```text
k_o(z0)=p_o q_o(z0) p_o^-1
u0_o=k_o(z0) w_o-w_o.
```

Retain the two summands and coefficient ancestry.  The top-level ABI uses one
unambiguous zero-safe format:

```text
"u0": [
  {"ordinal":1,"terms":[...],"translated_terms":[...],
   "source_coefficient_terms":[...]}, ... exactly 11 rows
]
```

Every occurrence also carries the complete immutable tag fields, `rword_g`,
`rword_f`, `p_o`, `q_o(x)`, `q_o(y)`, `xi_o`, `w_o`, and its `u0` row.  Empty
term lists are compared as empty lists; never skip equality because a list is
empty.

## 6. Stable output and task227 handoff

The positive result contains `specialization_v216_abi` with exact schema

```text
d972-r07-v216-specialization-abi/v1
```

and at least: modulus, actor convention, full immutable ledger, eleven
occurrences, `bar_epsilon_1`, the zero-safe eleven-row `u0`, ten-to-eleven,
literal substitutions, the two full block-word rosters, sparse Fox replay,
and self digest.  The checker rebuilds this ABI and seals it independently.

The task226 checker verdict must bind the checked receipt:

```text
schema, terminal, accepted=true, independent=true,
receipt_path, receipt_bytes, receipt_sha256,
abi_sha256, checker_reconstruction_sha256.
```

No member or manifest file is invented by task226.  A later parent-created
production binding will bind this receipt and verdict to run/head/artifact.

## 7. Exact predecessor authentication

Require canonical bytes, seals, and exact terminals:

```text
task192 schema   d972-r07-normalized-exact-common-word-cached/v3
task192 terminal R07_NORMALIZED_EXACT_CACHED_COLGEN_V3_COMMON_WORD
task198 schema   d972-r07-seven-context-roof-presentation/v1
task198 status   COMPLETE
task198 terminal ROOF_BRIDGE_ISOMORPHISM.
```

The task192 sidecar schema is exactly
`d972-r07-task192-production-binding/v1`; task198 is exactly
`d972-r07-task198-production-binding/v1`.  Parse canonical sidecar bytes.
For each, require its exact receipt path/bytes/SHA and also

```text
member_path == receipt_path
member_bytes == receipt_bytes
member_sha256 == receipt_sha256
terminal == receipt terminal
checker_acceptance == true
```

plus nonempty run/head/artifact/checker fields.  A sidecar of the other schema
must fail.  Bind `f=reduce(g760+c_exact)` and the two task192 replay Booleans
before specialization.

## 8. Genuine SELFTEST and mutation execution

Use a nontrivial pair `g0,a` with `f != g0`, all eleven literal occurrence
tags, both word roles, nonidentity signed prefixes, nonempty H1/H2/P replay,
and nontrivial marked actions.  The producer and checker separately rebuild
the package.

For every registered mutation, record

```text
name, changed_field, expected_gate, observed_reason, rejected=true.
```

Each name must change its named load-bearing datum and call the validator
which owns that datum.  It is forbidden to implement unrelated names by
setting `target_negative_fox=false`.  At minimum exercise both words,
right-correction order, all exact ledger fields, repeated E3 versus E4-C21,
each substitution, every sign/orientation/prefix rule, direct/inverse factor,
both Fox word identities, boundary `qG-q`, all PB bracket families, actor
normal form/cosets, marked conjugation, `z0`, every `u0` summand/ancestry,
ABI seal, predecessor binding, terminal vocabulary, stale output, resource
terminal, and all forbidden conclusion flags.  The checker must execute its
own mutations; producer mutation records are not evidence.

## 9. Resource and fresh-output contract

Use an explicit budget object with actual counters for input bytes, word
steps, group operations, sparse support, mutations, checker work, serialized
bytes, elapsed wall seconds, and peak RSS when the platform exposes it.
Exceeding a cap yields a fresh sealed `UNKNOWN_RESOURCE` receipt naming phase,
cap, value, and limit.  Malformed input yields a fresh sealed
`UNKNOWN_INPUT`.  Refuse a pre-existing output in producer and checker; do not
overwrite it.  SELFTEST must trigger and check one input and one resource
terminal on separate fresh paths.

## 10. Driver

Pin final producer/checker/fixture bytes.  Use `CreateDir` for `ci/out` and a
serial shell script.  Compare the exact producer and checker terminals with
anchored grouped regexes.  UNKNOWN is a typed run result but never an A2
acceptance.  Only exact SELFTEST producer+independent-checker success counts
for A2 milestone 2; only exact COMPLETE production counts for milestone 3.

## 11. Reply and v220 boundary

Report each repaired defect, final byte/SHA identities, exact SELFTEST roster,
remaining actual inputs, and `UNEXECUTED`.  State exactly:

```text
A2 paper contract:          1/3
A2 implementation SELFTEST: 0 until parent GHA producer+checker pass
A2 actual specialization:   0 until actual COMPLETE receipt+verdict
A3 and later:               untouched
```

No pointed multiplier, exact endpoint zero, compatible lift, fake, or Ihara
witness is constructed by this task.
