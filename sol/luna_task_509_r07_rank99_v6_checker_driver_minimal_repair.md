# Luna task 509 - minimal rank99-v6 checker/driver repair

Role: Luna implementation only.  Do not run production/GHA, commit, push,
change mathematics, edit the v6 producer/checker/driver, or touch any output
other than the four files named below.

The Task506 v6 producer remains frozen exactly at:

```text
search/d972_r07_a0_dual_anchored_rank99_durable_discovery_v6.py
14329 3173c9d99fc5a94713d3dbed1b2c90d4ed3a5723b428838ec0bd50d8aee3d90c
```

Read Task506, paper v431, Task507 GO, and Task508.  Repair only two already
identified acceptance-boundary defects while preserving the v6 schema and
producer marker.

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
Preserve the v6 schema, binding and terminal marker so the existing rank99
closed state migrates identically; the new file is a code-bundle version, not
a checkpoint-schema rewrite.  Add a bounded production-shaped source-patch
fixture proving the executed transformed loop receives a dict presentation
and reaches the formula iteration without `AttributeError`.  A text-only
presence check is insufficient.

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

## Repair B: checker-gate RESOURCE transport

The driver must run the independent v7 checker for both producer terminals:

- `COMMON_CANDIDATE`; and
- `UNKNOWN_RESOURCE`.

It must reject plain UNKNOWN, ERROR, traceback, stale/missing output, or any
producer/checker nonzero exit.  It may regard checker-approved
`UNKNOWN_RESOURCE` as workflow transport success only after the checker has
authenticated the closed checkpoint and false claim flags.  Then write the
`.ok` marker so artifact upload can occur.  Do not exit before the checker.

Keep the audited envelopes exactly:

```text
14040 < 14220 < 14400 seconds
4200000000 < 4500000000 < 5120000000 bytes
ulimit -v 5000000
```

Pin the new v7 producer, new v7 checker, and v431 proof in the driver.
Preserve ASCII-only GAP/driver text.

## Bounded gates

Run only parse/pin/self-test/fixture and tiny mocked transport gates.  No
production owner construction or unbounded search.  Report exact byte counts,
SHA-256 values, commands, and whether both terminal paths reach the checker.

Final marker:

`TASK509_R07_RANK99_V6_CHECKER_DRIVER_MINIMAL_REPAIR_PASS`

On any inability, stop honestly with `..._STOP`.
