# Sol(max) Task660 — final path-only release audit of Task640 workflow v4

## Scope

Audit the repaired, inert workflow v4 only. Read Task657/659 mails and replies
and the Task658 blocker report if already complete. No optional hardening,
implementation edit, production run, GHA dispatch, or git.

Frozen inputs:

| file | bytes | LF lines | SHA-256 |
|---|---:|---:|---|
| committed released v3 workflow | 9,959 | 160 | `f0dabf6a9cef421f6849391fcb1b2e2f229333d90eab61fb61a0fe95dcdc8ac4` |
| `.github/workflows/d972-r07-a0-fresh-precision2-endpoint-v4.yml` | 10,038 | 161 | `3a91aca913faf79dadd0e16d181c6e270df660ead0b19acbd6045b2f7cfb92fb` |
| `sol/luna_reply_657_r07_task640_artifact_root_path_v4.md` | 1,179 | 24 | `daaf93cfa8b2f640b9176432aafeed02cce9b6e007538030f1a1c19a593035c7` |
| `sol/luna_reply_659_r07_task640_v4_inert_line_repair.md` | 811 | 17 | `8feedc8747e2e37a645b807751d6767b8f4376155a5bee6a26267ae7da477908` |

Stop on `INPUT_MISMATCH`.

Confirm exactly:

1. the Task625 verdict remains at the download root;
2. exactly four payload consumers use `task625/task625-payload`;
3. after normalizing v3/v4 identity/self-path/fire/output labels and the inert
   guard, those four path changes are the only semantic delta;
4. `false &&` is present and effective;
5. YAML, exact code/reply/parent/resource pins, full action pins, caps,
   downloads, and success-only upload are unchanged/valid.

Do not rerun Python mathematics. Write only
`sol/sol_reply_660_final_audit_r07_task640_artifact_root_v4.md` and return
`PASS_PATH_ONLY / SAFE_TO_DISPATCH_GHA=yes` or one concrete required blocker.
A PASS authorizes only a replacement Task640 run and no mathematical claim.
