# Luna reply 430 — v11 finite central-power API fix

Implemented only the four task430 v11 outputs. The v10 owner is cloned with
versioned identifiers updated to v11/task430. The three `h0` power calls now
use the exact finite helper:

```python
central_power3(group, value, exponent)
```

It accepts only exponents `0,1,2` and uses `identity`, the value, or one
`mul(value,value)`. No generic power loop/cache or surrounding PB3/PB4 formula
was changed. The producer fixture uses a toy group exposing only `identity`
and `mul`, checks outputs for `0,1,2`, rejects `-1,3`, and checks the source
contains no `.power(` or `.pow(` token.

Final output pins:

- `search/d972_r07_a0_pb34_direct_quotient_owner_v11.py`: 27430 bytes, SHA-256 `b6ae32a89dfd0cd8afc540bc09089ef3722e489d4fdef574a8bd42540a1bfd63`
- `crosscheck/check_d972_r07_a0_pb34_direct_quotient_owner_v11.py`: 7401 bytes, SHA-256 `3dd65ccc71cf834674f2198458c4ecf4eea936a4e9cfca8c5e72e0dd10d9c8fd`
- `search/d972_r07_a0_pb34_direct_quotient_owner_gha_driver_v11.g`: 2903 bytes, SHA-256 `37e8c2893142ba5f7b0fe721a0b0033c15f37d9966b6a2c268ceb7854d957fb0`

The driver pins both v11 Python outputs, requires external
`D972_R07_A0_PB34_V11_RUN:=true`, uses fresh v11 artifact/checkpoint/log paths,
9000 seconds, 4.8 GB, one producer and one checker with live `tee`, and v11
markers.

Bounded local gates:

```text
python -m py_compile search/d972_r07_a0_pb34_direct_quotient_owner_v11.py crosscheck/check_d972_r07_a0_pb34_direct_quotient_owner_v11.py
PASS (exit 0)

python -B search/d972_r07_a0_pb34_direct_quotient_owner_v11.py --mode FIXTURE
R07_A0_PB34_DIRECT_QUOTIENT_OWNER_V11 FIXTURE_PASS
PASS (exit 0)

python -B crosscheck/check_d972_r07_a0_pb34_direct_quotient_owner_v11.py --self-test
R07_A0_PB34_DIRECT_QUOTIENT_CHECKER_V11_PASS {"fresh_object_mutation_gates":3,"status":"FIXTURE_PASS"}
PASS (exit 0)
```

Static search found no executable `V10`, `v10`, or `task429` identifiers and no
`.power(` / `.pow(` token in the v11 producer/checker. The Windows real
bootstrap and production search were not run.

V11_LOCAL_GO_FOR_PARENT_AUDIT_AND_DISPATCH
