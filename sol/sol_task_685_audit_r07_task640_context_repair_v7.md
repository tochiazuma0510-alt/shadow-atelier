# Sol(max) Task685 — audit Task640 Context repair v7

Audit Task683's producer delta and inert v7 workflow against the exact v6
failure in Root Task684.  Write only
`sol/sol_reply_685_audit_r07_task640_context_repair_v7.md`; no code/GHA/git or
production replay.

Check that:

- the authenticated grade1-v4 Context truly exposes `physical_shifts` and not
  `shifts`, and this is the only stale producer reference;
- the factored helper is the production path and its mutation fixture would
  red-light the old name/value;
- all other producer `context.*` accesses exist with the required type;
- checker code is unchanged and its independent local `Context.shifts` remains
  valid;
- after normalizing version/artifact labels and inert guard, v6-to-v7 changes
  only the producer hash plus this audited source delta;
- every v6 path, cap, service pin, verdict copy, action SHA, timeout and upload
  remains intact; v7 is valid and inert, and removing only `false &&` is the
  release operation.

Do not reopen already passed Task640 math or request unrelated hardening.  End
exactly `PASS_CONTEXT_ONLY / SAFE_TO_DISPATCH_GHA=yes` or
`FAIL_CONTEXT_ONLY / SAFE_TO_DISPATCH_GHA=no`, with `verified=false` and no
v220 numerator change.
