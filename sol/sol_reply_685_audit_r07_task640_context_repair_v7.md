# Sol(max) Task685 — Task640 Context repair v7 audit

## Verdict

The Task683 delta is exactly the required Context-field repair plus its live
regression fixture, and the inert v7 workflow preserves the released v6
contract.  No context/source-hash/workflow blocker remains.

`verified=false`.  The v220 numerator is unchanged: first-rung grades remain
`1/6` and A0 actual remains `0/1`.  No code, GHA, git state, production replay,
or mathematics was changed or run.

## Exact audited files

| path | bytes | LF lines | SHA-256 |
|---|---:|---:|---|
| producer | `27899` | `312` | `684c629eef8100175b676a4e4762db18f67e5a99672b4107facc7dad412acfc2` |
| independent checker | `92071` | `1563` | `889b7c7753e53e9c73c5edd575443446b0e3051794d6f20356809244c57cbd32` |
| released v6 workflow | `10167` | `160` | `56f3df0a23a75165a8576af09fd794ab2f80535780c7cf957d4c383100385120` |
| inert v7 workflow | `10178` | `160` | `b93ad9dcd1bb48b84cd60f25b0597785214d820f3ad2b2b2d98588a41469afd3` |
| grade1-v4 source inspected | `144552` | `3326` | `1fb4b29691f448782e7f7f2e2282e7067282bc619fb34b7214089c5a73e24dc4` |
| Task683 task | `2336` | `51` | `a191805b4e02587436e2d2075b68a39a31fd688087e147bd8ca326a8cb48d129` |
| Task683 reply | `1339` | `32` | `48b5feeaa3fb61132ada06a88bf569a029f31e46206823be905b7e8e9d01e584` |
| Root Task684 result | `1416` | `37` | `7dfd547e336c520ad85ca47df14783b662a79762a40de1e4b4abaed30c1e3391` |

The producer and checker paths are respectively
`search/d972_r07_a0_fresh_precision2_endpoint_signature_v3.py` and
`search/check_d972_r07_a0_fresh_precision2_endpoint_signature_v3.py`.

## Context field and exact source delta

The inspected grade1-v4 `Context` assigns `self.physical_shifts` at lines
310--317 as a six-entry tuple of affine values and assigns the required
six-entry `aggregate_table` at line 318.  It defines
`source_word_tags(...) -> tuple[Affine,...]` at lines 333--334.  It does not
assign or define a field named `shifts`.

The repaired producer has exactly these direct `context.*` accesses:

```text
aggregate_table
physical_shifts
source_word_tags
```

All three exist on grade1-v4 `Context` with the required types.  There are
zero `context.shifts` occurrences and exactly one
`context.physical_shifts` occurrence in the producer.

`first_six_shift_gate` at producer lines 211--212 compares the six actual
`physical_shifts` against the independently reconstructed expected tuple.
Production `evaluate` calls that helper at line 221.  The selftest's
`ShiftFixture` at lines 290--295 exposes `physical_shifts` and deliberately has
no `shifts`; its good value passes and its one-entry mismatch raises
`first_six_prefix_table`.  Reverting the helper to the old name would raise an
uncaught `AttributeError` on the good fixture and red-light the selftest;
changing the value is covered by the live mismatch.

I reversed only the declared Task683 edits in memory:

- remove the two-line helper;
- restore the production line using the stale `context.shifts`;
- remove the six fixture lines and its result counter.

The result is exactly `27474` bytes / `304` LF lines with SHA-256
`060202458e8643acb1ed42d2ad94b9f192406c57b803dc7f3b07897c39115ef7`,
the producer pinned and executed by v6.  Its census contains exactly one stale
`context.shifts` reference.  This byte identity proves that no other producer
delta is hidden in Task683.

## Independent checker boundary

The checker remains byte-identical to the v6-audited checker at SHA-256
`889b7c7753e53e9c73c5edd575443446b0e3051794d6f20356809244c57cbd32`.
Its independent local `Context` intentionally assigns `self.shifts` at lines
872--875, and its independent aggregation uses `context.shifts` at line 1109.
That field is valid for that class and must not be renamed.  Task683 did not
change it.

## Workflow delta and release operation

I normalized v7's mechanical `v7` labels to `v6` and normalized its inert job
condition to the released v6 event predicate.  The complete remaining diff is
one line:

```diff
-  PRODUCER_SHA256: "060202458e8643acb1ed42d2ad94b9f192406c57b803dc7f3b07897c39115ef7"
+  PRODUCER_SHA256: "684c629eef8100175b676a4e4762db18f67e5a99672b4107facc7dad412acfc2"
```

Replacing that repaired producer hash as well makes normalized v7
byte-identical to the released v6 file: `10167` bytes and SHA-256
`56f3df0a23a75165a8576af09fd794ab2f80535780c7cf957d4c383100385120`.
The v7 producer pin equals the actual repaired producer hash.

Consequently all nonmechanical v6 data are intact: Task625 accumulated cap,
run/attempt/job/head/workflow and artifact metadata checks; Task554 and Task595
downloads; the nested Task625 path; the post-`cmp` copies of both
`task625-verdict.json` and `task625-replayed-verdict.json`; checker, reply and
prebuild hashes; Task640 time/RSS/durable/path/trie/state/record caps; the
120-minute job timeout, both 45-minute process timeouts, and 8-GiB virtual
guard; all seven 40-hex action pins; success-only residual upload; and
always-run log upload.  Only workflow/self/fire/authentication/artifact labels
changed mechanically from v6 to v7.

PyYAML safe parsing finds the single `fresh-endpoint` job.  Its condition is
exactly

```text
${{ false && (github.event_name == 'workflow_dispatch' ||
contains(github.event.head_commit.message,
'[fire-fresh-precision2-endpoint-v7]')) }}
```

and is unconditionally false.  Removing only the literal `false && ` leaves
the same parenthesized v7 dispatch/fire predicate and is the complete release
operation; no path, pin, cap, timeout, action, copy, or upload edit is needed.

## Bounded checks and claim boundary

- Serial external-cache `py_compile`: producer and checker PASS.
- Producer `--selftest`: PASS with `first_six_shift_mutations=1`.
- Checker `--selftest`: PASS with its existing `mutation_count=43`.
- AST Context census: PASS; no missing direct producer attribute/method.
- Normalized source reconstruction and v6/v7 byte comparison: PASS.
- Safe YAML parse, one-job inert condition, and seven full action pins: PASS.

This is only the requested context-field/source-hash/workflow release audit.
It does not re-adjudicate Task640 mathematics, accept a rho2 artifact, or make
an A0/fake/Ihara claim.

PASS_CONTEXT_ONLY / SAFE_TO_DISPATCH_GHA=yes
