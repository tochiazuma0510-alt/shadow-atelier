# Luna task 157dc — GAP 4.16 immutable `RecNames` canary repair

Date: 2026-08-18

## Trigger and exact failure

GHA canary run `32129602522`, commit
`b40c7fcae815a4fe6e725001496982e24d6198aa`, completed setup and failed in
the GAP-script step after about 1m39s with:

```text
Error, immutable lists cannot be sorted
```

The source-local cause is `D972Q3Json` in
`search/d972_b345_q3_chief_v1.g`:

```gap
names := RecNames(x);; Sort(names);;
```

On GAP 4.16 the returned list is immutable. This is a serialization/runtime
bug, not a mathematical or ANUPQ failure.

## Role and authorized files

You are Luna. Make the minimum semantics-preserving repair and update its hash
chain. Authorized files only:

1. `search/d972_b345_q3_chief_v1.g`
2. `search/d972_b345_q3_gha_driver_v1.g`
3. `sol/luna_reply_157da_b345_q3_chief.md`
4. `sol/luna_reply_157db_b345_q3_gha_driver.md`
5. `sol/luna_reply_157dc_b345_q3_canary_repair.md`

No checker edit, workflow edit, GAP/Python/Git/GHA execution, or unrelated
cleanup.

## Required repair

Replace only the mutation of the immutable `RecNames` list by sorting a mutable
copy, e.g.:

```gap
names := ShallowCopy(RecNames(x));; Sort(names);;
```

Do not change JSON ordering, formula digest, any group construction, candidate
universe, predicate, terminal token, performance schedule, or receipt schema.

Update the driver producer SHA pin to the repaired producer. The checker SHA must
remain exactly:

```text
9864e55f6e0ee1ae8100788e5ba127ef95bffd62535c3aa23a192cde6109cfcb
```

Update the two prior replies' SHA tables/prose so they no longer claim the old
producer/driver hashes as current. Record the failed canary run and its exact
diagnosis. Create the 157dc reply with old/new hashes, byte counts, and a static
assertion that the only code changes are the mutable-copy repair and driver pin.

Do not run locally; the repaired GHA canary is the runtime test.

Terminal implementation token:

```text
B345_Q3_GAP416_RECNAME_REPAIR_READY
```
