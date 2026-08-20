# 157eh Luna reply — full-D2 monitor-scope repair v2

## Outcome and scope

Implemented the versioned transport/monitor repair in the four authorized v2
files only.  The frozen 157eg mathematical predicate, fixed prefix, raw-lambda
oracle, 76-occurrence correlation, ordering, caps, and terminal claims are
unchanged.  The v2 producer projects exactly to the pinned v1 receipt before
the frozen v1 schema is applied; the v2 checker independently validates the
new monitor envelope and then sends only that v1 projection through the exact
pinned v1 checker.

Canonical task:
`sol/luna_task_157eh_b345_full_d2_monitor_scope_repair.md`, SHA-256
`5d8da27e3997b261c004bb2fb4a40e9416bed39536816ab2fca9f3a9935c095e`,
15015 bytes.

## Repair implemented

- The producer owns one absolute clock/RSS/check state and immutable
  outer-scoped adapters.  The exact sorted registry has 18 registered pairs;
  no prefix, wildcard, or inner-to-outer inference is used.
- The fresh adapter is passed to the imported prefix builder, the raw adapter
  to the raw-lambda oracle, and the section adapter to the ACTIVE witness
  serializer.  `check` and `reserve` both preserve their pinned outer.
- Immediately after a successful fresh-prefix return, both
  `prefix["dag"].deadline` and `prefix["basis"].deadline` must be the identical
  fresh adapter.  Only after this identity gate are both detached to `None`;
  every later stage rechecks that state.
- Local monitor RESOURCE terminals bind the public phase to the explicit
  outer and export the inner callback only as a closed diagnostic.  Inherited
  structural caps remain bound to the caller-selected outer.  Receipt
  serialization remains outside the callback registry and keeps the v1 byte
  cap/fallback.
- The checker owns a separate literal registry/digest, exact repair-input
  table, pair validator, diagnostic schema, stale-prefix gate, and absolute
  deadline.  The original v1 checker still independently reconstructs the q3
  quotient, prefix, raw functional, base columns, complete correlation, and
  optional section witness.
- The driver owns the fixed v2 artifact path.  `RUN` and `SELFTEST` are the
  only mode selectors.  An optional `OUTPUT` is accepted only when it equals
  the fixed path; absence is valid.  The q3 child, package gates, artifact SHA,
  independent q3 checker, common 18000-second producer/checker budget,
  pipefail/tee, stale-output deletion, and exactly-one markers are retained.

## Frozen v1 provenance

The v2 lane authenticates the complete frozen v1 bundle, including producer
`6903b745…fde52`, checker `311dc941…57358`, driver `c0a0626f…b65b4`, task
`22b649c1…19720e`, and reply `12a1e5fe…a0445f`.

- `32368735249`: v1 combined lightweight selftest PASS.
- `32368850435`: transport-only failure from the old mandatory OUTPUT input.
- `32368985968`: transport-only quote stripping under `gh workflow run -f`.
- `32369164205`: q3 producer/checker PASS, then the v1 producer failed at
  `packed_provenance_dag_growth` after about 2m23s.  It evaluated no
  correlation pair and produced no mathematical result.

The last run is failure provenance only.  It is not evidence for a lift,
separator, obstruction, B4-A, or B4-B claim.

## Recurrence guard

| Repeated failure | Permanent v2 guard | Static status |
|---|---|---|
| callback label omitted from wrapper | trace the active imported call tree; actual packed DAG fixture crosses node 1024 | PASS |
| reused inner label assigned to wrong stage | immutable outer-scoped adapter; no string inference | PASS |
| adapter resets budget | one base absolute deadline/RSS/check/hit state | PASS |
| reserve path unimplemented | adapter implements and gates both `check` and `reserve` | PASS |
| selftest misses production callback | actual provenance DAG, packed pivot/target reducers, and section serializer fixtures | PASS in corrective combined selftest |
| shell strips quoted GAP input | driver-owned fixed output and JSON/boolean dispatch | PASS |

The bounded fixtures include every registered pair and cross-pair rejection,
dormant-label rejection, duplicate proof-DAG labels under both legal outers,
forced check/reserve resources, actual 1024-node callback, actual packed pivot
and target callbacks, actual three-label section serialization under both
outers, detach/stale-prefix checks, checker registry/digest/outer/inner
mutations, and all inherited v1 fixture coverage.

## Static freeze and test boundary

The implementation was statically checked for Python AST/compile validity,
ASCII-only GAP driver text, exact source-pin hashes, v2 paths/markers, balanced
driver delimiters, conflict markers, and placeholder strings.  No GAP, GHA,
full computation, or Git operation was run.
The first task-authorized combined attempt was run after hostile-review GO:

- command sequence: `python -u -B
  search/d972_b345_full_d2_dual_correlation_v2.py --self-test`, followed by
  the checker only on producer exit zero;
- log:
  `C:\Users\81905\AppData\Local\Temp\shadow-atelier-157eh-combined-selftest-20260820.log`;
- producer exit `1`; checker not started (`-1` in the combined ledger);
- v2 producer marker `0`; v2 checker marker `0`; the inherited v1 producer
  marker appeared exactly once before the failure;
- all four pre/post hashes were unchanged (`a603dfea…6e2a`,
  `6a953188…efc0`, `a5cee7e9…4d23`, `46e0f616…5531`).

The exact failure was fixture-only: frozen `v1.self_test()` had already loaded
`_d972_157eg_pinned_157ed_producer`, after which the v2 fixture called
`v1.load_ed()` a second time and hit its deliberate module-name-fresh guard.
No production path or mathematical computation was entered.  The corrective
fixture now reuses that already-loaded module only after exact module-name,
resolved path, byte length, SHA, and expected-API gates.  The production path,
checker predicate, and driver behavior are unchanged.  This corrective freeze
was then diff-audited before the separately authorized corrective attempt.

The corrective combined attempt used the same command sequence exactly once:

- log:
  `C:\Users\81905\AppData\Local\Temp\shadow-atelier-157eh-corrective-selftest-20260820.log`;
- producer exit `0`; checker exit `0`;
- v2 producer marker `1`; v2 checker marker `1`;
- inherited v1 producer marker `1`; inherited v1 checker marker `1`;
- all four pre/post hashes were unchanged: producer
  `6557bcfea70c0846158951fafe3d6ef8790479a5c7010db896ed76540dd5ae5f`,
  checker
  `881719f18b302afcb5ee25fd22e36ef7d6b50ee38a3562f208a2adb2a6e74060`,
  driver
  `5b76b267a36526f4f2d9e325b4b92e36c7b241f6f9d75abec7e08c3c9ff74cde`,
  and pre-update reply
  `e197c412dafa0048adf0fc39618b84299b499c8c6dd155324da57c1836c9d7e7`.

No further selftest was executed after this PASS.

Final code hashes:

| File | SHA-256 | Bytes |
|---|---:|---:|
| `search/d972_b345_full_d2_dual_correlation_v2.py` | `6557bcfea70c0846158951fafe3d6ef8790479a5c7010db896ed76540dd5ae5f` | 42449 |
| `search/check_d972_b345_full_d2_dual_correlation_v2.py` | `881719f18b302afcb5ee25fd22e36ef7d6b50ee38a3562f208a2adb2a6e74060` | 21933 |
| `search/d972_b345_full_d2_dual_correlation_gha_driver_v2.g` | `5b76b267a36526f4f2d9e325b4b92e36c7b241f6f9d75abec7e08c3c9ff74cde` | 13253 |

## Dispatch and expected cost

Use JSON workflow inputs for any GAP preamble containing quotes; do not use
`gh workflow run -f`.  The preferred full preamble is boolean-only:

```gap
D972_B345_FULL_D2_DUAL_CORRELATION_V2_RUN:=true;;
Read("search/d972_b345_full_d2_dual_correlation_gha_driver_v2.g");;
```

The repair adds only constant-size scope checks/counters.  The completed
runtime should therefore remain in the v1 lane's prior range rather than
becoming faster: the failed v1 run reached the first exposed prefix callback
after roughly 143 seconds, while the complete fresh-prefix construction and
independent replay remain the dominant, potentially multi-hour work within
the shared 18000-second bound.  No ACTIVE or SEPARATOR result is promised.

`B345_FULL_D2_DUAL_CORRELATION_V2_READY_FOR_GHA_SELFTEST`
