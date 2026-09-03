# R07 P1 checker state-head schema repair v493

Author: Sol / 2026-09-04

## Actual terminal

P1 semantic run/attempt `33814881435/1`, exact head
`15778e83c52941040ef9d4289ab76d897ee30ebc`, completed producer prepare, all
four character blocks, and the six-receipt join successfully.  The joined
producer receipt reports exactly

```text
old ranks             2014
new ranks             6045
DAG nodes              8059
global relations      32280
compound obligations  65340
```

The independent checker stopped before replay arithmetic after 0.32 seconds
and 41,320 KiB peak RSS with

```text
sealed_head:prepare
```

This is a finite schema-literal failure, not an arithmetic disagreement or a
resource terminal.

## Exact mismatch

The accepted Task554 state files use the head schema

```text
d972.r07.a0.first-rung-grade1.v3.state.head.
```

Producer v5 requires that literal.  Checker v3 instead constructs its expected
head schema as

```text
STATE_SCHEMA + ".head"
```

where `STATE_SCHEMA` is
`d972.r07.a0.first-rung-grade1.v3`.  It therefore requests the nonexistent
literal

```text
d972.r07.a0.first-rung-grade1.v3.head.
```

The same `read_sealed` routine would reject each block head for the same
reason.  Its positive fixture derived the synthetic head from the same wrong
expression, so the bounded selftest could not expose the mismatch.

## Finite repair

Use one explicit sealed-head schema constant equal to the authenticated
`...v3.state.head` literal for both prepare and block heads.  Keep
`STATE_SCHEMA` unchanged for state bodies.  The positive fixture must spell the
authenticated literal independently, and a mutation to `...v3.head` must be
rejected.  No producer receipt, equality digest, arithmetic recurrence,
coordinate order, rank or obligation count changes.

The already generated producer artifacts remain reusable.  A successor
workflow may download the same six-receipt artifact and rerun only the repaired
independent checker against the five immutable Task554 parents; rebuilding the
six producer phases is mathematically unnecessary.  The rerun must bind the
original run/attempt/head, the six exact receipt hashes and checker-v4 source
hash in a new result and workflow receipt.

```text
P1_PRODUCER_SIX_PHASES=ACTUAL_SUCCESS
P1_INDEPENDENT_CHECKER=FINITE_SCHEMA_REPAIR_REQUIRED
P1_SEMANTICS_CROSS_CHECKED=NO
A0/COMMON/COFINAL/FAKE/IHARA=NOT_DECLARED
verified=false
```

