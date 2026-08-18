# Luna task 157dd — GAP empty-list JSON canary repair

Date: 2026-08-18

## Trigger

Repaired canary run `32130140976` at commit
`522dc918e51fe14f5c68ea19620b214e7930ec92` passed package setup and the
immutable-`RecNames` point, then stopped before ANUPQ with:

```text
Error, 157da selftest: cross-language formula digest drift
```

Static comparison identifies the exact serialization mismatch. In GAP, the
empty list also satisfies `IsString`. `D972Q3Json` currently tests `IsString`
before its general list branch, so empty word/map lists become JSON `""` rather
than Python canonical JSON `[]`. The pinned row18 serializer already documents
and handles this GAP behavior.

## Role and authorized files

You are Luna. Apply the minimum semantics-preserving JSON repair and update its
hash chain. Authorized files only:

1. `search/d972_b345_q3_chief_v1.g`
2. `search/d972_b345_q3_gha_driver_v1.g`
3. `sol/luna_reply_157da_b345_q3_chief.md`
4. `sol/luna_reply_157db_b345_q3_gha_driver.md`
5. `sol/luna_reply_157dc_b345_q3_canary_repair.md`
6. `sol/luna_reply_157dd_b345_q3_emptylist_json_repair.md`

No checker edit, workflow edit, local execution, Git/GHA, or mathematical
change.

## Exact repair

Immediately before the `IsString(x)` branch in `D972Q3Json`, add the same
type-order guard used by the pinned row18 producer:

```gap
# GAP's empty list also satisfies IsString; empty values in this schema are arrays.
if IsList(x) and Length(x)=0 then return "[]"; fi;
```

Keep the repaired mutable record-name sorting from 157dc. Do not change the
expected formula SHA
`b43284edac5b4dae945bb3b30ac0f177dc47df8724cb32acd6057b26d82a27ef`,
formula construction, JSON key ordering, predicates, universe, receipt schema,
or terminal logic.

Update the driver producer SHA only. Its checker SHA must remain exactly:

```text
9864e55f6e0ee1ae8100788e5ba127ef95bffd62535c3aa23a192cde6109cfcb
```

Update prior replies' current hash tables and record canary `32130140976` as a
pre-ANUPQ serialization stop. The new 157dd reply must give old/new hashes,
byte counts, exact code diff description, and state that the next GHA canary is
the runtime test.

Terminal implementation token:

```text
B345_Q3_EMPTYLIST_JSON_REPAIR_READY
```
