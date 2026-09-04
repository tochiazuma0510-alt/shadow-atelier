# Luna Task781 — canonical P1 input-size type repair v1

Role: Luna implementation only.  Read `AGENTS.md` and this file completely.
Write only the three requested implementation outputs plus the designated
reply.  Do not run GHA, git, network, or a large local replay.

## Proven actual failure

Actual workflow run/attempt `33827142944/1`, job `100882118138`, exact head
`bd1f092b8301e4a07cf0a3c8b228bff63e23276b`, failed in producer-v6 at
`build.authenticate_inputs`:

```text
authenticate_inputs line 1302: sha(body_raw)
sha line 173: hashlib.sha256(data)
TypeError: object supporting the buffer API required
```

The cause is now exact.  The pinned imported function
`search/d972_r07_grade2_specific_owner_prejoin_v1.py::validate_block_envelope`
returns `(root, body, len(br))`; consequently
`semantic_replay_v5.block_envelope` returns an integer body length as its
third component.  Producer-v6 falsely names/types it `body_raw: bytes` and
hashes it.  This stop is before the 8,059-row recurrence.

## Required minimal repair

Create versioned successors:

1. `search/d972_r07_canonical_p1_dag_degree2_lift_v7.py`
2. `.github/workflows/d972-r07-canonical-p1-dag-degree2-lift-v4.yml`
3. `sol/luna_reply_781_r07_canonical_p1_input_size_type_repair_v1.md`

Start from producer-v6/workflow-v3.  Make only the following semantic repair
and mechanical version/pin changes:

- Treat the third block-envelope result as a plain nonnegative integer
  `body_size`, never as bytes.  Reject bool and negative values.
- Do **not** reread, retain, canonicalize, or copy the large block JSON bodies.
  In particular, do not use `canonical(body)` as a substitute raw buffer.
- The structural validator has already checked canonical bytes and the exact
  parent digest.  Register each block file with its pinned `PARENTS[index]`
  digest; make the raw-artifact entry compare `body_size` with the current
  regular file size and record that size plus stable identity.  Registry
  verification must still hash the physical file against the pinned digest.
- Apply the same size-taking artifact-entry ABI coherently to prepare via
  `len(prepare_raw)`, or use a separately named bounded helper if that yields
  the smaller diff.  No authentication gate may be weakened.
- Remove/rename the misleading `block_raws: list[bytes]` storage and returned
  boundary key.  Keep only the four small integer sizes; no downstream code
  currently consumes the old key, but prove that by static search.
- Retain v6's phase/traceback diagnostics and its harmless packet-row
  `.tobytes(order="C")` hardening.  Do not change recurrence, rows, actors,
  packets, coefficients, cache layout, source parents, time/RSS gates, or
  claim flags.
- Add a bounded selftest/control that supplies a block-envelope integer size
  and reaches the corrected artifact/registry path, and a mutation that tries
  bytes/bool/negative/wrong length.  It must not construct a production-size
  body or invoke the full build.
- Version the producer/result/launch schema and executable key to v7/v4 as
  needed.  Workflow fire token must be exactly
  `[fire-r07-canonical-p1-degree2-lift-v4]`.  Update all exact path/hash/size/LF
  pins and artifact labels mechanically.  Preserve one serial job and all
  immutable parent gates.

Run only bounded compile/selftest, YAML parse, exact pin checks, AST/diff
classification and a tiny isolated helper control.  Report exact SHA-256,
bytes, LF, files changed, and explicitly state whether any arithmetic/build
loop AST changed.

