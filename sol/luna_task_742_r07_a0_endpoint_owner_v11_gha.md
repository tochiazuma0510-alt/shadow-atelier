# Luna Task742 -- A0 endpoint owner-binding v11 GHA wrapper

Role declaration: Luna.  Create the smallest inert v11 workflow adapting the
accepted v10 actual path to producer v5.  Do not edit implementation, run git,
push, dispatch, or perform the real endpoint build.

Read fully:

- `.github/workflows/d972-r07-a0-fresh-precision2-endpoint-v10.yml`
- `sol/proof_r07_task640_v10_missing_owner_binding_v488.md`
- `search/d972_r07_a0_fresh_precision2_endpoint_signature_v5.py`
- `sol/luna_reply_735_r07_task640_owner_binding_v5.md`
- `sol/sol_reply_737_audit_r07_task640_owner_binding_v5.md`
- `search/check_d972_r07_a0_fresh_precision2_endpoint_signature_v4.py`

Create only:

- `.github/workflows/d972-r07-a0-fresh-precision2-endpoint-v11.yml`
- `sol/luna_reply_742_r07_a0_endpoint_owner_v11_gha.md`

Requirements:

1. Mechanically adapt v10 to v11.  Use producer v5 at 43,838 bytes / SHA
   `2f8cb910c79cb6046c8cd7a83f77e9e883187fe81b43209e3a8d09679a12ad6b`.
   Keep the already accepted checker v4 at SHA
   `581f9a5a9aa65ae298bf6d6f785ed1063ddfb0caf8a0c06e15f30ec2e713fd6f`.
2. Pin and authenticate v488 (2,232 bytes / SHA
   `e07d52e7864042d1a3fe22538b4ba408d7cc56721135b07c34b4111e726cf763`),
   Task735 reply (4,067 bytes / SHA
   `a547638073b64bced8e9e0893786d8bd9fc437b3ada85b47515d5d9dfde34184`),
   and Task737 audit (7,999 bytes / SHA
   `13e6d021c197cec3ca0213ab0f57fe711b982ecc11a4e9d3ca54984d3bd8cb49`).
   Require exact audit tokens `PASS_WITH_FINITE_TEXT_REPAIR` and
   `OWNER_BINDING_V5_SAFE_FOR_GHA=yes`.  Retain every v10 parent/source pin.
3. Preserve the cheap exact 1,120-byte Task625 verdict staging into both
   payload names, all download identities, caps, timeouts, serial execution,
   endpoint producer/checker arguments, marker gate and always-upload logs.
   Do not restore the 11m51 parent-checker replay or generic boundary build.
4. Change output/log artifact names from v10 to v11.  Do not alter the v4
   checker marker or producer protocol: v5 deliberately retains them.
5. Leave workflow `workflow_dispatch`-only and without a job-level fire
   condition.  Root will add one finite branch fire trigger after inspection.
6. Parse YAML, verify exact pins, and run only bounded producer/checker
   selftests if needed.  No real parents/build.  Report exact bytes/LF/final
   LF/SHA256 and `REAL_GHA_RUN=NOT_RUN`, `verified=false`.

