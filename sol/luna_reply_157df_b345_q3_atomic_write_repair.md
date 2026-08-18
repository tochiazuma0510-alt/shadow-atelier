# Luna reply 157df — B345 q3 atomic checkpoint repair

Date: 2026-08-18

## Verdict

```text
B345_Q3_ATOMIC_WRITE_REPAIR_READY_FOR_GHA
```

The repair is confined to the producer's checkpoint I/O, the producer
self-test, the thin driver's self-test gate, and the direct-scan branch log.
No local GAP/Python, Git, or GHA operation was run.

## Incident and repair

Canary `32130817181` passed. Full run `32131160061` stopped before ANUPQ and
before candidate enumeration at the first checkpoint because the GAP process
had no binding for the old core rename primitive. This was an operational I/O
failure, not a mathematical or search result.

`D972Q3AtomicWrite` now requires `LoadPackage("io")=true` and a bound
`IO_rename`. It writes `path.tmp` beside the destination, closes the stream,
and accepts the replacement only when `IO_rename(tmp,path)` returns exactly
`true`. There is no shell rename and no destination removal before the
replacement; a stale temporary file may be overwritten by the normal output
open.

The producer self-test writes two distinct records to the fixed
`ci/out/d972_b345_q3_atomic_io_smoke.json`, reads the second exact canonical
JSON plus newline, checks that it is not the first payload, removes the smoke
file, and then emits exactly one:

```text
D972_B345_Q3_ATOMIC_IO_SELFTEST_PASS backend=IO_rename replace=true
```

The driver creates `ci/out` before reading the producer and requires the
producer's exact marker binding and count to be one before invoking the
independent checker self-test.

Immediately after `D972Q3DirectScan` returns, the producer emits exactly one
branch marker. The positive branch is tied to
`FIRST_TYPED_WITNESS`, `solution_count=1`, and the selected receipt's
exponent/correction index. The negative branch is tied to
`ALL_162_EXHAUSTED`, `solution_count=0`, and `evaluated_candidates=162`:

```text
D972_B345_Q3_DIRECT_SCAN_RESULT result=first_typed_witness evaluated=<n> exponent=<n> correction_index=<n>
D972_B345_Q3_DIRECT_SCAN_RESULT result=all_162_negative evaluated=162 next=PB5_typed_d2_bundle
```

Only the selected runtime branch is printed; no per-candidate logging was
added, and the marker is not an A/B conclusion.

## Final pins and updated reply history

```text
search/d972_b345_q3_chief_v1.g         76,704 bytes  e3dad87ad066fc9c605e1eecaddbe63efd63ac68500e0fcff0d6d62eb7d83af3
search/d972_b345_q3_gha_driver_v1.g      5,463 bytes  6a3cb5339468dd7f1b214c67d9791b0f752d0df625f06781470dc24c92a8a859
search/check_d972_b345_q3_chief_v1.py  87,732 bytes  9864e55f6e0ee1ae8100788e5ba127ef95bffd62535c3aa23a192cde6109cfcb
```

The checker SHA and every producer mathematical input pin remain unchanged.
The authorized prior replies were updated with the superseding history:

```text
sol/luna_reply_157da_b345_q3_chief.md          19,461 bytes  d13694bcfde9e1074daeee3b591b410ae48d0acfff557b014302721448847648
sol/luna_reply_157db_b345_q3_gha_driver.md      6,322 bytes  7b4dd0441613ac568ca318c1d70a6d7975e5c6b9c80832166a2f85d14214c220
sol/luna_reply_157dc_b345_q3_canary_repair.md   5,016 bytes  d631047abb635b94354d6742963b02eca6b54e416e936e1c699757d90d361de9
sol/luna_reply_157dd_b345_q3_emptylist_json_repair.md
                                                4,333 bytes  eaee535461472f5b7cdbd96fb1c894bfef8b15e16deb86573d712cbc4b9f2923
```

## Static audit

Bounded source checks passed: one implementation call to `IO_rename`; two
real smoke writes to the same path; readback compares the second and rejects
the first; no destination deletion in the atomic writer; driver directory
creation precedes producer read; exact-one atomic marker gate; unchanged
checker pin; and exactly two source branch forms for the one runtime direct
scan marker. The producer's control flow and pins outside I/O/logging were
left unchanged. No runtime success, cross-check, or A/B claim is made here;
the next GHA canary is required.

## 157dg correction: checked closed write

Canary `32132850360` showed that the optional I/O package is unavailable on
the runner. The 157df replacement contract is superseded: the producer now
builds canonical JSON plus newline once, writes the final target with core
`OutputTextFile`, closes it, rereads it with `StringFile`, and fails unless the
bytes match exactly. This is not atomicity; it is a checked closed write.

The two-write smoke remains real and now uses exactly one
`D972_B345_Q3_CHECKED_IO_SELFTEST_PASS backend=OutputTextFile replace=true readback=true`
marker, enforced by the driver before checker execution. A killed/error
producer cannot return, so a partial file cannot be consumed and the final
driver marker is absent. The direct-scan markers and all mathematical pins are
unchanged.

Current code hashes:

```text
producer  76,867  b95fc29b326c3d6a378249cdeb03595eed8d0211a7fe0358fc02447d70d5f755
driver     5,488  93a03d8d44694f016603bebd3909fe718dbbd6fe8018c17f5460c040bc3aea76
checker   87,732  9864e55f6e0ee1ae8100788e5ba127ef95bffd62535c3aa23a192cde6109cfcb
```

## 157di checker-index supersession

Run `32134100496` at commit `c7ef41aab6507d2992f3c89913db84ac839ca3dd`
produced the exact first typed witness (`evaluated=28`, `exponent=2`,
`correction_index=1`), but the independent checker stopped at `Pi4 settlement
inverse compositions`. This was a checker-only off-by-one: `PcCollector.unit`
is one-based while the old zero-based composition loop called `unit(0)`, which
selected Python's final coordinate. The producer receipt, 162-row universe,
formulas, and terminal predicate were not changed.

The repaired checker centralizes both homomorphism and both inverse-composition
orders in `validate_inverse_pc_maps`, iterating `idx in range(pc.n)` and
comparing to `pc.unit(idx + 1)`; `unit` now rejects indices outside 1..n. Its
rank-2 elementary-abelian exponent-3 canary accepts the identity pair, rejects
the deliberately noninverse identity/swapped pair, and rejects `unit(0)`. The
one permitted self-test passed with
`D972_B345_Q3_CHECKER_SELFTEST_PASS mutations=9 orientation_canaries=1
rank2_pc_inverse_canaries=2`.

Current pins are producer 76,867 bytes
`b95fc29b326c3d6a378249cdeb03595eed8d0211a7fe0358fc02447d70d5f755`, driver
5,488 bytes `c397cd837ff6814f7b7a8ca0604c6aed54fa0bc85bb577516ea1c6e7df83a831`,
and checker 89,082 bytes
`ddb52ddae18327209692f0f6eb8b4f65cbdd446155be660a621de24274cc3f73`. The
repaired bundle is ready for a fresh GHA replay; the candidate remains pending
that checker pass and is not an A/B conclusion.
