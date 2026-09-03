# Luna reply 598 — grade-one MEMBER result replay

Implemented the bounded independent result checker in
`crosscheck/check_d972_r07_a0_first_rung_grade1_decision_result_v1.mjs`.

Local checks (the exact residual is optional; no sealed candidate is present):

```text
node --check crosscheck/check_d972_r07_a0_first_rung_grade1_decision_result_v1.mjs
=> exit 0
node crosscheck/check_d972_r07_a0_first_rung_grade1_decision_result_v1.mjs --selftest
=> {"marker":"R07_GRADE1_MEMBER_RESULT_REPLAY_V1_PASS","selftest":"PASS","coefficient_two":"PASS","zero_remainder":"PASS","nonzero_remainder":"PASS","mutated_hash_rejection":"PASS"}
```

The checker independently authenticates the four decision files, frozen
v2/v3 digests, all fixed counts/ranks/parents, packed bytes, basis leads,
and the ordered GF(3) coefficient replay. Without `--residual` it sums the
selected basis rows and performs a digest-bound replay (`DIGEST_BOUND_PASS`);
with the exact sealed residual it additionally performs byte subtraction and
returns `EXACT_FILE_PASS`. No exact candidate/residual is available locally,
so no 8,059-row replay was run. It does not claim physical-row regeneration
or a cofinal lift.

`R07_GRADE1_MEMBER_RESULT_REPLAY_V1_NOT_READY`

Checker bytes: 13,729; SHA-256:
`020daede47b0bcd894723fc4562154b79426a729098ce83b7bdc7a41a26183ea`.

Exact sealed replay (provided outside the repository) completed:

```text
replay=EXACT_FILE_PASS, cursor=8059, lower=2014/1661,
grade=6398/5044, basis_sha256=b562c980c22a25a932bae1b548f72aeede5637b9612afc908fff9a9aecff069d,
residual_packed_sha256=648696895595f479b6e2ccb65332589cf8a1a3bf4cf3f92be37e7910f72b79e6,
remainder_sha256=564cbfafc869a8c6eb761a392caa5e792b546bf577af7fe808177b2fdf13cbb0,
selected_coefficients=3317, remainder_support=0
```
