# Luna reply 445 — R07 A0 single-update tau-free rank ladder v3

Status: **bounded implementation complete; no production/GHA/git operation**.

## Exact outputs

| path | bytes | SHA256 |
|---|---:|---|
| `search/d972_r07_a0_actual_tau_free_rank_ladder_v3.py` | 12215 | `0140447110cfa568a77300bd7d43d51c622597704b7b91ed5209c63168c9ef37` |
| `crosscheck/check_d972_r07_a0_actual_tau_free_rank_ladder_v3.py` | 9683 | `8237db432c3930d9334ff6b4b557e0b1030343d4b349dd595a0a695d8a8b83f1` |
| `search/d972_r07_a0_actual_tau_free_rank_ladder_gha_driver_v3.g` | 2790 | `631c69f7d7b73be3b78ea1b3767a564c70efc8445ca6c407449d89db41679aab` |
| `sol/luna_reply_445_r07_a0_single_update_rank_ladder_v3.md` | self-referential | not driver-pinned |

The v3 producer pins the Task444 v2 producer at 18,191 bytes / `cd27d69b06538e77dac1963d147f4966d8f63b9bf0d9e54860f2dae69149369b`. The v3 checker pins the independent v2 checker at 7,766 bytes / `98b94c4b89d66f9a780051f2120ead0d41d3451a215bb112f3a3f389ba288641`; the inherited v1 source binding remains `880c4fe79b28391e3fa2d439566298cf3d9d2dfdbd9759615cd3c3300049fa7a`.

## Repairs

- Producer and checker each compute the initial state once, carry it forward, and perform exactly one post-add state computation per accepted rise. `insert` returns the post-state; progress, profile, checkpoint, and the next loop reuse it.
- Resume replay follows the same carry-forward rule. There is only one state-update definition in each v3 file.
- A synthetic `R`-rise fixture asserts exactly `R+1` state computations in both producer and checker.
- The adjoint performs one `q.transform({k:1})` per old candidate. No identical assertion call remains.
- Existing budget/RSS checks now cover deterministic intervals of localized-dual scanning, reverse-neighbourhood construction, old-candidate evaluation, and every seed formula compilation. Fibre-loop checks are retained.
- No pre-add `reduce(row)`, unconditional `gc.collect`, new cache, closure, quotient, search family, or mathematical claim was added.
- The checker reads the repo-relative checkpoint, authenticates exact bytes/SHA, independently derives its binding, verifies the internal canonical seal, and requires exact accepted list/count, rank, round, reason, and profile agreement.
- Correction sources require a lowercase 64-hex adjoint digest and a two-integer exact exponent pair.
- Checker boundaries now require `terminal == status` and the complete fixed claims object. Resource reasons use a strict allowlist. Tau, unrecognized-key, selector-coordinate, normalized-constant, and separator gates are tied to independently reconstructed data. Time/RSS and rise-cap gates remain typed non-promoting resource terminals.
- All current-profile fields are independently rebuilt: normalized exponents, block/label counts, tau coefficients, rejected keys, required coordinates, rank, target pairing, dual/remainder digests, and adjoint statistics when present.

The mathematical scope is unchanged from Task444: localized tau-free duals in the existing least-transversal ABI, S0--S2, and `K=0`. Nonzero tau, S3--S9, and `K != 0` remain measured `UNKNOWN_RESOURCE` gates; v411 is not claimed.

## Bounded gates

Executed with repository-external bytecode/output paths:

```text
PYTHONPYCACHEPREFIX=%TEMP%\task445_pycache2 python -m py_compile <v3 producer> <v3 checker>
python <v3 producer> --mode FIXTURE --output %TEMP%\task445_fixture2.json
python <v3 checker> --self-test
rg -n "gc\.collect|\.reduce\(row\)|q\.transform\(\{k:1\}\)" <v3 producer> <v3 checker>
```

Results:

- compile: PASS;
- producer fixture: `status=FIXTURE`, three synthetic rises / four state computations;
- checker self-test: PASS, four synthetic rises / five state computations;
- checkpoint mutation rejection: rank, binding, and internal state seal;
- inherited pivot/delta mutations: odd pivot, noncanonical pivot, illegal delta, malformed digest;
- hot-path scan: no `gc.collect`, no pre-add `reduce(row)`, exactly one producer old-candidate `q.transform({k:1})` occurrence.

Diff confinement: v3 is a thin versioned successor over v2; changes are limited to state carry-forward, deterministic cap calls, removal of the proven transform duplication, durable checkpoint authentication, stricter validation/profile/claim gates, v3 driver pins, and bounded fixtures. No production, Q0 enumeration, checkpoint load, GHA dispatch, workflow edit, commit, or push was performed.
