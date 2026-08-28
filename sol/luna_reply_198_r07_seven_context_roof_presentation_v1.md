# Luna reply 198d -- repair handoff after Sol212 STOP

The Sol212 repair series changed only the five task198-authorized files. This
follow-up changed only the driver and this designated reply. I did not run
Python, GAP, Node, git, GHA, or a network command; my checks were PowerShell
read-only/static checks. External GHA SELFTEST run `33132138219` at immutable
head `a79f425cfb5fb79b377231ae314c68bd3c7b3b50` reached only the driver and
stopped before producer launch because a production-only
`ci/in` receipt was pinned unconditionally. This is a repair handoff, not a
self-issued PASS and not a mathematical result.

## 1. Scope, proof contract, and dependency cone

Authorized files:

```text
search/d972_r07_seven_context_roof_presentation_v1.py
crosscheck/check_d972_r07_seven_context_roof_presentation_v1.py
search/d972_r07_seven_context_roof_presentation_gha_driver_v1.g
search/certs/d972_r07_seven_context_roof_presentation_selftest_v1_20260828.json
sol/luna_reply_198_r07_seven_context_roof_presentation_v1.md
```

Producer, checker, and driver retain the governing v145, v168, v173, and v184
pins required by original task198, together with v125/v188/v189/v190 and the
task198/task198b commissions. The complete final task175/task176/task179
producer/checker dependency cone remains a direct, path-sorted, duplicate-free
43-member manifest in both Python files and a direct 43-row table in the
driver. Its six roots are task175 producer/checker, task176 producer/checker,
and task179 producer/checker. Static comparison found both Python manifests
identical and all 43 declared byte/SHA identities equal to their current files;
the independently ordered driver table also has 43 current matching members.

## 2. One resource meter and early presentation preflight

`make_production` now performs a check-only `presentation_rows` reservation for
the complete workload (6,441 in production, 9 in linked SELFTEST) immediately
after optional resume authentication and before source authentication,
predecessor module loading, group construction, or roster reconstruction. The
normal row materializer remains the sole live `presentation_rows` charge, so
the reservation is not double-counted.

The existing Q0/fine-deletion/Gamma known-work preflights remain on the same
producer `Budget`; predecessor construction receives that meter, and completed
known extents are charged once. The independent checker likewise performs its
6,441-row check before loading its predecessor reconstruction and keeps Q0,
fine deletion, bridge replay, receipt/file reads, wall time, and RSS on one
global checker meter. No wall-only task176 budget is introduced.

## 3. Portable resource-stop continuation

Checkpoint schema remains `/checkpoint/v3`. The incompatible portable sidecar
is now `/resume-manifest/v2`. A resource stop that has authenticated checkpoint
state writes two current-run artifacts under `ci/out`:

```text
ci/out/d972_r07_seven_context_roof_presentation_resume_v1.checkpoint.json
ci/out/d972_r07_seven_context_roof_presentation_resume_v1.manifest.json
```

The manifest deliberately does not name the current `ci/out` checkpoint. It
binds its bytes, SHA, seal, row cursor, and bridge cursor to the fixed name that
the same artifact pair must have after staging for the next run:

```text
ci/in/d972_r07_seven_context_roof_presentation_resume_v1.checkpoint.json
```

The terminal envelope retains both the current checkpoint binding and the
portable manifest binding, including the future checkpoint path. Producer CLI
arguments `--checkpoint-manifest-output` and `--future-resume-checkpoint` make
the output/staging ABI explicit. A checkpoint output requires the full triple;
path aliases and stale current outputs are rejected. If no authenticated
checkpoint can be written, neither sidecar is emitted.

`load_resume` still requires the checkpoint and manifest as a pair, canonical
JSON, exact keysets, self/seal digests, and exact byte/SHA/seal/cursor agreement.
It records the full staged checkpoint and manifest identities in `resumed_from`,
then the shared materializer and full-word evaluator replay the entire stored
prefix before continuation. The independent checker reopens and authenticates
the same staged pair and independently reconstructs the row and bridge prefix.

## 4. Production-shaped SELFTEST continuation

The linked SELFTEST uses `make_production`, `Budget`, `load_resume`,
`write_checkpoint`, portable manifest writing, the shared row materializer,
the shared full-word bridge evaluator, and the normal terminal envelope.

Its chain is now:

```text
P0: presentation_rows cap 0
    -> presentation_roster_preflight UNKNOWN_RESOURCE, all work counters zero,
       no checkpoint and no manifest

P4: presentation_rows cap 4
    -> presentation_roster_preflight UNKNOWN_RESOURCE, all work counters zero,
       no checkpoint and no manifest

A:  presentation_rows cap 9, gamma_operations cap 4
    -> current-output checkpoint cursor 4 / bridge cursor 0 plus manifest
    -> byte-for-byte copy to fixed staged checkpoint/manifest names

B:  authenticate the staged A pair, replay its prefix, gamma cap 11
    -> current-output checkpoint cursor 9 / bridge cursor 2 plus manifest
    -> byte-for-byte copy to a second fixed staged pair

C:  authenticate the staged B pair, replay both prefixes, and continue through
    the complete linked receipt
```

Thus caps 0 and 4 prove that the known full row workload stops before even the
toy Q0/group construction, while A and B exercise real checkpoint continuation.
The producer itself performs current-output -> staged-pair -> next-run
reauthentication. The checker separately reads both current and staged copies,
requires byte identity, validates the portable manifest against the staged
checkpoint name, and reauthenticates both `resumed_from` links. Fixture schema
is now v4 and records the two preflight limits and two portable stages.

## 5. Genuine Dic3 maps and the executable v188 ABI

The ten toy coordinates are now genuine `Dic_3` automorphisms

```text
a |-> a^u,  b |-> a^v b,
u=1, v=0..5; then u=-1 mod 6, v=0..3.
```

Coordinate zero is the identity. Producer and checker independently enumerate
all twelve normal forms `a^i` and `a^i b`, require each coordinate map to have
twelve distinct images, and require the ten-coordinate joint image to have
exactly twelve distinct values. Every complete toy presentation relator is
evaluated by the actual ten-coordinate word evaluator and must decode to the
identity in every coordinate.

Each of the seven block signatures hashes only ordered `(x_image,y_image)`
value pairs. Coordinate indices, block indices, and receipt tags are excluded
from the signature input; actual normalized value blocks, not merely their
hashes, must also be seven distinct objects.

The live v188 eval/multiply/inverse/source-section/action/cocycle ABI remains
exported. The non-split `y,y` section cocycle is computed using the canonical
quotient-product section, is nonidentity, and must occur in the same twelve-
value joint coordinate image. Producer and checker serialize/reconstruct the
exact twelve normal forms, their ten-coordinate values, and the cocycle's
normal-form index independently. Production-only fields remain explicitly
null where the toy witness is inapplicable.

## 6. Independent checker and mutations

The checker does not import task198 producer helpers. It keeps its independent
row traversal/tie order, group law, coordinate evaluator, bridge operations,
section/cocycle implementation, order computation, and external file reads.
For a production `UNKNOWN_RESOURCE` with a checkpoint, it additionally requires
the fixed current output names, the fixed future staging name, exact portable
manifest identity, and checkpoint/terminal limit-counter agreement. Generic
resource terminals bind phase and cap limit to their resource snapshot; a
presentation preflight has the exact 6,441 target and zero prior work counters.

The mutation table remains 44 distinct controls. The terminal phase and cap
mutations now modify and reseal both duplicated real envelope locations
(`resource_terminals` and `resume_chain`) before validation, so they reach
semantic `UNKNOWN_RESOURCE` checks rather than duplicate-equality or digest
shortcuts. Value and limit controls act on the real preflight-four terminal and
make its `value > limit`/snapshot semantics false. Selected/kernel/order,
bridge sign/tag/prefix, row/Q0/DAG, resume/seal, resource, context-map, and
non-split controls remain present. No mutation run was performed this turn;
44/44 rejection remains a runtime gate, not a reported result.

## 7. Serial driver and sentinel boundary

The driver reads either both or neither fixed `ci/in` staged resume files and
passes the same pair to producer and checker. Its production command now also
passes the fixed current output checkpoint, current output manifest, and future
staging checkpoint names. The output checkpoint and manifest use the same
basenames as the next-run staged input, so artifact download need only place
the pair under `ci/in`; the v2 manifest already binds that future path.

Run `33132138219` exposed one driver input-scope error: the external task176
receipt `D198I` was inside unconditional `D198Pins`, although SELFTEST neither
stages nor consumes it. Its exact byte/SHA pin is now executed inside the
`PRODUCTION` branch immediately before the production-only task176 manifest
check. The unconditional bundle pins now contain checked-in task198/proof/
fixture/dependency files only. A static audit of every `ci/in` symbol found no
other external input action outside `PRODUCTION`: task176 receipt/manifest and
the optional checkpoint/manifest pair are all production-scoped. SELFTEST
still authenticates the full checked-in 43-member cone and current task198
producer/checker/fixture bundle.

All current-output sidecars and every SELFTEST output/staged/preflight path are
in the stale-output rejection list. Execution remains serial. A nonpositive
producer terminal makes the checker return nonzero, so no positive sentinel is
written. The declared 14,400-second and 8,000,000,000-byte values remain staged
one-process estimates/caps, not measurements.

## 8. Static audit and stable identities

PowerShell-only static checks found:

- producer/checker dependency cones: 43/43, exactly equal, sorted, unique;
- all 43 cone member byte/SHA identities: current, zero mismatches;
- driver dependency cone: 43, sorted, unique, zero identity mismatches;
- checker mutations: 44 names, 44 unique;
- unconditional driver pin table: zero `ci/in` members; all four external
  `ci/in` paths are consumed only in `PRODUCTION`;
- obsolete checkpoint-v2, resume-manifest-v1, fixture-v3, and
  `PROPER_QUOTIENT` terminal tokens absent;
- driver producer/checker/fixture pins equal the identities below.

Stable identities (the reply is intentionally reported out-of-band to avoid a
self-referential digest):

```text
producer  136938  292473d5f9d01827bb6971352a82b8f238be1b1a19a98002c575c8ebf39760ee
checker   153271  238eaa230b2ce1456e03780572c28b3fa71ae14786993e3dde056173886bed5a
driver     18994  4e0dc556a51581e3bc0f06d9cd478ff9689fa3f681080e770ad88ee714a827b5
fixture     1605  fb31f6a0be2f2f5b530c6fe99796476ea16edb72fe7ddc192323995f2ae55ce7
```

Execution boundary:

```text
GHA run 33132138219:                 PRE-PRODUCER DRIVER INPUT-SCOPE STOP
producer/checker in that run:        NOT STARTED
Python SELFTEST after this repair:    NOT RUN
GAP driver after this repair:        NOT RUN
production 6,441 reconstruction:     NOT RUN
independent production acceptance:   NOT RUN
mathematical lift/fake/Ihara result:  NOT DECLARED
```

Please send these exact five files to a new independent static auditor before
any runtime or mathematical claim is promoted.

## 9. Task220a — GAP `CreateDirectory` portability repair (2026-08-28)

The task-220a instruction was read in full. The only code change is the
replacement of unavailable `CreateDirectory("ci/out")` by the fixed-path,
quoted GAP `Exec("mkdir -p 'ci/out'")` mechanism, followed by an explicit
`OutputTextFile` failure check. This preserves the serial generated-shell
contract and fails closed if `ci/out` cannot be created or opened. No producer,
checker, fixture, workflow, proof, claim, or other file was modified.

Static byte/SHA identities after this repair:

```text
driver  19086  0751d13cdd6fc06837622c5c6cdf48f71fbbf71556a9d89bd6e044c23f23523d
reply   reported out-of-band after this append (self-referential digest avoided)
```

No Python, Node, GAP, git, GHA, network, producer, or checker execution was
performed by Luna. Parent Sol must rerun the GHA SELFTEST and obtain a new
independent audit.

TASK198 GAP DIRECTORY PORTABILITY: STATICALLY REPAIRED / GHA NOT RUN BY LUNA
TASK198 PRODUCER/CHECKER SELFTEST:  NOT EXECUTED BY LUNA
MATHEMATICAL ROOF BRIDGE:           NOT DECLARED

`TASK220A_TASK198_CREATEDIRECTORY_PORTABILITY_COMMISSIONED`

## 10. Task220a addendum — native GAP API correction (2026-08-28)

The prior §9 `Exec("mkdir -p ...")` repair was rejected by the additional
portability audit because local GAP 4.16.0 provides the native `CreateDir`
API. The driver now uses `IsDirectoryPath("ci/out")`, calls native
`CreateDir("ci/out")` only when needed, explicitly rejects `fail`, verifies
the resulting directory, and retains the `OutputTextFile` failure check.
No shell subprocess is used for directory creation.

Updated static identity:

```text
driver  19266  38b8d5efbf2694c59818f62df6d379113f1a8443c86d423f70e0cf464a394570
reply   reported out-of-band after this append (self-referential digest avoided)
```

Producer, checker, mathematics, and all runtime execution remain untouched;
Luna ran no Python, Node, GAP, git, GHA, or network command. Parent Sol must
rerun the GHA SELFTEST.

TASK220A NATIVE GAP DIRECTORY CORRECTION: STATICALLY REPAIRED / GHA NOT RUN BY LUNA
