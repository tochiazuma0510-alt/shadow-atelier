# Luna reply 428 — v9 Linux bootstrap trace

Implemented the three task428 outputs only. The wrapper is diagnostic and calls
the pinned v9 `run()` once with `seconds=0`, no checkpoint/resume, and the 4.8 GB
RSS cap. The expected `RuntimeError("UNKNOWN_RESOURCE:time_limit")` is classified
as `BOOTSTRAP_READY`; any other exception is bounded to 40 traceback frames and
16 KiB and classified as `TRACE_CAPTURED`.

Pinned v9 input:

- `search/d972_r07_a0_pb34_direct_quotient_owner_v9.py`
- 26006 bytes
- SHA-256 `98efac926970a5c3aa23a43b100ae64c52ce60ab0313d151f88b4dc37e6bd611`

New output pins:

- `search/d972_r07_a0_pb34_direct_quotient_bootstrap_trace_v1.py`: 2716 bytes, SHA-256 `7407e2b97623fef949955db432f31c64ec51a523da1686e007f380c19d785b94`
- `search/d972_r07_a0_pb34_direct_quotient_bootstrap_trace_gha_driver_v1.g`: 1669 bytes, SHA-256 `1feedb0b9b3ead7ed69c823afbe0a1a6f03adfaffc17bc24cd48f31c6244b8a7`

Bounded local gates:

```text
python -m py_compile search/d972_r07_a0_pb34_direct_quotient_bootstrap_trace_v1.py
PASS (exit 0)

python -B search/d972_r07_a0_pb34_direct_quotient_bootstrap_trace_v1.py --mode FIXTURE
R07_A0_V9_BOOTSTRAP_TRACE_V1 READY
R07_A0_V9_BOOTSTRAP_TRACE_V1 TRACE_CAPTURED
R07_A0_V9_BOOTSTRAP_TRACE_V1 FIXTURE_PASS {"status":"FIXTURE_PASS","toy_ready":true,"toy_trace_captured":true}
PASS (exit 0)
```

The real v9 bootstrap was not invoked locally, as required. The GHA driver
requires the external preamble
`D972_R07_A0_V9_BOOTSTRAP_TRACE_V1_RUN:=true`, then provides the one real
Linux-GHA trace call, live `tee`, exact wrapper pin, one terminal marker,
receipt check, and a distinct final marker. No production
search, workflow edit, commit, push, or dispatch was performed.

TRACE_V1_LOCAL_GO_FOR_PARENT_DISPATCH

## Parent dispatch receipt

- independent Sol verdict: `GO` for the bounded Linux traceback gate;
- dispatch commit: `501b8787903c3ee1ac46bb38b8b6d6b59fa0a630`;
- branch: `sol/r07-explicit-lift-20260825`;
- workflow: `gap-run.yml`;
- run id: `33318852115`;
- job id: `99277131484`;
- preamble: `D972_R07_A0_V9_BOOTSTRAP_TRACE_V1_RUN:=true;;`;
- workflow timeout: `15` minutes;
- initial state at dispatch: `in_progress`.
