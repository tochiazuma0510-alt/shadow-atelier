# Luna reply — Task503 A4 actual-production shard wiring

Implemented exactly the four requested outputs.  The frozen v23/v32/v42
owners were not edited; no production 6,441-row run, GHA, or git operation
was performed.

## Outputs and pins

| output | bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_word_independent_successor_kernel_v24.py` | 34535 | `8dc698e43fa7971dff4af3a5a19a7ac309ab5d43a19bb1f5189c0c222df01dfe` |
| `crosscheck/check_d972_r07_word_independent_successor_kernel_v33.py` | 24033 | `44e79864424a21d836d0b61dbe066889e3567d250e722026143a2eb8f7d87ccf` |
| `search/d972_r07_word_independent_successor_kernel_gha_driver_v43.g` | 15449 | `36be6a635fa7399c37048ef45debb5c25d5ede8cc1414fa153a7e8bb0dd7c8bb` |

Generated-body pins are v24 `285814 / 9e3619f2e83dc7bea2e58d250bff3fafc24b8e09910c389b7a402a3b2d0d2d6a` and v33 `312046 / cb1d2b390beb3bdbd71d2175983310971d0669f6a6d7b77e1e64f29ceae61f57`; both wrapper-local nonzero result-pin gates and v43 pins are active.

The v43 transport carries release `56410 / 5771806de2bfa769ef7d83364acd65d618be2a663d02a74497943c746a336e3` and authenticates all six row-26 members, including HEAD `700 / 910cc8afcca333dab56d9fefe35e63066eab764ac6325e3130c43a3c3d6f0114` and delta2 `3625 / acb34c8c69863cc274df4a12c614b002101770d97292f2c0df8bb43158df8523`.

## Wiring account

v24 constructs/restores one physical controller in `build_kernel`, calls
`prepare` from `consume_row`, closes the exact `m=min(64,len(private_candidates))`
prefix from the live `Oracle.query` correlation loop, direct-restores sealed
maps/formals/events/counters before resumed correlation, and commits once after
the row terminal.  Bridge/row/chunk/sample prefixes are appended only after
that commit.  Shard is written before HEAD, and the ResourceStop reference is
typed `physical_shard_chain`; the pre-first-close path remains the ordinary
row-26 reference.  The physical HEAD is marked obsolete after commit.

v33 extends the live `validate_terminal_checkpoint` route independently of v24
and recomputes the prefix, mask, dual/correlation values, reductions, formals,
events, epoch, rank, and semantic counters.  v43 has one producer process,
typed RESOURCE handling that skips the checker, and invokes at most one checker
for a positive producer terminal with exact owned one-line markers.

## Bounded gates

- v24 source-patch/cardinality, AST, generated compile, and active generated-pin gate: PASS.
- v33 source-patch/cardinality, AST, generated compile, self-test, and active generated-pin gate: PASS.
- Real `Oracle.query` fixture: `batches=3`, interruption after third close, file-HEAD restore, direct restore `1`, insertion/reduction/correlation during admitted restore `0`, uninterrupted/restored equality `1`; call counts `prepare=1 close_batch=3 commit=1 resumed_direct_restore=1`.
- Independent checker physical fixture: validation calls `1`, rank `64`; independently re-sealed accepted-mask, extra-entry, row, and raw-identity mutations were all rejected.
- v43 wrapper/generated pin comparison, exact branch/marker static checks, GAP `ReadAsFunction` reachability, and generated-driver parse: PASS.  GAP reached the typed authority-input gate before any network or production command.

The mathematical status remains A4 `1/3 UNKNOWN_RESOURCE`, cross-checked through row 26.  Local Windows disk-backed `write_atomic` was not used for an unbounded run; its existing fail-closed platform guard remains unchanged.  Temporary fixture files were outside the repository and removed.

TASK503_R07_A4_ACTUAL_PRODUCTION_SHARD_WIRING_PASS
