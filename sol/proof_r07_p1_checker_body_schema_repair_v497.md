# R07 P1 checker body-schema repair（v497）

## Actual failure

Checker-only run `33818161852/1`, job `100854717509`, head
`619b30a84d1585e5f377f34b7d28dd63ccfb3209` passed exact run/job/artifact
authentication, checker-v4 selftest, six receipts and all five parent downloads.
The actual checker then stopped in 0.87 s with peak RSS 310,816 KiB at

```text
prepare_body_metadata
```

No arithmetic terminal or downstream claim was emitted.

## Unique schema mismatch

The producing grade1-v4 source defines

```python
SCHEMA = "d972.r07.a0.first-rung-grade1.v3"
STATE_SCHEMA = SCHEMA + ".state"
```

and both sealed prepare/block bodies use `STATE_SCHEMA`.  Hence their exact
body schema is

```text
d972.r07.a0.first-rung-grade1.v3.state
```

while checker-v4 defines `STATE_SCHEMA` without the final `.state`.  V493
correctly repaired the separate HEAD schema to
`d972.r07.a0.first-rung-grade1.v3.state.head`; it did not repair the body
constant.  Once the HEAD gate passes on actual input, this second stale
constant is exactly the next conjunct in `prepare_body_metadata`.

## Minimal repair

Version checker-v4 to v5 with the sole production semantic change

```python
STATE_SCHEMA = "d972.r07.a0.first-rung-grade1.v3.state"
```

and retain the already-correct explicit `SEALED_HEAD_SCHEMA`.  Add independent
literal fixtures which accept the two distinct exact strings and reject
missing `.state`, missing `.head`, or interchanging body and HEAD schemas.
All arithmetic, 65,340 obligations, parser, output schema/marker and claim
boundary remain unchanged.  The same successful six producer receipts and
five parents can be replayed; producer phases must not be rebuilt.

```text
P1_SEMANTIC_CROSS_CHECKED=NO
A0/COMMON/COFINAL/FAKE/IHARA=NOT_DECLARED
verified=false
```

