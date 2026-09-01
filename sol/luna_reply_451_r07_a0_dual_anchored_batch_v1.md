# Luna reply 451 — R07 A0 dual-anchored ACTIVE batch v1

Status: **bounded implementation complete; production candidate only**.

## Exact outputs

| path | bytes | SHA256 |
|---|---:|---|
| `search/d972_r07_a0_dual_anchored_active_batch_v1.py` | 13834 | `ca7fb15e06dd04881146c38d63d93015a9e630fbc334cf15098cbd8a32f22f9b` |
| `crosscheck/check_d972_r07_a0_dual_anchored_active_batch_v1.py` | 13725 | `5c2f76b825bd920245d0200f29ff860ba93a32663ef5db9567bc499a86f7ff8a` |
| `search/d972_r07_a0_dual_anchored_active_batch_gha_driver_v1.g` | 2569 | `6910d38adc56a564b4cd80211bb994de72fd77bf2da6abd8df2df5597ab9a000` |
| `sol/luna_reply_451_r07_a0_dual_anchored_batch_v1.md` | self-referential | not driver-pinned |

Pinned inputs:

- frozen rank-51 checkpoint: 10,934 bytes / `a83959e4c9fcfa79093c712e82164d47c31b78c9fc00b512f7adac9413c481f4`;
- unchanged v3 producer/runtime: 12,215 bytes / `0140447110cfa568a77300bd7d43d51c622597704b7b91ed5209c63168c9ef37`;
- Task450 v6 checker dependency: 3,590 bytes / `e902468fca7ead498e78c06496ccea596c10a1904e571f5d6b709962458b1739`.

## Implemented batch boundary

- Rank 51 is rebuilt by replaying the exact eight word-bearing records. No old live row, pivot, or dual bytes are imported.
- Each batch freezes one canonical dual/remainder/rank. Six-action hits use the existing action oracle and close as an ordinary one-row batch.
- The correction branch retains exactly the v3 v410 tau-free compiler and its existing typed stops for tau, S3--S9, and nonzero `K`.
- For the supported branch, the producer traverses `(seed, coordinate, target, fibre_cursor)` deterministically and continues after the first ACTIVE value. Every nonzero formula value is rebuilt as a literal conjugate and checked against the frozen anchor dual.
- Rows are fed to the live echelon; only actual rank rises are recorded. The canonical target remainder/dual is recomputed once when the batch closes, not once per row.
- Batch cap is 16; total new-rise cap is 64. On resume the counter starts at the sum of all already closed batch row counts, so the cap is cumulative and checked before another insertion. Each accepted row records anchor scalar, selector cursor, ancestry, direct row digest, pre/post rank, and pivot.
- Checkpoints contain only fully closed compact batches and word-bearing records. They contain no physical rows or Q0 stores.
- A resource stop in an open batch returns the last closed seal, source list, rank, round, and profile. Partially inserted rows are absent from both artifact and durable state and promote no claim.
- Producer-only empty enumeration remains `UNKNOWN_RESOURCE:SEPARATOR_REQUIRES_INDEPENDENT_EXHAUSTION`; no NONMEMBER claim is made.
- A zero post-batch remainder delegates to the existing strict positive reconstruction.

## Independent checker

- Authenticates the frozen input and final compact checkpoint seals and requires the frozen eight-record prefix exactly.
- The frozen eight rows are also semantically replayed at their successive rank-43--50 duals. One shared selective runtime binds each recorded coordinate, `target_hex`, and fibre cursor back to `delta_word`; equality-pinning the JSON is not treated as semantic authentication.
- Rebuilds rank 51 and every batch anchor independently.
- Reconstructs every literal row, checks its frozen-anchor scalar, replays the actual pivot/rank rise, and computes one post-batch dual/remainder.
- Rebuilds the declared selector fibre and kernel state. In particular, `target_hex` is recomputed from `delta_word` through the full coordinate blobs; it is not accepted as auxiliary metadata.
- Exact normalized exponent pairs are independently reconstructed for both frozen and new correction rows.
- Checker linear algebra uses the Task445 checker-side `update`/`pair`, its independently implemented v410 adjoint, and a checker-local formula compiler. It does not call v3 producer `update`, `pair`, `profile`, `tau_free_adjoint`, `compile_formulas`, or `formula_scalar`.
- RESOURCE terminals inherit the exact Task447/448 reason allowlist and phase-sensitive independent profile reconstruction. Invented budget phases or suffixes fail closed.
- Resource artifacts separate the last closed durable profile from the measured `gate_profile`; the checker reconstructs both, so coordinate/K/separator gates are not inferred from a pre-adjoint profile.
- Every artifact is bounded by at most 64 closed batch rises. `UNKNOWN_RESOURCE:max_rises` is accepted only at exactly 64; synthetic totals 63 and 65 are rejected.
- Requires deterministic cursor ordering but deliberately does not pair later rows against intervening canonical duals.
- Requires the closed terminal profile to equal the independently rebuilt post-batch profile. Positive terminals reuse the strict literal positive replay.

## Bounded gates

```text
PYTHONPYCACHEPREFIX=%TEMP%\task451_final_pycache python -m py_compile <producer> <checker>
python <producer> --mode FIXTURE --output %TEMP%\task451_final_fixture.json
python <checker> --self-test
rg -n -- "--seconds 7200|--rss-bytes 4800000000|--max-rises 64|--batch-cap 16|SELFTEST|FIXTURE" <driver>
```

Results: compile PASS; producer fixture PASS; checker self-test PASS. The toy batch tested one frozen anchor across dependent/independent candidates and one post-batch update. Mutations rejected changed anchor digest/scalar, target cursor, exact exponent, false pivot rise, changed post-batch dual, open-batch promotion, and altered rank-51 prefix.

Driver inspection confirmed one production process, external preamble, 7,200 seconds, 4.8 GB RSS, 64 rises, batch cap 16, fresh output paths, and no production fixture/self-test.

Remaining resource risk is unchanged from v3: selective Q0 construction and its three S0--S2 stores dominate memory. Batching adds only compact row ancestry/receipts and does not copy the reducer or stores.

No local heavy production, GHA dispatch, workflow edit, commit, push, or other git operation was performed. The active v6 continuation was not touched or interrupted.
