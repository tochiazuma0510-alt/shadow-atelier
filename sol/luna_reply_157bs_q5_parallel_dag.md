# Luna reply 157bs — q5 parallel DAG

## Verdict

The versioned q5 parallel DAG is ready.  Only the authorized workflow and
this reply were changed.  No local GAP, Git, push, dispatch, or GHA run was
performed.

## Authorized asset

Created:

```text
.github/workflows/d972-burau-q5-parallel-v1.yml
```

The workflow has three matrix stages:

```text
calibration-check (q3, q4)   ─────────────┐
                                          ├─ q5-check (a=2, a=4)
q5-produce (a=2, a=4)        ─────────────┘
```

`q5-produce` has no `needs` edge, so both producer lanes start concurrently
with the independent q3/q4 calibration lanes.  Each `q5-check` lane depends
on both complete matrix jobs and is fail-closed unless the aggregate
calibration and producer results are successful.

The calibration lanes authenticate the old-run artifact by API id, unique
name, compressed size, run id, and non-expired state, then authenticate the
receipt SHA and all frozen v4 metadata before running the repaired checker.
They upload the receipt, checker log/status, and a seal binding run,
attempt, artifact id/name/size, receipt SHA, producer/checker SHAs, q/a,
972 rows, and the unique successful checker marker.

The producer lanes authenticate both pinned calibration artifacts and
receipts, current producer/checker source hashes, all roof/order/word/row
metadata, and the 972-row index ledger before invoking the unchanged q5
producer.  They always upload raw receipt/log evidence and a producer seal;
resource, malformed, non-admissible, or non-unique terminal output cannot be
accepted as a result.

The final lanes download only same-run, attempt-specific calibration and q5
artifacts, reauthenticate every seal/hash and the q5 log marker counts, and
run the repaired checker with both calibration receipts.  Checked evidence
and a concise step summary are uploaded on every outcome.  Artifact names
are lane- and attempt-specific.  The workflow has read-only permissions,
`persist-credentials: false`, Python 3.13.5, hash-pinned SymPy/mpmath,
`ulimit -v 12000000`, 360-minute job limits, `workflow_dispatch`, and the
requested restricted push paths.

## Frozen bindings

```text
calibration run: 32051744038
q3 artifact: 9296644565  d972-burau-tuple-v4-calibration-q3-attempt1  size=95607
q4 artifact: 9297445824  d972-burau-tuple-v4-calibration-q4-attempt1  size=95523
q3 receipt SHA256: 0813a151cd47a56f29aab629ebfc35a0293a8ce84d98c24f3a3ac3e0601ad8e2
q4 receipt SHA256: 414c13fe680c2eeb6f3f75c7f6a7206a707c18a426da619543232e1a98855de2
producer SHA256:   aa8726570c58840a000b4b247b34eccd39a958f97087e6745216e2055b578cec
checker SHA256:    e0b4cb923c1bd73b9afdc7f47de739f91c8aa3c0d7764c239e1df76d74fbce14
```

The final workflow also uses the corrected mpmath hash consistently in all
three dependency-install blocks.

## Static checks

Executed without running the workflow:

```text
YAML_PARSE_PASS jobs=['calibration_check', 'q5_check', 'q5_produce']
EMBEDDED_PY_COMPILE_PASS blocks=8
BASH_STATIC_BLOCK_AUDIT_PASS run_blocks=16 python_heredocs=8 escaped_interpolations=0
FROZEN_CONSTANTS_PASS 9
DAG_SHAPE_STATIC_PASS
```

The independent source hashes currently observed locally are:

```text
search/d972_b4_burau_fiber_v4.py          AA8726570C58840A000B4B247B34ECCD39A958F97087E6745216E2055B578CEC
search/check_d972_b4_burau_fiber_v4.py    E0B4CB923C1BD73B9AFDC7F47DE739F91C8AA3C0D7764C239E1DF76D74FBCE14
search/certs/d972_b4_word_key_artifact_v1_20260816.json
                                             564A921BE8114BDEB963F679C121E8D9AA90E148C65E95E393874FCBA843E9F9
```

Final workflow SHA256:

```text
.github/workflows/d972-burau-q5-parallel-v1.yml
59218F8FC4750EABCF63A93BEDFED9BB44FE3CF9F3095790EFE1E50EE2CDAF9B
```

Q5_PARALLEL_DAG_READY
