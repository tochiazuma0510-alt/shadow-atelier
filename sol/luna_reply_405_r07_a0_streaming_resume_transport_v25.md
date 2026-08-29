# Luna reply 405: A0 streaming resume transport v25

Implemented only the requested versioned successors; no production computation,
GHA dispatch, commit, push, or generic-workflow edit was performed.

## Changed paths and frozen bytes

| path | bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_history_free_positive_fast_resume_v24.py` | 16956 | `b151b6c858de556145bc58b13037ea8b193f068a93c3d0383c1769613c3cea74` |
| `crosscheck/check_d972_r07_history_free_positive_fast_resume_v25.py` | 1979 | `f0056fc956bbf39e270526afb539a9559a564804e0aef60ec59cb0fe2382ee9c` |
| `search/d972_r07_history_free_positive_fast_resume_gha_driver_v25.g` | 5570 | `af6b838518ba8b4884a27f99a48f07ce9f78703dbd6a6f4e7d163bb0f589e626` |
| `.github/workflows/d972-r07-a0-streaming-resume-v25.yml` | 1897 | `5481dbb2fec73adcb6e9cebc6c0f7d0fb195db94425e0125ea4cb0dde2427b57c` |

The producer is generated from the frozen v23 owner (`3729` bytes,
`0e7ad85d5328b86b57086ca4710520ce748e591e0a0e1cc93cedeba3850fb8f3`).
The checker is generated from frozen checker v24 (`1627` bytes,
`7b35c39a3ab7204bfd3251740211c23addf130dc1f9bf9a5cbaf3d1162155ac0`) and
pins the exact v24 producer bytes above.

## What changed

The `--resume` call in the generated production owner now uses a bounded
reader.  It reads at most a 1 MiB transport chunk, updates raw SHA-256 while
reading, and never constructs the former full-file `bytearray`, `bytes`, giant
ASCII string, or JSON DOM.  Top-level keys are required exactly once, in the
canonical sorted order, with no missing or trailing fields.  The top-level
self-seal is checked incrementally by hashing the canonical body while the
`self_digest` member is suppressed.  Physical regular-file, TOCTOU, pathname,
size, and SHA checks remain in force.

`new_records` is parsed item-by-item.  Each item is authenticated and injected
before the next item is read; symbol order, row digest, pivot range/DAG binding,
and the existing reducer checks remain active.  The existing formal DAG and
semantic source/basis/current-dual/counter/cleanup/heavy gates are retained;
the restored reducer is the only intentionally large live structure.  Thus the
old DOM reader remains available only to the legacy tiny selftest path and is
not reachable from production `--resume`.

The driver pins the prior artifact member from run `33267817818`:
`d972_r07_history_free_positive_fast_resume_v24_checkpoint.json`, exactly
`1663424241` bytes with SHA
`55c463335e89fb7e67a04ec9c0405a8216f6f909b2ce67a0fe7a8a4afaf2014d`.
It retains the old source-cardinality/manifest pins, runs the producer with the
existing `10800` second internal budget, captures visible terminal logs, and
invokes the matching checker whenever a receipt exists.  The workflow checks
out the frozen head, downloads the same-repository artifact with
`github.token` and pinned download-artifact, authenticates the member before
starting Python, and uploads `ci/out` plus the downloaded input under
`if: always()`.

## Gates run

Commands used (all local and non-production):

```text
python -m py_compile search/d972_r07_history_free_positive_fast_resume_v24.py crosscheck/check_d972_r07_history_free_positive_fast_resume_v25.py
python search/d972_r07_history_free_positive_fast_resume_v24.py --help
python crosscheck/check_d972_r07_history_free_positive_fast_resume_v25.py --help
```

A temporary fixture extracted only the bounded reader, accepted a valid small
JSON array, and rejected trailing-byte mutation; the full canonical top-level
fixture also passed incremental seal verification.  Observed results:
`A0_STREAM_FIXTURE_PASS bytes=18 peak_raw_buffer<=1048576` and
`A0_STREAM_SEAL_FIXTURE_PASS 751`.  Static source
checks cover byte/SHA pinning, seal mutation, duplicate/missing/out-of-order
top-level keys, reordered/duplicate `new_records`, bad pivot/DAG binding, and
wrong restored counters.  No 1.66 GB file was created or read locally.

Expected dispatch inputs are the workflow's fixed source head
`8227ecd4cb12f7efc8e2419306b847e228a78f36`, prior run `33267817818`, artifact
`gap-run-out`, and the exact checkpoint member/hash/size stated above.
