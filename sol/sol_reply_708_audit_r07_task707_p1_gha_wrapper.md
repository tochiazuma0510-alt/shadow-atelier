# Sol(max) Task708: inert P1 GHA wrapper audit

## Verdict

`PASS_P1_GHA_WRAPPER`

`SAFE_TO_DISPATCH_GHA=yes`

`verified=false`

The exact frozen wrapper is internally consistent and safe for root to make
live and dispatch.  I performed only bounded YAML/static checks: no replay,
artifact download, production or GHA action, git operation, or implementation
change.

## Audited receipts

| path | bytes | LF count | final LF | SHA-256 |
|---|---:|---:|---|---|
| `.github/workflows/d972-r07-p1-structural-replay-v1.yml` | `11950` | `206` | yes | `f25893d8ebc8bdd2c3d972e044c5b42fd8fa3e2ba7a279a84c1c774edc90e775` |
| `sol/luna_task_707_r07_p1_structural_replay_gha_wrapper.md` | `2928` | `23` | yes | `e3815e1aa79d54e24e4069adfad9d3d6ab903a9fe5ebe4cf4adb8b9d183f7e12` |
| `sol/luna_reply_707_r07_p1_structural_replay_gha_wrapper.md` | `2252` | `55` | yes | `1633c918a290c872966db31db79a52d2b949505d72f3b30047ef118548e19851` |
| `sol/sol_reply_705_audit_r07_task704_p1_finite_repairs.md` | `5590` | `115` | yes | `84380d4cacb2ffb21c6a95a19a5309394c76a9008257c4b7ed6881a3e5201675` |
| `sol/luna_task_699_r07_p1_four_block_structural_ingest.md` | `4231` | `79` | yes | `483c75985cbd8b26fd7e26db3fe598a0e4feff7ddffdf3ed25809cc70fce408a` |
| `sol/luna_reply_699_r07_p1_four_block_structural_ingest.md` | `2865` | `56` | yes | `a08d6407d80305323559ec7a89e9cf1ba4b2ed839f552ecdee55a49c1954d9f4` |
| `sol/sol_reply_702_audit_r07_task699_p1_structural_ingest.md` | `9478` | `142` | yes | `34ff2f6c79f79c4f08896c969951256ef83dc6aca6803481b00858f24100c93d` |
| `search/d972_r07_grade2_specific_owner_prejoin_v1.py` | `47995` | `545` | yes | `38fcbe3757d1b14fd19f4f557f763c1f5f6a2e8da47e0e061707cf28c5064d73` |
| `sol/sol_task_708_audit_r07_task707_p1_gha_wrapper.txt` | `1588` | `9` | yes | `86f1ed325a969d7b132765a860e32035ffad9ca157d2ce880118cd60a579a094` |

The workflow and producer receipts exactly match the frozen claims.

## Trigger, checkout, and source authentication

The workflow has one job, read-only `contents`/`actions` permissions, Python
3.13, thread-count-one environment variables, pinned 40-hex action revisions,
and a 45-minute job cap (`:1-58`).  Checkout explicitly uses
`ref: ${{ github.sha }}`.  Before any download, the job recomputes the exact
producer SHA-256, 47,995-byte size, 545 LF count, and final byte 10
(`:59-69`).

The only automatic trigger is a push to
`sol/r07-explicit-lift-20260825` touching the producer or this workflow;
manual dispatch is the only other trigger (`:2-8`).  The current job guard is
exactly

```text
${{ false && (github.event_name == 'workflow_dispatch' || contains(github.event.head_commit.message, '[fire-p1-structural-replay-v1]')) }}
```

so the job is inert now.  Removing only `false && ` produces the valid live
condition accepting either `workflow_dispatch` or the exact push marker
`[fire-p1-structural-replay-v1]`; it does not broaden the configured push
branch/path trigger.

## Exact five-parent binding and layout

The workflow literals at `:18-43` exactly equal the producer's frozen
`SERVICE` tuple: source run/attempt/head
`33677346616/1/22c6dddb43d107c05e65f53ad898823ae8ebe276`, followed by all five exact
artifact IDs, names, sizes, and `sha256:` digests.  For each artifact, the
pre-download API gate checks ID, name, byte size, digest, non-expiry,
workflow-run ID, and workflow-run head (`:70-84`); the run endpoint then
checks that same run's ID, attempt, and head (`:85-87`).  A failed or missing
API field therefore stops the job.

Five exact-name/same-run downloads use five distinct roots
`p1-prepare,p1-block-0,...,p1-block-3` (`:88-122`).  Before execution, the
wrapper requires `prepare.HEAD` and 15 top-level files, and each indexed
`block-i.HEAD` and three top-level files (`:123-134`).  The authenticated
producer subsequently applies its accepted exact member roster, canonical
byte, and pinned body/basis checks inside those roots; no merged-download
layout or broad artifact pattern is used.

## Serial replay and exact assertions

Compilation and the bounded selftest precede one, and only one, production
command (`:135-150`).  The command is a single serial Python process under a
40-minute inner timeout and `/usr/bin/time -v`; it passes the prepare root
once and the four block roots in the required `B0,B1,B2,B3` order.  Stdout,
producer stderr, and timing output have distinct paths.

The post-run gate parses stdout as JSON and asserts the exact terminal,
`[1509,1512,1512,1512]` ranks, exact nine offsets, 8,059 rows/distinct/
coefficient-one leads, and true global echelonicity (`:157-167`).  All eight
charged Task699/702 lead receipts are literal assertions: four combined
summary digests at `:168-171` and the four ordered block-local digests at
`:172-173`.  The values exactly match the frozen counters.  It also requires
`resident_matrix`, `semantic_equations_replayed`, `precision2`, and
`verified` all to be the boolean singleton false (`:174-175`).

The same assertion step rereads and rechecks the producer SHA/bytes/LF/final
LF, then emits a canonical one-line receipt binding event head, the complete
producer receipt, all five authenticated artifact identities plus source
run/attempt/head, and result SHA/bytes/terminal/ranks/offsets/counters
(`:176-185`).  The result SHA binds the complete asserted JSON, including
the lead fields not repeated in the small receipt.

The result and receipt upload is guarded by `success()` and treats a missing
file as an error; thus it cannot publish an acceptance artifact after an
authentication, replay, or assertion failure (`:187-197`).  Logs alone are
uploaded under `always()` (`:198-206`).  Both uploads use 90-day retention and
compression level zero.

## Bounded static result and claim boundary

Base-loader YAML parsing, literal producer-`SERVICE` comparison, action/call
census, unique-root census, and parsing of the embedded Python assertion code
all passed.  The normalized census is one inert job, 14 steps, five exact API
artifact authentications, five exact downloads, one serial replay, one
assertion/receipt step, one success-only result upload, and one always-log
upload.  No matrix, parallel Python, dense matrix construction, independent
checker, semantic equality replay, Task640 join, precision-two result, or
grade-two claim is introduced.  I found no deterministic shell/YAML/API/
layout failure, missing charged receipt binding, or unnecessary slow release
step within Task708's stated boundary.

Actual P1 structural promotion still awaits the successful GHA run terminal
and its exact result/code receipt.  The later independent checker and
semantic equality replay remain separate gates.  This audit authorizes the
wrapper release only and makes no verified or grade-two claim.
