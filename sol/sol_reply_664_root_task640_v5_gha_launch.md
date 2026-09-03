# Root Task664 — Task640 v5 replacement GHA launch receipt

## v4 failure and cap-only repair

Task640 v4 run/attempt `33750997558/1`, job `100634274219`, found the corrected
nested Task625 manifest but failed its old-checker replay at
`manifest_binding`, before Task640 production. The accepted Task625 manifest
seals `TASK625_ACCUMULATED_CAP=50000000`; v4 omitted that environment key and
the old checker therefore used its default `2000000`. The accepted replay has
2,605,954 accumulated states, so the mismatch and required value are exact.

Workflow v5 adds only that cap line beyond mechanical v5 labels. Task663
returned `PASS_CAP_ONLY / SAFE_TO_DISPATCH_GHA=yes`; its 4,177-byte reply has
SHA-256 `6e5687e32563eaa82ba64c9244c44cb2ea09c593454b17508720dc9d938b2216`.

## v5 launch

| field | exact value |
|---|---|
| branch | `sol/r07-explicit-lift-20260825` |
| workflow | `.github/workflows/d972-r07-a0-fresh-precision2-endpoint-v5.yml` |
| v5 release commit | `392fc3080df0715b9654729d9deca532a37bc3ab` |
| event head | `63e1565b0d0b3a7ee229ca3cf64882a2c8229f81` |
| audited inert v5 SHA-256 | `88f5169806ae83202aadbdba0c3505bf754cccc61131064d373a4e65946c664e` |
| released v5 SHA-256 | `22e4b1ef0a9b50fad79fc9b08914b6e77c463769b6f02fb75d48da9fd71b6b1a` |
| authorized release delta | deletion of the single inert `false &&` line |
| run/attempt | `33752047946/1` |
| job id/name | `100637599756` / `fresh-endpoint` |
| event | `workflow_dispatch` |
| URL | `https://github.com/tochiazuma0510-alt/shadow-atelier/actions/runs/33752047946` |

The same-workflow push run `33752017644` was skipped. The production run
passed checkout, code authentication, fixtures, accepted Task625 service
authentication and all three downloads. It then entered the exact Task625
checker replay and remained in progress beyond the previous immediate
`manifest_binding` failure point.

## Claim boundary

This is a launch/in-progress receipt. It proves no rho2, grade-two decision,
A0, full-Q0/order-54,432 solution, compatible cofinal lift, fake, Ihara,
cross-check, or Lean verification. A successful output still requires an
external artifact/checker audit.

`verified=false`
