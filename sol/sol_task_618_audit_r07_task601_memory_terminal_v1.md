# Sol(max) Task618: Task601 first-run MemoryError forensic and minimal repair

Role: independent mathematical/code forensic.  Do not edit implementation,
run production/GHA/git, or start a local full route.  Write only
`sol/sol_reply_618_audit_r07_task601_memory_terminal_v1.md`.

Read the complete current Task601 producer/checker/workflow, v468--v471,
Task614/616 audit replies and the run receipt below.

```text
run:       33717064826
job:       100528381356
head:      69e95d7fc50f04691a41417c495e27f7064f470d
main step: 2026-09-03T05:00:02Z -- 05:07:03Z
terminal:  producer MemoryError, no checker, no payload artifact
log artifact id/name: 9879043599 /
  task601-selected-slp-logs-33717064826-1
producer.log: 279 bytes, SHA-256
  912596f139e40502a9e9fdd00717c914158fe552530c51df718aee436dca1897
```

All preflight and parent downloads passed.  The failure came after about 421
seconds, close to the independently measured all-8,059 route time of about
396.5 seconds.  There is no inner phase trace.

Return `PASS_REPAIR_SPEC` or `FAIL_UNLOCALIZED`.  Determine the smallest
repair which makes both producer and checker safely fit the existing
60-minute/8-GiB contract without weakening the canonical selected SLP.
Specifically adjudicate:

1. whether the quotient-specific `derived.states`/literal-leaf export is
   optional under v468--v471 and may be removed from Task601, leaving fresh
   exact-path/signature computation to the later consumer;
2. whether physical node/edge/origin lists should be converted once to their
   packed byte streams and the Python tuple/bytes lists released before source
   closure;
3. whether four full block JSON bodies or owner matrices are retained
   simultaneously and can instead be consumed by character without reload per
   selected origin;
4. whether the checker duplicates large edge streams as Python tuples in
   `loaded`, `gedges/ledges` and independent expected lists, and the exact
   compact iterator/packed-comparison replacement;
5. the minimum phase/RSS counters needed to make a second terminal localized,
   without adding a selftest campaign or another discovery framework.

Preserve all 8,059 routing rows, ranks 1,661/5,044, 3,317 coefficients,
physical origins/companions/lower-zero receipts, independent full reroute,
least canonical source graph, roots and false claims.  A partial source graph,
raising the memory limit alone, skipping the checker, or calling resource
exhaustion a mathematical negative is forbidden.  Give a concrete bounded
patch plan for Luna and state whether one rerun is justified afterward.
