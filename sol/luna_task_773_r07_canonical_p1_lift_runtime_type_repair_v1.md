# Luna task 773 — canonical P1 lift actual-runtime type repair v1

Role: Luna (implementation only).  Do not change the mathematical row
construction, authenticated DAG, row order, reductions, or claim flags.

## 1. Frozen failure to diagnose

The audited v5 producer was dispatched by workflow v2 at:

- run `33824881796`, attempt `1`, job `100875303915`
- head `8bcc7182b4b6676ce4f752f61ad5ffee99d11926`
- build elapsed `50.62 s`, max RSS `5,196,492 KiB`
- terminal: `REJECTED: object supporting the buffer API required`
- log artifact id `9919602334`, digest
  `sha256:a604edf4ca38bcb318a919f0c1076d7f5623643238235a0bd0758ca391d26340`

The extracted logs are under the external temporary directory
`%TEMP%/shadow_atelier_lift_v2_logs_33824881796_1`.  Authentication,
selftest, checker receipt, all five parent downloads, and launch-manifest
construction passed.  The failure is neither timeout nor RSS ceiling.

## 2. Required implementation

Read the complete frozen v5 producer and v2 workflow.  Locate the actual
non-buffer value on the reached production path by static/call-graph analysis.
Make the smallest versioned repair as:

- `search/d972_r07_canonical_p1_dag_degree2_lift_v6.py`
- `.github/workflows/d972-r07-canonical-p1-dag-degree2-lift-v3.yml`
- this task's reply at
  `sol/luna_reply_773_r07_canonical_p1_lift_runtime_type_repair_v1.md`

The v6 exception terminal must include a bounded traceback or an unambiguous
phase/call-site label, so a second opaque 50-second failure is impossible.
If the cause can be proved statically, repair it in the same v6; do not create
a diagnostic-only production version.  Preserve fail-closed behavior.

Update all executable hashes, launch-manifest schema/pins, filename pins, and
workflow artifact names consistently.  The workflow must retain serial
production execution, the existing 7-GiB RSS gate and time gate, exact parent
artifact authentication, progress/checkpoint logging, and success/log artifact
publication.  It must invoke v6, never v5.

## 3. Scope and performance constraints

- Do not run the real 5-GiB build locally.
- Run only bounded compile/selftest/fixture/static checks.
- Do not add a heavy SELFTEST, full-input duplicate parse, extra matrix copy,
  or extra full-file pass to the production path.
- Do not refactor unrelated code and do not alter mathematical arithmetic.
- Do not use git, GitHub, GHA, network, or delegation; root is the broker.

## 4. Reply evidence

Report exact bytes/SHA/LF/CR/NUL/final-byte for v6 and workflow v3; identify
the exact bad value, reached call site, and why the repair is semantics-neutral;
list bounded commands and outputs; state whether any avoidable copy or dense
owner was introduced.  End with one of:

`READY_FOR_SOL_AUDIT=yes`

or

`READY_FOR_SOL_AUDIT=no` plus the precise blocker.
