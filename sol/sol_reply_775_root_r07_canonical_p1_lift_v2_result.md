# Root result 775 — canonical P1 degree-two lift workflow v2

## Exact run identity

- workflow run/attempt: `33824881796/1`
- job: `100875303915`
- head: `8bcc7182b4b6676ce4f752f61ad5ffee99d11926`
- audited producer: `search/d972_r07_canonical_p1_dag_degree2_lift_v5.py`
  (`32ee4c536e0f5289a13bcd71723bfc6cfc8bd52f074008b78ba2acaca7d6466b`)
- audited workflow:
  `.github/workflows/d972-r07-canonical-p1-dag-degree2-lift-v2.yml`
  (`be01039bf16bdb917d717979b4b309d3bebb1a6f60b9ccf95a5e17b8a1715d20`)

## Actual result

Authentication, bounded selftest, semantic-checker receipt, all five parent
downloads, and launch-manifest construction passed.  The serial production
build then stopped after `50.62 s` with:

```json
{"status":"REJECTED","error":"object supporting the buffer API required","verified":false}
```

`/usr/bin/time -v` recorded `48.13 s` user time, `2.43 s` system time, and
maximum RSS `5,196,492 KiB`.  This is below both the 8-GiB process ulimit and
the workflow's 7-GiB RSS gate.  The stop is therefore a finite Python buffer-
type interface defect, not timeout, OOM, or a mathematical NONMEMBER result.
No candidate lift or checkpoint was produced.

The always-uploaded log artifact is:

- artifact id: `9919602334`
- name: `task767-canonical-p1-degree2-lift-v2-logs-33824881796-1`
- API archive bytes: `82,608`
- digest:
  `sha256:a604edf4ca38bcb318a919f0c1076d7f5623643238235a0bd0758ca391d26340`

Luna Task773 is restricted to a versioned, arithmetic-neutral runtime-type
repair.  It must add bounded traceback/call-site telemetry so this opaque
failure cannot recur, and it may not add a heavy local replay or a duplicate
dense owner.  A fresh Sol audit is required before root dispatches v3.

```text
CANONICAL_P1_LIFT=NOT_PRODUCED
FAILURE_CLASS=FINITE_RUNTIME_TYPE_INTERFACE
TIMEOUT=no
OOM=no
MATHEMATICAL_NONMEMBER=NOT_CLAIMED
FAKE_IHARA=NOT_CLAIMED
verified=false
```

