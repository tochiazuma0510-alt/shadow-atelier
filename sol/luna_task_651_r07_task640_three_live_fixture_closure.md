# Luna Task651 — Task640 final three live-fixture blockers only

## Scope

You are Luna. Read the completed Task649 audit reply before editing. Repair
exactly the three remaining F646-C release blockers below in the existing
Task640 v3 checker. Do not redesign arithmetic, add hardening, touch producer
semantics, or run production work.

Authorized implementation files are only:

- `search/check_d972_r07_a0_fresh_precision2_endpoint_signature_v3.py`
- `.github/workflows/d972-r07-a0-fresh-precision2-endpoint-v3.yml`
- `sol/luna_reply_640_r07_fresh_precision2_endpoint_signature_v3.md`

Also write only the designated report
`sol/luna_reply_651_r07_task640_three_live_fixture_closure.md`.

## Exact repairs

1. Add a bounded negative fixture which passes a wrong ancestry digest/binding
   to the same live `parse_literal_leaves` used by production and requires
   rejection. Deleting the binding comparison must make selftest fail.
2. Factor only the existing occurrence-prefix construction at the current
   `IndependentAllSeven.__init__` lines (former lines 1337--1350) into one
   bounded helper used by production and selftest. Add a tiny noncommutative or
   otherwise order-sensitive live-helper fixture covering reverse traversal,
   sign/inverse choice, and prefix multiplication. Reversing/changing a real
   `U_j` rule or the helper order must make selftest fail. Do not instantiate
   the production-sized graph in selftest.
3. Add a dense fixture that passes all preceding byte-equality checks in
   `dense_result_gate` and fails specifically at its packing/unpacking
   roundtrip branch. For example, supply the same invalid packed bytes both in
   the blob and argument so the earlier equality gate passes. Removing or
   breaking the roundtrip branch must make selftest fail.

All fixtures must call the exact helpers/gates executed by production. Update
the mutation count honestly. Update the workflow's exact checker SHA pin and
the frozen quartet table in reply640; keep the workflow inert and otherwise
unchanged.

## Bounded checks

Run serially only: checker and producer `py_compile`, both selftests, YAML safe
parse, forbidden shared import/exec scan, immutable-action scan, and inert
`false &&` check. No parallel Python, no heavy local run, no GHA/git.

Reply with exact paths, sizes, LF counts, SHA-256 values, commands/outcomes,
the mutation count, and a line-by-line explanation showing that each of the
three production gates is now mutation-sensitive. End with
`READY_FOR_TASK652_FINAL_REAUDIT` or `NOT_READY`.
