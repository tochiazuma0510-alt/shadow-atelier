# Luna reply 429 — v10 component-origin fix

Implemented only the four task429 outputs. v10 preserves the v9 owner logic
and introduces one normalization boundary for raw component keys:

```text
raw_component_zero(block, component) = component - 1
```

The helper validates E3 raw components `1..3` and E4 raw components `1..6`.
`Quotient.transform` decodes the raw component once and passes the normalized
zero-based value to the existing formulas. No `comp=6` special case, sign,
translation, contraction, normal-section, actor, or aggregation logic was
changed. The fixture checks all nine legal mappings, rejects E3 `0,4` and E4
`0,7`, and checks E4 raw six maps to internal five.

Unexpected top-level exceptions which become `UNKNOWN` now carry only bounded
diagnostic scalars: exception type, existing reason, and a traceback limited to
24 frames / 12 KiB. Resource and candidate paths are unchanged and receive no
traceback field.

Output pins:

- `search/d972_r07_a0_pb34_direct_quotient_owner_v10.py`: 26758 bytes, SHA-256 `2a7ab84e8644579afa9137840eb0c018ba65065f0d07143ac9e46cfc7bbcdc15`
- `crosscheck/check_d972_r07_a0_pb34_direct_quotient_owner_v10.py`: 7399 bytes, SHA-256 `95b6348c75f1ea7316904b432f51e1a53caa84a4bdd5ac985bf1c6ec3c1c4acf`
- `search/d972_r07_a0_pb34_direct_quotient_owner_gha_driver_v10.g`: 2904 bytes, SHA-256 `f98a84b50eefa65e21f80fb964099b43ec9be71bac9fb5e7fd9591fe6628856e`

The driver pins both v10 Python files, requires the external preamble
`D972_R07_A0_PB34_V10_RUN:=true`, uses fresh v10 paths, 9000 seconds, the
4.8 GB cap, one producer and one checker with live `tee`, and distinct v10
markers.

Bounded local gates:

```text
python -m py_compile search/d972_r07_a0_pb34_direct_quotient_owner_v10.py crosscheck/check_d972_r07_a0_pb34_direct_quotient_owner_v10.py
PASS (exit 0)

python -B search/d972_r07_a0_pb34_direct_quotient_owner_v10.py --mode FIXTURE
R07_A0_PB34_DIRECT_QUOTIENT_OWNER_V10 FIXTURE_PASS
PASS (exit 0)

python -B crosscheck/check_d972_r07_a0_pb34_direct_quotient_owner_v10.py --self-test
R07_A0_PB34_DIRECT_QUOTIENT_CHECKER_V10_PASS {"fresh_object_mutation_gates":3,"status":"FIXTURE_PASS"}
PASS (exit 0)
```

The Windows real bootstrap and production search were not run. The v9-to-v10
producer diff is restricted to version/schema/marker text, the single
component-origin helper and use, its bounded fixture assertions, and bounded
unexpected-`UNKNOWN` telemetry.

V10_LOCAL_GO_FOR_PARENT_DISPATCH
