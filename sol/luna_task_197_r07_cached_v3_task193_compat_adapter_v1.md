# Luna task 197 - R07 cached-v3 to task193 compatibility adapter v1

Commissioner: Sol / 2026-08-28

Reply to:
`sol/luna_reply_197_r07_cached_v3_task193_compat_adapter_v1.md`.

Role: bounded mechanical implementation only.  Do not run Python, GAP,
Node, git, GHA, or network locally.  Parent Sol owns mathematical audit,
repository brokerage, input-artifact staging, and every execution.  Do not
edit task192, task193, task194--task196, proof, provenance, or workflow
files.

## 1. Objective and exact type mismatch

Read in full:

```text
sol/luna_task_186_r07_normalized_exact_common_word_colgen_v2.md
sol/luna_reply_186_r07_normalized_exact_common_word_colgen_v2.md
sol/luna_task_192_r07_normalized_exact_cached_colgen_v3.md
sol/luna_reply_192_r07_normalized_exact_cached_colgen_v3.md
sol/luna_task_193_r07_second_frattini_affine_prefix_compiler_v1.md
sol/luna_reply_193_r07_second_frattini_affine_prefix_compiler_v1.md
the complete final task186/task192/task193 producer/checker/driver dependency cone
sol/proof_r07_compressed_diagonal_successor_relation_module_v188.md
```

Task192-v3 emits

```text
schema   = d972-r07-normalized-exact-cached-colgen/v3
terminal = R07_NORMALIZED_EXACT_CACHED_COLGEN_V3_COMMON_WORD
```

whereas task193-v1 accepts only the task186-v2 envelope

```text
schema   = d972-r07-normalized-exact-common-word-colgen/v2
terminal = R07_NORMALIZED_EXACT_COMMON_WORD_COLGEN_V2_COMMON_WORD.
```

The v3 payload retains the v2 exactification/direct-replay mathematics, and
the v3 independent checker internally rebuilds a v2-shaped receipt and runs
the authenticated v2 helper checker.  Nevertheless, the raw v3 receipt is
not a task193 input.  Build a versioned adapter which produces one explicit
v2-compatible receipt and a separate conversion certificate, then requires
the unmodified full v2 checker to accept the converted receipt.  Merely
changing two labels without the two full checker attestations is forbidden.

This task changes no mathematical word, coefficient, row, or ancestry.

## 2. Authorized files

Create only:

```text
search/d972_r07_cached_v3_task193_compat_adapter_v1.py
crosscheck/check_d972_r07_cached_v3_task193_compat_adapter_v1.py
search/d972_r07_cached_v3_task193_compat_adapter_gha_driver_v1.g
search/certs/d972_r07_cached_v3_task193_compat_adapter_selftest_v1_20260828.json
sol/luna_reply_197_r07_cached_v3_task193_compat_adapter_v1.md
```

Pin exact bytes and SHA-256 of every imported source, checker, contract, and
fixture.  Do not self-pin the GAP driver.  Temporary files stay outside the
repository.

## 3. Production input authentication

Production accepts exactly one parent-staged task192-v3 artifact with:

1. immutable GHA run id, head SHA, artifact id/name, ZIP digest, member path,
   member bytes, and member SHA-256 supplied as explicit driver bindings;
2. a sealed v3 receipt with positive schema/status/exact terminal;
3. the exact one-line task192-v3 checker attestation produced by the pinned
   checker on that same byte string; and
4. the exact word and direct replay fields required by task193:

```text
exactification.positive_receipt = true
exactification.literal.c_exact
exactification exponent/provenance fields
exact_direct_replay.replay.corrected_word
exact_direct_replay.row and row_sha256
right_g760_multiplication = true
hexagons = true
pentagon_printed_order = true
replay.direct_all_seven_replay = true
```

Authenticate the committed v3 producer/checker identities and the immutable
artifact metadata.  Missing, resource-only, SELFTEST, malformed, stale,
wrong-word, or mismatched inputs are `UNKNOWN_INPUT`; do not emit a
compatible receipt on that branch.

The driver input path must be a parent-bound repository path under a
dedicated production certificate directory, with exact bytes/SHA bindings.
Reject absolute paths, traversal, `ci/out`, and an unbound identity.  The
implementation task does not add the later production artifact itself.

## 4. Lossless compatibility conversion

Create two runtime outputs:

```text
task193_compatible_v2.json
adapter_certificate_v1.json
```

For the compatible receipt:

1. deep-copy the authenticated v3 receipt;
2. remove its old outer `self_digest`;
3. replace only the outer schema and positive terminal by the exact v2
   values;
4. retain status `COMMON_WORD` and every other mathematical/provenance
   field byte-for-canonical-value;
5. add no field unless the unmodified v2 checker is proved to accept it; and
6. seal it with the exact canonical JSON convention expected by task186-v2.

The adapter certificate separately records:

1. all immutable input identities and both checker source identities;
2. input-v3 and output-v2 bytes/SHA-256/self-digests;
3. a canonical recursive field-difference transcript proving that only
   `schema`, `terminal`, and `self_digest` changed;
4. exact equality of corrected word, `c_exact`, exponents, direct row,
   direct-row digest, selected columns/coefficients, all-seven flags,
   checkpoint absence on a positive receipt, and every task193-consumed
   field;
5. the v3 checker line; and
6. the later v2 checker line over the converted bytes.

The producer must not forge the v2 checker line.  The driver runs the pinned
unmodified v2 checker, writes its exact one-line attestation, and only then
invokes/finalizes the adapter certificate.  A safe two-phase producer
(`prepare`, then `finalize`) is acceptable.  The final certificate seal must
bind the actual attestation bytes.

## 5. Independent checker

The adapter checker imports neither the adapter producer nor its canonical
diff/seal helpers.  It receives the original v3 receipt, converted v2
receipt, both checker attestations, immutable artifact bindings, and the
adapter certificate.  It independently:

1. validates both outer seals and exact positive envelopes;
2. recomputes the complete recursive field diff and enforces the three-field
   whitelist;
3. compares every task193-consumed field and all exactification/direct replay
   values;
4. validates the exact v3 and v2 checker lines and pinned checker identities;
5. binds both files to the recorded GHA artifact metadata; and
6. rejects any extra mathematical mutation even when both words freely
   reduce to the same word.

The external full v3 and v2 checkers remain load-bearing.  The adapter
checker is an additional helper-nonshared conversion checker, not a
replacement for either.

## 6. SELFTEST and mutations

SELFTEST uses a bounded production-shaped pair of sealed v3/v2 envelopes
with a nonempty signed corrected word, nontrivial `c_exact`, nonempty sparse
direct row, coefficient two, and all task193-consumed flags.  It exercises
prepare, external-checker placeholders with exact distinct typed lines,
finalize, and independent conversion replay.  It does not claim that the toy
word is an R07 correction.

Reject at least mutations of:

```text
v3 schema/status/terminal/self_digest
artifact run/head/id/zip/member bytes/member sha
v3 checker line or checker source pin
v2 schema/status/terminal/self_digest
v2 checker line or checker source pin
corrected_word sign/order
c_exact sign/order
one exponent or A/B value
direct sparse key/coefficient/order/row_sha256
one all-seven/hexagon/pentagon/right-multiplication flag
solution coefficient and selected column
an unwhitelisted added/deleted/changed field
stale output
SELFTEST substituted for production
```

Every advertised mutation must be attempted and rejected independently.

## 7. Driver and production handoff

Use only the generic GHA runner; do not edit a workflow.  Modes are
`SELFTEST` and `PRODUCTION`.  The driver must:

1. pin producer/checker/fixture and all three external source/checker files;
2. reject stale outputs and unsafe input paths;
3. run the full v3 checker on the original receipt and require its exact one
   positive line;
4. run adapter prepare;
5. run the full v2 checker on the compatible receipt and require its exact
   one positive line;
6. finalize the certificate;
7. run the independent adapter checker;
8. compare exact producer/checker terminals; and
9. write a nonempty sentinel only after every gate passes.

The final artifact must make `task193_compatible_v2.json` directly usable at
task193's existing `--task186-receipt` interface, with the emitted v2 checker
attestation directly usable at `--task186-attestation`.

The reply processes Sections 1--7 in order, gives exact identities and a
conservative GHA estimate, and ends with:

```text
TASK192-v3 POSITIVE INPUT:                    REQUIRED / NOT YET SUPPLIED
LOSSLESS v3 -> v2 COMPATIBILITY ADAPTER:      NOT EXECUTED BY LUNA
FULL v3 CHECKER ATTESTATION:                  NOT EXECUTED BY LUNA
FULL v2 CHECKER ATTESTATION:                  NOT EXECUTED BY LUNA
TASK193-COMPATIBLE RECEIPT:                   NOT PRODUCED BY LUNA
ACTUAL TASK193 beta1 / FIRST MULTIPLIER:       NOT EXECUTED
COMPATIBLE COFINAL LIFT / FAKE / IHARA:       NOT DECLARED
```
