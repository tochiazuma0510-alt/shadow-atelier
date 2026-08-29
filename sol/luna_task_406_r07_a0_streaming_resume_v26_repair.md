# Luna task 406: repair A0 streaming resume v25 before dispatch

Role: Luna.  Versioned implementation repair only; no commit, push, dispatch,
production run, or edit of v24/v25 candidate files.

Parent pre-audit rejects v25 for three concrete reasons:

1. The workflow checks out prior artifact head
   `8227ecd4cb12f7efc8e2419306b847e228a78f36`, which cannot contain the new
   v24 producer/checker/driver.  The successor must check out the exact
   workflow-dispatch head (`github.sha`).  The prior run/head remains a
   separately authenticated input-artifact identity.
2. `_RESUME_TOP_KEYS` omits `next_clean_boundary_epoch`, although the frozen
   terminal checkpoint contains it and `_stream_prepare` requires it.  Derive
   the complete canonical top-level key roster from the frozen owner/checkpoint
   construction, assert it statically, and use the exact order.  The small
   fixture must include the actual full key roster and pass through the same
   production parser entry point.
3. Do not re-upload `ci/in/prior/`: that needlessly recompresses the 1.66 GB
   immutable prior member.  Upload only new receipt/checkpoint/verdict/logs and
   a small input-binding record.

Recheck fail-closed exit propagation, internal 10,800-second budget, external
timeout/checker/upload headroom, exact prior member bytes/SHA, and periodic
progress.  Preserve v23 mathematics, one-column order, caps, and worker
lifecycle.  Incorporate any later Sol(max) v25 audit defects supplied by the
parent.

Create only new versioned producer/checker/driver/workflow and
`sol/luna_reply_406_r07_a0_streaming_resume_v26_repair.md`.  Report exact
paths, bytes, SHA-256, gates, and intended dispatch contract.
