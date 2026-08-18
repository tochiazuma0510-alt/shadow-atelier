# Luna reply 157di — B345 q3 checker index repair

Date: 2026-08-18

## Verdict

```text
B345_Q3_CHECKER_INDEX_REPAIR_READY_FOR_GHA
```

## Runtime evidence and exact diagnosis

Full run `32134100496` at commit
`c7ef41aab6507d2992f3c89913db84ac839ca3dd` produced the exact direct-scan
candidate:

```text
D972_B345_Q3_DIRECT_SCAN_RESULT result=first_typed_witness evaluated=28 exponent=2 correction_index=1
B345_Q3_TYPED_SIGN_EXACT_WITH_WORD_CORRECTION ... solutions=1 evaluated=28
```

The producer took about 10.2 seconds. The independent checker then reported
`Pi4 settlement inverse compositions`. This is a checker-only deterministic
indexing defect, not a producer or mathematical rejection: `PcCollector.unit`
is one-based, but the old inverse-composition loop used zero-based `i` and
called `unit(i)`. At `i=0`, Python's `row[-1]` placed the unit in the final
coordinate, so even a rank-greater-than-one identity map was rejected. The
producer directions, receipt fields, frozen inputs, predicates, and 162-row
universe remain unchanged.

## Repair

`validate_inverse_pc_maps` is now the single path used by the production
settlement validator and the self-test. It normalizes both image lists,
validates both maps as homomorphisms, then iterates `idx in range(pc.n)` and
checks both

```text
inverse(forward(g_idx)) = unit(idx + 1)
forward(inverse(g_idx)) = unit(idx + 1).
```

`PcCollector.unit` now fails closed unless its argument is an integer in
`1..n`. The regression fixture is a genuine rank-2 elementary abelian
exponent-3 `PcCollector` (`E2[3]`): the identity pair passes, `unit(0)` is
rejected, and an identity forward map paired with a deliberately swapped
noninverse inverse map is rejected. This canary fails under the old
`unit(idx)` behavior. No receipt field or acceptance predicate was weakened.

The one permitted lightweight checker self-test passed exactly as follows:

```text
D972_B345_Q3_CHECKER_SELFTEST_PASS mutations=9 orientation_canaries=1 rank2_pc_inverse_canaries=2 formula_sha256=b43284edac5b4dae945bb3b30ac0f177dc47df8724cb32acd6057b26d82a27ef
```

Bounded source checks confirm the helper has one definition and is used by the
production path, both composition orders remain present, the inverse path uses
`unit(idx + 1)`, the rank-2 canary is present, and the driver pins the repaired
checker and the unchanged producer. No local GAP, heavy enumeration, Git, GHA,
or full-artifact checker replay was run in this repair.

## Final code pins

```text
search/d972_b345_q3_chief_v1.g         76,867 bytes  b95fc29b326c3d6a378249cdeb03595eed8d0211a7fe0358fc02447d70d5f755
search/d972_b345_q3_gha_driver_v1.g      5,488 bytes  c397cd837ff6814f7b7a8ca0604c6aed54fa0bc85bb577516ea1c6e7df83a831
search/check_d972_b345_q3_chief_v1.py  89,082 bytes  ddb52ddae18327209692f0f6eb8b4f65cbdd446155be660a621de24274cc3f73
```

The six authorized prior histories were updated with this supersession. Their
post-update sizes and SHA-256 values are:

```text
sol/luna_reply_157da_b345_q3_chief.md          22,003 bytes  f963473be5105f7f613356e59e11d1001fc23fadb965cd925b54bb030a0a1686
sol/luna_reply_157db_b345_q3_gha_driver.md      8,663 bytes  237e23243731207237ffe4ef23b8a68158ca30bacc9189a7e15485b3cad76a68
sol/luna_reply_157dc_b345_q3_canary_repair.md   7,482 bytes  4b5f17f273da26792ae8e3c880240ccfe04ec5355e2c8896c709688cc19dbcea
sol/luna_reply_157dd_b345_q3_emptylist_json_repair.md
                                                  6,775 bytes  c812ac993adb41976c876afb67e74fb67c5b6c961005bf1260e145c37551c975
sol/luna_reply_157df_b345_q3_atomic_write_repair.md
                                                  6,481 bytes  bff7af14e7e467f33484e2bb871ee9f4d55e773eadb028a949232012bf65cf28
sol/luna_reply_157dg_b345_q3_checked_write_repair.md
                                                  5,337 bytes  2aac2215437881a259bfd4192e1071933fc6800eb5ce9d894b92600240584c9e
```

The code pins and history digests above were computed after the repair edits.
The old run's witness is a candidate only: a fresh GHA run must replay the
downloaded artifact with this checker and emit its pass marker before any
terminal claim.

Terminal implementation token:

```text
B345_Q3_CHECKER_INDEX_REPAIR_READY_FOR_GHA
```
