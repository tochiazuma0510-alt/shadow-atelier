# Luna task 169: g760 joint-kernel coefficient intersection v1

Date: 2026-08-27
Role: Luna / implementation and bounded mechanical audit only

## 1. Purpose and mathematical source

Read completely:

- `sol/proof_r07_joint_kernel_coefficient_intersection_v107.md`;
- task/reply/source/checker/driver/certificate produced by task 168; and
- the complete task-157ee/task-157ef joint-kernel record and full artifact.

Task 168 computes the 28-coordinate C-13 affine family

```text
A_j = {a in F3^28 : target_j - Sigma(a) lies in authenticated D2_j}.
```

This task computes the coefficient subspace represented by words in the
cross-checked registered joint value kernel

```text
K_joint = ker(F2 -> Q0 x E3 x E4^31),
```

intersects it with `A_j`, and materializes the resulting correction from
actual defining relation words.  It must run after a completed-j coefficient
calculation in the **same full invocation**, so the first parent GHA run can
return `A_9`, the joint-kernel intersection, and an explicit word without
repeating j=9.

This closes only the registered joint **value** gate at the projected
target6/presentation level.  It is not a literal A.18 lift.

## 2. Noninterference and pins

Use new versioned producer/checker/driver/certificate/reply files.  Do not
modify task-157ee/157ef, v1--v5, task-168 assets, workflows, proofs, CLAIMS,
or Sol replies.  Preserve exactly task 168's:

- g760, target6, 28 row order, Jennings projection and full-D2 traversal;
- completed-j and append-only delta authentication;
- coefficient affine family, lex-first rules and word conventions;
- default safe stop after 11 newly completed relators; and
- all mathematical terminal boundaries.

Pin at minimum the exact 157ee full receipt

```text
ci/b345_157ee_artifacts_32359956713/
  d972_b345_joint_kernel_qstar_closure_v1.json
SHA-256 1c3ad7a7124cee152eb40968cf212c14641a9f8720063c85f70533864898d0df
run 32359956713
```

and its task, producer, checker-v2, reports, q3 input, 31-context registry,
46-name alias table, record words, factor payload and every source required to
reconstruct the presentation.  Fail closed on any pin drift.

No git, push, workflow edit, GHA dispatch, full j=9 local run, or parallel
Python/GAP.  Use a clean TEMP overlay for bounded serial tests.

## 3. Reconstruct the exact group map

Independently reconstruct:

```text
omega3 : F2 -> Delta3
Omega  : F2 -> G_joint <= Q0 x E3 x E4^31
```

using the frozen `x,y` images and conventions.  Require:

1. `|Delta3|=27` and the same 28 ordered Schreier words as task 168;
2. the three target6 Pi4[3] contexts are exact projections of named rows in
   the 31-context registry (bind context ids and alias rows, not names alone);
3. the marked joint image/presentation invariants reproduce the 157ee
   receipt; and
4. the induced map `G_joint -> Delta3` respects all defining relations and is
   onto.

Let `K3=ker omega3`, `K_joint=ker Omega`, and
`Q=ker(G_joint -> Delta3)`.  Serialize this exact-sequence typing; do not infer
it from matching group orders alone.

## 4. Reconstruct defining kernel relators

Rebuild the complete task-157ee presentation layers:

- 6,318 Gamma Cayley-edge relations;
- 104 x/y action relations; and
- 19 complete Q0 factor relations with their Gamma defects.

Expand every auxiliary record/section generator back to its exact signed F2
word.  The output relation roster `R` must be a list of words in `{x,y}` whose
normal closure is the pinned `K_joint`; retain layer, ordinal, word length,
word SHA-256 and the original 157ee row binding.

For every `r in R` and every one of the 27 frozen Delta3 Schreier transversal
elements `t`, form and freely reduce `t*r*t^-1`, then rewrite it in the frozen
28-generator Schreier basis of `K3`.  Require direct reconstruction back to
the same F2 word and identity under `Omega`.

Take each rewritten word's exponent row modulo 3 and row-reduce the resulting
28-column system.  Retain the lexicographically first independent **input**
rows, not arbitrary linear combinations, so every basis row keeps one actual
word in `K_joint`.  Serialize:

```text
rank_B_joint
nullity / quotient H1 dimension
basis rows in F3^28
source layer/transversal/relation ids
exact F2 and Schreier words for every retained basis row
complete input-row digest and canonical basis digest
```

Require the row space to equal

```text
ker(H1(K3;F3) -> H1(Q;F3)).
```

Use a second bounded route where practical: construct the presentation of
`Q=K3/K_joint` by Reidemeister--Schreier and abelianize it modulo 3.  If that
route exceeds a registered resource cap, report it as an independent
promotion UNKNOWN; never silently replace the direct relation-row theorem.

## 5. Additional exponent gate

Do not assume the 157ee joint map encodes the historical exponent-sum-mod-3
prefilter.  Compute the two linear exponent rows of the 28 Schreier words and
measure whether they vanish on `B_joint`.

Define explicitly

```text
B_legal_value = B_joint intersect ker(exponent_mod_3 : F3^28 -> F3^2).
```

Report whether this intersection is strict.  Retain word-bearing independent
input rows for `B_legal_value`; if linear combinations are required, retain
short exact provenance in the selected `B_joint` relation-word basis and
materialize the combined word.  Every retained word must directly replay:

- identity in Q0 and E3;
- identity at all 31 E4 context ids and all 46 named aliases; and
- exponent sums zero modulo 3.

Call this `registered_joint_value_and_exp3_domain`.  Do not call it the full
literal A.18 domain.

## 6. Intersect with every completed coefficient family

For every completed MEMBER depth `j` from task 168, compute exactly

```text
A_joint_j = A_j intersect B_legal_value.
```

Parameterize the word-bearing basis of `B_legal_value` by `z`, solve the
task-168 quotient equation with `a=U*z`, and return:

- consistency, rank, nullity, canonical particular and kernel basis;
- lexicographically first coefficient vector `a` in the original 28-row
  order (prove lex-first; do not use an arbitrary RREF particular);
- canonical word-basis coefficients `z` for that `a`; and
- inclusion in the preceding depth's joint family when more than one depth
  is present.

Require mechanically:

```text
A_joint_j is nonempty => A_j is nonempty
A_joint_(j+1) subset A_joint_j
```

An empty intersection is a negative only for this pinned base, depth,
projected target6 and registered joint-value domain.  A nonempty intersection
is a positive coefficient certificate with the promotion boundaries in
Section 8.

## 7. Materialize the actual joint-kernel word

If `A_joint_j` is nonempty, form

```text
c_joint_j = R_1^(z_1) * ... * R_d^(z_d)
```

from the retained actual relation words, using paper multiplication and only
free cancellation.  Do **not** substitute the naive
`s_1^(a_1)*...*s_28^(a_28)` unless it independently passes every joint gate.

Record signed F2 word, length, exponent sums, SHA-256 and factorization.  From
the word itself, replay:

1. Q0, E3, all 31 context ids and 46 aliases;
2. the three target6 context identities;
3. projected Sigma at depth j;
4. equality with the 28-row linear combination for `a`;
5. `target_j-Sigma(c_joint_j)` reducing to zero against the authenticated
   task-168 D2 echelon; and
6. binding to g760, the completed-j public row and D2 state commitment.

## 8. Claim boundary and terminals

Every receipt must state explicitly:

```text
registered_joint_value_domain_computed = true/false
historical_exp3_prefilter_computed = true/false
full_E4_positive_class_reconstructed = false
true_PB4_D2_equality_used = false
literal_A18_replayed = false
two_hexagons_replayed_as_joint_system = false
HT1_HT5_all_edges_proved = false
cofinal_compatibility_proved = false
```

Use terminal names which distinguish at least:

```text
R07_760_JOINT_COEFF_INTERSECTION_NONEMPTY
R07_760_JOINT_COEFF_INTERSECTION_EMPTY
R07_760_JOINT_COEFF_UNKNOWN_RESOURCE
R07_760_JOINT_COEFF_INPUT_STOP
```

`NONEMPTY` means exactly one projected target6 solution in the registered
joint value+exp3 domain was materialized and replayed.  It does not mean an
A.18 lift.  `EMPTY` kills only this pinned g760 prefix in this registered
positive universe; audit whether the Pi projection and presentation image
make even that negative direction sound before any stronger declaration.

## 9. Independent checker and bounded tests

Create a helper-nonshared checker which imports neither the new producer nor
its math helpers.  It must independently reconstruct the group maps,
presentation relation words, 27 conjugates, Schreier rewriting, both
coefficient spaces, exponent intersection, selected word and every replay.
It may authenticate task 168's completed full-D2 state rather than regenerate
649,539 columns, and must label the resulting positive check conditional on
that authenticated D2 state.

Bounded serial tests must cover at least:

- small exact sequences of free groups onto finite nonabelian groups;
- relation normal closure needing more than the unconjugated relation rows;
- strict and redundant exponent filters;
- nonempty and empty affine intersections;
- a case where the naive Schreier product has the right coefficient but is
  outside the kernel, while the relation-word lift is inside;
- lex-first coefficient versus lex-first word-basis-coordinate distinction;
- mutations of every context id/alias, relation layer, transversal,
  Schreier sign/order, exponent row, basis row, source-word provenance,
  task-168 state commitment and every forbidden claim; and
- task 168 completed-j/safe-stop regression.

Generate the final preflight twice byte-identically from a clean pinned
overlay.  Run producer/checker/driver selftests serially.  If rebuilding the
full 157ee relation roster is too expensive for local bounded testing, use a
registered cap and prepare a GHA full lane; do not parallelize locally.

## 10. Report

Write a versioned `sol/luna_reply_169_r07_joint_kernel_coeff_intersection_v1.md`
with paths, bytes, SHA-256, exact commands/output, mutation counts, all
measured ranks, runtime estimates and UNKNOWNs.  Repeat verbatim:

```text
joint-kernel coefficient intersection closes registered value gates only
positive target6 modulo projected D2 is not literal A18
Pi4[3] projection and positive PB4 presentation comparison remain gates
all seven relation evaluations and HT1--HT5 remain required
no fake / cofinal lift / Ihara witness declared
```
