# Luna reply 444 — R07 A0 general tau-free rank ladder v2

Status: **bounded implementation complete; no production/GHA run**.

## Outputs and exact pins

| path | bytes | SHA256 |
|---|---:|---|
| `search/d972_r07_a0_actual_tau_free_rank_ladder_v2.py` | 18191 | `cd27d69b06538e77dac1963d147f4966d8f63b9bf0d9e54860f2dae69149369b` |
| `crosscheck/check_d972_r07_a0_actual_tau_free_rank_ladder_v2.py` | 7766 | `98b94c4b89d66f9a780051f2120ead0d41d3451a215bb112f3a3f389ba288641` |
| `search/d972_r07_a0_actual_tau_free_rank_ladder_gha_driver_v2.g` | 2781 | `a67e52c069478870834c6ff2760764b665433e92bc1906b759cde6b34e20a7df` |
| `sol/luna_reply_444_r07_a0_general_tau_free_rank_ladder_v2.md` | self-referential | not pinned by driver |

The v2 producer pins Task442 v1 at 16,068 bytes / `880c4fe79b28391e3fa2d439566298cf3d9d2dfdbd9759615cd3c3300049fa7a`. The independent checker additionally pins the v1 checker at 7,746 bytes / `d95d52f806aa29b497d014ee0c6efe37436b38fb6c82a745677e0c852c6730b1` only for the already independent strict positive reconstruction.

## Implemented scope

- Current-dual profiling records rank, dual/remainder digests, normalized `N1,N2`, block/label support counts, tau coefficients, unrecognized keys, and compiled required coordinates.
- For an arbitrary **localized, tau-free current dual in the existing v12 least-transversal ABI**, v410's PB3/PB4 reverse neighbourhood is rebuilt from the actual groups and central elements. Every retained old singleton coefficient is recomputed by direct pairing with `q.transform`.
- The independent checker rebuilds the complete sparse adjoint in reverse iteration order and compares its digest. It does not import the v2 producer.
- `K_i` uses exact `exp/18` normalized exponents and the identity value is compared with a fresh v12 physical seed row.
- The supported correction selector is exactly `K=0`, coordinates S0--S2. Literal conjugates, normalized exponents, physical scalar, pivot, rank transition, checkpoint replay, and strict positive reconstruction remain gated.
- Pivot validation is separated from 64-hex digest validation; the known 46-byte/92-hex pivot is accepted. Delta letters are restricted to `±1,±2`.
- A rise uses the already computed dual/remainder and one `PackedEchelon.add`; producer and checker do not perform a preceding duplicate reduction. `--max-rises` counts only rises accepted in the current invocation. No per-rise `gc.collect()` was added.

This is deliberately **not** a full arbitrary-dual/v411 implementation. The existing least-transversal ABI cannot represent that claim without a new ActorAdaptedQuotient and complete target/44-row reconstruction.

## Typed unsupported gates

- nonzero tau: `UNKNOWN_RESOURCE:NONZERO_TAU_PHASE_SELECTOR`;
- required coordinate outside S0--S2: `UNKNOWN_RESOURCE:SELECTOR_COORDINATES:S...`;
- nonzero normalized formula constant: `UNKNOWN_RESOURCE:NONZERO_CONSTANT_SELECTOR`;
- producer-only exhaustion: `UNKNOWN_RESOURCE:SEPARATOR_REQUIRES_INDEPENDENT_EXHAUSTION`.

Each gate is checkpointed and carries the current profile. None promotes EMPTY, NONMEMBER, fake, or Ihara.

## Bounded gates

Executed outside production:

```text
PYTHONPYCACHEPREFIX=%TEMP%\task444_pycache python -m py_compile <producer> <checker>
python <producer> --mode FIXTURE --output %TEMP%\task444_fixture.json
python <checker> --self-test
```

Results: compile PASS; producer emitted `status=FIXTURE`; checker emitted `...CHECKER_SELFTEST_PASS`. Mutations rejected odd and noncanonical pivots, illegal delta, and malformed digest. The fixture also exercised the 92-hex validator, resumed per-invocation rise counter, and pinned positive helper.

The local GAP wrapper could not perform its parse attempt because GAP itself failed before reading the driver with Windows runtime error `couldn't create signal pipe, Win32 error 5`. No retry, production bootstrap, Q0 enumeration, checkpoint load, download, GHA dispatch, commit, or push was performed.
