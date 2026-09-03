# Sol(max) Task658 — path-only audit of Task640 workflow v4

## Scope

Independently audit only the GHA artifact-root repair from failed run
`33749395427/1`. Read Task657 mail/reply and compare the committed released v3
workflow with the new inert v4 workflow. Do not edit, dispatch, run production,
or request optional hardening.

Frozen inputs:

| file | bytes | LF lines | SHA-256 |
|---|---:|---:|---|
| `.github/workflows/d972-r07-a0-fresh-precision2-endpoint-v3.yml` | 9,959 | 160 | `f0dabf6a9cef421f6849391fcb1b2e2f229333d90eab61fb61a0fe95dcdc8ac4` |
| `.github/workflows/d972-r07-a0-fresh-precision2-endpoint-v4.yml` | 10,023 | 160 | `c8deb31cf87554500d665ab6a9740af0529204858d5ec30a91be5b55735dac58` |
| `sol/luna_reply_657_r07_task640_artifact_root_path_v4.md` | 1,106 | 23 | `d2261347cf138ed7ccc3b7d2d6e978371c21157fbe0d099ca069fef470312ff0` |

Stop on `INPUT_MISMATCH`.

## Charged checks

1. Confirm from Task625 upload lines and the failed log that download has
   `task625-verdict.json` at the download root and payload files under
   `task625-payload/`.
2. Confirm exactly four consumers use the nested payload directory: old
   checker `--payload`, replayed-verdict destination, producer `--task601`,
   and new checker `--task601`; the original verdict compare stays at root.
3. Normalize v3/v4 identity/self-path/fire/output labels and the added inert
   `false &&`; prove there is no other semantic delta.
4. Recheck YAML parse, full action pins, exact code/reply/parent/resource pins,
   time/memory caps, downloads and success-only upload unchanged. Do not rerun
   Python mathematics.

Write only `sol/sol_reply_658_audit_r07_task640_artifact_root_path_v4.md`.
Return `PASS_PATH_ONLY / SAFE_TO_DISPATCH_GHA=yes` or a concrete finite
`FAIL / SAFE_TO_DISPATCH_GHA=no`. A PASS authorizes only a new Task640 run; it
proves no rho2 or downstream mathematical claim.
