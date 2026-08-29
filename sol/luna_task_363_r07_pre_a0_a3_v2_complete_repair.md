# Luna task 363 - pre-A0 A3 v2 complete authority/projection/resource repair

Role: Luna, bounded implementation only.  Read every numbered section from
first to last before editing.  Do not run Python, Node, GAP, GHA, a workflow,
git, network, or any candidate command.  Read-only PowerShell inspection and
hashing are allowed.  Use `apply_patch` for repository edits.

Task359/v1 is frozen and was rejected by the independent Sol(max) audit in
`sol/sol_reply_361_r07_task359_pre_a0_a3_code_performance_audit_v1.md`
(21,458 bytes, SHA-256
`2d4fc1a92f9ee4e68a879ab58b432c12b9ce3516141f38ea572803d5c424fdd2`).
No v1 owner may be edited or treated as accepted.  This task makes one
versioned v2 repair containing every F1--F7 correction together; it is not a
request for another partial wrapper or a fail-closed stub.

## 1. Binding prerequisites

Read in full, in this order:

1. `sol/luna_task_359_r07_pre_a0_single_target_a3_v1.md`;
2. all five frozen task359 outputs;
3. the complete task361 audit named above;
4. v302 and v303;
5. the accepted task198 receipt, acceptance manifest, both attestations,
   checker verdict, and all three source owners;
6. the current pinned task226 producer/checker and task227 producer/checker/
   driver; and
7. v220 deltas 38, 39, 123--126, 129 and 130.

Every mathematical and typing requirement of task359 Sections 4--8 remains
binding unless this repair explicitly strengthens it.  In particular the
computational base is not an A0 word, all H1/H2/P blocks stay disjoint, and
only the two accepted MEMBER/NONMEMBER terminals can support an A3 result.

## 2. Sole permitted outputs and execution boundary

Create only:

- `ci/in/d972_r07_pre_a0_single_target_a3_v2.prereg.v1.json`;
- `search/d972_r07_pre_a0_single_target_a3_v2.py`;
- `crosscheck/check_d972_r07_pre_a0_single_target_a3_v2.py`;
- `search/d972_r07_pre_a0_single_target_a3_gha_driver_v2.g`;
- `sol/luna_reply_363_r07_pre_a0_a3_v2_complete_repair.md`.

Do not edit v1, task198, task226, task227, a workflow, a proof file, v220, or
any other path.  Do not create a receipt or verdict.  V2 remains
`UNEXECUTED` until a fresh independent Sol(max) audit returns static PASS and
the parent dispatches GHA.

If the pinned task227 API genuinely cannot consume a sufficient pruned v303
interface, report `BLOCKED` with the first exact field access and do not feed
it the full task226 package under a projection label.

## 3. F1--F3: canonical preregistration and acyclic pins

P0 has schema `d972-r07-pre-a0-single-target-a3/v2/prereg/v1`.  Write it as
the exact compact sorted-key ASCII JSON byte string, with no BOM and no final
LF.  Its `self_digest_sha256` is the SHA-256 of the same canonical object
with exactly that top-level field removed.  Reparse the frozen bytes during
static construction and record the independently recomputed seal, byte count,
and physical SHA in the reply.

The graph remains acyclic:

```text
accepted task198 + v302/v303 + task226/task227 + g760 ancestry -> P0
P0 exact path/bytes/SHA/self-seal -> each new Python owner
P0 + final new Python bytes/SHA -> v2 GAP driver.
```

P0 must not pin a new v2 program or driver.  Both Python files must pin P0 by
path, exact bytes, full 64-hex physical SHA and self seal.  The driver must pin
P0 and both Python files with full 64-character SHA strings.  Reject wrong
length before comparison.  Do not preserve the rejected v1 P0 seal or any v1
program hash.

Both programs must establish this unmutated P0 baseline before dynamic import
or a mutation.  Their canonical-input predicate must accept the exact frozen
P0 bytes by construction; the reply must show the line-numbered predicate and
the final-byte audit.

## 4. Complete task198 authority and evaluator decoding

Retain the exact physical roster from task359, but close every omitted
semantic edge found in task361 Section 2.  Each side independently must
decode and require exact equality for:

1. `accepted_receipt_basename`;
2. every field of `producer.member` and `checker.member`, including basename,
   bytes and SHA;
3. both producer/checker attestation metadata records, including basename,
   bytes and SHA;
4. checker-verdict basename, bytes, SHA, schema, terminal, receipt terminal,
   `accepted=true` and `independent=true`;
5. every manifest run/head/artifact/zip/source-owner link and both manifest
   and receipt self seals; and
6. the complete exact evaluator ABI: schema/module/registry/runtime
   constructor, all ten coordinate widths, coordinate and relator digests,
   all six callable names with exact argument lists, encoding, multiplication,
   action and cocycle conventions, plus the literal eleven-row ledger.

Put the expected semantic contract in P0, derived from the frozen accepted
owners rather than from v1 labels.  A mere physical hash or existence of
`section_cocycle` is not enough.  Each side must exercise the decoded
evaluator contract through its ordinary base/central reconstruction.

Reserve the stat size before reading the 31-MB receipt.  Read and parse it
once per process.  Check canonical raw equality without allocating another
31-MB canonical byte string: use a bounded streaming canonical encoder and
compare its chunks against the retained raw bytes (also hashing/counting the
stream).  Release the raw buffer immediately after authority/ledger/evaluator
authentication and before constructing the new result.  The checker must not
overlap task198 raw bytes with the new production receipt DOM.

## 5. F4--F5: one sufficient projection and one closure input

Build the side-local task226 full base package only as
`BASE_REFERENCE_ONLY`, and replay every task359 g760, empty correction,
endpoint and v302 central/area canary.  Then construct a new explicit
`projected_a3_interface_v2` from an allowlist.  It must contain everything
needed to determine the task227 closure and nothing merely inherited from a
deep copy.  At minimum bind:

- the exact occurrence roster and all separate H1/H2/P types;
- every marked `q_o(x)` and `q_o(y)` image/action map for all eleven
  occurrences;
- every `p_o`, `xi_o`, `w_o`, `u0_o`, combined `w/u0`, target block and
  actor/orbit convention actually read by task227;
- the exact group/field/coordinate codecs and the v303 projection mode; and
- no `literals`, `rword_f`, `B_a`, exact PB-chain field, task192 ancestry, or
  other full-package-only value.

Statically trace every field read by the pinned task227 producer and checker.
From the explicit interface alone, construct a minimal `task227_consumer_abi`.
The load-bearing closure call must receive only this derived object; it may
not receive a deep copy of the full task226 ABI.  The checker independently
derives the same consumer ABI from its own projected interface.

For every projected or consumer ABI seal, remove any old
`self_digest_sha256` first, hash the canonical seal-stripped object, insert
the new seal, and immediately validate the untouched baseline.  Record
separate canonical digests for the explicit interface and consumer ABI.
The `ABI_seal_target` mutation occurs only after this baseline passes.

If task227 needs a field which v303 does not determine, stop as `BLOCKED` and
name it.  Do not silently import the excluded full-package field.

## 6. Exact closure evidence and genuinely independent checker

The producer calls the pinned task227 producer closure exactly once and
retains the complete occurrence ancestry, canonical 486 ideal rows, all 729
translates, block echelon/ranks, coefficients and four MEMBER replay rows or
the full NONMEMBER dual pairings required by task359.  No Boolean summary may
replace those objects.

The checker imports only the pinned independent task226/task227 checker
engines.  It invokes the task227 independent verifier once on the sufficient
consumer ABI and the physical producer gate.  Preserve its actual two-way
occurrence/block span comparison, exact 486/729 reconstruction, coefficient
replay and dual checks.  Do not add a second reversed call around a helper
which already checks both directions.  If the duplicate is internal to the
frozen task227 verifier, count and report it honestly; do not claim it was
removed without changing that frozen owner.

The checker verdict must require the complete producer
`false_conclusion_flags`, including `actual_a3_numerator=false` before an
accepted GHA result is promoted by the outer ledger.  Bind the receipt's
physical bytes/SHA, P0, all authority identities, projected-interface digest,
consumer-ABI digest, central replay digest, ranks, exact terminal and an
independently reconstructed result digest.

## 7. F6--F7: interruptible caps and honest accounting

Task359 forbids subprocesses and local parallelism.  Therefore bound the
meter-free task227 verifier in the checker process itself on the Linux GHA
target:

1. install a `signal.setitimer` wall deadline before the expensive call and
   restore/cancel it in `finally`;
2. install a conservative `resource.RLIMIT_AS` hard ceiling before dynamic
   imports/closure, treating `MemoryError` as `UNKNOWN_RESOURCE`;
3. sample RSS at all wrapper boundaries, but do not describe sampling as a
   hard in-call RSS interrupt; and
4. fail as `UNKNOWN_INPUT` before heavy work if the required Linux hard-cap
   APIs are unavailable.

The producer uses the same wall/address-space discipline in addition to the
pinned closure meter.  Use semantically honest counters.  In particular a
single opaque independent verifier call is one
`independent_verify_calls`, not zero fictional roster/action counts; do not
double-book one multiplication under two cap names.  Count the exact 486/729
sizes from the reconstructed accepted object after the bounded call.

Before every material read or known allocation, reserve from the relevant
cap using file stat or a conservative explicit bound.  This includes input
bytes, task226 builds, projected-area builds and output canonicalization.
Reserve an output maximum before serialization.  Compute the exact sealed
`serialized_bytes` by a bounded fixed-point serialization (the field is part
of the sealed telemetry), without charging repeated fixed-point passes as new
logical output.  The final sealed snapshot may not report zero serialization
after bytes were allocated.

Use workflow-feasible caps.  The accepted five-case task227 SELFTEST took 493
seconds.  Give a reasoned one-case producer/checker estimate; do not retain a
12-hour serial envelope.  The two external timeouts plus setup margin must be
strictly below the known six-hour workflow ceiling, and each external timeout
must strictly exceed its corresponding internal deadline.  Output caps must
be based on the accepted 4,636,766-byte five-case receipt rather than an
unmotivated 2-GB allowance.

## 8. Failure-atomic receipt/verdict and non-accepting UNKNOWN

Never open a final output path for incremental writing.  For every terminal,
serialize completely within the pre-reserved cap, create an exclusive temp
file in the same directory, write fully, flush and fsync it, then publish with
a no-overwrite same-filesystem operation, fsync the directory, and only then
print the one terminal.  Clean a failed temp best-effort.  There must be no
fallible acceptance work after final publication.

A failed normal attempt must leave the final path absent, so the small
pre-reserved emergency UNKNOWN constructor can publish independently without
recursing through the failed normal writer.  `MemoryError`, wall cap,
allocation cap and partial-temp I/O have narrow classifications.  A stale
pre-existing final owner always fails closed and is never overwritten.

Only

```text
R07_PRE_A0_A3_PROJECTED_MEMBER
R07_PRE_A0_A3_PROJECTED_NONMEMBER_DUAL
```

are accepting terminals.  `UNKNOWN_INPUT` and `UNKNOWN_RESOURCE` are
non-accepting: the driver must emit no PASS/ACCEPTED production sentinel and
must exit nonzero after printing a distinct diagnostic terminal.  Producer
and checker equality is necessary but not sufficient for acceptance.

## 9. Mutation baseline and exact expected reasons

Keep at least the twelve task359 glue mutations, but first run the complete
untouched cheap validator and require PASS.  P0 preregisters each mutation's
exact expected first reason.  Every mutation changes an extant independently
constructed authority/projection/central/conclusion owner, invokes the same
ordinary validator used by production, and compares the observed first
reason to the P0 value.  Never fill `expected_gate` from the caught exception.

The authority mutation must traverse the manifest-to-member/attestation/
verdict binding validator.  The ABI mutation must start from the now-valid
seal baseline.  Central and target mutations must traverse the actual replay
summary used by closure.  `MutationAccepted` and wrong-reason rejection stay
outside the narrow expected exception catch.  Producer and checker execute
their own rosters; copied producer records are not checker evidence.

## 10. Driver, static reply and final frontier

The ASCII GAP driver pins all four final owners, rejects stale output and
temp aliases, runs producer then checker serially with strict timeout margins,
hashes the receipt after production and injects that exact SHA into the
checker command with shell-safe quoting, and rehashes after checking.  It
requires exact-one full-line terminal on each side, exact accepted-terminal
equality, sealed nonempty receipt/verdict and all physical cross-bindings.
Only then may it print one v2 accepted sentinel.  UNKNOWN or any mismatch is
a failing run, not a driver PASS.

The reply gives exact bytes/SHA-256 of P0, producer, checker and driver; P0
self seal; the complete authority/import graph; the allowlisted projection
field trace; seal-stripped digest trace; exact mutation matrix; allocation,
wall/RSS/output formulas; one-case estimate; publication state machine; and
line-numbered evidence for every repair above.  State explicitly that no
candidate program or GHA was run.

End exactly with:

```text
V1 TASK359:                           STATIC REJECT / SUPERSEDED
V2 CANONICAL P0 + FULL PINS:          PASS or BLOCKED
TASK198 FULL AUTHORITY/EVALUATOR ABI: IMPLEMENTED or BLOCKED
SUFFICIENT V303-ONLY PROJECTION:      IMPLEMENTED or BLOCKED
ONE ACTUAL 486/729 CLOSURE ROUTE:     IMPLEMENTED or BLOCKED
INDEPENDENT BOUNDED MEMBER/CHECKER:   IMPLEMENTED or BLOCKED
BASELINE + GLUE MUTATIONS:            IMPLEMENTED or BLOCKED
FAILURE-ATOMIC PUBLICATION:           IMPLEMENTED or BLOCKED
SERIAL ACCEPTING-ONLY DRIVER:         IMPLEMENTED or BLOCKED
EXECUTION / GHA:                      UNEXECUTED
ACTUAL A3 NUMERATOR:                  remains 0/3 pending accepted run
A0 COMMON / POINTED / EXACT PB:       OPEN
COFINAL LIFT / FAKE / IHARA:          NONE
```

`TASK363_R07_PRE_A0_A3_V2_COMPLETE_REPAIR`
