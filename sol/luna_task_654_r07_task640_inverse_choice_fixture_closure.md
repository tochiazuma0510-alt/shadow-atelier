# Luna Task654 — Task640 final inverse-choice fixture closure only

## Scope

You are Luna. Read the complete Task652 reply if it is already present; the
independent auditor has already reported the exact blocker below to root.
Repair only its one concrete
blocker in the existing Task640 checker: changing production's negative-sign
factor from `base^{-1}` to `base` must make selftest fail.

Authorized files only:

- `search/check_d972_r07_a0_fresh_precision2_endpoint_signature_v3.py`
- `.github/workflows/d972-r07-a0-fresh-precision2-endpoint-v3.yml`
- `sol/luna_reply_640_r07_fresh_precision2_endpoint_signature_v3.md`
- `sol/luna_reply_651_r07_task640_three_live_fixture_closure.md`
- new report `sol/luna_reply_654_r07_task640_inverse_choice_fixture_closure.md`

## Exact repair

Factor the existing production expression
`base if sign > 0 else self.old.inv_word(base)` into one tiny helper used by
both production and selftest. The helper must reject signs outside `{-1,1}`.
Exercise its negative branch with a non-self-inverse element (for example an
S3 3-cycle) and compare to an independently fixed inverse. Do not merely feed
an already-signed `base_factor` into `occurrence_prefix_gate`. Demonstrate that
the exact mutation `negative -> base` fails the selftest.

Retain the Task651 noncommutative prefix/order fixture, ancestry-binding
fixture, and packing-roundtrip fixture unchanged. Update only the honest
mutation count and checker hash chain in workflow/replies. Keep `false &&` and
all production semantics otherwise unchanged.

Run only bounded serial py_compile/selftests/YAML/forbidden-import/action-pin/
inert checks. No heavy local run, GHA, git, hardening, or redesign.

Report exact paths/bytes/LF lines/SHA-256 and commands/outcomes. End with
`READY_FOR_TASK655_FINAL_REAUDIT` or `NOT_READY`.
