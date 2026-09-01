# Luna Task488 — rank-84 continuation runtime-envelope repair v9

## Role

You are Luna.  Diagnose and repair only the immediate runtime-envelope failure
of Task484 v8.  Do not change the pinned producer/checker mathematics and do
not run production locally.

Frozen accepted v8:

```text
driver 7680 ea4794dbe13e751e661804de238553b5607120c2f04d498fcc2a88fdaaed3edb
producer 12215 0140447110cfa568a77300bd7d43d51c622597704b7b91ed5209c63168c9ef37
checker 3653 e1b80c586985f5113b300508f6bc78d055a37243e3fd6795b8f81148b0988de1
```

GHA run `33543290399`, job `99974575290`, head
`301307802e6b174a94c0f63f284d3af1983f9ce2` failed in one second after the
release zip had been downloaded.  Its artifact is `9814471992`, 45,706 bytes,
API digest
`23bc8f0283f8198c39f9b78285e3dbd3ba95ec9537e11c1cf7a464bc227cb138`.
The uploaded payload contains only the exact 23,004-byte release zip plus the
generic workflow files; GAP reports `task484 result/checker missing`.  Hence a
silent `set -e` preflight gate failed before producer execution.

## Required repair

1. Download/inspect the failed artifact and reproduce the exact generated
   shell preflight in an external temporary directory with tracing, but replace
   the producer/checker invocations by fail-closed sentinels.  Identify the
   first failing command exactly.  No authority construction or production.
2. Create a fresh v9 driver; do not edit v8.  Change only the diagnosed
   envelope defect.  Keep the permanent release URL, all seven member pins,
   exact rank-84 resume pin/state, one producer and one checker, fresh owned
   paths, `7500>7200`, `5200000*1024>4800000000`, checker timeout 3600, and all
   exact marker/claim boundaries.
3. Make future pre-producer failures visible in an owned diagnostic log without
   weakening `set -euo pipefail`.  Do not enable noisy production xtrace.
4. Run bounded archive/source pins, generated-shell `bash -n`, a preflight-only
   execution that reaches the producer sentinel, GAP parse, and static exact-one
   process/resource gates.  Do not dispatch GHA, git, producer, or checker.

## Exact outputs

1. `search/d972_r07_a0_actual_tau_free_rank84_resume_gha_driver_v9.g`
2. `sol/luna_reply_488_r07_rank84_driver_runtime_repair_v9.md`

End with `TASK488_R07_RANK84_DRIVER_RUNTIME_REPAIR_V9_PASS` or a typed STOP.
