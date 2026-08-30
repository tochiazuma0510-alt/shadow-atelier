# Luna task 432 — A0 sequence-40 prefix-positive probe v1

Implement the smallest positive-only fork justified by
`sol/proof_r07_a0_prefix_positive_checkpoint_fork_v408.md`.  This is a
parallel probe of the existing rank-1316 checkpoint, not a replacement or
repair of the running task431 continuation.

## 1. Allowed outputs

Create only:

1. `search/d972_r07_a0_prefix_positive_probe_v1.py`
2. `search/d972_r07_a0_prefix_positive_probe_gha_driver_v1.g`
3. `sol/luna_reply_432_r07_a0_prefix_positive_probe_v1.md`

Reuse the unchanged task431/v12 checker.  Do not modify v12, its checker,
any workflow, v220, proof papers, or any other file.  No commit, push,
dispatch, download, or local production run.

## 2. Minimal implementation shape

Byte-pin and import the current task431/v12 producer:

```text
search/d972_r07_a0_pb34_direct_quotient_owner_v12.py
bytes 51884
sha256 3016b6a21d9fafbf037dbb5384dcca81f49e1fa44ae45a466ff16f1fd13948b3
```

Do not copy or rewrite its 52 KB implementation.  Use a local subclass of
`collections.deque` which retains length, iteration and content but whose
truth value is false.  Temporarily bind the imported v12 module's `deque` to
that class and call its existing `run` on the exact resume input with:

```text
resume_v11_url = None
checkpoint     = None
seconds        = 9000
rss_bytes      = 4800000000
```

This makes the v12 runner restore and authenticate the exact sequence-40
occurrence state, skip only the `while queue` actor loop in the probe process,
then reuse its existing physical aggregation, payload release, six-action
oracle and positive replay.  Require the input whole seal independently in
the wrapper before the call:

```text
bytes  326449173
sha256 0b3169fe6e7051fe46a28bb966ffd3dfeada841dce1a6fe2358959dd99402ff1
```

The input must be a relative regular non-symlink path under `ci/out`, and the
output JSON must be fresh.  Reset the imported module's mutable global result
state before the call.  Restore the original `deque` binding in `finally`.

Emit the same v12 candidate-envelope ABI expected by the unchanged checker,
plus an informational `prefix_probe` object containing the pinned input,
original rank/frontier and `positive_only=true`.  Keep every claim-boundary
flag false.  Because the unchanged v12 checker requires an output checkpoint
for a top-level `UNKNOWN_RESOURCE`, while this fork intentionally emits none,
the only top-level terminals are `COMMON_CANDIDATE` and `UNKNOWN`.  Preserve
an underlying resource stop inside the `a0`/`prefix_probe` reason fields, but
normalize its envelope status to `UNKNOWN`.  Translate `six_action_exhausted`
to an explicitly positive-only UNKNOWN reason.  Never emit COMMON_WORD or
NONMEMBER.  Never write a checkpoint.

## 3. Driver

Start from the already audited task431 recovery logic, changing only the
producer/output/log names and the producer invocation.  Preserve exactly:

- permanent release asset URL and zip/checkpoint bytes/SHA;
- exact six-name v12 roster;
- temporary same-directory download/extraction;
- regular-file and dangling-symlink gates;
- hash-bound seal and distinct one-shot completion receipt;
- GAP exact receipt-content comparison;
- external preamble requirement.

The driver invokes the probe with the recovered v12 checkpoint as input,
9,000 seconds and 4.8 GB, then invokes the unchanged v12 checker with
`--input-checkpoint` and no output checkpoint.  It requires unique producer
and checker PASS markers.  Use distinct probe artifact/log/receipt names so
it cannot collide with task431.  `ci/out` remains the artifact directory.

## 4. Bounded gates only

Run only seconds-scale checks:

1. AST/compile without leaving repository bytecode;
2. wrapper fixture proving the false-truth deque preserves all elements and
   length while suppressing the actor loop;
3. imported v12 fixture and unchanged checker self-test;
4. static proof that no checkpoint argument/write is possible in probe mode;
5. reconstructed GAP `Concatenation` command, including the exact one-line
   receipt;
6. `git diff --check` on the three outputs.

Do not load the 326 MB checkpoint locally.  Report exact bytes/SHA and an
explicit list of untouched files.  A candidate remains unpromoted until the
strict replay policy in v408 section 4 is met.
