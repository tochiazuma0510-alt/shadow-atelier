# Luna Task800 — A0 reached-seed canary wiring repair v16

Role: Luna implementation only. Process every numbered section.

## 1. Exact input and ruling

Read in full:

- `sol/sol_reply_795_audit_r07_a0_reached_seed_canary_v15.md`
- `search/d972_r07_a0_fresh_precision2_endpoint_signature_v9.py`
- `search/check_d972_r07_a0_fresh_precision2_endpoint_signature_v7.py`
- `.github/workflows/d972-r07-a0-fresh-precision2-endpoint-v15.yml`

Task795 found one reached deterministic blocker.  The production caller passes
the 12-key `direct_canary` object as the final `base_receipt` argument of
`validate_direct_canary`; an honest payload therefore stops at
`checker_canary_base_rows` before the `G=21,287` replay.

## 2. Authorized repair only

Create versioned successors:

- `search/check_d972_r07_a0_fresh_precision2_endpoint_signature_v8.py`
- `.github/workflows/d972-r07-a0-fresh-precision2-endpoint-v16.yml`
- `sol/luna_reply_800_r07_a0_canary_wiring_repair_v16.md`

Keep producer v9 byte-identical and use it directly from workflow v16.

In checker v8:

1. change only the reached production call's final argument from
   `direct_canary` to the already reconstructed five-key `base_receipt`;
2. add one bounded positive regression fixture which invokes the complete
   `validate_direct_canary` normal path with distinct 12-key full receipt and
   five-key base receipt and requires acceptance; and
3. retain the existing mutations, including resealed base-row mutation and
   incomplete `21,286/21,287` aggregation rejection.

Do not change arithmetic, owner construction, source universe, schedules,
targets, caps, generic-call count, bucket aggregation, or claim flags.  Do not
add production-size tests or another audit framework.

## 3. Workflow successor

Copy v15 to v16 mechanically.  Update only versioned names/schema/markers,
checker path/bytes/SHA, workflow fire token to
`[fire-fresh-precision2-endpoint-v16]`, and artifact names as required.  Keep
producer v9 bytes/SHA and all parent/source pins unchanged.  Preserve the
single serial job and existing limits.

## 4. Bounded checks and report

Run only py_compile and bounded producer-v9/checker-v8 selftests.  Compare the
checker AST/call graph against v7 and workflow v16 against v15, and report the
exact changed surface.  Record bytes, LF/CR/BOM and SHA-256 for all outputs.
Do not run production, GHA, git, or heavy local computation.

The reply must state `READY_FOR_HOSTILE_REAUDIT` or the first exact blocker.
No fresh rho2, A0, COMMON, compatible lift, fake or Ihara claim is authorized.
`verified=false`.
