# Luna Task 757 — P1 checker body-schema v5 + checker-only GHA v3

## 0. Scope

Create only:

- `crosscheck/check_d972_r07_grade2_p1_componentwise_semantics_v5.py`
- `.github/workflows/d972-r07-p1-semantic-checker-only-v3.yml`
- `sol/luna_reply_757_r07_p1_checker_body_schema_v5_and_gha.md`

Do not overwrite prior versions. No git/push/GHA/real artifact download.

## 1. Checker v5

Read v497 and use checker-v4 as source. Sole production semantic change:

```python
STATE_SCHEMA = "d972.r07.a0.first-rung-grade1.v3.state"
```

Keep `SEALED_HEAD_SCHEMA = "d972.r07.a0.first-rung-grade1.v3.state.head"`.
Add bounded literal fixture accepting the exact distinct body/HEAD strings and
rejecting missing suffixes and swaps. Do not change arithmetic, result schema,
terminal marker, CLI, parents, 65,340 obligation set, or downstream flags.

## 2. Workflow v3

Use checker-only workflow v2 as source. It must:

- trigger only its own path on the same branch;
- require `[fire-r07-p1-checker-only-v3]`;
- pin checker-v5 exact bytes/LF/SHA and v497 exact bytes/LF/SHA;
- preserve v2's honest `completed/failure` producer run and exact eight-job gate;
- reuse producer artifact `9916479231`, six receipts and five parents;
- run only checker-v5 actual arithmetic; no producer rerun;
- preserve 345/360 minute caps, memory/thread caps, canonical result checks,
  success-only output and always logs;
- version only workflow receipt/name to v3. Checker output schema/marker remain v1.

## 3. Bounded checks and reply

Run safe YAML parse, py_compile and `--selftest`. Report exact hashes/counts and:

```text
REAL_GHA=NOT_RUN
P1_SEMANTICS_CROSS_CHECKED=NO
A0/COMMON/COFINAL/FAKE/IHARA=NOT_DECLARED
verified=false
```
