# Luna reply 599 — independent grade-one full-routing replay

Implemented the standalone NumPy checker
`crosscheck/check_d972_r07_a0_first_rung_grade1_full_routing_v1.py` and the
candidate-only workflow
`.github/workflows/d972-r07-a0-grade1-independent-routing-v1.yml`.
Checker bytes: 26,358; SHA-256
`8e159cc262fd35d61018da4b30db45017534546f7bbe89ebd001b3dbff6286d8`.

Bounded local evidence:

```text
python -B -m py_compile crosscheck/check_d972_r07_a0_first_rung_grade1_full_routing_v1.py
=> exit 0
python -B crosscheck/check_d972_r07_a0_first_rung_grade1_full_routing_v1.py --selftest
=> {"coefficient_2":"PASS","fixture":"PASS","old_lower":"PASS","packed_echelon":"PASS"}
```

The checker independently authenticates the sealed prepare/four-block chain,
the exact Task595 four-file candidate, source residual, packed basis/leads,
and the full 2,014-old plus 6,045-block route. It has not been run against
the 8,059-row artifact locally; GHA is the only authorized full replay.
Expected source run/attempt is `33677346616/1`, candidate run/attempt is
`33707397894/1`, candidate commit is
`93f746ad1b649796e1bc28e00ff34993498929ee`, candidate body digest is
`62412762b3a208d31febb6c6b8d4707f880471ed32cf62c79c18108065ab7b5d`, and
the expected routed basis digest is
`b562c980c22a25a932bae1b548f72aeede5637b9612afc908fff9a9aecff069d`.

Readiness: `NOT_READY_NO_LOCAL_FULL_REPLAY`. Production output remains a
candidate; `verified=false` and `cross_checked=false` are emitted by the
verdict until root inspects the independent receipt.

`R07_GRADE1_FULL_ROUTING_REPLAY_V1_NOT_READY`
