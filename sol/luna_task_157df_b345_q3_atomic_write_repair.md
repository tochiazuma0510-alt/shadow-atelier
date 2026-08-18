# Luna task 157df — GAP 4.16 atomic checkpoint repair and observable direct-route split

Date: 2026-08-18

## Incident and scope

GHA canary `32130817181` passed. Full dispatch `32131160061` then stopped at
the first production checkpoint, before ANUPQ and before every candidate:

```text
D972_B345_Q3_PHASE pins ...
Error, Variable: 'RenameFile' must have an assigned value
```

This is a production-only I/O API error, not a mathematical or search result.
GAP 4.16 core has no `RenameFile`. The bundled deposited IO package exposes
the documented `IO_rename(oldpath,newpath)` operation, returning true/fail.

You are Luna. Repair this narrowly, keep every mathematical predicate and the
registered 162-candidate universe unchanged, and make the positive/all-negative
branch visible directly in the live GHA log.

## Authorized files only

1. `search/d972_b345_q3_chief_v1.g`
2. `search/d972_b345_q3_gha_driver_v1.g`
3. `sol/luna_reply_157da_b345_q3_chief.md`
4. `sol/luna_reply_157db_b345_q3_gha_driver.md`
5. `sol/luna_reply_157dc_b345_q3_canary_repair.md`
6. `sol/luna_reply_157dd_b345_q3_emptylist_json_repair.md`
7. `sol/luna_reply_157df_b345_q3_atomic_write_repair.md`

Do not edit the checker, workflow, frozen mathematical inputs, or the separate
157de positive-first files. No local GAP/Python, Git, or GHA operation.

## Required repair

1. Replace the nonexistent `RenameFile` call with the official IO-package
   primitive. `D972Q3AtomicWrite` must fail closed unless:

   - `LoadPackage("io")` succeeds;
   - `IO_rename` is bound;
   - the JSON is written to `path.tmp` in the same directory and the stream is
     closed before the rename;
   - `IO_rename(tmp,path)` returns exactly `true`.

2. Do **not** shell out for the rename. Do **not** remove the old destination
   before `IO_rename`; on the production POSIX runner, same-directory rename is
   the atomic replacement primitive. A stale temp may be overwritten before
   the rename.

3. Extend the producer self-test with a real, tiny I/O smoke that performs two
   atomic writes to the same fixed `ci/out` smoke path, reads back the second
   exact canonical JSON plus newline, and removes the smoke file after success.
   Extend the self-test branch of the thin driver to create `ci/out` before
   reading the producer. Require exactly one new marker:

```text
D972_B345_Q3_ATOMIC_IO_SELFTEST_PASS backend=IO_rename replace=true
```

   This must run before the next canary is allowed to pass, so another
   production-only checkpoint API error cannot escape the canary.

4. Immediately after `D972Q3DirectScan` returns, print and flush exactly one
   human-readable branch marker. Use stable values such as:

```text
D972_B345_Q3_DIRECT_SCAN_RESULT result=first_typed_witness evaluated=<n> exponent=<n> correction_index=<n>
D972_B345_Q3_DIRECT_SCAN_RESULT result=all_162_negative evaluated=162 next=PB5_typed_d2_bundle
```

   The first branch must agree with `FIRST_TYPED_WITNESS` and the selected
   receipt. The second must agree with `ALL_162_EXHAUSTED`; it is not an A/B
   conclusion. Do not add per-candidate logging or otherwise slow the hot loop.

5. Repin the driver to the repaired producer SHA. Keep the checker SHA and all
   mathematical hashes unchanged. Update the prior reply hash tables/history
   and write the new concise 157df reply with final SHA256/byte counts and a
   static assertion that the semantic diff is limited to I/O and logging.

## Static gates

- no `RenameFile` remains in either 157da or the repaired reply claims;
- exactly one `IO_rename` implementation call;
- the producer self-test actually exercises replacement, not merely package
  availability;
- driver enforces the I/O marker exactly once;
- checker SHA is unchanged;
- no mathematical predicate, candidate order, terminal mapping, ANUPQ budget,
  or receipt acceptance condition changes;
- all source pins are exact and no authorized-scope violation occurred.

Terminal implementation token:

```text
B345_Q3_ATOMIC_WRITE_REPAIR_READY_FOR_GHA
```
