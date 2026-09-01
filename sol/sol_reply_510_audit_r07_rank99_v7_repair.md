# Task510 independent Sol(max) audit — rank-99 v7 repair

## Verdict

`GO_FOR_GHA_DISPATCH`

I audited only the frozen Task510 boundary with bounded static, fixture,
mutation, pin, and parse checks.  I did not run production, GHA, git, or an
unbounded search, and I made no implementation change.

## Frozen pins

- v431 proof: 9,592 bytes,
  `7b08f2526b00f4b12e67b9de57e03b7e87936050bfe8c3f9200130ed1ef850a4`
- Task507 audit: 7,164 bytes,
  `741c5be74245e1944ce497a2fdd101b099b57d580f12ab96577f07074546ccdb`
- Task508 audit: 13,720 bytes,
  `dd4900afa9b212cc6b1c5379003015ac7ae4669a9abc7b493f00de4dd48366ee`
- v7 producer: 4,911 bytes,
  `a66526af4b4f86019b1a4a9283212b9782f5793a21c518a93f04b9925e6bee22`
- v7 checker: 9,067 bytes,
  `8de4f573a8a00da451c9518bbc87eb77c1c8cebfb2477ce38efb51e0e01c14f8`
- v7 GHA driver: 9,800 bytes,
  `fd355c0428f95332c3c822e47b0e2368bfc07cbe4372c47a33fd1ebe24d5d8b7`
- Task509 implementation reply: 2,556 bytes,
  `14fe9c4cec2b0a1bb55c990362dce6b1ad392d8acefde8ccd7995f2c04a5475c`

The producer and checker independently obtain the same current durable
binding:

`b679d6b91f3b2cba0b4105b3b5b028c0ec694cb87079833a1617aeff5ad539e3`.

I also recomputed all driver dependency pins for C99, rank51, Task451
producer/checker, and v424/v426/v427; every advertised byte/hash pair matched.

## Bounded checks run

- Producer `--mode FIXTURE`: PASS, including the executed dictionary
  presentation loop and zero/one selective-runtime construction counts.
- Checker `--self-test`: PASS; checker `--pin-check`: PASS.
- Independent AST compilation of both Python subjects: PASS.
- Imported-code/disassembly harness: PASS.  The executable `run` contains no
  `LOAD_ATTR relators`; its live loop uses two `BINARY_SUBSCR` operations for
  `P["pres"]["relators"]`.  After `replay_all`, bytecode branches on `sf is
  None`: the None arm calls `selective_runtime` once and the non-None arm loads
  `sf.rt` without construction.
- Independent zero-scalar live-helper harness:
  `TASK510_F2_ZERO_BEFORE_HIT_AND_EXHAUST_PASS`.  Cursor 0 returned `None`
  before physical insertion, cursor 1 retained the first actual rise, and an
  all-zero `0..W` schedule reached only
  `UNKNOWN:GLOBAL_SELECTOR_INVARIANT` after exhaustion.
- Independent binding harness:
  `TASK510_F3_INDEPENDENT_BINDING_PASS`.  Removing v431 changes the binding.
- Independent fully re-sealed mutation harness:
  `TASK510_F4_FULLY_RESEALED_W_MUTATION_REJECT_PASS`.  I changed record W,
  cursor W, and `global_cursor`, then recomputed the row-containing rolling
  prefix, segment ledger, end core, and top state seal.  The mutated state
  passed the exact structural closed-state validator and was then rejected by
  the live checker with `global:W_recompute`.
- Independent support/global batch harness:
  `TASK510_F5_SUPPORT_K0_LATER_K1_AND_GLOBAL_SOLE_PASS`.
- Independent legacy harness:
  `TASK510_F6_EXACT_V5_MIGRATION_PASS
  ['binding','schema','state_sha256']`.  Both producer and checker first
  authenticated the frozen v5 state; all non-top-level historical fields were
  equal after migration.
- GAP `ReadAsFunction` parse of the frozen driver: PASS (only expected unbound
  global warnings from parsing a driver body without executing its preamble).

## Findings F1–F8

### F1 — PASS

The production executable, not only fixture prose, uses the dictionary
presentation ABI.  `run` is the patched retained owner function.  Its
post-replay branch reuses the authenticated `sf` and assigns `runtime = sf.rt`;
only a genuinely absent `sf` calls `m.selective_runtime`.  This removes the
second full selective-store construction.

### F2 — PASS

The live `_retain_global` returns `None` for scalar 0 before occurrence-row or
physical work.  The enclosing compiled loop still scans exactly `range(W+1)`,
retains the first later nonzero actual rise, and raises the invariant only if
the entire schedule misses.  The action-first branch is inherited unchanged,
and the zero-K support branch remains reachable.

### F3 — PASS

Both public pin maps expose the exact v431 pin.  The producer extends its
durable binding body with that pin; the checker constructs its own binding body
from its independently pinned constants and file checks.  Their binding values
agree, and the remove-v431 mutation proves that the theorem pin is not dead.

### F4 — PASS

The checker recompiles the selected formula and computes W from live
`sf.kernel_orders`, once for every `(coordinate,target)` key in `merged`, so
distinct targets at the same coordinate retain multiplicity.  The independent
harness obtained W=27 for two coordinate-0 targets and one coordinate-2
target.  Coordinates are restricted to 0..2, each used kernel order must be 9,
and the exact bound is enforced.  Cursor W, record W, and `global_cursor` are
all independently bound.  The fully coordinated/re-sealed mutation described
above still failed for mathematical mismatch.

### F5 — PASS

An actual support replay selected from formula K=0 passed with a later K=1
formula present.  Selecting the K=1 support formula failed with
`batch:selected_K`.  Two global rows fail `batch:multiple_global`; global plus
support or action fails `batch:global_sole_row`.  The inherited typed cursor
ordering and fresh-anchor gates remain in the executed base replay, while the
new wrapper only strengthens the one-row global boundary.

### F6 — PASS

Migration calls the frozen v5 validator before rewriting anything.  The only
changed keys are exactly `schema`, `binding`, and `state_sha256`.  Prefix rows,
batches, segments, ledger, input identities, ready core, profiles, ranks, and
counters are unchanged; current producer and checker validators both accept
the migrated state.  No historical row is recompiled.

### F7 — PASS

The driver checks the exact producer/checker, v431, C99, rank51, Task451, and
v424/v426/v427 pins; rejects unsafe/noncanonical input and stale fixed outputs;
uses `set -euo pipefail`; runs one producer; and admits exactly one terminal
line, either `COMMON_CANDIDATE` or `UNKNOWN_RESOURCE`.  Plain UNKNOWN, ERROR,
and Traceback cannot satisfy that terminal gate.

COMMON alone invokes the v7 checker once with 5,400 seconds, requires its exact
one-line PASS plus nonempty verdict, writes COMPLETE, and GAP re-reads the
owned OK sentinel.  RESOURCE invokes no same-job full checker, requires fresh
nonempty receipt/checkpoint, the discovery resource marker/mode, a 64-hex
state-seal shape, and all five A0/COMMON/NONMEMBER/fake/Ihara flags false; it
writes only the owned RESOURCE sentinel and never COMPLETE/COMMON.

This RESOURCE decision uses the commissioned candidate-transport boundary:
the exact pinned producer is the sole writer of both previously nonexistent
fixed output paths in the one pipefail-guarded run.  An arbitrary counterfeit
file manually substituted outside that ownership boundary is not a reachable
driver result and is not a Task510 STOP.  This matches the audited v5 RESOURCE
structure (v5 driver lines 86–96); v7 lines 97–111 retain it and add the five
explicit false-claim gates.  Full semantic checkpoint authentication remains
mandatory at later resume/adoption, not as a duplicate same-job RESOURCE
checker.

The generated shell is syntax-checked and then actually executed.  No fixture,
self-test, or checker path precedes or duplicates production work.

### F8 — PASS

The registered margins remain strict:
`14040 < 14220 < 14400` seconds and
`4200000000 < 4500000000 < 5120000000` bytes.  There is one producer and only
the conditional one checker.  The retained `sf.rt` removes the blocking
duplicate selective-store build.  The extra pinned-v5 module load used solely
to expose the bounded fixture ABI is a small import-time cosmetic cost and
does not construct a physical/selective store; I found no remaining blocking
copy or traversal regression.

## Mathematical and claim boundary

Mathematics does not change in Task510.  The v431 nonzero-constant global-prefix
argument and its Task507 audit remain the mathematical boundary; v7 repairs
runtime ABI, replay independence, durable migration, and transport enforcement.
No bounded audit result is a negative certificate, compatible lift, fake or
Ihara witness, or current COMMON word.  RESOURCE states carry all five claims
false.  A mathematical COMMON claim still requires the independent v7 checker
PASS on the COMMON branch.

TASK510_R07_RANK99_V7_REPAIR_AUDIT_GO
