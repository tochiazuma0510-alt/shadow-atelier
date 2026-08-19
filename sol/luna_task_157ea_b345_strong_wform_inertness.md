# Luna task 157ea — explicit T-53 strong-word inertness certificate v1

## Role and objective

You are Luna.  Implement a new, diagnostic-only lane for the single explicit
T-53 strong correction

```text
x := PB3 letter 1 = A12
y := PB3 letter 2 = A23
xi  := x^18
eta := y^18
[a,b] := a^-1 b^-1 a b
s := [eta,xi] = y^-18 x^-18 y^18 x^18
```

The cross-checked v10 run exhausted the registered 4096 WordExpr corrections
without a positive certificate.  Every row first missed target 6,
`hexagon_1_coface_0`, component 4, but the exact missing blockers formed 31
classes.  Thus a common target slot is real, while a common cokernel class is
not established.  The explicit word `s` is not in that registered 4096-word
dictionary, so the run did not decide the preregistered W-P0 prediction.

This lane asks only two exact questions:

1. Do all five standard PB3-to-PB4 cofaces of `s` lie in
   `Phi_3(H4)=H4^3[H4,H4]`?
2. Is the target-6 residual for `f0*s` equal to the target-6 residual for `f0`
   in `H4/Phi_3(H4)`?

Use the same left-Fox/Crowell presentation criterion and the same freshly
reconstructed finite D2 prefix as v7--v10.  A positive solve is an exact
certificate because every stored column is a genuine translated PB4 relator
boundary.  A missing pivot is only prefix incompleteness.  This lane never
claims nonmembership, an obstruction, W-FORM universality, full-H3 coverage,
B4-A, or B4-B.

## Frozen inputs and provenance

Same-job q3 inputs:

```text
search/d972_b345_q3_chief_v1.g
  b95fc29b326c3d6a378249cdeb03595eed8d0211a7fe0358fc02447d70d5f755
search/check_d972_b345_q3_chief_v1.py
  ddb52ddae18327209692f0f6eb8b4f65cbdd446155be660a621de24274cc3f73
search/d972_b345_q3_gha_driver_v1.g
  c397cd837ff6814f7b7a8ca0604c6aed54fa0bc85bb577516ea1c6e7df83a831
q3 receipt
  3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72
```

Mathematical and certificate references:

```text
search/d972_b345_relfrat3_pivot_surgery_v7.py
  a19c3353c5cfc6da8ad0b7d941ba94bde043c80e69e33c889c5710c897d7a757
search/check_d972_b345_relfrat3_pivot_surgery_v7.py
  fbe033704180a808320c897c52613ca6847305dd85ddcd7a70aa825161e8bfa0
search/d972_b345_relfrat3_wordexpr_memo_v9.py
  7dede323c3c52bc7cf7d99af6d542b3683823879a4bb3e340aca8ce53dcf196f
search/check_d972_b345_relfrat3_wordexpr_memo_v10.py
  264258dcb945401e3db10ecd4fedd7a8dd79a8d7b0f31dbc0cfbe643537eac2d
search/d972_b345_relfrat3_wordexpr_memo_gha_driver_v10.g
  a5e9bdb34d85669a6221e4b0fa8e4c3af0aee343aade59fde52013d05753afc0
```

Cross-checked v10 production evidence is provenance, not a checkpoint:

```text
run                             32261068150
commit                          3553c18011d40056dd2e26623aeec3ba72a856b7
artifact ID                     9373093887
archive sha256                  503b8dbf506f0a03429b82a6efdf5645006f2c90540cc69b406163f9bb0f4c7e
receipt sha256                  0675e0ac957796cd2a9facee805b8f5e258d36f0c824e68ba916fdedeeedeade
terminal                        SEARCH_INCOMPLETE / registered_dictionary_exhausted
claim                           unknown_not_obstruction
```

Fresh prefix reconstruction must reproduce these deterministic bindings:

```text
formula_sha256
  b43284edac5b4dae945bb3b30ac0f177dc47df8724cb32acd6057b26d82a27ef
stable_rounds_projection_sha256
  75a2894da0f19d0e541e27924ee63e220a6eca35e852b21088ee304ba42fc42d
translations_sha256
  a4b952bce888713e293587cd63d710465121e782448a3e2a571d80b992ea363f
columns_sha256
  cb57176146b926df16e508429db5aa1ff6b5b0ec691f2328371973681089b343
blocker_history_sha256
  b5f100e45e874ce5ee3270cd31350b4318cf40931055571ac70066e69d62de53
candidate-1 final blocker sha256
  0cd653ee0966ccc83d270802bbb5d00b61731f28e27eec1918bb5ea282e00903
```

The volatile rounds SHA is provenance only and must not be a fresh gate.  Do
not import any old receipt, basis, pool, row, proof DAG, or blocker as an input.

## Authorized files

Create only:

```text
search/d972_b345_strong_wform_inertness_v1.py
search/check_d972_b345_strong_wform_inertness_v1.py
search/d972_b345_strong_wform_inertness_gha_driver_v1.g
sol/luna_reply_157ea_b345_strong_wform_inertness.md
```

Do not edit q3, v1--v10, workflows, receipts, claims, dialogue, or any other
file.  Temporary diagnostics belong outside the repository.  Do not run a
full producer locally, production GAP, Git, GHA, or a workflow.

## A. Exact word and typing gates

Rebuild, do not merely quote, the exact frozen base word

```text
f0 = [-2,-2,-1,-1,2,2,1,-2,-1,-1,2,2,2,-1,-2,-2,1,1,1,1]
digest_obj(f0)
  = b79f105ec2963ae55b69480f8ed8ab13083d01cb936da32edb4798698c22055d
```

Construct `xi`, `eta`, and `s` by the registered free-word operations and
require the literal reduced form

```text
s = [-2 repeated 18, -1 repeated 18, 2 repeated 18, 1 repeated 18]
length(s) = 72
digest_obj(s)
  = b85ac8d8b4528868282685a5da15eef9ee276d5e94e499d449d6aa1b0b7060ad
```

Require the code convention `[a,b]=a^-1 b^-1 a b` and independently replay
`s=[eta,xi]` as a free-word equality.  Construct

```text
fs = reduce(f0+s)
length(fs) = 92
digest_obj(fs)
  = c113c06d51480c8c819a563f6efc2323afecb7a54aabee96e7104d1d2921505b
```

Gate exponent sums `(0,0)` for `f0`, `s`, and `fs`.  In the authenticated E3
quotient, directly require `xi=eta=s=1`.  For the five canonical cofaces
`d_j:PB3->PB4`, directly require `d_j(xi)=d_j(eta)=d_j(s)=1` in E4.  These
identity tests are element comparisons, never digest comparisons.  Record all
words, canonical values, and ordered digests losslessly.

The five coface identities supply the actual typed premise; do not infer them
from an abstract label `H3`.  Since `s=[eta,xi]`, a five-positive Fox result is
an explicit instance of `s in J_Phi`, not a claim about every strong-form word.

## B. Fresh PB4 presentation and fixed prefix

Reconstruct the authenticated PB4 presentation, its eleven relators, E4, and
the exact left-Fox boundary map independently in the producer.  Preserve the
frozen convention:

```text
D(uv)=D(u)+uD(v)
for a negative letter, first move the prefix by x_i^-1, then add -prefix
translated column support (component,h) -> (component,t*h)
```

Build the complete 32768-translation BFS prefix and then the 207 directed
translations/2277 columns through the exact 32-round v7 fixed point.  Gate the
four stable hashes above and these final counts:

```text
BFS translations               32768
directed translations          207
total translation blocks       32975
total columns                   362725
pivots                          362709
dependent columns               16
```

Use the v6 calibrated caps and v7 sparse section/provenance representation.
The stable rounds projection removes exactly `elapsed_seconds` and `RSS_bytes`.
No measured runtime or RSS value may be copied into a deterministic hash.

As a drift canary, reconstruct the base target-6 residual `r0`, reduce its Fox
gradient against the saturated basis, and require its first missing pivot to
be component 4 with exact canonical-value SHA
`0cd653ee0966ccc83d270802bbb5d00b61731f28e27eec1918bb5ea282e00903`.
This canary is not a nonmembership claim.

## C. Six registered membership questions

The six targets, in this exact order, are:

```text
1..5  d_0(s), d_1(s), d_2(s), d_3(s), d_4(s)
6     delta = r_s * r_0^-1
```

Here `r0` is exactly v9 acceptance target 6,
`hexagon_1_coface_0`, constructed from `f0`; `r_s` is the same literal formula,
same coface, same association and inverse convention, constructed from `fs`.
Reconstruct both from the formula rather than editing the old word.  Require

```text
E4(r0)=E4(rs)=E4(delta)=1
D(delta)=D(rs)-D(r0) over F3[E4]^6
```

by direct exact evaluation.  Bind the reduced words, formula tree/order, word
digests, quotient values, sparse gradient counts, and gradient digests.  A
digest is only a binding.

For each target, first run a provenance-free exact reduction against the same
immutable saturated basis.  If it reduces to zero, regenerate that target from
the frozen word/formula and solve again with provenance enabled.  Require the
two gradients and solve outcomes to agree exactly.  Serialize a lossless proof
root.  If it leaves a missing pivot, record the full canonical component/value,
ordinal, and bounded prefix evidence, then continue to the next one; this is
`UNKNOWN` for that membership question, never false.

Do not add translations targeted at these six words.  The experiment is the
fixed registered prefix.  Do not construct the other 32 acceptance targets,
the 17 T diagnostics, normalized inverse words, onto checks, the 4096
dictionary, A5 layers, PB5, ANUPQ, or a candidate PASS.

## D. Positive proof format

For every positive bit, the receipt must contain enough data for a checker to
reconstruct the exact equality with a linear combination of genuine D2
columns:

- base relator index;
- exact left-translation canonical E4 value;
- exact section witness evaluating to that translation;
- F3 coefficient;
- packed provenance DAG with strictly backward references;
- exact target root and reachable-node/edge manifest;
- canonical registry and array length/SHA bindings.

Use the v7/v8 packed format where practical, but version the schema.  Internal
pool IDs are not public mathematical identities.  The exported proof must bind
canonical E4 bytes and section words.  A proof serialization cap after a
positive solve returns `UNKNOWN_RESOURCE`, never a boolean-only positive.

The independent checker must rebuild each translated PB4 relator column from
the presentation and section word, replay every packed node over F3, and
require the root to equal the independently recomputed target gradient.

## E. Receipt semantics and terminals

Use exactly four producer terminal tokens:

```text
B345_T53_STRONG_S_EXACT_TYPED_INERT
B345_T53_STRONG_S_PREFIX_INCOMPLETE
B345_T53_STRONG_S_UNKNOWN_RESOURCE
B345_T53_STRONG_S_UNKNOWN_INPUT
```

`EXACT_TYPED_INERT` requires all six membership bits positive with complete
proofs.  It proves only:

```text
this explicit s lies in intersection_j d_j^-1(Phi_3(H4)); and
the two explicit target-6 residuals r_s and r0 have the same H4/Phi_3(H4) class.
```

`PREFIX_INCOMPLETE` covers every complete six-question run with fewer than six
positive bits.  Preserve each exact positive independently and record:

```text
coface_membership_bits[5]
delta_membership_bit
explicit_s_JPhi_proved = all(coface bits)
target6_class_equality_proved = delta bit
exact_typed_inert = conjunction of the preceding two booleans
```

A zero bit means only `not proved in the registered prefix`.  Require

```text
claim_classification=unknown_not_obstruction
claim_scope=single_explicit_strong_word_fixed_prefix_only
negative_claimed=false
full_universe_claimed=false
W_FORM_universal_claimed=false
B4_A_claimed=false
B4_B_claimed=false
no_mathematical_obstruction_claimed=true
```

for every nonpositive terminal.

`UNKNOWN_RESOURCE` is restricted to the closed registered wall/RSS/sparse
entry/pool/pivot/DAG/serialization caps.  `UNKNOWN_INPUT` is restricted to a
missing or mismatched authenticated external file, SHA, schema, or upstream
terminal.  A formula, orientation, quotient-identity, proof, stable-prefix, or
internal invariant mismatch is a hard nonzero failure and must not produce a
receipt.

## F. Independent checker and self-test

The checker must not import the new producer or trust its words, formula
records, basis, bits, blocker, or proof DAG.  It may use a separately pinned
q3 collector implementation only after rebuilding and validating it.  It must
independently reconstruct:

- `f0`, `xi`, `eta`, `s`, `fs`, all digests and free equalities;
- E3/E4 marked images and the five cofaces;
- PB4 presentation and all base Fox columns;
- the 32768+207 translation schedule and the four stable prefix hashes;
- `r0`, `rs`, `delta`, quotient values, and Fox gradients;
- all six reductions and all positive proof roots;
- exact top-level/schema/terminal/claim key sets.

Include mutations for at least: commutator orientation, one exponent, coface
order, target-6 formula/coface, negative-letter Fox prefix order, quotient
identity, delta product order, gradient subtraction sign, missing-pivot
component/value, stable-prefix hash, proof coefficient/leaf/section/root,
positive bit without proof, a missing bit relabelled negative, and every claim
leakage boolean.

One combined lightweight producer+checker self-test is authorized.  It must
exercise the same production validation core with a small sealed toy
presentation, including a six-positive fixture, a partial-prefix fixture, and
RESOURCE/INPUT terminals.  If a fixture-only defect prevents reaching the
shared core, fix it and request one explicit corrective run before rerunning.
Do not run production q3, the full prefix, or a local GAP search.

## G. Driver and operational contract

The thin GAP driver must:

1. pin all q3 and new producer/checker source SHAs;
2. delete the exact output, logs, sentinels, and checker marker before running;
3. run q3 exactly once in a separate GAP child process using the configured
   package root, then require its sentinel, artifact SHA, and exactly one q3
   checker PASS marker;
4. run `python3 -u` producer and checker under `bash -o pipefail` with live
   `tee`, writing success sentinels only after zero exit;
5. require exactly one of the four producer terminal markers and exactly one
   checker PASS marker;
6. use output
   `ci/out/d972_b345_strong_wform_inertness_v1.json`;
7. emit progress at phase boundaries and at most every 30 seconds during the
   prefix build and six reductions.

Keep the 300-minute producer soft deadline, 4.5-GiB RSS guard, and a 330-minute
job contract.  Expected normal source runtime is roughly 4--10 minutes for the
producer and 4--10 minutes for the checker, but no runtime estimate is a proof
or a cap waiver.

The reply must list exact SHA-256/byte counts for the four authorized files,
self-test evidence, static pin/schema checks, known limitations, and the final
token

```text
B345_T53_STRONG_S_INERTNESS_V1_READY_FOR_GHA
```
