# Luna Task749 -- P1 independent checker state-head schema v4

Role: Luna.  Make only the finite checker repair exposed by actual GHA run
`33814881435/1`.  Do not change producer v5, arithmetic, receipt semantics,
workflow, or any unrelated file.  Do not run the five large artifacts.

Read completely:

- `crosscheck/check_d972_r07_grade2_p1_componentwise_semantics_v3.py`
- `search/d972_r07_grade2_p1_componentwise_semantic_replay_v5.py`
- `sol/proof_r07_p1_equality_literal_lf_repair_v489.md`
- `sol/sol_reply_743_audit_r07_p1_equality_lf_v5.md`

Actual evidence:

```text
run/attempt 33814881435/1
producer prepare + four blocks + join: SUCCESS
independent checker elapsed 0.32 s, peak 41,320 KiB
stderr: {"status":"REJECTED","error":"sealed_head:prepare","verified":false}
```

The authenticated Task554 head is exactly

```json
{"body_sha256":"1f191d88a0453360021ec57d253a7d16c9a66ac059ddaaadb6db3e2b9293c865","parent_sha256":null,"schema":"d972.r07.a0.first-rung-grade1.v3.state.head","stem":"prepare"}
```

Producer v5 correctly requires
`d972.r07.a0.first-rung-grade1.v3.state.head`.  Checker v3 defines
`STATE_SCHEMA = d972.r07.a0.first-rung-grade1.v3` but `read_sealed` currently
uses `STATE_SCHEMA + ".head"`, which incorrectly requests
`d972.r07.a0.first-rung-grade1.v3.head`.  The same defect affects block heads.

Create only:

- `crosscheck/check_d972_r07_grade2_p1_componentwise_semantics_v4.py`
- `sol/luna_reply_749_r07_p1_checker_state_head_v4.md`

Requirements:

1. Copy v3 and repair only this state-head schema binding, preferably with an
   explicit sealed-head schema constant.  Preserve body schema, producer-v5
   pin, equality LF repair, nonimporting arithmetic and every live validator.
2. Make the bounded fixture use the literal authenticated
   `...v3.state.head` value rather than deriving its positive case from the
   same possibly wrong checker expression.  Add/rebind a mutation that
   replaces it by `...v3.head` and require rejection.
3. Confirm both prepare and all four block heads route through the repaired
   `read_sealed`.  Do not weaken exact key/roster/canonical-byte checks.
4. Run `py_compile` and `--selftest` only.  Compare AST/call graph with v3 and
   report every executable difference.  No real artifact download/replay,
   workflow, git, GHA, or local heavy computation.
5. Report bytes, LF, final LF, SHA-256 and exact selftest counts.  Boundary:

```text
REAL_FIVE_ARTIFACT_CHECKER=NOT_RUN
P1_SEMANTIC_REPLAY=PRODUCER_SUCCESS_CHECKER_PENDING
A0/COMMON/COFINAL/FAKE/IHARA=NOT_DECLARED
verified=false
```

