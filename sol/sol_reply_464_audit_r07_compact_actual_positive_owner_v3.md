# Task464 adversarial audit — compact actual positive owner v3

## Verdict

**STOP / NOT ADOPTABLE / DO NOT DISPATCH.**

The 44-row specialization itself is the intended actual Task456 arithmetic,
not the rejected Task460 toy.  However, an actual MEMBER cannot traverse the
v3 driver/checker boundary.  There are three independent, deterministic
blockers.

## F1 — the driver rejects the producer's actual MEMBER terminal

The generated v3 producer retains the inherited terminal

```text
MEMBER = R07_ZERO_BASE_A5_A6_MEMBER
```

and therefore prints

```text
R07_COMPACT_DIRECT_RELATOR_A5_A6_POSITIVE_V3_PRODUCER_TERMINAL R07_ZERO_BASE_A5_A6_MEMBER
```

The driver strips the prefix into `p`, but its positive case accepts instead

```text
R07_COMPACT_DIRECT_RELATOR_A5_A6_POSITIVE_V3_MEMBER
```

Thus every real MEMBER exits in the first `case` and the independent checker
is never invoked.

**Exact repair:** minimally make the driver accept
`R07_ZERO_BASE_A5_A6_MEMBER`.  Alternatively rename the MEMBER ABI in both
producer and checker, but changing the inherited actual terminal is
unnecessary.  Add a static gate asserting that the producer `MEMBER`, checker
`MEMBER`, and driver positive case are the same literal.

## F2 — the checker does not pin the v3 producer

The generated v3 checker contains exactly

```text
PRODUCER_PIN = (
    "search/d972_r07_compact_direct_relator_a5_a6_positive_v2.py", 2018,
    "7a7272eb553d5256bdad2a123ad6cad87b171fb5d23c2e6d81b7702c5842f244")
```

The named v2 file is actually 7,707 bytes with SHA-256
`47cc53c0b59cbca0981983373d30604cbffd874cfa01d2d2adef599e505a21d3`.
The advertised 2,018-byte/hash pair belongs to the v3 file.  Consequently
`check_pin(PRODUCER_PIN, "producer:source")` must reject every MEMBER.

**Exact repair:** cardinality-guard the whole producer-pin tuple, including
the path, from v2 to v3.  Recompute and propagate the resulting checker
physical/generated pins and driver checker pin.  A bounded gate must compare
the complete tuple, not only the byte/hash variable names.

## F3 — producer and checker require incompatible Task193 verdict ABIs

The generated producer correctly requires

```text
d972-r07-second-frattini-affine-prefix-compiler/v5/checker-verdict/v5
```

but the generated checker requires

```text
d972-r07-second-frattini-affine-prefix-compiler/v5/checker-verdict/v3
```

The frozen Task193-v5 checker emits `/checker-verdict/v5`.  The driver passes
the same Task193 verdict to producer and checker, so no verdict can satisfy
both sides.  This arose because the broad two-occurrence replacement of
`/checker-verdict/v2` also rewrote `TASK193_CHECK_SCHEMA`, rather than only the
compact checker's own `CHECK_SCHEMA`.

**Exact repair:** use scoped, full-line transforms.  Advance only
`CHECK_SCHEMA = SCHEMA + "/checker-verdict/v2"` to v3, and explicitly restore
`TASK193_CHECK_SCHEMA = TASK193_SCHEMA + "/checker-verdict/v5"`.  Add a gate
requiring producer and checker Task193 schema/terminal/source pins to be
identical and equal to the frozen v5 ABI.

## Load-bearing parts that passed inspection

- All reported v2/v3 physical and generated-body byte/hash pins match the
  files presently in the tree.
- The producer and independent Task411 checker reconstructions each returned
  exactly 44 immutable word rows, with identical digest
  `7612682d024b61f873928ad122c9a5d7462c812a6633112f08706cda4412b6c8`.
- The producer fully constructs the original Task198 `AuthorityAdapter`,
  `Runtime`, and `BoundaryLedger` before creating the compact row view.  Only
  `DirectEngine` receives that view.  Its 44-seed loop retains the actual
  occurrence package, marked four-action closure, pointed target, translated
  PB boundary, proof DAG, and literal `M` expansion.  No Task460 synthetic
  coordinates, external target, assumed-empty PB ledger, or fake action edge
  is present.
- The checker reconstructs the 44 words through the pinned independent
  Task411 checker and retains independent Task198-v14 seed/action/target/PB
  replay and literal `M` comparison.  That replay is structurally present but
  unreachable until F1--F3 are repaired.
- The v3 producer inserts top-level `resumable=false` before its self seal on
  MEMBER, exhaustion, RESOURCE, and INPUT receipts.  There is no checkpoint,
  resume option, or state-file route.  Every nonpositive producer receipt has
  the exact six-field NONE/false frontier, and the driver parses and compares
  that complete frontier.
- The driver contains one producer invocation, the frozen 14,400-second and
  5,700,000,000-byte in-process caps, and a syntactic MEMBER-only checker
  branch.  Its generated shell uses `set -euo pipefail`, so direct producer,
  checker, pin, and JSON-assertion nonzero exits propagate.  It has no
  external `timeout`/RSS watchdog; this audit does not treat that as a new
  Task464 blocker because the commission expressly preserves the inherited
  in-process cap contract.  Any workflow claiming a hard process deadline
  must supply its own guarded watchdog.
- No old 6,441-row seed traversal, v2 production, synthetic MEMBER, GHA run,
  checkpoint replay, or other expensive mathematical run was performed.

After F1--F3, rerun the permitted load-without-main/pin/44-row gates plus the
three new ABI-consistency assertions.  Production and GHA remain unexecuted;
no MEMBER, lift, fake, or Ihara result is established by Task464.
