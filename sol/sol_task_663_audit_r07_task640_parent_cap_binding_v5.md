# Sol(max) Task663 — cap-only audit of Task640 workflow v5

Read Task662 mail/reply and independently compare released v4 with inert v5.
Audit only the `manifest_binding` repair. No optional hardening, edits,
production, GHA, or git.

Frozen inputs:

| file | bytes | LF lines | SHA-256 |
|---|---:|---:|---|
| released v4 workflow | 10,023 | 160 | `c8deb31cf87554500d665ab6a9740af0529204858d5ec30a91be5b55735dac58` |
| `.github/workflows/d972-r07-a0-fresh-precision2-endpoint-v5.yml` | 10,076 | 162 | `88f5169806ae83202aadbdba0c3505bf754cccc61131064d373a4e65946c664e` |
| `sol/luna_reply_662_r07_task640_parent_cap_binding_v5.md` | 951 | 22 | `a8f5593939fbb05b4a06c052922ffa123ce2ece7ff7e59549fb628beec7b8015` |

Confirm that accepted Task625 v3 used
`TASK625_ACCUMULATED_CAP=50000000`, that the pinned old checker reads precisely
this key into `manifest.resource_caps`, and that default 2,000,000 caused the
observed mismatch (accepted replay accumulated 2,605,954 states). Normalize
v4/v5 identity/self/fire/output labels and inert guard; the added cap line must
be the sole semantic delta. Recheck YAML, full action/code/reply/parent pins,
the four nested payload paths, root verdict, other caps/downloads, and
success-only upload unchanged.

Write only `sol/sol_reply_663_audit_r07_task640_parent_cap_binding_v5.md`.
Return `PASS_CAP_ONLY / SAFE_TO_DISPATCH_GHA=yes` or one concrete blocker. A
PASS authorizes only a replacement Task640 run and no mathematical claim.
