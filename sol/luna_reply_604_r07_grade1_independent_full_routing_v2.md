# Luna reply 604 — grade-one independent full-routing v2

Created the unlaunched v2 checker with the terminal bytes adapter repaired
and the five narrow Task602 repairs: a real old-lower companion fixture,
mandatory `queue_exhausted: true` on every block, boolean-any/argmax first
lead search in the reduction hot loop, and internal time/RSS guards after
route exhaustion and immediately before verdict output. Routing arithmetic,
source/candidate pins, row order, and verdict semantics are unchanged.

Bounded checks:

```text
python -B -m py_compile crosscheck/check_d972_r07_a0_first_rung_grade1_full_routing_v2.py
=> exit 0
python -B crosscheck/check_d972_r07_a0_first_rung_grade1_full_routing_v2.py --selftest
=> {"canonical_zero":"PASS","coefficient_2":"PASS","fixture":"PASS","mutated_remainder_rejection":"PASS","nonzero_remainder_rejection":"PASS","old_lower":"PASS","packed_echelon":"PASS"}
```

Checker bytes: 27,778; SHA-256
`a0504ae6a2562aab3b9af5ba7ed672bcc87bbd1cfdf5cc9fd3489240e51008e3`.
The v2 workflow uses the v2 trigger/artifacts, pins this checker and this
reply, and retains the exact source/candidate downloads with 40/45/60-minute
bounds.

The prior v1 run promoted nothing: basis/ranks matched, terminal adapter
failed at `target_reduction`, and no verdict was produced. No local full
replay, GHA dispatch, git operation, or production execution was performed.

`R07_GRADE1_FULL_ROUTING_REPLAY_V2_NOT_READY`
