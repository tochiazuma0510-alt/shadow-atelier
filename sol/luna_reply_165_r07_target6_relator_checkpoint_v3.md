# Luna reply 165: g760 target6 lossless relator checkpoint v3

Date: 2026-08-26
Role: Luna / implementation and bounded mechanical audit only

## 1. Result

Implemented the v3 producer adapter, producer-only GAP driver, and bounded
preflight certificate.  A completed D2 relator now publishes an immutable,
deterministic-gzip canonical JSONL stream containing the **entire** F3 pivot
dictionary.  Loading restores the original pivot insertion order into a fresh
`F3BitEchelon`, checks the exact reconstructed dictionary/rank, and authenticates
both canonical decompressed bytes and compressed-file bytes independently.

No full 649,539-row calculation was run locally.  No git operation, push,
workflow edit, workflow dispatch, or checker process was performed.

## 2. New files

| path | bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_760_l3_target6_relator_resume_v3.py` | 105736 | `0f1ef3bfd341cc5e596b4d84e4122a56b87488dc894dbf58f0561f288ac8a22f` |
| `search/d972_r07_760_l3_target6_relator_resume_gha_driver_v3.g` | 15861 | `5784cc29c5dbc24a89867ebb3a275000ffaa698ba2b3c1a6adc4d4b6efdc7870` |
| `search/certs/d972_r07_760_l3_target6_relator_resume_preflight_v3_20260826.json` | 22409 | `5928b30f0de8c0aa65e141cdb4101b77c412ab20541ee35c0b74e8680b68c59c` |
| `sol/luna_reply_165_r07_target6_relator_checkpoint_v3.md` | this report | computed after handoff |

The certificate canonical self digest is
`5c162cea2e8dee08e1b62d1a17e288e5c7139e192494a4d8aa92424389d0644c`;
its fixed-binding digest is
`4249041530950577972d22039149254e3cf2bed4fec305333c21c04422e35cf1`.

## 3. Checkpoint and resume implementation

Each relator stream has a canonical header followed by increasing-pivot rows

```text
[pivot_index, coefficient_one_plane_lowercase_hex,
              coefficient_two_plane_lowercase_hex]
```

and records the original insertion order separately.  Validation rejects an
out-of-range pivot, mask overflow, plane overlap, noncanonical hex, wrong
leading coordinate/coefficient, wrong row order, duplicate pivot, rank drift,
dictionary drift, canonical-stream drift, compressed-stream drift, and fixed
input drift.  Publication uses a temporary file, `fsync`, then an immutable
hard-link; gzip uses `mtime=0`, empty filename, and level 6.

The chain gate authenticates the exact fixed directory, filename, SHA and bytes
of every ancestor.  Adjacent relator headers must share the same prior-j anchor
and cumulative j progression; closure receipts must extend by exactly one.
The relator-11 header is bound exactly to the completed public j row: receipt
roster, D2 rank, monomial count, dimension, Jennings basis, target projection,
legal-row projection, and preceding j progression all agree.  This closes the
two recomputed-self-digest chain-splice cases found in final audit.

V3 resume works from a preseeded v3 relator checkpoint at its exact next
relator, or a preseeded v3 completed-j checkpoint at the next j/relator 1.
Arbitrary skips, terminal j checkpoints, stale/missing files, mutated
ancestors, and path substitution fail closed.

One task boundary remains **operationally blocked / UNKNOWN**: the generic GHA
runner uploads `ci/out` after a run but does not download an earlier run's
artifact before the next run.  Therefore cross-run GHA restart is not presently
ready unless the full authenticated chain is preseeded by a separately
authorized ingress step.  No workflow change was authorized or made.  The
current v3 entry point also does not directly import a raw v2 checkpoint chain;
it accepts v3 relator/completed-j files only.  Thus the task's requested raw-v2
checkpoint migration is not claimed complete.

## 4. Safe j=9 accelerators

Two optional exact caches were added without changing traversal, row insertion,
or first-terminal order:

1. A persistent lazy table for `gen_pcvec(i) * pcvec`, capped at
   `10 * 59049 = 590490` slots.
2. A lazy per-j `pcvec -> truncated Jennings bitplane pair` table, capped at
   59049 slots and explicitly cleared between j values.

Both have runtime equality canaries, fail closed to the original v1 arithmetic,
and can be disabled with `--disable-accelerators`.  The preflight comparison
covered all 59,049 pc vectors at j=2, 260 deterministic j=9 pc vectors, 103
actual j=9 row samples, 10,280 deterministic left-products, and all 11 j=2
relator closures.  Exact pivot dictionaries and insertion order agreed.

The bounded warm-cache microbenchmark (not a full-run prediction) reported
`left_warm_speedup=26.054` and `projection_warm_speedup=2.097` on the final
source.  Estimated cache maxima, excluding the echelon, are:

| cache | estimated maximum |
|---|---:|
| left multiplication | 31.000 MiB |
| Jennings j=9 | 74.334 MiB |
| Jennings j=10 | 115.330 MiB |
| Jennings j=11 | 169.842 MiB |
| Jennings j=12 | 237.868 MiB |

The inherited `v1.Monitor` retains the 5,600 MiB RSS cap.  Pivot statistics are
computed once and passed to the header and writer; serialization is therefore
two pivot passes (one statistics pass and one gzip write), not the former
statistics/header/writer triple pass.

For a fresh NONMEMBER, v3 deliberately still performs direct separator pairing
and then recomputes the entire j through the no-checkpoint state-leak replay.
That is roughly a second complete D2-closure cost before the independent v2
checker.  It was preserved as a mathematical gate, not advertised as a speedup.

## 5. Checkpoint size bounds and v4 preregistration

These are deterministic uncompressed **pivot-row payload** upper bounds at
rank = dimension; headers are additional and actual gzip sizes remain UNKNOWN
until a GHA full run.

| j | one full state | eleven v3 full states |
|---:|---:|---:|
| 9 | 371,063,184 B (0.346 GiB) | 4,081,695,024 B (3.801 GiB) |
| 10 | 950,915,952 B (0.886 GiB) | 10,460,075,472 B (9.742 GiB) |
| 11 | 2,144,208,000 B (1.997 GiB) | 23,586,288,000 B (21.966 GiB) |
| 12 | 4,292,381,760 B (3.998 GiB) | 47,216,199,360 B (43.974 GiB) |

The append-only pivot-row invariant was asserted after every closure: existing
pivot rows do not change.  A versioned v4 successor should therefore store only
each relator's new pivots plus an authenticated ancestor chain, cumulative rank,
insertion-order commitment, and cumulative state commitment.  Exact replay of
all deltas reconstructs the same full dictionary.  For the pivot payload alone,
v4's cumulative worst case is one final state versus v3's eleven copies: the
exact registered contrast is 1:11 (headers and gzip excluded).  V3 was not
silently weakened to this delta design.

## 6. Bounded test record

All substantive tests were serial in the isolated pinned-input overlay
`%TEMP%\d972_task164_clean_11cbe4b89ff048a8841e48ec5f863fa9`.

Final producer selftest:

```text
R07_760_L3_TARGET6_RELATOR_RESUME_V3_PRODUCER_SELFTEST_PASS checkpoint_mutations=16 j2_exhaustive=59049 j9_samples=260 j2_relators=11 left_warm_speedup=26.054 projection_warm_speedup=2.097 full_pivots=true deterministic_gzip=true
```

Final preflight generation:

```text
R07_760_L3_TARGET6_RELATOR_RESUME_V3_PRODUCER_PASS preflight_state=R07_760_L3_TARGET6_RELATOR_RESUME_V3_PREFLIGHT_READY grade=CANDIDATE checkpoints=0 sha256=5928b30f0de8c0aa65e141cdb4101b77c412ab20541ee35c0b74e8680b68c59c bytes=22409
```

The checked-in certificate was byte-equal to that clean-overlay output.
The 16 rejected mutations include every task-listed case plus prior-j chain
splice and terminal closure-roster splice.  Driver selftest and j09/r01 path
canary:

```text
R07_760_L3_TARGET6_RELATOR_RESUME_V3_GHA_DRIVER_PASS mode=selftest producer_processes=1 checker_processes=0 checkpoint_mutations=16 grade=CANDIDATE
TASK165_DRIVER_PATH_PASS
```

The GAP driver is ASCII/LF-only (`non-ASCII=0`, `CR=0`).  It runs one producer,
zero checkers, uses inner 21,000 s / outer 22,500 s, and independently hashes
every checkpoint into a ledger which must agree with the final receipt.

## 7. Exact driver invocations

Selftest:

```gap
D972_R07_760_L3_TARGET6_RELATOR_RESUME_V3_SELFTEST:=true;;
Read("search/d972_r07_760_l3_target6_relator_resume_gha_driver_v3.g");;
QUIT_GAP(0);;
```

Initial GHA producer:

```gap
D972_R07_760_L3_TARGET6_RELATOR_RESUME_V3_RUN:=true;;
D972_R07_760_L3_TARGET6_RELATOR_RESUME_V3_USE_PYTHON3:=true;;
Read("search/d972_r07_760_l3_target6_relator_resume_gha_driver_v3.g");;
QUIT_GAP(0);;
```

Resume after completed j=9 relator 6 (starts relator 7), provided the complete
chain is already preseeded in the fixed directory:

```gap
D972_R07_760_L3_TARGET6_RELATOR_RESUME_V3_RUN:=true;;
D972_R07_760_L3_TARGET6_RELATOR_RESUME_V3_USE_PYTHON3:=true;;
D972_R07_760_L3_TARGET6_RELATOR_RESUME_V3_RESUME_RELATOR_J:=9;;
D972_R07_760_L3_TARGET6_RELATOR_RESUME_V3_RESUME_RELATOR_R:=6;;
Read("search/d972_r07_760_l3_target6_relator_resume_gha_driver_v3.g");;
QUIT_GAP(0);;
```

Resume after completed v3 j=9 (starts j=10 relator 1), with the same preseed
condition:

```gap
D972_R07_760_L3_TARGET6_RELATOR_RESUME_V3_RUN:=true;;
D972_R07_760_L3_TARGET6_RELATOR_RESUME_V3_USE_PYTHON3:=true;;
D972_R07_760_L3_TARGET6_RELATOR_RESUME_V3_RESUME_J:=9;;
Read("search/d972_r07_760_l3_target6_relator_resume_gha_driver_v3.g");;
QUIT_GAP(0);;
```

## 8. Claim boundary

```text
relator checkpoint = resource recovery, not a mathematical result
inherited j2..8 = producer control-flow candidate only
fresh NONMEMBER = candidate until helper-nonshared direct checker agrees
MEMBER != actual A18 lift
no fake / cofinal lift / Ihara witness declared
```

The v2 direct-enumeration checker remains the required independent replay for a
completed fresh NONMEMBER; v3 checkpoint validation is not that checker.
