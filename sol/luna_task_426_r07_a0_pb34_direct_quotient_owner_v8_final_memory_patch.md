# Luna task 426 — v8 final memory-safe dispatch patch

## Verdict and strict scope

Task425/v7 is **NO-GO for dispatch**, but its five substantive production-loop
repairs, seed resume, boundary-free quotient, v3-only dependency, pins and fresh
GAP driver all passed independent audit.  Make one versioned v8 patch containing
**only** the three final blockers below.  Do not redesign the search, add audit
machinery, reconstruct an old boundary closure, or change the mathematics.

Allowed new outputs only:

1. `search/d972_r07_a0_pb34_direct_quotient_owner_v8.py`;
2. `crosscheck/check_d972_r07_a0_pb34_direct_quotient_owner_v8.py`;
3. `search/d972_r07_a0_pb34_direct_quotient_owner_gha_driver_v8.g`;
4. `sol/luna_reply_426_r07_a0_pb34_direct_quotient_owner_v8_final_memory_patch.md`.

Read task425, its four v7 outputs, and this task.  Copy v7 to standalone v8,
keeping the same pinned v3 ABI and no v6/v7 runtime dependency.  Update all
schemas, checkpoint headers, markers, identifiers and unique filenames to v8.
Do not edit any old file, workflow, proof, v220 paper, checkpoint or artifact.
Do not run production locally, commit, push or dispatch.  Run only compile and
seconds-scale executable fixtures/self-tests.

## 1. Checker must never retain or decode a full checkpoint twice

The v7 checker's `checkpoint` reads the complete compressed payload into `raw`,
wraps it in `BytesIO`, and the main path can retain decoded input plus decoded
output and decode output a second time.  This is a dispatch blocker near the
4.8 GB owner cap.

Split the operation conceptually into:

- a streaming seal check which reads the first line, then hashes/counts the
  remaining compressed bytes in bounded chunks and returns the whole-file
  bytes/SHA plus authenticated header data; and
- a state decoder which first performs that seal check, then reopens the file,
  skips the header, and calls `marshal.load` through
  `gzip.GzipFile(fileobj=f, mode="rb")` directly.

There must be no `f.read()` without a bounded size, no full compressed `raw`, no
`BytesIO`, and no second output decode.  For the input checkpoint, perform only
the streaming seal/identity comparison required by the artifact and do not
retain a decoded input state.  For an existing output checkpoint, decode it
exactly once and reuse the same `(n, h, state)` for durable-summary agreement,
output identity, and the `UNKNOWN_RESOURCE` result.  If output does not exist
and status is ordinary fail-closed `UNKNOWN`, do not try to decode it.

Retain all v7 state-shape, source-allowlist, boundary-invariant and candidate
checks for the one decoded output state.  Remove the now-unused `io` import.

## 2. A restored state already at the cap stops without another serialization

Immediately after authenticated resume restore and construction of its scalar
durable summary, measure owner RSS.  If it is at or above `--rss-bytes`, return
without seed/parent/action work and without calling `save`/`cp_write`:

```text
status = UNKNOWN
reason = MEMORY_STATE_LIMIT
durable_state = authenticated input scalar summary
```

This is deliberately fail-closed `UNKNOWN`, not `UNKNOWN_RESOURCE`, because no
new output checkpoint is created.  The artifact must still bind and seal the
immutable input checkpoint.  The checker/driver must accept this exact case
when the named fresh output path is absent; it must not require or synthesize an
output checkpoint.  For a restored state below the cap, discard the temporary
outer restored-state container if useful and continue exactly as v7.  Preserve
the ordinary elapsed/RSS guard behavior for work in progress: it atomically
saves a fresh output checkpoint and reports `UNKNOWN_RESOURCE`.

Add a bounded toy fixture for the no-save `MEMORY_STATE_LIMIT` branch without
allocating a large state or bootstrapping production.

## 3. Candidate metadata uses the selected durable fallback

In `main`, compute one scalar object such as

```python
final_durable = o.get("durable_state") or LAST_DURABLE
```

once after the run.  Use that same object both for `result["durable_state"]`
and, if an output checkpoint exists, for `result["checkpoint"]["sequence"]`.
Do not read the sequence only from `o.get("durable_state")`: a positive
candidate normally relies on the last sealed fallback and must not report zero.
Add a small fixture/assertion proving a candidate-shaped result selects a
nonzero fallback checkpoint sequence.

## Preserved dispatch gates

- The correct v7 physical aggregation and reachable positive terminal remain
  byte-for-byte in behavior.
- No old boundary rows or originals maps; `eliminated_boundary_rows=0` and
  `old_boundary_closure_present=false`.
- One owner process, RSS cap `4_800_000_000`, no Python fan-out.
- Distinct immutable input and fresh output checkpoint paths.
- Initial fresh GHA run has no input checkpoint.
- Driver uses the generic GAP-run workflow contract; no workflow edit.
- Driver pins the exact v8 producer and checker bytes/SHA and has no stale v7
  paths, schemas or markers.
- Checker rejects `COMMON_WORD`; `COMMON_CANDIDATE` remains an unpromoted
  envelope with every public claim flag false.

Report exact commands, outputs, bytes and SHA-256.  Give line/function evidence
for each of the three repairs and explicitly state that no other search logic
changed.  End with `V8_LOCAL_GO_FOR_PARENT_DISPATCH` or a precise `NO-GO`.
