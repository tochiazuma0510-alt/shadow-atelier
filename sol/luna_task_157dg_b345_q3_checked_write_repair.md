# Luna task 157dg — remove unavailable IO dependency; checked closed-write canary

Date: 2026-08-18

## Runtime evidence

157df code commit:

```text
a89506553925d0c28515b575c9a9fd79f189714a
```

GHA canary `32132850360` stopped in the new I/O smoke with:

```text
Error, 157df: official IO package unavailable
```

The setup-gap 4.16.0 runner does not ship/load the optional compiled IO
package. This again occurred before ANUPQ, the coarse model, and all 162
candidates. It is not a mathematical/search result.

The workflow uploads artifacts only after a successful GAP step. Therefore an
atomic rename is not load-bearing: a crash or partial write cannot reach the
checker/driver success path. The smallest robust contract is close + exact
readback using GAP core I/O, with no optional package and no shell command.

## Role and authorized files

You are Luna. Authorized files only:

1. `search/d972_b345_q3_chief_v1.g`
2. `search/d972_b345_q3_gha_driver_v1.g`
3. `sol/luna_reply_157da_b345_q3_chief.md`
4. `sol/luna_reply_157db_b345_q3_gha_driver.md`
5. `sol/luna_reply_157dc_b345_q3_canary_repair.md`
6. `sol/luna_reply_157dd_b345_q3_emptylist_json_repair.md`
7. `sol/luna_reply_157df_b345_q3_atomic_write_repair.md`
8. `sol/luna_reply_157dg_b345_q3_checked_write_repair.md`

Do not edit the checker, workflow, frozen inputs, or 157de files. No local
GAP/Python, Git, or GHA operation.

## Exact repair

1. Remove the IO-package dependency and every `IO_rename`/temp-file call from
   the producer. Do not replace it with `Exec`, `mv`, another optional package,
   or an untested GAP API.

2. Rename the helper and claims honestly to a checked closed write. For every
   output:

   - build the exact canonical JSON plus one newline once;
   - open the final target with core `OutputTextFile(path,false)`;
   - disable print formatting, write the exact bytes, and close the stream;
   - read the target with core `StringFile`;
   - fail unless readback is non-fail and byte-for-byte equal to the expected
     string.

   A partially written file after a killed/error job must never be promoted:
   the producer cannot return, the Python checker is not run, and the final
   driver marker is absent. State this explicitly in the receipt/reply.

3. Keep the two-write replacement selftest, but rename its stable marker to:

```text
D972_B345_Q3_CHECKED_IO_SELFTEST_PASS backend=OutputTextFile replace=true readback=true
```

   The driver must gate its exact binding/count=1. The smoke still writes two
   distinct records to the same fixed path, proves the second exact bytes are
   present and the first are absent, then removes the file.

4. Keep the already-audited one-line `DIRECT_SCAN_RESULT` branch markers
   unchanged. Do not alter any mathematical predicate, 162-candidate order,
   terminal, receipt acceptance condition, checker, or heavy-call budget.

5. Update performance/reply wording: do not claim atomicity. Use “closed exact
   write with immediate byte readback” and explain why checker/driver success
   cannot consume a partial file. Repin only the producer in the driver; the
   checker SHA and all mathematical pins remain unchanged.

6. Update the authorized prior histories and create the 157dg reply with final
   SHA256/bytes and this canary/run evidence.

## Static gates

- `LoadPackage("io")`, `IO_rename`, and `RenameFile` occur zero times in the
  producer/driver;
- no shell file operation is introduced;
- each checked write closes before exact readback;
- two-write replacement smoke and exact-one driver marker remain real;
- `DIRECT_SCAN_RESULT` remains one line and branch-exact;
- checker SHA/predicate/universe/terminal/heavy schedule are unchanged;
- `git diff --check` is clean within scope.

Terminal implementation token:

```text
B345_Q3_CHECKED_WRITE_REPAIR_READY_FOR_GHA
```
