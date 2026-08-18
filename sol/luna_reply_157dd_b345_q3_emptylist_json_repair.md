# Luna reply 157dd — GAP empty-list JSON canary repair

Date: 2026-08-18

## Verdict

```text
B345_Q3_EMPTYLIST_JSON_REPAIR_READY
```

The pre-ANUPQ serialization failure is repaired with the single prescribed
type-order guard and its driver SHA-pin update. No checker, workflow, formula,
predicate, candidate universe, receipt schema, or terminal logic was changed.
No local GAP/Python execution, Git, or GHA was used.

## Failure and exact repair

Canary run `32130140976` at commit
`522dc918e51fe14f5c68ea19620b214e7930ec92` passed the prior immutable
`RecNames` repair, then stopped before ANUPQ with:

```text
Error, 157da selftest: cross-language formula digest drift
```

In GAP, `[]` satisfies both `IsList` and `IsString`. The serializer tested
`IsString` first, so empty word/map arrays in the formula manifest became JSON
`""`, whereas Python canonical JSON emits `[]`. Immediately before the existing
string branch, the producer now has:

```gap
# GAP's empty list also satisfies IsString; empty values in this schema are arrays.
if IsList(x) and Length(x)=0 then return "[]"; fi;
```

The 157dc mutable-name repair remains unchanged:

```gap
names := ShallowCopy(RecNames(x));; Sort(names);;
```

The expected formula SHA remains exactly
`b43284edac5b4dae945bb3b30ac0f177dc47df8724cb32acd6057b26d82a27ef`.

## Hash chain

| File | Old bytes / SHA256 | New bytes / SHA256 |
|---|---|---|
| `search/d972_b345_q3_chief_v1.g` | 74,456 / `5a7146b2d119b667425e897b1a54d6daaf6582884e78bb87498179163f470a17` | 74,595 / `459c9b1728316a064644ce2e658c0e09dd06b0722fab3e767aaf6f51ebb91d45` |
| `search/d972_b345_q3_gha_driver_v1.g` | 5,108 / `fbf48d6e4103409362c3c93912ce2523a9f67f28b058665cac0034e2a073115b` | 5,108 / `e3883d8f28dc07ddad5088f2b19e4f78680f5953ed7b5e3220e3f0dd892f4da1` |

The independent checker was not edited and remains:

```text
search/check_d972_b345_q3_chief_v1.py
87,732 bytes
9864e55f6e0ee1ae8100788e5ba127ef95bffd62535c3aa23a192cde6109cfcb
```

Updated prior replies are:

```text
sol/luna_reply_157da_b345_q3_chief.md
17,557 bytes
c96a3dd92c31bb9da2f4d59472add82275a7ef7047bfd40931f0410a34aafcb0

sol/luna_reply_157db_b345_q3_gha_driver.md
4,805 bytes
3e68f51cc494264ebd53d2b4080a65c7c8a886d9b928122ecfbc1c8d1891758b

sol/luna_reply_157dc_b345_q3_canary_repair.md
3,462 bytes
aa47f219ba822fd403f72b69316fcc357438ddc8f8d64370d1151acb4ea71be5
```

## Static audit and next gate

The producer diff is only the empty-list guard above. The driver diff is only
its frozen producer SHA. The checker pin remains exactly
`9864e55f6e0ee1ae8100788e5ba127ef95bffd62535c3aa23a192cde6109cfcb`.
Run `32130140976` is recorded as a pre-ANUPQ serialization stop, not an ANUPQ
or mathematical result. The next registered GHA canary is the runtime test of
this repair.

## 157df atomic-write supersession

Canary `32130817181` passed. Full run `32131160061` stopped before ANUPQ at
the first checkpoint because the GAP process lacked the prior rename binding.
The producer now uses the official IO package and a closed same-directory
temporary stream with `IO_rename`; destination deletion before replacement is
not permitted, and all package/operation/return failures are fatal.

Its self-test performs two atomic writes to the fixed `ci/out` smoke path,
reads back the second exact canonical JSON plus newline, verifies it differs
from the first payload, removes the smoke file, and emits exactly one
`D972_B345_Q3_ATOMIC_IO_SELFTEST_PASS backend=IO_rename replace=true` marker.
The driver creates `ci/out` before reading the producer and enforces the
producer marker count. Immediately after the direct scan, one branch marker
records first typed witness or all 162 exhausted; it is not an A/B conclusion.

Current hashes:

```text
search/d972_b345_q3_chief_v1.g        76,704  e3dad87ad066fc9c605e1eecaddbe63efd63ac68500e0fcff0d6d62eb7d83af3
search/d972_b345_q3_gha_driver_v1.g    5,463  6a3cb5339468dd7f1b214c67d9791b0f752d0df625f06781470dc24c92a8a859
search/check_d972_b345_q3_chief_v1.py 87,732  9864e55f6e0ee1ae8100788e5ba127ef95bffd62535c3aa23a192cde6109cfcb
```

The static semantic diff is limited to I/O, self-test, and logging gates;
formula, predicate, universe/order, terminal mapping, ANUPQ budget, receipt
acceptance, and checker remain unchanged. Ready token:
`B345_Q3_ATOMIC_WRITE_REPAIR_READY_FOR_GHA`.
