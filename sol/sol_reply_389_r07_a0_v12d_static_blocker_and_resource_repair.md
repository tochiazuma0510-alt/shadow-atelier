# RUNNABLE RESEARCH HOTFIX / RESULT-SPECIFIC PROMOTION REQUIRED

## Scope disposition

The researcher superseded the original seven-defect/full-six-owner task during
implementation with a minimal runnable-hotfix checkpoint.  This delivery
therefore repairs only D1 and D2, versions the two executable owners and their
driver, and deliberately reuses the frozen v12c P0, fixture, schemas and output
names.  It is not the full task389 repair and is not promoted merely from its
source text.  D3--D7 and new v12d P0/fixture construction are deferred.  A
clean successful GHA result may nevertheless be promoted after a separate
result-specific audit establishes producer/checker agreement, physical
artifact identity and absence of stale-output admission on that trace.

The root broker committed and pushed this hotfix as
`1dfb9f6684c1e5c8e7b001b8b110c14ac67247e7` and dispatched GHA run
`33241458432`.  That first broker run stopped before candidate execution
because its required explicit mode preamble was omitted.  Root immediately
redispatched the same commit with the exact `SELFTEST_BOOTSTRAP` binding as run
`33241570468`; it entered the running state.  This implementer did not run or
observe either candidate; no mathematical result is claimed here.  The
two-layer A0 plan uses this D1/D2-only runnable
checkpoint to obtain the mathematical result first, while D3--D7 remain a
separate operational-hardening layer and do not automatically veto promotion
of an independently audited clean successful trace.

## Static repair delta

- D1, checker lines 2397--2439 and 2615--2618: `K0CoordinateStore` now receives
  the one live `CheckerMeter`; `put` has valid loop indentation and both build
  and lookup probes use that same meter.  The builder requires the meter before
  reservation/allocation and passes it to the sole store.
- D2, producer lines 5210--5221: `producer_boundary_validate` binds `live` from
  its explicit runtime owner and requires callable `parse_sparse` and
  `public_sparse` interfaces before the unchanged baseline/mutation validation
  route uses them.
- Driver lines 6--7 and 35--36: only the producer/checker source paths and their
  exact physical byte/SHA-256 pins change.  All v12c P0/fixture/schema/output
  contracts remain unchanged.

Static forward/reverse comparison against v12c found only the additions and
replacements above.  No mathematical, Q0/K0/Gamma, mutation-ledger, P0,
fixture, deadline, resource, publication or artifact-helper route was changed.

## Physical identities

- producer v12d: 342850 bytes;
  `cd78b2c7d38da9a18e636a2917880c135329501b8e5af1aa9fb3dd7a9a46a628`
- checker v12d: 298456 bytes;
  `4d4750162af04cd4961e5872c9538ef13723e6d6635361568f6487a94ed35046`
- driver v12d: 43559 bytes;
  `4a350c661a52e4fe57428910c509016aa86b7d7d44b62db86f72afcffe554850`
- reused frozen P0 v12c: 11476 bytes;
  `24fbc1f9d7a7be3c96e1a56d4eb97d0aa5ccca9233f1e552088e9848bc081d74`
- reused frozen fixture v12c: 22785 bytes;
  `6fb7fe92c3cf93f54e44f9f26c3e920d131dbc626fc826d8b5bb4745bf67c8ec`

No Python, Node, GAP, GHA, workflow, git, network, import, syntax/compile,
candidate, mutation, subprocess or RSS execution was performed.  Read-only
PowerShell inspection, line comparison and SHA-256 hashing only were used.

A0/V12D VERSIONED OWNERS:                INCOMPLETE
TASK385 F1 CANONICAL GRAPH:               RETAINED
D1 CHECKER K0 ROUTE:                      REPAIRED
D2 PRODUCER BOUNDARY ROUTE:               REPAIRED
D3 DUPLICATE TRANSLATED-PAIR WORK:        OPEN
D4 BOOTSTRAP-THROUGH-ROLLBACK DEADLINE:   OPEN
D5 EXACT SHARED RESOURCE LEDGER:          OPEN
D6 R/V TERMINAL ROLLBACK:                 OPEN
D7 NO POST-HELPER GAP EDGE:               OPEN
TASK376 MATHEMATICAL SEMANTICS:           RETAINED
CANDIDATE EXECUTION:                      GHA RUN 33241570468 IN PROGRESS
FRESH RESULT-SPECIFIC AUDIT:              REQUIRED FOR PROMOTION
V12D SELFTEST_BOOTSTRAP GHA:              IN PROGRESS
PRODUCTION / RESUME:                      FORBIDDEN
ACTUAL A0 COMMON + CHECKER:               remains 0/1
LIFT / FAKE / IHARA:                      NONE

TASK389_R07_A0_V12D_STATIC_BLOCKER_AND_RESOURCE_REPAIR
