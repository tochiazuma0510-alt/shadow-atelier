# Luna reply 454: Task451-carrier-fed task193 compiler v5

Status: **IMPLEMENTED / BOUNDED GATES PASS / PRODUCTION NOT RUN**

## Exact outputs

| path | bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_second_frattini_affine_prefix_compiler_v5.py` | 12207 | `fab51e296170ac34ebe48b49d79d3460017a51cd797d524e7b0d89481f23960f` |
| `crosscheck/check_d972_r07_second_frattini_affine_prefix_compiler_v5.py` | 7795 | `941eab0d9c60726436c866427de04b7c25b4ae1934fbf0a1d464f2010a7e2b9e` |
| `search/d972_r07_second_frattini_affine_prefix_compiler_gha_driver_v5.g` | 2269 | `d2cab901ae608d88bcff6dacdee6072c780b9157e1955cbaa740d227a8f2fe7a` |

No optional repository fixture was created.

## Reuse and firewall boundary

- All three Task452 and all three task193-v4 owners are exact-pinned.
- The producer and checker separately authenticate carrier/verdict canonical seals, exact positive schemas/terminals/claims, verdict-to-physical-carrier identity, Task451 source pins/input provenance, freely reduced literal triple, 760-letter g760, right product, full replay, exact exponent/joint flags, hexagon/printed pentagon conventions, and the historical u32be sparse digest.
- The normalized in-memory boundary and `minimal_input` are the only values passed across the firewall. No old history-free adapter receipt is forged or loaded.
- The producer calls the frozen v4 `load_owner()` and its rank-zero `actual_compile`; ordinary rows, pointed rows, equality oracle, and presentation mathematics are inherited unchanged. The checker makes an in-memory v4 compatibility view and invokes the frozen v4 `check_result` plus its patched independent v1 affine/Fox replay. It does not import v5 producer code.
- Foreign/v4 resume input is rejected. A resource terminal carries a fresh v5 checkpoint schema, exact carrier/verdict input identity, and `resumable=false` because v5 has no resume implementation. All non-PASS claims remain false.
- The checker normalizes the v4 shim inner artifact keys to `adapter_receipt`/`adapter_verdict`, then reseals both the v4 view and the final v1 independent-replay view. Its bounded synthetic gate executes this exact transformation and rejects stale seals.
- The JSON verdict ABI is fixed to schema `d972-r07-second-frattini-affine-prefix-compiler/v5/checker-verdict/v5`, terminal `R07_SECOND_FRATTINI_AFFINE_PREFIX_COMPILER_V5`, and claims `independent_carrier_authentication=true`, `independent_task193_replay=true`, `pointed_rows=true` with A2/lift/fake/Ihara false. The stdout `...V5_CHECKER_PASS` marker remains separate for the driver.

## Bounded gates

```text
python -m py_compile search/d972_r07_second_frattini_affine_prefix_compiler_v5.py crosscheck/check_d972_r07_second_frattini_affine_prefix_compiler_v5.py
python -B search/d972_r07_second_frattini_affine_prefix_compiler_v5.py --fixture --output %TEMP%\task454_fixture3.json
python -B crosscheck/check_d972_r07_second_frattini_affine_prefix_compiler_v5.py --self-test
```

Terminals:

```text
R07_SECOND_FRATTINI_AFFINE_PREFIX_COMPILER_V5_PRODUCER_TERMINAL FIXTURE
R07_SECOND_FRATTINI_AFFINE_PREFIX_COMPILER_V5_CHECKER_SELFTEST_PASS mutations=15 inner_key_transform=true final_reseal=true verdict_abi=true actual_task451_positive=false
```

The fixture is firewall/minimal-input only and asserts no task193 value. It executes the firewall and rejects 16 concrete mutations covering carrier seal, verdict identity, both schemas/terminals, claims, correction, g760/right product, sparse digest, full replay, exponent, joint kernel, hexagon, pentagon, and source pins.

No A0/Task452/task193 production, GHA, workflow edit, commit, push, or credential operation was performed.
