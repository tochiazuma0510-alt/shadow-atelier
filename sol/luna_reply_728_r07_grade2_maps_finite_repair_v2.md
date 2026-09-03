# Luna Reply 728 — grade-two map pair v2 finite repair

## Result

`DONE`. Task719 F719-1 through F719-4だけを versioned v2 producer/checker に修理した。v1 は上書きしていない。actual 40-table artifact build、GHA、git は実行していない。

## Outputs

| file | bytes | LF | CRLF | final LF | SHA-256 |
|---|---:|---:|---:|---|---|
| `search/d972_r07_grade2_forward_adjoint_maps_v2.py` | 44,667 | 959 | 0 | yes | `fdcb9a8ca9804179f350500c02203cdde550498b5cc5912ff1b0bde1d92e4d84` |
| `search/check_d972_r07_grade2_forward_adjoint_maps_v2.py` | 48,459 | 988 | 0 | yes | `e388300c88de674d6e4550a7f20a40031488e724e40e73cdc89189b472ae61f0` |
| `sol/luna_reply_728_r07_grade2_maps_finite_repair_v2.md` | sealed reply | sealed reply | 0 | yes | supplied externally after sealing |

Producer v2 was finalized first. Checker v2 pins exactly:

```text
path   search/d972_r07_grade2_forward_adjoint_maps_v2.py
SHA256 fdcb9a8ca9804179f350500c02203cdde550498b5cc5912ff1b0bde1d92e4d84
```

## Four finite repairs

### F719-1: immutable producer binding

Checker v2 hashes the actual producer-v2 bytes before artifact parsing and requires the literal digest above. The manifest `producer_sha256` must equal that same authenticated digest. Bounded fixtures reject both a changed-byte source path and a wrong literal without importing or executing producer code.

### F719-2: production actor/prefix fixture coverage

Both selftests now drive the actual record generators for character 0:

- `x,x^-1` and `y,y^-1`: four complete 36,288-coordinate actor tables;
- canonical sparse reduction and the actual inverse validator over all 36,288 source coordinates;
- full-width sparse application of both inverse compositions;
- the actual six-occurrence aggregation generator;
- a source coordinate belonging to a genuinely nonidentity g760 prefix, through aggregation and sparse application;
- the full actual B table through the production writer/parser path (producer) or independent canonical parser path (checker).

Only after these branches finish do the receipts report `both_inverse_pairs=true` and `nontrivial_prefix=true`. No 40-table artifact directory is built.

### F719-3: strict nested integer types

Checker v2 uses recursive `strict_fixed` comparison for dimensions, coordinate order, occurrence triples, source/marking/word/prefix receipts, and the complete structural receipt. Every expected integer requires `is_int`, excluding bool. The existing exact table-receipt key gate and integer gate remain active. Live production-validator mutations reject:

- actor `1 -> true`;
- character `0 -> false`;
- occurrence coordinate `0 -> false`;
- dimension `characters_count=4 -> true`;
- actor-order coordinate `1 -> true`.

### F719-4: safe checker output

`safe_output_path` is called by the production output writer. It requires a fresh output outside both the authenticated artifact tree and repository tree, rejects symlink/junction traversal in existing ancestors, creates only a validated external parent, and retains same-directory temporary write, flush/fsync, atomic replace, and byte readback. Live fixtures reject an existing file, artifact descendant, and repository descendant; the existing fixture file is confirmed unchanged.

## Preserved core and diff scope

The v2 producer differs from v1 only by versioned schema/marker and the bounded actual actor/prefix fixture additions (`+34/-3` lines). The v2 checker adds the four audited repair groups and corresponding bounded fixtures (`+211/-29` lines); sparse formulas and table construction are unchanged.

Preserved: `V_a=36,288`, `P=48,384`, six coupled monomials, exact 40-table roster, `(source,destination,c)` orientation, mod-3 duplicate cancellation, mechanical transpose, all-character production inverse identities, occurrence-first aggregation, independent checker arithmetic/import boundary, canonical EOF/digests, sparse-only construction, exclusive CLI, and false downstream claims.

## Bounded commands and results

Executed with bytecode cache redirected outside the repository:

```text
python -m py_compile search/d972_r07_grade2_forward_adjoint_maps_v2.py search/check_d972_r07_grade2_forward_adjoint_maps_v2.py
python search/d972_r07_grade2_forward_adjoint_maps_v2.py --selftest
python search/check_d972_r07_grade2_forward_adjoint_maps_v2.py --selftest
```

Results:

```text
py_compile: PASS
producer v2 selftest: PASS
  fixture_rejection_count=2
  actual actor coordinates checked=2 inverse pairs x 36,288
  actual aggregation records canonicalized=36,288
checker v2 selftest: PASS
  fixture_rejection_count=12
  actual actor coordinates checked=2 inverse pairs x 36,288
  actual aggregation records parsed=36,288
```

Checker rejection count 12 consists of truncation, trailing bytes, two table-descriptor bool mutations, three fixed-manifest bool mutations, two producer-pin mutations, and three safe-output mutations.

```text
ACTUAL_MAP_BUILD=DEFERRED_TO_GHA
GRADE2_DECISION=NOT_RUN
verified=false
```

`R07_GRADE2_FORWARD_ADJOINT_MAPS_V2_FINITE_REPAIR_COMPLETE`
