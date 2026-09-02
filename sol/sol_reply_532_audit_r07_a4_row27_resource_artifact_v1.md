# Task 532 independent bounded audit — A4 row27 RESOURCE artifact

## Verdict

`AUDITED_ZERO_DURABLE_PROGRESS_RESOURCE`

Run `33579631937` contributes zero new durable A4 rows and zero numerator.  A4
therefore remains `1/3 UNKNOWN_RESOURCE / cross-checked through row 26`.
The only promoted diagnosis is the 8-GB resource boundary.  No positive,
NONMEMBER, A4, fake, Ihara, or checker-PASS claim is promoted, and
`verified=false`.

## API identity and bounded ZIP authentication

Authenticated GitHub REST responses give a single-job, single-artifact run:

- run `33579631937`: `workflow_dispatch`, `completed/success`, attempt 1,
  head `efaa6234d5ea12c9f81dcb1f33f0609387964475`;
- job `100090966487` (`gap`): `completed/success`, with the same run and head;
  its GAP and upload-artifact steps both completed successfully;
- the commit endpoint resolves that exact 40-hex head;
- artifact `9831693721`, `gap-run-out`: 841367330 bytes, unexpired, attached to
  that run/head, with API service digest
  `sha256:2f77b0d3e24009a669761f1066e9e61dd79c88c14a85fd092e85cc11b70dd0b7`.

I did not fetch or recompute the digest of the 841-MB ZIP.  An authenticated
download redirect was used only with fail-closed HTTP byte ranges.  The
22-byte response for `841367308-841367329` was HTTP 206 with
`Content-Range: bytes 841367308-841367329/841367330`; its EOCD is `PK\x05\x06`
and reports 1907 entries, central-directory size 164671 and offset 841202637,
with zero comment bytes.  The exact central-directory range
`841202637-841367307` has SHA-256
`3e6d813134419817965ea0f3e9f6fdebfac83d8803b90c52eca519286185a5ec`.
It parses to 1907 distinct names.

The following members were obtained from their exact local-header and
compressed-data ranges, decompressed individually, and hashed:

| member | compressed range | bytes | SHA-256 |
|---|---:|---:|---|
| `task514_v45.success` | `841202567-841202620` | 60 | `dce44782c366a3bc171c492c0f6a9b9c831060ac2ee96d2c8a5a8213d5a0ffcb` |
| `task514_v25_producer.json` | `841089735-841199808` | 928325 | `dab9b493f935f5a15283820bb98b782ce0621d880176992cec7dc51beaa791b3` |
| `task514_v25.producer.log` | `124168-128818` | 42809 | `fdd79b4bc9af65a334671c0c5cf76f812c0f7019690b84821699e04b3416c9f8` |
| returned producer HEAD | `11233-11623` | 700 | `910cc8afcca333dab56d9fefe35e63066eab764ac6325e3130c43a3c3d6f0114` |
| returned checker checkpoint | `100-2545` | 8991 | `b96919b38272d87a6885da98a18603065d1c2ccf805cd2c4f65dd22e32ed7af2` |
| `task514_v25_physical/HEAD` | `128890-151084` | 634808 | `6abbf9a3ddc5e3c63fc5080d5084d84777970ed881efa4b1c90cd619078aa903` |

Every accepted range response was HTTP 206 with exactly the requested length;
the largest ZIP range was the 164671-byte central directory.  No physical
shard member body was requested or expanded.

## Unique RESOURCE branch and claim boundary

The marker is exactly

```text
TASK514_R07_A4_RESOURCE terminal=UNKNOWN_RESOURCE checker=0
```

including its final LF.  It is the sole `.success` member.  The central
directory contains exactly one marker, producer result, and producer log, but
zero `task514_v35_checker.json` and zero `task514_v35.checker.log` members.

The producer result has `status=terminal=UNKNOWN_RESOURCE`, `complete=false`,
and exact reason

```text
dual_pullback:rss_bytes:8001912832>8000000000:state=dual_pullback
```

Its `forbidden_downstream` is exactly
`{"Ihara":false,"fake":false,"lift":false}` and it has no root A0, COMMON,
or NONMEMBER field.  The producer log has exactly one terminal line,
`R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V6_PRODUCER_TERMINAL UNKNOWN_RESOURCE`,
and no case-sensitive `PASS`, `MEMBER`, `NONMEMBER`, `fake`, or `Ihara` token.
The `A4_PROGRESS` prefix is telemetry, not an A4 claim.  Thus there is one
unambiguous RESOURCE execution branch and no checker acceptance or positive
mathematical terminal.

## Zero durable row27 progress

The returned ordinary HEAD says
`last_row=26,next_row=27,segment_count=2,last_sequence=2`, with last segment
delta 2 and chain
`240714843f67b24fdee9593601130c5d36ef9996909a08af9ec909888cb8cfdb`.
Its 700 bytes are byte-identical to the archived row26 extract in this
artifact and match the identity recorded independently by Tasks 511, 516 and
520.  Likewise, the returned 8991-byte checker checkpoint is byte-identical
to the archived row26 extract and has the same Tasks 511/516/520 identity.
There is no delta 3 and no ordinary HEAD advancement.

The log contains 159 progress lines: one initial AUTHORITY line and 158
row27 CORRELATION lines.  Every CORRELATION line retains
`completed_row=26,durable_checkpoint_row=26,K_rank=0`.  Its last and maximum
logged telemetry is combined/boundary rank 112099, 33535212 correlation
pairs, and RSS 7974567936.  The terminal result subsequently records peak RSS
8001912832 and 33673124 pairs.  None of these open-query physical counters is
a completed row, a committed ordinary delta, or an A4 numerator.

## Physical intraquery checkpoint: retained candidate, not audited continuation

The RESOURCE result does preserve potentially useful Task499-style row27
state; it must not be described as nonexistent or discarded.  Its checkpoint
is `kind=physical_shard_chain`, `obsolete=false`, `sequence=1877`,
`next_row=27`, with `open_query.query_id=R:27`, cumulative
accepted/examined `112355/112376`, chain
`2844cddcc8fbc75e1f0ed9bb8ff2139305f279523d5e3fd41f0e833ce079ea3c`,
and `last_shard_sha256`
`7645391ccd25fd02687fd9eb137d3af714f11f32428bdcf6f92476a3430e9945`.
The separately range-read physical HEAD has exactly those scalar fields and
an identical serialized `open_query`; it reports physical rank/boundary rank
112355.  Its bytes/SHA also exactly match the identity embedded in the
producer result.

At index level, the result manifest and central directory are coherent: both
contain exactly 1877 uniquely named shards `00000001` through `00001877`,
with no missing or extra shard and no uncompressed-size mismatch.  All 1877
manifest SHA strings are syntactically 64-hex.  The last manifest identity is
the 25011895-byte `shard.00001877.json`, whose whole-file SHA claim is
`fb04a082eecc636699cb4034cad21c2ac7ea61cd5ea940aeeeb0d39517c6309d`.

This is not enough to declare the chain self-consistent, cross-checked, or
continuation-ready.  The HEAD's `last_shard_sha256` is an internal shard seal,
not the manifest's whole-file SHA.  Establishing their binding requires
reading each shard and checking its raw identity, internal self-digest,
`previous`/chain link, query binding, reconstructed candidate prefix and
mask/entries, semantic before/after state, counters, epoch, and final HEAD
binding.  That is precisely the full physical-chain replay performed by the
independent checker, which did not run (`checker=0`).  Because all shard
bodies were deliberately excluded from this bounded audit, the strongest
permitted classification is **index-consistent physical resume candidate**.
It may be preserved for a separately authorized full-chain validation, but it
does not alter the present zero-durable-progress verdict.

## Limitations

The API service digest is trusted metadata rather than a locally recomputed
full-ZIP digest.  No producer, checker, GAP computation, shard replay, or Lean
proof was run; no release, workflow, or git state was mutated.  Only the
small ranges listed above and the ZIP directory/EOCD were read.  The exact
physical byte count and SHA-256 of this frozen reply are reported in the
parent delivery envelope, since embedding the file's own final digest would
be self-referential.

AUDITED_ZERO_DURABLE_PROGRESS_RESOURCE
