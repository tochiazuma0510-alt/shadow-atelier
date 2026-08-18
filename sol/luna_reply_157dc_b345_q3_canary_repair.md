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
16,846 bytes
950ed4156ec913d19e9f798958e1811e08cb815a31b6904e91db2d30effece64

sol/luna_reply_157db_b345_q3_gha_driver.md
4,299 bytes
45fbbd50e7640e1b263d1ba651b65141d660e5661bf54e23a2069496840730f1
```

Both now present the repaired producer/driver hashes as current and record run
`32129602522` with the exact immutable-list diagnosis.

## Static audit

Static inspection confirms that the only code changes are:

1. `RecNames(x)` is wrapped in `ShallowCopy` before the existing `Sort`;
2. the driver's frozen producer SHA is changed from the old producer digest to
   the repaired digest.

The checker SHA pin remains exactly
`9864e55f6e0ee1ae8100788e5ba127ef95bffd62535c3aa23a192cde6109cfcb`.
Delimiter/control-token balance is unchanged, and the prior replies contain no
stale old hash presented as current. No workflow or mathematical file other
than the one-line serializer repair was changed.

The repaired GHA canary is the required runtime test.
