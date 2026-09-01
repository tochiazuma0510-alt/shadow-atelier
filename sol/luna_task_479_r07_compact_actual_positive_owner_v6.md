# Luna Task479 — compact actual positive owner v6 dormant-shell repair

## Scope

Repair only F1 from
`sol/sol_reply_476_audit_r07_compact_actual_positive_owner_v5.md`.
Task476 v5 already has the correct inherited-v3 tuple and the accepted v4
producer/checker ABI.  Preserve every mathematical body, pin, CLI argument,
cap, terminal, frontier and MEMBER-only checker policy.

Create a versioned v6 GAP driver as the exact v5 successor.  After closing
the generated bash payload, execute that payload **exactly once**, then fail
closed unless the fresh v6 success file exists and contains exactly

```text
R07_COMPACT_DIRECT_RELATOR_A5_A6_POSITIVE_V6_DRIVER_COMPLETE\n
```

Only after that exact check may the GAP driver print the same v6 COMPLETE
terminal.  READY is not an accepted terminal.  The generated shell must
still have `set -euo pipefail`, one producer command, one checker command
confined to the MEMBER branch, and the small nonpositive JSON assertion.

The driver must continue to require explicit `D479Task193Receipt` and
`D479Task193Verdict` inputs.  Do not invent or run fixtures: production
dispatch remains blocked until the broker materializes an authenticated
Task193-v5 receipt/verdict pair at those paths.

Run bounded static/load-without-production gates proving:

1. v5 and all inherited producer/checker path/byte/SHA tuples are exact;
2. `CloseStream` precedes exactly one `Exec` of the owned shell;
3. the exact success-file existence/content checks occur after `Exec`;
4. there is one producer command and one MEMBER-only checker command;
5. no SELFTEST/FIXTURE, retry, worker pool, extra traversal, or workflow edit
   was introduced.

Do not execute the v6 driver, production, GHA, git, or create bytecode caches.

## Exact outputs

1. `search/d972_r07_compact_direct_relator_a5_a6_positive_gha_driver_v6.g`
2. `sol/luna_reply_479_r07_compact_actual_positive_owner_v6.md`

End with `TASK479_R07_COMPACT_ACTUAL_POSITIVE_OWNER_V6_PASS` or a typed STOP.
