# Luna reply 157dg — B345 q3 checked closed-write repair

Date: 2026-08-18

## Verdict

```text
B345_Q3_CHECKED_WRITE_REPAIR_READY_FOR_GHA
```

The repair is limited to output I/O, the two-write self-test marker, the
driver gate, and the authorized history replies. Mathematical predicates,
candidate order, terminals, checker, frozen inputs, and heavy-call budgets are
unchanged. No local GAP/Python, Git, or GHA operation was run.

## Runtime evidence and exact repair

The 157df code was at commit `a89506553925d0c28515b575c9a9fd79f189714a`.
Canary `32132850360` stopped in the I/O smoke with an unavailable optional I/O
package, before ANUPQ, coarse construction, or candidate enumeration. This is
not a mathematical/search result.

The producer helper is now `D972Q3CheckedWrite`. For every checkpoint and
final output it constructs the canonical JSON plus exactly one newline once,
writes the final path with core `OutputTextFile(path,false)`, disables print
formatting, writes the expected bytes, closes the stream, rereads with core
`StringFile`, and fails unless the readback is non-fail and byte-for-byte equal.
No optional package, temporary path, shell move, or atomicity claim remains.

The smoke still writes two distinct records to the fixed
`ci/out/d972_b345_q3_checked_io_smoke.json`, checks that the second exact
payload is present and the first is absent, then removes the smoke file. It
emits exactly one:

```text
D972_B345_Q3_CHECKED_IO_SELFTEST_PASS backend=OutputTextFile replace=true readback=true
```

The driver requires that exact marker binding and count one before running the
checker. If a producer is killed or readback fails, the producer does not
return, so the checker is not invoked and the final driver success marker is
absent; a partial file is never consumed as a successful artifact.

The existing one-line `D972_B345_Q3_DIRECT_SCAN_RESULT` branch markers are
unchanged.

## Final hashes

```text
search/d972_b345_q3_chief_v1.g
76,867 bytes
b95fc29b326c3d6a378249cdeb03595eed8d0211a7fe0358fc02447d70d5f755

search/d972_b345_q3_gha_driver_v1.g
5,488 bytes
93a03d8d44694f016603bebd3909fe718dbbd6fe8018c17f5460c040bc3aea76

search/check_d972_b345_q3_chief_v1.py
87,732 bytes
9864e55f6e0ee1ae8100788e5ba127ef95bffd62535c3aa23a192cde6109cfcb
```

The authorized prior histories were updated with this superseding checked
write contract; no checker or workflow file was touched.

```text
sol/luna_reply_157da_b345_q3_chief.md          20,517 bytes  3c9031a96ac98260db14d6184f7b1e2172c1df7b9a9fbdfe7cc17840ce371510
sol/luna_reply_157db_b345_q3_gha_driver.md      7,148 bytes  3dc01bf203b22f36564c2dcd959bb3df44fa5447e53323aef0ae994cd6ea6659
sol/luna_reply_157dc_b345_q3_canary_repair.md   5,996 bytes  0a25b896f97b560ca2c00486c24517fa6cd3eb93e03b613a5bd643210768e031
sol/luna_reply_157dd_b345_q3_emptylist_json_repair.md
                                                5,289 bytes  78fc949805e5ce996b4e1e5e9acf510ed83a0a83c1edf61bddb5012e10bff53b
sol/luna_reply_157df_b345_q3_atomic_write_repair.md
                                                4,995 bytes  c60c5502ba270dae99e0916d3f1798f74b0d1b3435239bebbd2bb57d83893f7d
```

## Static audit

The bounded source audit confirms zero optional I/O-package loads, zero
rename/temp-file calls, and no shell file operation was introduced; existing
fixed driver commands are unchanged;
every producer output goes through the checked helper; the helper closes before
exact readback; the smoke performs two real replacement writes; the driver
enforces the exact-one new marker; direct-scan branch markers are unchanged;
and the checker SHA and mathematical pins remain unchanged. The receipt now
records `checked_write_policy` and an explicit `partial_write_nonpromotion`
contract.

Terminal implementation token:

```text
B345_Q3_CHECKED_WRITE_REPAIR_READY_FOR_GHA
```
