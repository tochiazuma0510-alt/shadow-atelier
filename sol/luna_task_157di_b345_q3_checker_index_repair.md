# Luna task 157di — Pi4 inverse-composition checker off-by-one repair

Date: 2026-08-18

## Runtime evidence

GHA full run `32134100496` on commit
`c7ef41aab6507d2992f3c89913db84ac839ca3dd` produced:

```text
D972_B345_Q3_DIRECT_SCAN_RESULT result=first_typed_witness evaluated=28 exponent=2 correction_index=1
B345_Q3_TYPED_SIGN_EXACT_WITH_WORD_CORRECTION ... solutions=1 evaluated=28
B345_Q3_CHECKER_FAIL Pi4 settlement inverse compositions
```

The producer finished in about 10.2 seconds. Independent source audit found a
deterministic checker indexing bug: `PcCollector.unit(i)` is 1-based, but the
composition loop uses `for i in range(pc4.n)` and compares to `unit(i)`. At
`i=0`, Python writes the 1 into `row[-1]`, so even identity maps fail when the
pc rank exceeds one. Producer forward/inverse directions are otherwise
correct.

## Role and authorized files

You are Luna. Authorized files only:

1. `search/check_d972_b345_q3_chief_v1.py`
2. `search/d972_b345_q3_gha_driver_v1.g`
3. `sol/luna_reply_157da_b345_q3_chief.md`
4. `sol/luna_reply_157db_b345_q3_gha_driver.md`
5. `sol/luna_reply_157dc_b345_q3_canary_repair.md`
6. `sol/luna_reply_157dd_b345_q3_emptylist_json_repair.md`
7. `sol/luna_reply_157df_b345_q3_atomic_write_repair.md`
8. `sol/luna_reply_157dg_b345_q3_checked_write_repair.md`
9. `sol/luna_reply_157di_b345_q3_checker_index_repair.md`

Do not change producer mathematics, workflow, frozen inputs, or 157de files.
No local GAP/heavy Python/Git/GHA. One lightweight checker selftest is allowed
only after implementing the bounded regression canary.

## Exact repair

1. Factor the forward/inverse pc composition check into one helper used by the
   production validator and selftest. It must:

   - validate both maps as homomorphisms;
   - iterate zero-based Python indices `idx in range(pc.n)`;
   - compare both compositions to `pc.unit(idx + 1)`;
   - retain both orders `inverse(forward(g_i))` and
     `forward(inverse(g_i))`.

2. Add a genuine rank-2 elementary abelian exponent-3 `PcCollector` selftest,
   not the existing rank-1 cyclic receipt. Test the identity pair and require a
   deliberately swapped/noninverse pair to reject. This must fail under the
   old `unit(idx)` implementation. Update mutation/canary counts honestly.

3. Change no receipt field and weaken no check. The producer witness remains a
   candidate until the repaired checker replays the downloaded artifact and
   emits its pass marker.

4. Repin the driver to the new checker SHA; producer SHA remains exactly
   `b95fc29b326c3d6a378249cdeb03595eed8d0211a7fe0358fc02447d70d5f755`.
   Update authorized histories and write the 157di reply with hashes/bytes,
   run evidence, and a precise producer-vs-checker verdict.

## Static/runtime gates

- no `pc.unit(idx)` or `pc.unit(i)` with a zero-based loop remains in the
  inverse-composition path;
- both composition orders remain checked;
- rank-2 identity canary passes and bad inverse pair rejects;
- checker selftest passes once; driver pins exact new checker SHA;
- producer/frozen inputs/math/162 universe/terminal are byte-identical;
- `git diff --check` clean in scope.

Terminal implementation token:

```text
B345_Q3_CHECKER_INDEX_REPAIR_READY_FOR_GHA
```
