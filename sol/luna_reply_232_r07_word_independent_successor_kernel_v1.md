# Luna reply 232 - task256 SELFTEST truth repair

The five commissioned task232 files were repaired through task256 after the
task244 pre-execution rejection, with task244b/proof v247 and task252 binding
the projection-anchor correction. No Python, Node, GAP, git, GHA, or network
execution was performed by Luna.

## 1. Scope

Only the original task232 producer, checker, serial GAP driver, selftest JSON,
and this reply were changed. No predecessor, proof, workflow, or task237 file
was changed.

## 2. File identities

Current producer/checker/driver/fixture identities are:

```text
search/d972_r07_word_independent_successor_kernel_v1.py
crosscheck/check_d972_r07_word_independent_successor_kernel_v1.py
search/d972_r07_word_independent_successor_kernel_gha_driver_v1.g
search/certs/d972_r07_word_independent_successor_kernel_selftest_v1_20260828.json
sol/luna_reply_232_r07_word_independent_successor_kernel_v1.md
```

```text
producer  88706  c884253038800d7ecdaa3931c57adb0f02b1e5f4d87a6533dfb09e65a94edd81
checker   54874  dd41f90fc3cb5c5701655abaea56fc82178a56d32fcf9c631d723933d7ea2bc0
driver     4242  ddcd1ca059e3b0460f9043b87930ea4bdbd5259097eedd7b4f818059797561be
fixture     720  302c31244a43a86dd46d4a54e41756f067044f251db78b749c7bf70025fc85e7
```

The reply identity is reported out of band to avoid a self-referential
digest.

## 3. Task198 ABI repair

Authentication now reads the accepted receipt's top-level `Delta0`, `bridge`,
and `evaluator` objects. It checks the 6,441 literal rows, row digest/chunks/
order, normal-closure certificate, Delta0 order and marked generators, bridge
isomorphism ledger, evaluator ABI, receipt seal, exact task198 pins, canonical
guarded `ci/in` manifest (artifact/zip/run/head/member bytes and SHA), embedded
task176 provenance, and nonempty exact producer/checker attestations. Missing
or malformed input is `UNKNOWN_INPUT` before successor work.

## 4. Pinned affine successor

Production now loads the pinned task179 runtime and uses its actual Fox
gradient, quotient multiplication/inverse, element blobs, typed row keys,
translated-boundary, and complete boundary-oracle APIs. The ten contexts use
the exact PB3/PB4 pure-generator substitutions with right-to-left
`PP(A,B)=B+A`, IDs `21,22,23,24,25,1,27,21,26,28`, and distinct E3-C21 and
E4-C21 tags.

## 5. Complete boundary-plus-K oracle

For each presentation row, production substitutes the literal source word in
all ten contexts, evaluates the affine Fox chain, requires every roof value
to be identity, and retains the tagged defect. Membership dynamically queries
the complete translated-boundary family, separates boundary and K
coefficients, records active correlations and negative complete duals, and
never treats a sample, digest, or rank as a decision.

## 6. Queue and ancestry

The actual path processes all 6,441 defects in order, normalizes quotient-K
rows, preserves literal relator/conjugator ancestry and row-operation
coefficients, applies all four exact generator actions, and terminates only on
queue exhaustion. It replays every initial defect and every basis translate
through the same oracle and checks literal ancestry replay.

## 7. K certificate and built-in H2 anchor

The positive envelope contains ten successor values and roof reductions,
boundary/K membership receipts, basis rows and literal ancestry, action
matrices, queue terminal, order `3^t`, nilpotence bound `2t+1`, and
downstream-forbidden flags. The task244 literal `[x,y]^3` canary is withdrawn
by task244b/proof v247 because it is non-roof-trivial in all ten Delta0
coordinates. A positive K certificate instead computes a built-in H2(9)
projection anchor: every basis source word is evaluated left-to-right in the
frozen `(a,b,r)` law, then the least nonzero projection and inverse F3 scalar
produce the literal source word. The complete ten-context roof evaluator and
boundary-plus-K oracle replay every basis word and the selected word, retaining
all D1 values, Delta0 values, K coordinates, coefficients, and endpoint
receipts. No q1/D1 dependency fallback or cube substitution is permitted. It
does not consume task192 and does not construct d1, e1, mu1, an endpoint, lift,
fake, or Ihara witness.

## 8. Independent checker

The checker does not import the task232 producer. Its production path
independently authenticates top-level task198 and the canonical external
manifest/attestation bindings, loads pinned task179 arithmetic,
reconstructs the ten substitutions and all 6,441 defects, implements its own
reverse support-times-occurrence complete boundary oracle (without calling
task179's decision oracle), uses reverse pivot/relator traversal, and compares
producer/checker K spans in both directions modulo complete boundaries. It also
replays rows, actions, rank, order, and nilpotence data.

## 9. SELFTEST and mutations

The bounded typed fixture enters SELFTEST through the shared typed
echelon/membership/ancestry interfaces used by production. Mutation handling
now invokes a semantic validator
rather than toggling an unrelated Boolean table. Controls cover task198
bytes/schema/terminal/run/head/artifact/member/checker, presentation
completeness, context substitutions/tags, affine/Fox order, boundary/dual/
ancestry/pivot, omitted relators/translates/queue, action/inverse,
elementary-abelian checks, Delta1 BFS, task192, stale traversal, resource
terminals, forbidden downstream objects, and the seven owning projection
anchor fields (projected coordinate, selected index, inverse scalar, word
exponent/concatenation, Delta0 identity, D1 `z0` target, and source word).
The producer and checker mutation terminal is 57 attempted and 57 rejected;
the toy replay includes a nonzero exponent-two projection and least-index
selection.
Task256 additionally fixes the toy basis digest to the serialized basis,
gives every toy ancestry term a nonempty source word, and reconstructs every
basis projection/D1/roof/membership receipt before validating the selected
anchor. Task260 makes the `projected_coordinate` mutation own
`projection_anchor.projected_coordinate`; its selected-anchor equality gate
now rejects that non-vacuous mutation. The exponent-zero toy source is the
nonempty cancelling word `[1,-1]`.
Task263 makes `roof_reductions` the sole toy roof ledger owner: producer
validation checks the ten typed successors/source words separately from
`roof_reductions == [True] * 10`, and the producer mutation changes one ledger
entry. The remaining mutation paths were audited; `false_ihara` now targets
the extant `Ihara_witness` field explicitly.
Task266 repairs the producer's tuple-owned `repeated_e3_insertion` mutation
with tuple slicing, preserving the owner type and reaching the semantic gate
without an `AttributeError`.

## 10. Resources, driver, and ledger

The single-process driver has SELFTEST and PRODUCTION modes, exact source
pins, stale-output rejection, exact-one markers, literal producer/checker
terminal equality, and post-checker sentinel creation. The producer v247 proof
pin was refreshed to 12104 bytes, SHA-256
`84ff184d6f2a55c7f59874ab7fc6433be1826f34694d5f5228477affef896a53`.
Production no longer has the former
unconditional `TASK198_RELATOR_DAG_NOT_STAGED` return; it runs the actual
runtime/defect/boundary/closure path and returns positive only after exhausted
closure. Resource exhaustion remains `UNKNOWN_RESOURCE`; malformed input
remains `UNKNOWN_INPUT`.

```text
A4 PRESENTATION INPUT:       0/1 AWAITING ACCEPTED TASK198
A4 INVARIANT CLOSURE:        0/1 UNEXECUTED
A4 WORD-BEARING K:           0/1 UNEXECUTED
A0/A2/A3:                    UNCHANGED
A5 AND LATER:                UNCHANGED
COMPATIBLE COFINAL LIFT / FAKE / IHARA: NOT DECLARED
```

No d1, e1, pointed multiplier, exact endpoint, compatible lift, fake
certificate, or Ihara witness was constructed. All runtime and mathematical
statuses remain UNEXECUTED by Luna.
