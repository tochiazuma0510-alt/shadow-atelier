# Luna reply 166: g760 target6 append-only delta checkpoint v4

Date: 2026-08-26
Role: Luna / implementation and bounded mechanical audit only

## 1. Result

Implemented v4 as a thin adapter over the pinned v3 producer.  It imports the
v3 traversal and both exact caches unchanged, but replaces eleven repeated full
echelon snapshots by an authenticated append-only delta chain.  Replaying every
delta from the root reconstructs a fresh `F3BitEchelon` with the exact pivot
dictionary, rank, and insertion order, then resumes at the exact next relator.

No full j=9 calculation, parallel Python/GAP, git operation, push, workflow
edit, workflow dispatch, or inspection/control of the two live GHA runs was
performed.

## 2. New files and final pins

| path | bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_760_l3_target6_delta_resume_v4.py` | 88429 | `08f2237ac6aa438dded775c55627f07ffeff74145765b6e9791a898d594d77ef` |
| `search/d972_r07_760_l3_target6_delta_resume_gha_driver_v4.g` | 16494 | `274291371fd5548d5cf5505c5b250cb88a7c74e08ab23f5d0b437a58a079e531` |
| `search/certs/d972_r07_760_l3_target6_delta_resume_preflight_v4_20260826.json` | 34608 | `0a715bcedec3283894461444fa3d7f542255a436780327bb95f87d1a411e4fbf` |
| `sol/luna_reply_166_r07_target6_delta_checkpoint_v4.md` | this report | computed after handoff |

The final producer mtime at handoff was
`2026-08-26T22:31:20.0698734+09:00`.  Its hash/bytes were rechecked after all
tests and it was not edited again.  The final preflight canonical self digest is
`7e14a33660ca026b55d910fc7b231a8dea92e81b1f4c068c4fcf9ec7c9340187`;
its fixed-binding digest is
`dc90aa5ec265287c67e29e4b6ff45b8108b208d7ea31422054634cf7ba57d823`.

### Source-drift repair

An intermediate source was 86891 bytes with SHA
`8b7ec4998454ccb6e6d01f8a567409040e02d3fd41da6d2325d80320383c99e8`.
It was intentionally extended by 1538 bytes before finalization to:

- bind the completed-j public row directly to the terminal cumulative state
  commitment; and
- record a deterministic toy multi-delta replay receipt in preflight/selftest,
  including exact next relator, rank, insertion order, and state commitment.

That produced the final 88429-byte source above.  Preflight was regenerated
twice from that final source, the two outputs were byte-identical, the driver
pins were updated, and the driver selftest was rerun.  No PASS from the older
source is used as final evidence.

## 3. Append-only and commitment contract

After every v3 closure, v4 asserts all four required conditions before writing:

1. every old pivot still exists;
2. both old bitplanes are integer-for-integer unchanged;
3. the new insertion-order list has the old list as an exact prefix; and
4. the receipt's `new_pivots`, rank increment, and suffix length are equal.

Only the suffix rows are serialized, in original insertion order, with the v3
canonical encoding

```text
[pivot_index, coefficient_one_plane_lowercase_hex,
              coefficient_two_plane_lowercase_hex]
```

The cumulative commitment is explicitly domain-separated by

```text
d972-r07-760-l3-target6/v4/cumulative-pivot-state/v1
```

The root commits j, dimension, Jennings/target/legal bindings and the exact
prior-j record.  Each extension hashes the domain, prior state commitment,
j/relator/rank metadata, and every length-prefixed canonical delta row.  Thus it
commits the full ordered append log, not a claimed digest in isolation.
Replay authenticates every ancestor filename/SHA/bytes/state commitment, adds
each actual row to a fresh echelon, and recomputes the cumulative commitment,
insertion-order commitment, exact dictionary and rank.

The relator-11 reconstructed state is bound to the ordinary completed-j row by
its state commitment, complete closure roster, D2 rank, dimension, monomial
count, Jennings basis, target/legal projections, and preceding j progression.

## 4. Bounded replay and mutation audit

The deterministic toy receipt recorded in the final certificate is:

```text
completed relators = [1,2,3]
delta checkpoints replayed = 3
exact next relator = 4
final rank = 4
final insertion order = [5,1,3,8]
final state SHA-256 = f9278ba3a46c0d50f051028ada1f8f0f29e2d76c3141615ef2c323b0e9b23010
exact dictionary/order reconstructed = true/true
```

All 12 registered mutations were rejected:

- delta bit flip;
- rewrite of an old pivot;
- rank gap;
- delta-order change;
- ancestor deletion, duplication, and reordering;
- prior-j splice;
- closure-roster splice;
- cumulative-state commitment forgery;
- noncanonical delta row; and
- stale-file injection.

## 5. Cache equality and storage identity

The exact v3 caches and fallback switch are imported, not reimplemented.  The
final bounded audit compared:

- all 59,049 j=2 PC elements;
- 10,280 deterministic left-multiplication pairs;
- 260 deterministic j=9 PC samples and 103 actual j=9 row samples; and
- all eleven j=2 relator closures, including exact pivot dictionary and
  insertion order.

All comparisons agreed and remain fail-closed.  `--disable-accelerators`
restores the original arithmetic paths.  The per-j Jennings cache is cleared
between j values; the left-multiplication cache may persist.  The final bounded
warm-cache microbenchmark reported `left_warm_speedup=26.408` and
`projection_warm_speedup=2.404`; these are not full-run predictions.

The exact j=2 storage identity was:

```text
sum(delta pivot counts over 11 relators) = 11 = final pivot count
sum(delta row payload bytes) = 266 = final row payload bytes
concatenated delta rows = final insertion-order rows byte-for-byte
```

For the registered rank=dimension pivot-payload upper bounds (headers excluded):

| j | v4 cumulative deltas | v3 eleven full copies |
|---:|---:|---:|
| 9 | 371,063,184 B | 4,081,695,024 B |
| 10 | 950,915,952 B | 10,460,075,472 B |
| 11 | 2,144,208,000 B | 23,586,288,000 B |
| 12 | 4,292,381,760 B | 47,216,199,360 B |

This is an exact 1:11 pivot-payload upper-bound contrast.  Headers are
additional.  Actual gzip size and full-run speed remain UNKNOWN until GHA.

## 6. Final serial test record

All authoritative tests used the isolated pinned-input overlay
`%TEMP%\d972_task164_clean_11cbe4b89ff048a8841e48ec5f863fa9`.

Final producer selftest:

```text
R07_760_L3_TARGET6_DELTA_RESUME_V4_PRODUCER_SELFTEST_PASS delta_mutations=12 j2_exhaustive=59049 j9_samples=260 j2_relators=11 delta_count=11 final_count=11 payload_bytes=266 toy_next_relator=4 toy_rank=4 left_warm_speedup=26.408 projection_warm_speedup=2.404 append_only=true exact_replay=true
```

Final preflight was generated twice from source SHA `08f2237a...`; both runs
returned exactly:

```text
R07_760_L3_TARGET6_DELTA_RESUME_V4_PRODUCER_PASS preflight_state=R07_760_L3_TARGET6_DELTA_RESUME_V4_PREFLIGHT_READY grade=CANDIDATE checkpoints=0 sha256=0a715bcedec3283894461444fa3d7f542255a436780327bb95f87d1a411e4fbf bytes=34608
PREFLIGHT_BYTE_EQUAL_PASS
```

After updating the final pins, the clean driver audit returned:

```text
R07_760_L3_TARGET6_DELTA_RESUME_V4_GHA_DRIVER_PASS mode=selftest producer_processes=1 checker_processes=0 delta_mutations=12 grade=CANDIDATE
TASK166_DRIVER_PATH_PASS
```

The driver is ASCII/LF-only (`non-ASCII=0`, `CR=0`), pins v4 plus the v3
chain, runs exactly one producer and zero checker processes, retains inner
21,000 s / outer 22,500 s, and independently hashes every delta/j checkpoint.

## 7. Resume invocations and operational UNKNOWN

Initial producer-only GHA input:

```gap
D972_R07_760_L3_TARGET6_DELTA_RESUME_V4_RUN:=true;;
D972_R07_760_L3_TARGET6_DELTA_RESUME_V4_USE_PYTHON3:=true;;
Read("search/d972_r07_760_l3_target6_delta_resume_gha_driver_v4.g");;
QUIT_GAP(0);;
```

Resume after completed j=9 relator 6 (starts relator 7):

```gap
D972_R07_760_L3_TARGET6_DELTA_RESUME_V4_RUN:=true;;
D972_R07_760_L3_TARGET6_DELTA_RESUME_V4_USE_PYTHON3:=true;;
D972_R07_760_L3_TARGET6_DELTA_RESUME_V4_RESUME_DELTA_J:=9;;
D972_R07_760_L3_TARGET6_DELTA_RESUME_V4_RESUME_DELTA_R:=6;;
Read("search/d972_r07_760_l3_target6_delta_resume_gha_driver_v4.g");;
QUIT_GAP(0);;
```

Resume after completed v4 j=9 (starts j=10 relator 1):

```gap
D972_R07_760_L3_TARGET6_DELTA_RESUME_V4_RUN:=true;;
D972_R07_760_L3_TARGET6_DELTA_RESUME_V4_USE_PYTHON3:=true;;
D972_R07_760_L3_TARGET6_DELTA_RESUME_V4_RESUME_J:=9;;
Read("search/d972_r07_760_l3_target6_delta_resume_gha_driver_v4.g");;
QUIT_GAP(0);;
```

All resumes require the complete v4 ancestor chain already present in the
fixed checkpoint directory.  Cross-run artifact ingress was not authorized or
implemented; generic GHA does not automatically download an earlier run's
artifact.  Cross-run restart therefore remains operationally UNKNOWN/blocked,
although the artifact itself is lossless recovery data.

For a fresh producer NONMEMBER, the v3 no-state replay remains in place and the
helper-nonshared v2 direct checker is still mandatory.  V4 does not execute or
replace that checker.

## 8. Claim boundary

```text
delta checkpoint = resource recovery, not a mathematical result
inherited j2..8 = producer control-flow candidate only
fresh NONMEMBER = candidate until helper-nonshared direct checker agrees
MEMBER != actual A18 lift
no fake / cofinal lift / Ihara witness declared
```
