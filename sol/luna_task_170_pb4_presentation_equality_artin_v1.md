# Luna task 170: PB4 11-relator positive presentation equality audit v1

Date: 2026-08-27
Role: Luna / bounded independent mechanical audit only

## 1. Purpose

The C-12/D1 lane already proves, with two implementations and falsifier
audit, one inclusion between the true (P_4) relation kernel and the normal
closure of the frozen eleven PB4 relators.  The opposite inclusion was marked
`closable` because the falsifier evaluated those eleven relators in the Artin
action, but the faithfulness reference had not been pinned.

Sol has now inspected Artin 1947, Theorem 14, on article page 112 (PDF page
13), which identifies braid classes with the indicated free-group mappings
and supplies faithfulness.  Perform the missing **mechanical** half cleanly:
independently show that each frozen PB4 relator, after substituting the
standard pure braid words (A_{ij}), acts trivially under the exact Artin
action on (F_4).

Do not alter C-12 certificates.  Produce a new versioned producer, independent
checker, certificate and reply.  This task does not prove the literature
theorem; Sol owns that paper inference.

## 2. Fixed mathematical inputs

Pin and reconstruct, do not hand-copy without a source check:

1. the frozen ordered generators
   `(a12,a13,a14,a23,a24,a34)`;
2. the exact eleven `pure_relations(4)` from the q3-chief artifact used by
   g760/v1--v6;
3. the standard braid words

```text
A_ij = sigma_(j-1) ... sigma_(i+1) sigma_i^2
       sigma_(i+1)^-1 ... sigma_(j-1)^-1
```

with the repository's signed-list and multiplication conventions; and
4. the task-157da/q3 producer and its helper-nonshared checker records which
already bind the PB4 marking and Artin orientation.

Pin the final C-12 files, especially
`search/certs/koubou158_completeness_v3.3_20260822.json`, while preserving its
historical statement that D2 was then unclaimed.

## 3. Producer calculation

Implement a small self-contained Artin action on the free group
(F_4=\langle t_1,t_2,t_3,t_4\rangle).  State the exact convention.  For every
signed braid generator require its forward and inverse automorphisms compose
to the identity on all four free generators.  Require both braid relations
and the distant commutation relation before evaluating PB4 words.

For each of the six (A_{ij}):

- output its signed braid word and SHA-256;
- compute all four freely reduced image words;
- check its induced permutation is the identity; and
- bind it to the corresponding q3 marked generator.

For each of the eleven frozen PB4 relators:

- expand it through the six (A_{ij}) words;
- freely reduce only at the braid-word/list level where valid;
- evaluate the composed Artin automorphism on all four free generators; and
- require the four images are exactly `[1]`, `[2]`, `[3]`, `[4]`.

Serialize the full 11-by-4 image table, expanded-word lengths and hashes.  The
terminal is positive only if all 44 images are literal identities.

## 4. Independent checker

Create a checker which imports neither the new producer nor its helper
functions.  It must reconstruct the q3 relators and (A_{ij}) words from the
pinned raw sources.  Use an implementation sufficiently different to expose
orientation mistakes; for example:

- producer: explicit substitution/composition of reduced free words;
- checker: evaluate braid letters successively on a tuple of free words with
  independently derived inverse formulas and opposite internal composition
  representation.

The checker must compare only canonical public outputs and direct identity
facts, not private intermediate object identities.  It must also directly
test the alternative inverse/order convention and show at least one frozen
canary distinguishes it.

## 5. Mutation and claim gates

At minimum reject mutations of:

- every one of the 11 relator words, one at a time;
- an (A_{ij}) conjugating-tail sign;
- braid multiplication order;
- forward/inverse Artin formulas;
- free-word inverse order;
- q3 input pin and relator order;
- one of the 44 output images; and
- any claim of Lean verification, literal A.18 solvability, cofinal lift,
  fake, or Ihara witness.

A mutated relator can accidentally remain a true relation.  Therefore use a
registered destructive mutation per row which is first required to produce a
nonidentity under an independent direct evaluation; do not demand that every
arbitrary byte flip must fail mathematically.

## 6. Evidence boundary

The receipt may assert only:

```text
all frozen 11 PB4 relators map to identity in the standard Artin action
conditional_paper_inference_with_Artin_Thm14: M_subset_Mtrue
```

It must separately cite the existing C-12 result as an input:

```text
existing_C12_D1_inference: Mtrue_subset_M
```

The machine certificate alone does not prove Artin faithfulness.  It becomes
the reverse inclusion only when Sol combines it with the inspected literature
theorem.  Do not rewrite CLAIMS or call the result `verified`.

## 7. Bounded execution and reply

Use new versioned files only.  Run all tests serially in a clean TEMP overlay;
this calculation should be small and must not invoke the full g760/Jennings
producer.  No git, push, workflow change or GHA dispatch.

Write `sol/luna_reply_170_pb4_presentation_equality_artin_v1.md` with exact
paths, bytes, SHA-256, commands, outputs, mutation counts and evidence grade.
Repeat verbatim:

```text
machine result: 11 frozen relators are identity under the Artin action
faithfulness is a literature theorem, not established by this checker
combined D1+D2 presentation equality requires Sol's paper inference
no literal A18 / cofinal lift / fake / Ihara witness declared
```
