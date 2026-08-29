# Luna reply 406: final A0 two-phase streaming resume v27

The dispatchable successor is now the v26 producer, v27 checker, v27 driver,
and v27 dedicated workflow below.  No local production run, GHA dispatch,
commit, push, generic-workflow edit, or batch/SAT change was made.

## Final dispatch set

| path | bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_history_free_positive_fast_resume_v26.py` | 5950 | `4ae9de2eaf0ae337d48309f107fe7aef94afe3783ee2bde63b7c839364e1098e` |
| `crosscheck/check_d972_r07_history_free_positive_fast_resume_v27.py` | 1964 | `181553ce338d1ef65e9ca275a41b157c2e4f8f4a8ca8616a63f3b5a144a045a3` |
| `search/d972_r07_history_free_positive_fast_resume_gha_driver_v27.g` | 5779 | `f43a1e9c1b403012880a17ed7b3f53f748f1743cac3d49037a8cde3a5936ab14` |
| `.github/workflows/d972-r07-a0-streaming-resume-v27.yml` | 4743 | `5e5932ee9a01aee4fb57162f681214c38acfa91f079315d8f44df7399a8dde16` |

The following frozen owner layers are runtime dependencies of that final set
and must be included in the same commit:

| path | bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_history_free_positive_fast_resume_v25.py` | 3870 | `8aad1fb0eb0f00e63ffe59d33f71bb89f65a63731084b668f10be587ba343460` |
| `crosscheck/check_d972_r07_history_free_positive_fast_resume_v26.py` | 1961 | `68fc28166e848d22d8e3b2731636c186733ce545a5e3fc313c14a5d4ce0d2d95` |

The temporary driver/workflow v26 drafts were discarded; only v27 is a
dispatch candidate.

## Closed blockers

1. The workflow checks out exactly `${{ github.sha }}`, so the committed
   successor files exist.  The old run is bound separately through GitHub API
   gates for run `33267817818`, head
   `8227ecd4cb12f7efc8e2419306b847e228a78f36`, artifact id `9721440597`, and
   name `gap-run-out`; a small binding receipt is written to `ci/out`.
2. Producer v26 pins frozen v13 (`147409` bytes,
   `4d1be83fefbb1a1c0b23010825c0013b80650439b714dce7e35a6e0f53a2ff2a`),
   mechanically extracts the literal keys of `Search.checkpoint_body`, adds
   `self_digest`, and requires exact equality with the streaming transport's
   32 canonical keys.  This includes `next_clean_boundary_epoch` immediately
   after `new_records`.
3. Restore is genuinely two-phase.  Before the first streamed record it
   authenticates/restores formal DAG, old pivot bindings, monitor counters,
   cleanup owner and accounting--only fields already read.  After the entire
   top-level object is parsed it binds `next_clean_boundary_epoch`; the
   source/basis/remainder/current-dual/final semantic gates then run before the
   boundary owner starts.  Empty and nonempty `new_records` take the same two
   phases.
4. `ci/in/prior` is not uploaded.  `if: always()` uploads only `ci/out`, which
   contains the successor checkpoint/receipt/verdict/logs and the small prior
   binding receipt.
5. The workflow installs pinned official GAP 4.16.0 using the same release URL
   and SHA-256 as `gap-run.yml`, builds it, and runs the version smoke gate.
   The producer outer cap is 11,100 seconds around the unchanged 10,800-second
   internal budget; the transport checker cap is 1,800 seconds; the job cap is
   245 minutes.  Output upload uses compression level zero to leave practical
   headroom for the large successor checkpoint.
6. Driver v27 requires exact producer/checker/source/manifest/resume bytes and
   hashes, runs the checker on the typed producer receipt, requires nonempty
   receipt and verdict, exactly one producer and checker terminal, identical
   terminal text, and zero statuses for both pipeline members.

The frozen resume member remains exactly
`d972_r07_history_free_positive_fast_resume_v24_checkpoint.json`,
`1663424241` bytes, SHA-256
`55c463335e89fb7e67a04ec9c0405a8216f6f909b2ce67a0fe7a8a4afaf2014d`.

## Memory statement

The avoidable transport allocation is bounded by the 1 MiB read chunk plus a
single JSON token/current record.  Each record's temporary raw token is
released after parsing.  Its authenticated semantic dictionary is retained in
`search.new_records`, because later formal-solution reconstruction needs the
old live record; the formal DAG/reducer and other semantic state are likewise
necessarily retained.  There is no full 1.66 GB bytearray, bytes copy, decoded
ASCII string, or whole-checkpoint DOM.  The generated production resume call
has exactly one `_stream_resume(...)` owner and no call to the legacy
`restore_checkpoint(search, resume_path)` path.

## Local gates

- Both final Python files compile and their `--help` paths execute.
- Generated source gate:
  `A0_V26_GENERATED_OWNER_PASS 165550 634d4d6d646e3736d81b31730ab53d97ef639b4ca280c2af26828f65a2d79110`.
- Actual-key fixture:
  `A0_V26_ACTUAL_KEYS_FIXTURE_PASS 32 823`.  It accepted the canonical sealed
  32-key fixture and rejected byte/SHA mismatch, seal mutation,
  duplicate/missing/out-of-order top-level keys, reordered/duplicate records,
  bad DAG binding, and an over-limit restored counter.
- Driver pin gate: `A0_V27_DRIVER_PIN_PASS`.
- Workflow parse gate: `YAML_PASS timeout 245`.
- Tiny GAP fail-fast parse reached only the deliberately absent local artifact:
  `Error, task407 missing input`; no shell or producer was started.

Expected parent action after review: commit these versioned final files and
dispatch `d972-r07-a0-streaming-resume-v27.yml` at that exact commit SHA.
