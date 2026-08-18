# Luna reply 157dc — GAP 4.16 immutable RecNames repair

Date: 2026-08-18

## Verdict

```text
B345_Q3_GAP416_RECNAME_REPAIR_READY
```

The canary failure is repaired with one semantics-preserving producer edit and
the corresponding driver SHA-pin update. No local GAP, Python, Git, GHA, or
workflow execution was performed.

## Failure and diagnosis

GHA canary run `32129602522`, commit
`b40c7fcae815a4fe6e725001496982e24d6198aa`, completed setup and entered the GAP
script. After about 1m39s it failed with:

```text
Error, immutable lists cannot be sorted
```

The failure was in `D972Q3Json`, before any mathematical verdict:

```gap
names := RecNames(x);; Sort(names);;
```

On GAP 4.16, `RecNames(x)` is immutable. The sole producer change is:

```gap
names := ShallowCopy(RecNames(x));; Sort(names);;
```

The same names are sorted in the same order. JSON ordering, formula digest,
groups, candidate universe, predicates, schemas, terminal tokens, and the
performance schedule are unchanged. This was a serializer/runtime mutability
bug, not an ANUPQ or mathematical failure.

## Hash chain

| File | Old bytes / SHA256 | New bytes / SHA256 |
|---|---|---|
| `search/d972_b345_q3_chief_v1.g` | 74,443 / `46827beb2b3cd93a9b29f9431b76ffc9626f7d40307dc2a6733f6900fa955b32` | 74,456 / `5a7146b2d119b667425e897b1a54d6daaf6582884e78bb87498179163f470a17` |
| `search/d972_b345_q3_gha_driver_v1.g` | 5,108 / `d44747f24a4d89d86b603ea3b7ec2c166f0e5fe90e235d03ab316047d1b5e135` | 5,108 / `fbf48d6e4103409362c3c93912ce2523a9f67f28b058665cac0034e2a073115b` |

The independent checker was not edited and remains:

```text
search/check_d972_b345_q3_chief_v1.py
87,732 bytes
9864e55f6e0ee1ae8100788e5ba127ef95bffd62535c3aa23a192cde6109cfcb
```

The updated prior replies are:

```text
sol/luna_reply_157da_b345_q3_chief.md
17,557 bytes
c96a3dd92c31bb9da2f4d59472add82275a7ef7047bfd40931f0410a34aafcb0

sol/luna_reply_157db_b345_q3_gha_driver.md
4,805 bytes
3e68f51cc494264ebd53d2b4080a65c7c8a886d9b928122ecfbc1c8d1891758b
```

Both now present the superseding 157dd producer/driver hashes as current and
record runs `32129602522` and `32130140976` with their exact pre-ANUPQ
serializer diagnoses.

The current code snapshot after that superseding empty-list repair is:

| File | Bytes | SHA256 |
|---|---:|---|
| `search/d972_b345_q3_chief_v1.g` | 74,595 | `459c9b1728316a064644ce2e658c0e09dd06b0722fab3e767aaf6f51ebb91d45` |
| `search/d972_b345_q3_gha_driver_v1.g` | 5,108 | `e3883d8f28dc07ddad5088f2b19e4f78680f5953ed7b5e3220e3f0dd892f4da1` |

## Static audit

For the 157dc repair itself, static inspection confirms that the only code
changes were:

1. `RecNames(x)` is wrapped in `ShallowCopy` before the existing `Sort`;
2. the driver's frozen producer SHA is changed from the old producer digest to
   the repaired digest.

The checker SHA pin remains exactly
`9864e55f6e0ee1ae8100788e5ba127ef95bffd62535c3aa23a192cde6109cfcb`.
Delimiter/control-token balance is unchanged, and the prior replies contain no
stale old hash presented as current. No workflow or mathematical file other
than the one-line serializer repair was changed.

Canary `32130140976` subsequently passed this immutable-sort repair and stopped
before ANUPQ because GAP serialized empty lists as strings. The superseding
157dd guard handles a length-zero list before `IsString`; it changes no formula,
predicate, universe, schema, or terminal. The next GHA canary is the required
runtime test.

## 157df atomic-write supersession

Canary `32130817181` passed; full run `32131160061` stopped before ANUPQ at
the first checkpoint because the GAP process lacked the prior rename binding.
The producer now loads the official IO package, closes its same-directory
temporary stream, and accepts replacement only when `IO_rename` returns true.
It does not remove the destination first and fails closed on package,
operation, or return-value failure.

The producer self-test performs two writes to
`ci/out/d972_b345_q3_atomic_io_smoke.json`, checks the exact second canonical
JSON plus newline against the first payload, removes the smoke file, and emits
exactly one `D972_B345_Q3_ATOMIC_IO_SELFTEST_PASS backend=IO_rename replace=true`
marker. The thin driver creates `ci/out` before reading the producer and gates
the marker count at one. The direct scan has one immediate post-return branch
marker for first typed witness or all 162 exhausted, with no per-candidate
logging and no A/B conclusion.

The superseding code hashes are:

```text
search/d972_b345_q3_chief_v1.g        76,704  e3dad87ad066fc9c605e1eecaddbe63efd63ac68500e0fcff0d6d62eb7d83af3
search/d972_b345_q3_gha_driver_v1.g    5,463  6a3cb5339468dd7f1b214c67d9791b0f752d0df625f06781470dc24c92a8a859
search/check_d972_b345_q3_chief_v1.py 87,732  9864e55f6e0ee1ae8100788e5ba127ef95bffd62535c3aa23a192cde6109cfcb
```

No formula, predicate, candidate order, terminal mapping, ANUPQ budget,
receipt acceptance, or checker code changed. Ready token:
`B345_Q3_ATOMIC_WRITE_REPAIR_READY_FOR_GHA`.

## 157dg checked-write supersession

Run `32132850360` established that the optional I/O package cannot be loaded
on the runner before ANUPQ. The prior replacement wording is superseded:
every output now uses core `OutputTextFile`, closes, rereads with `StringFile`,
and requires exact canonical bytes. This is deliberately a checked closed
write and makes no atomicity claim.

The two-write smoke and exact-one driver gate now use
`D972_B345_Q3_CHECKED_IO_SELFTEST_PASS backend=OutputTextFile replace=true readback=true`.
Partial output cannot be consumed by the checker because producer return and
readback must succeed before the checker command and final driver marker.

Current producer/driver/checker pins are:

```text
producer  76,867  b95fc29b326c3d6a378249cdeb03595eed8d0211a7fe0358fc02447d70d5f755
driver     5,488  93a03d8d44694f016603bebd3909fe718dbbd6fe8018c17f5460c040bc3aea76
checker   87,732  9864e55f6e0ee1ae8100788e5ba127ef95bffd62535c3aa23a192cde6109cfcb
```
