# Luna task 172: R07 full-E4 orbit preflight repair v2

Date: 2026-08-27
Role: Luna / bounded implementation and adversarial mechanical audit only

## 1. Why v2 is required

Read completely:

- `sol/luna_task_171_r07_full_e4_joint_orbit_preflight_v1.md`;
- all four task-171 v1 outputs;
- `sol/proof_r07_full_e4_joint_orbit_selector_v109.md`;
- `sol/proof_r07_full_e4_seven_evaluation_orbit_selector_v110.md`; and
- the task-157ee/157ef and 157eg--157en sources, replies and full artifact
  directories.

The Sol audit rejects promotion of the v1 checker result.  Two defects are
load-bearing:

1. the toy producer sets `equality = image == image`, while neither route
   enumerates the image of an actual kernel under an actual cocycle; and
2. the v1 mutation statuses are fixed strings rather than executions which
   alter inputs and observe validator rejection.

The v1 `UNKNOWN_INPUT` inventory is also incomplete.  In particular the
following authenticated artifact was present but not read:

```text
ci/b345_157ee_artifacts_32359956713/d972_b345_q3_chief_v1.json
SHA-256 3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72
```

Its `correction_fibre.records[].word` field contains the identity plus all
26 nonempty signed F2 record words.  The frozen 157ee producer itself reads
them at lines 953--966.  Thus `MISSING_RECORD_WORDS` is refuted as an input
blocker.

The same source chain already exposes the other purportedly missing objects:

- 157ee `run`, lines 944--950, calls `authenticated_input`,
  `reconstruct_quotients`, and `cheap_context_registry`, producing typed
  `e3`, `e4`, 31 contexts and 46 aliases;
- 157en `base_raw_columns`, lines 1921--1929, computes the eleven raw
  full-E4 PB4 Fox columns; and
- 157en lines 1932--1974 compare direct translated sparse rows with typed
  full-E4 translations.

V2 must use those authenticated paths or identify a narrower callable-level
failure.  It may not repeat the v1 generic missing-data strings.

## 2. Authorized outputs and noninterference

Create only new versioned files:

```text
search/d972_r07_full_e4_joint_orbit_preflight_v2.py
crosscheck/check_d972_r07_full_e4_joint_orbit_preflight_v2.py
search/certs/d972_r07_full_e4_joint_orbit_preflight_v2_20260827.json
sol/luna_reply_172_r07_full_e4_orbit_preflight_repair_v2.md
```

Do not modify or delete the v1 outputs, v108--v110, task169 or its assets,
157ee--157en, workflows, CLAIMS, or any existing certificate.  No git, push,
GHA dispatch, full correction-orbit enumeration, full D2 prefix build,
parallel Python/GAP, or credential access.  Use bounded serial processes and
a clean TEMP overlay.  Do not run the expensive 362,725-column prefix.

## 3. Authenticated raw-input bridge

Pin every file used by path, byte count and SHA-256.  Reconstruct from the
full 157ee q3 artifact and the exact predecessor source APIs:

1. typed `E4=Q4 x Pi4[3]`, including identity, multiplication, inverse,
   evaluation and canonical 154-byte blob;
2. all 26 nonempty signed F2 record words and their frozen digest
   `08d11c68dcbacc1b81e5e2732eedcbc41df82a16c8a0f97dfbbb13d6accee24f`;
3. the complete 6,318+104+19 expanded relation roster as actual signed F2
   words, retaining source layer and ordinal;
4. the three target6 full-E4 contexts and their exact bindings into the
   31-context/46-alias registry; and
5. the eleven raw full-E4 PB4 Fox rows through the `pure_relations(4)` and
   `fox_gradient_without_sections` route, requiring value identity and
   `D1=0` for each.

Do not build the historical fixed prefix merely to obtain these rows.  The
producer may import an authenticated predecessor module under a fresh module
name; the checker must reconstruct through a helper-nonshared path and must
not import the new producer.

Bind the fresh g760 word and SHA
`518f09820b8d7baee6b58ebf366cebf7b02a9a945cd1350cf8c701a4e6bc2b4d`.
Derive the target6 raw formula from the current g760 evaluator and the exact
three substitutions; do not inherit old20/616 target rows.  Record whether
the code convention is

```text
corrected_minus_base
```

or

```text
base_minus_corrected
```

and bind the sign by direct word comparison.  V110 uses
`corrected_minus_base`; an opposite executable convention is permitted only
when recorded explicitly.

## 4. Actual Fox conjugation and additivity canaries

Use a deterministic sample of at least 100 actual `(u,r)` pairs containing:

- every one of the three relation-roster layers;
- both source generators, inverses, products and several longer section
  words as conjugators;
- several relation lengths from each layer; and
- pairs `u,v` with the same ordered three-context full-E4 state, obtained by
  multiplying by actual joint-kernel words.

Compare literal sparse rows for

```text
Sigma_E(u*r*u^-1)
```

against the row obtained from the ordered context action on the three raw
Fox gradients of `r`.  Require literal equality of component, canonical E4
blob and coefficient.  Separately test additivity on products of actual
joint-kernel words.

Execute and reject real negative mutations of context order, left/right
action, fixed-prefix orientation, conjugator orientation, Fox inverse sign,
sparse-key component and serialized E4 blob.  A mutation count is evidence
only when a mutated object was passed to the same production validator and
raised the expected failure.

If a projected-kernel word distinguishing raw additivity is not found within
the registered bounded sample, retain
`PROJECTED_KERNEL_RAW_ADDITIVITY_UNKNOWN`; do not turn a bounded miss into a
theorem.

## 5. Genuine exhaustive toy theorem

Replace the v1 toy completely.  Use an explicit finite nonabelian marked
group `G`, a nontrivial finite F3-module `M` with a written `G` action, and
chosen generator cocycle values.  Enumerate the finite image of

```text
F2 -> (M semidirect G) x F3^2
```

by Cayley BFS.  The left side of v109 Theorem 3.1 is the complete identity-G
fibre projected to `(M,F3^2)`.  Compute it directly from that fibre.

Independently evaluate a complete finite normal presentation roster of `G`,
all of its `G`-conjugacy orbit columns under the same cocycle, and their F3
span.  Compare the two sets exactly.  Require an explicit example in which
the unconjugated relation rows span a strict subspace, so conjugation is
load-bearing.  The checker must use a different enumeration/order and derive
both sides independently; an equality of an object with itself is forbidden.

## 6. Real mutation harness and terminal

Run actual rejection tests for at least:

- source/artifact byte pin;
- one signed record-word letter;
- one relation layer/ordinal binding;
- one E4 multiplication or inverse result;
- one PB4 raw row coefficient;
- each Fox convention named in Section 4;
- toy action, cocycle generator value, normal relator and one missing orbit
  state; and
- every forbidden positive/global terminal.

The receipt records mutation id, altered semantic field and caught validator
message.  Hard-coded `PASS_*` strings without execution are prohibited.

If Sections 3--5 all pass, use terminal

```text
R07_FULL_E4_ORBIT_PREFLIGHT_READY
```

meaning only that a full target6 orbit GHA successor can be safely written.
Otherwise use a typed `UNKNOWN_INPUT` or `UNKNOWN_RESOURCE` and list the exact
callable/data edge.  No correction, literal A18, cofinal lift, fake or Ihara
witness is declared by this task.

## 7. Bounded run and report

Run producer and independent checker serially twice from clean overlays and
require a byte-identical certificate.  Report exact commands, outputs,
runtime/RSS, sample composition, row digests, mutation execution count and
all remaining UNKNOWNs.  Repeat verbatim:

```text
v1 toy/checker promotion rejected by Sol audit
full-E4 raw bridge and canaries are bounded preflight, not a correction
positive target6 at one universal relation-module layer is not literal A18
no cofinal lift / fake / Ihara witness declared
```
