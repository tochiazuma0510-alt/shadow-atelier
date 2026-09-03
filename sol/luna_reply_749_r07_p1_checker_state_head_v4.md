# Luna Task749 -- P1 independent checker state-head schema v4

```text
RESULT=COMPLETE
REAL_FIVE_ARTIFACT_CHECKER=NOT_RUN
P1_SEMANTIC_REPLAY=PRODUCER_SUCCESS_CHECKER_PENDING
A0/COMMON/COFINAL/FAKE/IHARA=NOT_DECLARED
verified=false
```

Created only the finite checker successor and this reply.  Producer v5,
arithmetic, receipt semantics, provenance pins, and CLI are unchanged.  The
checker now binds sealed heads through the explicit constant
`SEALED_HEAD_SCHEMA = d972.r07.a0.first-rung-grade1.v3.state.head`; body
schema remains `d972.r07.a0.first-rung-grade1.v3`.  Both `authenticate_prepare`
and `authenticate_block` continue to route through `read_sealed`, so prepare
and all four block heads use the repaired binding.

The bounded fixture writes canonical prepare and four block sealed heads with
the literal authenticated `...v3.state.head` schema, reads all five through
`read_sealed`, then replaces the prepare schema by the old
`...v3.head` value and requires rejection.  Exact key, roster, canonical-byte,
body-hash, producer-v5, and live validator checks remain strict.  The fixture
root is isolated from the existing safe-root toy fixture.

## v3-to-v4 executable difference audit

The complete diff has only these executable changes:

1. Add the `SEALED_HEAD_SCHEMA` string constant.
2. Change `read_sealed` expected-head schema from `STATE_SCHEMA + ".head"`
   to `SEALED_HEAD_SCHEMA`.
3. Extend `selftest` with a small `write_fixture_head` helper, five positive
   `read_sealed` calls, one literal old-schema rejection mutation, and a
   `sealed_head_schema` live-kernel/acceptance entry.
4. Put the pre-existing safe-root toy file under a dedicated `toy` directory
   so the new sealed fixture files cannot affect its exact roster.

No other top-level function, call target, import, arithmetic path, receipt
validator, producer pin, or CLI branch differs from checker v3.

## Exact receipts

| path | bytes | LF | final LF | SHA-256 |
|---|---:|---:|:---:|---|
| `crosscheck/check_d972_r07_grade2_p1_componentwise_semantics_v4.py` | `132129` | `2719` | yes | `cc9a27e8ab447ecd6e4fbebbd1240195e442d6c5eb14241a5f9d7c669154ee19` |
| `crosscheck/check_d972_r07_grade2_p1_componentwise_semantics_v3.py` | `130683` | `2689` | yes | `3cfdbe0485711b9b4a08db2d664ded7719a126e3a499724d33cd122a101e774e` |
| `search/d972_r07_grade2_p1_componentwise_semantic_replay_v5.py` | `41619` | `382` | yes | `dc5931c3fd3ad5d1a947346599824b02ad1d7b5f699361c05f1f051076dcbdcf` |
| `sol/proof_r07_p1_equality_literal_lf_repair_v489.md` | `2771` | `69` | yes | `14e4d33967cea1a26d1cb41c11ab125abad2cc9d5455e3c85e0377987832c789` |
| `sol/sol_reply_743_audit_r07_p1_equality_lf_v5.md` | `12090` | `228` | yes | `a3b4a3719c6464b795a2e0a935d1366cd727674aad39609f193af271a422377f` |

The reply's own digest is supplied post-seal rather than embedded, avoiding a
self-referential receipt.

## Bounded checks

```text
python -m py_compile crosscheck/check_d972_r07_grade2_p1_componentwise_semantics_v4.py
exit 0

python -B crosscheck/check_d972_r07_grade2_p1_componentwise_semantics_v4.py --selftest
exit 0
fixture_accept=7
rejections=42
sealed_head_schema=PASS
actual_five_artifact_check=DEFERRED_TO_GHA
verified=false
```

No real artifact download, five-parent replay, checker `--check`, workflow,
GHA, Git, or local heavy computation was performed.
