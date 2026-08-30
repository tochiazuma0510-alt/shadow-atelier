# Luna task 428 — v9 Linux bootstrap traceback gate

## Scope

Fresh v9 GHA run `33318299384` (commit
`530a29014fc0de20176d4f41a5032ffa787e973f`) passed the earlier `load` site but
stopped before both owner markers with fail-closed `UNKNOWN`, reason `"6"`.
There was no checkpoint and no seed/search work.  Do not guess a repair.
Build one tiny Linux-GHA-only traceback gate around the pinned v9 `run()` so the
exact failing source line is captured once.

Allowed new outputs only:

1. `search/d972_r07_a0_pb34_direct_quotient_bootstrap_trace_v1.py`;
2. `search/d972_r07_a0_pb34_direct_quotient_bootstrap_trace_gha_driver_v1.g`;
3. `sol/luna_reply_428_r07_a0_v9_linux_bootstrap_trace.md`.

Do not edit v9 or any prior file, workflow, proof, v220, checkpoint or artifact.
Do not run production locally, commit, push or dispatch.

## Wrapper contract

- Pin and isolated-load
  `search/d972_r07_a0_pb34_direct_quotient_owner_v9.py`, bytes `26006`, SHA-256
  `98efac926970a5c3aa23a43b100ae64c52ce60ab0313d151f88b4dc37e6bd611`.
- Call its real `run()` exactly once with a `SimpleNamespace` containing
  `checkpoint=None`, `resume=None`, `seconds=0`, and
  `rss_bytes=4_800_000_000`.
- This may construct the pinned bootstrap only.  It must never serialize a
  checkpoint and the first seed guard must stop before seed evaluation.
- If the call reaches the expected `UNKNOWN_RESOURCE:time_limit`, emit a JSON
  receipt with `status=BOOTSTRAP_READY` and the marker
  `R07_A0_V9_BOOTSTRAP_TRACE_V1 READY`.
- For every other exception, capture `type`, `str(exception)`, and the bounded
  Python traceback including filenames/line numbers into
  `ci/out/d972_r07_a0_v9_bootstrap_trace_v1.json`, emit
  `R07_A0_V9_BOOTSTRAP_TRACE_V1 TRACE_CAPTURED`, and return zero so the generic
  workflow reaches its always-upload artifact step.  This is diagnostic only;
  `TRACE_CAPTURED` is not PASS and must never be called a search result.
- Put no full mathematical state, input contents, checkpoint object, secret or
  environment dump in the receipt.  Limit traceback text to a small fixed
  bound (for example the last 40 frames / 16 KiB).

## Driver

Pin the wrapper's exact bytes/SHA, require a unique preamble flag
`D972_R07_A0_V9_BOOTSTRAP_TRACE_V1_RUN:=true`, create `ci/out`, run one unbuffered
Python process with live `tee`, require exactly one of the READY/TRACE_CAPTURED
terminal markers, require the JSON receipt, and print a distinct driver final
marker.  No fan-out, no workflow edit, no production owner driver invocation.

Run only syntax compilation and a fixture which substitutes a toy `run` for
both expected time-limit and unexpected-exception receipt paths; do not invoke
the real Windows bootstrap.  Report exact commands, markers, bytes and SHA.
End with `TRACE_V1_LOCAL_GO_FOR_PARENT_DISPATCH` or precise `NO-GO`.
