# Task426 v8 — final memory patch

Implemented only the four authorized v8 outputs. The v7 search and quotient logic was copied without broadening the search; only the three specified dispatch blockers were changed.

## Repairs

1. The checker now separates `seal()` (bounded chunk hashing/counting of the compressed tail) from `decode_checkpoint()` (one direct `gzip.GzipFile`/`marshal.load` pass). It has no `BytesIO`, no unbounded `f.read()`, and no `io` import. Input checkpoints use seal-only identity checking; an existing output checkpoint is decoded once and reused for durable agreement, output identity, and `UNKNOWN_RESOURCE` reporting.

2. Producer `run()` restores the authenticated scalar summary, checks RSS immediately, and returns `UNKNOWN` with `MEMORY_STATE_LIMIT` before calling `save()` or `cp_write()` when the restored state is at the cap. The ordinary work guard still force-saves and returns `UNKNOWN_RESOURCE` on time/RSS stops. The toy fixture exercises the no-save memory-state branch.

3. Producer `main()` computes `final_durable = o.get("durable_state") or LAST_DURABLE` once and uses it for both result telemetry and checkpoint sequence. The fallback fixture proves a candidate-shaped result retains the nonzero sealed sequence.

The v8 checker accepts the absent-output `MEMORY_STATE_LIMIT` case for ordinary `UNKNOWN`, while still requiring and validating an output checkpoint for `UNKNOWN_RESOURCE`. `COMMON_WORD` remains rejected and all public promotion flags remain false.

## Gates

```text
python -m py_compile search/d972_r07_a0_pb34_direct_quotient_owner_v8.py crosscheck/check_d972_r07_a0_pb34_direct_quotient_owner_v8.py
python -B search/d972_r07_a0_pb34_direct_quotient_owner_v8.py --mode FIXTURE
python -B crosscheck/check_d972_r07_a0_pb34_direct_quotient_owner_v8.py --self-test
```

Results:

```text
R07_A0_PB34_DIRECT_QUOTIENT_OWNER_V8 FIXTURE_PASS
R07_A0_PB34_DIRECT_QUOTIENT_CHECKER_V8_PASS {"fresh_object_mutation_gates":3,"status":"FIXTURE_PASS"}
```

No production run, GHA dispatch, commit, or push was performed.

## Exact output seals

| output | bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_a0_pb34_direct_quotient_owner_v8.py` | 26006 | `777955b05c919a3b2c5f108e84e10e672f44ea259dd85ac4a343116aae08b5fc` |
| `crosscheck/check_d972_r07_a0_pb34_direct_quotient_owner_v8.py` | 7390 | `a3ad40ec2dc92ca8213905b858edca92cbdfacf1a700e6715624edec985d3976` |
| `search/d972_r07_a0_pb34_direct_quotient_owner_gha_driver_v8.g` | 2896 | `1b7ab8511e76b991d04b2649f5753f33436bbf9d7fee5187af07051a31f1dcc1` |

The driver pins the producer/checker bytes and SHA-256 values above, uses unique v8 paths, the 4.8 GB RSS cap, live tee logs, and resumes only from an existing immutable input checkpoint.

V8_LOCAL_GO_FOR_PARENT_DISPATCH
