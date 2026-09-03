# Luna Task662 — Task640 parent-checker cap binding, workflow v5

## Exact observed failure

Task640 v4 run/attempt `33750997558/1` passed all downloads and found the
correct nested Task625 manifest, then the exact old Task625 checker rejected
`manifest_binding` before Task640 production.

The checker function `checker_staged_caps()` seals
`TASK625_ACCUMULATED_CAP` into `manifest.resource_caps`. The accepted Task625
workflow ran with `TASK625_ACCUMULATED_CAP=50000000`; Task640 v4 omitted this
environment variable, so the checker used its default `2000000`. The remaining
Task625 cap defaults already equal the accepted manifest values.

## Scope

Create only:

- `.github/workflows/d972-r07-a0-fresh-precision2-endpoint-v5.yml`, versioned
  from released v4;
- `sol/luna_reply_662_r07_task640_parent_cap_binding_v5.md`.

Allowed semantic delta: add exactly
`TASK625_ACCUMULATED_CAP: "50000000"` to the workflow environment. Make only
mechanical v4-to-v5 workflow name/self-path/fire/output-label changes. Retain
the four corrected nested Task625 payload paths, root verdict path, all code /
parent / reply / action pins, other caps, downloads, checker byte comparison,
success-only upload and fail-closed behavior. Add an inert `false &&` guard.
Do not modify Python or mathematics and do not dispatch/GHA/git.

Run safe YAML parse, exact normalized diff census, fixed inert/action scans,
and statically compare the added value against both the accepted Task625 v3
workflow and `checker_staged_caps`. Reply with exact bytes/LF/SHA-256 and every
changed line. End `READY_FOR_TASK663_CAP_ONLY_AUDIT` or `NOT_READY`.
