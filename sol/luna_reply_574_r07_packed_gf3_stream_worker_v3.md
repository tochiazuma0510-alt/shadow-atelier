# Luna reply 574 — packed GF(3) stream worker v3

Implemented the four authorized v3 files only. The v2 files, Task565,
workflows, GHA runs and production artifacts were not modified.

## Files

| file | bytes | SHA-256 |
|---|---:|---|
| `search/d972_packed_gf3_stream_worker_v3.c` | 7208 | `a19f0dccb44985403716f3446e795e5d901adc52c91e3acafc8035db7d6ed892` |
| `search/d972_packed_gf3_stream_worker_v3.py` | 6934 | `bb449830d1d4b919592144484a7b69859d9a57e7bd722a8639e6c1f09ec97b09` |
| `search/check_d972_packed_gf3_stream_worker_v3.py` | 5857 | `e4aa7dbf90b1d5421f39b664a0b5f7c773bdd3b727e275bef8ced24a349f1185` |
| `sol/luna_reply_574_r07_packed_gf3_stream_worker_v3.md` | measured after close | measured after close |

The v3 protocol is fixed binary framing with echoed uint64 IDs, typed
`DEPENDENT`, `ACCEPTED`, `UNKNOWN_RESOURCE`, `MALFORMED`, and `FATAL` statuses,
ordered reduction pairs, and optional dependent companion payloads. The
worker updates its live lead map and accepted basis before acknowledging a
new pivot, permits dependent offers at full rank, and uses one EOF offset per
offer boundary. The client accepts byte-oriented views and has no timeout or
implicit Python fallback. The checker uses dense GF(3) coordinates and does
not import the wrapper or C source.

## Checks

```text
$env:PYTHONPYCACHEPREFIX=Join-Path $env:TEMP 'd972-stream-v3-cache'
python -B -m py_compile search/d972_packed_gf3_stream_worker_v3.py search/check_d972_packed_gf3_stream_worker_v3.py
python -B -u search/check_d972_packed_gf3_stream_worker_v3.py
```

Both commands exited 0. Final checker result:

```json
{"checkpoint_resume": "PASS", "companion": "PASS", "compiled_service": "NOT_RUN_NO_COMPILER", "dynamic_closure": "PASS", "expression_replay": "PASS", "fixture": "PASS", "frozen_cases": 6, "member_nonmember": "PASS", "mutations_rejected": 13, "offset_eof": "PASS", "random_rows": 40, "reference_seconds": 0.021961}
```

Pure fixtures cover the six frozen reducer cases and chained trace, dense
random rows, expression replay and target remainder styles, dynamic closure,
companion normalization/dependent handoff, offset EOF parsing, checkpoint
protocol, and semantic/malformed mutation categories. The bounded v454
envelope is represented by argument-bound rank/offer/byte caps; no obsolete
36,288-rank static-input gate is introduced.

`Get-Command clang,gcc,cc,cl -ErrorAction SilentlyContinue` found no local C
compiler. Consequently the actual C service, compiled differential fixture,
RSS, and compiled timing were not run and no speedup is claimed. The pure
checker is not evidence of compiled execution; independent C compilation and
full resumable/companion calibration remain mandatory. No grade-two production
or mathematical terminal follows.

TASK565 INTEGRATION: not performed
CURRENT GRADE-ONE RUNS: unchanged
GRADE-TWO PRODUCTION: not launched
MATHEMATICAL TERMINAL: none
verified=false

PACKED_GF3_STREAM_WORKER_V3_CANDIDATE_AUDIT_REQUIRED
