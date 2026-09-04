# Root result: canonical P1 degree-two lift v3

Date: 2026-09-04 JST

## Actual terminal

- Run/attempt: `33827142944/1`.
- Job: `100882118138`.
- Exact head: `bd1f092b8301e4a07cf0a3c8b228bff63e23276b`.
- Workflow conclusion: `failure`.
- The job passed all source authentication, the bounded selftest, the accepted
  independent-checker provenance, all five parent downloads and launch
  construction.  The producer stopped after about 40 seconds, before the
  8,059-row recurrence.

V6's new diagnostic supplied the exact terminal:

```text
status=REJECTED
phase=build.authenticate_inputs
TypeError: object supporting the buffer API required
producer line 1302: sha(body_raw)
sha line 173: hashlib.sha256(data)
```

The cause is now proved.  The pinned structural
`validate_block_envelope(...)` returns `(root, body, len(br))`; the imported
semantic wrapper propagates that integer byte length.  Producer-v6 falsely
typed/named the third value as raw bytes and passed it to SHA-256.  The earlier
packet-row hypothesis was not the reached failure site.

This is a provenance-interface type defect, not a mathematical negative,
timeout, OOM, or recurrence failure.  The no-copy repair is to retain the
integer as `body_size`, bind the already authenticated pinned digest directly,
compare the physical file size/stable identity, and let the existing registry
rehash the file.  Task781 commissions only that finite repair; it expressly
forbids rereading or canonicalizing the large JSON bodies.

## Artifact

- Logs artifact ID: `9920389460`.
- Name: `task773-canonical-p1-degree2-lift-v3-logs-33827142944-1`.
- API archive size: `83,509` bytes.
- Digest:
  `sha256:28e8acad7b01cd4c569265e450806c12a844fc158a9f4f94b7362948c76e8d3e`.
- Expiry: `2026-12-03T01:48:24Z`.

No canonical P1 lift, A0/COMMON, compatible lift, fake, or Ihara witness is
claimed.  `verified=false`.

