# Luna task 509 - minimal rank99-v6 checker/driver repair

Role: Luna implementation only.  Do not run production/GHA, commit, push,
change mathematics, edit the v6 producer/checker/driver, or touch any output
other than the four files named below.

The Task506 v6 producer remains frozen exactly at:

```text
search/d972_r07_a0_dual_anchored_rank99_durable_discovery_v6.py
14329 3173c9d99fc5a94713d3dbed1b2c90d4ed3a5723b428838ec0bd50d8aee3d90c
```

Read Task506, paper v431, Task507 GO, and the completed Task508 STOP reply.
Repair only the enumerated acceptance-boundary defects while preserving the
v6 schema and producer marker.

## Required outputs

1. `search/d972_r07_a0_dual_anchored_rank99_durable_discovery_v7.py`
2. `crosscheck/check_d972_r07_a0_dual_anchored_rank99_durable_discovery_v7.py`
3. `search/d972_r07_a0_dual_anchored_rank99_durable_discovery_gha_driver_v7.g`
4. `sol/luna_reply_509_r07_rank99_v6_checker_driver_minimal_repair.md`

## Repair 0: actual production dict/attribute crash

Run `33553895281` completed with plain `UNKNOWN` and exact reason

```text
'dict' object has no attribute 'relators'
```

after rebuilding the selective Q0/S0/S1/S2 stores twice.  The exact live
defect is the transformed selector loop's

```python
zip(formulas, P["pres"].relators)
```

where the v424 adapter deliberately exposes `P["pres"]` as a dict and every
working formula/replay call uses `P["pres"]["relators"]`.  Make a versioned
v7 producer from the frozen v6 source and replace only the generated live-loop
expression with

```python
zip(formulas, P["pres"]["relators"])
```

Do not change the old source-anchor string that must still match frozen v5.
Preserve the v6 schema and terminal marker.  Strengthen the binding only as
required below to include v431; the new file is a code-bundle version, not a
checkpoint-schema rewrite.  Add a bounded production-shaped source-patch
fixture proving the executed transformed loop receives a dict presentation
and reaches the formula iteration without `AttributeError`.  A text-only
presence check is insufficient.

The same run log proves a second exact live inefficiency: the complete
`selective_Q0`, `selective_membership_S0`, `S1`, `S2` construction occurred
twice.  `replay_all(...)` already returns the authenticated `sf` built while
replaying the C99 correction prefix, but v5 line 1155 unconditionally discards
it with another `m.selective_runtime(...)` call.  In the transformed v7 live
run, reuse that returned object:

```python
if sf is None:
    runtime, sf = m.selective_runtime(P, p179, args)
else:
    runtime = sf.rt
P["runtime_selective"] = runtime
```

The replay path already clears only its candidate cache, not its authenticated
stores/kernel states.  Add a bounded call-count fixture proving a non-None
replay `sf` causes zero additional construction calls, while `None` causes
exactly one.  Do not rebuild/copy the Q0 stores.

## Repair A: independently recompute W

The checker must not accept a producer-supplied `W` merely because the same
value occurs in the record and typed cursor.  On the live global replay path,
after independently recompiling the selected formula and constructing its own
selective runtime, compute

```text
expected_W = sum(sf.kernel_orders[coordinate]
                 for coordinate,target in formula["merged"])
```

with target multiplicity.  Require all live coordinates in `{0,1,2}`, every
used order exactly nine on this frozen branch, `expected_W < 357128352`, and
both record/cursor W equal `expected_W`.  Do this in checker code independent
of producer helpers.

Add a bounded live-path mutation gate: a valid-shaped synthetic global record
or narrowly mocked call with a re-sealed/copy-consistent wrong W in both
record and cursor must be rejected specifically by the independent W check.
Do not substitute an AST/text-only assertion for execution of that gate.

The global scan must treat compiled scalar zero as an ordinary miss and
continue to the next cursor.  It must not raise `global:zero_scalar` before a
nonzero point is reached.  Only a retained record requires scalar in `{1,2}`.

When replaying an old support-fibre row in a mixed compiled roster, require
the row's independently selected formula to have `K==0`; do not require every
other formula in the batch anchor to have zero K.  Conversely, a global row
must be the sole row of its batch.  Reject two global rows and every
support/action/global mixed batch even if all row digests and seals are
recomputed consistently.

## Repair B: restore the audited v5 transport envelope

Restore the pinned v5 driver's live shell execution and transport boundary,
changing only the versioned paths, exact pins, binding/markers and preamble.
The independent v7 checker is mandatory for `COMMON_CANDIDATE`.

For `UNKNOWN_RESOURCE`, do not spend another full semantic replay inside the
same job.  Instead use the audited v5 claim-free transport boundary: require
the unique exact RESOURCE terminal, nonempty receipt and checkpoint,
RESOURCE candidate marker, `DISCOVERY_RESOURCE`, a 64-hex checkpoint state
seal, all claims false, and a resource-only owned OK marker which contains no
global COMPLETE marker.  The artifact is candidate transport and may not be
resumed or adopted until independent authentication.  This is not checker
approval or a mathematical milestone.

The driver must reject plain UNKNOWN, ERROR, traceback, stale/missing output,
or any producer/checker nonzero exit.  It must actually execute the generated
shell, not end at `bash -n`.  COMMON requires the exact v7 checker PASS
terminal, nonempty verdict, and global COMPLETE owned marker.  RESOURCE must
never print that marker.

Keep the audited envelopes exactly:

```text
14040 < 14220 < 14400 seconds
4200000000 < 4500000000 < 5120000000 bytes
ulimit -v 5000000
```

Pin the new v7 producer, new v7 checker, and v431 proof in the driver.  Also
restore exact byte/SHA checks for C99, rank51, Task451 producer/checker, and
v424/v426/v427.  Require canonical input realpath and a unique producer
terminal.  Keep COMMON checker timeout 5400 seconds rather than 14400.
Preserve ASCII-only GAP/driver text.

## Repair C: bind the new theorem

Task508 proved that the v6 producer/checker `PROOF` constants are dead: their
`pins()` and durable binding remain the old seven-entry v5 set.  The v7
producer and checker must each authenticate v431 independently, expose it in
their public pins, and include its exact path/bytes/SHA in the binding from
which migrated/new checkpoint seals are computed.  Producer and checker must
derive the same strengthened binding without importing each other's helper.

Authenticate a frozen v5 closed input under the old constants before changing
only its top-level schema, strengthened v7 binding and state seal.  Historical
rows, batches, segments, prefix, ready cores and ledger remain unchanged.

## Bounded gates

Run only parse/pin/self-test/fixture and tiny mocked transport gates.  No
production owner construction or unbounded search.  Report exact byte counts,
SHA-256 values, commands, and bounded execution of both terminal paths:
COMMON reaches the checker; RESOURCE reaches only the strict claim-free
transport gate and never COMMON/COMPLETE.

Final marker:

`TASK509_R07_RANK99_V6_CHECKER_DRIVER_MINIMAL_REPAIR_PASS`

On any inability, stop honestly with `..._STOP`.
